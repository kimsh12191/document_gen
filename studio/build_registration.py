"""⑥ 데이터셋 › 생성 현황: 완성한 데이터셋 자동 등록 (DESIGN.md 9.1.1). 재시작으로 놓친 완료 처리도 작업 기록과 완료 파일로 복구한다.

- 생성 작업(build_bank·build_ocr: 은행 업무 레시피, 합성 OCR 레시피, ④ 라벨 있는 데이터)은 job.json 의 info.dataset 에
  등록할 {path, name, meta} 를 남기고, 끝나면 register_output 으로 등록부(studio/datasets.py)에 올린다.
- recover_completed 는 GET /api/datasets · GET /api/builds 때 돈다: 끊긴(interrupted) 작업이라도 완료 파일이 다 있으면 등록한다.
  은행 업무는 dataset.json·meta.json 과 tasks/<과제>.jsonl 문항 수, OCR 은 prepared/DONE.json·pages.jsonl 로 완료를 판단한다.
- <workspace_dir>/datasets/ 밖의 폴더, 실패·취소한 작업은 등록하지 않는다. 같은 폴더는 한 번만 등록한다.
"""
from __future__ import annotations

import json
import threading
import time
from pathlib import Path

BUILD_KINDS = {"build_bank", "build_ocr", "build_tasks"}   # build_tasks: 라벨 있는 데이터 (업무 + 쪽 OCR 을 한 폴더로)
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


def list_builds(jobs, registry) -> list[dict]:
    recover_completed(jobs, registry)
    return [job for job in jobs.list() if job.get("kind") in BUILD_KINDS]
