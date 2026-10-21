"""생성 라벨 → 사내 OCR 응답 형식 JSON (쪽 이미지마다 하나). 합성 OCR 벤치마크의 정답 (studio/DESIGN.md 9.2).

사내 OCR 응답 형식 (OCR 준비 docgen.bench.ocr_data 의 기본 mapping 이 읽는 것)
  {"filename": "<이미지 파일 이름>", "success": "Y",
   "data": {"basicData": [[{"text", "confidence", "bounding": {"shape": "rectangle", "vertices": [{x, y} × 4]}, "line_num"}]]}}

두 가지로 만든다.
  fields_items  값 칸·항목명 칸만. 예시 데이터용으로 guide/examples/labels_to_ocr.py 가 export_fields 로 부른다
  page_items    쪽 전체 글자 (렌더러가 잰 단어 박스 + overlay 배경 PDF 의 인쇄 글자). 합성 OCR 세트(docgen/ocr_set.py)가 쓴다
                unit="word": 단어마다 한 항목, 같은 줄은 같은 line_num / unit="line": 줄마다 한 항목
                애매한 글자(견본 표시·도장 안 글자·정정으로 그은 글자)는 신뢰도를 낮춰, OCR 준비가 그 자리를
                문항에서 빼거나(필터) 칠해 가리게 한다.
"""
from __future__ import annotations

import json
import random
from pathlib import Path

MARK_TYPES = ("seal", "signature", "checkbox", "checkbox_multi")
LOW_KINDS = {"watermark", "seal", "struck"}
TEXT_CONF = 0.99
LOW_CONF = 0.3


def item(text: str, box, conf: float, line: int = 0) -> dict:
    x0, y0, x1, y1 = box
    return {"text": text, "confidence": conf, "bounding": {"shape": "rectangle", "vertices": [
        {"x": round(x0), "y": round(y0)}, {"x": round(x1), "y": round(y0)},
        {"x": round(x1), "y": round(y1)}, {"x": round(x0), "y": round(y1)}]}, "line_num": line}


def page_document(items: list[dict], filename: str) -> dict:
    return {"filename": filename, "success": "Y", "data": {"basicData": [items]}}


# ---------------------------------------------------------------------------
# 값 칸·항목명 칸만 (guide/examples/labels_to_ocr.py 에 있던 변환을 옮겨 온 것)
# ---------------------------------------------------------------------------

def fields_items(label: dict, rng: random.Random) -> dict[int, list[dict]]:
    """라벨의 값 칸(여러 줄이면 줄마다)과 항목명 칸 → 쪽마다 OCR 항목. 신뢰도는 rng 로 흔든다."""
    pages: dict[int, list] = {}
    for f in label["fields"]:
        p = f.get("page", 0)
        if f.get("type") not in MARK_TYPES and f.get("bbox") and isinstance(f.get("value"), str) and f["value"].strip():
            lines = [s for s in f["value"].split("\n") if s.strip()]
            x0, y0, x1, y1 = f["bbox"]
            h = (y1 - y0) / len(lines)
            for i, s in enumerate(lines):
                pages.setdefault(p, []).append((s.strip(), [x0, y0 + i * h, x1, y0 + (i + 1) * h]))
        if f.get("label") and f.get("label_bbox"):
            pages.setdefault(p, []).append((f["label"], f["label_bbox"]))
    out: dict[int, list[dict]] = {}
    for p in range(len(label["images"])):
        seen, items = set(), []
        for text, (x0, y0, x1, y1) in pages.get(p, []):
            key = (text, round(x0), round(y0))
            if key in seen:
                continue
            seen.add(key)
            conf = round(rng.choice([0.9999, 0.998, 0.995, 0.99, 0.97, 0.91]), 4)
            items.append(item(text, (x0, y0, x1, y1), conf, 0))
        out[p] = items
    return out


def export_fields(gen_dir: Path, out_dir: Path) -> int:
    """docgen generate --out 폴더의 labels/*.json → OCR JSON 폴더 (guide/examples/labels_to_ocr.py 가 부른다)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(0)
    n = 0
    for lf in sorted((gen_dir / "labels").glob("*.json")):
        lab = json.loads(lf.read_text(encoding="utf-8"))
        per_page = fields_items(lab, rng)
        for p, img in enumerate(lab["images"]):
            name = Path(img).name
            (out_dir / (Path(name).stem + ".json")).write_text(json.dumps(page_document(per_page.get(p, []), name),
                                                                          ensure_ascii=False), encoding="utf-8")
            n += 1
    return n


# ---------------------------------------------------------------------------
# 쪽 전체 글자
# ---------------------------------------------------------------------------

def background_words(doc_id: str) -> dict[int, list[dict]]:
    """overlay 서식 배경 그림 속 인쇄 글자: pdf 서식은 PDF 글자 층, image 서식은 layout.json 의 texts.
    좌표는 pt. 사람 수정의 배경 지우기 안에 있는 글자는 뺀다. html 서식이면 빈 것."""
    from . import overrides as OV
    from . import realform as RF

    no = RF.form_no(doc_id)
    out: dict[int, list[dict]] = {}
    if no is not None:
        if RF.layout_path(no) is None:
            return {}
        import pymupdf

        lay = RF.load_layout(no)
        with pymupdf.open(RF.ROOT / lay["file"]) as doc:
            for i, page in enumerate(doc):
                out[i] = [{"text": w[4], "bbox": list(w[:4]), "line": f"pdf:{w[5]}:{w[6]}"} for w in page.get_text("words")]
    elif RF.image_form_dir(doc_id) is not None:
        lay = RF.raw_layout(doc_id)
        for t in lay.get("texts", []):
            out.setdefault(t["page"], []).append({"text": t["text"], "bbox": t["rect"], "line": f"img:{t.get('line', 0)}"})
    else:
        return {}
    ov = OV.load(doc_id)
    for page, words in out.items():
        er = OV.erase_for(ov, page)
        if er:
            out[page] = [w for w in words if not any(e["rect"][0] <= (w["bbox"][0] + w["bbox"][2]) / 2 <= e["rect"][2] and
                                                     e["rect"][1] <= (w["bbox"][1] + w["bbox"][3]) / 2 <= e["rect"][3] for e in er)]
    return out


def _lines(words: list[dict]) -> list[list[dict]]:
    """같은 줄 단어 묶기: 같은 칸(blk)·같은 PDF 줄이고 세로로 절반 넘게 겹치는 것. 위에서 아래, 왼쪽에서 오른쪽."""
    lines: list[list[dict]] = []
    for w in sorted(words, key=lambda w: ((w["bbox"][1] + w["bbox"][3]) / 2, w["bbox"][0])):
        y0, y1 = w["bbox"][1], w["bbox"][3]
        for ln in lines:
            last = ln[-1]
            ly0, ly1 = min(x["bbox"][1] for x in ln), max(x["bbox"][3] for x in ln)
            overlap = min(y1, ly1) - max(y0, ly0)
            gap = w["bbox"][0] - last["bbox"][2]
            if w.get("group") == last.get("group") and overlap > 0.5 * min(y1 - y0, ly1 - ly0) and -2 < gap < 2.5 * (y1 - y0):
                ln.append(w)
                break
        else:
            lines.append([w])
    for ln in lines:
        ln.sort(key=lambda w: w["bbox"][0])
    lines.sort(key=lambda ln: (min(w["bbox"][1] for w in ln), min(w["bbox"][0] for w in ln)))
    return lines


def page_items(texts: list[dict], background: list[dict], scale: float, unit: str = "word") -> list[dict]:
    """렌더러가 잰 단어(texts, 이미지 픽셀)와 배경 글자(background, pt → × scale 픽셀) → 사내 OCR 항목 목록."""
    words = [{"text": t["text"], "bbox": t["bbox"], "kind": t.get("kind", "text"), "group": f"dom:{t.get('blk', 0)}"} for t in texts]
    words += [{"text": w["text"], "bbox": [v * scale for v in w["bbox"]], "kind": "text", "group": w["line"]} for w in background]
    out = []
    for n, ln in enumerate(_lines(words)):
        low = any(w["kind"] in LOW_KINDS for w in ln)
        if unit == "line":
            box = [min(w["bbox"][0] for w in ln), min(w["bbox"][1] for w in ln), max(w["bbox"][2] for w in ln), max(w["bbox"][3] for w in ln)]
            out.append(item(" ".join(w["text"] for w in ln), box, LOW_CONF if low else TEXT_CONF, n))
        else:
            out += [item(w["text"], w["bbox"], LOW_CONF if w["kind"] in LOW_KINDS else TEXT_CONF, n) for w in ln]
    return out


def transform_texts(texts: list[dict], tfs: list) -> list[dict]:
    """촬영 조건 증강의 좌표 변환을 단어 박스에도 (docgen/augment.py 의 tf.bbox)."""
    out = []
    for t in texts:
        tf = tfs[t["page"]] if t["page"] < len(tfs) else None
        out.append({**t, "bbox": tf.bbox(t["bbox"]) if tf else t["bbox"]})
    return out
