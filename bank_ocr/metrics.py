"""Shared evaluation/reward definitions; all reference labels are unreviewed OCR."""
import json
import math
import re
import unicodedata


def norm(text):
    return unicodedata.normalize("NFC", text.replace("\r\n", "\n")).strip()


def distance(a, b):
    a, b = norm(a), norm(b)
    if len(a) < len(b):
        a, b = b, a
    row = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        nxt = [i]
        for j, cb in enumerate(b, 1):
            nxt.append(min(nxt[-1] + 1, row[j] + 1, row[j - 1] + (ca != cb)))
        row = nxt
    return row[-1]


def similarity(a, b):
    return 1 - distance(a, b) / max(len(norm(a)), len(norm(b)), 1)


def numbers(text):
    # Preserve separate numeric tokens and punctuation, including signs.
    # "12 34" must not become equivalent to "1234".
    return re.findall(r"[+\-]?[0-9]+(?:[.,/:\-][0-9]+)*%?", norm(text))


def valid_box(box, width=1000, height=1000):
    return (isinstance(box, (list, tuple)) and len(box) == 4
            and all(type(x) in (int, float) and math.isfinite(x) for x in box)
            and 0 <= box[0] < box[2] <= width
            and 0 <= box[1] < box[3] <= height)


def parse_box(text):
    try:
        obj = json.loads(text)
        box = obj.get("bbox") if isinstance(obj, dict) else None
        return box if valid_box(box) and set(obj) == {"bbox"} else None
    except (ValueError, TypeError):
        return None


def iou(a, b):
    inter = max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))
    area = lambda c: (c[2] - c[0]) * (c[3] - c[1])
    return inter / max(area(a) + area(b) - inter, 1e-12)


def center_inside(item, container):
    x, y = (item[0] + item[2]) / 2, (item[1] + item[3]) / 2
    return container[0] <= x <= container[2] and container[1] <= y <= container[3]


def recover_text(box, items):
    # Keep the OCR provider's order. Do not reorder rotated/multi-column pages.
    return " ".join(x["text"] for x in items if center_inside(x["bbox"], box))


def reward(completion, task, target_text, target_bbox=None, ocr_items=None):
    if task == "grounding":
        box = parse_box(completion)
        if box is None:
            return 0.0
        return (0.55 * similarity(recover_text(box, ocr_items), target_text)
                + 0.35 * iou(box, target_bbox) + 0.10)
    if task not in ("ocr", "crop_ocr", "bbox_ocr"):
        raise ValueError(f"Unknown task: {task}")
    char = similarity(completion, target_text)
    nums = numbers(target_text)
    return (0.7 * char + 0.3 * similarity(" ".join(numbers(completion)), " ".join(nums))) if nums else char


def evaluate(rows, predictions):
    expected = {r["id"] for r in rows}
    if set(predictions) != expected:
        raise ValueError(f"Prediction IDs differ: missing={len(expected - set(predictions))}, extra={len(set(predictions) - expected)}")
    output = {"reference_type": "ocr_pseudo_unreviewed", "interpretation": "agreement_with_internal_ocr_not_verified_accuracy", "tasks": {}}
    for task in ("crop_ocr", "bbox_ocr", "grounding"):
        subset = [r for r in rows if r["task"] == task]
        if not subset:
            continue
        n = len(subset)
        if task == "grounding":
            boxes = [parse_box(predictions[r["id"]]) for r in subset]
            scores = [iou(b, r["target_bbox"]) if b else 0.0 for b, r in zip(boxes, subset)]
            vals = {
                "mean_iou": sum(scores) / n,
                "iou_at_0_5": sum(s >= 0.5 for s in scores) / n,
                "valid_json_box_rate": sum(b is not None for b in boxes) / n,
                "center_hit_rate": sum(b is not None and center_inside(b, r["target_bbox"]) for b, r in zip(boxes, subset)) / n,
                "cycle_em": sum(b is not None and norm(recover_text(b, r["ocr_items"])) == norm(r["target_text"]) for b, r in zip(boxes, subset)) / n,
            }
        else:
            numeric = [r for r in subset if numbers(r["target_text"])]
            vals = {
                "cer": sum(distance(predictions[r["id"]], r["target_text"]) for r in subset) / max(1, sum(len(norm(r["target_text"])) for r in subset)),
                "em": sum(norm(predictions[r["id"]]) == norm(r["target_text"]) for r in subset) / n,
                "numeric_em": sum(numbers(predictions[r["id"]]) == numbers(r["target_text"]) for r in numeric) / len(numeric) if numeric else None,
                "numeric_count": len(numeric),
            }
        output["tasks"][task] = {"count": n, **vals}
    return output
