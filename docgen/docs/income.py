"""소득·재직 관련 서류."""
from ..registry import doc
from ._common import *  # noqa: F401,F403


@doc("employment_certificate", "재직증명서", "income")
def employment_certificate(p: Profile, rng: random.Random) -> dict:
    """회사가 발급하는 재직증명서."""
    e = p.employment
    c = e.company
    purpose = rng.choice(["금융기관 제출용", "은행 제출용", "대출 신청용", "제출처: " + p.bank])
    return {
        "doc_no": f"제 {p.issue_date.year}-{rng.randint(1, 999):03d} 호",
        "employee": {
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.6 else p.person.rrn,
            "address": p.person.address.road_full,
        },
        "employment": {
            "department": e.department,
            "position": e.position,
            "job": e.job,
            "period": f"{D(e.hire_date, 'kor')} ~ 현재",
        },
        "company": {
            "name": c.name,
            "biz_no": c.biz_no,
            "address": c.address.road_short,
            "phone": c.phone,
            "ceo": c.ceo.name,
        },
        "purpose": purpose,
        "issue_date": D(p.issue_date, rng.choice(["kor", "kor_short"])),
    }


# ---------------------------------------------------------------------------
# 급여·세금 계산 헬퍼 (income / finance 모듈 공용). 프로필 seed 로 결정되는 값은
# random.Random(f"...:{p.seed}") 를 써서 서로 다른 서류에서도 같은 값이 나오게 한다.
# ---------------------------------------------------------------------------
from ..entities import COMPANY_CORE, COMPANY_PREFIX, DEPARTMENTS, POSITIONS  # noqa: E402

_MEAL = 200_000  # 식대 비과세 한도(월)
_POS_ALLOW = {"과장": 200_000, "차장": 300_000, "부장": 400_000, "이사": 600_000}
_DUTIES = {
    "경영지원팀": "총무 및 경영지원 업무", "재무팀": "자금관리 및 결산 업무", "인사팀": "인사·노무 및 급여 관리",
    "영업1팀": "국내 영업 및 거래처 관리", "영업2팀": "B2B 영업 및 수주 관리", "마케팅팀": "마케팅 기획 및 홍보",
    "개발팀": "소프트웨어 개발 및 유지보수", "연구소": "제품 연구개발", "품질관리팀": "품질검사 및 품질보증",
    "생산관리팀": "생산계획 및 공정관리", "구매팀": "자재 구매 및 협력사 관리", "해외영업팀": "해외 영업 및 수출입 관리",
    "IT운영팀": "전산시스템 운영 및 보안", "기획팀": "사업기획 및 예산관리", "법무팀": "계약 검토 및 법무 지원",
    "고객지원팀": "고객 상담 및 CS 관리",
}


def _t10(x: float) -> int:
    """10원 미만 절사 (음수는 0 방향)."""
    x = int(x)
    return x // 10 * 10 if x >= 0 else -((-x) // 10 * 10)


def _ins_rates(year: int) -> tuple[float, float, float]:
    """근로자 부담 (국민연금, 건강보험, 장기요양보험(건강보험료 대비)) 요율."""
    if year >= 2026:
        return 0.0475, 0.03595, 0.1314
    return 0.045, 0.03545, 0.1295


def _pension_base(monthly: int, d: date) -> int:
    """국민연금 기준소득월액 (천원 미만 절사, 상·하한 적용)."""
    lo, hi = (400_000, 6_370_000) if (d.year, d.month) >= (2025, 7) else (390_000, 6_170_000)
    return min(hi, max(lo, monthly // 1000 * 1000))


def _earned_income_deduction(total: int) -> int:
    if total <= 5_000_000:
        v = total * 0.7
    elif total <= 15_000_000:
        v = 3_500_000 + (total - 5_000_000) * 0.4
    elif total <= 45_000_000:
        v = 7_500_000 + (total - 15_000_000) * 0.15
    elif total <= 100_000_000:
        v = 12_000_000 + (total - 45_000_000) * 0.05
    else:
        v = 14_750_000 + (total - 100_000_000) * 0.02
    return int(min(v, 20_000_000))


def _progressive_tax(base: int) -> int:
    for upto, rate, ded in [(14_000_000, .06, 0), (50_000_000, .15, 1_260_000), (88_000_000, .24, 5_760_000),
                            (150_000_000, .35, 15_440_000), (300_000_000, .38, 19_940_000),
                            (500_000_000, .40, 25_940_000), (1_000_000_000, .42, 35_940_000)]:
        if base <= upto:
            return int(base * rate - ded)
    return int(base * .45 - 65_940_000)


def _earned_tax_credit(calc_tax: int, total: int) -> int:
    c = calc_tax * 0.55 if calc_tax <= 1_300_000 else 715_000 + (calc_tax - 1_300_000) * 0.30
    if total <= 33_000_000:
        lim = 740_000
    elif total <= 70_000_000:
        lim = max(660_000, 740_000 - (total - 33_000_000) * 0.008)
    elif total <= 120_000_000:
        lim = max(500_000, 660_000 - (total - 70_000_000) * 0.5)
    else:
        lim = max(200_000, 500_000 - (total - 120_000_000) * 0.5)
    return int(min(c, lim))


def _child_credit(n: int) -> int:
    return 0 if n <= 0 else 150_000 if n == 1 else 350_000 + 300_000 * (n - 2)


def _dependents(p: Profile, year: int) -> tuple[int, int]:
    """(기본공제 대상 인원, 8세 이상 자녀 수)."""
    n = 1 + (1 if p.spouse else 0) + len(p.children)
    n8 = sum(1 for c in p.children if year - c.birth.year >= 8)
    return n, n8


def _income_tax_calc(total: int, pension: int, special: int, deps: int, n_child8: int,
                     card_ded: int = 0, special_credit: int = 0) -> dict:
    """연말정산 세액 계산 (단순화). 모든 값은 원 단위 정수."""
    eid = _earned_income_deduction(total)
    earned = total - eid
    personal = 1_500_000 * deps
    base = max(0, earned - personal - pension - special - card_ded)
    calc = _progressive_tax(base)
    etc = _earned_tax_credit(calc, total)
    child = min(_child_credit(n_child8), max(0, calc - etc))
    sp = min(special_credit, max(0, calc - etc - child))
    final = _t10(max(0, calc - etc - child - sp))
    return {"total": total, "eid": eid, "earned": earned, "personal": personal, "pension": pension,
            "special": special, "card": card_ded, "base": base, "calc": calc, "etc": etc,
            "child": child, "special_credit": sp, "final": final}


def _simple_monthly_tax(taxable_monthly: int, deps: int, n_child8: int, year: int) -> int:
    """근로소득 간이세액표를 흉내 낸 월 원천징수 소득세."""
    pr, hr, lr = _ins_rates(year)
    annual = taxable_monthly * 12
    pension = int(min(taxable_monthly, 6_370_000) * pr) * 12
    special = int(annual * (hr * (1 + lr) + 0.009))
    t = _income_tax_calc(annual, pension, special, deps, n_child8)
    return _t10(t["final"] / 12)


def _latest_tax_year(p: Profile) -> int:
    """지급명세서가 제출되어 조회 가능한 최근 귀속연도."""
    y = p.issue_date.year - 1 if p.issue_date.month >= 3 else p.issue_date.year - 2
    return min(p.issue_date.year - 1, max(y, p.employment.hire_date.year))


def _salary_for_year(p: Profile, year: int) -> tuple[int, int, date, date]:
    """귀속연도의 (연간 총지급액(비과세 포함), 근무월수, 근무 시작일, 종료일)."""
    e = p.employment
    k = max(0, p.issue_date.year - year)
    annual = e.annual_salary / (1.035 ** k)
    start = max(e.hire_date, date(year, 1, 1))
    end = date(year, 12, 31)
    months = 12 - start.month + (1 if start.day <= 15 else 0) if start.year == year and start > date(year, 1, 1) else 12
    months = max(1, months)
    return K.round_to(annual * months / 12, 10_000), months, start, end


def _year_end(p: Profile, year: int) -> dict:
    """귀속연도의 연말정산 결과 (원천징수영수증 / 소득금액증명원 공용, 프로필 기준 결정적)."""
    r = random.Random(f"yearend:{p.seed}:{year}")
    gross, months, start, end = _salary_for_year(p, year)
    nontax = _MEAL * months
    taxable = gross - nontax
    bonus = K.round_to(taxable * _pay_cfg(p)["bonus_ratio"], 10_000)
    salary = taxable - bonus
    pr, hr, lr = _ins_rates(year)
    m_reg = salary // months
    pension = _t10(_pension_base(m_reg, date(year, 12, 1)) * pr) * months
    health = _t10(m_reg * hr) * months
    ltc = _t10(_t10(m_reg * hr) * lr) * months
    emp = _t10(taxable * 0.009)
    deps, n8 = _dependents(p, year)
    card = K.round_to(r.uniform(0, min(3_000_000, taxable * 0.07)), 10)
    ins_c = r.choice([0, 0, 48_000, 72_000, 120_000])
    med_c = r.choice([0, 0, 0, K.round_to(r.uniform(20_000, 400_000), 10)])
    edu_c = r.choice([0, 0, K.round_to(r.uniform(30_000, 600_000), 10)]) if p.children else 0
    don_c = r.choice([0, 0, 0, K.round_to(r.uniform(15_000, 150_000), 10)])
    t = _income_tax_calc(taxable, pension, health + ltc + emp, deps, n8, card, ins_c + med_c + edu_c + don_c)
    prepaid = _simple_monthly_tax(taxable // months, deps, n8, year) * months
    final_local = _t10(t["final"] * 0.1)
    prepaid_local = _t10(prepaid * 0.1)
    return {
        **t, "year": year, "gross": gross, "months": months, "start": start, "end": end, "nontax": nontax,
        "taxable": taxable, "salary": salary, "bonus": bonus, "health": health, "ltc": ltc, "emp": emp,
        "pension_amt": pension, "deps": deps, "n8": n8, "ins_c": ins_c, "med_c": med_c, "edu_c": edu_c,
        "don_c": don_c, "prepaid": prepaid, "final_local": final_local, "prepaid_local": prepaid_local,
        "diff": _t10(t["final"] - prepaid), "diff_local": _t10(final_local - prepaid_local),
    }


def _pay_cfg(p: Profile) -> dict:
    """프로필별 급여 체계 (상여 비율, 자가운전보조금, 노조비, 급여일 등)."""
    cfg = random.Random(f"paycfg:{p.seed}")
    return {"bonus_ratio": cfg.choice([0, 0, 0.08, 0.12, 0.16]), "car": 200_000 if cfg.random() < 0.4 else 0,
            "union": cfg.choice([0, 0, 0, 10_000, 15_000, 20_000]), "pay_day": cfg.choice([10, 15, 20, 21, 25, 25, 25]),
            "holiday_bonus": cfg.random() < 0.5}


def _payroll(p: Profile, year: int, month: int) -> dict:
    """해당 월 급여 계산 (급여명세서 / 거래내역 급여입금 공용, 프로필·월 기준 결정적)."""
    e = p.employment
    cfg = _pay_cfg(p)
    r = random.Random(f"pay:{p.seed}:{year}:{month}")
    car, union, pay_day, holiday_bonus = cfg["car"], cfg["union"], cfg["pay_day"], cfg["holiday_bonus"]
    monthly = _t10(e.annual_salary / 12)
    pos = _POS_ALLOW.get(e.position, 0)
    base = monthly - _MEAL - car - pos
    hours = r.choice([0, 0, 0, 4, 6, 8, 10, 12, 16, 20])
    hourly = int((base + pos) / 209)
    ot = _t10(hourly * 1.5 * hours)
    bonus = _t10(base * 0.5) if holiday_bonus and month in (2, 9) else 0
    pay = [("기본급", base)]
    if pos:
        pay.append(("직책수당", pos))
    if ot:
        pay.append(("연장근로수당", ot))
    if bonus:
        pay.append(("명절상여금", bonus))
    pay.append(("식대", _MEAL))
    if car:
        pay.append(("자가운전보조금", car))
    total = sum(v for _, v in pay)
    taxable = total - _MEAL - car
    pr, hr, lr = _ins_rates(year)
    fixed = base + pos
    health = _t10(fixed * hr)
    deps, n8 = _dependents(p, year)
    itax = _simple_monthly_tax(taxable, deps, n8, year)
    ded = [("국민연금", _t10(_pension_base(fixed, date(year, month, 1)) * pr)), ("건강보험", health),
           ("장기요양보험", _t10(health * lr)), ("고용보험", _t10(taxable * 0.009)),
           ("소득세", itax), ("지방소득세", _t10(itax * 0.1))]
    if union:
        ded.append(("노동조합비", union))
    ded_total = sum(v for _, v in ded)
    return {"pay": pay, "ded": ded, "total": total, "ded_total": ded_total, "net": total - ded_total,
            "hours": hours, "hourly": hourly, "pay_day": pay_day, "base": base, "pos": pos,
            "rates": (pr, hr, lr)}


def _company_name(r: random.Random) -> str:
    _, _, _, suffix = r.choice(COMPANY_CORE)
    name = r.choice(COMPANY_PREFIX) + suffix
    return r.choice([f"(주){name}", f"주식회사 {name}", f"{name}(주)"])


def _work_history(p: Profile) -> list[dict]:
    """이전 직장/공백 이력 (국민연금·건강보험 서류 공용). 마지막 항목이 현재 직장."""
    r = random.Random(f"hist:{p.seed}")
    e = p.employment
    first = date(p.person.birth.year + r.randint(24, 28), r.randint(1, 12), r.choice([1, 2, 3, 10, 15]))
    rows = []
    cur = first
    if (e.hire_date - first).days > 400:
        n_prev = 1 if (e.hire_date - first).days < 1500 else r.randint(1, 2)
        span = (e.hire_date - first).days
        bounds = sorted(r.sample(range(200, span - 30), n_prev - 1)) if n_prev > 1 else []
        ends = [first + timedelta(days=b) for b in bounds] + [e.hire_date - timedelta(days=1)]
        for end in ends:
            gap = r.choice([0, 0, 0, 30, 60, 120, 200])
            job_end = end - timedelta(days=gap)
            if job_end <= cur + timedelta(days=90):
                job_end, gap = end, 0
            rows.append({"kind": "work", "name": _company_name(r), "start": cur, "end": job_end + timedelta(days=1),
                         "wage": K.round_to(r.uniform(2_200_000, 3_600_000), 1000)})
            if gap >= 60:
                rows.append({"kind": "local", "start": job_end + timedelta(days=1), "end": end + timedelta(days=1)})
            cur = end + timedelta(days=1)
    else:
        first = e.hire_date
    rows.append({"kind": "work", "name": e.company.name, "start": e.hire_date, "end": None,
                 "wage": None, "current": True})
    return [{"first": first, **x} for x in rows]


def _months_between(a: date, b: date) -> int:
    return max(1, (b.year * 12 + b.month) - (a.year * 12 + a.month) + (1 if a.day == 1 else 0))


def _nps_branch(addr: Address) -> str:
    last = addr.sigungu.split()[0] if addr.sigungu else K.sido_short(addr.sido)
    if len(last) == 2 and last[-1] in "구시군":
        return f"{K.sido_short(addr.sido)}{last[0]}부지사"
    return f"{last[:-1] if last[-1] in '구시군' else last}지사"


# ---------------------------------------------------------------------------
# 서류
# ---------------------------------------------------------------------------

@doc("career_certificate", "경력증명서", "income")
def career_certificate(p: Profile, rng: random.Random) -> dict:
    """현 직장이 발급하는 경력증명서 (재직 중 부서·직위 이력)."""
    e = p.employment
    c = e.company
    names = [x[0] for x in POSITIONS]
    idx = names.index(e.position)
    stints = [(e.hire_date if i == 0 else date(e.hire_date.year + th, 1, 1), nm)
              for i, (nm, th) in enumerate(POSITIONS[:idx + 1])]
    stints = [s for s in stints if s[0] < p.issue_date]
    if len(stints) > 6:
        stints = [(e.hire_date, stints[-6][1])] + stints[-5:]
    df = rng.choice(["dot", "dot", "dash", "kor"])
    rows = []
    for i, (start, pos) in enumerate(stints):
        last = i == len(stints) - 1
        dept = e.department if last or rng.random() < 0.6 else rng.choice(DEPARTMENTS)
        end = "현재" if last else D(stints[i + 1][0] - timedelta(days=1), df)
        rows.append({"period": f"{D(start, df)} ~ {end}", "department": dept, "position": pos,
                     "duty": _DUTIES.get(dept, "일반 사무")})
    # 같은 부서·직위 연속 구간은 실제로 하나로 쓰지만, 직위가 매번 달라 그대로 둔다.
    m = (p.issue_date.year - e.hire_date.year) * 12 + p.issue_date.month - e.hire_date.month
    if p.issue_date.day < e.hire_date.day:
        m -= 1
    return {
        "doc_no": rng.choice([f"제 {p.issue_date.year}-{rng.randint(1, 999):03d} 호",
                              f"{c.name.replace('(주)', '').replace('주식회사 ', '')[:2]}인사-{p.issue_date.year}-{rng.randint(10, 999)}"]),
        "person": {
            "name": p.person.name,
            "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.6 else p.person.rrn,
            "address": p.person.address.road_full,
            "phone": p.person.mobile,
        },
        "hire_date": D(e.hire_date, df),
        "total_period": f"{m // 12}년 {m % 12}개월",
        "careers": rows,
        "purpose": rng.choice(["금융기관 제출용", "은행 제출용", "대출 신청용", "경력 확인용"]),
        "company": {
            "name": c.name,
            "biz_no": c.biz_no,
            "address": c.address.road_short,
            "phone": c.phone,
            "ceo": c.ceo.name,
        },
        "issue_date": D(p.issue_date, rng.choice(["kor", "kor_short"])),
    }


@doc("pay_stub", "급여명세서", "income")
def pay_stub(p: Profile, rng: random.Random) -> dict:
    """회사 급여명세서 (월 급여, 4대보험·소득세 공제)."""
    e = p.employment
    pm = months_back(p.issue_date, 1 if p.issue_date.day < 25 else 0)
    pr = _payroll(p, pm.year, pm.month)
    pay_date = date(pm.year, pm.month, pr["pay_day"])
    df = rng.choice(["dot", "dash", "kor_short"])
    rate = lambda x: f"{x * 100:.3f}".rstrip("0").rstrip(".") + "%"  # noqa: E731
    p_rate, h_rate, l_rate = pr["rates"]
    calc = [
        ("연장근로수당", f"통상시급 {pr['hourly']:,}원 × {pr['hours']}시간 × 1.5"),
        ("국민연금", f"기준소득월액 × {rate(p_rate)}"),
        ("건강보험", f"보수월액 × {rate(h_rate)}"),
        ("장기요양보험", f"건강보험료 × {rate(l_rate)}"),
        ("고용보험", "과세급여 × 0.9%"),
        ("지방소득세", "소득세 × 10%"),
    ]
    if not pr["hours"]:
        calc = calc[1:]
    nxt = months_back(pm, -1)
    wd = sum(1 for i in range((nxt - pm).days) if (pm + timedelta(days=i)).weekday() < 5)
    return {
        "title_month": f"{pm.year}년 {pm.month:02d}월",
        "company": e.company.name,
        "pay_date": D(pay_date, df),
        "employee": {
            "name": p.person.name, "employee_no": e.employee_no, "department": e.department,
            "position": e.position, "hire_date": D(e.hire_date, df),
        },
        "payments": [{"name": n, "amount": won(v, "")} for n, v in pr["pay"]],
        "deductions": [{"name": n, "amount": won(v, "")} for n, v in pr["ded"]],
        "pay_total": won(pr["total"], ""),
        "deduction_total": won(pr["ded_total"], ""),
        "net_pay": won(pr["net"], ""),
        "calc_methods": [{"item": a, "method": b} for a, b in calc],
        "account": f"{p.accounts[0].bank} {p.accounts[0].number}",
        "work": {"days": f"{wd}일", "hours": f"{wd * 8 + pr['hours']}시간", "overtime_hours": f"{pr['hours']}시간"},
    }


@doc("employment_contract", "근로계약서", "income")
def employment_contract(p: Profile, rng: random.Random) -> dict:
    """표준근로계약서 (기간의 정함이 없는 경우)."""
    e = p.employment
    c = e.company
    years = max(0, p.issue_date.year - e.hire_date.year)
    annual = K.round_to(e.annual_salary / (1.035 ** years), 100_000)
    monthly = _t10(annual / 12)
    s_h = rng.choice([8, 9, 9, 9, 10])
    pay_day = _pay_cfg(p)["pay_day"]
    df = rng.choice(["kor", "kor_short"])
    return {
        "employer": {"name": c.name, "ceo": c.ceo.name, "address": c.address.road_short, "phone": c.phone},
        "employee": {"name": p.person.name, "address": p.person.address.road_short, "phone": p.person.mobile,
                     "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.5 else p.person.rrn},
        "start_date": D(e.hire_date, df),
        "workplace": rng.choice([c.address.road_short, f"{c.name} 본사"]),
        "job": f"{e.department} {_DUTIES.get(e.department, '일반 사무')}",
        "work_hours": f"{s_h:02d}시 00분부터 {s_h + 9:02d}시 00분까지",
        "break_time": "12시 00분 ~ 13시 00분",
        "work_days": "매주 5일(월~금) 근무",
        "holiday": rng.choice(["매주 일요일", "매주 토요일, 일요일"]),
        "annual_salary": won(annual),
        "monthly_salary": won(monthly),
        "bonus": rng.choice(["있음", "없음"]),
        "allowances": "식대 월 200,000원" + (", 직책수당" if e.position in _POS_ALLOW else ""),
        "pay_day": f"매월 {pay_day}일",
        "pay_method": "근로자 명의 예금통장에 입금",
        "contract_date": D(e.hire_date - timedelta(days=rng.randint(0, 7)), df),
    }


@doc("withholding_receipt", "근로소득 원천징수영수증", "income")
def withholding_receipt(p: Profile, rng: random.Random) -> dict:
    """근로소득 원천징수영수증(근로소득 지급명세서) — 연말정산 결과."""
    e = p.employment
    c = e.company
    y = _latest_tax_year(p)
    t = _year_end(p, y)
    w = lambda n: won(n, "")  # noqa: E731
    issued = date(y + 1, 2, 28) + timedelta(days=rng.randint(0, 20))
    if issued > p.issue_date:
        issued = p.issue_date
    return {
        "copy_type": rng.choice(["소득자 보관용", "발행자 보관용", "발행자 보고용"]),
        "year": f"{y}",
        "resident": "거주자1",
        "household_head": "세대주" if (p.spouse is None or p.person.gender == "M") else "세대원",
        "settlement_type": "계속근로",
        "payer": {"name": c.name, "ceo": c.ceo.name, "biz_no": c.biz_no, "corp_no": c.corp_no,
                  "address": c.address.road_short},
        "earner": {"name": p.person.name, "rrn": p.person.rrn, "address": p.person.address.road_full},
        "work": {
            "company": c.name, "biz_no": c.biz_no,
            "period": f"{D(t['start'], 'dot')} ~ {D(t['end'], 'dot')}",
            "salary": w(t["salary"]), "bonus": w(t["bonus"]), "total": w(t["taxable"]),
        },
        "nontax": {"meal": w(t["nontax"]), "total": w(t["nontax"])},
        "calc": {
            "total_pay": w(t["total"]), "earned_deduction": w(t["eid"]), "earned_income": w(t["earned"]),
            "personal": w(t["personal"]), "pension": w(t["pension"]), "special": w(t["special"]),
            "card": w(t["card"]), "tax_base": w(t["base"]), "calc_tax": w(t["calc"]),
            "earned_credit": w(t["etc"]), "child_credit": w(t["child"]), "special_credit": w(t["special_credit"]),
        },
        "tax": {
            "final_income": w(t["final"]), "final_local": w(t["final_local"]),
            "prepaid_income": w(t["prepaid"]), "prepaid_local": w(t["prepaid_local"]),
            "diff_income": w(t["diff"]), "diff_local": w(t["diff_local"]),
        },
        "issue_date": D(issued, "kor_short"),
        "tax_office": tax_office(c.address),
    }


@doc("income_certificate", "소득금액증명원", "income")
def income_certificate(p: Profile, rng: random.Random) -> dict:
    """국세청(홈택스) 발급 소득금액증명 — 근로소득자용 / 종합소득세 신고자용."""
    e = p.employment
    latest = _latest_tax_year(p)
    n = min(rng.choice([2, 3, 3]), latest - e.hire_date.year + 1)
    kind = rng.choice(["근로소득자용", "근로소득자용", "종합소득세 신고자용"])
    rows = []
    for y in range(latest, latest - n, -1):
        t = _year_end(p, y)
        amount = t["taxable"] if kind == "근로소득자용" else t["earned"]
        rows.append({"year": f"{y}", "income_type": "근로소득", "payer": e.company.name, "payer_biz_no": e.company.biz_no,
                     "amount": won(amount, ""), "tax": won(t["final"], "")})
    d = {
        "issue_no": f"{rng.randint(1000, 9999)}-{rng.randint(100, 999)}-{rng.randint(1000, 9999)}-{rng.randint(100, 999)}",
        "kind": kind,
        "taxpayer": {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn, rng.choice([1, 7])),
                     "address": p.person.address.road_full},
        "period": f"{rows[-1]['year']}년 ~ {rows[0]['year']}년",
        "rows": rows,
        "purpose": rng.choice(["금융기관 제출용", "대출용", "은행 제출용"]),
        "submit_to": p.bank,
        "issue_date": D(p.issue_date, "kor_short"),
        "issuer": tax_office(p.person.address),
    }
    if kind == "종합소득세 신고자용":
        d["taxpayer"]["biz_name"] = e.company.name
        d["taxpayer"]["biz_no"] = e.company.biz_no
    return d


@doc("pension_enrollment_certificate", "국민연금 가입자 가입증명", "income")
def pension_enrollment_certificate(p: Profile, rng: random.Random) -> dict:
    """국민연금공단 발급 가입자 가입증명(가입내역확인서)."""
    hist = _work_history(p)
    df = rng.choice(["dot", "dash"])
    cur_wage = _pension_base(_t10(p.employment.annual_salary / 12) - _MEAL, p.issue_date)
    rows, months = [], 0
    for h in hist:
        end = h["end"] or p.issue_date
        months += _months_between(h["start"], end)
        row = {"start": D(h["start"], df), "kind": "사업장가입자" if h["kind"] == "work" else "지역가입자"}
        if h["kind"] == "work":
            row["workplace"] = h["name"]
            row["wage"] = won(h["wage"] if h["wage"] else cur_wage, "")
        else:
            row["wage"] = won(K.round_to(rng.uniform(900_000, 1_500_000), 1000), "")
        if h["end"]:
            row["end"] = D(h["end"], df)
        rows.append(row)
    return {
        "issue_no": f"{p.issue_date:%Y%m%d}-{rng.randint(10000000, 99999999)}",
        "person": {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.5 else p.person.rrn,
                   "address": p.person.address.road_short},
        "current_kind": "사업장가입자",
        "current_workplace": p.employment.company.name,
        "total_months": f"{months}개월",
        "rows": rows,
        "purpose": rng.choice(["금융기관 제출용", "은행 제출용", "기타"]),
        "issue_date": D(p.issue_date, "kor_short"),
        "issuer": f"국민연금공단 {_nps_branch(p.person.address)}장",
    }


@doc("health_insurance_qualification", "건강보험 자격득실확인서", "income")
def health_insurance_qualification(p: Profile, rng: random.Random) -> dict:
    """국민건강보험공단 발급 건강보험 자격득실 확인서."""
    hist = _work_history(p)
    df = rng.choice(["dot", "dash"])
    rows = [{"kind": "피부양자", "start": D(p.person.birth, df), "end": D(hist[0]["start"], df)}]
    for h in hist:
        row = {"kind": "직장가입자" if h["kind"] == "work" else "지역가입자", "start": D(h["start"], df)}
        if h["kind"] == "work":
            row["workplace"] = h["name"]
        if h["end"]:
            row["end"] = D(h["end"], df)
        rows.append(row)
    if p.person.birth.year < 1977:  # 전산 기록 이전 이력은 생략
        rows = rows[1:]
    return {
        "issue_no": f"{rng.randint(1000, 9999)}-{rng.randint(1000, 9999)}-{rng.randint(1000, 9999)}-{rng.randint(1000, 9999)}",
        "person": {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.6 else p.person.rrn},
        "rows": rows,
        "purpose": rng.choice(["금융기관 제출용", "은행 제출용", "기타 제출용"]),
        "issue_date": D(p.issue_date, "kor_short"),
    }


@doc("health_insurance_payment", "건강보험료 납부확인서", "income")
def health_insurance_payment(p: Profile, rng: random.Random) -> dict:
    """국민건강보험공단 발급 건강보험료 납부확인서 (직장가입자 본인부담분)."""
    e = p.employment
    n = rng.choice([6, 12, 12])
    last = months_back(p.issue_date, 1 if p.issue_date.day > 10 else 2)
    last = max(last, date(e.hire_date.year, e.hire_date.month, 1))
    rows, tot_h, tot_l = [], 0, 0
    for i in range(n - 1, -1, -1):
        m = months_back(last, i)
        if m < date(e.hire_date.year, e.hire_date.month, 1):
            continue
        _, hr, lr = _ins_rates(m.year)
        gross, months, _, _ = _salary_for_year(p, m.year)
        sal = gross / months
        h = _t10((sal - _MEAL) * hr)
        l = _t10(h * lr)
        paid = months_back(m, -1) + timedelta(days=9)
        while paid.weekday() >= 5:
            paid += timedelta(days=1)
        tot_h += h
        tot_l += l
        rows.append({"month": f"{m.year}.{m.month:02d}", "health": won(h, ""), "ltc": won(l, ""),
                     "total": won(h + l, ""), "paid_date": D(paid, "dot")})
    biz = e.company.biz_no.replace("-", "")
    return {
        "issue_no": f"{rng.randint(10, 99)}-{rng.randint(100000, 999999)}-{rng.randint(1000, 9999)}",
        "person": {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn), "address": p.person.address.road_short},
        "member_kind": "직장가입자",
        "workplace": {"name": e.company.name, "mgmt_no": f"{biz}0", "address": e.company.address.road_short},
        "period": f"{rows[0]['month']} ~ {rows[-1]['month']}",
        "rows": rows,
        "sum": {"health": won(tot_h, ""), "ltc": won(tot_l, ""), "total": won(tot_h + tot_l, "")},
        "purpose": rng.choice(["금융기관 제출용", "은행 제출용", "기타"]),
        "issue_date": D(p.issue_date, "kor_short"),
    }
