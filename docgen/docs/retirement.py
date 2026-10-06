"""퇴직연금 서식 (DB·DC·개인형IRP).

하나은행 공개 서식에서 뽑은 기재란 명세를 따랐다
(add_template/field_specs/퇴직연금/{168,169,171,173,177,179}.json).

제도 기준
  근로자퇴직급여 보장법 — DB(확정급여형), DC(확정기여형), IRP(개인형퇴직연금)
  연금계좌 연간 납입한도 1,800만원 (전 금융기관 합산), 세액공제 한도 900만원
  사전지정운용제도(디폴트옵션) 2022.7.12 시행 — 그 전 서식에는 없다
"""
from ..banks import since
from ..registry import doc
from ._common import *  # noqa: F401,F403

# 하나은행 디폴트옵션 포트폴리오 (공개 서식 5-14-0020 2쪽 상품표 그대로)
DEFAULT_OPTIONS = [
    ("디폴트옵션 적극투자형 포트폴리오 1", "고위험(2등급)", "집합투자증권(100%)"),
    ("디폴트옵션 적극투자형 포트폴리오 2", "고위험(2등급)", "집합투자증권(100%)"),
    ("디폴트옵션 적극투자형 BF 3", "고위험(2등급)", "집합투자증권(100%)"),
    ("디폴트옵션 중립투자형 포트폴리오 1", "중위험(3등급)", "원리금보장상품(25%)+집합투자증권(75%)"),
    ("디폴트옵션 중립투자형 포트폴리오 2", "중위험(3등급)", "원리금보장상품(20%)+집합투자증권(80%)"),
    ("디폴트옵션 중립투자형 포트폴리오 3", "중위험(3등급)", "원리금보장상품(25%)+집합투자증권(75%)"),
    ("디폴트옵션 안정투자형 포트폴리오 1", "저위험(4등급)", "원리금보장상품(40%)+집합투자증권(60%)"),
    ("디폴트옵션 안정투자형 포트폴리오 2", "저위험(4등급)", "원리금보장상품(50%)+집합투자증권(50%)"),
    ("디폴트옵션 안정투자형 포트폴리오 3", "저위험(4등급)", "원리금보장상품(50%)+집합투자증권(50%)"),
    ("디폴트옵션 안정형 포트폴리오", "초저위험(5등급)", "원리금보장상품(100%)"),
]

PRODUCTS = [
    ("원리금보장", "정기예금 (1년)", "초저위험"),
    ("원리금보장", "정기예금 (3년)", "초저위험"),
    ("원리금보장", "이율보증형 보험(GIC) 1년", "초저위험"),
    ("실적배당", "TDF 2035 증권자투자신탁", "중위험"),
    ("실적배당", "TDF 2045 증권자투자신탁", "고위험"),
    ("실적배당", "국내채권형 증권자투자신탁", "저위험"),
    ("실적배당", "글로벌주식형 증권자투자신탁", "고위험"),
    ("실적배당", "인덱스(KOSPI200) 증권자투자신탁", "중위험"),
]

JOIN_QUALIFY = ["당행 퇴직연금 가입자", "타금융기관 퇴직연금 가입자",
                "직역연금가입자(공무원·사학·군인·별정우체국)", "근로기간 1년미만 근로자",
                "1주 15시간 미만 근로자", "퇴직금제도 적용 근로자", "자영업자"]


def _staff(rng: random.Random) -> dict:
    return {"clerk": K.make_name(rng, rng.choice("MF"))[0],
            "manager": K.make_name(rng, rng.choice("MF"))[0]}


def _date(p: Profile, rng: random.Random) -> str:
    return D(p.issue_date, rng.choice(["kor", "kor", "kor_short", "dot"]))


def _acct(p: Profile, rng: random.Random) -> str:
    """퇴직연금 계좌번호 — 상품코드 형태."""
    return f"{rng.randint(100, 999)}-{rng.choice(['14', '15', '16'])}-{rng.randint(100000, 999999)}"


def _notice(p: Profile, rng: random.Random) -> dict:
    """통지 수신 방법 — 알림톡은 2018년 이후 서식에만 있다."""
    ways = ["이메일", "알림톡(LMS)"] if since(p.issue_date, "kakao_notice") else ["이메일", "우편"]
    return {
        "maturity": rng.choice(ways),
        "service_excluded": rng.choices(["신청안함(발송)", "신청(미발송)"], weights=[72, 28])[0],
        "terms_change": rng.choice(ways + ["수신거부"]),
    }


def _buy_plan(rng: random.Random, n: int) -> list[dict]:
    """상품별 매수비율 — 합이 100% 가 되게 맞춘다."""
    picks = rng.sample(PRODUCTS, k=n)
    cuts = sorted(rng.sample(range(1, 20), n - 1)) if n > 1 else []
    bounds = [0, *cuts, 20]
    ratios = [(bounds[i + 1] - bounds[i]) * 5 for i in range(n)]
    return [{"kind": k, "name": nm, "risk": r, "ratio": f"{ratio}%"}
            for (k, nm, r), ratio in zip(picks, ratios)]


def _participant(p: Profile) -> dict:
    per = p.person
    return {"name": per.name, "birth": D(per.birth, "dot"), "phone": per.mobile, "email": per.email,
            "address": per.address.road_short}


# ---------------------------------------------------------------------------
# 퇴직연금 거래신청서 (개인형IRP) — 5-14-0020
# ---------------------------------------------------------------------------


@doc("irp_account_application", "퇴직연금 거래신청서(개인형IRP)", "retirement", category="internal")
def irp_account_application(p: Profile, rng: random.Random) -> dict:
    """개인형퇴직연금(IRP) 계좌를 개설하고 운용상품·디폴트옵션을 지정하는 거래신청서."""
    limit = rng.choice([3_000_000, 6_000_000, 9_000_000, 12_000_000, 18_000_000])
    use = rng.choices(["퇴직금용", "퇴직금용+적립용"], weights=[42, 58])[0]
    qualify = JOIN_QUALIFY[:] if since(p.issue_date, "irp_expand") else JOIN_QUALIFY[:3]
    advice = rng.choices(["투자권유를 희망함", "투자권유를 희망하지 않음"], weights=[68, 32])[0]
    data = {
        "bank": p.bank,
        "branch": p.bank_branch,
        "participant": _participant(p),
        "happy_call": rng.choices(["전화(휴대폰)", "온라인(모바일 웹)"], weights=[55, 45])[0],
        "use": use,
        "qualify": rng.choice(qualify),
        "annual_limit": K.won(limit),
        "discount": rng.choices(["해당 없음", "장애인 등록증 소지 고객", "장기할인(타사IRP이전)"],
                                weights=[84, 5, 11])[0],
        "notice": _notice(p, rng),
        "advice": advice,
        "corp_plan": _buy_plan(rng, rng.randint(1, 3)),
        "personal_same": rng.choices(["동일 운용지시", "별도 지정"], weights=[58, 42])[0],
        "consumer_type": rng.choices(["일반투자자(투자자정보확인서에서 일반투자자 선택)",
                                      "전문투자자(투자자정보확인서에서 전문투자자 선택)"], weights=[94, 6])[0],
        "doc_receive": rng.choice(["서면 수령", "이메일", "알림톡"] if since(p.issue_date, "kakao_notice")
                                  else ["서면 수령", "이메일"]),
        "handwritten": ("설명을 듣고 이해하였음" if advice == "투자권유를 희망함"
                        else "설명을 듣고 이해하였음"),
        "account": _acct(p, rng),
        "date": _date(p, rng),
        "signature": p.person.name,
        "staff": _staff(rng),
    }
    if since(p.issue_date, "default_option"):
        name, risk, mix = rng.choice(DEFAULT_OPTIONS)
        data["default_option"] = {"name": f"{p.bank} {name}", "risk": risk, "mix": mix}
        data["options"] = [{"name": f"{p.bank} {n}", "risk": r, "mix": mx} for n, r, mx in DEFAULT_OPTIONS]
    if data["personal_same"] == "별도 지정":
        data["personal_plan"] = _buy_plan(rng, rng.randint(1, 3))
    return data


# ---------------------------------------------------------------------------
# 퇴직연금 가입자 거래신청서 (DC·기업형IRP)
# ---------------------------------------------------------------------------


@doc("dc_participant_application", "퇴직연금 가입자 거래신청서(DC·기업형IRP)", "retirement", category="internal")
def dc_participant_application(p: Profile, rng: random.Random) -> dict:
    """사용자가 설정한 확정기여형(DC)·기업형IRP 제도에 근로자를 가입자로 등록하는 신청서."""
    emp = p.employment
    kind = rng.choices(["DC", "기업형IRP"], weights=[78, 22])[0]
    monthly = K.round_to(emp.annual_salary / 12 / 12, 10_000)  # 연간 임금총액의 1/12
    data = {
        "bank": p.bank,
        "branch": p.bank_branch,
        "plan_kind": kind,
        "employer": {
            "name": emp.company.name,
            "biz_no": emp.company.biz_no,
            "contract_no": f"{rng.randint(10000, 99999)}-{rng.randint(100, 999)}",
            "phone": emp.company.phone,
        },
        "participant": {
            **_participant(p),
            "employee_no": emp.employee_no,
            "department": emp.department,
            "position": emp.position,
            "hire_date": D(emp.hire_date, "dot"),
            "join_date": D(recent(rng, p, 20), "dot"),
        },
        "contribution": {
            "monthly": K.won(monthly),
            "annual": K.won(monthly * 12),
            "pay_day": f"매월 {rng.choice([10, 15, 20, 25])}일",
            "extra": K.won(rng.choice([0, 0, 500_000, 1_000_000, 2_000_000])),
        },
        "notice": _notice(p, rng),
        "plan": _buy_plan(rng, rng.randint(1, 4)),
        "account": _acct(p, rng),
        "date": _date(p, rng),
        "signature": p.person.name,
        "staff": _staff(rng),
    }
    if since(p.issue_date, "default_option"):
        name, risk, mix = rng.choice(DEFAULT_OPTIONS)
        data["default_option"] = {"name": f"{p.bank} {name}", "risk": risk, "mix": mix}
    return data


# ---------------------------------------------------------------------------
# 퇴직연금 운용상품지정 신청서 (DC)
# ---------------------------------------------------------------------------


@doc("dc_product_selection", "퇴직연금 운용상품지정 신청서(DC)", "retirement", category="internal")
def dc_product_selection(p: Profile, rng: random.Random) -> dict:
    """확정기여형(DC) 가입자가 적립금 운용상품과 매수비율을 지정·변경하는 신청서."""
    emp = p.employment
    balance = K.round_to(emp.annual_salary / 12 * max(1, (p.issue_date.year - emp.hire_date.year)), 10_000)
    kind = rng.choices(["신규 지정", "변경(상품 교체)", "비율 변경"], weights=[38, 34, 28])[0]
    new_plan = _buy_plan(rng, rng.randint(2, 4))
    data = {
        "bank": p.bank,
        "branch": p.bank_branch,
        "kind": kind,
        "employer": {"name": emp.company.name, "biz_no": emp.company.biz_no},
        "participant": {**_participant(p), "employee_no": emp.employee_no},
        "account": _acct(p, rng),
        "balance": K.won(balance),
        "apply_to": rng.choices(["기존 적립금 + 향후 부담금", "향후 부담금만", "기존 적립금만"],
                                weights=[48, 34, 18])[0],
        "new_plan": new_plan,
        "effective": D(p.issue_date + timedelta(days=rng.choice([1, 2, 3])), "dot"),
        "date": _date(p, rng),
        "signature": p.person.name,
        "staff": _staff(rng),
    }
    if kind != "신규 지정":
        data["old_plan"] = _buy_plan(rng, rng.randint(1, 3))
    return data


# ---------------------------------------------------------------------------
# 퇴직연금 사전지정운용방법(디폴트옵션) 지정 신청서
# ---------------------------------------------------------------------------


@doc("default_option_designation", "퇴직연금 사전지정운용방법 지정 신청서", "retirement", category="internal")
def default_option_designation(p: Profile, rng: random.Random) -> dict:
    """가입자가 별도 운용지시를 하지 않을 때 적용될 사전지정운용방법(디폴트옵션)을 지정하는 신청서."""
    name, risk, mix = rng.choice(DEFAULT_OPTIONS)
    plan_kind = rng.choices(["DC", "개인형IRP", "기업형IRP"], weights=[52, 36, 12])[0]
    return {
        "bank": p.bank,
        "branch": p.bank_branch,
        "plan_kind": plan_kind,
        "kind": rng.choices(["신규 지정", "변경 지정"], weights=[72, 28])[0],
        "participant": _participant(p),
        "account": _acct(p, rng),
        "employer": {"name": p.employment.company.name} if plan_kind != "개인형IRP" else {"name": "해당 없음"},
        "selected": {"name": f"{p.bank} {name}", "risk": risk, "mix": mix},
        "options": [{"name": f"{p.bank} {n}", "risk": r, "mix": mx} for n, r, mx in DEFAULT_OPTIONS],
        "advice": rng.choices(["투자권유를 희망함", "투자권유를 희망하지 않음"], weights=[62, 38])[0],
        "handwritten": "설명을 듣고 이해하였음",
        "date": _date(p, rng),
        "signature": p.person.name,
        "staff": _staff(rng),
    }


# ---------------------------------------------------------------------------
# 퇴직연금 퇴직급여 지급신청서 (DB)
# ---------------------------------------------------------------------------

PAY_REASONS = ["정년퇴직", "자발적 퇴직", "회사 사정에 의한 퇴직", "정리해고", "계약기간 만료"]


@doc("retirement_benefit_claim", "퇴직연금 퇴직급여 지급신청서(DB)", "retirement", category="internal")
def retirement_benefit_claim(p: Profile, rng: random.Random) -> dict:
    """확정급여형(DB) 가입자가 퇴직에 따라 퇴직급여의 지급을 신청하는 서식."""
    emp = p.employment
    years = max(1, p.issue_date.year - emp.hire_date.year)
    avg_wage = K.round_to(emp.annual_salary / 12, 10_000)
    benefit = K.round_to(avg_wage * years, 10_000)
    way = rng.choices(["IRP 계좌 이전", "일시금 지급", "연금 수령"], weights=[66, 22, 12])[0]
    # 55세 미만 퇴직은 IRP 이전이 의무다 (근퇴법 제17조)
    if p.person.age < 55:
        way = "IRP 계좌 이전" if rng.random() < 0.9 else way
    tax = K.round_to(benefit * rng.uniform(0.02, 0.08), 10) if way != "IRP 계좌 이전" else 0
    return {
        "bank": p.bank,
        "branch": p.bank_branch,
        "employer": {"name": emp.company.name, "biz_no": emp.company.biz_no,
                     "contract_no": f"{rng.randint(10000, 99999)}-{rng.randint(100, 999)}"},
        "participant": {**_participant(p), "employee_no": emp.employee_no,
                        "hire_date": D(emp.hire_date, "dot"),
                        "leave_date": D(recent(rng, p, 30), "dot"),
                        "service_years": f"{years}년"},
        "reason": rng.choice(PAY_REASONS),
        "benefit": {
            "avg_wage": K.won(avg_wage),
            "amount": K.won(benefit),
            "tax": K.won(tax),
            "net": K.won(benefit - tax),
        },
        "way": way,
        "irp": {"bank": p.bank, "account": _acct(p, rng), "holder": p.person.name},
        "pay_account": p.accounts[0].number,
        "pay_date": D(p.issue_date + timedelta(days=rng.randint(3, 14)), "dot"),
        "date": _date(p, rng),
        "signature": p.person.name,
        "staff": _staff(rng),
    }


# ---------------------------------------------------------------------------
# 투자자확인서 (퇴직연금용)
# ---------------------------------------------------------------------------

INVEST_GOALS = ["원금 보존 위주", "안정적인 이자·배당 수익", "물가상승률 이상의 수익", "적극적인 자산 증식"]
INVEST_EXP = ["없음", "1년 미만", "1년 이상 3년 미만", "3년 이상"]
LOSS_TOLERANCE = ["원금 손실을 감수할 수 없음", "10% 미만", "10% 이상 20% 미만", "20% 이상"]
RISK_GRADES = ["초저위험", "저위험", "중위험", "고위험", "초고위험"]


@doc("investor_profile_retirement", "투자자확인서(퇴직연금용)", "retirement", category="internal")
def investor_profile_retirement(p: Profile, rng: random.Random) -> dict:
    """퇴직연금 가입자의 투자성향을 확인하여 적합한 상품 위험등급을 판정하는 확인서."""
    per = p.person
    goal = rng.choices(INVEST_GOALS, weights=[26, 34, 28, 12])[0]
    exp = rng.choices(INVEST_EXP, weights=[22, 18, 30, 30])[0]
    loss = rng.choices(LOSS_TOLERANCE, weights=[24, 36, 28, 12])[0]
    score = (INVEST_GOALS.index(goal) * 8 + INVEST_EXP.index(exp) * 7
             + LOSS_TOLERANCE.index(loss) * 9 + rng.randint(5, 20))
    grade = RISK_GRADES[min(4, score // 13)]
    if per.age >= 65:  # 고령투자자는 보수적으로 판정되는 경향
        grade = RISK_GRADES[max(0, RISK_GRADES.index(grade) - 1)]
    return {
        "bank": p.bank,
        "branch": p.bank_branch,
        "participant": _participant(p),
        "account": _acct(p, rng),
        "investor_type": rng.choices(["일반투자자", "전문투자자"], weights=[95, 5])[0],
        "elderly": "해당" if per.age >= 65 else "비해당",
        "age_band": ("만 65세 이상" if per.age >= 65 else
                     "만 50세 이상 만 65세 미만" if per.age >= 50 else "만 50세 미만"),
        "goal": goal,
        "experience": exp,
        "loss_tolerance": loss,
        "horizon": rng.choice(["1년 이내", "1년 이상 3년 미만", "3년 이상 5년 미만", "5년 이상"]),
        "income_source": rng.choices(["근로소득", "사업소득", "연금소득", "기타소득"],
                                     weights=[70, 14, 12, 4])[0],
        "asset_ratio": rng.choice(["10% 이하", "10~20%", "20~30%", "30% 초과"]),
        "score": str(score),
        "grade": grade,
        "agreed": rng.choices(["판정 결과에 동의함", "판정 결과보다 높은 위험등급 상품 거래를 희망함"],
                              weights=[91, 9])[0],
        "handwritten": "설명을 듣고 이해하였음",
        "date": _date(p, rng),
        "signature": per.name,
        "staff": _staff(rng),
    }
