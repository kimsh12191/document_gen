"""과제별 질문 원본과 정답 계약. 서류 한 건 과제는 과제 파일(docgen/bench/tasks/<과제>.py)의 PROMPT·ANSWER·EXAMPLE·NOTES 를,
업무 묶음 과제는 아래 설명과 생성기 상수(prompts.py)를 그대로 보여 준다.

studio 가 질문 형식 API(/api/question-formats, studio/app.py)로 보여 준다. 채점에는 쓰지 않는다.
"""
from . import prompts as P
from .tasks import BOX, ENTRY, LOCATION, STRINGS, classify, contract, freetext, kie, marks, ocr_field, ocr_page  # noqa: F401

SINGLE_ORDER = (classify, ocr_field, ocr_page, kie, marks, freetext)   # 화면에 보이는 차례


def contracts() -> dict:
    return {
        **{t.TASK: contract(t) for t in SINGLE_ORDER},
        "doc_check": {"name": "서류 구비 검사", "prompt_template": P.P_DOC_CHECK,
                      "answer_schema": {"type": "object", "required": ["missing", "not_required", "not_customer"],
                                        "properties": {key: STRINGS for key in ("missing", "not_required", "not_customer")}},
                      "example": {"missing": ["재직증명서"], "not_required": [], "not_customer": []},
                      "notes": "목록에는 서류명을 씁니다. 타인 명의의 필수 서류만 냈다면 missing과 not_customer에 모두 포함합니다. 입력은 제출 서류의 첫 쪽들입니다."},
        "cross_check": {"name": "서류 간 대조", "prompt_template": P.P_CROSS,
                        "answer_schema": {"type": "object", "required": ["consistent", "issues"], "properties": {
                            "consistent": {"type": "boolean"}, "issues": {"type": "array", "items": {"type": "object",
                                "required": ["document", "field", "value", "expected"], "properties": {
                                    "document": {"type": "string"}, "field": {"type": ["string", "null"]},
                                    "value": {"type": ["string", "number", "null"]}, "expected": {"type": ["string", "number", "null"]}}}}}},
                        "example": {"consistent": False, "issues": [{"document": "재직증명서", "field": "성명", "value": "김다름", "expected": "홍길동"}]},
                        "notes": "정상은 consistent:true, issues:[]입니다. 데이터 정답에 있는 alt_documents는 짝 서류도 인정하는 채점 보조 정보이며 모델 답의 필수 키가 아닙니다."},
        "review": {"name": "심사·계산·필드 비교", "prompt_template": P.P_REVIEW,
                   "answer_schema": {"anyOf": [{"type": "number"}, {"type": "string", "enum": ["예", "아니오"]}]},
                   "example": "예", "notes": "eval.answer_type이 number이면 질문에 적힌 단위·반올림 기준에 맞춘 숫자, yesno이면 예/아니오입니다. 숫자 허용 오차는 eval.tol에 있습니다."},
    }
