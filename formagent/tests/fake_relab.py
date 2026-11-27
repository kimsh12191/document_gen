#!/usr/bin/env python3
"""시험용 relab: `relab chat -p <요청> …` 을 흉내 낸다.

환경 변수 FAKE_RELAB_PLAN 의 JSON 파일에서 실행마다 한 줄씩 꺼내 그대로 한다:
  {"write": {"<작업 공간 기준 경로>": "<내용>"}, "exit": 0, "sleep": 0, "say": "<출력>"}
받은 요청은 FAKE_RELAB_PLAN 옆 requests.jsonl 에 남긴다.
"""
import json
import os
import sys
import time
from pathlib import Path

args = sys.argv[1:]
if "--help" in args:
    print("usage: relab chat [-p REQUEST] [--auto] [--workspace W]")
    sys.exit(0)
plan_file = Path(os.environ["FAKE_RELAB_PLAN"])
request = args[args.index("-p") + 1]
workspace = Path(args[args.index("--workspace") + 1])
with open(plan_file.with_name("requests.jsonl"), "a", encoding="utf-8") as f:
    f.write(json.dumps({"request": request, "argv": args,
                        "env": {k: os.environ.get(k) for k in ("RELAB_PRIVATE_HOME", "RELAB_EXECUTION_PYTHON")}}, ensure_ascii=False) + "\n")
plan = json.loads(plan_file.read_text(encoding="utf-8"))
step = plan.pop(0) if plan else {"exit": 0}
plan_file.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
for path, text in (step.get("write") or {}).items():
    target = workspace / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
print(step.get("say", "● 가짜 relab"), flush=True)
time.sleep(step.get("sleep", 0))
sys.exit(step.get("exit", 0))
