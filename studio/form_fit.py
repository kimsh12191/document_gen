"""서식 초안 다듬기의 비교: 원본 이미지와 렌더링을 견줘 점수·겹침 그림·덩어리별 위치 차이를 만든다 (PIL 만 쓴다).

원본에서 선·칸을 검출하지 않는다 (촬영·스캔본에서 자주 틀리고, 틀린 숫자는 모델을 망친다).
대신 깨끗한 쪽인 렌더링에서 덩어리(표·문단)와 세로선을 찾고, 원본과는 잉크 분포만 맞댄다.
  - 세로: 두 그림의 행별 잉크 양(가로로 합친 것)을 DTW 로 맞대어 렌더링 행 → 원본 행 대응을 얻는다.
  - 가로: 덩어리마다 그 띠의 열별 잉크 양을 같은 방법으로 맞대어 렌더링 세로선 → 원본 x 를 얻는다.
단위는 서식 쪽 px (A4 794×1123) 이라 모델이 템플릿 CSS 에 바로 쓴다. 점수는 잉크 겹침 F1 (±3px 허용, 0~100).

  compare(원본 경로, 렌더링 쪽 그림 경로, label.json 경로) → {score, precision, recall, feedback, blocks, ...}
  composite(원본, 렌더링, 저장 경로)   원본 | 렌더링 | 겹침(빨강 원본에만, 파랑 렌더링에만, 검정 겹침) 한 장
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter, ImageOps

PAGE = (794, 1123)          # 쪽 px (docgen A4)
AW = 600                    # 분석 폭
STEP = 3                    # 프로필을 몇 px 씩 묶어 맞댈지 (분석 해상도)
INK = 170                   # 이보다 어두우면 잉크


def _mask(im: Image.Image, size) -> Image.Image:
    g = ImageOps.grayscale(im.convert("RGB")).resize(size, Image.LANCZOS)
    return g.point(lambda v: 255 if v < INK else 0)


def _count(mask: Image.Image) -> int:
    return mask.histogram()[255]


def score(orig: Image.Image, render: Image.Image) -> dict:
    size = (AW, round(AW * PAGE[1] / PAGE[0]))
    A, B = _mask(orig, size), _mask(render, size)
    Ad, Bd = A.filter(ImageFilter.MaxFilter(7)), B.filter(ImageFilter.MaxFilter(7))
    p = _count(ImageChops.multiply(B, Ad)) / max(1, _count(B))
    r = _count(ImageChops.multiply(A, Bd)) / max(1, _count(A))
    return {"score": round(100 * 2 * p * r / max(1e-9, p + r), 1), "precision": round(100 * p, 1), "recall": round(100 * r, 1)}


def _profile(mask: Image.Image, axis: str, box=None) -> list[float]:
    """행별(axis="y") 또는 열별("x") 잉크 비율, STEP 칸씩 묶어서."""
    m = mask.crop(box) if box else mask
    w, h = m.size
    if axis == "y":
        n = max(1, h // STEP)
        return [v / 255 for v in m.resize((1, n), Image.BOX).tobytes()]
    n = max(1, w // STEP)
    return [v / 255 for v in m.resize((n, 1), Image.BOX).tobytes()]


def dtw(a: list[float], b: list[float], band: float = 0.15, skew: float = 0.02) -> list[int]:
    """a 의 각 칸이 b 의 어느 칸에 대응하는지 (띠 DTW, 대각선 선호)."""
    n, m = len(a), len(b)
    w = max(abs(n - m) + 2, int(band * max(n, m)))
    inf = float("inf")
    cost = [[inf] * (m + 1) for _ in range(n + 1)]
    move = [[0] * (m + 1) for _ in range(n + 1)]
    cost[0][0] = 0.0
    for i in range(1, n + 1):
        c = round(i * m / n)
        for j in range(max(1, c - w), min(m, c + w) + 1):
            d = abs(a[i - 1] - b[j - 1])
            best, mv = cost[i - 1][j - 1], 0
            if cost[i - 1][j] + skew < best:
                best, mv = cost[i - 1][j] + skew, 1
            if cost[i][j - 1] + skew < best:
                best, mv = cost[i][j - 1] + skew, 2
            cost[i][j] = d + best
            move[i][j] = mv
    i, j, match = n, m, [0] * n
    while i > 0 and j > 0:
        match[i - 1] = j - 1
        mv = move[i][j]
        if mv == 0:
            i, j = i - 1, j - 1
        elif mv == 1:
            i -= 1
        else:
            j -= 1
    return match


def _runs(prof: list[float], thr: float, gap: int, min_len: int) -> list[tuple[int, int]]:
    out, start, last = [], None, None
    for i, v in enumerate(prof):
        if v > thr:
            if start is None:
                start = i
            elif i - last > gap:
                out.append((start, last))
                start = i
            last = i
    if start is not None:
        out.append((start, last))
    return [(s, e) for s, e in out if e - s + 1 >= min_len]


def _peaks(prof: list[float], thr: float) -> list[int]:
    return [i for i, v in enumerate(prof) if v >= thr and (i == 0 or prof[i - 1] < v) and (i + 1 == len(prof) or prof[i + 1] <= v)]


def compare(orig_path, render_path, label_path=None) -> dict:
    orig = Image.open(orig_path).convert("RGB")
    render = Image.open(render_path).convert("RGB")
    res = score(orig, render)
    size = (AW, round(AW * PAGE[1] / PAGE[0]))
    A, B = _mask(orig, size), _mask(render, size)
    k = PAGE[0] / AW                                           # 분석 px → 쪽 px
    pa, pb = _profile(A, "y"), _profile(B, "y")
    ymap = dtw(pb, pa)                                         # 렌더링 칸 → 원본 칸
    fields = []
    if label_path and Path(label_path).exists():
        lab = json.loads(Path(label_path).read_text(encoding="utf-8"))
        sx = PAGE[0] / lab["pages"][0]["width"]
        fields = [(f.get("label") or f["key"], (f["bbox"][1] + f["bbox"][3]) / 2 * sx)
                  for f in lab.get("fields", []) if f.get("page", 0) == 0 and f.get("bbox")]
    blocks = []
    for s, e in _runs(pb, 0.004, gap=1, min_len=2):
        y0, y1 = s * STEP * k, (e + 1) * STEP * k
        o0, o1 = ymap[s] * STEP * k, (ymap[e] + 1) * STEP * k
        names = list(dict.fromkeys(n for n, cy in fields if y0 <= cy <= y1))
        # 가로: 이 띠의 세로선(렌더링에서 찾은 것)이 원본 띠의 어디에 대응하는지
        cols = []
        band_b = (0, s * STEP, AW, (e + 1) * STEP)
        band_a = (0, ymap[s] * STEP, AW, (ymap[e] + 1) * STEP)
        if (e - s + 1) * STEP * k >= 30:
            xb, xa = _profile(B, "x", band_b), _profile(A, "x", band_a)
            xmap = dtw(xb, xa, band=0.1)
            for p in _peaks(xb, 0.55):
                cols.append((round(p * STEP * k), round(xmap[p] * STEP * k)))
        fine = [v / 255 for v in B.crop(band_b).resize((1, band_b[3] - band_b[1]), Image.BOX).tobytes()]   # 1px 행: 가로선
        rows = [(round((band_b[1] + i) * k), round((ymap[s + i // STEP] * STEP + i % STEP) * k)) for i in _peaks(fine, 0.5)]
        blocks.append({"y": [round(y0), round(y1)], "orig_y": [round(o0), round(o1)], "names": names[:4], "cols": cols, "rows": rows})
    res.update(blocks=blocks, feedback=feedback(blocks, res), ymap_end=[len(pb), ymap[-1] if ymap else 0])
    return res


def feedback(blocks: list[dict], res: dict) -> str:
    """모델에게 줄 숫자 차이. 눈에 띄는 것만 (위치 4px, 높이 4%, 세로선 8px 이상)."""
    lines = []
    if blocks:
        last, olast = blocks[-1]["y"][1], blocks[-1]["orig_y"][1]
        if abs(last - olast) >= 8:
            lines.append(f"전체: 내용 끝이 원본보다 {abs(last - olast)}px {'아래' if last > olast else '위'} "
                         f"(렌더링 y={last} ↔ 원본 y={olast}). 위쪽 덩어리부터 맞추면 아래는 따라온다.")
    for n, b in enumerate(blocks, 1):
        (y0, y1), (o0, o1) = b["y"], b["orig_y"]
        h, oh = y1 - y0, o1 - o0
        notes = []
        if abs(y0 - o0) >= 4:
            notes.append(f"시작이 원본보다 {abs(y0 - o0)}px {'아래' if y0 > o0 else '위'}")
        if h >= 12 and oh > 0 and abs(h / oh - 1) >= 0.04:
            notes.append(f"높이 {h}px ↔ 원본 {oh}px ({(h / oh - 1) * 100:+.0f}%)")
        if any(abs(y - oy) >= 4 for y, oy in b["rows"]) and len(b["rows"]) >= 3:
            notes.append("가로선 렌더링→원본 " + ", ".join(f"{y}→{oy}" for y, oy in b["rows"][:14]))
        moved = [(x, ox) for x, ox in b["cols"] if abs(x - ox) >= 8]
        if moved:
            notes.append("세로선 " + ", ".join(f"x={x}→원본 x={ox}" for x, ox in moved[:6]))
        if notes:
            name = "·".join(f"'{x}'" for x in b["names"]) if b["names"] else "값 칸 없는 덩어리"
            lines.append(f"{n}. y {y0}~{y1} ({name}): " + "; ".join(notes))
    if not lines:
        lines.append("숫자로 보이는 큰 위치 차이는 없다. 겹침 그림에서 글자·선 모양 차이를 본다.")
    return "\n".join(lines)


def composite(orig_path, render_path, out_path) -> Path:
    render = Image.open(render_path).convert("RGB").resize(PAGE, Image.LANCZOS)
    orig = Image.open(orig_path).convert("RGB").resize(PAGE, Image.LANCZOS)
    A, B = _mask(orig, PAGE), _mask(render, PAGE)
    over = Image.new("RGB", PAGE, "white")
    over.paste((220, 40, 40), mask=ImageChops.subtract(A, B))
    over.paste((40, 90, 230), mask=ImageChops.subtract(B, A))
    over.paste((0, 0, 0), mask=ImageChops.multiply(A, B))
    W, H = PAGE
    comp = Image.new("RGB", (W * 3 + 20, H), "white")
    for i, im in enumerate((orig, render, over)):
        comp.paste(im, (i * (W + 10), 0))
    comp.save(out_path)
    return Path(out_path)
