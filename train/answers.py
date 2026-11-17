"""문항별 모델 답 (answers.html): 두 모델(A·B)을 골라 문항마다 질문·그림·정답과 두 답·점수를 나란히. report.py 가 만든다.

- 위에서 평가 세트·과제와 모델 A·B 를 고른다. 전체 문항 기준으로 B 가 A 보다 좋아진·나빠진·같은 문항 수를 보여 준다.
- 보기: 전체 · 점수가 다른 문항 · B 가 나빠진 문항 · B 가 좋아진 문항. 문항 ID 로 찾기. '모든 모델 답 보기'를 켜면 다른 모델 답도.
- 카드는 평가 세트·과제마다 per_task 개 (모델끼리 점수가 갈린 문항을 절반까지 먼저, 나머지는 무작위, seed 고정). --all 이면 모두.
- 점수는 그 과제의 주 지표를 문항 하나로 잰 값 (보고서와 같은 채점, 저장된 답으로 — 추론 없음).
- 그림은 평가 세트 캐시의 그림을 상대 경로로 건다 (결과 폴더나 캐시를 옮기면 그림이 안 보일 수 있다).
"""
import html
import json
import os
import random
from pathlib import Path

from docgen.bench import evaluate as E
from docgen.bench.metrics import parse_json
from docgen.bench.ocr_data import read_jsonl

LIMIT = 4000   # 질문·답 글자 수 (넘으면 자른다)


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


def build(models, out, title="", base_label=None, per_task=30, take_all=False, seed=0):
    """models: report.collect 의 모델들 (m["sets"], m["scores"][세트]["per_item"]). 기준 문항(기준 모델의 것)과 같은 모델만 견준다."""
    from .mix import task_rows
    from .predict import index_predictions

    out = Path(out).resolve()
    models = [m for m in models if m["scores"]]
    labels = [m["label"] for m in models]
    base = base_label if base_label in labels else labels[0]
    groups, cards, scores = [], [], []
    set_ids = list(dict.fromkeys(sid for m in models for sid in m["scores"]))
    rng = random.Random(seed)
    for sid in set_ids:
        owner = next((m for m in models if m["label"] == base and sid in m["scores"]), None) or next(m for m in models if sid in m["scores"])
        ref = owner["scores"][sid]["items_sha256"]
        same = [m for m in models if (m["scores"].get(sid) or {}).get("items_sha256") == ref]
        entry = owner["sets"][sid]
        rows, items = task_rows(entry["dir"], {r["id"] for r in read_jsonl(entry["tasks"])})
        rows = {r["id"]: r for r in rows}
        preds = {m["label"]: index_predictions(m["sets"][sid]["answers"]) for m in same}
        by_task = {}
        for it in items:
            by_task.setdefault(it["task"], []).append(it)
        for task, its in by_task.items():
            metric = owner["scores"][sid]["tasks"][task]["main"]
            per = {m["label"]: m["scores"][sid]["per_item"].get(task, {}) for m in same}
            its = sorted(its, key=lambda it: it["id"])
            g = len(groups)
            # 전체 문항의 모델별 점수 (A·B 를 골랐을 때 좋아진·나빠진 수를 세려고): [[모델마다 점수], ...]
            scores.append([[per.get(l, {}).get(it["id"]) if l in per else None for l in labels] for it in its])
            if take_all:
                chosen = its
            else:
                split, flat = [], []
                for it in its:
                    vals = [v for v in (per[l].get(it["id"]) for l in per) if v is not None]
                    (split if vals and max(vals) - min(vals) > 1e-9 else flat).append(it)
                rng.shuffle(split)
                rng.shuffle(flat)
                half = (per_task + 1) // 2
                chosen = split[:half] + (flat + split[half:])[:per_task - min(half, len(split))]
            groups.append({"set": sid, "task": task, "metric": metric, "lower": metric in E.LOWER_IS_BETTER,
                           "n": len(its), "shown": len(chosen)})
            for it in sorted(chosen, key=lambda it: it["id"]):
                row = rows[it["id"]]
                prompt = "".join(m["content"] for m in row["messages"] if m.get("role") == "user").replace("<image>", "")
                meta = it.get("meta") or {}
                answers, unread = [], []
                json_answer = isinstance(it.get("answer"), (list, dict)) or isinstance(parse_json(it.get("answer")), (list, dict))   # 정답이 JSON 인 문항: 답을 JSON 으로 못 읽으면 0점
                for label in labels:
                    if label not in preds:
                        answers.append(None)
                        unread.append(False)
                        continue
                    raw = preds[label].get(it["id"])
                    text = E.answer_text(raw) if raw is not None else None
                    answers.append(_cut("(답 없음)" if text is None else text))
                    unread.append(bool(json_answer and text is not None and not isinstance(parse_json(text), (list, dict))))
                cards.append({"g": g, "id": it["id"], "prompt": _cut(prompt), "ref": _cut(_reference(it)),
                              "info": " · ".join(str(meta[k]) for k in ("doc_type", "label_format") if meta.get(k)),
                              "images": [Path(os.path.relpath(p, out.parent)).as_posix() for p in row["images"]],
                              "scores": [per.get(l, {}).get(it["id"]) if l in per else None for l in labels], "answers": answers,
                              "unread": unread})
    payload = {"title": title, "base": base, "models": labels, "groups": groups, "cards": cards, "scores": scores,
               "per_task": None if take_all else per_task}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(PAGE.replace("__TITLE__", html.escape(title or "문항별 모델 답"))
                   .replace("__DATA__", json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")), encoding="utf-8")
    return out


PAGE = """<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>__TITLE__ · 문항별 답</title><style>
:root{--fg:#1f2328;--muted:#656d76;--line:#d0d7de;--bg:#fff;--head:#f6f8fa;--up:#1a7f37;--down:#cf222e;--card:#fff}
@media (prefers-color-scheme:dark){:root{--fg:#e6edf3;--muted:#8d96a0;--line:#30363d;--bg:#0d1117;--head:#161b22;--up:#3fb950;--down:#f85149;--card:#0d1117}}
body{font:14px/1.5 -apple-system,"Segoe UI","Malgun Gothic",sans-serif;color:var(--fg);background:var(--bg);margin:24px 16px}
h1{font-size:22px;margin:0 0 4px}p,.muted{color:var(--muted)}
.bar{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;margin:12px 0;position:sticky;top:0;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--line);z-index:1}
select,input{font:inherit;color:inherit;background:var(--bg);border:1px solid var(--line);border-radius:6px;padding:4px 6px;max-width:100%}
.sum b{font-variant-numeric:tabular-nums}.card{border:1px solid var(--line);border-radius:8px;padding:12px;margin:12px 0;background:var(--card)}
.card h3{font-size:14px;margin:0 0 6px;word-break:break-all}
pre{white-space:pre-wrap;word-break:break-word;margin:0;font:12px/1.45 ui-monospace,Consolas,monospace}
details>summary{cursor:pointer;color:var(--muted)}
.imgs{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0}.imgs img{height:120px;border:1px solid var(--line)}
.wrap{overflow-x:auto}table{border-collapse:collapse;width:100%}
th,td{border:1px solid var(--line);padding:4px 8px;text-align:left;vertical-align:top}th{background:var(--head);white-space:nowrap}
td.s{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums;width:5em}
.unread{color:var(--down);font-size:11px;white-space:normal}.up{color:var(--up);font-weight:600}.down{color:var(--down);font-weight:600}tr.ref td,tr.ref th{background:var(--head)}tr.other{opacity:.75}
</style></head><body>
<h1 id='t'></h1><p id='d'></p>
<div class='bar'><label>평가 세트 · 과제 <select id='g'></select></label>
<label>A <select id='a'></select></label><label>B <select id='b'></select></label>
<label>보기 <select id='f'><option value='all'>전체</option><option value='diff'>점수가 다른 문항</option>
<option value='worse'>B 가 나빠진 문항</option><option value='better'>B 가 좋아진 문항</option></select></label>
<label><input type='checkbox' id='every'> 모든 모델 답 보기</label>
<label>문항 ID <input id='q' placeholder='찾기'></label></div>
<p class='sum' id='sum'></p>
<div id='list'></div>
<script type='application/json' id='data'>__DATA__</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
$('t').textContent = (D.title ? D.title + ' · ' : '') + '문항별 모델 답';
$('d').innerHTML = '모델 A 와 B 를 골라 문항마다 견줍니다. 카드는 평가 세트·과제마다 ' + (D.per_task ? '표본 ' + D.per_task + '개 (모델끼리 점수가 갈린 문항을 절반까지 먼저)' : '모든 문항')
  + ', 아래 숫자(좋아진·나빠진 문항 수)는 전체 문항 기준. 점수는 그 과제의 주 지표를 문항 하나로 잰 값 (%, ↓ 는 낮을수록 좋음).';
D.groups.forEach((g, i) => $('g').add(new Option((g.set ? g.set + ' · ' : '') + g.task + ' — ' + g.metric + (g.lower ? ' ↓' : '') + ' (전체 ' + g.n + ', 카드 ' + g.shown + ')', i)));
D.models.forEach((m, i) => { $('a').add(new Option(m, i)); $('b').add(new Option(m, i)); });
$('a').value = Math.max(0, D.models.indexOf(D.base));
$('b').value = D.models.length > 1 ? (+$('a').value === D.models.length - 1 ? 0 : D.models.length - 1) : 0;
function cmp(b, a, lower) { return a == null || b == null || Math.abs(b - a) < 1e-9 ? 0 : ((b > a) !== lower ? 1 : -1); }
const pct = v => v == null ? '—' : (v * 100).toFixed(1);
function show() {
  const g = +$('g').value, G = D.groups[g], A = +$('a').value, B = +$('b').value, f = $('f').value, q = $('q').value.trim().toLowerCase();
  let up = 0, down = 0, same = 0, none = 0;
  (D.scores[g] || []).forEach(s => { if (s[A] == null || s[B] == null) none++; else { const c = cmp(s[B], s[A], G.lower); c > 0 ? up++ : c < 0 ? down++ : same++; } });
  $('sum').innerHTML = '<b>' + esc(D.models[B]) + '</b> 가 <b>' + esc(D.models[A]) + '</b> 보다 — 좋아진 문항 <b class="up">' + up + '</b> · 나빠진 문항 <b class="down">' + down
    + '</b> · 같음 ' + same + (none ? ' · 답·점수 없음 ' + none : '') + ' (전체 ' + G.n + ')';
  const cards = D.cards.filter(c => {
    if (q) return c.id.toLowerCase().includes(q);
    if (c.g !== g) return false;
    const r = cmp(c.scores[B], c.scores[A], D.groups[c.g].lower);
    return f === 'all' || (f === 'diff' && r !== 0) || (f === 'worse' && r < 0) || (f === 'better' && r > 0);
  });
  $('list').innerHTML = (cards.length ? '' : '<p>해당 문항이 카드 표본에 없습니다.</p>') + cards.map(c => {
    const H = D.groups[c.g];
    const order = $('every').checked ? [A, B, ...D.models.map((_, i) => i).filter(i => i !== A && i !== B)] : [A, B];
    const rows = order.filter((i, k) => order.indexOf(i) === k).map(i => {
      const r = i === A ? 0 : cmp(c.scores[i], c.scores[A], H.lower);
      const tag = i === A ? ' (A)' : i === B ? ' (B)' : '';
      return '<tr class="' + (i !== A && i !== B ? 'other' : '') + '"><th>' + esc(D.models[i]) + tag + '</th><td class="s ' + (r > 0 ? 'up' : r < 0 ? 'down' : '') + '">'
        + pct(c.scores[i]) + ((c.unread || [])[i] ? '<div class="unread">답을 JSON 으로 못 읽음</div>' : '') + '</td><td><pre>' + esc(c.answers[i] == null ? '(이 모델은 다른 평가 문항)' : c.answers[i]) + '</pre></td></tr>';
    }).join('');
    return '<div class="card"><h3>' + esc(c.id) + (q ? ' <span class="muted">' + esc(H.set + ' · ' + H.task) + '</span>' : '') + '</h3>'
      + (c.info ? '<div class="muted">' + esc(c.info) + '</div>' : '')
      + '<details><summary>질문 · 그림 ' + c.images.length + '장</summary><div class="imgs">'
      + c.images.map(p => '<a href="' + esc(p) + '" target="_blank"><img loading="lazy" src="' + esc(p) + '" alt=""></a>').join('')
      + '</div><pre>' + esc(c.prompt) + '</pre></details>'
      + '<div class="wrap"><table><tr><th>모델</th><th>' + esc(H.metric) + (H.lower ? ' ↓' : '') + '</th><th>답</th></tr>'
      + '<tr class="ref"><th>정답</th><td></td><td><pre>' + esc(c.ref) + '</pre></td></tr>' + rows + '</table></div></div>';
  }).join('');
}
['g', 'a', 'b', 'f', 'every'].forEach(id => $(id).addEventListener('change', show));
$('q').addEventListener('input', show);
show();
</script></body></html>
"""
