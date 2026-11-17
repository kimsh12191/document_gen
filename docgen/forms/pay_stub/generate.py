"""pay_stub: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/income.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.income import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _dependents,
    _payroll,
    _pension_base,
    _simple_monthly_tax,
    _t10,
    _year_end,
)
from docgen.registry import doc


@doc("pay_stub", "급여명세서", "income")
def pay_stub(p: Profile, rng: random.Random) -> dict:
    """임금명세서 (근로기준법 제48조제2항, 시행령 제27조의2 — 고용노동부 임금명세서 표준 예시 구조).

    지급일 / 성명·생년월일·사번·부서·직급 / 세부내역(매월 지급 · 격월 또는 부정기 지급 / 공제) /
    지급액 계·공제액 계·실수령액 / 근로일수·근로시간수·통상시급 / 계산방법(산출식 또는 산출방법).
    """
    e = p.employment
    pm = months_back(p.issue_date, 1 if p.issue_date.day < 25 else 0)
    pr = _payroll(p, pm.year, pm.month)
    pay_date = date(pm.year, pm.month, pr["pay_day"])
    df = rng.choice(["dot", "dash", "dash"])
    rate = lambda x: f"{x * 100:.3f}".rstrip("0").rstrip(".") + "%"  # noqa: E731
    p_rate, h_rate, l_rate = pr["rates"]
    w = lambda n: won(n, "")  # noqa: E731
    hourly = pr["hourly"]
    pay = list(pr["pay"])  # [(항목, 금액)]
    ded = list(pr["ded"])
    methods = {}  # 항목 -> 산출식
    if pr["hours"]:
        methods["연장근로수당"] = f"{pr['hours']}시간 × {hourly:,}원 × 1.5"
    if any(n == "명절상여금" for n, _ in pay):
        methods["명절상여금"] = "기본급 × 50%"
    night = holiday = 0
    fam = []
    if p.spouse:
        fam.append("배우자 1명")
    if p.children:
        fam.append(f"자녀 {len(p.children)}명")
    irregular_names = {"명절상여금", "정기상여금", "성과상여금", "임금인상소급분"}  # 격월 또는 부정기 지급

    def put(name, amount, method=None):
        # 식대 앞(과세 항목 끝)에 넣는다
        i = next((k for k, (n, _) in enumerate(pay) if n == "식대"), len(pay))
        pay.insert(i, (name, amount))
        if method:
            methods[name] = method

    if heavy(rng, 0.2):
        # 교대·생산직처럼 수당 항목과 공제 항목이 많은 경우 (계산방법 표가 길어져 2쪽이 되기도 한다)
        pool = [("근속수당", rng.choice([30_000, 50_000, 80_000, 100_000]), "근속연수별 정액"),
                ("자격수당", rng.choice([30_000, 50_000, 100_000]), "보유 자격증 정액"),
                ("교대근무수당", rng.choice([100_000, 150_000, 200_000]), "교대근무자 월 정액"),
                ("직무수당", rng.choice([50_000, 100_000, 150_000]), "직무등급별 정액"),
                ("통신비", rng.choice([30_000, 50_000]), "월 정액"),
                ("교통보조비", rng.choice([50_000, 100_000]), "월 정액"),
                ("위험수당", rng.choice([50_000, 80_000]), "위험작업 종사자 월 정액"),
                ("생산장려금", K.round_to(rng.uniform(50_000, 300_000), 1000), "월 생산실적 달성률에 따라 지급")]
        if p.spouse or p.children:
            fa = (40_000 if p.spouse else 0) + 20_000 * len(p.children)
            pool.append(("가족수당", fa, f"배우자 40,000원 + 자녀 {len(p.children)}명 × 20,000원" if p.spouse
                         else f"자녀 {len(p.children)}명 × 20,000원"))
        for name, amt, how in rng.sample(pool, rng.randint(4, min(8, len(pool)))):
            put(name, amt, how)
        night = rng.choice([8, 16, 24, 32])
        put("야간근로수당", _t10(hourly * 0.5 * night), f"{night}시간 × {hourly:,}원 × 0.5")
        holiday = rng.choice([0, 8, 8, 16])
        if holiday:
            put("휴일근로수당", _t10(hourly * 1.5 * holiday), f"{holiday}시간 × {hourly:,}원 × 1.5")
        for name, amt in rng.sample([("사우회비", 10_000), ("상조회비", 5_000), ("사내대출상환", rng.choice([200_000, 300_000, 500_000])),
                                     ("기숙사비", rng.choice([100_000, 150_000])), ("경조회비", 3_000), ("식권구입", rng.choice([44_000, 66_000]))],
                                    rng.randint(2, 4)):
            ded.append((name, amt))
            methods.setdefault(name, "본인 신청에 따른 공제")
    # 특수 상황: 상여 지급월 (정기상여·성과상여)
    if special(rng, "bonus", 0.15):
        if rng.random() < 0.5:
            pay.append(("정기상여금", _t10(pr["base"] * 1.0)))
            methods["정기상여금"] = "기본급 × 100% (연 4회 분할 지급)"
        else:
            amt = K.round_to(pr["base"] * rng.uniform(0.5, 2.0), 10_000)
            pay.append(("성과상여금", amt))
            methods["성과상여금"] = f"{pm.year - 1}년 성과평가 결과에 따른 지급"
    # 특수 상황: 임금인상 소급분 (인상 결정이 늦어 지난 달 차액을 이번 달에 지급)
    if special(rng, "retro_pay", 0.12):
        k = rng.randint(2, 4)
        diff = _t10(pr["base"] * rng.uniform(0.02, 0.05))
        pay.append(("임금인상소급분", diff * k))
        s_m, e_m = months_back(pm, k), months_back(pm, 1)
        methods["임금인상소급분"] = f"{s_m.year}.{s_m.month:02d}~{e_m.year}.{e_m.month:02d} 기본급 인상분 {diff:,}원 × {k}개월"
    # 특수 상황: 연말정산 환급·추징분을 급여에서 정산 (보통 2~3월)
    if special(rng, "yearend_settlement", 0.12):
        y0 = pm.year - 1
        if e.hire_date.year <= y0:
            diff = _year_end(p, y0)["diff"]
        else:
            diff = _t10(rng.uniform(-400_000, 200_000))
        ded.append(("연말정산소득세", diff))
        ded.append(("연말정산지방소득세", _t10(diff * 0.1)))
        methods["연말정산소득세"] = f"{y0}년 귀속 연말정산 {'추가징수' if diff > 0 else '환급'}분"
        methods["연말정산지방소득세"] = "연말정산소득세 × 10%"
    # 과세 급여가 바뀌었으면 소득세·고용보험을 다시 계산한다
    total = sum(v for _, v in pay)
    taxable = total - sum(v for n, v in pay if n in ("식대", "자가운전보조금"))
    deps, n8 = _dependents(p, pm.year)
    irr = sum(v for n, v in pay if n in irregular_names)
    reg = taxable - irr
    itax = _simple_monthly_tax(reg, deps, n8, pm.year)
    if irr:  # 상여·소급분은 연환산 한계세율로 따로 원천징수한 것으로 본다
        mr = next(r_ for upto, r_ in [(14_000_000, .06), (50_000_000, .15), (88_000_000, .24), (1e18, .35)]
                  if reg * 12 * 0.6 <= upto)
        itax += _t10(irr * mr)
    fixed = {"고용보험": _t10(taxable * 0.009), "소득세": itax, "지방소득세": _t10(itax * 0.1)}
    if pay != list(pr["pay"]):  # 변형이 없으면 _payroll 값 그대로 (거래내역 급여입금액과 맞춘다)
        ded = [(n, fixed.get(n, v)) for n, v in ded]
    ded_total = sum(v for _, v in ded)
    dd = dict(ded)
    pbase = _pension_base(pr["base"] + pr["pos"], date(pm.year, pm.month, 1))
    calc = [(n, methods[n], w(v)) for n, v in pay if n in methods]
    calc += [
        ("국민연금", f"기준소득월액 {pbase:,}원 × {rate(p_rate)}", w(dd["국민연금"])),
        ("건강보험", f"보수월액 × {rate(h_rate)}", w(dd["건강보험"])),
        ("장기요양보험", f"건강보험료 × {rate(l_rate)}", w(dd["장기요양보험"])),
        ("고용보험", "과세대상 임금 × 0.9%", w(dd["고용보험"])),
        ("소득세", "근로소득 간이세액표 적용", w(dd["소득세"])),
        ("지방소득세", "소득세 × 10%", w(dd["지방소득세"])),
    ]
    calc += [(n, methods[n], w(v)) for n, v in ded if n in methods]
    nxt = months_back(pm, -1)
    wd = sum(1 for i in range((nxt - pm).days) if (pm + timedelta(days=i)).weekday() < 5)
    monthly = [{"name": n, "amount": w(v)} for n, v in pay if n not in irregular_names]
    irregular = [{"name": n, "amount": w(v)} for n, v in pay if n in irregular_names]
    net = total - ded_total
    d = {
        "doc_title": rng.choice(["임금명세서", "임금명세서", "급여명세서"]),
        "title_month": f"{pm.year}년 {pm.month:02d}월분",
        "company": e.company.name,
        "pay_date": D(pay_date, df),
        "employee": {
            "name": p.person.name, "birth": D(p.person.birth, df), "employee_no": e.employee_no,
            "department": e.department, "position": e.position,
        },
        "payments": monthly,
        "deductions": [{"name": n, "amount": w(v)} for n, v in ded],
        "pay_total": w(total),
        "deduction_total": w(ded_total),
        "net_pay": w(net),
        "work": {"days": f"{wd}", "hours": f"{wd * 8 + pr['hours'] + holiday}", "overtime_hours": f"{pr['hours']}",
                 "night_hours": f"{night}", "holiday_hours": f"{holiday}", "hourly_wage": w(hourly),
                 "family": ", ".join(fam) if fam else "-"},
        "calc_methods": [{"item": a, "method": b, "amount": c} for a, b, c in calc],
    }
    if irregular:
        d["payments_irregular"] = irregular
    return d
