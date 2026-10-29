"""GPU 상태 (nvidia-smi). 컨테이너 안에서는 다른 컨테이너의 프로세스가 안 보일 수 있어서, 비었는지는 메모리로 본다."""
from __future__ import annotations

import shutil
import subprocess

GPU_QUERY = "index,uuid,name,memory.used,memory.total,utilization.gpu"
APP_QUERY = "gpu_uuid,pid,used_memory"
FREE_MIB = 1024   # 이만큼 안 쓰고 보이는 프로세스도 없으면 "비어 있음"


def _smi(args: list[str]) -> str:
    exe = shutil.which("nvidia-smi")
    if not exe:
        raise RuntimeError("nvidia-smi 가 없습니다 (GPU 컨테이너에서 띄우세요)")
    return subprocess.run([exe, *args, "--format=csv,noheader,nounits"], capture_output=True, text=True,
                          timeout=15, check=True).stdout


def _rows(text: str) -> list[list[str]]:
    return [[c.strip() for c in line.split(",")] for line in text.splitlines() if line.strip()]


def _num(v: str) -> float | None:
    try:
        return float(v)
    except ValueError:   # [N/A]
        return None


def parse(gpu_csv: str, app_csv: str) -> list[dict]:
    apps: dict[str, list[dict]] = {}
    for uuid, pid, used in (r[:3] for r in _rows(app_csv) if len(r) >= 3):
        if pid.isdigit():
            apps.setdefault(uuid, []).append({"pid": int(pid), "mib": _num(used)})
    out = []
    for r in _rows(gpu_csv):
        if len(r) < 6:
            continue
        index, uuid, name, used, total, util = r[:6]
        procs = apps.get(uuid, [])
        used_mib = _num(used)
        out.append({"index": int(index), "name": name, "used_mib": used_mib, "total_mib": _num(total), "util": _num(util),
                    "procs": procs, "free": not procs and used_mib is not None and used_mib < FREE_MIB})
    return out


def status() -> dict:
    """{"gpus": [{index, name, used_mib, total_mib, util, procs:[{pid, mib}], free}]} 또는 {"gpus": [], "error"}."""
    try:
        return {"gpus": parse(_smi([f"--query-gpu={GPU_QUERY}"]), _smi([f"--query-compute-apps={APP_QUERY}"]))}
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        return {"gpus": [], "error": str(exc)}
