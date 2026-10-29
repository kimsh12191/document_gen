"""이미지 폴더 보기, 보낼 그림 만들기 (자르기·상자 그리기·평가와 같은 크기로 줄이기)."""
from __future__ import annotations

import io
import math
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw

from docgen.bench.ocr_data import normalize_box
from docgen.bench.ocr_tasks import MARKERS
from train.mix import DEFAULTS as MIX, fit_size, sample_caps
from train.settings import image_tokens_for

EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
LIST_LIMIT = 5000
# 평가 세트와 같은 그림 크기: 그림 하나 image_max_size 의 토큰까지, 질문 하나는 모든 그림 합쳐 max_image_tokens_per_sample (train/mix.py)
IMAGE_MAX_SIZE = MIX["image_max_size"]
PER_SAMPLE = MIX["max_image_tokens_per_sample"]
COLORS = {en: (en, ko, rgb) for en, ko, rgb in MARKERS}


def _pages(p: Path) -> int:
    if p.suffix.lower() not in (".tif", ".tiff"):
        return 1
    try:
        with Image.open(p) as im:
            return max(1, getattr(im, "n_frames", 1))
    except OSError:
        return 1


def listing(folder: str) -> dict:
    """폴더(하위 포함)의 그림. 여러 쪽 TIFF 는 쪽마다 한 줄. {"folder", "items": [{path, page, name, pages}], "more"}"""
    root = Path(folder).expanduser()
    if not root.is_dir():
        raise ValueError(f"폴더가 아닙니다: {folder}")
    items, more = [], False
    for p in sorted(root.rglob("*")):
        if p.suffix.lower() not in EXTS or not p.is_file() or any(part.startswith(".") for part in p.relative_to(root).parts):
            continue
        n = _pages(p)
        for page in range(n):
            if len(items) >= LIST_LIMIT:
                more = True
                break
            items.append({"path": str(p), "page": page, "name": str(p.relative_to(root)) + (f" ({page + 1}/{n}쪽)" if n > 1 else ""),
                          "pages": n})
        if more:
            break
    return {"folder": str(root.resolve()), "items": items, "more": more}


def load(path: str, page: int = 0) -> Image.Image:
    p = Path(path)
    if p.suffix.lower() not in EXTS or not p.is_file():
        raise ValueError(f"그림 파일이 아닙니다: {path}")
    with Image.open(p) as im:
        if page:
            im.seek(page)
        return im.convert("RGB")


def png(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, "PNG", compress_level=1)
    return buf.getvalue()


@lru_cache(maxsize=512)
def thumb(path: str, page: int, size: int, mtime: float) -> bytes:   # mtime: 파일이 바뀌면 다시
    img = load(path, page)
    img.thumbnail((size, size))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=80)
    return buf.getvalue()


def view(path: str, page: int = 0) -> tuple[bytes, list[int]]:
    """화면에 보일 원본 (PNG) 과 크기. 화면의 상자 좌표는 이 크기 기준 픽셀."""
    img = load(path, page)
    return png(img), [img.width, img.height]


def marker_rect(box: list[float], w: int, h: int) -> list[int]:
    """사람이 끈 상자(글자 둘레) → 벤치마크 marked 과제처럼 그릴 상자: 선 굵기 글자 높이의 8%, 여백 15% (docgen/bench/ocr_tasks.py)."""
    x1, y1, x2, y2 = box
    width = max(2, round((y2 - y1) * 0.08))
    pad = max(3, (y2 - y1) * 0.15) + width
    return [max(0, math.floor(x1 - pad)), max(0, math.floor(y1 - pad)), min(w, math.ceil(x2 + pad)), min(h, math.ceil(y2 + pad))]


def marker_width(box: list[float]) -> int:
    return max(2, round((box[3] - box[1]) * 0.08))


def draw_markers(img: Image.Image, marks: list[dict]) -> Image.Image:
    """marks: [{"box": 픽셀, "color": red|blue|green}] → 상자를 그린 사본."""
    out = img.copy()
    draw = ImageDraw.Draw(out)
    for m in marks:
        draw.rectangle(marker_rect(m["box"], img.width, img.height), outline=COLORS[m["color"]][2], width=marker_width(m["box"]))
    return out


def crop(img: Image.Image, box: list[float]) -> Image.Image:
    x1, y1, x2, y2 = box
    c = (max(0, math.floor(x1)), max(0, math.floor(y1)), min(img.width, math.ceil(x2)), min(img.height, math.ceil(y2)))
    if c[2] - c[0] < 4 or c[3] - c[1] < 4:
        raise ValueError("자를 곳이 너무 작습니다")
    return img.crop(c)


def norm(box: list[float], w: int, h: int) -> list[int]:
    return normalize_box(box, w, h)


def fit(images: list[Image.Image], factor: int, same_as_eval: bool = True) -> list[Image.Image]:
    """평가 세트와 같은 크기로 (train/mix.py: 그림마다 같은 토큰 몫). same_as_eval 이 아니면 그대로."""
    if not same_as_eval:
        return images
    cap = sample_caps(len(images), image_tokens_for(IMAGE_MAX_SIZE, factor), PER_SAMPLE)
    out = []
    for img in images:
        size = fit_size(img.width, img.height, cap, factor)
        out.append(img if size == img.size else img.resize(size, Image.LANCZOS))
    return out
