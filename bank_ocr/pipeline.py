import random
from collections import Counter, defaultdict
from pathlib import Path

from .augment import make_view
from .data import (assign_splits, canonical_image, digest, dumps, load_callable,
                   parse_ocr, read_json, read_jsonl, write_json, write_jsonl)
from .metrics import TASKS, answer_for
from .tasks import (bbox_tasks, build_view, crop_tasks, grounding_tasks, marked_tasks, region_tasks,
                    relation_tasks, spotting_tasks)


def prepare(config_path):
    cfg = read_json(config_path)
    base = Path(config_path).resolve().parent
    resolve = lambda value: (base / value).resolve()
    out, cache = resolve(cfg["output_dir"]), resolve(cfg["cache_dir"])
    if out.exists():
        raise ValueError(f"Output already exists: {out}. Use a new output_dir; OCR cache is reusable.")
    seed = cfg.get("seed", 42)
    manifest = resolve(cfg["manifest"])
    rows = assign_splits(read_jsonl(manifest), seed, cfg.get("val_fraction", 0.05))
    if not any(r["split"] == "train" for r in rows) or not any(r["split"] == "benchmark" for r in rows):
        raise ValueError("Manifest must include train and benchmark documents")
    mapping = cfg.get("mapping", {})
    adapter = load_callable(cfg["ocr_callable"])
    revision = cfg["ocr_revision"]
    if not revision:
        raise ValueError("Set ocr_revision to the internal OCR model/config version for cache invalidation")
    cache.mkdir(parents=True, exist_ok=True)
    pixels, pages = {}, []
    # Preflight every page before invoking OCR; identical decoded pixels cannot cross splits.
    for row in sorted(rows, key=lambda r: (r["document_id"], r["page_id"])):
        source = (manifest.parent / row["image"]).resolve()
        im = canonical_image(source)
        sha = digest(str(im.size).encode() + im.tobytes())
        old_split = pixels.setdefault(sha, row["split"])
        if old_split != row["split"]:
            raise ValueError(f"Duplicate image leakage across {old_split}/{row['split']}: {source}")
        staged = cache / "images" / f"{sha}.png"
        if not staged.exists():
            staged.parent.mkdir(exist_ok=True)
            im.save(staged)
        pages.append({**row, "source_image": str(source), "image": str(staged), "pixel_sha256": sha, "width": im.width, "height": im.height,
                      "id": digest(dumps([row["document_id"], row["page_id"]]).encode())[:24]})
        im.close()
    for n, page in enumerate(pages, 1):
        key = digest(dumps([page["pixel_sha256"], cfg["ocr_callable"], revision]).encode())
        cached = cache / "ocr" / f"{key}.json"
        if not cached.exists():
            # OCR sees the EXACT same orientation-normalized PNG used by the VLM.
            raw = adapter(page["image"])
            parse_ocr(raw, page["width"], page["height"], mapping)
            write_json(cached, raw)
        page["ocr"] = parse_ocr(read_json(cached), page["width"], page["height"], mapping)
        page["ocr_cache"] = str(cached)
        page["reference_type"] = "ocr_pseudo_unreviewed"
        if n == 1 or n % 100 == 0 or n == len(pages):
            print(f"OCR {n}/{len(pages)}", flush=True)
    out.mkdir(parents=True)
    write_json(out / "config.snapshot.json", cfg)
    write_jsonl(out / "pages.jsonl", pages)
    result = build_datasets(pages, out, cfg)
    result.update({"reference_type": "ocr_pseudo_unreviewed", "human_reviewed": False,
                   "page_counts": dict(Counter(p["split"] for p in pages)),
                   "ocr_revision": revision, "manifest_sha256": digest(manifest.read_bytes()),
                   "image_policy": "OCR reads the EXIF-transposed original; model views are resized to image_max_size "
                                   "(clean) or degraded copies (aug) whose boxes follow every geometric step"})
    # DONE is written last; incomplete builds must never be used for training.
    write_json(out / "DONE.json", result)
    return result


OBSOLETE_KEYS = {"train_regions_per_page": "tasks_per_view", "benchmark_regions_per_page": "tasks_per_view"}
DEFAULT_VIEWS = {"train": {"clean": 1, "augmented": 2}, "val": {"clean": 1, "augmented": 1},
                 "benchmark": {"clean": 1, "augmented": 1}}
DEFAULT_TASKS_PER_VIEW = {
    "train": {"crop_ocr": 4, "bbox_ocr": 8, "grounding": 8, "region_ocr": 4, "spotting": 2, "relation": 6,
              "marked_ocr": 3, "marked_box": 3},
    "val": {"crop_ocr": 1, "bbox_ocr": 2, "grounding": 2, "region_ocr": 1, "spotting": 1, "relation": 2,
            "marked_ocr": 1, "marked_box": 1},
    "benchmark": {"crop_ocr": 2, "bbox_ocr": 4, "grounding": 4, "region_ocr": 2, "spotting": 1, "relation": 3,
                  "marked_ocr": 2, "marked_box": 2},
}
DEFAULT_TASK_MIX = {"crop_ocr": 0.1, "bbox_ocr": 0.15, "grounding": 0.2, "region_ocr": 0.15, "spotting": 0.15,
                    "relation": 0.15, "marked_ocr": 0.05, "marked_box": 0.05}


def build_datasets(pages, out, cfg):
    for key, replacement in OBSOLETE_KEYS.items():
        if key in cfg:
            raise ValueError(f"Config key {key} is no longer used; configure {replacement}")
    rng = random.Random(cfg.get("seed", 42))
    max_size = cfg.get("image_max_size", [2300, 1600])
    if len(max_size) != 2 or min(max_size) < 32:
        raise ValueError("image_max_size must be [long_side, short_side]")
    views_cfg = {**DEFAULT_VIEWS, **cfg.get("views", {})}
    per_view_cfg = {**DEFAULT_TASKS_PER_VIEW, **cfg.get("tasks_per_view", {})}
    augment = cfg.get("augment", {})
    negative_fraction = cfg.get("negative_grounding_fraction", 0.1)
    max_items = cfg.get("spotting_max_items", 40)
    if not 0 <= negative_fraction < 1 or max_items < 1:
        raise ValueError("Invalid negative_grounding_fraction/spotting_max_items")
    for directory in ("views", "crops", "tiles", "marked"):
        (out / directory).mkdir(parents=True, exist_ok=True)
    # Negative grounding queries come from other pages of the same split.
    vocabulary = defaultdict(set)
    for page in pages:
        vocabulary[page["split"]].update(x["text"] for x in page["ocr"] if 2 <= len(x["text"]) <= 20)
    vocabulary = {k: sorted(v) for k, v in vocabulary.items()}
    pools, audit, candidates, image_items = defaultdict(list), Counter(), Counter(), []
    for page in pages:
        split = page["split"]
        thresholds = cfg.get("filters", {}).get("benchmark" if split == "benchmark" else "train", {})
        confidence = thresholds.get("min_confidence", 0.0 if split == "benchmark" else 0.95)
        minimum, maximum = thresholds.get("min_length", 1), thresholds.get("max_length", 100)
        if not 0 <= confidence <= 1 or not 1 <= minimum <= maximum:
            raise ValueError("Invalid filter thresholds")
        items = []
        for x in page["ocr"]:
            if not x["text"]:
                continue
            candidates[split] += 1
            usable = x["confidence"] >= confidence and minimum <= len(x["text"]) <= maximum and "\ufffd" not in x["text"]
            audit[f"{split}:{'usable' if usable else 'filtered'}"] += 1
            items.append({"text": x["text"], "confidence": x["confidence"], "order": x["order"],
                          "line_num": x.get("line_num"), "usable": usable})
        boxes = [x["bbox"] for x in page["ocr"] if x["text"]]
        counts = per_view_cfg[split]
        specs = views_cfg[split]
        kinds = ["clean"] * specs.get("clean", 1) + ["aug"] * specs.get("augmented", 0)
        with canonical_image(page["image"]) as original:
            for n, kind in enumerate(kinds):
                view_rng = random.Random(f"{cfg.get('seed', 42)}:{page['id']}:{n}")
                im, envelopes, fractions, ops = make_view(original, boxes, view_rng, max_size, augment if kind == "aug" else None)
                view_id = f"{page['id']}_v{n}"
                path = (out / "views" / f"{view_id}.png").resolve()
                im.save(path)
                view = build_view(str(path), im.size, items, envelopes, fractions, kind, ops, view_id)
                audit[f"{split}:{kind}:cut_items"] += sum(i["cut"] for i in view["items"])
                rows = (crop_tasks(view, page, view_rng, counts.get("crop_ocr", 0), im, out / "crops")
                        + bbox_tasks(view, page, view_rng, counts.get("bbox_ocr", 0))
                        + grounding_tasks(view, page, view_rng, counts.get("grounding", 0), negative_fraction, vocabulary[split])
                        + region_tasks(view, page, view_rng, counts.get("region_ocr", 0))
                        + spotting_tasks(view, page, view_rng, counts.get("spotting", 0), im, out / "tiles", max_items))
                rows += relation_tasks(view, page, view_rng, counts.get("relation", 0))
                rows += marked_tasks(view, page, view_rng, counts.get("marked_ocr", 0), counts.get("marked_box", 0),
                                     im, out / "marked")
                numbering = Counter()
                for row in rows:
                    row["id"] = f"{view_id}_{row['task']}_{numbering[row['task']]}"
                    numbering[row["task"]] += 1
                    pools[split].append(row)
                image_items.append({"image": str(path), "width": im.width, "height": im.height, "kind": kind, "ops": ops,
                                    "items": [{"text": i["text"], "bbox_2d": i["box"], "confidence": i["confidence"]} for i in view["items"]]})
                im.close()
    if not pools["train"] or not pools["benchmark"]:
        raise ValueError("Empty train/benchmark dataset after filtering; inspect OCR and thresholds")
    train = pools["train"]
    # Fixed proportions where enough candidates exist; no oversampling duplicates.
    limit = cfg.get("sft_max_examples", 30000)
    if limit <= 0:
        raise ValueError("sft_max_examples must be positive")
    mix = cfg.get("task_mix", DEFAULT_TASK_MIX)
    if any(task not in TASKS for task in mix) or abs(sum(mix.values()) - 1) > 1e-6:
        raise ValueError("task_mix must use known tasks and sum to 1")
    chosen, remaining = [], []
    for task in TASKS:
        group = [r for r in train if r["task"] == task]
        rng.shuffle(group)
        quota = int(limit * mix.get(task, 0))
        chosen.extend(group[:quota])
        remaining.extend(group[quota:])
    rng.shuffle(remaining)
    chosen.extend(remaining[:max(0, min(limit, len(train)) - len(chosen))])
    rng.shuffle(chosen)
    for split in ("train", "val", "benchmark"):
        write_jsonl(out / f"{split}_tasks.jsonl", pools[split])
    write_jsonl(out / "image_items.jsonl", image_items)
    def sft(rows):
        for r in rows:
            yield {"messages": r["messages"] + [{"role": "assistant", "content": answer_for(r["task"], r["target"])}], "images": r["images"]}
    val = list(pools["val"])
    rng.shuffle(val)
    write_jsonl(out / "train_sft.jsonl", sft(chosen))
    write_jsonl(out / "val_sft.jsonl", sft(val[:cfg.get("val_max_examples", 2000)]))
    grpo_tasks = cfg.get("grpo_tasks", ["grounding", "spotting", "relation"])
    grpo = [{k: r[k] for k in ("id", "task", "split", "messages", "images", "target")} for r in train if r["task"] in grpo_tasks]
    write_jsonl(out / "train_grpo.jsonl", grpo)
    count = lambda rows: dict(sorted(Counter(r["task"] for r in rows).items()))
    return {"sft_examples": len(chosen), "sft_task_counts": count(chosen),
            "grpo_examples": len(grpo), "benchmark_examples": len(pools["benchmark"]),
            "benchmark_task_counts": count(pools["benchmark"]),
            "benchmark_view_counts": dict(Counter(r["view"] for r in pools["benchmark"])),
            "image_max_size": max_size, "ocr_region_counts": dict(candidates), "filter_audit": dict(sorted(audit.items()))}
