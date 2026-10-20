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


def ocr_training_config(registry, train_ids: list[str], bench_id: str, name: str) -> dict:
    """1부 run_pipeline.py: 파이프라인 설정(configs/studio-<이름>.json) + 데이터 설정(configs/studio-<이름>-data.json).
    데이터 설정의 output_dir 이 studio 가 만든(또는 등록한) prepare 결과라, 파이프라인은 준비 단계를 건너뛴다."""
    from .bank_data import _slug
    from .training_link import to_train_path

    reg = registry.load()["datasets"]
    if len(train_ids) != 1:
        raise ValueError("1부 학습은 OCR 데이터셋 하나를 고릅니다 (실서류+합성을 함께 쓰려면 합친 데이터셋을 먼저 만드세요)")
    t = train_ids[0]
    for i in (t, bench_id):
        if i not in reg:
            raise KeyError(i)
        if reg[i]["format"] != "bank_ocr/prepared":
            raise ValueError(f"{i}: 1부 OCR 데이터셋(prepare 결과)이 아닙니다")
    root = Path(reg[t]["path"])
    n_train = (reg[t].get("counts") or {}).get("train_tasks", 0)
    if not n_train:
        raise ValueError(f"{t}: 학습 문항(train_tasks)이 없습니다 (평가 전용 세트는 학습에 쓸 수 없음)")
    warn = []
    if bench_id != t:
        warn.append("1부 파이프라인은 학습 데이터셋 안의 benchmark 로 평가합니다. 고른 평가 세트에는 결과를 붙이기만 합니다")
    snap = root / "config.snapshot.json"
    data_cfg = json.loads(snap.read_text(encoding="utf-8")) if snap.exists() else \
        json.loads((ROOT / "ocr" / "config.example.json").read_text(encoding="utf-8"))
    data_cfg = {k: v for k, v in data_cfg.items() if k != "studio"}
    data_cfg["output_dir"] = to_train_path(str(root), registry.path_map)
    n = _slug(name)
    data_file = f"configs/studio-{n}-data.json"
    cfg = {"workdir": f"../runs/{n}", "data_config": f"studio-{n}-data.json"}
    return {"pipeline": "1부 run_pipeline.py", "file": f"configs/studio-{n}.json", "config": cfg, "warnings": warn,
            "extra_files": {data_file: data_cfg},
            "dir": "ocr", "command": f"cd ocr && python run_pipeline.py --config configs/studio-{n}.json",
            "note": "model·gpus·sft·grpo·eval 칸은 configs/pipeline.example.json 값을 쓴다. 데이터 설정은 "
                    f"{data_file} (output_dir 에 DONE.json 이 있어 준비 단계를 건너뜀)."}
