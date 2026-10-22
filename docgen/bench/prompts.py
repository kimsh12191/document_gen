"""평가 문항의 질문 문장 (build 가 쓰고, studio·학습 실행도 같은 문장으로 묻는다).

표준 라이브러리만 쓰므로 렌더링 환경(jinja2·Playwright)이 없어도 import 된다.
문장을 바꾸면 guide/questions.md 도 같이 고친다 (docgen/tests/test_bench.py 가 둘이 같은지 본다).
"""

P_CLASSIFY = ("이 문서는 고객이 은행에 제출한 서류입니다. 서류의 정식 명칭(서류명)을 답하세요. "
              "설명 없이 서류명만 한 줄로 답하세요.")
P_OCR_PAGE = ("이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, "
              "표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.")
P_OCR_FIELD = "이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요."
# kie·marks 는 값과 함께 위치를 답한다 (평가 세트 2.0). 좌표는 OCR 과제와 같은 bbox_2d: 그 쪽 이미지 기준 0~1000 정수.
P_KIE = ("이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 "
         '{{"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}} 를 쓰세요. '
         "좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 "
         '{{"key": 키, "value": null}} 로 답하세요.\n항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))\n{items}')
P_MARKS = ("이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.\n"
           '- 체크박스: 체크된 보기마다 {{"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}}. '
           '체크된 것이 없으면 {{"key": 키, "value": null}}\n'
           "- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)\n"
           '- 도장·서명: {{"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽}} (비어 있으면 value 만 false)\n항목\n{items}')
P_DOC_CHECK = ("고객 '{customer}' 님이 '{task}' 업무를 위해 서류를 제출했습니다. 첨부 이미지는 제출된 서류의 첫 쪽입니다 "
               "(순서 무관).\n필수 제출 서류:\n{required}\n\n제출 서류를 확인해 다음을 JSON 으로 답하세요.\n"
               "- missing: 필수 서류 중 제출되지 않은 서류. 고객 본인 명의가 아닌 서류만 낸 경우도 제출되지 않은 것으로 봅니다.\n"
               "- not_required: 제출됐지만 필수 서류 목록에 없는 서류\n"
               "- not_customer: 고객 본인 명의가 아닌 서류\n"
               '{{"missing": ["서류명", ...], "not_required": [...], "not_customer": [...]}} 형식으로 답하고, 해당 없으면 빈 목록 [] 으로 '
               "두세요. 서류명은 목록에 있으면 목록 그대로, 없으면 서류에 적힌 제목대로 쓰세요.")
P_CROSS = ("고객 '{customer}' 님이 '{task}' 업무를 위해 제출한 서류 {n}건입니다 (이미지 {pages}장). 서류들을 서로 대조해 "
           "맞지 않는 정보(성명, 주민등록번호, 생년월일, 주소, 연락처, 계좌번호, 상호, 금액, 날짜 등), 업무상 맞지 않는 관계"
           "(계약 상대방이 등기부 소유자가 아님, 금액·날짜 관계 오류 등), 고객 본인 명의가 아닌 서류가 있는지 확인하세요. "
           "표기 방식만 다른 것(날짜 형식, 주민번호 뒷자리 가림, 하이픈 유무 등)은 불일치가 아닙니다.\n"
           '{{"consistent": true 또는 false, "issues": [{{"document": "문제가 있는 서류명", "field": "항목명", '
           '"value": "그 서류에 적힌 값", "expected": "다른 서류에 적힌 값"}}]}} 형식의 JSON 으로 답하세요. '
           '문제가 없으면 {{"consistent": true, "issues": []}} 입니다.')


def kie_line(form_id: str | None, key: str, label: str | None, doc_key: str | None = None, extra: str = "",
             siblings: list[dict] | None = None) -> str:
    """kie·marks 항목 한 줄: '- 키: 항목명 (설명)'. 설명은 키 사전의 누구의 무엇과 표의 행 (docgen.dictionary.describe).
    extra 는 marks 의 종류·보기처럼 괄호에 같이 넣을 것. siblings(그 문서의 같은 과제 칸, 문서 순서)에 항목명이 같은 칸이
    또 있으면 몇 번째 칸인지 붙인다 (작성일·작성일2 처럼 행 번호가 없는 반복 칸)."""
    from .. import dictionary as DIC

    desc = DIC.describe(form_id, key, label, doc_key)
    same = [s["key"] for s in siblings or [] if DIC._norm(s.get("label") or "") == DIC._norm(label or "")]
    me = key if key in same else doc_key   # 공통 키로 묻는 칸은 서식의 키로 찾는다
    if label and len(same) > 1 and me in same and not any(p.isdigit() for p in key.split(".")):
        desc = ", ".join(x for x in [desc, f"같은 항목명 중 {same.index(me) + 1}번째 칸"] if x)
    note = ", ".join(x for x in [desc, extra] if x)
    return f"- {key}: {label or '-'}" + (f" ({note})" if note else "")


P_REVIEW ="고객이 '{task}' 업무를 위해 제출한 서류입니다 (이미지 {pages}장).\n{question}"
