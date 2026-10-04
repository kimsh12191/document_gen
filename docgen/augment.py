"""스캔/촬영 느낌의 이미지 증강 (Pillow 만 사용).

깨끗한 렌더링 이미지만으로 학습하면 실제 스캔본·폰카 사진에서 성능이 떨어지므로,
기울기·배경·밝기·흐림·노이즈·JPEG 압축을 무작위로 섞는다. 텍스트 내용은 바뀌지 않으므로
정답(GT)은 원본과 동일하게 쓴다.
"""
from __future__ import annotations

import io
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


def augment(img: Image.Image, rng: random.Random, preset: str | None = None) -> tuple[Image.Image, str]:
    preset = preset or rng.choice(PRESETS)
    img = img.convert("RGB")
    w, h = img.size

    if preset == "scan":
        img = img.rotate(rng.uniform(-1.5, 1.5), resample=Image.BICUBIC, expand=True, fillcolor=(255, 255, 255))
        img = ImageEnhance.Brightness(img).enhance(rng.uniform(0.9, 1.05))
        img = ImageEnhance.Contrast(img).enhance(rng.uniform(0.85, 1.2))
        tint = Image.new("RGB", img.size, rng.choice([(255, 252, 240), (245, 245, 245), (250, 248, 235)]))
        img = ImageChops.multiply(img, tint)
        img = img.filter(ImageFilter.GaussianBlur(rng.uniform(0.2, 0.8)))
        img = _noise(img, rng, rng.uniform(2, 6))
    elif preset == "photo":
        angle = rng.uniform(-6, 6)
        doc = img.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=(0, 0, 0))
        mask = Image.new("L", img.size, 255).rotate(angle, expand=True, fillcolor=0)
        pad = int(max(w, h) * rng.uniform(0.04, 0.12))
        canvas = _background(rng, (doc.width + pad * 2, doc.height + pad * 2))
        canvas.paste(doc, (pad + rng.randint(-pad // 2, pad // 2), pad + rng.randint(-pad // 2, pad // 2)), mask)
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
        img = img.resize((int(img.width * scale), int(img.height * scale)), Image.BILINEAR)
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
    return Image.open(buf).convert("RGB"), preset
