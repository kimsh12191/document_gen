"""평가 세트 하나 채점: 과제별 점수 + 구분별(서식·원본 데이터셋 …) 점수. 채점은 모두 docgen.bench.evaluate (studio 와 같은 함수)."""
import hashlib
import json

from docgen.bench import evaluate as E


def items_digest(items):
    h = hashlib.sha256()
    for it in sorted(items, key=lambda x: x["id"]):
        h.update(json.dumps(it, ensure_ascii=False, sort_keys=True).encode())
    return h.hexdigest()


def score(items, predictions):
    """{"items_sha256", "n", "tasks": {과제: {"main", "metrics", "n", "missing", "parse_fail", "slices"}}, "composition", "breakdowns"}.
    과제 순서는 evaluate.TASK_ORDER. 답이 없거나 못 읽은 답은 0점."""
    by_task = {}
    for it in items:
        by_task.setdefault(it["task"], []).append(it)
    tasks = {}
    for task in [*E.TASK_ORDER, *sorted(set(by_task) - set(E.TASK_ORDER))]:
        if task in by_task:
            res = E.score_task(task, by_task[task], predictions)
            res.pop("per_item", None)
            tasks[task] = res
    from docgen.bench.tracking import evaluate_groups

    return {"items_sha256": items_digest(items), "n": len(items), "tasks": tasks, **evaluate_groups(items, predictions, tasks)}
