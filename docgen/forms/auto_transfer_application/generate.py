"""auto_transfer_application: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/bank_form_loan.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.bank_form_loan import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _LOAN_ACCT_FMT,
    _digits,
    _legal_bank,
    _loan_acct,
    _plan_personal,
    _spouse,
)
from docgen.registry import doc


def _add_months(d: date, n: int) -> date:
    y, m = divmod(d.year * 12 + d.month - 1 + n, 12)
    return date(y, m + 1, min(d.day, 28))


def _pmt(principal: int, annual_rate: float, months: int) -> int:
    i = annual_rate / 100 / 12
    if i == 0:
        return principal // months
    return int(round(principal * i / (1 - (1 + i) ** -months), -1))


@doc("auto_transfer_application", "자동이체 신청서", "bank_form", category="internal")
def auto_transfer_application(p: Profile, rng: random.Random) -> dict:
    """대출이자/원리금 자동이체 신청서."""
    pl = _plan_personal(p)
    per = p.person
    a = pl["debit_account"]
    amortizing = pl["repayment"] != "만기일시상환"
    target = "대출원리금" if amortizing else "대출이자"
    months = pl["term_years"] * 12
    if amortizing and pl["repayment"] == "원리금균등분할상환":
        est = _pmt(pl["amount"], pl["rate"]["applied"], months)
    elif amortizing:
        est = int(round(pl["amount"] / months + pl["amount"] * pl["rate"]["applied"] / 1200, -1))
    else:
        est = int(round(pl["amount"] * pl["rate"]["applied"] / 1200, -1))
    amount = (f"청구금액 전액 (약 {won(est)})" if rng.random() < 0.5
              else rng.choice(["청구금액 전액", "매월 청구금액"]) + f" / 예상 {won(est)}")
    df = rng.choice(["dot", "kor_short", "dash"])
    first = _add_months(pl["start_date"].replace(day=min(pl["pay_day"], 28)), 1)
    birth = per.birth
    data = {
        "bank": p.bank,
        "branch": p.bank_branch,
        "kind": rng.choice(["신규", "신규", "변경"]),
        "biller": {"name": _legal_bank(p.bank), "fee_type": f"{target}({pl['subject']})"},
        "applicant": {
            "name": per.name,
            "birth": birth.strftime(rng.choice(["%Y.%m.%d", "%y%m%d", "%Y-%m-%d"])),
            "phone": per.mobile,
            "address": per.address.road_short,
        },
        "debit": {"bank": a.bank, "account": a.number, "holder": a.holder,
                  "holder_birth": birth.strftime("%y%m%d"), "holder_phone": per.mobile},
        "relation": "본인",
        "target": target,
        "loan_account": pl["loan_account"],
        "loan_product": pl["product"],
        "transfer_day": f"매월 {pl['pay_day']}일",
        "start_month": f"{first.year}년 {first.month}월분부터" if df != "dash" else D(first, "dash"),
        "amount": amount,
        "privacy_consent": "동의함",
        "third_party_consent": "동의함",
        "apply_date": D(pl["apply_date"] + timedelta(days=rng.randint(2, 12)), rng.choice(["kor", "kor_short", df])),
        "signature": per.name,
        "holder_signature": a.holder,
    }
    if heavy(rng, 0.15):  # 여러 대출의 이자·원리금을 한 번에 자동이체 등록
        extra = []
        for _ in range(rng.randint(4, 9)):
            kind = rng.choice(["가계일반자금대출", "주택담보대출", "마이너스통장", "전세자금대출", "예적금담보대출", "보금자리론"])
            extra.append({"loan_account": _loan_acct(rng, p.bank), "loan_product": kind,
                          "target": rng.choice(["대출이자", "대출원리금"]), "transfer_day": f"매월 {rng.choice([5, 10, 15, 20, 25])}일"})
        data["extra_loans"] = extra
    if special(rng, "other_holder", 0.15):  # 가족(배우자) 명의 계좌에서 출금 → 예금주 별도 서명
        sp = _spouse(p, rng)
        bank = rng.choice([b for b in ("국민은행", "신한은행", "우리은행", "농협은행", p.bank) if b])
        data["debit"] = {"bank": bank, "account": _digits(rng, _LOAN_ACCT_FMT.get(bank, "###-##-######"), head="1"),
                         "holder": sp.name, "holder_birth": sp.birth.strftime("%y%m%d"), "holder_phone": sp.mobile}
        data["relation"] = "가족"
        data["holder_signature"] = sp.name
    if special(rng, "no_check", 0.08):  # 체크 누락
        data[rng.choice(["relation", "target", "third_party_consent"])] = None
    if special(rng, "sparse", 0.1):  # 선택 기재란 공란
        data["applicant"]["address"] = None
    return data
