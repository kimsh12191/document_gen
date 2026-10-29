"""서식 폴더 (docgen/formdir.py): 예전 자리도 읽고, migrate 로 옮겨도 생성 결과·서식 해시가 같다."""
import json
import random
import shutil

import pytest

from docgen import formdir
from docgen import realform as RF
from docgen.entities import make_profile
from docgen.preview import source_hash
from docgen.registry import load_all


@pytest.fixture()
def legacy_hf(tmp_path, monkeypatch):
    """hf169 를 예전 꼴로: forms/layouts/<분류>/169.json + 레이아웃 "file" 자리의 원본 PDF (서식 폴더 없음)."""
    load_all()   # 서식 목록은 저장소 그대로 (자리를 바꾸기 전에 한 번 읽어 둔다)
    src = formdir.folder("hf169")
    lay = json.loads((src / "layout.json").read_text(encoding="utf-8"))
    root = tmp_path / "docgen"
    old = root / "forms" / "layouts" / lay["class"].replace("/", "_") / "169.json"
    old.parent.mkdir(parents=True)
    shutil.copyfile(src / "layout.json", old)
    pdf = root / lay["file"]
    pdf.parent.mkdir(parents=True)
    shutil.copyfile(src / "look" / "original.pdf", pdf)
    for name, value in (("DOCGEN", root), ("PUBLIC", root / "forms"), ("NEW_FORMS", root / "forms"),
                        ("LEGACY_LAYOUTS", root / "forms" / "layouts")):
        monkeypatch.setattr(formdir, name, value)
    RF.load_layout.cache_clear()
    yield root, old, pdf
    RF.load_layout.cache_clear()


def _build(seed=1):
    return RF.build_form("hf169", make_profile(seed), random.Random(f"data:{seed}:hf169"))


def test_legacy_hf_is_read_then_moved_with_same_output(legacy_hf):
    root, old, pdf = legacy_hf
    assert formdir.folder("hf169") is None and RF.layout_path(169) == old and formdir.original_pdf(169) == pdf
    before, bg, h = _build(), RF.raw_background("hf169", 0), source_hash("hf169", common=False)
    rows = formdir.migrate(ids=["hf169"])
    assert rows[0]["status"] == "옮길 것" and old.exists()
    formdir.migrate(apply=True, ids=["hf169"])
    d = root / "forms" / "hf169"
    assert (d / "layout.json").exists() and (d / "look" / "original.pdf").exists() and not pdf.exists()
    assert old.with_name("169.json.migrated").exists() and not old.exists()
    assert RF.layout_path(169) == d / "layout.json" and formdir.original_pdf(169) == d / "look" / "original.pdf"
    assert _build() == before and RF.raw_background("hf169", 0) == bg
    assert source_hash("hf169", common=False) == h   # 해시 이름은 옮기기 전 자리
    assert formdir.source_path(json.loads((d / "layout.json").read_text(encoding="utf-8"))["file"]) == d / "look" / "original.pdf"


def test_migrate_refuses_different_files(legacy_hf):
    root, old, _ = legacy_hf
    d = root / "forms" / "hf169"
    d.mkdir(parents=True)
    (d / "layout.json").write_text("{}", encoding="utf-8")
    [row] = formdir.migrate(apply=True, ids=["hf169"])
    assert row["status"].startswith("건너뜀: 예전과 새 파일이 다름") and old.exists()


def test_private_image_form_pages_move_into_look(tmp_path, monkeypatch):
    load_all()
    priv = tmp_path / "private"
    d = priv / "img_t_priv"
    d.mkdir(parents=True)
    (d / "layout.json").write_text(json.dumps({"name": "t", "pages": [{"width": 100, "height": 100}], "items": []}), encoding="utf-8")
    (d / "page_0.png").write_bytes(b"png")
    (d / "overrides.json").write_text(json.dumps({"erase": [{"page": 0, "rect": [0, 0, 1, 1]}]}), encoding="utf-8")
    monkeypatch.setenv("DOCGEN_PRIVATE_FORMS", str(priv))
    monkeypatch.setattr(formdir, "NEW_FORMS", tmp_path / "forms")
    assert formdir.image_dir("img_t_priv") == d and formdir.page_png("img_t_priv", 0) == d / "page_0.png"
    assert formdir.is_private(d) and d in formdir.image_dirs()
    formdir.migrate(apply=True, ids=["img_t_priv"])
    assert formdir.page_png("img_t_priv", 0) == d / "look" / "page_0.png" and (d / "layout.json").exists()
    from docgen import regions

    assert regions.path("img_t_priv") == d / "regions.json"   # 사람 수정도 사내 서식 폴더
    assert regions.read("img_t_priv")["erase"]               # 아직 옮기지 않은 예전 수정도 읽는다
    assert formdir.hash_label(d / "look" / "page_0.png") == d / "page_0.png"


def test_builtin_template_loader_and_paths():
    from docgen.render import env

    p = formdir.template("employment_certificate")
    assert p == formdir.folder("employment_certificate") / "look" / "template.html.j2"
    assert env().get_template("income/employment_certificate.html.j2").filename == str(p)
    assert formdir.jinja_source("corporate/_seal.html.j2") is None   # 그룹 부품은 templates/ 에 남는다
    assert formdir.hash_label(p) == formdir.LEGACY_TEMPLATES / "income" / "employment_certificate.html.j2"
    assert formdir.variants_dir("employment_certificate") == formdir.folder("employment_certificate") / "variants"
    roles = dict(formdir.describe("gov_income"))
    assert roles["값 선언 (form.json)"] == formdir.folder("gov_income") / "form.json"


def test_builtin_declarations_and_per_key_override(tmp_path, monkeypatch):
    """코드 서식 칸 목록: 생성 함수 칸은 source "code" (결과 그대로), 값 출처를 바꾼 칸만 덮어쓴다 (반복 행은 행마다)."""
    from docgen import formfields
    from docgen.htmlform import declare
    from docgen.render import render
    from docgen.tests.sandbox import forms_sandbox

    load_all()
    forms_sandbox(monkeypatch, tmp_path, "bank_statement")
    spec = load_all()["bank_statement"]
    html, raw, _ = render(spec, make_profile(2), 2)
    f = formfields.read("bank_statement")
    assert f["fields"]["holder"]["source"] == "code" and f["lists"]["rows"]["source"] == "code"
    assert render(spec, make_profile(2), 2)[0] == html   # "code" 만 적힌 칸 목록은 결과를 바꾸지 않는다
    f["fields"]["holder"] = {"label": "예금주", "source": "rule:fixed", "text": "칸목록"}
    memo = next(k for k in f["lists"]["rows"]["fields"] if "memo" in k or "desc" in k or "note" in k)
    f["lists"]["rows"]["fields"][memo] = {"source": "rule:fixed", "text": "행덮어쓰기"}
    formfields.write("bank_statement", f)
    _, raw2, data = render(spec, make_profile(2), 2)
    assert data["holder"] == "칸목록" and all(r[memo] == "행덮어쓰기" for r in data["rows"])
    assert len(data["rows"]) == len([r for r in raw if r["key"].endswith("." + memo)])   # 행 수는 생성 함수 그대로
    _, n = formfields.merge_declared("bank_statement", declare("bank_statement", 4))   # 다시 적어도 사람이 바꾼 칸은 그대로
    assert formfields.read("bank_statement")["fields"]["holder"]["source"] == "rule:fixed" and n == 0


def test_refresh_registers_updates_and_removes_form_folders(tmp_path, monkeypatch):
    """서식 다시 읽기 (registry.refresh): 다시 띄우지 않고 새 폴더 등록 · 이름 다시 읽기 · 깨진 폴더는 이유만 · 지운 폴더는 목록에서 뺌.
    코드 서식과 하나은행 원본은 그대로."""
    from docgen import registry
    from docgen.render import render

    reg = load_all()
    before = set(reg)
    priv = tmp_path / "private"
    monkeypatch.setenv("DOCGEN_PRIVATE_FORMS", str(priv))
    src = formdir.folder("gov_income")
    good = priv / "t_new_form"
    shutil.copytree(src, good)
    bad = priv / "t_bad_form"
    shutil.copytree(src, bad)
    (bad / "look" / "template.html.j2").write_text('{% extends "_base.html.j2" %}{% block content %}{% if %}{% endblock %}',
                                                    encoding="utf-8")
    img = priv / "img_t_refresh"
    img.mkdir()
    (img / "layout.json").write_text(json.dumps({"name": "새 이미지", "pages": [{"width": 100, "height": 140}], "items": []}),
                                     encoding="utf-8")
    try:
        r = registry.refresh()
        assert r["added"] == ["img_t_refresh", "t_new_form"] and not r["removed"]
        assert [p["id"] for p in r["problems"]] == ["t_bad_form"] and "템플릿 문법 오류" in r["problems"][0]["reason"]
        assert "t_bad_form" not in reg and reg["img_t_refresh"].name == "새 이미지"
        html, _, data = render(reg["t_new_form"], make_profile(1), 1)   # 등록하자마자 그려진다
        assert html and data
        form = json.loads((good / "form.json").read_text(encoding="utf-8"))
        (good / "form.json").write_text(json.dumps({**form, "name": "바꾼 이름", "group": "tax"}, ensure_ascii=False), encoding="utf-8")
        r = registry.refresh()
        assert r["updated"] == ["t_new_form"] and not r["added"] and reg["t_new_form"].name == "바꾼 이름"
        assert reg["t_new_form"].group == "tax"
        assert registry.refresh()["updated"] == []   # 바뀐 것이 없으면 그대로
        shutil.rmtree(good)
        shutil.rmtree(img)
        r = registry.refresh()
        assert r["removed"] == ["img_t_refresh", "t_new_form"] and "t_new_form" not in reg
        assert set(reg) == before   # 코드 서식·hf### 는 그대로
    finally:
        for k in ("t_new_form", "img_t_refresh", "t_bad_form"):
            reg.pop(k, None)


def test_unknown_form_id_gets_a_message_not_a_traceback(capsys):
    from docgen import formdir, regions

    assert formdir.main(["path", "employment_certificat"]) == 2
    err = capsys.readouterr().err
    assert "서식 ID 'employment_certificat' 가 없습니다" in err and "employment_certificate" in err
    assert formdir.main(["check", "hf001", "no_such_form_x"]) == 2
    assert regions.main(["path", "no_such_form_x"]) == 2


def test_regions_path_points_at_the_field_list(capsys):
    from docgen import regions

    assert regions.main(["path", "employment_certificate"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("docgen/forms/employment_certificate/fields.json") and "regions·variants" in out
    assert regions.main(["path", "hf001"]) == 0
    assert "docgen/forms/hf001/fields.json" in capsys.readouterr().out
