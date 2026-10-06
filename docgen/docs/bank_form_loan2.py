"""은행 자체 서식 — 여신 부속 (대출계약 철회, 적합성·적정성 확인서, 대출상품설명서).

대출 조건은 bank_form_loan.py 의 _plan_personal / _plan_corp 를 그대로 쓴다.
같은 프로필이면 대출신청서·약정서·근저당권설정계약서와 금액·금리·계좌가 일치한다.

서식 구성은 하나은행 공개 서식에서 뽑은 기재란 명세를 따랐다
(add_template/field_specs/대출/{051,061,062,063}.json).
"""
from ..banks import since
from ..registry import doc
from ._common import *  # noqa: F401,F403
from .bank_form_loan import _plan_corp, _plan_personal


def _staff(rng: random.Random) -> dict:
    return {"clerk": K.make_name(rng, rng.choice("MF"))[0],
            "manager": K.make_name(rng, rng.choice("MF"))[0]}


def _date(p: Profile, rng: random.Random) -> str:
    return D(p.issue_date, rng.choice(["kor", "kor", "kor_short", "dot"]))


def _pct(x: float) -> str:
    return f"{x:.2f}%"


# ---------------------------------------------------------------------------
# 대출계약 철회신청서 — 5-06-0681
# ---------------------------------------------------------------------------

WITHDRAW_REASONS = ["대출금리·조건이 기대와 다름", "타 금융기관 조건이 유리함", "자금이 필요 없게 됨",
                    "대출한도가 부족함", "기타"]


@doc("loan_withdrawal_request", "대출계약 철회신청서", "bank_form", category="internal")
def loan_withdrawal_request(p: Profile, rng: random.Random) -> dict:
    """은행여신거래기본약관상 대출계약 철회권(계약서류 받은 날부터 14일 이내)을 행사하는 서식."""
    per = p.person
    pl = _plan_personal(p)
    # 철회는 실행 후 14일 안에만 된다 — 실행일을 작성일 기준으로 되돌려 잡는다
    days = rng.randint(1, 13)
    executed = p.issue_date - timedelta(days=days)
    amount = pl["amount"]
    rate = pl["rate"]["applied"]
    interest = K.round_to(amount * rate / 100 * days / 365, 1)
    stamp = 0 if amount <= 50_000_000 else rng.choice([70_000, 150_000, 350_000])
    setup_cost = rng.choice([0, 0, 180_000, 240_000]) if pl["collateral"] == "부동산" else 0
    return {
        "bank": p.bank,
        "branch": p.bank_branch,
        "borrower": {"name": per.name, "birth": D(per.birth, "dot"),
                     "address": per.address.road_short, "phone": per.mobile},
        "loan": {
            "account": pl["loan_account"],
            "product": pl["product"],
            "amount": K.won(amount),
            "executed": D(executed, "dot"),
            "rate": _pct(rate),
            "days": str(days),
        },
        "reason": rng.choices(WITHDRAW_REASONS, weights=[30, 28, 18, 12, 12])[0],
        "repay": {
            "principal": K.won(amount),
            "interest": K.won(interest),
            "stamp": K.won(stamp),
            "setup_cost": K.won(setup_cost),
            "total": K.won(amount + interest + stamp + setup_cost),
            "date": D(p.issue_date + timedelta(days=rng.choice([0, 0, 1, 2])), "dot"),
            "account": pl["debit_account"].number,
        },
        "keep_loan": rng.choices(["철회함", "중도상환이나 철회하지 않고 대출 유지함"], weights=[88, 12])[0],
        "date": _date(p, rng),
        "signature": per.name,
        "staff": _staff(rng),
    }


# ---------------------------------------------------------------------------
# 적합성·적정성 고객정보 확인서 (개인·개인사업자) — 5-06-0967
# ---------------------------------------------------------------------------

PURPOSES = ["가계자금", "사업자금", "주택자금", "경조자금", "교육비", "의료비", "타 기관 대출금 상환", "기타"]
ASSETS = ["자산없음", "1억원 미만", "1억원 ~ 5억원", "5억원 이상"]
INCOMES = ["소득없음", "5천만원 미만", "5천만원 이상 1억원 미만", "1억원 이상"]
DEBTS = ["부채없음 (잘 모름 포함)", "5천만원 미만", "5천만원 이상 1억원 미만", "1억원 이상"]
REPAY_WAYS = ["근로소득", "사업소득", "임대소득", "연금소득", "기타소득", "담보의 처분(매매, 경매등)"]


def _band(value: int, bands: list[str], cuts: list[int]) -> str:
    for i, c in enumerate(cuts):
        if value < c:
            return bands[i]
    return bands[-1]


@doc("suitability_check", "적합성·적정성 고객정보 확인서(개인)", "bank_form", category="internal")
def suitability_check(p: Profile, rng: random.Random) -> dict:
    """금융소비자보호법 제17·18조에 따라 대출성 상품 권유 전 고객정보를 확인하는 서식."""
    per = p.person
    pl = _plan_personal(p)
    salary = p.employment.annual_salary
    net_assets = p.property.price - pl["amount"]
    purpose = {"mortgage": "주택자금", "jeonse": "주택자금", "credit": rng.choice(["가계자금", "생활자금"])}[pl["kind"]]
    if purpose == "생활자금":
        purpose = "가계자금"
    if pl["purpose"].startswith("타행대출"):
        purpose = "타 기관 대출금 상환"
    ways = ["근로소득"] if salary else []
    if rng.random() < 0.2:
        ways.append("임대소득")
    if pl["kind"] == "mortgage" and rng.random() < 0.25:
        ways.append("담보의 처분(매매, 경매등)")
    return {
        "bank": p.bank,
        "branch": p.bank_branch,
        "customer": {
            "name": per.name,
            "birth": D(per.birth, "dot"),
            "phone": per.mobile,
            "email": per.email,
            "address": per.address.road_short,
        },
        "guardian": rng.choices(["해당사항 없음", "피성년후견인", "피한정후견인"], weights=[97, 2, 1])[0],
        "purpose": purpose,
        "assets": _band(net_assets, ASSETS, [1, 100_000_000, 500_000_000]),
        "collateral_plan": "있음" if pl["collateral"] == "부동산" else "없음",
        "income": _band(salary, INCOMES, [1, 50_000_000, 100_000_000]),
        "debt": _band(pl["amount"], DEBTS, [1, 50_000_000, 100_000_000]),
        "overdue": rng.choices(["연체정보 없음", "연체정보 있음"], weights=[96, 4])[0],
        "credit_score": (f"{rng.randint(720, 980)}점 ({rng.choice(['KCB', 'NICE'])})"
                         if since(p.issue_date, "credit_score") and rng.random() < 0.75 else "잘 모름"),
        "repay_ways": ways or ["기타소득"],
        "bank_use": {
            "soundness": rng.choices(["양호", "보통", "주의"], weights=[72, 24, 4])[0],
            "credit_state": rng.choices(["정상", "정상", "요주의"], weights=[80, 15, 5])[0],
            "plan_review": rng.choice(["상환능력 적정", "상환능력 양호", "담보가치 범위 내 적정"]),
        },
        "date": _date(p, rng),
        "signature": per.name,
        "staff": _staff(rng),
    }


# ---------------------------------------------------------------------------
# 적합성·적정성 고객정보 확인서 (법인) — 5-06-0970
# ---------------------------------------------------------------------------

CORP_PRO = ["일반금융소비자", "주권을 국내외 증권시장에 상장한 법인",
            "법률에 의해 공제사업을 영위하는 법인·조합·단체", "금융회사", "국가 및 지방자치단체"]
CORP_BANDS = ["5억원 미만", "5억원 이상 10억원 미만", "10억원 이상"]
CORP_PROFIT = ["전년도 순이익 없음", "1억원 미만", "1억원 이상 5억원 미만", "5억원 이상"]
CORP_REPAY = ["사업소득", "임대소득", "금융소득", "기타소득", "담보의 처분(매매, 경매 등)"]


@doc("suitability_check_corp", "적합성·적정성 고객정보 확인서(법인)", "bank_form", category="internal")
def suitability_check_corp(p: Profile, rng: random.Random) -> dict:
    """법인 고객의 대출성 상품 권유 전 적합성·적정성 판단을 위한 고객정보 확인서."""
    c = p.corporation
    pl = _plan_corp(p)
    profit = K.round_to(c.revenue * rng.uniform(0.01, 0.09), 1_000_000)
    assets = K.round_to(c.revenue * rng.uniform(0.3, 1.1), 1_000_000)
    ways = ["사업소득"]
    if rng.random() < 0.25:
        ways.append("임대소득")
    if pl.get("collateral") == "부동산" and rng.random() < 0.3:
        ways.append("담보의 처분(매매, 경매 등)")
    return {
        "bank": p.bank,
        "branch": p.bank_branch,
        "company": {
            "name": c.name,
            "biz_no": c.biz_no,
            "ceo": c.ceo.name,
            "employees": f"{c.employees}명",
            "phone": c.phone,
            "ceo_phone": c.ceo.mobile,
            "email": c.email,
            "address": c.address.road_short,
        },
        "consumer_type": rng.choices(CORP_PRO, weights=[86, 3, 2, 5, 4])[0],
        "purpose": "시설자금" if "시설" in pl["kind"] else "운전자금",
        "assets": _band(assets, CORP_BANDS, [500_000_000, 1_000_000_000]),
        "collateral_plan": rng.choices(["있음", "없음", "은행과 상담후 담보제공 여부 결정 예정"],
                                       weights=[55, 25, 20])[0],
        "revenue": _band(c.revenue, CORP_BANDS, [500_000_000, 1_000_000_000]),
        "profit": _band(profit, CORP_PROFIT, [1, 100_000_000, 500_000_000]),
        "debt": _band(pl["amount"], CORP_BANDS, [500_000_000, 1_000_000_000]),
        "overdue": rng.choices(["연체정보 없음", "연체정보 있음"], weights=[95, 5])[0],
        "impairment": rng.choices(["비해당", "해당"], weights=[94, 6])[0],
        "repay_ways": ways,
        "bank_use": {
            "soundness": rng.choices(["양호", "보통", "주의"], weights=[70, 26, 4])[0],
            "credit_state": rng.choices(["정상", "정상", "요주의"], weights=[80, 15, 5])[0],
            "plan_review": rng.choice(["영업현금흐름으로 상환 가능", "상환능력 적정", "담보가치 범위 내 적정"]),
        },
        "date": _date(p, rng),
        "signature": c.name,
        "staff": _staff(rng),
    }


# ---------------------------------------------------------------------------
# 대출상품설명서(권유용) — 3-06-0148
# ---------------------------------------------------------------------------


@doc("loan_product_description", "대출상품설명서(권유용)", "bank_form", category="internal")
def loan_product_description(p: Profile, rng: random.Random) -> dict:
    """금융소비자보호법 제19조 설명의무 이행을 위해 대출 권유 단계에서 교부하는 상품설명서."""
    per = p.person
    pl = _plan_personal(p)
    rate = pl["rate"]
    late = 3.0 if since(p.issue_date, "late_3pct") else rng.choice([6.0, 7.0, 8.0])
    total_term = pl["term_years"]
    return {
        "bank": p.bank,
        "branch": p.bank_branch,
        "customer": {"name": per.name, "birth": D(per.birth, "dot"), "phone": per.mobile},
        "product": {
            "name": pl["product"],
            "subject": pl["subject"],
            "purpose": pl["purpose"],
            "amount": K.won(pl["amount"]),
            "term": f"{total_term}년",
            "repayment": pl["repayment"],
            "collateral": pl["collateral"],
            "start_date": D(pl["start_date"], "dot"),
            "maturity": D(pl["maturity"], "dot"),
        },
        "rate": {
            "type": pl["rate_type"],
            "base_name": rate["base_name"],
            "base": _pct(rate["base"]),
            "spread": _pct(rate["spread"]),
            "pref": _pct(rate["pref"]),
            "applied": _pct(rate["applied"]),
            "late": f"연체이자율 = 약정이율 + {late:.1f}%p (최고 연 {min(rate['applied'] + late, 15.0):.2f}%)",
        },
        "fees": [
            {"name": "중도상환해약금", "amount": f"{pl['prepay_fee']:.2f}% × 잔여일수/대출기간"},
            {"name": "인지세", "amount": "대출금액에 따라 0 ~ 350,000원 (은행과 고객이 각 50% 부담)"},
            {"name": "근저당권 설정비용", "amount": "등록면허세·지방교육세는 고객, 법무사 수수료는 은행 부담"
                                                if pl["collateral"] == "부동산" else "해당 없음"},
        ],
        "prepay_free": "대출일로부터 3년 경과 시 면제",
        "rate_cut": ("취업·승진·소득증가·신용평점 상승 등 신용상태 개선 시 금리인하를 요구할 수 있습니다"
                     if since(p.issue_date, "rate_cut_law") else "신용상태 개선 시 금리인하를 요구할 수 있습니다"),
        "withdraw": ("계약서류를 받은 날 또는 대출을 받은 날부터 14일 이내에 철회할 수 있습니다"
                     if since(p.issue_date, "withdraw") else "해당 없음"),
        "risks": [
            "변동금리 상품은 지표금리 상승 시 이자 부담이 늘어날 수 있습니다.",
            "원리금을 연체하면 연체이자가 부과되고 신용평점이 하락하며, 기한의 이익을 잃을 수 있습니다.",
            "담보 제공 시 채무를 갚지 못하면 담보물이 처분될 수 있습니다.",
        ],
        "explained_by": K.make_name(rng, rng.choice("MF"))[0],
        "handwritten": "설명을 듣고 이해하였음",
        "date": _date(p, rng),
        "signature": per.name,
        "staff": _staff(rng),
    }
