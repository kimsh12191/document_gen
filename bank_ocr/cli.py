import argparse
import csv
import math
import random
import statistics
from pathlib import Path

from .data import digest, dumps, read_json, read_jsonl, scan, write_json, write_jsonl
from .inference import index_predictions, predict, validate_tasks
from .metrics import REPORT_METRICS, evaluate, reward
from .pipeline import group_turns, prepare
from .settings import load_settings


def mine(tasks, predictions, output, count, seed, hard_fraction, hard_threshold=0.9):
    rows = read_jsonl(tasks)
    validate_tasks(rows)
    if any(r["split"] != "train" for r in rows):
        raise ValueError("Hard-case mining accepts TRAIN only, never validation/benchmark")
    if count < 1 or not 0 <= hard_fraction <= 1 or not 0 < hard_threshold <= 1:
        raise ValueError("Invalid count/hard_fraction/hard_threshold")
    preds = index_predictions(predictions)
    evaluate(rows, preds)  # Require complete ID coverage; missing output isn't a hard case.
    hard, easy = [], []
    for row in rows:
        # Same function as the GRPO reward, so "hard" means "room for reward to improve".
        (hard if reward(preds[row["id"]], row["task"], row["target"]) < hard_threshold else easy).append(row)
    rng = random.Random(seed)
    rng.shuffle(hard)
    rng.shuffle(easy)
    chosen = hard[:round(count * hard_fraction)]
    rest = hard[len(chosen):] + easy
    rng.shuffle(rest)
    chosen += rest[:max(0, count - len(chosen))]
    rng.shuffle(chosen)
    write_jsonl(output, chosen)
    hard_ids = {r["id"] for r in hard}
    return {"selected": len(chosen), "hard_available": len(hard), "hard_selected": sum(r["id"] in hard_ids for r in chosen),
            "hard_threshold": hard_threshold}


def image_tokens(model_dir, max_size):
    """Visual tokens needed for an image of max_size, from the model's vision config."""
    config = read_json(Path(model_dir) / "config.json")
    vision = config.get("vision_config", {})
    patch, merge = vision.get("patch_size"), vision.get("spatial_merge_size")
    if not patch or not merge:
        raise ValueError("config.json has no vision_config.patch_size/spatial_merge_size")
    factor = patch * merge
    return image_tokens_for(max_size, factor), factor


def image_tokens_for(max_size, factor):
    return math.ceil(max(max_size) / factor) * math.ceil(min(max_size) / factor)


def main():
    p = argparse.ArgumentParser(description="Bank OCR pseudo-label SFT/GRPO pipeline")
    commands = p.add_subparsers(dest="command", required=True)
    s = commands.add_parser("scan", help="Create a manifest from page images")
    s.add_argument("--root", required=True)
    s.add_argument("--split", choices=["train", "val", "benchmark"], required=True)
    grouping = s.add_mutually_exclusive_group(required=True)
    grouping.add_argument("--document-regex", help="Regex on relative path with (?P<document_id>...) group")
    grouping.add_argument("--single-page-documents", action="store_true")
    s.add_argument("--ocr-dir", help="Directory of OCR JSON already run on these images (same relative path or file name, .json)")
    s.add_argument("--out", required=True)
    m = commands.add_parser("merge", help="Combine manifests; validate leakage during prepare")
    m.add_argument("inputs", nargs="+")
    m.add_argument("--out", required=True)
    b = commands.add_parser("prepare")
    b.add_argument("--config", required=True)
    r = commands.add_parser("predict")
    r.add_argument("--config", help="Inference JSON config; explicit CLI options override it")
    r.add_argument("--tasks", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--endpoint", help="Model server URL; comma-separate several to spread requests across servers")
    r.add_argument("--model")
    r.add_argument("--run-id", required=True, help="Unique checkpoint identity; change when switching model")
    r.add_argument("--with-ocr", action="store_true")
    r.add_argument("--timeout", type=int)
    r.add_argument("--concurrency", type=int, help="Maximum simultaneous inference requests (default 1)")
    r.add_argument("--max-tokens", type=int)
    r.add_argument("--temperature", type=float)
    r.add_argument("--enable-thinking", action=argparse.BooleanOptionalAction, default=None)
    e = commands.add_parser("evaluate")
    e.add_argument("--tasks", required=True)
    e.add_argument("--predictions", required=True)
    e.add_argument("--out", required=True)
    e.add_argument("--label", required=True)
    c = commands.add_parser("compare", help="Compare reports produced on the same frozen benchmark")
    c.add_argument("reports", nargs="+")
    c.add_argument("--out", required=True, help="CSV output")
    h = commands.add_parser("mine")
    h.add_argument("--tasks", required=True)
    h.add_argument("--predictions", required=True)
    h.add_argument("--out", required=True)
    h.add_argument("--count", type=int, default=10000)
    h.add_argument("--seed", type=int, default=42)
    h.add_argument("--hard-fraction", type=float, default=0.7)
    h.add_argument("--hard-threshold", type=float, default=0.9, help="Rows whose reward is below this are hard")
    g = commands.add_parser("group-sft", help="Pack an existing prepared train/val SFT file into multi-turn samples per image")
    g.add_argument("--data", required=True, help="Prepared dataset directory with DONE.json")
    g.add_argument("--max-turns", type=int, default=8)
    g.add_argument("--max-chars", type=int, default=4000)
    g.add_argument("--seed", type=int, default=42)
    t = commands.add_parser("image-tokens", help="IMAGE_MAX_TOKEN_NUM that keeps prepared images at full size")
    t.add_argument("--model", required=True, help="Local model directory with config.json")
    t.add_argument("--data", required=True, help="Prepared dataset directory with DONE.json")
    d = commands.add_parser("rollout-stats", help="Input JSONL: id, completions (list of strings)")
    d.add_argument("--tasks", required=True)
    d.add_argument("--rollouts", required=True)
    d.add_argument("--out", required=True)
    a = p.parse_args()
    if a.command == "scan":
        if Path(a.out).exists():
            p.error("Manifest output already exists; choose a new path")
        rows = scan(a.root, a.split, a.document_regex, a.single_page_documents, a.ocr_dir)
        write_jsonl(a.out, rows)
        result = {"pages": len(rows), "output": a.out}
    elif a.command == "merge":
        if Path(a.out).exists():
            p.error("Manifest output already exists; choose a new path")
        rows = []
        for path in a.inputs:
            for row in read_jsonl(path):
                for key in ("image", "ocr_json"):
                    if key in row:
                        row[key] = str((Path(path).resolve().parent / row[key]).resolve())
                rows.append(row)
        write_jsonl(a.out, rows)
        result = {"pages": len(rows)}
    elif a.command == "prepare":
        result = prepare(a.config)
    elif a.command == "predict":
        settings = {"endpoint": "http://127.0.0.1:8000/v1", "model": "bank-ocr", "timeout": 180,
                    "max_tokens": 2048, "temperature": 0, "enable_thinking": False, "request_options": {}, "concurrency": 1}
        if a.config:
            configured = load_settings(a.config)
            unknown = configured.keys() - settings.keys()
            if unknown:
                p.error("Unknown inference settings: " + ", ".join(sorted(unknown)))
            settings.update(configured)
        for key in settings:
            value = getattr(a, key, None)
            if value is not None:
                settings[key] = value
        if not isinstance(settings["request_options"], dict):
            p.error("request_options must be an object")
        if not isinstance(settings["timeout"], (int, float)) or settings["timeout"] <= 0:
            p.error("timeout must be positive")
        result = predict(a.tasks, a.out, run_id=a.run_id, with_ocr=a.with_ocr, **settings)
    elif a.command == "evaluate":
        rows = read_jsonl(a.tasks)
        validate_tasks(rows)
        metadata = Path(a.predictions).with_suffix(Path(a.predictions).suffix + ".meta.json")
        info = read_json(metadata) if metadata.exists() else None
        tasks_sha = digest(Path(a.tasks).read_bytes())
        if info and info["tasks_sha256"] != tasks_sha:
            raise ValueError("Prediction metadata refers to a different task file")
        result = {"model_label": a.label, "tasks_sha256": tasks_sha,
                  "inference": info,
                  **evaluate(rows, index_predictions(a.predictions))}
        write_json(a.out, result)
    elif a.command == "compare":
        reports = [read_json(path) for path in a.reports]
        if len({r["tasks_sha256"] for r in reports}) != 1:
            raise ValueError("Reports use different benchmark tasks; do not compare them")
        image_hashes = {(r.get("inference") or {}).get("images_sha256") for r in reports}
        image_hashes.discard(None)
        if len(image_hashes) > 1:
            raise ValueError("Reports use different image content; do not compare them")
        infos = [r.get("inference") or {} for r in reports]
        for key in ("temperature", "max_tokens", "enable_thinking", "request_options"):
            values = [i.get(key, {}) if key == "request_options" else i[key] for i in infos if key == "request_options" or key in i]
            if values and any(v != values[0] for v in values):
                raise ValueError(f"Reports use different inference {key}")
        fields = ["model", "teacher_context", "reference_type"] + [m[0] for m in REPORT_METRICS]
        output = Path(a.out)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for r in reports:
                writer.writerow({"model": r["model_label"], "teacher_context": (r.get("inference") or {}).get("with_ocr", "unknown"),
                                 "reference_type": r["reference_type"],
                                 **{key: r["tasks"].get(task, {}).get(metric) for key, _, task, metric in REPORT_METRICS}})
        result = {"models": len(reports), "output": a.out}
    elif a.command == "mine":
        result = mine(a.tasks, a.predictions, a.out, a.count, a.seed, a.hard_fraction, a.hard_threshold)
    elif a.command == "group-sft":
        result = {}
        for name in ("train_sft", "val_sft"):
            path, single = Path(a.data) / f"{name}.jsonl", Path(a.data) / f"{name}.single.jsonl"
            if not path.exists():
                continue
            if not single.exists():
                path.replace(single)  # keep the one-question-per-sample original; re-runs start from it
            rows = read_jsonl(single)
            samples = group_turns(rows, a.max_turns, a.max_chars, a.seed)
            write_jsonl(path, samples)
            result[name] = {"questions": len(rows), "samples": len(samples)}
    elif a.command == "image-tokens":
        size = read_json(Path(a.data) / "DONE.json")["image_max_size"]
        tokens, factor = image_tokens(a.model, size)
        result = {"image_max_token_num": tokens, "image_max_size": size, "pixels_per_token_side": factor}
    else:
        rows = read_jsonl(a.tasks)
        validate_tasks(rows)
        targets = {r["id"]: r for r in rows}
        values = []
        for group in read_jsonl(a.rollouts):
            r = targets[group["id"]]
            if len(group["completions"]) < 2:
                raise ValueError("Need >=2 completions per rollout group")
            scores = [reward(c, r["task"], r["target"]) for c in group["completions"]]
            values.append({"id": r["id"], "task": r["task"], "reward_std": statistics.pstdev(scores),
                           "unique_completions": len(set(group["completions"])), "rewards": scores})
        result = {"groups": len(values), "zero_variance_fraction": sum(v["reward_std"] < 1e-8 for v in values) / len(values) if values else None, "details": values}
        write_json(a.out, result)
    print(dumps(result))


if __name__ == "__main__":
    main()
