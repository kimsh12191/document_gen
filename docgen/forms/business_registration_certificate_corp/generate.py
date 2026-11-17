"""business_registration_certificate_corp: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/business.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.business import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _SECONDARY,
    _cert_date,
    _prng,
    _reissue,
    _tax_office,
)
from docgen.registry import doc


# ---------------------------------------------------------------------------
# 사업자등록증 (법인)
# ---------------------------------------------------------------------------
def _corp_facts(p: Profile) -> dict | None:
    """법인 등기 이력(corporate.py _facts: 본점 이전·상호 변경·공동대표). 가져올 수 없으면 None."""
    try:
        from docgen.docs.corporate import _facts
        return _facts(p)
    except Exception:  # noqa: BLE001 - 다른 그룹 모듈 변경에 영향받지 않게
        return None


@doc("business_registration_certificate_corp", "사업자등록증(법인사업자)", "business")
def business_registration_certificate_corp(p: Profile, rng: random.Random) -> dict:
    """세무서가 발급하는 법인사업자 사업자등록증.

    본점 이전·상호 변경·공동대표 취임은 법인등기부(corporate._facts)와 같은 날짜를 쓰고, 등기 뒤 1~4주 안에 정정 교부.
    """
    c = p.corporation
    cf = _corp_facts(p) or {}
    pad = lambda d: d + timedelta(days=rng.randint(7, 25)) if d else None  # noqa: E731
    events = []
    offices = cf.get("offices") or []
    if len(offices) > 1 and offices[-1][1]:
        events.append((pad(offices[-1][1]), "정정(본점 이전)"))
    names = cf.get("names") or []
    if len(names) > 1 and names[-1][1]:
        events.append((pad(names[-1][1]), "정정(상호 변경)"))
    co = cf.get("co_ceo")
    if co and co.get("start") and co["start"] > c.established:
        events.append((pad(co["start"]), "정정(대표자 변경)"))
    added = None
    ra = _prng(p, "corp-added")
    if special(ra, "corp_biz_added", 0.12):
        lo = c.established + timedelta(days=300)
        if lo < p.issue_date - timedelta(days=30):
            t, i, code = ra.choice([s for s in _SECONDARY if s[1] != c.biz_item])
            added = {"date": rand_date(ra, lo, p.issue_date - timedelta(days=30)), "biz_type": t, "biz_item": i}
            events.append((added["date"], "정정(업종 추가)"))
    reason, issued, _ = _reissue(rng, events, c.established, p.issue_date)
    fd = _cert_date(rng)
    out = {
        "biz_no": c.biz_no,
        "corp_name": c.name,
        "ceo": p.person.name,
        "opened": fd(c.established),
        "corp_reg_no": c.corp_no,
        "address": c.address.road_full,
        "head_office": c.address.road_full,
        "biz_type": c.biz_type,
        "biz_item": c.biz_item,
        "issue_reason": reason,
        "unit_taxation": "부",
        "issue_date": fd(issued),
        "issuer": _tax_office(c.address),
    }
    if co and co.get("person") is not None and (not co.get("start") or co["start"] <= issued):
        out["co_ceo"] = co["person"].name
    if added and added["date"] <= issued:
        out["sub_kinds"] = [{"biz_type": added["biz_type"], "biz_item": added["biz_item"]}]
    if rng.random() < 0.5:
        out["einvoice_email"] = c.email
    return out
