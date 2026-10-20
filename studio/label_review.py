"""⑤ 검수 › 라벨 검수 (DESIGN.md 8.6): 결과 폴더(또는 autolabel)의 추론 결과를 문서마다 사람이 고쳐 실서류 정답을 만든다.
API 는 studio/api_review.py, 화면은 static/js/labels.js. 추론 결과가 없는 문서는 빈 라벨에서 시작한다.

흐름: 포맷마다 서식 정하기(④ 결정: 기존 서식과 같음·템플릿으로) → 키 대응(모델 키 → 그 서식의 표준 키, 포맷마다 한 번) →
문서마다 값·위치를 고치고 확인 → 확인한 문서는 **표준 라벨 v1 폴더**(studio/LABEL_FORMAT.md)로 → ④ 라벨 있는 데이터로 데이터셋.

저장 <real_data_dir>/labels/<묶음>/   (표준 라벨 v1 폴더 그대로: 그대로 ④ 라벨 있는 데이터의 경로로 쓴다)
  meta.json            {"format": "docgen-labels/1", "name", "real_data", "gt": "reviewed", "from_batch", "model"}
  labels/<문서>.json   확인한 문서의 v1 라벨 (doc_type = 포맷의 서식, fields 는 픽셀 bbox·page 0부터)
  images/<문서>_p<쪽>.png   그 쪽 그림 (OCR 이 본 그림)
  review/<문서>.json   검수 상태 {status: in_progress|done, by, at, fields: [... state: auto|edited|confirmed|added|deleted, original]}
  keymap.json          {포맷 ID: {모델 키: 표준 키 | ""(버림)}}
  bundles.jsonl        업무 묶음 (화면에서 정함, v1 bundles 형식)
- 원래 추론 값은 지우지 않고 fields[].original 에 함께 둔다. 원래 추론과 검수 결과의 차이로 그 모델의 실서류 점수를 낸다(score).
"""
from __future__ import annotations

import json
import re
import shutil
import time
from collections import Counter
from pathlib import Path

from . import importer as IM

MARKS = ("checkbox", "checkbox_multi", "seal", "signature")


def safe(doc: str) -> str:
    return re.sub(r"[^\w.-]+", "_", doc).strip("_") or "doc"


def root(real_root: Path, batch: str) -> Path:
    return Path(real_root) / "labels" / batch


def _read(p: Path, default=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def _write(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------------------------------------------------------------------------
# 묶음·포맷·문서
# ---------------------------------------------------------------------------

def _batch(bdir: Path) -> tuple[dict, list[dict], dict]:
    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    rows = IM._jsonl(bdir / "pages.jsonl")
    fx = _read(bdir / "formats.json", {"formats": []})
    return batch, rows, fx


def doc_type_of(fmt: dict) -> str | None:
    d = fmt.get("decision") or {}
    return d.get("form_id") if d.get("kind") in ("existing", "template") else None


def form_keys(doc_type: str | None) -> list[dict]:
    """그 서식의 표준 키 [{key, label, type}] (guide/fields/fields.json, 없으면 영역 편집기의 추가 칸 키)."""
    if not doc_type:
        return []
    from .catalog import _fields

    keys = _fields().get(doc_type, {}).get("keys", [])
    if keys:
        return [{"key": k["key"], "label": k.get("label"), "type": k.get("type", "text")} for k in keys]
    from docgen import overrides as OV

    return [{"key": a["key"], "label": a.get("label"), "type": "text"} for a in OV.load(doc_type).get("add", []) if a.get("key")]


def pred_of(bdir: Path, batch: dict, doc: str) -> dict | None:
    """문서의 추론 결과: 결과 폴더의 pred, 없으면 autolabel 결과(<묶음>/pred/<문서>.json)."""
    p = ((batch.get("results") or {}).get("pred") or {}).get(doc)
    f = Path(p) if p else bdir / "pred" / f"{safe(doc)}.json"
    return _read(f) if f.exists() else None


def _px(box, w, h):
    return [round(box[0] * w / 1000, 1), round(box[1] * h / 1000, 1), round(box[2] * w / 1000, 1), round(box[3] * h / 1000, 1)]


def pred_fields(pred: dict | None, pages: list[dict], keymap: dict) -> list[dict]:
    """추론 항목 → 검수 칸 [{key, label, type, value, page(0부터), bbox(px), state: auto, original}]. 키는 키 대응으로 바꾼다."""
    from .results import pred_items

    out = []
    for it in pred_items(pred or {}):
        mk = it.get("key")
        key = keymap.get(mk, mk)
        if key == "":   # 키 대응에서 버린 키
            continue
        pg = max(0, int(it.get("page", 1)) - 1)
        bbox = None
        if it.get("bbox_2d") and pg < len(pages):
            bbox = _px(it["bbox_2d"], pages[pg]["width"], pages[pg]["height"])
        elif it.get("bbox"):
            bbox = [float(v) for v in it["bbox"]]
        f = {"key": key, "label": it.get("label"), "type": it.get("type") or ("seal" if key.startswith("seal.") else
             "signature" if key.startswith("sign.") else "text"), "value": it.get("value"), "page": pg, "bbox": bbox, "state": "auto"}
        f["original"] = {k: f[k] for k in ("key", "value", "page", "bbox")} | {"model_key": mk}
        out.append(f)
    return out


def overview(bdir: Path, real_root: Path) -> dict:
    """라벨 검수 첫 화면: 포맷마다 서식·문서 수·검수 진행·키 대응 필요 여부."""
    from .results import pred_items

    batch, rows, fx = _batch(bdir)
    rt = root(real_root, batch["name"])
    km = _read(rt / "keymap.json", {})
    docs_of = {}
    for r in rows:
        docs_of.setdefault(r["doc"], []).append(r)
    out = []
    for f in fx["formats"]:
        dt = doc_type_of(f)
        docs = list((f.get("docs") or {}).keys())
        st = [(_read(rt / "review" / f"{safe(d)}.json", {}) or {}).get("status") for d in docs]
        model_keys = Counter(it.get("key") for d in docs for it in pred_items(pred_of(bdir, batch, d) or {}))
        std = {k["key"] for k in form_keys(dt)}
        unmapped = sorted(k for k in model_keys if k and k not in std and k not in km.get(f["id"], {}))
        out.append({"id": f["id"], "name": f["name"], "doc_type": dt, "documents": len(docs), "done": st.count("done"),
                    "in_progress": st.count("in_progress"), "with_pred": sum(1 for d in docs if pred_of(bdir, batch, d)),
                    "unmapped_keys": unmapped[:50], "n_unmapped": len(unmapped)})
    return {"batch": batch["name"], "real_data": batch.get("real_data"), "model": (batch.get("results") or {}).get("model"),
            "formats": out, "root": str(rt), "exported": len(list((rt / "labels").glob("*.json"))) if (rt / "labels").is_dir() else 0}


def keymap_view(bdir: Path, real_root: Path, fid: str) -> dict:
    from .results import pred_items

    batch, rows, fx = _batch(bdir)
    f = next((x for x in fx["formats"] if x["id"] == fid), None)
    if f is None:
        raise KeyError(fid)
    km = _read(root(real_root, batch["name"]) / "keymap.json", {}).get(fid, {})
    seen: dict[str, dict] = {}
    for d in (f.get("docs") or {}):
        for it in pred_items(pred_of(bdir, batch, d) or {}):
            s = seen.setdefault(it.get("key"), {"key": it.get("key"), "label": it.get("label"), "n": 0, "example": it.get("value")})
            s["n"] += 1
    std = form_keys(doc_type_of(f))
    stdk = {k["key"] for k in std}
    return {"format": fid, "doc_type": doc_type_of(f), "standard": std,
            "model_keys": [{**s, "mapped": km.get(s["key"], s["key"] if s["key"] in stdk else None)} for s in seen.values()]}


def save_keymap(bdir: Path, real_root: Path, fid: str, mapping: dict) -> dict:
    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    p = root(real_root, batch["name"]) / "keymap.json"
    km = _read(p, {})
    km[fid] = {k: v for k, v in mapping.items() if v is not None}
    _write(p, km)
    return km[fid]


def _doc_rows(rows: list[dict], doc: str) -> list[dict]:
    return sorted((r for r in rows if r["doc"] == doc), key=lambda r: r.get("page", 1))


def load_doc(bdir: Path, real_root: Path, doc: str) -> dict:
    batch, rows, fx = _batch(bdir)
    pr = _doc_rows(rows, doc)
    if not pr:
        raise KeyError(doc)
    fmt = next((f for f in fx["formats"] if doc in (f.get("docs") or {})), None)
    pages = [{"id": r["id"], "width": r.get("width"), "height": r.get("height")} for r in pr]
    rt = root(real_root, batch["name"])
    rv = _read(rt / "review" / f"{safe(doc)}.json")
    km = _read(rt / "keymap.json", {}).get(fmt["id"], {}) if fmt else {}
    fields = rv["fields"] if rv else pred_fields(pred_of(bdir, batch, doc), pages, km)
    dt = doc_type_of(fmt) if fmt else None
    return {"doc": doc, "format": fmt["id"] if fmt else None, "format_name": fmt["name"] if fmt else None, "doc_type": dt,
            "pages": pages, "fields": fields, "status": (rv or {}).get("status"), "review": {k: (rv or {}).get(k) for k in ("by", "at")},
            "standard": form_keys(dt), "has_pred": pred_of(bdir, batch, doc) is not None}


def save_doc(bdir: Path, real_root: Path, doc: str, fields: list[dict], done: bool, by: str) -> dict:
    """검수 저장. 확인(done)하면 v1 라벨로 내보낸다. 서식(포맷 결정)이 없으면 확인할 수 없다."""
    from docgen.registry import load_all

    batch, rows, fx = _batch(bdir)
    cur = load_doc(bdir, real_root, doc)
    pr = _doc_rows(rows, doc)
    clean = []
    for f in fields:
        key = str(f.get("key") or "").strip()
        if not key:
            continue
        g = {k: f.get(k) for k in ("key", "label", "type", "value", "page", "bbox", "state", "original", "present")}
        g["key"], g["type"] = key, g.get("type") or "text"
        g["page"] = int(g.get("page") or 0)
        if g["page"] >= len(pr):
            raise ValueError(f"{key}: 쪽 번호가 범위를 벗어났습니다")
        if g.get("bbox") is not None:
            b = [float(v) for v in g["bbox"]]
            w, h = pr[g["page"]]["width"], pr[g["page"]]["height"]
            g["bbox"] = [max(0.0, min(b[0], b[2])), max(0.0, min(b[1], b[3])), min(float(w), max(b[0], b[2])), min(float(h), max(b[1], b[3]))]
        if g.get("state") not in ("auto", "edited", "confirmed", "added", "deleted"):
            g["state"] = "added"
        clean.append(g)
    live = [g for g in clean if g["state"] != "deleted"]
    dup = [k for k, n in Counter(g["key"] for g in live).items() if n > 1]
    if dup:
        raise ValueError(f"같은 키가 둘 이상입니다: {dup[:5]}")
    if done:
        if not cur["doc_type"] or cur["doc_type"] not in load_all():
            raise ValueError("이 문서의 포맷에 서식이 정해지지 않았습니다 (④ 가져오기 › 포맷 › 기존 서식과 같음 / 템플릿으로)")
        for g in live:
            if g["state"] == "auto":
                g["state"] = "confirmed"   # 확인을 누르면 손대지 않은 칸도 사람이 본 것
    rt = root(real_root, batch["name"])
    st = {"doc": doc, "status": "done" if done else "in_progress", "by": by, "at": time.strftime("%Y-%m-%d %H:%M"), "fields": clean}
    _write(rt / "review" / f"{safe(doc)}.json", st)
    if done:
        export_doc(bdir, real_root, doc, cur["doc_type"], live, pr, batch)
    else:   # 확인을 풀면 내보낸 라벨도 뺀다 (v1 폴더에는 확인한 문서만)
        (rt / "labels" / f"{safe(doc)}.json").unlink(missing_ok=True)
    return {"status": st["status"], "at": st["at"], "fields": len(live)}


def _v1_field(g: dict) -> dict:
    t = g["type"]
    f = {"key": g["key"], "label": g.get("label") or g["key"].split(".")[-1], "type": t}
    if t in ("seal", "signature"):
        present = g.get("present") if g.get("present") is not None else bool(g.get("value"))
        f.update(value=None, present=bool(present))
    elif t in ("checkbox", "checkbox_multi"):
        vals = g["value"] if isinstance(g.get("value"), list) else ([] if g.get("value") in (None, "") else [g["value"]])
        f["value"] = vals if t == "checkbox_multi" else (vals[0] if vals else None)
        f["options"] = [{"text": str(v), "checked": True, **({"box_bbox": g["bbox"]} if g.get("bbox") else {})} for v in vals]
    else:
        f["value"] = None if g.get("value") in (None, "") else str(g["value"])
    if g.get("bbox") is not None and (f.get("value") is not None or f.get("present")):
        f.update(page=g["page"], bbox=[round(v, 1) for v in g["bbox"]])
    return f


def export_doc(bdir: Path, real_root: Path, doc: str, doc_type: str, live: list[dict], pr: list[dict], batch: dict) -> Path:
    from docgen.registry import load_all

    rt = root(real_root, batch["name"])
    sid = safe(doc)
    imgs = []
    for k, r in enumerate(pr, 1):
        src = Path(r.get("image") or r["source"])
        dst = rt / "images" / f"{sid}_p{k}{src.suffix.lower() or '.png'}"
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            shutil.copyfile(src, dst)
        imgs.append(dst.relative_to(rt).as_posix())
    label = {"id": sid, "doc_type": doc_type, "doc_name": load_all()[doc_type].name, "images": imgs,
             "pages": [{"width": r["width"], "height": r["height"]} for r in pr], "fields": [_v1_field(g) for g in live],
             "source": {"batch": batch["name"], "document": doc}}
    _write(rt / "labels" / f"{sid}.json", label)
    if not (rt / "meta.json").exists():
        _write(rt / "meta.json", {"format": "docgen-labels/1", "name": f"{batch['name']} 라벨 검수", "real_data": bool(batch.get("real_data")),
                                  "gt": "reviewed", "from_batch": batch["name"], "model": (batch.get("results") or {}).get("model")})
    return rt / "labels" / f"{sid}.json"


# ---------------------------------------------------------------------------
# 같은 자리 모아 보기 · 의심 먼저 · 점수
# ---------------------------------------------------------------------------

def key_view(bdir: Path, real_root: Path, fid: str, key: str) -> list[dict]:
    """한 포맷 안 모든 문서에서 같은 키의 값과 자리 (같은 실수를 한 번에 고친다)."""
    batch, rows, fx = _batch(bdir)
    f = next((x for x in fx["formats"] if x["id"] == fid), None)
    if f is None:
        raise KeyError(fid)
    out = []
    for d in f.get("docs") or {}:
        ld = load_doc(bdir, real_root, d)
        g = next((x for x in ld["fields"] if x["key"] == key and x.get("state") != "deleted"), None)
        out.append({"doc": d, "status": ld["status"], "field": g, "page_id": ld["pages"][g["page"]]["id"] if g and g.get("bbox") else None})
    return out


def suspicious(bdir: Path, real_root: Path, fid: str) -> list[dict]:
    """먼저 볼 문서: 같은 포맷 문서 절반 이상에 있는 키가 빠진 것, 위치가 없는 값, OCR 글자에 없는 값이 많은 것부터."""
    from .formats import norm_text

    batch, rows, fx = _batch(bdir)
    f = next((x for x in fx["formats"] if x["id"] == fid), None)
    if f is None:
        raise KeyError(fid)
    docs = list(f.get("docs") or {})
    loaded = {d: load_doc(bdir, real_root, d) for d in docs}
    common = Counter(k for ld in loaded.values() for k in {x["key"] for x in ld["fields"] if x.get("state") != "deleted"})
    need = {k for k, n in common.items() if n >= max(2, len(docs) / 2)}
    o = IM._ocr_settings(batch)
    out = []
    for d, ld in loaded.items():
        keys = {x["key"] for x in ld["fields"] if x.get("state") != "deleted"}
        missing = sorted(need - keys)
        nobox = [x["key"] for x in ld["fields"] if x.get("value") not in (None, "") and not x.get("bbox") and x["type"] not in MARKS]
        text = ""
        for r in _doc_rows(rows, d):
            if r.get("ocr"):
                text += norm_text("".join(w["text"] for w in IM.page_words(r, o["mapping"])))
        notin = [x["key"] for x in ld["fields"] if x["type"] not in MARKS and x.get("value") not in (None, "") and text
                 and norm_text(str(x["value"])) and norm_text(str(x["value"])) not in text]
        out.append({"doc": d, "status": ld["status"], "missing": missing, "no_box": nobox, "not_in_ocr": notin,
                    "score": 3 * len(missing) + len(nobox) + 2 * len(notin)})
    return sorted(out, key=lambda x: (x["status"] == "done", -x["score"], x["doc"]))


def _items_for(doc_type: str, fields: list[dict], sizes: list[tuple]) -> list[dict]:
    """검수한 칸 → 생성기와 같은 kie·marks 문항 (docgen.bench.build Builder.single 을 그대로 쓴다)."""
    from docgen.bench.build import Builder
    from docgen.schema import infer

    fs = []
    for g in fields:
        f = _v1_field(g)
        if "norm" not in f and f["type"] not in ("seal", "signature", "checkbox_multi"):
            _, f["norm"] = infer(f["key"], f.get("value"), f["type"])
        fs.append(f)
    b = Builder.__new__(Builder)
    b.out, b.buf = Path("."), []
    r = {"doc_id": doc_type, "name": doc_type, "group": "labeled", "condition": "original", "writing": "unknown",
         "images": [f"p{k}" for k in range(len(sizes))], "sizes": sizes, "pages": [{"width": w, "height": h} for w, h in sizes],
         "fields": fs, "raw_keys": [f["key"] for f in fs], "visible": {f["key"] for f in fs if f.get("value") is not None}}
    b.single(r, "review", 0, 10_000)
    return [it for it in b.take() if it["task"] in ("kie", "marks")]


def score(bdir: Path, real_root: Path) -> dict:
    """원래 추론(키 대응 뒤)을 검수 결과에 대어 채점: 그 모델의 실서류 점수 (평가 세트와 같은 채점기, 값·위치·값+위치)."""
    from docgen.bench import evaluate as E
    from docgen.bench.metrics import normalize_box

    batch, rows, fx = _batch(bdir)
    rt = root(real_root, batch["name"])
    items, preds = {"kie": [], "marks": []}, {}
    n = 0
    for f in sorted((rt / "review").glob("*.json")) if (rt / "review").is_dir() else []:
        rv = _read(f)
        if rv.get("status") != "done":
            continue
        ld = load_doc(bdir, real_root, rv["doc"])
        if not ld["has_pred"] or not ld["doc_type"]:
            continue
        pr = _doc_rows(rows, rv["doc"])
        sizes = [(r["width"], r["height"]) for r in pr]
        live = [g for g in rv["fields"] if g["state"] != "deleted"]
        orig = [g["original"] for g in rv["fields"] if g.get("original")]
        n += 1
        for it in _items_for(ld["doc_type"], live, sizes):
            it["id"] = f"{it['task']}/{rv['doc']}"
            items[it["task"]].append(it)
            ans = []
            for o in orig:
                e = {"key": o["key"], "value": o["value"]}
                if o.get("bbox") and o["page"] < len(sizes):
                    try:
                        e.update(bbox_2d=normalize_box(o["bbox"], *sizes[o["page"]]), page=o["page"] + 1)
                    except ValueError:
                        pass
                ans.append(e)
            preds[it["id"]] = json.dumps(ans, ensure_ascii=False)
    out = {"documents": n, "model": (batch.get("results") or {}).get("model"), "tasks": {}}
    for t, its in items.items():
        if its:
            res = E.score_task(t, its, preds)
            out["tasks"][t] = {k: v for k, v in res.items() if k != "per_item"}
    return out


# ---------------------------------------------------------------------------
# 업무 묶음
# ---------------------------------------------------------------------------

def bundles(bdir: Path, real_root: Path) -> dict:
    """업무 묶음 (화면에서 고친 것, 없으면 결과 폴더의 bundles.jsonl) + 묶음 후보 (검수한 주민번호·사업자번호·법인번호가 같은 문서)."""
    batch, rows, fx = _batch(bdir)
    rt = root(real_root, batch["name"])
    p = rt / "bundles.jsonl"
    cur = IM._jsonl(p)
    if not cur and (batch.get("results") or {}).get("bundles"):
        cur = IM._jsonl(Path(batch["results"]["bundles"]))
    docs = sorted({r["doc"] for r in rows})
    ids = {}
    for d in docs:
        rv = _read(rt / "review" / f"{safe(d)}.json")
        for g in (rv or {}).get("fields", []):
            k = g["key"].rsplit(".", 1)[-1]
            if k in ("rrn", "biz_no", "corp_reg_no") and g.get("value"):
                ids.setdefault(re.sub(r"\D", "", str(g["value"]))[:13], set()).add(d)
    suggest = [{"documents": sorted(v), "by": k} for k, v in ids.items() if len(v) > 1 and len(k) >= 6]
    from docgen.registry import SCENARIOS

    return {"bundles": cur, "documents": [{"doc": d, "status": (_read(rt / "review" / f"{safe(d)}.json", {}) or {}).get("status")} for d in docs],
            "suggest": suggest, "scenarios": [{"id": k, "name": v[0]} for k, v in SCENARIOS.items()]}


def save_bundles(bdir: Path, real_root: Path, items: list[dict]) -> int:
    """화면에서 정한 묶음을 v1 bundles.jsonl 로 (문서 ID 는 내보낸 라벨 ID)."""
    from docgen.registry import SCENARIOS

    batch, rows, fx = _batch(bdir)
    docs = {r["doc"] for r in rows}
    type_of = {d: doc_type_of(f) for f in fx["formats"] for d in (f.get("docs") or {})}
    out = []
    for b in items:
        bid = str(b.get("bundle_id") or "").strip()
        ds = [d for d in b.get("documents", []) if d in docs]
        if not bid or not ds or not b.get("scenario"):
            raise ValueError("묶음마다 bundle_id, 업무 시나리오, 문서가 필요합니다")
        if b["scenario"] not in SCENARIOS:
            raise ValueError(f"{bid}: 등록되지 않은 시나리오 {b['scenario']} (③ 시나리오)")
        same = [t for t, n in Counter(type_of.get(d) for d in ds).items() if t and n > 1]
        if same:   # 표준 라벨 v1 의 업무 묶음 규칙: 서식마다 문서 한 건
            raise ValueError(f"{bid}: 한 묶음에 같은 서식 문서가 둘 이상입니다 ({same[0]})")
        row = {"bundle_id": bid, "scenario": b["scenario"], "documents": [safe(d) for d in ds], "source_documents": ds}
        for k in ("customer",):
            if b.get(k):
                row[k] = b[k]
        if "not_customer" in b and b["not_customer"] is not None:
            row["not_customer"] = [safe(d) for d in b["not_customer"] if d in docs]
        out.append(row)
    p = root(real_root, batch["name"]) / "bundles.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    IM._write_jsonl(p, out)
    return len(out)
