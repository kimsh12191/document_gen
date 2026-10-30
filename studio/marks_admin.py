"""② 표시 요소 화면의 서버 쪽: 확률 설정(docgen/forms/_common/marks.json)과 풀(docgen/assets/marks/pools.json, 이미지)을 읽고 쓴다.

생성기가 쓰는 규칙은 docgen/marks.py. 여기서는 형식만 검사하고 파일에 쓴다. API 는 studio/app.py (/api/marks…), 화면은 static/js/marks.js.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
from pathlib import Path

from docgen import marks as M

IMAGE_POOLS = ("check", "sign", "seal")
SEAL_SHAPES = ("circle", "square", "oval")
PHOTO_EXTS = ("jpg", "jpeg", "webp")   # 도장 풀만: 사진도 받아 clean_seal 로 배경을 지운다


def view() -> dict:
    saved = json.loads(M.SETTINGS.read_text(encoding="utf-8")) if M.SETTINGS.exists() else {}
    pools = M.pools()
    for name, items in pools.items():
        for it in items:
            it["url"] = f"/marks-img/{it['file']}" if it.get("file") else None
            if name in ("hand_fonts", "print_fonts"):   # 화면 미리보기용 글꼴 주소 (설치된 인쇄체는 None)
                ff = M.font_file(name, it)
                it["face"] = f"/fonts/{ff}" if ff else None
    return {"settings": M.settings(), "saved": saved, "defaults": M.DEFAULTS, "pools": pools, "names": M.POOL_NAMES,
            "image_pools": IMAGE_POOLS, "seal_shapes": SEAL_SHAPES}


def _prob(v, where):
    if not isinstance(v, (int, float)) or not 0 <= v <= 1:
        raise ValueError(f"{where}: 0~1 사이 숫자")
    return float(v)


def save_settings(new: dict) -> dict:
    """바꾼 값만 docgen/forms/_common/marks.json 에 쓴다 (기본값과 같으면 뺀다)."""
    out = {}
    for k, dv in M.DEFAULTS.items():
        if k not in new:
            continue
        if isinstance(dv, dict):
            sub = {kk: _prob(new[k][kk], f"{k}.{kk}") for kk in dv if kk in new[k] and new[k][kk] != dv[kk]}
            if sub:
                out[k] = sub
        elif new[k] != dv:
            out[k] = _prob(new[k], k)
    for k in ("sign_spot", "seal_spot"):
        s = M._merge(M.DEFAULTS[k], out.get(k, {}))
        if s["seal_below"] > s["sign_below"]:
            raise ValueError(f"{k}: 도장 비율이 도장+서명 비율보다 클 수 없습니다")
    if out:
        M.SETTINGS.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    elif M.SETTINGS.exists():
        M.SETTINGS.unlink()
    return view()


def _write_pools(pools: dict) -> None:
    keep = {}
    for name, items in pools.items():
        clean = [{k: v for k, v in it.items() if k not in ("url", "face")} for it in items]
        if clean != M.DEFAULT_POOLS[name]:
            keep[name] = clean
    M.POOLS_DIR.mkdir(parents=True, exist_ok=True)
    if keep:
        M.POOLS.write_text(json.dumps(keep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    elif M.POOLS.exists():
        M.POOLS.unlink()


def save_pool(name: str, items: list[dict]) -> dict:
    if name not in M.DEFAULT_POOLS:
        raise KeyError(name)
    old = {it["id"]: it for it in M.pools()[name]}
    out = []
    for it in items:
        if not isinstance(it.get("id"), str) or not it["id"]:
            raise ValueError("항목마다 id 가 필요합니다")
        base = dict(old.get(it["id"]) or it)   # 새 항목(add_font·add_seal_template)은 id·origin 까지 그대로
        base.update({k: v for k, v in it.items() if k in ("name", "weight", "enabled", "kind", "scale", "shape", "border",
                                                          "double", "font", "ink")})
        if "weight" in base and (not isinstance(base["weight"], int) or not 0 <= base["weight"] <= 100):
            raise ValueError(f"{it['id']}: 가중치는 0~100 정수")
        if name == "seal" and not base.get("builtin"):
            if base.get("shape", "circle") not in SEAL_SHAPES:
                raise ValueError(f"{it['id']}: 도장 모양은 {SEAL_SHAPES}")
            if base.get("ink") and not re.fullmatch(r"#[0-9a-fA-F]{3,8}", base["ink"]):
                raise ValueError(f"{it['id']}: 인주 색은 #rrggbb")
        if name in ("hand_fonts", "print_fonts") and not re.fullmatch(r"[\w' -]+", base["id"]):
            raise ValueError(f"{it['id']}: 글꼴 이름에 쓸 수 없는 글자")
        ff = M.font_file(name, base) if name in ("hand_fonts", "print_fonts") else None
        if ff and not (M.FONTS_DIR / ff).exists():
            raise ValueError(f"{it['id']}: docgen/fonts/{ff} 가 없습니다 (글꼴 파일이 있는 경로로 다시 추가)")
        out.append(base)
    pools = M.pools()
    pools[name] = out
    _write_pools(pools)
    return view()


def add_font(pool: str, font_id: str, scale: float = 1.0) -> dict:
    """글꼴 추가. font_id 가 studio 서버에서 보이는 파일·폴더 경로면 그 안의 글꼴 파일(.ttf .otf .woff .woff2, 하위 폴더 포함)을
    docgen/fonts/ 로 복사해 모두 등록한다. 경로가 아니면 예전처럼 이름 하나 (손글씨: docgen/fonts/<이름>.woff2, 인쇄체: 설치된 글꼴)."""
    if pool not in ("hand_fonts", "print_fonts"):
        raise ValueError("글꼴 풀은 hand_fonts / print_fonts")
    p = Path(font_id.strip().strip('"')).expanduser()
    if font_id.strip() and p.exists():
        return _add_font_files(pool, p, scale)
    pools = M.pools()
    if any(x["id"] == font_id for x in pools[pool]):
        raise ValueError("이미 있는 글꼴")
    item = {"id": font_id, "weight": 1, "origin": "added"}
    if pool == "hand_fonts":
        item["scale"] = float(scale)
    return save_pool(pool, pools[pool] + [item])


def _add_font_files(pool: str, p: Path, scale: float) -> dict:
    files = [p] if p.is_file() else sorted(f for f in p.rglob("*") if f.is_file())
    files = [f for f in files if f.suffix.lower() in M.FONT_EXTS]
    if not files:
        raise ValueError(f"{p} 에 글꼴 파일(.ttf .otf .woff .woff2)이 없습니다")
    pools = M.pools()
    have = {M.font_file(pool, x) for x in pools[pool]}
    added, skipped = [], []
    M.FONTS_DIR.mkdir(parents=True, exist_ok=True)
    for f in files:
        data = f.read_bytes()
        ext = f.suffix.lower()
        # 글꼴 이름 = 파일 이름의 영문·숫자 (한글 이름이면 내용 해시). 렌더러 주소·CSS 에 그대로 쓴다
        stem = re.sub(r"[^A-Za-z0-9]", "", f.stem) or "Font" + hashlib.sha1(data).hexdigest()[:8]
        fid, n = stem, 1
        while (M.FONTS_DIR / f"{fid}{ext}").exists() and (M.FONTS_DIR / f"{fid}{ext}").read_bytes() != data:
            n += 1
            fid = f"{stem}{n}"
        fname = f"{fid}{ext}"
        if fname in have:
            skipped.append(f.name)
            continue
        (M.FONTS_DIR / fname).write_bytes(data)
        item = {"id": fid if pool == "hand_fonts" else f"'{fid}'", "name": f.name, "font_file": fname,
                "weight": 1, "origin": "added"}
        if pool == "hand_fonts":
            item["scale"] = float(scale)
        pools[pool].append(item)
        have.add(fname)
        added.append(f.name)
    if added:
        _write_pools(pools)
    return {**view(), "added": added, "skipped": skipped}


def add_seal_template(t: dict) -> dict:
    pools = M.pools()
    sid = "seal_" + hashlib.sha1(json.dumps(t, sort_keys=True).encode()).hexdigest()[:8]
    item = {"id": sid, "name": t.get("name") or "도장 틀", "weight": 1, "shape": t.get("shape", "circle"),
            "border": t.get("border"), "double": bool(t.get("double")), "font": t.get("font"), "ink": t.get("ink"),
            "origin": "template"}
    return save_pool("seal", pools["seal"] + [{k: v for k, v in item.items() if v not in (None, "")}])


def _percentile(im, q: float, mask=None) -> int:
    hist, acc = im.histogram(mask), 0
    total = sum(hist)
    for v, c in enumerate(hist):
        acc += c
        if acc >= total * q:
            return v
    return 255


def clean_seal(data: bytes) -> bytes:
    """도장 사진 → 배경을 지우고 인주만 남겨 도장 둘레로 자른 투명 PNG.

    - 이미 투명 배경인 PNG 는 그대로 두고 자르기·줄이기만 한다.
    - 붉은 인주가 보이면 '빨강 정도(R - max(G, B))', 아니면(검정·파랑 도장) 배경보다 어두운 정도로 인주를 고른다.
    - 인주 색은 진하게 찍힌 칸의 평균 한 가지로 칠한다 (가장자리에 섞인 종이색이 남지 않게).
    """
    from PIL import Image, ImageChops, ImageFilter, ImageOps, ImageStat

    try:
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(data)))
        im.load()
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"이미지를 읽을 수 없습니다: {e}") from e
    im = im.convert("RGBA")
    im.thumbnail((1200, 1200))
    if max(im.size) < 600:   # 작게 찍힌 도장: 키운 뒤 처리해야 잡티 필터가 가는 획을 지우지 않는다
        k = 600 / max(im.size)
        im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    alpha = im.getchannel("A")
    if alpha.getextrema()[0] < 128 and ImageStat.Stat(alpha).mean[0] < 230:   # 이미 투명 배경
        out = im
    else:
        rgb = im.convert("RGB")
        r, g, b = rgb.split()
        red = ImageChops.subtract(r, ImageChops.lighter(g, b))
        noise, peak = _percentile(red, 0.5), _percentile(red, 0.99)   # 종이·배경의 빨강 정도, 인주의 빨강 정도
        if peak - noise >= 18:   # 흐린 분홍 인주도 잡히게 사진마다 문턱을 정한다
            # JPEG 는 색을 밝기보다 거칠게 저장한다: 색으로는 '인주가 있는 곳'만 정하고, 획 모양은 밝기(제 해상도)로 잡는다
            near = red.point(lambda v: 255 if v > noise + (peak - noise) * 0.3 else 0).filter(ImageFilter.MaxFilter(9))
            dark = ImageOps.invert(rgb.convert("L"))
            sure = red.point(lambda v: 255 if v > noise + (peak - noise) * 0.5 else 0)   # 확실히 인주인 칸
            paper, inked = _percentile(dark, 0.2, near), _percentile(dark, 0.9, sure)
            if inked - paper < 12:
                score, lo, hi = red, noise + (peak - noise) * 0.15, noise + (peak - noise) * 0.6
            else:
                # 인주보다 훨씬 어두운 칸은 종이 밖 배경·검은 인쇄 글자 → 뺀다
                cut = inked + max(30, (inked - paper) // 2)
                score = ImageChops.multiply(dark.point(lambda v: 0 if v > cut else v), near)
                lo, hi = paper + (inked - paper) * 0.2, paper + (inked - paper) * 0.7
        else:
            dark = ImageOps.invert(rgb.convert("L"))
            w, h = dark.size
            edge = [dark.getpixel((x, y)) for x in range(0, w, max(1, w // 40)) for y in (0, h - 1)]
            bg = sorted(edge)[len(edge) // 2]   # 테두리 중앙값 = 종이 어둡기
            score, lo, hi = dark, bg + 30, bg + 120
        a = score.point(lambda v: 0 if v <= lo else 255 if v >= hi else int((v - lo) * 255 / (hi - lo)))
        a = a.filter(ImageFilter.MedianFilter(3))   # 종이 얼룩·잡티
        solid = a.point(lambda v: 255 if v >= 200 else 0)
        if not solid.getbbox():
            raise ValueError("도장(인주)을 찾지 못했습니다. 도장이 크게 나오게 찍은 사진을 올려 주세요")
        ink = tuple(int(c) for c in ImageStat.Stat(rgb, solid).mean)
        out = Image.new("RGBA", rgb.size, ink + (255,))
        out.putalpha(a)
    box = out.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox()
    if not box:
        raise ValueError("도장(인주)을 찾지 못했습니다")
    pad = max(2, int(max(box[2] - box[0], box[3] - box[1]) * 0.04))
    out = out.crop((max(0, box[0] - pad), max(0, box[1] - pad), min(out.width, box[2] + pad), min(out.height, box[3] + pad)))
    out.thumbnail((320, 320))
    buf = io.BytesIO()
    out.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def upload(name: str, filename: str, data: bytes, label: str = "") -> dict:
    """체크·서명 풀에 투명 배경 PNG(또는 SVG)를 올린다. 도장 풀은 사진(JPG·PNG·WEBP)도 받아 clean_seal 로 처리한다."""
    if name not in IMAGE_POOLS:
        raise ValueError(f"이미지를 올릴 수 있는 풀: {IMAGE_POOLS}")
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if len(data) > 20_000_000:
        raise ValueError("20MB 이하 이미지만")
    if name == "seal" and ext in PHOTO_EXTS + ("png",):
        data, ext = clean_seal(data), "png"
    if ext == "svg":
        head = data[:200].decode("utf-8", "ignore").lstrip()
        if not (head.startswith("<svg") or head.startswith("<?xml")):
            raise ValueError("SVG 파일이 아닙니다")
    elif ext == "png":
        from PIL import Image

        try:
            im = Image.open(io.BytesIO(data))
            im.verify()
        except Exception as e:  # noqa: BLE001
            raise ValueError(f"PNG 를 읽을 수 없습니다: {e}") from e
    else:
        raise ValueError("PNG 또는 SVG 만 올릴 수 있습니다")
    if len(data) > 2_000_000:
        raise ValueError("2MB 이하 이미지만")
    h = hashlib.sha1(data).hexdigest()[:10]
    rel = f"{name}/{name}_{h}.{ext}"
    dest = M.POOLS_DIR / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    pools = M.pools()
    if not any(it.get("file") == rel for it in pools[name]):
        pools[name].append({"id": f"{name}_{h}", "name": label or filename, "file": rel, "weight": 1, "origin": "upload"})
        _write_pools(pools)
    return view()


def delete_item(name: str, item_id: str) -> dict:
    pools = M.pools()
    items = pools.get(name)
    if items is None:
        raise KeyError(name)
    it = next((x for x in items if x["id"] == item_id), None)
    if it is None:
        raise KeyError(item_id)
    if it.get("builtin"):
        raise ValueError("코드가 그리는 기본 항목은 지우지 않고 끕니다 (가중치 0 또는 끄기)")
    pools[name] = [x for x in items if x["id"] != item_id]
    _write_pools(pools)
    if it.get("file") and not any(x.get("file") == it["file"] for x in pools[name]):
        (M.POOLS_DIR / it["file"]).unlink(missing_ok=True)
    ff = it.get("font_file")   # 경로로 등록하며 복사한 글꼴 파일 (다른 풀에서도 안 쓰면 지운다)
    if ff and not any(x.get("font_file") == ff for items in pools.values() for x in items):
        (M.FONTS_DIR / ff).unlink(missing_ok=True)
    return view()
