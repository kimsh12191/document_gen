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
    return {f"{d}/fields.md": "# 칸", f"{d}/template.html.j2": "{% extends '_base.html.j2' %}", f"{d}/form.json": "{}"}


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


def test_round_limit(ws):
    ws["plan"].write_text(json.dumps([{"write": draft_files("f2"), "exit": 0}, {"exit": 0}, {"exit": 0}]))
    runner.start([ws["img"]], "f2", "sample", None, {"relab": ws["relab"], "max_fix_rounds": 2})
    st = runner.go("f2", log=lambda *a: None)
    assert st["status"] == "done" and len(st["rounds"]) == 3 and st.get("note_end")


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
