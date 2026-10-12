import hashlib
import importlib
import json
import logging
import math
import re
from pathlib import Path

from PIL import Image, ImageOps

from .metrics import norm, valid_box


def dumps(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, allow_nan=False)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def read_jsonl(path):
    return [json.loads(s) for s in Path(path).read_text(encoding="utf-8-sig").splitlines() if s.strip()]


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(dumps(obj) + "\n", encoding="utf-8")
    tmp.replace(path)


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(dumps(row) + "\n")
    tmp.replace(path)


def load_callable(spec):
    module, name = spec.split(":", 1)
    return getattr(importlib.import_module(module), name)


def at_path(obj, path):
    for part in path.split(".") if path else []:
        obj = obj[int(part)] if isinstance(obj, list) else obj[part]
    return obj


def extract_items(raw, mapping):
    """The OCR adapter must return the actual result, not notebook stdout JSON."""
    if isinstance(raw, str):
        raw = json.loads(raw)
    success_key = mapping.get("success_key")
    if success_key and at_path(raw, success_key) != mapping.get("success_value", "Y"):
        raise ValueError("Internal OCR returned an unsuccessful response")
    path = mapping.get("items_path")
    text_key = mapping.get("text_key", "text")
    box_key = mapping.get("box_key", "bounding")
    if path is not None:
        items = at_path(raw, path)
        if not isinstance(items, list):
            raise ValueError("items_path must point to a list")
        def flatten(values):
            for value in values:
                if isinstance(value, list):
                    yield from flatten(value)
                elif isinstance(value, dict):
                    yield value
                else:
                    raise ValueError("OCR items must be dicts or nested lists of dicts")
        return list(flatten(items))
    def walk(value):
        if isinstance(value, dict):
            if text_key in value and box_key in value:
                yield value
            else:
                for v in value.values():
                    yield from walk(v)
        elif isinstance(value, list):
            for v in value:
                yield from walk(v)
    items = list(walk(raw))
    if not items:
        raise ValueError("No OCR items found. Configure mapping.items_path; use explicit path for empty pages.")
    return items


def pixel_box(value, mapping):
    if mapping.get("box_format", "polygon") == "xyxy":
        return value
    if isinstance(value, dict):
        key = mapping.get("points_key", "vertices")
        value = at_path(value, key)
    if not isinstance(value, list) or len(value) < 2:
        raise ValueError("Polygon requires at least two points")
    xs = [p["x"] if isinstance(p, dict) else p[0] for p in value]
    ys = [p["y"] if isinstance(p, dict) else p[1] for p in value]
    if not all(type(v) in (int, float) and math.isfinite(v) for v in xs + ys):
        raise ValueError("Non-finite polygon coordinate")
    return [min(xs), min(ys), max(xs), max(ys)]


def normalize_box(box, width, height):
    """Pixel [x1,y1,x2,y2] -> 0..1000 integers relative to the image (Qwen-VL bbox_2d)."""
    scaled = [v / (width if i % 2 == 0 else height) * 1000 for i, v in enumerate(box)]
    normalized = [round(v) for v in scaled]
    # Preserve positive area for sub-unit boxes after integer rounding.
    for axis in (0, 1):
        if normalized[axis] == normalized[axis + 2]:
            normalized[axis] = math.floor(scaled[axis])
            normalized[axis + 2] = math.ceil(scaled[axis + 2])
            if normalized[axis] == normalized[axis + 2]:
                normalized[axis + 2] += 1
            if normalized[axis + 2] > 1000:
                normalized[axis], normalized[axis + 2] = 999, 1000
    if not valid_box(normalized):
        raise ValueError("bbox collapsed during normalization")
    return normalized


def parse_ocr(raw, width, height, mapping):
    if any(type(v) not in (int, float) or not math.isfinite(v) or v <= 0 for v in (width, height)):
        raise ValueError(f"Invalid decoded image dimensions: width={width}, height={height}")
    result = []
    zero_area_indices = []
    for idx, item in enumerate(extract_items(raw, mapping)):
        try:
            text = at_path(item, mapping.get("text_key", "text"))
            if not isinstance(text, str):
                raise ValueError("text must be a string")
            confidence = at_path(item, mapping.get("confidence_key", "confidence"))
            if type(confidence) not in (float, int) or not math.isfinite(confidence) or not 0 <= confidence <= 1:
                raise ValueError("confidence must be in [0,1]")
            box = pixel_box(at_path(item, mapping.get("box_key", "bounding")), mapping)
            numeric_box = (isinstance(box, (list, tuple)) and len(box) == 4
                           and all(type(v) in (int, float) and math.isfinite(v) for v in box))
            if (numeric_box and box[0] <= box[2] and box[1] <= box[3]
                    and (box[0] == box[2] or box[1] == box[3])):
                # OCR occasionally returns a line/point instead of a region.
                # Do not invent a crop by expanding it; retain the other items.
                zero_area_indices.append(idx)
                continue
            if not valid_box(box, width, height):
                raise ValueError(f"invalid/out-of-image bbox: {box}; image width={width}, height={height}")
            normalized = normalize_box(box, width, height)
            result.append({"text": norm(text), "bbox": box, "bbox_norm": normalized, "confidence": confidence, "order": idx, "line_num": item.get("line_num")})
        except (KeyError, IndexError, TypeError, ValueError) as e:
            raise ValueError(f"OCR item {idx}: {e}. Check mapping configuration.") from e
    if zero_area_indices:
        logging.getLogger(__name__).warning(
            "Skipped %d zero-area OCR boxes (first indices: %s); image width=%s, height=%s",
            len(zero_area_indices), zero_area_indices[:10], width, height,
        )
    return result


def find_saved_ocr(ocr_dir, relative):
    """Saved OCR JSON for an image: same relative path or same file name, with .json
    replacing (or appended to) the image extension."""
    rel = Path(relative)
    for candidate in (rel.with_suffix(".json"), Path(str(rel) + ".json"),
                      Path(rel.name).with_suffix(".json"), Path(rel.name + ".json")):
        path = Path(ocr_dir) / candidate
        if path.is_file():
            return path.resolve()
    return None


def scan(root, split, document_regex=None, single_page=False, ocr_dir=None):
    root = Path(root).resolve()
    if ocr_dir is not None and not Path(ocr_dir).is_dir():
        raise ValueError(f"OCR result directory not found: {ocr_dir}")
    if not root.is_dir():
        raise ValueError(f"Image directory not found: {root}")
    pattern = re.compile(document_regex) if document_regex else None
    rows = []
    for path in sorted(root.rglob("*")):
        if path.suffix.lower() not in (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"):
            continue
        relative = path.relative_to(root).as_posix()
        match = pattern.search(relative) if pattern else None
        if pattern and (not match or "document_id" not in match.groupdict()):
            raise ValueError(f"Regex must match a named document_id group: {relative}")
        if not pattern and not single_page:
            raise ValueError("Specify document_regex or explicitly declare one image per document")
        doc_id = match.group("document_id") if match else relative
        row = {"document_id": doc_id, "page_id": relative, "image": str(path), "split": split}
        if ocr_dir is not None:
            saved = find_saved_ocr(ocr_dir, relative)
            if saved is None:
                raise ValueError(f"No saved OCR JSON for {relative} under {ocr_dir} (expected e.g. {Path(relative).with_suffix('.json')})")
            row["ocr_json"] = str(saved)
        rows.append(row)
    if not rows:
        raise ValueError("No supported page images found; render PDFs/multipage TIFFs before scanning")
    return rows


def assign_splits(rows, seed, val_fraction, benchmark_fraction=0.0):
    if not 0 <= val_fraction < 1 or not 0 <= benchmark_fraction < 1:
        raise ValueError("val_fraction and benchmark_fraction must be in [0,1)")
    docs, identities = {}, set()
    for r in rows:
        if not all(isinstance(r.get(k), str) and r[k] for k in ("document_id", "page_id", "image", "split")):
            raise ValueError("Each manifest row needs nonempty document_id/page_id/image/split strings")
        if r["split"] not in ("train", "val", "benchmark"):
            raise ValueError("split must be train, val or benchmark")
        old = docs.setdefault(r["document_id"], r["split"])
        if old != r["split"]:
            raise ValueError(f"Document leakage: {r['document_id']}")
        identity = (r["document_id"], r["page_id"])
        if identity in identities:
            raise ValueError(f"Duplicate page identity: {identity}")
        identities.add(identity)
    # Stable document-level held-out splits, independent of manifest ordering.
    if "benchmark" not in docs.values() and benchmark_fraction:
        train_docs = sorted(k for k, v in docs.items() if v == "train")
        if len(train_docs) < 2:
            raise ValueError("Need at least two training documents to hold out a benchmark")
        ranked = sorted(train_docs, key=lambda d: digest(f"{seed}:benchmark:{d}".encode()))
        for d in ranked[:max(1, min(len(ranked) - 1, round(len(ranked) * benchmark_fraction)))]:
            docs[d] = "benchmark"
    if "val" not in docs.values() and val_fraction:
        train_docs = sorted(k for k, v in docs.items() if v == "train")
        if len(train_docs) < 2:
            raise ValueError("Need at least two training documents for validation, or set val_fraction=0")
        ranked = sorted(train_docs, key=lambda d: digest(f"{seed}:{d}".encode()))
        n = max(1, min(len(ranked) - 1, round(len(ranked) * val_fraction)))
        for d in ranked[:n]:
            docs[d] = "val"
    return [{**r, "split": docs[r["document_id"]]} for r in rows]


def exif_orientation(path):
    with Image.open(path) as im:
        return im.getexif().get(274)


def canonical_image(path):
    with Image.open(path) as im:
        if getattr(im, "n_frames", 1) != 1:
            raise ValueError("Multipage image: render to individual pages before preparing")
        im = ImageOps.exif_transpose(im).convert("RGB")
        im.load()
        return im
