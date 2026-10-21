"""⑥ 자동 등록 시험 (studio/build_registration.py): 완료 파일이 다 있을 때만 한 번 등록, 재시작 뒤 복구, 작업 공간 밖 폴더 거부."""
import json
import sys
import threading
import time
from pathlib import Path

import pytest

from studio import bank_data as BD, ocr_data as OCR
from studio.build_registration import recover_completed, register_output
from studio.datasets import Registry
from studio.jobs import Jobs


def bank_output(root, n=1):
    (root / "tasks").mkdir(parents=True, exist_ok=True)
    (root / "tasks" / "classify.jsonl").write_text('{"id":"one","answer":"서류"}\n' * n, encoding="utf-8")
    meta = {"version": "2.0", "counts": {"classify": n}, "split": "test"}
    (root / "meta.json").write_text(json.dumps(meta), encoding="utf-8")
    (root / "dataset.json").write_text(json.dumps({**meta, "recipe": {"about": "생성 당시 설명"}}), encoding="utf-8")


def ocr_output(root, studio=None, done=True):
    """OCR 준비 결과 (과제 형식 tasks/ + meta.json, 쪽 정보, DONE.json 은 마지막)."""
    (root / "tasks").mkdir(parents=True, exist_ok=True)
    (root / "pages.jsonl").write_text("")
    (root / "tasks" / "crop_ocr.jsonl").write_text('{"id":"v0_crop_ocr_0","task":"crop_ocr","answer":{"text":"가"},"meta":{"split":"benchmark"}}\n')
    (root / "meta.json").write_text(json.dumps({"format": "docgen-tasks/1", "kind": "ocr", "version": "ocr:synthetic-test", "split": "test",
                                                "counts": {"crop_ocr": 1}, "studio": studio or {}}), encoding="utf-8")
    if done:
        (root / "DONE.json").write_text('{"ocr_revision":"synthetic-test"}')


def job_record(jobs, output, **kw):
    job = {"id": "build-test", "kind": "build_bank", "status": "interrupted", "started": "2026-10-20 12:00:00",
           "info": {"out": str(output), "recipe": "bank-test"}, **kw}
    jobs._save(job)
    return job


def test_completed_legacy_build_recovers_and_registers_once(tmp_path):
    reg = Registry(tmp_path)
    jobs = Jobs(tmp_path, tmp_path)
    out = tmp_path / "datasets" / "finished"
    bank_output(out)
    job_record(jobs, out)
    recover_completed(jobs, reg)
    recover_completed(jobs, reg)
    assert len(reg.load()["datasets"]) == 1
    dataset = reg.get("finished")
    assert dataset["registered"] is False and dataset["gt"] == "exact"
    assert dataset["card"]["purpose"] == "생성 당시 설명"
    job = jobs.get("build-test")
    assert job["status"] == "done" and job["stage"] == "registered"
    assert job["recovered"] and job["result"] == {"dataset": "finished"}


@pytest.mark.parametrize("state", ["running", "cancelled", "failed"])
def test_unfinished_or_unsuccessful_process_is_not_auto_registered(tmp_path, state):
    reg, jobs = Registry(tmp_path), Jobs(tmp_path, tmp_path)
    out = tmp_path / "datasets" / "unfinished"
    bank_output(out)
    job_record(jobs, out, status=state, code=1 if state == "failed" else None)
    recover_completed(jobs, reg)
    assert reg.load()["datasets"] == {}


def test_partial_files_are_not_treated_as_completed(tmp_path):
    reg, jobs = Registry(tmp_path), Jobs(tmp_path, tmp_path)
    out = tmp_path / "datasets" / "partial"
    bank_output(out)
    manifest = out / "dataset.json"
    snapshot = manifest.read_text()
    manifest.unlink()
    job_record(jobs, out)
    recover_completed(jobs, reg)
    assert reg.load()["datasets"] == {}
    manifest.write_text(snapshot)
    (out / "tasks" / "classify.jsonl").write_text("")
    recover_completed(jobs, reg)
    assert reg.load()["datasets"] == {}


def test_recovery_does_not_register_outputs_outside_workspace(tmp_path):
    reg, jobs = Registry(tmp_path / "ws"), Jobs(tmp_path / "ws", tmp_path)
    out = tmp_path / "outside-workspace"
    bank_output(out)
    job_record(jobs, out)
    recover_completed(jobs, reg)
    assert reg.load()["datasets"] == {}


def test_ocr_only_registers_after_prepare_done_and_keeps_provenance(tmp_path):
    reg, jobs = Registry(tmp_path), Jobs(tmp_path, tmp_path)
    root = tmp_path / "datasets" / "ocr" / "prepared"
    ocr_output(root, {"source": "synthetic", "gt": "exact", "real_data": False}, done=False)
    spec = {"path": str(root), "name": "ocr-finished", "meta": {"dataset_json": "../ocr_set.json"}}
    job_record(jobs, root, kind="build_ocr", info={"dataset": spec})
    recover_completed(jobs, reg)
    assert reg.load()["datasets"] == {}
    (root / "DONE.json").write_text('{"ocr_revision":"synthetic-test"}')
    recover_completed(jobs, reg)
    assert reg.get("ocr-finished")["source"] == "synthetic"
    assert reg.get("ocr-finished")["gt"] == "exact"


def test_callback_failure_can_recover_without_duplicate_or_overwriting_frozen_entry(tmp_path):
    reg, jobs = Registry(tmp_path), Jobs(tmp_path, tmp_path)
    out = tmp_path / "datasets" / "finished"
    bank_output(out)
    old = reg.register(str(out), "kept", frozen=True)
    job_record(jobs, out, status="failed", code=0, error="후처리 실패")
    recover_completed(jobs, reg)
    assert jobs.get("build-test")["result"] == {"dataset": old["id"]}
    assert reg.get(old["id"])["frozen"] is True
    assert len(reg.load()["datasets"]) == 1


def test_job_finishes_only_after_registration_callback(tmp_path):
    reg, jobs = Registry(tmp_path), Jobs(tmp_path, tmp_path)
    out = tmp_path / "datasets" / "job-output"
    bank_output(out)
    spec = {"path": str(out), "name": "job-output", "meta": {}}
    entered, release = threading.Event(), threading.Event()

    def done(job):
        entered.set()
        release.wait(5)
        return register_output(reg, spec)

    job = jobs.start("build_bank", "시험", [sys.executable, "-c", "print('complete')"], done, {"dataset": spec})
    try:
        assert entered.wait(5)
        pending = jobs.get(job["id"])
        assert pending["status"] == "running" and pending["stage"] == "registering"
        assert reg.load()["datasets"] == {}
    finally:
        release.set()
    deadline = time.monotonic() + 30   # 바쁜 PC 에서는 하위 프로세스가 늦게 끝난다
    while time.monotonic() < deadline:
        if jobs.get(job["id"])["status"] == "done":
            break
        time.sleep(0.02)
    assert jobs.get(job["id"])["result"] == {"dataset": "job-output"}


@pytest.mark.parametrize("track", ["bank", "ocr"])
def test_new_builds_persist_auto_registration_spec(tmp_path, monkeypatch, track):
    class Capture:
        def start(self, kind, title, cmd, on_done, info):
            self.done, self.info = on_done, info
            return {"id": "captured", "kind": kind}

    recipes = tmp_path / "recipes"
    recipes.mkdir()
    (recipes / "test.json").write_text(json.dumps({"track": track, "types": ["resident_id_card"], "split": "test" if track == "bank" else "benchmark"}))
    monkeypatch.setattr(BD, "ROOT", tmp_path)
    monkeypatch.setattr(BD, "RECIPES", recipes)
    monkeypatch.setattr(OCR, "ROOT", tmp_path)
    reg, jobs = Registry(tmp_path / "ws"), Capture()
    if track == "bank":
        BD.start_build(jobs, reg, "test", "output", 1)
    else:
        OCR.start_build(jobs, reg, recipes, "test", "output", 1)
    spec = jobs.info["dataset"]
    assert Path(spec["path"]).is_relative_to(reg.ws / "datasets")
    assert spec["name"] == "output"
    if track == "bank":
        bank_output(Path(spec["path"]))
    else:
        ocr_output(Path(spec["path"]))
    assert jobs.done({}) == {"dataset": "output"}
