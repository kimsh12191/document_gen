"""은행 자체 여신 서식 (대출신청서, 여신거래약정서, 근저당권설정계약서, 보증약정서, 자동이체 신청서).

이 파일에는 그룹 서식들이 같이 쓰는 도우미만 있다. 서식마다 값 만드는 함수(@doc)는 서식 폴더
docgen/forms/<ID>/generate.py 에 있고, 끝의 FORMS 차례로 등록한다.

같은 프로필로 만든 여신 서류끼리 대출 금액·기간·금리·계좌가 맞도록, 핵심 조건은
프로필 seed 에서 파생한 별도 난수(_plan_personal / _plan_corp)로 정한다.
서류별 표기 차이(날짜 포맷, 문구 선택 등)만 각 함수의 rng 로 만든다.
"""
from ..banks import brand, since
from ..entities import World
from ._common import *  # noqa: F401,F403
from ..registry import register_folder_forms

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
    """고객 자체가 바뀌는 변형(외국인 고객 등)을 쓸지. 예전 업무 묶음(같은 고객의 서류 여러 건)에서만 꺼졌고 지금은 늘 켬."""
    return True


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


# ---------------------------------------------------------------------------
# 1. 대출거래신청서 (개인)
# ---------------------------------------------------------------------------

_OTHER_LENDERS = ["국민은행", "신한은행", "우리은행", "하나은행", "농협은행", "현대카드", "삼성카드",
                  "KB국민카드", "신한카드", "카카오뱅크", "토스뱅크", "OK저축은행", "새마을금고"]


_LENDER_SINCE = {"카카오뱅크": date(2017, 7, 27), "토스뱅크": date(2021, 10, 5)}


def _lenders(p: Profile) -> list[str]:
    """작성일에 있던 타 금융기관 (옛 은행 서식이면 그 뒤 생긴 은행 제외, KEB하나은행 시기엔 하나은행=자행)."""
    same = {p.bank, "하나은행"} if p.bank == "KEB하나은행" else {p.bank}
    return [b for b in _OTHER_LENDERS if b not in same and p.issue_date >= _LENDER_SINCE.get(b, date.min)]


# ---------------------------------------------------------------------------
# 2. 기업여신 신청서 (법인)
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# 4. 여신거래약정서 (기업용)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 5. 근저당권설정계약서
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 6. 보증약정서
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 7. 자동이체 신청서
# ---------------------------------------------------------------------------


# 이 그룹의 코드 서식. 값 만드는 함수는 서식 폴더 docgen/forms/<ID>/generate.py 에 있다 (여기는 같이 쓰는 도우미).
FORMS = ('loan_application', 'loan_application_corp', 'credit_agreement', 'credit_agreement_corp', 'collateral_agreement', 'guarantee_agreement', 'auto_transfer_application',)
register_folder_forms(__name__, FORMS)   # 예전 @doc 차례 그대로 등록 (서식 목록·데이터셋 순서)
