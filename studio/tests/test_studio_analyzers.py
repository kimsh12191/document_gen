"""8단계 시험: 분석기 설정·작업 폴더·데이터 경계·명령 틀·결과 검사·승인 (studio/analyzers.py). 실제 분석기 없이."""
import json
import sys

import pytest
from PIL import Image

from studio import analyzers as AZ

CFG = {"providers": {
    "cli-in": {"kind": "cli", "cmd": sys.executable, "args": ["-c", "print(1)", "{job_dir}", "{image}", "{task_file}"], "external": False},
    "cli-out": {"kind": "cli", "cmd": sys.executable, "args": ["{task_text}"], "external": True},
    "api": {"kind": "openai", "base_url": "http://127.0.0.1:9/v1", "model": "m", "external": False},
    "bad": {"kind": "magic"}}}


@pytest.fixture
def img(tmp_path):
    p = tmp_path / "form.png"
    Image.new("RGB", (400, 560), "white").save(p)
    return p


def test_providers_and_check():
    ps = {p["name"]: p for p in AZ.providers(CFG)}
    assert ps["cli-in"]["cmd"] == sys.executable and not ps["cli-in"]["external"] and ps["cli-out"]["external"]
    assert AZ.check({"providers": {"v": {"kind": "cli", "cmd": sys.executable, "version_args": ["--version"]}}}, "v")["ok"]
    assert not AZ.check(CFG, "api")["ok"]   # 서버 없음 → 실패로 돌려줄 뿐 예외 아님
    with pytest.raises(ValueError):
        AZ.check(CFG, "bad")
    with pytest.raises(KeyError):
        AZ.check(CFG, "none")


def test_discover_newest(tmp_path):
    for n in ("tool-1.0", "tool-2.0"):
        (tmp_path / n).mkdir()
        (tmp_path / n / "cli.exe").write_text("x")
    import os
    import time
    os.utime(tmp_path / "tool-1.0" / "cli.exe", (time.time() - 100, time.time() - 100))
    assert AZ.resolve_cmd({"discover": str(tmp_path / "tool-*" / "cli*")}).endswith("tool-2.0" + os.sep + "cli.exe")


def test_job_folder_boundary_and_command(tmp_path, img):
    with pytest.raises(ValueError, match="외부 분석기"):
        AZ.create_job(tmp_path, CFG, "html", "cli-out", [str(img)], {}, {"real_data": True, "public": False})
    d = AZ.create_job(tmp_path, CFG, "html", "cli-in", [str(img)], {"form_id": "tx_a", "name": "거래내역", "group": "finance"},
                      {"real_data": True, "public": False, "label": "묶음 x"})
    job = json.loads((d / "job.json").read_text(encoding="utf-8"))
    assert job["kind"] == "html" and not job["external"] and "input/source.png" in job["sent"]
    assert {"TEMPLATE_GUIDE.md", "example_rows.html.j2", "_macros.html.j2", "keys.json"} <= {p.name for p in (d / "input").iterdir()}
    task = (d / "TASK.md").read_text(encoding="utf-8")
    assert "form_id: tx_a" in task and "python -m docgen.preview --dir output" in task and "{feedback}" not in task
    cmd = AZ.command(CFG, d)
    assert cmd[:3] == [sys.executable, "-c", "print(1)"] and cmd[3] == str(d) and cmd[4].endswith("source.png") and cmd[5].endswith("TASK.md")
    d2 = AZ.create_job(tmp_path, CFG, "html", "cli-out", [str(img)], {}, {"real_data": True, "public": True})   # 공개 서식이면 외부도 된다
    assert AZ.command(CFG, d2)[1].startswith("# 작업")   # {task_text} = 지시문 전체
    assert AZ.command(CFG, AZ.create_job(tmp_path, CFG, "layout", "api", [str(img)], {}, {}))[1:3] == ["-m", "studio.analyzers"]


def test_redo_carries_previous_output_and_comments(tmp_path, img):
    d = AZ.create_job(tmp_path, CFG, "html", "cli-in", [str(img)], {"form_id": "tx_b"}, {})
    (d / "output" / "template.html.j2").write_text("T", encoding="utf-8")
    (d / "output" / "form.json").write_text("{}", encoding="utf-8")
    AZ.add_comment(tmp_path, d.name, "합계 행을 넣어 주세요", "tester")
    d2 = AZ.create_job(tmp_path, CFG, "html", "cli-in", [str(img)], {"form_id": "tx_b"}, {}, from_job=d.name)
    assert (d2 / "input" / "previous" / "template.html.j2").read_text(encoding="utf-8") == "T"
    assert "합계 행을 넣어 주세요" in (d2 / "TASK.md").read_text(encoding="utf-8")
    d3 = AZ.create_job(tmp_path, CFG, "html", "cli-in", [str(img)], {"form_id": "tx_b"}, {}, comment="표 선을 굵게",
                       previous_files={"template.html.j2": "U", "form.json": {"fields": {}}})
    assert (d3 / "input" / "previous" / "template.html.j2").read_text(encoding="utf-8") == "U" and "표 선을 굵게" in (d3 / "TASK.md").read_text(encoding="utf-8")


def test_layout_validate_and_approve(tmp_path, img, monkeypatch):
    from docgen import overrides as OV
    from docgen import realform as RF

    form = tmp_path / "forms" / "img_az_t"
    form.mkdir(parents=True)
    (form / "layout.json").write_text(json.dumps({"name": "x", "pages": [{"width": 150, "height": 210}], "items": [], "texts": []}), encoding="utf-8")
    monkeypatch.setattr(RF, "IMAGE_FORMS", tmp_path / "forms")
    d = AZ.create_job(tmp_path, CFG, "layout", "cli-in", [str(img)], {"form_id": "img_az_t", "texts": [{"text": "성명"}]}, {})
    assert (d / "input" / "ocr_words.json").exists()
    assert not AZ.validate(d)["ok"]   # 결과 없음
    with pytest.raises(ValueError, match="검사를 통과"):
        AZ.approve(tmp_path, d.name, "t")
    (d / "output" / "layout.json").write_text(json.dumps({"items": [
        {"t": "text", "page": 0, "label": "성명", "rect": [80, 80, 240, 120], "key": "customer.name"},
        {"t": "check", "page": 0, "label": "수령", "rect": [80, 200, 300, 230], "options": [{"text": "자택", "box": [80, 205, 100, 225]}]},
        {"t": "oops", "page": 5, "rect": [1, 2]}]}), encoding="utf-8")
    assert not AZ.validate(d)["ok"]
    lay = json.loads((d / "output" / "layout.json").read_text(encoding="utf-8"))
    lay["items"].pop()
    (d / "output" / "layout.json").write_text(json.dumps(lay), encoding="utf-8")
    assert AZ.validate(d) == {**AZ.validate(d), "ok": True, "items": 2}
    got = AZ.approve(tmp_path, d.name, "tester")
    assert got["added"] == 2
    ov = OV.load("img_az_t")
    assert ov["add"][0]["rect"] == [round(80 / RF.BG_ZOOM, 2), round(80 / RF.BG_ZOOM, 2), round(240 / RF.BG_ZOOM, 2), round(120 / RF.BG_ZOOM, 2)]
    assert ov["add"][1]["options"][0]["text"] == "자택" and "rect" in ov["add"][1]["options"][0]
    assert AZ.get_job(tmp_path, d.name)["review"]["approved"]["by"] == "tester"
    assert [j["id"] for j in AZ.list_jobs(tmp_path)][0] == d.name


def test_html_validate_reports_missing_files(tmp_path, img):
    d = AZ.create_job(tmp_path, CFG, "html", "cli-in", [str(img)], {}, {})
    res = AZ.validate(d)
    assert not res["ok"] and any("template.html.j2" in e for e in res["errors"])
    (d / "output" / "template.html.j2").write_text("x", encoding="utf-8")
    (d / "output" / "form.json").write_text("{not json", encoding="utf-8")
    assert any("form.json" in e for e in AZ.validate(d)["errors"])
    with pytest.raises(KeyError):
        AZ.job_file(tmp_path, d.name, "../../etc/passwd")


def test_html_validate_renders_rows_min_max(tmp_path, img):
    """결과를 docgen.preview 로 실제 렌더링: 행 최대면 여러 쪽 (브라우저가 없으면 건너뜀)."""
    pytest.importorskip("playwright")
    from docgen.image import ImageRenderer

    try:
        ImageRenderer(scale=1.0).__enter__().__exit__(None, None, None)
    except Exception as e:  # noqa: BLE001
        pytest.skip(f"Chromium 없음: {e}")
    from docgen.tests.test_htmlform import FORM, TPL

    d = AZ.create_job(tmp_path, CFG, "html", "cli-in", [str(img)], {}, {})
    (d / "output" / "template.html.j2").write_text(TPL, encoding="utf-8")
    form = {**FORM, "lists": {"rows": {**FORM["lists"]["rows"], "min": 1, "max": 80}}}
    (d / "output" / "form.json").write_text(json.dumps(form, ensure_ascii=False), encoding="utf-8")
    res = AZ.validate(d)
    assert res["ok"], res["errors"]
    assert res["renders"]["min"]["pages"] == 1 and res["renders"]["max"]["pages"] >= 2
    assert all((d / p).exists() for p in res["renders"]["max"]["images"])
