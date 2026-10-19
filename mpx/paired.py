"""모델 짝 비교: 같은 정답 행이 두 모델에서 각각 어떻게 됐는지 (paired.md, paired.json).

  python -m mpx paired --rows runs/compare/rows.jsonl --probes base=runs/base/probes bank=runs/bank/probes --out runs/compare/paired.md

누락률을 나란히 놓으면 "어느 모델이 더 빠뜨리나"만 보인다. 같은 행끼리 짝지으면 행마다 네 칸으로 나뉜다:
  둘 다 냄 / A만 빠뜨림 / B만 빠뜨림 / 둘 다 빠뜨림
'둘 다 빠뜨림'은 두 모델이 공유하는 원인(구조·입력), 'B만 빠뜨림'은 B 쪽에만 생긴 원인(예: 학습)의 후보다.
A만·B만 수의 차이는 부호 검정(McNemar 정확 검정)으로 우연인지 본다(p).

관찰 실행  행 = (방법, 묶음, 문서, 목록, 행 번호). 방법마다, 그리고 특징 구간(analyze 의 참/거짓 특징, 일부 수치 특징의
           4분위, 서류 종류)마다 위 네 칸. 'B만 빠뜨림'이 어느 특징에 몰리는지가 핵심이다. 예시 행은 묶음 viewer 로 연결.
통제 실험  행 = (문항, 목록, 행 번호). 실험·조건마다 네 칸. E·F(같은 글자 반복)는 반복 묶음 안 행만 따로 한 줄 더.
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from .analyze import BINARY, LABEL, _bin, _bin_label, _quantile_edges
from .common import read_jsonl

GROUP_NUMERIC = ("pitch_tok", "glyph_tok", "rows_before", "row_frac")
EXAMPLES = 10


def sign_test(b: int, c: int) -> float | None:
    """두 쪽 정확 부호 검정 p (b, c = 한 쪽만 빠뜨린 수). n 이 크면 정규 근사."""
    n = b + c
    if n == 0:
        return None
    k = min(b, c)
    if n > 2000:
        z = (abs(b - c) - 1) / math.sqrt(n)
        return math.erfc(max(z, 0) / math.sqrt(2))
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def _cell(pairs: list[tuple[dict, dict]]) -> dict:
    both = sum(1 for a, b in pairs if a["dropped"] and b["dropped"])
    only_a = sum(1 for a, b in pairs if a["dropped"] and not b["dropped"])
    only_b = sum(1 for a, b in pairs if b["dropped"] and not a["dropped"])
    return {"rows": len(pairs), "a_dropped": both + only_a, "b_dropped": both + only_b,
            "both": both, "only_a": only_a, "only_b": only_b, "p": sign_test(only_a, only_b)}


def _models_of(rows: list[dict]) -> list[str]:
    """compare 가 붙인 실행 이름 '<모델>_<방법>' 에서 모델 이름 (관찰 실행은 방법 이름이 run 의 끝)."""
    return list(dict.fromkeys(r["run"][: -len(r["method"]) - 1] for r in rows))


def observe(rows: list[dict]) -> dict:
    """{'A vs B': {방법: {'all': 칸, 'groups': {특징: {구간: 칸}}, 'examples': {'only_a': [...], 'only_b': [...]}}}}"""
    models = _models_of(rows)
    by: dict = defaultdict(dict)
    for r in rows:
        m = r["run"][: -len(r["method"]) - 1]
        by[(m, r["method"])][(r["bundle"], r["doc"], r["list"], r["row"])] = r
    edges = {f: _quantile_edges([r[f] for r in rows if r.get(f) is not None]) for f in GROUP_NUMERIC}
    res: dict = {}
    for a, b in combinations(models, 2):
        res[f"{a} vs {b}"] = per = {}
        for method in dict.fromkeys(r["method"] for r in rows):
            ra, rb = by.get((a, method), {}), by.get((b, method), {})
            pairs = [(ra[k], rb[k]) for k in ra if k in rb]
            if not pairs:
                continue
            groups: dict = {}
            for f, _ in BINARY:
                groups[f] = {v: _cell([p for p in pairs if bool(p[0].get(f)) == v]) for v in (True, False)}
            for f in GROUP_NUMERIC:
                g = defaultdict(list)
                for p in pairs:
                    if p[0].get(f) is not None:
                        g[_bin(p[0][f], edges[f])].append(p)
                groups[f] = {_bin_label(k, edges[f]): _cell(v) for k, v in sorted(g.items())}
            g = defaultdict(list)
            for p in pairs:
                g[p[0]["doc_type"]].append(p)
            groups["doc_type"] = {k: _cell(v) for k, v in sorted(g.items())}
            ex = {}
            for side, test in (("only_a", lambda x, y: x["dropped"] and not y["dropped"]),
                               ("only_b", lambda x, y: y["dropped"] and not x["dropped"])):
                ex[side] = [{"bundle": x["bundle"], "doc": x["doc"], "list": x["list"], "row": x["row"],
                             "a": x["outcome"], "b": y["outcome"], "same_text_prev": x.get("same_text_prev")}
                            for x, y in pairs if test(x, y)][:EXAMPLES]
            per[method] = {"all": _cell(pairs), "groups": groups, "examples": ex}
    return res


def probes(runs: dict) -> dict:
    """runs = {모델: probes 폴더}. {'A vs B': {실험: {조건: 칸, 조건+' 반복 묶음 안': 칸}}}"""
    rows = {m: {(r["id"], r["list"], r["key"]): r for r in read_jsonl(Path(d) / "rows.jsonl")} for m, d in runs.items()}
    res: dict = {}
    for a, b in combinations(rows, 2):
        pairs = [(rows[a][k], rows[b][k]) for k in rows[a] if k in rows[b]]
        by = defaultdict(lambda: defaultdict(list))
        for p in pairs:
            by[p[0]["kind"]][p[0]["cond"]].append(p)
        out = res[f"{a} vs {b}"] = {}
        for kind, conds in by.items():
            out[kind] = {}
            for cond, ps in conds.items():
                out[kind][cond] = _cell(ps)
                if kind in ("repeat", "penalty"):
                    inr = [p for p in ps if p[0].get("in_run")]
                    if inr:
                        out[kind][f"{cond} 반복 묶음 안"] = _cell(inr)
    return res


def _pct(a, n) -> str:
    return "—" if not n else f"{100 * a / n:.1f}"


def _p(p) -> str:
    return "—" if p is None else ("<0.001" if p < 0.001 else f"{p:.3f}")


def _row(label: str, c: dict) -> str:
    n = c["rows"]
    return (f"| {label} | {n:,} | {_pct(c['a_dropped'], n)} | {_pct(c['b_dropped'], n)} | {c['both']:,} | "
            f"{c['only_a']:,} | {c['only_b']:,} | {_p(c['p'])} |")


def _head(a: str, b: str, first: str) -> list[str]:
    return [f"| {first} | 행 | {a} 누락 % | {b} 누락 % | 둘 다 빠뜨림 | {a}만 | {b}만 | p |", "|---|---:|---:|---:|---:|---:|---:|---:|"]


def report_md(obs: dict, prb: dict, viewer_dir: str | None = "viewer") -> str:
    from .probe import KINDS, ORDER, TITLE

    L = ["# 모델 짝 비교: 같은 행이 두 모델에서 어떻게 됐나", "",
         "같은 정답 행을 짝지어 셌다. **둘 다 빠뜨림**은 두 모델이 공유하는 원인, **한 모델만 빠뜨림**은 그 모델에만 있는 원인의 후보다.",
         "p 는 'A만'과 'B만' 수가 같다는 가정의 부호 검정(작을수록 차이가 우연이 아님). 구간 행은 그 특징을 가진 행만 센 것.", ""]
    for pair, per in obs.items():
        a, b = pair.split(" vs ")
        for method, d in per.items():
            L += [f"## 관찰 실행 {method}: {a} vs {b}", ""] + _head(a, b, "특징 · 구간") + [_row("**전체**", d["all"])]
            for f, cells in d["groups"].items():
                label = "서류 종류" if f == "doc_type" else LABEL.get(f, f)
                for k, c in cells.items():
                    if c["rows"]:
                        kk = {True: "예", False: "아니오"}.get(k, k) if isinstance(k, bool) else k
                        L.append(_row(f"{label} · {kk}", c))
            for side, who in (("only_a", a), ("only_b", b)):
                ex = d["examples"][side]
                if not ex:
                    continue
                L += ["", f"{who}만 빠뜨린 행 (처음 {len(ex)}개):", ""]
                for e in ex:
                    where = f"{e['doc']} · {e['list']} · {e['row'] + 1}행"
                    link = f"[{e['bundle']}]({viewer_dir}/b_{e['bundle']}.html)" if viewer_dir else e["bundle"]
                    L.append(f"- {link} {where} — {a}: {e['a']}, {b}: {e['b']}" + (" (위 행과 글자 같음)" if e["same_text_prev"] else ""))
            L.append("")
    for pair, kinds in prb.items():
        a, b = pair.split(" vs ")
        L += [f"## 통제 실험: {a} vs {b}", ""] + _head(a, b, "실험 · 조건")
        for kind in KINDS:
            for cond in ORDER.get(kind, []):
                for key in (cond, f"{cond} 반복 묶음 안"):
                    c = kinds.get(kind, {}).get(key)
                    if c:
                        L.append(_row(f"{TITLE[kind].split(' (')[0]} · {key}", c))
        L.append("")
    return "\n".join(L) + "\n"


def run_paired(rows_path, probe_dirs: dict, out, viewer_dir: str | None = "viewer") -> str:
    out = Path(out)
    obs = observe(read_jsonl(rows_path))
    prb = probes(probe_dirs) if len(probe_dirs) > 1 else {}
    md = report_md(obs, prb, viewer_dir)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    out.with_suffix(".json").write_text(json.dumps({"observe": obs, "probes": prb}, ensure_ascii=False, indent=1,
                                                   default=str), encoding="utf-8")
    return md
