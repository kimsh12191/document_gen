"""실험 묶음: 학습 데이터만 바꾼 모델 여러 개를 차례로 학습·평가하고 비교표 하나로 (python -m train sweep).

  python -m train sweep --config <묶음.json>            차례로 돌림 (다시 치면 이어서, 끝난 모델은 건너뜀)
  python -m train sweep --config <묶음.json> --status   진행 상황과 비교표 위치
  python -m train sweep --config <묶음.json> --smoke    모델마다 5 step 리허설 (<root>/<label>/smoke)

묶음 파일 (상대 경로는 이 파일이 있는 폴더 기준):
  {"name": "E01-realocr", "about": "무엇을 확인하는 실험인지", "record": "experiments/E01-realocr.md",
   "base": "pipeline.e01.json", "root": "../runs/E01-realocr", "part": "sft", "start_from": "../runs/E00-x/a1",
   "runs": [{"label": "a1-syn", "about": "기준: 합성만, 하나은행 서식 제외", "train": ["<데이터셋>", {"path": "<OCR 준비>", "count": 20000}]},
            {"label": "a2-synreal", "about": "기준 + 실서류 OCR", "train": [...], "part": "all", "set": {...}}]}
- name·about, runs 마다 about 은 꼭 적는다 (진행 상황·비교표 맨 위·<root>/sweep.config.json 에 남는다). record 는 실험 기록 파일 (선택).
- label 은 이 실험 안의 모델 이름이자 폴더 이름 (<root>/<label>/).
- part: "sft"(SFT 까지, 기본) | "all"(SFT + GRPO). 묶음 전체에, runs 마다 덮어쓸 수 있다.
  sft 로 끝난 모델을 all 로 바꿔 다시 치면 SFT 는 건너뛰고 GRPO 만 돈다 (base 의 grpo.select 가 mine 이어야 SFT 평가 때 후보 답을 내 둔다).
- start_from: 다른 묶음의 모델 폴더. 그 출발 모델 평가(reports/start.json)를 가져다 쓰고 이 묶음에서는 출발 모델을 평가하지 않는다.
  평가 문항·그림 설정이 다르면 쓰지 않고 첫 모델에서 출발 모델 평가를 돌린다.
- base: 공통 파이프라인 설정 (model, sft, data.benchmark, eval …). 모델마다 다른 것은 train(data.train) 뿐이 원칙.
  set 은 그 모델만 base 에 덮어쓸 칸 (꼭 필요할 때만, 비교표 해석이 달라진다).
- 모델마다 <root>/<label>/ 가 workdir, <root>/<label>/data 가 data.output_dir, 쓴 설정은 <root>/<label>/config.json.
- 출발 모델 평가는 첫 모델에서만 (나머지는 eval.skip_start), start_from 이 있으면 하지 않는다. 평가 문항·그림이 같은지는 비교표를 만들 때 확인한다.
- 모델 하나가 실패해도 다음 모델로 간다 (<root>/sweep.json 상태, <root>/<label>/sweep.log).
- 모델 하나가 끝날 때마다 <root>/compare.{csv,md,html} 를 다시 만든다.
- 이미 돈 모델의 설정이 바뀌면 그 모델은 돌리지 않는다 (새 label 로).
"""
import argparse
import html
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from docgen.bench.ocr_data import read_json, read_jsonl, write_json

from .cli import resolve_data
from .settings import load_settings

ROOT = Path(__file__).resolve().parents[1]
LABEL = re.compile(r"[a-z0-9][a-z0-9-]*")
DONE_PARTS = {"sft": "eval_sft", "all": "eval_grpo"}


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
    if any(not r.get("train") or not str(r.get("about", "")).strip() for r in sw["runs"]):
        raise ValueError("runs 마다 train 과 about (이 모델이 무엇인지) 이 있어야 합니다")
    if any(part_of(sw, r) not in DONE_PARTS for r in sw["runs"]):
        raise ValueError("part 는 sft (SFT 까지) · all (SFT + GRPO)")
    sw["_dir"] = path.parent
    sw["_file"] = path
    sw["_root"] = (path.parent / sw["root"]).resolve()
    if sw.get("start_from"):
        sf = (path.parent / sw["start_from"]).resolve()
        if not (sf / "config.json").is_file() or not (sf / "reports" / "start.json").is_file():
            raise ValueError(f"start_from 은 출발 모델 평가를 마친 다른 묶음의 모델 폴더여야 합니다 (config.json·reports/start.json): {sf}")
        sw["_start_from"] = sf
    return sw


def part_of(sw, run):
    return run.get("part") or sw.get("part", "sft")


def run_config(sw, run, first):
    """모델 하나의 파이프라인 설정: base + 이 모델의 train(+ set), 경로는 모두 절대 경로로."""
    from .pipeline import merged

    base_path = (sw["_dir"] / sw["base"]).resolve()
    base, at = load_settings(base_path), base_path.parent
    cfg = merged(base, run.get("set") or {})
    workdir = sw["_root"] / run["label"]
    cfg["data"] = {**cfg["data"], "train": run["train"], "output_dir": str(workdir / "data")}
    data = resolve_data({"data": {**cfg["data"], "train": []}}, at)   # benchmark 는 base 기준
    data["train"] = resolve_data({"data": {**cfg["data"], "benchmark": []}}, sw["_dir"])["train"]   # train 은 묶음 파일 기준
    cfg["data"] = data
    cfg["workdir"] = str(workdir)
    for sec, key in (("sft", "config"), ("grpo", "config"), ("eval", "inference_config")):
        p = (cfg.get(sec) or {}).get(key)
        if p and not Path(p).is_absolute() and (at / p).exists():   # 없으면 이름 그대로 (train/configs 의 기본 파일)
            cfg[sec][key] = str((at / p).resolve())
    if cfg.get("ocr_prepare"):
        ocr = cfg["ocr_prepare"]
        cfg["ocr_prepare"] = [p if Path(p).is_absolute() else str((at / p).resolve()) for p in (ocr if isinstance(ocr, list) else [ocr])]
    cfg.setdefault("eval", {})["skip_start"] = not first or "_start_from" in sw
    return cfg


def same_model(a, b):
    """설정이 같은 모델인지 (출발 모델 평가를 건너뛰는지 여부는 모델과 상관없다)."""
    def strip(c):
        return {**c, "eval": {k: v for k, v in (c.get("eval") or {}).items() if k != "skip_start"}}
    return strip(a) == strip(b)


def default_runner(config: Path, log_path: Path, part: str, smoke: bool, only: str | None = None) -> int:
    cmd = [sys.executable, "-m", "train", "--config", str(config)]
    cmd += ["--only", only] if only else ([] if part == "all" else ["--part", part])
    cmd += ["--smoke"] if smoke else []
    with log_path.open("a", encoding="utf-8") as out:
        out.write(time.strftime("[%Y-%m-%d %H:%M:%S] $ ") + " ".join(cmd) + "\n")
        out.flush()
        return subprocess.run(cmd, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT,
                              env={**os.environ, "PYTHONIOENCODING": "utf-8"}).returncode


def workdir_of(sw, label, smoke):
    return sw["_root"] / label / ("smoke" if smoke else "")


def finished(sw, run, smoke):
    state = workdir_of(sw, run["label"], smoke) / "state.json"
    return state.exists() and DONE_PARTS[part_of(sw, run)] in read_json(state).get("done", [])


def run(sweep_path, smoke=False, runner=default_runner):
    sw = load(sweep_path)
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
    try:
        for i, r in enumerate(sw["runs"]):
            label = r["label"]
            cfg = run_config(sw, r, first=i == 0)
            folder = root / label
            folder.mkdir(parents=True, exist_ok=True)
            cpath = folder / "config.json"
            if cpath.exists() and not same_model(read_json(cpath), cfg):
                status[label] = {"status": "failed", "why": "이미 돈 모델의 설정이 바뀜 (base·train·set). 새 label 로 추가하세요",
                                 "at": time.strftime("%Y-%m-%d %H:%M")}
                write_json(status_path, status)
                log(f"{label}: 설정이 바뀌어 건너뜁니다 ({cpath})")
                continue
            write_json(cpath, cfg)
            if finished(sw, r, smoke) and status.get(label, {}).get("status") == "done":
                log(f"{label}: 끝남 (건너뜀)")
                continue
            log(f"=== {label} ({i + 1}/{len(sw['runs'])}) → {folder / 'sweep.log'}")
            status[label] = {"status": "running", "started": time.strftime("%Y-%m-%d %H:%M"), "pid": os.getpid()}
            write_json(status_path, status)
            started = time.monotonic()
            code = runner(cpath, folder / "sweep.log", part_of(sw, r), smoke)
            hours = round((time.monotonic() - started) / 3600, 2)
            ok = code == 0 and finished(sw, r, smoke)
            status[label] = {"status": "done" if ok else "failed", "hours": hours, "at": time.strftime("%Y-%m-%d %H:%M"),
                             **({} if ok else {"why": f"종료 코드 {code}, 로그 {folder / 'sweep.log'}"})}
            write_json(status_path, status)
            log(f"{label}: {'끝' if ok else '실패 — 다음 모델로'} ({hours} h)")
            compare(sw, smoke)
        compare(sw, smoke)
        first = sw["runs"][0]["label"]
        if sw.get("_start_mismatch") and (root / first / "data" / "DONE.json").exists():
            # start_from 의 평가 문항이 이 묶음과 다르다: 첫 모델에서 출발 모델을 평가한다
            log(f"start_from 의 출발 모델 평가를 쓸 수 없어 {first} 에서 출발 모델을 평가합니다")
            spath = root / first / "config.start.json"
            write_json(spath, {**read_json(root / first / "config.json"), "eval": {**read_json(root / first / "config.json")["eval"],
                                                                                 "skip_start": False}})
            runner(spath, root / first / "sweep.log", part_of(sw, sw["runs"][0]), smoke, only="eval_base")
            compare(sw, smoke)
    finally:
        lock.unlink(missing_ok=True)


# -- 비교표 ----------------------------------------------------------------------------------
def _images(workdir, data):
    """같은 그림으로 평가했는지: 문항별 원본 그림 + 그림 줄이기 설정 (섞은 폴더마다 경로는 달라도)."""
    done = read_json(data / "DONE.json")
    tasks = {r["id"]: r.get("source_images", r["images"]) for r in read_jsonl(data / "benchmark_tasks.jsonl")}
    return [done.get(k) for k in ("image_max_size", "pixels_per_token_side", "max_image_tokens_per_sample")], tasks


def compare(sw, smoke=False):
    """끝난 모델들의 점수를 한 표로: <root>/compare.{csv,md,html}. 출발 모델은 첫 모델의 평가."""
    from .report import _build_reports

    root, reports, notes, ref = sw["_root"], [], [], None
    sw["_start_mismatch"] = False
    own = workdir_of(sw, sw["runs"][0]["label"], smoke)
    start = None
    if (own / "reports" / "start.json").exists():   # 이 묶음에서 평가한 출발 모델이 우선
        start = (own / "reports" / "start.json", own, root / sw["runs"][0]["label"] / "data", "출발 모델")
    elif "_start_from" in sw:
        sf = sw["_start_from"]
        start = (sf / "reports" / "start.json", sf, Path(read_json(sf / "config.json")["data"]["output_dir"]),
                 f"출발 모델 ({sf.parent.name}/{sf.name})")
    for i, r in enumerate(sw["runs"]):
        label = r["label"]
        wd = workdir_of(sw, label, smoke)
        rep = wd / "reports"
        picks = [(rep / "sft.json", label)]
        if part_of(sw, r) != "sft":
            grpo = sorted(rep.glob("grpo-*.json"), key=lambda p: p.stat().st_mtime)
            picks += [(grpo[-1], f"{label} GRPO")] if grpo else []
        picks = [(p, name) for p, name in picks if p.exists()]
        if not picks:
            continue
        try:
            sig = _images(wd, root / label / "data")
        except (OSError, KeyError, ValueError) as exc:
            notes.append(f"{label}: 비교 제외 (평가 문항을 읽지 못함: {exc})")
            continue
        if ref is None:
            ref = sig
        elif sig != ref:
            notes.append(f"{label}: 비교 제외 (평가 문항 또는 그림 설정이 첫 모델과 다름)")
            continue
        for p, name in picks:
            reports.append({**read_json(p), "label": name})
    if start and ref is not None:
        try:
            ok = _images(start[1], start[2]) == ref and read_json(start[0])["items_sha256"] == reports[0]["items_sha256"]
        except (OSError, KeyError, ValueError):
            ok = False
        if ok:
            reports.insert(0, {**read_json(start[0]), "label": start[3]})
        else:
            sw["_start_mismatch"] = "_start_from" in sw and start[1] != own
            notes.append(f"출발 모델 평가({start[0]})는 평가 문항·그림 설정이 달라 표에서 뺍니다")
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
        _header(sw, root / "compare.md", root / "compare.html", notes)
        log(f"비교표 → {root / 'compare.html'} ({', '.join(result['models'])})")
    return result


def _header(sw, md, page, notes):
    """비교표(.md·.html) 맨 위에 실험 이름·설명·모델별 설명과 학습 데이터."""
    def train(r):
        return "<br>".join(html.escape(e if isinstance(e, str) else e["path"] + (f" (count {e['count']})" if e.get("count") is not None else ""))
                           for e in r["train"])
    head = [f"# {sw['name']}", "", sw["about"], ""]
    if sw.get("record"):
        head += [f"기록: {sw['record']}", ""]
    head += ["| 모델 | 설명 | 학습 데이터 |", "|---|---|---|"]
    head += [f"| {r['label']} | {r['about']} | {train(r)} |" for r in sw["runs"]]
    head += ["", *[f"- {n}" for n in notes], ""] if notes else [""]
    md.write_text("\n".join(head) + "\n" + md.read_text(encoding="utf-8"), encoding="utf-8")
    e = html.escape
    block = (f"<h1>{e(sw['name'])}</h1><p>{e(sw['about'])}</p>" + (f"<p>기록: {e(sw['record'])}</p>" if sw.get("record") else "")
             + "<table><tr><th>모델</th><th>설명</th><th>학습 데이터</th></tr>"
             + "".join(f"<tr><td>{e(r['label'])}</td><td>{e(r['about'])}</td><td>{train(r)}</td></tr>" for r in sw["runs"])
             + "</table>" + "".join(f"<p>{e(n)}</p>" for n in notes))
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
        print(f"  {label:20s} {st:10s} {r['about']}\n  {'':20s} 끝난 단계: {', '.join(done) or '-'}" + (f"  ({s['why']})" if s.get("why") else ""))
    if (root / "compare.html").exists():
        print(f"비교표: {root / 'compare.md'} · {root / 'compare.html'}")


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
