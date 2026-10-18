"""서류 묶음 만들기: 고객 한 명의 여러 쪽 대상 서류 2~4건 + 한 쪽짜리 다른 서류 1~3건을 섞어 한 묶음으로.

docgen 의 렌더러를 그대로 쓰고, 연구용으로 세 가지만 조절한다.
  heavy            대상 서류를 '내용이 많은 경우'(목록이 길어 여러 쪽)로 만들 확률 (DOCGEN_HEAVY)
  no_repeat_header 이어지는 쪽에 표 머리글을 다시 찍지 않는 서식으로 만들 확률 (앞 쪽 정보가 있어야 읽히는 쪽)
  augment          스캔·촬영·팩스 증강을 적용할 확률 (서류 단위, 모든 쪽에 같은 효과)

출력:
  <out>/images/<서류ID>_<seed>[_pN].png (증강이면 _aug.jpg)
  <out>/labels/<서류ID>_<seed>.json      docgen 정답 + 연구용 정보 (heavy, no_repeat_header, augment)
  <out>/bundles.jsonl                     묶음마다 {id, split, seed, docs, pages: [{image, doc, page}]}
"""
from __future__ import annotations

import json
import os
import random
import sys
from pathlib import Path

TARGETS = ("real_estate_registry", "resident_registration_copy", "bank_statement",
           "commercial_invoice", "packing_list", "financial_statements")
DISTRACTORS = ("resident_id_card", "employment_certificate", "income_certificate", "bankbook_copy",
               "business_registration_certificate", "health_insurance_qualification")
# 평가 세트(1,500,000~)와 학습 세트(500,000~)의 고객이 겹치지 않게. docgen 기본 생성(0~)·벤치마크(1,000,000~)와도 다르다.
SEED_BASE = {"train": 500_000, "test": 1_500_000}


def _render_doc(renderer, spec, profile, seed, out: Path, rng: random.Random, opts: dict) -> dict:
    from docgen.cli import _aug_fields
    from docgen.render import render
    from docgen.schema import build_fields

    target = spec.id in opts["targets"]
    heavy = target and rng.random() < opts["heavy"]
    if heavy:
        os.environ["DOCGEN_HEAVY"] = "1"
    else:
        os.environ.pop("DOCGEN_HEAVY", None)
    try:
        html, raw, _ = render(spec, profile, seed)
    finally:
        os.environ.pop("DOCGEN_HEAVY", None)
    no_head = target and rng.random() < opts["no_repeat_header"]
    if no_head:
        html = html.replace("<head>", "<head><script>window.__noRepeatHeader = true;</script>", 1)
    sid = f"{spec.id}_{seed:07d}"
    info = renderer.render(html, out / "images" / f"{sid}.png")
    fields = build_fields(raw, info)
    images = [str(Path(p).relative_to(out)) for p in info["images"]]
    pages = info["pages"]
    preset = None
    if rng.random() < opts["augment"]:
        from PIL import Image

        from docgen.augment import augment

        preset = rng.choice(["scan", "photo", "fax"])
        arng = random.Random(f"mpx-aug:{sid}")
        a_imgs, a_pages, tfs = [], [], []
        for img_path in images:
            aimg, _, tf = augment(Image.open(out / img_path), arng, preset, with_transform=True)
            ap = f"images/{Path(img_path).stem}_aug.jpg"
            aimg.save(out / ap, quality=92)
            a_imgs.append(ap)
            a_pages.append({"width": aimg.width, "height": aimg.height})
            tfs.append(tf)
        images, pages, fields = a_imgs, a_pages, _aug_fields(fields, tfs)
    label = {"id": sid, "doc_type": spec.id, "doc_name": spec.name, "group": spec.group, "seed": seed,
             "target": target, "heavy": heavy, "no_repeat_header": no_head, "augment": preset,
             "images": images, "pages": pages, "n_pages": len(images), "overflow": info["overflow"], "fields": fields}
    (out / "labels" / f"{sid}.json").write_text(json.dumps(label, ensure_ascii=False, indent=1), encoding="utf-8")
    return label


_WORKER: dict = {}


def _bundle_worker(job):
    """한 프로세스가 렌더러 하나를 계속 쓴다."""
    from docgen.entities import make_profile
    from docgen.image import ImageRenderer
    from docgen.registry import load_all

    seed, split, out, targets, distractors, n_targets, n_distractors, opts, scale = job
    if "renderer" not in _WORKER:
        _WORKER["renderer"] = ImageRenderer(scale=scale).__enter__()
        _WORKER["reg"] = load_all()
    reg = _WORKER["reg"]
    rng = random.Random(f"mpx:{seed}")
    chosen = rng.sample(list(targets), min(len(targets), rng.randint(*n_targets)))
    chosen += rng.sample(list(distractors), min(len(distractors), rng.randint(*n_distractors)))
    rng.shuffle(chosen)
    profile = make_profile(seed)
    labels = [_render_doc(_WORKER["renderer"], reg[t], profile, seed, Path(out), rng, opts) for t in chosen]
    pages = [{"image": img, "doc": lb["id"], "page": k} for lb in labels for k, img in enumerate(lb["images"])]
    return {"id": f"bundle_{seed:07d}", "split": split, "seed": seed, "docs": [lb["id"] for lb in labels], "pages": pages}


def generate(out, n: int, split: str = "test", targets=TARGETS, distractors=DISTRACTORS, n_targets=(2, 4),
             n_distractors=(1, 3), heavy: float = 0.7, no_repeat_header: float = 0.3, augment: float = 0.3,
             scale: float = 2.0, start: int = 0, workers: int = 1) -> Path:
    from docgen.registry import load_all

    out = Path(out)
    (out / "images").mkdir(parents=True, exist_ok=True)
    (out / "labels").mkdir(parents=True, exist_ok=True)
    reg = load_all()
    unknown = [t for t in (*targets, *distractors) if t not in reg]
    if unknown:
        sys.exit(f"알 수 없는 서류: {unknown}")
    opts = {"targets": set(targets), "heavy": heavy, "no_repeat_header": no_repeat_header, "augment": augment}
    bundles_path = out / "bundles.jsonl"
    done = set()
    if bundles_path.exists():
        done = {json.loads(ln)["seed"] for ln in bundles_path.open(encoding="utf-8") if ln.strip()}
    jobs = [(SEED_BASE[split] + i, split, str(out), tuple(targets), tuple(distractors), n_targets, n_distractors,
             opts, scale) for i in range(start, start + n) if SEED_BASE[split] + i not in done]
    with bundles_path.open("a", encoding="utf-8") as bf:
        if workers > 1:
            import multiprocessing as mp

            with mp.get_context("spawn").Pool(workers) as pool:
                results = pool.imap(_bundle_worker, jobs)
                for k, bundle in enumerate(results, 1):
                    bf.write(json.dumps(bundle, ensure_ascii=False) + "\n")
                    bf.flush()
                    print(f"\r묶음 {k}/{len(jobs)}", end="", file=sys.stderr)
        else:
            for k, job in enumerate(jobs, 1):
                bf.write(json.dumps(_bundle_worker(job), ensure_ascii=False) + "\n")
                bf.flush()
                print(f"\r묶음 {k}/{len(jobs)}", end="", file=sys.stderr)
            if "renderer" in _WORKER:
                _WORKER.pop("renderer").__exit__(None, None, None)
    print(file=sys.stderr)
    return bundles_path


def load(data_dir) -> tuple[list[dict], dict[str, dict]]:
    """(묶음 목록, 서류ID → 정답 label)."""
    from .common import read_jsonl

    data_dir = Path(data_dir)
    bundles = read_jsonl(data_dir / "bundles.jsonl")
    labels = {}
    for b in bundles:
        for sid in b.get("docs", []):  # 실제 서류 묶음은 정답이 없다 (docs 없음)
            if sid not in labels:
                labels[sid] = json.loads((data_dir / "labels" / f"{sid}.json").read_text(encoding="utf-8"))
    return bundles, labels


def stats(data_dir) -> dict:
    """묶음 쪽 수, 서류별 쪽 수·목록 행 수 분포."""
    from .pages import page_views

    bundles, labels = load(data_dir)
    by_type: dict[str, dict] = {}
    for lb in labels.values():
        t = by_type.setdefault(lb["doc_type"], {"docs": 0, "pages": [], "rows": []})
        t["docs"] += 1
        t["pages"].append(lb["n_pages"])
        t["rows"].append(sum(len(r) for v in page_views(lb) for r in v["lists"].values()))
    summary = {"bundles": len(bundles), "pages_per_bundle": [len(b["pages"]) for b in bundles]}
    for t, v in sorted(by_type.items()):
        summary[t] = {"docs": v["docs"], "pages_max": max(v["pages"]), "pages_mean": sum(v["pages"]) / len(v["pages"]),
                      "rows_max": max(v["rows"]), "rows_mean": sum(v["rows"]) / len(v["rows"])}
    summary["pages_per_bundle"] = {"min": min(summary["pages_per_bundle"]), "max": max(summary["pages_per_bundle"]),
                                   "mean": sum(summary["pages_per_bundle"]) / len(bundles)}
    return summary
