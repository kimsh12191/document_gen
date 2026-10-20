"""① 서식 › html 편집 · 복제, ⑧ 작업 › 분석기 API (DESIGN.md 4.3, 7절).

html 서식 (화면에서 만든 것: docgen/htmlform.py)
  GET  /api/forms/{id}/html               템플릿·form.json·출처·원본 그림 여부
  PUT  /api/forms/{id}/html               저장 {template, form} (문법·형식 검사 뒤)
  POST /api/forms/{id}/html/render        저장 전 미리보기 {template?, form?, seed, rows: auto|min|max, condition} → 라벨 + 검사
  GET  /api/forms/{id}/source-image       분석기에 보낸 원본 그림 (편집기의 겹쳐 보기)
  POST /api/forms/{id}/clone              복제 {new_id, name, private}
  POST /api/forms/{id}/html/redo          분석기에 다시 고쳐 {provider, comment, template?, form?} → 분석기 작업
분석기
  GET  /api/providers · POST /api/providers/{이름}/check     설정한 분석기, 연결 확인
  POST /api/analyzer/upload                서식 그림 올리기 (이미지·PDF 첫 쪽) → {upload}
  GET  /api/analyzer · GET /api/analyzer/{작업}               작업 목록·상세 (지시문, 결과 파일, 검사, 의견)
  POST /api/analyzer                       작업 시작 {kind: html|layout, provider, source: {upload}|{batch, pages}|{form}, target, real_data, public, comment}
  GET  /api/analyzer/{작업}/file?path=     작업 폴더의 파일 (입력 그림, 검사 그림)
  POST /api/analyzer/{작업}/comment · /redo · /approve · /recheck
"""
import json
import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

from . import analyzers as AZ


def make_router(reg, jobs, guard, cfg: dict, previewer, preview_url) -> APIRouter:
    r = APIRouter()
    ws = reg.ws

    def html_form(doc_id: str):
        from docgen import htmlform as H
        from docgen.registry import load_all

        spec = load_all().get(doc_id)
        if spec is None:
            raise HTTPException(404, f"알 수 없는 서식: {doc_id}")
        if not spec.template.startswith(H.PREFIX) or H.form_dir(doc_id) is None:
            raise HTTPException(400, "html 편집기는 화면에서 만든 html 서식(복제·분석기)만 씁니다. 코드 서식은 먼저 복제하세요")
        return H, spec

    @r.get("/api/forms/{doc_id}/html")
    def get_html(doc_id: str):
        H, spec = html_form(doc_id)
        d = H.form_dir(doc_id)
        return {"template": H.template_source(doc_id), "form": H.load_form(doc_id), "origin": spec.origin, "dir": str(d),
                "private": d.parent != H.COPIES, "has_source": (d / "source.png").exists()}

    class HtmlReq(BaseModel):
        template: str | None = None
        form: dict | None = None
        seed: int = 0
        rows: str = "auto"
        condition: str = "clean"

    def check_input(H, req: HtmlReq) -> None:
        from docgen.registry import GROUPS
        from docgen.render import env
        from jinja2 import TemplateSyntaxError

        if req.template is not None:
            try:
                env().parse(req.template)
            except TemplateSyntaxError as e:
                raise HTTPException(400, f"템플릿 문법 오류 ({e.lineno}행): {e.message}")
        if req.form is not None:
            f = req.form
            if not isinstance(f.get("fields", {}), dict) or not isinstance(f.get("lists", {}), dict):
                raise HTTPException(400, "form.json 의 fields·lists 는 객체여야 합니다")
            if f.get("group") and f["group"] not in GROUPS:
                raise HTTPException(400, f"group 은 {list(GROUPS)} 중 하나")
            for name, L in (f.get("lists") or {}).items():
                if int(L.get("min", 1)) > int(L.get("max", L.get("min", 1))):
                    raise HTTPException(400, f"lists.{name}: min 이 max 보다 큽니다")

    @r.put("/api/forms/{doc_id}/html")
    def put_html(doc_id: str, req: HtmlReq):
        H, _ = html_form(doc_id)
        check_input(H, req)
        guard(H.save, doc_id, req.template, req.form)
        return {"saved": True}

    @r.post("/api/forms/{doc_id}/html/render")
    def render_html(doc_id: str, req: HtmlReq):
        H, _ = html_form(doc_id)
        check_input(H, req)
        draft = {k: v for k, v in (("template", req.template), ("form", req.form)) if v is not None} or None
        try:
            label = previewer.render(doc_id, req.seed, condition=req.condition, draft=draft, rows=req.rows)
        except ValueError as e:
            raise HTTPException(400, str(e))
        except Exception as e:  # noqa: BLE001  템플릿 실행 오류도 화면에 그대로
            raise HTTPException(400, f"렌더링 오류: {type(e).__name__}: {e}")
        return {**label, "image_urls": [preview_url(p) for p in label["images"]]}

    @r.get("/api/forms/{doc_id}/source-image")
    def source_image(doc_id: str):
        H, _ = html_form(doc_id)
        f = H.form_dir(doc_id) / "source.png"
        if not f.exists():
            raise HTTPException(404, "원본 그림이 없습니다")
        return FileResponse(f)

    class CloneReq(BaseModel):
        new_id: str
        name: str = ""
        private: bool = False

    @r.post("/api/forms/{doc_id}/clone")
    def clone(doc_id: str, req: CloneReq):
        from docgen import htmlform as H

        d = guard(H.clone, doc_id, req.new_id, req.name, req.private)
        return {"id": req.new_id, "dir": str(d)}

    class RedoReq(BaseModel):
        provider: str
        comment: str = ""
        template: str | None = None
        form: dict | None = None

    @r.post("/api/forms/{doc_id}/html/redo")
    def redo_html(doc_id: str, req: RedoReq):
        H, spec = html_form(doc_id)
        d = H.form_dir(doc_id)
        if not (d / "source.png").exists():
            raise HTTPException(400, "원본 그림이 없는 서식은 분석기에 맡길 수 없습니다 (복제한 코드 서식 등)")
        form = req.form if req.form is not None else H.load_form(doc_id)
        prev = {"template.html.j2": req.template if req.template is not None else H.template_source(doc_id), "form.json": form}
        private = d.parent != H.COPIES
        jd = guard(AZ.create_job, ws, cfg, "html", req.provider, [str(d / "source.png")],
                   {"form_id": doc_id, "name": spec.name, "group": spec.group, "update": True},
                   {"real_data": private, "public": not private, "label": f"서식 {doc_id}"}, None, req.comment, prev)
        return start(jd)

    # -- 분석기 ------------------------------------------------------------------
    @r.get("/api/providers")
    def list_providers():
        return {"providers": AZ.providers(cfg)}

    @r.post("/api/providers/{name}/check")
    def check_provider(name: str):
        return guard(AZ.check, cfg, name)

    @r.post("/api/analyzer/upload")
    async def upload(file: UploadFile = File(...)):
        up = ws / "analyzer_uploads"
        up.mkdir(parents=True, exist_ok=True)
        uid = uuid.uuid4().hex[:12]
        raw = up / f"{uid}{Path(file.filename or 'x.png').suffix.lower()}"
        with open(raw, "wb") as out:
            shutil.copyfileobj(file.file, out)
        png = up / f"{uid}.png"
        try:
            if raw.suffix == ".pdf":
                import pymupdf

                with pymupdf.open(raw) as doc:
                    doc[0].get_pixmap(matrix=pymupdf.Matrix(200 / 72, 200 / 72), alpha=False).save(str(png))
            elif raw != png:
                from PIL import Image

                with Image.open(raw) as im:
                    im.convert("RGB").save(png)
        except Exception as e:  # noqa: BLE001
            raise HTTPException(400, f"그림으로 읽지 못했습니다: {e}")
        return {"upload": uid, "name": file.filename}

    def source_images(src: dict) -> tuple[list[str], dict]:
        """작업 입력 그림과 그 출처 (실서류 여부)."""
        if src.get("upload"):
            f = ws / "analyzer_uploads" / f"{Path(src['upload']).name}.png"
            if not f.exists():
                raise HTTPException(404, "올린 그림이 없습니다")
            return [str(f)], {"label": "올린 그림"}
        if src.get("batch"):
            from . import importer as IM

            bdir = ws / "imports" / IM._slug(src["batch"])
            batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
            rows = {x["id"]: x for x in IM._jsonl(bdir / "pages.jsonl")}
            pages = src.get("pages") or []
            missing = [p for p in pages if p not in rows]
            if not pages or missing:
                raise HTTPException(400, f"쪽을 고르세요 (없는 쪽: {missing[:3]})")
            return [rows[p].get("image") or rows[p]["source"] for p in pages], \
                {"real_data": bool(batch.get("real_data")), "public": bool(batch.get("public")), "label": f"묶음 {batch['name']}"}
        if src.get("form"):
            from docgen import realform as RF

            d = RF.image_form_dir(src["form"])
            if d is None:
                raise HTTPException(400, "가져온 이미지 서식(img_*)만 쓸 수 있습니다")
            lay = json.loads((d / "layout.json").read_text(encoding="utf-8"))
            return [str(d / f"page_{k}.png") for k in range(len(lay["pages"]))], \
                {"real_data": bool(lay.get("private")), "public": not lay.get("private"), "label": f"서식 {src['form']}", "texts": lay.get("texts")}
        raise HTTPException(400, "그림 출처를 고르세요 (upload / batch / form)")

    def start(jd: Path) -> dict:
        job = json.loads((jd / "job.json").read_text(encoding="utf-8"))
        cmd = guard(AZ.command, cfg, jd)
        title = f"분석기 {job['kind']}: {job['target'].get('name') or job['target'].get('form_id') or ''} ({job['provider']})"
        j = jobs.start("analyzer", title, cmd, lambda _j: AZ.validate(jd), {"analyzer": job["id"]}, cwd=jd, env=AZ.env(cfg))
        return {"analyzer": job["id"], "job": j["id"]}

    class JobReq(BaseModel):
        kind: str
        provider: str
        source: dict
        target: dict = {}
        real_data: bool = True
        public: bool = False
        comment: str = ""

    @r.post("/api/analyzer")
    def create(req: JobReq):
        images, meta = source_images(req.source)
        texts = meta.pop("texts", None)
        if req.source.get("upload"):   # 올린 그림은 사람이 정한 표시 그대로
            meta.update(real_data=req.real_data, public=req.public)
        target = dict(req.target)
        if req.kind == "layout":
            if not req.source.get("form"):
                raise HTTPException(400, "값 영역 초안(layout)은 가져온 이미지 서식(img_*)을 골라 맡깁니다")
            target["form_id"] = req.source["form"]
            if texts:
                target["texts"] = texts
        jd = guard(AZ.create_job, ws, cfg, req.kind, req.provider, images, target, meta, None, req.comment)
        return start(jd)

    def job_status(aid: str) -> dict | None:
        for j in jobs.list("analyzer"):
            if (j.get("info") or {}).get("analyzer") == aid:
                return j
        return None

    @r.get("/api/analyzer")
    def list_jobs():
        out = []
        for a in AZ.list_jobs(ws):
            j = job_status(a["id"])
            out.append({**a, "status": (j or {}).get("status"), "job": (j or {}).get("id")})
        return {"jobs": out, "providers": AZ.providers(cfg)}

    @r.get("/api/analyzer/{aid}")
    def get_job(aid: str):
        a = guard(AZ.get_job, ws, aid)
        j = job_status(aid)
        if j:
            j = jobs.get(j["id"])
        return {**a, "run": j}

    @r.get("/api/analyzer/{aid}/file")
    def job_file(aid: str, path: str):
        return FileResponse(guard(AZ.job_file, ws, aid, path))

    class CommentReq(BaseModel):
        text: str
        provider: str | None = None

    @r.post("/api/analyzer/{aid}/comment")
    def comment(aid: str, req: CommentReq):
        return guard(AZ.add_comment, ws, aid, req.text, cfg.get("user") or "studio")

    @r.post("/api/analyzer/{aid}/redo")
    def redo(aid: str, req: CommentReq):
        a = guard(AZ.get_job, ws, aid)
        d = ws / "analyzer" / aid
        images = [str(d / "input" / n) for n in sorted(a["inputs"]) if n == "source.png" or n.startswith("page_")]
        if req.text.strip():
            AZ.add_comment(ws, aid, req.text, cfg.get("user") or "studio")
        jd = guard(AZ.create_job, ws, cfg, a["kind"], req.provider or a["provider"], images, a["target"], a["source"], aid)
        return start(jd)

    @r.post("/api/analyzer/{aid}/recheck")
    def recheck(aid: str):
        d = ws / "analyzer" / Path(aid).name
        if not (d / "job.json").exists():
            raise HTTPException(404, aid)
        return AZ.validate(d)

    class ApproveReq(BaseModel):
        form_id: str | None = None
        name: str | None = None

    @r.post("/api/analyzer/{aid}/approve")
    def approve(aid: str, req: ApproveReq):
        return guard(AZ.approve, ws, aid, cfg.get("user") or "studio", req.form_id, req.name, cfg.get("private_forms_dir"))

    return r
