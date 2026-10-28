"""⑤ 검수 › OCR 검수 (DESIGN.md 8.7): 사내 OCR 결과를 쪽마다 사람이 고쳐 "OCR 검수 정답"을 만든다.
API 는 studio/api_import.py (/api/imports/{묶음}/ocr), 화면은 static/js/review.js.

저장
  <real_data_dir>/ocr_reviewed/<묶음>/<쪽>.json   고친 OCR. 사내 OCR 응답 형식 그대로 → docgen.bench.ocr_data.scan(ocr_dir=…) 로 바로 읽힌다
  <real_data_dir>/ocr_reviewed/<묶음>/review.jsonl 쪽마다 마지막 상태 {page, status: in_progress|done, by, at, stats}
원래 OCR 은 캐시에 그대로 둔다. 원래와 고친 것의 차이가 사내 OCR 의 오류다 (글자 오류율 CER, 박스 F1).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from . import importer as IM


def _dir(reviewed_root: Path, batch: str) -> Path:
    return Path(reviewed_root) / batch


def reviewed_pages(reviewed_root: Path, batch: str) -> set[str]:
    """확인(done)을 누른 쪽."""
    return {k for k, v in states(reviewed_root, batch).items() if v.get("status") == "done"}


def states(reviewed_root: Path, batch: str) -> dict[str, dict]:
    f = _dir(reviewed_root, batch) / "review.jsonl"
    out: dict[str, dict] = {}
    if f.exists():
        for s in f.read_text(encoding="utf-8").splitlines():
            if s.strip():
                r = json.loads(s)
                out[r["page"]] = r
    return out


def load_page(bdir: Path, page_id: str, reviewed_root: Path) -> dict:
    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    rows = {r["id"]: r for r in IM._jsonl(bdir / "pages.jsonl")}
    if page_id not in rows:
        raise KeyError(page_id)
    r = rows[page_id]
    o = IM._ocr_settings(batch)
    rv = _dir(reviewed_root, batch["name"]) / f"{IM._safe(page_id)}.json"
    words = IM.page_words(r, o["mapping"], rv)
    orig = IM.page_words(r, o["mapping"])
    st = states(reviewed_root, batch["name"]).get(page_id, {})
    return {"page": page_id, "doc": r["doc"], "width": r["width"], "height": r["height"], "image": r["image"],
            "words": [{"text": w["text"], "bbox": [round(v, 1) for v in w["bbox"]], "confidence": w["confidence"],
                       "line": w.get("line_num")} for w in words],
            "original": [{"text": w["text"], "bbox": [round(v, 1) for v in w["bbox"]], "confidence": w["confidence"]} for w in orig],
            "reviewed_file": str(rv) if rv.exists() else None, "state": st}


def _cer(a: str, b: str) -> float:
    from docgen.bench.metrics import levenshtein

    return levenshtein(a, b) / max(1, len(b))


def stats(original: list[dict], reviewed: list[dict]) -> dict:
    """사내 OCR(원래) 을 검수본 기준으로 잰 오류: 글자 오류율, 박스 F1(IoU 0.5), 고친·더한·뺀 단어 수."""
    from docgen.bench.metrics import iou

    a = " ".join(w["text"] for w in sorted(original, key=lambda w: (w["bbox"][1], w["bbox"][0])))
    b = " ".join(w["text"] for w in sorted(reviewed, key=lambda w: (w["bbox"][1], w["bbox"][0])))
    used, hit, same = set(), 0, 0
    for w in reviewed:
        best, bj = 0.0, None
        for j, o in enumerate(original):
            if j in used:
                continue
            v = iou(w["bbox"], o["bbox"])
            if v > best:
                best, bj = v, j
        if bj is not None and best >= 0.5:
            used.add(bj)
            hit += 1
            same += original[bj]["text"] == w["text"]
    p = hit / len(original) if original else 1.0
    r = hit / len(reviewed) if reviewed else 1.0
    return {"ocr_cer": round(_cer(a, b), 4), "box_f1": round(2 * p * r / (p + r), 4) if p + r else 0.0,
            "changed": hit - same, "added": len(reviewed) - hit, "deleted": len(original) - hit,
            "n_original": len(original), "n_reviewed": len(reviewed)}


def save_page(bdir: Path, page_id: str, words: list[dict], reviewed_root: Path, by: str, done: bool) -> dict:
    """고친 단어 [{text, bbox(px), confidence?, line?}] 를 사내 OCR 형식으로 저장하고 상태를 남긴다."""
    from docgen.ocr_export import item, page_document

    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    rows = {r["id"]: r for r in IM._jsonl(bdir / "pages.jsonl")}
    r = rows[page_id]
    clean = []
    for w in words:
        t = str(w.get("text", "")).strip()
        b = w.get("bbox")
        if not t or not b or len(b) != 4:
            continue
        x0, y0, x1, y1 = (float(v) for v in b)
        x0, y0, x1, y1 = max(0, min(x0, x1)), max(0, min(y0, y1)), min(r["width"], max(x0, x1)), min(r["height"], max(y0, y1))
        if x1 - x0 < 1 or y1 - y0 < 1:
            continue
        # 확인(done)한 쪽은 사람이 모든 단어를 본 것이라 신뢰도 1. 고치는 중이면 손대지 않은 단어는 사내 OCR 신뢰도 그대로
        clean.append({"text": t, "bbox": [x0, y0, x1, y1], "confidence": 1.0 if done or w.get("edited") else float(w.get("confidence", 1.0)),
                      "line": w.get("line") or 0})
    d = _dir(reviewed_root, batch["name"])
    d.mkdir(parents=True, exist_ok=True)
    name = Path(r["image"]).name
    doc = page_document([item(w["text"], w["bbox"], round(w["confidence"], 4), w["line"]) for w in clean], name)
    (d / f"{IM._safe(page_id)}.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    orig = load_page(bdir, page_id, Path("/nonexistent"))["original"]
    st = {"page": page_id, "status": "done" if done else "in_progress", "by": by, "at": time.strftime("%Y-%m-%d %H:%M"),
          "stats": stats(orig, clean)}
    with open(d / "review.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(st, ensure_ascii=False) + "\n")
    return st


def suspicious_order(page: dict) -> list[int]:
    """먼저 볼 단어 순서: 신뢰도 낮은 것 → 숫자가 섞인 것 → 나머지 (읽는 순서)."""
    ws = page["words"]
    return sorted(range(len(ws)), key=lambda i: (ws[i]["confidence"] >= 0.9, not any(c.isdigit() for c in ws[i]["text"]),
                                                 ws[i]["bbox"][1], ws[i]["bbox"][0]))


def summary(reviewed_root: Path, batch: str) -> dict:
    s = states(reviewed_root, batch)
    done = [v for v in s.values() if v.get("status") == "done"]
    if not done:
        return {"done": 0, "in_progress": len(s)}
    avg = lambda k: round(sum(v["stats"][k] for v in done) / len(done), 4)  # noqa: E731
    return {"done": len(done), "in_progress": len(s) - len(done), "ocr_cer": avg("ocr_cer"), "box_f1": avg("box_f1"),
            "changed": sum(v["stats"]["changed"] for v in done), "added": sum(v["stats"]["added"] for v in done),
            "deleted": sum(v["stats"]["deleted"] for v in done)}
