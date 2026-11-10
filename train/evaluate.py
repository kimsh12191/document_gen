"""학습 없이 평가만: 모델 경로 목록 × 평가 세트 → 보고서 (python -m train eval).

  python -m train eval --config <평가.json> [--smoke | --dry-run]

평가 설정 (상대 경로는 이 파일 기준):
  {"name": "E03-po", "about": "실서류 매입추심에서 a2·a5 비교", "root": "../runs/E03-po",
   "base": "pipeline.json",                       (선택) 이 학습 설정의 평가 세트·gpus·model_type·eval·그림 예산·cache_dir 를 물려받음
   "gpus": [0, 1], "model_type": "qwen3_5", "baseline": "a2",
   "models": [{"label": "base", "path": "/share/cv_share/qwen3.5/9b"},
              {"label": "a2", "path": "../runs/E02-tune/a2/merged/sft-v0-…-checkpoint-500", "about": "…"},
              {"label": "a5-ckpt", "path": "../runs/E02-tune/a5/sft/v0-…/checkpoint-300"},   LoRA 체크포인트면 합쳐서 평가
              {"sweep": "../runs/E02-tune"}],      실험 묶음(또는 학습 실행) 결과 폴더: 그 모델들을 그 label 로 모두
   "benchmark": [{"id": "real_po_kie", "name": "실서류 매입추심", "group": "real", "format": "swift-fields", "gt": "reviewed",
                  "paths": ["/share/…/eval_qa_PO.kie.jsonl"], "scorer": "../scorers/swift_kie_scorer.py:score"}]}
- benchmark 를 적으면 그것만, 안 적으면 base 의 data.benchmark. 꼴은 학습 설정의 data.benchmark 와 같다 (train/benchmarks.py).
- 모델마다 model_type 을 따로 적을 수 있다. LoRA 체크포인트(adapter_config.json)는 "base_model"(없으면 체크포인트에 적힌 것)과
  합쳐 <root>/merged/<label>/ 에 두고 평가한다.
- 같은 모델·같은 평가 세트의 답이 cache_dir 에 있으면 추론하지 않는다 (학습 때 낸 답도). 모델·세트를 더해 다시 치면 새 것만 돈다.
- 결과: <root>/report.html · answers.html(두 모델 골라 견주기) · scores.csv · results.json. 모델 하나 끝날 때마다 다시 만든다.
"""
import argparse
import json
from pathlib import Path

from docgen.bench.ocr_data import read_json, write_json

from .settings import load_settings, log, pixel_factor

KEYS = {"name", "about", "record", "root", "base", "gpus", "model_type", "baseline", "models", "benchmark", "cache_dir",
        "image_max_size", "max_image_tokens_per_sample", "eval", "smoke"}


def load(path):
    from .benchmarks import normalize, resolve as res_entries
    from .pipeline import resolve as resolve_pipeline
    from .serve import EVAL_DEFAULTS, conf_path

    path = Path(path).resolve()
    here = path.parent
    raw = load_settings(path)
    unknown = set(raw) - KEYS
    if unknown:
        raise ValueError(f"모르는 칸 {sorted(unknown)} (쓸 수 있는 칸: {', '.join(sorted(KEYS))})")
    for k in ("name", "about", "root", "models"):
        if not raw.get(k):
            raise ValueError(f"평가 설정에 {k} 가 없습니다")
    cfg = {"gpus": [0, 1], "model_type": "qwen3_5", "eval": dict(EVAL_DEFAULTS), "smoke": {"benchmark_per_task": 8}}
    if raw.get("base"):   # 학습 설정에서 물려받기
        bpath = (here / raw["base"]).resolve()
        b = load_settings(bpath)
        b = resolve_pipeline({**{k: v for k, v in b.items() if k != "grpo"}, "workdir": b.get("workdir") or "."}, bpath.parent)
        cfg.update({k: b[k] for k in ("gpus", "model_type", "eval")})
        cfg["benchmark"] = b["data"]["benchmark"]
        cfg["image_max_size"] = b["data"].get("image_max_size")
        cfg["max_image_tokens_per_sample"] = b["data"].get("max_image_tokens_per_sample")
        if load_settings(bpath).get("cache_dir"):
            cfg["cache_dir"] = b["cache_dir"]
    for k in ("name", "about", "record", "gpus", "model_type", "baseline", "image_max_size", "max_image_tokens_per_sample"):
        if raw.get(k) is not None:
            cfg[k] = raw[k]
    if raw.get("eval"):
        cfg["eval"] = {**cfg["eval"], **raw["eval"]}
        if raw["eval"].get("inference_config"):
            cfg["eval"]["inference_config"] = conf_path(raw["eval"]["inference_config"], here)
    cfg["eval"]["inference_config"] = conf_path(cfg["eval"]["inference_config"], here)
    if raw.get("benchmark"):
        cfg["benchmark"] = res_entries(raw["benchmark"], here)
    if not cfg.get("benchmark"):
        raise ValueError("평가 세트가 없습니다: benchmark 를 적거나 base 에 data.benchmark 가 있는 학습 설정을 주세요")
    cfg["benchmark"] = normalize(cfg["benchmark"])
    cfg["root"] = str((here / raw["root"]).resolve())
    cfg["cache_dir"] = str((here / raw["cache_dir"]).resolve()) if raw.get("cache_dir") else cfg.get("cache_dir") or str(Path(cfg["root"]).parent / "_cache")
    cfg["models"] = models_of(raw["models"], here, cfg["model_type"])
    labels = [m["label"] for m in cfg["models"]]
    dup = sorted({x for x in labels if labels.count(x) > 1})
    if dup:
        raise ValueError(f"모델 label 이 겹칩니다: {dup} (묶음에서 가져온 모델과 겹치면 직접 적은 쪽 label 을 바꾸세요)")
    if cfg.get("baseline") and cfg["baseline"] not in labels:
        raise ValueError(f"baseline 은 models 의 label 이어야 합니다: {cfg['baseline']} (있는 것: {labels})")
    return cfg


def models_of(entries, here: Path, model_type):
    out = []
    for e in entries:
        if not isinstance(e, dict):
            raise ValueError(f"models 의 칸은 {{\"label\", \"path\"}} 또는 {{\"sweep\": 결과 폴더}} 입니다: {e}")
        if e.get("sweep"):
            folder = (here / e["sweep"]).resolve()
            if not (folder / "results.json").is_file():
                raise ValueError(f"{folder} 에 results.json 이 없습니다 (실험 묶음 root 또는 학습 실행 workdir, 끝난 모델이 있어야 함)")
            res = read_json(folder / "results.json")
            for m in res["models"]:
                out.append({"label": m["label"], "path": m["model"], "about": f"{res['name']}: {m.get('about') or ''}".strip(": "),
                            "model_type": model_type, "checkpoint": m.get("checkpoint"), "changes": m.get("changes"),
                            "train": m.get("train")})
            continue
        if not e.get("label") or not e.get("path"):
            raise ValueError(f"models 의 칸에 label·path 가 있어야 합니다: {e}")
        p = Path(e["path"]) if Path(e["path"]).is_absolute() else (here / e["path"]).resolve()
        out.append({"label": e["label"], "path": str(p), "about": e.get("about") or "", "model_type": e.get("model_type") or model_type,
                    **({"base_model": e["base_model"]} if e.get("base_model") else {})})
    return out


def check(cfg):
    problems = []
    for m in cfg["models"]:
        p = Path(m["path"])
        if not (p / "config.json").is_file() and not (p / "adapter_config.json").is_file():
            problems.append(f"{m['label']}: 모델 폴더(config.json) 도 LoRA 체크포인트(adapter_config.json) 도 아닙니다: {p}")
    for b in cfg["benchmark"]:
        for p in b["paths"]:
            ok = Path(p).is_file() if b.get("format") == "swift-fields" else (Path(p) / "meta.json").is_file() and (Path(p) / "tasks").is_dir()
            if not ok:
                problems.append(f"benchmark {b['id']}: 경로가 없습니다: {p}")
    if problems:
        raise SystemExit("평가 설정을 확인하세요:\n  " + "\n  ".join(problems))


def model_dir(m, cfg, ev):
    """LoRA 체크포인트면 합친 폴더, 아니면 그대로."""
    p = Path(m["path"])
    if (p / "config.json").is_file() or not (p / "adapter_config.json").is_file():
        return str(p)
    base = m.get("base_model") or json.loads((p / "adapter_config.json").read_text(encoding="utf-8")).get("base_model_name_or_path")
    if not base or not (Path(base) / "config.json").is_file():
        raise SystemExit(f"{m['label']}: LoRA 체크포인트의 출발 모델을 찾지 못했습니다 ({base}). 모델 칸에 \"base_model\" 을 적으세요")
    root = Path(cfg["root"])
    return ev.merge(base, m["model_type"], str(p), root / "merged" / m["label"], root / "logs" / f"merge-{m['label']}.log")


def run(path, smoke=False, dry=False):
    from .mix import DEFAULTS as MIX, prepare_sets
    from .report import write_safe
    from .serve import Evaluator

    cfg = load(path)
    if not dry:
        check(cfg)
    root = Path(cfg["root"]) / ("smoke" if smoke else "")
    root.mkdir(parents=True, exist_ok=True)
    write_json(root / "eval.config.json", cfg)
    ev = Evaluator(cfg["eval"], cfg["gpus"], root / "logs", cfg["cache_dir"], dry, cfg["smoke"]["benchmark_per_task"] if smoke else None)
    first = next((m["path"] for m in cfg["models"] if (Path(m["path"]) / "config.json").is_file()), None)
    size = cfg.get("image_max_size") or MIX["image_max_size"]
    budget = cfg.get("max_image_tokens_per_sample") or MIX["max_image_tokens_per_sample"]
    if dry:
        sets = {b["id"]: str(Path(cfg["cache_dir"]) / "sets" / b["id"]) for b in cfg["benchmark"]}
    else:
        sets = {k: str(v) for k, v in prepare_sets(cfg["benchmark"], cfg["cache_dir"], size, budget,
                                                   pixel_factor(first) if first else 32).items()}
    res = {"name": cfg["name"], "about": cfg["about"], "record": cfg.get("record"), "baseline": cfg.get("baseline"), "models": []}
    for m in cfg["models"]:
        log(f"=== {m['label']} ({m['path']})")
        try:
            path_ = model_dir(m, cfg, ev)
            plan = ev.answer(path_, m["model_type"], sets, m["label"])
        except (RuntimeError, OSError, ValueError) as exc:   # 모델 하나가 실패해도 다음 모델로
            log(f"WARNING: {m['label']}: 평가하지 못했습니다 ({type(exc).__name__}: {exc}); 다음 모델로")
            res.setdefault("notes", []).append(f"{m['label']}: 평가하지 못함 ({exc})")
            continue
        res["models"].append({k: v for k, v in {"label": m["label"], "about": m.get("about"), "model": path_,
                                                "checkpoint": m.get("checkpoint") or (m["path"] if path_ != m["path"] else None),
                                                "changes": m.get("changes"), "train": m.get("train"), "sets": plan}.items() if v})
        if not dry:
            write_json(root / "results.json", res)
            write_safe(res, root)
    log(f"끝: {root / 'report.html'}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m train eval", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", required=True, help="평가 설정 JSON (train/configs/eval.example.json)")
    p.add_argument("--smoke", action="store_true", help="리허설: 평가 세트·과제마다 8문항 (<root>/smoke)")
    p.add_argument("--dry-run", action="store_true", help="무엇을 평가할지만 보기")
    a = p.parse_args(argv)
    run(a.config, a.smoke, a.dry_run)
