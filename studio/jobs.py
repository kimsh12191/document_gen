"""오래 걸리는 일(데이터셋 빌드, OCR 준비)을 백그라운드 프로세스로 돌리고 진행을 보여 준다.

  <workspace_dir>/jobs/<작업ID>/job.json   종류, 명령, 상태(running/done/failed/cancelled/interrupted), 시작·끝, 진행, 결과
                               log.txt    명령의 출력 그대로

- 명령은 명령줄과 똑같은 것(예: python -m docgen.bench build --recipe …)을 그대로 실행한다. 화면 없이도 같은 결과.
- studio 를 다시 띄우면 돌던 작업은 "끊김"(interrupted)으로 표시된다. 생성이 끝난 데이터셋은 studio 를 띄울 때 한 번
  완료 파일을 확인해 자동 등록을 복구한다 (build_registration.py). 미완성 작업은 다시 실행해야 한다.
- 진행: 명령이 stderr 에 쓰는 "\\r서류 3/40" 같은 줄에서 마지막 "a/b" 를 읽는다.
- 끝나면 on_done(job) 을 부른다 (예: 만든 폴더를 데이터셋 등록부에 올리기).
- 같은 출력 폴더(info.out)로 도는 작업이 있거나 그 폴더가 이미 있으면 시작하지 않는다 (Conflict → HTTP 409).
- 시작하다 실패하면(명령을 못 띄움) 작업은 failed 로 남고 error 에 까닭을 적는다.
- 깨진 job.json 은 건너뛴다 (경고만 찍는다).
"""
from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

_PROGRESS = re.compile(r"(\d+)\s*/\s*(\d+)")
_LOG = logging.getLogger("studio.jobs")


class Conflict(ValueError):
    """같은 폴더로 도는 작업이 있거나 폴더가 이미 있다 (app.py guard 가 409 로 돌려준다)."""


def _read(f: Path) -> dict | None:
    """job.json 하나. 깨졌으면 경고만 찍고 None."""
    try:
        j = json.loads(f.read_text(encoding="utf-8"))
        if not isinstance(j, dict):
            raise ValueError("JSON 객체가 아님")
        return j
    except (OSError, ValueError) as e:
        _LOG.warning("작업 기록을 읽지 못해 건너뜁니다: %s (%s)", f, e)
        return None


class Jobs:
    def __init__(self, root: Path, cwd: Path):
        self.root = Path(root) / "jobs"
        self.cwd = cwd
        self.live: dict[str, subprocess.Popen] = {}
        self.busy: dict[str, str] = {}   # 작업 ID → 출력 폴더 (끝날 때까지 같은 폴더로 다른 작업을 못 띄움)
        self.lock = threading.Lock()
        self.root.mkdir(parents=True, exist_ok=True)
        for f in self.root.glob("*/job.json"):   # 지난번에 돌다 만 작업
            j = _read(f)
            if j is not None and j.get("status") == "running":
                j["status"] = "interrupted"
                f.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")

    def _file(self, job_id: str) -> Path:
        return self.root / job_id / "job.json"

    def get(self, job_id: str) -> dict:
        f = self._file(job_id)
        if not f.exists():
            raise KeyError(job_id)
        j = _read(f)
        if j is None:
            raise ValueError(f"작업 기록이 깨졌습니다: {f}")
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
            try:
                j = self.get(f.parent.name)
            except (KeyError, ValueError):   # 깨진 기록·막 지워진 폴더는 목록에서 뺀다
                continue
            if kind is None or j.get("kind") == kind:
                j.pop("log_tail", None)
                out.append(j)
        return out

    def _save(self, j: dict) -> None:
        f = self._file(j["id"])
        f.parent.mkdir(parents=True, exist_ok=True)
        tmp = f.with_name(f".{uuid.uuid4().hex}.tmp")
        try:
            tmp.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
            tmp.replace(f)
        finally:
            tmp.unlink(missing_ok=True)

    def start(self, kind: str, title: str, cmd: list[str], on_done=None, info: dict | None = None,
              cwd: Path | None = None, env: dict | None = None) -> dict:
        job_id = time.strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:4]
        out = (info or {}).get("out")
        with self.lock:   # 폴더 확인과 자리 잡기를 한 번에 (같은 이름을 두 번 눌러도 하나만)
            if out:
                key = str(Path(out).resolve())
                if key in self.busy.values():
                    raise Conflict(f"같은 폴더로 만드는 작업이 이미 돌고 있습니다: {out}")
                if Path(out).exists() and any(Path(out).iterdir()):
                    raise Conflict(f"이미 있는 폴더입니다: {out}. 다른 이름을 쓰세요 (만든 데이터셋은 덮어쓰지 않습니다)")
                self.busy[job_id] = key
        j = {"id": job_id, "kind": kind, "title": title, "cmd": cmd, "status": "running", "started": time.strftime("%Y-%m-%d %H:%M:%S"),
             "info": info or {}}
        log = None
        try:
            self._save(j)
            log = open(self.root / job_id / "log.txt", "wb")
            full_env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1", **(env or {})}
            group = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
            p = subprocess.Popen(cmd, cwd=str(cwd or self.cwd), stdout=log, stderr=subprocess.STDOUT, env=full_env, **group)
        except Exception as e:   # 명령을 못 띄움: "돌고 있음"으로 남기지 않는다
            if log is not None:
                log.close()
            with self.lock:
                self.busy.pop(job_id, None)
            j.update(status="failed", ended=time.strftime("%Y-%m-%d %H:%M:%S"), error=f"시작 실패: {type(e).__name__}: {e}")
            try:
                self._save(j)
            except OSError:
                pass
            raise
        with self.lock:
            self.live[job_id] = p

        def wait():
            try:
                finish()
            finally:
                with self.lock:
                    self.busy.pop(job_id, None)

        def finish():
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
                registration = bool(j2.get("info", {}).get("dataset"))
                j2["status"] = "running"
                j2["stage"] = "registering" if registration else "finalizing"
                self._save(j2)
                try:
                    j2["result"] = on_done(j2)
                    j2["status"] = "done"
                    j2["stage"] = "registered" if isinstance(j2["result"], dict) and j2["result"].get("dataset") else "done"
                except Exception as e:  # noqa: BLE001  후처리 실패도 작업 화면에 보인다
                    j2["status"] = "failed"
                    j2["stage"] = "registration_failed" if registration else "finalize_failed"
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
