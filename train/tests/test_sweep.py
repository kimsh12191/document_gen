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
    for d in ("syn-train", "real", "tgt", "x", "y", "other", "bench"):   # 데이터셋 폴더 꼴 (돌리기 전 검사가 본다)
        write_json(tmp_path / d / "meta.json", {})
        (tmp_path / d / "tasks").mkdir()
    write_json(tmp_path / "model" / "config.json", {})
    write_json(tmp_path / "base.json", {"workdir": "x", "model": str(tmp_path / "model"), "sft": {"config": "sft.yaml"},
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
    glance = md.split("## 한눈에 보기")[1].split("# 벤치마크 비교")[0]   # 맨 위 요약: 기준(a1) 대비 %p
    assert "| 출발 모델 | a1-syn | a3-more |" in glance and "| cross_check | score | 6 | 33.3 | 66.7 | 100.0 (+33.3) |" in glance
    assert "한눈에 보기" in (root / "compare.html").read_text(encoding="utf-8")
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


def test_sweep_checks_every_model_before_starting(sweep_file, tmp_path):
    base = read_json(tmp_path / "base.json")
    base["data"]["benchmark"] = [{"id": "ocr_synthetic_v1 (261023 전체)", "name": "합성 OCR", "paths": ["bench"]},
                                 {"id": "real", "name": "실서류", "format": "swift-fields", "paths": ["no.jsonl"]}]
    write_json(tmp_path / "base.json", base)
    sw = read_json(sweep_file)
    sw["runs"][2]["train"] = ["syn-train", "nowhere"]
    write_json(sweep_file, sw)
    runner, calls = fake_pipeline({"a1-syn": 4, "a2-real": 8, "a3-more": 10})
    with pytest.raises(SystemExit) as e:
        S.run(sweep_file, runner=runner)
    msg = str(e.value)
    assert calls == [] and "아무 모델도 시작하지 않았습니다" in msg
    assert "ocr_synthetic_v1 (261023 전체)" in msg and "a3-more: train 경로" in msg
    assert msg.count("benchmark.id") == 1   # 공통 설정 문제는 한 번만
    base["data"]["benchmark"] = [{"id": "syn", "name": "합성", "paths": ["bench"]},
                                 {"id": "real", "name": "실서류", "format": "swift-fields", "paths": ["no.jsonl"]}]
    write_json(tmp_path / "base.json", base)
    with pytest.raises(SystemExit, match="real: 경로가 없습니다"):
        S.run(sweep_file, runner=runner)


def test_overview_per_benchmark_id():
    """평가 세트를 id 로 나눈 보고서: 세트·과제마다 한 줄, 기준 모델 대비 %p, 낮을수록 좋은 지표 표시."""
    def rep(label, kie, cer):
        return {"label": label, "benchmarks": {
            "real-fx-po": {"name": "매입추심", "tasks": {"kie": {"main": "f1", "n": 50, "metrics": {"f1": kie}}}},
            "ocr_real": {"name": "검사부", "tasks": {"ocr_page": {"main": "cer", "n": 9, "metrics": {"cer": cer}}}}}}
    sw = {"runs": [{"label": "a1-syn"}, {"label": "a2"}]}
    base, rows = S._overview(sw, [rep("출발 모델", 0.1, 0.5), rep("a1-syn", 0.4, 0.3), rep("a2", 0.5, 0.2)])
    assert base == "a1-syn"
    kie, ocr = rows
    assert kie[:4] == ("real-fx-po", "kie", "f1", 50) and [round(d, 1) if d is not None else d for _, d in kie[5]] == [None, None, 10.0]
    assert ocr[2] == "cer ↓" and ocr[4] is True and round(ocr[5][2][1], 1) == -10.0


def test_summary_across_experiments(sweep_file, tmp_path):
    """실험 여러 개를 html 하나로: 묶음 파일·결과 폴더 둘 다 받고, 평가 문항이 다른 실험 칸은 † 로."""
    from train import summary as M

    runner, _ = fake_pipeline({"a1-syn": 4, "a2-real": 8, "a3-more": 10})
    with contextlib.redirect_stdout(io.StringIO()):
        S.run(sweep_file, runner=runner)
    exps = M.gather([sweep_file, tmp_path / "runs" / "E09"])   # 같은 실험을 두 번 (파일·폴더)
    assert [len(r) for _, r, _ in exps] == [4, 4]   # 출발 모델(첫 모델에서 평가) + 모델 3
    rows = M.table(exps)
    assert {r[2] for r in rows} == {"cross_check", "kie"}
    cells = rows[0][6]
    assert len(cells) == 8 and cells[1][1] is None and cells[2][1] is not None and all(same for *_, same in cells)

    def rep(label, sha, v):
        return {"label": label, "benchmarks": {"syn": {"name": "합성", "items_sha256": sha, "tasks": {"kie": {"main": "f1", "n": 4, "metrics": {"f1": v}}}}}}
    a = ({"name": "A", "runs": [{"label": "a1"}]}, [rep("a1", "h1", 0.5)], [])
    b = ({"name": "B", "runs": [{"label": "b1"}]}, [rep("b1", "h1", 0.6)], [])
    c = ({"name": "C", "runs": [{"label": "c1"}]}, [rep("c1", "h2", 0.9)], [])
    (row,) = M.table([a, b, c])
    assert [same for *_, same in row[6]] == [True, True, False]   # 다수(h1)가 기준

    out = M.render(exps, tmp_path / "summary.html").read_text(encoding="utf-8")
    assert "E09-test" in out and "compare.html" in out and "한눈에 보기" in out and "a3-more" in out


def test_summary_reads_eval_only_workdir(tmp_path):
    """평가만 다시 한 workdir (guide/eval.md): compare_models 가 먼저, 기준은 출발 모델이 아닌 첫 줄."""
    from train import summary as M

    wd = tmp_path / "E01-reeval"
    for name, label, role, n in (("cmp-compare0", "a1-syn SFT", "other", 4), ("cmp-compare1", "a2 SFT", "other", 8),
                                 ("start", "출발 모델", "start", 2)):
        write_json(wd / "reports" / f"{name}.json", {"label": label, "role": role, "model": f"/m/{name}",
                                                       **score(ITEMS, {it["id"]: oracle_output(it) if i < n else "x" for i, it in enumerate(ITEMS)})})
    ((sw, reports, _),) = M.gather([wd])
    assert [r["label"] for r in reports] == ["a1-syn SFT", "a2 SFT", "출발 모델"] and sw["runs"][0]["label"] == "a1-syn SFT"
    cells = M.table([(sw, reports, [])])[0][6]
    assert cells[0][1] is None and cells[1][1] is not None and cells[2][1] is None
    assert "reports/benchmark.html" not in M.render([(sw, reports, [])], tmp_path / "s.html").read_text(encoding="utf-8")   # 표가 아직 없으면 링크 없음
    with pytest.raises(SystemExit):
        M.load(tmp_path)
