"""문서 포맷·양식 묶기: OCR 단어로 지문을 만들어 생김새가 같은 문서끼리 묶는다 (DESIGN.md 8.3).

masking_ui(https://github.com/kimsh12191/masking_ui, 커밋 6f5bca6)의 app/geometry.py(줄 만들기·글자 정규화)와
app/clustering.py(fingerprint, _Cluster, _vectors, _best, _merge_similar, _run, _attach_continuations, _variants)에서
지문·묶기 부분만 옮겨 왔다. 전역 저장소(DOCS·FORMATS·LOCK)와 설정 대신 인자로 받고 결과를 돌려준다.
마스킹, 제목으로 나누기(split_by_title), 규칙, VLM 부분은 가져오지 않았다. masking_ui 가 바뀌어도 따라가지 않는다.

  포맷  생김새가 비슷한 문서 묶음: 줄 글자의 2글자 조각 + 대략적인 세로 위치, 코사인 유사도 (기준 0.40)
  양식  포맷 안에서 표 배치·값 위치까지 같은 문서: 글자 조각 + 가로·세로 위치 (기준 0.60)
  이어지는 쪽: 제목 없이 표만 이어지는 쪽은 표 머리줄이 같은 (제목 있는) 포맷에 붙인다
숫자가 든 조각, 전체 문서 중 한 문서에만 나오는 조각(값)은 비교에서 뺀다.
영문(라틴 글자끼리의 2글자 조각)은 조각 대신 단어("w:invoice")로 비교한다 — 영문 2글자 조각은 거의 모든 영문 문서에 나와
서로 다른 영문 서류가 한 포맷으로 뭉친다 (2026-10-21, 서류 넣기 시험 폴더에서 확인). 한글 조각은 그대로다.

단어 형식: [{"text", "bbox": [x0, y0, x1, y1] 픽셀, "confidence"?, "line_num"?}] (docgen.bench.ocr_data.parse_ocr 결과 그대로).
"""
from __future__ import annotations

import math
import re
from collections import Counter
from statistics import median

YBINS = 8
LX, LY = 8, 16
THRESHOLD = 0.40
VARIANT_TH = 0.6
VARIANT_ATTACH = 0.4
REASSIGN_MARGIN = 0.02
SPARSE, SPARSE_MIN = 80, 8
HEAD_DOCS = 2


# ---------------------------------------------------------------------------
# 줄 (masking_ui geometry.py)
# ---------------------------------------------------------------------------

def norm_text(s: str) -> str:
    return "".join(c.lower() for c in s if c.isalnum())


def _char_weight(ch: str) -> float:
    if ch.isspace():
        return 0.3
    o = ord(ch)
    if 0xAC00 <= o <= 0xD7A3 or 0x3131 <= o <= 0x318E or 0x4E00 <= o <= 0x9FFF:
        return 1.0
    return 0.6 if ch.isalnum() else 0.35


def _char_boxes(w: dict) -> list:
    t = w["text"] or " "
    x1, y1, x2, y2 = w["bbox"]
    ws = [_char_weight(c) for c in t]
    tot = sum(ws) or 1.0
    out, acc = [], 0.0
    for wt in ws:
        a = x1 + (x2 - x1) * acc / tot
        acc += wt
        out.append((a, y1, x1 + (x2 - x1) * acc / tot, y2))
    return out


def _union(boxes):
    boxes = [b for b in boxes if b is not None]
    if not boxes:
        return None
    return (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))


class Line:
    def __init__(self, words: list, idxs: list):
        idxs = sorted(idxs, key=lambda i: words[i]["bbox"][0])
        hs = [words[i]["bbox"][3] - words[i]["bbox"][1] for i in idxs]
        self.H = max(1.0, median(hs)) if hs else 1.0
        self.word_idxs = idxs
        text, boxes, prev = [], [], None
        for i in idxs:
            w = words[i]
            if prev is not None and w["bbox"][0] - prev["bbox"][2] > 0.25 * self.H:
                text.append(" ")
                boxes.append(None)
            cb = _char_boxes(w)
            for ci, ch in enumerate(w["text"]):
                text.append(ch)
                boxes.append(None if ch.isspace() else cb[ci])
            prev = w
        self.text = "".join(text)
        self.boxes = boxes
        self.bbox = _union(words[i]["bbox"] for i in idxs) or (0, 0, 0, 0)

    def span_box(self, a: int, b: int):
        return _union(self.boxes[p] for p in range(a, b) if self.boxes[p] is not None)

    def segments(self, gap_mult: float = 1.0) -> list:
        segs, cur, prev_x2 = [], [], None
        for p, b in enumerate(self.boxes):
            if b is None:
                continue
            if prev_x2 is not None and b[0] - prev_x2 > gap_mult * self.H:
                segs.append(cur)
                cur = []
            cur.append(p)
            prev_x2 = b[2]
        if cur:
            segs.append(cur)
        return [(s[0], s[-1] + 1) for s in segs if norm_text(self.text[s[0]:s[-1] + 1])]

    def pieces(self) -> list:
        out, start = [], None
        for p, ch in enumerate(self.text):
            if ch.isalnum():
                if start is None:
                    start = p
            elif start is not None:
                out.append((start, p))
                start = None
        if start is not None:
            out.append((start, len(self.text)))
        return out


def build_lines(words: list) -> list[Line]:
    """세로로 절반 넘게 겹치고 가로로 이어지는 단어끼리 한 줄 (OCR 줄 번호가 있으면 같은 번호 안에서)."""
    if not words:
        return []
    order = sorted(range(len(words)), key=lambda i: ((words[i]["bbox"][1] + words[i]["bbox"][3]) / 2, words[i]["bbox"][0]))
    groups: list[list[int]] = []
    for i in order:
        b = words[i]["bbox"]
        h = b[3] - b[1]
        for g in groups:
            last = words[g[-1]]["bbox"]
            gl = words[g[-1]].get("line_num")
            if gl is not None and words[i].get("line_num") is not None and gl != words[i].get("line_num"):
                continue
            ov = min(b[3], last[3]) - max(b[1], last[1])
            if ov > 0.5 * min(h, last[3] - last[1]) and -0.5 * h < b[0] - last[2] < 6 * h:
                g.append(i)
                break
        else:
            groups.append([i])
    lines = [Line(words, g) for g in groups]
    lines.sort(key=lambda L: (L.bbox[1], L.bbox[0]))
    return lines


# ---------------------------------------------------------------------------
# 지문 (masking_ui clustering.py fingerprint · _head_line · main_title)
# ---------------------------------------------------------------------------

def _is_token(n: str) -> bool:
    return 2 <= len(n) <= 20 and sum(c.isdigit() for c in n) / len(n) < 0.4


def _head_line(L: Line) -> str:
    cells = [c for c in (norm_text(L.text[a:z]) for a, z in L.segments(1.0)) if c]
    if len(cells) < 3 or any(any(ch.isdigit() for ch in c) for c in cells):
        return ""
    t = "|".join(cells)
    return t if 6 <= len(t) <= 80 else ""


def _lcs(a: str, b: str) -> int:
    prev = [0] * (len(b) + 1)
    for ca in a:
        cur = [0]
        for j, cb in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if ca == cb else max(prev[j], cur[j - 1]))
        prev = cur
    return prev[-1]


def _same_cell(a: str, b: str) -> bool:
    return a == b or _lcs(a, b) >= 0.7 * max(len(a), len(b))


def same_line(a: str, b: str) -> bool:
    A, B = a.split("|"), b.split("|")
    i = j = k = 0
    while i < len(A) and j < len(B):
        if _same_cell(A[i], B[j]):
            k, i, j = k + 1, i + 1, j + 1
        elif any(_same_cell(A[i], y) for y in B[j + 1:j + 3]):
            j += 1
        else:
            i += 1
    return k >= 3 and k >= 0.6 * max(len(A), len(B))


def _title_chars(t: str) -> str:
    """제목 글자: 한글이 2자 이상이면 한글만, 아니면 영문자(대문자로). 영문 서류(인보이스·B/L…)도 제목으로 가른다."""
    h = "".join(c for c in t if "가" <= c <= "힣")
    return h if len(h) >= 2 else "".join(c for c in t if c.isascii() and c.isalpha()).upper()


def main_title(lines: list[Line]) -> str:
    """본문보다 확실히 큰 맨 위쪽 줄의 한글(없으면 영문, 4자 이상) (제목). 없으면 ''."""
    if len(lines) < 3:
        return ""
    y0 = min(L.bbox[1] for L in lines)
    y1 = max(L.bbox[3] for L in lines)
    med = sorted(L.H for L in lines)[len(lines) // 2]
    hang = lambda t: "".join(c for c in t if "가" <= c <= "힣")  # noqa: E731
    ok = lambda t: len(hang(t)) >= 2 or len(_title_chars(t)) >= 4  # noqa: E731
    top = [L for L in lines if L.bbox[1] < y0 + 0.3 * (y1 - y0) and ok(L.text) and L.H < 5 * med]
    if not top:
        return ""
    b = max(top, key=lambda L: L.H)
    if b.H < 1.4 * med:
        return ""
    t = _title_chars(b.text)[:24]
    return t if len(t) >= 2 else ""


def titles_differ(a: str, b: str) -> bool:
    """두 제목이 분명히 다르다 (둘 다 있고 글자가 70% 넘게 같지 않음). 다른 제목끼리는 한 포맷으로 묶지 않는다."""
    return bool(a and b) and not _same_cell(a, b)


def title_of(words: list, H: float) -> str:
    """화면에 보일 이름: 위쪽 30% 에서 한글 비율 × 글자 크기가 가장 큰 줄."""
    lines = build_lines(words)
    if not lines:
        return "빈 문서"

    def score(L):
        t = L.text.replace(" ", "")
        h = sum(1 for c in t if "가" <= c <= "힣")
        return L.H * (h / max(1, len(t))) if h >= 2 else 0.0
    top = [L for L in lines if L.bbox[1] < 0.3 * H and norm_text(L.text)] or lines
    best = max(top, key=score)
    if score(best) <= 0:
        best = max(lines, key=score)
    t = best.text.strip()
    parts = t.split()
    if len(parts) >= 3 and sum(len(p) == 1 for p in parts) >= 0.7 * len(parts):
        t = "".join(parts)
    return t[:30] or "포맷"


def _latin(bg: str) -> bool:
    return bg.isascii() and bg.isalpha()


def _words(text: str) -> list[str]:
    """영문 단어 (2자 이상). 영문은 2글자 조각이 거의 모든 문서에 나와 생김새를 가르지 못하므로 단어로 비교한다."""
    return [w.lower() for w in re.findall(r"[A-Za-z]{2,}", text)][:40]


def fingerprint(words: list, W: float, H: float) -> dict:
    lines = build_lines(words)
    toks, labels, layout, heads = set(), set(), set(), set()
    if lines:
        y0 = min(L.bbox[1] for L in lines)
        span = max(1.0, max(L.bbox[3] for L in lines) - y0)
        x0 = min(L.bbox[0] for L in lines)
        xspan = max(1.0, max(L.bbox[2] for L in lines) - x0)
    for L in lines:
        n = norm_text(L.text)
        cy = min(0.999, max(0.0, ((L.bbox[1] + L.bbox[3]) / 2 - y0) / span))
        for a, z in L.segments(1.0):
            sb = L.span_box(a, z)
            sn = norm_text(L.text[a:z])
            if not sb or len(sn) < 2:
                continue
            cx = min(0.999, max(0.0, ((sb[0] + sb[2]) / 2 - x0) / xspan))
            sy = max(0.0, ((sb[1] + sb[3]) / 2 - y0) / xspan)
            grams = [sn[i:i + 2] for i in range(len(sn) - 1)]
            for bg in [g for g in grams if not _latin(g)] + ["w:" + w for w in _words(L.text[a:z])]:
                if any(c.isdigit() for c in bg):
                    continue
                layout.add(f"{bg}@{int(cx * LX)}.{int(sy * LY)}")
                layout.add(f"{bg}@h{int(cx * LX + 0.5)}.{int(sy * LY + 0.5)}")
        grams = [n[i:i + 2] for i in range(len(n) - 1)]
        for bg in [g for g in grams if not _latin(g)] + ["w:" + w for w in _words(L.text)]:
            if any(c.isdigit() for c in bg):
                continue
            toks.add(bg)
            toks.add(f"{bg}@{int(cy * YBINS)}")
            toks.add(f"{bg}@h{int(cy * YBINS + 0.5)}")
        for a, z in L.pieces():
            t = norm_text(L.text[a:z])
            if _is_token(t):
                labels.add(t)
        h = _head_line(L)
        if h:
            heads.add(h)
    return {"tokens": sorted(toks), "labels": sorted(labels), "layout": sorted(layout), "heads": sorted(heads),
            "title": main_title(lines), "name": title_of(words, H)}


# ---------------------------------------------------------------------------
# 묶기 (masking_ui clustering.py _Cluster · _vectors · _best · _merge_similar · _run · _attach_continuations · _variants)
# ---------------------------------------------------------------------------

class Cluster:
    def __init__(self):
        self.sum = Counter()
        self.n = 0
        self._norm = None
        self.titles = Counter()
        self.merged_into = None

    def add(self, v, title=""):
        self.sum.update(v)
        self.n += 1
        self._norm = None
        if title:
            self.titles[title] += 1

    def remove(self, v, title=""):
        self.sum.subtract(v)
        self.n -= 1
        self._norm = None
        if title:
            self.titles[title] -= 1
            if self.titles[title] <= 0:
                del self.titles[title]

    def dominant(self) -> str:
        tot = sum(self.titles.values())
        if not tot:
            return ""
        best, c = self.titles.most_common(1)[0]
        return best if c / tot >= 0.4 else ""

    def norm(self) -> float:
        if self._norm is None:
            self._norm = math.sqrt(sum((c / self.n) ** 2 for c in self.sum.values() if c > 0)) if self.n else 0.0
        return self._norm

    def sim(self, v) -> float:
        if not v or not self.n or not self.norm():
            return 0.0
        cos = sum(self.sum[t] for t in v) / self.n / (math.sqrt(len(v)) * self.norm())
        if SPARSE_MIN <= len(v) < SPARSE:   # 글자가 적은 문서(신분증 사본 등)는 포함률과 평균
            cont = sum(1 for t in v if self.sum.get(t, 0) >= 0.3 * self.n) / len(v)
            return (cos + cont) / 2
        return cos

    def sim_cluster(self, o) -> float:
        if not self.n or not o.n or not self.norm() or not o.norm():
            return 0.0
        a, b = (self, o) if len(self.sum) < len(o.sum) else (o, self)
        num = sum(c * b.sum[t] for t, c in a.sum.items() if c > 0 and b.sum.get(t, 0) > 0)
        return num / (self.n * o.n) / (self.norm() * o.norm())


def _resolve(c: Cluster) -> Cluster:
    while c.merged_into is not None:
        c = c.merged_into
    return c


def _vectors(fps: dict[str, set]) -> dict[str, frozenset]:
    df = Counter()
    for s in fps.values():
        df.update(s)
    return {k: frozenset(t for t in s if df[t] >= 2) for k, s in fps.items()}


def _best(clusters: list, v):
    best, best_s = None, 0.0
    for c in clusters:
        s = c.sim(v)
        if s > best_s:
            best, best_s = c, s
    return best, best_s


def _merge_similar(clusters: list, threshold: float, can_absorb) -> None:
    while True:
        alive = [c for c in clusters if c.n]
        best = None
        for i, a in enumerate(alive):
            for b in alive[i + 1:]:
                if not (can_absorb(a, b) or can_absorb(b, a)):
                    continue
                s = a.sim_cluster(b)
                if s >= threshold and (best is None or s > best[0]):
                    best = (s, a, b)
        if best is None:
            return
        _, a, b = best
        keep, gone = (a, b) if (a.n >= b.n and can_absorb(a, b)) or not can_absorb(b, a) else (b, a)
        keep.sum.update(gone.sum)
        keep.n += gone.n
        keep._norm = None
        keep.titles.update(gone.titles)
        gone.sum, gone.n, gone._norm = Counter(), 0, None
        gone.merged_into = keep


def cluster(docs: list[dict], threshold: float = THRESHOLD, fixed: dict | None = None) -> dict[str, int]:
    """docs: [{"id", "fp": fingerprint(...)}]. → {문서 id: 포맷 번호 (문서가 많은 포맷부터 0, 1, …)}.
    fixed: {문서 id: 사람이 정한 묶음 이름} — 같은 이름은 한 포맷으로 고정하고, 자동 묶기가 다른 데로 옮기지 않는다."""
    fixed = fixed or {}
    V = _vectors({d["id"]: set(d["fp"]["tokens"]) for d in docs})
    T = {d["id"]: d["fp"].get("title", "") for d in docs}
    heads = {d["id"]: d["fp"].get("heads") or [] for d in docs}
    pinned: dict[str, Cluster] = {}
    cl: list[Cluster] = []
    assign: dict[str, Cluster] = {}
    for d in docs:
        did = d["id"]
        v = V[did]
        if did in fixed:
            c = pinned.get(fixed[did])
            if c is None:
                c = pinned[fixed[did]] = Cluster()
                c.pinned = True
                cl.append(c)
        else:
            c, s = _best([x for x in cl if x.n and not titles_differ(T[did], x.dominant())], v)
            if c is None or s < threshold:
                c = Cluster()
                cl.append(c)
        c.add(v, T[did])
        assign[did] = c
    _merge_similar(cl, threshold, lambda keep, gone: not getattr(gone, "pinned", False)
                   and not titles_differ(keep.dominant(), gone.dominant()))
    assign = {k: _resolve(c) for k, c in assign.items()}
    for _ in range(2):
        moved = 0
        live = [c for c in cl if c.n]
        for d in docs:
            did = d["id"]
            if did in fixed:
                continue
            v, cur = V[did], assign[did]
            c, s = _best([x for x in live if not titles_differ(T[did], x.dominant())], v)
            if c is not None and c is not cur and s > cur.sim(v) + REASSIGN_MARGIN:
                cur.remove(v, T[did])
                c.add(v, T[did])
                assign[did] = c
                moved += 1
        if not moved:
            break
    # 이어지는 쪽: 제목 없는 포맷에 든, 제목 없는 문서를 표 머리줄이 같은 제목 있는 포맷으로
    by: dict[int, tuple] = {}
    for did, c in assign.items():
        by.setdefault(id(c), (c, []))[1].append(did)
    homes = [(c, [heads[i] for i in ids]) for c, ids in by.values() if c.dominant()]
    for did, cur in list(assign.items()):
        if did in fixed or T[did] or not heads[did] or cur.dominant() or not homes:
            continue
        best, best_r = None, 0.0
        for c, hs in homes:
            if c is cur:
                continue
            k = max(sum(1 for xs in hs if any(same_line(h, x) for x in xs)) for h in heads[did])
            r = k + k / len(hs)
            if k >= min(HEAD_DOCS, len(hs)) and r > best_r:
                best, best_r = c, r
        if best is not None:
            cur.remove(V[did], T[did])
            best.add(V[did], T[did])
            assign[did] = best
    groups: dict[int, list[str]] = {}
    for did, c in assign.items():
        groups.setdefault(id(c), []).append(did)
    order = sorted(groups.values(), key=lambda ids: (-len(ids), ids[0]))
    return {did: n for n, ids in enumerate(order) for did in ids}


def variants(docs: list[dict]) -> dict[str, int]:
    """포맷 안의 양식: 글자 조각 + 가로·세로 위치로 다시 묶는다. → {문서 id: 양식 번호 (큰 것부터)}"""
    if not docs:
        return {}
    V = _vectors({d["id"]: set(d["fp"]["layout"]) for d in docs})
    cl, assign = [], {}
    for d in docs:
        v = V[d["id"]]
        c, s = _best(cl, v)
        if c is None or s < VARIANT_TH:
            c = Cluster()
            cl.append(c)
        c.add(v)
        assign[d["id"]] = c
    for _ in range(3):
        moved = 0
        for d in docs:
            v, cur = V[d["id"]], assign[d["id"]]
            c, s = _best([x for x in cl if x.n], v)
            if c is not None and c is not cur and s > cur.sim(v) + REASSIGN_MARGIN:
                cur.remove(v)
                c.add(v)
                assign[d["id"]] = c
                moved += 1
        if not moved:
            break
    _merge_similar(cl, VARIANT_TH, lambda keep, gone: True)
    assign = {k: _resolve(c) for k, c in assign.items()}
    for _ in range(2):   # 잡음으로 떨어진 한두 건은 가장 가까운 큰 양식에
        cores = [c for c in {id(x): x for x in assign.values()}.values() if c.n >= 3]
        for d in docs:
            cur = assign[d["id"]]
            if cur.n >= 3 or not cores:
                continue
            c, s = _best(cores, V[d["id"]])
            if c is not None and s >= VARIANT_ATTACH:
                cur.remove(V[d["id"]])
                c.add(V[d["id"]])
                assign[d["id"]] = c
    groups: dict[int, list[str]] = {}
    for did, c in assign.items():
        groups.setdefault(id(c), []).append(did)
    order = sorted(groups.values(), key=lambda ids: (-len(ids), ids[0]))
    return {did: n for n, ids in enumerate(order) for did in ids}


def centroid_sim(tokens_a: set, members: list[set]) -> float:
    """기존 서식 하나(지문)와 포맷(문서 지문들)의 비슷한 정도 (가까운 기존 서식 찾기)."""
    c = Cluster()
    for m in members:
        c.add(frozenset(m))
    return c.sim(frozenset(tokens_a))
