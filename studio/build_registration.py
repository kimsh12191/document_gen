"""완성한 데이터셋 자동 등록. 재시작으로 놓친 완료 처리도 작업 기록과 완료 파일로 복구한다."""
from __future__ import annotations

import json
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
        meta["recipe"] = f"datasets/recipes/{Path(info['recipe']).name}.json"
    return {"path": str(out if bank else out / "prepared"), "name": out.name, "meta": meta}


def _complete(registry, job: dict, spec: dict) -> bool:
    root = Path(spec["path"]).resolve()
    if not root.is_relative_to((registry.ws / "datasets").resolve()):
        return False
    try:
        if job["kind"] == "build_bank":
            manifest = json.loads((root / "dataset.json").read_text(encoding="utf-8"))
            meta = json.loads((root / "meta.json").read_text(encoding="utf-8"))
            counts = meta.get("counts")
            if not isinstance(counts, dict) or not counts or manifest.get("counts") != counts:
                return False
            for task, count in counts.items():
                # 작업 파일 이름은 과제 ID여야 한다. 다른 경로를 읽지 않는다.
                if not isinstance(task, str) or Path(task).name != task or not isinstance(count, int) or count < 0:
                    return False
                with (root / "tasks" / f"{task}.jsonl").open(encoding="utf-8") as f:
                    if sum(1 for line in f if line.strip()) != count:
                        return False
            return bool(meta.get("version"))
        # 1부 prepare는 모든 파일을 저장한 뒤 DONE.json을 마지막으로 쓴다.
        done = json.loads((root / "DONE.json").read_text(encoding="utf-8-sig"))
        return isinstance(done, dict) and (root / "pages.jsonl").is_file()
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


def list_builds(jobs, registry) -> list[dict]:
    recover_completed(jobs, registry)
    return [job for job in jobs.list() if job.get("kind") in BUILD_KINDS]
