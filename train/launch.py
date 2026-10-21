"""ms-swift 학습 실행기 (옛 ocr/train.py). --execute 면 학습을 시작하고, 아니면 명령만 보여 준다.

  python -m train.launch {sft,grpo} --config train/configs/sft.yaml --model <모델 폴더> --data <섞은 폴더> --output <폴더> --execute
학습 실행(pipeline.py)의 sft·grpo 단계가 부른다. GRPO 보상 플러그인은 reward_plugin.py (reward_funcs ["docgen"])."""
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import shlex
import subprocess

from .settings import image_tokens, image_tokens_for, load_settings

ROOT = Path(__file__).resolve().parent

def swift_args(options):
    result = []
    for key, value in options.items():
        if not key.replace("_", "").isalnum() or key.startswith("-"):
            raise ValueError(f"Invalid SWIFT option: {key}")
        if value is None:
            continue
        values = value if isinstance(value, list) else [value]
        if not values:
            continue
        result.append("--" + key)
        result.extend(json.dumps(v) if isinstance(v, (bool, dict)) else str(v) for v in values)
    return result

def gpu_selection(value):
    ids = [v.strip() for v in value.split(",")]
    if not ids or any(not v.isdigit() for v in ids) or len(set(ids)) != len(ids):
        raise ValueError("GPU IDs must be distinct numbers, e.g. 4,5,6,7")
    return ",".join(ids), len(ids)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("stage", choices=["sft", "grpo"])
    p.add_argument("--config", help="Native MS-SWIFT YAML/JSON options; default train/configs/sft.yaml · grpo_a100x2.yaml")
    p.add_argument("--gpus", help="GPU IDs; overrides CUDA_VISIBLE_DEVICES, default 0,1,2,3")
    p.add_argument("--model", required=True, help="Local Qwen3.5-9B directory")
    p.add_argument("--model-type", "--model_type", dest="model_type",
                   help="MS-SWIFT model type; overrides config, default qwen3_5")
    p.add_argument("--data", required=True, help="Prepared dataset directory with DONE.json")
    p.add_argument("--output", required=True)
    p.add_argument("--adapter", help="SFT adapter checkpoint, required for GRPO")
    p.add_argument("--grpo-dataset", help="Optional mined TRAIN dataset")
    p.add_argument("--max-steps", type=int, default=None, help="Use 5 for first GPU smoke test")
    p.add_argument("--image-tokens", type=int, default=None,
                   help="Default: IMAGE_MAX_TOKEN_NUM, else computed from image_max_size and the model's vision config")
    p.add_argument("--deepspeed", help="zero2, zero3, or custom DeepSpeed config path")
    p.add_argument("--execute", action="store_true")
    a = p.parse_args()
    config = Path(a.config).resolve() if a.config else ROOT / "configs" / {"sft": "sft.yaml", "grpo": "grpo_a100x2.yaml"}[a.stage]
    try:
        options = load_settings(config)
        reserved = {"model", "dataset", "val_dataset", "output_dir", "adapters", "ref_adapters", "config", "ENV"}
        if reserved & options.keys():
            raise ValueError("Use launcher CLI for paths/environment: " + ", ".join(sorted(reserved & options.keys())))
        gpus, processes = gpu_selection(a.gpus if a.gpus is not None else os.getenv("CUDA_VISIBLE_DEVICES", "0,1,2,3"))
    except (ValueError, OSError) as exc:
        p.error(str(exc))
    data = Path(a.data).resolve()
    if not (data / "DONE.json").is_file():
        p.error("Dataset preparation must complete (DONE.json missing)")
    if not Path(a.model).is_dir():
        p.error("--model must be a local model directory")
    if a.image_tokens is None and os.getenv("IMAGE_MAX_TOKEN_NUM"):
        a.image_tokens = int(os.environ["IMAGE_MAX_TOKEN_NUM"])
    elif a.image_tokens is None:
        # Enough tokens that prepared images (image_max_size) are never downscaled again.
        size = json.loads((data / "DONE.json").read_text(encoding="utf-8")).get("image_max_size", [2300, 1600])
        try:
            a.image_tokens, factor = image_tokens(a.model, size)
        except (OSError, ValueError) as exc:
            a.image_tokens, factor = image_tokens_for(size, 32), 32
            print(f"WARNING: {exc}; assuming 32x32 pixels per visual token")
        print(f"image_max_size={size} pixels_per_token_side={factor} -> IMAGE_MAX_TOKEN_NUM={a.image_tokens}")
    if a.stage == "grpo" and (not a.adapter or not Path(a.adapter).is_dir()):
        p.error("GRPO needs --adapter pointing to an SFT checkpoint")
    if a.image_tokens < 1:
        p.error("--image-tokens must be positive")
    dataset = Path(a.grpo_dataset).resolve() if a.stage == "grpo" and a.grpo_dataset else data / f"train_{a.stage}.jsonl"
    if not dataset.is_file() or not dataset.stat().st_size:
        p.error("Empty or missing training dataset")
    if a.stage == "grpo":
        with dataset.open(encoding="utf-8") as f:
            for line in f:
                if line.strip() and json.loads(line).get("split") != "train":
                    p.error("GRPO dataset must contain only train rows")
    options.update(model=str(Path(a.model).resolve()), dataset=[str(dataset)], output_dir=str(Path(a.output).resolve()))
    if a.model_type is not None:
        options["model_type"] = a.model_type
    elif options.get("model_type") is None:
        options["model_type"] = "qwen3_5"
    if a.max_steps is not None:
        options["max_steps"] = a.max_steps
    if a.deepspeed is not None:
        options["deepspeed"] = a.deepspeed
    if a.stage == "sft":
        validation = data / "val_sft.jsonl"
        if validation.is_file() and validation.stat().st_size:
            options["val_dataset"] = [str(validation)]
    else:
        if options.get("rlhf_type", "grpo") != "grpo":
            p.error("GRPO stage requires rlhf_type=grpo")
        if options.get("remove_unused_columns", False) is not False:
            p.error("Reward fields (task, bench_item) require remove_unused_columns=false")
        options.update(rlhf_type="grpo", remove_unused_columns=False,
                       adapters=[str(Path(a.adapter).resolve())], ref_adapters=[str(Path(a.adapter).resolve())])
        # 플러그인은 절대 경로 (학습 프로세스의 작업 폴더와 상관없이), 저장소 최상위가 PYTHONPATH 에 있어야 docgen 을 불러온다
        options["external_plugins"] = [str(ROOT / "reward_plugin.py")]
        options.setdefault("reward_funcs", ["docgen"])
    try:
        cmd = ["swift", "sft" if a.stage == "sft" else "rlhf"] + swift_args(options)
    except ValueError as exc:
        p.error(str(exc))
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(ROOT.parent)] + ([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else [])),
           "CUDA_VISIBLE_DEVICES": gpus, "NPROC_PER_NODE": str(processes),
           "IMAGE_MAX_TOKEN_NUM": str(a.image_tokens), "HF_HUB_OFFLINE": "1",
           "TRANSFORMERS_OFFLINE": "1", "HF_DATASETS_OFFLINE": "1", "WANDB_DISABLED": "true"}
    print(f"CUDA_VISIBLE_DEVICES={gpus} NPROC_PER_NODE={processes} IMAGE_MAX_TOKEN_NUM={a.image_tokens}")
    print(shlex.join(cmd), flush=True)
    if a.execute:
        version = importlib.metadata.version("ms-swift")
        if version.split(".")[0] != "4":
            p.error(f"Launcher targets ms-swift 4.x; installed: {version}")
        Path(a.output).mkdir(parents=True, exist_ok=True)
        info = {"command": cmd, "ms_swift_version": version, "image_max_token_num": a.image_tokens,
                "hardware_target": f"{processes}x A100 40GB", "cuda_visible_devices": gpus,
                "nproc_per_node": processes, "config": str(config)}
        (Path(a.output) / "launch.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
        (Path(a.output) / "training.resolved.json").write_text(json.dumps(options, indent=2), encoding="utf-8")
        with (Path(a.output) / "environment.freeze.txt").open("w", encoding="utf-8") as f:
            for dist in sorted(importlib.metadata.distributions(), key=lambda d: d.metadata.get("Name", "")):
                f.write(f"{dist.metadata.get('Name')}=={dist.version}\n")
        subprocess.run(cmd, env=env, check=True)


if __name__ == "__main__":
    main()
