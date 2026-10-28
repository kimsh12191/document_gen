"""business_registration_proof: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/business.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.business import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _biz_facts,
    _biz_kind_label,
    _hometax_no,
    _industry,
    _tax_office,
)
from docgen.registry import doc


def _purpose(rng: random.Random, p: Profile) -> tuple[str, str]:
    return (rng.choice(["금융기관 제출", "대출 신청", "금융기관 제출용", "은행 제출"]),
            rng.choice([p.bank, f"{p.bank} {p.bank_branch}", "금융기관"]))


# ---------------------------------------------------------------------------
# 사업자등록증명 (홈택스)
# ---------------------------------------------------------------------------
@doc("business_registration_proof", "사업자등록증명", "business")
def business_registration_proof(p: Profile, rng: random.Random) -> dict:
    """홈택스에서 발급한 개인사업자 사업자등록증명. 부업종·공동사업자는 _biz_facts() 를 따른다."""
    b, fx = p.business, _biz_facts(p)
    _, _, code, _ = _industry(b)
    kinds = [{"biz_type": b.biz_type, "biz_item": b.biz_item, "code": code, "main": "주업종"}]
    if fx["added"]:
        a = fx["added"]
        kinds.append({"biz_type": a["biz_type"], "biz_item": a["biz_item"], "code": a["code"], "main": "부업종"})
    purpose, submit_to = _purpose(rng, p)
    fmt = rng.choice(["kor", "dash"])
    registered = b.established + timedelta(days=rng.randint(-10, 15))
    out = {
        "issue_no": _hometax_no(rng),
        "trade_name": b.name,
        "biz_no": b.biz_no,
        "name": p.person.name,
        "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.8 else p.person.rrn,
        "address": b.address.road_full,
        "opened": D(b.established, fmt),
        "registered": D(registered, fmt),
        "kind": _biz_kind_label(p),
        "kinds": kinds,
        "joint": "해당" if fx["joint"] else "해당없음",
        "purpose": purpose,
        "submit_to": submit_to,
        "issue_date": D(p.issue_date, "kor"),
        "issuer": _tax_office(b.address),
    }
    if fx["joint"]:
        j = fx["joint"]
        out["co_owners"] = [
            {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn), "share": f"{j['own_share']}%", "role": "대표공동사업자"},
            {"name": j["name"], "rrn": K.mask_rrn(j["rrn"]), "share": f"{j['share']}%", "role": "공동사업자"},
        ]
    return out
