"""kie — 정보 추출. 서류 한 건의 모든 쪽을 보고, 질문에 적은 항목마다 값과 위치를 답한다.

질문: P_KIE + 항목 줄 '- 키: 키 설명 (덧붙임)' (prompts.kie_line). 항목은 체크·도장·서명과 묶음 칸, 표 칸(table 과제가 묻는다,
      Doc.table_keys)을 뺀 칸 전부, max_keys(기본 40)개를 넘으면 그만큼만 골라 문서 순서로.
      일부 문항(ABSENT_RATE)에는 이 서류에 없는 칸 1~3개를 아무 자리에나 섞는다 (같은 그룹 다른 서식의 칸, 정답 null —
      docgen/bench/absent.py).
      어떤 칸을 어떤 항목명·설명으로 묻나는 칸 목록 fields.json 의 그 칸 "q" (ask·label·note)
정답: 항목마다 {"key": 키, "value": 서식을 그릴 때 넣은 값, "bbox_2d": 0~1000 좌표, "page": 쪽}.
      빈 칸은 {"key": 키, "value": null} (위치 없음). 값·위치 모두 그릴 때 기록한 것 그대로 — 사람이 따로 단 정답이 아니다
      질문 전문(prompt)·질문 항목 줄 틀(item)·답 항목 틀(answer, answer_empty)은 서식 폴더 questions.json 의 kie (없으면 공통
      docgen/forms/_common/questions.json). 답 틀의 칸 이름이 기본과 다르면 eval.answer_fields 에 적어 채점이 거꾸로 읽는다.
      답 틀에 위치(bbox_2d)가 없으면 값 점수(f1)가 주 지표.
      답 틀이 글자("{label}: {value}")면 줄글 답 — 칸마다 한 줄. eval.text 에 틀·항목명, eval.gold 에 [{"key", "value"}]
      (채점은 틀로 줄글에서 값을 찾아 값 점수 f1)
eval.fields: 키마다 타입(날짜·금액 등 표기를 맞춰 비교)·norm·값 종류
채점: evaluate.s_kie, 주 지표 vl_f1 (값+위치), 값만은 f1
"""
from ... import formquestions as FQ
from .. import prompts
from . import ENTRY, MARK_TYPES, field_kind

ABSENT_RATE = 0.3   # 없는 칸을 섞는 문항 비율
ABSENT_N = (1, 3)   # 섞는 개수

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


def answer(doc, f, tpl: dict, empty: dict) -> dict:
    """칸 하나의 답 항목: 답 틀에 키·그린 값·위치를 채운다 (docgen/formquestions.fill_answer)."""
    where = doc.where(f, f.get("bbox")) if f["value"] is not None else {}
    return FQ.fill_answer(tpl, empty, f["key"], f["value"], where)


def make(doc):
    from ..absent import absent_keys

    mine = [f for f in items(doc.fields) if f["key"] not in doc.table_keys]   # 표 칸은 table 과제가 묻는다
    all_kf = FQ.pick(doc.q, TASK, mine, doc.fq)   # 서식의 questions.json 대로. 같은 항목명 칸의 순번은 뽑기 전 전체에서 센다
    kf = doc.sample(all_kf, doc.max_keys)
    if not kf:
        return []
    if doc.rng.random() < ABSENT_RATE:   # 이 서류에 없는 칸 (정답 null)
        kf = list(kf)
        for f in absent_keys(doc, doc.rng.randint(*ABSENT_N)):
            kf.insert(doc.rng.randrange(len(kf) + 1), f)
    item, tpl, empty = FQ.shell(doc.q, TASK)   # 질문 항목 줄 틀·답 항목 틀·빈 칸 틀 (서식 questions.json, 없으면 공통)
    lines = "\n".join(prompts.kie_line(f["key"], f.get("label"), siblings=all_kf,
                                        note=f.get("_note"), line=item) for f in kf)
    ev = {"fields": {f["key"]: {"type": f["type"], "norm": f.get("norm"), "kind": "absent" if f.get("_absent") else field_kind(f)}
                     for f in kf}}
    if any(f.get("_absent") for f in kf):
        ev["absent"] = [f["key"] for f in kf if f.get("_absent")]
    if isinstance(tpl, str):   # 줄글 답
        ev |= {"text": {"answer": tpl, "answer_empty": empty, "labels": {f["key"]: f.get("label") or "-" for f in kf}},
               "gold": [{"key": f["key"], "value": f["value"]} for f in kf]}
        ans = "\n".join(FQ.fill_text(tpl, empty, f["key"], f.get("label"), f["value"]) for f in kf)
        return [{"id": f"kie/{doc.sid}", "task": TASK, "prompt": FQ.prompt(doc.q, TASK, lines), "answer": ans, "eval": ev, **doc.base}]
    names = FQ.answer_fields(tpl)
    if names != {p: p for p in FQ.PLACES}:   # 답 틀의 칸 이름이 기본과 다르면 채점이 거꾸로 읽게 적어 둔다
        ev["answer_fields"] = names
    return [{"id": f"kie/{doc.sid}", "task": TASK, "prompt": FQ.prompt(doc.q, TASK, lines),
             "answer": [answer(doc, f, tpl, empty) for f in kf], "eval": ev, **doc.base}]
