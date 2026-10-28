"""kie — 정보 추출. 서류 한 건의 모든 쪽을 보고, 질문에 적은 항목마다 값과 위치를 답한다.

질문: P_KIE + 항목 줄 '- 키: 항목명 (설명)' (prompts.kie_line). 항목은 체크·도장·서명과 묶음 칸을 뺀 칸 전부,
      max_keys(기본 40)개를 넘으면 그만큼만 골라 문서 순서로.
      어떤 칸을 어떤 항목명·설명으로 묻나는 칸 목록 fields.json 의 그 칸 "q" (ask·label·note)
정답: 항목마다 {"key": 키, "value": 서식을 그릴 때 넣은 값, "bbox_2d": 0~1000 좌표, "page": 쪽}.
      빈 칸은 {"key": 키, "value": null} (위치 없음). 값·위치 모두 그릴 때 기록한 것 그대로 — 사람이 따로 단 정답이 아니다
      질문 전문(prompt)·항목 줄 꼴(line)·답 꼴(answer: list_box 위 꼴 / list 위치 없이 / object {키: 값})은
      서식 폴더 questions.json 의 kie 에서 (없으면 공통). list·object 는 eval.answer 에 적혀 값 점수(f1)가 주 지표
eval.fields: 키마다 타입(날짜·금액 등 표기를 맞춰 비교)·norm·값 종류
채점: evaluate.s_kie, 주 지표 vl_f1 (값+위치), 값만은 f1
"""
from ... import formquestions as FQ
from .. import prompts
from . import ENTRY, MARK_TYPES, field_kind

TASK = "kie"
NAME = "정보 추출"
PROMPT = prompts.P_KIE
ANSWER = {"type": "array", "items": ENTRY}
EXAMPLE = [{"key": "employee.name", "value": "홍길동", "bbox_2d": [100, 200, 300, 230], "page": 1}, {"key": "memo", "value": None}]
NOTES = ("key는 질문의 키 그대로, value는 문서 표시값입니다. 좌표는 해당 쪽 기준 0~1000, page는 1부터입니다. "
         "비어 있거나 없는 항목은 value:null이며 위치를 생략합니다.")


def items(fields: list[dict]) -> list[dict]:
    """물을 수 있는 칸: 체크·도장·서명, 묶음 칸을 뺀 전부."""
    return [f for f in fields if f["type"] not in MARK_TYPES and not f.get("group")
            and not f["key"].startswith(("seal.", "sign."))]


def answer(doc, f, shape: str = "list_box") -> dict:
    where = doc.where(f, f.get("bbox")) if f["value"] is not None and shape == "list_box" else {}
    return {"key": f["key"], "value": f["value"], **where}


def make(doc):
    all_kf = FQ.pick(doc.q, TASK, items(doc.fields), doc.fq)   # 서식의 questions.json 대로. 같은 항목명 칸의 순번은 뽑기 전 전체에서 센다
    kf = doc.sample(all_kf, doc.max_keys)
    if not kf:
        return []
    line, shape = FQ.shell(doc.q, TASK)   # 서식의 항목 줄 꼴·답 꼴 (없으면 공통)
    lines = "\n".join(prompts.kie_line(doc.r["doc_id"], f["key"], f.get("label"), f.get("doc_key"), siblings=all_kf,
                                        note=f.get("_note"), line=line) for f in kf)
    ans = [answer(doc, f, shape) for f in kf]
    ev = {"fields": {f["key"]: {"type": f["type"], "norm": f.get("norm"), "kind": field_kind(f)} for f in kf}}
    return [{"id": f"kie/{doc.sid}", "task": TASK, "prompt": FQ.prompt(doc.q, TASK, lines),
             "answer": {a["key"]: a["value"] for a in ans} if shape == "object" else ans,
             "eval": ev if shape == "list_box" else {**ev, "answer": shape}, **doc.base}]
