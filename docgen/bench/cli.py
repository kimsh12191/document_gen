"""python -m docgen.bench {build,run,eval}"""
from __future__ import annotations

import argparse


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="docgen.bench", description="OCR·은행업무 벤치마크")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="평가 세트 만들기")
    b.add_argument("--out", default="bench_out")
    b.add_argument("--types", default="all", help="단일 서류 과제에 쓸 서류: all | 서류ID,... | 그룹명")
    b.add_argument("--per-doc", type=int, default=1, help="서류 종류마다 샘플 수")
    b.add_argument("--scenarios", default="all", help="업무 묶음 과제에 쓸 시나리오: all | 이름,...")
    b.add_argument("--bundles", type=int, default=4, help="시나리오마다 고객 묶음 수 (짝수 번째는 cross_check 변조)")
    b.add_argument("--fields-per-doc", type=int, default=6, help="서류마다 ocr_field 문항 수")
    b.add_argument("--max-keys", type=int, default=40, help="kie·marks 문항 하나에 묻는 최대 항목 수")
    b.add_argument("--scale", type=float, default=2.0, help="이미지 배율 (2.0 ≈ 192dpi)")
    b.add_argument("--force", action="store_true", help="이미 있는 출력 폴더에 다시 만들기")

    r = sub.add_parser("run", help="모델 예측 (OpenAI 호환 API)")
    r.add_argument("--bench", default="bench_out")
    r.add_argument("--pred", required=True, help="예측 저장 폴더")
    r.add_argument("--tasks", default="all")
    r.add_argument("--base-url", help="예: http://localhost:8000/v1")
    r.add_argument("--model")
    r.add_argument("--api-key-env", default="OPENAI_API_KEY")
    r.add_argument("--system", help="시스템 프롬프트 (선택)")
    r.add_argument("--max-side", type=int, default=None, help="이미지 긴 변을 이 픽셀 이하로 줄여서 보냄")
    r.add_argument("--temperature", type=float, default=0.0)
    r.add_argument("--timeout", type=float, default=300)
    r.add_argument("--workers", type=int, default=4)
    r.add_argument("--limit", type=int, default=0, help="과제마다 앞에서 N 문항만 (빠른 점검용)")
    r.add_argument("--oracle", action="store_true", help="정답을 출력으로 (채점기 점검용)")

    e = sub.add_parser("eval", help="채점")
    e.add_argument("--bench", default="bench_out")
    e.add_argument("--pred", action="append", required=True, help="예측 폴더 (여러 번 주면 비교표)")
    e.add_argument("--tasks", default="all")

    args = ap.parse_args(argv)
    if args.cmd == "build":
        from .build import build
        build(args)
    elif args.cmd == "run":
        from .runner import run
        run(args)
    else:
        from .evaluate import evaluate
        evaluate(args)
