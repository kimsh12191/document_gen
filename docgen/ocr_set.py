"""합성 OCR 벤치마크·학습 데이터: 생성 서류의 쪽 전체 글자를 정답으로, 1부(bank_ocr) prepare 형식으로 만든다.

  python -m docgen.ocr_set build --recipe datasets/recipes/<이름>.json --out <폴더> [--workers 4] [--no-prepare]

출력
  <폴더>/images/<서식>_<seed>[_p<쪽>].png|jpg   쪽 이미지 (촬영 조건 증강 포함)
  <폴더>/ocr_json/<같은 이름>.json               정답: 사내 OCR 응답 형식 (docgen/ocr_export.py)
  <폴더>/manifest.jsonl                         1부 scan 결과와 같은 줄 {document_id, page_id, image, split, ocr_json}
  <폴더>/config.json                            1부 prepare 설정 (training/config.example.json + 레시피의 prepare)
  <폴더>/prepared/                              1부 prepare 결과 (studio 가 데이터셋으로 등록하는 폴더)
  <폴더>/ocr_set.json                           레시피, 생성기 커밋, 수, 서식 해시

레시피 (track: "ocr")
  {"track": "ocr", "name", "about", "split": "benchmark" | "train",
   "types": "all" | [서식ID·그룹], "per_doc": 서식당 고객 수, "exclude": [...], "reviewed_only": false,
   "conditions": {"clean": .5, "scan": .2, "photo": .15, "fax": .15},
   "unit": "word" | "line",     정답 한 항목의 단위 (사내 OCR 에 맞춘다: DESIGN.md 12절)
   "heavy": "default"|"on"|"off", "special": "default"|"on"|"off",
   "merge_manifests": [다른 1부 manifest 경로 (실서류 등)],
   "prepare": {1부 설정 덮어쓰기: tasks_per_view, filters, benchmark_fraction …}}
- split="benchmark": 모든 쪽이 평가용 (1부 benchmark_only). split="train": 1부가 benchmark_fraction 만큼 평가로 떼어 둔다.
- seed 범위는 docgen generate(0~)·docgen.bench(1,000,000~ / 10,000,000~)와 겹치지 않는다: 평가 3,000,000~, 학습 30,000,000~.
- 견본 표시·도장 안 글자·정정으로 그은 글자는 신뢰도 0.3 으로 적고, 1부 필터(기본: 평가 0.5, 학습 0.95)가 그 자리를 뺀다.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEEDS = {"benchmark": 3_000_000, "train": 30_000_000}
DEFAULT_CONDITIONS = {"clean": 0.5, "scan": 0.2, "photo": 0.15, "fax": 0.15}
# 합성 정답에 맞춘 1부 설정: 애매한 글자(신뢰도 0.3)를 평가에서도 거른다
PREPARE_DEFAULTS = {"filters": {"train": {"min_confidence": 0.95, "min_length": 1, "max_length": 100},
                                "benchmark": {"min_confidence": 0.5, "min_length": 1, "max_length": 100}}}
_ENV = {"heavy": ("DOCGEN_HEAVY", {"on": "1", "off": "0"}), "special": ("DOCGEN_SPECIAL", {"on": "all", "off": "none"})}


def pick(key: str, conditions: dict) -> str:
    x = random.Random(f"ocrset:cond:{key}").random()
    acc = 0.0
    for name, p in conditions.items():
        acc += p
        if x < acc:
            return name
    return next(iter(conditions))


def select_ids(recipe: dict) -> list[str]:
    from .registry import GROUPS, load_all

    reg = load_all()
    types = recipe.get("types", "all")
    if types == "all":
        ids = list(reg)
    else:
        lst = types if isinstance(types, list) else [t.strip() for t in str(types).split(",") if t.strip()]
        ids = []
        for t in lst:
            ids += [s.id for s in reg.values() if s.group == t] if t in GROUPS else [t]
    bad = [i for i in ids if i not in reg]
    if bad:
        raise SystemExit(f"알 수 없는 서식: {bad}")
    if any(reg[i].group == "imported" for i in ids):   # 가져온 서식은 검수한 것만 "all"·그룹으로 (ID 를 직접 적으면 허용)
        named = set(lst) if types != "all" else set()
        ok = _reviewed()
        ids = [i for i in ids if reg[i].group != "imported" or i in ok or i in named]
    ex = set(recipe.get("exclude") or [])
    ids = [i for i in ids if i not in ex]
    if recipe.get("reviewed_only"):
        ok = _reviewed()
        ids = [i for i in ids if i in ok]
    return ids


def _reviewed() -> set[str]:
    p = ROOT / "docgen" / "catalog.json"
    return {k for k, v in json.loads(p.read_text(encoding="utf-8")).items() if v.get("reviewed")} if p.exists() else set()


_R = None


def _init(scale: float):
    from multiprocessing.util import Finalize

    from .image import ImageRenderer

    global _R
    _R = ImageRenderer(scale=scale).__enter__()
    Finalize(_R, lambda: _R.__exit__(None, None, None), exitpriority=10)


def _one(job: tuple) -> list[dict]:
    """서류 한 건: 렌더링 → (증강) → 쪽마다 이미지 + 정답 OCR JSON. manifest 줄들을 돌려준다."""
    doc_id, seed, cond, out, unit, heavy, special, split, scale = job
    from PIL import Image

    from .augment import augment
    from .entities import make_profile
    from .ocr_export import background_words, page_document, page_items, transform_texts
    from .registry import load_all
    from .render import render

    spec = load_all()[doc_id]
    saved = {k: os.environ.get(v) for k, (v, _) in _ENV.items()}
    try:
        for name, mode in (("heavy", heavy), ("special", special)):
            var, values = _ENV[name]
            if mode in values:
                os.environ[var] = values[mode]
            else:
                os.environ.pop(var, None)
        html, raw, _ = render(spec, make_profile(seed), seed)
    finally:
        for k, (v, _) in _ENV.items():
            if saved[k] is None:
                os.environ.pop(v, None)
            else:
                os.environ[v] = saved[k]
    out = Path(out)
    stem = f"{doc_id}_{seed}"
    info = _R.render(html, out / "images" / f"{stem}.png", texts=True)
    paths = [Path(p) for p in info["images"]]
    texts = info["texts"]
    bg = background_words(doc_id) if spec.group in ("hana", "imported") else {}
    zoom = scale * 96 / 72   # pt → 이미지 픽셀
    if cond != "clean":
        arng = random.Random(f"ocrset:aug:{stem}")
        new, tfs = [], []
        for p in paths:
            img, _, tf = augment(Image.open(p), arng, cond, with_transform=True)
            q = p.with_suffix(".jpg")
            img.save(q, quality=92)
            p.unlink()
            new.append(q)
            tfs.append(tf)
        bg_px = {pg: [{**w, "bbox": [v * zoom for v in w["bbox"]]} for w in ws] for pg, ws in bg.items()}
        texts = transform_texts(texts, tfs)
        bg_px = {pg: [{**w, "bbox": tfs[pg].bbox(w["bbox"])} for w in ws] for pg, ws in bg_px.items() if pg < len(tfs)}
        paths, zoom_bg = new, 1.0
    else:
        bg_px, zoom_bg = bg, zoom
    rows = []
    for k, p in enumerate(paths):
        items = page_items([t for t in texts if t["page"] == k], bg_px.get(k, []), zoom_bg, unit)
        oj = out / "ocr_json" / (p.stem + ".json")
        oj.write_text(json.dumps(page_document(items, p.name), ensure_ascii=False), encoding="utf-8")
        rows.append({"document_id": stem, "page_id": f"{stem}/p{k + 1}", "image": str(p.resolve()), "split": split,
                     "ocr_json": str(oj.resolve()), "doc_type": doc_id, "condition": cond})
    return rows


def build(args) -> None:
    recipe = json.loads(Path(args.recipe).read_text(encoding="utf-8"))
    if recipe.get("track") != "ocr":
        raise SystemExit("OCR 레시피(track: ocr)가 아닙니다")
    out = Path(args.out)
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"{out} 가 비어 있지 않습니다 (만든 데이터셋은 덮어쓰지 않습니다)")
    split = recipe.get("split", "benchmark")
    if split not in SEEDS:
        raise SystemExit("split 은 benchmark / train")
    conditions = recipe.get("conditions") or DEFAULT_CONDITIONS
    if abs(sum(conditions.values()) - 1) > 1e-6:
        raise SystemExit("conditions 비율의 합은 1")
    unit = recipe.get("unit", "word")
    ids = select_ids(recipe)
    per = int(recipe.get("per_doc", 1))
    for d in ("images", "ocr_json"):
        (out / d).mkdir(parents=True, exist_ok=True)
    start = SEEDS[split] + int(recipe.get("start", 0))
    jobs = [(doc_id, start + k, pick(f"{doc_id}:{start + k}", conditions), str(out), unit, recipe.get("heavy", "default"),
             recipe.get("special", "default"), split, args.scale) for k in range(per) for doc_id in ids]
    t0 = time.time()
    rows: list[dict] = []
    if args.workers > 1:
        import multiprocessing as mp

        with mp.get_context("spawn").Pool(args.workers, _init, (args.scale,)) as pool:
            for i, r in enumerate(pool.imap(_one, jobs)):
                rows += r
                print(f"\r서류 {i + 1}/{len(jobs)}", end="", file=sys.stderr)
    else:
        _init(args.scale)
        for i, j in enumerate(jobs):
            rows += _one(j)
            print(f"\r서류 {i + 1}/{len(jobs)}", end="", file=sys.stderr)
    print(file=sys.stderr)
    for m in recipe.get("merge_manifests") or []:   # 다른 1부 manifest (실서류 등) 를 합친다 (1부 merge 와 같은 규칙)
        mp_ = Path(m)
        for s in mp_.read_text(encoding="utf-8-sig").splitlines():
            if s.strip():
                row = json.loads(s)
                for key in ("image", "ocr_json"):
                    if key in row:
                        row[key] = str((mp_.resolve().parent / row[key]).resolve())
                rows.append(row)
    with open(out / "manifest.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps({k: r[k] for k in ("document_id", "page_id", "image", "split", "ocr_json") if k in r},
                               ensure_ascii=False) + "\n")
    cfg = json.loads((ROOT / "training" / "config.example.json").read_text(encoding="utf-8"))
    cfg.update({"manifest": str((out / "manifest.jsonl").resolve()), "output_dir": str((out / "prepared").resolve()),
                "cache_dir": str((out / "ocr_cache").resolve()), "ocr_revision": f"docgen-synthetic-{unit}-v1"})
    for k, v in PREPARE_DEFAULTS.items():
        cfg[k] = v
    for k, v in (recipe.get("prepare") or {}).items():
        cfg[k] = v
    if split == "benchmark":
        cfg["benchmark_only"] = True
    if not recipe.get("merge_manifests"):   # 정답이 렌더링한 글자 그대로 (합친 실서류는 사내 OCR 이라 기본값으로 둔다)
        cfg["reference_type"] = "synthetic_exact"
    cfg["studio"] = {"source": "synthetic" if not recipe.get("merge_manifests") else "results", "gt": "exact",
                     "real_data": bool(recipe.get("merge_manifests"))}
    (out / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
    from .bench.build import _git_rev
    from .preview import source_hash

    info = {"recipe": recipe, "recipe_path": str(args.recipe), "generator_commit": _git_rev(), "created": time.strftime("%Y-%m-%d %H:%M:%S"),
            "split": split, "unit": unit, "documents": len(jobs), "pages": len(rows), "seconds": round(time.time() - t0),
            "form_hashes": {i: source_hash(i, common=False) for i in ids}}
    (out / "ocr_set.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"서류 {len(jobs)}건, 쪽 {len(rows)} → {out}")
    if not args.no_prepare:
        subprocess.run([sys.executable, "-m", "bank_ocr", "prepare", "--config", str((out / "config.json").resolve())],
                       cwd=ROOT / "training", check=True)
        print(f"1부 prepare → {out / 'prepared'}")


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="docgen.ocr_set", description="합성 OCR 데이터셋 (1부 prepare 형식)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--recipe", required=True)
    b.add_argument("--out", required=True)
    b.add_argument("--workers", type=int, default=1)
    b.add_argument("--scale", type=float, default=2.0)
    b.add_argument("--no-prepare", action="store_true", help="이미지·OCR JSON·manifest 까지만 (1부 prepare 는 따로)")
    args = ap.parse_args(argv)
    build(args)


if __name__ == "__main__":
    main()
