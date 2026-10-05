"""라벨 좌표 확인용: 이미지 위에 값/항목명/체크박스/도장·서명 위치를 그린다.

  python scripts/visualize_labels.py out/labels/loan_application_000000.json            # 원본 이미지
  python scripts/visualize_labels.py out/swift/grounding.jsonl --line 3                  # 학습 레코드 (0~1000 좌표)
결과는 같은 폴더의 *_viz.png
  파랑=값, 초록=항목명, 빨강=체크된 칸, 주황=빈 칸, 자홍=도장(있음), 회색=도장·서명(없음), 남색=서명(있음)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw

C = {"value": (30, 90, 230), "label": (20, 160, 60), "on": (230, 30, 30), "off": (240, 150, 0),
     "seal": (220, 0, 200), "sign": (40, 40, 140), "absent": (130, 130, 130)}


def draw_label(path: Path) -> list[Path]:
    lab = json.loads(path.read_text(encoding="utf-8"))
    root = path.parent.parent
    imgs = [Image.open(root / p).convert("RGB") for p in lab.get("images", [lab["image"]])]
    draws = [ImageDraw.Draw(im) for im in imgs]
    for f in lab["fields"]:
        d = draws[f.get("page", 0)]
        if f["type"] in ("seal", "signature"):
            if f.get("bbox"):
                col = C["absent"] if not f["present"] else C["seal"] if f["type"] == "seal" else C["sign"]
                d.rectangle(f["bbox"], outline=col, width=3)
            continue
        if f.get("bbox"):
            d.rectangle(f["bbox"], outline=C["value"], width=2)
        if f.get("label_bbox"):
            d.rectangle(f["label_bbox"], outline=C["label"], width=1)
        for o in f.get("options", []):
            if o.get("box_bbox"):
                d.rectangle(o["box_bbox"], outline=C["on" if o["checked"] else "off"], width=2)
    outs = []
    for i, im in enumerate(imgs):
        o = path.with_name(f"{path.stem}_p{i + 1}_viz.png")
        im.save(o)
        outs.append(o)
    return outs


def draw_record(path: Path, line: int) -> list[Path]:
    rec = json.loads(path.read_text(encoding="utf-8").splitlines()[line])
    root = path.parent.parent
    imgs = [Image.open(root / p).convert("RGB") for p in rec["images"]]
    ans = json.loads(rec["messages"][1]["content"])
    items = ans if isinstance(ans, list) else [*ans.get("checkboxes", []), *ans.get("seals", []), *ans.get("signatures", [])]

    def px(b, im):
        return [b[0] / 1000 * im.width, b[1] / 1000 * im.height, b[2] / 1000 * im.width, b[3] / 1000 * im.height]

    for it in items:
        im = imgs[it.get("page", 1) - 1]
        d = ImageDraw.Draw(im)
        if it.get("bbox_2d"):
            col = C["value"] if "value" in it else C["seal"] if it.get("present") else C["absent"]
            d.rectangle(px(it["bbox_2d"], im), outline=col, width=2)
        for o in it.get("options", []):
            if o.get("bbox_2d"):
                d.rectangle(px(o["bbox_2d"], im), outline=C["on" if o["checked"] else "off"], width=2)
    outs = []
    for i, im in enumerate(imgs):
        o = path.with_name(f"{path.stem}_{line}_p{i + 1}_viz.png")
        im.save(o)
        outs.append(o)
    return outs


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--line", type=int, default=0)
    a = ap.parse_args()
    p = Path(a.path)
    print(*(draw_record(p, a.line) if p.suffix == ".jsonl" else draw_label(p)), sep="\n")
