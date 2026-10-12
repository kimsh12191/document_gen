"""Scores, GRPO reward and hard-case mining, all with docgen's benchmark scorers.

The scorers live in the docgen code (docgen/bench/evaluate.py, standard library only), so the
reward used in GRPO is exactly the benchmark's grading. The docgen folder is found through
DOCGEN_ROOT (set by run_bank_pipeline.py from the pipeline config) or PYTHONPATH.
"""
import hashlib
import json
import os
import random
import sys
from pathlib import Path


def docgen(module="evaluate"):
    """Import docgen.bench.<module> (evaluate or runner)."""
    root = os.environ.get("DOCGEN_ROOT")
    if root and str(Path(root).resolve()) not in sys.path:
        sys.path.insert(0, str(Path(root).resolve()))
    try:
        if module == "runner":
            from docgen.bench import runner as mod
        else:
            from docgen.bench import evaluate as mod
    except ImportError as exc:
        raise ImportError("docgen code not found: set data.docgen_root in the pipeline config "
                          "(the folder that contains docgen/) or DOCGEN_ROOT") from exc
    return mod


def reward(output, item):
    """GRPO reward in [0, 1] for one benchmark-format item; 0 for no answer or unparseable output.

    Same scorers as the benchmark, smoothed where the benchmark metric is all-or-nothing over
    several parts so a partly right answer beats a wrong one:
      doc_check    0.5 x exact + 0.5 x F1 over the three lists
      cross_check  consistent item: 1 if it says consistent
                   tampered item:   0.5 x (says inconsistent) + 0.5 x (also points at the right document and value)
      ocr_field    1 - CER
      ocr_page     value recall with 20% character tolerance
      others       the benchmark's main metric (kie F1, marks / classify / review accuracy)
    """
    if output is None:
        return 0.0
    E = docgen()
    task = item["task"]
    result = E.SCORERS[task](item, output)
    if result.get("parse_fail"):
        return 0.0
    m = result["metrics"]
    if task == "doc_check":
        value = 0.5 * m["exact"] + 0.5 * m["set_f1"]
    elif task == "cross_check":
        value = m["score"] if item["answer"]["consistent"] else 0.5 * m["detect"] + 0.5 * m["score"]
    elif task == "ocr_field":
        value = 1.0 - m["cer"]
    elif task == "ocr_page":
        value = m.get("recall_fuzzy", m["recall"])
    else:
        value = m[E.MAIN[task]]
    return float(min(1.0, max(0.0, value)))


def oracle(item):
    """The reference answer written as model output (what SFT teaches)."""
    return docgen("runner").oracle_output(item)


def items_digest(items):
    h = hashlib.sha256()
    for it in sorted(items, key=lambda x: x["id"]):
        h.update(json.dumps(it, ensure_ascii=False, sort_keys=True).encode())
    return h.hexdigest()


def score(items, predictions):
    """Benchmark result per task (docgen score_task, without the per-item rows)."""
    E = docgen()
    by_task = {}
    for it in items:
        by_task.setdefault(it["task"], []).append(it)
    tasks = {}
    for task in E.TASK_ORDER:
        if task in by_task:
            res = E.score_task(task, by_task[task], predictions)
            res.pop("per_item", None)
            tasks[task] = res
    return {"items_sha256": items_digest(items), "n": len(items), "tasks": tasks}


def mine(rows, predictions, count, seed, hard_fraction, hard_threshold=0.9):
    """Pick GRPO rows: `hard_fraction` of them where the SFT model's reward is below the threshold
    (room to improve), the rest at random. Rows carry the benchmark item as JSON in `bench_item`."""
    if any(r.get("split") != "train" for r in rows):
        raise ValueError("GRPO rows must all be train rows")
    if count < 1 or not 0 <= hard_fraction <= 1:
        raise ValueError("Invalid count/hard_fraction")
    missing = [r["id"] for r in rows if r["id"] not in predictions]
    if missing:
        raise ValueError(f"{len(missing)} candidate rows have no prediction, e.g. {missing[0]}")
    hard, easy = [], []
    for r in rows:
        (hard if reward(predictions[r["id"]], json.loads(r["bench_item"])) < hard_threshold else easy).append(r)
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
                    "hard_selected": sum(r["id"] in hard_ids for r in chosen), "by_task": by_task}
