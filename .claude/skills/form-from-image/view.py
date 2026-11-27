"""보기 창: 원본·렌더의 한 곳을 잘라 크게, 눈금·칸 이름을 그려 view_<n>.png 에 쓴다 (form-from-image 스킬).

    python .claude/skills/form-from-image/view.py page    <초안> [--page 1] [--to 1]
    python .claude/skills/form-from-image/view.py crop    <초안> x0 y0 x1 y1 [--page 1] [--to 1] [--cells]
    python .claude/skills/form-from-image/view.py table   <초안> T2 [--rows 3-8] [--page 1] [--to 1]
    python .claude/skills/form-from-image/view.py compare <초안> x0 y0 x1 y1 [--page 1] [--to 1]      (위 원본 · 아래 렌더)
    python .claude/skills/form-from-image/view.py overlay <초안> x0 y0 x1 y1 [--page 1] [--to 1]      (원본 회색 위에 렌더 빨강)

- 자리는 **쪽 px** (쪽 가로 794, grid.py 와 같음). 먼저 grid.py 를 돌려 page_<n>.png·grid_<n>.json 이 있어야 한다.
- 결과는 초안 폴더의 view_<to>.png (1~4). 에이전트 진행기(ReLab)에서는 이 네 장이 요청에 붙어 있어서,
  명령으로 다시 쓰면 **다음 단계에서 새 그림이 보인다**. Claude Code 에서는 그 파일을 열어 본다.
- 그림 위: 위·왼쪽 가장자리에 쪽 px 눈금(10마다 짧게, 50마다 숫자). page·table·crop --cells 는 칸 이름(T2.7)과 글자 덩어리(B3)를 파랑으로.
- compare·overlay 의 렌더는 render_<n>.png (check.py 가 만든다; 없거나 템플릿보다 오래됐으면 여기서 새로 그린다).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
S = 2                       # page_<n>.png 은 쪽 px × 2
MAX_SIDE = 1600             # 창 그림 긴 쪽
MAX_BYTES = 2 * 1024 * 1024 - 64 * 1024
RULER = 34
BLUE, RED = (0, 70, 230), (220, 0, 0)


def font(size: int):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:                       # 옛 Pillow
        return ImageFont.load_default()


def load_page(draft: Path, page: int) -> Image.Image:
    p = draft / f"page_{page}.png"
    if not p.exists():
        raise SystemExit(f"{p.name} 이 없습니다. 먼저: python .claude/skills/form-from-image/grid.py {draft}")
    return Image.open(p).convert("RGB")


def load_grid(draft: Path, page: int) -> dict:
    p = draft / f"grid_{page}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"tables": [], "blocks": []}


def render_image(draft: Path, page: int) -> Image.Image:
    """render_<n>.png — 없거나 템플릿·form.json 보다 오래됐으면 새로 그린다 (seed 1)."""
    out = draft / f"render_{page}.png"
    newest = max((draft / f).stat().st_mtime for f in ("template.html.j2", "form.json", "generate.py") if (draft / f).exists())
    if not out.exists() or out.stat().st_mtime < newest:
        sys.path.insert(0, str(HERE))
        import check  # noqa: E402
        check.save_renders(draft)
    if not out.exists():
        raise SystemExit(f"렌더 {out.name} 을 만들지 못했습니다 (쪽 수가 원본보다 적을 수 있음). check.py 를 돌려 오류를 보세요.")
    im = Image.open(out).convert("RGB")
    return im


def clamp(box, w, h):
    x0, y0, x1, y1 = box
    x0, x1 = sorted((max(0, x0), min(w, x1)))
    y0, y1 = sorted((max(0, y0), min(h, y1)))
    if x1 - x0 < 4 or y1 - y0 < 4:
        raise SystemExit(f"자리가 너무 작거나 쪽 밖입니다: {box} (쪽 px 0~{w}, 0~{h})")
    return x0, y0, x1, y1


def zoom_for(box) -> float:
    w, h = (box[2] - box[0]) * S, (box[3] - box[1]) * S
    return min(3.0, (MAX_SIDE - RULER) / max(w, h))


def with_ruler(img: Image.Image, box, z: float) -> Image.Image:
    """img = 쪽 px box 를 z 배(작업 그림 기준)로 키운 것. 위·왼쪽에 쪽 px 눈금."""
    W, H = img.size
    canvas = Image.new("RGB", (W + RULER, H + RULER), "white")
    canvas.paste(img, (RULER, RULER))
    d = ImageDraw.Draw(canvas)
    f = font(12)
    k = S * z                                   # 쪽 px 1 = 그림 k px
    step_label = 50 if k * 50 >= 60 else 100
    if k * 10 >= 40:
        step_label = 10 if k * 10 >= 60 else 20
    for axis in ("x", "y"):
        a0, a1 = (box[0], box[2]) if axis == "x" else (box[1], box[3])
        v = int(a0 // 10 * 10)
        while v <= a1:
            if v >= a0:
                p = RULER + (v - a0) * k
                big = v % step_label == 0
                ln = 12 if big else 5
                if axis == "x":
                    d.line([(p, RULER - ln), (p, RULER - 1)], fill=(0, 0, 0))
                    if big:
                        d.text((p + 2, 2), str(v), fill=(0, 0, 0), font=f)
                else:
                    d.line([(RULER - ln, p), (RULER - 1, p)], fill=(0, 0, 0))
                    if big:
                        d.text((1, p + 1), str(v), fill=(0, 0, 0), font=f)
            v += 10
    return canvas


def cut(im: Image.Image, box, z: float) -> Image.Image:
    c = im.crop(tuple(round(v * S) for v in box))
    return c.resize((max(1, round(c.width * z)), max(1, round(c.height * z))), Image.LANCZOS)


def label_cells(img: Image.Image, g: dict, box, z: float, rows: tuple[int, int] | None = None, table: str | None = None):
    d = ImageDraw.Draw(img)
    f = font(max(11, min(16, int(6 * z * S / 2))))
    k = S * z

    def put(text, x, y):
        px, py = (x - box[0]) * k + 2, (y - box[1]) * k + 1
        if px < 0 or py < 0 or px > img.width - 10 or py > img.height - 8:
            return
        tb = d.textbbox((px, py), text, font=f)
        d.rectangle([tb[0] - 1, tb[1] - 1, tb[2] + 1, tb[3] + 1], fill=(255, 255, 255))
        d.text((px, py), text, fill=BLUE, font=f)

    for t in g.get("tables", []):
        if table and t["id"] != table:
            continue
        for c in t["cells"]:
            if rows and not (c["r"] <= rows[1] and c["r"] + c["rs"] - 1 >= rows[0]):
                continue
            b = c["box"]
            if b[2] <= box[0] or b[0] >= box[2] or b[3] <= box[1] or b[1] >= box[3]:
                continue
            put(c["id"], max(b[0], box[0]), max(b[1], box[1]))
    if not table:
        for bl in g.get("blocks", []):
            b = bl["box"]
            if b[2] <= box[0] or b[0] >= box[2] or b[3] <= box[1] or b[1] >= box[3]:
                continue
            x0, y0, x1, y1 = ((b[0] - box[0]) * k, (b[1] - box[1]) * k, (b[2] - box[0]) * k, (b[3] - box[1]) * k)
            d.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], outline=(255, 140, 0), width=1)
            put(bl["id"], b[0], max(box[1], b[1] - 7 / (k / 2)))


def save(img: Image.Image, dest: Path) -> int:
    if max(img.size) > MAX_SIDE + RULER * 2:
        img.thumbnail((MAX_SIDE + RULER, MAX_SIDE + RULER))
    img.save(dest, optimize=True)
    if dest.stat().st_size > MAX_BYTES:
        img.convert("P", palette=Image.ADAPTIVE, colors=64).save(dest, optimize=True)
    while dest.stat().st_size > MAX_BYTES:
        img = img.resize((int(img.width * 0.85), int(img.height * 0.85)), Image.LANCZOS)
        img.convert("P", palette=Image.ADAPTIVE, colors=64).save(dest, optimize=True)
    return dest.stat().st_size


def stack(a: Image.Image, b: Image.Image, names=("원본 SOURCE", "렌더 RENDER")) -> Image.Image:
    """넓으면 위아래, 높으면 좌우."""
    f = font(14)
    gap = 26
    if a.width >= a.height:
        canvas = Image.new("RGB", (max(a.width, b.width), a.height + b.height + 2 * gap), "white")
        canvas.paste(a, (0, gap))
        canvas.paste(b, (0, a.height + 2 * gap))
        d = ImageDraw.Draw(canvas)
        d.text((4, 4), names[0], fill=RED, font=f)
        d.text((4, a.height + gap + 4), names[1], fill=RED, font=f)
        d.line([(0, a.height + gap + 1), (canvas.width, a.height + gap + 1)], fill=(150, 150, 150), width=2)
    else:
        canvas = Image.new("RGB", (a.width + b.width + gap, max(a.height, b.height) + gap), "white")
        canvas.paste(a, (0, gap))
        canvas.paste(b, (a.width + gap, gap))
        d = ImageDraw.Draw(canvas)
        d.text((4, 4), names[0], fill=RED, font=f)
        d.text((a.width + gap + 4, 4), names[1], fill=RED, font=f)
        d.line([(a.width + gap // 2, 0), (a.width + gap // 2, canvas.height)], fill=(150, 150, 150), width=2)
    return canvas


def overlay_img(src: Image.Image, ren: Image.Image) -> Image.Image:
    base = ImageOps.grayscale(src).point(lambda v: 150 + v * 105 // 255).convert("RGB")
    ink = ImageOps.grayscale(ren).point(lambda v: 255 if v < 150 else 0)
    base.paste(RED, mask=ink)
    return base


def parse_rows(s: str | None):
    if not s:
        return None
    a, _, b = s.partition("-")
    return int(a), int(b or a)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["page", "crop", "table", "compare", "overlay"])
    ap.add_argument("draft", type=Path)
    ap.add_argument("args", nargs="*")
    ap.add_argument("--page", type=int, default=1)
    ap.add_argument("--to", type=int, default=1, choices=[1, 2, 3, 4], help="보기 창 번호 (view_<n>.png)")
    ap.add_argument("--rows", help="table: 행 범위 (예: 3-8)")
    ap.add_argument("--cells", action="store_true", help="crop: 칸 이름·글자 덩어리 그리기")
    a = ap.parse_args(argv)
    src = load_page(a.draft, a.page)
    g = load_grid(a.draft, a.page)
    w, h = src.width // S, src.height // S
    dest = a.draft / f"view_{a.to}.png"
    if a.mode == "page":
        box = (0, 0, w, h)
        z = min(1.0, (MAX_SIDE - RULER) / (h * S))
        img = cut(src, box, z)
        label_cells(img, g, box, z)
        what = f"원본 {a.page}쪽 전체"
    elif a.mode == "table":
        if not a.args:
            raise SystemExit("표 이름을 주세요 (예: T2)")
        tid = a.args[0].split(":")[-1]
        t = next((t for t in g["tables"] if t["id"] == tid), None)
        if t is None:
            raise SystemExit(f"{tid} 가 없습니다. 있는 표: {', '.join(t['id'] for t in g['tables']) or '없음'}")
        rows = parse_rows(a.rows)
        ys = t["ys"]
        y0, y1 = (ys[rows[0] - 1], ys[min(rows[1], len(ys) - 1)]) if rows else (t["box"][1], t["box"][3])
        box = clamp((t["box"][0] - 6, y0 - 6, t["box"][2] + 6, y1 + 6), w, h)
        z = zoom_for(box)
        img = cut(src, box, z)
        label_cells(img, g, box, z, rows, tid)
        what = f"원본 {a.page}쪽 표 {tid}" + (f" 행 {rows[0]}~{rows[1]}" if rows else "")
    else:
        if len(a.args) != 4:
            raise SystemExit("자리 x0 y0 x1 y1 (쪽 px) 을 주세요")
        box = clamp(tuple(float(v) for v in a.args), w, h)
        z = zoom_for(box)
        if a.mode == "crop":
            img = cut(src, box, z)
            if a.cells:
                label_cells(img, g, box, z)
            what = f"원본 {a.page}쪽"
        else:
            ren = render_image(a.draft, a.page)
            if ren.size != src.size:
                ren = ren.resize(src.size, Image.LANCZOS)
            if a.mode == "compare":
                z = zoom_for((0, 0, box[2] - box[0], (box[3] - box[1]) * 2)) if (box[2] - box[0]) >= (box[3] - box[1]) else \
                    zoom_for((0, 0, (box[2] - box[0]) * 2, box[3] - box[1]))
                img = stack(with_ruler(cut(src, box, z), box, z), with_ruler(cut(ren, box, z), box, z))
                size = save(img, dest)
                print(f"{dest.name}: {a.page}쪽 x {box[0]:.0f}~{box[2]:.0f} y {box[1]:.0f}~{box[3]:.0f} 원본(위·왼)과 렌더(아래·오른) "
                      f"{z * S:.1f}배 · {size // 1024}KB")
                return 0
            img = cut(overlay_img(src, ren), box, z)
            what = f"{a.page}쪽 겹치기 (회색 원본 · 빨강 렌더)"
    img = with_ruler(img, box, z)
    size = save(img, dest)
    print(f"{dest.name}: {what} · x {box[0]:.0f}~{box[2]:.0f} y {box[1]:.0f}~{box[3]:.0f} · {z * S:.1f}배 · {size // 1024}KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
