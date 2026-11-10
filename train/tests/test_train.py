"""학습·평가 (train/): 섞기·평가 세트 캐시·답 내기·평가만 하기·실험 묶음·보고서 (GPU·ms-swift 없이, 가짜 모델 서버로)."""
import contextlib
import io
import json
import runpy
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image

from docgen.bench.ocr_data import dumps, read_json, read_jsonl, write_json
from train import mix as M
from train.predict import index_predictions, predict

ORDER = 'in order: ["name", "date"]'
FAKE_SERVER = '''
import json, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
a = sys.argv
model, port = a[a.index("--model") + 1], int(a[a.index("--port") + 1])
wrong = Path(model, "wrong").read_text().split() if Path(model, "wrong").exists() else []
truth = {json.loads(l)["messages"][0]["content"].split("|")[1]: json.loads(l)["messages"][1]["content"]
         for l in open(sys.argv[1], encoding="utf-8")}
class H(BaseHTTPRequestHandler):
    def log_message(self, *x): pass
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"{}")
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        key = body["messages"][0]["content"][-1]["text"].split("|")[1]
        ans = '["x", "x"]' if key in wrong else truth[key]
        out = json.dumps({"choices": [{"message": {"content": ans}, "finish_reason": "stop"}]}).encode()
        self.send_response(200); self.end_headers(); self.wfile.write(out)
ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
'''


def make_model(path: Path, wrong=()):
    path.mkdir(parents=True)
    write_json(path / "config.json", {"vision_config": {"patch_size": 16, "spatial_merge_size": 2}})
    (path / "wrong").write_text(" ".join(wrong))
    return str(path)


def swift_bench(path: Path, n=4):
    """ms-swift 평가 세트: 질문에 '|<키>|' (가짜 서버가 정답을 찾는 표시), 정답은 필드 배열 (swift_default 채점)."""
    (path.parent / "img").mkdir(parents=True, exist_ok=True)
    rows = []
    for i in range(n):
        img = path.parent / "img" / f"b{i}.png"
        Image.new("RGB", (800 + i, 600), "white").save(img)
        rows.append({"messages": [{"role": "user", "content": f"<image>값 |k{i}| {ORDER}"},
                                  {"role": "assistant", "content": json.dumps([f"이름{i}", f"2024-01-0{i + 1}"], ensure_ascii=False)}],
                     "images": [str(img)]})
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return str(path)


def swift_train(path: Path, n=6, images=None):
    (path.parent / "timg").mkdir(parents=True, exist_ok=True)
    rows = []
    for i in range(n):
        img = images[i] if images else path.parent / "timg" / f"t{i}.png"
        if not images:
            Image.new("RGB", (3000, 2000), "white").save(img)
        rows.append({"messages": [{"role": "system", "content": "도우미"}, {"role": "user", "content": "<image>뭐가 보여?"},
                                  {"role": "assistant", "content": "흰 종이"}, {"role": "user", "content": "확실해?"},
                                  {"role": "assistant", "content": "네"}], "images": [str(img)]})
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    return str(path)


def sets_for(tmp_path, bench):
    from train.benchmarks import normalize

    return M.prepare_sets(normalize([{"id": "po", "format": "swift-fields", "paths": [bench]}]), tmp_path / "cache",
                          [2300, 1600], 12000, 32, workers=1)


def test_benchmark_set_is_prepared_once_and_renewed_when_source_changes(tmp_path):
    bench = swift_bench(tmp_path / "data" / "bench.jsonl")
    first = sets_for(tmp_path, bench)["po"]
    done = read_json(first / "DONE.json")
    assert done["n"] == 4 and done["by_task"] == {"kie": 4} and (first / "tasks.jsonl").is_file()
    assert sets_for(tmp_path, bench)["po"] == first   # 그대로 다시 쓴다
    swift_bench(Path(bench), n=3)                     # 원본이 바뀌면 새 폴더
    assert sets_for(tmp_path, bench)["po"] != first


def test_mix_takes_swift_training_lines_as_is_and_refuses_benchmark_images(tmp_path):
    bench = swift_bench(tmp_path / "data" / "bench.jsonl")
    sets = sets_for(tmp_path, bench)
    train = swift_train(tmp_path / "data" / "train.jsonl")
    cfg = {"train": [{"path": train, "format": "swift", "count": 5}], "output_dir": str(tmp_path / "mixed"), "val_count": 1, "workers": 1}
    res = M.mix(cfg, 32, list(sets.values()), tmp_path / "cache" / "images")
    assert res["sft_rows_by_task"] == {"swift:train": 4} and res["val"] == 1 and res["resized_images"] > 0
    row = read_jsonl(tmp_path / "mixed" / "train_sft.jsonl")[0]
    assert [m["role"] for m in row["messages"]] == ["system", "user", "assistant", "user", "assistant"]   # 여러 턴 그대로
    assert Path(row["images"][0]).parent == tmp_path / "cache" / "images"
    # 같은 그림을 다른 실험이 섞으면 줄인 그림을 다시 만들지 않는다
    res2 = M.mix({**cfg, "output_dir": str(tmp_path / "mixed2")}, 32, list(sets.values()), tmp_path / "cache" / "images")
    assert res2["resized_images"] == 0
    leak = swift_train(tmp_path / "data" / "leak.jsonl", n=2, images=[r["images"][0] for r in read_jsonl(bench)[:2]])
    with pytest.raises(ValueError, match="평가 세트와 같은"):
        M.mix({**cfg, "train": [{"path": leak, "format": "swift"}], "output_dir": str(tmp_path / "mixed3")}, 32,
              list(sets.values()), tmp_path / "cache" / "images")


def test_quotas_follow_mix_and_refill():
    assert M.quotas({"a": 100, "b": 5, "c": 50}, {"a": 0.5, "b": 0.5}, 40) == {"a": 35, "b": 5, "c": 50}


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


def test_predict_spreads_images_and_resumes_on_any_server(tmp_path):
    tasks = sets_for(tmp_path, swift_bench(tmp_path / "data" / "bench.jsonl"))["po"] / "tasks.jsonl"
    out = tmp_path / "p.jsonl"
    srv = _Server(2)
    with srv as endpoints:
        predict(tasks, out, endpoints, concurrency=4)
    assert len({i for i, _ in srv.seen}) == 2   # 그림별로 두 서버에 나눔
    other = _Server(1)
    with other as e:   # 서버 주소가 달라도 이어 쓴다 (다시 묻지 않음)
        predict(tasks, out, e)
    assert not other.seen and len(index_predictions(out)) == 4
    with pytest.raises(ValueError, match="다릅니다"), _Server(1) as e:
        predict(tasks, out, e, max_tokens=10)


def _eval_config(tmp_path, models, bench, root="runs/E", extra=None):
    server = tmp_path / "fake_server.py"
    server.write_text(FAKE_SERVER)
    cfg = {"name": "E", "about": "평가만", "root": root, "gpus": [0],
           "eval": {"deploy_command": [sys.executable, str(server), bench, "--model", "{model}", "--port", "{port}"],
                    "port_base": 18900 + (hash(str(tmp_path)) % 50) * 2},
           "models": models, "benchmark": [{"id": "po", "name": "매입추심", "format": "swift-fields", "paths": [bench]}], **(extra or {})}
    path = tmp_path / "eval.json"
    write_json(path, cfg)
    return path


def test_eval_only_caches_answers_and_reports_two_models(tmp_path):
    from train import evaluate as EV

    bench = swift_bench(tmp_path / "data" / "bench.jsonl")
    m1, m2 = make_model(tmp_path / "m1"), make_model(tmp_path / "m2", wrong=["k1", "k3"])
    path = _eval_config(tmp_path, [{"label": "m1", "path": m1}, {"label": "m2", "path": m2, "about": "절반 틀림"}], bench)
    with contextlib.redirect_stdout(io.StringIO()):
        EV.run(path)
    root = tmp_path / "runs" / "E"
    res = read_json(root / "results.json")
    assert [m["label"] for m in res["models"]] == ["m1", "m2"] and res["models"][0]["model"] == m1
    rows = {(r["model"], r["metric"]): r for r in __import__("csv").DictReader((root / "scores.csv").open(encoding="utf-8-sig"))}
    assert float(rows[("m1", "f1")]["value"]) == 1.0 and float(rows[("m2", "f1")]["value"]) == 0.5
    assert float(rows[("m2", "f1")]["delta_pp"]) == -50.0
    page = (root / "answers.html").read_text(encoding="utf-8")
    assert '"models": ["m1", "m2"]' in page and "B 가 나빠진 문항" in page
    assert m1 in (root / "report.html").read_text(encoding="utf-8")   # 모델 경로가 보고서에
    with contextlib.redirect_stdout(io.StringIO()) as out:   # 다시: 서버를 띄우지 않는다
        EV.run(path)
    assert "start server" not in out.getvalue() and out.getvalue().count("캐시") == 2


def test_sweep_runs_models_shares_start_eval_and_reports(tmp_path):
    """실험 묶음: 평가 세트·OCR 준비를 먼저 한 번, 모델마다 학습 실행 (SFT 는 가짜), 출발 모델 평가는 한 번, 보고서·모델 경로."""
    from train import pipeline, sweep

    bench = swift_bench(tmp_path / "data" / "bench.jsonl")
    train = swift_train(tmp_path / "data" / "train.jsonl")
    m1 = make_model(tmp_path / "m1")
    server = tmp_path / "fake_server.py"
    server.write_text(FAKE_SERVER)
    (tmp_path / "cfg").mkdir()
    write_json(tmp_path / "cfg" / "pipeline.json", {
        "model": m1, "gpus": [0], "data": {"train": [{"path": train, "format": "swift"}], "val_count": 1, "workers": 1,
                                            "benchmark": [{"id": "po", "format": "swift-fields", "paths": [bench]}]},
        "eval": {"deploy_command": [sys.executable, str(server), bench, "--model", "{model}", "--port", "{port}"],
                 "port_base": 18800 + (hash(str(tmp_path)) % 50) * 2, "merge_command": ["cp", "-r", "{adapter}", "{output}"],
                 "fill_from_base": False}})
    write_json(tmp_path / "cfg" / "sweep.json", {"name": "S", "about": "묶음", "base": "pipeline.json", "root": "../runs/S",
                                                 "runs": [{"label": "a1", "about": "기준"},
                                                          {"label": "a2", "about": "lr", "sft": {"learning_rate": 1e-5}}]})
    starts = []

    def runner(config, log_path, smoke, env=None):   # 학습 실행을 같은 프로세스에서, SFT 만 가짜 체크포인트로
        cfg = read_json(config)
        run = pipeline.Run(cfg, smoke)
        for st in ("prepare", "eval_start"):
            getattr(run, "stage_" + st)()
            run.state["done"].append(st)
        starts.append(cfg["data"]["prepared_sets"])
        ck = Path(cfg["workdir"]) / "sft" / "v0" / "checkpoint-5"
        ck.mkdir(parents=True)
        write_json(ck / "config.json", {})
        (ck / "wrong").write_text("k0" if cfg["sft"].get("learning_rate") else "")
        run.state["sft_checkpoint"] = str(ck)
        for st in ("eval_sft", "report"):
            getattr(run, "stage_" + st)()
            run.state["done"].append(st)
        run.save()
        return 0
    with contextlib.redirect_stdout(io.StringIO()) as out:
        sweep.run(tmp_path / "cfg" / "sweep.json", runner=runner)
    assert out.getvalue().count("출발 모델: 평가 세트 1개 모두 답이 있습니다") == 1   # 두 번째 모델은 캐시
    assert starts[0] == starts[1]   # 모든 모델이 같은 평가 세트
    root = tmp_path / "runs" / "S"
    res = read_json(root / "results.json")
    assert [m["label"] for m in res["models"]] == ["출발 모델", "a1", "a2"]
    assert res["models"][1]["model"].endswith("a1/merged/sft-v0-checkpoint-5") and res["models"][2]["changes"] == "sft.learning_rate=1e-05"
    assert (root / "report.html").is_file() and (root / "answers.html").is_file()
    assert not (root / "a1" / "report.html").exists()   # 묶음은 보고서 하나
    with contextlib.redirect_stdout(io.StringIO()) as out:
        sweep.show_status(sweep.load(tmp_path / "cfg" / "sweep.json"))
    assert "a2/merged/sft-v0-checkpoint-5" in out.getvalue()


def test_sweep_refuses_removed_keys(tmp_path):
    from train import sweep

    write_json(tmp_path / "s.json", {"name": "S", "about": "x", "base": "p.json", "root": "r",
                                     "runs": [{"label": "a1", "about": "x", "from_sft": "a0"}]})
    with pytest.raises(ValueError, match="from_sft"):
        sweep.load(tmp_path / "s.json")


def test_launch_dry_run(tmp_path):
    model = make_model(tmp_path / "m")
    data = tmp_path / "mixed"
    data.mkdir()
    write_json(data / "DONE.json", {"image_max_size": [2300, 1600]})
    (data / "train_sft.jsonl").write_text('{"messages": []}\n')
    argv = ["launch", "--model", model, "--data", str(data), "--output", str(tmp_path / "runs"), "--max-steps", "5",
            "--options", '{"learning_rate": 5e-05, "lora_rank": 64}']
    capture = io.StringIO()
    with patch.object(sys, "argv", argv), contextlib.redirect_stdout(capture):
        runpy.run_module("train.launch", run_name="__main__")
    out = capture.getvalue()
    assert "swift sft" in out and "IMAGE_MAX_TOKEN_NUM=3600" in out and "--learning_rate 5e-05" in out and "--max_steps 5" in out


def test_port_that_never_frees_is_reported():
    import socket

    from train import serve

    with socket.socket() as held:
        held.bind(("", 0))
        port = held.getsockname()[1]
        assert not serve.port_bindable(port)
        with pytest.raises(RuntimeError, match="still not free"), contextlib.redirect_stdout(io.StringIO()):
            serve.wait_port_free(port, limit=1)
    assert serve.port_bindable(port)
