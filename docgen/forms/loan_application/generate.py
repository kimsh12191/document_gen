"""loan_application: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/bank_form_loan.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.bank_form_loan import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _OTHER_LENDERS,
    _add_years,
    _korean_amount,
    _lenders,
    _plan_personal,
    _relative,
    _spouse,
    _term_text,
)
from docgen.registry import doc


def _home_phone(r: random.Random, p: Profile) -> str:
    return K.landline(r, p.person.address.sido)


_DWELLING = {"아파트": "아파트", "오피스텔": "오피스텔", "단독주택": "단독", "다세대주택": "다세대"}


def _debts(p: Profile, pl: dict, rng: random.Random, df: str, n: int | None = None) -> list[dict]:
    """부채현황 (타 금융기관 대출). 대환이면 상환 대상 대출을 반드시 넣는다. n: 건수 (다중채무 고객)."""
    out = []
    lenders = _lenders(p)
    sal = p.employment.annual_salary
    if "대환" in pl["purpose"]:
        lender = rng.choice([b for b in _OTHER_LENDERS[:5] if b in lenders])
        kind = "주택담보대출" if pl["kind"] == "mortgage" else "신용대출"
        out.append({"lender": lender, "kind": kind,
                    "balance": won(K.round_to(pl["amount"] * rng.uniform(0.85, 1.0), 100_000), ""),
                    "maturity": D(_add_years(p.issue_date, rng.randint(1, 25)), df), "refinance": "상환예정"})
    for _ in range((rng.choice([0, 0, 1, 1, 2]) if n is None else n) - len(out)):
        lender = rng.choice(lenders)
        kind = "카드론" if "카드" in lender else rng.choice(["신용대출", "마이너스통장", "자동차할부", "학자금대출"]
                                                         + (["현금서비스", "보험약관대출"] if n else []))
        bal = K.round_to(sal * rng.uniform(0.03, 0.4 if n is None else 0.15), 100_000)
        mat = _add_years(p.issue_date, rng.randint(1, 5)) + timedelta(days=rng.randint(-160, 160))
        out.append({"lender": lender, "kind": kind, "balance": won(bal, ""), "maturity": D(mat, df),
                    "refinance": "상환예정" if n and rng.random() < 0.15 else "유지"})
    return out


@doc("loan_application", "대출거래신청서", "bank_form", category="internal")
def loan_application(p: Profile, rng: random.Random) -> dict:
    """개인 고객 대출신청서(가계용). 하나은행 「대출신청서(가계용)」, 신한은행 「대출상담및신청서(가계용)」 항목 구성 참고."""
    pl = _plan_personal(p)
    per, e, prop = p.person, p.employment, p.property
    df = rng.choice(["dot", "kor", "dash"])
    owns_home = prop.address.road_short == per.address.road_short
    if owns_home:
        housing = "자가"
    elif pl["kind"] == "jeonse":
        housing = "전세"
    else:
        housing = rng.choices(["전세", "월세", "기타"], weights=[60, 30, 10])[0]
    if owns_home:
        dwelling = _DWELLING.get(prop.kind, "아파트")
    else:
        dwelling = rng.choices(["아파트", "다세대", "연립·빌라", "오피스텔", "단독"], weights=[55, 15, 12, 12, 6])[0]
    if pl["collateral"] == "부동산":
        col_detail = f"{prop.address.road_short} ({prop.kind}, 전용 {prop.exclusive_area}㎡)"
    elif pl["collateral"] == "보증":
        col_detail = f"{pl['guarantor']} 보증서"
    else:
        col_detail = rng.choice(["신용", "무보증 신용", "신용(급여이체 조건)"])
    acct = pl["debit_account"]
    salary = e.annual_salary
    job = "전문직" if pl["product"].startswith("전문직") else rng.choices(["급여소득자", "공무원"], weights=[92, 8])[0]
    purpose_cat = ("주택구입" if pl["purpose"] == "주택구입자금" else "주택임차" if pl["kind"] == "jeonse"
                   else "부채상환" if "대환" in pl["purpose"] else "생활비")
    assets = []
    if owns_home or (pl["collateral"] == "부동산" and pl["purpose"] != "주택구입자금"):
        assets.append({"kind": prop.kind.replace("주택", ""), "location": prop.address.road_short.split(",")[0],
                       "value": won(K.round_to(prop.price, 10_000_000), "")})
    dep = sum(a.balance for a in p.accounts)
    if dep > 1_000_000 and rng.random() < 0.7:
        assets.append({"kind": "예금", "location": ", ".join(list(dict.fromkeys(a.bank for a in p.accounts))[:2]),
                       "value": won(K.round_to(dep, 100_000), "")})
    data = {
        "bank": p.bank,
        "branch": p.bank_branch,
        "applicant": {
            "name": per.name,
            "rrn": per.rrn if rng.random() < 0.4 else K.mask_rrn(per.rrn),
            "address": per.address.road_full,
            "zipcode": per.address.zipcode,
            "mobile": per.mobile,
            "email": per.email,
            "home_phone": _home_phone(rng, p),
            "work_phone": e.company.phone,
        },
        "workplace": {
            "job_type": job,
            "name": e.company.name,
            "department": e.department,
            "position": e.position,
            "hire_date": D(e.hire_date, df),
            "annual_income": won(salary) if rng.random() < 0.5 else f"{salary // 10000:,}만원",
            "address": e.company.address.road_short,
        },
        "housing": housing,
        "dwelling": dwelling,
        "debts": _debts(p, pl, rng, rng.choice(["dot", "dash"])),
        "assets": assets,
        "loan": {
            "subject": pl["subject"],
            "product": pl["product"],
            "amount": won(pl["amount"], ""),
            "amount_korean": _korean_amount(pl["amount"], rng),
            "term": _term_text(pl["term_years"], rng),
            "hope_date": D(pl["start_date"], df),
            "repayment": {"원리금균등분할상환": "원리금균등분할", "원금균등분할상환": "원금균등분할",
                          "만기일시상환": "만기일시"}[pl["repayment"]],
            "rate_type": pl["rate_type"][:2],
            "purpose_category": purpose_cat,
            "purpose": pl["purpose"],
            "interest_day": f"매월 {pl['pay_day']}일",
            "debit_bank": acct.bank,
            "debit_account": acct.number,
            "debit_holder": acct.holder,
        },
        "collateral": pl["collateral"],
        "collateral_detail": col_detail,
        "consent": "동의함",
        "manual_received": "예",
        "apply_date": D(pl["apply_date"], rng.choice(["kor", "kor_short"])),
        "signature": per.name,
    }
    _loan_app_variants(p, pl, rng, data)
    return data


def _loan_app_variants(p: Profile, pl: dict, rng: random.Random, data: dict) -> None:
    """대출신청서 변형: 다중채무(여러 쪽), 공동차주, 대리인 신청, 공란 많은 서식, 체크 누락."""
    if heavy(rng, 0.2):  # 타 금융기관 대출·재산이 많은 고객 → 부채현황 표가 길어진다
        data["debts"] = _debts(p, pl, rng, rng.choice(["dot", "dash"]), n=rng.randint(6, 14))
        assets = data["assets"]
        for _ in range(rng.randint(2, 4)):
            kind = rng.choice(["예금", "적금", "주식", "펀드", "자동차", "보험(해약환급금)"])
            where = {"자동차": rng.choice(["그랜저 (2021년식)", "쏘렌토 (2020년식)", "K5 (2019년식)", "아반떼 (2022년식)"]),
                     "주식": rng.choice(["미래에셋증권", "키움증권", "삼성증권", "한국투자증권"]),
                     "펀드": rng.choice(["KB자산운용", "미래에셋자산운용", "삼성자산운용"]),
                     "보험(해약환급금)": rng.choice(["삼성생명", "한화생명", "교보생명"])}.get(kind, rng.choice(_lenders(p)[:5]))
            assets.append({"kind": kind, "location": where,
                           "value": won(K.round_to(p.employment.annual_salary * rng.uniform(0.05, 0.6), 100_000), "")})
    if special(rng, "co_borrower", 0.12):  # 부부 공동명의 등 공동차주(공동신청인)
        sp = _spouse(p, rng)
        data["co_borrower"] = {"name": sp.name, "rrn": K.mask_rrn(sp.rrn), "relation": "배우자", "mobile": sp.mobile,
                               "workplace": rng.choice(["", "", "주부", "자영업", f"{p.employment.company.name[:2]}물산"]) or None}
    if special(rng, "agent", 0.1):  # 대리인 신청 (위임장·인감증명서 첨부)
        ag, rel = _relative(p, rng)
        data["agent"] = {"name": ag.name, "rrn": K.mask_rrn(ag.rrn), "relation": rel, "phone": ag.mobile,
                         "poa": "첨부"}
    if special(rng, "sparse", 0.15):  # 선택 항목을 비워 둔 서식
        ap, wp = data["applicant"], data["workplace"]
        for k in rng.sample(["email", "home_phone", "work_phone", "zipcode"], rng.randint(2, 4)):
            ap[k] = None
        if rng.random() < 0.6:
            wp["address"] = None
        if rng.random() < 0.5:
            wp["department"] = None
    if special(rng, "no_check", 0.1):  # 체크 누락
        for k in rng.sample(["housing", "dwelling", "loan.rate_type"], rng.randint(1, 2)):
            if "." in k:
                data["loan"][k.split(".")[1]] = None
            else:
                data[k] = None
