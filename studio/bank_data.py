"""⑥ 데이터셋의 은행 서류 쪽: 레시피, 빌드. API 는 studio/api_bank.py, 화면은 static/js/recipes.js.

레시피 docgen/recipes/<이름>.json (docgen.bench build --recipe 가 읽는 것, docgen/bench/build.py 의 RECIPE_KEYS)
  {"name", "about", "track": "bank", "split": "test"|"train", "types": "all"|[서식ID·그룹], "per_doc",
   "fields_per_doc", "max_keys", "conditions": {"clean": .5, …}, "exclude": [서식ID], "reviewed_only": false,
   "nulls": {"blank": .3, "mask": .1}, "page_view": .5}
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from docgen.bench import build as BUILD
from docgen.registry import GROUPS, load_all

from .config import ROOT

RECIPES = ROOT / "docgen" / "recipes"
TEMPLATES = {
    # docgen/scripts/make_bank_data.sh 와 같은 양 (평가 세트·학습 데이터)
    "bank-bench": {"about": "은행 서류 평가 세트: 서류 476종 × 1건", "track": "bank", "split": "test",
                   "types": "all", "per_doc": 1},
    "bank-train": {"about": "은행 서류 학습 데이터: 서류 476종 × 5건 (평가 세트와 seed 가 겹치지 않음)",
                   "track": "bank", "split": "train", "types": "all", "per_doc": 5},
    "bank-try": {"about": "몇 분짜리 시험: 서식 몇 개", "track": "bank", "split": "test",
                 "types": ["resident_id_card", "loan_application"], "per_doc": 1},
}


def _slug(s: str) -> str:
    return re.sub(r"[^\w.-]+", "-", s).strip("-") or "recipe"


# ---------------------------------------------------------------------------
# 레시피
# ---------------------------------------------------------------------------

def list_recipes() -> list[dict]:
    out = []
    for f in sorted(RECIPES.glob("*.json")) if RECIPES.exists() else []:
        try:
            r = json.loads(f.read_text(encoding="utf-8"))
        except ValueError as e:
            out.append({"name": f.stem, "error": str(e)})
            continue
        out.append({"name": f.stem, "path": str(f.relative_to(ROOT)).replace("\\", "/"), **r})
    return out


def get_recipe(name: str) -> dict:
    f = RECIPES / f"{_slug(name)}.json"
    if not f.exists():
        raise KeyError(name)
    return json.loads(f.read_text(encoding="utf-8"))


def validate_recipe(r: dict) -> dict:
    if r.get("track") == "ocr":
        from . import ocr_data

        return ocr_data.validate(r)
    allowed = set(BUILD.RECIPE_KEYS) | {"name", "about", "track", "kind"}
    bad = set(r) - allowed
    if bad:
        raise ValueError(f"모르는 항목: {sorted(bad)}")
    if r.get("track", "bank") == "bank":
        reg = load_all()
        types = r.get("types", "all")
        if types != "all":
            lst = types if isinstance(types, list) else [t.strip() for t in str(types).split(",")]
            unknown = [t for t in lst if t not in reg and t not in GROUPS]
            if unknown:
                raise ValueError(f"모르는 서식·그룹: {unknown[:10]}")
        conds = r.get("conditions")
        if conds and abs(sum(conds.values()) - 1) > 1e-6:
            raise ValueError("촬영 조건 비율의 합은 1 이어야 합니다")
    if r.get("split", "test") not in ("test", "train"):
        raise ValueError("split 은 test / train")
    return r


def save_recipe(name: str, r: dict) -> dict:
    validate_recipe(r)
    RECIPES.mkdir(parents=True, exist_ok=True)
    f = RECIPES / f"{_slug(name)}.json"
    f.write_text(json.dumps({**r, "name": _slug(name)}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return {"name": f.stem, "path": str(f.relative_to(ROOT)).replace("\\", "/"), **r}


def delete_recipe(name: str) -> None:
    f = RECIPES / f"{_slug(name)}.json"
    if not f.exists():
        raise KeyError(name)
    f.unlink()


def options() -> dict:
    """레시피 편집 화면에 보여 줄 것: 그룹, 촬영 조건 기본값, 서식틀, 평가 세트 버전."""
    return {"groups": GROUPS,
            "conditions": dict(BUILD.CONDITIONS), "templates": {**TEMPLATES, **_ocr_templates()}, "version": BUILD.VERSION}


def _ocr_templates() -> dict:
    from .ocr_data import TEMPLATES as T

    return T


# ---------------------------------------------------------------------------
# 빌드
# ---------------------------------------------------------------------------

def start_build(jobs, registry, recipe_name: str, out_name: str, workers: int = 1) -> dict:
    from .jobs import python
    from .build_registration import register_output

    r = get_recipe(recipe_name)
    if r.get("track", "bank") != "bank":
        raise ValueError("은행 서류 레시피가 아닙니다")
    out = registry.ws / "datasets" / _slug(out_name)
    if out.exists() and any(out.iterdir()):
        raise ValueError(f"이미 있는 폴더입니다: {out}. 다른 이름을 쓰세요 (만든 데이터셋은 덮어쓰지 않습니다)")
    rpath = RECIPES / f"{_slug(recipe_name)}.json"
    cmd = [python(), "-m", "docgen.bench", "build", "--recipe", str(rpath), "--out", str(out), "--workers", str(max(1, workers))]

    spec = {"path": str(out), "name": _slug(out_name), "meta": {
        "source": "synthetic", "gt": "exact", "recipe": str(rpath.relative_to(ROOT)).replace("\\", "/"),
        "dataset_json": "dataset.json", "purpose": r.get("about", "")}}

    def done(job):
        return register_output(registry, spec)

    return jobs.start("build_bank", f"은행 서류 데이터셋 만들기: {out_name} (레시피 {recipe_name})", cmd, done,
                      {"recipe": recipe_name, "out": str(out), "dataset": spec})
