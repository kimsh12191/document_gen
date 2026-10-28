"""credit_agreement_corp: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/bank_form_loan.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.bank_form_loan import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _agreement_terms,
    _agreement_variants,
    _legal_bank,
    _plan_corp,
    _stamp_tax,
)
from docgen.registry import doc


_TERMS_CORP = [
    "채무자는 매 회계연도 종료 후 90일 이내에 외부감사인의 감사를 받은 재무제표를 은행에 제출한다.",
    "채무자는 여신기간 중 부채비율을 {debt}% 이하로 유지하며, 이를 초과한 경우 은행은 가산금리 연 {p1:.1f}%p를 추가 적용할 수 있다.",
    "채무자는 은행의 사전 서면 동의 없이 다른 금융기관으로부터 담보부 차입을 하거나 제3자를 위한 담보를 제공하지 아니한다.",
    "채무자의 대표이사 변경, 최대주주 변경, 합병·분할 또는 영업양도가 있는 경우 지체 없이 은행에 통지한다.",
    "이 여신은 {purpose} 용도로만 사용하며, 은행이 요구하는 경우 자금사용 증빙(세금계산서, 계약서 등)을 제출한다.",
    "채무자는 여신기간 중 당행 결제성 계좌의 월평균 입금액이 {amt}백만원 이상 유지되도록 노력하며, 미달 시 우대금리를 적용하지 아니한다.",
    "보증기관의 보증서 기한이 연장되지 아니하거나 보증이 해지된 경우 은행은 기한의 이익을 상실시킬 수 있다.",
    "채무자는 매 반기 종료 후 60일 이내에 부가가치세 과세표준증명 및 국세·지방세 완납증명서를 제출한다.",
    "채무자가 담보물건을 임대하는 경우 사전에 은행의 동의를 받아야 하며, 임대차계약서 사본을 은행에 제출한다.",
    "이자보상배율이 2기 연속 1 미만인 경우 은행은 추가 담보 제공 또는 여신 일부 상환을 요구할 수 있다.",
    "한도여신의 미사용 한도에 대하여는 연 {p3:.1f}%의 한도약정수수료를 매 분기 말 후취한다.",
]


@doc("credit_agreement_corp", "여신거래약정서(기업용)", "bank_form", category="internal")
def credit_agreement_corp(p: Profile, rng: random.Random) -> dict:
    """기업 여신거래약정서 첫 페이지."""
    c = p.corporation
    pl = _plan_corp(p)
    df = rng.choice(["dot", "kor_short", "dash"])
    terms = _agreement_terms({**pl, "debit_bank": p.bank, "debit_number": pl["debit_account"]}, rng, df)
    terms["interest_pay"] = f"매월 {pl['pay_day']}일" if pl["pay_day"] != 30 else "매월 말일"
    data = {
        "bank": p.bank,
        "creditor": _legal_bank(p.bank),
        "branch": p.bank_branch,
        "debtor": {
            "name": c.name,
            "biz_no": c.biz_no,
            "corp_no": c.corp_no,
            "ceo": c.ceo.name,
            "address": c.address.road_full,
            "phone": c.phone,
        },
        "loan": {
            "subject": pl["kind"],
            "product": pl["product"],
            "method": "한도거래" if pl["kind"] == "한도대출" else "개별거래",
            "account_no": pl["loan_account"],
            "rate_type": pl["rate_type"],
            "rate_reset": "해당없음" if pl["rate_type"] == "고정금리" else rng.choice(["3개월", "6개월"]),
            "repayment": pl["repayment"],
            "purpose": pl["purpose"],
            **terms,
        },
        "stamp_tax": _stamp_tax(pl["amount"]),
        "explained": "예",
        "contract_date": D(pl["contract_date"], rng.choice(["kor", "kor_short"])),
        "signature": c.ceo.name,
    }
    fmt = {"p1": rng.choice([0.2, 0.3, 0.5]), "p3": rng.choice([0.2, 0.3, 0.5]), "debt": rng.choice([200, 250, 300, 400]),
           "purpose": pl["purpose"], "amt": max(10, K.round_to(c.revenue / 12 / 1_000_000 * rng.uniform(0.1, 0.3), 10))}
    pool = [t for t in _TERMS_CORP if ("한도약정" not in t or pl["kind"] == "한도대출")
            and ("보증기관" not in t or pl["collateral"] == "보증서")
            and ("담보물건" not in t or pl["collateral"] == "부동산")]
    _agreement_variants(p, rng, data, pool, fmt, personal=False)
    return data
