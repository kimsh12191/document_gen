"""오래 걸리는 일(데이터셋 빌드, OCR prepare, 분석기 작업)을 백그라운드 프로세스로 돌리고 진행을 보여 준다.

  <workspace_dir>/jobs/<작업ID>/job.json   종류, 명령, 상태(running/done/failed/cancelled), 시작·끝, 진행, 결과
                               log.txt    명령의 출력 그대로

- 명령은 명령줄과 똑같은 것(예: python -m docgen.bench build --recipe …)을 그대로 실행한다. 화면 없이도 같은 결과.
- studio 를 다시 띄우면 돌던 작업은 "끊김"으로 표시된다 (명령을 다시 돌리면 된다).
- 진행: 명령이 stderr 에 쓰는 "\\r서류 3/40" 같은 줄에서 마지막 "a/b" 를 읽는다.
- 끝나면 on_done(job) 을 부른다 (예: 만든 폴더를 데이터셋 등록부에 올리기).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

_PROGRESS = re.compile(r"(\d+)\s*/\s*(\d+)")


class Jobs:
    def __init__(self, root: Path, cwd: Path):
        self.root = Path(root) / "jobs"
        self.cwd = cwd
        self.live: dict[str, subprocess.Popen] = {}
        self.lock = threading.Lock()
        self.root.mkdir(parents=True, exist_ok=True)
        for f in self.root.glob("*/job.json"):   # 지난번에 돌다 만 작업
            j = json.loads(f.read_text(encoding="utf-8"))
            if j.get("status") == "running":
                j["status"] = "interrupted"
                f.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")

    def _file(self, job_id: str) -> Path:
        return self.root / job_id / "job.json"

    def get(self, job_id: str) -> dict:
        f = self._file(job_id)
        if not f.exists():
            raise KeyError(job_id)
        j = json.loads(f.read_text(encoding="utf-8"))
        log = f.parent / "log.txt"
        if log.exists():
            tail = log.read_bytes()[-6000:].decode("utf-8", "replace")
            j["log_tail"] = tail.replace("\r", "\n")
            m = None
            for m in _PROGRESS.finditer(tail.splitlines()[-1] if tail.strip() else ""):
                pass
            if m is None:
                for line in reversed(tail.replace("\r", "\n").splitlines()):
                    found = list(_PROGRESS.finditer(line))
                    if found:
                        m = found[-1]
                        break
            if m and j.get("status") == "running":
                a, b = int(m.group(1)), int(m.group(2))
                if 0 < b and a <= b:
                    j["progress"] = [a, b]
        return j

    def list(self, kind: str | None = None) -> list[dict]:
        out = []
        for f in sorted(self.root.glob("*/job.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            j = self.get(f.parent.name)
            if kind is None or j.get("kind") == kind:
                j.pop("log_tail", None)
                out.append(j)
        return out

    def _save(self, j: dict) -> None:
        f = self._file(j["id"])
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")

    def start(self, kind: str, title: str, cmd: list[str], on_done=None, info: dict | None = None,
              cwd: Path | None = None, env: dict | None = None) -> dict:
        job_id = time.strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:4]
        j = {"id": job_id, "kind": kind, "title": title, "cmd": cmd, "status": "running", "started": time.strftime("%Y-%m-%d %H:%M:%S"),
             "info": info or {}}
        self._save(j)
        log = open(self.root / job_id / "log.txt", "wb")
        full_env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1", **(env or {})}
        group = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
        p = subprocess.Popen(cmd, cwd=str(cwd or self.cwd), stdout=log, stderr=subprocess.STDOUT, env=full_env, **group)
        with self.lock:
            self.live[job_id] = p

        def wait():
            code = p.wait()
            log.close()
            with self.lock:
                self.live.pop(job_id, None)
            j2 = json.loads(self._file(job_id).read_text(encoding="utf-8"))
            if j2["status"] == "cancelled":
                return
            j2["status"] = "done" if code == 0 else "failed"
            j2["code"] = code
            j2["ended"] = time.strftime("%Y-%m-%d %H:%M:%S")
            if code == 0 and on_done:
                try:
                    j2["result"] = on_done(j2)
                except Exception as e:  # noqa: BLE001  후처리 실패도 작업 화면에 보인다
                    j2["status"] = "failed"
                    j2["error"] = f"후처리 실패: {type(e).__name__}: {e}"
            self._save(j2)

        threading.Thread(target=wait, daemon=True).start()
        return j

    def cancel(self, job_id: str) -> dict:
        with self.lock:
            p = self.live.get(job_id)
        j = self.get(job_id)
        if p is None:
            raise ValueError("돌고 있는 작업이 아닙니다")
        j["status"] = "cancelled"
        j["ended"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self._save({k: v for k, v in j.items() if k not in ("log_tail", "progress")})
        if os.name == "nt":   # 여러 프로세스로 렌더링하는 빌드: 자식 프로세스까지
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
        else:
            import signal

            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        return j


def python() -> str:
    return sys.executable
