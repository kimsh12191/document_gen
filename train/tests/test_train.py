"""학습 실행 (train/): 데이터셋 섞기·보상·골라 뽑기·보고서·답 내기·학습 실행기·파이프라인 리허설 (GPU·모델 없이).
옛 ocr/tests (학습 쪽)·bank/tests 를 옮기고, OCR·업무 데이터셋을 한 번에 섞는 시험을 더했다 (studio/DESIGN.md 17절)."""
import contextlib
import io
import json
import runpy
import sys
import threading
import types
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image

from docgen.bench.evaluate import reward
from docgen.bench.ocr_data import dumps, read_json, read_jsonl, write_json, write_jsonl
from docgen.bench.runner import oracle_output
from docgen.tests.ocr_fixture import create_demo
from train import mix as M
from train.predict import index_predictions, predict
from train.report import build
from train.score import mine, score

REPO = Path(__file__).resolve().parents[2]


def _item(task, key, **kw):
    """업무 과제 문항 (docgen 형식, 그 채점기로 맞는 정답)."""
    base = {"cross_check": {"answer": {"consistent": False, "issues": [
                {"document": "대출거래신청서", "field": "성명", "value": "김나무", "expected": "김나우"}]},
                            "eval": {"documents": ["대출거래신청서", "주민등록증"]}, "meta": {"category": "typo"}},
            "review": {"answer": "75.5", "eval": {"answer_type": "number", "tol": 0.05}, "meta": {"skill": "계산(비율)"}},
            "doc_check": {"answer": {"missing": ["재직증명서"], "not_required": [], "not_customer": []},
                          "eval": {"required": ["주민등록증", "재직증명서"], "names": ["주민등록증", "재직증명서"]},
                          "meta": {"n_missing": 1}},
            "kie": {"answer": {"name": "김나우"}, "eval": {"fields": {"name": {"type": "text", "norm": "김나우"}}},
                    "meta": {"group": "bank_form"}}}[task]
    return {"id": f"{task}/{key}/x" if task in ("cross_check", "review") else f"{task}/{key}", "task": task,
            "prompt": f"{task} 질문", **base, **kw}


def bank_folder(root: Path, split, keys, n_images=2, size=(1600, 2260)):
    """docgen.bench build 출력 꼴의 과제 폴더 (고객 묶음마다 문항 몇 개)."""
    (root / "tasks").mkdir(parents=True)
    (root / "images").mkdir()
    items = {}
    for key in keys:
        imgs = []
        for i in range(n_images):
            p = root / "images" / f"{key}_{i}.jpg"
            Image.new("RGB", size, (250, 250, 250)).save(p)
            imgs.append(f"images/{key}_{i}.jpg")
        for task in ("cross_check", "review", "doc_check", "kie"):
            items.setdefault(task, []).append(_item(task, key, images=imgs if task != "kie" else imgs[:1]))
    for task, rows in items.items():
        (root / "tasks" / f"{task}.jsonl").write_text("".join(json.dumps(it, ensure_ascii=False) + "\n" for it in rows), encoding="utf-8")
    write_json(root / "meta.json", {"version": "3.0", "split": split or "test", "counts": {t: len(v) for t, v in items.items()}})
    return items


@pytest.fixture
def model(tmp_path):
    m = tmp_path / "model"
    m.mkdir()
    write_json(m / "config.json", {"vision_config": {"patch_size": 16, "spatial_merge_size": 2}})
    return str(m)


@pytest.fixture(scope="module")
def ocr_set(tmp_path_factory):
    """OCR 준비 결과 (train·val·benchmark 문서가 한 폴더에, 과제 형식 tasks/ 포함)."""
    from docgen.bench.ocr_prepare import prepare

    root = tmp_path_factory.mktemp("ocr")
    prepare(create_demo(root))
    return root / "prepared"


def data_cfg(tmp_path, **kw):
    return {"train": [str(tmp_path / "train")], "benchmark": [str(tmp_path / "bench")],
            "output_dir": str(tmp_path / "prep"), "val_count": 2, "grpo_holdout": 0.3, "workers": 1, **kw}


def test_reward_matches_benchmark_scoring_with_partial_credit():
    cc = _item("cross_check", "b1")
    assert reward("cross_check", oracle_output(cc), cc) == 1.0
    # 다르다고는 했지만 서류를 잘못 짚음: 절반
    assert reward("cross_check", '{"consistent": false, "issues": [{"document": "주민등록증", "field": "주소"}]}', cc) == 0.5
    assert reward("cross_check", '{"consistent": true, "issues": []}', cc) == 0.0
    assert reward("cross_check", "모르겠습니다", cc) == 0.0
    assert reward("cross_check", None, cc) == 0.0
    dc = _item("doc_check", "b1")
    assert reward("doc_check", oracle_output(dc), dc) == 1.0
    assert 0 < reward("doc_check", '{"missing": ["재직증명서", "주민등록증"], "not_required": [], "not_customer": []}', dc) < 1
    rv = _item("review", "b1")
    assert reward("review", "75.5%", rv) == 1.0 and reward("review", "80", rv) == 0.0
    ocr = {"task": "grounding", "answer": {"boxes": [{"bbox_2d": [10, 20, 30, 40], "label": "42"}]}}
    assert reward("grounding", oracle_output(ocr), ocr) == 1.0 and reward("grounding", "[]", ocr) == 0.0


def test_mix_ocr_and_bank_splits_budgets_and_formats(tmp_path, model, ocr_set):
    """업무 학습 세트 + OCR 준비 결과(학습 문항 일부만)를 함께 섞고, 업무 평가 세트 + OCR 평가 문항으로 평가."""
    bank_folder(tmp_path / "train", "train", [f"mortgage_{20000000 + i}" for i in range(12)], n_images=5)
    bank_folder(tmp_path / "bench", None, ["mortgage_2000000", "mortgage_2000001"], n_images=5)
    cfg = data_cfg(tmp_path, max_image_tokens_per_sample=6000,
                   train=[str(tmp_path / "train"), {"path": str(ocr_set), "count": 10}],
                   benchmark=[str(tmp_path / "bench"), str(ocr_set)])
    result = M.mix(cfg, model)
    prep = tmp_path / "prep"
    done = read_json(prep / "DONE.json")
    assert done["max_image_tokens_per_image"] == 3600
    ocr_bench = {t: n for t, n in read_json(ocr_set / "meta.json")["counts"].items()}
    bench_by = result["benchmark_by_task"]
    assert {"cross_check", "doc_check", "kie", "review"} <= set(bench_by) and set(bench_by) & set(ocr_bench)
    ocr_eval = sum(1 for t in ocr_bench for it in read_jsonl(ocr_set / "tasks" / f"{t}.jsonl") if it["meta"]["split"] == "benchmark")
    assert sum(bench_by.values()) == 8 + ocr_eval   # OCR 은 평가 문항(meta.split=benchmark)만
    assert done["sources"]["train"][str(ocr_set)]["rows"] <= 10

    def tokens(p):
        with Image.open(p) as im:
            return -(-im.size[0] // 32) * -(-im.size[1] // 32)

    sft, grpo, bench = (read_jsonl(prep / f) for f in ("train_sft.jsonl", "train_grpo.jsonl", "benchmark_tasks.jsonl"))
    for rows in (sft, grpo, bench):
        for r in rows:
            assert sum(m["content"].count("<image>") for m in r["messages"]) == len(r["images"])
            assert sum(tokens(p) for p in r["images"]) <= 6000   # 5쪽이 예산을 나눠 씀
    assert all(p.endswith(".png") for r in bench + grpo for p in r["images"])
    grpo_items = [json.loads(r["bench_item"]) for r in grpo]
    assert all(r["split"] == "train" and it["task"] == r["task"] for r, it in zip(grpo, grpo_items))
    grpo_keys = {M.group_key(it) for it in grpo_items}
    sft_text = json.dumps(sft, ensure_ascii=False)
    assert grpo_keys and all(k.split(":")[-1] not in sft_text for k in grpo_keys if not k.startswith("doc:"))
    assert any(len(r["messages"]) >= 4 for r in sft)   # 같은 그림의 질문은 한 대화로
    items = read_jsonl(prep / "benchmark_items.jsonl")
    assert all("images" not in it and "prompt" not in it for it in items)
    # OCR 문항의 SFT 답은 옛 1부 답 꼴 그대로 (글자 / 박스 목록 JSON)
    ocr_q = next(it for it in items if it["task"] == "crop_ocr")
    assert oracle_output(ocr_q) == ocr_q["answer"]["text"]
    assert (prep / "image_items.jsonl").is_file()   # --with-ocr 용 사내 OCR


def test_mix_fixes_benchmark_images_apart_from_training(tmp_path, model):
    """benchmark_image_max_size·benchmark_max_image_tokens_per_sample: 학습 그림 예산을 바꿔도 평가 그림은 따로."""
    bank_folder(tmp_path / "train", "train", [f"mortgage_{20000000 + i}" for i in range(6)], n_images=2)
    bank_folder(tmp_path / "bench", None, ["mortgage_2000000"], n_images=2)
    out = {}
    for name, extra in (("a", {}), ("b", {"image_max_size": [800, 600], "max_image_tokens_per_sample": 900,
                                          "benchmark_image_max_size": [2300, 1600], "benchmark_max_image_tokens_per_sample": 12000})):
        cfg = {**data_cfg(tmp_path, train=[str(tmp_path / "train")], benchmark=[str(tmp_path / "bench")]),
               "output_dir": str(tmp_path / name), **extra}
        M.mix(cfg, model)
        out[name] = read_jsonl(tmp_path / name / "benchmark_tasks.jsonl"), read_jsonl(tmp_path / name / "train_sft.jsonl")

    def size(p):
        with Image.open(p) as im:
            return im.size
    assert [[size(p) for p in r["images"]] for r in out["a"][0]] == [[size(p) for p in r["images"]] for r in out["b"][0]]
    assert max(max(size(p)) for r in out["b"][1] for p in r["images"]) < 1000 < max(max(size(p)) for r in out["a"][1] for p in r["images"])
    assert read_json(tmp_path / "b" / "DONE.json")["benchmark_image_max_size"] == [2300, 1600]


def test_mix_refuses_leaks_and_eval_only_training(tmp_path, model):
    bank_folder(tmp_path / "bench", None, ["mortgage_2"], n_images=1)
    bank_folder(tmp_path / "train", None, ["mortgage_1"], n_images=1)   # 평가 세트를 학습에 넣음
    with pytest.raises(ValueError, match="학습 문항이 없습니다"):
        M.mix(data_cfg(tmp_path), model)
    same = tmp_path / "same"
    bank_folder(same, "train", ["mortgage_2"], n_images=1)   # 평가와 같은 고객
    with pytest.raises(ValueError, match="share a customer"):
        M.mix(data_cfg(tmp_path, train=[str(same)]), model)


def test_quotas_follow_mix_and_refill():
    take = M.quotas({"a": 100, "b": 5, "c": 100, "d": 50}, {"a": 0.5, "b": 0.5, "d": 0}, 40)
    assert take == {"a": 35, "b": 5, "c": 100}   # b 가 모자라 a 가 채움, c(목록 밖)는 다, d(0)는 뺌
    assert sum(M.quotas({"a": 3, "b": 4}, None, 100).values()) == 7


def test_mine_and_report(tmp_path):
    items = [_item("cross_check", f"b{i}") for i in range(10)]
    ocr = [{"id": f"o{i}", "task": "crop_ocr", "answer": {"text": "홍길동"}, "meta": {"view": "clean"}} for i in range(4)]
    rows = [{"id": it["id"], "split": "train", "task": it["task"], "bench_item": json.dumps(it)} for it in items]
    preds = {it["id"]: oracle_output(it) if i < 6 else "틀림" for i, it in enumerate(items)}
    chosen, info = mine(rows, preds, count=4, seed=0, hard_fraction=0.5)
    assert len(chosen) == 4 and info["hard_available"] == 4 and info["hard_selected"] >= 2
    reports = []
    for name, role, good in (("출발", "start", 3), ("SFT", "sft", 8)):
        res = score(items + ocr, {**{it["id"]: oracle_output(it) if i < good else "x" for i, it in enumerate(items)},
                                  **{it["id"]: "홍길동" if role == "sft" else "홍길" for it in ocr}})
        path = tmp_path / f"{role}.json"
        write_json(path, {"label": name, "role": role, **res})
        reports.append(path)
    build(reports, tmp_path / "out" / "benchmark.csv")
    md = (tmp_path / "out" / "benchmark.md").read_text(encoding="utf-8")
    assert "칸 잘라 읽기 CER ↓" in md and "| SFT | 0.0 |" in md   # OCR 열 (CER 은 낮을수록)
    assert "+50.0" in md
    other = score(items[:5], {})
    write_json(tmp_path / "other.json", {"label": "다른 세트", **other})
    with pytest.raises(ValueError, match="different benchmark"):
        build(reports + [tmp_path / "other.json"], tmp_path / "out" / "x.csv")


def test_swift_plugin_batch_contract():
    # 공개 등록부만 흉내 낸다 (GPU·ms-swift 실제 연동은 시험하지 않음)
    swift = types.ModuleType("swift")
    registry = types.ModuleType("swift.rewards")
    registry.ORM, registry.orms = object, {}
    with patch.dict(sys.modules, {"swift": swift, "swift.rewards": registry}):
        runpy.run_path(str(REPO / "train" / "reward_plugin.py"))
    plugin = registry.orms["docgen"]()
    box = {"bbox_2d": [10, 20, 30, 40], "label": "42"}
    cc = _item("cross_check", "b1")
    scores = plugin(["ABC", dumps([box]), oracle_output(cc)], ["bbox_ocr", "grounding", "cross_check"],
                    [dumps({"answer": {"text": "ABC"}}), dumps({"answer": {"boxes": [box]}}), dumps(cc)])
    assert scores == [1, 1, 1.0]
    with pytest.raises(ValueError):
        plugin(["ABC"], [], [])


@pytest.fixture
def mixed(tmp_path, model, ocr_set):
    bank_folder(tmp_path / "train", "train", [f"m_{i}" for i in range(6)], n_images=1, size=(400, 560))
    bank_folder(tmp_path / "bench", None, ["b_0", "b_1"], n_images=1, size=(400, 560))
    M.mix(data_cfg(tmp_path, benchmark=[str(tmp_path / "bench"), str(ocr_set)]), model)
    return tmp_path / "prep"


def test_launch_dry_runs(tmp_path, mixed, model):
    adapter = tmp_path / "fake-adapter"
    adapter.mkdir()
    for stage in ["sft", "grpo"]:
        argv = ["launch", stage, "--model", model, "--data", str(mixed), "--output", str(tmp_path / "runs"), "--max-steps", "5"]
        if stage == "grpo":
            argv += ["--adapter", str(adapter)]
        capture = io.StringIO()
        with patch.object(sys, "argv", argv), contextlib.redirect_stdout(capture):
            runpy.run_module("train.launch", run_name="__main__")
        out = capture.getvalue()
        assert "NPROC_PER_NODE=4" in out and "IMAGE_MAX_TOKEN_NUM=3600" in out and "--freeze_vit false" in out
        if stage == "grpo":
            assert "--remove_unused_columns false" in out and "reward_plugin.py" in out and '--reward_funcs docgen' in out
    # --options: yaml 위에 칸 하나씩 (실험 묶음의 sft·grpo 칸)
    argv = ["launch", "sft", "--model", model, "--data", str(mixed), "--output", str(tmp_path / "runs"),
            "--options", '{"learning_rate": 5e-05, "lora_rank": 64}']
    capture = io.StringIO()
    with patch.object(sys, "argv", argv), contextlib.redirect_stdout(capture):
        runpy.run_module("train.launch", run_name="__main__")
    assert "--learning_rate 5e-05" in capture.getvalue() and "--lora_rank 64" in capture.getvalue()


class _Server:
    def __init__(self, n, answer="x"):
        self.seen = []
        outer = self

        def make(i):
            class Handler(BaseHTTPRequestHandler):
                def do_POST(self):
                    payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                    outer.seen.append((i, payload))
                    body = dumps({"choices": [{"message": {"content": answer}, "finish_reason": "stop"}]}).encode()
                    self.send_response(200)
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)

                def log_message(self, *args):
                    pass
            return Handler
        self.servers = [HTTPServer(("127.0.0.1", 0), make(i)) for i in range(n)]
        self.threads = [threading.Thread(target=s.serve_forever, daemon=True) for s in self.servers]

    def __enter__(self):
        for t in self.threads:
            t.start()
        return ",".join(f"http://127.0.0.1:{s.server_port}/v1" for s in self.servers)

    def __exit__(self, *exc):
        for s, t in zip(self.servers, self.threads):
            s.shutdown()
            t.join()
            s.server_close()


def test_predict_spreads_images_resumes_and_does_not_leak(tmp_path, mixed):
    tasks = mixed / "benchmark_tasks.jsonl"
    srv = _Server(2)
    with srv as endpoints:
        out = tmp_path / "p.jsonl"
        predict(tasks, out, endpoints, "docgen", "base", concurrency=4)
        n = len(srv.seen)
        predict(tasks, out, endpoints, "docgen", "base")
        assert len(srv.seen) == n == len(read_jsonl(tasks))   # 이어서 낼 때 다시 묻지 않는다
        with pytest.raises(ValueError, match="changed"):
            predict(tasks, out, endpoints, "docgen", "sft-v1")
    by_image = {}
    for i, payload in srv.seen:
        content = payload["messages"][0]["content"]
        assert content[0]["type"] == "image_url" and content[-1]["type"] == "text"   # 그림 먼저 (학습과 같게)
        assert "<image>" not in content[-1]["text"]
        by_image.setdefault(content[0]["image_url"]["url"], set()).add(i)
    assert all(len(v) == 1 for v in by_image.values())   # 같은 그림은 같은 서버로
    items = {it["id"]: it for it in read_jsonl(mixed / "benchmark_items.jsonl")}
    sent = {p["messages"][0]["content"][-1]["text"] for _, p in srv.seen}
    for it in items.values():
        if it["task"] == "crop_ocr":
            assert it["answer"]["text"] not in sent   # 정답이 질문에 새지 않는다
    assert len(index_predictions(out)) == n


def test_pipeline_ocr_prepare_stage_is_optional_and_runs_once(tmp_path, model):
    """ocr_prepare: 가진 이미지를 OCR 준비 (설정이 없으면 건너뜀, 여러 개면 차례로). 결과 폴더는 data 에 적어 둔 경로로
    섞기에 들어간다: 학습용 준비 폴더는 학습(train·val 문서)·평가(떼어 둔 문서) 둘 다, 평가 전용(benchmark_only)은 평가에만."""
    from train import pipeline as P

    create_demo(tmp_path / "ocr")   # manifest + OCR 준비 설정 (가짜 사내 OCR), output_dir = ocr/prepared
    create_demo(tmp_path / "ocr_eval")
    man = [{**r, "document_id": "eval_" + r["document_id"], "split": "benchmark"}
           for r in read_jsonl(tmp_path / "ocr_eval" / "manifest.jsonl")]
    (tmp_path / "ocr_eval" / "manifest.jsonl").write_text("".join(dumps(r) + "\n" for r in man), encoding="utf-8")
    write_json(tmp_path / "ocr_eval" / "config.json", {**read_json(tmp_path / "ocr_eval" / "config.json"), "benchmark_only": True})
    bank_folder(tmp_path / "train", "train", [f"mortgage_{20000000 + i}" for i in range(6)], n_images=1)
    bank_folder(tmp_path / "bench", None, ["mortgage_2000000"], n_images=1)
    config = tmp_path / "pipeline.json"
    write_json(config, {"workdir": "runs", "model": model, "ocr_prepare": ["ocr/config.json", "ocr_eval/config.json"], "data": {
        "train": ["train", {"path": "ocr/prepared", "count": 10}], "benchmark": ["bench", "ocr/prepared", "ocr_eval/prepared"],
        "output_dir": "prep", "val_count": 2, "grpo_holdout": 0.3, "workers": 1}})
    runner = P.Runner(P.merged(P.DEFAULTS, read_json(config)), config, False, False)
    assert runner.ocr_configs == [str(tmp_path / "ocr" / "config.json"), str(tmp_path / "ocr_eval" / "config.json")]
    runner.check_inputs()   # 아직 없는 OCR 준비 폴더는 묻지 않는다
    with contextlib.redirect_stdout(io.StringIO()) as out:
        runner.stage_ocr_prepare()
        runner.stage_ocr_prepare()
        runner.stage_prepare()
    assert out.getvalue().count("OCR prepared data exists") == 2
    done = read_json(tmp_path / "prep" / "DONE.json")
    assert done["sources"]["train"][str(tmp_path / "ocr" / "prepared")]["rows"] <= 10
    assert set(done["sources"]["benchmark"]) == {str(tmp_path / p) for p in ("bench", "ocr/prepared", "ocr_eval/prepared")}
    eval_ids = {it["id"] for t in read_json(tmp_path / "ocr_eval" / "prepared" / "meta.json")["counts"]
                for it in read_jsonl(tmp_path / "ocr_eval" / "prepared" / "tasks" / f"{t}.jsonl")}
    assert eval_ids <= {it["id"] for it in read_jsonl(tmp_path / "prep" / "benchmark_items.jsonl")}
    assert {"spotting", "kie"} <= set(done["counts"]["benchmark_by_task"])
    write_json(config, {"workdir": "runs2", "model": model, "data": read_json(config)["data"]})
    runner = P.Runner(P.merged(P.DEFAULTS, read_json(config)), config, False, False)
    with contextlib.redirect_stdout(io.StringIO()) as out:
        runner.stage_ocr_prepare()
    assert "no ocr_prepare config" in out.getvalue()


def test_swift_jsonl_is_a_benchmark_as_is(tmp_path, model):
    """실서류 swift .jsonl 을 data.benchmark 에 format swift-fields 로: 질문은 그대로, 정답 글은 그대로 채점 함수에.
    scorer 를 안 적으면 swift_default (질문의 필드 순서와 답 배열을 짝지어 필드마다), 그 함수가 못 읽는 줄은 건너뜀."""
    real = tmp_path / "real"
    (real / "images").mkdir(parents=True)
    Image.new("RGB", (400, 560), "white").save(real / "images" / "a.png")
    prompt = ('<image>\nWhat are the values of the following fields in this document, in order: ["NO_LC", "DATE", "DATE"]\n'
              "Return only a valid JSON array of strings.")
    rows = [{"messages": [{"role": "user", "content": prompt},
                          {"role": "assistant", "content": dumps(["K114434", "2025 년 01월 01일", "20250101"])}],
             "images": [str(real / "images" / "a.png")]},
            {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": "[\"하나뿐\"]"}],
             "images": ["images/a.png"]}]
    (real / "eval_qa.jsonl").write_text("".join(dumps(r) + "\n" for r in rows), encoding="utf-8")
    bank_folder(tmp_path / "train", "train", [f"m_{i}" for i in range(6)], n_images=1, size=(400, 560))
    bench = [{"id": "real-fx", "name": "실서류 외환", "group": "real", "paths": [str(real / "eval_qa.jsonl")]}]
    with pytest.raises(ValueError, match="swift-fields"):   # 형식을 적지 않으면 짐작하지 않는다
        M.mix(data_cfg(tmp_path, benchmark=bench), model)
    bench[0].update(format="swift-fields", gt="reviewed")
    with contextlib.redirect_stdout(io.StringIO()) as out:
        M.mix(data_cfg(tmp_path, benchmark=bench), model)
    assert "읽지 못한 1줄을 건너뜁니다" in out.getvalue()
    assert read_json(tmp_path / "prep" / "DONE.json")["sources"]["benchmark"][str(real / "eval_qa.jsonl")]["gt"] == "reviewed"
    items = read_jsonl(tmp_path / "prep" / "benchmark_items.jsonl")
    assert [it["id"] for it in items] == ["eval_qa/00001"]
    it = items[0]
    assert it["answer"] == dumps(["K114434", "2025 년 01월 01일", "20250101"]) and it["eval"]["scorer"].endswith("swift_default.py:score")
    task = read_jsonl(tmp_path / "prep" / "benchmark_tasks.jsonl")[0]
    assert task["messages"][0]["content"].startswith("<image>What are the values")   # 질문은 그대로
    res = score([it], {it["id"]: '["K114434", "2025년 01월 01일", "20250101"]'})["tasks"]["kie"]
    assert res["main"] == "f1" and res["metrics"]["field_acc"] == 1.0 and abs(res["metrics"]["field_exact"] - 2 / 3) < 1e-9
    assert score([it], {it["id"]: '["K114434", "20250101"]'})["tasks"]["kie"]["metrics"]["field_acc"] == 0.0   # 개수가 다름
    assert score([it], {it["id"]: '{"NO_LC": "K114434", "DATE": "2025 년 01월 01일", "DATE#2": "20250101"}'})["tasks"]["kie"]["metrics"]["f1"] == 1.0


def test_swift_jsonl_any_content_with_scorer(tmp_path, model):
    """swift .jsonl 은 질문·답 내용과 상관없이 읽는다: 기본 견본이 못 읽는 정답 꼴은 그 세트에 맞는 채점 함수를 붙인다."""
    real = tmp_path / "real"
    (real / "images").mkdir(parents=True)
    Image.new("RGB", (400, 560), "white").save(real / "images" / "a.png")
    obj = [{"messages": [{"role": "user", "content": "<image>이 문서의 항목 값을 JSON 객체로 답하세요.\n- NEGO_CLCT\n- DATE"},
                         {"role": "assistant", "content": dumps({"NEGO_CLCT": "EOA", "DATE": "2025 05 21"})}],
            "images": ["images/a.png"]}]
    free = [{**obj[0], "messages": [{"role": "user", "content": "<image>매입추심 구분은?"}, {"role": "assistant", "content": "EOA"}]}]
    write_jsonl(real / "obj.jsonl", obj)
    write_jsonl(real / "free.jsonl", free)
    bank_folder(tmp_path / "train", "train", [f"m_{i}" for i in range(6)], n_images=1, size=(400, 560))
    bench = [{"id": "po-obj", "paths": [str(real / "obj.jsonl")], "format": "swift-fields"},
             {"id": "po-free", "paths": [str(real / "free.jsonl")], "format": "swift-fields"}]
    with pytest.raises(ValueError, match="po-free.*읽은 정답이 없습니다"):   # 기본 견본이 모르는 꼴
        M.mix(data_cfg(tmp_path, benchmark=bench), model)
    (tmp_path / "same.py").write_text("def score(item, output):\n    return {'metrics': {'acc': float(output.strip() == item['answer'])}, 'main': 'acc'}\n",
                                      encoding="utf-8")
    bench[1]["scorer"] = str(tmp_path / "same.py")
    with contextlib.redirect_stdout(io.StringIO()):
        M.mix(data_cfg(tmp_path, benchmark=bench), model)
    items = {it["meta"]["benchmark_id"]: it for it in read_jsonl(tmp_path / "prep" / "benchmark_items.jsonl")}
    pred = {items["po-obj"]["id"]: '{"NEGO_CLCT": "EOA", "DATE": "2025-05-21"}', items["po-free"]["id"]: " EOA"}
    res = score(list(items.values()), pred)["benchmarks"]
    assert res["po-obj"]["tasks"]["kie"]["metrics"]["f1"] == 1.0 and res["po-free"]["tasks"]["kie"]["main"] == "acc"
    assert res["po-free"]["tasks"]["kie"]["metrics"]["acc"] == 1.0


def _swift_rows(real, names):
    prompt = '<image>\nWhat are the values of the following fields in this document, in order: ["NO", "DATE"]'
    (real / "images").mkdir(parents=True, exist_ok=True)
    rows = []
    for i, n in enumerate(names):
        Image.new("RGB", (400, 560), "white").save(real / "images" / f"{n}.png")
        rows.append({"messages": [{"role": "user", "content": prompt},
                                  {"role": "assistant", "content": dumps([f"K{i:04d}", "2025-01-01"])}],
                     "images": [f"images/{n}.png"]})
    return rows


def test_swift_jsonl_as_training_data(tmp_path, model):
    """swift .jsonl 을 data.train 에 format swift-fields 로: 정답 글 그대로 SFT 답, 채점 함수가 못 읽는 줄은 빼고,
    GRPO 보상은 그 채점 함수 (부분 점수), 평가 세트와 같은 그림이면 파일이 달라도 멈춘다. 경로만 적은 학습 데이터는 예전 그대로."""
    real = tmp_path / "real"
    rows = _swift_rows(real, [f"d{i}" for i in range(12)])
    broken = {**rows[0], "messages": [rows[0]["messages"][0], {"role": "assistant", "content": "[\"하나뿐\"]"}]}
    write_jsonl(real / "train_qa.jsonl", rows + [broken])
    bank_folder(tmp_path / "bench", None, ["b_0", "b_1"], n_images=1, size=(400, 560))
    train = [{"path": str(real / "train_qa.jsonl")}]
    with pytest.raises(ValueError, match="swift-fields"):   # 형식을 적지 않으면 짐작하지 않는다
        M.mix(data_cfg(tmp_path, train=train), model)
    train[0]["format"] = "swift-fields"
    with contextlib.redirect_stdout(io.StringIO()) as out:
        done = M.mix(data_cfg(tmp_path, train=train), model)
    assert "읽지 못한 1줄을 학습에서 뺍니다" in out.getvalue()
    src = read_json(tmp_path / "prep" / "DONE.json")["sources"]["train"][str(real / "train_qa.jsonl")]
    assert src["format"] == "swift-fields" and src["scorer"].endswith("swift_default.py:score")
    sft = read_jsonl(tmp_path / "prep" / "train_sft.jsonl") + read_jsonl(tmp_path / "prep" / "val_sft.jsonl")
    grpo = read_jsonl(tmp_path / "prep" / "train_grpo.jsonl")
    answers = {m["content"] for r in sft for m in r["messages"] if m["role"] == "assistant"}
    assert answers and answers <= {r["messages"][1]["content"] for r in rows}   # 정답 글 그대로, 깨진 줄 없음
    assert grpo and all(r["task"] == "kie" for r in grpo)
    item = json.loads(grpo[0]["bench_item"])
    assert item["eval"]["scorer"].endswith("swift_default.py:score")
    assert reward("kie", item["answer"], item) == 1.0
    assert reward("kie", dumps([json.loads(item["answer"])[0], "1999-12-31"]), item) == 0.5   # 두 칸 중 하나
    assert reward("kie", "모르겠습니다", item) == 0.0 and reward("kie", None, item) == 0.0
    del done

    # 평가 swift 세트가 같은 그림을 쓰면 (파일 이름이 달라 문서 ID 가 달라도) 멈춘다
    write_jsonl(real / "eval_qa.jsonl", rows[:1])
    bench = [{"id": "real", "paths": [str(real / "eval_qa.jsonl")], "format": "swift-fields"}]
    with pytest.raises(ValueError, match="share a customer or document"):
        M.mix(data_cfg(tmp_path, train=train, benchmark=bench, output_dir=str(tmp_path / "prep2")), model)


def test_eval_drops_questions_over_server_image_limit(tmp_path, mixed, model):
    """서버(--vllm_limit_mm_per_prompt)보다 그림이 많은 평가 문항은 빼고 기록한다: 한 문항 때문에 추론 전체가 멈추지 않게."""
    from train import pipeline as P

    rows = read_jsonl(mixed / "benchmark_tasks.jsonl")
    big = {**rows[0], "id": "big/1", "images": rows[0]["images"] * 3}
    write_jsonl(mixed / "benchmark_tasks.jsonl", rows + [big])
    config = tmp_path / "pipeline.json"
    write_json(config, {"workdir": "runs", "model": model, "data": {"train": [str(tmp_path / "train")], "output_dir": "prep",
                                                                     "benchmark": [str(tmp_path / "bench")]}})
    cfg = P.merged(P.DEFAULTS, read_json(config))
    cfg["eval"]["deploy_command"] = [p.replace("16", "2") for p in cfg["eval"]["deploy_command"]]
    runner = P.Runner(cfg, config, False, False)
    assert runner.image_limit() == 2
    with contextlib.redirect_stdout(io.StringIO()) as out:
        tasks = runner.benchmark_tasks()
    assert "1개는 그림이 2장보다 많아" in out.getvalue()
    assert [r["id"] for r in read_jsonl(tasks)] == [r["id"] for r in rows]
    assert read_jsonl(tmp_path / "runs" / "benchmark_over_image_limit.jsonl") == [{"id": "big/1", "task": big["task"], "n_images": 3}]
    runner.cfg["eval"]["deploy_command"] = ["swift", "deploy"]   # 한도를 못 읽으면 그대로
    assert runner.benchmark_tasks() == mixed / "benchmark_tasks.jsonl"


def test_pipeline_parts_run_sft_and_grpo_separately(tmp_path, mixed, model):
    """--part sft 는 SFT 까지 + 보고서, --part grpo 는 SFT 체크포인트에서 GRPO + 보고서. 체크포인트가 없으면 멈춘다."""
    from train import pipeline as P

    config = tmp_path / "pipeline.json"
    write_json(config, {"workdir": "runs", "model": model,
                        "data": {"train": [str(tmp_path / "train")], "benchmark": [str(tmp_path / "bench")], "output_dir": "prep"}})

    def ran(*args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            P.main(["--config", str(config), "--dry-run", *args])
        return [st for st in P.STAGES if f"=== {st} done" in out.getvalue()], out.getvalue()

    assert ran("--part", "sft")[0] == ["ocr_prepare", "prepare", "eval_base", "sft", "eval_sft", "report"]
    stages, text = ran("--part", "grpo")
    assert stages == ["prepare", "eval_sft", "select", "grpo", "eval_grpo", "report"]
    assert "--adapter <sft checkpoint>" in text
    ckpt = tmp_path / "other" / "checkpoint-100"
    ckpt.mkdir(parents=True)
    assert f"--adapter {ckpt}" in ran("--part", "grpo", "--sft-checkpoint", str(ckpt))[1]
    with pytest.raises(SystemExit, match="SFT 체크포인트가 없습니다"):
        P.main(["--config", str(config), "--part", "grpo"])
    # SFT 가 끝난 상태: --part grpo 는 SFT 평가를 건너뛰고, 보고서는 늘 다시 만든다
    runner = P.Runner(P.merged(P.DEFAULTS, read_json(config)), config, False, False)
    runner.state.update(done=["ocr_prepare", "prepare", "eval_base", "sft", "eval_sft", "report"], sft_checkpoint=str(ckpt))
    runner.save()
    calls = []
    with patch.object(P.Runner, "check_inputs", lambda self: None), \
            patch.multiple(P.Runner, **{f"stage_{st}": (lambda st: lambda self: calls.append(st))(st) for st in P.STAGES}):
        with contextlib.redirect_stdout(io.StringIO()):
            P.main(["--config", str(config), "--part", "grpo"])
    assert calls == ["select", "grpo", "eval_grpo", "report"]
    calls.clear()
    other = tmp_path / "other" / "checkpoint-200"
    other.mkdir()
    with patch.object(P.Runner, "check_inputs", lambda self: None), \
            patch.multiple(P.Runner, **{f"stage_{st}": (lambda st: lambda self: calls.append(st))(st) for st in P.STAGES}):
        with contextlib.redirect_stdout(io.StringIO()):
            P.main(["--config", str(config), "--part", "grpo", "--sft-checkpoint", str(other)])
    assert calls == ["eval_sft", "select", "grpo", "eval_grpo", "report"]
    assert read_json(runner.state_path)["sft_checkpoint"] == str(other)


def test_pipeline_dry_run_and_grpo_rerun_report(tmp_path, mixed, model):
    from train import pipeline as P

    config = tmp_path / "pipeline.json"
    write_json(config, {"workdir": "runs", "model": model,
                        "data": {"train": [str(tmp_path / "train")], "benchmark": [str(tmp_path / "bench")], "output_dir": "prep"}})
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        P.main(["--config", str(config), "--dry-run"])
    text = capture.getvalue()
    for stage in P.STAGES:
        assert f"=== {stage} done" in text
    assert "IMAGE_MAX_TOKEN_NUM=3600" in text and "--gpus 0,1" in text and "-m train.launch" in text
    assert "--options" not in text   # yaml 그대로
    write_json(config, {**read_json(config), "sft": {"learning_rate": 5e-05}, "grpo": {"beta": 0.08, "count": 10},
                        "data": {**read_json(config)["data"], "sft_max_length": 8192}})
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        P.main(["--config", str(config), "--dry-run"])
    text = capture.getvalue()
    assert '--options {"learning_rate": 5e-05, "max_length": 8192}' in text and '--options {"beta": 0.08}' in text
    write_json(config, {k: v for k, v in read_json(config).items() if k not in ("sft", "grpo")})
    assert "prepared data exists" in text   # 섞은 폴더가 있으면 다시 섞지 않는다
    assert not (tmp_path / "runs" / "state.json").exists()
    # GRPO 를 다시 돌리면 앞의 점수도 보고서에 남는다
    runner = P.Runner(P.merged(P.DEFAULTS, read_json(config)), config, False, False)
    reports = runner.workdir / "reports"
    items = read_jsonl(mixed / "benchmark_items.jsonl")
    res = score(items, {it["id"]: oracle_output(it) for it in items})
    for name, role in (("start", "start"), ("sft", "sft"), ("grpo-v0-1-checkpoint-500", "grpo"), ("grpo-v1-2-checkpoint-500", "grpo")):
        write_json(reports / f"{name}.json", {"label": name, "role": role, **res})
    commands = []
    with patch.object(runner, "run", lambda cmd, log_name, env=None: commands.append(cmd)):
        runner.stage_report()
    cmd = commands[0]
    names = [Path(p).name for p in cmd[cmd.index("--reports") + 1:cmd.index("--out")]]
    assert names == ["start.json", "sft.json", "grpo-v0-1-checkpoint-500.json", "grpo-v1-2-checkpoint-500.json"]
    page = (reports / "summary.html").read_text(encoding="utf-8")   # 학습 실행도 한 화면을 남긴다 (이 workdir 의 모델만)
    assert "grpo-v1-2-checkpoint-500" in page and "한눈에 보기" in page
    import subprocess

    subprocess.run(cmd, check=True, capture_output=True, cwd=REPO)
    rows = (reports / "benchmark.csv").read_text(encoding="utf-8-sig").splitlines()
    assert [r.split(",")[0] for r in rows[1:]] == ["start", "sft", "grpo-v0-1-checkpoint-500", "grpo-v1-2-checkpoint-500"]


FAKE_SERVER = r'''
import sys, time
from http.server import BaseHTTPRequestHandler, HTTPServer
port, mode = int(sys.argv[1]), sys.argv[2]
if mode == "moved":   # swift deploy 가 포트를 못 잡아 다음 포트로 뜬 것처럼
    print(f"INFO:     Uvicorn running on http://127.0.0.1:{port + 2} (Press CTRL+C to quit)", flush=True)
    time.sleep(60)
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"{}")
    def log_message(self, *a):
        pass
srv = HTTPServer(("127.0.0.1", port), H)
print(f"INFO:     Uvicorn running on http://127.0.0.1:{port} (Press CTRL+C to quit)", flush=True)
srv.serve_forever()
'''


def _free_port():
    import socket

    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _serve_runner(tmp_path, mixed, model, mode):
    from train import pipeline as P

    config = tmp_path / "pipeline.json"
    write_json(config, {"workdir": "runs", "model": model, "data": {"train": [str(tmp_path / "train")], "output_dir": "prep",
                                                                     "benchmark": [str(tmp_path / "bench")]}})
    script = tmp_path / "fake_server.py"
    script.write_text(FAKE_SERVER, encoding="utf-8")
    cfg = P.merged(P.DEFAULTS, read_json(config))
    cfg["gpus"] = [0]
    cfg["eval"] |= {"port_base": _free_port(), "deploy_command": [sys.executable, str(script), "{port}", mode],
                    "server_start_timeout_minutes": 1}
    runner = P.Runner(cfg, config, False, False)
    (runner.workdir / "logs").mkdir(parents=True, exist_ok=True)
    return runner, cfg["eval"]["port_base"]


def test_eval_server_waits_until_the_port_is_free(tmp_path, mixed, model):
    """앞 서버를 끈 직후처럼 포트에 bind 가 안 되면 (TIME_WAIT), 빌 때까지 기다렸다 그 포트로 띄운다.
    그냥 띄우면 swift deploy 는 말없이 다음 포트로 떠서 이 포트만 기다리다 시간이 다 간다."""
    import socket

    runner, port = _serve_runner(tmp_path, mixed, model, "ok")
    held = socket.socket()
    held.bind(("", port))   # bind 만 (listen 안 함): 연결은 안 되지만 새 bind 는 실패 — TIME_WAIT 와 같은 상황
    threading.Timer(2.0, held.close).start()
    with contextlib.redirect_stdout(io.StringIO()) as out, runner.serve("model", "t") as endpoints:
        assert endpoints == f"http://127.0.0.1:{port}/v1"
    assert f"port {port} is not free yet" in out.getvalue() and f"server on port {port} ready" in out.getvalue()


def test_eval_server_on_another_port_stops_at_once(tmp_path, mixed, model):
    import time

    runner, port = _serve_runner(tmp_path, mixed, model, "moved")
    started = time.monotonic()
    with pytest.raises(RuntimeError, match=f"started on port {port + 2} instead"), \
            contextlib.redirect_stdout(io.StringIO()), runner.serve("model", "t"):
        pass
    assert time.monotonic() - started < 30   # 40분(시간 한도)을 기다리지 않는다


def test_port_that_never_frees_is_reported():
    import socket

    from train import pipeline as P

    with socket.socket() as held:
        held.bind(("", 0))
        port = held.getsockname()[1]
        assert not P.port_bindable(port)
        with pytest.raises(RuntimeError, match="still not free"), contextlib.redirect_stdout(io.StringIO()):
            P.wait_port_free(port, limit=1)
    assert P.port_bindable(port)
