"""⑥ 데이터셋 API (studio/datasets.py 를 부른다). 모델 답·채점은 학습 서버의 python -m train (guide/train/steps.md).

  GET    /api/datasets                       등록부 목록 (읽기만. 놓친 자동 등록 복구·옛 줄 고치기는 띄울 때 한 번, app.py)
  POST   /api/datasets                       폴더 등록 {path, name, source?, gt?, real_data?} (설명서도 쓴다)
  GET    /api/datasets/{id}                  데이터셋 하나: 정보, 과제별 문항 수, 설명서 (읽기만)
  DELETE /api/datasets/{id}                  등록만 지운다 (폴더는 그대로)
  POST   /api/datasets/{id}/freeze           고정 {frozen}
  PUT    /api/datasets/{id}/card             설명서의 사람 칸 {purpose, limits, not_for}
  GET    /api/datasets/{id}/composition      구성 (과제·정답 구조별 문항 수, 생성 레시피·버전)
  GET    /api/datasets/{id}/items            문항 {task, offset, limit, q, 구성 필터}
  GET    /api/datasets/{id}/file?p=          문항 이미지
"""

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from . import datasets as DS


def make_router(reg: DS.Registry, guard) -> APIRouter:
    r = APIRouter()

    def ds_or_404(ds_id: str) -> dict:
        try:
            return reg.get(ds_id)
        except KeyError:
            raise HTTPException(404, f"등록되지 않은 데이터셋: {ds_id}")

    @r.get("/api/datasets")
    def list_datasets():
        d = guard(reg.load)
        out = []
        for k, v in d["datasets"].items():
            out.append({"id": k, **{x: v.get(x) for x in ("name", "groups", "kind", "split", "format", "source", "gt", "real_data", "frozen",
                                                         "version", "counts", "created", "registered", "path")},
                        "exists": Path(v["path"]).exists()})
        return {"datasets": out, "workspace": str(reg.ws), "sources": DS.SOURCE_NAME, "gts": DS.GT_NAME, "groups": DS.GROUP_NAME}

    class RegisterReq(BaseModel):
        path: str
        name: str = ""
        source: str | None = None
        gt: str | None = None
        real_data: bool | None = None

    @r.post("/api/datasets")
    def register(req: RegisterReq):
        meta = {k: v for k, v in req.model_dump().items() if k not in ("path", "name") and v is not None}
        return guard(reg.register, req.path, req.name, **meta)

    @r.get("/api/datasets/{ds_id}")
    def get_dataset(ds_id: str):
        ds = ds_or_404(ds_id)
        return {**ds, "exists": Path(ds["path"]).exists(),
                "tasks": {t: len(v) for t, v in guard(DS.items, ds).items()} if Path(ds["path"]).exists() else {},
                "card_md": guard(reg.card_text, ds), "card_file": str(reg.card_path(ds))}

    @r.delete("/api/datasets/{ds_id}")
    def unregister(ds_id: str):
        guard(reg.unregister, ds_id)
        return {"ok": True}

    @r.get("/api/datasets/{ds_id}/composition")
    def composition(ds_id: str):
        from docgen.bench.tracking import composition as summarize

        ds = ds_or_404(ds_id)
        all_rows = guard(DS.items, ds)
        eval_rows = guard(DS.items, ds, evaluation=True)
        root = Path(ds["path"])
        meta = json.loads((root / "meta.json").read_text(encoding="utf-8"))
        recipe = json.loads((root / "dataset.json").read_text(encoding="utf-8")) if (root / "dataset.json").exists() else {}
        if not recipe:
            ocr_info = root.parent / "ocr_set.json" if root.name == "prepared" else root / "ocr_set.json"
            if ocr_info.exists():
                recipe = json.loads(ocr_info.read_text(encoding="utf-8"))
        return {"all": summarize(x for rows in all_rows.values() for x in rows),
                "evaluation": summarize(x for rows in eval_rows.values() for x in rows),
                "provenance": {k: recipe.get(k, meta.get(k)) for k in
                               ("generator_commit", "version", "created", "recipe", "form_hashes")}}

    class FreezeReq(BaseModel):
        frozen: bool = True

    @r.post("/api/datasets/{ds_id}/freeze")
    def freeze(ds_id: str, req: FreezeReq):
        return guard(reg.set_frozen, ds_id, req.frozen)

    @r.put("/api/datasets/{ds_id}/card")
    def card(ds_id: str, req: dict):
        ds = guard(reg.set_card, ds_id, req)
        return {"card_md": reg.card_text(ds)}

    @r.get("/api/datasets/{ds_id}/items")
    def list_items(ds_id: str, task: str = "", offset: int = 0, limit: int = 20, q: str = "",
                   task_group: str = "", label_format: str = "", doc_type: str = "", evaluation_only: bool = False):
        ds = ds_or_404(ds_id)
        by_task = guard(DS.items, ds)
        if task and task not in by_task:
            raise HTTPException(404, f"과제가 없습니다: {task}")
        rows = by_task[task] if task else [x for v in by_task.values() for x in v]
        if evaluation_only:
            evaluation_ids = {x["id"] for rs in guard(DS.items, ds, evaluation=True).values() for x in rs}
            rows = [x for x in rows if x["id"] in evaluation_ids]
        from docgen.bench.tracking import facets

        filters = {"task_group": task_group, "label_format": label_format, "doc_type": doc_type}
        rows = [x for x in rows if all(not v or facets(x)[k] == v for k, v in filters.items())]
        if q:
            rows = [x for x in rows if q.lower() in json.dumps(x, ensure_ascii=False).lower()]
        page = rows[offset: offset + limit]
        return {"total": len(rows), "offset": offset, "items": [DS.view_item(ds, it) for it in page]}

    @r.get("/api/datasets/{ds_id}/file")
    def file(ds_id: str, p: str):
        ds = ds_or_404(ds_id)
        f = reg.resolve_file(ds, p)
        if f is None or not reg.allowed(ds, f):
            raise HTTPException(404, "파일을 찾을 수 없습니다")
        return FileResponse(f)

    return r
