"""⑥ 데이터셋 › 생성 현황: 완성한 데이터셋 자동 등록. 재시작으로 놓친 완료 처리도 작업 기록과 완료 파일로 복구한다.

- 생성 작업(build_bank·build_ocr: 은행 서류 레시피, 합성 OCR 레시피)은 job.json 의 info.dataset 에
  등록할 {path, name, meta} 를 남기고, 끝나면 register_output 으로 등록부(studio/datasets.py)에 올린다.
- recover_completed 는 studio 를 띄울 때, 그리고 끊긴(interrupted) 작업이 있는 동안 30초마다 돈다 (app.py, settle_interrupted):
  끊긴 작업이라도 완료 파일이 다 있으면 등록한다. 프로세스가 끝났는데 완료 파일이 없으면 실패로 바꾼다.
  은행 서류는 dataset.json·meta.json 과 tasks/<과제>.jsonl 문항 수, OCR 은 prepared/DONE.json·pages.jsonl 로 완료를 판단한다.
- <workspace_dir>/datasets/ 밖의 폴더, 실패·취소한 작업은 등록하지 않는다. 같은 폴더는 한 번만 등록한다.
- forget_job·cleanup_jobs: 끝난 작업 기록(jobs/<ID>/)을 지운다. 데이터셋 폴더는 지우지 않는다.
"""
from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path

BUILD_KINDS = {"build_bank", "build_ocr"}
_LOCK = threading.Lock()


def register_output(registry, spec: dict) -> dict:
    """같은 출력 폴더의 완료 콜백·복구가 겹쳐도 등록은 한 번만 한다."""
    root = Path(spec["path"]).resolve()
    try:
        ds = registry.register(str(root), spec["name"], **{**spec.get("meta", {}), "made_by_studio": True})
    except ValueError:
        ds = next(({"id": key, **value} for key, value in registry.load()["datasets"].items()
                   if Path(value["path"]).resolve() == root), None)
        if ds is None:
            raise
    return {"dataset": ds["id"]}


def _spec(job: dict) -> dict | None:
    info = job.get("info") or {}
    if info.get("dataset"):
        spec = info["dataset"]
        return spec if isinstance(spec, dict) and isinstance(spec.get("path"), str) and isinstance(spec.get("name"), str) and isinstance(spec.get("meta", {}), dict) else None
    # 기존 작업도 복구한다. 현재 레시피 대신 생성된 파일의 레시피를 우선한다.
    if not info.get("out") or job.get("kind") not in BUILD_KINDS:
        return None
    out = Path(info["out"])
    bank = job["kind"] == "build_bank"
    manifest = out / ("dataset.json" if bank else "ocr_set.json")
    try:
        snapshot = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    meta = {"dataset_json": "dataset.json" if bank else "../ocr_set.json",
            "purpose": (snapshot.get("recipe") or {}).get("about", "")}
    if bank:
        meta.update(source="synthetic", gt="exact")
    if isinstance(info.get("recipe"), str):
        meta["recipe"] = f"docgen/recipes/{Path(info['recipe']).name}.json"
    return {"path": str(out if bank else out / "prepared"), "name": out.name, "meta": meta}


def _complete(registry, job: dict, spec: dict) -> bool:
    root = Path(spec["path"]).resolve()
    if not root.is_relative_to((registry.ws / "datasets").resolve()):
        return False
    try:
        # 과제 폴더(docgen-tasks): meta.json 문항 수 = tasks/ 줄 수, dataset.json 이 있으면 그 수와도 같음,
        # OCR 준비 폴더(pages.jsonl)는 DONE.json 을 마지막에 쓴다
        if (root / "meta.json").is_file():
            meta = json.loads((root / "meta.json").read_text(encoding="utf-8"))
            counts = meta.get("counts")
            if not isinstance(counts, dict) or not counts:
                return False
            if (root / "dataset.json").is_file() and json.loads((root / "dataset.json").read_text(encoding="utf-8")).get("counts") != counts:
                return False
            if (root / "pages.jsonl").is_file() and not (root / "DONE.json").is_file():
                return False
            for task, count in counts.items():
                # 작업 파일 이름은 과제 ID여야 한다. 다른 경로를 읽지 않는다.
                if not isinstance(task, str) or Path(task).name != task or not isinstance(count, int) or count < 0:
                    return False
                with (root / "tasks" / f"{task}.jsonl").open(encoding="utf-8") as f:
                    if sum(1 for line in f if line.strip()) != count:
                        return False
            return bool(meta.get("version"))
        return False
    except (OSError, ValueError, TypeError):
        return False


def recover_completed(jobs, registry) -> None:
    with _LOCK:
        for job in jobs.list():
            if job.get("kind") not in BUILD_KINDS or (job.get("result") or {}).get("dataset"):
                continue
            # 실제 생성 실패나 사용자가 취소한 작업을 완료로 바꾸지 않는다.
            if job.get("status") not in ("interrupted", "done") and not (job.get("status") == "failed" and job.get("code") == 0):
                continue
            spec = _spec(job)
            if not spec or not _complete(registry, job, spec):
                continue
            try:
                result = register_output(registry, spec)
            except (OSError, ValueError) as e:
                message = f"자동 등록 실패: {e}"
                if job.get("error") != message:
                    job.update(status="failed", code=0, stage="registration_failed", error=message)
                    jobs._save(job)
                continue
            job.update(status="done", stage="registered", result=result, recovered=True,
                       recovered_at=time.strftime("%Y-%m-%d %H:%M:%S"))
            job.setdefault("ended", job["recovered_at"])
            job.pop("error", None)
            jobs._save(job)


STALE_MINUTES = 15   # pid 를 모르는 예전 작업: 로그가 이만큼 멈춰 있으면 끝난 것으로 본다


def _pid_running(pid) -> bool:
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    try:   # 끝났지만 거두지 않은 프로세스(좀비)는 끝난 것
        return Path(f"/proc/{pid}/stat").read_text().split(") ", 1)[1][:1] != "Z"
    except (OSError, IndexError):
        return True


def _still_running(jobs, job: dict) -> bool:
    if job.get("pid"):
        return _pid_running(job["pid"])
    log = jobs.root / job["id"] / "log.txt"
    try:
        return time.time() - log.stat().st_mtime < STALE_MINUTES * 60
    except OSError:
        return False


def settle_interrupted(jobs, registry) -> int:
    """끊긴 생성 작업 정리: 완료 파일이 다 있으면 등록, 프로세스가 끝났는데 없으면 실패로. 남은 끊긴 작업 수를 돌려준다."""
    if not any(j.get("status") == "interrupted" and j.get("kind") in BUILD_KINDS for j in jobs.list()):
        return 0
    recover_completed(jobs, registry)
    left = 0
    with _LOCK:
        for job in jobs.list():
            if job.get("kind") not in BUILD_KINDS or job.get("status") != "interrupted":
                continue
            if _still_running(jobs, job):
                left += 1
                continue
            job.update(status="failed", stage="interrupted_incomplete", ended=job.get("ended") or time.strftime("%Y-%m-%d %H:%M:%S"),
                       error="studio 가 다시 뜬 사이 생성이 멈췄고 완료 파일이 없습니다. 로그 끝을 보고, 새 이름으로 다시 만드세요")
            jobs._save(job)
    return left


def _removable(jobs, registry, job: dict) -> bool:
    """기록을 지워도 되는 작업: 돌고 있지 않고, 실패·취소했거나, 끝났지만 등록한 데이터셋이 없어졌거나(등록 해제·폴더 삭제)."""
    if job.get("status") == "running" or job["id"] in jobs.live:
        return False
    if job.get("status") == "interrupted":
        return not _still_running(jobs, job)
    if job.get("status") in ("failed", "cancelled"):
        return True
    ds_id = (job.get("result") or {}).get("dataset")
    ds = registry.load()["datasets"].get(ds_id) if ds_id else None
    return ds is None or not Path(ds["path"]).exists()


def forget_job(jobs, registry, job_id: str) -> None:
    """작업 기록 하나 지우기 (jobs/<ID>/ 의 job.json·log.txt). 만든 데이터셋 폴더는 건드리지 않는다."""
    job = jobs.get(job_id)
    if not _removable(jobs, registry, job):
        raise ValueError("돌고 있거나, 만든 데이터셋이 아직 등록돼 있는 작업입니다 (데이터셋을 먼저 등록 해제하세요)")
    jobs.remove(job_id)


def cleanup_jobs(jobs, registry) -> list[str]:
    """지워도 되는 생성 작업 기록을 모두 지운다 (실패·취소·멈춘 작업, 데이터셋이 없어진 작업). 지운 작업 ID 목록."""
    gone = []
    for job in jobs.list():
        if job.get("kind") in BUILD_KINDS and _removable(jobs, registry, job):
            jobs.remove(job["id"])
            gone.append(job["id"])
    return gone


def list_builds(jobs) -> list[dict]:
    """생성 작업 목록. 읽기만 한다 (복구는 띄울 때 recover_completed 가 한 번)."""
    return [job for job in jobs.list() if job.get("kind") in BUILD_KINDS]
