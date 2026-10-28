"""classify — 서류 분류. 그림(서류 한 건의 모든 쪽)을 보고 서류의 정식 명칭을 답한다.

질문: P_CLASSIFY (고정 문장)
정답: 문서명 한 줄. 같은 문서의 서식이 여러 개여도 정답은 하나 (키 사전 docgen/dictionary 의 문서명),
      서식 이름·다른 이름도 맞게 친다 (eval.aliases). 서식 폴더 questions.json 의 classify 가 있으면 그 정답·다른 이름
채점: evaluate.s_classify, 주 지표 acc
"""
from .. import prompts
from ... import dictionary as DIC

TASK = "classify"
NAME = "서류 분류"
PROMPT = prompts.P_CLASSIFY
ANSWER = {"type": "string"}
EXAMPLE = "재직증명서"
NOTES = "서류의 정식 명칭 한 줄. 설명을 붙이지 않습니다."


def make(doc):
    r = doc.r
    name, aliases = DIC.doc_name(r["doc_id"], r["name"])   # 정답 = 문서명, 서식 이름·다른 이름도 맞음
    mine = (doc.q or {}).get("classify") or {}   # 서식의 questions.json 이 정하면 그것
    name, aliases = mine.get("answer") or name, mine.get("aliases", aliases)
    return [{"id": f"classify/{doc.sid}", "task": TASK, "prompt": PROMPT, "answer": name,
             **({"eval": {"aliases": aliases}} if aliases else {}), **doc.base}]
