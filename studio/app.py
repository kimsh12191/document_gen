"""studio 웹 서버 (FastAPI). 화면은 studio/static/ 의 HTML·JS 한 벌이다.

API (1단계)
  GET  /api/info                      설정 요약, 브라우저 경로
  GET  /api/groups                    서식 그룹
  GET  /api/forms                     서식 목록
  GET  /api/forms/{id}                서식 상세 (키 목록, 파일, 시나리오)
  POST /api/forms/{id}/render         미리보기 {seed, heavy, special, condition, force} → 라벨 + 이미지 주소
  GET  /preview/...                   미리보기 이미지
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from docgen.preview import CONDITIONS, MODES, Previewer

from . import catalog
from .config import load, resolve_path, setup_browser

STATIC = Path(__file__).resolve().parent / "static"
CFG = load()
BROWSER = setup_browser(CFG)
CACHE = resolve_path(CFG["cache_dir"])
PREVIEW_DIR = CACHE / "preview"
PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
previewer = Previewer(PREVIEW_DIR)


@asynccontextmanager
async def lifespan(_app):
    yield
    previewer.close()


app = FastAPI(title="docgen studio", lifespan=lifespan)
app.mount("/preview", StaticFiles(directory=PREVIEW_DIR), name="preview")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/info")
def info():
    return {
        "config_file": CFG["config_file"], "browser": BROWSER, "cache_dir": str(CACHE),
        "paths": {k: CFG[k] for k in ("workspace_dir", "import_dir", "real_data_dir", "private_forms_dir")},
        "ocr": CFG["ocr"], "providers": sorted(CFG["providers"]),
        "conditions": CONDITIONS, "modes": MODES,
    }


@app.get("/api/groups")
def groups():
    return catalog.groups()


@app.get("/api/forms")
def forms():
    return catalog.list_forms()


@app.get("/api/forms/{doc_id}")
def form(doc_id: str):
    try:
        return catalog.form_detail(doc_id)
    except KeyError:
        raise HTTPException(404, f"알 수 없는 서식: {doc_id}")


class RenderReq(BaseModel):
    seed: int = 0
    heavy: str = "default"
    special: str = "default"
    condition: str = "clean"
    force: bool = False


@app.post("/api/forms/{doc_id}/render")
def render(doc_id: str, req: RenderReq):
    # 일반 def 라서 FastAPI 가 스레드에서 돌린다. 실제 렌더링은 Previewer 의 전용 스레드 하나에서 차례로 한다.
    try:
        label = previewer.render(doc_id, req.seed, req.heavy, req.special, req.condition, req.force)
    except KeyError as e:
        raise HTTPException(404, str(e))
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:  # noqa: BLE001  렌더링 실패는 화면에 그대로 보여 준다
        raise HTTPException(500, f"{type(e).__name__}: {e}")
    return {**label, "image_urls": [f"/preview/{p}" for p in label["images"]]}
