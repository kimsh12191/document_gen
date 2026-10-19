"""6단계 — viewer: 묶음마다 쪽 이미지, 정답, 방법별 답을 나란히 보는 정적 HTML.

  python -m mpx viewer --data data/test --pred preds/*.jsonl            # → data/test/viewer/index.html
  python -m mpx viewer --data data/test --pred preds/*.jsonl --serve 7862   # 브라우저 http://localhost:7862/viewer/

화면
  index.html          묶음 목록: 시나리오, 쪽 수, 대상 서류, 방법별 쪽 배정·행 F1
  b_<묶음ID>.html     ① 쪽 목록: 이미지, 정답(서류·쪽), 방법별로 이 쪽을 어느 문서로 묶었는지(맞으면 초록)
                      ② 대상 서류마다 항목 표(정답 / 방법별 답)와 목록 행 표. 행마다 방법별 결과 분류(rows.py):
                         ✓ 정확 · △ 일부 틀림(틀린 칸 표시) · ≠ 잘못 읽음 · ↷ 다른 곳에 · ✗ 건너뜀 · ✂ 길이에 잘림 ·
                         ■ 스스로 끝냄 · ∅ 문서 못 찾음.  ┆ 쪽 경계 행, ↪ 이어지는 쪽의 행.
서버 없이 파일로도 열린다(이미지는 데이터 폴더의 상대 경로).
"""
from __future__ import annotations

import html
import os
from pathlib import Path

from .common import read_jsonl
from .gen import load
from .pages import flatten
from .report import fmt, score_run
from .rows import DROPPED, NAME, SYMBOL, classify_bundle
from .score import _filled, _match, gt_docs, match_docs, row_sim, summarize

CSS = """
body{font-family:-apple-system,'Malgun Gothic','Noto Sans KR',sans-serif;margin:16px;color:#1d1d1f;background:#fff}
h1{font-size:20px}h2{font-size:17px;margin-top:28px;border-bottom:2px solid #ddd;padding-bottom:4px}h3{font-size:15px;margin:18px 0 6px}
table{border-collapse:collapse;font-size:12px;margin:6px 0}td,th{border:1px solid #ddd;padding:3px 6px;vertical-align:top}
th{background:#f4f4f6;position:sticky;top:0}.ok{background:#e6f4ea}.bad{background:#fde2e1}.part{background:#fff3cd}
.drop{background:#f8b4b0}.muted{color:#888}.pages{display:flex;flex-wrap:wrap;gap:10px}.card{border:1px solid #ddd;border-radius:6px;padding:6px;width:190px;font-size:12px}
.card img{width:100%;border:1px solid #eee}.tag{display:inline-block;padding:0 5px;border-radius:4px;background:#eef;margin:1px}
details pre{white-space:pre-wrap;font-size:11px;max-height:240px;overflow:auto;background:#f8f8f8;padding:4px}
a{color:#0b57d0;text-decoration:none}.legend{font-size:12px;color:#555}
"""


def _e(v) -> str:
    return html.escape("" if v is None else str(v))


def _page(title: str, body: str) -> str:
    return f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{_e(title)}</title><style>{CSS}</style></head><body>{body}</body></html>"


def build(data_dir, pred_paths, out=None, names=None) -> Path:
    """names 를 주면 방법 이름으로 쓴다 (기본: 파일 이름). 모델 여러 개를 함께 볼 때."""
    data_dir = Path(data_dir)
    out = Path(out) if out else data_dir / "viewer"
    out.mkdir(parents=True, exist_ok=True)
    bundles, labels = load(data_dir)
    img_root = os.path.relpath(data_dir, out)
    methods, scores = {}, {}
    for i, p in enumerate(pred_paths):
        name = names[i] if names else Path(p).stem
        methods[name] = {r["bundle"]: r for r in read_jsonl(p)}
        scores[name] = {r["bundle"]: r for r in score_run(data_dir, p)[1]}
    names = list(methods)

    rows = []
    for b in bundles:
        targets = [labels[s]["doc_name"] for s in b["docs"] if labels[s].get("target")]
        cells = []
        for m in names:
            r = scores[m].get(b["id"])
            if not r:
                cells.append("<td class='muted'>—</td>")
                continue
            s = summarize([{**r, "docs": [d for d in r["docs"] if d["target"]]}])["all"]
            page_acc = r["page_ok"] / r["n_pages"] if r["n_pages"] else None
            gts = gt_docs(b, labels)
            es = [e for (gi, _), v in classify_bundle(b, labels, methods[m][b["id"]]).items() if gts[gi]["target"] for e in v]
            drop = sum(e["outcome"] in DROPPED for e in es) / len(es) if es else None
            cells.append(f"<td>{fmt(page_acc)} / {fmt(s['row_f1'])} / {fmt(drop)}</td>")
        rows.append(f"<tr><td><a href='b_{_e(b['id'])}.html'>{_e(b['id'])}</a></td><td>{_e(b.get('task_name') or '')}</td>"
                    f"<td>{len(b['pages'])}</td><td>{_e(', '.join(targets))}</td>{''.join(cells)}</tr>")
    head = "".join(f"<th>{_e(m)}<br><span class='muted'>쪽 배정 / 행 F1 / 누락</span></th>" for m in names)
    index = (f"<h1>여러 쪽 문서 추출 viewer</h1><p class='legend'>데이터: {_e(data_dir)} · 묶음 {len(bundles)}개 · "
             f"방법 {len(names)}개. 행 F1·누락(%)은 대상 서류 기준.</p>"
             f"<table><tr><th>묶음</th><th>업무</th><th>쪽</th><th>대상 서류</th>{head}</tr>{''.join(rows)}</table>")
    (out / "index.html").write_text(_page("viewer", index), encoding="utf-8")
    for b in bundles:
        (out / f"b_{b['id']}.html").write_text(_bundle_page(b, labels, methods, names, img_root), encoding="utf-8")
    return out / "index.html"


def _bundle_page(b: dict, labels: dict, methods: dict, names: list[str], img_root: str) -> str:
    gts = gt_docs(b, labels)
    preds = {m: (methods[m].get(b["id"]) or {}) for m in names}
    matches = {m: match_docs(gts, preds[m].get("docs") or []) for m in names}
    classes = {m: classify_bundle(b, labels, preds[m]) if preds[m] else {} for m in names}
    page_gt = {}
    for gi, g in enumerate(gts):
        for k, pg in enumerate(g["pages"]):
            page_gt[pg] = (gi, k + 1, len(g["pages"]))
    parts = [f"<p><a href='index.html'>← 목록</a></p><h1>{_e(b['id'])} <span class='muted'>{_e(b.get('task_name') or '')}</span></h1>",
             "<p class='legend'>" + " · ".join(f"{SYMBOL[o]} {NAME[o]}" for o in SYMBOL)
             + ". 진한 빨강 = 누락(건너뜀·잘림·끝냄·문서 못 찾음). ┆ 쪽 경계 행, ↪ 앞 쪽에서 이어지는 행.</p>",
             "<h2>① 쪽 목록</h2><div class='pages'>"]
    for i, p in enumerate(b["pages"], 1):
        gi, k, n = page_gt[i]
        g = gts[gi]
        lines = [f"<a href='{_e(img_root)}/{_e(p['image'])}' target='_blank'><img loading='lazy' src='{_e(img_root)}/{_e(p['image'])}'></a>",
                 f"<b>{i}쪽</b> · 정답: {_e(g['name'])} {k}/{n}"]
        for m in names:
            docs = preds[m].get("docs") or []
            pi = next((j for j, d in enumerate(docs) if i in (d.get("pages") or [])), None)
            ok = pi is not None and matches[m].get(gi) == pi
            label = "—" if pi is None else f"{docs[pi].get('type') or docs[pi].get('name')} #{pi + 1}"
            lines.append(f"<div class='{'ok' if ok else 'bad'}'>{_e(m)}: {_e(label)}</div>")
        parts.append(f"<div class='card'>{'<br>'.join(lines)}</div>")
    parts.append("</div><h2>② 대상 서류</h2>")
    for gi, g in enumerate(gts):
        if not g["target"]:
            continue
        lb = labels[g["id"]]
        tags = [f"{g['n_pages']}쪽"] + (["목록 김"] if lb.get("heavy") else []) + (["머리글 반복 없음"] if lb.get("no_repeat_header") else []) \
            + ([f"증강 {lb['augment']}"] if lb.get("augment") else [])
        parts.append(f"<h3>{_e(g['name'])} <span class='muted'>({_e(g['id'])}, 묶음 {', '.join(map(str, g['pages']))}쪽)</span> "
                     + "".join(f"<span class='tag'>{_e(t)}</span>" for t in tags) + "</h3>")
        pdocs = {m: (preds[m].get("docs") or [])[matches[m][gi]] if gi in matches[m] else None for m in names}
        parts.append(_fields_table(g, pdocs, names))
        for path, grows in g["lists"].items():
            cls = {m: classes[m].get((gi, path)) for m in names}
            parts.append(_rows_table(path, grows, g["row_page"][path], pdocs, cls, names))
    return _page(b["id"], "".join(parts))


def _fields_table(g: dict, pdocs: dict, names: list[str]) -> str:
    flats = {m: flatten((d or {}).get("fields") or {}) for m, d in pdocs.items()}
    rows = []
    for key, gv in g["fields"].items():
        if not _filled(gv[0]):
            continue
        cells = []
        for m in names:
            v = flats[m].get(key)
            cls = "ok" if _filled(v) and _match(v, gv) else "bad"
            cells.append(f"<td class='{cls}'>{_e(v) if _filled(v) else '<span class=muted>없음</span>'}</td>")
        rows.append(f"<tr><td>{_e(key)}</td><td>{_e(gv[0])}</td>{''.join(cells)}</tr>")
    head = "".join(f"<th>{_e(m)}</th>" for m in names)
    return f"<table><tr><th>항목</th><th>정답</th>{head}</tr>{''.join(rows)}</table>" if rows else ""


def _rows_table(path: str, grows: list[dict], pages: list[int], pdocs: dict, cls: dict, names: list[str]) -> str:
    keys = list(dict.fromkeys(k for r in grows for k, v in r.items() if _filled(v[0])))
    boundary = {i for i in range(1, len(pages)) if pages[i] != pages[i - 1]}
    boundary |= {i - 1 for i in boundary}
    first = pages[0] if pages else 0
    prows = {m: [flatten(r) for r in ((pdocs[m] or {}).get("lists") or {}).get(path, []) if isinstance(r, dict)] for m in names}
    head = "".join(f"<th>{_e(k)}</th>" for k in keys) + "".join(f"<th>{_e(m)}</th>" for m in names)
    body, counts = [], {m: {} for m in names}
    for i, r in enumerate(grows):
        mark = ("┆" if i in boundary else "") + ("↪" if pages[i] > first else "")
        cells = "".join(f"<td>{_e(r[k][0]) if k in r else ''}</td>" for k in keys)
        for m in names:
            e = (cls[m] or [None] * len(grows))[i]
            oc = e["outcome"] if e else "doc_missing"
            counts[m][oc] = counts[m].get(oc, 0) + 1
            note = ""
            if oc == "partial" and e["j"] is not None and e["j"] < len(prows[m]):
                pr = prows[m][e["j"]]
                note = ", ".join(f"{k}: {pr.get(k)!s}" for k in keys if k in r and _filled(r[k][0])
                                 and not _match(pr.get(k), r[k]))
            elif oc == "misplaced":
                note = f"→ {e.get('where')}"
            elif oc == "misread":
                note = f"유사도 {e['sim']:.2f}"
            css = {"exact": "ok", "partial": "part", "misread": "bad", "misplaced": "part"}.get(oc, "drop")
            cells += f"<td class='{css}' title='{_e(NAME[oc])}'>{SYMBOL[oc]} {_e(note)}</td>"
        body.append(f"<tr><td>{i + 1}{mark}</td><td>{pages[i] + 1}</td>{cells}</tr>")
    summary = " · ".join(f"{_e(m)}: 정확 {counts[m].get('exact', 0)}/{len(grows)}, 누락 {sum(counts[m].get(o, 0) for o in DROPPED)}"
                         for m in names)
    return (f"<p><b>목록 {_e(path)}</b> <span class='muted'>({len(grows)}행 · {summary})</span></p>"
            f"<table><tr><th>#</th><th>쪽</th>{head}</tr>{''.join(body)}</table>")


__all__ = ["build", "row_sim"]
