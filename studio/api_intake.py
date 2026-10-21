"""④ 서류 넣기 API (studio/DESIGN.md 15절). 묶음 폴더·OCR·묶기는 가져오기와 같다 (studio/importer.py).

  POST /api/intake/check        {path} → 폴더 검사 (서류·쪽·OCR·추출 결과·업무/건 구분)
  GET  /api/intake              서류 넣기로 만든 묶음 목록
  POST /api/intake              {name, path} → 묶음 만들기 + OCR·묶기 작업
  GET  /api/intake/{묶음}        ❶ 결과와 ❷에 넘길 양식 요약 (양식마다 서류 수·업무 분포·추출 결과·가까운 기존 서식)
  GET  /api/intake/{묶음}/judge  ❷ 모양마다 판정 제안(기존 서식·새 서식)·가까운 서식 3·쓸 길·추출 키 → 공통 키 제안·저장된 결정
  POST /api/intake/{묶음}/decide {formats: {모양: {kind, form_id?, name?, uses, keymap}}}
  GET  /api/intake/{묶음}/draft/{모양}       새 서식 초안 (값 칸·지울 자리·지운 배경 그림 이름)
  GET  /api/intake/{묶음}/draft-image/{그림}  지운 배경 그림
  GET  /api/intake/{묶음}/raw   원본 데이터로: 건 단위 학습/평가 나누기 미리보기와 마지막 내보내기
  POST /api/intake/{묶음}/raw   {ratio} → 의사정답 v1 폴더 두 개(<real_data_dir>/labels/<묶음>-raw/train·test)로 내보내기
"""
import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from . import importer as IM
from . import intake as IN
from . import intake_judge as IJ
from . import intake_raw as IR


def make_router(reg, jobs, guard, cfg: dict, real_root) -> APIRouter:
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

    def bdir(name: str):
        d = imports / IM._slug(name)
        if not (d / "formats.json").exists():
            raise HTTPException(404, f"묶기가 끝난 묶음이 없습니다: {name}")
        return d

    @r.get("/api/intake/{name}/judge")
    def judge(name: str):
        return {"formats": guard(IJ.judge, bdir(name))}

    class DecideReq(BaseModel):
        formats: dict

    @r.post("/api/intake/{name}/decide")
    def decide(name: str, req: DecideReq):
        return guard(IJ.decide, bdir(name), req.formats)

    @r.get("/api/intake/{name}/draft/{fid}")
    def draft(name: str, fid: str):
        return guard(IJ.draft, bdir(name), fid)

    @r.get("/api/intake/{name}/draft-image/{img}")
    def draft_image(name: str, img: str):
        f = bdir(name) / "drafts" / IM._slug(img)
        if not f.is_file():
            raise HTTPException(404, img)
        return FileResponse(f, headers={"Cache-Control": "no-store"})

    @r.get("/api/intake/{name}/raw")
    def raw(name: str, ratio: float | None = None):
        return {**guard(IR.preview, bdir(name), ratio), "real_root_set": bool(cfg.get("real_data_dir"))}

    class RawReq(BaseModel):
        ratio: float | None = None

    @r.post("/api/intake/{name}/raw")
    def raw_export(name: str, req: RawReq):
        if req.ratio is not None and not 0 <= req.ratio < 1:
            raise HTTPException(400, "평가 비율은 0 이상 1 미만입니다")
        return guard(IR.export, bdir(name), real_root, req.ratio)

    return r
