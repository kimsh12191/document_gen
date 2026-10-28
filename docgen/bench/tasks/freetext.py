"""freetext — 기타 칸 정리. 기타·비고·사유·용도 칸에 사람이 대충 쓴 글을 DB 칸(용도·금액·날짜 …)으로 정리한다.

질문: P_FREETEXT (prompts.freetext_prompt: 칸 이름, 기준일, 보기 목록)
정답: 서식을 그릴 때 docgen/freetext.py 가 글과 함께 만든 정리값 (data["_freetext"][글]). 그 글이 들어간 칸마다 문항 하나
채점: evaluate.s_freetext, 주 지표 f1
"""
from .. import prompts
from . import STRINGS

TASK = "freetext"
NAME = "기타 칸 정리"
PROMPT = prompts.P_FREETEXT
ANSWER = {"type": "object", "properties": {
    **{k: {"type": "string"} for k in ("purpose", "reason", "date", "request", "memo")},
    "amount": {"type": "integer"}, "period_months": {"type": "integer"}, "approx": STRINGS}}
EXAMPLE = {"purpose": "생활자금", "amount": 30000000, "period_months": 12, "approx": ["amount"]}
NOTES = ("기타·비고·사유 칸의 자유 기재를 DB 칸으로 정리합니다. 적힌 키만 쓰고 null 은 쓰지 않습니다. "
         "용도·사유·요청은 질문의 보기 중 하나, 금액은 원 단위 정수, 날짜는 YYYY-MM-DD(상대 날짜는 질문의 기준일로 계산)입니다.")


def make(doc):
    written = (doc.r.get("data") or {}).get("_freetext") or {}
    out = []
    for f in doc.fields:
        ft = written.get(f["value"]) if isinstance(f.get("value"), str) else None
        if ft:
            out.append({"id": f"freetext/{doc.sid}/{f['key']}", "task": TASK,
                        "prompt": prompts.freetext_prompt((f.get("label") or f["key"]).strip(), ft["basis"]),
                        "answer": ft["answer"], **doc.base,
                        "meta": {**doc.meta, "key": f["key"], "label": f.get("label"), "level": ft["level"]}})
    return out
