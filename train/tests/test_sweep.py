"""실험 묶음 (train/sweep.py): 모델을 차례로, 실패해도 다음으로, 다시 치면 이어서, 끝날 때마다 비교표. 파이프라인은 흉내 낸다."""
import contextlib
import io
import json
import sys
import threading
import time

import pytest

from docgen.bench.ocr_data import read_json, write_json, write_jsonl
from docgen.bench.runner import oracle_output
from train import sweep as S
from train.score import score
from train.tests.test_train import _item

ITEMS = [_item("cross_check", f"b{i}") for i in range(6)] + [_item("kie", f"k{i}") for i in range(4)]


def fake_pipeline(good, fail=(), src="/src", start=2, delay=0):
    """설정을 받아 파이프라인이 남기는 것(섞은 폴더·state·보고서·답 파일)을 흉내 낸다.
    good[label] = 맞히는 문항 수, src = 원본 그림 폴더, delay = 모델마다 걸리는 초 (동시 실행 확인)."""
    calls, live = [], {"now": 0, "max": 0}
    lock = threading.Lock()

    def report(wd, role, n, label):
        preds = {it["id"]: oracle_output(it) if i < n else "x" for i, it in enumerate(ITEMS)}
        path = wd / "predictions" / f"{role}.jsonl"
        write_jsonl(path, [{"id": k, "prediction": v} for k, v in preds.items()])
        write_json(wd / "reports" / f"{role}.json", {"label": role, "role": role.split("-")[0], "predictions": str(path),
                                                     "inference": {"images_sha256": label, "temperature": 0}, **score(ITEMS, preds)})

    def runner(config, log_path, part, smoke, only=None, sft_checkpoint=None, env=None):
        cfg = read_json(config)
        wd, data = config.parent, config.parent / "data"
        label = wd.name
        with lock:
            calls.append((label, cfg, part, only, sft_checkpoint, env))
            live["now"] += 1
            live["max"] = max(live["max"], live["now"])
        try:
            time.sleep(delay)
            log_path.write_text("log\n", encoding="utf-8")
            if only == "eval_base":
                report(wd, "start", start, label)
                return 0
            if label in fail:
                return 1
            d = cfg["data"]
            size = d.get("image_max_size", [2300, 1600])
            write_json(data / "DONE.json", {"image_max_size": size, "benchmark_image_max_size": d.get("benchmark_image_max_size") or size,
                                            "pixels_per_token_side": 28 if "vl" in cfg["model"] else 32,
                                            "max_image_tokens_per_sample": 12000})
            write_jsonl(data / "benchmark_tasks.jsonl", [{"id": it["id"], "images": [f"{data}/{it['id']}.png"],
                                                          "messages": [{"role": "user", "content": "<image>" + it["prompt"]}],
                                                          "source_images": [f"{src}/{it['id']}.png"]} for it in ITEMS])
            write_jsonl(data / "benchmark_items.jsonl", ITEMS)
            if not cfg["eval"]["skip_start"]:
                report(wd, "start", start, label)
            report(wd, "sft", good[label], label)
            done = ["prepare", "eval_base", "sft", "eval_sft", "report"]
            if part in ("all", "grpo"):
                report(wd, "grpo-x", min(len(ITEMS), good[label] + 1), label)
                done += ["select", "grpo", "eval_grpo"]
            write_json(wd / "state.json", {"done": done, "sft_checkpoint": str(sft_checkpoint or wd / "sft" / "checkpoint-5")})
            return 0
        finally:
            with lock:
                live["now"] -= 1
    runner.live = live
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
    assert md.startswith("# E09-test\n\n실서류 OCR 을 더하면 오르나") and "| a2-real | 기준 + 실서류 OCR |  | syn-train<br>real (count 10) |" in md
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


def test_sweep_compares_named_benchmarks_across_mixed_folders(sweep_file, tmp_path, monkeypatch):
    """평가 세트가 여럿(id)이어도 비교표가 만들어진다: 모델마다 섞은 폴더가 달라 그림 경로(images_sha256)가 달라도
    원본 그림이 같으면 세트별 표까지 비교한다 (예전: 'Reports use different inference images_sha256' 로 비교표 실패)."""
    named = [{**it, "meta": {**it["meta"], "benchmark_id": "syn" if i % 2 else "real", "benchmark_name": "합성" if i % 2 else "실서류",
                             "benchmark_group": "g"}} for i, it in enumerate(ITEMS)]
    monkeypatch.setattr(sys.modules[__name__], "ITEMS", named)
    runner, _ = fake_pipeline({"a1-syn": 4, "a2-real": 8, "a3-more": 10})
    with contextlib.redirect_stdout(io.StringIO()):
        S.run(sweep_file, runner=runner)
    root = tmp_path / "runs" / "E09"
    assert "비교표를 만들지 못함" not in (root / "compare_notes.txt").read_text(encoding="utf-8")
    md = (root / "compare.md").read_text(encoding="utf-8")
    assert all(f"| {m} |" in md for m in ("a1-syn", "a2-real", "a3-more"))
    assert (root / "benchmarks" / "syn" / "compare.md").exists() and (root / "benchmarks" / "real" / "compare.md").exists()
    (root / "compare.md").unlink()   # 학습 없이 비교표만 다시: S.compare(S.load(<묶음 파일>)) (guide/training.md)
    with contextlib.redirect_stdout(io.StringIO()):
        assert S.compare(S.load(sweep_file))["models"][-3:] == ["a1-syn", "a2-real", "a3-more"]
    assert (root / "compare.md").exists() and (root / "summary.html").exists()


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
    assert "a3-more" in (tmp_path / "runs" / "E09" / "summary.html").read_text(encoding="utf-8")   # 묶음이 스스로 만든 한 화면
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
    # compare_models 가 없는 학습 실행은 출발 모델이 기준
    for f in ("cmp-compare0", "cmp-compare1"):
        (wd / "reports" / f"{f}.json").unlink()
    write_json(wd / "reports" / "sft.json", {"label": "SFT", "role": "sft", "model": "/m/sft",
                                            **score(ITEMS, {it["id"]: oracle_output(it) for it in ITEMS})})
    ((sw2, reports2, _),) = M.gather([wd])
    assert sw2["runs"][0]["label"] == "출발 모델" and [r["label"] for r in reports2] == ["출발 모델", "SFT"]
    cells2 = M.table([(sw2, reports2, [])])[0][6]
    assert cells2[0][1] is None and cells2[1][1] > 0
    cells = M.table([(sw, reports, [])])[0][6]
    assert cells[0][1] is None and cells[1][1] is not None and cells[2][1] is None
    assert "reports/benchmark.html" not in M.render([(sw, reports, [])], tmp_path / "s.html").read_text(encoding="utf-8")   # 표가 아직 없으면 링크 없음
    with pytest.raises(SystemExit):
        M.load(tmp_path)


def test_sweep_runs_change_any_training_setting_but_not_evaluation(sweep_file, tmp_path):
    """모델마다 학습 쪽 칸(출발 모델·데이터·SFT 옵션·GRPO)을 바꾸고, 적지 않은 칸은 base. 평가 칸은 못 바꾼다."""
    write_json(tmp_path / "vl" / "config.json", {})
    base = read_json(tmp_path / "base.json")
    base["data"]["train"] = ["syn-train"]
    write_json(tmp_path / "base.json", base)
    sw = read_json(sweep_file)
    sw["baseline"] = "a2-real"
    sw["runs"] = [{"label": "a1-syn", "about": "base 그대로"},
                  {"label": "a2-real", "about": "학습률·데이터", "train": ["real"],
                   "sft": {"learning_rate": 5e-5, "num_train_epochs": 2}, "data": {"task_mix": {"kie": 0.5}, "image_max_size": [1600, 1200]}},
                  {"label": "a3-vl", "about": "다른 출발 모델", "model": "vl", "model_type": "qwen3_vl", "part": "all",
                   "grpo": {"beta": 0.08, "count": 500}, "deploy": ["swift", "deploy", "--port", "{port}"]}]
    write_json(sweep_file, sw)
    runner, calls = fake_pipeline({"a1-syn": 4, "a2-real": 8, "a3-vl": 6})
    with contextlib.redirect_stdout(io.StringIO()):
        S.run(sweep_file, runner=runner)
    cfg = {c[0]: c[1] for c in calls}
    assert cfg["a1-syn"]["data"]["train"] == [str(tmp_path / "syn-train")]   # train 을 안 적으면 base (base 파일 기준 경로)
    assert cfg["a2-real"]["data"]["train"] == [str(tmp_path / "real")] and cfg["a2-real"]["data"]["task_mix"] == {"kie": 0.5}
    assert cfg["a2-real"]["sft"] == {"config": "sft.yaml", "learning_rate": 5e-5, "num_train_epochs": 2}
    assert cfg["a2-real"]["data"]["benchmark_image_max_size"] == [2300, 1600]   # 학습 그림을 바꿔도 평가 그림은 base 값
    assert "benchmark_image_max_size" not in cfg["a1-syn"]["data"]
    assert cfg["a3-vl"]["model"] == str(tmp_path / "vl") and cfg["a3-vl"]["model_type"] == "qwen3_vl"
    assert cfg["a3-vl"]["grpo"] == {"beta": 0.08, "count": 500} and cfg["a3-vl"]["eval"]["deploy_command"][1] == "deploy"
    # 출발 모델마다 한 번씩 평가
    assert [cfg[k]["eval"]["skip_start"] for k in ("a1-syn", "a2-real", "a3-vl")] == [False, True, False]
    root = tmp_path / "runs" / "E09"
    md = (root / "compare.md").read_text(encoding="utf-8")
    assert "| a2-real | 학습률·데이터 | data.image_max_size=[1600, 1200] · data.task_mix.kie=0.5 · sft.learning_rate=5e-05 · sft.num_train_epochs=2 | real |" in md
    assert "출발 모델 tmp_path" not in md and "| a1-syn | base 그대로 |  | <i>공통 (base)</i> |" in md
    table = md.split("# 벤치마크 비교")[1].split("## ")[0]
    assert f"| 출발 모델 ({tmp_path.name}/model) |" in table and f"| 출발 모델 ({tmp_path.name}/vl) |" in table and "| a3-vl GRPO |" in table
    glance = md.split("## 한눈에 보기")[1].split("# 벤치마크 비교")[0]
    assert "기준 모델 `a2-real`" in glance and "| 100.0 |" in glance   # baseline 이 기준
    assert "그림 조각 28px" in (root / "compare_notes.txt").read_text(encoding="utf-8")   # 다른 규격 모델도 표에 남음
    # 평가 칸은 모델마다 못 바꾼다 — 돌리기 전에 멈춘다
    sw["runs"][1]["set"] = {"data": {"benchmark": []}}
    sw["runs"][2]["data"] = {"output_dir": "x"}
    write_json(sweep_file, sw)
    with pytest.raises(SystemExit) as e:
        S.run(sweep_file, runner=runner)
    assert "a2-real: 설정을 만들지 못함 (a2-real: data.benchmark 는 모델마다 바꿀 수 없습니다" in str(e.value)
    assert "a3-vl: 설정을 만들지 못함 (a3-vl: data.output_dir" in str(e.value)
    sw["runs"][1] = {"label": "a2-real", "about": "x", "lr": 1}
    write_json(sweep_file, sw)
    with pytest.raises(ValueError, match="모르는 칸 \\['lr'\\]"):
        S.load(sweep_file)


def test_sweep_parallel_gpu_groups_and_from_sft(sweep_file, tmp_path):
    """gpu_groups: 비는 GPU 묶음에 다음 모델 (포트·MASTER_PORT 다르게). from_sft 는 부모 SFT 가 끝나면 그 체크포인트에서 GRPO 만."""
    sw = read_json(sweep_file)
    sw["gpu_groups"] = [[0, 1], [2, 3]]
    sw["runs"] = [{"label": "a1", "about": "기준", "train": ["syn-train"]},
                  {"label": "a2", "about": "데이터", "train": ["real"]},
                  {"label": "a3", "about": "a1 에서 GRPO", "from_sft": "a1", "grpo": {"beta": 0.08}},
                  {"label": "a4", "about": "GPU 지정", "train": ["tgt"], "gpus": [2]}]
    write_json(sweep_file, sw)
    runner, calls = fake_pipeline({"a1": 4, "a2": 8, "a3": 6, "a4": 5}, delay=0.3)
    with contextlib.redirect_stdout(io.StringIO()):
        S.run(sweep_file, runner=runner)
    assert runner.live["max"] == 2   # 두 묶음이 동시에
    by = {c[0]: c for c in calls}
    assert {tuple(by["a1"][1]["gpus"]), tuple(by["a2"][1]["gpus"])} == {(0, 1), (2, 3)}
    assert by["a1"][1]["eval"]["port_base"] != by["a2"][1]["eval"]["port_base"]
    assert by["a1"][5]["MASTER_PORT"] != by["a2"][5]["MASTER_PORT"]
    assert by["a4"][1]["gpus"] == [2]
    a3 = by["a3"]
    assert a3[2] == "grpo" and a3[4] == str(tmp_path / "runs" / "E09" / "a1" / "sft" / "checkpoint-5")   # 부모 체크포인트
    assert a3[1]["data"]["train"] == [str(tmp_path / "syn-train")] and a3[1]["grpo"]["beta"] == 0.08   # 부모 칸을 물려받음
    assert a3[1]["eval"]["skip_start"] is True
    assert [c[0] for c in calls].index("a3") > [c[0] for c in calls].index("a1")
    root = tmp_path / "runs" / "E09"
    assert {v["status"] for v in read_json(root / "sweep.json").values()} == {"done"}
    table = (root / "compare.md").read_text(encoding="utf-8").split("# 벤치마크 비교")[1].split("## ")[0]
    assert "| a3 |" in table and "| a3 GRPO |" not in table   # from_sft 는 GRPO 줄 하나 (SFT 는 부모와 같음)
    assert "a1 의 SFT 에서 GRPO · grpo.beta=0.08" in (root / "compare.md").read_text(encoding="utf-8")
    # 부모가 실패하면 from_sft 모델은 시작하지 않는다
    runner2, calls2 = fake_pipeline({"b1": 4, "b2": 6}, fail={"b1"})
    sw2 = {**sw, "root": "runs/E10", "gpu_groups": [], "runs": [{"label": "b1", "about": "x"}, {"label": "b2", "about": "y", "from_sft": "b1"}]}
    write_json(tmp_path / "e10.sweep.json", sw2)
    base = read_json(tmp_path / "base.json")
    base["data"]["train"] = ["syn-train"]
    write_json(tmp_path / "base.json", base)
    with contextlib.redirect_stdout(io.StringIO()):
        S.run(tmp_path / "e10.sweep.json", runner=runner2)
    assert [c[0] for c in calls2] == ["b1"] and "b1 가 끝나지 않음" in read_json(tmp_path / "runs" / "E10" / "sweep.json")["b2"]["why"]


def test_answers_page(sweep_file, tmp_path):
    """문항별 모델 답: 평가 세트·과제마다 표본, 모델끼리 갈린 문항이 먼저, 모델마다 답과 문항 점수."""
    from train import answers as A

    runner, _ = fake_pipeline({"a1-syn": 4, "a2-real": 8, "a3-more": 10})
    with contextlib.redirect_stdout(io.StringIO()):
        S.run(sweep_file, runner=runner)
    root = tmp_path / "runs" / "E09"
    page = (root / "answers.html").read_text(encoding="utf-8")   # 묶음이 스스로 만든다
    data = json.loads(page.split("id='data'>")[1].split("</script>")[0])
    assert data["models"] == ["출발 모델", "a1-syn", "a2-real", "a3-more"] and data["base"] == "a1-syn"
    assert {(g["set"], g["task"]) for g in data["groups"]} == {("", "cross_check"), ("", "kie")}   # 가짜 문항엔 평가 세트 id 가 없다
    card = next(c for c in data["cards"] if c["id"] == ITEMS[0]["id"])
    assert [a[1] for a in card["answers"]] == [1.0, 1.0, 1.0, 1.0] and "cross_check 질문" in card["prompt"]
    late = next(c for c in data["cards"] if c["id"] == ITEMS[9]["id"])   # a3 만 맞힌 문항
    assert [a[1] for a in late["answers"]] == [0.0, 0.0, 0.0, 1.0] and late["images"][0].endswith(".png")
    sw = S.load(sweep_file)
    reports, _ = S.collect(sw)
    out = A.build(reports, sw["_sources"], tmp_path / "small.html", per_task=2)
    small = json.loads(out.read_text(encoding="utf-8").split("id='data'>")[1].split("</script>")[0])
    kie = next(g for g in small["groups"] if g["task"] == "kie")
    assert kie["shown"] == 2 and kie["n"] == 4 and kie["split"] == 4
    assert len([c for c in small["cards"] if small["groups"][c["g"]]["task"] == "cross_check"]) == 2
