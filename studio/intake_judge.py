"""④ 서류 넣기 ❷ 양식 정리 (studio/DESIGN.md 15.3·15.4): 묶인 모양마다 기존 서식인지 새 서식인지 판정하고, 쓸 길(서식으로·원본 데이터로)과
추출 키 → 공통 키 잇기를 제안하며, 새 서식이면 추출값 위치로 값 칸 초안과 값을 지운 배경 미리보기를 만든다.
결정은 formats.json 의 모양마다 "intake" 에 둔다 (반영은 ❸). 묶음 폴더는 studio/importer.py 와 같다.

  judge(묶음)        모양마다 {판정 제안, 가까운 기존 서식 3, 쓸 길, 추출 키와 공통 키 제안, 저장된 결정}
  decide(묶음, …)    사람의 결정 저장
  draft(묶음, 모양)  견본 문서 + 값 칸(추출값 위치·키) + 지울 자리 + 지운 배경 그림 (drafts/<모양>_p<쪽>.png)

  python -m studio.intake_judge <묶음 폴더> [--truth truth.json] [--exclude 서식ID,…]   판정 정확도 (시험 폴더 정답으로)
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from . import importer as IM

MATCH = 0.4          # 기존 서식 지문과 이 이상이면 '기존 서식과 같음'으로 제안 (시험 폴더로 정함, DESIGN 15.6 3번)
TEMPLATE_MIN = 3     # 새 모양이 이만큼 이상 서류면 '서식으로'도 켠다 (적으면 원본 데이터로만)


def _load(bdir: Path):
    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    rows = {r["id"]: r for r in IM._jsonl(bdir / "pages.jsonl")}
    fx = json.loads((bdir / "formats.json").read_text(encoding="utf-8"))
    return batch, rows, fx


def _pred(batch: dict, doc: str) -> list[dict]:
    from .results import pred_items

    p = (batch.get("results") or {}).get("pred", {}).get(doc)
    return pred_items(json.loads(Path(p).read_text(encoding="utf-8"))) if p and Path(p).is_file() else []


def _plain(tokens) -> frozenset:
    """자리(@세로 칸) 없는 글자 조각만. 스캔·사진처럼 기울거나 밀린 쪽도 같은 서식으로 잰다."""
    return frozenset(t for t in tokens if "@" not in t)


def _print_pages(v: dict) -> list[frozenset]:
    return [_plain(p["tokens"]) for p in v.get("pages") or []] or [_plain(v["tokens"])]


def similar(members: list[set], prints: dict, n: int = 3) -> list[dict]:
    """기존 서식 지문 중 가까운 것 n개. 서식마다 레이아웃·쪽 지문 가운데 가장 가까운 것으로 잰다."""
    from .formats import Cluster

    c = Cluster()
    for m in members:
        c.add(_plain(m))
    return sorted(({"form": k, "name": v["name"], "score": round(max(c.sim(t) for t in _print_pages(v)), 3)}
                   for k, v in prints.items()), key=lambda x: -x["score"])[:n]


def judge(bdir: Path, exclude: set[str] = frozenset(), threshold: float | None = None) -> list[dict]:
    from docgen import dictionary as DIC

    threshold = MATCH if threshold is None else threshold
    batch, rows, fx = _load(bdir)
    prints = {k: v for k, v in IM.load_form_prints().items() if k not in exclude}
    out = []
    for f in fx["formats"]:
        heads = [ids[0] for ids in f["docs"].values()]   # 문서마다 첫 쪽 지문
        members = [set(rows[p]["fp"]["tokens"]) for p in heads if rows.get(p, {}).get("fp")]
        sim = similar(members, prints) if prints and members else []
        n_docs = len(f["docs"])
        top = sim[0] if sim else None
        if top and top["score"] >= threshold:
            dt = DIC.doc_type_of(top["form"])
            name = DIC.doc_name(top["form"], top["name"])[0]
            suggest = {"kind": "existing", "form_id": top["form"], "doc_type": dt, "doc_name": name, "score": top["score"]}
            uses = {"template": False, "raw": True}
        else:
            suggest = {"kind": "new", "score": top["score"] if top else 0.0}
            uses = {"template": n_docs >= TEMPLATE_MIN, "raw": True}
        keys: dict[str, dict] = {}
        for d in f["docs"]:
            for it in _pred(batch, d):
                k = keys.setdefault(it["key"], {"key": it["key"], "docs": 0, "label": it.get("label") or "", "example": it.get("value")})
                k["docs"] += 1
        dt = suggest.get("doc_type")
        for k in keys.values():
            k["common"] = DIC.match_extracted(k["key"], dt)
        out.append({"id": f["id"], "name": f["name"], "n_docs": n_docs, "n_pages": len(f["pages"]), "sample": f["pages"][0],
                    "similar": sim, "suggest": suggest, "uses": uses, "keys": sorted(keys.values(), key=lambda x: -x["docs"]),
                    "with_pred": sum(1 for d in f["docs"] if _pred(batch, d)), "decision": f.get("intake")})
    out.sort(key=lambda x: -x["n_docs"])
    return out


def decide(bdir: Path, decisions: dict[str, dict]) -> dict:
    """{모양 ID: {kind: existing|new|skip, form_id?, name?, uses: {template, raw}, keymap: {추출 키: 공통 키|None}}} 저장."""
    fx = json.loads((bdir / "formats.json").read_text(encoding="utf-8"))
    by = {f["id"]: f for f in fx["formats"]}
    from docgen.registry import load_all

    reg = load_all()
    for fid, d in decisions.items():
        if fid not in by:
            raise KeyError(fid)
        if d.get("kind") not in ("existing", "new", "skip"):
            raise ValueError(f"{fid}: kind 는 existing · new · skip")
        if d["kind"] == "existing" and d.get("form_id") not in reg:
            raise ValueError(f"{fid}: 기존 서식 ID 가 없습니다 ({d.get('form_id')})")
        uses = d.get("uses") or {}
        by[fid]["intake"] = {"kind": d["kind"], **({"form_id": d["form_id"]} if d["kind"] == "existing" else {}),
                             **({"name": d["name"].strip()} if d.get("name") else {}),
                             "uses": {"template": bool(uses.get("template")) and d["kind"] == "new", "raw": bool(uses.get("raw"))},
                             "keymap": {k: v for k, v in (d.get("keymap") or {}).items()}}
        for p in by[fid]["pages"]:   # 사람이 정한 모양은 다시 묶어도 그대로
            fx["fixed"].setdefault(p, f"keep:{fid}")
    IM._write_json(bdir / "formats.json", fx)
    return {"saved": len(decisions)}


def _fill(img, rect):
    """사각형을 둘레 색(가장자리 픽셀의 중앙값)으로 칠한다 — 영역 편집기의 '주변색' 지우기와 같은 생각."""
    from statistics import median

    x0, y0, x1, y1 = (int(round(v)) for v in rect)
    W, H = img.size
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W - 1, x1), min(H - 1, y1)
    if x1 <= x0 or y1 <= y0:
        return
    px = img.load()
    ring = [px[x, y] for x in range(x0, x1 + 1, 2) for y in (max(0, y0 - 2), min(H - 1, y1 + 2))] + \
           [px[x, y] for y in range(y0, y1 + 1, 2) for x in (max(0, x0 - 2), min(W - 1, x1 + 2))]
    color = tuple(int(median(c[i] for c in ring)) for i in range(3)) if ring else (255, 255, 255)
    from PIL import ImageDraw

    ImageDraw.Draw(img).rectangle([x0, y0, x1, y1], fill=color)


def draft(bdir: Path, fid: str) -> dict:
    """새 서식 초안: 추출값이 가장 많이 위치를 가진 문서(평가 쪽 건은 빼고)를 견본으로, 값 칸 = 추출값 위치(키·공통 키·값), 지울 자리 = 값 칸 + (같은 모양
    문서가 여럿이면) 문서마다 달라지는 글자 중 값 칸 밖의 것(남은 값 후보). 지운 배경 그림을 drafts/ 에 쓴다."""
    from docgen import dictionary as DIC
    from PIL import Image

    batch, rows, fx = _load(bdir)
    f = next((x for x in fx["formats"] if x["id"] == fid), None)
    if f is None:
        raise KeyError(fid)
    o = IM._ocr_settings(batch)
    keymap = (f.get("intake") or {}).get("keymap") or {}
    from .intake_raw import test_docs

    held = test_docs(bdir)   # 평가로 뺀 건의 서류는 서식 배경으로 쓰지 않는다 (모두 평가 쪽이면 어쩔 수 없이 쓴다)
    cands = [d for d in f["docs"] if d not in held] or list(f["docs"])
    best, best_n = None, -1
    for d in cands:
        n = sum(1 for it in _pred(batch, d) if it.get("bbox_2d"))
        if n > best_n:
            best, best_n = d, n
    pages = f["docs"][best]
    regions = []
    for it in _pred(batch, best):
        b, k = it.get("bbox_2d"), int(it.get("page", 1)) - 1
        if not b or k >= len(pages):
            continue
        r = rows[pages[k]]
        W, H = r["width"], r["height"]
        rect = [b[0] * W / 1000, b[1] * H / 1000, b[2] * W / 1000, b[3] * H / 1000]
        regions.append({"page": k, "rect": [round(v, 1) for v in rect], "key": it["key"], "label": it.get("label") or "",
                        "value": it.get("value"), "type": it.get("type") or "text",
                        "common": keymap.get(it["key"], DIC.match_extracted(it["key"]))})
    leftover = []
    others = [d for d in f["docs"] if d != best][:12]
    if others:
        sample = [IM.page_words(rows[p], o["mapping"]) for p in pages]
        dr = IM.value_drafts(sample, [[IM.page_words(rows[p], o["mapping"]) for p in f["docs"][d]] for d in others],
                             [(rows[p]["width"], rows[p]["height"]) for p in pages])

        def covered(e):
            cx, cy = (e["rect"][0] + e["rect"][2]) / 2, (e["rect"][1] + e["rect"][3]) / 2
            return any(g["page"] == e["page"] and g["rect"][0] - 4 <= cx <= g["rect"][2] + 4 and g["rect"][1] - 4 <= cy <= g["rect"][3] + 4
                       for g in regions)
        leftover = [{"page": a["page"], "rect": [round(v, 1) for v in a["rect"]], "label": a["label"], "note": a.get("note", "")}
                    for a in dr["add"] if not covered(a)]
    out_dir = bdir / "drafts"
    out_dir.mkdir(exist_ok=True)
    images = []
    for k, pid in enumerate(pages):
        img = Image.open(rows[pid]["image"]).convert("RGB")
        for g in [*regions, *leftover]:
            if g["page"] == k:
                pad = max(1.5, 0.12 * (g["rect"][3] - g["rect"][1]))
                _fill(img, [g["rect"][0] - pad, g["rect"][1] - pad, g["rect"][2] + pad, g["rect"][3] + pad])
        name = f"{IM._slug(fid)}_p{k + 1}.png"
        img.save(out_dir / name)
        images.append({"name": name, "width": rows[pid]["width"], "height": rows[pid]["height"], "page_id": pid})
    return {"format": fid, "sample_doc": best, "pages": pages, "images": images, "regions": regions, "leftover": leftover,
            "with_box": best_n, "keymapped": sum(1 for g in regions if g["common"])}


def score(bdir: Path, truth_path: Path, exclude: set[str]) -> dict:
    """판정 정확도: 모양의 다수 진짜 서식이 빼 둔 서식·외부 문서면 '새 서식'이 맞고, 아니면 그 서식(또는 같은 문서명의 서식)이 맞다.
    빼 둔 서식이라도 같은 문서명의 다른 서식(예: building_register ↔ gov_building_unit)을 고르면 맞은 것으로 센다 — 문서명이 이미 있다는 제안이라."""
    from docgen import dictionary as DIC

    truth = json.loads(truth_path.read_text(encoding="utf-8"))["documents"]
    by = {**truth, **{d["flat"]: d for d in truth.values()}}
    _, _, fx = _load(bdir)
    fmt_docs = {f["id"]: f["docs"] for f in fx["formats"]}
    ok = n = 0
    rows = []
    for j in judge(bdir, exclude):
        forms = Counter(by[d]["form"] for d in fmt_docs[j["id"]] if d in by)
        if not forms:
            continue
        top = forms.most_common(1)[0][0]
        new = top.startswith("ext:") or top in exclude
        s = j["suggest"]
        dt = DIC.doc_type_of(s["form_id"]) if s["kind"] == "existing" else None
        same_doc = s["kind"] == "existing" and (s["form_id"] == top or dt is not None and dt == DIC.doc_type_of(top))
        right = (s["kind"] == "new" or same_doc) if new else same_doc
        ok += right
        n += 1
        if not right:
            rows.append({"format": j["id"], "truth": top, "new": new, "suggest": s, "similar": j["similar"][:2]})
    return {"formats": n, "accuracy": round(ok / n, 4) if n else None, "wrong": rows}


def main(argv=None) -> None:
    import argparse

    ap = argparse.ArgumentParser(prog="python -m studio.intake_judge", description=__doc__.split("\n")[0])
    ap.add_argument("batch")
    ap.add_argument("--truth")
    ap.add_argument("--exclude", default="", help="'새 서식'으로 다룰 서식 ID (기존 서식 지문에서 뺀다, 시험 폴더의 --hold-out)")
    a = ap.parse_args(argv)
    ex = {x.strip() for x in a.exclude.split(",") if x.strip()}
    if a.truth:
        r = score(Path(a.batch), Path(a.truth), ex)
        print(json.dumps({k: v for k, v in r.items() if k != "wrong"}, ensure_ascii=False))
        for w in r["wrong"][:20]:
            print(" ", w["format"], "정답", w["truth"], "새" if w["new"] else "", "→ 제안", w["suggest"].get("kind"), w["suggest"].get("form_id", ""),
                  w["suggest"].get("score"), [(s["form"], s["score"]) for s in w["similar"]])
        return
    for j in judge(Path(a.batch), ex):
        print(j["id"], j["name"], j["n_docs"], j["suggest"])


if __name__ == "__main__":
    main(sys.argv[1:])
