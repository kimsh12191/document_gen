"""⑥ 데이터셋의 OCR 쪽: 합성 OCR 레시피·빌드(docgen.ocr_set → 1부 prepare), 1부 학습 설정 내보내기(run_pipeline.py).

OCR 레시피는 은행 업무 레시피와 같은 docgen/recipes/ 에 track: "ocr" 로 둔다. 형식은 docgen/ocr_set.py 머리말.
API 는 studio/api_bank.py (/api/builds, /api/training/…), 화면은 static/js/recipes.js·datasets.js(학습 탭).
"""
from __future__ import annotations

import json
from pathlib import Path

from .config import ROOT

OCR_KEYS = {"name", "about", "track", "split", "types", "per_doc", "exclude", "reviewed_only", "conditions", "unit", "heavy",
            "special", "merge_manifests", "prepare", "start"}
TEMPLATES = {
    "ocr-bench": {"about": "합성 OCR 평가 세트: 서식 476종 × 1건, 쪽 전체 글자 정답 (1부 8과제)", "track": "ocr", "split": "benchmark",
                  "types": "all", "per_doc": 1, "unit": "word"},
    "ocr-train": {"about": "합성 OCR 학습 데이터: 서식 476종 × 3건 (1부가 10% 를 평가로 떼어 둠)", "track": "ocr", "split": "train",
                  "types": "all", "per_doc": 3, "unit": "word", "prepare": {"benchmark_fraction": 0.1}},
    "ocr-try": {"about": "몇 분짜리 시험: 서식 3종 × 2건", "track": "ocr", "split": "benchmark",
                "types": ["employment_certificate", "hf169", "resident_id_card"], "per_doc": 2, "unit": "word"},
}


def validate(r: dict) -> dict:
    from docgen.registry import GROUPS, load_all

    bad = set(r) - OCR_KEYS
    if bad:
        raise ValueError(f"OCR 레시피에 모르는 항목: {sorted(bad)}")
    if r.get("split", "benchmark") not in ("benchmark", "train"):
        raise ValueError("OCR 레시피의 split 은 benchmark / train")
    if r.get("unit", "word") not in ("word", "line"):
        raise ValueError("unit 은 word / line")
    types = r.get("types", "all")
    if types != "all":
        reg = load_all()
        lst = types if isinstance(types, list) else [t.strip() for t in str(types).split(",")]
        unknown = [t for t in lst if t not in reg and t not in GROUPS]
        if unknown:
            raise ValueError(f"모르는 서식·그룹: {unknown[:10]}")
    conds = r.get("conditions")
    if conds and abs(sum(conds.values()) - 1) > 1e-6:
        raise ValueError("촬영 조건 비율의 합은 1")
    for m in r.get("merge_manifests") or []:
        if not Path(m).is_file():
            raise ValueError(f"합칠 manifest 가 없습니다: {m}")
    return r


def start_build(jobs, registry, recipes_dir: Path, recipe_name: str, out_name: str, workers: int = 1) -> dict:
    from .bank_data import _slug, get_recipe
    from .jobs import python
    from .build_registration import register_output

    r = get_recipe(recipe_name)
    validate(r)
    out = registry.ws / "datasets" / _slug(out_name)
    if out.exists() and any(out.iterdir()):
        raise ValueError(f"이미 있는 폴더입니다: {out}. 다른 이름을 쓰세요")
    rpath = recipes_dir / f"{_slug(recipe_name)}.json"
    cmd = [python(), "-m", "docgen.ocr_set", "build", "--recipe", str(rpath), "--out", str(out), "--workers", str(max(1, workers))]

    spec = {"path": str(out / "prepared"), "name": _slug(out_name), "meta": {
        "recipe": str(rpath.relative_to(ROOT)).replace("\\", "/"), "dataset_json": "../ocr_set.json", "purpose": r.get("about", "")}}

    def done(job):
        return register_output(registry, spec)

    return jobs.start("build_ocr", f"OCR 데이터셋 만들기: {out_name} (레시피 {recipe_name})", cmd, done,
                      {"recipe": recipe_name, "out": str(out), "dataset": spec})
