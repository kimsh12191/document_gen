"""④ 가져오기 (이미지 묶음): 문서 이미지 뭉치 → 사내 OCR → 포맷·양식 묶기 → 사람이 포맷마다 정한다 (DESIGN.md 8.1~8.5).
API 는 studio/api_import.py, 화면은 static/js/import.js. 묶기 계산은 studio/formats.py, 결과 폴더 묶음은 studio/results.py.

묶음 폴더 <workspace_dir>/imports/<묶음>/
  batch.json      이름, 출처(폴더·올린 파일·생성 데이터), 실서류 여부, 공개 서식 표시, OCR 설정, 단계
  pages.jsonl     쪽마다 {id, doc, source, page, image(OCR 이 본 그림), width, height, sha, ocr(원본 응답 경로), fp(지문)}
  formats.json    포맷·양식 묶기 결과와 사람의 결정 {"formats": [...], "fixed": {쪽 id: 묶음 이름}}
  pages/          PDF 를 쪽마다 그린 그림, 올린 파일
원본 폴더(import_dir 아래)는 읽기만 한다.

OCR 은 1부 OCR 준비 단계(ocr/bank_ocr)와 같은 코드·같은 캐시 규칙이다: EXIF 회전을 적용한 그림을 <OCR 캐시>/images/<픽셀 해시>.png
로 두고 그 그림으로 OCR 을 부르며, 결과는 <OCR 캐시>/ocr/<digest(픽셀 해시, ocr_callable, ocr_revision)>.json. 1부의 cache_dir 을
studio 설정 ocr.cache_dir 로 두면 1부에서 이미 읽은 쪽은 다시 부르지 않는다.

명령줄 (studio 작업이 이것을 돌린다)
  python -m studio.importer ocr <묶음 폴더>          OCR (없는 쪽만) → 지문 → 묶기
  python -m studio.importer group <묶음 폴더>        지문·묶기만 다시
  python -m studio.importer form-prints [서식ID…]    기존 서식 지문 (가까운 기존 서식 찾기용, studio_cache/form_prints/)
  python -m studio.importer from-docgen <묶음 폴더>  시험용: 생성 데이터로 묶음 채우기 (OCR 대신 합성 정답)
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OCR_DIR = ROOT / "ocr"   # 1부 OCR 코드 (bank_ocr). 명령줄로 돌 때도 불러 쓴다
if str(OCR_DIR) not in sys.path:
    sys.path.insert(0, str(OCR_DIR))
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
PRINTS = ROOT / "studio_cache" / "form_prints"


def _slug(s: str) -> str:
    return re.sub(r"[^\w.-]+", "-", s).strip("-") or "batch"


def _jsonl(p: Path) -> list[dict]:
    return [json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip()] if p.exists() else []


def _write_jsonl(p: Path, rows: list[dict]) -> None:
    tmp = p.with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    tmp.replace(p)


def _write_json(p: Path, obj) -> None:
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(p)


# ---------------------------------------------------------------------------
# 묶음 만들기
# ---------------------------------------------------------------------------

def create_batch(ws: Path, name: str, source: str | None, real_data: bool = True, public: bool = False,
                 ocr: dict | None = None, import_dir: str | None = None, kind: str = "folder") -> dict:
    """이미지·PDF 폴더(또는 생성 데이터)로 묶음을 만든다. 쪽 목록만 만들고 OCR 은 작업으로 돌린다."""
    bdir = ws / "imports" / _slug(name)
    if bdir.exists():
        raise ValueError(f"이미 있는 묶음 이름입니다: {_slug(name)}")
    if kind == "folder":
        src = Path(source or "").expanduser()
        if not src.is_dir():
            raise ValueError(f"폴더가 없습니다: {src}")
        if import_dir and Path(import_dir).resolve() not in [src.resolve(), *src.resolve().parents]:
            raise ValueError(f"가져올 폴더는 설정의 import_dir ({import_dir}) 아래여야 합니다")
    bdir.mkdir(parents=True)
    (bdir / "pages").mkdir()
    batch = {"name": _slug(name), "created": time.strftime("%Y-%m-%d %H:%M"), "source": {"kind": kind, "path": source},
             "real_data": bool(real_data), "public": bool(public), "ocr": ocr or {}, "stage": "listed"}
    pages = list_pages(bdir, Path(source)) if kind in ("folder", "upload") else []
    _write_json(bdir / "batch.json", batch)
    _write_jsonl(bdir / "pages.jsonl", pages)
    return {**batch, "n_pages": len(pages)}


def list_pages(bdir: Path, src: Path) -> list[dict]:
    """폴더 안의 이미지(한 장 = 문서 하나)와 PDF(쪽마다 그림, 파일 하나 = 문서 하나)."""
    rows = []
    for p in sorted(src.rglob("*")):
        rel = p.relative_to(src).as_posix()
        if p.suffix.lower() in IMAGE_EXT:
            rows.append({"id": rel, "doc": rel, "source": str(p), "page": 1})
        elif p.suffix.lower() == ".pdf":
            import pymupdf

            with pymupdf.open(p) as doc:
                for k, page in enumerate(doc):
                    out = bdir / "pages" / f"{rel.replace('/', '__')}_p{k + 1}.png"
                    if not out.exists():
                        page.get_pixmap(matrix=pymupdf.Matrix(200 / 72, 200 / 72), alpha=False).save(str(out))
                    rows.append({"id": f"{rel}#p{k + 1}", "doc": rel, "source": str(out), "page": k + 1, "pdf": str(p)})
    if not rows:
        raise ValueError(f"{src}: 이미지(png·jpg·tif…)나 PDF 가 없습니다")
    return rows


def from_docgen(bdir: Path) -> None:
    """시험용 묶음: docgen 합성 OCR 데이터(docgen.ocr_set, prepare 없이)를 만들어 그 정답 OCR 을 사내 OCR 결과처럼 쓴다.
    쪽마다 진짜 서식 ID(truth)를 알기 때문에 묶기 정확도를 잴 수 있고, 사내 OCR 없이 가져오기·검수 흐름을 끝까지 볼 수 있다."""
    from docgen.ocr_set import build

    recipe = bdir / "recipe.json"
    build(argparse.Namespace(recipe=str(recipe), out=str(bdir / "gen"), workers=1, scale=2.0, no_prepare=True))
    rows = []
    for m in _jsonl(bdir / "gen" / "manifest.jsonl"):
        k = int(m["page_id"].rsplit("/p", 1)[1])
        rows.append({"id": m["page_id"], "doc": m["document_id"], "source": m["image"], "page": k, "ocr_json": m["ocr_json"],
                     "truth": m["document_id"].rsplit("_", 1)[0]})
    _write_jsonl(bdir / "pages.jsonl", rows)
    run_ocr(bdir)
    res = run_group(bdir)
    print(f"포맷 {len(res['formats'])}개")


# ---------------------------------------------------------------------------
# OCR (1부와 같은 규칙)
# ---------------------------------------------------------------------------

def _ocr_settings(batch: dict) -> dict:
    o = dict(batch.get("ocr") or {})
    o.setdefault("callable", "internal_ocr_adapter:ocr_from_file")
    o.setdefault("revision", "")
    o.setdefault("cache_dir", str(ROOT / "studio_cache" / "ocr"))
    if not o.get("mapping"):
        o["mapping"] = json.loads((OCR_DIR / "config.example.json").read_text(encoding="utf-8"))["mapping"]
    return o


def run_ocr(bdir: Path) -> None:
    import os

    from bank_ocr.data import canonical_image, digest, dumps, exif_orientation, load_callable, parse_ocr, write_json

    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    o = _ocr_settings(batch)
    if o.get("base_url"):
        os.environ.setdefault("INTERNAL_OCR_BASE_URL", o["base_url"])
    cache = Path(o["cache_dir"])
    rows = _jsonl(bdir / "pages.jsonl")
    need = [r for r in rows if not r.get("ocr")]
    adapter = None
    if any(not r.get("ocr_json") for r in need):
        if not o.get("revision"):
            raise SystemExit("OCR 설정이 없습니다 (studio/config.json 의 ocr.callable·revision). 사내 OCR 은 내부망에서만 쓸 수 있습니다")
        adapter = load_callable(o["callable"])
    for n, r in enumerate(rows, 1):
        if r.get("ocr"):
            continue
        im = canonical_image(r["source"])
        sha = digest(str(im.size).encode() + im.tobytes())
        staged = cache / "images" / f"{sha}.png"
        if not staged.exists():
            staged.parent.mkdir(parents=True, exist_ok=True)
            im.save(staged)
        r.update(image=str(staged), width=im.width, height=im.height, sha=sha)
        if r.get("ocr_json") and exif_orientation(r["source"]) in (None, 1):
            raw_path = Path(r["ocr_json"])
            parse_ocr(json.loads(raw_path.read_text(encoding="utf-8")), im.width, im.height, o["mapping"])
            r["ocr"] = str(raw_path)
        else:
            key = digest(dumps([sha, o["callable"], o["revision"]]).encode())
            cached = cache / "ocr" / f"{key}.json"
            if not cached.exists():
                raw = adapter(str(staged))
                if raw is None:
                    raise SystemExit(f"OCR 실패: {r['id']}")
                parse_ocr(raw, im.width, im.height, o["mapping"])
                write_json(cached, raw)
            r["ocr"] = str(cached)
        im.close()
        print(f"\rOCR {n}/{len(rows)}", end="", file=sys.stderr, flush=True)
        if n % 20 == 0:
            _write_jsonl(bdir / "pages.jsonl", rows)
    print(file=sys.stderr)
    _write_jsonl(bdir / "pages.jsonl", rows)
    batch["stage"] = "ocr_done"
    _write_json(bdir / "batch.json", batch)


def page_words(r: dict, mapping: dict, reviewed: Path | None = None) -> list[dict]:
    from bank_ocr.data import parse_ocr

    src = reviewed if reviewed and reviewed.exists() else Path(r["ocr"])
    return parse_ocr(json.loads(src.read_text(encoding="utf-8")), r["width"], r["height"], mapping)


# ---------------------------------------------------------------------------
# 묶기
# ---------------------------------------------------------------------------

def run_group(bdir: Path) -> dict:
    from . import formats as F

    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    o = _ocr_settings(batch)
    rows = _jsonl(bdir / "pages.jsonl")
    fx = json.loads((bdir / "formats.json").read_text(encoding="utf-8")) if (bdir / "formats.json").exists() else {}
    fixed = fx.get("fixed", {})
    old = {f["id"]: f for f in fx.get("formats", [])}
    docs = []
    first = {r["doc"]: r["id"] for r in rows if r.get("ocr") and r.get("page", 1) == 1}
    follow = {}   # 여러 쪽 문서(PDF·생성 데이터)의 뒷쪽은 그 문서 첫 쪽의 포맷을 따른다: 포맷 = 문서 종류
    for r in rows:
        if not r.get("ocr"):
            continue
        if not r.get("fp"):
            words = [{"text": w["text"], "bbox": w["bbox"], "line_num": w.get("line_num")} for w in page_words(r, o["mapping"])]
            fp = F.fingerprint(words, r["width"], r["height"])
            r["fp"] = {k: fp[k] for k in ("tokens", "layout", "heads", "title", "name")}
            r["n_words"] = len(words)
        if r.get("page", 1) > 1 and r["doc"] in first and r["id"] not in fixed:
            follow[r["id"]] = first[r["doc"]]
            continue
        docs.append({"id": r["id"], "fp": r["fp"]})
    _write_jsonl(bdir / "pages.jsonl", rows)
    assign = F.cluster(docs, fixed=fixed)
    for pid, head in follow.items():
        assign[pid] = assign[head]
    groups: dict[int, list[str]] = {}
    for r in rows:
        if r["id"] in assign:
            groups.setdefault(assign[r["id"]], []).append(r["id"])
    by_id = {r["id"]: r for r in rows}
    prints = load_form_prints()
    formats = []
    for n, ids in sorted(groups.items()):
        members = [{"id": i, "fp": by_id[i]["fp"]} for i in ids if i not in follow]
        va = F.variants(members)
        for i in ids:
            if i in follow:
                va[i] = va.get(follow[i], 0)
        titles = Counter(by_id[i]["fp"]["title"] for i in ids if by_id[i]["fp"].get("title") and i not in follow)
        names = Counter(by_id[i]["fp"]["name"] for i in ids if i not in follow) or Counter(by_id[i]["fp"]["name"] for i in ids)
        name = titles.most_common(1)[0][0] if titles else names.most_common(1)[0][0]
        # 이전 결정 이어 받기: 같은 쪽을 가장 많이 가진 이전 포맷
        prev = max(old.values(), key=lambda f: len(set(f["pages"]) & set(ids)), default=None)
        keep = prev if prev and len(set(prev["pages"]) & set(ids)) > len(ids) / 2 else None
        fid = keep["id"] if keep else f"f{n + 1}"
        while fid in {f["id"] for f in formats}:
            fid += "b"
        sim = []
        if prints:
            toks = [set(by_id[i]["fp"]["tokens"]) for i in ids]
            sim = sorted(({"form": k, "name": v["name"], "score": round(F.centroid_sim(set(v["tokens"]), toks), 3)}
                          for k, v in prints.items()), key=lambda x: -x["score"])[:3]
        docs_of: dict[str, list[str]] = {}
        for i in ids:
            docs_of.setdefault(by_id[i]["doc"], []).append(i)
        formats.append({"id": fid, "name": (keep or {}).get("name") or name, "pages": ids, "docs": docs_of,
                        "variants": {str(k): [i for i in ids if va[i] == k] for k in sorted(set(va.values()))},
                        "decision": (keep or {}).get("decision"), "similar": sim})
    out = {"formats": formats, "fixed": fixed, "grouped": time.strftime("%Y-%m-%d %H:%M")}
    _write_json(bdir / "formats.json", out)
    batch["stage"] = "grouped"
    _write_json(bdir / "batch.json", batch)
    return out


def merge_formats(bdir: Path, src: str, dst: str) -> dict:
    fx = json.loads((bdir / "formats.json").read_text(encoding="utf-8"))
    fs = {f["id"]: f for f in fx["formats"]}
    if src not in fs or dst not in fs:
        raise KeyError(src if src not in fs else dst)
    for p in fs[src]["pages"] + fs[dst]["pages"]:
        fx["fixed"][p] = f"keep:{dst}"
    _write_json(bdir / "formats.json", fx)
    return run_group(bdir)


def split_pages(bdir: Path, page_ids: list[str], name: str = "") -> dict:
    fx = json.loads((bdir / "formats.json").read_text(encoding="utf-8"))
    tag = f"split:{int(time.time() * 1000)}"
    for p in page_ids:
        fx["fixed"][p] = tag
    _write_json(bdir / "formats.json", fx)
    out = run_group(bdir)
    if name:
        for f in out["formats"]:
            if set(f["pages"]) == set(page_ids):
                f["name"] = name
        _write_json(bdir / "formats.json", out)
    return out


def set_decision(bdir: Path, fid: str, decision: dict | None, name: str | None = None) -> dict:
    fx = json.loads((bdir / "formats.json").read_text(encoding="utf-8"))
    for f in fx["formats"]:
        if f["id"] == fid:
            if decision is not None:
                if decision.get("kind") not in (None, "template", "existing", "skip"):
                    raise ValueError("결정은 template / existing / skip")
                f["decision"] = decision if decision.get("kind") else None
            if name is not None:
                f["name"] = name
            for p in f["pages"]:   # 사람이 이름·결정을 정한 포맷은 다시 묶어도 그대로
                fx["fixed"].setdefault(p, f"keep:{fid}")
            break
    else:
        raise KeyError(fid)
    _write_json(bdir / "formats.json", fx)
    return fx


# ---------------------------------------------------------------------------
# 기존 서식 지문 (가까운 기존 서식 찾기)
# ---------------------------------------------------------------------------

def load_form_prints() -> dict:
    out = {}
    for f in PRINTS.glob("*.json") if PRINTS.exists() else []:
        out[f.stem] = json.loads(f.read_text(encoding="utf-8"))
    return out


def build_form_prints(ids: list[str] | None = None) -> int:
    """서식마다 seed 0 으로 렌더링해 쪽 전체 글자(합성 OCR 정답)로 첫 쪽 지문을 만든다."""
    import tempfile

    from docgen.entities import make_profile
    from docgen.image import ImageRenderer
    from docgen.ocr_export import background_words, page_items
    from docgen.preview import source_hash
    from docgen.registry import load_all
    from docgen.render import render

    from . import formats as F

    reg = load_all()
    ids = ids or list(reg)
    PRINTS.mkdir(parents=True, exist_ok=True)
    n = 0
    with tempfile.TemporaryDirectory() as d, ImageRenderer(2.0) as R:
        for k, i in enumerate(ids, 1):
            out = PRINTS / f"{i}.json"
            h = source_hash(i, common=False)
            if out.exists() and json.loads(out.read_text(encoding="utf-8")).get("hash") == h:
                continue
            spec = reg[i]
            html, _, _ = render(spec, make_profile(0), 0)
            info = R.render(html, Path(d) / f"{i}.png", texts=True)
            bg = background_words(i) if spec.group in ("hana", "imported") else {}
            items = page_items([t for t in info["texts"] if t["page"] == 0], bg.get(0, []), 2 * 96 / 72, "word")
            words = [{"text": x["text"], "bbox": [x["bounding"]["vertices"][0]["x"], x["bounding"]["vertices"][0]["y"],
                                                  x["bounding"]["vertices"][2]["x"], x["bounding"]["vertices"][2]["y"]],
                      "line_num": x["line_num"]} for x in items]
            fp = F.fingerprint(words, info["pages"][0]["width"], info["pages"][0]["height"])
            out.write_text(json.dumps({"name": spec.name, "hash": h, "tokens": fp["tokens"]}, ensure_ascii=False), encoding="utf-8")
            n += 1
            print(f"\r서식 {k}/{len(ids)}", end="", file=sys.stderr, flush=True)
    print(file=sys.stderr)
    return n


# ---------------------------------------------------------------------------
# 템플릿으로 (overlay(image) 서식 만들기)
# ---------------------------------------------------------------------------

def _solve3(m: list[list[float]], v: list[float]) -> list[float] | None:
    """3x3 연립방정식 (가우스 소거). 풀 수 없으면 None."""
    a = [row[:] + [x] for row, x in zip(m, v)]
    for c in range(3):
        p = max(range(c, 3), key=lambda i: abs(a[i][c]))
        if abs(a[p][c]) < 1e-9:
            return None
        a[c], a[p] = a[p], a[c]
        for i in range(3):
            if i != c:
                f = a[i][c] / a[c][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[c])]
    return [a[i][3] / a[i][i] for i in range(3)]


def _affine(src: list[tuple[float, float]], dst: list[tuple[float, float]]):
    """src → dst 최소제곱 아핀 변환 (x' = ax+by+c, y' = dx+ey+f)."""
    m = [[0.0] * 3 for _ in range(3)]
    vx, vy = [0.0] * 3, [0.0] * 3
    for (x, y), (u, w) in zip(src, dst):
        row = (x, y, 1.0)
        for i in range(3):
            for j in range(3):
                m[i][j] += row[i] * row[j]
            vx[i] += row[i] * u
            vy[i] += row[i] * w
    px, py = _solve3(m, vx), _solve3(m, vy)
    if px is None or py is None:
        return None
    return lambda x, y: (px[0] * x + px[1] * y + px[2], py[0] * x + py[1] * y + py[2])


def _aligned(ref: list[dict], other: list[dict]) -> list[dict]:
    """other 를 ref 좌표로 옮긴다 (스캔·촬영 쪽의 밀림·기울기·크기): 양쪽에 한 번씩만 나오는 같은 글자들의 중심으로 아핀 변환을
    맞추고, 크게 어긋나는 짝(같은 글자가 우연히 다른 자리)을 빼고 한 번 더 맞춘다. 짝이 모자라면 그대로."""
    from .formats import norm_text

    def once(ws):
        c = Counter(norm_text(w["text"]) for w in ws)
        return {norm_text(w["text"]): w for w in ws if c[norm_text(w["text"])] == 1 and len(norm_text(w["text"])) >= 2}
    ctr = lambda w: ((w["bbox"][0] + w["bbox"][2]) / 2, (w["bbox"][1] + w["bbox"][3]) / 2)  # noqa: E731
    a, b = once(ref), once(other)
    pairs = [(ctr(b[k]), ctr(a[k])) for k in a if k in b]
    if len(pairs) < 4:
        return other
    f = None
    for _ in range(2):
        f = _affine([s for s, _ in pairs], [d for _, d in pairs])
        if f is None:
            return other
        err = sorted(((f(*s)[0] - d[0]) ** 2 + (f(*s)[1] - d[1]) ** 2, s, d) for s, d in pairs)
        keep = err[: max(4, int(len(err) * 0.7))]
        pairs = [(s, d) for _, s, d in keep]
    out = []
    for w in other:
        x0, y0 = f(w["bbox"][0], w["bbox"][1])
        x1, y1 = f(w["bbox"][2], w["bbox"][3])
        out.append({**w, "bbox": [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]})
    return out


def value_drafts(sample: list[list[dict]], others: list[list[list[dict]]], sizes: list[tuple[float, float]]) -> dict:
    """같은 포맷 문서끼리 견줘 견본 쪽의 값 자리를 찾는다: 다른 문서 60% 이상에서 같은 자리에 같은 글자가 있으면 서식 글자,
    아니면 값. 같은 줄에 붙은 값 단어를 한 자리로 묶어 지우기(주변색) + 글자 칸 초안(항목명 = 왼쪽(없으면 위) 서식 글자)으로.
    sample[k] = 견본 k쪽 단어 (px), others[d][k] = 다른 문서 d 의 k쪽 단어, sizes[k] = 견본 k쪽 (너비, 높이) px. 결과 좌표는 px."""
    from .formats import norm_text

    erase, add = [], []
    for k, words in enumerate(sample):
        W, H = sizes[k]
        def seen(w, ws):   # 다른 문서 쪽 ws 의 같은 자리에 같은 글자가 있나
            t = norm_text(w["text"])
            cx, cy = (w["bbox"][0] + w["bbox"][2]) / 2, (w["bbox"][1] + w["bbox"][3]) / 2
            return any(norm_text(o["text"]) == t and abs((o["bbox"][0] + o["bbox"][2]) / 2 - cx) < 0.04 * W
                       and abs((o["bbox"][1] + o["bbox"][3]) / 2 - cy) < 0.02 * H for o in ws)
        peers = [_aligned(words, o[k]) for o in others if len(o) > k and o[k]]
        # 겉모습만 비슷한 다른 서식(한 포맷에 섞인 재직·경력증명서 등)은 빼고 견준다: 견본 글자가 거의 안 겹치는 문서
        probe = [w for w in words if len(norm_text(w["text"])) >= 2]
        ratio = [sum(seen(w, ws) for w in probe) / max(1, len(probe)) for ws in peers]
        top = max(ratio, default=0)
        peers = [ws for ws, x in zip(peers, ratio) if x >= max(0.25, 0.6 * top)]
        if not peers:
            continue
        need = math.ceil(0.6 * len(peers))   # 다른 문서 둘이면 둘 다: 우연히 같은 값(같은 시·도, "주식회사")을 서식 글자로 보지 않게
        flags = [not norm_text(w["text"]) or sum(seen(w, ws) for ws in peers) >= need for w in words]
        # 기호만인 단어(@ , - …)는 항목명도 값 사이 경계도 아니다 (값 자리를 묶을 때 그 사이 기호는 사각형에 함께 들어간다)
        fix = [w for w, f in zip(words, flags) if f and norm_text(w["text"])]
        lines: list[list[dict]] = []   # 값 단어를 줄로 (세로 중심이 글자 높이 절반 안) → 줄마다 왼쪽부터
        for w in sorted((w for w, f in zip(words, flags) if not f), key=lambda w: (w["bbox"][1] + w["bbox"][3]) / 2):
            cy, h = (w["bbox"][1] + w["bbox"][3]) / 2, w["bbox"][3] - w["bbox"][1]
            if lines and abs(sum((x["bbox"][1] + x["bbox"][3]) / 2 for x in lines[-1]) / len(lines[-1]) - cy) < 0.5 * h:
                lines[-1].append(w)
            else:
                lines.append([w])
        var = [w for ln in lines for w in sorted(ln, key=lambda w: w["bbox"][0])]
        groups: list[list[dict]] = []
        for w in var:
            h = w["bbox"][3] - w["bbox"][1]
            g = groups[-1] if groups else None
            if g:
                last = g[-1]
                same_line = abs((last["bbox"][1] + last["bbox"][3]) / 2 - (w["bbox"][1] + w["bbox"][3]) / 2) < 0.5 * h
                gap = w["bbox"][0] - last["bbox"][2]
                between = any(f["bbox"][0] >= last["bbox"][2] - 1 and f["bbox"][2] <= w["bbox"][0] + 1
                              and abs((f["bbox"][1] + f["bbox"][3]) / 2 - (w["bbox"][1] + w["bbox"][3]) / 2) < 0.5 * h for f in fix)
                if same_line and -h < gap < 2.0 * h and not between:
                    g.append(w)
                    continue
            groups.append([w])
        for g in groups:
            x0, y0 = min(w["bbox"][0] for w in g), min(w["bbox"][1] for w in g)
            x1, y1 = max(w["bbox"][2] for w in g), max(w["bbox"][3] for w in g)
            h, cy = y1 - y0, (y0 + y1) / 2
            left = [f for f in fix if f["bbox"][2] <= x0 + 1 and abs((f["bbox"][1] + f["bbox"][3]) / 2 - cy) < 0.6 * h]
            above = [f for f in fix if f["bbox"][3] <= y0 + 1 and y0 - f["bbox"][3] < 3 * h and f["bbox"][0] < x1 and f["bbox"][2] > x0]
            lab = max(left, key=lambda f: f["bbox"][2], default=None) or max(above, key=lambda f: f["bbox"][3], default=None)
            label = lab["text"] if lab else ""
            if lab and lab in left:   # 띄어 쓴 항목명 ("소 재 지"): 왼쪽으로 붙어 있는 서식 글자를 이어 붙인다
                run = [lab]
                for f in sorted(left, key=lambda f: -f["bbox"][2]):
                    if f is not lab and 0 <= run[-1]["bbox"][0] - f["bbox"][2] < 1.5 * h and len(run) < 6:
                        run.append(f)
                parts = [f["text"] for f in reversed(run)]
                label = "".join(parts) if all(len(p) == 1 for p in parts) else " ".join(parts)
            pad = max(1.5, 0.15 * h)
            rect = [max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad)]
            erase.append({"page": k, "rect": rect, "fill": "auto"})
            add.append({"t": "text", "page": k, "label": label, "rect": rect,
                        "note": "가져오기 초안: " + " ".join(w["text"] for w in g)[:40]})
    return {"erase": erase, "add": add}


def create_template(bdir: Path, fid: str, page_ids: list[str], form_id: str, name: str, private_dir: str | None,
                    drafts: bool = True) -> dict:
    """견본 쪽 그림을 배경으로 하는 overlay(image) 서식. 영역은 비어 있고 영역 편집기에서 그린다.
    실서류에서 온 묶음은 private_forms_dir 에만 만든다 (공개 서식으로 표시한 묶음만 저장소의 docgen/forms/images)."""
    from docgen import realform as RF

    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    if not re.fullmatch(r"img_[a-z0-9_]{2,40}", form_id):
        raise ValueError("서식 ID 는 img_ 로 시작하는 영어 소문자·숫자·밑줄 (예: img_payslip_a)")
    from docgen.registry import load_all

    if form_id in load_all() or RF.image_form_dir(form_id):
        raise ValueError(f"이미 있는 서식 ID: {form_id}")
    if batch.get("real_data") and not batch.get("public"):
        if not private_dir:
            raise ValueError("실서류 묶음에서 만든 서식은 private_forms_dir 에만 둡니다. 설정에 private_forms_dir 을 정하세요")
        root = Path(private_dir)
    else:
        root = RF.IMAGE_FORMS
    rows = {r["id"]: r for r in _jsonl(bdir / "pages.jsonl")}
    o = _ocr_settings(batch)
    dest = root / form_id
    dest.mkdir(parents=True)
    pages, texts = [], []
    for k, pid in enumerate(page_ids):
        r = rows[pid]
        shutil.copyfile(r["image"], dest / f"page_{k}.png")
        pages.append({"width": round(r["width"] / RF.BG_ZOOM, 2), "height": round(r["height"] / RF.BG_ZOOM, 2), "from": pid})
        for w in page_words(r, o["mapping"]):   # 배경 그림 속 글자 (합성 OCR 정답용, 지운 곳은 빠짐)
            texts.append({"page": k, "text": w["text"], "rect": [round(v / RF.BG_ZOOM, 2) for v in w["bbox"]],
                          "line": w.get("line_num") or 0})
    lay = {"name": name, "class": "가져온 서식", "from_batch": batch["name"], "format": fid, "pages": pages, "items": [],
           "texts": texts, "created": time.strftime("%Y-%m-%d %H:%M"), "private": root != RF.IMAGE_FORMS}
    (dest / "layout.json").write_text(json.dumps(lay, ensure_ascii=False, indent=1), encoding="utf-8")
    n_drafts = 0
    if drafts:   # 같은 포맷의 다른 문서와 견줘 값 자리 초안 → 서식 폴더의 overrides.json (영역 편집기에서 "추가"·"지우기"로 보인다)
        fx = json.loads((bdir / "formats.json").read_text(encoding="utf-8"))
        f = next((x for x in fx["formats"] if x["id"] == fid), None)
        docs = (f or {}).get("docs") or {}
        sample_doc = rows[page_ids[0]]["doc"]
        va = {p: k for k, ps in ((f or {}).get("variants") or {}).items() for p in ps}
        same = [d for d, ids in docs.items() if d != sample_doc and va.get(ids[0]) == va.get(page_ids[0])]
        pick = same + [d for d in docs if d != sample_doc and d not in same]   # 같은 변형 먼저 (최대 12개)
        others = [[page_words(rows[p], o["mapping"]) for p in docs[d]] for d in pick[:12]]
        if others:
            sample = [page_words(rows[p], o["mapping"]) for p in page_ids]
            dr = value_drafts(sample, others, [(rows[p]["width"], rows[p]["height"]) for p in page_ids])
            to_pt = lambda r: [round(v / RF.BG_ZOOM, 2) for v in r]  # noqa: E731
            ov = {"erase": [{**e, "rect": to_pt(e["rect"])} for e in dr["erase"]],
                  "add": [{**a, "rect": to_pt(a["rect"])} for a in dr["add"]]}
            (dest / "overrides.json").write_text(json.dumps(ov, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            n_drafts = len(ov["add"])
    set_decision(bdir, fid, {"kind": "template", "form_id": form_id, "dir": str(dest)})
    return {"form_id": form_id, "dir": str(dest), "private": lay["private"], "drafts": n_drafts}


# ---------------------------------------------------------------------------
# OCR 벤치마크로 (1부 prepare)
# ---------------------------------------------------------------------------

def ocr_set_files(bdir: Path, out: Path, format_ids: list[str] | None, gt: str, split: str, reviewed_dir: Path | None,
                  prepare: dict | None = None) -> dict:
    """묶음의 쪽들로 1부 manifest·설정을 만든다. gt=reviewed 면 OCR 검수에서 확인한 쪽만, 그 검수본을 정답으로."""
    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    fx = json.loads((bdir / "formats.json").read_text(encoding="utf-8")) if (bdir / "formats.json").exists() else {"formats": []}
    pick = None if not format_ids else {p for f in fx["formats"] if f["id"] in format_ids for p in f["pages"]}
    rows = [r for r in _jsonl(bdir / "pages.jsonl") if r.get("ocr") and (pick is None or r["id"] in pick)]
    done = set()
    if gt == "reviewed":
        from .ocr_review import reviewed_pages

        done = reviewed_pages(reviewed_dir, batch["name"]) if reviewed_dir else set()
        rows = [r for r in rows if r["id"] in done]
        if not rows:
            raise ValueError("OCR 검수에서 확인한 쪽이 없습니다")
    out.mkdir(parents=True, exist_ok=False)
    man = []
    for r in rows:
        ocr = (reviewed_dir / batch["name"] / f"{_safe(r['id'])}.json") if gt == "reviewed" else Path(r["ocr"])
        man.append({"document_id": r["doc"], "page_id": r["id"], "image": r["image"], "split": split, "ocr_json": str(ocr)})
    _write_jsonl(out / "manifest.jsonl", man)
    cfg = json.loads((OCR_DIR / "config.example.json").read_text(encoding="utf-8"))
    o = _ocr_settings(batch)
    cfg.update({"manifest": str((out / "manifest.jsonl").resolve()), "output_dir": str((out / "prepared").resolve()),
                "cache_dir": str((out / "ocr_cache").resolve()), "ocr_revision": o.get("revision") or "saved-ocr",
                "mapping": o["mapping"]})
    if gt == "reviewed":   # 사람이 확인한 정답: 신뢰도 필터가 고친 글자를 빼지 않게
        cfg["reference_type"] = "human_reviewed"
        cfg["filters"] = {"train": {"min_confidence": 0.0, "min_length": 1, "max_length": 100},
                          "benchmark": {"min_confidence": 0.0, "min_length": 1, "max_length": 100}}
    for k, v in (prepare or {}).items():
        cfg[k] = v
    if split == "benchmark":
        cfg["benchmark_only"] = True
    cfg["studio"] = {"source": "images" if batch["source"]["kind"] != "results" else "results", "gt": gt,
                     "real_data": bool(batch.get("real_data")), "batch": batch["name"]}
    (out / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
    names = {f["id"]: f["name"] for f in fx["formats"]}
    info = {"batch": batch["name"], "source": batch["source"], "gt": gt, "split": split, "real_data": bool(batch.get("real_data")),
            "ocr_revision": cfg["ocr_revision"], "created": time.strftime("%Y-%m-%d %H:%M:%S"), "pages": len(man),
            "documents": len({m["document_id"] for m in man}),
            "formats": {fid: names.get(fid, fid) for fid in (format_ids or names)}}
    (out / "import_set.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"pages": len(man), "config": str(out / "config.json")}


def _safe(page_id: str) -> str:
    return page_id.replace("/", "__").replace("#", "_").replace("\\", "__")


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="studio.importer")
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("ocr")
    o.add_argument("batch")
    g = sub.add_parser("group")
    g.add_argument("batch")
    fp = sub.add_parser("form-prints")
    fp.add_argument("ids", nargs="*")
    dg = sub.add_parser("from-docgen", help="시험용: recipe.json 이 있는 묶음 폴더를 생성 데이터로 채운다")
    dg.add_argument("batch")
    a = ap.parse_args(argv)
    if a.cmd == "from-docgen":
        from_docgen(Path(a.batch))
    elif a.cmd == "ocr":
        run_ocr(Path(a.batch))
        res = run_group(Path(a.batch))
        print(f"포맷 {len(res['formats'])}개")
    elif a.cmd == "group":
        res = run_group(Path(a.batch))
        print(f"포맷 {len(res['formats'])}개")
    else:
        print(f"서식 지문 {build_form_prints(a.ids or None)}개 새로 만듦")


if __name__ == "__main__":
    main()
