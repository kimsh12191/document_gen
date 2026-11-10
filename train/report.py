"""결과 보고서: 모델들의 평가 세트별 점수를 한 화면에 (report.html), 같은 숫자를 표 데이터로 (scores.csv), 문항별 답 (answers.html).

  python -m train report <결과 폴더> [--rescore] [--per-task 30 | --all]

- 결과 폴더: 학습 실행 workdir · 실험 묶음 root · 평가만 하기 root (results.json 이 있는 곳). 학습·평가가 끝날 때마다 저절로 만든다.
  이 명령은 저장된 답으로 다시 만들 때 (추론 없음, GPU 안 씀).
- --rescore: 채점 규칙(docgen.bench.evaluate·채점 함수)을 고쳤을 때. 점수 캐시(<답>.scores.json)를 버리고 다시 채점한다.
- results.json: {"name", "about", "record"?, "baseline"?, "notes"?, "models": [{"label", "about", "model", "checkpoint"?, "changes"?,
  "train"?, "sets": {세트 id: {"dir": 준비한 평가 세트, "tasks": 물은 질문 파일, "answers": 답 파일}}}]}
"""
import argparse
import csv
import html
from collections import Counter
from pathlib import Path

from docgen.bench import evaluate as E
from docgen.bench.ocr_data import read_json, read_jsonl, write_json
from docgen.bench.tracking import DIMENSIONS

LOWER = E.LOWER_IS_BETTER
DIMS = ("doc_type", "source_dataset", "label_format", "view")   # 구분별 표 (그룹이 둘 이상일 때만)
SCORE_VERSION = 1


def _pct(v):
    return "—" if v is None else f"{v * 100:.1f}"


# -- 채점 (캐시) ---------------------------------------------------------------------------------
def scored(entry, rescore=False):
    """세트 하나의 답 → 점수 (score.score + 문항별 주 지표). <답>.scores.json 에 둔다 (문항·답이 같으면 다시 쓰지 않음)."""
    from .mix import task_rows
    from .predict import index_predictions
    from .score import items_digest, score

    answers = Path(entry["answers"])
    rows, items = task_rows(entry["dir"], {r["id"] for r in read_jsonl(entry["tasks"])})
    if not answers.is_file():
        return None
    st = answers.stat()
    key = {"v": SCORE_VERSION, "items": items_digest(items), "answers": [st.st_size, st.st_mtime_ns]}
    cache = answers.with_name(answers.name + ".scores.json")
    if cache.is_file() and not rescore:
        old = read_json(cache)
        if old.get("key") == key:
            return old["score"]
    preds = index_predictions(answers)
    res = score(items, preds)
    per = {}
    for task, its in _by_task(items).items():
        main = res["tasks"][task]["main"]
        per[task] = {p["id"]: p.get(main) for p in E.score_task(task, its, preds)["per_item"]}
    res["per_item"] = per
    res["answered"] = sum(1 for it in items if it["id"] in preds)
    res["complete"] = Path(str(answers) + ".done").exists()
    write_json(cache, {"key": key, "score": res})
    return res


def _by_task(items):
    out = {}
    for it in items:
        out.setdefault(it["task"], []).append(it)
    return out


def collect(results, rescore=False):
    """→ (모델들, 세트 정보 {id: {"name", "group", "ref"(기준 문항 지문)}}, 알림). 모델마다 m["scores"][세트 id] = 점수."""
    models, notes, sets = [], list(results.get("notes") or []), {}
    for m in results["models"]:
        m = {**m, "scores": {}}
        for sid, entry in (m.get("sets") or {}).items():
            try:
                s = scored(entry, rescore)
            except (OSError, ValueError, KeyError) as exc:
                notes.append(f"{m['label']} · {sid}: 채점하지 못함 ({type(exc).__name__}: {exc})")
                continue
            if s is None:
                continue
            if not s["complete"]:
                notes.append(f"{m['label']} · {sid}: 답이 다 나오지 않았습니다 ({s['answered']}/{s['n']}, 없는 답은 0점)")
            m["scores"][sid] = s
            done = read_json(Path(entry["dir"]) / "DONE.json") if (Path(entry["dir"]) / "DONE.json").is_file() else {}
            info = sets.setdefault(sid, {"name": done.get("name", sid), "group": done.get("group", ""), "hashes": []})
            info["hashes"].append(s["items_sha256"])
        models.append(m)
    base = baseline_of(results, models)
    for sid, info in sets.items():
        own = (base or {}).get("scores", {}).get(sid)
        info["ref"] = own["items_sha256"] if own else Counter(info["hashes"]).most_common(1)[0][0]
        others = sorted({m["label"] for m in models if sid in m["scores"] and m["scores"][sid]["items_sha256"] != info["ref"]})
        if others:
            notes.append(f"{sid}: {', '.join(others)} 는 평가 문항이 기준 모델과 달라(평가 세트 원본·리허설이 다름) 흐리게 † 로 표시하고 비교하지 않습니다")
    return models, sets, notes


def baseline_of(results, models):
    want = results.get("baseline")
    return next((m for m in models if m["label"] == want), None) or (models[0] if models else None)


# -- report.html · scores.csv -----------------------------------------------------------------
CSS = """
:root{--fg:#1f2328;--muted:#656d76;--line:#d0d7de;--bg:#fff;--head:#f6f8fa;--up:#1a7f37;--down:#cf222e;--group:#eef2f6}
@media (prefers-color-scheme:dark){:root{--fg:#e6edf3;--muted:#8d96a0;--line:#30363d;--bg:#0d1117;--head:#161b22;--up:#3fb950;--down:#f85149;--group:#1c2430}}
body{font:14px/1.5 -apple-system,"Segoe UI","Malgun Gothic",sans-serif;color:var(--fg);background:var(--bg);margin:24px 16px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:28px 0 8px}h3{font-size:15px;margin:16px 0 4px}
p,li,.muted{color:var(--muted)}a{color:inherit}code{font:12px ui-monospace,Consolas,monospace;word-break:break-all}
.wrap{overflow-x:auto}table{border-collapse:collapse;font-variant-numeric:tabular-nums;margin:4px 0 12px}
th,td{border:1px solid var(--line);padding:4px 8px;text-align:right;white-space:nowrap}
th{background:var(--head)}td.l,th.l{text-align:left}td.w{white-space:normal;min-width:16em}
tr.g td{background:var(--group);font-weight:600;text-align:left}
.up{color:var(--up)}.down{color:var(--down)}.d{color:var(--muted)}.off{opacity:.45}b{font-weight:700}
details{margin:8px 0}summary{cursor:pointer;font-weight:600}
"""


def _cell(v, d, lower, same=True, best=False):
    if v is None:
        return "<td>—</td>"
    num = f"<b>{_pct(v)}</b>" if best and same else _pct(v)
    delta = "" if d is None else f" <span class='{'d' if abs(d) < 0.05 else ('up' if (d > 0) != lower else 'down')}'>({d:+.1f})</span>"
    return f"<td><span class='{'' if same else 'off'}'>{num}{'' if same else '†'}</span>{delta}</td>"


def write(results, out_dir, rescore=False, per_task=30, take_all=False):
    """results(results.json 꼴) → <out_dir>/report.html · scores.csv · answers.html. 만든 report.html 경로 (모델이 없으면 None)."""
    out_dir = Path(out_dir)
    models, sets, notes = collect(results, rescore)
    if not any(m["scores"] for m in models):
        return None
    base = baseline_of(results, models)
    e = html.escape
    labels = [m["label"] for m in models]
    head = "".join(f"<th>{e(l)}</th>" for l in labels)

    def val(m, sid, task, metric, dim=None, bucket=None):
        s = m["scores"].get(sid)
        if not s:
            return None, False
        t = (s.get("breakdowns", {}).get(dim, {}).get(bucket, {}).get("tasks", {}) if dim else s["tasks"]).get(task)
        v = (t or {}).get("metrics", {}).get(metric)
        return v, s["items_sha256"] == sets[sid]["ref"]

    def cells(sid, task, metric, dim=None, bucket=None, csv_rows=None, n=None):
        lower = metric in LOWER
        vals = [val(m, sid, task, metric, dim, bucket) for m in models]
        b = val(base, sid, task, metric, dim, bucket)[0] if base else None
        ok = [v for v, same in vals if v is not None and same]
        best = (min(ok) if lower else max(ok)) if len(ok) > 1 else None
        out = []
        for m, (v, same) in zip(models, vals):
            d = None if v is None or b is None or m is base or not same else (v - b) * 100
            out.append(_cell(v, d, lower, same, v == best))
            if csv_rows is not None and v is not None:
                csv_rows.append({"set_id": sid, "set_name": sets[sid]["name"], "set_group": sets[sid]["group"],
                                 "dimension": dim or "", "bucket": bucket or "", "task": task, "metric": metric, "model": m["label"],
                                 "n": n, "value": round(v, 6), "delta_pp": None if d is None else round(d, 3),
                                 "lower_is_better": lower, "same_items": same})
        return "".join(out)

    csv_rows = []
    parts = [f"<h1>{e(results.get('name') or '결과')}</h1><p>{e(results.get('about') or '')}</p>"]
    if results.get("record"):
        parts.append(f"<p>기록: {e(results['record'])}</p>")
    parts.append("<p>점수 %, 괄호는 기준 모델 <b>" + e(base["label"] if base else "") + "</b> 대비 %p (초록 = 좋아짐, 빨강 = 나빠짐, ↓ 는 낮을수록 좋음). "
                 "굵게 = 그 줄에서 가장 좋은 값. 흐린 † = 평가 문항이 기준 모델과 달라 비교하지 않는 칸. "
                 "문항별 답은 <a href='answers.html'>answers.html</a> (두 모델을 골라 견줌), 숫자는 <a href='scores.csv'>scores.csv</a>.</p>")
    # 모델
    parts.append("<h2>모델</h2><div class='wrap'><table><tr><th class='l'>모델</th><th class='l'>설명</th><th class='l'>바꾼 설정</th>"
                 "<th class='l'>학습 데이터</th><th class='l'>모델 경로</th></tr>")
    for m in models:
        path = f"<code>{e(str(m.get('model') or ''))}</code>" + (f"<br><small>SFT 체크포인트 <code>{e(m['checkpoint'])}</code></small>" if m.get("checkpoint") else "")
        train = "<br>".join(e(t) for t in m.get("train") or [])
        parts.append(f"<tr><td class='l'>{e(m['label'])}{' (기준)' if m is base else ''}</td><td class='l w'>{e(m.get('about') or '')}</td>"
                     f"<td class='l w'>{e(m.get('changes') or '')}</td><td class='l w'>{train}</td><td class='l w'>{path}</td></tr>")
    parts.append("</table></div>")
    # 한눈에 보기
    order = list(sets)
    parts.append(f"<h2>한눈에 보기</h2><p>평가 세트·과제마다 주 지표.</p><div class='wrap'><table><tr><th class='l'>과제</th><th class='l'>지표</th><th>문항 수</th>{head}</tr>")
    for sid in order:
        parts.append(f"<tr class='g'><td colspan='{3 + len(models)}'>{e(sets[sid]['name'])} · {e(sid)}"
                     + (f" <span class='muted'>({e(sets[sid]['group'])})</span>" if sets[sid]['group'] not in ("", "ungrouped") else "") + "</td></tr>")
        ref = next((m["scores"][sid] for m in ([base] if base else []) + models if sid in m["scores"]), None)
        for task, t in ref["tasks"].items():
            metric = t["main"]
            parts.append(f"<tr><td class='l'>{e(task)}</td><td class='l'>{e(metric)}{' ↓' if metric in LOWER else ''}</td><td>{t['n']}</td>"
                         + cells(sid, task, metric, n=t["n"]) + "</tr>")
    parts.append("</table></div>")
    # 평가 세트별 자세히
    parts.append("<h2>평가 세트별 자세히</h2><p>모든 지표, 답 형식 오류(못 읽은 답, 0점 처리), 구분별 점수.</p>")
    for sid in order:
        ref = next((m["scores"][sid] for m in ([base] if base else []) + models if sid in m["scores"]), None)
        block = [f"<details><summary>{e(sets[sid]['name'])} · {e(sid)} — 문항 {ref['n']}</summary>",
                 f"<div class='wrap'><table><tr><th class='l'>과제</th><th class='l'>지표</th><th>문항 수</th>{head}</tr>"]
        for task, t in ref["tasks"].items():
            for metric in [t["main"], *sorted(k for k in t["metrics"] if k != t["main"])]:
                block.append(f"<tr><td class='l'>{e(task)}</td><td class='l'>{e(metric)}{' ↓' if metric in LOWER else ''}</td><td>{t['n']}</td>"
                             + cells(sid, task, metric, csv_rows=csv_rows, n=t["n"]) + "</tr>")
            fails = [(m["scores"].get(sid) or {}).get("tasks", {}).get(task, {}).get("parse_fail") for m in models]
            block.append(f"<tr><td class='l'>{e(task)}</td><td class='l'>답 형식 오류 ↓</td><td></td>"
                         + "".join(f"<td>{_pct(v)}</td>" for v in fails) + "</tr>")
        block.append("</table></div>")
        for dim in DIMS:
            groups = ref.get("breakdowns", {}).get(dim, {})
            if len(groups) < 2:
                continue
            block.append(f"<h3>{e(DIMENSIONS.get(dim, dim))}별</h3><div class='wrap'><table><tr><th class='l'>{e(DIMENSIONS.get(dim, dim))}</th>"
                         f"<th class='l'>과제</th><th class='l'>지표</th><th>문항 수</th>{head}</tr>")
            for bucket, g in groups.items():
                for task, t in g["tasks"].items():
                    block.append(f"<tr><td class='l'>{e(bucket)}</td><td class='l'>{e(task)}</td><td class='l'>{e(t['main'])}</td><td>{t['n']}</td>"
                                 + cells(sid, task, t["main"], dim, bucket, csv_rows, t["n"]) + "</tr>")
            block.append("</table></div>")
        for task, t in ref["tasks"].items():   # 과제 안의 구분 (kie 값 종류 등)
            for key, groups in (t.get("slices") or {}).items():
                if len(groups) < 2:
                    continue
                block.append(f"<h3>{e(task)} · {e(key)}별</h3><div class='wrap'><table><tr><th class='l'>{e(key)}</th><th>수</th>{head}</tr>")
                for bucket, g in groups.items():
                    vs = []
                    for m in models:
                        c = (m["scores"].get(sid) or {}).get("tasks", {}).get(task, {}).get("slices", {}).get(key, {}).get(bucket)
                        vs.append(next((v for k, v in c.items() if k != "n"), None) if c else None)
                    block.append(f"<tr><td class='l'>{e(bucket)}</td><td>{g['n']}</td>" + "".join(f"<td>{_pct(v)}</td>" for v in vs) + "</tr>")
                block.append("</table></div>")
        parts.append("".join(block) + "</details>")
    if notes:
        parts.append("<h2>알림</h2><ul>" + "".join(f"<li>{e(n)}</li>" for n in notes) + "</ul>")
    parts.append("<p>합성 서류 평가는 학습 데이터와 같은 생성기라 실서류보다 높게 나옵니다. 읽는 법: guide/results.md</p>")
    out_dir.mkdir(parents=True, exist_ok=True)
    page = out_dir / "report.html"
    page.write_text("<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
                    f"<title>{e(results.get('name') or '결과')}</title><style>{CSS}</style></head><body>" + "".join(parts) + "</body></html>\n",
                    encoding="utf-8")
    if csv_rows:
        with (out_dir / "scores.csv").open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(csv_rows[0]))
            w.writeheader()
            w.writerows(csv_rows)
    try:
        from .answers import build

        build(models, out_dir / "answers.html", results.get("name") or "", base["label"] if base else None, per_task, take_all)
    except Exception as exc:  # noqa: BLE001  문항별 답 페이지 하나 때문에 보고서를 멈추지 않는다
        print(f"WARNING: answers.html 을 만들지 못했습니다: {type(exc).__name__}: {exc}", flush=True)
    return page


def write_safe(results, out_dir):
    """학습·평가 중에 부를 때: 보고서가 실패해도 학습은 계속한다."""
    try:
        page = write(results, out_dir)
        if page:
            print(f"보고서 → {page} · {Path(out_dir) / 'answers.html'}", flush=True)
        return page
    except Exception as exc:  # noqa: BLE001
        print(f"WARNING: 보고서를 만들지 못했습니다 ({out_dir}): {type(exc).__name__}: {exc}", flush=True)
        return None


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m train report", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("folder", help="결과 폴더 (results.json 이 있는 곳)")
    p.add_argument("--rescore", action="store_true", help="점수 캐시를 버리고 다시 채점 (채점 규칙을 고쳤을 때)")
    p.add_argument("--per-task", type=int, default=30, help="answers.html: 평가 세트·과제마다 보여 줄 문항 수 (기본 30)")
    p.add_argument("--all", action="store_true", help="answers.html: 모든 문항 (파일이 커짐)")
    a = p.parse_args(argv)
    folder = Path(a.folder).resolve()
    if not (folder / "results.json").is_file():
        raise SystemExit(f"{folder} 에 results.json 이 없습니다 (학습 실행 workdir · 실험 묶음 root · 평가만 하기 root)")
    page = write(read_json(folder / "results.json"), folder, a.rescore, a.per_task, a.all)
    print(f"보고서 → {page} · {folder / 'answers.html'} · {folder / 'scores.csv'}" if page else "점수가 있는 모델이 없습니다")


if __name__ == "__main__":
    main()
