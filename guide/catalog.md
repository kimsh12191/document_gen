# 업무별 서류·대조 사례·심사 규칙

이 문서는 `python -m studio.guidebook`으로 현재 등록부·필드 스키마·시나리오 설정에서 생성합니다. 직접 수정하지 않습니다.

Studio의 **사용 가이드 → 서류·추출 카탈로그**와 서식 상세의 **개요 › 업무·시나리오** 화면은 같은 구조의 현재 데이터를 보여 줍니다. 이 파일과 catalog.json은 갱신 시점의 스냅샷입니다.

단일 서류 KIE는 해당 서식의 필드를 사용합니다. 업무 시나리오의 명시적 추출·비교 작업은 별도 설정입니다. 작업이 없더라도 켜진 기본 구비·대조·심사 과제는 유효한 서류·규칙에 따라 생성됩니다.

## 업무별 서류와 처리 설정

### account_opening · 개인 계좌개설

필수 역할/기준 서식: resident_id_card, employment_certificate, account_opening_application, financial_transaction_purpose, customer_due_diligence, privacy_consent, fatca_crs

처리·추출·비교 및 후보 서식 설정 (현재 설정):

```json
{
  "sampling": {},
  "processing": {
    "doc_check": true,
    "cross_check": true,
    "review": true,
    "case_ids": null,
    "rule_ids": null,
    "operations": []
  }
}
```

### personal_credit_loan · 개인 신용대출

필수 역할/기준 서식: resident_id_card, employment_certificate, income_certificate, withholding_receipt, health_insurance_qualification, pay_stub, loan_application, credit_agreement, privacy_consent

처리·추출·비교 및 후보 서식 설정 (현재 설정):

```json
{
  "sampling": {},
  "processing": {
    "doc_check": true,
    "cross_check": true,
    "review": true,
    "case_ids": null,
    "rule_ids": null,
    "operations": []
  }
}
```

### mortgage · 주택담보대출

필수 역할/기준 서식: resident_id_card, resident_registration_copy, family_relation_certificate, seal_certificate, income_certificate, real_estate_registry, building_register, sales_contract, loan_application, credit_agreement, collateral_agreement, privacy_consent

처리·추출·비교 및 후보 서식 설정 (현재 설정):

```json
{
  "sampling": {},
  "processing": {
    "doc_check": true,
    "cross_check": true,
    "review": true,
    "case_ids": null,
    "rule_ids": null,
    "operations": []
  }
}
```

### jeonse_loan · 전세자금대출

필수 역할/기준 서식: resident_id_card, resident_registration_copy, lease_contract, real_estate_registry, employment_certificate, income_certificate, loan_application, privacy_consent

처리·추출·비교 및 후보 서식 설정 (현재 설정):

```json
{
  "sampling": {},
  "processing": {
    "doc_check": true,
    "cross_check": true,
    "review": true,
    "case_ids": null,
    "rule_ids": null,
    "operations": []
  }
}
```

### sole_proprietor_loan · 개인사업자 대출

필수 역할/기준 서식: resident_id_card, business_registration_certificate, business_registration_proof, vat_tax_base_certificate, income_certificate, tax_payment_certificate, local_tax_payment_certificate, loan_application, credit_agreement, privacy_consent

처리·추출·비교 및 후보 서식 설정 (현재 설정):

```json
{
  "sampling": {},
  "processing": {
    "doc_check": true,
    "cross_check": true,
    "review": true,
    "case_ids": null,
    "rule_ids": null,
    "operations": []
  }
}
```

### corporate_credit · 법인 여신

필수 역할/기준 서식: corporate_registry, articles_of_incorporation, shareholder_registry, financial_statements, corporate_seal_certificate, board_minutes, business_registration_certificate_corp, tax_payment_certificate_corp, corporate_customer_due_diligence, loan_application_corp, credit_agreement_corp, power_of_attorney

처리·추출·비교 및 후보 서식 설정 (현재 설정):

```json
{
  "sampling": {},
  "processing": {
    "doc_check": true,
    "cross_check": true,
    "review": true,
    "case_ids": null,
    "rule_ids": null,
    "operations": []
  }
}
```

### fx_remittance · 해외송금

필수 역할/기준 서식: resident_id_card, overseas_remittance_application, commercial_invoice, trade_contract, bill_of_lading

처리·추출·비교 및 후보 서식 설정 (현재 설정):

```json
{
  "sampling": {},
  "processing": {
    "doc_check": true,
    "cross_check": true,
    "review": true,
    "case_ids": null,
    "rule_ids": null,
    "operations": []
  }
}
```

### study_abroad_remittance · 유학생 송금

필수 역할/기준 서식: passport, admission_letter, tuition_invoice, family_relation_certificate, overseas_remittance_application

처리·추출·비교 및 후보 서식 설정 (현재 설정):

```json
{
  "sampling": {},
  "processing": {
    "doc_check": true,
    "cross_check": true,
    "review": true,
    "case_ids": null,
    "rule_ids": null,
    "operations": []
  }
}
```

### irp_opening · 개인형IRP 개설

필수 역할/기준 서식: resident_id_card, employment_certificate, hf171, hf173, hf168, privacy_consent

처리·추출·비교 및 후보 서식 설정 (현재 설정):

```json
{
  "sampling": {},
  "processing": {
    "doc_check": true,
    "cross_check": true,
    "review": true,
    "case_ids": null,
    "rule_ids": null,
    "operations": []
  }
}
```

### retirement_payout · 퇴직급여 수령

필수 역할/기준 서식: resident_id_card, employment_certificate, hf176, hf171, hf028

처리·추출·비교 및 후보 서식 설정 (현재 설정):

```json
{
  "sampling": {},
  "processing": {
    "doc_check": true,
    "cross_check": true,
    "review": true,
    "case_ids": null,
    "rule_ids": null,
    "operations": []
  }
}
```

### efinance_signup · 전자금융 가입

필수 역할/기준 서식: resident_id_card, account_opening_application, hf337, hf335, privacy_consent

처리·추출·비교 및 후보 서식 설정 (현재 설정):

```json
{
  "sampling": {},
  "processing": {
    "doc_check": true,
    "cross_check": true,
    "review": true,
    "case_ids": null,
    "rule_ids": null,
    "operations": []
  }
}
```

### inheritance · 상속예금 지급

필수 역할/기준 서식: resident_id_card, family_relation_certificate, basic_certificate, seal_certificate, hf001, hf011

처리·추출·비교 및 후보 서식 설정 (현재 설정):

```json
{
  "sampling": {},
  "processing": {
    "doc_check": true,
    "cross_check": true,
    "review": true,
    "case_ids": null,
    "rule_ids": null,
    "operations": []
  }
}
```

## 기본 대조 사례

| ID | 사례 | 근거 |
|---|---|---|
| typo | 성명·번호·주소 오기 | 신청서·약정서 기재 오류 (성명·주민번호·연락처·주소 한 자리) |
| other_person | 타인 명의 서류 | 명의도용·가족 서류 혼입, 대리 제출 시 타인 서류 |
| loan_vs_agreement | 신청금액 ≠ 약정금액 | 신청서와 약정서 금액 상이 (약정서 작성 오류·변조) |
| income_inflated | 소득 부풀리기 | 작업대출: 원천징수영수증 위·변조로 소득 과다 기재 |
| lease_owner | 임대인 ≠ 등기부 소유자 | 전세사기: 계약서상 임대인이 등기부 소유자가 아님 |
| seller_owner | 매도인 ≠ 등기부 소유자 | 무권리자 매도·허위 매매계약 |
| hire_date | 재직기간 부풀리기 | 작업대출: 재직증명서 입사일 ≠ 건강보험 자격취득일 |
| rep_director | 법인 대표자 불일치 | 대표이사 변경 미반영·권한 없는 자의 신청 |
| contract_before_apply | 약정일 < 신청일 | 서류 작성일 순서 오류 (사후 작성·소급 작성) |
| collateral_short | 채권최고액 < 대출금 | 근저당 설정 금액 부족 |
| jeonse_over | 전세대출 > 보증금 | 허위 임대차계약·보증금 부풀리기 |
| sales_sum | 업계약 (대금 합계 불일치) | 업계약: 대출 한도를 늘리려 매매대금을 부풀림 |
| fx_beneficiary | 송금 수취인 ≠ 송장 수출자 | 증빙과 다른 상대방에게 송금 (외국환 증빙 불일치) |
| format_only | 표기만 다름 (정상) | 날짜·금액·주민번호·전화·주소 표기 차이는 불일치가 아님 |

## 기본 심사 규칙

| ID | 계산·판단 |
|---|---|
| ltv | 대출신청금액 ÷ 매매대금 (LTV) |
| collateral_ratio | 채권최고액 ÷ 약정금액 |
| jeonse_ratio | 전세대출금 ÷ 보증금 |
| income_multiple | 대출금 ÷ 연소득 |
| age | 신청일 기준 만 나이 |
| tenure | 신청일 기준 재직기간 |
| net_pay | 지급액 − 공제액 |
| sales_rest | 매매대금 − 계약금 − 중도금 |
| invoice_sum | 송장 품목 금액 합계 |
| tuition_due | 이전 잔액 + 청구액 − 납부액 |
| debt_ratio | 부채총계 ÷ 자본총계 |
| doc_valid | 신청일 기준 발급 후 90일 이내 |

서류별 추출 항목은 서식마다 카드 `docgen/forms/<ID>/FORM.md` 와 studio 서식 상세의 **개요** 탭에 있습니다 (기계용 catalog.json).
