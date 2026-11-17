"""business_registration_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/business.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.business import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _biz_facts,
    _biz_kind_label,
    _cert_date,
    _reissue,
    _tax_office,
)
from docgen.registry import doc


# ---------------------------------------------------------------------------
# 사업자등록증 (개인)
# ---------------------------------------------------------------------------
@doc("business_registration_certificate", "사업자등록증", "business")
def business_registration_certificate(p: Profile, rng: random.Random) -> dict:
    """세무서가 발급하는 개인사업자 사업자등록증.

    정정 교부(사업장 이전·업종 추가·과세유형 전환·상호 변경)와 공동사업자는 _biz_facts() 의 프로필 고정 사실을 따른다.
    """
    b, fx = p.business, _biz_facts(p)
    events = []
    if fx["moved"]:
        events.append((fx["moved"]["date"], "정정(사업장 소재지 변경)"))
    if fx["added"]:
        events.append((fx["added"]["date"], "정정(업종 추가)"))
    if fx["switch"]:
        events.append((fx["switch"], "정정(과세유형 전환)"))
    if fx["renamed"]:
        events.append((fx["renamed"]["date"], "정정(상호 변경)"))
    reason, issued, _ = _reissue(rng, events, b.established, p.issue_date)
    fd = _cert_date(rng)
    out = {
        "kind": _biz_kind_label(p),
        "biz_no": b.biz_no,
        "trade_name": b.name,
        "name": p.person.name,
        "birth": fd(p.person.birth),
        "opened": fd(b.established),
        "address": b.address.road_full,
        "biz_type": b.biz_type,
        "biz_item": b.biz_item,
        "issue_reason": reason,
        "co_owner": fx["joint"]["name"] if fx["joint"] else None,
        "unit_taxation": "부",
        "issue_date": fd(issued),
        "issuer": _tax_office(b.address),
    }
    if fx["added"] and fx["added"]["date"] <= issued:
        out["sub_kinds"] = [{"biz_type": fx["added"]["biz_type"], "biz_item": fx["added"]["biz_item"]}]
    if rng.random() < 0.4:
        out["einvoice_email"] = rng.choice([p.person.email, b.email])
    return out
