"""서식 생성 스크립트 (서식 폴더의 generate.py, docgen/htmlform.run_script): 칸 목록이 채운 값을 adjust(d, p, rng) 가 다듬는다.
없으면 그대로, 오류는 그 서식만 (줄 번호와 함께), 재현성·새 키는 검사 경고, 스크립트도 서식 해시에 들어간다."""
import json
import random

import pytest

from docgen import formkit as FK
from docgen import htmlform as H
from docgen.entities import make_profile
from docgen.preview import source_hash
from docgen.registry import load_all, refresh
from docgen.render import render

TEMPLATE = """{% extends "_base.html.j2" %}
{% import "_macros.html.j2" as m with context %}
{% block content %}
<p>{{ f("period.start", label="시작일") }} ~ {{ f("period.end", label="종료일") }}</p>
<table>{% for r in d.rows %}<tr><td>{{ f("rows." ~ loop.index0 ~ ".out", label="출금") }}</td></tr>{% endfor %}</table>
<p>{{ f("total.out", label="합계") }}</p>
{% endblock %}
"""
FORM = {"name": "스크립트 시험", "group": "finance", "category": "external", "page": "a4", "origin": "analyzer", "parent": None}
FIELDS = {"engine": "html", "unit": "px",
          "fields": {"period.start": {"label": "시작일", "type": "date", "source": "rule:date"},
                     "period.end": {"label": "종료일", "type": "date", "source": "rule:date"},
                     "total.out": {"label": "합계", "type": "amount", "source": "rule:amount"}},
          "lists": {"rows": {"min": 3, "max": 6, "fields": {"out": {"label": "출금", "type": "amount", "source": "rule:amount"}}}}}
SCRIPT = '''from docgen.formkit import to_date, date_like, to_amount, amount_like, rows


def adjust(d, p, rng):
    s, e = to_date(d["period"]["start"]), to_date(d["period"]["end"])
    if s > e:
        d["period"]["start"], d["period"]["end"] = date_like(e, d["period"]["start"]), date_like(s, d["period"]["end"])
    d["total"]["out"] = amount_like(sum(to_amount(r["out"]) or 0 for r in rows(d, "rows")), d["total"]["out"])
    return d
'''


@pytest.fixture()
def form(tmp_path, monkeypatch):
    reg = load_all()
    priv = tmp_path / "private"
    d = priv / "t_script_form"
    (d / "look").mkdir(parents=True)
    (d / "look" / "template.html.j2").write_text(TEMPLATE, encoding="utf-8")
    (d / "form.json").write_text(json.dumps(FORM, ensure_ascii=False), encoding="utf-8")
    (d / "fields.json").write_text(json.dumps(FIELDS, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setenv("DOCGEN_PRIVATE_FORMS", str(priv))
    assert refresh()["added"] == ["t_script_form"]
    yield d
    reg.pop("t_script_form", None)


def _values(seed):
    _, raw, data = render(load_all()["t_script_form"], make_profile(seed), seed)
    return {r["key"]: r["value"] for r in raw}, data


def test_no_script_is_unchanged_and_script_fixes_relations(form):
    plain = {s: _values(s)[0] for s in range(8)}
    total = lambda v: (FK.to_amount(v["total.out"]), sum(FK.to_amount(x) for k, x in v.items() if k.startswith("rows.")))  # noqa: E731
    assert any(a != b for a, b in map(total, plain.values()))   # 칸마다 따로 뽑으면 합계가 안 맞는다
    h = source_hash("t_script_form", common=False)
    (form / "generate.py").write_text(SCRIPT, encoding="utf-8")
    assert source_hash("t_script_form", common=False) != h   # 스크립트도 해시에 (미리보기 다시 그림, 재검수 필요)
    assert refresh()["with_script"] == [] and H.script_path("t_script_form") == form / "generate.py"
    for s in range(8):
        v, _ = _values(s)
        assert FK.to_date(v["period.start"]) <= FK.to_date(v["period.end"])
        outs = [FK.to_amount(x) for k, x in v.items() if k.startswith("rows.")]
        assert FK.to_amount(v["total.out"]) == sum(outs)
        assert v == _values(s)[0]   # 같은 seed 는 같은 문서
    assert H.script_warnings("t_script_form") == []
    assert any(r == "생성 스크립트 (generate.py)" for r, _ in __import__("docgen.formdir", fromlist=["x"]).describe("t_script_form"))


def test_script_errors_point_to_line_and_stay_in_that_form(form):
    (form / "generate.py").write_text("def adjust(d, p, rng):\n    x = 1\n    return d['nope']['x']\n", encoding="utf-8")
    with pytest.raises(ValueError, match=r"generate.py 3번째 줄: KeyError"):
        _values(0)
    render(load_all()["employment_certificate"], make_profile(0), 0)   # 다른 서식은 그대로
    (form / "generate.py").write_text("def adjust(d, p, rng)\n    return d\n", encoding="utf-8")
    assert "생성 스크립트 문법 오류" in H.check_dir(form)
    with pytest.raises(ValueError, match="generate.py 1번째 줄: SyntaxError"):
        _values(0)
    (form / "generate.py").write_text("def other(d):\n    return d\n", encoding="utf-8")
    with pytest.raises(ValueError, match="adjust"):
        _values(0)


def test_script_checks_warn_on_new_keys_and_nondeterminism(form):
    (form / "generate.py").write_text(
        "import random\n\ndef adjust(d, p, rng):\n    d['extra'] = {'n': str(random.random())}\n    return d\n", encoding="utf-8")
    _, raw, data = render(load_all()["t_script_form"], make_profile(0), 0)
    warn = [w["text"] for w in H.check(H.load_form("t_script_form"), raw, data, doc_id="t_script_form")]
    assert any("두 번 돌렸는데 결과가 다릅니다" in w for w in warn)
    assert any("칸 목록에 없는 키" in w and "extra.n" in w for w in warn)


def test_formkit_helpers_keep_the_notation():
    assert FK.to_date("2025년 1월 3일") == FK.to_date("2025-01-03") == FK.to_date("2025.01.03")
    d = FK.to_date("2025.01.03")
    assert FK.date_like(d, "2024-12-31") == "2025-01-03" and FK.date_like(d, "2024년 12월 31일") == "2025년 1월 3일"
    assert FK.date_like(d, "2024년 02월 01일") == "2025년 01월 03일" and FK.add_days("2025.01.03", 30) == "2025.02.02"
    assert FK.to_amount("1,234,000원") == 1234000 and FK.to_amount("-12,000") == -12000 and FK.to_amount("") is None
    assert FK.amount_like(5000000, "1,234,000원") == "5,000,000원" and FK.amount_like(1500, "USD 1,000.00") == "USD 1,500"
    assert FK.amount_like(1500) == "1,500" and FK.won_korean(120000000) == "일억이천만"
    v = {"a": {"b": 1}, "rows": [{"x": 1}]}
    FK.put(v, "a.c", 2)
    assert FK.get(v, "a.c") == 2 and FK.get(v, "rows.0.x") == 1 and FK.get(v, "z", "-") == "-"
    assert random  # noqa: 시험 모듈의 random 은 스크립트 비결정성 예시용
