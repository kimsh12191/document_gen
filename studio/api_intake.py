"""④ 서류 넣기 API (studio/DESIGN.md 15절). 묶음 폴더·OCR·묶기는 가져오기와 같다 (studio/importer.py).

  POST /api/intake/check        {path} → 폴더 검사 (서류·쪽·OCR·추출 결과·업무/건 구분)
  GET  /api/intake              서류 넣기로 만든 묶음 목록
  POST /api/intake              {name, path} → 묶음 만들기 + OCR·묶기 작업
  GET  /api/intake/{묶음}        ❶ 결과와 ❷에 넘길 양식 요약 (양식마다 서류 수·업무 분포·추출 결과·가까운 기존 서식)
"""
import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from . import importer as IM
from . import intake as IN


def make_router(reg, jobs, guard, cfg: dict) -> APIRouter:
    r = APIRouter()
    imports = reg.ws / "imports"

    class CheckReq(BaseModel):
        path: str

    @r.post("/api/intake/check")
    def check(req: CheckReq):
        res = guard(IN.check, req.path)
        return {k: res.get(k) for k in ("ok", "errors", "warnings", "summary", "root", "images")} | {
            "examples": [{"id": d["id"], "scenario": d["scenario"], "case": d["case"], "pages": len(d["pages"]), "pred": "pred" in d}
                         for d in res.get("docs", [])[:8]]}

    @r.get("/api/intake")
    def list_intake():
        out = []
        for f in sorted(imports.glob("*/batch.json")) if imports.exists() else []:
            b = json.loads(f.read_text(encoding="utf-8"))
            if b.get("source", {}).get("kind") != "intake":
                continue
            fx = json.loads((f.parent / "formats.json").read_text(encoding="utf-8")) if (f.parent / "formats.json").exists() else {}
            out.append({k: b[k] for k in ("name", "created", "stage", "real_data")} | {"path": b["source"]["path"],
                       "summary": b["intake"]["summary"], "n_formats": len(fx.get("formats", []))})
        return {"batches": out, "import_dir": cfg.get("import_dir"), "ocr_set": bool((cfg.get("ocr") or {}).get("revision"))}

    class CreateReq(BaseModel):
        name: str
        path: str

    @r.post("/api/intake")
    def create(req: CreateReq):
        from .jobs import python

        b = guard(IN.create_batch, reg.ws, req.name, req.path, cfg.get("ocr"), cfg.get("import_dir"))
        d = imports / b["name"]
        job = jobs.start("import_ocr", f"서류 넣기 OCR·묶기: {d.name}", [python(), "-m", "studio.importer", "ocr", str(d)],
                         lambda job: {"batch": d.name}, {"batch": d.name})
        return {"name": b["name"], "summary": b["intake"]["summary"], "job": job["id"]}

    @r.get("/api/intake/{name}")
    def get(name: str):
        d = imports / IM._slug(name)
        if not (d / "batch.json").exists():
            raise HTTPException(404, f"묶음이 없습니다: {name}")
        out = IN.overview(d)
        b = out["batch"]
        running = [j for j in jobs.list("import_ocr") if (j.get("info") or {}).get("batch") == b["name"] and j.get("status") == "running"]
        rows = IM._jsonl(d / "pages.jsonl")
        return {"name": b["name"], "stage": b["stage"], "real_data": b["real_data"], "path": b["source"]["path"],
                "summary": b["intake"]["summary"], "warnings": b["intake"]["warnings"],
                "n_ocr": sum(1 for x in rows if x.get("ocr")), "n_pages": len(rows),
                "job": running[0] if running else None, "formats": out["formats"]}

    return r
