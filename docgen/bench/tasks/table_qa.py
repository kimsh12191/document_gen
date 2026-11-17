"""table_qa — 표에 대해 묻기. 표(반복 묶음)마다 질문 둘 (종류는 무작위): 행 수, 조건에 맞는 행 수, 찾기, 몇 번째 행, 마지막 행, 합계.

질문: P_TABLE_QA (target 표를 가리키는 말 — table.py 와 같은 방법, question 아래 KINDS 의 문장)
정답: 숫자(행 수·합계) 또는 칸 값 (문서에 적힌 그대로, 빈 칸이면 null)
eval: {"answer_type": "number" | "value", "type": 열 타입, "key": 열 키}
채점: evaluate.s_table_qa — 숫자는 같은 수, 값은 kie 와 같은 비교 (빈 칸이면 답도 비어야). 주 지표 acc, 종류(meta.kind)별로도
"""
from .. import prompts
from ..metrics import to_number
from .table import choose_target, columns, flat

TASK = "table_qa"
NAME = "표 질의"
PROMPT = prompts.P_TABLE_QA
ANSWER = {"anyOf": [{"type": "number"}, {"type": "string"}, {"type": "null"}]}
EXAMPLE = 14
NOTES = "숫자를 묻는 질문은 숫자만, 칸 값을 묻는 질문은 문서에 적힌 그대로 (비어 있으면 null) 답합니다."
PER_TABLE = 2
NUM = " (숫자만 답하세요)"
VAL = " (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)"
NUM_TYPES = ("amount", "amount_korean", "number", "percent")


def _questions(doc, cols, rows):
    """이 표로 만들 수 있는 질문 [(종류, 질문, 정답, answer_type, 열 키, 열 타입)]."""
    out = [("count", "표의 행은 모두 몇 개입니까? 머리글·합계 행과 모두 빈 행은 세지 않습니다." + NUM, len(rows), "number", None, None)]
    vals = {c: [flat(r[c]["value"]) if c in r else None for r in rows] for c, _ in cols}
    for c, f in cols:
        lab, v = f.get("label") or c, vals[c]
        filled = [x for x in v if x is not None]
        distinct = sorted(set(filled))
        if 1 < len(distinct) <= 6 and len(filled) >= 3:   # 범주 열: 조건에 맞는 행 수
            pick = doc.rng.choice(distinct)
            out.append(("count_if", f"'{lab}' 칸이 '{pick}'인 행은 몇 개입니까?" + NUM, sum(x == pick for x in v), "number", c, f["type"]))
        if f["type"] in NUM_TYPES and filled and all(to_number(x) is not None for x in filled):   # 합계
            s = sum(to_number(x) for x in filled)
            out.append(("sum", f"'{lab}' 칸의 값을 모두 더하면 얼마입니까? 빈 칸은 0 으로 봅니다. (쉼표·단위 없이 숫자만 답하세요)",
                        int(s) if float(s).is_integer() else round(s, 6), "number", c, f["type"]))
    keys = [c for c, _ in cols if len(set(vals[c])) == len(rows) and None not in vals[c]]   # 행마다 다른 값 → 찾기
    for kc in keys[:1]:
        others = [(c, f) for c, f in cols if c != kc]
        if others:
            i = doc.rng.randrange(len(rows))
            c, f = doc.rng.choice(others)
            klab = dict(cols)[kc].get("label") or kc
            out.append(("lookup", f"'{klab}' 칸이 '{vals[kc][i]}'인 행의 '{f.get('label') or c}' 값은 무엇입니까?" + VAL,
                        vals[c][i], "value", c, f["type"]))
    if len(rows) >= 2:
        c, f = doc.rng.choice(cols)
        n = doc.rng.randrange(min(len(rows), 10))
        out.append(("nth", f"위에서 {n + 1}번째 행의 '{f.get('label') or c}' 값은 무엇입니까? 머리글은 세지 않습니다." + VAL,
                    vals[c][n], "value", c, f["type"]))
        c, f = doc.rng.choice(cols)
        out.append(("last", f"마지막 행의 '{f.get('label') or c}' 값은 무엇입니까?" + VAL, vals[c][-1], "value", c, f["type"]))
    return out


def make(doc):
    out = []
    for group, t in doc.tables.items():
        cols = columns(doc, t)
        if not cols:
            continue
        how, target = choose_target(doc, t, cols, t["rows"])
        qs = _questions(doc, cols, t["rows"])
        for n, (kind, question, answer, atype, col, ctype) in enumerate(doc.rng.sample(qs, min(PER_TABLE, len(qs)))):
            out.append({"id": f"table_qa/{doc.sid}/{group}/{n}", "task": TASK,
                        "prompt": prompts.P_TABLE_QA.format(target=target, question=question), "answer": answer,
                        "eval": {"answer_type": atype, "type": ctype, "key": col}, **doc.base,
                        "meta": {**doc.meta, "table": group, "kind": kind, "ref": how, "n_rows": len(t["rows"])}})
    return out
