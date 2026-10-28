"""customer_due_diligence: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/bank_form_account.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.bank_form_account import (  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
    CDD_PURPOSES,
    _bank,
    _date,
    _id_type,
    _occupation,
    _rrn,
    _staff,
)
from docgen.docs.bank_form_loan import _foreigner, _relative, _solo  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("customer_due_diligence", "고객확인서(개인)", "bank_form", category="internal")
def customer_due_diligence(p: Profile, rng: random.Random) -> dict:
    """특정금융정보법 제5조의2에 따른 개인 고객확인(CDD) — 은행 '고객거래확인서(개인·개인사업자용)'."""
    per = p.person
    job = _occupation(p, rng)
    if job["type"] == "주부" and per.gender == "M":
        job = {"type": "무직"}
    if per.age >= 62 and job["type"] in ("무직", "기타") and rng.random() < 0.6:
        job = {"type": "연금소득자"}
    work = {"type": job["type"]}
    if job["type"] in ("급여소득자", "전문직"):
        emp = p.employment
        work.update({"company": emp.company.name, "department": f"{emp.department} / {emp.position}",
                     "industry": emp.company.biz_type, "work_phone": emp.company.phone})
    elif job["type"] == "개인사업자":
        b = p.business
        work.update({"company": b.name, "biz_no": b.biz_no, "opened": D(b.established, "dot"),
                     "industry": f"{b.biz_type} / {b.biz_item}", "work_phone": b.phone})
    fund = {"급여소득자": "근로 및 연금소득", "전문직": "근로 및 연금소득", "연금소득자": "근로 및 연금소득",
            "개인사업자": "사업소득"}.get(job["type"]) or rng.choice(
        ["부동산임대소득", "금융소득(이자 및 배당)", "상속·증여", "기타"])
    if job["type"] == "개인사업자":
        purpose = rng.choice(["사업상 거래", "사업상 거래", "급여 및 생활비", "대출원리금 상환결제"])
    else:
        purpose = rng.choices(CDD_PURPOSES[:6], weights=[50, 20, 5, 8, 9, 8])[0]
    data = {
        "bank": _bank(p),
        "customer": {
            "name": per.name,
            "name_en": per.name_en,
            "rrn": _rrn(p, rng),
            "resident_type": "내국인",
            "gender": "남" if per.gender == "M" else "여",
            "nationality": per.nationality,
            "address": per.address.road_full,
            "mobile": per.mobile,
            "email": per.email,
        },
        "job": work,
        "transaction": {
            "purpose": purpose,
            "fund_source": fund,
            "expected_amount": rng.choices(["1천만원 미만", "1천만원~5천만원", "5천만원~1억원", "1억원 이상"],
                                           weights=[50, 32, 12, 6])[0],
            "frequency": rng.choices(["월 5회 미만", "월 5~10회", "월 10~20회", "월 20회 이상"],
                                     weights=[35, 35, 20, 10])[0],
        },
        "beneficial_owner": "예",
        "pep": "아니오",
        "date": _date(p, rng),
        "signature": per.name,
        "bank_use": {
            "risk_grade": rng.choices(["저위험", "중위험", "고위험"], weights=[70, 26, 4])[0],
            "id_type": _id_type(p, rng),
            "branch": p.bank_branch,
            **_staff(rng),
        },
    }
    _cdd_variants(p, rng, data)
    return data


_EDD_ASSETS = ["5억원 미만", "5억원~10억원", "10억원~30억원", "30억원 이상"]


def _cdd_variants(p: Profile, rng: random.Random, data: dict) -> None:
    """고객확인서(개인) 변형: 강화된 고객확인(EDD) 추가정보(여러 쪽), 외국인, 대리인, 실제소유자 별도, 공란, 체크 누락."""
    cu = data["customer"]
    if _solo(p) and special(rng, "foreigner", 0.1):  # 외국인 고객 (외국인등록증으로 실명확인)
        fo = _foreigner(p, rng)
        cu.update({"name": fo["name"], "name_en": fo["name_en"], "rrn": fo["arc_no"], "resident_type": "외국인",
                   "gender": "남" if fo["gender"] == "M" else "여", "nationality": fo["nationality"],
                   "mobile": fo["mobile"], "email": fo["email"]})
        data["signature"] = fo["name_en"] if rng.random() < 0.6 else fo["name"]
        data["bank_use"]["id_type"] = rng.choice(["외국인등록증", "여권"])
    if special(rng, "agent", 0.1):  # 대리인 거래
        ag, rel = _relative(p, rng)
        data["agent"] = {"name": ag.name, "rrn": K.mask_rrn(ag.rrn), "relation": rel}
    if special(rng, "not_owner", 0.06):  # 실제소유자가 따로 있는 경우 (예: 부모 자금 관리)
        ow, _ = _relative(p, rng, ("부", "모", "배우자"))
        data["beneficial_owner"] = "아니오"
        data["owner"] = {"name": ow.name, "birth": D(ow.birth, "dot"), "nationality": ow.nationality}
    if heavy(rng, 0.15):  # 고위험 고객: 강화된 고객확인(EDD) 추가정보 → 2쪽
        data["bank_use"]["risk_grade"] = "고위험"
        sal = p.employment.annual_salary
        accts = []
        for _ in range(rng.randint(3, 7)):
            b = rng.choice(["국민은행", "신한은행", "우리은행", "농협은행", "기업은행", "카카오뱅크", "미래에셋증권", "삼성증권"])
            accts.append({"bank": b, "kind": rng.choice(["보통예금", "정기예금", "증권위탁", "외화예금", "적금"]),
                          "purpose": rng.choice(["급여 수령", "생활비", "투자", "사업 결제", "저축", "임대료 수령"])})
        data["edd"] = {
            "annual_income": f"{sal // 10000:,}만원",
            "assets": rng.choices(_EDD_ASSETS, weights=[40, 30, 20, 10])[0],
            "fund_detail": rng.choice([f"{p.employment.company.name} 근로소득 및 상여금", "부동산 매각대금 (매매계약서 제출)",
                                       "부모로부터 증여받은 자금 (증여세 신고서 제출)", "보유 주식 매도대금",
                                       "임대소득 (임대차계약서 제출)"]),
            "purpose_detail": rng.choice(["해외 부동산 취득 자금 송금", "사업자금 결제 및 거래처 대금 지급",
                                          "자녀 해외 유학자금 관리", "고액 현금 입출금 (매장 매출금)", "주식·가상자산 투자자금 이체"]),
            "cash_tx": rng.choice(["해당 없음", "월 1~2회 (1천만원 이상)", "월 3회 이상 (1천만원 이상)"]),
            "overseas_tx": rng.choice(["해당 없음", "있음 (미국)", "있음 (중국)", "있음 (베트남)", "있음 (싱가포르)"]),
            "accounts": accts,
        }
    if special(rng, "sparse", 0.12):  # 선택 항목 미기재
        for k in rng.sample(["email", "name_en"], rng.randint(1, 2)):
            cu[k] = None
    if special(rng, "no_check", 0.08):  # 체크 누락
        data["transaction"][rng.choice(["frequency", "expected_amount", "fund_source"])] = None
