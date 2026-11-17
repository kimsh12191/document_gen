"""income_tax_return: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/tax.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.business import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    _biz_facts,
    _filed_year,
    _prng,
    _side_person,
    _tax_office,
)
from docgen.docs.tax import _Doc, _itr_calc, _signed  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("income_tax_return", "종합소득세 과세표준확정신고 및 납부계산서", "tax")
def income_tax_return(p: Profile, rng: random.Random) -> dict:
    """종합소득세 확정신고서. 제1쪽(기본사항 + 환급금 계좌 + 세액의 계산)은 항상, 명세(제2·3쪽)는 소득이 여럿이거나
    수정신고·기한후신고·경정청구·공동사업 등일 때 붙는다. 사업소득금액은 표준손익계산서 당기순이익(공동사업이면 지분만큼)과 같다.

    현행 서식은 종합소득세ㆍ농어촌특별세만 적는다 (지방소득세는 별도 신고서).
    paper: 손으로 쓴 서면 신고서(전자신고세액공제 없음) — 템플릿이 손글씨체 + 정정 효과를 쓴다.
    """
    b = p.business
    y = max(_filed_year(p), b.established.year)
    c = _itr_calc(p, y)
    filing = c["filing"]
    w = lambda n: _signed(n)  # noqa: E731
    out = {
        "tax_year": f"{y}",
        "residency": "거주자",
        "nationality": "내국인",
        "taxpayer": {
            "name": p.person.name,
            "rrn": p.person.rrn if c["paper"] or rng.random() < 0.5 else K.mask_rrn(p.person.rrn),
            "address": p.person.address.road_full,
            "email": p.person.email,
            "biz_phone": b.phone,
            "mobile": p.person.mobile,
        },
        "filing_type": c["filing_type"],
        "bookkeeping": c["bookkeeping"],
        "filing_kind": filing["kind"],
        "national": {
            "total_income": w(c["total_income"]), "deduction": w(c["deduction"]), "base": w(c["base"]), "rate": f"{c['rate']}%",
            "computed": w(c["computed"]), "reduction": "0", "credit": w(c["credit"]), "determined": w(c["determined"]),
            "penalty": w(c["penalty"]), "additional": "0", "total": w(c["total"]), "prepaid": w(c["prepaid"]),
            "payable": w(c["payable"]), "special_deduct": "0", "special_add": "0", "installment": w(c["installment"]),
            "due_payable": w(c["payable"] - c["installment"]),
        },
        "filed_date": D(filing["filed"], rng.choice(["kor", "kor_short"])),
        "tax_office": _tax_office(p.person.address),
    }
    out = _Doc(out)
    out.paper = c["paper"]  # 화면 구성 선택 (정답 값 아님)
    if c["payable"] < 0 or rng.random() < 0.5:
        acc = p.accounts[0]
        out["refund_account"] = {"bank": acc.bank, "number": acc.number}
    if c["agent"]:
        ag = _side_person(f"tax-agent:{p.seed}")
        out["tax_agent"] = {"name": ag.name, "biz_no": K.biz_no(_prng(p, "agent-biz")),
                            "phone": K.landline(_prng(p, "agent-tel"), b.address.sido)}
    if c["detail"]:
        fx = _biz_facts(p)
        out["incomes"] = [{"type": i["type"], "payer": i["payer"], "revenue": w(i["revenue"]), "expense": w(i["expense"]),
                           "amount": w(i["amount"]), "withheld": w(i["withheld"])} for i in c["incomes"]]
        bi = c["incomes"][0]
        out["business_income"] = {"address": b.address.road_full, "trade_name": b.name, "biz_no": b.biz_no, "code": c["code"],
                                  "revenue": w(bi["revenue"]), "expense": w(bi["expense"]), "income": w(bi["amount"])}
        if fx["joint"]:
            out["business_income"]["share"] = f"{c['share']}%"
            out["business_income"]["partner"] = fx["joint"]["name"]
        mask = not c["paper"] and rng.random() < 0.6
        out["dependents"] = [{"relation": d["relation"], "name": d["person"].name,
                              "rrn": K.mask_rrn(d["person"].rrn) if mask else d["person"].rrn,
                              "basic": "○", "extra": d["extra"]} for d in c["deps"]]
        out["deduction_items"] = [{"item": n, "amount": w(a)} for n, a in c["ded_items"]]
        out["credit_items"] = [{"item": n, "amount": w(a)} for n, a in c["credits"]]
        if c["penalties"]:
            out["penalty_items"] = [{"item": n, "amount": w(a)} for n, a in c["penalties"]]
        if c["prepaid_items"]:
            out["prepaid_items"] = [{"item": n, "amount": w(a)} for n, a in c["prepaid_items"]]
    return out
