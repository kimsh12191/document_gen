"""④ 가져오기 · ⑤ 검수(OCR 검수) API.

  GET  /api/imports                         묶음 목록
  POST /api/imports                         묶음 만들기 {name, kind: folder|docgen, path?, recipe?, real_data, public} → OCR 작업
  POST /api/imports/upload                  파일 올려 묶음 만들기 (multipart: name, files…)
  GET  /api/imports/{묶음}                  묶음 정보, 포맷·양식, 쪽 목록(지문 없이)
  POST /api/imports/{묶음}/regroup          다시 묶기 · POST /api/imports/{묶음}/merge {src, dst} · /split {pages, name}
  POST /api/imports/{묶음}/formats/{포맷}    결정·이름 {decision: {kind, form_id?}, name}
  POST /api/imports/{묶음}/template         템플릿으로 {format, pages, form_id, name, drafts} → overlay(image) 서식 (+ 값 자리·지우기 초안)
  POST /api/imports/{묶음}/ocr-set          OCR 벤치마크로 {formats, gt: pseudo|reviewed, split, name} → 작업 → 등록부
  GET  /api/imports/{묶음}/page?p=          쪽 그림 · GET /api/imports/{묶음}/ocr?p= OCR 검수용 단어(원래·검수본)
  PUT  /api/imports/{묶음}/ocr?p=           OCR 검수 저장 {words, done}
  POST /api/form-prints                     기존 서식 지문 만들기 (가까운 기존 서식 찾기) → 작업
"""
import json
import shutil
import time
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

from . import importer as IM
from . import ocr_review as OR


def make_router(reg, jobs, guard, cfg: dict, real_root: Path) -> APIRouter:
    r = APIRouter()
    imports = reg.ws / "imports"

    def bdir(name: str) -> Path:
        d = imports / IM._slug(name)
        if not (d / "batch.json").exists():
            raise HTTPException(404, f"묶음이 없습니다: {name}")
        return d

    def start_ocr(d: Path) -> dict:
        from .jobs import python

        return jobs.start("import_ocr", f"가져오기 OCR·묶기: {d.name}", [python(), "-m", "studio.importer", "ocr", str(d)],
                          lambda job: {"batch": d.name}, {"batch": d.name})

    @r.get("/api/imports")
    def list_imports():
        out = []
        for f in sorted(imports.glob("*/batch.json")) if imports.exists() else []:
            b = json.loads(f.read_text(encoding="utf-8"))
            rows = IM._jsonl(f.parent / "pages.jsonl")
            fx = json.loads((f.parent / "formats.json").read_text(encoding="utf-8")) if (f.parent / "formats.json").exists() else {}
            out.append({**b, "n_pages": len(rows), "n_ocr": sum(1 for x in rows if x.get("ocr")), "n_formats": len(fx.get("formats", [])),
                        "review": OR.summary(real_root, b["name"])})
        return {"imports": out, "import_dir": cfg.get("import_dir"), "real_root": str(real_root),
                "real_root_set": bool(cfg.get("real_data_dir")), "ocr_set": bool((cfg.get("ocr") or {}).get("revision"))}

    class CreateReq(BaseModel):
        name: str
        kind: str = "folder"
        path: str | None = None
        recipe: dict | None = None
        real_data: bool = True
        public: bool = False

    @r.post("/api/imports")
    def create(req: CreateReq):
        if req.kind == "docgen":
            return guard(_from_docgen, req)
        b = guard(IM.create_batch, reg.ws, req.name, req.path, req.real_data, req.public, cfg.get("ocr"), cfg.get("import_dir"))
        job = start_ocr(imports / b["name"])
        return {**b, "job": job["id"]}

    def _from_docgen(req: CreateReq) -> dict:
        """시험용: 생성 데이터로 묶음 (OCR 대신 생성 정답을 OCR 결과로). 서식 ID 를 알아 묶기 정확도를 잴 수 있다."""
        from .jobs import python

        recipe = {"track": "ocr", "split": "benchmark", "types": ["employment_certificate", "career_certificate", "hf169"],
                  "per_doc": 3, **(req.recipe or {})}
        d = imports / IM._slug(req.name)
        if d.exists():
            raise ValueError(f"이미 있는 묶음 이름입니다: {d.name}")
        d.mkdir(parents=True)
        (d / "pages").mkdir()
        (d / "recipe.json").write_text(json.dumps(recipe, ensure_ascii=False), encoding="utf-8")
        batch = {"name": d.name, "created": time.strftime("%Y-%m-%d %H:%M"), "source": {"kind": "docgen", "path": str(d / "gen")},
                 "real_data": False, "public": True, "ocr": {"revision": "docgen-synthetic"}, "stage": "generating"}
        IM._write_json(d / "batch.json", batch)
        IM._write_jsonl(d / "pages.jsonl", [])
        cmd = [python(), "-m", "studio.importer", "from-docgen", str(d)]
        job = jobs.start("import_ocr", f"가져오기(생성 데이터): {d.name}", cmd, lambda job: {"batch": d.name}, {"batch": d.name})
        return {**batch, "job": job["id"]}

    @r.post("/api/imports/upload")
    async def upload(name: str = Form(...), real_data: bool = Form(True), public: bool = Form(False),
                     files: list[UploadFile] = File(...)):
        d = imports / IM._slug(name)
        if d.exists():
            raise HTTPException(400, f"이미 있는 묶음 이름입니다: {d.name}")
        raw = reg.ws / "uploads" / d.name
        raw.mkdir(parents=True, exist_ok=False)
        for f in files:
            dest = raw / Path(f.filename or "file").name
            with open(dest, "wb") as out:
                shutil.copyfileobj(f.file, out)
        b = guard(IM.create_batch, reg.ws, name, str(raw), real_data, public, cfg.get("ocr"), None, "upload")
        job = start_ocr(imports / b["name"])
        return {**b, "job": job["id"]}

    @r.get("/api/imports/{name}")
    def get_batch(name: str):
        d = bdir(name)
        b = json.loads((d / "batch.json").read_text(encoding="utf-8"))
        rows = IM._jsonl(d / "pages.jsonl")
        fx = json.loads((d / "formats.json").read_text(encoding="utf-8")) if (d / "formats.json").exists() else {"formats": []}
        st = OR.states(real_root, b["name"])
        pages = [{"id": x["id"], "doc": x["doc"], "has_ocr": bool(x.get("ocr")), "name": (x.get("fp") or {}).get("name"),
                  "n_words": x.get("n_words"), "review": (st.get(x["id"]) or {}).get("status"),
                  **({"truth": x["truth"]} if x.get("truth") else {})} for x in rows]
        acc = None
        if any(x.get("truth") for x in rows) and fx["formats"]:   # 생성 데이터: 서식 ID 대비 묶기 정확도 (순도)
            from collections import Counter
            tr = {x["id"]: x.get("truth") for x in rows}
            pure = sum(Counter(tr[p] for p in f["pages"]).most_common(1)[0][1] for f in fx["formats"])
            acc = {"purity": round(pure / max(1, sum(len(f["pages"]) for f in fx["formats"])), 3),
                   "formats": len(fx["formats"]), "true_forms": len({v for v in tr.values() if v})}
        return {**b, "pages": pages, "formats": fx["formats"], "grouped": fx.get("grouped"), "accuracy": acc,
                "review": OR.summary(real_root, b["name"]), "has_prints": bool(IM.load_form_prints())}

    @r.post("/api/imports/{name}/regroup")
    def regroup(name: str):
        return guard(IM.run_group, bdir(name))

    class MergeReq(BaseModel):
        src: str
        dst: str

    @r.post("/api/imports/{name}/merge")
    def merge(name: str, req: MergeReq):
        return guard(IM.merge_formats, bdir(name), req.src, req.dst)

    class SplitReq(BaseModel):
        pages: list[str]
        name: str = ""

    @r.post("/api/imports/{name}/split")
    def split(name: str, req: SplitReq):
        return guard(IM.split_pages, bdir(name), req.pages, req.name)

    class DecisionReq(BaseModel):
        decision: dict | None = None
        name: str | None = None

    @r.post("/api/imports/{name}/formats/{fid}")
    def decide(name: str, fid: str, req: DecisionReq):
        return guard(IM.set_decision, bdir(name), fid, req.decision, req.name)

    class TemplateReq(BaseModel):
        format: str
        pages: list[str]
        form_id: str
        name: str
        drafts: bool = True

    @r.post("/api/imports/{name}/template")
    def template(name: str, req: TemplateReq):
        from docgen import realform as RF

        res = guard(IM.create_template, bdir(name), req.format, req.pages, req.form_id, req.name, cfg.get("private_forms_dir"), req.drafts)
        RF.register_images()   # 바로 서식 목록·영역 편집기에 나오게
        return res

    class OcrSetReq(BaseModel):
        formats: list[str] = []
        gt: str = "pseudo"
        split: str = "benchmark"
        name: str

    @r.post("/api/imports/{name}/ocr-set")
    def ocr_set(name: str, req: OcrSetReq):
        from .jobs import python

        if req.gt not in ("pseudo", "reviewed") or req.split not in ("benchmark", "train"):
            raise HTTPException(400, "gt 는 pseudo/reviewed, split 은 benchmark/train")
        d = bdir(name)
        out = reg.ws / "datasets" / IM._slug(req.name)
        if out.exists():
            raise HTTPException(400, f"이미 있는 폴더입니다: {out}")
        info = guard(IM.ocr_set_files, d, out, req.formats or None, req.gt, req.split, real_root)
        cmd = [python(), "-m", "bank_ocr", "prepare", "--config", info["config"]]

        def done(job):
            from .build_registration import register_output

            return register_output(reg, spec)
        spec = {"path": str(out / "prepared"), "name": IM._slug(req.name), "meta": {"dataset_json": "../import_set.json",
                "purpose": f"가져온 묶음 {d.name} 의 OCR ({'사람 검수' if req.gt == 'reviewed' else '사내 OCR 그대로'})"}}
        job = jobs.start("build_ocr", f"OCR 벤치마크로: {req.name} (묶음 {d.name}, 쪽 {info['pages']})", cmd, done,
                         {"batch": d.name, "dataset": spec}, cwd=IM.ROOT / "training")
        return {"job": job["id"], **info}

    @r.get("/api/imports/{name}/page")
    def page_image(name: str, p: str, w: int = 0):
        """쪽 그림 (OCR 이 본 그림). w 를 주면 그 너비의 미리보기 (묶음 폴더 thumbs/ 에 둔다)."""
        d = bdir(name)
        row = next((x for x in IM._jsonl(d / "pages.jsonl") if x["id"] == p), None)
        if row is None:
            raise HTTPException(404, "쪽이 없습니다")
        src = Path(row.get("image") or row["source"])
        if not w:
            return FileResponse(src)
        w = max(80, min(w, 1200))
        th = d / "thumbs" / f"{IM._safe(p)}_{w}.jpg"
        if not th.exists():
            from PIL import Image

            th.parent.mkdir(exist_ok=True)
            with Image.open(src) as im:
                im = im.convert("RGB")
                im.thumbnail((w, w * 4))
                im.save(th, quality=85)
        return FileResponse(th)

    @r.get("/api/imports/{name}/ocr")
    def ocr_page(name: str, p: str):
        page = guard(OR.load_page, bdir(name), p, real_root)
        return {**page, "order": OR.suspicious_order(page)}

    class OcrSave(BaseModel):
        words: list[dict]
        done: bool = False

    @r.put("/api/imports/{name}/ocr")
    def save_ocr(name: str, p: str, req: OcrSave):
        return guard(OR.save_page, bdir(name), p, req.words, real_root, cfg.get("user") or "studio", req.done)

    @r.post("/api/form-prints")
    def form_prints():
        from .jobs import python

        return jobs.start("form_prints", "기존 서식 지문 만들기 (가까운 기존 서식 찾기용)",
                          [python(), "-m", "studio.importer", "form-prints"])

    return r
