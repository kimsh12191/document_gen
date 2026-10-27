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
    assert formdir.hash_label(p) == formdir.TEMPLATES / "income" / "employment_certificate.html.j2"
    assert formdir.variants_dir("employment_certificate") == formdir.folder("employment_certificate") / "variants"
    roles = dict(formdir.describe("gov_income"))
    assert roles["값 선언 (form.json)"] == formdir.folder("gov_income") / "form.json"
