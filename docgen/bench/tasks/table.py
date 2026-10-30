"""table — 표 추출 (열을 정해 모든 행). 서류의 표(반복 묶음)마다 문항 하나: 열(키: 항목명)을 주고, 행 수는 모델이 정한다.

표의 정의 (guide/benchmark.md "표의 정의"): 항목 묶음(열 구성)은 서식이 정하고 그 묶음이 몇 번 나오는지가 서류마다 다른 것.
키에 행 번호가 들어간 칸(rows.0.kind)이 표 칸이다 (Doc.tables). 개수가 정해진 격자는 서식 questions.json 의
{"table": {"<묶음>": {"ask": false}}} 로 kie 에 남긴다. 표 제목은 {"title": "…"} (없으면 머리글·위치로 가리킨다).

질문: P_TABLE (target 표를 가리키는 말 — 제목 / 머리글 두어 개 / 위치 / 표가 하나뿐이면 "표", scope 범위, columns 열 줄)
      넣은 이미지에 보이는 행은 늘 전부 묻는다 (4.2 부터. 행을 잘라 묻으면 정답이 보이는 표와 어긋난다).
      한 쪽만 묻는 것은 그 쪽 이미지만 넣는 view "page" 문항 (tasks/__init__.py make_single).
      일부 문항(ABSENT_RATE)에는 이 표에 없는 열을 하나 섞는다 (같은 그룹 다른 서식의 열, 정답은 그 열 전부 null).
정답: {"columns": [열 키], "rows": [[값 또는 null]], "row_boxes": [{"bbox_2d", "page"}]} — 행은 보이는 순서 (쪽, 위),
      모두 빈 행은 뺌, 칸 안의 줄바꿈은 공백 하나. 값·위치는 그릴 때 기록한 것 그대로.
eval.fields: 열마다 타입·norm·값 종류 (kie 와 같은 비교). eval.absent: 섞은 없는 열.
채점: evaluate.s_table — 행을 순서대로 짝지은 뒤 칸 F1 (주 지표), 행 완전 일치, 행 수 일치, 행 위치 F1
"""
import re

from ... import formquestions as FQ
from .. import prompts
from ..metrics import normalize_box
from . import BOX, field_kind

TASK = "table"
NAME = "표 추출"
PROMPT = prompts.P_TABLE
ANSWER = {"type": "object", "required": ["columns", "rows"], "properties": {
    "columns": {"type": "array", "items": {"type": "string"}},
    "rows": {"type": "array", "items": {"type": "array", "items": {"type": ["string", "number", "null"]}}},
    "row_boxes": {"type": "array", "items": {"type": "object", "properties": {"bbox_2d": BOX, "page": {"type": "integer", "minimum": 1}}}}}}
EXAMPLE = {"columns": ["kind", "workplace", "start", "end"],
           "rows": [["지역세대원", None, "2022-07-30", None], ["직장가입자", "변호사유지은법률사무소", "2015-03-13", "2022-07-30"]],
           "row_boxes": [{"bbox_2d": [40, 600, 960, 640], "page": 1}, {"bbox_2d": [40, 640, 960, 700], "page": 1}]}
NOTES = ("행 수는 모델이 정합니다. columns 는 질문의 열 키 그대로, rows 는 행마다 같은 순서의 값(빈 칸·없는 열은 null), "
         "row_boxes 는 행마다 상자 하나입니다. 합계·소계 행, 다시 나온 머리글 행, 모두 빈 행은 뺍니다.")
ABSENT_RATE = 0.3    # 없는 열을 하나 섞는 문항 비율 (docgen/bench/absent.py 의 열 후보가 있을 때)


def flat(v):
    """칸 값 → 정답 값: 줄바꿈은 공백 하나 (질문의 규칙)."""
    return None if v is None else re.sub(r"\s*\n\s*", " ", str(v)).strip() or None


def row_page(cells: dict) -> int:
    boxed = [c for c in cells.values() if c.get("bbox")]
    return min(c.get("page", 0) for c in boxed) if boxed else 0


def row_box(doc, cells: dict) -> dict:
    """행을 감싸는 상자 (행의 첫 쪽 칸들만): {"bbox_2d", "page"} 또는 {}."""
    pg = row_page(cells)
    bs = [c["bbox"] for c in cells.values() if c.get("bbox") and c.get("page", 0) == pg]
    if not bs or pg >= len(doc.r["sizes"]):
        return {}
    u = [min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)]
    return {"bbox_2d": normalize_box(u, *doc.r["sizes"][pg]), "page": pg + 1}


def table_box(doc, t: dict, rows: list[dict]) -> tuple[list[int], int] | None:
    """표 위치 (첫 쪽): 머리글 칸(label_bbox)과 그 쪽 행 칸들을 감싸는 상자, 쪽(1부터)."""
    pages = [row_page(r) for r in rows]
    if not pages:
        return None
    pg = min(pages)
    bs = [c["bbox"] for r in rows for c in r.values() if c.get("bbox") and c.get("page", 0) == pg]
    bs += [c["label_bbox"] for r in rows for c in r.values() if c.get("label_bbox") and c.get("page", 0) == pg]
    if not bs or pg >= len(doc.r["sizes"]):
        return None
    u = [min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)]
    return normalize_box(u, *doc.r["sizes"][pg]), pg + 1


def columns(doc, t: dict) -> list[tuple[str, dict]]:
    """열 (열 키, 대표 칸): 칸 목록 fields.json 의 q (묻지 않기·항목명) 를 따른다."""
    reps = [{**f, "_col": col} for col, f in t["columns"]]
    for f in reps:   # 항목명이 빈 첫 칸이면 그 열의 다른 칸 항목명
        if not f.get("label"):
            f["label"] = next((r[f["_col"]].get("label") for r in t["rows"] if f["_col"] in r and r[f["_col"]].get("label")), None)
    return [(f["_col"], f) for f in FQ.pick(doc.q, "kie", reps, doc.fq)]


def choose_target(doc, t: dict, cols: list[tuple[str, dict]], rows: list[dict]) -> tuple[str, str]:
    """(가리키는 방법, 가리키는 말). 제목 있으면 제목도, 표가 하나뿐이면 "표" 도 후보."""
    ways = []
    if t.get("title"):
        ways.append("title")
    labels = list(dict.fromkeys(f["label"] for _, f in cols if f.get("label")))
    if labels:
        ways.append("header")
    box = table_box(doc, t, rows)
    if box:
        ways.append("box")
    if len(doc.tables) == 1:
        ways.append("only")
    how = doc.rng.choice(ways) if ways else "only"
    if how == "header":
        pick = sorted(doc.rng.sample(range(len(labels)), min(2, len(labels))))
        return how, prompts.table_target("header", labels=[labels[i] for i in pick])
    if how == "box":
        return how, prompts.table_target("box", box=box[0], page=box[1])
    return how, prompts.table_target(how, title=t.get("title"))


def choose_scope(doc, rows: list[dict]) -> tuple[str, list[dict], str]:
    """(범위 이름, 묻는 행, 범위 말). 4.2 부터 늘 모든 행 — 4.1 까지는 30행 넘는 표·여러 쪽 표 일부를 "N쪽에 있는 행만"·
    "앞에서부터 30행까지만" 으로 잘라 물었다. 범위 말(prompts.table_scope)은 예전 세트를 읽을 때를 위해 남긴다."""
    return "all", rows, ""


def make(doc):
    from ..absent import absent_column

    out = []
    for group, t in doc.tables.items():
        cols = columns(doc, t)
        if not cols:
            continue
        how, target = choose_target(doc, t, cols, t["rows"])
        scope, rows, scope_text = choose_scope(doc, t["rows"])
        info = {col: {"type": f["type"], "norm": None, "kind": field_kind(f), "label": f.get("label")} for col, f in cols}
        absent = absent_column(doc, group, cols) if doc.rng.random() < ABSENT_RATE else None
        lines = [prompts.column_line(col, f.get("label"), f.get("_note")) for col, f in cols]
        keys = [col for col, _ in cols]
        if absent:   # 없는 열: 아무 자리에나 끼운다 (정답은 그 열 전부 null)
            at = doc.rng.randrange(len(keys) + 1)
            keys.insert(at, absent["key"])
            lines.insert(at, prompts.column_line(absent["key"], absent["label"]))
            info[absent["key"]] = {"type": absent["type"], "norm": None, "kind": "absent", "label": absent["label"]}
        answer = {"columns": keys,
                  "rows": [[flat(r[k]["value"]) if k in r else None for k in keys] for r in rows],
                  "row_boxes": [row_box(doc, r) for r in rows]}
        ev = {"fields": info, "group": group, **({"absent": [absent["key"]]} if absent else {})}
        out.append({"id": f"table/{doc.sid}/{group}", "task": TASK,
                    "prompt": prompts.P_TABLE.format(target=target, scope=scope_text, columns="\n".join(lines)),
                    "answer": answer, "eval": ev, **doc.base,
                    "meta": {**doc.meta, "table": group, "ref": how, "scope": scope, "n_rows": len(rows), "n_cols": len(keys),
                             "absent": bool(absent)}})
    return out
