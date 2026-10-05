"""스캔/촬영 느낌의 이미지 증강 (Pillow 만 사용).

깨끗한 렌더링 이미지만으로 학습하면 실제 스캔본·폰카 사진에서 성능이 떨어지므로,
기울기·배경·밝기·흐림·노이즈·JPEG 압축을 무작위로 섞는다. 텍스트 내용은 바뀌지 않으므로
정답(GT)은 원본과 동일하게 쓴다.
"""
from __future__ import annotations

import io
import math
import random

from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps

PRESETS = ("scan", "photo", "fax", "clean_jpeg")


def _background(rng: random.Random, size: tuple[int, int]) -> Image.Image:
    base = rng.choice([(60, 60, 60), (120, 100, 80), (200, 200, 195), (35, 45, 60), (150, 140, 120)])
    bg = Image.new("RGB", size, base)
    noise = Image.effect_noise(size, rng.uniform(8, 25)).convert("RGB")
    return ImageChops.add(bg, noise, scale=2.0, offset=-64)


def _noise(img: Image.Image, rng: random.Random, sigma: float) -> Image.Image:
    n = Image.effect_noise(img.size, sigma).convert("RGB")
    return ImageChops.add(img, n, scale=1.0, offset=-128)


class Transform:
    """증강의 기하 변환(회전·이동·확대)을 누적해 원본 좌표를 증강 이미지 좌표로 옮긴다."""

    def __init__(self):
        self.ops: list[tuple] = []

    def rotate(self, angle: float, w: int, h: int, nw: int, nh: int):
        self.ops.append(("rot", math.radians(angle), w / 2, h / 2, nw / 2, nh / 2))

    def shift(self, dx: float, dy: float):
        self.ops.append(("shift", dx, dy))

    def scale(self, sx: float, sy: float):
        self.ops.append(("scale", sx, sy))

    def point(self, x: float, y: float) -> tuple[float, float]:
        for op in self.ops:
            if op[0] == "rot":  # PIL rotate: 반시계 방향, y 축이 아래
                _, a, cx, cy, ncx, ncy = op
                dx, dy = x - cx, y - cy
                x, y = ncx + dx * math.cos(a) + dy * math.sin(a), ncy - dx * math.sin(a) + dy * math.cos(a)
            elif op[0] == "shift":
                x, y = x + op[1], y + op[2]
            else:
                x, y = x * op[1], y * op[2]
        return x, y

    def bbox(self, b: list[float]) -> list[float]:
        pts = [self.point(x, y) for x in (b[0], b[2]) for y in (b[1], b[3])]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return [round(min(xs), 1), round(min(ys), 1), round(max(xs), 1), round(max(ys), 1)]


def augment(img: Image.Image, rng: random.Random, preset: str | None = None,
            with_transform: bool = False):
    """증강 이미지와 preset 이름. with_transform=True 면 좌표 변환(Transform)도 함께 돌려준다."""
    preset = preset or rng.choice(PRESETS)
    img = img.convert("RGB")
    w, h = img.size
    tf = Transform()

    if preset == "scan":
        angle = rng.uniform(-1.5, 1.5)
        img = img.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=(255, 255, 255))
        tf.rotate(angle, w, h, img.width, img.height)
        img = ImageEnhance.Brightness(img).enhance(rng.uniform(0.9, 1.05))
        img = ImageEnhance.Contrast(img).enhance(rng.uniform(0.85, 1.2))
        tint = Image.new("RGB", img.size, rng.choice([(255, 252, 240), (245, 245, 245), (250, 248, 235)]))
        img = ImageChops.multiply(img, tint)
        img = img.filter(ImageFilter.GaussianBlur(rng.uniform(0.2, 0.8)))
        img = _noise(img, rng, rng.uniform(2, 6))
    elif preset == "photo":
        angle = rng.uniform(-6, 6)
        doc = img.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=(0, 0, 0))
        tf.rotate(angle, w, h, doc.width, doc.height)
        mask = Image.new("L", img.size, 255).rotate(angle, expand=True, fillcolor=0)
        pad = int(max(w, h) * rng.uniform(0.04, 0.12))
        canvas = _background(rng, (doc.width + pad * 2, doc.height + pad * 2))
        off = (pad + rng.randint(-pad // 2, pad // 2), pad + rng.randint(-pad // 2, pad // 2))
        canvas.paste(doc, off, mask)
        tf.shift(*off)
        img = canvas
        # 조명 그라데이션
        diag = int((img.width ** 2 + img.height ** 2) ** 0.5) + 2
        grad = Image.linear_gradient("L").resize((diag, diag)).rotate(rng.uniform(0, 360), resample=Image.BILINEAR)
        left, top = (diag - img.width) // 2, (diag - img.height) // 2
        grad = grad.crop((left, top, left + img.width, top + img.height))
        shade = ImageOps.colorize(grad, black=(rng.randint(150, 200),) * 3, white=(255, 255, 255))
        img = ImageChops.multiply(img, shade)
        img = ImageEnhance.Color(img).enhance(rng.uniform(0.8, 1.1))
        img = img.filter(ImageFilter.GaussianBlur(rng.uniform(0.4, 1.2)))
        img = _noise(img, rng, rng.uniform(4, 10))
        scale = rng.uniform(0.55, 0.85)
        nw, nh = int(img.width * scale), int(img.height * scale)
        tf.scale(nw / img.width, nh / img.height)
        img = img.resize((nw, nh), Image.BILINEAR)
    elif preset == "fax":
        g = img.convert("L").filter(ImageFilter.GaussianBlur(rng.uniform(0.3, 0.7)))
        thr = rng.randint(150, 200)
        img = g.point(lambda v: 255 if v > thr else 0).convert("RGB")
        small = img.resize((int(w * 0.6), int(h * 0.6)), Image.NEAREST)
        img = small.resize((w, h), Image.NEAREST)
    # clean_jpeg: 압축만

    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=rng.randint(45, 85) if preset != "clean_jpeg" else rng.randint(70, 92))
    buf.seek(0)
    out = Image.open(buf).convert("RGB")
    return (out, preset, tf) if with_transform else (out, preset)
