"""Shared evaluation/reward definitions; all reference labels are unreviewed OCR.

Box outputs use the Qwen-VL grounding format: a JSON list of
{"bbox_2d": [x1, y1, x2, y2], "label": "..."} with 0..1000 integer coordinates
relative to the input image. Text tasks answer with plain text.
"""
import json
import math
import re
import unicodedata


TEXT_TASKS = ("crop_ocr", "bbox_ocr", "region_ocr", "marked_ocr")
BOX_TASKS = ("grounding", "spotting", "relation", "marked_box")
TASKS = TEXT_TASKS + BOX_TASKS
# Box-list tasks whose predicted labels are scored (grounding's label is the query itself).
LABELLED_TASKS = ("spotting", "relation", "marked_box")
HIGH_CONFIDENCE = 0.95
SIZE_BUCKETS = ((12, "small"), (25, "medium"), (math.inf, "large"))  # target box height, 0..1000 units

# add_non_thinking_prefix trains the model to emit an empty think block before the answer.
EMPTY_THINK = re.compile(r"^\s*<think>\s*</think>\s*")
FENCE = re.compile(r"^```(?:json)?\s*\n?(.*?)\n?\s*```$", re.S)

# (key, heading, task, metric) used by `compare` and benchmark_report.py.
REPORT_METRICS = [
    ("crop_cer", "Crop CER ↓", "crop_ocr", "cer"),
    ("bbox_text_em", "BBox→Text EM ↑", "bbox_ocr", "em"),
    ("bbox_numeric_em", "Numeric EM ↑", "bbox_ocr", "numeric_em"),
    ("region_cer", "Region CER ↓", "region_ocr", "cer"),
    ("grounding_f1", "Grounding F1@0.5 ↑", "grounding", "f1_iou50"),
    ("grounding_negative_acc", "Grounding 없음 정확도 ↑", "grounding", "negative_accuracy"),
    ("spotting_det_f1", "Spotting 위치 F1@0.5 ↑", "spotting", "f1_iou50"),
    ("spotting_e2e_f1", "Spotting 위치+글자 F1 ↑", "spotting", "e2e_f1"),
    ("relation_e2e_f1", "Relation 위치+글자 F1 ↑", "relation", "e2e_f1"),
    ("marked_text_em", "그린 박스→글자 EM ↑", "marked_ocr", "em"),
    # The drawn rectangle is an exact label, so the stricter IoU 0.75 is meaningful here.
    ("marked_box_f1", "그린 박스→좌표 F1@0.75 ↑", "marked_box", "f1_iou75"),
]
LOWER_IS_BETTER = {"crop_cer", "region_cer"}


def answer(text):
    return EMPTY_THINK.sub("", text, count=1)


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


def parse_target(target):
    return json.loads(target) if isinstance(target, str) else target


def answer_for(task, target):
    """The exact assistant answer for a task row (SFT target and oracle prediction)."""
    target = parse_target(target)
    if task in BOX_TASKS:
        return json.dumps([{"bbox_2d": b["bbox_2d"], "label": b["label"]} for b in target["boxes"]], ensure_ascii=False)
    return target["text"]


def parse_boxes(text):
    """Strict list-of-boxes parser. A single ```json fence is tolerated because base
    models emit it; anything else malformed returns None (counted as invalid)."""
    text = answer(text).strip()
    fenced = FENCE.match(text)
    if fenced:
        text = fenced.group(1).strip()
    try:
        value = json.loads(text)
    except ValueError:
        return None
    if isinstance(value, dict):
        value = [value]
    if not isinstance(value, list):
        return None
    boxes = []
    for entry in value:
        if not isinstance(entry, dict) or not valid_box(entry.get("bbox_2d")):
            return None
        label = entry.get("label", "")
        if not isinstance(label, str):
            return None
        boxes.append({"bbox_2d": entry["bbox_2d"], "label": label})
    return boxes


def iou(a, b):
    inter = max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))
    area = lambda c: (c[2] - c[0]) * (c[3] - c[1])
    return inter / max(area(a) + area(b) - inter, 1e-12)


def center_inside(item, container):
    x, y = (item[0] + item[2]) / 2, (item[1] + item[3]) / 2
    return container[0] <= x <= container[2] and container[1] <= y <= container[3]


def match(preds, gts, accept):
    """Greedy one-to-one matching by IoU over pairs that `accept(pred, gt, iou)`."""
    pairs = []
    for i, p in enumerate(preds):
        for j, g in enumerate(gts):
            value = iou(p["bbox_2d"], g["bbox_2d"])
            if accept(p, g, value):
                pairs.append((value, i, j))
    pairs.sort(key=lambda t: (-t[0], t[1], t[2]))
    used_p, used_g, result = set(), set(), []
    for value, i, j in pairs:
        if i not in used_p and j not in used_g:
            used_p.add(i)
            used_g.add(j)
            result.append((i, j, value))
    return result


def reward(completion, task, target, iou_full=0.8):
    """GRPO reward in [0, 1].

    Text tasks: character similarity, with 30% on numeric tokens when the target has numbers.
    Box tasks: soft F1 = 2 * sum(credit) / (#pred + #gold). Pairs are matched greedily by IoU
    (any overlap). Box credit is min(1, IoU / iou_full): OCR boxes are not consistently
    tight, so IoU above `iou_full` is not pushed further toward the teacher's box edges.
    Spotting/relation credit is 50% box + 50% label similarity. Extra or missing boxes
    lower the score through the denominator; for a negative target only [] scores 1.
    """
    target = parse_target(target)
    completion = answer(completion)
    if task in TEXT_TASKS:
        text = target["text"]
        char = similarity(completion, text)
        nums = numbers(text)
        return (0.7 * char + 0.3 * similarity(" ".join(numbers(completion)), " ".join(nums))) if nums else char
    if task not in BOX_TASKS:
        raise ValueError(f"Unknown task: {task}")
    preds, gts = parse_boxes(completion), target["boxes"]
    if preds is None:
        return 0.0
    if not gts or not preds:
        return float(not gts and not preds)
    credit = 0.0
    for i, j, value in match(preds, gts, lambda p, g, v: v > 0):
        box = min(1.0, value / iou_full)
        credit += 0.5 * box + 0.5 * similarity(preds[i]["label"], gts[j]["label"]) if task in LABELLED_TASKS else box
    return 2 * credit / (len(preds) + len(gts))


def _ratio(num, den):
    return num / den if den else None


def _f1(p, r):
    return 2 * p * r / (p + r) if p is not None and r is not None and p + r else (0.0 if p is not None and r is not None else None)


def _text_metrics(subset, predictions):
    targets = [parse_target(r["target"])["text"] for r in subset]
    preds = [predictions[r["id"]] for r in subset]
    numeric = [(p, t) for p, t in zip(preds, targets) if numbers(t)]
    vals = {
        "cer": sum(distance(p, t) for p, t in zip(preds, targets)) / max(1, sum(len(norm(t)) for t in targets)),
        "em": sum(norm(p) == norm(t) for p, t in zip(preds, targets)) / len(subset),
        "numeric_em": sum(numbers(p) == numbers(t) for p, t in numeric) / len(numeric) if numeric else None,
        "numeric_count": len(numeric),
    }
    if subset[0]["task"] == "region_ocr":
        # Order-insensitive word overlap separates recognition errors from reading-order errors.
        hit = pred_n = gold_n = 0
        for p, t in zip(preds, targets):
            pw, tw = norm(p).split(), norm(t).split()
            remaining = list(tw)
            for w in pw:
                if w in remaining:
                    remaining.remove(w)
                    hit += 1
            pred_n, gold_n = pred_n + len(pw), gold_n + len(tw)
        vals["word_f1"] = _f1(_ratio(hit, pred_n) or 0.0, _ratio(hit, gold_n) or 0.0)
    return vals


def _box_metrics(subset, predictions):
    task = subset[0]["task"]
    labelled = task in LABELLED_TASKS
    n_pred = n_gold = valid = 0
    m50 = m75 = e2e = centre = 0
    matched_iou, label_dist, label_len = [], 0, 0
    negatives = negative_ok = count_ok = 0
    for r in subset:
        gts = parse_target(r["target"])["boxes"]
        preds = parse_boxes(predictions[r["id"]])
        n_gold += len(gts)
        if not gts:
            negatives += 1
            negative_ok += preds == []
        if preds is None:
            continue
        valid += 1
        n_pred += len(preds)
        count_ok += len(preds) == len(gts)
        at50 = match(preds, gts, lambda p, g, v: v >= 0.5)
        m50 += len(at50)
        m75 += len(match(preds, gts, lambda p, g, v: v >= 0.75))
        matched_iou.extend(v for *_, v in at50)
        centre += len(match(preds, gts, lambda p, g, v: v > 0 and center_inside(p["bbox_2d"], g["bbox_2d"])
                                                     and center_inside(g["bbox_2d"], p["bbox_2d"])))
        if labelled:
            e2e += len(match(preds, gts, lambda p, g, v: v >= 0.5 and norm(p["label"]) == norm(g["label"])))
            for i, j, _ in at50:
                label_dist += distance(preds[i]["label"], gts[j]["label"])
                label_len += len(norm(gts[j]["label"]))
    def f1(hits):
        return _f1(_ratio(hits, n_pred) if n_pred else 0.0, _ratio(hits, n_gold) if n_gold else 0.0)
    vals = {
        "valid_json_rate": valid / len(subset),
        "precision_iou50": _ratio(m50, n_pred), "recall_iou50": _ratio(m50, n_gold),
        "f1_iou50": f1(m50), "f1_iou75": f1(m75),
        # Mutual centre containment: tolerant to how tightly the teacher OCR draws boxes.
        "f1_center": f1(centre),
        "mean_iou_matched": sum(matched_iou) / len(matched_iou) if matched_iou else None,
        "count_accuracy": count_ok / len(subset),
        "negative_count": negatives,
        "negative_accuracy": negative_ok / negatives if negatives else None,
    }
    if labelled:
        vals["e2e_f1"] = f1(e2e)
        vals["matched_label_cer"] = label_dist / label_len if label_len else None
    return vals


def evaluate_tasks(rows, predictions):
    output = {}
    for task in TASKS:
        subset = [r for r in rows if r["task"] == task]
        if subset:
            metrics = _text_metrics(subset, predictions) if task in TEXT_TASKS else _box_metrics(subset, predictions)
            output[task] = {"count": len(subset), **metrics}
    return output


def size_bucket(height):
    return next(name for limit, name in SIZE_BUCKETS if height < limit)


def evaluate(rows, predictions):
    expected = {r["id"] for r in rows}
    if set(predictions) != expected:
        raise ValueError(f"Prediction IDs differ: missing={len(expected - set(predictions))}, extra={len(set(predictions) - expected)}")
    predictions = {k: answer(v) for k, v in predictions.items()}
    groups = {
        # clean = resized original; aug = synthetic geometric/photometric degradation.
        "view": lambda r: r.get("view"),
        # Teacher confidence: low-confidence labels are themselves unreliable.
        "confidence": lambda r: None if r.get("confidence") is None else ("high" if r["confidence"] >= HIGH_CONFIDENCE else "low"),
        "size": lambda r: r.get("size"),
    }
    breakdown = {}
    for name, key in groups.items():
        buckets = {}
        for r in rows:
            value = key(r)
            if value is not None:
                buckets.setdefault(value, []).append(r)
        breakdown[name] = {value: evaluate_tasks(subset, predictions) for value, subset in sorted(buckets.items())}
    return {"reference_type": "ocr_pseudo_unreviewed", "interpretation": "agreement_with_internal_ocr_not_verified_accuracy",
            "tasks": evaluate_tasks(rows, predictions), "breakdown": breakdown}
