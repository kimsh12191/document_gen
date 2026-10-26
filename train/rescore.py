"""이미 낸 모델 답으로 다시 채점 (추론 없이): 채점 규칙을 고쳤을 때 (python -m train rescore).

  python -m train rescore <workdir 또는 실험 묶음 결과 폴더> ... [--data <섞은 폴더>]

- workdir: reports/*.json 마다 그 보고서가 가리키는 답 파일(predictions/*.jsonl)을 지금 채점기로 다시 채점해 같은 이름으로 쓴다.
  고치기 전 보고서는 reports/before-rescore-<시각>/ 에 옮겨 둔다. 끝나면 benchmark.{csv,md,html} 도 다시 만든다.
- 실험 묶음 결과 폴더(sweep.config.json 이 있는 곳): 모델 폴더마다 위처럼 하고 compare.{csv,md,html} 를 다시 만든다.
- 섞은 폴더(benchmark_items.jsonl 이 있는 곳)는 <workdir>/config.json 의 data.output_dir. 없으면 --data 로.
- GPU·평가 서버는 쓰지 않는다. 평가 문항은 그대로라 점수끼리 계속 비교할 수 있다.
"""
import argparse
import shutil
import time
from pathlib import Path

from docgen.bench.ocr_data import read_json, read_jsonl, write_json

from .predict import index_predictions
from .score import score


def rescore_workdir(wd, data=None):
    wd = Path(wd).resolve()
    rep = wd / "reports"
    olds = [p for p in sorted(rep.glob("*.json")) if "predictions" in read_json(p)]
    if not olds:
        print(f"{wd}: 다시 채점할 보고서가 없습니다")
        return []
    data = Path(data) if data else Path(read_json(wd / "config.json")["data"]["output_dir"])
    ids = {row["id"] for row in read_jsonl(data / "benchmark_tasks.jsonl")}
    items = [it for it in read_jsonl(data / "benchmark_items.jsonl") if it["id"] in ids]
    backup = rep / f"before-rescore-{time.strftime('%Y%m%d-%H%M%S')}"
    backup.mkdir()
    done = []
    for p in olds:
        old = read_json(p)
        preds = Path(old["predictions"])
        if not preds.is_file():
            preds = wd / "predictions" / preds.name   # 폴더를 옮겼으면 workdir 안에서
        shutil.copy2(p, backup / p.name)
        new = score(items, index_predictions(preds))
        if new["items_sha256"] != old.get("items_sha256"):
            raise SystemExit(f"{p}: 평가 문항이 그 보고서를 낼 때와 다릅니다 (섞은 폴더 {data} 확인). 고친 것 없음, 백업 {backup}")
        write_json(p, {**{k: v for k, v in old.items() if k not in new}, **new})
        main = {t: round((v["metrics"].get(v["main"]) or 0) * 100, 1) for t, v in new["tasks"].items()}
        was = {t: round((v["metrics"].get(v["main"]) or 0) * 100, 1) for t, v in old.get("tasks", {}).items()}
        changed = {t: f"{was.get(t)} → {v}" for t, v in main.items() if was.get(t) != v}
        print(f"  {p.name} ({old.get('label')}): " + (", ".join(f"{t} {c}" for t, c in changed.items()) or "바뀐 점수 없음"))
        done.append(p)
    if (rep / "benchmark.csv").exists():
        from .report import build

        order = (sorted(rep.glob("cmp-compare*.json")) + [rep / "start.json", rep / "sft.json"]
                 + sorted(rep.glob("grpo-*.json"), key=lambda q: q.stat().st_mtime))
        build([q for q in order if q.exists()], rep / "benchmark.csv")
    print(f"{wd}: {len(done)}개 다시 채점, 예전 보고서 {backup}")
    return done


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m train rescore", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("folders", nargs="+", help="workdir 또는 실험 묶음 결과 폴더")
    p.add_argument("--data", help="섞은 폴더 (workdir 하나일 때, config.json 이 없으면)")
    a = p.parse_args(argv)
    for f in map(Path, a.folders):
        if (f / "sweep.config.json").is_file():
            from . import summary, sweep

            sw = summary.load(f)
            for r in sw["runs"]:
                if (f / r["label"] / "reports").is_dir():
                    rescore_workdir(f / r["label"], f / r["label"] / "data")
            sweep.compare(sw)
        else:
            rescore_workdir(f, a.data)
