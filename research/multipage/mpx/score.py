"""채점: 묶음 하나의 예측 문서 목록을 정답 문서들과 맞춰 보고, 문서 나누기·항목·목록 행·쪽 경계·합계 검사를 센다.

목록 행은 순서를 지키며 맞춘다(행 유사도 0.5 이상만 짝, 동적 계획법). 그래서 빠진 행·겹친 행이 그대로 드러난다.
  행 유사도 = 정답 행의 비어 있지 않은 칸 중 맞힌 칸의 비율
  정확한 행 = 모든 칸을 맞힌 행
  경계 행   = 목록이 쪽을 넘어갈 때 앞 쪽 마지막 행과 다음 쪽 첫 행
  이어지는 행 = 목록이 시작된 쪽 다음 쪽부터 나오는 행 (앞 쪽 정보가 있어야 읽히는 행)
"""
from __future__ import annotations

from collections import defaultdict

from docgen.bench.metrics import loose_text, norm_text, to_number, value_match, yes_no

from .pages import flatten, leaf, page_views, split_key

MATCH_MIN = 0.5


# ---------------------------------------------------------------------------
# 정답 문서
# ---------------------------------------------------------------------------

def gt_doc(label: dict, bundle_pages: list[int]) -> dict:
    """채점용 정답: 평탄 항목 {키: (값, 타입, 정규화값)}, 목록 {이름: [행 {키: (값, 타입, 정규화값)}]}, 행이 있는 쪽."""
    views = page_views(label)
    typed = {}
    for f in label["fields"]:
        if not (f.get("group") or f.get("group_only")):
            typed[f["key"]] = (leaf(f), f.get("type"), f.get("norm"))
    fields, lists, row_page = {}, {}, {}
    for k, v in enumerate(views):
        for key in v["fields"]:
            fields[key] = typed[key]
        for path, rows in v["lists"].items():
            for idx, cells in rows:
                lists.setdefault(path, []).append({rest: typed[f"{path}.{idx}.{rest}" if rest else f"{path}.{idx}"]
                                                   for rest in cells})
                row_page.setdefault(path, []).append(k)
    return {"id": label["id"], "type": label["doc_type"], "name": label["doc_name"], "pages": bundle_pages,
            "fields": fields, "lists": lists, "row_page": row_page, "no_repeat_header": label.get("no_repeat_header"),
            "augment": label.get("augment"), "n_pages": len(views)}


def gt_docs(bundle: dict, labels: dict) -> list[dict]:
    pages = defaultdict(list)
    for i, p in enumerate(bundle["pages"], 1):
        pages[p["doc"]].append(i)
    return [gt_doc(labels[sid], pages[sid]) for sid in bundle["docs"]]


# ---------------------------------------------------------------------------
# 값 비교
# ---------------------------------------------------------------------------

def _match(pred, gt) -> bool:
    value, typ, norm = gt
    if isinstance(value, bool):
        return (pred if isinstance(pred, bool) else yes_no(pred)) is value
    return value_match(pred, value, typ, norm)


def _filled(v) -> bool:
    return v is not None and v != "" and v != [] and v != {}


def row_sim(gt_row: dict, pred_row: dict) -> tuple[float, int]:
    """(맞힌 비율, 채워진 정답 칸 수)."""
    cells = [(k, g) for k, g in gt_row.items() if _filled(g[0])]
    if not cells:
        return (1.0 if not any(_filled(v) for v in pred_row.values()) else 0.0), 0
    hit = sum(1 for k, g in cells if norm_text(pred_row.get(k)) == norm_text(g[0]) or _match(pred_row.get(k), g))
    return hit / len(cells), len(cells)


def align(gt_rows: list[dict], pred_rows: list[dict]) -> list[tuple[int, int, float]]:
    """순서를 지키는 최대 유사도 짝짓기. [(정답 행, 예측 행, 유사도)]."""
    n, m = len(gt_rows), len(pred_rows)
    sim = [[row_sim(g, p)[0] for p in pred_rows] for g in gt_rows]
    best = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            s = sim[i][j]
            take = s + best[i + 1][j + 1] if s >= MATCH_MIN else -1.0
            best[i][j] = max(take, best[i + 1][j], best[i][j + 1])
    pairs, i, j = [], 0, 0
    while i < n and j < m:
        s = sim[i][j]
        if s >= MATCH_MIN and abs(best[i][j] - (s + best[i + 1][j + 1])) < 1e-9:
            pairs.append((i, j, s))
            i, j = i + 1, j + 1
        elif best[i][j] == best[i + 1][j]:
            i += 1
        else:
            j += 1
    return pairs


# ---------------------------------------------------------------------------
# 합계·흐름 검사 (정답 없이 예측만으로 할 수 있는 검사)
# ---------------------------------------------------------------------------

def _num(v):
    return to_number(v) if _filled(v) else 0.0


def balance_chain(fields: dict, rows: list[dict]) -> tuple[int, int]:
    """거래내역: 앞 잔액 - 출금 + 입금 = 이 행 잔액 인 행 수 / 검사한 행 수. 첫 행은 opening_balance 로."""
    ok = total = 0
    prev = to_number(fields.get("opening_balance")) if _filled(fields.get("opening_balance")) else None
    for r in rows:
        bal = to_number(r.get("balance")) if _filled(r.get("balance")) else None
        out, inn = _num(r.get("out")), _num(r.get("in"))
        if prev is not None and bal is not None and out is not None and inn is not None:
            total += 1
            ok += (out or inn) and abs(prev - out + inn - bal) < 0.5  # 금액 없는 행(같은 행 복사 등)은 실패로
        prev = bal
    return ok, total


def sum_check(fields: dict, rows: list[dict], row_key: str, total_key: str) -> tuple[int, int]:
    """목록 금액 합 = 합계 칸 이면 (1, 1), 아니면 (0, 1). 읽을 수 없으면 (0, 0)."""
    total = to_number(fields.get(total_key)) if _filled(fields.get(total_key)) else None
    vals = [to_number(r.get(row_key)) for r in rows if _filled(r.get(row_key))]
    if total is None or not vals or any(v is None for v in vals):
        return 0, 0
    return int(abs(sum(vals) - total) < 0.5), 1


def consistency(doc_type: str, fields: dict, lists: dict) -> dict:
    out = {}
    if doc_type == "bank_statement":
        out["balance_chain"] = balance_chain(fields, lists.get("rows", []))
    elif doc_type == "commercial_invoice":
        out["items_sum"] = sum_check(fields, lists.get("items", []), "amount", "total_amount")
    return out


# ---------------------------------------------------------------------------
# 묶음 하나 채점
# ---------------------------------------------------------------------------

def _same_type(pred: dict, gt: dict) -> bool:
    t = loose_text(pred.get("type"))
    return bool(t) and t in (loose_text(gt["type"]), loose_text(gt["name"])) or loose_text(pred.get("name")) == loose_text(gt["name"])


def match_docs(gts: list[dict], preds: list[dict]) -> dict[int, int]:
    """정답 문서 → 예측 문서. 쪽 집합이 가장 많이 겹치는 것부터 하나씩 (종류가 같으면 우선)."""
    cand = []
    for gi, g in enumerate(gts):
        for pi, p in enumerate(preds):
            a, b = set(g["pages"]), set(p.get("pages") or [])
            inter = len(a & b)
            if inter:  # 같으면 종류가 같은 것, 그다음 문서 첫 쪽을 가진 것을 먼저
                cand.append((inter / len(a | b), _same_type(p, g), min(g["pages"]) in b, -pi, gi, pi))
    cand.sort(reverse=True)
    out, used = {}, set()
    for *_, gi, pi in cand:
        if gi not in out and pi not in used:
            out[gi] = pi
            used.add(pi)
    return out


def _flat_rows(rows) -> list[dict]:
    return [flatten(r) for r in rows if isinstance(r, dict)]


def score_doc(g: dict, p: dict | None) -> dict:
    pf = flatten(p.get("fields") or {}) if p else {}
    plists = {k: _flat_rows(v) for k, v in (p.get("lists") or {}).items()} if p else {}
    r = defaultdict(float)
    # 항목
    for key, gv in g["fields"].items():
        if _filled(gv[0]):
            r["field_gt"] += 1
            r["field_hit"] += _filled(pf.get(key)) and _match(pf.get(key), gv)
    r["field_pred"] = sum(1 for k, v in pf.items() if _filled(v))
    r["field_pred_hit"] = sum(1 for k, v in pf.items() if _filled(v) and k in g["fields"] and _match(v, g["fields"][k]))
    # 목록
    for path, grows in g["lists"].items():
        prows = plists.get(path, [])
        pairs = align(grows, prows)
        pages = g["row_page"][path]
        first = pages[0] if pages else 0
        boundary = {i for i in range(1, len(pages)) if pages[i] != pages[i - 1]}
        boundary |= {i - 1 for i in boundary}
        exact = {i for i, _, s in pairs if s == 1.0}
        matched = {i for i, _, _ in pairs}
        r["row_gt"] += len(grows)
        r["row_pred"] += len(prows)
        r["row_exact"] += len(exact)
        r["row_matched"] += len(matched)
        r["row_dup"] += sum(1 for j in range(1, len(prows)) if prows[j] == prows[j - 1] and prows[j])
        r["count_abs_err"] += abs(len(prows) - len(grows))
        for i, gr in enumerate(grows):
            n = sum(1 for v in gr.values() if _filled(v[0]))
            r["cell_gt"] += n
        for i, j, s in pairs:
            r["cell_hit"] += s * sum(1 for v in grows[i].values() if _filled(v[0]))
        r["boundary_gt"] += len(boundary)
        r["boundary_exact"] += len(boundary & exact)
        cont = {i for i, pg in enumerate(pages) if pg > first}
        r["cont_gt"] += len(cont)
        r["cont_exact"] += len(cont & exact)
    for path in set(plists) - set(g["lists"]):
        r["row_pred"] += len(plists[path])
    # 합계 검사 (예측, 그리고 같은 검사가 정답에서 성립하는지)
    gt_fields = {k: v[0] for k, v in g["fields"].items()}
    gt_lists = {k: [{c: v[0] for c, v in row.items()} for row in rows] for k, rows in g["lists"].items()}
    gt_ok = consistency(g["type"], gt_fields, gt_lists)
    pred_ok = consistency(g["type"], pf, plists)
    for name, (ok, total) in pred_ok.items():
        if gt_ok.get(name, (0, 0))[1] and gt_ok[name][0] == gt_ok[name][1]:  # 정답에서 성립하는 검사만
            r[f"check_{name}_ok"] += ok
            r[f"check_{name}_n"] += total
    return dict(r)


def score_bundle(bundle: dict, labels: dict, pred_docs: list[dict]) -> dict:
    gts = gt_docs(bundle, labels)
    m = match_docs(gts, pred_docs)
    n_pages = len(bundle["pages"])
    # 쪽 배정: 쪽 i 가 정답 문서의 짝 예측 문서에 들어 있으면 맞음
    page_ok = 0
    for gi, g in enumerate(gts):
        p = pred_docs[m[gi]] if gi in m else None
        page_ok += len(set(g["pages"]) & set(p.get("pages") or [])) if p else 0
    docs = []
    for gi, g in enumerate(gts):
        p = pred_docs[m[gi]] if gi in m else None
        s = score_doc(g, p)
        s.update(doc=g["id"], type=g["type"], n_pages=g["n_pages"], no_repeat_header=bool(g["no_repeat_header"]),
                 augment=g["augment"], found=p is not None, type_ok=bool(p) and _same_type(p, g),
                 pages_exact=bool(p) and sorted(p.get("pages") or []) == sorted(g["pages"]))
        docs.append(s)
    return {"bundle": bundle["id"], "n_pages": n_pages, "page_ok": page_ok, "n_docs": len(gts),
            "n_pred_docs": len(pred_docs), "docs": docs}


# ---------------------------------------------------------------------------
# 모으기
# ---------------------------------------------------------------------------

def _ratio(a, b):
    return a / b if b else None


def summarize(results: list[dict], group_key=None) -> dict:
    """묶음 채점 결과들 → 지표. group_key(doc) 가 있으면 그 값별로도."""
    def agg(docs, bundles=None):
        t = defaultdict(float)
        for d in docs:
            for k, v in d.items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    t[k] += v
        out = {"docs": len(docs),
               "doc_found": _ratio(sum(d["found"] for d in docs), len(docs)),
               "doc_type_acc": _ratio(sum(d["type_ok"] for d in docs), len(docs)),
               "doc_pages_exact": _ratio(sum(d["pages_exact"] for d in docs), len(docs)),
               "field_recall": _ratio(t["field_hit"], t["field_gt"]),
               "field_precision": _ratio(t["field_pred_hit"], t["field_pred"]),
               "row_recall": _ratio(t["row_exact"], t["row_gt"]),
               "row_precision": _ratio(t["row_exact"], t["row_pred"]),
               "row_dropped": _ratio(t["row_gt"] - t["row_matched"], t["row_gt"]),
               "row_dup": _ratio(t["row_dup"], t["row_pred"]),
               "cell_recall": _ratio(t["cell_hit"], t["cell_gt"]),
               "boundary_row_recall": _ratio(t["boundary_exact"], t["boundary_gt"]),
               "cont_row_recall": _ratio(t["cont_exact"], t["cont_gt"]),
               "count_abs_err": _ratio(t["count_abs_err"], len(docs))}
        for k in list(t):
            if k.startswith("check_") and k.endswith("_ok"):
                name = k[len("check_"):-len("_ok")]
                out[f"check_{name}"] = _ratio(t[k], t[f"check_{name}_n"])
        for name in ("row", "field"):  # 정답이 있는데 예측이 비면 F1 = 0
            p, r = out[f"{name}_precision"], out[f"{name}_recall"]
            out[f"{name}_f1"] = None if r is None else (2 * p * r / (p + r) if p and r else 0.0)
        if bundles is not None:
            out["page_assign_acc"] = _ratio(sum(b["page_ok"] for b in bundles), sum(b["n_pages"] for b in bundles))
        return out

    all_docs = [d for b in results for d in b["docs"]]
    summary = {"all": agg(all_docs, results)}
    if group_key:
        groups = defaultdict(list)
        for d in all_docs:
            groups[group_key(d)].append(d)
        for k in sorted(groups, key=str):
            summary[str(k)] = agg(groups[k])
    return summary


def cost(preds: list[dict]) -> dict:
    """실행 기록의 비용: 묶음당 요청 수, 입력·출력 토큰, 가장 긴 입력, 이미지 토큰, 시간."""
    n = len(preds) or 1
    usage = [u for p in preds for u in p.get("usage", []) if u]
    keys = ("requests", "prompt_tokens", "completion_tokens", "image_tokens", "latency")
    tot = {k: 0.0 for k in keys}
    max_prompt = 0
    for p in preds:
        tot["requests"] += len(p.get("usage", []))
        tot["image_tokens"] += sum(p.get("image_tokens", []))
        tot["latency"] += p.get("latency", 0.0)
    for u in usage:
        tot["prompt_tokens"] += u.get("prompt_tokens") or 0
        tot["completion_tokens"] += u.get("completion_tokens") or 0
        max_prompt = max(max_prompt, u.get("prompt_tokens") or 0)
    out = {f"{k}_per_bundle": v / n for k, v in tot.items()}
    out["max_prompt_tokens"] = max_prompt
    return out


# ---------------------------------------------------------------------------
# 정답 없는 실제 서류 검사
# ---------------------------------------------------------------------------

def _strings(obj) -> list[str]:
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        return [s for v in obj.values() for s in _strings(v)]
    if isinstance(obj, list):
        return [s for v in obj for s in _strings(v)]
    return []


def ocr_blob(path) -> str:
    """사내 OCR JSON(형식 무관)의 모든 문자열을 이어 붙여 정규화한 것."""
    import json
    from pathlib import Path

    p = Path(path)
    if not p.exists():
        return ""
    return norm_text("".join(_strings(json.loads(p.read_text(encoding="utf-8-sig")))))


def check_real(bundle: dict, pred_docs: list[dict], data_dir) -> dict:
    """정답 없이: 예측 값이 그 쪽들의 사내 OCR 글자에 있는 비율, 잔액 흐름·품목 합계 검사."""
    from pathlib import Path

    blobs = {i: ocr_blob(Path(data_dir) / p["ocr"]) for i, p in enumerate(bundle["pages"], 1) if p.get("ocr")}
    r = defaultdict(float)
    for d in pred_docs:
        flat = flatten(d.get("fields") or {})
        lists = {k: _flat_rows(v) for k, v in (d.get("lists") or {}).items()}
        values = [v for v in flat.values() if isinstance(v, str)] + [v for rows in lists.values() for row in rows
                                                                     for v in row.values() if isinstance(v, str)]
        blob = "".join(blobs.get(i, "") for i in d.get("pages") or [])
        if blob:
            vals = [norm_text(v) for v in values if len(norm_text(v)) >= 2]
            r["ocr_n"] += len(vals)
            r["ocr_found"] += sum(1 for v in vals if v in blob)
        r["rows"] += sum(len(v) for v in lists.values())
        for name, (ok, total) in consistency(_canon_type(d), flat, lists).items():
            r[f"check_{name}_ok"] += ok
            r[f"check_{name}_n"] += total
    r["docs"] = len(pred_docs)
    return dict(r)


def _canon_type(d: dict) -> str:
    t = loose_text(d.get("type")) or loose_text(d.get("name"))
    for doc_type, names in (("bank_statement", ("bankstatement", "거래내역확인서", "거래내역서")),
                            ("commercial_invoice", ("commercialinvoice", "상업송장", "인보이스"))):
        if t in names or any(n in t for n in names):
            return doc_type
    return t


def summarize_real(results: list[dict]) -> dict:
    t = defaultdict(float)
    for r in results:
        for k, v in r.items():
            t[k] += v
    out = {"bundles": len(results), "docs_per_bundle": _ratio(t["docs"], len(results)),
           "rows_per_bundle": _ratio(t["rows"], len(results)), "ocr_support": _ratio(t["ocr_found"], t["ocr_n"])}
    for k in list(t):
        if k.startswith("check_") and k.endswith("_ok"):
            name = k[len("check_"):-len("_ok")]
            out[f"check_{name}"] = _ratio(t[k], t[f"check_{name}_n"])
    return out


__all__ = ["score_bundle", "summarize", "cost", "gt_docs", "align", "row_sim", "consistency", "split_key"]
