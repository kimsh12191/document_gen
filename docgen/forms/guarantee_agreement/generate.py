"""guarantee_agreement: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/bank_form_loan.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.bank_form_loan import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _add_years,
    _legal_bank,
    _plan_corp,
    _special_terms,
)
from docgen.registry import doc


@doc("guarantee_agreement", "보증약정서", "bank_form", category="internal")
def guarantee_agreement(p: Profile, rng: random.Random) -> dict:
    """법인 여신에 대한 대표이사 보증약정서."""
    c = p.corporation
    per = p.person
    pl = _plan_corp(p)
    method = rng.choices(["특정채무보증", "특정근보증", "한정근보증"], weights=[45, 20, 35])[0]
    max_amt = K.round_to(pl["amount"] * pl["guarantee_ratio"] / 100, 1_000_000)
    df = rng.choice(["dot", "kor_short"])
    if method == "특정채무보증":
        debt = f"{D(pl['contract_date'], 'kor_short')}자 {pl['kind']} 금 {won(pl['amount'])}"
        period = f"{D(pl['start_date'], df)} ~ {D(pl['maturity'], df)}"
    elif method == "특정근보증":
        debt = f"{D(pl['contract_date'], 'kor_short')}자 여신거래약정서(기업용)에 의한 {pl['kind']} 거래"
        period = f"{D(pl['start_date'], df)} ~ {D(_add_years(pl['start_date'], max(3, pl['term_years'])), df)}"
    else:
        debt = rng.choice(["기업일반자금대출 거래", "기업자금대출 거래", "운전자금대출 및 시설자금대출 거래",
                           f"{pl['kind']} 거래"])
        period = f"{D(pl['start_date'], df)} ~ {D(_add_years(pl['start_date'], 3), df)}"
    amt_kr = K.won_korean(max_amt)
    data = {
        "bank": p.bank,
        "creditor": _legal_bank(p.bank),
        "branch": p.bank_branch,
        "debtor": {"name": c.name, "biz_no": c.biz_no, "ceo": c.ceo.name, "address": c.address.road_short},
        "guarantor": {
            "name": per.name,
            "rrn": K.mask_rrn(per.rrn) if rng.random() < 0.6 else per.rrn,
            "address": per.address.road_short,
            "phone": per.mobile,
            "relation": rng.choice(["대표이사(실제경영자)", "대표이사"]),
        },
        "method": method,
        "max_amount": won(max_amt, ""),
        "max_amount_korean": f"금 {amt_kr}원정",
        "period": period,
        "secured_debt": debt,
        "handwritten": {
            "max_amount": f"금 {amt_kr}원정",
            "method": method,
            "name": per.name,
            "confirm": rng.choice(["설명을 듣고 이해함", "충분히 설명듣고 이해함", "확인함"]),
        },
        "explained": "예",
        "contract_date": D(pl["contract_date"], rng.choice(["kor", "kor_short"])),
        "signature": per.name,
    }
    if heavy(rng, 0.25):  # 본문 조항 + 특약 → 여러 쪽
        data["special_terms"] = _special_terms(_TERMS_GUARANTEE, rng, rng.randint(2, 4),
                                               debt=rng.choice([200, 300]), amt=won(max_amt))
    if special(rng, "multi_guarantor", 0.2):  # 연대보증인 다수 (공동대표·최대주주 등)
        others = rng.sample(p.directors, rng.randint(1, min(2, len(p.directors))))
        data["co_guarantors"] = [{"name": g.name, "rrn": K.mask_rrn(g.rrn) if rng.random() < 0.6 else g.rrn,
                                  "address": g.address.road_short, "phone": g.mobile,
                                  "relation": rng.choice(["이사", "공동대표이사", "최대주주(이사)", "감사"])} for g in others]
    if special(rng, "handwriting_missing", 0.1):  # 자필기재란 일부 미기재
        for k in rng.sample(["confirm", "method", "name"], rng.randint(1, 2)):
            data["handwritten"][k] = None
    if special(rng, "no_check", 0.08):
        data["explained"] = None
    return data


_TERMS_GUARANTEE = [
    "보증인은 보증기간 중 보증인의 재산에 관한 중대한 변동이 있는 경우 지체 없이 은행에 통지한다.",
    "공동보증인이 있는 경우 각 보증인은 보증채무최고액 {amt} 범위에서 채무 전액에 대하여 연대하여 책임을 진다.",
    "보증인이 채무자의 대표이사직에서 퇴임한 경우 보증인은 은행에 서면으로 보증계약의 해지를 청구할 수 있으며, 은행은 새로운 보증인 또는 담보를 채무자에게 요구할 수 있다.",
    "채무자의 부채비율이 {debt}%를 초과하는 경우 은행은 보증인에게 그 사실을 통지한다.",
    "보증인은 은행의 동의 없이 보증인 소유 주요 재산을 처분하거나 담보로 제공하는 경우 은행에 사전 통지한다.",
]
