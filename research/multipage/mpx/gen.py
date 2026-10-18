"""1단계 — 서류 묶음 만들기 (docgen 렌더러를 그대로 쓴다).

묶음 구성 두 가지 (--compose):
  scenario (기본)  벤치마크(docgen.bench)의 업무 시나리오 묶음을 그대로 쓴다. 고객 한 명이 한 업무를 위해 낸 서류 전부
                   (예: 주택담보대출 12종). 고객 프로필(bundle_profile)과 촬영 조건 비율(원본 50%, 스캔·촬영·팩스 50%,
                   pick_condition)도 벤치마크와 같다. 대상 서류가 든 시나리오만 쓰고, 시나리오에 없는 대상 서류
                   (거래내역서, 패킹리스트)는 SCENARIO_ADDONS 로 덧붙인다.
  random           대상 서류 2~4건 + 한 쪽짜리 다른 서류 1~3건을 무작위로 섞는다 (대상 서류 비중이 높아 학습용으로 좋다).

연구용으로 조절하는 것:
  heavy            대상 서류를 '내용이 많은 경우'(목록이 길어 여러 쪽)로 만들 확률 (docgen 의 DOCGEN_HEAVY)
  no_repeat_header 이어지는 쪽에 표 머리글을 다시 찍지 않을 확률 (앞 쪽 정보가 있어야 읽히는 쪽이 생긴다)
  augment          random 구성에서 스캔·촬영·팩스 증강 확률 (scenario 구성은 벤치마크 조건을 따른다)

출력 (<out>/):
  images/<서류ID>_<seed>[_pN].png  (증강이면 .jpg)
  labels/<서류ID>_<seed>.json      docgen 정답(fields: 키·값·타입·쪽·박스) + heavy, no_repeat_header, augment
  bundles.jsonl                     묶음 한 줄: {id, split, seed, scenario, docs: [서류ID], pages: [{image, doc, page}]}
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
# 대상 서류가 들어 있는 벤치마크 시나리오와, 시나리오에 없는 대상 서류를 덧붙이는 규칙 (실무에서 함께 내는 서류)
SCENARIO_ADDONS = {"mortgage": ["bank_statement"], "jeonse_loan": ["bank_statement"],
                   "corporate_credit": ["bank_statement"], "fx_remittance": ["packing_list"]}
ADDON_PROB = 0.8
# 학습(500,000~)과 평가(1,500,000~) 고객이 겹치지 않게. docgen 기본 생성(0~)·벤치마크(1,000,000~, 10,000,000~)와도 다르다.
SEED_BASE = {"train": 500_000, "test": 1_500_000}

_WORKER: dict = {}


def _render_doc(renderer, spec, profile, seed, out: Path, rng: random.Random, opts: dict, preset: str | None) -> dict:
    """서류 한 건 렌더링 → 이미지·정답 저장. preset 이 있으면 모든 쪽에 같은 증강."""
    from docgen.cli import _aug_fields
    from docgen.render import render
    from docgen.schema import build_fields

    target = spec.id in opts["targets"]
    heavy = target and rng.random() < opts["heavy"]
    if heavy:
        os.environ["DOCGEN_HEAVY"] = "1"
    try:
        html, raw, _ = render(spec, profile, seed)
    finally:
        os.environ.pop("DOCGEN_HEAVY", None)
    no_head = target and rng.random() < opts["no_repeat_header"]
    if no_head:  # docgen/paginate.js 가 읽는 연구용 스위치
        html = html.replace("<head>", "<head><script>window.__noRepeatHeader = true;</script>", 1)
    sid = f"{spec.id}_{seed:07d}"
    info = renderer.render(html, out / "images" / f"{sid}.png")
    fields = build_fields(raw, info)
    images = [str(Path(p).relative_to(out)) for p in info["images"]]
    pages = info["pages"]
    if preset:
        from PIL import Image

        from docgen.augment import augment

        arng = random.Random(f"mpx-aug:{sid}")
        a_imgs, a_pages, tfs = [], [], []
        for img_path in images:
            aimg, _, tf = augment(Image.open(out / img_path), arng, preset, with_transform=True)
            ap = f"images/{Path(img_path).stem}.jpg"
            aimg.save(out / ap, quality=92)
            (out / img_path).unlink()
            a_imgs.append(ap)
            a_pages.append({"width": aimg.width, "height": aimg.height})
            tfs.append(tf)
        images, pages, fields = a_imgs, a_pages, _aug_fields(fields, tfs)
    label = {"id": sid, "doc_type": spec.id, "doc_name": spec.name, "group": spec.group, "seed": seed,
             "target": target, "heavy": heavy, "no_repeat_header": no_head, "augment": preset,
             "images": images, "pages": pages, "n_pages": len(images), "overflow": info["overflow"], "fields": fields}
    (out / "labels" / f"{sid}.json").write_text(json.dumps(label, ensure_ascii=False, indent=1), encoding="utf-8")
    return label


def _compose(seed: int, i: int, compose: str, targets, distractors, n_targets, n_distractors, rng, augment: float):
    """(묶음 ID, 시나리오, 업무명, 프로필, [(서류ID, 증강 preset)])"""
    from docgen.entities import make_profile

    if compose == "scenario":
        from docgen.bench.build import Builder, pick_condition
        from docgen.registry import SCENARIOS

        names = [s for s in SCENARIO_ADDONS if any(d in targets for d in SCENARIOS[s][1] + SCENARIO_ADDONS[s])]
        sc = names[i % len(names)]
        task_name, ids = SCENARIOS[sc]
        ids = list(ids) + [d for d in SCENARIO_ADDONS[sc] if d in targets and rng.random() < ADDON_PROB]
        rng.shuffle(ids)  # 제출 순서는 사람마다 다르다
        bid = f"{sc}_{seed}"
        conds = [pick_condition(f"{bid}:{d}") for d in ids]  # 벤치마크와 같은 조건 비율
        return bid, sc, task_name, Builder.bundle_profile(sc, seed), [(d, None if c == "clean" else c) for d, c in zip(ids, conds)]
    chosen = rng.sample(list(targets), min(len(targets), rng.randint(*n_targets)))
    chosen += rng.sample(list(distractors), min(len(distractors), rng.randint(*n_distractors)))
    rng.shuffle(chosen)
    docs = [(d, rng.choice(["scan", "photo", "fax"]) if rng.random() < augment else None) for d in chosen]
    return f"bundle_{seed:07d}", None, None, make_profile(seed), docs


def _bundle_worker(job):
    """묶음 하나. 프로세스마다 Chromium 렌더러 하나를 계속 쓴다."""
    from docgen.image import ImageRenderer
    from docgen.registry import load_all

    seed, i, split, out, compose, targets, distractors, n_targets, n_distractors, opts, scale = job
    if "renderer" not in _WORKER:
        _WORKER["renderer"] = ImageRenderer(scale=scale).__enter__()
        _WORKER["reg"] = load_all()
    reg = _WORKER["reg"]
    rng = random.Random(f"mpx:{compose}:{seed}")
    bid, sc, task_name, profile, docs = _compose(seed, i, compose, targets, distractors, n_targets, n_distractors,
                                                 rng, opts["augment"])
    labels = [_render_doc(_WORKER["renderer"], reg[d], profile, seed, Path(out), rng, opts, preset) for d, preset in docs]
    pages = [{"image": img, "doc": lb["id"], "page": k} for lb in labels for k, img in enumerate(lb["images"])]
    return {"id": bid, "split": split, "seed": seed, "compose": compose, "scenario": sc, "task_name": task_name,
            "docs": [lb["id"] for lb in labels], "pages": pages}


def generate(out, n: int, split: str = "test", compose: str = "scenario", targets=TARGETS, distractors=DISTRACTORS,
             n_targets=(2, 4), n_distractors=(1, 3), heavy: float = 0.7, no_repeat_header: float = 0.3,
             augment: float = 0.3, scale: float = 2.0, start: int = 0, workers: int = 1) -> Path:
    """묶음 n 개를 <out>/bundles.jsonl 에 이어 쓴다 (이미 있는 seed 는 건너뜀)."""
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
    jobs = [(SEED_BASE[split] + i, i, split, str(out), compose, tuple(targets), tuple(distractors), n_targets,
             n_distractors, opts, scale) for i in range(start, start + n) if SEED_BASE[split] + i not in done]
    with bundles_path.open("a", encoding="utf-8") as bf:
        if workers > 1 and len(jobs) > 1:
            import multiprocessing as mp

            with mp.get_context("spawn").Pool(min(workers, len(jobs))) as pool:
                for k, bundle in enumerate(pool.imap(_bundle_worker, jobs), 1):
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
    """(묶음 목록, 서류ID → 정답 label). 정답 없는 실제 서류 묶음은 docs 가 없다."""
    from .common import read_jsonl

    data_dir = Path(data_dir)
    bundles = read_jsonl(data_dir / "bundles.jsonl")
    labels = {}
    for b in bundles:
        for sid in b.get("docs", []):
            if sid not in labels:
                labels[sid] = json.loads((data_dir / "labels" / f"{sid}.json").read_text(encoding="utf-8"))
    return bundles, labels


def stats(data_dir) -> dict:
    """묶음 쪽 수, 서류별 쪽 수·목록 행 수 분포."""
    from .pages import page_views

    bundles, labels = load(data_dir)
    by_type: dict[str, dict] = {}
    for lb in labels.values():
        t = by_type.setdefault(lb["doc_type"], {"docs": 0, "pages": [], "rows": [], "target": lb.get("target")})
        t["docs"] += 1
        t["pages"].append(lb["n_pages"])
        t["rows"].append(sum(len(r) for v in page_views(lb) for r in v["lists"].values()))
    sizes = [len(b["pages"]) for b in bundles]
    summary = {"bundles": len(bundles),
               "pages_per_bundle": {"min": min(sizes), "max": max(sizes), "mean": round(sum(sizes) / len(sizes), 1)},
               "scenarios": {s: sum(1 for b in bundles if b.get("scenario") == s) for s in {b.get("scenario") for b in bundles}},
               "docs": {}}
    for t, v in sorted(by_type.items(), key=lambda kv: (not kv[1]["target"], kv[0])):
        summary["docs"][t] = {"target": bool(v["target"]), "n": v["docs"], "pages_max": max(v["pages"]),
                              "pages_mean": round(sum(v["pages"]) / len(v["pages"]), 2), "rows_max": max(v["rows"]),
                              "rows_mean": round(sum(v["rows"]) / len(v["rows"]), 1)}
    return summary
