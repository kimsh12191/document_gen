"""table_read — 표 그대로 옮기기 (표 인식). 머리글까지, 열을 정해 주지 않는다.

정답은 그릴 때 브라우저에서 읽은 <table> 구조 (docgen/image.py _JS_TABLES, r["tables"]) — html 서식만 (overlay 서식은 표 구조가 없음).
묻는 표: 값 칸이 한 표(반복 묶음, Doc.tables)의 칸뿐인 <table> 하나 (그 밖의 칸이 섞인 표·겹친 표는 묻지 않는다),
         맨 위에 머리글 줄(값 칸이 없는 줄)이 있어야 한다. 쪽 나눔으로 나뉜 표는 쪽마다 따로 (위치로 가리킨다).
정답 꼴: {"columns": [머리글], "rows": [[칸 글자]], "row_boxes"} — 머리글 줄이 여럿이면 위·아래 글자를 " > " 로,
         여러 행에 걸친 칸(rowspan)은 행마다 같은 글자, 여러 열에 걸친 칸(colspan)은 첫 열에만, 빈 칸 null, 모두 빈 행은 뺌.
         합계·소계 행은 그대로 둔다 (table 과제와 다름). 행이 MAX_ROWS 를 넘으면 앞에서부터 그만큼.
채점: evaluate.s_table_read — 머리글을 글자로 짝지은 뒤 table 과 같은 칸 F1 (주 지표), 머리글 F1
"""
from .. import prompts
from ..metrics import normalize_box
from . import table_cell
from .table import BOX, MAX_ROWS, choose_target, columns

TASK = "table_read"
NAME = "표 그대로 옮기기"
PROMPT = prompts.P_TABLE_READ
ANSWER = {"type": "object", "required": ["columns", "rows"], "properties": {
    "columns": {"type": "array", "items": {"type": "string"}},
    "rows": {"type": "array", "items": {"type": "array", "items": {"type": ["string", "null"]}}},
    "row_boxes": {"type": "array", "items": {"type": "object", "properties": {"bbox_2d": BOX, "page": {"type": "integer", "minimum": 1}}}}}}
EXAMPLE = {"columns": ["NO", "가입자구분", "사업장명칭", "자격취득일", "자격상실일"],
           "rows": [["1", "지역세대원", None, "2022-07-30", None]], "row_boxes": [{"bbox_2d": [40, 600, 960, 640], "page": 1}]}
NOTES = "머리글을 그대로 columns 로, 칸 글자를 그대로 rows 로. 여러 줄 머리글은 ' > ' 로 잇고, 합계 행은 그대로 둡니다."


def grid(rows: list[dict]) -> list[list[dict | None]]:
    """rowspan·colspan 을 펼친 격자: 칸마다 {"cell", "origin": 처음 칸인지, "first_col": 걸친 열의 첫 열인지}."""
    g: list[list] = []
    for i, row in enumerate(rows):
        while len(g) <= i:
            g.append([])
        col = 0
        for c in row["cells"]:
            while col < len(g[i]) and g[i][col] is not None:
                col += 1
            for di in range(c["rs"]):
                while len(g) <= i + di:
                    g.append([])
                line = g[i + di]
                while len(line) < col + c["cs"]:
                    line.append(None)
                for dj in range(c["cs"]):
                    line[col + dj] = {"cell": c, "origin": di == 0, "first_col": dj == 0, "span_row": di > 0}
            col += c["cs"]
    width = max((len(r) for r in g), default=0)
    return [r + [None] * (width - len(r)) for r in g]


def transcribe(t: dict, groups: set[str]) -> dict | None:
    """DOM 표 하나 → {"group", "columns", "rows": [[글자]], "boxes": [[픽셀 상자]]} 또는 None (물을 수 없는 표)."""
    keys = [k for r in t["rows"] for c in r["cells"] for k in c["keys"]]
    cells = [table_cell(k) for k in keys]
    if not keys or any(tc is None or tc[1] < 0 for tc in cells):
        return None   # 표 칸이 아닌 값이 섞인 표
    owners = {tc[0] for tc in cells}
    if len(owners) != 1 or not owners <= groups:
        return None
    first = next(i for i, r in enumerate(t["rows"]) if any(c["keys"] for c in r["cells"]))
    if first == 0:
        return None   # 머리글 줄이 없음
    g = grid(t["rows"])
    width = len(g[0]) if g else 0
    if not width:
        return None
    heads = []
    for j in range(width):
        parts = []
        for i in range(first):
            e = g[i][j]
            text = e and e["cell"]["text"]
            if text and (not parts or parts[-1] != text):
                parts.append(text)
        heads.append(" > ".join(parts) or None)
    if not any(heads):
        return None
    rows, boxes = [], []
    for i in range(first, len(g)):
        vals, bs = [], []
        for e in g[i]:
            if e is None or not e["first_col"]:
                vals.append(None)
                continue
            vals.append(e["cell"]["text"] or None)   # rowspan 은 아래 행에도 같은 글자
            if e["origin"] and e["cell"]["bbox"]:
                bs.append(e["cell"]["bbox"])
        if all(v is None for v in vals):
            continue
        rows.append(vals)
        boxes.append([min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)] if bs else None)
    if not rows:
        return None
    return {"group": owners.pop(), "columns": [h or "" for h in heads], "rows": rows, "boxes": boxes, "page": t["page"]}


def make(doc):
    groups = set(doc.tables)
    found = [x for x in (transcribe(t, groups) for t in doc.r.get("tables") or []) if x]
    segments = {}
    for x in found:
        segments.setdefault(x["group"], []).append(x)
    out = []
    for group, segs in segments.items():
        t = doc.tables[group]
        for n, x in enumerate(segs):
            size = doc.r["sizes"][x["page"]] if x["page"] < len(doc.r["sizes"]) else None
            if not size:
                continue
            rows, boxes = x["rows"], x["boxes"]
            scope_text, scope = "", "all"
            if len(rows) > MAX_ROWS:
                rows, boxes, scope = rows[:MAX_ROWS], boxes[:MAX_ROWS], "first"
                scope_text = prompts.table_scope(first=MAX_ROWS)
            if len(segs) > 1:   # 쪽마다 나뉜 표: 그 쪽 표를 위치로
                bs = [b for b in boxes if b]
                if not bs:
                    continue
                u = [min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)]
                how, target = "box", prompts.table_target("box", box=normalize_box(u, *size), page=x["page"] + 1)
            else:
                how, target = choose_target(doc, t, columns(doc, t), t["rows"])
            answer = {"columns": x["columns"], "rows": rows,
                      "row_boxes": [{"bbox_2d": normalize_box(b, *size), "page": x["page"] + 1} if b else {} for b in boxes]}
            out.append({"id": f"table_read/{doc.sid}/{group}/{n}", "task": TASK,
                        "prompt": prompts.P_TABLE_READ.format(target=target, scope=scope_text), "answer": answer, **doc.base,
                        "meta": {**doc.meta, "table": group, "ref": how, "scope": scope, "n_rows": len(rows),
                                 "n_cols": len(x["columns"]), "segments": len(segs)}})
    return out
