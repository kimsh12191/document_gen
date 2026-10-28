"""실험 묶음: 평가 세트는 고정하고 학습 쪽 설정을 바꾼 모델 여러 개를 차례로(또는 GPU 를 나눠 동시에) 학습·평가하고
비교표 하나로 (python -m train sweep).

  python -m train sweep --config <묶음.json>            돌림 (다시 치면 이어서, 끝난 모델은 건너뜀)
  python -m train sweep --config <묶음.json> --status   진행 상황과 비교표 위치
  python -m train sweep --config <묶음.json> --smoke    모델마다 5 step 리허설 (<root>/<label>/smoke)

묶음 파일 (상대 경로는 이 파일이 있는 폴더 기준, base 안의 경로는 base 파일 기준):
  {"name": "E02-tune", "about": "무엇을 확인하는 실험인지", "record": "experiments/E02-tune.md",
   "base": "pipeline.json", "root": "../runs/E02-tune", "part": "sft", "baseline": "a1",
   "gpu_groups": [[0, 1], [2, 3]], "start_from": "../runs/E00-x/a1",
   "runs": [{"label": "a1", "about": "기준 (base 그대로)"},
            {"label": "a2-lr", "about": "학습률·에폭", "sft": {"learning_rate": 5e-5, "num_train_epochs": 2}},
            {"label": "a3-data", "about": "실서류 OCR 더함", "train": ["<데이터셋>", {"path": "<OCR 준비>", "count": 20000}],
             "data": {"task_mix": {"kie": 0.3}}},
            {"label": "a4-vl", "about": "다른 출발 모델", "model": "/share/…/qwen3-vl-8b", "model_type": "qwen3_vl"},
            {"label": "a5-grpo", "about": "a1 SFT 에서 GRPO beta", "from_sft": "a1", "grpo": {"beta": 0.08}}]}
- 모델마다 적지 않은 칸은 base 값. 바꿀 수 있는 칸 (RUN_KEYS):
  model · model_type   출발 모델 (다르면 그 출발 모델도 한 번 평가)
  train                학습 데이터셋 목록 (= data.train)
  data                 섞기 칸: task_mix · sft_max_examples · grpo_holdout · image_max_size · max_image_tokens_per_sample ·
                       sft_max_length · seed … (benchmark·output_dir 는 못 바꿈)
  sft · grpo           "config"(yaml 파일) + yaml 안의 ms-swift 옵션을 칸 하나씩 (learning_rate, lora_rank …),
                       grpo 는 후보 고르기 칸(select · candidates · count · hard_fraction · seed · tasks · max_images)도
  part                 "sft"(SFT 까지, 기본) | "all"(SFT + GRPO). 묶음 전체에도 적을 수 있다
  from_sft             같은 묶음의 label (또는 다른 묶음의 모델 폴더): 그 SFT 결과에서 GRPO 만. 그 모델의 칸을 물려받는다
  gpus                 이 모델만 쓸 GPU · deploy: 평가 서버 명령(eval.deploy_command) · set: 그 밖의 파이프라인 칸 덮어쓰기
- 평가는 고정: data.benchmark(채점 함수 포함) · eval.inference_config · eval.compare_models 는 모델마다 바꿀 수 없고,
  모델마다 학습 그림 예산을 바꿔도 평가 그림은 base 값으로 만든다 (mix 의 benchmark_image_max_size …).
- gpu_groups 를 적으면 비는 GPU 묶음에 다음 모델을 넣어 동시에 돌린다 (평가 서버 포트·MASTER_PORT 는 GPU 마다 다르게).
  없으면 하나씩. 모델의 gpus 를 적으면 그 GPU 가 모두 빌 때 들어간다.
- 출발 모델은 서로 다른 것마다 그것을 쓰는 첫 모델에서 한 번 평가 (start_from 이 같은 출발 모델이면 그 평가를 가져다 씀.
  평가 문항·그림이 다르면 쓰지 않고 그 출발 모델의 첫 모델에서 평가).
- baseline: 비교표 괄호 %p 의 기준 모델 label (기본 첫 모델).
- name·about, runs 마다 label·about 은 꼭 적는다 (진행 상황·비교표 맨 위·<root>/sweep.config.json 에 남는다).
  label 은 이 실험 안의 모델 이름이자 폴더 이름 (<root>/<label>/ 가 workdir, <root>/<label>/data 가 data.output_dir).
- 모델 하나가 실패해도 다음 모델로 간다 (<root>/sweep.json 상태, <root>/<label>/sweep.log).
- 모델 하나가 끝날 때마다 <root>/compare.{csv,md,html}, 한 화면 <root>/summary.html, 문항별 답 <root>/answers.html 을 다시 만든다.
- 실험 여러 개를 한 html 로: python -m train summary <묶음.json|결과 폴더> ... --out <html> (train/summary.py).
- 이미 돈 모델의 설정이 바뀌면 그 모델은 돌리지 않는다 (새 label 로).
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

from docgen.bench.ocr_data import read_json, read_jsonl, write_json

from .cli import resolve_data
from .settings import load_settings

ROOT = Path(__file__).resolve().parents[1]
LABEL = re.compile(r"[a-z0-9][a-z0-9-]*")
DONE_PARTS = {"sft": "eval_sft", "all": "eval_grpo", "grpo": "eval_grpo"}
RUN_KEYS = {"label", "about", "model", "model_type", "train", "data", "sft", "grpo", "part", "from_sft", "gpus", "deploy", "set"}
FIXED = [("data", "benchmark"), ("data", "output_dir"), ("eval", "inference_config"), ("eval", "compare_models"),
         ("eval", "skip_start"), ("workdir",)]   # 평가를 고정하려고 모델마다 못 바꾸는 칸 (data.output_dir·workdir 는 묶음이 정함)
MASTER_PORT = 29500


def log(message):
    print(time.strftime("[%Y-%m-%d %H:%M:%S] ") + message, flush=True)


def load(path):
    path = Path(path).resolve()
    sw = load_settings(path)
    for k in ("name", "about", "base", "root", "runs"):
        if not sw.get(k):
            raise ValueError(f"묶음 파일에 {k} 가 없습니다 (about: 무엇을 확인하는 실험인지)")
    labels = [r.get("label") for r in sw["runs"]]
    bad = [x for x in labels if not isinstance(x, str) or not LABEL.fullmatch(x)]
    if bad or len(set(labels)) != len(labels):
        raise ValueError(f"runs.label 은 겹치지 않는 영문 소문자·숫자·- 여야 합니다: {bad or labels}")
    if any(not str(r.get("about", "")).strip() for r in sw["runs"]):
        raise ValueError("runs 마다 about (이 모델이 무엇인지) 이 있어야 합니다")
    for r in sw["runs"]:
        unknown = set(r) - RUN_KEYS
        if unknown:
            raise ValueError(f"{r['label']}: 모르는 칸 {sorted(unknown)} (쓸 수 있는 칸: {', '.join(sorted(RUN_KEYS))}; 그 밖의 칸은 set 으로)")
        if "train" in r and not r["train"]:
            raise ValueError(f"{r['label']}: train 이 비었습니다 (base 의 학습 데이터를 쓰려면 train 칸을 지우세요)")
        if r.get("from_sft") and r["from_sft"] not in labels[:labels.index(r["label"])] and not (path.parent / r["from_sft"]).is_dir():
            raise ValueError(f"{r['label']}: from_sft 는 앞에 적힌 모델의 label 이거나 다른 묶음의 모델 폴더여야 합니다: {r['from_sft']}")
    if any(part_of(sw, r) not in DONE_PARTS for r in sw["runs"]):
        raise ValueError("part 는 sft (SFT 까지) · all (SFT + GRPO)")
    if sw.get("baseline") and sw["baseline"] not in labels:
        raise ValueError(f"baseline 은 runs 의 label 이어야 합니다: {sw['baseline']}")
    groups = sw.get("gpu_groups") or []
    flat = [g for grp in groups for g in grp] if isinstance(groups, list) and all(isinstance(x, list) and x for x in groups) else None
    if flat is None or any(not isinstance(g, int) for g in flat) or len(set(flat)) != len(flat):
        raise ValueError(f"gpu_groups 는 겹치지 않는 GPU 번호 묶음 목록이어야 합니다 (예: [[0, 1], [2, 3]]): {groups}")
    sw["_dir"] = path.parent
    sw["_file"] = path
    sw["_root"] = (path.parent / sw["root"]).resolve()
    if sw.get("start_from"):
        sf = (path.parent / sw["start_from"]).resolve()
        if not (sf / "config.json").is_file() or not (sf / "reports" / "start.json").is_file():
            raise ValueError(f"start_from 은 출발 모델 평가를 마친 다른 묶음의 모델 폴더여야 합니다 (config.json·reports/start.json): {sf}")
        sw["_start_from"] = sf
    return sw


def by_label(sw):
    return {r["label"]: r for r in sw["runs"]}


def parent_of(sw, run):
    """from_sft 가 같은 묶음의 label 이면 그 모델 (칸을 물려받는다), 아니면 None."""
    return by_label(sw).get(run.get("from_sft"))


def spec(sw, run):
    """모델 하나의 칸: from_sft 로 이어받은 모델이면 부모의 칸 위에 이 모델의 칸 (dict 칸은 칸마다 덮어씀)."""
    from .pipeline import merged

    parent = parent_of(sw, run)
    if not parent:
        return dict(run)
    up = {k: v for k, v in spec(sw, parent).items() if k not in ("label", "about", "part", "from_sft")}
    own = {k: v for k, v in run.items() if k != "model" or v != up.get("model")}
    if "model" in own and "model" in up:
        raise ValueError(f"{run['label']}: from_sft 모델은 부모({parent['label']})와 출발 모델이 같아야 합니다")
    return merged(up, own)


def part_of(sw, run):
    return "grpo" if run.get("from_sft") else run.get("part") or sw.get("part", "sft")


def _fixed(over, label):
    for keys in FIXED:
        v = over
        for k in keys:
            v = v.get(k, None) if isinstance(v, dict) else None
        if v is not None:
            raise ValueError(f"{label}: {'.'.join(keys)} 는 모델마다 바꿀 수 없습니다 (평가 고정·묶음이 정함). base 에서 바꾸세요")


def run_config(sw, run, eval_start=False):
    """모델 하나의 파이프라인 설정: base + 이 모델의 칸, 경로는 모두 절대 경로로."""
    from .mix import DEFAULTS as MIX
    from .pipeline import merged

    base_path = (sw["_dir"] / sw["base"]).resolve()
    base, at, here = load_settings(base_path), base_path.parent, sw["_dir"]
    s = spec(sw, run)
    label = run["label"]
    _fixed(s.get("set") or {}, label)
    _fixed({"data": s.get("data") or {}}, label)

    def conf(p, where):   # yaml·json 파일: 그 폴더에 있으면 절대 경로, 없으면 이름 그대로 (train/configs 의 기본 파일)
        return str((where / p).resolve()) if p and not Path(p).is_absolute() and (where / p).exists() else p
    for sec, key in (("sft", "config"), ("grpo", "config"), ("eval", "inference_config")):
        if (base.get(sec) or {}).get(key):
            base[sec] = {**base[sec], key: conf(base[sec][key], at)}
    cfg = merged(base, s.get("set") or {})
    if s.get("model"):
        cfg["model"] = s["model"] if Path(s["model"]).is_absolute() else str((here / s["model"]).resolve())
    for k in ("model_type", "gpus"):
        if k in s:
            cfg[k] = s[k]
    if s.get("deploy"):
        cfg["eval"] = {**(cfg.get("eval") or {}), "deploy_command": s["deploy"]}
    for sec in ("sft", "grpo"):
        if s.get(sec):
            own = dict(s[sec])
            if own.get("config"):
                own["config"] = conf(own["config"], here)
            cfg[sec] = merged(cfg.get(sec) or {}, own)
    workdir = sw["_root"] / label
    data = {**cfg["data"], **(s.get("data") or {}), "output_dir": str(workdir / "data")}
    bench = resolve_data({"data": {**data, "train": []}}, at)   # benchmark 는 base 기준
    if "train" in s:
        bench["train"] = resolve_data({"data": {**data, "train": s["train"], "benchmark": []}}, here)["train"]   # 묶음 파일 기준
    else:
        bench["train"] = resolve_data({"data": {**data, "benchmark": []}}, at)["train"]
    cfg["data"] = bench
    # 평가 그림은 base 값으로 고정 (이 모델이 학습 그림 예산을 바꿨을 때만 적는다)
    want, have = {**MIX, **base["data"]}, {**MIX, **bench}
    for img, fixed in (("image_max_size", "benchmark_image_max_size"),
                       ("max_image_tokens_per_sample", "benchmark_max_image_tokens_per_sample")):
        if (have[fixed] or have[img]) != (want[fixed] or want[img]):
            cfg["data"][fixed] = want[fixed] or want[img]
    cfg["workdir"] = str(workdir)
    if cfg.get("ocr_prepare"):
        ocr = cfg["ocr_prepare"]
        cfg["ocr_prepare"] = [p if Path(p).is_absolute() else str((at / p).resolve()) for p in (ocr if isinstance(ocr, list) else [ocr])]
    cfg.setdefault("eval", {})["skip_start"] = not eval_start
    return cfg


def model_of(sw, run):
    return run_config(sw, run)["model"]


def start_labels(sw):
    """출발 모델을 평가할 모델: 서로 다른 출발 모델마다 그것을 쓰는 첫 모델 (start_from 이 같은 출발 모델이면 없음).
    from_sft 모델은 부모와 출발 모델이 같아 평가하지 않는다."""
    seen = set()
    if "_start_from" in sw:
        seen.add(read_json(sw["_start_from"] / "config.json")["model"])
    out = []
    for r in sw["runs"]:
        if r.get("from_sft"):
            continue
        m = model_of(sw, r)
        if m not in seen:
            seen.add(m)
            out.append(r["label"])
    return out


def same_model(a, b):
    """설정이 같은 모델인지 (출발 모델 평가 여부·GPU·포트는 모델과 상관없다)."""
    def strip(c):
        return {**{k: v for k, v in c.items() if k != "gpus"},
                "eval": {k: v for k, v in (c.get("eval") or {}).items() if k not in ("skip_start", "port_base")}}
    return strip(a) == strip(b)


def default_runner(config: Path, log_path: Path, part: str, smoke: bool, only: str | None = None,
                   sft_checkpoint: str | None = None, env: dict | None = None) -> int:
    cmd = [sys.executable, "-m", "train", "--config", str(config)]
    if only:
        cmd += ["--only", only]
    elif part == "grpo":
        cmd += ["--part", "grpo", "--sft-checkpoint", str(sft_checkpoint)]
    elif part != "all":
        cmd += ["--part", part]
    cmd += ["--smoke"] if smoke else []
    with log_path.open("a", encoding="utf-8") as out:
        out.write(time.strftime("[%Y-%m-%d %H:%M:%S] $ ") + " ".join(cmd) + "\n")
        out.flush()
        return subprocess.run(cmd, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT,
                              env={**os.environ, **(env or {}), "PYTHONIOENCODING": "utf-8"}).returncode


def workdir_of(sw, label, smoke):
    return sw["_root"] / label / ("smoke" if smoke else "")


def finished(sw, run, smoke):
    state = workdir_of(sw, run["label"], smoke) / "state.json"
    return state.exists() and DONE_PARTS[part_of(sw, run)] in read_json(state).get("done", [])


def sft_checkpoint(sw, run, smoke):
    """from_sft 모델이 GRPO 를 시작할 SFT 체크포인트 (부모 workdir 의 state.json). 없으면 None."""
    src = run["from_sft"]
    wd = workdir_of(sw, src, smoke) if src in by_label(sw) else (sw["_dir"] / src).resolve() / ("smoke" if smoke else "")
    state = wd / "state.json"
    return read_json(state).get("sft_checkpoint") if state.exists() else None


def preflight(sw):
    """돌리기 전에 모든 모델의 설정을 한꺼번에 검사한다: 모델마다 칸, 평가 칸(id·format·gt), 출발 모델, 학습·평가 경로.
    틀린 것이 있으면 하나도 돌리지 않는다 (모델마다 시작했다가 같은 이유로 줄줄이 실패하지 않게)."""
    from .benchmarks import normalize

    problems = []
    for r in sw["runs"]:
        label = r["label"]
        try:
            cfg = run_config(sw, r)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            problems.append(f"{label}: 설정을 만들지 못함 ({exc})")
            continue
        try:
            benches = normalize(cfg["data"]["benchmark"])
        except ValueError as exc:
            problems.append(f"base 의 data.benchmark: {exc}")
            benches = []
        model = Path(cfg["model"]) if Path(cfg["model"]).is_absolute() else ROOT / cfg["model"]
        if not (model / "config.json").is_file():
            problems.append(f"{label}: 출발 모델 폴더(config.json)가 없습니다: {model}")
        for sec in ("sft", "grpo"):
            p = (cfg.get(sec) or {}).get("config")
            if p and not Path(p).is_file() and not (ROOT / "train" / "configs" / p).is_file():
                problems.append(f"{label}: {sec}.config 파일이 없습니다: {p}")
        later = set()   # ocr_prepare 단계가 만들 폴더
        for conf in cfg.get("ocr_prepare") or []:
            if Path(conf).is_file():
                later.add(str((Path(conf).parent / read_json(conf)["output_dir"]).resolve()))
        for e in cfg["data"]["train"]:
            path = e if isinstance(e, str) else e.get("path", "")
            if not isinstance(e, str) and e.get("format") == "swift-fields":
                if not Path(path).is_file():
                    problems.append(f"{label}: train swift .jsonl 이 없습니다: {path}")
            elif path not in later and not ((Path(path) / "meta.json").is_file() and (Path(path) / "tasks").is_dir()):
                problems.append(f"{label}: train 경로가 데이터셋 폴더(meta.json + tasks/)가 아닙니다: {path}")
        for b in benches:
            for path in b["paths"]:
                if path in later:
                    continue
                ok = Path(path).is_file() if b.get("format") == "swift-fields" else \
                    (Path(path) / "meta.json").is_file() and (Path(path) / "tasks").is_dir()
                if not ok:
                    problems.append(f"base 의 data.benchmark {b['id']}: 경로가 없습니다: {path}")
        if r.get("gpus") and sw.get("gpu_groups") and not set(r["gpus"]) <= {g for grp in sw["gpu_groups"] for g in grp}:
            problems.append(f"{label}: gpus {r['gpus']} 가 gpu_groups 밖에 있습니다")
    problems = list(dict.fromkeys(problems))   # 공통 설정의 문제는 한 번만
    if problems:
        raise SystemExit(f"묶음 {sw['_file']} 를 돌리기 전에 고칠 것 ({len(problems)}건, 아무 모델도 시작하지 않았습니다):\n  "
                         + "\n  ".join(problems))


def run(sweep_path, smoke=False, runner=default_runner):
    sw = load(sweep_path)
    preflight(sw)
    root = sw["_root"]
    root.mkdir(parents=True, exist_ok=True)
    lock = root / "sweep.lock"
    if lock.exists():
        pid = int(lock.read_text().strip() or 0)
        try:
            os.kill(pid, 0)
            raise SystemExit(f"이미 돌고 있습니다 (pid {pid}). 진행 상황: --status")
        except (OSError, ValueError):
            pass   # 끝난 실행이 남긴 잠금
    lock.write_text(str(os.getpid()))
    write_json(root / "sweep.config.json", {k: v for k, v in sw.items() if not k.startswith("_")})   # 결과 폴더만 봐도 무슨 실험인지
    status_path = root / "sweep.json"
    status = read_json(status_path) if status_path.exists() else {}
    starters = set(start_labels(sw))
    groups = sw.get("gpu_groups") or []
    outcome, busy, used = {}, {}, set()
    n = len(sw["runs"])

    def note(label, **kw):
        status[label] = {**kw, "at": time.strftime("%Y-%m-%d %H:%M")}
        write_json(status_path, status)

    def launch(i, r, cfg, gpus, pool):
        """돌릴 모델이면 future, 건너뛰면 None (outcome 에 적음)."""
        label = r["label"]
        folder = root / label
        folder.mkdir(parents=True, exist_ok=True)
        cpath = folder / "config.json"
        if cpath.exists() and not same_model(read_json(cpath), cfg):
            note(label, status="failed", why="이미 돈 모델의 설정이 바뀜 (base·train·칸). 새 label 로 추가하세요")
            log(f"{label}: 설정이 바뀌어 건너뜁니다 ({cpath})")
            outcome[label] = "failed"
            return None
        write_json(cpath, cfg)
        if finished(sw, r, smoke) and status.get(label, {}).get("status") == "done":
            log(f"{label}: 끝남 (건너뜀)")
            outcome[label] = "done"
            return None
        ckpt = None
        if r.get("from_sft"):
            ckpt = sft_checkpoint(sw, r, smoke)
            if not ckpt:
                note(label, status="failed", why=f"from_sft {r['from_sft']} 의 SFT 체크포인트가 없습니다")
                outcome[label] = "failed"
                return None
        env = {"MASTER_PORT": str(MASTER_PORT + min(gpus))} if groups else {}
        log(f"=== {label} ({i + 1}/{n}, GPU {','.join(map(str, gpus))}) → {folder / 'sweep.log'}")
        status[label] = {"status": "running", "started": time.strftime("%Y-%m-%d %H:%M"), "pid": os.getpid(), "gpus": gpus}
        write_json(status_path, status)
        return pool.submit(runner, cpath, folder / "sweep.log", part_of(sw, r), smoke, None, ckpt, env)

    def pick(r, cfg):
        """이 모델에 줄 GPU (지금 비어 있는 것), 없으면 None."""
        if not groups:
            from .pipeline import DEFAULTS

            return list(cfg.get("gpus") or DEFAULTS["gpus"]) if not busy else None
        for want in ([r["gpus"]] if r.get("gpus") else groups):
            if not set(want) & used:
                return list(want)
        return None

    try:
        todo = list(enumerate(sw["runs"]))
        with ThreadPoolExecutor(max_workers=max(1, len(groups))) as pool:
            while todo or busy:
                before = len(todo)
                for i, r in list(todo):
                    label, src = r["label"], r.get("from_sft")
                    if src in by_label(sw) and src not in outcome:
                        continue   # 부모 SFT 를 기다린다
                    if src in by_label(sw) and outcome[src] != "done":
                        note(label, status="failed", why=f"from_sft {src} 가 끝나지 않음")
                        outcome[label] = "failed"
                        todo.remove((i, r))
                        continue
                    cfg = run_config(sw, r, eval_start=label in starters)
                    gpus = pick(r, cfg)
                    if gpus is None:
                        if not groups:
                            break   # 하나씩: 차례를 지킨다
                        continue
                    todo.remove((i, r))
                    if groups:   # 동시에: 받은 GPU 묶음, 묶음마다 평가 서버 포트를 다르게
                        cfg["gpus"] = gpus
                        cfg["eval"]["port_base"] = (cfg["eval"].get("port_base") or 8000) + 10 * min(gpus)
                    fut = launch(i, r, cfg, gpus, pool)
                    if fut:
                        busy[fut] = (r, gpus, time.monotonic())
                        used.update(gpus)
                if not busy:
                    if todo and len(todo) < before:
                        continue   # 이번 바퀴에 끝낸(건너뛴) 모델이 있다: 기다리던 모델을 다시 본다
                    for i, r in todo:   # 더 돌 수 있는 것이 없다
                        note(r["label"], status="failed", why="시작하지 못함 (from_sft·gpus 확인)")
                    break
                done, _ = wait(list(busy), return_when=FIRST_COMPLETED)
                for fut in done:
                    r, gpus, started = busy.pop(fut)
                    used.difference_update(gpus)
                    label = r["label"]
                    try:
                        code = fut.result()
                    except Exception as exc:  # noqa: BLE001  한 모델의 실행 오류로 묶음 전체가 멈추지 않게
                        code = f"{type(exc).__name__}: {exc}"
                    hours = round((time.monotonic() - started) / 3600, 2)
                    ok = code == 0 and finished(sw, r, smoke)
                    outcome[label] = "done" if ok else "failed"
                    note(label, status=outcome[label], hours=hours, gpus=gpus,
                         **({} if ok else {"why": f"종료 코드 {code}, 로그 {root / label / 'sweep.log'}"}))
                    log(f"{label}: {'끝' if ok else '실패 — 다음 모델로'} ({hours} h)")
                    compare(sw, smoke)
        compare(sw, smoke)
        first = sw.get("_start_mismatch")
        if first and (root / first / "data" / "DONE.json").exists():
            # start_from 의 평가 문항이 이 묶음과 다르다: 그 출발 모델을 쓰는 첫 모델에서 출발 모델을 평가한다
            log(f"start_from 의 출발 모델 평가를 쓸 수 없어 {first} 에서 출발 모델을 평가합니다")
            cfg = read_json(root / first / "config.json")
            spath = root / first / "config.start.json"
            write_json(spath, {**cfg, "eval": {**cfg["eval"], "skip_start": False}})
            runner(spath, root / first / "sweep.log", part_of(sw, by_label(sw)[first]), smoke, "eval_base")
            compare(sw, smoke)
    finally:
        lock.unlink(missing_ok=True)


# -- 비교표 ----------------------------------------------------------------------------------
def _images(workdir, data):
    """같은 평가 입력인지: (그림 줄이기 설정, 문항별 원본 그림) 과 그림 조각 크기(출발 모델 규격). 섞은 폴더마다 경로는 달라도."""
    done = read_json(data / "DONE.json")
    tasks = {r["id"]: r.get("source_images", r["images"]) for r in read_jsonl(data / "benchmark_tasks.jsonl")}
    size = done.get("benchmark_image_max_size") or done.get("image_max_size")
    budget = done.get("benchmark_max_image_tokens_per_sample") or done.get("max_image_tokens_per_sample")
    return ([size, budget], tasks), done.get("pixels_per_token_side")


def short(model):
    """출발 모델 이름 (폴더 끝 두 단계)."""
    return "/".join(Path(str(model)).parts[-2:])


def baseline(sw):
    return sw.get("baseline") or sw["runs"][0]["label"]


def collect(sw, smoke=False):
    """끝난 모델들의 보고서(평가 문항·그림이 첫 모델과 같은 것만)와 뺀 이유. 출발 모델은 서로 다른 것마다 앞에.
    sw["_sources"][줄 이름] = (workdir, 섞은 폴더) 는 문항별 답 페이지(answers.py)가 쓴다."""
    root, reports, notes, ref, factor = sw["_root"], [], [], None, None
    sw["_start_mismatch"] = None
    sources = sw["_sources"] = {}
    runs = by_label(sw)
    models = {label: read_json(root / label / "config.json")["model"] for label in runs if (root / label / "config.json").is_file()}
    owners = {}   # 출발 모델 → 그것을 쓰는 (from_sft 가 아닌) 모델들
    for label, m in models.items():
        if not runs[label].get("from_sft"):
            owners.setdefault(m, []).append(label)
    sf = sw.get("_start_from")
    sf_model = read_json(sf / "config.json")["model"] if sf else None
    starts = []
    for m, labels in owners.items():
        own = next((label for label in labels if (workdir_of(sw, label, smoke) / "reports" / "start.json").exists()), None)
        if own:
            wd = workdir_of(sw, own, smoke)
            name = f"출발 모델 ({short(m)})" if len(owners) > 1 else "출발 모델"
            starts.append((wd / "reports" / "start.json", wd, root / own / "data", name, None))
        elif sf and sf_model == m:
            starts.append((sf / "reports" / "start.json", sf, Path(read_json(sf / "config.json")["data"]["output_dir"]),
                           f"출발 모델 ({sf.parent.name}/{sf.name})", labels[0]))
    for r in sw["runs"]:
        label = r["label"]
        wd = workdir_of(sw, label, smoke)
        rep = wd / "reports"
        grpo = sorted(rep.glob("grpo-*.json"), key=lambda p: p.stat().st_mtime) if part_of(sw, r) != "sft" else []
        if r.get("from_sft"):   # SFT 는 부모와 같아 GRPO 줄만
            picks = [(grpo[-1], label)] if grpo else []
        else:
            picks = [(rep / "sft.json", label)] + ([(grpo[-1], f"{label} GRPO")] if grpo else [])
        picks = [(p, name) for p, name in picks if p.exists()]
        if not picks:
            continue
        try:
            sig, fac = _images(wd, root / label / "data")
        except (OSError, KeyError, ValueError) as exc:
            notes.append(f"{label}: 비교 제외 (평가 문항을 읽지 못함: {exc})")
            continue
        if ref is None:
            ref, factor = sig, fac
        elif sig != ref:
            notes.append(f"{label}: 비교 제외 (평가 문항 또는 평가 그림 설정이 다른 모델과 다름)")
            continue
        elif fac != factor:
            notes.append(f"{label}: 출발 모델 규격이 달라 평가 그림 크기가 조금 다름 (그림 조각 {fac}px, 다른 모델 {factor}px). "
                         "문항은 같아 표에 넣음")
        for p, name in picks:
            reports.append({**read_json(p), "label": name})
            sources[name] = (wd, root / label / "data")
    head = []
    for path, wd, data, name, first in starts:
        if ref is None:
            break
        try:
            ok = _images(wd, data)[0] == ref and read_json(path)["items_sha256"] == reports[0]["items_sha256"]
        except (OSError, KeyError, ValueError):
            ok = False
        if ok:
            head.append({**read_json(path), "label": name})
            sources[name] = (wd, data)
        else:
            sw["_start_mismatch"] = first   # start_from 을 못 쓰면 그 출발 모델의 첫 모델에서 평가
            notes.append(f"출발 모델 평가({path})는 평가 문항·그림 설정이 달라 표에서 뺍니다")
    return head + reports, notes


def compare(sw, smoke=False):
    """끝난 모델들의 점수를 한 표로: <root>/compare.{csv,md,html}."""
    from .report import _build_reports

    root = sw["_root"]
    reports, notes = collect(sw, smoke)
    out = root / "compare.csv"
    if not reports:
        return None
    try:
        result = _build_reports(reports, out, check_images=False)
    except ValueError as exc:
        notes.append(f"비교표를 만들지 못함: {exc}")
        result = None
    (root / "compare_notes.txt").write_text("\n".join(notes) + ("\n" if notes else ""), encoding="utf-8")
    for n in notes:
        log("WARNING: " + n)
    if result:
        _header(sw, root / "compare.md", root / "compare.html", notes, reports)
        log(f"비교표 → {root / 'compare.html'} ({', '.join(result['models'])})")
        from .summary import write_own

        write_own([(sw, reports, notes)], root / "summary.html")   # 한 화면 (실험 모아 보기와 같은 꼴, 이 묶음의 모델만)
        from .answers import write_own as write_answers

        write_answers(reports, sw["_sources"], root / "answers.html", sw["name"], baseline(sw))   # 문항별 모델 답
    return result


LOWER = {"cer", "false_alarm", "matched_label_cer", "extra_key"}


def _overview(sw, reports):
    """한눈에 보기: 평가 세트·과제마다 주 지표 한 줄, 열은 모델. 괄호는 기준 모델(baseline, 기본 첫 모델) 대비 %p.

    평가 세트(id)를 나눠 둔 설정이면 세트별로, 아니면 과제별로. 세트별 자세한 표는 아래 본문."""
    base = baseline(sw)
    ref = next((r for r in reports if r["label"] == base), None)

    def scopes(r):
        if r.get("benchmarks"):
            return {(b.get("name") or i, i): b["tasks"] for i, b in r["benchmarks"].items()}
        return {("", ""): r["tasks"]}

    rows = []
    first = scopes(reports[0])
    for (name, ident), tasks in first.items():
        for task, t in tasks.items():
            metric = t["main"]
            cells = []
            for r in reports:
                v = scopes(r).get((name, ident), {}).get(task, {}).get("metrics", {}).get(metric)
                b = scopes(ref).get((name, ident), {}).get(task, {}).get("metrics", {}).get(metric) if ref else None
                d = None if v is None or b is None or r is ref or r["label"].startswith("출발 모델") else (v - b) * 100
                cells.append((v, d))
            rows.append((ident or "", task, metric + (" ↓" if metric in LOWER else ""), t.get("n"), metric in LOWER, cells))
    return base, rows


def _spec(sw, r):
    try:
        return spec(sw, r) if sw else r
    except (ValueError, KeyError):
        return r


def train(r, sw=None):
    """모델의 학습 데이터 (html, 줄마다 하나). 적지 않았으면 base 의 학습 데이터."""
    s = _spec(sw, r)
    if "train" not in s:
        return "<i>공통 (base)</i>"
    return "<br>".join(html.escape(e if isinstance(e, str) else e["path"] + (f" (count {e['count']})" if e.get("count") is not None else ""))
                       for e in s["train"])


def changes(r, sw=None):
    """base 와 달라진 칸 (학습 데이터 말고): 'sft.learning_rate=5e-05 · 출발 모델 qwen3/vl-8b' 꼴. 없으면 ''."""
    s = _spec(sw, r)
    out = []

    def flat(prefix, v):
        if isinstance(v, dict) and v:
            for k, x in v.items():
                flat(f"{prefix}.{k}", x)
        else:
            out.append(f"{prefix}={v if not isinstance(v, (list, dict)) else json.dumps(v, ensure_ascii=False)}")
    if r.get("from_sft"):
        out.append(f"{r['from_sft']} 의 SFT 에서 GRPO")
    if s.get("model"):
        out.append(f"출발 모델 {short(s['model'])}")
    for k in ("model_type", "gpus"):
        if k in s:
            out.append(f"{k}={s[k]}")
    for k in ("data", "sft", "grpo", "set"):
        if s.get(k):
            flat(k, s[k])
    if s.get("deploy"):
        out.append("평가 서버 명령 바꿈")
    if part_of(sw or {}, r) == "all":
        out.append("GRPO 까지")
    return " · ".join(out)


def _header(sw, md, page, notes, reports=()):
    """비교표(.md·.html) 맨 위에 실험 이름·설명·모델별 설명과 학습 데이터, 한눈에 보기 표."""
    head = [f"# {sw['name']}", "", sw["about"], ""]
    if sw.get("record"):
        head += [f"기록: {sw['record']}", ""]
    head += ["| 모델 | 설명 | 바꾼 설정 | 학습 데이터 |", "|---|---|---|---|"]
    head += [f"| {r['label']} | {r['about']} | {changes(r, sw)} | {train(r, sw)} |" for r in sw["runs"]]
    head += ["", *[f"- {n}" for n in notes], ""] if notes else [""]
    labels = [r["label"] for r in reports]
    base, rows = _overview(sw, reports) if reports else (None, [])

    def cell(v, d):
        return "—" if v is None else f"{v * 100:.1f}" + ("" if d is None else f" ({d:+.1f})")
    if rows:
        head += ["## 한눈에 보기", "", f"점수 %, 괄호는 기준 모델 `{base}` 대비 %p (↓ 는 낮을수록 좋음). 평가 세트별 자세한 표는 아래.", "",
                 "| 평가 세트 | 과제 | 지표 | 문항 수 | " + " | ".join(labels) + " |", "|---" * (4 + len(labels)) + "|"]
        head += [f"| {i} | {t} | {m} | {n} | " + " | ".join(cell(v, d) for v, d in cells) + " |" for i, t, m, n, _, cells in rows]
        head += [""]
    md.write_text("\n".join(head) + "\n" + md.read_text(encoding="utf-8"), encoding="utf-8")
    e = html.escape
    block = (f"<h1>{e(sw['name'])}</h1><p>{e(sw['about'])}</p>" + (f"<p>기록: {e(sw['record'])}</p>" if sw.get("record") else "")
             + "<table><tr><th>모델</th><th>설명</th><th>바꾼 설정</th><th>학습 데이터</th></tr>"
             + "".join(f"<tr><td>{e(r['label'])}</td><td>{e(r['about'])}</td><td>{e(changes(r, sw))}</td><td>{train(r, sw)}</td></tr>"
                       for r in sw["runs"])
             + "</table>" + "".join(f"<p>{e(n)}</p>" for n in notes))
    if rows:
        def td(v, d, lower):
            if v is None:
                return "<td>—</td>"
            color = "" if d is None or abs(d) < 0.05 else ("#1a7f37" if (d > 0) != lower else "#cf222e")
            return f"<td>{v * 100:.1f}" + ("" if d is None else f" <span style='color:{color or '#666'}'>({d:+.1f})</span>") + "</td>"
        block += (f"<h2>한눈에 보기</h2><p>점수 %, 괄호는 기준 모델 <b>{e(base)}</b> 대비 %p (초록 = 좋아짐, 빨강 = 나빠짐, ↓ 는 낮을수록 좋음). "
                  "평가 세트별 자세한 표는 아래.</p><table><tr><th>평가 세트</th><th>과제</th><th>지표</th><th>문항 수</th>"
                  + "".join(f"<th>{e(l)}</th>" for l in labels) + "</tr>"
                  + "".join(f"<tr><td>{e(i)}</td><td>{e(t)}</td><td>{e(m)}</td><td>{n if n is not None else ''}</td>"
                            + "".join(td(v, d, lower) for v, d in cells) + "</tr>" for i, t, m, n, lower, cells in rows)
                  + "</table>")
    text = page.read_text(encoding="utf-8")
    i = text.find("<h1>")
    page.write_text(text[:i] + block + text[i:] if i >= 0 else text, encoding="utf-8")


def show_status(sw, smoke=False):
    root = sw["_root"]
    status = read_json(root / "sweep.json") if (root / "sweep.json").exists() else {}
    lock = root / "sweep.lock"
    alive = False
    if lock.exists():
        try:
            os.kill(int(lock.read_text().strip()), 0)
            alive = True
        except (OSError, ValueError):
            pass
    print(f"{sw['name']}: {sw['about']}  ({root})  {'돌고 있음' if alive else '멈춰 있음'}")
    for r in sw["runs"]:
        label, s = r["label"], status.get(r["label"], {})
        state = workdir_of(sw, label, smoke) / "state.json"
        done = read_json(state).get("done", []) if state.exists() else []
        st = s.get("status", "대기")
        if st == "running" and not alive:
            st = "끊김 (다시 실행하면 이어서)"
        elif st == "running" and s.get("gpus") is not None:
            st = f"running (GPU {','.join(map(str, s['gpus']))})"
        print(f"  {label:20s} {st:10s} {r['about']}\n  {'':20s} 끝난 단계: {', '.join(done) or '-'}" + (f"  ({s['why']})" if s.get("why") else ""))
    if (root / "compare.html").exists():
        print(f"비교표: {root / 'compare.md'} · {root / 'compare.html'} · 한 화면 {root / 'summary.html'} · 문항별 답 {root / 'answers.html'}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m train sweep", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", required=True, help="묶음 파일 (JSON)")
    p.add_argument("--status", action="store_true", help="진행 상황만 보기")
    p.add_argument("--smoke", action="store_true", help="모델마다 5 step 리허설")
    a = p.parse_args(argv)
    if a.status:
        show_status(load(a.config), a.smoke)
    else:
        run(a.config, a.smoke)
