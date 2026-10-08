import math
import random
from collections import Counter, defaultdict
from pathlib import Path

from .data import (assign_splits, canonical_image, digest, dumps, load_callable,
                   parse_ocr, read_json, read_jsonl, write_json, write_jsonl)


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
                   "image_policy": "EXIF transpose, RGB PNG, original dimensions; OCR and VLM share pixels"})
    # DONE is written last; incomplete builds must never be used for training.
    write_json(out / "DONE.json", result)
    return result


def build_datasets(pages, out, cfg):
    rng = random.Random(cfg.get("seed", 42))
    pools = defaultdict(list)
    audit = Counter()
    candidates = Counter()
    for page in pages:
        split = page["split"]
        thresholds = cfg.get("filters", {}).get("benchmark" if split == "benchmark" else "train", {})
        confidence = thresholds.get("min_confidence", 0.0 if split == "benchmark" else 0.95)
        minimum, maximum = thresholds.get("min_length", 1), thresholds.get("max_length", 100)
        if not 0 <= confidence <= 1 or not 1 <= minimum <= maximum:
            raise ValueError("Invalid filter thresholds")
        counts = Counter(x["text"] for x in page["ocr"] if x["text"])
        all_items = [{"text": x["text"], "bbox": x["bbox_norm"]} for x in page["ocr"] if x["text"]]
        usable = []
        for item in page["ocr"]:
            candidates[split] += 1
            if item["confidence"] < confidence or not minimum <= len(item["text"]) <= maximum or "\ufffd" in item["text"]:
                audit[f"{split}:filtered"] += 1
                continue
            usable.append(item)
        cap = cfg.get("benchmark_regions_per_page", 5) if split == "benchmark" else cfg.get("train_regions_per_page", 0)
        if cap and len(usable) > cap:
            usable = sorted(rng.sample(usable, cap), key=lambda r: r["order"])
        with canonical_image(page["image"]) as im:
            for item in usable:
                box, text = item["bbox_norm"], item["text"]
                region_id = f"{page['id']}_{item['order']}"
                crop = (out / "crops" / f"{region_id}.png").resolve()
                crop.parent.mkdir(exist_ok=True)
                x1, y1, x2, y2 = item["bbox"]
                im.crop((math.floor(x1), math.floor(y1), math.ceil(x2), math.ceil(y2))).save(crop)
                for task in ("crop_ocr", "bbox_ocr", "grounding"):
                    if task == "grounding" and counts[text] != 1:
                        audit[f"{split}:ambiguous_grounding"] += 1
                        continue
                    if task == "crop_ocr":
                        prompt = "Read all text exactly as written. Do not correct or infer characters. Return only the text."
                    elif task == "bbox_ocr":
                        prompt = f"Read the exact text inside bbox={dumps(box)}. Coordinates range from 0 to 1000. Return only the text."
                    else:
                        prompt = f"Locate this exact text: {dumps(text)}. Coordinates range from 0 to 1000. Return only JSON: {{\"bbox\":[x1,y1,x2,y2]}}"
                    pools[split].append({
                        "id": f"{region_id}_{task}", "document_id": page["document_id"], "page_id": page["page_id"],
                        "split": split, "reference_type": "ocr_pseudo_unreviewed", "task": task,
                        "messages": [{"role": "user", "content": "<image>\n" + prompt}],
                        "images": [str(crop) if task == "crop_ocr" else page["image"]],
                        "target_text": text, "target_bbox": box, "ocr_items": all_items,
                        "confidence": item["confidence"],
                    })
    if not pools["train"] or not pools["benchmark"]:
        raise ValueError("Empty train/benchmark dataset after filtering; inspect OCR and thresholds")
    train = pools["train"]
    # Fixed proportions where enough candidates exist; no oversampling duplicates.
    limit = cfg.get("sft_max_examples", 30000)
    if limit <= 0:
        raise ValueError("sft_max_examples must be positive")
    groups = {t: [r for r in train if r["task"] == t] for t in ("crop_ocr", "bbox_ocr", "grounding")}
    chosen, remaining = [], []
    for i, (task, proportion) in enumerate(zip(groups, (0.4, 0.3, 0.3))):
        group = groups[task]
        rng.shuffle(group)
        quota = int(limit * proportion)
        chosen.extend(group[:quota])
        remaining.extend(group[quota:])
    rng.shuffle(remaining)
    chosen.extend(remaining[:max(0, min(limit, len(train)) - len(chosen))])
    rng.shuffle(chosen)
    for split in ("train", "val", "benchmark"):
        write_jsonl(out / f"{split}_tasks.jsonl", pools[split])
    def sft(rows):
        for r in rows:
            answer = dumps({"bbox": r["target_bbox"]}) if r["task"] == "grounding" else r["target_text"]
            yield {"messages": r["messages"] + [{"role": "assistant", "content": answer}], "images": r["images"]}
    write_jsonl(out / "train_sft.jsonl", sft(chosen))
    write_jsonl(out / "val_sft.jsonl", sft(pools["val"]))
    grpo = [r for r in train if r["task"] in cfg.get("grpo_tasks", ["bbox_ocr", "grounding"])]
    write_jsonl(out / "train_grpo.jsonl", grpo)
    return {"sft_examples": len(chosen), "sft_task_counts": dict(Counter(r["task"] for r in chosen)),
            "grpo_examples": len(grpo), "benchmark_examples": len(pools["benchmark"]),
            "ocr_region_counts": dict(candidates), "filter_audit": dict(audit)}
