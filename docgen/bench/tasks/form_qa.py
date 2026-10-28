"""form_qa — 서식 전용 질문. 서식 폴더 questions.json 의 extra 에 적은 질문을 그 서식 문서마다 하나씩 묻는다.

질문: extra 의 prompt 그대로 (서식마다 사람이 쓴 문장 — 공통 지시문이 없다)
정답: 한 줄. 그 문서의 칸 값에서 만든다 (docgen/formquestions.py)
      type text   — answer 의 {키} 를 칸 값으로 채운 글  ("{bank} {branch}" → "국민은행 센텀지점")
      type number — answer 를 채워 숫자로 ("{loan.amount}" → 35000000, 금액 단위 표기는 칸의 정규화 값)
      type yesno  — when 칸에 값이 있으면 "예", 비었거나 없으면 "아니오"
      {키} 는 질문 키(공통 키)나 서식의 원래 키. 칸이 없거나 비어 있으면 (text·number) 그 문서에서는 묻지 않는다
eval: answer_type, tol (number 허용 오차, 기본 0)
채점: evaluate.s_form_qa, 주 지표 acc (text 는 띄어쓰기·문장부호를 맞춰 같은지, number·yesno 는 심사 질의와 같은 채점)
"""
from ... import formquestions as FQ
from ..metrics import is_null, to_number

TASK = "form_qa"
NAME = "서식 전용 질문"
PROMPT = "(서식 폴더 questions.json 의 extra[].prompt — 서식마다 다름)"
ANSWER = {"anyOf": [{"type": "string"}, {"type": "number"}, {"type": "string", "enum": ["예", "아니오"]}]}
EXAMPLE = 35000000
NOTES = ("서식마다 사람이 정한 질문입니다. eval.answer_type 이 number 면 숫자, yesno 면 예/아니오, text 면 문서에 적힌 글자 "
         "(질문이 정한 꼴)로 답합니다.")


def _fill(template: str, fields: list[dict]):
    """{키} 를 칸 값으로. 칸이 없거나 비면 None. → (글, 칸 하나만 쓴 경우 그 칸)."""
    used = []

    def one(m):
        f = FQ.field_value(fields, m.group(1))
        if f is None or is_null(f.get("value")):
            raise LookupError(m.group(1))
        used.append(f)
        return str(f["value"])
    try:
        text = FQ.PLACE.sub(one, template)
    except LookupError:
        return None, None
    return text, used[0] if len(used) == 1 and template.strip() == "{" + FQ.PLACE.search(template).group(1) + "}" else None


def answer(x: dict, fields: list[dict]):
    """extra 한 줄 → 정답 (못 만들면 None)."""
    if x["type"] == "yesno":
        f = FQ.field_value(fields, x["when"])
        return "아니오" if f is None or is_null(f.get("value")) else "예"
    text, only = _fill(x["answer"], fields)
    if text is None:
        return None
    if x["type"] == "text":
        return text
    n = only.get("norm") if only is not None and isinstance(only.get("norm"), (int, float)) \
        and not isinstance(only.get("norm"), bool) else to_number(text)
    if n is None:
        return None
    return int(n) if float(n).is_integer() else float(n)


def make(doc):
    out = []
    for x in (doc.q or {}).get("extra") or []:
        a = answer(x, doc.fields)
        if a is None:
            continue
        out.append({"id": f"form_qa/{doc.sid}/{x['id']}", "task": TASK, "prompt": x["prompt"], "answer": a,
                    "eval": {"answer_type": x["type"], "tol": x.get("tol", 0)},
                    **doc.base, "meta": {**doc.meta, "question": x["id"]}})
    return out
