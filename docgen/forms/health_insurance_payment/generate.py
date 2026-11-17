"""health_insurance_payment: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/income.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.income import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _MEAL,
    _ins_rates,
    _leave_period,
    _salary_for_year,
    _t10,
)
from docgen.registry import doc


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
    s_start = aprils[-1] if settle and aprils else None   # 정산 분할납부는 정한 확률(15%)일 때만 (평가 세트 2.0 에서 고침)
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
