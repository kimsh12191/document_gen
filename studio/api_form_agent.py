"""이미지로 서식 만들기 탭: formagent 진행기(ReLab + 스킬 form-from-image)를 작업으로 띄우고 초안 폴더를 보여 준다.

실제 일은 명령줄과 같은 명령이 한다 (studio 없이도 같은 결과):
  시작        화면에서 ID·이미지를 검사하고 초안을 만든 뒤(formagent.runner.start)  python -m formagent go --id <ID>
  이어서      python -m formagent continue --id <ID> --message <지시>
  멈추기      초안 폴더에 STOP 표시 + relab 끝내기 → 진행기가 "멈춤"으로 정리하고 끝남
ReLab 이 없으면 go 가 묶음(formagent/relab)으로 설치한다 (상태 "installing").
한 번에 한 건만 돈다 (같은 저장소에서 미리보기·검사가 겹치지 않게).

API
  GET  /api/form-agent                     ReLab 상태 · 모델 설정 · 도는 작업 · 초안 목록
  GET  /api/form-agent/check-id?id=        쓸 수 있는 서식 ID 인지
  POST /api/form-agent                     새로 만들기 (multipart: images[] 쪽 순서, id, kind, note)
  GET  /api/form-agent/{id}                상세: run.json · report.json · 회차별 검사·그림 · 파일 내용
  GET  /api/form-agent/{id}/log/{n}        n회차 ReLab 출력 · GET /api/form-agent/{id}/job-log 진행기 출력
  GET  /api/form-agent/{id}/file/{path}    초안 폴더의 파일 (그림 등)
  POST /api/form-agent/{id}/continue       {message} 이어서 지시 (질문에 대한 답도)
  POST /api/form-agent/{id}/stop           멈추기
  POST /api/form-agent/{id}/register       {to: public|private} 등록 (스킬 register.py: 검사 통과·ID 비어 있음 확인 → 옮기기 → 카드·formdir check)
                                           → 서식 다시 읽기. 실서류는 비공개 폴더만
"""
from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel

from formagent import relab as R
from formagent import runner

from .jobs import Conflict, python

KIND = "form_agent"
TEXT_FILES = ("source_text.md", "fields.md", "template.html.j2", "form.json", "generate.py", "review.md", "report.md")
MAX_TEXT = 300_000


class ContinueReq(BaseModel):
    message: str


class RegisterReq(BaseModel):
    to: str


def _alive(pid) -> bool:
    if not pid:
        return False
    try:
        os.kill(int(pid), 0)
        return True
    except (OSError, ValueError):
        return False


def _status(st: dict) -> str:
    """run.json 의 상태. 돌고 있다는데 진행기 프로세스가 없으면 끊김."""
    s = st.get("status", "ready")
    if s in ("running", "installing") and not _alive(st.get("runner_pid")):
        return "interrupted"
    return s


def _url(form_id: str, path: Path) -> str:
    rel = path.resolve().relative_to(runner.draft_dir(form_id).resolve()).as_posix()
    return f"/api/form-agent/{form_id}/file/{rel}"


def _images(form_id: str, check: dict | None) -> dict:
    imgs = (check or {}).get("images") or {}
    d = runner.draft_dir(form_id).resolve()
    keep = lambda p: p and Path(p).exists() and Path(p).resolve().is_relative_to(d)  # noqa: E731
    return {"side": [_url(form_id, Path(p)) for p in imgs.get("side") or [] if keep(p)],
            "renders": _url(form_id, Path(imgs["renders"])) if keep(imgs.get("renders")) else None}


def _read_json(f: Path) -> dict | None:
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def summary(st: dict) -> dict:
    form_id = st["id"]
    d = runner.draft_dir(form_id)
    form = _read_json(d / "form.json") or {}
    last = next((r.get("check_full") for r in reversed(st.get("rounds") or []) if r.get("check_full")), None)
    return {"id": form_id, "name": form.get("name"), "kind": st.get("kind"), "status": _status(st),
            "rounds": len(st.get("rounds") or []), "created": st.get("created"), "ended": st.get("ended"),
            "passed": (last or {}).get("passed"), "problems": len((last or {}).get("problems") or []),
            "warnings": len((last or {}).get("warnings") or []), "outside": len(st.get("outside_changes") or []),
            "registered": (st.get("registered") or {}).get("to"),
            "thumb": _url(form_id, d / "source.png"),
            "side": (_images(form_id, last)["side"] or [None])[0]}


def make_router(jobs, guard, cfg: dict, refresh=None) -> APIRouter:
    r = APIRouter()
    agent_cfg = dict(cfg.get("form_agent") or {})

    def settings() -> dict:
        s = {k: agent_cfg.get(k) for k in ("relab", "provider", "endpoint", "model", "max_fix_rounds", "round_minutes")}
        return {k: v for k, v in s.items() if v not in (None, "")}

    def running_job() -> dict | None:
        return next((j for j in jobs.list(KIND) if j.get("status") == "running"), None)

    def launch(form_id: str, title: str, cmd: list[str]) -> dict:
        if running_job():
            raise Conflict("다른 서식을 만드는 중입니다. 끝나거나 멈춘 뒤에 시작하세요 (한 번에 한 건)")
        return jobs.start(KIND, title, cmd, info={"form_id": form_id})

    @r.get("/api/form-agent")
    def overview():
        items = []
        if runner.DRAFTS.is_dir():
            for f in sorted(runner.DRAFTS.glob("*/run.json"), key=lambda p: p.stat().st_mtime, reverse=True):
                st = _read_json(f)
                if st and st.get("id"):
                    items.append(summary(st))
        return {"relab": R.status(agent_cfg.get("relab")), "settings": settings(), "busy": running_job(),
                "kinds": runner.KINDS, "max_pages": runner.MAX_PAGES, "items": items}

    @r.get("/api/form-agent/check-id")
    def check_id(id: str):  # noqa: A002
        try:
            runner.check_id(id)
            return {"ok": True}
        except runner.AgentError as e:
            return {"ok": False, "reason": str(e)}

    @r.post("/api/form-agent")
    def create(images: list[UploadFile] = File(...), id: str = Form(...), kind: str = Form(...),  # noqa: A002
               note: str = Form("")):
        if running_job():
            raise HTTPException(409, "다른 서식을 만드는 중입니다. 끝나거나 멈춘 뒤에 시작하세요 (한 번에 한 건)")
        tmp = Path(tempfile.mkdtemp(prefix="form_agent_"))
        try:
            paths = []
            for i, up in enumerate(images):
                p = tmp / f"{i}{Path(up.filename or 'x.png').suffix.lower() or '.png'}"
                with open(p, "wb") as out:
                    shutil.copyfileobj(up.file, out)
                paths.append(str(p))
            try:
                runner.start(paths, id, kind, note.strip() or None, settings())
            except runner.AgentError as e:
                raise HTTPException(400, str(e))
            except OSError as e:
                raise HTTPException(400, f"그림을 읽지 못했습니다: {e}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        job = guard(launch, id, f"서식 만들기 {id}", [python(), "-m", "formagent", "go", "--id", id])
        return {"id": id, "job": job["id"]}

    @r.get("/api/form-agent/{form_id}")
    def detail(form_id: str):
        try:
            st = runner.load(form_id)
        except runner.AgentError as e:
            raise HTTPException(404, str(e))
        d = runner.draft_dir(form_id)
        rounds = []
        for rnd in st.get("rounds") or []:
            check = rnd.get("check_full")
            rounds.append({k: rnd.get(k) for k in ("n", "kind", "read", "started", "ended", "seconds", "exit", "request")}
                          | {"check": {k: (check or {}).get(k) for k in ("passed", "problems", "warnings")} if check else None,
                             "images": _images(form_id, check)})
        report = _read_json(d / "report.json")
        final = (report or {}).get("final_check")
        files = {}
        for name in TEXT_FILES:
            f = d / name
            if f.exists():
                files[name] = f.read_text(encoding="utf-8", errors="replace")[:MAX_TEXT]
        job = next((j for j in jobs.list(KIND) if (j.get("info") or {}).get("form_id") == form_id), None)
        return {**summary(st), "note": st.get("note"), "error": st.get("error"), "question": st.get("question"),
                "sources": [_url(form_id, d / s) for s in st.get("sources") or []], "rounds": rounds,
                "final": {k: (final or {}).get(k) for k in ("passed", "problems", "warnings", "renders")} if final else None,
                "final_images": _images(form_id, final) if final else None,
                "outside_changes": st.get("outside_changes") or [], "files": files,
                "relab": st.get("relab"), "relab_version": st.get("relab_version"), "settings": st.get("settings"),
                "registered": st.get("registered"), "private_dir": os.environ.get("DOCGEN_PRIVATE_FORMS"),
                "job": job and {k: job.get(k) for k in ("id", "status", "started", "ended", "cmd")}}

    @r.get("/api/form-agent/{form_id}/log/{n}")
    def round_log(form_id: str, n: int):
        f = runner.draft_dir(form_id) / f"relab_{n}.log"
        if not f.exists():
            raise HTTPException(404, f"{n}회차 로그가 없습니다")
        return PlainTextResponse(f.read_text(encoding="utf-8", errors="replace")[-200_000:])

    @r.get("/api/form-agent/{form_id}/job-log")
    def job_log(form_id: str):
        job = next((j for j in jobs.list(KIND) if (j.get("info") or {}).get("form_id") == form_id), None)
        if not job:
            return PlainTextResponse("")
        return PlainTextResponse(guard(jobs.get, job["id"]).get("log_tail", ""))

    @r.get("/api/form-agent/{form_id}/file/{path:path}")
    def file(form_id: str, path: str):
        d = runner.draft_dir(form_id).resolve()
        f = (d / path).resolve()
        if not f.is_relative_to(d) or not f.is_file():
            raise HTTPException(404, "없는 파일")
        return FileResponse(f)

    @r.post("/api/form-agent/{form_id}/continue")
    def cont(form_id: str, req: ContinueReq):
        if not req.message.strip():
            raise HTTPException(400, "지시를 적어 주세요")
        try:
            st = runner.load(form_id)
        except runner.AgentError as e:
            raise HTTPException(404, str(e))
        if _status(st) in ("running", "installing"):
            raise HTTPException(409, "아직 돌고 있습니다")
        job = guard(launch, form_id, f"서식 만들기 {form_id} (이어서)",
                    [python(), "-m", "formagent", "continue", "--id", form_id, "--message", req.message.strip()])
        return {"id": form_id, "job": job["id"]}

    @r.post("/api/form-agent/{form_id}/register")
    def register(form_id: str, req: RegisterReq):
        if running_job():
            raise HTTPException(409, "도는 작업이 있습니다. 끝난 뒤에 등록하세요")
        try:
            out = runner.register(form_id, req.to, log=lambda *a: None)
        except runner.AgentError as e:
            raise HTTPException(400, str(e))
        if refresh:
            refresh()                                   # 서식 다시 읽기 (서식 목록에 나오게)
        return {k: out[k] for k in ("id", "to", "path", "files", "card", "formdir_check", "warnings")}

    @r.delete("/api/form-agent/{form_id}")
    def delete(form_id: str):
        """초안 폴더를 지운다. 등록한 서식은 남는다. 이 서식의 작업이 돌고 있으면 거절."""
        job = running_job()
        if job and (job.get("info") or {}).get("form_id") == form_id:
            raise HTTPException(409, "이 서식을 만드는 작업이 돌고 있습니다. 멈춘 뒤에 지우세요")
        try:
            return runner.delete(form_id)
        except runner.AgentError as e:
            raise HTTPException(404 if "작업이 없습니다" in str(e) else 409, str(e))

    @r.post("/api/form-agent/{form_id}/stop")
    def stop(form_id: str):
        """STOP 표시를 남기고 relab 을 끝낸다. 진행기(작업)가 이를 보고 "멈춤"으로 정리하고 끝난다."""
        try:
            runner.stop(form_id)
        except runner.AgentError as e:
            raise HTTPException(404, str(e))
        return {"id": form_id, "stopped": True}

    return r
