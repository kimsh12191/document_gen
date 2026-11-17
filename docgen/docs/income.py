"""소득·재직 관련 서류.

이 파일에는 그룹 서식들이 같이 쓰는 도우미만 있다. 서식마다 값 만드는 함수(@doc)는 서식 폴더
docgen/forms/<ID>/generate.py 에 있고, 끝의 FORMS 차례로 등록한다.
"""
from ._common import *  # noqa: F401,F403
from ..registry import register_folder_forms


# ---------------------------------------------------------------------------
# 급여·세금 계산 헬퍼 (income / finance 모듈 공용). 프로필 seed 로 결정되는 값은
# random.Random(f"...:{p.seed}") 를 써서 서로 다른 서류에서도 같은 값이 나오게 한다.
# ---------------------------------------------------------------------------
from ..entities import COMPANY_CORE, COMPANY_PREFIX  # noqa: E402

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


def _biz_no(r: random.Random) -> str:
    return f"{r.randint(101, 899)}-{r.randint(10, 99)}-{r.randint(10000, 99999)}"


# 이 그룹의 코드 서식. 값 만드는 함수는 서식 폴더 docgen/forms/<ID>/generate.py 에 있다 (여기는 같이 쓰는 도우미).
FORMS = ('employment_certificate', 'career_certificate', 'pay_stub', 'employment_contract', 'withholding_receipt', 'income_certificate', 'pension_enrollment_certificate', 'health_insurance_qualification', 'health_insurance_payment',)
register_folder_forms(__name__, FORMS)   # 예전 @doc 차례 그대로 등록 (서식 목록·데이터셋 순서)
