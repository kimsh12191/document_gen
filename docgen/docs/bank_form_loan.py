"""은행 자체 여신 서식 (대출신청서, 여신거래약정서, 근저당권설정계약서, 보증약정서, 자동이체 신청서).

같은 프로필로 만든 여신 서류끼리 대출 금액·기간·금리·계좌가 맞도록, 핵심 조건은
프로필 seed 에서 파생한 별도 난수(_plan_personal / _plan_corp)로 정한다.
서류별 표기 차이(날짜 포맷, 문구 선택 등)만 각 함수의 rng 로 만든다.
"""
from ..banks import brand, since
from ..registry import doc
from ._common import *  # noqa: F401,F403

# ---------------------------------------------------------------------------
# 내부 헬퍼
# ---------------------------------------------------------------------------

_LOAN_ACCT_FMT = {"국민은행": "###-##-####-###", "신한은행": "###-###-######", "우리은행": "####-###-######",
                  "하나은행": "###-######-#####", "농협은행": "###-####-####-##", "기업은행": "###-######-##-###",
                  "SC제일은행": "###-##-######", "외환은행": "###-######-###", "KEB하나은행": "###-######-#####"}


def _add_years(d: date, n: int) -> date:
    try:
        return d.replace(year=d.year + n)
    except ValueError:  # 2/29
        return d.replace(year=d.year + n, day=28)


def _add_months(d: date, n: int) -> date:
    y, m = divmod(d.year * 12 + d.month - 1 + n, 12)
    return date(y, m + 1, min(d.day, 28))


def _digits(r: random.Random, fmt: str, head: str = "") -> str:
    out = list(head)
    for c in fmt[len(head):]:
        out.append(str(r.randint(0, 9)) if c == "#" else c)
    return "".join(out)


def _loan_acct(r: random.Random, bank: str) -> str:
    fmt = _LOAN_ACCT_FMT.get(bank, "###-##-######")
    return _digits(r, fmt, head=r.choice(["7", "8", "5", "2"]))


def _rate(x: float) -> str:
    return f"{x:.2f}%"


def _pa(x: float) -> str:
    return f"연 {x:.2f}%"


def _korean_amount(n: int, rng: random.Random, style: str | None = None) -> str:
    """'금 일억이천만원정' 형태."""
    style = style or rng.choice(["금 {}원정", "금 {}원整", "일금 {}원정"])
    return style.format(K.won_korean(n))


def _pmt(principal: int, annual_rate: float, months: int) -> int:
    i = annual_rate / 100 / 12
    if i == 0:
        return principal // months
    return int(round(principal * i / (1 - (1 + i) ** -months), -1))


def _home_phone(r: random.Random, p: Profile) -> str:
    return K.landline(r, p.person.address.sido)


def _plan_personal(p: Profile) -> dict:
    """개인 고객의 대출 조건 (같은 프로필의 신청서/약정서/근저당/자동이체에서 공통)."""
    r = random.Random(f"bank_form_loan:personal:{p.seed}")
    sal = p.employment.annual_salary
    prop = p.property
    kind = r.choices(["credit", "mortgage", "jeonse"], weights=[35, 45, 20])[0]
    kind = p.extra.get("loan_kind", kind)  # 시나리오가 대출 종류를 정하면 그것을 따른다

    # 주택담보 조건은 근저당권설정계약서에서 항상 쓰므로 미리 계산한다.
    ltv = r.uniform(0.4, 0.7)
    m_amount = K.round_to(min(prop.price * ltv, sal * r.uniform(4.0, 7.0)), 1_000_000)
    m_amount = max(m_amount, 30_000_000)
    m_purpose = r.choice(["주택구입자금", "주택구입자금", "생활안정자금", "타행대출 상환(대환)"])
    mortgage = {
        "amount": m_amount,
        "term_years": r.choice([30, 30, 35, 40]),
        "repayment": r.choice(["원리금균등분할상환", "원리금균등분할상환", "원금균등분할상환"]),
        "rate_type": r.choice(["고정금리", "변동금리", "혼합금리"]),
        "subject": "주택담보대출",
        "purpose": m_purpose,
        "product": {"주택구입자금": r.choice(["주택구입자금대출", "주택담보대출", "아파트 담보대출"]),
                    "생활안정자금": r.choice(["생활안정자금 주택담보대출", "주택담보대출"]),
                    "타행대출 상환(대환)": r.choice(["주택담보 대환대출", "주택담보대출"])}[m_purpose],
        "collateral": "부동산",
        "max_ratio": r.choice([120, 120, 120, 130]),
    }
    if kind == "mortgage":
        plan = dict(mortgage)
    elif kind == "credit":
        limit_loan = r.random() < 0.35
        amt = K.round_to(sal * r.uniform(0.5, 1.4), 1_000_000)
        amt = max(10_000_000, min(amt, 150_000_000))
        if limit_loan:
            plan = {"amount": amt, "term_years": 1, "repayment": "만기일시상환", "rate_type": "변동금리",
                    "subject": "가계일반자금대출(한도)", "product": r.choice(["직장인 마이너스통장", "직장인 신용한도대출"]),
                    "purpose": r.choice(["생활자금", "생계자금", "기타 생활자금"])}
        else:
            ty = r.choice([1, 3, 5])
            plan = {"amount": amt, "term_years": ty,
                    "repayment": "만기일시상환" if ty == 1 else r.choice(["원리금균등분할상환", "원금균등분할상환"]),
                    "rate_type": r.choice(["고정금리", "변동금리"]),
                    "subject": "가계일반자금대출", "product": r.choice(["직장인 신용대출", "우량직장인 신용대출",
                                                                   "급여이체 신용대출", "전문직 신용대출"]),
                    "purpose": r.choice(["생활자금", "주택 임차자금 보충", "교육비", "의료비", "타행대출 상환(대환)"])}
        plan["collateral"] = "신용"
    else:  # jeonse
        amt = K.round_to(min(prop.lease_deposit * 0.8, 400_000_000), 1_000_000)
        plan = {"amount": max(amt, 20_000_000), "term_years": 2, "repayment": "만기일시상환",
                "rate_type": r.choice(["변동금리", "고정금리"]), "subject": "전세자금대출",
                "product": r.choice(["전세자금대출", "주택금융공사 전세자금보증대출", "HUG 전세보증금대출"]),
                "purpose": "주택 임차보증금", "collateral": "보증",
                "guarantor": r.choice(["한국주택금융공사", "주택도시보증공사(HUG)", "서울보증보험(SGI)"])}
        if p.issue_date < date(2015, 7, 1):  # 주택도시보증공사 출범(2015.7) 전
            plan["product"] = plan["product"].replace("HUG 전세보증금대출", "전세자금대출")
            plan["guarantor"] = plan["guarantor"].replace("주택도시보증공사(HUG)", "대한주택보증")
    plan["kind"] = kind
    plan["mortgage"] = mortgage

    # 금리
    def rate_set(rate_type: str, kind_: str):
        if rate_type == "고정금리":
            base_name, base = r.choice([("금융채 5년물(AAA)", r.uniform(2.9, 3.6)), ("금융채 3년물(AAA)", r.uniform(2.7, 3.4))])
        elif rate_type == "혼합금리":
            base_name, base = "금융채 5년물(AAA)", r.uniform(2.9, 3.6)
        else:
            base_name, base = r.choice([("신규취급액기준 COFIX 6개월", r.uniform(2.6, 3.6)),
                                        ("신잔액기준 COFIX 6개월", r.uniform(2.6, 3.3)),
                                        ("CD 91일물", r.uniform(2.5, 3.5)), ("금융채 6개월물(AAA)", r.uniform(2.6, 3.4))])
        base = round(base, 2)
        spread = round(r.uniform(1.2, 2.2) if kind_ in ("mortgage", "jeonse") else r.uniform(1.8, 3.6), 2)
        pref = round(r.choice([0, 0.1, 0.2, 0.3, 0.5]), 2)
        applied = round(base + spread - pref, 2)
        return {"base_name": base_name, "base": base, "spread": spread, "pref": pref, "applied": applied}

    plan["rate"] = rate_set(plan["rate_type"], kind)
    mortgage["rate"] = plan["rate"] if kind == "mortgage" else rate_set(mortgage["rate_type"], "mortgage")

    # 날짜/계좌
    plan["apply_date"] = p.issue_date
    plan["contract_date"] = p.issue_date + timedelta(days=r.randint(2, 12))
    plan["start_date"] = plan["contract_date"] + timedelta(days=r.choice([0, 0, 1, 3, 7]))
    plan["maturity"] = _add_years(plan["start_date"], plan["term_years"])
    mortgage["start_date"] = plan["start_date"]
    mortgage["maturity"] = _add_years(plan["start_date"], mortgage["term_years"])
    plan["pay_day"] = r.choice([5, 10, 15, 20, 21, 25, plan["start_date"].day])
    plan["loan_account"] = _loan_acct(r, p.bank)
    mortgage["loan_account"] = plan["loan_account"] if kind == "mortgage" else _loan_acct(r, p.bank)
    own = [a for a in p.accounts if a.bank == p.bank] or p.accounts
    plan["debit_account"] = own[0]
    # 2025.1.13 중도상환수수료 개편 이후 수준 (주담대 0.56~0.74%, 변동 신용대출 0.1%대).
    # 그 전(옛 은행 서식 시기)에는 담보 1.2~1.5%, 신용 0.7~1.0% 수준.
    if p.issue_date >= date(2025, 1, 13):
        m_fees = [0.56, 0.58, 0.65, 0.66, 0.74]
        credit_fee = r.choice([0.1, 0.11, 0.14, 0.17]) if plan["rate_type"] == "변동금리" else r.choice([0.4, 0.5, 0.6, 0.7])
        j_fees = [0.5, 0.6, 0.65]
    else:
        m_fees = [1.2, 1.4, 1.5, 1.5]
        credit_fee = r.choice([0.7, 0.8, 1.0])
        j_fees = [0.8, 1.0, 1.2]
    plan["prepay_fee"] = {"mortgage": r.choice(m_fees), "credit": credit_fee, "jeonse": r.choice(j_fees)}[kind]
    if plan["subject"].endswith("(한도)"):
        plan["prepay_fee"] = 0.0
    mortgage["prepay_fee"] = plan["prepay_fee"] if kind == "mortgage" else r.choice(m_fees)
    return plan


def _plan_corp(p: Profile) -> dict:
    """법인 여신 조건 (기업여신 신청서/약정서/보증약정서에서 공통)."""
    r = random.Random(f"bank_form_loan:corp:{p.seed}")
    c = p.corporation
    kind = r.choice(["일반자금대출", "일반자금대출", "시설자금대출", "한도대출"])
    amt = K.round_to(c.revenue * r.uniform(0.012, 0.07), 10_000_000)
    amt = max(50_000_000, min(amt, r.choice([1_500_000_000, 2_000_000_000, 3_000_000_000, 5_000_000_000])))
    if kind == "시설자금대출":
        years = r.choice([5, 7, 10])
        grace = r.choice([1, 2])
        repay = f"{grace}년 거치 후 {years - grace}년 원금균등분할상환"
        purpose = r.choice(["생산설비 구입", "공장 신축자금", "사옥 매입자금", "기계장치 도입"])
        product = "기업시설자금대출"
    elif kind == "한도대출":
        years = 1
        repay = "만기일시상환(한도 내 수시인출·상환)"
        purpose = r.choice(["운전자금(결제자금)", "경상운전자금", "원자재 구매대금 결제"])
        product = r.choice(["기업일반자금 한도대출", "기업당좌대출", "운전자금 한도대출"])
    else:
        years = r.choice([1, 1, 2, 3])
        repay = "만기일시상환" if years == 1 else r.choice(["만기일시상환", "원금균등분할상환", f"{years * 12}개월 원리금균등분할상환"])
        purpose = r.choice(["운전자금(원자재 구입)", "운전자금(인건비 등 경상비)", "매출채권 회수 지연에 따른 운전자금", "운전자금"])
        product = r.choice(["기업일반자금대출", "중소기업 운전자금대출", "기업일반운전자금대출"])
    collateral = r.choice(["신용", "부동산", "보증서", "보증서"])
    if collateral == "부동산":
        col_detail = f"본사 사옥({c.address.region} 소재) 근저당권 설정, 채권최고액 {won(K.round_to(amt * 1.2, 10_000_000))}"
    elif collateral == "보증서":
        org = r.choice(["신용보증기금", "기술보증기금", f"{K.sido_short(c.address.sido)}신용보증재단"])
        col_detail = f"{org} 보증서 (보증비율 {r.choice([85, 90, 100])}%)"
    else:
        col_detail = "신용 (대표이사 연대보증)"
    base_name, base = r.choice([("CD 91일물", r.uniform(2.5, 3.5)), ("금융채 1년물(AAA)", r.uniform(2.6, 3.4)),
                                ("금융채 3개월물(AAA)", r.uniform(2.5, 3.3)), ("시장금리(MOR) 6개월", r.uniform(2.6, 3.4))])
    base = round(base, 2)
    spread = round(r.uniform(1.4, 3.4), 2)
    pref = round(r.choice([0, 0, 0.1, 0.2, 0.3]), 2)
    apply_date = p.issue_date
    contract = apply_date + timedelta(days=r.randint(3, 14))
    start = contract + timedelta(days=r.choice([0, 0, 1, 3]))
    corp_acct = _digits(r, _LOAN_ACCT_FMT.get(p.bank, "###-##-######"), head="1")
    return {
        "kind": kind, "product": product, "amount": amt, "term_years": years, "repayment": repay,
        "purpose": purpose, "collateral": collateral, "collateral_detail": col_detail,
        "rate": {"base_name": base_name, "base": base, "spread": spread, "pref": pref,
                 "applied": round(base + spread - pref, 2)},
        "rate_type": "변동금리" if r.random() < 0.75 else "고정금리",
        "apply_date": apply_date, "contract_date": contract, "start_date": start,
        "maturity": _add_years(start, years), "pay_day": r.choice([10, 15, 20, 25, 30]),
        "loan_account": _loan_acct(r, p.bank), "debit_account": corp_acct,
        "prepay_fee": 0.0 if kind == "한도대출" else r.choice([0.5, 0.6, 0.7, 0.8]),
        "guarantee_ratio": r.choice([120, 120, 130]),
        "contact": K.make_name(r, r.choice("MF"))[0],
        "contact_pos": r.choice(["재무팀 과장", "경영지원팀 차장", "재무팀 대리", "경영지원본부 부장", "회계팀 과장"]),
        "contact_phone": K.mobile(r),
    }


def _term_text(years: int, rng: random.Random) -> str:
    return f"{years}년" if rng.random() < 0.6 else f"{years * 12}개월"


def _legal_bank(bank: str) -> str:
    """약정서 '○○은행 앞' 에 쓰는 법인 명칭."""
    return brand(bank).legal


def _bank_name(p: Profile, rng: random.Random) -> str:
    return p.bank if rng.random() < 0.3 else _legal_bank(p.bank)


# ---------------------------------------------------------------------------
# 1. 대출거래신청서 (개인)
# ---------------------------------------------------------------------------

_DWELLING = {"아파트": "아파트", "오피스텔": "오피스텔", "단독주택": "단독", "다세대주택": "다세대"}
_OTHER_LENDERS = ["국민은행", "신한은행", "우리은행", "하나은행", "농협은행", "현대카드", "삼성카드",
                  "KB국민카드", "신한카드", "카카오뱅크", "토스뱅크", "OK저축은행", "새마을금고"]


_LENDER_SINCE = {"카카오뱅크": date(2017, 7, 27), "토스뱅크": date(2021, 10, 5)}


def _lenders(p: Profile) -> list[str]:
    """작성일에 있던 타 금융기관 (옛 은행 서식이면 그 뒤 생긴 은행 제외, KEB하나은행 시기엔 하나은행=자행)."""
    same = {p.bank, "하나은행"} if p.bank == "KEB하나은행" else {p.bank}
    return [b for b in _OTHER_LENDERS if b not in same and p.issue_date >= _LENDER_SINCE.get(b, date.min)]


def _debts(p: Profile, pl: dict, rng: random.Random, df: str) -> list[dict]:
    """부채현황 (타 금융기관 대출). 대환이면 상환 대상 대출을 반드시 넣는다."""
    out = []
    lenders = _lenders(p)
    sal = p.employment.annual_salary
    if "대환" in pl["purpose"]:
        lender = rng.choice([b for b in _OTHER_LENDERS[:5] if b in lenders])
        kind = "주택담보대출" if pl["kind"] == "mortgage" else "신용대출"
        out.append({"lender": lender, "kind": kind,
                    "balance": won(K.round_to(pl["amount"] * rng.uniform(0.85, 1.0), 100_000), ""),
                    "maturity": D(_add_years(p.issue_date, rng.randint(1, 25)), df), "refinance": "상환예정"})
    for _ in range(rng.choice([0, 0, 1, 1, 2]) - len(out)):
        lender = rng.choice(lenders)
        kind = "카드론" if "카드" in lender else rng.choice(["신용대출", "마이너스통장", "자동차할부", "학자금대출"])
        bal = K.round_to(sal * rng.uniform(0.03, 0.4), 100_000)
        out.append({"lender": lender, "kind": kind, "balance": won(bal, ""),
                    "maturity": D(_add_years(p.issue_date, rng.randint(1, 5)), df), "refinance": "유지"})
    return out


@doc("loan_application", "대출거래신청서", "bank_form", category="internal")
def loan_application(p: Profile, rng: random.Random) -> dict:
    """개인 고객 대출신청서(가계용). 하나은행 「대출신청서(가계용)」, 신한은행 「대출상담및신청서(가계용)」 항목 구성 참고."""
    pl = _plan_personal(p)
    per, e, prop = p.person, p.employment, p.property
    df = rng.choice(["dot", "kor", "dash"])
    owns_home = prop.address.road_short == per.address.road_short
    if owns_home:
        housing = "자가"
    elif pl["kind"] == "jeonse":
        housing = "전세"
    else:
        housing = rng.choices(["전세", "월세", "기타"], weights=[60, 30, 10])[0]
    if owns_home:
        dwelling = _DWELLING.get(prop.kind, "아파트")
    else:
        dwelling = rng.choices(["아파트", "다세대", "연립·빌라", "오피스텔", "단독"], weights=[55, 15, 12, 12, 6])[0]
    if pl["collateral"] == "부동산":
        col_detail = f"{prop.address.road_short} ({prop.kind}, 전용 {prop.exclusive_area}㎡)"
    elif pl["collateral"] == "보증":
        col_detail = f"{pl['guarantor']} 보증서"
    else:
        col_detail = rng.choice(["신용", "무보증 신용", "신용(급여이체 조건)"])
    acct = pl["debit_account"]
    salary = e.annual_salary
    job = "전문직" if pl["product"].startswith("전문직") else rng.choices(["급여소득자", "공무원"], weights=[92, 8])[0]
    purpose_cat = ("주택구입" if pl["purpose"] == "주택구입자금" else "주택임차" if pl["kind"] == "jeonse"
                   else "부채상환" if "대환" in pl["purpose"] else "생활비")
    assets = []
    if owns_home or (pl["collateral"] == "부동산" and pl["purpose"] != "주택구입자금"):
        assets.append({"kind": prop.kind.replace("주택", ""), "location": prop.address.road_short.split(",")[0],
                       "value": won(K.round_to(prop.price, 10_000_000), "")})
    dep = sum(a.balance for a in p.accounts)
    if dep > 1_000_000 and rng.random() < 0.7:
        assets.append({"kind": "예금", "location": ", ".join(list(dict.fromkeys(a.bank for a in p.accounts))[:2]),
                       "value": won(K.round_to(dep, 100_000), "")})
    return {
        "bank": p.bank,
        "branch": p.bank_branch,
        "applicant": {
            "name": per.name,
            "rrn": per.rrn if rng.random() < 0.4 else K.mask_rrn(per.rrn),
            "address": per.address.road_full,
            "zipcode": per.address.zipcode,
            "mobile": per.mobile,
            "email": per.email,
            "home_phone": _home_phone(rng, p),
            "work_phone": e.company.phone,
        },
        "workplace": {
            "job_type": job,
            "name": e.company.name,
            "department": e.department,
            "position": e.position,
            "hire_date": D(e.hire_date, df),
            "annual_income": won(salary) if rng.random() < 0.5 else f"{salary // 10000:,}만원",
            "address": e.company.address.road_short,
        },
        "housing": housing,
        "dwelling": dwelling,
        "debts": _debts(p, pl, rng, rng.choice(["dot", "dash"])),
        "assets": assets,
        "loan": {
            "subject": pl["subject"],
            "product": pl["product"],
            "amount": won(pl["amount"], ""),
            "amount_korean": _korean_amount(pl["amount"], rng),
            "term": _term_text(pl["term_years"], rng),
            "hope_date": D(pl["start_date"], df),
            "repayment": {"원리금균등분할상환": "원리금균등분할", "원금균등분할상환": "원금균등분할",
                          "만기일시상환": "만기일시"}[pl["repayment"]],
            "rate_type": pl["rate_type"][:2],
            "purpose_category": purpose_cat,
            "purpose": pl["purpose"],
            "interest_day": f"매월 {pl['pay_day']}일",
            "debit_bank": acct.bank,
            "debit_account": acct.number,
            "debit_holder": acct.holder,
        },
        "collateral": pl["collateral"],
        "collateral_detail": col_detail,
        "consent": "동의함",
        "manual_received": "예",
        "apply_date": D(pl["apply_date"], rng.choice(["kor", "kor_short"])),
        "signature": per.name,
    }


# ---------------------------------------------------------------------------
# 2. 기업여신 신청서 (법인)
# ---------------------------------------------------------------------------

@doc("loan_application_corp", "기업여신 신청서", "bank_form", category="internal")
def loan_application_corp(p: Profile, rng: random.Random) -> dict:
    """법인 고객 기업여신 신청서 (은행 자체 서식)."""
    c = p.corporation
    pl = _plan_corp(p)
    fy = p.issue_date.year - 1
    rev = c.revenue
    size = "중소기업" if rev < 150_000_000_000 else rng.choice(["중견기업", "중소기업"]) if rev < 300_000_000_000 else "중견기업"
    other = []
    for _ in range(rng.choice([0, 1, 1, 2, 2])):
        lender = rng.choice([b for b in ["국민은행", "신한은행", "우리은행", "하나은행", "농협은행", "기업은행",
                                         "산업은행", "수협은행"] if b != p.bank and not (b == "하나은행" and p.bank == "KEB하나은행")])
        if lender in (x["lender"] for x in other):
            continue
        other.append({"lender": lender,
                      "kind": rng.choice(["운전자금대출", "시설자금대출", "무역금융", "할인어음", "당좌대출", "구매자금대출"]),
                      "balance": f"{K.round_to(rev * rng.uniform(0.005, 0.04), 10_000_000) // 1_000_000:,}",
                      "collateral": rng.choice(["신용", "부동산", "신용보증기금", "기술보증기금", "예금"])})
    return {
        "bank": p.bank,
        "branch": p.bank_branch,
        "company": {
            "name": c.name,
            "name_en": c.name_en,
            "biz_no": c.biz_no,
            "corp_no": c.corp_no,
            "ceo": c.ceo.name,
            "established": D(c.established, rng.choice(["dot", "kor"])),
            "industry": f"{c.biz_type} / {c.biz_item}",
            "employees": f"{c.employees:,}명",
            "size": size,
            "revenue": won(c.revenue) if rng.random() < 0.4 else f"{c.revenue // 1_000_000:,}백만원",
            "revenue_year": f"{fy}년",
            "capital": won(c.capital),
            "address": c.address.road_full,
            "phone": c.phone,
            "fax": c.fax,
        },
        "contact": {
            "name": pl["contact"],
            "position": pl["contact_pos"],
            "phone": pl["contact_phone"],
            "email": c.email,
        },
        "loan": {
            "subject": pl["kind"],
            "product": pl["product"],
            "amount": won(pl["amount"]),
            "amount_korean": _korean_amount(pl["amount"], rng),
            "term": _term_text(pl["term_years"], rng),
            "hope_date": D(pl["start_date"], rng.choice(["dot", "dash"])),
            "repayment": pl["repayment"],
            "rate_type": pl["rate_type"],
            "fund_type": "시설자금" if pl["kind"] == "시설자금대출" else "운전자금",
            "purpose": pl["purpose"],
            "deposit_account": f"{p.bank} {pl['debit_account']}",
            "collateral": pl["collateral"],
            "collateral_detail": pl["collateral_detail"],
        },
        "other_loans": other,
        "apply_date": D(pl["apply_date"], rng.choice(["kor", "kor_short"])),
        "signature": c.ceo.name,
    }


# ---------------------------------------------------------------------------
# 3. 여신거래약정서 (가계용)
# ---------------------------------------------------------------------------

def _agreement_terms(pl: dict, rng: random.Random, df: str) -> dict:
    rt = pl["rate"]
    if since(pl["apply_date"], "late_3pct"):
        late = min(rt["applied"] + 3.0, 15.0)
        late_rate = f"대출이자율 + 연체가산이자율 연 3% (현재 연 {late:.2f}%, 최고 연 15%)"
    else:  # 2018.4.30 이전: 연체기간별 가산 (3개월 이하 연 6~7%, 초과 연 8%)
        late = min(rt["applied"] + 6.0, 15.0)
        late_rate = f"대출이자율 + 연체기간별 가산이자율 연 6~8% (현재 연 {late:.2f}%, 최고 연 15%)"
    pf = pl["prepay_fee"]
    return {
        "amount": won(pl["amount"]),
        "amount_korean": _korean_amount(pl["amount"], rng),
        "start_date": D(pl["start_date"], df),
        "maturity": D(pl["maturity"], df),
        "base_rate_name": rt["base_name"],
        "base_rate": _rate(rt["base"]),
        "spread": _rate(rt["spread"]),
        "pref_rate": _rate(rt["pref"]),
        "applied_rate": _pa(rt["applied"]),
        "late_rate": late_rate,
        "prepay_fee": "면제" if pf == 0 else f"중도상환금액 × {pf:.2f}% × 잔존일수 ÷ 대출기간일수 (3년 경과 시 면제)",
        "interest_calc": rng.choice(["1년을 365일(윤년 366일)로 보고 1일 단위로 계산",
                                     "연 365일 일할 계산 (윤년은 366일)"]),
        "interest_pay": f"매월 {pl['pay_day']}일 (후취)",
        "debit_account": f"{pl['debit_bank']} {pl['debit_number']}",
    }


def _stamp_tax(amount: int) -> str:
    """인지세법 제3조: 금융기관 대출 약정서 (5천만원 이하 비과세). 고객·은행 50%씩 부담."""
    if amount <= 50_000_000:
        return "비과세 (5천만원 이하)"
    tax = 70_000 if amount <= 100_000_000 else 150_000 if amount <= 1_000_000_000 else 350_000
    return f"{won(tax)} (고객 {won(tax // 2)} / 은행 {won(tax // 2)})"


@doc("credit_agreement", "대출거래약정서(가계용)", "bank_form", category="internal")
def credit_agreement(p: Profile, rng: random.Random) -> dict:
    """대출거래약정서(가계용) 첫 장. 은행연합회 표준 구성(제1조 거래조건 ~ 인지세 부담) 기준."""
    pl = _plan_personal(p)
    per = p.person
    df = rng.choice(["dot", "kor_short", "dash"])
    a = pl["debit_account"]
    terms = _agreement_terms({**pl, "debit_bank": a.bank, "debit_number": a.number}, rng, df)
    reset = {"고정금리": "해당없음(만기까지 고정)", "혼합금리": "최초 5년 고정 후 6개월마다 변동",
             "변동금리": rng.choice(["6개월", "3개월", "12개월"])}[pl["rate_type"]]
    limit = pl["subject"].endswith("(한도)")
    return {
        "bank": p.bank,
        "creditor": _legal_bank(p.bank),
        "branch": p.bank_branch,
        "debtor": {
            "name": per.name,
            "rrn": K.mask_rrn(per.rrn) if rng.random() < 0.5 else per.rrn,
            "address": per.address.road_full,
            "phone": per.mobile,
        },
        "loan": {
            "subject": pl["subject"],
            "product": pl["product"],
            "method": "한도거래" if limit else "개별거래",
            "account_no": pl["loan_account"],
            "rate_type": pl["rate_type"],
            "rate_reset": reset,
            "repayment": pl["repayment"],
            "installment": "해당없음" if pl["repayment"] == "만기일시상환" else f"{pl['term_years'] * 12}회 (매월)",
            **terms,
        },
        "stamp_tax": _stamp_tax(pl["amount"]),
        "explained": "예",
        "handwritten": rng.choice(["설명을 듣고 이해함", "충분히 설명듣고 이해함", "설명들었음"]),
        "contract_date": D(pl["contract_date"], rng.choice(["kor", "kor_short"])),
        "signature": per.name,
    }


# ---------------------------------------------------------------------------
# 4. 여신거래약정서 (기업용)
# ---------------------------------------------------------------------------

@doc("credit_agreement_corp", "여신거래약정서(기업용)", "bank_form", category="internal")
def credit_agreement_corp(p: Profile, rng: random.Random) -> dict:
    """기업 여신거래약정서 첫 페이지."""
    c = p.corporation
    pl = _plan_corp(p)
    df = rng.choice(["dot", "kor_short", "dash"])
    terms = _agreement_terms({**pl, "debit_bank": p.bank, "debit_number": pl["debit_account"]}, rng, df)
    terms["interest_pay"] = f"매월 {pl['pay_day']}일" if pl["pay_day"] != 30 else "매월 말일"
    return {
        "bank": p.bank,
        "creditor": _legal_bank(p.bank),
        "branch": p.bank_branch,
        "debtor": {
            "name": c.name,
            "biz_no": c.biz_no,
            "corp_no": c.corp_no,
            "ceo": c.ceo.name,
            "address": c.address.road_full,
            "phone": c.phone,
        },
        "loan": {
            "subject": pl["kind"],
            "product": pl["product"],
            "method": "한도거래" if pl["kind"] == "한도대출" else "개별거래",
            "account_no": pl["loan_account"],
            "rate_type": pl["rate_type"],
            "rate_reset": "해당없음" if pl["rate_type"] == "고정금리" else rng.choice(["3개월", "6개월"]),
            "repayment": pl["repayment"],
            "purpose": pl["purpose"],
            **terms,
        },
        "stamp_tax": _stamp_tax(pl["amount"]),
        "explained": "예",
        "contract_date": D(pl["contract_date"], rng.choice(["kor", "kor_short"])),
        "signature": c.ceo.name,
    }


# ---------------------------------------------------------------------------
# 5. 근저당권설정계약서
# ---------------------------------------------------------------------------

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
    return {
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


# ---------------------------------------------------------------------------
# 6. 보증약정서
# ---------------------------------------------------------------------------

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
    return {
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


# ---------------------------------------------------------------------------
# 7. 자동이체 신청서
# ---------------------------------------------------------------------------

@doc("auto_transfer_application", "자동이체 신청서", "bank_form", category="internal")
def auto_transfer_application(p: Profile, rng: random.Random) -> dict:
    """대출이자/원리금 자동이체 신청서."""
    pl = _plan_personal(p)
    per = p.person
    a = pl["debit_account"]
    amortizing = pl["repayment"] != "만기일시상환"
    target = "대출원리금" if amortizing else "대출이자"
    months = pl["term_years"] * 12
    if amortizing and pl["repayment"] == "원리금균등분할상환":
        est = _pmt(pl["amount"], pl["rate"]["applied"], months)
    elif amortizing:
        est = int(round(pl["amount"] / months + pl["amount"] * pl["rate"]["applied"] / 1200, -1))
    else:
        est = int(round(pl["amount"] * pl["rate"]["applied"] / 1200, -1))
    amount = (f"청구금액 전액 (약 {won(est)})" if rng.random() < 0.5
              else rng.choice(["청구금액 전액", "매월 청구금액"]) + f" / 예상 {won(est)}")
    df = rng.choice(["dot", "kor_short", "dash"])
    first = _add_months(pl["start_date"].replace(day=min(pl["pay_day"], 28)), 1)
    birth = per.birth
    return {
        "bank": p.bank,
        "branch": p.bank_branch,
        "kind": rng.choice(["신규", "신규", "변경"]),
        "biller": {"name": _legal_bank(p.bank), "fee_type": f"{target}({pl['subject']})"},
        "applicant": {
            "name": per.name,
            "birth": birth.strftime(rng.choice(["%Y.%m.%d", "%y%m%d", "%Y-%m-%d"])),
            "phone": per.mobile,
            "address": per.address.road_short,
        },
        "debit": {"bank": a.bank, "account": a.number, "holder": a.holder,
                  "holder_birth": birth.strftime("%y%m%d"), "holder_phone": per.mobile},
        "relation": "본인",
        "target": target,
        "loan_account": pl["loan_account"],
        "loan_product": pl["product"],
        "transfer_day": f"매월 {pl['pay_day']}일",
        "start_month": f"{first.year}년 {first.month}월분부터" if df != "dash" else D(first, "dash"),
        "amount": amount,
        "privacy_consent": "동의함",
        "third_party_consent": "동의함",
        "apply_date": D(pl["apply_date"] + timedelta(days=rng.randint(2, 12)), rng.choice(["kor", "kor_short", df])),
        "signature": per.name,
        "holder_signature": a.holder,
    }
