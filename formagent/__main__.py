"""python -m formagent run|continue|status|stop|install (README.md)."""
from __future__ import annotations

import argparse
import json
import os
import sys

from . import relab as R
from . import runner


def settings(a) -> dict:
    """명령 옵션 → 설정. 비우면 ReLab 설정 파일(~/.relab/config.json)의 값."""
    s = {"relab": a.relab or os.environ.get("RELAB_BIN"), "provider": a.provider, "endpoint": a.endpoint, "model": a.model,
         "max_fix_rounds": a.rounds, "round_minutes": a.round_minutes}
    return {k: v for k, v in s.items() if v is not None}


def model_options(ap):
    ap.add_argument("--relab", help="relab 실행 파일 (없으면 찾고, 그래도 없으면 묶음으로 설치)")
    ap.add_argument("--provider", help="vllm · ollama · openai · openrouter (기본: ReLab 설정)")
    ap.add_argument("--endpoint", help="vLLM 주소 http://<host>:<port>/v1 (기본: ReLab 설정)")
    ap.add_argument("--model", help="served model 이름 (기본: ReLab 설정의 codingModel)")
    ap.add_argument("--rounds", type=int, help="고치기 회차 최대 (기본 3)")
    ap.add_argument("--round-minutes", type=float, help="회차 하나의 시간 한도 (기본 60분)")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m formagent", description="서식 이미지 → docgen 서식 (ReLab + 스킬 form-from-image)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="새로 만들기: 초안 폴더를 만들고 회차를 돈다")
    r.add_argument("--image", nargs="+", required=True, help="서식 이미지, 쪽 순서대로 (최대 3장)")
    r.add_argument("--id", required=True, help="서식 ID")
    r.add_argument("--kind", required=True, choices=list(runner.KINDS), help="원본 종류")
    r.add_argument("--note", help="사람의 추가 요청")
    model_options(r)
    c = sub.add_parser("continue", help="이어서: 사람의 지시(또는 질문에 대한 답)로 한 회차 + 고치기")
    c.add_argument("--id", required=True)
    c.add_argument("--message", required=True)
    model_options(c)
    g = sub.add_parser("go", help="start 로 만든 초안의 회차를 돈다 (studio 가 쓴다: 화면에서 검사한 뒤 작업으로)")
    g.add_argument("--id", required=True)
    s = sub.add_parser("status", help="상태 (run.json)")
    s.add_argument("--id", required=True)
    t = sub.add_parser("stop", help="멈추기")
    t.add_argument("--id", required=True)
    i = sub.add_parser("install", help="ReLab 이 없으면 묶음으로 설치하고 경로를 보여 준다")
    i.add_argument("--relab")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "install":
            print(R.ensure(a.relab))
        elif a.cmd == "run":
            runner.start(a.image, a.id, a.kind, a.note, settings(a))
            state = runner.go(a.id)
            sys.exit(0 if state["status"] == "done" else 3 if state["status"] == "waiting" else 1)
        elif a.cmd == "go":
            state = runner.go(a.id)
            sys.exit(0 if state["status"] == "done" else 3 if state["status"] == "waiting" else 1)
        elif a.cmd == "continue":
            state = runner.load(a.id)
            state["settings"].update(settings(a))
            runner.save(state)
            state = runner.go(a.id, message=a.message)
            sys.exit(0 if state["status"] == "done" else 3 if state["status"] == "waiting" else 1)
        elif a.cmd == "status":
            st = runner.load(a.id)
            print(json.dumps({k: st.get(k) for k in ("id", "status", "kind", "draft", "error", "question", "outside_changes")}
                             | {"rounds": [{k: r.get(k) for k in ("n", "exit", "seconds", "check")} for r in st["rounds"]]},
                             ensure_ascii=False, indent=1))
        elif a.cmd == "stop":
            runner.stop(a.id)
            print("멈춤 표시를 남겼습니다")
    except (runner.AgentError, R.RelabError) as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
