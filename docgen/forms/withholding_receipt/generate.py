"""withholding_receipt: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/income.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.income import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _MEAL,
    _biz_no,
    _company_name,
    _dependents,
    _income_tax_calc,
    _ins_rates,
    _latest_tax_year,
    _months_between,
    _t10,
    _work_history,
    _year_end,
)
from docgen.registry import doc


@doc("withholding_receipt", "근로소득 원천징수영수증", "income")
def withholding_receipt(p: Profile, rng: random.Random) -> dict:
    """근로소득 원천징수영수증(근로소득 지급명세서) 제1쪽 — 소득세법 시행규칙 [별지 제24호서식(1)].

    제1쪽 구성: 관리번호·영수증/지급명세서 구분·보관용 구분 / 거주구분 등 / 징수의무자 ①~⑤ / 소득자 ⑥~⑧ /
    Ⅰ 근무처별 소득명세 ⑨~⑯ / Ⅱ 비과세 및 감면 소득 명세 / Ⅲ 세액명세 (72)~(76)·실효세율 / 영수 문구·서명.
    (정산명세 ㉑~ 는 제2쪽이라 표시하지 않는다.)
    """
    e = p.employment
    c = e.company
    y = _latest_tax_year(p)
    t = _year_end(p, y)
    w = lambda n: won(n, "")  # noqa: E731
    issued = date(y + 1, 2, 28) + timedelta(days=rng.randint(0, 20))
    if issued > p.issue_date:
        issued = p.issue_date
    taxable, final, prepaid = t["taxable"], t["final"], t["prepaid"]
    nontax_total = t["nontax"]
    work = {
        "company": c.name, "biz_no": c.biz_no,
        "period": f"{D(t['start'], 'dot')}~{D(t['end'], 'dot')}",
        "salary": w(t["salary"]), "bonus": w(t["bonus"]), "total": w(t["taxable"]),
    }
    nontax = {"meal": w(t["nontax"])}
    extra = {}
    # 특수 상황: 종(전) 근무지 합산 — 그해 이직했거나(중도 입사), 다른 회사에서 함께 근로소득이 있었던 경우
    if special(rng, "prev_employer", 0.2):
        hist = [h for h in _work_history(p) if h["kind"] == "work" and not h.get("current")]
        prev = next((h for h in reversed(hist) if h["end"] and h["end"].year == y), None)
        r2 = random.Random(f"wr_prev:{p.seed}:{y}")
        if prev:
            name, ps, pe = prev["name"], max(prev["start"], date(y, 1, 1)), prev["end"] - timedelta(days=1)
            monthly = prev["wage"]
        else:  # 겸업(이중근로) — 단기 근로
            name = _company_name(r2)
            ps = date(y, r2.randint(1, 8), 1)
            pe = months_back(ps, -r2.randint(2, 4)) - timedelta(days=1)
            monthly = K.round_to(r2.uniform(600_000, 1_500_000), 10_000)
        months = _months_between(ps, pe + timedelta(days=1))
        p_tax = K.round_to(monthly * months, 10)
        p_meal = min(_MEAL * months, p_tax // 10) // 10 * 10 if prev else 0
        p_salary = p_tax
        pr_, hr_, lr_ = _ins_rates(y)
        p_ins = _t10(p_tax * (pr_ + hr_ * (1 + lr_) + 0.009))
        deps, n8 = _dependents(p, y)
        p_final = _income_tax_calc(p_tax, 0, p_ins, 1, 0)["final"]
        tot = _income_tax_calc(taxable + p_tax, t["pension"], t["special"] + p_ins, deps, n8, t["card"], t["special_credit"])
        final = tot["final"]
        extra["work_prev"] = {"company": name, "biz_no": _biz_no(r2), "period": f"{D(ps, 'dot')}~{D(pe, 'dot')}",
                              "salary": w(p_salary), "bonus": "0", "total": w(p_tax)}
        if p_meal:
            extra["work_prev"]["meal"] = w(p_meal)
        nontax_total += p_meal
        extra["work_sum"] = {"salary": w(t["salary"] + p_salary), "bonus": w(t["bonus"]), "total": w(taxable + p_tax),
                             "meal": w(t["nontax"] + p_meal)}
        extra["tax_prev"] = {"biz_no": extra["work_prev"]["biz_no"], "income": w(p_final), "local": w(_t10(p_final * 0.1))}
        prepaid_prev = p_final
        taxable += p_tax
    else:
        prepaid_prev = 0
    # 특수 상황: 중소기업 취업자 소득세 감면 (청년 5년간 90%, 연 200만원 한도)
    if special(rng, "sme_reduction", 0.1):
        rs = max(e.hire_date, date(y - 4, 1, 1))
        re_ = date(rs.year + 5, rs.month, rs.day) - timedelta(days=1)
        work["reduction_period"] = f"{D(rs, 'dot')}~{D(re_, 'dot')}"
        nontax["reduction"] = w(t["taxable"])
        cut = min(int(final * 0.9), 2_000_000)
        final = _t10(final - cut)
    # 특수 상황: 출산·보육수당 비과세 (6세 이하 자녀, 2024년부터 월 20만원)
    if p.children and special(rng, "childcare_nontax", 0.15):
        young = [ch for ch in p.children if y - ch.birth.year <= 6]
        if young:
            cc = (200_000 if y >= 2024 else 100_000) * t["months"]
            nontax["childcare"] = w(cc)
            nontax_total += cc
    nontax["total"] = w(nontax_total)
    final_local = _t10(final * 0.1)
    diff = _t10(final - prepaid_prev - prepaid)
    diff_local = _t10(final_local - _t10(prepaid_prev * 0.1) - t["prepaid_local"])
    eff = final / taxable * 100 if taxable else 0
    return {
        "copy_type": rng.choice(["소득자 보관용", "소득자 보관용", "발행자 보관용", "발행자 보고용"]),
        "year": f"{y}",
        "resident": "거주자1",
        "nationality": "내국인1",
        "household_head": "세대주1" if (p.spouse is None or p.person.gender == "M") else "세대원2",
        "settlement_type": "계속근로1",
        "payer": {"name": c.name, "ceo": c.ceo.name, "biz_no": c.biz_no, "address": c.address.road_short},
        "earner": {"name": p.person.name, "rrn": p.person.rrn, "address": p.person.address.road_full},
        "work": work,
        "nontax": nontax,
        "tax": {
            "final_income": w(final), "final_local": w(final_local),
            "prepaid_income": w(prepaid), "prepaid_local": w(t["prepaid_local"]),
            "diff_income": w(diff), "diff_local": w(diff_local),
            "effective_rate": f"{eff:.1f}",
        },
        **extra,
        "issue_date": D(issued, rng.choice(["kor_short", "kor"])),
        "tax_office": tax_office(c.address),
    }
