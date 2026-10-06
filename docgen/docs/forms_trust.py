"""하나은행 공개 서식 — 선언형 스펙 (2종).

scripts/build_form_specs.py 가 add_template/field_specs/ 에서 생성한다.
직접 고치지 말고 생성 스크립트의 라벨 표를 고칠 것.
서식 하나를 수제 템플릿으로 승격할 때는 여기서 해당 FORM 을 지운다.
"""
from ..formspec import FORM  # noqa: F401

FORM("hf197", "위임장(집합투자증권 및 연금저축계좌 투자용)", "finance", code="3-14-0231",
     title_note="하나은행 공개 서식 No.197 (펀드)",
     sections=[("대리인 정보", [
        ("customer.name", "성 명", "text"),
        ("agent.relation", "본인과의 관계", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.phone", "연 락 처", "text"),
        ("customer.address", "주 소", "text"),
        ("item", "인감 및 실명확인 (인)서명", "text")
     ])])

FORM("hf198", "공모부동산집합투자증권 과세특례신청서", "finance", code="5-19-0014",
     title_note="하나은행 공개 서식 No.198 (펀드)",
     sections=[("선취수수료 차감후 투자금액을 투자한도금액 산정시 반", [
        ("customer.name", "성명", "text"),
        ("customer.birth", "생년월일", "date"),
        ("customer.address", "주소", "text"),
        ("customer.phone", "연락처", "text"),
        ("item", "신청 내용", "text"),
        ("amount", "금액", "amount"),
        ("date", "신청일자", "date")
     ])])
