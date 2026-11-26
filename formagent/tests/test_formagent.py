"""formagent 진행기: 가짜 relab(tests/fake_relab.py) 과 가짜 검사로 회차·질문·이어서·멈추기·초안 밖 변경을 본다.
미리보기(브라우저)와 실제 모델은 쓰지 않는다. 실제 ReLab 으로 한 시험은 PLAN.md 13절."""
import json
import os
import stat
import threading
import time
from pathlib import Path

import pytest
from PIL import Image

from formagent import relab as R
from formagent import runner

FAKE = Path(__file__).with_name("fake_relab.py")


@pytest.fixture
def ws(tmp_path, monkeypatch):
    """작업 공간을 tmp 로: 저장소 대신 빈 폴더, 검사는 가짜."""
    root = tmp_path / "repo"
    root.mkdir()
    (root / "keep.txt").write_text("x")
    monkeypatch.setattr(runner, "ROOT", root)
    monkeypatch.setattr(runner, "DRAFTS", root / "out" / "form_drafts")
    monkeypatch.setattr(runner, "check_id", lambda form_id: None)
    checks = []

    def fake_check(draft, out):
        out = Path(out)
        out.mkdir(parents=True, exist_ok=True)
        (out / "side_0.jpg").write_bytes(b"jpg")
        (out / "renders.jpg").write_bytes(b"jpg")
        passed = (Path(draft) / "template.html.j2").exists()
        result = {"passed": passed, "problems": [] if passed else ["template.html.j2 이 없습니다"], "warnings": ["경고 하나"],
                  "images": {"side": [str(out / "side_0.jpg")], "renders": str(out / "renders.jpg")}, "renders": {}}
        checks.append(out.name)
        return result

    monkeypatch.setattr(runner, "run_check", fake_check)
    exe = tmp_path / "relab"
    exe.write_text(FAKE.read_text())
    exe.chmod(exe.stat().st_mode | stat.S_IEXEC)
    plan = tmp_path / "plan.json"
    monkeypatch.setenv("FAKE_RELAB_PLAN", str(plan))
    img = tmp_path / "form.png"
    Image.new("RGB", (1190, 1684), "white").save(img)
    return {"root": root, "relab": str(exe), "plan": plan, "img": str(img), "checks": checks,
            "requests": lambda: [json.loads(line) for line in (tmp_path / "requests.jsonl").read_text().splitlines()]}


def draft_files(form_id):
    d = f"out/form_drafts/{form_id}"
    return {f"{d}/source_text.md": "## 1쪽", f"{d}/fields.md": "# 칸", f"{d}/template.html.j2": "{% extends '_base.html.j2' %}",
            f"{d}/form.json": "{}"}


def test_start_makes_draft_with_sources_and_package_marks(ws):
    st = runner.start([ws["img"]], "my_form", "blank", "메모", {"relab": ws["relab"]})
    d = ws["root"] / "out/form_drafts/my_form"
    assert (d / "source.png").exists() and st["sources"] == ["source.png"] and st["status"] == "ready"
    for folder in (ws["root"] / "out", ws["root"] / "out/form_drafts", d):
        assert (folder / "__init__.py").exists()            # ReLab 이 저장소 전체를 프로젝트로 보게
    with pytest.raises(runner.AgentError):
        runner.start([ws["img"]], "my_form2", "nope", None, {})
    with pytest.raises(runner.AgentError):
        runner.start([ws["img"]] * 4, "my_form3", "blank", None, {})


def test_bad_ids_refused():
    for bad in ("Bad", "a", "my-form", "private_form", "x_secrets"):
        with pytest.raises(runner.AgentError):
            runner.check_id(bad)


def test_rounds_until_report(ws):
    """1회차 미완료(1) → 2회차에 report.md 를 쓰고 검사 통과 → 끝."""
    ws["plan"].write_text(json.dumps([{"write": draft_files("f1"), "exit": 1},
                                      {"write": {"out/form_drafts/f1/report.md": "## 보고"}, "exit": 0}]))
    runner.start([ws["img"]], "f1", "blank", "현금 행은 계좌 비워", {"relab": ws["relab"], "max_fix_rounds": 3})
    st = runner.go("f1", log=lambda *a: None)
    assert st["status"] == "done" and [r["exit"] for r in st["rounds"]] == [1, 0]
    reqs = ws["requests"]()
    assert reqs[0]["request"].startswith("@out/form_drafts/f1/source.png") and "1회차" in reqs[0]["request"]
    assert "현금 행은 계좌 비워" in reqs[0]["request"] and "--auto" in reqs[0]["argv"]
    assert "@out/form_drafts/f1/check_1/side_0.jpg" in reqs[1]["request"] and "2회차" in reqs[1]["request"]
    assert "경고 하나" in reqs[1]["request"] and "fields.md" in reqs[1]["request"]
    report = json.loads((ws["root"] / "out/form_drafts/f1/report.json").read_text())
    assert report["status"] == "done" and report["report_md"] and report["outside_changes"] == []


def test_three_kinds_of_rounds(ws):
    """1 글자 옮기기(그림만, 스킬 안 읽음) → 2 만들기(원본 그림 다시, source_text.md 기준) → 3 고치기(비교 그림) → 끝."""
    d = "out/form_drafts/k1"
    files = draft_files("k1")
    ws["plan"].write_text(json.dumps([{"write": {f"{d}/source_text.md": "## 1쪽\n고객번호 | ( )"}, "exit": 0},
                                      {"write": {k: v for k, v in files.items() if "source_text" not in k}, "exit": 0},
                                      {"write": {f"{d}/report.md": "## 보고"}, "exit": 0}]))
    runner.start([ws["img"]], "k1", "real", "결재란은 빼", {"relab": ws["relab"], "max_fix_rounds": 3})
    st = runner.go("k1", log=lambda *a: None)
    assert st["status"] == "done" and [r["kind"] for r in st["rounds"]] == ["read", "build", "fix"]
    r1, r2, r3 = (r["request"] for r in ws["requests"]())
    assert r1.startswith(f"@{d}/source.png") and "source_text.md" in r1 and f"{d}/source_text" not in r1 and "SKILL.md" not in r1
    assert "(값)" in r1 and "짐작" in r1
    assert r2.startswith(f"@{d}/source.png") and "source_text.md" in r2 and "SKILL.md" in r2 and "결재란은 빼" in r2
    assert f"@{d}/check_2/side_0.jpg" in r3 and "3회차" in r3


def test_round_limit(ws):
    ws["plan"].write_text(json.dumps([{"write": draft_files("f2"), "exit": 0}, {"exit": 0}, {"exit": 0}]))
    runner.start([ws["img"]], "f2", "sample", None, {"relab": ws["relab"], "max_fix_rounds": 2})
    st = runner.go("f2", log=lambda *a: None)
    assert st["status"] == "done" and len(st["rounds"]) == 4 and st.get("note_end")      # 글자 옮기기·만들기 + 고치기 2


def test_question_then_continue(ws):
    ws["plan"].write_text(json.dumps([{"write": draft_files("f3"), "exit": 3, "say": "질문: 성명 칸이 두 개인데 같은 사람인가요?"},
                                      {"write": {"out/form_drafts/f3/report.md": "## 보고"}, "exit": 0}]))
    runner.start([ws["img"]], "f3", "blank", None, {"relab": ws["relab"]})
    st = runner.go("f3", log=lambda *a: None)
    assert st["status"] == "waiting" and "같은 사람" in st["question"]
    st = runner.go("f3", message="네, 같은 사람입니다", log=lambda *a: None)
    assert st["status"] == "done" and "네, 같은 사람입니다" in ws["requests"]()[1]["request"]


def test_stop(ws):
    ws["plan"].write_text(json.dumps([{"exit": 0, "sleep": 30}]))
    runner.start([ws["img"]], "f4", "blank", None, {"relab": ws["relab"]})
    flag = ws["root"] / "out/form_drafts/f4/STOP"
    threading.Timer(1.5, lambda: flag.write_text("x")).start()
    t0 = time.time()
    st = runner.go("f4", log=lambda *a: None)
    assert st["status"] == "stopped" and time.time() - t0 < 15


def test_outside_change_reported(ws):
    ws["plan"].write_text(json.dumps([{"write": {**draft_files("f5"), "docgen/forms/zz/form.json": "{}"}, "exit": 0},
                                      {"write": {"out/form_drafts/f5/report.md": "#"}, "exit": 0}]))
    runner.start([ws["img"]], "f5", "blank", None, {"relab": ws["relab"]})
    st = runner.go("f5", log=lambda *a: None)
    assert st["outside_changes"] == ["새로 생김: docgen/forms/zz/form.json"]


def test_relab_found_or_refused(tmp_path, monkeypatch):
    exe = tmp_path / "relab"
    exe.write_text(FAKE.read_text())
    exe.chmod(exe.stat().st_mode | stat.S_IEXEC)
    assert R.find(str(exe)) == str(exe)
    with pytest.raises(R.RelabError):
        R.ensure(str(tmp_path / "없는-relab"))


def test_bundle_matches_version():
    wheels = sorted(p.name for p in (R.BUNDLE / "wheels").glob("*.whl"))
    assert f"relab-{R.VERSION}-py3-none-any.whl" in wheels
    assert any(w.startswith("pydantic_core") and "cp313" in w and "manylinux" in w for w in wheels)
    assert not any("win" in w for w in wheels)


def test_project_relab_settings():
    cfg = json.loads((Path(__file__).resolve().parents[2] / ".relab" / "config.json").read_text())
    assert cfg["defaultRules"] is False and cfg["planFirst"] is False
    assert os.environ.get("RELAB_BIN") is None or True


def _register_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location("form_register_t", Path(__file__).resolve().parents[2] / ".claude/skills/form-from-image/register.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_register_example_into_private_dir(tmp_path, monkeypatch):
    """완성 예시 초안을 임시 비공개 폴더로 등록: 파일 꼴 · 카드 · formdir check (렌더링 검사는 통과로 둔다)."""
    import shutil
    reg = _register_module()
    example = Path(__file__).resolve().parents[2] / ".claude/skills/form-from-image/example"
    draft = tmp_path / "drafts" / "zz_reg_example"
    shutil.copytree(example, draft)
    Image.new("RGB", (595, 842), "white").save(draft / "source.png")
    private = tmp_path / "private"
    monkeypatch.setenv("DOCGEN_PRIVATE_FORMS", str(private))
    monkeypatch.setattr(reg.check, "run", lambda d, out: {"passed": True, "problems": [], "warnings": []})
    with pytest.raises(reg.RegisterError):
        reg.register(draft, "public", real=True, log=lambda *a: None)          # 실서류는 공개 폴더 거부
    out = reg.register(draft, "private", log=lambda *a: None)
    dest = private / "zz_reg_example"
    assert out["path"] == str(dest) and sorted(p.name for p in dest.iterdir() if p.name != "__pycache__") == \
        ["FORM.md", "fields.json", "form.json", "generate.py", "look", "source.png"]
    body = json.loads((dest / "fields.json").read_text())
    form = json.loads((dest / "form.json").read_text())
    assert body["engine"] == "html" and "customer.name" in body["fields"] and "accounts" in body["lists"]
    assert "fields" not in form and form["origin"] == "analyzer" and form["source_image"] == "source.png"
    assert not (dest / "fields.md").exists() and out["card"]["ok"]
    assert out["formdir_check"]["ok"], out["formdir_check"]["out"]
    with pytest.raises(reg.RegisterError):
        reg.register(draft, "private", log=lambda *a: None)                    # 이미 있으면 덮어쓰지 않음


def test_runner_register_records_and_refuses_twice(ws, monkeypatch):
    ws["plan"].write_text(json.dumps([{"write": draft_files("f6"), "exit": 0}, {"write": {"out/form_drafts/f6/report.md": "#"}, "exit": 0}]))
    runner.start([ws["img"]], "f6", "real", None, {"relab": ws["relab"]})
    runner.go("f6", log=lambda *a: None)

    class Fake:
        class RegisterError(Exception):
            pass

        @staticmethod
        def register(draft, to, form_id, real=False, log=print):
            assert real is True and form_id == "f6"
            return {"path": f"/x/{form_id}", "files": ["form.json"], "card": {"ok": True}, "formdir_check": {"ok": True, "out": ""}}

    monkeypatch.setattr(runner, "_skill", lambda name: Fake)
    out = runner.register("f6", "private", log=lambda *a: None)
    assert out["path"] == "/x/f6" and runner.load("f6")["registered"]["to"] == "private"
    with pytest.raises(runner.AgentError):
        runner.register("f6", "private", log=lambda *a: None)


def test_browser_env_survives_stripped_environment(tmp_path, monkeypatch):
    """ReLab 은 검사 명령에 환경 변수를 몇 개만 넘긴다: 진행기가 남긴 파일로 check.py 가 브라우저 위치를 채운다."""
    import importlib.util
    monkeypatch.setattr(runner, "DRAFTS", tmp_path / "out" / "form_drafts")
    monkeypatch.setenv("PLAYWRIGHT_BROWSERS_PATH", "/opt/ms-playwright-test")
    runner.save_env()
    saved = json.loads((tmp_path / "out/form_drafts/.formagent_env.json").read_text())
    assert saved["PLAYWRIGHT_BROWSERS_PATH"] == "/opt/ms-playwright-test"
    spec = importlib.util.spec_from_file_location("form_check_t", Path(__file__).resolve().parents[2] / ".claude/skills/form-from-image/check.py")
    chk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(chk)
    monkeypatch.setattr(chk, "ENV_FILE", tmp_path / "out/form_drafts/.formagent_env.json")
    monkeypatch.delenv("PLAYWRIGHT_BROWSERS_PATH")                      # ReLab 이 버린 상태
    assert chk.child_env()["PLAYWRIGHT_BROWSERS_PATH"] == "/opt/ms-playwright-test"
    monkeypatch.setattr(chk, "ENV_FILE", tmp_path / "없음.json")          # 파일도 없으면 흔한 자리를 찾음
    found = tmp_path / "pw"
    (found / "chromium-1").mkdir(parents=True)
    monkeypatch.setattr(chk, "BROWSER_ROOTS", (str(found),))
    assert chk.child_env()["PLAYWRIGHT_BROWSERS_PATH"] == str(found)


def test_fix_request_shows_sample_values(ws):
    """고치기 요청에 렌더 키→값 두 벌 (반복 표는 첫 행만) — 모델이 값이 칸의 뜻에 맞는지 보게."""
    st = runner.start([ws["img"]], "sv1", "blank", None, {"relab": ws["relab"]})
    for name, text in draft_files("sv1").items():
        (ws["root"] / name).write_text(text)
    check = {"passed": True, "problems": [], "warnings": [], "images": {"side": [], "renders": None},
             "values": {"s1": {"bill.tenor": "주소 변경", "docs.0.bl": "3", "docs.1.bl": "2"}, "s2": {"bill.tenor": "본인 요청"}}}
    req = runner.round_request(runner.load("sv1"), 3, check)
    assert "bill.tenor: 주소 변경 / 본인 요청" in req and "docs.0.bl: 3" in req and "docs.1.bl" not in req and "9문항" in req
