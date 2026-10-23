"""실험 묶음 (train/sweep.py): 모델을 차례로, 실패해도 다음으로, 다시 치면 이어서, 끝날 때마다 비교표. 파이프라인은 흉내 낸다."""
import contextlib
import io
import json

import pytest

from docgen.bench.ocr_data import read_json, write_json, write_jsonl
from docgen.bench.runner import oracle_output
from train import sweep as S
from train.score import score
from train.tests.test_train import _item

ITEMS = [_item("cross_check", f"b{i}") for i in range(6)] + [_item("kie", f"k{i}") for i in range(4)]


def fake_pipeline(good, fail=(), src="/src", start=2):
    """설정을 받아 파이프라인이 남기는 것(섞은 폴더·state·보고서)을 흉내 낸다. good[label] = 맞히는 문항 수, src = 원본 그림 폴더."""
    calls = []

    def report(wd, role, n, label):
        res = score(ITEMS, {it["id"]: oracle_output(it) if i < n else "x" for i, it in enumerate(ITEMS)})
        write_json(wd / "reports" / f"{role}.json", {"label": role, "role": role.split("-")[0],
                                                     "inference": {"images_sha256": label, "temperature": 0}, **res})

    def runner(config, log_path, part, smoke, only=None):
        cfg = read_json(config)
        wd, data = config.parent, config.parent / "data"
        label = wd.name
        calls.append((label, cfg, part, only))
        log_path.write_text("log\n", encoding="utf-8")
        if only == "eval_base":
            report(wd, "start", start, label)
            return 0
        if label in fail:
            return 1
        write_json(data / "DONE.json", {"image_max_size": [2300, 1600], "pixels_per_token_side": 32, "max_image_tokens_per_sample": 12000})
        write_jsonl(data / "benchmark_tasks.jsonl", [{"id": it["id"], "images": [f"{data}/{it['id']}.png"],
                                                      "source_images": [f"{src}/{it['id']}.png"]} for it in ITEMS])
        if not cfg["eval"]["skip_start"]:
            report(wd, "start", start, label)
        report(wd, "sft", good[label], label)
        done = ["prepare", "eval_base", "sft", "eval_sft", "report"]
        if part == "all":
            report(wd, "grpo-x", min(len(ITEMS), good[label] + 1), label)
            done += ["select", "grpo", "eval_grpo"]
        write_json(wd / "state.json", {"done": done})
        return 0
    return runner, calls


@pytest.fixture
def sweep_file(tmp_path):
    write_json(tmp_path / "base.json", {"workdir": "x", "model": "/m", "sft": {"config": "sft.yaml"},
                                        "data": {"train": [], "benchmark": [{"id": "syn", "name": "합성", "paths": ["bench"]}],
                                                 "output_dir": "x"}})
    sw = {"name": "E09-test", "about": "실서류 OCR 을 더하면 오르나", "record": "experiments/E09-test.md",
          "base": "base.json", "root": "runs/E09", "part": "sft",
          "runs": [{"label": "a1-syn", "about": "기준: 합성만", "train": ["syn-train"]},
                   {"label": "a2-real", "about": "기준 + 실서류 OCR", "train": ["syn-train", {"path": "real", "count": 10}]},
                   {"label": "a3-more", "about": "비교2", "train": ["syn-train", "real", "tgt"]}]}
    write_json(tmp_path / "e09.sweep.json", sw)
    return tmp_path / "e09.sweep.json"


def test_sweep_runs_in_order_survives_failure_resumes_and_compares(sweep_file, tmp_path):
    runner, calls = fake_pipeline({"a1-syn": 4, "a2-real": 8, "a3-more": 10}, fail={"a2-real"})
    with contextlib.redirect_stdout(io.StringIO()):
        S.run(sweep_file, runner=runner)
    root = tmp_path / "runs" / "E09"
    assert [c[0] for c in calls] == ["a1-syn", "a2-real", "a3-more"]   # 둘째가 실패해도 셋째까지
    first, second = calls[0][1], calls[1][1]
    assert first["eval"]["skip_start"] is False and second["eval"]["skip_start"] is True   # 출발 모델 평가는 한 번
    assert first["workdir"] == str(root / "a1-syn") and first["data"]["output_dir"] == str(root / "a1-syn" / "data")
    assert first["data"]["train"] == [str(tmp_path / "syn-train")]
    assert second["data"]["train"][1] == {"path": str(tmp_path / "real"), "count": 10}
    assert first["data"]["benchmark"][0]["paths"] == [str(tmp_path / "bench")]   # base 기준 상대 경로
    status = read_json(root / "sweep.json")
    assert [status[k]["status"] for k in ("a1-syn", "a2-real", "a3-more")] == ["done", "failed", "done"]
    md = (root / "compare.md").read_text(encoding="utf-8")
    assert md.startswith("# E09-test\n\n실서류 OCR 을 더하면 오르나") and "| a2-real | 기준 + 실서류 OCR | syn-train<br>real (count 10) |" in md
    table = md.split("# 벤치마크 비교")[1].split("## ")[0]
    assert "| 출발 모델 |" in table and "| a1-syn |" in table and "| a3-more |" in table and "| a2-real |" not in table
    assert "실서류 OCR 을 더하면 오르나" in (root / "compare.html").read_text(encoding="utf-8")
    assert read_json(root / "sweep.config.json")["about"] == "실서류 OCR 을 더하면 오르나"
    # 다시 치면 실패한 것만 (끝난 모델은 건너뜀)
    runner2, calls2 = fake_pipeline({"a1-syn": 4, "a2-real": 8, "a3-more": 10})
    with contextlib.redirect_stdout(io.StringIO()):
        S.run(sweep_file, runner=runner2)
    assert [c[0] for c in calls2] == ["a2-real"]
    assert "| a2-real |" in (root / "compare.md").read_text(encoding="utf-8").split("# 벤치마크 비교")[1].split("## ")[0]
    with contextlib.redirect_stdout(io.StringIO()) as out:
        S.show_status(S.load(sweep_file))
    assert "E09-test: 실서류 OCR 을 더하면 오르나" in out.getvalue() and "기준 + 실서류 OCR" in out.getvalue()


def test_sweep_refuses_changed_settings_and_missing_about(sweep_file, tmp_path):
    runner, _ = fake_pipeline({"a1-syn": 4, "a2-real": 8, "a3-more": 10})
    with contextlib.redirect_stdout(io.StringIO()):
        S.run(sweep_file, runner=runner)
    sw = read_json(sweep_file)
    sw["runs"][0]["train"] = ["other"]   # 이미 돈 모델의 데이터를 바꿈 → 돌리지 않음
    write_json(sweep_file, sw)
    runner2, calls2 = fake_pipeline({"a1-syn": 4, "a2-real": 8, "a3-more": 10})
    with contextlib.redirect_stdout(io.StringIO()):
        S.run(sweep_file, runner=runner2)
    assert calls2 == [] and "설정이 바뀜" in read_json(tmp_path / "runs" / "E09" / "sweep.json")["a1-syn"]["why"]
    del sw["runs"][1]["about"]
    write_json(sweep_file, sw)
    with pytest.raises(ValueError, match="about"):
        S.load(sweep_file)


def test_sweep_reuses_start_from_and_per_model_grpo(sweep_file, tmp_path):
    runner, _ = fake_pipeline({"a1-syn": 4, "a2-real": 8, "a3-more": 10})
    with contextlib.redirect_stdout(io.StringIO()):
        S.run(sweep_file, runner=runner)
    sw = read_json(sweep_file)
    e10 = {**sw, "name": "E10-next", "root": "runs/E10", "start_from": "runs/E09/a1-syn",
           "runs": [{"label": "b1", "about": "다른 데이터", "train": ["x"]},
                    {"label": "b2", "about": "GRPO 까지", "train": ["y"], "part": "all"}]}
    write_json(tmp_path / "e10.sweep.json", e10)
    runner2, calls = fake_pipeline({"b1": 6, "b2": 7})
    with contextlib.redirect_stdout(io.StringIO()):
        S.run(tmp_path / "e10.sweep.json", runner=runner2)
    assert [(c[0], c[1]["eval"]["skip_start"], c[2]) for c in calls] == [("b1", True, "sft"), ("b2", True, "all")]   # 출발 모델 평가 없음
    table = (tmp_path / "runs" / "E10" / "compare.md").read_text(encoding="utf-8").split("# 벤치마크 비교")[1].split("## ")[0]
    assert "| 출발 모델 (E09/a1-syn) |" in table and "| b2 GRPO |" in table
    # 평가 문항이 다른 묶음: start_from 을 쓰지 않고 첫 모델에서 출발 모델을 평가한다
    write_json(tmp_path / "e11.sweep.json", {**e10, "name": "E11", "root": "runs/E11", "runs": e10["runs"][:1]})
    runner3, calls3 = fake_pipeline({"b1": 6}, src="/other")
    with contextlib.redirect_stdout(io.StringIO()):
        S.run(tmp_path / "e11.sweep.json", runner=runner3)
    assert [(c[0], c[3]) for c in calls3] == [("b1", None), ("b1", "eval_base")]
    table = (tmp_path / "runs" / "E11" / "compare.md").read_text(encoding="utf-8").split("# 벤치마크 비교")[1].split("## ")[0]
    assert "| 출발 모델 |" in table and "E09" not in table
    # sft 로 끝난 모델을 all 로 바꾸면 그 모델만 다시 (GRPO)
    e10["runs"][0]["part"] = "all"
    write_json(tmp_path / "e10.sweep.json", e10)
    runner4, calls4 = fake_pipeline({"b1": 6, "b2": 7})
    with contextlib.redirect_stdout(io.StringIO()):
        S.run(tmp_path / "e10.sweep.json", runner=runner4)
    assert [(c[0], c[2]) for c in calls4] == [("b1", "all")]
