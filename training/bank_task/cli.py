"""python -m bank_task {prepare,score,mine,report}  (run_bank_pipeline.py calls these)."""
import argparse
from pathlib import Path

from bank_ocr.data import dumps, read_json, read_jsonl, write_json, write_jsonl
from bank_ocr.inference import index_predictions
from bank_ocr.settings import load_settings


def resolve_data(cfg: dict, base: Path) -> dict:
    """Paths in the pipeline config's data section, relative to the config file."""
    def res(p):
        return str((base / p).resolve()) if p and not Path(p).is_absolute() else p
    d = dict(cfg["data"])
    for key in ("docgen_root", "benchmark", "output_dir"):
        d[key] = res(d.get(key))
    d["train"] = [res(p) for p in d["train"]]
    if d.get("replay"):
        d["replay"] = {**d["replay"], "path": res(d["replay"]["path"])}
    return d


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    pr = sub.add_parser("prepare", help="docgen output -> prepared folder (data section of the pipeline config)")
    pr.add_argument("--config", required=True)
    s = sub.add_parser("score", help="Score predictions on the docgen benchmark")
    s.add_argument("--items", required=True, help="benchmark_items.jsonl of the prepared folder")
    s.add_argument("--tasks", required=True, help="benchmark tasks that were predicted (all, or a smoke subset)")
    s.add_argument("--predictions", required=True)
    s.add_argument("--label", required=True)
    s.add_argument("--role", default="other", choices=["start", "sft", "grpo", "other"])
    s.add_argument("--model", help="Model path, recorded in the report")
    s.add_argument("--out", required=True)
    m = sub.add_parser("mine", help="Pick GRPO rows, half of them where the SFT model scores low")
    m.add_argument("--tasks", required=True)
    m.add_argument("--predictions", required=True)
    m.add_argument("--out", required=True)
    m.add_argument("--count", type=int, required=True)
    m.add_argument("--seed", type=int, default=42)
    m.add_argument("--hard-fraction", type=float, default=0.5)
    m.add_argument("--hard-threshold", type=float, default=0.9)
    r = sub.add_parser("report", help="Comparison table from score outputs")
    r.add_argument("--reports", nargs="+", required=True)
    r.add_argument("--out", required=True, help=".csv; .md and .html next to it")
    r.add_argument("--ocr-reports", nargs="*", default=[], help="OCR-benchmark evaluate outputs of the same models")
    r.add_argument("--ocr-labels", nargs="*", default=[])
    r.add_argument("--ocr-out", help=".csv for the OCR retention table")
    a = p.parse_args()
    if a.command == "prepare":
        import os

        from .prepare import prepare
        path = Path(a.config).resolve()
        cfg = load_settings(path)
        data = resolve_data(cfg, path.parent)
        if data.get("docgen_root"):
            os.environ["DOCGEN_ROOT"] = data["docgen_root"]
        result = prepare(data, cfg.get("model"))
    elif a.command == "score":
        from .score import score
        ids = {row["id"] for row in read_jsonl(a.tasks)}
        items = [it for it in read_jsonl(a.items) if it["id"] in ids]
        preds = index_predictions(a.predictions)
        meta = Path(a.predictions).with_suffix(Path(a.predictions).suffix + ".meta.json")
        res = score(items, preds)
        result = {"label": a.label, "role": a.role, "model": a.model, "predictions": a.predictions,
                  "inference": read_json(meta) if meta.exists() else None, **res}
        write_json(a.out, result)
        result = {"label": a.label, "out": a.out,
                  **{t: round(v["metrics"].get(v["main"]) or 0, 4) for t, v in res["tasks"].items()}}
    elif a.command == "mine":
        from .score import mine
        rows, info = mine(read_jsonl(a.tasks), index_predictions(a.predictions), a.count, a.seed,
                          a.hard_fraction, a.hard_threshold)
        write_jsonl(a.out, rows)
        result = info
    else:
        from .report import build
        result = build(a.reports, a.out)
        if a.ocr_reports:
            from benchmark_report import build_report
            result["ocr"] = build_report(a.ocr_reports, a.ocr_out, a.ocr_labels or None)
    print(dumps(result) if not isinstance(result, str) else result)


if __name__ == "__main__":
    main()
