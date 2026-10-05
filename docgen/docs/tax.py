"""세금 관련 증명서 (국세청·지방자치단체 발급) 및 종합소득세 신고서.

개인사업체 매출·손익은 business.py 의 프로필 고정 모델(_revenue, _pl)을 공유하므로
부가가치세 과세표준증명·종합소득세 신고서·표준재무제표증명의 숫자가 서로 맞는다.
사업장 이전·간이→일반 전환·휴업·공동사업자 같은 사실은 business._biz_facts(), 종합소득세 신고 구분은
business._itr_filing() 이 프로필 단위로 정한다.
"""
import os

from ..registry import doc
from ._common import *  # noqa: F401,F403
from .business import (_biz_facts, _bookkeeping_double, _filed_year, _half_base, _hometax_no, _industry, _itr_filing,
                       _pl, _prng, _revenue, _side_person, _sincere_filer, _tax_office, _vat_simple)

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


_PAYERS = ["조달청", "한국토지주택공사", "서울특별시", "한국도로공사", "한국전력공사"]


def _purpose_pair(rng: random.Random, p: Profile, corp: bool) -> dict:
    """사용목적 체크항목(대금 수령 / 해외이주 / 기타) + 괄호 안 구체적 목적 + 대금 지급자.
    special emigration: 개인의 해외이주용 발급."""
    kind = rng.choices(["기타", "대금 수령"], [9, 1])[0]
    if not corp and special(rng, "emigration", 0.03):
        return {"purpose_type": "해외이주", "purpose": "해외이주 신고", "payer": None}
    if kind == "대금 수령":
        payer = rng.choice(_PAYERS + [district_office(p.person.address).replace("청장", "청").replace("장", "")])
        return {"purpose_type": kind, "purpose": rng.choice(["공사대금 수령", "용역대금 수령", "물품대금 수령"]), "payer": payer}
    return {"purpose_type": kind, "purpose": _cert_purpose(rng, p), "payer": None}


def _due_dates(issue: date, corp: bool) -> list[tuple[date, str]]:
    """발급일 전후의 지정납부기한 후보 (기한, 세목 설명)."""
    out = []
    for y in (issue.year - 1, issue.year, issue.year + 1):
        out += [(date(y, 1, 25), f"{y - 1}년 2기 부가가치세"), (date(y, 7, 25), f"{y}년 1기 부가가치세")]
        if corp:
            out += [(date(y, 3, 31), f"{y - 1}사업연도 법인세"), (date(y, 8, 31), f"{y}사업연도 법인세 중간예납"),
                    (date(y, 4, 25), f"{y}년 1기 부가가치세 예정"), (date(y, 10, 25), f"{y}년 2기 부가가치세 예정")]
        else:
            out += [(date(y, 5, 31), f"{y - 1}년 귀속 종합소득세"), (date(y, 11, 30), f"{y}년 귀속 종합소득세 중간예납")]
    return sorted(out)


def _validity(rng: random.Random, p: Profile, corp: bool, name: str) -> tuple[str, str | None]:
    """납세증명서 유효기간: 발급일부터 30일. special(name): 신고·고지 후 납부기한이 30일 안에 오는 국세가 있으면
    그 지정납부기한까지로 줄이고 사유를 적는다 (국세징수법 시행령 제98조)."""
    issue = p.issue_date
    end, reason = issue + timedelta(days=29), None
    if special(rng, name, 0.12):
        due = next(((d, t) for d, t in _due_dates(issue, corp) if issue < d <= issue + timedelta(days=29)), None)
        if due:
            end, reason = due[0], f"{due[1]} 납부기한({D(due[0], 'kor_short')}) 도래"
    return f"{D(issue, 'kor')} ~ {D(end, 'kor')}", reason


def _deferrals(rng: random.Random, p: Profile, corp: bool) -> list[dict]:
    """연장ㆍ유예 명세 1~2건 (납부기한 연장 / 납부고지 유예 / 압류ㆍ매각의 유예)."""
    issue = p.issue_date
    rows = []
    for _ in range(rng.choice([1, 1, 2])):
        kind = rng.choice(["납부기한등 연장", "납부고지의 유예", "압류ㆍ매각의 유예"])
        item = rng.choice(["법인세", "부가가치세", "원천세"] if corp else ["종합소득세", "부가가치세", "부가가치세"])
        md = {"법인세": [(3, 31)], "종합소득세": [(5, 31)], "부가가치세": [(1, 25), (7, 25)],
              "원천세": [(m, 10) for m in range(1, 13)]}[item]
        lo = issue - timedelta(days=150 if kind != "압류ㆍ매각의 유예" else 420)
        hi = issue - timedelta(days=20 if kind != "압류ㆍ매각의 유예" else 80)
        cands = [date(y, m, d) for y in (issue.year - 2, issue.year - 1, issue.year) for m, d in md if lo <= date(y, m, d) <= hi]
        if not cands:
            continue
        due = rng.choice(cands)
        start = due + timedelta(days=1) if kind != "압류ㆍ매각의 유예" else due + timedelta(days=rng.randint(40, 70))
        end = start + timedelta(days=rng.choice([182, 273, 364]))
        if end <= issue:
            end = issue + timedelta(days=rng.randint(60, 200))
        if item == "법인세":
            tp = f"{due.year - 1}.01.01 ~ {due.year - 1}.12.31"
        elif item == "종합소득세":
            tp = f"{due.year - 1}년 귀속"
        elif item == "원천세":
            pm = due.month - 1 or 12
            tp = f"{due.year if due.month > 1 else due.year - 1}년 {pm}월"
        else:
            tp = f"{due.year}년 1기" if due.month == 7 else f"{due.year - 1}년 2기"
        amt = K.round_to(rng.uniform(0.6e6, 9e6) * (3 if corp else 1), 10)
        rows.append({"kind": kind, "period": f"{D(start, 'dot')} ~ {D(end, 'dot')}", "tax_period": tp, "tax_item": item,
                     "due": D(due, "dot"), "amount": won(amt, "")})
    return rows


def _national_cert(p: Profile, rng: random.Random, corp: bool) -> dict:
    valid, reason = _validity(rng, p, corp, "short_validity")
    out = {
        "issue_no": _hometax_no(rng),
        "valid_period": valid,
        "valid_reason": reason,
        **_purpose_pair(rng, p, corp),
        "arrears": "없음",
        "issue_date": D(p.issue_date, "kor"),
    }
    rows = _deferrals(rng, p, corp) if special(rng, "tax_deferral", 0.08) else []
    if rows:
        out["deferrals"] = rows
    else:
        out["deferral"] = "해당없음"
    return out


# ---------------------------------------------------------------------------
# 국세 납세증명서 (개인 / 법인)
# ---------------------------------------------------------------------------
@doc("tax_payment_certificate", "납세증명서(국세완납증명)", "tax")
def tax_payment_certificate(p: Profile, rng: random.Random) -> dict:
    """홈택스 발급 국세 납세증명서 (개인사업자).

    special short_validity: 유효기간 단축 + 사유, tax_deferral: 연장ㆍ유예 명세, emigration: 해외이주용.
    """
    b = p.business
    out = {
        "taxpayer": {
            "trade_name": b.name,
            "biz_no": b.biz_no,
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.85 else p.person.rrn,
            "address": p.person.address.road_full,
        },
        **_national_cert(p, rng, False),
        "issuer": _tax_office(p.person.address),
    }
    return out


@doc("tax_payment_certificate_corp", "납세증명서(법인)", "tax")
def tax_payment_certificate_corp(p: Profile, rng: random.Random) -> dict:
    """홈택스 발급 국세 납세증명서 (법인)."""
    c = p.corporation
    return {
        "taxpayer": {
            "corp_name": c.name,
            "biz_no": c.biz_no,
            "ceo": p.person.name,
            "corp_reg_no": c.corp_no,
            "address": c.address.road_full,
        },
        **_national_cert(p, rng, True),
        "issuer": _tax_office(c.address),
    }


# ---------------------------------------------------------------------------
# 지방세 납세증명서
# ---------------------------------------------------------------------------
@doc("local_tax_payment_certificate", "지방세 납세증명서", "tax")
def local_tax_payment_certificate(p: Profile, rng: random.Random) -> dict:
    """정부24·위택스 발급 지방세 납세증명서 (체납 없음). 개인사업자면 상호·사업자등록번호도 적는다.

    special local_deferral: 징수유예등 내역 1~2건 (재산세·자동차세·지방소득세), local_short_validity: 유효기간이
    30일 안에 오는 정기분 납기까지.
    """
    issue = p.issue_date
    taxpayer = {
        "name": p.person.name,
        "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.7 else p.person.rrn,
        "address": p.person.address.road_full,
    }
    if rng.random() < 0.4:
        taxpayer.update(trade_name=p.business.name, biz_no=p.business.biz_no)
    end = issue + timedelta(days=29)
    if special(rng, "local_short_validity", 0.08):
        cands = sorted(date(y, m, d) for y in (issue.year, issue.year + 1)
                       for m, d in ((6, 30), (7, 31), (8, 31), (9, 30), (12, 31)))
        end = next((d for d in cands if issue < d <= end), end)
    out = {
        "issue_no": issue_no(rng),
        "taxpayer": taxpayer,
        "valid_period": f"{D(issue, 'kor')} ~ {D(end, 'kor')}",
        "purpose": _cert_purpose(rng, p),
        "arrears": "없음",
        "issue_date": D(issue, "kor"),
        "issuer": district_office(p.person.address),
    }
    if special(rng, "local_deferral", 0.08):
        rows = []
        opts = [("재산세", 7, 31), ("재산세", 9, 30), ("자동차세", 6, 30), ("자동차세", 12, 31), ("지방소득세", 5, 31)]
        for item, m, d in rng.sample(opts, rng.choice([1, 1, 2])):
            due = date(issue.year, m, d)
            if due >= issue - timedelta(days=10):
                due = date(issue.year - 1, m, d)
            start = due + timedelta(days=rng.randint(-15, 5))
            if start + timedelta(days=180) <= issue:
                start = issue - timedelta(days=rng.randint(20, 150))
            amt = K.round_to(rng.uniform(1.2e5, 2.4e6), 10)
            rows.append({"tax_year": f"{due.year}", "tax_item": item, "due": D(due, "dot"), "amount": won(amt, ""),
                         "period": f"{D(start, 'dot')} ~ {D(start + timedelta(days=rng.choice([181, 273, 364])), 'dot')}"})
        out["deferrals"] = rows
    else:
        out["deferral"] = "해당없음"
    return out


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


def _land_tax(official: int) -> tuple[int, int]:
    """토지분 재산세(종합합산과세대상) (과세표준, 세액)."""
    base = int(official * 0.7) // 1000 * 1000
    if base <= 50_000_000:
        t = base * 0.002
    elif base <= 100_000_000:
        t = 100_000 + (base - 50_000_000) * 0.003
    else:
        t = 250_000 + (base - 100_000_000) * 0.005
    return base, _floor10(int(t))


_CAR_HANGUL = "가나다라마거너더러머버서어저고노도로모보소오조구누두루무부수우주"
_PREPAY_RATE = {2022: 9.15, 2023: 7, 2024: 5, 2025: 5, 2026: 5}
_LICENSED = {"한식": "일반음식점 영업신고", "커피전문점": "휴게음식점 영업신고", "제과": "제과점영업 신고",
             "미용": "미용업 신고", "학원": "학원 등록"}


def _new_car(rng: random.Random, year: int) -> dict:
    return {"no": f"{rng.randint(10, 399)}{rng.choice(_CAR_HANGUL)}{rng.randint(1000, 9999)}",
            "cc": rng.choice([998, 1353, 1591, 1598, 1999, 2151, 2497, 3342, 3470]), "model_year": year}


def _car_annual(car: dict, y: int) -> int:
    age = y - car["model_year"] + 1
    cut = min(max(age - 2, 0) * 5, 50)
    per_cc = 80 if car["cc"] <= 1000 else 140 if car["cc"] <= 1600 else 200
    return car["cc"] * per_cc * (100 - cut) // 100


@doc("local_tax_assessment", "지방세 세목별 과세증명서", "tax")
def local_tax_assessment(p: Profile, rng: random.Random) -> dict:
    """주소지 시·군·구청장이 발급하는 지방세 세목별 과세증명서 (재산세·자동차세·주민세 등).

    heavy: 4~5개 연도 + 물건 여러 개(토지·두 번째 주택, 자동차 2대, 등록면허세), 2~3쪽.
    special: car_replaced(차량 교체, 일할 과세), car_prepay(자동차세 연납), biz_resident_tax(주민세 사업소분),
             local_income_tax(지방소득세 종합소득분), second_house(2주택: 일반세율).
    """
    a = p.person.address
    prop = p.property
    issue = p.issue_date
    many = heavy(rng, 0.3)
    growth = _prng(p, "official_price").uniform(-0.03, 0.08)
    second = None
    if special(rng, "second_house", 0.08) or (many and rng.random() < 0.4):
        w_off = rng.uniform(0.25, 0.6)
        second = {"official": K.round_to(prop.official_price * w_off, 1_000_000),
                  "object": f"{a.sigungu or a.sido} {rng.choice(['신정동', '중앙동', '송정동', '양지동'])} {rng.randint(10, 990)}-{rng.randint(1, 30)}"}
    land = None
    if many and rng.random() < 0.5:
        land = {"official": K.round_to(rng.uniform(4e7, 3.5e8), 100_000),
                "object": f"{rng.choice(['경기도 양평군 양서면', '강원특별자치도 홍천군 서면', '충청남도 당진시 송악읍', '경기도 이천시 마장면'])} {rng.randint(100, 999)}"}
    one_house = second is None and rng.random() < 0.8
    cars = []
    if rng.random() < 0.75 or many:
        cars.append(dict(_new_car(rng, rng.randint(issue.year - 12, issue.year - 1)), since=None, until=None))
        if many and rng.random() < 0.6:
            cars.append(dict(_new_car(rng, rng.randint(issue.year - 8, issue.year - 1)), since=None, until=None))
    n_years = rng.randint(4, 5) if many else (2 if rng.random() < 0.6 else 3)
    years = list(range(issue.year - n_years + 1, issue.year + 1))
    if cars and special(rng, "car_replaced", 0.12):
        sold = rand_date(rng, date(years[0], 2, 1), min(issue - timedelta(days=40), date(issue.year, 11, 30)))
        cars[0]["until"] = sold
        cars.append(dict(_new_car(rng, sold.year), since=sold + timedelta(days=1), until=None))
    prepay = bool(cars) and special(rng, "car_prepay", 0.15)
    seoul = a.sido == "서울특별시"
    edu_rate = 25 if seoul else 10
    resident_tax = 6_000 if seoul else rng.choice([5_000, 7_000, 10_000])
    biz = p.business
    biz_tax = special(rng, "biz_resident_tax", 0.25) and _revenue(p, issue.year - 1) >= 80_000_000
    local_income = special(rng, "local_income_tax", 0.2)
    license_tax = biz.biz_item in _LICENSED and (many or rng.random() < 0.15)
    lic_amt = rng.choice([18_000, 27_000, 40_500, 54_000, 67_500])

    rows: list[tuple[date, dict]] = []

    def add(due, item, kind, obj, base, tax, edu):
        rows.append((due, {"tax_item": item, "kind": kind, "object": obj, "base": base, "tax": tax, "edu": edu}))

    for y in years:
        official = K.round_to(prop.official_price * (1 + growth) ** (y - issue.year), 1_000_000)
        pa = prop.address
        houses = [(official, f"{pa.sigungu or pa.sido} {pa.dong} {pa.jibun}")]
        if second:
            houses.append((K.round_to(second["official"] * (1 + growth) ** (y - issue.year), 1_000_000), second["object"]))
        for off, obj in houses:
            base, ptax = _property_tax(off, one_house)
            if ptax <= 200_000:
                parts = [(date(y, 7, 31), "정기분", ptax)]
            else:
                half = _floor10(ptax // 2)
                parts = [(date(y, 7, 31), "정기분(1/2)", half), (date(y, 9, 30), "정기분(2/2)", ptax - half)]
            for due, label, t in parts:
                add(due, "재산세(주택)", label, obj, won(base, ""), t, _floor10(t * 20 // 100))
        if land:
            lbase, ltax = _land_tax(int(land["official"] * (1 + growth / 2) ** (y - issue.year)))
            add(date(y, 9, 30), "재산세(토지)", "정기분", land["object"], won(lbase, ""), ltax, _floor10(ltax * 20 // 100))
        for car in cars:
            if car["since"] and car["since"].year > y or car["until"] and car["until"].year < y:
                continue
            annual = _car_annual(car, y)
            obj, base = f"{car['no']} 승용", f"{car['cc']:,}cc"
            if prepay and not car["since"] and not car["until"]:
                rate = _PREPAY_RATE.get(y, 5)
                t = _floor10(int(annual * (100 - rate) / 100))
                add(date(y, 1, 31), "자동차세", "연납", obj, base, t, _floor10(t * 30 // 100))
                continue
            for h, (s, e) in enumerate(((date(y, 1, 1), date(y, 6, 30)), (date(y, 7, 1), date(y, 12, 31))), 1):
                lo, hi = max(s, car["since"] or s), min(e, car["until"] or e)
                if lo > hi:
                    continue
                full = (e - s).days + 1
                days = (hi - lo).days + 1
                t = _floor10(annual // 2 * days // full)
                add(e, "자동차세", f"{h}기분" + ("(일할)" if days < full else ""), obj, base, t, _floor10(t * 30 // 100))
        add(date(y, 8, 31), "주민세(개인분)", "정기분", "세대주 개인분", "-", resident_tax,
            _floor10(resident_tax * edu_rate // 100))
        if biz_tax and y >= max(biz.established.year + 1, 2021):
            add(date(y, 8, 31), "주민세(사업소분)", "정기분", f"사업소 {biz.address.road_short}", "-", 50_000,
                _floor10(50_000 * edu_rate // 100))
        if license_tax and y > biz.established.year:
            add(date(y, 1, 31), "등록면허세(면허)", "정기분", _LICENSED[biz.biz_item], "-", lic_amt, _floor10(lic_amt * 30 // 100))
        if local_income and y - 1 >= biz.established.year:
            calc = _itr_calc(p, y - 1)
            t = _floor10(calc["determined"] // 10)
            add(date(y, 5, 31), "지방소득세", "확정신고", f"{y - 1}년 귀속 종합소득", won(calc["base"], ""), t, 0)
    rows = sorted(((due, r) for due, r in rows if due < issue), key=lambda x: x[0])
    if not many:
        rows = rows[-10:]
    tot_tax = sum(r["tax"] for _, r in rows)
    tot_edu = sum(r["edu"] for _, r in rows)
    items = []
    for due, r in rows:
        items.append({"tax_item": r["tax_item"], "levied": f"{due.year}.{due.month:02d}", "kind": r["kind"],
                      "object": r["object"], "base": r["base"], "tax": won(r["tax"], ""), "edu": won(r["edu"], ""),
                      "total": won(r["tax"] + r["edu"], "")})
    first, last = rows[0][0].year, rows[-1][0].year
    return {
        "issue_no": issue_no(rng),
        "taxpayer": {
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.6 else p.person.rrn,
            "address": a.road_full,
        },
        "period": f"{first}년 ~ {last}년" if first < last else f"{first}년",
        "items": items,
        "sum": {"tax": won(tot_tax, ""), "edu": won(tot_edu, ""), "total": won(tot_tax + tot_edu, "")},
        "purpose": _cert_purpose(rng, p),
        "issue_date": D(issue, "kor"),
        "issuer": district_office(a),
    }


# ---------------------------------------------------------------------------
# 부가가치세 과세표준증명
# ---------------------------------------------------------------------------
_EXEMPT_ITEMS = ("학원", "농산물")


def _vat_periods(p: Profile) -> list[dict]:
    """과세기간 목록 (오래된 것부터). 간이과세자는 1년, 일반과세자는 반기. 간이→일반 전환(_biz_facts switch)이면
    전환 전은 간이(전환 연도는 1.1~6.30), 이후 일반."""
    b, issue = p.business, p.issue_date
    sw = _biz_facts(p)["switch"]
    simple_now = _vat_simple(p)
    out = []
    for y in range(b.established.year, issue.year + 1):
        simple_y = simple_now or (sw is not None and y < sw.year)
        if simple_y:
            start = max(date(y, 1, 1), b.established)
            out.append({"start": start, "end": date(y, 12, 31), "due": date(y + 1, 1, 25), "simple": True,
                        "base": _half_base(p, y, 1) + _half_base(p, y, 2), "y": y, "h": 0})
            continue
        for h in (1, 2):
            start = max(date(y, 1, 1) if h == 1 else date(y, 7, 1), b.established)
            end = date(y, 6, 30) if h == 1 else date(y, 12, 31)
            if start > end:
                continue
            simple_h = sw is not None and y == sw.year and h == 1
            out.append({"start": start, "end": end, "due": date(y, 7, 25) if h == 1 else date(y + 1, 1, 25),
                        "simple": simple_h, "base": _half_base(p, y, h), "y": y, "h": h})
    return [r for r in out if r["due"] < issue]


@doc("vat_tax_base_certificate", "부가가치세 과세표준증명", "tax")
def vat_tax_base_certificate(p: Profile, rng: random.Random) -> dict:
    """홈택스 발급 부가가치세 과세표준증명 (개인사업자).

    heavy: 3~5년치(일반 6~10기간). special: vat_prelim(예정신고 분리), vat_amended(수정신고 줄 추가),
    vat_late(기한후신고), vat_refund(시설투자 환급). 휴업(_biz_facts suspended) 기간은 매출 0 또는 감소,
    간이→일반 전환(simple_to_general)이면 앞쪽 기간이 1년 단위 간이과세 기간.
    """
    b = p.business
    issue = p.issue_date
    va_rate = _industry(b)[1]
    many = heavy(rng, 0.25)
    periods = _vat_periods(p)
    n_simple = rng.randint(4, 6) if many else 3
    n_general = rng.randint(6, 10) if many else 4
    keep = []
    for r in reversed(periods):
        if len(keep) >= (n_simple if r["simple"] and all(k["simple"] for k in keep) else n_general):
            break
        keep.append(r)
    keep.reverse()
    rows = []
    for r in keep:
        base = r["base"]
        if r["simple"]:
            full = (r["end"] - r["start"]).days > 200
            tax = 0 if base < (48_000_000 if full else 24_000_000) else \
                max(0, _floor10(int(base * va_rate * 0.1) - int(base * 0.7 * 0.013)))
        else:
            pl = _pl(p, r["y"])
            buy_ratio = (pl["cogs"] + pl["rent"] + pl["other_sga"] // 2) / max(pl["revenue"], 1)
            buy_ratio *= _prng(p, "vatbuy", r["y"], r["h"]).uniform(0.9, 1.1)
            card = int(base * 0.6 * 0.013) if b.biz_type in ("음식점업", "소매업") else 0
            tax = _floor10(int(base * 0.1 * (1 - buy_ratio)) - min(card, 5_000_000))
        filed = rand_date(rng, r["end"] + timedelta(days=5), min(r["due"], issue - timedelta(days=1)))
        rows.append({"start": r["start"], "end": r["end"], "kind": "정기확정", "filed": filed, "base": base, "tax": tax,
                     "due": r["due"], "simple": r["simple"]})
    general = [i for i, r in enumerate(rows) if not r["simple"] and r["base"] > 0]
    if general and special(rng, "vat_prelim", 0.1):  # 예정신고를 한 기간: 예정(1~3월) + 확정(4~6월)
        for i in sorted(rng.sample(general[-2:], min(2, len(general[-2:]))), reverse=True):
            r = rows[i]
            mid = date(r["start"].year, 3, 31) if r["end"].month == 6 else date(r["start"].year, 9, 30)
            if r["start"] > mid:
                continue
            share = rng.uniform(0.42, 0.55)
            pb = _floor10(int(r["base"] * share))
            pt = _floor10(int(r["tax"] * share))
            pre = {"start": r["start"], "end": mid, "kind": "예정신고", "base": pb, "tax": pt, "simple": False,
                   "filed": rand_date(rng, mid + timedelta(days=5), mid + timedelta(days=25)), "due": mid + timedelta(days=25)}
            rows[i] = dict(r, start=mid + timedelta(days=1), base=r["base"] - pb, tax=r["tax"] - pt)
            rows.insert(i, pre)
    if rows and special(rng, "vat_late", 0.06):
        i = rng.randrange(len(rows))
        r = rows[i]
        late = r["due"] + timedelta(days=rng.randint(5, 60))
        if late < issue:
            r.update(kind="기한후신고", filed=late)
    general = [i for i, r in enumerate(rows) if not r["simple"] and r["kind"] == "정기확정"]
    if general and special(rng, "vat_refund", 0.08):
        r = rows[rng.choice(general)]
        r["tax"] = -K.round_to(rng.uniform(2e6, 1.5e7), 10)
    if rows and special(rng, "vat_amended", 0.1):
        i = rng.randrange(len(rows))
        r = rows[i]
        filed = r["filed"] + timedelta(days=rng.randint(30, 200))
        if filed < issue:
            k = rng.uniform(1.02, 1.12)
            nb = _floor10(int(r["base"] * k))
            nt = r["tax"] + _floor10(int((nb - r["base"]) * 0.1))
            rows.insert(i + 1, dict(r, kind="수정신고", filed=filed, base=nb, tax=nt))
    fmt = rng.choice(["dash", "dot"])
    # 학원(교육용역)·농산물은 면세 매출이 대부분인 과·면세 겸영사업자로 본다.
    exempt_share = _prng(p, "vatexempt").uniform(0.85, 0.97) if b.biz_item in _EXEMPT_ITEMS else 0.0
    items = []
    for r in rows:
        exempt = _floor10(int(r["base"] * exempt_share))
        taxable = r["base"] - exempt
        tax = _floor10(int(r["tax"] * (1 - exempt_share))) if r["tax"] > 0 else r["tax"]
        items.append({"period": f"{D(r['start'], fmt)} ~ {D(r['end'], fmt)}", "kind": r["kind"],
                      "filed": D(r["filed"], fmt), "base_total": won(r["base"], ""), "base_taxable": won(taxable, ""),
                      "base_exempt": won(exempt, ""), "tax": _signed(tax)})
    return {
        "issue_no": _hometax_no(rng),
        "taxpayer": {
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn),
            "trade_name": b.name,
            "biz_no": b.biz_no,
            "address": b.address.road_full,
            "biz_type": b.biz_type,
            "biz_item": b.biz_item,
        },
        "items": items,
        "purpose": _cert_purpose(rng, p),
        "issue_date": D(issue, "kor"),
        "issuer": _tax_office(b.address),
    }


# ---------------------------------------------------------------------------
# 종합소득세 과세표준확정신고 및 납부계산서
# ---------------------------------------------------------------------------
def _wage_deduction(g: int) -> int:
    """근로소득공제."""
    if g <= 5_000_000:
        return g * 70 // 100
    if g <= 15_000_000:
        return 3_500_000 + (g - 5_000_000) * 40 // 100
    if g <= 45_000_000:
        return 7_500_000 + (g - 15_000_000) * 15 // 100
    if g <= 100_000_000:
        return 12_000_000 + (g - 45_000_000) * 5 // 100
    return min(14_750_000 + (g - 100_000_000) * 2 // 100, 20_000_000)


def _reduce_rate(months: int) -> float:
    """수정신고 과소신고가산세 감면율 (법정신고기한 경과 개월 수)."""
    for m, r in ((1, 0.9), (3, 0.75), (6, 0.5), (12, 0.3), (18, 0.2), (24, 0.1)):
        if months <= m:
            return r
    return 0.0


_ITR_CACHE: dict = {}


def _itr_calc(p: Profile, y: int) -> dict:
    """y년 귀속 종합소득세 계산 (프로필 고정). 지방세 과세증명의 지방소득세(종합소득분)도 이 값을 쓴다.

    heavy itr_many: 소득 종류 다수(근로·부동산임대·이자배당·기타). special itr_wage / itr_rental / itr_other: 한 가지 추가.
    """
    key = (p.seed, y, p.issue_date, os.environ.get("DOCGEN_SPECIAL", ""), os.environ.get("DOCGEN_HEAVY", ""))
    if key in _ITR_CACHE:
        return _ITR_CACHE[key]
    r = _prng(p, "itr", y)
    b, fx = p.business, _biz_facts(p)
    filing = _itr_filing(p, y)
    many = heavy(r, 0.25)
    pl = _pl(p, y)
    share = fx["joint"]["own_share"] if fx["joint"] else 100
    rev = pl["revenue"] * share // 100
    biz_income = pl["net"] * share // 100
    code = _industry(b)[2]
    incomes = [{"type": "사업소득", "payer": b.name, "revenue": rev, "expense": rev - biz_income, "amount": biz_income,
                "withheld": 0}]
    wage = special(r, "itr_wage", 0.1) or (many and r.random() < 0.5)
    rental = special(r, "itr_rental", 0.08) or (many and r.random() < 0.5)
    fin = many and r.random() < 0.4
    other = special(r, "itr_other", 0.08) or (many and r.random() < 0.5)
    wage_gross = 0
    if wage:
        g = K.round_to(r.uniform(1.8e7, 4.8e7), 10_000)
        wage_gross = g
        ded = _wage_deduction(g)
        emp = f"(주){r.choice(['한빛', '대성', '미래', '세진', '우진', '다온'])}{r.choice(['산업', '테크', '물산', '푸드'])}"
        incomes.append({"type": "근로소득", "payer": emp, "revenue": g, "expense": ded, "amount": g - ded,
                        "withheld": _floor10(int(g * r.uniform(0.012, 0.04)))})
    if rental:
        rv = r.choice([60, 80, 100, 120, 150, 200, 250]) * 10_000 * 12
        ex = _floor10(int(rv * r.uniform(0.25, 0.45)))
        incomes.append({"type": "부동산임대업소득", "payer": f"{p.property.address.sigungu or p.property.address.sido} 주택임대",
                        "revenue": rv, "expense": ex, "amount": rv - ex, "withheld": 0})
    if fin:
        it = K.round_to(r.uniform(1.3e7, 2.4e7), 10)
        dv = K.round_to(r.uniform(5e6, 1.5e7), 10)
        incomes.append({"type": "이자소득", "payer": p.accounts[0].bank, "revenue": it, "expense": 0, "amount": it,
                        "withheld": _floor10(it * 14 // 100)})
        incomes.append({"type": "배당소득", "payer": r.choice(["삼성전자(주)", "(주)케이티앤지", "현대자동차(주)", "에스케이텔레콤(주)"]),
                        "revenue": dv, "expense": 0, "amount": dv, "withheld": _floor10(dv * 14 // 100)})
    if other:
        orv = K.round_to(r.uniform(3e6, 9e6), 1000)
        oex = orv * 60 // 100
        incomes.append({"type": "기타소득", "payer": r.choice(["한국생산성본부", "(사)한국외식업중앙회", "○○대학교 산학협력단", "한국방송공사"]),
                        "revenue": orv, "expense": oex, "amount": orv - oex, "withheld": _floor10((orv - oex) * 20 // 100)})
    total_income = sum(i["amount"] for i in incomes)

    # 인적공제 대상자
    deps = [{"relation": "본인", "person": p.person, "extra": None}]
    if p.spouse and r.random() < 0.5:
        deps.append({"relation": "배우자", "person": p.spouse, "extra": None})
    for c in p.children:
        if c.birth.year <= y and y - c.birth.year < 20:
            deps.append({"relation": "자녀", "person": c, "extra": None})
    for rel, par in (("부", p.father), ("모", p.mother)):
        if y - par.birth.year >= 60 and r.random() < (0.5 if many else 0.25):
            deps.append({"relation": rel, "person": par, "extra": "경로우대" if y - par.birth.year >= 70 else None})
    personal = 1_500_000 * len(deps)
    extra = 1_000_000 * sum(1 for d in deps if d["extra"])
    pension = _floor10(min(total_income // 12, 6_170_000) * 9 // 100 * 12)
    yellow = 0
    if r.random() < 0.55:
        limits = (6_000_000, 4_000_000) if y >= 2025 else (5_000_000, 3_000_000)
        lim = limits[0] if biz_income <= 40_000_000 else limits[1] if biz_income <= 100_000_000 else 2_000_000
        yellow = min(r.choice([1_200_000, 2_400_000, 3_000_000, 3_600_000, 6_000_000]), lim)
    ded_items = [("기본공제", personal)]
    if extra:
        ded_items.append(("추가공제", extra))
    ded_items.append(("연금보험료공제", pension))
    if wage_gross:
        ded_items.append(("특별소득공제(보험료)", _floor10(wage_gross * 45 // 1000)))
    if yellow:
        ded_items.append(("소기업ㆍ소상공인 공제부금 소득공제", yellow))
    claim = filing["kind"] == "경정청구"
    missed = None
    if claim:  # 경정청구: 당초 신고에서 빠뜨린 공제를 추가
        missed = ("소기업ㆍ소상공인 공제부금 소득공제", 3_000_000) if not yellow else ("추가공제", 1_000_000)
        ded_items.append(missed)
    deduction = sum(a for _, a in ded_items)
    base = max(0, total_income - deduction)
    computed, rate, _ = _income_tax(base)
    paper = filing["kind"] == "정기신고" and r.random() < 0.2
    kids = sum(1 for c in p.children if c.birth.year <= y and 8 <= y - c.birth.year < 20)
    credits = []
    if kids:
        one, two, more = (250_000, 550_000, 400_000) if y >= 2025 else (150_000, 350_000, 300_000)
        credits.append(("자녀세액공제", one if kids == 1 else two + more * (kids - 2)))
    if wage_gross:
        wt = computed * incomes[1]["amount"] // max(total_income, 1)
        credits.append(("근로소득세액공제", min(_floor10(wt * 55 // 100), 660_000)))
    credits.append(("표준세액공제", 70_000))
    if not paper:
        credits.append(("전자신고세액공제", 20_000))
    credit = min(computed, sum(a for _, a in credits))
    determined = computed - credit
    withheld = sum(i["withheld"] for i in incomes)
    mid = _floor10(int(determined * r.uniform(0.25, 0.45))) if y > b.established.year else 0
    prepaid_items = []
    if mid:
        prepaid_items.append(("중간예납세액", mid))
    if withheld:
        prepaid_items.append(("원천징수세액", withheld))
    penalties = []
    deadline = date(y + 1, 6, 30) if _bookkeeping_double(p) and _sincere_filer(p) else date(y + 1, 5, 31)
    if filing["kind"] == "기한후신고":
        days = filing["late_days"]
        unpaid = max(0, determined - mid - withheld)
        penalties.append(("무신고가산세", _floor10(int(unpaid * 0.2 * (0.5 if days <= 30 else 0.7 if days <= 90 else 0.8)))))
        penalties.append(("납부지연가산세", _floor10(unpaid * 22 * days // 100_000)))
    elif filing["kind"] == "수정신고":
        added = _floor10(int(determined * r.uniform(0.08, 0.25)))
        days = (filing["filed"] - deadline).days
        penalties.append(("과소신고가산세", _floor10(int(added * 0.1 * (1 - _reduce_rate(max(1, days // 30)))))))
        penalties.append(("납부지연가산세", _floor10(added * 22 * max(days, 0) // 100_000)))
        prepaid_items.append(("당초 신고 납부세액", max(0, determined - added - mid - withheld)))
    elif claim:
        old_det = computed - credit + _income_tax(base + missed[1])[0] - computed
        prepaid_items.append(("당초 신고 납부세액", max(0, old_det - mid - withheld)))
    penalty = sum(a for _, a in penalties)
    total = determined + penalty
    prepaid = sum(a for _, a in prepaid_items)
    payable = total - prepaid
    if payable > 0:
        payable = _floor10(payable)
    installment = 0
    if payable > 10_000_000 and filing["kind"] == "정기신고" and r.random() < 0.6:
        installment = payable - 10_000_000 if payable <= 20_000_000 else _floor10(payable // 2)
    double = _bookkeeping_double(p)
    if double:
        filing_type = "성실신고확인" if _sincere_filer(p) else r.choice(["자기조정", "외부조정"])
    else:
        filing_type = r.choices(["간편장부", "추계-기준율", "추계-단순율"], [8, 1, 1])[0]
    agent = filing_type in ("외부조정", "성실신고확인") or special(r, "itr_tax_agent", 0.3)
    paper = paper and not agent
    out = {
        "filing": filing, "many": many, "incomes": incomes, "deps": deps, "ded_items": ded_items, "credits": credits,
        "penalties": penalties, "prepaid_items": prepaid_items, "total_income": total_income, "deduction": deduction,
        "base": base, "rate": rate, "computed": computed, "credit": credit, "determined": determined, "penalty": penalty,
        "total": total, "prepaid": prepaid, "payable": payable, "installment": installment, "filing_type": filing_type,
        "bookkeeping": "복식부기의무자" if double else "간편장부대상자", "agent": agent, "paper": paper, "share": share,
        "code": code, "detail": many or len(incomes) > 1 or filing["kind"] != "정기신고" or bool(fx["joint"]) or r.random() < 0.3,
    }
    _ITR_CACHE[key] = out
    return out


class _Doc(dict):
    """서류 데이터. 화면 구성 선택(손글씨 서면 신고 등)은 값이 아니라 속성으로 둔다 (정답에 들어가지 않음)."""
    paper = False


@doc("income_tax_return", "종합소득세 과세표준확정신고 및 납부계산서", "tax")
def income_tax_return(p: Profile, rng: random.Random) -> dict:
    """종합소득세 확정신고서. 제1쪽(기본사항 + 환급금 계좌 + 세액의 계산)은 항상, 명세(제2·3쪽)는 소득이 여럿이거나
    수정신고·기한후신고·경정청구·공동사업 등일 때 붙는다. 사업소득금액은 표준손익계산서 당기순이익(공동사업이면 지분만큼)과 같다.

    현행 서식은 종합소득세ㆍ농어촌특별세만 적는다 (지방소득세는 별도 신고서).
    paper: 손으로 쓴 서면 신고서(전자신고세액공제 없음) — 템플릿이 손글씨체 + 정정 효과를 쓴다.
    """
    b = p.business
    y = max(_filed_year(p), b.established.year)
    c = _itr_calc(p, y)
    filing = c["filing"]
    w = lambda n: _signed(n)  # noqa: E731
    out = {
        "tax_year": f"{y}",
        "residency": "거주자",
        "nationality": "내국인",
        "taxpayer": {
            "name": p.person.name,
            "rrn": p.person.rrn if c["paper"] or rng.random() < 0.5 else K.mask_rrn(p.person.rrn),
            "address": p.person.address.road_full,
            "email": p.person.email,
            "biz_phone": b.phone,
            "mobile": p.person.mobile,
        },
        "filing_type": c["filing_type"],
        "bookkeeping": c["bookkeeping"],
        "filing_kind": filing["kind"],
        "national": {
            "total_income": w(c["total_income"]), "deduction": w(c["deduction"]), "base": w(c["base"]), "rate": f"{c['rate']}%",
            "computed": w(c["computed"]), "reduction": "0", "credit": w(c["credit"]), "determined": w(c["determined"]),
            "penalty": w(c["penalty"]), "additional": "0", "total": w(c["total"]), "prepaid": w(c["prepaid"]),
            "payable": w(c["payable"]), "special_deduct": "0", "special_add": "0", "installment": w(c["installment"]),
            "due_payable": w(c["payable"] - c["installment"]),
        },
        "filed_date": D(filing["filed"], rng.choice(["kor", "kor_short"])),
        "tax_office": _tax_office(p.person.address),
    }
    out = _Doc(out)
    out.paper = c["paper"]  # 화면 구성 선택 (정답 값 아님)
    if c["payable"] < 0 or rng.random() < 0.5:
        acc = p.accounts[0]
        out["refund_account"] = {"bank": acc.bank, "number": acc.number}
    if c["agent"]:
        ag = _side_person(f"tax-agent:{p.seed}")
        out["tax_agent"] = {"name": ag.name, "biz_no": K.biz_no(_prng(p, "agent-biz")),
                            "phone": K.landline(_prng(p, "agent-tel"), b.address.sido)}
    if c["detail"]:
        fx = _biz_facts(p)
        out["incomes"] = [{"type": i["type"], "payer": i["payer"], "revenue": w(i["revenue"]), "expense": w(i["expense"]),
                           "amount": w(i["amount"]), "withheld": w(i["withheld"])} for i in c["incomes"]]
        bi = c["incomes"][0]
        out["business_income"] = {"address": b.address.road_full, "trade_name": b.name, "biz_no": b.biz_no, "code": c["code"],
                                  "revenue": w(bi["revenue"]), "expense": w(bi["expense"]), "income": w(bi["amount"])}
        if fx["joint"]:
            out["business_income"]["share"] = f"{c['share']}%"
            out["business_income"]["partner"] = fx["joint"]["name"]
        mask = not c["paper"] and rng.random() < 0.6
        out["dependents"] = [{"relation": d["relation"], "name": d["person"].name,
                              "rrn": K.mask_rrn(d["person"].rrn) if mask else d["person"].rrn,
                              "basic": "○", "extra": d["extra"]} for d in c["deps"]]
        out["deduction_items"] = [{"item": n, "amount": w(a)} for n, a in c["ded_items"]]
        out["credit_items"] = [{"item": n, "amount": w(a)} for n, a in c["credits"]]
        if c["penalties"]:
            out["penalty_items"] = [{"item": n, "amount": w(a)} for n, a in c["penalties"]]
        if c["prepaid_items"]:
            out["prepaid_items"] = [{"item": n, "amount": w(a)} for n, a in c["prepaid_items"]]
    return out
