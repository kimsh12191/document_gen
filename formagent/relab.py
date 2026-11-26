"""ReLab CLI 찾기·설치·실행.

찾는 순서: 직접 준 경로 → 환경 변수 RELAB_BIN → PATH 의 relab → 기본 설치 자리(~/.local/share/relab-cli/bin/relab).
없으면 이 폴더의 묶음(relab/wheels, 리눅스 x86_64, Python 3.10~3.13)으로 인터넷 없이 설치한다.
배포 묶음의 install.sh 와 같은 방식: 자리에 venv 를 만들고 pip --no-index 로 relab==<VERSION> 을 넣는다.
"""
from __future__ import annotations

import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent / "relab"
VERSION = (BUNDLE / "VERSION").read_text(encoding="utf-8").strip()
DEFAULT_HOME = Path.home() / ".local" / "share" / "relab-cli"


class RelabError(RuntimeError):
    pass


def works(path: str | Path) -> bool:
    """relab chat --help 가 되는지."""
    try:
        return subprocess.run([str(path), "chat", "--help"], capture_output=True, timeout=60).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def find(given: str | None = None) -> str | None:
    """쓸 수 있는 relab 실행 파일, 없으면 None. 경로를 직접 줬으면 그것만 본다."""
    candidates = [given] if given else [os.environ.get("RELAB_BIN"), shutil.which("relab"), DEFAULT_HOME / "bin" / "relab"]
    for candidate in candidates:
        if candidate and Path(candidate).is_file() and works(candidate):
            return str(candidate)
    return None


def install(home: Path = DEFAULT_HOME, log=print) -> str:
    """묶음으로 설치하고 relab 경로를 돌려준다."""
    if not (3, 10) <= sys.version_info[:2] <= (3, 13):
        raise RelabError(f"ReLab 묶음은 Python 3.10~3.13 용입니다 (지금 {sys.version.split()[0]})")
    if not sys.platform.startswith("linux"):
        raise RelabError("ReLab 묶음은 리눅스 x86_64 용입니다. 다른 OS 는 배포 묶음(install.cmd)으로 따로 설치하세요")
    home = Path(home).expanduser()
    log(f"ReLab {VERSION} 설치: {home}")
    python = home / "bin" / "python"
    if not python.exists():
        subprocess.run([sys.executable, "-m", "venv", str(home)], check=True)
    p = subprocess.run([str(python), "-m", "pip", "install", "--upgrade", "--no-index", "--find-links", str(BUNDLE / "wheels"),
                        f"relab=={VERSION}", "--disable-pip-version-check", "-q"], capture_output=True, text=True)
    if p.returncode != 0:
        raise RelabError("ReLab 설치 실패:\n" + (p.stderr or p.stdout)[-2000:])
    relab = home / "bin" / "relab"
    if not works(relab):
        raise RelabError(f"설치했지만 {relab} chat --help 가 되지 않습니다")
    return str(relab)


def ensure(given: str | None = None, home: Path = DEFAULT_HOME, log=print) -> str:
    """있으면 그것, 없으면 설치."""
    found = find(given)
    if found:
        return found
    if given:
        raise RelabError(f"relab 을 실행할 수 없습니다: {given}")
    return install(home, log)


def command(relab: str, request: str, workspace: Path, provider: str | None = None, endpoint: str | None = None,
            model: str | None = None) -> list[str]:
    """비대화 실행 명령: 요청 하나, 묻지 않고 승인."""
    cmd = [relab, "chat", "-p", request, "--auto", "--workspace", str(workspace)]
    for flag, value in (("--provider", provider), ("--endpoint", endpoint), ("--model", model)):
        if value:
            cmd += [flag, value]
    return cmd


def run(cmd: list[str], log_file: Path, cwd: Path, timeout_minutes: float = 60, on_start=None, stopped=lambda: False) -> int | None:
    """실행하고 출력을 log_file 에 그대로 쓴다. 종료 코드 (시간 초과·멈춤이면 None).

    종료 코드: 0 완료, 1 미완료, 2 시작 못 함, 3 모델이 묻고 기다림 (ReLab MANUAL 5장)."""
    env = {**os.environ, "NO_COLOR": "1"}
    with open(log_file, "w", encoding="utf-8") as out:
        proc = subprocess.Popen(cmd, cwd=cwd, stdout=out, stderr=subprocess.STDOUT, env=env, start_new_session=True)
        if on_start:
            on_start(proc.pid)
        end = time.time() + timeout_minutes * 60
        while proc.poll() is None:
            if stopped() or time.time() > end:
                why = "멈춤" if stopped() else f"{timeout_minutes}분 넘음"
                try:
                    os.killpg(proc.pid, signal.SIGTERM)
                    proc.wait(10)
                except (ProcessLookupError, subprocess.TimeoutExpired):
                    os.killpg(proc.pid, signal.SIGKILL)
                out.write(f"\n[formagent] relab 을 끝냄: {why}\n")
                return None
            time.sleep(1)
        return proc.returncode
