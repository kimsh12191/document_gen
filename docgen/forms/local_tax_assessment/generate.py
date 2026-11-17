"""local_tax_assessment: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/tax.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.business import _prng, _revenue  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.docs.tax import _cert_purpose, _floor10, _itr_calc  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


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
