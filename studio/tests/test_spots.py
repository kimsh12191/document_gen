"""① 서식 › 자리·템플릿 (studio/spots.py): 모든 자리·정한 곳, 템플릿 초안의 키 전후 비교, 템플릿·값 출처 저장. 브라우저 없이
(렌더러 대신 docgen.render 로 키·값을 얻고 자리 위치는 가짜)."""
import json

import pytest

from docgen import formdir, formfields
from docgen.entities import make_profile
from docgen.registry import load_all
from docgen.render import env, render
from docgen.tests.sandbox import forms_sandbox
from studio import spots as SP

ID = "employment_certificate"


def fake_render(doc_id, seed=0, heavy="default", special="default", draft=None, extra=None, rows=None):
    """Previewer.render 꼴. draft {"template"} 는 formdir.template_draft 로 (preview._render 와 같은 길). 기본 레이아웃으로."""
    from contextlib import nullcontext

    draft = {k: v for k, v in (draft or {}).items() if k != "blank"}
    ctx = formdir.template_draft(doc_id, draft["template"]) if "template" in draft else nullcontext()
    prof = make_profile(seed)
    prof.extra.update(extra or {"template_variants": {doc_id: "default"}})
    with ctx:
        _, raw, _ = render(load_all()[doc_id], prof, seed)
    return {"raw_keys": [f["key"] for f in raw], "fields": raw, "scale": 2, "pages": [{"width": 1588, "height": 2246}],
            "images": ["x.png"], "anchors": [{"key": f["key"], "occurrence": 0, "target": "field", "page": 0,
                                              "bbox": [10, 10 + 30 * i, 200, 30 + 30 * i], "text": str(f.get("value") or "")}
                                             for i, f in enumerate(raw)]}


@pytest.fixture
def sandbox(monkeypatch, tmp_path):
    root = forms_sandbox(monkeypatch, tmp_path, ID)
    yield root
    env().cache.clear() if env().cache else None


def test_template_line():
    text = 'a\n{{ f("x.name", label="성명") }}\n{% for r in d.rows %}{{ f("rows." ~ i ~ ".date") }}{% endfor %}\n{{ m.seal("인", key="company") }}'
    assert SP.template_line(text, "x.name") == 2
    assert SP.template_line(text, "rows.*.date") == 3
    assert SP.template_line(text, "seal.company") == 4
    assert SP.template_line(text, "nope") is None
    assert SP.raw_pattern("rows.12.date") == "rows.*.date"


def test_spots_lists_every_key_with_where(sandbox):
    out = SP.spots(ID, fake_render)
    assert out["file"].endswith(f"{ID}/look/template.html.j2") and out["kind"] == "code"
    keys = {k["pattern"]: k for k in out["keys"]}
    k = keys["employment.period"]
    assert k["status"] == "base" and k["spots"] == 1 and k["examples"]
    assert 'f("employment.period"' in out["template"].splitlines()[k["template_line"] - 1]
    assert k["fields_line"].startswith("fields.json:") and k["source"] == "code"
    assert {s["pattern"] for s in out["spots"]} <= set(keys)
    assert all(k["status"] in ("base", "other", "never") for k in keys.values())
    assert "diff" not in out


def test_draft_template_shows_lost_and_added_keys(sandbox):
    text = formdir.template(ID).read_text(encoding="utf-8")
    assert str(formdir.template(ID)).startswith(str(sandbox))
    draft = text.replace('{{ f("employment.duty", label="담당업무") }}', '{{ f("employment.memo", label="비고") }}')
    assert draft != text
    out = SP.spots(ID, fake_render, template=draft)
    assert out["diff"] == {"lost": ["employment.duty"], "added": ["employment.memo"]}
    assert out["template"] == draft
    assert formdir.template(ID).read_text(encoding="utf-8") == text   # 미리보기는 저장하지 않음


def test_save_template_checks_then_writes(sandbox):
    p = formdir.template(ID)
    text = p.read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="문법 오류"):
        SP.save_template(ID, text.replace("{% endblock %}", "{% endblok %}", 1), fake_render)
    with pytest.raises(ValueError, match="그리기 오류"):
        SP.save_template(ID, text.replace("{% block content %}", "{% block content %}{{ d.no_such_value }}", 1), fake_render)
    assert p.read_text(encoding="utf-8") == text
    new = text.replace("재 직 증 명 서", "재 직 증 명 서 (갑)")
    assert SP.save_template(ID, new, fake_render)["saved"]
    assert p.read_text(encoding="utf-8") == new and str(p).startswith(str(sandbox))


def test_set_value_writes_fields_json(sandbox):
    with pytest.raises(ValueError, match="고정 글자"):
        SP.set_value(ID, "employment.duty", "rule:fixed")
    with pytest.raises(ValueError, match="값 출처는"):
        SP.set_value(ID, "employment.duty", "javascript:x")
    SP.set_value(ID, "employment.duty", "rule:fixed", text="영업 관리")
    body = json.loads(formfields.path(ID).read_text(encoding="utf-8"))
    assert body["fields"]["employment.duty"]["source"] == "rule:fixed" and body["fields"]["employment.duty"]["text"] == "영업 관리"
    assert str(formfields.path(ID)).startswith(str(sandbox))
    SP.set_value(ID, "employment.duty", "rule:choice", choices=["영업", " ", "회계"])
    body = json.loads(formfields.path(ID).read_text(encoding="utf-8"))
    assert body["fields"]["employment.duty"]["choices"] == ["영업", "회계"] and "text" not in body["fields"]["employment.duty"]
    SP.set_value(ID, "employment.duty", "code")
    assert json.loads(formfields.path(ID).read_text(encoding="utf-8"))["fields"]["employment.duty"]["source"] == "code"


def test_overlay_form_has_no_template():
    with pytest.raises(ValueError, match="영역 편집"):
        SP.template_file("hf169")


def test_blank_css_hides_values_only():
    from docgen.preview import BLANK_CSS

    assert ".fv{color:transparent" in BLANK_CSS and ".seal" in BLANK_CSS


def test_draft_wins_over_cached_saved_template(sandbox):
    """저장본을 한 번 그린 뒤(템플릿 캐시에 있음) 초안을 그려도 초안이 쓰인다. 새 키는 값 출처를 정하면 값이 나온다."""
    a = '{{ f("employment.duty", label="담당업무") }}'
    draft = formdir.template(ID).read_text(encoding="utf-8").replace(a, a + ' {{ f("extra.memo", label="비고") }}', 1)
    assert "extra.memo" not in fake_render(ID)["raw_keys"]
    prof = make_profile(0)
    prof.extra.update({"template_variants": {ID: "default"}})
    with formdir.template_draft(ID, draft):
        _, raw, _ = render(load_all()[ID], prof, 0)
    assert any(f["key"] == "extra.memo" for f in raw)
    assert "extra.memo" not in fake_render(ID)["raw_keys"]   # 초안이 끝나면 다시 저장본
    SP.set_value(ID, "extra.memo", "rule:fixed", text="메모")
    out = SP.spots(ID, fake_render, template=draft)
    k = next(x for x in out["keys"] if x["pattern"] == "extra.memo")
    assert k["examples"] == ["메모"] and k["source"] == "rule:fixed" and out["diff"]["added"] == ["extra.memo"]
