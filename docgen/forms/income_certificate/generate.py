"""income_certificate: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/income.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.income import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _biz_no,
    _income_tax_calc,
    _ins_rates,
    _latest_tax_year,
    _months_between,
    _t10,
    _work_history,
    _year_end,
)
from docgen.registry import doc


@doc("income_certificate", "소득금액증명원", "income")
def income_certificate(p: Profile, rng: random.Random) -> dict:
    """국세청(홈택스) 발급 소득금액증명.

    2022.9.22. 서식 개정으로 종전 5종(종합소득세 신고자용·근로소득자용 등)이 1종으로 통합되어,
    '종합소득세 신고 현황'(소득구분별 수입금액·소득금액)과 '연말정산 현황'(원천징수의무자별
    소득금액(과세대상급여액)·총결정세액)을 한 장에 표시한다.
    """
    e = p.employment
    latest = _latest_tax_year(p)
    prior = [h for h in _work_history(p) if h["kind"] == "work" and not h.get("current")]
    if heavy(rng, 0.25):  # 여러 해(4~5년) 증명 — 이전 직장 소득까지 나온다
        n = rng.randint(4, 5)
    else:
        n = min(rng.choice([1, 2, 3, 3]), latest - e.hire_date.year + 1)
    # 특수 상황: 이직 — 이전 직장 소득이 나오는 해까지 증명기간을 넓힌다
    if special(rng, "job_change", 0.15) and prior and latest - prior[-1]["end"].year + 1 <= 5:
        n = max(n, latest - prior[-1]["end"].year + 1)
    n = max(1, n)
    years = list(range(latest, latest - n, -1))
    rows = []
    for y in years:
        if y >= e.hire_date.year:
            t = _year_end(p, y)
            rows.append({"year": f"{y}", "income_type": "근로", "payer": e.company.name, "payer_biz_no": e.company.biz_no,
                         "amount": won(t["taxable"], ""), "tax": won(t["final"], "")})
        for h in reversed(prior):
            ys, ye = max(h["start"], date(y, 1, 1)), min(h["end"] - timedelta(days=1), date(y, 12, 31))
            if ys > ye:
                continue
            amt = K.round_to(h["wage"] * _months_between(ys, ye + timedelta(days=1)), 10)
            pr_, hr_, lr_ = _ins_rates(y)
            tax = _income_tax_calc(amt, _t10(amt * pr_), _t10(amt * (hr_ * (1 + lr_) + 0.009)), 1, 0)["final"]
            rows.append({"year": f"{y}", "income_type": "근로", "payer": h["name"],
                         "payer_biz_no": _biz_no(random.Random(f"biz:{h['name']}")),
                         "amount": won(amt, ""), "tax": won(tax, "")})
    if not rows:  # 이력상 소득이 없는 해만 고른 경우: 최근 연도로 되돌린다
        years = [latest]
        t = _year_end(p, latest)
        rows.append({"year": f"{latest}", "income_type": "근로", "payer": e.company.name, "payer_biz_no": e.company.biz_no,
                     "amount": won(t["taxable"], ""), "tax": won(t["final"], "")})
    d = {
        "issue_no": f"{rng.randint(1000, 9999)}-{rng.randint(100, 999)}-{rng.randint(1000, 9999)}-{rng.randint(100, 999)}",
        "taxpayer": {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn, rng.choice([1, 7])),
                     "address": p.person.address.road_full},
        "period": f"{years[-1]}년 ~ {years[0]}년" if len(years) > 1 else f"{years[0]}년",
        "rows": rows,
        "purpose": rng.choice(["금융기관 제출용", "대출용", "은행 제출용"]),
        "submit_to": p.bank,
        "issue_date": D(p.issue_date, "kor_short"),
        "issuer": tax_office(p.person.address),
    }
    filing = []
    if rng.random() < 0.2:  # 의료비 등 추가 공제를 위해 종합소득세 확정신고를 한 경우
        y = years[0]
        t = _year_end(p, y) if y >= e.hire_date.year else None
        if t:
            filing.append({"year": f"{y}", "income_type": "근로", "revenue": won(t["taxable"], ""), "income": won(t["earned"], "")})
    # 특수 상황: 부업(프리랜서 사업소득·강연료 등 기타소득)이 있어 종합소득세를 신고한 경우
    if special(rng, "side_income", 0.15):
        filing = []
        for y in years[:rng.randint(1, min(3, len(years)))]:
            if y >= e.hire_date.year:
                t = _year_end(p, y)
                filing.append({"year": f"{y}", "income_type": "근로", "revenue": won(t["taxable"], ""), "income": won(t["earned"], "")})
            if rng.random() < 0.6:
                rev = K.round_to(rng.uniform(2_000_000, 25_000_000), 10)
                filing.append({"year": f"{y}", "income_type": "사업", "revenue": won(rev, ""), "income": won(_t10(rev * (1 - 0.641)), "")})
            else:
                rev = K.round_to(rng.uniform(500_000, 8_000_000), 10)
                filing.append({"year": f"{y}", "income_type": "기타", "revenue": won(rev, ""), "income": won(_t10(rev * 0.4), "")})
    if filing:
        d["filing_rows"] = filing
    return d
