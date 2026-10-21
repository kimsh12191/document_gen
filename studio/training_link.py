"""학습으로 이어 쓰기 (DESIGN.md 9.9·17절, studio/TRAINING.md): 설정 만들기, 학습 기록, 진행 읽기, 결과 자동 붙이기.

- 학습은 하나다 (train/, python -m train). 설정은 train/configs/studio-<이름>.json 에 쓴다. 예시 파일
  (train/configs/pipeline.example.json)과 같은 폴더라 그 안의 상대 경로(sft.yaml, ../runs/…, ../data/…)가 그대로 맞는다.
  내부 경로가 들어가므로 git 에 넣지 않는다.
- 학습 데이터·평가 세트는 studio 데이터셋(과제 폴더) 목록이다. OCR·문서 이해·업무 과제를 섞어도 된다 (데이터셋마다 쓸 문항 수 count).
- studio 는 학습을 실행하지 않는다. 학습 컨테이너에서 실행할 명령을 보여 주고, 공유 폴더의 <workdir>/state.json 을 읽어
  진행을 보여 준다. report 단계가 끝나면 그 workdir 을 평가 세트 데이터셋마다 모델 답으로 붙인다.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from .config import ROOT

TRAIN_DIR = ROOT / "train"
DIRS = {"train": TRAIN_DIR, "ocr": ROOT / "ocr", "bank": ROOT / "bank"}   # 학습 기록의 "dir" (ocr·bank 는 옛 기록)
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


def training_config(registry, train: list, benchmark: list | str, name: str) -> dict:
    """학습 설정 조각과 실행할 명령. train = [데이터셋 ID 또는 {id, count}], benchmark = 평가 데이터셋 ID 목록.
    나머지 칸(모델·GPU·SFT·GRPO)은 예시 파일 값을 쓴다."""
    reg = registry.load()["datasets"]
    train = [t if isinstance(t, dict) else {"id": t} for t in train]
    bench = [benchmark] if isinstance(benchmark, str) else list(benchmark)
    if not train or not bench:
        raise ValueError("학습 데이터와 평가 세트를 하나 이상 고르세요")
    warn = []
    for i in [t["id"] for t in train] + bench:
        if i not in reg:
            raise KeyError(i)
        if reg[i].get("format") != "docgen-tasks":
            raise ValueError(f"{i}: 과제 폴더 데이터셋이 아닙니다")

    def meta(i):
        return json.loads((Path(reg[i]["path"]) / "meta.json").read_text(encoding="utf-8"))
    for t in train:
        m = meta(t["id"])
        if m.get("split") not in ("train", "mixed") and not (m.get("split_counts") or {}).get("train"):
            raise ValueError(f"{t['id']}: 학습 문항이 없습니다 (평가 전용 세트)")
    for b in bench:
        m = meta(b)
        if m.get("split") == "train":
            raise ValueError(f"{b}: 평가 세트로 학습 전용 데이터셋을 골랐습니다")
        if not reg[b].get("frozen"):
            warn.append(f"평가 세트 {b} 를 아직 고정하지 않았습니다")
    versions = {meta(i).get("version") for i in [t["id"] for t in train] + bench if reg[i].get("kind") != "ocr"}
    if len(versions - {None}) > 1:
        warn.append(f"문서·업무 과제의 생성기 버전이 섞였습니다: {sorted(v for v in versions if v)}")
    pm = registry.path_map
    n = slug(name)
    data = {"train": [{"path": to_train_path(reg[t["id"]]["path"], pm), **({"count": int(t["count"])} if t.get("count") else {})}
                      for t in train],
            "benchmark": [to_train_path(reg[b]["path"], pm) for b in bench], "output_dir": f"../data/mixed-{n}"}
    file = f"configs/studio-{n}.json"
    return {"pipeline": "train", "dir": "train", "file": file, "config": {"workdir": f"../runs/{n}", "data": data},
            "warnings": warn, "command": f"python -m train --config train/{file}",
            "note": "model·gpus·sft·grpo·eval·task_mix 칸은 train/configs/pipeline.example.json 값을 쓴다. 모델 경로는 직접 확인하세요."}


def write_training(registry, info: dict, datasets: list[str], benchmark: list[str] | str, name: str) -> dict:
    """설정 조각을 예시 파일과 합쳐 train/configs/studio-<이름>.json 에 쓰고 등록부 trainings 에 남긴다."""
    base = pipeline_dir(info)
    example = json.loads((base / "configs" / "pipeline.example.json").read_text(encoding="utf-8"))
    merged = {**example, **{k: v for k, v in info["config"].items() if k != "data"}}
    if "data" in info["config"]:
        merged["data"] = {**example.get("data", {}), **info["config"]["data"]}
    f = base / info["file"]
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(merged, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    d = registry.load()
    rec = {"name": slug(name), "pipeline": info["pipeline"], "dir": info.get("dir", "train"), "config": info["file"], "datasets": datasets,
           "benchmark": [benchmark] if isinstance(benchmark, str) else benchmark, "workdir": merged.get("workdir"),
           "created": time.strftime("%Y-%m-%d %H:%M"), "command": info["command"]}
    d["trainings"] = [t for t in d.get("trainings", []) if t["name"] != rec["name"]] + [rec]
    registry.save(d)
    return {**rec, "written": str(f)}


def pipeline_dir(info: dict) -> Path:
    """설정 조각·학습 기록의 폴더. 옛 기록(1부·2부)은 그때 폴더."""
    if info.get("dir") in DIRS:
        return DIRS[info["dir"]]
    p = str(info.get("pipeline", ""))
    return DIRS["bank" if p.startswith("2부") else "ocr" if p.startswith("1부") else "train"]


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
    benches = rec.get("benchmark") or []
    benches = [benches] if isinstance(benches, str) else benches
    if out["finished"] and benches:   # 끝났으면 평가 세트마다 모델 답으로 붙인다 (한 번만)
        try:
            for b in benches:
                ds = registry.get(b)
                if not any(Path(r["path"]).resolve() == wd.resolve() for r in ds.get("runs", [])):
                    registry.attach_run(b, str(wd), f"학습 {rec['name']}")
            out["attached"] = True
        except (KeyError, ValueError) as e:
            out["attach_error"] = str(e)
    out["benchmark"] = benches
    return out
