"""ocr_field — 값 칸 읽기. 값 칸 하나를 잘라낸 그림을 보고 적힌 글자를 옮긴다.

질문: P_OCR_FIELD (고정 문장)
정답: 그 칸에 넣은 값 (줄바꿈은 빈칸으로). 서류마다 위치가 있는 보이는 칸 중 fields_per_doc 개를 골라
      칸 둘레를 조금 넓혀 잘라 crops/<서류>_<n>.png 로 저장한다
채점: evaluate.s_ocr_field, 주 지표 exact
"""
from .. import prompts
from ..metrics import norm_text
from . import field_kind

TASK = "ocr_field"
NAME = "값 칸 OCR"
PROMPT = prompts.P_OCR_FIELD
ANSWER = {"type": "string"}
EXAMPLE = "홍길동"
NOTES = "입력은 값 칸을 잘라낸 이미지입니다. 칸에 적힌 문자열만 답합니다."


def make(doc):
    from PIL import Image

    r, out = doc.r, []
    boxed = [f for f in doc.visible if f.get("bbox") and f.get("page", 0) < len(r["images"])]
    # 칸 수가 적어도 sample 을 부른다 (난수를 쓰는 횟수가 세트를 정한다)
    for j, f in enumerate(sorted(doc.rng.sample(boxed, min(len(boxed), doc.fields_per_doc)), key=boxed.index)):
        img = Image.open(doc.out / r["images"][f.get("page", 0)])
        x0, y0, x1, y1 = f["bbox"]
        pad = (y1 - y0) * 0.25 + 4
        box = (max(0, int(x0 - pad)), max(0, int(y0 - pad)), min(img.width, int(x1 + pad)), min(img.height, int(y1 + pad)))
        if box[2] - box[0] < 4 or box[3] - box[1] < 4:
            continue
        crop_path = f"crops/{doc.sid}_{j}.png"
        img.crop(box).convert("RGB").save(doc.out / crop_path)
        out.append({"id": f"ocr_field/{doc.sid}/{f['key']}", "task": TASK, "images": [crop_path],
                    "prompt": PROMPT, "answer": str(f["value"]).replace("\n", " "),
                    "meta": {**doc.meta, "n_pages": 1, "key": f["key"], "label": f.get("label"), "kind": field_kind(f),
                             "writing": doc.writing(f["key"]), "corrected": bool(f.get("corrected_from")),
                             "length": len(norm_text(f["value"]))}})
    return out
