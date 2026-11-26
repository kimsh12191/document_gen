"""이미지로 서식 만들기 탭 API (studio/api_form_agent.py). 작업은 띄우지 않고 띄우려는 명령을 본다."""
import io
import json

import pytest
from PIL import Image

pytest.importorskip("fastapi")
from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from formagent import runner  # noqa: E402
from studio import api_form_agent  # noqa: E402
from studio.app import guard  # noqa: E402


class FakeJobs:
    def __init__(self):
        self.started, self.running = [], False

    def list(self, kind=None):
        return [{"id": "j1", "kind": "form_agent", "status": "running", "title": "서식 만들기 x", "info": {"form_id": "x"}}] if self.running else []

    def start(self, kind, title, cmd, info=None, **kw):
        self.started.append({"kind": kind, "title": title, "cmd": cmd, "info": info})
        return {"id": f"j{len(self.started)}", **self.started[-1]}

    def get(self, job_id):
        return {"log_tail": "ReLab 0.3.46 설치: …"}


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(runner, "DRAFTS", tmp_path / "out" / "form_drafts")
    monkeypatch.setattr(runner, "check_id", lambda i: None if i != "taken_id" else (_ for _ in ()).throw(runner.AgentError("이미 있는 서식 ID 입니다")))
    jobs = FakeJobs()
    app = FastAPI()
    app.include_router(api_form_agent.make_router(jobs, guard, {"form_agent": {"provider": "vllm", "model": "m", "endpoint": "http://h:1/v1"}}))
    return TestClient(app), jobs, tmp_path


def png():
    b = io.BytesIO()
    Image.new("RGB", (600, 850), "white").save(b, "PNG")
    return b.getvalue()


def test_overview_and_check_id(env):
    c, jobs, _ = env
    ov = c.get("/api/form-agent").json()
    assert ov["items"] == [] and ov["settings"]["model"] == "m" and "installed" in ov["relab"] and ov["busy"] is None
    assert c.get("/api/form-agent/check-id", params={"id": "good_id"}).json() == {"ok": True}
    assert c.get("/api/form-agent/check-id", params={"id": "taken_id"}).json()["ok"] is False


def test_create_starts_go_job_and_detail(env):
    c, jobs, root = env
    r = c.post("/api/form-agent", data={"id": "loan_app", "kind": "blank", "note": "현금 행은 비워"},
               files=[("images", ("a.png", png(), "image/png")), ("images", ("b.png", png(), "image/png"))])
    assert r.status_code == 200, r.text
    d = root / "out/form_drafts/loan_app"
    assert (d / "source.png").exists() and (d / "source_2.png").exists()
    st = json.loads((d / "run.json").read_text())
    assert st["settings"] == {"provider": "vllm", "endpoint": "http://h:1/v1", "model": "m"} and st["note"] == "현금 행은 비워"
    cmd = jobs.started[0]["cmd"]
    assert cmd[1:] == ["-m", "formagent", "go", "--id", "loan_app"] and jobs.started[0]["info"] == {"form_id": "loan_app"}
    one = c.get("/api/form-agent/loan_app").json()
    assert one["status"] == "ready"                  # 진행기(go)가 돌기 전
    assert one["sources"][1].endswith("/file/source_2.png")
    assert c.get(one["sources"][0]).status_code == 200
    assert c.get("/api/form-agent/loan_app/file/../../../etc/passwd").status_code == 404
    items = c.get("/api/form-agent").json()["items"]
    assert [i["id"] for i in items] == ["loan_app"]


def test_create_refuses_bad_input_and_second_run(env):
    c, jobs, _ = env
    bad = c.post("/api/form-agent", data={"id": "x_one", "kind": "nope"}, files=[("images", ("a.png", png(), "image/png"))])
    assert bad.status_code == 400 and "원본 종류" in bad.json()["detail"]
    jobs.running = True
    busy = c.post("/api/form-agent", data={"id": "x_two", "kind": "blank"}, files=[("images", ("a.png", png(), "image/png"))])
    assert busy.status_code == 409


def test_continue_and_stop(env):
    c, jobs, root = env
    c.post("/api/form-agent", data={"id": "f_one", "kind": "sample"}, files=[("images", ("a.png", png(), "image/png"))])
    st = runner.load("f_one")
    st["status"] = "waiting"
    st["question"] = "같은 사람인가요?"
    runner.save(st)
    assert c.post("/api/form-agent/f_one/continue", json={"message": " "}).status_code == 400
    r = c.post("/api/form-agent/f_one/continue", json={"message": "네 같은 사람"})
    assert r.status_code == 200 and jobs.started[-1]["cmd"][-5:] == ["continue", "--id", "f_one", "--message", "네 같은 사람"]
    assert c.get("/api/form-agent/f_one").json()["question"] == "같은 사람인가요?"
    assert c.post("/api/form-agent/f_one/stop").json()["stopped"] is True
    assert (root / "out/form_drafts/f_one/STOP").exists()
    assert c.get("/api/form-agent/nobody").status_code == 404


def test_register_calls_runner_and_refreshes(env, monkeypatch):
    c, jobs, _ = env
    seen = {}
    monkeypatch.setattr(runner, "register", lambda form_id, to, log=None: seen.update(id=form_id, to=to) or
                        {"id": form_id, "to": to, "path": "/p", "files": [], "card": {"ok": True}, "formdir_check": {"ok": True, "out": "ok"}, "warnings": []})
    refreshed = []
    app = FastAPI()
    app.include_router(api_form_agent.make_router(jobs, guard, {}, refresh=lambda: refreshed.append(1)))
    r = TestClient(app).post("/api/form-agent/f_one/register", json={"to": "public"})
    assert r.status_code == 200 and seen == {"id": "f_one", "to": "public"} and refreshed == [1]
    monkeypatch.setattr(runner, "register", lambda *a, **k: (_ for _ in ()).throw(runner.AgentError("검사를 통과하지 못해")))
    assert TestClient(app).post("/api/form-agent/f_one/register", json={"to": "public"}).status_code == 400
