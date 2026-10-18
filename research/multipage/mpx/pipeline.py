"""한 번에 실행: 생성 → 통계 → 학습 데이터 → 실행(모든 방법) → 채점 → viewer.

  python -m mpx pipeline --out runs/local --n-train 8 --n-test 6 --workers 4                 # 모델 없이 (정답으로 점검)
  python -m mpx pipeline --out runs/exp1 --base-url http://127.0.0.1:8000/v1 --model mpx    # 띄워 둔 모델로

모델 없이 돌리면 각 방법을 정답(--oracle)으로 실행해 상태·병합·채점·viewer 가 끝까지 맞는지 확인하고(100% 여야 통과),
일부러 오류를 넣은 실행(simulated_errors)으로 채점과 viewer 가 오류를 잡는지도 본다. 모델 학습(GPU)은 run_experiment.sh.

출력 (<out>/):
  data/train, data/test     묶음 (학습은 random 구성, 평가는 벤치마크 시나리오 구성이 기본)
  data/train/swift_page, swift_all   학습 데이터 (training/train.py 용)
  preds/<방법>.jsonl         실행 결과 (allatonce, pagewise_none, pagewise_doc, pagewise_tail, pagewise_context)
  report/report.md          비교표
  data/test/viewer/index.html   viewer
  summary.json              단계별 소요 시간, 점검 결과
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from . import gen, report, sft, viewer
from .pages import STATES
from .run import Client, run

CHECK_KEYS = ("page_assign_acc", "doc_pages_exact", "field_f1", "row_f1", "boundary_row_recall", "cont_row_recall")


def _step(summary: dict, name: str, t0: float) -> float:
    t = time.monotonic()
    summary["seconds"][name] = round(t - t0, 1)
    print(f"[{name}] {t - t0:.1f}s", file=sys.stderr)
    return t


def run_all(out, n_train: int = 8, n_test: int = 6, workers: int = 4, base_url: str | None = None,
            model: str | None = None, states=STATES, budget: int = 12000, train_compose: str = "random",
            test_compose: str = "scenario", simulate: float = 0.1, max_tokens: int = 8192) -> dict:
    out = Path(out)
    train, test, preds = out / "data" / "train", out / "data" / "test", out / "preds"
    summary: dict = {"out": str(out), "model": model or "oracle", "seconds": {}}
    t = time.monotonic()

    gen.generate(train, n_train, "train", train_compose, workers=workers)
    gen.generate(test, n_test, "test", test_compose, workers=workers)
    summary["stats"] = {"train": gen.stats(train), "test": gen.stats(test)}
    t = _step(summary, "1 생성", t)

    summary["sft"] = sft.build(train, budget=budget)
    t = _step(summary, "2 학습 데이터", t)

    client = Client(base_url, model, max_tokens) if base_url else None
    runs = [("allatonce", "allatonce", None)] + [(f"pagewise_{s}", "pagewise", s) for s in states]
    paths = []
    for name, method, state in runs:
        paths.append(run(test, preds / f"{name}.jsonl", method, state or "none", client, workers=workers, budget=budget))
    if client is None and simulate:
        paths.append(run(test, preds / "simulated_errors.jsonl", "pagewise", "context", None, workers=workers,
                         budget=budget, simulate=simulate))
    t = _step(summary, "3 실행", t)

    md = report.compare(test, paths, out / "report")
    t = _step(summary, "4 채점", t)

    summary["viewer"] = str(viewer.build(test, paths))
    t = _step(summary, "5 viewer", t)

    # 점검: 정답으로 돌린 방법은 모든 지표가 100% 여야 하고, 오류를 넣은 실행은 100% 보다 낮아야 한다
    checks = {}
    if client is None:
        for p in paths:
            res = json.loads((out / "report" / f"{p.stem}.json").read_text(encoding="utf-8"))
            vals = {k: res["overall"].get(k) for k in CHECK_KEYS}
            perfect = all(v in (None, 1.0) for v in vals.values())
            checks[p.stem] = "통과" if perfect == (p.stem != "simulated_errors") else f"실패 {vals}"
    summary["checks"] = checks
    summary["report"] = str(out / "report" / "report.md")
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(md)
    return summary
