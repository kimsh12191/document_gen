"""③ 시나리오·묶음, ⑥ 데이터셋 만들기(은행 업무), ⑧ 작업, 학습 연결 API.

  GET    /api/recipes                     레시피 목록 · GET /api/recipes/options 편집용 목록(시나리오·사례·기본 규칙)
  GET/PUT/DELETE /api/recipes/{이름}       레시피 하나
  POST   /api/builds                      은행 업무 데이터셋 만들기 {recipe, name, workers} → 작업
  GET    /api/jobs                        작업 목록 · GET /api/jobs/{id} · POST /api/jobs/{id}/cancel
  GET    /api/datasets/{id}/bundles       업무 묶음 목록 · GET /api/datasets/{id}/bundles/{묶음} 상세(서류, 고객 프로필, 검사)
  GET/PUT /api/scenarios                  시나리오 목록·저장
  POST   /api/training/preview            학습 설정 조각 미리보기 {pipeline, train, benchmark, ocr, name}
  POST   /api/training/save               설정 파일 쓰기 + 학습 기록
  GET    /api/trainings                   학습 기록과 진행 (끝난 학습은 평가 세트에 모델 답으로 자동으로 붙음)
"""
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from . import bank_data as BD
from . import catalog
from . import training_link as TL


def make_router(reg, jobs, guard) -> APIRouter:
    r = APIRouter()

    @r.get("/api/recipes")
    def recipes():
        return {"recipes": BD.list_recipes()}

    @r.get("/api/recipes/options")
    def recipe_options():
        return BD.options()

    @r.get("/api/recipes/{name}")
    def recipe(name: str):
        return guard(BD.get_recipe, name)

    @r.put("/api/recipes/{name}")
    def save_recipe(name: str, req: dict[str, Any]):
        return guard(BD.save_recipe, name, req)

    @r.delete("/api/recipes/{name}")
    def delete_recipe(name: str):
        guard(BD.delete_recipe, name)
        return {"ok": True}

    class BuildReq(BaseModel):
        recipe: str
        name: str
        workers: int = 1

    @r.post("/api/builds")
    def build(req: BuildReq):
        rec = guard(BD.get_recipe, req.recipe)
        if rec.get("track", "bank") == "ocr":
            from . import ocr_data

            return guard(ocr_data.start_build, jobs, reg, BD.RECIPES, req.recipe, req.name, req.workers)
        return guard(BD.start_build, jobs, reg, req.recipe, req.name, req.workers)

    @r.get("/api/builds")
    def list_builds():
        from .build_registration import list_builds as builds

        return {"jobs": guard(builds, jobs, reg)}

    @r.get("/api/jobs")
    def list_jobs(kind: str | None = None):
        return {"jobs": jobs.list(kind)}

    @r.get("/api/jobs/{job_id}")
    def job(job_id: str):
        return guard(jobs.get, job_id)

    @r.post("/api/jobs/{job_id}/cancel")
    def cancel(job_id: str):
        return guard(jobs.cancel, job_id)

    def ds_or_404(ds_id):
        try:
            return reg.get(ds_id)
        except KeyError:
            raise HTTPException(404, f"등록되지 않은 데이터셋: {ds_id}")

    @r.get("/api/datasets/{ds_id}/bundles")
    def bundles(ds_id: str):
        ds = ds_or_404(ds_id)
        return {"bundles": [BD.bundle_summary(b) for b in guard(BD.bundles, ds)]}

    @r.get("/api/datasets/{ds_id}/bundles/{bid}")
    def bundle(ds_id: str, bid: str):
        ds = ds_or_404(ds_id)
        b = next((x for x in guard(BD.bundles, ds) if x["bundle_id"] == bid), None)
        if b is None:
            raise HTTPException(404, f"묶음이 없습니다: {bid}")
        return {**b, "summary": BD.bundle_summary(b), "profile": guard(BD.profile_view, b),
                "consistency": guard(BD.consistency, b)}

    @r.get("/api/scenarios")
    def scenarios():
        counts: dict = {}
        for k, v in reg.load()["datasets"].items():
            if v["format"] == "docgen.bench":
                try:
                    for b in BD.bundles({**v, "id": k}):
                        counts[b["scenario"]] = counts.get(b["scenario"], 0) + 1
                except OSError:
                    pass
        return {"scenarios": BD.scenarios_view(catalog._catalog(), counts),
                "cases": BD.options()["cases"], "rules": BD.options()["rules"],
                "processing_rules": BD.PROCESS.RULE_TITLES, "compare_operators": BD.PROCESS.COMPARE_OPS}

    class ScenariosReq(BaseModel):
        scenarios: list[dict]

    @r.put("/api/scenarios")
    def save_scenarios(req: ScenariosReq):
        guard(BD.save_scenarios_list, req.scenarios)
        catalog._scenarios_of.cache_clear()
        return scenarios()

    class TrainReq(BaseModel):
        pipeline: str = "bank"
        train: list[str] = []
        benchmark: str
        ocr: str | None = None
        name: str

    def _info(req: TrainReq) -> dict:
        if req.pipeline == "bank":
            return BD.bank_training_config(reg, req.train, req.benchmark, req.ocr, req.name)
        from . import ocr_data

        return ocr_data.ocr_training_config(reg, req.train, req.benchmark, req.name)

    @r.post("/api/training/preview")
    def training_preview(req: TrainReq):
        return guard(_info, req)

    @r.post("/api/training/save")
    def training_save(req: TrainReq):
        info = guard(_info, req)
        return guard(TL.write_training, reg, info, list(dict.fromkeys([*req.train, req.benchmark] + ([req.ocr] if req.ocr else []))),
                     req.benchmark, req.name)

    @r.get("/api/trainings")
    def trainings():
        return {"trainings": [TL.status(reg, t) for t in reg.load().get("trainings", [])]}

    return r
