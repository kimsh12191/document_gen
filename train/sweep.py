"""실험 묶음: 평가 세트는 고정하고 학습 쪽 설정을 바꾼 모델 여러 개를 차례로(또는 GPU 를 나눠 동시에) 학습·평가하고 보고서 하나로.

  python -m train sweep --config <묶음.json>            돌림 (다시 치면 이어서, 끝난 모델은 건너뜀)
  python -m train sweep --config <묶음.json> --status   진행 상황과 모델 경로
  python -m train sweep --config <묶음.json> --smoke    모델마다 5 step 리허설 (<root>/<label>/smoke)

묶음 파일 (상대 경로는 이 파일이 있는 폴더 기준, base 안의 경로는 base 파일 기준):
  {"name": "E02-tune", "about": "무엇을 확인하는 실험인지", "record": "experiments/E02-tune.md",
   "base": "pipeline.json", "root": "../runs/E02-tune", "baseline": "a1", "gpu_groups": [[0, 1], [2, 3]],
   "runs": [{"label": "a1", "about": "기준 (base 그대로)"},
            {"label": "a2-lr", "about": "학습률·에폭", "sft": {"learning_rate": 5e-5, "num_train_epochs": 2}},
            {"label": "a3-data", "about": "밖에서 가져온 swift 데이터 더함",
             "train": ["<데이터셋>", {"path": "<가져온 것>.jsonl", "format": "swift", "count": 20000}], "data": {"task_mix": {"kie": 0.3}}},
            {"label": "a4-vl", "about": "다른 출발 모델", "model": "/share/…/qwen3-vl-8b", "model_type": "qwen3_vl"}]}
- 모델마다 적지 않은 칸은 base 값. 바꿀 수 있는 칸 (RUN_KEYS):
  model · model_type   출발 모델 (다르면 그 출발 모델도 평가 — 같은 출발 모델은 캐시로 한 번만)
  template             ms-swift --template (기본 model_type; 모델 폴더 이름으로 못 고를 때)
  train                학습 데이터 목록 (= data.train)
  data                 섞기 칸: task_mix · sft_max_examples · image_max_size · max_image_tokens_per_sample · sft_max_length · seed …
  sft                  "config"(yaml 파일) + yaml 안의 ms-swift 옵션을 칸 하나씩 (learning_rate, lora_rank …)
  gpus                 이 모델만 쓸 GPU · deploy: 평가 서버 명령(eval.deploy_command) · set: 그 밖의 설정 칸 덮어쓰기
- 평가는 고정: data.benchmark(채점 함수 포함)·eval.inference_config 는 모델마다 바꿀 수 없고, 평가 세트는 돌리기 전에 base 의
  그림 예산·출발 모델로 한 번 준비해 모든 모델이 같은 문항·그림으로 잰다.
- gpu_groups 를 적으면 비는 GPU 묶음에 다음 모델을 넣어 동시에 돌린다 (평가 서버 포트·MASTER_PORT 는 묶음마다 다르게).
  없으면 하나씩. 모델의 gpus 를 적으면 그 GPU 가 모두 빌 때 들어간다.
- baseline: 보고서 괄호 %p 의 기준 모델 label (기본 첫 모델). 출발 모델도 줄로 들어간다.
- name·about, runs 마다 label·about 은 꼭 적는다. label 은 모델 이름이자 폴더 이름 (<root>/<label>/ 가 workdir).
- 모델 하나가 실패해도 다음 모델로 간다 (<root>/sweep.json 상태, <root>/<label>/sweep.log).
- 모델 하나가 끝날 때마다 <root>/report.html · answers.html · scores.csv · results.json(모델 경로) 을 다시 만든다.
- 이미 돈 모델의 설정이 바뀌면 그 모델은 돌리지 않는다 (새 label 로).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

from docgen.bench.ocr_data import read_json, write_json

from .settings import load_settings, log, merged

ROOT = Path(__file__).resolve().parents[1]
LABEL = re.compile(r"[a-z0-9][a-z0-9-]*")
RUN_KEYS = {"label", "about", "model", "model_type", "template", "train", "data", "sft", "gpus", "deploy", "set"}
SWEEP_KEYS = {"name", "about", "record", "base", "root", "baseline", "gpu_groups", "runs"}
GONE = {"part": "GRPO 는 이 브랜치에서 뺐습니다 (SFT 까지만)", "from_sft": "GRPO 는 이 브랜치에서 뺐습니다",
        "grpo": "GRPO 는 이 브랜치에서 뺐습니다", "start_from": "필요 없음: 같은 출발 모델·평가 세트의 답은 cache_dir 에서 그대로 씀"}
FIXED = [("data", "benchmark"), ("data", "output_dir"), ("data", "prepared_sets"), ("eval", "inference_config"),
         ("workdir",), ("cache_dir",)]   # 평가를 고정하려고 모델마다 못 바꾸는 칸 (workdir·output_dir 는 묶음이 정함)
MASTER_PORT = 29500


def load(path):
    path = Path(path).resolve()
    sw = load_settings(path)
    for k in ("name", "about", "base", "root", "runs"):
        if not sw.get(k):
            raise ValueError(f"묶음 파일에 {k} 가 없습니다 (about: 무엇을 확인하는 실험인지)")
    old = [f"{k}: {GONE[k]}" for k in sw if k in GONE] + [f"{r.get('label')}.{k}: {GONE[k]}" for r in sw["runs"] for k in r if k in GONE]
    if old:
        raise ValueError("묶음 파일에 없어진 칸이 있습니다:\n  " + "\n  ".join(old))
    unknown = set(sw) - SWEEP_KEYS
    if unknown:
        raise ValueError(f"묶음 파일의 모르는 칸 {sorted(unknown)} (쓸 수 있는 칸: {', '.join(sorted(SWEEP_KEYS))})")
    labels = [r.get("label") for r in sw["runs"]]
    bad = [x for x in labels if not isinstance(x, str) or not LABEL.fullmatch(x)]
    if bad or len(set(labels)) != len(labels):
        raise ValueError(f"runs.label 은 겹치지 않는 영문 소문자·숫자·- 여야 합니다: {bad or labels}")
    for r in sw["runs"]:
        if not str(r.get("about", "")).strip():
            raise ValueError(f"{r['label']}: about (이 모델이 무엇인지) 이 있어야 합니다")
        unknown = set(r) - RUN_KEYS
        if unknown:
            raise ValueError(f"{r['label']}: 모르는 칸 {sorted(unknown)} (쓸 수 있는 칸: {', '.join(sorted(RUN_KEYS))}; 그 밖의 칸은 set 으로)")
        if "train" in r and not r["train"]:
            raise ValueError(f"{r['label']}: train 이 비었습니다 (base 의 학습 데이터를 쓰려면 train 칸을 지우세요)")
    if sw.get("baseline") and sw["baseline"] not in labels:
        raise ValueError(f"baseline 은 runs 의 label 이어야 합니다: {sw['baseline']}")
    groups = sw.get("gpu_groups") or []
    flat = [g for grp in groups for g in grp] if isinstance(groups, list) and all(isinstance(x, list) and x for x in groups) else None
    if flat is None or any(not isinstance(g, int) for g in flat) or len(set(flat)) != len(flat):
        raise ValueError(f"gpu_groups 는 겹치지 않는 GPU 번호 묶음 목록이어야 합니다 (예: [[0, 1], [2, 3]]): {groups}")
    sw["_dir"] = path.parent
    sw["_file"] = path
    sw["_root"] = (path.parent / sw["root"]).resolve()
    return sw


def base_config(sw):
    """base 파일을 절대 경로로 (평가 세트·OCR 준비·cache_dir 는 모든 모델이 이것)."""
    from .pipeline import resolve

    from .pipeline import drop_removed

    path = (sw["_dir"] / sw["base"]).resolve()
    raw = drop_removed(load_settings(path))
    raw.setdefault("workdir", str(sw["_root"] / "_base"))
    cfg = resolve(raw, path.parent)
    if not load_settings(path).get("cache_dir"):
        cfg["cache_dir"] = str(sw["_root"].parent / "_cache")
    return cfg


def _fixed(over, label):
    for keys in FIXED:
        v = over
        for k in keys:
            v = v.get(k, None) if isinstance(v, dict) else None
        if v is not None:
            raise ValueError(f"{label}: {'.'.join(keys)} 는 모델마다 바꿀 수 없습니다 (평가 고정·묶음이 정함). base 에서 바꾸세요")


def run_config(sw, run, base=None, sets=None):
    """모델 하나의 학습 설정: base + 이 모델의 칸, 경로는 모두 절대 경로로."""
    from .benchmarks import resolve as res_entries
    from .serve import conf_path

    base = base or base_config(sw)
    here, label = sw["_dir"], run["label"]
    _fixed(run.get("set") or {}, label)
    _fixed({"data": run.get("data") or {}}, label)
    cfg = merged(base, run.get("set") or {})
    if run.get("model"):
        cfg["model"] = run["model"] if Path(run["model"]).is_absolute() else str((here / run["model"]).resolve())
    if "model_type" in run and "template" not in run:
        cfg.pop("template", None)   # 다른 모델 종류에 base 의 template 을 물려주지 않는다
    for k in ("model_type", "template", "gpus"):
        if k in run:
            cfg[k] = run[k]
    if run.get("deploy"):
        cfg["eval"] = {**cfg["eval"], "deploy_command": run["deploy"]}
    if run.get("sft"):
        own = dict(run["sft"])
        if own.get("config"):
            own["config"] = conf_path(own["config"], here)
        cfg["sft"] = merged(cfg["sft"], own)
    workdir = sw["_root"] / label
    cfg["data"] = {**cfg["data"], **(run.get("data") or {}), "output_dir": str(workdir / "data")}
    if "train" in run:
        cfg["data"]["train"] = res_entries(run["train"], here)   # 묶음 파일 기준
    if sets:
        cfg["data"]["prepared_sets"] = sets
    cfg["workdir"] = str(workdir)
    cfg["sweep"] = sw["name"]
    return cfg


def same_model(a, b):
    """설정이 같은 모델인지 (GPU·포트·준비한 평가 세트 폴더는 모델과 상관없다)."""
    def strip(c):
        return {**{k: v for k, v in c.items() if k != "gpus"}, "data": {k: v for k, v in c["data"].items() if k != "prepared_sets"},
                "eval": {k: v for k, v in (c.get("eval") or {}).items() if k != "port_base"}}
    return strip(a) == strip(b)


def default_runner(config: Path, log_path: Path, smoke: bool, env: dict | None = None) -> int:
    cmd = [sys.executable, "-m", "train", "--config", str(config)] + (["--smoke"] if smoke else [])
    with log_path.open("a", encoding="utf-8") as out:
        out.write(time.strftime("[%Y-%m-%d %H:%M:%S] $ ") + " ".join(cmd) + "\n")
        out.flush()
        return subprocess.run(cmd, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT,
                              env={**os.environ, **(env or {}), "PYTHONIOENCODING": "utf-8"}).returncode


def workdir_of(sw, label, smoke):
    return sw["_root"] / label / ("smoke" if smoke else "")


def finished(sw, run, smoke):
    state = workdir_of(sw, run["label"], smoke) / "state.json"
    return state.exists() and "eval_sft" in read_json(state).get("done", [])


def preflight(sw, base):
    """돌리기 전에 모든 모델의 설정을 한꺼번에 검사한다. 틀린 것이 있으면 하나도 돌리지 않는다."""
    from .benchmarks import normalize, train_entries
    from .pipeline import FOLDER_HINT

    problems = []
    try:
        for b in normalize(base["data"]["benchmark"]):
            for p in b["paths"]:
                ok = (Path(p).is_file() if b.get("format") else (Path(p) / "meta.json").is_file() and (Path(p) / "tasks").is_dir())
                if not ok:
                    problems.append(f"base 의 data.benchmark {b['id']}: 경로가 없거나 {FOLDER_HINT} 가 아닙니다: {p}")
    except ValueError as exc:
        problems.append(f"base 의 data.benchmark: {exc}")
    for r in sw["runs"]:
        label = r["label"]
        try:
            cfg = run_config(sw, r, base)
            entries = train_entries(cfg["data"]["train"])
        except (OSError, ValueError, KeyError, TypeError) as exc:
            problems.append(f"{label}: 설정을 만들지 못함 ({exc})")
            continue
        if not (Path(cfg["model"]) / "config.json").is_file():
            problems.append(f"{label}: 출발 모델 폴더(config.json)가 없습니다: {cfg['model']}")
        if not Path(cfg["sft"]["config"]).is_file():
            problems.append(f"{label}: sft.config 파일이 없습니다: {cfg['sft']['config']}")
        for e in entries:
            p = e["path"]
            ok = (Path(p).is_file() if e.get("format") else (Path(p) / "meta.json").is_file() and (Path(p) / "tasks").is_dir())
            if not ok:
                problems.append(f"{label}: train 경로가 없거나 {FOLDER_HINT} 가 아닙니다: {p}")
        if r.get("gpus") and sw.get("gpu_groups") and not set(r["gpus"]) <= {g for grp in sw["gpu_groups"] for g in grp}:
            problems.append(f"{label}: gpus {r['gpus']} 가 gpu_groups 밖에 있습니다")
    problems = list(dict.fromkeys(problems))
    if problems:
        raise SystemExit(f"묶음 {sw['_file']} 를 돌리기 전에 고칠 것 ({len(problems)}건, 아무 모델도 시작하지 않았습니다):\n  "
                         + "\n  ".join(problems))


def run(sweep_path, smoke=False, runner=default_runner):
    from .pipeline import benchmark_sets

    sw = load(sweep_path)
    base = base_config(sw)
    preflight(sw, base)
    root = sw["_root"]
    root.mkdir(parents=True, exist_ok=True)
    lock = root / "sweep.lock"
    if lock.exists():
        try:
            os.kill(int(lock.read_text().strip() or 0), 0)
            raise SystemExit(f"이미 돌고 있습니다 (pid {lock.read_text().strip()}). 진행 상황: --status")
        except (OSError, ValueError):
            pass   # 끝난 실행이 남긴 잠금
    lock.write_text(str(os.getpid()))
    write_json(root / "sweep.config.json", {k: v for k, v in sw.items() if not k.startswith("_")})
    status_path = root / "sweep.json"
    status = read_json(status_path) if status_path.exists() else {}
    groups = sw.get("gpu_groups") or []
    busy, used = {}, set()
    n = len(sw["runs"])

    def note(label, **kw):
        status[label] = {**kw, "at": time.strftime("%Y-%m-%d %H:%M")}
        write_json(status_path, status)

    try:
        sets = benchmark_sets(base)   # 모든 모델이 같이 쓰는 평가 세트를 먼저 한 번
        log(f"평가 세트 {len(sets)}개: " + ", ".join(Path(d).name for d in sets.values()))

        def launch(i, r, cfg, gpus, pool):
            label = r["label"]
            folder = root / label
            folder.mkdir(parents=True, exist_ok=True)
            cpath = folder / "config.json"
            if cpath.exists() and not same_model(read_json(cpath), cfg):
                note(label, status="failed", why="이미 돈 모델의 설정이 바뀜 (base·train·칸). 새 label 로 추가하세요")
                log(f"{label}: 설정이 바뀌어 건너뜁니다 ({cpath})")
                return None
            write_json(cpath, cfg)
            if finished(sw, r, smoke) and status.get(label, {}).get("status") == "done":
                log(f"{label}: 끝남 (건너뜀)")
                return None
            env = {"MASTER_PORT": str(MASTER_PORT + min(gpus))} if groups else {}
            log(f"=== {label} ({i + 1}/{n}, GPU {','.join(map(str, gpus))}) → {folder / 'sweep.log'}")
            status[label] = {"status": "running", "started": time.strftime("%Y-%m-%d %H:%M"), "pid": os.getpid(), "gpus": gpus}
            write_json(status_path, status)
            return pool.submit(runner, cpath, folder / "sweep.log", smoke, env)

        def pick(r, cfg):
            """이 모델에 줄 GPU (지금 비어 있는 것), 없으면 None."""
            if not groups:
                return list(cfg["gpus"]) if not busy else None
            for want in ([r["gpus"]] if r.get("gpus") else groups):
                if not set(want) & used:
                    return list(want)
            return None

        todo = list(enumerate(sw["runs"]))
        with ThreadPoolExecutor(max_workers=max(1, len(groups))) as pool:
            while todo or busy:
                for i, r in list(todo):
                    cfg = run_config(sw, r, base, sets)
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
                    if todo:
                        continue   # 건너뛴 모델만 있었다: 다음 모델로
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
                    note(label, status="done" if ok else "failed", hours=hours, gpus=gpus,
                         **({} if ok else {"why": f"종료 코드 {code}, 로그 {root / label / 'sweep.log'}"}))
                    log(f"{label}: {'끝' if ok else '실패 — 다음 모델로'} ({hours} h)")
                    report(sw, smoke)
        report(sw, smoke)
    finally:
        lock.unlink(missing_ok=True)


# -- 보고서 ----------------------------------------------------------------------------------
def short(model):
    return "/".join(Path(str(model)).parts[-2:])


def train_text(r):
    """모델의 학습 데이터 (줄마다 하나). 적지 않았으면 base."""
    if "train" not in r:
        return ["공통 (base)"]
    return [e if isinstance(e, str) else e["path"] + (f" ({e['format']})" if e.get("format") else "")
            + (f" (count {e['count']})" if e.get("count") is not None else "") for e in r["train"]]


def changes(r):
    """base 와 달라진 칸 (학습 데이터 말고): 'sft.learning_rate=5e-05 · 출발 모델 qwen3/vl-8b' 꼴."""
    out = []

    def flat(prefix, v):
        if isinstance(v, dict) and v:
            for k, x in v.items():
                flat(f"{prefix}.{k}", x)
        else:
            out.append(f"{prefix}={v if not isinstance(v, (list, dict)) else json.dumps(v, ensure_ascii=False)}")
    if r.get("model"):
        out.append(f"출발 모델 {short(r['model'])}")
    for k in ("model_type", "template", "gpus"):
        if k in r:
            out.append(f"{k}={r[k]}")
    for k in ("data", "sft", "set"):
        if r.get(k):
            flat(k, r[k])
    if r.get("deploy"):
        out.append("평가 서버 명령 바꿈")
    return " · ".join(out)


def results(sw, smoke=False):
    """묶음의 results.json: 출발 모델(서로 다른 것마다 하나) + 모델마다 SFT, 모델 경로와 평가 세트별 답."""
    starts, models = {}, []
    for r in sw["runs"]:
        state = workdir_of(sw, r["label"], smoke) / "state.json"
        st = read_json(state) if state.exists() else {}
        start = (st.get("models") or {}).get("start")
        if start and start["model"] not in starts:
            starts[start["model"]] = start
        sft = (st.get("models") or {}).get("sft")
        if sft:
            models.append({**sft, "label": r["label"], "about": r["about"], "changes": changes(r), "train": train_text(r)})
    heads = [{**s, "label": "출발 모델" + (f" ({short(m)})" if len(starts) > 1 else ""), "about": "학습 전"} for m, s in starts.items()]
    return {"name": sw["name"], "about": sw["about"], "record": sw.get("record"),
            "baseline": sw.get("baseline") or sw["runs"][0]["label"], "models": heads + models}


def report(sw, smoke=False):
    from .report import write_safe

    res = results(sw, smoke)
    out = sw["_root"] / ("smoke" if smoke else "")
    write_json(out / "results.json", res)
    return write_safe(res, out)


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
        st = read_json(state) if state.exists() else {}
        sft = (st.get("models") or {}).get("sft") or {}
        state_text = s.get("status", "대기")
        if state_text == "running" and not alive:
            state_text = "끊김 (다시 실행하면 이어서)"
        elif state_text == "running" and s.get("gpus") is not None:
            state_text = f"running (GPU {','.join(map(str, s['gpus']))})"
        print(f"  {label:20s} {state_text:10s} {r['about']}\n  {'':20s} 끝난 단계: {', '.join(st.get('done', [])) or '-'}"
              + (f"  ({s['why']})" if s.get("why") else ""))
        if sft.get("model"):
            print(f"  {'':20s} 모델: {sft['model']}\n  {'':20s} SFT 체크포인트: {sft.get('checkpoint')}")
    out = root / ("smoke" if smoke else "")
    if (out / "report.html").exists():
        print(f"보고서: {out / 'report.html'} · 문항별 답 {out / 'answers.html'} · 모델 경로 {out / 'results.json'}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m train sweep", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", required=True, help="묶음 파일 (JSON)")
    p.add_argument("--status", action="store_true", help="진행 상황과 모델 경로만 보기")
    p.add_argument("--smoke", action="store_true", help="모델마다 5 step 리허설")
    a = p.parse_args(argv)
    if a.status:
        show_status(load(a.config), a.smoke)
    else:
        run(a.config, a.smoke)
