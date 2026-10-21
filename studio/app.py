"""studio 웹 서버 (FastAPI). 화면은 studio/static/ 의 HTML·JS 한 벌이다.

여기에는 ① 서식·② 표시 요소·③ 시나리오 예시 실행 API 를 두고, 나머지 메뉴는 api_*.py 의 라우터를 붙인다.

API
  GET  /api/info                      설정 요약, 브라우저 경로
  GET  /api/groups                    서식 그룹
  GET  /api/forms                     서식 목록
  GET  /api/forms/{id}                서식 상세 (키 목록, 파일, 시나리오, 검수·배정·문제 표시)
  POST /api/forms/{id}/render         미리보기 {seed, heavy, special, condition, force, draft?, extra?} → 라벨 + 이미지 주소
  POST /api/forms/{id}/questions      ① 문항 Q/A: 그 미리보기로 실제 생성기(Builder.single)가 만드는 문항 (studio/questions.py)
  GET  /api/question-formats          과제별 공통 질문·answer 형식 (docgen.bench.contracts)
  POST /api/scenarios/run             ③ 처리 설정 예시 실행 {scenario, seed} (studio/scenario_processing.py)
  GET  /api/forms/{id}/layout        overlay 영역 편집기: 영역(자동/수정/추가/뺌), 사람 수정, 깨진 수정
  PUT  /api/forms/{id}/overrides      사람 수정 저장 {overrides}
  GET  /api/forms/{id}/bg/{page}      지우기 전 배경 그림
  GET  /api/forms/{id}/checks         검수 전 자동 검사 (경고)
  POST /api/forms/{id}/review         검수 완료 {done}
  POST /api/forms/{id}/meta           학습/평가 배정·메모 {split, note}
  POST /api/forms/{id}/issues         문제 표시 추가 · PATCH /api/forms/{id}/issues/{iid} 상태·메모·삭제
  GET  /api/keys                      표준 키 사전 (docgen/keys.json)
  GET  /api/sources                   값 출처 목록 (프로필 경로와 예시, 규칙)
  GET  /api/marks                     표시 요소 설정·풀 · PUT /api/marks/settings · PUT /api/marks/pools/{풀}
  POST /api/marks/pools/{풀}/upload   풀 이미지 올리기 · POST /api/marks/pools/{풀}/font 글꼴 · POST /api/marks/seal-template
                                      · DELETE /api/marks/pools/{풀}/{id}
  GET  /preview/...                   미리보기 이미지 · /marks-img/... 풀 이미지 · /fonts/... 손글씨 글꼴
  (⑥⑦ 등록부·채점: api_datasets.py, ③⑥⑧ 레시피·빌드·작업·업무 묶음·학습 설정: api_bank.py,
   키 사전: api_keys.py·api_dictionary.py, ④ 서류 넣기: api_intake.py, ④⑤ 이미지 묶음·OCR 검수: api_import.py, ④ 라벨 있는 데이터: api_labels.py, ④ 결과 폴더·⑤ 라벨 검수: api_review.py,
   ① html 편집·복제·⑧ 분석기: api_html.py)
"""
from __future__ import annotations

import json
import os
from contextlib import asynccontextmanager
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from docgen import marks as M
from docgen.preview import CONDITIONS, MODES, Previewer

from . import api_bank, api_datasets, api_dictionary, api_html, api_import, api_intake, api_keys, api_labels, api_review, catalog, editor, marks_admin
from . import datasets as DS
from .jobs import Jobs
from .config import ROOT, load, resolve_path, setup_browser

STATIC = Path(__file__).resolve().parent / "static"
CFG = load()
BROWSER = setup_browser(CFG)
CACHE = resolve_path(CFG["cache_dir"])
PREVIEW_DIR = CACHE / "preview"
PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
previewer = Previewer(PREVIEW_DIR)
USER = CFG.get("user") or os.environ.get("USERNAME") or os.environ.get("USER") or "studio"
CFG["user"] = USER
if CFG.get("private_forms_dir"):   # 실서류에서 만든 서식 (docgen.realform 이 등록하고, studio 가 돌리는 작업도 물려받는다)
    os.environ["DOCGEN_PRIVATE_FORMS"] = str(resolve_path(CFG["private_forms_dir"]))
M.POOLS_DIR.mkdir(parents=True, exist_ok=True)


def guard(fn, *args, **kw):
    """모듈 함수의 오류를 HTTP 오류로: 모르는 것 404, 잘못된 입력 400, 그 밖 500 (화면에 그대로 보인다)."""
    try:
        return fn(*args, **kw)
    except HTTPException:
        raise
    except KeyError as e:
        raise HTTPException(404, f"찾을 수 없음: {e}")
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:  # noqa: BLE001
        raise HTTPException(500, f"{type(e).__name__}: {e}")


@asynccontextmanager
async def lifespan(_app):
    yield
    previewer.close()


app = FastAPI(title="docgen studio", lifespan=lifespan)
app.mount("/preview", StaticFiles(directory=PREVIEW_DIR), name="preview")
app.mount("/static", StaticFiles(directory=STATIC), name="static")
app.mount("/marks-img", StaticFiles(directory=M.POOLS_DIR), name="marks-img")
REGISTRY = DS.Registry(resolve_path(CFG["workspace_dir"]), CFG.get("path_map") or {})
JOBS = Jobs(REGISTRY.ws, ROOT)
app.include_router(api_datasets.make_router(REGISTRY, guard, JOBS))
app.include_router(api_bank.make_router(REGISTRY, JOBS, guard))
# 실서류 검수 결과 (OCR 검수본 등). 설정이 없으면 작업 공간 안에 두고 화면에 경고한다
REAL_ROOT = resolve_path(CFG.get("real_data_dir")) or REGISTRY.ws / "real_data"
app.include_router(api_import.make_router(REGISTRY, JOBS, guard, CFG, REAL_ROOT / "ocr_reviewed"))
app.include_router(api_labels.make_router(REGISTRY, JOBS, guard, CFG))
app.include_router(api_html.make_router(REGISTRY, JOBS, guard, CFG, previewer, lambda p: f"/preview/{p}"))   # html 편집·복제·분석기
app.include_router(api_review.make_router(REGISTRY, JOBS, guard, CFG, REAL_ROOT))   # 결과 폴더 검사, 라벨 검수
app.include_router(api_intake.make_router(REGISTRY, JOBS, guard, CFG, REAL_ROOT))   # ④ 서류 넣기
app.include_router(api_keys.make_router(guard))   # 키 사전 (키 규칙·값 종류)
app.include_router(api_dictionary.make_router(guard))   # 키 사전 (당사자 계층·문서 분류·업무·합치기)
app.mount("/fonts", StaticFiles(directory=ROOT / "docgen" / "fonts"), name="fonts")   # 손글씨 글꼴 (화면의 글꼴 미리보기)


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/info")
def info():
    return {
        "config_file": CFG["config_file"], "browser": BROWSER, "cache_dir": str(CACHE),
        "paths": {k: CFG[k] for k in ("workspace_dir", "import_dir", "real_data_dir", "private_forms_dir")},
        "ocr": CFG["ocr"], "providers": sorted(CFG["providers"]),
        "conditions": CONDITIONS, "modes": MODES, "user": USER,
    }


@app.get("/api/groups")
def groups():
    return catalog.groups()


@app.get("/api/forms")
def forms():
    return catalog.list_forms()


def host_path(p: str | Path) -> str | None:
    """컨테이너 안 경로 → 서버(도커 호스트)에서 보이는 경로. docker/studio.sh 가 DOCGEN_HOST_CODE·DOCGEN_HOST_DATA 로 넘긴다"""
    p = Path(p).as_posix()
    for inside, env in ((ROOT.as_posix(), "DOCGEN_HOST_CODE"), ("/out", "DOCGEN_HOST_DATA")):
        host = os.environ.get(env)
        if host and (p == inside or p.startswith(inside + "/")):
            return host.rstrip("/") + p[len(inside):]
    return None


@app.get("/api/paths")
def paths():
    """데이터셋이 어디에 생기는지: 컨테이너 안 경로와 서버 경로"""
    ws = REGISTRY.ws
    return {"workspace": str(ws), "workspace_host": host_path(ws), "datasets": str(ws / "datasets"),
            "datasets_host": host_path(ws / "datasets"), "config_file": CFG["config_file"],
            "mounts": [[i, os.environ[e]] for i, e in ((ROOT.as_posix(), "DOCGEN_HOST_CODE"), ("/out", "DOCGEN_HOST_DATA"))
                       if os.environ.get(e)]}


@app.get("/api/form-ids")
def form_ids():
    """서식 ID·이름·그룹만 (원격 생성 docker/remote_build.py 용. /api/forms 는 서식마다 통계를 내서 느리다)"""
    from docgen.registry import load_all

    return [{"id": s.id, "name": s.name, "group": s.group} for s in load_all().values()]


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
    draft: dict | None = None     # 저장하지 않은 overlay 수정 (수정 전후 비교)
    extra: dict | None = None     # 시나리오 예시의 고객 프로필 값


@app.post("/api/forms/{doc_id}/render")
def render(doc_id: str, req: RenderReq):
    if not BROWSER:
        raise HTTPException(503, "렌더링 브라우저가 없어 미리보기를 만들 수 없습니다. Chromium 이 있는 docgen 컨테이너에서 "
                                 "studio 를 띄우거나 설정의 browser 를 지정하세요. 렌더링이 필요 없는 화면은 그대로 씁니다.")
    # 일반 def 라서 FastAPI 가 스레드에서 돌린다. 실제 렌더링은 Previewer 의 전용 스레드 하나에서 차례로 한다.
    try:
        if req.draft is not None and set(req.draft) == {"html_regions"}:
            from docgen import html_regions

            html_regions.path(doc_id)
            draft = {"html_regions": html_regions.validate(req.draft["html_regions"])}
        else:
            draft = editor.validate(doc_id, req.draft) if req.draft is not None else None
        label = previewer.render(doc_id, req.seed, req.heavy, req.special, req.condition, req.force, draft, extra=req.extra)
    except KeyError as e:
        raise HTTPException(404, str(e))
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:  # noqa: BLE001  렌더링 실패는 화면에 그대로 보여 준다
        raise HTTPException(500, f"{type(e).__name__}: {e}")
    return {**label, "image_urls": [f"/preview/{p}" for p in label["images"]]}


class ScenarioRunReq(BaseModel):
    scenario: dict
    seed: int = Field(default=0, ge=0, le=2147483647)


@app.post("/api/scenarios/run")
def run_scenario(req: ScenarioRunReq):
    from .scenario_processing import run

    if not BROWSER:
        raise HTTPException(503, "렌더링 브라우저가 없어 예시 고객의 문서를 만들 수 없습니다")
    result = guard(run, req.scenario, req.seed, previewer.render)
    result["labels"] = {did: {**label, "image_urls": [f"/preview/{p}" for p in label["images"]]}
                        for did, label in result["labels"].items()}
    return result


@app.post("/api/scenarios/resolve")
def resolve_scenario(req: ScenarioRunReq):
    from docgen.roles import resolve
    return {"selections":guard(resolve,req.scenario.get("docs"),req.scenario.get("sampling"),req.seed,req.scenario.get("id") or "draft")}


@app.get("/api/question-formats")
def question_formats():
    from docgen.bench.contracts import contracts

    return contracts()


class FormQuestionsReq(RenderReq):
    seed: int = Field(default=0, ge=0, le=2147483647)
    fields_per_doc: int = Field(default=6, ge=0, le=50)
    max_keys: int = Field(default=40, ge=1, le=500)


@app.post("/api/forms/{doc_id}/questions")
def form_questions(doc_id: str, req: FormQuestionsReq):
    from .questions import form_items

    label = render(doc_id, req)
    items = guard(form_items, label, PREVIEW_DIR, req.fields_per_doc, req.max_keys)
    return {"items": items, "seed": req.seed, "doc_id": doc_id}


# ---------------------------------------------------------------------------
# 2단계: overlay 영역 편집기, 검수·배정·문제 표시, 키 사전, 값 출처, 표시 요소
# ---------------------------------------------------------------------------

@app.get("/api/forms/{doc_id}/regions")
def html_regions_get(doc_id: str, variant: str = "default"):
    from docgen import html_regions

    return guard(html_regions.load, doc_id, variant)


class RegionsReq(BaseModel):
    regions: list[dict]
    seed: int = 0
    template_variant: str = "default"


@app.put("/api/forms/{doc_id}/regions")
def html_regions_save(doc_id: str, req: RegionsReq):
    from docgen import html_regions

    value = guard(html_regions.validate, {"regions": req.regions})
    guard(html_regions.path, doc_id, req.template_variant)
    if not BROWSER:
        raise HTTPException(503, "저장 전 이미지 검사를 위해 렌더링 브라우저가 필요합니다")
    guard(previewer.render, doc_id, req.seed, draft={"html_regions": value}, extra={"template_variants":{doc_id:req.template_variant}})
    return guard(html_regions.save, doc_id, value, req.template_variant)


@app.get("/api/forms/{doc_id}/layout")
def layout(doc_id: str):
    return guard(editor.layout_view, doc_id)


class OverridesReq(BaseModel):
    overrides: dict


@app.put("/api/forms/{doc_id}/overrides")
def save_overrides(doc_id: str, req: OverridesReq):
    return guard(editor.save, doc_id, req.overrides, USER)


@app.get("/api/forms/{doc_id}/bg/{page}")
def background(doc_id: str, page: int):
    from docgen.realform import raw_background

    return Response(guard(raw_background, doc_id, page), media_type="image/png")


@app.get("/api/forms/{doc_id}/checks")
def checks(doc_id: str, seed: int = 0):
    label = guard(previewer.render, doc_id, seed) if BROWSER else None
    keys = catalog._fields().get(doc_id, {}).get("keys", [])
    return {"checks": guard(editor.checks, doc_id, label, keys), "rendered": label is not None}


class ReviewReq(BaseModel):
    done: bool = True


@app.post("/api/forms/{doc_id}/review")
def review(doc_id: str, req: ReviewReq):
    return guard(catalog.set_review, doc_id, req.done, USER)


class MetaReq(BaseModel):
    split: str | None = None
    note: str | None = None


@app.post("/api/forms/{doc_id}/meta")
def form_meta(doc_id: str, req: MetaReq):
    return guard(catalog.set_meta, doc_id, req.split, req.note)


class IssueReq(BaseModel):
    seed: int | None = None
    page: int = 0
    bbox: list[float] | None = None
    key: str | None = None
    note: str = ""
    heavy: str | None = None
    special: str | None = None
    condition: str | None = None


@app.post("/api/forms/{doc_id}/issues")
def add_issue(doc_id: str, req: IssueReq):
    return guard(catalog.add_issue, doc_id, {k: v for k, v in req.model_dump().items() if v is not None})


class IssuePatch(BaseModel):
    status: str | None = None
    note: str | None = None
    delete: bool = False


@app.patch("/api/forms/{doc_id}/issues/{issue_id}")
def patch_issue(doc_id: str, issue_id: str, req: IssuePatch):
    return guard(catalog.set_issue, doc_id, issue_id, req.status, req.note, req.delete)


@lru_cache(maxsize=2)
def _keys(mtime: float) -> dict:
    return json.loads((ROOT / "docgen" / "keys.json").read_text(encoding="utf-8"))


@app.get("/api/keys")
def keys():
    p = ROOT / "docgen" / "keys.json"
    if not p.exists():
        return {"keys": [], "duplicates": [], "synonyms": {}, "missing": True}
    return _keys(p.stat().st_mtime)


@lru_cache(maxsize=1)
def _sources() -> dict:
    from docgen import sources as SRC
    from docgen.entities import make_profile

    return {"profile": SRC.profile_paths(make_profile(0)), "rules": SRC.RULE_KINDS, "special": SRC.SPECIAL_RULES}


@app.get("/api/sources")
def sources():
    return _sources()


@app.get("/api/marks")
def marks_view():
    return marks_admin.view()


@app.put("/api/marks/settings")
def marks_settings(req: dict[str, Any]):
    return guard(marks_admin.save_settings, req)


@app.put("/api/marks/pools/{name}")
def marks_pool(name: str, req: list[dict[str, Any]]):
    return guard(marks_admin.save_pool, name, req)


@app.post("/api/marks/pools/{name}/upload")
async def marks_upload(name: str, file: UploadFile = File(...), label: str = Form("")):
    data = await file.read()
    return guard(marks_admin.upload, name, file.filename or "image.png", data, label)


class FontReq(BaseModel):
    id: str
    scale: float = 1.0


@app.post("/api/marks/pools/{name}/font")
def marks_font(name: str, req: FontReq):
    return guard(marks_admin.add_font, name, req.id, req.scale)


@app.post("/api/marks/seal-template")
def marks_seal(req: dict[str, Any]):
    return guard(marks_admin.add_seal_template, req)


@app.delete("/api/marks/pools/{name}/{item_id}")
def marks_delete(name: str, item_id: str):
    return guard(marks_admin.delete_item, name, item_id)
