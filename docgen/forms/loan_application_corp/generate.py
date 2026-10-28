"""loan_application_corp: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/bank_form_loan.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.bank_form_loan import _korean_amount, _plan_corp, _term_text  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("loan_application_corp", "기업여신 신청서", "bank_form", category="internal")
def loan_application_corp(p: Profile, rng: random.Random) -> dict:
    """법인 고객 기업여신 신청서 (은행 자체 서식)."""
    c = p.corporation
    pl = _plan_corp(p)
    fy = p.issue_date.year - 1
    rev = c.revenue
    size = "중소기업" if rev < 150_000_000_000 else rng.choice(["중견기업", "중소기업"]) if rev < 300_000_000_000 else "중견기업"
    other = []
    many = heavy(rng, 0.25)  # 거래 금융기관이 많은 기업 → 타 금융기관 여신 현황이 길어진다
    pool = [b for b in ["국민은행", "신한은행", "우리은행", "하나은행", "농협은행", "기업은행", "산업은행", "수협은행"]
            + (["수출입은행", "부산은행", "경남은행", "iM뱅크", "SC제일은행", "OK저축은행", "SBI저축은행",
                "현대캐피탈", "KB캐피탈", "신한캐피탈"] if many else [])
            if b != p.bank and not (b == "하나은행" and p.bank == "KEB하나은행")]
    for _ in range(rng.randint(7, 16) if many else rng.choice([0, 1, 1, 2, 2])):
        lender = rng.choice(pool)
        kind = rng.choice(["운전자금대출", "시설자금대출", "무역금융", "할인어음", "당좌대출", "구매자금대출"]
                          + (["외화대출", "수입신용장(L/C)", "리스", "팩토링"] if many else []))
        if (lender, kind) in ((x["lender"], x["kind"]) for x in other) or (not many and lender in (x["lender"] for x in other)):
            continue
        other.append({"lender": lender, "kind": kind,
                      "balance": K.round_to(rev * rng.uniform(0.002 if many else 0.005, 0.02 if many else 0.04), 10_000_000) // 1_000_000,
                      "collateral": rng.choice(["신용", "부동산", "신용보증기금", "기술보증기금", "예금"])})
    total = sum(x["balance"] for x in other)
    for x in other:
        x["balance"] = f"{x['balance']:,}"
    data = {
        "bank": p.bank,
        "branch": p.bank_branch,
        "company": {
            "name": c.name,
            "name_en": c.name_en,
            "biz_no": c.biz_no,
            "corp_no": c.corp_no,
            "ceo": c.ceo.name,
            "established": D(c.established, rng.choice(["dot", "kor"])),
            "industry": f"{c.biz_type} / {c.biz_item}",
            "employees": f"{c.employees:,}명",
            "size": size,
            "revenue": won(c.revenue) if rng.random() < 0.4 else f"{c.revenue // 1_000_000:,}백만원",
            "revenue_year": f"{fy}년",
            "capital": won(c.capital),
            "address": c.address.road_full,
            "phone": c.phone,
            "fax": c.fax,
        },
        "contact": {
            "name": pl["contact"],
            "position": pl["contact_pos"],
            "phone": pl["contact_phone"],
            "email": c.email,
        },
        "loan": {
            "subject": pl["kind"],
            "product": pl["product"],
            "amount": won(pl["amount"]),
            "amount_korean": _korean_amount(pl["amount"], rng),
            "term": _term_text(pl["term_years"], rng),
            "hope_date": D(pl["start_date"], rng.choice(["dot", "dash"])),
            "repayment": pl["repayment"],
            "rate_type": pl["rate_type"],
            "fund_type": "시설자금" if pl["kind"] == "시설자금대출" else "운전자금",
            "purpose": pl["purpose"],
            "deposit_account": f"{p.bank} {pl['debit_account']}",
            "collateral": pl["collateral"],
            "collateral_detail": pl["collateral_detail"],
        },
        "other_loans": other,
        "apply_date": D(pl["apply_date"], rng.choice(["kor", "kor_short"])),
        "signature": c.ceo.name,
    }
    if len(other) >= 3:
        data["other_loans_total"] = f"{total:,}"
    if special(rng, "agent", 0.15):  # 직원이 대리인으로 신청 (법인인감 날인 위임장 첨부)
        data["agent"] = {"name": pl["contact"], "position": pl["contact_pos"], "phone": pl["contact_phone"],
                         "rrn": K.mask_rrn(K.rrn(rng, rand_date(rng, date(p.issue_date.year - 50, 1, 1),
                                                                 date(p.issue_date.year - 26, 12, 31)), rng.choice("MF")))}
    if special(rng, "sparse", 0.15):  # 선택 항목 미기재
        for k in rng.sample(["fax", "name_en", "employees"], rng.randint(1, 3)):
            data["company"][k] = None
        if rng.random() < 0.5:
            data["contact"]["email"] = None
    if special(rng, "no_check", 0.1):  # 체크 누락
        k = rng.choice(["company.size", "loan.fund_type", "loan.rate_type"])
        data[k.split(".")[0]][k.split(".")[1]] = None
    return data
