"""credit_agreement: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/bank_form_loan.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.bank_form_loan import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _agreement_terms,
    _agreement_variants,
    _legal_bank,
    _lenders,
    _plan_personal,
    _stamp_tax,
)
from docgen.registry import doc


# 약정서 특약사항 (여러 쪽 약정서). 은행이 입력해 출력하는 문구.
_TERMS_PERSONAL = [
    "급여이체 및 당행 신용카드 결제계좌를 대출기간 중 당행으로 유지하는 조건으로 우대금리 연 {p1:.1f}%p를 적용하며, 조건 미충족 시 그 다음 이자계산기간부터 우대금리를 적용하지 아니한다.",
    "채무자는 대출 실행일로부터 {m}개월 이내에 담보물건에 전입하여 실거주하여야 하며, 이를 이행하지 아니하는 경우 은행은 기한의 이익을 상실시킬 수 있다.",
    "채무자는 대출기간 중 담보주택 외 추가 주택을 취득하지 아니하기로 하며, 이를 위반한 경우 즉시 대출금을 상환한다.",
    "이 대출금은 {purpose} 용도로만 사용하며, 은행이 요청하는 경우 자금 사용 증빙서류를 제출한다.",
    "대환 대상 대출({lender})은 대출 실행일에 은행이 직접 상환하며, 채무자는 상환영수증을 은행에 제출한다.",
    "기준금리 변동 시 대출이자율은 매 {reset} 단위로 변경되며, 변경된 이자율은 은행 홈페이지 및 문자메시지로 통지한다.",
    "은행이 정한 중도상환해약금 면제 요건(대출 실행 후 3년 경과 등)에 해당하는 경우 중도상환해약금을 면제한다.",
    "채무자가 은행의 동의 없이 담보물건에 임대차(전세권 설정 포함)를 하는 경우 은행은 추가 담보 제공 또는 대출금 일부 상환을 요구할 수 있다.",
    "자동이체계좌 잔액 부족으로 이자를 납입하지 못한 경우 은행은 채무자의 당행 다른 예금 계좌에서 출금하여 충당할 수 있다.",
    "채무자는 주소·연락처·직장 등 신용상태에 중요한 변동이 있는 경우 지체 없이 은행에 서면으로 신고한다.",
    "본 대출의 우대금리 합계는 연 {p2:.1f}%p를 한도로 하며, 우대 항목별 충족 여부는 매월 말일 기준으로 판단한다.",
]


@doc("credit_agreement", "대출거래약정서(가계용)", "bank_form", category="internal")
def credit_agreement(p: Profile, rng: random.Random) -> dict:
    """대출거래약정서(가계용) 첫 장. 은행연합회 표준 구성(제1조 거래조건 ~ 인지세 부담) 기준."""
    pl = _plan_personal(p)
    per = p.person
    df = rng.choice(["dot", "kor_short", "dash"])
    a = pl["debit_account"]
    terms = _agreement_terms({**pl, "debit_bank": a.bank, "debit_number": a.number}, rng, df)
    reset = {"고정금리": "해당없음(만기까지 고정)", "혼합금리": "최초 5년 고정 후 6개월마다 변동",
             "변동금리": rng.choice(["6개월", "3개월", "12개월"])}[pl["rate_type"]]
    limit = pl["subject"].endswith("(한도)")
    data = {
        "bank": p.bank,
        "creditor": _legal_bank(p.bank),
        "branch": p.bank_branch,
        "debtor": {
            "name": per.name,
            "rrn": K.mask_rrn(per.rrn) if rng.random() < 0.5 else per.rrn,
            "address": per.address.road_full,
            "phone": per.mobile,
        },
        "loan": {
            "subject": pl["subject"],
            "product": pl["product"],
            "method": "한도거래" if limit else "개별거래",
            "account_no": pl["loan_account"],
            "rate_type": pl["rate_type"],
            "rate_reset": reset,
            "repayment": pl["repayment"],
            "installment": "해당없음" if pl["repayment"] == "만기일시상환" else f"{pl['term_years'] * 12}회 (매월)",
            **terms,
        },
        "stamp_tax": _stamp_tax(pl["amount"]),
        "explained": "예",
        "handwritten": rng.choice(["설명을 듣고 이해함", "충분히 설명듣고 이해함", "설명들었음"]),
        "contract_date": D(pl["contract_date"], rng.choice(["kor", "kor_short"])),
        "signature": per.name,
    }
    fmt = {"p1": rng.choice([0.1, 0.2, 0.3]), "p2": rng.choice([0.5, 0.7, 1.0]), "m": rng.choice([1, 3, 6]),
           "purpose": pl["purpose"], "lender": rng.choice(_lenders(p)[:5]),
           "reset": reset if pl["rate_type"] == "변동금리" else "6개월"}
    pool = [t for t in _TERMS_PERSONAL if ("{lender}" not in t or "대환" in pl["purpose"])
            and (pl["kind"] == "mortgage" or not any(w in t for w in ("담보", "전입")))]
    _agreement_variants(p, rng, data, pool, fmt, personal=True)
    return data
