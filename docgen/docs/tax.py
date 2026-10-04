"""세금 관련 증명서 (국세청·지방자치단체 발급) 및 종합소득세 신고서.

개인사업체 매출·손익은 business.py 의 프로필 고정 모델(_revenue, _pl)을 공유하므로
부가가치세 과세표준증명·종합소득세 신고서·표준재무제표증명의 숫자가 서로 맞는다.
"""
from ..registry import doc
from ._common import *  # noqa: F401,F403
from .business import (_bookkeeping_double, _filed_year, _half_share, _hometax_no, _industry, _pl, _prng,
                       _revenue, _tax_office, _vat_simple)

# 종합소득세 기본세율 (2023년 귀속 이후): (과세표준 상한, 세율 %, 누진공제)
_BRACKETS = [
    (14_000_000, 6, 0), (50_000_000, 15, 1_260_000), (88_000_000, 24, 5_760_000),
    (150_000_000, 35, 15_440_000), (300_000_000, 38, 19_940_000), (500_000_000, 40, 25_940_000),
    (1_000_000_000, 42, 35_940_000), (float("inf"), 45, 65_940_000),
]


def _income_tax(base: int) -> tuple[int, int, int]:
    """(산출세액, 세율%, 누진공제)."""
    for cap, rate, prog in _BRACKETS:
        if base <= cap:
            return max(0, base * rate // 100 - prog), rate, prog
    raise AssertionError


def _floor10(n: int) -> int:
    return n // 10 * 10


def _signed(n: int) -> str:
    return won(n, "") if n >= 0 else "-" + won(-n, "")


def _cert_purpose(rng: random.Random, p: Profile) -> str:
    return rng.choice(["금융기관 제출", "금융기관 제출용", "대출 신청", "은행 제출", f"{p.bank} 제출"])


def _validity(p: Profile) -> str:
    """납세증명서 유효기간: 발급일부터 30일."""
    fmt = "kor"
    return f"{D(p.issue_date, fmt)} ~ {D(p.issue_date + timedelta(days=29), fmt)}"


# ---------------------------------------------------------------------------
# 국세 납세증명서 (개인 / 법인)
# ---------------------------------------------------------------------------
@doc("tax_payment_certificate", "납세증명서(국세완납증명)", "tax")
def tax_payment_certificate(p: Profile, rng: random.Random) -> dict:
    """홈택스 발급 국세 납세증명서 (개인사업자)."""
    b = p.business
    return {
        "issue_no": _hometax_no(rng),
        "taxpayer": {
            "trade_name": b.name,
            "biz_no": b.biz_no,
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.85 else p.person.rrn,
            "address": p.person.address.road_full,
        },
        "valid_period": _validity(p),
        "purpose_type": "대금수령 이외",
        "purpose": _cert_purpose(rng, p),
        "deferral": "해당없음",
        "arrears": "없음",
        "issue_date": D(p.issue_date, "kor"),
        "issuer": _tax_office(p.person.address),
    }


@doc("tax_payment_certificate_corp", "납세증명서(법인)", "tax")
def tax_payment_certificate_corp(p: Profile, rng: random.Random) -> dict:
    """홈택스 발급 국세 납세증명서 (법인)."""
    c = p.corporation
    return {
        "issue_no": _hometax_no(rng),
        "taxpayer": {
            "corp_name": c.name,
            "biz_no": c.biz_no,
            "ceo": p.person.name,
            "corp_reg_no": c.corp_no,
            "address": c.address.road_full,
        },
        "valid_period": _validity(p),
        "purpose_type": "대금수령 이외",
        "purpose": _cert_purpose(rng, p),
        "deferral": "해당없음",
        "arrears": "없음",
        "issue_date": D(p.issue_date, "kor"),
        "issuer": _tax_office(c.address),
    }


# ---------------------------------------------------------------------------
# 지방세 납세증명서
# ---------------------------------------------------------------------------
@doc("local_tax_payment_certificate", "지방세 납세증명서", "tax")
def local_tax_payment_certificate(p: Profile, rng: random.Random) -> dict:
    """정부24·위택스 발급 지방세 납세증명서 (체납 없음)."""
    return {
        "issue_no": issue_no(rng),
        "taxpayer": {
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.7 else p.person.rrn,
            "address": p.person.address.road_full,
        },
        "valid_period": _validity(p),
        "purpose": _cert_purpose(rng, p),
        "deferral": "해당없음",
        "arrears": "없음",
        "issue_date": D(p.issue_date, "kor"),
        "issuer": district_office(p.person.address),
    }


# ---------------------------------------------------------------------------
# 지방세 세목별 과세증명서
# ---------------------------------------------------------------------------
def _property_tax(official: int, one_house: bool) -> tuple[int, int]:
    """주택분 재산세 (과세표준, 세액). 1세대 1주택(공시가격 9억 이하)은 특례세율."""
    if one_house:
        ratio = 0.43 if official <= 300_000_000 else 0.44 if official <= 600_000_000 else 0.45
    else:
        ratio = 0.60
    base = int(official * ratio) // 1000 * 1000
    if one_house and official <= 900_000_000:
        table = [(60_000_000, 0.0005, 0), (150_000_000, 0.001, 30_000), (300_000_000, 0.002, 120_000), (None, 0.0035, 420_000)]
    else:
        table = [(60_000_000, 0.001, 0), (150_000_000, 0.0015, 60_000), (300_000_000, 0.0025, 195_000), (None, 0.004, 570_000)]
    lower = 0
    for cap, rate, fixed in table:
        if cap is None or base <= cap:
            return base, _floor10(int(fixed + (base - lower) * rate))
        lower = cap
    raise AssertionError


_CAR_HANGUL = "가나다라마거너더러머버서어저고노도로모보소오조구누두루무부수우주"


@doc("local_tax_assessment", "지방세 세목별 과세증명서", "tax")
def local_tax_assessment(p: Profile, rng: random.Random) -> dict:
    """주소지 시·군·구청장이 발급하는 지방세 세목별 과세증명서 (재산세·자동차세·주민세)."""
    a = p.person.address
    prop = p.property
    issue = p.issue_date
    one_house = rng.random() < 0.8
    growth = _prng(p, "official_price").uniform(-0.03, 0.08)
    car = None
    if rng.random() < 0.75:
        cc = rng.choice([998, 1353, 1591, 1598, 1999, 2151, 2497, 3342, 3470])
        car = {
            "no": f"{rng.randint(10, 399)}{rng.choice(_CAR_HANGUL)}{rng.randint(1000, 9999)}",
            "cc": cc,
            "model_year": rng.randint(issue.year - 12, issue.year - 1),
        }
    seoul = a.sido == "서울특별시"
    resident_tax = 6_000 if seoul else rng.choice([5_000, 7_000, 10_000])

    years = [issue.year - 1, issue.year] if rng.random() < 0.6 else [issue.year - 2, issue.year - 1, issue.year]
    rows: list[tuple[date, dict]] = []
    for y in years:
        official = K.round_to(prop.official_price * (1 + growth) ** (y - issue.year), 1_000_000)
        base, ptax = _property_tax(official, one_house)
        pa = prop.address
        obj = f"{pa.sigungu or pa.sido} {pa.dong} {pa.jibun}"
        if ptax <= 200_000:
            parts = [(date(y, 7, 31), "7월분", ptax)]
        else:
            half = _floor10(ptax // 2)
            parts = [(date(y, 7, 31), "7월분(1/2)", half), (date(y, 9, 30), "9월분(2/2)", ptax - half)]
        for due, label, t in parts:
            rows.append((due, {"year": f"{y}", "tax_item": "재산세(주택)", "due": label, "object": obj,
                               "base": won(base, ""), "tax": t, "edu": _floor10(t * 20 // 100)}))
        if car:
            age = y - car["model_year"] + 1
            cut = min(max(age - 2, 0) * 5, 50)
            per_cc = 80 if car["cc"] <= 1000 else 140 if car["cc"] <= 1600 else 200
            annual = car["cc"] * per_cc * (100 - cut) // 100
            for due, label in ((date(y, 6, 30), "6월분(1기)"), (date(y, 12, 31), "12월분(2기)")):
                t = _floor10(annual // 2)
                rows.append((due, {"year": f"{y}", "tax_item": "자동차세", "due": label,
                                   "object": f"{car['no']} 승용", "base": f"{car['cc']:,}cc",
                                   "tax": t, "edu": _floor10(t * 30 // 100)}))
        rows.append((date(y, 8, 31), {"year": f"{y}", "tax_item": "주민세(개인분)", "due": "8월분",
                                      "object": "세대주 개인분", "base": "-", "tax": resident_tax,
                                      "edu": _floor10(resident_tax * (25 if seoul else 10) // 100)}))
    rows = [r for due, r in sorted(rows, key=lambda x: x[0]) if due < issue][-10:]
    tot_tax = sum(r["tax"] for r in rows)
    tot_edu = sum(r["edu"] for r in rows)
    items = []
    for r in rows:
        items.append({**r, "tax": won(r["tax"], ""), "edu": won(r["edu"], ""), "total": won(r["tax"] + r["edu"], "")})
    first = rows[0]["year"]
    return {
        "issue_no": issue_no(rng),
        "taxpayer": {
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.6 else p.person.rrn,
            "address": a.road_full,
        },
        "period": f"{first}년 ~ {issue.year}년",
        "items": items,
        "sum": {"tax": won(tot_tax, ""), "edu": won(tot_edu, ""), "total": won(tot_tax + tot_edu, "")},
        "purpose": _cert_purpose(rng, p),
        "issue_date": D(issue, "kor"),
        "issuer": district_office(a),
    }


# ---------------------------------------------------------------------------
# 부가가치세 과세표준증명
# ---------------------------------------------------------------------------
@doc("vat_tax_base_certificate", "부가가치세 과세표준증명", "tax")
def vat_tax_base_certificate(p: Profile, rng: random.Random) -> dict:
    """홈택스 발급 부가가치세 과세표준증명 (개인사업자, 최근 4개 과세기간)."""
    b = p.business
    issue = p.issue_date
    simple = _vat_simple(p)
    va_rate = _industry(b)[1]
    rows = []
    if simple:  # 간이과세자: 1년 단위 과세기간
        y = issue.year
        while len(rows) < 3 and y >= b.established.year:
            due = date(y + 1, 1, 25)
            if due < issue:
                start = max(date(y, 1, 1), b.established)
                base = _revenue(p, y)  # 공급대가
                tax = 0 if base < 48_000_000 else max(0, _floor10(int(base * va_rate * 0.1) - int(base * 0.7 * 0.013)))
                rows.append({"period": f"{y}년 ({start:%m.%d}~12.31)", "kind": "정기확정",
                             "filed": rand_date(rng, date(y + 1, 1, 5), min(due, issue - timedelta(days=1))),
                             "base": base, "tax": tax})
            y -= 1
    else:  # 일반과세자: 반기 단위 확정신고
        y, h = issue.year, 2
        while len(rows) < 4 and y >= b.established.year:
            due = date(y, 7, 25) if h == 1 else date(y + 1, 1, 25)
            start = max(date(y, 1, 1) if h == 1 else date(y, 7, 1), b.established)
            end = date(y, 6, 30) if h == 1 else date(y, 12, 31)
            if due < issue and start <= end:
                rev = _revenue(p, y)
                h1 = int(rev * _half_share(p, y)) // 10 * 10
                base = h1 if h == 1 else rev - h1
                pl = _pl(p, y)
                buy_ratio = (pl["cogs"] + pl["rent"] + pl["other_sga"] // 2) / max(pl["revenue"], 1)
                buy_ratio *= _prng(p, "vatbuy", y, h).uniform(0.9, 1.1)
                card = int(base * 0.6 * 0.013) if b.biz_type in ("음식점업", "소매업") else 0
                tax = _floor10(int(base * 0.1 * (1 - buy_ratio)) - min(card, 5_000_000))
                rows.append({"period": f"{y}년 {h}기 ({start:%m.%d}~{end:%m.%d})", "kind": "정기확정",
                             "filed": rand_date(rng, end + timedelta(days=5), min(due, issue - timedelta(days=1))),
                             "base": base, "tax": tax})
            y, h = (y, 1) if h == 2 else (y - 1, 2)
    rows.reverse()
    fmt = rng.choice(["dash", "dot"])
    return {
        "issue_no": _hometax_no(rng),
        "taxpayer": {
            "trade_name": b.name,
            "biz_no": b.biz_no,
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn),
            "address": b.address.road_full,
            "biz_type": b.biz_type,
            "biz_item": b.biz_item,
            "kind": "간이과세자" if simple else "일반과세자",
        },
        "period": f"{rows[0]['period'].split(' (')[0]} ~ {rows[-1]['period'].split(' (')[0]}",
        "items": [{"period": r["period"], "kind": r["kind"], "filed": D(r["filed"], fmt),
                   "base": won(r["base"], ""), "tax": _signed(r["tax"])} for r in rows],
        "purpose": _cert_purpose(rng, p),
        "issue_date": D(issue, "kor"),
        "issuer": _tax_office(b.address),
    }


# ---------------------------------------------------------------------------
# 종합소득세 과세표준확정신고 및 납부계산서
# ---------------------------------------------------------------------------
@doc("income_tax_return", "종합소득세 과세표준확정신고 및 납부계산서", "tax")
def income_tax_return(p: Profile, rng: random.Random) -> dict:
    """종합소득세 확정신고서 첫 장 (기본사항 + 소득금액 + 세액계산). 사업소득은 표준손익계산서 당기순이익과 같다."""
    b = p.business
    y = max(_filed_year(p), b.established.year)
    biz_income = _pl(p, y)["net"]
    total_income = biz_income

    # 소득공제
    n_people = 1
    if p.spouse and rng.random() < 0.5:
        n_people += 1
    n_people += sum(1 for c in p.children if y - c.birth.year < 20)
    personal = 1_500_000 * n_people
    pension = _floor10(min(total_income // 12, 6_170_000) * 9 // 100 * 12)
    if rng.random() < 0.55:
        limits = (6_000_000, 4_000_000) if y >= 2025 else (5_000_000, 3_000_000)
        lim = limits[0] if total_income <= 40_000_000 else limits[1] if total_income <= 100_000_000 else 2_000_000
        yellow = min(rng.choice([1_200_000, 2_400_000, 3_000_000, 3_600_000, 6_000_000]), lim)
    else:
        yellow = 0
    deduction = personal + pension + yellow
    base = max(0, total_income - deduction)
    computed, rate, _ = _income_tax(base)
    reduction = 0
    credit = min(computed, 70_000 + 20_000)  # 표준세액공제 + 전자신고세액공제
    determined = computed - reduction - credit
    penalty = 0
    total = determined + penalty
    prepaid = _floor10(int(total * rng.uniform(0.3, 0.5))) if y > b.established.year else 0
    payable = _floor10(total - prepaid)
    installment = 0
    if payable > 10_000_000 and rng.random() < 0.6:
        installment = payable - 10_000_000 if payable <= 20_000_000 else _floor10(payable // 2)

    l_computed = computed // 10
    l_credit = min(l_computed, credit // 10)
    l_determined = l_computed - l_credit
    l_payable = _floor10(l_determined)

    double = _bookkeeping_double(p)
    filed = rand_date(rng, date(y + 1, 5, 2), date(y + 1, 5, 31))
    w = lambda n: won(n, "")  # noqa: E731
    return {
        "tax_year": f"{y}",
        "taxpayer": {
            "name": p.person.name,
            "rrn": p.person.rrn if rng.random() < 0.5 else K.mask_rrn(p.person.rrn),
            "address": p.person.address.road_full,
            "mobile": p.person.mobile,
            "email": p.person.email,
            "trade_name": b.name,
            "biz_no": b.biz_no,
            "biz_address": b.address.road_full,
        },
        "bookkeeping": "복식부기의무자" if double else "간편장부대상자",
        "filing_type": rng.choice(["자기조정", "외부조정"]) if double else "간편장부",
        "filing_kind": "정기신고",
        "income": {"interest": "0", "dividend": "0", "business": w(biz_income), "wage": "0",
                   "pension": "0", "other": "0", "total": w(total_income)},
        "deductions": {"personal": w(personal), "persons": f"{n_people}명", "pension": w(pension),
                       "yellow_umbrella": w(yellow), "total": w(deduction)},
        "national": {
            "total_income": w(total_income), "deduction": w(deduction), "base": w(base), "rate": f"{rate}%",
            "computed": w(computed), "reduction": w(reduction), "credit": w(credit), "determined": w(determined),
            "penalty": w(penalty), "total": w(total), "prepaid": w(prepaid), "payable": w(payable),
            "installment": w(installment), "due_payable": w(payable - installment),
        },
        "local": {
            "base": w(base), "rate": f"{rate / 10:g}%", "computed": w(l_computed), "reduction": "0",
            "credit": w(l_credit), "determined": w(l_determined), "penalty": "0", "total": w(l_determined),
            "prepaid": "0", "payable": w(l_payable), "due_payable": w(l_payable),
        },
        "filed_date": D(filed, rng.choice(["kor", "kor_short"])),
        "tax_office": _tax_office(p.person.address),
        "local_office": district_office(p.person.address),
    }
