"""서식 초안 탭 API (외주 작업: 예시 이미지 → html 서식 → 추출 키 추천). 설명은 studio/form_draft.py.

  GET  /api/form-draft                     초안 목록 + 쓸 수 있는 모델 연결 (OCR·모델 연결 화면과 같은 설정)
  POST /api/form-draft                     이미지 올리고 시작 (multipart: file, provider, name, group, comment, real_data)
  GET  /api/form-draft/catalog             키 사전 (키·뜻·타입·공통/문서별) — 키 입력 칸의 후보
  GET  /api/form-draft/{작업}              상세: 칸·키·검사 결과·실행 상태
  PUT  /api/form-draft/{작업}/keys         키 저장 {keys: [{slot, key, label, description, type}]} → 다시 그려 검사
  POST /api/form-draft/{작업}/rerun        같은 이미지로 다시 {provider?, comment}
  GET  /api/form-draft/{작업}/export       키 목록 JSON
  POST /api/form-draft/{작업}/register     서식으로 등록 {form_id, name} (분석기 승인과 같다)
그림은 /api/analyzer/{작업}/file?path=input/source.png · check/… 로 본다.
"""
import shutil
import threading
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from . import analyzers as AZ, form_draft as FD, key_suggestions as KS, real_benchmark as RB
from .jobs import python


def make_router(reg, jobs, guard, cfg: dict) -> APIRouter:
    r = APIRouter(prefix="/api/form-draft")
    ws = reg.ws
    lock = threading.Lock()
    user = lambda: cfg.get("user") or "studio"   # noqa: E731

    def conn():
        return RB.connection_config(ws, cfg)

    def providers():
        return [{"name": n, "model": p.get("model"), "base_url": p.get("base_url"), "external": bool(p.get("external", True))}
                for n, p in conn()["providers"].items() if p.get("kind") == "openai"]

    def start(d: Path) -> dict:
        job = RB.read(d / "job.json")
        j = jobs.start("analyzer", f"서식 초안: {job['target'].get('name') or job['id']} ({job['provider']})",
                       [python(), "-m", "studio.form_draft", str(d)], lambda _j: AZ.validate(d),
                       {"analyzer": job["id"], "draft": True}, env=AZ.env(cfg))
        return {"id": job["id"], "job": j["id"]}

    def run_status(aid: str) -> dict | None:
        for j in jobs.list("analyzer"):
            if (j.get("info") or {}).get("analyzer") == aid:
                return jobs.get(j["id"])
        return None

    @r.get("")
    def listing():
        rows = guard(FD.listing, ws)
        status = {(j.get("info") or {}).get("analyzer"): j["status"] for j in jobs.list("analyzer")}
        return {"drafts": [{**d, "status": status.get(d["id"])} for d in rows], "providers": providers()}

    @r.post("")
    async def create(file: UploadFile = File(...), provider: str = Form(...), name: str = Form(""), group: str = Form("finance"),
                     comment: str = Form(""), real_data: bool = Form(True)):
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
        d = guard(FD.create, ws, conn(), provider, png, name.strip(), group, comment, real_data, user())
        return start(d)

    @r.get("/catalog")
    def catalog():
        rows = guard(KS.catalog, ws)
        return {"keys": [{"key": x["key"], "meaning": x.get("meaning", ""), "type": x.get("type"), "scope": x.get("scope")} for x in rows]}

    @r.get("/{aid}")
    def detail(aid: str):
        return {**guard(FD.detail, ws, aid), "run": run_status(aid)}

    class Keys(BaseModel):
        keys: list[dict] = Field(default_factory=list)

    @r.put("/{aid}/keys")
    def save_keys(aid: str, req: Keys):
        with lock:
            return guard(FD.save_keys, ws, aid, req.keys, user())

    class Rerun(BaseModel):
        provider: str = ""
        comment: str = ""

    @r.post("/{aid}/rerun")
    def rerun(aid: str, req: Rerun):
        info = guard(FD.detail, ws, aid)
        src = ws / "analyzer" / info["id"] / "input" / "source.png"
        d = guard(FD.create, ws, conn(), req.provider or info["provider"], src, info["target"].get("name", ""),
                  info["target"].get("group", "finance"), req.comment, bool(info["source"].get("real_data")), user())
        return start(d)

    @r.get("/{aid}/export")
    def export(aid: str):
        return guard(FD.export, ws, aid)

    class Register(BaseModel):
        form_id: str
        name: str = ""

    @r.post("/{aid}/register")
    def register(aid: str, req: Register):
        guard(FD.detail, ws, aid)
        return guard(AZ.approve, ws, aid, user(), req.form_id, req.name or None, cfg.get("private_forms_dir"))

    return r
