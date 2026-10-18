"""명령줄 (research/multipage 에서 실행).

  python -m mpx gen   --out data/test --n 200 --split test
  python -m mpx stats --data data/test
  python -m mpx sft   --data data/train --budget 12000      # → data/train/swift_page, data/train/swift_all
  python -m mpx run   --data data/test --method pagewise --state context --base-url http://127.0.0.1:8000/v1 --model bank-ocr --out preds/pw_context.jsonl
  python -m mpx run   --data data/test --method pagewise --oracle --out preds/oracle.jsonl
  python -m mpx score --data data/test --pred preds/*.jsonl --out reports/compare
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .common import read_jsonl

KEY_METRICS = [
    ("doc_pages_exact", "문서 나누기 정확"), ("page_assign_acc", "쪽 배정"), ("field_f1", "항목 F1"),
    ("row_f1", "행 F1"), ("row_recall", "행 재현율"), ("row_dropped", "빠진 행 ↓"), ("cell_recall", "칸 재현율"),
    ("boundary_row_recall", "경계 행"), ("cont_row_recall", "이어지는 행"), ("check_balance_chain", "잔액 흐름"),
    ("check_items_sum", "품목 합계"),
]
COST_METRICS = [("requests_per_bundle", "요청/묶음"), ("image_tokens_per_bundle", "이미지 토큰/묶음"),
                ("max_prompt_tokens", "최대 입력 토큰"), ("completion_tokens_per_bundle", "출력 토큰/묶음"),
                ("latency_per_bundle", "초/묶음")]


def _fmt(v, pct=True):
    if v is None:
        return "—"
    if isinstance(v, float) and pct:
        return f"{v * 100:.1f}"
    return f"{v:,.0f}" if isinstance(v, (int, float)) else str(v)


def cmd_gen(a):
    from .gen import DISTRACTORS, TARGETS, generate

    targets = a.targets.split(",") if a.targets else TARGETS
    distractors = a.distractors.split(",") if a.distractors else DISTRACTORS
    generate(a.out, a.n, a.split, targets, distractors, heavy=a.heavy, no_repeat_header=a.no_repeat_header,
             augment=a.augment, start=a.start, workers=a.workers)
    print(f"→ {a.out}/bundles.jsonl")


def cmd_stats(a):
    from .gen import stats

    print(json.dumps(stats(a.data), ensure_ascii=False, indent=1))


def cmd_sft(a):
    from .sft import build

    print(json.dumps(build(a.data, a.out, a.methods.split(","), a.state, a.noise, a.budget, a.seed), ensure_ascii=False, indent=1))


def cmd_run(a):
    from .run import Client, run

    if not a.oracle and not (a.base_url and a.model):
        sys.exit("--base-url 과 --model 이 필요합니다 (또는 --oracle)")
    client = None if a.oracle else Client(a.base_url, a.model, a.max_tokens, a.timeout)
    out = run(a.data, a.out, a.method, a.state, client, a.workers, a.budget, a.limit)
    print(f"→ {out}")


def cmd_score(a):
    from .gen import load
    from .score import cost, score_bundle, summarize

    bundles, labels = load(a.data)
    by_id = {b["id"]: b for b in bundles}
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    table = {}
    for pred_path in a.pred:
        preds = read_jsonl(pred_path)
        name = Path(pred_path).stem
        results = [score_bundle(by_id[p["bundle"]], labels, p["docs"]) for p in preds if p["bundle"] in by_id]
        res = {"overall": summarize(results)["all"], "cost": cost(preds),
               "by_type": summarize(results, lambda d: d["type"]),
               "by_no_repeat_header": summarize(results, lambda d: "머리글 반복 없음" if d["no_repeat_header"] else "머리글 반복"),
               "by_pages": summarize(results, lambda d: f"{min(d['n_pages'], 4)}{'+' if d['n_pages'] >= 4 else ''}쪽"),
               "bundles": len(results)}
        (out / f"{name}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        table[name] = res
    md = report_md(table)
    (out / "report.md").write_text(md, encoding="utf-8")
    print(md)


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
        lines.append(f"| {name} | " + " | ".join(_fmt(res.get(k), pct=k in ("ocr_support",) or k.startswith("check_"))
                                                   for k, _ in keys) + " |")
    print("\n".join(lines))


def report_md(table: dict) -> str:
    lines = ["# 여러 쪽 문서 추출 비교", "", "점수는 % (↓ 는 낮을수록 좋음). 비용은 묶음 하나 기준.", ""]
    lines += ["| 방법 | 묶음 | " + " | ".join(n for _, n in KEY_METRICS) + " |",
              "|---|---:|" + "---:|" * len(KEY_METRICS)]
    for name, res in table.items():
        o = res["overall"]
        lines.append(f"| {name} | {res['bundles']} | " + " | ".join(_fmt(o.get(k)) for k, _ in KEY_METRICS) + " |")
    lines += ["", "| 방법 | " + " | ".join(n for _, n in COST_METRICS) + " |", "|---|" + "---:|" * len(COST_METRICS)]
    for name, res in table.items():
        c = res["cost"]
        lines.append(f"| {name} | " + " | ".join(_fmt(c.get(k), pct=False) if k != "latency_per_bundle" else f"{c.get(k, 0):.1f}"
                                                  for k, _ in COST_METRICS) + " |")
    for section, title in (("by_type", "서류별"), ("by_pages", "서류 쪽 수별"), ("by_no_repeat_header", "머리글 반복 여부별")):
        lines += ["", f"## {title} (행 F1 / 이어지는 행 / 항목 F1)", ""]
        groups = sorted({g for res in table.values() for g in res[section] if g != "all"})
        lines += ["| 방법 | " + " | ".join(groups) + " |", "|---|" + "---:|" * len(groups)]
        for name, res in table.items():
            cells = []
            for g in groups:
                s = res[section].get(g)
                cells.append("—" if not s else f"{_fmt(s.get('row_f1'))} / {_fmt(s.get('cont_row_recall'))} / {_fmt(s.get('field_f1'))}")
            lines.append(f"| {name} | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="mpx", description="서류 묶음 속 여러 쪽 문서 추출 연구")
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("gen", help="서류 묶음 만들기 (docgen 렌더링, Chromium 필요)")
    g.add_argument("--out", required=True)
    g.add_argument("--n", type=int, default=100, help="묶음(고객) 수")
    g.add_argument("--split", choices=["train", "test"], default="test")
    g.add_argument("--start", type=int, default=0, help="이어서 만들 때 시작 번호")
    g.add_argument("--workers", type=int, default=1, help="렌더링 프로세스 수 (Chromium 하나씩)")
    g.add_argument("--targets", help="대상 서류 ID (쉼표). 기본: 등기부, 등본, 거래내역, 인보이스, 패킹리스트, 재무제표")
    g.add_argument("--distractors", help="섞어 넣을 한 쪽 서류 ID (쉼표)")
    g.add_argument("--heavy", type=float, default=0.7, help="대상 서류를 목록이 긴 경우로 만들 확률")
    g.add_argument("--no-repeat-header", type=float, default=0.3, help="이어지는 쪽에 표 머리글을 반복하지 않을 확률")
    g.add_argument("--augment", type=float, default=0.3, help="스캔·촬영·팩스 증강 확률 (서류 단위)")
    g.set_defaults(fn=cmd_gen)

    s = sub.add_parser("stats", help="묶음·서류 쪽 수, 목록 행 수 분포")
    s.add_argument("--data", required=True)
    s.set_defaults(fn=cmd_stats)

    t = sub.add_parser("sft", help="ms-swift 학습 데이터 (<data>/swift_page, <data>/swift_all; training/train.py 로 학습)")
    t.add_argument("--data", required=True)
    t.add_argument("--out", help="기본: <data>")
    t.add_argument("--methods", default="pagewise,allatonce")
    t.add_argument("--state", default="mix", choices=["mix", "none", "doc", "tail", "context"])
    t.add_argument("--noise", type=float, default=0.2, help="상태를 일부러 틀리게 할 확률")
    t.add_argument("--budget", type=int, default=12000, help="한 번에 넣기의 이미지 토큰 합 상한")
    t.add_argument("--seed", type=int, default=0)
    t.set_defaults(fn=cmd_sft)

    r = sub.add_parser("run", help="모델 실행 (OpenAI 호환 서버) 또는 --oracle")
    r.add_argument("--data", required=True)
    r.add_argument("--out", required=True, help="예측 jsonl (있으면 남은 묶음만 이어서)")
    r.add_argument("--method", choices=["pagewise", "allatonce"], required=True)
    r.add_argument("--state", choices=["none", "doc", "tail", "context"], default="context")
    r.add_argument("--base-url")
    r.add_argument("--model")
    r.add_argument("--oracle", action="store_true", help="정답을 답으로 (파이프라인 확인용)")
    r.add_argument("--budget", type=int, default=12000)
    r.add_argument("--max-tokens", type=int, default=8192)
    r.add_argument("--timeout", type=float, default=900)
    r.add_argument("--workers", type=int, default=8, help="동시에 처리할 묶음 수")
    r.add_argument("--limit", type=int, default=0)
    r.set_defaults(fn=cmd_run)

    c = sub.add_parser("score", help="채점과 비교 보고서")
    c.add_argument("--data", required=True)
    c.add_argument("--pred", nargs="+", required=True)
    c.add_argument("--out", required=True)
    c.set_defaults(fn=cmd_score)

    k = sub.add_parser("check", help="정답 없는 실제 서류 묶음 검사 (OCR에 있는 값 비율, 잔액·합계)")
    k.add_argument("--data", required=True, help="bundles.jsonl 이 있는 폴더 (pages[].image, pages[].ocr)")
    k.add_argument("--pred", nargs="+", required=True)
    k.set_defaults(fn=cmd_check)

    args = ap.parse_args(argv)
    args.fn(args)
