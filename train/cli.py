"""python -m train.cli {ocr,mix,predict,score,mine,report} — 학습 실행(pipeline.py)이 단계마다 부른다. 따로 돌려도 된다."""
import argparse
from pathlib import Path

from docgen.bench.ocr_data import digest, dumps, read_json, read_jsonl, write_json, write_jsonl

from .settings import load_settings


def resolve_data(cfg: dict, base: Path) -> dict:
    """파이프라인 설정 data 칸의 경로 (설정 파일 기준 상대 경로)."""
    def res(p):
        return str((base / p).resolve()) if p and not Path(p).is_absolute() else p

    def entries(v):
        return [({**e, "path": res(e["path"])} if isinstance(e, dict) else res(e)) for e in (v if isinstance(v, list) else [v])]
    d = dict(cfg["data"])
    d["output_dir"] = res(d.get("output_dir"))
    d["train"] = entries(d.get("train") or [])
    d["benchmark"] = entries(d.get("benchmark") or [])
    if d.get("ocr_images"):   # 그림 폴더 → ocr 단계가 준비할 폴더를 학습·평가 목록에 (ocr_images.py)
        from .ocr_images import entries as ocr_entries
        from .ocr_images import resolve

        d["ocr_images"] = resolve(d["ocr_images"], d["output_dir"], res)
        train, bench = ocr_entries(d["ocr_images"])
        d["train"] += [train] if train else []
        d["benchmark"] += [bench] if bench else []
    return d


PREDICT_DEFAULTS = {"endpoint": "http://127.0.0.1:8000/v1", "model": "docgen", "timeout": 600, "max_tokens": 4096,
                    "temperature": 0, "enable_thinking": False, "request_options": {}, "concurrency": 1}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    o = sub.add_parser("ocr", help="그림 폴더 OCR·준비 (설정의 data.ocr_images)")
    o.add_argument("--config", required=True)
    m = sub.add_parser("mix", help="데이터셋 섞기 (설정의 data 칸)")
    m.add_argument("--config", required=True)
    r = sub.add_parser("predict", help="모델 답 내기")
    r.add_argument("--config", help="답 내기 설정 JSON (train/configs/inference.json); 명령줄이 우선")
    r.add_argument("--tasks", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--endpoint", help="모델 서버 주소, 여러 개는 쉼표로")
    r.add_argument("--model")
    r.add_argument("--run-id", required=True, help="체크포인트마다 다른 값")
    r.add_argument("--with-ocr", action="store_true", help="사내 OCR 결과를 질문에 붙인다 (OCR 과제 비교용)")
    r.add_argument("--timeout", type=int)
    r.add_argument("--concurrency", type=int)
    r.add_argument("--max-tokens", type=int)
    r.add_argument("--temperature", type=float)
    r.add_argument("--enable-thinking", action=argparse.BooleanOptionalAction, default=None)
    s = sub.add_parser("score", help="평가 채점")
    s.add_argument("--items", required=True, help="섞은 폴더의 benchmark_items.jsonl")
    s.add_argument("--tasks", required=True, help="답을 낸 평가 문항 (전체 또는 리허설 일부)")
    s.add_argument("--predictions", required=True)
    s.add_argument("--label", required=True)
    s.add_argument("--role", default="other", choices=["start", "sft", "grpo", "other"])
    s.add_argument("--model", help="모델 경로 (보고서에 남김)")
    s.add_argument("--out", required=True)
    h = sub.add_parser("mine", help="GRPO 문항 고르기 (반은 SFT 모델이 낮게 받는 것)")
    h.add_argument("--tasks", required=True)
    h.add_argument("--predictions", required=True)
    h.add_argument("--out", required=True)
    h.add_argument("--count", type=int, required=True)
    h.add_argument("--seed", type=int, default=42)
    h.add_argument("--hard-fraction", type=float, default=0.5)
    h.add_argument("--hard-threshold", type=float, default=0.9)
    b = sub.add_parser("report", help="score 결과들 → 비교표")
    b.add_argument("--reports", nargs="+", required=True)
    b.add_argument("--out", required=True, help=".csv (.md·.html 은 옆에)")
    a = p.parse_args(argv)
    if a.command == "ocr":
        from .ocr_images import build

        path = Path(a.config).resolve()
        d = resolve_data(load_settings(path), path.parent)
        if not d.get("ocr_images"):
            p.error("설정에 data.ocr_images 가 없습니다")
        done = build(d["ocr_images"])
        result = {"output_dir": d["ocr_images"]["output_dir"], "pages": done.get("page_counts"), "sft_examples": done.get("sft_examples")}
    elif a.command == "mix":
        from .mix import mix

        path = Path(a.config).resolve()
        cfg = load_settings(path)
        result = mix(resolve_data(cfg, path.parent), cfg.get("model"))
    elif a.command == "predict":
        from .predict import predict

        settings = dict(PREDICT_DEFAULTS)
        if a.config:
            configured = load_settings(a.config)
            unknown = configured.keys() - settings.keys()
            if unknown:
                p.error("Unknown inference settings: " + ", ".join(sorted(unknown)))
            settings.update(configured)
        for key in settings:
            value = getattr(a, key, None)
            if value is not None:
                settings[key] = value
        if not isinstance(settings["request_options"], dict):
            p.error("request_options must be an object")
        if not isinstance(settings["timeout"], (int, float)) or settings["timeout"] <= 0:
            p.error("timeout must be positive")
        result = predict(a.tasks, a.out, run_id=a.run_id, with_ocr=a.with_ocr, **settings)
    elif a.command == "score":
        from .predict import index_predictions
        from .score import score

        ids = {row["id"] for row in read_jsonl(a.tasks)}
        items = [it for it in read_jsonl(a.items) if it["id"] in ids]
        meta = Path(a.predictions).with_suffix(Path(a.predictions).suffix + ".meta.json")
        info = read_json(meta) if meta.exists() else None
        if info and info.get("tasks_sha256") and info["tasks_sha256"] != digest(Path(a.tasks).read_bytes()):
            raise ValueError("Prediction metadata refers to a different task file")
        res = score(items, index_predictions(a.predictions))
        write_json(a.out, {"label": a.label, "role": a.role, "model": a.model, "predictions": a.predictions,
                           "inference": info, **res})
        result = {"label": a.label, "out": a.out,
                  **{t: round(v["metrics"].get(v["main"]) or 0, 4) for t, v in res["tasks"].items()}}
    elif a.command == "mine":
        from .predict import index_predictions
        from .score import mine

        rows, info = mine(read_jsonl(a.tasks), index_predictions(a.predictions), a.count, a.seed,
                          a.hard_fraction, a.hard_threshold)
        write_jsonl(a.out, rows)
        result = info
    else:
        from .report import build

        result = build(a.reports, a.out)
    print(dumps(result))


if __name__ == "__main__":
    main()
