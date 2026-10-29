"""table_find — 표 찾기. 서류에 있는 표(반복 묶음)를 모두: 머리글, 위치, 쪽, 행 수. 여러 쪽에 걸친 표는 쪽마다 한 줄.

표의 정의는 table.py 와 같다 (항목명·값이 번갈아 있는 칸, 정해진 격자는 표가 아님 — 질문에도 적음).
표가 없는 서류도 일부(NEGATIVE_RATE) 묻는다 (정답 []) — 무엇이 표가 아닌지도 배우게.
정답: [{"columns": [머리글], "bbox_2d", "page", "n_rows"}] (쪽, 위 순서). 머리글은 열의 항목명, 위치는 머리글 칸과 그 쪽 행 칸을 감싼 상자.
채점: evaluate.s_table_find — 같은 쪽·IoU 0.5 이상으로 짝지은 F1 (주 지표 f1_iou50), 표 수 일치, 찾은 표의 행 수 일치, 머리글 F1
"""
from .. import prompts
from . import BOX
from .table import columns, row_page, table_box

TASK = "table_find"
NAME = "표 찾기"
PROMPT = prompts.P_TABLE_FIND
ANSWER = {"type": "array", "items": {"type": "object", "required": ["bbox_2d", "page", "n_rows"], "properties": {
    "columns": {"type": "array", "items": {"type": "string"}}, "bbox_2d": BOX, "page": {"type": "integer", "minimum": 1},
    "n_rows": {"type": "integer", "minimum": 0}}}}
EXAMPLE = [{"columns": ["가입자구분", "사업장명칭", "자격취득일", "자격상실일"], "bbox_2d": [40, 520, 960, 900], "page": 1, "n_rows": 14}]
NOTES = "표마다(여러 쪽이면 쪽마다) 머리글·위치·쪽·행 수. 행 수에 머리글·합계 행과 빈 행은 넣지 않습니다. 표가 없으면 []."
NEGATIVE_RATE = 0.15   # 표가 없는 서류에도 묻는 비율


def make(doc):
    segs = []
    for t in doc.tables.values():
        labels = [f.get("label") for _, f in columns(doc, t) if f.get("label")]
        pages = sorted({row_page(r) for r in t["rows"]})
        for p in pages:
            rows = [r for r in t["rows"] if row_page(r) == p]
            box = table_box(doc, t, rows)
            if not box:
                return []   # 위치를 모르는 표가 있으면 묻지 않는다
            segs.append({"columns": labels, "bbox_2d": box[0], "page": box[1], "n_rows": len(rows)})
    if not segs and doc.rng.random() >= NEGATIVE_RATE:
        return []
    segs.sort(key=lambda s: (s["page"], s["bbox_2d"][1]))
    return [{"id": f"table_find/{doc.sid}", "task": TASK, "prompt": prompts.P_TABLE_FIND, "answer": segs, **doc.base,
             "meta": {**doc.meta, "n_tables": len(doc.tables), "n_segments": len(segs)}}]
