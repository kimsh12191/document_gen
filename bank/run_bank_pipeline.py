"""Banking tasks on top of the OCR model: one command from docgen data to the comparison report.

Starts from the OCR stage's result (a merged model folder, e.g. ../ocr/runs/exp1/merged/grpo-...) and
trains the docgen banking tasks: document check, cross-document consistency, review questions,
plus extraction / classification / marks. Uses the same machinery as ../ocr/run_pipeline.py (one vLLM
server per GPU, LoRA merge, ../ocr/train.py, state.json resume); only data, scoring and the report differ.

Stages (each recorded in <workdir>/state.json; a re-run continues where it stopped):
  prepare     docgen output (built once in the docgen container) -> data/prepared-bank
  eval_base   benchmark the start model (and any eval.compare_models)
  sft         SFT from the start model on the docgen training data (+ OCR replay)
  eval_sft    merge + benchmark the SFT model; also answers GRPO candidates for mining
  select      choose GRPO rows (mine / random / all)
  grpo        GRPO from the SFT checkpoint, reward = the benchmark's own scorer
  eval_grpo   merge + benchmark the GRPO model
  report      reports/benchmark.{csv,md,html} (+ reports/ocr_retention.* when ocr_check is set)

Run from bank/ (setup and config keys: README.md):
  python run_bank_pipeline.py --config configs/bank_pipeline.json --smoke    # rehearsal
  python run_bank_pipeline.py --config configs/bank_pipeline.json            # everything
  python run_bank_pipeline.py --config configs/bank_pipeline.json --from grpo
"""
import argparse
import json
import os
import random
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent     # bank/
OCR = ROOT.parent / "ocr"                  # 1부 OCR 코드: bank_ocr, run_pipeline.py, train.py
sys.path[:0] = [p for p in (str(ROOT), str(OCR)) if p not in sys.path]

from bank_ocr.data import read_json, read_jsonl, write_jsonl  # noqa: E402
from bank_ocr.settings import load_settings  # noqa: E402
from bank_task.cli import resolve_data  # noqa: E402
from run_pipeline import DEFAULTS as OCR_DEFAULTS, STAGES, Runner, log, merged  # noqa: E402
DEFAULTS = merged(OCR_DEFAULTS, {
    "sft": {"config": "configs/bank_sft.yaml"},
    "grpo": {"config": "configs/bank_grpo_a100x2.yaml", "select": "mine", "candidates": 3000, "count": 1000,
             "hard_fraction": 0.5, "seed": 42, "tasks": ["cross_check", "review", "doc_check", "kie"],
             "max_images": 4},
    "eval": {
        "inference_config": "configs/bank_inference.json",
        # Up to 13 images per question: allow them, and room for ~12000 image tokens + a 4096-token answer.
        "deploy_command": ["swift", "deploy", "--model", "{model}", "--model_type", "{model_type}",
                           "--infer_backend", "vllm", "--vllm_max_model_len", "20480", "--vllm_max_num_seqs", "32",
                           "--vllm_limit_mm_per_prompt", "{{\"image\": 16}}",  # braces doubled: parts go through str.format
                           "--vllm_gpu_memory_utilization", "0.9", "--host", "127.0.0.1", "--port", "{port}",
                           "--served_model_name", "bank-ocr", "--enable_thinking", "false", "--max_new_tokens", "4096"],
        "concurrency_per_server": 16,
        "compare_models": [],
    },
    "ocr_check": None,
    "smoke": {"train_steps": 5, "benchmark_per_task": 8, "ocr_rows": 30, "grpo_candidates": 40, "grpo_count": 8},
})
LABELS = {"start": "출발(OCR) 모델", "sft": "은행 SFT", "grpo": "은행 GRPO"}


class BankRunner(Runner):
    def __init__(self, cfg, config_path, smoke, dry_run):
        self.cfg, self.smoke, self.dry = cfg, smoke, dry_run
        self.config_path = Path(config_path).resolve()
        base = self.config_path.parent
        resolve = lambda p: str((base / p).resolve()) if not Path(p).is_absolute() else p
        self.workdir = Path(resolve(cfg["workdir"])) / ("smoke" if smoke else "")
        self.data_cfg = resolve_data(cfg, base)
        self.data = Path(self.data_cfg["output_dir"])
        self.model = cfg["model"]
        self.gpus = [str(g) for g in cfg["gpus"]]
        for section in ("sft", "grpo"):
            cfg[section]["config"] = resolve(cfg[section]["config"])
        cfg["eval"]["inference_config"] = resolve(cfg["eval"]["inference_config"])
        if cfg.get("ocr_check"):
            cfg["ocr_check"]["tasks"] = resolve(cfg["ocr_check"]["tasks"])
        # docgen (scoring, GRPO reward) and this project must be importable in every subprocess,
        # including the distributed training workers that load bank_task_reward.py.
        docgen = self.data_cfg.get("docgen_root")
        if docgen:
            os.environ["DOCGEN_ROOT"] = docgen
        os.environ["PYTHONPATH"] = os.pathsep.join(
            [str(ROOT), str(OCR)] + ([docgen] if docgen else []) + ([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else []))
        self.state_path = self.workdir / "state.json"
        self.state = read_json(self.state_path) if self.state_path.exists() else {"done": [], "timings": {}}
        for d in ("logs", "predictions", "reports", "merged"):
            (self.workdir / d).mkdir(parents=True, exist_ok=True)

    def check_inputs(self):
        """Every input path in the config, checked before any stage runs; all problems at once."""
        d, problems = self.data_cfg, []

        def need(ok, key, path, hint):
            if not ok:
                problems.append(f"  {key}: {path}\n      {hint}")

        need(Path(self.model, "config.json").is_file(), "model", self.model,
             "OCR 단계 병합 모델 폴더 (config.json 이 있는 폴더, 예: runs/exp1/merged/grpo-…-checkpoint-500)")
        root = d.get("docgen_root")
        need(bool(root) and Path(root, "docgen", "bench").is_dir(), "data.docgen_root", root,
             "docgen/ 폴더가 들어 있는 저장소 최상위")
        if not Path(d["output_dir"], "DONE.json").is_file():  # prepare still has to read the docgen output
            for p in d["train"]:
                need(Path(p, "meta.json").is_file(), "data.train", p, "docgen 학습 데이터 폴더 (make_bank_data.sh 의 bank_train)")
            need(Path(d["benchmark"] or "", "meta.json").is_file(), "data.benchmark", d["benchmark"],
                 "docgen 평가 세트 폴더 (make_bank_data.sh 의 bench)")
            if d.get("replay"):
                need(Path(d["replay"]["path"]).is_file(), "data.replay.path", d["replay"]["path"],
                     "OCR 단계 prepare 결과의 train_sft.jsonl. OCR 데이터를 섞지 않으려면 \"replay\": null")
        if self.cfg.get("ocr_check"):
            need(Path(self.cfg["ocr_check"]["tasks"]).is_file(), "ocr_check.tasks", self.cfg["ocr_check"]["tasks"],
                 "OCR 단계 prepare 결과의 benchmark_tasks.jsonl. OCR 유지 확인을 안 하려면 \"ocr_check\": null")
        if problems:
            sys.exit(f"설정({self.config_path})의 경로를 확인하세요. 상대 경로는 설정 파일이 있는 폴더 기준입니다.\n"
                     + "\n".join(problems))

    # -- benchmark ---------------------------------------------------------------------------
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

    def ocr_check_tasks(self):
        oc = self.cfg.get("ocr_check")
        if not oc:
            return None
        path = self.workdir / "ocr_check_tasks.jsonl"
        if not path.exists() and not self.dry:
            rows = read_jsonl(oc["tasks"])
            random.Random(oc.get("seed", 0)).shuffle(rows)
            write_jsonl(path, rows[:self.cfg["smoke"]["ocr_rows"] if self.smoke else oc.get("rows", 1000)])
        return path

    def evaluate(self, label, model_path, run_id, extra=None):
        role = label if label in LABELS else "other"
        name = LABELS.get(label, label)
        tasks, ocr_tasks = self.benchmark_tasks(), self.ocr_check_tasks()
        preds = self.workdir / "predictions" / f"{run_id}.jsonl"
        ocr_preds = self.workdir / "predictions" / f"{run_id}-ocr.jsonl"
        key = label if label in LABELS else "cmp-" + run_id
        report = self.workdir / "reports" / f"{key}.json"
        with self.serve(model_path, key) as endpoints:
            started = time.monotonic()
            self.predict(tasks, endpoints, run_id, preds)
            log(f"{name} benchmark inference took {(time.monotonic() - started) / 60:.1f} min")
            if ocr_tasks:
                self.predict(ocr_tasks, endpoints, run_id + "-ocr", ocr_preds)
            if extra:
                extra(endpoints)
        if label == "grpo":
            name = f"{name} {self.tag(self.state['grpo_checkpoint'])}" if not self.dry else name
        self.run([sys.executable, "-m", "bank_task", "score", "--items", str(self.data / "benchmark_items.jsonl"),
                  "--tasks", str(tasks), "--predictions", str(preds), "--label", name, "--role", role,
                  "--model", str(model_path), "--out", str(report)], f"score-{key}.log")
        if ocr_tasks:
            self.run([sys.executable, "-m", "bank_ocr", "evaluate", "--tasks", str(ocr_tasks), "--predictions",
                      str(ocr_preds), "--label", name, "--out", str(report.with_name(f"ocr-{key}.json"))],
                     f"evaluate-ocr-{key}.log")
        if label == "grpo" and not self.dry:
            # Every GRPO run keeps its scores, so a re-run (--from grpo) adds a row instead of replacing one.
            tag = self.tag(self.state["grpo_checkpoint"])
            shutil.copy2(report, report.with_name(f"grpo-{tag}.json"))
            if ocr_tasks:
                shutil.copy2(report.with_name("ocr-grpo.json"), report.with_name(f"ocr-grpo-{tag}.json"))

    # -- stages ------------------------------------------------------------------------------
    def stage_prepare(self):
        if (self.data / "DONE.json").exists():
            log(f"prepared data exists: {self.data}")
            return
        self.run([sys.executable, "-m", "bank_task", "prepare", "--config", str(self.config_path)], "prepare.log")

    def stage_eval_base(self):
        for i, m in enumerate(self.cfg["eval"].get("compare_models") or []):
            self.evaluate(m["label"], m["model"], f"compare{i}")
        self.evaluate("start", self.model, "start")

    def stage_sft(self):
        self.train("sft", [])

    def stage_eval_sft(self):
        ckpt = self.state["sft_checkpoint"]
        model = self.merge(ckpt, "sft")

        def mining_predictions(endpoints):
            if self.cfg["grpo"]["select"] == "mine":
                run_id = "sft-grpo-candidates-" + self.tag(ckpt)
                self.predict(self.grpo_candidates(), endpoints, run_id, self.workdir / "predictions" / f"{run_id}.jsonl")
                self.state["grpo_candidate_predictions"] = str(self.workdir / "predictions" / f"{run_id}.jsonl")
        self.evaluate("sft", model, "sft-" + self.tag(ckpt), mining_predictions)

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
            self.run([sys.executable, "-m", "bank_task", "mine", "--tasks", str(self.grpo_candidates()),
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
        cmd = [sys.executable, "-m", "bank_task", "report", "--reports", *map(str, ordered),
               "--out", str(reports / "benchmark.csv")]
        ocr = [p.with_name("ocr-" + p.name) for p in ordered]
        ocr = [p for p in ocr if p.exists() or self.dry]
        if self.cfg.get("ocr_check") and ocr:
            labels = [read_json(p)["label"] if p.exists() else p.stem for p in ordered if p.with_name("ocr-" + p.name) in ocr]
            cmd += ["--ocr-reports", *map(str, ocr), "--ocr-labels", *labels, "--ocr-out", str(reports / "ocr_retention.csv")]
        self.run(cmd, "report.log")
        log(f"open {reports / 'benchmark.html'}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", required=True, help="Pipeline JSON (see configs/bank_pipeline.example.json)")
    p.add_argument("--from", dest="start", choices=STAGES, help="Re-run this stage and every later stage")
    p.add_argument("--only", choices=STAGES, help="Run just this stage")
    p.add_argument("--smoke", action="store_true", help="5 training steps, small evaluation; separate workdir/smoke")
    p.add_argument("--dry-run", action="store_true", help="Print the commands without running anything")
    a = p.parse_args()
    cfg = merged(DEFAULTS, load_settings(a.config))
    runner = BankRunner(cfg, a.config, a.smoke, a.dry_run)
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
