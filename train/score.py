"""평가 채점·GRPO 골라 뽑기 (옛 bank_task/score.py + bank_ocr evaluate·mine): 모든 과제가 docgen.bench.evaluate."""
import hashlib
import json
import random

from docgen.bench import evaluate as E


def items_digest(items):
    h = hashlib.sha256()
    for it in sorted(items, key=lambda x: x["id"]):
        h.update(json.dumps(it, ensure_ascii=False, sort_keys=True).encode())
    return h.hexdigest()


def score(items, predictions, _split_benchmarks=True):
    """과제별 결과 (docgen score_task, 문항별 줄은 뺌). 과제 순서는 evaluate.TASK_ORDER."""
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

    result = {"items_sha256": items_digest(items), "n": len(items), "tasks": tasks, **evaluate_groups(items, predictions, tasks)}
    if _split_benchmarks and any((it.get("meta") or {}).get("benchmark_id") for it in items):
        buckets = {}
        for it in items:
            ident = (it.get("meta") or {}).get("benchmark_id")
            if not ident:
                raise ValueError("이름 있는 벤치마크와 식별자 없는 문항이 섞였습니다")
            buckets.setdefault(ident, []).append(it)
        result["benchmarks"] = {}
        for ident, rows in buckets.items():
            names = {(it["meta"].get("benchmark_name", ident), it["meta"].get("benchmark_group", "ungrouped")) for it in rows}
            if len(names) != 1:
                raise ValueError(f"benchmark {ident}: name/group 설정이 일치하지 않습니다")
            name, group = names.pop()
            details = score(rows, predictions, _split_benchmarks=False)
            result["benchmarks"][ident] = {"id": ident, "name": name, "group": group,
                                           "paths": sorted({it["meta"]["benchmark_path"] for it in rows if it["meta"].get("benchmark_path")}), **details}
    return result


def mine(rows, predictions, count, seed, hard_fraction, hard_threshold=0.9):
    """GRPO 문항 고르기: hard_fraction 만큼은 SFT 모델 보상이 hard_threshold 아래인 것(나아질 여지), 나머지는 무작위.
    문항은 정답을 bench_item(JSON)으로 갖고, 보상은 GRPO 와 같은 함수."""
    if any(r.get("split") != "train" for r in rows):
        raise ValueError("GRPO rows must all be train rows")
    if count < 1 or not 0 <= hard_fraction <= 1 or not 0 < hard_threshold <= 1:
        raise ValueError("Invalid count/hard_fraction/hard_threshold")
    missing = [r["id"] for r in rows if r["id"] not in predictions]
    if missing:
        raise ValueError(f"{len(missing)} candidate rows have no prediction, e.g. {missing[0]}")
    hard, easy = [], []
    for r in rows:
        (hard if E.reward(r["task"], predictions[r["id"]], json.loads(r["bench_item"])) < hard_threshold else easy).append(r)
    rng = random.Random(seed)
    rng.shuffle(hard)
    rng.shuffle(easy)
    chosen = hard[:round(count * hard_fraction)]
    rest = hard[len(chosen):] + easy
    rng.shuffle(rest)
    chosen += rest[:max(0, count - len(chosen))]
    rng.shuffle(chosen)
    hard_ids = {r["id"] for r in hard}
    by_task = {}
    for r in chosen:
        by_task[r["task"]] = by_task.get(r["task"], 0) + 1
    return chosen, {"selected": len(chosen), "hard_available": len(hard),
                    "hard_selected": sum(r["id"] in hard_ids for r in chosen), "by_task": by_task,
                    "hard_threshold": hard_threshold}
