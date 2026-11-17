"""financial_transaction_purpose: 이 서식의 값 만들기 (코드 서식). @doc 이 서식을 등록하고, 함수가 고객(p)·난수(rng)로 칸 값을 만든다.

템플릿 look/template.html.j2 의 {{ f("키", …) }} 자리에 이 함수가 돌려준 값이 들어간다 (d.키).
같은 그룹 서식들이 같이 쓰는 도우미는 docgen/docs/bank_form_account.py, 모든 서식 공통 도우미는 docgen/docs/_common.py.
"""
from docgen.docs._common import *  # noqa: F401,F403  (모든 서식 공통 도우미: D 날짜, won 금액, special, K …)
from docgen.docs.bank_form_account import _bank, _date, _occupation, _rrn, _staff  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.docs.bank_form_loan import _foreigner, _solo  # noqa: F401  (같은 그룹 서식들이 같이 쓰는 것)
from docgen.registry import doc


@doc("financial_transaction_purpose", "금융거래목적확인서", "bank_form", category="internal")
def financial_transaction_purpose(p: Profile, rng: random.Random) -> dict:
    """입출금계좌 신규 시 금융거래 목적과 증빙서류를 확인하는 서식 (대포통장 예방)."""
    per = p.person
    job = _occupation(p, rng)
    if job["type"] in ("급여소득자", "전문직"):
        purpose = rng.choice(["급여계좌"] * 5 + ["공과금 이체", "모임 회비"])
    elif job["type"] == "개인사업자":
        purpose = rng.choice(["사업자 거래"] * 3 + ["공과금 이체"])
    elif job["type"] == "학생":
        purpose = "아르바이트"
    else:
        purpose = rng.choice(["공과금 이체", "모임 회비", "기타"])
    data = {
        "bank": _bank(p),
        "customer": {
            "name": per.name, "rrn": _rrn(p, rng), "address": per.address.road_full,
            "mobile": per.mobile, "job": job["type"],
        },
        "account_type": rng.choice(["보통예금", "보통예금", "저축예금"]),
        "purpose": purpose,
    }
    if "company" in job:
        data["customer"]["company"] = job["company"]
    if purpose == "기타":
        data["purpose_detail"] = rng.choice(["생활비 관리", "연금 수령", "자녀 용돈 관리"])
    data["evidence"] = {
        "급여계좌": lambda: rng.choice(["재직증명서", "근로소득원천징수영수증", "급여명세서", "건강보험 자격득실확인서"]),
        "사업자 거래": lambda: rng.choice(["사업자등록증명", "부가가치세 과세표준증명", "전자세금계산서(공급자용)"]),
        "공과금 이체": lambda: rng.choice(["공과금 납입영수증", "아파트 관리비 고지서"]),
        "모임 회비": lambda: "모임 회칙 및 구성원 명부",
        "아르바이트": lambda: "근로계약서, 고용주 사업자등록증 사본",
    }.get(purpose, lambda: "연금 수급증명서" if data.get("purpose_detail") == "연금 수령" else "가족관계증명서")()
    data["questions"] = {
        "q1": "아니오",
        "q2": "아니오",
        "q3": rng.choices(["아니오", "예"], weights=[80, 20])[0],
    }
    data["date"] = _date(p, rng)
    data["signature"] = per.name
    data["bank_use"] = {
        "result": rng.choices(["일반계좌 개설", "금융거래한도계좌 개설"], weights=[88, 12])[0],
        **_staff(rng),
    }
    if _solo(p) and special(rng, "foreigner", 0.08):  # 외국인 근로자 급여계좌
        fo = _foreigner(p, rng, (22, 45))
        data["customer"].update({"name": fo["name"], "rrn": fo["arc_no"], "mobile": fo["mobile"],
                                 "nationality": fo["nationality"]})
        data["signature"] = fo["name"]
    if special(rng, "no_evidence", 0.1):  # 증빙서류 미제출 → 금융거래한도계좌
        data["evidence"] = None
        data["bank_use"]["result"] = "금융거래한도계좌 개설"
    if special(rng, "no_check", 0.1):  # 확인사항 체크 누락
        data["questions"][rng.choice(["q1", "q2", "q3"])] = None
    return data
