"""학습 실행 하나 (옛 ocr/run_pipeline.py + bank/run_bank_pipeline.py): 데이터셋 섞기부터 Base/SFT/GRPO 비교 보고서까지.

단계 (<workdir>/state.json 에 끝난 것을 적고, 다시 돌리면 이어서):
  ocr_prepare (설정에 ocr_prepare 가 있을 때만) 가진 이미지를 사내 OCR 해 OCR 학습·평가 데이터로 (docgen.bench.ocr_prepare <그 설정>,
              여러 개면 차례로. 예: 학습용 + 평가 전용(benchmark_only)).
              결과 폴더(그 설정의 output_dir)를 data.train·data.benchmark 에 적어 둔다. 합성 OCR 등 이미 만든 데이터만 쓰면 빼 둔다
  prepare     data 칸의 데이터셋 섞기 (mix.py) → data.output_dir
  eval_base   출발 모델 평가 (eval.compare_models 도)
  sft         SFT (launch.py), 마지막 체크포인트를 적어 둠
  eval_sft    SFT 모델 병합·평가, GRPO 후보 답 (골라 뽑기용)
  select      GRPO 문항 고르기 (mine / random / all)
  grpo        SFT 체크포인트에서 GRPO, 보상 = 평가 채점 (reward_plugin.py)
  eval_grpo   GRPO 모델 병합·평가
  report      reports/benchmark.{csv,md,html}

평가는 GPU 마다 추론 서버 하나를 띄우고 요청을 나눠 보낸다 (같은 그림의 질문은 같은 서버로 → 그림 캐시 재사용).
저장소 최상위에서:
  python -m train --config train/configs/pipeline.json --smoke     # 5 step·작은 평가 리허설 (workdir/smoke)
  python -m train --config train/configs/pipeline.json             # 전부
  python -m train --config train/configs/pipeline.json --from grpo # GRPO 다시 (보고서는 둘 다 남김)
  python -m train --config train/configs/pipeline.json --dry-run   # 명령만 보기
"""
import argparse
import json
import os
import random
import shutil
import signal
import socket
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from docgen.bench.ocr_data import read_json, read_jsonl, write_json, write_jsonl

from .cli import resolve_data
from .settings import image_tokens, image_tokens_for, load_settings

ROOT = Path(__file__).resolve().parents[1]   # 저장소 최상위: 하위 명령은 여기서 python -m train.… 으로
STAGES = ["ocr_prepare", "prepare", "eval_base", "sft", "eval_sft", "select", "grpo", "eval_grpo", "report"]
DEFAULTS = {
    "model_type": "qwen3_5",
    "gpus": [0, 1],
    "sft": {"config": "sft.yaml"},
    "grpo": {"config": "grpo_a100x2.yaml", "select": "mine", "candidates": 3000, "count": 1000,
             "hard_fraction": 0.5, "seed": 42,
             "tasks": ["cross_check", "review", "doc_check", "kie", "grounding", "spotting", "relation"], "max_images": 4},
    "eval": {
        "inference_config": "inference.json",
        "concurrency_per_server": 16,
        "port_base": 8000,
        "server_start_timeout_minutes": 40,
        "merge_command": ["swift", "export", "--model", "{model}", "--model_type", "{model_type}",
                          "--adapters", "{adapter}", "--merge_lora", "true", "--output_dir", "{output}"],
        # 질문 하나에 그림 13장까지 (여러 서류), 그림 토큰 ~12000 + 답 4096
        "deploy_command": ["swift", "deploy", "--model", "{model}", "--model_type", "{model_type}",
                           "--infer_backend", "vllm", "--vllm_max_model_len", "20480", "--vllm_max_num_seqs", "32",
                           "--vllm_limit_mm_per_prompt", "{{\"image\": 16}}",  # 중괄호 두 겹: str.format 을 거친다
                           "--vllm_gpu_memory_utilization", "0.9", "--host", "127.0.0.1", "--port", "{port}",
                           "--served_model_name", "docgen", "--enable_thinking", "false", "--max_new_tokens", "4096"],
        "health_path": "/v1/models",
        "compare_models": [],
    },
    "smoke": {"train_steps": 5, "benchmark_per_task": 8, "grpo_candidates": 40, "grpo_count": 8},
}
LABELS = {"start": "출발 모델", "sft": "SFT", "grpo": "GRPO"}


def log(message):
    print(time.strftime("[%Y-%m-%d %H:%M:%S] ") + message, flush=True)


def merged(base, override):
    result = dict(base)
    for key, value in override.items():
        result[key] = merged(base[key], value) if isinstance(value, dict) and isinstance(base.get(key), dict) else value
    return result


class Runner:
    def __init__(self, cfg, config_path, smoke, dry_run):
        self.cfg, self.smoke, self.dry = cfg, smoke, dry_run
        self.config_path = Path(config_path).resolve()
        base = self.config_path.parent
        here = Path(__file__).resolve().parent / "configs"   # 설정 파일 옆에 없으면 train/configs 의 기본 파일
        resolve = lambda p: str((base / p).resolve()) if not Path(p).is_absolute() else p  # noqa: E731

        def resolve_conf(p):
            q = Path(resolve(p))
            return str(q) if q.exists() or Path(p).is_absolute() else str(here / p)
        self.workdir = Path(resolve(cfg["workdir"])) / ("smoke" if smoke else "")
        self.data_cfg = resolve_data(cfg, base)
        ocr = cfg.get("ocr_prepare") or []   # OCR 준비 설정 (선택, 하나 또는 목록)
        self.ocr_configs = [resolve(p) for p in (ocr if isinstance(ocr, list) else [ocr])]
        self.data = Path(self.data_cfg["output_dir"])
        self.model = cfg["model"]
        self.gpus = [str(g) for g in cfg["gpus"]]
        for section in ("sft", "grpo"):
            cfg[section]["config"] = resolve_conf(cfg[section]["config"])
        cfg["eval"]["inference_config"] = resolve_conf(cfg["eval"]["inference_config"])
        os.environ["PYTHONPATH"] = os.pathsep.join([str(ROOT)] + ([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else []))
        self.state_path = self.workdir / "state.json"
        self.state = read_json(self.state_path) if self.state_path.exists() else {"done": [], "timings": {}}
        for d in ("logs", "predictions", "reports", "merged"):
            (self.workdir / d).mkdir(parents=True, exist_ok=True)

    def check_inputs(self):
        """설정의 입력 경로를 단계 시작 전에 한꺼번에 확인한다."""
        d, problems = self.data_cfg, []

        def need(ok, key, path, hint):
            if not ok:
                problems.append(f"  {key}: {path}\n      {hint}")

        need(Path(self.model, "config.json").is_file(), "model", self.model, "출발 모델 폴더 (config.json 이 있는 폴더)")
        ocr_outs = set()
        for conf in self.ocr_configs:
            need(Path(conf).is_file(), "ocr_prepare", conf, "OCR 준비 설정 (docgen/bench/ocr_config.example.json 꼴)")
            if Path(conf).is_file():
                oc, at = read_json(conf), Path(conf).parent
                out = str((at / oc["output_dir"]).resolve())
                ocr_outs.add(out)
                if not Path(out, "DONE.json").is_file():
                    need((at / oc["manifest"]).is_file(), "ocr_prepare → manifest", str((at / oc["manifest"]).resolve()),
                         "이미지 목록 (docgen.bench.ocr_data.scan 으로 만든 manifest.jsonl)")
        if not Path(d["output_dir"], "DONE.json").is_file():   # 섞기가 아직이면 데이터셋을 읽어야 한다
            from .benchmarks import paths as benchmark_paths

            train_paths = [e["path"] if isinstance(e, dict) else e for e in d["train"]]
            for p in [*train_paths, *benchmark_paths(d["benchmark"])]:
                if p in ocr_outs:
                    continue   # ocr_prepare 단계가 만든다
                need(Path(p, "meta.json").is_file() and Path(p, "tasks").is_dir(), "data.train / data.benchmark", p,
                     "studio 데이터셋 폴더 (meta.json + tasks/)")
        if problems:
            sys.exit(f"설정({self.config_path})의 경로를 확인하세요. 상대 경로는 설정 파일이 있는 폴더 기준입니다.\n"
                     + "\n".join(problems))

    # -- helpers -------------------------------------------------------------------------
    def save(self):
        if not self.dry:
            write_json(self.state_path, self.state)

    def run(self, cmd, log_name, env=None):
        log("$ " + " ".join(cmd) + f"   (log: logs/{log_name})")
        if self.dry:
            return
        path = self.workdir / "logs" / log_name
        with path.open("a", encoding="utf-8") as out:
            proc = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=ROOT)
            for line in proc.stdout:
                out.write(line)
                sys.stdout.write(line)
            if proc.wait():
                raise RuntimeError(f"Command failed ({proc.returncode}); see {path}")

    def image_token_budget(self):
        if self.dry and not (self.data / "DONE.json").exists():
            return image_tokens_for([2300, 1600], 32)
        size = read_json(self.data / "DONE.json")["image_max_size"]
        try:
            return image_tokens(self.model, size)[0]
        except (OSError, ValueError) as exc:
            log(f"WARNING: {exc}; assuming 32x32 pixels per visual token")
            return image_tokens_for(size, 32)

    def benchmark_tasks(self):
        tasks = self.data / "benchmark_tasks.jsonl"
        if not self.smoke:
            return tasks
        subset = self.workdir / "benchmark_subset.jsonl"
        if not subset.exists() and not self.dry:
            by_task = {}
            for row in read_jsonl(tasks):
                by_task.setdefault(row["task"], []).append(row)
            n = self.cfg["smoke"]["benchmark_per_task"]
            rows = [r for t in sorted(by_task) for r in random.Random(0).sample(by_task[t], min(n, len(by_task[t])))]
            write_jsonl(subset, rows)
        return subset

    @staticmethod
    def last_checkpoint(output):
        found = [p for p in Path(output).rglob("checkpoint-*") if p.is_dir() and p.name.split("-")[-1].isdigit()]
        if not found:
            raise RuntimeError(f"No checkpoint-* directory under {output}")
        return str(max(found, key=lambda p: (p.stat().st_mtime, int(p.name.split("-")[-1]))))

    @contextmanager
    def serve(self, model_path, name):
        ev = self.cfg["eval"]
        tokens = self.image_token_budget()
        procs, endpoints = [], []
        for i, gpu in enumerate(self.gpus):
            port = ev["port_base"] + i
            with socket.socket() as sock:
                if sock.connect_ex(("127.0.0.1", port)) == 0 and not self.dry:
                    raise RuntimeError(f"Port {port} is already in use; stop the old server so the wrong model is not evaluated")
            cmd = [part.format(model=model_path, model_type=self.cfg["model_type"], port=port) for part in ev["deploy_command"]]
            env = {**os.environ, "CUDA_VISIBLE_DEVICES": gpu, "IMAGE_MAX_TOKEN_NUM": str(tokens),
                   "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"}
            env.pop("NPROC_PER_NODE", None)
            log(f"start server {name} on GPU {gpu}: IMAGE_MAX_TOKEN_NUM={tokens} " + " ".join(cmd))
            endpoints.append(f"http://127.0.0.1:{port}/v1")
            if not self.dry:
                out = (self.workdir / "logs" / f"{name}-server{i}.log").open("w", encoding="utf-8")
                procs.append((subprocess.Popen(cmd, env=env, stdout=out, stderr=subprocess.STDOUT, cwd=ROOT,
                                               start_new_session=True), out, port))
        try:
            deadline = time.monotonic() + ev["server_start_timeout_minutes"] * 60
            for proc, out, port in procs:
                while True:
                    if proc.poll() is not None:
                        raise RuntimeError(f"Server on port {port} exited; see {out.name}")
                    try:
                        with urlopen(f"http://127.0.0.1:{port}{ev['health_path']}", timeout=5) as response:
                            if response.status == 200:
                                break
                    except (URLError, OSError):
                        pass
                    if time.monotonic() > deadline:
                        raise RuntimeError(f"Server on port {port} not ready in time; see {out.name}")
                    time.sleep(3)
                log(f"server on port {port} ready")
            yield ",".join(endpoints)
        finally:
            for proc, out, _ in procs:
                if proc.poll() is None:
                    os.killpg(proc.pid, signal.SIGTERM)
            for proc, out, _ in procs:
                try:
                    proc.wait(timeout=120)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                out.close()

    @staticmethod
    def tag(checkpoint):
        # ms-swift writes <output>/<version>/checkpoint-N; both parts identify one training run.
        return f"{Path(checkpoint).parent.name}-{Path(checkpoint).name}"

    def merge(self, adapter, name):
        output = self.workdir / "merged" / f"{name}-{self.tag(adapter)}"
        if (output / "config.json").exists():
            return str(output)
        cmd = [p.format(model=self.model, model_type=self.cfg["model_type"], adapter=adapter, output=output)
               for p in self.cfg["eval"]["merge_command"]]
        self.run(cmd, f"merge-{name}.log", env={**os.environ, "CUDA_VISIBLE_DEVICES": self.gpus[0]})
        return str(output)

    def predict(self, tasks, endpoints, run_id, out):
        concurrency = self.cfg["eval"]["concurrency_per_server"] * len(self.gpus)
        self.run([sys.executable, "-m", "train.cli", "predict", "--config", self.cfg["eval"]["inference_config"],
                  "--tasks", str(tasks), "--endpoint", endpoints, "--model", "docgen", "--run-id", run_id,
                  "--concurrency", str(concurrency), "--out", str(out)], f"predict-{run_id}.log")

    def evaluate(self, label, model_path, run_id, extra=None):
        role = label if label in LABELS else "other"
        name = LABELS.get(label, label)
        tasks = self.benchmark_tasks()
        # 모델 실행마다 파일 하나: 끊긴 실행은 이어서, 다시 학습한 모델은 새로.
        preds = self.workdir / "predictions" / f"{run_id}.jsonl"
        key = label if label in LABELS else "cmp-" + run_id
        report = self.workdir / "reports" / f"{key}.json"
        with self.serve(model_path, key) as endpoints:
            started = time.monotonic()
            self.predict(tasks, endpoints, run_id, preds)
            log(f"{name} benchmark inference took {(time.monotonic() - started) / 60:.1f} min")
            if extra:
                extra(endpoints)
        if label == "grpo" and not self.dry:
            name = f"{name} {self.tag(self.state['grpo_checkpoint'])}"
        self.run([sys.executable, "-m", "train.cli", "score", "--items", str(self.data / "benchmark_items.jsonl"),
                  "--tasks", str(tasks), "--predictions", str(preds), "--label", name, "--role", role,
                  "--model", str(model_path), "--out", str(report)], f"score-{key}.log")
        self.state[f"report_{key}"] = str(report)
        if label == "grpo" and not self.dry:
            # GRPO 를 다시 돌려도(--from grpo) 앞의 점수를 남겨 보고서에 줄이 늘어난다
            shutil.copy2(report, report.with_name(f"grpo-{self.tag(self.state['grpo_checkpoint'])}.json"))

    def train(self, stage, extra):
        output = self.workdir / stage
        cmd = [sys.executable, "-m", "train.launch", stage, "--config", self.cfg[stage]["config"],
               "--gpus", ",".join(self.gpus), "--model", self.model, "--model-type", self.cfg["model_type"],
               "--data", str(self.data), "--output", str(output), "--execute"] + extra
        if self.smoke:
            cmd += ["--max-steps", str(self.cfg["smoke"]["train_steps"])]
        self.run(cmd, f"train-{stage}.log")
        self.state[f"{stage}_checkpoint"] = "<checkpoint>" if self.dry else self.last_checkpoint(output)
        log(f"{stage} checkpoint: {self.state[f'{stage}_checkpoint']}")

    # -- stages --------------------------------------------------------------------------
    def stage_ocr_prepare(self):
        if not self.ocr_configs:
            log("no ocr_prepare config")
        for n, conf in enumerate(self.ocr_configs):
            out = (Path(conf).parent / read_json(conf)["output_dir"]).resolve() if Path(conf).is_file() else None
            if out and (out / "DONE.json").exists():
                log(f"OCR prepared data exists: {out}")
                continue
            self.run([sys.executable, "-m", "docgen.bench.ocr_prepare", conf], f"ocr_prepare{n or ''}.log")

    def stage_prepare(self):
        if (self.data / "DONE.json").exists():
            log(f"prepared data exists: {self.data}")
            return
        self.run([sys.executable, "-m", "train.cli", "mix", "--config", str(self.config_path)], "prepare.log")

    def stage_eval_base(self):
        for i, m in enumerate(self.cfg["eval"].get("compare_models") or []):
            self.evaluate(m["label"], m["model"], f"compare{i}")
        self.evaluate("start", self.model, "start")

    def stage_sft(self):
        self.train("sft", [])

    def grpo_candidates(self):
        g = self.cfg["grpo"]
        n = self.cfg["smoke"]["grpo_candidates"] if self.smoke else g["candidates"]
        path = self.workdir / "grpo_candidates.jsonl"
        if not path.exists() and not self.dry:
            rows = [r for r in read_jsonl(self.data / "train_grpo.jsonl")
                    if (not g.get("tasks") or r["task"] in g["tasks"])
                    and (not g.get("max_images") or r["n_images"] <= g["max_images"])]
            random.Random(g["seed"]).shuffle(rows)
            write_jsonl(path, rows[:n])
        return path

    def stage_eval_sft(self):
        ckpt = self.state["sft_checkpoint"]
        model = self.merge(ckpt, "sft")

        def mining_predictions(endpoints):
            # 띄운 SFT 서버로 GRPO 후보에도 답해 둔다 (골라 뽑기)
            if self.cfg["grpo"]["select"] == "mine":
                run_id = "sft-grpo-candidates-" + self.tag(ckpt)
                self.predict(self.grpo_candidates(), endpoints, run_id, self.workdir / "predictions" / f"{run_id}.jsonl")
                self.state["grpo_candidate_predictions"] = str(self.workdir / "predictions" / f"{run_id}.jsonl")
        self.evaluate("sft", model, "sft-" + self.tag(ckpt), mining_predictions)

    def stage_select(self):
        g = self.cfg["grpo"]
        count = self.cfg["smoke"]["grpo_count"] if self.smoke else g["count"]
        out = self.workdir / "grpo_train.jsonl"
        if g["select"] == "all":
            self.state["grpo_dataset"] = None
            return
        if g["select"] == "random":
            if not self.dry:
                write_jsonl(out, read_jsonl(self.grpo_candidates())[:count])
        elif g["select"] == "mine":
            self.run([sys.executable, "-m", "train.cli", "mine", "--tasks", str(self.grpo_candidates()),
                      "--predictions", str(self.state.get("grpo_candidate_predictions", "<predictions>")),
                      "--out", str(out), "--count", str(count), "--seed", str(g["seed"]),
                      "--hard-fraction", str(g["hard_fraction"])], "mine.log")
        else:
            raise ValueError("grpo.select must be mine, random or all")
        self.state["grpo_dataset"] = str(out)

    def stage_grpo(self):
        extra = ["--adapter", self.state["sft_checkpoint"]]
        if self.state.get("grpo_dataset"):
            extra += ["--grpo-dataset", self.state["grpo_dataset"]]
        self.train("grpo", extra)

    def stage_eval_grpo(self):
        ckpt = self.state["grpo_checkpoint"]
        self.evaluate("grpo", self.merge(ckpt, "grpo"), "grpo-" + self.tag(ckpt))

    def stage_report(self):
        reports = self.workdir / "reports"
        compare = [reports / f"cmp-compare{i}.json" for i, _ in enumerate(self.cfg["eval"].get("compare_models") or [])]
        grpo = sorted(reports.glob("grpo-*.json"), key=lambda p: p.stat().st_mtime) or [reports / "grpo.json"]
        ordered = [p for p in compare + [reports / "start.json", reports / "sft.json"] + grpo if p.exists() or self.dry]
        self.run([sys.executable, "-m", "train.cli", "report", "--reports", *map(str, ordered),
                  "--out", str(reports / "benchmark.csv")], "report.log")
        log(f"open {reports / 'benchmark.html'}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m train", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", required=True, help="파이프라인 설정 JSON (train/configs/pipeline.example.json)")
    p.add_argument("--from", dest="start", choices=STAGES, help="이 단계와 뒤 단계를 다시")
    p.add_argument("--only", choices=STAGES, help="이 단계만")
    p.add_argument("--smoke", action="store_true", help="5 step 학습·작은 평가 (workdir/smoke)")
    p.add_argument("--dry-run", action="store_true", help="명령만 보여 주고 실행하지 않음")
    a = p.parse_args(argv)
    cfg = merged(DEFAULTS, load_settings(a.config))
    runner = Runner(cfg, a.config, a.smoke, a.dry_run)
    stages = [a.only] if a.only else STAGES[STAGES.index(a.start):] if a.start else STAGES
    if a.start or a.only:
        runner.state["done"] = [s for s in runner.state["done"] if s not in stages]
    if not a.dry_run:
        runner.check_inputs()
    for stage in stages:
        if stage in runner.state["done"]:
            log(f"skip {stage} (done)")
            continue
        log(f"=== {stage} ===")
        started = time.monotonic()
        getattr(runner, "stage_" + stage)()
        hours = (time.monotonic() - started) / 3600
        runner.state["timings"][stage] = round(hours, 3)
        runner.state["done"].append(stage)
        runner.save()
        log(f"=== {stage} done in {hours:.2f} h ===")
    log("timings (h): " + json.dumps(runner.state["timings"]))


if __name__ == "__main__":
    main()
