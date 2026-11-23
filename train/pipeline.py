"""학습 실행 하나: 데이터 준비 → 출발 모델 평가 → SFT → SFT 모델 평가 → 보고서.

  python -m train --config <설정.json> [--smoke | --dry-run | --from <단계> | --only <단계>]

단계 (<workdir>/state.json 에 끝난 것을 적고, 다시 돌리면 이어서):
  prepare      평가 세트 준비 (<cache_dir>/sets/, 같은 세트는 실험끼리 같이 씀) + 학습 데이터 섞기 (data.output_dir)
  eval_start   출발 모델 평가 (같은 모델·같은 평가 세트의 답이 캐시에 있으면 추론 없이)
  sft          SFT (launch.py → ms-swift), 마지막 체크포인트를 적어 둠
  eval_sft     SFT 체크포인트 병합(<workdir>/merged/…)·평가
  report       <workdir>/report.html · answers.html · scores.csv, results.json (python -m train report <workdir> 로 다시)
평가는 GPU 마다 vLLM 서버 하나를 띄우고 요청을 나눠 보낸다 (같은 그림의 질문은 같은 서버로). 여러 모델은 python -m train sweep.

설정 (상대 경로는 설정 파일 기준):
  workdir, cache_dir(기본 <workdir 의 부모>/_cache), model, model_type, template(ms-swift --template, 기본 model_type), gpus,
  data: train · benchmark · output_dir(기본 <workdir>/data) · task_mix · sft_max_examples · image_max_size ·
        max_image_tokens_per_sample · sft_max_length · val_count · pack_turns · seed  (train/mix.py)
  sft:  config(yaml) + yaml 위에 덮어쓸 ms-swift 옵션 (learning_rate, lora_rank …)
  eval: inference_config · concurrency_per_server · port_base · server_start_timeout_minutes · deploy_command · merge_command ·
        fill_from_base  (train/serve.py)
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from docgen.bench.ocr_data import read_json, write_json

from .settings import load_settings, log, merged, pixel_factor

ROOT = Path(__file__).resolve().parents[1]   # 저장소 최상위: 하위 명령은 여기서 python -m train.… 으로
STAGES = ["prepare", "eval_start", "sft", "eval_sft", "report"]
FOLDER_HINT = ("데이터셋 폴더 (meta.json + tasks/): studio 데이터셋, 또는 OCR 준비 결과 폴더 — OCR 준비는 학습 전에 따로 한 번 "
               "python -m docgen.bench.ocr_prepare <설정> (guide/train/ocr.md)")
REMOVED = {"grpo": "GRPO 는 이 브랜치에서 뺐습니다",
           "ocr_prepare": "OCR 준비는 학습 전에 따로 한 번 python -m docgen.bench.ocr_prepare <설정> 으로 하고, 결과 폴더를 data.train·data.benchmark 에 적습니다"}
DEFAULTS = {
    "model_type": "qwen3_5",
    "gpus": [0, 1],
    "sft": {"config": "sft.yaml"},
    "eval": {},
    "smoke": {"train_steps": 5, "benchmark_per_task": 8},
}


def drop_removed(raw: dict) -> dict:
    """없어진 칸(grpo · ocr_prepare · eval.compare_models · eval.skip_start)은 알리고 뺀다."""
    for k in [k for k in raw if k in REMOVED]:
        log(f"WARNING: 설정의 {k} 는 쓰지 않습니다: {REMOVED[k]}")
    ev = {k: v for k, v in (raw.get("eval") or {}).items() if k not in ("compare_models", "skip_start")}
    if len(ev) < len(raw.get("eval") or {}):
        log("WARNING: eval.compare_models · eval.skip_start 는 쓰지 않습니다 (다른 모델 평가는 python -m train eval)")
    return {**{k: v for k, v in raw.items() if k not in REMOVED}, **({"eval": ev} if "eval" in raw else {})}


def resolve(cfg: dict, base: Path) -> dict:
    """설정의 상대 경로를 설정 파일 기준 절대 경로로, 빠진 칸은 기본값으로 (두 번 해도 같다)."""
    from .benchmarks import resolve as res_entries
    from .serve import EVAL_DEFAULTS, conf_path

    def res(p):
        return str((base / p).resolve()) if p and not Path(p).is_absolute() else p

    cfg = merged(DEFAULTS, cfg)
    cfg["eval"] = {**EVAL_DEFAULTS, **cfg["eval"]}
    cfg["workdir"] = res(cfg["workdir"])
    cfg["cache_dir"] = res(cfg.get("cache_dir")) or str(Path(cfg["workdir"]).parent / "_cache")
    cfg["model"] = res(cfg["model"]) if cfg["model"].startswith(".") else cfg["model"]
    d = dict(cfg["data"])
    d["train"] = res_entries(d.get("train") or [], base)
    d["benchmark"] = res_entries(d.get("benchmark") or [], base)
    d["output_dir"] = res(d.get("output_dir")) or str(Path(cfg["workdir"]) / "data")
    cfg["data"] = d
    cfg["sft"] = {**cfg["sft"], "config": conf_path(cfg["sft"]["config"], base)}
    cfg["eval"]["inference_config"] = conf_path(cfg["eval"]["inference_config"], base)
    return cfg


def sh(cmd, log_path, env=None, dry=False):
    """명령을 돌리며 화면과 로그 파일에 같이 쓴다."""
    log("$ " + " ".join(map(str, cmd)) + f"   (log: {log_path})")
    if dry:
        return
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as out:
        # 하위 로그는 한국어: 양쪽 다 UTF-8 (윈도 콘솔 기본값 cp949)
        proc = subprocess.Popen(list(map(str, cmd)), env={**(env or os.environ), "PYTHONIOENCODING": "utf-8"}, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
        for line in proc.stdout:
            out.write(line)
            sys.stdout.write(line)
        if proc.wait():
            raise RuntimeError(f"명령 실패 ({proc.returncode}); see {log_path}")


def benchmark_sets(cfg, dry=False) -> dict:
    """설정의 평가 세트를 준비(또는 캐시에서 찾아) {세트 id: 폴더}. 실험 묶음은 미리 준비해 data.prepared_sets 로 넘긴다."""
    from .benchmarks import normalize
    from .mix import DEFAULTS as MIX, prepare_sets

    d = cfg["data"]
    if d.get("prepared_sets"):
        return d["prepared_sets"]
    size = d.get("image_max_size") or MIX["image_max_size"]
    budget = d.get("max_image_tokens_per_sample") or MIX["max_image_tokens_per_sample"]
    if dry:
        log(f"평가 세트 {len(d['benchmark'])}개 준비 → {Path(cfg['cache_dir']) / 'sets'} (dry run)")
        return {b["id"]: str(Path(cfg["cache_dir"]) / "sets" / b["id"]) for b in normalize(d["benchmark"])}
    return {k: str(v) for k, v in prepare_sets(normalize(d["benchmark"]), cfg["cache_dir"], size, budget,
                                               pixel_factor(cfg["model"]), d.get("workers") or MIX["workers"]).items()}


class Run:
    def __init__(self, cfg, smoke=False, dry=False):
        from .serve import Evaluator

        self.cfg, self.smoke, self.dry = cfg, smoke, dry
        self.workdir = Path(cfg["workdir"]) / ("smoke" if smoke else "")
        self.data = Path(cfg["data"]["output_dir"])
        self.model = cfg["model"]
        self.state_path = self.workdir / "state.json"
        self.state = read_json(self.state_path) if self.state_path.exists() else {"done": [], "timings": {}, "models": {}}
        self.state.setdefault("models", {})
        self.ev = Evaluator(cfg["eval"], cfg["gpus"], self.workdir / "logs", cfg["cache_dir"], dry,
                            cfg["smoke"]["benchmark_per_task"] if smoke else None)
        if not dry:
            self.workdir.mkdir(parents=True, exist_ok=True)

    def check_inputs(self):
        """설정의 입력 경로를 단계 시작 전에 한꺼번에 확인한다."""
        from .benchmarks import normalize, train_entries

        d, problems = self.cfg["data"], []

        def need(ok, key, path, hint):
            if not ok:
                problems.append(f"  {key}: {path}\n      {hint}")

        need(Path(self.model, "config.json").is_file(), "model", self.model, "출발 모델 폴더 (config.json 이 있는 폴더)")
        need(Path(self.cfg["sft"]["config"]).is_file(), "sft.config", self.cfg["sft"]["config"], "ms-swift 학습 설정 yaml")
        benches = normalize(d["benchmark"]) if d.get("benchmark") else []
        need(bool(benches), "data.benchmark", "(비어 있음)", "평가 세트를 하나 이상 적으세요")
        for b in benches:
            for p in b["paths"]:
                ok = Path(p).is_file() if b.get("format") == "swift-fields" else Path(p, "meta.json").is_file() and Path(p, "tasks").is_dir()
                need(ok, f"data.benchmark {b['id']}", p, "swift .jsonl" if b.get("format") else FOLDER_HINT)
        if not (self.data / "DONE.json").is_file():
            for e in train_entries(d["train"]):
                ok = Path(e["path"]).is_file() if e.get("format") == "swift" else \
                    Path(e["path"], "meta.json").is_file() and Path(e["path"], "tasks").is_dir()
                need(ok, "data.train", e["path"], "ms-swift .jsonl" if e.get("format") else FOLDER_HINT)
        if problems:
            sys.exit("설정의 경로를 확인하세요. 상대 경로는 설정 파일이 있는 폴더 기준입니다.\n" + "\n".join(problems))

    def save(self):
        if not self.dry:
            write_json(self.state_path, self.state)

    @staticmethod
    def last_checkpoint(output):
        found = [p for p in Path(output).rglob("checkpoint-*") if p.is_dir() and p.name.split("-")[-1].isdigit()]
        if not found:
            raise RuntimeError(f"No checkpoint-* directory under {output}")
        return str(max(found, key=lambda p: (p.stat().st_mtime, int(p.name.split("-")[-1]))))

    def sets(self):
        if "sets" not in self.state:
            raise SystemExit("평가 세트가 준비되지 않았습니다: prepare 단계부터 돌리세요 (--from prepare)")
        return self.state["sets"]

    # -- 단계 --------------------------------------------------------------------------------
    def stage_prepare(self):
        from .mix import mix

        self.state["sets"] = benchmark_sets(self.cfg, self.dry)
        if (self.data / "DONE.json").exists():
            log(f"섞은 학습 데이터가 있습니다: {self.data}")
            return
        if self.dry:
            log(f"학습 데이터 섞기 → {self.data} (dry run)")
            return
        result = mix({**self.cfg["data"], "output_dir": str(self.data)}, pixel_factor(self.model),
                     list(self.state["sets"].values()), Path(self.cfg["cache_dir"]) / "images")
        log("섞기: " + json.dumps(result, ensure_ascii=False))

    def stage_eval_start(self):
        plan = self.ev.answer(self.model, self.cfg["model_type"], self.sets(), "출발 모델", self.cfg.get("template"))
        self.state["models"]["start"] = {"label": "출발 모델", "model": self.model, "sets": plan}

    def stage_sft(self):
        output = self.workdir / "sft"
        options = {k: v for k, v in self.cfg["sft"].items() if k != "config"}   # yaml 위에 덮어쓸 ms-swift 옵션
        if "sft_max_length" in self.cfg["data"]:   # 섞기가 이 길이에 맞춰 문항을 거른다
            options.setdefault("max_length", self.cfg["data"]["sft_max_length"])
        cmd = [sys.executable, "-m", "train.launch", "--config", self.cfg["sft"]["config"], "--gpus", ",".join(map(str, self.cfg["gpus"])),
               "--model", self.model, "--model-type", self.cfg["model_type"], "--data", str(self.data), "--output", str(output), "--execute"]
        if self.cfg.get("template"):
            cmd += ["--template", self.cfg["template"]]
        if options:
            cmd += ["--options", json.dumps(options, ensure_ascii=False)]
        if self.smoke:
            cmd += ["--max-steps", str(self.cfg["smoke"]["train_steps"])]
        env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(ROOT)] + ([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else []))}
        sh(cmd, self.workdir / "logs" / "train-sft.log", env, self.dry)
        self.state["sft_checkpoint"] = "<checkpoint>" if self.dry else self.last_checkpoint(output)
        log(f"SFT 체크포인트: {self.state['sft_checkpoint']}")

    def stage_eval_sft(self):
        ckpt = self.state["sft_checkpoint"]
        tag = f"{Path(ckpt).parent.name}-{Path(ckpt).name}"   # ms-swift: <output>/<version>/checkpoint-N
        model = self.ev.merge(self.model, self.cfg["model_type"], ckpt, self.workdir / "merged" / f"sft-{tag}",
                              self.workdir / "logs" / "merge-sft.log", self.cfg.get("template"))
        plan = self.ev.answer(model, self.cfg["model_type"], self.sets(), "SFT", self.cfg.get("template"))
        self.state["models"]["sft"] = {"label": "SFT", "model": model, "checkpoint": ckpt, "sets": plan}

    def results(self):
        models = [self.state["models"][k] for k in ("start", "sft") if k in self.state["models"]]
        return {"name": Path(self.cfg["workdir"]).name, "about": self.cfg.get("about") or "학습 실행 (출발 모델 → SFT)",
                "baseline": "출발 모델", "models": models}

    def stage_report(self):
        from .report import write_safe

        if self.dry:
            return
        write_json(self.workdir / "results.json", self.results())
        if not self.cfg.get("sweep"):   # 실험 묶음은 묶음 보고서 하나만 만든다
            write_safe(self.results(), self.workdir)


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m train", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", required=True, help="학습 설정 JSON (train/configs/pipeline.example.json)")
    pick = p.add_mutually_exclusive_group()
    pick.add_argument("--from", dest="start", choices=STAGES, help="이 단계와 뒤 단계를 다시")
    pick.add_argument("--only", choices=STAGES, help="이 단계만")
    p.add_argument("--smoke", action="store_true", help="리허설: 5 step 학습, 평가 세트·과제마다 8문항 (workdir/smoke)")
    p.add_argument("--dry-run", action="store_true", help="명령만 보여 주고 실행하지 않음")
    a = p.parse_args(argv)
    path = Path(a.config).resolve()
    cfg = resolve(drop_removed(load_settings(path)), path.parent)
    run = Run(cfg, a.smoke, a.dry_run)
    stages = [a.only] if a.only else STAGES[STAGES.index(a.start):] if a.start else STAGES
    if a.start or a.only:
        run.state["done"] = [s for s in run.state["done"] if s not in stages]
    run.state["done"] = [s for s in run.state["done"] if s != "report"]   # 보고서는 늘 다시
    if not a.dry_run:
        run.check_inputs()
        write_json(run.workdir / "config.json", cfg)   # 실제로 쓴 설정 (절대 경로)
    for stage in stages:
        if stage in run.state["done"]:
            log(f"skip {stage} (done)")
            continue
        log(f"=== {stage} ===")
        started = time.monotonic()
        getattr(run, "stage_" + stage)()
        hours = (time.monotonic() - started) / 3600
        run.state["timings"][stage] = round(hours, 3)
        run.state["done"].append(stage)
        run.save()
        log(f"=== {stage} done in {hours:.2f} h ===")
    log("timings (h): " + json.dumps(run.state["timings"]))


if __name__ == "__main__":
    main()
