"""Page views for training: resize to the model input size, optional geometric and
photometric augmentation. Every geometric step also moves the OCR boxes, so the
labels read from the clean original stay valid on the degraded image."""
import io
import math

from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps

# Paper / desk / scanner-bed colours used for padding and rotation fill.
BACKGROUNDS = [(255, 255, 255), (244, 241, 232), (228, 228, 226), (96, 96, 94), (168, 146, 116)]

DEFAULT_AUGMENT = {
    "crop_probability": 0.5, "crop_min_fraction": 0.7,
    "rotate_probability": 0.4, "max_rotation_degrees": 1.5,
    "pad_probability": 0.4, "max_pad_fraction": 0.06,
    "scale_range": [0.75, 1.0],
    "photometric_ops": [1, 3],
    "blur_radius": [0.3, 1.3], "jpeg_quality": [25, 70], "noise_sigma": [4, 18],
    "downsample": [0.45, 0.8], "contrast": [0.6, 1.3], "brightness": [0.75, 1.15],
    "shadow_strength": [0.15, 0.45], "fax_threshold": [140, 200],
}


def fit_scale(width, height, max_size):
    """Downscale factor so the long side <= max_size[0] and the short side <= max_size[1]."""
    long_limit, short_limit = max(max_size), min(max_size)
    long_side, short_side = max(width, height), min(width, height)
    return min(1.0, long_limit / long_side, short_limit / short_side)


def _rect(box):
    x1, y1, x2, y2 = box
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]


def _envelope(points):
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    return [min(xs), min(ys), max(xs), max(ys)]


def _crop(im, polys, rng, cfg):
    w, h = im.size
    cw = round(w * rng.uniform(cfg["crop_min_fraction"], 1))
    ch = round(h * rng.uniform(cfg["crop_min_fraction"], 1))
    x0, y0 = rng.randint(0, w - cw), rng.randint(0, h - ch)
    # Clip now: later padding would otherwise bring cropped-away words back onto the canvas.
    kept, fractions = [], []
    for p in polys:
        x1, y1, x2, y2 = _envelope([(x - x0, y - y0) for x, y in p])
        c = [max(0, x1), max(0, y1), min(cw, x2), min(ch, y2)]
        inside = max(0, c[2] - c[0]) * max(0, c[3] - c[1]) / max((x2 - x1) * (y2 - y1), 1e-9)
        fractions.append(inside)
        kept.append(_rect(c) if inside > 0 else _rect([0, 0, 0, 0]))
    return im.crop((x0, y0, x0 + cw, y0 + ch)), kept, fractions, f"crop{cw}x{ch}"


def rotate(im, polys, angle, fill):
    """PIL rotates counter-clockwise; map points with the same rotation about the centre."""
    w, h = im.size
    out = im.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=fill)
    nw, nh = out.size
    t = math.radians(angle)
    c, s = math.cos(t), math.sin(t)
    def move(x, y):
        dx, dy = x - w / 2, y - h / 2
        return (dx * c + dy * s + nw / 2, -dx * s + dy * c + nh / 2)
    return out, [[move(x, y) for x, y in p] for p in polys]


def _pad(im, polys, rng, cfg, fill):
    w, h = im.size
    l, r = (round(w * rng.uniform(0, cfg["max_pad_fraction"])) for _ in range(2))
    t, b = (round(h * rng.uniform(0, cfg["max_pad_fraction"])) for _ in range(2))
    out = Image.new("RGB", (w + l + r, h + t + b), fill)
    out.paste(im, (l, t))
    return out, [[(x + l, y + t) for x, y in p] for p in polys]


def _shadow(im, strength, rng):
    """Linear illumination falloff from one side, as in a phone photo or a curled page."""
    w, h = im.size
    ramp = Image.linear_gradient("L").resize((w, h))
    ramp = ramp.rotate(rng.choice([0, 90, 180, 270]), expand=False).resize((w, h))
    dark = ImageEnhance.Brightness(im).enhance(1 - strength)
    return Image.composite(im, dark, ramp)


def photometric(im, rng, cfg):
    ops = ["blur", "motion", "jpeg", "noise", "downsample", "contrast", "shadow", "fax", "gray"]
    count = rng.randint(*cfg["photometric_ops"])
    applied = []
    for op in rng.sample(ops, count):
        if op == "blur":
            im = im.filter(ImageFilter.GaussianBlur(rng.uniform(*cfg["blur_radius"])))
        elif op == "motion":
            horizontal = rng.random() < 0.5
            kernel = [0] * 25
            for i in range(5):
                kernel[(2 * 5 + i) if horizontal else (i * 5 + 2)] = 1
            im = im.filter(ImageFilter.Kernel((5, 5), kernel, scale=5))
        elif op == "jpeg":
            buffer = io.BytesIO()
            im.save(buffer, "JPEG", quality=rng.randint(*cfg["jpeg_quality"]))
            buffer.seek(0)
            im = Image.open(buffer).convert("RGB")
        elif op == "noise":
            noise = Image.effect_noise(im.size, rng.uniform(*cfg["noise_sigma"]))
            # effect_noise is centred on 128; add its deviation to every band.
            im = Image.merge("RGB", [ImageChops.add(band, noise, scale=1, offset=-128) for band in im.split()])
        elif op == "downsample":
            w, h = im.size
            f = rng.uniform(*cfg["downsample"])
            im = im.resize((max(1, round(w * f)), max(1, round(h * f))), Image.BILINEAR).resize((w, h), Image.BILINEAR)
        elif op == "contrast":
            im = ImageEnhance.Contrast(im).enhance(rng.uniform(*cfg["contrast"]))
            im = ImageEnhance.Brightness(im).enhance(rng.uniform(*cfg["brightness"]))
        elif op == "shadow":
            im = _shadow(im, rng.uniform(*cfg["shadow_strength"]), rng)
        elif op == "fax":
            threshold = rng.randint(*cfg["fax_threshold"])
            im = ImageOps.grayscale(im).point(lambda v: 255 if v > threshold else 0).convert("RGB")
        else:
            im = ImageOps.grayscale(im).convert("RGB")
        applied.append(op)
    return im, applied


def make_view(page, boxes, rng, max_size, augment=None):
    """Return (image, envelopes, visible, ops). envelopes are pixel [x1,y1,x2,y2] of each input
    box after every geometric step; visible is the fraction of each box that survived cropping."""
    polys = [_rect(b) for b in boxes]
    visible = [1.0] * len(boxes)
    im, ops = page, []
    if augment is not None:
        cfg = {**DEFAULT_AUGMENT, **augment}
        fill = rng.choice(BACKGROUNDS)
        if rng.random() < cfg["crop_probability"]:
            im, polys, visible, op = _crop(im, polys, rng, cfg)
            ops.append(op)
        if rng.random() < cfg["rotate_probability"]:
            angle = rng.uniform(-cfg["max_rotation_degrees"], cfg["max_rotation_degrees"])
            im, polys = rotate(im, polys, angle, fill)
            ops.append(f"rotate{angle:+.2f}")
        if rng.random() < cfg["pad_probability"]:
            im, polys = _pad(im, polys, rng, cfg, fill)
            ops.append("pad")
        scale = fit_scale(*im.size, max_size) * rng.uniform(*cfg["scale_range"])
    else:
        scale = fit_scale(*im.size, max_size)
    if scale != 1:
        w, h = im.size
        nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
        im = im.resize((nw, nh), Image.LANCZOS)
        sx, sy = nw / w, nh / h
        polys = [[(x * sx, y * sy) for x, y in p] for p in polys]
        ops.append(f"scale{scale:.3f}")
    if augment is not None:
        im, applied = photometric(im, rng, cfg)
        ops.extend(applied)
    return im.convert("RGB"), [_envelope(p) for p in polys], visible, ops
