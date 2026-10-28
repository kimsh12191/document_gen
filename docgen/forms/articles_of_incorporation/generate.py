"""articles_of_incorporation: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/corporate.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from __future__ import annotations

from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.corporate import PAR_VALUE, _Doc, _facts, _formal  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("articles_of_incorporation", "정관", "corporate")
def articles_of_incorporation(p: Profile, rng: random.Random) -> dict:
    """주식회사 정관 사본 (원본대조필).

    기본은 첫 쪽(총칙·주식)만 싣고 '중략' 후 부칙. heavy 면 전문(주주총회·이사·감사·계산 장까지, 3~4쪽).
    개정 이력은 프로필 단위(_facts): 상호 변경·목적 추가 등 등기부 변경과 같은 날 개정, 해당 조문 끝에 <개정 …>."""
    c, fx = p.corporation, _facts(p)
    est = c.established
    dates = fx["articles_dates"]
    hist = [f"제정 {D(dates[0], 'dot')}"] + [f"개정 {D(x, 'dot')}" for x in dates[1:]]
    full = heavy(rng, 0.3)
    preferred = any(h["type"] != "보통주" for h in fx["holders"])
    d = {
        "company_name": _formal(c.name),
        "company_name_en": c.name_en,
        "purposes": [f"{i}. {x}" for i, x in enumerate(fx["purposes"], 1)],
        "head_office_city": fx["city"],
        "notice_method": fx["notice"],
        "authorized_shares": f"{fx['authorized']:,}주",
        "par_value": f"금 {PAR_VALUE:,}원",
        "initial_shares": f"{fx['initial_shares']:,}주",
        "effective_date": D(est, "kor_short"),
        "revision_history": hist,
        "revision_effective": [D(x, "kor_short") for x in dates[1:]],
        "ceo_name": p.person.name,
    }
    amended = {}
    if len(fx["names"]) > 1:
        amended["company_name"] = ", ".join(D(dt, "dot") for _, dt in fx["names"][1:])
    if len(fx["purpose_versions"]) > 1:
        amended["purposes"] = ", ".join(D(dt, "dot") for _, dt in fx["purpose_versions"][1:])
    if preferred:
        amended["share_types"] = D(fx["capital_hist"][-1][1] or dates[-1], "dot")
    if amended:
        d["amended"] = amended
    if special(rng, "cert_missing", 0.1):  # 원본대조필 없이 사본만 낸 경우
        d.pop("ceo_name")
    else:
        d["certify_date"] = D(p.issue_date - timedelta(days=rng.randint(0, 7)), rng.choice(["kor", "kor_short", "dot"]))
    if preferred:
        d["preferred"] = "상환전환우선주식"
    d = _Doc(d)
    d.full = full
    return d
