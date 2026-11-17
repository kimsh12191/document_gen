"""⑥ 데이터셋 만들기(은행 서류·합성 OCR), ⑧ 작업 API.

서버 쪽 일은 studio/bank_data.py(은행 서류), studio/ocr_data.py(합성 OCR)가 한다. 학습 설정은 손으로 (guide/train/sweep.md).

  GET    /api/recipes                     레시피 목록 · GET /api/recipes/options 편집용 목록(그룹·촬영 조건·서식틀)
  GET/PUT/DELETE /api/recipes/{이름}       레시피 하나
  POST   /api/builds                      데이터셋 만들기 {recipe, name, workers} → 작업 (레시피 track 이 ocr 이면 합성 OCR).
                                          같은 이름의 폴더가 있거나 그 폴더로 도는 작업이 있으면 409
  GET    /api/builds                      생성 작업 목록 (⑥ 생성 현황). 읽기만 한다 — 놓친 자동 등록은 띄울 때 복구 (build_registration.py)
  GET    /api/jobs                       작업 목록 · GET /api/jobs/{id} · POST /api/jobs/{id}/cancel
  DELETE /api/jobs/{id}                  끝난 작업 기록 지우기 · POST /api/builds/cleanup 지워도 되는 생성 기록 모두 (데이터셋 폴더는 그대로)
"""
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from . import bank_data as BD


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

        return {"jobs": guard(builds, jobs)}

    @r.get("/api/jobs")
    def list_jobs(kind: str | None = None):
        return {"jobs": jobs.list(kind)}

    @r.get("/api/jobs/{job_id}")
    def job(job_id: str):
        return guard(jobs.get, job_id)

    @r.post("/api/jobs/{job_id}/cancel")
    def cancel(job_id: str):
        return guard(jobs.cancel, job_id)

    @r.delete("/api/jobs/{job_id}")
    def forget(job_id: str):
        from .build_registration import forget_job

        guard(forget_job, jobs, reg, job_id)
        return {"ok": True}

    @r.post("/api/builds/cleanup")
    def cleanup():
        from .build_registration import cleanup_jobs

        return {"removed": guard(cleanup_jobs, jobs, reg)}

    return r
