"""서식 수정 파일 하나 (docgen/regions.py, 서식 폴더의 regions.json): 예전 위치도 읽고, 옮겨도 결과가 같고, 서식 종류가 다른 수정은 멈춘다."""
import json
import random

import pytest

from docgen import html_regions as HR
from docgen import overrides as OV
from docgen import realform as RF
from docgen import regions
from docgen import formdir
from docgen import template_variants as T
from docgen.entities import make_profile
from docgen.preview import source_hash
from docgen.tests.sandbox import forms_sandbox


@pytest.fixture()
def roots(tmp_path, monkeypatch):
    monkeypatch.setattr(regions, "LEGACY_OVERLAY", tmp_path / "overrides")
    monkeypatch.setattr(regions, "LEGACY_HTML", tmp_path / "html_regions")
    monkeypatch.setattr(formdir, "LEGACY_REGIONS", tmp_path / "regions")
    monkeypatch.setattr(formdir, "LEGACY_VARIANTS", tmp_path / "variants")
    forms_sandbox(monkeypatch, tmp_path, "hf169", "gov_income", "employment_certificate", fields=False)   # 칸 목록 만들기 전 꼴
    return tmp_path


def _write(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def _build(doc_id="hf169", seed=1):
    return RF.build_form(doc_id, make_profile(seed), random.Random(f"data:{seed}:{doc_id}"))


def test_overlay_legacy_is_read_then_migrated_with_same_output(roots):
    lay = RF.raw_layout("hf169")
    m = next(m for it, m in OV.matches(lay) if it.get("label") == "직장주소")
    ov = {"items": [{"match": m, "drop": True}], "updated": {"by": "a", "at": "x"}}
    plain = source_hash("hf169", common=False)
    _write(roots / "overrides" / "hf169.json", ov)
    assert OV.load("hf169") == ov and regions.path("hf169") == roots / "forms" / "hf169" / "regions.json"
    before, h_legacy = _build(), source_hash("hf169", common=False)
    assert "employer.address" not in {it.get("key") for it in before["items"]} and h_legacy != plain
    assert [r["status"] for r in regions.migrate(ids=["hf169"])] == ["옮길 것"] and not regions.path("hf169").exists()
    regions.migrate(apply=True, ids=["hf169"])
    saved = json.loads(regions.path("hf169").read_text(encoding="utf-8"))
    assert saved == {"engine": "overlay", "unit": "pt", **ov}   # 기록 칸(updated)도 그대로
    assert (roots / "overrides" / "hf169.json.migrated").exists() and not (roots / "overrides" / "hf169.json").exists()
    assert _build() == before and regions.check("hf169") == []
    OV.freeze("hf169")   # 칸 목록(fields.json)으로 굳히면 예전 수정 파일은 .migrated
    assert not regions.path("hf169").exists() and _build() == before and regions.check("hf169") == []
    f = json.loads(OV.path("hf169").read_text(encoding="utf-8"))
    assert f["engine"] == "overlay" and f["updated"] == ov["updated"] and f["dropped"] == [m]
    assert "employer.address" not in {it.get("key") for it in RF.form_layout("hf169")[0]["items"]}


def test_hash_unchanged_until_moved(roots):
    """경로가 해시에 들어가도, 새 파일이 없는 서식은 예전과 같은 해시 (검수 표시가 풀리지 않는다)."""
    files = regions.hash_files("hf169")
    assert files == [roots / "overrides" / "hf169.json"]
    assert regions.hash_files("gov_income") == [roots / "overrides" / "gov_income.json", roots / "html_regions" / "gov_income.json"]


def test_wrong_engine_stops_instead_of_being_ignored(roots):
    _write(regions.path("hf169"), {"regions": [{"key": "x"}]})
    with pytest.raises(ValueError, match="overlay 서식인데"):
        OV.load("hf169")
    _write(regions.path("gov_income"), {"engine": "overlay", "items": []})
    with pytest.raises(ValueError, match="html 서식인데"):
        HR.load("gov_income")
    assert "html 서식인데" in regions.check("gov_income")[0]


def test_html_default_and_variants_in_one_file(roots):
    T.add("employment_certificate", "letter_copy", "회사별 양식")
    row = {"key": "x.a", "source": "rule:fixed", "text": "가", "page": 0, "rect": [10, 10, 50, 20]}
    row2 = {**row, "text": "나"}
    _write(roots / "html_regions" / "employment_certificate.json", {"regions": [row]})
    _write(T.folder("employment_certificate") / "letter_copy.regions.json", {"regions": [row2]})
    assert HR.load("employment_certificate") == {"regions": [row]}
    assert HR.load("employment_certificate", "letter_copy") == {"regions": [row2]}
    HR.save("employment_certificate", {"regions": [row, {**row, "key": "x.b"}]})
    saved = json.loads(HR.path("employment_certificate").read_text(encoding="utf-8"))   # 칸 목록 fields.json
    assert saved["engine"] == "html" and saved["unit"] == "px" and len(saved["regions"]) == 2
    assert saved["variants"] == {"letter_copy": {"regions": [row2]}}   # 저장하면서 변형 파일도 합쳐진다
    assert regions.legacy("employment_certificate") == {}
    assert (T.folder("employment_certificate") / "letter_copy.regions.json.migrated").exists()


def test_check_reports_leftovers_and_unknown_fields(roots):
    _write(regions.path("hf169"), {"engine": "overlay", "items": [], "add": [], "erase": [{"page": 0, "rect": [0, 0, 5, 5]}],
                                   "typo": 1})
    _write(roots / "overrides" / "hf169.json", {"items": []})
    probs = regions.check("hf169")
    assert any("예전 수정 파일이 남아" in p for p in probs) and any("typo" in p for p in probs)
    assert OV.load("hf169")["erase"]   # 새 파일만 읽는다
    _write(regions.path("hf169"), {"items": [{"match": {"page": 0, "t": "text", "label": "없는항목", "n": 0}, "drop": True}]})
    assert any("깨진 수정" in p for p in regions.check("hf169"))


def test_cli_path_and_show(roots, capsys):
    assert regions.main(["path", "hf169"]) == 0
    assert "hf169/fields.json" in capsys.readouterr().out   # 사람 수정은 칸 목록에 (처음 저장할 때 생김)
    rows = regions.show("hf169")
    assert rows and all(r["key"] and r["how"] == "자동" for r in rows)
    lay = RF.raw_layout("hf169")
    m = next(m for it, m in OV.matches(lay) if it.get("label") == "직장주소")
    OV.save("hf169", {"items": [{"match": m, "source": "rule:fixed", "text": "고정"}]})
    assert any(r["how"] == "수정" and r["source"] == "rule:fixed" for r in regions.show("hf169"))
    assert OV.load("no_such_form") == {}


def test_html_fields_hold_value_declarations_and_overrides(roots):
    """복제 서식의 form.json 값 선언(fields)이 칸 목록으로 옮겨지고, 코드 서식도 칸 목록의 값 선언으로 덮어쓴다."""
    from docgen import formfields
    from docgen import htmlform as H
    from docgen.registry import load_all
    from docgen.render import render

    d = H.form_dir("gov_income")
    form = json.loads((d / "form.json").read_text(encoding="utf-8"))
    form["fields"] = json.loads((formdir.PUBLIC / "gov_income" / "fields.json").read_text(encoding="utf-8"))["fields"]
    _write(d / "form.json", form)   # 칸 목록 만들기 전 꼴: 값 선언이 form.json 에
    assert not formfields.exists("gov_income")
    before = H.load_form("gov_income")
    formfields.adopt("gov_income")
    assert "fields" not in json.loads((d / "form.json").read_text(encoding="utf-8"))
    assert formfields.read("gov_income")["fields"] == form["fields"] and H.load_form("gov_income") == before
    spec = load_all()["employment_certificate"]
    html, raw, _ = render(spec, make_profile(1), 1)
    formfields.update("employment_certificate", {"fields": {"employee.name": {"source": "rule:fixed", "text": "칸목록값"}}}, ("fields",))
    _, raw2, data = render(spec, make_profile(1), 1)
    assert data["employee"]["name"] == "칸목록값"
    assert next(f for f in raw2 if f["key"] == "employee.name")["value"] == "칸목록값"
    formfields.update("employment_certificate", {}, ("fields",))
    assert render(spec, make_profile(1), 1)[0] == html   # 비우면 그대로
