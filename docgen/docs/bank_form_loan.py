"""은행 자체 여신 서식 (대출신청서, 여신거래약정서, 근저당권설정계약서, 보증약정서, 자동이체 신청서).

같은 프로필로 만든 여신 서류끼리 대출 금액·기간·금리·계좌가 맞도록, 핵심 조건은
프로필 seed 에서 파생한 별도 난수(_plan_personal / _plan_corp)로 정한다.
서류별 표기 차이(날짜 포맷, 문구 선택 등)만 각 함수의 rng 로 만든다.
"""
from ..banks import brand, since
from ..entities import World
from ..registry import doc
from ._common import *  # noqa: F401,F403

# ---------------------------------------------------------------------------
# 변형(여러 쪽·특수 상황)용 공용 헬퍼 — bank_form_account.py 도 가져다 쓴다
# ---------------------------------------------------------------------------


def _age(p: Profile, x: Person) -> int:
    """작성일 기준 만 나이 (옛 은행 서식은 날짜가 옮겨져 있으므로 Person.age 대신 쓴다)."""
    d = p.issue_date
    return d.year - x.birth.year - ((d.month, d.day) < (x.birth.month, x.birth.day))


def _new_person(p: Profile, rng: random.Random, gender: str | None = None, age: tuple[int, int] = (30, 60),
                same_address: bool = False, surname_of: Person | None = None) -> Person:
    """프로필에 없는 사람(공동차주·보증인·대리인 등). 작성일 기준 나이 범위로 만든다."""
    w = World(rng.randint(0, 10 ** 9))
    y = p.issue_date.year
    sur = None
    if surname_of is not None:
        n = len(surname_of.name) - 2
        sur = (surname_of.name[:n], surname_of.hanja[:n], surname_of.surname_en)
    return w.person(gender, (y - age[1], y - age[0]), p.person.address if same_address else None, surname=sur)


def _solo(p: Profile) -> bool:
    """시나리오(서류 묶음) 생성이 아닐 때만 고객 자체가 바뀌는 변형(외국인 고객 등)을 쓴다."""
    return "scenario" not in p.extra


def _spouse(p: Profile, rng: random.Random) -> Person:
    if p.spouse:
        return p.spouse
    a = _age(p, p.person)
    return _new_person(p, rng, "F" if p.person.gender == "M" else "M", (max(22, a - 5), a + 5), same_address=True)


def _relative(p: Profile, rng: random.Random, rels=("배우자", "부", "모", "자녀", "형제자매")) -> tuple[Person, str]:
    """대리인 등으로 올 가족 한 명과 관계."""
    a = _age(p, p.person)
    cands = []
    if "배우자" in rels and p.spouse:
        cands += [(p.spouse, "배우자")] * 3
    if "부" in rels and a < 55:
        cands.append((p.father, "부"))
    if "모" in rels and a < 58:
        cands.append((p.mother, "모"))
    if "자녀" in rels:
        cands += [(c, "자녀") for c in p.children if _age(p, c) >= 19]
    if "형제자매" in rels or not cands:
        sib = _new_person(p, rng, None, (max(19, a - 8), a + 8), surname_of=p.person)
        cands.append((sib, "형제자매"))
    return rng.choice(cands)


def _minor(p: Profile, rng: random.Random) -> Person:
    """프로필 고객의 미성년 자녀 (없으면 새로 만든다)."""
    kids = [c for c in p.children if 0 <= _age(p, c) < 19]
    if kids:
        return rng.choice(kids)
    father = p.person if p.person.gender == "M" else (p.spouse or p.person)
    return _new_person(p, rng, None, (1, 17), same_address=True, surname_of=father)


# 외국인 고객: (한글 표기, 영문 성, 영문 이름, 국적, 국적(영문), 성별)
FOREIGN_NAMES = [
    ("응우옌 반 안", "NGUYEN", "VAN AN", "베트남", "VIETNAM", "M"),
    ("쩐 티 흐엉", "TRAN", "THI HUONG", "베트남", "VIETNAM", "F"),
    ("왕웨이", "WANG", "WEI", "중국", "CHINA", "M"),
    ("리나", "LI", "NA", "중국", "CHINA", "F"),
    ("마리아 산토스", "SANTOS", "MARIA", "필리핀", "PHILIPPINES", "F"),
    ("존 밀러", "MILLER", "JOHN", "미국", "UNITED STATES", "M"),
    ("다나카 유키", "TANAKA", "YUKI", "일본", "JAPAN", "F"),
    ("수레시 쿠마르", "KUMAR", "SURESH", "인도", "INDIA", "M"),
    ("시티 누르하야티", "NURHAYATI", "SITI", "인도네시아", "INDONESIA", "F"),
    ("솜차이 분마", "BOONMA", "SOMCHAI", "태국", "THAILAND", "M"),
    ("알렉산드르 이바노프", "IVANOV", "ALEKSANDR", "러시아", "RUSSIA", "M"),
    ("굴나라 사파로바", "SAFAROVA", "GULNARA", "우즈베키스탄", "UZBEKISTAN", "F"),
    ("바트바야르 간바트", "GANBAT", "BATBAYAR", "몽골", "MONGOLIA", "M"),
]


def _foreigner(p: Profile, rng: random.Random, age: tuple[int, int] = (24, 50), nations=None) -> dict:
    """외국인 고객 (외국인등록번호·국적). 이름·주소 외 값은 프로필과 별개로 만든다. nations: 국적(영문) 제한."""
    ko, sur, given, nat, nat_en, g = rng.choice([x for x in FOREIGN_NAMES if not nations or x[4] in nations])
    y = p.issue_date.year
    birth = rand_date(rng, date(y - age[1], 1, 1), date(y - age[0], 12, 31))
    return {"name": ko, "surname_en": sur, "given_en": given, "name_en": f"{sur} {given}", "nationality": nat,
            "nationality_en": nat_en, "gender": g, "birth": birth, "arc_no": K.rrn(rng, birth, g, foreigner=True),
            "mobile": K.mobile(rng),
            "email": f"{given.split()[0].lower()}{rng.randint(1, 99)}@{rng.choice(['gmail.com', 'naver.com', 'yahoo.com'])}"}


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


def _debts(p: Profile, pl: dict, rng: random.Random, df: str, n: int | None = None) -> list[dict]:
    """부채현황 (타 금융기관 대출). 대환이면 상환 대상 대출을 반드시 넣는다. n: 건수 (다중채무 고객)."""
    out = []
    lenders = _lenders(p)
    sal = p.employment.annual_salary
    if "대환" in pl["purpose"]:
        lender = rng.choice([b for b in _OTHER_LENDERS[:5] if b in lenders])
        kind = "주택담보대출" if pl["kind"] == "mortgage" else "신용대출"
        out.append({"lender": lender, "kind": kind,
                    "balance": won(K.round_to(pl["amount"] * rng.uniform(0.85, 1.0), 100_000), ""),
                    "maturity": D(_add_years(p.issue_date, rng.randint(1, 25)), df), "refinance": "상환예정"})
    for _ in range((rng.choice([0, 0, 1, 1, 2]) if n is None else n) - len(out)):
        lender = rng.choice(lenders)
        kind = "카드론" if "카드" in lender else rng.choice(["신용대출", "마이너스통장", "자동차할부", "학자금대출"]
                                                         + (["현금서비스", "보험약관대출"] if n else []))
        bal = K.round_to(sal * rng.uniform(0.03, 0.4 if n is None else 0.15), 100_000)
        mat = _add_years(p.issue_date, rng.randint(1, 5)) + timedelta(days=rng.randint(-160, 160))
        out.append({"lender": lender, "kind": kind, "balance": won(bal, ""), "maturity": D(mat, df),
                    "refinance": "상환예정" if n and rng.random() < 0.15 else "유지"})
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
    data = {
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
    _loan_app_variants(p, pl, rng, data)
    return data


def _loan_app_variants(p: Profile, pl: dict, rng: random.Random, data: dict) -> None:
    """대출신청서 변형: 다중채무(여러 쪽), 공동차주, 대리인 신청, 공란 많은 서식, 체크 누락."""
    if heavy(rng, 0.2):  # 타 금융기관 대출·재산이 많은 고객 → 부채현황 표가 길어진다
        data["debts"] = _debts(p, pl, rng, rng.choice(["dot", "dash"]), n=rng.randint(6, 14))
        assets = data["assets"]
        for _ in range(rng.randint(2, 4)):
            kind = rng.choice(["예금", "적금", "주식", "펀드", "자동차", "보험(해약환급금)"])
            where = {"자동차": rng.choice(["그랜저 (2021년식)", "쏘렌토 (2020년식)", "K5 (2019년식)", "아반떼 (2022년식)"]),
                     "주식": rng.choice(["미래에셋증권", "키움증권", "삼성증권", "한국투자증권"]),
                     "펀드": rng.choice(["KB자산운용", "미래에셋자산운용", "삼성자산운용"]),
                     "보험(해약환급금)": rng.choice(["삼성생명", "한화생명", "교보생명"])}.get(kind, rng.choice(_lenders(p)[:5]))
            assets.append({"kind": kind, "location": where,
                           "value": won(K.round_to(p.employment.annual_salary * rng.uniform(0.05, 0.6), 100_000), "")})
    if special(rng, "co_borrower", 0.12):  # 부부 공동명의 등 공동차주(공동신청인)
        sp = _spouse(p, rng)
        data["co_borrower"] = {"name": sp.name, "rrn": K.mask_rrn(sp.rrn), "relation": "배우자", "mobile": sp.mobile,
                               "workplace": rng.choice(["", "", "주부", "자영업", f"{p.employment.company.name[:2]}물산"]) or None}
    if special(rng, "agent", 0.1):  # 대리인 신청 (위임장·인감증명서 첨부)
        ag, rel = _relative(p, rng)
        data["agent"] = {"name": ag.name, "rrn": K.mask_rrn(ag.rrn), "relation": rel, "phone": ag.mobile,
                         "poa": "첨부"}
    if special(rng, "sparse", 0.15):  # 선택 항목을 비워 둔 서식
        ap, wp = data["applicant"], data["workplace"]
        for k in rng.sample(["email", "home_phone", "work_phone", "zipcode"], rng.randint(2, 4)):
            ap[k] = None
        if rng.random() < 0.6:
            wp["address"] = None
        if rng.random() < 0.5:
            wp["department"] = None
    if special(rng, "no_check", 0.1):  # 체크 누락
        for k in rng.sample(["housing", "dwelling", "loan.rate_type"], rng.randint(1, 2)):
            if "." in k:
                data["loan"][k.split(".")[1]] = None
            else:
                data[k] = None


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
    many = heavy(rng, 0.25)  # 거래 금융기관이 많은 기업 → 타 금융기관 여신 현황이 길어진다
    pool = [b for b in ["국민은행", "신한은행", "우리은행", "하나은행", "농협은행", "기업은행", "산업은행", "수협은행"]
            + (["수출입은행", "부산은행", "경남은행", "iM뱅크", "SC제일은행", "OK저축은행", "SBI저축은행",
                "현대캐피탈", "KB캐피탈", "신한캐피탈"] if many else [])
            if b != p.bank and not (b == "하나은행" and p.bank == "KEB하나은행")]
    for _ in range(rng.randint(7, 16) if many else rng.choice([0, 1, 1, 2, 2])):
        lender = rng.choice(pool)
        kind = rng.choice(["운전자금대출", "시설자금대출", "무역금융", "할인어음", "당좌대출", "구매자금대출"]
                          + (["외화대출", "수입신용장(L/C)", "리스", "팩토링"] if many else []))
        if (lender, kind) in ((x["lender"], x["kind"]) for x in other) or (not many and lender in (x["lender"] for x in other)):
            continue
        other.append({"lender": lender, "kind": kind,
                      "balance": K.round_to(rev * rng.uniform(0.002 if many else 0.005, 0.02 if many else 0.04), 10_000_000) // 1_000_000,
                      "collateral": rng.choice(["신용", "부동산", "신용보증기금", "기술보증기금", "예금"])})
    total = sum(x["balance"] for x in other)
    for x in other:
        x["balance"] = f"{x['balance']:,}"
    data = {
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
    if len(other) >= 3:
        data["other_loans_total"] = f"{total:,}"
    if special(rng, "agent", 0.15):  # 직원이 대리인으로 신청 (법인인감 날인 위임장 첨부)
        data["agent"] = {"name": pl["contact"], "position": pl["contact_pos"], "phone": pl["contact_phone"],
                         "rrn": K.mask_rrn(K.rrn(rng, rand_date(rng, date(p.issue_date.year - 50, 1, 1),
                                                                 date(p.issue_date.year - 26, 12, 31)), rng.choice("MF")))}
    if special(rng, "sparse", 0.15):  # 선택 항목 미기재
        for k in rng.sample(["fax", "name_en", "employees"], rng.randint(1, 3)):
            data["company"][k] = None
        if rng.random() < 0.5:
            data["contact"]["email"] = None
    if special(rng, "no_check", 0.1):  # 체크 누락
        k = rng.choice(["company.size", "loan.fund_type", "loan.rate_type"])
        data[k.split(".")[0]][k.split(".")[1]] = None
    return data


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


# 약정서 특약사항 (여러 쪽 약정서). 은행이 입력해 출력하는 문구.
_TERMS_PERSONAL = [
    "급여이체 및 당행 신용카드 결제계좌를 대출기간 중 당행으로 유지하는 조건으로 우대금리 연 {p1:.1f}%p를 적용하며, 조건 미충족 시 그 다음 이자계산기간부터 우대금리를 적용하지 아니한다.",
    "채무자는 대출 실행일로부터 {m}개월 이내에 담보물건에 전입하여 실거주하여야 하며, 이를 이행하지 아니하는 경우 은행은 기한의 이익을 상실시킬 수 있다.",
    "채무자는 대출기간 중 담보주택 외 추가 주택을 취득하지 아니하기로 하며, 이를 위반한 경우 즉시 대출금을 상환한다.",
    "이 대출금은 {purpose} 용도로만 사용하며, 은행이 요청하는 경우 자금 사용 증빙서류를 제출한다.",
    "대환 대상 대출({lender})은 대출 실행일에 은행이 직접 상환하며, 채무자는 상환영수증을 은행에 제출한다.",
    "기준금리 변동 시 대출이자율은 매 {reset} 단위로 변경되며, 변경된 이자율은 은행 홈페이지 및 문자메시지로 통지한다.",
    "은행이 정한 중도상환해약금 면제 요건(대출 실행 후 3년 경과 등)에 해당하는 경우 중도상환해약금을 면제한다.",
    "채무자가 은행의 동의 없이 담보물건에 임대차(전세권 설정 포함)를 하는 경우 은행은 추가 담보 제공 또는 대출금 일부 상환을 요구할 수 있다.",
    "자동이체계좌 잔액 부족으로 이자를 납입하지 못한 경우 은행은 채무자의 당행 다른 예금 계좌에서 출금하여 충당할 수 있다.",
    "채무자는 주소·연락처·직장 등 신용상태에 중요한 변동이 있는 경우 지체 없이 은행에 서면으로 신고한다.",
    "본 대출의 우대금리 합계는 연 {p2:.1f}%p를 한도로 하며, 우대 항목별 충족 여부는 매월 말일 기준으로 판단한다.",
]
_TERMS_CORP = [
    "채무자는 매 회계연도 종료 후 90일 이내에 외부감사인의 감사를 받은 재무제표를 은행에 제출한다.",
    "채무자는 여신기간 중 부채비율을 {debt}% 이하로 유지하며, 이를 초과한 경우 은행은 가산금리 연 {p1:.1f}%p를 추가 적용할 수 있다.",
    "채무자는 은행의 사전 서면 동의 없이 다른 금융기관으로부터 담보부 차입을 하거나 제3자를 위한 담보를 제공하지 아니한다.",
    "채무자의 대표이사 변경, 최대주주 변경, 합병·분할 또는 영업양도가 있는 경우 지체 없이 은행에 통지한다.",
    "이 여신은 {purpose} 용도로만 사용하며, 은행이 요구하는 경우 자금사용 증빙(세금계산서, 계약서 등)을 제출한다.",
    "채무자는 여신기간 중 당행 결제성 계좌의 월평균 입금액이 {amt}백만원 이상 유지되도록 노력하며, 미달 시 우대금리를 적용하지 아니한다.",
    "보증기관의 보증서 기한이 연장되지 아니하거나 보증이 해지된 경우 은행은 기한의 이익을 상실시킬 수 있다.",
    "채무자는 매 반기 종료 후 60일 이내에 부가가치세 과세표준증명 및 국세·지방세 완납증명서를 제출한다.",
    "채무자가 담보물건을 임대하는 경우 사전에 은행의 동의를 받아야 하며, 임대차계약서 사본을 은행에 제출한다.",
    "이자보상배율이 2기 연속 1 미만인 경우 은행은 추가 담보 제공 또는 여신 일부 상환을 요구할 수 있다.",
    "한도여신의 미사용 한도에 대하여는 연 {p3:.1f}%의 한도약정수수료를 매 분기 말 후취한다.",
]


def _special_terms(pool: list[str], rng: random.Random, n: int, **kw) -> list[str]:
    return [t.format(**kw) for t in rng.sample(pool, min(n, len(pool)))]


def _agreement_variants(p: Profile, rng: random.Random, data: dict, pool: list[str], fmt: dict,
                        personal: bool) -> None:
    """약정서 변형: 특약 추가로 본문이 여러 쪽(heavy), 공동차주·연대보증인, 자필 누락, 체크 누락."""
    if heavy(rng, 0.3):  # 특약 조항이 붙어 본문이 2~3쪽으로 이어지는 약정서
        data["special_terms"] = _special_terms(pool, rng, rng.randint(3, 7), **fmt)
    if personal and special(rng, "co_borrower", 0.1):  # 부부 공동차주
        sp = _spouse(p, rng)
        data["co_borrower"] = {"name": sp.name, "rrn": K.mask_rrn(sp.rrn) if rng.random() < 0.5 else sp.rrn,
                               "address": sp.address.road_full, "phone": sp.mobile}
    if not personal and special(rng, "joint_guarantor", 0.15):  # 실제경영자·이사 연대보증
        gs = [p.person] + ([rng.choice(p.directors)] if rng.random() < 0.5 else [])
        data["guarantors"] = [{"name": g.name, "rrn": K.mask_rrn(g.rrn), "address": g.address.road_short,
                               "relation": "대표이사(실제경영자)" if g is p.person else rng.choice(["이사", "공동대표", "최대주주"])}
                              for g in gs]
    if personal and special(rng, "handwriting_missing", 0.08):  # 자필기재란을 비워 둔 채 제출
        data["handwritten"] = None
    if special(rng, "no_check", 0.08):  # 설명 확인 체크 누락
        data["explained"] = None


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
    data = {
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
    fmt = {"p1": rng.choice([0.1, 0.2, 0.3]), "p2": rng.choice([0.5, 0.7, 1.0]), "m": rng.choice([1, 3, 6]),
           "purpose": pl["purpose"], "lender": rng.choice(_lenders(p)[:5]),
           "reset": reset if pl["rate_type"] == "변동금리" else "6개월"}
    pool = [t for t in _TERMS_PERSONAL if ("{lender}" not in t or "대환" in pl["purpose"])
            and (pl["kind"] == "mortgage" or not any(w in t for w in ("담보", "전입")))]
    _agreement_variants(p, rng, data, pool, fmt, personal=True)
    return data


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
    data = {
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
    fmt = {"p1": rng.choice([0.2, 0.3, 0.5]), "p3": rng.choice([0.2, 0.3, 0.5]), "debt": rng.choice([200, 250, 300, 400]),
           "purpose": pl["purpose"], "amt": max(10, K.round_to(c.revenue / 12 / 1_000_000 * rng.uniform(0.1, 0.3), 10))}
    pool = [t for t in _TERMS_CORP if ("한도약정" not in t or pl["kind"] == "한도대출")
            and ("보증기관" not in t or pl["collateral"] == "보증서")
            and ("담보물건" not in t or pl["collateral"] == "부동산")]
    _agreement_variants(p, rng, data, pool, fmt, personal=False)
    return data


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
    data = {
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
    if heavy(rng, 0.15):  # 여러 대출의 이자·원리금을 한 번에 자동이체 등록
        extra = []
        for _ in range(rng.randint(4, 9)):
            kind = rng.choice(["가계일반자금대출", "주택담보대출", "마이너스통장", "전세자금대출", "예적금담보대출", "보금자리론"])
            extra.append({"loan_account": _loan_acct(rng, p.bank), "loan_product": kind,
                          "target": rng.choice(["대출이자", "대출원리금"]), "transfer_day": f"매월 {rng.choice([5, 10, 15, 20, 25])}일"})
        data["extra_loans"] = extra
    if special(rng, "other_holder", 0.15):  # 가족(배우자) 명의 계좌에서 출금 → 예금주 별도 서명
        sp = _spouse(p, rng)
        bank = rng.choice([b for b in ("국민은행", "신한은행", "우리은행", "농협은행", p.bank) if b])
        data["debit"] = {"bank": bank, "account": _digits(rng, _LOAN_ACCT_FMT.get(bank, "###-##-######"), head="1"),
                         "holder": sp.name, "holder_birth": sp.birth.strftime("%y%m%d"), "holder_phone": sp.mobile}
        data["relation"] = "가족"
        data["holder_signature"] = sp.name
    if special(rng, "no_check", 0.08):  # 체크 누락
        data[rng.choice(["relation", "target", "third_party_consent"])] = None
    if special(rng, "sparse", 0.1):  # 선택 기재란 공란
        data["applicant"]["address"] = None
    return data
