"""form_qa — 서식 전용 질문. 서식 폴더 qa.py 의 함수마다 그 서식 문서 한 건에 질문 하나 (docgen/formqa.py).

질문·정답: qa.py 의 함수가 돌려준 (질문, 정답) 그대로. 정답은 그린 문서의 칸 값 v 로 함수가 만든다.
           칸이 빈 문서(함수가 v["키"] 에서 KeyError)나 None 을 돌려준 문서에서는 묻지 않는다.
eval.answer_type: 정답 꼴 — number · yesno · text · json (docgen/formqa.kind)
meta.question: "<서식ID>.<함수 이름>" — 채점 함수·보고서에서 질문을 가를 때
채점: evaluate.s_form_qa (정답 꼴로 기본 채점), 주 지표 acc. 다르게 채점하려면 train/scorers 의 채점 함수
      (견본 train/scorers/form_qa_example.py)
"""
from ... import formqa as FQA

TASK = "form_qa"
NAME = "서식 전용 질문"
PROMPT = "(서식 폴더 qa.py 의 함수가 돌려준 질문 — 서식마다 다름)"
ANSWER = {"anyOf": [{"type": "string"}, {"type": "number"}, {"type": "string", "enum": ["예", "아니오"]}, {"type": "object"},
                    {"type": "array"}]}
EXAMPLE = 35000000
NOTES = ("서식마다 사람이 정한 질문입니다. eval.answer_type 이 number 면 숫자, yesno 면 예/아니오, text 면 질문이 정한 꼴의 글, "
         "json 이면 질문이 정한 JSON 으로 답합니다.")


def make(doc):
    doc_id = doc.r["doc_id"]
    return [{"id": f"form_qa/{doc.sid}/{q['name']}", "task": TASK, "prompt": q["prompt"], "answer": q["answer"],
             "eval": {"answer_type": q["kind"]}, **doc.base, "meta": {**doc.meta, "question": f"{doc_id}.{q['name']}"}}
            for q in FQA.ask(doc_id, doc.fields)]
