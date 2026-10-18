"""2단계 통제 실험: 같은 쪽·같은 행을 두고 조건 하나만 바꿔, 그 쪽 행의 누락률을 잰다.

  python -m mpx probe --data data/test --out probes --base-url http://127.0.0.1:8000/v1 --model bank-ocr
  python -m mpx probe --data data/test --out probes --oracle [--simulate 0.1]        # 모델 없이 점검

실험 (KINDS)                       바꾸는 것                                   고정하는 것
  resolution  A  해상도             쪽 이미지 토큰 460 / 920 / 1800 / 원래      그 쪽 한 장, 그 쪽 행만 묻기
  scope       B  출력 길이          문서 전체 행을 묻기(doc) / 그 쪽 행만(page)  입력: 문서 전 쪽, 쪽당 920토큰
  images      C  이미지 수          대상 쪽 + 같은 묶음 다른 쪽 0 / 2 / 4 / 8장  쪽당 920토큰, 대상 쪽 행만 묻기
  header      D  머리글             머리글 없는 판(no_header) / 반복한 쌍둥이 판(header)의 이어지는 쪽  한 장, 원래 해상도
모든 질문에 그 서류의 목록 이름과 칸 이름을 알려 준다(키 이름 맞히기가 아니라 누락을 재기 위해).
header 실험은 gen --twins 로 만든 데이터에서만 문항이 생긴다.

파일 (<out>/)
  items.jsonl    문항 {id, kind, cond, bundle, doc, label, page, scope, images:[{image, budget}], prompt}
  answers.jsonl  답 {id, raw, truncated, usage, lists}   (있으면 남은 문항만 이어서)
  rows.jsonl     대상 쪽 정답 행마다 {kind, cond, doc, list, key, outcome, dropped, glyph_tok, page_tokens, out_pos}
  probes.md      실험·조건별 결과 분포와 누락률, 기준 조건과의 짝지은 비교
짝지은 비교: 같은 행(서류, 목록, 행 번호)이 기준 조건에서는 나왔는데 이 조건에서 빠진 수(+)와 그 반대(−).
"""
from __future__ import annotations

import json
import random
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .common import PATCH, dumps, fit, load_resized, read_jsonl, tokens_of, write_jsonl
from .gen import load
from .pages import doc_content, list_schema, page_answer, page_views
from .parse import parse_output
from .rows import DROPPED, NAME, OUTCOMES, classify_lists, row_geometry
from .score import gt_doc

KINDS = ("resolution", "scope", "images", "header")
RES_BUDGETS = {"460": 460, "920": 920, "1800": 1800, "full": None}
CTX = (0, 2, 4, 8)
PER_PAGE = 920
MIN_ROWS = 3
REF = {"resolution": "full", "scope": "page", "images": "0", "header": "header"}
TITLE = {"resolution": "A 해상도", "scope": "B 출력 길이 (묻는 범위)", "images": "C 이미지 수", "header": "D 머리글"}

FORMAT = ('형식: {{"lists": {{"목록 이름": [{{"칸 이름": "값"}}, ...]}}}}\n'
          "값은 적힌 그대로 옮기세요. 목록 이름과 칸 이름 (이대로 쓰세요): {cols}")
P_ONE = "이미지는 {name}의 한 쪽입니다. 이 쪽에 적힌 목록의 행을 위에서부터 하나도 빠뜨리지 말고 JSON 으로 옮기세요. 이 쪽에 없는 행은 쓰지 마세요.\n" + FORMAT
P_AMONG = ("이미지가 {n}장 있습니다. 그중 {pos}번째 이미지만 보세요. 그 이미지는 {name}의 한 쪽입니다. "
           "그 이미지에 적힌 목록의 행을 위에서부터 하나도 빠뜨리지 말고 JSON 으로 옮기세요. 다른 이미지의 행은 쓰지 마세요.\n" + FORMAT)
P_DOC = ("이미지 {n}장은 {name} 한 건의 1~{n}쪽입니다. 모든 쪽의 목록 행을 쪽 순서대로 하나도 빠뜨리지 말고 "
         "JSON 으로 옮기세요. 쪽이 바뀌어도 같은 목록이면 이어서 쓰세요.\n" + FORMAT)


def _cols(label: dict) -> str:
    return "; ".join(f"{p}[{', '.join(c)}]" for p, c in list_schema(label).items())


def _label(data_dir: Path, sid: str, cache: dict) -> dict:
    if sid not in cache:
        cache[sid] = json.loads((data_dir / "labels" / f"{sid}.json").read_text(encoding="utf-8"))
    return cache[sid]


def _rows_on(label: dict, k: int) -> int:
    return sum(len(r) for r in page_views(label)[k]["lists"].values()) if k < label["n_pages"] else 0


# ---------------------------------------------------------------------------
# 문항 만들기
# ---------------------------------------------------------------------------

def build(data_dir, out, kinds=KINDS, max_items: int = 40, seed: int = 0) -> Path:
    """실험마다 '기준 쪽'을 최대 max_items 개 골라 조건별 문항을 만든다 → <out>/items.jsonl."""
    data_dir, out = Path(data_dir), Path(out)
    bundles, labels = load(data_dir)
    cache = dict(labels)
    rng = random.Random(f"probe:{seed}")
    bases = []  # (묶음, 묶음 안 쪽 번호, 서류ID, 서류 안 쪽 번호)
    for b in bundles:
        for t, p in enumerate(b["pages"]):
            lb = labels[p["doc"]]
            if lb.get("target") and _rows_on(lb, p["page"]) >= MIN_ROWS:
                bases.append((b, t, p["doc"], p["page"]))
    rng.shuffle(bases)
    items = []

    def add(kind, cond, b, doc, label_id, k, scope, images, prompt):
        items.append({"id": f"{kind}:{doc}:p{k + 1}:{cond}", "kind": kind, "cond": cond, "bundle": b["id"], "doc": doc,
                      "label": label_id, "page": k, "scope": scope, "images": images, "prompt": prompt})

    for kind in kinds:
        picked = 0
        for b, t, doc, k in bases:
            if picked >= max_items:
                break
            lb = labels[doc]
            name, cols = lb["doc_name"], _cols(lb)
            if kind == "resolution":
                for cond, budget in RES_BUDGETS.items():
                    add(kind, cond, b, doc, doc, k, "page", [{"image": lb["images"][k], "budget": budget}],
                        P_ONE.format(name=name, cols=cols))
            elif kind == "scope":
                if lb["n_pages"] < 2:
                    continue
                imgs = [{"image": im, "budget": PER_PAGE} for im in lb["images"]]
                n = len(imgs)
                add(kind, "doc", b, doc, doc, k, "doc", imgs, P_DOC.format(n=n, name=name, cols=cols))
                add(kind, "page", b, doc, doc, k, "page", imgs, P_AMONG.format(n=n, pos=k + 1, name=name, cols=cols))
            elif kind == "images":
                others = sorted((i for i in range(len(b["pages"])) if i != t), key=lambda i: (abs(i - t), i))
                for m in CTX:
                    if m > len(others):
                        break
                    sel = sorted(others[:m] + [t])
                    imgs = [{"image": b["pages"][i]["image"], "budget": PER_PAGE} for i in sel]
                    prompt = P_ONE.format(name=name, cols=cols) if m == 0 else \
                        P_AMONG.format(n=len(imgs), pos=sel.index(t) + 1, name=name, cols=cols)
                    add(kind, str(m), b, doc, doc, k, "page", imgs, prompt)
            elif kind == "header":
                twin = lb.get("twin")
                if not twin or k == 0:
                    continue
                tl = _label(data_dir, twin, cache)
                if _rows_on(tl, k) < MIN_ROWS:
                    continue
                add(kind, "no_header", b, doc, doc, k, "page", [{"image": lb["images"][k], "budget": None}],
                    P_ONE.format(name=name, cols=cols))
                add(kind, "header", b, doc, twin, k, "page", [{"image": tl["images"][k], "budget": None}],
                    P_ONE.format(name=name, cols=cols))
            picked += 1
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out / "items.jsonl", items)
    return out / "items.jsonl"


# ---------------------------------------------------------------------------
# 실행
# ---------------------------------------------------------------------------

def oracle_lists(label: dict, item: dict) -> dict:
    views = page_views(label)
    if item["scope"] == "doc":
        return doc_content(views)["lists"]
    return page_answer(label, views, item["page"])["lists"]


def answer_item(item: dict, data_dir: Path, client, cache: dict, simulate: float = 0.0) -> dict:
    if client is None:
        from .run import simulate_cut, simulate_rows

        obj = {"lists": oracle_lists(_label(data_dir, item["label"], cache), item)}
        raw, cut, finish = dumps(obj), False, "stop"
        if simulate:
            rng = random.Random(f"probe-sim:{item['id']}")
            injected: dict = {}
            obj = simulate_rows(obj, rng, simulate, injected)
            raw, obj, cut, finish = simulate_cut(dumps(obj), obj, rng, simulate, injected, "")
        return {"id": item["id"], "raw": raw, "truncated": cut, "usage": {"finish_reason": finish},
                "lists": (obj or {}).get("lists") if isinstance(obj, dict) else {}}
    imgs = [load_resized(data_dir / im["image"], im["budget"]) for im in item["images"]]
    raw, u = client.ask(imgs, item["prompt"])
    obj, repaired = parse_output(raw)
    lists = obj.get("lists") if isinstance(obj, dict) and isinstance(obj.get("lists"), dict) else {}
    return {"id": item["id"], "raw": raw, "truncated": repaired or u.get("finish_reason") == "length", "usage": u,
            "lists": lists, "image_tokens": [tokens_of(*im.size) for im in imgs]}


def run_probes(data_dir, out, client=None, workers: int = 8, simulate: float = 0.0) -> Path:
    data_dir, out = Path(data_dir), Path(out)
    items = read_jsonl(out / "items.jsonl")
    path = out / "answers.jsonl"
    done = {r["id"] for r in read_jsonl(path)} if path.exists() else set()
    todo = [it for it in items if it["id"] not in done]
    cache: dict = {}
    with path.open("a", encoding="utf-8") as f, ThreadPoolExecutor(max(1, workers)) as ex:
        futs = [ex.submit(answer_item, it, data_dir, client, cache, simulate) for it in todo]
        for k, fu in enumerate(as_completed(futs), 1):
            f.write(json.dumps(fu.result(), ensure_ascii=False) + "\n")
            f.flush()
            print(f"\r통제 실험: {k}/{len(todo)}", end="", file=sys.stderr)
    print(file=sys.stderr)
    return path


# ---------------------------------------------------------------------------
# 채점과 보고서
# ---------------------------------------------------------------------------

def _row_keys(label: dict) -> dict[str, list[int]]:
    """gt_doc 목록 순서대로 각 행의 원래 행 번호 (같은 내용의 쌍둥이 판끼리 같은 행을 잇는 데 쓴다)."""
    out: dict[str, list[int]] = {}
    for v in page_views(label):
        for path, rows in v["lists"].items():
            out.setdefault(path, []).extend(idx for idx, _ in rows)
    return out


def score_probes(data_dir, out) -> Path:
    """답 → 대상 쪽 정답 행마다 결과 (<out>/rows.jsonl)."""
    data_dir, out = Path(data_dir), Path(out)
    items = {it["id"]: it for it in read_jsonl(out / "items.jsonl")}
    answers = {a["id"]: a for a in read_jsonl(out / "answers.jsonl")}
    cache: dict = {}
    recs = []
    for iid, it in items.items():
        a = answers.get(iid)
        if a is None:
            continue
        lb = _label(data_dir, it["label"], cache)
        g = gt_doc(lb, [])
        keys, geo = _row_keys(lb), row_geometry(lb)
        k = it["page"]
        if it["scope"] == "doc":
            gt_lists, sel = g["lists"], {p: list(range(len(r))) for p, r in g["lists"].items()}
        else:
            sel = {p: [i for i, pg in enumerate(g["row_page"][p]) if pg == k] for p in g["lists"]}
            gt_lists = {p: [g["lists"][p][i] for i in ix] for p, ix in sel.items() if ix}
            sel = {p: ix for p, ix in sel.items() if ix}
        res = classify_lists(gt_lists, a.get("lists") or {}, bool(a.get("truncated")))
        im = next((x for x in it["images"] if x["image"] == lb["images"][k]), it["images"][0])
        pw = lb["pages"][k]
        w, h = fit(pw["width"], pw["height"], im["budget"])
        scale = w / pw["width"]
        pos = 0
        for p, ix in sel.items():
            for local, i in enumerate(ix):
                e = res[p][local]
                pos += 1
                if g["row_page"][p][i] != k:
                    continue
                gm = geo[p][i] if len(geo.get(p, [])) == len(g["lists"][p]) else {}
                recs.append({"id": iid, "kind": it["kind"], "cond": it["cond"], "doc": it["doc"], "doc_type": lb["doc_type"],
                             "page": k, "list": p, "key": keys[p][i], "outcome": e["outcome"],
                             "dropped": e["outcome"] in DROPPED, "truncated": bool(a.get("truncated")),
                             "glyph_tok": gm["glyph_px"] * scale / PATCH if gm.get("glyph_px") else None,
                             "page_tokens": tokens_of(w, h), "n_images": len(it["images"]), "out_pos": pos - 1})
    write_jsonl(out / "rows.jsonl", recs)
    return out / "rows.jsonl"


def _pct(a, b) -> str:
    return "—" if not b else f"{100 * a / b:.1f}"


def summarize(rows: list[dict]) -> dict:
    """{실험: {조건: {items, rows, 결과별 수, dropped, glyph_tok, worse, better, paired}}}"""
    res: dict = {}
    by = defaultdict(lambda: defaultdict(list))
    for r in rows:
        by[r["kind"]][r["cond"]].append(r)
    for kind, conds in by.items():
        ref = {(r["doc"], r["list"], r["key"]): r["dropped"] for r in conds.get(REF[kind], [])}
        res[kind] = {}
        order = list(RES_BUDGETS) if kind == "resolution" else sorted(conds, key=lambda c: (c != REF[kind], int(c) if c.isdigit() else c))
        for cond in order:
            rs = conds.get(cond, [])
            if not rs:
                continue
            c = Counter(r["outcome"] for r in rs)
            g = [r["glyph_tok"] for r in rs if r.get("glyph_tok")]
            worse = better = paired = 0
            for r in rs:
                key = (r["doc"], r["list"], r["key"])
                if key in ref and cond != REF[kind]:
                    paired += 1
                    worse += r["dropped"] and not ref[key]
                    better += ref[key] and not r["dropped"]
            res[kind][cond] = {"items": len({r["id"] for r in rs}), "rows": len(rs), **{o: c.get(o, 0) for o in OUTCOMES},
                               "dropped": sum(r["dropped"] for r in rs), "truncated": sum(r["truncated"] for r in rs),
                               "glyph_tok": sum(g) / len(g) if g else None,
                               "page_tokens": sum(r["page_tokens"] for r in rs) / len(rs),
                               "paired": paired, "worse": worse, "better": better}
    return res


def report_md(res: dict) -> str:
    L = ["# 2단계 통제 실험: 한 가지만 바꿨을 때 누락률", "",
         "대상 쪽의 정답 행 기준 (%). 누락 = 건너뜀 + 길이에 잘림 + 스스로 끝냄. "
         "짝지은 비교는 같은 행이 기준 조건 대비 이 조건에서 새로 빠진 수(+) / 새로 나온 수(−).", ""]
    for kind in KINDS:
        if kind not in res:
            continue
        L += [f"## {TITLE[kind]} (기준: {REF[kind]})", "",
              "| 조건 | 문항 | 행 | 글자 높이(토큰) | 쪽 토큰 | " + " | ".join(NAME[o] for o in OUTCOMES[:7]) + " | **누락** | 짝지은 비교 |",
              "|---|---:|---:|---:|---:|" + "---:|" * 8 + "---|"]
        for cond, s in res[kind].items():
            pair = "기준" if cond == REF[kind] else (f"+{s['worse']} / −{s['better']} (짝 {s['paired']})" if s["paired"] else "—")
            gt = f"{s['glyph_tok']:.2f}" if s["glyph_tok"] else "—"
            L.append(f"| {cond} | {s['items']} | {s['rows']:,} | {gt} | {s['page_tokens']:,.0f} | "
                     + " | ".join(_pct(s[o], s["rows"]) for o in OUTCOMES[:7]) + f" | **{_pct(s['dropped'], s['rows'])}** | {pair} |")
        L.append("")
    if not res:
        L.append("문항이 없습니다 (header 실험은 gen --twins 데이터가 필요).")
    return "\n".join(L) + "\n"


def report(out) -> str:
    out = Path(out)
    res = summarize(read_jsonl(out / "rows.jsonl"))
    md = report_md(res)
    (out / "probes.md").write_text(md, encoding="utf-8")
    (out / "probes.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return md


def viewer(data_dir, out) -> Path:
    """<out>/viewer.html: 실험마다 기준 쪽 이미지와, 조건별로 그 쪽 행의 결과를 기호 줄로 (행 순서대로)."""
    import html
    import os

    from .rows import SYMBOL
    from .viewer import CSS

    data_dir, out = Path(data_dir), Path(out)
    items = {it["id"]: it for it in read_jsonl(out / "items.jsonl")}
    rows = read_jsonl(out / "rows.jsonl")
    root = os.path.relpath(data_dir, out)
    cache: dict = {}
    by = defaultdict(lambda: defaultdict(list))
    for r in rows:
        by[(r["kind"], r["doc"], r["page"])][r["cond"]].append(r)
    parts = [f"<h1>통제 실험 viewer</h1><p class='legend'>" + " · ".join(f"{SYMBOL[o]} {NAME[o]}" for o in SYMBOL)
             + ". 기호는 그 쪽 정답 행 순서. 이미지를 누르면 원본.</p>"]
    for kind in KINDS:
        bases = [k for k in by if k[0] == kind]
        if not bases:
            continue
        parts.append(f"<h2>{html.escape(TITLE[kind])}</h2><table><tr><th>쪽</th><th>조건</th><th>누락 / 행</th><th>행별 결과</th></tr>")
        for base in sorted(bases):
            conds = by[base]
            ref = conds.get(REF[kind]) or next(iter(conds.values()))
            it = items[ref[0]["id"]]
            img = _label(data_dir, it["label"], cache)["images"][it["page"]]
            first = True
            for cond in (list(RES_BUDGETS) if kind == "resolution" else sorted(conds, key=lambda c: (c != REF[kind], c))):
                rs = sorted(conds.get(cond, []), key=lambda r: (r["list"], r["key"]))
                if not rs:
                    continue
                cell = (f"<td rowspan='{len(conds)}'><a href='{html.escape(root)}/{html.escape(img)}' target='_blank'>"
                        f"{html.escape(base[1])} {base[2] + 1}쪽</a></td>") if first else ""
                first = False
                syms = "".join(SYMBOL[r["outcome"]] for r in rs)
                drop = sum(r["dropped"] for r in rs)
                parts.append(f"<tr>{cell}<td>{html.escape(cond)}</td><td class='{'drop' if drop else 'ok'}'>{drop} / {len(rs)}</td>"
                             f"<td style='font-family:monospace'>{syms}</td></tr>")
        parts.append("</table>")
    path = out / "viewer.html"
    path.write_text(f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>통제 실험</title><style>{CSS}</style>"
                    f"</head><body>{''.join(parts)}</body></html>", encoding="utf-8")
    return path


def run_all(data_dir, out, client=None, kinds=KINDS, max_items: int = 40, workers: int = 8, simulate: float = 0.0) -> str:
    build(data_dir, out, kinds, max_items)
    run_probes(data_dir, out, client, workers, simulate)
    score_probes(data_dir, out)
    viewer(data_dir, out)
    return report(out)
