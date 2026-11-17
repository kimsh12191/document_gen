"""평가 세트 하나 채점: 과제별 점수 + 구분별(서식·원본 데이터셋 …) 점수. 채점은 모두 docgen.bench.evaluate (studio 와 같은 함수)."""
import hashlib
import json

from docgen.bench import evaluate as E


def items_digest(items):
    h = hashlib.sha256()
    for it in sorted(items, key=lambda x: x["id"]):
        h.update(json.dumps(it, ensure_ascii=False, sort_keys=True).encode())
    return h.hexdigest()


LOC = "loc_f1"


def headline(task: str, t: dict) -> list[str]:
    """보고서·답 비교에서 앞에 내는 지표. 위치까지 답하는 과제(kie·marks: 주 지표가 값+위치 vl_f1)는 값과 위치를 따로
    (값을 맞게 읽었나 / 박스를 맞게 짚었나), 그 밖은 주 지표 하나. 값+위치(vl_f1)는 세트별 자세히에 그대로 있다."""
    ms = t.get("metrics") or {}
    value = E.MAIN_V1.get(task)
    if t.get("main") == "vl_f1" and value in ms and LOC in ms:
        return [value, LOC]
    return [t["main"]]


def metric_label(task: str, metric: str, t: dict) -> str:
    """지표 이름 앞에 무엇을 재는지: 값 · f1 / 위치 · loc_f1 (주 지표 하나면 이름 그대로)."""
    if len(headline(task, t)) < 2:
        return metric
    return ("위치 · " if metric == LOC else "값 · ") + metric


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
