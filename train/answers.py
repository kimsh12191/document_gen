"""문항별 모델 답: 평가 세트·과제마다 문항을 골라 질문·그림·정답과 모델마다의 답·점수를 나란히 (python -m train answers).

  python -m train answers <묶음.json | 결과 폴더 | workdir> [--per-task 30] [--all] [--out <html>]

- 따로 치지 않아도 실험 묶음은 <root>/answers.html, 학습 실행은 <workdir>/reports/answers.html 을 만든다 (기본 표본).
- 표본: 평가 세트·과제마다 --per-task 개 (기본 30). 모델끼리 점수가 갈린 문항을 절반까지 먼저, 나머지는 무작위 (seed 고정).
  --all 이면 모든 문항 (파일이 커진다).
- 점수는 그 과제의 주 지표를 문항 하나로 잰 값 (보고서와 같은 채점 함수, 저장된 답으로 다시 채점 — 추론 없음).
- 페이지에서 평가 세트·과제를 고르고, '갈린 문항만'·'기준보다 나빠진 모델이 있는 문항만'으로 거르고, 문항 ID 로 찾는다.
- 그림은 섞은 폴더의 그림을 상대 경로로 건다 (결과 폴더를 옮기면 그림이 안 보일 수 있다).
"""
import argparse
import html
import json
import os
import random
from pathlib import Path

from docgen.bench import evaluate as E
from docgen.bench.ocr_data import read_json, read_jsonl

LIMIT = 4000   # 질문·답 글자 수 (넘으면 자른다)
LOWER = {"cer", "false_alarm", "matched_label_cer", "extra_key"}


def _cut(text):
    text = "" if text is None else str(text)
    return text if len(text) <= LIMIT else text[:LIMIT] + f"\n… ({len(text) - LIMIT}자 더)"


def _reference(it):
    a = it["answer"]
    if isinstance(a, str):
        return a
    try:
        from docgen.bench.runner import oracle_output

        return oracle_output(it)
    except Exception:  # noqa: BLE001  보여 주기만 한다
        return json.dumps(a, ensure_ascii=False)


def _predictions(report, wd):
    from .predict import index_predictions

    path = Path(report.get("predictions") or "")
    if not path.is_file():
        path = Path(wd) / "predictions" / path.name   # 폴더를 옮겼으면 workdir 안에서
    return index_predictions(path) if path.is_file() else None


def build(reports, sources, out, title="", base_label=None, per_task=30, take_all=False, seed=0):
    """reports: 보고서(json) 목록 (label 이 열 이름), sources[label] = (workdir, 섞은 폴더)."""
    out = Path(out).resolve()
    models, notes = [], []
    for r in reports:
        if r["label"] not in sources:
            continue
        wd, data = sources[r["label"]]
        preds = _predictions(r, wd)
        if preds is None:
            notes.append(f"{r['label']}: 답 파일이 없어 뺍니다 ({r.get('predictions')})")
            continue
        models.append((r["label"], preds, Path(data)))
    if not models:
        raise ValueError("답 파일이 있는 모델이 없습니다")
    data = models[0][2]
    rows = {r["id"]: r for r in read_jsonl(data / "benchmark_tasks.jsonl")}
    asked = set().union(*(p.keys() for _, p, _ in models))
    items = [it for it in read_jsonl(data / "benchmark_items.jsonl") if it["id"] in rows and it["id"] in asked]
    groups = {}
    for it in items:
        groups.setdefault(((it.get("meta") or {}).get("benchmark_id") or "", it["task"]), []).append(it)
    names = {(it.get("meta") or {}).get("benchmark_id") or "": (it.get("meta") or {}).get("benchmark_name") or "" for it in items}
    base = base_label if base_label in [m[0] for m in models] else models[0][0]
    rng = random.Random(seed)
    out_groups, cards = [], []
    for (ident, task), its in groups.items():
        per, metric = {}, None
        for label, preds, _ in models:
            res = E.score_task(task, its, preds)
            metric = metric or res["main"]
            per[label] = {p["id"]: p.get(metric) for p in res["per_item"]}
        lower = metric in LOWER
        split = {"갈림": [], "같음": []}
        for it in its:
            vals = [per[m][it["id"]] for m, _, _ in models if per[m].get(it["id"]) is not None]
            split["갈림" if vals and max(vals) - min(vals) > 1e-9 else "같음"].append(it)
        if take_all:
            chosen = its
        else:
            for v in split.values():
                v.sort(key=lambda it: it["id"])
                rng.shuffle(v)
            half = (per_task + 1) // 2
            chosen = split["갈림"][:half]
            chosen += (split["같음"] + split["갈림"][half:])[:per_task - len(chosen)]
        g = len(out_groups)
        out_groups.append({"set": ident, "name": names.get(ident, ""), "task": task, "metric": metric, "lower": lower,
                           "n": len(its), "split": len(split["갈림"]), "shown": len(chosen)})
        for it in sorted(chosen, key=lambda it: it["id"]):
            row = rows[it["id"]]
            prompt = "".join(m["content"] for m in row["messages"] if m.get("role") == "user").replace("<image>", "")
            meta = it.get("meta") or {}
            answers = []
            for label, preds, _ in models:
                raw = preds.get(it["id"])
                text = E.answer_text(raw) if raw is not None else None
                answers.append([label, per[label].get(it["id"]), _cut("(답 없음)" if text is None else text)])
            cards.append({"g": g, "id": it["id"], "prompt": _cut(prompt), "ref": _cut(_reference(it)),
                          "info": " · ".join(str(meta[k]) for k in ("doc_type", "label_format") if meta.get(k)),
                          "images": [Path(os.path.relpath(p, out.parent)).as_posix() for p in row["images"]],
                          "answers": answers})
    payload = {"title": title, "base": base, "models": [m[0] for m in models], "groups": out_groups, "cards": cards,
               "notes": notes, "per_task": None if take_all else per_task}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(PAGE.replace("__TITLE__", html.escape(title or "문항별 모델 답"))
                   .replace("__DATA__", json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")), encoding="utf-8")
    return out


def write_own(reports, sources, out, title="", base_label=None):
    """실험 묶음·학습 실행이 보고서를 쓸 때 (실패해도 학습은 계속)."""
    try:
        return build(reports, sources, out, title, base_label)
    except Exception as exc:  # noqa: BLE001  보고서 하나 때문에 멈추지 않는다
        print(f"WARNING: 문항별 답 페이지를 만들지 못했습니다 ({out}): {type(exc).__name__}: {exc}", flush=True)
        return None


PAGE = """<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>__TITLE__ · 문항별 답</title><style>
:root{--fg:#1f2328;--muted:#656d76;--line:#d0d7de;--bg:#fff;--head:#f6f8fa;--up:#1a7f37;--down:#cf222e;--card:#fff}
@media (prefers-color-scheme:dark){:root{--fg:#e6edf3;--muted:#8d96a0;--line:#30363d;--bg:#0d1117;--head:#161b22;--up:#3fb950;--down:#f85149;--card:#0d1117}}
body{font:14px/1.5 -apple-system,"Segoe UI","Malgun Gothic",sans-serif;color:var(--fg);background:var(--bg);margin:24px 16px}
h1{font-size:22px;margin:0 0 4px}p,.muted{color:var(--muted)}
.bar{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;margin:12px 0;position:sticky;top:0;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--line)}
select,input{font:inherit;color:inherit;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:4px 6px;max-width:100%}
.card{border:1px solid var(--line);border-radius:8px;padding:12px;margin:12px 0;background:var(--card)}
.card h3{font-size:14px;margin:0 0 6px;word-break:break-all}
pre{white-space:pre-wrap;word-break:break-word;margin:0;font:12px/1.45 ui-monospace,Consolas,monospace}
details>summary{cursor:pointer;color:var(--muted)}
.imgs{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0}.imgs img{height:120px;border:1px solid var(--line)}
.wrap{overflow-x:auto}table{border-collapse:collapse;width:100%}
th,td{border:1px solid var(--line);padding:4px 8px;text-align:left;vertical-align:top}th{background:var(--head);white-space:nowrap}
td.s{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.up{color:var(--up);font-weight:600}.down{color:var(--down);font-weight:600}tr.ref td{background:var(--head)}
</style></head><body>
<h1 id='t'></h1><p id='d'></p>
<div class='bar'><label>평가 세트 · 과제 <select id='g'></select></label>
<label><input type='checkbox' id='split'> 모델끼리 점수가 갈린 문항만</label>
<label><input type='checkbox' id='worse'> 기준보다 나빠진 모델이 있는 문항만</label>
<label>문항 ID <input id='q' placeholder='찾기'></label><span id='c' class='muted'></span></div>
<div id='list'></div>
<script type='application/json' id='data'>__DATA__</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
$('t').textContent = (D.title ? D.title + ' · ' : '') + '문항별 모델 답';
$('d').innerHTML = '평가 세트·과제마다 ' + (D.per_task ? '표본 ' + D.per_task + '개 (모델끼리 점수가 갈린 문항을 절반까지 먼저, 나머지는 무작위)' : '모든 문항')
  + '. 점수는 그 과제의 주 지표를 문항 하나로 잰 값 (%, ↓ 는 낮을수록 좋음). 초록 = 기준 모델 <b>' + esc(D.base) + '</b>보다 좋음, 빨강 = 나쁨.'
  + D.notes.map(n => '<br>' + esc(n)).join('');
D.groups.forEach((g, i) => {
  const o = document.createElement('option');
  o.value = i;
  o.textContent = (g.set ? (g.name || g.set) + ' · ' : '') + g.task + ' — ' + g.metric + (g.lower ? ' ↓' : '')
    + ' (보기 ' + g.shown + ' / 전체 ' + g.n + ', 갈림 ' + g.split + ')';
  $('g').appendChild(o);
});
function better(v, b, lower) { return v == null || b == null || Math.abs(v - b) < 1e-9 ? 0 : ((v > b) !== lower ? 1 : -1); }
function show() {
  const g = +$('g').value, G = D.groups[g], q = $('q').value.trim().toLowerCase();
  const bi = D.models.indexOf(D.base);
  const cards = D.cards.filter(c => {
    if (q) return c.id.toLowerCase().includes(q);
    if (c.g !== g) return false;
    const vals = c.answers.map(a => a[1]).filter(v => v != null);
    if ($('split').checked && !(vals.length && Math.max(...vals) - Math.min(...vals) > 1e-9)) return false;
    if ($('worse').checked && !c.answers.some(a => better(a[1], c.answers[bi][1], G.lower) < 0)) return false;
    return true;
  });
  $('c').textContent = cards.length + '개';
  $('list').innerHTML = cards.map(c => {
    const H = D.groups[c.g];
    const rows = c.answers.map((a, i) => {
      const cmp = i === bi ? 0 : better(a[1], c.answers[bi][1], H.lower);
      return '<tr><th>' + esc(a[0]) + (i === bi ? ' (기준)' : '') + '</th><td class="s ' + (cmp > 0 ? 'up' : cmp < 0 ? 'down' : '') + '">'
        + (a[1] == null ? '—' : (a[1] * 100).toFixed(1)) + '</td><td><pre>' + esc(a[2]) + '</pre></td></tr>';
    }).join('');
    return '<div class="card"><h3>' + esc(c.id) + (q ? ' <span class="muted">' + esc(H.task) + '</span>' : '') + '</h3>'
      + (c.info ? '<div class="muted">' + esc(c.info) + '</div>' : '')
      + '<details><summary>질문 · 그림 ' + c.images.length + '장</summary><div class="imgs">'
      + c.images.map(p => '<a href="' + esc(p) + '" target="_blank"><img loading="lazy" src="' + esc(p) + '" alt=""></a>').join('')
      + '</div><pre>' + esc(c.prompt) + '</pre></details>'
      + '<div class="wrap"><table><tr><th>모델</th><th>' + esc(H.metric) + (H.lower ? ' ↓' : '') + '</th><th>답</th></tr>'
      + '<tr class="ref"><th>정답</th><td></td><td><pre>' + esc(c.ref) + '</pre></td></tr>' + rows + '</table></div></div>';
  }).join('');
}
['g', 'split', 'worse'].forEach(id => $(id).addEventListener('change', show));
$('q').addEventListener('input', show);
show();
</script></body></html>
"""


def main(argv=None):
    from . import summary

    p = argparse.ArgumentParser(prog="python -m train answers", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("target", help="묶음 파일 · 결과 폴더(<root>) · workdir")
    p.add_argument("--per-task", type=int, default=30, help="평가 세트·과제마다 보여 줄 문항 수 (기본 30)")
    p.add_argument("--all", action="store_true", help="모든 문항")
    p.add_argument("--data", help="workdir 의 섞은 폴더 (config.json 이 없을 때)")
    p.add_argument("--out", help="만들 html (기본 <root>/answers.html 또는 <workdir>/reports/answers.html)")
    p.add_argument("--smoke", action="store_true", help="리허설(--smoke) 결과로")
    a = p.parse_args(argv)
    sw = summary.load(a.target)
    if "_reports" in sw:   # workdir
        reports = sw["_reports"]
        data = a.data or (read_json(sw["_root"] / "config.json")["data"]["output_dir"] if (sw["_root"] / "config.json").is_file() else None)
        if not data:
            raise SystemExit("섞은 폴더를 알 수 없습니다: --data <섞은 폴더>")
        sources = {r["label"]: (sw["_root"], Path(data)) for r in reports}
        base, out = sw["runs"][0]["label"] if sw["runs"] else None, a.out or sw["_root"] / "reports" / "answers.html"
    else:
        from . import sweep as S

        reports, _ = S.collect(sw, a.smoke)
        sources, base, out = sw["_sources"], S.baseline(sw), a.out or sw["_root"] / "answers.html"
    path = build(reports, sources, out, sw["name"], base, a.per_task, a.all)
    print(f"문항별 답 → {path}")
