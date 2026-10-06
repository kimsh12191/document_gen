"""서류 종류 레지스트리.

각 서류는 docgen/docs/*.py 에서 @doc(...) 데코레이터로 등록한다.
생성 함수는 (Profile, random.Random) -> dict 이며, dict 값은 화면에 표시될 문자열이다.
"""
from __future__ import annotations

import importlib
import pkgutil
import random
from dataclasses import dataclass
from typing import Callable

from .entities import Profile

GROUPS = {
    "identity": "신원·신분",
    "family": "가족관계",
    "income": "소득·재직",
    "tax": "세금·보험",
    "finance": "금융거래",
    "real_estate": "부동산",
    "business": "개인사업자",
    "corporate": "법인",
    "fx": "외환·무역",
    "bank_form": "은행 서식",
    "retirement": "퇴직연금",
    "efinance": "전자금융",
}

# 은행이 직접 쓰는 서식 그룹. 이 그룹의 서류는 렌더링할 때
#   - 서식을 낸 은행(옛 은행 포함)에 맞춰 프로필·표기를 바꾸고 (banks.bank_view)
#   - 템플릿에 서식 문맥 bk 를 넘긴다 (banks.form_context)
BANK_FORM_GROUPS = {"bank_form", "retirement", "efinance"}

# 업무(시나리오)별 제출 서류 묶음 — 같은 고객 프로필로 생성된다.
SCENARIOS = {
    "account_opening": ("개인 계좌개설", ["resident_id_card", "employment_certificate", "account_opening_application",
                                     "financial_transaction_purpose", "customer_due_diligence", "privacy_consent", "fatca_crs"]),
    "personal_credit_loan": ("개인 신용대출", ["resident_id_card", "employment_certificate", "income_certificate",
                                          "withholding_receipt", "health_insurance_qualification", "pay_stub",
                                          "loan_application", "credit_agreement", "privacy_consent"]),
    "mortgage": ("주택담보대출", ["resident_id_card", "resident_registration_copy", "family_relation_certificate",
                             "seal_certificate", "income_certificate", "real_estate_registry", "building_register",
                             "sales_contract", "loan_application", "credit_agreement", "collateral_agreement", "privacy_consent"]),
    "jeonse_loan": ("전세자금대출", ["resident_id_card", "resident_registration_copy", "lease_contract", "real_estate_registry",
                               "employment_certificate", "income_certificate", "loan_application", "privacy_consent"]),
    "sole_proprietor_loan": ("개인사업자 대출", ["resident_id_card", "business_registration_certificate", "business_registration_proof",
                                           "vat_tax_base_certificate", "income_certificate", "tax_payment_certificate",
                                           "local_tax_payment_certificate", "loan_application", "credit_agreement", "privacy_consent"]),
    "corporate_credit": ("법인 여신", ["corporate_registry", "articles_of_incorporation", "shareholder_registry",
                                   "financial_statements", "corporate_seal_certificate", "board_minutes",
                                   "business_registration_certificate_corp", "tax_payment_certificate_corp",
                                   "corporate_customer_due_diligence", "loan_application_corp", "credit_agreement_corp",
                                   "power_of_attorney"]),
    "fx_remittance": ("해외송금", ["resident_id_card", "overseas_remittance_application", "commercial_invoice",
                               "trade_contract", "bill_of_lading"]),
    "study_abroad_remittance": ("유학생 송금", ["passport", "admission_letter", "tuition_invoice",
                                           "family_relation_certificate", "overseas_remittance_application"]),
    "irp_opening": ("개인형IRP 개설", ["resident_id_card", "employment_certificate",
                                   "irp_account_application", "investor_profile_retirement",
                                   "default_option_designation", "privacy_consent"]),
    "retirement_payout": ("퇴직급여 수령", ["resident_id_card", "employment_certificate",
                                       "retirement_benefit_claim", "irp_account_application",
                                       "bank_power_of_attorney"]),
    "efinance_signup": ("전자금융 가입", ["resident_id_card", "account_opening_application",
                                     "efinance_application_personal", "sms_notice_application",
                                     "privacy_consent"]),
    "inheritance": ("상속예금 지급", ["resident_id_card", "family_relation_certificate",
                                 "basic_certificate", "seal_certificate",
                                 "inheritance_deposit_claim", "balance_certificate_request"]),
}

# 시나리오별로 프로필에 주입하는 값 (Profile.extra). 서류 생성 함수가 참고한다.
SCENARIO_EXTRA = {
    "personal_credit_loan": {"loan_kind": "credit"},
    "mortgage": {"loan_kind": "mortgage"},
    "jeonse_loan": {"loan_kind": "jeonse"},
}


@dataclass
class DocSpec:
    id: str
    name: str
    group: str
    category: str  # "external"(외부 발급) / "internal"(은행 자체 서식)
    template: str
    generate: Callable[[Profile, random.Random], dict]
    page: str = "a4"  # "a4" | "a4_landscape" | "card" | "passport"
    sample_mark: bool = False  # 신분증 등: '견본' 표시 강제
    description: str = ""


REGISTRY: dict[str, DocSpec] = {}


def doc(id: str, name: str, group: str, category: str = "external", page: str = "a4",
        template: str | None = None, sample_mark: bool = False, description: str = ""):
    assert group in GROUPS, group

    def deco(fn):
        if id in REGISTRY:
            raise ValueError(f"duplicate doc id: {id}")
        REGISTRY[id] = DocSpec(id, name, group, category, template or f"{group}/{id}.html.j2", fn,
                               page, sample_mark, description or (fn.__doc__ or "").strip())
        return fn

    return deco


def load_all() -> dict[str, DocSpec]:
    from . import docs

    for m in pkgutil.iter_modules(docs.__path__):
        importlib.import_module(f"{docs.__name__}.{m.name}")
    return REGISTRY
