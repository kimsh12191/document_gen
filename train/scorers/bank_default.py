"""채점 함수 견본: docgen studio 기본 채점 그대로 — 합성 은행 서류 세트(bank-* 레시피, docgen.bench build) 전부.

과제마다 함수 하나 (아래 TASKS). 한 과제만 바꾸려면 이 파일을 복사해 그 함수만 고친다. 고치지 않은 과제는 기본 채점과 같은 점수.
  {"id": "syn", "paths": ["<bank 데이터셋>"], "scorer": "scorers/my_bank.py:score"}
꼴·규칙은 train/scorers/kie_default.py 맨 위, guide/eval.md 2절 '채점'. 쪽 OCR 8과제는 ocr_default.py.
"""
from docgen.bench import evaluate as E


def classify(item, output):
    """서류 분류: 답 첫 줄이 정답 서류명이나 그 다른 이름(item["eval"]["aliases"])과 같으면 1 (공백·문장부호 무시). 주 지표 acc."""
    return E.s_classify(item, output)


def kie(item, output):
    """정보 추출: 키마다 값 비교(타입별: 금액·숫자는 숫자 값, 날짜는 날짜, 그 밖은 대소문자·공백·문장부호 무시) → f1,
    정답에 위치가 있으면 같은 키·같은 쪽 IoU 0.5 이상 → loc_f1, 둘 다 → vl_f1 (주 지표). 값만 고치려면 kie_default.py."""
    return E.s_kie(item, output)


def marks(item, output):
    """체크·도장·서명: 체크된 보기 글자, 도장·서명 유무(true/false) + 위치. 주 지표 vl_f1 (위치 없는 1.x 세트는 acc)."""
    return E.s_marks(item, output)


def freetext(item, output):
    """기타 칸 정리: 키마다 정확히 같은 값 (금액·기간 숫자, 날짜 YYYY-MM-DD, 보기 글자). memo 만 띄어쓰기 허용. 주 지표 f1."""
    return E.s_freetext(item, output)


def form_qa(item, output):
    """서식 전용 질문 (서식 폴더 qa.py): 정답 꼴로 — 숫자·예/아니오는 심사 질의와 같게, 글은 띄어쓰기·문장부호를 맞춰 같은지,
    JSON 은 칸마다 같은지. 주 지표 acc. 질문 하나만 다르게 채점하려면 form_qa_example.py."""
    return E.s_form_qa(item, output)


def doc_check(item, output):
    """서류 구비 확인: missing·not_required·not_customer 세 목록이 모두 맞으면 exact (주 지표), 목록 F1 은 set_f1."""
    return E.s_doc_check(item, output)


def cross_check(item, output):
    """서류 간 대조: 정상 문항은 consistent=true 면 1, 변조 문항은 탐지(detect) + 문제 서류·값까지 맞힘. 주 지표 score."""
    return E.s_cross_check(item, output)


def review(item, output):
    """심사 질의: 예/아니오, 숫자(허용 오차 item["eval"]["tol"]), 짧은 답 일치. 주 지표 acc."""
    return E.s_review(item, output)


def ocr_field(item, output):
    """값 칸 OCR: 글자 그대로(공백 무시) 같으면 exact (주 지표), 글자 오류율 cer."""
    return E.s_ocr_field(item, output)


def ocr_page(item, output):
    """전체 받아쓰기: 정답 값들이 받아쓴 글 안에 있는 비율 recall (주 지표), 20% 글자 오차 허용 recall_fuzzy."""
    return E.s_ocr_page(item, output)


TASKS = {"classify": classify, "kie": kie, "marks": marks, "freetext": freetext, "form_qa": form_qa, "doc_check": doc_check,
         "cross_check": cross_check, "review": review, "ocr_field": ocr_field, "ocr_page": ocr_page}


def score(item, output):
    task = item["task"]
    if task not in TASKS:
        raise ValueError(f"이 견본은 {task} 과제를 모릅니다 (쪽 OCR 은 ocr_default.py)")
    r = TASKS[task](item, output)
    return {**r, "main": r.get("main") or E.main_metric(task, r["metrics"])}
