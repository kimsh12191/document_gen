"""생성 구성·Studio 필터·학습 평가에서 공통으로 사용하는 분류 기준.

서로 다른 과제의 지표를 하나의 점수로 평균내지 않는다. 각 구분 안에서도 과제별로 채점한다.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json

GROUPS = {**{t: "ocr" for t in ("crop_ocr", "bbox_ocr", "region_ocr", "marked_ocr", "grounding", "spotting", "relation", "marked_box", "ocr_field", "ocr_page")},
          "classify": "doc", "kie": "doc", "marks": "doc", "doc_check": "work", "cross_check": "work", "review": "work"}
FORMATS = {**{t: "text" for t in ("crop_ocr", "bbox_ocr", "region_ocr", "marked_ocr", "ocr_field", "classify")},
           **{t: "text_boxes" for t in ("grounding", "spotting", "relation", "marked_box")},
           "ocr_page": "text_list", "kie": "key_values", "marks": "mark_states",
           "doc_check": "document_sets", "cross_check": "consistency_issues", "review": "scalar"}
DIMENSIONS = {"task_group": "업무·과제 그룹", "task": "과제", "scenario": "업무 시나리오",
              "label_format": "정답 구조", "doc_type": "서식", "source_dataset": "원본 데이터셋"}
SCORE_DIMENSIONS = ("task_group", "scenario", "label_format", "doc_type", "source_dataset")
PROVENANCE_KEYS = ("doc_type", "scenario", "scenario_name", "condition", "template_variant", "source_dataset")


def facets(item: dict) -> dict[str, str]:
    task, meta = item["task"], item.get("meta") or {}
    group = GROUPS.get(task, "unknown")
    return {"task_group": group, "task": task,
            "scenario": str(meta.get("scenario") or ("unknown" if group == "work" else "not_applicable")),
            "label_format": str(meta.get("label_format") or FORMATS.get(task, "unknown")),
            "doc_type": str(meta.get("doc_type") or "unknown"),
            "source_dataset": str(meta.get("source_dataset") or "unknown")}


def enrich(item: dict, source_dataset: str | None = None) -> dict:
    """기존 문항도 읽을 때 분류한다. 파일을 수정하지 않고 meta를 보완한다."""
    meta = dict(item.get("meta") or {})
    f = facets(item)
    meta.update(task_group=f["task_group"], label_format=f["label_format"])
    if source_dataset is not None and not meta.get("source_dataset"):
        meta["source_dataset"] = source_dataset
    return {**item, "meta": meta}


def source_id(name: str, metadata: dict) -> str:
    digest = hashlib.sha256(json.dumps(metadata, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]
    return f"{name}@{digest}"


class Composition:
    def __init__(self):
        self.n = 0
        self.by = {key: Counter() for key in DIMENSIONS}
        self.cells = Counter()
        self.fields = Counter()

    def add(self, item: dict):
        f = facets(item)
        self.n += 1
        for key, value in f.items():
            self.by[key][value] += 1
        self.cells[(f["task_group"], f["scenario"], f["task"], f["label_format"])] += 1
        ev = item.get("eval") or {}
        fields = ev.get("fields") or {}
        kinds = [v.get("kind") or v.get("type") or "unknown" for v in fields.values()]
        kinds += list((ev.get("types") or {}).values())
        if not kinds and (item.get("meta") or {}).get("kind"):
            kinds = [item["meta"]["kind"]]
        self.fields.update(str(k) for k in kinds)

    def result(self) -> dict:
        return {"version": 1, "n": self.n,
                "by": {key: dict(sorted(c.items())) for key, c in self.by.items()},
                "rows": [dict(zip(("task_group", "scenario", "task", "label_format"), key), n=n)
                         for key, n in sorted(self.cells.items())],
                "field_kind_counts": dict(sorted(self.fields.items())),
                "notes": "by·rows의 n은 문항 수. field_kind_counts는 eval에 정의된 필드 수. unknown은 이전 데이터의 누락 정보이며 시나리오를 추측하지 않습니다."}


def composition(items) -> dict:
    out = Composition()
    for item in items:
        out.add(item)
    return out.result()


def evaluate_groups(items: list[dict], predictions: dict, full_tasks: dict | None = None) -> dict:
    from . import evaluate as E

    buckets = {key: defaultdict(lambda: defaultdict(list)) for key in SCORE_DIMENSIONS}
    for item in items:
        item_facets = facets(item)
        for key, groups in buckets.items():
            groups[item_facets[key]][item["task"]].append(item)
    result = {}
    for key, groups in buckets.items():
        result[key] = {}
        for value, tasks in sorted(groups.items()):
            scored = {}
            for task, rows in sorted(tasks.items()):
                if task not in E.MAIN:
                    continue
                full = (full_tasks or {}).get(task)
                base = full if full and full["n"] == len(rows) else E.score_task(task, rows, predictions)
                res = {k: v for k, v in base.items() if k not in ("per_item", "slices")}
                res["membership_sha256"] = hashlib.sha256(json.dumps(sorted(r["id"] for r in rows)).encode()).hexdigest()
                scored[task] = res
            result[key][value] = {"n": sum(len(rs) for rs in tasks.values()), "tasks": scored}
    return {"composition": composition(items), "breakdowns": result}
