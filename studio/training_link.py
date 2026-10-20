"""학습으로 이어 쓰기 (DESIGN.md 9.9, studio/TRAINING.md): 설정 조각 내보내기, 학습 기록, 진행 읽기, 결과 자동 붙이기.

- 설정은 1부면 ocr/configs/studio-<이름>.json, 2부면 bank/configs/studio-<이름>.json 에 쓴다. 예시 파일(configs/*.example.json)과
  같은 폴더라 그 안의 상대 경로(sft.yaml, ../runs/…, ../data/…)가 그대로 맞는다. 이 파일들은 내부 경로가 들어가므로 git 에 넣지 않는다.
- studio 는 학습을 실행하지 않는다. 학습 컨테이너에서 실행할 명령을 보여 주고, 공유 폴더의 <workdir>/state.json 을 읽어
  진행을 보여 준다. report 단계가 끝나면 그 workdir 을 평가 세트 데이터셋의 모델 답으로 붙인다.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from .config import BANK_DIR, OCR_DIR

DIRS = {"ocr": OCR_DIR, "bank": BANK_DIR}   # 파이프라인 폴더 (설정 조각의 "dir")
STAGES = ["prepare", "eval_base", "sft", "eval_sft", "select", "grpo", "eval_grpo", "report"]
STAGE_NAME = {"prepare": "데이터 준비", "eval_base": "원래 모델 평가", "sft": "SFT 학습", "eval_sft": "SFT 평가",
              "select": "GRPO 문제 고르기", "grpo": "GRPO 학습", "eval_grpo": "GRPO 평가", "report": "비교표"}


def slug(s: str) -> str:
    return re.sub(r"[^\w.-]+", "-", s).strip("-") or "run"


def to_train_path(p: str, path_map: dict) -> str:
    """studio 쪽 경로 → 학습 컨테이너 쪽 경로 (설정의 path_map)."""
    for here, there in path_map.items():
        if p.startswith(here):
            rest = p[len(here):]
            return there + (rest.replace("\\", "/") if there.startswith("/") else rest)   # 학습 쪽이 Linux 경로면 / 로
    return p


def from_train_path(p: str, path_map: dict) -> str:
    for here, there in path_map.items():
        if p.startswith(there):
            return here + p[len(there):]
    return p


def write_training(registry, info: dict, datasets: list[str], benchmark: str, name: str) -> dict:
    """설정 조각을 예시 파일과 합쳐 <ocr|bank>/configs/studio-<이름>.json 에 쓰고 등록부 trainings 에 남긴다."""
    base = pipeline_dir(info)
    example_name = "bank_pipeline.example.json" if info["pipeline"].startswith("2부") else "pipeline.example.json"
    example = json.loads((base / "configs" / example_name).read_text(encoding="utf-8"))
    merged = {**example, **{k: v for k, v in info["config"].items() if k != "data"}}
    if "data" in info["config"]:
        merged["data"] = {**example.get("data", {}), **info["config"]["data"]}
    f = base / info["file"]
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(merged, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for extra_name, content in (info.get("extra_files") or {}).items():   # 1부: 데이터 설정(config.json) 따로
        (base / extra_name).write_text(json.dumps(content, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    d = registry.load()
    rec = {"name": slug(name), "pipeline": info["pipeline"], "dir": base.name, "config": info["file"], "datasets": datasets,
           "benchmark": benchmark, "workdir": merged.get("workdir"), "created": time.strftime("%Y-%m-%d %H:%M"),
           "command": info["command"]}
    d["trainings"] = [t for t in d.get("trainings", []) if t["name"] != rec["name"]] + [rec]
    registry.save(d)
    return {**rec, "written": str(f)}


def pipeline_dir(info: dict) -> Path:
    """설정 조각·학습 기록의 파이프라인 폴더. 예전 기록(dir 없음)은 파이프라인 이름으로 정한다."""
    return DIRS[info.get("dir") or ("bank" if str(info.get("pipeline", "")).startswith("2부") else "ocr")]


def workdir_of(rec: dict, path_map: dict) -> Path:
    w = rec.get("workdir") or f"../runs/{rec['name']}"
    if Path(w).is_absolute() or w.startswith("/"):
        return Path(from_train_path(w, path_map))
    return (pipeline_dir(rec) / "configs" / w).resolve()


def status(registry, rec: dict) -> dict:
    """학습 하나의 진행: state.json 의 done 단계, 결과 폴더, 자동으로 붙였는지."""
    wd = workdir_of(rec, registry.path_map)
    st = wd / "state.json"
    done = json.loads(st.read_text(encoding="utf-8")).get("done", []) if st.exists() else []
    out = {**rec, "workdir_here": str(wd), "started": st.exists(), "done": done,
           "stages": [{"id": s, "name": STAGE_NAME[s], "done": s in done} for s in STAGES],
           "finished": "report" in done}
    if out["finished"] and rec.get("benchmark"):   # 끝났으면 평가 세트에 모델 답으로 붙인다 (한 번만)
        try:
            ds = registry.get(rec["benchmark"])
            if not any(Path(r["path"]).resolve() == wd.resolve() for r in ds.get("runs", [])):
                registry.attach_run(rec["benchmark"], str(wd), f"학습 {rec['name']}")
            out["attached"] = True
        except (KeyError, ValueError) as e:
            out["attach_error"] = str(e)
    return out
