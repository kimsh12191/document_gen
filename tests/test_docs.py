"""모든 서류가 여러 프로필에서 예외 없이 렌더링되고, GT 가 올바르게 만들어지는지 검사한다."""
import json
import re

import pytest

from docgen import korean as K
from docgen.entities import make_profile
from docgen.registry import GROUPS, SCENARIOS, load_all
from docgen.render import render, to_nested

REG = load_all()
SEEDS = range(8)


@pytest.mark.parametrize("doc_id", sorted(REG))
def test_renders_and_records_fields(doc_id):
    spec = REG[doc_id]
    assert spec.group in GROUPS
    assert spec.category in ("external", "internal")
    for seed in SEEDS:
        html, fields, data = render(spec, make_profile(seed), seed)
        assert fields, f"{doc_id}: f() 로 기록된 필드가 없음"
        keys = [f["key"] for f in fields]
        assert len(keys) == len(set(keys))
        for f in fields:
            assert f'data-field="{f["key"]}"' in html
        json.dumps(to_nested(fields), ensure_ascii=False)
        if spec.sample_mark:
            assert "sample-mark" in html


def test_scenarios_reference_registered_docs():
    for name, (_, ids) in SCENARIOS.items():
        missing = [i for i in ids if i not in REG]
        assert not missing, f"{name}: {missing}"


def test_profile_is_deterministic():
    a, b = make_profile(42), make_profile(42)
    assert a.person.name == b.person.name and a.person.rrn == b.person.rrn
    html1, f1, _ = render(REG["employment_certificate"], a, 42)
    html2, f2, _ = render(REG["employment_certificate"], b, 42)
    assert html1 == html2 and f1 == f2


def test_rrn_checksum():
    for seed in range(50):
        rrn = make_profile(seed).person.rrn
        digits = rrn.replace("-", "")
        s = sum(int(c) * w for c, w in zip(digits[:12], [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]))
        assert (11 - s % 11) % 10 == int(digits[12])
        assert re.fullmatch(r"\d{6}-[1-4]\d{6}", rrn)


def test_won_korean():
    assert K.won_korean(120_000_000) == "일억이천만"
    assert K.won_korean(1_234_567) == "일백이십삼만사천오백육십칠"
    assert K.won_korean(214_000_000) == "이억일천사백만"
    assert K.won_korean(10_000) == "일만"
    assert K.won_korean(350_000_000, hanja=True) == "參億伍阡萬"


def test_to_nested_lists():
    fields = [{"key": "a.b", "value": "1"}, {"key": "items.0.x", "value": "2"}, {"key": "items.1.x", "value": "3"}]
    assert to_nested(fields) == {"a": {"b": "1"}, "items": [{"x": "2"}, {"x": "3"}]}


# ---------------------------------------------------------------------------
# 은행별 서식 (하나은행, 옛 은행 외환은행·KEB하나은행)
# ---------------------------------------------------------------------------

from docgen.banks import BRANDS, LEGACY, bank_view, form_bank, supports  # noqa: E402

BANK_FORMS = [s.id for s in REG.values() if s.group == "bank_form"]


def _rrn_ok(v: str) -> bool:
    d = v.replace("-", "")
    s = sum(int(c) * w for c, w in zip(d[:12], [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]))
    return (11 - s % 11) % 10 == int(d[12])


@pytest.mark.parametrize("bank", LEGACY)
def test_legacy_bank_view_moves_dates_into_era(bank):
    era = BRANDS[bank].era
    for seed in range(20):
        p = make_profile(seed)
        q = bank_view(p, bank)
        assert q.bank == bank and q.accounts[0].bank == bank
        assert era[0] <= q.issue_date <= era[1]
        assert q.person.rrn[:6] == q.person.birth.strftime("%y%m%d") and _rrn_ok(q.person.rrn)
        assert q.employment.hire_date <= q.issue_date
        assert q.person.birth.year + 18 <= q.issue_date.year


@pytest.mark.parametrize("bank", ["하나은행", *LEGACY])
@pytest.mark.parametrize("doc_id", BANK_FORMS)
def test_bank_forms_render_for_bank(bank, doc_id):
    if not supports(bank, doc_id):
        pytest.skip("그 시기에 없던 서식")
    p = make_profile(5, None if bank in LEGACY else bank)
    p.extra["form_bank"] = bank
    html, fields, _ = render(REG[doc_id], p, 5)
    shown = {f["key"]: f["value"] for f in fields}
    assert shown.get("bank", shown.get("bank.name")) == bank
    if bank == "외환은행":
        assert "금융소비자 보호에 관한 법률" not in html and "모바일신분증" not in html
    if doc_id == "credit_agreement":
        assert BRANDS[bank].legal in html


def test_default_mix_includes_legacy_banks_outside_scenarios():
    banks = set()
    for seed in range(60):
        p = make_profile(seed)
        _, fields, _ = render(REG["credit_agreement"], p, seed)
        banks.add(next(f["value"] for f in fields if f["key"] == "bank"))
    assert {"외환은행", "KEB하나은행"} <= banks
    for seed in range(60):  # 시나리오는 서류 간 일관성을 위해 프로필 은행 그대로
        p = make_profile(seed)
        p.extra["scenario"] = "mortgage"
        assert form_bank(p, "credit_agreement") == p.bank
