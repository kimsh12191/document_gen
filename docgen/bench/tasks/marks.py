"""marks — 체크박스·도장·서명. 서류 한 건의 모든 쪽을 보고 체크된 보기, 도장·서명이 있는지와 그 위치를 답한다.

질문: P_MARKS + 항목 줄 '- 키: 항목명 (종류, 보기: …)' (prompts.kie_line). 항목은 보기가 있는 체크박스와 도장·서명 자리,
      max_keys 개를 넘으면 그만큼만 골라 문서 순서로. 어떤 칸을 어떤 항목명으로 묻나는 칸 목록 fields.json 의 그 칸 "q"
정답: 체크박스 — 체크된 보기마다 {"key", "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page"}, 없으면 {"key", "value": null}
      도장·서명 — {"key", "value": true/false, 있으면 위치}. 모두 그릴 때 기록한 체크 상태·위치 그대로
eval.types: 키마다 checkbox / checkbox_multi / seal / signature
질문 전문·질문 항목 줄 틀(item)·답 항목 틀(answer, answer_empty)은 서식 폴더 questions.json 의 marks (없으면 공통).
답 틀이 글자면 줄글 답 (도장·서명 값은 있음/없음) — kie 와 같음
채점: evaluate.s_marks, 주 지표 vl_f1
"""
from ... import formquestions as FQ
from .. import prompts
from . import ENTRY, MARK_TYPES

TASK = "marks"
NAME = "체크·도장·서명 검사"
PROMPT = prompts.P_MARKS
ANSWER = {"type": "array", "items": {**ENTRY, "properties": {**ENTRY["properties"], "value": {"type": ["string", "boolean", "null"]}}}}
EXAMPLE = [{"key": "consent", "value": "동의", "bbox_2d": [100, 200, 120, 220], "page": 1}, {"key": "seal", "value": False}]
NOTES = ("체크박스는 체크된 보기마다 한 항목(없으면 null), 도장·서명은 true/false입니다. "
         "표시가 있으면 그 위치와 쪽을 답합니다.")


def items(fields: list[dict]) -> list[dict]:
    """물을 수 있는 칸: 보기가 있는 체크박스, 도장·서명 자리 (이름 없는 도장 seal.untagged 는 뺀다)."""
    return [f for f in fields if f["type"] in MARK_TYPES and not f["key"].startswith("seal.untagged")
            and (f["type"] in ("seal", "signature") or f.get("options"))]


def make(doc):
    all_mf = FQ.pick(doc.q, TASK, items(doc.fields), doc.fq)   # 서식의 questions.json 대로
    mf = doc.sample(all_mf, doc.max_keys)
    if not mf:
        return []
    form_line, tpl, empty = FQ.shell(doc.q, TASK)   # 질문 항목 줄 틀·답 항목 틀·빈 칸 틀 (서식 questions.json, 없으면 공통)
    text = isinstance(tpl, str)   # 줄글 답: 정답은 [{"key", "value"}] 로 모았다가 줄로
    fill = (lambda key, value, where: {"key": key, "value": value}) if text else \
        (lambda key, value, where: FQ.fill_answer(tpl, empty, key, value, where))
    lines, ans, types = [], [], {}
    for f in mf:
        line = lambda extra: prompts.kie_line(doc.r["doc_id"], f["key"], f.get("label"), f.get("doc_key"), extra, all_mf,  # noqa: E731
                                              note=f.get("_note"), line=form_line)
        if f["type"] in ("checkbox", "checkbox_multi"):
            kind = "체크박스" if f["type"] == "checkbox" else "복수 선택"
            lines.append(line(f"{kind}, 보기: {' / '.join(o['text'] for o in f['options'])}"))
            on = [o for o in f["options"] if o["checked"]]
            ans += [fill(f["key"], o["text"], doc.where(f, o.get("box_bbox"))) for o in on] or [fill(f["key"], None, {})]
        else:
            lines.append(line("도장" if f["type"] == "seal" else "서명"))
            ans.append(fill(f["key"], bool(f["present"]), doc.where(f, f.get("bbox")) if f["present"] else {}))
        types[f["key"]] = f["type"]
    ev = {"types": types}
    if text:
        labels = {f["key"]: f.get("label") or "-" for f in mf}
        ev |= {"text": {"answer": tpl, "answer_empty": empty, "labels": labels}, "gold": ans}
        ans = "\n".join(FQ.fill_text(tpl, empty, a["key"], labels[a["key"]], a["value"]) for a in ans)
        return [{"id": f"marks/{doc.sid}", "task": TASK, "prompt": FQ.prompt(doc.q, TASK, "\n".join(lines)),
                 "answer": ans, "eval": ev, **doc.base}]
    names = FQ.answer_fields(tpl)
    if names != {p: p for p in FQ.PLACES}:   # 답 틀의 칸 이름이 기본과 다르면 채점이 거꾸로 읽게 적어 둔다
        ev["answer_fields"] = names
    return [{"id": f"marks/{doc.sid}", "task": TASK, "prompt": FQ.prompt(doc.q, TASK, "\n".join(lines)),
             "answer": ans, "eval": ev, **doc.base}]
