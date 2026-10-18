"""docgen labels -> OCR JSON in the in-house OCR response format, one file per page image (example data only).

Real training uses the in-house OCR on real scans. For the guide examples there is no real image to show, so this
turns the generator's ground truth (value boxes, label boxes) into the same response format, one line per item:

  python guide/examples/labels_to_ocr.py <docgen generate --out 폴더> <OCR JSON 폴더>
"""
import json, random, sys
from pathlib import Path

gen, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
rng = random.Random(0)
for lf in sorted((gen / "labels").glob("*.json")):
    lab = json.loads(lf.read_text(encoding="utf-8"))
    pages = {}
    for f in lab["fields"]:
        p = f.get("page", 0)
        if f.get("type") not in ("seal", "signature", "checkbox", "checkbox_multi") and f.get("bbox") and isinstance(f.get("value"), str) and f["value"].strip():
            lines = [s for s in f["value"].split("\n") if s.strip()]
            x0, y0, x1, y1 = f["bbox"]
            h = (y1 - y0) / len(lines)
            for i, s in enumerate(lines):
                pages.setdefault(p, []).append((s.strip(), [x0, y0 + i * h, x1, y0 + (i + 1) * h]))
        if f.get("label") and f.get("label_bbox"):
            pages.setdefault(p, []).append((f["label"], f["label_bbox"]))
    for p, img in enumerate(lab["images"]):
        seen, items = set(), []
        for text, (x0, y0, x1, y1) in pages.get(p, []):
            key = (text, round(x0), round(y0))
            if key in seen:
                continue
            seen.add(key)
            conf = round(rng.choice([0.9999, 0.998, 0.995, 0.99, 0.97, 0.91]), 4)
            items.append({"text": text, "confidence": conf, "bounding": {"shape": "rectangle", "vertices": [
                {"x": round(x0), "y": round(y0)}, {"x": round(x1), "y": round(y0)},
                {"x": round(x1), "y": round(y1)}, {"x": round(x0), "y": round(y1)}]}, "line_num": 0})
        name = Path(img).name
        (out / (Path(name).stem + ".json")).write_text(json.dumps(
            {"filename": name, "success": "Y", "data": {"basicData": [items]}}, ensure_ascii=False), encoding="utf-8")
print("done")
