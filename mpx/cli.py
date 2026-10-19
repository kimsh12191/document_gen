"""명령줄 (저장소 루트에서 실행).

  python -m mpx gen   --out data/test --n 200 --split test
  python -m mpx stats --data data/test
  python -m mpx run   --data data/test --method allatonce --base-url http://127.0.0.1:8000/v1 --model bank-ocr --out preds/allatonce.jsonl
  python -m mpx run   --data data/test --method pagewise --oracle --out preds/oracle.jsonl
  python -m mpx score --data data/test --pred preds/*.jsonl --out reports/compare
  python -m mpx rows    --data data/test --pred preds/*.jsonl --out rows.jsonl      # 1단계: 행 결과 분류·특징
  python -m mpx analyze --rows rows.jsonl --out analysis.md                         # 1단계: 누락 분석
  python -m mpx probe   --data data/test --out probes --base-url ... --model ...     # 2단계: 통제 실험
  python -m mpx viewer --data data/test --pred preds/*.jsonl --serve 7862
  python -m mpx pipeline --out runs/check --n-test 6            # 한 번에 (모델 없으면 정답·오류 주입으로 점검)
  python -m mpx compare --runs base=runs/base bank=runs/bank --data data/test --out runs/compare   # 모델 비교
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .common import read_jsonl
from .report import fmt


def cmd_gen(a):
    from .gen import DISTRACTORS, TARGETS, generate

    targets = a.targets.split(",") if a.targets else TARGETS
    distractors = a.distractors.split(",") if a.distractors else DISTRACTORS
    generate(a.out, a.n, a.split, a.compose, targets, distractors, heavy=a.heavy, no_repeat_header=a.no_repeat_header,
             augment=a.augment, start=a.start, workers=a.workers, twins=a.twins)
    print(f"→ {a.out}/bundles.jsonl")


def cmd_stats(a):
    from .gen import stats

    print(json.dumps(stats(a.data), ensure_ascii=False, indent=1))


def _sampling(a) -> dict | None:
    return {"repetition_penalty": a.repetition_penalty} if a.repetition_penalty is not None else None


def cmd_run(a):
    from .run import Client, run

    if not a.oracle and not (a.base_url and a.model):
        sys.exit("--base-url 과 --model 이 필요합니다 (또는 --oracle)")
    client = None if a.oracle else Client(a.base_url, a.model, a.max_tokens, a.timeout, sampling=_sampling(a))
    out = run(a.data, a.out, a.method, client, a.workers, a.budget, a.limit, a.simulate, hint=not a.no_hint)
    print(f"→ {out}")


def cmd_score(a):
    from .report import compare

    print(compare(a.data, a.pred, a.out))


def cmd_viewer(a):
    from .viewer import build

    index = build(a.data, a.pred, a.out)
    print(f"→ {index}")
    if a.serve:
        import functools
        import http.server

        root = Path(a.data).resolve()
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
        rel = index.resolve().relative_to(root)
        print(f"http://{a.host}:{a.serve}/{rel}  (Ctrl+C 로 종료)")
        http.server.ThreadingHTTPServer((a.host, a.serve), handler).serve_forever()


def cmd_rows(a):
    from .rows import collect

    print(f"→ {collect(a.data, a.pred, a.out)}")


def cmd_analyze(a):
    from .analyze import run_analysis

    print(run_analysis(a.rows, a.out))


def cmd_probe(a):
    from .probe import KINDS, run_all
    from .run import Client

    if not a.oracle and not (a.base_url and a.model):
        sys.exit("--base-url 과 --model 이 필요합니다 (또는 --oracle)")
    client = None if a.oracle else Client(a.base_url, a.model, a.max_tokens, a.timeout, sampling=_sampling(a))
    kinds = a.kinds.split(",") if a.kinds else KINDS
    print(run_all(a.data, a.out, client, kinds, a.max_items, a.workers, a.simulate))


def cmd_pipeline(a):
    from .pipeline import run_all

    s = run_all(a.out, a.n_test, a.workers, a.base_url, a.model, a.budget, a.test_compose, a.simulate, a.max_tokens,
                a.probe_items, not a.no_hint, a.data, _sampling(a))
    print(json.dumps({k: s[k] for k in ("seconds", "checks", "outputs")}, ensure_ascii=False, indent=1))


def cmd_compare(a):
    from .pipeline import compare

    runs = dict(x.split("=", 1) for x in a.runs)
    print(json.dumps(compare(runs, a.data, a.out), ensure_ascii=False, indent=1))


def cmd_check(a):
    from .gen import load
    from .score import check_real, summarize_real

    bundles, _ = load(a.data)
    by_id = {b["id"]: b for b in bundles}
    rows = []
    for pred_path in a.pred:
        preds = [p for p in read_jsonl(pred_path) if p["bundle"] in by_id]
        res = summarize_real([check_real(by_id[p["bundle"]], p["docs"], a.data) for p in preds])
        rows.append((Path(pred_path).stem, res))
    keys = [("bundles", "묶음"), ("docs_per_bundle", "문서/묶음"), ("rows_per_bundle", "행/묶음"),
            ("ocr_support", "OCR에 있는 값"), ("check_balance_chain", "잔액 흐름"), ("check_items_sum", "품목 합계")]
    lines = ["| 방법 | " + " | ".join(n for _, n in keys) + " |", "|---|" + "---:|" * len(keys)]
    for name, res in rows:
        lines.append(f"| {name} | " + " | ".join(fmt(res.get(k), pct=k in ("ocr_support",) or k.startswith("check_"))
                                                   for k, _ in keys) + " |")
    print("\n".join(lines))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="mpx", description="여러 쪽 문서 추출에서 행이 빠지는 원인 연구")
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("gen", help="서류 묶음 만들기 (docgen 렌더링, Chromium 필요)")
    g.add_argument("--out", required=True)
    g.add_argument("--n", type=int, default=100, help="묶음(고객) 수")
    g.add_argument("--split", choices=["train", "test"], default="test")
    g.add_argument("--compose", choices=["scenario", "random"], default="scenario",
                   help="scenario: 벤치마크 업무 시나리오 묶음(기본), random: 대상 서류 위주로 무작위")
    g.add_argument("--start", type=int, default=0, help="이어서 만들 때 시작 번호")
    g.add_argument("--workers", type=int, default=1, help="렌더링 프로세스 수 (Chromium 하나씩)")
    g.add_argument("--targets", help="대상 서류 ID (쉼표). 기본: 등기부, 등본, 거래내역, 인보이스, 패킹리스트, 재무제표")
    g.add_argument("--distractors", help="섞어 넣을 한 쪽 서류 ID (쉼표)")
    g.add_argument("--heavy", type=float, default=0.7, help="대상 서류를 목록이 긴 경우로 만들 확률")
    g.add_argument("--no-repeat-header", type=float, default=0.3, help="이어지는 쪽에 표 머리글을 반복하지 않을 확률")
    g.add_argument("--augment", type=float, default=0.3, help="random 구성의 스캔·촬영·팩스 증강 확률 (scenario 는 벤치마크 조건)")
    g.add_argument("--twins", action="store_true", help="머리글을 뺀 서류마다 머리글을 반복한 쌍둥이 판도 (통제 실험 D)")
    g.set_defaults(fn=cmd_gen)

    s = sub.add_parser("stats", help="묶음·서류 쪽 수, 목록 행 수 분포")
    s.add_argument("--data", required=True)
    s.set_defaults(fn=cmd_stats)

    r = sub.add_parser("run", help="모델 실행 (OpenAI 호환 서버) 또는 --oracle")
    r.add_argument("--data", required=True)
    r.add_argument("--out", required=True, help="예측 jsonl (있으면 남은 묶음만 이어서)")
    r.add_argument("--method", choices=["pagewise", "allatonce"], required=True)
    r.add_argument("--base-url")
    r.add_argument("--model")
    r.add_argument("--oracle", action="store_true", help="정답을 답으로 (파이프라인 확인용)")
    r.add_argument("--budget", type=int, default=12000)
    r.add_argument("--max-tokens", type=int, default=20480)
    r.add_argument("--repetition-penalty", type=float, help="주지 않으면 서버 기본값 (모델의 generation_config.json)")
    r.add_argument("--timeout", type=float, default=900)
    r.add_argument("--workers", type=int, default=8, help="동시에 처리할 묶음 수")
    r.add_argument("--limit", type=int, default=0)
    r.add_argument("--simulate", type=float, default=0.0, help="--oracle 에 일부러 오류를 넣을 확률 (채점·viewer 시험용)")
    r.add_argument("--no-hint", action="store_true", help="질문에 목록·칸 이름을 알려 주지 않음")
    r.set_defaults(fn=cmd_run)

    c = sub.add_parser("score", help="채점과 비교 보고서")
    c.add_argument("--data", required=True)
    c.add_argument("--pred", nargs="+", required=True)
    c.add_argument("--out", required=True)
    c.set_defaults(fn=cmd_score)

    v = sub.add_parser("viewer", help="묶음별 쪽 이미지·정답·방법별 답 비교 HTML")
    v.add_argument("--data", required=True)
    v.add_argument("--pred", nargs="+", required=True)
    v.add_argument("--out", help="기본: <data>/viewer")
    v.add_argument("--serve", type=int, help="이 포트로 바로 띄우기 (예: 7862)")
    v.add_argument("--host", default="127.0.0.1", help="다른 PC 에서 열려면 0.0.0.0")
    v.set_defaults(fn=cmd_viewer)

    w = sub.add_parser("rows", help="1단계: 정답 행마다 결과 분류와 특징 → rows.jsonl")
    w.add_argument("--data", required=True)
    w.add_argument("--pred", nargs="+", required=True)
    w.add_argument("--out", required=True)
    w.set_defaults(fn=cmd_rows)

    z = sub.add_parser("analyze", help="1단계: 결과 분포, 특징별 누락률, 회귀 → analysis.md")
    z.add_argument("--rows", required=True)
    z.add_argument("--out", required=True)
    z.set_defaults(fn=cmd_analyze)

    o = sub.add_parser("probe", help="2단계: 통제 실험 (해상도, 출력 길이, 이미지 수, 머리글)")
    o.add_argument("--data", required=True)
    o.add_argument("--out", required=True)
    o.add_argument("--kinds", help="쉼표로 (기본: resolution,scope,images,header)")
    o.add_argument("--max-items", type=int, default=40, help="실험마다 기준 쪽 수")
    o.add_argument("--base-url")
    o.add_argument("--model")
    o.add_argument("--oracle", action="store_true")
    o.add_argument("--simulate", type=float, default=0.0)
    o.add_argument("--max-tokens", type=int, default=20480)
    o.add_argument("--repetition-penalty", type=float, help="F 실험 외 문항에 줄 값. 주지 않으면 서버 기본값")
    o.add_argument("--timeout", type=float, default=900)
    o.add_argument("--workers", type=int, default=8)
    o.set_defaults(fn=cmd_probe)

    q = sub.add_parser("pipeline", help="생성→관찰 실행→행 기록→분석→통제 실험→종합·viewer 를 한 번에")
    q.add_argument("--out", required=True)
    q.add_argument("--n-test", type=int, default=6)
    q.add_argument("--workers", type=int, default=4)
    q.add_argument("--base-url", help="없으면 정답·오류 주입으로 점검 실행")
    q.add_argument("--model")
    q.add_argument("--budget", type=int, default=12000)
    q.add_argument("--max-tokens", type=int, default=20480)
    q.add_argument("--repetition-penalty", type=float, help="주지 않으면 서버 기본값 (모델의 generation_config.json)")
    q.add_argument("--data", help="이미 만든 묶음 폴더를 쓴다 (생성 건너뜀; 모델 여러 개를 같은 묶음으로)")
    q.add_argument("--test-compose", choices=["scenario", "random"], default="scenario")
    q.add_argument("--simulate", type=float, default=0.1, help="모델 없을 때 오류 주입 확률")
    q.add_argument("--probe-items", type=int, default=40, help="통제 실험마다 기준 쪽 수")
    q.add_argument("--no-hint", action="store_true")
    q.set_defaults(fn=cmd_pipeline)

    m = sub.add_parser("compare", help="모델별 pipeline 결과를 합쳐 분석·통제 실험·viewer 비교")
    m.add_argument("--runs", nargs="+", required=True, help="이름=pipeline 출력 폴더 (예: base=runs/base bank=runs/bank)")
    m.add_argument("--data", required=True, help="모델들이 함께 쓴 묶음 폴더")
    m.add_argument("--out", required=True)
    m.set_defaults(fn=cmd_compare)

    k = sub.add_parser("check", help="정답 없는 실제 서류 묶음 검사 (OCR에 있는 값 비율, 잔액·합계)")
    k.add_argument("--data", required=True, help="bundles.jsonl 이 있는 폴더 (pages[].image, pages[].ocr)")
    k.add_argument("--pred", nargs="+", required=True)
    k.set_defaults(fn=cmd_check)

    args = ap.parse_args(argv)
    args.fn(args)
