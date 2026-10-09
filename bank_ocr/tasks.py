"""Task rows built from one page view (clean or augmented).

Every task only uses an area when the teacher label for that area is complete:
an area that touches a filtered (low-confidence) word or a word cut by the image
border is rejected, because the answer would silently miss text. Spotting tiles are
the exception: low-confidence words there are painted over in the tile image.
"""
import math

from PIL import ImageDraw, ImageStat

from .data import dumps, normalize_box
from .metrics import size_bucket

PROMPTS = {
    "crop_ocr": [
        "Read all text exactly as written. Do not correct or infer characters. Return only the text.",
        "이미지의 글자를 보이는 그대로 읽으세요. 고치거나 추측하지 말고 글자만 답하세요.",
    ],
    "bbox_ocr": [
        "Read the exact text inside bbox_2d={box}. Coordinates are 0-1000 relative to the image. Return only the text.",
        "bbox_2d={box} 영역 안의 글자를 그대로 읽으세요. 좌표는 이미지 기준 0~1000입니다. 글자만 답하세요.",
    ],
    "region_ocr": [
        "Read all text inside bbox_2d={box} in reading order, one line per text line. Coordinates are 0-1000 relative to the image. Return only the text.",
        "bbox_2d={box} 영역 안의 모든 글자를 읽는 순서대로 적으세요. 줄이 바뀌면 줄바꿈하세요. 좌표는 0~1000입니다. 글자만 답하세요.",
    ],
    "grounding": [
        'Find every occurrence of the exact text {text}. Coordinates are 0-1000 relative to the image. '
        'Return only a JSON list like [{{"bbox_2d": [x1, y1, x2, y2], "label": "..."}}]; return [] if it does not appear.',
        '{text} 와 정확히 같은 글자가 있는 곳을 모두 찾으세요. 좌표는 이미지 기준 0~1000입니다. '
        '[{{"bbox_2d": [x1, y1, x2, y2], "label": "..."}}] 형식의 JSON 리스트만 답하고, 없으면 []로 답하세요.',
    ],
    "spotting": [
        'Detect every piece of text in the image in reading order. Coordinates are 0-1000 relative to the image. '
        'Return only a JSON list like [{{"bbox_2d": [x1, y1, x2, y2], "label": "text"}}].',
        '이미지의 모든 글자를 읽는 순서대로 위치와 함께 찾으세요. 좌표는 0~1000입니다. '
        '[{{"bbox_2d": [x1, y1, x2, y2], "label": "글자"}}] 형식의 JSON 리스트만 답하세요.',
    ],
    "relation": [
        'Find the text immediately {direction} {anchor}. Coordinates are 0-1000 relative to the image. '
        'Return only a JSON list with one entry like [{{"bbox_2d": [x1, y1, x2, y2], "label": "text"}}].',
        '{anchor} 바로 {direction_ko}에 있는 글자를 찾으세요. 좌표는 0~1000입니다. '
        '[{{"bbox_2d": [x1, y1, x2, y2], "label": "글자"}}] 형식으로 하나만 답하세요.',
    ],
}
DIRECTIONS = {"right": ("to the right of", "오른쪽"), "left": ("to the left of", "왼쪽"),
              "below": ("below", "아래"), "above": ("above", "위")}


def area(b):
    return max(0, b[2] - b[0]) * max(0, b[3] - b[1])


def overlap(a, b):
    return area([max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])])


def union(boxes):
    return [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)]


def build_view(image_path, size, items, envelopes, fractions, kind, ops, view_id):
    """Classify every OCR item on the view: visible (kept, maybe clipped), cut by the border, or gone.
    `fractions` is how much of each box survived cropping (see augment.make_view)."""
    width, height = size
    visible = []
    for item, env, fraction in zip(items, envelopes, fractions):
        clipped = [max(0, env[0]), max(0, env[1]), min(width, env[2]), min(height, env[3])]
        inside = fraction * area(clipped) / max(area(env), 1e-9)
        if inside <= 0.02 or clipped[0] >= clipped[2] or clipped[1] >= clipped[3]:
            continue
        cut = inside < 0.98
        try:
            box = normalize_box(clipped, width, height)
        except ValueError:
            continue
        visible.append({**item, "px": clipped, "box": box, "cut": cut, "usable": item["usable"] and not cut})
    return {"id": view_id, "image": image_path, "width": width, "height": height,
            "kind": kind, "ops": ops, "items": visible}


def _row(view, page, task, prompt, image, target, items, size=None):
    return {"task": task, "document_id": page["document_id"], "page_id": page["page_id"], "split": page["split"],
            "view": view["kind"], "view_id": view["id"], "view_ops": view["ops"],
            "reference_type": "ocr_pseudo_unreviewed",
            "messages": [{"role": "user", "content": "<image>\n" + prompt}], "images": [image],
            "context_image": view["image"], "target": dumps(target),
            "confidence": min((i["confidence"] for i in items), default=None), "size": size}


def reading_lines(items):
    """Group words into lines by vertical overlap, top to bottom, then left to right.
    Geometry gives one consistent convention regardless of how the OCR orders its output."""
    lines = []
    for item in sorted(items, key=lambda i: ((i["px"][1] + i["px"][3]) / 2, i["px"][0])):
        y1, y2 = item["px"][1], item["px"][3]
        for line in lines:
            shared = min(line["y2"], y2) - max(line["y1"], y1)
            if shared >= 0.5 * min(line["y2"] - line["y1"], y2 - y1):
                line["items"].append(item)
                line["y1"], line["y2"] = min(line["y1"], y1), max(line["y2"], y2)
                break
        else:
            lines.append({"y1": y1, "y2": y2, "items": [item]})
    lines.sort(key=lambda line: (line["y1"] + line["y2"]) / 2)
    return [sorted(line["items"], key=lambda i: i["px"][0]) for line in lines]


def _entries(items, frame=None, width=None, height=None):
    """Box entries in reading order; re-normalized to `frame` (pixel box of a tile) when given."""
    out = []
    for i in [item for line in reading_lines(items) for item in line]:
        if frame is None:
            box = i["box"]
        else:
            x0, y0 = frame[0], frame[1]
            box = normalize_box([i["px"][0] - x0, i["px"][1] - y0, i["px"][2] - x0, i["px"][3] - y0], width, height)
        out.append({"bbox_2d": box, "label": i["text"]})
    return out


def _height_bucket(box):
    return size_bucket(box[3] - box[1])


def _reading_text(items):
    return "\n".join(" ".join(i["text"] for i in line) for line in reading_lines(items))


def _grow(region, items, key, limit, allow_untrusted=False):
    """Expand `region` until no item is partially inside it. Returns (region, contained) or None
    when the area includes an item whose label is not trustworthy (low-confidence items are
    allowed with `allow_untrusted`; words cut by the image border never are)."""
    for _ in range(50):
        partial = [i for i in items if overlap(i[key], region) > 0 and overlap(i[key], region) < area(i[key])]
        if not partial:
            break
        region = union([region] + [i[key] for i in partial])
        region = [max(0, region[0]), max(0, region[1]), min(limit[0], region[2]), min(limit[1], region[3])]
    else:
        return None
    contained = [i for i in items if overlap(i[key], region) > 0]
    if any(overlap(i[key], region) < area(i[key]) for i in contained):
        return None
    if any(i["cut"] or (not i["usable"] and not allow_untrusted) for i in contained):
        return None
    return region, contained


def crop_tasks(view, page, rng, count, im, crops_dir):
    rows = []
    usable = [i for i in view["items"] if i["usable"]]
    for item in rng.sample(usable, min(count, len(usable))):
        x1, y1, x2, y2 = item["px"]
        # Some context around the word, but never reaching into a neighbouring word.
        pad = (y2 - y1) * rng.uniform(0, 0.3)
        padded = [max(0, x1 - pad), max(0, y1 - pad), min(view["width"], x2 + pad), min(view["height"], y2 + pad)]
        if any(overlap(o["px"], padded) > 0 for o in view["items"] if o is not item):
            padded = [x1, y1, x2, y2]
        path = crops_dir / f"{view['id']}_{item['order']}.png"
        im.crop((math.floor(padded[0]), math.floor(padded[1]), math.ceil(padded[2]), math.ceil(padded[3]))).save(path)
        rows.append(_row(view, page, "crop_ocr", rng.choice(PROMPTS["crop_ocr"]), str(path),
                         {"text": item["text"]}, [item], _height_bucket(item["box"])))
    return rows


def bbox_tasks(view, page, rng, count):
    usable = [i for i in view["items"] if i["usable"]]
    return [_row(view, page, "bbox_ocr", rng.choice(PROMPTS["bbox_ocr"]).format(box=dumps(i["box"])), view["image"],
                 {"text": i["text"]}, [i], _height_bucket(i["box"]))
            for i in rng.sample(usable, min(count, len(usable)))]


def grounding_tasks(view, page, rng, count, negative_fraction, vocabulary):
    by_text = {}
    for i in view["items"]:
        by_text.setdefault(i["text"], []).append(i)
    # Every occurrence must be trustworthy, otherwise the gold list would be incomplete.
    candidates = sorted(t for t, group in by_text.items() if all(i["usable"] for i in group))
    rows = []
    for text in rng.sample(candidates, min(count, len(candidates))):
        group = by_text[text]
        rows.append(_row(view, page, "grounding", rng.choice(PROMPTS["grounding"]).format(text=dumps(text)), view["image"],
                         {"boxes": _entries(group)}, group, _height_bucket(group[0]["box"])))
    negatives = round(len(rows) * negative_fraction / max(1e-9, 1 - negative_fraction)) if rows else 0
    texts = [i["text"] for i in view["items"]]
    # Rejection-sample the (large) vocabulary instead of filtering all of it per view.
    chosen = set()
    for _ in range(negatives * 20):
        if len(chosen) >= negatives or not vocabulary:
            break
        text = vocabulary[rng.randrange(len(vocabulary))]
        if text not in chosen and not any(text in s or s in text for s in texts):
            chosen.add(text)
    for text in sorted(chosen):
        rows.append(_row(view, page, "grounding", rng.choice(PROMPTS["grounding"]).format(text=dumps(text)), view["image"],
                         {"boxes": []}, []))
    return rows


def region_tasks(view, page, rng, count):
    usable = [i for i in view["items"] if i["usable"]]
    rows, seen = [], set()
    for _ in range(count * 6):
        if len(rows) >= count or not usable:
            break
        anchor = rng.choice(usable)
        cx, cy = (anchor["box"][0] + anchor["box"][2]) / 2, (anchor["box"][1] + anchor["box"][3]) / 2
        near = sorted(view["items"], key=lambda i: ((i["box"][0] + i["box"][2]) / 2 - cx) ** 2 + ((i["box"][1] + i["box"][3]) / 2 - cy) ** 2)
        grown = _grow(union([i["box"] for i in near[:rng.randint(2, 12)]]), view["items"], "box", (1000, 1000))
        if grown is None:
            continue
        region, contained = grown
        margin = rng.randint(0, 8)
        wider = [max(0, region[0] - margin), max(0, region[1] - margin), min(1000, region[2] + margin), min(1000, region[3] + margin)]
        if all(overlap(i["box"], wider) == 0 for i in view["items"] if i not in contained):
            region = wider
        key = tuple(sorted(i["order"] for i in contained))
        if len(contained) < 2 or key in seen:
            continue
        seen.add(key)
        rows.append(_row(view, page, "region_ocr", rng.choice(PROMPTS["region_ocr"]).format(box=dumps(region)), view["image"],
                         {"text": _reading_text(contained)}, contained))
    return rows


def _mask(tile, boxes):
    """Paint words over with their surroundings' median colour so the tile shows no text
    that is missing from the answer."""
    draw = ImageDraw.Draw(tile)
    for x1, y1, x2, y2 in boxes:
        pad = max(2, (y2 - y1) * 0.15)
        ring = tile.crop((max(0, math.floor(x1 - pad)), max(0, math.floor(y1 - pad)),
                          min(tile.width, math.ceil(x2 + pad)), min(tile.height, math.ceil(y2 + pad))))
        colour = tuple(int(v) for v in ImageStat.Stat(ring).median)
        draw.rectangle([x1 - 1, y1 - 1, x2 + 1, y2 + 1], fill=colour)
    return tile


def spotting_tasks(view, page, rng, count, im, tiles_dir, max_items):
    """Spotting on tiles cut from the view; coordinates are relative to the tile.
    Low-confidence words inside a tile are masked out instead of rejecting the tile:
    scattered uncertain words would otherwise rule out almost every multi-line tile."""
    W, H = view["width"], view["height"]
    rows, seen = [], set()
    attempts = [None] + [0] * (count * 6)  # first try the whole view
    for attempt in attempts:
        if len(rows) >= count:
            break
        if attempt is None:
            region = [0, 0, W, H]
        else:
            tw, th = W * rng.uniform(0.35, 1.0), H * rng.uniform(0.08, 0.4)
            x0, y0 = rng.uniform(0, W - tw), rng.uniform(0, H - th)
            region = [x0, y0, x0 + tw, y0 + th]
        grown = _grow(region, view["items"], "px", (W, H), allow_untrusted=True)
        if grown is None:
            continue
        region, inside = grown
        contained = [i for i in inside if i["usable"]]
        untrusted = [i for i in inside if not i["usable"]]
        region = [math.floor(region[0]), math.floor(region[1]), math.ceil(region[2]), math.ceil(region[3])]
        key = tuple(sorted(i["order"] for i in contained))
        if not 1 <= len(contained) <= max_items or key in seen or region[2] - region[0] < 8 or region[3] - region[1] < 8:
            continue
        seen.add(key)
        tw, th = region[2] - region[0], region[3] - region[1]
        path = tiles_dir / f"{view['id']}_{len(rows)}.png"
        tile = im.crop(tuple(region))
        if untrusted:
            x0, y0 = region[0], region[1]
            tile = _mask(tile, [[i["px"][0] - x0, i["px"][1] - y0, i["px"][2] - x0, i["px"][3] - y0] for i in untrusted])
        tile.save(path)
        row = _row(view, page, "spotting", rng.choice(PROMPTS["spotting"]).format(), str(path),
                   {"boxes": _entries(contained, region, tw, th)}, contained)
        row["masked_words"] = len(untrusted)
        rows.append(row)
    return rows


def _neighbour(anchor, items, direction):
    a = anchor["box"]
    ah, aw = a[3] - a[1], a[2] - a[0]
    found = []
    for i in items:
        if i is anchor:
            continue
        b = i["box"]
        if direction in ("right", "left"):
            shared = min(a[3], b[3]) - max(a[1], b[1])
            if shared < 0.5 * min(ah, b[3] - b[1]):
                continue
            gap = b[0] - a[2] if direction == "right" else a[0] - b[2]
            limit = 8 * ah
        else:
            shared = min(a[2], b[2]) - max(a[0], b[0])
            if shared < 0.5 * min(aw, b[2] - b[0]):
                continue
            gap = b[1] - a[3] if direction == "below" else a[1] - b[3]
            limit = 3 * ah
        if -0.2 * ah <= gap <= limit:
            found.append((gap, i))
    found.sort(key=lambda t: t[0])
    if not found:
        return None
    # Ambiguous when a second candidate is about as close as the first.
    if len(found) > 1 and found[1][0] - found[0][0] < 0.5 * ah:
        return None
    return found[0][1]


def relation_tasks(view, page, rng, count):
    counts = {}
    for i in view["items"]:
        counts[i["text"]] = counts.get(i["text"], 0) + 1
    usable = [i for i in view["items"] if i["usable"]]
    rows, seen = [], set()
    for _ in range(count * 6):
        if len(rows) >= count or not usable:
            break
        anchor = rng.choice(usable)
        direction = rng.choice(sorted(DIRECTIONS))
        if (anchor["order"], direction) in seen:
            continue
        seen.add((anchor["order"], direction))
        target = _neighbour(anchor, view["items"], direction)
        if target is None or not target["usable"]:
            continue
        # Refer to the anchor by text when it is unique on the view, otherwise by its box.
        by_text = counts[anchor["text"]] == 1 and rng.random() < 0.5
        ref = dumps(anchor["text"]) if by_text else "the text at bbox_2d=" + dumps(anchor["box"])
        ref_ko = dumps(anchor["text"]) if by_text else "bbox_2d=" + dumps(anchor["box"]) + " 글자"
        template = rng.randrange(2)
        prompt = PROMPTS["relation"][template].format(direction=DIRECTIONS[direction][0], direction_ko=DIRECTIONS[direction][1],
                                                      anchor=ref if template == 0 else ref_ko)
        rows.append(_row(view, page, "relation", prompt, view["image"], {"boxes": _entries([target])},
                         [anchor, target], _height_bucket(target["box"])))
    return rows
