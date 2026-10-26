"""실험 여러 개를 한 화면에: 실험 묶음마다의 '한눈에 보기'를 모아 html 하나로 (python -m train summary).

  python -m train summary <묶음.json 또는 결과 폴더> ... --out runs/summary.html

- 인자는 묶음 파일(train/configs/E01-….json) 이나 그 결과 폴더(<root>, sweep.config.json 이 있는 곳). 섞어도 된다.
  결과 폴더만 주면 start_from 으로 가져온 출발 모델은 표에 없다 (묶음 파일로 주면 있다).
- 학습 실행·평가만 다시 한 workdir(reports/ 가 있는 곳)도 실험 하나로 받는다.
  줄은 compare_models · 출발 모델 · SFT · GRPO 순, 기준(괄호 %p)은 compare_models 가 있으면 그 첫 모델, 없으면 출발 모델.
- 따로 치지 않아도 학습 실행은 <workdir>/reports/summary.html, 실험 묶음은 <root>/summary.html 을 만든다 (그 실험 안의 모델만).
- 행은 평가 세트(id)·과제의 주 지표, 열은 실험별 모델. 괄호는 그 실험의 기준 모델(묶음의 baseline, 기본 첫 모델) 대비 %p.
- 실험마다 평가 문항이 다를 수 있다. 평가 세트마다 가장 많은 실험이 쓴 문항을 기준으로,
  문항이 다른 칸은 흐리게 † 를 붙인다 (그 칸은 다른 실험과 점수를 직접 비교하지 않는다).
  굵은 글씨는 기준 문항을 쓴 칸 중 가장 좋은 값.
- 실험마다 자세한 표는 각 <root>/compare.html, 평가만 한 workdir 는 reports/benchmark.html (링크).
- 학습·평가는 하지 않고 이미 끝난 보고서만 읽는다.
"""
import argparse
import html
import os
from collections import Counter
from pathlib import Path

from docgen.bench.ocr_data import read_json

from . import sweep as S


def workdir(path):
    """평가만 다시 한(또는 하나만 돌린) 파이프라인 workdir → 묶음 설정 꼴과 보고서 (pipeline 의 report 단계와 같은 순서)."""
    rep = path / "reports"
    cfg = read_json(path / "config.json") if (path / "config.json").is_file() else {}
    picks = (sorted(rep.glob("cmp-compare*.json"), key=lambda p: int(p.stem.removeprefix("cmp-compare") or 0))
             + [rep / "start.json", rep / "sft.json"] + sorted(rep.glob("grpo-*.json"), key=lambda p: p.stat().st_mtime))
    reports = [read_json(p) for p in picks if p.is_file()]
    cmp = [r for r in reports if r.get("role") == "other"]   # 평가만 다시 한 것: compare_models 첫 모델이 기준
    base = (cmp or [r for r in reports if r.get("role") == "start"] or reports)[:1]   # 학습 실행: 출발 모델이 기준
    runs = [{"label": r["label"], "about": r.get("model") or "", "train": []} for r in base + [r for r in reports if r not in base]]
    about = cfg.get("about") or ("평가만 다시 한 결과 (guide/eval.md)" if cmp else "학습 실행 (출발 모델 → SFT → GRPO)")
    sw = {"name": path.name, "about": about, "runs": runs, "_root": path, "_page": rep / "benchmark.html", "_reports": reports}
    return sw


def load(arg):
    """묶음 파일 · 결과 폴더 · 평가만 한 workdir → 묶음 설정 (sw)."""
    path = Path(arg).resolve()
    if path.is_dir():
        if not (path / "sweep.config.json").is_file():
            if (path / "reports").is_dir():
                return workdir(path)
            raise SystemExit(f"{path} 에 sweep.config.json 도 reports/ 도 없습니다 (실험 묶음 결과 폴더·묶음 파일·평가 workdir 를 주세요)")
        sw = read_json(path / "sweep.config.json")
        sw.pop("start_from", None)   # 묶음 파일 기준 상대 경로라 결과 폴더만으로는 못 찾는다
        return {**sw, "_root": path}
    return S.load(path)


def _scopes(r):
    if r.get("benchmarks"):
        return {i: (b.get("name") or i, b.get("items_sha256"), b["tasks"]) for i, b in r["benchmarks"].items()}
    return {"": ("", r.get("items_sha256"), r["tasks"])}


def gather(args, smoke=False):
    """실험마다 (sw, 보고서들, 뺀 이유). 끝난 모델이 없는 실험도 목록에는 남긴다."""
    out = []
    for a in args:
        sw = load(a)
        reports, notes = (sw["_reports"], []) if "_reports" in sw else S.collect(sw, smoke)
        out.append((sw, reports, notes))
    return out


def table(exps):
    """행: (평가 세트 id, 이름, 과제, 지표, 낮을수록 좋은지, 문항 수, 칸들). 칸: (값, 기준 대비 %p, 기준 문항인지)."""
    keys, hashes = {}, {}
    for sw, reports, _ in exps:
        for r in reports[:1]:
            for ident, (name, sha, tasks) in _scopes(r).items():
                hashes.setdefault(ident, []).append(sha)
                for task, t in tasks.items():
                    keys.setdefault((ident, task), (name, t["main"], t.get("n")))
    ref = {i: Counter(h).most_common(1)[0][0] for i, h in hashes.items()}
    order = list(hashes)
    rows = []
    for (ident, task), (name, metric, n) in sorted(keys.items(), key=lambda kv: order.index(kv[0][0])):   # 평가 세트끼리 붙여서
        cells = []
        for sw, reports, _ in exps:
            base = next((r for r in reports if r["label"] == S.baseline(sw)), None)

            def get(r):
                sc = _scopes(r).get(ident)
                return (sc[2].get(task, {}).get("metrics", {}).get(metric), sc[1]) if sc else (None, None)
            b = get(base)[0] if base else None
            for r in reports:
                v, sha = get(r)
                d = None if v is None or b is None or r is base or r["label"].startswith("출발 모델") else (v - b) * 100
                cells.append((v, d, sha == ref.get(ident)))
        rows.append((ident, name, task, metric, metric in S.LOWER, n, cells))
    return rows


CSS = """
:root{--fg:#1f2328;--muted:#656d76;--line:#d0d7de;--bg:#fff;--head:#f6f8fa;--up:#1a7f37;--down:#cf222e;--group:#eef2f6}
@media (prefers-color-scheme:dark){:root{--fg:#e6edf3;--muted:#8d96a0;--line:#30363d;--bg:#0d1117;--head:#161b22;--up:#3fb950;--down:#f85149;--group:#1c2430}}
body{font:14px/1.5 -apple-system,"Segoe UI","Malgun Gothic",sans-serif;color:var(--fg);background:var(--bg);margin:24px 16px;max-width:none}
h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:28px 0 8px}h3{font-size:15px;margin:16px 0 4px}
p,li{color:var(--muted)}a{color:inherit}
.wrap{overflow-x:auto}table{border-collapse:collapse;font-variant-numeric:tabular-nums}
th,td{border:1px solid var(--line);padding:4px 8px;text-align:right;white-space:nowrap}
th{background:var(--head)}td.l,th.l{text-align:left}td.exp{border-left:2px solid var(--fg)}
tr.g td{background:var(--group);font-weight:600;text-align:left}
.up{color:var(--up)}.down{color:var(--down)}.d{color:var(--muted)}.off{opacity:.45}b{font-weight:700}
.exp-list td{white-space:normal;text-align:left;vertical-align:top}
"""


def render(exps, out):
    out = Path(out).resolve()
    e = html.escape
    rows = table(exps)
    cols = [(sw, r["label"]) for sw, reports, _ in exps for r in reports]
    parts = [f"<h1>실험 모아 보기</h1><p>실험 {len(exps)}개 · 모델 {len(cols)}개. 점수 %, 괄호는 각 실험의 기준 모델(baseline, 기본 첫 모델) 대비 %p "
             "(초록 = 좋아짐, 빨강 = 나빠짐, ↓ 는 낮을수록 좋음). 굵게 = 같은 평가 문항을 쓴 칸 중 가장 좋은 값, "
             "흐린 † = 평가 문항이 다른 실험 (다른 실험과 직접 비교하지 않음).</p>"]
    parts.append("<h2>실험</h2><div class='wrap'><table class='exp-list'><tr><th class='l'>실험</th><th class='l'>무엇을 보나</th>"
                 "<th class='l'>모델</th><th class='l'>설명</th><th class='l'>바꾼 설정</th><th class='l'>학습 데이터</th></tr>")
    for sw, reports, notes in exps:
        done = {r["label"].removesuffix(" GRPO") for r in reports}
        link = sw.get("_page") or sw["_root"] / "compare.html"
        rel = os.path.relpath(link, out.parent) if link.exists() else None
        head = (f"<b>{e(sw['name'])}</b>" + (f"<br><a href='{e(Path(rel).as_posix())}'>자세한 비교표</a>" if rel else "")
                + (f"<br>기록: {e(sw['record'])}" if sw.get("record") else "")
                + "".join(f"<br><small>{e(n)}</small>" for n in notes))
        runs = sw["runs"]
        own = None if "_reports" in sw else sw   # 묶음이면 from_sft 로 물려받은 칸까지
        for i, r in enumerate(runs):
            first = (f"<td class='l' rowspan='{len(runs)}'>{head}</td><td class='l' rowspan='{len(runs)}'>{e(sw['about'])}</td>"
                     if i == 0 else "")
            state = "" if r["label"] in done else " <small>(결과 없음)</small>"
            parts.append(f"<tr>{first}<td class='l'>{e(r['label'])}{state}</td><td class='l'>{e(r['about'])}</td>"
                         f"<td class='l'>{e(S.changes(r, own))}</td><td class='l'>{S.train(r, own)}</td></tr>")
    parts.append("</table></div>")

    parts.append("<h2>한눈에 보기</h2><div class='wrap'><table><tr><th class='l' rowspan='2'>과제</th><th class='l' rowspan='2'>지표</th>"
                 "<th rowspan='2'>문항 수</th>")
    for sw, reports, _ in exps:
        if reports:
            parts.append(f"<th class='exp' colspan='{len(reports)}'>{e(sw['name'])}</th>")
    parts.append("</tr><tr>" + "".join(f"<th{' class=exp' if i == 0 else ''}>{e(r['label'])}</th>"
                                      for sw, reports, _ in exps for i, r in enumerate(reports)) + "</tr>")
    starts = {id(c) for _, reports, _ in exps for c in reports[:1]}
    first_col = [id(r) in starts for _, reports, _ in exps for r in reports]
    ident_now = object()
    for ident, name, task, metric, lower, n, cells in rows:
        if ident != ident_now:
            title = f"{e(name)} · {e(ident)}" if ident else "평가 세트 구분 없음 (data.benchmark 에 id 없음)"
            parts.append(f"<tr class='g'><td colspan='{3 + len(cols)}'>{title}</td></tr>")
        ident_now = ident
        ok = [v for v, _, same in cells if v is not None and same]
        best = (min(ok) if lower else max(ok)) if len(ok) > 1 else None
        tds = []
        for (v, d, same), edge in zip(cells, first_col):
            cls = " class='exp'" if edge else ""
            if v is None:
                tds.append(f"<td{cls}>—</td>")
                continue
            num = f"{v * 100:.1f}"
            num = f"<b>{num}</b>" if same and v == best else num
            delta = "" if d is None else (f" <span class='{'d' if abs(d) < 0.05 else ('up' if (d > 0) != lower else 'down')}'>({d:+.1f})</span>")
            tds.append(f"<td{cls}><span class='{'' if same else 'off'}'>{num}{'' if same else '†'}</span>{delta}</td>")
        parts.append(f"<tr><td class='l'>{e(task)}</td><td class='l'>{e(metric)}{' ↓' if lower else ''}</td><td>{n if n is not None else ''}</td>"
                     + "".join(tds) + "</tr>")
    parts.append("</table></div>")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
                   f"<title>실험 모아 보기</title><style>{CSS}</style></head><body>" + "".join(parts) + "</body></html>\n", encoding="utf-8")
    return out


def write_own(exps, out):
    """학습 실행·실험 묶음이 보고서를 쓸 때 그 실험 모델만의 한 화면 (실패해도 학습은 계속)."""
    try:
        return render(exps, out)
    except Exception as exc:  # noqa: BLE001  보고서 하나 때문에 멈추지 않는다
        print(f"WARNING: 한 화면 보고서를 만들지 못했습니다 ({out}): {type(exc).__name__}: {exc}", flush=True)
        return None


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m train summary", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("sweeps", nargs="+", help="묶음 파일 또는 결과 폴더 (<root>)")
    p.add_argument("--out", required=True, help="만들 html 파일")
    p.add_argument("--smoke", action="store_true", help="리허설(--smoke) 결과로")
    a = p.parse_args(argv)
    exps = gather(a.sweeps, a.smoke)
    print(f"모아 보기 → {render(exps, a.out)} (실험 {len(exps)}개, 모델 {sum(len(r) for _, r, _ in exps)}개)")
