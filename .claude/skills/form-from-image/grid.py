"""원본 그림을 재는 도구 (form-from-image 스킬 1·2단계). 글자는 읽지 않는다 — 선·칸·글자 덩어리의 **자리**만 잰다.

    python .claude/skills/form-from-image/grid.py <초안 폴더>            # 쪽마다 기울기 바로잡기 → 표·칸·글자 덩어리 재기
    python .claude/skills/form-from-image/grid.py <초안 폴더> --page 2   # 한 쪽만

단위는 **쪽 px**: 쪽 가로를 794 로 놓은 자리 (html 서식의 px 과 같다. A4 세로는 1123).

결과 (초안 폴더):
  page_<n>.png   기울기를 바로잡고 가로 1588(=794×2)로 맞춘 원본. view.py 가 이것을 자른다
  grid_<n>.json  표(열 경계 x · 행 경계 y · 칸과 합친 칸) · 표 밖 선 · 표 밖 글자 덩어리 · 칸마다 글자 자리
  화면에는 같은 내용을 글로 (모델이 읽는 꼴)

칸 이름: T<표>.<번호> (예: T2.7). 글자 덩어리: B<번호>. 쪽이 둘 이상이면 앞에 쪽 번호 (2:T1.3).
쓰는 것: Pillow 만 (numpy·OpenCV 없이 돈다).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

PAGE_W = 794            # 쪽 px 가로
S = 2                   # 작업 그림 = 쪽 px × 2
WORK_W = PAGE_W * S
LONG = 30 * S           # 이만큼 길면 혼자서도 선
SHORT = 7 * S           # 이보다 짧으면 선 아님. 사이 길이는 양 끝이 다른 방향 선에 닿을 때만 선
GAP = 2                 # 선 안의 끊김 메우기 — 크면 글자 획이 이어져 선이 된다
THICK = 7 * S           # 이보다 두꺼우면 선이 아니라 칠한 덩어리
TOL = 4 * S             # 같은 선으로 볼 거리


# ---------------------------------------------------------------- 그림 준비

def sources(draft: Path) -> list[Path]:
    first = draft / "source.png"
    rest = sorted(draft.glob("source_*.png"), key=lambda p: int(re.sub(r"\D", "", p.stem) or 0))
    return ([first] if first.exists() else []) + rest


def otsu(gray: Image.Image) -> int:
    h = gray.histogram()
    total = sum(h)
    sum_all = sum(i * c for i, c in enumerate(h))
    best, thr, w0, s0 = -1.0, 128, 0, 0
    for t in range(256):
        w0 += h[t]
        if w0 == 0:
            continue
        w1 = total - w0
        if w1 == 0:
            break
        s0 += t * h[t]
        m0, m1 = s0 / w0, (sum_all - s0) / w1
        var = w0 * w1 * (m0 - m1) ** 2
        if var > best:
            best, thr = var, t
    return thr


def binary(gray: Image.Image, thr: int | None = None) -> Image.Image:
    """글자·선 = 1, 바탕 = 0 (mode L)."""
    t = thr if thr is not None else min(max(otsu(gray), 140), 200)
    return gray.point(lambda v: 1 if v < t else 0)


def skew_angle(gray: Image.Image) -> float:
    """가로선이 가장 또렷해지는 기울기 (도). 줄마다 검은 비율의 제곱합이 가장 큰 각."""
    small = gray.copy()
    small.thumbnail((900, 1300))
    inv = ImageOps.invert(small)
    h = inv.size[1]

    def score(a: float) -> float:
        r = inv.rotate(a, resample=Image.BILINEAR, fillcolor=0)
        col = r.resize((1, h), Image.BOX).tobytes()
        return sum(v * v for v in col)

    best = max((score(a / 10), a / 10) for a in range(-30, 31))[1]
    fine = max((score(best + d / 100), best + d / 100) for d in range(-10, 11))[1]
    return round(fine, 2)


def prepare(src: Path, dest: Path) -> dict:
    im = ImageOps.exif_transpose(Image.open(src)).convert("L")
    src_w = im.size[0]
    angle = skew_angle(im)
    if abs(angle) >= 0.05:
        im = im.rotate(angle, resample=Image.BICUBIC, fillcolor=255, expand=False)
    h = round(im.size[1] * WORK_W / im.size[0])
    im = im.resize((WORK_W, h), Image.LANCZOS)
    im.save(dest, optimize=True)
    return {"angle": angle, "size": [PAGE_W, round(h / S)], "upscale": WORK_W / src_w}


# ---------------------------------------------------------------- 선 찾기

PIECE = 4                # 끊긴 선을 찾을 때 쓰는 조각의 최소 길이
CHAIN = 9 * S            # 끊긴 선: 조각 사이 틈이 이만큼까지면 한 선


def row_runs(data: bytes, w: int, h: int, gap: int, minlen: int) -> list[list[tuple[int, int]]]:
    fill = re.compile(rb"(?<=\x01)\x00{1,%d}(?=\x01)" % gap)
    run = re.compile(rb"\x01{%d,}" % minlen)
    out = []
    for y in range(h):
        row = data[y * w:(y + 1) * w]
        if b"\x01" not in row:
            out.append([])
            continue
        row = fill.sub(lambda m: b"\x01" * len(m.group()), row)
        out.append([(m.start(), m.end()) for m in run.finditer(row)])
    return out


def track(runs: list[list[tuple[int, int]]], same) -> list[dict]:
    """줄마다 찾은 검은 줄을 위아래로 이어 두께가 있는 선으로. same(run, line) 이 참이면 같은 선."""
    open_, done = [], []
    for y, rr in enumerate(runs):
        still, used = [], set()
        for ln in open_:
            hit = next((i for i, r in enumerate(rr) if i not in used and same(r, ln)), None)
            if hit is None:
                (done if y - ln["y1"] > 1 else still).append(ln)
                continue
            used.add(hit)
            a, b = rr[hit]
            ln["a"], ln["b"], ln["y1"] = min(a, ln["a"]), max(b, ln["b"]), y
            ln["sum"] += y
            ln["n"] += 1
            still.append(ln)
        still += [{"a": a, "b": b, "y0": y, "y1": y, "sum": y, "n": 1} for i, (a, b) in enumerate(rr) if i not in used]
        open_ = still
    return done + open_


def overlap(r, ln) -> float:
    return min(r[1], ln["b"]) - max(r[0], ln["a"])


def segments(bin_img: Image.Image, vertical: bool, gap: int = GAP) -> list[dict]:
    """한 방향 선: {pos, a, b, thick} (px, 작업 그림). 가로면 pos=y, a..b=x."""
    img = bin_img.transpose(Image.TRANSPOSE) if vertical else bin_img
    w, h = img.size
    data = img.tobytes()

    def flat(lines):
        out = []
        for ln in lines:
            thick = ln["y1"] - ln["y0"] + 1
            if thick <= THICK and not crowded(img, ln):
                out.append({"pos": ln["sum"] / ln["n"], "a": ln["a"], "b": ln["b"], "thick": thick, "ink": ln["b"] - ln["a"]})
        return out

    solid = merge_colinear(flat(track(row_runs(data, w, h, gap, SHORT),
                                      lambda r, ln: overlap(r, ln) > 0.5 * min(r[1] - r[0], ln["b"] - ln["a"]))))
    return solid


def lonely(img: Image.Image, ln: dict) -> bool:
    """선 바로 위·아래(3~6px) 줄이 양쪽 다 거의 비었나."""
    a, b = int(ln["a"]), int(ln["b"])
    for sign in (-1, 1):
        total = dark = 0
        for d in (3, 4, 6):
            y = int(ln["pos"]) + sign * (d + ln["thick"] // 2)
            if 0 <= y < img.size[1]:
                row = img.crop((a, y, b, y + 1)).tobytes()
                total += len(row)
                dark += row.count(1)
        if total and dark / total > 0.1:
            return False
    return True


def crowded(img: Image.Image, ln: dict) -> bool:
    """선 바로 위아래 줄이 함께 검으면(글자 획이 이어진 것) 선이 아니다."""
    a, b = int(ln["a"]), int(ln["b"])
    up, down = ln["y0"] - 2, ln["y1"] + 2
    if up < 0 or down >= img.size[1] or b - a < 4:
        return False
    above = img.crop((a, up, b, up + 1)).tobytes()
    below = img.crop((a, down, b, down + 1)).tobytes()
    both = sum(1 for x, y in zip(above, below) if x and y)
    either = sum(1 for x, y in zip(above, below) if x or y)
    return both > 0.25 * (b - a) or either > 0.6 * (b - a)


def chain(lines: list[dict], gap: int) -> list[dict]:
    """같은 자리(±2px) 조각을 왼쪽부터 이어 붙인다. 틈이 gap 이하면 한 선. ink = 실제로 검은 길이."""
    lines = sorted(lines, key=lambda l: l["pos"])
    groups: list[list[dict]] = []
    for ln in lines:
        if groups and ln["pos"] - groups[-1][-1]["pos"] <= 2:
            groups[-1].append(ln)
        else:
            groups.append([ln])
    out = []
    for g in groups:
        cur = None
        for ln in sorted(g, key=lambda l: l["a"]):
            if cur and ln["a"] <= cur["b"] + gap:
                cur["ink"] += max(0, ln["b"] - max(ln["a"], cur["b"]))
                cur["b"] = max(cur["b"], ln["b"])
                cur["thick"] = max(cur["thick"], ln["thick"])
                cur["_p"].append(ln["pos"])
            else:
                if cur:
                    out.append(cur)
                cur = {**ln, "_p": [ln["pos"]]}
        if cur:
            out.append(cur)
    for ln in out:
        ln["pos"] = sum(ln["_p"]) / len(ln["_p"])
        del ln["_p"]
    return out


def merge_colinear(lines: list[dict]) -> list[dict]:
    out: list[dict] = []
    for ln in sorted(lines, key=lambda l: (l["pos"], l["a"])):
        for o in out:
            if abs(o["pos"] - ln["pos"]) <= 3 and ln["a"] <= o["b"] + 2 * GAP and ln["b"] >= o["a"] - 2 * GAP:
                o["a"], o["b"] = min(o["a"], ln["a"]), max(o["b"], ln["b"])
                o["thick"] = max(o["thick"], ln["thick"])
                break
        else:
            out.append(dict(ln))
    return out


def touches(end: float, pos: float, others: list[dict]) -> bool:
    """end(이 선 끝의 자리, 다른 방향 축)·pos(이 선의 자리)에 다른 방향 선이 지나가나."""
    return any(abs(o["pos"] - end) <= TOL and o["a"] - TOL <= pos <= o["b"] + TOL for o in others)


def keep_lines(hs: list[dict], vs: list[dict]) -> tuple[list[dict], list[dict]]:
    long_h = [l for l in hs if l["b"] - l["a"] >= LONG]
    long_v = [l for l in vs if l["b"] - l["a"] >= LONG]
    h2 = long_h + [l for l in hs if l["b"] - l["a"] < LONG and touches(l["a"], l["pos"], long_v) and touches(l["b"], l["pos"], long_v)]
    v2 = long_v + [l for l in vs if l["b"] - l["a"] < LONG and touches(l["a"], l["pos"], long_h) and touches(l["b"], l["pos"], long_h)]
    return h2, v2


# ---------------------------------------------------------------- 표 묶기

def crosses(h: dict, v: dict) -> bool:
    return h["a"] - TOL <= v["pos"] <= h["b"] + TOL and v["a"] - TOL <= h["pos"] <= v["b"] + TOL


def cluster(values: list[float], tol: float) -> list[float]:
    out: list[list[float]] = []
    for v in sorted(values):
        if out and v - out[-1][-1] <= tol:
            out[-1].append(v)
        else:
            out.append([v])
    return [sum(c) / len(c) for c in out]


def covered(lines: list[dict], pos: float, a: float, b: float) -> float:
    """pos 자리(±TOL) 선들이 a..b 를 덮는 비율."""
    spans = sorted((max(l["a"], a), min(l["b"], b)) for l in lines if abs(l["pos"] - pos) <= TOL and l["b"] > a and l["a"] < b)
    total, cur = 0.0, a
    for s, e in spans:
        s = max(s, cur)
        if e > s:
            total += e - s
            cur = e
    return total / max(b - a, 1)


def tables(hs: list[dict], vs: list[dict]) -> tuple[list[dict], list[dict]]:
    """선끼리 이어진 묶음 → 표. 표에 안 든 선은 따로."""
    items = [("h", l) for l in hs] + [("v", l) for l in vs]
    parent = list(range(len(items)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i, (ki, li) in enumerate(items):
        for j in range(i + 1, len(items)):
            kj, lj = items[j]
            if ki != kj and (crosses(li, lj) if ki == "h" else crosses(lj, li)):
                parent[find(i)] = find(j)
    groups: dict[int, list] = {}
    for i in range(len(items)):
        groups.setdefault(find(i), []).append(items[i])
    out, loose = [], []
    for g in groups.values():
        gh = [l for k, l in g if k == "h"]
        gv = [l for k, l in g if k == "v"]
        if len(gh) >= 2 and len(gv) >= 2:
            out.append(make_table(gh, gv))
        else:
            loose += [{"dir": k, **l} for k, l in g]
    out.sort(key=lambda t: (t["y0"], t["x0"]))
    return out, loose


def make_table(hs: list[dict], vs: list[dict]) -> dict:
    x0, x1 = min(l["a"] for l in hs), max(l["b"] for l in hs)
    y0, y1 = min(l["a"] for l in vs), max(l["b"] for l in vs)
    xs = cluster([l["pos"] for l in vs] + [x0, x1], TOL)
    ys = cluster([l["pos"] for l in hs] + [y0, y1], TOL)
    nr, nc = len(ys) - 1, len(xs) - 1
    vb = [[covered(vs, xs[j], ys[i], ys[i + 1]) >= 0.6 for j in range(nc + 1)] for i in range(nr)]
    hb = [[covered(hs, ys[i], xs[j], xs[j + 1]) >= 0.6 for j in range(nc)] for i in range(nr + 1)]
    parent = {(i, j): (i, j) for i in range(nr) for j in range(nc)}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in range(nr):
        for j in range(nc):
            if j + 1 < nc and not vb[i][j + 1]:
                parent[find((i, j))] = find((i, j + 1))
            if i + 1 < nr and not hb[i + 1][j]:
                parent[find((i, j))] = find((i + 1, j))
    regions: dict = {}
    for k in parent:
        regions.setdefault(find(k), []).append(k)
    cells = []
    for members in regions.values():
        r0, r1 = min(m[0] for m in members), max(m[0] for m in members)
        c0, c1 = min(m[1] for m in members), max(m[1] for m in members)
        if len(members) != (r1 - r0 + 1) * (c1 - c0 + 1):      # ㄱ자 같은 모양: 합치지 않고 한 칸씩
            cells += [{"r": i, "c": j, "rs": 1, "cs": 1, "odd": True} for i, j in members]
        else:
            cells.append({"r": r0, "c": c0, "rs": r1 - r0 + 1, "cs": c1 - c0 + 1})
    cells.sort(key=lambda c: (c["r"], c["c"]))
    for c in cells:
        c["box"] = [xs[c["c"]], ys[c["r"]], xs[c["c"] + c["cs"]], ys[c["r"] + c["rs"]]]
    return {"x0": xs[0], "y0": ys[0], "x1": xs[-1], "y1": ys[-1], "xs": xs, "ys": ys, "cells": cells,
            "open": {"left": not any(vb[i][0] for i in range(nr)), "right": not any(vb[i][nc] for i in range(nr)),
                     "top": not any(hb[0]), "bottom": not any(hb[nr])}}


# ---------------------------------------------------------------- 글자 자리 (읽지 않고 자리만)

def erase_lines(bin_img: Image.Image, hs: list[dict], vs: list[dict]) -> Image.Image:
    im = bin_img.copy()
    for l in hs:
        r = l["thick"] // 2 + 2
        im.paste(0, (int(l["a"]) - 1, int(l["pos"] - r), int(l["b"]) + 2, int(l["pos"] + r + 1)))
    for l in vs:
        r = l["thick"] // 2 + 2
        im.paste(0, (int(l["pos"] - r), int(l["a"]) - 1, int(l["pos"] + r + 1), int(l["b"]) + 2))
    return im


def projection(im: Image.Image, axis: str) -> bytes:
    """axis='y': 줄마다 검은 점이 있나(0/1 아님, 0..255 비율), 'x': 열마다."""
    w, h = im.size
    if w == 0 or h == 0:
        return b""
    scaled = im.point(lambda v: 255 if v else 0)
    return (scaled.resize((1, h), Image.BOX) if axis == "y" else scaled.resize((w, 1), Image.BOX)).tobytes()


def bands(prof: bytes, gap: int, min_len: int = 2) -> list[tuple[int, int]]:
    out, start, last = [], None, None
    for i, v in enumerate(prof):
        if v > 0:
            if start is None:
                start = i
            elif i - last > gap:
                if last - start + 1 >= min_len:
                    out.append((start, last + 1))
                start = i
            last = i
    if start is not None and last - start + 1 >= min_len:
        out.append((start, last + 1))
    return out


GLYPH = 0.9             # 글자 검은 부분 높이 ≈ 글자 크기 × 0.9 (렌더로 맞춘 값)


def ink(im: Image.Image, box: list[float]) -> dict | None:
    """칸 안 글자 자리: 검은 영역, 줄 수, 글자 크기 짐작, 정렬 짐작."""
    x0, y0, x1, y1 = (int(round(v)) for v in box)
    pad = 2 * S
    crop = im.crop((x0 + pad, y0 + pad, x1 - pad, y1 - pad))
    if crop.size[0] <= 2 or crop.size[1] <= 2 or crop.getbbox() is None:
        return None
    rows = bands(projection(crop, "y"), gap=3, min_len=2)            # 틈 3px 이하는 한 줄 (한 글자 안 자모 틈)
    rows = [r for r in rows if r[1] - r[0] >= 3]
    if not rows:
        return None
    bx = crop.getbbox()
    heights = sorted(r[1] - r[0] for r in rows)
    size = heights[len(heights) // 2] / S / GLYPH
    left = (bx[0]) / S
    right = (crop.size[0] - bx[2]) / S
    width = crop.size[0] / S
    align = "center" if abs(left - right) <= max(4, 0.08 * width) else ("left" if left < right else "right")
    return {"box": [round((x0 + pad + bx[0]) / S), round((y0 + pad + bx[1]) / S), round((x0 + pad + bx[2]) / S), round((y0 + pad + bx[3]) / S)],
            "lines": len(rows), "size": round(size, 1), "align": align}


def shade(gray: Image.Image, box: list[float]) -> int | None:
    """칸 바탕이 회색으로 칠해졌으면 그 밝기(0~255), 흰 바탕이면 None."""
    x0, y0, x1, y1 = (int(round(v)) for v in box)
    pad = 3 * S
    crop = gray.crop((x0 + pad, y0 + pad, x1 - pad, y1 - pad))
    if crop.size[0] < 4 or crop.size[1] < 4:
        return None
    h = crop.histogram()
    mode = max(range(128, 256), key=lambda v: h[v])
    return mode if mode < 240 else None


def text_blocks(im: Image.Image, table_boxes: list[list[float]]) -> list[dict]:
    """표 밖 글자 덩어리: 줄(가로띠)마다, 띄어 쓴 큰 틈으로 나눈 자리."""
    work = im.copy()
    for b in table_boxes:
        work.paste(0, (int(b[0]) - 2, int(b[1]) - 2, int(b[2]) + 3, int(b[3]) + 3))
    out = []
    for y0, y1 in bands(projection(work, "y"), gap=3, min_len=2):
        strip = work.crop((0, y0, work.size[0], y1))
        hgt = y1 - y0
        for x0, x1 in bands(projection(strip, "x"), gap=max(int(hgt * 1.6), 10 * S), min_len=2):
            piece = strip.crop((x0, 0, x1, hgt))
            bb = piece.getbbox()
            if not bb or (x1 - x0) * hgt < 30:          # 점 같은 티끌
                continue
            rows = bands(projection(piece.crop((0, bb[1], piece.size[0], bb[3])), "y"), gap=3, min_len=2) or [(0, bb[3] - bb[1])]
            hs = sorted(r[1] - r[0] for r in rows)
            out.append({"box": [round(x0 / S), round((y0 + bb[1]) / S), round(x1 / S), round((y0 + bb[3]) / S)],
                        "size": round(hs[len(hs) // 2] / S / GLYPH, 1), "n": len(rows)})
    # 위아래로 붙은 줄(같은 왼쪽, 줄 간격 좁음)은 한 덩어리로
    out.sort(key=lambda b: (b["box"][1], b["box"][0]))
    merged: list[dict] = []
    for b in out:
        for m in merged:
            mb = m["box"]
            if (abs(mb[0] - b["box"][0]) <= 6 and 0 <= b["box"][1] - mb[3] <= 0.8 * m["size"]
                    and abs(m["size"] - b["size"]) <= 0.25 * m["size"]):
                mb[1], mb[2], mb[3] = min(mb[1], b["box"][1]), max(mb[2], b["box"][2]), b["box"][3]
                m["lines"] += b.get("n", 1)
                break
        else:
            merged.append({**b, "lines": b.pop("n", 1)})
    return merged


# ---------------------------------------------------------------- 한 쪽 재기

def measure(work: Image.Image, upscale: float = 1.0) -> dict:
    """작업 그림(가로 1588) 하나 → 쪽 px 단위 결과. upscale: 원본 1px 이 작업 그림 몇 px 인지 (팩스처럼 거칠면 끊김도 크다)."""
    gray = work.convert("L")
    b = binary(gray)
    gap = GAP if upscale < 1.5 else 2 * GAP          # 원본이 작으면(크게 늘린 그림) 끊김도 크다
    hs, vs = keep_lines(segments(b, False, gap), segments(b, True, gap))
    tbls, loose = tables(hs, vs)
    erased = erase_lines(b, hs, vs)
    u = lambda v: round(v / S)  # noqa: E731
    out_tables = []
    for ti, t in enumerate(tbls, 1):
        cells = []
        for ci, c in enumerate(t["cells"], 1):
            cell = {"id": f"T{ti}.{ci}", "r": c["r"] + 1, "c": c["c"] + 1, "rs": c["rs"], "cs": c["cs"],
                    "box": [u(v) for v in c["box"]]}
            k = ink(erased, c["box"])
            if k:
                cell["ink"] = k
            sh = shade(gray, c["box"])
            if sh:
                cell["shade"] = sh
            if c.get("odd"):
                cell["odd"] = True
            cells.append(cell)
        out_tables.append({"id": f"T{ti}", "box": [u(t["x0"]), u(t["y0"]), u(t["x1"]), u(t["y1"])],
                           "xs": [u(v) for v in t["xs"]], "ys": [u(v) for v in t["ys"]],
                           "open": [k for k, v in t["open"].items() if v], "cells": cells})
    lines = [{"dir": l["dir"], "pos": u(l["pos"]), "from": u(l["a"]), "to": u(l["b"])} for l in loose
             if l["b"] - l["a"] >= LONG]
    lines, codes = barcodes(lines)
    blocks = text_blocks(erased, [[t["x0"], t["y0"], t["x1"], t["y1"]] for t in tbls])
    for i, bl in enumerate(blocks, 1):
        bl["id"] = f"B{i}"
    blocks = [bl for bl in blocks if not any(inside(bl["box"], c["box"]) for c in codes)]
    for i, bl in enumerate(blocks, 1):
        bl["id"] = f"B{i}"
    return {"size": [PAGE_W, round(work.size[1] / S)], "tables": out_tables, "lines": lines, "blocks": blocks, "barcodes": codes,
            "raw": {"h": [[u(l["pos"]), u(l["a"]), u(l["b"])] for l in hs], "v": [[u(l["pos"]), u(l["a"]), u(l["b"])] for l in vs]}}


def inside(a, b, tol=2) -> bool:
    return a[0] >= b[0] - tol and a[1] >= b[1] - tol and a[2] <= b[2] + tol and a[3] <= b[3] + tol


def barcodes(lines: list[dict]) -> tuple[list[dict], list[dict]]:
    """같은 높이의 세로선이 촘촘히 5개 넘게 늘어선 곳 = 바코드 (선 목록에서 빼고 자리만)."""
    vs = sorted((l for l in lines if l["dir"] == "v"), key=lambda l: l["pos"])
    groups, cur = [], []
    for l in vs:
        if cur and l["pos"] - cur[-1]["pos"] <= 20 and abs(l["from"] - cur[0]["from"]) <= 3 and abs(l["to"] - cur[0]["to"]) <= 3:
            cur.append(l)
        else:
            if len(cur) >= 5:
                groups.append(cur)
            cur = [l]
    if len(cur) >= 5:
        groups.append(cur)
    used = {id(l) for g in groups for l in g}
    codes = [{"box": [g[0]["pos"] - 2, min(l["from"] for l in g), g[-1]["pos"] + 2, max(l["to"] for l in g)]} for g in groups]
    return [l for l in lines if id(l) not in used], codes


def describe(g: dict, page: int, multi: bool) -> str:
    p = f"{page}:" if multi else ""
    out = [f"## {page}쪽 — 쪽 px {g['size'][0]}×{g['size'][1]}" + (f" (기울기 {g['angle']}° 바로잡음)" if g.get("angle") else "")]
    for t in g["tables"]:
        b = t["box"]
        out.append(f"\n### 표 {p}{t['id']}  x {b[0]}~{b[2]} · y {b[1]}~{b[3]} · 열 {len(t['xs']) - 1} · 행 {len(t['ys']) - 1}"
                   + (f" · 선 없는 쪽: {', '.join(t['open'])}" if t["open"] else ""))
        out.append("열 경계 x: " + " ".join(map(str, t["xs"])))
        out.append("행 경계 y: " + " ".join(map(str, t["ys"])))
        for c in t["cells"]:
            b = c["box"]
            span = (f" 행{c['r']}~{c['r'] + c['rs'] - 1}" if c["rs"] > 1 else f" 행{c['r']}") + \
                   (f" 열{c['c']}~{c['c'] + c['cs'] - 1}" if c["cs"] > 1 else f" 열{c['c']}")
            k = c.get("ink")
            ink_s = (f" · 글자 {k['lines']}줄 약 {k['size']}px {k['align']}" if k else " · 빈 칸") + (" · 회색 바탕" if c.get("shade") else "")
            out.append(f"- {p}{c['id']}{span} · x {b[0]}~{b[2]} y {b[1]}~{b[3]}{ink_s}" + (" · 모양 이상" if c.get("odd") else ""))
    if g["lines"]:
        out.append("\n### 표 밖 선")
        for l in g["lines"]:
            out.append(f"- {'가로' if l['dir'] == 'h' else '세로'} {'y' if l['dir'] == 'h' else 'x'} {l['pos']} · {l['from']}~{l['to']}")
    for c in g.get("barcodes") or []:
        b = c["box"]
        out.append(f"\n바코드 자리 x {b[0]}~{b[2]} y {b[1]}~{b[3]} (서식에 넣지 않음)")
    if g["blocks"]:
        out.append("\n### 표 밖 글자 덩어리")
        for bl in g["blocks"]:
            b = bl["box"]
            out.append(f"- {p}{bl['id']} · x {b[0]}~{b[2]} y {b[1]}~{b[3]} · {bl['lines']}줄 약 {bl['size']}px")
    return "\n".join(out)


def run(draft: Path, only: int | None = None, quiet: bool = False) -> list[dict]:
    srcs = sources(draft)
    if not srcs:
        raise SystemExit(f"원본 그림이 없습니다: {draft}/source.png")
    results = []
    for n, src in enumerate(srcs, 1):
        if only and n != only:
            continue
        work = draft / f"page_{n}.png"
        info = prepare(src, work)
        g = measure(Image.open(work), info["upscale"])
        g["angle"] = info["angle"]
        (draft / f"grid_{n}.json").write_text(json.dumps(g, ensure_ascii=False, indent=1), encoding="utf-8")
        results.append(g)
        if not quiet:
            print(describe(g, n, len(srcs) > 1))
            print()
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft", type=Path)
    ap.add_argument("--page", type=int)
    a = ap.parse_args()
    run(a.draft, a.page)


if __name__ == "__main__":
    sys.exit(main())
