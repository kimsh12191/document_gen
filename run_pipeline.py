"""One command from prepared OCR to the Base/SFT/GRPO comparison report.

Stages (in order; each is skipped once recorded as done in <workdir>/state.json):
  prepare     build data/prepared-* from the manifest (saved OCR JSON or the OCR adapter)
  eval_base   serve the base model on every GPU, predict + evaluate the benchmark
  sft         SFT training (train.py), records the last checkpoint
  eval_sft    merge + serve the SFT model, evaluate; also predicts GRPO candidates for mining
  select      choose the GRPO training rows (mine / random / all)
  grpo        GRPO training from the SFT checkpoint
  eval_grpo   merge + serve the GRPO model, evaluate
  report      benchmark_report.py -> reports/benchmark.{csv,md,html}

Evaluation runs one inference server per GPU and spreads requests over them; questions
about the same image go to the same server so its image prefix cache is reused.

  python run_pipeline.py --config configs/pipeline.json            # everything
  python run_pipeline.py --config configs/pipeline.json --smoke    # 5-step / small-eval rehearsal
  python run_pipeline.py --config configs/pipeline.json --from sft # redo sft and later stages
  python run_pipeline.py --config configs/pipeline.json --dry-run  # print commands only
"""
import argparse
import json
import os
import random
import signal
import socket
import subprocess
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from bank_ocr.cli import image_tokens, image_tokens_for, mine
from bank_ocr.data import read_json, read_jsonl, write_json, write_jsonl
from bank_ocr.settings import load_settings

ROOT = Path(__file__).resolve().parent
STAGES = ["prepare", "eval_base", "sft", "eval_sft", "select", "grpo", "eval_grpo", "report"]
DEFAULTS = {
    "model_type": "qwen3_5",
    "gpus": [0, 1],
    "sft": {"config": "configs/sft.yaml"},
    "grpo": {"config": "configs/grpo_a100x2.yaml", "select": "mine", "candidates": 6000, "count": 2000,
             "hard_fraction": 0.5, "seed": 42},
    "eval": {
        "inference_config": "configs/inference.json",
        "concurrency_per_server": 32,
        "port_base": 8000,
        "server_start_timeout_minutes": 40,
        "merge_command": ["swift", "export", "--model", "{model}", "--model_type", "{model_type}",
                          "--adapters", "{adapter}", "--merge_lora", "true", "--output_dir", "{output}"],
        "deploy_command": ["swift", "deploy", "--model", "{model}", "--model_type", "{model_type}",
                           "--infer_backend", "vllm", "--vllm_max_model_len", "10240", "--vllm_max_num_seqs", "64",
                           "--vllm_gpu_memory_utilization", "0.9", "--host", "127.0.0.1", "--port", "{port}",
                           "--served_model_name", "bank-ocr", "--enable_thinking", "false", "--max_new_tokens", "2048"],
        "health_path": "/v1/models",
    },
    "smoke": {"train_steps": 5, "benchmark_rows": 60, "grpo_candidates": 40, "grpo_count": 8},
}


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
        base = Path(config_path).resolve().parent
        resolve = lambda p: str((base / p).resolve()) if not Path(p).is_absolute() else p
        self.workdir = Path(resolve(cfg["workdir"])) / ("smoke" if smoke else "")
        self.data_config = Path(resolve(cfg["data_config"]))
        data_cfg = read_json(self.data_config)
        self.data = (self.data_config.parent / data_cfg["output_dir"]).resolve()
        self.model = cfg["model"]
        self.gpus = [str(g) for g in cfg["gpus"]]
        for section in ("sft", "grpo"):
            cfg[section]["config"] = resolve(cfg[section]["config"])
        cfg["eval"]["inference_config"] = resolve(cfg["eval"]["inference_config"])
        self.state_path = self.workdir / "state.json"
        self.state = read_json(self.state_path) if self.state_path.exists() else {"done": [], "timings": {}}
        for d in ("logs", "predictions", "reports", "merged"):
            (self.workdir / d).mkdir(parents=True, exist_ok=True)

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
            rows = read_jsonl(tasks)
            random.Random(0).shuffle(rows)
            write_jsonl(subset, rows[:self.cfg["smoke"]["benchmark_rows"]])
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
        self.run([sys.executable, "-m", "bank_ocr", "predict", "--config", self.cfg["eval"]["inference_config"],
                  "--tasks", str(tasks), "--endpoint", endpoints, "--model", "bank-ocr", "--run-id", run_id,
                  "--concurrency", str(concurrency), "--out", str(out)], f"predict-{run_id}.log")

    def evaluate(self, label, model_path, run_id, extra=None):
        tasks = self.benchmark_tasks()
        # One file per model run: an interrupted run resumes, a retrained model starts fresh.
        preds = self.workdir / "predictions" / f"{run_id}.jsonl"
        report = self.workdir / "reports" / f"{label.lower()}.json"
        with self.serve(model_path, label.lower()) as endpoints:
            started = time.monotonic()
            self.predict(tasks, endpoints, run_id, preds)
            log(f"{label} benchmark inference took {(time.monotonic() - started) / 60:.1f} min")
            if extra:
                extra(endpoints)
        self.run([sys.executable, "-m", "bank_ocr", "evaluate", "--tasks", str(tasks), "--predictions", str(preds),
                  "--label", label, "--out", str(report)], f"evaluate-{label.lower()}.log")
        self.state[f"report_{label.lower()}"] = str(report)

    def train(self, stage, extra):
        output = self.workdir / stage
        cmd = [sys.executable, str(ROOT / "train.py"), stage, "--config", self.cfg[stage]["config"],
               "--gpus", ",".join(self.gpus), "--model", self.model, "--model-type", self.cfg["model_type"],
               "--data", str(self.data), "--output", str(output), "--execute"] + extra
        if self.smoke:
            cmd += ["--max-steps", str(self.cfg["smoke"]["train_steps"])]
        self.run(cmd, f"train-{stage}.log")
        self.state[f"{stage}_checkpoint"] = "<checkpoint>" if self.dry else self.last_checkpoint(output)
        log(f"{stage} checkpoint: {self.state[f'{stage}_checkpoint']}")

    # -- stages --------------------------------------------------------------------------
    def stage_prepare(self):
        if (self.data / "DONE.json").exists():
            log(f"prepared data exists: {self.data}")
            return
        self.run([sys.executable, "-m", "bank_ocr", "prepare", "--config", str(self.data_config)], "prepare.log")

    def stage_eval_base(self):
        self.evaluate("Base", self.model, "base")

    def stage_sft(self):
        self.train("sft", [])

    def grpo_candidates(self):
        g = self.cfg["grpo"]
        n = self.cfg["smoke"]["grpo_candidates"] if self.smoke else g["candidates"]
        path = self.workdir / "grpo_candidates.jsonl"
        if not path.exists() and not self.dry:
            rows = read_jsonl(self.data / "train_grpo.jsonl")
            random.Random(g["seed"]).shuffle(rows)
            write_jsonl(path, rows[:n])
        return path

    def stage_eval_sft(self):
        ckpt = self.state["sft_checkpoint"]
        model = self.merge(ckpt, "sft")
        def mining_predictions(endpoints):
            # Reuse the running SFT servers to score GRPO candidates for mining.
            if self.cfg["grpo"]["select"] == "mine":
                run_id = "sft-grpo-candidates-" + self.tag(ckpt)
                self.predict(self.grpo_candidates(), endpoints, run_id, self.workdir / "predictions" / f"{run_id}.jsonl")
                self.state["grpo_candidate_predictions"] = str(self.workdir / "predictions" / f"{run_id}.jsonl")
        self.evaluate("SFT", model, "sft-" + self.tag(ckpt), mining_predictions)

    def stage_select(self):
        g = self.cfg["grpo"]
        count = self.cfg["smoke"]["grpo_count"] if self.smoke else g["count"]
        out = self.workdir / "grpo_train.jsonl"
        if g["select"] == "all":
            self.state["grpo_dataset"] = None
            return
        if self.dry:
            log(f"select GRPO rows ({g['select']}, count={count}) -> {out}")
        elif g["select"] == "random":
            rows = read_jsonl(self.grpo_candidates())
            write_jsonl(out, rows[:count])
        elif g["select"] == "mine":
            result = mine(self.grpo_candidates(), self.state["grpo_candidate_predictions"],
                          out, count, g["seed"], g["hard_fraction"])
            log(f"mined GRPO rows: {result}")
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
        self.evaluate("GRPO", self.merge(ckpt, "grpo"), "grpo-" + self.tag(ckpt))

    def stage_report(self):
        reports = self.workdir / "reports"
        self.run([sys.executable, str(ROOT / "benchmark_report.py"), "--base", str(reports / "base.json"),
                  "--sft", str(reports / "sft.json"), "--grpo", str(reports / "grpo.json"),
                  "--out", str(reports / "benchmark.csv")], "report.log")
        log(f"open {reports / 'benchmark.html'}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", required=True, help="Pipeline JSON (see configs/pipeline.example.json)")
    p.add_argument("--from", dest="start", choices=STAGES, help="Re-run this stage and every later stage")
    p.add_argument("--only", choices=STAGES, help="Run just this stage")
    p.add_argument("--smoke", action="store_true", help="5 training steps, small evaluation; separate workdir/smoke")
    p.add_argument("--dry-run", action="store_true", help="Print the commands without running anything")
    a = p.parse_args()
    cfg = merged(DEFAULTS, load_settings(a.config))
    runner = Runner(cfg, a.config, a.smoke, a.dry_run)
    stages = [a.only] if a.only else STAGES[STAGES.index(a.start):] if a.start else STAGES
    if a.start or a.only:
        runner.state["done"] = [s for s in runner.state["done"] if s not in stages]
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
