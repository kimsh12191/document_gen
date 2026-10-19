"""1단계 관찰의 기본 자료: 정답 행 하나하나의 결과 분류와 특징.

  python -m mpx rows --data data/test --pred preds/*.jsonl --out rows.jsonl

결과 분류 (classify_bundle)
  정답 행과 예측 행을 순서를 지키며 맞춘다(score.align, 칸 절반 이상 같으면 짝). 짝이 없는 정답 행은 앞뒤 짝 사이의
  '빈자리'를 본다.
    exact       모든 칸 맞음
    partial     짝은 지어졌으나 일부 칸 틀림
    misread     빈자리에 예측 행이 있음 (행은 냈으나 절반 이상 틀림). 빈자리 안에서 순서대로 짝지어 남는 정답 행만 아래로
    misplaced   다른 목록·다른 문서의 남는 예측 행과 짝이 됨
    skipped     그 뒤에도 출력이 이어지는데 이 행이 없음                              ← 누락
    cut_length  출력 단위가 길이 상한에 잘렸고, 이 행이 마지막으로 낸 행보다 뒤        ← 누락
    cut_stop    잘리지 않았는데 이 행이 마지막으로 낸 행보다 뒤 (모델이 스스로 끝냄)   ← 누락
    doc_missing 문서를 못 찾았고 위에 해당하지 않음                                    ← 누락
  출력 단위: 한 번에 넣기는 답 전체, 쪽 단위는 쪽마다의 답. 쪽 단위는 예측 행이 어느 쪽 답에서 왔는지
  (merge_pages 의 row_pages)로 '그 쪽 답에서 마지막으로 낸 행'을 찾는다.

행 특징 (row_records)
  glyph_tok   칸 글자 높이(중앙값)를 모델 입력 크기로 줄인 뒤 토큰(32px) 단위로
  pitch_tok   바로 위 행과의 세로 간격, 토큰 단위 (쪽의 첫 행은 없음)
  page_tokens 그 쪽 이미지의 토큰 수 (모델 입력 기준)
  y_top       쪽 안 세로 위치 0(위)~1(아래)
  n_images    그 요청에 들어간 이미지 수
  rows_before 출력에서 이 행 앞에 나올 정답 행 수 (묶음 서류 순서 기준 추정; 쪽 단위는 그 쪽 안에서)
  row_frac, list_len  목록 안 위치(0~1)와 목록 길이
  sim_neighbor 위·아래 행과 같은 값인 칸의 비율 (큰 쪽)
  same_text_prev 글자 칸(적요·기재내용 같은 text 타입)이 모두 바로 위 행과 같음 ('같은 글자 반복' 행)
  n_cells, chars      채워진 칸 수, 글자 수
  boundary, cont, no_header, augmented, heavy   쪽 경계 행, 이어지는 쪽의 행, 머리글 없는 쪽의 행, 증강, 긴 목록 서류
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

from docgen.bench.metrics import norm_text

from .common import PATCH, fit, page_budget, read_jsonl, tokens_of
from .gen import load
from .pages import flatten, page_views, split_key
from .score import MATCH_MIN, _filled, align, gt_docs, match_docs, row_sim

OUTCOMES = ("exact", "partial", "misread", "misplaced", "skipped", "cut_length", "cut_stop", "doc_missing")
DROPPED = ("skipped", "cut_length", "cut_stop", "doc_missing")
SYMBOL = {"exact": "✓", "partial": "△", "misread": "≠", "misplaced": "↷", "skipped": "✗", "cut_length": "✂",
          "cut_stop": "■", "doc_missing": "∅"}
NAME = {"exact": "정확", "partial": "일부 틀림", "misread": "잘못 읽음", "misplaced": "다른 곳에", "skipped": "건너뜀",
        "cut_length": "길이에 잘림", "cut_stop": "스스로 끝냄", "doc_missing": "문서 못 찾음"}


# ---------------------------------------------------------------------------
# 결과 분류
# ---------------------------------------------------------------------------

def _gap_assign(gi: list[int], pj: list[int], sim) -> dict[int, tuple[int, float]]:
    """빈자리 안에서 순서를 지키며 min(len) 쌍을 짝짓는다 (유사도 합이 가장 큰 것). {정답 행: (예측 행, 유사도)}."""
    a, b = len(gi), len(pj)
    if not a or not b:
        return {}
    s = [[sim(x, y) for y in pj] for x in gi]
    f = [[(0, 0.0)] * (b + 1) for _ in range(a + 1)]
    for x in range(a - 1, -1, -1):
        for y in range(b - 1, -1, -1):
            c, v = f[x + 1][y + 1]
            f[x][y] = max((c + 1, v + s[x][y]), f[x + 1][y], f[x][y + 1])
    out, x, y = {}, 0, 0
    while x < a and y < b:
        c, v = f[x + 1][y + 1]
        if f[x][y] == (c + 1, v + s[x][y]):
            out[gi[x]] = (pj[y], s[x][y])
            x, y = x + 1, y + 1
        elif f[x][y] == f[x + 1][y]:
            x += 1
        else:
            y += 1
    return out


def classify_list(grows: list[dict], prows: list[dict]) -> list[list]:
    """정답 행마다 [결과, 예측 행 번호, 유사도]. 결과는 exact/partial/misread, 빈자리에 예측 행이 없으면 'missing'."""
    n, m = len(grows), len(prows)
    pairs = align(grows, prows)
    res = [["missing", None, 0.0] for _ in range(n)]
    for i, j, s in pairs:
        res[i] = ["exact" if s == 1.0 else "partial", j, s]
    anchors = [(-1, -1)] + [(i, j) for i, j, _ in pairs] + [(n, m)]
    for (i0, j0), (i1, j1) in zip(anchors, anchors[1:]):
        got = _gap_assign(list(range(i0 + 1, i1)), list(range(j0 + 1, j1)), lambda x, y: row_sim(grows[x], prows[y])[0])
        for i, (j, s) in got.items():
            res[i] = ["misread", j, s]
    return res


def _flat_lists(doc: dict | None) -> dict[str, list[dict]]:
    lists = (doc or {}).get("lists") or {}
    return {p: [flatten(r) for r in rows if isinstance(r, dict)] for p, rows in lists.items() if isinstance(rows, list)}


def classify_lists(gt_lists: dict[str, list[dict]], pred_lists: dict, truncated: bool) -> dict[str, list[dict]]:
    """답 하나(출력 단위 하나)의 목록들 → {목록: [행마다 {outcome, j, sim}]}. 통제 실험(probe)에서 쓴다.
    pred_lists 는 모델 답의 lists (행은 중첩이어도 됨)."""
    pflat = {p: [flatten(r) for r in rows if isinstance(r, dict)] for p, rows in (pred_lists or {}).items()
             if isinstance(rows, list)}
    rank = list(pflat)
    out, used = {}, set()
    for path, grows in gt_lists.items():
        res = classify_list(grows, pflat.get(path, []))
        out[path] = [{"outcome": oc, "j": j, "sim": s, "where": path} for oc, j, s in res]
        used |= {(path, j) for _, j, _ in res if j is not None}
    for path, entries in out.items():
        for k, e in enumerate(entries):
            if e["outcome"] != "missing":
                continue
            best = max(((row_sim(gt_lists[path][k], r)[0], (p, j)) for p, rows in pflat.items() if p != path
                        for j, r in enumerate(rows) if (p, j) not in used), default=(0.0, None))
            if best[0] >= MATCH_MIN:
                used.add(best[1])
                e.update(outcome="misplaced", where=best[1][0], j=best[1][1], sim=best[0])
    last = max([(rank.index(p), j) for p, rows in pflat.items() for j in range(len(rows))], default=(-1, -1))
    for path, entries in out.items():
        r = rank.index(path) if path in rank else len(rank)
        for k, e in enumerate(entries):
            if e["outcome"] != "missing":
                continue
            before = [x["j"] for x in entries[:k] if x["j"] is not None and x["where"] == path]
            pos = (r, (max(before) if before else -1) + 0.5)
            e["outcome"] = ("cut_length" if truncated else "cut_stop") if pos > last else "skipped"
    return out


def classify_bundle(bundle: dict, labels: dict, pred: dict) -> dict[tuple[int, str], list[dict]]:
    """{(정답 문서 번호, 목록): [행마다 {outcome, pi, j, sim, unit, truncated}]} — 묶음의 모든 정답 문서."""
    gts = gt_docs(bundle, labels)
    pdocs = pred.get("docs") or []
    m = match_docs(gts, pdocs)
    pflat = [_flat_lists(d) for d in pdocs]
    trunc = pred.get("truncated") or []
    pagewise = pred.get("method") == "pagewise"

    out: dict[tuple[int, str], list[dict]] = {}
    used = set()
    for gi, g in enumerate(gts):
        pi = m.get(gi)
        for path, grows in g["lists"].items():
            prows = pflat[pi].get(path, []) if pi is not None else []
            entries = []
            for k, (oc, j, s) in enumerate(classify_list(grows, prows)):
                unit = g["pages"][g["row_page"][path][k]] if pagewise else 0
                entries.append({"outcome": oc, "pi": pi, "j": j, "sim": s, "unit": unit})
                if j is not None:
                    used.add((pi, path, j))
            out[(gi, path)] = entries

    # 다른 목록·다른 문서에 들어간 행
    spare = [(pi, path, j, r) for pi, lists in enumerate(pflat) for path, rows in lists.items()
             for j, r in enumerate(rows) if (pi, path, j) not in used]
    for (gi, path), entries in out.items():
        for k, e in enumerate(entries):
            if e["outcome"] != "missing":
                continue
            grow = gts[gi]["lists"][path][k]
            best = max(((row_sim(grow, r)[0], (pi, p, j)) for pi, p, j, r in spare
                        if (pi, p, j) not in used and not (pi == e["pi"] and p == path)), default=(0.0, None))
            if best[0] >= MATCH_MIN:
                used.add(best[1])
                e.update(outcome="misplaced", pi=best[1][0], j=best[1][2], sim=best[0], where=best[1][1])

    # 남은 누락: 출력 단위에서 마지막으로 낸 행보다 뒤인가
    if pagewise:
        for (gi, path), entries in out.items():
            pi = m.get(gi)
            rp = ((pdocs[pi].get("row_pages") or {}).get(path) or []) if pi is not None else []
            for k, e in enumerate(entries):
                if e["outcome"] != "missing":
                    continue
                later = any(x["j"] is not None and x["pi"] == pi and x["j"] < len(rp) and rp[x["j"]] == e["unit"]
                            for x in entries[k + 1:])
                e["truncated"] = bool(trunc[e["unit"] - 1]) if e["unit"] - 1 < len(trunc) else False
                e["outcome"] = "skipped" if later else ("cut_length" if e["truncated"] else "cut_stop")
    else:
        rank = [list(((d or {}).get("lists") or {}).keys()) for d in pdocs]
        last = max([(pi, -1, -1.0) for pi in range(len(pdocs))]
                   + [(pi, rank[pi].index(p), float(j)) for pi, lists in enumerate(pflat) for p, rows in lists.items()
                      for j in range(len(rows))], default=(-1, -1, -1.0))
        truncated = bool(trunc[0]) if trunc else False
        for (gi, path), entries in out.items():
            pi = m.get(gi)
            for k, e in enumerate(entries):
                if e["outcome"] != "missing":
                    continue
                if pi is None:  # 문서를 못 찾음: 앞 정답 문서의 짝 바로 뒤에 나왔어야 한다
                    prev = [m[x] for x in range(gi) if x in m]
                    pos = (max(prev) + 0.5 if prev else -0.5, 0, 0.0)
                else:
                    r = rank[pi].index(path) if path in rank[pi] else len(rank[pi])
                    before = [x["j"] for x in entries[:k] if x["j"] is not None and x["pi"] == pi and x.get("where", path) == path]
                    pos = (pi, r, (max(before) if before else -1) + 0.5)
                e["truncated"] = truncated
                if pos > last:
                    e["outcome"] = "cut_length" if truncated else "cut_stop"
                else:
                    e["outcome"] = "doc_missing" if pi is None else "skipped"
    return out


# ---------------------------------------------------------------------------
# 행 특징
# ---------------------------------------------------------------------------

def row_geometry(label: dict) -> dict[str, list[dict]]:
    """{목록: [행마다 {page, glyph_px, y_top_px, y_top, pitch_px}]} — gt_doc 의 행 순서와 같다."""
    views = page_views(label)
    box = {f["key"]: f for f in label["fields"] if f.get("bbox")}
    out: dict[str, list[dict]] = {}
    for k, v in enumerate(views):
        h = (label.get("pages") or [{}] * len(views))[k].get("height") or 1
        for path, rows in v["lists"].items():
            prev_top = None
            for idx, cells in rows:
                bs = [box[f"{path}.{idx}.{rest}" if rest else f"{path}.{idx}"]["bbox"] for rest in cells
                      if (f"{path}.{idx}.{rest}" if rest else f"{path}.{idx}") in box
                      and box[f"{path}.{idx}.{rest}" if rest else f"{path}.{idx}"].get("page", 0) == k]
                top = min(b[1] for b in bs) if bs else None
                out.setdefault(path, []).append({
                    "page": k, "glyph_px": statistics.median(b[3] - b[1] for b in bs) if bs else None,
                    "y_top_px": top, "y_top": top / h if top is not None else None,
                    "pitch_px": top - prev_top if top is not None and prev_top is not None and top > prev_top else None})
                prev_top = top if top is not None else prev_top
    return out


def _same_ratio(a: dict, b: dict | None) -> float:
    if not b:
        return 0.0
    keys = [k for k, v in a.items() if _filled(v[0])]
    if not keys:
        return 0.0
    return sum(1 for k in keys if k in b and norm_text(a[k][0]) == norm_text(b[k][0])) / len(keys)


def same_text_prev(rows: list[dict], i: int) -> bool:
    """정답 행 i 의 글자(text 타입) 칸이 하나 이상 있고, 모두 바로 위 행과 같은가."""
    if i == 0:
        return False
    cur = {k: v[0] for k, v in rows[i].items() if v[1] == "text" and _filled(v[0])}
    prev = rows[i - 1]
    return bool(cur) and all(k in prev and norm_text(prev[k][0]) == norm_text(c) for k, c in cur.items())


def input_scale(label: dict, page: int, method: str, n_images: int, budget: int, per_page: int | None = None) -> float:
    """원래 쪽 이미지 → 모델 입력 크기의 비율 (run.py 가 줄이는 방식과 같게)."""
    p = (label.get("pages") or [{}])[page]
    w, h = p.get("width"), p.get("height")
    if not w or not h:
        return 1.0
    if per_page is None and method == "allatonce":
        per_page = page_budget(n_images, budget)
    return fit(w, h, per_page)[0] / w


def row_records(bundle: dict, labels: dict, pred: dict, run_name: str, budget: int = 12000) -> list[dict]:
    """묶음 하나, 실행 하나 → 대상 서류의 정답 행마다 결과와 특징."""
    gts = gt_docs(bundle, labels)
    classes = classify_bundle(bundle, labels, pred)
    method = pred.get("method")
    budget = pred.get("budget") or budget
    n_bundle = len(bundle["pages"])
    usage = pred.get("usage") or []
    recs = []
    before_bundle = 0
    for gi, g in enumerate(gts):
        lb = labels[g["id"]]
        geo = row_geometry(lb)
        for path, grows in g["lists"].items():
            pages = g["row_page"][path]
            first = pages[0] if pages else 0
            boundary = {i for i in range(1, len(pages)) if pages[i] != pages[i - 1]}
            boundary |= {i - 1 for i in boundary}
            for i, grow in enumerate(grows):
                if not g["target"]:
                    continue
                e = classes[(gi, path)][i]
                k = pages[i]
                n_images = 1 if method == "pagewise" else n_bundle
                s = input_scale(lb, k, method, n_images, budget)
                p = (lb.get("pages") or [{}])[k]
                gm = geo.get(path, [{}] * len(grows))[i] if len(geo.get(path, [])) == len(grows) else {}
                cells = [v[0] for v in grow.values() if _filled(v[0])]
                same_page_before = sum(1 for x in pages[:i] if x == k)
                u = usage[e["unit"] - 1] if method == "pagewise" and 0 < e["unit"] <= len(usage) else (usage[0] if usage else {})
                recs.append({
                    "run": run_name, "method": method, "bundle": bundle["id"], "doc": g["id"], "doc_type": g["type"],
                    "list": path, "row": i, "outcome": e["outcome"], "dropped": e["outcome"] in DROPPED, "sim": round(e["sim"], 3),
                    "truncated": bool(e.get("truncated")), "finish_reason": (u or {}).get("finish_reason"),
                    "list_len": len(grows), "row_frac": i / max(1, len(grows) - 1), "page_in_doc": k, "doc_pages": g["n_pages"],
                    "n_images": n_images,
                    "page_tokens": tokens_of(round((p.get("width") or 0) * s), round((p.get("height") or 0) * s)) if p.get("width") else None,
                    "glyph_tok": gm["glyph_px"] * s / PATCH if gm.get("glyph_px") else None,
                    "pitch_tok": gm["pitch_px"] * s / PATCH if gm.get("pitch_px") else None,
                    "y_top": gm.get("y_top"),
                    "rows_before": same_page_before if method == "pagewise" else before_bundle + i,
                    "sim_neighbor": max(_same_ratio(grow, grows[i - 1] if i else None),
                                        _same_ratio(grow, grows[i + 1] if i + 1 < len(grows) else None)),
                    "same_text_prev": same_text_prev(grows, i),
                    "n_cells": len(cells), "chars": sum(len(str(c)) for c in cells),
                    "boundary": i in boundary, "cont": k > first,
                    "no_header": bool(g["no_repeat_header"]) and k > 0, "augmented": bool(g["augment"]),
                    "heavy": bool(lb.get("heavy"))})
            before_bundle += len(grows)
    return recs


def collect(data_dir, pred_paths, out) -> Path:
    """예측 파일들 → rows.jsonl (실행 이름 = 파일 이름)."""
    bundles, labels = load(data_dir)
    by_id = {b["id"]: b for b in bundles}
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for p in pred_paths:
            for pred in read_jsonl(p):
                if pred["bundle"] in by_id:
                    for r in row_records(by_id[pred["bundle"]], labels, pred, Path(p).stem):
                        f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return out


__all__ = ["OUTCOMES", "DROPPED", "classify_list", "classify_bundle", "row_records", "collect", "split_key"]
