"""collateral_agreement: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/bank_form_loan.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.bank_form_loan import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _age,
    _korean_amount,
    _legal_bank,
    _plan_personal,
    _special_terms,
    _spouse,
)
from docgen.registry import doc


@doc("collateral_agreement", "근저당권설정계약서", "bank_form", category="internal")
def collateral_agreement(p: Profile, rng: random.Random) -> dict:
    """주택담보대출용 근저당권설정계약서 (개인)."""
    pl = _plan_personal(p)
    mg = pl["mortgage"]
    per, prop = p.person, p.property
    a = prop.address
    max_amt = K.round_to(mg["amount"] * mg["max_ratio"] / 100, 1_000_000)
    scope = rng.choices(["특정근담보", "한정근담보", "포괄근담보"], weights=[50, 45, 5])[0]
    cdate = pl["contract_date"]
    df = rng.choice(["dot", "kor_short"])
    if scope == "특정근담보":
        debt = f"{D(cdate, 'kor_short')}자 대출거래약정서(가계용)"
    elif scope == "한정근담보":
        debt = rng.choice(["가계자금대출(주택담보대출) 거래", "주택자금대출 거래", "가계일반자금대출 및 주택자금대출 거래"])
    else:
        debt = "현재 및 장래에 부담하는 모든 채무"
    # 결산기: 지정형 / 자동확정형 / 장래지정형 (설정자가 선택)
    settle_type = rng.choices(["지정형", "자동확정형", "장래지정형"], weights=[15, 50, 35])[0]
    settle = D(mg["maturity"], df) if settle_type == "지정형" else "정하지 아니함"
    unit = a.detail or f"{prop.floor}층"
    ratio_den = round(prop.land_area * rng.uniform(80, 400), 1)
    data = {
        "bank": p.bank,
        "creditor": {
            "name": _legal_bank(p.bank),
            "branch": p.bank_branch,
        },
        "debtor": {"name": per.name, "address": per.address.road_short},
        "mortgagor": {
            "name": per.name,
            "rrn": per.rrn if rng.random() < 0.5 else K.mask_rrn(per.rrn),
            "address": per.address.road_short,
        },
        "max_amount": won(max_amt, ""),
        "max_amount_korean": _korean_amount(max_amt, rng),
        "scope": scope,
        "scope_handwritten": scope,
        "secured_debt": debt,
        "settlement_type": settle_type,
        "settlement": settle,
        "property": {
            "location": f"{a.jibun_full}" + (f" {a.building_name}" if a.building_name else ""),
            "road_address": a.road_short.split(",")[0],
            "kind": prop.kind,
            "structure": prop.structure,
            "floors": f"{prop.total_floors}층",
            "unit": unit,
            "exclusive_area": f"{prop.exclusive_area:.2f}㎡",
            "land_right": f"소유권대지권 {ratio_den:,}분의 {prop.land_area:.2f}",
            "unique_no": prop.unique_no,
        },
        "rank": rng.choices(["1", "2"], weights=[85, 15])[0],
        "handwritten_confirm": rng.choice(["설명을 듣고 이해함", "충분히 설명듣고 이해함", "확인함"]),
        "contract_date": D(cdate, rng.choice(["kor", "kor_short"])),
        "signature_debtor": per.name,
        "signature_mortgagor": per.name,
    }
    if heavy(rng, 0.25):  # 공동담보(여러 필지·건물) + 본문 조항 → 여러 쪽
        data["joint_collateral"] = _joint_collateral(p, rng)
        data["special_terms"] = _special_terms(_TERMS_MORTGAGE, rng, rng.randint(2, 5))
    if special(rng, "third_party", 0.1):  # 물상보증: 부모가 담보 제공 (채무자 ≠ 근저당권설정자)
        owner = p.father if _age(p, p.person) < 55 else _spouse(p, rng)
        rel = "부" if owner is p.father else "배우자"
        data["mortgagor"] = {"name": owner.name, "rrn": owner.rrn if rng.random() < 0.5 else K.mask_rrn(owner.rrn),
                             "address": owner.address.road_short}
        data["mortgagor_relation"] = rel
        data["signature_mortgagor"] = owner.name
    elif special(rng, "co_mortgagor", 0.15):  # 부부 공동소유 → 공동 근저당권설정자
        sp = _spouse(p, rng)
        data["co_mortgagor"] = {"name": sp.name, "rrn": sp.rrn if rng.random() < 0.5 else K.mask_rrn(sp.rrn),
                                "address": sp.address.road_short, "share": rng.choice(["2분의 1", "2분의 1", "3분의 1"])}
    if special(rng, "handwriting_missing", 0.08):  # 자필기재란 일부 미기재
        data[rng.choice(["scope_handwritten", "handwritten_confirm"])] = None
    return data


_TERMS_MORTGAGE = [
    "설정자는 이 근저당권보다 선순위인 임대차보증금이 있는 경우 그 내역을 은행에 신고하며, 신고하지 아니한 임대차로 인하여 발생한 손해는 설정자가 부담한다.",
    "담보물건에 대한 화재보험은 은행을 제1순위 질권자로 하여 가입하고 보험증권 사본을 은행에 제출한다.",
    "설정자는 담보물건의 재건축·리모델링 등 사업계획이 확정된 경우 지체 없이 은행에 통지한다.",
    "이 근저당권은 공동담보로서 각 담보물건은 피담보채무 전액을 담보하며, 일부 담보물건의 해지는 은행의 승낙을 받아야 한다.",
    "채무자가 피담보채무 전액을 상환한 경우에도 결산기 전까지 근저당권은 존속하며, 설정자의 해지 요청 시 은행은 지체 없이 말소에 협조한다.",
    "담보물건의 소유권을 이전하는 경우 설정자는 사전에 은행에 통지하여야 한다.",
]


def _joint_collateral(p: Profile, rng: random.Random) -> list[dict]:
    """공동담보 목록 (토지 여러 필지 + 건물). 프로필 부동산과 같은 동네의 필지."""
    a = p.property.address
    base = f"{a.sido} {a.sigungu} {a.dong}".replace("  ", " ")
    main = int(a.jibun.split("-")[0])
    out = []
    for i in range(rng.randint(5, 12)):
        kind = rng.choices(["토지", "건물"], weights=[70, 30])[0]
        jb = f"{main + rng.randint(-30, 30)}" + (f"-{rng.randint(1, 40)}" if rng.random() < 0.6 else "")
        if kind == "토지":
            desc = f"{rng.choice(['대', '대', '전', '답', '임야', '잡종지'])} {rng.uniform(80, 1200):,.1f}㎡"
        else:
            desc = f"{rng.choice(['철근콘크리트조', '조적조', '경량철골조'])} {rng.choice(['단독주택', '근린생활시설', '창고'])} {rng.uniform(40, 400):,.2f}㎡"
        out.append({"kind": kind, "location": f"{base} {jb}", "detail": desc,
                    "unique_no": f"{rng.randint(1101, 2843)}-{rng.randint(1990, 2023)}-{rng.randint(1, 99999):06d}"})
    return out
