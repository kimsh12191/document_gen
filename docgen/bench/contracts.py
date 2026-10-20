"""과제별 질문 원본과 정답 계약. 표시용 설명만 두고 프롬프트는 생성기 상수를 직접 참조한다."""
from . import prompts as P

BOX = {"type": "array", "items": {"type": "integer", "minimum": 0, "maximum": 1000}, "minItems": 4, "maxItems": 4}
LOCATION = {"bbox_2d": BOX, "page": {"type": "integer", "minimum": 1}}
STRINGS = {"type": "array", "items": {"type": "string"}}
ENTRY = {"type": "object", "required": ["key", "value"], "properties": {
    "key": {"type": "string"}, "value": {"type": ["string", "number", "null"]}, **LOCATION}}


def contracts() -> dict:
    return {
        "classify": {"name": "서류 분류", "prompt_template": P.P_CLASSIFY, "answer_schema": {"type": "string"},
                     "example": "재직증명서", "notes": "서류의 정식 명칭 한 줄. 설명을 붙이지 않습니다."},
        "ocr_field": {"name": "값 칸 OCR", "prompt_template": P.P_OCR_FIELD, "answer_schema": {"type": "string"},
                      "example": "홍길동", "notes": "입력은 값 칸을 잘라낸 이미지입니다. 칸에 적힌 문자열만 답합니다."},
        "ocr_page": {"name": "문서 OCR", "prompt_template": P.P_OCR_PAGE, "answer_schema": STRINGS,
                     "example": ["홍길동", "2026년 1월 31일"],
                     "notes": "데이터의 answer는 채점할 값 문자열의 목록입니다. 모델은 줄바꿈한 전체 텍스트를 출력합니다. 고정 인쇄 문구까지 정답인 합성 OCR 세트와 구분합니다."},
        "kie": {"name": "정보 추출", "prompt_template": P.P_KIE, "answer_schema": {"type": "array", "items": ENTRY},
                "example": [{"key": "employee.name", "value": "홍길동", "bbox_2d": [100, 200, 300, 230], "page": 1}, {"key": "memo", "value": None}],
                "notes": "key는 질문의 키 그대로, value는 문서 표시값입니다. 좌표는 해당 쪽 기준 0~1000, page는 1부터입니다. 비어 있거나 없는 항목은 value:null이며 위치를 생략합니다."},
        "marks": {"name": "체크·도장·서명 검사", "prompt_template": P.P_MARKS,
                  "answer_schema": {"type": "array", "items": {**ENTRY, "properties": {**ENTRY["properties"], "value": {"type": ["string", "boolean", "null"]}}}},
                  "example": [{"key": "consent", "value": "동의", "bbox_2d": [100, 200, 120, 220], "page": 1}, {"key": "seal", "value": False}],
                  "notes": "체크박스는 체크된 보기마다 한 항목(없으면 null), 도장·서명은 true/false입니다. 표시가 있으면 그 위치와 쪽을 답합니다."},
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
