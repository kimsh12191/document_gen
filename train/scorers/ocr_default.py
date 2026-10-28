"""채점 함수 견본: docgen 기본 OCR 채점 — 쪽 OCR 8과제(합성 OCR 세트·실서류 OCR 준비 폴더)와 값 칸 OCR·전체 받아쓰기.

  {"id": "ocr", "paths": ["<OCR 데이터셋>"], "scorer": "scorers/my_ocr.py:score"}

기본 채점과 다른 점 하나: 기본 채점은 쪽 OCR 지표를 과제 전체로 낸다 (CER = 틀린 글자 합 / 전체 글자 수).
채점 함수는 문항마다 점수를 내고 평균하므로, 같은 답이라도 CER 등이 기본 표와 조금 다르다 (긴 칸·짧은 칸의 무게가 같아짐).
문항 점수 계산 자체는 같다 (docgen.bench.ocr_metrics).

과제와 주 지표
  crop_ocr 칸 잘라 읽기 cer↓ · bbox_ocr 좌표→글자 em · region_ocr 영역 받아쓰기 cer↓ · marked_ocr 그린 박스→글자 em
  grounding 글자→좌표 f1_iou50 · spotting 글자 찾기 e2e_f1 · relation 항목명→값 e2e_f1 · marked_box 그린 박스→좌표 f1_iou75
  ocr_field 값 칸 OCR exact · ocr_page 전체 받아쓰기 recall
글자 비교는 NFC·줄바꿈 정리 후, 박스는 그 쪽 이미지 기준 0~1000 좌표의 IoU.
"""
from docgen.bench import evaluate as E
from docgen.bench import ocr_metrics as OM


def page_ocr(item, output):
    """쪽 OCR 한 문항의 지표 (기본 채점이 과제 전체에 쓰는 계산을 문항 하나에)."""
    task = item["task"]
    rows = [{"id": item["id"], "task": task, "target": item["answer"]}]
    calc = OM._text_metrics if task in OM.TEXT_TASKS else OM._box_metrics
    m = calc(rows, {item["id"]: OM.answer(output or "")})
    return {"metrics": {k: (None if v is None else float(v)) for k, v in m.items()
                        if not k.endswith("_count") and (v is None or isinstance(v, (int, float)))}}


def score(item, output):
    task = item["task"]
    if task in OM.TASKS:
        r = page_ocr(item, output)
    elif task in ("ocr_field", "ocr_page"):
        r = E.SCORERS[task](item, output)
    else:
        raise ValueError(f"이 견본은 {task} 과제를 모릅니다 (은행 서류 과제는 bank_default.py)")
    return {**r, "main": E.MAIN[task]}
