"""1단계 관찰 분석: 행 기록(rows.jsonl) → 결과 분포, 특징별 누락률, 로지스틱 회귀 (analysis.md, analysis.json).

  python -m mpx analyze --rows rows.jsonl --out analysis.md

세 가지 표
  ① 결과 분포   실행(run)마다 정답 행이 어느 결과로 갔는지 (%). '누락' = skipped + cut_length + cut_stop + doc_missing
  ② 특징별 누락률  특징 구간(모든 실행을 합친 4분위, 참/거짓)마다 실행별 누락률과 행 수
  ③ 회귀        실행마다 '누락 여부'를 특징들로 설명하는 로지스틱 회귀(외부 패키지 없이 뉴턴법). 특징은 표준화하므로 계수는 1 표준편차당 로그 오즈,
                오즈비 = exp(계수). |z| 큰 순서가 '용의자 순위'. 대상을 두 가지로:
                  누락 전체      모든 행
                  건너뜀         잘림·스스로 끝냄·문서 못 찾음을 뺀 행에서 skipped 여부 (출력 중간에 빠진 것만)
회귀는 상관이다. 한 번에 넣기에서는 쪽 수가 늘면 해상도·이미지 수·출력 위치가 함께 변하므로 원인 판정은 통제 실험(probe)으로 한다.
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

from .common import read_jsonl
from .rows import DROPPED, NAME, OUTCOMES

NUMERIC = [("glyph_tok", "글자 높이(토큰)"), ("pitch_tok", "행 간격(토큰)"), ("page_tokens", "쪽 이미지 토큰"),
           ("y_top", "쪽 안 세로 위치"), ("n_images", "요청 이미지 수"), ("rows_before", "출력에서 앞선 행 수"),
           ("row_frac", "목록 안 위치"), ("list_len", "목록 길이"), ("sim_neighbor", "이웃 행과 같은 칸 비율"),
           ("n_cells", "칸 수"), ("chars", "글자 수")]
BINARY = [("boundary", "쪽 경계 행"), ("cont", "이어지는 쪽의 행"), ("no_header", "머리글 없는 쪽의 행"),
          ("augmented", "증강(스캔·촬영·팩스)"), ("heavy", "긴 목록 서류")]
LABEL = dict(NUMERIC + BINARY)
CUT = ("cut_length", "cut_stop", "doc_missing")


def _pct(a, b) -> str:
    return "—" if not b else f"{100 * a / b:.1f}"


def _quantile_edges(values: list[float], k: int = 4) -> list[float]:
    v = sorted(values)
    if not v:
        return []
    edges = sorted({v[min(len(v) - 1, int(len(v) * q / k))] for q in range(1, k)})
    return [e for e in edges if v[0] < e <= v[-1]]


def _bin(x, edges: list[float]) -> int:
    return sum(1 for e in edges if x >= e)


def _bin_label(b: int, edges: list[float]) -> str:
    def f(x):
        return f"{x:.2f}" if abs(x) < 10 else f"{x:,.0f}"
    lo = f(edges[b - 1]) if b > 0 else "최소"
    hi = f(edges[b]) if b < len(edges) else "최대"
    return f"{lo} ~ {hi}" if b < len(edges) else f"{lo} 이상"


# ---------------------------------------------------------------------------
# 로지스틱 회귀 (표준화한 특징, 작은 L2, 뉴턴법)
# ---------------------------------------------------------------------------

def _solve(A: list[list[float]], b: list[float]) -> list[float]:
    """가우스 소거 (부분 피벗). A 는 대칭 양정치라 가정."""
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c]:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def logistic(rows: list[dict], target, features: list[str], l2: float = 1.0) -> list[dict]:
    """[{feature, coef, se, z, odds}] |z| 큰 순서. 행이 적거나 한쪽 결과만 있으면 []. 뉴턴법, 외부 패키지 없음."""
    y = [1.0 if target(r) else 0.0 for r in rows]
    if len(rows) < 20 or sum(y) < 3 or sum(y) > len(y) - 3:
        return []
    cols, names = [], []
    for f in features:
        vals = [r.get(f) for r in rows]
        num = [float(v) for v in vals if v is not None]
        if len(num) < len(vals) * 0.5:
            continue
        mean = sum(num) / len(num)
        x = [float(v) if v is not None else mean for v in vals]
        m = sum(x) / len(x)
        sd = math.sqrt(sum((v - m) ** 2 for v in x) / len(x))
        if sd < 1e-9:
            continue
        cols.append([(v - m) / sd for v in x])
        names.append(f)
    if not cols:
        return []
    X = [[1.0] + [c[i] for c in cols] for i in range(len(y))]
    d = len(X[0])
    w = [0.0] * d

    def hessian(p):
        H = [[0.0] * d for _ in range(d)]
        for xi, pi in zip(X, p):
            v = pi * (1 - pi)
            for a in range(d):
                va = v * xi[a]
                Ha = H[a]
                for b in range(a, d):
                    Ha[b] += va * xi[b]
        for a in range(d):
            for b in range(a):
                H[a][b] = H[b][a]
            if a:
                H[a][a] += l2
        return H

    def probs():
        out = []
        for xi in X:
            z = max(-30.0, min(30.0, sum(a * b for a, b in zip(w, xi))))
            out.append(1 / (1 + math.exp(-z)))
        return out

    for _ in range(50):
        p = probs()
        g = [sum((yi - pi) * xi[a] for xi, yi, pi in zip(X, y, p)) - (l2 * w[a] if a else 0.0) for a in range(d)]
        step = _solve(hessian(p), g)
        w = [a + b for a, b in zip(w, step)]
        if max(abs(v) for v in step) < 1e-6:
            break
    H = hessian(probs())
    se = []
    for a in range(d):  # 역행렬의 대각 = H x = e_a 의 해의 a 번째
        e = [0.0] * d
        e[a] = 1.0
        se.append(math.sqrt(max(_solve(H, e)[a], 0.0)))
    out = [{"feature": n, "coef": w[i + 1], "se": se[i + 1], "z": w[i + 1] / se[i + 1] if se[i + 1] > 0 else 0.0,
            "odds": math.exp(w[i + 1])} for i, n in enumerate(names)]
    return sorted(out, key=lambda r: -abs(r["z"]))


# ---------------------------------------------------------------------------
# 분석
# ---------------------------------------------------------------------------

def analyze(rows: list[dict]) -> dict:
    runs = list(dict.fromkeys(r["run"] for r in rows))
    by_run = defaultdict(list)
    for r in rows:
        by_run[r["run"]].append(r)
    res: dict = {"runs": runs, "outcomes": {}, "bins": {}, "regression": {}}
    for run in runs:
        c = Counter(r["outcome"] for r in by_run[run])
        n = len(by_run[run])
        res["outcomes"][run] = {"rows": n, **{o: c.get(o, 0) for o in OUTCOMES},
                                "dropped": sum(c.get(o, 0) for o in DROPPED),
                                "truncated_outputs": sum(1 for r in by_run[run] if r["truncated"])}
    for f, _ in NUMERIC:
        edges = _quantile_edges([r[f] for r in rows if r.get(f) is not None])
        table = {}
        for run in runs:
            cnt = defaultdict(lambda: [0, 0])
            for r in by_run[run]:
                if r.get(f) is None:
                    continue
                b = _bin(r[f], edges)
                cnt[b][0] += r["dropped"]
                cnt[b][1] += 1
            table[run] = {b: v for b, v in cnt.items()}
        res["bins"][f] = {"edges": edges, "table": table}
    for f, _ in BINARY:
        table = {}
        for run in runs:
            cnt = defaultdict(lambda: [0, 0])
            for r in by_run[run]:
                cnt[int(bool(r.get(f)))][0] += r["dropped"]
                cnt[int(bool(r.get(f)))][1] += 1
            table[run] = dict(cnt)
        res["bins"][f] = {"edges": None, "table": table}
    feats = [f for f, _ in NUMERIC + BINARY]
    for run in runs:
        rs = by_run[run]
        res["regression"][run] = {
            "dropped": logistic(rs, lambda r: r["dropped"], feats),
            "skipped": logistic([r for r in rs if r["outcome"] not in CUT], lambda r: r["outcome"] == "skipped", feats)}
    return res


def report_md(res: dict) -> str:
    runs = res["runs"]
    L = ["# 1단계 관찰: 행이 어디서 빠지는가", "",
         "정답 행 하나하나의 결과(rows.py)와 특징으로 본 분석. 누락 = 건너뜀 + 길이에 잘림 + 스스로 끝냄 + 문서 못 찾음.",
         "회귀는 상관이며, 원인 판정은 통제 실험(probes.md)으로 한다.", "", "## ① 결과 분포 (정답 행 %)", ""]
    L += ["| 실행 | 행 | " + " | ".join(NAME[o] for o in OUTCOMES) + " | **누락** | 잘린 답의 행 |",
          "|---|---:|" + "---:|" * (len(OUTCOMES) + 2)]
    for run in runs:
        o = res["outcomes"][run]
        L.append(f"| {run} | {o['rows']:,} | " + " | ".join(_pct(o[k], o["rows"]) for k in OUTCOMES)
                 + f" | **{_pct(o['dropped'], o['rows'])}** | {_pct(o['truncated_outputs'], o['rows'])} |")
    L += ["", "## ② 특징별 누락률 (실행마다 누락 % / 행 수)", ""]
    L += ["| 특징 | 구간 | " + " | ".join(runs) + " |", "|---|---|" + "---:|" * len(runs)]
    for f, label in NUMERIC + BINARY:
        b = res["bins"][f]
        keys = sorted({k for t in b["table"].values() for k in t})
        for k in keys:
            name = ("예" if k else "아니오") if b["edges"] is None else _bin_label(k, b["edges"])
            cells = []
            for run in runs:
                d, n = b["table"][run].get(k, [0, 0])
                cells.append(f"{_pct(d, n)} / {n:,}" if n else "—")
            L.append(f"| {label} | {name} | " + " | ".join(cells) + " |")
    L += ["", "## ③ 회귀: 누락과 묶이는 특징 (|z| 큰 순서, 계수는 1 표준편차당 로그 오즈)", ""]
    for run in runs:
        for target, title in (("dropped", "누락 전체"), ("skipped", "건너뜀만 (잘림·끝냄 제외)")):
            reg = res["regression"][run][target]
            L += [f"**{run} — {title}**", ""]
            if not reg:
                L += ["행이 적거나 한쪽 결과만 있어 회귀를 하지 않음.", ""]
                continue
            L += ["| 특징 | 계수 | 오즈비 | z |", "|---|---:|---:|---:|"]
            for d in reg:
                L.append(f"| {LABEL.get(d['feature'], d['feature'])} | {d['coef']:+.2f} | {d['odds']:.2f} | {d['z']:+.1f} |")
            L.append("")
    return "\n".join(L) + "\n"


def run_analysis(rows_path, out) -> str:
    rows = read_jsonl(rows_path)
    res = analyze(rows)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    md = report_md(res)
    out.write_text(md, encoding="utf-8")
    out.with_suffix(".json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return md
