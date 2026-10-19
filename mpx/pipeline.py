"""한 번에 실행: ① 생성 → ② 관찰 실행 → ③ 행 기록·분류 → ④ 분석 → ⑤ 통제 실험 → ⑥ 종합표·viewer.

  python -m mpx pipeline --out runs/check --n-test 6                                            # 모델 없이 점검
  python -m mpx pipeline --out runs/obs1 --n-test 100 --base-url http://127.0.0.1:8000/v1 --model bank-ocr

① 생성       평가 묶음(벤치마크 시나리오 구성 + 긴 목록, 머리글 쌍둥이 판 포함)
② 관찰 실행  한 번에 넣기(allatonce, 2부 방식)와 쪽 단위(pagewise, 원래 해상도). 모델이 없으면 정답을 답으로
             넣은 실행(oracle_*)과 일부러 오류를 넣은 실행(simulated_*) 두 가지.
③ 행 기록    정답 행마다 결과 분류와 특징 → rows.jsonl
④ 분석       결과 분포, 특징별 누락률, 회귀 → analysis.md
⑤ 통제 실험  해상도·출력 길이·이미지 수·머리글 → probes/probes.md, probes/viewer.html (모델 없으면 probes_oracle, probes_simulated)
⑥ 종합       방법별 점수표 report/report.md, 묶음 viewer data/test/viewer/index.html

모델 없이 돌릴 때의 점검 (summary.json 의 checks, 모두 '통과'여야 함)
  oracle 실행은 모든 정답 행이 exact 이고 종합 지표가 100%
  simulated 실행은 넣은 오류 종류(일부 틀림·잘못 읽음·다른 곳에·건너뜀·길이에 잘림)를 분류가 모두 찾아냄
  통제 실험 oracle 은 누락 0, simulated 는 누락 > 0, 머리글 실험(쌍둥이 판) 문항이 생김
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter
from pathlib import Path

from . import analyze, gen, probe, report, rows, viewer
from .common import read_jsonl
from .run import Client, run

CHECK_KEYS = ("page_assign_acc", "doc_pages_exact", "field_f1", "row_f1", "boundary_row_recall", "cont_row_recall")
SIM_EXPECT = ("partial", "misread", "misplaced", "skipped", "cut_length")


def _step(summary: dict, name: str, t0: float) -> float:
    t = time.monotonic()
    summary["seconds"][name] = round(t - t0, 1)
    print(f"[{name}] {t - t0:.1f}s", file=sys.stderr)
    return t


def run_all(out, n_test: int = 6, workers: int = 4, base_url: str | None = None,
            model: str | None = None, budget: int = 12000, test_compose: str = "scenario",
            simulate: float = 0.1, max_tokens: int = 16384, probe_items: int = 40, hint: bool = True) -> dict:
    out = Path(out)
    test, preds = out / "data" / "test", out / "preds"
    summary: dict = {"out": str(out), "model": model or "oracle", "seconds": {}}
    t = time.monotonic()

    gen.generate(test, n_test, "test", test_compose, workers=workers, twins=True)
    summary["stats"] = {"test": gen.stats(test)}
    t = _step(summary, "1 생성", t)

    client = Client(base_url, model, max_tokens) if base_url else None
    paths = []
    for method in ("allatonce", "pagewise"):
        if client:
            paths.append(run(test, preds / f"{method}.jsonl", method, client, workers, budget, hint=hint))
            continue
        paths.append(run(test, preds / f"oracle_{method}.jsonl", method, None, workers, budget, hint=hint))
        if simulate:
            paths.append(run(test, preds / f"simulated_{method}.jsonl", method, None, workers, budget,
                             simulate=simulate, hint=hint))
    t = _step(summary, "2 관찰 실행", t)

    rows_path = rows.collect(test, paths, out / "rows.jsonl")
    t = _step(summary, "3 행 기록", t)

    analyze.run_analysis(rows_path, out / "analysis.md")
    t = _step(summary, "4 분석", t)

    probe_runs = {"probes": (client, 0.0)} if client else {"probes_oracle": (None, 0.0), "probes_simulated": (None, max(simulate, 0.1))}
    for name, (c, sim) in probe_runs.items():
        probe.run_all(test, out / name, c, max_items=probe_items, workers=workers, simulate=sim)
    t = _step(summary, "5 통제 실험", t)

    report.compare(test, paths, out / "report")
    summary["viewer"] = str(viewer.build(test, paths))
    t = _step(summary, "6 종합·viewer", t)

    summary["checks"] = _checks(out, paths, probe_runs) if client is None else {}
    summary["outputs"] = {"analysis": str(out / "analysis.md"), "probes": [str(out / n / "probes.md") for n in probe_runs],
                          "probe_viewer": [str(out / n / "viewer.html") for n in probe_runs],
                          "report": str(out / "report" / "report.md"), "viewer": summary["viewer"]}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    return summary


def _checks(out: Path, paths: list[Path], probe_runs: dict) -> dict:
    checks = {}
    outcomes = {}
    for r in read_jsonl(out / "rows.jsonl"):
        outcomes.setdefault(r["run"], Counter())[r["outcome"]] += 1
    for p in paths:
        c = outcomes.get(p.stem, Counter())
        res = json.loads((out / "report" / f"{p.stem}.json").read_text(encoding="utf-8"))["overall"]
        if p.stem.startswith("oracle_"):
            bad = {k: res.get(k) for k in CHECK_KEYS if res.get(k) not in (None, 1.0)}
            ok = set(c) == {"exact"} and not bad
            checks[p.stem] = "통과" if ok else f"실패: 결과 {dict(c)}, 지표 {bad}"
        else:
            missing = [o for o in SIM_EXPECT if not c.get(o)]
            checks[p.stem] = "통과" if not missing else f"실패: 분류가 못 찾은 오류 {missing} (결과 {dict(c)})"
    for name in probe_runs:
        pr = read_jsonl(out / name / "rows.jsonl")
        kinds = {r["kind"] for r in pr}
        dropped = sum(r["dropped"] for r in pr)
        if name.endswith("oracle"):
            ok = pr and all(r["outcome"] == "exact" for r in pr)
            checks[name] = "통과" if ok else f"실패: 정답 답인데 exact 가 아닌 행 {sum(r['outcome'] != 'exact' for r in pr)}"
        else:
            checks[name] = "통과" if dropped else "실패: 오류를 넣었는데 누락이 0"
        if "header" not in kinds:
            checks[name] += " (머리글 실험 문항 없음: 머리글 없는 여러 쪽 서류가 생성되지 않았음)"
    return checks
