"""employment_contract: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/income.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.income import _DUTIES, _MEAL, _pay_cfg, _t10  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


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
