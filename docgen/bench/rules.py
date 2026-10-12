"""review 과제: 은행 심사 담당자가 서류 묶음을 보고 답해야 하는 질문.

각 규칙은 묶음의 정답(GT)에서 답을 계산한다. 필요한 서류·항목이 없으면 문항을 만들지 않는다.
질문에는 판단 기준(반올림 자릿수, 날짜 기준 등)을 적어 답이 하나로 정해지게 한다.

규칙 함수: (B, rng) -> dict | None
  B = Bundle (서류ID → 라벨 필드)
  반환 {"question", "answer", "answer_type": "number"|"yesno", "tol", "docs": [서류ID], "skill"}
"""
from __future__ import annotations

import random
from datetime import date

APP_DATES = [("loan_application", "apply_date"), ("loan_application_corp", "apply_date"),
             ("account_opening_application", "date"), ("overseas_remittance_application", "date")]


class Bundle:
    def __init__(self, scenario: str, docs: dict[str, dict]):
        """docs: 서류ID → {"name", "fields"}"""
        self.scenario = scenario
        self.docs = docs
        self.idx = {d: {f["key"]: f for f in v["fields"]} for d, v in docs.items()}

    def name(self, doc: str) -> str:
        return self.docs[doc]["name"]

    def f(self, doc: str, key: str) -> dict | None:
        return self.idx.get(doc, {}).get(key)

    def num(self, doc: str, key: str) -> float | None:
        f = self.f(doc, key)
        n = f and f.get("norm")
        return float(n) if isinstance(n, (int, float)) and not isinstance(n, bool) else None

    def date(self, doc: str, key: str) -> date | None:
        f = self.f(doc, key)
        if not f or f.get("type") != "date":
            return None
        try:
            return date.fromisoformat(f["norm"])
        except (TypeError, ValueError):
            return None

    def app_date(self) -> tuple[str, str, date] | None:
        """업무 신청일: 신청서의 신청일, 없으면 하나은행 원본 서식의 작성일."""
        for d, k in APP_DATES:
            if (v := self.date(d, k)) is not None:
                return d, (self.f(d, k).get("label") or "신청일"), v
        for d in self.docs:
            if d.startswith("hf") and (v := self.date(d, "date")) is not None:
                return d, (self.f(d, "date").get("label") or "작성일"), v
        return None


def _age(birth: date, on: date) -> int:
    return on.year - birth.year - ((on.month, on.day) < (birth.month, birth.day))


def _birth_from_rrn(rrn: str) -> date | None:
    digits = rrn.replace("-", "")
    if len(digits) < 7 or not digits[:7].isdigit():
        return None
    century = {"1": 1900, "2": 1900, "5": 1900, "6": 1900, "3": 2000, "4": 2000, "7": 2000, "8": 2000,
               "9": 1800, "0": 1800}[digits[6]]
    try:
        return date(century + int(digits[:2]), int(digits[2:4]), int(digits[4:6]))
    except ValueError:
        return None


def _pct(a: float, b: float) -> float:
    return round(a / b * 100, 1)


# ---------------------------------------------------------------------------
# 규칙
# ---------------------------------------------------------------------------

def r_ltv(B: Bundle, rng):
    loan, price = B.num("loan_application", "loan.amount"), B.num("sales_contract", "payment.price")
    if not loan or not price:
        return None
    return {"question": f"주택담보대출 심사입니다. '{B.name('loan_application')}'의 대출신청금액은 '{B.name('sales_contract')}'의 "
                        "매매대금의 몇 %입니까? (LTV, 소수 첫째 자리까지 반올림한 숫자만 답하세요)",
            "answer": _pct(loan, price), "answer_type": "number", "tol": 0.1,
            "docs": ["loan_application", "sales_contract"], "skill": "계산(비율)"}


def r_collateral_ratio(B: Bundle, rng):
    mx, loan = B.num("collateral_agreement", "max_amount"), B.num("credit_agreement", "loan.amount")
    if not mx or not loan:
        return None
    return {"question": f"'{B.name('collateral_agreement')}'의 채권최고액은 '{B.name('credit_agreement')}'의 대출(한도)금액의 "
                        "몇 %입니까? (소수 첫째 자리까지 반올림한 숫자만 답하세요)",
            "answer": _pct(mx, loan), "answer_type": "number", "tol": 0.1,
            "docs": ["collateral_agreement", "credit_agreement"], "skill": "계산(비율)"}


def r_jeonse_ratio(B: Bundle, rng):
    loan, dep = B.num("loan_application", "loan.amount"), B.num("lease_contract", "deposit")
    if not loan or not dep:
        return None
    return {"question": f"전세자금대출 심사입니다. '{B.name('loan_application')}'의 대출신청금액은 '{B.name('lease_contract')}'의 "
                        "보증금의 몇 %입니까? (소수 첫째 자리까지 반올림한 숫자만 답하세요)",
            "answer": _pct(loan, dep), "answer_type": "number", "tol": 0.1,
            "docs": ["loan_application", "lease_contract"], "skill": "계산(비율)"}


def r_income_multiple(B: Bundle, rng):
    loan, inc = B.num("loan_application", "loan.amount"), B.num("withholding_receipt", "work.total")
    if not loan or not inc:
        return None
    return {"question": f"'{B.name('loan_application')}'의 대출신청금액은 '{B.name('withholding_receipt')}'의 "
                        "주(현)근무지 급여 합계(계)의 몇 배입니까? (소수 둘째 자리까지 반올림한 숫자만 답하세요)",
            "answer": round(loan / inc, 2), "answer_type": "number", "tol": 0.01,
            "docs": ["loan_application", "withholding_receipt"], "skill": "계산(비율)"}


def r_age(B: Bundle, rng):
    f = B.f("resident_id_card", "rrn")
    app = B.app_date()
    if not f or not app or not f.get("value"):
        return None
    birth = _birth_from_rrn(f["value"])
    if not birth:
        return None
    doc, label, on = app
    return {"question": f"'{B.name('resident_id_card')}'의 주민등록번호로 보아, '{B.name(doc)}'의 {label} 당일 고객의 "
                        "만 나이는 몇 세입니까? (숫자만 답하세요)",
            "answer": _age(birth, on), "answer_type": "number", "tol": 0,
            "docs": ["resident_id_card", doc], "skill": "날짜 계산"}


def r_tenure(B: Bundle, rng):
    hire, app = B.date("loan_application", "workplace.hire_date"), B.date("loan_application", "apply_date")
    if not hire or not app:
        return None
    return {"question": f"'{B.name('loan_application')}'에 적힌 입사일과 신청일로 보아, 신청일 현재 재직기간은 "
                        "만 몇 년입니까? (만 1년 미만은 버리고 숫자만 답하세요)",
            "answer": _age(hire, app), "answer_type": "number", "tol": 0,
            "docs": ["loan_application"], "skill": "날짜 계산"}


def valid_candidates(B: Bundle) -> list[str]:
    """유효기간을 따지는 서류 (발급일이 있는 외부 발급 서류, 신분증 제외)."""
    return sorted(d for d in B.docs if d not in ("resident_id_card", "passport") and B.date(d, "issue_date"))


def r_doc_valid(B: Bundle, rng, doc: str | None = None):
    """제출 서류 유효기간 (발급 후 90일 이내). 묶음 서류는 대개 신청일 무렵 발급이라
    build 에서 절반은 발급일을 90일 넘게 앞당긴 사본을 만들어 doc 으로 넘긴다."""
    app = B.app_date()
    if not app:
        return None
    cands = valid_candidates(B)
    if not cands:
        return None
    d = doc or rng.choice(cands)
    days = (app[2] - B.date(d, "issue_date")).days
    return {"question": f"은행은 제출 서류가 업무 신청일 기준 발급 후 90일 이내여야 받습니다. '{B.name(d)}'의 발급일부터 "
                        f"'{B.name(app[0])}'의 {app[1]}까지 90일 이내입니까? ('예' 또는 '아니오'로만 답하세요)",
            "answer": "예" if 0 <= days <= 90 else "아니오", "answer_type": "yesno", "tol": 0,
            "docs": [d, app[0]], "skill": "날짜 계산", "info": {"days": days}}


def r_net_pay(B: Bundle, rng):
    a, b = B.num("pay_stub", "pay_total"), B.num("pay_stub", "deduction_total")
    if a is None or b is None:
        return None
    return {"question": f"'{B.name('pay_stub')}'의 지급액계에서 공제액계를 빼면 얼마입니까? (원 단위 숫자만 답하세요)",
            "answer": round(a - b), "answer_type": "number", "tol": 0,
            "docs": ["pay_stub"], "skill": "계산(합계)"}


def r_sales_rest(B: Bundle, rng):
    price, down = B.num("sales_contract", "payment.price"), B.num("sales_contract", "payment.down")
    mid = B.num("sales_contract", "payment.middle") or 0
    if not price or down is None:
        return None
    return {"question": f"'{B.name('sales_contract')}'의 매매대금에서 계약금과 중도금(없으면 0)을 빼면 얼마입니까? "
                        "(원 단위 숫자만 답하세요)",
            "answer": round(price - down - mid), "answer_type": "number", "tol": 0,
            "docs": ["sales_contract"], "skill": "계산(합계)"}


def r_invoice_sum(B: Bundle, rng):
    idx = B.idx.get("commercial_invoice", {})
    amts = [f["norm"] for k, f in idx.items() if k.startswith("items.") and k.endswith(".amount")
            and isinstance(f.get("norm"), (int, float))]
    if len(amts) < 2:
        return None
    return {"question": f"'{B.name('commercial_invoice')}'의 품목별 금액(Amount)을 모두 더하면 얼마입니까? "
                        "(통화 기호 없이 숫자만 답하세요)",
            "answer": round(sum(amts), 2), "answer_type": "number", "tol": 0.01,
            "docs": ["commercial_invoice"], "skill": "표 계산"}


def r_tuition_due(B: Bundle, rng):
    prev, ch, cr = (B.num("tuition_invoice", f"summary.{k}") for k in ("previous_balance", "charges", "credits"))
    if None in (prev, ch, cr):
        return None
    return {"question": f"'{B.name('tuition_invoice')}'에서 Previous Balance + New Charges - Payments/Credits 는 "
                        "얼마입니까? (통화 기호 없이 숫자만 답하세요)",
            "answer": round(prev + ch - cr, 2), "answer_type": "number", "tol": 0.01,
            "docs": ["tuition_invoice"], "skill": "계산(합계)"}


def r_debt_ratio(B: Bundle, rng):
    idx = B.idx.get("financial_statements", {})

    def total(prefix, name):
        for k, f in idx.items():
            if k.startswith(prefix) and k.endswith(".account") and (f.get("value") or "").replace(" ", "") == name:
                v = idx.get(k[: -len("account")] + "current")
                if v and isinstance(v.get("norm"), (int, float)):
                    return float(v["norm"])
        return None

    debt, eq = total("liabilities.", "부채총계"), total("equity.", "자본총계")
    if not debt or not eq or eq <= 0:
        return None
    return {"question": f"'{B.name('financial_statements')}'의 당기 기준 부채비율(부채총계 ÷ 자본총계 × 100)은 몇 %입니까? "
                        "(소수 첫째 자리까지 반올림한 숫자만 답하세요)",
            "answer": _pct(debt, eq), "answer_type": "number", "tol": 0.1,
            "docs": ["financial_statements"], "skill": "표 계산"}


# doc_valid 는 서류 사본을 다시 렌더링해야 해서 build.Builder.doc_valid 가 따로 만든다
RULES = {
    "ltv": r_ltv,
    "collateral_ratio": r_collateral_ratio,
    "jeonse_ratio": r_jeonse_ratio,
    "income_multiple": r_income_multiple,
    "age": r_age,
    "tenure": r_tenure,
    "net_pay": r_net_pay,
    "sales_rest": r_sales_rest,
    "invoice_sum": r_invoice_sum,
    "tuition_due": r_tuition_due,
    "debt_ratio": r_debt_ratio,
}


def questions(B: Bundle, rng: random.Random) -> list[dict]:
    out = []
    for rid, fn in RULES.items():
        q = fn(B, rng)
        if q:
            q["rule"] = rid
            out.append(q)
    return out
