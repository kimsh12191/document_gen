"""소득·재직 관련 서류."""
from ..registry import doc
from ._common import *  # noqa: F401,F403


@doc("employment_certificate", "재직증명서", "income")
def employment_certificate(p: Profile, rng: random.Random) -> dict:
    """회사가 발급하는 재직증명서 (근로기준법 제39조 사용증명서, 법정서식 없음 — 통용 양식).

    통용 양식: 문서번호 / 인적사항(성명·주민등록번호(또는 생년월일)·주소) / 재직사항(회사명·사업자등록번호·
    소재지·소속·직위·재직기간·담당업무) / 용도·제출처 / 증명 문구 / 발급일 / 회사명·대표이사 (직인).
    """
    e = p.employment
    c = e.company
    df = rng.choice(["kor", "dot", "dot"])
    idv = rng.random()
    employee = {"name": p.person.name, "address": p.person.address.road_full}
    if idv < 0.55:
        employee["rrn"] = K.mask_rrn(p.person.rrn)
    elif idv < 0.75:
        employee["rrn"] = p.person.rrn
    else:
        employee["birth"] = D(p.person.birth, rng.choice(["kor", "dot"]))
    employment = {
        "department": e.department,
        "position": e.position,
        "period": f"{D(e.hire_date, df)} ~ 현재",
        "duty": _DUTIES.get(e.department, "일반 사무"),
    }
    # 특수 상황: 기간제(계약직) 근로자 — 고용형태와 현재 계약기간을 함께 적는다
    if special(rng, "contract_worker", 0.08):
        employment["employment_type"] = rng.choice(["계약직", "계약직(기간제)", "촉탁직"])
        cs = e.hire_date
        while date(cs.year + 1, cs.month, min(cs.day, 28)) <= p.issue_date:
            cs = date(cs.year + 1, cs.month, min(cs.day, 28))
        ce = date(cs.year + 1, cs.month, min(cs.day, 28)) - timedelta(days=1)
        employment["contract_period"] = f"{D(cs, df)} ~ {D(ce, df)}"
    # 특수 상황: 육아휴직 (현재 휴직 중이거나 지난 휴직 이력)
    if special(rng, "parental_leave", 0.1):
        lv = _leave_period(p)
        if lv:
            employment["leave"] = f"{D(lv[0], df)} ~ {D(lv[1], df)} ({rng.choice(['육아휴직', '육아휴직', '출산전후휴가 및 육아휴직'])})"
    # 특수 상황: 급여(연봉)를 함께 적어 달라고 한 경우 (재직 및 급여 증명)
    if special(rng, "salary_shown", 0.12):
        employment["annual_salary"] = f"연 {won(e.annual_salary)}" if rng.random() < 0.5 else won(e.annual_salary)
    return {
        "doc_no": rng.choice([f"제 {p.issue_date.year}-{rng.randint(1, 999):03d} 호",
                              f"제{p.issue_date:%y}{rng.randint(1, 999):04d}호"]),
        "employee": employee,
        "company": {
            "name": c.name,
            "biz_no": c.biz_no,
            "address": c.address.road_short,
            "phone": c.phone,
            "ceo": c.ceo.name,
        },
        "employment": employment,
        "purpose": rng.choice(["금융기관 제출용", "대출 신청용", "은행 제출용"]),
        "submit_to": p.bank,
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
    """근로자 부담 (국민연금, 건강보험, 장기요양보험(건강보험료 대비)) 요율.

    2026: 국민연금 9.5%(연금개혁, 근로자 4.75%), 건강보험 7.19%(3.595%), 장기요양 건보료의 13.14%.
    2024~2025: 9%, 7.09%, 12.95% / 2023: 9%, 7.09%, 12.81% / 2022: 9%, 6.99%, 12.27% / 2021: 9%, 6.86%, 11.52%.
    """
    if year >= 2026:
        return 0.0475, 0.03595, 0.1314
    if year >= 2024:
        return 0.045, 0.03545, 0.1295
    if year == 2023:
        return 0.045, 0.03545, 0.1281
    if year == 2022:
        return 0.045, 0.03495, 0.1227
    return 0.045, 0.0343, 0.1152


def _pension_base(monthly: int, d: date) -> int:
    """국민연금 기준소득월액 (천원 미만 절사, 상·하한 적용). 상·하한은 매년 7월 조정."""
    ym = (d.year, d.month)
    if ym >= (2026, 7):
        lo, hi = 410_000, 6_590_000
    elif ym >= (2025, 7):
        lo, hi = 400_000, 6_370_000
    elif ym >= (2024, 7):
        lo, hi = 390_000, 6_170_000
    else:
        lo, hi = 370_000, 5_900_000
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
    pension = int(_pension_base(taxable_monthly, date(year, 6, 1)) * pr) * 12
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


def _work_history(p: Profile, many: bool = False) -> list[dict]:
    """이전 직장/공백 이력 (국민연금·건강보험·소득금액증명 공용). 마지막 항목이 현재 직장.

    kind: work(사업장) / local(지역가입자 공백) / dep(배우자 등의 피부양자로 등재된 공백).
    many=True 면 이직이 잦은 사람 (사업장 6~16곳, 자격 취득·상실 반복). 같은 프로필이면 서류가 달라도 같은 이력.
    """
    r = random.Random(f"hist{'_many' if many else ''}:{p.seed}")
    e = p.employment
    first = date(p.person.birth.year + r.randint(24, 28), r.randint(1, 12), r.choice([1, 2, 3, 10, 15]))
    if many:  # 이직이 잦은 사람은 사회생활을 일찍 시작한 경우가 많다
        first = date(p.person.birth.year + r.randint(20, 24), r.randint(1, 12), r.choice([1, 2, 3, 10, 15]))
    rows = []
    cur = first
    if (e.hire_date - first).days > 400:
        span = (e.hire_date - first).days
        if many:
            n_prev = max(2, min(16, span // r.randint(220, 480)))
            w = [r.uniform(0.5, 1.6) for _ in range(n_prev)]
            acc, ends = 0.0, []
            for x in w[:-1]:
                acc += x
                ends.append(first + timedelta(days=int(span * acc / sum(w))))
            ends.append(e.hire_date - timedelta(days=1))
        else:
            n_prev = 1 if span < 1500 else r.randint(1, 2)
            bounds = sorted(r.sample(range(200, span - 30), n_prev - 1)) if n_prev > 1 else []
            ends = [first + timedelta(days=b) for b in bounds] + [e.hire_date - timedelta(days=1)]
        for end in ends:
            gap = r.choice([0, 0, 30, 45, 60, 90, 120, 200]) if many else r.choice([0, 0, 0, 30, 60, 120, 200])
            job_end = end - timedelta(days=gap)
            if job_end <= cur + timedelta(days=60 if many else 90):
                job_end, gap = end, 0
            wage = r.uniform(2_000_000, 3_600_000) / 1.045 ** max(0, p.issue_date.year - cur.year)  # 예전 직장일수록 낮은 임금
            rows.append({"kind": "work", "name": _company_name(r), "start": cur, "end": job_end + timedelta(days=1),
                         "wage": max(220_000, K.round_to(wage, 1000))})
            if gap >= 60:
                rows.append({"kind": r.choice(["local", "local", "dep"]) if many else "local",
                             "start": job_end + timedelta(days=1), "end": end + timedelta(days=1)})
            cur = end + timedelta(days=1)
    else:
        first = e.hire_date
    rows.append({"kind": "work", "name": e.company.name, "start": e.hire_date, "end": None,
                 "wage": None, "current": True})
    return [{"first": first, **x} for x in rows]


def _ensure_gap(hist: list[dict], kind: str, rng: random.Random) -> list[dict]:
    """이력에 kind(local/dep) 공백 구간이 없으면 이전 직장 하나의 끝을 당겨 공백을 만든다 (특수 상황용)."""
    if any(h["kind"] == kind for h in hist):
        return hist
    hist = [dict(h) for h in hist]
    for i in range(len(hist) - 2, -1, -1):
        h = hist[i]
        if h["kind"] != "work" or h.get("current"):
            continue
        g = rng.randint(70, 240)
        if (h["end"] - h["start"]).days < g + 90:
            continue
        old_end = h["end"]
        if i + 1 < len(hist) and hist[i + 1]["kind"] != "work":  # 이미 다른 공백이 붙어 있으면 그 종류만 바꾼다
            hist[i + 1]["kind"] = kind
            return hist
        h["end"] = old_end - timedelta(days=g)
        hist.insert(i + 1, {"first": h["first"], "kind": kind, "start": h["end"], "end": old_end})
        return hist
    return hist


def _leave_period(p: Profile) -> tuple[date, date] | None:
    """프로필별 육아휴직 기간 (입사 1년 이후, 발급일 기준 진행 중일 수도 있다). 재직 기간이 짧으면 None."""
    e = p.employment
    r = random.Random(f"leave:{p.seed}")
    lo = e.hire_date + timedelta(days=400)
    hi = p.issue_date - timedelta(days=45)
    if hi <= lo:
        return None
    s = rand_date(r, lo, hi)
    s = date(s.year, s.month, 1)
    if s <= e.hire_date:
        s = months_back(s, -1)
    end = months_back(s, -r.choice([3, 6, 6, 10, 12, 12, 12])) - timedelta(days=1)
    return s, end


def _months_between(a: date, b: date) -> int:
    return max(1, (b.year * 12 + b.month) - (a.year * 12 + a.month) + (1 if a.day == 1 else 0))


# ---------------------------------------------------------------------------
# 서류
# ---------------------------------------------------------------------------

@doc("career_certificate", "경력증명서", "income")
def career_certificate(p: Profile, rng: random.Random) -> dict:
    """현 직장이 발급하는 경력증명서 (근로기준법 제39조 사용증명서, 통용 양식: 인적사항 / 경력사항
    (근무기간·근무부서·직위·담당업무) / 총 근무기간 / 용도·제출처 / 증명 문구 / 회사 정보·대표이사 직인)."""
    e = p.employment
    c = e.company
    names = [x[0] for x in POSITIONS]
    idx = names.index(e.position)
    promos = [(e.hire_date if i == 0 else date(e.hire_date.year + th, 1, 1), nm)
              for i, (nm, th) in enumerate(POSITIONS[:idx + 1])]
    promos = [s for s in promos if s[0] < p.issue_date]
    df = rng.choice(["dot", "dot", "dash", "kor"])
    # 구간: (시작일, 부서, 직위, 담당업무)
    if heavy(rng, 0.25):
        # 인사발령(부서 이동·승진·겸무)이 많은 장기 근속자: 발령마다 한 줄
        segs, cur, dept = [], e.hire_date, rng.choice(DEPARTMENTS)
        pi = 0
        while cur < p.issue_date:
            while pi + 1 < len(promos) and promos[pi + 1][0] <= cur:
                pi += 1
            segs.append([cur, dept, promos[pi][1], _DUTIES.get(dept, "일반 사무")])
            nxt = months_back(cur, -rng.choice([3, 6, 6, 8, 12, 12, 18]))
            nxt = date(nxt.year, nxt.month, 1)
            if pi + 1 < len(promos) and promos[pi + 1][0] < nxt:
                nxt = promos[pi + 1][0]  # 승진 발령
            elif rng.random() < 0.65:
                dept = rng.choice([x for x in DEPARTMENTS if x != dept])  # 전보 발령
            cur = nxt
        # 마지막 구간은 현재 부서·직위
        segs[-1][1], segs[-1][2], segs[-1][3] = e.department, e.position, _DUTIES.get(e.department, "일반 사무")
        for s in segs:
            if rng.random() < 0.12 and s[2] in ("과장", "차장", "부장"):
                s[3] = f"{s[3]} (팀장 직무대행)" if rng.random() < 0.5 else f"{s[3]} / {rng.choice(DEPARTMENTS)} 겸무"
    else:
        stints = promos
        if len(stints) > 6:
            stints = [(e.hire_date, stints[-6][1])] + stints[-5:]
        segs = []
        for i, (start, pos) in enumerate(stints):
            last = i == len(stints) - 1
            dept = e.department if last or rng.random() < 0.6 else rng.choice(DEPARTMENTS)
            segs.append([start, dept, pos, _DUTIES.get(dept, "일반 사무")])
    ends = [segs[i + 1][0] - timedelta(days=1) for i in range(len(segs) - 1)] + [None]
    segs = [s + [en] for s, en in zip(segs, ends)]  # [시작, 부서, 직위, 업무, 끝(None=현재)]
    # 특수 상황: 계열사 파견 근무 구간
    if special(rng, "dispatch", 0.08):
        cand = [i for i, s in enumerate(segs) if s[4] and (s[4] - s[0]).days > 200]
        if cand:
            i = rng.choice(cand)
            s = segs[i]
            ds = date(s[0].year, s[0].month, 1) if s[0].day == 1 else s[0]
            de = months_back(ds, -rng.choice([3, 6, 6, 12]))
            if de < s[4]:
                aff = _company_name(random.Random(f"aff:{p.seed}"))
                segs[i:i + 1] = [[ds, f"{aff} 파견", s[2], "계열사 파견 근무", de - timedelta(days=1)],
                                 [de, s[1], s[2], s[3], s[4]]]
    # 특수 상황: 육아휴직 기간 (해당 구간을 휴직 전/휴직/복직으로 나눈다)
    leave_m = 0
    if special(rng, "parental_leave", 0.12):
        lv = _leave_period(p)
        if lv:
            for i, s in enumerate(segs):
                end = s[4] or p.issue_date
                if s[0] < lv[0] <= end:
                    ongoing = lv[1] >= p.issue_date
                    new = [[s[0], s[1], s[2], s[3], lv[0] - timedelta(days=1)]]
                    if ongoing:  # 현재 휴직 중: 이후 발령 없음
                        new.append([lv[0], e.department, e.position, "육아휴직", None])
                    else:
                        new.append([lv[0], s[1], s[2], "육아휴직", lv[1]])
                        for sg in [[lv[1] + timedelta(days=1), s[1], s[2], s[3], s[4]]] + segs[i + 1:]:
                            if sg[4] is not None and sg[4] <= lv[1]:
                                continue  # 휴직 중에 끝난 구간은 없앤다
                            sg[0] = max(sg[0], lv[1] + timedelta(days=1))
                            new.append(sg)
                    segs = segs[:i] + new
                    leave_m = _months_between(lv[0], min(lv[1], p.issue_date))
                    break
    rows = []
    for s in segs:
        rows.append({"period": f"{D(s[0], df)} ~ {D(s[4], df) if s[4] else '현재'}", "department": s[1],
                     "position": s[2], "duty": s[3]})
    m = (p.issue_date.year - e.hire_date.year) * 12 + p.issue_date.month - e.hire_date.month
    if p.issue_date.day < e.hire_date.day:
        m -= 1
    total = f"{m // 12}년 {m % 12}개월"
    if leave_m:
        total += f" (휴직기간 {leave_m}개월 포함)"
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
        "total_period": total,
        "careers": rows,
        "purpose": rng.choice(["금융기관 제출용", "은행 제출용", "대출 신청용", "경력 확인용"]),
        "submit_to": p.bank,
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


@doc("employment_contract", "근로계약서", "income")
def employment_contract(p: Profile, rng: random.Random) -> dict:
    """고용노동부 표준근로계약서 (기간의 정함이 없는 경우) — 1.근로개시일 ~ 11.기타, 사업주·근로자 서명."""
    e = p.employment
    c = e.company
    cfg = _pay_cfg(p)
    years = max(0, p.issue_date.year - e.hire_date.year)
    annual = K.round_to(e.annual_salary / (1.035 ** years), 100_000)
    monthly = _t10(annual / 12)
    s_h = rng.choice([8, 9, 9, 9, 10])
    df = rng.choice(["kor", "kor_short"])
    allow = [{"name": "식대", "amount": won(_MEAL)}]
    if cfg["car"]:
        allow.append({"name": "자가운전보조금", "amount": won(cfg["car"])})
    d = {
        "employer": {"name": c.name, "ceo": c.ceo.name, "address": c.address.road_short, "phone": c.phone},
        "employee": {"name": p.person.name, "address": p.person.address.road_short, "phone": p.person.mobile},
        "start_date": D(e.hire_date, df),
        "workplace": rng.choice([c.address.road_short, f"{c.name} 본사"]),
        "job": f"{e.department} {_DUTIES.get(e.department, '일반 사무')}",
        "work_start": f"{s_h:02d}시 00분",
        "work_end": f"{s_h + 9:02d}시 00분",
        "break_time": rng.choice(["12시 00분 ~ 13시 00분", "12시 00분 ~ 13시 00분", "11시 30분 ~ 12시 30분"]),
        "work_days": "5",
        "weekly_holiday": "일",
        "monthly_salary": won(monthly, ""),
        "bonus": "있음" if cfg["holiday_bonus"] else "없음",
        "other_pay": "있음",
        "allowances": allow,
        "pay_day": f"{cfg['pay_day']}",
        "pay_method": "근로자 명의 예금통장에 입금",
        "contract_date": D(e.hire_date - timedelta(days=rng.randint(0, 7)), df),
    }
    if cfg["holiday_bonus"]:
        d["bonus_amount"] = won(_t10((monthly - _MEAL - cfg["car"]) * 0.5) * 2, "")
    # 특수 상황: 기간의 정함이 있는 근로계약 (계약직) — 서식 제목과 1번 항목이 바뀐다
    if special(rng, "fixed_term", 0.15):
        end = date(e.hire_date.year + rng.choice([1, 1, 2]), e.hire_date.month, min(e.hire_date.day, 28)) - timedelta(days=1)
        d["end_date"] = D(end, df)
    # 특수 상황: 수습기간
    if special(rng, "probation", 0.2):
        n = rng.choice([3, 3, 3, 6])
        pe = months_back(date(e.hire_date.year, e.hire_date.month, 1), -n)
        pe = date(pe.year, pe.month, min(e.hire_date.day, 28)) - timedelta(days=1)
        d["probation"] = {"period": f"{D(e.hire_date, df)} ~ {D(pe, df)} ({n}개월)",
                          "wage_rate": rng.choice(["90%", "90%", "100%"])}
    # 특수 상황: 특약사항 (손으로 추가 기재). 내용이 많으면 2쪽으로 넘어간다.
    n_terms = rng.randint(6, 11) if heavy(rng, 0.15) else (rng.randint(1, 4) if special(rng, "special_terms", 0.2) else 0)
    if n_terms:
        pool = [
            "월 급여에는 월 20시간분의 고정연장근로수당이 포함되어 있으며, 이를 초과하는 연장근로는 별도 지급한다.",
            "근로자는 재직 중 및 퇴직 후 2년간 업무상 알게 된 회사의 영업비밀을 누설하지 아니한다.",
            "연봉은 매년 1월 인사평가 결과에 따라 조정하며, 조정된 연봉은 별도 연봉계약서로 정한다.",
            "회사는 근로자의 사전 신청에 따라 주 1회 재택근무를 허용할 수 있다.",
            "근로자는 회사의 사전 승인 없이 다른 사업장에 겸직하지 아니한다.",
            "출장 시 교통비·숙박비는 회사 여비규정에 따라 실비로 지급한다.",
            f"입사 후 {rng.choice([1, 2])}개월 이내에 건강검진 결과서를 제출한다.",
            "업무상 필요한 경우 근로자의 동의를 얻어 근무장소를 변경할 수 있다.",
            "퇴직하고자 하는 경우 30일 전까지 회사에 서면으로 통보한다.",
            "시용기간 중 근무성적이 현저히 불량한 경우 본채용을 거부할 수 있다.",
            "개인정보 수집·이용 동의서는 별지로 작성하여 이 계약서에 첨부한다.",
            "회사가 지급한 노트북 등 업무용 장비는 퇴직 시 즉시 반납한다.",
            "탄력적 근로시간제를 실시하는 경우 근로자대표와의 서면합의에 따른다.",
            "명절 귀향비는 설·추석에 각 300,000원을 지급한다.",
        ]
        d["special_terms"] = rng.sample(pool, min(n_terms, len(pool)))
    return d


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


def _biz_no(r: random.Random) -> str:
    return f"{r.randint(101, 899)}-{r.randint(10, 99)}-{r.randint(10000, 99999)}"


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


@doc("pension_enrollment_certificate", "국민연금 가입자 가입증명", "income")
def pension_enrollment_certificate(p: Profile, rng: random.Random) -> dict:
    """국민연금공단 발급 가입자 가입증명 — 국민연금법 시행규칙 [별지 제11호서식] 국민연금가입자증명서.

    □ 가입자의 인적사항(발급번호·발급일자·성명·주민등록번호) / □ 가입자의 종류 및 자격 취득일
    (최초 자격취득일, 가입자 종류·사업장명칭·자격취득일·자격상실일) / 증명 문구 / 국민연금공단 이사장.
    """
    hist = _work_history(p, many=heavy(rng, 0.3))  # 이직이 잦은 사람: 사업장 이동 다수
    exempt = special(rng, "pension_exemption", 0.15)  # 실직 기간 납부예외
    if exempt:
        hist = _ensure_gap(hist, "local", rng)
    voluntary = special(rng, "voluntary_member", 0.08)  # 소득 없는 기간 임의가입
    if voluntary:
        hist = _ensure_gap(hist, "dep", rng)
    df = rng.choice(["dot", "dash"])
    cur_wage = _pension_base(_t10(p.employment.annual_salary / 12) - _MEAL, p.issue_date)
    rows, months = [], 0
    for h in hist:
        end = h["end"] or p.issue_date
        if h["kind"] == "dep" and not voluntary:
            continue  # 소득 없는 배우자: 적용제외 (가입 이력 없음)
        kind = {"work": "사업장가입자", "local": "지역가입자", "dep": "임의가입자"}[h["kind"]]
        row = {"kind": kind, "start": D(h["start"], df)}
        if h["kind"] == "work":
            row["workplace"] = h["name"]
            row["wage"] = won(h["wage"] if h["wage"] else cur_wage, "")
        elif h["kind"] == "dep":
            row["wage"] = won(rng.choice([1_000_000, 1_000_000, 1_500_000, 2_000_000]) if h["start"].year >= 2015
                              else rng.choice([700_000, 900_000, 1_000_000]), "")
        else:
            row["wage"] = won(K.round_to(rng.uniform(900_000, 1_500_000), 1000), "")
            if exempt and (rng.random() < 0.7 or not any(r_.get("note", "").startswith("납부예외") for r_ in rows)):
                row["note"] = rng.choice(["납부예외(실직)", "납부예외(실직)", "납부예외(휴·폐업)"])
        if not row.get("note", "").startswith("납부예외"):
            months += _months_between(h["start"], end)
        if h["end"]:
            row["end"] = D(h["end"], df)
        rows.append(row)
    return {
        "issue_no": f"{p.issue_date:%Y%m%d}-{rng.randint(10000000, 99999999)}",
        "person": {"name": p.person.name, "rrn": K.mask_rrn(p.person.rrn) if rng.random() < 0.5 else p.person.rrn},
        "first_acquired": D(next(h["start"] for h in hist if h["kind"] != "dep" or voluntary), df),
        "total_months": f"{months}개월",
        "rows": rows,
        "purpose": rng.choice(["금융기관 제출용", "은행 제출용", "기타"]),
        "issue_date": D(p.issue_date, "kor_short"),
        "issue_date_head": D(p.issue_date, df),
    }


@doc("health_insurance_qualification", "건강보험 자격득실확인서", "income")
def health_insurance_qualification(p: Profile, rng: random.Random) -> dict:
    """국민건강보험공단 발급 건강보험 자격득실 확인서 (국민건강보험법 제11조 자격취득 등의 확인).

    가입자구분(직장가입자·지역세대주·지역세대원·직장피부양자) / 사업장 명칭 / 자격취득일 / 자격상실일.
    """
    hist = _work_history(p, many=heavy(rng, 0.3))  # 이직이 잦은 사람: 자격 취득·상실 반복
    if special(rng, "regional_switch", 0.15):  # 퇴직 후 지역가입자로 전환된 기간
        hist = _ensure_gap(hist, "local", rng)
    if special(rng, "spouse_dependent", 0.1):  # 퇴직 후 배우자(가족)의 피부양자로 등재된 기간
        hist = _ensure_gap(hist, "dep", rng)
    fam_co = _company_name(random.Random(f"famco:{p.seed}"))
    df = rng.choice(["dot", "dash"])
    rows = [{"kind": "직장피부양자", "start": D(p.person.birth, df), "end": D(hist[0]["start"], df)}]
    items = []
    for h in hist:
        if h["kind"] == "work":
            row = {"kind": "직장가입자", "workplace": h["name"]}
        elif h["kind"] == "dep":
            row = {"kind": "직장피부양자", "workplace": fam_co}
        else:
            row = {"kind": rng.choice(["지역세대주", "지역세대원"])}
        items.append((h["start"], row, h["end"]))
    # 특수 상황: 두 사업장에 동시에 다닌 기간 (이중 직장가입)
    if special(rng, "dual_job", 0.05):
        lo, hi = p.employment.hire_date + timedelta(days=60), p.issue_date - timedelta(days=60)
        if hi > lo:
            ds = rand_date(rng, lo, hi)
            de = ds + timedelta(days=rng.randint(60, 400))
            items.append((ds, {"kind": "직장가입자", "workplace": _company_name(rng)}, de if de < p.issue_date else None))
            items.sort(key=lambda x: x[0])
    for start, row, end in items:
        row["start"] = D(start, df)
        if end:
            row["end"] = D(end, df)
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
    """국민건강보험공단 발급 건강보험료 납부확인서 (직장가입자 본인부담분, 월별 고지·납부 보험료를 건강/장기요양 구분)."""
    e = p.employment
    n = rng.randint(24, 36) if heavy(rng, 0.25) else rng.choice([6, 12, 12])  # 최근 2~3년치 요청
    hire_m = date(e.hire_date.year, e.hire_date.month, 1)
    last = months_back(p.issue_date, 1 if p.issue_date.day > 10 else 2)
    last = max(last, hire_m)
    regional = special(rng, "regional_switch", 0.12)  # 입사 전 지역가입자로 낸 보험료까지 조회
    overdue = special(rng, "overdue", 0.1)  # 지역가입자 기간의 체납·연체 후 납부
    settle = special(rng, "yearend_installment", 0.15)  # 건강보험 연말정산 추가징수 10회 분할납부
    lv = _leave_period(p) if special(rng, "parental_leave", 0.1) else None  # 육아휴직 보험료 경감·납입고지 유예
    months = [months_back(last, i) for i in range(n - 1, -1, -1)]
    months = [m for m in months if m >= hire_m or regional]
    local_h = K.round_to(rng.uniform(70_000, 230_000), 10)
    local_ms = [m for m in months if m < hire_m]
    late = set(rng.sample(local_ms, min(len(local_ms), rng.randint(1, 3)))) if overdue else set()
    aprils = [m for m in months if m.month == 4]
    s_start = aprils[-1] if aprils else None
    s_per = _t10(K.round_to(rng.uniform(80_000, 700_000), 10) / 10)

    def due(m):
        d_ = months_back(m, -1) + timedelta(days=9)
        while d_.weekday() >= 5:
            d_ += timedelta(days=1)
        return d_

    rows, tot = [], [0, 0, 0, 0]
    for m in months:
        _, hr, lr = _ins_rates(m.year)
        note = None
        if m < hire_m:
            h = _t10(local_h * (1 + 0.015 * (m.year - 2023)))
            note = "지역가입자"
        else:
            gross, mm, _, _ = _salary_for_year(p, m.year)
            h = _t10((gross / mm - _MEAL) * hr)
        if s_start and s_start <= m and (m.year * 12 + m.month) - (s_start.year * 12 + s_start.month) < 10:
            k = (m.year * 12 + m.month) - (s_start.year * 12 + s_start.month) + 1
            h += s_per
            note = f"정산 분할 {k}/10회"
        l = _t10(h * lr)
        nh, nl, ph, pl = h, l, h, l
        paid = D(due(m), "dot")
        if lv and date(lv[0].year, lv[0].month, 1) <= m <= lv[1]:
            nh = ph = _t10(h * 0.4)
            nl = pl = _t10(nh * lr)
            note = "육아휴직 경감"
            back = months_back(date(lv[1].year, lv[1].month, 1), -1)
            paid = D(due(back), "dot") if due(back) < p.issue_date else "납입고지유예"
            if paid == "납입고지유예":
                ph = pl = 0
        if m in late:
            pd_ = due(months_back(m, -rng.randint(2, 4)))
            if rng.random() < 0.45 or pd_ >= p.issue_date:
                ph = pl = 0
                paid, note = "미납", "체납"
            else:
                paid = D(pd_, "dot")
                note = f"연체금 {won(_t10((nh + nl) * 0.03), '')}원 별도"
        tot = [tot[0] + nh, tot[1] + nl, tot[2] + ph, tot[3] + pl]
        r_ = {"month": f"{m.year}.{m.month:02d}", "notice_health": won(nh, ""), "notice_ltc": won(nl, ""),
              "health": won(ph, ""), "ltc": won(pl, ""), "total": won(ph + pl, ""), "paid_date": paid}
        if note:
            r_["note"] = note
        rows.append(r_)
    tot_h, tot_l = tot[2], tot[3]
    biz = e.company.biz_no.replace("-", "")
    return {
        "issue_no": f"{rng.randint(10, 99)}-{rng.randint(100000, 999999)}-{rng.randint(1000, 9999)}",
        "person": {"name": p.person.name, "address": p.person.address.road_short,
                   **({"rrn": K.mask_rrn(p.person.rrn)} if rng.random() < 0.5 else {"birth": D(p.person.birth, "dot")})},
        "member_kind": "직장가입자",
        "workplace": {"name": e.company.name, "mgmt_no": f"{biz}0", "address": e.company.address.road_short},
        "period": f"{rows[0]['month']} ~ {rows[-1]['month']}",
        "rows": rows,
        "sum": {"notice_health": won(tot[0], ""), "notice_ltc": won(tot[1], ""),
                "health": won(tot_h, ""), "ltc": won(tot_l, ""), "total": won(tot_h + tot_l, "")},
        "purpose": rng.choice(["금융기관 제출용", "은행 제출용", "기타"]),
        "issue_date": D(p.issue_date, "kor_short"),
    }
