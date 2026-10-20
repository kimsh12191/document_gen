"""Turn docgen output into the prepared folder that train.py and run_bank_pipeline.py read.

  <output_dir>/
    DONE.json              image budget, counts, sources (docgen meta.json of each folder)
    train_sft.jsonl        SFT samples {"messages", "images"}: docgen training data (+ OCR replay)
    val_sft.jsonl
    train_grpo.jsonl       GRPO pool {"id", "split": "train", "task", "bench_item", "messages", "images"}
    benchmark_tasks.jsonl  benchmark questions for `python -m bank_ocr predict` (PNG images)
    benchmark_items.jsonl  benchmark answers for scoring (docgen format, no images)
    images/                resized copies, only where an image is over its token budget (or not PNG for inference)

Data generation itself (docker container, once) is not part of this: `bash docgen/scripts/make_bank_data.sh`
(README.md section 1) runs, by default,
  python -m docgen.bench build --out bench --bundles 40
  python -m docgen.bench build --split train --out bank_train --per-doc 5 --bundles 200

Image budget: one image keeps at most the tokens of `image_max_size` (same as the OCR stage), and
one sample keeps at most `max_image_tokens_per_sample` over all its images; multi-document samples
(up to 13 pages) are scaled down evenly to fit. The benchmark goes through the same rule, so
training and evaluation see the same pixels.
"""
import hashlib
import json
import math
import os
import random
import time
from pathlib import Path

from PIL import Image

from bank_ocr.cli import image_tokens, image_tokens_for
from bank_ocr.data import read_json, read_jsonl, write_json, write_jsonl

from .score import oracle, reward

DEFAULTS = {
    "image_max_size": [2300, 1600],
    "max_image_tokens_per_sample": 12000,
    "sft_max_length": 16384,
    "sft_max_examples": 20000,
    "task_mix": None,
    "val_count": 200,
    "grpo_holdout": 0.2,
    "pack_turns": 8,
    "replay": None,
    "workers": min(16, os.cpu_count() or 1),
    "seed": 42,
}
BENCH_ITEM_KEYS = ("id", "task", "answer", "eval", "meta")
CHARS_PER_TOKEN = 0.67  # conservative for Korean text: assume 1.5 tokens per character


def folder_kind(path: Path) -> str:
    meta = path / "meta.json"
    if meta.is_file():
        split = read_json(meta).get("split", "test")  # sets built before 1.1 have no split: test
        if split == "train":
            return "bench_train"
        if split == "test":
            return "bench_test"
    if (path / "manifest.jsonl").is_file() and (path / "swift" / "all.jsonl").is_file():
        return "generate"
    raise ValueError(f"{path}: not a docgen output folder (meta.json of `docgen.bench build`, "
                     "or manifest.jsonl + swift/ of `docgen generate --png`)")


def group_key(item_id: str) -> str:
    """Customer bundle (or single document) an item belongs to: 'cross_check/<bundle>/<case>' -> '<bundle>'."""
    parts = item_id.split("/")
    return parts[1] if len(parts) > 1 else item_id.split(":")[0]


def bucket(key: str, seed: int) -> float:
    return int(hashlib.sha1(f"{seed}:{key}".encode()).hexdigest()[:8], 16) / 0x100000000


def _write(job):
    src, dst, size = job
    with Image.open(src) as im:
        img = im.convert("RGB")
        if img.size != tuple(size):
            img = img.resize(tuple(size), Image.LANCZOS)
        tmp = dst.with_name(dst.stem + ".tmp" + dst.suffix)
        if dst.suffix == ".png":
            img.save(tmp, compress_level=1)
        else:
            img.save(tmp, quality=95)
        tmp.replace(dst)


def fit_size(w: int, h: int, cap: int, factor: int) -> tuple[int, int]:
    """Largest size (same aspect) whose visual tokens, ceil(w/factor) x ceil(h/factor), fit `cap`."""
    def tokens(a, b):
        return math.ceil(a / factor) * math.ceil(b / factor)
    if tokens(w, h) <= cap:
        return w, h
    s = min(1.0, math.sqrt(cap * factor ** 2 / (w * h)))
    while tokens(max(1, int(w * s)), max(1, int(h * s))) > cap:
        s *= 0.98
    return max(1, int(w * s)), max(1, int(h * s))


def sample_caps(n_images: int, per_image: int, per_sample: int) -> int:
    """Token cap of each image when a question has n_images: same share for every page."""
    return max(1, min(per_image, per_sample // max(1, n_images)))


class Fitter:
    """Image path under a token cap: the original if it already fits, else a resized copy
    (PNG for inference, which sends PNG; JPEG quality 95 for training). Paths are planned first and
    the copies written together in parallel by run()."""

    def __init__(self, out: Path, factor: int):
        self.out, self.factor, self.cache, self.jobs, self.size = out, factor, {}, {}, {}
        (out / "images").mkdir(parents=True, exist_ok=True)

    def tokens(self, w, h):
        return math.ceil(w / self.factor) * math.ceil(h / self.factor)

    def __call__(self, src: Path, cap: int, png: bool) -> str:
        key = (str(src), cap, png)
        if key in self.cache:
            return self.cache[key]
        with Image.open(src) as im:
            w, h = im.size
        if self.tokens(w, h) <= cap and (not png or src.suffix.lower() == ".png"):
            path, size = str(src), (w, h)
        else:
            size = fit_size(w, h, cap, self.factor)
            dst = self.out / "images" / (hashlib.sha1(f"{src}|{cap}".encode()).hexdigest()[:20] + (".png" if png else ".jpg"))
            path = str(dst)
            if not dst.exists():
                self.jobs[path] = (src, dst, size)
        self.cache[key] = path
        self.size[path] = size
        return path

    def image_tokens(self, path) -> int:
        if path not in self.size:
            with Image.open(path) as im:
                self.size[path] = im.size
        return self.tokens(*self.size[path])

    def run(self, workers: int) -> int:
        jobs = list(self.jobs.values())
        self.jobs = {}
        if workers > 1 and len(jobs) > 1:
            from concurrent.futures import ProcessPoolExecutor
            with ProcessPoolExecutor(workers) as pool:
                list(pool.map(_write, jobs, chunksize=8))
        else:
            for job in jobs:
                _write(job)
        return len(jobs)


def quotas(avail: dict, mix: dict | None, total: int) -> dict:
    """Rows to take per task: `mix` proportions (unlisted tasks get none), filled up from tasks
    that still have rows when one runs short. No mix: proportional to what is available."""
    weights = {t: (mix.get(t, 0) if mix else n) for t, n in avail.items()}
    weights = {t: w for t, w in weights.items() if w > 0 and avail[t] > 0}
    total = min(total, sum(avail[t] for t in weights))
    take = {t: 0 for t in weights}
    left = total
    while left > 0 and weights:
        wsum = sum(weights.values())
        step = {t: min(avail[t] - take[t], max(1, math.floor(left * w / wsum))) for t, w in weights.items()}
        for t, n in sorted(step.items(), key=lambda kv: -kv[1]):
            n = min(n, left)
            take[t] += n
            left -= n
        weights = {t: w for t, w in weights.items() if take[t] < avail[t]}
    return take


def strip_images(text: str) -> str:
    while text.startswith("<image>"):
        text = text[len("<image>"):]
    return text.lstrip("\n")


def pack(rows: list[dict], max_turns: int, room_chars) -> list[dict]:
    """Questions on the same image(s) become one multi-turn conversation (images encoded once);
    image tags stay on the first question only."""
    groups = {}
    for r in rows:
        groups.setdefault(tuple(r["images"]), []).append(r)
    out = []
    for images, group in groups.items():
        turns, chars = [], 0
        limit = room_chars(images)
        for r in group:
            q, a = r["messages"]
            size = len(q["content"]) + len(a["content"])
            if turns and (len(turns) // 2 >= max_turns or chars + size > limit):
                out.append({"messages": turns, "images": list(images)})
                turns, chars = [], 0
            if turns:
                q = {**q, "content": strip_images(q["content"])}
            turns, chars = turns + [q, a], chars + size
        if turns:
            out.append({"messages": turns, "images": list(images)})
    return out


def prepare(data_cfg: dict, model_dir: str | None) -> dict:
    cfg = {**DEFAULTS, **data_cfg}
    out = Path(cfg["output_dir"])
    if (out / "DONE.json").exists():
        raise ValueError(f"{out} already prepared; use a new output_dir")
    out.mkdir(parents=True, exist_ok=True)
    started = time.time()
    seed = cfg["seed"]
    try:
        per_image, factor = image_tokens(model_dir, cfg["image_max_size"])
    except (OSError, ValueError, TypeError) as exc:
        factor = 32
        per_image = image_tokens_for(cfg["image_max_size"], factor)
        print(f"WARNING: {exc}; assuming 32x32 pixels per visual token")
    budget = cfg["max_image_tokens_per_sample"]
    fit = Fitter(out, factor)

    def cap(n):
        return sample_caps(n, per_image, budget)

    # -- sources ---------------------------------------------------------------------------
    bench_dir = Path(cfg["benchmark"])
    if folder_kind(bench_dir) != "bench_test":
        raise ValueError(f"benchmark {bench_dir} must be a test set (`docgen.bench build` without --split train)")
    train_dirs = [Path(p) for p in cfg["train"]]
    kinds = {str(p): folder_kind(p) for p in train_dirs}
    if "bench_test" in kinds.values():
        raise ValueError("A test set is listed under train: " + ", ".join(p for p, k in kinds.items() if k == "bench_test"))
    bench_items = [it for f in sorted((bench_dir / "tasks").glob("*.jsonl")) for it in read_jsonl(f)]
    bench_keys = {group_key(it["id"]) for it in bench_items}

    # -- SFT and GRPO pools from the training folders -------------------------------------
    pools, grpo, overlap = {}, [], 0
    for path in train_dirs:
        kind = kinds[str(path)]
        for r in read_jsonl(path / "swift" / "all.jsonl"):
            key = group_key(r["id"])
            if kind == "bench_train":
                if key in bench_keys:
                    overlap += 1
                    continue
                if bucket(key, seed) < cfg["grpo_holdout"]:
                    continue  # this customer's questions are kept for GRPO
                task = r["task"]
            else:
                task = "gen_" + r["task"]  # docgen generate: its own prompts and answer formats
            pools.setdefault(task, []).append({"id": r["id"], "task": task, "messages": r["messages"],
                                               "images": [path / p for p in r["images"]]})
        if kind == "bench_train":
            for f in sorted((path / "tasks").glob("*.jsonl")):
                for it in read_jsonl(f):
                    key = group_key(it["id"])
                    if key in bench_keys or bucket(key, seed) >= cfg["grpo_holdout"]:
                        continue
                    grpo.append((path, it))
    if overlap:
        raise ValueError(f"{overlap} training rows share a customer with the benchmark; "
                         "build training data with --split train")
    if not pools:
        raise ValueError("No SFT rows: check data.train")

    rng = random.Random(seed)
    for task in sorted(pools):
        pools[task].sort(key=lambda r: r["id"])
        rng.shuffle(pools[task])
    bank_val_pool = [t for t in sorted(pools) if not t.startswith("gen_")]
    val = []
    for i in range(cfg["val_count"]):
        if not bank_val_pool:
            break
        t = bank_val_pool[i % len(bank_val_pool)]
        if len(pools[t]) > 1:
            val.append(pools[t].pop())
    avail = {t: len(rows) for t, rows in pools.items()}
    take = quotas(avail, cfg["task_mix"], cfg["sft_max_examples"])
    chosen = [r for t, n in take.items() for r in pools[t][:n]]

    def to_sample(r):
        imgs = [fit(p, cap(len(r["images"])), png=False) for p in r["images"]]
        return {"messages": r["messages"], "images": imgs}

    def image_tokens_of(images):
        return sum(fit.image_tokens(p) for p in images)

    def room_chars(images):
        return int((cfg["sft_max_length"] - image_tokens_of(images) - 256) * CHARS_PER_TOKEN)

    samples, too_long = [], 0
    for r in chosen:
        s = to_sample(r)
        if sum(len(m["content"]) for m in s["messages"]) > room_chars(s["images"]):
            too_long += 1  # would pass sft_max_length: dropped rather than truncated
        else:
            samples.append(s)
    sft = pack(samples, cfg["pack_turns"], room_chars) if cfg["pack_turns"] > 1 else samples

    replay = 0
    if cfg.get("replay"):
        rows = read_jsonl(cfg["replay"]["path"])
        random.Random(seed).shuffle(rows)
        rows = rows[:cfg["replay"].get("count", 3000)]
        for r in rows:
            for p in r["images"]:
                if not Path(p).is_file():
                    raise ValueError(f"replay image missing: {p}")
        sft += [{"messages": r["messages"], "images": r["images"]} for r in rows]
        replay = len(rows)
    random.Random(seed).shuffle(sft)
    write_jsonl(out / "train_sft.jsonl", sft)
    write_jsonl(out / "val_sft.jsonl", [to_sample(r) for r in val])

    # -- GRPO pool ---------------------------------------------------------------------------
    grpo_rows = []
    for path, it in grpo:
        # PNG: the SFT model answers these through the same inference code as the benchmark (mining).
        imgs = [fit(path / p, cap(len(it["images"])), png=True) for p in it["images"]]
        grpo_rows.append({"id": it["id"], "split": "train", "task": it["task"],
                          "bench_item": json.dumps({k: it[k] for k in BENCH_ITEM_KEYS if k in it}, ensure_ascii=False),
                          "n_images": len(imgs),
                          "messages": [{"role": "user", "content": "<image>" * len(imgs) + it["prompt"]}],
                          "images": imgs})
    grpo_rows.sort(key=lambda r: r["id"])
    write_jsonl(out / "train_grpo.jsonl", grpo_rows)

    # -- benchmark ---------------------------------------------------------------------------
    bench_rows = []
    for it in bench_items:
        imgs = [fit(bench_dir / p, cap(len(it["images"])), png=True) for p in it["images"]]
        bench_rows.append({"id": it["id"], "split": "benchmark", "task": it["task"],
                           "messages": [{"role": "user", "content": "<image>" * len(imgs) + it["prompt"]}],
                           "images": imgs, "source_images": it["images"]})  # docgen paths: page labels in the viewer
    resized = fit.run(cfg["workers"])
    write_jsonl(out / "benchmark_tasks.jsonl", bench_rows)
    write_jsonl(out / "benchmark_items.jsonl", [{k: it[k] for k in BENCH_ITEM_KEYS if k in it} for it in bench_items])

    # The reference answer must score full marks, or the docgen code and the data disagree.
    sample = random.Random(0).sample(bench_items, min(200, len(bench_items)))
    bad = [it["id"] for it in sample if reward(oracle(it), it) < 1.0]
    if bad:
        raise ValueError(f"Reference answers do not score 1.0 with this docgen code (e.g. {bad[:3]}); "
                         "use the docgen code the data was built with")

    def count(rows, key="task"):
        c = {}
        for r in rows:
            c[r[key]] = c.get(r[key], 0) + 1
        return dict(sorted(c.items()))

    done = {
        "image_max_size": cfg["image_max_size"], "pixels_per_token_side": factor,
        "max_image_tokens_per_image": per_image, "max_image_tokens_per_sample": budget,
        "sft_max_length": cfg["sft_max_length"],
        "counts": {"sft_rows_by_task": {t: n for t, n in take.items() if n}, "sft_available_by_task": avail,
                   "sft_samples": len(sft), "sft_packed_from": len(samples), "sft_dropped_too_long": too_long,
                   "replay": replay, "val": len(val), "grpo_by_task": count(grpo_rows),
                   "benchmark_by_task": count(bench_rows), "resized_images": resized},
        "excluded_tasks": sorted(t for t in avail if not take.get(t)),
        "sources": {"train": {p: {"kind": k, "meta": read_json(Path(p) / "meta.json") if k != "generate" else None}
                              for p, k in kinds.items()},
                    "benchmark": {"path": str(bench_dir), "meta": {k: v for k, v in read_json(bench_dir / "meta.json").items()
                                                                     if k != "doc_names"}},
                    "replay": cfg.get("replay")},
        "settings": {k: cfg[k] for k in DEFAULTS},
        "seconds": round(time.time() - started),
    }
    for src in done["sources"]["train"].values():
        if src["meta"]:
            src["meta"].pop("doc_names", None)
    write_json(out / "DONE.json", done)
    return {"output": str(out), **done["counts"]}
