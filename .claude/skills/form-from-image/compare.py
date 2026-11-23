"""원본 그림과 초안 서식의 렌더를 눈으로 비교할 그림을 만든다 (form-from-image 스킬 5단계).

    python .claude/skills/form-from-image/compare.py --source <원본 그림 …> --render <preview --out 폴더> --out <폴더>

- --source: 원본 그림. 쪽마다 하나씩, 쪽 순서대로 (png/jpg).
- --render: `python -m docgen.preview --dir <초안> --out <폴더>` 의 --out 폴더 (안의 label.json 을 찾는다).
- 만드는 것 (쪽마다):
    side_<쪽>.png     왼쪽 원본 · 오른쪽 렌더 (같은 크기로 맞춤)
    overlay_<쪽>.png  원본(옅은 회색) 위에 렌더의 선·글자(빨강), 값 자리 박스(파랑, 키 이름)
- 원본은 렌더 쪽 크기(A4)로 늘려 맞출 뿐 기울기·여백은 보정하지 않는다. 스캔 여백만큼 전체가 어긋나 보이는 것은 무시하고 부분끼리의 어긋남을 본다.
- 마지막 줄에 JSON: {"pages": {"source": n, "render": m}, "images": [...], "warnings": [...]}
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

SIDE_WIDTH = 2000          # 나란히 놓은 그림의 가로 (모델이 읽기 좋은 크기)


def find_label(render):
    labels = sorted(Path(render).rglob("label.json"), key=lambda p: p.stat().st_mtime)
    if not labels:
        raise SystemExit(f"label.json 이 없습니다: {render} (docgen.preview --out 폴더를 주세요)")
    return labels[-1]


def page_images(label_path, label, render):
    out = []
    for rel in label["images"]:
        for cand in (Path(render) / rel, label_path.parent / Path(rel).name):
            if cand.exists():
                out.append(cand)
                break
        else:
            raise SystemExit(f"렌더 그림을 찾지 못했습니다: {rel}")
    return out


def side_by_side(src, ren):
    gap = 24
    canvas = Image.new("RGB", (src.width + gap + ren.width, max(src.height, ren.height)), "white")
    canvas.paste(src, (0, 0))
    canvas.paste(ren, (src.width + gap, 0))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([src.width, 0, src.width + gap - 1, canvas.height], fill=(180, 180, 180))
    draw.text((10, 10), "SOURCE", fill=(200, 0, 0))
    draw.text((src.width + gap + 10, 10), "RENDER", fill=(200, 0, 0))
    scale = SIDE_WIDTH / canvas.width
    return canvas.resize((SIDE_WIDTH, round(canvas.height * scale))) if scale < 1 else canvas


def overlay(src, ren, boxes):
    base = ImageOps.grayscale(src).point(lambda v: 140 + v * 115 // 255).convert("RGB")   # 옅은 회색 원본
    ink = ImageOps.grayscale(ren).point(lambda v: 255 if v < 160 else 0)                  # 렌더의 선·글자
    base.paste((220, 0, 0), mask=ink)
    draw = ImageDraw.Draw(base)
    for key, (x0, y0, x1, y1) in boxes:
        draw.rectangle([x0, y0, x1, y1], outline=(0, 90, 255), width=2)
        draw.text((x0 + 2, max(0, y0 - 11)), key, fill=(0, 90, 255))
    return base


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--source", nargs="+", required=True)
    ap.add_argument("--render", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    label_path = find_label(a.render)
    label = json.loads(label_path.read_text(encoding="utf-8"))
    renders = page_images(label_path, label, a.render)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    warnings = []
    if len(a.source) != len(renders):
        warnings.append(f"쪽 수가 다릅니다: 원본 {len(a.source)} · 렌더 {len(renders)} (--rows min 렌더와 비교했는지 확인)")
    images = []
    for page, (src_path, ren_path) in enumerate(zip(a.source, renders)):
        ren = Image.open(ren_path).convert("RGB")
        src = ImageOps.exif_transpose(Image.open(src_path)).convert("RGB")
        ratio = (src.height / src.width) / (ren.height / ren.width)
        if abs(ratio - 1) > 0.08:
            warnings.append(f"{page}쪽: 원본 가로세로 비율이 A4 와 {abs(ratio - 1):.0%} 다릅니다 (잘린 사진·가로 서식인지 확인)")
        src = src.resize(ren.size)
        boxes = [(f["key"], f["bbox"]) for f in label.get("fields", []) if f.get("page", 0) == page and f.get("bbox")]
        for name, img in ((f"side_{page}.png", side_by_side(src, ren)), (f"overlay_{page}.png", overlay(src, ren, boxes))):
            img.save(out / name)
            images.append(str(out / name))
    print(json.dumps({"pages": {"source": len(a.source), "render": len(renders)}, "images": images, "warnings": warnings},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
