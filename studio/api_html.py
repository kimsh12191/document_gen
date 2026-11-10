"""① 서식 › html 편집 · 복제 API (DESIGN.md 4.3).

html 서식 (화면에서 만든 것: docgen/htmlform.py)
  GET  /api/forms/{id}/html               템플릿·form.json·출처·원본 그림 여부
  PUT  /api/forms/{id}/html               저장 {template, form} (문법·형식 검사 뒤)
  POST /api/forms/{id}/html/render        저장 전 미리보기 {template?, form?, seed, rows: auto|min|max, condition} → 라벨 + 검사
  POST /api/forms/{id}/clone              복제 {new_id, name, private}
"""
import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


def make_router(reg, jobs, guard, cfg: dict, previewer, preview_url) -> APIRouter:
    r = APIRouter()
    ws = reg.ws

    @r.get("/api/forms/{doc_id}/templates")
    def templates(doc_id: str):
        from docgen import template_variants as T
        return guard(T.load,doc_id)

    @r.put("/api/forms/{doc_id}/templates")
    def save_templates(doc_id: str, req: dict):
        from docgen import template_variants as T
        return guard(T.save,doc_id,req)

    @r.post("/api/forms/{doc_id}/templates")
    def add_template(doc_id: str, req: dict):
        from docgen import template_variants as T
        return guard(T.add,doc_id,req.get("id"),req.get("name"),req.get("base","default"))

    @r.get("/api/forms/{doc_id}/templates/{variant}")
    def template_source(doc_id: str, variant: str):
        from docgen import template_variants as T
        return {"template":guard(T.source,doc_id,variant),"editable":variant!="default"}

    @r.put("/api/forms/{doc_id}/templates/{variant}")
    def save_template_source(doc_id: str, variant: str, req: dict):
        from docgen import template_variants as T
        from docgen.render import env
        from jinja2 import TemplateSyntaxError

        guard(T.source,doc_id,variant)
        if variant=="default":raise HTTPException(400,"기본 레이아웃은 보존합니다. 변형을 추가한 뒤 편집하세요")
        text=req.get("template")
        if not isinstance(text,str):raise HTTPException(400,"HTML 템플릿을 지정하세요")
        try:env().parse(text)
        except TemplateSyntaxError as e:raise HTTPException(400,f"템플릿 문법 오류 ({e.lineno}행): {e.message}")
        (T.folder(doc_id)/(variant+".html.j2")).write_text(text,encoding="utf-8")
        return {"saved":True}

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
        from docgen import formdir

        H, spec = html_form(doc_id)
        d = H.form_dir(doc_id)
        return {"template": H.template_source(doc_id), "form": H.load_form(doc_id), "origin": spec.origin, "dir": str(d),
                "private": formdir.is_private(d), "has_source": (d / "source.png").exists()}

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

    class CloneReq(BaseModel):
        new_id: str
        name: str = ""
        private: bool = False

    @r.post("/api/forms/{doc_id}/clone")
    def clone(doc_id: str, req: CloneReq):
        from docgen import htmlform as H

        d = guard(H.clone, doc_id, req.new_id, req.name, req.private)
        return {"id": req.new_id, "dir": str(d)}

    return r
