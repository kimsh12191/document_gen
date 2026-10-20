"""studio 와 그 생성기 쪽 변경(사람 수정층, 표시 요소, 값 출처, 검수 목록표) 시험. 브라우저 없이 돈다."""
import json
import random

import pytest

from docgen import marks as M
from docgen import overrides as OV
from docgen import realform as RF
from docgen import sources as SRC
from docgen.entities import make_profile
from docgen.registry import load_all


@pytest.fixture()
def tmp_overrides(tmp_path, monkeypatch):
    monkeypatch.setattr(OV, "OVERRIDES", tmp_path / "overrides")
    return tmp_path / "overrides"


def _build(doc_id="hf169", seed=1):
    return RF.build_form(doc_id, make_profile(seed), random.Random(f"data:{seed}:{doc_id}"))


def _by_key(d):
    return {it["key"]: it for it in d["items"] if it.get("key")}


def test_no_override_is_same_as_before(tmp_overrides):
    """수정 파일이 없으면 build_form 은 build(no) 와 같은 결과 (예전 함수 이름 그대로)."""
    a = RF.build(169, make_profile(3), random.Random("x"))
    b = RF.build_form("hf169", make_profile(3), random.Random("x"))
    assert a == b


def test_override_source_rect_drop_add_erase(tmp_overrides):
    lay = RF.raw_layout("hf169")
    m = next(m for it, m in OV.matches(lay) if it.get("label") == "직장주소")
    staff = next(m for it, m in OV.matches(lay) if it["t"] == "staff")
    ov = {"items": [{"match": m, "source": "profile.employment.company.address.road_short", "set": {"rect": [120, 270, 400, 287]}},
                    {"match": staff, "drop": True}],
          "add": [{"t": "text", "page": 1, "label": "비고", "rect": [80, 600, 300, 618], "key": "remark", "source": "rule:fixed",
                   "text": "추가 확인"}],
          "erase": [{"page": 0, "rect": [380, 15, 550, 68], "fill": "white"}]}
    before = _by_key(_build())
    OV.save("hf169", ov)
    after = _by_key(_build())
    p = make_profile(1)
    assert after["employer.address"]["value"] == p.employment.company.address.road_short
    assert before["employer.address"]["value"] != after["employer.address"]["value"]
    assert after["employer.address"]["rect"][0] == pytest.approx(120 * RF.PX, abs=0.2)
    assert after["remark"]["value"] == "추가 확인" and after["remark"]["page"] == 1
    n_staff = lambda d: sum(1 for k in d if k.startswith("staff."))   # noqa: E731
    assert n_staff(after) == n_staff(before) - 1
    d = _build()
    assert "?e=" in d["pages"][0]["bg"] and "?e=" not in d["pages"][1]["bg"]


def test_draft_does_not_touch_file(tmp_overrides):
    lay = RF.raw_layout("hf169")
    m = next(m for it, m in OV.matches(lay) if it.get("label") == "직장주소")
    with OV.draft("hf169", {"items": [{"match": m, "drop": True}]}):
        assert "employer.address" not in _by_key(_build())
    assert "employer.address" in _by_key(_build())
    assert not OV.path("hf169").exists()


def test_broken_override_reported(tmp_overrides):
    lay, broken = OV.apply(RF.raw_layout("hf169"), {"items": [{"match": {"page": 0, "t": "text", "label": "없는항목", "n": 0},
                                                              "drop": True}]})
    assert len(broken) == 1 and len(lay["items"]) == len(RF.raw_layout("hf169")["items"])


def test_erase_white_and_auto():
    from PIL import Image

    img = Image.new("RGB", (100, 100), (230, 220, 200))
    img.paste((0, 0, 0), (40, 40, 60, 60))
    w = OV.apply_erase(img, [{"rect": [10, 10, 20, 20], "fill": "white"}], 3.0)
    assert w.getpixel((45, 45)) == (255, 255, 255)
    a = OV.apply_erase(img, [{"rect": [12, 12, 22, 22], "fill": "auto"}], 3.0)
    assert a.getpixel((50, 50)) == (230, 220, 200)   # 주변 종이색으로 덮였다


def test_marks_defaults_reproduce_old_constants(monkeypatch, tmp_path):
    monkeypatch.setattr(M, "SETTINGS", tmp_path / "marks.json")
    monkeypatch.setattr(M, "POOLS", tmp_path / "pools.json")
    assert M.settings() == M.DEFAULTS
    assert [x["id"] for x in M.expand(M.pools()["check"])] == ["V", "V", "✓", "✔", "■", "O"]
    assert [x["id"] for x in M.expand(M.pools()["hand_fonts"])] == ["NanumPen", "NanumBrush", "HiMelody", "GamjaFlower"]
    r = random.Random(0)
    state = r.getstate()
    assert M.pick(r, M.pools()["sign"])["builtin"] and r.getstate() == state   # 하나뿐이면 난수를 쓰지 않는다


def test_sources():
    p = make_profile(0)
    assert SRC.value("profile.person.name", p, random.Random(0)) == p.person.name
    assert SRC.value("profile.person.birth", p, random.Random(0)).count(".") >= 2
    assert SRC.value("rule:empty", p, random.Random(0)) is None
    assert SRC.value("rule:choice", p, random.Random(0), {"choices": ["가", "나"]}) in ("가", "나")
    assert SRC.value("rule:amount", p, random.Random(0)) is not None
    paths = {x["source"] for x in SRC.profile_paths(p)}
    assert "profile.person.name" in paths and "profile.employment.company.address.road_short" in paths


def test_editor_validate_rejects_bad_input():
    from studio import editor

    with pytest.raises(ValueError):
        editor.validate("hf169", {"add": [{"t": "text", "page": 0, "rect": [0, 0, 10, 10], "key": "한글키"}]})
    with pytest.raises(ValueError):
        editor.validate("hf169", {"add": [{"t": "text", "page": 0, "rect": [0, 0, 10, 10], "source": "rule:nothing"}]})
    with pytest.raises(ValueError):
        editor.validate("hf169", {"erase": [{"page": 99, "rect": [0, 0, 10, 10]}]})
    ok = editor.validate("hf169", {"erase": [{"page": 0, "rect": [1, 1, 10, 10], "fill": "auto"}]})
    assert ok["erase"][0]["fill"] == "auto"
    with pytest.raises(ValueError):
        editor.validate("loan_application", {})   # html 서식은 영역 편집기가 아니다


def test_layout_view_ids_and_status(tmp_overrides):
    from studio import editor

    v = editor.layout_view("hf169")
    ids = [it["id"] for it in v["items"]]
    assert len(ids) == len(set(ids))
    it = next(x for x in v["items"] if x.get("label") == "직장주소")
    OV.save("hf169", {"items": [{"match": it["match"], "key": "employer.address_full"}]})
    v2 = editor.layout_view("hf169")
    it2 = next(x for x in v2["items"] if x["id"] == it["id"])
    assert it2["status"] == "edited" and it2["key"] == "employer.address_full" and it2["base_raw"].get("key") is None


def test_catalog_review_goes_stale(tmp_path, monkeypatch, tmp_overrides):
    from studio import catalog

    monkeypatch.setattr(catalog, "CATALOG_JSON", tmp_path / "catalog.json")
    catalog.set_review("hf169", True, "tester")
    entry = json.loads((tmp_path / "catalog.json").read_text(encoding="utf-8"))["hf169"]
    assert catalog.review_state("hf169", entry) == "done"
    OV.save("hf169", {"erase": [{"page": 0, "rect": [1, 1, 10, 10], "fill": "white"}]})
    assert catalog.review_state("hf169", entry) == "stale"
    catalog.set_meta("hf169", split="test_only", note="평가 전용")
    catalog.add_issue("hf169", {"seed": 0, "page": 0, "note": "겹침"})
    e = json.loads((tmp_path / "catalog.json").read_text(encoding="utf-8"))["hf169"]
    assert e["split"] == "test_only" and e["issues"][0]["id"] == "i1"
    with pytest.raises(ValueError):
        catalog.set_meta("hf169", split="nope")

