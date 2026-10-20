"""③ 시나리오·묶음과 ⑥ 데이터셋의 은행 업무 쪽: 레시피, 빌드, 업무 묶음 보기, 고객 일관성 검사, 학습 설정 내보내기(2부).

레시피 datasets/recipes/<이름>.json (docgen.bench build --recipe 가 읽는 것, docgen/bench/build.py 의 RECIPE_KEYS)
  {"name", "about", "track": "bank", "split": "test"|"train", "types": "all"|[서식ID·그룹], "per_doc", "scenarios": "all"|[…],
   "bundles": 4 | {"default": 4, "<시나리오>": n}, "fields_per_doc", "max_keys", "conditions": {"clean": .5, …},
   "bundle": {"missing": [.3,.5,.2], "other_customer": .3, "extra_doc": .35, "tamper": .5},
   "cases": {"<사례>": {"enabled": false} | {"tamper": .8}}, "custom_bundles": [{…}], "exclude": [서식ID], "reviewed_only": false}
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from docgen.bench import build as BUILD
from docgen.bench.cases import CASES
from docgen.bench.rules import RULES
from docgen.registry import GROUPS, SCENARIO_EXTRA, SCENARIOS, load_all, save_scenarios

from .config import ROOT

RECIPES = ROOT / "datasets" / "recipes"
TEMPLATES = {
    # scripts/make_bank_data.sh 와 같은 양 (평가 세트·학습 데이터)
    "bank-bench": {"about": "은행 업무 평가 세트: 서류 476종 × 1건 + 업무 12종 × 고객 40명", "track": "bank", "split": "test",
                   "types": "all", "per_doc": 1, "scenarios": "all", "bundles": 40},
    "bank-train": {"about": "은행 업무 학습 데이터: 서류 476종 × 5건 + 업무 12종 × 고객 200명 (평가 세트와 seed 가 겹치지 않음)",
                   "track": "bank", "split": "train", "types": "all", "per_doc": 5, "scenarios": "all", "bundles": 200},
    "bank-try": {"about": "몇 분짜리 시험: 서식 몇 개 + 업무 하나 × 고객 2명", "track": "bank", "split": "test",
                 "types": ["resident_id_card", "loan_application"], "per_doc": 1, "scenarios": ["mortgage"], "bundles": 2},
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
        scs = r.get("scenarios", "all")
        if scs != "all":
            unknown = [s for s in scs if s not in SCENARIOS]
            if unknown:
                raise ValueError(f"모르는 시나리오: {unknown}")
        conds = r.get("conditions")
        if conds and abs(sum(conds.values()) - 1) > 1e-6:
            raise ValueError("촬영 조건 비율의 합은 1 이어야 합니다")
        m = (r.get("bundle") or {}).get("missing")
        if m is not None and (len(m) != 3 or abs(sum(m) - 1) > 1e-6):
            raise ValueError("빠진 서류 0/1/2건 비율은 세 개, 합 1")
        ids = {c.id for c in CASES}
        for c in r.get("cases") or {}:
            if c not in ids:
                raise ValueError(f"모르는 대조 사례: {c}")
        for k, cb in enumerate(r.get("custom_bundles") or []):
            if cb.get("scenario") not in SCENARIOS:
                raise ValueError(f"직접 만든 묶음 {k + 1}: 시나리오를 고르세요")
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
    """레시피 편집 화면에 보여 줄 것: 그룹, 시나리오, 대조 사례, 심사 규칙, 기본 규칙값, 서식틀."""
    return {"groups": GROUPS, "scenarios": [{"id": k, "name": n, "docs": d} for k, (n, d) in SCENARIOS.items()],
            "cases": [{"id": c.id, "title": c.title, "category": c.category, "basis": c.basis} for c in CASES],
            "rules": list(RULES), "bundle_defaults": BUILD.BUNDLE_RULES,
            "conditions": dict(BUILD.CONDITIONS), "templates": {**TEMPLATES, **_ocr_templates()}, "version": BUILD.VERSION}


def _ocr_templates() -> dict:
    from .ocr_data import TEMPLATES as T

    return T


# ---------------------------------------------------------------------------
# 빌드
# ---------------------------------------------------------------------------

def start_build(jobs, registry, recipe_name: str, out_name: str, workers: int = 1) -> dict:
    from .jobs import python

    r = get_recipe(recipe_name)
    if r.get("track", "bank") != "bank":
        raise ValueError("은행 업무 레시피가 아닙니다")
    out = registry.ws / "datasets" / _slug(out_name)
    if out.exists() and any(out.iterdir()):
        raise ValueError(f"이미 있는 폴더입니다: {out}. 다른 이름을 쓰세요 (만든 데이터셋은 덮어쓰지 않습니다)")
    rpath = RECIPES / f"{_slug(recipe_name)}.json"
    cmd = [python(), "-m", "docgen.bench", "build", "--recipe", str(rpath), "--out", str(out), "--workers", str(max(1, workers))]

    def done(job):
        ds = registry.register(str(out), _slug(out_name), source="synthetic", gt="exact", made_by_studio=True,
                               recipe=str(rpath.relative_to(ROOT)).replace("\\", "/"), dataset_json="dataset.json",
                               purpose=r.get("about", ""))
        return {"dataset": ds["id"]}

    return jobs.start("build_bank", f"은행 업무 데이터셋 만들기: {out_name} (레시피 {recipe_name})", cmd, done,
                      {"recipe": recipe_name, "out": str(out)})


# ---------------------------------------------------------------------------
# 업무 묶음 보기
# ---------------------------------------------------------------------------

def bundles(ds: dict) -> list[dict]:
    f = Path(ds["path"]) / "bundles.jsonl"
    if not f.exists():
        return []
    return [json.loads(s) for s in f.read_text(encoding="utf-8").splitlines() if s.strip()]


def bundle_summary(b: dict) -> dict:
    dc = b.get("doc_check") or {}
    return {"bundle_id": b["bundle_id"], "scenario": b["scenario"], "task_name": b["task_name"], "customer": b["customer"],
            "customer_seed": b["customer_seed"], "n_docs": len([d for d in b["docs"] if not d.get("why")]),
            "n_pages": sum(len(d["images"]) for d in b["docs"] if not d.get("why")), "n_items": len(b.get("items", [])),
            "missing": len(dc.get("missing", [])), "other": len(dc.get("not_customer", [])), "extra": len(dc.get("not_required", [])),
            "tampered": sum(1 for v in b.get("variants", []) if v.get("perturbed")),
            "conditions": sorted({d["condition"] for d in b["docs"]}), "custom": bool(b.get("plan"))}


def _n(v) -> str:
    return re.sub(r"[\s\-·.,()]", "", unicodedata.normalize("NFKC", str(v or ""))).lower()


def profile_view(b: dict) -> list[dict]:
    """고객 프로필에서 서류끼리 맞아야 하는 값과, 그 값이 각 서류의 어디에 있는지."""
    from docgen.entities import make_profile
    from docgen.korean import fmt_date

    p = make_profile(b["customer_seed"])
    p.extra.update(scenario=b["scenario"], **SCENARIO_EXTRA.get(b["scenario"], {}))
    e, prop = p.employment, p.property
    vals = [("성명", p.person.name), ("주민등록번호", p.person.rrn), ("생년월일", fmt_date(p.person.birth, "dot")),
            ("주소", p.person.address.road_short), ("휴대전화", p.person.mobile), ("직장", e.company.name),
            ("입사일", fmt_date(e.hire_date, "dot")), ("연봉", f"{e.annual_salary:,}"), ("부동산 주소", prop.address.road_short),
            ("매매가", f"{prop.price:,}"), ("전세보증금", f"{prop.lease_deposit:,}"),
            ("계좌번호", p.accounts[0].number if p.accounts else "")]
    out = []
    base = [d for d in b["docs"] if not d.get("why")]
    digits = lambda s: re.sub(r"\D", "", str(s or ""))   # noqa: E731
    for name, v in vals:
        if not v:
            continue
        nv = _n(v)
        dv = digits(v) if name in ("생년월일", "입사일") else ""
        hits = []
        for d in base:
            for f in d["fields"]:
                fv = _n(f.get("value"))
                fd = digits(f.get("value"))
                same_date = bool(dv) and len(fd) in (6, 8) and fd in (dv, dv[2:])   # 1981.10.13 = 811013 = 1981년 10월 13일
                if fv and (same_date or (len(nv) >= 2 and fv == nv) or (len(nv) >= 8 and nv in fv)):
                    hits.append({"doc_id": d["doc_id"], "doc": d["name"], "key": f["key"], "label": f.get("label"),
                                 "value": f.get("value"), "page": f.get("page"), "bbox": f.get("bbox")})
        out.append({"what": name, "value": v, "where": hits})
    return out


_ROLE = re.compile(r"^(customer|applicant|holder|employee|borrower|debtor|tenant|person|insured|taxpayer|subscriber|"
                   r"grantor|principal|owner_self)\.")


def consistency(b: dict) -> list[dict]:
    """고객 일관성 검사 (경고만): 고객 본인 역할의 성명·주민번호·주소 칸이 프로필과 다르면 경고.
    변조판(cross_check)과 다른 고객·불필요 서류는 일부러 다르므로 보지 않는다."""
    from docgen.entities import make_profile

    p = make_profile(b["customer_seed"])
    want = {"name": _n(p.person.name), "rrn": _n(p.person.rrn)[:6], "address": _n(p.person.address.road_short)[:10]}
    out = []
    for d in b["docs"]:
        if d.get("why"):
            continue
        for f in d["fields"]:
            if not _ROLE.match(f["key"]) or f.get("value") in (None, ""):
                continue
            leaf = f["key"].split(".")[-1]
            v = _n(f["value"])
            bad = (leaf == "name" and v != want["name"]) or (leaf == "rrn" and not v.startswith(want["rrn"])) or \
                  (leaf == "address" and want["address"] not in v)
            if bad:
                out.append({"doc_id": d["doc_id"], "doc": d["name"], "key": f["key"], "label": f.get("label"),
                            "value": f["value"], "page": f.get("page"), "bbox": f.get("bbox"),
                            "expected": {"name": p.person.name, "rrn": p.person.rrn, "address": p.person.address.road_short}[leaf]})
    return out


# ---------------------------------------------------------------------------
# 시나리오 편집
# ---------------------------------------------------------------------------

def scenarios_view(forms: dict, bundle_counts: dict) -> list[dict]:
    reg = load_all()
    out = []
    for k, (name, docs) in SCENARIOS.items():
        out.append({"id": k, "name": name, "extra": SCENARIO_EXTRA.get(k, {}),
                    "docs": [{"id": d, "name": reg[d].name if d in reg else None, "reviewed": bool((forms.get(d) or {}).get("reviewed")),
                              "kind": "overlay" if d.startswith("hf") else "html"} for d in docs],
                    "bundles": bundle_counts.get(k, 0)})
    return out


def save_scenarios_list(items: list[dict]) -> None:
    reg = load_all()
    seen, clean = set(), []
    old_order = list(SCENARIOS)
    for s in items:
        sid = re.sub(r"[^\w]", "_", s.get("id") or "").strip("_")
        if not sid or sid in seen:
            raise ValueError(f"시나리오 ID 가 비었거나 겹칩니다: {s.get('id')!r}")
        seen.add(sid)
        docs = [d for d in s.get("docs", []) if d]
        unknown = [d for d in docs if d not in reg]
        if unknown:
            raise ValueError(f"{sid}: 모르는 서식 {unknown}")
        if not docs:
            raise ValueError(f"{sid}: 필수 서류가 하나도 없습니다")
        clean.append({"id": sid, "name": s.get("name") or sid, "docs": docs,
                      **({"extra": s["extra"]} if s.get("extra") else {})})
    # 이미 있던 시나리오의 순서는 바꾸지 않는다 (순서가 고객 seed 를 정함). 지운 것은 빠지고 새것은 끝에.
    kept = [s for s in clean if s["id"] in old_order]
    if [s["id"] for s in kept] != [x for x in old_order if x in seen]:
        raise ValueError("이미 있던 시나리오의 순서는 바꿀 수 없습니다 (고객 seed 가 바뀝니다). 새 시나리오는 끝에 더하세요")
    save_scenarios(clean)


# ---------------------------------------------------------------------------
# 학습 설정 내보내기 (2부 run_bank_pipeline.py)
# ---------------------------------------------------------------------------

def bank_training_config(registry, train_ids: list[str], bench_id: str, ocr_id: str | None, name: str) -> dict:
    """configs/bank_pipeline.json 의 data·ocr_check 조각과 실행할 명령. 나머지 칸은 예시 파일 값을 쓴다."""
    reg = registry.load()["datasets"]
    warn = []
    for i in [*train_ids, bench_id] + ([ocr_id] if ocr_id else []):
        if i not in reg:
            raise KeyError(i)
    bench = reg[bench_id]
    if bench["format"] != "docgen.bench":
        raise ValueError("평가 세트는 docgen.bench 형식(은행 업무)이어야 합니다")
    meta = json.loads((Path(bench["path"]) / "meta.json").read_text(encoding="utf-8"))
    if meta.get("split", "test") != "test":
        raise ValueError("평가 세트로 test split 데이터셋을 고르세요")
    if not bench.get("frozen"):
        warn.append("평가 세트를 아직 고정하지 않았습니다")
    for t in train_ids:
        m = json.loads((Path(reg[t]["path"]) / "meta.json").read_text(encoding="utf-8"))
        if m.get("split") != "train":
            raise ValueError(f"{t}: 학습 데이터는 train split 이어야 합니다")
        if m.get("version") != meta.get("version"):
            warn.append(f"{t}: 생성기 버전 {m.get('version')} ≠ 평가 세트 {meta.get('version')}")
    from .training_link import to_train_path

    pm = registry.path_map
    data = {"docgen_root": "../..", "train": [to_train_path(reg[t]["path"], pm) for t in train_ids],
            "benchmark": to_train_path(bench["path"], pm), "output_dir": f"../data/prepared-bank-{_slug(name)}"}
    cfg = {"workdir": f"../runs/{_slug(name)}", "data": data}
    if ocr_id:
        ocr = reg[ocr_id]
        if ocr["format"] != "bank_ocr/prepared":
            raise ValueError("OCR 유지용으로는 1부 OCR 데이터셋을 고르세요")
        op = to_train_path(ocr["path"], pm)
        data["replay"] = {"path": f"{op}/train_sft.jsonl", "count": 3000}
        cfg["ocr_check"] = {"tasks": f"{op}/benchmark_tasks.jsonl", "rows": 1000}
    file = f"configs/studio-{_slug(name)}.json"
    return {"pipeline": "2부 run_bank_pipeline.py", "file": file, "config": cfg, "warnings": warn,
            "command": f"cd training && python run_bank_pipeline.py --config {file}",
            "note": "model·gpus·sft·grpo·eval 칸은 configs/bank_pipeline.example.json 값을 쓴다. 모델 경로는 직접 확인하세요."}
