"""⑥ 데이터셋 API (studio/datasets.py 를 부른다). 모델 답·채점은 학습 서버의 python -m train (guide/eval.md).

  GET    /api/datasets                       등록부 목록 (먼저 놓친 자동 등록을 복구한다, build_registration.py)
  POST   /api/datasets                       폴더 등록 {path, name, source?, gt?, real_data?}
  GET    /api/datasets/{id}                  데이터셋 하나: 정보, 과제별 문항 수, 설명서
  DELETE /api/datasets/{id}                  등록만 지운다 (폴더는 그대로)
  PATCH  /api/datasets/{id}                  이름·출처·정답 종류·실서류 여부
  POST   /api/datasets/{id}/freeze           고정 {frozen}
  PUT    /api/datasets/{id}/card             설명서의 사람 칸 {purpose, limits, not_for} · GET /api/datasets/{id}/card.md 설명서 원문
  GET    /api/datasets/{id}/composition      구성 (과제·정답 구조별 문항 수, 생성 레시피·버전)
  GET    /api/datasets/{id}/items            문항 {task, offset, limit, q, 구성 필터}
  GET    /api/datasets/{id}/file?p=          문항 이미지
"""

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel

from . import datasets as DS


def make_router(reg: DS.Registry, guard, jobs=None) -> APIRouter:
    r = APIRouter()

    def ds_or_404(ds_id: str) -> dict:
        try:
            return reg.get(ds_id)
        except KeyError:
            raise HTTPException(404, f"등록되지 않은 데이터셋: {ds_id}")

    def card_path(ds: dict) -> Path:
        return (Path(ds["path"]) / "DATASET.md") if not ds.get("registered") else (reg.ws / "cards" / f"{ds['id']}.md")

    def write_card(ds: dict) -> str:
        md = DS.card_markdown(ds)
        if ds.get("frozen") and card_path(ds).exists() and not ds.get("registered"):
            return card_path(ds).read_text(encoding="utf-8")   # 고정한 데이터셋은 자동 칸을 다시 쓰지 않는다
        p = card_path(ds)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(md, encoding="utf-8")
        return md

    @r.get("/api/datasets")
    def list_datasets():
        if jobs is not None:
            from .build_registration import recover_completed

            guard(recover_completed, jobs, reg)
        d = reg.load()
        out = []
        for k, v in d["datasets"].items():
            out.append({"id": k, **{x: v.get(x) for x in ("name", "groups", "kind", "split", "format", "source", "gt", "real_data", "frozen",
                                                         "version", "counts", "created", "registered", "path")},
                        "exists": Path(v["path"]).exists(), "n_runs": len(v.get("runs", [])),
                        "n_scores": len(saved_scores(k))})
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
        ds = guard(reg.register, req.path, req.name, **meta)
        write_card(ds)
        return ds

    @r.get("/api/datasets/{ds_id}")
    def get_dataset(ds_id: str):
        ds = ds_or_404(ds_id)
        return {**ds, "exists": Path(ds["path"]).exists(),
                "tasks": {t: len(v) for t, v in guard(DS.items, ds).items()} if Path(ds["path"]).exists() else {},
                "card_md": write_card(ds), "card_file": str(card_path(ds))}

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

    @r.patch("/api/datasets/{ds_id}")
    def patch(ds_id: str, req: dict):
        return guard(reg.set_meta, ds_id, req)

    class FreezeReq(BaseModel):
        frozen: bool = True

    @r.post("/api/datasets/{ds_id}/freeze")
    def freeze(ds_id: str, req: FreezeReq):
        ds = guard(reg.set_frozen, ds_id, req.frozen)
        write_card(ds)
        return ds

    @r.put("/api/datasets/{ds_id}/card")
    def card(ds_id: str, req: dict):
        ds = guard(reg.set_card, ds_id, req)
        return {"card_md": write_card(ds)}

    @r.get("/api/datasets/{ds_id}/card.md", response_class=PlainTextResponse)
    def card_md(ds_id: str):
        return write_card(ds_or_404(ds_id))

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
