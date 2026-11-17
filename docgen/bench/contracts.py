"""과제별 질문 원본과 정답 계약: 과제 파일(docgen/bench/tasks/<과제>.py)의 PROMPT·ANSWER·EXAMPLE·NOTES 를 그대로 보여 준다.

studio 가 질문 형식 API(/api/question-formats, studio/app.py)로 보여 준다. 채점에는 쓰지 않는다.
"""
from .tasks import (BOX, ENTRY, LOCATION, STRINGS, classify, contract, form_qa, freetext, kie, marks, ocr_field,  # noqa: F401
                    ocr_page, table, table_find, table_qa, table_read)

SINGLE_ORDER = (classify, ocr_field, ocr_page, kie, marks, freetext, form_qa, table, table_read, table_find, table_qa)   # 화면에 보이는 차례


def contracts() -> dict:
    return {
        **{t.TASK: contract(t) for t in SINGLE_ORDER},
    }
