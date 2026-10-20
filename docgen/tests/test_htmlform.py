"""화면에서 만든 html 서식 (docgen/htmlform.py): form.json 값 채우기, 반복 행 수, 복제, 저장 전 초안, 검사. 브라우저 없이."""
import json
import random

import pytest

from docgen import htmlform as H
from docgen.entities import make_profile
from docgen.registry import REGISTRY, load_all
from docgen.render import render

TPL = """{% extends "_base.html.j2" %}
{% import "_macros.html.j2" as m with context %}
{% block content %}
{{ m.title("거 래 내 역") }}
<table><tr><th>성명</th><td>{{ f("customer.name", label="성명") }}</td></tr></table>
<table>{% for r in d.rows %}<tr><td>{{ f("rows." ~ loop.index0 ~ ".date", label="거래일") }}</td><td>{{ f("rows." ~ loop.index0 ~ ".amount", label="금액") }}</td></tr>{% endfor %}</table>
{% endblock %}
"""
FORM = {"name": "거래내역(시험)", "group": "finance", "origin": "analyzer", "parent": None,
        "fields": {"customer.name": {"label": "성명", "source": "profile.person.name"}},
        "lists": {"rows": {"min": 2, "max": 9, "fields": {"date": {"source": "rule:date_seq"}, "amount": {"source": "rule:amount"}}}}}


@pytest.fixture
def copies(tmp_path, monkeypatch):
    load_all()
    monkeypatch.setattr(H, "COPIES", tmp_path / "copies")
    added = []
    yield tmp_path / "copies", added
    for k in [k for k, v in REGISTRY.items() if v.template.startswith(H.PREFIX)]:
        REGISTRY.pop(k)


def make(root, doc_id, tpl=TPL, form=FORM):
    d = root / doc_id
    d.mkdir(parents=True)
    (d / "template.html.j2").write_text(tpl, encoding="utf-8")
    (d / "form.json").write_text(json.dumps(form, ensure_ascii=False), encoding="utf-8")
    assert H.register_forms() >= 1
    return load_all()[doc_id]


def test_fill_rows_and_values(copies):
    spec = make(copies[0], "tx_t")
    assert spec.origin == "analyzer" and spec.group == "finance" and spec.template == "@form/tx_t"
    p = make_profile(4)
    html, raw, data = render(spec, p, 4)
    keys = {r["key"]: r["value"] for r in raw}
    assert keys["customer.name"] == p.person.name
    n = len(data["rows"])
    assert 2 <= n <= 9 and f"rows.{n - 1}.amount" in keys and keys["rows.0.date"] < keys[f"rows.{n - 1}.date"]   # 날짜가 행마다 늘어남
    with H.draft("tx_t", rows="max"):
        assert len(render(spec, p, 4)[2]["rows"]) == 9
    with H.draft("tx_t", rows="min"):
        assert len(render(spec, p, 4)[2]["rows"]) == 2


def test_draft_template_and_checks(copies):
    spec = make(copies[0], "tx_t2")
    p = make_profile(1)
    new = TPL.replace("거 래 내 역", "초 안 제 목") + ""
    with H.draft("tx_t2", {"template": new.replace("{% endblock %}", '{{ f("nope.key") }}{% endblock %}')}):
        html, raw, data = render(spec, p, 1)
        assert "초 안 제 목" in html
        warn = H.check(H.load_form("tx_t2"), raw, data)
    assert any("nope.key" in w["text"] for w in warn)
    assert "초 안 제 목" not in render(spec, p, 1)[0]   # 초안은 그 렌더링 동안만
    form2 = {**FORM, "fields": {**FORM["fields"], "issue_date": {"source": "rule:date"}}}
    with H.draft("tx_t2", {"form": form2}):
        html, raw, data = render(spec, p, 1)
        warn = H.check(form2, raw, data)
    assert any("issue_date" in w["text"] and "안 나오는" in w["text"] for w in warn)


def test_clone_builtin_keeps_parent_generator(copies):
    d = H.clone("employment_certificate", "emp_copy_t", "재직증명서 복제")
    form = json.loads((d / "form.json").read_text(encoding="utf-8"))
    assert form["parent"] == "employment_certificate" and form["origin"] == "copy"
    spec = load_all()["emp_copy_t"]
    html, raw, data = render(spec, make_profile(2), 2)
    assert {r["key"] for r in raw} >= {"employee.name", "company.name"}
    with pytest.raises(ValueError):
        H.clone("employment_certificate", "emp_copy_t", "")   # 같은 ID
    with pytest.raises(ValueError):
        H.clone("hf169", "hf_copy_t", "")                    # overlay 는 복제하지 않음


def test_preview_source_files_follow_form_folder(copies):
    from docgen.preview import source_files, source_hash

    make(copies[0], "tx_t3")
    files = {f.name for f in source_files("tx_t3", common=False)}
    assert {"template.html.j2", "form.json", "htmlform.py"} <= files
    h0 = source_hash("tx_t3", common=False)
    H.save("tx_t3", TPL.replace("거 래 내 역", "바 뀐 제 목"), None)
    assert source_hash("tx_t3", common=False) != h0   # 고치면 미리보기 다시·재검수 필요


def test_catalog_kind_for_made_forms(copies):
    from studio import catalog

    make(copies[0], "tx_t4", form={**FORM, "group": "no_such_group"})
    assert load_all()["tx_t4"].group == "finance"
    assert catalog.kind_of(load_all()["tx_t4"].group, "tx_t4") == ("html", "analyzer")
    files = {f["role"] for f in catalog.form_detail("tx_t4")["files"]}
    assert "값 선언 (form.json)" in files


def test_rule_values_differ_per_row(copies):
    spec = make(copies[0], "tx_t5")
    with H.draft("tx_t5", rows="max"):
        data = spec.generate(make_profile(3), random.Random(0))
    assert len({r["amount"] for r in data["rows"]}) > 1
