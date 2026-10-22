"""② 표시 요소 화면의 서버 쪽: 확률 설정(docgen/marks.json)과 풀(docgen/assets/marks/pools.json, 이미지)을 읽고 쓴다.

생성기가 쓰는 규칙은 docgen/marks.py. 여기서는 형식만 검사하고 파일에 쓴다. API 는 studio/app.py (/api/marks…), 화면은 static/js/marks.js.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
from pathlib import Path

from docgen import marks as M

IMAGE_POOLS = ("check", "sign")
SEAL_SHAPES = ("circle", "square", "oval")


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
    """바꾼 값만 docgen/marks.json 에 쓴다 (기본값과 같으면 뺀다)."""
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


def upload(name: str, filename: str, data: bytes, label: str = "") -> dict:
    """체크·서명 풀에 투명 배경 PNG(또는 SVG)를 올린다."""
    if name not in IMAGE_POOLS:
        raise ValueError(f"이미지를 올릴 수 있는 풀: {IMAGE_POOLS}")
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
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
