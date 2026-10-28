# 서류별 추출 항목과 시나리오 카탈로그

이 문서는 `python -m studio.guidebook`으로 현재 등록부·필드 스키마·시나리오 설정에서 생성합니다. 직접 수정하지 않습니다.

Studio의 **사용 가이드 → 서류·추출 카탈로그**와 서식 상세의 **추출·시나리오** 탭은 같은 구조의 현재 데이터를 보여 줍니다. 이 파일과 catalog.json은 갱신 시점의 스냅샷입니다.

필드 스키마를 바꿨다면 `python docgen/scripts/build_schema.py` 후 이 문서를 갱신하세요. 필드가 미수집인 서식은 추출 불가가 아니라 목록 갱신이 필요한 상태입니다. 필드별 예시는 가상 값이며 고정 출력값이 아닙니다.

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

## 서류별 목록

### loan_application · 대출거래신청서

그룹: 은행 서식 (`bank_form`)

개인 고객 대출신청서(가계용). 하나은행 「대출신청서(가계용)」, 신한은행 「대출상담및신청서(가계용)」 항목 구성 참고.

연결 업무: 개인 신용대출 (personal_credit_loan), 주택담보대출 (mortgage), 전세자금대출 (jeonse_loan), 개인사업자 대출 (sole_proprietor_loan)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank | bank | 은행명 | text | 기업은행 |
| branch | branch | 취급점 | text | 범어지점 |
| applicant.name | customer.name | 성명 | text | 박찬연 |
| applicant.rrn | customer.rrn | 실명번호 | rrn | 900210-1659382 |
| applicant.zipcode | applicant.zipcode | 우편번호 | number | 06931 |
| applicant.address | customer.address | 자택주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| applicant.mobile | customer.mobile | 휴대전화 | phone | 010-5907-7253 |
| applicant.home_phone | customer.home_phone | 자택전화 | phone | 02-5105-8357 |
| applicant.email | customer.email | E-mail | text | chanyeon363@naver.com |
| applicant.work_phone | applicant.work_phone | 직장전화 | phone | 043-783-2775 |
| housing | housing | 주택소유구분 | checkbox | 월세 |
| dwelling | dwelling | 주거형태 | checkbox | 아파트 |
| workplace.job_type | workplace.job_type | 직업구분 | checkbox | 급여소득자 |
| workplace.name | employer.name | 직장명 | text | 주식회사 태평양무역 |
| workplace.department | employer.department | 근무부서 | text | 구매팀 |
| workplace.position | employer.position | 직위 | text | 대리 |
| workplace.hire_date | employer.hire_date | 입사년월일 | date | 2020-05-08 |
| workplace.annual_income | workplace.annual_income | 연소득(본인) | text | 5,460만원 |
| workplace.address | employer.address | 직장주소 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 |
| debts[].lender | debts[].lender | 금융기관 | text | 국민은행 |
| debts[].kind | debts[].kind | 대출종류 | text | 현금서비스 |
| debts[].balance | debts[].balance | 잔액 | amount | 5,800,000 |
| debts[].maturity | debts[].maturity | 만기일 | date | 2027.03.23 |
| debts[].refinance | debts[].refinance | 상환여부 | text | 유지 |
| assets[].kind | assets[].kind | 종류 | text | 자동차 |
| assets[].location | assets[].location | 소재지 | text | 쏘렌토 (2020년식) |
| assets[].value | assets[].value | 평가금액 | amount | 21,800,000 |
| loan.subject | loan.subject | 대출과목 | text | 주택담보대출 |
| loan.product | loan.product | 상품명 | text | 아파트 담보대출 |
| loan.amount_korean | loan.amount_korean | 대출신청금액(한글) | amount_korean | 일금 이억구천이백만원정 |
| loan.amount | loan.amount | 대출신청금액 | amount | 292,000,000 |
| loan.term | loan.term | 대출기간 | text | 40년 |
| loan.hope_date | loan.hope_date | 대출희망일 | date | 2026-02-16 |
| loan.repayment | loan.repayment | 상환방법 | checkbox | 원리금균등분할 |
| loan.rate_type | loan.rate_type | 금리방식 | checkbox | 변동 |
| loan.interest_day | loan.interest_day | 이자납입일 | text | 매월 15일 |
| loan.purpose_category | loan.purpose_category | 자금용도구분 | checkbox | 주택구입 |
| loan.purpose | loan.purpose | 세부용도 | text | 주택구입자금 |
| collateral | collateral | 담보구분 | checkbox | 부동산 |
| collateral_detail | collateral_detail | 담보내용 | text | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (아파트, 전용 101.84㎡) |
| loan.debit_bank | loan.debit_bank | 이체은행 | text | 기업은행 |
| loan.debit_account | loan.debit_account | 이체계좌번호 | account_no | 171-760452-29-611 |
| loan.debit_holder | loan.debit_holder | 예금주 | text | 박찬연 |
| agent.name | agent.name | 대리인성명 | text | 우나민 |
| agent.rrn | agent.rrn | 대리인실명번호 | rrn | 671023-2****** |
| agent.relation | agent.relation | 본인과의관계 | text | 모 |
| agent.phone | agent.phone | 대리인연락처 | phone | 010-7560-2133 |
| agent.poa | agent.poa | 위임장 | checkbox | 첨부 |
| manual_received | manual_received | 설명서수령확인 | checkbox | 예 |
| consent | consent | 개인(신용)정보동의 | checkbox | 동의함 |
| apply_date | apply_date | 신청일 | date | 2026년 1월 31일 |
| signature | signature | 신청인 | text | 박찬연 |
| seal.applicant | seal.customer | 신청인 | seal | 김소윤 |
| sign.applicant | sign.customer | 신청인 | signature | 박찬연 |
| seal.agent | seal.agent | 대리인 | seal | 우나민 |
| sign.agent | sign.agent | 대리인 | signature | 강형은 |
| co_borrower.name | related.name | 공동차주성명 | text | 설기현 |
| co_borrower.rrn | related.rrn | 공동차주실명번호 | rrn | 851210-1****** |
| co_borrower.relation | co_borrower.relation | 신청인과의관계 | text | 배우자 |
| co_borrower.mobile | co_borrower.mobile | 공동차주휴대전화 | phone | 010-2037-1392 |
| co_borrower.workplace | co_borrower.workplace | 공동차주직장 | text | 자영업 |
| seal.co_borrower | seal.related | 공동차주 | seal | 설기현 |
| sign.co_borrower | sign.related | 공동차주 | signature | 오성원 |

연결 업무 personal_credit_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 mortgage · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 jeonse_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 sole_proprietor_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### loan_application_corp · 기업여신 신청서

그룹: 은행 서식 (`bank_form`)

법인 고객 기업여신 신청서 (은행 자체 서식).

연결 업무: 법인 여신 (corporate_credit)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank | bank | 은행명 | text | 기업은행 |
| branch | branch | 취급점 | text | 범어지점 |
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| company.name_en | corp.name_en | 영문명 | text | Union Trading Co., Ltd. |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| company.established | corp.established | 설립일 | date | 2018.11.01 |
| company.industry | corp.industry | 업태/종목 | text | 도매 및 소매업 / 무역 |
| company.employees | company.employees | 종업원수 | text | 312명 |
| company.size | company.size | 기업규모 | checkbox | 중소기업 |
| company.capital | company.capital | 자본금 | amount | 50,000,000원 |
| company.revenue | company.revenue | 매출액 | amount | 61,800,000,000원 |
| company.revenue_year | company.revenue_year | 결산연도 | text | 2025년 |
| company.address | corp.address | 본점소재지 | text | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| company.phone | corp.phone | 전화번호 | phone | 02-9508-6789 |
| company.fax | company.fax | 팩스번호 | phone | 02-716-6590 |
| contact.name | contact.name | 담당자 | text | 길예태 |
| contact.position | contact.position | 부서/직위 | text | 회계팀 과장 |
| contact.phone | contact.phone | 연락처 | phone | 010-5228-8790 |
| contact.email | contact.email | E-mail | text | biz@union.co.kr |
| loan.subject | loan.subject | 여신과목 | checkbox | 일반자금대출 |
| loan.product | loan.product | 상품명 | text | 중소기업 운전자금대출 |
| loan.rate_type | loan.rate_type | 금리종류 | checkbox | 고정금리 |
| loan.amount_korean | loan.amount_korean | 신청금액(한글) | amount_korean | 일금 삼십억원정 |
| loan.amount | loan.amount | 신청금액 | amount | 3,000,000,000원 |
| loan.term | loan.term | 여신기간 | text | 1년 |
| loan.hope_date | loan.hope_date | 대출희망일 | date | 2026-02-03 |
| loan.repayment | loan.repayment | 상환방법 | text | 만기일시상환 |
| loan.fund_type | loan.fund_type | 자금구분 | checkbox | 운전자금 |
| loan.purpose | loan.purpose | 자금용도 | text | 매출채권 회수 지연에 따른 운전자금 |
| loan.deposit_account | loan.deposit_account | 대출금입금계좌 | account_no | 기업은행 198-866024-83-977 |
| loan.collateral | loan.collateral | 담보구분 | checkbox | 보증서 |
| loan.collateral_detail | loan.collateral_detail | 담보/보증내용 | text | 기술보증기금 보증서 (보증비율 85%) |
| other_loans[].lender | other_loans[].lender | 금융기관 | text | 신한캐피탈 |
| other_loans[].kind | other_loans[].kind | 여신종류 | text | 시설자금대출 |
| other_loans[].balance | other_loans[].balance | 잔액 | amount | 1,140 |
| other_loans[].collateral | other_loans[].collateral | 담보 | text | 부동산 |
| other_loans_total | other_loans_total | 합계 | amount | 9,330 |
| agent.name | agent.name | 대리인성명 | text | 길예태 |
| agent.position | agent.position | 대리인직위 | text | 회계팀 과장 |
| agent.rrn | agent.rrn | 대리인실명번호 | rrn | 841126-1****** |
| agent.phone | agent.phone | 대리인연락처 | phone | 010-5228-8790 |
| apply_date | apply_date | 신청일 | date | 2026년 1월 31일 |
| signature | signature | 대표이사 | text | 박찬연 |
| seal.corp | seal.corp | 법인인감 | seal | 대표이사 |
| seal.agent | seal.agent | 대리인 | seal | 이채재 |
| sign.agent | sign.agent | 대리인 | signature | 길예태 |

연결 업무 corporate_credit · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### credit_agreement · 대출거래약정서(가계용)

그룹: 은행 서식 (`bank_form`)

대출거래약정서(가계용) 첫 장. 은행연합회 표준 구성(제1조 거래조건 ~ 인지세 부담) 기준.

연결 업무: 개인 신용대출 (personal_credit_loan), 주택담보대출 (mortgage), 개인사업자 대출 (sole_proprietor_loan)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank | bank | 은행명 | text | 기업은행 |
| creditor | creditor | 채권자 | text | 중소기업은행 |
| branch | branch | 취급점 | text | 범어지점 |
| debtor.name | customer.name | 성명 | text | 박찬연 |
| debtor.rrn | customer.rrn | 실명번호 | rrn | 900210-1659382 |
| debtor.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| debtor.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| loan.subject | loan.subject | 대출과목 | text | 주택담보대출 |
| loan.product | loan.product | 상품명 | text | 아파트 담보대출 |
| loan.method | loan.method | 거래구분 | checkbox | 개별거래 |
| loan.account_no | loan.account_no | 대출계좌번호 | account_no | 740-757492-44-140 |
| loan.amount_korean | loan.amount_korean | 대출(한도)금액(한글) | amount_korean | 금 이억구천이백만원整 |
| loan.amount | loan.amount | 대출(한도)금액 | amount | 292,000,000원 |
| loan.start_date | loan.start_date | 대출개시일 | date | 2026.02.16 |
| loan.maturity | loan.maturity | 대출기간만료일 | date | 2066.02.16 |
| loan.rate_type | loan.rate_type | 금리종류 | checkbox | 변동금리 |
| loan.base_rate_name | loan.base_rate_name | 기준금리종류 | text | CD 91일물 |
| loan.base_rate | loan.base_rate | 기준금리 | percent | 2.87% |
| loan.spread | loan.spread | 가산금리 | percent | 1.58% |
| loan.pref_rate | loan.pref_rate | 우대금리 | percent | 0.50% |
| loan.applied_rate | loan.applied_rate | 대출이자율 | percent | 연 3.95% |
| loan.rate_reset | loan.rate_reset | 금리변동주기 | text | 3개월 |
| loan.interest_pay | loan.interest_pay | 이자지급시기 | text | 매월 15일 (후취) |
| loan.interest_calc | loan.interest_calc | 이자계산방법 | text | 1년을 365일(윤년 366일)로 보고 1일 단위로 계산 |
| loan.repayment | loan.repayment | 상환방법 | checkbox | 원리금균등분할상환 |
| loan.installment | loan.installment | 분할상환횟수 | text | 480회 (매월) |
| loan.debit_account | loan.debit_account | 자동이체계좌 | account_no | 기업은행 171-760452-29-611 |
| loan.prepay_fee | loan.prepay_fee | 중도상환해약금 | text | 중도상환금액 × 0.74% × 잔존일수 ÷ 대출기간일수 (3년 경과 시 면제) |
| loan.late_rate | loan.late_rate | 지연배상금률 | text | 대출이자율 + 연체가산이자율 연 3% (현재 연 6.95%, 최고 연 15%) |
| stamp_tax | stamp_tax | 인지세 | text | 150,000원 (고객 75,000원 / 은행 75,000원) |
| explained | explained | 설명이해확인 | checkbox | 예 |
| handwritten | handwritten | 자필기재 | text | 설명들었음 |
| contract_date | contract_date | 약정일 | date | 2026년 2월 9일 |
| signature | signature | 채무자 | text | 박찬연 |
| seal.debtor | seal.customer | 채무자 | seal | 박찬연 |
| sign.debtor | sign.customer | 채무자 | signature | 김소윤 |
| co_borrower.name | related.name | 공동차주성명 | text | 김순우 |
| co_borrower.rrn | related.rrn | 공동차주실명번호 | rrn | 810108-2****** |
| co_borrower.address | related.address | 공동차주주소 | text | 경기도 수원시 영통구 중부대로 379, 501호 (매탄동) |
| co_borrower.phone | related.phone | 공동차주연락처 | phone | 010-9897-2197 |
| seal.co_borrower | seal.related | 공동차주 | seal | 천숙승 |
| sign.co_borrower | sign.related | 공동차주 | signature | 김순우 |
| special_terms[] | special_terms[] | 특약사항 | text | 자동이체계좌 잔액 부족으로 이자를 납입하지 못한 경우 은행은 채무자의 당행 다른 예금 계좌에서 출금하여 충당할 수 있다. |

연결 업무 personal_credit_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 mortgage · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 sole_proprietor_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### credit_agreement_corp · 여신거래약정서(기업용)

그룹: 은행 서식 (`bank_form`)

기업 여신거래약정서 첫 페이지.

연결 업무: 법인 여신 (corporate_credit)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank | bank | 은행명 | text | 기업은행 |
| creditor | creditor | 채권자 | text | 중소기업은행 |
| branch | branch | 취급점 | text | 범어지점 |
| debtor.name | customer.name | 상호(법인명) | text | (주)유니온무역 |
| debtor.biz_no | customer.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| debtor.corp_reg_no | customer.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| debtor.ceo | customer.ceo | 대표이사 | text | 박찬연 |
| debtor.phone | customer.phone | 전화번호 | phone | 02-9508-6789 |
| debtor.address | customer.address | 본점소재지 | text | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| loan.subject | loan.subject | 여신과목 | text | 일반자금대출 |
| loan.product | loan.product | 상품명 | text | 중소기업 운전자금대출 |
| loan.method | loan.method | 거래방법 | checkbox | 개별거래 |
| loan.account_no | loan.account_no | 여신계좌번호 | account_no | 203-617585-91-545 |
| loan.amount_korean | loan.amount_korean | 여신(한도)금액(한글) | amount_korean | 금 삼십억원정 |
| loan.amount | loan.amount | 여신(한도)금액 | amount | 3,000,000,000원 |
| loan.start_date | loan.start_date | 여신개시일 | date | 2026년 2월 3일 |
| loan.maturity | loan.maturity | 여신기간만료일 | date | 2027년 2월 3일 |
| loan.purpose | loan.purpose | 자금용도 | text | 매출채권 회수 지연에 따른 운전자금 |
| loan.rate_type | loan.rate_type | 금리종류 | checkbox | 고정금리 |
| loan.base_rate_name | loan.base_rate_name | 기준금리종류 | text | 금융채 1년물(AAA) |
| loan.base_rate | loan.base_rate | 기준금리 | percent | 3.23% |
| loan.spread | loan.spread | 가산금리 | percent | 1.75% |
| loan.pref_rate | loan.pref_rate | 우대금리 | percent | 0.00% |
| loan.applied_rate | loan.applied_rate | 여신이자율 | percent | 연 4.98% |
| loan.rate_reset | loan.rate_reset | 금리변동주기 | text | 해당없음 |
| loan.interest_pay | loan.interest_pay | 이자지급시기 | text | 매월 10일 |
| loan.interest_calc | loan.interest_calc | 이자계산방법 | text | 1년을 365일(윤년 366일)로 보고 1일 단위로 계산 |
| loan.repayment | loan.repayment | 상환방법 | text | 만기일시상환 |
| loan.debit_account | loan.debit_account | 자동이체계좌 | account_no | 기업은행 198-866024-83-977 |
| loan.prepay_fee | loan.prepay_fee | 중도상환해약금 | text | 중도상환금액 × 0.50% × 잔존일수 ÷ 대출기간일수 (3년 경과 시 면제) |
| loan.late_rate | loan.late_rate | 지연배상금률 | text | 대출이자율 + 연체가산이자율 연 3% (현재 연 7.98%, 최고 연 15%) |
| stamp_tax | stamp_tax | 인지세 | text | 350,000원 (고객 175,000원 / 은행 175,000원) |
| explained | explained | 설명이해확인 | checkbox | 예 |
| contract_date | contract_date | 약정일 | date | 2026년 2월 3일 |
| signature | signature | 대표이사 | text | 박찬연 |
| seal.corp | seal.corp | 법인인감 | seal | 대표이사 |
| special_terms[] | special_terms[] | 특약사항 | text | 채무자는 매 반기 종료 후 60일 이내에 부가가치세 과세표준증명 및 국세·지방세 완납증명서를 제출한다. |
| guarantors[].name | guarantors[].name | 연대보증인 | text | 김아진 |
| guarantors[].rrn | guarantors[].rrn | 실명번호 | rrn | 880114-2****** |
| guarantors[].address | guarantors[].address | 주소 | text | 강원특별자치도 춘천시 후석로 147, 120동 801호 |
| guarantors[].relation | guarantors[].relation | 채무자와의관계 | text | 대표이사(실제경영자) |
| seal.guarantor | seal.related | 보증인 | seal | 김아진인 |
| seal.guarantor2 | seal.guarantor2 | 보증인 | seal | 천지영인 |

연결 업무 corporate_credit · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### collateral_agreement · 근저당권설정계약서

그룹: 은행 서식 (`bank_form`)

주택담보대출용 근저당권설정계약서 (개인).

연결 업무: 주택담보대출 (mortgage)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank | bank | 은행명 | text | 기업은행 |
| creditor.name | counterparty.name | 채권자겸근저당권자 | text | 중소기업은행 |
| creditor.branch | creditor.branch | 취급점 | text | 범어지점 |
| mortgagor.name | related.name | 근저당권설정자 | text | 박찬연 |
| mortgagor.rrn | related.rrn | 실명번호 | rrn | 900210-1****** |
| mortgagor.address | related.address | 설정자주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| co_mortgagor.name | co_mortgagor.name | 공동설정자 | text | 서민진 |
| co_mortgagor.share | co_mortgagor.share | 지분 | text | 3분의 1 |
| co_mortgagor.rrn | co_mortgagor.rrn | 공동설정자실명번호 | rrn | 890630-2189779 |
| co_mortgagor.address | co_mortgagor.address | 공동설정자주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| debtor.name | customer.name | 채무자 | text | 박찬연 |
| debtor.address | customer.address | 채무자주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| rank | rank | 순위 | number | 1 |
| max_amount_korean | max_amount_korean | 채권최고액(한글) | amount_korean | 금 삼억팔천만원整 |
| max_amount | max_amount | 채권최고액 | amount | 380,000,000 |
| scope | scope | 피담보채무의범위 | text | 특정근담보 |
| secured_debt | secured_debt | 피담보채무 | text | 2026년 2월 9일자 대출거래약정서(가계용) |
| settlement_type | settlement_type | 결산기유형 | text | 지정형 |
| settlement | settlement | 결산기 | text | 2066.02.16 |
| property.location | property.location | 소재지 | text | 경기도 수원시 영통구 원천동 87 한신휴플러스에듀포레 |
| property.road_address | property.road_address | 도로명주소 | text | 경기도 수원시 영통구 매탄로 376 |
| property.structure | property.structure | 구조 | text | 철근콘크리트구조 |
| property.floors | property.floors | 층수 | text | 17층 |
| property.unit | property.unit | 건물번호 | text | 115동 2104호 |
| property.kind | property.kind | 건물종류 | text | 아파트 |
| property.exclusive_area | property.exclusive_area | 전용면적 | text | 101.84㎡ |
| property.land_right | property.land_right | 대지권 | text | 소유권대지권 9,562.1분의 54.47 |
| property.unique_no | property.unique_no | 고유번호 | text | 1792-2013-094176 |
| scope_handwritten | scope_handwritten | 자필기재(피담보채무범위) | text | 특정근담보 |
| handwritten_confirm | handwritten_confirm | 자필기재(확인) | text | 확인함 |
| contract_date | contract_date | 계약일 | date | 2026년 2월 9일 |
| signature_debtor | signature_debtor | 채무자 | text | 박찬연 |
| seal.debtor | seal.customer | 채무자 | seal | 박찬연 |
| sign.debtor | sign.customer | 채무자 | signature | 이욱유 |
| signature_mortgagor | signature_mortgagor | 근저당권설정자 | text | 박찬연 |
| seal.mortgagor | seal.related | 근저당권설정자 | seal | 박찬연인 |
| seal.co_mortgagor | seal.co_mortgagor | 인감 | seal | 서민진인 |
| joint_collateral[].kind | joint_collateral[].kind | 종류 | text | 토지 |
| joint_collateral[].location | joint_collateral[].location | 소재지번 | text | 인천광역시 연수구 송도동 517 |
| joint_collateral[].detail | joint_collateral[].detail | 지목면적 | text | 잡종지 325.6㎡ |
| joint_collateral[].unique_no | joint_collateral[].unique_no | 고유번호 | text | 1236-1995-087174 |
| special_terms[] | special_terms[] | 특약사항 | text | 이 근저당권은 공동담보로서 각 담보물건은 피담보채무 전액을 담보하며, 일부 담보물건의 해지는 은행의 승낙을 받아야 한다. |
| mortgagor_relation | mortgagor_relation | 채무자와의관계 | text | 부 |

연결 업무 mortgage · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### guarantee_agreement · 보증약정서

그룹: 은행 서식 (`bank_form`)

법인 여신에 대한 대표이사 보증약정서.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank | bank | 은행명 | text | 기업은행 |
| creditor | creditor | 채권자 | text | 중소기업은행 |
| branch | branch | 취급점 | text | 범어지점 |
| debtor.name | customer.name | 채무자 | text | (주)유니온무역 |
| debtor.biz_no | customer.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| debtor.ceo | customer.ceo | 대표자 | text | 박찬연 |
| debtor.address | customer.address | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| guarantor.name | related.name | 보증인 | text | 박찬연 |
| guarantor.rrn | related.rrn | 실명번호 | rrn | 900210-1****** |
| guarantor.address | related.address | 보증인주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| guarantor.phone | related.phone | 연락처 | phone | 010-5907-7253 |
| guarantor.relation | guarantor.relation | 채무자와의관계 | text | 대표이사 |
| method | method | 보증방법 | text | 한정근보증 |
| secured_debt | secured_debt | 피보증채무 | text | 일반자금대출 거래 |
| max_amount_korean | max_amount_korean | 보증채무최고액(한글) | amount_korean | 금 삼십구억원정 |
| max_amount | max_amount | 보증채무최고액 | amount | 3,900,000,000 |
| period | period | 보증기간 | text | 2026년 2월 3일 ~ 2029년 2월 3일 |
| handwritten.method | handwritten.method | 자필보증방법 | text | 한정근보증 |
| handwritten.name | handwritten.name | 자필성명 | text | 박찬연 |
| handwritten.max_amount | handwritten.max_amount | 자필보증채무최고액 | amount_korean | 금 삼십구억원정 |
| handwritten.confirm | handwritten.confirm | 자필설명확인 | text | 충분히 설명듣고 이해함 |
| explained | explained | 설명이해확인 | checkbox | 예 |
| contract_date | contract_date | 약정일 | date | 2026년 02월 03일 |
| signature | signature | 보증인 | text | 박찬연 |
| seal.guarantor | seal.related | 보증인 | seal | 강순준인 |
| special_terms[] | special_terms[] | 특약사항 | text | 공동보증인이 있는 경우 각 보증인은 보증채무최고액 2,400,000,000원 범위에서 채무 전액에 대하여 연대하여 책임을 진다. |
| co_guarantors[].name | co_guarantors[].name | 보증인 | text | 정주하 |
| co_guarantors[].rrn | co_guarantors[].rrn | 실명번호 | rrn | 650617-2119564 |
| co_guarantors[].address | co_guarantors[].address | 보증인주소 | text | 서울특별시 종로구 자하문로 26, 115동 503호 |
| co_guarantors[].phone | co_guarantors[].phone | 연락처 | phone | 010-6311-7824 |
| co_guarantors[].relation | co_guarantors[].relation | 채무자와의관계 | text | 감사 |
| seal.co_guarantor | seal.co_guarantor | 인감 | seal | 정주하인 |
| seal.co_guarantor2 | seal.co_guarantor2 | 인감 | seal | 원주연인 |

### auto_transfer_application · 자동이체 신청서

그룹: 은행 서식 (`bank_form`)

대출이자/원리금 자동이체 신청서.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank | bank | 은행명 | text | 기업은행 |
| biller.name | counterparty.name | 수납기관 | text | 중소기업은행 |
| branch | branch | 취급점 | text | 범어지점 |
| kind | kind | 신청구분 | checkbox | 신규 |
| biller.fee_type | biller.fee_type | 요금종류 | text | 대출원리금(주택담보대출) |
| target | target | 이체대상 | checkbox | 대출원리금 |
| loan_product | loan_product | 대출상품명 | text | 아파트 담보대출 |
| loan_account | loan_account | 납부자번호(대출계좌번호) | account_no | 740-757492-44-140 |
| applicant.name | customer.name | 신청인 | text | 박찬연 |
| applicant.birth | customer.birth | 생년월일 | date | 1990-02-10 |
| applicant.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| applicant.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| debit.bank | debit.bank | 출금은행 | text | 기업은행 |
| debit.account | debit.account | 출금계좌번호 | account_no | 171-760452-29-611 |
| debit.holder | debit.holder | 예금주 | text | 박찬연 |
| debit.holder_birth | debit.holder_birth | 예금주생년월일 | number | 900210 |
| debit.holder_phone | debit.holder_phone | 예금주휴대전화 | phone | 010-5907-7253 |
| relation | relation | 신청인과예금주와의관계 | checkbox | 본인 |
| transfer_day | transfer_day | 출금일 | text | 매월 15일 |
| start_month | start_month | 이체개시 | text | 2026년 3월분부터 |
| amount | amount | 출금금액 | text | 청구금액 전액 (약 1,211,320원) |
| privacy_consent | privacy_consent | 개인정보수집이용동의 | checkbox | 동의함 |
| third_party_consent | third_party_consent | 제3자제공동의 | checkbox | 동의함 |
| apply_date | apply_date | 신청일 | date | 2026년 2월 3일 |
| signature | signature | 신청인 | text | 박찬연 |
| seal.applicant | seal.customer | 신청인 | seal | 강순준 |
| sign.applicant | sign.customer | 신청인 | signature | 이욱유 |
| holder_signature | holder_signature | 예금주 | text | 박찬연 |
| seal.holder | seal.holder | 예금주 | seal | 이욱유 |
| sign.holder | sign.holder | 예금주 | signature | 박찬연 |
| extra_loans[].loan_account | extra_loans[].loan_account | 납부자번호 | account_no | 2451-245-638780 |
| extra_loans[].loan_product | extra_loans[].loan_product | 대출상품 | text | 전세자금대출 |
| extra_loans[].target | extra_loans[].target | 이체대상 | text | 대출원리금 |
| extra_loans[].transfer_day | extra_loans[].transfer_day | 출금일 | text | 매월 15일 |

### customer_due_diligence · 고객확인서(개인)

그룹: 은행 서식 (`bank_form`)

특정금융정보법 제5조의2에 따른 개인 고객확인(CDD) — 은행 '고객거래확인서(개인·개인사업자용)'.

연결 업무: 개인 계좌개설 (account_opening)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank.name | bank.name | 은행명 | text | 기업은행 |
| customer.name | customer.name | 성명(한글) | text | 존 밀러 |
| customer.name_en | customer.name_en | 성명(영문) | text | KANG SOONJUN |
| customer.rrn | customer.rrn | 실명번호 | rrn | 950627-5955869 |
| customer.resident_type | customer.resident_type | 구분 | checkbox | 외국인 |
| customer.gender | customer.gender | 성별 | checkbox | 남 |
| customer.nationality | customer.nationality | 국적 | text | 미국 |
| customer.address | customer.address | 주소(거소) | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| customer.mobile | customer.mobile | 휴대전화 | phone | 010-3055-5155 |
| customer.email | customer.email | E-mail | text | john89@yahoo.com |
| job.type | job.type | 직업 | checkbox | 급여소득자 |
| job.company | job.company | 직장명 | text | 주식회사 태평양무역 |
| job.department | employer.department | 부서/직위 | text | 구매팀 / 대리 |
| job.industry | job.industry | 업종 | text | 도매 및 소매업 |
| job.work_phone | job.work_phone | 직장전화 | phone | 043-783-2775 |
| transaction.purpose | transaction.purpose | 거래목적 | checkbox | 공과금 납부결제 |
| transaction.fund_source | transaction.fund_source | 자금의원천 | checkbox | 근로 및 연금소득 |
| transaction.expected_amount | transaction.expected_amount | 예상거래금액 | checkbox | 1천만원 미만 |
| transaction.frequency | transaction.frequency | 예상거래빈도 | checkbox | 월 5회 미만 |
| beneficial_owner | beneficial_owner | 실제소유자여부 | checkbox | 예 |
| pep | pep | 외국의정치적주요인물여부 | checkbox | 아니오 |
| date | date | 작성일 | date | 2026년 01월 31일 |
| signature | signature | 고객성명 | text | MILLER JOHN |
| seal.customer | seal.customer | 고객 | seal | MILL |
| sign.customer | sign.customer | 고객 | signature | 강순준 |
| bank_use.risk_grade | bank_use.risk_grade | 고객위험등급 | checkbox | 저위험 |
| bank_use.id_type | bank_use.id_type | 실명확인증표 | checkbox | 외국인등록증 |
| bank_use.branch | bank_use.branch | 확인영업점 | text | 범어지점 |
| seal.staff.clerk | seal.staff.clerk | 담당 | seal | 김도서 |
| bank_use.clerk | bank_use.clerk | 담당 | text | 김도서 |
| seal.staff.manager | seal.staff.manager | 책임자 | seal | 강예경 |
| bank_use.manager | bank_use.manager | 책임자 | text | 강예경 |
| agent.name | agent.name | 대리인성명 | text | 기희호 |
| agent.rrn | agent.rrn | 대리인실명번호 | rrn | 700803-2****** |
| agent.relation | agent.relation | 본인과의관계 | text | 모 |
| seal.agent | seal.agent | 대리인 | seal | 김수연 |
| sign.agent | sign.agent | 대리인 | signature | 기희호 |
| job.biz_no | job.biz_no | 사업자등록번호 | biz_no | 696-24-15367 |
| job.opened | job.opened | 개업년월일 | date | 2016.10.11 |
| edd.annual_income | edd.annual_income | 연간소득 | text | 5,920만원 |
| edd.assets | edd.assets | 보유자산규모 | checkbox | 10억원~30억원 |
| edd.fund_detail | edd.fund_detail | 자금원천상세 | text | 부모로부터 증여받은 자금 (증여세 신고서 제출) |
| edd.purpose_detail | edd.purpose_detail | 거래목적상세 | text | 주식·가상자산 투자자금 이체 |
| edd.cash_tx | edd.cash_tx | 고액현금거래 | text | 월 1~2회 (1천만원 이상) |
| edd.overseas_tx | edd.overseas_tx | 해외거래 | text | 해당 없음 |
| edd.accounts[].bank | edd.accounts[].bank | 금융회사 | text | 신한은행 |
| edd.accounts[].kind | edd.accounts[].kind | 계좌종류 | text | 증권위탁 |
| edd.accounts[].purpose | edd.accounts[].purpose | 주된용도 | text | 생활비 |
| owner.name | owner.name | 실제소유자성명 | text | 김서호 |
| owner.birth | owner.birth | 실제소유자생년월일 | date | 1980.11.12 |
| owner.nationality | owner.nationality | 실제소유자국적 | text | 대한민국 |

연결 업무 account_opening · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### corporate_customer_due_diligence · 고객확인서(법인·단체)

그룹: 은행 서식 (`bank_form`)

법인 고객확인 + 실제소유자 확인 서식.

연결 업무: 법인 여신 (corporate_credit)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank.name | bank.name | 은행명 | text | 기업은행 |
| corp.name | corp.name | 법인명(국문) | text | (주)유니온무역 |
| corp.name_en | corp.name_en | 법인명(영문) | text | Union Trading Co., Ltd. |
| corp.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| corp.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| corp.established | corp.established | 설립일 | date | 2018년 11월 01일 |
| corp.industry | corp.industry | 업종 | text | 도매 및 소매업 / 무역 |
| corp.hq_address | corp.hq_address | 본점주소 | text | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| corp.biz_address | corp.biz_address | 사업장주소 | text | 본점과 동일 |
| corp.phone | corp.phone | 대표전화 | phone | 02-9508-6789 |
| corp.email | corp.email | 이메일 | text | admin@hanbit.co.kr |
| corp.corp_type | corp.corp_type | 법인구분 | checkbox | 중소기업 |
| corp.listed | corp.listed | 상장여부 | checkbox | 비상장 |
| rep.name | rep.name | 대표자성명 | text | 박찬연 |
| rep.name_en | rep.name_en | 대표자영문성명 | text | KANG SOONJUN |
| rep.birth | rep.birth | 대표자생년월일 | date | 1990.02.10 |
| rep.nationality | rep.nationality | 대표자국적 | text | 대한민국 |
| transaction.purpose | transaction.purpose | 거래목적 | checkbox | 대출 |
| transaction.fund_source | transaction.fund_source | 자금원천 | checkbox | 영업수익 |
| owner_step | owner_step | 실제소유자확인단계 | checkbox | 1단계 |
| owners[].name | owners[].name | 성명 | text | 박찬연 |
| owners[].birth | owners[].birth | 생년월일 | date | 1990.02.10 |
| owners[].nationality | owners[].nationality | 국적 | text | 대한민국 |
| owners[].ratio | owners[].ratio | 지분율 | percent | 74.04% |
| owners[].relation | owners[].relation | 법인과의관계 | text | 대표이사 |
| pep | pep | 외국의정치적주요인물여부 | checkbox | 아니오 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.corp | seal.corp | 법인인감 | seal | 유니온무역대표이사인 |
| bank_use.risk_grade | bank_use.risk_grade | 고객위험등급 | checkbox | 저위험 |
| bank_use.documents[] | bank_use.documents[] | 징구서류 | text | 사업자등록증 |
| bank_use.branch | bank_use.branch | 확인영업점 | text | 범어지점 |
| seal.staff.clerk | seal.staff.clerk | 담당 | seal | 변찬하 |
| bank_use.clerk | bank_use.clerk | 담당 | text | 변찬하 |
| seal.staff.manager | seal.staff.manager | 책임자 | seal | 이민재 |
| bank_use.manager | bank_use.manager | 책임자 | text | 이민재 |
| bank_use.documents | bank_use.documents | 징구서류 | checkbox_multi |  |
| shareholders[].name | shareholders[].name | 주주명 | text | 현예지 |
| shareholders[].birth | shareholders[].birth | 생년월일 | date | 1966.08.12 |
| shareholders[].shares | shareholders[].shares | 소유주식수 | number | 22,821 |
| shareholders[].ratio | shareholders[].ratio | 지분율 | percent | 22.82% |
| shareholders[].relation | shareholders[].relation | 법인과의관계 | text | 대표이사 |
| agent.name | agent.name | 거래담당자성명 | text | 이채지 |
| agent.rrn | agent.rrn | 거래담당자실명번호 | rrn | 981116-2****** |
| agent.position | agent.position | 직위관계 | text | 재무팀 과장 |

연결 업무 corporate_credit · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### privacy_consent · 개인(신용)정보 수집·이용·제공·조회 동의서

그룹: 은행 서식 (`bank_form`)

여신 금융거래용 개인(신용)정보 동의서 (필수/선택 동의).

연결 업무: 개인 계좌개설 (account_opening), 개인 신용대출 (personal_credit_loan), 주택담보대출 (mortgage), 전세자금대출 (jeonse_loan), 개인사업자 대출 (sole_proprietor_loan), 개인형IRP 개설 (irp_opening), 전자금융 가입 (efinance_signup)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank.name | bank.name | 은행명 | text | 기업은행 |
| consent.collect | consent.collect | 수집이용동의 | checkbox | 동의함 |
| consent.unique_id | consent.unique_id | 고유식별정보처리동의 | checkbox | 동의함 |
| providers[].name | providers[].name | 제공받는자 | text | 신용정보집중기관(한국신용정보원) |
| providers[].purpose | providers[].purpose | 제공받는자의이용목적 | text | 본인의 신용을 판단하기 위한 자료로 활용하거나 공공기관에서 정책자료로 활용 |
| providers[].items | providers[].items | 제공하는항목 | text | 개인식별정보, 신용거래정보, 신용도판단정보, 신용능력정보, 공공정보 |
| providers[].period | providers[].period | 제공받는자의보유이용기간 | text | 관련 법령 및 규약에서 정한 기간 |
| consent.provide | consent.provide | 제공동의 | checkbox | 동의함 |
| consent.provide_unique_id | consent.provide_unique_id | 고유식별정보제공동의 | checkbox | 동의함 |
| consent.inquiry | consent.inquiry | 조회동의 | checkbox | 동의함 |
| marketing.collect | marketing.collect | 마케팅수집이용동의 | checkbox | 동의함 |
| marketing.provide | marketing.provide | 마케팅제공동의 | checkbox | 동의하지 않음 |
| marketing.channels[] | marketing.channels[] | 연락방법 | text | 전화 |
| date | date | 작성일 | date | 2026.01.31 |
| applicant.birth | customer.birth | 생년월일 | date | 1990년 02월 10일 |
| applicant.name | customer.name | 본인성명 | text | 박찬연 |
| seal.applicant | seal.customer | 본인 | seal | 박찬연 |
| sign.applicant | sign.customer | 본인 | signature | 강순준 |
| seal.staff.clerk | seal.staff.clerk | 본인확인 | seal | 이태경 |
| bank_use.clerk | bank_use.clerk | 본인확인 | text | 이태경 |
| marketing.channels | marketing.channels | 연락방법 | checkbox_multi |  |
| legal_rep.name | agent.name | 법정대리인 | text | 정수린 |
| legal_rep.relation | agent.relation | 본인과의관계 | text | 모 |
| seal.legal_rep | seal.agent | 법정대리인 | seal | 정수린 |
| sign.legal_rep | sign.agent | 법정대리인 | signature | 김나진 |

연결 업무 account_opening · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 personal_credit_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 mortgage · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 jeonse_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 sole_proprietor_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 irp_opening · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 efinance_signup · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### account_opening_application · 예금거래신청서

그룹: 은행 서식 (`bank_form`)

계좌개설(신규) 신청서 — 상품, 통장, 전자금융, 알림 서비스.

연결 업무: 개인 계좌개설 (account_opening), 전자금융 가입 (efinance_signup)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank.name | bank.name | 은행명 | text | 기업은행 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.name_en | customer.name_en | 영문명 | text | PARK CHANYEON |
| customer.rrn | customer.rrn | 실명번호 | rrn | 900210-1659382 |
| customer.zipcode | customer.zipcode | 우편번호 | number | 06931 |
| customer.address | customer.address | 자택주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| customer.mobile | customer.mobile | 휴대폰 | phone | 010-5907-7253 |
| customer.email | customer.email | 이메일 | text | chanyeon363@naver.com |
| customer.job | customer.job | 직업 | text | 급여소득자 |
| customer.company | customer.company | 직장명 | text | 주식회사 태평양무역 |
| product.type | product.type | 예금종류 | checkbox | 정기예금 |
| product.name | product.name | 상품명 | text | 정기예금(일반) |
| product.amount | product.amount | 신규금액 | amount | 119,000,000원 |
| product.term | product.term | 계약기간 | text | 36개월 |
| product.interest_payment | product.interest_payment | 이자지급방법 | text | 만기일시지급 |
| product.linked_account | product.linked_account | 출금계좌 | account_no | 171-760452-29-611 |
| passbook | passbook | 통장발행 | checkbox | 미발행 |
| seal_type | seal_type | 인감서명등록 | checkbox | 인감 |
| check_card | check_card | 체크카드 | checkbox | 미신청 |
| ebank.internet | ebank.internet | 인터넷뱅킹 | checkbox | 신청 |
| ebank.mobile | ebank.mobile | 모바일뱅킹 | checkbox | 미신청 |
| ebank.otp | ebank.otp | 보안매체 | checkbox | 모바일OTP |
| ebank.limit_once | ebank.limit_once | 1회이체한도 | amount | 5,000,000원 |
| ebank.limit_day | ebank.limit_day | 1일이체한도 | amount | 5,000,000원 |
| alert | alert | 입출금알림 | checkbox | 앱 푸시 |
| mail_to | mail_to | 우편물수령처 | checkbox | 자택 |
| salary_transfer | salary_transfer | 급여이체지정 | checkbox | 미지정 |
| protection_limit | protection_limit | 예금자보호한도 | text | 1억원 |
| signature | signature | 확인자 | text | 박찬연 |
| date | date | 신청일 | date | 2026년 1월 31일 |
| seal.applicant | seal.customer | 신청인 | seal | 이재주 |
| sign.applicant | sign.customer | 신청인 | signature | 박찬연 |
| bank_use.account_no | bank_use.account_no | 계좌번호 | account_no | 956-619004-07-320 |
| bank_use.branch | bank_use.branch | 개설영업점 | text | 범어지점 |
| bank_use.id_type | bank_use.id_type | 실명확인증표 | checkbox | 주민등록증 |
| seal.staff.clerk | seal.staff.clerk | 담당 | seal | 위성준 |
| bank_use.clerk | bank_use.clerk | 담당 | text | 위성준 |
| seal.staff.manager | seal.staff.manager | 책임자 | seal | 반찬우 |
| bank_use.manager | bank_use.manager | 책임자 | text | 반찬우 |
| legal_rep.name | legal_rep.name | 법정대리인성명 | text | 이민빈 |
| legal_rep.relation | legal_rep.relation | 본인과의관계 | text | 부 |
| legal_rep.rrn | legal_rep.rrn | 법정대리인실명번호 | rrn | 720524-1****** |
| legal_rep.phone | legal_rep.phone | 법정대리인연락처 | phone | 010-6144-4077 |
| legal_rep.documents | legal_rep.documents | 제출서류 | text | 가족관계증명서(상세), 법정대리인 신분증 |
| seal.legal_rep | seal.legal_rep | 법정대리인 | seal | 옥영아 |
| sign.legal_rep | sign.legal_rep | 법정대리인 | signature | 이민빈 |
| agent.name | agent.name | 대리인성명 | text | 김준현 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| agent.rrn | agent.rrn | 대리인실명번호 | rrn | 440309-1****** |
| agent.phone | agent.phone | 대리인연락처 | phone | 010-8700-9939 |
| seal.agent | seal.agent | 대리인 | seal |  |
| sign.agent | sign.agent | 대리인 | signature | 김준현 |
| customer.nationality | customer.nationality | 국적 | text | 태국 |
| extra_products[].type | extra_products[].type | 예금종류 | text | 정기예금 |
| extra_products[].name | extra_products[].name | 상품명 | text | e-정기예금 |
| extra_products[].amount | extra_products[].amount | 신규금액 | amount | 100,000원 |
| extra_products[].term | extra_products[].term | 계약기간 | text | 24개월 |
| extra_products[].account_no | extra_products[].account_no | 계좌번호 | account_no | 199-14-607140 |

연결 업무 account_opening · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 efinance_signup · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### financial_transaction_purpose · 금융거래목적확인서

그룹: 은행 서식 (`bank_form`)

입출금계좌 신규 시 금융거래 목적과 증빙서류를 확인하는 서식 (대포통장 예방).

연결 업무: 개인 계좌개설 (account_opening)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank.name | bank.name | 은행명 | text | 기업은행 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.rrn | customer.rrn | 실명번호 | rrn | 900210-1659382 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| customer.mobile | customer.mobile | 연락처 | phone | 010-5907-7253 |
| customer.job | customer.job | 직업 | text | 개인사업자 |
| customer.company | customer.company | 직장명 | text | 동방학원 |
| account_type | account_type | 신규예금종류 | checkbox | 저축예금 |
| purpose | purpose | 금융거래목적 | checkbox | 사업자 거래 |
| evidence | evidence | 제출증빙서류 | text | 사업자등록증명 |
| questions.q1 | questions.q1 | 통장양도대여요청여부 | checkbox | 아니오 |
| questions.q2 | questions.q2 | 취업대출빙자요청여부 | checkbox | 아니오 |
| questions.q3 | questions.q3 | 최근타행계좌개설여부 | checkbox | 아니오 |
| date | date | 작성일 | date | 2026년 01월 31일 |
| signature | signature | 고객성명 | text | 박찬연 |
| seal.customer | seal.customer | 고객 | seal | 박찬연 |
| sign.customer | sign.customer | 고객 | signature | 현예지 |
| bank_use.result | bank_use.result | 처리결과 | checkbox | 일반계좌 개설 |
| seal.staff.clerk | seal.staff.clerk | 담당 | seal | 구호재 |
| bank_use.clerk | bank_use.clerk | 담당 | text | 구호재 |
| seal.staff.manager | seal.staff.manager | 책임자 | seal | 정연경 |
| bank_use.manager | bank_use.manager | 책임자 | text | 정연경 |
| customer.nationality | customer.nationality | 국적 | text | 베트남 |

연결 업무 account_opening · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### overseas_remittance_application · 해외송금신청서

그룹: 은행 서식 (`bank_form`)

당발송금(전신송금 T/T) 신청서 + 은행 사용란(환율/원화환산액).

연결 업무: 해외송금 (fx_remittance), 유학생 송금 (study_abroad_remittance)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank.name | bank.name | 은행명 | text | 기업은행 |
| remitter.name | customer.name | 송금인성명 | text | 박찬연 |
| remitter.name_en | customer.name_en | 송금인영문명 | text | PARK CHANYEON |
| remitter.rrn | customer.rrn | 실명번호 | rrn | 900210-1****** |
| remitter.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| remitter.address | customer.address | 송금인주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| remitter.company | customer.company | 상호(사업자번호) | text | 동방학원 (860-11-55034) |
| beneficiary.name | foreign.name | 수취인성명 | text | Mekong Garment JSC |
| beneficiary.address | foreign.address | 수취인주소 | text | 45 Le Loi St, District 1, Ho Chi Minh City |
| beneficiary.country | beneficiary.country | 수취인국가 | text | VIETNAM |
| beneficiary.relationship | beneficiary.relationship | 신청인과의관계 | text | 거래처 |
| beneficiary.swift | foreign.swift | SWIFTBIC | text | BFTVVNVX |
| beneficiary.bank_name | beneficiary.bank_name | 수취은행명 | text | Vietcombank |
| beneficiary.bank_address | beneficiary.bank_address | 수취은행주소 | text | 198 Tran Quang Khai St, Hoan Kiem, Hanoi, Vietnam |
| beneficiary.account_no | beneficiary.account_no | 수취인계좌번호 | account_no | 884779361534 |
| remittance.currency | remittance.currency | 송금통화 | text | USD |
| remittance.amount | remittance.amount | 송금금액 | amount | 73,190.66 |
| remittance.purpose | remittance.purpose | 송금사유 | checkbox | 수입대금 |
| remittance.purpose_code | remittance.purpose_code | 지급사유코드 | number | 10103 |
| remittance.charge | remittance.charge | 수수료부담 | checkbox | SHA |
| remittance.method | remittance.method | 송금방법 | checkbox | 전신송금(T/T) |
| remittance.message | remittance.message | 송금메시지 | text | INVOICE NO. MEK-2026-0068 |
| remittance.documents | remittance.documents | 지급증빙서류 | text | Commercial Invoice, B/L 사본 |
| date | date | 신청일 | date | 2026.01.31 |
| signature | signature | 신청인 | text | 박찬연 |
| seal.applicant | seal.customer | 신청인 | seal | 박찬연 |
| sign.applicant | sign.customer | 신청인 | signature | 강순준 |
| bank_use.ref_no | bank_use.ref_no | 참조번호 | text | OR26013115455 |
| bank_use.branch | bank_use.branch | 취급영업점 | text | 범어지점 |
| bank_use.rate | bank_use.rate | 적용환율 | number | 1,467.46 |
| bank_use.krw_amount | bank_use.krw_amount | 원화환산액 | amount | 107,404,366원 |
| bank_use.fee | bank_use.fee | 송금수수료 | amount | 20,000원 |
| bank_use.cable_fee | bank_use.cable_fee | 전신료 | amount | 8,000원 |
| bank_use.total | bank_use.total | 합계 | amount | 107,432,366원 |
| seal.staff.clerk | seal.staff.clerk | 담당자 | seal | 박서주 |
| bank_use.clerk | bank_use.clerk | 담당자 | text | 박서주 |
| seal.staff.manager | seal.staff.manager | 결재권자 | seal | 주아주 |
| bank_use.manager | bank_use.manager | 결재권자 | text | 주아주 |
| batch_count | batch_count | 송금건수 | text | 12건 |
| batch[].beneficiary | batch[].beneficiary | 수취인 | text | SAIGON TEXTILE JSC |
| batch[].message | batch[].message | 송금메시지 | text | INV 9657 |
| batch[].country | batch[].country | 국가 | text | VIETNAM |
| batch[].bank | batch[].bank | 수취은행 | text | VIETCOMBANK HO CHI MINH (BFTVVNVX007) |
| batch[].account_no | batch[].account_no | 계좌번호 | account_no | 963900390920 |
| batch[].currency | batch[].currency | 통화 | text | USD |
| batch[].amount | batch[].amount | 금액 | amount | 9,455.88 |
| agent.name | agent.name | 대리인성명 | text | 위민준 |
| agent.relation | agent.relation | 신청인과의관계 | text | 형제자매 |
| agent.rrn | agent.rrn | 대리인실명번호 | rrn | 961009-1****** |
| agent.phone | agent.phone | 대리인연락처 | phone | 010-4083-8691 |
| seal.agent | seal.agent | 대리인 | seal | 위민준 |
| sign.agent | sign.agent | 대리인 | signature | 최경재 |

연결 업무 fx_remittance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 study_abroad_remittance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### fatca_crs · 해외금융계좌 납세자 확인서(개인)

그룹: 은행 서식 (`bank_form`)

FATCA/CRS 본인확인서(개인/개인사업자용) — 국제조세조정법·금융정보자동교환 이행규정에 따른 자기확인서.

연결 업무: 개인 계좌개설 (account_opening)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank.name | bank.name | 은행명 | text | 기업은행 |
| holder.name | customer.name | 성명(한글) | text | 박찬연 |
| holder.surname_en | holder.surname_en | 영문성 | text | PARK |
| holder.given_en | holder.given_en | 영문이름 | text | CHANYEON |
| holder.birth | customer.birth | 생년월일 | date | 1990-02-10 |
| holder.mobile | customer.mobile | 연락처 | phone | 010-3347-9183 |
| holder.birth_place | holder.birth_place | 출생국가 | text | 대한민국 (KOREA) |
| holder.nationality | customer.nationality | 국적 | text | 대한민국 (KOREA) |
| holder.address | customer.address | 현재거주지주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| residence_category | residence_category | 해외거주자여부 | text | 미국 세법상 미국 거주자 |
| residences[].country | residences[].country | 거주관할권 | text | 미국 (U.S.A.) |
| residences[].tin | residences[].tin | 납세자번호 | number | 387-79-8629 |
| date | date | 작성일 | date | 2026.01.31 |
| signature | signature | 계좌보유자 | text | 박찬연 |
| seal.holder | seal.customer | 계좌보유자 | seal | 우지현 |
| sign.holder | sign.customer | 계좌보유자 | signature | 박찬연 |
| bank_use.branch | bank_use.branch | 접수영업점 | text | 범어지점 |
| seal.staff.clerk | seal.staff.clerk | 담당 | seal | 김숙희 |
| bank_use.clerk | bank_use.clerk | 담당 | text | 김숙희 |
| seal.staff.manager | seal.staff.manager | 책임자 | seal | 남궁환인 |
| bank_use.manager | bank_use.manager | 책임자 | text | 남궁환인 |
| residences[].no_tin_reason | residences[].no_tin_reason | 납세자번호미기재사유 | text | C |

연결 업무 account_opening · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### business_registration_certificate · 사업자등록증

그룹: 개인사업자 (`business`)

세무서가 발급하는 개인사업자 사업자등록증.  정정 교부(사업장 이전·업종 추가·과세유형 전환·상호 변경)와 공동사업자는 _biz_facts() 의 프로필 고정 사실을 따른다.

연결 업무: 개인사업자 대출 (sole_proprietor_loan)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| kind | kind | 과세유형 | text | 일반과세자 |
| biz_no | biz_no | 등록번호 | biz_no | 860-11-55034 |
| trade_name | trade_name | 상호 | text | 동방학원 |
| name | name | 성명 | text | 박찬연 |
| birth | birth | 생년월일 | date | 1990년 02월 10일 |
| opened | opened | 개업연월일 | date | 2020년 03월 21일 |
| address | address | 사업장소재지 | text | 울산광역시 남구 대학로 14, 11층 (달동, 아이엠스퀘어) |
| biz_type | biz_type | 업태 | text | 서비스업 |
| biz_item | biz_item | 종목 | text | 학원 |
| issue_reason | issue_reason | 발급사유 | text | 정정(과세유형 전환) |
| co_owner | co_owner | 공동사업자 | text | 김훈도 |
| unit_taxation | unit_taxation | 사업자단위과세적용사업자여부 | text | 부 |
| issue_date | issue_date | 발급일 | date | 2024년 07월 08일 |
| issuer | issuer | 발급기관 | text | 울산세무서장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 울산세무서장인 |
| einvoice_email | einvoice_email | 전자세금계산서전용전자우편주소 | text | soonjun606@gmail.com |
| sub_kinds[].biz_type | sub_kinds[].biz_type | 업태 | text | 음식점업 |
| sub_kinds[].biz_item | sub_kinds[].biz_item | 종목 | text | 커피전문점 |

연결 업무 sole_proprietor_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### business_registration_certificate_corp · 사업자등록증(법인사업자)

그룹: 개인사업자 (`business`)

세무서가 발급하는 법인사업자 사업자등록증.  본점 이전·상호 변경·공동대표 취임은 법인등기부(corporate._facts)와 같은 날짜를 쓰고, 등기 뒤 1~4주 안에 정정 교부.

연결 업무: 법인 여신 (corporate_credit)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| biz_no | biz_no | 등록번호 | biz_no | 264-82-36559 |
| corp_name | corp.name | 법인명(단체명) | text | (주)유니온무역 |
| ceo | ceo | 대표자 | text | 박찬연 |
| opened | opened | 개업연월일 | date | 2018년 11월 01일 |
| corp_reg_no | corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| address | address | 사업장소재지 | text | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| head_office | head_office | 본점소재지 | text | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| biz_type | biz_type | 업태 | text | 도매 및 소매업 |
| biz_item | biz_item | 종목 | text | 무역 |
| issue_reason | issue_reason | 발급사유 | text | 재발급 |
| unit_taxation | unit_taxation | 사업자단위과세적용사업자여부 | text | 부 |
| issue_date | issue_date | 발급일 | date | 2021년 08월 03일 |
| issuer | issuer | 발급기관 | text | 중부세무서장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 중부세무서장인 |
| einvoice_email | einvoice_email | 전자세금계산서전용전자우편주소 | text | contact@daesung.co.kr |
| sub_kinds[].biz_type | sub_kinds[].biz_type | 업태 | text | 소매업 |
| sub_kinds[].biz_item | sub_kinds[].biz_item | 종목 | text | 전자상거래 |
| co_ceo | co_ceo | 대표자 | text | 허석주 |

연결 업무 corporate_credit · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### business_registration_proof · 사업자등록증명

그룹: 개인사업자 (`business`)

홈택스에서 발급한 개인사업자 사업자등록증명. 부업종·공동사업자는 _biz_facts() 를 따른다.

연결 업무: 개인사업자 대출 (sole_proprietor_loan)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| issue_no | issue_no | 발급번호 | text | 5992-133-7220-660 |
| trade_name | trade_name | 상호(법인명) | text | 동방학원 |
| biz_no | biz_no | 사업자등록번호 | biz_no | 860-11-55034 |
| name | name | 성명(대표자) | text | 박찬연 |
| rrn | rrn | 주민(법인)등록번호 | rrn | 900210-1****** |
| address | address | 사업장소재지 | text | 울산광역시 남구 대학로 14, 11층 (달동, 아이엠스퀘어) |
| opened | opened | 개업일 | date | 2020년 03월 21일 |
| registered | registered | 사업자등록일 | date | 2020년 03월 17일 |
| kind | kind | 과세유형 | text | 일반과세자 |
| joint | joint | 공동사업자 | text | 해당없음 |
| kinds[].biz_type | kinds[].biz_type | 업태 | text | 서비스업 |
| kinds[].biz_item | kinds[].biz_item | 종목 | text | 학원 |
| kinds[].code | kinds[].code | 업종코드 | number | 809009 |
| kinds[].main | kinds[].main | 구분 | text | 주업종 |
| purpose | purpose | 사용목적 | text | 은행 제출 |
| submit_to | submit_to | 제출처 | text | 기업은행 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 울산세무서장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 울산세무서장인 |
| co_owners[].name | co_owners[].name | 성명 | text | 김나진 |
| co_owners[].rrn | co_owners[].rrn | 주민등록번호 | rrn | 711009-2****** |
| co_owners[].share | co_owners[].share | 지분율 | percent | 60% |
| co_owners[].role | co_owners[].role | 구분 | text | 대표공동사업자 |

연결 업무 sole_proprietor_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### standard_financial_statement_proof · 표준재무제표증명

그룹: 개인사업자 (`business`)

홈택스 발급 표준재무제표증명(개인): 표준재무상태표 + 표준손익계산서.  heavy: 세부 계정과목까지 표시 (재무상태표 30~40줄, 손익계산서 25~35줄, 2~3쪽). 신고구분·신고일은 종합소득세 신고(_itr_filing)와 같다 (기한후신고·수정신고면 그 날짜).

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| issue_no | issue_no | 발급번호 | text | 6888-572-1183-223 |
| taxpayer_type | taxpayer_type | 개인/법인 | checkbox | 개인 |
| taxpayer.trade_name | customer.trade_name | 상호(법인명) | text | 동방학원 |
| taxpayer.biz_no | customer.biz_no | 사업자등록번호 | biz_no | 860-11-55034 |
| taxpayer.name | customer.name | 성명(대표자) | text | 박찬연 |
| taxpayer.rrn | customer.rrn | 주민(법인)등록번호 | rrn | 900210-1****** |
| taxpayer.biz_type | taxpayer.biz_type | 업태 | text | 서비스업 |
| taxpayer.biz_item | taxpayer.biz_item | 종목 | text | 학원 |
| taxpayer.address | customer.address | 사업장 | text | 울산광역시 남구 대학로 14, 11층 (달동, 아이엠스퀘어) |
| period | period | 사업연도 | text | 2024-01-01 ~ 2024-12-31 |
| filing_kind | filing_kind | 신고구분 | text | 정기신고 |
| attachments | attachments | 첨부서류 | text | 표준재무상태표, 표준손익계산서 |
| filed_date | filed_date | 신고일 | date | 2025-06-21 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 울산세무서장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 울산세무서장인 |
| balance_sheet.current | balance_sheet.current | 유동자산 | amount | 200,632,487 |
| balance_sheet.quick | balance_sheet.quick | 당좌자산 | number | 190,196,447 |
| balance_sheet.inventory | balance_sheet.inventory | 재고자산 | number | 10,436,040 |
| balance_sheet.noncurrent | balance_sheet.noncurrent | 비유동자산 | amount | 158,229,375 |
| balance_sheet.investment | balance_sheet.investment | 투자자산 | number | 3,709,694 |
| balance_sheet.tangible | balance_sheet.tangible | 유형자산 | number | 127,274,649 |
| balance_sheet.intangible | balance_sheet.intangible | 무형자산 | number | 2,744,699 |
| balance_sheet.other_noncurrent | balance_sheet.other_noncurrent | 기타비유동자산 | amount | 24,500,333 |
| balance_sheet.assets | balance_sheet.assets | 자산총계 | amount | 358,861,862 |
| balance_sheet.current_liab | balance_sheet.current_liab | 유동부채 | amount | 101,614,107 |
| balance_sheet.noncurrent_liab | balance_sheet.noncurrent_liab | 비유동부채 | amount | 153,194,870 |
| balance_sheet.liabilities | balance_sheet.liabilities | 부채총계 | amount | 254,808,977 |
| balance_sheet.capital | balance_sheet.capital | 자본금 | amount | 104,052,885 |
| balance_sheet.equity | balance_sheet.equity | 자본총계 | amount | 104,052,885 |
| balance_sheet.liab_equity | balance_sheet.liab_equity | 부채와자본총계 | amount | 358,861,862 |
| income_statement.revenue | income_statement.revenue | 매출액 | amount | 417,475,090 |
| income_statement.cogs | income_statement.cogs | 매출원가 | number | 44,004,509 |
| income_statement.gross | income_statement.gross | 매출총이익 | number | 373,470,581 |
| income_statement.sga | income_statement.sga | 판매비와관리비 | number | 332,766,929 |
| income_statement.salary | income_statement.salary | 급여 | amount | 194,386,270 |
| income_statement.welfare | income_statement.welfare | 복리후생비 | number | 23,326,350 |
| income_statement.rent | income_statement.rent | 임차료 | amount | 59,812,100 |
| income_statement.depreciation | income_statement.depreciation | 감가상각비 | number | 20,263,010 |
| income_statement.other_sga | income_statement.other_sga | 기타판매비와관리비 | number | 34,979,199 |
| income_statement.op | income_statement.op | 영업이익 | number | 40,703,652 |
| income_statement.non_op_income | income_statement.non_op_income | 영업외수익 | amount | 438,652 |
| income_statement.non_op_expense | income_statement.non_op_expense | 영업외비용 | amount | 2,883,032 |
| income_statement.net | income_statement.net | 당기순이익 | number | 38,259,272 |
| bs_accounts.quick[].account | bs_accounts.quick[].account | 계정과목 | text | 현금및현금성자산 |
| bs_accounts.quick[].amount | bs_accounts.quick[].amount | 금액 | amount | 65,982,923 |
| bs_accounts.inventory[].account | bs_accounts.inventory[].account | 계정과목 | text | 상품 |
| bs_accounts.inventory[].amount | bs_accounts.inventory[].amount | 금액 | amount | 3,607,371 |
| bs_accounts.investment[].account | bs_accounts.investment[].account | 계정과목 | text | 장기금융상품 |
| bs_accounts.investment[].amount | bs_accounts.investment[].amount | 금액 | amount | 6,757,583 |
| bs_accounts.tangible[].account | bs_accounts.tangible[].account | 계정과목 | text | 차량운반구 |
| bs_accounts.tangible[].amount | bs_accounts.tangible[].amount | 금액 | amount | 59,911,859 |
| bs_accounts.intangible[].account | bs_accounts.intangible[].account | 계정과목 | text | 상표권 |
| bs_accounts.intangible[].amount | bs_accounts.intangible[].amount | 금액 | amount | 10,397,329 |
| bs_accounts.other_noncurrent[].account | bs_accounts.other_noncurrent[].account | 계정과목 | text | 임차보증금 |
| bs_accounts.other_noncurrent[].amount | bs_accounts.other_noncurrent[].amount | 금액 | amount | 19,734,714 |
| bs_accounts.current_liab[].account | bs_accounts.current_liab[].account | 계정과목 | text | 매입채무 |
| bs_accounts.current_liab[].amount | bs_accounts.current_liab[].amount | 금액 | amount | 17,965,282 |
| bs_accounts.noncurrent_liab[].account | bs_accounts.noncurrent_liab[].account | 계정과목 | text | 장기차입금 |
| bs_accounts.noncurrent_liab[].amount | bs_accounts.noncurrent_liab[].amount | 금액 | amount | 125,502,355 |
| pl_accounts.revenue[].account | pl_accounts.revenue[].account | 계정과목 | text | 용역매출 |
| pl_accounts.revenue[].amount | pl_accounts.revenue[].amount | 금액 | amount | 335,244,390 |
| pl_accounts.cogs[].account | pl_accounts.cogs[].account | 계정과목 | text | 기초재고액 |
| pl_accounts.cogs[].amount | pl_accounts.cogs[].amount | 금액 | amount | 12,295,718 |
| pl_accounts.sga[].account | pl_accounts.sga[].account | 계정과목 | text | 퇴직급여 |
| pl_accounts.sga[].amount | pl_accounts.sga[].amount | 금액 | amount | 1,988,130 |
| pl_accounts.non_op_income[].account | pl_accounts.non_op_income[].account | 계정과목 | text | 이자수익 |
| pl_accounts.non_op_income[].amount | pl_accounts.non_op_income[].amount | 금액 | amount | 584,199 |
| pl_accounts.non_op_expense[].account | pl_accounts.non_op_expense[].account | 계정과목 | text | 이자비용 |
| pl_accounts.non_op_expense[].amount | pl_accounts.non_op_expense[].amount | 금액 | amount | 2,076,494 |

### corporate_registry · 법인 등기사항전부증명서(현재 유효사항)

그룹: 법인 (`corporate`)

인터넷등기소 발급 법인 등기사항전부증명서.  기본은 '현재 유효사항'. heavy/special(full_history) 이면 '말소사항 포함'으로 상호·본점·자본금·목적·임원·지점의 지난 기록을 모두 싣고 말소된 기록은 빨간 줄로 긋는다 (실제 등기부 방식). 임원 변경이 많으면 여러 쪽.

연결 업무: 법인 여신 (corporate_credit)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| viewed_at | viewed_at | 열람일시 | datetime | 2026년01월31일 15시09분03초 |
| issue_type | issue_type | 발급구분 | text | 열람용 |
| issue_scope | issue_scope | 증명서구분 | text | 현재 유효사항 |
| reg_no | reg_no | 등기번호 | number | 155825 |
| corp_reg_no | corp_reg_no | 등록번호 | corp_reg_no | 200112-7448551 |
| company_name | corp.name | 상호 | text | 주식회사 유니온무역 |
| head_office | head_office | 본점 | text | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| notice_method | notice_method | 공고방법 | text | 서울특별시 내에서 발행되는 일간 서울경제신문에 게재한다. |
| par_value | par_value | 1주의금액 | amount | 금 5,000 원 |
| authorized_shares | authorized_shares | 발행할주식의총수 | text | 400,000 주 |
| issued_shares | issued_shares | 발행주식의총수 | text | 10,000 주 |
| common_shares | common_shares | 보통주식 | text | 10,000 주 |
| capital | capital | 자본금의액 | amount | 금 50,000,000 원 |
| capital_change.changed | capital_change.changed | 변경연월일 | text | 2025.02.08 변경 |
| capital_change.registered | capital_change.registered | 등기연월일 | text | 2025.02.13 등기 |
| purposes[] | purposes[] | 목적 | text | 1. 무역업 |
| officers[].position | officers[].position | 직위 | text | 사내이사 |
| officers[].name | officers[].name | 성명 | text | 박찬연 |
| officers[].rrn | officers[].rrn | 주민등록번호 | rrn | 900210-******* |
| officers[].appointed | officers[].appointed | 취임일 | date | 2024 년 11 월 01 일 |
| officers[].appointment_type | officers[].appointment_type | 취임구분 | text | 중임 |
| officers[].registered | officers[].registered | 등기일 | date | 2024 년 11 월 14 일 |
| officers[].address | officers[].address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| established | established | 회사성립연월일 | date | 2018 년 11 월 01 일 |
| opening_reason | opening_reason | 등기기록개설사유 | text | 설립 |
| opening_date | opening_date | 등기기록개설일 | date | 2018 년 11 월 01 일 |
| jurisdiction | jurisdiction | 관할등기소 | text | 서울중앙지방법원 등기국 |
| issue_no | issue_no | 발행번호 | number | 63538237030711037235 |
| name_history[].name | name_history[].name | 상호 | text | 주식회사 한빛코리아 |
| company_name_change.changed | company_name_change.changed | 변경연월일 | text | 2024.02.05 변경 |
| company_name_change.registered | company_name_change.registered | 등기연월일 | text | 2024.02.10 등기 |
| capital_history[].issued_shares | capital_history[].issued_shares | 발행주식의총수 | text | 100,000 주 |
| capital_history[].common_shares | capital_history[].common_shares | 보통주식 | text | 100,000 주 |
| capital_history[].capital | capital_history[].capital | 자본금의액 | amount | 금 500,000,000 원 |
| capital_history[].changed | capital_history[].changed | 변경연월일 | text | 2022.12.31 변경 |
| capital_history[].registered | capital_history[].registered | 등기연월일 | text | 2023.01.09 등기 |
| officers[].ended | officers[].ended | 퇴임일 | date | 2024 년 05 월 11 일 |
| officers[].end_type | officers[].end_type | 퇴임구분 | text | 사임 |
| officers[].end_registered | officers[].end_registered | 등기일 | date | 2024 년 05 월 15 일 |
| fee | fee | 수수료 | amount | 1,000원 |
| issue_date | issue_date | 발행일 | text | 서기 2025년 05월 19일 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 전산운영책임관인 |
| confirm_no | confirm_no | 발급확인번호 | text | 2QN6-F8DU-8EAX |
| issue_date_short | issue_date_short | 발행일 | date | 2025/05/19 |
| head_office_change.changed | head_office_change.changed | 변경연월일 | text | 2022.10.28 이전 |
| head_office_change.registered | head_office_change.registered | 등기연월일 | text | 2022.11.05 등기 |
| purpose_change.changed | purpose_change.changed | 변경연월일 | text | 2023.06.14 변경 |
| purpose_change.registered | purpose_change.registered | 등기연월일 | text | 2023.06.17 등기 |
| branches[].no | branches[].no | 지점번호 | number | 1 |
| branches[].address | branches[].address | 지점소재지 | text | 제주특별자치도 제주시 중앙로 442, 4층 08호 (연동, 스마트빌딩) |
| branches[].opened | branches[].opened | 설치일 | date | 2024 년 01 월 15 일 |
| branches[].opened_registered | branches[].opened_registered | 등기일 | date | 2024 년 01 월 19 일 |
| office_history[].address | office_history[].address | 본점 | text | 부산광역시 해운대구 해운대로 480, 2층 09호 (재송동, 현대센터) |
| office_history[].changed | office_history[].changed | 변경연월일 | text | 2021.11.15 이전 |
| office_history[].registered | office_history[].registered | 등기연월일 | text | 2021.11.18 등기 |
| purpose_history[].purposes[] | purpose_history[].purposes[] | 목적 | text | 1. 광고 대행업 |
| purpose_history[].changed | purpose_history[].changed | 변경연월일 | text | 2022.11.25 변경 |
| purpose_history[].registered | purpose_history[].registered | 등기연월일 | text | 2022.12.04 등기 |
| preferred_shares | preferred_shares | 상환전환우선주식 | text | 29,996 주 |
| branches[].closed | branches[].closed | 폐지일 | date | 2022 년 09 월 10 일 |
| branches[].closed_registered | branches[].closed_registered | 등기일 | date | 2022 년 09 월 18 일 |
| name_history[].changed | name_history[].changed | 변경연월일 | text | 2022.04.20 변경 |
| name_history[].registered | name_history[].registered | 등기연월일 | text | 2022.04.26 등기 |
| joint_representation | joint_representation | 공동대표 | text | 대표이사 현예지, 대표이사 정주하는 공동으로 회사를 대표 |
| joint_registered | joint_registered | 등기일 | date | 2024 년 01 월 26 일 |

연결 업무 corporate_credit · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### articles_of_incorporation · 정관

그룹: 법인 (`corporate`)

주식회사 정관 사본 (원본대조필).  기본은 첫 쪽(총칙·주식)만 싣고 '중략' 후 부칙. heavy 면 전문(주주총회·이사·감사·계산 장까지, 3~4쪽). 개정 이력은 프로필 단위(_facts): 상호 변경·목적 추가 등 등기부 변경과 같은 날 개정, 해당 조문 끝에 <개정 …>.

연결 업무: 법인 여신 (corporate_credit)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company_name | corp.name | 상호 | text | 주식회사 유니온무역 |
| revision_history[] | revision_history[] | 제정·개정일 | text | 제정 2018.11.01 |
| company_name_en | company_name_en | 영문상호 | text | Union Trading Co., Ltd. |
| purposes[] | purposes[] | 목적 | text | 1. 무역업 |
| head_office_city | head_office_city | 본점소재지 | text | 서울특별시 |
| notice_method | notice_method | 공고방법 | text | 서울특별시 내에서 발행되는 일간 서울경제신문에 게재한다. |
| authorized_shares | authorized_shares | 발행예정주식의총수 | text | 400,000주 |
| par_value | par_value | 1주의금액 | amount | 금 5,000원 |
| initial_shares | initial_shares | 설립시발행주식총수 | text | 5,000주 |
| effective_date | effective_date | 시행일 | date | 2018년 11월 1일 |
| revision_effective[] | revision_effective[] | 시행일 | date | 2020년 6월 26일 |
| certify_date | certify_date | 증명일 | date | 2026년 1월 24일 |
| ceo | ceo | 대표이사 | text | 박찬연 |
| seal.corp | seal.corp | 법인인감 | seal | 주식회사 유니온무역 대표이사인 |
| amended.company_name | amended.company_name | 개정일 | date | 2024.02.05 |
| amended.purposes | amended.purposes | 개정일 | date | 2023.06.14 |
| preferred | preferred | 종류주식 | text | 상환전환우선주식 |
| amended.share_types | amended.share_types | 개정일 | date | 2011.06.28 |

연결 업무 corporate_credit · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### shareholder_registry · 주주명부

그룹: 법인 (`corporate`)

법인 주주명부 (대표이사 확인 날인).  주주 구성은 프로필 단위(_cap_table): heavy 면 주주 20~40명(여러 쪽), 자기주식(회사 명의, 비고 '자기주식'), 투자사 법인주주(상환전환우선주) 특수 상황.

연결 업무: 법인 여신 (corporate_credit)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| base_date | base_date | 기준일 | date | 2026.01.26 |
| company_name | corp.name | 회사명 | text | (주)유니온무역 |
| corp_reg_no | corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| biz_no | biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| total_shares | total_shares | 발행주식총수 | text | 10,000주 |
| head_office | head_office | 본점소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| par_value | par_value | 1주의금액 | amount | 5,000원 |
| capital | capital | 자본금 | amount | 50,000,000원 |
| shareholders[].no | shareholders[].no | 번호 | number | 1 |
| shareholders[].name | shareholders[].name | 주주명 | text | 박찬연 |
| shareholders[].id_no | shareholders[].id_no | 주민등록번호(사업자번호) | rrn | 900210-******* |
| shareholders[].address | shareholders[].address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| shareholders[].share_type | shareholders[].share_type | 주식종류 | text | 보통주 |
| shareholders[].shares | shareholders[].shares | 소유주식수 | number | 7,404 |
| shareholders[].amount | shareholders[].amount | 금액 | amount | 37,020,000 |
| shareholders[].ratio | shareholders[].ratio | 지분율 | percent | 74.0% |
| shareholders[].acquired | shareholders[].acquired | 취득일 | date | 2018.11.01 |
| shareholders[].note | shareholders[].note | 비고 | text | 대표이사 |
| sum_shares | sum_shares | 합계주식수 | amount | 10,000 |
| sum_amount | sum_amount | 합계금액 | amount | 50,000,000 |
| sum_ratio | sum_ratio | 합계지분율 | percent | 100.0% |
| certify_date | certify_date | 확인일 | date | 2026년 1월 31일 |
| ceo | ceo | 대표이사 | text | 박찬연 |
| seal.corp | seal.corp | 법인인감 | seal | 주식회사 유니온무역 대표이사인 |

연결 업무 corporate_credit · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### financial_statements · 재무제표(재무상태표·손익계산서)

그룹: 법인 (`corporate`)

최근 결산 2개년 비교 재무상태표 + 손익계산서 (일반기업회계기준 과목 배열, 자산 = 부채 + 자본).  heavy: 판매비와관리비·매출원가 세부 계정 + 이익잉여금처분계산서 (+ 제조업은 제조원가명세서) → 2~3쪽. special: net_loss 당기순손실, certified 원본대조(대표이사 확인·법인인감).

연결 업무: 법인 여신 (corporate_credit)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| current_term | current_term | 당기 | text | 제 7(당)기 |
| bs_current_date | bs_current_date | 당기말 | text | 2024년 12월 31일 현재 |
| prior_term | prior_term | 전기 | text | 제 6(전)기 |
| bs_prior_date | bs_prior_date | 전기말 | text | 2023년 12월 31일 현재 |
| company_name | corp.name | 회사명 | text | (주)유니온무역 |
| unit | unit | 단위 | text | (단위 : 원) |
| assets[].account | assets[].account | 과목 | text | Ⅰ. 유동자산 |
| assets[].current | assets[].current | 당기 | amount | 11,122,518,720 |
| assets[].prior | assets[].prior | 전기 | number | 8,311,220,220 |
| liabilities[].account | liabilities[].account | 과목 | text | Ⅰ. 유동부채 |
| liabilities[].current | liabilities[].current | 당기 | amount | 9,252,827,912 |
| liabilities[].prior | liabilities[].prior | 전기 | number | 4,625,491,116 |
| equity[].account | equity[].account | 과목 | text | Ⅰ. 자본금 |
| equity[].current | equity[].current | 당기 | amount | 50,000,000 |
| equity[].prior | equity[].prior | 전기 | number | 50,000,000 |
| total_liabilities_equity.current | total_liabilities_equity.current | 부채와자본총계(당기) | amount | 36,481,679,381 |
| total_liabilities_equity.prior | total_liabilities_equity.prior | 부채와자본총계(전기) | number | 27,119,928,475 |
| is_current_period | is_current_period | 당기회계기간 | text | 2024년 01월 01일부터 2024년 12월 31일까지 |
| is_prior_period | is_prior_period | 전기회계기간 | text | 2023년 01월 01일부터 2023년 12월 31일까지 |
| income_statement[].account | income_statement[].account | 과목 | text | Ⅰ. 매출액 |
| income_statement[].current | income_statement[].current | 당기 | amount | 61,800,000,000 |
| income_statement[].prior | income_statement[].prior | 전기 | number | 49,310,988,871 |
| appropriation_date_current | appropriation_date_current | 처분일 | text | 처분예정일 2025년 03월 27일 |
| appropriation_date_prior | appropriation_date_prior | 처분일 | text | 처분확정일 2024년 03월 26일 |
| appropriation[].account | appropriation[].account | 과목 | text | Ⅰ. 미처분이익잉여금 |
| appropriation[].current | appropriation[].current | 당기 | amount | 17,163,787,652 |
| appropriation[].prior | appropriation[].prior | 전기 | number | 8,649,782,085 |
| certify_date | certify_date | 확인일 | date | 2025년 08월 21일 |
| ceo | ceo | 대표이사 | text | 이민빈 |
| seal.corp | seal.corp | 법인인감 | seal | 주식회사 스마트에프앤비 대표이사인 |
| manufacturing_cost[].account | manufacturing_cost[].account | 과목 | text | Ⅰ. 재료비 |
| manufacturing_cost[].current | manufacturing_cost[].current | 당기 | amount | 30,291,246,736 |
| manufacturing_cost[].prior | manufacturing_cost[].prior | 전기 | number | 23,074,391,287 |

연결 업무 corporate_credit · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### corporate_seal_certificate · 법인인감증명서

그룹: 법인 (`corporate`)

등기소 발급 법인 인감증명서.

연결 업무: 법인 여신 (corporate_credit)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| issue_no | issue_no | 발급번호 | text | 7988-2706-6500-7892 |
| reg_no | reg_no | 등기번호 | number | 155825 |
| seal.registered | seal.registered | 등록인감 | seal | 주식회사 유니온무역 대표이사인 |
| corp_reg_no | corp_reg_no | 등록번호 | corp_reg_no | 200112-7448551 |
| company_name | corp.name | 상호 | text | 주식회사 유니온무역 |
| head_office | head_office | 본점 | text | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| rep_title | rep_title | 자격 | text | 대표이사 |
| rep_name | corp.ceo | 성명 | text | 박찬연 |
| rep_rrn | rep_rrn | 주민등록번호 | rrn | 900210-1****** |
| purpose | purpose | 용도 | text | 여신거래용 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 25일 |
| issue_office | issue_office | 발급기관 | text | 서울중앙지방법원 등기국 |
| registrar | registrar | 등기관 | text | 이정유 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 등기관인 |
| fee | fee | 수수료 | amount | 1,000원 |
| confirm_no | confirm_no | 발급확인번호 | text | 6HW4-R4PD-T4YS |

연결 업무 corporate_credit · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### board_minutes · 이사회의사록

그룹: 법인 (`corporate`)

은행 차입 승인 이사회의사록 (출석 이사 기명날인).  heavy: 안건 5~8개(지점 설치·주총 소집·담보 제공 등) → 2쪽. special: dissent 반대·기권 이사, remote 원격(화상) 참석, notarized 공증인 인증, seal_missing 일부 이사 날인 누락.

연결 업무: 법인 여신 (corporate_credit)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| datetime | datetime | 일시 | text | 2026년 1월 21일 오후 3시 00분 |
| venue | venue | 장소 | text | 본점 회의실 (서울특별시 중구 다산로 361, 6층) |
| directors_total | directors_total | 이사총수 | text | 3명 |
| directors_present | directors_present | 출석이사수 | text | 3명 |
| auditor_total | auditor_total | 감사총수 | text | 1명 |
| auditor_present | auditor_present | 출석감사수 | text | 1명 |
| chair | chair | 의장 | text | 박찬연 |
| loan.lender | loan.lender | 차입은행 | text | 기업은행 |
| loan.bank | loan.bank | 차입기관 | text | 기업은행 범어지점 |
| loan.kind | loan.kind | 대출과목 | text | 일반자금대출 |
| loan.amount | loan.amount | 차입금액 | amount | 금 사십삼억일천만원정 (₩4,310,000,000) |
| loan.period | loan.period | 차입기간 | text | 1년 (2026.01.28 ~ 2027.01.27) |
| loan.purpose | loan.purpose | 자금용도 | text | 운영자금 |
| loan.rate | loan.rate | 적용금리 | text | 변동금리 (CD 91일물 + 가산금리) |
| loan.collateral | loan.collateral | 담보 | text | 신용 |
| agendas[].no | agendas[].no | 의안번호 | text | 제2호 의안 |
| agendas[].title | agendas[].title | 의안 | text | 차입 관련 제반 권한 위임의 건 |
| agendas[].body | agendas[].body | 결의내용 | text | 의장은 제1호 의안의 차입과 관련하여 여신거래약정서 등 제반 서류의 작성, 날인 및 제출 등 일체의 권한을 대표이사에게 위임할 것을 제안하고 그 가부를 물은바, 출석이사 전원의 찬성으로 원안대로 승인 가결하다. |
| agendas[].detail | agendas[].detail | 세부내용 | text | 지점명 : 제주지점 / 소재지 : 제주특별자치도 제주시 첨단로 541, 16층 20호 / 설치일 : 2026.02.19 |
| end_time | end_time | 종료시각 | text | 오후 3시 40분 |
| minutes_date | minutes_date | 작성일 | date | 2026년 1월 21일 |
| company_name | corp.name | 상호 | text | (주)유니온무역 |
| head_office | head_office | 본점 | text | 서울특별시 중구 다산로 361, 6층 |
| signers[].title | signers[].title | 자격 | text | 의장 대표이사 |
| signers[].name | signers[].name | 성명 | text | 박찬연 |
| seal.corp | seal.corp | 법인인감 | seal | 주식회사 유니온무역 대표이사인 |
| seal.signer2 | seal.signer2 | 서명인2 | seal | 조태재 |
| seal.signer3 | seal.signer3 | 서명인3 | seal | 선옥도 |
| seal.signer4 | seal.signer4 | 서명인4 | seal | 길성은 |
| seal.signer5 | seal.signer5 | 서명인5 | seal | 표진하 |
| remote_count | remote_count | 원격참석 | text | 원격 참석 2명 포함 |
| remote_attendees | remote_attendees | 원격참석이사 | text | 사내이사 김준아, 사내이사 허지태 |
| remote_method | remote_method | 원격참석방법 | text | 화상회의, Zoom |
| signers[].remote | signers[].remote | 비고 | text | (원격 참석) |
| agendas[].votes | agendas[].votes | 표결결과 | text | 찬성 2명, 반대 1명 (사내이사 김호희) |
| notary.reg_no | notary.reg_no | 등부번호 | text | 2026년 제331호 |
| notary.date | notary.date | 인증일 | date | 2026년 4월 13일 |
| notary.office | notary.office | 공증인 | text | 법무법인 해송 |
| notary.lawyer | notary.lawyer | 공증담당변호사 | text | 이형윤 |
| seal.notary | seal.notary | 공증인직인 | seal | 공증인 |

연결 업무 corporate_credit · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### shareholders_meeting_minutes · 임시주주총회의사록

그룹: 법인 (`corporate`)

임시(또는 정기)주주총회의사록 (이사 선임 / 정관 변경 등).  주주 구성은 _facts 와 같다(자기주식은 의결권 없음). heavy: 안건 4~7개 + 출석주주 명단(주주가 많으면 여러 쪽). special: annual 정기주주총회(재무제표 승인·배당), dissent 반대 주식수 기재, proxy 위임장에 의한 대리출석, notarized 공증인 인증, seal_missing 일부 이사 날인 누락.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| meeting_title | meeting_title | 의사록종류 | text | 임시주주총회의사록 |
| datetime | datetime | 일시 | text | 2026년 1월 16일 오후 4시 30분 |
| venue | venue | 장소 | text | 본점 대회의실 (서울특별시 중구 다산로 361, 6층) |
| shareholders_total | shareholders_total | 주주의총수 | text | 3명 |
| issued_shares | issued_shares | 발행주식의총수 | text | 10,000주 |
| shareholders_present | shareholders_present | 출석주주의수 | text | 3명 |
| shares_present | shares_present | 출석주주의주식수 | text | 10,000주 |
| present_ratio | present_ratio | 출석비율 | percent | 100.00% |
| chair | chair | 의장 | text | 박찬연 |
| agendas[].no | agendas[].no | 의안번호 | text | 제1호 의안 |
| agendas[].title | agendas[].title | 의안 | text | 이사 선임의 건 |
| agendas[].body | agendas[].body | 결의내용 | text | 의장은 사내이사 조태재의 임기가 만료됨에 따라 이사를 선임할 필요가 있음을 설명하고 동인을 사내이사로 중임할 것을 물은바, 출석주주 전원의 찬성으로 이를 승인 가결하다. 피선임자는 즉석에서 그 취임을 승낙하다. |
| agendas[].detail | agendas[].detail | 세부내용 | text | 사내이사  조태재 (1985년 3월 8일생)  중임 |
| end_time | end_time | 종료시각 | text | 오후 5시 26분 |
| minutes_date | minutes_date | 작성일 | date | 2026년 1월 16일 |
| company_name | corp.name | 상호 | text | (주)유니온무역 |
| head_office | head_office | 본점 | text | 서울특별시 중구 다산로 361, 6층 |
| signers[].title | signers[].title | 자격 | text | 의장 대표이사 |
| signers[].name | signers[].name | 성명 | text | 박찬연 |
| seal.corp | seal.corp | 법인인감 | seal | 주식회사 유니온무역 대표이사인 |
| seal.signer2 | seal.signer2 | 서명인2 | seal | 김준아 |
| seal.signer3 | seal.signer3 | 서명인3 | seal | 황보형아 |
| proxy_count | proxy_count | 대리출석 | text | 위임장에 의한 대리출석 1명 포함 |
| treasury_shares | treasury_shares | 자기주식수 | text | 60,649주 |
| attendees[].name | attendees[].name | 주주명 | text | 이욱유 |
| attendees[].shares | attendees[].shares | 소유주식수 | number | 775,624 |
| attendees[].method | attendees[].method | 출석구분 | text | 본인출석 |
| attendees[].proxy | attendees[].proxy | 대리인 | text | 정우승 (대리인) |
| notary.reg_no | notary.reg_no | 등부번호 | text | 2025년 제3341호 |
| notary.date | notary.date | 인증일 | date | 2025년 4월 18일 |
| notary.office | notary.office | 공증인 | text | 법무법인 정명 |
| notary.lawyer | notary.lawyer | 공증담당변호사 | text | 설소서 |
| seal.notary | seal.notary | 공증인직인 | seal | 공증인 |
| seal.signer4 | seal.signer4 | 서명인4 | seal | 김수예 |
| agendas[].votes | agendas[].votes | 표결결과 | text | 찬성 48,998주, 반대 11,002주 |

### power_of_attorney · 위임장

그룹: 법인 (`corporate`)

은행 여신거래 관련 위임장 (법인 또는 개인 위임인).

연결 업무: 법인 여신 (corporate_credit)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| agent.name | agent.name | 성명 | text | 구은태 |
| agent.birth | agent.birth | 생년월일 | date | 1976.10.04 |
| agent.relation | agent.relation | 본인과의관계 | text | 직원 (회계팀 과장) |
| agent.phone | agent.phone | 연락처 | phone | 010-5160-1926 |
| agent.address | agent.address | 주소 | text | 서울특별시 노원구 노원로 458-26, 112동 1904호 (하계동, 호반베르디움퍼스트) |
| tasks[] | tasks[] | 위임내용 | text | 1. 기업은행 범어지점 여신(대출) 기한연장 신청 및 관련 서류 제출 일체 |
| period | period | 위임기간 | text | 2026.01.31 ~ 2026.03.02 |
| grant_date | grant_date | 작성일 | date | 2026년 01월 31일 |
| grantor.type | grantor.type | 위임인구분 | checkbox | 법인 |
| grantor.name | related.name | 상호 | text | (주)유니온무역 |
| grantor.ceo | grantor.ceo | 대표자 | text | 박찬연 |
| grantor.biz_no | grantor.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| grantor.corp_reg_no | grantor.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| grantor.address | related.address | 본점소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| grantor.phone | related.phone | 연락처 | phone | 02-9508-6789 |
| seal.corp | seal.corp | 법인인감 | seal | 주식회사 유니온무역 대표이사인 |
| attachment | attachment | 첨부서류 | text | 법인인감증명서 1부 |
| recipient | recipient | 제출처 | text | 기업은행 범어지점 귀중 |
| sub_delegation | sub_delegation | 복대리인선임 | checkbox | 불허 |
| grantor.birth | grantor.birth | 생년월일 | date | 1966년 08월 12일 |
| seal.grantor | seal.related | 위임인 | seal | 현예지 |
| tasks_extra | tasks_extra | 위임내용 | text | 4. 통장 및 OTP 재발급 신청·수령 |
| use_limit | use_limit | 사용제한 | text | 본 위임장은 위 업무 1회에 한하여 유효함 |

연결 업무 corporate_credit · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### resident_registration_copy · 주민등록표 등본

그룹: 가족관계 (`family`)

주민등록표 등본 (세대 전체). 부모·형제 동거, 세대주 변경, 동거인, 과거 주소 변동 포함 발급 등.

연결 업무: 주택담보대출 (mortgage), 전세자금대출 (jeonse_loan)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| doc_no | doc_no | 문서확인번호 | text | 제 1639 호 |
| officer | officer | 담당자 | text | 양경예 |
| officer_phone | officer_phone | 전화 | phone | 02-4484-9569 |
| applicant | applicant | 신청인 | text | 박찬연 |
| purpose | purpose | 용도및목적 | text | 대출신청 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 서울특별시 서초구 방배동장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 직인 |
| household_head.name | household_head.name | 세대주성명 | text | 박영준 |
| household_head.name_hanja | household_head.name_hanja | 세대주성명(한자) | text | 朴英準 |
| household_formed.reason | household_formed.reason | 세대구성사유 | text | 전입세대구성 |
| household_formed.date | household_formed.date | 세대구성일자 | date | 2007-07-23 |
| past_addresses[].no | past_addresses[].no | 번호 | number | 1 |
| past_addresses[].address | past_addresses[].address | 주소 | text | 서울특별시 송파구 올림픽로 273 (방이동) |
| past_addresses[].moved_in | past_addresses[].moved_in | 전입일/변동일 | date | 1983-06-20 |
| past_addresses[].reason | past_addresses[].reason | 변동사유 | text | 전입 |
| current_address.address | customer.address | 현주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| current_address.moved_in | current_address.moved_in | 전입일/변동일 | date | 2007-07-23 |
| current_address.reason | current_address.reason | 변동사유 | text | 전입 |
| members[].no | members[].no | 번호 | number | 1 |
| members[].relation | members[].relation | 세대주관계 | text | 본인 |
| members[].name | members[].name | 성명 | text | 박영준 |
| members[].name_hanja | members[].name_hanja | 한자 | text | 朴英準 |
| members[].moved_in | members[].moved_in | 전입일/변동일 | date | 2007-07-23 |
| members[].reason | members[].reason | 변동사유 | text | 전입 |
| members[].rrn | members[].rrn | 주민등록번호 | rrn | 621219-1****** |

연결 업무 mortgage · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 jeonse_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### resident_registration_abstract · 주민등록표 초본

그룹: 가족관계 (`family`)

주민등록표 초본 (개인 인적사항 + 주소 변동 이력). 이사가 잦은 사람은 여러 쪽이 된다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| doc_no | doc_no | 문서확인번호 | text | 6319-1340-7703-9808 |
| applicant | applicant | 신청인 | text | 박찬연 |
| purpose | purpose | 용도및목적 | text | 금융기관제출 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 서울특별시 서초구청장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 직인 |
| person.name | customer.name | 성명 | text | 박찬연 |
| person.name_hanja | customer.name_hanja | 한자 | text | 朴讚姸 |
| person.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| history_scope | history_scope | 주소변동사항 | text | 최근 5년 |
| addresses[].no | addresses[].no | 번호 | number | 1 |
| addresses[].address | addresses[].address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| addresses[].moved_in | addresses[].moved_in | 전입일 | date | 2018-10-20 |
| addresses[].changed | addresses[].changed | 변동일 | date | 2018-10-20 |
| addresses[].head_relation | addresses[].head_relation | 세대주및관계 | text | 박영준의 자 |
| addresses[].status | addresses[].status | 등록상태 | text | 거주자 |
| addresses[].reason | addresses[].reason | 변동사유 | text | 전입 |
| officer | officer | 담당자 | text | 서규은 |
| officer_phone | officer_phone | 전화 | phone | 02-4755-9378 |
| person_changes[].no | person_changes[].no | 번호 | number | 1 |
| person_changes[].content | person_changes[].content | 변경내용 | text | 성명 이태린(李泰麟) → 이민빈(李旻彬) |
| person_changes[].changed | person_changes[].changed | 변동일 | date | 1997-04-13 |
| person_changes[].reason | person_changes[].reason | 변동사유 | text | 개명 |

### family_relation_certificate · 가족관계증명서

그룹: 가족관계 (`family`)

가족관계증명서 (일반/상세). 사망한 부모, 전혼 자녀, 입양(친생부모) 등.

연결 업무: 주택담보대출 (mortgage), 유학생 송금 (study_abroad_remittance), 상속예금 지급 (inheritance)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| cert_type | cert_type | 증명서종류 | text | 일반 |
| reg_base | reg_base | 등록기준지 | text | 서울특별시 종로구 평창동 851-12 |
| self.relation | customer.relation | 구분 | text | 본인 |
| self.name | customer.name | 성명 | text | 박찬연 |
| self.name_hanja | customer.name_hanja | 성명(한자) | text | 朴讚姸 |
| self.birth | customer.birth | 출생연월일 | date | 1990년 02월 10일 |
| self.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| self.gender | customer.gender | 성별 | text | 남 |
| self.bon | customer.bon | 본 | text | 密陽 |
| family[].relation | family[].relation | 구분 | text | 부 |
| family[].name | family[].name | 성명 | text | 박영준 |
| family[].name_hanja | family[].name_hanja | 성명(한자) | text | 朴英準 |
| family[].birth | family[].birth | 출생연월일 | date | 1962년 12월 19일 |
| family[].rrn | family[].rrn | 주민등록번호 | rrn | 621219-1****** |
| family[].gender | family[].gender | 성별 | text | 남 |
| family[].bon | family[].bon | 본 | text | 密陽 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 법원행정처 전산정보중앙관리소 전산운영책임관 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 전산운영책임관인 |
| issue_time | issue_time | 발급시각 | text | 16시 15분 |
| applicant | applicant | 신청인 | text | 박찬연 |
| doc_check_no | doc_check_no | 문서확인번호 | text | 4446-8180-3034-4028 |
| officer | officer | 발급담당자 | text | 최정주 |
| officer_phone | officer_phone | 전화 | phone | 02-6654-0284 |
| family[].status | family[].status | 사망 | text | 사망 |
| family[].nationality | family[].nationality | 국적 | text | 중국 |

연결 업무 mortgage · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 study_abroad_remittance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 inheritance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### basic_certificate · 기본증명서

그룹: 가족관계 (`family`)

기본증명서 (일반/상세). 상세에는 개명·국적취득·성별정정 기록이 나온다.

연결 업무: 상속예금 지급 (inheritance)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| cert_type | cert_type | 증명서종류 | text | 상세 |
| reg_base | reg_base | 등록기준지 | text | 서울특별시 종로구 평창동 851-12 |
| self.relation | customer.relation | 구분 | text | 본인 |
| self.name | customer.name | 성명 | text | 박찬연 |
| self.name_hanja | customer.name_hanja | 성명(한자) | text | 朴讚姸 |
| self.birth | customer.birth | 출생연월일 | date | 1990년 02월 10일 |
| self.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| self.gender | customer.gender | 성별 | text | 남 |
| self.bon | customer.bon | 본 | text | 密陽 |
| birth.place | birth.place | 출생장소 | text | 부산광역시 부산진구 전포동 |
| birth.reported | birth.reported | 신고일 | date | 1990년 02월 24일 |
| birth.reporter | birth.reporter | 신고인 | text | 모 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 법원행정처 전산정보중앙관리소 전산운영책임관 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 전산운영책임관인 |
| issue_time | issue_time | 발급시각 | text | 06시 20분 |
| applicant | applicant | 신청인 | text | 박찬연 |
| doc_check_no | doc_check_no | 문서확인번호 | text | 8334-0642-5397-9222 |
| officer | officer | 발급담당자 | text | 채선원 |
| officer_phone | officer_phone | 전화 | phone | 055-748-8832 |
| name_change.permitted | name_change.permitted | 개명허가일 | date | 1997년 03월 26일 |
| name_change.court | name_change.court | 허가법원 | text | 서울가정법원 |
| name_change.old_name | name_change.old_name | 개명전이름 | text | 이태린 |
| name_change.reported | name_change.reported | 신고일 | date | 1997년 04월 13일 |
| naturalization.acquired | naturalization.acquired | 국적취득일 | date | 2008년 11월 04일 |
| naturalization.reason | naturalization.reason | 국적취득사유 | text | 귀화허가 |
| naturalization.prev_nationality | naturalization.prev_nationality | 종전국적 | text | 중국 |
| naturalization.notified | naturalization.notified | 통보일 | date | 2008년 11월 11일 |
| naturalization.notifier | naturalization.notifier | 통보자 | text | 법무부장관 |
| correction.permitted | correction.permitted | 정정허가일 | date | 2013년 02월 21일 |
| correction.court | correction.court | 허가법원 | text | 서울가정법원 |
| correction.content | correction.content | 정정내용 | text | 성별 여 → 남 |
| correction.reported | correction.reported | 신고일 | date | 2013년 02월 24일 |

연결 업무 inheritance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### marriage_relation_certificate · 혼인관계증명서

그룹: 가족관계 (`family`)

혼인관계증명서 (일반/상세). 일반은 현재 혼인만, 상세는 이혼한 혼인(외국인 배우자 포함)까지 표시.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| cert_type | cert_type | 증명서종류 | text | 일반 |
| reg_base | reg_base | 등록기준지 | text | 서울특별시 종로구 평창동 851-12 |
| self.relation | customer.relation | 구분 | text | 본인 |
| self.name | customer.name | 성명 | text | 박찬연 |
| self.name_hanja | customer.name_hanja | 성명(한자) | text | 朴讚姸 |
| self.birth | customer.birth | 출생연월일 | date | 1990년 02월 10일 |
| self.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| self.gender | customer.gender | 성별 | text | 남 |
| self.bon | customer.bon | 본 | text | 密陽 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 서울특별시 서초구청장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 직인 |
| issue_time | issue_time | 발급시각 | text | 09시 13분 |
| officer | officer | 발급담당자 | text | 황숙율 |
| officer_phone | officer_phone | 전화 | phone | 02-598-1196 |
| applicant | applicant | 신청인 | text | 박찬연 |
| spouse.relation | spouse.relation | 구분 | text | 배우자 |
| spouse.name | family.name | 성명 | text | 이도민 |
| spouse.name_hanja | spouse.name_hanja | 성명(한자) | text | 李度民 |
| spouse.birth | spouse.birth | 출생연월일 | date | 1967년 09월 21일 |
| spouse.rrn | spouse.rrn | 주민등록번호 | rrn | 670921-1882767 |
| spouse.gender | spouse.gender | 성별 | text | 남 |
| spouse.bon | spouse.bon | 본 | text | 廣州 |
| marriage.reported | marriage.reported | 신고일 | date | 1995년 05월 07일 |
| marriage.spouse_name | marriage.spouse_name | 배우자 | text | 이도민 |
| marriage.spouse_rrn | marriage.spouse_rrn | 배우자의주민등록번호 | rrn | 670921-1882767 |
| marriage.office | marriage.office | 처리관서 | text | 서울특별시 송파구 |
| doc_check_no | doc_check_no | 문서확인번호 | text | 5542-8548-2400-0602 |
| past_events[].kind | past_events[].kind | 구분 | text | 혼인 |
| past_events[].reported | past_events[].reported | 신고일 | date | 2014년 04월 09일 |
| past_events[].spouse_name | past_events[].spouse_name | 배우자 | text | 이바노바안나(IVANOVA ANNA) |
| past_events[].spouse_nationality | past_events[].spouse_nationality | 배우자국적 | text | 러시아 |
| past_events[].spouse_birth | past_events[].spouse_birth | 배우자의출생연월일 | date | 1991년 01월 11일 |
| past_events[].office | past_events[].office | 처리관서 | text | 서울특별시 송파구 |
| past_events[].judgment_date | past_events[].judgment_date | 이혼판결확정일 | date | 2008년 04월 30일 |
| past_events[].court | past_events[].court | 법원 | text | 수원가정법원 |

### employment_certificate · 재직증명서

그룹: 소득·재직 (`income`)

회사가 발급하는 재직증명서 (근로기준법 제39조 사용증명서, 법정서식 없음 — 통용 양식).  통용 양식: 문서번호 / 인적사항(성명·주민등록번호(또는 생년월일)·주소) / 재직사항(회사명·사업자등록번호· 소재지·소속·직위·재직기간·담당업무) / 용도·제출처 / 증명 문구 / 발급일 / 회사명·대표이사 (직인).

연결 업무: 개인 계좌개설 (account_opening), 개인 신용대출 (personal_credit_loan), 전세자금대출 (jeonse_loan), 개인형IRP 개설 (irp_opening), 퇴직급여 수령 (retirement_payout)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | employer.name | 회사명 | text | 주식회사 태평양무역 |
| company.address | employer.address | 소재지 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 |
| company.phone | employer.phone | 전화번호 | phone | 043-783-2775 |
| company.biz_no | company.biz_no | 사업자등록번호 | biz_no | 501-82-42625 |
| doc_no | doc_no | 문서번호 | text | 제 2026-145 호 |
| employee.name | customer.name | 성명 | text | 박찬연 |
| employee.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| employee.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| employment.department | employer.department | 소속 | text | 구매팀 |
| employment.position | employer.position | 직위 | text | 대리 |
| employment.period | employer.period | 재직기간 | text | 2020.05.08 ~ 현재 |
| employment.duty | employment.duty | 담당업무 | text | 자재 구매 및 협력사 관리 |
| purpose | purpose | 용도 | text | 금융기관 제출용 |
| submit_to | submit_to | 제출처 | text | 기업은행 |
| issue_date | issue_date | 발급일 | date | 2026년 1월 31일 |
| company.ceo | company.ceo | 대표이사 | text | 공정태 |
| seal.company | seal.company | 회사직인 | seal | 대표이사인 |
| employee.birth | customer.birth | 생년월일 | date | 1994.09.26 |
| employment.employment_type | employment.employment_type | 고용형태 | text | 계약직(기간제) |
| employment.contract_period | employment.contract_period | 계약기간 | text | 2026.05.27 ~ 2027.05.26 |
| employment.leave | employment.leave | 휴직기간 | text | 2013.04.01 ~ 2013.09.30 (육아휴직) |
| employment.annual_salary | employment.annual_salary | 급여(연봉) | amount | 54,600,000원 |

연결 업무 account_opening · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 personal_credit_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 jeonse_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 irp_opening · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 retirement_payout · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### career_certificate · 경력증명서

그룹: 소득·재직 (`income`)

현 직장이 발급하는 경력증명서 (근로기준법 제39조 사용증명서, 통용 양식: 인적사항 / 경력사항 (근무기간·근무부서·직위·담당업무) / 총 근무기간 / 용도·제출처 / 증명 문구 / 회사 정보·대표이사 직인).

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| doc_no | doc_no | 문서번호 | text | 제 2026-837 호 |
| person.name | customer.name | 성명 | text | 박찬연 |
| person.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1****** |
| person.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| person.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| hire_date | hire_date | 입사일 | date | 2020년 05월 08일 |
| careers[].period | careers[].period | 근무기간 | text | 2020년 05월 08일 ~ 2021년 12월 31일 |
| careers[].department | careers[].department | 근무부서 | text | 구매팀 |
| careers[].position | careers[].position | 직위 | text | 사원 |
| careers[].duty | careers[].duty | 담당업무 | text | 자재 구매 및 협력사 관리 |
| total_period | total_period | 총근무기간 | text | 5년 8개월 |
| purpose | purpose | 용도 | text | 대출 신청용 |
| submit_to | submit_to | 제출처 | text | 기업은행 |
| issue_date | issue_date | 발급일 | date | 2026년 1월 31일 |
| company.name | employer.name | 회사명 | text | 주식회사 태평양무역 |
| company.biz_no | company.biz_no | 사업자등록번호 | biz_no | 501-82-42625 |
| company.address | employer.address | 소재지 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 |
| company.phone | employer.phone | 전화번호 | phone | 043-783-2775 |
| company.ceo | company.ceo | 대표이사 | text | 공정태 |
| seal.company | seal.company | 회사직인 | seal | 대표이사인 |

### pay_stub · 급여명세서

그룹: 소득·재직 (`income`)

임금명세서 (근로기준법 제48조제2항, 시행령 제27조의2 — 고용노동부 임금명세서 표준 예시 구조).  지급일 / 성명·생년월일·사번·부서·직급 / 세부내역(매월 지급 · 격월 또는 부정기 지급 / 공제) / 지급액 계·공제액 계·실수령액 / 근로일수·근로시간수·통상시급 / 계산방법(산출식 또는 산출방법).

연결 업무: 개인 신용대출 (personal_credit_loan)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| doc_title | doc_title | 서식명 | text | 급여명세서 |
| title_month | title_month | 귀속연월 | text | 2026년 01월분 |
| company | company | 회사명 | text | 주식회사 태평양무역 |
| pay_date | pay_date | 지급일 | date | 2026-01-25 |
| employee.name | customer.name | 성명 | text | 박찬연 |
| employee.birth | customer.birth | 생년월일 | date | 1990-02-10 |
| employee.employee_no | employee.employee_no | 사번 | text | B88222 |
| employee.department | employee.department | 부서 | text | 구매팀 |
| employee.position | employee.position | 직급 | text | 대리 |
| payments[].name | payments[].name | 임금항목 | text | 기본급 |
| payments[].amount | payments[].amount | 지급금액 | amount | 4,350,000 |
| deductions[].name | deductions[].name | 공제항목 | text | 국민연금 |
| deductions[].amount | deductions[].amount | 공제금액 | amount | 206,620 |
| pay_total | pay_total | 지급액계 | amount | 5,174,390 |
| deduction_total | deduction_total | 공제액계 | amount | 807,590 |
| net_pay | net_pay | 실수령액 | amount | 4,366,800 |
| work.days | work.days | 근로일수 | number | 22 |
| work.hours | work.hours | 총근로시간수 | number | 196 |
| work.overtime_hours | work.overtime_hours | 연장근로시간수 | number | 20 |
| work.night_hours | work.night_hours | 야간근로시간수 | number | 0 |
| work.holiday_hours | work.holiday_hours | 휴일근로시간수 | number | 0 |
| work.hourly_wage | work.hourly_wage | 통상시급(원) | amount | 20,813 |
| work.family | work.family | 가족수 | text | - |
| calc_methods[].item | calc_methods[].item | 구분 | text | 연장근로수당 |
| calc_methods[].method | calc_methods[].method | 산출식또는산출방법 | text | 20시간 × 20,813원 × 1.5 |
| calc_methods[].amount | calc_methods[].amount | 금액(원) | amount | 624,390 |
| payments_irregular[].name | payments_irregular[].name | 임금항목 | text | 명절상여금 |
| payments_irregular[].amount | payments_irregular[].amount | 지급금액 | amount | 1,570,830 |

연결 업무 personal_credit_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### employment_contract · 근로계약서

그룹: 소득·재직 (`income`)

고용노동부 표준근로계약서 (기간의 정함이 없는 경우) — 1.근로개시일 ~ 11.기타, 사업주·근로자 서명.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| employer.name | employer.name | 사업주 | text | 주식회사 태평양무역 |
| employee.name | customer.name | 근로자 | text | 박찬연 |
| start_date | start_date | 근로개시일 | date | 2020년 5월 8일 |
| workplace | workplace | 근무장소 | text | 주식회사 태평양무역 본사 |
| job | job | 업무의내용 | text | 구매팀 자재 구매 및 협력사 관리 |
| work_start | work_start | 소정근로시간 | text | 09시 00분 |
| work_end | work_end | 소정근로시간 | text | 18시 00분 |
| break_time | break_time | 휴게시간 | text | 12시 00분 ~ 13시 00분 |
| work_days | work_days | 근무일 | number | 5 |
| weekly_holiday | weekly_holiday | 주휴일 | text | 일 |
| monthly_salary | monthly_salary | 월(일,시간)급 | amount | 3,700,000 |
| bonus | bonus | 상여금 | text | 있음 |
| bonus_amount | bonus_amount | 상여금 | amount | 3,500,000 |
| other_pay | other_pay | 기타급여 | text | 있음 |
| allowances[].name | allowances[].name | 기타급여(제수당등) | text | 식대 |
| allowances[].amount | allowances[].amount | 기타급여(제수당등) | amount | 200,000원 |
| pay_day | pay_day | 임금지급일 | amount | 25 |
| pay_method | pay_method | 지급방법 | text | 근로자 명의 예금통장에 입금 |
| special_terms[] | special_terms[] | 특약사항 | text | 회사가 지급한 노트북 등 업무용 장비는 퇴직 시 즉시 반납한다. |
| contract_date | contract_date | 계약일 | date | 2020년 5월 7일 |
| employer.phone | employer.phone | 전화 | phone | 043-783-2775 |
| employer.address | employer.address | 주소 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 |
| employer.ceo | employer.ceo | 대표자 | text | 공정태 |
| seal.employer | seal.employer | 사용자 | seal | 대표이사인 |
| employee.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| employee.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| seal.employee | seal.customer | 근로자 | seal | 박찬연 |
| sign.employee | sign.customer | 근로자 | signature | 현예지 |
| end_date | end_date | 근로계약종료일 | date | 2020년 05월 27일 |
| probation.period | probation.period | 수습기간 | text | 2014년 12월 01일 ~ 2015년 02월 28일 (3개월) |
| probation.wage_rate | probation.wage_rate | 수습기간임금지급률 | percent | 100% |

### withholding_receipt · 근로소득 원천징수영수증

그룹: 소득·재직 (`income`)

근로소득 원천징수영수증(근로소득 지급명세서) 제1쪽 — 소득세법 시행규칙 [별지 제24호서식(1)].  제1쪽 구성: 관리번호·영수증/지급명세서 구분·보관용 구분 / 거주구분 등 / 징수의무자 ①~⑤ / 소득자 ⑥~⑧ / Ⅰ 근무처별 소득명세 ⑨~⑯ / Ⅱ 비과세 및 감면 소득 명세 / Ⅲ 세액명세 (72)~(76)·실효세율 / 영수 문구·서명. (정산명세 ㉑~ 는 제2쪽이라 표시하지 않는다.)

연결 업무: 개인 신용대출 (personal_credit_loan)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| copy_type | copy_type | 보관용구분 | checkbox | 소득자 보관용 |
| year | year | 귀속연도 | number | 2024 |
| resident | resident | 거주구분 | checkbox | 거주자1 |
| nationality | customer.nationality | 내·외국인 | checkbox | 내국인1 |
| household_head | household_head | 세대주여부 | checkbox | 세대주1 |
| settlement_type | settlement_type | 연말정산구분 | checkbox | 계속근로1 |
| payer.name | customer.name | 법인명(상호) | text | 주식회사 태평양무역 |
| payer.ceo | customer.ceo | 대표자(성명) | text | 공정태 |
| payer.biz_no | customer.biz_no | 사업자등록번호 | biz_no | 501-82-42625 |
| payer.address | customer.address | 소재지(주소) | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 |
| earner.name | earner.name | 성명 | text | 박찬연 |
| earner.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| earner.address | earner.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| work.company | work.company | 근무처명 | text | 주식회사 태평양무역 |
| work.biz_no | work.biz_no | 사업자등록번호 | biz_no | 501-82-42625 |
| work.period | employer.period | 근무기간 | text | 2024.01.01~2024.12.31 |
| work.salary | work.salary | 급여 | amount | 40,800,000 |
| work.bonus | work.bonus | 상여 | amount | 7,770,000 |
| work.total | work.total | 계 | amount | 48,570,000 |
| nontax.meal | nontax.meal | 식사대 | number | 2,400,000 |
| nontax.total | nontax.total | 비과세소득계 | amount | 2,400,000 |
| tax.final_income | tax.final_income | 결정세액 | amount | 2,257,830 |
| tax.final_local | tax.final_local | 결정세액 | number | 225,780 |
| tax.prepaid_income | tax.prepaid_income | 주(현)근무지 | amount | 2,628,600 |
| tax.prepaid_local | tax.prepaid_local | 주(현)근무지 | number | 262,860 |
| tax.diff_income | tax.diff_income | 차감징수세액 | amount | -370,770 |
| tax.diff_local | tax.diff_local | 차감징수세액 | number | -37,080 |
| tax.effective_rate | tax.effective_rate | 실효세율(%) | number | 4.6 |
| issue_date | issue_date | 발급일 | date | 2025년 02월 28일 |
| seal.payer | seal.customer | 징수의무자 | seal | 대표이사인 |
| tax_office | tax_office | 세무서장 | text | 청주세무서장 |
| work_prev.company | work_prev.company | 종(전)근무처명 | text | 주식회사 코리아파트너스 |
| work_prev.biz_no | work_prev.biz_no | 종(전)사업자등록번호 | biz_no | 558-18-39130 |
| work_prev.period | work_prev.period | 종(전)근무기간 | text | 2023.03.01~2023.05.31 |
| work.reduction_period | work.reduction_period | 감면기간 | text | 2019.02.22~2024.02.21 |
| work_prev.salary | work_prev.salary | 종(전)급여 | amount | 2,920,000 |
| work_sum.salary | work_sum.salary | 급여합계 | amount | 40,190,000 |
| work_prev.bonus | work_prev.bonus | 종(전)상여 | amount | 0 |
| work_sum.bonus | work_sum.bonus | 상여합계 | amount | 0 |
| work_prev.total | work_prev.total | 종(전)계 | amount | 2,920,000 |
| work_sum.total | work_sum.total | 계합계 | amount | 40,190,000 |
| work_sum.meal | work_sum.meal | 식사대합계 | number | 2,400,000 |
| nontax.reduction | nontax.reduction | 감면소득계 | number | 37,270,000 |
| tax_prev.biz_no | tax_prev.biz_no | 종(전)근무지사업자등록번호 | biz_no | 558-18-39130 |
| tax_prev.income | tax_prev.income | 종(전)근무지기납부소득세 | amount | 0 |
| tax_prev.local | tax_prev.local | 종(전)근무지기납부지방소득세 | number | 0 |
| work_prev.meal | work_prev.meal | 종(전)식사대 | number | 1,000,000 |
| nontax.childcare | nontax.childcare | 출산·보육수당 | number | 2,400,000 |

연결 업무 personal_credit_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### income_certificate · 소득금액증명원

그룹: 소득·재직 (`income`)

국세청(홈택스) 발급 소득금액증명.  2022.9.22. 서식 개정으로 종전 5종(종합소득세 신고자용·근로소득자용 등)이 1종으로 통합되어, '종합소득세 신고 현황'(소득구분별 수입금액·소득금액)과 '연말정산 현황'(원천징수의무자별 소득금액(과세대상급여액)·총결정세액)을 한 장에 표시한다.

연결 업무: 개인 신용대출 (personal_credit_loan), 주택담보대출 (mortgage), 전세자금대출 (jeonse_loan), 개인사업자 대출 (sole_proprietor_loan)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| issue_no | issue_no | 발급번호 | text | 2145-532-2462-517 |
| taxpayer.name | customer.name | 성명(대표자) | text | 박찬연 |
| taxpayer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| taxpayer.address | customer.address | 주소(사업장소재지) | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| period | period | 증명기간 | text | 2024년 |
| rows[].year | rows[].year | 귀속연도 | number | 2024 |
| rows[].income_type | rows[].income_type | 소득구분 | text | 근로 |
| rows[].payer | rows[].payer | 법인명(상호) | text | 주식회사 태평양무역 |
| rows[].payer_biz_no | rows[].payer_biz_no | 사업자등록번호 | biz_no | 501-82-42625 |
| rows[].amount | rows[].amount | 소득금액(과세대상급여액) | amount | 48,570,000 |
| rows[].tax | rows[].tax | 총결정세액 | amount | 2,257,830 |
| purpose | purpose | 용도 | text | 은행 제출용 |
| submit_to | submit_to | 제출처 | text | 기업은행 |
| issue_date | issue_date | 발급일 | date | 2026년 1월 31일 |
| issuer | issuer | 발급기관 | text | 서초세무서장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 서초세무서장인 |
| filing_rows[].year | filing_rows[].year | 귀속연도 | number | 2024 |
| filing_rows[].income_type | filing_rows[].income_type | 소득구분 | text | 근로 |
| filing_rows[].revenue | filing_rows[].revenue | 수입금액 | amount | 46,390,000 |
| filing_rows[].income | filing_rows[].income | 소득금액 | amount | 34,320,500 |

연결 업무 personal_credit_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 mortgage · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 jeonse_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 sole_proprietor_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### pension_enrollment_certificate · 국민연금 가입자 가입증명

그룹: 소득·재직 (`income`)

국민연금공단 발급 가입자 가입증명 — 국민연금법 시행규칙 [별지 제11호서식] 국민연금가입자증명서.  □ 가입자의 인적사항(발급번호·발급일자·성명·주민등록번호) / □ 가입자의 종류 및 자격 취득일 (최초 자격취득일, 가입자 종류·사업장명칭·자격취득일·자격상실일) / 증명 문구 / 국민연금공단 이사장.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| issue_no | issue_no | 발급번호 | text | 20260131-21521346 |
| issue_date_head | issue_date_head | 발급일자 | date | 2026.01.31 |
| person.name | customer.name | 성명 | text | 박찬연 |
| person.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| first_acquired | first_acquired | 최초자격취득일 | date | 2018.03.15 |
| total_months | total_months | 가입기간합계 | text | 88개월 |
| rows[].kind | rows[].kind | 가입자종류 | text | 사업장가입자 |
| rows[].workplace | rows[].workplace | 사업장명칭 | text | (주)우진오토텍 |
| rows[].start | rows[].start | 자격취득일 | date | 2018.03.15 |
| rows[].end | rows[].end | 자격상실일 | date | 2019.11.15 |
| rows[].wage | rows[].wage | 기준소득월액 | amount | 2,079,000 |
| rows[].note | rows[].note | 비고 | text | 납부예외(실직) |
| purpose | purpose | 용도 | text | 은행 제출용 |
| issue_date | issue_date | 발급일 | date | 2026년 1월 31일 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 국민연금공단이사장 |

### health_insurance_qualification · 건강보험 자격득실확인서

그룹: 소득·재직 (`income`)

국민건강보험공단 발급 건강보험 자격득실 확인서 (국민건강보험법 제11조 자격취득 등의 확인).  가입자구분(직장가입자·지역세대주·지역세대원·직장피부양자) / 사업장 명칭 / 자격취득일 / 자격상실일.

연결 업무: 개인 신용대출 (personal_credit_loan)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| issue_no | issue_no | 발급번호 | text | 3829-2859-3487-6640 |
| person.name | customer.name | 성명 | text | 박찬연 |
| person.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1****** |
| rows[].kind | rows[].kind | 가입자구분 | text | 직장피부양자 |
| rows[].start | rows[].start | 자격취득일 | date | 1990.02.10 |
| rows[].end | rows[].end | 자격상실일 | date | 2018.03.15 |
| rows[].workplace | rows[].workplace | 사업장명칭 | text | (주)우진오토텍 |
| purpose | purpose | 용도 | text | 기타 제출용 |
| issue_date | issue_date | 발급일 | date | 2026년 1월 31일 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 국민건강보험공단이사장인 |

연결 업무 personal_credit_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### health_insurance_payment · 건강보험료 납부확인서

그룹: 소득·재직 (`income`)

국민건강보험공단 발급 건강보험료 납부확인서 (직장가입자 본인부담분, 월별 고지·납부 보험료를 건강/장기요양 구분).

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| issue_no | issue_no | 발급번호 | text | 85-651171-2643 |
| person.name | customer.name | 성명 | text | 박찬연 |
| person.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| person.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| member_kind | member_kind | 가입자구분 | text | 직장가입자 |
| period | period | 대상기간 | text | 2023.08 ~ 2025.12 |
| workplace.name | employer.name | 사업장명칭 | text | 주식회사 태평양무역 |
| workplace.mgmt_no | workplace.mgmt_no | 사업장관리번호 | number | 50182426250 |
| workplace.address | employer.address | 소재지 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 |
| rows[].month | rows[].month | 년월 | month | 2023.08 |
| rows[].notice_health | rows[].notice_health | 고지보험료(건강보험) | number | 138,400 |
| rows[].notice_ltc | rows[].notice_ltc | 고지보험료(장기요양) | number | 17,720 |
| rows[].health | rows[].health | 납부보험료(건강보험) | number | 138,400 |
| rows[].ltc | rows[].ltc | 납부보험료(장기요양) | number | 17,720 |
| rows[].total | rows[].total | 납부보험료(계) | amount | 156,120 |
| rows[].paid_date | rows[].paid_date | 납부일자 | date | 2023.09.11 |
| sum.notice_health | sum.notice_health | 고지보험료(건강보험)합계 | number | 4,198,640 |
| sum.notice_ltc | sum.notice_ltc | 고지보험료(장기요양)합계 | number | 542,680 |
| sum.health | sum.health | 납부보험료(건강보험)합계 | number | 4,198,640 |
| sum.ltc | sum.ltc | 납부보험료(장기요양)합계 | number | 542,680 |
| sum.total | sum.total | 납부보험료(계)합계 | amount | 4,741,320 |
| purpose | purpose | 용도 | text | 기타 |
| issue_date | issue_date | 발급일 | date | 2026년 1월 31일 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 국민건강보험공단이사장인 |
| person.rrn | customer.rrn | 주민등록번호 | rrn | 660812-2****** |
| rows[].note | rows[].note | 비고 | text | 정산 분할 1/10회 |

### bankbook_copy · 통장사본

그룹: 금융거래 (`finance`)

예금통장 첫 면 사본 (스캔본 또는 인터넷 출력본).

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| bank | bank | 은행명 | text | 기업은행 |
| product | product | 상품명 | text | 저축예금 |
| seal.registered | seal.registered | 등록인감 | seal | 박찬연 |
| passbook_no | passbook_no | 통장번호 | number | 03 |
| account_no | account_no | 계좌번호 | account_no | 171-760452-29-611 |
| holder | holder | 예금주 | text | 박찬연 |
| opened | opened | 신규일 | date | 2014.06.11 |
| branch | branch | 지점명 | text | 여의도지점 |
| branch_phone | branch_phone | 지점전화번호 | phone | 02-3937-0125 |
| first_tx.date | first_tx.date | 거래일 | date | 2014.06.11 |
| first_tx.memo | first_tx.memo | 적요 | text | 신규 |
| first_tx.amount | first_tx.amount | 맡기신금액 | amount | 50,000 |
| first_tx.balance | first_tx.balance | 잔액 | amount | 50,000 |
| txs[].date | txs[].date | 거래일 | date | 2014.06.25 |
| txs[].memo | txs[].memo | 적요 | text | 모바일출금 |
| txs[].out | txs[].out | 찾으신금액 | number | 40,000 |
| txs[].balance | txs[].balance | 잔액 | amount | 10,000 |
| status | status | 계좌상태 | text | 해지 |
| closed_date | closed_date | 해지일 | date | 2014.08.01 |
| issue_date | issue_date | 출력일 | date | 2025.05.19 |
| txs[].in | txs[].in | 맡기신금액 | number | 2,151,600 |
| limit_note | limit_note | 계좌제한구분 | text | 금융거래한도계좌 |

### bank_statement · 거래내역확인서

그룹: 금융거래 (`finance`)

은행 발급 예금 거래내역확인서 (조회기간 거래 목록, 잔액 일관).  열 구성은 국내 은행 거래내역 통용 형식: 거래일시 / 적요(거래구분) / 기재내용(보낸분·받는분) / 찾으신금액 / 맡기신금액 / 거래후잔액.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| issue_no | issue_no | 발급번호 | text | 20260131-215660 |
| holder | holder | 예금주 | text | 박찬연 |
| birth | birth | 생년월일 | date | 1990.02.10 |
| account_no | account_no | 계좌번호 | account_no | 171-760452-29-611 |
| product | product | 상품명 | text | 저축예금 |
| period | period | 조회기간 | text | 2025.10.29 ~ 2026.01.30 |
| opening_balance | opening_balance | 조회기간전잔액 | amount | 52,145,840 |
| rows[].datetime | rows[].datetime | 거래일시 | datetime | 2025.11.15 10:54:57 |
| rows[].type | rows[].type | 적요 | text | 자동이체 |
| rows[].memo | rows[].memo | 기재내용 | text | 현대카드 |
| rows[].out | rows[].out | 찾으신금액 | number | 1,381,960 |
| rows[].balance | rows[].balance | 거래후잔액 | amount | 50,763,880 |
| rows[].in | rows[].in | 맡기신금액 | number | 3,847,280 |
| summary.count | summary.count | 거래건수 | text | 12건 |
| summary.out | summary.out | 찾으신금액합계 | number | 4,511,960 |
| summary.in | summary.in | 맡기신금액합계 | number | 12,380,699 |
| summary.balance | summary.balance | 최종잔액 | amount | 60,014,579 |
| issue_date | issue_date | 발급일 | date | 2026.01.31 |
| issuer | issuer | 발급점 | text | 기업은행 범어지점 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 범어지점장인 |
| overdraft_limit | overdraft_limit | 대출한도 | amount | 30,000,000 |

### balance_certificate · 잔액증명서

그룹: 금융거래 (`finance`)

은행 예금잔액증명서 (예금주·고객번호 / 과목·계좌번호·예금잔액·미결제타점권·질권·지급정지·압류 여부 / 합계).

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| cert_no | cert_no | 증명서번호 | text | 제 2026-58458 호 |
| holder.name | customer.name | 예금주 | text | 박찬연 |
| holder.rrn | customer.rrn | 고객번호(주민등록번호) | rrn | 900210-1****** |
| base_date | base_date | 기준일 | text | 2026년 01월 30일 현재 |
| rows[].kind | rows[].kind | 과목 | text | 보통예금 |
| rows[].account_no | rows[].account_no | 계좌번호 | account_no | 171-760452-29-611 |
| rows[].balance | rows[].balance | 예금잔액 | amount | 60,014,579 |
| rows[].uncleared | rows[].uncleared | 미결제타점권 | number | 0 |
| rows[].pledge | rows[].pledge | 질권 | text | 무 |
| rows[].restriction | rows[].restriction | 지급정지·압류·가압류 | text | 무 |
| currency | currency | 통화 | text | KRW |
| total | total | 합계 | amount | 62,714,579 |
| total_korean | total_korean | 합계금액(한글) | amount_korean | 금 육천이백칠십일만사천오백칠십구원정 |
| purpose | purpose | 용도 | text | 입찰 참가용 |
| issue_date | issue_date | 발급일 | date | 2026년 1월 31일 |
| issuer | issuer | 발급점 | text | 기업은행 범어지점장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 범어지점장인 |
| remarks[] | remarks[] | 비고 | text | 계좌번호 093-105-808241 : 질권설정 (질권자 : 서울보증보험(주), 설정금액 1,810,000원) |
| rows[].fx_amount | rows[].fx_amount | 외화잔액 | amount | EUR 2,307.87 |
| fx_rate | fx_rate | 매매기준율 | amount | EUR 1,589.39 |

### debt_certificate · 부채증명서

그룹: 금융거래 (`finance`)

은행 발급 부채증명서 (대출 잔액).

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| cert_no | cert_no | 증명서번호 | text | 제 2026-75909 호 |
| borrower.name | customer.name | 차주명 | text | 박찬연 |
| borrower.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1****** |
| borrower.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| base_date | base_date | 기준일 | text | 2026년 01월 30일 현재 |
| loans[].subject | loans[].subject | 대출과목 | text | 주택담보대출 |
| loans[].account_no | loans[].account_no | 계좌번호 | account_no | 913-249880-40-481 |
| loans[].loan_date | loans[].loan_date | 대출일 | date | 2024.08.11 |
| loans[].maturity | loans[].maturity | 만기일 | date | 2054.08.11 |
| loans[].amount | loans[].amount | 대출금액 | amount | 310,000,000 |
| loans[].balance | loans[].balance | 대출잔액 | amount | 301,889,215 |
| loans[].rate | loans[].rate | 금리 | text | 3.77% |
| total_amount | total_amount | 대출금액합계 | amount | 320,000,000 |
| total_balance | total_balance | 대출잔액합계 | amount | 303,430,084 |
| total_korean | total_korean | 대출잔액합계(한글) | amount_korean | 금 삼억삼백사십삼만팔십사원정 |
| guarantee | guarantee | 보증채무 | checkbox | 없음 |
| overdue | overdue | 연체여부 | text | 없음 |
| purpose | purpose | 용도 | text | 법원 제출용 |
| issue_date | issue_date | 발급일 | date | 2026년 1월 31일 |
| issuer | issuer | 발급점 | text | 기업은행 범어지점장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 범어지점장인 |
| guarantee_detail | guarantee_detail | 보증내역 | text | 채욱정 차주 전세자금대출 연대보증 10,000,000원 |
| overdue_detail | overdue_detail | 연체내역 | text | 개인사업자대출(472-84-246131) 연체 47일, 연체원리금 2,000,800원 |

### card_statement · 신용카드 이용대금명세서

그룹: 금융거래 (`finance`)

카드사 신용카드 이용대금명세서 (일시불·할부·수수료 합계 일관).  결제하실 금액·결제일·결제계좌·이용기간 요약 / 이용내역(이용일자·이용하신 가맹점·이용금액·할부·회차· 원금·수수료(이자)·결제 후 잔액) / 연간 할부수수료율 및 100원당 할부개월별 수수료 안내(표준약관상 통지사항).

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company | company | 카드사 | text | NH농협카드 |
| statement_month | statement_month | 청구월 | month | 2026년 1월 |
| member | member | 회원명 | text | 박찬연 |
| card_no | card_no | 카드번호 | text | 5186-69**-****-6103 |
| pay_date | pay_date | 결제일 | date | 2026.01.15 |
| pay_account | pay_account | 결제계좌 | account_no | 기업은행 171-760***-*9-611 |
| usage_period | usage_period | 이용기간 | text | 2025.12.01 ~ 2025.12.31 |
| summary.total | summary.total | 청구금액 | amount | 1,315,504 |
| summary.lump | summary.lump | 일시불 | number | 658,240 |
| summary.installment | summary.installment | 할부 | number | 636,634 |
| summary.cash | summary.cash | 현금서비스 | amount | 0 |
| summary.fee | summary.fee | 수수료(이자) | amount | 20,630 |
| summary.next_month | summary.next_month | 다음달결제예정금액 | number | 239,666 |
| summary.limit | summary.limit | 이용한도 | amount | 8,000,000 |
| rows[].date | rows[].date | 이용일자 | date | 2025.10.22 |
| rows[].merchant | rows[].merchant | 이용하신가맹점 | text | 신세계백화점 |
| rows[].amount | rows[].amount | 이용금액 | amount | 1,190,900 |
| rows[].months | rows[].months | 할부 | text | 3개월 |
| rows[].seq | rows[].seq | 회차 | text | 3/3 |
| rows[].principal | rows[].principal | 원금 | amount | 396,968 |
| rows[].fee | rows[].fee | 수수료(이자) | amount | 4,460 |
| rows[].after | rows[].after | 결제후잔액 | number | 0 |
| sum.amount | sum.amount | 이용금액합계 | amount | 3,287,140 |
| sum.principal | sum.principal | 결제원금합계 | amount | 1,294,874 |
| sum.fee | sum.fee | 수수료합계 | amount | 20,630 |
| fee_rate | fee_rate | 할부수수료율 | percent | 연 13.5% |
| fee_per_100[].months | fee_per_100[].months | 할부개월 | text | 2개월 |
| fee_per_100[].fee | fee_per_100[].fee | 100원당수수료 | amount | 1.69원 |
| summary.overdue | summary.overdue | 연체금액 | number | 597,080 |
| summary.overdue_fee | summary.overdue_fee | 연체이자 | amount | 6,290 |

### commercial_invoice · 상업송장(Commercial Invoice)

그룹: 외환·무역 (`fx`)

COMMERCIAL INVOICE (수출입 상업송장). 품목이 많으면(heavy, 프로필 단위) 여러 쪽, 합계는 마지막 쪽.

연결 업무: 해외송금 (fx_remittance)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| shipper.name | foreign.name | Shipper/Exporter | text | Mekong Garment JSC |
| shipper.address | foreign.address | ShipperAddress | text | 45 Le Loi St, District 1, Ho Chi Minh City, VIETNAM |
| invoice_no | invoice_no | InvoiceNo | text | MGJ-2512-054 |
| invoice_date | invoice_date | InvoiceDate | date | 30 DEC 2025 |
| consignee.name | consignee.name | Consignee | text | UNION TRADING CO., LTD. |
| consignee.address | consignee.address | ConsigneeAddress | text | 6F, GREEN KNOWLEDGE INDUSTRY CENTER, 361 DASAN-RO, JUNG-GU, SEOUL 04766, KOREA |
| notify | notify | NotifyParty | text | SAME AS ABOVE |
| terms.delivery | terms.delivery | TermsofDelivery | text | FOB HO CHI MINH CITY (CAT LAI), VIETNAM (INCOTERMS 2020) |
| terms.payment | terms.payment | TermsofPayment | text | T/T 60 DAYS AFTER B/L DATE |
| origin | origin | CountryofOrigin | text | VIETNAM |
| port_of_loading | port_of_loading | PortofLoading | text | HO CHI MINH CITY (CAT LAI), VIETNAM |
| final_destination | final_destination | FinalDestination | text | BUSAN, KOREA |
| carrier | carrier | Carrier | text | CORAL VOYAGER V.126S |
| sailing_date | sailing_date | Sailingonorabout | date | 01 JAN 2026 |
| marks | marks | MarksandNumbers | text | UNION BUSAN, KOREA C/NO. 1-488 MADE IN VIETNAM |
| items[].description | items[].description | DescriptionofGoods | text | Men's Cotton Crew Neck T-Shirt |
| items[].model | items[].model | Model | text | MT-277A |
| items[].quantity | items[].quantity | Quantity/Unit | text | 18,100 PCS |
| items[].unit_price | items[].unit_price | Unit-price | amount | USD 3.70 |
| items[].amount | items[].amount | Amount | amount | USD 66,970.00 |
| total_quantity | total_quantity | TotalPackages | text | 488 CTNS |
| total_amount | total_amount | TotalAmount | amount | USD 193,394.30 |
| signed_by | signed_by | Signedby | text | Mekong Garment JSC |
| signer | signer | Signer | text | Nguyen Van An |
| contract_no | contract_no | ContractNo | text | HAN-SC-25529 |
| lc.no | lc.no | L/CNo | text | M45972508NU76564 |
| lc.date | lc.date | L/CDate | date | 09 JUL 2025 |
| lc.bank | lc.bank | L/CIssuingBank | text | INDUSTRIAL BANK OF KOREA |
| manufacturer.name | manufacturer.name | Manufacturer | text | Mekong Garment JSC |
| manufacturer.address | manufacturer.address | ManufacturerAddress | text | 45 Le Loi St, District 1, Ho Chi Minh City, VIETNAM |
| beneficiary_bank.name | foreign.bank | BeneficiaryBank | text | BANK OF CHINA (HONG KONG) LIMITED |
| beneficiary_bank.swift | foreign.swift | BeneficiaryBankSWIFT | text | BKCHHKHH |
| beneficiary_bank.account | beneficiary_bank.account | BeneficiaryAccountNo | account_no | 799-657998-874 |
| price_breakdown.fob | price_breakdown.fob | FOBValue | amount | USD 142,545.17 |
| price_breakdown.freight | price_breakdown.freight | OceanFreight | amount | USD 7,240.21 |
| price_breakdown.insurance | price_breakdown.insurance | InsurancePremium | amount | USD 115.42 |
| partial_shipment | partial_shipment | PartialShipment | text | 1ST LOT OF 2 LOTS |

연결 업무 fx_remittance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### trade_contract · 무역 매매계약서(Sales Contract)

그룹: 외환·무역 (`fx`)

SALES CONTRACT (수출입 매매계약서).

연결 업무: 해외송금 (fx_remittance)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| seller.name | foreign.name | Seller | text | Mekong Garment JSC |
| seller.address | foreign.address | SellerAddress | text | 45 Le Loi St, District 1, Ho Chi Minh City, VIETNAM |
| buyer.name | customer.name | Buyer | text | UNION TRADING CO., LTD. |
| buyer.address | customer.address | BuyerAddress | text | 6F, GREEN KNOWLEDGE INDUSTRY CENTER, 361 DASAN-RO, JUNG-GU, SEOUL 04766, KOREA |
| contract_no | contract_no | ContractNo | text | MGJ-SC-25461 |
| contract_date | contract_date | Date | date | November 10, 2025 |
| items[].description | items[].description | Commodity&Description | text | Men's Cotton Crew Neck T-Shirt |
| items[].model | items[].model | Model | text | MT-277A |
| items[].quantity | items[].quantity | Quantity | text | 18,100 PCS |
| items[].unit_price | items[].unit_price | UnitPrice | amount | USD 3.70 |
| items[].amount | items[].amount | Amount | amount | USD 66,970.00 |
| total_amount | total_amount | TotalAmount | amount | USD 193,394.30 |
| total_words | total_words | TotalAmountinWords | text | SAY US DOLLARS ONE HUNDRED NINETY THREE THOUSAND THREE HUNDRED NINETY FOUR AND CENTS THIRTY ONLY |
| clauses.price_terms | clauses.price_terms | PriceTerms | text | FOB HO CHI MINH CITY (CAT LAI), VIETNAM (INCOTERMS 2020), prices in USD. |
| clauses.origin | clauses.origin | Origin | text | Vietnam |
| clauses.packing | clauses.packing | Packing | text | Export standard packing in cartons, suitable for ocean transportation. |
| clauses.shipping_mark | clauses.shipping_mark | ShippingMark | text | UNION BUSAN, KOREA C/NO. 1-UP MADE IN VIETNAM |
| clauses.shipment | clauses.shipment | Shipment | text | Not later than January 09, 2026. Partial shipments not allowed, transshipment not allowed. |
| clauses.port_of_shipment | clauses.port_of_shipment | PortofShipment | text | HO CHI MINH CITY (CAT LAI), VIETNAM |
| clauses.destination | clauses.destination | Destination | text | BUSAN, KOREA |
| clauses.payment | clauses.payment | Payment | text | By telegraphic transfer within 60 days after B/L date. |
| clauses.inspection | clauses.inspection | Inspection | text | Inspection by an independent surveyor (SGS or equivalent) at the port of loading; cost borne by the Seller. |
| clauses.arbitration | clauses.arbitration | Arbitration | text | Any dispute shall be settled by arbitration in Singapore under the SIAC Rules. |
| seal.buyer | seal.customer | BuyerSignature | seal |  |
| sign.buyer | sign.customer | BuyerSignature | signature | Akira Tanaka |
| buyer.signer | buyer.signer | BuyerSignatory | text | Park Chanyeon |
| buyer.title | buyer.title | BuyerTitle | text | Representative Director |
| buyer.sign_date | buyer.sign_date | BuyerSigningDate | date | 13 NOV 2025 |
| seal.seller | seal.seller | SellerSignature | seal |  |
| sign.seller | sign.seller | SellerSignature | signature | Nguyen Van An |
| seller.signer | seller.signer | SellerSignatory | text | Nguyen Van An |
| seller.title | seller.title | SellerTitle | text | Export Manager |
| seller.sign_date | seller.sign_date | SellerSigningDate | date | 10 NOV 2025 |
| clauses.insurance | clauses.insurance | Insurance | text | To be covered by the Seller for 110% of invoice value against Institute Cargo Clauses (A). |
| gtc_terms.late_penalty | gtc_terms.late_penalty | LateShipmentPenalty | percent | 1% |
| gtc_terms.inspection_days | gtc_terms.inspection_days | InspectionPeriod(days) | number | 21 |
| gtc_terms.warranty | gtc_terms.warranty | WarrantyPeriod | text | eighteen (18) months |
| gtc_terms.late_interest | gtc_terms.late_interest | LatePaymentInterest | percent | 6% |
| gtc_terms.governing_law | gtc_terms.governing_law | GoverningLaw | text | the State of New York, U.S.A. |
| gtc_terms.qty_tolerance | gtc_terms.qty_tolerance | QuantityTolerance | percent | 3% |
| gtc_terms.claim_days | gtc_terms.claim_days | ClaimPeriod(days) | number | 90 |
| clauses.manufacturer | clauses.manufacturer | Manufacturer | text | Mekong Garment JSC, 45 Le Loi St, District 1, Ho Chi Minh City, VIETNAM (goods to be shipped directly from the manufacturer) |

연결 업무 fx_remittance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### bill_of_lading · 선하증권(B/L)

그룹: 외환·무역 (`fx`)

BILL OF LADING (해상 선하증권). 컨테이너가 많으면 부속 목록(ATTACHED SHEET)이 다음 쪽에 붙는다.

연결 업무: 해외송금 (fx_remittance)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| shipper.name | foreign.name | Shipper | text | Mekong Garment JSC |
| shipper.address | foreign.address | ShipperAddress | text | 45 Le Loi St, District 1, Ho Chi Minh City, VIETNAM |
| booking_no | booking_no | BookingNo | text | BKG3185811 |
| bl_no | bl_no | B/LNo | text | OCLN15701972 |
| carrier | carrier | Carrier | text | OCEANLINK CONTAINER LINES |
| forwarder | forwarder | ForwardingAgent | text | Daon Logistics Co., Ltd. |
| consignee.name | consignee.name | Consignee | text | UNION TRADING CO., LTD. |
| consignee.address | consignee.address | ConsigneeAddress | text | 6F, GREEN KNOWLEDGE INDUSTRY CENTER, 361 DASAN-RO, JUNG-GU, SEOUL 04766, KOREA |
| notify.name | notify.name | NotifyParty | text | SAME AS CONSIGNEE |
| pre_carriage | pre_carriage | Pre-carriageby | text | TRUCK |
| place_of_receipt | place_of_receipt | PlaceofReceipt | text | HO CHI MINH CITY (CAT LAI) CY |
| origin | origin | PointandCountryofOrigin | text | VIETNAM |
| vessel_voyage | vessel_voyage | OceanVessel/VoyNo | text | CORAL VOYAGER 126S |
| port_of_loading | port_of_loading | PortofLoading | text | HO CHI MINH CITY (CAT LAI), VIETNAM |
| port_of_discharge | port_of_discharge | PortofDischarge | text | BUSAN, KOREA |
| place_of_delivery | place_of_delivery | PlaceofDelivery | text | BUSAN CY |
| containers[].no | containers[].no | ContainerNo | text | OCLU1212140 |
| containers[].type | containers[].type | ContainerType | text | 40'HC |
| containers[].seal | containers[].seal | SealNo | text | H388222 |
| marks | marks | MarksandNumbers | text | UNION BUSAN, KOREA C/NO. 1-488 MADE IN VIETNAM |
| container_count | container_count | No.ofContainers | text | 1 X 40'HC |
| packages | packages | No.ofPackages | text | 488 CTNS |
| description | description | DescriptionofGoods | text | Men's Cotton Crew Neck T-Shirt  18,100 PCS Men's Chino Pants  8,240 PCS Women's Cotton Knit Cardigan  3,030 PCS |
| freight | freight | Freight | text | FREIGHT COLLECT |
| gross_weight | gross_weight | GrossWeight | text | 9,381.96 KGS |
| measurement | measurement | Measurement | text | 49.050 CBM |
| total_words | total_words | TotalNumberinWords | text | SAY: ONE (1) CONTAINER ONLY |
| freight_payable_at | freight_payable_at | FreightPayableat | text | BUSAN |
| issue_place | issue_place | PlaceofIssue | text | HO CHI MINH CITY (CAT LAI) |
| issue_date | issue_date | DateofIssue | date | 01 JAN 2026 |
| originals | originals | NumberofOriginalB/L | text | THREE (3) |
| on_board_date | on_board_date | OnBoardDate | date | 01 JAN 2026 |
| document_type | document_type | DocumentType | text | SEA WAYBILL |
| surrender | surrender | Surrender | text | SURRENDERED |
| surrender_date | surrender_date | SurrenderDate | date | 18 AUG 2025 |
| containers[].packages | containers[].packages | ContainerPackages | text | 1,571 PKGS |
| containers[].gross_weight | containers[].gross_weight | ContainerGrossWeight | number | 41,420.40 |
| containers[].measurement | containers[].measurement | ContainerMeasurement | number | 44.735 |
| notify.address | notify.address | NotifyPartyAddress | text | 13F, DN SQUARE, 499 HWAUN-RO, SEO-GU, GWANGJU 61425, KOREA |
| lc_no | lc_no | L/CNo | text | M45972508NU76564 |
| charges[].name | charges[].name | Charge | text | OCEAN FREIGHT |
| charges[].quantity | charges[].quantity | RevenueTons | number | 2.00 |
| charges[].rate | charges[].rate | Rate | number | 3,300.00 |
| charges[].per | charges[].per | Per | text | CNTR |
| charges[].collect | charges[].collect | Collect | amount | USD 6,600.00 |
| charges[].prepaid | charges[].prepaid | Prepaid | amount | USD 280.00 |

연결 업무 fx_remittance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### packing_list · 포장명세서(Packing List)

그룹: 외환·무역 (`fx`)

PACKING LIST (포장명세서). 상업송장과 같은 선적 정보. 품목이 많으면 여러 쪽, 컨테이너별로 나눠 적기도 한다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| shipper.name | foreign.name | Shipper/Exporter | text | Mekong Garment JSC |
| shipper.address | foreign.address | ShipperAddress | text | 45 Le Loi St, District 1, Ho Chi Minh City, VIETNAM |
| invoice_no | invoice_no | InvoiceNo | text | MGJ-2512-054 |
| invoice_date | invoice_date | InvoiceDate | date | 30 DEC 2025 |
| consignee.name | consignee.name | Consignee | text | UNION TRADING CO., LTD. |
| consignee.address | consignee.address | ConsigneeAddress | text | 6F, GREEN KNOWLEDGE INDUSTRY CENTER, 361 DASAN-RO, JUNG-GU, SEOUL 04766, KOREA |
| contract_no | contract_no | ContractNo | text | MGJ-SC-25461 |
| notify | notify | NotifyParty | text | SAME AS CONSIGNEE |
| port_of_loading | port_of_loading | PortofLoading | text | HO CHI MINH CITY (CAT LAI), VIETNAM |
| final_destination | final_destination | FinalDestination | text | BUSAN, KOREA |
| carrier | carrier | Carrier | text | CORAL VOYAGER V.126S |
| sailing_date | sailing_date | Sailingonorabout | date | January 01, 2026 |
| marks | marks | MarksandNumbers | text | UNION BUSAN, KOREA C/NO. 1-488 MADE IN VIETNAM |
| items[].ctn_no | items[].ctn_no | C/TNo | text | 1-181 |
| items[].description | items[].description | DescriptionofGoods | text | Men's Cotton Crew Neck T-Shirt |
| items[].packages | items[].packages | Packages | text | 181 CTNS |
| items[].quantity | items[].quantity | Quantity | text | 18,100 PCS |
| items[].net_weight | items[].net_weight | NetWeight | number | 3,258.00 |
| items[].gross_weight | items[].gross_weight | GrossWeight | number | 3,518.64 |
| items[].measurement | items[].measurement | Measurement | number | 16.290 |
| total.packages | total.packages | TotalPackages | text | 488 CTNS |
| total.net_weight | total.net_weight | TotalNetWeight | text | 8,687.00 KGS |
| total.gross_weight | total.gross_weight | TotalGrossWeight | text | 9,381.96 KGS |
| total.measurement | total.measurement | TotalMeasurement | text | 49.050 CBM |
| signed_by | signed_by | Signedby | text | Mekong Garment JSC |
| signer | signer | Signer | text | Nguyen Van An |
| containers[].no | containers[].no | ContainerNo | text | TPMU9280511 |
| containers[].seal | containers[].seal | SealNo | text | SL436094 |
| containers[].packages | containers[].packages | ContainerPackages | text | 409 PKGS |
| containers[].net_weight | containers[].net_weight | ContainerNetWeight | number | 15,244.00 |
| containers[].gross_weight | containers[].gross_weight | ContainerGrossWeight | number | 15,653.52 |
| containers[].measurement | containers[].measurement | ContainerMeasurement | number | 51.260 |
| lc_no | lc_no | L/CNo | text | M45972508NU76564 |
| manufacturer.name | manufacturer.name | Manufacturer | text | Mekong Garment JSC |
| manufacturer.address | manufacturer.address | ManufacturerAddress | text | 45 Le Loi St, District 1, Ho Chi Minh City, VIETNAM |
| partial_shipment | partial_shipment | PartialShipment | text | 1ST LOT OF 2 LOTS |

### import_declaration · 수입신고필증

그룹: 외환·무역 (`fx`)

수입신고필증 (UNI-PASS 발행 양식). 과세가격·관세·부가세가 계산상 일치한다. 란은 세번부호(상품)별로 묶고, 같은 상품의 모델·규격 줄은 란 안의 규격 줄(01, 02 ...)로 적는다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| decl_no | decl_no | 신고번호 | text | 20097-26-7868647U |
| decl_date | decl_date | 신고일 | date | 2026/01/10 |
| customs | customs | 세관.과 | text | 030-17 |
| arrival_date | arrival_date | 입항일 | date | 2026/01/09 |
| bl_no | bl_no | B/L번호 | text | OCLN15701972 |
| cargo_no | cargo_no | 화물관리번호 | text | 26OCLN610441I-2996-002 |
| warehouse_date | warehouse_date | 반입일 | date | 2026/01/10 |
| collection_type | collection_type | 징수형태 | number | 11 |
| declarant | declarant | 신고인 | text | 대한관세법인 정채유 |
| importer.name | customer.name | 수입자 | text | (주)유니온무역 |
| importer.code | importer.code | 수입자통관고유부호 | text | 유니온무8255080 |
| taxpayer.code | taxpayer.code | 납세의무자통관고유부호 | text | 유니온무8255080 |
| taxpayer.address | customer.address | 납세의무자주소 | text | 서울특별시 중구 다산로 361, 6층 |
| taxpayer.name | taxpayer.name | 납세의무자상호 | text | (주)유니온무역 |
| taxpayer.ceo | customer.ceo | 납세의무자성명 | text | 박찬연 |
| taxpayer.biz_no | customer.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| forwarder | forwarder | 운송주선인 | text | DAON LOGISTICS CO., LTD. |
| supplier | supplier | 해외거래처 | text | MEKONG GARMENT JSC (VN) |
| clearance_plan | clearance_plan | 통관계획 | text | D 보세구역장치후 |
| origin_cert | origin_cert | 원산지증명서유무 | text | Y |
| total_weight | total_weight | 총중량 | text | 9,382 KG |
| total_packages | total_packages | 총포장갯수 | text | 488 CT |
| arrival_port | arrival_port | 국내도착항 | text | KRPUS 부산항 |
| transport | transport | 운송형태 | text | 10 FCL |
| export_country | export_country | 적출국 | text | VN VIETNAM |
| vessel | vessel | 선기명 | text | CORAL VOYAGER |
| master_bl | master_bl | MASTERB/L번호 | text | OCLN15701972 |
| carrier_code | carrier_code | 운수기관부호 | text | OCLN |
| inspection_place | inspection_place | 검사(반입)장소 | text | 03055276-55499004 부산신항국제터미널 |
| items[].line_no | items[].line_no | 란번호 | number | 001 |
| line_total | line_total | 총란수 | amount | 003 |
| items[].std_name | items[].std_name | 품명 | text | T-SHIRTS, KNITTED, OF COTTON |
| items[].trade_name | items[].trade_name | 거래품명 | text | MEN'S COTTON CREW NECK T-SHIRT |
| items[].specs[].no | items[].specs[].no | 규격번호 | number | 01 |
| items[].specs[].model | items[].specs[].model | 모델·규격 | text | MT-277A |
| items[].specs[].quantity | items[].specs[].quantity | 수량 | text | 18,100 PCS |
| items[].specs[].unit_price | items[].specs[].unit_price | 단가 | amount | 3.70 |
| items[].specs[].amount | items[].specs[].amount | 금액 | amount | 66,970.00 |
| items[].hs_code | items[].hs_code | 세번부호 | text | 6109.10-0000 |
| items[].net_weight | items[].net_weight | 순중량 | text | 3,258.0 KG |
| items[].taxable_usd | items[].taxable_usd | 과세가격(USD) | amount | $67,865 |
| items[].taxable_krw | items[].taxable_krw | 과세가격(원화) | amount | ₩98,445,056 |
| items[].origin | items[].origin | 원산지 | text | VN-B-Y |
| items[].duty_type | items[].duty_type | 세종 | text | 관 |
| items[].duty_rate | items[].duty_rate | 관세율 | text | 0.00(FVN1) |
| items[].duty_amount | items[].duty_amount | 관세액 | amount | 0 |
| items[].vat_rate | items[].vat_rate | 부가세율 | text | 10.00(A) |
| items[].vat_amount | items[].vat_amount | 부가세액 | amount | 9,844,500 |
| payment | payment | 결제금액 | text | FOB-USD-193,394.30-TT |
| exchange_rate | exchange_rate | 환율 | number | 1,450.60 |
| total_taxable | total_taxable | 총과세가격 | amount | ₩284,287,194 |
| freight | freight | 운임 | amount | ₩3,553,041 |
| vat_base | vat_base | 부가가치세과표 | amount | ₩284,287,194 |
| insurance | insurance | 보험료 | amount | ₩196,382 |
| tax.duty | tax.duty | 관세 | amount | 0 |
| customs_office | customs_office | 세관 | text | 부산세관 |
| officer | officer | 담당자 | text | 이도경 |
| receipt_datetime | receipt_datetime | 접수일시 | datetime | 2026/01/10 12:33 |
| accept_date | accept_date | 수리일자 | date | 2026/01/11 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 세관장인 |
| tax.vat | tax.vat | 부가세 | amount | 28,428,700 |
| tax.total | tax.total | 총세액합계 | amount | 28,428,700 |
| amendment.date | amendment.date | 정정승인일자 | date | 2026/04/03 |
| amendment.reason | amendment.reason | 정정사유 | text | (42)원산지표시 정정 |
| items[].reduction.rate | items[].reduction.rate | 감면율 | number | 50.00 |
| items[].reduction.code | items[].reduction.code | 감면분납부호 | text | Y8010 |
| items[].reduction.amount | items[].reduction.amount | 감면액 | amount | 12,607,110 |

### admission_letter · 입학허가서(Letter of Admission)

그룹: 외환·무역 (`fx`)

해외 대학 입학허가서 (유학생 송금 증빙). 조건부 입학·장학금·입학 연기는 프로필 단위(_study).

연결 업무: 유학생 송금 (study_abroad_remittance)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| university.name | foreign.name | University | text | Westlake State University |
| university.office | foreign.office | Office | text | Office of Graduate Admissions |
| university.address | foreign.address | UniversityAddress | text | 1800 Lakeview Dr, Seattle, WA 98105, USA |
| university.email | university.email | Email | text | admissions@westlakestate.edu |
| letter_date | letter_date | Date | date | December 05, 2025 |
| student.name | family.name | StudentName | text | Chanyeon Park |
| student.address | student.address | StudentAddress | text | Apt. 110-501, 524 Bangbae-ro, Seocho-gu, Seoul 06931, Korea |
| admission_type | admission_type | AdmissionType | text | CONDITIONAL ADMISSION |
| term | term | TermofEntry | text | Fall 2026 |
| student.birth | student.birth | DateofBirth | date | 10 FEB 1990 |
| student.nationality | student.nationality | Citizenship | text | Republic of Korea |
| student.id | family.id | StudentID | text | M94946101 |
| program | program | Program | text | Education |
| degree | degree | Degree | text | Master of Education (M.Ed.) |
| start_date | start_date | ClassesBegin | date | August 25, 2026 |
| duration | duration | Duration | text | 2 years (full-time) |
| condition_deadline | condition_deadline | ConditionDeadline | date | July 20, 2026 |
| conditions[] | conditions[] | Condition | text | Submission of an official TOEFL iBT score of 80 or above (or IELTS Academic 6.5) |
| deposit_deadline | deposit_deadline | DepositDeadline | date | December 31, 2025 |
| signer | signer | Signedby | text | Emily R. Watson |
| signer_title | signer_title | Title | text | Director of Admissions |
| cost.tuition | cost.tuition | EstimatedTuition | number | $56,000.00 |
| cost.living | cost.living | EstimatedLivingExpenses | number | $22,000.00 |
| cost.insurance | cost.insurance | EstimatedHealthInsurance | number | $3,120.00 |
| cost.books | cost.books | EstimatedBooksandSupplies | number | $1,620.00 |
| cost.total | cost.total | TotalEstimatedCost | amount | $82,740.00 |
| scholarship.name | scholarship.name | Scholarship | text | International Student Award |
| scholarship.amount | scholarship.amount | ScholarshipAmount | text | $8,860.00 per semester |
| deferred_from | deferred_from | DeferredFrom | text | Spring 2025 |

연결 업무 study_abroad_remittance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### tuition_invoice · 학비 청구서(Tuition Invoice)

그룹: 외환·무역 (`fx`)

해외 대학 학비 청구서 (Statement of Fees). 장학금은 입학허가서와 같은 프로필 단위 값.

연결 업무: 유학생 송금 (study_abroad_remittance)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| university.name | foreign.name | University | text | Westlake State University |
| university.office | foreign.office | Office | text | Student Financial Services |
| university.address | foreign.address | UniversityAddress | text | 1800 Lakeview Dr, Seattle, WA 98105, USA |
| student.name | family.name | StudentName | text | Chanyeon Park |
| student.id | family.id | StudentID | text | M94946101 |
| student.program | student.program | Program | text | Master of Education (M.Ed.) in Education |
| invoice_no | invoice_no | InvoiceNo | text | INV-2026368927 |
| invoice_date | invoice_date | InvoiceDate | date | December 31, 2025 |
| term | term | Term | text | Fall 2026 |
| items[].date | items[].date | Date | date | 12/30/2025 |
| items[].description | items[].description | Description | text | Tuition - Full-time Graduate |
| items[].charge | items[].charge | Charges | amount | $17,430.00 |
| items[].credit | items[].credit | Payments/Credits | amount | $1,000.00 |
| summary.previous_balance | summary.previous_balance | PreviousBalance | amount | $0.00 |
| summary.charges | summary.charges | NewCharges | amount | $21,032.00 |
| summary.credits | summary.credits | Payments/Credits | amount | $10,400.00 |
| total | total | TotalAmountDue | amount | USD 10,632.00 |
| due_date | due_date | DueDate | date | August 03, 2026 |
| bank.beneficiary | bank.beneficiary | Beneficiary | text | Westlake State University |
| bank.bank_name | bank.bank_name | BankName | text | Bank of America, N.A. |
| bank.swift | bank.swift | SWIFT | text | BOFAUS3N |
| bank.account | bank.account | AccountNumber | account_no | 212604946606 |
| bank.routing_label | bank.routing_label | RoutingLabel | text | ABA Routing No. |
| bank.routing | bank.routing | RoutingNumber | number | 036941220 |
| bank.reference | bank.reference | PaymentReference | text | M94946101 Chanyeon Park |
| amount_due_now | amount_due_now | AmountDueNow | amount | £2,247.25 |
| installments[].no | installments[].no | InstallmentNo | number | 1 |
| installments[].due_date | installments[].due_date | InstallmentDueDate | date | January 01, 2026 |
| installments[].amount | installments[].amount | InstallmentAmount | amount | £2,247.25 |

연결 업무 study_abroad_remittance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### resident_id_card · 주민등록증

그룹: 신원·신분 (`identity`)

주민등록증 앞면.

연결 업무: 개인 계좌개설 (account_opening), 개인 신용대출 (personal_credit_loan), 주택담보대출 (mortgage), 전세자금대출 (jeonse_loan), 개인사업자 대출 (sole_proprietor_loan), 해외송금 (fx_remittance), 개인형IRP 개설 (irp_opening), 퇴직급여 수령 (retirement_payout), 전자금융 가입 (efinance_signup), 상속예금 지급 (inheritance)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| name | customer.name | 성명 | text | 박찬연 |
| name_hanja | customer.name_hanja | 한자성명 | text | 朴讚姸 |
| rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| issue_date | issue_date | 발급일 | date | 2020. 4. 22. |
| issuer | issuer | 발급기관 | text | 서울특별시 서초구청장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 서초구청장인 |
| resident_type | resident_type | 재외국민 | text | 재외국민 |

연결 업무 account_opening · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 personal_credit_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 mortgage · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 jeonse_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 sole_proprietor_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 fx_remittance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 irp_opening · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 retirement_payout · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 efinance_signup · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 inheritance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### driver_license · 운전면허증

그룹: 신원·신분 (`identity`)

자동차운전면허증 앞면.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| license_type | license_type | 면허종류 | text | 2종보통 |
| serial | serial | 암호일련번호 | text | X0T6QD |
| license_no | license_no | 면허번호 | text | 11-14-634523-71 |
| name | customer.name | 성명 | text | 박찬연 |
| rrn | customer.rrn | 주민등록번호 | rrn | 900210-1****** |
| address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| renewal_period | renewal_period | 갱신기간 | text | 2035.01.01~2035.12.31 |
| issue_date | issue_date | 발급일 | date | 2025.12.02 |
| issuer | issuer | 발급기관 | text | 서울특별시경찰청장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 경찰청장인 |
| aptitude_period | aptitude_period | 적성검사기간 | text | 2034.01.01~2034.12.31 |
| condition | condition | 조건 | text | A |

### passport · 여권

그룹: 신원·신분 (`identity`)

대한민국 여권 사진정보면 (MRZ 포함).

연결 업무: 유학생 송금 (study_abroad_remittance)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| type | type | 종류/Type | text | PM |
| country_code | country_code | 발행국/Issuingcountry | text | KOR |
| passport_no | passport_no | 여권번호/PassportNo. | text | M93151969 |
| surname | surname | 성/Surname | text | PARK |
| given_names | given_names | 이름/Givennames | text | CHANYEON |
| name_korean | name_korean | 한글성명 | text | 박찬연 |
| nationality | customer.nationality | 국적/Nationality | text | REPUBLIC OF KOREA |
| birth | customer.birth | 생년월일/Dateofbirth | text | 10 FEB 1990 |
| gender | customer.gender | 성별/Sex | text | M |
| personal_no | personal_no | 주민등록번호/PersonalNo. | text | 1****** |
| date_of_issue | date_of_issue | 발급일/Dateofissue | text | 30 AUG 2018 |
| date_of_expiry | date_of_expiry | 기간만료일/Dateofexpiry | text | 29 AUG 2028 |
| authority | authority | 발행관청/Authority | text | MINISTRY OF FOREIGN AFFAIRS |
| mrz.line1 | mrz.line1 | MRZ | text | PMKORPARK<<CHANYEON<<<<<<<<<<<<<<<<<<<<<<<<< |
| mrz.line2 | mrz.line2 | MRZ | text | M931519697KOR9002100M2808299<<<<<<<<<<<<<<<6 |

연결 업무 study_abroad_remittance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### alien_registration_card · 외국인등록증

그룹: 신원·신분 (`identity`)

외국인등록증(RESIDENCE CARD) 앞면. 프로필에 외국인이 없으므로 이 서류 안에서 외국인을 만든다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| registration_no | registration_no | 외국인등록번호 | rrn | 011031-8341376 |
| name | customer.name | 성명 | text | HOANG NGOC ANH |
| country | country | 국가/지역 | text | VIETNAM |
| gender | customer.gender | 성별 | text | F |
| visa_status | visa_status | 체류자격 | text | 비전문취업(E-9) |
| issue_date | issue_date | 발급일자 | date | 2025.12.09 |
| issuer | issuer | 발급기관 | text | 서울남부출입국·외국인사무소장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 출입국장인 |

### seal_certificate · 인감증명서

그룹: 신원·신분 (`identity`)

인감증명서 (인감증명법 시행령 별지 제14호서식 / 전자발급 제14호의2서식). 일반용 / 부동산 매도용. 대리 발급, 법인·공동 매수자, 미성년 자녀(법정대리인 동의) 발급 등.

연결 업무: 주택담보대출 (mortgage), 상속예금 지급 (inheritance)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| doc_no | doc_no | 인감증명서발급사실확인용번호 | text | 7043-3278-9148 |
| applicant_type | applicant_type | 발급구분 | checkbox | 본인 |
| seal.registered | seal.registered | 등록인감 | seal | 박찬연인 |
| seal_name | seal_name | 인감 | text | 박찬연인 |
| person.name | customer.name | 성명 | text | 박찬연 |
| person.name_hanja | customer.name_hanja | 한자 | text | 朴讚姸 |
| person.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| person.nationality | customer.nationality | 국적 | text | 대한민국 |
| person.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| usage_type | usage_type | 용도 | checkbox | 일반용 |
| issue_date | issue_date | 발급일 | date | 2026년 1월 31일 |
| issuer | issuer | 발급기관 | text | 서울특별시 서초구 방배동장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 직인 |
| buyer.name | counterparty.name | 성명(법인명) | text | 최다희 |
| buyer.rrn | buyer.rrn | 주민등록번호(법인등록번호) | rrn | 630929-2087142 |
| buyer.address | counterparty.address | 주소(법인소재지) | text | 서울특별시 송파구 송파대로 179 |
| applicant_signature | applicant_signature | 발급신청자서명 | text | 송소경 |
| agent.name | agent.name | 성명 | text | 송소경 |
| agent.rrn | agent.rrn | 주민등록번호 | rrn | 580414-2****** |
| remark | remark | 비고 | text | 법정대리인(모) 전영경 동의 |

연결 업무 mortgage · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 inheritance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### signature_confirmation · 본인서명사실확인서

그룹: 신원·신분 (`identity`)

본인서명사실확인서 (본인서명사실 확인 등에 관한 법률 시행령 별지 제2호서식).

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| doc_no | doc_no | 문서확인번호 | text | 2169-2497-2882-0522 |
| signer.name | customer.name | 성명 | text | 박찬연 |
| signer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| signer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| other_usage | other_usage | 그외의용도 | text | 대출보증용 |
| signature | signature | 서명 | text | 박찬연 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 서울특별시 서초구 방배동장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 직인 |
| real_estate_usage | real_estate_usage | 부동산관련용도및자동차매도용도 | checkbox | 소유권 이전(매매, 증여 등) |
| counterparty.name | counterparty.name | 성명(법인명) | text | 이서우 |
| counterparty.rrn | counterparty.rrn | 주민등록번호(법인등록번호) | rrn | 930301-2699865 |
| counterparty.address | counterparty.address | 주소 | text | 전라남도 여수시 시청로 126, 115동 1503호 |
| delegate.name | agent.name | 성명 | text | 엄주영 |
| delegate.address | agent.address | 주소 | text | 서울특별시 종로구 자하문로 92, 114동 504호 |

### real_estate_registry · 등기사항전부증명서(집합건물)

그룹: 부동산 (`real_estate`)

등기사항전부증명서(말소사항 포함) - 집합건물. 표제부·갑구·을구.  이력이 많은 물건(소유권 이전·근저당 설정/말소 반복)은 갑구·을구가 길어져 여러 쪽이 된다. 말소된 사항은 빨간 실선으로 지우고, 말소 등기('3번근저당권설정등기말소')는 별도 순위번호로 적는다.

연결 업무: 주택담보대출 (mortgage), 전세자금대출 (jeonse_loan)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| property | property | 부동산의표시 | text | 경기도 수원시 영통구 원천동 87 한신휴플러스에듀포레 제115동 제21층 제2104호 |
| unique_no | unique_no | 고유번호 | text | 1792-2013-094176 |
| buildings[].display_no | buildings[].display_no | 표시번호 | number | 1 |
| buildings[].receipt | buildings[].receipt | 접수 | date | 1994년11월4일 |
| buildings[].location | buildings[].location | 소재지번,건물명칭및번호 | text | 경기도 수원시 영통구 원천동 87 한신휴플러스에듀포레 제115동 |
| buildings[].detail | buildings[].detail | 건물내역 | text | 철근콘크리트구조 (철근)콘크리트지붕 21층 공동주택(아파트) 지하1층 185.39㎡ 1층 234.92㎡ 2층~21층 각 280.74㎡ |
| buildings[].cause | buildings[].cause | 등기원인및기타사항 | text | 도면편철장 제8책 제698장 |
| land.display_no | land.display_no | 표시번호 | number | 1 |
| land.location | property.location | 소재지번 | text | 1. 경기도 수원시 영통구 원천동 87 |
| land.category | land.category | 지목 | text | 대 |
| land.area | land.area | 면적 | text | 31,054.7㎡ |
| land.cause | land.cause | 등기원인및기타사항 | text | 1994년11월4일 등기 |
| unit.display_no | unit.display_no | 표시번호 | number | 1 |
| unit.receipt | unit.receipt | 접수 | date | 1994년11월4일 |
| unit.unit_no | unit.unit_no | 건물번호 | text | 제21층 제2104호 |
| unit.detail | unit.detail | 건물내역 | text | 철근콘크리트구조 101.84㎡ |
| unit.cause | unit.cause | 등기원인및기타사항 | text | 도면편철장 제8책 제698장 |
| land_right.display_no | land_right.display_no | 표시번호 | number | 1 |
| land_right.kind | property.kind | 대지권종류 | text | 1 소유권대지권 |
| land_right.ratio | land_right.ratio | 대지권비율 | text | 31,054.7분의 54.47 |
| land_right.cause | land_right.cause | 등기원인및기타사항 | text | 1994년10월19일 대지권 1994년11월4일 등기 |
| gapgu[].rank | gapgu[].rank | 순위번호 | number | 1 |
| gapgu[].purpose | gapgu[].purpose | 등기목적 | text | 소유권보존 |
| gapgu[].receipt | gapgu[].receipt | 접수 | text | 1994년11월4일 제30434호 |
| gapgu[].holder.role | gapgu[].holder.role | 권리자구분 | text | 소유자 |
| gapgu[].holder.name | gapgu[].holder.name | 소유자 | text | 주식회사쌍용건설 |
| gapgu[].holder.reg_no | gapgu[].holder.reg_no | 등록번호 | text | 171512-4430096 |
| gapgu[].holder.address | gapgu[].holder.address | 주소 | text | 경기도 수원시 영통구 시청로 108 |
| gapgu[].cause | gapgu[].cause | 등기원인 | text | 2020년1월13일 매매 |
| gapgu[].holder.note | gapgu[].holder.note | 거래가액 | text | 거래가액 금410,000,000원 |
| eulgu[].rank | eulgu[].rank | 순위번호 | number | 1 |
| eulgu[].purpose | eulgu[].purpose | 등기목적 | text | 근저당권설정 |
| eulgu[].receipt | eulgu[].receipt | 접수 | text | 2020년2월18일 제40565호 |
| eulgu[].cause | eulgu[].cause | 등기원인 | text | 2020년2월18일 설정계약 |
| eulgu[].max_amount | eulgu[].max_amount | 채권최고액 | amount | 금318,000,000원 |
| eulgu[].debtor | eulgu[].debtor | 채무자 | text | 박기우 |
| eulgu[].debtor_address | eulgu[].debtor_address | 채무자주소 | text | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신휴플러스에듀포레) |
| eulgu[].mortgagee | eulgu[].mortgagee | 근저당권자 | text | 주식회사우리은행 171511-7786133 |
| eulgu[].mortgagee_address | eulgu[].mortgagee_address | 근저당권자주소 | text | 서울특별시 중구 소공로 51 (송도지점) |
| registry_office | registry_office | 관할등기소 | text | 수원지방법원 등기과 |
| view_datetime | view_datetime | 열람일시 | datetime | 2026년01월31일 15시31분14초 |
| gapgu[].holders[].role | gapgu[].holders[].role | 권리자구분 | text | 공유자 |
| gapgu[].holders[].share | gapgu[].holders[].share | 지분 | text | 지분 2분의 1 |
| gapgu[].holders[].name | gapgu[].holders[].name | 공유자 | text | 반원인 |
| gapgu[].holders[].reg_no | gapgu[].holders[].reg_no | 등록번호 | text | 580519-******* |
| gapgu[].holders[].address | gapgu[].holders[].address | 주소 | text | 대구광역시 수성구 수성로 401, 107동 2004호 (지산동, 센트레빌에듀포레아파트) |
| gapgu[].note | gapgu[].note | 거래가액 | text | 거래가액 금470,000,000원 |
| gapgu[].claim_amount | gapgu[].claim_amount | 청구금액 | amount | 금4,134,361원 |
| gapgu[].creditor | gapgu[].creditor | 채권자 | text | 주식회사삼성카드 130111-2186484 |
| gapgu[].creditor_address | gapgu[].creditor_address | 채권자주소 | text | 서울특별시 중구 국제금융로 331 |
| fee | fee | 수수료 | amount | 1,000원 |
| issue_date | issue_date | 발행일 | date | 2025년 5월 19일 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 전산운영책임관인 |
| issue_no | issue_no | 발행번호 | number | 88889704605527375125 |
| confirm_no | confirm_no | 발급확인번호 | text | NTOZ-IUSA-4727 |
| issue_date_short | issue_date_short | 발행일 | date | 2025/05/19 |
| eulgu[].deposit | eulgu[].deposit | 전세금 | amount | 금345,000,000원 |
| eulgu[].rent | eulgu[].rent | 차임 | text | 없음 |
| eulgu[].scope | eulgu[].scope | 범위 | text | 주거용 건물의 전부 |
| eulgu[].contract_date | eulgu[].contract_date | 임대차계약일자 | date | 2012년9월4일 |
| eulgu[].resident_date | eulgu[].resident_date | 주민등록일자 | date | 2012년10월6일 |
| eulgu[].possession_date | eulgu[].possession_date | 점유개시일자 | date | 2012년10월6일 |
| eulgu[].fixed_date | eulgu[].fixed_date | 확정일자 | date | 2012년10월7일 |
| eulgu[].lessee | eulgu[].lessee | 임차권자 | text | 박윤성 880417-******* |
| eulgu[].lessee_address | eulgu[].lessee_address | 임차권자주소 | text | 전라남도 여수시 좌수영로 575, 105동 604호 (문수동, 현대파크) |
| summary.owners[].name | summary.owners[].name | 등기명의인 | text | 이민빈 (소유자) |
| summary.owners[].reg_no | summary.owners[].reg_no | (주민)등록번호 | text | 720524-******* |
| summary.owners[].share | summary.owners[].share | 최종지분 | text | 단독소유 |
| summary.owners[].address | summary.owners[].address | 주소 | text | 서울특별시 마포구 월드컵로 491-5, 118동 1203호 (상암동, e편한세상아파트) |
| summary.owners[].rank | summary.owners[].rank | 순위번호 | number | 4 |
| summary.rights[].rank | summary.rights[].rank | 순위번호 | number | 1 |
| summary.rights[].purpose | summary.rights[].purpose | 등기목적 | text | 근저당권설정 |
| summary.rights[].receipt | summary.rights[].receipt | 접수정보 | text | 2025년6월21일 제78131호 |
| summary.rights[].main | summary.rights[].main | 주요등기사항 | text | 채권최고액 금361,000,000원  근저당권자 중소기업은행 |
| summary.rights[].target_owner | summary.rights[].target_owner | 대상소유자 | text | 이민빈 |
| page_label | page_label | 쪽번호 | text | 2/2 |
| gapgu[].change | gapgu[].change | 변경사항 | text | 김태유의 주소 세종특별자치시 갈매로 202, 123동 2504호 (보람동, 자이파크) |
| eulgu[].change | eulgu[].change | 변경사항 | text | 채권최고액 금131,000,000원 |
| gapgu[].right_holder | gapgu[].right_holder | 권리자 | text | 국민건강보험공단 |
| gapgu[].trust_no | gapgu[].trust_no | 신탁원부 | text | 신탁원부 제2022-9693호 |
| eulgu[].period | eulgu[].period | 존속기간 | text | 1996년4월24일부터 1998년4월23일까지 |
| eulgu[].jeonse_holder | eulgu[].jeonse_holder | 전세권자 | text | 마예태 900930-******* |
| eulgu[].jeonse_holder_address | eulgu[].jeonse_holder_address | 전세권자주소 | text | 서울특별시 송파구 백제고분로 29, 120동 903호 (문정동, 롯데캐슬파크) |
| gapgu[].agency | gapgu[].agency | 처분청 | text | 북대전세무서 |

연결 업무 mortgage · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 jeonse_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### building_register · 집합건축물대장(전유부)

그룹: 부동산 (`real_estate`)

집합건축물대장(전유부, 갑) 등본.  소유자 변동 이력이 많거나 공용부분이 많은 경우(heavy)는 표를 세로로 쌓아 여러 쪽이 된다.

연결 업무: 주택담보대출 (mortgage)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| confirm_no | confirm_no | 문서확인번호 | text | 3188-4949-1246-2345 |
| unique_no | unique_no | 고유번호 | text | 4156211400-3-00870000 |
| building_name | building_name | 명칭 | text | 한신휴플러스에듀포레 제115동 |
| unit_name | unit_name | 호명칭 | text | 115동 2104호 |
| site_location | site_location | 대지위치 | text | 경기도 수원시 영통구 원천동 |
| jibun | jibun | 지번 | text | 87 |
| road_address | road_address | 도로명주소 | text | 경기도 수원시 영통구 매탄로 376 |
| exclusive[].kind | exclusive[].kind | 구분 | text | 주 |
| exclusive[].floor | exclusive[].floor | 층별 | text | 21층 |
| exclusive[].structure | exclusive[].structure | 구조 | text | 철근콘크리트구조 |
| exclusive[].usage | exclusive[].usage | 용도 | text | 아파트 |
| exclusive[].area | exclusive[].area | 면적(㎡) | number | 101.84 |
| common[].kind | common[].kind | 구분 | text | 주 |
| common[].floor | common[].floor | 층별 | text | 각층 |
| common[].structure | common[].structure | 구조 | text | 철근콘크리트구조 |
| common[].usage | common[].usage | 용도 | text | 계단실,복도,승강기 |
| common[].area | common[].area | 면적(㎡) | number | 24.60 |
| owners[].name | owners[].name | 성명(명칭) | text | 주식회사쌍용건설 |
| owners[].rrn | owners[].rrn | 주민(법인)등록번호 | rrn | 171512-4430096 |
| owners[].address | owners[].address | 주소 | text | 경기도 수원시 영통구 시청로 108 |
| owners[].share | owners[].share | 소유권지분 | text | 1/1 |
| owners[].change_date | owners[].change_date | 변동일 | date | 1994.11.04 |
| owners[].change_cause | owners[].change_cause | 변동원인 | text | 소유권보존 |
| house_prices[].base_date | house_prices[].base_date | 기준일 | date | 2025.01.01 |
| house_prices[].price | house_prices[].price | 공동주택(아파트)가격 | amount | 359,000,000 |
| officer | officer | 담당자 | text | 민원여권과 |
| officer_phone | officer_phone | 전화 | phone | 031-410-6139 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 수원시 영통구청장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 영통구청장인 |
| owners_note | owners_note | 비고 | text | ※ 이 건축물대장은 현소유자만 표시한 것입니다. |
| violation | violation | 위반건축물 | text | 위반건축물 |

연결 업무 mortgage · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### land_register · 토지대장

그룹: 부동산 (`real_estate`)

토지대장 등본 (집합건물 대지). 소유자 변동 이력이 길면 여러 쪽.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| unique_no | unique_no | 고유번호 | text | 4156211400-10087-0000 |
| drawing_no | drawing_no | 도면번호 | number | 47 |
| issue_no | issue_no | 발급번호 | number | 202644552441 |
| location | location | 토지소재 | text | 경기도 수원시 영통구 원천동 |
| sheet_no | sheet_no | 장번호 | text | 1-2 |
| processed_time | processed_time | 처리시각 | text | 15시 41분 19초 |
| jibun | jibun | 지번 | text | 87 |
| scale | scale | 축척 | text | 1:1200 |
| issuer_name | issuer_name | 발급자 | text | 인터넷민원 |
| land[].category | land[].category | 지목 | text | (08)대 |
| land[].area | land[].area | 면적 | number | 34,688.3 |
| land[].reason | land[].reason | 사유 | text | (20)1992년 03월 13일 등록전환 |
| owners[].change_date | owners[].change_date | 변동일자 | date | 1994년 11월 04일 |
| owners[].change_cause | owners[].change_cause | 변동원인 | text | (01)소유권보존 |
| owners[].address | owners[].address | 주소 | text | 경기도 수원시 영통구 시청로 108 |
| owners[].name | owners[].name | 성명또는명칭 | text | 주식회사쌍용건설 |
| owners[].reg_no | owners[].reg_no | 등록번호 | text | 171512-4430096 |
| owners[].co_owners | owners[].co_owners | 공유자 | text | 외 1,344인 |
| grades[].date | grades[].date | 등급수정년월일 | text | 1984.07.01. 수정 |
| grades[].grade | grades[].grade | 토지등급 | number | 149 |
| land_prices[].base_date | land_prices[].base_date | 개별공시지가기준일 | date | 2020/01/01 |
| land_prices[].price | land_prices[].price | 개별공시지가 | amount | 2,529,000 |
| zoning | zoning | 용도지역 | text | 준주거지역 |
| issue_date | issue_date | 발급일 | date | 2026년 1월 31일 |
| issuer | issuer | 발급기관 | text | 수원시 영통구청장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 영통구청장인 |

### sales_contract · 부동산 매매계약서

그룹: 부동산 (`real_estate`)

부동산(아파트) 매매계약서 (공인중개사 중개).

연결 업무: 주택담보대출 (mortgage)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| property.location | property.location | 소재지 | text | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신휴플러스에듀포레) |
| property.land_category | property.land_category | 지목 | text | 대 |
| property.land_right | property.land_right | 대지권 | text | 소유권대지권 31,054.7분의 54.47 |
| property.land_area | property.land_area | 면적 | text | 54.47㎡ |
| property.structure | property.structure | 구조 | text | 철근콘크리트구조 |
| property.usage | property.usage | 용도 | text | 공동주택(아파트) |
| property.building_area | property.building_area | 면적 | text | 101.84㎡ |
| payment.price | payment.price | 매매대금 | amount | 금 오억육천만원정 (₩560,000,000) |
| payment.down | payment.down | 계약금 | amount | 금 오천육백만원정 (₩56,000,000) |
| payment.middle | payment.middle | 중도금 | amount | 금 일억칠천만원정 (₩170,000,000) |
| payment.middle_date | payment.middle_date | 중도금지급일 | date | 2025년 10월 14일 |
| payment.balance | payment.balance | 잔금 | amount | 금 삼억삼천사백만원정 (₩334,000,000) |
| payment.balance_date | payment.balance_date | 잔금지급일 | date | 2025년 11월 03일 |
| specials[] | specials[] | 특약사항 | text | 1. 현 시설물 상태의 계약이며, 매수인은 등기사항증명서 및 현장을 확인하고 계약함. |
| contract_date | contract_date | 계약일 | date | 2025년 09월 16일 |
| seller.address | counterparty.address | 주소 | text | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신휴플러스에듀포레) |
| seller.rrn | seller.rrn | 주민등록번호 | rrn | 570508-1456825 |
| seller.phone | seller.phone | 전화 | phone | 010-6594-7883 |
| seller.name | counterparty.name | 성명 | text | 박기우 |
| seal.seller | seal.seller | 매도인 | seal | 반원인 |
| sign.seller | sign.seller | 매도인 | signature | 여혜인 |
| buyer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| buyer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| buyer.phone | customer.phone | 전화 | phone | 010-5907-7253 |
| buyer.name | customer.name | 성명 | text | 박찬연 |
| seal.buyer | seal.customer | 매수인 | seal | 강순준 |
| sign.buyer | sign.customer | 매수인 | signature | 박찬연 |
| brokers[].office_address | brokers[].office_address | 사무소소재지 | text | 경기도 수원시 영통구 매탄로 29, 1층 108호 (원천동) |
| brokers[].office_name | brokers[].office_name | 사무소명칭 | text | 한신휴공인중개사 |
| brokers[].representative | brokers[].representative | 대표 | text | 문채현 |
| brokers[].reg_no | brokers[].reg_no | 등록번호 | text | 29669-2012-02206 |
| brokers[].phone | brokers[].phone | 전화 | phone | 031-661-0605 |
| co_seller.address | co_seller.address | 주소 | text | 대구광역시 수성구 수성로 401, 107동 2004호 (지산동, 센트레빌에듀포레아파트) |
| co_seller.rrn | co_seller.rrn | 주민등록번호 | rrn | 590110-1645169 |
| co_seller.phone | co_seller.phone | 전화 | phone | 010-6479-6446 |
| co_seller.name | co_seller.name | 성명 | text | 김찬민 |
| seal.co_seller | seal.co_seller | 공동매도인 | seal | 김찬민 |
| sign.co_seller | sign.co_seller | 공동매도인 | signature | 최희원 |
| seller_agent.address | seller_agent.address | 대리인주소 | text | 서울특별시 영등포구 국제금융로 322, 122동 2001호 (신길동, 한신휴플러스아파트) |
| seller_agent.rrn | seller_agent.rrn | 대리인주민등록번호 | rrn | 650531-1503031 |
| seller_agent.name | seller_agent.name | 대리인성명 | text | 우건유 |
| seal.seller_agent | seal.seller_agent | 매도인대리인 | seal | 석진연 |
| sign.seller_agent | sign.seller_agent | 매도인대리인 | signature | 우건유 |
| brokers[].assistant | brokers[].assistant | 소속공인중개사 | text | 현수은 |
| co_buyer.address | related.address | 주소 | text | 서울특별시 강남구 도곡로 458-8, 102동 1102호 (논현동, 우성1차아파트) |
| co_buyer.rrn | related.rrn | 주민등록번호 | rrn | 820218-1260586 |
| co_buyer.phone | related.phone | 전화 | phone | 010-9382-0528 |
| co_buyer.name | related.name | 성명 | text | 이석인 |
| seal.co_buyer | seal.related | 공동매수인 | seal |  |
| sign.co_buyer | sign.related | 공동매수인 | signature | 이석인 |

연결 업무 mortgage · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### lease_contract · 주택임대차표준계약서

그룹: 부동산 (`real_estate`)

주택임대차표준계약서 (전세). 임대인 = 기존 소유자(seller), 임차인 = 본인.

연결 업무: 전세자금대출 (jeonse_loan)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| landlord_name | counterparty.name | 임대인 | text | 박기우 |
| tenant_name | customer.name | 임차인 | text | 박찬연 |
| house.location | property.location | 소재지 | text | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신휴플러스에듀포레) |
| house.land_category | house.land_category | 지목 | text | 대 |
| house.land_area | house.land_area | 토지면적 | text | 31,054.7㎡ |
| house.structure_usage | house.structure_usage | 구조·용도 | text | 철근콘크리트구조 / 공동주택(아파트) |
| house.building_area | house.building_area | 건물면적 | text | 101.84㎡ |
| house.lease_part | house.lease_part | 임차할부분 | text | 전부 (101.84㎡) |
| contract_type | contract_type | 계약의종류 | checkbox | 신규 계약 |
| tax_arrears | tax_arrears | 미납국세·지방세 | text | 없음 |
| prior_fixed_date | prior_fixed_date | 선순위확정일자현황 | text | 해당 없음 |
| fixed_date.date | fixed_date.date | 확정일자 | date | 2026.01.27 |
| fixed_date.no | fixed_date.no | 확정일자번호 | text | 2026-7849 |
| fixed_date.office | fixed_date.office | 확정일자부여기관 | text | 영통구 원천동행정복지센터 |
| deposit | deposit | 보증금 | amount | 금 삼억육천만원정 (₩360,000,000) |
| down_payment | down_payment | 계약금 | amount | 금 삼천육백만원정 (₩36,000,000) |
| balance | balance | 잔금 | amount | 금 삼억이천사백만원정 (₩324,000,000) |
| balance_date | balance_date | 잔금지급일 | date | 2026년 03월 03일 |
| management_fee | management_fee | 관리비 | text | 관리규약에 따라 관리주체가 부과하는 금액 |
| handover_date | handover_date | 인도일 | date | 2026년 03월 03일 |
| end_date | end_date | 임대차종료일 | date | 2028년 03월 02일 |
| specials[] | specials[] | 특약사항 | text | 1. 주택을 인도받은 임차인은 2026년 3월 3일까지 주민등록(전입신고)과 주택임대차계약서상 확정일자를 받기로 하고, 임대인은 2026년 3월 5일(최소한 임차인의 위 약정일자 이틀 후부터 가능)에 저당권 등 담보권을 설정할 수 있다. |
| contract_date | contract_date | 계약일 | date | 2026년 01월 26일 |
| landlord.address | counterparty.address | 주소 | text | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신휴플러스에듀포레) |
| landlord.rrn | landlord.rrn | 주민등록번호 | rrn | 570508-1456825 |
| landlord.phone | landlord.phone | 전화 | phone | 010-6594-7883 |
| landlord.name | landlord.name | 성명 | text | 박기우 |
| seal.landlord | seal.landlord | 임대인 | seal | 박기우 |
| sign.landlord | sign.landlord | 임대인 | signature | 반원인 |
| tenant.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| tenant.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| tenant.phone | customer.phone | 전화 | phone | 010-5907-7253 |
| tenant.name | tenant.name | 성명 | text | 박찬연 |
| seal.tenant | seal.customer | 임차인 | seal | 현예지 |
| sign.tenant | sign.customer | 임차인 | signature | 박찬연 |
| brokers[].office_address | brokers[].office_address | 사무소소재지 | text | 경기도 수원시 영통구 매탄로 68, 1층 111호 (원천동) |
| brokers[].office_name | brokers[].office_name | 사무소명칭 | text | 한신휴공인중개사사무소 |
| brokers[].representative | brokers[].representative | 대표 | text | 위영지 |
| brokers[].reg_no | brokers[].reg_no | 등록번호 | text | 41835-2020-01056 |
| brokers[].phone | brokers[].phone | 전화 | phone | 031-885-2129 |
| co_landlord.address | co_landlord.address | 주소 | text | 대구광역시 수성구 수성로 401, 107동 2004호 (지산동, 센트레빌에듀포레아파트) |
| co_landlord.rrn | co_landlord.rrn | 주민등록번호 | rrn | 590110-1645169 |
| co_landlord.phone | co_landlord.phone | 전화 | phone | 010-6479-6446 |
| co_landlord.name | co_landlord.name | 성명 | text | 김찬민 |
| seal.co_landlord | seal.co_landlord | 공동임대인 | seal | 정건수 |
| sign.co_landlord | sign.co_landlord | 공동임대인 | signature | 김찬민 |
| brokers[].assistant | brokers[].assistant | 소속공인중개사 | text | 공건인 |
| landlord_agent.address | landlord_agent.address | 대리인주소 | text | 부산광역시 해운대구 달맞이길 142, 114동 2403호 (중동, 센트레빌아파트) |
| landlord_agent.rrn | landlord_agent.rrn | 대리인주민등록번호 | rrn | 790510-2944862 |
| landlord_agent.name | landlord_agent.name | 대리인성명 | text | 심정아 |
| seal.landlord_agent | seal.landlord_agent | 임대인대리인 | seal | 송영아 |
| sign.landlord_agent | sign.landlord_agent | 임대인대리인 | signature | 심정아 |

연결 업무 jeonse_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### move_in_household_list · 전입세대확인서

그룹: 부동산 (`real_estate`)

전입세대확인서(열람). 해당 주소에 전입신고된 세대주 목록.  다세대·오피스텔을 건물 전체(동·호 없이)로 열람하면 여러 세대가 나오고, 많으면 여러 쪽이 된다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| issue_no | issue_no | 발급번호 | text | 8136-8334-8254-1287 |
| issue_date | issue_date | 발급일자 | date | 2026.01.31 |
| kind | kind | 열람·교부구분 | text | 교부 |
| address | address | 건물또는시설소재지 | text | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신휴플러스에듀포레) |
| jibun_address | jibun_address | 지번주소 | text | 경기도 수원시 영통구 원천동 87 115동 2104호 |
| households[].no | households[].no | 순번 | number | 1 |
| households[].head_name | households[].head_name | 세대주성명 | text | 박*연 |
| households[].move_in_date | households[].move_in_date | 전입일자 | date | 2025-11-11 |
| households[].reg_type | households[].reg_type | 등록구분 | text | 거주자 |
| households[].first_name | households[].first_name | 최초전입자성명 | text | 박*연 |
| households[].first_date | households[].first_date | 최초전입일자 | date | 2025-11-11 |
| households[].first_reg_type | households[].first_reg_type | 최초전입자등록구분 | text | 거주자 |
| households[].cohabitants | households[].cohabitants | 동거인수 | number | 0 |
| applicant.name | customer.name | 성명 | text | 박찬연 |
| applicant.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1****** |
| applicant.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| applicant.purpose | applicant.purpose | 열람·교부목적 | text | 금융기관 대출(주택담보대출) |
| view_date | view_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 영통구 원천동장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 동장의인 |
| cohabitants[].no | cohabitants[].no | 순번 | number | 1 |
| cohabitants[].name | cohabitants[].name | 동거인성명 | text | 심*민 |
| cohabitants[].move_in_date | cohabitants[].move_in_date | 전입일자 | date | 2010-02-25 |
| cohabitants[].reg_type | cohabitants[].reg_type | 등록구분 | text | 거주자 |
| households[].unit | households[].unit | 동·호 | text | 101호 |

### hf407 · 본인확인서(FATCA CRS 법인,임의단체용) 본문 설명서(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.407 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| followingbusinesses | followingbusinesses | followingbusinesses). | text |  |
| bankruptcy | bankruptcy | bankruptcy | text |  |
| RevenueCode | RevenueCode | RevenueCode | text |  |
| USbank | USbank | (6)U.S.bank | text |  |
| FATCANonReporting | FATCANonReporting | FATCANon-Reporting | text |  |
| requirements | requirements | requirements | text |  |
| Investment | Investment | Investment | text |  |
| BActiveNFFEs | BActiveNFFEs | B.ActiveNFFEs | text |  |
| Participation | Participation | Participation | text |  |
| Retirement | Retirement | Retirement | text |  |
| Fund | Fund | Fund | text |  |
| NonReportingFI | NonReportingFI | Non-ReportingFI | text |  |
| Investment2 | Investment2 | Investment | text |  |
| Office | Office | Office | text |  |
| Retirement2 | Retirement2 | Retirement | text |  |
| Fund2 | Fund2 | Fund | text |  |
| CRSNonReporting | CRSNonReporting | CRSNon-Reporting | text |  |
| Services | Services | Services | text |  |
| Commission | Commission | Commission | text |  |
| Vehicle | Vehicle | Vehicle | text |  |
| Office2 | Office2 | Office | text |  |
| Retirement3 | Retirement3 | Retirement | text |  |
| Fund3 | Fund3 | Fund | text |  |

### hf408 · 본인확인서(FATCA CRS 개인,개인사업자용)(국문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.408 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.surname_en | customer.surname_en | 성(SurName) | text | PARK |
| customer.given_name_en | customer.given_name_en | 이름(GivenName) | text | CHANYEON |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| check.FATCA | check.FATCA | FATCA | checkbox | 미국세법상 미국거주자 |
| check.CRS | check.CRS | CRS | checkbox | 미국이외의 해외거주자 |
| check.해당없음 | check.해당없음 | 해당없음 | checkbox | 모두 해당사항없음 |
| tax.residence_list[].country | tax.residence_list[].country | 거주관할권*(1) | text | 중국 |
| tax.residence_list[].tin | tax.residence_list[].tin | 납세자번호(TIN) | text | 009-923882-29493 |
| customer.overseas_address | customer.overseas_address | 해외영문주소 | text | 45 Le Loi St, District 1, Ho Chi Minh City |
| check.미발급국가 | check.미발급국가 | 미발급국가 | checkbox | 미발급국가 |
| check.미발급국가2 | check.미발급국가2 | 미발급국가 | checkbox | 조세당국이 요구하지 않음 |
| tax.no_tin_reason | tax.no_tin_reason | 내국인또는거주자증명서*또는반증증표*을제출한경우 | text | 본인 요청 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 인성명 | text | 박찬연 |
| seal.signer | seal.customer | 인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 인성명 | signature | 강순준 |
| signer2.name | signer2.name | 대리인성명 | text | 강석호 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 김수연 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 강석호 |
| date2 | date2 | 작성일(년월일) | date | 2026.01.31 |
| customer.name | customer.name | 본인성명 | text | 박찬연 |
| agent.name | agent.name | 대리인성명 | text | 박영준 |
| agent.relation | agent.relation | 대리인관계 | text | 부 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 임주빈 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 손은연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김기예 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 박영혜 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 박은혜 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 채영승 |

### hf409 · 본인확인서(FATCA CRS 법인,임의단체용) 본문 설명서(국문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.409 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 는기관 | 는기관 | 는기관 | text |  |
| 능동적비금융법인여부 | 능동적비금융법인여부 | 능동적비금융법인여부 | text |  |
| 미함 | 미함 | 미함. | text |  |
| 재개하려는의도로조직변경중인경우 | 재개하려는의도로조직변경중인경우 | 재개하려는의도로조직변경중인경우 | text |  |
| 된관계회사그룹 | 된관계회사그룹 | 된관계회사그룹 | text |  |
| 위법인에귀속될것을요구할것 | 위법인에귀속될것을요구할것 | 위법인에귀속될것을요구할것 | text |  |
| 미국미국정부소유기관미국정부대행기관 | 미국미국정부소유기관미국정부대행기관 | 미국,미국정부소유기관,미국정부대행기관 | text |  |
| 미국연방세법제581조에정의된은행 | 미국연방세법제581조에정의된은행 | 미국연방세법제581조에정의된은행 | text | 카카오뱅크 |
| 미국연방세법제6045조에정의된중개인 | 미국연방세법제6045조에정의된중개인 | 미국연방세법제6045(c)조에정의된중개인 | text |  |
| 유기관또는대행기관 | 유기관또는대행기관 | 유기관또는대행기관 | text |  |
| 라미국증권거래위원회에등록된법인 | 라미국증권거래위원회에등록된법인 | 라미국증권거래위원회에등록된법인 | text |  |
| 신탁 | 신탁 | 신탁 | text |  |
| 여등록된자 | 여등록된자 | 여등록된자 | text |  |
| 다음의요건을모두충족하는금융기관 | 다음의요건을모두충족하는금융기관 | 다음의요건을모두충족하는금융기관 | text | 카카오뱅크 |
| 다음의요건을모두충족하는금융기관2 | 다음의요건을모두충족하는금융기관2 | 다음의요건을모두충족하는금융기관 | text | 하나은행 |
| 구분 | 구분 | 구분[FATCA비보고대상유형] | text |  |
| 가법에따라금융회사로인가받고규제될것 | 가법에따라금융회사로인가받고규제될것 | 가.법에따라금융회사로인가받고규제될것 | text | 국민은행 |
| 관행을가지지아니할것 | 관행을가지지아니할것 | 관행을가지지아니할것 | text |  |
| 다음의요건을모두충족하는금융기관3 | 다음의요건을모두충족하는금융기관3 | 다음의요건을모두충족하는금융기관 | text | 국민은행 |
| 다음의요건을모두충족하는투자기구 | 다음의요건을모두충족하는투자기구 | 다음의요건을모두충족하는투자기구 | text |  |
| 가투자법인이아닐것 | 가투자법인이아닐것 | 가.투자법인이아닐것 | text |  |
| 의정보를보고하는신탁 | 의정보를보고하는신탁 | 의정보를보고하는신탁 | text |  |
| 사에해당하는경우로한정한다 | 사에해당하는경우로한정한다 | 사에해당하는경우로한정한다 | text |  |
| 부여받을것 | 부여받을것 | 부여받을것 | text |  |
| 별번호를포함할것 | 별번호를포함할것 | 별번호를포함할것 | text | 846-064434-12299 |
| 바후원자로서의지위를취소하지아니할것 | 바후원자로서의지위를취소하지아니할것 | 바.후원자로서의지위를취소하지아니할것 | text |  |
| 요건을충족하는피지배외국회사 | 요건을충족하는피지배외국회사 | 요건을충족하는피지배외국회사 | text |  |
| 해완전히소유되는금융회사일것 | 해완전히소유되는금융회사일것 | 해완전히소유되는금융회사일것 | text | 우리은행 |
| 후원자로서의지위를취소하지아니할것 | 후원자로서의지위를취소하지아니할것 | 후원자로서의지위를취소하지아니할것 | text |  |
| 법인 | 법인 | 법인 | text |  |
| 가투자자문제공 | 가투자자문제공 | 가.투자자문제공 | text |  |
| 용을포함한다 | 용을포함한다 | 용을포함한다 | text |  |
| 다음의요건을모두충족해야함 | 다음의요건을모두충족해야함 | 다음의요건을모두충족해야함 | text |  |
| 다음의요건을모두충족해야함2 | 다음의요건을모두충족해야함2 | 다음의요건을모두충족해야함 | text |  |
| 가한국에서설립된펀드일것 | 가한국에서설립된펀드일것 | 가.한국에서설립된펀드일것 | text |  |
| 에만분배또는인출이가능할것 | 에만분배또는인출이가능할것 | 에만분배또는인출이가능할것 | text |  |
| 다음의요건을모두충족해야함3 | 다음의요건을모두충족해야함3 | 다음의요건을모두충족해야함 | text |  |
| 별정우체국법에의한별정우체국연금관리단 | 별정우체국법에의한별정우체국연금관리단 | 별정우체국법에의한별정우체국연금관리단 | text |  |
| 다음각목의요건을모두충족하는금융회사 | 다음각목의요건을모두충족하는금융회사 | 다음각목의요건을모두충족하는금융회사 | text | 신한은행 |
| 가한국에서설립된펀드일것2 | 가한국에서설립된펀드일것2 | 가.한국에서설립된펀드일것 | text |  |
| 할것 | 할것 | 할것 | text |  |
| 수익자또는참가자 | 수익자또는참가자 | 수익자또는참가자 | text |  |
| 가투자법인라는이유만으로금융회사일것 | 가투자법인라는이유만으로금융회사일것 | 가.투자법인라는이유만으로금융회사일것 | text | 카카오뱅크 |
| 채권지분을소유할것 | 채권지분을소유할것 | 채권지분을소유할것 | text |  |
| 연금관리단 | 연금관리단 | 연금관리단 | text |  |
| 구분2 | 구분2 | 구분[CRS비보고대상유형] | text |  |
| 금융회사 | 금융회사 | 금융회사 | text | 하나은행 |
| 를보고하는신탁 | 를보고하는신탁 | 를보고하는신탁 | text |  |
| 다음의요건을모두충족해야함4 | 다음의요건을모두충족해야함4 | 다음의요건을모두충족해야함 | text |  |
| 다음의요건을모두충족해야함5 | 다음의요건을모두충족해야함5 | 다음의요건을모두충족해야함 | text |  |
| 별정우체국법에의한별정우체국연금관리단2 | 별정우체국법에의한별정우체국연금관리단2 | 별정우체국법에의한별정우체국연금관리단 | text |  |
| 연금간리단 | 연금간리단 | 연금간리단 | text |  |

### hf410 · 본인확인서(FATCA CRS 법인,임의단체용)(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.410 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| NameofEntity | NameofEntity | NameofEntity | text |  |
| BusinessRegistrationNo | BusinessRegistrationNo | BusinessRegistrationNo. | biz_no | 264-82-36559 |
| PhoneNo | PhoneNo | PhoneNo. | phone | 010-5907-7253 |
| TaxpayerIdentificationNo | TaxpayerIdentificationNo | TaxpayerIdentificationNo | text | 222-787118-55738 |
| customer.address | customer.address | Address(HeadOffice'sAddress) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| NameofEntity2 | NameofEntity2 | NameofEntity | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 오윤우 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 백규린 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 한예진 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 최유영 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 하경우 |
| GIINKIINEINNO | GIINKIINEINNO | GIIN/KIIN/EINNO | text |  |
| JurisdictionofResidence | JurisdictionofResidence | JurisdictionofResidence | text |  |
| JurisdictionofResidence2 | JurisdictionofResidence2 | JurisdictionofResidence | text |  |
| JurisdictionofResidence3 | JurisdictionofResidence3 | JurisdictionofResidence | text |  |
| GivenName | GivenName | GivenName | text |  |
| TaxpayerIdentificationNO | TaxpayerIdentificationNO | TaxpayerIdentificationNO | amount |  |
| Overseaaddress | Overseaaddress | Overseaaddress | text |  |
| GivenName2 | GivenName2 | GivenName | text |  |
| TaxpayerIdentificationNO2 | TaxpayerIdentificationNO2 | TaxpayerIdentificationNO | amount |  |
| Overseaaddress2 | Overseaaddress2 | Overseaaddress | text |  |
| GivenName3 | GivenName3 | GivenName | text |  |
| TaxpayerIdentificationNO3 | TaxpayerIdentificationNO3 | TaxpayerIdentificationNO | amount |  |
| Overseaaddress3 | Overseaaddress3 | Overseaaddress | text |  |
| check.Nonissuingc | check.Nonissuingc | Non-issuingcountry | checkbox | Not required by tax authority |
| check.Nonissuingc2 | check.Nonissuingc2 | Non-issuingcountry | checkbox | Not aqucired (write the reason |
| check.Nonissuingc3 | check.Nonissuingc3 | Non-issuingcountry | checkbox | Non-issuing country |
| SareRatio | SareRatio | SareRatio(%)* | text |  |
| Surname | Surname | Surname | text |  |
| SareRatio2 | SareRatio2 | SareRatio(%)* | text |  |
| Surname2 | Surname2 | Surname | text |  |
| SareRatio3 | SareRatio3 | SareRatio(%)* | text |  |
| Surname3 | Surname3 | Surname | text |  |
| customer.birth | customer.birth | DateofBirth | date | 1990년 2월 10일 |
| customer.birth2 | customer.birth2 | DateofBirth | date | 1990년 2월 10일 |
| customer.birth3 | customer.birth3 | DateofBirth | date | 1990년 2월 10일 |

### hf411 · [필수]본인 행정정보 제공 요구서(공공마이데이터 수신 묶음정보用 - 주민등록표 등·초본 조회)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.411 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일 | date | 1990-02-10 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 이용기관 | 이용기관 | 이용기관 | text |  |
| 제공유형 | 제공유형 | 제공유형 | text |  |
| customer.name2 | customer.name2 | 성명 | text | 박찬연 |
| customer.birth2 | customer.birth2 | 생년월일 | date | 1990-02-10 |
| customer.phone2 | customer.phone2 | 연락처 | phone | 010-5907-7253 |
| 하나은행 | 하나은행 | (주)하나은행 | text | 카카오뱅크 |
| 수신 | 수신 | 수신 | text |  |
| 일회성제공 | 일회성제공 | 일회성제공 | text |  |
| check.보기1 | check.보기1 | 보기1 | checkbox | 보기1 |
| check.제공요구하지않습니다 | check.제공요구하지않습니다 | 제공요구하지않습니다(아니오) | checkbox | 제공 요구하지 않습니다 (아니오) |
| check.에는해당되는곳에표를합 | check.에는해당되는곳에표를합 | 에는해당되는곳에√표를합니다. | checkbox | 에는 해당되는 곳에 √ 표를 합니다. |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 현예지 |
| 금융수신 | 금융수신 | ¶금융수신 | text |  |
| 금융거래의설정유지이행관리 | 금융거래의설정유지이행관리 | -금융거래의설정·유지·이행·관리 | text |  |
| 본인정보에관한사항 | 본인정보에관한사항 | [별지]본인정보에관한사항(상세항목) | text |  |

### hf412 · [필수]본인 행정정보 제공 요구서(공공마이데이터 수신 묶음정보用 - 사업자등록증명 조회)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.412 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 이용기관 | 이용기관 | 이용기관 | text |  |
| 제공유형 | 제공유형 | 제공유형 | text |  |
| customer.name2 | customer.name2 | 성명 | text | 박찬연 |
| customer.birth2 | customer.birth2 | 생년월일 | date | 1990.02.10 |
| customer.phone2 | customer.phone2 | 연락처 | phone | 010-5907-7253 |
| 하나은행 | 하나은행 | (주)하나은행 | text | 농협은행 |
| 수신 | 수신 | 수신 | text |  |
| 일회성제공 | 일회성제공 | 일회성제공 | text |  |
| check.보기1 | check.보기1 | 보기1 | checkbox | 보기1 |
| check.제공요구하지않습니다 | check.제공요구하지않습니다 | 제공요구하지않습니다(아니오) | checkbox | 제공 요구하지 않습니다 (아니오) |
| check.에는해당되는곳에표를합 | check.에는해당되는곳에표를합 | 에는해당되는곳에√표를합니다. | checkbox | 에는 해당되는 곳에 √ 표를 합니다. |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 김소윤 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| 금융수신 | 금융수신 | ¶금융수신 | text |  |
| 금융거래의설정유지이행관리 | 금융거래의설정유지이행관리 | -금융거래의설정·유지·이행·관리 | text |  |
| 본인정보에관한사항 | 본인정보에관한사항 | [별지]본인정보에관한사항(상세항목) | text |  |

### hf413 · 고객확인서(법인,고유번호나 납세번호가 있는 임의 단체용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.413 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].사업장 | 목록[].사업장 | 사업장(국내) | text |  |
| 대표자3 | 대표자3 | 대표자3 | text |  |
| 전화 | 전화 | 전화 | phone | 010-5907-7253 |
| 대표자1 | 대표자1 | 대표자1 | text |  |
| 대표자2 | 대표자2 | 대표자2 | text |  |
| 대표자32 | 대표자32 | 대표자3 | text |  |
| 한글명 | 한글명 | 한글명 | text | 신현예 |
| customer.name_en | customer.name_en | 영문명(외국법인필수) | text | PARK CHANYEON |
| company.biz_item | corp.biz_item | 업종(업태/종목) | text | 무역 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 전화2 | 전화2 | 전화 | phone | 010-5907-7253 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 전화3 | 전화3 | 전화 | phone | 010-5907-7253 |
| company.established | corp.established | 설립일 | date | 2018.11.01 |
| check.기업규모 | check.기업규모 | 기업규모 | checkbox | 중소기업 |
| check.상장여부 | check.상장여부 | 상장여부 | checkbox | 상장 |
| 목록[].영문명 | 목록[].영문명 | 영문명 | text |  |
| FAX | FAX | FAX | phone | 043-783-2775 |
| company.biz_no | corp.biz_no | 사업자등록번호(고유번호및납세번호등포함) | biz_no | 264-82-36559 |
| 설립목적 | 설립목적 | 설립목적(비영리법인,단체) | text | 의료비 |
| FAX2 | FAX2 | FAX | phone | 043-783-2775 |
| FAX3 | FAX3 | FAX | phone | 043-783-2775 |
| 홈페이지 | 홈페이지 | 홈페이지 | text |  |
| check.국내 | check.국내 | 국내 | checkbox | 유가증권시장 |
| 목록[].생년월일 | 목록[].생년월일 | 생년월일(사업자번호) | text | 2025.05.28 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| 목록[].국적 | 목록[].국적 | 국적(본점소재지) | text |  |
| check.일회성거래 | check.일회성거래 | 일회성거래(무통장입금,수표발행☞지급등) | checkbox | 상속 / 증여성거래 |
| check.대표자정보 | check.대표자정보 | 대표자정보 | checkbox | 각자대표 |
| check.뉴욕증권거래소 | check.뉴욕증권거래소 | 뉴욕증권거래소 | checkbox | 뉴욕증권거래소 |
| check.홍콩증권거래소 | check.홍콩증권거래소 | 홍콩증권거래소 | checkbox | 홍콩증권거래소 |
| check.예 | check.예 | 예(비영리단체) | checkbox | 아니오(비영리단체 해당안됨) |
| check.계좌개설 | check.계좌개설 | 계좌개설 | checkbox | 공과금 납부결제 |
| check.대출원리금상환결제 | check.대출원리금상환결제 | (예금,대출등) | checkbox | 대출원리금 상환 결제 |
| check.사업소득 | check.사업소득 | 사업소득 | checkbox | 부동산 임대소득 |
| check.상속증여 | check.상속증여 | 상속/증여 | checkbox | 상속 / 증여 |
| check.추가확인 | check.추가확인 | 추가확인 | checkbox | 대부업자 |
| check.필요업종 | check.필요업종 | 필요업종 | checkbox | 공인회계사업 |
| check.대표자 | check.대표자 | 대표자 | checkbox | 대리인 성명 |
| 거래목적 | 거래목적 | 거래목적 | text | 의료비 |
| 25이상의결권이있는주식출자지분을보유한사람 | 25이상의결권이있는주식출자지분을보유한사람 | 25%이상의결권이있는주식/출자지분을보유한사람 | text |  |
| 의결권있는주식및출자지분의최대소유자 | 의결권있는주식및출자지분의최대소유자 | 의결권있는주식및출자지분의최대소유자 | text |  |
| 대표자또는임원등의과반수를선임한주주 | 대표자또는임원등의과반수를선임한주주 | 대표자또는임원등의과반수를선임한주주 | text |  |
| 법인단체를사실상지배하는자 | 법인단체를사실상지배하는자 | 법인•단체를사실상지배하는자 | text |  |
| 법인단체의대표자중1인 | 법인단체의대표자중1인 | 법인•단체의대표자중1인 | text |  |
| 목록[].한글명 | 목록[].한글명 | 한글명(상호명) | text | 박찬연 |
| check.25이상의결권이있는주식출자지분을보유한사람 | check.25이상의결권이있는주식출자지분을보유한사람 | 25%이상의결권이있는주식/출자지분을보유한사람 | checkbox | 보기1 |
| check.의결권있는주식및출자지분의최대소유자 | check.의결권있는주식및출자지분의최대소유자 | 의결권있는주식및출자지분의최대소유자 | checkbox | 보기1 |
| check.대표자또는임원등의과반수를선임한주주 | check.대표자또는임원등의과반수를선임한주주 | 대표자또는임원등의과반수를선임한주주 | checkbox | 보기1 |
| check.법인단체를사실상지배하는자 | check.법인단체를사실상지배하는자 | 법인•단체를사실상지배하는자 | checkbox | 보기1 |
| check.법인단체의대표자중1인 | check.법인단체의대표자중1인 | 법인•단체의대표자중1인 | checkbox | 보기1 |
| 목록[].지분율 | 목록[].지분율 | 지분율 | number | 20 |
| 항목 | 항목 | 항목 | text |  |
| 목록[].Y | 목록[].Y | Y | text |  |
| 목록[].N | 목록[].N | N | text |  |
| 지배자 | 지배자 | 지배자 | text |  |
| 목록[].지배형태 | 목록[].지배형태 | 지배형태 | text |  |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| agent.birth | agent.birth | 생년월일 | date | 1962.12.19 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.phone | agent.phone | 전화번호 | phone | 010-6515-4769 |
| check.국가또는지방자치단체1 | check.국가또는지방자치단체1 | 국가또는지방자치단체1 | checkbox | 사업보고서 제출대상 법인 (상장법인 1) 등) |
| check.실제소유자와사실상지배자 | check.실제소유자와사실상지배자 | 실제소유자와사실상지배자가동일합니다 | checkbox | 실제소유자와 사실상지배자가 동일합니다 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | corp.name | 법인/단체명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 법인/단체명 | seal | (주)유니온무역 |
| sign.signer | sign.customer | 법인/단체명 | signature | 주식회사 한빛패션 |
| check.작성자 | check.작성자 | 작성자( | checkbox | 대표자 |
| customer.name | customer.name | 위임인(법인/단체명) | text | 박찬연 |

### hf414 · [필수] 개인(신용)정보 수집·이용·제공 동의서 [공공마이데이터 주민등록 등·초본 조회용]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.414 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 수집이용목적 | 수집이용목적 | 수집·이용목적 | text | 만기 해지 |
| 제공일로부터5년이내보유이용 | 제공일로부터5년이내보유이용 | -제공일로부터5년이내보유·이용 | text |  |
| 일반개인정보2 | 일반개인정보2 | ■일반개인정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 현예지 |
| signer2.name | agent.name | 대리인성명 | text | 김순우 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 이성원 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 김서호 |

### hf415 · [필수] 개인(신용)정보 제3자 제공 동의서 [공공마이데이터 주민등록 등·초본 조회용]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.415 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 하나은행 | 하나은행 | -(주)하나은행 | text |  |
| 고유식별정보 | 고유식별정보 | ■고유식별정보 | text |  |
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 이도민 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 강석호 |
| 산정보 | 산정보 | 산정보 | text |  |
| 본과동일한공공마이데이터 | 본과동일한공공마이데이터 | 본과동일한공공마이데이터 | text |  |
| 행정안전부주민등록등초본 | 행정안전부주민등록등초본 | ■행정안전부:주민등록등·초본 | text |  |

### hf416 · [필수] 개인(신용)정보 수집·이용·제공 동의서 [공공마이데이터 사업자정보 조회용]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.416 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 고유식별정보 | 고유식별정보 | ■고유식별정보 | text |  |
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집☞이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집☞이용에동의하십니까? | checkbox | 동의함 |
| 수집이용목적 | 수집이용목적 | 수집·이용목적 | text | 학자금 |
| 제공일로부터5년이내보유이용 | 제공일로부터5년이내보유이용 | -제공일로부터5년이내보유·이용 | text |  |
| 고유식별정보2 | 고유식별정보2 | ■고유식별정보 | text |  |
| 일반개인정보2 | 일반개인정보2 | ■일반개인정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 김서호 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 박영준 |

### hf417 · [필수] 개인(신용)정보 제3자 제공 동의서 [공공마이데이터 사업자정보 조회용]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.417 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 하나은행 | 하나은행 | -(주)하나은행 | text |  |
| 고유식별정보 | 고유식별정보 | ■고유식별정보 | text |  |
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 강순준 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 이도민 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 강석호 |
| 산정보 | 산정보 | 산정보 | text |  |
| 본과동일한공공마이데이터 | 본과동일한공공마이데이터 | 본과동일한공공마이데이터 | text |  |
| 국세청사업자등록증명 | 국세청사업자등록증명 | ■국세청:사업자등록증명 | text |  |

### hf418 · [필수] 개인(신용)정보 수집·이용 동의서 [비대면 스크래핑 서비스]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.418 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 고유식별정보 | 고유식별정보 | ■고유식별정보 | text |  |
| 일반개인정보 | 일반개인정보 | ■■일반개인정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 성명휴대전화번호자녀성명 | 성명휴대전화번호자녀성명 | 성명,휴대전화번호,자녀성명 | phone | 010-5907-7253 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 현예지 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 김순우 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 김순우 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 김서호 |

### hf419 · [필수] 개인(신용)정보 수집 · 이용 동의서 (비여신 금융거래)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.419 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 강석호 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 김수연 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 이도민 |
| signer3.name | signer3.name | 법정대리인성명 | text | 이도민 |
| seal.signer3 | seal.signer3 | 법정대리인성명 | seal | 이도민 |
| sign.signer3 | sign.signer3 | 법정대리인성명 | signature | 김순우 |
| 온오프라인거래연계및본인식별 | 온오프라인거래연계및본인식별 | -온·오프라인(금융)거래연계및본인식별 | text |  |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | -금융사고조사,분쟁해결,민원처리 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 검인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 조경린 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 오원도 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 안옥준 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 한다재 |

### hf420 · 비대면 계좌개설 안심차단 서비스 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.420 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.구분 | check.구분 | 구분 | checkbox | 신청 |
| check.대리인정보 | check.대리인정보 | 대리인정보 | checkbox | 임의대리인 신청시에도 신청내역에 대한 안내는 신청인(본인)에게 통지됩니다 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.birth | agent.birth | 생년월일 | date | 1962.12.19 |
| check.해제 | check.해제 | 해제 | checkbox | 해제 |
| check.휴대전화번호 | check.휴대전화번호 | 휴대전화번호 | checkbox | 신청내역 통지 동의 |
| 신청인과의관계 | 신청인과의관계 | 신청인과의관계 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 강순준 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| signer2.name | signer2.name | 대리인 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인 | seal | 김순우 |
| sign.signer2 | sign.agent | 대리인 | signature | 박영준 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 최용율 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 양선찬 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김석도 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 문옥하 |

### hf421 · [필수] 개인(신용)정보 수집·이용·제공·조회 동의서 [비대면 계좌개설 안심차단 서비스]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.421 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 고유식별정보 | 고유식별정보 | ■고유식별정보 | text |  |
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 수집이용목적 | 수집이용목적 | 수집·이용목적 | text | 주택구입 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | -금융사고조사,분쟁해결,민원처리 | text |  |
| 거부권리및불이익 | 거부권리및불이익 | 거부권리및불이익 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 정혁은 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 최건정 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 민예빈 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 추철현 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 박건지 |
| 목록[].고유식별정보 | 목록[].고유식별정보 | ■고유식별정보 | text |  |
| 목록[].공공정보등 | 목록[].공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| check.위고유식별정보조회에동의하십니까 | check.위고유식별정보조회에동의하십니까 | 위고유식별정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보조회에동의하십니까 | check.위개인정보조회에동의하십니까 | 위개인(신용)정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 강순준 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 강석호 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 박영준 |
| 거부권리및불이익2 | 거부권리및불이익2 | 거부권리및불이익 | text |  |

### hf422 · [필수] 개인(신용)정보 수집·이용·조회 동의서[비대면 계좌개설 안심차단 신청여부 조회용]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.422 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].고유식별정보 | 목록[].고유식별정보 | ■고유식별정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 비대면계좌개설안심차단신청여부조회 | 비대면계좌개설안심차단신청여부조회 | -비대면계좌개설안심차단신청여부조회 | text |  |
| 수집이용목적 | 수집이용목적 | 수집·이용목적 | text | 자녀 교육비 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | -금융사고조사,분쟁해결,민원처리 | text |  |
| 보유및이용기간 | 보유및이용기간 | 보유및이용기간 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 이순정 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 확인 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 문규도 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 우서혜 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 하형현 |
| check.위고유식별정보제공에동의하십니까2 | check.위고유식별정보제공에동의하십니까2 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보조회에동의하십니까 | check.위고유식별정보조회에동의하십니까 | 위고유식별정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보조회에동의하십니까 | check.위개인정보조회에동의하십니까 | 위개인(신용)정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 현예지 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 김순우 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 장민인 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 김순우 |

### hf423 · [선택] 개인(신용)정보 수집ㆍ이용 및 제공동의서 (상품서비스 안내 등)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.423 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위개인정보수집이용에동의하십니까안심 | check.위개인정보수집이용에동의하십니까안심 | 위개인(신용)정보수집·이용에동의하십니까?안심 | checkbox | 동의함 |
| check.광고성정보의수신을동의하시겠습니까 | check.광고성정보의수신을동의하시겠습니까 | 광고성정보의수신을동의하시겠습니까? | checkbox | 동의하지 않음 |
| check.14전체 | check.14전체 | 1~4전체 | checkbox | 보기1 |
| check.문자메시지 | check.문자메시지 | 문자메시지(SMS,LMS,모바일메시지등) | checkbox | 보기1 |
| check.전자우편 | check.전자우편 | 전자우편(이메일) | checkbox | 보기1 |
| 수집이용목적 | 수집이용목적 | 수집·이용목적 | text | 투자 목적 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 검인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 명희민 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 윤영지 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 검인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 정용정 |
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| 성명생년월일 | 성명생년월일 | 성명,생년월일 | date | 2025.05.12 |
| check.위개인정보제공에동의하십니까안심 | check.위개인정보제공에동의하십니까안심 | 위개인(신용)정보제공에동의하십니까?안심 | checkbox | 동의함 |
| 하나금융그룹계열사 | 하나금융그룹계열사 | -하나금융그룹계열사 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 성명 | text | 박찬연 |
| seal.signer | seal.customer | 성명 | seal | 이욱유 |
| sign.signer | sign.customer | 성명 | signature | 현예지 |
| signer2.name | agent.name | 법정대리인 | text | 박영준 |
| seal.signer2 | seal.agent | 법정대리인 | seal | 박영준 |
| sign.signer2 | sign.agent | 법정대리인 | signature | 김서호 |

### hf424 · [필수] 개인(신용)정보 제3자제공 동의서 [하나카드 발급_미성년자용]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.424 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 하나카드 | 하나카드 | 하나카드 | text |  |
| 고유식별정보 | 고유식별정보 | ■고유식별정보 | text |  |
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 현예지 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 강석호 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 이도민 |
| 제공받는자의이용목적 | 제공받는자의이용목적 | 제공받는자의이용목적 | text | 자녀 교육비 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |

### hf425 · [필수] 개인(신용)정보 제3자제공 동의서 [하나카드 발급_법정대리인용]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.425 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 하나카드 | 하나카드 | 하나카드 | text |  |
| 제공일로부터5년까지보유이용 | 제공일로부터5년까지보유이용 | -제공일로부터5년까지보유·이용 | text |  |
| 고유식별정보 | 고유식별정보 | ■고유식별정보 | text |  |
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 이민빈 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 박영준 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 위우호 |
| 제공받는자의이용목적 | 제공받는자의이용목적 | 제공받는자의이용목적 | text | 계좌 정리 |
| 우그기간을따름 | 우그기간을따름 | 우그기간을따름 | text |  |
| 휴대전화번호email주소 | 휴대전화번호email주소 | 휴대전화번호,e-mail주소 | phone | 010-5907-7253 |

### hf426 · 이의제기 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.426 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| customer.email | customer.email | 전자우편주소 | text | chanyeon363@naver.com |
| 개설점포 | 개설점포 | 개설점포 | text | 범어지점 |
| 예금종별 | 예금종별 | 예금종별 | text | 하나 정기예금 |
| customer.name | customer.name | 명의인 | text | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인성명 | text | 박찬연 |
| seal.signer | seal.customer | 신청인성명 | seal | 이욱유 |
| sign.signer | sign.customer | 신청인성명 | signature | 박찬연 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| customer.phone2 | customer.phone2 | 휴대전화번호 | phone | 010-5907-7253 |
| 금융회사 | 금융회사 | 금융회사 | text | 신한은행 |
| 지급정지 | 지급정지 | 지급정지 | text |  |
| account | account | 계좌번호 | account_no | 000-287736-52424 |

### hf427 · 아이부자 선불전자지급수단 잔액 상속(지급) 및 서비스 해지 요청서(위임장 겸용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.427 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일 | date | 900210 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 주된상속인 | 주된상속인 | 주된상속인(소득귀속인) | text |  |
| customer.birth2 | customer.birth2 | 생년월일 | date | 900210 |
| customer.phone2 | customer.phone2 | 연락처 | phone | 010-5907-7253 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| check.상속인 | check.상속인 | 상속인 | checkbox | 위임(별도위임장 작성) |
| check.상속인2 | check.상속인2 | 상속인 | checkbox | 본인 |
| check.상속인3 | check.상속인3 | 상속인 | checkbox | 위임(별도위임장 작성) |
| check.상속인4 | check.상속인4 | 상속인 | checkbox | 본인 |
| check.상속인5 | check.상속인5 | 상속인 | checkbox | 본인 |
| check.상속인6 | check.상속인6 | 상속인 | checkbox | 본인 |
| check.상속인7 | check.상속인7 | 상속인 | checkbox | 본인 |
| check.상속인8 | check.상속인8 | 상속인 | checkbox | 본인 |
| check.상속인9 | check.상속인9 | 상속인 | checkbox | 위임(별도위임장 작성) |
| 목록[].성명 | 목록[].성명 | 성명 | text | 여형지 |
| 목록[].생년월일 | 목록[].생년월일 | 생년월일 | text | 2025.08.25 |
| 목록[].연락처 | 목록[].연락처 | 연락처 | text | 010-5907-7253 |

### hf428 · 본인확인서(FATCA CRS 법인,임의단체용)(국문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.428 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 가고객정보 | 가고객정보 | 가.고객정보 | text |  |
| company.name | corp.name | 법인(단체)명 | text | (주)유니온무역 |
| 구분선택 | 구분선택 | 구분선택(☑) | text |  |
| company.name2 | company.name2 | 법인(단체)명 | text | (주)유니온무역 |
| 口국내법인 | 口국내법인 | 口국내법인(단체) | text |  |
| company.biz_no | corp.biz_no | 사업자번호 | biz_no | 264-82-36559 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 거주관할권 | 거주관할권 | 거주관할권 | text |  |
| 납세자번호 | 납세자번호 | 납세자번호(TIN) | text | 5925-5140 |
| 관할권주소 | 관할권주소 | 관할권(소재지)주소(본점,설립관할권) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 법인명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 법인명 | seal | 주식회사 대성패션 |
| sign.signer | sign.customer | 법인명 | signature | (주)유니온무역 |
| 나확인사항 | 나확인사항 | 나.확인사항 | text |  |
| 口11공익적법인 | 口11공익적법인 | 口11.공익적법인(단체) | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 원주도 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 김민영 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김환진 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 엄규민 |
| c | c | c | text |  |
| d | d | d | text |  |
| 口EIN口GIIN口기타 | 口EIN口GIIN口기타 | 口EIN口GIIN口기타 | text | 해당 없음 |
| 목록[].실질지배자 | 목록[].실질지배자 | 실질지배자(1) | text |  |
| 목록[].거주관할권 | 목록[].거주관할권 | 거주관할권(국가) | text |  |
| customer.name | customer.name | 이름(GivenName) | text | 박찬연 |
| 목록[].납세자번호 | 목록[].납세자번호 | 납세자번호(TIN) | text | 175-698208-49328 |
| customer.name2 | customer.name2 | 이름(GivenName) | text | 박찬연 |
| customer.name3 | customer.name3 | 이름(GivenName) | text | 박찬연 |
| 거주관할권주소 | 거주관할권주소 | 거주관할권주소(영문) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 거주관할권주소2 | 거주관할권주소2 | 거주관할권주소(영문) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 거주관할권주소3 | 거주관할권주소3 | 거주관할권주소(영문) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.미발급국가 | check.미발급국가 | 미발급국가 | checkbox | 미발급국가 |
| check.미발급국가2 | check.미발급국가2 | 미발급국가 | checkbox | 미취득 (사유기재 |
| check.미발급국가3 | check.미발급국가3 | 미발급국가 | checkbox | 미발급국가 |
| 지분율 | 지분율 | 지분율(%) | number | 10 |
| 성 | 성 | 성(Surname) | text |  |
| 지분율2 | 지분율2 | 지분율(%) | number | 100 |
| 성2 | 성2 | 성(Surname) | text |  |
| 지분율3 | 지분율3 | 지분율(%) | number | 30 |
| 성3 | 성3 | 성(Surname) | text |  |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| customer.birth2 | customer.birth2 | 생년월일 | date | 1990년 2월 10일 |
| customer.birth3 | customer.birth3 | 생년월일 | date | 1990년 2월 10일 |
| 口01주권상장법인 | 口01주권상장법인 | 口01.주권상장법인 | text |  |
| 口03미국정부기관등 | 口03미국정부기관등 | 口03.미국정부기관등 | text |  |
| 口25별정우체국연금관리단 | 口25별정우체국연금관리단 | 口25.별정우체국연금관리단 | text |  |

### hf429 · 본인확인서(FATCA CRS 개인,개인사업자용)(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.429 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| CustomerProfile | CustomerProfile | CustomerProfile | text |  |
| 목록[].value | 목록[].value | (CapitalLetter)* | amount |  |
| WhetherOverseasResidentorNot | WhetherOverseasResidentorNot | WhetherOverseasResidentorNot | text |  |
| IdentificationNumberetc | IdentificationNumberetc | IdentificationNumber(TIN),etc. | text |  |
| Reportingcountry | Reportingcountry | Reportingcountry | text |  |
| 목록[].FATCA | 목록[].FATCA | FATCA | text |  |
| 목록[].CRS | 목록[].CRS | CRS | text |  |
| NA | NA | N/A | text |  |
| Surname | Surname | Surname(성) | text |  |
| Surname2 | Surname2 | Surname(성) | text |  |
| GivenName | GivenName | GivenName(이름) | text |  |
| check.UScitizen | check.UScitizen | U.S.citizen(includingdualcitizenship) | checkbox | U.S. resident under U.S. tax law |
| check.Residentinac | check.Residentinac | ResidentinacountryotherthanU.S | checkbox | Resident in a country other than U.S |
| check.AllNA | check.AllNA | AllN/A | checkbox | All N/A |
| Jurisdictionof | Jurisdictionof | Jurisdictionof | text |  |
| Country | Country | Country*(2) | text | 영국 |
| OverseaEnglishaddress | OverseaEnglishaddress | OverseaEnglishaddress | text |  |
| Surname3 | Surname3 | Surname(성) | text |  |
| GivenName2 | GivenName2 | GivenName(이름) | text |  |
| customer.birth | customer.birth | DateofBirth | date | 1990년 2월 10일 |
| customer.birth2 | customer.birth2 | DateofBirth | date | 1990년 2월 10일 |
| 목록[].PhoneNo | 목록[].PhoneNo | PhoneNo. | phone | 010-5907-7253 |
| check.Nonissuingc | check.Nonissuingc | Non-issuingcountry | checkbox | Not requested by tax authority |
| check.Nonissuingc2 | check.Nonissuingc2 | Non-issuingcountry | checkbox | Not requested by tax authority |
| customer.birth3 | customer.birth3 | DateofBirth | date | 1990년 2월 10일 |
| PhoneNo | PhoneNo | PhoneNo. | phone | 010-5907-7253 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 김서현 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 제갈형성 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 문민성 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 기환린 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 선우규인 |

### hf430 · 민원신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.430 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].기타 | 목록[].기타 | 기타 | text | 해당 없음 |
| 기타 | 기타 | 기타 | text | 자동이체 같이 신청함 |
| 기타2 | 기타2 | 기타 | text | 해당 없음 |
| customer.email | customer.email | e-mail | text | chanyeon363@naver.com |
| agent.email | agent.email | e-mail | text | youngjun641@nate.com |
| signer.name | signer.name | 본인확인(직원기재) | text | 제갈승은 |
| seal.signer | seal.signer | 본인확인(직원기재) | seal | 제갈승은 |
| sign.signer | sign.signer | 본인확인(직원기재) | signature | 이경연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.name | customer.name | 신청인 | text | 박찬연 |
| 본인확인 | 본인확인 | 본인확인(직원기재) | text |  |
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 신용거래정보2 | 신용거래정보2 | ■신용거래정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까2 | check.위고유식별정보수집이용에동의하십니까2 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 본인성명 | text | 박찬연 |
| seal.signer2 | seal.customer | 본인성명 | seal | 이욱유 |
| sign.signer2 | sign.customer | 본인성명 | signature | 강순준 |
| signer3.name | agent.name | 대리인성명 | text | 김순우 |
| seal.signer3 | seal.agent | 대리인성명 | seal | 김순우 |
| sign.signer3 | sign.agent | 대리인성명 | signature | 장민인 |
| 기타3 | 기타3 | 기타 | text | 학자금 300만 (삼년) |
| 기타4 | 기타4 | 기타 | text | 해당 없음 |
| customer.email2 | customer.email2 | e-mail | text | chanyeon363@naver.com |
| agent.email2 | agent.email2 | e-mail | text | youngjun641@nate.com |
| signer4.name | signer4.name | 본인확인(직원기재) | text | 최민태 |
| seal.signer4 | seal.signer4 | 본인확인(직원기재) | seal | 이민태 |
| sign.signer4 | sign.signer4 | 본인확인(직원기재) | signature | 최민태 |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| signer5.name | signer5.name | 위임자(본인) | text | 박찬연 |
| seal.signer5 | seal.signer5 | 위임자(본인) | seal | 이욱유 |
| sign.signer5 | sign.signer5 | 위임자(본인) | signature | 박찬연 |
| 본인확인2 | 본인확인2 | 본인확인(직원기재) | text |  |

### hf431 · 전자금융거래 사고 피해 신고서(통합서류)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.431 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| company.name | corp.name | 법인명 | text | (주)유니온무역 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| check.진행관련SMS수신동의여부 | check.진행관련SMS수신동의여부 | 진행관련SMS수신동의여부】 | checkbox | 동의하지 않음 |
| check.이용자본인이직접지급지시 | check.이용자본인이직접지급지시 | 이용자본인이직접지급지시한금융거래(가족사칭,협박,대출사기등 | checkbox | 이용자 본인이 직접 지급지시한 금융거래(가족 사칭, 협박, 대출사기 등  |
| check.동거가족또는지인에의한거 | check.동거가족또는지인에의한거 | 동거가족또는지인에의한거래 | checkbox | 동거가족 또는 지인에 의한 거래 |
| check.이용자가접근매체를양도양 | check.이용자가접근매체를양도양 | 이용자가접근매체를양도·양수하거나질권을설정하는등전자금융거래법제 | checkbox | 이용자가 접근매체를 양도·양수하거나 질권을 설정하는 등 전자금융거래법 제 |
| check.법인인이용자의기관내지는 | check.법인인이용자의기관내지는 | 법인인이용자의기관내지는피용자로서법인을위한금융거래 | checkbox | 법인인 이용자의 기관 내지는 피용자로서 법인을 위한 금융거래 |
| check.재화의공급을가장한상거래 | check.재화의공급을가장한상거래 | 재화의공급을가장한상거래로서이용자본인의의지로신청·계약한금융거 | checkbox | 재화의 공급을 가장한 상거래로서 이용자 본인의 의지로 신청·계약한 금융거 |
| check.용역의제공을가장한거래로 | check.용역의제공을가장한거래로 | 용역의제공을가장한거래로서이용자본인의의지로신청·계약한금융거래 | checkbox | 용역의 제공을 가장한 거래로서 이용자 본인의 의지로 신청·계약한 금융거래 |
| check.불법적이거나비정상적인재 | check.불법적이거나비정상적인재 | 불법적이거나비정상적인재화의공급또는용역의제공등과관련된금융거 | checkbox | 불법적이거나 비정상적인 재화의 공급 또는 용역의 제공 등과 관련된 금융거 |
| check.간편송금업체를통한금융거 | check.간편송금업체를통한금융거 | 간편송금업체(OO페이)를통한금융거래 | checkbox | 간편송금업체(OO페이)를 통한 금융거래 |
| check.영업점창구를통한거래등대 | check.영업점창구를통한거래등대 | 영업점창구를통한거래등대면금융거래 | checkbox | 영업점 창구를 통한 거래 등 대면 금융거래 |
| check.은행의보이스피싱의심거래 | check.은행의보이스피싱의심거래 | 은행의보이스피싱의심거래감지등에따른피해예방안내에도불구하고 | checkbox | 은행의 보이스피싱 의심거래 감지 등에 따른 피해 예방 안내에도 불구하고  |
| check.본사고발생이전에사고발 | check.본사고발생이전에사고발 | 본사고발생이전에사고발생은행에서「전기통신금융사기피해방지및 | checkbox | 본 사고 발생 이전에 사고발생 은행에서 「전기통신금융사기 피해 방지 및 |
| check.신용체크카드물품구입단 | check.신용체크카드물품구입단 | 신용/체크카드물품구입,단기카드대출(현금서비스)및장기카드대출(카드 | checkbox | 신용/체크카드 물품 구입, 단기카드대출(현금서비스) 및 장기카드대출(카드 |
| check.사실관계확인결과전자금융 | check.사실관계확인결과전자금융 | 사실관계확인결과전자금융사고로보기어려운경우 | checkbox | 사실관계 확인 결과 전자금융사고로 보기 어려운 경우 |
| check.소송등법적분쟁이진행중이 | check.소송등법적분쟁이진행중이 | 소송등법적분쟁이진행중이거나판결이확정된경우 | checkbox | 소송 등 법적 분쟁이 진행중이거나 판결이 확정된 경우 |
| 피해신고제외대상확인 | 피해신고제외대상확인 | 피해신고제외대상확인 | text |  |
| 출금은행 | 출금은행 | 출금은행 | text | 하나은행 |
| 입금은행 | 입금은행 | 입금은행(상대은행) | text | 신한은행 |
| 출금은행2 | 출금은행2 | 출금은행 | text | 신한은행 |
| 입금은행2 | 입금은행2 | 입금은행(상대은행) | text | 우리은행 |
| 출금은행3 | 출금은행3 | 출금은행 | text | 국민은행 |
| 입금은행3 | 입금은행3 | 입금은행(상대은행) | text | 농협은행 |
| 사고발생총피해금액 | 사고발생총피해금액 | 사고발생총피해금액 | number | 7,110,000 |
| account | account | 출금계좌번호 | account_no | 000-287736-52424 |
| check.입금계좌예금주 | check.입금계좌예금주 | 입금(상대)계좌예금주 | checkbox | 타인( |
| account2 | account2 | 출금계좌번호 | account_no | 000-287736-52424 |
| check.입금계좌예금주2 | check.입금계좌예금주2 | 입금(상대)계좌예금주 | checkbox | 본인 |
| account3 | account3 | 출금계좌번호 | account_no | 000-287736-52424 |
| check.입금계좌예금주3 | check.입금계좌예금주3 | 입금(상대)계좌예금주 | checkbox | 타인( |
| check.신분증분실신고 | check.신분증분실신고 | 신분증분실신고(해당기관앞) | checkbox | 예 (신고일 |
| check.명의도용휴대전화개설신고 | check.명의도용휴대전화개설신고 | 명의도용휴대전화개설신고(통신사앞) | checkbox | 아니오 |
| check.휴대전화분실신고 | check.휴대전화분실신고 | 휴대전화분실신고(통신사앞) | checkbox | 예 (신고일 |
| 기타 | 기타 | 기타 | text | 해당 없음 |
| check.피해구제환급신청 | check.피해구제환급신청 | 피해구제환급신청 | checkbox | 신청예정 |
| 수사기관 | 수사기관 | 수사기관 | text |  |
| check.이용자와은행사이에민법제 | check.이용자와은행사이에민법제 | 이용자와은행사이에민법제731조소정의화해(합의)가이미성립된 | checkbox | 이용자와 은행 사이에 민법 제731조 소정의 화해(합의)가 이미 성립된  |
| check.수사기관등의수사를통해전 | check.수사기관등의수사를통해전 | 수사기관등의수사를통해전자금융사고가아닌경우로판명된경우 | checkbox | 수사기관 등의 수사를 통해 전자금융사고가 아닌 경우로 판명된 경우 |
| check.기타비대면금융사고책임 | check.기타비대면금융사고책임 | 기타(비대면금융사고책임분담협약참여은행외금융회사를통한비대면 | checkbox | 기타(비대면 금융사고 책임분담 협약 참여은행 외 금융회사를 통한 비대면  |
| check.사고유형중한가지이상이라도 | check.사고유형중한가지이상이라도 | 사고유형중한가지이상이라도【 | checkbox | ( |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 현예지 |
| sign.signer | sign.customer | 신청인 | signature | 김소윤 |
| check.손님본인 | check.손님본인 | 손님본인 | checkbox | 가족 |
| check.예 | check.예 | 예 | checkbox | 아니오 |
| check.예2 | check.예2 | 예 | checkbox | 아니오 |
| check.신분증SMS문자메시지 | check.신분증SMS문자메시지 | 신분증(SMS문자메시지또는카톡등을통한신분증사본사진,파일 | checkbox | 신분증 (SMS 문자메시지 또는 카톡 등을 통한 신분증 사본 사진, 파일 |
| check.개인정보 | check.개인정보 | 개인정보(이름,휴대전화번호,주민등록번호등) | checkbox | 개인정보(이름, 휴대전화번호, 주민등록번호 등) |
| check.전자적장치 | check.전자적장치 | 전자적장치(휴대전화등,휴대전화를빌려준경우포함) | checkbox | 전자적 장치(휴대전화 등, 휴대전화를 빌려준 경우 포함) |
| check.계좌번호및계좌용비밀번호 | check.계좌번호및계좌용비밀번호 | 계좌번호및계좌용비밀번호 | checkbox | 계좌번호 및 계좌용 비밀번호 |
| check.보안매체제공또는보안매체 | check.보안매체제공또는보안매체 | 보안매체(OTP,보안카드,인증서등)제공또는보안매체용비밀번호 | checkbox | 보안매체(OTP, 보안카드, 인증서 등) 제공 또는 보안매체용 비밀번호  |
| check.기타전자금융관련정보 | check.기타전자금융관련정보 | 기타전자금융관련정보( | checkbox | 기타 전자금융 관련정보( |
| check.예3 | check.예3 | 예 | checkbox | 예 |
| check.보관방식 | check.보관방식 | 보관방식 | checkbox | 예 |
| check.예4 | check.예4 | 예 | checkbox | 아니오 |
| check.경우해당기관앞신분증분실신고를 | check.경우해당기관앞신분증분실신고를 | 경우,해당기관앞신분증분실신고를 | checkbox | 예 |
| check.해당없음 | check.해당없음 | 해당없음 | checkbox | 해당없음 |
| check.사본을휴대전화PC클라우드 | check.사본을휴대전화PC클라우드 | 사본(사진,파일등)을휴대전화,PC,클라우드 | checkbox | 아니오 |
| check.있었습니까 | check.있었습니까 | 있었습니까? | checkbox | 기타( |
| check.계좌용비밀번호를휴대전화PC클라우드 | check.계좌용비밀번호를휴대전화PC클라우드 | 계좌용비밀번호를휴대전화,PC,클라우드 | checkbox | 예 |
| check.있었습니까2 | check.있었습니까2 | 있었습니까? | checkbox | 기타( |
| check.방식이설정되어있었습니까 | check.방식이설정되어있었습니까 | 방식*이설정되어있었습니까? | checkbox | 아니오 |
| check.지문얼굴인식등 | check.지문얼굴인식등 | 지문/얼굴인식등 | checkbox | 기타( |
| 등에저장하여보관하고있었습니까 | 등에저장하여보관하고있었습니까 | 등에저장하여보관하고있었습니까? | text |  |
| 등에저장하고있었습니까 | 등에저장하고있었습니까 | 등에저장(메모)하고있었습니까? | text |  |
| 행번 | 행번 | 행번 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신청인 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신청인 | seal | 현예지 |
| sign.signer2 | sign.signer2 | 신청인 | signature | 박찬연 |
| signer3.name | signer3.name | 직원명 | text | 명혜윤 |
| seal.signer3 | seal.signer3 | 직원명 | seal | 김훈우 |
| sign.signer3 | sign.signer3 | 직원명 | signature | 명혜윤 |
| 전자금융거래사고발생경위및사유 | 전자금융거래사고발생경위및사유 | 전자금융거래사고발생경위및사유 | text | 만기 해지 |
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 신용거래정보2 | 신용거래정보2 | ■신용거래정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer4.name | signer4.name | 본인성명 | text | 박찬연 |
| seal.signer4 | seal.signer4 | 본인성명 | seal | 박찬연 |
| sign.signer4 | sign.signer4 | 본인성명 | signature | 이욱유 |
| signer5.name | signer5.name | 대리인성명 | text | 박영준 |
| seal.signer5 | seal.agent | 대리인성명 | seal | 김서호 |
| sign.signer5 | sign.agent | 대리인성명 | signature | 박영준 |
| 신분증사본 | 신분증사본 | 신분증사본 | text |  |
| seal.signer6 | seal.signer6 | 본인서명사실확인서 | seal | 강순준 |
| sign.signer6 | sign.signer6 | 본인서명사실확인서 | signature | 박찬연 |
| 목록[].출입국사실증명원또는여권사본 | 목록[].출입국사실증명원또는여권사본 | 출입국사실증명원또는여권사본 | text |  |
| 수사기관의결정문내지는처분서 | 수사기관의결정문내지는처분서 | 수사기관의결정문내지는처분서 | text |  |
| 시간이상지연 | 시간이상지연 | 시간이상지연 | text |  |
| 연계여부등포함 | 연계여부등포함 | 연계여부등)포함 | text |  |
| customer.name2 | customer.name2 | 성명 | text | 박찬연 |
| company.name2 | company.name2 | 법인명 | text | (주)유니온무역 |
| customer.phone2 | customer.phone2 | 전화번호 | phone | 010-5907-7253 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.phone | agent.phone | 전화번호 | phone | 010-6515-4769 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 지점명 | 지점명 | 지점명 | text | 범어지점 |
| 행번2 | 행번2 | 행번 | text |  |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| signer7.name | signer7.name | 위임자(본인) | text | 박찬연 |
| seal.signer7 | seal.signer7 | 위임자(본인) | seal | 이욱유 |
| sign.signer7 | sign.signer7 | 위임자(본인) | signature | 박찬연 |
| signer8.name | signer8.name | 성명 | text | 박찬연 |
| seal.signer8 | seal.signer8 | 성명 | seal | 박찬연 |
| sign.signer8 | sign.signer8 | 성명 | signature | 현예지 |

### hf432 · [필수] 개인(신용)정보 제3자 제공 동의서 (하나원큐 공모주 정보제공 제휴서비스용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.432 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 엠엘투자자문 | 엠엘투자자문 | -엠엘투자자문(주) | text |  |
| 회원탈회시까지보유이용 | 회원탈회시까지보유이용 | -회원탈회시까지보유·이용 | text |  |
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 이욱유 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 김서호 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 설기현 |

### hf433 · 추심지급 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.433 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 접수점 | 접수점 | 접수점 | text |  |
| signer.name | signer.name | 본인및서류확인 | text | 강준주 |
| seal.signer | seal.signer | 본인및서류확인 | seal | 김동은 |
| sign.signer | sign.signer | 본인및서류확인 | signature | 강준주 |
| 법원명 | 법원명 | 법원명 | text |  |
| 채권자 | 채권자 | 채권자 | text |  |
| check.최소추심요청금액 | check.최소추심요청금액 | 최소추심요청금액 | checkbox | 만원 |
| 사건번호 | 사건번호 | 사건번호 | text | 707-253625-37457 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.birth | agent.birth | 생년월일 | date | 1962년 12월 19일 |
| agent.phone | agent.phone | 연락처 | phone | 010-6515-4769 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| customer.name | customer.name | 위임인 | text | 박찬연 |
| 은행계좌번호 | 은행계좌번호 | 은행▣계좌번호 | text | 526-254089-32580 |
| 예금주명 | 예금주명 | ▣예금주명 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 본인및서류확인 | 본인및서류확인 | 본인및서류확인 | text |  |

### hf434 · 세종특별자치시 지역개발채권 매입 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.434 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 채권매입금액 | 채권매입금액 | 채권매입금액 | number | 30,460,000 |
| 성명법인명 | 성명법인명 | 성명/법인명 | text | 동방화학 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.name | agent.name | 대리인(성명) | text | 박영준 |
| customer.rrn | customer.rrn | 주민등록번호(사업자등록번호) | rrn | 900210-1****** |
| customer.rrn2 | customer.rrn2 | 주민등록번호 | rrn | 900210-1****** |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 징구기관 | 징구기관 | 징구기관 | text |  |
| customer.phone2 | customer.phone2 | 연락처 | phone | 010-5907-7253 |
| check.즉시매도시 | check.즉시매도시 | 즉시매도시 | checkbox | 보기1 |
| check.만기시하나은행본인계좌로원리금자동상환 | check.만기시하나은행본인계좌로원리금자동상환 | 만기시하나은행본인계좌로원리금자동상환 | checkbox | 하나은행 계좌번호 ( |
| check.만기시증권회사본인계좌로원리금자동상환 | check.만기시증권회사본인계좌로원리금자동상환 | 만기시증권회사본인계좌로원리금자동상환 | checkbox | 하나금융투자 계좌번호 ( |
| check.만기시직접내점하여원리금상환 | check.만기시직접내점하여원리금상환 | 만기시직접내점하여원리금상환 | checkbox | 보기1 |
| check.자동차신규등록 | check.자동차신규등록 | 자동차신규등록(1) | checkbox | 기타허가☞신고(6) |
| 증서번호 | 증서번호 | 증서번호 | text | 라가21663908 |
| 매출일자 | 매출일자 | 매출일자 | date | 2025년 3월 30일 |
| 매출점 | 매출점 | 매출점 | number | 2,990,000 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 수납금액 | 수납금액 | 수납금액 | number | 59,220,000 |
| 소득세 | 소득세 | 소득세 | number | 93,690,000 |
| 법인세 | 법인세 | 법인세 | text |  |
| 지방소득세 | 지방소득세 | 지방소득세 | number | 60,000 |
| 농특세 | 농특세 | 농특세 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 강순준 |
| sign.signer | sign.customer | 신청인 | signature | 현예지 |
| signer2.name | signer2.name | (대리인 | text | 박영준 |
| seal.signer2 | seal.agent | (대리인 | seal | 이도민 |
| sign.signer2 | sign.agent | (대리인 | signature | 강석호 |
| 위탁 | 위탁 | 위탁 | text |  |
| check.개인정보수집및이용내역 | check.개인정보수집및이용내역 | 개인정보수집및이용내역 | checkbox | 개인정보 수집 및 이용 내역 |
| check.동의함 | check.동의함 | 동의함 | checkbox | 동의하지 않음 |
| check.개인정보3자제공내역 | check.개인정보3자제공내역 | 개인정보3자제공내역 | checkbox | 개인정보 3자 제공 내역 |
| check.동의함2 | check.동의함2 | 동의함 | checkbox | 동의하지 않음 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer3.name | signer3.name | 성명 | text | 박찬연 |
| seal.signer3 | seal.signer3 | 성명 | seal | 강순준 |
| sign.signer3 | sign.signer3 | 성명 | signature | 박찬연 |

### hf435 · 대전광역시 지역개발채권 매입 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.435 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 채권매입금액 | 채권매입금액 | 채권매입금액 | number | 6,810,000 |
| 성명법인명 | 성명법인명 | 성명/법인명 | text | (주)유니온무역 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.name | agent.name | 대리인(성명) | text | 박영준 |
| customer.rrn | customer.rrn | 주민등록번호(사업자등록번호) | rrn | 900210-1****** |
| customer.rrn2 | customer.rrn2 | 주민등록번호 | rrn | 900210-1****** |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 징구기관 | 징구기관 | 징구기관 | text |  |
| customer.phone2 | customer.phone2 | 연락처 | phone | 010-5907-7253 |
| check.즉시매도시 | check.즉시매도시 | 즉시매도시 | checkbox | 보기1 |
| check.만기시하나은행본인계좌로원리금자동상환 | check.만기시하나은행본인계좌로원리금자동상환 | 만기시하나은행본인계좌로원리금자동상환 | checkbox | 하나은행 계좌번호 ( |
| check.만기시증권회사본인계좌로원리금자동상환 | check.만기시증권회사본인계좌로원리금자동상환 | 만기시증권회사본인계좌로원리금자동상환 | checkbox | 하나금융투자 계좌번호 ( |
| check.만기시직접내점하여원리금상환 | check.만기시직접내점하여원리금상환 | 만기시직접내점하여원리금상환 | checkbox | 보기1 |
| check.자동차신규등록 | check.자동차신규등록 | 자동차신규등록(1) | checkbox | 각종 계약체결(7) |
| 증서번호 | 증서번호 | 증서번호 | text | 아마13516284 |
| 매출일자 | 매출일자 | 매출일자 | date | 2025년 4월 30일 |
| 매출점 | 매출점 | 매출점 | number | 7,470,000원 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 수납금액 | 수납금액 | 수납금액 | number | 9,340,000 |
| 소득세 | 소득세 | 소득세 | number | 225,560,000 |
| 법인세 | 법인세 | 법인세 | text |  |
| 지방소득세 | 지방소득세 | 지방소득세 | number | 22,940,000 |
| 농특세 | 농특세 | 농특세 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 이욱유 |
| sign.signer | sign.customer | 신청인 | signature | 강순준 |
| signer2.name | signer2.name | (대리인 | text | 박영준 |
| seal.signer2 | seal.agent | (대리인 | seal | 강석호 |
| sign.signer2 | sign.agent | (대리인 | signature | 박영준 |
| 위탁 | 위탁 | 위탁 | text |  |
| check.개인정보수집및이용내역 | check.개인정보수집및이용내역 | 개인정보수집및이용내역 | checkbox | 개인정보 수집 및 이용 내역 |
| check.동의함 | check.동의함 | 동의함 | checkbox | 동의함 |
| check.개인정보3자제공내역 | check.개인정보3자제공내역 | 개인정보3자제공내역 | checkbox | 개인정보 3자 제공 내역 |
| check.동의함2 | check.동의함2 | 동의함 | checkbox | 동의함 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer3.name | signer3.name | 성명 | text | 박찬연 |
| seal.signer3 | seal.signer3 | 성명 | seal | 강순준 |
| sign.signer3 | sign.signer3 | 성명 | signature | 박찬연 |

### hf436 · 주주명부(법인 비대면 실명확인 서비스 용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.436 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].주주명 | 목록[].주주명 | 주주명 | text | 윤혁영 |
| 목록[].생년월일 | 목록[].생년월일 | 생년월일(YYYY-MM-DD) | date | 2025년 7월 1일 |
| 목록[].주식의종류 | 목록[].주식의종류 | 주식의종류(보통주등) | text |  |
| 목록[].지분율 | 목록[].지분율 | 지분율(%) | number | 70 |
| 목록[].주식수 | 목록[].주식수 | 주식수(주) | text |  |
| 목록[].주당액면가액 | 목록[].주당액면가액 | 주당액면가액(원) | text | 6,510,000 |
| 목록[].자본금액 | 목록[].자본금액 | 자본금액(원) | number | 19,100,000 |
| 목록[].국적 | 목록[].국적 | 국적 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |

### hf437 · 고객정보 활용 동의서(매출채권보험_모집대행업무용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.437 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 매출채권보험추천등모집대행업무수행 | 매출채권보험추천등모집대행업무수행 | ▪매출채권보험추천등모집대행업무수행 | number | 5,020,000 |
| 필수사항 | 필수사항 | 필수사항 | text |  |
| 필수사항2 | 필수사항2 | 필수사항 | text |  |
| company.name | corp.name | 업체명 | text | (주)유니온무역 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| signer.name | corp.ceo | 대표자 | text | 박찬연 |
| seal.signer | seal.corp | 대표자 | seal | 강순준 |
| sign.signer | sign.customer | 대표자 | signature | 박찬연 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| signer2.name | signer2.name | 본인확인 | text | 길형성 |
| seal.signer2 | seal.signer2 | 본인확인 | seal | 천예성 |
| sign.signer2 | sign.signer2 | 본인확인 | signature | 김아태 |
| customer.phone2 | customer.phone2 | 연락처(전화번호,핸드폰,E-mail) | phone | 010-5907-7253 |

### hf438 · 매출채권보험 상담 신청서(신청기업용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.438 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업체명 | text | (주)유니온무역 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| company.address | corp.address | 사업장주소 | text | 서울특별시 중구 다산로 361, 6층 |
| 당기매출액 | 당기매출액 | 당기매출액(최근1년매출액) | number | 71,940,000 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 업종업종분류코드 | 업종업종분류코드 | 업종/업종분류코드 | number | 7777 |
| company.established | corp.established | 설립일 | date | 2018.11.01 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| 품목 | 품목 | 품목 | text | 냉동 수산물 |
| 년 | 년 | 년 | number | 12 |
| 년2 | 년2 | 년 | text |  |
| 년3 | 년3 | 년 | text |  |
| 월 | 월 | 월 | text |  |
| 월2 | 월2 | 월 | text |  |
| 일 | 일 | 일 | text |  |
| 일2 | 일2 | 일 | text |  |
| 신청기업담당자 | 신청기업담당자 | 신청기업담당자 | text | 최민하 |
| employer.position | employer.position | 직위 | text | 대리 |
| customer.phone2 | customer.phone2 | 연락처 | phone | 010-5907-7253 |
| company.name2 | company.name2 | 기업체명 | text | (주)유니온무역 |
| company.biz_no2 | company.biz_no2 | 사업자등록번호 | biz_no | 264-82-36559 |
| company.corp_no2 | company.corp_no2 | 법인등록번호 | rrn | 200112-7448551 |
| signer.name | signer.name | 대표자명 | text | 박찬연 |
| seal.signer | seal.corp | 대표자명 | seal | 박찬연 |
| sign.signer | sign.customer | 대표자명 | signature | 현예지 |
| signer2.name | signer2.name | 본인확인 | text | 강원예 |
| seal.signer2 | seal.signer2 | 본인확인 | seal | 구유서 |
| sign.signer2 | sign.signer2 | 본인확인 | signature | 강원예 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 신용보험센터 | 신용보험센터 | 신용보험센터 | text |  |

### hf439 · 상조회사 선수금 예치확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.439 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 상조회사명 | 상조회사명 | 상조회사명 | text | (주)유니온무역 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.biz_no | corp.biz_no | 사업자번호 | biz_no | 264-82-36559 |
| 목록[].예금과목 | 목록[].예금과목 | 예금과목 | text | 하나 적금 |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 143-691509-07570 |
| 목록[].금액 | 목록[].금액 | 금액 | text | 4,990,000 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.signer | seal.signer | 지점장 | seal | 신주하 |
| sign.signer | sign.signer | 지점장 | signature | 백상우 |

### hf440 · 금융사고예방을 위한 문자통지(SMS) 서비스 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.440 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.phone | customer.phone | 핸드폰번호 | phone | 010-5907-7253 |
| signer.name | customer.name | 고객명 | text | 박찬연 |
| seal.signer | seal.customer | 고객명 | seal | 강순준 |
| sign.signer | sign.customer | 고객명 | signature | 박찬연 |
| 요구불예금 | 요구불예금 | 요구불예금(금액제한없음) | text |  |
| 중도해지금액제한없음 | 중도해지금액제한없음 | 중도해지:금액제한없음 | number | 2,280,000 |
| 건당1억원이상 | 건당1억원이상 | 건당1억원이상 | text |  |
| 통장재발급 | 통장재발급 | 통장재발급 | text |  |
| 계좌비밀번호변경 | 계좌비밀번호변경 | 계좌비밀번호변경 | text | 108-773325-89145 |
| 현금IC카드재발급 | 현금IC카드재발급 | 현금IC카드재발급 | text |  |
| 통장MS훼손재기록 | 통장MS훼손재기록 | 통장M/S훼손재기록 | text |  |
| customer.phone2 | customer.phone2 | 휴대폰번호(변경전/후번호로통지) | phone | 010-5907-7253 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이민도 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 한환린 |

### hf441 · 법원보관금 납부서(은행제출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.441 (기타) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 법원명 | 법원명 | 법원명 | text |  |
| 납부금액 | 납부금액 | 납부금액 | number | 31,270,000원 |
| 납부자성명 | 납부자성명 | 납부자성명 | text | 박찬연 |
| 납부자주소 | 납부자주소 | 납부자주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 잔액환급계좌번호 | 잔액환급계좌번호 | 잔액환급계좌번호 | number | 299,750,000 |
| 은행 | 은행 | 은행 | text | 기업은행 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| 사건번호 | 사건번호 | 사건번호 | text | 9574-5311 |
| 보관금종류 | 보관금종류 | 보관금종류 | text |  |
| customer.rrn | customer.rrn | 주민등록번호(사업자등록번호) | rrn | 900210-1659382 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| customer.name | customer.name | 예금주 | text | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 납부당사자 | text | 박찬연 |
| seal.signer | seal.customer | 납부당사자 | seal | 최우빈 |
| sign.signer | sign.customer | 납부당사자 | signature | 강순준 |
| 법원명2 | 법원명2 | 법원명 | text |  |
| 납부금액2 | 납부금액2 | 납부금액 | number | 880,000 |
| 납부자성명2 | 납부자성명2 | 납부자성명 | text | 박도준 |
| 납부자주소2 | 납부자주소2 | 납부자주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 잔액환급계좌번호2 | 잔액환급계좌번호2 | 잔액환급계좌번호 | number | 8,100,000 |
| 은행2 | 은행2 | 은행 | text | 카카오뱅크 |
| account2 | account2 | 계좌번호 | account_no | 000-287736-52424 |
| 사건번호2 | 사건번호2 | 사건번호 | text | 7683-3678 |
| 보관금종류2 | 보관금종류2 | 보관금종류 | text |  |
| customer.rrn2 | customer.rrn2 | 주민등록번호(사업자등록번호) | rrn | 900210-1659382 |
| customer.phone2 | customer.phone2 | 전화번호 | phone | 010-5907-7253 |
| customer.name2 | customer.name2 | 예금주 | text | 박찬연 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 법원명3 | 법원명3 | 법원명 | text |  |
| 납부금액3 | 납부금액3 | 납부금액 | number | 640,000 |
| 납부자성명3 | 납부자성명3 | 납부자성명 | text | 박찬연 |
| 납부자주소3 | 납부자주소3 | 납부자주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 잔액환급계좌번호3 | 잔액환급계좌번호3 | 잔액환급계좌번호 | number | 4,230,000 |
| 은행3 | 은행3 | 은행 | text | 기업은행 |
| account3 | account3 | 계좌번호 | account_no | 000-287736-52424 |
| 사건번호3 | 사건번호3 | 사건번호 | text | 678-403775-06876 |
| 보관금종류3 | 보관금종류3 | 보관금종류 | text |  |
| customer.rrn3 | customer.rrn3 | 주민등록번호(사업자등록번호) | rrn | 900210-1659382 |
| customer.phone3 | customer.phone3 | 전화번호 | phone | 010-5907-7253 |
| customer.name3 | customer.name3 | 예금주 | text | 박찬연 |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |

### hf047 · 대출상담 및 신청서(한국주택금융공사채권유동화목적 보금자리론용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.47 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신청금액 | 신청금액 | 신청금액 | number | 710,000 |
| check.자금용도 | check.자금용도 | 자금용도 | checkbox | 구입 |
| check.주택보유수 | check.주택보유수 | 주택보유수(본건담보주택제외) | checkbox | 주택(처분 예정) |
| check.담보제공자 | check.담보제공자 | 담보제공자 | checkbox | 본인 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.rrn | customer.rrn | 주민번호앞6자리 | number | 900210 |
| check.결혼여부 | check.결혼여부 | 결혼여부 | checkbox | 기혼 |
| employer.name | employer.name | 직장명 | text | 주식회사 태평양무역 |
| 부서직위 | 부서직위 | 부서/직위 | text |  |
| check.직업구분 | check.직업구분 | 직업구분 | checkbox | 기타( |
| 근무기간 | 근무기간 | 근무기간(업력) | number | 6 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| 소득 | 소득 | 소득(합계) | number | 81,390,000 |
| 부채 | 부채 | 부채(합계) | number | 6,180,000 |
| 금융기관 | 금융기관 | 금융기관 | text | 하나은행 |
| 금융기관2 | 금융기관2 | 금융기관 | text | 국민은행 |
| customer.name2 | customer.name2 | 성명 | text | 박찬연 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.rrn2 | customer.rrn2 | 주민번호앞6자리 | number | 900210 |
| employer.name2 | employer.name2 | 직장명 | text | 주식회사 태평양무역 |
| 부서직위2 | 부서직위2 | 부서/직위 | text |  |
| check.직업구분2 | check.직업구분2 | 직업구분 | checkbox | 사업소득자 |
| 근무기간2 | 근무기간2 | 근무기간(업력) | number | 36 |
| customer.phone2 | customer.phone2 | 전화번호 | phone | 010-5907-7253 |
| 소득2 | 소득2 | 소득(합계) | number | 530,000 |
| 부채2 | 부채2 | 부채(합계) | number | 2,350,000원 |
| 금융기관3 | 금융기관3 | 금융기관 | text | 국민은행 |
| 금융기관4 | 금융기관4 | 금융기관 | text | 농협은행 |
| check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까 | check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까 | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 안내 받음 (구두, 우편, 이메일, 팩스, 직접 수령) |
| check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2 | check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2 | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 원하지 않음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인(본인) | text | 박찬연 |
| seal.signer | seal.customer | 신청인(본인) | seal | 박찬연 |
| sign.signer | sign.customer | 신청인(본인) | signature | 현예지 |
| signer2.name | signer2.name | 상담자확인 | text | 김숙원 |
| seal.signer2 | seal.signer2 | 상담자확인 | seal | 성석예 |
| sign.signer2 | sign.signer2 | 상담자확인 | signature | 김숙원 |
| 계약기간 | 계약기간 | 계약기간 | text |  |
| 자택 | 자택 | 자택 | text |  |
| customer.phone3 | customer.phone3 | 핸드폰 | phone | 010-5907-7253 |
| 대출금액 | 대출금액 | 대출금액 | number | 9.56 |
| 대출금액2 | 대출금액2 | 대출금액 | number | 23.5 |
| 자택2 | 자택2 | 자택 | text |  |
| customer.phone4 | customer.phone4 | 핸드폰 | phone | 010-5907-7253 |
| 대출금액3 | 대출금액3 | 대출금액 | number | 43.6 |
| 대출금액4 | 대출금액4 | 대출금액 | number | 88.55 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 정옥우 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 검인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김경희 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 손도태 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 고영희 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 이용윤 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 검인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 확인 |
| customer.name3 | customer.name3 | 성명 | text | 박찬연 |
| customer.address3 | customer.address3 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| employer.name3 | employer.name3 | 직장명 | text | 주식회사 태평양무역 |
| check.상담희망전화 | check.상담희망전화 | 상담희망전화 | checkbox | 직장 또는 자택 |
| customer.phone5 | customer.phone5 | 전화번호 | phone | 010-5907-7253 |
| check.주택보유수2 | check.주택보유수2 | 주택보유수(본건담보주택제외) | checkbox | 주택(처분 예정) |
| 대출신청금액 | 대출신청금액 | 대출신청금액 | number | 5,100,000 |
| check.대출만기 | check.대출만기 | 대출만기 | checkbox | 년 / |
| 희망취급기관 | 희망취급기관 | 희망취급기관 | text |  |
| 대출희망일 | 대출희망일 | 대출희망일 | date | 2025.09.25 |
| 거치기간 | 거치기간 | 거치기간 | text |  |
| 소유권이전등기일 | 소유권이전등기일 | 소유권이전등기일 | date | 2026-07-29 |
| 담보주택소재지 | 담보주택소재지 | 담보주택소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.주택유형 | check.주택유형 | 주택유형 | checkbox | 아파트 |
| check.소유자 | check.소유자 | 소유(예정)자 | checkbox | 배우자 |
| check.담보제공자2 | check.담보제공자2 | 담보제공자 | checkbox | 부부공동 (담보제공자 성함 |
| check.본건설정순위 | check.본건설정순위 | 본건설정순위 | checkbox | 순위 |
| 임대계약건수 | 임대계약건수 | 임대계약건수 | number | 1 |
| 임대보증금합계액 | 임대보증금합계액 | 임대보증금합계액 | number | 9,610,000원 |
| check.전용면적 | check.전용면적 | 전용면적 | checkbox | m2이하 |
| check.규제지역해당 | check.규제지역해당 | 규제지역해당 | checkbox | 아니오 |
| check.소득증명 | check.소득증명 | 소득증명 | checkbox | 본인ᆞ배우자 합산 |
| 본인부채 | 본인부채 | 본인부채 | text |  |
| 제외부채 | 제외부채 | 제외부채 | text |  |
| 02p | 02p | 0.2%p | text |  |
| customer.rrn3 | customer.rrn3 | 주민번호앞6자리 | number | 900210 |
| check.결혼여부2 | check.결혼여부2 | 결혼여부 | checkbox | 결혼예정(3개월이내) |
| check.배우자세대분리 | check.배우자세대분리 | 배우자세대분리 | checkbox | 아니오 |
| spouse.name | spouse.name | 배우자성명 | text | 이도민 |
| 배우자주민번호앞6자리 | 배우자주민번호앞6자리 | 배우자주민번호앞6자리 | text | 6072-0437 |
| check.상환방식 | check.상환방식 | 상환방식 | checkbox | 원리금균등 |
| 희망취급지점 | 희망취급지점 | 희망취급지점 | text | 범어지점 |
| 변동금리기간 | 변동금리기간 | 변동금리기간 | number | 7.42 |
| check.자금용도2 | check.자금용도2 | 자금용도 | checkbox | 상환 |
| check.최저층여부 | check.최저층여부 | 최저층여부 | checkbox | 아니오 |
| check.선순위종류 | check.선순위종류 | 선순위종류 | checkbox | 주택도시기금 |
| 선순위설정금액 | 선순위설정금액 | 선순위설정금액 | number | 20,590,000 |
| 총방수 | 총방수 | 총방수 | text |  |
| 임대방수 | 임대방수 | 임대방수 | number | 3 |
| check.건물등기부등본 | check.건물등기부등본 | 건물등기부등본 | checkbox | 있음 |
| check.녹색건축물여부 | check.녹색건축물여부 | 녹색건축물여부 | checkbox | 아니오 |
| 배우자부채 | 배우자부채 | 배우자부채 | text |  |
| 제외대출 | 제외대출 | 제외대출 | text |  |
| 종류 | 종류 | 종류 | text | 하나 TDF 2040 |
| employer.name4 | employer.name4 | 소속 | text | 주식회사 태평양무역 |
| 발급기관 | 발급기관 | 발급기관 | text |  |
| 발급일자 | 발급일자 | 발급일자 | date | 2025-11-29 |
| customer.name4 | customer.name4 | 성명 | text | 박찬연 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer3.name | signer3.name | 신청인(본인) | text | 박찬연 |
| seal.signer3 | seal.signer3 | 신청인(본인) | seal | 현예지 |
| sign.signer3 | sign.signer3 | 신청인(본인) | signature | 박찬연 |
| 협회코드 | 협회코드 | 협회코드(대출상담사) | number | 90680 |

### hf048 · 가계형소호 여신차입신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.48 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 대환(재약정) |
| check.신청인구분 | check.신청인구분 | 신청인구분 | checkbox | 공동사업자 |
| check.여신신청인의 | check.여신신청인의 | 여신신청인()의 | checkbox | 공동사업자 |
| 고객번호 | 고객번호 | 고객번호 | text | 296-021235-19158 |
| check.우편물수령처 | check.우편물수령처 | 우편물수령처 | checkbox | 사업장 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.address | customer.address | 자택주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.address | corp.address | 사업장주소 | text | 서울특별시 중구 다산로 361, 6층 |
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| check.직업군 | check.직업군 | 직업군 | checkbox | 기타( |
| company.name | corp.name | 업체명(상호) | text | (주)유니온무역 |
| check.매출정보 | check.매출정보 | 매출(소득)정보 | checkbox | 세무서신고 |
| check.사업장소유여부 | check.사업장소유여부 | 사업장소유여부 | checkbox | 예 |
| 월임차료 | 월임차료 | 월임차료 | number | 9,750,000 |
| check.자가 | check.자가 | 자가( | checkbox | 본인 |
| check.주거형태코드 | check.주거형태코드 | 주거형태코드 | checkbox | 기타( |
| check.부채현황취급예정포함 | check.부채현황취급예정포함 | 부채현황(단위:백만원)【취급예정포함】 | checkbox | 담보( |
| 종류 | 종류 | 종류 | text | 하나 정기예금 |
| 평가금액 | 평가금액 | 평가금액 | number | 262,350,000 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 월관리비 | 월관리비 | 월관리비 | number | 133,780,000 |
| 면적 | 면적 | 면적 | text |  |
| customer.birth | customer.birth | 생년월일 | date | 1990-02-10 |
| customer.home_phone | customer.home_phone | 자택전화번호 | phone | 02-8556-8366 |
| 사업장전화번호 | 사업장전화번호 | 사업장전화번호 | phone | 010-5907-7253 |
| check.국적 | check.국적 | 국적 | checkbox | 기타 ( |
| company.biz_item | corp.biz_item | 업종(주요제품) | text | 무역 |
| 연매출 | 연매출 | 연매출(연소득) | number | 1,800,000 |
| 임차보증금 | 임차보증금 | 임차보증금 | number | 110,000 |
| company.address2 | company.address2 | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| check.공동대표여부 | check.공동대표여부 | 공동대표여부 | checkbox | 아니오 |
| 종업원수 | 종업원수 | 종업원수 | number | 36 |
| check.담보종류 | check.담보종류 | 담보종류 | checkbox | 기타( |
| check.임대차확인 | check.임대차확인 | 임대차확인 | checkbox | 없음 |
| 소유자명 | 소유자명 | 소유자명 | text |  |
| 신청금액 | 신청금액 | 신청금액 | number | 7,270,000 |
| check.상환방법 | check.상환방법 | 상환방법 | checkbox | 원금균등분할 |
| check.자금용도 | check.자금용도 | 자금용도 | checkbox | 시설자금 |
| date | date | 대출희망일 | date | 2026년 1월 31일 |
| 대출과목 | 대출과목 | 대출과목 | text | 시설자금대출 |
| check.거래구분 | check.거래구분 | 거래구분 | checkbox | 건별 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 여신신청인(본인) | text | 박찬연 |
| seal.signer | seal.customer | 여신신청인(본인) | seal | 현예지 |
| sign.signer | sign.customer | 여신신청인(본인) | signature | 박찬연 |
| signer2.name | related.name | 담보제공자(또는연대보증인또는공동사업자) | text | 반아지 |
| seal.signer2 | seal.related | 담보제공자(또는연대보증인또는공동사업자) | seal | 황보현도 |
| sign.signer2 | sign.related | 담보제공자(또는연대보증인또는공동사업자) | signature | 반아지 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 윤경도 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 길예호 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 민승찬 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 확인 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 박숙연 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 이석우 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 검인 |
| check.신규증액처리시안내 | check.신규증액처리시안내 | 신규,증액처리시안내 | checkbox | 이메일 |
| check.동의함 | check.동의함 | 동의함( | checkbox | 문자 |
| check.중도상환해약금면제시점도래안내문자통지 | check.중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | checkbox | 원치않음 |
| check.우편 | check.우편 | 우편 | checkbox | 원치않음 |
| check.문자 | check.문자 | 문자 | checkbox | 원치않음 |
| check.이메일 | check.이메일 | 이메일 | checkbox | 원치않음 |
| 대출금입금계좌 | 대출금입금계좌 | 대출금입금(실행)계좌 | text | 426-088252-72419 |
| check.예금담보등상계후잔액반환계좌번호 | check.예금담보등상계후잔액반환계좌번호 | 예금담보등상계후잔액반환계좌번호(담보제공자기준) | checkbox | 별도 지정(은행명 |
| 원금및이자자동이체결제계좌 | 원금및이자자동이체결제계좌 | 원(리)금및이자자동이체결제계좌 | number | 6,070,000 |
| seal.signer3 | seal.signer3 | 신청인:____________________________ | seal | 강순준 |
| sign.signer3 | sign.signer3 | 신청인:____________________________ | signature | 현예지 |
| 설정순위 | 설정순위 | •설정순위(설정일자) | text |  |
| signer4.name | signer4.name | •접수번호(등기부등본을구기준) | text | 강우민 |
| seal.signer4 | seal.signer4 | •접수번호(등기부등본을구기준) | seal | 강우민 |
| sign.signer4 | sign.signer4 | •접수번호(등기부등본을구기준) | signature | 허영서 |
| 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | text |  |
| 채권최고액 | 채권최고액 | •채권최고액 | number | 7,220,000 |

### hf049 · 《개인》대출신청서(가계용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.49 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 채무인수 |
| check.신청인구분 | check.신청인구분 | 신청인구분 | checkbox | 연대보증인 |
| check.대출신청인의 | check.대출신청인의 | 대출신청인()의 | checkbox | 친인척 |
| 고객번호 | 고객번호 | 고객번호 | text | 423-550840-84091 |
| check.우편물수령처 | check.우편물수령처 | 우편물수령처 | checkbox | 직장 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.address | customer.address | 자택주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| employer.address | employer.address | 직장주소 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태평양무역 구매팀 |
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| check.직업군 | check.직업군 | 직업군 | checkbox | 급여소득자 |
| employer.name | employer.name | 직장명 | text | 주식회사 태평양무역 |
| 근무부서 | 근무부서 | 근무부서 | text |  |
| 입사년월 | 입사년월 | 입사년월 | text |  |
| check.자가 | check.자가 | 자가( | checkbox | 가족 |
| check.주거형태코드 | check.주거형태코드 | 주거형태코드 | checkbox | 기타( |
| check.부채현황취급예정포함 | check.부채현황취급예정포함 | 부채현황(단위:백만원)【취급예정포함】 | checkbox | 미상환 |
| 종류 | 종류 | 종류 | text | 하나 적금 |
| 평가금액 | 평가금액 | 평가금액 | number | 31,040,000 |
| check.고용형태 | check.고용형태 | 고용형태 | checkbox | 정규직 |
| employer.position | employer.position | 직위 | text | 대리 |
| check.직무구분 | check.직무구분 | 직무구분 | checkbox | 자영업자 |
| 면적 | 면적 | 면적 | text |  |
| company.address | corp.address | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| check.연소득 | check.연소득 | 연소득 | checkbox | 배우자( |
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| customer.home_phone | customer.home_phone | 자택전화번호 | phone | 02-5426-0645 |
| employer.phone | employer.phone | 직장전화번호 | phone | 043-783-2775 |
| check.국적 | check.국적 | 국적 | checkbox | 기타( |
| check.담보종류 | check.담보종류 | 담보종류 | checkbox | 상가 |
| check.임대차확인 | check.임대차확인 | 임대차확인 | checkbox | 없 |
| 소유자명 | 소유자명 | 소유자명 | text |  |
| check.결혼여부 | check.결혼여부 | 결혼여부 | checkbox | 기혼 |
| date | date | 대출희망일 | date | 2026년 1월 31일 |
| check.상환방법 | check.상환방법 | 상환방법 | checkbox | 원리금균등분할 |
| check.주택 | check.주택 | 주택( | checkbox | 구입 |
| check.기타부동산 | check.기타부동산 | 기타부동산( | checkbox | 임차 |
| check.거래구분 | check.거래구분 | 거래구분 | checkbox | 한도 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 대출신청인(본인) | text | 박찬연 |
| seal.signer | seal.customer | 대출신청인(본인) | seal | 박찬연 |
| sign.signer | sign.customer | 대출신청인(본인) | signature | 현예지 |
| signer2.name | related.name | 담보제공자(또는연대보증인) | text | 현혜윤 |
| seal.signer2 | seal.related | 담보제공자(또는연대보증인) | seal | 현혜윤 |
| sign.signer2 | sign.related | 담보제공자(또는연대보증인) | signature | 장수린 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김정주 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 정미서 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 석준아 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 정수원 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 확인 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 류주아 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 확인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 박은영 |
| check.신규증액채무인수한도감액한도완제처리시안내 | check.신규증액채무인수한도감액한도완제처리시안내 | 신규,증액,채무인수,한도감액,한도완제처리시안내 | checkbox | 원치않음 |
| check.신청대출승인완료시안내문자통지 | check.신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | checkbox | 동의함 |
| check.동의함 | check.동의함 | 동의함( | checkbox | 문자 |
| check.중도상환해약금면제시점도래안내문자통지 | check.중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | checkbox | 동의함 |
| check.우편 | check.우편 | 우편 | checkbox | 직장 |
| check.문자 | check.문자 | 문자 | checkbox | 원치않음 |
| check.이메일 | check.이메일 | 이메일 | checkbox | 동의함 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| customer.name2 | customer.name2 | 예금주 | text | 박찬연 |
| check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까 | check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까 | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 원치않음 |
| check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2 | check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2 | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 직접 수령 |
| 이관희망점 | 이관희망점 | 이관희망점 | text |  |
| 설정순위 | 설정순위 | •설정순위(설정일자) | text |  |
| 접수번호 | 접수번호 | •접수번호(등기부등본을구기준) | text | 245-067416-39200 |
| signer3.name | signer3.name | 담보제공 | text | 김윤주 |
| seal.signer3 | seal.signer3 | 담보제공 | seal | 김윤주 |
| sign.signer3 | sign.signer3 | 담보제공 | signature | 현혜윤 |
| customer.name3 | customer.name3 | 성명 | text | 박찬연 |
| 신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | text |  |
| 대출부수거래충족여부안내통지 | 대출부수거래충족여부안내통지 | 대출부수거래충족여부안내통지(문자만) | text |  |
| 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | text |  |
| 거절사유에대해안내를받으시겠습니까 | 거절사유에대해안내를받으시겠습니까 | 거절사유에대해안내를받으시겠습니까? | text | 생활자금 |

### hf050 · [필수]개인(신용)정보 제3자 제공 동의서(토지분양대금 대출 약정_대구도시개발공사)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.50 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 대구도시개발공사 | 대구도시개발공사 | -대구도시개발공사 | text |  |
| 제공일로부터5년까지보유이용 | 제공일로부터5년까지보유이용 | -제공일로부터5년까지보유·이용 | text |  |
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 강석호 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 강석호 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 위우호 |

### hf051 · 대출계약 철회신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.51 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 차주 | text | 박찬연 |
| 상품명 | 상품명 | 상품명 | text | 하나 정기예금 |
| 실행일 | 실행일 | 실행일 | date | 2025.01.20 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| 금액 | 금액 | 금액 | number | 340,000 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 강순준 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| check.중도상환이나철회하지않고 | check.중도상환이나철회하지않고 | 중도상환이나철회하지않고대출유지함 | checkbox | 중도상환이나 철회하지 않고 대출 유지함 |
| check.기타 | check.기타 | 기타( | checkbox | 기타 ( |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신청인 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신청인 | seal | 강순준 |
| sign.signer2 | sign.signer2 | 신청인 | signature | 현예지 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 노선인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 박미성 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김유정 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 이우윤 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이건재 |

### hf052 · [필수] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택전월세자금대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.52 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 목록[].공공정보등 | 목록[].공공정보등 | ■공공정보등 | text |  |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| 부채금액 | 부채금액 | ¶부채금액 | number | 260,310,000 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인정보제공에동의하십니까2 | check.위개인정보제공에동의하십니까2 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| 보유현황공공임대주택계약정보 | 보유현황공공임대주택계약정보 | 보유현황,공공임대주택계약정보 | text |  |
| 업권등의공시가액 | 업권등의공시가액 | 업권등의공시가액 | number | 31,180,000 |
| 제공받는자와동일 | 제공받는자와동일 | -제공받는자와동일 | text |  |
| check.위고유식별정보조회에동의하십니까 | check.위고유식별정보조회에동의하십니까 | 위고유식별정보조회에동의하십니까? | checkbox | 동의함 |
| 정보전월세거래정보 | 정보전월세거래정보 | 정보,전·월세거래정보 | text |  |
| check.위개인정보조회에동의하십니까 | check.위개인정보조회에동의하십니까 | 위개인(신용)정보조회에동의하십니까? | checkbox | 동의함 |
| check.위개인정보조회에동의하십니까2 | check.위개인정보조회에동의하십니까2 | 위개인(신용)정보조회에동의하십니까? | checkbox | 동의함 |
| check.이용동의여부 | check.이용동의여부 | 이용동의여부 | checkbox | 보기1 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 이욱유 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| signer2.name | family.name | 배우자성명 | text | 김순우 |
| seal.signer2 | seal.signer2 | 배우자성명 | seal | 김수연 |
| sign.signer2 | sign.signer2 | 배우자성명 | signature | 김순우 |

### hf053 · [필수] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택구입자금대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.53 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 재지및면적유형가격임대차현황등 | 재지및면적유형가격임대차현황등 | 재지및면적,유형,가격,임대차현황등 | text |  |
| 목록[].공공정보등 | 목록[].공공정보등 | ■공공정보등 | text |  |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| 부채금액 | 부채금액 | ¶부채금액 | number | 820,000원 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인정보제공에동의하십니까2 | check.위개인정보제공에동의하십니까2 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| 보유현황공공주택계약정보 | 보유현황공공주택계약정보 | 보유현황,공공주택계약(입주)정보 | text |  |
| 권등의공시가액 | 권등의공시가액 | 권등의공시가액 | number | 1,820,000 |
| 제공받는자와동일 | 제공받는자와동일 | -제공받는자와동일 | text |  |
| check.위고유식별정보조회에동의하십니까 | check.위고유식별정보조회에동의하십니까 | 위고유식별정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보조회에동의하십니까 | check.위개인정보조회에동의하십니까 | 위개인(신용)정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보조회에동의하십니까2 | check.위개인정보조회에동의하십니까2 | 위개인(신용)정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| check.이용동의여부 | check.이용동의여부 | 이용동의여부 | checkbox | 동의함 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 강순준 |
| signer2.name | family.name | 배우자성명 | text | 이도민 |
| seal.signer2 | seal.signer2 | 배우자성명 | seal | 장민인 |
| sign.signer2 | sign.signer2 | 배우자성명 | signature | 김서호 |

### hf054 · 주택도시기금 대출 신청서(가계용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.54 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 주택가격 | 주택가격 | 주택가격 | text |  |
| 순담보가액 | 순담보가액 | 순담보가액 | number | 174,580,000 |
| 선순위설정액 | 선순위설정액 | 선순위설정액 | text |  |
| 대출가능액 | 대출가능액 | 대출가능액 | text |  |
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 대환(재약정) |
| check.신청인구분 | check.신청인구분 | 신청인구분 | checkbox | 연대보증인 |
| check.대출신청인의 | check.대출신청인의 | 대출신청인()의 | checkbox | 기타 ( |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.address | customer.address | 주민등록지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.address2 | customer.address2 | 현거주지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 전세보증금 | 전세보증금 | 전세보증금 | number | 8.44 |
| 이사예정지 | 이사예정지 | 이사예정지 | text |  |
| 전세보증금2 | 전세보증금2 | 전세보증금 | number | 7.17 |
| employer.name | employer.name | 직장명 | text | 주식회사 태평양무역 |
| employer.address | employer.address | 직장주소 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태평양무역 구매팀 |
| 배우자명 | 배우자명 | 배우자명 | text |  |
| 다자녀가구다문화가구장애인가구 | 다자녀가구다문화가구장애인가구 | ▢다자녀가구▢다문화가구▢장애인가구 | text |  |
| 원리금자동이체계좌번호 | 원리금자동이체계좌번호 | 원리금자동이체계좌번호 | text | 313-369816-15825 |
| 대출신청금액 | 대출신청금액 | 대출신청금액 | number | 16,410,000 |
| 대출과목 | 대출과목 | 대출과목 | text | 가계일반자금대출 |
| 대출기간 | 대출기간 | 대출기간 | text |  |
| 대출이율 | 대출이율 | 대출이율 | number | 4.49 |
| 목록[].임차보증금 | 목록[].임차보증금 | 임차보증금 | number | 40,190,000원 |
| 본인 | 본인 | 본인 | number | 6.17 |
| 자기자금 | 자기자금 | 자기자금 | number | 3.9 |
| 방수 | 방수 | 방수 | number | 3 |
| 목록[].소액보증금 | 목록[].소액보증금 | 소액보증금 | number | 7,210,000 |
| customer.birth | customer.birth | 생년월일 | date | 900210 |
| employer.department | employer.department | 부서명 | text | 구매팀 |
| 월세보증금 | 월세보증금 | 월세보증금 | number | 200.52 |
| 월세보증금2 | 월세보증금2 | 월세보증금 | number | 31.88 |
| 만기일시원리금균등분할원금균등분할 | 만기일시원리금균등분할원금균등분할 | ▢만기일시▢원리금균등분할▢원금균등분할 | date | 2026-06-15 |
| 소액보증금 | 소액보증금 | 소액보증금 | number | 7,230,000 |
| 배우자 | 배우자 | 배우자 | number | 21.71 |
| 본건대출 | 본건대출 | 본건대출(기금) | number | 130.27 |
| 배우자직장번호 | 배우자직장번호 | 배우자직장번호(핸드폰번호) | text | 808-618126-47914 |
| 대출희망일 | 대출희망일 | 대출희망일 | date | 2026.01.22 |
| 목록[].금액 | 목록[].금액 | 금액 | number | 2,810,000 |
| customer.phone | customer.phone | 휴대폰번호 | phone | 010-5907-7253 |
| customer.email | customer.email | e-mail | text | chanyeon363@naver.com |
| customer.phone2 | customer.phone2 | 전화번호 | phone | 010-5907-7253 |
| employer.position | employer.position | 직위 | text | 대리 |
| 목록[].자금용도 | 목록[].자금용도 | 자금용도 | text | 생활자금 |
| 고객번호 | 고객번호 | 고객번호 | text | 7457-2721 |
| check.우편물수령처 | check.우편물수령처 | 우편물수령처 | checkbox | 자택 |
| 월임대료 | 월임대료 | 월임대료 | number | 675 |
| 주거방수 | 주거방수 | 주거방수 | number | 2 |
| 월임대료2 | 월임대료2 | 월임대료 | number | 4,256 |
| employer.phone | employer.phone | 직장전화번호 | phone | 043-783-2775 |
| 가구총소득 | 가구총소득 | 가구총소득 | number | 253.85 |
| 기타조달 | 기타조달 | 기타조달 | number | 290.1 |
| 결혼일 | 결혼일 | 결혼(예정)일 | date | 2025년 8월 12일 |
| employer.hire_date | employer.hire_date | 입사일자 | date | 2020.05.08 |
| 목록[].담보종류 | 목록[].담보종류 | 담보종류 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 분양가격 | 분양가격 | ▢분양가격 | text |  |
| customer.name2 | customer.name2 | 신청인(본인) | text | 박찬연 |
| customer.name3 | customer.name3 | 차주 | text | 박찬연 |
| 의담보제공자 | 의담보제공자 | 의담보제공자(또는연대보증인) | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 권철경 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김건윤 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이주호 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 검인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 기성율 |
| 신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | text |  |
| check.신규증액채무인수한도감액한도완제처리시안내 | check.신규증액채무인수한도감액한도완제처리시안내 | 신규,증액,채무인수,한도감액,한도완제처리시안내 | checkbox | 원치않음 |
| check.신청대출승인완료시안내문자통지 | check.신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | checkbox | 동의함 |
| check.동의함 | check.동의함 | 동의함( | checkbox | 원치않음 |
| check.중도상환해약금면제시점도래안내문자통지 | check.중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | checkbox | 원치않음 |
| check.우편 | check.우편 | 우편 | checkbox | 원치않음 |
| check.문자 | check.문자 | 문자 | checkbox | 동의함 |
| check.이메일 | check.이메일 | 이메일 | checkbox | 원치않음 |
| 대출금입금계좌 | 대출금입금계좌 | 대출금입금(실행)계좌 | text | 238-494411-44946 |
| check.예금담보등상계후잔액반환계좌번호 | check.예금담보등상계후잔액반환계좌번호 | 예금담보등상계후잔액반환계좌번호(담보제공자기준) | checkbox | 자동이체 결제 계좌 |
| check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까 | check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까 | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 원치않음 |
| check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2 | check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2 | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 구두 |
| 설정순위 | 설정순위 | •설정순위(설정일자) | text |  |
| 접수번호 | 접수번호 | •접수번호(등기부등본을구기준) | text | 2312-1376 |
| signer.name | signer.name | (담보제공자기준) | text | 박찬연 |
| seal.signer | seal.customer | (담보제공자기준) | seal | 박찬연 |
| sign.signer | sign.customer | (담보제공자기준) | signature | 강순준 |
| 대출부수거래충족여부안내통지 | 대출부수거래충족여부안내통지 | 대출부수거래충족여부안내통지(문자만) | text |  |
| 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | text |  |
| 대출신청이거절되는경우 | 대출신청이거절되는경우 | 대출신청이거절되는경우, | text |  |
| 거절사유에대해안내를받으시겠습니까 | 거절사유에대해안내를받으시겠습니까 | 거절사유에대해안내를받으시겠습니까? | text | 주택구입 |
| 채권최고액 | 채권최고액 | •채권최고액 | text |  |

### hf055 · 주택도시기금 대출상담 및 신청서(내집마련 디딤돌 대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.55 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.근저당권과관련된모든대출 | check.근저당권과관련된모든대출 | 근저당권과관련된모든대출금을상환하고말소를원하는경우영업점에방 | checkbox | 근저당권과 관련된 모든 대출금을 상환하고 말소를 원하는 경우 영업점에 방 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.address | customer.address | 주민등록지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.address2 | customer.address2 | 현거주지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.주택유형 | check.주택유형 | 주택유형 | checkbox | 단독주택(다가구 포함) |
| 전세보증금 | 전세보증금 | 전세보증금 | number | 0.95 |
| customer.address3 | customer.address3 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.소유자 | check.소유자 | 소유자 | checkbox | 본인 |
| check.주택유형2 | check.주택유형2 | 주택유형 | checkbox | 연립주택 |
| 임대방수 | 임대방수 | 임대방수 | number | 4 |
| employer.name | employer.name | 직장명 | text | 주식회사 태평양무역 |
| check.직업 | check.직업 | 직업 | checkbox | 자영업 |
| employer.address | employer.address | 직장주소 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태평양무역 구매팀 |
| spouse.name | spouse.name | 배우자성명 | text | 이도민 |
| check.우편물배달장소 | check.우편물배달장소 | 우편물배달장소 | checkbox | 자택 |
| 원리금자동이체계좌번호 | 원리금자동이체계좌번호 | 원리금자동이체계좌번호 | text | 030-927629-39327 |
| 대출신청금액 | 대출신청금액 | 대출신청금액 | number | 26,910,000 |
| 대출과목 | 대출과목 | 대출과목 | text | 가계일반자금대출 |
| check.대출기간 | check.대출기간 | 대출기간 | checkbox | 년 |
| check.거치기간 | check.거치기간 | 거치기간 | checkbox | 년 |
| check.상환방법 | check.상환방법 | 상환방법 | checkbox | 체증식분할상환 |
| check.대출금리 | check.대출금리 | 대출금리 | checkbox | 년 단위 변동금리 연 |
| check.우대금리 | check.우대금리 | 우대금리 | checkbox | 없음 |
| check.대출가부 | check.대출가부 | 대출가부 | checkbox | 가 |
| 본인 | 본인 | 본인 | number | 4.32 |
| 본인2 | 본인2 | 본인 | number | 125.65 |
| 자기자금 | 자기자금 | 자기자금 | number | 9.76 |
| check.배우자 | check.배우자 | 배우자 | checkbox | 무 |
| 방수 | 방수 | 방수 | number | 1 |
| 월세보증금 | 월세보증금 | 월세보증금 | number | 7.61 |
| 방수2 | 방수2 | 방수 | number | 1 |
| 임대보증금 | 임대보증금 | 임대보증금 | number | 42.59 |
| employer.department | employer.department | 부서명 | text | 구매팀 |
| 목록[].차입기관명 | 목록[].차입기관명 | 차입기관명 | text | 카카오뱅크 |
| 배우자 | 배우자 | 배우자 | number | 8.24 |
| 배우자2 | 배우자2 | 배우자 | number | 9.23 |
| 본건대출 | 본건대출 | 본건대출 | number | 7.5 |
| 목록[].금액 | 목록[].금액 | 금액 | number | 58,530,000 |
| customer.rrn | customer.rrn | 주민등록번호앞6자리 | number | 900210 |
| customer.phone | customer.phone | 휴대폰번호 | phone | 010-5907-7253 |
| customer.phone2 | customer.phone2 | 전화번호 | phone | 010-5907-7253 |
| check.주거형태 | check.주거형태 | 주거형태 | checkbox | 기타 |
| 월임대료 | 월임대료 | 월임대료 | number | 43 |
| check.주택보유수 | check.주택보유수 | 주택보유수 | checkbox | 본건 담보주택을 제외하고는 없음 |
| 선순위설정금액 | 선순위설정금액 | 선순위설정금액 | number | 0.45 |
| check.무상거주 | check.무상거주 | 무상거주 | checkbox | 무 |
| employer.position | employer.position | 직위 | text | 대리 |
| spouse.rrn | spouse.rrn | 배우자주민등록번호앞6자리 | number | 670921 |
| 대출희망일 | 대출희망일 | 대출희망일 | date | 2025년 5월 26일 |
| check.본대출과관련된비용및수수료를무통장무인감으로인출함에동의 | check.본대출과관련된비용및수수료를무통장무인감으로인출함에동의 | 본대출과관련된비용및수수료를무통장,무인감으로인출함에동의 | checkbox | 동의함 |
| 상담자 | 상담자 | 상담자(직위/성명) | text |  |
| 목록[].자금용도 | 목록[].자금용도 | 자금용도 | text | 자녀 교육비 |
| employer.phone | employer.phone | 직장전화번호 | phone | 043-783-2775 |
| 가구총소득 | 가구총소득 | 가구총소득 | number | 0.94 |
| 제외부채 | 제외부채 | 제외부채 | number | 28.65 |
| 기타조달 | 기타조달 | 기타조달 | number | 43.88 |
| 목록[].담보종류 | 목록[].담보종류 | 담보종류 | text |  |
| employer.hire_date | employer.hire_date | 입사일자 | date | 2020.05.08 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김정수 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 고하인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 남경유 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 확인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 이유경 |
| 신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | text |  |
| check.신규증액채무인수한도감액한도완제처리시안내 | check.신규증액채무인수한도감액한도완제처리시안내 | 신규,증액,채무인수,한도감액,한도완제처리시안내 | checkbox | 원치않음 |
| check.신청대출승인완료시안내문자통지 | check.신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | checkbox | 원치않음 |
| check.동의함 | check.동의함 | 동의함( | checkbox | 문자 |
| check.중도상환해약금면제시점도래안내문자통지 | check.중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | checkbox | 동의함 |
| check.우편 | check.우편 | 우편 | checkbox | 자택 |
| check.문자 | check.문자 | 문자 | checkbox | 원치않음 |
| check.이메일 | check.이메일 | 이메일 | checkbox | 원치않음 |
| 대출부수거래충족여부안내통지 | 대출부수거래충족여부안내통지 | 대출부수거래충족여부안내통지(문자만) | text |  |
| 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | text |  |

### hf056 · [필수] 개인(신용)정보 제3자 제공 동의서(하나더넥스트 내집연금용_역모기지)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.56 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공에동의하십니까? | checkbox | 동의함 |
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.name | customer.name | 본인성명 | text | 박찬연 |
| spouse.name | spouse.name | 배우자성명 | text | 이건빈 |
| date2 | date2 | 작성일(년월일) | date | 2026.01.31 |

### hf058 · 융자상담 및 차입신청서(기업용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.58 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 신규 |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 이욱유 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| company.address | corp.address | 사업장주소 | text | 서울특별시 중구 다산로 361, 6층 |
| company.biz_no | corp.biz_no | 사업자번호(생년월일) | biz_no | 264-82-36559 |
| 사업장전화번호 | 사업장전화번호 | 사업장전화번호 | phone | 010-5907-7253 |
| 대출과목 | 대출과목 | 대출과목 | text | 일반자금대출 |
| 신청금액 | 신청금액 | 신청금액 | number | 52,520,000원 |
| check.대출기간만료일 | check.대출기간만료일 | 대출기간만료일 | checkbox | 대출실행(한도약정)일로부터 |
| 거치기간 | 거치기간 | 거치기간 | number | 2 |
| check.상환방법 | check.상환방법 | 상환방법 | checkbox | 기타( |
| check.자금용도 | check.자금용도 | 자금용도 | checkbox | 운영자금(급여, 원자재매입 등) |
| check.거래구분 | check.거래구분 | 거래구분 | checkbox | 한도 |
| check.금리적용방식 | check.금리적용방식 | 금리적용방식 | checkbox | 변동 |
| 부채현황_목록[].금융기관명 | 부채현황_목록[].금융기관명 | 금융기관명 | text | 신한은행 |
| company.address2 | company.address2 | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| 종류 | 종류 | 종류 | text | 하나 MMF |
| employer.name | employer.name | 직장명(직위) | text | 주식회사 태평양무역 |
| 부채현황_목록[].금액 | 부채현황_목록[].금액 | 금액 | number | 140,000원 |
| 수량 | 수량 | 수량 | number | 24 |
| 차주와의관계 | 차주와의관계 | 차주와의관계 | text |  |
| 부채현황_목록[].담보 | 부채현황_목록[].담보 | 담보 | text |  |
| 추정가액 | 추정가액 | 추정가액 | number | 3,460,000 |
| 실재산 | 실재산 | 실재산 | text |  |
| 담보제공자 | 담보제공자 | 담보제공자 | text |  |
| 나이 | 나이 | 나이 | text |  |
| 부채현황_목록[].자금용도 | 부채현황_목록[].자금용도 | 자금용도 | text | 투자 목적 |
| 신청인과의관계 | 신청인과의관계 | 신청인과의관계 | text |  |
| 보증종류 | 보증종류 | 보증종류 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 송현하 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김건준 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 이기유 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 임수도 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 안건지 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 확인 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 검인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 명혁인 |
| check.신규처리시안내 | check.신규처리시안내 | 신규처리시안내 | checkbox | 이메일 |
| customer.phone | customer.phone | 휴대폰번호 | phone | 010-5907-7253 |
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| check.동의함 | check.동의함 | 동의함( | checkbox | 이메일 |
| customer.phone2 | customer.phone2 | 휴대폰번호 | phone | 010-5907-7253 |
| customer.email2 | customer.email2 | E-mail | text | chanyeon363@naver.com |
| check.확인서 | check.확인서 | 확인서(담보제공자용) | checkbox | 해당 |
| check.확인서2 | check.확인서2 | 확인서(담보제공자용) | checkbox | 미해당 |
| 대출금입금계좌 | 대출금입금계좌 | 대출금입금(실행)계좌 | text | 295-702848-88938 |
| 원금및이자자동이체결제계좌 | 원금및이자자동이체결제계좌 | 원(리)금및이자자동이체결제계좌 | number | 42,900,000 |
| 설정순위 | 설정순위 | ●설정순위(설정일자) | text |  |
| 부동산담보대출접수번호 | 부동산담보대출접수번호 | 부동산담보대출●접수번호(등기부등본기준) | text | 782446-6734277 |

### hf059 · 개인(신용)정보 조회 동의서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.59 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 거래와관련한개인정보조회 | 거래와관련한개인정보조회 | (금융)거래와관련한개인(신용)정보조회 | text |  |
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 국내거소신고번호성명주소전화번호 | 국내거소신고번호성명주소전화번호 | 국내거소신고번호,성명,주소,전화번호 | phone | 010-5907-7253 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 이용목적 | 이용목적 | 이용목적 | text | 주택구입 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 검인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 길성현 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김아예 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 성정경 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김원도 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김찬재 |
| 일반개인정보2 | 일반개인정보2 | ■일반개인정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| 국내거소신고번호성명 | 국내거소신고번호성명 | 국내거소신고번호,성명 | text | 144-826179-44556 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| 제공받는자와동일 | 제공받는자와동일 | 제공받는자와동일 | date | 2025년 6월 20일 |
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보조회에동의하십니까 | check.위고유식별정보조회에동의하십니까 | 위고유식별정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보조회에동의하십니까 | check.위개인정보조회에동의하십니까 | 위개인(신용)정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 이욱유 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 박영준 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 위우호 |
| 이용목적2 | 이용목적2 | 이용목적 | text | 자녀 교육비 |
| 재산채무소득의총액납세실적등 | 재산채무소득의총액납세실적등 | 재산·채무·소득의총액,납세실적등 | number | 32,890,000 |

### hf060 · [필수] 개인(신용)정보 수집이용 동의서(대출성상품 적합성적정성 판단용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.60 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 위나아 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 장민인 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 강석호 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 염철원 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 정석인 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김준우 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 현희도 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 류원민 |

### hf061 · 적합성, 적정성 고객정보 확인서(개인 및 개인사업자용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.61 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.email | customer.email | Email | text | chanyeon363@naver.com |
| check.후견인여부 | check.후견인여부 | 후견인여부 | checkbox | 해당사항 없음 |
| check.대출용도 | check.대출용도 | 대출용도 | checkbox | 기타 |
| check.총자산규모 | check.총자산규모 | 총자산규모(순자산) | checkbox | 억원 미만 |
| check.담보제공계획 | check.담보제공계획 | 담보제공계획 | checkbox | 없음 |
| check.담보제공계획2 | check.담보제공계획2 | 담보제공계획 | checkbox | 있음 |
| check.소득없음 | check.소득없음 | 소득없음 | checkbox | 소득없음 |
| check.부채 | check.부채 | 부채 | checkbox | 천만원 미만 |
| check.연체여부 | check.연체여부 | 연체여부 | checkbox | 연체정보 없음 |
| check.신용점수 | check.신용점수 | 신용점수 | checkbox | 보기2 |
| check.근로소득 | check.근로소득 | 근로소득 | checkbox | 임대소득 |
| customer.birth | customer.birth | 생년월일 | date | 900210 |
| 기거래건전성 | 기거래건전성 | 기거래건전성 | text |  |
| 신용상태 | 신용상태 | 신용상태 | text |  |
| 상환능력및변제계획 | 상환능력및변제계획 | 상환능력및변제계획 | text |  |
| 진단결과번호 | 진단결과번호 | 진단결과번호 | text | 629-950578-50244 |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 강순준 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| signer2.name | signer2.name | 신청인 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신청인 | seal | 강순준 |
| sign.signer2 | sign.signer2 | 신청인 | signature | 박찬연 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 마소린 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 이민호 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 류소린 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 표호은 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 이현서 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 배기은 |

### hf062 · 적합성, 적정성 고객정보 확인서(법인용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.62 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 업체명 | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자명 | text | 박찬연 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 대표자연락처 | 대표자연락처 | 대표자연락처 | phone | 010-5907-7253 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 상시근로자수 | 상시근로자수 | 상시근로자수 | text |  |
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| check.전문금융소비자여부 | check.전문금융소비자여부 | 전문금융소비자여부 | checkbox | 자산의 취득 또는 자금 조달 등 특정목적을 위해 설립된 법인 |
| check.전문금융소비자여부2 | check.전문금융소비자여부2 | 전문금융소비자여부 | checkbox | 일반금융소비자 |
| 업력 | 업력 | 업력 | number | 24 |
| check.총자산규모 | check.총자산규모 | 총자산규모(순자산) | checkbox | 억원 이상 |
| check.주택증권지식재산권등의담보제공예정 | check.주택증권지식재산권등의담보제공예정 | 주택,증권(주식,채권등),지식재산권등의담보제공예정 | checkbox | 있음 |
| check.담보제공계획 | check.담보제공계획 | 담보제공계획 | checkbox | 없음 |
| check.매출액 | check.매출액 | 매출액 | checkbox | 억원 미만 |
| check.순이익 | check.순이익 | 순이익 | checkbox | 전년도 순이익 없음 |
| check.부채 | check.부채 | 부채 | checkbox | 억원 이상 10억원 미만 |
| check.연체여부 | check.연체여부 | 연체여부 | checkbox | 연체정보 있음 |
| check.변제방법 | check.변제방법 | 변제방법 | checkbox | 기타소득 |
| check.대출용도 | check.대출용도 | 대출용도 | checkbox | 운전자금 |
| check.최근3년간연속자본잠식 | check.최근3년간연속자본잠식 | 최근3년간연속자본잠식 | checkbox | 비해당 |
| 기거래건전성 | 기거래건전성 | 기거래건전성 | text |  |
| 신용상태 | 신용상태 | 신용상태 | text |  |
| 상환능력및변제계획 | 상환능력및변제계획 | 상환능력및변제계획 | text |  |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 이욱유 |
| signer2.name | signer2.name | 신청인 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신청인 | seal | 현예지 |
| sign.signer2 | sign.signer2 | 신청인 | signature | 박찬연 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 확인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 검인 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 확인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 노예아 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| agent.relation | agent.relation | 관계 | text | 부 |

### hf064 · 대출정보 열람청구, 상환 및 말소접수 위임장(주택담보대출 대출이동서비스)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.64 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일 | date | 900210 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 위임인(본인) | text | 박찬연 |
| seal.signer | seal.customer | 위임인(본인) | seal | 강순준 |
| sign.signer | sign.customer | 위임인(본인) | signature | 박찬연 |

### hf065 · 국토교통부 주택소유확인 시스템 등 이용 관련 [필수] 개인(신용)정보 수집·이용·제공 동의서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.65 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 김승빈 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 신기희 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 백동서 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 임아빈 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 이현서 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이성예 |
| 일반개인정보2 | 일반개인정보2 | ■일반개인정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 현예지 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| signer2.name | family.name | 세대원성명 | text | 박영준 |
| seal.signer2 | seal.signer2 | 세대원성명 | seal | 이도민 |
| sign.signer2 | sign.signer2 | 세대원성명 | signature | 박영준 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer3.name | signer3.name | 세대원성명 | text | 박영준 |
| seal.signer3 | seal.signer3 | 세대원성명 | seal | 박영준 |
| sign.signer3 | sign.signer3 | 세대원성명 | signature | 강석호 |
| signer4.name | signer4.name | 세대원성명 | text | 박영준 |
| seal.signer4 | seal.signer4 | 세대원성명 | seal | 박영준 |
| sign.signer4 | sign.signer4 | 세대원성명 | signature | 장민인 |
| signer5.name | signer5.name | 세대원성명 | text | 이도민 |
| seal.signer5 | seal.signer5 | 세대원성명 | seal | 이도민 |
| sign.signer5 | sign.signer5 | 세대원성명 | signature | 장민인 |
| signer6.name | signer6.name | 세대원성명 | text | 강석호 |
| seal.signer6 | seal.signer6 | 세대원성명 | seal | 장민인 |
| sign.signer6 | sign.signer6 | 세대원성명 | signature | 강석호 |

### hf066 · 대출정보 열람청구 및 상환 위임장(대출이동서비스)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.66 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일 | date | 1990-02-10 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 위임자(본인) | text | 박찬연 |
| seal.signer | seal.customer | 위임자(본인) | seal | 현예지 |
| sign.signer | sign.customer | 위임자(본인) | signature | 박찬연 |

### hf067 · [필수] 개인(신용)정보 수집 · 이용 동의서[대출이동서비스]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.67 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 현예지 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| ᄋ금융사고조사분쟁해결민원처리 | ᄋ금융사고조사분쟁해결민원처리 | ᄋ금융사고조사,분쟁해결,민원처리 | text |  |
| ᄋ법령상의무이행 | ᄋ법령상의무이행 | ᄋ법령상의무이행 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 검인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 백태도 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 왕수은 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 왕유진 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 전혁인 |

### hf068 · 계약 체결 이행 등을 위한 필수 동의서(개인금융성 신용보험용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.68 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 대위변제시대위권행사 | 대위변제시대위권행사 | -대위변제시대위권행사 | text |  |
| 인의관계등기타개인신용정보분리보관정보 | 인의관계등기타개인신용정보분리보관정보 | 인의관계등기타개인신용정보,분리보관정보 | text |  |
| 신용도판단정보 | 신용도판단정보 | ■신용도판단정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공*에동의하십니까? | checkbox | 동의함 |
| 공공정보등2 | 공공정보등2 | ■공공정보등 | text |  |
| check.위고유식별정보조회에동의하십니까 | check.위고유식별정보조회에동의하십니까 | 위고유식별정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인신용정보조회에동의하십니까 | check.위개인신용정보조회에동의하십니까 | 위개인신용정보조회에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인 | text | 박찬연 |
| seal.signer | seal.customer | 본인 | seal | 박찬연 |
| sign.signer | sign.customer | 본인 | signature | 강순준 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 법정대리인 | text | 박영준 |
| seal.signer2 | seal.agent | 법정대리인 | seal | 이도민 |
| sign.signer2 | sign.agent | 법정대리인 | signature | 박영준 |

### hf069 · 기업간결제 제신고(약정해지,변경) 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.69 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 업체명 | text | (주)유니온무역 |
| customer.phone | customer.phone | 연락처(선택) | phone | 010-5907-7253 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 대표자생년월일 | 대표자생년월일 | 대표자/생년월일 | date | 2026.01.30 |
| customer.address | customer.address | 주소(선택) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.신청내용 | check.신청내용 | 신청내용 | checkbox | 사업자번호 변경 |
| 변경내용 | 변경내용 | 변경내용 | text | 해당 없음 |
| 약정상품명 | 약정상품명 | 약정상품명 | text | 하나 MMF |
| 약정번호 | 약정번호 | 약정번호 | rrn | 472435-8232120 |
| 변경후 | 변경후 | 변경후 | text | 해당 없음 |
| customer.name | customer.name | 위임인 | text | 박찬연 |
| agent.name | agent.name | 대리인성명 | text | 박영준 |
| customer.phone2 | customer.phone2 | 연락처 | phone | 010-5907-7253 |
| 위임내용 | 위임내용 | 위임내용 | text | 해당 없음 |
| customer.birth | customer.birth | 생년월일 | date | 900210 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 업체명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 업체명 | seal | (주)유니온무역 |
| sign.signer | sign.customer | 업체명 | signature | 주식회사 한빛패션 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 검인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 신영경 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 정선희 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 배진원 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 이용수 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 민윤유 |

### hf072 · 전자방식 외상매출채권 결제제도 이용신청서(외담대,동반성장론,e-안심팩토링대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.72 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 법인명(또는상호명) | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표이사(또는대표자명) | text | 박찬연 |
| company.biz_type | company.biz_type | 업태 | text | 도매 및 소매업 |
| 주요취급품목 | 주요취급품목 | 주요취급품목 | text | 커피 원두 |
| value | value | (우편번호:) | amount |  |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| check.기업규모 | check.기업규모 | 기업규모 | checkbox | 중기업 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호(법인의경우) | corp_reg_no | 200112-7448551 |
| 대표이사생년월일 | 대표이사생년월일 | 대표이사(대표자)생년월일 | date | 2026-01-18 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| 팩스번호 | 팩스번호 | 팩스번호 | phone | 043-783-2775 |
| check.구매기업 | check.구매기업 | 구매기업(중심기업) | checkbox | 구매기업 (중심기업) |
| check.구매기업2 | check.구매기업2 | 구매기업(온라인마켓) | checkbox | 구매기업(온라인마켓) |
| check.판매기업 | check.판매기업 | 판매기업(1차협력기업) | checkbox | 판매기업(1차협력기업) |
| check.입점Seller | check.입점Seller | 입점Seller(판매기업) | checkbox | 입점 Seller(판매기업) |
| check.동반협력기업 | check.동반협력기업 | 동반협력기업 | checkbox | 동반협력기업 |
| check.협력기업 | check.협력기업 | 협력기업 | checkbox | 협력기업 |
| 협력기업을위한채권발행및Exposure약정 | 협력기업을위한채권발행및Exposure약정 | 협력기업(판매기업)을위한채권발행및Exposure약정 | text | (주)세진시스템즈 |
| 입점Seller를위한채권발행 | 입점Seller를위한채권발행 | 입점Seller(판매기업)를위한채권발행 | text |  |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| 동반협력기업간상생매출채권발행및수취약정 | 동반협력기업간상생매출채권발행및수취약정 | 동반협력기업간상생매출채권발행및수취약정 | number | 43,460,000 |
| 공급망상생결제협력기업간상생매출채권발행및수취약정 | 공급망상생결제협력기업간상생매출채권발행및수취약정 | 공급망상생결제협력기업간상생매출채권발행및수취약정 | number | 96,890,000 |
| 담당부서 | 담당부서 | 담당부서 | text |  |
| check.SKT | check.SKT | SKT | checkbox | KT |
| check.해당되는 | check.해당되는 | 해당되는“ | checkbox | ”에 “V” 표시 합니다. |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이다아 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김옥호 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 허미윤 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 검인 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 김재유 |
| 담당자팩스번호 | 담당자팩스번호 | 담당자팩스번호 | phone | 043-783-2775 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 현예지 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |

### hf073 · [필수] 개인(신용)정보 제3자 제공 동의서(안전망대출Ⅱ)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.73 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 안전망대출II보증업무수행 | 안전망대출II보증업무수행 | 안전망대출II보증업무수행 | text |  |
| 신용도판단정보 | 신용도판단정보 | ■신용도판단정보 | text |  |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1****** |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| date | date | 작성일 | date | 2026년 1월 31일 |

### hf074 · [필수] 개인(신용)정보 제3자 제공 동의서(햇살론17)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.74 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 햇살론17보증업무수행 | 햇살론17보증업무수행 | -햇살론17보증업무수행 | text |  |
| 신용능력정보 | 신용능력정보 | ■신용능력정보 | text |  |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 박영준 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 이도민 |

### hf077 · [필수]개인(신용)정보 제3자 제공 동의서(토지분양대금대출약정_대전광역시,대전도시공사)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.77 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 대전광역시대전도시공사 | 대전광역시대전도시공사 | -대전광역시,대전도시공사 | text |  |
| 제공일로부터5년까지보유이용 | 제공일로부터5년까지보유이용 | -제공일로부터5년까지보유·이용 | text |  |
| 신용거래정보 | 신용거래정보 | ■■신용거래정보 | text |  |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 이주원 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 강석호 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 박영준 |
| 이용목적 | 이용목적 | 이용목적 | text | 타행 이체 |

### hf078 · 통화전환 옵션부 외화대출 원화대출 전환신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.78 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 원화대출전환희망일 | 원화대출전환희망일 | 원화대출전환희망일 | date | 2025-09-14 |
| 신청사유 | 신청사유 | 신청사유 | text | 자녀 교육비 |
| 대출과목 | 대출과목 | 대출과목 | text | 운전자금대출 |
| 대출금액 | 대출금액 | 대출금액(본건전환후외화대출잔액) | number | 23,180,000 |
| date | date | 대출취급일 | date | 2026년 1월 31일 |
| date2 | date2 | 대출만기일 | date | 2026년 1월 31일 |
| 대출금리 | 대출금리 | 대출금리 | number | 50 |
| date3 | date3 | 일자 | date | 2026년 1월 31일 |
| date4 | date4 | 년월일 | date | 2026.01.31 |
| 주1 | 주1 | 주1 | text |  |
| date5 | date5 | 년월일 | date | 2026.01.31 |
| 주3 | 주3 | 주3 | text |  |
| date6 | date6 | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 채무자본인 | text | 박찬연 |
| seal.signer | seal.customer | 채무자본인 | seal | 이욱유 |
| sign.signer | sign.customer | 채무자본인 | signature | 박찬연 |

### hf079 · 정보교환 기업구매자금어음금 미결제통보확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.79 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 미결제통보번호 | 미결제통보번호 | 미결제통보번호 | text | 494-782888-54252 |
| 추심의뢰일 | 추심의뢰일 | 추심의뢰일 | date | 2025년 8월 22일 |
| 금융결제원어음번호 | 금융결제원어음번호 | 금융결제원어음번호 | text | 나마64647941 |
| 어음금액 | 어음금액 | 어음금액 | number | 280,000 |
| 발행인 | 발행인 | 발행인 | text | (주)미래상사 |
| 사유 | 사유 | 사유 | text | 투자 목적 |
| 미결제확인번호 | 미결제확인번호 | 미결제확인번호 | text | 125-895024-41164 |
| Fax | Fax | Fax()- | text |  |
| Fax2 | Fax2 | Fax()- | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.signer | seal.signer | _____________________부(지점) | seal | 연도예 |
| sign.signer | sign.signer | _____________________부(지점) | signature | 김옥호 |
| seal.signer2 | seal.signer2 | _____________________부(지점) | seal | 김민정 |
| sign.signer2 | sign.signer2 | _____________________부(지점) | signature | 연민주 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이지영 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 박찬연 |

### hf080 · 정보교환 기업구매자금어음 부도통보확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.80 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 부도통보번호 | 부도통보번호 | 부도통보번호 | text | 995232-8862246 |
| 추심의뢰일 | 추심의뢰일 | 추심의뢰일 | date | 2025.08.24 |
| 금융결제원어음번호 | 금융결제원어음번호 | 금융결제원어음번호 | text | 아라56768451 |
| 어음금액 | 어음금액 | 어음금액 | number | 205,470,000 |
| 발행인 | 발행인 | 발행인 | text | (주)제일메디칼 |
| 사유 | 사유 | 사유 | text | 급여 수령 |
| 부도확인번호 | 부도확인번호 | 부도확인번호 | text | 1796-8239 |
| Fax | Fax | Fax()- | text |  |
| Fax2 | Fax2 | Fax()- | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.signer | seal.signer | _____________________부(지점) | seal | 김유정 |
| sign.signer | sign.signer | _____________________부(지점) | signature | 김소찬 |
| seal.signer2 | seal.signer2 | _____________________부(지점) | seal | 원나주 |
| sign.signer2 | sign.signer2 | _____________________부(지점) | signature | 최재주 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 정건유 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이주아 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 이주수 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 민혜지 |

### hf081 · 정보교환 기업구매자금어음 인수거절통보확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.81 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 인수거절통보번호 | 인수거절통보번호 | 인수거절통보번호 | text | 502-219827-35378 |
| 추심의뢰일 | 추심의뢰일 | 추심의뢰일 | date | 2025-11-14 |
| 금융결제원어음번호 | 금융결제원어음번호 | 금융결제원어음번호 | text | 바라39202580 |
| 어음금액 | 어음금액 | 어음금액 | number | 5,080,000 |
| 발행인 | 발행인 | 발행인 | text | 미래물산 |
| 사유 | 사유 | 사유 | text | 투자 목적 |
| 인수거절확인번호 | 인수거절확인번호 | 인수거절확인번호 | text | 0697-7410 |
| Fax | Fax | Fax()- | text |  |
| Fax2 | Fax2 | Fax()- | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.signer | seal.signer | _____________________부(지점) | seal | 지규혜 |
| sign.signer | sign.signer | _____________________부(지점) | signature | 심윤민 |
| seal.signer2 | seal.signer2 | _____________________부(지점) | seal | 김주율 |
| sign.signer2 | sign.signer2 | _____________________부(지점) | signature | 반영린 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 박원재 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김소현 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 박은하 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이선예 |

### hf082 · 채권발행 등록 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.82 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 구매기업명 | 구매기업명 | 구매기업명 | text | (주)가온푸드 |
| 총처리건수 | 총처리건수 | 총처리건수 | number | 60 |
| 구매기업사업자등록번호 | 구매기업사업자등록번호 | 구매기업사업자등록번호 | biz_no | 781-77-32938 |
| 총처리금액 | 총처리금액 | 총처리금액 | number | 17,280,000 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 호 | 호 | 호 | text |  |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| signer.name | customer.name | 자 | text | 박찬연 |
| seal.signer | seal.customer | 자 | seal | 현예지 |
| sign.signer | sign.customer | 자 | signature | 박찬연 |
| 소 | 소 | 소 | text |  |
| signer2.name | signer2.name | 명 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 명 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 명 | signature | 강순준 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 권숙호 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이정우 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 엄현영 |
| 목록[].중심업체코드 | 목록[].중심업체코드 | 중심업체코드 | text | 263651 |
| 목록[].판매기업사업자번호 | 목록[].판매기업사업자번호 | 판매기업사업자번호 | text | 264-82-36559 |
| 목록[].판매기업명 | 목록[].판매기업명 | 판매기업명 | text | 세진물산(주) |
| 목록[].채권발행일자채권만기일자 | 목록[].채권발행일자채권만기일자 | 채권발행일자채권만기일자 | text | 2029.05.05 |
| 목록[].채권금액 | 목록[].채권금액 | 채권금액 | text | 390,000 |
| 목록[].세금계산서승인번호 | 목록[].세금계산서승인번호 | 세금계산서승인번호 | text | 5815-0462 |
| 목록[].세금계산서합계금액 | 목록[].세금계산서합계금액 | 세금계산서합계금액 | text | 170,760,000 |
| 목록[].세금계산서작성일자 | 목록[].세금계산서작성일자 | 세금계산서작성일자 | text | 2025년 7월 9일 |

### hf083 · 전자방식 외상매출채권 결제제도 이용신청서 (서울시농수산식품공사용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.83 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 법인명(또는상호명) | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표이사(또는대표자명) | text | 박찬연 |
| company.biz_type | company.biz_type | 업태 | text | 도매 및 소매업 |
| 주요취급품목 | 주요취급품목 | 주요취급품목 | text | 식품 원재료 |
| value | value | (우편번호:) | amount |  |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| check.기업규모 | check.기업규모 | 기업규모 | checkbox | 중기업 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호(법인인경우) | corp_reg_no | 200112-7448551 |
| 대표이사생년월일 | 대표이사생년월일 | 대표이사(대표자)생년월일 | date | 2025년 8월 11일 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| 팩스번호 | 팩스번호 | 팩스번호 | phone | 043-783-2775 |
| check.외상매출채권의 | check.외상매출채권의 | 외상매출채권의 | checkbox | 외상매출채권의 |
| check.판매기업 | check.판매기업 | 판매기업 | checkbox | 판매기업 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| 담당부서 | 담당부서 | 담당부서 | text |  |
| check.SKT | check.SKT | SKT | checkbox | LGU+ |
| 담당자팩스번호 | 담당자팩스번호 | 담당자팩스번호 | phone | 043-783-2775 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 강순준 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 황보호예 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 추나현 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 왕연정 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이철하 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 남우인 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 검인 |

### hf084 · 외상매출채권 양도통지서(장래채권양도통지용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.84 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 주식회사하나은행 | text | 김정진 |
| seal.signer | seal.signer | 주식회사하나은행 | seal | 길나예 |
| sign.signer | sign.signer | 주식회사하나은행 | signature | 조용우 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer2.name | signer2.name | 주식회사하나은행 | text | 하지영 |
| seal.signer2 | seal.signer2 | 주식회사하나은행 | seal | 전옥원 |
| sign.signer2 | sign.signer2 | 주식회사하나은행 | signature | 하지영 |
| customer.address3 | customer.address3 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |

### hf085 · 신용정보 제공 동의서(외담대,e-안심팩토링,동반성장론 구매기업용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.85 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].상품명 | 목록[].상품명 | 상품명 | text | 하나 정기예금 |
| 목록[].중심업체코드 | 목록[].중심업체코드 | 중심업체코드 | number | 803603 |
| 목록[].한도승인번호 | 목록[].한도승인번호 | 한도승인번호 | number | 35,500,000 |
| 목록[].정보제공내용 | 목록[].정보제공내용 | 정보제공내용 | text | 해당 없음 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| 신용거래정보의제공목적 | 신용거래정보의제공목적 | ■신용거래정보의제공목적 | text |  |
| 신용거래정보의제공받을자 | 신용거래정보의제공받을자 | ■신용거래정보의제공받을자 | text |  |
| 제공할신용거래정보등의내용및범위 | 제공할신용거래정보등의내용및범위 | ■제공할신용거래정보등의내용및범위 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | corp.name | 동의자본인회사명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 동의자본인회사명 | seal | (주)대한시스템즈 |
| sign.signer | sign.customer | 동의자본인회사명 | signature | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| customer.phone | customer.phone | 전화번호(선택항목) | phone | 010-5907-7253 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 이욱연 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이찬영 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 선우미주 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 최훈영 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 검인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 검인 |

### hf086 · 미래채권담보대출 협력기업 일괄추천서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.86 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].업체명 | 목록[].업체명 | 업체명 | text | (주)유니온무역 |
| 목록[].대표자 | 목록[].대표자 | 대표자 | text |  |
| 목록[].법인번호 | 목록[].법인번호 | 법인번호 | text | 009-177134-17430 |
| 목록[].사업자번호 | 목록[].사업자번호 | 사업자번호 | text | 498-59-90099 |
| 총계 | 총계 | 총계 | text |  |
| 목록[].최초거래일자 | 목록[].최초거래일자 | 최초거래일자 | text | 2025.09.23 |
| 목록[].납품실적 | 목록[].납품실적 | 납품실적* | text |  |
| 목록[].평균결제기간 | 목록[].평균결제기간 | 평균결제기간* | text |  |
| 목록[].주소 | 목록[].주소 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 목록[].전화 | 목록[].전화 | 전화 | text | 010-5907-7253 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | corp.name | (회사명) | text | (주)유니온무역 |
| seal.signer | seal.corp | (회사명) | seal | (주)유니온무역 |
| sign.signer | sign.customer | (회사명) | signature | 주식회사 한빛패션 |

### hf087 · 미래채권담보대출 추천서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.87 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 최초거래일자 | 최초거래일자 | 최초거래일자 | date | 2025년 8월 3일 |
| 연간 | 연간 | 연간 | text |  |
| 계약서 | 계약서 | 계약서(주1) | text |  |
| 평균결제기간 | 평균결제기간 | 평균결제기간(주2) | text |  |
| 백만원 | 백만원 | ()백만원 | text |  |
| 전자결제방식 | 전자결제방식 | 전자결제방식 | text |  |
| 전자방식외상매출채권전자어음구매전용카드 | 전자방식외상매출채권전자어음구매전용카드 | ()전자방식외상매출채권()전자어음()구매전용카드 | number | 5,070,000원 |
| customer.phone | customer.phone | 연락처(핸드폰번호) | phone | 010-5907-7253 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | corp.name | 업체명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 업체명 | seal | (주)유니온무역 |
| sign.signer | sign.customer | 업체명 | signature | 주식회사 대성패션 |
| signer2.name | corp.ceo | 대표자 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 대표자 | seal | 이민빈 |
| sign.signer2 | sign.signer2 | 대표자 | signature | 박찬연 |
| 납품 | 납품 | 납품 | text |  |

### hf088 · 기업구매자금어음 추심취소 및 반환의뢰서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.88 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].사업자번호 | 목록[].사업자번호 | 사업자번호 | text | 865-34-26760 |
| 목록[].사업자명 | 목록[].사업자명 | 사업자명 | text | (주)유니온무역 |
| 목록[].추심금액 | 목록[].추심금액 | 추심금액 | text | 180,000 |
| 건 | 건 | 건 | text |  |
| 목록[].추심의뢰일 | 목록[].추심의뢰일 | 추심의뢰일 | text | 2025년 4월 23일 |
| 목록[].지급은행 | 목록[].지급은행 | 지급은행 | text | 국민은행 |
| 목록[].대표품명 | 목록[].대표품명 | 대표품명 | text | LED 모듈 |
| 목록[].공급가액 | 목록[].공급가액 | 공급가액 | text | 1,730,000 |
| 목록[].반환사유 | 목록[].반환사유 | 반환사유 | text | 사업자금 |
| check.아래의기업구매자금어음을 | check.아래의기업구매자금어음을 | 아래의기업구매자금어음을( | checkbox | 추심취소 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 최승진 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 검인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김욱혜 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 반태우 |

### hf089 · 외상매출채권 양도통지서(e-안심팩토링대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.89 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.address3 | customer.address3 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |

### hf090 · 납품대금 선입금(벤더입금) 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.90 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 선입금신청금액 | 선입금신청금액 | 선입금(벤더입금)신청금액 | number | 230,000원 |
| 판매기업입금일 | 판매기업입금일 | 판매기업입금일(또는결제일) | date | 2025년 3월 13일 |
| 벤더기업명 | 벤더기업명 | 벤더기업명 | text | (주)세진푸드 |
| check.벤더취급수수료부담주체 | check.벤더취급수수료부담주체 | 벤더취급수수료부담주체(벤더입금건별₩1,000) | checkbox | 벤더기업 |
| 지급승인금액 | 지급승인금액 | 지급승인금액 | number | 1,000,000 |
| 벤더기업사업자등록번호 | 벤더기업사업자등록번호 | 벤더기업사업자등록번호 | biz_no | 834-45-73362 |
| check.벤더입금이자부담주체 | check.벤더입금이자부담주체 | 벤더입금이자부담주체 | checkbox | 판매기업 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| signer.name | corp.ceo | 대표자 | text | 박찬연 |
| seal.signer | seal.corp | 대표자 | seal | 박찬연 |
| sign.signer | sign.customer | 대표자 | signature | 현예지 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer2.name | customer.name | 성명 | text | 박찬연 |
| seal.signer2 | seal.customer | 성명 | seal | 김소윤 |
| sign.signer2 | sign.signer2 | 성명 | signature | 박찬연 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 나영주 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 왕주도 |
| seal.staff.대리 | seal.staff.대리 | 대리 | seal | 박규유 |
| sign.staff.대리 | sign.staff.대리 | 대리 | signature | 이도아 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 왕건빈 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 최유예 |
| 목록[].선입금신청금액 | 목록[].선입금신청금액 | 선입금신청금액 | text | 160,000 |
| 목록[].채권번호 | 목록[].채권번호 | 채권번호 | text | 769-109745-92690 |
| 목록[].채권금액 | 목록[].채권금액 | 채권금액 | text | 140,000원 |
| 목록[].발행일 | 목록[].발행일 | 발행일 | text | 2025년 11월 1일 |
| 목록[].결제일 | 목록[].결제일 | 결제일 | text | 2025-06-24 |
| 목록[].중심업체코드 | 목록[].중심업체코드 | 중심업체코드 | text | 5289 |
| 목록[].구매기업사업자번호 | 목록[].구매기업사업자번호 | 구매기업사업자번호 | text | 264-82-36559 |
| 목록[].구매기업명 | 목록[].구매기업명 | 구매기업명 | text | 주식회사 청솔테크 |

### hf091 · 기업구매자금 결제제도 이용 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.91 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 법인명(또는상호명) | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표이사(또는대표자명) | text | 박찬연 |
| company.biz_type | company.biz_type | 업태 | text | 도매 및 소매업 |
| 주요취급품목 | 주요취급품목 | 주요취급품목 | text | PCB 기판 |
| value | value | (우편번호:) | amount |  |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| 대표이사생년월일 | 대표이사생년월일 | 대표이사(대표자)생년월일 | date | 2025.06.03 |
| company.biz_item | corp.biz_item | 종목 | text | 무역 |
| 팩스번호 | 팩스번호 | 팩스번호 | phone | 043-783-2775 |
| 일반구매자금결제제도 | 일반구매자금결제제도 |  일반구매자금결제제도 | text |  |
| 담당부서 | 담당부서 | 담당부서 | text |  |
| 담당자전화번호 | 담당자전화번호 | 담당자전화번호 | phone | 010-5907-7253 |
| 담당자팩스번호 | 담당자팩스번호 | 담당자팩스번호 | phone | 043-783-2775 |
| 담당자명 | 담당자명 | 담당자명 | text | 황아인 |
| 담당자휴대전화번호 | 담당자휴대전화번호 | 담당자휴대전화번호 | phone | 010-5907-7253 |
| 담당자이메일 | 담당자이메일 | 담당자이메일 | date | 2025년 12월 2일 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 엄주정 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 검인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김규진 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 송아윤 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 검인 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 김희린 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 이환재 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 이경찬 |

### hf092 · 외상매출채권양도통지서(개별채권양도통지용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.92 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 발신인주소 | 발신인주소 | 발신인주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 발신인 | 발신인 | 발신인 | text |  |
| 수신인주소 | 수신인주소 | 수신인주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 수신인 | 수신인 | 수신인 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 주식회사하나은행 | text | 기훈린 |
| seal.signer | seal.signer | 주식회사하나은행 | seal | 장정준 |
| sign.signer | sign.signer | 주식회사하나은행 | signature | 김찬승 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 목록[].외상매출채권번호 | 목록[].외상매출채권번호 | 외상매출채권번호 | text | 5,040,000 |
| 목록[].채권양도인사업자번호 | 목록[].채권양도인사업자번호 | 채권양도인사업자번호 | text | 155-56-40221 |
| 목록[].채권양도인 | 목록[].채권양도인 | 채권양도인 | text | (주)유니온무역 |
| 목록[].채권양도금액 | 목록[].채권양도금액 | 채권양도금액 | text | 23,080,000원 |
| 목록[].채권발행일 | 목록[].채권발행일 | 채권발행일 | text | 2025.06.03 |
| 목록[].채권지급일 | 목록[].채권지급일 | 채권지급일 | text | 2025년 2월 26일 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |

### hf093 · 미결제 전자채권대금 입금확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.93 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].전자채권번호 | 목록[].전자채권번호 | 전자채권번호 | text | 957977-1822116 |
| 목록[].구매기업명 | 목록[].구매기업명 | 구매기업명(사업자번호) | text | (주)유니온무역 |
| 목록[].발행일 | 목록[].발행일 | 발행일 | text | 2025.06.11 |
| 목록[].만기일 | 목록[].만기일 | 만기일(미결제일) | text | 2025.08.21 |
| 목록[].입금액 | 목록[].입금액 | 입금액 | text | 210,000 |
| 목록[].입금일 | 목록[].입금일 | 입금일 | text | 2025.02.06 |
| 목록[].판매기업명 | 목록[].판매기업명 | 판매기업명 | text | 한빛로지스 |
| 목록[].판매기업계좌번호 | 목록[].판매기업계좌번호 | 판매기업계좌번호 | text | 597-555250-75543 |
| seal.signer | seal.signer | 지점장 | seal | 전상준 |
| sign.signer | sign.signer | 지점장 | signature | 주채연 |

### hf094 · 상생벤더구매론 승인명세 등록신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.94 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 차협력기업명 | 차협력기업명 | 차협력기업명 | text | 다온물산 |
| 총처리건수 | 총처리건수 | 총처리건수 | number | 1 |
| 차협력기업사업자등록번호 | 차협력기업사업자등록번호 | 차협력기업사업자등록번호 | biz_no | 615-22-78976 |
| 총처리금액 | 총처리금액 | 총처리금액 | number | 9,980,000 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 호 | 호 | 호 | text |  |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| signer.name | customer.name | 자 | text | 박찬연 |
| seal.signer | seal.customer | 자 | seal | 현예지 |
| sign.signer | sign.customer | 자 | signature | 박찬연 |
| 소 | 소 | 소 | text |  |
| signer2.name | signer2.name | 명 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 명 | seal | 현예지 |
| sign.signer2 | sign.signer2 | 명 | signature | 박찬연 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김예율 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 권서우 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 추경찬 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김훈율 |
| 목록[].원청채권종류 | 목록[].원청채권종류 | 원청채권종류 | text |  |
| 목록[].원청채권번호 | 목록[].원청채권번호 | 원청채권번호 | text | 576-876007-76785 |
| 목록[].원청구매기업명 | 목록[].원청구매기업명 | 원청구매기업명 | text | 주식회사 제일무역 |
| 목록[].사업자등록번호 | 목록[].사업자등록번호 | 사업자등록번호 | text | 153-37-79452 |
| 목록[].원청채권금액 | 목록[].원청채권금액 | 원청채권금액 | text | 74,630,000 |
| 목록[].원청채권발행일 | 목록[].원청채권발행일 | 원청채권발행일 | text | 2025-09-18 |
| 목록[].원청채권만기일 | 목록[].원청채권만기일 | 원청채권만기일 | text | 2026-12-02 |
| 목록[].차협력기업명 | 목록[].차협력기업명 | 차협력기업명 | text | 다온산업 |
| 목록[].승인금액 | 목록[].승인금액 | 승인금액 | text | 4,550,000원 |
| 목록[].선입금가능일 | 목록[].선입금가능일 | 선입금가능일 | text | 2024.12.29 |
| 목록[].세금계산서승인번호 | 목록[].세금계산서승인번호 | 세금계산서승인번호 | text | 1111-5985 |
| 목록[].세금계산서합계금액 | 목록[].세금계산서합계금액 | 세금계산서합계금액 | text | 4,340,000 |
| 목록[].세금계산서작성일자 | 목록[].세금계산서작성일자 | 세금계산서작성일자 | text | 2025년 6월 7일 |
| 목록[].품목명 | 목록[].품목명 | 품목명 | text | 포장재 |

### hf095 · 벤더승인명세 등록 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.95 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].하위벤더기업명 | 목록[].하위벤더기업명 | 하위벤더기업명 | text | (주)유니온무역 |
| 목록[].사업자등록번호 | 목록[].사업자등록번호 | 사업자등록번호 | text | 264-82-36559 |
| 목록[].벤더승인금액 | 목록[].벤더승인금액 | 벤더승인금액 | text | 440,000 |
| 목록[].세금계산서발행일 | 목록[].세금계산서발행일 | 세금계산서발행일 | text | 2025년 8월 28일 |
| 목록[].세금계산서발행금액 | 목록[].세금계산서발행금액 | 세금계산서발행금액 | text | 2,070,000 |
| 목록[].세금계산서승인번호 | 목록[].세금계산서승인번호 | 세금계산서승인번호 | text | 7743-5710 |
| 목록[].품목명 | 목록[].품목명 | 품목명 | text | 기계 부품 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 호 | 호 | 호 | text |  |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| signer.name | customer.name | 자 | text | 박찬연 |
| seal.signer | seal.customer | 자 | seal | 강순준 |
| sign.signer | sign.customer | 자 | signature | 박찬연 |
| 소 | 소 | 소 | text |  |
| signer2.name | signer2.name | 명 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 명 | seal | 현예지 |
| sign.signer2 | sign.signer2 | 명 | signature | 강순준 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김진린 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 엄준승 |

### hf096 · 발주명세 등록신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.96 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 중심기업명 | 중심기업명 | 중심기업명 | text | (주)유니온메디칼 |
| 총처리건수 | 총처리건수 | 총처리건수 | number | 24 |
| 중심기업사업자등록번호 | 중심기업사업자등록번호 | 중심기업사업자등록번호 | biz_no | 264-82-36559 |
| 총처리금액 | 총처리금액 | 총처리금액 | number | 117,230,000 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 호 | 호 | 호 | text |  |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| signer.name | customer.name | 자 | text | 박찬연 |
| seal.signer | seal.customer | 자 | seal | 전영경 |
| sign.signer | sign.customer | 자 | signature | 박찬연 |
| 소 | 소 | 소 | text |  |
| signer2.name | signer2.name | 명 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 명 | seal | 현예지 |
| sign.signer2 | sign.signer2 | 명 | signature | 박찬연 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김태영 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 검인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 이주인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 표현찬 |
| 목록[].차협력기업명 | 목록[].차협력기업명 | 차협력기업명 | text | 미래정밀 |
| 목록[].사업자등록번호 | 목록[].사업자등록번호 | 사업자등록번호 | text | 264-82-36559 |
| 목록[].발주번호 | 목록[].발주번호 | 발주번호 | text | 909-899679-70163 |
| 목록[].발주금액 | 목록[].발주금액 | 발주금액 | text | 100,000 |
| 목록[].납품기한 | 목록[].납품기한 | 납품기한 | text | 2027-11-18 |
| 목록[].대금지급일 | 목록[].대금지급일 | 대금지급일 | text | 2025.02.03 |
| 목록[].대금지급확약비율 | 목록[].대금지급확약비율 | 대금지급확약비율 | text | 90 |
| 목록[].품목명 | 목록[].품목명 | 품목명 | text | 커피 원두 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |

### hf097 · 미래채권 대출신청서(미래대,상생미래대용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.97 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].대출실행일 | 목록[].대출실행일 | 대출실행일 | text | 2025-07-29 |
| 목록[].대출신청금액 | 목록[].대출신청금액 | 대출신청금액 | text | 10,990,000 |
| 목록[].의뢰일 | 목록[].의뢰일 | 의뢰일 | text | 2025.11.09 |
| 목록[].발주번호 | 목록[].발주번호 | 발주번호 | text | 057359-2046993 |
| 목록[].발주금액 | 목록[].발주금액 | 발주금액 | text | 33,370,000 |
| 목록[].납품기한 | 목록[].납품기한 | 납품기한 | text | 2028-03-29 |
| 목록[].대금지급일 | 목록[].대금지급일 | 대금지급일 | text | 2025.01.05 |
| 목록[].대금지급확약비율 | 목록[].대금지급확약비율 | 대금지급확약비율 | text | 100 |
| 목록[].구매기업사업자등록번호 | 목록[].구매기업사업자등록번호 | 구매기업사업자등록번호 | text | 174-15-09742 |
| 목록[].구매기업명 | 목록[].구매기업명 | 구매기업명 | text | (주)가온정밀 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 소 | 소 | 소 | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 문석서 |
| seal.staff.대리 | seal.staff.대리 | 대리 | seal | 검인 |
| sign.staff.대리 | sign.staff.대리 | 대리 | signature | 안영수 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김나린 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김유연 |

### hf098 · 기업구매자금어음 지급제시 명세

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.98 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].결제원어음번호 | 목록[].결제원어음번호 | 결제원어음번호 | text | 마마63016307 |
| 목록[].어음금액 | 목록[].어음금액 | 어음금액 | text | 4,720,000 |
| 목록[].인수거절여부 | 목록[].인수거절여부 | 인수거절여부 | text |  |
| 목록[].인수거절사유 | 목록[].인수거절사유 | 인수거절사유 | text | 사업자금 |
| 목록[].대출일 | 목록[].대출일 | 대출일 | text | 2025-01-31 |
| 목록[].대출신청금액 | 목록[].대출신청금액 | 대출신청금액 | text | 6,360,000 |
| 목록[].대출만기일 | 목록[].대출만기일 | 대출만기일 | text | 2030년 2월 21일 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |

### hf099 · 지급승인명세 등록 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.99 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 중심기업명 | 중심기업명 | 중심기업명 | text | 한빛전자 |
| 중심기업사업자등록번호 | 중심기업사업자등록번호 | 중심기업사업자등록번호 | biz_no | 264-82-36559 |
| 총처리금액 | 총처리금액 | 총처리금액 | number | 249,670,000 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 호 | 호 | 호 | text |  |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| signer.name | customer.name | 자 | text | 박찬연 |
| seal.signer | seal.customer | 자 | seal | 강순준 |
| sign.signer | sign.customer | 자 | signature | 현예지 |
| 소 | 소 | 소 | text |  |
| signer2.name | signer2.name | 명 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 명 | seal | 현예지 |
| sign.signer2 | sign.signer2 | 명 | signature | 박찬연 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 장철유 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 검인 |
| 목록[].판매기업사업자번호 | 목록[].판매기업사업자번호 | 판매기업사업자번호 | text | 264-82-36559 |
| 목록[].판매기업명 | 목록[].판매기업명 | 판매기업명 | text | 청솔푸드 |
| 목록[].구매기업결제일자 | 목록[].구매기업결제일자 | 구매기업결제일자 | text | 2025.02.09 |
| 목록[].판매기업입금일자 | 목록[].판매기업입금일자 | 판매기업입금일자 | text | 2025.01.23 |
| 목록[].승인금액 | 목록[].승인금액 | 승인금액 | text | 8,500,000 |
| 목록[].선입금가능일자 | 목록[].선입금가능일자 | 선입금가능일자 | text | 2025.04.04 |
| 목록[].세금계산서승인번호 | 목록[].세금계산서승인번호 | 세금계산서승인번호 | text | 103074-0173351 |
| 목록[].세금계산서합계금액 | 목록[].세금계산서합계금액 | 세금계산서합계금액 | text | 7,350,000 |
| 목록[].세금계산서작성일자 | 목록[].세금계산서작성일자 | 세금계산서작성일자 | text | 2025년 12월 26일 |
| 목록[].품목명 | 목록[].품목명 | 품목명 | text | 냉동 수산물 |

### hf100 · 창구대출신청서(전자채권담보대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.100 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].채권번호 | 목록[].채권번호 | 채권번호 | text | 777-228980-77775 |
| 목록[].구매기업명 | 목록[].구매기업명 | 구매기업명 | text | 주식회사 우진시스템즈 |
| 목록[].대표자 | 목록[].대표자 | 대표자 | text |  |
| 목록[].공급물품명 | 목록[].공급물품명 | 공급물품명 | text | 냉동 수산물 |
| 목록[].세금계산서발행일 | 목록[].세금계산서발행일 | 세금계산서발행일 | date | 2025.09.26 |
| 목록[].전자채권금액 | 목록[].전자채권금액 | 전자채권금액 | number | 620,000 |
| 목록[].만기일 | 목록[].만기일 | 만기일 | date | 2028.05.16 |
| 목록[].대출신청액 | 목록[].대출신청액 | 대출신청액 | text |  |
| 목록[].대출만기일 | 목록[].대출만기일 | 대출만기일 | date | 2029.06.09 |
| 목록[].입금계좌번호 | 목록[].입금계좌번호 | 입금계좌번호 | text | 427-579298-43874 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 인 | text | 박찬연 |
| seal.signer | seal.customer | 인 | seal | 박찬연 |
| sign.signer | sign.customer | 인 | signature | 강순준 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 소 | 소 | 소 | text |  |

### hf102 · 기업현황서(B2B전자결제서비스 업무, MP용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.102 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| date | date | 작성일 | date | 2026년 1월 31일 |
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| signer.name | corp.ceo | 대표이사 | text | 박찬연 |
| seal.signer | seal.corp | 대표이사 | seal | 박찬연 |
| sign.signer | sign.customer | 대표이사 | signature | 강순준 |
| employer.position | employer.position | 직위 | text | 대리 |
| signer2.name | signer2.name | 성명 | text | 박찬연 |
| seal.signer2 | seal.customer | 성명 | seal | 이민빈 |
| sign.signer2 | sign.signer2 | 성명 | signature | 박찬연 |
| 연락처TEL | 연락처TEL | 연락처:TEL | phone | 010-5907-7253 |
| customer.phone | customer.phone | HP | phone | 010-5907-7253 |
| FAX | FAX | FAX | phone | 043-783-2775 |
| company.name2 | company.name2 | 기업체명 | text | (주)유니온무역 |
| 본사 | 본사 | 본사 | text |  |
| 주사무소 | 주사무소 | 주사무소 | text |  |
| 사업장 | 사업장 | 사업장 | text |  |
| company.biz_item | corp.biz_item | 업종(표준산업분류기호) | text | 무역 |
| 종업원수 | 종업원수 | 종업원수 | text |  |
| 사업모델및특성_목록[].모델명 | 사업모델및특성_목록[].모델명 | 모델명 | text | PCB 기판 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 협회및단체가입 | 협회및단체가입 | 협회및단체가입 | text |  |
| 인허가등록 | 인허가등록 | 인허가등록 | text |  |
| 주거래은행 | 주거래은행 | 주거래은행 | text | 국민은행 |
| 총자산 | 총자산 | 총자산 | text |  |
| 자본금 | 자본금 | 자본금 | text |  |
| 자기자본 | 자기자본 | 자기자본 | text |  |
| 매출액 | 매출액 | 매출액 | number | 140,000 |
| 경상이익 | 경상이익 | 경상이익 | text |  |
| 당기순이익 | 당기순이익 | 당기순이익 | text |  |
| 사업모델및특성_목록[].내용 | 사업모델및특성_목록[].내용 | 내용 | text | 해당 없음 |
| company.ceo | company.ceo | 대표자 | text | 박찬연 |
| TEL | TEL | TEL | text |  |
| FAX2 | FAX2 | FAX | phone | 043-783-2775 |
| TEL2 | TEL2 | TEL | text |  |
| TEL3 | TEL3 | TEL | text |  |
| 설립년월 | 설립년월 | 설립년월 | text |  |
| 사업모델및특성_목록[].특성 | 사업모델및특성_목록[].특성 | 특성 | text |  |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| 정부기관및금융기관우대 | 정부기관및금융기관우대 | 정부기관및금융기관우대 | text | 우리은행 |
| 요약재무현황_목록[].년 | 요약재무현황_목록[].년 | 년 | text |  |
| 당좌거래은행 | 당좌거래은행 | 당좌거래은행 | text | 국민은행 |
| 목록[].주주명 | 목록[].주주명 | 주주명 | text | 홍채혜 |
| 목록[].소유주식수 | 목록[].소유주식수 | 소유주식수 | text |  |
| 목록[].지분율 | 목록[].지분율 | 지분율 | text | 85 |
| 목록[].대주주와의관계 | 목록[].대주주와의관계 | 대주주와의관계 | text |  |
| 목록[].회사와의관계 | 목록[].회사와의관계 | 회사와의관계 | text |  |
| 목록[].성명 | 목록[].성명 | 성명 | text | 박찬연 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| 주요경력_목록[].기간 | 주요경력_목록[].기간 | 기간 | text |  |
| 주요경력_목록[].근무처 | 주요경력_목록[].근무처 | 근무처 | text |  |
| 주요경력_목록[].담당업무 | 주요경력_목록[].담당업무 | 담당업무 | text |  |
| 주요경력_목록[].최종직위 | 주요경력_목록[].최종직위 | 최종직위 | text |  |
| 목록[].직위 | 목록[].직위 | 직위 | text |  |
| 목록[].관계 | 목록[].관계 | 관계 | text |  |
| 목록[].주요경력 | 목록[].주요경력 | 주요경력 | text |  |
| 목록[].연월일 | 목록[].연월일 | 연월일 | text | 2025.12.23 |
| 목록[].내용 | 목록[].내용 | 내용 | text | 해당 없음 |
| 제품명 | 제품명 | 제품명 | text | 식품 원재료 |
| 판매처 | 판매처 | 판매처 | text |  |
| 목록[].년 | 목록[].년 | 년 | text |  |
| 판매조건 | 판매조건 | 판매조건 | text |  |
| 원재료명 | 원재료명 | 원재료명 | text |  |
| 구매처 | 구매처 | 구매처 | text |  |
| 구매조건 | 구매조건 | 구매조건 | text |  |

### hf103 · B2B 전자결제서비스 업무 이용신청서(MP용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.103 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.biz_type | company.biz_type | 업태 | text | 도매 및 소매업 |
| company.name | corp.name | 기업명(MP상호명) | text | (주)유니온무역 |
| MPURL | MPURL | MPURL | text |  |
| company.ceo | corp.ceo | 대표자명 | text | 박찬연 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 수수료입금계좌 | 수수료입금계좌 | 수수료입금계좌 | number | 26,840,000원 |
| 담당부서 | 담당부서 | 담당부서 | text |  |
| 담당자명 | 담당자명 | 담당자명 | text | 신순서 |
| email주소 | email주소 | e-mail주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 신용보증 | 신용보증 | 신용보증 | text |  |
| 기술보증 | 기술보증 | 기술보증 | text |  |
| 지역보증 | 지역보증 | 지역보증 | text |  |
| 대표자생년월일 | 대표자생년월일 | 대표자생년월일 | date | 2025-12-01 |
| FAX번호 | FAX번호 | FAX번호 | phone | 043-783-2775 |
| customer.name | customer.name | 예금주명 | text | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 성명 | text | 박찬연 |
| seal.signer | seal.customer | 성명 | seal | 이민빈 |
| sign.signer | sign.customer | 성명 | signature | 박찬연 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 선택 | 선택 | 선택 | text |  |
| 있어야추심등록및대출실행 | 있어야추심등록및대출실행 | 있어야추심등록및대출실행 | text |  |
| 절차필요 | 절차필요 | 절차필요 | text |  |

### hf104 · 기업구매자금어음 추심의뢰서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.104 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].사업자번호 | 목록[].사업자번호 | 사업자번호 | text | 765-60-22314 |
| 목록[].사업자명 | 목록[].사업자명 | 사업자명 | text | 주식회사 가온산업 |
| 목록[].어음금액 | 목록[].어음금액 | 어음금액 | text | 9,980,000 |
| 목록[].발행일 | 목록[].발행일 | 발행일 | text | 2025.06.29 |
| 목록[].대표품명 | 목록[].대표품명 | 대표품명 | text | 냉동 수산물 |
| 목록[].공급가액 | 목록[].공급가액 | 공급가액 | text | 5,210,000 |
| 목록[].지급은행 | 목록[].지급은행 | 지급은행 | text | 국민은행 |
| 건수 | 건수 | 건수 | number | 1 |
| 금액 | 금액 | 금액 | number | 8,970,000 |
| 수수료 | 수수료 | 수수료 | number | 85,340,000 |
| 비고 | 비고 | 비고 | text | 해당 없음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 인 | text | 박찬연 |
| seal.signer | seal.customer | 인 | seal | 박찬연 |
| sign.signer | sign.customer | 인 | signature | 위나아 |
| signer2.name | signer2.name | 사업자번호 | text | 여욱태 |
| seal.signer2 | seal.signer2 | 사업자번호 | seal | 여옥은 |
| sign.signer2 | sign.signer2 | 사업자번호 | signature | 김지승 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| seal.signer3 | seal.signer3 | 지점 | seal | 강훈영 |
| sign.signer3 | sign.signer3 | 지점 | signature | 손경원 |

### hf105 · 전자채권미결제 확인의뢰서 및 확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.105 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].전자채권번호 | 목록[].전자채권번호 | 전자채권번호 | text | 173-754584-87548 |
| 목록[].발행기업명 | 목록[].발행기업명 | 발행기업명(사업자등록번호) | text | 제일전자 |
| 목록[].금액 | 목록[].금액 | 금액 | number | 40,650,000 |
| 목록[].발행일 | 목록[].발행일 | 발행일 | date | 2026-01-22 |
| 목록[].만기일 | 목록[].만기일 | 만기일 | date | 2026.09.14 |
| 목록[].미결제사유 | 목록[].미결제사유 | 미결제사유 | text | 전세자금 |
| 전자채권지급장소 | 전자채권지급장소 | 전자채권지급장소 | text |  |
| 발행은행지점 | 발행은행지점 | 발행은행지점 | text | 신한은행 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.name | customer.name | 의뢰인 | text | 박찬연 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| seal.signer | seal.signer | 지점 | seal | 김경인 |
| sign.signer | sign.signer | 지점 | signature | 허건호 |

### hf106 · 기업구매자금어음(기업구매자금용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.106 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 발행인 | text | 박찬연 |
| seal.signer | seal.customer | 발행인 | seal | 박찬연 |
| sign.signer | sign.customer | 발행인 | signature | 이욱유 |

### hf107 · 기업구매자금대출 연장신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.107 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 005-785664-39470 |
| 목록[].추심의뢰인 | 목록[].추심의뢰인 | 추심의뢰인 | text | 주식회사 청솔로지스 |
| 목록[].대출금액 | 목록[].대출금액 | 대출금액 | text | 2,310,000 |
| 목록[].대출취급일 | 목록[].대출취급일 | 대출취급일 | text | 2025년 9월 8일 |
| 목록[].당초만기일 | 목록[].당초만기일 | 당초만기일 | text | 2028.06.24 |
| 목록[].기한연장일 | 목록[].기한연장일 | 기한연장일 | text | 2026.10.13 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 최우빈 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| seal.staff.계 | seal.staff.계 | 계 | seal | 검인 |
| sign.staff.계 | sign.staff.계 | 계 | signature | 지영우 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김동민 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김성은 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 황재주 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 윤경린 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 확인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 추현예 |

### hf108 · 외상매출채권 대출신청서(외담대,e-안심팩토링대출 겸용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.108 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].대출실행일 | 목록[].대출실행일 | 대출실행일 | text | 2025.10.27 |
| 목록[].대출신청금액 | 목록[].대출신청금액 | 대출신청금액 | text | 285,940,000원 |
| 목록[].의뢰일 | 목록[].의뢰일 | 의뢰일 | text | 2025년 4월 25일 |
| 목록[].의뢰번호 | 목록[].의뢰번호 | 의뢰번호 | text | 459-639898-31801 |
| 목록[].매출금액 | 목록[].매출금액 | 매출금액 | text | 225,780,000원 |
| 목록[].지급기일 | 목록[].지급기일 | 지급기일 | text | 2028.12.17 |
| 목록[].구매기업사업자번호 | 목록[].구매기업사업자번호 | 구매기업사업자번호 | text | 622-32-65823 |
| 목록[].구매기업명 | 목록[].구매기업명 | 구매기업명 | text | (주)세진산업 |
| 목록[].발행일 | 목록[].발행일 | 발행일 | text | 2025.06.01 |
| 목록[].공급금액 | 목록[].공급금액 | 공급금액 | text | 44,380,000 |
| 목록[].총공급금액 | 목록[].총공급금액 | 총공급금액(세금포함) | text | 119,790,000 |
| 목록[].거래품목 | 목록[].거래품목 | 거래품목 | text | 식품 원재료 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 인 | text | 박찬연 |
| seal.signer | seal.customer | 인 | seal | 박찬연 |
| sign.signer | sign.customer | 인 | signature | 강순준 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 소 | 소 | 소 | text |  |

### hf109 · 전자채권사고신고(취하)서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.109 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 전자채권번호 | 전자채권번호 | 전자채권번호 | text | 989947-4181692 |
| 발행일 | 발행일 | 발행일 | date | 2025년 11월 20일 |
| 판매기업기업명 | 판매기업기업명 | 판매기업기업명 | text | (주)유니온무역 |
| 담보금입금유무 | 담보금입금유무 | 담보금입금유무 | text |  |
| 사고신고사유 | 사고신고사유 | 사고신고(취하)사유 | text | 투자 목적 |
| 금액 | 금액 | 금액 | number | 187,170,000 |
| 만기일 | 만기일 | 만기일 | date | 2025-08-15 |
| 판매기업사업자번호 | 판매기업사업자번호 | 판매기업사업자번호 | biz_no | 264-82-36559 |
| check.사고신고구분 | check.사고신고구분 | 사고신고구분 | checkbox | 신고 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 발행인 | text | 박찬연 |
| seal.signer | seal.customer | 발행인 | seal | 현예지 |
| sign.signer | sign.customer | 발행인 | signature | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |

### hf110 · 전자방식 외상매출채권 발행취소 신청서(외담대,e-안심팩토링용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.110 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].채권번호 | 목록[].채권번호 | 채권번호 | text | 245409-2769119 |
| 목록[].판매기업명 | 목록[].판매기업명 | 판매기업명 | text | (주)가온정밀 |
| 목록[].판매기업사업자번호 | 목록[].판매기업사업자번호 | 판매기업사업자번호 | text | 264-82-36559 |
| 목록[].발행일 | 목록[].발행일 | 발행일 | text | 2026.01.26 |
| 목록[].만기일 | 목록[].만기일 | 만기일 | text | 2027년 11월 6일 |
| 목록[].채권금액 | 목록[].채권금액 | 채권금액 | text | 580,000 |
| 목록[].취소사유 | 목록[].취소사유 | 취소사유 | text | 학자금 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 구매기업주소 | 구매기업주소 | 구매기업:주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.name | corp.name | 업체명 | text | (주)유니온무역 |
| signer.name | corp.ceo | 대표자 | text | 박찬연 |
| seal.signer | seal.corp | 대표자 | seal | 박찬연 |
| sign.signer | sign.customer | 대표자 | signature | 이욱유 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| company.name2 | company.name2 | 업체명 | text | (주)유니온무역 |
| signer2.name | signer2.name | 대표자 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 대표자 | seal | 최우빈 |
| sign.signer2 | sign.signer2 | 대표자 | signature | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김호영 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 차지유 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 황보순지 |

### hf111 · 《개인》위임장(해외체제자 담보대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.111 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| customer.address | customer.address | 현주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 영주권번호 | 영주권번호 | 영주권번호 | text | 817044-5155447 |
| 여권번호 | 여권번호 | 여권번호 | text | M23592908 |
| agent.birth | agent.birth | 생년월일 | date | 1962년 12월 19일 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| 대출금용도 | 대출금용도 | 대출금용도 | text | 투자 목적 |
| 대출기간 | 대출기간 | 대출기간 | text |  |
| customer.name | customer.name | 채무자(대출신청인) | text | 박찬연 |
| 설정최고액 | 설정최고액 | 설정최고액(대출금액의120%기재) | text |  |
| 설정자 | 설정자 | 설정자(소유자) | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.name2 | customer.name2 | 성명(본인) | text | 박찬연 |
| seal.signer | seal.customer | 서명 | seal | 현예지 |
| sign.signer | sign.customer | 서명 | signature | 박찬연 |

### hf112 · [필수]개인(신용)정보 제공동의서(서민맞춤대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.112 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신청일로부터10년까지보유이용 | 신청일로부터10년까지보유이용 | -신청일로부터10년까지보유·이용 | text |  |
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 현예지 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 장민인 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 박영준 |
| 이용목적 | 이용목적 | 이용목적 | text | 전세자금 |

### hf113 · 개인(신용)정보 수집.이용 및 제공 동의서[필수적 동의](적격대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.113 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | ■금융사고조사,분쟁해결,민원처리 | text |  |
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| 제공받는자와동일 | 제공받는자와동일 | -제공받는자와동일 | text |  |
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보조회에동의하십니까 | check.위고유식별정보조회에동의하십니까 | 위고유식별정보조회에동의하십니까? | checkbox | 동의함 |
| check.위개인신용정보조회에동의하십니까 | check.위개인신용정보조회에동의하십니까 | 위개인신용정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| 공사및하나은행 | 공사및하나은행 | 공사및(주)하나은행 | text | 신한은행 |
| 미수채권소멸시까지 | 미수채권소멸시까지 | 미수채권소멸시까지 | text |  |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | family.name | 배우자성명 | text | 강석호 |
| seal.signer2 | seal.signer2 | 배우자성명 | seal | 김순우 |
| sign.signer2 | sign.signer2 | 배우자성명 | signature | 장민인 |
| 재산채무소득의총액납세실적 | 재산채무소득의총액납세실적 | 재산·채무·소득의총액,납세실적 | number | 220,740,000 |
| 신용등급및평점정보 | 신용등급및평점정보 | 신용등급및평점정보 | text |  |
| 일반개인정보2 | 일반개인정보2 | ■일반개인정보 | text |  |
| check.위고유식별정보제공에동의하십니까2 | check.위고유식별정보제공에동의하십니까2 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인신용정보제공에동의하십니까2 | check.위개인신용정보제공에동의하십니까2 | 위개인신용정보제공에동의하십니까? | checkbox | 동의함 |
| 공사및하나은행2 | 공사및하나은행2 | 공사및(주)하나은행 | text | 하나은행 |
| 공공정보등2 | 공공정보등2 | ■공공정보등 | text |  |
| check.위고유식별정보제공에동의하십니까3 | check.위고유식별정보제공에동의하십니까3 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인신용정보제공에동의하십니까3 | check.위개인신용정보제공에동의하십니까3 | 위개인신용정보제공에동의하십니까? | checkbox | 동의함 |
| signer3.name | signer3.name | 본인성명 | text | 박찬연 |
| seal.signer3 | seal.signer3 | 본인성명 | seal | 현예지 |
| sign.signer3 | sign.signer3 | 본인성명 | signature | 박찬연 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer4.name | signer4.name | 배우자성명 | text | 박영준 |
| seal.signer4 | seal.signer4 | 배우자성명 | seal | 이도민 |
| sign.signer4 | sign.signer4 | 배우자성명 | signature | 박영준 |
| 재산채무소득의총액납세실적2 | 재산채무소득의총액납세실적2 | 재산·채무·소득의총액,납세실적 | number | 5,390,000 |
| 신용등급및평점정보2 | 신용등급및평점정보2 | 신용등급및평점정보 | text |  |

### hf114 · 개인(신용)정보 수집.이용 제공 동의서(주택보유수 확인등)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.114 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 본인과배우자의주택보유수확인 | 본인과배우자의주택보유수확인 | -본인과배우자의주택보유수확인 | text |  |
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 일반개인정보2 | 일반개인정보2 | ■■일반개인정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 현예지 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | family.name | 배우자성명 | text | 박영준 |
| seal.signer2 | seal.signer2 | 배우자성명 | seal | 박영준 |
| sign.signer2 | sign.signer2 | 배우자성명 | signature | 강석호 |

### hf115 · [필수] 개인(신용)정보 수집이용, 제공 동의서(핀크생활비대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.115 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | ■금융사고조사,분쟁해결,민원처리 | text |  |
| 핀크 | 핀크 | (주)핀크[WWW.FINNQ.COM] | text |  |
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 이주원 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 김서호 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 김서호 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 위우호 |
| 이용목적 | 이용목적 | 이용목적 | text | 학자금 |

### hf116 · [필수] 개인(신용)정보 수집이용, 제공 동의서(공무원대출)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.116 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 금융거래관계의설정유지이행관리 | 금융거래관계의설정유지이행관리 | ■금융거래관계의설정·유지·이행·관리 | text |  |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | ■금융사고조사,분쟁해결,민원처리 | text |  |
| 공무원연금공단이제공하는대출정보 | 공무원연금공단이제공하는대출정보 | 공무원연금공단이제공하는대출정보 | text |  |
| 공무원연금공단 | 공무원연금공단 | 공무원연금공단 | text |  |
| 신용거래정보2 | 신용거래정보2 | ■신용거래정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | signer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 강순준 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 박영준 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 김서호 |
| 이용목적 | 이용목적 | 이용목적 | text | 해외 이주 |
| customer.name | customer.name | 성명 | text | 박찬연 |

### hf117 · [필수] 개인(신용)정보 수집이용, 제공 동의서(군인생활안정자금)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.117 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 금융거래관계의설정여부판단 | 금융거래관계의설정여부판단 | ■금융거래관계의설정여부판단 | text |  |
| 금융거래관계의설정유지이행관리 | 금융거래관계의설정유지이행관리 | ■금융거래관계의설정·유지·이행·관리 | text |  |
| 국군재정관리단 | 국군재정관리단 | 국군재정관리단 | text |  |
| 신용거래정보2 | 신용거래정보2 | ■신용거래정보 | text |  |
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 이욱유 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 강석호 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 이도민 |

### hf118 · [필수] 개인(신용)정보 수집·이용·제공_동의서[가계여신_금융거래]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.118 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | -금융사고조사,분쟁해결,민원처리 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 현규우 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 김아재 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김진태 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 신채준 |
| 공공정보등2 | 공공정보등2 | ■공공정보등 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 현예지 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 이도민 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 김순우 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 이도민 |
| 성명국내거소신고번호 | 성명국내거소신고번호 | 성명,국내거소신고번호 | text | 146-926653-47954 |
| 있는정보 | 있는정보 | 있는정보 | text |  |

### hf119 · 필수 개인(신용)정보_수집·이용·제공_동의서[하나_사잇돌_중금리대출용]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.119 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | -금융사고조사,분쟁해결,민원처리 | text |  |
| 성명주소전화번호직장정보 | 성명주소전화번호직장정보 | 성명,주소,전화번호,직장정보 | phone | 043-783-2775 |
| 고유식별정보 | 고유식별정보 | ■고유식별정보 | text |  |
| 신용거래정보2 | 신용거래정보2 | ■신용거래정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 이욱유 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 이도민 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 강석호 |

### hf120 · 필수 개인(신용)정보수집·이용및제공동의서(하나원클릭모기지,원클릭전세론,e금리고정형적격)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.120 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | -금융사고조사,분쟁해결,민원처리 | text |  |
| 성명생년월일주소전화번호 | 성명생년월일주소전화번호 | 성명,생년월일,주소,전화번호 | date | 2025.10.22 |
| 공공정보등2 | 공공정보등2 | ■공공정보등 | text |  |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 현예지 |
| sign.signer | sign.customer | 본인성명 | signature | 강순준 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 박영준 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 이도민 |
| 성명생년월일주소전화번호2 | 성명생년월일주소전화번호2 | 성명,생년월일,주소,전화번호 | date | 2025.01.02 |
| 공공정보등3 | 공공정보등3 | ■공공정보등 | text |  |
| check.위개인정보수집이용에동의하십니까2 | check.위개인정보수집이용에동의하십니까2 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 성명생년월일주소전화번호3 | 성명생년월일주소전화번호3 | 성명,생년월일,주소,전화번호 | date | 2025년 2월 19일 |
| 공공정보등4 | 공공정보등4 | ■공공정보등 | text |  |
| check.위개인정보제공에동의하십니까2 | check.위개인정보제공에동의하십니까2 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| signer3.name | signer3.name | 본인성명 | text | 박찬연 |
| seal.signer3 | seal.signer3 | 본인성명 | seal | 현예지 |
| sign.signer3 | sign.signer3 | 본인성명 | signature | 박찬연 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer4.name | signer4.name | 대리인성명 | text | 강석호 |
| seal.signer4 | seal.signer4 | 대리인성명 | seal | 이도민 |
| sign.signer4 | sign.signer4 | 대리인성명 | signature | 강석호 |
| 성명생년월일주소전화번호4 | 성명생년월일주소전화번호4 | 성명,생년월일,주소,전화번호 | date | 2025.02.27 |

### hf121 · [필수] 개인(신용)정보 제3차 제공 동의서(우량주택전세론,군간부전세자금대출)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.121 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 서울보증보험 | 서울보증보험 | 서울보증보험(주)(www.sgic.co.kr) | text |  |
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 전영경 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 강석호 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 강석호 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 이도민 |
| 이용목적 | 이용목적 | 이용목적 | text | 계좌 정리 |

### hf122 · [필수] 개인(신용)정보 수집·이용 및 제공 동의서(전세자금대출 권리보험가입용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.122 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | ■금융사고조사,분쟁해결,민원처리 | text |  |
| 정보질권통지업무상필요한정보 | 정보질권통지업무상필요한정보 | 정보,질권통지업무상필요한정보 | text |  |
| 개인대출현황대출한도금액 | 개인대출현황대출한도금액 | 개인대출현황(본건),대출한도금액 | number | 49,130,000원 |
| 신용거래정보2 | 신용거래정보2 | ■신용거래정보 | text |  |
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 현예지 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 박영준 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 강석호 |
| 제공목적 | 제공목적 | 제공목적 | text | 본인 요청 |
| 개인대출현황대출한도금액2 | 개인대출현황대출한도금액2 | 개인대출현황(본건),대출한도금액 | number | 100,000 |

### hf123 · [필수] 개인(신용)정보 수집·이용 동의서 [전세자금대출-주택금융보증서용]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.123 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용능력정보 | 신용능력정보 | ■신용능력정보 | text |  |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 현예지 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 김승성 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 박영준 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | -금융사고조사,분쟁해결,민원처리 | text |  |

### hf124 · [필수] 개인(신용)정보 처리 동의서(전세자금대출 권리보험가입용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.124 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 체결유지관리목적 | 체결유지관리목적 | 체결·유지·관리목적 | text | 전세자금 |
| 보험계약관련분쟁대응민원처리 | 보험계약관련분쟁대응민원처리 | 보험계약관련분쟁대응,민원처리 | text |  |
| 질권통지업무수행 | 질권통지업무수행 | 질권통지업무수행 | text |  |
| 정보등기타보험계약운영상필요정보 | 정보등기타보험계약운영상필요정보 | 정보등기타보험계약운영상필요정보 | text |  |
| 신용거래정보2 | 신용거래정보2 | ■신용거래정보 | text |  |
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 강순준 |
| date | date | 작성일 | date | 2026년 1월 31일 |

### hf125 · [필수] 개인(신용)정보 수집·이용 및 제공동의서[군간부전세자금대출기본),군간부월세자금대출]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.125 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 금융거래관계의설정여부판단 | 금융거래관계의설정여부판단 | ■금융거래관계의설정여부판단 | text |  |
| 금융거래관계의설정유지이행관리 | 금융거래관계의설정유지이행관리 | ■금융거래관계의설정·유지·이행·관리 | text |  |
| 제공하는재직정보 | 제공하는재직정보 | 제공하는재직정보 | text |  |
| 대출정보퇴직정보 | 대출정보퇴직정보 | 대출정보,퇴직정보 | text |  |
| 국방부 | 국방부 | 국방부 | text |  |
| 신용거래정보2 | 신용거래정보2 | ■신용거래정보 | text |  |
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 현예지 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 박영준 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 강석호 |
| 제공목적 | 제공목적 | 제공목적 | text | 주택구입 |

### hf126 · [필수] 상품별 개인(신용)정보 수집·이용·제공 동의서[목돈안드는 행복전세,목돈 안다는 드림전세(집주인담보대출)용]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.126 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | ■금융사고조사,분쟁해결,민원처리 | text |  |
| 성명 | 성명 | ■성명 | text |  |
| 개인식별정보외에고객이제공한정보 | 개인식별정보외에고객이제공한정보 | ■개인식별정보외에고객이제공한정보 | text |  |
| 국토교통부 | 국토교통부 | 국토교통부 | text |  |
| 일반개인정보2 | 일반개인정보2 | ■일반개인정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 성명 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 성명 | seal | 강순준 |
| sign.signer2 | sign.signer2 | 성명 | signature | 박찬연 |
| signer3.name | signer3.name | 성명 | text | 박찬연 |
| seal.signer3 | seal.signer3 | 성명 | seal | 현예지 |
| sign.signer3 | sign.signer3 | 성명 | signature | 박찬연 |
| signer4.name | signer4.name | 성명 | text | 박찬연 |
| seal.signer4 | seal.signer4 | 성명 | seal | 이욱유 |
| sign.signer4 | sign.signer4 | 성명 | signature | 박찬연 |
| 이용목적 | 이용목적 | 이용목적 | text | 의료비 |
| 성명2 | 성명2 | ■성명 | text |  |
| 개인식별정보외에고객이제공한정보2 | 개인식별정보외에고객이제공한정보2 | ■개인식별정보외에고객이제공한정보 | text |  |

### hf127 · 상품별 필수 개인(신용)정보 제공동의서(하나V-Plus대출)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.127 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용보증기금 | 신용보증기금 | 신용보증기금 | text |  |
| 신용도판단정보 | 신용도판단정보 | ■신용도판단정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 강순준 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 강석호 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 장민인 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 김순우 |
| 이용목적 | 이용목적 | 이용목적 | text | 타행 이체 |

### hf128 · 필수 개인(신용)정보 수집, 이용 및 제공 동의서(소호여신)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.128 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | -금융사고조사,분쟁해결,민원처리 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 검인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 이철정 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 진연호 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 위욱우 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 표현인 |
| 공공정보등2 | 공공정보등2 | ■공공정보등 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 이주원 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 이도민 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 장민인 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 이도민 |
| 이용목적 | 이용목적 | 이용목적 | text | 급여 수령 |

### hf129 · 필수 개인(신용)정보 수집, 이용 및 제공 동의서(법인여신)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.129 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | -금융사고조사,분쟁해결,민원처리 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 반건태 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 이영수 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 최선진 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 검인 |
| 공공정보등2 | 공공정보등2 | ■공공정보등 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 이민빈 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 이도민 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 이도민 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 김수연 |

### hf130 · 기업가치 및 기업정보 제공활용 동의서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.130 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| date | date | 작성일 | date | 2026년 1월 31일 |
| company.name | corp.name | 기업체명 | text | (주)유니온무역 |
| signer.name | corp.ceo | 대표자 | text | 박찬연 |
| seal.signer | seal.corp | 대표자 | seal | 강순준 |
| sign.signer | sign.customer | 대표자 | signature | 박찬연 |

### hf131 · 전세자금대출 이용 확약서(서울보증보험증권 담보 전세자금대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.131 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.birth | customer.birth | 생년월일 | date | 900210 |
| signer.name | customer.name | 명 | text | 박찬연 |
| seal.signer | seal.customer | 명 | seal | 최우빈 |
| sign.signer | sign.customer | 명 | signature | 박찬연 |

### hf132 · 다주택처분확약서(서울보증보험)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.132 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 본인 | text | 박찬연 |
| 대출계좌번호 | 대출계좌번호 | 대출계좌번호 | text | 403-930666-16188 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.birth | customer.birth | 생년월일 | date | 1990-02-10 |
| signer.name | signer.name | 명 | text | 박찬연 |
| seal.signer | seal.customer | 명 | seal | 이욱유 |
| sign.signer | sign.customer | 명 | signature | 박찬연 |

### hf133 · 금융거래 정보제공 동의서(연대보증 면제 신용보증서 담보대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.133 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.제공받는자 | check.제공받는자 | 제공받는자 | checkbox | 기술보증기금 |
| 보증서담보대출입금전용계좌번호 | 보증서담보대출입금전용계좌번호 | ▦보증서담보대출입금전용계좌번호 | text | 마바42199239 |
| check.금융거래정보제공동의여부 | check.금융거래정보제공동의여부 | 금융거래정보제공동의여부 | checkbox | 보기2 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | corp.name | 법인명(채무자) | text | (주)유니온무역 |
| seal.signer | seal.corp | 법인명(채무자) | seal | (주)유니온무역 |
| sign.signer | sign.customer | 법인명(채무자) | signature | (주)스마트에프앤비 |
| 연대보증제도폐지에따른사후관리강화 | 연대보증제도폐지에따른사후관리강화 | ▦연대보증제도폐지에따른사후관리강화 | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김원지 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김승은 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 선우훈서 |

### hf134 · 개인(신용)정보 수집.이용 동의서(매도인,무상거주인등 제3자용)(적격대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.134 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.해당되는 | check.해당되는 | ■해당되는 | checkbox | 에 반드시 체크 |
| check.수집ᆞ이용동의여부 | check.수집ᆞ이용동의여부 | 수집ᆞ이용동의여부 | checkbox | 보기2 |
| check.고유식별정보동의여부 | check.고유식별정보동의여부 | 고유식별정보동의여부 | checkbox | 보기2 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인 | text | 박찬연 |
| seal.signer | seal.customer | 본인 | seal | 박찬연 |
| sign.signer | sign.customer | 본인 | signature | 이욱유 |
| signer2.name | signer2.name | 본인 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 본인 | seal | 이민빈 |
| sign.signer2 | sign.signer2 | 본인 | signature | 박찬연 |
| signer3.name | signer3.name | 본인 | text | 박찬연 |
| seal.signer3 | seal.signer3 | 본인 | seal | 박찬연 |
| sign.signer3 | sign.signer3 | 본인 | signature | 현예지 |
| signer4.name | signer4.name | 본인 | text | 박찬연 |
| seal.signer4 | seal.signer4 | 본인 | seal | 박찬연 |
| sign.signer4 | sign.signer4 | 본인 | signature | 최우빈 |
| 개인식별정보 | 개인식별정보 | ■개인식별정보 | text |  |

### hf135 · 동의서(대출비용지급용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.135 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| date | date | 작성일 | date | 2026년 1월 31일 |
| check.한국주택금융공사보증료 | check.한국주택금융공사보증료 | 한국주택금융공사보증료【출금된보증료는한국주택금융공사로납부됩니다.】 | checkbox | 한국주택금융공사 보증료【출금된 보증료는 한국주택금융공사로 납부됩니다.】 |
| check.주택도시보증공사보증료 | check.주택도시보증공사보증료 | 주택도시보증공사보증료【출금된보증료는주택도시보증공사로납부됩니다.】 | checkbox | 주택도시보증공사 보증료【출금된 보증료는 주택도시보증공사로 납부됩니다.】 |
| check.수입인지대금출금된수입 | check.수입인지대금출금된수입 | 수입인지대금【출금된수입인지대금은수입인지세금으로납부됩니다.】 | checkbox | 수입인지대금【출금된 수입인지대금은 수입인지세금으로 납부됩니다.】 |
| check.국민주택채권매입비용 | check.국민주택채권매입비용 | 국민주택채권매입(할인)비용 | checkbox | 국민주택채권 매입(할인) 비용 |
| check.기타 | check.기타 | 기타( | checkbox | 기타( |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |

### hf136 · 《기업》차입신청서(한도내 개별/분할실행용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.136 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 신규 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 여신과목 | 여신과목 | 여신과목 | text | 무역금융 |
| 신청금액 | 신청금액 | 신청금액 | number | 44,360,000 |
| 기한 | 기한 | 기한 | date | 2025년 7월 11일 |
| 금리 | 금리 | 금리 | number | 30 |
| 자금용도 | 자금용도 | 자금용도 | text | 중고차 구입 대금 |
| 승인금액 | 승인금액 | 승인금액(A) | number | 3,920,000원 |
| 여신잔액 | 여신잔액 | 여신잔액(B) | number | 880,000 |
| 본건신청액 | 본건신청액 | 본건신청액(C) | text |  |
| 본건취급후 | 본건취급후 | 본건취급후 | text |  |
| 잔액 | 잔액 | 잔액(A-B-C) | number | 8,580,000 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 조건정 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김민희 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 함성은 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 김수영 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 김찬도 |

### hf137 · 대출금 분할실행 신청서(에듀큐론용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.137 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 총대출한도 | 총대출한도 | 총대출한도(A) | number | 9,310,000 |
| 기사용한도 | 기사용한도 | 기사용한도(B) | number | 750,000 |
| 분할실행신청액 | 분할실행신청액 | 분할실행신청액(C) | text |  |
| 미사용한도 | 미사용한도 | 미사용한도(A-B-C) | number | 97,010,000 |
| 비고 | 비고 | 비고 | text | 해당 없음 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| 분할실행신청액2 | 분할실행신청액2 | ◦분할실행신청액 | text |  |
| signer.name | customer.name | 채무자 | text | 박찬연 |
| seal.signer | seal.customer | 채무자 | seal | 이욱유 |
| sign.signer | sign.customer | 채무자 | signature | 강순준 |

### hf138 · 대출금 수령위임동의서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.138 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 용도 | 용도 | 용도 | text | 사업자금으로 일억원 필요 |
| 수령금액 | 수령금액 | 수령금액 | number | 410,000 |
| customer.name | customer.name | 예금주 | text | 박찬연 |
| check.차주와의관계 | check.차주와의관계 | 차주와의관계 | checkbox | 차주를 대신하여 당타행 대출의 상환을 위임받은 자 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 수령위임인 | text | 박찬연 |
| seal.signer | seal.customer | 수령위임인 | seal | 이욱유 |
| sign.signer | sign.customer | 수령위임인 | signature | 박찬연 |
| signer2.name | agent.name | 수령위임인의대리인 | text | 박영준 |
| seal.signer2 | seal.agent | 수령위임인의대리인 | seal | 강석호 |
| sign.signer2 | sign.agent | 수령위임인의대리인 | signature | 위우호 |

### hf139 · 《기업》 지급보증거래 신청서(서면.전자 지급보증 겸용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.139 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 보증금액 | 보증금액 | 보증금액 | number | 46,670,000 |
| 피보증채무의종류 | 피보증채무의종류 | 피보증채무의종류 | text |  |
| 피보증채무의종류2 | 피보증채무의종류2 | 피보증채무의종류 | text |  |
| seal.signer | seal.signer | 인감(서명)대조 | seal | 이욱유 |
| sign.signer | sign.signer | 인감(서명)대조 | signature | 강순준 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | customer.name | 본인 | text | 박찬연 |
| seal.signer2 | seal.customer | 본인 | seal | 박찬연 |
| sign.signer2 | sign.customer | 본인 | signature | 이욱유 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 상호 | 상호 | •상호(성명) | text | (주)세진화학 |
| 사업자번호 | 사업자번호 | •사업자번호 | biz_no | 715-51-28572 |
| 주소 | 주소 | •주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 전화번호및팩스번호 | 전화번호및팩스번호 | •전화번호및팩스번호(또는E-Mail) | phone | 043-783-2775 |
| 계좌번호 | 계좌번호 | •계좌번호 | text | 208-371607-58772 |
| 특정채무 | 특정채무 | 특정채무 | text |  |
| 보증 | 보증 | 보증 | text |  |
| 근보증 | 근보증 | 근보증 | text |  |
| 예금주 | 예금주 | •예금주 | text |  |

### hf140 · 매출채권 잔액 확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.140 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 판매기업에대한정보 | 판매기업에대한정보 | 판매기업에대한정보 | text |  |
| 본인에대한정보 | 본인에대한정보 | 본인(구매기업)에대한정보 | text |  |
| 판매기업명 | 판매기업명 | 판매기업명 | text | 유니온상사 |
| 판매기업결제계좌 | 판매기업결제계좌 | 판매기업결제계좌 | text | 596-676769-83857 |
| employer.name | employer.name | 회사명 | text | 주식회사 태평양무역 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| 담당부서 | 담당부서 | 담당부서 | text |  |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 입금은행명 | 입금은행명 | 입금은행명 | text | 농협은행 |
| company.biz_no2 | company.biz_no2 | 사업자등록번호 | biz_no | 264-82-36559 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| 목록[].일련번호 | 목록[].일련번호 | 일련번호 | text | 135-572662-43096 |
| 목록[].매출채권금액 | 목록[].매출채권금액 | 매출채권금액 | text | 980,000 |
| 목록[].발생일 | 목록[].발생일 | 발생일 | text | 2025-02-13 |
| 목록[].지급기일 | 목록[].지급기일 | 지급기일 | text | 2029.01.06 |
| 목록[].다른권리존재여부 | 목록[].다른권리존재여부 | 다른권리존재여부 | text |  |
| 목록[].특기사항 | 목록[].특기사항 | 특기사항 | text | 해당 없음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 물품공급계약내용 | 물품공급계약내용 | 물품공급계약내용[ | text | 기계 부품 |
| 계약일자 | 계약일자 | 계약일자[..] | date | 2026-01-10 |
| 지급이확정된미지급매출채권내용 | 지급이확정된미지급매출채권내용 | 지급이확정된미지급매출채권내용 | text | 해당 없음 |

### hf141 · 매출채권 잔액 확인서(사전확인용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.141 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 판매기업에대한정보 | 판매기업에대한정보 | 판매기업에대한정보 | text |  |
| 본인에대한정보 | 본인에대한정보 | 본인(구매기업)에대한정보 | text |  |
| 판매기업명 | 판매기업명 | 판매기업명 | text | (주)유니온무역 |
| 판매기업결제계좌 | 판매기업결제계좌 | 판매기업결제계좌 | text | 718-622426-99921 |
| employer.name | employer.name | 회사명 | text | 주식회사 태평양무역 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| 담당부서 | 담당부서 | 담당부서 | text |  |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 입금은행명 | 입금은행명 | 입금은행명 | text | 국민은행 |
| company.biz_no2 | company.biz_no2 | 사업자등록번호 | biz_no | 264-82-36559 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| 목록[].일련번호 | 목록[].일련번호 | 일련번호 | text | 7431-3256 |
| 목록[].매출채권금액 | 목록[].매출채권금액 | 매출채권금액 | text | 24,240,000 |
| 목록[].발생일 | 목록[].발생일 | 발생(예정)일 | text | 2025년 1월 31일 |
| 목록[].지급기일 | 목록[].지급기일 | 지급기일 | text | 2027-03-12 |
| 목록[].매출채권확정여부 | 목록[].매출채권확정여부 | 매출채권확정여부 | text | 48,230,000 |
| 목록[].다른권리존재여부 | 목록[].다른권리존재여부 | 다른권리존재여부 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 물품공급계약내용 | 물품공급계약내용 | 물품공급계약내용[ | text | LED 모듈 |
| 계약일자 | 계약일자 | 계약일자[..] | date | 2025년 3월 22일 |
| 미지급매출채권잔액 | 미지급매출채권잔액 | 미지급매출채권잔액 | number | 70,820,000 |

### hf142 · 매출채권설정등기통지서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.142 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].일련번호 | 목록[].일련번호 | 일련번호 | text | 2021-3735 |
| 목록[].발생일 | 목록[].발생일 | 발생일 | date | 2025년 7월 7일 |
| 목록[].만기일 | 목록[].만기일 | 만기일 | date | 2027.08.13 |
| 목록[].채권금액 | 목록[].채권금액 | 채권금액 | number | 18,450,000원 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| 가계약내용 | 가계약내용 | 가.계약내용 | text | 해당 없음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 은행 | text | 김민빈 |
| seal.signer | seal.signer | 은행 | seal | 서훈정 |
| sign.signer | sign.signer | 은행 | signature | 김민빈 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 절취선 | 절취선 | 절취선 | text |  |
| 절취선2 | 절취선2 | 절취선 | text |  |

### hf144 · 동산담보 제공 예정내역서(개별동산용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.144 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.address | corp.address | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| 보관장소명 | 보관장소명 | 보관장소명(주) | text |  |
| 목록[].제품명 | 목록[].제품명 | 제품명 | text | 플라스틱 원료 |
| 목록[].식별번호 | 목록[].식별번호 | 식별번호(주) | text | 801-156779-86345 |
| 목록[].모델명 | 목록[].모델명 | 모델명 | text | 전자부품 |
| 목록[].제조사 | 목록[].제조사 | 제조사 | text | 플라스틱 원료 |
| 목록[].제조년월 | 목록[].제조년월 | 제조년월 | text |  |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 채무자(담보제공자) | text | 박찬연 |
| seal.signer | seal.customer | 채무자(담보제공자) | seal | 강순준 |
| sign.signer | sign.customer | 채무자(담보제공자) | signature | 박찬연 |

### hf145 · 동산담보 제공 예정내역서(집합동산용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.145 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.address | corp.address | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| 보관장소명 | 보관장소명 | 보관장소명(주) | text |  |
| 목록[].동산의명칭 | 목록[].동산의명칭 | 동산의명칭 | text | 대성물산 |
| 목록[].규격 | 목록[].규격 | 규격 | text | 기계 부품 |
| 목록[].수량 | 목록[].수량 | 수량(주1) | text | 1 |
| 목록[].수량단위 | 목록[].수량단위 | 수량단위 | text | 2 |
| 목록[].단가 | 목록[].단가 | 단가(주2) | text | 1,180,000 |
| 목록[].제조사 | 목록[].제조사 | 제조사 | text | 전자부품 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 채무자(담보제공자) | text | 박찬연 |
| seal.signer | seal.customer | 채무자(담보제공자) | seal | 박찬연 |
| sign.signer | sign.customer | 채무자(담보제공자) | signature | 현예지 |

### hf149 · 《기업》금융거래확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.149 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].종별 | 목록[].종별 | 종별 | text | 하나 TDF 2040 |
| 목록[].용도 | 목록[].용도 | 용도 | text | 의료비 |
| 목록[].이율 | 목록[].이율 | 이율 | text | 25 |
| 목록[].일자 | 목록[].일자 | 일자 | text | 2025.04.11 |
| 목록[].금액 | 목록[].금액 | 금액 | text | 74,930,000 |
| 목록[].잔액 | 목록[].잔액 | 잔액 | text | 147,790,000 |
| 목록[].대출기한 | 목록[].대출기한 | 대출기한 | text | 2028.02.11 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| 종류 | 종류 | 종류 | text | 하나 적금 |
| 선정일자 | 선정일자 | 선정일자 | date | 2025.10.01 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 어음 | 어음 | 어음 | text |  |
| 수표 | 수표 | 수표 | text |  |
| 목록[].소재지 | 목록[].소재지 | 소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 목록[].소유자 | 목록[].소유자 | 소유자 | text |  |
| 목록[].채무자와의관계 | 목록[].채무자와의관계 | 채무자와의관계 | text |  |
| 목록[].종류 | 목록[].종류 | 종류 | text | 하나 정기예금 |
| 목록[].수량 | 목록[].수량 | 수량 | text | 6 |
| 목록[].감정가격 | 목록[].감정가격 | 감정가격 | text |  |
| 목록[].감정일자 | 목록[].감정일자 | 감정일자 | text | 2025-04-30 |
| 목록[].설정내용 | 목록[].설정내용 | 설정내용(순위,금액) | text | 해당 없음 |
| 대출종별 | 대출종별 | 대출종별 | text |  |
| 연체발생일 | 연체발생일 | 연체발생일 | date | 2025.01.27 |
| 연체발생일2 | 연체발생일2 | 연체발생일 | date | 2025.09.04 |
| 원금 | 원금 | 원금 | number | 710,000 |
| 이자 | 이자 | 이자 | number | 83,650,000 |
| 연체정리일 | 연체정리일 | 연체정리일 | date | 2026.01.12 |
| 연체일수 | 연체일수 | 연체일수 | text |  |
| seal.signer | seal.signer | (부)점장 | seal | 김예은 |
| sign.signer | sign.signer | (부)점장 | signature | 최수현 |
| signer2.name | corp.ceo | 대표자명 | text | 박찬연 |
| seal.signer2 | seal.corp | 대표자명 | seal | 박찬연 |
| sign.signer2 | sign.customer | 대표자명 | signature | 현예지 |
| company.name | corp.name | 기업체명 | text | (주)유니온무역 |

### hf150 · 《기업》근저당권유용합의서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.150 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 근저당권설정내역 | 근저당권설정내역 | 근저당권설정내역 | text |  |
| 채권최고액 | 채권최고액 | 채권최고액 | text |  |
| customer.name | customer.name | 채무자 | text | 박찬연 |
| 근저당권설정자 | 근저당권설정자 | 근저당권설정자 | text |  |
| seal.signer | seal.customer | 인 | seal | 현예지 |
| sign.signer | sign.customer | 인 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 채무자 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 채무자 | seal | 이민빈 |
| sign.signer2 | sign.signer2 | 채무자 | signature | 박찬연 |
| signer3.name | signer3.name | 후순위근저당권자 | text | 박용유 |
| seal.signer3 | seal.signer3 | 후순위근저당권자 | seal | 박용유 |
| sign.signer3 | sign.signer3 | 후순위근저당권자 | signature | 박욱호 |
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer4.name | signer4.name | 근저당권자 | text | 박채호 |
| seal.signer4 | seal.signer4 | 근저당권자 | seal | 김건정 |
| sign.signer4 | sign.signer4 | 근저당권자 | signature | 박채호 |
| signer5.name | signer5.name | 주택임차인 | text | 정희율 |
| seal.signer5 | seal.signer5 | 주택임차인 | seal | 정희율 |
| sign.signer5 | sign.signer5 | 주택임차인 | signature | 김규재 |
| customer.birth2 | customer.birth2 | 생년월일 | date | 1990.02.10 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer6.name | related.name | 근저당권설정자 | text | 신욱수 |
| seal.signer6 | seal.related | 근저당권설정자 | seal | 신욱수 |
| sign.signer6 | sign.related | 근저당권설정자 | signature | 위채유 |
| customer.birth3 | customer.birth3 | 생년월일 | date | 1990.02.10 |
| customer.address3 | customer.address3 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 검인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 이나은 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 곽찬윤 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 마지재 |
| seal.staff.대리 | seal.staff.대리 | 대리 | seal | 조혁찬 |
| sign.staff.대리 | sign.staff.대리 | 대리 | signature | 손하승 |
| seal.staff.차장 | seal.staff.차장 | 차장 | seal | 하훈원 |
| sign.staff.차장 | sign.staff.차장 | 차장 | signature | 확인 |
| seal.staff.점장 | seal.staff.점장 | 점장 | seal | 명하아 |
| sign.staff.점장 | sign.staff.점장 | 점장 | signature | 양환도 |

### hf151 · 《기업》무역어음인수·할인신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.151 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 어음번호 | 어음번호 | 어음번호 | text | 사다59385697 |
| 년 | 년 | 년 | text |  |
| 목록[].월 | 목록[].월 | 월 | text |  |
| 목록[].일 | 목록[].일 | 일 | text |  |
| 년2 | 년2 | 년 | text |  |
| 년3 | 년3 | 년 | number | 100 |
| 일 | 일 | 일 | text |  |
| 년4 | 년4 | 년 | text |  |
| 지급기일 | 지급기일 | 지급기일 | date | 2030년 1월 3일 |
| 비 | 비 | 비 | text |  |
| 선적기일할인료율 | 선적기일할인료율 | 선적기일할인료율 | number | 20 |
| 주소본인 | 주소본인 | 주소:본인 | text | 서울특별시 서초구 방배로 524, 110동 501호 |

### hf152 · 《기업》연대보증인(교체·면제)증서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.152 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].약정일자 | 목록[].약정일자 | 약정일자 | date | 2025-10-07 |
| 목록[].거래약정서류명 | 목록[].거래약정서류명 | 거래약정서류명(또는어음채무내용) | text |  |
| 목록[].채무한도액 | 목록[].채무한도액 | 채무한도액 | text | 76,090,000 |
| 목록[].보증종류 | 목록[].보증종류 | 보증종류 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 구연대보증인의보증채무내용 | 구연대보증인의보증채무내용 | ○구연대보증인의보증채무내용 | text | 해당 없음 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 최혜은 |
| seal.staff.대리 | seal.staff.대리 | 대리 | seal | 검인 |
| sign.staff.대리 | sign.staff.대리 | 대리 | signature | 확인 |
| seal.staff.차장 | seal.staff.차장 | 차장 | seal | 여호태 |
| sign.staff.차장 | sign.staff.차장 | 차장 | signature | 이미호 |

### hf153 · 《기업》질권설정등록청구서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.153 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].종류 | 목록[].종류 | 종류 | text | 하나 단기채 펀드 |
| 목록[].기호 | 목록[].기호 | 기호 | text |  |
| 목록[].번호 | 목록[].번호 | 번호 | text | 9150-1354 |
| 목록[].액면금액 | 목록[].액면금액 | 액면금액 | text | 340,000 |
| 목록[].매수 | 목록[].매수 | 매수 | text | 12 |
| 목록[].총액 | 목록[].총액 | 총액 | text | 32,610,000원 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| check.주권 | check.주권 | 주권 | checkbox | 주 권 |
| check.사채권 | check.사채권 | 사채권 | checkbox | 사채권 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| check.증권 | check.증권 | 증권 | checkbox | 증 권 |
| check.예금 | check.예금 | 예금 | checkbox | 예 금 |
| signer.name | customer.name | 명 | text | 박찬연 |
| seal.signer | seal.customer | 명 | seal | 박찬연 |
| sign.signer | sign.customer | 명 | signature | 강순준 |

### hf154 · 차입신청서(무역금융용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.154 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| related_list[].name | related_list[].name | 성명 | text | 박찬연 |
| loan.basis_list[].line | loan.basis_list[].line | 수량 | text | 해당 없음 |
| bank.opinion_list[].line | bank.opinion_list[].line | 수량 | text | 해당 없음 |
| loan.amount | loan.amount | 금액 | amount | 14,410,000원 |
| check.과목 | check.과목 | 과목 | checkbox | 보기4 |
| loan.interest_timing | loan.interest_timing | 이자지급시기 | text | 3개월마다 후취 |
| related_list[].age | related_list[].age | 연령 | number | 56 |
| trade.lc_no | trade.lc_no | L/C(계약서)No | text | 459-810568-36030 |
| trade.amount | trade.amount | 금액 | amount | CNY 124,400 |
| trade.goods | trade.goods | 품목 | text | 포장재 |
| trade.quantity | trade.quantity | 수량 | number | 1 |
| related_list[].job | related_list[].job | 직업및직위 | text | 회사원/대표이사 |
| related_list[].relation | related_list[].relation | 차주와의관계 | text | 이사 |
| related_list[].monthly_income | related_list[].monthly_income | 월평균수입 | amount | 18,150,000 |
| related_list[].net_assets | related_list[].net_assets | 실자산 | amount | 44,260,000원 |
| trade.shipment_date | trade.shipment_date | 선적(납품)기일 | date | 2026-11-29 |
| trade.incoterms | trade.incoterms | 가격조건 | text | CIF |
| trade.payment_terms | trade.payment_terms | 결제조건 | text | L/C AT SIGHT |
| trade.special_terms | trade.special_terms | 기타특수조건 | text | 해당 없음 |
| check.자금용도 | check.자금용도 | 자금용도 | checkbox | 완제품구매자금 |
| loan.due_date | loan.due_date | 기한 | date | 2025년 5월 23일 |
| loan.repay | loan.repay | 상환자원및방법 | text | 혼합상환 |
| related_list[].address | related_list[].address | 주소(전화번호) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| bank.approval_date | bank.approval_date | 승인일자 | date | 2025.02.01 |
| bank.approval_expiry | bank.approval_expiry | 승인기한 | date | 2025년 12월 5일 |
| bank.proper_limit_usd | bank.proper_limit_usd | U$ | amount | 55,370,000원 |
| bank.used_usd | bank.used_usd | U$ | amount | 12,010,000 |
| bank.limit_remaining_usd | bank.limit_remaining_usd | U$ | amount | 1,600,000원 |
| trade.expiry_date | trade.expiry_date | 유효기일 | date | 2026.06.29 |
| date | date | 작성일(년월일) | date | 2026년 01월 31일 |
| company.address | company.address | 신청인주소 | text | 서울특별시 중구 다산로 361, 6층 |
| company.name | company.name | 신청인상호 | text | (주)유니온무역 |
| company.phone | company.phone | 신청인전화번호 | phone | 02-9508-6789 |
| company.ceo | company.ceo | 신청인대표자 | text | 박찬연 |
| loan.rate | loan.rate | 이자율연이율(%) | number | 5.52 |
| loan.overdue_rate | loan.overdue_rate | 지연배상금이율연(%) | number | 7.27 |
| bank.trade_limit | bank.trade_limit | 무역금융승인한도(천원) | amount | 3,440,000원 |
| bank.trade_used | bank.trade_used | 사용액(본건포함)(천원) | number | 880,000 |
| bank.trade_remaining | bank.trade_remaining | 여유액(본건취급후)(천원) | number | 5,960,000 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김서은 |
| seal.staff.팀장 | seal.staff.팀장 | 팀장 | seal | 검인 |
| sign.staff.팀장 | sign.staff.팀장 | 팀장 | signature | 이경도 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 배건성 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 김건윤 |
| credit.trade.production | credit.trade.production | 생산 | number | 950,000 |
| credit.trade.raw_import | credit.trade.raw_import | 원자재수입 | number | 7,320,000원 |
| credit.trade.raw_purchase | credit.trade.raw_purchase | 원자재구매 | number | 90,000 |
| credit.trade.product_purchase | credit.trade.product_purchase | 완제품구매 | number | 2,750,000 |
| credit.trade.comprehensive | credit.trade.comprehensive | 포괄금융 | number | 78,390,000 |
| credit.trade.agri_export | credit.trade.agri_export | 농수산물수출준비 | number | 2,980,000 |
| credit.trade.local_lc | credit.trade.local_lc | 내국신용장발행 | number | 135,760,000 |
| credit.trade.import_lc | credit.trade.import_lc | 수입신용장발행 | number | 290,000원 |
| 무역금융신청건포함명세_목록[].당행 | 무역금융신청건포함명세_목록[].당행 | 당행 | text |  |
| 계 | 계 | 계 | text |  |
| credit.working.trade_finance | credit.working.trade_finance | 무역금융 | number | 420,000 |
| credit.working.general | credit.working.general | 일반자금대출 | number | 69,540,000 |
| credit.working.overdraft | credit.working.overdraft | 당좌대출 | number | 6,820,000 |
| credit.working.commercial_bill | credit.working.commercial_bill | 상업어음 | number | 900,000원 |
| 운전자금_목록[].당행 | 운전자금_목록[].당행 | 당행 | text |  |
| credit.facility.general | credit.facility.general | 일반자금대출 | number | 19,860,000원 |
| credit.facility.fx_loan | credit.facility.fx_loan | 외화대출 | amount | JPY 134,200 |
| 시설자금_목록[].당행 | 시설자금_목록[].당행 | 당행 | text |  |
| credit.guarantee.trade | credit.guarantee.trade | 무역금융관계 | number | 5,950,000 |
| credit.guarantee.other_krw | credit.guarantee.other_krw | 기타원화표시 | amount | 6,170,000 |
| credit.guarantee.other_fx | credit.guarantee.other_fx | 기타외화표시 | amount | GBP 33,600 |
| 당행 | 당행 | 당행 | text |  |
| 무역금융신청건포함명세_목록[].타행 | 무역금융신청건포함명세_목록[].타행 | 타행 | text |  |
| 운전자금_목록[].타행 | 운전자금_목록[].타행 | 타행 | text |  |
| 시설자금_목록[].타행 | 시설자금_목록[].타행 | 타행 | text |  |
| 지급보증_목록[].타행 | 지급보증_목록[].타행 | 타행 | text |  |
| 타행 | 타행 | 타행 | text |  |
| property.location | property.location | 부동산 | text | 본인 요청 |
| collateral.other | collateral.other | 기타 | text | 해당 없음 |
| deposit.savings_balance | deposit.savings_balance | 보통예금 | amount | 530,000 |
| deposit.time_balance | deposit.time_balance | 정기예금 | amount | 9,600,000 |
| 계2 | 계2 | 계 | text |  |
| collateral.time_deposit | collateral.time_deposit | 정기예금 | amount | 31,590,000 |
| collateral_list.i.property_amount | collateral_list.i.property_amount | 담보제공액 | amount | 340,000 |
| deposit_list[].savings_pledged | deposit_list[].savings_pledged | 담보제공액 | number | 6,680,000 |
| deposit_list[].time_pledged | deposit_list[].time_pledged | 담보제공액 | number | 6,540,000 |
| deposit_list[].savings_note | deposit_list[].savings_note | 비고 | text | 해당 없음 |
| deposit_list[].time_note | deposit_list[].time_note | 비고 | text | 해당 없음 |
| export.last_year | export.last_year | 전년도실적 | amount | USD 158,700 |
| export.last_year_nego | export.last_year_nego | 전년도실적당행Nego액 | amount | EUR 73,900 |
| export.past_year | export.past_year | 과거1년간실적 | amount | JPY 83,500 |
| export.past_year_nego | export.past_year_nego | 과거1년간당행Nego액 | amount | USD 12,600 |
| export.recent_3m | export.recent_3m | 최근3개월실적 | amount | USD 80,500 |
| export.recent_3m_nego | export.recent_3m_nego | 최근3개월당행Nego액 | amount | EUR 72,000 |
| export.this_year | export.this_year | 금년도수출실적 | amount | EUR 18,200 |
| export.this_year_nego | export.this_year_nego | 금년도당행Nego액 | amount | AUD 90,200 |
| export.this_year_plan | export.this_year_plan | 금년도예정액 | amount | EUR 124,700 |

### hf155 · 채권양도통지서(외국법인용)(K-biz파트너론)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.155 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 채무자(Obligor) | text | 박찬연 |
| 특기사항 | 특기사항 | 특기사항(Specialnote) | text | 해당 없음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 양도인주소 | 양도인주소 | 양도인(Assignor)주소(Address) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.name | corp.name | 상호(TradeName) | text | (주)유니온무역 |
| 양수인주소 | 양수인주소 | 양수인(Assignee)주소(Address) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 미화 | 미화 | 미화(USD) | text |  |
| 달러 | 달러 | 달러 | text |  |

### hf157 · 여신거래용 인감명판 등 신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.157 (대출) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 명판 | 명판 | 명판 | text |  |
| seal.signer | seal.customer | 거래용인감또는서명(서명을병용한경우및외국인에한함) | seal | 박찬연 |
| sign.signer | sign.customer | 거래용인감또는서명(서명을병용한경우및외국인에한함) | signature | 이욱유 |
| 목록[].변경후 | 목록[].변경후 | 변경후 | text | 해당 없음 |
| signer2.name | signer2.name | 대표자(본인자필) | text | 박찬연 |
| seal.signer2 | seal.corp | 대표자(본인자필) | seal | 강순준 |
| sign.signer2 | sign.signer2 | 대표자(본인자필) | signature | 박찬연 |
| 신고사항 | 신고사항 | 신고사항 | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 현선예 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 전민원 |
| seal.staff.대리 | seal.staff.대리 | 대리 | seal | 홍은호 |
| sign.staff.대리 | sign.staff.대리 | 대리 | signature | 정채은 |
| seal.staff.차장 | seal.staff.차장 | 차장 | seal | 김승경 |
| sign.staff.차장 | sign.staff.차장 | 차장 | signature | 고하도 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 확인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 황보건원 |

### hf158 · 위임장(하나골드신탁 만기 연장 접수용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.158 (신탁/ISA) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| signer.name | signer.name | ■기타※하나골드신탁만기연장외기타위임거래를구체적으로명시 | text | 주연희 |
| seal.signer | seal.signer | ■기타※하나골드신탁만기연장외기타위임거래를구체적으로명시 | seal | 박수은 |
| sign.signer | sign.signer | ■기타※하나골드신탁만기연장외기타위임거래를구체적으로명시 | signature | 주연희 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 본인(위임인)성명 | text | 박찬연 |
| seal.signer2 | seal.customer | 본인(위임인)성명 | seal | 현예지 |
| sign.signer2 | sign.customer | 본인(위임인)성명 | signature | 박찬연 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 소 | 소 | 소 | text |  |
| customer.phone2 | customer.phone2 | 연락처 | phone | 010-5907-7253 |
| 본인의투자성향파악여부에대한의사결정 | 본인의투자성향파악여부에대한의사결정 | -본인의투자성향파악여부에대한의사결정 | text |  |
| 본인의투자성향분석결과를확인하는행위 | 본인의투자성향분석결과를확인하는행위 | -본인의투자성향분석결과를확인하는행위 | text |  |
| 하나골드신탁만기연장과관련한일체의사항 | 하나골드신탁만기연장과관련한일체의사항 | ■하나골드신탁만기연장과관련한일체의사항 | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 윤영율 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 공수준 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 기선유 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 진진정 |

### hf159 · [필수] 개인(신용)정보 수집·이용 동의서(일임형ISA)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.159 (신탁/ISA) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용능력정보 | 신용능력정보 | ■신용능력정보 | text |  |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | -금융사고조사,분쟁해결,민원처리 | text |  |
| 직업에관한정보 | 직업에관한정보 | 직업에관한정보 | text |  |
| 연소득 | 연소득 | 연소득 | number | 16,990,000 |
| agent.name | agent.name | 대리인 | text | 박영준 |
| agent.name2 | agent.name2 | 대리인 | text | 박영준 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 확인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 위혜태 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 차우은 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 최우연 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이수지 |

### hf160 · 계약대상자확인서(일임형ISA용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.160 (신탁/ISA) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 가입대상 | 가입대상 | 가입대상 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| agent.name | agent.name | 대리인 | text | 박영준 |
| agent.name2 | agent.name2 | 대리인 | text | 박영준 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 김은진 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 이수빈 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 정성호 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 권원연 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 정영성 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 마찬민 |
| 가입대상2 | 가입대상2 | 가입대상 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| agent.name3 | agent.name3 | 대리인 | text | 박영준 |
| agent.name4 | agent.name4 | 대리인 | text | 박영준 |

### hf161 · 위임장 (특정금전신탁용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.161 (신탁/ISA) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일 | date | 900210 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| signer.name | signer.name | ■기타※신규외기타위임거래를구체적으로명시1.2.3. | text | 구유호 |
| seal.signer | seal.signer | ■기타※신규외기타위임거래를구체적으로명시1.2.3. | seal | 구유호 |
| sign.signer | sign.signer | ■기타※신규외기타위임거래를구체적으로명시1.2.3. | signature | 구민율 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 소 | 소 | 소 | text |  |
| 처 | 처 | 처 | text |  |
| signer2.name | signer2.name | 직원명 | text | 박환민 |
| seal.signer2 | seal.signer2 | 직원명 | seal | 박환민 |
| sign.signer2 | sign.signer2 | 직원명 | signature | 백기유 |
| 본인의투자성향파악여부에대한의사결정 | 본인의투자성향파악여부에대한의사결정 | -본인의투자성향파악여부에대한의사결정 | text |  |
| 본인의투자성향분석결과를확인하는행위 | 본인의투자성향분석결과를확인하는행위 | -본인의투자성향분석결과를확인하는행위 | text |  |
| 특정금전신탁상품가입과관련한일체의사항 | 특정금전신탁상품가입과관련한일체의사항 | ■특정금전신탁상품가입과관련한일체의사항 | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 박철희 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 심연승 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 임예린 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이규진 |

### hf162 · ISA계약만기연장 확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.162 (신탁/ISA) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 고객명(고객번호) | text | 박찬연 |
| ISA계좌번호 | ISA계좌번호 | ISA계좌번호 | text | 572-493488-10982 |
| 연장전계약만기일 | 연장전계약만기일 | 연장전계약만기일 | date | 2029.06.22 |
| 둥록점명 | 둥록점명 | 둥록점명(등록점번호) | text |  |
| 연장후계약만기일 | 연장후계약만기일 | 연장후계약만기일 | date | 2026-11-19 |
| 상담직원명 | 상담직원명 | 상담직원명(직원번호) | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 강수아 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 민수인 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 조연빈 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 임동도 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김훈승 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 금아연 |
| customer.name2 | customer.name2 | 고객명(고객번호) | text | 박찬연 |
| ISA계좌번호2 | ISA계좌번호2 | ISA계좌번호 | text | 868-027314-58004 |
| 연장전계약만기일2 | 연장전계약만기일2 | 연장전계약만기일 | date | 2028.01.30 |
| 둥록점명2 | 둥록점명2 | 둥록점명(등록점번호) | text |  |
| 연장후계약만기일2 | 연장후계약만기일2 | 연장후계약만기일 | date | 2029-05-06 |
| 상담직원명2 | 상담직원명2 | 상담직원명(직원번호) | text |  |

### hf163 · 위임장(일임형 개인종합자산관리계좌(ISA)용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.163 (신탁/ISA) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| signer.name | signer.name | ■기타※신규외기타위임거래를구체적으로명시1.2.3. | text | 장기연 |
| seal.signer | seal.signer | ■기타※신규외기타위임거래를구체적으로명시1.2.3. | seal | 이서혜 |
| sign.signer | sign.signer | ■기타※신규외기타위임거래를구체적으로명시1.2.3. | signature | 장기연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.birth2 | customer.birth2 | 생년월일 | date | 1990.02.10 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone2 | customer.phone2 | 연락처 | phone | 010-5907-7253 |
| 손실가능 | 손실가능 | 손실가능 | text |  |
| 본인의투자성향파악여부에대한의사결정 | 본인의투자성향파악여부에대한의사결정 | -본인의투자성향파악여부에대한의사결정 | text |  |
| 본인의투자성향분석결과를확인하는행위 | 본인의투자성향분석결과를확인하는행위 | -본인의투자성향분석결과를확인하는행위 | text |  |
| agent.name | agent.name | 대리인 | text | 박영준 |
| seal.signer2 | seal.signer2 | 사용인감,일임형ISA위임장 | seal | 현예지 |
| sign.signer2 | sign.signer2 | 사용인감,일임형ISA위임장 | signature | 이민빈 |
| seal.signer3 | seal.signer3 | 인감도장,일임형ISA위임장 | seal | 강순준 |
| sign.signer3 | sign.signer3 | 인감도장,일임형ISA위임장 | signature | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 주찬은 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 한건현 |

### hf001 · 상속예금 명의변경(지급) 의뢰서 및 손해담보 확약서(상속예금 지급 위임장 겸용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.1 (예금) 원본 위에 기재

연결 업무: 상속예금 지급 (inheritance)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 예금주 | text | 박찬연 |
| check.지급구분 | check.지급구분 | 지급구분 | checkbox | 분할지급 |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| 사망일자 | 사망일자 | 사망일자 | date | 2025.02.18 |
| 목록[].상품명 | 목록[].상품명 | 상품명 | text | 하나의정기예금 |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 022-588859-42883 |
| 목록[].금액 | 목록[].금액 | 금액 | text | 710,000 |
| check.보기1 | check.보기1 | 보기1 | checkbox | 보기1 |
| check.보기12 | check.보기12 | 보기1 | checkbox | 보기1 |
| check.보기13 | check.보기13 | 보기1 | checkbox | 보기1 |
| check.보기14 | check.보기14 | 보기1 | checkbox | 보기1 |
| check.보기15 | check.보기15 | 보기1 | checkbox | 보기1 |
| check.명의변경 | check.명의변경 | 명의변경 | checkbox | □ |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 기타특약사항 | 기타특약사항 | 기타특약사항 | text | 해당 없음 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김규준 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 배석도 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 성연은 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 확인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 최석주 |
| check.주된상속인 | check.주된상속인 | 주된상속인(소득귀속인) | checkbox | 본인 |
| check.상속인 | check.상속인 | 상속인 | checkbox | 위임(주된 상속인 앞) |
| check.상속인2 | check.상속인2 | 상속인 | checkbox | 위임(주된 상속인 앞) |
| check.상속인3 | check.상속인3 | 상속인 | checkbox | 본인 |
| check.상속인4 | check.상속인4 | 상속인 | checkbox | 본인 |
| check.상속인5 | check.상속인5 | 상속인 | checkbox | 본인 |
| 목록[].성명 | 목록[].성명 | 성명 | text | 강민도 |
| 목록[].생년월일 | 목록[].생년월일 | 생년월일 | text | 2025-05-23 |
| 목록[].연락처 | 목록[].연락처 | 연락처 | text | 010-5907-7253 |
| 목록[].예금잔액 | 목록[].예금잔액 | 예금잔액 | text | 70,740,000 |
| 목록[].미지급사유주1 | 목록[].미지급사유주1 | 미지급사유주1 | text | 만기 해지 |
| 목록[].상속인확인 | 목록[].상속인확인 | 상속인확인 | text |  |
| signer.name | signer.name | 확인담당자 | text | 류상빈 |
| seal.signer | seal.signer | 확인담당자 | seal | 김철찬 |
| sign.signer | sign.signer | 확인담당자 | signature | 류상빈 |
| signer2.name | signer2.name | 확인책임자 | text | 이호서 |
| seal.signer2 | seal.signer2 | 확인책임자 | seal | 남궁도원 |
| sign.signer2 | sign.signer2 | 확인책임자 | signature | 김규호 |

연결 업무 inheritance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### hf002 · 은행거래신청서(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.2 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| Home | Home | Home | text |  |
| Office | Office | Office | text |  |
| Home2 | Home2 | Home | text |  |
| Office2 | Office2 | Office | text |  |
| Occupation | Occupation | Occupation | text |  |
| Occupation2 | Occupation2 | Occupation | text |  |
| Payday | Payday | Payday | text |  |
| Nochangeincustomerinformation | Nochangeincustomerinformation | Nochangeincustomerinformation | text |  |
| RequestforSMSmaturitynotice | RequestforSMSmaturitynotice | RequestforSMSmaturitynotice | text |  |
| 갋 | 갋 | 갋 | text |  |
| 갋2 | 갋2 | 갋 | text |  |
| 갋3 | 갋3 | 갋 | text |  |
| 목록[].FixedFloating | 목록[].FixedFloating | FixedFloating(mth) | text |  |
| AccountItem | AccountItem | AccountItem | text |  |
| PaymentDeadline | PaymentDeadline | PaymentDeadline | text |  |
| mthcapitalizationLimit | mthcapitalizationLimit | ()mthcapitalizationLimit | amount | 660,000 |
| mthcapitalizationLimit2 | mthcapitalizationLimit2 | ()mthcapitalizationLimit | amount | 251,710,000원 |
| mthcapitalizationLimit3 | mthcapitalizationLimit3 | ()mthcapitalizationLimit | amount | 240,000 |
| check.Irequestagr | check.Irequestagr | Irequest/agreetoaninquiryofmyfina | checkbox | I request/agree to an inquiry of my fina |
| check.Ishallraisen | check.Ishallraisen | Ishallraisenoobjectiontoaset-off | checkbox | I shall raise no objection to a set-off  |
| check.Ihavereceive | check.Ihavereceive | Ihavereceivedanexplanationthatcust | checkbox | I have received an explanation that cust |
| Bankbook | Bankbook | Bankbook | text |  |
| Annual | Annual | Annual | text |  |
| Bankbook2 | Bankbook2 | Bankbook | text |  |
| Annual2 | Annual2 | Annual | text |  |
| Annual3 | Annual3 | Annual | text |  |
| Bankbook3 | Bankbook3 | Bankbook | text |  |
| WithdrawalAccount | WithdrawalAccount | WithdrawalAccount[ | text |  |
| Applicant | Applicant | Applicant | text | 제일무역 |
| YYYY | YYYY | YYYY | text |  |
| account | account | AccountNo. | account_no | 000-287736-52424 |
| DateofOpening | DateofOpening | DateofOpening | date | 2025.02.01 |
| Category | Category | Category | text |  |
| Time | Time | Time | text |  |
| EmployeeNumber | EmployeeNumber | EmployeeNumber | text |  |
| NewWithdrawalAccountAddition | NewWithdrawalAccountAddition | NewWithdrawalAccountAddition | text |  |
| YesNo | YesNo | YesNo | text | 151-558491-65694 |
| Statusofassets | Statusofassets | Statusofassets | amount |  |
| Sourcesoffinancing | Sourcesoffinancing | Sourcesoffinancing | text |  |
| YesNo2 | YesNo2 | YesNo | text | 353-944363-95188 |
| BusinessName | BusinessName | BusinessName | text |  |
| Industry | Industry | Industry(BusinessType/Item) | text |  |
| BusinessRegistrationNo | BusinessRegistrationNo | BusinessRegistrationNo. | biz_no | 264-82-36559 |
| BusinessCommencementDate | BusinessCommencementDate | BusinessCommencementDate | date | 2025.02.18 |
| DepositAccount | DepositAccount | DepositAccount | text |  |
| customer.name | customer.name | Name | text | 박찬연 |
| RelationtoPrincipal | RelationtoPrincipal | RelationtoPrincipal | text |  |
| customer.birth | customer.birth | DateofBirth | date | 1990.02.10 |
| customer.address | customer.address | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| PhoneNo | PhoneNo | PhoneNo. | phone | 010-5907-7253 |
| AccountItem2 | AccountItem2 | AccountItem | text |  |
| PaymentDeadline2 | PaymentDeadline2 | PaymentDeadline | text |  |
| PhoneBanking | PhoneBanking | PhoneBanking | text |  |
| Applicant2 | Applicant2 | Applicant | text | (주)유니온물산 |
| Applicant3 | Applicant3 | Applicant | text | (주)대성화학 |
| Publicfeepayment | Publicfeepayment | Publicfeepayment | amount |  |
| Other | Other | Other() | text |  |
| Applicant4 | Applicant4 | Applicant | text | 주식회사 동방메디칼 |
| thedateofrenewal | thedateofrenewal | thedateofrenewal | date |  |
| Depositor | Depositor | Depositor | text |  |
| Proxy | Proxy | Proxy | text |  |
| Delegator | Delegator | Delegator(Depositor) | text |  |
| account2 | account2 | AccountNo. | account_no | 000-287736-52424 |
| DateofOpening2 | DateofOpening2 | DateofOpening | date | 2025.03.06 |
| Category2 | Category2 | Category | text |  |
| Time2 | Time2 | Time | text |  |
| EmployeeNumber2 | EmployeeNumber2 | EmployeeNumber | text |  |

### hf003 · 은행거래신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.3 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| deposit_list[].interest_account | deposit_list[].interest_account | 통장발행 | account_no | 852-218961-86830 |
| 목록[].갋 | 목록[].갋 | 갋 | text |  |
| 갋 | 갋 | 갋 | text |  |
| 갋2 | 갋2 | 갋 | text |  |
| 갋3 | 갋3 | 갋 | text |  |
| deposit_list_list[][].transfer_day | deposit_list_list[][].transfer_day | 확정형연동형(개월) | text | 15일 |
| seal.signer | seal.signer | 한도:₩..~.. | seal | 강순준 |
| sign.signer | sign.signer | 한도:₩..~.. | signature | 박찬연 |
| seal.signer2 | seal.signer2 | 한도:₩..~.. | seal | 강순준 |
| sign.signer2 | sign.signer2 | 한도:₩..~.. | signature | 박찬연 |
| seal.signer3 | seal.signer3 | 한도:₩..~.. | seal | 이욱유 |
| sign.signer3 | sign.signer3 | 한도:₩..~.. | signature | 박찬연 |
| customer.name_en | customer.name_en | 영문명 | text | PARK CHANYEON |
| customer.email | customer.email | 이메일 | text | chanyeon363@naver.com |
| customer.address | customer.address | 자택 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| employer.address | employer.address | 직장 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태평양무역 구매팀 |
| customer.home_phone | customer.home_phone | 자택 | phone | 02-1577-0823 |
| employer.phone | employer.phone | 직장 | phone | 043-783-2775 |
| customer.payday | customer.payday | 급여일 | text | 10일 |
| seal.signer4 | seal.signer4 | 고객정보변경없음 | seal | 박찬연 |
| sign.signer4 | sign.signer4 | 고객정보변경없음 | signature | 현예지 |
| bank.auto_transfer_account | bank.auto_transfer_account | 자동이체계좌번호 | account_no | 695-630925-11217 |
| bank.subject | bank.subject | 과목명 | text | 하나의정기예금 |
| bank.contract_amount | bank.contract_amount | 계약(확인)금액 | amount | 8,670,000 |
| bank.pay_date | bank.pay_date | 지급기일 | date | 2029.03.18 |
| check.비과세종합저축재형저축 | check.비과세종합저축재형저축 | 비과세종합저축/재형저축/주택청약상품의계약금액/한도/중복 | checkbox | 비과세종합저축 / 재형저축 / 주택청약상품의 계약금액 / 한도 / 중복  |
| check.귀행에대한제대출금보증채 | check.귀행에대한제대출금보증채 | 귀행에대한제대출금,보증채무,신용카드채무에대하여변제기가도래하 | checkbox | 귀행에 대한 제 대출금, 보증채무, 신용카드채무에 대하여 변제기가 도래하 |
| check.본인은금융지주회사법제4 | check.본인은금융지주회사법제4 | 본인은금융지주회사법제48조의2에근거하여하나금융그룹내지주사및자 | checkbox | 본인은 금융지주회사법 제48조의2에 근거하여 하나금융그룹내 지주사 및 자 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| deposit_list[].tax_free_limit | deposit_list[].tax_free_limit | 연원가식 | amount | 6,370,000원 |
| deposit.withdraw_account | deposit.withdraw_account | 출금계좌[ | account_no | 000-287736-52424 |
| customer.name | customer.name | 신청인 | text | 박찬연 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| bank.first_trade_date | bank.first_trade_date | 최초거래일 | date | 2025년 4월 7일 |
| bank.open_date | bank.open_date | 신규일 | date | 2025.07.05 |
| bank.deposit_amount | bank.deposit_amount | 입금(수탁)액 | amount | 2,050,000 |
| bank.kind | bank.kind | 종별 | text | 급여하나 통장 |
| bank.staff_no | bank.staff_no | 권유직원번호 | text | 1543-9646 |
| customer.name7 | customer.name7 | 성명(업체명) | text | 박찬연 |
| customer.birth | customer.birth | 생년월일(사업자번호) | date | 1990년 2월 10일 |
| customer.phone | customer.phone | 휴대폰 | phone | 010-5907-7253 |
| customer.email2 | customer.email2 | 계약서류수령E-mail또는휴대폰번호 | text | chanyeon363@naver.com |
| deposit_list[].product | deposit_list[].product | 상품명1 | text | 급여하나 통장 |
| deposit_list[].amount | deposit_list[].amount | 가입금액1 | amount | 530,000 |
| deposit_list[].period | deposit_list[].period | 계약기간1 | text | 6개월 |
| deposit_list[].transfer_amount | deposit_list[].transfer_amount | 이체금액1 | amount | 179,700,000 |
| deposit_list[].transfer_end | deposit_list[].transfer_end | 이체기간(만료일)1 | date | 2025-02-28 |
| deposit_list[].funding_amount | deposit_list[].funding_amount | 출금금액① | amount | 5,070,000원 |
| date2 | date2 | 작성일(년월일) | date | 2026.01.31 |
| ebank.user_id | ebank.user_id | 이용자ID | text | leewk1025 |
| company.name | corp.name | 상호명 | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| company.established | company.established | 개업년월일 | date | 2018.11.01 |
| account2 | account2 | 입금계좌 | account_no | 000-287736-52424 |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| agent.birth | agent.birth | 생년월일 | date | 1962.12.19 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.phone | agent.phone | 전화번호 | phone | 010-6515-4769 |
| bank.auto_transfer_account2 | bank.auto_transfer_account2 | 자동이체계좌번호 | text | 392-645706-50333 |
| bank.subject2 | bank.subject2 | 과목명 | text | 하나 적금 |
| bank.contract_amount2 | bank.contract_amount2 | 계약(확인)금액 | amount | 196,780,000 |
| bank.pay_date2 | bank.pay_date2 | 지급기일 | date | 2027.08.02 |
| ebank.phone_limit_once | ebank.phone_limit_once | 원)(1회 | amount | 250,000 |
| customer.name2 | customer.name2 | 신청인 | text | 박찬연 |
| customer.name3 | customer.name3 | 신청인 | text | 박찬연 |
| related.name | related.name | 아니오(실제소유자성명 | text | 서서예 |
| redeposit_list[].product | redeposit_list[].product | [신청상품]1 | text | 청년도약계좌 |
| customer.name4 | customer.name4 | 신청인 | text | 박찬연 |
| customer.name5 | customer.name5 | 예금주 | text | 박찬연 |
| agent.name2 | agent.name2 | 대리인 | text | 박영준 |
| customer.name6 | customer.name6 | 위임인(예금주) | text | 박찬연 |
| account3 | account3 | 계좌번호 | account_no | 000-287736-52424 |
| bank.first_trade_date2 | bank.first_trade_date2 | 최초거래일 | date | 2025년 1월 31일 |
| bank.open_date2 | bank.open_date2 | 신규일 | date | 2025.11.09 |
| bank.deposit_amount2 | bank.deposit_amount2 | 입금(수탁)액 | amount | 52,410,000 |
| bank.kind2 | bank.kind2 | 종별 | text | 청년도약계좌 |
| bank.staff_no2 | bank.staff_no2 | 권유직원번호 | text | 054561-0220146 |
| related.rrn | related.rrn | 실명번호: | text | 532403-4667905 |
| ebank.internet_limit_day | ebank.internet_limit_day | 인터넷/스마트폰뱅킹1일한도 | amount | 9,650,000 |
| ebank.internet_limit_once | ebank.internet_limit_once | 인터넷/스마트폰뱅킹1회한도 | amount | 3,580,000 |
| ebank.phone_limit_day | ebank.phone_limit_day | 폰뱅킹1일한도 | amount | 44,370,000 |
| ebank.passbook_memo | ebank.passbook_memo | 전자통장설명문구(한글6자) | text | 만기 해지 |
| customer.name_en2 | customer.name_en2 | 영문명(전자화폐발급시) | text | PARK CHANYEON |
| deposit.renew_count | deposit.renew_count | 갱신횟수 | number | 1 |

### hf004 · 보호예수품 반환 의뢰서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.4 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 일련번호 | 일련번호 | 일련번호 | text | 163-002222-55387 |
| check.예수방법 | check.예수방법 | 예수방법 | checkbox | 봉함예수 |
| 예수품명 | 예수품명 | 예수품명 | text | LED 모듈 |
| 예수금액 | 예수금액 | 예수금액 | number | 30,250,000 |
| 증권번호 | 증권번호 | 증권번호 | text | 579884-6812926 |
| 예수수량 | 예수수량 | 예수수량 | number | 2 |
| signer.name | customer.name | 성명(상호명) | text | 박찬연 |
| seal.signer | seal.customer | 성명(상호명) | seal | 박찬연 |
| sign.signer | sign.customer | 성명(상호명) | signature | 강순준 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.birth | customer.birth | 생년월일(사업자등록번호) | date | 1990.02.10 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 김원인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 이환성 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 기정인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 정철린 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이하호 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 김미예 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 김윤찬 |

### hf005 · 보호예수 의뢰서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.5 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.예수종류 | check.예수종류 | 예수종류 | checkbox | 봉함예수 |
| 예수수량 | 예수수량 | 예수수량 | number | 3 |
| check.만기일자 | check.만기일자 | 만기일자 | checkbox | 예적금 만기일( |
| 예수품명 | 예수품명 | 예수품명 | text | 철강 코일 |
| 예수금액 | 예수금액 | 예수금액 | number | 99,200,000 |
| 증권번호 | 증권번호 | 증권번호 | text | 803-587953-68618 |
| check.수령방법 | check.수령방법 | 수령방법 | checkbox | 영업점 |
| signer.name | customer.name | 성명(상호명) | text | 박찬연 |
| seal.signer | seal.customer | 성명(상호명) | seal | 현예지 |
| sign.signer | sign.customer | 성명(상호명) | signature | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.birth | customer.birth | 생년월일(사업자등록번호) | date | 1990.02.10 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 검인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 박나도 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 염나연 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이현우 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 마철린 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 장영호 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 확인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 방선준 |

### hf006 · 자동이체 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.6 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 예금자성명 | text | 박찬연 |
| seal.signer | seal.customer | 예금자성명 | seal | 강순준 |
| sign.signer | sign.customer | 예금자성명 | signature | 박찬연 |
| account | account | 출금계좌번호 | account_no | 000-287736-52424 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 변경후출금계좌번호 | 변경후출금계좌번호 | 변경후출금계좌번호 | text | 해당 없음 |
| check.신청구분 | check.신청구분 | 신청구분( | checkbox | 해지 |
| check.이체일이휴일인경우 | check.이체일이휴일인경우 | [당행요구불계좌이체,타행자동이체]이체일이휴일인경우 | checkbox | 익 영업일 이체를 신청합니다. |
| check.신청구분2 | check.신청구분2 | 신청구분( | checkbox | 변경 |
| check.이체일이휴일인경우2 | check.이체일이휴일인경우2 | [당행요구불계좌이체,타행자동이체]이체일이휴일인경우 | checkbox | 익 영업일 이체를 신청합니다. |
| 은행 | 은행 | 은행 | text | 우리은행 |
| 지급인자내용 | 지급인자내용 | 지급인자내용 | text | 해당 없음 |
| 은행2 | 은행2 | 은행 | text | 하나은행 |
| 지급인자내용2 | 지급인자내용2 | 지급인자내용 | text | 해당 없음 |
| check.자동이체기간만료SMS통지 | check.자동이체기간만료SMS통지 | 자동이체기간만료SMS통지( | checkbox | 미신청 |
| 목록[].예금주명 | 목록[].예금주명 | 예금주명 | text |  |
| check.자동이체기간만료SMS통지2 | check.자동이체기간만료SMS통지2 | 자동이체기간만료SMS통지( | checkbox | 미신청 |
| 목록[].이체일 | 목록[].이체일 | 이체일 | date | 2025.12.01 |
| 목록[].이체주기 | 목록[].이체주기 | 이체주기(일☞주☞월☞년) | text |  |
| 목록[].이체금액 | 목록[].이체금액 | 이체금액 | number | 9,330,000 |
| 입금인자내용 | 입금인자내용 | 입금인자내용 | text | 해당 없음 |
| 입금인자내용2 | 입금인자내용2 | 입금인자내용 | text | 해당 없음 |
| check.수수료포함출금 | check.수수료포함출금 | 수수료포함출금( | checkbox | 미신청 |
| date | date | 일자 | date | 2026년 1월 31일 |
| check.수수료포함출금2 | check.수수료포함출금2 | 수수료포함출금( | checkbox | 신청 |
| date2 | date2 | 일자 | date | 2026년 1월 31일 |
| date3 | date3 | 년월일 | date | 2026년 1월 31일 |
| date4 | date4 | 년월일 | date | 2026년 1월 31일 |
| account2 | account2 | 입금계좌번호 | account_no | 000-287736-52424 |
| check.만기이연시선택 | check.만기이연시선택 | [정액적립식]만기이연시선택 | checkbox | 이연만기일 이체 신청함 |
| check.갱신구분 | check.갱신구분 | 갱신구분 | checkbox | 이자포함 |
| check.계약서류수령방법 | check.계약서류수령방법 | 계약서류*수령방법 | checkbox | 별도 연락처로 수령( |
| account3 | account3 | 입금계좌 | account_no | 000-287736-52424 |
| check.자동이체정지 | check.자동이체정지 | 자동이체정지 | checkbox | 해제 |
| 구분 | 구분 | 구분 | text |  |
| 관리비지로공과금기타_목록[].수납기관 | 관리비지로공과금기타_목록[].수납기관 | 수납기관(아파트,상가) | text |  |
| 수납기관 | 수납기관 | 수납기관(아파트,상가) | text |  |
| 관리비지로공과금기타_목록[].납부자번호 | 관리비지로공과금기타_목록[].납부자번호 | 납부자번호(동,호수,수용가번호,등) | text | 1242-4488 |
| 납부자번호 | 납부자번호 | 납부자번호(동,호수,수용가번호,등) | text | 028927-2699202 |
| 관리비지로공과금기타_목록[].지로번호기관코드 | 관리비지로공과금기타_목록[].지로번호기관코드 | 지로번호/기관코드 | number | 59199 |
| 지로번호기관코드 | 지로번호기관코드 | 지로번호/기관코드 | number | 609622 |
| 관리비지로공과금기타_목록[].납부희망일 | 관리비지로공과금기타_목록[].납부희망일 | 납부희망일 | date | 2025년 3월 9일 |
| date5 | date5 | 작성일 | date | 2026년 1월 31일 |
| check.계좌간자동이체 | check.계좌간자동이체 | 계좌간자동이체( | checkbox | 당행 자동이체 |
| check.만기해지자동이체 | check.만기해지자동이체 | 만기해지자동이체( | checkbox | 신규 |
| check.자동갱신자동이체 | check.자동갱신자동이체 | 자동갱신(재예치)자동이체( | checkbox | 신규 |
| check.기타자동이체 | check.기타자동이체 | 기타자동이체( | checkbox | 신규 |
| check.계좌번호 | check.계좌번호 | 계좌번호 | checkbox | 미적용 |
| check.조회 | check.조회 | 조회 | checkbox | 조회 |
| check.고객명 | check.고객명 | 고객명 | checkbox | 미적용 |

### hf007 · 질권실행 의뢰서(수신_제3자 질권용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.7 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].예금종류 | 목록[].예금종류 | 예금종류 | text | 하나 적금 |
| 목록[].예금주 | 목록[].예금주 | 예금주(위탁자/수탁자) | text |  |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 526-608893-10332 |
| 목록[].예금액 | 목록[].예금액 | 예금액 | number | 33,170,000 |
| 목록[].만기일주1 | 목록[].만기일주1 | 만기일주1 | date | 2027-12-13 |
| 목록[].질권설정금액 | 목록[].질권설정금액 | 질권설정금액 | number | 2,130,000 |
| 목록[].변제기일주1 | 목록[].변제기일주1 | 변제기일주1 | date | 2027.10.01 |
| signer.name | customer.name | 성명(업체명) | text | 박찬연 |
| seal.signer | seal.customer | 성명(업체명) | seal | 현예지 |
| sign.signer | sign.customer | 성명(업체명) | signature | 강순준 |
| customer.birth | customer.birth | 생년월일(사업자등록번호) | date | 1990.02.10 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인인감대조 | seal.staff.본인확인인감대조 | 본인확인인감대조 | seal | 검인 |
| sign.staff.본인확인인감대조 | sign.staff.본인확인인감대조 | 본인확인인감대조 | signature | 김현인 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 연서유 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 선영인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 위환연 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 검인 |
| seal.staff.지점장 | seal.staff.지점장 | 지점장 | seal | 검인 |
| sign.staff.지점장 | sign.staff.지점장 | 지점장 | signature | 성환도 |

### hf008 · 질권해지 통지서(수신_제3자 질권용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.8 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].예금종류 | 목록[].예금종류 | 예금종류 | text | 하나 적금 |
| 목록[].예금주 | 목록[].예금주 | 예금주(위탁자/수탁자) | text |  |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 538-829499-23588 |
| 목록[].예금액 | 목록[].예금액 | 예금액 | number | 28,480,000 |
| 목록[].만기일 | 목록[].만기일 | 만기일 | date | 2029년 9월 1일 |
| 목록[].질권설정금액 | 목록[].질권설정금액 | 질권설정금액 | number | 68,210,000 |
| 목록[].변제기일 | 목록[].변제기일 | 변제기일 | date | 2027.01.11 |
| signer.name | customer.name | 성명(업체명) | text | 박찬연 |
| seal.signer | seal.customer | 성명(업체명) | seal | 박찬연 |
| sign.signer | sign.customer | 성명(업체명) | signature | 강순준 |
| customer.birth | customer.birth | 생년월일(사업자등록번호) | date | 1990년 2월 10일 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인인감대조 | seal.staff.본인확인인감대조 | 본인확인인감대조 | seal | 이준현 |
| sign.staff.본인확인인감대조 | sign.staff.본인확인인감대조 | 본인확인인감대조 | signature | 명소경 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 이현예 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이우혜 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 홍경인 |
| seal.staff.지점장 | seal.staff.지점장 | 지점장 | seal | 검인 |
| sign.staff.지점장 | sign.staff.지점장 | 지점장 | signature | 원다혜 |

### hf009 · 질권설정 승낙의뢰서(수신_제3자 질권용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.9 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].예금종류 | 목록[].예금종류 | 예금종류 | text | 하나의정기예금 |
| 목록[].예금주 | 목록[].예금주 | 예금주(위탁자/수탁자) | text |  |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 903-550493-89454 |
| 목록[].금액주1 | 목록[].금액주1 | 금액주1 | number | 116,080,000원 |
| 목록[].만기일주2 | 목록[].만기일주2 | 만기일주2 | date | 2027-03-02 |
| 목록[].질권설정금액 | 목록[].질권설정금액 | 질권설정금액 | number | 16,800,000 |
| 목록[].변제기일주2 | 목록[].변제기일주2 | 변제기일주2 | date | 2027.06.12 |
| signer.name | customer.name | 성명(업체명) | text | 박찬연 |
| seal.signer | seal.customer | 성명(업체명) | seal | 강순준 |
| sign.signer | sign.customer | 성명(업체명) | signature | 박찬연 |
| customer.birth | customer.birth | 생년월일(사업자등록번호) | date | 1990.02.10 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| signer2.name | signer2.name | 성명(업체명) | text | 박찬연 |
| seal.signer2 | seal.signer2 | 성명(업체명) | seal | 강순준 |
| sign.signer2 | sign.signer2 | 성명(업체명) | signature | 박찬연 |
| customer.birth2 | customer.birth2 | 생년월일(사업자등록번호) | date | 1990.02.10 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone2 | customer.phone2 | 연락처 | phone | 010-5907-7253 |
| signer3.name | signer3.name | 질권설정자(예금주) | text | 박찬연 |
| seal.signer3 | seal.signer3 | 질권설정자(예금주) | seal | 박찬연 |
| sign.signer3 | sign.signer3 | 질권설정자(예금주) | signature | 강순준 |
| signer4.name | signer4.name | 질권자 | text | 황영태 |
| seal.signer4 | seal.signer4 | 질권자 | seal | 이우찬 |
| sign.signer4 | sign.signer4 | 질권자 | signature | 황영태 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인인감대조 | seal.staff.본인확인인감대조 | 본인확인인감대조 | seal | 검인 |
| sign.staff.본인확인인감대조 | sign.staff.본인확인인감대조 | 본인확인인감대조 | signature | 장연준 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김연찬 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 배재인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 천진율 |
| seal.staff.지점장 | seal.staff.지점장 | 지점장 | seal | 검인 |
| sign.staff.지점장 | sign.staff.지점장 | 지점장 | signature | 채서호 |

### hf010 · 주식(사채)납입금 수납대행의뢰서(보관증명서 발급의뢰서 겸용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.10 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 책임자 | 책임자 | 책임자(관리자) | text |  |
| 영업점장 | 영업점장 | 영업점장 | text |  |
| date | date | 납입기일 | date | 2026년 1월 31일 |
| check.주식납입금수납 | check.주식납입금수납 | 주식납입금수납 | checkbox | 신주발행 |
| check.사채납입금수납 | check.사채납입금수납 | 사채납입금수납 | checkbox | 사채발행 |
| 주식수 | 주식수 | 주식수 | number | 60 |
| 발행가액 | 발행가액 | 발행가액(1주당) | number | 12,030,000 |
| 발행주식총수 | 발행주식총수 | 발행주식총수 | number | 60 |
| 주주배정 | 주주배정 | 주주배정 | number | 60 |
| check.증명서종류 | check.증명서종류 | 증명서종류 | checkbox | 보관증명서 |
| check.증명서종류2 | check.증명서종류2 | 증명서종류 | checkbox | 납입완료사실증명서 |
| 금액 | 금액 | 금액 | number | 9,310,000 |
| 액면가액 | 액면가액 | 액면가액(1주당) | number | 191,340,000 |
| 기발행주식총수 | 기발행주식총수 | 기발행주식총수 | number | 3 |
| 공모 | 공모 | 공모 | number | 24 |
| signer.name | corp.ceo | 발기인대표(또는)대표이사 | text | 박찬연 |
| seal.signer | seal.corp | 발기인대표(또는)대표이사 | seal | 강순준 |
| sign.signer | sign.customer | 발기인대표(또는)대표이사 | signature | 박찬연 |
| 위탁회사주소 | 위탁회사주소 | 위탁회사주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| employer.name | employer.name | 회사명 | text | 주식회사 태평양무역 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 또는주주총회결의록사본 | 또는주주총회결의록사본 | 또는주주총회결의록사본 | text |  |

### hf011 · 예금(신탁)잔액증명 의뢰서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.11 (예금) 원본 위에 기재

연결 업무: 상속예금 지급 (inheritance)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 변경 |
| check.대상계좌 | check.대상계좌 | 대상계좌(발급세부) | checkbox | 지정계좌 |
| check.대상계좌2 | check.대상계좌2 | 대상계좌(발급세부) | checkbox | 계좌마스킹(계좌번호 일부숨김) |
| check.수령방법 | check.수령방법 | 수령방법 | checkbox | 카카오톡(문자) |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| account2 | account2 | 계좌번호 | account_no | 000-287736-52424 |
| account3 | account3 | 계좌번호 | account_no | 000-287736-52424 |
| check.기준일자 | check.기준일자 | 기준일자 | checkbox | 매월 |
| check.유효기간 | check.유효기간 | 유효기간 | checkbox | 보기1 |
| check.창구수령대리인 | check.창구수령대리인 | 창구수령대리인 | checkbox | 성명 |
| check.우편수령대리인 | check.우편수령대리인 | 우편수령대리인 | checkbox | 주소 |
| 발급기준일 | 발급기준일 | 발급기준일 | date | 2025-01-29 |
| 국문 | 국문 | 국문 | number | 6 |
| 매 | 매 | 매 | number | 3 |
| 계좌번호_목록[].value | 계좌번호_목록[].value | (통화코드:) | amount |  |
| check.수령방법2 | check.수령방법2 | 수령방법 | checkbox | 우편수령 ᄆ 창구수령 |
| 발급부수 | 발급부수 | 발급부수 | text |  |
| 발급부수2 | 발급부수2 | 발급부수 | text |  |
| signer.name | customer.name | 성명(상호명) | text | 박찬연 |
| seal.signer | seal.customer | 성명(상호명) | seal | 위나아 |
| sign.signer | sign.customer | 성명(상호명) | signature | 박찬연 |
| customer.name_en | customer.name_en | 영문명 | text | PARK CHANYEON |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.birth | customer.birth | 생년월일(사업자번호) | date | 1990-02-10 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| agent.name | agent.name | 대리인성명 | text | 박영준 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.본인은상기계좌의 | check.본인은상기계좌의 | 본인은상기계좌의( | checkbox | 잔액증명서 발급 |
| agent.birth | agent.birth | 생년월일 | date | 1962.12.19 |
| agent.phone | agent.phone | 연락처 | phone | 010-6515-4769 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 황숙은 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 지원혜 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 위순영 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이민태 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 최하찬 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 확인 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 확인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 이주원 |

연결 업무 inheritance · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### hf015 · 통합제신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.15 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.성명휴대폰번호자택주소직장원본수익자수익수익자 | check.성명휴대폰번호자택주소직장원본수익자수익수익자 | 성명(업체명)휴대폰번호자택주소직장원본수익자수익수익자 | checkbox | KT |
| 신청내용 | 신청내용 | 신청내용 | text | 해당 없음 |
| 변경내용 | 변경내용 | 변경내용 | text | 해당 없음 |
| 변경전 | 변경전 | 변경전 | text | 해당 없음 |
| seal.signer | seal.customer | 인감(서명) | seal | 위나아 |
| sign.signer | sign.customer | 인감(서명) | signature | 현예지 |
| 변경후 | 변경후 | 변경후 | text | 해당 없음 |
| Email또는휴대폰번호 | Email또는휴대폰번호 | E-mail또는휴대폰번호 | phone | 010-5907-7253 |
| 연락처Email기타 | 연락처Email기타 | 연락처,E-mail,기타 | text | 해당 없음 |
| 수령확인 | 수령확인 | 수령확인 | text |  |
| account | account | 출금계좌번호 | account_no | 000-287736-52424 |
| customer.name | customer.name | 성명(업체명) | text | 박찬연 |
| 신고인 | 신고인 | ⇁신고인 | text |  |
| 본인과의관계 | 본인과의관계 | ⇁본인과의관계 | text |  |
| 연락처 | 연락처 | )⇁연락처 | phone | 010-5907-7253 |
| 상품명 | 상품명 | ⇁상품명 | text | 급여하나 통장 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 대리인 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인 | seal | 박영준 |
| sign.signer2 | sign.agent | 대리인 | signature | 강석호 |
| 제신고내용 | 제신고내용 | ⇁제신고(내용 | text | 해당 없음 |
| value | value | [유선신고사항] | amount |  |
| agent.name | agent.name | 대리인성명 | text | 박영준 |
| agent.phone | agent.phone | 연락처 | phone | 010-6515-4769 |
| 위임내용 | 위임내용 | 위임내용 | text | 해당 없음 |
| customer.birth | customer.birth | 생년월일 | date | 900210 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer3.name | signer3.name | 위임인 | text | 박찬연 |
| seal.signer3 | seal.signer3 | 위임인 | seal | 현예지 |
| sign.signer3 | sign.signer3 | 위임인 | signature | 박찬연 |
| 위임장 | 위임장 | 위임장 | text |  |

### hf016 · 종합금융상품 ON-LINE 거래 약정서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.16 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 예금주 | text | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.biz_no | corp.biz_no | 사업자등록번호(생년월일) | biz_no | 264-82-36559 |
| seal.signer | seal.customer | 통장인감 | seal | 박찬연 |
| sign.signer | sign.customer | 통장인감 | signature | 강순준 |
| seal.signer2 | seal.signer2 | 통장인감 | seal | 최우빈 |
| sign.signer2 | sign.signer2 | 통장인감 | signature | 박찬연 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| customer.name2 | customer.name2 | 예금주 | text | 박찬연 |
| account2 | account2 | 계좌번호 | account_no | 000-287736-52424 |
| customer.name3 | customer.name3 | 예금주 | text | 박찬연 |
| 참고사항 | 참고사항 | 참고사항(신청내용등) | text |  |
| 목록[].은행지점 | 목록[].은행지점 | 은행지점 | text | 국민은행 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer3.name | signer3.name | 본인(예금주) | text | 박찬연 |
| seal.signer3 | seal.signer3 | 본인(예금주) | seal | 현예지 |
| sign.signer3 | sign.signer3 | 본인(예금주) | signature | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 양하준 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 남상현 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 확인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 민채도 |

### hf017 · 종합금융상품 ON-LINE_거래 (이체)신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.17 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명(회사명) | text | 박찬연 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| Fax번호 | Fax번호 | Fax번호 | text | 456890-3500297 |
| check.입금 | check.입금 | 입금 | checkbox | 입 금 |
| check.예금종류 | check.예금종류 | 예금종류 | checkbox | CMA |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| 입금금액 | 입금금액 | 입금금액 | number | 6,080,000 |
| 기간 | 기간 | 기간(만기일) | text |  |
| 이율 | 이율 | 이율 | number | 6.70 |
| check.입금방법 | check.입금방법 | 입금방법 | checkbox | 지준 |
| 지준입금액 | 지준입금액 | 지준입금액 | number | 880,000 |
| 전금입금액 | 전금입금액 | 전금입금액 | number | 15,750,000 |
| 계좌입금액 | 계좌입금액 | 계좌입금액 | number | 2,580,000원 |
| check.당일출금 | check.당일출금 | 당일출금 | checkbox | 당일 출금 |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 649-944254-31189 |
| check.예금종류2 | check.예금종류2 | 예금종류 | checkbox | CMA |
| account2 | account2 | 계좌번호 | account_no | 000-287736-52424 |
| 인출금액 | 인출금액 | 인출금액 | number | 24,220,000원 |
| check.이체방법 | check.이체방법 | 이체방법 | checkbox | 전금 |
| 목록[].은행명 | 목록[].은행명 | 은행명 | text | 우리은행 |
| check.인출방법 | check.인출방법 | 인출방법 | checkbox | 할인식 |
| 목록[].금액 | 목록[].금액 | 금액 | number | 221,400,000 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인(예금주) | text | 박찬연 |
| seal.signer | seal.customer | 신청인(예금주) | seal | 현예지 |
| sign.signer | sign.customer | 신청인(예금주) | signature | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 최은유 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 백도정 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 박민아 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 반철린 |

### hf018 · 본인계좌 일괄지급정지 조회신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.18 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 신청인 | text | 박찬연 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.birth | customer.birth | 생년월일 | date | 900210 |
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| check.금융기관별조회 | check.금융기관별조회 | ■금융기관별조회(※요청기관V체크) | checkbox | 시티 |
| check.수령함 | check.수령함 | 수령함 | checkbox | 수령함 |
| customer.name2 | customer.name2 | 신청인성명 | text | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 확인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 추철윤 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 송선서 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김규빈 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 확인 |
| 서비스신청일로부터5년까지 | 서비스신청일로부터5년까지 | -서비스신청일로부터5년까지 | text |  |
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 현예지 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| 고객상담분쟁조정및민원처리 | 고객상담분쟁조정및민원처리 | -고객상담,분쟁조정및민원처리 | text |  |
| 성명연락처 | 성명연락처 | 성명,연락처 | phone | 010-5907-7253 |

### hf019 · 본인계좌 일괄지급정지(해제)신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.19 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].개설기관명 | 목록[].개설기관명 | 개설기관명 | text | 국민은행 |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 857-873265-13818 |
| customer.name | customer.name | 이름 | text | 박찬연 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| 지급정지시 | 지급정지시 | 지급정지시 | text |  |
| 지급정지해제시 | 지급정지해제시 | 지급정지해제시 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 검인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 확인 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 강하영 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김찬혜 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 엄하진 |

### hf020 · 노무비닷컴계좌 개설 및 지급이체서비스 이용 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.20 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| employer.department | employer.department | 부서 | text | 구매팀 |
| TEL | TEL | TEL | text |  |
| company.biz_no | corp.biz_no | 사업자번호 | biz_no | 264-82-36559 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| FAX | FAX | FAX | phone | 043-783-2775 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| customer.name2 | customer.name2 | 예금주 | text | 박찬연 |
| 원청기업사업자번호 | 원청기업사업자번호 | 원청기업사업자번호 | biz_no | 264-82-36559 |
| 원청기업명 | 원청기업명 | 원청기업명 | text | 다온로지스 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | (신청인)신청기업명 | text | (주)유니온무역 |
| seal.signer | seal.corp | (신청인)신청기업명 | seal | (주)삼정전자 |
| sign.signer | sign.customer | (신청인)신청기업명 | signature | (주)유니온무역 |
| 청구서류 | 청구서류 | 청구서류 | text |  |
| 사업자등록증대표자실명확인증표 | 사업자등록증대표자실명확인증표 | 사업자등록증,대표자실명확인증표 | text |  |
| 개인사업자 | 개인사업자 | 개인사업자 | text |  |

### hf021 · 일괄처리(지급)요청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.21 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.현금 | check.현금 | 현금 | checkbox | 이체 (수수료차감 후 입금) |
| check.현금2 | check.현금2 | 현금 | checkbox | 이체 |
| check.현금3 | check.현금3 | 현금 | checkbox | 이체 |
| check.현금4 | check.현금4 | 현금 | checkbox | 현금 |
| check.현금5 | check.현금5 | 현금 | checkbox | 대체 |
| check.현금6 | check.현금6 | 현금 | checkbox | 현금 |
| check.현금7 | check.현금7 | 현금 | checkbox | 이체 |
| check.현금8 | check.현금8 | 현금 | checkbox | 이체 |
| check.현금9 | check.현금9 | 현금 | checkbox | 이체 |
| check.현금10 | check.현금10 | 현금 | checkbox | 대체 |
| 목록[].거래금액 | 목록[].거래금액 | 거래금액(원) | text | 70,000 |
| check.수수료 | check.수수료 | 수수료 | checkbox | 대체(계좌출금) |
| 목록[].지급적요 | 목록[].지급적요 | 지급적요 | text |  |
| 목록[].입금은행 | 목록[].입금은행 | 입금은행 | text | 하나은행 |
| 목록[].입금계좌번호 | 목록[].입금계좌번호 | 입금계좌번호 | text | 319-359450-84249 |
| 목록[].수취인명 | 목록[].수취인명 | 수취인명 | text | 주식회사 미래전자 |
| 목록[].입금적요 | 목록[].입금적요 | 입금적요 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 현예지 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 박정태 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 전선유 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 검인 |

### hf023 · 하도급협력대금통장(상생결제 노무비) 지급이체서비스 이용신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.23 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 업체명 | text | (주)유니온무역 |
| customer.zipcode | customer.zipcode | 우편번호 | number | 06931 |
| employer.department | employer.department | 부서 | text | 구매팀 |
| TEL | TEL | TEL | text |  |
| company.biz_no | corp.biz_no | 사업자번호 | biz_no | 264-82-36559 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| FAX | FAX | FAX | phone | 010-5907-7253 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| customer.name2 | customer.name2 | 예금주 | text | 박찬연 |
| 비고 | 비고 | 비고 | text | 학비 송금, 4,000,000원 정도 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | (신청인)신청기관명 | text | (주)유니온무역 |
| seal.signer | seal.corp | (신청인)신청기관명 | seal | (주)유니온무역 |
| sign.signer | sign.customer | (신청인)신청기관명 | signature | (주)다온커뮤니케이션 |

### hf024 · 금융거래정보제공(요구·동의)서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.24 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.구분 | check.구분 | 구분 | checkbox | 동의 |
| check.신청항목 | check.신청항목 | 신청항목 | checkbox | 거래내역 조회 |
| check.신청항목2 | check.신청항목2 | 신청항목 | checkbox | 한도조회 및 |
| check.신청항목3 | check.신청항목3 | 신청항목 | checkbox | 기타 조회 |
| check.전금융기관한도및중복가입 | check.전금융기관한도및중복가입 | 전금융기관한도및중복가입제한상품 | checkbox | 전 금융기관 한도 및 중복가입 제한 상품 |
| check.금융거래종합보고서 | check.금융거래종합보고서 | 금융거래종합보고서 | checkbox | 기타 ( |
| check.계좌번호 | check.계좌번호 | 계좌번호 | checkbox | 전체 |
| check.대상기간 | check.대상기간 | 대상기간 | checkbox | 최근 6개월 |
| check.대상기간2 | check.대상기간2 | 대상기간 | checkbox | 기타 ( |
| check.신청추가 | check.신청추가 | 신청추가 | checkbox | 추가요청사항 |
| check.신청추가2 | check.신청추가2 | 신청추가 | checkbox | 수수료 출금동의 |
| check.계좌번호마스킹제외 | check.계좌번호마스킹제외 | 계좌번호마스킹제외 | checkbox | 부기명 표시 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| 출금금액 | 출금금액 | 출금금액 | number | 100,000 |
| 거래정보등의제공목적 | 거래정보등의제공목적 | 거래정보등의제공목적 | text | 급여 수령 |
| check.동의서유효기간 | check.동의서유효기간 | 동의서유효기간 | checkbox | 작성일로부터 ( |
| check.정보제공사실의통보여부 | check.정보제공사실의통보여부 | 정보제공사실의통보여부 | checkbox | 통보 요청 |
| customer.name | customer.name | 성명(사업자명) | text | 박찬연 |
| customer.birth | customer.birth | 생년월일(사업자번호) | date | 900210 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| signer.name | signer.name | 성명(사업자명) | text | 박찬연 |
| seal.signer | seal.customer | 성명(사업자명) | seal | 이욱유 |
| sign.signer | sign.customer | 성명(사업자명) | signature | 박찬연 |
| customer.phone2 | customer.phone2 | 연락처 | phone | 010-5907-7253 |
| customer.birth2 | customer.birth2 | 생년월일(사업자번호) | date | 900210 |
| 반출신청email | 반출신청email | 반출신청e-mail | text |  |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| signer2.name | signer2.name | 예금주 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 예금주 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 예금주 | signature | 강순준 |
| check.대리인을통하여금융거래정보제공을요청하는경우 | check.대리인을통하여금융거래정보제공을요청하는경우 | 대리인을통하여금융거래정보제공을요청하는경우 | checkbox | 요구에 체크 표시한 후 금융거래자 본인란을 기재한다. |
| check.본인이제3자앞정보제공에동의하는경우 | check.본인이제3자앞정보제공에동의하는경우 | 본인이제3자앞정보제공에동의하는경우 | checkbox | 동의에 체크 표시한 후 금융거래정보 등의 제공 동의시 기재사항을 기재하고 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 정철린 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 최민진 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 고다인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이숙현 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 정서유 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 전민지 |

### hf025 · 대여금고(신규·변경·해지)신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.25 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 금고번호 | 금고번호 | 금고번호 | text | 0066-0927 |
| 보증금 | 보증금 | 보증금 | number | 9,600,000 |
| 원 | 원 | 원 | text |  |
| signer.name | signer.name | 성명 | text | 박찬연 |
| seal.signer | seal.customer | 성명 | seal | 이민빈 |
| sign.signer | sign.customer | 성명 | signature | 박찬연 |
| agent.birth | agent.birth | 생년월일 | date | 1962.12.19 |
| agent.phone | agent.phone | 연락처 | phone | 010-6515-4769 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.relation | agent.relation | 관계 | text | 부 |
| signer2.name | signer2.name | 성명 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 성명 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 성명 | signature | 이욱유 |
| agent.birth2 | agent.birth2 | 생년월일 | date | 1962.12.19 |
| agent.phone2 | agent.phone2 | 연락처 | phone | 010-6515-4769 |
| agent.address2 | agent.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.relation2 | agent.relation2 | 관계 | text | 부 |
| customer.name | customer.name | 성명(사업자명) | text | 박찬연 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer3.name | signer3.name | 성명(사업자명) | text | 박찬연 |
| seal.signer3 | seal.signer3 | 성명(사업자명) | seal | 박찬연 |
| sign.signer3 | sign.signer3 | 성명(사업자명) | signature | 현예지 |
| customer.birth | customer.birth | 생년월일(사업자번호) | date | 900210 |
| customer.email | customer.email | e-mail | text | chanyeon363@naver.com |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 검인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 확인 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 하도원 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김나은 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 홍은혜 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 위유도 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 검인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 검인 |

### hf026 · [필수]개인(신용)정보 제3자 제공동의서(하나미소드림적금가입자용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.26 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 현예지 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 김순우 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 김순우 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 박원영 |
| 이용목적 | 이용목적 | 이용목적 | text | 만기 해지 |
| 계좌번호거래일입금금액 | 계좌번호거래일입금금액 | 계좌번호,거래일,입금금액 | number | 8,380,000 |

### hf027 · 위임장(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.27 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.Pleasetickintherelevantbox | check.Pleasetickintherelevantbox | Pleasetick√intherelevantbox | checkbox | . |
| agent.name_en | agent.name_en | Name | text | PARK YOUNGJUN |
| agent.relation_en | agent.relation_en | RelationshiptoPrincipal | text | Spouse |
| agent.address | agent.address | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.AccountOpening | check.AccountOpening | AccountOpening | checkbox | Savings Deposit |
| account | account | AccountNo. | account_no | 000-287736-52424 |
| check.Details | check.Details | Details | checkbox | Change of password |
| poa.other_powers_en | poa.other_powers_en | Others | text | Inquiry of account balance and transaction history |
| agent.birth | agent.birth | DateofBirth | date | 1962.12.19 |
| agent.phone | agent.phone | ContactInformation | phone | 010-6515-4769 |
| bank.confirm_date | bank.confirm_date | DateofConfirmingPowersGiven | date | 2025.09.11 |
| customer.name_en | customer.name_en | Name | text | PARK CHANYEON |
| customer.address | customer.address | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone | customer.phone | ContactInformation | phone | 010-5907-7253 |
| bank.branch | bank.branch | HanaBank___Branch | text | 범어지점 |
| date | date | Date(MM-DD-YYYY) | date | 2026년 01월 31일 |
| customer.birth | customer.birth | PrincipalDateofBirth | date | 1990-02-10 |

### hf028 · 위임장

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.28 (예금) 원본 위에 기재

연결 업무: 퇴직급여 수령 (retirement_payout)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.해당 | check.해당 | 해당 | checkbox | 에 √ 표시하며 기타의 경우 구체적인 위임내용을 기재합니다 |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.신규계좌개설 | check.신규계좌개설 | 신규계좌개설 | checkbox | 적금 |
| check.신규계좌개설2 | check.신규계좌개설2 | 신규계좌개설 | checkbox | 개인(신용)정보 수집 이용 및 제공 동의서(상품서비스 안내 등) 작성 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| check.세부내용 | check.세부내용 | 세부내용 | checkbox | 비밀번호 변경 |
| 기타사항 | 기타사항 | 기타사항 | text | 서류 챙겨서 5일 뒤 재방문 |
| agent.birth | agent.birth | 생년월일 | date | 1962년 12월 19일 |
| agent.phone | agent.phone | 연락처 | phone | 010-6515-4769 |
| 위임내용확인일시 | 위임내용확인일시 | 위임내용확인일시 | text |  |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer.name | signer.name | 성명(업체명) | text | 박찬연 |
| seal.signer | seal.customer | 성명(업체명) | seal | 현예지 |
| sign.signer | sign.customer | 성명(업체명) | signature | 박찬연 |
| customer.birth | customer.birth | 생년월일(사업자번호) | date | 900210 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 최진찬 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이윤도 |

연결 업무 retirement_payout · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### hf029 · 사용인감계(금융계좌개설용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.29 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| seal.signer | seal.customer | 사용인감 | seal | 강순준 |
| sign.signer | sign.customer | 사용인감 | signature | 박찬연 |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.phone | agent.phone | 연락처(선택항목) | phone | 010-6515-4769 |
| agent.address | agent.address | 주소(선택항목) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.birth | agent.birth | 생년월일 | date | 1962.12.19 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| company.name | corp.name | 법인명 | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| customer.address | customer.address | 주소(선택항목) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.ceo | corp.ceo | 대표자명 | text | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 최지영 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이숙아 |

### hf030 · 국내원천소득 제한세율 적용신청서(외국법인용-영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.30 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| FilingNo | FilingNo | FilingNo. | text | 078596-7940688 |
| ApplicantInformation | ApplicantInformation | ApplicantInformation | text | (주)유니온무역 |
| NameofCorporation | NameofCorporation | NameofCorporation | text |  |
| NameofRepresentative | NameofRepresentative | NameofRepresentative | text |  |
| TaxpayerIdentificationNo | TaxpayerIdentificationNo | TaxpayerIdentificationNo. | text | 933-754746-82806 |
| DateofIncorporation | DateofIncorporation | DateofIncorporation | date | 2025.01.21 |
| FilingDate | FilingDate | FilingDate | date | 2025.01.04 |
| customer.address | customer.address | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.address2 | customer.address2 | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| CountryofResidence | CountryofResidence | CountryofResidence | text | 싱가포르 |
| CountryCode | CountryCode | CountryCode | text | 미국 |
| TelephoneNumber | TelephoneNumber | TelephoneNumber | phone | 010-5907-7253 |
| AddressorLocation | AddressorLocation | AddressorLocation | text |  |
| To | To | To | text |  |
| Type | Type | Type | text |  |
| TaxAdministrator | TaxAdministrator | []TaxAdministrator | text |  |
| Other | Other | []Other | text |  |

### hf031 · 국내원천소득 제한세율 적용신청서(외국법인용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.31 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 법인명 | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자성명 | text | 박찬연 |
| 납세자번호 | 납세자번호 | 납세자번호 | text | 370597-5598113 |
| 설립년월일 | 설립년월일 | 설립년월일 | date | 2025년 3월 1일 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 거주지국 | 거주지국 | 거주지국 | text |  |
| 국가코드 | 국가코드 | 국가코드 | number | 44251 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| 거주지국의세법상납세의무가있습니까 | 거주지국의세법상납세의무가있습니까 | 거주지국의세법상납세의무가있습니까? | text |  |
| 지급받는국내원천소득의실질귀속자입니까 | 지급받는국내원천소득의실질귀속자입니까 | 지급받는국내원천소득의실질귀속자입니까? | number | 6,240,000 |
| 목록[].예 | 목록[].예 | 예 | text |  |
| 거주지국의세법상납세의무가있습니까2 | 거주지국의세법상납세의무가있습니까2 | 거주지국의세법상납세의무가있습니까? | text |  |
| 지급받는국내원천소득의실질귀속자입니까2 | 지급받는국내원천소득의실질귀속자입니까2 | 지급받는국내원천소득의실질귀속자입니까? | number | 1,540,000 |
| 목록[].아니오 | 목록[].아니오 | 아니오 | text |  |
| 주소또는소재지 | 주소또는소재지 | 주소또는소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 성명또는법인명 | 성명또는법인명 | 성명또는법인명 | text | (주)미래정밀 |
| company.biz_no | corp.biz_no | 사업자(주민)등록번호 | biz_no | 264-82-36559 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인(대표자) | text | 박찬연 |
| seal.signer | seal.customer | 신청인(대표자) | seal | 강순준 |
| sign.signer | sign.customer | 신청인(대표자) | signature | 이민빈 |
| 법인연금기금 | 법인연금기금 | []법인,[]연금,[]기금, | text |  |

### hf032 · 국내원천소득 제한세율 적용신청서(비거주자용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.32 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 납세자번호 | 납세자번호 | 납세자번호 | text | 2908-6211 |
| 거주지국 | 거주지국 | 거주지국 | text |  |
| value | value | (거주지전화)(국내전화) | amount |  |
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| 거주지국코드 | 거주지국코드 | 거주지국코드 | number | 890147 |
| 가국내에주소를두고있습니까 | 가국내에주소를두고있습니까 | 가국내에주소를두고있습니까? | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 나국내에계속하여183일이상거주하고있습니까 | 나국내에계속하여183일이상거주하고있습니까 | 나국내에계속하여183일이상거주하고있습니까? | text |  |
| 바대한민국의공무원입니까 | 바대한민국의공무원입니까 | 바대한민국의공무원입니까? | text |  |
| 가국내에주소를두고있습니까2 | 가국내에주소를두고있습니까2 | 가국내에주소를두고있습니까? | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 나국내에계속하여183일이상거주하고있습니까2 | 나국내에계속하여183일이상거주하고있습니까2 | 나국내에계속하여183일이상거주하고있습니까? | text |  |
| 다최근1년동안국내에체재한날이183일이상입니까 | 다최근1년동안국내에체재한날이183일이상입니까 | 다최근1년동안국내에체재한날이183일이상입니까? | text |  |
| 목록[].예 | 목록[].예 | 예 | text |  |
| 마국내에계속하여183일이상거주할것을필요로하는직업이있습니까 | 마국내에계속하여183일이상거주할것을필요로하는직업이있습니까 | 마국내에계속하여183일이상거주할것을필요로하는직업이있습니까? | text |  |
| 바대한민국의공무원입니까2 | 바대한민국의공무원입니까2 | 바대한민국의공무원입니까? | text |  |
| 목록[].아니오 | 목록[].아니오 | 아니오 | text |  |
| 주소또는소재지 | 주소또는소재지 | 주소또는소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 성명또는법인명 | 성명또는법인명 | 성명또는법인명 | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자(주민)등록번호 | biz_no | 264-82-36559 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 강순준 |
| signer2.name | signer2.name | 고객명 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 고객명 | seal | 강순준 |
| sign.signer2 | sign.signer2 | 고객명 | signature | 박찬연 |

### hf033 · 국내원천소득 제한세율 적용신청서(비거주자용-영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.33 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| FilingNo | FilingNo | FilingNo. | text | 544-576943-50555 |
| FilingDate | FilingDate | FilingDate | date | 2025.10.10 |
| TaxpayerIdentificationNo | TaxpayerIdentificationNo | TaxpayerIdentificationNo. | text | 9780-8005 |
| CountryofResidence | CountryofResidence | CountryofResidence | text | 캐나다 |
| customer.birth | customer.birth | DateofBirth | date | 1990.02.10 |
| CountryCode | CountryCode | CountryCode | text | 필리핀 |
| 목록[].Yes | 목록[].Yes | Yes | text |  |
| 목록[].No | 목록[].No | No | text | 414-220666-66571 |
| AddressorLocation | AddressorLocation | AddressorLocation | text |  |
| NameofIndividualorCorporation | NameofIndividualorCorporation | NameofIndividualorCorporation | text |  |
| Applicant | Applicant | Applicant | text | (주)유니온무역 |

### hf034 · 확인서(잔액통보생략용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.34 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 감사통할 | 감사통할 | 감사통할 | text |  |
| 영업점장 | 영업점장 | 영업점장 | text |  |
| 목록[].예금종별 | 목록[].예금종별 | 예금종별 | text | 청년도약계좌 |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 171-749568-37605 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 예금주 | text | 박찬연 |
| seal.signer | seal.customer | 예금주 | seal | 강순준 |
| sign.signer | sign.customer | 예금주 | signature | 박찬연 |

### hf035 · 수표·어음용지 폐기신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.35 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 기호및번호 | 기호및번호 | 기호및번호 | text | 259-424231-88167 |
| 수령일자 | 수령일자 | 수령일자 | date | 2025년 8월 14일 |
| 폐기일자 | 폐기일자 | 폐기일자 | date | 2025.09.11 |
| 폐기경위 | 폐기경위 | 폐기경위 | text |  |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| signer.name | customer.name | 명 | text | 박찬연 |
| seal.signer | seal.customer | 명 | seal | 김소윤 |
| sign.signer | sign.customer | 명 | signature | 현예지 |
| customer.birth | customer.birth | 생년월일(사업자등록번호) | date | 1990-02-10 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 검인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 박채혜 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 정순지 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 우영재 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 검인 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 검인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 확인 |

### hf036 · 예금(신탁) 이관 의뢰서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.36 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 예금종류 | 예금종류 | 예금(신탁)종류 | text | 급여하나 통장 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| customer.name | customer.name | 예금주(위탁자) | text | 박찬연 |
| 예금잔액 | 예금잔액 | 예금(신탁)잔액 | number | 44,990,000원 |
| 현취급점명 | 현취급점명 | 현취급점명 | text | 범어지점 |
| 비고 | 비고 | 비고 | text | 서류 챙겨서 다음 달 초 재방문 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 명 | text | 박찬연 |
| seal.signer | seal.customer | 명 | seal | 박찬연 |
| sign.signer | sign.customer | 명 | signature | 위나아 |
| signer2.name | signer2.name | 명 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 명 | seal | 강순준 |
| sign.signer2 | sign.signer2 | 명 | signature | 박찬연 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| seal.signer3 | seal.signer3 | 지점 | seal | 이연율 |
| sign.signer3 | sign.signer3 | 지점 | signature | 최은태 |
| 이관점기재란 | 이관점기재란 | 이관점기재란 | text |  |
| 이관서류목록 | 이관서류목록 | 이관서류목록 | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 왕영윤 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 왕연혜 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 오동찬 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 검인 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 검인 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 검인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 배소하 |
| seal.staff.담당2 | seal.staff.담당2 | 담당 | seal | 확인 |
| sign.staff.담당2 | sign.staff.담당2 | 담당 | signature | 제갈호율 |
| seal.staff.책임자2 | seal.staff.책임자2 | 책임자 | seal | 김수재 |
| sign.staff.책임자2 | sign.staff.책임자2 | 책임자 | signature | 박철민 |
| seal.staff.관리자2 | seal.staff.관리자2 | 관리자 | seal | 조승린 |
| sign.staff.관리자2 | sign.staff.관리자2 | 관리자 | signature | 정수승 |
| seal.staff.부점장2 | seal.staff.부점장2 | 부점장 | seal | 성채연 |
| sign.staff.부점장2 | sign.staff.부점장2 | 부점장 | signature | 김호도 |

### hf037 · 위탁유가증권 반환청구서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.37 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 유가증권수탁통장번호 | 유가증권수탁통장번호 | 유가증권수탁통장번호 | text | 2281-9827 |
| 목록[].위탁일자 | 목록[].위탁일자 | 위탁일자 | text | 2025.06.27 |
| 목록[].수탁번호 | 목록[].수탁번호 | 수탁번호 | text | 133-316554-47617 |
| 목록[].종류 | 목록[].종류 | 종류 | text | 급여하나 통장 |
| 목록[].증서어음번호 | 목록[].증서어음번호 | 증서【어음】번호 | text | 라다42187716 |
| 목록[].지급지 | 목록[].지급지 | 지급지 | text | 범어지점 |
| 목록[].발행인 | 목록[].발행인 | 발행인 | text | 유니온무역 |
| 목록[].만기일 | 목록[].만기일 | 만기일 | text | 2029년 3월 1일 |
| 목록[].금액 | 목록[].금액 | 금액 | text | 2,580,000 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 명 | text | 박찬연 |
| seal.signer | seal.customer | 명 | seal | 현예지 |
| sign.signer | sign.customer | 명 | signature | 박찬연 |
| customer.birth | customer.birth | 생년월일(사업자등록번호) | date | 1990-02-10 |
| customer.phone | customer.phone | 전화번호(선택항목) | phone | 010-5907-7253 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 성명 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 성명 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 성명 | signature | 강순준 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김희하 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 최환경 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 원우혜 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이형정 |

### hf038 · 수표(어음)발행사실 확인의뢰서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.38 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].수표어음 | 목록[].수표어음 | 수표어음 | text | 가계수표 |
| 목록[].번호 | 목록[].번호 | 번호 | text | 975405-1428869 |
| 목록[].발행일 | 목록[].발행일 | 발행일 | text | 2025년 7월 30일 |
| 목록[].지급일 | 목록[].지급일 | 지급일 | text | 2025.06.08 |
| 목록[].금액 | 목록[].금액 | 금액 | text | 289,650,000 |
| 목록[].수취인 | 목록[].수취인 | 수취인 | text | 제일메디칼 |
| 목록[].용도 | 목록[].용도 | 용도 | text | 자녀 교육비 |
| 목록[].확인여부 | 목록[].확인여부 | 확인여부(결제일등) | text |  |
| 목록[].담당자인 | 목록[].담당자인 | 담당자인 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 상호및대표자 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자 | seal | 박찬연 |
| sign.signer | sign.customer | 상호및대표자 | signature | 강순준 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 천승인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 확인 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 진옥아 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 정희아 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 석정율 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 기영수 |

### hf039 · 유가증권 수탁약정서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.39 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 신청인성명(예금주) | text | 박찬연 |
| 추심대전입금계좌번호 | 추심대전입금계좌번호 | 추심대전입금계좌번호 | text | 786-576266-92119 |
| check.주소 | check.주소 | 주소(선택또는전부기재) | checkbox | 직장 |
| check.연락처 | check.연락처 | 연락처(선택또는전부기재) | checkbox | 자택 |
| seal.signer | seal.customer | 거래인감(또는서명) | seal | 이욱유 |
| sign.signer | sign.customer | 거래인감(또는서명) | signature | 박찬연 |
| customer.birth | customer.birth | 생년월일(사업자등록번호) | date | 1990.02.10 |
| check.보관어음월별잔고현황통지여부 | check.보관어음월별잔고현황통지여부 | 보관어음월별잔고현황통지여부 | checkbox | E-MAIL |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 왕수준 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 김혜은 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 배상진 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김도원 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 선우훈원 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 남채성 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 원건진 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 송우경 |

### hf041 · 사고신고 담보금 지급정지가처분담보금 처리를 위한 약정서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.41 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 명 | text | 박찬연 |
| seal.signer | seal.customer | 명 | seal | 박찬연 |
| sign.signer | sign.customer | 명 | signature | 이욱유 |
| seal.signer2 | seal.signer2 | 지점 | seal | 이재인 |
| sign.signer2 | sign.signer2 | 지점 | signature | 김순희 |

### hf042 · 사채원리금 지급대행 계약서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.42 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 사채의명칭 | 사채의명칭 | 사채의명칭 | text | 청솔테크 |
| 사채의종류 | 사채의종류 | 사채의종류 | text |  |
| 사채의전자등록총액 | 사채의전자등록총액 | 사채의전자등록총액 | number | 84,070,000 |
| 사채의발행가액 | 사채의발행가액 | 사채의발행가액 | number | 114,350,000 |
| 사채의발행가액총액 | 사채의발행가액총액 | 사채의발행가액총액 | number | 44,600,000 |
| 사채의거래단위 | 사채의거래단위 | 사채의거래단위 | text |  |
| 사채의이율 | 사채의이율 | 사채의이율 | number | 3.44 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 이자지급기일 | 이자지급기일 | 이자지급기일 | date | 2026.05.19 |
| 연체이자 | 연체이자 | 연체이자 | number | 60,450,000 |
| 사채관리회사 | 사채관리회사 | 사채관리회사 | text |  |
| 기타 | 기타 | 기타 | text | 환전 50,000,000원, 여행 경비 |
| 목록[].예금주 | 목록[].예금주 | 예금주 | text |  |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 343-445601-24898 |
| 담당자성명 | 담당자성명 | 담당자성명 | text | 박경현 |
| customer.phone | customer.phone | 핸드폰번호(SMS교환안내수신번호) | phone | 010-5907-7253 |
| 회사전화번호 | 회사전화번호 | 회사전화번호 | phone | 043-783-2775 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer.name | corp.ceo | 대표이사 | text | 박찬연 |
| seal.signer | seal.corp | 대표이사 | seal | 박찬연 |
| sign.signer | sign.customer | 대표이사 | signature | 강순준 |
| signer2.name | signer2.name | 지점지점장 | text | 함예재 |
| seal.signer2 | seal.signer2 | 지점지점장 | seal | 염소영 |
| sign.signer2 | sign.signer2 | 지점지점장 | signature | 함예재 |

### hf043 · 세금우대종합저축(비과세저축) 제변경신고서(비과세공용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.43 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 예금신탁종류 | 예금신탁종류 | 예금/신탁종류 | text |  |
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 장애인 해제 |
| 한도설정 | 한도설정 | 한도설정 | number | 5,750,000 |
| 한도증액 | 한도증액 | 한도증액 | number | 28,210,000원 |
| 한도감액 | 한도감액 | 한도감액 | number | 49,560,000원 |
| 상속인등록 | 상속인등록 | 상속인등록 | text |  |
| 기타 | 기타 | 기타 | text | 해당 없음 |
| signer.name | customer.name | 성명 | text | 박찬연 |
| seal.signer | seal.customer | 성명 | seal | 이욱유 |
| sign.signer | sign.customer | 성명 | signature | 강순준 |
| customer.address | customer.address | 주소(선택항목) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer2.name | signer2.name | 성명 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 성명 | seal | 이민빈 |
| sign.signer2 | sign.signer2 | 성명 | signature | 박찬연 |
| customer.address2 | customer.address2 | 주소(선택항목) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| 목록[].변경후 | 목록[].변경후 | 변경후 | text | 해당 없음 |
| customer.birth | customer.birth | 생년월일 | date | 900210 |
| customer.birth2 | customer.birth2 | 생년월일 | date | 900210 |
| check.한도설정 | check.한도설정 | 한도설정 | checkbox | 한도증액 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 한소인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 박선호 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 한용예 |

### hf044 · 예금(신탁) 양도승낙 의뢰서 및 양도승낙서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.44 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 예금주(양도인)(위탁자겸수익자) | text | 박찬연 |
| deposit.product | deposit.product | 예금(신탁)종별 | text | 청년도약계좌 |
| deposit.amount | deposit.amount | 금액 | amount | 4,780,000 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| deposit.due_date | deposit.due_date | 만기일 | date | 2025.04.29 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 명 | text | 박찬연 |
| seal.signer | seal.customer | 명 | seal | 현예지 |
| sign.signer | sign.customer | 명 | signature | 박찬연 |
| signer2.name | signer2.name | 명 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 명 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 명 | signature | 강순준 |
| date3 | date3 | 작성일(년월일) | date | 2026.01.31 |
| customer.address | customer.address | 양도인주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.birth2 | customer.birth2 | 양도인생년월일(사업자등록번호) | date | 1990.02.10 |
| customer.name2 | customer.name2 | 양도인성명 | text | 박찬연 |
| related.address | related.address | 양수인주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| related.birth2 | related.birth2 | 양수인생년월일(사업자등록번호) | date | 2025.01.28 |
| related.name | related.name | 양수인성명 | text | 배숙정 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 박순은 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 천기빈 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 최다유 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 서순진 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 정민재 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 확인 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 확인 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 확인 |
| deposit.product2 | deposit.product2 | 예금(신탁)종별 | text | 하나의정기예금 |
| deposit.amount2 | deposit.amount2 | 금액 | amount | 2,220,000 |
| account2 | account2 | 계좌번호 | account_no | 000-287736-52424 |
| deposit.due_date2 | deposit.due_date2 | 만기일 | date | 2026.01.09 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| seal.signer3 | seal.signer3 | 부점장 | seal | 한환은 |
| sign.signer3 | sign.signer3 | 부점장 | signature | 길건재 |
| customer.birth | customer.birth | 생년월일(사업자등록번호) | date | 1990.02.10 |
| related.birth | related.birth | 생년월일(사업자등록번호) | date | 2025.03.22 |
| related.name2 | related.name2 | 양수인귀하 | text | 배숙정 |
| customer.name3 | customer.name3 | 양도인성명(상호) | text | 박찬연 |
| related.name3 | related.name3 | 양수인성명(상호) | text | 배숙정 |
| date4 | date4 | 승낙일(년월일) | date | 2026.01.31 |
| seal.staff.담당2 | seal.staff.담당2 | 담당 | seal | 확인 |
| sign.staff.담당2 | sign.staff.담당2 | 담당 | signature | 천기빈 |
| seal.staff.책임자2 | seal.staff.책임자2 | 책임자 | seal | 서순진 |
| sign.staff.책임자2 | sign.staff.책임자2 | 책임자 | signature | 최나인 |
| seal.staff.관리자2 | seal.staff.관리자2 | 관리자 | seal | 검인 |
| sign.staff.관리자2 | sign.staff.관리자2 | 관리자 | signature | 윤영희 |
| seal.staff.부점장2 | seal.staff.부점장2 | 부점장 | seal | 함도희 |
| sign.staff.부점장2 | sign.staff.부점장2 | 부점장 | signature | 남규재 |

### hf045 · 야간금고입금의뢰서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.45 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 만원권 | 만원권 | 만원권 | number | 24 |
| 천원권 | 천원권 | 천원권 | number | 60 |
| 천원권2 | 천원권2 | 천원권 | number | 24 |
| 원 | 원 | 원 | number | 24 |
| 원2 | 원2 | 원 | number | 12 |
| 원3 | 원3 | 원 | number | 36 |
| 원4 | 원4 | 원 | number | 36 |
| 소계 | 소계 | 소계(A) | number | 4,870,000원 |
| 매 | 매 | 매 | number | 38,750,000원 |
| 매2 | 매2 | 매 | number | 187,840,000 |
| 매3 | 매3 | 매 | number | 131,170,000원 |
| 개 | 개 | 개 | number | 90,000 |
| 개2 | 개2 | 개 | number | 6,230,000 |
| 개3 | 개3 | 개 | number | 16,380,000 |
| 개4 | 개4 | 개 | number | 9,670,000 |
| 약속어음 | 약속어음 | 약속어음 | text |  |
| 당점권 | 당점권 | 당점권 | number | 6 |
| 자기앞수표 | 자기앞수표 | 자기앞수표 | number | 12 |
| 송금수표 | 송금수표 | 송금수표 | number | 24 |
| 당좌수표 | 당좌수표 | 당좌수표 | number | 12 |
| 가계수표 | 가계수표 | 가계수표 | number | 2 |
| 약속어음2 | 약속어음2 | 약속어음 | number | 2 |
| 매4 | 매4 | 매 | number | 6 |
| 소계2 | 소계2 | 소계(B) | number | 93,610,000원 |
| 총계 | 총계 | 총계(A+B) | number | 3,810,000원 |
| 매5 | 매5 | 매 | number | 9,120,000원 |
| 매6 | 매6 | 매 | number | 16,280,000 |
| 매7 | 매7 | 매 | number | 184,110,000 |
| 매8 | 매8 | 매 | number | 8,670,000 |
| 매9 | 매9 | 매 | number | 2,830,000 |
| 매10 | 매10 | 매 | number | 8,720,000 |
| 매11 | 매11 | 매 | number | 42,050,000원 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| 예금과목 | 예금과목 | 예금과목 | text | 하나 적금 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| signer.name | signer.name | 의뢰인성명 | text | 박찬연 |
| seal.signer | seal.customer | 의뢰인성명 | seal | 이욱유 |
| sign.signer | sign.customer | 의뢰인성명 | signature | 강순준 |
| 원整 | 원整 | 원整 | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 진규지 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 제갈건인 |
| 목록[].수표종류 | 목록[].수표종류 | 수표종류 | text | 약속어음 |
| 목록[].지급은행 | 목록[].지급은행 | 지급은행 | text | 하나은행 |
| 목록[].수표번호 | 목록[].수표번호 | 수표번호 | text | 사바21877925 |
| 목록[].발행일자 | 목록[].발행일자 | 발행일자 | text | 2025년 1월 1일 |
| 목록[].지급일자 | 목록[].지급일자 | 지급일자 | text | 2025-04-21 |
| 목록[].발행인 | 목록[].발행인 | 발행인 | text | (주)유니온무역 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |

### hf046 · 목돈을 불리는 통장 거래신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.46 (예금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| 자택 | 자택 | 자택 | text |  |
| employer.name | employer.name | 근무처 | text | 주식회사 태평양무역 |
| 모계좌계좌번호 | 모계좌계좌번호 | 모계좌(이체지정계좌)계좌번호 | text | 591-125619-52675 |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1****** |
| 통장번호 | 통장번호 | 통장번호 | text | 453985-7672989 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 박하예 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 장승진 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 차성경 |
| 목록[].일자 | 목록[].일자 | 일자 | text | 2025-10-23 |
| 목록[].내용 | 목록[].내용 | 내용 | text | 해당 없음 |
| date2 | date2 | 일자 | date | 2026.01.31 |
| seal.signer | seal.customer | 변경인감 | seal | 박찬연 |
| sign.signer | sign.customer | 변경인감 | signature | 이욱유 |

### hf199 · 외화송금신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.199 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 담당 | 담당 | 담당(실명확인) | text |  |
| check.송금방법 | check.송금방법 | 송금방법 | checkbox | 국내전신송금(ODT) |
| check.송금정보등록 | check.송금정보등록 | 송금정보등록 | checkbox | 해지 (NO. |
| 영문 | 영문 | 영문(English) | text |  |
| 국문 | 국문 | 국문(Korean) | text |  |
| customer.rrn | customer.rrn | 주민(사업자)번호(I.DNo./PassportNo.) | rrn | 900210-1659382 |
| 과거송금번호 | 과거송금번호 | 과거송금번호(EXISTINGREF.NO) | text | 384376-6761006 |
| check.결제은행수수료부담 | check.결제은행수수료부담 | 결제은행수수료부담(REIMBURSINGBANKCHG.) | checkbox | 수취인 (CRED - 수취인이 송금과 관련한 국내 , 국외 수수료 모두  |
| check.받으실분 | check.받으실분 | 받으실분(Beneficiary) | checkbox | HAPPY E-MAIL 서비스 신청 (무료) |
| 송금목적 | 송금목적 | 송금목적(송금사유)(PURPOSEOFPAYMENT) | text | 생활자금 |
| 적요 | 적요 | 적요(DETAILSOFPAYMENT) | text |  |
| 은행코드 | 은행코드 | 은행코드(SWIFTBIC) | number | 646772 |
| 은행명 | 은행명 | 은행명(BANKNAME) | text | 국민은행 |
| 은행명2 | 은행명2 | 은행명(BANKNAME) | text | 신한은행 |
| 통화금액 | 통화금액 | 통화(CURRENCY):금액(AMOUNT) | number | 790,000 |
| 은행코드2 | 은행코드2 | 은행코드(BANKCODE) | number | 63815 |
| 수취인계좌번호 | 수취인계좌번호 | 수취인계좌번호(BNF'sA/CNo.) | text | 152-554473-11908 |
| foreign.name | foreign.name | 성명(Name) | text | Mekong Garment JSC |
| 신청인과의관계 | 신청인과의관계 | 신청인과의관계(RELATIONTOAPPLICANT) | text |  |
| check.송금정보등록건송금결과통지 | check.송금정보등록건송금결과통지 | 송금정보등록건송금결과통지 | checkbox | SMS |
| check.통화금액 | check.통화금액 | 통화(CURRENCY):금액(AMOUNT) | checkbox | 수수료 별도납부 |
| 보내는분계좌번호 | 보내는분계좌번호 | 보내는분계좌번호(A/CNO) | text | 470-366422-58632 |
| check.수수료차감후송금 | check.수수료차감후송금 | 수수료차감후송금 | checkbox | 수수료차감후 송금 |
| 신청인과의관계2 | 신청인과의관계2 | 신청인과의관계(RELATIONTOAPPLICANT) | text |  |
| check.귀행을 | check.귀행을 | ●귀행을 | checkbox | 외국인 또는 비거주자의 국내보수 등을 위한 거래 외국환 은행으로 지정하고 |
| signer.name | customer.name | 예금주명(A/CHOLDERNAME) | text | 박찬연 |
| seal.signer | seal.customer | 예금주명(A/CHOLDERNAME) | seal | 위나아 |
| sign.signer | sign.customer | 예금주명(A/CHOLDERNAME) | signature | 강순준 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신청인(Applicant) | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신청인(Applicant) | seal | 강순준 |
| sign.signer2 | sign.signer2 | 신청인(Applicant) | signature | 박찬연 |
| signer3.name | agent.name | 대리인(Agent) | text | 박영준 |
| seal.signer3 | seal.agent | 대리인(Agent) | seal | 제갈찬율 |
| sign.signer3 | sign.agent | 대리인(Agent) | signature | 박영준 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| seal.signer4 | seal.signer4 | 지점장 | seal | 최상재 |
| sign.signer4 | sign.signer4 | 지점장 | signature | 변찬인 |
| 대리인실명번호 | 대리인실명번호 | 대리인실명번호(AGENTID.NO) | text | 655769-4049123 |
| check.자동화기기를이용한외화송금서비스신청 | check.자동화기기를이용한외화송금서비스신청 | ◈자동화기기를이용한외화송금서비스신청( | checkbox | 변경 |
| check.송금항목 | check.송금항목 | 송금항목 | checkbox | 거주자의 무증빙 해외송금 |
| check.송금항목2 | check.송금항목2 | 송금항목 | checkbox | 체재비 송금 |
| 인출계좌번호 | 인출계좌번호 | 인출계좌번호 | text | 429-508471-10085 |
| check.송금결과통보 | check.송금결과통보 | 송금결과통보 | checkbox | E-MAIL |
| check.유학생송금 | check.유학생송금 | 유학생송금 | checkbox | 유학생 송금 |
| check.외국인근로자의보수송금 | check.외국인근로자의보수송금 | 외국인근로자의보수송금 | checkbox | 외국인 근로자의 보수 송금 |
| check.국내전신송금 | check.국내전신송금 | 국내전신송금 | checkbox | 국내 전신 송금 |
| 사전송금방식국내통관전수입대금을지급 | 사전송금방식국내통관전수입대금을지급 | 사전송금방식:국내통관(물품인수)전수입대금을지급 | number | 1,930,000 |
| check.대금송금후물품수령예정일 | check.대금송금후물품수령예정일 | 대금송금후물품(선적서류)수령예정일 | checkbox | 년 이내 |
| check.대금송금후물품수령예정일2 | check.대금송금후물품수령예정일2 | 대금송금후물품(선적서류)수령예정일 | checkbox | 년 초과 ( |
| check.일반수입 | check.일반수입 | 일반수입 | checkbox | 일반 수입 |
| check.중계무역 | check.중계무역 | 중계무역 | checkbox | 중계 무역 |
| check.외국인수수입 | check.외국인수수입 | 외국인수수입 | checkbox | 외국인수 수입 |
| check.현재수출계약체결 | check.현재수출계약체결 | 현재수출계약체결 | checkbox | 현재 수출계약 체결 |
| check.현재수출계약미체결 | check.현재수출계약미체결 | 현재수출계약미체결 | checkbox | 현재 수출계약 미체결 |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| signer5.name | signer5.name | 신청인 | text | 박찬연 |
| seal.signer5 | seal.signer5 | 신청인 | seal | 현예지 |
| sign.signer5 | sign.signer5 | 신청인 | signature | 이욱유 |
| 대금송금후물품수령예정일 | 대금송금후물품수령예정일 | 대금송금후물품(선적서류)수령예정일 | date | 2025년 1월 12일 |

### hf201 · 거래외국환지정(변경)신청서(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.201 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| Staff | Staff | Staff | text |  |
| Manager | Manager | Manager | text |  |
| PhoneNo | PhoneNo | PhoneNo | phone | 010-5907-7253 |
| PhoneNo2 | PhoneNo2 | PhoneNo | phone | 010-5907-7253 |
| of | of | of | text |  |
| Bank | Bank | Bank | text |  |

### hf202 · 거래외국환지정(변경)신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.202 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 지정인성명(상호) | text | 박찬연 |
| seal.signer | seal.customer | 지정인성명(상호) | seal | 최우빈 |
| sign.signer | sign.customer | 지정인성명(상호) | signature | 박찬연 |
| 소 | 소 | 소 | text |  |
| customer.email | customer.email | E-Mail주소 | text | chanyeon363@naver.com |
| signer2.name | agent.name | 대리인성명(상호) | text | 강석호 |
| seal.signer2 | seal.agent | 대리인성명(상호) | seal | 김순우 |
| sign.signer2 | sign.agent | 대리인성명(상호) | signature | 강석호 |
| 소2 | 소2 | 소 | text |  |
| customer.email2 | customer.email2 | E-Mail주소 | text | chanyeon363@naver.com |
| seal.signer3 | seal.signer3 | 장 | seal | 반혁주 |
| sign.signer3 | sign.signer3 | 장 | signature | 최연현 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.signer4 | seal.signer4 | 지점장 | seal | 김혜지 |
| sign.signer4 | sign.signer4 | 지점장 | signature | 연수유 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 노준서 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 안수은 |

### hf203 · 주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.203 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| DateofReceipt | DateofReceipt | DateofReceipt | date | 2025년 10월 18일 |
| check.Individual | check.Individual | Individual | checkbox | 보기2 |
| check.ForeignInvestor | check.ForeignInvestor | ForeignInvestor | checkbox | 보기1 |
| customer.address | customer.address | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| value | value | (Korean) | amount |  |
| value2 | value2 | (English) | amount |  |
| Headquarter | Headquarter | Headquarter | text |  |
| Mainfactory | Mainfactory | Mainfactory(Mainplaceofbusiness) | text |  |
| customer.nationality | customer.nationality | Nationality | text | 대한민국 |
| AcquisitionPricewon | AcquisitionPricewon | AcquisitionPrice:won(USD) | number | 70 |
| check.보기1 | check.보기1 | 보기1 | checkbox | 보기1 |
| check.보기12 | check.보기12 | 보기1 | checkbox | 보기1 |
| check.보기13 | check.보기13 | 보기1 | checkbox | 보기1 |
| check.보기14 | check.보기14 | 보기1 | checkbox | 보기1 |
| NotificationNo | NotificationNo | NotificationNo | text | 6998-9505 |
| NumberofReceipt | NumberofReceipt | NumberofReceipt | text | 202-647603-59940 |
| DateofCompletion | DateofCompletion | DateofCompletion | date | 2025년 10월 19일 |
| won | won | won | text |  |
| Capital | Capital | Capital | text |  |
| wonUSD | wonUSD | won(USD | amount | USD 12,600 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 이소주 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이영빈 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김윤원 |
| DateofReceipt2 | DateofReceipt2 | DateofReceipt | date | 2025년 7월 16일 |
| check.Individual2 | check.Individual2 | Individual | checkbox | Foreign company |
| check.ForeignInvestor2 | check.ForeignInvestor2 | ForeignInvestor | checkbox | 보기1 |
| customer.address2 | customer.address2 | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| value3 | value3 | (Korean) | amount |  |
| value4 | value4 | (English) | amount |  |
| Headquarter2 | Headquarter2 | Headquarter | text |  |
| Mainfactory2 | Mainfactory2 | Mainfactory(Mainplaceofbusiness) | text |  |
| customer.nationality2 | customer.nationality2 | Nationality | text | 대한민국 |
| AcquisitionPricewon2 | AcquisitionPricewon2 | AcquisitionPrice:won(USD) | number | 60 |
| check.보기15 | check.보기15 | 보기1 | checkbox | 보기1 |
| check.보기16 | check.보기16 | 보기1 | checkbox | 보기1 |
| check.보기17 | check.보기17 | 보기1 | checkbox | 보기1 |
| check.보기18 | check.보기18 | 보기1 | checkbox | 보기1 |
| NotificationNo2 | NotificationNo2 | NotificationNo | text | 298-047842-95649 |
| NumberofReceipt2 | NumberofReceipt2 | NumberofReceipt | text | 499-772009-79911 |
| DateofCompletion2 | DateofCompletion2 | DateofCompletion | date | 2025년 5월 14일 |
| won2 | won2 | won | text |  |
| Capital2 | Capital2 | Capital | text |  |
| wonUSD2 | wonUSD2 | won(USD | amount | JPY 122,900 |
| Delegated | Delegated | Delegated | text |  |
| Delegated2 | Delegated2 | Delegated | text |  |
| Delegated3 | Delegated3 | Delegated | text |  |

### hf204 · 주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(국문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.204 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 접수일 | 접수일 | 접수일 | text |  |
| 처리일 | 처리일 | 처리일 | text |  |
| check.개인 | check.개인 | 개인 | checkbox | 외국법인 |
| customer.address | customer.address | 주소(영문) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 하려는사업 | 하려는사업 | 하려는(하고있는)사업 | text |  |
| value | value | (국문) | amount |  |
| value2 | value2 | (영문) | amount |  |
| 본사 | 본사 | 본사 | text |  |
| 주공장소재지 | 주공장소재지 | 주공장(주사업장)소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 금번투자지역 | 금번투자지역 | 금번투자지역(신주취득및출연의경우) | text |  |
| 액면총액 | 액면총액 | 액면총액(A×B) | number | 2,620,000 |
| 금번투자에따른예상근로자수 | 금번투자에따른예상근로자수 | 금번투자에따른예상근로자수 | text |  |
| 취득총액 | 취득총액 | 취득총액(A×C) | number | 6,380,000원 |
| customer.nationality | customer.nationality | 국적 | text | 대한민국 |
| 취득총액원 | 취득총액원 | 취득총액:원(USD상당) | number | 70 |
| check.방위사업법제3조제7호에따른방위산업물자를생산하는기업 | check.방위사업법제3조제7호에따른방위산업물자를생산하는기업 | 「방위사업법」제3조제7호에따른방위산업물자를생산하는기업 | checkbox | 보기1 |
| check.보기1 | check.보기1 | 보기1 | checkbox | 보기1 |
| check.보기12 | check.보기12 | 보기1 | checkbox | 보기1 |
| check.보기13 | check.보기13 | 보기1 | checkbox | 보기1 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신고인또는신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신고인또는신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신고인또는신청인 | signature | 최우빈 |
| 신고번호 | 신고번호 | 신고(허가)번호 | text | 4361-7064 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 접수번호 | 접수번호 | 접수번호 | text |  |
| 기존주취득시 | 기존주취득시 | 기존주취득시 | number | 840,000 |
| 취득전 | 취득전 | 취득(출연)전 | number | 9,720,000 |
| 취득후 | 취득후 | 취득(출연)후 | number | 76,630,000 |
| 의내용 | 의내용 | 의내용 | text | 해당 없음 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 남철호 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김준찬 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 검인 |
| 접수일2 | 접수일2 | 접수일 | text |  |
| 처리일2 | 처리일2 | 처리일 | text |  |
| check.개인2 | check.개인2 | 개인 | checkbox | 국제경제협력기구 |
| customer.address2 | customer.address2 | 주소(영문) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 하려는사업2 | 하려는사업2 | 하려는(하고있는)사업 | text |  |
| value3 | value3 | (국문) | amount |  |
| value4 | value4 | (영문) | amount |  |
| 본사2 | 본사2 | 본사 | text |  |
| 주공장소재지2 | 주공장소재지2 | 주공장(주사업장)소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 금번투자지역2 | 금번투자지역2 | 금번투자지역(신주취득및출연의경우) | text |  |
| 액면총액2 | 액면총액2 | 액면총액(A×B) | number | 340,000 |
| 금번투자에따른예상근로자수2 | 금번투자에따른예상근로자수2 | 금번투자에따른예상근로자수 | text |  |
| 취득총액2 | 취득총액2 | 취득총액(A×C) | number | 25,250,000 |
| customer.nationality2 | customer.nationality2 | 국적 | text | 대한민국 |
| 취득총액원2 | 취득총액원2 | 취득총액:원(USD상당) | number | 70 |
| check.방위사업법제3조제7호에따른방위산업물자를생산하는기업2 | check.방위사업법제3조제7호에따른방위산업물자를생산하는기업2 | 「방위사업법」제3조제7호에따른방위산업물자를생산하는기업 | checkbox | 보기1 |
| check.보기14 | check.보기14 | 보기1 | checkbox | 보기1 |
| check.보기15 | check.보기15 | 보기1 | checkbox | 보기1 |
| check.보기16 | check.보기16 | 보기1 | checkbox | 보기1 |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고인또는신청인 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신고인또는신청인 | seal | 현예지 |
| sign.signer2 | sign.signer2 | 신고인또는신청인 | signature | 박찬연 |
| 신고번호2 | 신고번호2 | 신고(허가)번호 | text | 499054-4730488 |
| date4 | date4 | 작성일 | date | 2026년 1월 31일 |
| 접수번호2 | 접수번호2 | 접수번호 | text |  |
| 기존주취득시2 | 기존주취득시2 | 기존주취득시 | number | 21,120,000 |
| 취득전2 | 취득전2 | 취득(출연)전 | number | 1,500,000원 |
| 취득후2 | 취득후2 | 취득(출연)후 | number | 8,190,000 |
| 의내용2 | 의내용2 | 의내용 | text | 해당 없음 |

### hf205 · 외국환거래법시행령상 거주성확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.205 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1****** |
| 여권번호 | 여권번호 | 여권번호 | text | M67845442 |
| customer.nationality | customer.nationality | 국적 | text | 대한민국 |
| 가외국에서영업활동에종사하고있습니까 | 가외국에서영업활동에종사하고있습니까 | 가외국에서영업활동에종사하고있습니까? | text |  |
| 나외국에있는국제기구에서근무하고있습니까 | 나외국에있는국제기구에서근무하고있습니까 | 나외국에있는국제기구에서근무하고있습니까? | text |  |
| 예 | 예 | 예(YES) | text |  |
| 예2 | 예2 | 예(YES) | text |  |
| 마외국정부또는국제기구의공무로입국하는자입니까 | 마외국정부또는국제기구의공무로입국하는자입니까 | 마외국정부또는국제기구의공무로입국하는자입니까? | text |  |
| 바거주자였던외국인으로서출국하여외국에서3개월이상체재중입니까 | 바거주자였던외국인으로서출국하여외국에서3개월이상체재중입니까 | 바거주자였던외국인으로서출국하여외국에서3개월이상체재중입니까? | text |  |
| 예3 | 예3 | 예(YES) | text |  |
| 국민_목록[].아니오 | 국민_목록[].아니오 | 아니오(NO) | text |  |
| 외국인_목록[].아니오 | 외국인_목록[].아니오 | 아니오(NO) | text |  |
| 아니오 | 아니오 | 아니오(NO) | text |  |
| check.판정방법 | check.판정방법 | 판정방법 | checkbox | 판정방법 |
| 항목 | 항목 | 항목 | text |  |
| 외국인 | 외국인 | 외국인 | text |  |
| 예4 | 예4 | 예(YES) | text |  |
| 나비거주자이었던자로서입국하여국내에3개월이상체재중입니까 | 나비거주자이었던자로서입국하여국내에3개월이상체재중입니까 | 나비거주자이었던자로서입국하여국내에3개월이상체재중입니까? | text |  |
| 다국내에서영업활동에종사하고있습니까 | 다국내에서영업활동에종사하고있습니까 | 다국내에서영업활동에종사하고있습니까? | text |  |
| 라6개월이상국내에서체재하고있습니까 | 라6개월이상국내에서체재하고있습니까 | 라6개월이상국내에서체재하고있습니까? | text |  |
| check.판정방법2 | check.판정방법2 | 판정방법 | checkbox | 판정방법 |
| 거주성판정결과 | 거주성판정결과 | 거주성판정결과 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 강순준 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| 항목2 | 항목2 | 항목 | text |  |
| 가외국에서영업활동에종사하고있는자 | 가외국에서영업활동에종사하고있는자 | 가.외국에서영업활동에종사하고있는자 | text |  |
| 나외국에있는국제기구에서근무하고있는자 | 나외국에있는국제기구에서근무하고있는자 | 나.외국에있는국제기구에서근무하고있는자 | text |  |
| 자로서재정경제부장관이정하는자 | 자로서재정경제부장관이정하는자 | 자로서재정경제부장관이정하는자 | text |  |
| 수행원이나사용인 | 수행원이나사용인 | 수행원이나사용인 | text |  |
| 비거주자입증서류 | 비거주자입증서류 | ■비거주자입증서류(다음중택1) | text |  |
| 영업활동입증서류 | 영업활동입증서류 | 영업활동입증서류 | text |  |

### hf206 · 연간사업실적보고서(투자잔액 1,000만불 초과 기업)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.206 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 투자자명담당자 | 투자자명담당자 | 투자자명담당자 | text | 허욱지 |
| company.biz_item | corp.biz_item | 업종(중분류) | text | 무역 |
| check.투자자법인성격 | check.투자자법인성격 | 투자자법인성격 | checkbox | 실제영업법인 |
| check.외국인투자기업2여부 | check.외국인투자기업2여부 | 외국인투자기업2)여부 | checkbox | 아니오 |
| check.예 | check.예 | 예 | checkbox | 예 |
| 자기자본 | 자기자본 | 자기자본 | number | 5.2 |
| 계열명 | 계열명 | 계열명 | text |  |
| 사후관리은행 | 사후관리은행 | 사후관리은행 | text | 하나은행 |
| 법인명1 | 법인명1 | 법인명1 | text | (주)제일무역 |
| 소재지2 | 소재지2 | 소재지(국가,주,성)2) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 투자업종3 | 투자업종3 | 투자업종3 | text |  |
| 설립등기일 | 설립등기일 | 설립등기일 | date | 2026.12.25 |
| check.법인성격 | check.법인성격 | 법인성격 | checkbox | 특수목적회사(SPC) |
| check.투자형태6 | check.투자형태6 | 투자형태6 | checkbox | 단독투자 |
| check.지배구조 | check.지배구조 | 지배구조 | checkbox | 지주회사 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| 주요취급품목4 | 주요취급품목4 | 주요취급품목4 | text | 기계 부품 |
| 영업개시일 | 영업개시일 | 영업개시일 | date | 2025.10.16 |
| check.설립형태 | check.설립형태 | 설립형태 | checkbox | 기존법인 지분인수 |
| 전화 | 전화 | 전화 | phone | 010-5907-7253 |
| 임원 | 임원 | 임원 | text |  |
| 주주현황7_목록[].국가 | 주주현황7_목록[].국가 | 국가 | text | 미국 |
| 주주현황7_목록[].상호또는성명 | 주주현황7_목록[].상호또는성명 | 상호또는성명 | text | (주)유니온무역 |
| 상호또는성명 | 상호또는성명 | 상호또는성명 | text | 새한푸드 |
| 한국투자자지분율합 | 한국투자자지분율합 | 한국투자자지분율합(B) | number | 60 |
| 주주현황7_목록[].금기말 | 주주현황7_목록[].금기말 | 금기말 | text |  |
| 주주현황7_목록[].전기말 | 주주현황7_목록[].전기말 | 전기말 | text |  |
| 천미불 | 천미불 | 천미불 | number | 30 |
| 주주현황7_목록[].계열여부 | 주주현황7_목록[].계열여부 | 계열여부 | text |  |
| 기타 | 기타 | 기타 | text | 해당 없음 |
| 기타2 | 기타2 | 기타 | text | 해당 없음 |
| 지분율10이상투자자 | 지분율10이상투자자 | -지분율10%이상투자자 | text |  |
| 주투자자관계사1 | 주투자자관계사1 | 주투자자관계사1 | text |  |
| 기타3 | 기타3 | 기타 | text | 해당 없음 |
| 계 | 계 | 계(A) | text |  |
| 지분율10이상투자자2 | 지분율10이상투자자2 | -지분율10%이상투자자 | text |  |
| 주투자자관계사12 | 주투자자관계사12 | 주투자자관계사1 | text |  |
| 기타4 | 기타4 | 기타 | text | 해당 없음 |
| 계2 | 계2 | 계(B) | text |  |
| 합계 | 합계 | 합계(A+B) | number | 4,190,000 |
| 대부투자_목록[].금기말 | 대부투자_목록[].금기말 | 금기말 | text |  |
| 지분율10미만_목록[].금기말 | 지분율10미만_목록[].금기말 | 금기말 | text |  |
| 지분투자 | 지분투자 | 지분투자 | text |  |
| 대부투자 | 대부투자 | 대부투자(대여금및채권인수) | text |  |
| 매출채권 | 매출채권 | 매출채권 | number | 133,280,000 |
| 목록[].금기말 | 목록[].금기말 | 금기말 | text |  |
| 목록[].전기말 | 목록[].전기말 | 전기말 | text |  |
| 배당금 | 배당금 | 배당금 | text |  |
| 목록[].이자 | 목록[].이자 | 이자 | number | 36,300,000 |
| 지급총액 | 지급총액 | 지급총액 | number | 80,410,000원 |
| 한국투자자앞지급액 | 한국투자자앞지급액 | 한국투자자앞지급액 | text |  |
| 한국투자자앞대부이자지급액 | 한국투자자앞대부이자지급액 | 한국투자자앞대부이자지급액 | number | 900,000원 |
| 한국투자자앞로얄티등기타지급액 | 한국투자자앞로얄티등기타지급액 | 한국투자자앞로얄티등기타지급액 | text |  |
| 한국인근로자앞임금지급액 | 한국인근로자앞임금지급액 | 한국인근로자앞임금지급액 | text |  |
| 채권인수 | 채권인수 | 채권인수(단위:천미불) | text |  |
| 목록[].차입처 | 목록[].차입처 | 차입처 | text | 대성정밀(주) |
| 차입처 | 차입처 | 차입처 | text | 미래메디칼 |
| 목록[].코드1 | 목록[].코드1 | 코드1 | text | 8241 |
| 목록[].차입금액 | 목록[].차입금액 | 차입금액 | text | 920,000 |
| 목록[].보증자 | 목록[].보증자 | 보증자 | text | (주)유니온무역 |
| 보증자 | 보증자 | 보증자 | text | 주식회사 우진전자 |
| 목록[].년미만 | 목록[].년미만 | 년미만 | text |  |
| 목록[].년이상 | 목록[].년이상 | 년이상 | text |  |
| 목록[].변동2 | 목록[].변동2 | 변동2 | text |  |
| 목록[].고정 | 목록[].고정 | 고정 | text |  |
| 목록[].용도3 | 목록[].용도3 | 용도3 | text | 생활자금 |
| 금액 | 금액 | 금액 | number | 8,520,000 |
| 비중 | 비중 | 비중 | text |  |
| 목록[].기타 | 목록[].기타 | 기타 | text | 해당 없음 |
| 목록[].한국투자자앞 | 목록[].한국투자자앞 | 한국투자자앞 | text |  |
| 목록[].관계회사앞 | 목록[].관계회사앞 | 관계회사앞 | text |  |
| 목록[].계 | 목록[].계 | 계 | text |  |
| 금액2 | 금액2 | 금액 | number | 540,000 |
| 비중2 | 비중2 | 비중 | text |  |
| 목록[].전기 | 목록[].전기 | 전기 | text |  |
| 자산총계 | 자산총계 | 자산총계 | text |  |
| 목록[].금기 | 목록[].금기 | 금기 | text |  |
| 부채총계 | 부채총계 | 부채총계 | text |  |
| 자본총계 | 자본총계 | 자본총계 | text |  |
| 부채및자본총계 | 부채및자본총계 | 부채및자본총계 | text |  |
| check.현지법인운영상애로사항 | check.현지법인운영상애로사항 | 현지법인운영상애로사항(복수선택가능) | checkbox | 기타 |
| 대정부건의사항 | 대정부건의사항 | 대정부건의사항 | text |  |
| 철수 | 철수 | 철수 | text |  |
| 투자축소 | 투자축소 | 투자축소 | text |  |
| 현상유지 | 현상유지 | 현상유지 | text |  |
| 국가명 | 국가명 | 국가명 | text | 미국 |

### hf207 · 연간사업실적보고서(투자잔액 300만불 초과 1,000만불 이하 기업)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.207 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 투자자명담당자 | 투자자명담당자 | 투자자명담당자 | text | 선민인 |
| 업종1 | 업종1 | 업종(중분류)1) | text |  |
| check.투자자법인성격 | check.투자자법인성격 | 투자자법인성격 | checkbox | 실제영업법인 |
| check.외국인투자기업2여부 | check.외국인투자기업2여부 | 외국인투자기업2)여부 | checkbox | 아니오 |
| check.예 | check.예 | 예 | checkbox | 예 |
| 자기자본 | 자기자본 | 자기자본 | number | 31.05 |
| 계열명 | 계열명 | 계열명 | text |  |
| 사후관리은행 | 사후관리은행 | 사후관리은행 | text | 기업은행 |
| check.법인성격 | check.법인성격 | 법인성격 | checkbox | 특수목적회사(SPC) |
| check.투자형태7 | check.투자형태7 | 투자형태7 | checkbox | 단독투자 |
| check.지배구조 | check.지배구조 | 지배구조 | checkbox | 비지주회사 |
| 법인명1 | 법인명1 | 법인명1 | text | 우진정밀 |
| 소재지2 | 소재지2 | 소재지(국가,주,성)2) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 투자업종3 | 투자업종3 | 투자업종3 | text |  |
| 설립등기일 | 설립등기일 | 설립등기일 | date | 2027.07.04 |
| 주주구성_목록[].상호또는성명 | 주주구성_목록[].상호또는성명 | 상호또는성명 | text | 우진무역(주) |
| 주주구성_목록[].국가 | 주주구성_목록[].국가 | 국가 | text | 싱가포르 |
| 주주구성_목록[].지분율 | 주주구성_목록[].지분율 | 지분율(%) | number | 100 |
| check.설립형태 | check.설립형태 | 설립형태 | checkbox | 신설법인 설립 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| 주요취급품목4 | 주요취급품목4 | 주요취급품목4 | text | 전자부품 |
| 영업개시일 | 영업개시일 | 영업개시일 | date | 2025.04.17 |
| 주주구성_목록[].순투자액5 | 주주구성_목록[].순투자액5 | 순투자액(천미불)5) | text |  |
| 전화 | 전화 | 전화 | phone | 010-5907-7253 |
| 임원 | 임원 | 임원 | text |  |
| 지분투자 | 지분투자 | 지분투자 | text |  |
| 대부투자 | 대부투자 | 대부투자(대여금및채권인수) | text |  |
| 목록[].금기말 | 목록[].금기말 | 금기말 | text |  |
| 목록[].전기말 | 목록[].전기말 | 전기말 | text |  |
| 배당금 | 배당금 | 배당금 | text |  |
| 이자 | 이자 | 이자 | number | 3,090,000 |
| 지급총액 | 지급총액 | 지급총액 | number | 48,370,000 |
| 한국투자자앞지급액 | 한국투자자앞지급액 | 한국투자자앞지급액 | text |  |
| 한국투자자앞대부이자지급액 | 한국투자자앞대부이자지급액 | 한국투자자앞대부이자지급액 | number | 2,970,000 |
| 한국투자자앞로얄티등기타지급액 | 한국투자자앞로얄티등기타지급액 | 한국투자자앞로얄티등기타지급액 | text |  |
| 한국인근로자앞임금지급액 | 한국인근로자앞임금지급액 | 한국인근로자앞임금지급액 | text |  |
| 목록[].차입처 | 목록[].차입처 | 차입처 | text | (주)다온전자 |
| 차입처 | 차입처 | 차입처 | text | (주)유니온무역 |
| 목록[].코드1 | 목록[].코드1 | 코드1 | text | 410779 |
| 목록[].차입금액 | 목록[].차입금액 | 차입금액 | number | 20,600,000 |
| 목록[].보증자 | 목록[].보증자 | 보증자 | text | 제일시스템즈 |
| 보증자 | 보증자 | 보증자 | text | 주식회사 우진푸드 |
| 목록[].년미만 | 목록[].년미만 | 년미만 | text |  |
| 목록[].년이상 | 목록[].년이상 | 년이상 | text |  |
| 목록[].변동2 | 목록[].변동2 | 변동2 | text |  |
| 목록[].고정 | 목록[].고정 | 고정 | text |  |
| 목록[].용도3 | 목록[].용도3 | 용도3 | text | 계좌 정리 |
| 금액 | 금액 | 금액 | number | 150,000 |
| 비중 | 비중 | 비중 | text |  |
| 목록[].기타 | 목록[].기타 | 기타 | text | 해당 없음 |
| 목록[].한국투자자앞 | 목록[].한국투자자앞 | 한국투자자앞 | text |  |
| 목록[].관계회사앞 | 목록[].관계회사앞 | 관계회사앞 | text |  |
| 목록[].계 | 목록[].계 | 계 | text |  |
| 금액2 | 금액2 | 금액 | number | 5,700,000원 |
| 비중2 | 비중2 | 비중 | text |  |
| 목록[].전기 | 목록[].전기 | 전기 | text |  |
| 자산총계 | 자산총계 | 자산총계 | text |  |
| 목록[].금기 | 목록[].금기 | 금기 | text |  |
| 부채총계 | 부채총계 | 부채총계 | text |  |
| 자본총계 | 자본총계 | 자본총계 | text |  |
| 부채및자본총계 | 부채및자본총계 | 부채및자본총계 | text |  |
| check.현지법인운영상애로사항 | check.현지법인운영상애로사항 | 현지법인운영상애로사항(복수선택가능) | checkbox | 기타 |
| 대정부건의사항 | 대정부건의사항 | 대정부건의사항 | text |  |
| 철수 | 철수 | 철수 | text |  |
| 투자축소 | 투자축소 | 투자축소 | text |  |
| 현상유지 | 현상유지 | 현상유지 | text |  |
| 국가명 | 국가명 | 국가명 | text | 영국 |

### hf208 · 지급확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.208 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 지급사유 | 지급사유 | 지급사유 | text | 만기 해지 |
| 수취인 | 수취인 | 수취인 | text | (주)유니온무역 |
| 수취인과의관계 | 수취인과의관계 | 수취인과의관계 | text | (주)유니온무역 |
| customer.rrn | customer.rrn | 주민번호(사업자등록번호) | rrn | 900210-1659382 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 강순준 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 지정거래외국환은행의장 | text | 길훈진 |
| seal.signer2 | seal.signer2 | 지정거래외국환은행의장 | seal | 김원아 |
| sign.signer2 | sign.signer2 | 지정거래외국환은행의장 | signature | 길훈진 |

### hf209 · 영수확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.209 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 무역 | 무역 | 무역 | text |  |
| 용역및서비스 | 용역및서비스 | 용역및서비스 | text |  |
| 증여 | 증여 | 증여 | text |  |
| 기타 | 기타 | 기타 | text | 해당 없음 |
| 송금인 | 송금인 | 송금인 | text |  |
| 송금인과관계 | 송금인과관계 | 송금인과관계 | text |  |
| customer.rrn | customer.rrn | 주민번호(사업자등록번호) | rrn | 900210-1659382 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 인 | text | 박찬연 |
| seal.signer | seal.customer | 인 | seal | 현예지 |
| sign.signer | sign.customer | 인 | signature | 박찬연 |

### hf210 · 대북투자 신고 및 투자실적 보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.210 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| date | date | 일자 | date | 2026.01.31 |
| 목록[].투자자 | 목록[].투자자 | 투자자 | text |  |
| 기업규모1 | 기업규모1 | 기업규모1 | text |  |
| 목록[].현지법인명 | 목록[].현지법인명 | 현지법인명 | text | (주)유니온물산 |
| 투자지역2 | 투자지역2 | 투자지역2 | text |  |
| 업종3 | 업종3 | 업종3 | text |  |
| 투자방법4 | 투자방법4 | 투자방법4 | text |  |
| 비율 | 비율 | 비율 | number | 40 |
| 목록[].현금 | 목록[].현금 | 현금 | text |  |
| 현물 | 현물 | 현물 | text |  |
| 기타 | 기타 | 기타 | text | 해당 없음 |
| 합작투자자 | 합작투자자 | 합작(합영)투자자 | text |  |
| 신고기관 | 신고기관 | 신고기관 | text |  |
| 비고4 | 비고4 | 비고4 | text | 해당 없음 |
| 목록[].신고일자 | 목록[].신고일자 | 신고일자 | date | 2025년 6월 21일 |
| 목록[].신고금액 | 목록[].신고금액 | 신고금액 | number | 470,000 |
| 투자일자 | 투자일자 | 투자일자 | date | 2025.03.29 |
| 투자방법주 | 투자방법주 | 투자방법주 | text |  |
| 이익잉여금등기타 | 이익잉여금등기타 | 이익잉여금등기타 | text | 해당 없음 |
| 신규증액 | 신규증액 | 신규·증액 | text |  |
| 투자자명 | 투자자명 | 투자자명 | text |  |
| 구분주 | 구분주 | 구분주 | text |  |
| 취득일 | 취득일 | 취득일 | date | 2025년 6월 2일 |
| 취득금액 | 취득금액 | 취득금액 | number | 3,840,000 |
| date2 | date2 | 신고일자 | date | 2026.01.31 |
| 외환매입일자 | 외환매입일자 | 외환매입일자 | date | 2025.03.25 |
| 매입금액 | 매입금액 | 매입금액 | number | 1,270,000 |
| 투자국 | 투자국 | 투자국 | text |  |
| date3 | date3 | 일자 | date | 2026.01.31 |
| 투자지역 | 투자지역 | 투자지역 | text |  |
| 투자방법 | 투자방법 | 투자방법 | text |  |
| 비율2 | 비율2 | 비율 | number | 10 |
| 회수내역주 | 회수내역주 | 회수내역주 | text |  |
| 회수금액 | 회수금액 | 회수(실효)금액 | number | 12,700,000원 |
| 합작투자자2 | 합작투자자2 | 합작(합영)투자자 | text |  |
| 비고 | 비고 | 비고 | text | 해당 없음 |
| 구분주2 | 구분주2 | 구분주 | text |  |
| 변경일자 | 변경일자 | 변경일자 | date | 2025년 8월 11일 |
| 변경전 | 변경전 | 변경전 | text | 해당 없음 |
| 변경후 | 변경후 | 변경후 | text | 해당 없음 |

### hf211 · 사업계획서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.211 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 상호또는성명 | 상호또는성명 | 상호또는성명 | text | (주)유니온무역 |
| company.address | corp.address | 소재지(주소) | text | 서울특별시 중구 다산로 361, 6층 |
| check.투자자규모 | check.투자자규모 | 투자자규모 | checkbox | 대기업 |
| check.투자자법인성격 | check.투자자법인성격 | 투자자법인성격 | checkbox | 실제영업법인 |
| check.외국인투자기업2여부 | check.외국인투자기업2여부 | 외국인투자기업2)여부 | checkbox | 아니오 |
| 총자산 | 총자산 | 총자산 | number | 0.72 |
| company.biz_item | corp.biz_item | 업종(제품) | text | 무역 |
| check.예 | check.예 | 예 | checkbox | 예 |
| 설립년월일 | 설립년월일 | 설립년월일 | date | 2025-04-29 |
| 자기자본 | 자기자본 | 자기자본(자본금) | text |  |
| 담당자및연락처 | 담당자및연락처 | 담당자및연락처 | phone | 010-5907-7253 |
| company.name | corp.name | 법인명 | text | (주)유니온무역 |
| check.법인형태 | check.법인형태 | 법인형태 | checkbox | 해외자원개발사업 |
| check.법인형태2 | check.법인형태2 | 법인형태 | checkbox | 법인미설립 |
| 총자본금 | 총자본금 | 총자본금 | text |  |
| check.투자형태1 | check.투자형태1 | 투자형태1 | checkbox | 공동투자 |
| check.투자유형2 | check.투자유형2 | 투자유형2 | checkbox | M&A |
| check.법인성격 | check.법인성격 | 법인성격 | checkbox | 실제 영업법인 |
| check.지배구조 | check.지배구조 | 지배구조 | checkbox | 지주회사 |
| check.투자목적 | check.투자목적 | 투자목적(택일) | checkbox | 수출촉진 |
| company.name2 | company.name2 | 상호 | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자명 | text | 박찬연 |
| company.ceo2 | company.ceo2 | 대표자 | text | 박찬연 |
| check.년월일 | check.년월일 | 년월일 | checkbox | 자본금 미납입 |
| company.biz_no | corp.biz_no | 사업자번호 | biz_no | 264-82-36559 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| check.설립형태 | check.설립형태 | 설립형태 | checkbox | 신설법인 설립 |
| check.증권투자 | check.증권투자 | 증권투자(1.신규투자2.증액투자) | checkbox | 제재기관 보고후 사후신고 |
| 지분율이50를초과할경우최대주주의최대주주소속국가 | 지분율이50를초과할경우최대주주의최대주주소속국가 | 지분율이50%를초과할경우최대주주의최대주주소속국가 | number | 60 |
| 취득증권_목록[].증권종류 | 취득증권_목록[].증권종류 | 증권종류 | text |  |
| 취득증권_목록[].주수 | 취득증권_목록[].주수 | 주수 | text |  |
| 주당액면 | 주당액면 | 주당액면 | text |  |
| 취득가액이액면과상이할경우그산출근거1 | 취득가액이액면과상이할경우그산출근거1 | 취득가액이액면과상이할경우그산출근거1 | number | 21,600,000원 |
| 취득증권_목록[].주당가액 | 취득증권_목록[].주당가액 | 주당가액 | number | 297,320,000 |
| 현금 | 현금 | 현금 | text |  |
| 주식 | 주식 | 주식 | text |  |
| 기술투자 | 기술투자 | 기술투자 | text |  |
| 현물 | 현물 | 현물 | text |  |
| 이익잉여금 | 이익잉여금 | 이익잉여금 | text |  |
| 기타 | 기타 | 기타() | text | 해당 없음 |
| 한국측 | 한국측 | 한국측(1) | text |  |
| 한국측2 | 한국측2 | 한국측(1) | text |  |
| 한국측3 | 한국측3 | 한국측(1) | text |  |
| 한국측4 | 한국측4 | 한국측(1) | text |  |
| 한국측5 | 한국측5 | 한국측(1) | text |  |
| 현지측 | 현지측 | 현지측(2) | text |  |
| 제3국 | 제3국 | 제3국(3) | text |  |
| 한국측_목록[].금액 | 한국측_목록[].금액 | 금액 | text | 2,140,000 |
| 목록[].금액 | 목록[].금액 | 금액 | text | 640,000 |
| 합계 | 합계 | 합계(1+2+3) | number | 62,420,000 |
| 한국측_목록[].비율 | 한국측_목록[].비율 | 비율(%) | text | 5 |
| 목록[].비율 | 목록[].비율 | 비율(%) | number | 100 |
| 대부액 | 대부액 | 대부액 | text |  |
| 이율 | 이율 | 이율 | number | 10 |
| 원금상환방법 | 원금상환방법 | 원금상환방법 | number | 7,130,000 |
| 자기자금 | 자기자금 | 자기자금 | text |  |
| 자금용도 | 자금용도 | 자금용도 | text | 결혼자금 |
| 기간 | 기간 | 기간 | text |  |
| 이자징수방법 | 이자징수방법 | 이자징수방법 | number | 7,460,000 |
| 차입금 | 차입금 | 차입금 | text |  |

### hf212 · 해외직접투자 신고서(보고서)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.212 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| signer.name | corp.ceo | 대표자 | text | 박찬연 |
| seal.signer | seal.corp | 대표자 | seal | 박찬연 |
| sign.signer | sign.customer | 대표자 | signature | 이민빈 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| 투자국명 | 투자국명 | 투자국명 | text | 필리핀 |
| 투자방법 | 투자방법 | 투자방법 | text |  |
| 투자업종 | 투자업종 | 투자업종 | text |  |
| 투자금액 | 투자금액 | 투자금액 | number | 32,970,000 |
| 투자비율 | 투자비율 | 투자비율 | number | 100 |
| 투자목적 | 투자목적 | 투자목적 | text | 주택구입 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| company.address | corp.address | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| 자금조달 | 자금조달 | 자금조달 | text |  |
| 주요제품 | 주요제품 | 주요제품 | text |  |
| 출자금액 | 출자금액 | 출자금액 | number | 770,000 |
| 결산월 | 결산월 | 결산월 | text |  |
| 투자유형 | 투자유형 | 투자유형 | text |  |
| 신고번호 | 신고번호 | 신고번호 | text | 604-529450-43876 |
| 신고금액 | 신고금액 | 신고금액 | number | 13,760,000 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 해외직접투자신고서 | 해외직접투자신고서 | 해외직접투자신고서(보고서) | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| company.ceo | company.ceo | 대표자 | text | 박찬연 |
| 위와같이신고되었음을확인함 | 위와같이신고되었음을확인함 | 위와같이신고(보고)되었음을확인함 | text |  |

### hf213 · 사전 송금방식 수입대금 지급시

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.213 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.사전송금방식 | check.사전송금방식 | 사전송금방식 | checkbox | 사전 송금방식 |
| check.대금송금후물품수령예정일 | check.대금송금후물품수령예정일 | 대금송금후물품(선적서류)수령예정일 | checkbox | 년 이내 |
| check.대금송금후물품수령예정일2 | check.대금송금후물품수령예정일2 | 대금송금후물품(선적서류)수령예정일 | checkbox | 년 초과 |
| check.중계무역 | check.중계무역 | 중계무역 | checkbox | 중계무역 |
| check.현재수출계약체결 | check.현재수출계약체결 | 현재수출계약체결 | checkbox | 현재 수출계약 체결 |
| check.현재수출계약미체결 | check.현재수출계약미체결 | 현재수출계약미체결 | checkbox | 현재 수출계약 미체결 |
| check.사후송금방식 | check.사후송금방식 | 사후송금방식 | checkbox | 사후 송금방식 |
| check.일반수입 | check.일반수입 | 일반수입 | checkbox | 일반 수입 |
| check.외국인수수입 | check.외국인수수입 | 외국인수수입 | checkbox | 외국인수수입 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 고객명 | text | 박찬연 |
| seal.signer | seal.customer | 고객명 | seal | 박찬연 |
| sign.signer | sign.customer | 고객명 | signature | 강순준 |
| 본서식의작성대상이아님 | 본서식의작성대상이아님 | →본서식의작성대상이아님 | text |  |
| 수입물품을국내에서인수하는경우 | 수입물품을국내에서인수하는경우 | :수입물품을국내에서인수하는경우 | text | 포장재 |

### hf214 · 자본거래 사후보고 확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.214 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 신청인 | text | 박찬연 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.rrn | customer.rrn | 주민(사업자)번호 | rrn | 900210-1659382 |
| customer.email | customer.email | 이메일주소 | text | chanyeon363@naver.com |
| check.거주자의미화5천만불이하 | check.거주자의미화5천만불이하 | 거주자의미화5천만불이하외화자금차입(증권발행포함)(규정제7- | checkbox | 거주자의 미화 5천만불 이하 외화자금 차입(증권발행 포함) (규정 제7- |
| check.현지법인등의외화자금차입 | check.현지법인등의외화자금차입 | 현지법인등의외화자금차입(규정제7-14조의2,제7-18조) | checkbox | 현지법인등의 외화자금 차입 (규정 제7-14조의2, 제7-18조) |
| check.현지법인에대한1년미만의 | check.현지법인에대한1년미만의 | 현지법인에대한1년미만의금전대여(규정제7-16조) | checkbox | 현지법인에 대한 1년 미만의 금전대여 (규정 제7-16조) |
| check.거주자와비거주자간채무의 | check.거주자와비거주자간채무의 | 거주자와비거주자간채무의보증계약에따른자본거래(규정제7-18조) | checkbox | 거주자와 비거주자간 채무의 보증계약에 따른 자본거래 (규정 제7-18조) |
| check.거주자의외국부동산시설물 | check.거주자의외국부동산시설물 | 거주자의외국부동산·시설물이용에관한권리취득(규정제7-21조 | checkbox | 거주자의 외국부동산 · 시설물 이용에 관한 권리 취득 (규정 제7-21조 |
| check.거자와비거주자간임대차계 | check.거자와비거주자간임대차계 | 거자와비거주자간임대차계약(규정제7-46조) | checkbox | 거자와 비거주자간 임대차 계약 (규정 제7-46조) |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 강순준 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |

### hf215 · 상호계산계정 결산대차기잔액처분(변경)신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.215 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 금액 | 금액 | 금액 | number | 7,230,000 |
| 송금처 | 송금처 | 송금처 | text |  |
| 송금방법 | 송금방법 | 송금방법 | text |  |
| 송금은행 | 송금은행 | 송금은행 | text | 하나은행 |
| 신고번호 | 신고번호 | 신고번호 | text | 8038-5906 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 명 | text | 박찬연 |
| seal.signer | seal.customer | 명 | seal | 강순준 |
| sign.signer | sign.customer | 명 | signature | 박찬연 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| seal.signer2 | seal.signer2 | 은행장 | seal | 강희유 |
| sign.signer2 | sign.signer2 | 은행장 | signature | 반순아 |

### hf216 · 해외부동산 취득신고(수리)서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.216 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.본신고 | check.본신고 | 본신고 | checkbox | 내신고 |
| 취득가액 | 취득가액 | 취득가액 | number | 28,470,000 |
| 총취득금액 | 총취득금액 | 총취득금액(A=B+C) | number | 274,200,000 |
| signer.name | customer.name | 성명(법인명) | text | 박찬연 |
| seal.signer | seal.customer | 성명(법인명) | seal | 최우빈 |
| sign.signer | sign.customer | 성명(법인명) | signature | 박찬연 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| check.부동산의종류 | check.부동산의종류 | 부동산의종류 | checkbox | 주택 |
| check.취득목적 | check.취득목적 | 취득목적 | checkbox | 주거이외(투자등) |
| company.address | corp.address | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| 면적 | 면적 | 면적 | text |  |
| 수취인명 | 수취인명 | 수취인명 | text | (주)한빛산업 |
| 신고인과의관계 | 신고인과의관계 | 신고인과의관계 | text |  |
| 총취득금액2 | 총취득금액2 | 총취득금액(A=B+C) | number | 770,000 |
| 취득자금국내송금액 | 취득자금국내송금액 | 취득자금국내송금액 | number | 96,600,000 |
| 모기지론 | 모기지론 | 모기지론(원리금상환송금예정금액) | text |  |
| 모기지론2 | 모기지론2 | 모기지론(원리금상환현지조달금액) | text |  |
| 기타 | 기타 | 기타:() | text | 해당 없음 |
| 수취인명2 | 수취인명2 | 수취인명 | text | (주)유니온무역 |
| check.신고인과의관계 | check.신고인과의관계 | 신고인과의관계 | checkbox | 기타 |
| customer.rrn | customer.rrn | 주민(사업자)등록번호 | rrn | 900210-1****** |
| 신고번호 | 신고번호 | 신고(수리)번호 | text | 4774-8180 |
| 신고금액 | 신고금액 | 신고(수리)금액 | number | 229,930,000원 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| 미달러환산액 | 미달러환산액 | 미달러환산액 | text |  |
| 국내송금액_목록[].미달러환산액 | 국내송금액_목록[].미달러환산액 | 미달러환산액 | text |  |
| 현지조달액_목록[].미달러환산액 | 현지조달액_목록[].미달러환산액 | 미달러환산액 | text |  |
| 미달러환산액2 | 미달러환산액2 | 미달러환산액 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고수리기관 | text | 연기하 |
| seal.signer2 | seal.signer2 | 신고수리기관 | seal | 원욱아 |
| sign.signer2 | sign.signer2 | 신고수리기관 | signature | 연기하 |
| 명 | 명 | 명(법인명) | text |  |
| 위의신고를다음과같이신고수리함 | 위의신고를다음과같이신고수리함 | 위의신고를다음과같이신고수리함. | text |  |

### hf217 · 해외직접투자 내용변경 신고(보고)서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.217 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 변경사항 | 변경사항 | 변경사항 | text |  |
| 변경사유 | 변경사유 | 변경사유(요약) | text | 자녀 교육비 |
| 목록[].변경후 | 목록[].변경후 | 변경후 | text | 해당 없음 |
| 신고번호 | 신고번호 | 신고번호 | text | 342308-1177041 |
| check.현지법인내용변경 | check.현지법인내용변경 | 현지법인내용변경 | checkbox | 기타 |
| signer.name | customer.name | 상호또는성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호또는성명 | seal | 현예지 |
| sign.signer | sign.customer | 상호또는성명 | signature | 박찬연 |
| 변경대상현지법인명 | 변경대상현지법인명 | 변경대상현지법인명 | text | 대성무역 |
| signer2.name | signer2.name | 신고기관 | text | 제갈수희 |
| seal.signer2 | seal.signer2 | 신고기관 | seal | 제갈수희 |
| sign.signer2 | sign.signer2 | 신고기관 | signature | 채순재 |
| company.biz_no | corp.biz_no | 사업자(주민)번호 | biz_no | 264-82-36559 |
| 소재지또는주소 | 소재지또는주소 | 소재지또는주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 전화 | 전화 | 전화 | phone | 010-5907-7253 |
| 대상신고번호 | 대상신고번호 | 대상신고번호 | text | 247738-3617639 |
| date | date | 신고일자 | date | 2026.01.31 |
| 신고금액 | 신고금액 | 신고금액 | number | 40,680,000 |

### hf218 · 서약서(개인의 외국주택 취득)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.218 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 신고인성명 | text | 박찬연 |
| seal.signer | seal.customer | 신고인성명 | seal | 이욱유 |
| sign.signer | sign.customer | 신고인성명 | signature | 박찬연 |
| signer2.name | family.name | 배우자성명* | text | 박영준 |
| seal.signer2 | seal.signer2 | 배우자성명* | seal | 김서호 |
| sign.signer2 | sign.signer2 | 배우자성명* | signature | 박영준 |
| check.지정거래외국환은행의장으 | check.지정거래외국환은행의장으 | 지정거래외국환은행의장으로부터신고수리를받아외국주택을취득한자는외 | checkbox | 지정거래외국환은행의 장으로부터 신고수리를 받아 외국주택을 취득한 자는 외 |
| check.사후보고서의제출등추가적 | check.사후보고서의제출등추가적 | 사후보고서의제출등추가적인문의사항이있거나,신고인의주소(해외체 | checkbox | 사후 보고서의 제출 등 추가적인 문의사항이 있거나, 신고인의 주소(해외체 |
| 부동산취득자금송금후3개월이내 | 부동산취득자금송금후3개월이내 | 부동산취득자금송금후3개월이내 | text |  |
| 부동산처분후3개월이내 | 부동산처분후3개월이내 | 부동산처분(변경)후3개월이내 | text |  |
| 수시보고서 | 수시보고서 | 수시보고서* | text |  |
| 매2년마다보유사실입증서류 | 매2년마다보유사실입증서류 | 매2년마다보유사실입증서류 | text |  |

### hf219 · 해외사무소 설치(변경)신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.219 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | corp.name | 상호 | text | (주)유니온무역 |
| seal.signer | seal.corp | 상호 | seal | 주식회사 한빛패션 |
| sign.signer | sign.customer | 상호 | signature | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자(주민)번호 | biz_no | 264-82-36559 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| check.기업규모 | check.기업규모 | 기업규모 | checkbox | 개인사업자 |
| check.구분 | check.구분 | 구분 | checkbox | 설치 |
| value | value | (표준산업분류코드5자리) | amount |  |
| 설치사유 | 설치사유 | 설치사유 | text | 생활자금 |
| 내용 | 내용 | 내용 | text | 해당 없음 |
| 사유 | 사유 | 사유 | text | 타행 이체 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| 신고번호 | 신고번호 | 신고번호 | text | 297-598748-80207 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고(보고)기관 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신고(보고)기관 | seal | 이욱유 |
| sign.signer2 | sign.signer2 | 신고(보고)기관 | signature | 박찬연 |
| company.name | company.name | 상호 | text | (주)유니온무역 |
| 위의신청을다음과같이신고필함 | 위의신청을다음과같이신고필함 | 위의신청을다음과같이신고필함. | text |  |

### hf220 · 해외지점 설치(변경)신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.220 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | corp.name | 상호 | text | (주)유니온무역 |
| seal.signer | seal.corp | 상호 | seal | (주)유니온무역 |
| sign.signer | sign.customer | 상호 | signature | 주식회사 한빛패션 |
| company.biz_no | corp.biz_no | 사업자(주민)번호 | biz_no | 264-82-36559 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| check.기업규모 | check.기업규모 | 기업규모 | checkbox | 중소기업 |
| check.구분 | check.구분 | 구분 | checkbox | 설치 |
| value | value | (표준산업분류코드5자리) | amount |  |
| 설치사유 | 설치사유 | 설치사유 | text | 계좌 정리 |
| 내용 | 내용 | 내용 | text | 해당 없음 |
| 사유 | 사유 | 사유 | text | 급여 수령 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| 신고번호 | 신고번호 | 신고번호 | text | 662-449450-55076 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고(보고)기관 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신고(보고)기관 | seal | 이욱유 |
| sign.signer2 | sign.signer2 | 신고(보고)기관 | signature | 박찬연 |
| company.name | company.name | 상호 | text | (주)유니온무역 |

### hf221 · 해외지사 설치·현황 보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.221 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| date | date | 일자 | date | 2026.01.31 |
| 목록[].신고자 | 목록[].신고자 | 신고자 | text | 주식회사 제일푸드 |
| 목록[].사업자번호 | 목록[].사업자번호 | 사업자(주민)번호 | biz_no | 128-48-59193 |
| 기업규모1 | 기업규모1 | 기업규모1 | text |  |
| 목록[].지사명 | 목록[].지사명 | 지사명 | text | 청솔물산 |
| 목록[].설치국가 | 목록[].설치국가 | 설치국가 | text | 중국 |
| 구분2 | 구분2 | 구분2 | text |  |
| 신고기관 | 신고기관 | 신고기관 | text |  |
| date2 | date2 | 신고일자 | date | 2026.01.31 |
| 송금일자 | 송금일자 | 송금일자 | date | 2025.07.17 |
| 송금내역 | 송금내역 | 송금내역 | text |  |
| date3 | date3 | 일자 | date | 2026.01.31 |
| 해외지사명 | 해외지사명 | 해외지사명 | text | 동방물산 |
| 설치국가 | 설치국가 | 설치국가 | text | 캐나다 |
| 회수구분주 | 회수구분주 | 회수구분주 | text |  |
| 회수금액 | 회수금액 | 회수금액 | number | 93,080,000 |
| 비고 | 비고 | 비고 | text | 해당 없음 |
| 구분주 | 구분주 | 구분주 | text |  |
| 변경일자 | 변경일자 | 변경일자 | date | 2025.10.29 |
| 변경전 | 변경전 | 변경전 | text | 해당 없음 |
| 변경후 | 변경후 | 변경후 | text | 해당 없음 |
| 지사명 | 지사명 | 지사명 | text | (주)유니온무역 |
| 취득일 | 취득일 | 취득일 | date | 2025.02.15 |
| 취득금액 | 취득금액 | 취득금액 | number | 890,000 |
| 처분일 | 처분일 | 처분일 | date | 2025-01-30 |
| 처분금액 | 처분금액 | 처분금액 | number | 790,000 |

### hf222 · 해외 부동산 취득 보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.222 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 부동산취득명의인 | 부동산취득명의인 | 부동산취득명의인 | text | 이기은 |
| 가성명또는법인명 | 가성명또는법인명 | 가.성명또는법인명 | text | 제일시스템즈(주) |
| 나주민등록번호 | 나주민등록번호 | 나.주민등록번호(사업자등록번호) | text | 1506-3935 |
| 다주소또는소재지 | 다주소또는소재지 | 다.주소또는소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 가성명또는법인명2 | 가성명또는법인명2 | 가.성명또는법인명 | text | (주)유니온무역 |
| 나주민등록번호2 | 나주민등록번호2 | 나.주민등록번호(사업자등록번호) | text | 080-844553-43059 |
| 다주소또는소재지2 | 다주소또는소재지2 | 다.주소또는소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 가상호또는성명 | 가상호또는성명 | 가.상호또는성명 | text | 가온메디칼(주) |
| 나주소또는소재지 | 나주소또는소재지 | 나.주소또는소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 가신고수리에관한사항 | 가신고수리에관한사항 | 가.신고수리에관한사항 | text |  |
| 부동산취득신고수리일및신고수리번호 | 부동산취득신고수리일및신고수리번호 | (1)부동산취득신고수리일및신고수리번호 | text | 491061-9935155 |
| 부동산취득등기일 | 부동산취득등기일 | (2)부동산취득등기일 | date | 2029.04.04 |
| 종류 | 종류 | (가)종류 | text | 하나 MMF |
| 건평 | 건평 | (나)건평 | text |  |
| 대지 | 대지 | (다)대지 | text |  |
| company.address | company.address | (2)소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| 건물가격 | 건물가격 | (가)건물가격 | text |  |
| 대지가격 | 대지가격 | (나)대지가격 | text |  |
| 부대비 | 부대비 | (다)부대비 | text |  |

### hf223 · 「외국환서식관리프로그램」전자무역업무이용(신규,변경,해지)신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.223 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.이용신청 | check.이용신청 | 이용신청 | checkbox | 무서류무역송금) (지급지시용 비밀번호 |
| check.이용신청2 | check.이용신청2 | 이용신청 | checkbox | goGlobal 전용 지급지시업무 |
| 변경신청_목록[].변경항목 | 변경신청_목록[].변경항목 | 변경항목 | text |  |
| check.지정사업자 | check.지정사업자 | 지정사업자 | checkbox | KTNet |
| check.EDI | check.EDI | EDI | checkbox | 상호대사 |
| check.계산서발신업무 | check.계산서발신업무 | 계산서발신업무 | checkbox | 계좌입금통지 |
| check.기반사업자 | check.기반사업자 | 기반사업자 | checkbox | uTradeHub |
| check.eNego | check.eNego | e-Nego | checkbox | e-L/C 통지업무 |
| check.자동승인 | check.자동승인 | 자동승인 | checkbox | 내국신용장개설승인 |
| 지급지시업무관련출금계좌_목록[].예금과목 | 지급지시업무관련출금계좌_목록[].예금과목 | 예금과목 | text | 하나 TDF 2040 |
| 신청인_목록[].수발신인식별자 | 신청인_목록[].수발신인식별자 | 수발신인식별자 | text |  |
| 지급지시업무관련출금계좌_목록[].계좌번호 | 지급지시업무관련출금계좌_목록[].계좌번호 | 계좌번호 | text | 778-049018-95570 |
| 수수료결제계좌번호 | 수수료결제계좌번호 | 수수료결제계좌번호 | number | 660,000 |
| 변경신청_목록[].변경전 | 변경신청_목록[].변경전 | 변경전 | text | 해당 없음 |
| 신청인_목록[].상세수발신식별자 | 신청인_목록[].상세수발신식별자 | 상세수발신식별자 | text |  |
| NET12 | NET12 | NET12 | text |  |
| 지급지시업무관련출금계좌_목록[].예금주 | 지급지시업무관련출금계좌_목록[].예금주 | 예금주 | text |  |
| 변경신청_목록[].변경후 | 변경신청_목록[].변경후 | 변경후 | text | 해당 없음 |
| 신청인_목록[].전자문서인증키 | 신청인_목록[].전자문서인증키 | 전자문서인증키 | text |  |
| 전자문서인증키 | 전자문서인증키 | 전자문서인증키 | text |  |
| 지급지시업무관련출금계좌_목록[].통화 | 지급지시업무관련출금계좌_목록[].통화 | 통화 | text | USD |
| seal.signer | seal.signer | 인감대조 | seal | 박찬연 |
| sign.signer | sign.signer | 인감대조 | signature | 현예지 |
| signer2.name | signer2.name | 전자무역업무기본약관수령필 | text | 박태율 |
| seal.signer2 | seal.signer2 | 전자무역업무기본약관수령필 | seal | 김승아 |
| sign.signer2 | sign.signer2 | 전자무역업무기본약관수령필 | signature | 박태율 |
| check.전자무역업무기본약관에따라아래와같이 | check.전자무역업무기본약관에따라아래와같이 | 『전자무역업무기본약관』에따라아래와같이( | checkbox | 해지)신청합니다. |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer3.name | signer3.name | 신청인 | text | 박찬연 |
| seal.signer3 | seal.customer | 신청인 | seal | 이욱유 |
| sign.signer3 | sign.customer | 신청인 | signature | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 기재사항 | 기재사항 | 기재사항 | text |  |
| 계산서 | 계산서 | 계산서 | text |  |
| 발신업무 | 발신업무 | 발신업무 | text |  |
| eNego | eNego | e-Nego | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 최소희 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김정연 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 천연예 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 최준서 |
| check.승인업무 | check.승인업무 | 승인업무 | checkbox | 승인업무 |
| check.수입업무 | check.수입업무 | 수입업무 | checkbox | 수입업무 |
| check.LC통지업무 | check.LC통지업무 | L/C통지업무(EDI) | checkbox | L/C 통지업무(EDI) |
| check.내국신용장업무 | check.내국신용장업무 | 내국신용장업무 | checkbox | 내국신용장업무 |
| check.계산서및입출금통지업무 | check.계산서및입출금통지업무 | 계산서및입출금통지업무 | checkbox | 계산서 및 입출금 통지업무 |
| check.지급지시업무 | check.지급지시업무 | 지급지시업무 | checkbox | 지급지시업무 |
| check.수출업무 | check.수출업무 | 수출업무 | checkbox | 수출업무 |
| check.외화지급보증업무 | check.외화지급보증업무 | 외화지급보증업무 | checkbox | 외화지급보증업무 |
| check.상호대사 | check.상호대사 | 상호대사 | checkbox | 상호대사 |
| check.계산서발신업무2 | check.계산서발신업무2 | 계산서발신업무 | checkbox | 계산서발신업무 |
| check.자동승인업무 | check.자동승인업무 | 자동승인업무 | checkbox | 자동승인업무 |
| check.eLC통지업무 | check.eLC통지업무 | e-L/C통지업무 | checkbox | e-L/C 통지업무 |
| check.eNego업무 | check.eNego업무 | e-Nego업무 | checkbox | e-Nego 업무 |
| 외화지급보증조건변경신청업무 | 외화지급보증조건변경신청업무 | 외화지급보증/조건변경신청업무 | amount | CNY 135,300 |
| 상호대사일반응답 | 상호대사일반응답 | 상호대사,일반응답 | text | 삼정메디칼(주) |
| check.Ο처리하실업무의 | check.Ο처리하실업무의 | Ο처리하실업무의 | checkbox | 에 V 표시를 하십시오 |
| 계산서업무입금통지업무출금통지업무 | 계산서업무입금통지업무출금통지업무 | 계산서업무,입금통지업무,출금통지업무 | text |  |
| 계좌입금통지출금통지당발송금출금통지 | 계좌입금통지출금통지당발송금출금통지 | 계좌입금통지,출금통지,당발송금출금통지 | text | 316-307155-03327 |
| 전자적매입신청업무 | 전자적매입신청업무 | 전자적매입신청업무 | text |  |
| EDI | EDI | EDI | text |  |
| 계산서발급업무 | 계산서발급업무 | 계산서발급업무 | text |  |
| eLC | eLC | e-L/C | text |  |
| 자동승인 | 자동승인 | 자동승인 | text |  |
| 지급지시업무 | 지급지시업무 | 지급지시업무 | text | 범어지점 |
| 수수료결제계좌번호2 | 수수료결제계좌번호2 | 수수료결제계좌번호 | number | 21,460,000 |
| NET122 | NET122 | NET12 | text |  |
| 전자문서인증키2 | 전자문서인증키2 | 전자문서인증키 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| seal.signer4 | seal.signer4 | 지점 | seal | 류은지 |
| sign.signer4 | sign.signer4 | 지점 | signature | 김훈승 |
| 기재사항2 | 기재사항2 | 기재사항 | text |  |
| 약정항목eLC통지업무 | 약정항목eLC통지업무 | 약정항목:e-L/C통지업무 | text |  |
| customer.name | customer.name | 신청인 | text | 박찬연 |
| 하나은행 | 하나은행 | 하나은행 | text | 카카오뱅크 |
| 수수료결제계좌번호3 | 수수료결제계좌번호3 | 수수료결제계좌번호 | number | 254,290,000 |
| 상세수발신인식별자 | 상세수발신인식별자 | 상세수발신인식별자 | text |  |
| 상세수발신인식별자2 | 상세수발신인식별자2 | 상세수발신인식별자 | text |  |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| seal.signer5 | seal.signer5 | 지점 | seal | 이상민 |
| sign.signer5 | sign.signer5 | 지점 | signature | 금은현 |
| 기재사항3 | 기재사항3 | 기재사항 | text |  |
| 계산서2 | 계산서2 | 계산서 | text |  |

### hf224 · Usance 송금 조건변경신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.224 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신청인정보 | 신청인정보 | ♣신청인정보 | text |  |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| Usance송금번호 | Usance송금번호 | Usance송금번호 | text | 711-260611-72112 |
| 통화금액 | 통화금액 | 통화금액 | number | 150,000 |
| 수취인명 | 수취인명 | 수취인명 | text | (주)삼정로지스 |
| 수취인주소및전화번호 | 수취인주소및전화번호 | 수취인주소및전화번호 | phone | 010-5907-7253 |
| 수취인주소및전화번호2 | 수취인주소및전화번호2 | 수취인주소및전화번호 | phone | 010-5907-7253 |
| 수취인계좌번호 | 수취인계좌번호 | 수취인계좌번호 | text | 389-373464-81713 |
| 수취은행BIC | 수취은행BIC | 수취은행BIC | text | 국민은행 |
| check.만기 | check.만기 | 만기(상환일) | checkbox | Fixed due date ( |
| check.만기2 | check.만기2 | 만기(상환일) | checkbox | ( |
| 기타 | 기타 | 기타 | text | 가족 명의 계좌로 이체 요청 |
| 수취은행명 | 수취은행명 | 수취은행명 | text | 신한은행 |
| 영문 | 영문 | 영문(English) | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 강순준 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| signer2.name | signer2.name | 신청인 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신청인 | seal | 이민빈 |
| sign.signer2 | sign.signer2 | 신청인 | signature | 박찬연 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 이나원 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 최건원 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 최원현 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 곽연아 |

### hf225 · Usance 송금 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.225 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신청정보 | 신청정보 | ♣신청정보 | text |  |
| 신청인정보 | 신청인정보 | ♣신청인정보 | text |  |
| 영문 | 영문 | 영문(English) | text |  |
| 한글 | 한글 | 한글(Korean) | text |  |
| check.수입형태사전송금방식만작성 | check.수입형태사전송금방식만작성 | 수입형태*사전송금방식만작성 | checkbox | 사전 통관수입 |
| check.만기 | check.만기 | 만기(상환일) | checkbox | Fixed due date ( |
| check.거래방식 | check.거래방식 | 거래방식(선적구분) | checkbox | 사후송금 방식 (선적 후) |
| 선적정보 | 선적정보 | ♣선적정보 | text |  |
| 계약서번호 | 계약서번호 | 계약서번호 | rrn | 1819-3933 |
| 상품명세 | 상품명세 | 상품명세 | text | 하나 정기예금 |
| 가격조건 | 가격조건 | 가격조건 | text |  |
| 원산지 | 원산지 | 원산지 | text |  |
| 운송서류번호사후송금방식인경우작성 | 운송서류번호사후송금방식인경우작성 | 운송서류번호(B/LNo등)*사후송금방식인경우작성 | text | 5231-5217 |
| 선적항 | 선적항 | (예정)선적항(또는공항) | text |  |
| 도착항 | 도착항 | (예정)도착항(또는공항) | text |  |
| HS코드 | HS코드 | HS코드 | number | 90726 |
| 수출국 | 수출국 | 수출국 | text |  |
| date | date | 선적(예정)일 | date | 2026년 1월 31일 |
| 선적국가 | 선적국가 | 선적국가 | text | 미국 |
| 도착국가 | 도착국가 | 도착국가 | text | 독일 |
| 수취인명 | 수취인명 | 수취인명 | text | 주식회사 누리로지스 |
| 수취인주소및전화번호 | 수취인주소및전화번호 | 수취인주소및전화번호 | phone | 010-5907-7253 |
| 수취인주소및전화번호2 | 수취인주소및전화번호2 | 수취인주소및전화번호 | phone | 010-5907-7253 |
| 수취인계좌번호 | 수취인계좌번호 | 수취인계좌번호 | text | 471-459590-30098 |
| 수취은행BIC | 수취은행BIC | 수취은행BIC | text | 카카오뱅크 |
| 송금수취인및수취은행정보 | 송금수취인및수취은행정보 | ♣송금수취인및수취은행정보 | text | 기업은행 |
| check.송금수수료부담자 | check.송금수수료부담자 | 송금수수료부담자 | checkbox | OUR |
| 수취은행명 | 수취은행명 | 수취은행명 | text | 카카오뱅크 |
| 담당자명 | 담당자명 | 담당자명 | text | 박찬연 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| TELNo | TELNo | TELNo | text | 2948-7143 |
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| 통화금액 | 통화금액 | 통화(),금액 | number | 8,200,000원 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| SWIFTCode | foreign.swift | SWIFTCode | text |  |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 현예지 |
| signer2.name | signer2.name | 신청인 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신청인 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 신청인 | signature | 강순준 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 이욱호 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 금민수 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 지채예 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 추은준 |

### hf226 · 거주자의 외화자금 차입 및 상환 현황보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.226 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].차주명 | 목록[].차주명 | 차주명 | text |  |
| 목록[].사업자등록번호 | 목록[].사업자등록번호 | 사업자등록번호 | biz_no | 264-82-36559 |
| 목록[].담당자성명 | 목록[].담당자성명 | 담당자성명 | text | 최환정 |
| 목록[].담당자전화번호 | 목록[].담당자전화번호 | 담당자전화번호 | phone | 010-5907-7253 |
| 목록[].대주명 | 목록[].대주명 | 대주명 | text |  |
| 목록[].대주소재국 | 목록[].대주소재국 | 대주소재국 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 목록[].차입근거법1 | 목록[].차입근거법1 | 차입근거법1 | text |  |
| 목록[].신고번호 | 목록[].신고번호 | 신고번호 | text | 607-006507-98562 |
| 목록[].지정거래외국환은행지점명 | 목록[].지정거래외국환은행지점명 | 지정거래외국환은행지점명 | text | 기업은행 |
| 목록[].자금용도 | 목록[].자금용도 | 자금용도 | text | 만기 해지 |
| 목록[].계약통화 | 목록[].계약통화 | 계약통화 | text | JPY |
| 목록[].계약금액 | 목록[].계약금액 | 계약금액(A) | number | 8,270,000 |
| 목록[].최초차입일자 | 목록[].최초차입일자 | 최초차입일자 | date | 2025.09.29 |
| 목록[].만기일자 | 목록[].만기일자 | 만기일자 | date | 2028-03-04 |
| 목록[].기차입액 | 목록[].기차입액 | 기차입액(B) | text |  |
| 목록[].당월차입일자 | 목록[].당월차입일자 | 당월차입일자 | date | 2025년 11월 4일 |
| 목록[].당월차입액 | 목록[].당월차입액 | 당월차입액(국내예치액)(C) | text |  |
| 목록[].차입누계 | 목록[].차입누계 | 차입누계(D=B+C+L) | text |  |
| 목록[].미차입액 | 목록[].미차입액 | 미차입액(E=A-D) | text |  |
| 목록[].기원금상환액 | 목록[].기원금상환액 | 기원금상환액(F) | number | 510,000 |
| 목록[].당월상환일자 | 목록[].당월상환일자 | 당월상환일자 | date | 2026-01-15 |
| 목록[].당월원금상환액 | 목록[].당월원금상환액 | 당월원금상환액(해외송금분)(G) | text | 23,210,000 |
| 목록[].상환잔액 | 목록[].상환잔액 | 상환잔액(I=D-F-G-H) | number | 162,980,000원 |
| 목록[].당월이자상환액 | 목록[].당월이자상환액 | 당월이자상환액 | number | 5,690,000 |
| 목록[].해외예치일자 | 목록[].해외예치일자 | 해외예치일자 | date | 2025.07.08 |
| 목록[].해외예치은행명 | 목록[].해외예치은행명 | 해외예치은행명 | text | 국민은행 |
| 목록[].해외예치은행BIC코드 | 목록[].해외예치은행BIC코드 | 해외예치은행BIC코드 | number | 033090 |
| 목록[].전월말예치잔액 | 목록[].전월말예치잔액 | 전월말예치잔액(J) | number | 8,790,000 |
| 제출자 | 제출자 | 제출자 | text |  |
| 목록[].당월예치액 | 목록[].당월예치액 | 당월예치액(K=L+M) | text |  |
| 목록[].당월예치이자 | 목록[].당월예치이자 | 당월예치이자(M) | number | 1,940,000 |
| 목록[].당월인출액 | 목록[].당월인출액 | 당월인출액(N=O+P) | text |  |
| 목록[].국내입금액 | 목록[].국내입금액 | 국내입금액(O) | number | 880,000원 |
| 목록[].해외사용액 | 목록[].해외사용액 | 해외사용액(P) | text |  |
| 목록[].당월예치잔액 | 목록[].당월예치잔액 | 당월예치잔액(Q=J+K-N) | number | 3,250,000 |
| 목록[].이자유형2 | 목록[].이자유형2 | 이자유형2 | number | 91,740,000 |
| 목록[].변동금리구분3 | 목록[].변동금리구분3 | 변동금리구분3 | number | 95 |
| 목록[].금리통화 | 목록[].금리통화 | 금리통화 | number | 95 |
| 목록[].금리수준4 | 목록[].금리수준4 | 금리수준4 | number | 95 |
| 목록[].금리스프레드5 | 목록[].금리스프레드5 | 금리스프레드(변동금리)5) | number | 95 |
| 목록[].이자지급주기6 | 목록[].이자지급주기6 | 이자지급주기6 | number | 34,240,000 |
| 목록[].Option종류7 | 목록[].Option종류7 | Option종류7 | text |  |
| 목록[].Option행사일 | 목록[].Option행사일 | Option행사일 | date | 2026.01.02 |
| 목록[].상환방법 | 목록[].상환방법 | 상환방법 | text | 혼합상환 |
| 목록[].지급보증기관8 | 목록[].지급보증기관8 | 지급보증기관8 | text |  |
| 목록[].지급보증기관본점국적국 | 목록[].지급보증기관본점국적국 | 지급보증기관본점국적국 | text |  |
| 목록[].지급보증기관명 | 목록[].지급보증기관명 | 지급보증기관명 | text | 우리은행 |

### hf227 · 거주자의 해외 증권발행 및 상환 현황 보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.227 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].발행자명 | 목록[].발행자명 | 발행자명 | text |  |
| 목록[].사업자등록번호 | 목록[].사업자등록번호 | 사업자등록번호 | biz_no | 549-35-19291 |
| 목록[].담당자성명 | 목록[].담당자성명 | 담당자성명 | text | 조채재 |
| 목록[].담당자전화번호 | 목록[].담당자전화번호 | 담당자전화번호 | phone | 010-5907-7253 |
| 목록[].대주명 | 목록[].대주명 | 대주명 | text |  |
| 목록[].대주소재국 | 목록[].대주소재국 | 대주소재국 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 목록[].신고번호 | 목록[].신고번호 | 신고번호 | text | 331792-1441248 |
| 목록[].지정거래외국환은행지점명 | 목록[].지정거래외국환은행지점명 | 지정거래외국환은행지점명 | text | 국민은행 |
| 목록[].발행일자 | 목록[].발행일자 | 발행일자 | date | 2025.10.25 |
| 목록[].발행시장소재국 | 목록[].발행시장소재국 | 발행시장소재국 | text |  |
| 목록[].자금용도 | 목록[].자금용도 | 자금용도 | text | 생활자금 |
| 목록[].증권종류1 | 목록[].증권종류1 | 증권종류1 | text |  |
| 목록[].발행통화 | 목록[].발행통화 | 발행통화 | text | AUD |
| 목록[].발행금액 | 목록[].발행금액 | 발행금액(A) | number | 40,980,000 |
| 목록[].만기일자 | 목록[].만기일자 | 만기일자 | date | 2027-05-04 |
| 목록[].당월국내예치일자 | 목록[].당월국내예치일자 | 당월국내예치일자 | date | 2025.09.05 |
| 목록[].당월국내예치액 | 목록[].당월국내예치액 | 당월국내예치액 | text |  |
| 목록[].기원금상환액 | 목록[].기원금상환액 | 기원금상환액(B) | number | 8,860,000 |
| 목록[].당월상환일자 | 목록[].당월상환일자 | 당월상환일자 | date | 2025-04-16 |
| 목록[].상환잔액 | 목록[].상환잔액 | 상환잔액(E=A-B-C-D) | number | 1,970,000 |
| 목록[].당월이자상환액 | 목록[].당월이자상환액 | 당월이자상환액 | number | 292,360,000 |
| 목록[].당월주식전환액2 | 목록[].당월주식전환액2 | 당월주식전환액2 | text |  |
| 목록[].당월말주식전환누계액3 | 목록[].당월말주식전환누계액3 | 당월말주식전환누계액3 | text |  |
| 목록[].해외예치일자 | 목록[].해외예치일자 | 해외예치일자 | date | 2025년 9월 11일 |
| 목록[].해외예치은행명 | 목록[].해외예치은행명 | 해외예치은행명 | text | 국민은행 |
| 목록[].해외예치은행BIC코드 | 목록[].해외예치은행BIC코드 | 해외예치은행BIC코드 | number | 732312 |
| 목록[].전월말예치잔액 | 목록[].전월말예치잔액 | 전월말예치잔액(F) | number | 70,420,000 |
| 제출자 | 제출자 | 제출자 | text |  |
| 목록[].당월예치액 | 목록[].당월예치액 | 당월예치액(G=H+I) | text |  |
| 목록[].당월발행대금 | 목록[].당월발행대금 | 당월발행대금(H) | number | 910,000 |
| 목록[].당월예치이자 | 목록[].당월예치이자 | 당월예치이자(I) | number | 10,270,000원 |
| 목록[].당월인출액 | 목록[].당월인출액 | 당월인출액(J=K+L) | text |  |
| 목록[].국내입금액 | 목록[].국내입금액 | 국내입금액(K) | number | 86,920,000원 |
| 목록[].해외사용액 | 목록[].해외사용액 | 해외사용액(L) | text |  |
| 목록[].당월말예치잔액 | 목록[].당월말예치잔액 | 당월말예치잔액(M=F+G-J) | number | 49,240,000 |
| 목록[].표면금리 | 목록[].표면금리 | 표면금리 | number | 20 |
| 목록[].발행비용 | 목록[].발행비용 | 발행비용(%) | text |  |
| 목록[].이자유형4 | 목록[].이자유형4 | 이자유형4 | number | 2,360,000 |
| 목록[].변동금리구분5 | 목록[].변동금리구분5 | 변동금리구분5 | number | 20 |
| 목록[].금리통화 | 목록[].금리통화 | 금리통화 | number | 20 |
| 목록[].금리수준6 | 목록[].금리수준6 | 금리수준6 | number | 20 |
| 목록[].금리스프레드7 | 목록[].금리스프레드7 | 금리스프레드(변동금리)7) | number | 20 |
| 목록[].이자지급주기8 | 목록[].이자지급주기8 | 이자지급주기8 | number | 130,000 |
| 목록[].Option종류9 | 목록[].Option종류9 | Option종류9 | text |  |
| 목록[].Option행사일10 | 목록[].Option행사일10 | Option행사일10 | text |  |
| 목록[].SWAP종류11 | 목록[].SWAP종류11 | SWAP종류11 | text |  |
| 목록[].권리행사일12 | 목록[].권리행사일12 | 권리행사일(CB,BW)12) | text |  |
| 목록[].상환방법 | 목록[].상환방법 | 상환방법 | text | 원금균등분할상환 |
| 목록[].지급보증기관13 | 목록[].지급보증기관13 | 지급보증기관13 | text |  |
| 목록[].지급보증기관본점국적국 | 목록[].지급보증기관본점국적국 | 지급보증기관본점국적국 | text |  |
| 목록[].지급보증기관명 | 목록[].지급보증기관명 | 지급보증기관명 | text | 하나은행 |

### hf228 · 담보제공신고(보고)서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.228 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 강순준 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 현예지 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| 담보제공자 | 담보제공자 | 담보제공자 | text |  |
| 담보취득자 | 담보취득자 | 담보취득자 | text |  |
| 담보제공수혜자 | 담보제공수혜자 | 담보제공수혜자 | text |  |
| check.담보물종류 | check.담보물종류 | 담보물종류 | checkbox | 부동산 |
| 담보소재지 | 담보소재지 | 담보소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 수량 | 수량 | 수량 | number | 36 |
| 담보제공기간 | 담보제공기간 | 담보제공기간 | text |  |
| check.담보제공용도 | check.담보제공용도 | 담보제공용도 | checkbox | 거주자의 현지법인의 해외리스에 대한 국내본사등의 담보제공 |
| 담보가액 | 담보가액 | 담보가액 | number | 2,930,000원 |
| 신고번호 | 신고번호 | 신고번호 | text | 0832-3910 |
| 신고금액 | 신고금액 | 신고금액 | number | 44,980,000 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 신고조건 | 신고조건 | 신고조건 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고기관 | text | 김훈은 |
| seal.signer2 | seal.signer2 | 신고기관 | seal | 김훈은 |
| sign.signer2 | sign.signer2 | 신고기관 | signature | 성성인 |
| 위의신청을다음과같이신고필함 | 위의신청을다음과같이신고필함 | 위의신청을다음과같이신고필함. | text |  |

### hf229 · 매매신고(보고)서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.229 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 강순준 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 박찬연 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| 매매대상물종류 | 매매대상물종류 | 매매대상물종류 | text |  |
| 매매사유 | 매매사유 | 매매사유 | text | 의료비 |
| 신고번호 | 신고번호 | 신고번호 | text | 059693-1410733 |
| 신고금액 | 신고금액 | 신고금액 | number | 630,000 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| seal.signer2 | seal.signer2 | 은행장 | seal | 김훈승 |
| sign.signer2 | sign.signer2 | 은행장 | signature | 이민하 |

### hf230 · 보증계약신고(보고)서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.230 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 박찬연 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 현예지 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| 보증채권자 | 보증채권자 | 보증채권자 | text |  |
| 보증채무자 | 보증채무자 | 보증채무자 | text |  |
| 보증수혜자 | 보증수혜자 | 보증수혜자 | text |  |
| 보증금액 | 보증금액 | 보증금액 | number | 8,570,000원 |
| 보증기간 | 보증기간 | 보증기간 | text |  |
| check.보증용도 | check.보증용도 | 보증용도 | checkbox | 기타( |
| 상환방법 | 상환방법 | 상환방법 | text | 만기일시상환 |
| 신고번호 | 신고번호 | 신고번호 | text | 6828-8711 |
| 신고금액 | 신고금액 | 신고금액 | number | 8,150,000 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 신고조건 | 신고조건 | 신고조건 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고기관 | text | 차연준 |
| seal.signer2 | seal.signer2 | 신고기관 | seal | 차연준 |
| sign.signer2 | sign.signer2 | 신고기관 | signature | 도은찬 |
| 위의신청을다음과같이신고필함 | 위의신청을다음과같이신고필함 | 위의신청을다음과같이신고필함. | text |  |

### hf231 · 현지금융 차입·상환·보증등 한도 운영현황 보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.231 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].보고업체명1 | 목록[].보고업체명1 | 보고업체명1)(본사명) | text | (주)유니온무역 |
| 목록[].사업자번호법인번호 | 목록[].사업자번호법인번호 | 사업자번호/법인번호 | biz_no | 544-72-36612 |
| 계 | 계 | 계 | text |  |
| 목록[].차주2 | 목록[].차주2 | 차주2 | text |  |
| 목록[].대주3대주지역 | 목록[].대주3대주지역 | 대주3)대주지역 | text |  |
| 목록[].차입구분4외화증권5 | 목록[].차입구분4외화증권5 | 차입구분4)외화증권5 | text | GBP 58,400 |
| 목록[].차입잔액6 | 목록[].차입잔액6 | 차입잔액6 | text | 4,350,000 |
| 목록[].금리7 | 목록[].금리7 | 금리7)(bp) | text | 30 |
| 목록[].차입일8 | 목록[].차입일8 | 차입일8 | text |  |
| 목록[].만기일8 | 목록[].만기일8 | 만기일8 | text | 2028-07-01 |
| 목록[].보증9 | 목록[].보증9 | 보증9 | text |  |
| 목록[].용도10 | 목록[].용도10 | 용도10 | text | 사업자금 |
| 제출자 | 제출자 | 제출자 | text |  |

### hf232 · 증권발행 신고(보고)서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.232 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 강순준 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 박찬연 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| 상호기타명칭 | 상호기타명칭 | 상호기타명칭 | text | (주)세진푸드 |
| 증권종류 | 증권종류 | 증권종류 | text |  |
| 발행금액 | 발행금액 | 발행금액 | number | 163,640,000 |
| 계약체결시기및장소 | 계약체결시기및장소 | 계약체결시기및장소 | text |  |
| 표면금리 | 표면금리 | 표면금리 | number | 40 |
| 만기 | 만기 | 만기 | date | 2025년 11월 15일 |
| 배당금지급시기및방법 | 배당금지급시기및방법 | 배당금지급시기및방법 | text |  |
| 원리금상환방법 | 원리금상환방법 | 원리금상환방법 | text | 원리금균등분할상환 |
| 자금용도 | 자금용도 | 자금용도 | text | 결혼자금 |
| 발행관련기관 | 발행관련기관 | 발행관련기관 | text |  |
| 액면금액및수량 | 액면금액및수량 | 액면금액및수량 | number | 34,370,000 |
| 발행시기및장소 | 발행시기및장소 | 발행시기및장소 | text |  |
| 발행가격 | 발행가격 | 발행가격 | text |  |
| 해외판매여부 | 해외판매여부 | 해외판매여부 | text |  |
| 신고번호 | 신고번호 | 신고번호 | text | 7911-4480 |
| 신고금액 | 신고금액 | 신고금액 | number | 350,000 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 신고조건 | 신고조건 | 신고조건 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고기관 | text | 김형현 |
| seal.signer2 | seal.signer2 | 신고기관 | seal | 임도윤 |
| sign.signer2 | sign.signer2 | 신고기관 | signature | 방혜하 |
| 위의신청을다음과같이신고필함 | 위의신청을다음과같이신고필함 | 위의신청을다음과같이신고필함. | text |  |

### hf233 · 금전의 대차계약 신고(보고)서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.233 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | signer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 김아진 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 박찬연 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| customer.name | customer.name | 차주 | text | 박찬연 |
| 대주 | 대주 | 대주 | text |  |
| 통화및금액 | 통화및금액 | 통화및금액 | number | 93,380,000 |
| 차입일대출일 | 차입일대출일 | 차입일/대출일 | date | 2025-04-03 |
| 대차기간 | 대차기간 | 대차기간 | text |  |
| 사용용도 | 사용용도 | 사용용도 | text | 만기 해지 |
| 상환방법 | 상환방법 | 상환방법 | text | 원금균등분할상환 |
| 신고번호 | 신고번호 | 신고번호 | text | 867598-7395967 |
| 신고금액 | 신고금액 | 신고금액 | number | 47,430,000원 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 신고조건 | 신고조건 | 신고조건 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고기관 | text | 이소희 |
| seal.signer2 | seal.signer2 | 신고기관 | seal | 이소희 |
| sign.signer2 | sign.signer2 | 신고기관 | signature | 위준호 |
| 위의신청을다음과같이신고필함 | 위의신청을다음과같이신고필함 | 위의신청을다음과같이신고필함. | text |  |

### hf234 · 외화송금의 내용변경 및 취소, 송금수표 분실신고 등 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.234 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.송금방법 | check.송금방법 | 송금방법 | checkbox | 송금수표(D/D) |
| 송금일자 | 송금일자 | 송금일자 | date | 2025년 7월 11일 |
| 송금번호 | 송금번호 | 송금번호(수표번호) | text | 5037-0911 |
| 수취인 | 수취인 | 수취인 | text | 주식회사 신영상사 |
| value | value | [전신송금내용변경기재란] | amount |  |
| check.전신송금 | check.전신송금 | 전신송금 | checkbox | 전신송금 지급여부조회 |
| check.송금수표 | check.송금수표 | 송금수표 | checkbox | 송금수표 분실신고 |
| 거래은행 | 거래은행 | 거래은행 | text | 카카오뱅크 |
| foreign.account | foreign.account | 계좌번호 | account_no | 884779361534 |
| foreign.name | foreign.name | 성명 | text | Mekong Garment JSC |
| foreign.address | foreign.address | 주소 | text | 45 Le Loi St, District 1, Ho Chi Minh City |
| foreign.phone | foreign.phone | 전화번호 | text | John Miller |
| 기타 | 기타 | 기타(사유등) | text | 해당 없음 |
| 수취인_목록[].변경후 | 수취인_목록[].변경후 | 변경후 | text | 해당 없음 |
| 변경후 | 변경후 | 변경후 | text | 해당 없음 |
| 송금인 | 송금인 | 송금인 | text |  |
| customer.birth | customer.birth | 생년월일/사업자번호 | date | 1990.02.10 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| customer.email | customer.email | E-mail주소 | text | chanyeon363@naver.com |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 천다준 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 확인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 나호정 |

### hf235 · 외국인투자기업등록(변경등록)신청서(국문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.235 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 접수일 | 접수일 | 접수일 | text |  |
| 처리일 | 처리일 | 처리일 | text |  |
| 처리기간1일 | 처리기간1일 | 처리기간1일 | date | 2025.09.05 |
| 상호또는명칭 | 상호또는명칭 | 상호또는명칭(영문) | text | (주)유니온무역 |
| 신고된사업명 | 신고된사업명 | 신고(허가)된사업명 | text |  |
| 자본금 | 자본금 | 자본금(출연금) | text |  |
| value | value | (국문) | amount |  |
| value2 | value2 | (영문) | amount |  |
| SPC여부예아니오 | SPC여부예아니오 | (*)SPC여부[]예[]아니오 | text |  |
| 본사 | 본사 | 본사 | text |  |
| 주공장소재지 | 주공장소재지 | 주공장(주사업장)소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 홈페이지 | 홈페이지 | 홈페이지 | text |  |
| 액면총액 | 액면총액 | 액면총액 | number | 44,830,000 |
| 상호또는명칭2 | 상호또는명칭2 | 상호또는명칭(영문) | text | (주)누리상사 |
| 상호또는명칭3 | 상호또는명칭3 | 상호또는명칭(영문) | text | 주식회사 미래물산 |
| 대표Email | 대표Email | 대표E-mail | text | chanyeon363@naver.com |
| customer.nationality | customer.nationality | 국적 | text | 대한민국 |
| customer.nationality2 | customer.nationality2 | 국적 | text | 대한민국 |
| customer.nationality3 | customer.nationality3 | 국적 | text | 대한민국 |
| 액면총액2 | 액면총액2 | 액면총액 | number | 40 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신고인또는신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신고인또는신청인 | seal | 강순준 |
| sign.signer | sign.customer | 신고인또는신청인 | signature | 박찬연 |
| 접수번호 | 접수번호 | 접수번호 | text |  |
| 투자기업 | 투자기업 | 투자기업 | text |  |
| 상당 | 상당 | 상당 | text |  |
| 등록후예상규모 | 등록후예상규모 | 등록후예상규모(신규및변경등록) | number | 36 |
| 투자기업2 | 투자기업2 | 투자기업 | text |  |
| 양도또는감소할 | 양도또는감소할 | 양도또는감소할 | text |  |
| 액면총액3 | 액면총액3 | 액면총액(A×B) | number | 4,650,000 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 임재수 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 강욱민 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 마환도 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이규주 |
| check.송달받는것에대하여 | check.송달받는것에대하여 | 송달받는것에대하여 | checkbox | 동의하지 않습니다. |
| 신규등록인경우 | 신규등록인경우 | <신규등록인경우> | text |  |

### hf236 · 해외예금 및 신탁 잔액 보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.236 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 개설인명 | 개설인명 | 개설인명 | text |  |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.biz_no | corp.biz_no | 사업자(주민)등록번호 | biz_no | 264-82-36559 |
| 직위성명 | 직위성명 | 직위‧성명 | text | 박찬연 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| 예금종류1 | 예금종류1 | 예금종류1 | text | 하나 정기예금 |
| 예금기관명2 | 예금기관명2 | 예금기관명2 | text | 농협은행 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| 국가명3 | 국가명3 | 국가명3 | text | 필리핀 |
| 전년말잔액 | 전년말잔액 | 전년말잔액(A) | number | 4,290,000 |
| 국내송금 | 국내송금 | 국내송금 | text |  |
| 해외입금수출대금외화증권처분예금신탁처분기타계 | 해외입금수출대금외화증권처분예금신탁처분기타계 | 해외입금수출대금외화증권처분예금‧신탁처분기타계 | amount | USD 26,400 |
| 해외입금수출대금외화증권처분예금신탁처분기타계2 | 해외입금수출대금외화증권처분예금신탁처분기타계2 | 해외입금수출대금외화증권처분예금‧신탁처분기타계 | amount | USD 37,600 |
| 해외입금수출대금외화증권처분예금신탁처분기타계3 | 해외입금수출대금외화증권처분예금신탁처분기타계3 | 해외입금수출대금외화증권처분예금‧신탁처분기타계 | amount | USD 83,600 |
| 해외입금수출대금외화증권처분예금신탁처분기타계4 | 해외입금수출대금외화증권처분예금신탁처분기타계4 | 해외입금수출대금외화증권처분예금‧신탁처분기타계 | amount | USD 143,300 |
| 해외입금수출대금외화증권처분예금신탁처분기타계5 | 해외입금수출대금외화증권처분예금신탁처분기타계5 | 해외입금수출대금외화증권처분예금‧신탁처분기타계 | amount | JPY 86,100 |
| 해외입금수출대금외화증권처분예금신탁처분기타계6 | 해외입금수출대금외화증권처분예금신탁처분기타계6 | 해외입금수출대금외화증권처분예금‧신탁처분기타계 | amount | CAD 199,600 |
| 목록[].금액 | 목록[].금액 | 금액 | text | 34,060,000 |
| 금액 | 금액 | 금액 | number | 520,000 |
| 국내회수 | 국내회수 | 국내회수 | text |  |
| 해외처분수입대금지급외화증권취득예금신탁예치기타계 | 해외처분수입대금지급외화증권취득예금신탁예치기타계 | 해외처분수입대금지급외화증권취득예금‧신탁예치기타계 | amount | AUD 119,900 |
| 해외처분수입대금지급외화증권취득예금신탁예치기타계2 | 해외처분수입대금지급외화증권취득예금신탁예치기타계2 | 해외처분수입대금지급외화증권취득예금‧신탁예치기타계 | amount | USD 83,800 |
| 해외처분수입대금지급외화증권취득예금신탁예치기타계3 | 해외처분수입대금지급외화증권취득예금신탁예치기타계3 | 해외처분수입대금지급외화증권취득예금‧신탁예치기타계 | amount | CNY 168,700 |
| 해외처분수입대금지급외화증권취득예금신탁예치기타계4 | 해외처분수입대금지급외화증권취득예금신탁예치기타계4 | 해외처분수입대금지급외화증권취득예금‧신탁예치기타계 | amount | AUD 165,300 |
| 해외처분수입대금지급외화증권취득예금신탁예치기타계5 | 해외처분수입대금지급외화증권취득예금신탁예치기타계5 | 해외처분수입대금지급외화증권취득예금‧신탁예치기타계 | amount | AUD 43,400 |
| 해외처분수입대금지급외화증권취득예금신탁예치기타계6 | 해외처분수입대금지급외화증권취득예금신탁예치기타계6 | 해외처분수입대금지급외화증권취득예금‧신탁예치기타계 | amount | USD 24,400 |
| 연중이자 | 연중이자 | 연중이자(D) | number | 650,000원 |
| 금년말잔액 | 금년말잔액 | 금년말잔액(A+B-C+D) | number | 8,800,000 |
| date | date | 작성일 | date | 2026년 1월 31일 |

### hf237 · 해외예금 입금보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.237 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 개설인명 | 개설인명 | 개설인명 | text |  |
| customer.rrn | customer.rrn | 주민등록번호(사업자등록번호) | rrn | 900210-1****** |
| 입금일자 | 입금일자 | 입금일자 | date | 2025-08-30 |
| 예금종류2 | 예금종류2 | 예금종류2 | text | 하나 단기채 펀드 |
| 예금기관명 | 예금기관명 | 예금기관명 | text | 하나은행 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| 입금액3 | 입금액3 | 입금액3 | number | 2,550,000 |
| 입금재원4 | 입금재원4 | 입금재원4 | text |  |
| 국가명5 | 국가명5 | 국가명5 | text | 일본 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer.name | corp.ceo | 대표자성명1 | text | 박찬연 |
| seal.signer | seal.corp | 대표자성명1 | seal | 강순준 |
| sign.signer | sign.customer | 대표자성명1 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |

### hf238 · 해외직접투자사업 청산 및 대부채권 회수보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.238 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 상호또는성명 | 상호또는성명 | 상호또는성명 | text | (주)유니온무역 |
| company.address | corp.address | 소재지(주소) | text | 서울특별시 중구 다산로 361, 6층 |
| company.biz_no | corp.biz_no | 사업자(주민)등록번호 | biz_no | 264-82-36559 |
| 현지법인명 | 현지법인명 | 현지법인명 | text | (주)청솔무역 |
| company.address2 | company.address2 | 소재지(주소) | text | 서울특별시 중구 다산로 361, 6층 |
| check.법인형태 | check.법인형태 | 법인형태 | checkbox | 개인기업 |
| check.투자형태주1 | check.투자형태주1 | 투자형태주1 | checkbox | 합작투자(한국측 투자비율 |
| 납입자본금 | 납입자본금 | 납입자본금 | text |  |
| 대부금액 | 대부금액 | 대부금액 | number | 25,620,000 |
| 기회수금액 | 기회수금액 | 기회수금액 | number | 5,440,000 |
| 금회회수금액 | 금회회수금액 | 금회회수금액 | number | 45,770,000원 |
| 잔액 | 잔액 | 잔액 | number | 67,730,000 |
| date | date | 일자 | date | 2026년 01월 31일 |
| 목록[].원금 | 목록[].원금 | 원금 | number | 147,050,000원 |
| 회수금액_목록[].원금 | 회수금액_목록[].원금 | 원금 | number | 1,540,000 |
| 유동자산투자및기타자산고정자산이연자산 | 유동자산투자및기타자산고정자산이연자산 | 유동자산투자및기타자산고정자산이연자산 | text |  |
| 유동부채고정부채이연부채자본금잉여금 | 유동부채고정부채이연부채자본금잉여금 | 유동부채고정부채이연부채자본금잉여금 | text |  |
| check.청산 | check.청산 | 청산 | checkbox | 청산 |
| 청산종료일 | 청산종료일 | 청산종료일 | date | 2026.09.27 |
| 목록[].구분회수일자 | 목록[].구분회수일자 | 구분회수일자 | date | 2025.02.07 |
| 목록[].회수재산의종류 | 목록[].회수재산의종류 | 회수재산의종류 | text |  |
| 계 | 계 | 계 | text |  |
| 목록[].금액 | 목록[].금액 | 금액 | text | 31,430,000 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| 다청산손익 | 다청산손익 | 다.청산손익(해산일로부터청산종료일까지의손익) | text |  |
| 바회수가불가능한재산이있을경우그내역및사유 | 바회수가불가능한재산이있을경우그내역및사유 | 바.회수가불가능한재산이있을경우그내역및사유 | text | 결혼자금 |
| 회수되어야할재산 | 회수되어야할재산 | -회수되어야할재산 | text |  |

### hf239 · 해외 부동산 처분(변경)신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.239 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 처분전부동산명의인 | 처분전부동산명의인 | 처분(변경)전부동산명의인 | text | 최원지 |
| 가성명또는법인명 | 가성명또는법인명 | 가.성명또는법인명 | text | 새한메디칼 |
| 나주민등록번호 | 나주민등록번호 | 나.주민등록번호(사업자등록번호) | text | 483779-6579687 |
| 다주소또는소재지 | 다주소또는소재지 | 다.주소또는소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 가성명또는법인명2 | 가성명또는법인명2 | 가.성명또는법인명 | text | (주)유니온무역 |
| 나주민등록번호2 | 나주민등록번호2 | 나.주민등록번호(사업자등록번호) | text | 420-940119-13436 |
| 다주소또는소재지2 | 다주소또는소재지2 | 다.주소또는소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 가부동산의명세 | 가부동산의명세 | 가.부동산의명세(종류,수량,가격등) | text |  |
| 나부동산의소재지 | 나부동산의소재지 | 나.부동산의소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 가부동산처분등기일 | 가부동산처분등기일 | 가.부동산처분등기일 | date | 2028-04-29 |
| 나처분가격 | 나처분가격 | 나.처분가격 | text |  |
| 다기타지급비용 | 다기타지급비용 | 다.기타지급비용 | text |  |
| 라국내회수금액 | 라국내회수금액 | 라.국내회수금액 | number | 170,490,000 |
| 바신고인과국내회수금액수취인과의관계 | 바신고인과국내회수금액수취인과의관계 | 바.신고인과국내회수금액수취인과의관계 | number | 5,740,000원 |
| 해외부동산변경내용 | 해외부동산변경내용 | 해외부동산변경내용 | text | 해당 없음 |

### hf240 · 외화증권(채권)취득보고서(법인 및 개인기업 설립보고서 포함)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.240 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 상호또는성명 | 상호또는성명 | 상호또는성명 | text | 세진테크(주) |
| company.address | corp.address | 소재지(주소) | text | 서울특별시 중구 다산로 361, 6층 |
| check.투자자규모 | check.투자자규모 | 투자자규모 | checkbox | 중소기업 |
| date | date | 신고일자 | date | 2026.01.31 |
| 설립년월일 | 설립년월일 | 설립년월일 | date | 2024-12-30 |
| 신고번호 | 신고번호 | 신고번호 | text | 925515-2779752 |
| company.name | corp.name | 법인명 | text | (주)유니온무역 |
| company.address2 | company.address2 | 소재지(주소) | text | 서울특별시 중구 다산로 361, 6층 |
| check.법인형태 | check.법인형태 | 법인형태 | checkbox | 해외자원개발사업 |
| check.투자형태주1 | check.투자형태주1 | 투자형태주1 | checkbox | 단독투자 |
| 설립등기일 | 설립등기일 | 설립등기일 | date | 2025.02.20 |
| 납입자본금 | 납입자본금 | 납입자본금 | text |  |
| 영업개시일 | 영업개시일 | 영업개시(예정)일 | date | 2025.04.23 |
| 결산일 | 결산일 | 결산일 | date | 2025.10.14 |
| 증권취득일 | 증권취득일 | 증권취득일(자본금출자일) | date | 2025-10-03 |
| 액면가액합계 | 액면가액합계 | 액면가액합계 | number | 15,250,000 |
| check.증권발행여부 | check.증권발행여부 | 증권발행여부 | checkbox | 증권발행 |
| 증권종류 | 증권종류 | 증권종류 | text |  |
| 취득가액합계 | 취득가액합계 | 취득가액합계 | number | 294,400,000원 |
| 채권취득일 | 채권취득일 | 채권취득일 | date | 2025.06.11 |
| 이자율 | 이자율 | 이자율 | number | 10 |
| check.원금회수방법 | check.원금회수방법 | 원금회수방법 | checkbox | 분할회수( |
| 대부원금 | 대부원금 | 대부원금 | number | 110,440,000 |
| 대부기간 | 대부기간 | 대부기간 | text |  |
| check.외화증권 | check.외화증권 | 외화증권 | checkbox | 외화증권 |

### hf241 · 대외지급보증 조건변경 신청서(SWIFT 방식)(2D)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.241 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.전문사본요청합니다 | check.전문사본요청합니다 | 전문사본요청합니다. | checkbox | 전문 사본 요청합니다. |
| FAXorEMAIL | FAXorEMAIL | FAXorE-MAIL | phone | 043-783-2775 |
| 보증서번호 | 보증서번호 | 보증서번호 | text | 자바28075003 |
| 보증서증액 | 보증서증액 | 보증서증액 | text |  |
| 보증서감액 | 보증서감액 | 보증서감액 | text |  |
| 만기일자 | 만기일자 | (변경후)만기일자(년/월/일) | date | 2026-09-25 |
| 기타조건변경 | 기타조건변경 | 기타조건변경 | text | 해당 없음 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이형재 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 심나우 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 확인 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 명상하 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 강순준 |

### hf242 · 대외지급보증 발급 신청서(SWIFT 방식)(2D)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.242 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.전문사본요청합니다 | check.전문사본요청합니다 | 전문사본요청합니다. | checkbox | 전문 사본 요청합니다. |
| FAXorEMAIL | FAXorEMAIL | FAXorE-MAIL | phone | 043-783-2775 |
| ExpiryDate | ExpiryDate | ExpiryDate(년/월/일) | date | 2026-01-30 |
| Applicant | Applicant | Applicant | text | 주식회사 세진화학 |
| Beneficiary | Beneficiary | Beneficiary | text |  |
| Beneficiary2 | Beneficiary2 | Beneficiary | text |  |
| Beneficiary3 | Beneficiary3 | Beneficiary | text |  |
| AdvisingBank | AdvisingBank | AdvisingBank | text |  |
| UndertakingAmount | UndertakingAmount | UndertakingAmount(보증금액) | number | 132,570,000 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 윤석재 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김동원 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 선우상도 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김민호 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 확인 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 추현준 |
| UndertakingtermsandConditions | UndertakingtermsandConditions | UndertakingtermsandConditions | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 강순준 |

### hf243 · 외국환거래 UMS통지서비스 (변경)신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.243 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 당발송금 | 당발송금 | 당발송금 | text |  |
| 타발송금내도통지 | 타발송금내도통지 | 타발송금내도통지 | text |  |
| 타발송금입금통지 | 타발송금입금통지 | 타발송금입금통지 | text |  |
| 외화수표추심 | 외화수표추심 | 외화수표추심 | amount | CAD 161,900 |
| 로칼서류접수 | 로칼서류접수 | 로칼서류접수 | text |  |
| check.수입선적서류접수 | check.수입선적서류접수 | 수입선적서류접수( | checkbox | 고객별 |
| 수출네고특사번호통지 | 수출네고특사번호통지 | 수출네고특사번호통지 | text | 2843-6109 |
| customer.name | customer.name | 고객명 | text | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.당발송금 | check.당발송금 | 당발송금 | checkbox | SMS |
| check.타발송금내도통지 | check.타발송금내도통지 | 타발송금내도통지 | checkbox | SMS |
| check.타발송금입금통지 | check.타발송금입금통지 | 타발송금입금통지 | checkbox | FAX |
| check.외화수표추심 | check.외화수표추심 | 외화수표추심 | checkbox | FAX |
| check.로칼서류접수 | check.로칼서류접수 | 로칼서류접수 | checkbox | FAX |
| check.FAX | check.FAX | FAX | checkbox | E-MAIL |
| check.수출네고특사번호통지 | check.수출네고특사번호통지 | 수출네고특사번호통지 | checkbox | E-MAIL |
| check.수출입금통지 | check.수출입금통지 | 수출입금통지(매입/추심포함) | checkbox | FAX |
| check.수출인수통지 | check.수출인수통지 | 수출인수통지(매입/추심포함) | checkbox | E-MAIL |
| company.biz_no | corp.biz_no | 사업자등록번호(생년월일) | biz_no | 264-82-36559 |
| SMS수신전화번호 | SMS수신전화번호 | SMS수신전화번호 | phone | 010-5907-7253 |
| FAX번호 | FAX번호 | FAX번호 | phone | 043-783-2775 |
| customer.email | customer.email | E-MAIL주소 | text | chanyeon363@naver.com |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| check.외국환업무에대한UMS통지서비스 | check.외국환업무에대한UMS통지서비스 | 외국환업무에대한UMS통지서비스( | checkbox | 변경) 를 신청합니다. |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 이욱유 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| 수출입금통지 | 수출입금통지 | 수출입금통지(매입/추심포함) | text |  |
| 수출인수통지 | 수출인수통지 | 수출인수통지(매입/추심포함) | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 박민빈 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 나건인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 임민경 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 주순현 |

### hf244 · 자본재 등 도입물품명세 검토ㆍ확인신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.244 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 접수일 | 접수일 | 접수일 | text |  |
| 처리일 | 처리일 | 처리일 | text |  |
| 신고된사업명 | 신고된사업명 | 신고된사업명 | text |  |
| 상호또는명칭 | 상호또는명칭 | 상호또는명칭(영문) | text | 주식회사 세진메디칼 |
| customer.nationality | customer.nationality | 국적 | text | 대한민국 |
| HSK분류번호 | HSK분류번호 | HSK분류번호 | text | 296-732138-80222 |
| 품명 | 품명 | 품명 | text | 자동차 부품 |
| 수량 | 수량 | 수량 | number | 36 |
| 규격 | 규격 | 규격 | text | 자동차 부품 |
| 제작자 | 제작자 | 제작자 | text |  |
| 금액 | 금액 | 금액(기준통화ᆞ도입통화) | number | 10,250,000 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신고인(또는대리인) | text | 박찬연 |
| seal.signer | seal.customer | 신고인(또는대리인) | seal | 박찬연 |
| sign.signer | sign.customer | 신고인(또는대리인) | signature | 최우빈 |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| 접수번호 | 접수번호 | 접수번호 | text |  |
| 상호또는명칭2 | 상호또는명칭2 | 상호또는명칭(영문) | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 외국인투자금액및비율 | 외국인투자금액및비율 | 외국인투자금액및비율 | number | 60 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 검인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김철희 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 공훈수 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 심진혜 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 이재희 |
| 접수일2 | 접수일2 | 접수일 | text |  |
| 처리일2 | 처리일2 | 처리일 | text |  |
| 신고된사업명2 | 신고된사업명2 | 신고된사업명 | text |  |
| 상호또는명칭3 | 상호또는명칭3 | 상호또는명칭(영문) | text | 제일물산(주) |
| customer.nationality2 | customer.nationality2 | 국적 | text | 대한민국 |
| HSK분류번호2 | HSK분류번호2 | HSK분류번호 | text | 189394-2829342 |
| 품명2 | 품명2 | 품명 | text | 커피 원두 |
| 수량2 | 수량2 | 수량 | number | 6 |
| 규격2 | 규격2 | 규격 | text | 포장재 |
| 제작자2 | 제작자2 | 제작자 | text |  |
| 금액2 | 금액2 | 금액(기준통화ᆞ도입통화) | number | 212,710,000 |
| date4 | date4 | 작성일 | date | 2026년 1월 31일 |
| date5 | date5 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고인(또는대리인) | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신고인(또는대리인) | seal | 이욱유 |
| sign.signer2 | sign.signer2 | 신고인(또는대리인) | signature | 박찬연 |
| date6 | date6 | 작성일 | date | 2026년 1월 31일 |
| 접수번호2 | 접수번호2 | 접수번호 | text |  |
| 상호또는명칭4 | 상호또는명칭4 | 상호또는명칭(영문) | text | 유니온테크(주) |
| company.biz_no2 | company.biz_no2 | 사업자등록번호 | biz_no | 264-82-36559 |
| 외국인투자금액및비율2 | 외국인투자금액및비율2 | 외국인투자금액및비율 | number | 60 |
| 접수일3 | 접수일3 | 접수일 | text |  |
| 처리일3 | 처리일3 | 처리일 | text |  |
| 신고된사업명3 | 신고된사업명3 | 신고된사업명 | text |  |
| 상호또는명칭5 | 상호또는명칭5 | 상호또는명칭(영문) | text | (주)유니온무역 |
| customer.nationality3 | customer.nationality3 | 국적 | text | 대한민국 |
| HSK분류번호3 | HSK분류번호3 | HSK분류번호 | text | 720276-2611603 |
| 품명3 | 품명3 | 품명 | text | 의류 원단 |
| 수량3 | 수량3 | 수량 | number | 60 |
| 규격3 | 규격3 | 규격 | text | 포장재 |
| 제작자3 | 제작자3 | 제작자 | text |  |
| 금액3 | 금액3 | 금액(기준통화ᆞ도입통화) | number | 6,400,000 |
| date7 | date7 | 작성일 | date | 2026년 1월 31일 |
| date8 | date8 | 작성일 | date | 2026년 1월 31일 |
| signer3.name | signer3.name | 신고인(또는대리인) | text | 박찬연 |
| seal.signer3 | seal.signer3 | 신고인(또는대리인) | seal | 박찬연 |
| sign.signer3 | sign.signer3 | 신고인(또는대리인) | signature | 김연지 |
| date9 | date9 | 작성일 | date | 2026년 1월 31일 |
| 접수번호3 | 접수번호3 | 접수번호 | text |  |
| 상호또는명칭6 | 상호또는명칭6 | 상호또는명칭(영문) | text | 대성로지스 |
| company.biz_no3 | company.biz_no3 | 사업자등록번호 | biz_no | 264-82-36559 |
| 외국인투자금액및비율3 | 외국인투자금액및비율3 | 외국인투자금액및비율 | number | 70 |

### hf245 · 장기차관 방식의 외국인투자신고서, 변경신고서(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.245 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | Name | text | 박찬연 |
| customer.address | customer.address | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.name2 | customer.name2 | Name | text | 박찬연 |
| customer.address2 | customer.address2 | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| Cash | Cash | Cash | text |  |
| PurposeofLoan | PurposeofLoan | PurposeofLoan | text |  |
| RateofInterest | RateofInterest | RateofInterest | text |  |
| Capitalinkind | Capitalinkind | Capitalinkind | text |  |
| customer.nationality | customer.nationality | Nationality | text | 대한민국 |
| AverageLoanPeriod | AverageLoanPeriod | AverageLoanPeriod | text |  |
| Other | Other | Other | text |  |
| Other2 | Other2 | Other | text |  |
| LocationofInvestment | LocationofInvestment | LocationofInvestment | text |  |
| ChangeinInformation | ChangeinInformation | ChangeinInformation | text |  |
| InformationAfterChange | InformationAfterChange | InformationAfterChange | text |  |
| NotificationNo | NotificationNo | NotificationNo | text | 7890-6065 |
| ReceiptNumber | ReceiptNumber | ReceiptNumber | text |  |
| DateofReceipt | DateofReceipt | DateofReceipt | date | 2025.09.29 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 변태하 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 확인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 채건준 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 서재현 |
| customer.name3 | customer.name3 | Name | text | 박찬연 |
| customer.address3 | customer.address3 | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.name4 | customer.name4 | Name | text | 박찬연 |
| customer.address4 | customer.address4 | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| Cash2 | Cash2 | Cash | text |  |
| PurposeofLoan2 | PurposeofLoan2 | PurposeofLoan | text |  |
| RateofInterest2 | RateofInterest2 | RateofInterest | text |  |
| Capitalinkind2 | Capitalinkind2 | Capitalinkind | text |  |
| customer.nationality2 | customer.nationality2 | Nationality | text | 대한민국 |
| AverageLoanPeriod2 | AverageLoanPeriod2 | AverageLoanPeriod | text |  |
| Other3 | Other3 | Other | text |  |
| Other4 | Other4 | Other | text |  |
| LocationofInvestment2 | LocationofInvestment2 | LocationofInvestment | text |  |
| ChangeinInformation2 | ChangeinInformation2 | ChangeinInformation | text |  |
| InformationAfterChange2 | InformationAfterChange2 | InformationAfterChange | text |  |
| NotificationNo2 | NotificationNo2 | NotificationNo | text | 708-739297-37411 |
| ReceiptNumber2 | ReceiptNumber2 | ReceiptNumber | text |  |
| DateofReceipt2 | DateofReceipt2 | DateofReceipt | date | 2025.01.31 |

### hf246 · 장기차관 방식의 외국인투자신고서, 변경신고서(국문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.246 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 접수일 | 접수일 | 접수일 | text |  |
| 처리일 | 처리일 | 처리일 | text |  |
| 상호또는명칭 | 상호또는명칭 | 상호또는명칭 | text | 가온로지스 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 상호또는명칭2 | 상호또는명칭2 | 상호또는명칭(영문) | text | 우진로지스(주) |
| customer.address2 | customer.address2 | 주소(영문) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 현금 | 현금 | 현금 | text |  |
| 차관용도 | 차관용도 | 차관용도 | text | 급여 수령 |
| 연이자율 | 연이자율 | 연이자율 | number | 40 |
| 자본재 | 자본재 | 자본재 | text |  |
| customer.nationality | customer.nationality | 국적 | text | 대한민국 |
| 평균차관기간 | 평균차관기간 | 평균차관기간 | text |  |
| 기타 | 기타 | 기타 | text | 해당 없음 |
| 기타2 | 기타2 | 기타 | text | 해당 없음 |
| 금번투자지역 | 금번투자지역 | 금번투자지역 | text |  |
| 변경신고의경우변경내용 | 변경신고의경우변경내용 | 변경신고의경우변경내용 | text | 해당 없음 |
| 변경후내용 | 변경후내용 | 변경후내용 | text | 해당 없음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신고인(또는대리인) | text | 박찬연 |
| seal.signer | seal.customer | 신고인(또는대리인) | seal | 강순준 |
| sign.signer | sign.customer | 신고인(또는대리인) | signature | 박찬연 |
| 신고번호 | 신고번호 | 신고번호 | text | 833-741399-25438 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 접수번호 | 접수번호 | 접수번호 | text |  |
| 신고인경우 | 신고인경우 | <신고인경우> | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 현주연 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 박미재 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김수인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이현린 |
| 접수일2 | 접수일2 | 접수일 | text |  |
| 처리일2 | 처리일2 | 처리일 | text |  |
| 상호또는명칭3 | 상호또는명칭3 | 상호또는명칭 | text | (주)유니온무역 |
| customer.address3 | customer.address3 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 상호또는명칭4 | 상호또는명칭4 | 상호또는명칭(영문) | text | (주)유니온무역 |
| customer.address4 | customer.address4 | 주소(영문) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 현금2 | 현금2 | 현금 | text |  |
| 차관용도2 | 차관용도2 | 차관용도 | text | 결혼자금 |
| 연이자율2 | 연이자율2 | 연이자율 | number | 40 |
| 자본재2 | 자본재2 | 자본재 | text |  |
| customer.nationality2 | customer.nationality2 | 국적 | text | 대한민국 |
| 평균차관기간2 | 평균차관기간2 | 평균차관기간 | text |  |
| 기타3 | 기타3 | 기타 | text | 해당 없음 |
| 기타4 | 기타4 | 기타 | text | 해당 없음 |
| 금번투자지역2 | 금번투자지역2 | 금번투자지역 | text |  |
| 변경신고의경우변경내용2 | 변경신고의경우변경내용2 | 변경신고의경우변경내용 | text | 해당 없음 |
| 변경후내용2 | 변경후내용2 | 변경후내용 | text | 해당 없음 |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고인(또는대리인) | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신고인(또는대리인) | seal | 이민빈 |
| sign.signer2 | sign.signer2 | 신고인(또는대리인) | signature | 박찬연 |
| 신고번호2 | 신고번호2 | 신고번호 | text | 109704-6865606 |
| date4 | date4 | 작성일 | date | 2026년 1월 31일 |
| 접수번호2 | 접수번호2 | 접수번호 | text |  |
| 신고인경우2 | 신고인경우2 | <신고인경우> | text |  |

### hf247 · 외국인투자기업등록(변경등록)신청서(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.247 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| ReceiptNumber | ReceiptNumber | ReceiptNumber | text |  |
| DateofReceipt | DateofReceipt | DateofReceipt | date | 2025-04-29 |
| customer.name | customer.name | Name | text | 박찬연 |
| Capital | Capital | Capital(ContributionAmount) | text |  |
| value | value | (Korean) | amount |  |
| value2 | value2 | (English) | amount |  |
| SPCYesNo | SPCYesNo | (*)SPC[]Yes[]No | text | 0751-9517 |
| Headquarters | Headquarters | Headquarters | text |  |
| MainFactory | MainFactory | MainFactory(MainPlaceofBusiness) | text |  |
| Homepage | Homepage | Homepage(website) | text |  |
| customer.name2 | customer.name2 | Name | text | 박찬연 |
| customer.name3 | customer.name3 | Name | text | 박찬연 |
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| customer.nationality | customer.nationality | Nationality | text | 대한민국 |
| customer.nationality2 | customer.nationality2 | Nationality | text | 대한민국 |
| customer.nationality3 | customer.nationality3 | Nationality | text | 대한민국 |
| AcquisitionPricewon | AcquisitionPricewon | AcquisitionPrice:won(*USD) | number | 60 |
| InvestmentandParValueofStocks | InvestmentandParValueofStocks | InvestmentandParValueofStocks | text |  |
| DateofCompletion | DateofCompletion | DateofCompletion | date | 2025-09-11 |
| Investor | Investor | Investor | text |  |
| customer.name4 | customer.name4 | Name | text | 박찬연 |
| Foreign | Foreign | Foreign- | text |  |
| Invested | Invested | Invested | text |  |
| Changeof | Changeof | Changeof | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 손우승 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 확인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 남재윤 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 함원성 |
| check.agrees | check.agrees | agrees | checkbox | doesn’t agree to receive a |

### hf248 · 주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.248 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| ReceiptNumber | ReceiptNumber | ReceiptNumber | text |  |
| DateofReceipt | DateofReceipt | DateofReceipt | date | 2025년 11월 30일 |
| customer.name | customer.name | Name | text | 박찬연 |
| customer.address | customer.address | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.name2 | customer.name2 | Name | text | 박찬연 |
| customer.nationality | customer.nationality | Nationality | text | 대한민국 |
| AcquisitionPriceWon | AcquisitionPriceWon | AcquisitionPrice:Won(USD) | number | 50 |
| NotificationNo | NotificationNo | NotificationNo | text | 0676-7663 |
| DateofCompletion | DateofCompletion | DateofCompletion | date | 2025-09-21 |
| Changein | Changein | Changein | text |  |
| Information | Information | Information | text |  |
| changed | changed | changed | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 이혜아 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 허승주 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 오혜민 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 박철영 |
| ReceiptNumber2 | ReceiptNumber2 | ReceiptNumber | text |  |
| DateofReceipt2 | DateofReceipt2 | DateofReceipt | date | 2025.07.16 |
| customer.name3 | customer.name3 | Name | text | 박찬연 |
| customer.address2 | customer.address2 | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.name4 | customer.name4 | Name | text | 박찬연 |
| customer.nationality2 | customer.nationality2 | Nationality | text | 대한민국 |
| AcquisitionPriceWon2 | AcquisitionPriceWon2 | AcquisitionPrice:Won(USD) | number | 60 |
| NotificationNo2 | NotificationNo2 | NotificationNo | text | 940-348098-71692 |
| DateofCompletion2 | DateofCompletion2 | DateofCompletion | date | 2026.01.26 |
| Changein2 | Changein2 | Changein | text |  |
| Information2 | Information2 | Information | text |  |
| changed2 | changed2 | changed | text |  |

### hf249 · 주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(국문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.249 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 접수일 | 접수일 | 접수일 | text |  |
| 처리일 | 처리일 | 처리일 | text |  |
| date | date | 신고(허가)일 | date | 2026.01.31 |
| 하려는 | 하려는 | 하려는(하고있는사업) | text |  |
| 상호또는명칭 | 상호또는명칭 | 상호또는명칭 | text | (주)유니온무역 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 상호또는명칭2 | 상호또는명칭2 | 상호또는명칭 | text | 주식회사 한빛푸드 |
| customer.nationality | customer.nationality | 국적 | text | 대한민국 |
| 변경후내용 | 변경후내용 | 변경후내용 | text | 해당 없음 |
| 취득총액원 | 취득총액원 | 취득총액:원(USD상당) | number | 50 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신고인또는신청인(또는대리인) | text | 박찬연 |
| seal.signer | seal.customer | 신고인또는신청인(또는대리인) | seal | 현예지 |
| sign.signer | sign.customer | 신고인또는신청인(또는대리인) | signature | 박찬연 |
| 신고번호 | 신고번호 | 신고(허가)번호 | text | 0343-1435 |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| 접수번호 | 접수번호 | 접수번호 | text |  |
| 외국인 | 외국인 | 외국인 | text |  |
| 변경사항 | 변경사항 | 변경사항 | text |  |
| 이미신고된내용 | 이미신고된내용 | 이미신고(허가)된내용 | text | 해당 없음 |
| 변경내용 | 변경내용 | 변경내용 | text | 해당 없음 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김소호 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 확인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 구숙서 |
| 접수일2 | 접수일2 | 접수일 | text |  |
| 처리일2 | 처리일2 | 처리일 | text |  |
| date4 | date4 | 신고(허가)일 | date | 2026.01.31 |
| 하려는2 | 하려는2 | 하려는(하고있는사업) | text |  |
| 상호또는명칭3 | 상호또는명칭3 | 상호또는명칭 | text | 한빛로지스(주) |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 상호또는명칭4 | 상호또는명칭4 | 상호또는명칭 | text | (주)유니온무역 |
| customer.nationality2 | customer.nationality2 | 국적 | text | 대한민국 |
| 변경후내용2 | 변경후내용2 | 변경후내용 | text | 해당 없음 |
| 취득총액원2 | 취득총액원2 | 취득총액:원(USD상당) | number | 10 |
| date5 | date5 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고인또는신청인(또는대리인) | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신고인또는신청인(또는대리인) | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 신고인또는신청인(또는대리인) | signature | 이욱유 |
| 신고번호2 | 신고번호2 | 신고(허가)번호 | text | 045-960772-53289 |
| date6 | date6 | 작성일 | date | 2026년 1월 31일 |
| 접수번호2 | 접수번호2 | 접수번호 | text |  |
| 외국인2 | 외국인2 | 외국인 | text |  |
| 변경사항2 | 변경사항2 | 변경사항 | text |  |
| 이미신고된내용2 | 이미신고된내용2 | 이미신고(허가)된내용 | text | 해당 없음 |
| 변경내용2 | 변경내용2 | 변경내용 | text | 해당 없음 |

### hf250 · [필수] 개인(신용)정보 수집 이용 동의서(외투용)_영문

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.250 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| GeneralPersonalInformation | GeneralPersonalInformation | ■■GeneralPersonalInformation | text |  |
| check.identityverificationinformation | check.identityverificationinformation | identityverificationinformation? | checkbox | Agree |
| check.personalcreditinformation | check.personalcreditinformation | personalcreditinformation? | checkbox | Agree |
| customer.name | customer.name | 본인성명 | text | 박찬연 |
| written.month | written.month | 작성월 | number | 1 |
| written.day | written.day | 작성일 | number | 31 |
| written.year | written.year | 작성연도 | number | 2,026 |
| seal.principal | seal.principal | 본인서명 | seal | 이욱유 |
| sign.principal | sign.principal | 본인서명 | signature | 박찬연 |

### hf251 · [필수] 개인(신용)정보 수집 이용 동의서(외투용)_국문

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.251 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 일반개인정보 | 일반개인정보 | ■■일반개인정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 현예지 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 강석호 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 장민인 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 김순우 |
| 대리인은일반개인정보제공에한함 | 대리인은일반개인정보제공에한함 | 대리인은일반개인정보제공에한함 | text |  |

### hf252 · 외국환 신고(확인)필증

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.252 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 반출입구분 | 반출입구분 | 반출입구분(ExorImport) | text |  |
| 휴대_목록[].통화종류CodeofCurrency | 휴대_목록[].통화종류CodeofCurrency | 통화종류CodeofCurrency | text | USD |
| 송금 | 송금 | 송금(Remitted) | text |  |
| 기타 | 기타 | 기타(FromOthereligiblesources) | text | 해당 없음 |
| 휴대_목록[].형태Form | 휴대_목록[].형태Form | 형태Form | text |  |
| 목록[].형태Form | 목록[].형태Form | 형태Form | text |  |
| 휴대_목록[].통화별금액AmountineachCurrency | 휴대_목록[].통화별금액AmountineachCurrency | 통화별금액AmountineachCurrency | number | 41,540,000 |
| 목록[].통화별금액AmountineachCurrency | 목록[].통화별금액AmountineachCurrency | 통화별금액AmountineachCurrency | number | 16,140,000 |
| 휴대_목록[].합계Sum | 휴대_목록[].합계Sum | 합계(미화상당)Sum(US$equiv) | number | 9,280,000원 |
| 목록[].합계Sum | 목록[].합계Sum | 합계(미화상당)Sum(US$equiv) | number | 6,250,000 |
| 휴대_목록[].반출입용도Use | 휴대_목록[].반출입용도Use | 반출입용도Use | text | 해외 이주 |
| 목록[].반출입용도Use | 목록[].반출입용도Use | 반출입용도Use | text | 본인 요청 |
| 휴대_목록[].비고 | 휴대_목록[].비고 | 비고(Note)(수표번호등) | text | 해당 없음 |
| 목록[].비고 | 목록[].비고 | 비고(Note)(수표번호등) | text | 해당 없음 |
| 국적Nationality | 국적Nationality | 국적Nationality | text |  |
| 목록[].일자Date | 목록[].일자Date | 일자Date | date | 2025-10-12 |
| 목록[].금액Amount | 목록[].금액Amount | 금액Amount | number | 480,000 |
| 확인ResponsibleOfficial | 확인ResponsibleOfficial | 확인ResponsibleOfficial | text |  |
| 통화종류CodeofCurrency | 통화종류CodeofCurrency | 통화종류CodeofCurrency | text | GBP |
| 확인기관ConfirmationOffice | 확인기관ConfirmationOffice | 확인기관ConfirmationOffice | text |  |
| 확인자Signature | 확인자Signature | 확인자Signature | text |  |
| seal.signer | seal.customer | 신고인서명 | seal | 현예지 |
| sign.signer | sign.customer | 신고인서명 | signature | 박찬연 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.name2 | customer.name2 | Name | text | 박찬연 |
| Initial | Initial | Initial | text |  |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| PassportNo | PassportNo | PassportNo. | text | M52059472 |
| ExpectedTermofStayTo | ExpectedTermofStayTo | ExpectedTermofStayTo | text |  |

### hf253 · ( ) 변경신고(수리)서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.253 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 변경사유 | 변경사유 | 변경사유(요약) | text | 급여 수령 |
| 변경내용 | 변경내용 | 변경내용 | text | 해당 없음 |
| 변경후 | 변경후 | 변경후 | text | 해당 없음 |
| 신고번호 | 신고번호 | 신고(수리)번호 | text | 3193-9401 |
| 신고금액 | 신고금액 | 신고(수리)금액 | number | 450,000 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| signer.name | customer.name | 상호또는성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호또는성명 | seal | 이욱유 |
| sign.signer | sign.customer | 상호또는성명 | signature | 박찬연 |
| 주소또는소재지 | 주소또는소재지 | 주소또는소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| 기신고사항 | 기신고사항 | 기신고(수리)사항 | text |  |
| 나금액 | 나금액 | 나.금액 | number | 33,120,000 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 외국환은행의장 | text | 김도준 |
| seal.signer2 | seal.signer2 | 외국환은행의장 | seal | 김도준 |
| sign.signer2 | sign.signer2 | 외국환은행의장 | signature | 성민아 |
| 가신고번호 | 가신고번호 | 가.신고(수리)번호 | text | 9257-6273 |

### hf254 · 금전의 대차계약 신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.254 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 박찬연 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 현예지 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| check.차주 | check.차주 | 차주 | checkbox | 개인 |
| check.대주 | check.대주 | 대주 | checkbox | 기관투자가 |
| check.통화및금액 | check.통화및금액 | 통화및금액 | checkbox | 외화(1미화 1천만달러 이하 2미화 1천만달러 초과) |
| 차입대출일 | 차입대출일 | 차입/대출일 | date | 2024-12-31 |
| 적용금리 | 적용금리 | 적용금리 | number | 50 |
| 대차기간 | 대차기간 | 대차기간 | text |  |
| 사용용도 | 사용용도 | 사용용도 | text | 계좌 정리 |
| 상환방법 | 상환방법 | 상환방법 | text | 원리금균등분할상환 |
| check.거주자의보증또는담보유무 | check.거주자의보증또는담보유무 | 거주자의보증또는담보유무 | checkbox | 담보제공 |
| 신고번호 | 신고번호 | 신고번호 | text | 008-470320-73270 |
| 신고금액 | 신고금액 | 신고금액 | number | 360,000 |
| date | date | 신고일자 | date | 2026.01.31 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 기타참고사항 | 기타참고사항 | 기타참고사항 | text | 해당 없음 |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 신고기관 | 신고기관 | 신고기관 | text |  |

### hf255 · 자(손자)회사 사업계획서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.255 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 현지법인명 | 현지법인명 | 현지법인명 | text | 주식회사 우진산업 |
| company.address | corp.address | 소재지(주소) | text | 서울특별시 중구 다산로 361, 6층 |
| 총자산 | 총자산 | 총자산 | text |  |
| company.biz_item | corp.biz_item | 업종(제품) | text | 무역 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| 자본금 | 자본금 | 자본금 | text |  |
| 설립등기일 | 설립등기일 | 설립등기일 | date | 2029-01-12 |
| 자회사명 | 자회사명 | 자(손자)회사명 | text | 한빛테크(주) |
| company.address2 | company.address2 | 소재지(주소) | text | 서울특별시 중구 다산로 361, 6층 |
| 자본금2 | 자본금2 | 자본금 | text |  |
| check.투자형태 | check.투자형태 | 투자형태 | checkbox | 단독투자 |
| check.법인성격 | check.법인성격 | 법인성격 | checkbox | 특수목적회사(SPC) |
| company.ceo2 | company.ceo2 | 대표자 | text | 박찬연 |
| company.established | corp.established | 설립(예정)일 | date | 2018.11.01 |
| company.biz_item2 | company.biz_item2 | 업종(제품) | text | 무역 |
| check.설립형태 | check.설립형태 | 설립형태 | checkbox | 신설법인 설립 |
| 증권종류 | 증권종류 | 증권종류 | text |  |
| 주수 | 주수 | 주수 | text |  |
| 주당액면 | 주당액면 | 주당액면 | text |  |
| 취득가액이액면과상이할경우그산출근거 | 취득가액이액면과상이할경우그산출근거 | 취득가액이액면과상이할경우그산출근거 | number | 7,120,000 |
| 주당가액 | 주당가액 | 주당가액 | number | 4,050,000원 |
| check.자회사설립 | check.자회사설립 | 자회사설립 | checkbox | 손자회사 설립 |
| 투자형태 | 투자형태 | 투자형태 | text |  |
| 법인성격 | 법인성격 | 법인성격 | text |  |
| 현금 | 현금 | 현금 | text |  |
| 주식 | 주식 | 주식 | text |  |
| 기술투자 | 기술투자 | 기술투자 | text |  |
| 현물 | 현물 | 현물 | text |  |
| 이익잉여금 | 이익잉여금 | 이익잉여금 | text |  |
| 기타 | 기타 | 기타() | text | 해당 없음 |
| 한국측_목록[].출자자명 | 한국측_목록[].출자자명 | 출자자명 | text |  |
| 현지측 | 현지측 | 현지측(2) | text |  |
| 제3국 | 제3국 | 제3국(3) | text |  |
| 한국측_목록[].금액 | 한국측_목록[].금액 | 금액 | text | 4,430,000 |
| 소계 | 소계 | 소계(1) | text |  |
| 목록[].금액 | 목록[].금액 | 금액 | text | 49,620,000 |
| 합계 | 합계 | 합계(1+2+3) | number | 490,000 |
| 한국측_목록[].비율 | 한국측_목록[].비율 | 비율(%) | text | 100 |
| 목록[].비율 | 목록[].비율 | 비율(%) | text | 45 |
| 토지건물기계설비운영자금 | 토지건물기계설비운영자금 | 토지건물기계설비운영자금 | text |  |
| 차입금자본금 | 차입금자본금 | 차입금자본금 | text |  |

### hf256 · 외국환업무 등록 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.256 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 상호(본점) | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자(본점) | text | 박찬연 |
| 본점소재지주 | 본점소재지주 | 본점소재지주 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 외국환업무의내용 | 외국환업무의내용 | 외국환업무의내용 | text | 해당 없음 |
| 자기자본 | 자기자본 | 자기자본 | number | 0.54 |
| 영업점수 | 영업점수 | 영업점수 | number | 2 |
| 외국환업무취급점 | 외국환업무취급점 | 외국환업무취급점 | number | 12 |
| 위험관리전산시스템명 | 위험관리전산시스템명 | 위험관리전산시스템명 | text |  |
| company.established | corp.established | 설립연월일 | date | 2026년 1월 31일 |
| customer.nationality | customer.nationality | 국적(대표자) | text | 대한민국 |
| 납입자본 | 납입자본 | 납입자본 | number | 91.05 |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| 도입시기 | 도입시기 | 도입(개발)시기 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 인력현황 | 인력현황 | 인력현황 | text |  |

### hf258 · 환전업무 등록신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.258 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.등록구분 | check.등록구분 | 등록구분 | checkbox | 무인환전기기 |
| 기타 | 기타 | 기타 | text | 고객 요청: 지점 방문 예정 |
| check.동의함 | check.동의함 | 동의함 | checkbox | 동의함 |
| 환전업시작일 | 환전업시작일 | 환전업시작일 | date | 2025-01-23 |
| 근거법령 | 근거법령 | 근거법령 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 행정정보공동 | 행정정보공동 | 행정정보공동 | text |  |

### hf259 · 환전업무 등록내용 변경 신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.259 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 변경전 | 변경전 | 변경전 | text | 해당 없음 |
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 변경사유 | 변경사유 | 변경사유 | text | 월급 받는 통장으로 바꿈 |
| 변경후 | 변경후 | 변경후 | text | 해당 없음 |
| check.동의함 | check.동의함 | 동의함 | checkbox | 동의하지않음 |
| company.established | corp.established | 설립연월일 | date | 2026년 1월 31일 |
| 근거법령 | 근거법령 | 근거법령 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |

### hf260 · 외국환업무 등록내용 변경 신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.260 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 상호(본점) | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자(본점) | text | 박찬연 |
| 본점소재지주 | 본점소재지주 | 본점소재지주 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 위험관리시스템명 | 위험관리시스템명 | 위험관리시스템명 | text |  |
| 자기자본 | 자기자본 | 자기자본 | text |  |
| 명칭 | 명칭 | 명칭 | text | 세진화학 |
| company.address | corp.address | 본점소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| 외국환업무의내용 | 외국환업무의내용 | 외국환업무의내용 | text | 해당 없음 |
| company.established | corp.established | 설립연월일 | date | 2026년 1월 31일 |
| customer.nationality | customer.nationality | 국적(대표자) | text | 대한민국 |
| 납입자본 | 납입자본 | 납입자본 | number | 41.9 |
| 도입시기 | 도입시기 | 도입(개발)시기 | text |  |
| 목록[].변경후 | 목록[].변경후 | 변경후 | text | 해당 없음 |
| date | date | 작성일 | date | 2026년 1월 31일 |

### hf261 · 환전업무 폐지 신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.261 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 폐지사유 | 폐지사유 | 폐지사유 | text | 전세자금 |
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.established | corp.established | 설립연월일 | date | 2026년 1월 31일 |
| date | date | 작성일 | date | 2026년 1월 31일 |

### hf262 · 상호계산신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.262 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 상호대표자성명 | 상호대표자성명 | 상호,대표자성명 | text | 주식회사 누리무역 |
| 주소및전화번호 | 주소및전화번호 | 주소및전화번호 | phone | 010-5907-7253 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 상호및대표자 | 상호및대표자 | 상호및대표자(지정) | text | (주)유니온무역 |
| foreign.address | foreign.address | 주소 | text | 45 Le Loi St, District 1, Ho Chi Minh City |
| company.biz_item2 | company.biz_item2 | 업종 | text | 무역 |
| 자본금 | 자본금 | 자본금(영업기금) | text |  |
| 본지사여부 | 본지사여부 | 본지사여부 | text |  |
| 회계기간 | 회계기간 | 회계기간 | text |  |
| 변경내용 | 변경내용 | 변경내용 | text | 해당 없음 |
| 지사설치유효기간 | 지사설치유효기간 | 지사설치유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신고인 | text | 박찬연 |
| seal.signer | seal.customer | 신고인 | seal | 박찬연 |
| sign.signer | sign.customer | 신고인 | signature | 강순준 |

### hf263 · 지급등의 방법(변경)신고(보고)서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.263 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 변경 | 변경 | 변경 | text |  |
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자성명 | text | 박찬연 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.거래종류 | check.거래종류 | 거래종류 | checkbox | 자본거래 |
| check.결제방법 | check.결제방법 | 결제방법 | checkbox | 송금 |
| 계약금액 | 계약금액 | 계약금액 | number | 40,510,000 |
| check.결제방법2 | check.결제방법2 | 결제방법 | checkbox | 기타( |
| check.결제방법3 | check.결제방법3 | 결제방법 | checkbox | 외국환은행을 통한 방법 |
| check.구분 | check.구분 | 구분 | checkbox | 제3자 지급 |
| 결제시기 | 결제시기 | 결제시기 | text |  |
| 상호및대표자성명 | 상호및대표자성명 | 상호및대표자성명 | text | (주)유니온무역 |
| 주소전화번호 | 주소전화번호 | 주소,전화번호 | phone | 010-5907-7253 |
| 당초기간 | 당초기간 | 당초기간 | text |  |
| 당초시기 | 당초시기 | 당초시기 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| 신고금액 | 신고금액 | 신고금액 | number | 790,000 |
| 변경2 | 변경2 | 변경 | text |  |
| 변경3 | 변경3 | 변경 | text |  |
| 잔액 | 잔액 | 잔액 | number | 140,000 |
| 신고번호 | 신고번호 | 신고번호 | text | 166702-8463782 |
| 신고금액2 | 신고금액2 | 신고금액 | number | 110,540,000 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신고인 | text | 박찬연 |
| seal.signer | seal.customer | 신고인 | seal | 강순준 |
| sign.signer | sign.customer | 신고인 | signature | 박찬연 |
| seal.signer2 | seal.signer2 | 지점 | seal | 장수율 |
| sign.signer2 | sign.signer2 | 지점 | signature | 선다찬 |

### hf264 · 거주자간 해외직접투자 양수도 신고(보고)서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.264 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호또는성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호또는성명 | seal | 박찬연 |
| sign.signer | sign.customer | 상호또는성명 | signature | 강순준 |
| company.address | corp.address | 소재지(주소) | text | 서울특별시 중구 다산로 361, 6층 |
| check.투자자규모 | check.투자자규모 | 투자자규모 | checkbox | 대기업 |
| company.biz_no | corp.biz_no | 사업자(주민등록)번호 | biz_no | 264-82-36559 |
| signer2.name | signer2.name | 상호또는성명 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 상호또는성명 | seal | 이욱유 |
| sign.signer2 | sign.signer2 | 상호또는성명 | signature | 박찬연 |
| company.biz_no2 | company.biz_no2 | 사업자(주민등록)번호 | biz_no | 264-82-36559 |
| company.address2 | company.address2 | 소재지(주소) | text | 서울특별시 중구 다산로 361, 6층 |
| check.투자자규모2 | check.투자자규모2 | 투자자규모 | checkbox | 개인 |
| company.ceo | corp.ceo | 대표자명 | text | 박찬연 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| company.name | corp.name | 법인명 | text | (주)유니온무역 |
| company.address3 | company.address3 | 소재지(주소) | text | 서울특별시 중구 다산로 361, 6층 |
| date | date | 신고일자 | date | 2026년 01월 31일 |
| check.투자내역 | check.투자내역 | 투자내역 | checkbox | 투자비율 |
| 설립등기일 | 설립등기일 | 설립등기일 | date | 2028.03.01 |
| 신고번호 | 신고번호 | 신고번호 | rrn | 7782-9962 |
| check.투자지분양도내역 | check.투자지분양도내역 | 투자지분양도내역 | checkbox | 투자비율 |
| 양수도일자 | 양수도일자 | 양수도일자 | date | 2025.05.25 |
| 양수도가액 | 양수도가액 | 양수도가액 | number | 6,350,000 |
| 신고번호2 | 신고번호2 | 신고번호 | text | 6971-1767 |
| date2 | date2 | 신고일자 | date | 2026년 01월 31일 |
| check.양수도내역 | check.양수도내역 | 양수도내역( | checkbox | 전액양수도 |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| signer3.name | signer3.name | 신고기관 | text | 김희경 |
| seal.signer3 | seal.signer3 | 신고기관 | seal | 진민현 |
| sign.signer3 | sign.signer3 | 신고기관 | signature | 김희경 |
| 상호또는성명 | 상호또는성명 | 상호또는성명 | text | 미래정밀 |
| 상호또는성명2 | 상호또는성명2 | 상호또는성명 | text | 주식회사 우진상사 |
| 담당자및연락처 | 담당자및연락처 | 담당자및연락처 | phone | 010-5907-7253 |
| 지점 | 지점 | 지점 | text | 범어지점 |

### hf265 · 수탁기관 변경 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.265 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 상호또는명칭 | 상호또는명칭 | 상호또는명칭 | text | 한빛메디칼(주) |
| 상호또는명칭2 | 상호또는명칭2 | 상호또는명칭 | text | (주)가온산업 |
| 상호또는명칭3 | 상호또는명칭3 | 상호또는명칭 | text | 주식회사 우진로지스 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인(대표자) | text | 박찬연 |
| seal.signer | seal.customer | 신청인(대표자) | seal | 이욱유 |
| sign.signer | sign.customer | 신청인(대표자) | signature | 박찬연 |
| 신고번호 | 신고번호 | 신고번호 | text | 686-204785-38408 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |

### hf266 · 수출대금채권 매입의뢰서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.266 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| RM | RM | RM | text |  |
| 영업점장 | 영업점장 | 영업점장 | text |  |
| 고객번호 | 고객번호 | 고객번호 | text | 809-722115-17058 |
| 매입번호 | 매입번호 | 매입번호 | text | 910-849523-05251 |
| 상품명 | 상품명 | 상품명 | text | 하나 단기채 펀드 |
| 수출신고번호 | 수출신고번호 | 수출신고번호 | text | 1918-6815 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인 | text | 박찬연 |
| seal.signer | seal.customer | 본인 | seal | 박찬연 |
| sign.signer | sign.customer | 본인 | signature | 현예지 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| OATNET기타 | OATNET기타 | OAT()/NET()/기타() | text | 해당 없음 |

### hf267 · 외국환거래용 인감(서명)신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.267 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 한글 | 한글 | 한글(한문) | text |  |
| 영문 | 영문 | 영문 | text |  |
| 무역업고유번호 | 무역업고유번호 | 무역업고유번호 | text | 451-847848-24685 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| 한글2 | 한글2 | 한글 | text |  |
| 영문2 | 영문2 | 영문 | text |  |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| agent.name | agent.name | 대리인 | text | 박영준 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인 | text | 박찬연 |
| seal.signer | seal.customer | 본인 | seal | 박찬연 |
| sign.signer | sign.customer | 본인 | signature | 강순준 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 공성정 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김진서 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 공미태 |

### hf268 · 수입선적서류 도착통지 및 수입신용장 조건불일치에 관한 조회

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.268 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| LCNO | LCNO | L/CNO(REFNO) | text |  |
| 선적서류금액 | 선적서류금액 | 선적서류금액 | number | 38,660,000 |
| 통보내역 | 통보내역 | [은행사용란]통보내역 | text |  |
| 신용장번호 | 신용장번호 | 신용장번호 | text | 4182-4395 |
| 선적서류금액2 | 선적서류금액2 | 선적서류금액 | number | 640,000 |
| 불일치내용 | 불일치내용 | 불일치내용 | text | 해당 없음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |

### hf272 · REDEMPTION OF OUR LETTERS OF GUARANTEE

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.272 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| NumberofLG | NumberofLG | NumberofL/G | text | 614-444848-76283 |
| NumberofCredit | NumberofCredit | NumberofCredit | text | 490-521182-50628 |
| LGAmount | LGAmount | L/GAmount | number | 6,020,000 |
| NumberofBL | NumberofBL | NumberofB/L | text | 751258-0543936 |
| VesselName | VesselName | VesselName | text |  |
| Gentlemen | Gentlemen | Gentlemen | text |  |
| NumberofLG2 | NumberofLG2 | NumberofL/G | text | 7139-8932 |
| NumberofCredit2 | NumberofCredit2 | NumberofCredit | text | 0983-8860 |
| LGAmount2 | LGAmount2 | L/GAmount | number | 770,000 |
| NumberofBL2 | NumberofBL2 | NumberofB/L | text | 412-014101-40124 |
| VesselName2 | VesselName2 | VesselName | text |  |
| Gentlemen2 | Gentlemen2 | Gentlemen | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김다연 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 장기하 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 확인 |
| NumberofLG3 | NumberofLG3 | NumberofL/G | text | 433-910562-72702 |
| NumberofCredit3 | NumberofCredit3 | NumberofCredit | text | 075056-5134481 |
| LGAmount3 | LGAmount3 | L/GAmount | number | 89,680,000원 |
| NumberofBL3 | NumberofBL3 | NumberofB/L | text | 327505-5898863 |
| VesselName3 | VesselName3 | VesselName | text |  |
| Gentlemen3 | Gentlemen3 | Gentlemen | text |  |

### hf273 · [서식관리프로그램] 수입신용장 취소 및 수입보증금 환급 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.273 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 번호 | 번호 | 번호 | text | 346569-4725193 |
| 금액 | 금액 | 금액 | number | 277,880,000 |
| 유효기일 | 유효기일 | 유효기일 | date | 2028.04.17 |
| 취소신청금액 | 취소신청금액 | 취소신청금액 | number | 39,400,000원 |
| 환급신청금액 | 환급신청금액 | 환급신청금액 | number | 39,550,000 |
| account | account | 입금계좌 | account_no | 000-287736-52424 |
| 기타 | 기타 | 기타 | text | 해당 없음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 이욱유 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 검인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이은하 |

### hf274 · 「외국환서식관리프로그램」신용장 분실신고 및 재발행 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.274 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 분실사유 | 분실사유 | 분실사유 | text | 해외 이주 |
| 첨부서류분실신용장사본 | 첨부서류분실신용장사본 | 첨부서류:분실신용장사본 | text |  |
| 통지번호 | 통지번호 | 통지번호 | text | 380-439317-51275 |
| LC번호 | LC번호 | L/C번호 | text | 1939-6930 |
| 금액 | 금액 | 금액 | number | 68,900,000원 |
| 유효기일 | 유효기일 | 유효기일 | date | 2027년 7월 28일 |
| 발행은행 | 발행은행 | 발행은행 | text | 하나은행 |
| 수익자 | 수익자 | 수익자 | text |  |
| 개설의뢰인 | 개설의뢰인 | 개설의뢰인 | text |  |
| 발행일 | 발행일 | 발행일 | date | 2025.03.08 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 위나아 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이연재 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 정선빈 |

### hf275 · 수입신용장 재개설 및 중계에 관한 약정서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.275 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| RM | RM | RM | text |  |
| 영업점장 | 영업점장 | 영업점장 | text |  |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 은행명 | 은행명 | 은행명 | text | 기업은행 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 은행명2 | 은행명2 | 은행명 | text | 신한은행 |
| 나개설의뢰인 | 나개설의뢰인 | 나.개설의뢰인 | text |  |
| 다개설금액 | 다개설금액 | 다.개설금액 | number | 3,170,000 |
| 라신용장번호 | 라신용장번호 | 라.신용장번호 | text | 8730-7233 |
| 나포괄약정인경우 | 나포괄약정인경우 | 나.포괄약정인경우 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 갑 | text | 박찬연 |
| seal.signer | seal.customer | 갑 | seal | 박찬연 |
| sign.signer | sign.customer | 갑 | signature | 현예지 |
| signer2.name | signer2.name | 을 | text | 송수원 |
| seal.signer2 | seal.signer2 | 을 | seal | 천규율 |
| sign.signer2 | sign.signer2 | 을 | signature | 송수원 |

### hf276 · 확약서(단기수출보험(본지사금융))

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.276 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 소 | 소 | 소 | text |  |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| company.name | corp.name | 업체명 | text | (주)유니온무역 |
| signer.name | customer.name | 자 | text | 박찬연 |
| seal.signer | seal.customer | 자 | seal | 박찬연 |
| sign.signer | sign.customer | 자 | signature | 현예지 |

### hf277 · 포페이팅 의뢰서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.277 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 고객번호 | 고객번호 | 고객번호 | text | 3675-6027 |
| 거래번호 | 거래번호 | 거래번호 | text | 330559-7512254 |
| check.Forfaiting종류 | check.Forfaiting종류 | Forfaiting종류(해당항목선택) | checkbox | 인수후 비소구조건 매입 |
| ForfaitingAmount | ForfaitingAmount | ForfaitingAmount | number | 670,000원 |
| LCNO | LCNO | L/CNO. | text |  |
| LCIssuingBank | LCIssuingBank | L/CIssuingBank | text |  |
| Applicant | Applicant | Applicant | text | (주)유니온무역 |
| Tenor | Tenor | Tenor | text |  |
| ExpiryDate | ExpiryDate | ExpiryDate | date | 2025-12-14 |
| ShipmentDate | ShipmentDate | ShipmentDate | date | 2025.03.05 |
| account | account | 입금계좌번호 | account_no | 000-287736-52424 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인 | text | 박찬연 |
| seal.signer | seal.customer | 본인 | seal | 박찬연 |
| sign.signer | sign.customer | 본인 | signature | 최우빈 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김영예 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 신호서 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김환은 |

### hf278 · 판매대금추심의뢰서 매입(취소) 등록 요청/확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.278 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].번호 | 목록[].번호 | 번호 | text | 265795-9858541 |
| 목록[].종류 | 목록[].종류 | 종류 | text | 하나 정기예금 |
| 목록[].통화코드 | 목록[].통화코드 | 통화코드 | text | USD |
| 목록[].매입금액 | 목록[].매입금액 | 매입(추심)금액 | text | 7,420,000원 |
| 목록[].판매대금추심의뢰서번호 | 목록[].판매대금추심의뢰서번호 | 판매대금추심의뢰서번호 | text | 2,850,000원 |
| 목록[].매입점포코드 | 목록[].매입점포코드 | 매입(추심)점포코드 | number | 61273 |
| FAX | FAX | FAX()- | phone | 043-783-2775 |
| FAX2 | FAX2 | FAX()- | phone | 043-783-2775 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 부(지점) | text | 서용승 |
| seal.signer | seal.signer | 부(지점) | seal | 김소린 |
| sign.signer | sign.signer | 부(지점) | signature | 서용승 |
| signer2.name | signer2.name | 부(지점) | text | 여미빈 |
| seal.signer2 | seal.signer2 | 부(지점) | seal | 김용경 |
| sign.signer2 | sign.signer2 | 부(지점) | signature | 여미빈 |
| 추심의뢰 | 추심의뢰 | 추심의뢰 | text |  |
| 개설점포 | 개설점포 | 개설점포 | text | 범어지점 |
| 점포 | 점포 | 점포 | text |  |

### hf279 · 추심의뢰서(Renego)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.279 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].OurRefNo | 목록[].OurRefNo | OurRef.No. | text | 683-418491-97938 |
| 목록[].Amount | 목록[].Amount | Amount | number | 96,800,000원 |
| 목록[].사유 | 목록[].사유 | 사유(하자내용등) | text | 자녀 교육비 |
| 수신 | 수신 | 수신 | text |  |
| 참조 | 참조 | 참조 | text |  |
| 발신 | 발신 | 발신 | text |  |
| 목록[].Discrepancies | 목록[].Discrepancies | Discrepancies | text |  |
| To | To | To | text |  |
| Attn | Attn | Attn | text |  |
| From | From | From | text |  |
| date | date | Date | date | 2026년 01월 31일 |

### hf280 · 추심 수출환어음 종결처리(유예) 요청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.280 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 거래번호 | 거래번호 | 거래번호 | text | 417-495769-75906 |
| 추심금액 | 추심금액 | 추심금액 | number | 60,000 |
| 추심의뢰일 | 추심의뢰일 | 추심의뢰일 | date | 2025-12-02 |
| 신용장번호계약서번호 | 신용장번호계약서번호 | 신용장번호/계약서번호 | text | 021637-4632857 |
| 개설일자 | 개설일자 | 개설일자 | date | 2025.10.08 |
| 유효기일 | 유효기일 | 유효기일 | date | 2025-11-25 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer.name | corp.name | 상호(명판및직인) | text | (주)유니온무역 |
| seal.signer | seal.corp | 상호(명판및직인) | seal | 주식회사 새한소프트 |
| sign.signer | sign.customer | 상호(명판및직인) | signature | (주)유니온무역 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 여철빈 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김우민 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 윤예경 |
| 거래번호2 | 거래번호2 | 거래번호 | text | 871-814069-87046 |
| 추심금액2 | 추심금액2 | 추심금액 | number | 239,270,000 |
| 추심의뢰일2 | 추심의뢰일2 | 추심의뢰일 | date | 2025년 11월 7일 |
| 신용장번호계약서번호2 | 신용장번호계약서번호2 | 신용장번호/계약서번호 | text | 776142-4771901 |
| 개설일자2 | 개설일자2 | 개설일자 | date | 2025-06-20 |
| 유효기일2 | 유효기일2 | 유효기일 | date | 2025-02-08 |
| 취급점2 | 취급점2 | 취급점 | text | 범어지점 |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 상호(명판및직인) | text | (주)유니온무역 |
| seal.signer2 | seal.signer2 | 상호(명판및직인) | seal | 주식회사 한빛패션 |
| sign.signer2 | sign.signer2 | 상호(명판및직인) | signature | (주)유니온무역 |
| customer.phone2 | customer.phone2 | 전화번호 | phone | 010-5907-7253 |
| seal.staff.담당2 | seal.staff.담당2 | 담당 | seal | 검인 |
| sign.staff.담당2 | sign.staff.담당2 | 담당 | signature | 김우민 |
| seal.staff.책임자2 | seal.staff.책임자2 | 책임자 | seal | 김승린 |
| sign.staff.책임자2 | sign.staff.책임자2 | 책임자 | signature | 왕선성 |

### hf281 · 「외국환서식관리프로그램」조건변경부 신용장양도(SKY T/S) 조건변경.취소 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.281 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.전문사본요청합니다 | check.전문사본요청합니다 | 전문사본요청합니다. | checkbox | 전문사본 요청합니다. |
| FAX | FAX | FAX | phone | 043-783-2775 |
| 유효기일 | 유효기일 | 유효기일 | date | 2028.03.21 |
| 제시기일 | 제시기일 | 제시기일 | date | 2029년 5월 20일 |
| 선적기일 | 선적기일 | 선적기일 | date | 2028-06-13 |
| 부보비율 | 부보비율 | 부보비율 | number | 10 |
| 목록[].변경후 | 목록[].변경후 | 변경후 | text | 해당 없음 |
| check.신용장양도 | check.신용장양도 | 신용장양도(SKYT/S) | checkbox | 조건변경 신청서 |
| check.취소 | check.취소 | 취소 | checkbox | 취소 |
| 기발행SKYTS번호 | 기발행SKYTS번호 | 기발행SKYT/S번호 | text | 598-328826-12280 |
| 본건양도후신용장잔액 | 본건양도후신용장잔액 | 본건양도후신용장잔액 | number | 5,560,000 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 현예지 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 전소태 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 노도희 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 추호지 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 정유찬 |

### hf282 · 「외국환서식관리프로그램」조건변경부 신용장양도(SKY T/S) 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.282 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.전문사본요청합니다 | check.전문사본요청합니다 | 전문사본요청합니다. | checkbox | 전문사본 요청합니다. |
| FAX | FAX | FAX | phone | 043-783-2775 |
| 유효기일 | 유효기일 | 유효기일 | date | 2027-02-25 |
| 제시기일 | 제시기일 | 제시기일 | date | 2029년 1월 25일 |
| 선적기일 | 선적기일 | 선적기일 | date | 2030년 1월 30일 |
| 부보비율 | 부보비율 | 부보비율 | number | 10 |
| 목록[].조건변경부신용장내용 | 목록[].조건변경부신용장내용 | 조건변경부신용장내용 | text | 해당 없음 |
| 제2수익자상호 | 제2수익자상호 | 제2수익자상호 | text | 가온정밀(주) |
| 제2수익자주소 | 제2수익자주소 | 제2수익자주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 통지은행명및주소 | 통지은행명및주소 | 통지은행명및주소 | text | 기업은행 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 현예지 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 확인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 확인 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김선정 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 천정준 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 남궁재예 |

### hf283 · 인감증(외국환업무)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.283 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| seal.signer | seal.customer | 인감증번호 | seal | 이욱유 |
| sign.signer | sign.customer | 인감증번호 | signature | 강순준 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 한글 | 한글 | 한글(한문) | text |  |
| 영문 | 영문 | 영문 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |

### hf284 · 인감증 분실신고 및 재발급 신청서(외국환업무)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.284 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 각영업점앞통보 | 각영업점앞통보 | 각영업점앞통보 | text | 범어지점 |
| 재발급 | 재발급 | 재발급 | text |  |
| 분실사유 | 분실사유 | 분실사유 | text | 급여 수령 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 인 | text | 박찬연 |
| seal.signer | seal.customer | 인 | seal | 이민빈 |
| sign.signer | sign.customer | 인 | signature | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 확인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 문미예 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 여영예 |

### hf285 · 인감증 발급신청서(외국환업무)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.285 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| seal.signer | seal.customer | 인감증번호 | seal | 이민빈 |
| sign.signer | sign.customer | 인감증번호 | signature | 박찬연 |
| 발급일자 | 발급일자 | 발급일자 | date | 2025-07-09 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 인 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 인 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 인 | signature | 이욱유 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 신철우 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 박석영 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김형인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김민준 |

### hf286 · 신용장 확인 신청 및 확약서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.286 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| check.CREDITNO | check.CREDITNO | CREDITNO.(신용장번호) | checkbox | CREDIT NO. (신용장번호) |
| check.ADVICENO | check.ADVICENO | ADVICENO.(신용장통지번호) | checkbox | ADVICE NO.(신용장통지번호) |
| check.ISSUINGBANK | check.ISSUINGBANK | ISSUINGBANK(개설은행) | checkbox | ISSUING BANK(개설은행) |
| check.ISSUINGDATE | check.ISSUINGDATE | ISSUINGDATE(개설일) | checkbox | ISSUING DATE(개설일) |
| check.AMOUNT | check.AMOUNT | AMOUNT(금액) | checkbox | AMOUNT(금액) |
| signer.name | customer.name | (본인) | text | 박찬연 |
| seal.signer | seal.customer | (본인) | seal | 이욱유 |
| sign.signer | sign.customer | (본인) | signature | 박찬연 |
| check.CREDITNO2 | check.CREDITNO2 | CREDITNO.(신용장번호) | checkbox | CREDIT NO. (신용장번호) |
| check.ADVICENO2 | check.ADVICENO2 | ADVICENO.(신용장통지번호) | checkbox | ADVICE NO.(신용장통지번호) |
| check.ISSUINGBANK2 | check.ISSUINGBANK2 | ISSUINGBANK(개설은행) | checkbox | ISSUING BANK(개설은행) |
| check.ISSUINGDATE2 | check.ISSUINGDATE2 | ISSUINGDATE(개설일) | checkbox | ISSUING DATE(개설일) |
| check.AMOUNT2 | check.AMOUNT2 | AMOUNT(금액) | checkbox | AMOUNT(금액) |

### hf287 · 「외국환서식관리프로그램」신용장 양도 조건변경/취소 신청서 (Amendment / Cancellation)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.287 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.Amendment | check.Amendment | Amendment | checkbox | Amendment |
| check.Cancellation | check.Cancellation | Cancellation | checkbox | Cancellation |
| date | date | Date | date | 2026년 01월 31일 |
| LCNo | LCNo | L/CNo. | text | 024-747930-32594 |
| LCAmount | LCAmount | L/CAmount | number | 11,370,000원 |
| IssuingBank | IssuingBank | IssuingBank | text |  |
| TSNo | TSNo | T/SNo | text | 6498-4752 |
| TSAmount | TSAmount | T/SAmount | number | 41,040,000 |
| Gentlemen | Gentlemen | Gentlemen | text |  |
| check.amend | check.amend | amend | checkbox | totally |
| check.cancel | check.cancel | cancel | checkbox | cancel |
| check.increasedby | check.increasedby | increasedby | checkbox | increased by |
| Amount | Amount | Amount | number | 62,280,000원 |
| check.decreasedby | check.decreasedby | decreasedby | checkbox | decreased by |
| Latestshippingdate | Latestshippingdate | Latestshippingdate | date |  |
| Expirydate | Expirydate | Expirydate | date |  |

### hf288 · 「외국환서식관리프로그램」신용장 양도 신청서(Application for Total/Partial transfer)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.288 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.Total | check.Total | Total | checkbox | Total |
| check.Partial | check.Partial | Partial | checkbox | Partial |
| date | date | Date | date | 2026.01.31 |
| LCNo | LCNo | L/CNo. | text | 4185-2150 |
| Dated | Dated | Dated | date | 2025.11.08 |
| IssuingBank | IssuingBank | IssuingBank | text |  |
| Amount | Amount | Amount | number | 730,000 |
| Beneficiary | Beneficiary | Beneficiary | text |  |
| Accountee | Accountee | Accountee | text |  |
| Gentlemen | Gentlemen | Gentlemen | text |  |
| Amounttobetransferred | Amounttobetransferred | Amounttobetransferred | number | 8,780,000 |
| Latestshippingdate | Latestshippingdate | Latestshippingdate | date |  |
| Expirydate | Expirydate | Expirydate | date |  |
| check.thefirstbene | check.thefirstbene | thefirstbeneficiary. | checkbox | the first beneficiary. |
| check.thesecondben | check.thesecondben | thesecondbeneficiary. | checkbox | the second beneficiary. |

### hf289 · 수출환어음등의 재매입을 위한 약정서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.289 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| RM | RM | RM | text |  |
| 영업점장 | 영업점장 | 영업점장 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인 | text | 박찬연 |
| seal.signer | seal.customer | 본인 | seal | 현예지 |
| sign.signer | sign.customer | 본인 | signature | 박찬연 |

### hf290 · 수출환어음 추심 후 매입전환 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.290 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| RM | RM | RM | text |  |
| 영업점장 | 영업점장 | 영업점장 | text |  |
| 거래번호 | 거래번호 | 거래번호(추심번호) | text | 131295-0106660 |
| 추심의뢰일자 | 추심의뢰일자 | 추심의뢰일자 | date | 2025.10.22 |
| 추심금액 | 추심금액 | 추심금액 | number | 279,150,000 |
| 예정만기일 | 예정만기일 | 예정(확정)만기일 | date | 2028.03.29 |
| 신용장번호 | 신용장번호 | 신용장번호 | text | 711351-2171261 |
| 신용장개설은행 | 신용장개설은행 | 신용장개설은행 | text | 신한은행 |
| 신용장개설의뢰인 | 신용장개설의뢰인 | 신용장개설의뢰인 | text |  |
| signer.name | customer.name | 본인 | text | 박찬연 |
| seal.signer | seal.customer | 본인 | seal | 현예지 |
| sign.signer | sign.customer | 본인 | signature | 강순준 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 거래형태 | 거래형태 | 거래형태 | text |  |

### hf291 · 「외국환서식관리프로그램」수출대금채권 양도에 따른 대금지급지시서 및 동의통지서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.291 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | Name | text | 박찬연 |
| Title | Title | Title | text |  |
| customer.name2 | customer.name2 | Name | text | 박찬연 |
| Title2 | Title2 | Title | text |  |
| date | date | Date | date | 2026.01.31 |
| signer.name | signer.name | [수출상] | text | 박찬연 |
| seal.signer | seal.customer | [수출상] | seal | 최우빈 |
| sign.signer | sign.customer | [수출상] | signature | 박찬연 |
| customer.name3 | customer.name3 | 이름 | text | 박찬연 |
| employer.position | employer.position | 직위 | text | 대리 |
| signer2.name | signer2.name | [수입상] | text | 손석린 |
| seal.signer2 | seal.signer2 | [수입상] | seal | 손석린 |
| sign.signer2 | sign.signer2 | [수입상] | signature | 김순찬 |
| customer.name4 | customer.name4 | 이름 | text | 박찬연 |
| employer.position2 | employer.position2 | 직위 | text | 대리 |
| date2 | date2 | 일자 | date | 2026.01.31 |

### hf292 · 수입통관도우미서비스 이용신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.292 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 업체명 | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 신용장번호 | 신용장번호 | 신용장(또는당발송금)번호 | text | 232766-8633566 |
| 선적일 | 선적일 | 선적(예정)일 | date | 2025-11-23 |
| 품목 | 품목 | 품목 | text | LED 모듈 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 이민빈 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| seal.signer2 | seal.signer2 | 지점 | seal | 김수서 |
| sign.signer2 | sign.signer2 | 지점 | signature | 백욱호 |
| TEL | TEL | TEL | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 염훈혜 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 위서우 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 최예은 |

### hf293 · 「외국환서식관리프로그램」선적서류 수령증 및 수입화물 대도(T/R)신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.293 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].신용장번호 | 목록[].신용장번호 | 신용장번호 | text | 640-175873-04816 |
| 목록[].통화 | 목록[].통화 | 통화 | text | USD |
| 목록[].금액 | 목록[].금액 | 금액 | text | 9,140,000 |
| 목록[].선하증권 | 목록[].선하증권 | 선하증권 | text |  |
| 목록[].항공화물운송장 | 목록[].항공화물운송장 | 항공화물운송장 | text |  |
| 목록[].상업송장보험서류 | 목록[].상업송장보험서류 | 상업송장보험서류 | text |  |
| 목록[].선하증권번호항공화물운송장번호 | 목록[].선하증권번호항공화물운송장번호 | 선하증권번호/항공화물운송장번호 | text | 5277-1762 |
| 목록[].대도금액 | 목록[].대도금액 | 대도금액 | text | 560,000 |
| check.선적서류수령증 | check.선적서류수령증 | 선적서류수령증 | checkbox | 선적서류 수령증 |
| check.수입화물대도신청서 | check.수입화물대도신청서 | 수입화물대도(T/R)신청서 | checkbox | 수입화물 대도(T/R) 신청서 |
| check.본인은아래신용장에의한선 | check.본인은아래신용장에의한선 | 본인은아래신용장에의한선적서류를정히수령하였습니다. | checkbox | 본인은 아래 신용장에 의한 선적서류를 정히 수령하였습니다. |
| check.본인은아래신용장등에의하 | check.본인은아래신용장등에의하 | 본인은아래신용장등에의하여도착된수입화물을대도(T/R)신청함에 | checkbox | 본인은 아래 신용장 등에 의하여 도착된 수입화물을 대도(T/R) 신청함에 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 김소윤 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 구분 | 구분 | 구분 | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 곽순태 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김소성 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 최민지 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 함도빈 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 허욱아 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 조기인 |

### hf294 · 「외국환서식관리프로그램」선적서류 (일부)매입(추심) 의뢰서(2D용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.294 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| RM | RM | RM | text |  |
| 영업점장 | 영업점장 | 영업점장 | text |  |
| 고객번호 | 고객번호 | 고객번호 | text | 401709-7529186 |
| 매입번호 | 매입번호 | 매입번호 | text | 5574-0840 |
| 일부매입금액 | 일부매입금액 | 일부매입금액 | number | 4,380,000 |
| 일부추심금액 | 일부추심금액 | 일부추심금액 | number | 48,860,000 |
| AMOUNT | AMOUNT | AMOUNT | number | 2,980,000 |
| COMMODITY | COMMODITY | COMMODITY | text |  |
| ACCOUNTEE | ACCOUNTEE | ACCOUNTEE(drawee) | text |  |
| PRICETERM | PRICETERM | PRICETERM | text |  |
| 수출상대국 | 수출상대국 | 수출상대국 | text |  |
| 수출신고번호 | 수출신고번호 | 수출신고번호 | text | 1630-7034 |
| TENORMATURITY | TENORMATURITY | TENOR&MATURITY | text |  |
| HSCODE | HSCODE | H.S.CODE | text |  |
| BENEFICIARY | BENEFICIARY | BENEFICIARY(drawer) | text |  |
| FOB금액 | FOB금액 | FOB금액 | number | 6,880,000 |
| TOISSUINGBANK_목록[].BENE | TOISSUINGBANK_목록[].BENE | BENE | text |  |
| TOREIMBANK | TOREIMBANK | TOREIM.BANK | text |  |
| TOISSUINGBANK_목록[].BANK | TOISSUINGBANK_목록[].BANK | BANK | text |  |
| BANK | BANK | BANK | text |  |
| TOISSUINGBANK_목록[].COMM | TOISSUINGBANK_목록[].COMM | COMM | text |  |
| TOISSUINGBANK_목록[].CUST | TOISSUINGBANK_목록[].CUST | CUST | text |  |
| TOISSUINGBANK_목록[].BL | TOISSUINGBANK_목록[].BL | B/L | text |  |
| TOISSUINGBANK_목록[].AWB | TOISSUINGBANK_목록[].AWB | AWB | text |  |
| TOISSUINGBANK_목록[].PL | TOISSUINGBANK_목록[].PL | P/L | text |  |
| TOISSUINGBANK_목록[].IP | TOISSUINGBANK_목록[].IP | I/P | text |  |
| TOISSUINGBANK_목록[].CO | TOISSUINGBANK_목록[].CO | C/O | text |  |
| TOISSUINGBANK_목록[].IC | TOISSUINGBANK_목록[].IC | I/C | text |  |
| TOISSUINGBANK_목록[].BENECERT | TOISSUINGBANK_목록[].BENECERT | BENECERT | text |  |
| BENECERT | BENECERT | BENECERT | text |  |
| 외화계정대체 | 외화계정대체 | 외화계정대체 | amount | EUR 97,800 |
| 원화계정대체 | 원화계정대체 | 원화계정대체 | text |  |
| A | A | A | text |  |
| B | B | B | text |  |
| 수입보증금 | 수입보증금 | 수입보증금 | number | 4,960,000 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인 | text | 박찬연 |
| seal.signer | seal.customer | 본인 | seal | 박찬연 |
| sign.signer | sign.customer | 본인 | signature | 강순준 |
| MAILTO | MAILTO | MAILTO | text |  |
| NO | NO | NO | text | 048802-6932569 |
| FROM | FROM | FROM | text |  |

### hf295 · 보증서(수출환어음등 재매입용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.295 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 발행은행 | 발행은행 | 발행은행 | text | 농협은행 |
| 신용장번호 | 신용장번호 | 신용장(계약서)번호 | rrn | 729191-2297037 |
| 신용장금액 | 신용장금액 | 신용장(계약서)금액 | number | 6,540,000 |
| 발행일자 | 발행일자 | 발행일자 | date | 2026.01.23 |
| 매입금액 | 매입금액 | 매입금액 | number | 134,370,000 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 강순준 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 왕훈정 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 윤영인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 남궁유아 |

### hf296 · 매입제한 해제 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.296 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용장통지번호 | 신용장통지번호 | 신용장통지번호 | text | 273193-9195293 |
| 신용장번호 | 신용장번호 | 신용장번호 | text | 386-342416-78650 |
| 신용장금액 | 신용장금액 | 신용장금액 | number | 1,620,000 |
| 발행은행 | 발행은행 | 발행은행 | text | 우리은행 |
| 발행일자 | 발행일자 | 발행일자 | date | 2025년 4월 28일 |
| 해제신청금액 | 해제신청금액 | 해제신청금액 | number | 940,000 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.name | customer.name | 신청인 | text | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 오준재 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 확인 |

### hf297 · 단기수출보험(수출채권유동화) 청약 확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.297 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.청약종류 | check.청약종류 | 청약종류 | checkbox | 신규 |
| 한도신청액 | 한도신청액 | 한도신청액 | number | 6,740,000 |
| check.일반구분1 | check.일반구분1 | 일반구분1 | checkbox | 일반수출 |
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| company.name2 | company.name2 | 상호 | text | (주)유니온무역 |
| 주소_목록[].대표자 | 주소_목록[].대표자 | 대표자 | text |  |
| company.ceo2 | company.ceo2 | 대표자 | text | 박찬연 |
| 소재국 | 소재국 | 소재국 | text |  |
| check.수출자와수입자관계의본지사해당하는지여부 | check.수출자와수입자관계의본지사해당하는지여부 | 수출자와수입자관계의본지사해당하는지여부 | checkbox | 여 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 수출자명 | 수출자명 | 수출자명 | text |  |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer.name | signer.name | 대표 | text | 박찬연 |
| seal.signer | seal.corp | 대표 | seal | 현예지 |
| sign.signer | sign.customer | 대표 | signature | 박찬연 |
| 담당자성명 | 담당자성명 | 담당자성명 | text | 여다희 |
| check.종류 | check.종류 | 종류 | checkbox | CONFIRMED L/C |
| company.name3 | company.name3 | 상호 | text | (주)유니온무역 |
| customer.address3 | customer.address3 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.name4 | company.name4 | 상호 | text | (주)유니온무역 |
| company.ceo3 | company.ceo3 | 대표자 | text | 박찬연 |
| 소재국2 | 소재국2 | 소재국 | text |  |
| 소재국3 | 소재국3 | 소재국 | text |  |
| 결제조건 | 결제조건 | 결제조건 | text |  |
| check.이면계약또는대응구매계약존재여부 | check.이면계약또는대응구매계약존재여부 | 이면계약또는대응구매계약존재여부 | checkbox | 있음 |
| 수출상품명 | 수출상품명 | 수출상품명 | text | 하나 적금 |
| 건수 | 건수 | 건수 | number | 6 |
| CLAIM사유및결과 | CLAIM사유및결과 | CLAIM사유및결과 | text | 투자 목적 |
| 신용장방식 | 신용장방식 | 신용장방식 | text |  |
| 무신용장방식 | 무신용장방식 | 무신용장방식 | text |  |
| 총거래실적 | 총거래실적 | 총거래실적 | text |  |
| 최근1년간거래실적_목록[].결제금액 | 최근1년간거래실적_목록[].결제금액 | 결제금액 | number | 46,780,000 |
| 금액 | 금액 | 금액 | number | 43,070,000원 |
| 최근1년간거래실적_목록[].만기경과미결제액 | 최근1년간거래실적_목록[].만기경과미결제액 | 만기경과미결제액 | date | 2029년 3월 4일 |
| 존재여부 | 존재여부 | 존재여부 | text |  |
| company.name5 | company.name5 | 상호 | text | (주)유니온무역 |
| customer.address4 | customer.address4 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 계약서상수입자와의관계 | 계약서상수입자와의관계 | 계약서상수입자와의관계 | text |  |
| 계약서상대금지급책임인 | 계약서상대금지급책임인 | 계약서상대금지급책임인 | number | 980,000 |
| 대행수입사유 | 대행수입사유 | 대행수입사유 | text | 급여 수령 |
| check.대행수입여부 | check.대행수입여부 | 대행수입여부 | checkbox | 부 |
| company.ceo4 | company.ceo4 | 대표자 | text | 박찬연 |
| 소재국4 | 소재국4 | 소재국 | text |  |
| check.이자보상특약가입여부 | check.이자보상특약가입여부 | 이자보상특약가입여부 | checkbox | 미가입 |
| 이자보상특약가입여부 | 이자보상특약가입여부 | 이자보상특약가입여부 | number | 57,010,000 |

### hf300 · LG 보증금 환급 신청 및 확약서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.300 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| RM | RM | RM | text |  |
| 영업점장 | 영업점장 | 영업점장 | text |  |
| 신용장번호 | 신용장번호 | (무)신용장번호 | text | 115-842353-26102 |
| 신용장유효기일 | 신용장유효기일 | 신용장유효기일 | date | 2026.05.07 |
| 수출상 | 수출상 | 수출상(Beneficiary) | text |  |
| LG금액 | LG금액 | L/G금액 | number | 24,230,000 |
| LG발행일자 | LG발행일자 | L/G발행일자 | date | 2026.01.14 |
| BL번호및선적일자 | BL번호및선적일자 | B/L번호및선적일자 | date | 2025.06.20 |
| LG보증금금액 | LG보증금금액 | L/G보증금금액 | number | 71,210,000 |
| account | account | 입금계좌번호 | account_no | 000-287736-52424 |
| signer.name | customer.name | 본인 | text | 박찬연 |
| seal.signer | seal.customer | 본인 | seal | 위나아 |
| sign.signer | sign.customer | 본인 | signature | 박찬연 |
| LG번호 | LG번호 | L/G번호 | text | 352-529225-19308 |

### hf301 · Cable Nego 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.301 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| RM | RM | RM | text |  |
| 영업점장 | 영업점장 | 영업점장 | text |  |
| 신용장번호 | 신용장번호 | 신용장번호 | text | 650300-4983930 |
| 개설은행 | 개설은행 | 개설은행(SWIFTCODE) | text | 농협은행 |
| 신청통화및금액 | 신청통화및금액 | 신청통화및금액 | number | 330,000 |
| 신용장유효기일 | 신용장유효기일 | 신용장유효기일 | date | 2027.04.09 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인명 | text | 박찬연 |
| seal.signer | seal.customer | 신청인명 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인명 | signature | 강순준 |
| 담당자명 | 담당자명 | 담당자명 | text | 박찬연 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| FAX번호 | FAX번호 | FAX번호 | phone | 043-783-2775 |

### hf302 · 「외국환서식관리프로그램」BILL OF EXCHANGE (환어음 고객용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.302 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| TO | TO | TO | text |  |
| TO2 | TO2 | TO | text |  |
| FOR | FOR | FOR | number | 58,220,000 |
| AT | AT | AT | date | 2024.12.29 |
| DATED | DATED | DATED | date | 2024년 12월 29일 |
| FOR2 | FOR2 | FOR | number | 5,130,000원 |
| AT2 | AT2 | AT | date | 2025년 5월 7일 |
| DATED2 | DATED2 | DATED | date | 2025-09-06 |

### hf303 · 수입실적 확인 및 증명 발급신청서(별지 제11호 서식)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.303 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 증명발급번호 | 증명발급번호 | 증명발급번호 | text | 287-959596-88656 |
| 발급용도 | 발급용도 | 발급용도 | text | 본인 요청 |
| customer.name | customer.name | 신청인(상호,주소성명) | text | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.signer | seal.signer | 지점장 | seal | 김동서 |
| sign.signer | sign.signer | 지점장 | signature | 고상진 |
| 비고 | 비고 | 비고 | text | 해당 없음 |

### hf304 · 수출실적 확인 및 증명 발급신청서(별지 제10호 서식)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.304 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 증명발급번호 | 증명발급번호 | 증명발급번호 | text | 837-907726-25956 |
| 발급용도 | 발급용도 | 발급용도 | text | 전세자금 |
| customer.name | customer.name | 신청인(상호,주소성명) | text | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.signer | seal.signer | 지점장 | seal | 심민아 |
| sign.signer | sign.signer | 지점장 | signature | 송서현 |
| 비고 | 비고 | 비고 | text | 해당 없음 |

### hf305 · ( )예금/신탁 거래신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.305 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 강순준 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 현예지 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| 예치금액 | 예치금액 | 예치(처분)금액 | number | 30,940,000 |
| 예치후잔액 | 예치후잔액 | 예치(처분)후잔액 | number | 6,880,000 |
| 예치사유 | 예치사유 | 예치(처분)사유 | text | 해외 이주 |
| 송금은행 | 송금은행 | 송금은행 | text | 카카오뱅크 |
| 신고번호 | 신고번호 | 신고번호 | text | 2964-3681 |
| 신고금액 | 신고금액 | 신고금액 | number | 5,860,000 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고기관:한국은행총재 | text | 도훈진 |
| seal.signer2 | seal.signer2 | 신고기관:한국은행총재 | seal | 이다혜 |
| sign.signer2 | sign.signer2 | 신고기관:한국은행총재 | signature | 도훈진 |

### hf306 · 증권대차계약 신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.306 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 박찬연 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 이욱유 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| 차입자 | 차입자 | 차입자 | text |  |
| 대여자 | 대여자 | 대여자 | text |  |
| 대차대상증권종류 | 대차대상증권종류 | 대차대상증권종류 | text |  |
| 차입금액 | 차입금액 | 차입(한도)금액 | number | 770,000 |
| 차입수량 | 차입수량 | 차입수량 | number | 2 |
| check.차입목적 | check.차입목적 | 차입목적 | checkbox | 위험회피거래 |
| 차입기간 | 차입기간 | 차입기간 | text |  |
| 신고번호 | 신고번호 | 신고번호 | text | 221-202046-02486 |
| 신고금액 | 신고금액 | 신고금액 | number | 20,180,000 |
| date | date | 신고일자 | date | 2026년 01월 31일 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 기타참고사항 | 기타참고사항 | 기타참고사항 | text | 해당 없음 |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 신고기관 | 신고기관 | 신고기관 | text |  |

### hf307 · 지급수단등의 수출입(변경)신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.307 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 종류 | 종류 | 종류 | text | 하나 단기채 펀드 |
| 수량 | 수량 | 수량 | number | 3 |
| 수출입금액 | 수출입금액 | 수출입금액 | number | 870,000 |
| 대가결제방법 | 대가결제방법 | 대가결제방법 | text |  |
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| company.address | corp.address | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| 기타 | 기타 | 기타(또는변경내용) | text | 해당 없음 |
| 신고번호 | 신고번호 | 신고번호 | text | 785739-8542438 |
| 신고금액 | 신고금액 | 신고금액 | number | 216,900,000 |
| date | date | 신고일자 | date | 2026년 01월 31일 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| company.name2 | company.name2 | 상호 | text | (주)유니온무역 |
| company.ceo2 | company.ceo2 | 대표자 | text | 박찬연 |

### hf308 · 대북투자사업계획서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.308 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 상호또는성명 | 상호또는성명 | 상호또는성명 | text | (주)제일푸드 |
| company.address | corp.address | 소재지(주소) | text | 서울특별시 중구 다산로 361, 6층 |
| check.투자자규모 | check.투자자규모 | 투자자규모 | checkbox | 개인사업자 |
| 총자산 | 총자산 | 총자산 | number | 0.81 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| 설립년월일 | 설립년월일 | 설립년월일 | date | 2025.08.31 |
| 자기자본 | 자기자본 | 자기자본(자본금) | text |  |
| 담당자및연락처 | 담당자및연락처 | 담당자및연락처 | phone | 010-5907-7253 |
| company.name | corp.name | 법인명 | text | (주)유니온무역 |
| check.법인형태 | check.법인형태 | 법인형태 | checkbox | 법인 |
| 총자본금 | 총자본금 | 총자본금 | text |  |
| check.투자형태주 | check.투자형태주 | 투자형태주 | checkbox | 합작투자(지분율 ; |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| company.established | corp.established | 설립(예정)일 | date | 2018.11.01 |
| 현금 | 현금 | 현금 | text |  |
| 주식 | 주식 | 주식 | text |  |
| 기술투자 | 기술투자 | 기술투자 | text |  |
| 자기자금 | 자기자금 | 자기자금 | text |  |
| 현물 | 현물 | 현물 | text |  |
| 이익잉여금 | 이익잉여금 | 이익잉여금 | text |  |
| 기타 | 기타 | 기타() | text | 해당 없음 |
| 차입금 | 차입금 | 차입금 | text |  |
| 한국측_목록[].출자자명 | 한국측_목록[].출자자명 | 출자자명 | text |  |
| 현지측 | 현지측 | 현지측(2) | text |  |
| 제3국 | 제3국 | 제3국(3) | text |  |
| 한국측_목록[].금액 | 한국측_목록[].금액 | 금액 | text | 5,650,000 |
| 소계 | 소계 | 소계(1) | text |  |
| 목록[].금액 | 목록[].금액 | 금액 | text | 28,880,000 |
| 합계 | 합계 | 합계(1+2+3) | number | 6,650,000 |
| 한국측_목록[].비율 | 한국측_목록[].비율 | 비율(%) | text | 100 |
| 목록[].비율 | 목록[].비율 | 비율(%) | text | 80 |
| 법인형태 | 법인형태 | 법인형태 | text |  |
| 대부액 | 대부액 | 대부액 | text |  |
| 이율 | 이율 | 이율 | number | 20 |
| 자기자금2 | 자기자금2 | 자기자금 | text |  |
| 자금용도 | 자금용도 | 자금용도 | text | 사업자금 |
| 기간 | 기간 | 기간 | number | 1 |
| 차입금2 | 차입금2 | 차입금 | text |  |
| 토지건물기계설비운영자금 | 토지건물기계설비운영자금 | 토지건물기계설비운영자금... | text |  |
| 차입금자기자본 | 차입금자기자본 | 차입금자기자본 | text |  |

### hf309 · 파생상품거래 신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.309 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 박찬연 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 위나아 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| 상호및대표자성명 | 상호및대표자성명 | 상호및대표자성명 | text | (주)유니온무역 |
| company.biz_item2 | company.biz_item2 | 업종(직업) | text | 무역 |
| check.거래기초자산 | check.거래기초자산 | 거래기초자산 | checkbox | 기타( |
| check.거래종류 | check.거래종류 | 거래종류 | checkbox | 선도거래 |
| 계약금액 | 계약금액 | 계약(명목)금액 | number | 50,000원 |
| 만기 | 만기 | 만기 | date | 2025.02.04 |
| 세부내용 | 세부내용 | 세부내용 | text | 해당 없음 |
| check.거래특이사항 | check.거래특이사항 | 거래특이사항 | checkbox | 자금유출입·거주자와 비거주자간 금전대차 거래 관련 신고등의 절차를 회피 |
| 신고번호 | 신고번호 | 신고번호 | text | 839-264505-12135 |
| 신고금액 | 신고금액 | 신고금액 | number | 77,370,000 |
| date | date | 신고일자 | date | 2026년 01월 31일 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 기타참고사항 | 기타참고사항 | 기타참고사항 | text | 해당 없음 |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 신고기관 | 신고기관 | 신고기관 | text |  |

### hf310 · 대북투자사업 청산 및 대부채권 회수보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.310 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 상호또는성명 | 상호또는성명 | 상호또는성명 | text | 주식회사 가온물산 |
| company.biz_no | corp.biz_no | 사업자(주민)등록번호 | biz_no | 264-82-36559 |
| 현지법인명 | 현지법인명 | 현지법인명 | text | (주)유니온무역 |
| customer.address | customer.address | 주소(소재지) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.법인형태 | check.법인형태 | 법인형태 | checkbox | 기타 |
| check.투자형태주 | check.투자형태주 | 투자형태주 | checkbox | 공동투자 |
| 납입자본금 | 납입자본금 | 납입자본금 | text |  |
| 대부금액 | 대부금액 | 대부금액 | number | 6,320,000 |
| 기회수금액 | 기회수금액 | 기회수금액 | number | 26,590,000원 |
| 금회회수금액 | 금회회수금액 | 금회회수금액 | number | 35,490,000 |
| 잔액 | 잔액 | 잔액 | number | 6,600,000 |
| date | date | 일자 | date | 2026년 01월 31일 |
| 목록[].원금 | 목록[].원금 | 원금 | number | 135,740,000 |
| 회수금액_목록[].원금 | 회수금액_목록[].원금 | 원금 | number | 91,350,000 |
| check.청산 | check.청산 | 청산 | checkbox | 대부채권 회수 |
| 법인형태 | 법인형태 | 법인형태 | text |  |
| 유동자산투자및기타자산고정자산이연자산 | 유동자산투자및기타자산고정자산이연자산 | 유동자산투자및기타자산고정자산이연자산 | text |  |
| 계 | 계 | 계 | text |  |
| 유동부채고정부채자본금잉여금 | 유동부채고정부채자본금잉여금 | 유동부채고정부채자본금잉여금 | text |  |
| 계2 | 계2 | 계 | text |  |
| 목록[].구분회수일자 | 목록[].구분회수일자 | 구분회수일자 | date | 2025-05-12 |
| 목록[].회수재산의종류 | 목록[].회수재산의종류 | 회수재산의종류 | text |  |
| 계3 | 계3 | 계 | text |  |
| 목록[].금액 | 목록[].금액 | 금액 | text | 20,010,000 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| 청산종료일 | 청산종료일 | 청산종료일 | date | 2028.10.08 |
| 다청산손익 | 다청산손익 | 다.청산손익(해산일로부터청산종료일까지의손익) | text |  |
| 바회수가불가능한재산이있을경우그내역및사유 | 바회수가불가능한재산이있을경우그내역및사유 | 바.회수가불가능한재산이있을경우그내역및사유 | text | 계좌 정리 |

### hf311 · 상호계산계정 폐쇄 신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.311 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 계정상대방 | 계정상대방 | 계정상대방 | text |  |
| 대차기잔고 | 대차기잔고 | 대차기잔고 | text |  |
| 폐쇄사유 | 폐쇄사유 | 폐쇄사유 | text | 주택구입 |
| 기타 | 기타 | 기타 | text | 해당 없음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 명 | text | 박찬연 |
| seal.signer | seal.customer | 명 | seal | 강순준 |
| sign.signer | sign.customer | 명 | signature | 박찬연 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| seal.signer2 | seal.signer2 | 은행장 | seal | 김도현 |
| sign.signer2 | sign.signer2 | 은행장 | signature | 엄혜린 |

### hf312 · 비거주자원화계정을 통한 송금(투자)보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.312 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 가신고수리일자및신고수리번호 | 가신고수리일자및신고수리번호 | 가.신고수리일자및신고수리번호 | date | 2025.12.07 |
| 나투자국명 | 나투자국명 | 나.투자국명 | text | 중국 |
| 다투자업종 | 다투자업종 | 다.투자업종 | text |  |
| 라북한현지법인명 | 라북한현지법인명 | 라.북한현지법인명 | text | (주)유니온무역 |
| 가수취인 | 가수취인 | 가.수취인 | text | 주식회사 다온무역 |
| 나비거주자원화계정계좌번호 | 나비거주자원화계정계좌번호 | 나.비거주자원화계정계좌번호 | text | 756-619878-83693 |
| 송금일자 | 송금일자 | (1)송금일자 | date | 2025-04-20 |
| 투자내용 | 투자내용 | (3)투자내용 | text | 해당 없음 |

### hf313 · 북한지사 설치·현황 보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.313 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| date | date | 일자 | date | 2026년 01월 31일 |
| 목록[].신고자 | 목록[].신고자 | 신고자 | text | (주)미래정밀 |
| 기업규모 | 기업규모 | 기업규모 | text |  |
| 목록[].지사명 | 목록[].지사명 | 지사명 | text | (주)신영무역 |
| 목록[].설치지역 | 목록[].설치지역 | 설치지역 | text |  |
| 구분 | 구분 | 구분 | text |  |
| 투자금구분 | 투자금구분 | 투자금구분 | text |  |
| 목록[].신고금액 | 목록[].신고금액 | 신고금액 | number | 22,630,000 |
| 신고기관 | 신고기관 | 신고기관 | text |  |
| date2 | date2 | 신고일자 | date | 2026년 01월 31일 |
| 송금일자 | 송금일자 | 송금일자 | date | 2025.09.19 |
| 영업기금 | 영업기금 | 영업기금 | text |  |
| 설치비 | 설치비 | 설치비 | text |  |
| 기본경비 | 기본경비 | 기본경비 | text |  |
| 기타경비 | 기타경비 | 기타경비 | text | 해당 없음 |
| 최초추가 | 최초추가 | 최초,추가 | text |  |
| 지사명 | 지사명 | 지사명 | text | 제일푸드 |
| 구분2 | 구분2 | 구분(증권/부동산) | text |  |
| 취득일 | 취득일 | 취득일 | date | 2025.11.11 |
| 취득금액 | 취득금액 | 취득금액 | number | 9,050,000원 |
| 처분일 | 처분일 | 처분일 | date | 2025-12-19 |
| 처분금액 | 처분금액 | 처분금액 | number | 42,790,000 |
| 투자자명 | 투자자명 | 투자자명 | text |  |
| date3 | date3 | 신고일자 | date | 2026년 01월 31일 |
| 목록[].북한지사명 | 목록[].북한지사명 | 북한지사명 | text | (주)대성테크 |
| 주구분 | 주구분 | 주)구분 | text |  |
| 설치일 | 설치일 | 설치일 | date | 2025.08.30 |
| date4 | date4 | 일자 | date | 2026년 01월 31일 |
| 설치지역 | 설치지역 | 설치지역 | text |  |
| 신고금액 | 신고금액 | 신고금액 | number | 210,000 |
| 회수구분주 | 회수구분주 | 회수구분주 | text |  |
| 회수금액 | 회수금액 | 회수금액 | number | 299,060,000 |
| 비고 | 비고 | 비고 | text | 해당 없음 |
| 구분주 | 구분주 | 구분주 | text |  |
| 변경일자 | 변경일자 | 변경일자 | date | 2025-04-06 |
| 변경전 | 변경전 | 변경전 | text | 해당 없음 |
| 변경후 | 변경후 | 변경후 | text | 해당 없음 |

### hf314 · 북한지사 설치(변경) 신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.314 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | corp.name | 상호 | text | (주)유니온무역 |
| seal.signer | seal.corp | 상호 | seal | (주)유니온무역 |
| sign.signer | sign.customer | 상호 | signature | 주식회사 한빛패션 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| check.신고구분 | check.신고구분 | 신고구분 | checkbox | 설 치 |
| check.지사구분 | check.지사구분 | 지사구분 | checkbox | 사 무 소 |
| 지사명 | 지사명 | 지사명 | text | (주)한빛전자 |
| company.address | corp.address | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| 회계기간 | 회계기간 | 회계기간 | text |  |
| check.설치사유 | check.설치사유 | 설치사유 | checkbox | 저임활용 |
| 내용 | 내용 | 내용 | text | 해당 없음 |
| 사유 | 사유 | 사유 | text | 주택구입 |
| 신고번호 | 신고번호 | 신고번호 | text | 112691-1312756 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1****** |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고기관 | text | 이준희 |
| seal.signer2 | seal.signer2 | 신고기관 | seal | 이준희 |
| sign.signer2 | sign.signer2 | 신고기관 | signature | 정민혜 |
| 위의신청을다음과같이신고필함 | 위의신청을다음과같이신고필함 | 위의신청을다음과같이신고필함. | text |  |

### hf315 · 증권(채권)취득 보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.315 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호또는성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호또는성명 | seal | 박찬연 |
| sign.signer | sign.customer | 상호또는성명 | signature | 강순준 |
| check.투자자규모 | check.투자자규모 | 투자자규모 | checkbox | 중소기업 |
| 신고수리일자 | 신고수리일자 | 신고수리일자 | date | 2025년 4월 6일 |
| 설립년월일 | 설립년월일 | 설립년월일 | date | 2025.05.25 |
| 신고수리번호 | 신고수리번호 | 신고수리번호 | text | 555-138019-72852 |
| company.name | corp.name | 법인명 | text | (주)유니온무역 |
| 설립등기일 | 설립등기일 | 설립등기일 | date | 2025.09.13 |
| 영업개시일 | 영업개시일 | 영업개시(예정)일 | date | 2025.09.05 |
| 결산일 | 결산일 | 결산일 | date | 2025.08.19 |
| 증권취득일 | 증권취득일 | 증권취득일(자본금출자일) | date | 2025년 4월 16일 |
| 액면가액합계 | 액면가액합계 | 액면가액합계 | number | 9,710,000 |
| check.증권발행여부 | check.증권발행여부 | 증권발행여부 | checkbox | 증권미발행 |
| 증권종류 | 증권종류 | 증권종류 | text |  |
| 취득가액합계 | 취득가액합계 | 취득가액합계 | number | 68,720,000 |
| 채권취득일 | 채권취득일 | 채권취득일 | date | 2025-08-10 |
| 이자율 | 이자율 | 이자율 | number | 10 |
| check.원금회수방법 | check.원금회수방법 | 원금회수방법 | checkbox | 분할회수(총 |
| 대부원금 | 대부원금 | 대부원금 | number | 2,700,000원 |
| 대부기간 | 대부기간 | 대부기간 | text |  |
| check.증권 | check.증권 | 증권 | checkbox | 증권 |
| 상호또는성명 | 상호또는성명 | 상호또는성명 | text | (주)대성물산 |

### hf316 · 북한지사 등의 영업활동 보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.316 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 상호또는성명 | 상호또는성명 | 상호또는성명 | text | 우진정밀(주) |
| company.biz_no | corp.biz_no | 사업자(주민)등록번호 | biz_no | 264-82-36559 |
| 지사명 | 지사명 | 지사명 | text | (주)대성시스템즈 |
| company.address | corp.address | 소재지(주소) | text | 서울특별시 중구 다산로 361, 6층 |
| 설치일 | 설치일 | 설치일 | date | 2025-09-16 |
| 설치지역 | 설치지역 | 설치지역 | text |  |
| check.구분 | check.구분 | 구분 | checkbox | 사무소 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| 총자산 | 총자산 | 총자산 | text |  |
| 매출액 | 매출액 | 매출액 | number | 4,970,000 |
| 순이익금 | 순이익금 | 순이익(결손)금 | text |  |
| 영업기금잔액 | 영업기금잔액 | 영업기금잔액 | number | 5,440,000 |
| 영업손익금 | 영업손익금 | 영업손익금 | text |  |
| 자금차입현황 | 자금차입현황 | 자금차입현황 | text |  |
| 자금대여현황 | 자금대여현황 | 자금대여현황 | text |  |
| 영업기금 | 영업기금 | 영업기금 | text |  |
| 설치비 | 설치비 | 설치비 | text |  |
| 유지활동비 | 유지활동비 | 유지활동비 | text |  |
| 남한파견명 | 남한파견명 | 남한파견:명 | text |  |

### hf317 · 증권발행 보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.317 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 명칭 | 명칭 | 명칭 | text | (주)유니온무역 |
| signer.name | corp.ceo | 대표자성명 | text | 박찬연 |
| seal.signer | seal.corp | 대표자성명 | seal | 최우빈 |
| sign.signer | sign.customer | 대표자성명 | signature | 박찬연 |
| signer2.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer2 | seal.customer | 상호및대표자성명 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 상호및대표자성명 | signature | 최우빈 |
| 증권종류 | 증권종류 | 증권종류 | text |  |
| 발행금액 | 발행금액 | 발행금액 | number | 540,000 |
| 계약체결시및장소 | 계약체결시및장소 | 계약체결시및장소 | text |  |
| 표면금리 | 표면금리 | 표면금리 | number | 100 |
| 만기 | 만기 | 만기 | date | 2025.11.23 |
| 배당금지급시기및방법 | 배당금지급시기및방법 | 배당금지급시기및방법 | text |  |
| 원리금상환방법 | 원리금상환방법 | 원리금상환방법 | text | 만기일시상환 |
| 자금용도 | 자금용도 | 자금용도 | text | 타행 이체 |
| 발행관련기관 | 발행관련기관 | 발행관련기관 | text |  |
| 기타 | 기타 | 기타 | text | 해당 없음 |
| 액면금액및수량 | 액면금액및수량 | 액면금액및수량 | number | 31,180,000 |
| 발행시기및장소 | 발행시기및장소 | 발행시기및장소 | text |  |
| 발행가격 | 발행가격 | 발행가격 | text |  |
| 해외판매여부 | 해외판매여부 | 해외판매여부 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 상장여부 | 상장여부 | 상장여부 | text |  |
| 발행비용 | 발행비용 | 발행비용 | text |  |

### hf318 · 대북투자(변경)신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.318 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| signer.name | corp.ceo | 대표자 | text | 박찬연 |
| seal.signer | seal.corp | 대표자 | seal | 박찬연 |
| sign.signer | sign.customer | 대표자 | signature | 이욱유 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| check.투자구분 | check.투자구분 | 투자구분 | checkbox | 감액 |
| check.투자방식 | check.투자방식 | 투자방식 | checkbox | 대부채권취득 |
| 투자업종 | 투자업종 | 투자업종 | text |  |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| 주요제품 | 주요제품 | 주요제품 | text |  |
| 신고수리번호 | 신고수리번호 | 신고수리번호 | text | 216-642241-52609 |
| value | value | (U$) | amount |  |
| date | date | 유효기간 | date | 2026년 1월 31일 |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| 현금 | 현금 | 현금(U$) | text |  |
| 현물 | 현물 | 현물(U$) | text |  |
| 합계 | 합계 | 합계(U$) | number | 27,020,000 |
| 목록[].대부투자 | 목록[].대부투자 | 대부투자 | text |  |
| 목록[].총투자액 | 목록[].총투자액 | 총투자액 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고기관 | text | 석철성 |
| seal.signer2 | seal.signer2 | 신고기관 | seal | 석철성 |
| sign.signer2 | sign.signer2 | 신고기관 | signature | 연태재 |
| company.ceo | company.ceo | 대표자 | text | 박찬연 |
| 현지법인명 | 현지법인명 | 현지법인명 | text | 주식회사 새한푸드 |
| 위의신고를다음과같이신고필함 | 위의신고를다음과같이신고필함 | 위의신고를다음과같이신고필함. | text |  |
| 유효기간 | 유효기간 | 유효기간 | text |  |

### hf319 · 증권취득 신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.319 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 박찬연 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 이욱유 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| 증권취득자 | 증권취득자 | 증권취득자 | text |  |
| 증권취득상대방 | 증권취득상대방 | 증권취득상대방 | text |  |
| check.증권취득방법 | check.증권취득방법 | 증권취득방법 | checkbox | 기타 교환 |
| check.증권종류 | check.증권종류 | 증권종류 | checkbox | 직접기재( |
| 액면가액 | 액면가액 | 액면가액 | number | 840,000 |
| 수량 | 수량 | 수량 | number | 36 |
| 취득단가 | 취득단가 | 취득단가 | number | 83,950,000 |
| 취득가액 | 취득가액 | 취득가액 | number | 160,170,000 |
| 취득사유 | 취득사유 | 취득사유 | text | 해외 이주 |
| 신고번호 | 신고번호 | 신고번호 | text | 344-177699-45189 |
| 신고금액 | 신고금액 | 신고금액 | number | 97,620,000 |
| date | date | 신고일자 | date | 2026년 01월 31일 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 기타참고사항 | 기타참고사항 | 기타참고사항 | text | 원천징수영수증 나중에 제출 |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 신고기관 | 신고기관 | 신고기관 | text |  |

### hf320 · 재환전 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.320 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명(NAME) | text | 박찬연 |
| 여권번호 | 여권번호 | 여권번호(PASSPORTNUMBER) | text | M79050511 |
| 입국일자 | 입국일자 | 입국일자(ENTRANCEDATEINTOKOREA) | date | 2025년 6월 7일 |

### hf321 · 부동산취득신고(수리)서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.321 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 강순준 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 박찬연 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| 부동산의종류 | 부동산의종류 | 부동산의종류 | text |  |
| company.address | corp.address | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| 면적 | 면적 | 면적 | text |  |
| 취득기간 | 취득기간 | 취득기간 | text |  |
| 취득사유 | 취득사유 | 취득사유 | text | 해외 이주 |
| 신고번호 | 신고번호 | 신고(수리)번호 | text | 289-004351-06976 |
| 신고금액 | 신고금액 | 신고(수리)금액 | number | 390,000원 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 신고수리조건 | 신고수리조건 | 신고수리조건 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| seal.signer2 | seal.signer2 | 신고수리기관:한국은행총재 | seal | 박진승 |
| sign.signer2 | sign.signer2 | 신고수리기관:한국은행총재 | signature | 김선태 |
| 소 | 소 | 소(소재지) | text |  |
| 취득가액 | 취득가액 | 취득가액 | number | 5,230,000원 |
| 위의신고를다음과같이신고수리함 | 위의신고를다음과같이신고수리함 | 위의신고를다음과같이신고수리함. | text |  |

### hf322 · 북한사무소 경비지급신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.322 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.신청내역 | check.신청내역 | 신청내역 | checkbox | 설 치 비 |
| check.신청내역2 | check.신청내역2 | 신청내역 | checkbox | 유지활동비 |
| signer.name | signer.name | 성명(법인명) | text | 박찬연 |
| seal.signer | seal.customer | 성명(법인명) | seal | 박찬연 |
| sign.signer | sign.customer | 성명(법인명) | signature | 현예지 |
| 영업내용 | 영업내용 | 영업내용 | text | 해당 없음 |
| 사무소명 | 사무소명 | 사무소명 | text |  |
| customer.address | customer.address | 주소(소재지) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| value | value | (주소)(전화번호)(e-mail) | amount |  |
| value2 | value2 | (기본경비) | amount |  |
| value3 | value3 | (기타경비) | amount |  |
| customer.rrn | customer.rrn | 주민(사업자)등록번호 | rrn | 900210-1****** |
| 신고번호 | 신고번호 | 신고번호 | text | 0354-1925 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고기관 | text | 함선현 |
| seal.signer2 | seal.signer2 | 신고기관 | seal | 함선현 |
| sign.signer2 | sign.signer2 | 신고기관 | signature | 양욱수 |
| customer.name | customer.name | 성명(법인명) | text | 박찬연 |

### hf323 · 북한지점 경비지급신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.323 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | signer.name | 성명(법인명) | text | 박찬연 |
| seal.signer | seal.customer | 성명(법인명) | seal | 강순준 |
| sign.signer | sign.customer | 성명(법인명) | signature | 현예지 |
| 영업내용 | 영업내용 | 영업내용 | text | 해당 없음 |
| check.지점구분 | check.지점구분 | 지점구분 | checkbox | 비독립채산지점 |
| 지점명 | 지점명 | 지점명 | text | 범어지점 |
| customer.address | customer.address | 주소(소재지) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| check.비독립채산지점 | check.비독립채산지점 | 비독립채산지점 | checkbox | 설 치 비 |
| check.비독립채산지점2 | check.비독립채산지점2 | 비독립채산지점 | checkbox | 유지활동비 |
| 영업기금 | 영업기금 | 영업기금 | text |  |
| 비독립채산지점_목록[].value | 비독립채산지점_목록[].value | (주소)(전화번호)(e-mail) | amount |  |
| value | value | (기본경비) | amount |  |
| value2 | value2 | (기본경비) | amount |  |
| customer.rrn | customer.rrn | 주민(사업자)등록번호 | rrn | 900210-1659382 |
| 신고번호 | 신고번호 | 신고번호 | text | 0845-8826 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고기관 | text | 한채혜 |
| seal.signer2 | seal.signer2 | 신고기관 | seal | 한채혜 |
| sign.signer2 | sign.signer2 | 신고기관 | signature | 윤승아 |
| customer.name | customer.name | 성명(법인명) | text | 박찬연 |

### hf324 · 임대차계약신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.324 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 이욱유 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 박찬연 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| 임대차물종류 | 임대차물종류 | 임대차물종류 | text |  |
| company.address | corp.address | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| 수량 | 수량 | 수량 | number | 36 |
| 임대차기간 | 임대차기간 | 임대차기간 | text |  |
| 임대차사유 | 임대차사유 | 임대차사유 | text | 학자금 |
| 신고번호 | 신고번호 | 신고번호 | text | 2113-1678 |
| date | date | 신고일자 | date | 2026년 01월 31일 |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |

### hf325 · 증권취득신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.325 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 박찬연 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 강순준 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| 액면가액 | 액면가액 | 액면가액 | number | 73,980,000 |
| 수량 | 수량 | 수량 | number | 3 |
| 취득단가 | 취득단가 | 취득단가 | number | 41,940,000원 |
| 취득사유 | 취득사유 | 취득사유 | text | 의료비 |
| 신고번호 | 신고번호 | 신고번호 | text | 4891-5750 |
| 신고금액 | 신고금액 | 신고금액 | number | 21,350,000 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| seal.signer2 | seal.signer2 | 신고기관:외국환은행의장 | seal | 정규준 |
| sign.signer2 | sign.signer2 | 신고기관:외국환은행의장 | signature | 허규아 |

### hf326 · ( )매매 신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.326 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 박찬연 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 현예지 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| 매매대상물종류 | 매매대상물종류 | 매매대상물종류 | text |  |
| 매매사유 | 매매사유 | 매매사유 | text | 급여 수령 |
| 신고번호 | 신고번호 | 신고번호 | text | 024798-5563156 |
| 신고금액 | 신고금액 | 신고금액 | number | 52,210,000원 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신고기관:한국은행총재 | text | 최나원 |
| seal.signer2 | seal.signer2 | 신고기관:한국은행총재 | seal | 이소도 |
| sign.signer2 | sign.signer2 | 신고기관:한국은행총재 | signature | 최나원 |
| 매매금액 | 매매금액 | 매매금액 | number | 1,680,000원 |

### hf327 · 담보제공 신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.327 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 상호및대표자성명 | text | 박찬연 |
| seal.signer | seal.customer | 상호및대표자성명 | seal | 강순준 |
| sign.signer | sign.customer | 상호및대표자성명 | signature | 박찬연 |
| company.biz_item | corp.biz_item | 업종(직업) | text | 무역 |
| check.담보제공자 | check.담보제공자 | 담보제공자 | checkbox | 거주자/ |
| check.담보취득자 | check.담보취득자 | 담보취득자 | checkbox | 거주자/ |
| check.담보제공수혜자 | check.담보제공수혜자 | 담보제공수혜자 | checkbox | 거주자/ |
| check.담보물종류 | check.담보물종류 | 담보물종류 | checkbox | 부동산 |
| 담보소재지 | 담보소재지 | 담보소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 수량 | 수량 | 수량 | number | 3 |
| 담보가액 | 담보가액 | 담보가액 | number | 1,610,000 |
| 담보제공기간 | 담보제공기간 | 담보제공기간 | text |  |
| check.담보제공용도 | check.담보제공용도 | 담보제공용도 | checkbox | 주채무계열소속 30대 계열기업체의 단기외화차입에 대한 담보제공 |
| 신고번호 | 신고번호 | 신고번호 | text | 006352-1615394 |
| 신고금액 | 신고금액 | 신고금액 | number | 760,000 |
| date | date | 신고일자 | date | 2026.01.31 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 기타참고사항 | 기타참고사항 | 기타참고사항 | text | 치료비 100만 상담, 5년 희망 |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 신고기관 | 신고기관 | 신고기관 | text |  |

### hf328 · 외국기업 국내지사 폐쇄신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.328 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| company.address | corp.address | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| check.폐쇄구분 | check.폐쇄구분 | 폐쇄구분 | checkbox | 지점 |
| 폐쇄일자 | 폐쇄일자 | 폐쇄일자 | date | 2025-09-26 |
| 폐쇄사유 | 폐쇄사유 | 폐쇄사유 | text | 의료비 |
| 신고번호 | 신고번호 | 신고번호 | text | 125-702414-61662 |
| date | date | 신고일자 | date | 2026년 01월 31일 |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신고인 | text | 박찬연 |
| seal.signer | seal.customer | 신고인 | seal | 박찬연 |
| sign.signer | sign.customer | 신고인 | signature | 현예지 |
| 폐쇄구분 | 폐쇄구분 | 폐쇄구분 | text |  |
| 위와같이신고되었음을확인함 | 위와같이신고되었음을확인함 | 위와같이신고되었음을확인함. | text |  |

### hf329 · 외국기업 국내지사 설치신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.329 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 상호(본점) | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자(본점) | text | 박찬연 |
| company.address | corp.address | 소재지(본점) | text | 서울특별시 중구 다산로 361, 6층 |
| 사업내용 | 사업내용 | 사업내용 | text | 해당 없음 |
| 자본금 | 자본금 | 자본금 | text |  |
| company.name2 | company.name2 | 상호 | text | (주)유니온무역 |
| company.ceo2 | company.ceo2 | 대표자 | text | 박찬연 |
| company.address2 | company.address2 | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| 영위업종 | 영위업종 | 영위업종 | text |  |
| check.설치구분 | check.설치구분 | 설치구분 | checkbox | 사무소 |
| date | date | 설치년월일 | date | 2026년 1월 31일 |
| customer.rrn | customer.rrn | 주민등록번호(또는국적) | rrn | 900210-1****** |
| 신고번호 | 신고번호 | 신고번호 | text | 8843-1585 |
| date2 | date2 | 신고일자 | date | 2026년 01월 31일 |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신고인 | text | 박찬연 |
| seal.signer | seal.customer | 신고인 | seal | 강순준 |
| sign.signer | sign.customer | 신고인 | signature | 박찬연 |
| 신고기관기획재정부장관 | 신고기관기획재정부장관 | 신고기관:기획재정부장관 | text |  |

### hf330 · 외국기업 국내지사 변경신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.330 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 이미신고된사항 | 이미신고된사항 | 이미신고된사항 | text |  |
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| company.address | corp.address | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| 변경사유 | 변경사유 | 변경사유 | text | 결혼자금 |
| 변경하고자하는사항 | 변경하고자하는사항 | 변경하고자하는사항 | text |  |
| 신고번호 | 신고번호 | 신고번호 | text | 081-400281-43556 |
| date | date | 신고일자 | date | 2026년 01월 31일 |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신고인 | text | 박찬연 |
| seal.signer | seal.customer | 신고인 | seal | 현예지 |
| sign.signer | sign.customer | 신고인 | signature | 강순준 |
| 신고기관기획재정부장관 | 신고기관기획재정부장관 | 신고기관:기획재정부장관 | text |  |

### hf331 · 해외지점의 영업활동 보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.331 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 상호또는성명 | 상호또는성명 | 상호또는성명 | text | (주)가온화학 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.biz_no | corp.biz_no | 사업자(주민)등록번호 | biz_no | 264-82-36559 |
| 지점명 | 지점명 | 지점명 | text | 범어지점 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 설치일 | 설치일 | 설치일 | date | 2025.09.08 |
| 설치국가 | 설치국가 | 설치국가 | text | 필리핀 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| 총자산 | 총자산 | 총자산 | text |  |
| 매출액 | 매출액 | 매출액 | number | 45,210,000 |
| 순이익금 | 순이익금 | 순이익(결손)금 | text |  |
| 영업기금잔액 | 영업기금잔액 | 영업기금잔액 | number | 770,000 |
| 영업손익금 | 영업손익금 | 영업손익금 | text |  |
| 자금차입현황 | 자금차입현황 | 자금차입현황 | text |  |
| 자금대여현황 | 자금대여현황 | 자금대여현황 | text |  |
| 영업기금 | 영업기금 | 영업기금 | text |  |
| 본국파견명 | 본국파견명 | 본국파견:명 | text |  |

### hf332 · 외국기업 국내 결산순이익금 송금신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.332 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 상호(본점) | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자(본점) | text | 박찬연 |
| company.address | corp.address | 본점소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| 송금예정일자 | 송금예정일자 | 송금예정일자 | date | 2025년 6월 4일 |
| 송금액산출근거 | 송금액산출근거 | 송금액산출근거 | number | 420,000 |
| 결산기간 | 결산기간 | 결산기간 | number | 1 |
| 처리기간 | 처리기간 | 처리기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 현예지 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| 금액 | 금액 | 금액 | number | 16,300,000 |

### hf333 · 송금(투자)보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.333 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 현금현물주식이익잉여금기술투자기타 | 현금현물주식이익잉여금기술투자기타 | 현금현물주식이익잉여금기술투자기타() | text | 해당 없음 |
| 투자액 | 투자액 | 투자(송금)액(U$환산액) | text |  |
| 투자방법 | 투자방법 | 투자방법 | text |  |
| 비고 | 비고 | 비고(현지화) | text | 해당 없음 |
| 가신고일자및신고번호 | 가신고일자및신고번호 | 가.신고일자및신고번호 | date | 2025.01.07 |
| 나투자국명 | 나투자국명 | 나.투자국명 | text | 필리핀 |
| 다투자업종 | 다투자업종 | 다.투자업종 | text |  |
| 라현지법인명 | 라현지법인명 | 라.현지법인명 | text | (주)유니온무역 |
| 가수취인 | 가수취인 | 가.수취인 | text | (주)세진상사 |
| 나구좌번호 | 나구좌번호 | 나.구좌번호 | text | 2201-7126 |

### hf334 · 전자적무역결제금융등록(변경,해지)신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.334 (외환) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| value | value | (한글) | amount |  |
| value2 | value2 | (영문) | amount |  |
| company.biz_no | corp.biz_no | 사업자번호 | biz_no | 264-82-36559 |
| company.ceo | corp.ceo | 대표자성명 | text | 박찬연 |
| value3 | value3 | (한글) | amount |  |
| value4 | value4 | (영문) | amount |  |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| company.corp_reg_no | corp.corp_reg_no | 법인번호 | corp_reg_no | 200112-7448551 |
| 대표자생년월일 | 대표자생년월일 | 대표자생년월일 | date | 2025-11-05 |
| 팩스번호 | 팩스번호 | 팩스번호 | phone | 043-783-2775 |
| customer.name2 | customer.name2 | 성명 | text | 박찬연 |
| customer.email2 | customer.email2 | E-mail | text | chanyeon363@naver.com |
| 원화 | 원화 | 원화(KRW) | text |  |
| 미화 | 미화 | 미화(USD) | text |  |
| 위안화 | 위안화 | 위안화(CNY) | text |  |
| 엔화 | 엔화 | 엔화(JPY) | text |  |
| 목록[].거래인감 | 목록[].거래인감 | 거래인감 | text |  |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| value5 | value5 | (한글) | amount |  |
| 기업식별번호 | 기업식별번호 | 기업식별번호 | text | 224564-5206792 |
| value6 | value6 | (한글) | amount |  |
| value7 | value7 | (영문) | amount |  |
| customer.phone2 | customer.phone2 | 전화번호 | phone | 010-5907-7253 |
| value8 | value8 | (은행명) | amount |  |
| value9 | value9 | (계좌번호) | amount |  |
| customer.name3 | customer.name3 | 성명 | text | 박찬연 |
| customer.phone3 | customer.phone3 | 전화번호 | phone | 010-5907-7253 |
| 팩스번호2 | 팩스번호2 | 팩스번호 | phone | 043-783-2775 |
| BicCode | BicCode | BicCode | text |  |
| foreign.address | foreign.address | 주소(영문) | text | 45 Le Loi St, District 1, Ho Chi Minh City |
| 팩스번호3 | 팩스번호3 | 팩스번호 | phone | 043-783-2775 |
| customer.email3 | customer.email3 | E-mail | text | chanyeon363@naver.com |
| 신청인주소 | 신청인주소 | 신청인(업체)주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.name | corp.name | 업체명 | text | (주)유니온무역 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 최수우 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이승연 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 박다린 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 박영원 |

### hf335 · 하나 입출금 거래내역 문자통지서비스 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.335 (전자금융) 원본 위에 기재

연결 업무: 전자금융 가입 (efinance_signup)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명(업체명) | text | 박찬연 |
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 변경 |
| customer.birth | customer.birth | 생년월일(사업자등록번호) | date | 1990.02.10 |
| check.이용료미납시문자통지 | check.이용료미납시문자통지 | 이용료미납시문자통지 | checkbox | 신청 |
| 통지대상계좌 | 통지대상계좌 | 통지대상계좌 | text | 398-290417-13085 |
| 이용료출금계좌 | 이용료출금계좌 | 이용료출금계좌 | text | 152-291064-40887 |
| check.요금제 | check.요금제 | 요금제 | checkbox | 종량제(건당 20원 부과) |
| check.통지대상거래유형 | check.통지대상거래유형 | 통지대상거래유형 | checkbox | 입금 |
| check.통지대상거래금액 | check.통지대상거래금액 | 통지대상거래금액 | checkbox | 입금 ( |
| check.통지범위 | check.통지범위 | 통지범위 | checkbox | 체크카드제외 |
| check.통지시간 | check.통지시간 | 통지시간 | checkbox | 실시간 (즉시) |
| check.심야자동이체통지시작시간 | check.심야자동이체통지시작시간 | 심야자동이체(C/C)통지시작시간 | checkbox | 지정시간 ( |
| check.계좌잔액 | check.계좌잔액 | 계좌잔액 | checkbox | 표시 |
| check.통지언어 | check.통지언어 | 통지언어 | checkbox | 영어 |
| 문자통지대상휴대폰번호 | 문자통지대상휴대폰번호 | 문자통지대상휴대폰번호 | phone | 010-5907-7253 |
| 문자통지대상휴대폰번호2 | 문자통지대상휴대폰번호2 | 문자통지대상휴대폰번호 | phone | 010-5907-7253 |
| 문자통지대상휴대폰번호3 | 문자통지대상휴대폰번호3 | 문자통지대상휴대폰번호 | phone | 010-5907-7253 |
| 목록[].문자통지신청계좌2 | 목록[].문자통지신청계좌2 | 문자통지신청계좌2 | text | 325-353618-10562 |
| check.정액제 | check.정액제 | 정액제(월800원) | checkbox | 정액제(월 800원) |
| check.입금 | check.입금 | 입금 | checkbox | 출금 |
| check.입금2 | check.입금2 | 입금( | checkbox | 출금 ( |
| check.모든거래 | check.모든거래 | 모든거래 | checkbox | 자동이체(C/C)제외 |
| check[] | check[] | 08:00~24:00(심야시간지연통지) | checkbox | 실시간 (즉시) |
| check.지정시간 | check.지정시간 | 지정시간( | checkbox | 실시간 (00시) |
| check.표시 | check.표시 | 표시 | checkbox | 미표시 |
| check.한글 | check.한글 | 한글 | checkbox | 영어 |
| 목록[].문자통지신청계좌3 | 목록[].문자통지신청계좌3 | 문자통지신청계좌3 | text | 239-738259-74435 |
| check.정액제2 | check.정액제2 | 정액제(월800원) | checkbox | 정액제(월 800원) |
| check.입금3 | check.입금3 | 입금 | checkbox | 입금 |
| check.입금4 | check.입금4 | 입금( | checkbox | 출금 ( |
| check.모든거래2 | check.모든거래2 | 모든거래 | checkbox | 모든거래 |
| check.지정시간2 | check.지정시간2 | 지정시간( | checkbox | 지정시간 ( |
| check.표시2 | check.표시2 | 표시 | checkbox | 표시 |
| check.한글2 | check.한글2 | 한글 | checkbox | 영어 |
| agent.relation | agent.relation | 관계 | text | 부 |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.phone | agent.phone | 연락처 | phone | 010-6515-4769 |
| agent.birth | agent.birth | 생년월일 | date | 1962년 12월 19일 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청및수령인 | text | 박찬연 |
| seal.signer | seal.customer | 신청및수령인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청및수령인 | signature | 현예지 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김환빈 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 박상주 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 확인 |

연결 업무 efinance_signup · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### hf336 · 개인 전자금융 서비스 신청서(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.336 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | Name | text | 박찬연 |
| customer.address | customer.address | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.email | customer.email | E-Mail | text | chanyeon363@naver.com |
| UserID | UserID | UserID | text | 383503-5687186 |
| customer.birth | customer.birth | DateofBirth | date | 1990-02-10 |
| HomePhone | HomePhone | HomePhone | text |  |
| GMgr | GMgr | GMgr | text |  |
| Manager | Manager | Manager | text |  |
| Clerk | Clerk | Clerk | text |  |
| 목록[].BankName | 목록[].BankName | BankName | text |  |
| 목록[].AccountNo | 목록[].AccountNo | AccountNo. | text | 250843-2802292 |
| 목록[].SpeedDialNumberforPhoneBanking | 목록[].SpeedDialNumberforPhoneBanking | SpeedDialNumberforPhoneBanking | text |  |
| customer.name2 | customer.name2 | Name | text | 박찬연 |
| customer.birth2 | customer.birth2 | DateofBirth | date | 1990-02-10 |
| Delegator | Delegator | Delegator | text |  |
| ToHanaBank | ToHanaBank | To:HanaBank | text |  |
| BranchGeneralManager | BranchGeneralManager | BranchGeneralManager | text |  |
| OTPManufacturer | OTPManufacturer | ) OTP(Manufacturer | text |  |
| Applicant | Applicant | Applicant | text | (주)유니온무역 |
| KRW | KRW | KRW), | text |  |
| Category | Category | Category | text |  |
| DesignateChange | DesignateChange |  Designate Change | text |  |
| OtherRequests | OtherRequests | ■OtherRequests | text |  |
| PowerofAttorney | PowerofAttorney | ■PowerofAttorney | text |  |
| customer.name3 | customer.name3 | Name | text | 박찬연 |
| customer.address2 | customer.address2 | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.email2 | customer.email2 | E-Mail | text | chanyeon363@naver.com |
| UserID2 | UserID2 | UserID | text | 400-384836-49075 |
| customer.birth3 | customer.birth3 | DateofBirth | date | 1990-02-10 |
| HomePhone2 | HomePhone2 | HomePhone | text |  |
| customer.name4 | customer.name4 | Name | text | 박찬연 |
| customer.birth4 | customer.birth4 | DateofBirth | date | 1990-02-10 |
| Delegator2 | Delegator2 | Delegator | text |  |
| OTPManufacturer2 | OTPManufacturer2 | ) OTP(Manufacturer | text |  |
| Applicant2 | Applicant2 | Applicant | text | 새한전자 |
| KRW2 | KRW2 | KRW), | text |  |
| Category2 | Category2 | Category | text |  |
| DesignateChange2 | DesignateChange2 |  Designate Change | text |  |
| OtherRequests2 | OtherRequests2 | ■OtherRequests | text |  |
| PowerofAttorney2 | PowerofAttorney2 | ■PowerofAttorney | text |  |

### hf337 · 개인 전자금융 서비스 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.337 (전자금융) 원본 위에 기재

연결 업무: 전자금융 가입 (efinance_signup)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.email | customer.email | E-Mail주소 | text | chanyeon363@naver.com |
| 이용자ID | 이용자ID | 이용자ID | text | 055-030158-64829 |
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| customer.home_phone | customer.home_phone | 자택전화(직장전화) | phone | 02-2611-9326 |
| customer.phone | customer.phone | 휴대전화 | phone | 010-5907-7253 |
| 목록[].은행명 | 목록[].은행명 | 은행명 | text | 하나은행 |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 853-996761-31226 |
| 목록[].폰뱅킹단축번호 | 목록[].폰뱅킹단축번호 | 폰뱅킹단축번호 | text | 349-599247-65257 |
| 목록[].통장인감서명 | 목록[].통장인감서명 | 통장인감/서명 | text |  |
| agent.name | agent.name | 성명 | text | 박영준 |
| 계 | 계 | 계 | text |  |
| 명 | 명 | 명 | text |  |
| 소 | 소 | 소 | text |  |
| customer.name2 | customer.name2 | 위임인 | text | 박찬연 |
| seal.signer | seal.signer | 실명증표진위여부확인필 | seal | 방동찬 |
| sign.signer | sign.signer | 실명증표진위여부확인필 | signature | 남현태 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 지점장 | 지점장 | 지점장 | text | 범어지점 |
| 자물쇠카드일련번호 | 자물쇠카드일련번호 |  자물쇠카드(일련번호 | text | 745635-9583584 |
| OTP제조업체 | OTP제조업체 | ) OTP(제조업체 | text |  |
| 일련번호 | 일련번호 | ,일련번호 | text | 472036-9354982 |
| customer.name3 | customer.name3 | 신청인 | text | 박찬연 |
| 구분 | 구분 | 구분 | text |  |
| 3시간지연4시간지연 | 3시간지연4시간지연 |  3시간지연, 4시간지연 | text |  |
| 위임장 | 위임장 | ■위임장 | text |  |
| 실명확인증표사본 | 실명확인증표사본 | 실명확인증표사본 | text |  |
| customer.name4 | customer.name4 | 성명 | text | 박찬연 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.email2 | customer.email2 | E-Mail주소 | text | chanyeon363@naver.com |
| 이용자ID2 | 이용자ID2 | 이용자ID | text | 1624-0366 |
| customer.birth2 | customer.birth2 | 생년월일 | date | 1990.02.10 |
| customer.home_phone2 | customer.home_phone2 | 자택전화(직장전화) | phone | 02-2611-9326 |
| customer.phone2 | customer.phone2 | 휴대전화 | phone | 010-5907-7253 |
| agent.name2 | agent.name2 | 성명 | text | 박영준 |
| 계2 | 계2 | 계 | text |  |
| 명2 | 명2 | 명 | text |  |
| 소2 | 소2 | 소 | text |  |
| customer.name5 | customer.name5 | 위임인 | text | 박찬연 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 자물쇠카드일련번호2 | 자물쇠카드일련번호2 |  자물쇠카드(일련번호 | text | 258-594727-48424 |
| OTP제조업체2 | OTP제조업체2 | ) OTP(제조업체 | text |  |
| 일련번호2 | 일련번호2 | ,일련번호 | text | 894-734344-70717 |
| customer.name6 | customer.name6 | 신청인 | text | 박찬연 |
| 구분2 | 구분2 | 구분 | text |  |
| 3시간지연4시간지연2 | 3시간지연4시간지연2 |  3시간지연, 4시간지연 | text |  |
| 위임장2 | 위임장2 | ■위임장 | text |  |

연결 업무 efinance_signup · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### hf338 · 기업 전자금융서비스 신청서(은행용)(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.338 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| Clerk | Clerk | Clerk | text |  |
| Mgr | Mgr | Mgr | text |  |
| GM | GM | GM | text |  |
| NameCompanyName | NameCompanyName | Name/CompanyName | text |  |
| customer.address | customer.address | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| OtherRequest | OtherRequest | OtherRequest | text |  |
| BusinessRegistrationNo | BusinessRegistrationNo | BusinessRegistrationNo. | biz_no | 264-82-36559 |
| DailyKRW | DailyKRW | DailyKRW, | text |  |
| KRW | KRW | KRW | text |  |
| OnetimeKRW | OnetimeKRW | One-timeKRW | text |  |
| OnetimeKRW2 | OnetimeKRW2 | One-timeKRW | text |  |
| OnetimeKRW3 | OnetimeKRW3 | One-timeKRW | text |  |
| 목록[].OverseasIPBlockingService | 목록[].OverseasIPBlockingService | OverseasIPBlockingService | text |  |
| OTP | OTP | OTP | text |  |
| 목록[].OfficeName | 목록[].OfficeName | OfficeName | text |  |
| PhoneNoforIdentityVerification | PhoneNoforIdentityVerification | PhoneNo.forIdentityVerification | phone | 010-5907-7253 |
| 목록[].BusinessRegistrationNo | 목록[].BusinessRegistrationNo | BusinessRegistrationNo. | text | 264-82-36559 |
| RequestNotRequest | RequestNotRequest | RequestNotRequest | text |  |
| 목록[].CorporateRegistrationNo | 목록[].CorporateRegistrationNo | CorporateRegistrationNo. | text | 965-283639-91822 |
| PostpaidFee | PostpaidFee | Post-paidFee | text |  |
| RequestCancel | RequestCancel | Request(Account:)Cancel | text |  |
| OtherChange | OtherChange | OtherChange | text |  |
| GeneralUser | GeneralUser | GeneralUser | text |  |
| OTP2 | OTP2 | OTP | text |  |
| UserCategory | UserCategory | UserCategory | text |  |
| RequestCancel2 | RequestCancel2 | RequestCancel | text |  |
| DailyKRW2 | DailyKRW2 | DailyKRW | text |  |
| OnetimeKRW4 | OnetimeKRW4 | One-timeKRW | text |  |
| WithdrawalAccount | WithdrawalAccount | WithdrawalAccount | text |  |
| WithdrawalAccount2 | WithdrawalAccount2 | WithdrawalAccount | text |  |
| WithdrawalAccount_목록[].UserID | WithdrawalAccount_목록[].UserID | UserID | text | 3602-0274 |
| DailyKRW3 | DailyKRW3 | DailyKRW | text |  |
| OnetimeKRW5 | OnetimeKRW5 | One-timeKRW | text |  |
| DesignationofBeneficiaryAccount | DesignationofBeneficiaryAccount | DesignationofBeneficiaryAccount | text |  |
| DesignationofBeneficiaryAccount2 | DesignationofBeneficiaryAccount2 | DesignationofBeneficiaryAccount | text |  |
| DesignationofBeneficiaryAccount3 | DesignationofBeneficiaryAccount3 | DesignationofBeneficiaryAccount | text |  |
| DesignationofBeneficiaryAccount4 | DesignationofBeneficiaryAccount4 | DesignationofBeneficiaryAccount | text |  |
| customer.name | customer.name | Name | text | 박찬연 |
| customer.address2 | customer.address2 | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| Relationship | Relationship | Relationship | text |  |
| customer.birth | customer.birth | DateofBirth | date | 1990.02.10 |
| Delegator | Delegator | Delegator | text |  |
| DoNOTAgree | DoNOTAgree | DoNOTAgree | text |  |

### hf340 · 기업 전자금융서비스 신청서(은행용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.340 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 성명업체명 | 성명업체명 | 성명/업체명 | text | (주)유니온무역 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 기타신청사항 | 기타신청사항 | 기타신청사항 | text | 해당 없음 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| customer.birth | customer.birth | 생년월일(법인등록번호) | date | 1990.02.10 |
| 일원 | 일원 | 일원, | text |  |
| 출금계좌지정 | 출금계좌지정 | 출금계좌지정(괄호는폰뱅킹단축번호***) | text | 464-953334-06435 |
| 기업뱅킹업체총이체한도 | 기업뱅킹업체총이체한도 | 기업뱅킹업체총이체한도(1일) | number | 50,000 |
| 회원 | 회원 | 회원 | text |  |
| 입금계좌지정신청신청안함_목록[].해외IP차단 | 입금계좌지정신청신청안함_목록[].해외IP차단 | 해외IP차단 | text |  |
| OTP | OTP | OTP | text |  |
| 기업뱅킹본지사서비스신청해지_목록[].지사명 | 기업뱅킹본지사서비스신청해지_목록[].지사명 | 지사명 | text | (주)유니온무역 |
| 본인인증전화번호 | 본인인증전화번호 | 본인인증전화번호 | phone | 010-5907-7253 |
| 기업뱅킹본지사서비스신청해지_목록[].사업자번호 | 기업뱅킹본지사서비스신청해지_목록[].사업자번호 | 사업자번호 | biz_no | 264-82-36559 |
| 신청미신청 | 신청미신청 | 신청미신청 | text |  |
| 기업뱅킹본지사서비스신청해지_목록[].법인등록번호 | 기업뱅킹본지사서비스신청해지_목록[].법인등록번호 | 법인등록번호 | text | 671518-5579757 |
| 수수료후취 | 수수료후취 | 수수료후취 | number | 244,400,000원 |
| 신청해지 | 신청해지 | 신청(계좌:)해지 | text |  |
| signer.name | corp.ceo | 대표자 | text | 박찬연 |
| seal.signer | seal.corp | 대표자 | seal | 강순준 |
| sign.signer | sign.customer | 대표자 | signature | 박찬연 |
| signer2.name | signer2.name | 확인자명 | text | 곽수혜 |
| seal.signer2 | seal.signer2 | 확인자명 | seal | 곽수혜 |
| sign.signer2 | sign.signer2 | 확인자명 | signature | 손경주 |
| signer3.name | signer3.name | 대표자 | text | 박찬연 |
| seal.signer3 | seal.signer3 | 대표자 | seal | 현예지 |
| sign.signer3 | sign.signer3 | 대표자 | signature | 박찬연 |
| signer4.name | signer4.name | 확인자명 | text | 이선승 |
| seal.signer4 | seal.signer4 | 확인자명 | seal | 이다우 |
| sign.signer4 | sign.signer4 | 확인자명 | signature | 김석윤 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer5.name | customer.name | 신청및수령인 | text | 박찬연 |
| seal.signer5 | seal.customer | 신청및수령인 | seal | 강순준 |
| sign.signer5 | sign.signer5 | 신청및수령인 | signature | 박찬연 |
| signer6.name | signer6.name | 대리인 | text | 이도민 |
| seal.signer6 | seal.agent | 대리인 | seal | 이도민 |
| sign.signer6 | sign.agent | 대리인 | signature | 김순우 |
| signer7.name | signer7.name | 대리인 | text | 강석호 |
| seal.signer7 | seal.signer7 | 대리인 | seal | 이도민 |
| sign.signer7 | sign.signer7 | 대리인 | signature | 강석호 |
| OTP2 | OTP2 | OTP | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 허영빈 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 권민수 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 심다수 |
| seal.staff.지점장 | seal.staff.지점장 | 지점장 | seal | 천옥경 |
| sign.staff.지점장 | sign.staff.지점장 | 지점장 | signature | 강주하 |
| 사용자구분 | 사용자구분 | 사용자구분 | text |  |
| account | account | 출금계좌 | account_no | 000-287736-52424 |
| account2 | account2 | 출금계좌 | account_no | 000-287736-52424 |
| 출금계좌_목록[].대량이체한도iNetCMS에한함 | 출금계좌_목록[].대량이체한도iNetCMS에한함 | 대량이체한도iNet*CMS에한함 | number | 2,660,000 |
| 입금계좌지정 | 입금계좌지정 | 입금계좌지정 | text | 987-677266-08893 |
| 입금계좌지정2 | 입금계좌지정2 | 입금계좌지정 | text | 476-729413-08304 |
| 입금계좌지정3 | 입금계좌지정3 | 입금계좌지정 | text | 194-363196-96440 |
| 입금계좌지정4 | 입금계좌지정4 | 입금계좌지정 | text | 281-625316-19479 |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.relation | agent.relation | 관계 | text | 부 |
| agent.birth | agent.birth | 생년월일 | date | 1962년 12월 19일 |
| agent.name2 | agent.name2 | 위임인 | text | 박영준 |
| 해지 | 해지 | 해지 | text |  |

### hf341 · 기업 전자금융서비스 신청확인서(고객용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.341 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 전국대표번호1599111115881111 | 전국대표번호1599111115881111 | 전국대표번호\|1599-1111,1588-1111 | text | 0499-6689 |
| 기업모바일뱅킹 | 기업모바일뱅킹 | 기업모바일뱅킹 | text |  |
| 기업인터넷뱅킹 | 기업인터넷뱅킹 | 기업인터넷뱅킹 | text |  |
| 해외이용시82425202500 | 해외이용시82425202500 | 해외이용시\|82-42-520-2500 | text |  |

### hf342 · 해외은행 계좌정보 수신서비스(SWIFT MT940) 이용신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.342 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 고객명 | text | 박찬연 |
| 이용자ID | 이용자ID | 이용자ID | text | 3984-4102 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| employer.address | employer.address | 회사주소 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태평양무역 구매팀 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 담당자 | 담당자 | 담당자(직위/성명) | text | 이소빈 |
| eMail주소 | eMail주소 | e-Mail주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 통지은행명 | 통지은행명 | 통지은행명 | text | 신한은행 |
| BankCode | BankCode | BankCode(BIC) | text |  |
| 통지계좌_목록[].통화 | 통지계좌_목록[].통화 | 통화 | text | USD |
| 통지계좌_목록[].계좌번호 | 통지계좌_목록[].계좌번호 | 계좌번호 | text | 437-215076-16022 |
| 통지계좌_목록[].예금주 | 통지계좌_목록[].예금주 | 예금주 | text |  |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| seal.signer | seal.customer | 거래인감 | seal | 현예지 |
| sign.signer | sign.customer | 거래인감 | signature | 이민빈 |
| check.신청종류 | check.신청종류 | 신청종류 | checkbox | 해지 |
| check.이용채널 | check.이용채널 | 이용채널 | checkbox | 기업뱅킹(통합CMS) |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 최수성 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 양미인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 변소찬 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김소원 |

### hf343 · 금융거래정보 이용제공 동의서(기업관계사서비스용)(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.343 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| HanaBank | HanaBank | HanaBank | text |  |
| HanaBank2 | HanaBank2 | HanaBank | text |  |
| Emailaddresstobenotified | Emailaddresstobenotified | E-mailaddresstobenotified | text | chanyeon363@naver.com |
| BusinessRegistrationNo | BusinessRegistrationNo | BusinessRegistrationNo. | biz_no | 533-50-23527 |

### hf344 · 기업관계사 서비스 이용계약서(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.344 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| Affiliate | Affiliate | Affiliate | text |  |
| Bank | Bank | Bank | text |  |
| company.name | corp.name | CompanyName | text | (주)유니온무역 |
| customer.address | customer.address | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| CEO | CEO | CEO | text |  |
| date | date | Date | date | 2026년 01월 31일 |
| company.name2 | company.name2 | CompanyName | text | (주)유니온무역 |
| customer.address2 | customer.address2 | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| CEO2 | CEO2 | CEO | text |  |
| date2 | date2 | Date | date | 2026년 01월 31일 |
| customer.address3 | customer.address3 | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| GeneralManager | GeneralManager | GeneralManager | text |  |
| date3 | date3 | Date | date | 2026년 01월 31일 |

### hf345 · 금융거래정보 이용제공 동의서(기업관계사서비스용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.345 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 주식회사하나은행 | 주식회사하나은행 | 주식회사하나은행 | text | 기업은행 |
| 거래정보등을제공받을자 | 거래정보등을제공받을자 | 거래정보등을제공받을자(주계약사명) | text |  |
| 통지받을이메일주소 | 통지받을이메일주소 | 통지받을이메일주소 | text | chanyeon363@naver.com |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 동의자(관계사)성명(사업자명) | text | 박찬연 |
| seal.signer | seal.customer | 동의자(관계사)성명(사업자명) | seal | 박찬연 |
| sign.signer | sign.customer | 동의자(관계사)성명(사업자명) | signature | 강순준 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 등 | 등 | 등)(이하“거래정보”) | text |  |
| 계사서비스의이행 | 계사서비스의이행 | 계사서비스의이행 | text |  |
| 관련서비스를제공받을수없게됨 | 관련서비스를제공받을수없게됨 | 관련서비스를제공받을수없게됨. | text |  |
| seal.staff.담당자 | seal.staff.담당자 | 담당자 | seal | 염석하 |
| sign.staff.담당자 | sign.staff.담당자 | 담당자 | signature | 검인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 양환유 |

### hf346 · 기업관계사 서비스 이용신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.346 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 해지 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| employer.name | employer.name | 회사명 | text | 주식회사 태평양무역 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.corp_no2 | company.corp_no2 | 법인등록번호 | rrn | 200112-7448551 |
| 거래은행영업점 | 거래은행영업점 | 거래은행/영업점 | text | 신한은행 |
| employer.name2 | employer.name2 | 회사명 | text | 주식회사 태평양무역 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| customer.email | customer.email | e-mail | text | chanyeon363@naver.com |
| check.서비스종류 | check.서비스종류 | 서비스종류 | checkbox | 국내관계사 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| company.biz_no2 | company.biz_no2 | 사업자등록번호 | biz_no | 264-82-36559 |
| 글로벌고객번호 | 글로벌고객번호 | 글로벌고객번호 | text | 241786-1027388 |
| company.ceo2 | company.ceo2 | 대표자 | text | 박찬연 |
| Fax | Fax | Fax | text |  |
| check.조회서비스 | check.조회서비스 | 조회서비스(위임범위) | checkbox | 카드, |
| check.아이디 | check.아이디 | 아이디(ID) | checkbox | OTP |
| check.아이디2 | check.아이디2 | 아이디(ID) | checkbox | 실행자 |
| 목록[].실행자ID | 목록[].실행자ID | 실행자ID* | text | 3039-1859 |
| 목록[].통화 | 목록[].통화 | 통화 | text | USD |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 588-067325-57905 |
| 목록[].인감서명 | 목록[].인감서명 | 인감/서명 | text |  |
| check.기업뱅킹 | check.기업뱅킹 | 기업뱅킹(통합CMS) | checkbox | CMSiNet |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 한소태 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 장형준 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김찬하 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 임성빈 |
| seal.staff.지점장 | seal.staff.지점장 | 지점장 | seal | 검인 |
| sign.staff.지점장 | sign.staff.지점장 | 지점장 | signature | 이혜지 |
| check.주계약사 | check.주계약사 | 주계약사 | checkbox | 관계사ID에 대한 동의 |
| check.관계사 | check.관계사 | 관계사 | checkbox | 계좌 사용에 대한 동의 |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.relation | agent.relation | 관계 | text | 부 |
| employer.name3 | employer.name3 | 회사명 | text | 주식회사 태평양무역 |
| agent.birth | agent.birth | 생년월일 | date | 1962년 12월 19일 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.ceo3 | company.ceo3 | 대표자 | text | 박찬연 |
| check.본인은 | check.본인은 | 본인은 | checkbox | OTP를 수령하고 “전자금융거래에 필요한 접근매체(OTP, 인증서 암호, |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 관계사업무위임및관계사ID에대한동의 | 관계사업무위임및관계사ID에대한동의 | ■관계사업무위임및관계사ID에대한동의 | text |  |

### hf347 · 기업관계사 서비스 이용계약서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.347 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| employer.name | employer.name | 회사명 | text | 주식회사 태평양무역 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer.name | corp.ceo | 대표이사 | text | 박찬연 |
| seal.signer | seal.corp | 대표이사 | seal | 박찬연 |
| sign.signer | sign.customer | 대표이사 | signature | 이욱유 |
| employer.name2 | employer.name2 | 회사명 | text | 주식회사 태평양무역 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer2.name | signer2.name | 대표이사 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 대표이사 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 대표이사 | signature | 이욱유 |
| customer.address3 | customer.address3 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer3.name | signer3.name | 대표이사 | text | 박찬연 |
| seal.signer3 | seal.signer3 | 대표이사 | seal | 최우빈 |
| sign.signer3 | sign.signer3 | 대표이사 | signature | 박찬연 |

### hf348 · 기업관계사 서비스 이용신청서(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.348 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.ApplicationType | check.ApplicationType | ApplicationType | checkbox | Change |
| CorporateRegistrationNo | CorporateRegistrationNo | CorporateRegistrationNo. | text | 036236-1901329 |
| company.name | corp.name | CompanyName | text | (주)유니온무역 |
| customer.address | customer.address | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| CorporateRegistrationNo2 | CorporateRegistrationNo2 | CorporateRegistrationNo. | text | 711290-8831217 |
| BankBranch | BankBranch | Bank/Branch | text |  |
| company.name2 | company.name2 | CompanyName | text | (주)유니온무역 |
| customer.address2 | customer.address2 | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| PhoneNo | PhoneNo | PhoneNo. | phone | 010-5907-7253 |
| customer.email | customer.email | e-mail | text | chanyeon363@naver.com |
| check.LocationofAffiliate | check.LocationofAffiliate | LocationofAffiliate | checkbox | In Korea |
| BusinessRegistrationNo | BusinessRegistrationNo | BusinessRegistrationNo. | biz_no | 781-64-28453 |
| Representative | Representative | Representative | text |  |
| BusinessRegistrationNo2 | BusinessRegistrationNo2 | BusinessRegistrationNo. | biz_no | 264-82-36559 |
| GlobalClientNo | GlobalClientNo | GlobalClientNo. | rrn | 972-535505-96530 |
| Representative2 | Representative2 | Representative | text |  |
| Fax | Fax | Fax | text |  |
| check.Entire | check.Entire | Entire | checkbox | Specific |
| check.ID | check.ID | ID | checkbox | OTP |
| check.ID2 | check.ID2 | ID | checkbox | Executor |
| 목록[].ExecutorID | 목록[].ExecutorID | ExecutorID* | text | 8978-1713 |
| 목록[].Currency | 목록[].Currency | Currency | text | USD |
| 목록[].AccountNo | 목록[].AccountNo | AccountNo. | text | 912-503737-48563 |
| 목록[].RegisteredSealSign | 목록[].RegisteredSealSign | RegisteredSeal/Sign | text |  |
| check.CorporateBan | check.CorporateBan | CorporateBanking(IntegratedCMS) | checkbox | CMSiNet |
| check.PrincipalContractor | check.PrincipalContractor | PrincipalContractor | checkbox | Consent to the Affiliate’s Use of ID |
| check.Affiliate | check.Affiliate | Affiliate | checkbox | Consent to the Users under Control |
| customer.name | customer.name | Name | text | 박찬연 |
| customer.address3 | customer.address3 | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| Relationship | Relationship | Relationship | text |  |
| company.name3 | company.name3 | CompanyName | text | (주)유니온무역 |
| customer.birth | customer.birth | DateofBirth | date | 1990-02-10 |
| Delegator | Delegator | Delegator | text |  |
| Representative3 | Representative3 | Representative | text |  |

### hf349 · 펌뱅킹 출금전용계좌이용 동의서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.349 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.동의 | check.동의 | 동의 | checkbox | 동의 |
| date | date | 작성일 | date | 2026년 1월 31일 |

### hf350 · 아이부자 걷기챌린지 서비스 동의서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.350 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| 걸음정보 | 걸음정보 | 걸음정보(걸음수) | text |  |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인정보수집·이용에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 강순준 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 김순우 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 위우호 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 김순우 |

### hf352 · 하나 sERP 상담신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.352 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 사업장전화번호 | 사업장전화번호 | 사업장전화번호 | phone | 010-5907-7253 |
| company.address | corp.address | 사업장주소 | text | 서울특별시 중구 다산로 361, 6층 |
| company.ceo | corp.ceo | 대표자명 | text | 박찬연 |
| 담당자명 | 담당자명 | 담당자명 | text | 도숙경 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 이욱유 |

### hf353 · CMS Plus 이용신청서(지사)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.353 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.해외고객여부 | check.해외고객여부 | 해외고객여부 | checkbox | 아니오 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| 사업자명 | 사업자명 | 사업자명 | text | 미래물산 |
| 주소_목록[].대표자 | 주소_목록[].대표자 | 대표자 | text |  |
| check.대표연락처 | check.대표연락처 | 대표연락처(선택또는전부기재) | checkbox | 전화번호 |
| check.대표연락처2 | check.대표연락처2 | 대표연락처(선택또는전부기재) | checkbox | e-Mail |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| 거래은행영업점 | 거래은행영업점 | 거래은행/영업점 | text | 농협은행 |
| 고객번호 | 고객번호 | 고객번호 | text | 878060-4596178 |
| 목록[].통화 | 목록[].통화 | 통화 | text | CAD |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 434-166029-82392 |
| 목록[].예금주명 | 목록[].예금주명 | 예금주명 | text |  |
| 목록[].인감서명 | 목록[].인감서명 | 인감/서명 | text |  |
| 목록[].실행자아이디 | 목록[].실행자아이디 | 실행자아이디(ID) | text |  |
| 목록[].개설점 | 목록[].개설점 | 개설점 | text | 범어지점 |
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 해지 |
| check.전체예금외환수출입대출 | check.전체예금외환수출입대출 | 전체(예금,외환,수출입,대출,전자결제,카드,지로/공과금등 | checkbox | 전체 (예금, 외환, 수출입, 대출, 전자결제, 카드, 지로/공과금 등  |
| check.부분 | check.부분 | 부분( | checkbox | 수출입, |
| check.신청일현재및미래에보유한 | check.신청일현재및미래에보유한 | 신청일현재및미래에보유한모든계좌에대하여조회허용 | checkbox | 신청일 현재 및 미래에 보유한 모든 계좌에 대하여 조회 허용 |
| check.아래에서지정한계좌에대해 | check.아래에서지정한계좌에대해 | 아래에서지정한계좌에대해서만조회허용 | checkbox | 아래에서 지정한 계좌에 대해서만 조회 허용 |
| check.구분 | check.구분 | 구분 | checkbox | 실행자 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| 개별1회 | 개별1회 | 개별1회 | text |  |
| 개별1일 | 개별1일 | 개별1일 | date | 2025.08.21 |
| 대량1회 | 대량1회 | 대량1회 | text |  |
| 대량1일 | 대량1일 | 대량1일 | date | 2025년 10월 28일 |
| 보안카드No | 보안카드No | 보안(OTP)카드No | text | 5477-5445 |
| check.실행자 | check.실행자 | 실행자 | checkbox | 실행자 |
| 목록[].value | 목록[].value | (영문+숫자혼합6~10자리) | amount |  |
| 이체한도_목록[].value | 이체한도_목록[].value | (영문+숫자혼합6~10자리) | amount |  |
| 목록[].지사의실행자아이디 | 목록[].지사의실행자아이디 | 지사의실행자아이디(ID) | text |  |
| 목록[].통장인감 | 목록[].통장인감 | 통장인감 | text |  |
| 등록일자 | 등록일자 | 등록일자 | date | 2026년 1월 12일 |
| agent.name | agent.name | 성명 | text | 박영준 |
| 주소_목록[].생년월일 | 주소_목록[].생년월일 | 생년월일 | date | 2025.10.03 |
| agent.relation | agent.relation | 관계 | text | 부 |
| 주소_목록[].대표이사 | 주소_목록[].대표이사 | 대표이사 | text |  |
| agent.birth | agent.birth | 생년월일 | date | 1962.12.19 |
| date | date | 작성일 | date | 2026년 1월 31일 |

### hf354 · CMS Plus 이용계약서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.354 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 기타 | 기타 | 기타 | text | 해당 없음 |
| 설치장소 | 설치장소 | 설치장소 | text |  |
| Server | Server | Server | text |  |
| PC | PC | PC | text |  |
| 모니터 | 모니터 | 모니터 | text |  |
| 목록[].명세 | 목록[].명세 | 명세 | text |  |
| HW_목록[].수량 | HW_목록[].수량 | 수량 | number | 24 |
| 목록[].수량 | 목록[].수량 | 수량 | number | 3 |
| 키보드마우스포함 | 키보드마우스포함 | 키보드,마우스포함 | text |  |
| 목록[].키보드마우스포함 | 목록[].키보드마우스포함 | 키보드,마우스포함 | text |  |
| customer.name | customer.name | ,예금주 | text | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | corp.ceo | 대표이사 | text | 박찬연 |
| seal.signer | seal.corp | 대표이사 | seal | 강순준 |
| sign.signer | sign.customer | 대표이사 | signature | 이민빈 |
| seal.signer2 | seal.signer2 | 지점장 | seal | 이나정 |
| sign.signer2 | sign.signer2 | 지점장 | signature | 김유아 |
| employer.name | employer.name | 회사명 | text | 주식회사 태평양무역 |

### hf355 · CMS Mega 이용계약서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.355 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 예금주 | text | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | corp.ceo | 대표이사 | text | 박찬연 |
| seal.signer | seal.corp | 대표이사 | seal | 박찬연 |
| sign.signer | sign.customer | 대표이사 | signature | 현예지 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| seal.signer2 | seal.signer2 | 지점장 | seal | 김영원 |
| sign.signer2 | sign.signer2 | 지점장 | signature | 함은윤 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |

### hf356 · CMS Plus 이용신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.356 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| employer.name | employer.name | 회사명(대표자) | text | 주식회사 태평양무역 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| 주소_목록[].사업자등록번호 | 주소_목록[].사업자등록번호 | 사업자등록번호 | biz_no | 264-82-36559 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| check.이용Model | check.이용Model | 이용Model | checkbox | 인터넷 |
| 맞춤서비스_목록[].value | 맞춤서비스_목록[].value | (맞춤기능또는시스템연계내용) | amount |  |
| check.전용선 | check.전용선 | 전용선(VAN) | checkbox | 전용선(VAN) |
| check.인터넷전용선 | check.인터넷전용선 | 인터넷+전용선(VAN) | checkbox | 인터넷+전용선(VAN) |
| check.인터넷 | check.인터넷 | 인터넷 | checkbox | 인터넷 |
| check.전용선2 | check.전용선2 | 전용선(VAN) | checkbox | 전용선(VAN) |
| check.인터넷전용선2 | check.인터넷전용선2 | 인터넷+전용선(VAN) | checkbox | 인터넷+전용선(VAN) |
| check[] | check[] | ₩300,000(매월) | checkbox | ₩300,000 (매월) |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| customer.name | customer.name | 예금주 | text | 박찬연 |
| seal.signer | seal.customer | 거래인감(서명) | seal | 박찬연 |
| sign.signer | sign.customer | 거래인감(서명) | signature | 현예지 |
| 관리점 | 관리점 | 관리점 | text |  |
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 신규 |
| check.구분 | check.구분 | 구분 | checkbox | 총괄관리자 |
| customer.name2 | customer.name2 | 성명 | text | 박찬연 |
| 부서직위 | 부서직위 | 부서/직위 | text |  |
| customer.phone2 | customer.phone2 | 연락처 | phone | 010-5907-7253 |
| 개별1회 | 개별1회 | 개별1회 | text |  |
| 개별1일 | 개별1일 | 개별1일 | date | 2025.01.06 |
| 대량1회 | 대량1회 | 대량1회 | text |  |
| 대량1일 | 대량1일 | 대량1일 | date | 2025.11.10 |
| 보안카드No | 보안카드No | 보안(OTP)카드No | text | 016-000399-57855 |
| check.일반이용자 | check.일반이용자 | 일반이용자 | checkbox | 실행자 |
| 목록[].value | 목록[].value | (영문+숫자혼합6~10자리) | amount |  |
| 이체한도_목록[].value | 이체한도_목록[].value | (영문+숫자혼합6~10자리) | amount |  |
| check.일반이용자2 | check.일반이용자2 | 일반이용자 | checkbox | 일반이용자 |
| check.일반이용자3 | check.일반이용자3 | 일반이용자 | checkbox | 일반이용자 |
| 총괄관리자용 | 총괄관리자용 | 총괄관리자용 | text |  |
| 일반이용자용 | 일반이용자용 | 일반이용자용 | text |  |
| 목록[].일련번호 | 목록[].일련번호 | 일련번호(은행영업점직원이기입) | text | 075-336134-80286 |
| 목록[].실행자아이디 | 목록[].실행자아이디 | 실행자아이디(ID) | text |  |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 265-437394-56041 |
| 목록[].통장인감 | 목록[].통장인감 | 통장인감 | text |  |
| 목록[].개설점 | 목록[].개설점 | 개설점 | text | 범어지점 |
| check.입금계좌 | check.입금계좌 | 입금계좌( | checkbox | 지정 |
| 목록[].은행 | 목록[].은행 | 은행 | text | 하나은행 |
| 목록[].예금주 | 목록[].예금주 | 예금주 | text |  |
| 등록일자 | 등록일자 | 등록일자 | date | 2025년 4월 14일 |
| agent.name | agent.name | 성명 | text | 박영준 |
| 주소_목록[].생년월일 | 주소_목록[].생년월일 | 생년월일 | date | 2025.02.25 |
| agent.relation | agent.relation | 관계 | text | 부 |
| 주소_목록[].대표이사 | 주소_목록[].대표이사 | 대표이사 | text |  |
| agent.birth | agent.birth | 생년월일 | date | 1962.12.19 |
| date | date | 작성일 | date | 2026년 1월 31일 |

### hf357 · CMSiNet 지사정보 등록신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.357 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| check.하나해외지점법인주1고객 | check.하나해외지점법인주1고객 | 하나해외지점/법인주1)고객 | checkbox | 예 (아래내용 필수기입) |
| 사업자명 | 사업자명 | 사업자명 | text | 새한물산 |
| 사업자대표 | 사업자대표 | 사업자대표 | text |  |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| 팩스번호 | 팩스번호 | 팩스번호 | phone | 043-783-2775 |
| customer.email | customer.email | e-mail | text | chanyeon363@naver.com |
| 목록[].실행자ID | 목록[].실행자ID | 실행자ID | text | 8974-1584 |
| 목록[].통화 | 목록[].통화 | 통화 | text | EUR |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 622-300852-84304 |
| 목록[].예금주명 | 목록[].예금주명 | 예금주명 | text |  |
| 목록[].인감서명 | 목록[].인감서명 | 인감/서명 | text |  |
| 목록[].개설점 | 목록[].개설점 | 개설점 | text | 범어지점 |
| check.아래의사업장을CMSiN | check.아래의사업장을CMSiN | 아래의사업장을CMSiNet지사로등록하여주시기바랍니다. | checkbox | 아래의 사업장을 CMS iNet 지사로 등록하여 주시기 바랍니다. |
| check.지사출금계좌 | check.지사출금계좌 | 지사출금계좌 | checkbox | 지사 출금계좌 |

### hf358 · CMS Global 이용신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.358 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.biz_no | corp.biz_no | 사업자등록번호* | biz_no | 264-82-36559 |
| employer.name | employer.name | 회사명(대표자)* | text | 주식회사 태평양무역 |
| customer.address | customer.address | 주소* | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.address2 | customer.address2 | 주소* | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| email주소 | email주소 | e-mail주소* | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| customer.name | customer.name | 예금주 | text | 박찬연 |
| seal.signer | seal.customer | 거래인감 | seal | 이민빈 |
| sign.signer | sign.customer | 거래인감 | signature | 강순준 |
| 口KRW100000 | 口KRW100000 | 口KRW100,000(한국외국가1개)- | text |  |
| 口초과1개국가당KRW50000 | 口초과1개국가당KRW50000 | 口초과1개국가당KRW50,000- | text | 일본 |
| 이용수수료1_목록[].조회집금서비스2신청국가 | 이용수수료1_목록[].조회집금서비스2신청국가 | 조회+집금서비스2)신청국가 | text | 중국 |
| ID | ID | ID* | text | 8044-4543 |
| customer.name2 | customer.name2 | 성명 | text | 박찬연 |
| employer.position | employer.position | 직위 | text | 대리 |
| employer.department | employer.department | 부서 | text | 구매팀 |
| customer.phone | customer.phone | 휴대폰 | phone | 010-5907-7253 |
| 직통전화 | 직통전화 | 직통전화* | phone | 010-5907-7253 |
| email주소2 | email주소2 | e-mail주소* | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.name3 | customer.name3 | 신청인 | text | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 확인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 정소준 |
| seal.staff.팀장 | seal.staff.팀장 | 팀장 | seal | 천준희 |
| sign.staff.팀장 | sign.staff.팀장 | 팀장 | signature | 안호주 |
| seal.staff.부서장 | seal.staff.부서장 | 부서장 | seal | 검인 |
| sign.staff.부서장 | sign.staff.부서장 | 부서장 | signature | 김경지 |

### hf359 · 하나 sERP 이용신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.359 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 신고 |
| 기업인터넷뱅킹ID | 기업인터넷뱅킹ID | 기업인터넷뱅킹ID | text | 4567-6991 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| company.ceo | corp.ceo | 대표자명 | text | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 담당자명 | 담당자명 | 담당자명 | text | 박찬연 |
| 담당부서연락처 | 담당부서연락처 | 담당부서연락처 | phone | 010-5907-7253 |
| employer.name | employer.name | 회사명 | text | 주식회사 태평양무역 |
| 업태종목 | 업태종목 | 업태/종목 | text |  |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| 담당부서 | 담당부서 | 담당부서 | text |  |
| 세금계산서교부용eMail | 세금계산서교부용eMail | 세금계산서교부용e-Mail | text |  |
| account | account | 출금계좌(하나은행) | account_no | 000-287736-52424 |
| customer.name | customer.name | 예금주 | text | 박찬연 |
| seal.signer | seal.signer | 본인및인감확인 | seal | 현예지 |
| sign.signer | sign.signer | 본인및인감확인 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.name2 | customer.name2 | 성명 | text | 박찬연 |
| 기타필요서류 | 기타필요서류 | 기타필요서류 | text | 해당 없음 |

### hf360 · 개인(신용)정보 및 금융거래정보 제3자 제공동의서(모임통장서비스용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.360 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 일반개인정보 | 일반개인정보 | └일반개인정보 | text |  |
| check.위금융거래정보제공에동의하십니까 | check.위금융거래정보제공에동의하십니까 | 위금융거래정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |

### hf362 · 자동화기기 이용(신규,해지,변경)신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.362 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| 이용계좌번호 | 이용계좌번호 | 이용계좌번호 | text | 467-770658-47293 |
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 이민빈 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| signer2.name | agent.name | 대리인 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인 | seal | 박영준 |
| sign.signer2 | sign.agent | 대리인 | signature | 강석호 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 민혜성 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 검인 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 길태우 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김민연 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 최주윤 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 금소아 |
| customer.name2 | customer.name2 | 성명 | text | 박찬연 |
| 이용계좌번호2 | 이용계좌번호2 | 이용계좌번호 | text | 625-529396-79762 |
| customer.birth2 | customer.birth2 | 생년월일 | date | 1990.02.10 |
| customer.phone2 | customer.phone2 | 전화번호 | phone | 010-5907-7253 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer3.name | signer3.name | 신청인 | text | 박찬연 |
| seal.signer3 | seal.signer3 | 신청인 | seal | 박찬연 |
| sign.signer3 | sign.signer3 | 신청인 | signature | 강순준 |
| signer4.name | signer4.name | 대리인 | text | 박영준 |
| seal.signer4 | seal.signer4 | 대리인 | seal | 박영준 |
| sign.signer4 | sign.signer4 | 대리인 | signature | 김순우 |

### hf363 · 개인(신용)정보 수집이용 동의서[은행공동인증서비스(BankSign)]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.363 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].수집이용목적 | 목록[].수집이용목적 | 수집·이용목적 | text | 의료비 |
| 보유및이용기간 | 보유및이용기간 | 보유및이용기간 | text |  |
| 목록[].고유식별정보 | 목록[].고유식별정보 | 고유식별정보 | text |  |
| 목록[].개인정보 | 목록[].개인정보 | 개인(신용)정보 | text |  |
| 목록[].일반개인정보 | 목록[].일반개인정보 | 일반개인정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | signer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 이욱유 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 일 | text | 나우준 |
| seal.signer2 | seal.signer2 | 일 | seal | 나우준 |
| sign.signer2 | sign.signer2 | 일 | signature | 마민재 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| 위한인증처리 | 위한인증처리 | 위한인증처리 | text |  |
| 불이익 | 불이익 | 불이익 | text |  |

### hf364 · 개인(신용)정보 제3자 제공 동의서[은행공동인증서비스(BankSign)]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.364 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].제공받는자 | 목록[].제공받는자 | 제공받는자 | text |  |
| 목록[].이용목적 | 목록[].이용목적 | 이용목적 | text | 타행 이체 |
| 보유및이용기간 | 보유및이용기간 | 보유및이용기간 | text |  |
| 고유식별정보 | 고유식별정보 | 고유식별정보 | text |  |
| 일반개인정보 | 일반개인정보 | 일반개인정보 | text |  |
| 개인정보 | 개인정보 | 개인(신용)정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인신용정보제공에동의하십니까 | check.위개인신용정보제공에동의하십니까 | 위개인신용정보제공에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 이민빈 |
| sign.signer | sign.customer | 본인성명 | signature | 현예지 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 장민인 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 박영준 |
| 불이익 | 불이익 | 불이익 | text |  |

### hf365 · Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.365 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| PostalCode | PostalCode | PostalCode* | text |  |
| customer.address | customer.address | Address* | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| CorporateIdentificationNo | CorporateIdentificationNo | CorporateIdentificationNo.* | text | 380462-0324203 |
| BusinessRegistrationNo | BusinessRegistrationNo | BusinessRegistrationNo.* | biz_no | 279-13-57642 |
| value | value | (Korean)* | amount |  |
| value2 | value2 | (English)* | amount |  |
| PostalCode2 | PostalCode2 | PostalCode* | text |  |
| customer.address2 | customer.address2 | Address* | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| PhoneNo | PhoneNo | PhoneNo.* | phone | 010-5907-7253 |
| FaxNo | FaxNo | FaxNo.* | text | 671-587902-20584 |
| 목록[].Currency | 목록[].Currency | Currency | text | USD |
| 목록[].AccountNo | 목록[].AccountNo | AccountNo.(AccountType) | text | 7629-3137 |
| 목록[].AccountHolderName | 목록[].AccountHolderName | AccountHolderName | text |  |
| 목록[].SealSignature | 목록[].SealSignature | Seal/Signature | text |  |
| check.Iherebywishto | check.Iherebywishto | Iherebywishto | checkbox | Change/Add |
| Representative | Representative | Representative* | text |  |
| customer.name | customer.name | Name* | text | 박찬연 |
| customer.address3 | customer.address3 | Address* | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.address4 | customer.address4 | Address* | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| ResidentRegistrationNo | ResidentRegistrationNo | ResidentRegistrationNo. | text | 649143-4752511 |
| Relation | Relation | Relation(Dept./Position) | text |  |
| SignatureSeal | SignatureSeal | Signature/Seal* | text |  |
| SignatureSeal2 | SignatureSeal2 | Signature/Seal | text |  |
| BankVerifiersNameSignature | BankVerifiersNameSignature | BankVerifier’sName/Signature* | text |  |
| DateSubmitted | DateSubmitted | DateSubmitted* | date | 2025.07.06 |
| DateRegistered | DateRegistered | DateRegistered* | date | 2025.08.08 |
| customer.address5 | customer.address5 | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| PROXY | PROXY | PROXY | text |  |
| date | date | Date | date | 2026.01.31 |

### hf366 · Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(국문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.366 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호* | corp_reg_no | 200112-7448551 |
| customer.zipcode | customer.zipcode | 우편번호* | number | 06931 |
| customer.address | customer.address | 주소* | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.corp_no2 | company.corp_no2 | 법인등록번호* | rrn | 200112-7448551 |
| company.biz_no | corp.biz_no | 사업자등록번호* | biz_no | 264-82-36559 |
| value | value | (국문)* | amount |  |
| value2 | value2 | (영문)* | amount |  |
| 교육기관대표자 | 교육기관대표자 | 교육기관대표자* | text |  |
| customer.zipcode2 | customer.zipcode2 | 우편번호* | number | 06931 |
| customer.address2 | customer.address2 | 주소* | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone | customer.phone | 전화번호* | phone | 010-5907-7253 |
| 팩스번호 | 팩스번호 | 팩스번호* | phone | 043-783-2775 |
| 목록[].통화 | 목록[].통화 | 통화 | text | JPY |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호(계좌종류) | text | 398-065616-09467 |
| 목록[].예금주명 | 목록[].예금주명 | 예금주명 | text |  |
| 목록[].인감서명 | 목록[].인감서명 | 인감/서명 | text |  |
| check.다음과같이 | check.다음과같이 | 다음과같이 | checkbox | 신규 |
| seal.signer | seal.customer | 서명/인감* | seal | 박찬연 |
| sign.signer | sign.customer | 서명/인감* | signature | 현예지 |
| customer.name | customer.name | 성명* | text | 박찬연 |
| customer.address3 | customer.address3 | 주소* | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.name | agent.name | 성명* | text | 박영준 |
| agent.address | agent.address | 주소* | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.address2 | agent.address2 | 주소* | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.rrn | agent.rrn | 주민등록번호 | rrn | 621219-1****** |
| agent.relation | agent.relation | 관계(부서/직위)* | text | 부 |
| seal.signer2 | seal.signer2 | 서명/인감* | seal | 이욱유 |
| sign.signer2 | sign.signer2 | 서명/인감* | signature | 박찬연 |
| seal.signer3 | seal.signer3 | 서명/인감 | seal | 이욱유 |
| sign.signer3 | sign.signer3 | 서명/인감 | signature | 박찬연 |
| seal.signer4 | seal.signer4 | 담당자성명/서명* | seal | 강순준 |
| sign.signer4 | sign.signer4 | 담당자성명/서명* | signature | 박찬연 |
| 접수일자 | 접수일자 | 접수일자* | date | 2025.08.13 |
| 등록일자 | 등록일자 | 등록일자* | date | 2025.01.10 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 고객교육기관명 | 고객교육기관명 | “고객”교육기관명 | text | 우리은행 |
| customer.address4 | customer.address4 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |

### hf367 · Hana 1Q bank CMS iNet 서비스 이용 추가 계약서(iSBS)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.367 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 교육기관명 | 교육기관명 | 교육기관명 | text | 국민은행 |
| signer.name | corp.ceo | 대표자(학교장) | text | 박찬연 |
| seal.signer | seal.corp | 대표자(학교장) | seal | 현예지 |
| sign.signer | sign.customer | 대표자(학교장) | signature | 강순준 |
| signer2.name | signer2.name | 지점장 | text | 최경혜 |
| seal.signer2 | seal.signer2 | 지점장 | seal | 방우도 |
| sign.signer2 | sign.signer2 | 지점장 | signature | 최경혜 |
| 고객 | 고객 | “고객” | text |  |

### hf368 · 가상계좌서비스 이용계약서(외화)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.368 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 입금모계좌 | 입금모계좌 | 입금모계좌 | text | 427-854155-59099 |
| 수수료인출계좌 | 수수료인출계좌 | 수수료인출계좌 | number | 2,610,000 |
| 외화 | 외화 | 외화 | amount | USD 94,700 |
| 원화 | 원화 | 원화 | text |  |
| 목록[].예금주 | 목록[].예금주 | 예금주 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | corp.ceo | 대표이사 | text | 박찬연 |
| seal.signer | seal.corp | 대표이사 | seal | 박찬연 |
| sign.signer | sign.customer | 대표이사 | signature | 이욱유 |
| 만원이상 | 만원이상 | 만원이상 | number | 395 |
| check.정산일 | check.정산일 | 정산일 | checkbox | 입금당일정산 |
| check.정산방식 | check.정산방식 | 정산방식 | checkbox | 실시간 입금 |
| 영업일기준 | 영업일기준 | 영업일기준 | text |  |
| check.예금주명표기방식 | check.예금주명표기방식 | 예금주명표기방식 | checkbox | 예금주명만 표기 |
| check.가상계좌재사용여부 | check.가상계좌재사용여부 | 가상계좌재사용여부 | checkbox | 재사용 |
| check.가상계좌별입금횟수제한 | check.가상계좌별입금횟수제한 | 가상계좌별입금횟수제한 | checkbox | 매월 |
| 사유 | 사유 | 사유 | text | 학자금 |
| 부기명표기사유및부기명내용 | 부기명표기사유및부기명내용 | 부기명표기사유및부기명내용 | text | 해당 없음 |
| 가상계좌개설후최초입금시1회징구 | 가상계좌개설후최초입금시1회징구 | 가상계좌개설후최초입금시1회징구 | text | 203-464182-55808 |
| 가상계좌로입금거래발생시매회징구 | 가상계좌로입금거래발생시매회징구 | 가상계좌로입금거래발생시매회징구 | text | 411-024069-89447 |
| 신청좌수 | 신청좌수 | 신청좌수 | text |  |
| 동일가상계좌에입금가능한횟수를의미함 | 동일가상계좌에입금가능한횟수를의미함 | 동일가상계좌에입금가능한횟수를의미함 | text | 231-121052-84569 |

### hf369 · 가상계좌서비스 이용계약서(원화)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.369 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 입금모계좌 | 입금모계좌 | 입금모계좌 | text | 422-285308-58130 |
| 수수료인출계좌 | 수수료인출계좌 | 수수료인출계좌 | number | 6,750,000 |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 538-483819-71934 |
| 목록[].예금주 | 목록[].예금주 | 예금주 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | corp.ceo | 대표이사 | text | 박찬연 |
| seal.signer | seal.corp | 대표이사 | seal | 박찬연 |
| sign.signer | sign.customer | 대표이사 | signature | 강순준 |
| 만원이상 | 만원이상 | 만원이상 | number | 754 |
| check.정산일 | check.정산일 | 정산일 | checkbox | 입금후 |
| check.정산방식 | check.정산방식 | 정산방식 | checkbox | 실시간 입금 |
| 영업일기준 | 영업일기준 | 영업일기준 | text |  |
| check.예금주명표기방식 | check.예금주명표기방식 | 예금주명표기방식 | checkbox | 예금주명만 표기 |
| check.가상계좌재사용여부 | check.가상계좌재사용여부 | 가상계좌재사용여부 | checkbox | 재사용 |
| check.가상계좌별입금횟수제한 | check.가상계좌별입금횟수제한 | 가상계좌별입금횟수제한 | checkbox | 제한없음 |
| 사유 | 사유 | 사유 | text | 주택구입 |
| 부기명표기사유및부기명내용 | 부기명표기사유및부기명내용 | 부기명표기사유및부기명내용 | text | 해당 없음 |
| 가상계좌개설후최초입금시1회징구 | 가상계좌개설후최초입금시1회징구 | 가상계좌개설후최초입금시1회징구 | text | 616-528850-77559 |
| 가상계좌로입금거래발생시매회징구 | 가상계좌로입금거래발생시매회징구 | 가상계좌로입금거래발생시매회징구 | text | 075-607353-35231 |
| 신청좌수 | 신청좌수 | 신청좌수 | text |  |
| 동일가상계좌에입금가능한횟수를의미함 | 동일가상계좌에입금가능한횟수를의미함 | 동일가상계좌에입금가능한횟수를의미함 | text | 053-632225-75151 |

### hf372 · 전산기기 임대차계약서(Hana 1Q bank CMS)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.372 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 기타 | 기타 | 기타 | text | 해당 없음 |
| 설치장소 | 설치장소 | 설치장소 | text |  |
| Server | Server | Server | text |  |
| PC | PC | PC | text |  |
| 모니터 | 모니터 | 모니터 | text |  |
| 목록[].명세 | 목록[].명세 | 명세 | text |  |
| HW_목록[].수량 | HW_목록[].수량 | 수량 | number | 1 |
| 목록[].수량 | 목록[].수량 | 수량 | number | 3 |
| 키보드마우스포함 | 키보드마우스포함 | 키보드,마우스포함 | text |  |
| 목록[].키보드마우스포함 | 목록[].키보드마우스포함 | 키보드,마우스포함 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.address | customer.address | (고객)주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer.name | corp.ceo | 대표이사 | text | 박찬연 |
| seal.signer | seal.corp | 대표이사 | seal | 박찬연 |
| sign.signer | sign.customer | 대표이사 | signature | 강순준 |
| customer.address2 | customer.address2 | (은행)주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| seal.signer2 | seal.signer2 | 지점장 | seal | 김동도 |
| sign.signer2 | sign.signer2 | 지점장 | signature | 진욱린 |

### hf373 · 전자어음 교부 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.373 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 법인명(성명) | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자등록번호(법인) | biz_no | 264-82-36559 |
| 당좌계좌번호 | 당좌계좌번호 | 당좌계좌번호 | text | 103-580117-45846 |
| 교부신청매수 | 교부신청매수 | 교부신청매수 | number | 1 |
| company.ceo | corp.ceo | 대표자명 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일(개인/개인사업자) | date | 1990-02-10 |
| 회수신청매수 | 회수신청매수 | 회수신청매수 | number | 2 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 강순준 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 마용도 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김준은 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 윤영서 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 정승지 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 이정민 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 김숙아 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 장옥경 |

### hf374 · 전자어음 이용(변경,해지) 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.374 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.거래구분 | check.거래구분 | 거래구분 | checkbox | 신규가입 |
| check.회원구분 | check.회원구분 | 회원구분 | checkbox | 발행인(수취,배서포함) |
| company.name | corp.name | 법인명(성명) | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자등록번호(법인) | biz_no | 264-82-36559 |
| check.규모 | check.규모 | 규모 | checkbox | 중소기업 |
| 담당부서 | 담당부서 | 담당부서 | text |  |
| employer.phone | employer.phone | 회사전화 | phone | 043-783-2775 |
| FAX | FAX | FAX | phone | 043-783-2775 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| 대표전화 | 대표전화 | 대표전화 | phone | 010-5907-7253 |
| customer.phone | customer.phone | 휴대폰 | phone | 010-5907-7253 |
| customer.email | customer.email | E-Mail | text | chanyeon363@naver.com |
| 발행지정계좌 | 발행지정계좌 | 발행(당좌)지정계좌 | text | 031-656767-48641 |
| 수취지정계좌 | 수취지정계좌 | 수취(요구불)지정계좌 | text | 095-020779-84508 |
| seal.signer | seal.customer | 거래인감 | seal | 박찬연 |
| sign.signer | sign.customer | 거래인감 | signature | 위나아 |
| seal.signer2 | seal.signer2 | 거래인감 | seal | 강순준 |
| sign.signer2 | sign.signer2 | 거래인감 | signature | 이주원 |
| value | value | [변경전] | amount |  |
| 변경항목 | 변경항목 | 변경항목 | text |  |
| value2 | value2 | [변경후] | amount |  |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer3.name | agent.name | 신청인(대리인) | text | 이도민 |
| seal.signer3 | seal.agent | 신청인(대리인) | seal | 이도민 |
| sign.signer3 | sign.agent | 신청인(대리인) | signature | 김순우 |
| 징구서류 | 징구서류 | •징구서류 | text |  |
| 자택 | 자택 | 자택()- | text |  |
| 휴대폰 | 휴대폰 | 휴대폰()- | phone | 010-5907-7253 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 조환원 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 심지아 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김준재 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 정지재 |

### hf375 · 자금관리서비스 이용계약서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.375 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.phone | customer.phone | 휴대폰 | phone | 010-5907-7253 |
| 직위성명 | 직위성명 | 직위/성명 | text | 박찬연 |
| employer.address | employer.address | 회사주소 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태평양무역 구매팀 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | corp.ceo | 대표이사 | text | 박찬연 |
| seal.signer | seal.corp | 대표이사 | seal | 강순준 |
| sign.signer | sign.customer | 대표이사 | signature | 박찬연 |
| seal.signer2 | seal.signer2 | 지점장 | seal | 김혁율 |
| sign.signer2 | sign.signer2 | 지점장 | signature | 김도재 |

### hf376 · 위임장(해외체류자 전자금융용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.376 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.birth | agent.birth | 생년월일 | date | 1962.12.19 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 명: | text | 박찬연 |
| seal.signer | seal.customer | 명: | seal | 최우빈 |
| sign.signer | sign.customer | 명: | signature | 이욱유 |
| 해외영업점 | 해외영업점 | 해외영업점 | text | 범어지점 |
| signer2.name | signer2.name | 확인자 | text | 장혁성 |
| seal.signer2 | seal.signer2 | 확인자 | seal | 황지승 |
| sign.signer2 | sign.signer2 | 확인자 | signature | 김재주 |
| 비밀번호재등록 | 비밀번호재등록 | 비밀번호재등록 | text | 129-909377-72328 |
| 보안매체재발급 | 보안매체재발급 | 보안매체재발급(OTP/자물쇠카드) | text |  |
| employer.position | employer.position | 직위 | text | 대리 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 조순원 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 강욱혜 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김예인 |

### hf377 · 해외영업점 계좌개설 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.377 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 담당Prepare | 담당Prepare | 담당Prepare | text |  |
| 책임자Approval | 책임자Approval | 책임자Approval | text |  |
| 성명Name | 성명Name | 성명Name | text | 이성유 |
| 성명Name2 | 성명Name2 | 성명Name | text | 제갈상승 |
| customer.birth | customer.birth | 생년월일DateofBirth | date | 1990.02.10 |
| 여권번호PassportNo | 여권번호PassportNo | 여권번호PassportNo. | text | M49146990 |
| 국내주소DomesticAddress_목록[].여권유효기일DateofExpiry | 국내주소DomesticAddress_목록[].여권유효기일DateofExpiry | 여권유효기일DateofExpiry | date | 2029.07.27 |
| 국내주소DomesticAddress | 국내주소DomesticAddress | 국내주소DomesticAddress | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 해외주소OverseasAddress_목록[].여권유효기일DateofExpiry | 해외주소OverseasAddress_목록[].여권유효기일DateofExpiry | 여권유효기일DateofExpiry | date | 2028년 7월 27일 |
| 국적Nationality | 국적Nationality | 국적Nationality | text |  |
| 여권유효기일DateofExpiry | 여권유효기일DateofExpiry | 여권유효기일DateofExpiry | date | 2029년 8월 27일 |
| 개설신청은행지점명OpeningBankBranch | 개설신청은행지점명OpeningBankBranch | 개설신청은행/지점명OpeningBank/Branch | text | 카카오뱅크 |
| 개설통화Currency | 개설통화Currency | 개설통화Currency | text | JPY |
| 접수은행지점명BankBranch | 접수은행지점명BankBranch | 접수은행/지점명Bank/Branch | text | 국민은행 |
| customer.name | customer.name | 고객명(Name) | text | 박찬연 |
| 제출서류 | 제출서류 | 제출서류(Document) | text |  |
| account | account | 계좌번호(A/CNo.) | account_no | 000-287736-52424 |
| check.신청 | check.신청 | 신청(Application) | checkbox | 취소(Cancellation) |
| check.본인은위와같이예금계좌개 | check.본인은위와같이예금계좌개 | 본인은위와같이예금계좌개설/취소를신청합니다. | checkbox | 본인은 위와 같이 예금계좌 개설/취소를 신청합니다. |
| check.현지국의법규및규제사항거 | check.현지국의법규및규제사항거 | 현지국의법규및규제사항,거래약관에따라신청자앞예금계좌가개설되 | checkbox | 현지국의 법규 및 규제사항, 거래약관에 따라 신청자 앞 예금계좌가 개설되 |
| date | date | 신청일자(Date) | date | 2026년 01월 31일 |
| signer.name | signer.name | 담당자(직,성명) | text | 이석영 |
| seal.signer | seal.signer | 담당자(직,성명) | seal | 염지인 |
| sign.signer | sign.signer | 담당자(직,성명) | signature | 이석영 |
| seal.signer2 | seal.signer2 | 지점장 | seal | 이욱하 |
| sign.signer2 | sign.signer2 | 지점장 | signature | 김윤민 |
| signer3.name | signer3.name | 담당자(직,성명) | text | 현도수 |
| seal.signer3 | seal.signer3 | 담당자(직,성명) | seal | 이영승 |
| sign.signer3 | sign.signer3 | 담당자(직,성명) | signature | 장미민 |

### hf378 · 글로벌뱅킹서비스 이용,변경,해지 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.378 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 담당Prepare | 담당Prepare | 담당Prepare | text |  |
| 책임자Approval | 책임자Approval | 책임자Approval | text |  |
| 성명Name | 성명Name | 성명Name | text | 한유경 |
| 성명Name2 | 성명Name2 | 성명Name | text | 박채지 |
| customer.birth | customer.birth | 생년월일DateofBirth | date | 1990.02.10 |
| 해외주소OverseasAddress_목록[].직장Company | 해외주소OverseasAddress_목록[].직장Company | 직장Company | text |  |
| 자택House_목록[].여권번호PassportNo | 자택House_목록[].여권번호PassportNo | 여권번호PassportNo. | text | M46216934 |
| 직장Company_목록[].여권번호PassportNo | 직장Company_목록[].여권번호PassportNo | 여권번호PassportNo. | text | M20200989 |
| 여권번호PassportNo | 여권번호PassportNo | 여권번호PassportNo. | text | M99312521 |
| 인터넷뱅킹이용자IDInternetBankingUserID | 인터넷뱅킹이용자IDInternetBankingUserID | 인터넷뱅킹이용자IDInternetBankingUserID | text | 408233-4491370 |
| 서비스이용계좌번호ACNo | 서비스이용계좌번호ACNo | 서비스이용계좌번호A/CNo. | text | 024-796433-73165 |
| 개설은행지점명BankBranch | 개설은행지점명BankBranch | 개설은행/지점명Bank/Branch | text | 우리은행 |
| seal.signer | seal.customer | 서명/인감Signature | seal | 이민빈 |
| sign.signer | sign.customer | 서명/인감Signature | signature | 박찬연 |
| 직장Company | 직장Company | 직장Company | text |  |
| eMail | customer.email | e-Mail | text |  |
| signer2.name | signer2.name | 실명확인자 | text | 김원도 |
| seal.signer2 | seal.signer2 | 실명확인자 | seal | 김원도 |
| sign.signer2 | sign.signer2 | 실명확인자 | signature | 양승서 |
| 조회 | 조회 | ‌조회 | text |  |
| 조회2 | 조회2 | ‌조회 | text |  |
| 조회3 | 조회3 | ‌조회 | text |  |
| Inquiry | Inquiry | Inquiry | text |  |
| Inquiry2 | Inquiry2 | Inquiry | text |  |
| Inquiry3 | Inquiry3 | Inquiry | text |  |

### hf379 · 주류구매전용카드 가맹점가입신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.379 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| check.주소 | check.주소 | 주소 | checkbox | 보기1 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.name2 | customer.name2 | 예금주 | text | 박찬연 |
| company.established | corp.established | 개업일 | date | 2018.11.01 |
| 자본금 | 자본금 | 자본금 | text |  |
| company.biz_item | corp.biz_item | 업종 | text | 무역 |
| 매출액 | 매출액 | 매출액 | number | 75,280,000 |
| 취급품목 | 취급품목 | 취급품목 | text | 커피 원두 |
| 종업원수 | 종업원수 | 종업원수 | text |  |
| check.사업체구분 | check.사업체구분 | 사업체구분 | checkbox | 수입 |
| employer.name | employer.name | 소속 | text | 주식회사 태평양무역 |
| employer.name2 | employer.name2 | 소속 | text | 주식회사 태평양무역 |
| customer.name3 | customer.name3 | 성명 | text | 박찬연 |
| customer.name4 | customer.name4 | 성명 | text | 박찬연 |
| check.주류구매전용카드가맹점가입신청서 | check.주류구매전용카드가맹점가입신청서 | 주류구매전용카드가맹점가입신청서( | checkbox | (주)엔젤넷) |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인(상호) | text | (주)유니온무역 |
| seal.signer | seal.corp | 신청인(상호) | seal | (주)유니온무역 |
| sign.signer | sign.customer | 신청인(상호) | signature | 주식회사 대성패션 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 가맹점신청인 | text | 박찬연 |
| seal.signer2 | seal.customer | 가맹점신청인 | seal | 강순준 |
| sign.signer2 | sign.signer2 | 가맹점신청인 | signature | 박찬연 |
| seal.signer3 | seal.signer3 | 지점장 | seal | 강수빈 |
| sign.signer3 | sign.signer3 | 지점장 | signature | 심나태 |

### hf380 · 금융결제원CMS 이용계약서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.380 (전자금융) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 출금이체 | 출금이체 | 출금이체 | text |  |
| 입금이체 | 입금이체 | 입금이체 | text |  |
| 목록[].예금주명 | 목록[].예금주명 | 예금주명 | text |  |
| 원 | 원 | 원 | text |  |
| 이체건당 | 이체건당 | 이체건당 | text |  |
| 원2 | 원2 | 원 | text |  |
| 원3 | 원3 | 원 | text |  |
| 원4 | 원4 | 원 | text |  |
| 계약지점코드 | 계약지점코드 | 계약지점코드 | number | 23702 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| signer.name | signer.name | 지점장 | text | 김숙호 |
| seal.signer | seal.signer | 지점장 | seal | 조은예 |
| sign.signer | sign.signer | 지점장 | signature | 김숙호 |
| signer2.name | corp.ceo | 대표자 | text | 박찬연 |
| seal.signer2 | seal.corp | 대표자 | seal | 박찬연 |
| sign.signer2 | sign.customer | 대표자 | signature | 이욱유 |

### hf164 · 퇴직연금 퇴직급여 지급신청서(DC,기업형IRP)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.164 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| employer.hire_date | employer.hire_date | 입사일자 | date | 2020.05.08 |
| account | account | 퇴직연금계좌번호 | account_no | 000-287736-52424 |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| 중간정산일자 | 중간정산일자 | 중간정산일자 | date | 2026-01-17 |
| check.제도구분 | check.제도구분 | 제도구분 | checkbox | 기업형IRP |
| check.임원여부 | check.임원여부 | 임원여부 | checkbox | 근로자 |
| 퇴직급여입금총액 | 퇴직급여입금총액 | 퇴직급여입금총액* | number | 9,310,000원 |
| 퇴직일자 | 퇴직일자 | 퇴직일자 | date | 2025.10.19 |
| check.지급형태 | check.지급형태 | 지급형태 | checkbox | 개인형IRP(의무) |
| check.지급형태2 | check.지급형태2 | 지급형태 | checkbox | 입출금계좌 |
| check.잔여부담금 | check.잔여부담금 | 잔여부담금*** | checkbox | 없음 |
| check.잔여부담금2 | check.잔여부담금2 | 잔여부담금*** | checkbox | 있음 (금액 |
| check.기업반환신청 | check.기업반환신청 | 기업반환신청***** | checkbox | 국민연금 전환금 |
| check.현물이전 | check.현물이전 | 현물이전** | checkbox | 미신청 (보유상품 ‘해지 후’ IRP로 이전 (특별중도해지이율 적용)) |
| check.예외사유 | check.예외사유 | 예외사유 | checkbox | 만원이하 퇴직금 지급 |
| check.연동출금신청 | check.연동출금신청 | 연동출금신청(사전에약정된경우) | checkbox | 미신청(기업별도입금) |
| 예약지급일 | 예약지급일 | 예약지급일* | date | 2025.03.05 |
| check.당해연도이전에중간정산한금액이있는경우 | check.당해연도이전에중간정산한금액이있는경우 | 당해연도이전에중간정산(중도인출)한금액이있는경우 | checkbox | 해당사항 없음 |
| check.해당사항없음 | check.해당사항없음 | 해당사항없음 | checkbox | 해당사항 없음 |
| 금융기관명 | 금융기관명 | 금융기관명 | text | 우리은행 |
| 금융기관명2 | 금융기관명2 | 금융기관명 | text | 기업은행 |
| account2 | account2 | 계좌번호 | account_no | 000-287736-52424 |
| account3 | account3 | 계좌번호 | account_no | 000-287736-52424 |
| check.퇴직소득세계산을위한근속연수산정시제외가산월수있는경우기재 | check.퇴직소득세계산을위한근속연수산정시제외가산월수있는경우기재 | 퇴직소득세계산을위한근속연수산정시제외·가산월수있는경우기재 | checkbox | 제외월수( |
| check.개인적립금과세제외신청 | check.개인적립금과세제외신청 | 개인적립금과세제외신청 | checkbox | 과세제외 미신청 |
| check.가입자단독청구 | check.가입자단독청구 | 가입자단독청구 | checkbox | 기타 (사용자 지급거절 등) |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 가입자 | text | 박찬연 |
| seal.signer | seal.customer | 가입자 | seal | 현예지 |
| sign.signer | sign.customer | 가입자 | signature | 강순준 |
| signer2.name | signer2.name | 가입자 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 가입자 | seal | 강순준 |
| sign.signer2 | sign.signer2 | 가입자 | signature | 박찬연 |
| signer3.name | signer3.name | 기업명 | text | (주)유니온무역 |
| seal.signer3 | seal.corp | 기업명 | seal | (주)삼정전자 |
| sign.signer3 | sign.signer3 | 기업명 | signature | (주)유니온무역 |
| signer4.name | signer4.name | 가입자 | text | 박찬연 |
| seal.signer4 | seal.signer4 | 가입자 | seal | 강순준 |
| sign.signer4 | sign.signer4 | 가입자 | signature | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김우예 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김영서 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 허준주 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김선민 |
| 타금융기관IRP통장사본 | 타금융기관IRP통장사본 | 타금융기관IRP통장사본(가입확인서) | text | 우리은행 |
| 퇴직금전환금부과내역서 | 퇴직금전환금부과내역서 | 퇴직금전환금부과내역서(국민연금공단발급) | text |  |
| 연금보험료등소득세액공제확인서 | 연금보험료등소득세액공제확인서 | 연금보험료등소득☞세액공제확인서 | number | 70,000 |
| signer5.name | signer5.name | 가입자 | text | 박찬연 |
| seal.signer5 | seal.signer5 | 가입자 | seal | 강순준 |
| sign.signer5 | sign.signer5 | 가입자 | signature | 현예지 |
| signer6.name | signer6.name | 가입자 | text | 박찬연 |
| seal.signer6 | seal.signer6 | 가입자 | seal | 이민빈 |
| sign.signer6 | sign.signer6 | 가입자 | signature | 박찬연 |
| 아래양식중한가지 | 아래양식중한가지 | 아래양식중한가지 | text |  |

### hf165 · 퇴직연금 계약이전신청서(DB)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.165 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| 예약지급일 | 예약지급일 | 예약지급일 | date | 2025-11-13 |
| account | account | 퇴직연금계좌번호 | account_no | 000-287736-52424 |
| check.전부이전 | check.전부이전 | 전부이전 | checkbox | 전부이전 |
| 이전구분 | 이전구분 | 이전구분 | text |  |
| check.일부이전 | check.일부이전 | 일부이전 | checkbox | 일부이전 |
| check.금액이전 | check.금액이전 | 금액이전 | checkbox | 금액이전 |
| check.퇴직연금사업자변경 | check.퇴직연금사업자변경 | 퇴직연금사업자변경 | checkbox | 퇴직연금 사업자 변경 |
| check.계열사이전 | check.계열사이전 | 계열사이전(과거입사일인정) | checkbox | 계열사이전(과거입사일 인정) |
| 이전사유 | 이전사유 | 이전사유 | text | 해외 이민 예정 |
| check.퇴직연금사업자변경2 | check.퇴직연금사업자변경2 | 퇴직연금사업자변경 | checkbox | 분할/영업양수도 |
| check.퇴직연금사업자변경3 | check.퇴직연금사업자변경3 | 퇴직연금사업자변경 | checkbox | 퇴직연금 사업자 변경 |
| 이전받는금융기관 | 이전받는금융기관 | 이전받는금융기관 | text | 농협은행 |
| 자산관리기관 | 자산관리기관 | 자산관리기관 | text | 하나은행 |
| 이전방식 | 이전방식 | 이전방식 | text |  |
| 현물이전 | 현물이전 | 현물이전* | text |  |
| check.금액지정방식 | check.금액지정방식 | 금액지정방식 | checkbox | 상품지정방식(뒷장 필수 기재) |
| 금융기관명 | 금융기관명 | 금융기관명 | text | 카카오뱅크 |
| foreign.account | foreign.account | 계좌번호 | account_no | 884779361534 |
| foreign.name | foreign.name | 예금주 | text | Mekong Garment JSC |
| check.현물이전 | check.현물이전 | 현물이전* | checkbox | 신청(보유상품 ‘해지 없이’ 이전) |
| check.현물이전2 | check.현물이전2 | 현물이전* | checkbox | 미신청(보유상품 ‘해지 후’ 이전) |
| 목록[].가입자명 | 목록[].가입자명 | 가입자명* | text |  |
| 목록[].생년월일 | 목록[].생년월일 | 생년월일(주민번호) | text | 2026.01.03 |
| 목록[].제도전환전출일자 | 목록[].제도전환전출일자 | 제도전환/전출일자 | text | 2025.07.23 |
| signer.name | customer.name | 제도전환/전출일자 | text | 박찬연 |
| seal.signer | seal.customer | 제도전환/전출일자 | seal | 박찬연 |
| sign.signer | sign.customer | 제도전환/전출일자 | signature | 강순준 |
| 목록[].서명또는 | 목록[].서명또는 | 서명또는(인) | text |  |
| 목록[].지급요청금액 | 목록[].지급요청금액 | 지급요청금액 | text | 48,440,000 |
| 목록[].매도순위 | 목록[].매도순위 | 매도순위 | text |  |
| 목록[].상품명 | 목록[].상품명 | 상품명 | text | 이율보증형 보험(GIC) 1년 |
| 목록[].상품계좌번호 | 목록[].상품계좌번호 | 상품계좌번호 | text | 679-952971-59380 |
| 목록[].매도금액 | 목록[].매도금액 | 매도금액(원/좌) | text | 2,690,000 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 염호린 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 구윤우 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이우원 |
| 매도상품_목록[].상품명 | 매도상품_목록[].상품명 | 상품명 | text | 인덱스(KOSPI200) 증권자투자신탁 |
| 입금비율 | 입금비율 | 입금비율* | number | 100 |
| 금융기관명2 | 금융기관명2 | 금융기관명 | text | 신한은행 |
| foreign.account2 | foreign.account2 | 계좌번호 | account_no | 884779361534 |
| foreign.name2 | foreign.name2 | 예금주 | text | Mekong Garment JSC |
| 매도상품_목록[].상품계좌번호 | 매도상품_목록[].상품계좌번호 | 상품계좌번호 | text | 041-130567-10161 |
| 이전받는금융기관_목록[].상품계좌번호 | 이전받는금융기관_목록[].상품계좌번호 | 상품계좌번호 | text | 139-403266-70575 |
| 매도상품_목록[].만기일 | 매도상품_목록[].만기일 | 만기일 | text | 2027.06.20 |
| 이전받는금융기관_목록[].만기일 | 이전받는금융기관_목록[].만기일 | 만기일 | text | 2028년 8월 1일 |
| signer2.name | signer2.name | 기업명 | text | (주)유니온무역 |
| seal.signer2 | seal.corp | 기업명 | seal | (주)삼정전자 |
| sign.signer2 | sign.signer2 | 기업명 | signature | 주식회사 한빛패션 |
| signer3.name | signer3.name | 기업명 | text | (주)유니온무역 |
| seal.signer3 | seal.signer3 | 기업명 | seal | 주식회사 한빛패션 |
| sign.signer3 | sign.signer3 | 기업명 | signature | (주)유니온무역 |
| signer4.name | signer4.name | 신탁관리인 | text | 공환성 |
| seal.signer4 | seal.signer4 | 신탁관리인 | seal | 성미아 |
| sign.signer4 | sign.signer4 | 신탁관리인 | signature | 공환성 |
| value | value | [유의사항] | amount |  |

### hf166 · 퇴직연금 계약이전신청서(DC)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.166 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 서류확인및접수확인자 | 서류확인및접수확인자 | 서류확인및접수확인자 | text |  |
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| 예약지급일 | 예약지급일 | 예약지급일* | date | 2025년 8월 14일 |
| account | account | 퇴직연금계좌번호 | account_no | 000-287736-52424 |
| check.수수료연동출금 | check.수수료연동출금 | 수수료연동출금 | checkbox | 미동의(기업별도 입금) |
| check.퇴직연금사업자변경 | check.퇴직연금사업자변경 | 퇴직연금사업자변경 | checkbox | 퇴직연금 사업자 변경 |
| 이전받는금융기관 | 이전받는금융기관 | 이전받는금융기관 | text | 기업은행 |
| 자산관리기관 | 자산관리기관 | 자산관리기관 | text | 카카오뱅크 |
| check.일부이전 | check.일부이전 | 일부이전(현물이전은3번항목에서개별신청) | checkbox | 일부이전(현물이전은 3번 항목에서 개별 신청) |
| check.전부이전 | check.전부이전 | 전부이전 | checkbox | 전부이전 |
| 금융기관 | 금융기관 | 금융기관 | text | 우리은행 |
| foreign.account | foreign.account | 계좌번호 | account_no | 884779361534 |
| foreign.name | foreign.name | 예금주 | text | Mekong Garment JSC |
| check.현물이전 | check.현물이전 | 현물이전** | checkbox | 신청(보유상품 ‘해지 없이’ 이전) |
| check.현물이전2 | check.현물이전2 | 현물이전** | checkbox | 미신청(보유상품 ‘해지 후’ 이전) |
| 목록[].가입자성명 | 목록[].가입자성명 | 가입자성명 | text | 김숙성 |
| signer.name | customer.name | 가입자성명 | text | 박찬연 |
| seal.signer | seal.customer | 가입자성명 | seal | 박찬연 |
| sign.signer | sign.customer | 가입자성명 | signature | 강순준 |
| 목록[].서명또는 | 목록[].서명또는 | 서명또는(인) | text |  |
| 목록[].생년월일 | 목록[].생년월일 | 생년월일(주민번호) | text | 2026.01.24 |
| 목록[].제도전환전출일자 | 목록[].제도전환전출일자 | 제도전환/전출일자 | text | 2025.04.15 |
| check.미신청 | check.미신청 | 미신청 | checkbox | 미신청 |
| check.미신청2 | check.미신청2 | 미신청 | checkbox | 미신청 |
| check.미신청3 | check.미신청3 | 미신청 | checkbox | 신청 |
| check.미신청4 | check.미신청4 | 미신청 | checkbox | 신청 |
| check.미신청5 | check.미신청5 | 미신청 | checkbox | 신청 |
| check.미신청6 | check.미신청6 | 미신청 | checkbox | 미신청 |
| check.미신청7 | check.미신청7 | 미신청 | checkbox | 신청 |
| 목록[].현물이전유의사항확인 | 목록[].현물이전유의사항확인 | 현물이전유의사항확인 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 기업명 | text | (주)유니온무역 |
| seal.signer2 | seal.corp | 기업명 | seal | 주식회사 한빛패션 |
| sign.signer2 | sign.signer2 | 기업명 | signature | (주)유니온무역 |
| signer3.name | signer3.name | 신탁관리인 | text | 원원주 |
| seal.signer3 | seal.signer3 | 신탁관리인 | seal | 원원주 |
| sign.signer3 | sign.signer3 | 신탁관리인 | signature | 박환수 |
| seal.signer4 | seal.signer4 | 이전받는기업의법인인감증명서징구 | seal | 박찬연 |
| sign.signer4 | sign.signer4 | 이전받는기업의법인인감증명서징구 | signature | 김소윤 |

### hf167 · 퇴직연금 사전지정운용제도 신청서(디폴트옵션, 기업용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.167 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| check.등록구분 | check.등록구분 | 등록구분 | checkbox | 변경 |
| company.biz_no | corp.biz_no | 사업자번호 | biz_no | 264-82-36559 |
| check.일괄선택 | check.일괄선택 | 일괄선택 | checkbox | 전체 상품 일괄 선택 |
| check.체크 | check.체크 | 체크 | checkbox | 하나은행 디폴트옵션 안정형 포트폴리오 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 기업명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 기업명 | seal | (주)다온커뮤니케이션 |
| sign.signer | sign.customer | 기업명 | signature | (주)유니온무역 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 함선승 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이준은 |

### hf168 · 퇴직연금 사전지정운용방법 지정 신청서(디폴트옵션 지정)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.168 (퇴직연금) 원본 위에 기재

연결 업무: 개인형IRP 개설 (irp_opening)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| check.제도 | check.제도 | 제도 | checkbox | 개인형IRP(고객 단위로 사전운용지정방법 지정(계좌 복수일 경우 1개만  |
| customer.birth | customer.birth | 생년월일 | date | 1990-02-10 |
| check.택1 | check.택1 | 택1 | checkbox | 전화 |
| check.선택 | check.선택 | 선택(1개) | checkbox | 하나은행 디폴트옵션 중립투자형 포트폴리오 1 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| check.투자권유를희망함 | check.투자권유를희망함 | 투자권유를희망함 | checkbox | 투자권유를 희망함 |
| check.투자권유를희망하지않음 | check.투자권유를희망하지않음 | 투자권유를희망하지않음 | checkbox | 투자권유를 희망하지 않음 |
| handwritten | handwritten | 아래내용에대해 | text | 설명을듣고이해하였음 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 확인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 한서민 |
| seal.staff.판매직원 | seal.staff.판매직원 | 판매직원 | seal | 확인 |
| sign.staff.판매직원 | sign.staff.판매직원 | 판매직원 | signature | 여민정 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 천영성 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 박아린 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 진형승 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 임도성 |
| check.일반금융소비자 | check.일반금융소비자 | 일반금융소비자 | checkbox | 만 65세 이상 고령자 |
| check.전문금융소비자 | check.전문금융소비자 | 전문금융소비자 | checkbox | 만 19세 이상 ~ 만 65세 미만 성년자 |
| check.일반금융소비자2 | check.일반금융소비자2 | 일반금융소비자 | checkbox | 일반투자자(투자자정보확인서에서 일반투자자 선택) |
| check.전문금융소비자2 | check.전문금융소비자2 | 전문금융소비자 | checkbox | 전문투자자(투자자정보확인서에서 전문투자자 선택) |
| check.약관및상품설명서 | check.약관및상품설명서 | 약관및상품설명서 | checkbox | 서면 수령 |
| signer.name | signer.name | 가입자 | text | 박찬연 |
| seal.signer | seal.customer | 가입자 | seal | 박찬연 |
| sign.signer | sign.customer | 가입자 | signature | 강순준 |
| signer2.name | agent.name | 대리인 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인 | seal | 설기현 |
| sign.signer2 | sign.agent | 대리인 | signature | 박영준 |
| handwritten2 | handwritten2 | 가입자자필기재 | text | 설명듣고이해함 |
| handwritten3 | handwritten3 | 가입자자필기재 | text | 계약서,약관,상품설명서를수령함 |
| handwritten4 | handwritten4 | 가입자자필기재 | text | 설명을듣고이해 |

연결 업무 irp_opening · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### hf169 · 퇴직연금 가입자 거래신청서(DC/기업형IRP)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.169 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| employer.name | employer.name | 회사명 | text | 주식회사 태평양무역 |
| customer.birth | customer.birth | 생년월일 | date | 900210 |
| check.휴대전화 | check.휴대전화 | 휴대전화 | checkbox | LG U+ |
| customer.address | customer.address | 자택주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| employer.address | employer.address | 직장주소 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태평양무역 구매팀 |
| customer.home_phone | customer.home_phone | 자택전화 | phone | 02-6588-1442 |
| check.우편물수령처 | check.우편물수령처 | 우편물수령처 | checkbox | 직장 |
| customer.email | customer.email | 이메일주소 | text | chanyeon363@naver.com |
| employer.phone | employer.phone | 직장전화 | phone | 043-783-2775 |
| check.전화연락처 | check.전화연락처 | 전화연락처 | checkbox | 원치않음 |
| check.원리금보장상품만기도래시전월통지발송 | check.원리금보장상품만기도래시전월통지발송 | 원리금보장상품(정기예금등)만기도래시전월통지발송 | checkbox | 이메일 |
| check.신청 | check.신청 | 신청(미발송) | checkbox | 신청(미발송) |
| check.퇴직연금운용및자산관리약관이변경되는경우통지 | check.퇴직연금운용및자산관리약관이변경되는경우통지 | 퇴직연금운용및자산관리약관이변경되는경우통지 | checkbox | 이메일 |
| check.전화 | check.전화 | 전화(휴대폰) | checkbox | 전화(휴대폰) |
| 기업부담금_목록[].상품명 | 기업부담금_목록[].상품명 | 상품명 | text | 하나 IRP 정기예금 3년 |
| check.개인부담금 | check.개인부담금 | 개인부담금 | checkbox | 개인부담금에 대하여 기업부담금(퇴직금)과 동일한 운용지시(체크 후 아래  |
| 개인부담금_목록[].상품명 | 개인부담금_목록[].상품명 | 상품명 | text | 정기예금 (1년) |
| 기업부담금_목록[].매수비율 | 기업부담금_목록[].매수비율 | 매수비율(%) | text | 100 |
| 개인부담금_목록[].매수비율 | 개인부담금_목록[].매수비율 | 매수비율(%) | text | 100 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 나성윤 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 석나지 |
| seal.staff.판매직원 | seal.staff.판매직원 | 판매직원 | seal | 강용예 |
| sign.staff.판매직원 | sign.staff.판매직원 | 판매직원 | signature | 안우찬 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 황보우지 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 안현하 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 구정서 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 강승빈 |
| 목록[].상품명 | 목록[].상품명 | 상품명 | text | 미국S&P500 인덱스 증권투자신탁 |
| check.부담금구분 | check.부담금구분 | 부담금구분 | checkbox | 개인부담금 |
| 목록[].매수비율 | 목록[].매수비율 | 매수비율(%) | number | 100 |
| check.선택 | check.선택 | 선택(1개) | checkbox | 하나은행 디폴트옵션 적극투자형 포트폴리오 2 |
| check.보험성상품 | check.보험성상품 | 보험성상품(GIC) | checkbox | 일반금융소비자 |
| check.일반금융소비자 | check.일반금융소비자 | 일반금융소비자 | checkbox | 피한정후견인 |
| check.전문금융소비자 | check.전문금융소비자 | 전문금융소비자 | checkbox | 만 19세 이상~만 65세 미만 성년자 |
| check.일반금융소비자2 | check.일반금융소비자2 | 일반금융소비자 | checkbox | 일반투자자(투자자정보확인서에서 일반투자자 선택) |
| check.전문금융소비자2 | check.전문금융소비자2 | 전문금융소비자 | checkbox | 전문투자자(투자자정보확인서에서 전문투자자 선택) |
| check.약관및상품설명서 | check.약관및상품설명서 | 약관및상품설명서 | checkbox | 알림톡(발송실패시 LMS 발송) |
| check.투자권유를희망함 | check.투자권유를희망함 | 투자권유를희망함 | checkbox | 투자권유를 희망함 |
| check.투자권유를희망하지않음 | check.투자권유를희망하지않음 | 투자권유를희망하지않음 | checkbox | 투자권유를 희망하지 않음 |
| handwritten | handwritten | 아래내용에대해 | text | 설명을듣고이해하였음 |
| handwritten2 | handwritten2 | 가입자자필기재 | text | 설명듣고이해함 |
| handwritten3 | handwritten3 | 가입자자필기재 | text | 계약서,약관,상품설명서를수령함 |
| signer.name | signer.name | 가입자 | text | 박찬연 |
| seal.signer | seal.customer | 가입자 | seal | 박찬연 |
| sign.signer | sign.customer | 가입자 | signature | 강순준 |
| signer2.name | agent.name | 대리인 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인 | seal | 김순우 |
| sign.signer2 | sign.agent | 대리인 | signature | 박영준 |
| handwritten4 | handwritten4 | 가입자자필기재 | text | 설명을듣고이해 |

### hf170 · 퇴직연금 계약이전 신청서(기업형IRP)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.170 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| customer.name | customer.name | 가입자명 | text | 박찬연 |
| account | account | 퇴직연금계좌번호 | account_no | 000-287736-52424 |
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| check.전부이전 | check.전부이전 | 전부이전 | checkbox | 전부이전 |
| check.일부이전 | check.일부이전 | 일부이전 | checkbox | 일부이전 |
| check.제도전환 | check.제도전환 | 제도전환(기업형IRP→DC) | checkbox | 퇴직연금사업자 변경 |
| check.계열사이전 | check.계열사이전 | 계열사이전(과거입사일인정) | checkbox | 계열사 이전(과거입사일 인정) |
| 예약지급일 | 예약지급일 | 예약지급일** | date | 2025.03.12 |
| 운용관리기관 | 운용관리기관 | 운용관리기관 | text | 신한은행 |
| 자산관리기관 | 자산관리기관 | 자산관리기관 | text | 하나은행 |
| 현물이전 | 현물이전 | 현물이전* | text |  |
| check.수수료연동출금동의 | check.수수료연동출금동의 | 수수료연동출금동의 | checkbox | 동의(사전에 약정된 경우) |
| check.현물이전 | check.현물이전 | 현물이전* | checkbox | 신청(보유상품 ‘해지 없이’ 이전) |
| check.현물이전2 | check.현물이전2 | 현물이전* | checkbox | 미신청(보유상품 ‘해지 후’ 이전) |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 금융기관 | 금융기관 | 금융기관 | text | 하나은행 |
| account2 | account2 | 계좌번호 | account_no | 000-287736-52424 |
| signer.name | signer.name | 가입자 | text | 박찬연 |
| seal.signer | seal.customer | 가입자 | seal | 박찬연 |
| sign.signer | sign.customer | 가입자 | signature | 강순준 |
| signer2.name | signer2.name | 기업명 | text | (주)유니온무역 |
| seal.signer2 | seal.corp | 기업명 | seal | 주식회사 대성패션 |
| sign.signer2 | sign.signer2 | 기업명 | signature | 주식회사 한빛패션 |
| signer3.name | signer3.name | 가입자 | text | 박찬연 |
| seal.signer3 | seal.signer3 | 가입자 | seal | 박찬연 |
| sign.signer3 | sign.signer3 | 가입자 | signature | 강순준 |
| 이전받는기업 | 이전받는기업 | 이전받는기업 | text |  |
| seal.signer4 | seal.signer4 | 이전받는기업의법인인감증명서징구 | seal | 강순준 |
| sign.signer4 | sign.signer4 | 이전받는기업의법인인감증명서징구 | signature | 박찬연 |
| value | value | [유의사항] | amount |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 이서영 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 검인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 하혜호 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 검인 |

### hf171 · 퇴직연금 거래신청서(개인형IRP)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.171 (퇴직연금) 원본 위에 기재

연결 업무: 개인형IRP 개설 (irp_opening), 퇴직급여 수령 (retirement_payout)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.phone | customer.phone | 휴대전화 | phone | 010-5907-7253 |
| check.해피콜방식 | check.해피콜방식 | 해피콜방식 | checkbox | 온라인(모바일 웹) |
| customer.birth | customer.birth | 생년월일 | date | 1990-02-10 |
| customer.email | customer.email | 이메일주소 | text | chanyeon363@naver.com |
| check.신청용도 | check.신청용도 | 신청용도 | checkbox | 퇴직금용 |
| check.신청용도2 | check.신청용도2 | 신청용도 | checkbox | 퇴직금용+ |
| 퇴직급여수령을위한계좌개설 | 퇴직급여수령을위한계좌개설 | 퇴직급여수령을위한계좌개설 | text | 002-799708-70791 |
| check.할인대상정보 | check.할인대상정보 | 할인대상정보(증빙첨부) | checkbox | 장기할인(타사IRP이전시, 타사IRP가입일 |
| check.가입자격 | check.가입자격 | 가입자격 | checkbox | 퇴직금제도 적용 근로자 |
| check.원리금보장상품만기도래시전월통지발송 | check.원리금보장상품만기도래시전월통지발송 | 원리금보장상품(정기예금등)만기도래시전월통지발송 | checkbox | 이메일 |
| check.서비스통지발송제외신청 | check.서비스통지발송제외신청 | 서비스통지발송제외신청 | checkbox | 신청안함(발송) |
| check.퇴직연금운용및자산관리약관이변경되는경우통지 | check.퇴직연금운용및자산관리약관이변경되는경우통지 | 퇴직연금운용및자산관리약관이변경되는경우통지 | checkbox | 이메일 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| check.투자권유를희망함 | check.투자권유를희망함 | 투자권유를희망함 | checkbox | 투자권유를 희망함 |
| check.투자권유를희망하지않음 | check.투자권유를희망하지않음 | 투자권유를희망하지않음 | checkbox | 투자권유를 희망하지 않음 |
| handwritten | handwritten | 아래내용에대해 | text | 설명을듣고이해하였음 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 검인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 박영주 |
| seal.staff.판매직원 | seal.staff.판매직원 | 판매직원 | seal | 조예은 |
| sign.staff.판매직원 | sign.staff.판매직원 | 판매직원 | signature | 이호성 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김소희 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 장민원 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김혁윤 |
| check.선택 | check.선택 | 선택(1개) | checkbox | 하나은행 디폴트옵션 중립투자형 포트폴리오 1 |
| 기업부담금_목록[].상품명 | 기업부담금_목록[].상품명 | 상품명 | text | 하나 단기채 증권투자신탁 |
| check.개인부담금 | check.개인부담금 | 개인부담금 | checkbox | 개인부담금에 대하여 기업부담금(퇴직금)과 동일한 운용지시(체크 후 아래  |
| 개인부담금_목록[].상품명 | 개인부담금_목록[].상품명 | 상품명 | text | MMF 증권투자신탁 |
| 기업부담금_목록[].매수비율 | 기업부담금_목록[].매수비율 | 매수비율(%) | text | 10 |
| 개인부담금_목록[].매수비율 | 개인부담금_목록[].매수비율 | 매수비율(%) | text | 35 |
| check.보험성상품 | check.보험성상품 | 보험성상품(GIC) | checkbox | 일반금융소비자 |
| check.일반금융소비자 | check.일반금융소비자 | 일반금융소비자 | checkbox | 피성년후견인 |
| check.전문금융소비자 | check.전문금융소비자 | 전문금융소비자 | checkbox | 전문금융소비자이나 상품설명을 희망 |
| check.일반금융소비자2 | check.일반금융소비자2 | 일반금융소비자 | checkbox | 일반투자자(투자자정보확인서에서 일반투자자 선택) |
| check.전문금융소비자2 | check.전문금융소비자2 | 전문금융소비자 | checkbox | 전문투자자(투자자정보확인서에서 전문투자자 선택) |
| handwritten2 | handwritten2 | 가입자자필기재 | text | 설명듣고이해함 |
| check.약관및상품설명서 | check.약관및상품설명서 | 약관및상품설명서 | checkbox | 알림톡(발송실패시 LMS 발송) |
| signer.name | signer.name | 가입자 | text | 박찬연 |
| seal.signer | seal.customer | 가입자 | seal | 박찬연 |
| sign.signer | sign.customer | 가입자 | signature | 강순준 |
| signer2.name | agent.name | 대리인 | text | 강석호 |
| seal.signer2 | seal.agent | 대리인 | seal | 강석호 |
| sign.signer2 | sign.agent | 대리인 | signature | 이도민 |
| handwritten3 | handwritten3 | 가입자자필기재 | text | 계약서,약관,상품설명서를수령함 |
| handwritten4 | handwritten4 | 가입자자필기재 | text | 설명을듣고이해수령 |

연결 업무 irp_opening · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

연결 업무 retirement_payout · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### hf172 · 퇴직연금 거래신청서(DC, 기업형IRP)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.172 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| check.제도구분 | check.제도구분 | 제도구분 | checkbox | DC |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| check.기업구분 | check.기업구분 | 기업구분 | checkbox | 개인사업자 |
| 회계결산월 | 회계결산월 | 회계결산월 | text |  |
| check.근로자대표 | check.근로자대표 | 근로자대표 | checkbox | 근로자과반수 |
| check.제도가입대상 | check.제도가입대상 | 제도가입대상 | checkbox | 입사후 1년 경과가입 |
| check.제도가입대상2 | check.제도가입대상2 | 제도가입대상 | checkbox | 임원제외 |
| check.부담금납입주기 | check.부담금납입주기 | 부담금납입주기 | checkbox | 월납 |
| check.표준형DC대상여부 | check.표준형DC대상여부 | 표준형DC대상여부 | checkbox |  비대상 |
| check.장기할인수수료대상여부 | check.장기할인수수료대상여부 | 장기할인수수료대상여부* | checkbox |  비대상 |
| date | date | 제도시행일 | date | 2026년 1월 31일 |
| check.퇴직연금가입기간 | check.퇴직연금가입기간 | 퇴직연금가입기간 | checkbox | 제도가입 이전 특정시점 이후 근무분 포함 |
| date2 | date2 | 규약수리통보일 | date | 2026년 1월 31일 |
| check.약관변경통지방법 | check.약관변경통지방법 | 약관변경통지방법 | checkbox |  이메일 |
| check.중소기업수수료할인대상여부 | check.중소기업수수료할인대상여부 | 중소기업수수료할인대상여부 | checkbox |  비대상 |
| customer.name | customer.name | 이름 | text | 박찬연 |
| customer.name2 | customer.name2 | 이름 | text | 박찬연 |
| customer.phone | customer.phone | 휴대폰번호 | phone | 010-5907-7253 |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| customer.birth2 | customer.birth2 | 생년월일 | date | 1990년 2월 10일 |
| customer.email | customer.email | 이메일주소 | text | chanyeon363@naver.com |
| check.일괄선택 | check.일괄선택 | 일괄선택 | checkbox | 전체 상품 일괄 선택 |
| check.체크 | check.체크 | 체크 | checkbox | 하나은행 디폴트옵션 적극투자형 포트폴리오 2 |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| customer.name3 | customer.name3 | 성명 | text | 박찬연 |
| customer.birth3 | customer.birth3 | 생년월일 | date | 1990년 2월 10일 |
| 금융기관 | 금융기관 | 금융기관 | text | 하나은행 |
| customer.name4 | customer.name4 | 예금주 | text | 박찬연 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 김원혜 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 김우은 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 박희주 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 채진아 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 엄상정 |
| check.사원번호임직원구분 | check.사원번호임직원구분 | -사원번호:-임직원구분 | checkbox | 임원 4) 20 |
| check.사원번호임직원구분2 | check.사원번호임직원구분2 | -사원번호:-임직원구분 | checkbox | 직원 |
| check.사원번호임직원구분3 | check.사원번호임직원구분3 | -사원번호:-임직원구분 | checkbox | 임원 4) 20 |
| check.사원번호임직원구분4 | check.사원번호임직원구분4 | -사원번호:-임직원구분 | checkbox | 직원 |
| 가입자수 | 가입자수 | 가입자수 | number | 2 |
| check.등록정보 | check.등록정보 | 등록정보 | checkbox | 개별등록(아래표 작성) |
| 기업부담금합계 | 기업부담금합계 | 기업부담금합계 | number | 8,920,000 |
| check.신청 | check.신청 | 신청 | checkbox | 신청 |
| check.신청2 | check.신청2 | 신청 | checkbox | 신청 |
| account | account | 출금계좌번호 | account_no | 000-287736-52424 |
| account2 | account2 | 출금계좌번호 | account_no | 000-287736-52424 |
| 이체개시일 | 이체개시일 | 이체개시일 | date | 2025-04-05 |
| 이체종료일 | 이체종료일 | 이체종료일 | date | 2026.08.19 |
| check.신청3 | check.신청3 | 신청 | checkbox | 신청 |
| check.신청4 | check.신청4 | 신청 | checkbox | 신청 |
| account3 | account3 | 출금계좌번호 | account_no | 000-287736-52424 |
| account4 | account4 | 출금계좌번호 | account_no | 000-287736-52424 |
| signer.name | signer.name | 기업명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 기업명 | seal | 주식회사 한빛패션 |
| sign.signer | sign.customer | 기업명 | signature | (주)스마트에프앤비 |

### hf173 · 투자자확인서(퇴직연금용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.173 (퇴직연금) 원본 위에 기재

연결 업무: 개인형IRP 개설 (irp_opening)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 투자자 | text | 박찬연 |
| seal.signer | seal.customer | 투자자 | seal | 박찬연 |
| sign.signer | sign.customer | 투자자 | signature | 이욱유 |
| signer2.name | agent.name | 대리인 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인 | seal | 김순우 |
| sign.signer2 | sign.agent | 대리인 | signature | 박영준 |
| check.원금손실위험이거의없거나 | check.원금손실위험이거의없거나 | 원금손실위험이거의없거나경미한수준이다. | checkbox | 원금손실위험이 거의 없거나 경미한 수준이다. |
| check.원금손실위험이있지만높은 | check.원금손실위험이있지만높은 | 원금손실위험이있지만높은수익률을위해감수할수있다. | checkbox | 원금손실위험이 있지만 높은 수익률을 위해 감수할 수 있다. |
| check.경미한수준일것이다 | check.경미한수준일것이다 | 경미한수준일것이다. | checkbox | 경미한 수준일 것이다. |
| check.원금의최대100손실이 | check.원금의최대100손실이 | 원금의최대100%(원금전액)손실이발생할수있다. | checkbox | 원금의 최대 100%(원금 전액) 손실이 발생할 수 있다. |
| check.예 | check.예 | 예 | checkbox | 아니오 |
| check.email | check.email | e-mail | checkbox | e-mail |
| signer3.name | signer3.name | 판매직원 | text | 옥승찬 |
| seal.signer3 | seal.signer3 | 판매직원 | seal | 곽환정 |
| sign.signer3 | sign.signer3 | 판매직원 | signature | 옥승찬 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer4.name | signer4.name | 투자자 | text | 박찬연 |
| seal.signer4 | seal.signer4 | 투자자 | seal | 박찬연 |
| sign.signer4 | sign.signer4 | 투자자 | signature | 강순준 |
| signer5.name | signer5.name | 대리인 | text | 강석호 |
| seal.signer5 | seal.signer5 | 대리인 | seal | 강석호 |
| sign.signer5 | sign.signer5 | 대리인 | signature | 김순우 |
| check.원금손실위험이거의없거나2 | check.원금손실위험이거의없거나2 | 원금손실위험이거의없거나경미한수준이다. | checkbox | 원금손실위험이 거의 없거나 경미한 수준이다. |
| check.원금손실위험이있지만높은2 | check.원금손실위험이있지만높은2 | 원금손실위험이있지만높은수익률을위해감수할수있다. | checkbox | 원금손실위험이 있지만 높은 수익률을 위해 감수할 수 있다. |
| check.경미한수준일것이다2 | check.경미한수준일것이다2 | 경미한수준일것이다. | checkbox | 경미한 수준일 것이다. |
| check.원금의최대100손실이2 | check.원금의최대100손실이2 | 원금의최대100%(원금전액)손실이발생할수있다. | checkbox | 원금의 최대 100%(원금 전액) 손실이 발생할 수 있다. |
| check.예2 | check.예2 | 예 | checkbox | 아니오 |
| check.email2 | check.email2 | e-mail | checkbox | 수령거절 |
| signer6.name | signer6.name | 판매직원 | text | 표연찬 |
| seal.signer6 | seal.signer6 | 판매직원 | seal | 이미진 |
| sign.signer6 | sign.signer6 | 판매직원 | signature | 표연찬 |

연결 업무 irp_opening · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### hf174 · 퇴직연금 계약이전 동의서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.174 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| check.동의주체 | check.동의주체 | 동의주체 | checkbox | 노동조합(근로자 과반수로 조직된 노동조합이 있는 경우) |
| check.제도구분 | check.제도구분 | 제도구분 | checkbox | DC |
| check.동의 | check.동의 | 동의 | checkbox | 동의 |
| check.동의2 | check.동의2 | 동의 | checkbox | 미동의 |
| check.동의3 | check.동의3 | 동의 | checkbox | 미동의 |
| check.동의4 | check.동의4 | 동의 | checkbox | 미동의 |
| check.동의5 | check.동의5 | 동의 | checkbox | 미동의 |
| check.동의6 | check.동의6 | 동의 | checkbox | 동의 |
| check.동의7 | check.동의7 | 동의 | checkbox | 동의 |
| check.동의8 | check.동의8 | 동의 | checkbox | 미동의 |
| check.동의9 | check.동의9 | 동의 | checkbox | 미동의 |
| check.동의10 | check.동의10 | 동의 | checkbox | 미동의 |
| check.동의11 | check.동의11 | 동의 | checkbox | 미동의 |
| check.동의12 | check.동의12 | 동의 | checkbox | 미동의 |
| check.동의13 | check.동의13 | 동의 | checkbox | 미동의 |
| check.동의14 | check.동의14 | 동의 | checkbox | 동의 |
| check.동의15 | check.동의15 | 동의 | checkbox | 동의 |
| check.동의16 | check.동의16 | 동의 | checkbox | 미동의 |
| check.동의17 | check.동의17 | 동의 | checkbox | 미동의 |
| check.동의18 | check.동의18 | 동의 | checkbox | 동의 |
| check.동의19 | check.동의19 | 동의 | checkbox | 미동의 |
| check.동의20 | check.동의20 | 동의 | checkbox | 동의 |
| 목록[].성명 | 목록[].성명 | 성명 | text | 이민예 |
| 목록[].생년월일 | 목록[].생년월일 | 생년월일 | text | 2025년 1월 30일 |
| signer.name | customer.name | 생년월일 | text | 박찬연 |
| seal.signer | seal.customer | 생년월일 | seal | 현예지 |
| sign.signer | sign.customer | 생년월일 | signature | 박찬연 |
| 목록[].인서명 | 목록[].인서명 | 인/서명 | text |  |
| check.동의21 | check.동의21 | 동의 | checkbox | 동의 |
| check.동의22 | check.동의22 | 동의 | checkbox | 동의 |
| check.동의23 | check.동의23 | 동의 | checkbox | 동의 |
| check.동의24 | check.동의24 | 동의 | checkbox | 동의 |
| check.동의25 | check.동의25 | 동의 | checkbox | 미동의 |
| check.동의26 | check.동의26 | 동의 | checkbox | 동의 |
| check.동의27 | check.동의27 | 동의 | checkbox | 동의 |
| check.동의28 | check.동의28 | 동의 | checkbox | 동의 |
| check.동의29 | check.동의29 | 동의 | checkbox | 미동의 |
| check.동의30 | check.동의30 | 동의 | checkbox | 동의 |
| check.동의31 | check.동의31 | 동의 | checkbox | 미동의 |
| check.동의32 | check.동의32 | 동의 | checkbox | 동의 |
| check.동의33 | check.동의33 | 동의 | checkbox | 동의 |
| check.동의34 | check.동의34 | 동의 | checkbox | 동의 |
| check.동의35 | check.동의35 | 동의 | checkbox | 미동의 |
| check.동의36 | check.동의36 | 동의 | checkbox | 동의 |
| check.동의37 | check.동의37 | 동의 | checkbox | 동의 |
| check.동의38 | check.동의38 | 동의 | checkbox | 동의 |
| check.동의39 | check.동의39 | 동의 | checkbox | 동의 |
| check.동의40 | check.동의40 | 동의 | checkbox | 미동의 |
| signer2.name | signer2.name | 생년월일 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 생년월일 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 생년월일 | signature | 강순준 |
| signer3.name | corp.ceo | 대표자 | text | 박찬연 |
| seal.signer3 | seal.corp | 대표자 | seal | 강순준 |
| sign.signer3 | sign.signer3 | 대표자 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| check.근로자동의 | check.근로자동의 | 근로자동의 | checkbox | 근로자 동의 |
| check.노동조합동의 | check.노동조합동의 | 노동조합동의 | checkbox | 노동조합 동의 |
| signer4.name | signer4.name | 기업명 | text | (주)유니온무역 |
| seal.signer4 | seal.signer4 | 기업명 | seal | (주)대한시스템즈 |
| sign.signer4 | sign.signer4 | 기업명 | signature | 주식회사 한빛패션 |
| company.ceo | company.ceo | 대표자 | text | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 박지인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 장도민 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 우수하 |

### hf175 · 퇴직연금 AI 포트폴리오 설계(신규 리밸런싱)신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.175 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| check.제도구분 | check.제도구분 | 제도구분 | checkbox | 개인형IRP |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| 계좌번호또는회사명 | 계좌번호또는회사명 | 계좌번호또는회사명 | text | 592-432747-29336 |
| 하나연금닥터AI연금투자솔루션 | 하나연금닥터AI연금투자솔루션 | 하나연금닥터AI연금투자솔루션 | text |  |
| check.포트폴리오매수또는리밸런싱후6개월마다리밸런싱안내 | check.포트폴리오매수또는리밸런싱후6개월마다리밸런싱안내 | 포트폴리오매수또는리밸런싱후6개월마다리밸런싱안내 | checkbox | 이메일 |
| check.신청여부 | check.신청여부 | 신청여부 | checkbox | 신청안함 |
| 상승 | 상승 | 상승+( | text |  |
| 하락 | 하락 | )%하락–( | text |  |
| handwritten | handwritten | 설계신청을동의합니다. | text | (동의함) |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인(본인) | text | 박찬연 |
| seal.signer | seal.customer | 신청인(본인) | seal | 박찬연 |
| sign.signer | sign.customer | 신청인(본인) | signature | 강순준 |
| 에도달할경우통지 | 에도달할경우통지 | 에도달할경우통지 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 확인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 현석재 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 옥아진 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 류아예 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이하태 |

### hf176 · 퇴직연금 퇴직급여 지급신청서(DC,기업형IRP)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.176 (퇴직연금) 원본 위에 기재

연결 업무: 퇴직급여 수령 (retirement_payout)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| employer.hire_date | employer.hire_date | 입사일자 | date | 2020.05.08 |
| account | account | 퇴직연금계좌번호 | account_no | 000-287736-52424 |
| customer.birth | customer.birth | 생년월일 | date | 900210 |
| 중간정산일자 | 중간정산일자 | 중간정산일자 | date | 2025.11.06 |
| check.제도구분 | check.제도구분 | 제도구분 | checkbox | DC |
| check.임원여부 | check.임원여부 | 임원여부 | checkbox | 임원 |
| 퇴직급여입금총액 | 퇴직급여입금총액 | 퇴직급여입금총액* | number | 8,960,000 |
| 퇴직일자 | 퇴직일자 | 퇴직일자 | date | 2026-01-01 |
| check.지급형태 | check.지급형태 | 지급형태 | checkbox | 개인형IRP(의무) |
| check.지급형태2 | check.지급형태2 | 지급형태 | checkbox | 입출금계좌 |
| check.잔여부담금 | check.잔여부담금 | 잔여부담금*** | checkbox | 없음 |
| check.잔여부담금2 | check.잔여부담금2 | 잔여부담금*** | checkbox | 있음 (금액 |
| check.기업반환신청 | check.기업반환신청 | 기업반환신청***** | checkbox | 국민연금 전환금 |
| check.현물이전 | check.현물이전 | 현물이전** | checkbox | 신청 (보유상품 ‘해지 없이’ IRP로 이전) |
| check.예외사유 | check.예외사유 | 예외사유 | checkbox | 가입자 사망 |
| check.연동출금신청 | check.연동출금신청 | 연동출금신청(사전에약정된경우) | checkbox | 미신청(기업별도입금) |
| 예약지급일 | 예약지급일 | 예약지급일* | date | 2025-01-07 |
| check.당해연도이전에중간정산한금액이있는경우 | check.당해연도이전에중간정산한금액이있는경우 | 당해연도이전에중간정산(중도인출)한금액이있는경우 | checkbox | 해당사항 없음 |
| check.해당사항없음 | check.해당사항없음 | 해당사항없음 | checkbox | 해당사항 없음 |
| 금융기관명 | 금융기관명 | 금융기관명 | text | 카카오뱅크 |
| 금융기관명2 | 금융기관명2 | 금융기관명 | text | 기업은행 |
| account2 | account2 | 계좌번호 | account_no | 000-287736-52424 |
| account3 | account3 | 계좌번호 | account_no | 000-287736-52424 |
| check.퇴직소득세계산을위한근속연수산정시제외가산월수있는경우기재 | check.퇴직소득세계산을위한근속연수산정시제외가산월수있는경우기재 | 퇴직소득세계산을위한근속연수산정시제외·가산월수있는경우기재 | checkbox | 가산월수( |
| check.개인적립금과세제외신청 | check.개인적립금과세제외신청 | 개인적립금과세제외신청 | checkbox | 과세제외 미신청 |
| check.가입자단독청구 | check.가입자단독청구 | 가입자단독청구 | checkbox | 기타 (사용자 지급거절 등) |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 가입자 | text | 박찬연 |
| seal.signer | seal.customer | 가입자 | seal | 강순준 |
| sign.signer | sign.customer | 가입자 | signature | 박찬연 |
| signer2.name | signer2.name | 가입자 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 가입자 | seal | 강순준 |
| sign.signer2 | sign.signer2 | 가입자 | signature | 박찬연 |
| signer3.name | signer3.name | 기업명 | text | (주)유니온무역 |
| seal.signer3 | seal.corp | 기업명 | seal | 주식회사 대성패션 |
| sign.signer3 | sign.signer3 | 기업명 | signature | (주)유니온무역 |
| signer4.name | signer4.name | 가입자 | text | 박찬연 |
| seal.signer4 | seal.signer4 | 가입자 | seal | 박찬연 |
| sign.signer4 | sign.signer4 | 가입자 | signature | 강순준 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 염혁현 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 검인 |
| 타금융기관IRP통장사본 | 타금융기관IRP통장사본 | 타금융기관IRP통장사본(가입확인서) | text | 농협은행 |
| 연금보험료등소득세액공제확인서 | 연금보험료등소득세액공제확인서 | 연금보험료등소득☞세액공제확인서 | number | 390,000 |
| signer5.name | signer5.name | 가입자 | text | 박찬연 |
| seal.signer5 | seal.signer5 | 가입자 | seal | 박찬연 |
| sign.signer5 | sign.signer5 | 가입자 | signature | 강순준 |
| 아래양식중한가지 | 아래양식중한가지 | 아래양식중한가지 | text |  |

연결 업무 retirement_payout · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### hf177 · 퇴직연금 운용상품지정 신청서(DC)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.177 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자번호 | biz_no | 264-82-36559 |
| check.아래의상품을퇴직연금운용상품으로 | check.아래의상품을퇴직연금운용상품으로 | 아래의상품을퇴직연금운용상품으로 | checkbox | 선택  |
| 상품선택 | 상품선택 | 상품선택 | text | 이율보증형 보험(GIC) 1년 |
| 상품명 | 상품명 | 상품명 | text | 미국S&P500 인덱스 증권투자신탁 |
| 경남은행정기예금 | 경남은행정기예금 | 경남은행정기예금 | text | 신한은행 |
| 수익증권_목록[].경남은행정기예금 | 수익증권_목록[].경남은행정기예금 | 경남은행정기예금 | text | 국민은행 |
| 부산은행정기예금 | 부산은행정기예금 | 부산은행정기예금 | text | 우리은행 |
| 정기예금_목록[].년 | 정기예금_목록[].년 | 년 | text |  |
| 상품명2 | 상품명2 | 상품명 | text | 국내채권형 증권자투자신탁 |
| 저축은행정기예금_목록[].JT저축은행정기예금 | 저축은행정기예금_목록[].JT저축은행정기예금 | JT저축은행정기예금 | text | 농협은행 |
| 하나저축은행정기예금 | 하나저축은행정기예금 | 하나저축은행정기예금 | text | 하나은행 |
| 신한저축은행정기예금 | 신한저축은행정기예금 | 신한저축은행정기예금 | text | 신한은행 |
| NH저축은행정기예금 | NH저축은행정기예금 | NH저축은행정기예금 | text | 국민은행 |
| KB저축은행정기예금 | KB저축은행정기예금 | KB저축은행정기예금 | text | 하나은행 |
| IBK저축은행정기예금 | IBK저축은행정기예금 | IBK저축은행정기예금 | text | 농협은행 |
| 한화저축은행정기예금 | 한화저축은행정기예금 | 한화저축은행정기예금 | text | 국민은행 |
| SBI저축은행정기예금 | SBI저축은행정기예금 | SBI저축은행정기예금 | text | 신한은행 |
| OK저축은행정기예금 | OK저축은행정기예금 | OK저축은행정기예금 | text | 우리은행 |
| 키움저축은행정기예금 | 키움저축은행정기예금 | 키움저축은행정기예금 | text | 농협은행 |
| 키움예스저축은행정기예금 | 키움예스저축은행정기예금 | 키움예스저축은행정기예금 | text | 카카오뱅크 |
| 페퍼저축은행정기예금 | 페퍼저축은행정기예금 | 페퍼저축은행정기예금 | text | 농협은행 |
| 모아저축은행정기예금 | 모아저축은행정기예금 | 모아저축은행정기예금 | text | 우리은행 |
| 유진저축은행정기예금 | 유진저축은행정기예금 | 유진저축은행정기예금 | text | 카카오뱅크 |
| OSB저축은행정기예금 | OSB저축은행정기예금 | OSB저축은행정기예금 | text | 기업은행 |
| JT저축은행정기예금 | JT저축은행정기예금 | JT저축은행정기예금 | text | 기업은행 |
| check.보기1 | check.보기1 | 보기1 | checkbox | 보기1 |
| check.보기12 | check.보기12 | 보기1 | checkbox | 보기1 |
| check.보기13 | check.보기13 | 보기1 | checkbox | 보기1 |
| check.보기14 | check.보기14 | 보기1 | checkbox | 보기1 |
| check.보기15 | check.보기15 | 보기1 | checkbox | 보기1 |
| check.보기16 | check.보기16 | 보기1 | checkbox | 보기1 |
| check.보기17 | check.보기17 | 보기1 | checkbox | 보기1 |
| 저축은행정기예금_목록[].년 | 저축은행정기예금_목록[].년 | 년 | text |  |
| check.보기18 | check.보기18 | 보기1 | checkbox | 보기1 |
| check.보기19 | check.보기19 | 보기1 | checkbox | 보기1 |
| check.보기110 | check.보기110 | 보기1 | checkbox | 보기1 |
| check.보기111 | check.보기111 | 보기1 | checkbox | 보기1 |
| check.보기112 | check.보기112 | 보기1 | checkbox | 보기1 |
| check.보기113 | check.보기113 | 보기1 | checkbox | 보기1 |
| check.보기114 | check.보기114 | 보기1 | checkbox | 보기1 |
| check.보기115 | check.보기115 | 보기1 | checkbox | 보기1 |
| check.보기116 | check.보기116 | 보기1 | checkbox | 보기1 |
| check.보기117 | check.보기117 | 보기1 | checkbox | 보기1 |
| check.보기118 | check.보기118 | 보기1 | checkbox | 보기1 |
| check.개월 | check.개월 | 개월 | checkbox | □ |
| check.년 | check.년 | 년 | checkbox | □ |
| check.년2 | check.년2 | 년 | checkbox | □ |
| check.년3 | check.년3 | 년 | checkbox | □ |
| check.년4 | check.년4 | 년 | checkbox | 저 축 은 행 정 기 예 금 |
| check.개월2 | check.개월2 | 개월 | checkbox | □ |
| check.년5 | check.년5 | 년 | checkbox | □ |
| check.년6 | check.년6 | 년 | checkbox | □ |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 기업명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 기업명 | seal | (주)삼정전자 |
| sign.signer | sign.customer | 기업명 | signature | (주)유니온무역 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 확인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 원용지 |

### hf178 · 퇴직연금 입금예정상품등록/변경 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.178 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명(기업명) | text | 박찬연 |
| check.제도구분 | check.제도구분 | 제도구분 | checkbox | DC |
| customer.birth | customer.birth | 생년월일(사업자등록번호) | date | 1990.02.10 |
| 계좌번호또는회사명 | 계좌번호또는회사명 | 계좌번호또는회사명 | text | 964-030192-77102 |
| check.상품구분 | check.상품구분 | 상품구분 | checkbox | AI포트폴리오 |
| 기업부담금_목록[].상품명 | 기업부담금_목록[].상품명 | 상품명 | text | 원리금보장 ELB 1년 |
| check.개인부담금 | check.개인부담금 | 개인부담금 | checkbox | 개인부담금에 대하여 기업부담금(퇴직금)과 동일한 운용지시(√체크 후 아래 |
| 개인부담금_목록[].상품명 | 개인부담금_목록[].상품명 | 상품명 | text | 하나 TDF 2045 증권투자신탁 |
| 기업부담금_목록[].매수비율 | 기업부담금_목록[].매수비율 | 매수비율(%) | number | 100 |
| 개인부담금_목록[].매수비율 | 개인부담금_목록[].매수비율 | 매수비율(%) | text | 85 |
| 목록[].상품명 | 목록[].상품명 | 상품명 | text | 하나 TDF 2045 증권투자신탁 |
| check.등록구분 | check.등록구분 | 등록구분 | checkbox | 기업부담금(퇴직금) |
| 목록[].매수비율 | 목록[].매수비율 | 매수비율(%) | number | 35 |
| check.일반금융소비자 | check.일반금융소비자 | 일반금융소비자 | checkbox | 피한정후견인 |
| check.전문금융소비자 | check.전문금융소비자 | 전문금융소비자 | checkbox | 전문금융소비자이나 상품설명을 희망 |
| check.일반금융소비자2 | check.일반금융소비자2 | 일반금융소비자 | checkbox | 전문금융소비자 외 금융소비자 |
| check.전문금융소비자2 | check.전문금융소비자2 | 전문금융소비자 | checkbox | 전문금융소비자이나 상품설명 희망 |
| check.일반금융소비자3 | check.일반금융소비자3 | 일반금융소비자 | checkbox | 일반투자자(투자자정보확인서에서 일반투자자 선택) |
| check.전문금융소비자3 | check.전문금융소비자3 | 전문금융소비자 | checkbox | 전문투자자(투자자정보확인서에서 전문투자자 선택) |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 최숙지 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 금재호 |
| seal.staff.판매직원 | seal.staff.판매직원 | 판매직원 | seal | 검인 |
| sign.staff.판매직원 | sign.staff.판매직원 | 판매직원 | signature | 선수정 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 임건태 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 장기수 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 홍소서 |
| check.약관및상품설명서 | check.약관및상품설명서 | 약관및상품설명서 | checkbox | 알림톡(발송실패시 LMS 발송) |
| handwritten | handwritten | 가입자자필기재 | text | 설명듣고이해함 |
| handwritten2 | handwritten2 | 가입자자필기재 | text | 계약서,약관,상품설명서를수령함 |
| check.전화해피콜 | check.전화해피콜 | 전화(휴대폰)해피콜 | checkbox | 온라인(모바일 웹) 해피콜 |
| handwritten3 | handwritten3 | 가입자자필기재 | text | 설명을듣고이해 |
| signer.name | corp.name | 가입자(기업명) | text | (주)유니온무역 |
| seal.signer | seal.corp | 가입자(기업명) | seal | (주)대한시스템즈 |
| sign.signer | sign.customer | 가입자(기업명) | signature | (주)유니온무역 |
| signer2.name | agent.name | 대리인 | text | 강석호 |
| seal.signer2 | seal.agent | 대리인 | seal | 강석호 |
| sign.signer2 | sign.agent | 대리인 | signature | 이도민 |

### hf179 · 퇴직연금 퇴직급여 지급신청서(DB)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.179 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| customer.name | customer.name | 가입자성명 | text | 박찬연 |
| employer.hire_date | employer.hire_date | 입사일자 | date | 2020.05.08 |
| DB계좌번호 | DB계좌번호 | DB계좌번호 | text | 803-266681-55972 |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| 퇴직일자 | 퇴직일자 | 퇴직일자 | date | 2025년 1월 4일 |
| check.지급형태 | check.지급형태 | 지급형태 | checkbox | IRP이전(의무) |
| check.지급형태2 | check.지급형태2 | 지급형태 | checkbox | 요구불계좌 |
| 예약지급일주1 | 예약지급일주1 | 예약지급일주1 | text |  |
| check.만55세이후퇴직 | check.만55세이후퇴직 | 만55세이후퇴직 | checkbox | 한시적 체류자격 외국인 |
| 퇴직급여총액 | 퇴직급여총액 | 퇴직급여총액 | number | 9,720,000 |
| 지급신청금액 | 지급신청금액 | 지급신청금액 | number | 25,470,000원 |
| check.기업으로반환신청 | check.기업으로반환신청 | (필요시기재)기업으로반환신청 | checkbox | 국민연금전환금 |
| check.지급방식 | check.지급방식 | 지급방식 | checkbox | 전액지급 |
| 금융기관명 | 금융기관명 | 금융기관명 | text | 기업은행 |
| 금융기관명2 | 금융기관명2 | 금융기관명 | text | 농협은행 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| account2 | account2 | 계좌번호 | account_no | 000-287736-52424 |
| 목록[].매도순위 | 목록[].매도순위 | 매도순위 | text |  |
| 목록[].상품명 | 목록[].상품명 | 상품명 | text | 정기예금 (1년) |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 976-032344-29141 |
| 목록[].매도금액 | 목록[].매도금액 | 매도금액(원/좌) | number | 680,000원 |
| check.가입자단독청구 | check.가입자단독청구 | 가입자단독청구 | checkbox | 업체 폐업 |
| 영업점본인확인 | 영업점본인확인 | 영업점본인확인 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 가입자 | text | 박찬연 |
| seal.signer | seal.customer | 가입자 | seal | 박찬연 |
| sign.signer | sign.customer | 가입자 | signature | 강순준 |
| signer2.name | signer2.name | 기업명 | text | (주)유니온무역 |
| seal.signer2 | seal.corp | 기업명 | seal | (주)삼정전자 |
| sign.signer2 | sign.signer2 | 기업명 | signature | (주)유니온무역 |
| signer3.name | signer3.name | 가입자 | text | 박찬연 |
| seal.signer3 | seal.signer3 | 가입자 | seal | 전영경 |
| sign.signer3 | sign.signer3 | 가입자 | signature | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김재수 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이혜현 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이영경 |
| 필수서류 | 필수서류 | 필수서류 | text |  |
| 퇴직소득원천징수영수증 | 퇴직소득원천징수영수증 | 퇴직소득원천징수영수증 | number | 9,590,000원 |
| 타금융기관IRP또는요구불계좌사본 | 타금융기관IRP또는요구불계좌사본 | 타금융기관IRP또는요구불계좌사본 | text | 782-933641-20100 |

### hf180 · DB 적립금 이전 요청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.180 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].이전하는금융회사 | 목록[].이전하는금융회사 | 이전하는금융회사(운용관리기관명) | text | 하나은행 |
| 목록[].운용관리기관명 | 목록[].운용관리기관명 | 운용관리기관명 | text | 하나은행 |
| 목록[].자산관리기관명 | 목록[].자산관리기관명 | 자산관리기관명 | text | 기업은행 |
| 목록[].적립금이전액 | 목록[].적립금이전액 | 적립금이전액* | text | 3,590,000원 |
| 목록[].실물이전여부 | 목록[].실물이전여부 | 실물이전여부 | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 최영빈 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 박혁현 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 기하윤 |

### hf181 · 이전 가입자 명부(DC,기업형 IRP용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.181 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].이전하는금융회사 | 목록[].이전하는금융회사 | 이전하는금융회사(운용관리기관명) | text | 우리은행 |
| 목록[].운용관리기관명자산관리기관명 | 목록[].운용관리기관명자산관리기관명 | 운용관리기관명자산관리기관명 | text | 기업은행 |
| 목록[].성명 | 목록[].성명 | 성명 | text | 표원준 |
| 목록[].주민번호 | 목록[].주민번호 | 주민번호 | text | 598-233590-25329 |
| 목록[].연락처 | 목록[].연락처 | 연락처 | text | 010-5907-7253 |
| 목록[].실물이전여부1현금2실물 | 목록[].실물이전여부1현금2실물 | 실물이전여부1.현금2.실물 | text |  |
| 목록[].서명날인 | 목록[].서명날인 | 서명/날인 | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 구준린 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 정예주 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 고영원 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 강진원 |

### hf182 · 이전신청(취소)서(DB,DC,기업형IRP 이전용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.182 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.신청내용 | check.신청내용 | 신청내용 | checkbox | 이전 신청 |
| check.이전의사확인 | check.이전의사확인 | 이전의사확인* | checkbox | 이전하는 금융회사 방문 |
| check.신청서제출처 | check.신청서제출처 | 신청서제출처 | checkbox | 이전받을 금융회사 |
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자번호 | biz_no | 264-82-36559 |
| 담당자성명 | 담당자성명 | 담당자성명 | text | 박찬연 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| check.제도유형 | check.제도유형 | 제도유형 | checkbox | 기업형IRP |
| check.이전계약 | check.이전계약 | 이전계약 | checkbox | 운용관리계약 |
| check.이전유형 | check.이전유형 | 이전유형 | checkbox | 일부(적립금, 가입자)이전 |
| check.이전대상 | check.이전대상 | 이전대상** | checkbox | 실물 |
| 이전금액 | 이전금액 | 이전금액***(DB일부이전) | number | 42,410,000 |
| 금융회사명 | 금융회사명 | 금융회사명 | text | 국민은행 |
| signer.name | signer.name | 금융기관명:지점명 | text | 변혁영 |
| seal.signer | seal.signer | 금융기관명:지점명 | seal | 변혁영 |
| sign.signer | sign.signer | 금융기관명:지점명 | signature | 신건태 |
| 금융회사명2 | 금융회사명2 | 금융회사명 | text | 우리은행 |
| 관리번호 | 관리번호 | (운용관리기관관리번호)관리번호 | text | 355-138241-50009 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 기업명 | text | (주)유니온무역 |
| seal.signer2 | seal.corp | 기업명 | seal | 주식회사 대성패션 |
| sign.signer2 | sign.customer | 기업명 | signature | (주)유니온무역 |
| signer3.name | signer3.name | 지점명 | text | 박아린 |
| seal.signer3 | seal.signer3 | 지점명 | seal | 금하재 |
| sign.signer3 | sign.signer3 | 지점명 | signature | 박아린 |
| 이전받을기관 | 이전받을기관 | 이전받을기관 | text |  |
| agent.name | agent.name | 대리인 | text | 박영준 |
| 금융기관명 | 금융기관명 | 금융기관명 | text | 기업은행 |
| customer.phone2 | customer.phone2 | 전화번호 | phone | 010-5907-7253 |
| 팩스번호 | 팩스번호 | 팩스번호 | phone | 043-783-2775 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 원우하 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 최기정 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 여순준 |

### hf183 · 퇴직연금 통지서비스 신청서(가입자용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.183 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].은행사용란 | 목록[].은행사용란 | 은행사용란 | text |  |
| customer.name | customer.name | 성명(업체명) | text | 박찬연 |
| customer.birth | customer.birth | 생년월일 | date | 2026년 1월 31일 |
| check.휴대전화 | check.휴대전화 | 휴대전화 | checkbox | SKT  |
| customer.email | customer.email | E-mail주소 | text | chanyeon363@naver.com |
| 자택 | 자택 | 자택 | text |  |
| employer.name | employer.name | 직장 | text | 주식회사 태평양무역 |
| customer.home_phone | customer.home_phone | 자택전화 | phone | 02-1244-9090 |
| employer.phone | employer.phone | 직장전화 | phone | 043-783-2775 |
| check.우편물수령처 | check.우편물수령처 | 우편물수령처 | checkbox | 직장 |
| check.전화연락처 | check.전화연락처 | 전화연락처 | checkbox | 직장 |
| check.년월일 | check.년월일 | 년월일 | checkbox | 고객정보  |
| 필수통지 | 필수통지 | 필수(법적)통지 | text |  |
| 목표수익률에도달하면펀드자동환매 | 목표수익률에도달하면펀드자동환매 | 목표수익률에도달하면펀드자동환매 | text |  |
| check.상승자동환매 | check.상승자동환매 | 상승+%자동환매 | checkbox | 보기2 |
| check.상승자동환매2 | check.상승자동환매2 | 상승+%자동환매 | checkbox | 하락 - % 자동환매 |
| check.상승자동환매3 | check.상승자동환매3 | 상승+%자동환매 | checkbox | 하락 - % 자동환매 |
| check.운용현황보고서발송주기 | check.운용현황보고서발송주기 | 운용현황보고서발송주기(기본값:분기발송) | checkbox | 월 |
| check.원리금보장상품만기도래시전월통지발송 | check.원리금보장상품만기도래시전월통지발송 | 원리금보장상품(정기예금등)만기도래시전월통지발송 | checkbox | 알림톡(LMS) |
| check.퇴직연금운용및자산관리약관이변경되는경우통지 | check.퇴직연금운용및자산관리약관이변경되는경우통지 | 퇴직연금운용및자산관리약관이변경되는경우통지 | checkbox | 수신거부 |
| check.집합투자증권매수시예탁결제원의자산운용보고서수령방법 | check.집합투자증권매수시예탁결제원의자산운용보고서수령방법 | 집합투자증권매수시예탁결제원의자산운용보고서수령방법 | checkbox | 우편(직장→자택) |
| check.목표수익률에도달하면펀드자동환매 | check.목표수익률에도달하면펀드자동환매 | 목표수익률에도달하면펀드자동환매 | checkbox | 해지 |
| check.신청 | check.신청 | 신청(미발송) | checkbox | 신청안함(발송) |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 차유현 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 남욱원 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 금나원 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 박영예 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 허다지 |
| check.AI포트폴리오가입후매1년마다정기적으로리밸런싱을안내 | check.AI포트폴리오가입후매1년마다정기적으로리밸런싱을안내 | AI포트폴리오가입후매1년마다정기적으로리밸런싱을안내 | checkbox | 이메일 |
| check.신청여부 | check.신청여부 | 신청여부 | checkbox | 신청안함 |
| signer.name | signer.name | 가입자 | text | 박찬연 |
| seal.signer | seal.customer | 가입자 | seal | 강순준 |
| sign.signer | sign.customer | 가입자 | signature | 박찬연 |

### hf184 · 퇴직연금 계약해지 신청서(개인형IRP)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.184 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| account | account | 퇴직연금계좌번호 | account_no | 000-287736-52424 |
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| check.일반사유 | check.일반사유 | 일반사유 | checkbox | 일반 중도해지 |
| check.부득이한사유 | check.부득이한사유 | 부득이한사유 | checkbox | 가입자의 사망 |
| 금융기관명 | 금융기관명 | 금융기관명 | text | 하나은행 |
| account2 | account2 | 계좌번호 | account_no | 000-287736-52424 |
| 당해년도납입액 | 당해년도납입액 | 당해년도납입액 | text |  |
| 퇴직금 | 퇴직금 | 퇴직금 | text |  |
| 연금계좌의운용소득 | 연금계좌의운용소득 | 연금계좌의운용소득 | number | 10,740,000 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 현예지 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| 소득공제받은납입금액 | 소득공제받은납입금액 | 소득(세액)공제받은납입금액 | number | 600,000 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 연철찬 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 표용수 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김재예 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 이서태 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김건린 |

### hf185 · 퇴직연금 DC 기업부담금 자동이체 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.185 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 신청 |
| date | date | 이체개시일 | date | 2026년 1월 31일 |
| date2 | date2 | 이체종료일 | date | 2026년 1월 31일 |
| account | account | 출금계좌번호 | account_no | 000-287736-52424 |
| account2 | account2 | 입금계좌번호 | account_no | 000-287736-52424 |
| date3 | date3 | 년월일 | date | 2026년 01월 31일 |
| 목록[].가입자명 | 목록[].가입자명 | 가입자명 | text |  |
| 총가입자수 | 총가입자수 | 총가입자수 | text |  |
| 목록[].생년월일 | 목록[].생년월일 | 생년월일 | text | 2025-09-26 |
| 목록[].이체금액 | 목록[].이체금액 | 이체금액 | number | 63,640,000 |
| 목록[].원 | 목록[].원 | 원 | text | 2,120,000원 |
| 총액 | 총액 | 총액 | number | 18,400,000 |
| date4 | date4 | 작성일 | date | 2026년 1월 31일 |
| seal.signer | seal.customer | 서명또는 | seal | 박찬연 |
| sign.signer | sign.customer | 서명또는 | signature | 강순준 |
| seal.staff.인감대조 | seal.staff.인감대조 | 인감대조 | seal | 손순윤 |
| sign.staff.인감대조 | sign.staff.인감대조 | 인감대조 | signature | 김준민 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 권원은 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 주원호 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김용혜 |

### hf186 · 퇴직연금_거래신청서(DB)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.186 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 회계결산월 | 회계결산월 | 회계결산월 | text |  |
| date | date | 제도시행일 | date | 2026년 1월 31일 |
| 간사기관 | 간사기관 | 간사기관 | text |  |
| 비간사기관 | 비간사기관 | 비간사기관 | text |  |
| 동의미동의 | 동의미동의 | 동의󠇧미동의(현금성자산으로운용) | text |  |
| date2 | date2 | 규약수리통보일 | date | 2026년 1월 31일 |
| customer.name | customer.name | 이름 | text | 박찬연 |
| customer.name2 | customer.name2 | 이름 | text | 박찬연 |
| customer.phone | customer.phone | 휴대폰번호 | phone | 010-5907-7253 |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| customer.birth2 | customer.birth2 | 생년월일 | date | 1990년 2월 10일 |
| customer.email | customer.email | 이메일주소 | text | chanyeon363@naver.com |
| 명미만 | 명미만 | 명미만(명)󠇧 | text |  |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| customer.name3 | customer.name3 | 성명 | text | 박찬연 |
| customer.birth3 | customer.birth3 | 생년월일 | date | 1990년 2월 10일 |
| customer.name4 | customer.name4 | 예금주 | text | 박찬연 |
| 제도가입이후근무분만 | 제도가입이후근무분만 | 제도가입이후근무분만󠇧 | text |  |
| 제도가입이전근무분포함 | 제도가입이전근무분포함 | 제도가입이전근무분포함󠇧 | text |  |
| 비대상 | 비대상 | 비대상󠇧 | text |  |
| 대상타사가입일자 | 대상타사가입일자 | 대상(타사가입일자 | date | 2025.11.10 |
| 비대상2 | 비대상2 | 비대상󠇧 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 김채찬 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 방훈율 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 이민도 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 길훈서 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 명채원 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 위찬영 |
| 가입자수 | 가입자수 | 가입자수 | text |  |
| signer.name | signer.name | 기업명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 기업명 | seal | 주식회사 대성패션 |
| sign.signer | sign.customer | 기업명 | signature | (주)유니온무역 |
| 성명 | 성명 | -성명 | text |  |
| 직원임원촉탁정년초과 | 직원임원촉탁정년초과 | 직원󠇧임원󠇧촉탁󠇧정년초과 | text |  |
| 주민등록번호 | 주민등록번호 | -주민등록번호 | text |  |
| 입사일중간정산일자 | 입사일중간정산일자 | -입사일:-중간정산일자 | text |  |
| 사원번호이메일 | 사원번호이메일 | -사원번호:-이메일:󠇧 | text |  |
| 성명2 | 성명2 | -성명 | text |  |
| 직원임원촉탁정년초과2 | 직원임원촉탁정년초과2 | 직원󠇧임원󠇧촉탁󠇧정년초과 | text |  |
| 주민등록번호2 | 주민등록번호2 | -주민등록번호 | text |  |
| 입사일중간정산일자2 | 입사일중간정산일자2 | -입사일:-중간정산일자 | text |  |
| 사원번호이메일2 | 사원번호이메일2 | -사원번호:-이메일:󠇧 | text |  |
| 성명3 | 성명3 | -성명 | text |  |
| 직원임원촉탁정년초과3 | 직원임원촉탁정년초과3 | 직원󠇧임원󠇧촉탁󠇧정년초과 | text |  |
| 주민등록번호3 | 주민등록번호3 | -주민등록번호 | text |  |
| 입사일중간정산일자3 | 입사일중간정산일자3 | -입사일:-중간정산일자 | text |  |
| 사원번호이메일3 | 사원번호이메일3 | -사원번호:-이메일:󠇧 | text |  |
| 성명4 | 성명4 | -성명 | text |  |
| 직원임원촉탁정년초과4 | 직원임원촉탁정년초과4 | 직원󠇧임원󠇧촉탁󠇧정년초과 | text |  |
| 주민등록번호4 | 주민등록번호4 | -주민등록번호 | text |  |
| 입사일중간정산일자4 | 입사일중간정산일자4 | -입사일:-중간정산일자 | text |  |
| 사원번호이메일4 | 사원번호이메일4 | -사원번호:-이메일:󠇧 | text |  |
| 성명5 | 성명5 | -성명 | text |  |
| 직원임원촉탁정년초과5 | 직원임원촉탁정년초과5 | 직원󠇧임원󠇧촉탁󠇧정년초과 | text |  |
| 주민등록번호5 | 주민등록번호5 | -주민등록번호 | text |  |
| 입사일중간정산일자5 | 입사일중간정산일자5 | -입사일:-중간정산일자 | text |  |
| 사원번호이메일5 | 사원번호이메일5 | -사원번호:-이메일:󠇧 | text |  |
| 성명6 | 성명6 | -성명 | text |  |
| 직원임원촉탁정년초과6 | 직원임원촉탁정년초과6 | 직원󠇧임원󠇧촉탁󠇧정년초과 | text |  |
| 주민등록번호6 | 주민등록번호6 | -주민등록번호 | text |  |
| 입사일중간정산일자6 | 입사일중간정산일자6 | -입사일:-중간정산일자 | text |  |
| 사원번호이메일6 | 사원번호이메일6 | -사원번호:-이메일:󠇧 | text |  |
| 성명7 | 성명7 | -성명 | text |  |
| 직원임원촉탁정년초과7 | 직원임원촉탁정년초과7 | 직원󠇧임원󠇧촉탁󠇧정년초과 | text |  |
| 주민등록번호7 | 주민등록번호7 | -주민등록번호 | text |  |
| 입사일중간정산일자7 | 입사일중간정산일자7 | -입사일:-중간정산일자 | text |  |
| 사원번호이메일7 | 사원번호이메일7 | -사원번호:-이메일:󠇧 | text |  |
| 성명8 | 성명8 | -성명 | text |  |
| 직원임원촉탁정년초과8 | 직원임원촉탁정년초과8 | 직원󠇧임원󠇧촉탁󠇧정년초과 | text |  |
| 주민등록번호8 | 주민등록번호8 | -주민등록번호 | text |  |
| 입사일중간정산일자8 | 입사일중간정산일자8 | -입사일:-중간정산일자 | text |  |
| 사원번호이메일8 | 사원번호이메일8 | -사원번호:-이메일:󠇧 | text |  |
| 성명9 | 성명9 | -성명 | text |  |
| 직원임원촉탁정년초과9 | 직원임원촉탁정년초과9 | 직원󠇧임원󠇧촉탁󠇧정년초과 | text |  |
| 주민등록번호9 | 주민등록번호9 | -주민등록번호 | text |  |
| 입사일중간정산일자9 | 입사일중간정산일자9 | -입사일:-중간정산일자 | text |  |
| 사원번호이메일9 | 사원번호이메일9 | -사원번호:-이메일:󠇧 | text |  |
| 성명10 | 성명10 | -성명 | text |  |
| 직원임원촉탁정년초과10 | 직원임원촉탁정년초과10 | 직원󠇧임원󠇧촉탁󠇧정년초과 | text |  |
| 주민등록번호10 | 주민등록번호10 | -주민등록번호 | text |  |
| 입사일중간정산일자10 | 입사일중간정산일자10 | -입사일:-중간정산일자 | text |  |
| 사원번호이메일10 | 사원번호이메일10 | -사원번호:-이메일:󠇧 | text |  |

### hf188 · 퇴직연금 중도인출신청서(DC,기업형·개인형IRP)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.188 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| check.제도 | check.제도 | 제도 | checkbox | DC |
| employer.hire_date | employer.hire_date | 입사일 | date | 2020.05.08 |
| customer.birth | customer.birth | 생년월일 | date | 1990-02-10 |
| employer.name | employer.name | 계좌번호또는회사명 | text | 주식회사 태평양무역 |
| pension.interim_settlement_date | pension.interim_settlement_date | 중간정산일 | date | 2025년 2월 20일 |
| customer.phone | customer.phone | 휴대전화 | phone | 010-5907-7253 |
| check.신청금액 | check.신청금액 | 신청금액 | checkbox | 일부 |
| check.임원여부 | check.임원여부 | 임원여부 | checkbox | 근로자 |
| check.가입자부담금여부 | check.가입자부담금여부 | 가입자부담금여부 | checkbox | 가입자부담금(적립금) 없음 |
| check.추가부담금입금여부 | check.추가부담금입금여부 | 추가부담금입금여부 | checkbox | 해당사항 없음 |
| check.해당사항있음금액 | check.해당사항있음금액 | 해당사항있음(금액 | checkbox | 연동출금 동의 |
| check.당해연도이전에중간정산한금액이있는경우 | check.당해연도이전에중간정산한금액이있는경우 | 당해연도이전에중간정산(중도인출)한금액이있는경우 | checkbox | 합산과세 적용 |
| check.해당사항없음 | check.해당사항없음 | 해당사항없음 | checkbox | 해당사항 없음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| value | value | [일부신청시유의사항] | amount |  |
| value2 | value2 | [가입자부담금이있는경우유의사항] | amount |  |
| payout.bank | payout.bank | 금융기관명 | text | 하나은행 |
| customer.name2 | customer.name2 | 예금주 | text | 박찬연 |
| date2 | date2 | 작성일(년월일) | date | 2026년 01월 31일 |
| pension.withdraw_amount | pension.withdraw_amount | 신청금액일부(원) | amount | 201,920,000원 |
| pension.extra_contribution | pension.extra_contribution | 추가부담금해당사항있음금액(원) | number | 198,920,000원 |
| payout.account | payout.account | 입금계좌계좌번호 | account_no | 000-287736-52424 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 조희승 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 황보용수 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 선우철진 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김순연 |
| sell_list[].order | sell_list[].order | 매도순위 | number | 1 |
| sell_list[].product | sell_list[].product | 상품명 | text | 정기예금 (3년) |
| sell_list[].account | sell_list[].account | 계좌번호 | account_no | 679-024147-48445 |
| sell_list[].amount | sell_list[].amount | 매도금액(원/좌) | amount | 153,660,000 |
| check.무주택자인가입자가본인명 | check.무주택자인가입자가본인명 | 무주택자인가입자가본인명의로주택구입하는경우 | checkbox | 무주택자인 가입자가 본인 명의로 주택 구입하는 경우 |
| check.무주택자인가입자의주거목 | check.무주택자인가입자의주거목 | 무주택자인가입자의주거목적의전세금(임차보증금)부담하는경우 | checkbox | 무주택자인 가입자의 주거 목적의 전세금(임차보증금) 부담하는 경우 |
| check.개월이상요양을필요로하는 | check.개월이상요양을필요로하는 | 개월이상요양을필요로하는본인또는부양가족(배우자의부양가족포함 | checkbox | 개월 이상 요양을 필요로 하는 본인 또는 부양가족(배우자의 부양가족 포함 |
| check.년이내에채무자회생및파 | check.년이내에채무자회생및파 | 년이내에「채무자회생및파산에관한법률」에따라파산선고를받은 | checkbox | 년 이내에 「채무자 회생 및 파산에 관한 법률」에 따라 파산선고를 받은  |
| check.년이내에채무자회생및파2 | check.년이내에채무자회생및파2 | 년이내에「채무자회생및파산에관한법률」에따라개인회생절차개시 | checkbox | 년 이내에 「채무자 회생 및 파산에 관한 법률」에 따라 개인회생절차 개시 |
| check.가입자가입자의배우자또는 | check.가입자가입자의배우자또는 | 가입자,가입자의배우자또는부양가족이「재난및안전관리기본법」에따 | checkbox | 가입자, 가입자의 배우자 또는 부양가족이 「재난 및 안전관리기본법」에 따 |
| check.퇴직급여를담보로제공하여 | check.퇴직급여를담보로제공하여 | 퇴직급여를담보로제공하여대출을받은가입자가그대출상환을하기위한 | checkbox | 퇴직급여를 담보로 제공하여 대출을 받은 가입자가 그 대출상환을 하기 위한 |
| value3 | value3 | [무주택서약서] | amount |  |
| customer.name3 | customer.name3 | 가입자 | text | 박찬연 |
| customer.name4 | customer.name4 | 가입자 | text | 박찬연 |
| customer.name5 | customer.name5 | 가입자 | text | 박찬연 |
| customer.name6 | customer.name6 | 가입자 | text | 박찬연 |
| customer.name7 | customer.name7 | 가입자 | text | 박찬연 |
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| customer.name8 | customer.name8 | 가입자 | text | 박찬연 |
| pension.household_contract_reason | pension.household_contract_reason | 세대원명의계약사유 | text | 계좌 정리 |
| check.신청시기 | check.신청시기 | 신청시기 | checkbox | 계약 체결일로부터 소유권 이전 등기 후 1개월 이내 |
| check.공통서류 | check.공통서류 | 공통서류 | checkbox | 현거주지의 등기사항전부증명서-건물 또는 건축물관리대장 또는 무허가건물확인 |
| check.주택매매 | check.주택매매 | 주택매매 | checkbox | 매수할 부동산의 등기사항전부증명서-건물 또는 건축물관리대장 (1개월 이내 |
| check.분양분양전환 | check.분양분양전환 | 분양/분양전환 | checkbox | 분양(공급) 계약서 (동/호수 배정, 권리의무 승계 내역 포함한 계약서  |
| check.분양권매수 | check.분양권매수 | 분양권매수 | checkbox | 주택분양(공급)계약서 및 분양권 매매계약서 (동/호수 배정, 권리의무 승 |
| check.주택청약당첨 | check.주택청약당첨 | 주택청약당첨 | checkbox | 당첨자 확인서류 |
| check.주택신축 | check.주택신축 | 주택신축 | checkbox | 건축설계서 |
| check.경매취득 | check.경매취득 | 경매취득 | checkbox | 대금지급기한통지서 |
| check.오피스텔 | check.오피스텔 | 오피스텔 | checkbox | 건축물관리대장 –건물 용도 |
| check.소유권이전후 | check.소유권이전후 | 소유권이전후 | checkbox | 소유권 이전 완료 된 등기사항전부증명서-건물 또는 건축물관리대장 (1개월 |
| check.신청시기2 | check.신청시기2 | 신청시기 | checkbox | 주택임대차계약 체결일로부터 잔금 지급일 이후 1개월 이내 |
| check.공통서류2 | check.공통서류2 | 공통서류 | checkbox | 현거주지의 등기사항전부증명서-건물 또는 건축물관리대장 또는 무주택확인원  |
| check.연장 | check.연장 | 연장 | checkbox | 연장 전/후 전(월)세 임대차 계약서 (부동산 중개인을 통한 거래 ) |
| check.주택이외 | check.주택이외 | 주택이외 | checkbox | 전입 후 주민등록등본 ( 임차부동산 전입신고 후 신청 가능) |
| check.잔금지급후 | check.잔금지급후 | 잔금지급후 | checkbox | 잔금 입금증 (수기 영수증 제외) |
| check.신청시기3 | check.신청시기3 | 신청시기 | checkbox | 요양 중이거나 요양 종료일로부터 1개월 이내 |
| check.요양필요확인서류 | check.요양필요확인서류 | 요양필요확인서류 | checkbox | 중도인출신청서 (회사 명판 및 거래인감 날인, 가입자 날인) , 가입자  |
| check.의료비지출확인서류 | check.의료비지출확인서류 | 의료비지출확인서류 | checkbox | 의료기관 등에서 발급한 영수증, 진료비 청구서, 진료비 납입확인서, 진료 |
| check.연간임금총액확인서류 | check.연간임금총액확인서류 | 연간임금총액확인서류 | checkbox | 가입자의 직전연도 근로소득원천징수영수증 또는 급여명세서 |
| check.배우자또는부양가족요양비용의경우확인서류 | check.배우자또는부양가족요양비용의경우확인서류 | 배우자또는부양가족요양비용의경우확인서류 | checkbox | 주민등록등본 또는 가족관계증명서 (1개월 이내) |
| check.신청시기4 | check.신청시기4 | 신청시기 | checkbox | 신청일 기준 개인회생 개시결정일로부터 5년 이내 |
| check.필요서류 | check.필요서류 | 필요서류 | checkbox | 중도인출신청서 (회사 명판 및 거래인감 날인, 가입자 날인) , 가입자  |
| check.신청시기5 | check.신청시기5 | 신청시기 | checkbox | 신청일 기준 파산 선고일로부터 5년 이내 |
| check.필요서류2 | check.필요서류2 | 필요서류 | checkbox | 중도인출신청서 (회사 명판 및 거래인감 날인, 가입자 날인) , 가입자  |
| check.과세제외및환급신청서 | check.과세제외및환급신청서 | 과세제외및환급신청서 | checkbox | 금융거래정보제공서 (연합회한도 조회용) |
| check.신청시기6 | check.신청시기6 | 신청시기 | checkbox | 피해발생일로부터 3개월 이내 |
| check.물적피해 | check.물적피해 | 물적피해 | checkbox | 등기사항전부증명서-건물 (임차의 경우 임대차계약서 포함) |
| check.인적피해 | check.인적피해 | 인적피해 | checkbox | 중도인출신청서 (회사 명판 및 거래인감 날인, 가입자 날인) , 가입자  |
| check.배우자또는부양가족재난의경우확인서류 | check.배우자또는부양가족재난의경우확인서류 | 배우자또는부양가족재난의경우확인서류 | checkbox | 주민등록등본 또는 가족관계증명서 (1개월 이내) |

### hf189 · 퇴직연금 부담금 등록 신청서(DC,기업형IRP)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.189 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| account | account | 퇴직연금계좌번호 | account_no | 000-287736-52424 |
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 취소 |
| check.부담금종류 | check.부담금종류 | 부담금종류 | checkbox | 잔여부담금(퇴직정산 후 부족액) |
| 부담금등록가입자수 | 부담금등록가입자수 | 부담금등록가입자수 | number | 6 |
| check.납부방법 | check.납부방법 | 납부방법 | checkbox | 예약연동납부 [예약일 |
| check.부담금등록구분 | check.부담금등록구분 | 부담금등록구분 | checkbox | 개별 신청 |
| 목록[].성명 | 목록[].성명 | 성명 | text | 김혁예 |
| 목록[].생년월일주1 | 목록[].생년월일주1 | 생년월일주1 | text | 2025-05-02 |
| 목록[].기업부담금 | 목록[].기업부담금 | 기업부담금 | text | 190,000 |
| 목록[].개인부담금 | 목록[].개인부담금 | 개인부담금 | text | 15,180,000 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 기업명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 기업명 | seal | 주식회사 대성패션 |
| sign.signer | sign.customer | 기업명 | signature | (주)유니온무역 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김철유 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 서은경 |

### hf191 · 퇴직연금 계약해지 신청서(DB,DC)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.191 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| account | account | 퇴직연금계좌번호 | account_no | 000-287736-52424 |
| check.제도 | check.제도 | 제도 | checkbox | DC |
| 해지사유 | 해지사유 | 해지사유 | text | 결혼자금 |
| check.해지사유 | check.해지사유 | 해지사유 | checkbox | 사업장의 인수합병 |
| check.수수료연동출금 | check.수수료연동출금 | 수수료연동출금**(DC형만해당) | checkbox | 연동출금 미동의(기업별도입금) |
| 목록[].성명 | 목록[].성명 | 성명 | text | 김재희 |
| check.개인형IRP | check.개인형IRP | 개인형IRP | checkbox | 요구불계좌 |
| 금융기관명 | 금융기관명 | 금융기관명 | text | 카카오뱅크 |
| account2 | account2 | 계좌번호 | account_no | 000-287736-52424 |
| check.개인형IRP2 | check.개인형IRP2 | 개인형IRP | checkbox | 요구불계좌 |
| 금융기관명2 | 금융기관명2 | 금융기관명 | text | 농협은행 |
| account3 | account3 | 계좌번호 | account_no | 000-287736-52424 |
| signer.name | customer.name | 성명 | text | 박찬연 |
| seal.signer | seal.customer | 성명 | seal | 현예지 |
| sign.signer | sign.customer | 성명 | signature | 박찬연 |
| 목록[].서명또는 | 목록[].서명또는 | 서명또는(인) | text |  |
| signer2.name | signer2.name | 성명 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 성명 | seal | 강순준 |
| sign.signer2 | sign.signer2 | 성명 | signature | 이민빈 |
| check.만55세이후퇴직 | check.만55세이후퇴직 | 만55세이후퇴직 | checkbox | 만55세이후 퇴직 |
| check.만55세이후퇴직2 | check.만55세이후퇴직2 | 만55세이후퇴직 | checkbox | 만55세이후 퇴직 |
| 목록[].생년월일 | 목록[].생년월일 | 생년월일 | date | 2025-06-28 |
| 목록[].입사일자 | 목록[].입사일자 | 입사일자 | date | 2025.12.15 |
| 목록[].잔여부담금 | 목록[].잔여부담금 | 잔여부담금(DC형만기재) | number | 8,240,000 |
| check.기업반환 | check.기업반환 | 기업반환(기업반환계좌로반환) | checkbox | 퇴직소득세 |
| check.기업반환2 | check.기업반환2 | 기업반환(기업반환계좌로반환) | checkbox | 퇴직소득세 |
| 목록[].중간정산일자 | 목록[].중간정산일자 | 중간정산일자 | date | 2025-11-12 |
| check.적용 | check.적용 | 적용 | checkbox | 미적용 |
| check.적용2 | check.적용2 | 적용 | checkbox | 적용 |
| 목록[].퇴직일자 | 목록[].퇴직일자 | 퇴직일자 | date | 2025년 4월 19일 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer3.name | signer3.name | 기업명 | text | (주)유니온무역 |
| seal.signer3 | seal.corp | 기업명 | seal | (주)유니온무역 |
| sign.signer3 | sign.signer3 | 기업명 | signature | 주식회사 한빛패션 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 확인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 이나린 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 최채빈 |

### hf192 · 퇴직연금 통지서비스 신청서(기업용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.192 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| check.제도구분 | check.제도구분 | 제도구분 | checkbox | DC |
| 주담당자 | 주담당자 | 주담당자 | text | 전숙윤 |
| 부담당자 | 부담당자 | 부담당자 | text | 박형태 |
| 목록[].휴대폰번호 | 목록[].휴대폰번호 | 휴대폰번호 | phone | 010-5907-7253 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| account | account | 퇴직연금계좌번호 | account_no | 000-287736-52424 |
| 목록[].이메일주소 | 목록[].이메일주소 | 이메일주소 | text | chanyeon363@naver.com |
| check.상승자동환매 | check.상승자동환매 | 상승+%자동환매 | checkbox | 보기2 |
| check.상승자동환매2 | check.상승자동환매2 | 상승+%자동환매 | checkbox | 보기2 |
| check.상승자동환매3 | check.상승자동환매3 | 상승+%자동환매 | checkbox | 하락 - % 자동환매 |
| check.운용현황보고서발송주기 | check.운용현황보고서발송주기 | 운용현황보고서발송주기(기본값:분기발송) | checkbox | 분기 |
| check.원리금보장상품만기도래시전월통지발송 | check.원리금보장상품만기도래시전월통지발송 | 원리금보장상품(정기예금등)만기도래시전월통지발송 | checkbox | 알림톡(LMS) |
| check.퇴직연금운용및자산관리약관이변경되는경우통지 | check.퇴직연금운용및자산관리약관이변경되는경우통지 | 퇴직연금운용및자산관리약관이변경되는경우통지 | checkbox | 이메일 |
| check.집합투자증권매수시예탁결제원의자산운용보고서수령방법 | check.집합투자증권매수시예탁결제원의자산운용보고서수령방법 | 집합투자증권매수시예탁결제원의자산운용보고서수령방법 | checkbox | 우편 |
| check.신청안함 | check.신청안함 | 신청안함 | checkbox | 알림톡(LMS) |
| check.매월말전체적립금에대한운용내역을익월초통지 | check.매월말전체적립금에대한운용내역을익월초통지 | 매월말전체적립금에대한운용내역을익월초통지 | checkbox | 알림톡(LMS) |
| check.목표수익률에도달하면펀드자동환매 | check.목표수익률에도달하면펀드자동환매 | 목표수익률에도달하면펀드자동환매 | checkbox | 해지 |
| check.신청 | check.신청 | 신청(미발송) | checkbox | 신청(미발송) |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 기업명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 기업명 | seal | (주)유니온무역 |
| sign.signer | sign.customer | 기업명 | signature | 주식회사 한빛패션 |
| 목표수익률에도달하면펀드자동환매 | 목표수익률에도달하면펀드자동환매 | 목표수익률에도달하면펀드자동환매 | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 배예윤 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 표영원 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 백민연 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 류희혜 |
| 거래내용 | 거래내용 | 거래내용 | text | 해당 없음 |

### hf193 · 퇴직연금 계약해지 신청서(기업형IRP)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.193 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 서류확인및접수확인자 | 서류확인및접수확인자 | 서류확인및접수확인자 | text |  |
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| account | account | 퇴직연금계좌번호 | account_no | 000-287736-52424 |
| check.해지사유 | check.해지사유 | 해지사유 | checkbox | 제도폐지 |
| check.수수료연동출금 | check.수수료연동출금 | 수수료연동출금** | checkbox | 연동출금 미동의(기업별도입금) |
| customer.name | customer.name | 성명 | text | 박찬연 |
| check.개인형IRP | check.개인형IRP | 개인형IRP | checkbox | 요구불계좌 |
| 금융기관명 | 금융기관명 | 금융기관명 | text | 국민은행 |
| account2 | account2 | 계좌번호 | account_no | 000-287736-52424 |
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| check.만55세이후퇴직 | check.만55세이후퇴직 | 만55세이후퇴직 | checkbox | 만원 이하 퇴직금 지급 |
| employer.hire_date | employer.hire_date | 입사일자 | date | 2020.05.08 |
| 중간정산일자 | 중간정산일자 | 중간정산일자 | date | 2025.07.31 |
| 잔여부담금 | 잔여부담금 | 잔여부담금 | number | 5,130,000 |
| check.계좌번호 | check.계좌번호 | 계좌번호 | checkbox | 계속근로기관 1년 미만 |
| 퇴직일자 | 퇴직일자 | 퇴직일자 | date | 2025-01-26 |
| check.적용 | check.적용 | 적용 | checkbox | 적용 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 기업명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 기업명 | seal | 주식회사 한빛패션 |
| sign.signer | sign.customer | 기업명 | signature | (주)유니온무역 |
| signer2.name | signer2.name | 가입자 | text | 박찬연 |
| seal.signer2 | seal.customer | 가입자 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 가입자 | signature | 이민빈 |

### hf194 · 퇴직연금 항목등록/변경 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.194 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명(업체명) | text | 박찬연 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| customer.birth | customer.birth | 생년월일(사업자번호) | date | 1990.02.10 |
| check.제도구분 | check.제도구분 | 제도구분 | checkbox | 개인형IRP |
| 변경전 | 변경전 | 변경전 | text | 해당 없음 |
| check.구분 | check.구분 | 구분 | checkbox | 해제 |
| check.공통사항 | check.공통사항 | 공통사항 | checkbox | 부담금 납입주기 변경 |
| check.DB | check.DB | DB | checkbox | 대체상품 매수 동의 |
| check.DC기업형IRP | check.DC기업형IRP | DC/기업형IRP | checkbox | 임금총액 등록 |
| check.공통사항2 | check.공통사항2 | 공통사항 | checkbox | 퇴직연금정보 제3수령처 등록 |
| check.개인형IRP | check.개인형IRP | 개인형IRP | checkbox | 개인형IRP 속성 변경 |
| 변경후 | 변경후 | 변경후 | text | 해당 없음 |
| check.구분2 | check.구분2 | 구분 | checkbox | 변경 |
| customer.name2 | customer.name2 | 성명 | text | 박찬연 |
| customer.birth2 | customer.birth2 | 생년월일 | date | 1990.02.10 |
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 해제 |
| customer.name3 | customer.name3 | 성명 | text | 박찬연 |
| customer.phone | customer.phone | 휴대폰번호 | phone | 010-5907-7253 |
| check.담당자구분 | check.담당자구분 | 담당자구분 | checkbox | 주담당자 |
| customer.birth3 | customer.birth3 | 생년월일 | date | 1990.02.10 |
| customer.email | customer.email | 이메일주소 | text | chanyeon363@naver.com |
| 기업담당자성명 | 기업담당자성명 | 기업담당자성명 | text | 김용승 |
| 기업담당자휴대폰번호 | 기업담당자휴대폰번호 | 기업담당자휴대폰번호 | phone | 010-5907-7253 |
| 근로자앞문자발송요청일 | 근로자앞문자발송요청일 | 근로자앞문자발송요청일 | date | 2025-05-19 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 강순준 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 양승진 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 도성은 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 최석우 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 송민은 |

### hf195 · 퇴직연금 가입자(등록·변경·삭제) 신청서(DB,DC,기업형IRP)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.195 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| check.퇴직연금가입제도 | check.퇴직연금가입제도 | 퇴직연금가입제도 | checkbox | DB |
| account | account | 퇴직연금계좌번호 | account_no | 000-287736-52424 |
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 등록 |
| check.신청구분2 | check.신청구분2 | 신청구분 | checkbox | 변경 |
| 가입자수 | 가입자수 | 가입자수 | text |  |
| check.가입자 | check.가입자 | 가입자 | checkbox | 가입자 |
| check.가입자등록구분 | check.가입자등록구분 | 가입자등록구분 | checkbox | 일괄(파일) 신청 |
| 가입자명부산정기준일자 | 가입자명부산정기준일자 | 가입자명부산정기준일자 | date | 2025년 2월 18일 |
| check.기준급여원 | check.기준급여원 | 기준급여:원 | checkbox | 촉탁 |
| check.기준급여원2 | check.기준급여원2 | 기준급여:원 | checkbox | 임원 |
| check.기준급여원3 | check.기준급여원3 | 기준급여:원 | checkbox | 촉탁 |
| check.기준급여원4 | check.기준급여원4 | 기준급여:원 | checkbox | 임원 |
| check.기준급여원5 | check.기준급여원5 | 기준급여:원 | checkbox | 정년초과 |
| check.직원 | check.직원 | 직원 | checkbox | 직원 |
| check.직원2 | check.직원2 | 직원 | checkbox | 임원 |
| check.직원3 | check.직원3 | 직원 | checkbox | 임원 |
| check.직원4 | check.직원4 | 직원 | checkbox | 임원 |
| check.직원5 | check.직원5 | 직원 | checkbox | 직원 |
| check.퇴직일전환일사유 | check.퇴직일전환일사유 | 퇴직일/전환일:사유 | checkbox | 선지급(회사지급) |
| check.퇴직일전환일사유2 | check.퇴직일전환일사유2 | 퇴직일/전환일:사유 | checkbox | 근속기간1년미만(DB) |
| check.퇴직일전환일사유3 | check.퇴직일전환일사유3 | 퇴직일/전환일:사유 | checkbox | 무급부(대표지급)(DB) |
| check.퇴직일전환일사유4 | check.퇴직일전환일사유4 | 퇴직일/전환일:사유 | checkbox | 선지급(회사지급) |
| check.퇴직일전환일사유5 | check.퇴직일전환일사유5 | 퇴직일/전환일:사유 | checkbox | 기타( |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| 사원번호 | 사원번호 | 사원번호 | text | 752-562926-86438 |
| customer.name2 | customer.name2 | 성명 | text | 박찬연 |
| customer.rrn2 | customer.rrn2 | 주민등록번호 | rrn | 900210-1659382 |
| 사원번호2 | 사원번호2 | 사원번호 | text | 395643-1020752 |
| customer.name3 | customer.name3 | 성명 | text | 박찬연 |
| customer.rrn3 | customer.rrn3 | 주민등록번호 | rrn | 900210-1659382 |
| 사원번호3 | 사원번호3 | 사원번호 | text | 656596-4187378 |
| customer.name4 | customer.name4 | 성명 | text | 박찬연 |
| customer.rrn4 | customer.rrn4 | 주민등록번호 | rrn | 900210-1659382 |
| 사원번호4 | 사원번호4 | 사원번호 | text | 869-562922-36609 |
| customer.name5 | customer.name5 | 성명 | text | 박찬연 |
| customer.rrn5 | customer.rrn5 | 주민등록번호 | rrn | 900210-1659382 |
| 사원번호5 | 사원번호5 | 사원번호 | text | 7606-4272 |
| signer.name | signer.name | 기업명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 기업명 | seal | (주)유니온무역 |
| sign.signer | sign.customer | 기업명 | signature | (주)삼정전자 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 변규경 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 임승혜 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 염영예 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 금동경 |

### hf196 · 기업형IRP 가입대상 근로자 확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.196 (퇴직연금) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 기업명 | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자번호 | biz_no | 264-82-36559 |
| 상시근로자수 | 상시근로자수 | (A)상시근로자수 | number | 6 |
| 명 | 명 | 명 | number | 2 |
| 기업형IRP가입대상근로자수 | 기업형IRP가입대상근로자수 | (C)=(A)-(B)기업형IRP가입대상근로자수 | number | 3 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 기업명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 기업명 | seal | 주식회사 대성패션 |
| sign.signer | sign.customer | 기업명 | signature | (주)유니온무역 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 정수희 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 차진율 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 방찬윤 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 확인 |

### hf381 · 장외파생상품 일반투자자 (부)적정성 판단보고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.381 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 고객명 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일및나이 | date | 900210 |
| 고객유형 | 고객유형 | 고객유형 | text |  |
| 미성년자고령초고령구분 | 미성년자고령초고령구분 | 미성년자/고령/초고령구분 | text |  |
| check.예 | check.예 | 예 | checkbox | 보기1 |
| check.예2 | check.예2 | 예 | checkbox | 보기1 |
| check.예3 | check.예3 | 예 | checkbox | 보기1 |
| check.예4 | check.예4 | 예 | checkbox | 보기1 |
| check.하 | check.하 | 하 | checkbox | 보기1 |
| check.5미만 | check.5미만 | 5%미만 | checkbox | 보기1 |
| check.년미만 | check.년미만 | 년미만 | checkbox | 보기1 |
| check.아니오 | check.아니오 | 아니오 | checkbox | 보기1 |
| check.아니오2 | check.아니오2 | 아니오 | checkbox | 보기1 |
| check.아니오3 | check.아니오3 | 아니오 | checkbox | 보기1 |
| check.아니오4 | check.아니오4 | 아니오 | checkbox | 보기1 |
| check.중 | check.중 | 중 | checkbox | 보기1 |
| check.10미만 | check.10미만 | 10%미만 | checkbox | 보기1 |
| check.년미만2 | check.년미만2 | 년미만 | checkbox | 보기1 |
| check.상 | check.상 | 상 | checkbox | 보기1 |
| check.10이상 | check.10이상 | 10%이상 | checkbox | 보기1 |
| check.년이상 | check.년이상 | 년이상 | checkbox | 보기1 |
| 고객등급 | 고객등급 | 고객등급 | text |  |
| 거래가능상품의위험등급 | 거래가능상품의위험등급 | 거래가능상품의위험등급 | text | 하나 TDF 2040 |
| 거래목적위험회피목적여부 | 거래목적위험회피목적여부 | 거래목적-위험회피목적여부 | text | 사업자금 |
| 위험의속성및규모에따른적합여부 | 위험의속성및규모에따른적합여부 | 위험의속성및규모에따른적합여부 | text |  |
| 장외파생상품에대한지식보유정도 | 장외파생상품에대한지식보유정도 | 장외파생상품에대한지식보유정도 | text | 하나 TDF 2040 |
| 장외파생상품을취득처분한경험 | 장외파생상품을취득처분한경험 | 장외파생상품을취득·처분한경험 | text | 하나 TDF 2040 |
| check.적정 | check.적정 | 적정 | checkbox | 보기1 |
| check.부적정 | check.부적정 | 부적정 | checkbox | 보기1 |
| check.미충족항목존재 | check.미충족항목존재 | 미충족항목존재 | checkbox | 보기1 |
| check.상품위험등급대비고객등급미달 | check.상품위험등급대비고객등급미달 | 상품위험등급대비고객등급미달 | checkbox | 보기1 |
| check.충족 | check.충족 | 충족 | checkbox | 보기1 |
| check.충족2 | check.충족2 | 충족 | checkbox | 보기1 |
| check.충족3 | check.충족3 | 충족 | checkbox | 보기1 |
| check.충족4 | check.충족4 | 충족 | checkbox | 보기1 |
| check.미충족 | check.미충족 | 미충족 | checkbox | 보기1 |
| check.미충족2 | check.미충족2 | 미충족 | checkbox | 보기1 |
| check.미충족3 | check.미충족3 | 미충족 | checkbox | 보기1 |
| check.미충족4 | check.미충족4 | 미충족 | checkbox | 보기1 |
| 항목점수 | 항목점수 | 항목점수 | text |  |
| 거래목적위험회피목적여부2 | 거래목적위험회피목적여부2 | 거래목적-위험회피목적여부 | text | 자녀 교육비 |
| customer.name2 | customer.name2 | 고객명 | text | 박찬연 |
| agent.name | agent.name | 대리인 | text | 박영준 |
| 담당자 | 담당자 | 담당자(파생상품투자권유자문인력) | text | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |

### hf382 · 장외파생상품 일반투자자 투자자정보 분석결과표

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.382 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 고객명 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일및나이 | date | 1990-02-10 |
| 고객유형 | 고객유형 | 고객유형 | text |  |
| 미성년자고령초고령구분 | 미성년자고령초고령구분 | 미성년자/고령/초고령구분 | text |  |
| check.예 | check.예 | 예 | checkbox | 보기1 |
| check.예2 | check.예2 | 예 | checkbox | 보기1 |
| check.예3 | check.예3 | 예 | checkbox | 보기1 |
| check.예4 | check.예4 | 예 | checkbox | 보기1 |
| check.하 | check.하 | 하 | checkbox | 보기1 |
| check.5미만 | check.5미만 | 5%미만 | checkbox | 보기1 |
| check.년미만 | check.년미만 | 년미만 | checkbox | 보기1 |
| check.아니오 | check.아니오 | 아니오 | checkbox | 보기1 |
| check.아니오2 | check.아니오2 | 아니오 | checkbox | 보기1 |
| check.아니오3 | check.아니오3 | 아니오 | checkbox | 보기1 |
| check.아니오4 | check.아니오4 | 아니오 | checkbox | 보기1 |
| check.중 | check.중 | 중 | checkbox | 보기1 |
| check.10미만 | check.10미만 | 10%미만 | checkbox | 보기1 |
| check.년미만2 | check.년미만2 | 년미만 | checkbox | 보기1 |
| check.상 | check.상 | 상 | checkbox | 보기1 |
| check.10이상 | check.10이상 | 10%이상 | checkbox | 보기1 |
| check.년이상 | check.년이상 | 년이상 | checkbox | 보기1 |
| 고객등급 | 고객등급 | 고객등급 | text |  |
| 거래가능상품의위험등급 | 거래가능상품의위험등급 | 거래가능상품의위험등급 | text | 하나 정기예금 |
| 거래목적위험회피목적여부 | 거래목적위험회피목적여부 | 거래목적-위험회피목적여부 | text | 학자금 |
| 위험의속성및규모에따른적합여부 | 위험의속성및규모에따른적합여부 | 위험의속성및규모에따른적합여부 | text |  |
| 장외파생상품에대한지식보유정도 | 장외파생상품에대한지식보유정도 | 장외파생상품에대한지식보유정도 | text | 하나 TDF 2040 |
| 장외파생상품을취득처분한경험 | 장외파생상품을취득처분한경험 | 장외파생상품을취득·처분한경험 | text | 하나 단기채 펀드 |
| customer.name2 | customer.name2 | 고객명 | text | 박찬연 |
| agent.name | agent.name | 대리인 | text | 박영준 |
| 담당자 | 담당자 | 담당자(파생상품투자권유자문인력) | text | 정옥지 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |

### hf383 · 장외파생상품 투자성향에 적정하지 않은 거래확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.383 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 고객등급 | 고객등급 | 고객등급 | text |  |
| 거래가능상품의위험등급 | 거래가능상품의위험등급 | 거래가능상품의위험등급 | text | 하나 정기예금 |
| 거래희망상품명 | 거래희망상품명 | 거래희망상품명 | text | 하나 단기채 펀드 |
| 거래희망상품의위험등급 | 거래희망상품의위험등급 | 거래희망상품의위험등급 | text | 하나 TDF 2040 |
| customer.name | customer.name | 본인 | text | 박찬연 |
| customer.name2 | customer.name2 | 고객명 | text | 박찬연 |
| agent.name | agent.name | 대리인 | text | 박영준 |
| 담당자 | 담당자 | 담당자(파생상품투자권유자문인력) | text | 정혁유 |
| 영업점장 | 영업점장 | 영업점장(파생상품영업관리자) | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |

### hf384 · 장외파생상품 일반투자자 투자자정보 확인서(법인 및 개인사업자 고객용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.384 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.비상장기업 | check.비상장기업 | 비상장기업 | checkbox | 보기1 |
| 상장거래소명 | 상장거래소명 | 상장거래소명 | text |  |
| 상장거래소명2 | 상장거래소명2 | 상장거래소명 | text |  |
| 종목코드 | 종목코드 | 종목코드 | number | 38747 |
| check.선택 | check.선택 | 선택 | checkbox | 생년월일 및 나이 |
| 자산총계 | 자산총계 | 자산총계 | text |  |
| 부채총계 | 부채총계 | 부채총계 | text |  |
| check.보기1 | check.보기1 | 보기1 | checkbox | 보기1 |
| check. | check. | □ | checkbox | □ |
| check[] | check[] | □ | checkbox | □ |
| check.보기12 | check.보기12 | 보기1 | checkbox | 보기1 |
| check.보기13 | check.보기13 | 보기1 | checkbox | 보기1 |
| check.보기14 | check.보기14 | 보기1 | checkbox | 보기1 |
| check.선택2 | check.선택2 | 선택 | checkbox | □ |
| check.개월이하 | check.개월이하 | 개월이하 | checkbox | □ |
| check.개월이하2 | check.개월이하2 | 개월이하 | checkbox | □ |
| check.년이하 | check.년이하 | 년이하 | checkbox | □ |
| check.보기15 | check.보기15 | 보기1 | checkbox | 보기1 |
| 하금융투자상품에투자해본경험이없음 | 하금융투자상품에투자해본경험이없음 | 하:금융투자상품에투자해본경험이없음 | text | 하나 MMF |
| employer.department | employer.department | 소속부서 | text | 구매팀 |
| 관련경력 | 관련경력 | 관련경력 | text |  |
| employer.position | employer.position | 직급 | text | 대리 |
| 관련자격 | 관련자격 | 관련자격 | text |  |
| customer.name | customer.name | 성명 | text | 박찬연 |
| check.보기16 | check.보기16 | 보기1 | checkbox | 보기1 |
| check.보기17 | check.보기17 | 보기1 | checkbox | 보기1 |
| check.하금융투자상품에투자해본경험이없음 | check.하금융투자상품에투자해본경험이없음 | 하:금융투자상품에투자해본경험이없음 | checkbox | 보기1 |
| 하금융투자상품에투자해본경험이없음2 | 하금융투자상품에투자해본경험이없음2 | 하:금융투자상품에투자해본경험이없음 | text | 하나 MMF |
| employer.department2 | employer.department2 | 소속부서 | text | 구매팀 |
| 관련경력2 | 관련경력2 | 관련경력 | text |  |
| employer.position2 | employer.position2 | 직급 | text | 대리 |
| 관련자격2 | 관련자격2 | 관련자격 | text |  |
| customer.name2 | customer.name2 | 성명 | text | 박찬연 |
| check.보기18 | check.보기18 | 보기1 | checkbox | 보기1 |
| check.보기19 | check.보기19 | 보기1 | checkbox | 보기1 |
| check.하금융투자상품에투자해본경험이없음2 | check.하금융투자상품에투자해본경험이없음2 | 하:금융투자상품에투자해본경험이없음 | checkbox | 보기1 |
| check.보기110 | check.보기110 | 보기1 | checkbox | 보기1 |
| check.보기111 | check.보기111 | 보기1 | checkbox | 보기1 |
| check.보기112 | check.보기112 | 보기1 | checkbox | 보기1 |
| check.보기113 | check.보기113 | 보기1 | checkbox | 보기1 |
| check.보기114 | check.보기114 | 보기1 | checkbox | 보기1 |
| check.보기115 | check.보기115 | 보기1 | checkbox | 보기1 |
| check.보기116 | check.보기116 | 보기1 | checkbox | 보기1 |
| check.보기117 | check.보기117 | 보기1 | checkbox | 보기1 |
| check.보기118 | check.보기118 | 보기1 | checkbox | 보기1 |
| check.거래경험있음 | check.거래경험있음 | 거래경험있음 | checkbox | □ |
| check.년미만 | check.년미만 | 년미만 | checkbox | □ |
| check.년이상3년미만 | check.년이상3년미만 | 년이상~3년미만 | checkbox | □ |
| check.예 | check.예 | 예 | checkbox | □ |
| check.아니오 | check.아니오 | 아니오 | checkbox | 전산시스템명 |
| 구조화통화옵션 | 구조화통화옵션 | 구조화통화옵션(ExoticFXOption) | text | AUD |
| 규모에비추어적합합니까 | 규모에비추어적합합니까 | 규모에비추어적합합니까? | text |  |
| 업무절차보유여부 | 업무절차보유여부 | 업무절차보유여부 | text |  |
| check.보기119 | check.보기119 | 보기1 | checkbox | 보기1 |
| customer.name3 | customer.name3 | 고객명 | text | 박찬연 |
| agent.name | agent.name | 대리인 | text | 박영준 |
| 담당자 | 담당자 | 담당자(파생상품투자권유자문인력) | text | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |

### hf385 · 장외파생상품 일반투자자 투자자정보 확인서(개인 고객용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.385 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 자산총계 | 자산총계 | 자산총계 | text |  |
| 부채총계 | 부채총계 | 부채총계 | text |  |
| check.보기1 | check.보기1 | 보기1 | checkbox | 보기1 |
| check. | check. | □ | checkbox | □ |
| check[] | check[] | □ | checkbox | □ |
| check.보기12 | check.보기12 | 보기1 | checkbox | 보기1 |
| check.보기13 | check.보기13 | 보기1 | checkbox | 보기1 |
| check.보기14 | check.보기14 | 보기1 | checkbox | 보기1 |
| check.선택 | check.선택 | 선택 | checkbox | □ |
| check.개월이하 | check.개월이하 | 개월이하 | checkbox | □ |
| check.개월이하2 | check.개월이하2 | 개월이하 | checkbox | □ |
| check.년이하 | check.년이하 | 년이하 | checkbox | □ |
| check.보기15 | check.보기15 | 보기1 | checkbox | 보기1 |
| 하금융투자상품에투자해본경험이없음 | 하금융투자상품에투자해본경험이없음 | 하:금융투자상품에투자해본경험이없음 | text | 하나 TDF 2040 |
| check.보기16 | check.보기16 | 보기1 | checkbox | 보기1 |
| check.보기17 | check.보기17 | 보기1 | checkbox | 보기1 |
| check.하금융투자상품에투자해본경험이없음 | check.하금융투자상품에투자해본경험이없음 | 하:금융투자상품에투자해본경험이없음 | checkbox | 보기1 |
| check.보기18 | check.보기18 | 보기1 | checkbox | 보기1 |
| check.보기19 | check.보기19 | 보기1 | checkbox | 보기1 |
| check.보기110 | check.보기110 | 보기1 | checkbox | 보기1 |
| check.보기111 | check.보기111 | 보기1 | checkbox | 보기1 |
| check.보기112 | check.보기112 | 보기1 | checkbox | 보기1 |
| check.보기113 | check.보기113 | 보기1 | checkbox | 보기1 |
| check.보기114 | check.보기114 | 보기1 | checkbox | 보기1 |
| check.보기115 | check.보기115 | 보기1 | checkbox | 보기1 |
| check.보기116 | check.보기116 | 보기1 | checkbox | 보기1 |
| check.거래경험있음 | check.거래경험있음 | 거래경험있음 | checkbox | □ |
| check.년미만 | check.년미만 | 년미만 | checkbox | □ |
| check.년이상3년미만 | check.년이상3년미만 | 년이상~3년미만 | checkbox | □ |
| 구조화통화옵션 | 구조화통화옵션 | 구조화통화옵션(ExoticFXOption) | text | USD |
| 규모에비추어적합합니까 | 규모에비추어적합합니까 | 규모에비추어적합합니까? | text |  |
| customer.name | customer.name | 고객명 | text | 박찬연 |
| 담당자 | 담당자 | 담당자(파생상품투자권유자문인력) | text | 우민준 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |

### hf386 · 외환파생상품거래 헤지 수요 현황 및 거래 실행에 따른 확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.386 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.해당 | check.해당 | (해당 | checkbox | 란에 체크 |
| check.기타 | check.기타 | 기타(향후예상경상/재무거래등) | checkbox | 기타 (향후 예상 경상/재무거래 등) |
| check.택일 | check.택일 | 택일 | checkbox | 과거 수출입 실적기준 |
| check.택일2 | check.택일2 | 택일 | checkbox | 개별 계약건별 기준 |
| 택일_목록[].수출 | 택일_목록[].수출 | 수출(투자포함) | text |  |
| 수출 | 수출 | 수출(투자포함) | text |  |
| 헤지대상금액합계 | 헤지대상금액합계 | 헤지대상금액합계(헤지비율분모에해당) | number | 8,620,000 |
| 통화선도 | 통화선도 | 통화선도(외환스왑,NDF포함) | text | EUR |
| 통화옵션 | 통화옵션 | 통화옵션 | text | CNY |
| 통화스왑 | 통화스왑 | 통화스왑 | text | AUD |
| 환변동보험및기타 | 환변동보험및기타 | 환변동보험및기타() | text | 해당 없음 |
| 기헤지거래금액합계 | 기헤지거래금액합계 | 기헤지거래금액합계(헤지비율분자에해당) | number | 6,350,000 |
| 택일_목록[].수입 | 택일_목록[].수입 | 수입(조달포함) | text |  |
| 목록[].수입 | 목록[].수입 | 수입(조달포함) | text |  |
| 기체결외환파생상품거래금액_목록[].수입 | 기체결외환파생상품거래금액_목록[].수입 | 수입(조달포함) | text |  |
| 택일_목록[].비고 | 택일_목록[].비고 | 비고 | text | 해당 없음 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| 기체결외환파생상품거래금액_목록[].비고 | 기체결외환파생상품거래금액_목록[].비고 | 비고 | text | 해당 없음 |
| 거래금액 | 거래금액 | 거래금액 | number | 1,490,000 |
| date | date | 작성일 | date | 2026년 1월 31일 |

### hf387 · HANA FX TRADING SYSTEM 자동결제 이용신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.387 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 원화계좌_목록[].통화 | 원화계좌_목록[].통화 | 통화 | text | EUR |
| 외화계좌_목록[].통화 | 외화계좌_목록[].통화 | 통화 | text | USD |
| 원화계좌_목록[].계좌번호 | 원화계좌_목록[].계좌번호 | 계좌번호 | text | 149-773490-72624 |
| 외화계좌_목록[].계좌번호 | 외화계좌_목록[].계좌번호 | 계좌번호 | text | 192-339631-79709 |
| 원화계좌_목록[].통장용인감 | 원화계좌_목록[].통장용인감 | 통장용인감(서명) | text |  |
| 외화계좌_목록[].통장용인감 | 외화계좌_목록[].통장용인감 | 통장용인감(서명) | text |  |
| check.신청 | check.신청 | 신청 | checkbox | 해지 |
| check.신청2 | check.신청2 | 신청 | checkbox | 해지 |
| check.신청3 | check.신청3 | 신청 | checkbox | 신청 |
| check.신청4 | check.신청4 | 신청 | checkbox | 신청 |
| check.신청5 | check.신청5 | 신청 | checkbox | 해지 |
| check.신청6 | check.신청6 | 신청 | checkbox | 해지 |
| check.신청7 | check.신청7 | 신청 | checkbox | 신청 |
| check.신청8 | check.신청8 | 신청 | checkbox | 해지 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.HANAFXTRADINGSYSTEM일괄예약결제 | check.HANAFXTRADINGSYSTEM일괄예약결제 | ■HANAFXTRADINGSYSTEM일괄예약결제 | checkbox | 신청 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 하희하 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 길하영 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 천준승 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 박건혜 |

### hf388 · HANA FX TRADING SYSTEM 이용신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.388 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| employer.name | employer.name | 회사명 | text | 주식회사 태평양무역 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| 대표전화번호 | 대표전화번호 | 대표전화번호 | phone | 010-5907-7253 |
| 현물환거래한도 | 현물환거래한도 | 현물환거래한도 | number | 5,960,000원 |
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 해지 |
| 아이디 | 아이디 | 아이디(ID) | text |  |
| customer.name | customer.name | 성명 | text | 박찬연 |
| 부서직위 | 부서직위 | 부서/직위 | text |  |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| check.신청 | check.신청 | 신청 | checkbox | 해지 |
| check.신청2 | check.신청2 | 신청 | checkbox | 해지 |
| check.신청3 | check.신청3 | 신청 | checkbox | 신청 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| check.동의하십니까 | check.동의하십니까 | 동의하십니까? | checkbox | 동의하지 않음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 개인정보 | 개인정보 | ■개인(신용)정보 | text |  |

### hf389 · 위임장(장외파생상품 일반투자자용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.389 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 이름 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| customer.name2 | customer.name2 | 고객명(위임인) | text | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 본인의투자성향파악여부에대한의사결정 | 본인의투자성향파악여부에대한의사결정 | -본인의투자성향파악여부에대한의사결정 | text |  |
| 본인의투자성향분석결과를확인하는행위 | 본인의투자성향분석결과를확인하는행위 | -본인의투자성향분석결과를확인하는행위 | text |  |

### hf390 · 매매내역 등의 통지방법에 대한 고객확인서(장외파생상품)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.390 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].담당자명 | 목록[].담당자명 | 담당자명 | text | 박호진 |
| 목록[].부서및직급 | 목록[].부서및직급 | 부서및직급 | text |  |
| 목록[].전화번호 | 목록[].전화번호 | 전화번호 | text | 010-5907-7253 |
| check.전화번호 | check.전화번호 | 전화번호 | checkbox | 팩스 |
| check.이메일 | check.이메일 | 이메일 | checkbox | 이메일 |
| check.기타 | check.기타 | 기타 | checkbox | 기타 |
| check.V원하는항목의박스에체크 | check.V원하는항목의박스에체크 | V원하는항목의박스에체크 | checkbox | V 원하는 항목의 박스에 체크 |
| check.수령 | check.수령 | 수령 | checkbox | 수령 |
| customer.address | customer.address | 주소(필수,상세주소명기) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 팩스 | 팩스 | 팩스(선택) | phone | 010-5907-7253 |
| customer.email | customer.email | 이메일(선택) | text | chanyeon363@naver.com |
| check.수령거부 | check.수령거부 | 수령거부 | checkbox | 수령거부 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | (고객명) | text | 박찬연 |
| seal.signer | seal.customer | (고객명) | seal | 박찬연 |
| sign.signer | sign.customer | (고객명) | signature | 이민빈 |
| value | value | (법인등록번호/생년월일) | amount |  |

### hf391 · 고령투자자확인서(장외파생상품용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.391 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위개인신용정보수집이용에동의하십니까 | check.위개인신용정보수집이용에동의하십니까 | 위개인신용정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.조력자연락처제공 | check.조력자연락처제공 | [조력자방문]조력자연락처제공 | checkbox | [조력자 방문] 조력자 연락처 제공 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 조력자연락처작성 | 조력자연락처작성 | ■[조력자방문]조력자연락처작성 | text |  |
| 장외파생상품만기일까지보유이용 | 장외파생상품만기일까지보유이용 | -장외파생상품만기일까지보유·이용 | text |  |
| 거래목적및숙려기간제외대상사전확인 | 거래목적및숙려기간제외대상사전확인 | ■거래목적및숙려기간제외대상사전확인 | text |  |

### hf392 · 초고령투자자확인서(장외파생상품용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.392 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.조력자연락처제공 | check.조력자연락처제공 | [조력자방문]조력자연락처제공 | checkbox | [조력자 방문] 조력자 연락처 제공 |
| check.수집이용에동의하십니까 | check.수집이용에동의하십니까 | 수집·이용에동의하십니까? | checkbox | 동의함 |
| 조력자연락처 | 조력자연락처 | 조력자연락처 | phone | 010-5907-7253 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 조력자연락처작성 | 조력자연락처작성 | ■[조력자방문]조력자연락처작성 | text |  |
| 조력자와고객과의관계 | 조력자와고객과의관계 | 조력자와고객과의관계 | text |  |
| 장외파생상품거래불가 | 장외파생상품거래불가 | ■[조력자미방문]장외파생상품거래불가 | text |  |
| 거래목적및숙려기간제외대상사전확인 | 거래목적및숙려기간제외대상사전확인 | ■거래목적및숙려기간제외대상사전확인 | text |  |

### hf393 · 이자율스왑 연계 대출 분할상환 원금 및 이자율스왑 정산이자 출금서비스 특약

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.393 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 여신과목 | 여신과목 | 여신과목 | text | 주택담보대출 |
| 여신개시일 | 여신개시일 | 여신개시일 | date | 2025.09.11 |
| 여신금액 | 여신금액 | 여신(한도)금액 | number | 58,740,000 |
| 여신기간만료일 | 여신기간만료일 | 여신기간만료일 | date | 2025-01-30 |
| 거래일 | 거래일 | 거래일 | date | 2025.07.21 |
| 발효일 | 발효일 | 발효일 | date | 2025년 1월 25일 |
| 지급고정금리 | 지급고정금리 | 지급고정금리 | number | 2.57 |
| 금액 | 금액 | 금액 | number | 207,330,000 |
| 종료일 | 종료일 | 종료일 | date | 2027.03.22 |
| 수취변동금리 | 수취변동금리 | 수취변동금리 | number | 6.55 |
| account | account | 출금계좌번호 | account_no | 000-287736-52424 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 강순준 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |

### hf394 · 적정성원칙 투자자확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.394 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| A등급 | A등급 | A등급 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 법인등록번호생년월일 | 법인등록번호생년월일 | 법인등록번호/생년월일 | date | 2025년 2월 8일 |

### hf397 · 금융거래정보이용제공동의서(영문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.397 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| KEBHanaBank | KEBHanaBank | KEBHanaBank | text |  |
| NameNameoftheCorporation | NameNameoftheCorporation | Name/NameoftheCorporation | text |  |
| customer.address | customer.address | Address | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| Consentedby | Consentedby | Consentedby | text |  |
| CustomerWhoConsents | CustomerWhoConsents | CustomerWhoConsents | text |  |
| FinancialCompanies | FinancialCompanies | FinancialCompanies, | text |  |
| etcWhichWillProvide | etcWhichWillProvide | etc.WhichWillProvide | text |  |
| toWhichTransaction | toWhichTransaction | toWhichTransaction | text |  |
| Signedon | Signedon | Signedon | text |  |

### hf398 · 금융거래정보이용제공동의서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.398 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 주식회사하나은행 | 주식회사하나은행 | 주식회사하나은행 | text | 신한은행 |
| 거래정보저장소 | 거래정보저장소 | 거래정보저장소(한국거래소) | text |  |
| 법인명이름 | 법인명이름 | 법인명/이름 | text | 주식회사 신영상사 |
| 명의인의인적사항사업자등록증번호생년월일 | 명의인의인적사항사업자등록증번호생년월일 | 명의인의인적사항사업자등록증번호/생년월일 | date | 2025-07-02 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.signer | seal.customer | 서명또는 | seal | 박찬연 |
| sign.signer | sign.customer | 서명또는 | signature | 현예지 |
| 명의인에대한정보 | 명의인에대한정보 | 명의인에대한정보 | text | 이윤성 |
| 금융거래관련정보 | 금융거래관련정보 | 금융거래관련정보 | text |  |
| 법령및금융투자업규정에따른보고의무이행 | 법령및금융투자업규정에따른보고의무이행 | 법령및금융투자업규정에따른보고의무이행 | text |  |
| 일로동의를철회할수있음 | 일로동의를철회할수있음 | 일로동의를철회할수있음 | text |  |
| 으로봄 | 으로봄 | 으로봄 | text |  |

### hf399 · 파생상품거래 손실한도 초과 및 증거담보 요청 통지서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.399 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.ceo | company.ceo | [수신]대표이사 | text | 박찬연 |
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 참조 | 참조 | 참조 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer.name | signer.name | 상호:주식회사하나은행 | text | 채예영 |
| seal.signer | seal.signer | 상호:주식회사하나은행 | seal | 채예영 |
| sign.signer | sign.signer | 상호:주식회사하나은행 | signature | 남정희 |

### hf400 · 파생상품거래 손실한도 감액통지서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.400 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer.name | corp.name | 상호 | text | (주)유니온무역 |
| seal.signer | seal.corp | 상호 | seal | (주)삼정전자 |
| sign.signer | sign.customer | 상호 | signature | (주)유니온무역 |
| signer2.name | signer2.name | 상호:주식회사하나은행 | text | 염건윤 |
| seal.signer2 | seal.signer2 | 상호:주식회사하나은행 | seal | 석은원 |
| sign.signer2 | sign.signer2 | 상호:주식회사하나은행 | signature | 표다지 |

### hf401 · 전문투자자 전환신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.401 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 전문투자자확인증보유자 | 전문투자자확인증보유자 | 전문투자자확인증보유자 | text |  |
| 등록번호 | 등록번호 | 등록번호 | text | 3873-7667 |
| 발급일자 | 발급일자 | 발급일자 | date | 2025-06-09 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.name | customer.name | 고객명 | text | 박찬연 |
| company.ceo | corp.ceo | 대표이사 | text | 박찬연 |
| 법인등록번호생년월일 | 법인등록번호생년월일 | 법인등록번호/생년월일(고객번호) | date | 2025.07.20 |
| signer.name | signer.name | 신청담당자성명 | text | 채승린 |
| seal.signer | seal.signer | 신청담당자성명 | seal | 윤수하 |
| sign.signer | sign.signer | 신청담당자성명 | signature | 채승린 |
| 신청담당자생년월일 | 신청담당자생년월일 | 신청담당자생년월일 | date | 2025.10.02 |

### hf402 · 장외파생상품 거래 담당자 지정 통지서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.402 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].성명 | 목록[].성명 | 성명 | text | 구동현 |
| 목록[].소속부서및직급 | 목록[].소속부서및직급 | 소속부서및직급 | text |  |
| 목록[].생년월일 | 목록[].생년월일 | 생년월일 | text | 2025.09.06 |
| 목록[].인감 | 목록[].인감 | 인감(서명) | text |  |
| 목록[].권한의제한 | 목록[].권한의제한 | 권한의제한 | text |  |
| 목록[].전화번호팩스번호 | 목록[].전화번호팩스번호 | 전화번호&팩스번호 | text | 043-783-2775 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| company.name | corp.name | 법인명 | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표이사 | text | 박찬연 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |

### hf403 · 일반투자자 전환신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.403 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.nationality | customer.nationality | 국적 | text | 대한민국 |
| 주권상장거래소명 | 주권상장거래소명 | 주권상장거래소명 | text |  |
| 설립근거법 | 설립근거법 | 설립근거법 | text |  |
| customer.name | customer.name | 고객명 | text | 박찬연 |
| company.ceo | corp.ceo | 대표이사 | text | 박찬연 |
| 법인등록번호생년월일 | 법인등록번호생년월일 | 법인등록번호/생년월일(고객번호) | date | 2025.09.03 |
| signer.name | signer.name | 신청담당자성명 | text | 지훈주 |
| seal.signer | seal.signer | 신청담당자성명 | seal | 이유승 |
| sign.signer | sign.signer | 신청담당자성명 | signature | 지훈주 |
| 신청담당자생년월일 | 신청담당자생년월일 | 신청담당자생년월일 | date | 2025년 11월 9일 |

### hf405 · 외환파생상품 거래 금액 확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.405 (파생상품) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 통화선도 | 통화선도 | 통화선도(외환스왑,NDF포함) | text | USD |
| 통화옵션 | 통화옵션 | 통화옵션 | text | EUR |
| 통화스왑 | 통화스왑 | 통화스왑 | text | EUR |
| 환변동보험 | 환변동보험 | 환변동보험 | text |  |
| 통화선도2 | 통화선도2 | 통화선도(외환스왑,NDF포함) | text | USD |
| 통화옵션2 | 통화옵션2 | 통화옵션 | text | USD |
| 통화스왑2 | 통화스왑2 | 통화스왑 | text | USD |
| 환변동보험2 | 환변동보험2 | 환변동보험 | text |  |
| 헤지거래한도 | 헤지거래한도 | 헤지거래한도(a) | number | 290,000 |
| 기체결외환파생거래금액 | 기체결외환파생거래금액 | 기체결외환파생거래금액(b) | number | 14,250,000 |
| 금번거래예정금액 | 금번거래예정금액 | 금번거래예정금액(c) | number | 136,270,000 |
| 위험헤지비율100 | 위험헤지비율100 | 위험헤지비율((b+c)/(a)*100) | number | 30 |
| date | date | 작성일 | date | 2026년 1월 31일 |

### hf197 · 위임장(집합투자증권 및 연금저축계좌 투자용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.197 (펀드) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.birth2 | customer.birth2 | 생년월일/사업자번호 | date | 1990년 2월 10일 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone2 | customer.phone2 | 연락처 | phone | 010-5907-7253 |
| signer.name | signer.name | 직원명 | text | 허동현 |
| seal.signer | seal.signer | 직원명 | seal | 허동현 |
| sign.signer | sign.signer | 직원명 | signature | 심나도 |
| 본인의투자성향파악여부에대한의사결정 | 본인의투자성향파악여부에대한의사결정 | -본인의투자성향파악여부에대한의사결정 | text |  |
| 본인의투자성향분석결과를확인하는행위 | 본인의투자성향분석결과를확인하는행위 | -본인의투자성향분석결과를확인하는행위 | text |  |
| 신규외기타위임거래를구체적으로명시 | 신규외기타위임거래를구체적으로명시 | 신규외기타위임거래를구체적으로명시 | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 전환은 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 추원정 |

### hf198 · 공모부동산집합투자증권 과세특례신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 서식 No.198 (펀드) 원본 위에 기재

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| check.보기1 | check.보기1 | 보기1 | checkbox | 보기1 |
| check.보기12 | check.보기12 | 보기1 | checkbox | 보기1 |
| 금융기관펀드계좌번호 | 금융기관펀드계좌번호 | 금융기관펀드계좌번호 | text | 869-918596-51054 |
| 투자대상 | 투자대상 | 투자대상(펀드명) | text |  |
| 투자금액 | 투자금액 | 투자금액(투자한도금액) | number | 150,000 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 강순준 |
| signer2.name | agent.name | 대리인 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인 | seal | 강석호 |
| sign.signer2 | sign.agent | 대리인 | signature | 박영준 |
| customer.birth | customer.birth | 생년월일:... | date | 1990.02.10 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 심민지 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김소현 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김환진 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 노정율 |

### tax_payment_certificate · 납세증명서(국세완납증명)

그룹: 세금·보험 (`tax`)

홈택스 발급 국세 납세증명서 (개인사업자).  special short_validity: 유효기간 단축 + 사유, tax_deferral: 연장ㆍ유예 명세, emigration: 해외이주용.

연결 업무: 개인사업자 대출 (sole_proprietor_loan)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| issue_no | issue_no | 발급번호 | text | 6377-316-8893-532 |
| taxpayer.trade_name | customer.trade_name | 상호(법인명) | text | 동방학원 |
| taxpayer.biz_no | customer.biz_no | 사업자등록번호 | biz_no | 860-11-55034 |
| taxpayer.name | customer.name | 성명(대표자) | text | 박찬연 |
| taxpayer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| taxpayer.address | customer.address | 주소(본점) | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| valid_period | valid_period | 증명서유효기간 | text | 2026년 01월 31일 ~ 2026년 03월 01일 |
| valid_reason | valid_reason | 유효기간을정한사유 | text | 2024년 귀속 종합소득세 납부기한(2025년 5월 31일) 도래 |
| purpose_type | purpose_type | 사용목적 | checkbox | 기타 |
| purpose | purpose | 사용목적 | text | 금융기관 제출용 |
| payer | payer | 대금지급자 | amount | 서울특별시 |
| deferral | deferral | 연장ㆍ유예명세 | text | 해당없음 |
| arrears | arrears | 체납액 | text | 없음 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 서초세무서장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 서초세무서장인 |
| deferrals[].kind | deferrals[].kind | 연장ㆍ유예종류 | text | 납부기한등 연장 |
| deferrals[].period | deferrals[].period | 연장ㆍ유예기간 | text | 2025.06.01 ~ 2026.03.01 |
| deferrals[].tax_period | deferrals[].tax_period | 과세기간 | text | 2024년 귀속 |
| deferrals[].tax_item | deferrals[].tax_item | 세목 | text | 종합소득세 |
| deferrals[].due | deferrals[].due | 납부기한 | date | 2025.05.31 |
| deferrals[].amount | deferrals[].amount | 세액 | amount | 1,507,330 |

연결 업무 sole_proprietor_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### tax_payment_certificate_corp · 납세증명서(법인)

그룹: 세금·보험 (`tax`)

홈택스 발급 국세 납세증명서 (법인).

연결 업무: 법인 여신 (corporate_credit)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| issue_no | issue_no | 발급번호 | text | 2207-657-1657-159 |
| taxpayer.corp_name | taxpayer.corp_name | 상호(법인명) | text | (주)유니온무역 |
| taxpayer.biz_no | customer.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| taxpayer.ceo | customer.ceo | 성명(대표자) | text | 박찬연 |
| taxpayer.corp_reg_no | customer.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| taxpayer.address | customer.address | 주소(본점) | text | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| valid_period | valid_period | 증명서유효기간 | text | 2026년 01월 31일 ~ 2026년 03월 01일 |
| valid_reason | valid_reason | 유효기간을정한사유 | text | 2026사업연도 법인세 중간예납 납부기한(2026년 8월 31일) 도래 |
| purpose_type | purpose_type | 사용목적 | checkbox | 기타 |
| purpose | purpose | 사용목적 | text | 금융기관 제출용 |
| payer | payer | 대금지급자 | amount | 한국전력공사 |
| deferral | deferral | 연장ㆍ유예명세 | text | 해당없음 |
| arrears | arrears | 체납액 | text | 없음 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 중부세무서장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 중부세무서장인 |
| deferrals[].kind | deferrals[].kind | 연장ㆍ유예종류 | text | 납부고지의 유예 |
| deferrals[].period | deferrals[].period | 연장ㆍ유예기간 | text | 2025.04.01 ~ 2025.09.30 |
| deferrals[].tax_period | deferrals[].tax_period | 과세기간 | text | 2024.01.01 ~ 2024.12.31 |
| deferrals[].tax_item | deferrals[].tax_item | 세목 | text | 법인세 |
| deferrals[].due | deferrals[].due | 납부기한 | date | 2025.03.31 |
| deferrals[].amount | deferrals[].amount | 세액 | amount | 21,334,860 |

연결 업무 corporate_credit · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### local_tax_payment_certificate · 지방세 납세증명서

그룹: 세금·보험 (`tax`)

정부24·위택스 발급 지방세 납세증명서 (체납 없음). 개인사업자면 상호·사업자등록번호도 적는다.  special local_deferral: 징수유예등 내역 1~2건 (재산세·자동차세·지방소득세), local_short_validity: 유효기간이 30일 안에 오는 정기분 납기까지.

연결 업무: 개인사업자 대출 (sole_proprietor_loan)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| issue_no | issue_no | 발급번호 | text | 9572-3737-4206-7656 |
| taxpayer.name | customer.name | 성명(법인명) | text | 박찬연 |
| taxpayer.rrn | customer.rrn | 주민등록번호(법인등록번호) | rrn | 900210-1****** |
| taxpayer.address | customer.address | 주소(영업소) | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| purpose | purpose | 증명서사용목적 | text | 금융기관 제출용 |
| valid_period | valid_period | 증명서유효기간 | text | 2026년 01월 31일 ~ 2026년 03월 01일 |
| deferrals[].tax_year | deferrals[].tax_year | 과세연도 | number | 2025 |
| deferrals[].tax_item | deferrals[].tax_item | 세목 | text | 지방소득세 |
| deferrals[].due | deferrals[].due | 납부기한 | date | 2025.05.31 |
| deferrals[].amount | deferrals[].amount | 세액 | amount | 2,199,610 |
| deferrals[].period | deferrals[].period | 유예기간 | text | 2025.11.22 ~ 2026.08.22 |
| arrears | arrears | 체납액 | text | 없음 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 서울특별시 서초구청장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 서초구청장인 |
| deferral | deferral | 징수유예등또는체납처분유예의내역 | text | 해당없음 |
| taxpayer.trade_name | customer.trade_name | 상호 | text | 한빛세무회계 |
| taxpayer.biz_no | customer.biz_no | 사업자등록번호 | biz_no | 696-24-15367 |

연결 업무 sole_proprietor_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### local_tax_assessment · 지방세 세목별 과세증명서

그룹: 세금·보험 (`tax`)

주소지 시·군·구청장이 발급하는 지방세 세목별 과세증명서 (재산세·자동차세·주민세 등).  heavy: 4~5개 연도 + 물건 여러 개(토지·두 번째 주택, 자동차 2대, 등록면허세), 2~3쪽. special: car_replaced(차량 교체, 일할 과세), car_prepay(자동차세 연납), biz_resident_tax(주민세 사업소분),          local_income_tax(지방소득세 종합소득분), second_house(2주택: 일반세율).

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| issue_no | issue_no | 발급번호 | text | 6934-2589-5434-0275 |
| taxpayer.name | customer.name | 성명(법인명) | text | 박찬연 |
| taxpayer.rrn | customer.rrn | 주민(법인,외국인)등록번호 | rrn | 900210-1659382 |
| taxpayer.address | customer.address | 주소(영업소) | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| period | period | 과세연도 | text | 2024년 ~ 2025년 |
| purpose | purpose | 사용목적 | text | 은행 제출 |
| items[].tax_item | items[].tax_item | 세목 | text | 지방소득세 |
| items[].levied | items[].levied | 부과연월 | month | 2024.05 |
| items[].kind | items[].kind | 구분 | text | 확정신고 |
| items[].object | items[].object | 과세대상 | text | 2023년 귀속 종합소득 |
| items[].base | items[].base | 과세표준 | text | 60,297,716 |
| items[].tax | items[].tax | 세액 | amount | 864,140 |
| items[].edu | items[].edu | 지방교육세 | number | 0 |
| items[].total | items[].total | 합계 | amount | 864,140 |
| sum.tax | sum.tax | 세액합계 | amount | 1,548,330 |
| sum.edu | sum.edu | 지방교육세합계 | number | 73,990 |
| sum.total | sum.total | 총합계 | amount | 1,622,320 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 서울특별시 서초구청장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 서초구청장인 |

### vat_tax_base_certificate · 부가가치세 과세표준증명

그룹: 세금·보험 (`tax`)

홈택스 발급 부가가치세 과세표준증명 (개인사업자).  heavy: 3~5년치(일반 6~10기간). special: vat_prelim(예정신고 분리), vat_amended(수정신고 줄 추가), vat_late(기한후신고), vat_refund(시설투자 환급). 휴업(_biz_facts suspended) 기간은 매출 0 또는 감소, 간이→일반 전환(simple_to_general)이면 앞쪽 기간이 1년 단위 간이과세 기간.

연결 업무: 개인사업자 대출 (sole_proprietor_loan)

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| issue_no | issue_no | 발급번호 | text | 5373-520-1909-420 |
| taxpayer.name | customer.name | 성명(대표자) | text | 박찬연 |
| taxpayer.rrn | customer.rrn | 주민(법인)등록번호 | rrn | 900210-1****** |
| taxpayer.trade_name | customer.trade_name | 상호(법인명) | text | 동방학원 |
| taxpayer.biz_no | customer.biz_no | 사업자등록번호 | biz_no | 860-11-55034 |
| taxpayer.address | customer.address | 사업장소재지 | text | 울산광역시 남구 대학로 14, 11층 (달동, 아이엠스퀘어) |
| taxpayer.biz_type | taxpayer.biz_type | 업태 | text | 서비스업 |
| taxpayer.biz_item | taxpayer.biz_item | 종목 | text | 학원 |
| items[].period | items[].period | 과세기간 | text | 2024.01.01 ~ 2024.06.30 |
| items[].kind | items[].kind | 신고구분 | text | 정기확정 |
| items[].filed | items[].filed | 신고일 | date | 2024.07.13 |
| items[].base_total | items[].base_total | 매출과세표준계 | amount | 307,114,710 |
| items[].base_taxable | items[].base_taxable | 과세분 | amount | 15,015,130 |
| items[].base_exempt | items[].base_exempt | 면세수입금액 | amount | 292,099,580 |
| items[].tax | items[].tax | 납부할세액(환급받을세액) | amount | 313,810 |
| purpose | purpose | 사용목적 | text | 대출 신청 |
| issue_date | issue_date | 발급일 | date | 2026년 01월 31일 |
| issuer | issuer | 발급기관 | text | 울산세무서장 |
| seal.issuer | seal.issuer | 발급기관직인 | seal | 울산세무서장인 |

연결 업무 sole_proprietor_loan · 추출/비교 작업:

명시적 작업 없음. 업무별 기본 처리 설정은 위 업무 목록 또는 catalog.json에서 확인합니다.

### income_tax_return · 종합소득세 과세표준확정신고 및 납부계산서

그룹: 세금·보험 (`tax`)

종합소득세 확정신고서. 제1쪽(기본사항 + 환급금 계좌 + 세액의 계산)은 항상, 명세(제2·3쪽)는 소득이 여럿이거나 수정신고·기한후신고·경정청구·공동사업 등일 때 붙는다. 사업소득금액은 표준손익계산서 당기순이익(공동사업이면 지분만큼)과 같다.  현행 서식은 종합소득세ㆍ농어촌특별세만 적는다 (지방소득세는 별도 신고서). paper: 손으로 쓴 서면 신고서(전자신고세액공제 없음) — 템플릿이 손글씨체 + 정정 효과를 쓴다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| tax_year | tax_year | 귀속연도 | number | 2024 |
| residency | residency | 거주구분 | checkbox | 거주자 |
| nationality | customer.nationality | 내ㆍ외국인 | checkbox | 내국인 |
| taxpayer.name | customer.name | 성명 | text | 박찬연 |
| taxpayer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| taxpayer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| taxpayer.email | customer.email | 전자우편주소 | text | chanyeon363@naver.com |
| taxpayer.biz_phone | taxpayer.biz_phone | 사업장전화번호 | phone | 052-956-0748 |
| taxpayer.mobile | customer.mobile | 휴대전화번호 | phone | 010-5907-7253 |
| filing_type | filing_type | 신고유형 | text | 성실신고확인 |
| bookkeeping | bookkeeping | 기장의무 | text | 복식부기의무자 |
| filing_kind | filing_kind | 신고구분 | text | 정기신고 |
| national.total_income | national.total_income | 종합소득금액 | amount | 38,259,272 |
| national.deduction | national.deduction | 소득공제 | amount | 6,443,320 |
| national.base | national.base | 과세표준 | amount | 31,815,952 |
| national.rate | national.rate | 세율 | percent | 15% |
| national.computed | national.computed | 산출세액 | number | 3,512,392 |
| national.reduction | national.reduction | 세액감면 | number | 0 |
| national.credit | national.credit | 세액공제 | amount | 90,000 |
| national.determined | national.determined | 결정세액 | number | 3,422,392 |
| national.penalty | national.penalty | 가산세 | number | 0 |
| national.additional | national.additional | 추가납부세액 | number | 0 |
| national.total | national.total | 합계 | amount | 3,422,392 |
| national.prepaid | national.prepaid | 기납부세액 | number | 922,970 |
| national.payable | national.payable | 납부(환급)할총세액 | amount | 2,499,420 |
| national.special_deduct | national.special_deduct | 납부특례세액차감 | number | 0 |
| national.special_add | national.special_add | 납부특례세액가산 | number | 0 |
| national.installment | national.installment | 분납할세액 | number | 0 |
| national.due_payable | national.due_payable | 신고기한이내납부할세액 | amount | 2,499,420 |
| filed_date | filed_date | 신고일 | date | 2025년 06월 21일 |
| seal.taxpayer | seal.customer | 신고인 | seal | 이욱유 |
| sign.taxpayer | sign.customer | 신고인 | signature | 위나아 |
| tax_agent.name | related.name | 세무대리인 | text | 지선수 |
| seal.tax_agent | seal.related | 세무대리인 | seal | 최원하 |
| sign.tax_agent | sign.related | 세무대리인 | signature | 지선수 |
| tax_agent.biz_no | tax_agent.biz_no | 세무대리인사업자등록번호 | biz_no | 388-36-49294 |
| tax_agent.phone | related.phone | 세무대리인전화번호 | phone | 052-673-9329 |
| tax_office | tax_office | 세무서장 | text | 서초세무서장 |
| incomes[].type | incomes[].type | 소득구분 | text | 사업소득 |
| incomes[].payer | incomes[].payer | 소득의지급자 | text | 넥스트학원 |
| incomes[].revenue | incomes[].revenue | 총수입금액 | amount | 390,549,770 |
| incomes[].expense | incomes[].expense | 필요경비 | amount | 347,059,995 |
| incomes[].amount | incomes[].amount | 소득금액 | amount | 43,489,775 |
| incomes[].withheld | incomes[].withheld | 원천징수세액 | number | 0 |
| business_income.address | business_income.address | 사업장소재지 | text | 강원특별자치도 춘천시 공지로 647, 11층 03호 (효자동, 케이타워) |
| business_income.trade_name | business_income.trade_name | 상호 | text | 넥스트학원 |
| business_income.biz_no | business_income.biz_no | 사업자등록번호 | biz_no | 234-02-91864 |
| business_income.code | business_income.code | 업종코드 | number | 809009 |
| business_income.revenue | business_income.revenue | 총수입금액 | amount | 390,549,770 |
| business_income.expense | business_income.expense | 필요경비 | amount | 347,059,995 |
| business_income.income | business_income.income | 소득금액 | amount | 43,489,775 |
| dependents[].relation | dependents[].relation | 관계 | text | 본인 |
| dependents[].name | dependents[].name | 성명 | text | 강순준 |
| dependents[].rrn | dependents[].rrn | 주민등록번호 | rrn | 970514-2150000 |
| dependents[].basic | dependents[].basic | 기본공제 | text | ○ |
| dependents[].extra | dependents[].extra | 추가공제 | text | 경로우대 |
| deduction_items[].item | deduction_items[].item | 소득공제항목 | text | 기본공제 |
| deduction_items[].amount | deduction_items[].amount | 금액 | amount | 1,500,000 |
| credit_items[].item | credit_items[].item | 세액공제항목 | text | 표준세액공제 |
| credit_items[].amount | credit_items[].amount | 금액 | amount | 70,000 |
| refund_account.bank | refund_account.bank | 금융기관/체신관서명 | text | 기업은행 |
| refund_account.number | refund_account.number | 계좌번호 | text | 941-473791-23-142 |
| prepaid_items[].item | prepaid_items[].item | 기납부세액항목 | text | 중간예납세액 |
| prepaid_items[].amount | prepaid_items[].amount | 금액 | amount | 2,291,860 |
| penalty_items[].item | penalty_items[].item | 가산세항목 | text | 무신고가산세 |
| penalty_items[].amount | penalty_items[].amount | 금액 | amount | 681,530 |
| business_income.partner | business_income.partner | 공동사업자 | text | 김훈도 |
| business_income.share | business_income.share | 손익분배비율 | percent | 60% |

### gov_building_general · 일반건축물대장(갑)

그룹: 부동산 (`real_estate`)

일반건축물대장(갑) 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=155204859&bylClsCd=110202

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | official.name | 명칭 | text | 한신휴플러스에듀포레 |
| official.address | property.location | 대지위치 | text | 경기도 수원시 영통구 원천동 87 |
| official.road | official.road | 도로명주소 | text | 경기도 수원시 영통구 매탄로 376, 115동 2104호 |
| official.owner | official.owner | 소유자 | text | 박찬연 |
| official.structure | official.structure | 주구조 | text | 철근콘크리트구조 |

### gov_building_unit · 집합건축물대장(전유부, 갑)

그룹: 부동산 (`real_estate`)

집합건축물대장(전유부, 갑) 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=155204921&bylClsCd=110202 전유부 갑·계속면·현황도 빈 양식을 모두 포함하며 평면도는 임의 생성하지 않는다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.id | official.id | 건물ID | text | 1792-2013-094176 |
| official.name | official.name | 명칭 | text | 한신휴플러스에듀포레 |
| official.address | property.location | 대지위치 | text | 경기도 수원시 영통구 원천동 87 |
| official.road | official.road | 도로명주소 | text | 경기도 수원시 영통구 매탄로 376, 115동 2104호 |
| official.owner | official.owner | 소유자성명 | text | 박찬연 |
| official.rrn | official.rrn | 소유자등록번호 | rrn | 900210-1659382 |
| official.area | official.area | 전유면적 | number | 101.84 |

### gov_business_proof · 사업자등록증명

그룹: 개인사업자 (`business`)

사업자등록증명 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?flSeq=155626677&flNm=%5B%EB%B3%84%EC%A7%80+5%5D+%EC%82%AC%EC%97%85%EC%9E%90%EB%93%B1%EB%A1%9D%EC%A6%9D%EB%AA%85%28%EA%B5%AD%EB%AC%B8%29&bylClsCd=200203

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.company | corp.name | 상호(법인명) | text | 동방학원 |
| official.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 860-11-55034 |
| official.name | corp.ceo | 대표자성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | corp.address | 사업장소재지 | text | 울산광역시 남구 대학로 14, 11층 |
| official.opened | corp.established | 개업일 | date | 2020.03.21 |
| official.registered | official.registered | 사업자등록일 | date | 2020.03.21 |
| official.industry | official.industry | 업태 | text | 서비스업 |
| official.item | corp.biz_item | 종목 | text | 학원 |
| official.number | official.number | 발급번호 | text | 328739-0928843 |

### gov_business_registration · 사업자등록증

그룹: 개인사업자 (`business`)

사업자등록증 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=162624673&bylClsCd=110202 개인사업자용 서식 및 종된 사업장 부표. 원본의 서식 규격 안내도 유지한다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.biz_no | corp.biz_no | 등록번호 | biz_no | 860-11-55034 |
| official.company | corp.name | 상호 | text | 동방학원 |
| official.name | customer.name | 성명 | text | 박찬연 |
| official.address | corp.address | 사업장소재지 | text | 울산광역시 남구 대학로 14, 11층 |
| official.industry | official.industry | 업태 | text | 서비스업 |
| official.item | corp.biz_item | 종목 | text | 학원 |
| official.taxpayer_type | official.taxpayer_type | 과세유형 | text | 간이과세자 |
| official.opened0 | official.opened0 | 개업연월일년 | number | 2020 |
| official.opened1 | official.opened1 | 개업연월일월 | number | 03 |
| official.opened2 | official.opened2 | 개업연월일일 | number | 21 |
| official.birth | official.birth | 생년월일 | date | 1990.02.10 |
| official.issue_reason | official.issue_reason | 발급사유 | text | 재발급 |
| official.unit_tax_no | official.unit_tax_no | 사업자단위과세적용여부부(V) | text | V |
| official.einvoice_email | official.einvoice_email | 전자세금계산서전용전자우편주소 | text | contact@dongbang.co.kr |
| official.issue0 | official.issue0 | 발급일년 | number | 2026 |
| official.issue1 | official.issue1 | 발급일월 | number | 01 |
| official.issue2 | official.issue2 | 발급일일 | number | 31 |
| official.annex_biz_no0 | official.annex_biz_no0 | 부표사업자등록번호앞 | number | 860 |
| official.annex_biz_no1 | official.annex_biz_no1 | 부표사업자등록번호가운데 | number | 11 |
| official.annex_biz_no2 | official.annex_biz_no2 | 부표사업자등록번호뒤 | number | 55034 |
| official.annex_issue0 | official.annex_issue0 | 부표발급일년 | number | 2026 |
| official.annex_issue1 | official.annex_issue1 | 부표발급일월 | number | 01 |
| official.annex_issue2 | official.annex_issue2 | 부표발급일일 | number | 31 |

### gov_business_registration_corp · 사업자등록증(법인사업자)

그룹: 개인사업자 (`business`)

사업자등록증 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=162624673&bylClsCd=110202 법인사업자용 서식 및 종된 사업장 부표. 원본의 서식 규격 안내도 유지한다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.biz_no | corp.biz_no | 등록번호 | biz_no | 264-82-36559 |
| official.company | corp.name | 상호 | text | (주)유니온무역 |
| official.name | corp.ceo | 성명 | text | 박찬연 |
| official.address | corp.address | 사업장소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| official.industry | official.industry | 업태 | text | 도매 및 소매업 |
| official.item | corp.biz_item | 종목 | text | 무역 |
| official.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |

### gov_financial_proof · 표준재무제표증명

그룹: 개인사업자 (`business`)

표준재무제표증명 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?flSeq=155626725&flNm=%5B%EB%B3%84%EC%A7%80+13%5D+%ED%91%9C%EC%A4%80%EC%9E%AC%EB%AC%B4%EC%A0%9C%ED%91%9C%EC%A6%9D%EB%AA%85%28%EA%B5%AD%EB%AC%B8%29&bylClsCd=200203 표준재무제표증명 표지 서식이며 첨부 재무제표 전체를 포함하지 않는다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.company | corp.name | 상호 | text | (주)유니온무역 |
| official.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| official.name | corp.ceo | 대표자 | text | 박찬연 |
| official.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| official.industry | official.industry | 업태 | text | 도매 및 소매업 |
| official.item | corp.biz_item | 종목 | text | 무역 |
| official.address | corp.address | 사업장 | text | 서울특별시 중구 다산로 361, 6층 |
| official.year | official.year | 사업연도 | text | 2025.01.01 ~ 2025.12.31 |
| official.filing | official.filing | 신고구분 | text | 정기신고 |

### gov_foreign_household · 외국인체류확인서

그룹: 가족관계 (`family`)

외국인체류확인서 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169477471&bylClsCd=110202 외국인 체류자가 있는 대상 건물 예시이며 외국인 고객 프로필을 사용할 때 이름을 대조한다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.address | property.location | 대상건물소재지 | text | 경기도 수원시 영통구 매탄로 376, 115동 2104호 |
| official.name | customer.name | 성명 | text | PARK CHANYEON |
| official.moved | official.moved | 전입일자 | date | 2020.05.08 |
| official.number | official.number | 일련번호 | number | 1 |

### gov_income · 소득금액증명

그룹: 소득·재직 (`income`)

소득금액증명 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?flSeq=155626737&flNm=%5B%EB%B3%84%EC%A7%80+15%5D+%EC%86%8C%EB%93%9D%EA%B8%88%EC%95%A1%EC%A6%9D%EB%AA%85%28%EA%B5%AD%EB%AC%B8%29&bylClsCd=200203 종합과세와 연말정산을 구분한 2024 개정 서식. 같은 근로소득을 두 구역에 중복 기재하지 않는다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.company | employer.name | 근로소득발생처 | text | 주식회사 태평양무역 |
| official.biz_no | official.biz_no | 발생처사업자등록번호 | biz_no | 501-82-42625 |
| official.salary | official.salary | 지급받은총액 | amount | 48,570,000 |
| official.year | official.year | 귀속연도 | number | 2024 |
| official.tax | official.tax | 총결정세액 | amount | 2,257,830 |
| official.number | official.number | 발급번호 | text | 5748-861-1943-635 |
| official.office | official.office | 관할지역 | text | 서초 |
| official.issue0 | official.issue0 | 발급일년 | number | 2026 |
| official.issue1 | official.issue1 | 발급일월 | number | 01 |
| official.issue2 | official.issue2 | 발급일일 | number | 31 |
| official.salary_income | official.salary_income | 근로소득소득금액 | amount | 900,000 |
| official.period_from | official.period_from | 납세자가신청한증명귀속연도시작 | number | 2022 |
| official.period_to | official.period_to | 납세자가신청한증명귀속연도끝 | number | 2024 |
| official.receipt_no | official.receipt_no | 접수번호 | text | 038516-5681192 |
| official.issuer_department | official.issuer_department | 증명발급자담당부서 | text | 소득세과 |
| official.issuer_person | official.issuer_person | 증명발급자담당자 | text | 이민윤 |
| official.issuer_phone | official.issuer_phone | 증명발급자연락처 | phone | 02-3424-1065 |
| official.tax_officer_department | official.tax_officer_department | 세적담당자담당부서 | text | 부가가치세과 |
| official.tax_officer_person | official.tax_officer_person | 세적담당자담당자 | text | 금진아 |
| official.tax_officer_phone | official.tax_officer_phone | 세적담당자연락처 | phone | 043-988-3147 |

### gov_income_tax_return · 종합소득세 과세표준확정신고 및 납부계산서(일반)

그룹: 세금·보험 (`tax`)

국세청 종합소득세 일반 신고서 35쪽(본표·작성방법·부속명세) 원문 대조 HTML. 제40호(2)~(4)의 단순 신고서 변형은 제외. 기본사항만 합성값으로 채우며 전체 세액 계산이나 신고의 완결성을 의미하지 않는다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.mobile | customer.phone | 휴대전화 | phone | 010-5907-7253 |

### gov_land · 토지대장

그룹: 부동산 (`real_estate`)

토지대장 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=162454805&bylClsCd=110202

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.address | property.location | 토지소재 | text | 경기도 수원시 영통구 원천동 87 |
| official.owner | official.owner | 소유자 | text | 박찬연 |
| official.rrn | official.rrn | 등록번호 | rrn | 900210-1659382 |

### gov_local_assessment · 지방세 세목별 과세증명서

그룹: 세금·보험 (`tax`)

지방세 세목별 과세증명서 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169943579&bylClsCd=110202

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.company | corp.name | 상호 | text | 동방학원 |
| official.purpose | official.purpose | 사용목적 | text | 금융기관 제출용 |
| official.tax | official.tax | 세목 | text | 재산세 |
| official.period | official.period | 부과연월 | month | 2025.07 |
| official.amount | official.amount | 세액 | amount | 198,970,000 |

### gov_local_tax · 지방세 납세증명(신청)서

그룹: 세금·보험 (`tax`)

지방세 납세증명(신청)서 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169946943&bylClsCd=110202 앞쪽의 신청·증명 겸용 서식과 뒤쪽 확인사항을 모두 보존한다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| official.arrears | official.arrears | 유예내역 | text | 해당 없음 |

### gov_move_in · 전입세대확인서

그룹: 부동산 (`real_estate`)

전입세대확인서 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=167818343&bylClsCd=110202

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.address | property.location | 대상도로명주소 | text | 경기도 수원시 영통구 매탄로 376, 115동 2104호 |
| official.jibun | official.jibun | 대상지번주소 | text | 경기도 수원시 영통구 원천동 87 |
| official.head | official.head | 세대주 | text | 박찬연 |
| official.moved | official.moved | 전입일자 | date | 2020.05.08 |
| official.status | official.status | 등록구분 | text | 거주자 |

### gov_national_tax · 납세증명서

그룹: 세금·보험 (`tax`)

납세증명서 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/flDownload.do?bylClsCd=110202&flSeq=114053165&gubun=

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.purpose | official.purpose | 사용목적(기타) | text | 금융기관 제출용 |
| official.arrears | official.arrears | 연장·유예내역 | text | 해당 없음 |

### gov_pension · 국민연금가입자 증명서

그룹: 소득·재직 (`income`)

국민연금가입자 증명서 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=161706061&bylClsCd=110202 법령 별지 제11호 국민연금가입자 증명서로, 전자민원 가입증명서(국문)의 전체 이력 출력과는 다르다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.issued | official.issued | 발급일자 | date | 2026.01.31 |
| official.first_joined | official.first_joined | 최초자격취득일 | date | 2020.05.08 |
| official.type | official.type | 가입자종류 | text | 사업장가입자 |
| official.qual | official.qual | 자격취득일 | date | 2020.05.08 |

### gov_pension_withholding · 연금소득 원천징수영수증

그룹: 소득·재직 (`income`)

연금소득 원천징수영수증 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/flDownload.do?gubun=&flSeq=150204063&bylClsCd=110202

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.amount | official.amount | 총연금액 | amount | 74,880,000 |

### gov_resident_abstract · 주민등록표(초본)

그룹: 가족관계 (`family`)

주민등록표(초본) 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=167818367&bylClsCd=110202

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |

### gov_resident_copy · 주민등록표(등본)

그룹: 가족관계 (`family`)

주민등록표(등본) 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=167818361&bylClsCd=110202

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.head | official.head | 세대주 | text | 박찬연 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.row | official.row | 순번 | number | 1 |
| official.relation | official.relation | 세대주와의관계 | text | 본인 |
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |

### gov_retirement_withholding · 퇴직소득 원천징수영수증

그룹: 소득·재직 (`income`)

퇴직소득 원천징수영수증 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/flDownload.do?gubun=&flSeq=150204063&bylClsCd=110202

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.company | employer.name | 징수의무자상호 | text | 주식회사 태평양무역 |

### gov_seal · 인감증명서

그룹: 신원·신분 (`identity`)

인감증명서 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=145953337&bylClsCd=110202 인감 영역은 원본 직인·인감 이미지 없이 빈칸으로 유지한다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.nationality | customer.nationality | 국적 | text | 대한민국 |
| official.purpose | official.purpose | 일반용용도 | text | 금융기관 제출용 |

### gov_signature · 본인서명사실확인서

그룹: 신원·신분 (`identity`)

본인서명사실확인서 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=145951719&bylClsCd=110202 본인 서명란은 빈칸으로 유지한다.

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.purpose | official.purpose | 일반용도 | text | 금융기관 제출용 |

### gov_tax_payment_history · 납부내역증명

그룹: 세금·보험 (`tax`)

납부내역증명 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?flSeq=155626763&flNm=%5B%EB%B3%84%EC%A7%80+19%5D+%EB%82%A9%EB%B6%80%EB%82%B4%EC%97%AD%EC%A6%9D%EB%AA%85%28%EA%B5%AD%EB%AC%B8%29&bylClsCd=200203

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.company | corp.name | 상호 | text | 동방학원 |
| official.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 860-11-55034 |
| official.tax_year | official.tax_year | 귀속연도 | number | 2025 |
| official.tax_kind | official.tax_kind | 세목 | text | 종합소득세 |
| official.paid_on | official.paid_on | 납부일 | date | 2026.05.31 |
| official.paid | official.paid | 납부금액 | number | 96,990,000 |

### gov_vat_base · 부가가치세 과세표준증명

그룹: 세금·보험 (`tax`)

부가가치세 과세표준증명 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?flSeq=155626701&flNm=%5B%EB%B3%84%EC%A7%80+9%5D+%EB%B6%80%EA%B0%80%EA%B0%80%EC%B9%98%EC%84%B8%EA%B3%BC%EC%84%B8%ED%91%9C%EC%A4%80%EC%A6%9D%EB%AA%85%28%EA%B5%AD%EB%AC%B8%29&bylClsCd=200203

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.company | corp.name | 상호 | text | 동방학원 |
| official.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 860-11-55034 |
| official.biz_type | official.biz_type | 업태 | text | 서비스업 |
| official.biz_item | corp.biz_item | 종목 | text | 학원 |
| official.period_start | official.period_start | 과세기간시작 | date | 2025.01.01 |
| official.period_end | official.period_end | 과세기간종료 | date | 2025.06.30 |
| official.sales | official.sales | 매출과세표준 | number | 236,880,000원 |

### gov_vat_exempt_income · 면세사업자 수입금액증명

그룹: 개인사업자 (`business`)

면세사업자 수입금액증명 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?flSeq=155626713&flNm=%5B%EB%B3%84%EC%A7%80+11%5D+%EB%B6%80%EA%B0%80%EA%B0%80%EC%B9%98%EC%84%B8%EB%A9%B4%EC%84%B8%EC%82%AC%EC%97%85%EC%9E%90+%EC%88%98%EC%9E%85%EA%B8%88%EC%95%A1%EC%A6%9D%EB%AA%85%28%EA%B5%AD%EB%AC%B8%29&bylClsCd=200203

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.company | corp.name | 상호 | text | 동방학원 |
| official.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 860-11-55034 |
| official.biz_type | official.biz_type | 업태 | text | 서비스업 |
| official.biz_item | corp.biz_item | 종목 | text | 학원 |
| official.period | official.period | 과세기간 | text | 2025.01.01 ~ 2025.12.31 |
| official.income | official.income | 수입금액 | amount | 2,840,000원 |

### gov_withholding · 근로소득 원천징수영수증

그룹: 소득·재직 (`income`)

근로소득 원천징수영수증 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/flDownload.do?gubun=&flSeq=150204063&bylClsCd=110202

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.company | employer.name | 징수의무자상호 | text | 주식회사 태평양무역 |
| official.biz_no | official.biz_no | 사업자등록번호 | biz_no | 501-82-42625 |
| official.name | customer.name | 성명 | text | 박찬연 |
| official.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.salary | official.salary | 급여 | amount | 54,600,000 |

### hana_collateral_agreement · 근저당권설정계약서(근담보용)

그룹: 하나은행 서식(원본) (`hana`)

근저당권설정계약서(근담보용) 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://image.kebhana.com/cont/download/documents/provide/0000000001049_20211126.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 채무자 | text | 박찬연 |
| official.address | customer.address | 채무자주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.amount | official.amount | 채권최고액 | amount | 4,660,000 |
| official.name_copy | official.name_copy | 채무자 | text | 박찬연 |
| official.address_copy | official.address_copy | 채무자주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.amount_copy | official.amount_copy | 채권최고액 | amount | 4,660,000 |

### hana_corporate_agreement · 여신거래약정서(기업용)

그룹: 하나은행 서식(원본) (`hana`)

여신거래약정서(기업용) 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://image.kebhana.com/cont/download/documents/provide/0000003061032_20260630.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 채무자 | text | (주)유니온무역 |
| official.address | customer.address | 주소 | text | 서울특별시 중구 다산로 361, 6층 |
| official.amount | official.amount | 여신금액 | amount | 3,000,000,000 |
| official.subject | official.subject | 여신과목 | text | 일반자금대출 |
| terms.method | terms.method | 개별거래 | checkbox | 개별거래 |
| terms.fixed | terms.fixed | 고정금리 | checkbox | 고정금리 |
| terms.fixed_choice | terms.fixed_choice | 확정금리 | checkbox | 확정금리 |
| terms.rate | terms.rate | 약정이율 | number | 4.98 |
| terms.repay | terms.repay | 만기일시상환 | checkbox | 만기일시상환 |
| terms.execution | terms.execution | 전액실행 | checkbox | 전액실행 |
| terms.start0 | terms.start0 | 개시일년 | number | 26 |
| terms.start1 | terms.start1 | 개시일월 | number | 02 |
| terms.start2 | terms.start2 | 개시일일 | number | 03 |
| terms.end0 | terms.end0 | 만료일년 | number | 27 |
| terms.end1 | terms.end1 | 만료일월 | number | 02 |
| terms.end2 | terms.end2 | 만료일일 | number | 03 |
| terms.written0 | terms.written0 | 작성일년 | number | 26 |
| terms.written1 | terms.written1 | 작성일월 | number | 2 |
| terms.written2 | terms.written2 | 작성일일 | number | 3 |
| official.name_copy | official.name_copy | 채무자 | text | (주)유니온무역 |
| official.address_copy | official.address_copy | 주소 | text | 서울특별시 중구 다산로 361, 6층 |
| official.amount_copy | official.amount_copy | 여신금액 | amount | 3,000,000,000 |
| official.subject_copy | official.subject_copy | 여신과목 | text | 일반자금대출 |
| terms.method_copy | terms.method_copy | 개별거래 | checkbox | 개별거래 |
| terms.fixed_copy | terms.fixed_copy | 고정금리 | checkbox | 고정금리 |
| terms.fixed_choice_copy | terms.fixed_choice_copy | 확정금리 | checkbox | 확정금리 |
| terms.rate_copy | terms.rate_copy | 약정이율 | number | 4.98 |
| terms.repay_copy | terms.repay_copy | 만기일시상환 | checkbox | 만기일시상환 |
| terms.execution_copy | terms.execution_copy | 전액실행 | checkbox | 전액실행 |
| terms.start0_copy | terms.start0_copy | 개시일년 | number | 26 |
| terms.start1_copy | terms.start1_copy | 개시일월 | number | 02 |
| terms.start2_copy | terms.start2_copy | 개시일일 | number | 03 |
| terms.end0_copy | terms.end0_copy | 만료일년 | number | 27 |
| terms.end1_copy | terms.end1_copy | 만료일월 | number | 02 |
| terms.end2_copy | terms.end2_copy | 만료일일 | number | 03 |
| terms.written0_copy | terms.written0_copy | 작성일년 | number | 26 |
| terms.written1_copy | terms.written1_copy | 작성일월 | number | 2 |
| terms.written2_copy | terms.written2_copy | 작성일일 | number | 3 |

### hana_official_001 · 상속예금 명의변경(지급) 의뢰서 및 손해담보 확약서(상속예금 지급 위임장 겸용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 상속예금 명의변경(지급) 의뢰서 및 손해담보 확약서(상속예금 지급 위임장 겸용). 기존 hf001 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2026/09/07/5-08-0084.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 예금주 | text | 박찬연 |
| check.지급구분 | check.지급구분 | 지급구분 | checkbox | 지급 |
| customer.birth | customer.birth | 생년월일 | date | 900210 |
| 사망일자 | 사망일자 | 사망일자 | date | 2025.04.21 |
| 목록[].상품명 | 목록[].상품명 | 상품명 | text | 청년도약계좌 |
| 목록[].계좌번호 | 목록[].계좌번호 | 계좌번호 | text | 324-375150-71588 |
| 목록[].금액 | 목록[].금액 | 금액 | text | 32,350,000원 |
| check.보기1 | check.보기1 | 보기1 | checkbox | 보기1 |
| check.보기12 | check.보기12 | 보기1 | checkbox | 보기1 |
| check.보기13 | check.보기13 | 보기1 | checkbox | 보기1 |
| check.보기14 | check.보기14 | 보기1 | checkbox | 보기1 |
| check.보기15 | check.보기15 | 보기1 | checkbox | 보기1 |
| check.명의변경 | check.명의변경 | 명의변경 | checkbox | □ |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 기타특약사항 | 기타특약사항 | 기타특약사항 | text | 해당 없음 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김원경 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 천은윤 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 현민은 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 검인 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 류원주 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 이정영 |
| check.주된상속인 | check.주된상속인 | 주된상속인(소득귀속인) | checkbox | 본인 |
| check.상속인 | check.상속인 | 상속인 | checkbox | 본인 |
| check.상속인2 | check.상속인2 | 상속인 | checkbox | 본인 |
| check.상속인3 | check.상속인3 | 상속인 | checkbox | 본인 |
| check.상속인4 | check.상속인4 | 상속인 | checkbox | 위임(주된 상속인 앞) |
| check.상속인5 | check.상속인5 | 상속인 | checkbox | 위임(주된 상속인 앞) |
| 목록[].성명 | 목록[].성명 | 성명 | text | 왕규희 |
| 목록[].생년월일 | 목록[].생년월일 | 생년월일 | text | 2025년 4월 3일 |
| 목록[].연락처 | 목록[].연락처 | 연락처 | text | 010-5907-7253 |
| 목록[].예금잔액 | 목록[].예금잔액 | 예금잔액 | text | 750,000원 |
| 목록[].미지급사유주1 | 목록[].미지급사유주1 | 미지급사유주1 | text | 만기 해지 |
| 목록[].상속인확인 | 목록[].상속인확인 | 상속인확인 | text |  |
| signer.name | signer.name | 확인담당자 | text | 김주우 |
| seal.signer | seal.signer | 확인담당자 | seal | 김주우 |
| sign.signer | sign.signer | 확인담당자 | signature | 김민빈 |
| signer2.name | signer2.name | 확인책임자 | text | 이우승 |
| seal.signer2 | seal.signer2 | 확인책임자 | seal | 채규도 |
| sign.signer2 | sign.signer2 | 확인책임자 | signature | 이우승 |

### hana_official_003 · 은행거래신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 은행거래신청서. 기존 hf003 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2026/06/19/3-08-1016.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| seal.signer | seal.signer | 한도:₩..~.. | seal | 강순준 |
| sign.signer | sign.signer | 한도:₩..~.. | signature | 박찬연 |
| seal.signer2 | seal.signer2 | 한도:₩..~.. | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 한도:₩..~.. | signature | 이욱유 |
| seal.signer3 | seal.signer3 | 한도:₩..~.. | seal | 박찬연 |
| sign.signer3 | sign.signer3 | 한도:₩..~.. | signature | 이욱유 |
| seal.signer4 | seal.signer4 | 고객정보변경없음 | seal | 강순준 |
| sign.signer4 | sign.signer4 | 고객정보변경없음 | signature | 박찬연 |
| check.비과세종합저축재형저축 | check.비과세종합저축재형저축 | 비과세종합저축/재형저축/주택청약상품의계약금액/한도/중복 | checkbox | 비과세종합저축 / 재형저축 / 주택청약상품의 계약금액 / 한도 / 중복  |
| check.귀행에대한제대출금보증채 | check.귀행에대한제대출금보증채 | 귀행에대한제대출금,보증채무,신용카드채무에대하여변제기가도래하 | checkbox | 귀행에 대한 제 대출금, 보증채무, 신용카드채무에 대하여 변제기가 도래하 |
| check.본인은금융지주회사법제4 | check.본인은금융지주회사법제4 | 본인은금융지주회사법제48조의2에근거하여하나금융그룹내지주사및자 | checkbox | 본인은 금융지주회사법 제48조의2에 근거하여 하나금융그룹내 지주사 및 자 |
| official.name | customer.name | 성명 | text | 박찬연 |
| official.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.name_en | customer.name_en | 영문명 | text | PARK CHANYEON |
| official.phone | customer.phone | 휴대폰 | phone | 010-5907-7253 |
| official.email | customer.email | 이메일 | text | chanyeon363@naver.com |

### hana_official_006 · 자동이체 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 자동이체 신청서. 기존 hf006 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2025/11/27/3-11-0012.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| signer.name | customer.name | 예금자성명 | text | 박찬연 |
| seal.signer | seal.customer | 예금자성명 | seal | 박찬연 |
| sign.signer | sign.customer | 예금자성명 | signature | 강순준 |
| account | account | 출금계좌번호 | account_no | 000-287736-52424 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 변경후출금계좌번호 | 변경후출금계좌번호 | 변경후출금계좌번호 | text | 해당 없음 |
| check.신청구분 | check.신청구분 | 신청구분( | checkbox | 변경 |
| check.이체일이휴일인경우 | check.이체일이휴일인경우 | [당행요구불계좌이체,타행자동이체]이체일이휴일인경우 | checkbox | 전 영업일 |
| check.신청구분2 | check.신청구분2 | 신청구분( | checkbox | 변경 |
| check.이체일이휴일인경우2 | check.이체일이휴일인경우2 | [당행요구불계좌이체,타행자동이체]이체일이휴일인경우 | checkbox | 익 영업일 이체를 신청합니다. |
| 은행 | 은행 | 은행 | text | 카카오뱅크 |
| 지급인자내용 | 지급인자내용 | 지급인자내용 | text | 해당 없음 |
| 은행2 | 은행2 | 은행 | text | 카카오뱅크 |
| 지급인자내용2 | 지급인자내용2 | 지급인자내용 | text | 해당 없음 |
| check.자동이체기간만료SMS통지 | check.자동이체기간만료SMS통지 | 자동이체기간만료SMS통지( | checkbox | 신청 |
| 목록[].예금주명 | 목록[].예금주명 | 예금주명 | text |  |
| check.자동이체기간만료SMS통지2 | check.자동이체기간만료SMS통지2 | 자동이체기간만료SMS통지( | checkbox | 미신청 |
| 목록[].이체일 | 목록[].이체일 | 이체일 | date | 2025.04.29 |
| 목록[].이체주기 | 목록[].이체주기 | 이체주기(일☞주☞월☞년) | text |  |
| 목록[].이체금액 | 목록[].이체금액 | 이체금액 | number | 450,000 |
| 입금인자내용 | 입금인자내용 | 입금인자내용 | text | 해당 없음 |
| 입금인자내용2 | 입금인자내용2 | 입금인자내용 | text | 해당 없음 |
| check.수수료포함출금 | check.수수료포함출금 | 수수료포함출금( | checkbox | 미신청 |
| date | date | 일자 | date | 2026년 1월 31일 |
| check.수수료포함출금2 | check.수수료포함출금2 | 수수료포함출금( | checkbox | 미신청 |
| date2 | date2 | 일자 | date | 2026년 1월 31일 |
| date3 | date3 | 년월일 | date | 2026년 1월 31일 |
| date4 | date4 | 년월일 | date | 2026년 1월 31일 |
| account2 | account2 | 입금계좌번호 | account_no | 000-287736-52424 |
| check.만기이연시선택 | check.만기이연시선택 | [정액적립식]만기이연시선택 | checkbox | 만기일 |
| check.갱신구분 | check.갱신구분 | 갱신구분 | checkbox | 원리금지급 |
| check.계약서류수령방법 | check.계약서류수령방법 | 계약서류*수령방법 | checkbox | 별도 연락처로 수령( |
| account3 | account3 | 입금계좌 | account_no | 000-287736-52424 |
| check.자동이체정지 | check.자동이체정지 | 자동이체정지 | checkbox | 등록 |
| 구분 | 구분 | 구분 | text |  |
| 관리비지로공과금기타_목록[].수납기관 | 관리비지로공과금기타_목록[].수납기관 | 수납기관(아파트,상가) | text |  |
| 수납기관 | 수납기관 | 수납기관(아파트,상가) | text |  |
| 관리비지로공과금기타_목록[].납부자번호 | 관리비지로공과금기타_목록[].납부자번호 | 납부자번호(동,호수,수용가번호,등) | text | 582784-8446534 |
| 납부자번호 | 납부자번호 | 납부자번호(동,호수,수용가번호,등) | text | 2407-9826 |
| 관리비지로공과금기타_목록[].지로번호기관코드 | 관리비지로공과금기타_목록[].지로번호기관코드 | 지로번호/기관코드 | number | 062638 |
| 지로번호기관코드 | 지로번호기관코드 | 지로번호/기관코드 | number | 131690 |
| 관리비지로공과금기타_목록[].납부희망일 | 관리비지로공과금기타_목록[].납부희망일 | 납부희망일 | date | 2025.12.05 |
| date5 | date5 | 작성일 | date | 2026년 1월 31일 |
| check.계좌간자동이체 | check.계좌간자동이체 | 계좌간자동이체( | checkbox | 납부자 자동이체 |
| check.만기해지자동이체 | check.만기해지자동이체 | 만기해지자동이체( | checkbox | 해지 |
| check.자동갱신자동이체 | check.자동갱신자동이체 | 자동갱신(재예치)자동이체( | checkbox | 해지 |
| check.기타자동이체 | check.기타자동이체 | 기타자동이체( | checkbox | 변경 |
| check.계좌번호 | check.계좌번호 | 계좌번호 | checkbox | 적용 |
| check.조회 | check.조회 | 조회 | checkbox | 조회 |
| check.고객명 | check.고객명 | 고객명 | checkbox | 적용 |

### hana_official_011 · 예금(신탁)잔액증명 의뢰서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 예금(신탁)잔액증명 의뢰서. 기존 hf011 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2025/01/07/5-08-0094.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 해제 |
| check.대상계좌 | check.대상계좌 | 대상계좌(발급세부) | checkbox | 전체계좌 |
| check.대상계좌2 | check.대상계좌2 | 대상계좌(발급세부) | checkbox | 발급용도 |
| check.수령방법 | check.수령방법 | 수령방법 | checkbox | 카카오톡(문자) |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| account2 | account2 | 계좌번호 | account_no | 000-287736-52424 |
| account3 | account3 | 계좌번호 | account_no | 000-287736-52424 |
| check.기준일자 | check.기준일자 | 기준일자 | checkbox | 매월 |
| check.유효기간 | check.유효기간 | 유효기간 | checkbox | 보기1 |
| check.창구수령대리인 | check.창구수령대리인 | 창구수령대리인 | checkbox | 생년월일 |
| check.우편수령대리인 | check.우편수령대리인 | 우편수령대리인 | checkbox | 성명 |
| 발급기준일 | 발급기준일 | 발급기준일 | date | 2025-04-27 |
| 국문 | 국문 | 국문 | number | 36 |
| 매 | 매 | 매 | number | 36 |
| 계좌번호_목록[].value | 계좌번호_목록[].value | (통화코드:) | amount |  |
| check.수령방법2 | check.수령방법2 | 수령방법 | checkbox | E-mail |
| 발급부수 | 발급부수 | 발급부수 | text |  |
| 발급부수2 | 발급부수2 | 발급부수 | text |  |
| signer.name | customer.name | 성명(상호명) | text | 박찬연 |
| seal.signer | seal.customer | 성명(상호명) | seal | 이욱유 |
| sign.signer | sign.customer | 성명(상호명) | signature | 박찬연 |
| customer.name_en | customer.name_en | 영문명 | text | PARK CHANYEON |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.birth | customer.birth | 생년월일(사업자번호) | date | 1990.02.10 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| agent.name | agent.name | 대리인성명 | text | 박영준 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.본인은상기계좌의 | check.본인은상기계좌의 | 본인은상기계좌의( | checkbox | 정기발급 신청) 과 관련한 일체의 행위를 상기 대리인에게 |
| agent.birth | agent.birth | 생년월일 | date | 1962년 12월 19일 |
| agent.phone | agent.phone | 연락처 | phone | 010-6515-4769 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 확인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 정윤희 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 박우인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 임윤성 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 최원찬 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 하소하 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 이민진 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 검인 |

### hana_official_015 · 통합제신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 통합제신고서. 기존 hf015 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2024/02/02/3-08-1280_240202.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.성명휴대폰번호자택주소직장원본수익자수익수익자 | check.성명휴대폰번호자택주소직장원본수익자수익수익자 | 성명(업체명)휴대폰번호자택주소직장원본수익자수익수익자 | checkbox | 기타 |
| 신청내용 | 신청내용 | 신청내용 | text | 해당 없음 |
| 변경내용 | 변경내용 | 변경내용 | text | 해당 없음 |
| 변경전 | 변경전 | 변경전 | text | 해당 없음 |
| seal.signer | seal.customer | 인감(서명) | seal | 박찬연 |
| sign.signer | sign.customer | 인감(서명) | signature | 강순준 |
| 변경후 | 변경후 | 변경후 | text | 해당 없음 |
| Email또는휴대폰번호 | Email또는휴대폰번호 | E-mail또는휴대폰번호 | phone | 010-5907-7253 |
| 연락처Email기타 | 연락처Email기타 | 연락처,E-mail,기타 | text | 해당 없음 |
| 수령확인 | 수령확인 | 수령확인 | text |  |
| account | account | 출금계좌번호 | account_no | 000-287736-52424 |
| customer.name | customer.name | 성명(업체명) | text | 박찬연 |
| 신고인 | 신고인 | ⇁신고인 | text |  |
| 본인과의관계 | 본인과의관계 | ⇁본인과의관계 | text |  |
| 연락처 | 연락처 | )⇁연락처 | phone | 010-5907-7253 |
| 상품명 | 상품명 | ⇁상품명 | text | 하나의정기예금 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 대리인 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인 | seal | 박영준 |
| sign.signer2 | sign.agent | 대리인 | signature | 강석호 |
| 제신고내용 | 제신고내용 | ⇁제신고(내용 | text | 해당 없음 |
| value | value | [유선신고사항] | amount |  |
| agent.name | agent.name | 대리인성명 | text | 박영준 |
| agent.phone | agent.phone | 연락처 | phone | 010-6515-4769 |
| 위임내용 | 위임내용 | 위임내용 | text | 해당 없음 |
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer3.name | signer3.name | 위임인 | text | 박찬연 |
| seal.signer3 | seal.signer3 | 위임인 | seal | 강순준 |
| sign.signer3 | sign.signer3 | 위임인 | signature | 박찬연 |
| 위임장 | 위임장 | 위임장 | text |  |

### hana_official_024 · 금융거래정보제공(요구·동의)서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 금융거래정보제공(요구·동의)서. 기존 hf024 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2021/09/07/5-08-0016_200508.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.구분 | check.구분 | 구분 | checkbox | 요구 |
| check.신청항목 | check.신청항목 | 신청항목 | checkbox | 거래내역 조회 |
| check.신청항목2 | check.신청항목2 | 신청항목 | checkbox | 한도조회 및 |
| check.신청항목3 | check.신청항목3 | 신청항목 | checkbox | 기타 조회 |
| check.전금융기관한도및중복가입 | check.전금융기관한도및중복가입 | 전금융기관한도및중복가입제한상품 | checkbox | 전 금융기관 한도 및 중복가입 제한 상품 |
| check.금융거래종합보고서 | check.금융거래종합보고서 | 금융거래종합보고서 | checkbox | 금융거래종합보고서 |
| check.계좌번호 | check.계좌번호 | 계좌번호 | checkbox | 전체 |
| check.대상기간 | check.대상기간 | 대상기간 | checkbox | 최근 3개월 |
| check.대상기간2 | check.대상기간2 | 대상기간 | checkbox | 대출이자 |
| check.신청추가 | check.신청추가 | 신청추가 | checkbox | 추가요청사항 |
| check.신청추가2 | check.신청추가2 | 신청추가 | checkbox | 수수료 출금동의 |
| check.계좌번호마스킹제외 | check.계좌번호마스킹제외 | 계좌번호마스킹제외 | checkbox | 영문주소 표시 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| 출금금액 | 출금금액 | 출금금액 | number | 8,100,000원 |
| 거래정보등의제공목적 | 거래정보등의제공목적 | 거래정보등의제공목적 | text | 급여 수령 |
| check.동의서유효기간 | check.동의서유효기간 | 동의서유효기간 | checkbox | 보기1 |
| check.정보제공사실의통보여부 | check.정보제공사실의통보여부 | 정보제공사실의통보여부 | checkbox | 통보 요청 |
| customer.name | customer.name | 성명(사업자명) | text | 박찬연 |
| customer.birth | customer.birth | 생년월일(사업자번호) | date | 1990.02.10 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| signer.name | signer.name | 성명(사업자명) | text | 박찬연 |
| seal.signer | seal.customer | 성명(사업자명) | seal | 이욱유 |
| sign.signer | sign.customer | 성명(사업자명) | signature | 현예지 |
| customer.phone2 | customer.phone2 | 연락처 | phone | 010-5907-7253 |
| customer.birth2 | customer.birth2 | 생년월일(사업자번호) | date | 1990.02.10 |
| 반출신청email | 반출신청email | 반출신청e-mail | text |  |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| signer2.name | signer2.name | 예금주 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 예금주 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 예금주 | signature | 강순준 |
| check.대리인을통하여금융거래정보제공을요청하는경우 | check.대리인을통하여금융거래정보제공을요청하는경우 | 대리인을통하여금융거래정보제공을요청하는경우 | checkbox | 요구에 체크 표시한 후 금융거래자 본인란을 기재한다. |
| check.본인이제3자앞정보제공에동의하는경우 | check.본인이제3자앞정보제공에동의하는경우 | 본인이제3자앞정보제공에동의하는경우 | checkbox | 동의에 체크 표시한 후 금융거래정보 등의 제공 동의시 기재사항을 기재하고 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 곽훈승 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 검인 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 확인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 기예유 |

### hana_official_028 · 위임장

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 위임장. 기존 hf028 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/29/5_08_0041_20200601.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.해당 | check.해당 | 해당 | checkbox | 에 √ 표시하며 기타의 경우 구체적인 위임내용을 기재합니다 |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.신규계좌개설 | check.신규계좌개설 | 신규계좌개설 | checkbox | 기타 ( |
| check.신규계좌개설2 | check.신규계좌개설2 | 신규계좌개설 | checkbox | 개인(신용)정보 수집 이용 및 제공 동의서(상품서비스 안내 등) 작성 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| check.세부내용 | check.세부내용 | 세부내용 | checkbox | 통장/인감 분실 |
| 기타사항 | 기타사항 | 기타사항 | text | 서류 챙겨서 5일 뒤 재방문 |
| agent.birth | agent.birth | 생년월일 | date | 1962.12.19 |
| agent.phone | agent.phone | 연락처 | phone | 010-6515-4769 |
| 위임내용확인일시 | 위임내용확인일시 | 위임내용확인일시 | text |  |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| signer.name | signer.name | 성명(업체명) | text | 박찬연 |
| seal.signer | seal.customer | 성명(업체명) | seal | 박찬연 |
| sign.signer | sign.customer | 성명(업체명) | signature | 이욱유 |
| customer.birth | customer.birth | 생년월일(사업자번호) | date | 1990-02-10 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이훈하 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 이도유 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 민숙수 |

### hana_official_029 · 사용인감계(금융계좌개설용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 사용인감계(금융계좌개설용). 기존 hf029 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0056_200508.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| seal.signer | seal.customer | 사용인감 | seal | 이욱유 |
| sign.signer | sign.customer | 사용인감 | signature | 박찬연 |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.phone | agent.phone | 연락처(선택항목) | phone | 010-6515-4769 |
| agent.address | agent.address | 주소(선택항목) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.birth | agent.birth | 생년월일 | date | 1962.12.19 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| 취급점 | 취급점 | 취급점 | text | 범어지점 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| company.name | corp.name | 법인명 | text | (주)유니온무역 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| customer.address | customer.address | 주소(선택항목) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.ceo | corp.ceo | 대표자명 | text | 박찬연 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김용민 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김선주 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 고찬하 |

### hana_official_047 · 대출상담 및 신청서(한국주택금융공사채권유동화목적 보금자리론용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 대출상담 및 신청서(한국주택금융공사채권유동화목적 보금자리론용). 기존 hf047 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2026/07/30/3-06-1104.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신청금액 | 신청금액 | 신청금액 | number | 8,110,000 |
| check.자금용도 | check.자금용도 | 자금용도 | checkbox | 상환 |
| check.주택보유수 | check.주택보유수 | 주택보유수(본건담보주택제외) | checkbox | 무주택 |
| check.담보제공자 | check.담보제공자 | 담보제공자 | checkbox | 배우자 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.rrn | customer.rrn | 주민번호앞6자리 | number | 900210 |
| check.결혼여부 | check.결혼여부 | 결혼여부 | checkbox | 미혼 |
| employer.name | employer.name | 직장명 | text | 주식회사 태평양무역 |
| 부서직위 | 부서직위 | 부서/직위 | text |  |
| check.직업구분 | check.직업구분 | 직업구분 | checkbox | 급여소득자 |
| 근무기간 | 근무기간 | 근무기간(업력) | number | 1 |
| customer.phone | customer.phone | 전화번호 | phone | 010-5907-7253 |
| 소득 | 소득 | 소득(합계) | number | 9,680,000 |
| 부채 | 부채 | 부채(합계) | number | 242,690,000원 |
| 금융기관 | 금융기관 | 금융기관 | text | 기업은행 |
| 금융기관2 | 금융기관2 | 금융기관 | text | 신한은행 |
| customer.name2 | customer.name2 | 성명 | text | 박찬연 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.rrn2 | customer.rrn2 | 주민번호앞6자리 | number | 900210 |
| employer.name2 | employer.name2 | 직장명 | text | 주식회사 태평양무역 |
| 부서직위2 | 부서직위2 | 부서/직위 | text |  |
| check.직업구분2 | check.직업구분2 | 직업구분 | checkbox | 연금생활자 |
| 근무기간2 | 근무기간2 | 근무기간(업력) | number | 2 |
| customer.phone2 | customer.phone2 | 전화번호 | phone | 010-5907-7253 |
| 소득2 | 소득2 | 소득(합계) | number | 17,150,000 |
| 부채2 | 부채2 | 부채(합계) | number | 22,780,000 |
| 금융기관3 | 금융기관3 | 금융기관 | text | 우리은행 |
| 금융기관4 | 금융기관4 | 금융기관 | text | 하나은행 |
| check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까 | check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까 | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 안내 받음 (구두, 우편, 이메일, 팩스, 직접 수령) |
| check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2 | check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2 | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 원하지 않음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인(본인) | text | 박찬연 |
| seal.signer | seal.customer | 신청인(본인) | seal | 현예지 |
| sign.signer | sign.customer | 신청인(본인) | signature | 박찬연 |
| signer2.name | signer2.name | 상담자확인 | text | 장소연 |
| seal.signer2 | seal.signer2 | 상담자확인 | seal | 석철율 |
| sign.signer2 | sign.signer2 | 상담자확인 | signature | 장소연 |
| 계약기간 | 계약기간 | 계약기간 | text |  |
| 자택 | 자택 | 자택 | text |  |
| customer.phone3 | customer.phone3 | 핸드폰 | phone | 010-5907-7253 |
| 대출금액 | 대출금액 | 대출금액 | number | 88.13 |
| 대출금액2 | 대출금액2 | 대출금액 | number | 20.18 |
| 자택2 | 자택2 | 자택 | text |  |
| customer.phone4 | customer.phone4 | 핸드폰 | phone | 010-5907-7253 |
| 대출금액3 | 대출금액3 | 대출금액 | number | 9.89 |
| 대출금액4 | 대출금액4 | 대출금액 | number | 179.89 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김연주 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 우원준 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 김영아 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 금훈성 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 확인 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 임용유 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 최경율 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 장우준 |
| customer.name3 | customer.name3 | 성명 | text | 박찬연 |
| customer.address3 | customer.address3 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| employer.name3 | employer.name3 | 직장명 | text | 주식회사 태평양무역 |
| check.상담희망전화 | check.상담희망전화 | 상담희망전화 | checkbox | 직장 또는 자택 |
| customer.phone5 | customer.phone5 | 전화번호 | phone | 010-5907-7253 |
| check.주택보유수2 | check.주택보유수2 | 주택보유수(본건담보주택제외) | checkbox | 무주택 |
| 대출신청금액 | 대출신청금액 | 대출신청금액 | number | 199,730,000 |
| check.대출만기 | check.대출만기 | 대출만기 | checkbox | 년 / |
| 희망취급기관 | 희망취급기관 | 희망취급기관 | text |  |
| 대출희망일 | 대출희망일 | 대출희망일 | date | 2025.08.03 |
| 거치기간 | 거치기간 | 거치기간 | text |  |
| 소유권이전등기일 | 소유권이전등기일 | 소유권이전등기일 | date | 2026년 9월 29일 |
| 담보주택소재지 | 담보주택소재지 | 담보주택소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.주택유형 | check.주택유형 | 주택유형 | checkbox | 오피스텔 |
| check.소유자 | check.소유자 | 소유(예정)자 | checkbox | 부부공동 |
| check.담보제공자2 | check.담보제공자2 | 담보제공자 | checkbox | 배우자 |
| check.본건설정순위 | check.본건설정순위 | 본건설정순위 | checkbox | 순위 |
| 임대계약건수 | 임대계약건수 | 임대계약건수 | number | 24 |
| 임대보증금합계액 | 임대보증금합계액 | 임대보증금합계액 | number | 6,720,000 |
| check.전용면적 | check.전용면적 | 전용면적 | checkbox | m2이하 |
| check.규제지역해당 | check.규제지역해당 | 규제지역해당 | checkbox | 아니오 |
| check.소득증명 | check.소득증명 | 소득증명 | checkbox | 배우자 |
| 본인부채 | 본인부채 | 본인부채 | text |  |
| 제외부채 | 제외부채 | 제외부채 | text |  |
| 02p | 02p | 0.2%p | text |  |
| customer.rrn3 | customer.rrn3 | 주민번호앞6자리 | number | 900210 |
| check.결혼여부2 | check.결혼여부2 | 결혼여부 | checkbox | 미혼 |
| check.배우자세대분리 | check.배우자세대분리 | 배우자세대분리 | checkbox | 예 |
| spouse.name | family.name | 배우자성명 | text | 이도민 |
| 배우자주민번호앞6자리 | 배우자주민번호앞6자리 | 배우자주민번호앞6자리 | text | 579525-2995846 |
| check.상환방식 | check.상환방식 | 상환방식 | checkbox | 원리금균등 |
| 희망취급지점 | 희망취급지점 | 희망취급지점 | text | 범어지점 |
| 변동금리기간 | 변동금리기간 | 변동금리기간 | number | 4.90 |
| check.자금용도2 | check.자금용도2 | 자금용도 | checkbox | 구입 |
| check.최저층여부 | check.최저층여부 | 최저층여부 | checkbox | 아니오 |
| check.선순위종류 | check.선순위종류 | 선순위종류 | checkbox | 보금자리론 |
| 선순위설정금액 | 선순위설정금액 | 선순위설정금액 | number | 250,000 |
| 총방수 | 총방수 | 총방수 | text |  |
| 임대방수 | 임대방수 | 임대방수 | number | 4 |
| check.건물등기부등본 | check.건물등기부등본 | 건물등기부등본 | checkbox | 없음(아파트 후취담보) |
| check.녹색건축물여부 | check.녹색건축물여부 | 녹색건축물여부 | checkbox | 아니오 |
| 배우자부채 | 배우자부채 | 배우자부채 | text |  |
| 제외대출 | 제외대출 | 제외대출 | text |  |
| 종류 | 종류 | 종류 | text | 하나 적금 |
| employer.name4 | employer.name4 | 소속 | text | 주식회사 태평양무역 |
| 발급기관 | 발급기관 | 발급기관 | text |  |
| 발급일자 | 발급일자 | 발급일자 | date | 2025.04.13 |
| customer.name4 | customer.name4 | 성명 | text | 박찬연 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer3.name | signer3.name | 신청인(본인) | text | 박찬연 |
| seal.signer3 | seal.signer3 | 신청인(본인) | seal | 강순준 |
| sign.signer3 | sign.signer3 | 신청인(본인) | signature | 박찬연 |
| 협회코드 | 협회코드 | 협회코드(대출상담사) | number | 2875 |

### hana_official_048 · 가계형소호 여신차입신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 가계형소호 여신차입신청서. 기존 hf048 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/10/20/b000005060519_20251020.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 채무인수 |
| check.신청인구분 | check.신청인구분 | 신청인구분 | checkbox | 담보제공자 |
| check.여신신청인의 | check.여신신청인의 | 여신신청인()의 | checkbox | 기타( |
| 고객번호 | 고객번호 | 고객번호 | rrn | 7021-1790 |
| check.우편물수령처 | check.우편물수령처 | 우편물수령처 | checkbox | 사업장 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.address | customer.address | 자택주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| company.address | corp.address | 사업장주소 | text | 서울특별시 중구 다산로 361, 6층 |
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| check.직업군 | check.직업군 | 직업군 | checkbox | 자영업자 |
| company.name | corp.name | 업체명(상호) | text | (주)유니온무역 |
| check.매출정보 | check.매출정보 | 매출(소득)정보 | checkbox | 세무서신고 |
| check.사업장소유여부 | check.사업장소유여부 | 사업장소유여부 | checkbox | 기타( |
| 월임차료 | 월임차료 | 월임차료 | number | 2,560,000 |
| check.자가 | check.자가 | 자가( | checkbox | 전세 |
| check.주거형태코드 | check.주거형태코드 | 주거형태코드 | checkbox | 오피스텔 |
| check.부채현황취급예정포함 | check.부채현황취급예정포함 | 부채현황(단위:백만원)【취급예정포함】 | checkbox | 금융기관명( |
| 종류 | 종류 | 종류 | text | 하나 정기예금 |
| 평가금액 | 평가금액 | 평가금액 | number | 3,420,000원 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 월관리비 | 월관리비 | 월관리비 | number | 9,060,000 |
| 면적 | 면적 | 면적 | text |  |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| customer.home_phone | customer.home_phone | 자택전화번호 | phone | 02-9704-4847 |
| 사업장전화번호 | 사업장전화번호 | 사업장전화번호 | phone | 010-5907-7253 |
| check.국적 | check.국적 | 국적 | checkbox | 기타 ( |
| company.biz_item | corp.biz_item | 업종(주요제품) | text | 무역 |
| 연매출 | 연매출 | 연매출(연소득) | number | 20,080,000 |
| 임차보증금 | 임차보증금 | 임차보증금 | number | 4,620,000 |
| company.address2 | company.address2 | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| check.공동대표여부 | check.공동대표여부 | 공동대표여부 | checkbox | 아니오 |
| 종업원수 | 종업원수 | 종업원수 | number | 1 |
| check.담보종류 | check.담보종류 | 담보종류 | checkbox | 대지 |
| check.임대차확인 | check.임대차확인 | 임대차확인 | checkbox | 있음(임대보증금 백만원) |
| 소유자명 | 소유자명 | 소유자명 | text |  |
| 신청금액 | 신청금액 | 신청금액 | number | 73,310,000 |
| check.상환방법 | check.상환방법 | 상환방법 | checkbox | 원리금균등분할 |
| check.자금용도 | check.자금용도 | 자금용도 | checkbox | 운전자금 |
| date | date | 대출희망일 | date | 2026년 1월 31일 |
| 대출과목 | 대출과목 | 대출과목 | text | 일반자금대출 |
| check.거래구분 | check.거래구분 | 거래구분 | checkbox | 한도 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 여신신청인(본인) | text | 박찬연 |
| seal.signer | seal.customer | 여신신청인(본인) | seal | 강순준 |
| sign.signer | sign.customer | 여신신청인(본인) | signature | 박찬연 |
| signer2.name | related.name | 담보제공자(또는연대보증인또는공동사업자) | text | 한성주 |
| seal.signer2 | seal.related | 담보제공자(또는연대보증인또는공동사업자) | seal | 최주승 |
| sign.signer2 | sign.related | 담보제공자(또는연대보증인또는공동사업자) | signature | 한성주 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 고재민 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 윤현승 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 원유성 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 한영도 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 검인 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 황찬서 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 민건아 |
| check.신규증액처리시안내 | check.신규증액처리시안내 | 신규,증액처리시안내 | checkbox | 원치않음 |
| check.동의함 | check.동의함 | 동의함( | checkbox | 원치않음 |
| check.중도상환해약금면제시점도래안내문자통지 | check.중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | checkbox | 원치않음 |
| check.우편 | check.우편 | 우편 | checkbox | 자택 |
| check.문자 | check.문자 | 문자 | checkbox | 동의함 |
| check.이메일 | check.이메일 | 이메일 | checkbox | 원치않음 |
| 대출금입금계좌 | 대출금입금계좌 | 대출금입금(실행)계좌 | text | 103-352510-18953 |
| check.예금담보등상계후잔액반환계좌번호 | check.예금담보등상계후잔액반환계좌번호 | 예금담보등상계후잔액반환계좌번호(담보제공자기준) | checkbox | 별도 지정(은행명 |
| 원금및이자자동이체결제계좌 | 원금및이자자동이체결제계좌 | 원(리)금및이자자동이체결제계좌 | number | 260,000원 |
| seal.signer3 | seal.signer3 | 신청인:____________________________ | seal | 전영경 |
| sign.signer3 | sign.signer3 | 신청인:____________________________ | signature | 강순준 |
| 설정순위 | 설정순위 | •설정순위(설정일자) | text |  |
| signer4.name | signer4.name | •접수번호(등기부등본을구기준) | text | 반영인 |
| seal.signer4 | seal.signer4 | •접수번호(등기부등본을구기준) | seal | 반영인 |
| sign.signer4 | sign.signer4 | •접수번호(등기부등본을구기준) | signature | 이환빈 |
| 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | text |  |
| 채권최고액 | 채권최고액 | •채권최고액 | number | 46,080,000 |

### hana_official_049 · 《개인》대출신청서(가계용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 《개인》대출신청서(가계용). 기존 hf049 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/10/20/5160178_20251020.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 한도증액 |
| check.신청인구분 | check.신청인구분 | 신청인구분 | checkbox | 연대보증인 |
| check.대출신청인의 | check.대출신청인의 | 대출신청인()의 | checkbox | 동료 |
| 고객번호 | 고객번호 | 고객번호 | rrn | 956008-6651686 |
| check.우편물수령처 | check.우편물수령처 | 우편물수령처 | checkbox | 자택 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.address | customer.address | 자택주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| employer.address | employer.address | 직장주소 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태평양무역 구매팀 |
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| check.직업군 | check.직업군 | 직업군 | checkbox | 자영업자 |
| employer.name | employer.name | 직장명 | text | 주식회사 태평양무역 |
| 근무부서 | 근무부서 | 근무부서 | text |  |
| 입사년월 | 입사년월 | 입사년월 | text |  |
| check.자가 | check.자가 | 자가( | checkbox | 본인 |
| check.주거형태코드 | check.주거형태코드 | 주거형태코드 | checkbox | 오피스텔 |
| check.부채현황취급예정포함 | check.부채현황취급예정포함 | 부채현황(단위:백만원)【취급예정포함】 | checkbox | 금융기관명( |
| 종류 | 종류 | 종류 | text | 하나 적금 |
| 평가금액 | 평가금액 | 평가금액 | number | 26,310,000 |
| check.고용형태 | check.고용형태 | 고용형태 | checkbox | 전문 |
| employer.position | employer.position | 직위 | text | 대리 |
| check.직무구분 | check.직무구분 | 직무구분 | checkbox | 자영업자 |
| 면적 | 면적 | 면적 | text |  |
| company.address | corp.address | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| check.연소득 | check.연소득 | 연소득 | checkbox | 본인( |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| customer.home_phone | customer.home_phone | 자택전화번호 | phone | 02-9221-1609 |
| employer.phone | employer.phone | 직장전화번호 | phone | 043-783-2775 |
| check.국적 | check.국적 | 국적 | checkbox | 대한민국 |
| check.담보종류 | check.담보종류 | 담보종류 | checkbox | 다가구 |
| check.임대차확인 | check.임대차확인 | 임대차확인 | checkbox | 예정(임대보증금 |
| 소유자명 | 소유자명 | 소유자명 | text |  |
| check.결혼여부 | check.결혼여부 | 결혼여부 | checkbox | 기혼 |
| date | date | 대출희망일 | date | 2026년 1월 31일 |
| check.상환방법 | check.상환방법 | 상환방법 | checkbox | 원금균등분할 |
| check.주택 | check.주택 | 주택( | checkbox | 부채상환(구입자금) |
| check.기타부동산 | check.기타부동산 | 기타부동산( | checkbox | 결혼 |
| check.거래구분 | check.거래구분 | 거래구분 | checkbox | 건별 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 대출신청인(본인) | text | 박찬연 |
| seal.signer | seal.customer | 대출신청인(본인) | seal | 박찬연 |
| sign.signer | sign.customer | 대출신청인(본인) | signature | 강순준 |
| signer2.name | related.name | 담보제공자(또는연대보증인) | text | 박채희 |
| seal.signer2 | seal.related | 담보제공자(또는연대보증인) | seal | 박채희 |
| sign.signer2 | sign.related | 담보제공자(또는연대보증인) | signature | 민진율 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 확인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김미재 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 송유태 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 제갈철하 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 검인 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 허태예 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 김기희 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 선찬서 |
| check.신규증액채무인수한도감액한도완제처리시안내 | check.신규증액채무인수한도감액한도완제처리시안내 | 신규,증액,채무인수,한도감액,한도완제처리시안내 | checkbox | 원치않음 |
| check.신청대출승인완료시안내문자통지 | check.신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | checkbox | 동의함 |
| check.동의함 | check.동의함 | 동의함( | checkbox | 이메일 |
| check.중도상환해약금면제시점도래안내문자통지 | check.중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | checkbox | 원치않음 |
| check.우편 | check.우편 | 우편 | checkbox | 직장 |
| check.문자 | check.문자 | 문자 | checkbox | 동의함 |
| check.이메일 | check.이메일 | 이메일 | checkbox | 동의함 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| customer.name2 | customer.name2 | 예금주 | text | 박찬연 |
| check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까 | check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까 | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 원치않음 |
| check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2 | check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2 | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 직접 수령 |
| 이관희망점 | 이관희망점 | 이관희망점 | text |  |
| 설정순위 | 설정순위 | •설정순위(설정일자) | text |  |
| 접수번호 | 접수번호 | •접수번호(등기부등본을구기준) | text | 4062-7383 |
| signer3.name | signer3.name | 담보제공 | text | 박채희 |
| seal.signer3 | seal.signer3 | 담보제공 | seal | 박채희 |
| sign.signer3 | sign.signer3 | 담보제공 | signature | 김호우 |
| customer.name3 | customer.name3 | 성명 | text | 박찬연 |
| 신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | text |  |
| 대출부수거래충족여부안내통지 | 대출부수거래충족여부안내통지 | 대출부수거래충족여부안내통지(문자만) | text |  |
| 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | text |  |
| 거절사유에대해안내를받으시겠습니까 | 거절사유에대해안내를받으시겠습니까 | 거절사유에대해안내를받으시겠습니까? | text | 생활자금 |

### hana_official_051 · 대출계약 철회신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 대출계약 철회신청서. 기존 hf051 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/30/5-06-0681.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 차주 | text | 박찬연 |
| 상품명 | 상품명 | 상품명 | text | 하나 MMF |
| 실행일 | 실행일 | 실행일 | date | 2025-06-06 |
| account | account | 계좌번호 | account_no | 000-287736-52424 |
| 금액 | 금액 | 금액 | number | 207,910,000 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 강순준 |
| check.중도상환이나철회하지않고 | check.중도상환이나철회하지않고 | 중도상환이나철회하지않고대출유지함 | checkbox | 중도상환이나 철회하지 않고 대출 유지함 |
| check.기타 | check.기타 | 기타( | checkbox | 기타 ( |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신청인 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신청인 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 신청인 | signature | 강순준 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 검인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 금예아 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 엄환빈 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 장윤예 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이호서 |

### hana_official_052 · [필수] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택전월세자금대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. [필수] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택전월세자금대출용). 기존 hf052 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/23/5-06-0920.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 목록[].공공정보등 | 목록[].공공정보등 | ■공공정보등 | text |  |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| 부채금액 | 부채금액 | ¶부채금액 | number | 170,000 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까2 | check.위개인정보제공에동의하십니까2 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| 보유현황공공임대주택계약정보 | 보유현황공공임대주택계약정보 | 보유현황,공공임대주택계약정보 | text |  |
| 업권등의공시가액 | 업권등의공시가액 | 업권등의공시가액 | number | 90,540,000 |
| 제공받는자와동일 | 제공받는자와동일 | -제공받는자와동일 | text |  |
| check.위고유식별정보조회에동의하십니까 | check.위고유식별정보조회에동의하십니까 | 위고유식별정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| 정보전월세거래정보 | 정보전월세거래정보 | 정보,전·월세거래정보 | text |  |
| check.위개인정보조회에동의하십니까 | check.위개인정보조회에동의하십니까 | 위개인(신용)정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보조회에동의하십니까2 | check.위개인정보조회에동의하십니까2 | 위개인(신용)정보조회에동의하십니까? | checkbox | 동의함 |
| check.이용동의여부 | check.이용동의여부 | 이용동의여부 | checkbox | 보기2 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 이욱유 |
| signer2.name | family.name | 배우자성명 | text | 박영준 |
| seal.signer2 | seal.signer2 | 배우자성명 | seal | 박영준 |
| sign.signer2 | sign.signer2 | 배우자성명 | signature | 김순우 |

### hana_official_053 · [필수] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택구입자금대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. [필수] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택구입자금대출용). 기존 hf053 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/23/5-06-0919.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 재지및면적유형가격임대차현황등 | 재지및면적유형가격임대차현황등 | 재지및면적,유형,가격,임대차현황등 | text |  |
| 목록[].공공정보등 | 목록[].공공정보등 | ■공공정보등 | text |  |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| 부채금액 | 부채금액 | ¶부채금액 | number | 3,510,000 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인정보제공에동의하십니까2 | check.위개인정보제공에동의하십니까2 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| 보유현황공공주택계약정보 | 보유현황공공주택계약정보 | 보유현황,공공주택계약(입주)정보 | text |  |
| 권등의공시가액 | 권등의공시가액 | 권등의공시가액 | number | 1,650,000원 |
| 제공받는자와동일 | 제공받는자와동일 | -제공받는자와동일 | text |  |
| check.위고유식별정보조회에동의하십니까 | check.위고유식별정보조회에동의하십니까 | 위고유식별정보조회에동의하십니까? | checkbox | 동의함 |
| check.위개인정보조회에동의하십니까 | check.위개인정보조회에동의하십니까 | 위개인(신용)정보조회에동의하십니까? | checkbox | 동의함 |
| check.위개인정보조회에동의하십니까2 | check.위개인정보조회에동의하십니까2 | 위개인(신용)정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| check.이용동의여부 | check.이용동의여부 | 이용동의여부 | checkbox | 동의하지 않음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 최우빈 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| signer2.name | family.name | 배우자성명 | text | 박영준 |
| seal.signer2 | seal.signer2 | 배우자성명 | seal | 김순우 |
| sign.signer2 | sign.signer2 | 배우자성명 | signature | 박영준 |

### hana_official_054 · 주택도시기금 대출 신청서(가계용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 주택도시기금 대출 신청서(가계용). 기존 hf054 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/23/5-16-0177.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 주택가격 | 주택가격 | 주택가격 | text |  |
| 순담보가액 | 순담보가액 | 순담보가액 | number | 1,830,000원 |
| 선순위설정액 | 선순위설정액 | 선순위설정액 | text |  |
| 대출가능액 | 대출가능액 | 대출가능액 | text |  |
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 대환(재약정) |
| check.신청인구분 | check.신청인구분 | 신청인구분 | checkbox | 대출신청인(본인) |
| check.대출신청인의 | check.대출신청인의 | 대출신청인()의 | checkbox | 동료 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.address | customer.address | 주민등록지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.address2 | customer.address2 | 현거주지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 전세보증금 | 전세보증금 | 전세보증금 | number | 121.42 |
| 이사예정지 | 이사예정지 | 이사예정지 | text |  |
| 전세보증금2 | 전세보증금2 | 전세보증금 | number | 1.4 |
| employer.name | employer.name | 직장명 | text | 주식회사 태평양무역 |
| employer.address | employer.address | 직장주소 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태평양무역 구매팀 |
| 배우자명 | 배우자명 | 배우자명 | text |  |
| 다자녀가구다문화가구장애인가구 | 다자녀가구다문화가구장애인가구 | ▢다자녀가구▢다문화가구▢장애인가구 | text |  |
| 원리금자동이체계좌번호 | 원리금자동이체계좌번호 | 원리금자동이체계좌번호 | text | 845-029474-53384 |
| 대출신청금액 | 대출신청금액 | 대출신청금액 | number | 99,470,000원 |
| 대출과목 | 대출과목 | 대출과목 | text | 운전자금대출 |
| 대출기간 | 대출기간 | 대출기간 | text |  |
| 대출이율 | 대출이율 | 대출이율 | number | 4.71 |
| 목록[].임차보증금 | 목록[].임차보증금 | 임차보증금 | number | 9,110,000 |
| 본인 | 본인 | 본인 | number | 176.91 |
| 자기자금 | 자기자금 | 자기자금 | number | 16.81 |
| 방수 | 방수 | 방수 | number | 4 |
| 목록[].소액보증금 | 목록[].소액보증금 | 소액보증금 | number | 69,010,000 |
| customer.birth | customer.birth | 생년월일 | date | 1990-02-10 |
| employer.department | employer.department | 부서명 | text | 구매팀 |
| 월세보증금 | 월세보증금 | 월세보증금 | number | 6.95 |
| 월세보증금2 | 월세보증금2 | 월세보증금 | number | 93.46 |
| 만기일시원리금균등분할원금균등분할 | 만기일시원리금균등분할원금균등분할 | ▢만기일시▢원리금균등분할▢원금균등분할 | date | 2029-05-18 |
| 소액보증금 | 소액보증금 | 소액보증금 | number | 19,910,000원 |
| 배우자 | 배우자 | 배우자 | number | 0.84 |
| 본건대출 | 본건대출 | 본건대출(기금) | number | 1.69 |
| 배우자직장번호 | 배우자직장번호 | 배우자직장번호(핸드폰번호) | text | 4041-9754 |
| 대출희망일 | 대출희망일 | 대출희망일 | date | 2025.04.11 |
| 목록[].금액 | 목록[].금액 | 금액 | number | 80,710,000원 |
| customer.phone | customer.phone | 휴대폰번호 | phone | 010-5907-7253 |
| customer.email | customer.email | e-mail | text | chanyeon363@naver.com |
| customer.phone2 | customer.phone2 | 전화번호 | phone | 010-5907-7253 |
| employer.position | employer.position | 직위 | text | 대리 |
| 목록[].자금용도 | 목록[].자금용도 | 자금용도 | text | 결혼자금 |
| 고객번호 | 고객번호 | 고객번호 | text | 0503-6661 |
| check.우편물수령처 | check.우편물수령처 | 우편물수령처 | checkbox | 자택 |
| 월임대료 | 월임대료 | 월임대료 | number | 2,607 |
| 주거방수 | 주거방수 | 주거방수 | number | 4 |
| 월임대료2 | 월임대료2 | 월임대료 | number | 2,789 |
| employer.phone | employer.phone | 직장전화번호 | phone | 043-783-2775 |
| 가구총소득 | 가구총소득 | 가구총소득 | number | 7.76 |
| 기타조달 | 기타조달 | 기타조달 | number | 0.48 |
| 결혼일 | 결혼일 | 결혼(예정)일 | date | 2025년 2월 2일 |
| employer.hire_date | employer.hire_date | 입사일자 | date | 2020.05.08 |
| 목록[].담보종류 | 목록[].담보종류 | 담보종류 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| 분양가격 | 분양가격 | ▢분양가격 | text |  |
| customer.name2 | customer.name2 | 신청인(본인) | text | 박찬연 |
| customer.name3 | customer.name3 | 차주 | text | 박찬연 |
| 의담보제공자 | 의담보제공자 | 의담보제공자(또는연대보증인) | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 박태유 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김규하 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 마성혜 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 백정윤 |
| 신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | text |  |
| check.신규증액채무인수한도감액한도완제처리시안내 | check.신규증액채무인수한도감액한도완제처리시안내 | 신규,증액,채무인수,한도감액,한도완제처리시안내 | checkbox | 이메일 |
| check.신청대출승인완료시안내문자통지 | check.신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | checkbox | 동의함 |
| check.동의함 | check.동의함 | 동의함( | checkbox | 문자 |
| check.중도상환해약금면제시점도래안내문자통지 | check.중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | checkbox | 원치않음 |
| check.우편 | check.우편 | 우편 | checkbox | 원치않음 |
| check.문자 | check.문자 | 문자 | checkbox | 원치않음 |
| check.이메일 | check.이메일 | 이메일 | checkbox | 동의함 |
| 대출금입금계좌 | 대출금입금계좌 | 대출금입금(실행)계좌 | text | 112-110846-04076 |
| check.예금담보등상계후잔액반환계좌번호 | check.예금담보등상계후잔액반환계좌번호 | 예금담보등상계후잔액반환계좌번호(담보제공자기준) | checkbox | 대출금 입금 계좌 |
| check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까 | check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까 | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 원치않음 |
| check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2 | check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2 | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 팩스 |
| 설정순위 | 설정순위 | •설정순위(설정일자) | text |  |
| 접수번호 | 접수번호 | •접수번호(등기부등본을구기준) | text | 051303-0772719 |
| signer.name | signer.name | (담보제공자기준) | text | 박찬연 |
| seal.signer | seal.customer | (담보제공자기준) | seal | 현예지 |
| sign.signer | sign.customer | (담보제공자기준) | signature | 강순준 |
| 대출부수거래충족여부안내통지 | 대출부수거래충족여부안내통지 | 대출부수거래충족여부안내통지(문자만) | text |  |
| 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | text |  |
| 대출신청이거절되는경우 | 대출신청이거절되는경우 | 대출신청이거절되는경우, | text |  |
| 거절사유에대해안내를받으시겠습니까 | 거절사유에대해안내를받으시겠습니까 | 거절사유에대해안내를받으시겠습니까? | text | 생활자금 |
| 채권최고액 | 채권최고액 | •채권최고액 | text |  |

### hana_official_055 · 주택도시기금 대출상담 및 신청서(내집마련 디딤돌 대출용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 주택도시기금 대출상담 및 신청서(내집마련 디딤돌 대출용). 기존 hf055 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/23/5-16-0139.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.address | customer.address | 주민등록지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.address2 | customer.address2 | 현거주지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 전세보증금 | 전세보증금 | 전세보증금 | number | 2.11 |
| customer.address3 | customer.address3 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 임대방수 | 임대방수 | 임대방수 | number | 3 |
| employer.name | employer.name | 직장명 | text | 주식회사 태평양무역 |
| employer.address | employer.address | 직장주소 | text | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태평양무역 구매팀 |
| spouse.name | family.name | 배우자성명 | text | 이도민 |
| 원리금자동이체계좌번호 | 원리금자동이체계좌번호 | 원리금자동이체계좌번호 | text | 536-048795-58753 |
| 대출신청금액 | 대출신청금액 | 대출신청금액 | number | 6,710,000 |
| 대출과목 | 대출과목 | 대출과목 | text | 시설자금대출 |
| 본인 | 본인 | 본인 | number | 8.48 |
| 본인2 | 본인2 | 본인 | number | 2.13 |
| 자기자금 | 자기자금 | 자기자금 | number | 24.52 |
| 방수 | 방수 | 방수 | number | 4 |
| 월세보증금 | 월세보증금 | 월세보증금 | number | 0.55 |
| 방수2 | 방수2 | 방수 | number | 2 |
| 임대보증금 | 임대보증금 | 임대보증금 | number | 28.74 |
| employer.department | employer.department | 부서명 | text | 구매팀 |
| 목록[].차입기관명 | 목록[].차입기관명 | 차입기관명 | text | 신한은행 |
| 배우자 | 배우자 | 배우자 | number | 2.94 |
| 배우자2 | 배우자2 | 배우자 | number | 33.58 |
| 본건대출 | 본건대출 | 본건대출 | number | 22.51 |
| 목록[].금액 | 목록[].금액 | 금액 | number | 580,000 |
| customer.rrn | customer.rrn | 주민등록번호앞6자리 | number | 900210 |
| customer.phone | customer.phone | 휴대폰번호 | phone | 010-5907-7253 |
| customer.phone2 | customer.phone2 | 전화번호 | phone | 010-5907-7253 |
| 월임대료 | 월임대료 | 월임대료 | number | 1,951 |
| 선순위설정금액 | 선순위설정금액 | 선순위설정금액 | number | 17.06 |
| employer.position | employer.position | 직위 | text | 대리 |
| spouse.rrn | spouse.rrn | 배우자주민등록번호앞6자리 | number | 670921 |
| 대출희망일 | 대출희망일 | 대출희망일 | date | 2025.03.27 |
| 상담자 | 상담자 | 상담자(직위/성명) | text |  |
| 목록[].자금용도 | 목록[].자금용도 | 자금용도 | text | 의료비 |
| employer.phone | employer.phone | 직장전화번호 | phone | 043-783-2775 |
| 가구총소득 | 가구총소득 | 가구총소득 | number | 4.95 |
| 제외부채 | 제외부채 | 제외부채 | number | 24.43 |
| 기타조달 | 기타조달 | 기타조달 | number | 0.35 |
| 목록[].담보종류 | 목록[].담보종류 | 담보종류 | text |  |
| employer.hire_date | employer.hire_date | 입사일자 | date | 2020.05.08 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 이수도 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 옥성희 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 박윤호 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 검인 |
| 신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | text |  |
| check.신규증액채무인수한도감액한도완제처리시안내 | check.신규증액채무인수한도감액한도완제처리시안내 | 신규,증액,채무인수,한도감액,한도완제처리시안내 | checkbox | 이메일 |
| check.신청대출승인완료시안내문자통지 | check.신청대출승인완료시안내문자통지 | 신청대출승인완료시안내문자통지 | checkbox | 동의함 |
| check.동의함 | check.동의함 | 동의함( | checkbox | 원치않음 |
| check.중도상환해약금면제시점도래안내문자통지 | check.중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | checkbox | 원치않음 |
| check.우편 | check.우편 | 우편 | checkbox | 원치않음 |
| check.문자 | check.문자 | 문자 | checkbox | 동의함 |
| check.이메일 | check.이메일 | 이메일 | checkbox | 동의함 |
| 대출부수거래충족여부안내통지 | 대출부수거래충족여부안내통지 | 대출부수거래충족여부안내통지(문자만) | text |  |
| 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | 중도상환해약금면제시점도래안내문자통지 | text |  |

### hana_official_058 · 융자상담 및 차입신청서(기업용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 융자상담 및 차입신청서(기업용). 기존 hf058 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/10/10/3-06-0201_1.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.신청구분 | check.신청구분 | 신청구분 | checkbox | 채무인수 |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 강순준 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| company.address | corp.address | 사업장주소 | text | 서울특별시 중구 다산로 361, 6층 |
| company.biz_no | corp.biz_no | 사업자번호(생년월일) | biz_no | 264-82-36559 |
| 사업장전화번호 | 사업장전화번호 | 사업장전화번호 | phone | 010-5907-7253 |
| 대출과목 | 대출과목 | 대출과목 | text | 주택담보대출 |
| 신청금액 | 신청금액 | 신청금액 | number | 4,670,000원 |
| check.대출기간만료일 | check.대출기간만료일 | 대출기간만료일 | checkbox | 대출실행(한도약정)일로부터 |
| 거치기간 | 거치기간 | 거치기간 | number | 2 |
| check.상환방법 | check.상환방법 | 상환방법 | checkbox | 원금균등분할 |
| check.자금용도 | check.자금용도 | 자금용도 | checkbox | 시설자금(사업장구입, 설비구입 등) |
| check.거래구분 | check.거래구분 | 거래구분 | checkbox | 한도 |
| check.금리적용방식 | check.금리적용방식 | 금리적용방식 | checkbox | 고정 |
| 부채현황_목록[].금융기관명 | 부채현황_목록[].금융기관명 | 금융기관명 | text | 농협은행 |
| company.address2 | company.address2 | 소재지 | text | 서울특별시 중구 다산로 361, 6층 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| 종류 | 종류 | 종류 | text | 하나 정기예금 |
| employer.name | employer.name | 직장명(직위) | text | 주식회사 태평양무역 |
| 부채현황_목록[].금액 | 부채현황_목록[].금액 | 금액 | text | 45,130,000 |
| 수량 | 수량 | 수량 | number | 3 |
| 차주와의관계 | 차주와의관계 | 차주와의관계 | text |  |
| 부채현황_목록[].담보 | 부채현황_목록[].담보 | 담보 | text |  |
| 추정가액 | 추정가액 | 추정가액 | number | 105,540,000 |
| 실재산 | 실재산 | 실재산 | text |  |
| 담보제공자 | 담보제공자 | 담보제공자 | text |  |
| 나이 | 나이 | 나이 | text |  |
| 부채현황_목록[].자금용도 | 부채현황_목록[].자금용도 | 자금용도 | text | 계좌 정리 |
| 신청인과의관계 | 신청인과의관계 | 신청인과의관계 | text |  |
| 보증종류 | 보증종류 | 보증종류 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 김형호 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 손태연 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 염수주 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 연승혜 |
| seal.staff.관리자 | seal.staff.관리자 | 관리자 | seal | 이진예 |
| sign.staff.관리자 | sign.staff.관리자 | 관리자 | signature | 전채찬 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 허서주 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 확인 |
| check.신규처리시안내 | check.신규처리시안내 | 신규처리시안내 | checkbox | 원치않음 |
| customer.phone | customer.phone | 휴대폰번호 | phone | 010-5907-7253 |
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| check.동의함 | check.동의함 | 동의함( | checkbox | 원치않음 |
| customer.phone2 | customer.phone2 | 휴대폰번호 | phone | 010-5907-7253 |
| customer.email2 | customer.email2 | E-mail | text | chanyeon363@naver.com |
| check.확인서 | check.확인서 | 확인서(담보제공자용) | checkbox | 미해당 |
| check.확인서2 | check.확인서2 | 확인서(담보제공자용) | checkbox | 미해당 |
| 대출금입금계좌 | 대출금입금계좌 | 대출금입금(실행)계좌 | text | 416-192946-55723 |
| 원금및이자자동이체결제계좌 | 원금및이자자동이체결제계좌 | 원(리)금및이자자동이체결제계좌 | number | 830,000 |
| 설정순위 | 설정순위 | ●설정순위(설정일자) | text |  |
| 부동산담보대출접수번호 | 부동산담보대출접수번호 | 부동산담보대출●접수번호(등기부등본기준) | text | 581299-5538092 |

### hana_official_059 · 개인(신용)정보 조회 동의서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 개인(신용)정보 조회 동의서. 기존 hf059 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/06/27/5-06-0548.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 거래와관련한개인정보조회 | 거래와관련한개인정보조회 | (금융)거래와관련한개인(신용)정보조회 | text |  |
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 국내거소신고번호성명주소전화번호 | 국내거소신고번호성명주소전화번호 | 국내거소신고번호,성명,주소,전화번호 | phone | 010-5907-7253 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 이용목적 | 이용목적 | 이용목적 | text | 해외 이주 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 확인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 김소율 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 박하유 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 곽순서 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 서은지 |
| 일반개인정보2 | 일반개인정보2 | ■일반개인정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| 국내거소신고번호성명 | 국내거소신고번호성명 | 국내거소신고번호,성명 | text | 000593-2100559 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| 제공받는자와동일 | 제공받는자와동일 | 제공받는자와동일 | date | 2025년 9월 23일 |
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보조회에동의하십니까 | check.위고유식별정보조회에동의하십니까 | 위고유식별정보조회에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보조회에동의하십니까 | check.위개인정보조회에동의하십니까 | 위개인(신용)정보조회에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 현예지 |
| sign.signer | sign.customer | 본인성명 | signature | 전영경 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 강석호 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 김승성 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 강석호 |
| 이용목적2 | 이용목적2 | 이용목적 | text | 결혼자금 |
| 재산채무소득의총액납세실적등 | 재산채무소득의총액납세실적등 | 재산·채무·소득의총액,납세실적등 | number | 10,250,000원 |

### hana_official_060 · [필수] 개인(신용)정보 수집이용 동의서(대출성상품 적합성적정성 판단용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. [필수] 개인(신용)정보 수집이용 동의서(대출성상품 적합성적정성 판단용). 기존 hf060 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/06/14/3-06-0151.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 박영준 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 엄소원 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 방예린 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 진승진 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 손동지 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 왕영희 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 도석서 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이민태 |

### hana_official_061 · 적합성, 적정성 고객정보 확인서(개인 및 개인사업자용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 적합성, 적정성 고객정보 확인서(개인 및 개인사업자용). 기존 hf061 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/06/14/5-06-0967.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.email | customer.email | Email | text | chanyeon363@naver.com |
| check.후견인여부 | check.후견인여부 | 후견인여부 | checkbox | 피한정후견인 |
| check.대출용도 | check.대출용도 | 대출용도 | checkbox | 교육비 |
| check.총자산규모 | check.총자산규모 | 총자산규모(순자산) | checkbox | 억원 이상 |
| check.담보제공계획 | check.담보제공계획 | 담보제공계획 | checkbox | 없음 |
| check.담보제공계획2 | check.담보제공계획2 | 담보제공계획 | checkbox | 있음 |
| check.소득없음 | check.소득없음 | 소득없음 | checkbox | 억원 이상 |
| check.부채 | check.부채 | 부채 | checkbox | 부채없음 (잘 모름 포함) |
| check.연체여부 | check.연체여부 | 연체여부 | checkbox | 연체정보 없음 |
| check.신용점수 | check.신용점수 | 신용점수 | checkbox | KCB |
| check.근로소득 | check.근로소득 | 근로소득 | checkbox | 임대소득 |
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| 기거래건전성 | 기거래건전성 | 기거래건전성 | text |  |
| 신용상태 | 신용상태 | 신용상태 | text |  |
| 상환능력및변제계획 | 상환능력및변제계획 | 상환능력및변제계획 | text |  |
| 진단결과번호 | 진단결과번호 | 진단결과번호 | text | 579041-2388625 |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 위나아 |
| sign.signer | sign.customer | 신청인 | signature | 박찬연 |
| signer2.name | signer2.name | 신청인 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신청인 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 신청인 | signature | 강순준 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 진미준 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 정숙빈 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 구성승 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김주현 |

### hana_official_062 · 적합성, 적정성 고객정보 확인서(법인용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 적합성, 적정성 고객정보 확인서(법인용). 기존 hf062 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/06/14/5-06-0970.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 업체명 | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자명 | text | 박찬연 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 대표자연락처 | 대표자연락처 | 대표자연락처 | phone | 010-5907-7253 |
| company.biz_no | corp.biz_no | 사업자등록번호 | biz_no | 264-82-36559 |
| 상시근로자수 | 상시근로자수 | 상시근로자수 | text |  |
| customer.email | customer.email | E-mail | text | chanyeon363@naver.com |
| check.전문금융소비자여부 | check.전문금융소비자여부 | 전문금융소비자여부 | checkbox | 주권을 국내외 증권시장에 상장한 법인 |
| check.전문금융소비자여부2 | check.전문금융소비자여부2 | 전문금융소비자여부 | checkbox | 일반금융소비자 |
| 업력 | 업력 | 업력 | number | 12 |
| check.총자산규모 | check.총자산규모 | 총자산규모(순자산) | checkbox | 억원 이상 10억원 미만 |
| check.주택증권지식재산권등의담보제공예정 | check.주택증권지식재산권등의담보제공예정 | 주택,증권(주식,채권등),지식재산권등의담보제공예정 | checkbox | 있음 |
| check.담보제공계획 | check.담보제공계획 | 담보제공계획 | checkbox | 없음 |
| check.매출액 | check.매출액 | 매출액 | checkbox | 억원~ 10억원 미만 |
| check.순이익 | check.순이익 | 순이익 | checkbox | 억원 미만 |
| check.부채 | check.부채 | 부채 | checkbox | 억원 미만 |
| check.연체여부 | check.연체여부 | 연체여부 | checkbox | 연체정보 있음 |
| check.변제방법 | check.변제방법 | 변제방법 | checkbox | 담보의 처분(매매, 경매 등) |
| check.대출용도 | check.대출용도 | 대출용도 | checkbox | 운전자금 |
| check.최근3년간연속자본잠식 | check.최근3년간연속자본잠식 | 최근3년간연속자본잠식 | checkbox | 해당 |
| 기거래건전성 | 기거래건전성 | 기거래건전성 | text |  |
| 신용상태 | 신용상태 | 신용상태 | text |  |
| 상환능력및변제계획 | 상환능력및변제계획 | 상환능력및변제계획 | text |  |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 강순준 |
| signer2.name | signer2.name | 신청인 | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신청인 | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 신청인 | signature | 강순준 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 최훈정 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 조희혜 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 박유아 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 허현예 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김태현 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| agent.relation | agent.relation | 관계 | text | 부 |

### hana_official_064 · 대출정보 열람청구, 상환 및 말소접수 위임장(주택담보대출 대출이동서비스)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 대출정보 열람청구, 상환 및 말소접수 위임장(주택담보대출 대출이동서비스). 기존 hf064 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/12/08/5-16-0401.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 위임인(본인) | text | 박찬연 |
| seal.signer | seal.customer | 위임인(본인) | seal | 박찬연 |
| sign.signer | sign.customer | 위임인(본인) | signature | 강순준 |

### hana_official_065 · 국토교통부 주택소유확인 시스템 등 이용 관련 [필수] 개인(신용)정보 수집·이용·제공 동의서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 국토교통부 주택소유확인 시스템 등 이용 관련 [필수] 개인(신용)정보 수집·이용·제공 동의서. 기존 hf065 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/06/13/5-06-0893.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 검인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 한우주 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 정순찬 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 임승영 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 권다예 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 기순희 |
| 일반개인정보2 | 일반개인정보2 | ■일반개인정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의함 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 이민빈 |
| signer2.name | family.name | 세대원성명 | text | 박영준 |
| seal.signer2 | seal.signer2 | 세대원성명 | seal | 박영준 |
| sign.signer2 | sign.signer2 | 세대원성명 | signature | 강석호 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer3.name | signer3.name | 세대원성명 | text | 박영준 |
| seal.signer3 | seal.signer3 | 세대원성명 | seal | 강석호 |
| sign.signer3 | sign.signer3 | 세대원성명 | signature | 박영준 |
| signer4.name | signer4.name | 세대원성명 | text | 박영준 |
| seal.signer4 | seal.signer4 | 세대원성명 | seal | 김순우 |
| sign.signer4 | sign.signer4 | 세대원성명 | signature | 박영준 |
| signer5.name | signer5.name | 세대원성명 | text | 박영준 |
| seal.signer5 | seal.signer5 | 세대원성명 | seal | 김서호 |
| sign.signer5 | sign.signer5 | 세대원성명 | signature | 박영준 |
| signer6.name | signer6.name | 세대원성명 | text | 박영준 |
| seal.signer6 | seal.signer6 | 세대원성명 | seal | 장민인 |
| sign.signer6 | sign.signer6 | 세대원성명 | signature | 이도민 |

### hana_official_066 · 대출정보 열람청구 및 상환 위임장(대출이동서비스)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 대출정보 열람청구 및 상환 위임장(대출이동서비스). 기존 hf066 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/05/31/5-16-0365_230531.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 위임자(본인) | text | 박찬연 |
| seal.signer | seal.customer | 위임자(본인) | seal | 현예지 |
| sign.signer | sign.customer | 위임자(본인) | signature | 박찬연 |

### hana_official_067 · [필수] 개인(신용)정보 수집 · 이용 동의서[대출이동서비스]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. [필수] 개인(신용)정보 수집 · 이용 동의서[대출이동서비스]. 기존 hf067 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/05/31/5-16-0364_230531.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1659382 |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| ᄋ금융사고조사분쟁해결민원처리 | ᄋ금융사고조사분쟁해결민원처리 | ᄋ금융사고조사,분쟁해결,민원처리 | text |  |
| ᄋ법령상의무이행 | ᄋ법령상의무이행 | ᄋ법령상의무이행 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 이수경 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 구영정 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 왕도지 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이선유 |

### hana_official_118 · [필수] 개인(신용)정보 수집·이용·제공_동의서[가계여신_금융거래]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. [필수] 개인(신용)정보 수집·이용·제공_동의서[가계여신_금융거래]. 기존 hf118 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/03/02/5-16-0179_20210302.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | -금융사고조사,분쟁해결,민원처리 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 이찬태 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 정연정 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 남민인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 검인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 길상민 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 이훈주 |
| 공공정보등2 | 공공정보등2 | ■공공정보등 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 김순우 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 박영준 |
| 성명국내거소신고번호 | 성명국내거소신고번호 | 성명,국내거소신고번호 | text | 321152-4854050 |
| 있는정보 | 있는정보 | 있는정보 | text |  |

### hana_official_128 · 필수 개인(신용)정보 수집, 이용 및 제공 동의서(소호여신)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 필수 개인(신용)정보 수집, 이용 및 제공 동의서(소호여신). 기존 hf128 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/02/25/5_06_0724.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | -금융사고조사,분쟁해결,민원처리 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 검인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 검인 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 표예서 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 김예은 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 추준린 |
| 공공정보등2 | 공공정보등2 | ■공공정보등 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 강순준 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 강석호 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 김순우 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 강석호 |
| 이용목적 | 이용목적 | 이용목적 | text | 해외 이주 |

### hana_official_129 · 필수 개인(신용)정보 수집, 이용 및 제공 동의서(법인여신)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 필수 개인(신용)정보 수집, 이용 및 제공 동의서(법인여신). 기존 hf129 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/02/25/5-06-0734.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 공공정보등 | 공공정보등 | ■공공정보등 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | -금융사고조사,분쟁해결,민원처리 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 위현재 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 염선성 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 기기혜 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 검인 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김형은 |
| 공공정보등2 | 공공정보등2 | ■공공정보등 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 본인성명 | signature | 이욱유 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 이도민 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 김서호 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 이도민 |

### hana_official_138 · 대출금 수령위임동의서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 대출금 수령위임동의서. 기존 hf138 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5-06-0741_20150901.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 용도 | 용도 | 용도 | text | 사업자금으로 일억원 필요 |
| 수령금액 | 수령금액 | 수령금액 | number | 7,230,000 |
| customer.name | customer.name | 예금주 | text | 박찬연 |
| check.차주와의관계 | check.차주와의관계 | 차주와의관계 | checkbox | 전세자금대출의 경우 임대인 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 수령위임인 | text | 박찬연 |
| seal.signer | seal.customer | 수령위임인 | seal | 최우빈 |
| sign.signer | sign.customer | 수령위임인 | signature | 박찬연 |
| signer2.name | agent.name | 수령위임인의대리인 | text | 강석호 |
| seal.signer2 | seal.agent | 수령위임인의대리인 | seal | 엄소원 |
| sign.signer2 | sign.agent | 수령위임인의대리인 | signature | 강석호 |

### hana_official_139 · 《기업》 지급보증거래 신청서(서면.전자 지급보증 겸용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 《기업》 지급보증거래 신청서(서면.전자 지급보증 겸용). 기존 hf139 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5060703_20160707.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 보증금액 | 보증금액 | 보증금액 | number | 10,880,000원 |
| 피보증채무의종류 | 피보증채무의종류 | 피보증채무의종류 | text |  |
| 피보증채무의종류2 | 피보증채무의종류2 | 피보증채무의종류 | text |  |
| seal.signer | seal.signer | 인감(서명)대조 | seal | 현예지 |
| sign.signer | sign.signer | 인감(서명)대조 | signature | 강순준 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | customer.name | 본인 | text | 박찬연 |
| seal.signer2 | seal.customer | 본인 | seal | 위나아 |
| sign.signer2 | sign.customer | 본인 | signature | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| 상호 | 상호 | •상호(성명) | text | 주식회사 가온정밀 |
| 사업자번호 | 사업자번호 | •사업자번호 | biz_no | 473-35-87740 |
| 주소 | 주소 | •주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 전화번호및팩스번호 | 전화번호및팩스번호 | •전화번호및팩스번호(또는E-Mail) | phone | 043-783-2775 |
| 계좌번호 | 계좌번호 | •계좌번호 | text | 040-539358-98291 |
| 특정채무 | 특정채무 | 특정채무 | text |  |
| 보증 | 보증 | 보증 | text |  |
| 근보증 | 근보증 | 근보증 | text |  |
| 예금주 | 예금주 | •예금주 | text |  |

### hana_official_149 · 《기업》금융거래확인서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 《기업》금융거래확인서. 기존 hf149 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5060189_20160707.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].종별 | 목록[].종별 | 종별 | text | 하나 단기채 펀드 |
| 목록[].용도 | 목록[].용도 | 용도 | text | 자녀 교육비 |
| 목록[].이율 | 목록[].이율 | 이율 | text | 15 |
| 목록[].일자 | 목록[].일자 | 일자 | text | 2025년 11월 9일 |
| 목록[].금액 | 목록[].금액 | 금액 | text | 96,990,000 |
| 목록[].잔액 | 목록[].잔액 | 잔액 | text | 9,890,000 |
| 목록[].대출기한 | 목록[].대출기한 | 대출기한 | text | 2028-10-25 |
| 목록[].비고 | 목록[].비고 | 비고 | text | 해당 없음 |
| 종류 | 종류 | 종류 | text | 하나 단기채 펀드 |
| 선정일자 | 선정일자 | 선정일자 | date | 2025-03-24 |
| 유효기간 | 유효기간 | 유효기간 | text |  |
| 어음 | 어음 | 어음 | text |  |
| 수표 | 수표 | 수표 | text |  |
| 목록[].소재지 | 목록[].소재지 | 소재지 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 목록[].소유자 | 목록[].소유자 | 소유자 | text |  |
| 목록[].채무자와의관계 | 목록[].채무자와의관계 | 채무자와의관계 | text |  |
| 목록[].종류 | 목록[].종류 | 종류 | text | 하나 TDF 2040 |
| 목록[].수량 | 목록[].수량 | 수량 | text | 1 |
| 목록[].감정가격 | 목록[].감정가격 | 감정가격 | text |  |
| 목록[].감정일자 | 목록[].감정일자 | 감정일자 | text | 2025년 1월 16일 |
| 목록[].설정내용 | 목록[].설정내용 | 설정내용(순위,금액) | text | 해당 없음 |
| 대출종별 | 대출종별 | 대출종별 | text |  |
| 연체발생일 | 연체발생일 | 연체발생일 | date | 2025.10.03 |
| 연체발생일2 | 연체발생일2 | 연체발생일 | date | 2025-03-23 |
| 원금 | 원금 | 원금 | number | 940,000 |
| 이자 | 이자 | 이자 | number | 6,960,000 |
| 연체정리일 | 연체정리일 | 연체정리일 | date | 2025.08.12 |
| 연체일수 | 연체일수 | 연체일수 | text |  |
| seal.signer | seal.signer | (부)점장 | seal | 김지우 |
| sign.signer | sign.signer | (부)점장 | signature | 이규율 |
| signer2.name | corp.ceo | 대표자명 | text | 박찬연 |
| seal.signer2 | seal.corp | 대표자명 | seal | 강순준 |
| sign.signer2 | sign.customer | 대표자명 | signature | 박찬연 |
| company.name | corp.name | 기업체명 | text | (주)유니온무역 |

### hana_official_157 · 여신거래용 인감명판 등 신고서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 여신거래용 인감명판 등 신고서. 기존 hf157 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5090002_20160707.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| company.name | corp.name | 상호 | text | (주)유니온무역 |
| company.ceo | corp.ceo | 대표자 | text | 박찬연 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 명판 | 명판 | 명판 | text |  |
| seal.signer | seal.customer | 거래용인감또는서명(서명을병용한경우및외국인에한함) | seal | 박찬연 |
| sign.signer | sign.customer | 거래용인감또는서명(서명을병용한경우및외국인에한함) | signature | 강순준 |
| 목록[].변경후 | 목록[].변경후 | 변경후 | text | 해당 없음 |
| signer2.name | signer2.name | 대표자(본인자필) | text | 박찬연 |
| seal.signer2 | seal.corp | 대표자(본인자필) | seal | 박찬연 |
| sign.signer2 | sign.signer2 | 대표자(본인자필) | signature | 강순준 |
| 신고사항 | 신고사항 | 신고사항 | text |  |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 류현도 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 확인 |
| seal.staff.대리 | seal.staff.대리 | 대리 | seal | 검인 |
| sign.staff.대리 | sign.staff.대리 | 대리 | signature | 이하인 |
| seal.staff.차장 | seal.staff.차장 | 차장 | seal | 확인 |
| sign.staff.차장 | sign.staff.차장 | 차장 | signature | 이원유 |
| seal.staff.부점장 | seal.staff.부점장 | 부점장 | seal | 김원윤 |
| sign.staff.부점장 | sign.staff.부점장 | 부점장 | signature | 박서유 |

### hana_official_199 · 외화송금신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 외화송금신청서. 기존 hf199 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/06/02/3-09-0131_260602.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 담당 | 담당 | 담당(실명확인) | text |  |
| check.송금방법 | check.송금방법 | 송금방법 | checkbox | 국외전신송금(OTT) |
| check.송금정보등록 | check.송금정보등록 | 송금정보등록 | checkbox | 신규 |
| 영문 | 영문 | 영문(English) | text |  |
| 국문 | 국문 | 국문(Korean) | text |  |
| customer.rrn | customer.rrn | 주민(사업자)번호(I.DNo./PassportNo.) | rrn | 900210-1****** |
| 과거송금번호 | 과거송금번호 | 과거송금번호(EXISTINGREF.NO) | text | 752-195055-46715 |
| check.결제은행수수료부담 | check.결제은행수수료부담 | 결제은행수수료부담(REIMBURSINGBANKCHG.) | checkbox | 송금인 (DEBT) |
| check.받으실분 | check.받으실분 | 받으실분(Beneficiary) | checkbox | HAPPY E-MAIL 서비스 신청 (무료) |
| 송금목적 | 송금목적 | 송금목적(송금사유)(PURPOSEOFPAYMENT) | text | 계좌 정리 |
| 적요 | 적요 | 적요(DETAILSOFPAYMENT) | text |  |
| 은행코드 | 은행코드 | 은행코드(SWIFTBIC) | number | 453537 |
| 은행명 | 은행명 | 은행명(BANKNAME) | text | 신한은행 |
| 은행명2 | 은행명2 | 은행명(BANKNAME) | text | 우리은행 |
| 통화금액 | 통화금액 | 통화(CURRENCY):금액(AMOUNT) | number | 95,000,000 |
| 은행코드2 | 은행코드2 | 은행코드(BANKCODE) | number | 1318 |
| 수취인계좌번호 | 수취인계좌번호 | 수취인계좌번호(BNF'sA/CNo.) | text | 611-882699-77738 |
| foreign.name | foreign.name | 성명(Name) | text | Mekong Garment JSC |
| 신청인과의관계 | 신청인과의관계 | 신청인과의관계(RELATIONTOAPPLICANT) | text |  |
| check.송금정보등록건송금결과통지 | check.송금정보등록건송금결과통지 | 송금정보등록건송금결과통지 | checkbox | SMS |
| check.통화금액 | check.통화금액 | 통화(CURRENCY):금액(AMOUNT) | checkbox | 수수료 별도납부 |
| 보내는분계좌번호 | 보내는분계좌번호 | 보내는분계좌번호(A/CNO) | text | 225-358024-23960 |
| check.수수료차감후송금 | check.수수료차감후송금 | 수수료차감후송금 | checkbox | 수수료차감후 송금 |
| 신청인과의관계2 | 신청인과의관계2 | 신청인과의관계(RELATIONTOAPPLICANT) | text |  |
| check.귀행을 | check.귀행을 | ●귀행을 | checkbox | 외국인 또는 비거주자의 국내보수 등을 위한 거래 외국환 은행으로 지정하고 |
| signer.name | customer.name | 예금주명(A/CHOLDERNAME) | text | 박찬연 |
| seal.signer | seal.customer | 예금주명(A/CHOLDERNAME) | seal | 박찬연 |
| sign.signer | sign.customer | 예금주명(A/CHOLDERNAME) | signature | 강순준 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | signer2.name | 신청인(Applicant) | text | 박찬연 |
| seal.signer2 | seal.signer2 | 신청인(Applicant) | seal | 강순준 |
| sign.signer2 | sign.signer2 | 신청인(Applicant) | signature | 박찬연 |
| signer3.name | agent.name | 대리인(Agent) | text | 위우호 |
| seal.signer3 | seal.agent | 대리인(Agent) | seal | 김수연 |
| sign.signer3 | sign.agent | 대리인(Agent) | signature | 위우호 |
| date2 | date2 | 작성일 | date | 2026년 1월 31일 |
| seal.signer4 | seal.signer4 | 지점장 | seal | 정건진 |
| sign.signer4 | sign.signer4 | 지점장 | signature | 황다은 |
| 대리인실명번호 | 대리인실명번호 | 대리인실명번호(AGENTID.NO) | text | 559-622721-13850 |
| check.자동화기기를이용한외화송금서비스신청 | check.자동화기기를이용한외화송금서비스신청 | ◈자동화기기를이용한외화송금서비스신청( | checkbox | 해지 |
| check.송금항목 | check.송금항목 | 송금항목 | checkbox | 거주자의 무증빙 해외송금 |
| check.송금항목2 | check.송금항목2 | 송금항목 | checkbox | 체재비 송금 |
| 인출계좌번호 | 인출계좌번호 | 인출계좌번호 | text | 055-099772-81205 |
| check.송금결과통보 | check.송금결과통보 | 송금결과통보 | checkbox | SMS |
| check.유학생송금 | check.유학생송금 | 유학생송금 | checkbox | 유학생 송금 |
| check.외국인근로자의보수송금 | check.외국인근로자의보수송금 | 외국인근로자의보수송금 | checkbox | 외국인 근로자의 보수 송금 |
| check.국내전신송금 | check.국내전신송금 | 국내전신송금 | checkbox | 국내 전신 송금 |
| 사전송금방식국내통관전수입대금을지급 | 사전송금방식국내통관전수입대금을지급 | 사전송금방식:국내통관(물품인수)전수입대금을지급 | number | 17,520,000 |
| check.대금송금후물품수령예정일 | check.대금송금후물품수령예정일 | 대금송금후물품(선적서류)수령예정일 | checkbox | 년 이내 |
| check.대금송금후물품수령예정일2 | check.대금송금후물품수령예정일2 | 대금송금후물품(선적서류)수령예정일 | checkbox | 년 초과 ( |
| check.일반수입 | check.일반수입 | 일반수입 | checkbox | 일반 수입 |
| check.중계무역 | check.중계무역 | 중계무역 | checkbox | 중계 무역 |
| check.외국인수수입 | check.외국인수수입 | 외국인수수입 | checkbox | 외국인수 수입 |
| check.현재수출계약체결 | check.현재수출계약체결 | 현재수출계약체결 | checkbox | 현재 수출계약 체결 |
| check.현재수출계약미체결 | check.현재수출계약미체결 | 현재수출계약미체결 | checkbox | 현재 수출계약 미체결 |
| date3 | date3 | 작성일 | date | 2026년 1월 31일 |
| signer5.name | signer5.name | 신청인 | text | 박찬연 |
| seal.signer5 | seal.signer5 | 신청인 | seal | 이민빈 |
| sign.signer5 | sign.signer5 | 신청인 | signature | 박찬연 |
| 대금송금후물품수령예정일 | 대금송금후물품수령예정일 | 대금송금후물품(선적서류)수령예정일 | date | 2026-01-19 |

### hana_official_408 · 본인확인서(FATCA CRS 개인,개인사업자용)(국문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 본인확인서(FATCA CRS 개인,개인사업자용)(국문). 기존 hf408 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/07/29/5-08-0334.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| customer.surname_en | customer.surname_en | 성(SurName) | text | PARK |
| customer.given_name_en | customer.given_name_en | 이름(GivenName) | text | CHANYEON |
| customer.birth | customer.birth | 생년월일 | date | 1990.02.10 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| tax.residence_list[].country | tax.residence_list[].country | 거주관할권*(1) | text | 영국 |
| tax.residence_list[].tin | tax.residence_list[].tin | 납세자번호(TIN) | text | 858712-6658495 |
| customer.overseas_address | customer.overseas_address | 해외영문주소 | text | 45 Le Loi St, District 1, Ho Chi Minh City |
| tax.no_tin_reason | tax.no_tin_reason | 내국인또는거주자증명서*또는반증증표*을제출한경우 | text | 생활자금 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 인성명 | text | 박찬연 |
| seal.signer | seal.customer | 인성명 | seal | 박찬연 |
| sign.signer | sign.customer | 인성명 | signature | 강순준 |
| signer2.name | signer2.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 김순우 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 박영준 |
| date2 | date2 | 작성일(년월일) | date | 2026.01.31 |
| customer.name | customer.name | 본인성명 | text | 박찬연 |
| agent.name | agent.name | 대리인성명 | text | 박영준 |
| agent.relation | agent.relation | 대리인관계 | text | 부 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 황보숙윤 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 한훈영 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 황민성 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 최서태 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 도상아 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 김혁태 |

### hana_official_413 · 고객확인서(법인,고유번호나 납세번호가 있는 임의 단체용)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 고객확인서(법인,고유번호나 납세번호가 있는 임의 단체용). 기존 hf413 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/06/17/3-08-1301.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 목록[].사업장 | 목록[].사업장 | 사업장(국내) | text |  |
| 대표자3 | 대표자3 | 대표자3 | text |  |
| 전화 | 전화 | 전화 | phone | 010-5907-7253 |
| 대표자1 | 대표자1 | 대표자1 | text |  |
| 대표자2 | 대표자2 | 대표자2 | text |  |
| 대표자32 | 대표자32 | 대표자3 | text |  |
| 한글명 | 한글명 | 한글명 | text | 박찬연 |
| customer.name_en | customer.name_en | 영문명(외국법인필수) | text | PARK CHANYEON |
| company.biz_item | corp.biz_item | 업종(업태/종목) | text | 무역 |
| customer.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 전화2 | 전화2 | 전화 | phone | 010-5907-7253 |
| customer.address2 | customer.address2 | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 전화3 | 전화3 | 전화 | phone | 010-5907-7253 |
| company.established | corp.established | 설립일 | date | 2018.11.01 |
| check.기업규모 | check.기업규모 | 기업규모 | checkbox | 대기업 |
| check.상장여부 | check.상장여부 | 상장여부 | checkbox | 상장 |
| 목록[].영문명 | 목록[].영문명 | 영문명 | text |  |
| FAX | FAX | FAX | phone | 043-783-2775 |
| company.biz_no | corp.biz_no | 사업자등록번호(고유번호및납세번호등포함) | biz_no | 264-82-36559 |
| 설립목적 | 설립목적 | 설립목적(비영리법인,단체) | text | 전세자금 |
| FAX2 | FAX2 | FAX | phone | 043-783-2775 |
| FAX3 | FAX3 | FAX | phone | 043-783-2775 |
| 홈페이지 | 홈페이지 | 홈페이지 | text |  |
| check.국내 | check.국내 | 국내 | checkbox | 유가증권시장 |
| 목록[].생년월일 | 목록[].생년월일 | 생년월일(사업자번호) | text | 2026년 1월 21일 |
| company.corp_reg_no | corp.corp_reg_no | 법인등록번호 | corp_reg_no | 200112-7448551 |
| 목록[].국적 | 목록[].국적 | 국적(본점소재지) | text |  |
| check.일회성거래 | check.일회성거래 | 일회성거래(무통장입금,수표발행☞지급등) | checkbox | 기타 ( |
| check.대표자정보 | check.대표자정보 | 대표자정보 | checkbox | 공동대표 |
| check.뉴욕증권거래소 | check.뉴욕증권거래소 | 뉴욕증권거래소 | checkbox | 뉴욕증권거래소 |
| check.홍콩증권거래소 | check.홍콩증권거래소 | 홍콩증권거래소 | checkbox | 홍콩증권거래소 |
| check.예 | check.예 | 예(비영리단체) | checkbox | 아니오(비영리단체 해당안됨) |
| check.계좌개설 | check.계좌개설 | 계좌개설 | checkbox | 저축 및 투자 |
| check.대출원리금상환결제 | check.대출원리금상환결제 | (예금,대출등) | checkbox | 대출원리금 상환 결제 |
| check.사업소득 | check.사업소득 | 사업소득 | checkbox | 부동산 양도소득 |
| check.상속증여 | check.상속증여 | 상속/증여 | checkbox | 기타 ( |
| check.추가확인 | check.추가확인 | 추가확인 | checkbox | 상품권매매업자 |
| check.필요업종 | check.필요업종 | 필요업종 | checkbox | 공인회계사업 |
| check.대표자 | check.대표자 | 대표자 | checkbox | 대표자 |
| 거래목적 | 거래목적 | 거래목적 | text | 의료비 |
| 25이상의결권이있는주식출자지분을보유한사람 | 25이상의결권이있는주식출자지분을보유한사람 | 25%이상의결권이있는주식/출자지분을보유한사람 | text |  |
| 의결권있는주식및출자지분의최대소유자 | 의결권있는주식및출자지분의최대소유자 | 의결권있는주식및출자지분의최대소유자 | text |  |
| 대표자또는임원등의과반수를선임한주주 | 대표자또는임원등의과반수를선임한주주 | 대표자또는임원등의과반수를선임한주주 | text |  |
| 법인단체를사실상지배하는자 | 법인단체를사실상지배하는자 | 법인•단체를사실상지배하는자 | text |  |
| 법인단체의대표자중1인 | 법인단체의대표자중1인 | 법인•단체의대표자중1인 | text |  |
| 목록[].한글명 | 목록[].한글명 | 한글명(상호명) | text | 천숙준 |
| check.25이상의결권이있는주식출자지분을보유한사람 | check.25이상의결권이있는주식출자지분을보유한사람 | 25%이상의결권이있는주식/출자지분을보유한사람 | checkbox | 보기1 |
| check.의결권있는주식및출자지분의최대소유자 | check.의결권있는주식및출자지분의최대소유자 | 의결권있는주식및출자지분의최대소유자 | checkbox | 보기1 |
| check.대표자또는임원등의과반수를선임한주주 | check.대표자또는임원등의과반수를선임한주주 | 대표자또는임원등의과반수를선임한주주 | checkbox | 보기1 |
| check.법인단체를사실상지배하는자 | check.법인단체를사실상지배하는자 | 법인•단체를사실상지배하는자 | checkbox | 보기1 |
| check.법인단체의대표자중1인 | check.법인단체의대표자중1인 | 법인•단체의대표자중1인 | checkbox | 보기1 |
| 목록[].지분율 | 목록[].지분율 | 지분율 | number | 10 |
| 항목 | 항목 | 항목 | text |  |
| 목록[].Y | 목록[].Y | Y | text |  |
| 목록[].N | 목록[].N | N | text |  |
| 지배자 | 지배자 | 지배자 | text |  |
| 목록[].지배형태 | 목록[].지배형태 | 지배형태 | text |  |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.relation | agent.relation | 본인과의관계 | text | 부 |
| agent.birth | agent.birth | 생년월일 | date | 1962.12.19 |
| agent.address | agent.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| agent.phone | agent.phone | 전화번호 | phone | 010-6515-4769 |
| check.국가또는지방자치단체1 | check.국가또는지방자치단체1 | 국가또는지방자치단체1 | checkbox | 공공단체 1 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | corp.name | 법인/단체명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 법인/단체명 | seal | 주식회사 대성패션 |
| sign.signer | sign.customer | 법인/단체명 | signature | (주)유니온무역 |
| check.작성자 | check.작성자 | 작성자( | checkbox | 대리인) 성명 |
| customer.name | customer.name | 위임인(법인/단체명) | text | 박찬연 |

### hana_official_414 · [필수] 개인(신용)정보 수집·이용·제공 동의서 [공공마이데이터 주민등록 등·초본 조회용]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. [필수] 개인(신용)정보 수집·이용·제공 동의서 [공공마이데이터 주민등록 등·초본 조회용]. 기존 hf414 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/06/10/7-08-0039.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의함 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의함 |
| 수집이용목적 | 수집이용목적 | 수집·이용목적 | text | 만기 해지 |
| 제공일로부터5년이내보유이용 | 제공일로부터5년이내보유이용 | -제공일로부터5년이내보유·이용 | text |  |
| 일반개인정보2 | 일반개인정보2 | ■일반개인정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 최우빈 |
| sign.signer | sign.customer | 본인성명 | signature | 강순준 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 강석호 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 박영준 |

### hana_official_416 · [필수] 개인(신용)정보 수집·이용·제공 동의서 [공공마이데이터 사업자정보 조회용]

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. [필수] 개인(신용)정보 수집·이용·제공 동의서 [공공마이데이터 사업자정보 조회용]. 기존 hf416 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/06/10/7-08-0035.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 고유식별정보 | 고유식별정보 | ■고유식별정보 | text |  |
| 일반개인정보 | 일반개인정보 | ■일반개인정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집☞이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집☞이용에동의하십니까? | checkbox | 동의하지 않음 |
| 수집이용목적 | 수집이용목적 | 수집·이용목적 | text | 본인 요청 |
| 제공일로부터5년이내보유이용 | 제공일로부터5년이내보유이용 | -제공일로부터5년이내보유·이용 | text |  |
| 고유식별정보2 | 고유식별정보2 | ■고유식별정보 | text |  |
| 일반개인정보2 | 일반개인정보2 | ■일반개인정보 | text |  |
| check.위고유식별정보제공에동의하십니까 | check.위고유식별정보제공에동의하십니까 | 위고유식별정보제공에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보제공에동의하십니까 | check.위개인정보제공에동의하십니까 | 위개인(신용)정보제공에동의하십니까? | checkbox | 동의함 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 현예지 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 강석호 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 박영준 |

### hana_official_419 · [필수] 개인(신용)정보 수집 · 이용 동의서 (비여신 금융거래)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. [필수] 개인(신용)정보 수집 · 이용 동의서 (비여신 금융거래). 기존 hf419 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2025/08/20/3-08-1294.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 신용거래정보 | 신용거래정보 | ■신용거래정보 | text |  |
| check.위고유식별정보수집이용에동의하십니까 | check.위고유식별정보수집이용에동의하십니까 | 위고유식별정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| check.위개인정보수집이용에동의하십니까 | check.위개인정보수집이용에동의하십니까 | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 동의하지 않음 |
| signer.name | customer.name | 본인성명 | text | 박찬연 |
| seal.signer | seal.customer | 본인성명 | seal | 현예지 |
| sign.signer | sign.customer | 본인성명 | signature | 박찬연 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer2.name | agent.name | 대리인성명 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인성명 | seal | 박영준 |
| sign.signer2 | sign.agent | 대리인성명 | signature | 이도민 |
| signer3.name | signer3.name | 법정대리인성명 | text | 박영준 |
| seal.signer3 | seal.signer3 | 법정대리인성명 | seal | 김승성 |
| sign.signer3 | sign.signer3 | 법정대리인성명 | signature | 박영준 |
| 온오프라인거래연계및본인식별 | 온오프라인거래연계및본인식별 | -온·오프라인(금융)거래연계및본인식별 | text |  |
| 금융사고조사분쟁해결민원처리 | 금융사고조사분쟁해결민원처리 | -금융사고조사,분쟁해결,민원처리 | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 확인 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 김연찬 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 류채서 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 기철연 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 확인 |

### hana_official_420 · 비대면 계좌개설 안심차단 서비스 신청서

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 비대면 계좌개설 안심차단 서비스 신청서. 기존 hf420 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2025/05/09/5-08-0737.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| check.구분 | check.구분 | 구분 | checkbox | 신청 |
| check.대리인정보 | check.대리인정보 | 대리인정보 | checkbox | 임의대리인 신청시에도 신청내역에 대한 안내는 신청인(본인)에게 통지됩니다 |
| customer.name | customer.name | 성명 | text | 박찬연 |
| customer.rrn | customer.rrn | 주민등록번호 | rrn | 900210-1****** |
| agent.name | agent.name | 성명 | text | 박영준 |
| agent.birth | agent.birth | 생년월일 | date | 1962년 12월 19일 |
| check.해제 | check.해제 | 해제 | checkbox | 해제 |
| check.휴대전화번호 | check.휴대전화번호 | 휴대전화번호 | checkbox | 신청내역 통지 동의 |
| 신청인과의관계 | 신청인과의관계 | 신청인과의관계 | text |  |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 신청인 | text | 박찬연 |
| seal.signer | seal.customer | 신청인 | seal | 박찬연 |
| sign.signer | sign.customer | 신청인 | signature | 강순준 |
| signer2.name | signer2.name | 대리인 | text | 박영준 |
| seal.signer2 | seal.agent | 대리인 | seal | 박영준 |
| sign.signer2 | sign.agent | 대리인 | signature | 이성원 |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 조원율 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 최호우 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 길유우 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 최형희 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 검인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 주상경 |

### hana_official_428 · 본인확인서(FATCA CRS 법인,임의단체용)(국문)

그룹: 하나은행 서식(원본) (`hana`)

하나은행 공개 원문을 대조한 HTML. 본인확인서(FATCA CRS 법인,임의단체용)(국문). 기존 hf428 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2024/01/05/5-08-0335.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| 가고객정보 | 가고객정보 | 가.고객정보 | text |  |
| company.name | corp.name | 법인(단체)명 | text | (주)유니온무역 |
| 구분선택 | 구분선택 | 구분선택(☑) | text |  |
| company.name2 | company.name2 | 법인(단체)명 | text | (주)유니온무역 |
| 口국내법인 | 口국내법인 | 口국내법인(단체) | text |  |
| company.biz_no | corp.biz_no | 사업자번호 | biz_no | 264-82-36559 |
| customer.phone | customer.phone | 연락처 | phone | 010-5907-7253 |
| 거주관할권 | 거주관할권 | 거주관할권 | text |  |
| 납세자번호 | 납세자번호 | 납세자번호(TIN) | text | 855637-7307455 |
| 관할권주소 | 관할권주소 | 관할권(소재지)주소(본점,설립관할권) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| date | date | 작성일 | date | 2026년 1월 31일 |
| signer.name | signer.name | 법인명 | text | (주)유니온무역 |
| seal.signer | seal.corp | 법인명 | seal | 주식회사 한빛패션 |
| sign.signer | sign.customer | 법인명 | signature | (주)삼정전자 |
| 나확인사항 | 나확인사항 | 나.확인사항 | text |  |
| 口11공익적법인 | 口11공익적법인 | 口11.공익적법인(단체) | text |  |
| seal.staff.본인확인 | seal.staff.본인확인 | 본인확인 | seal | 박지승 |
| sign.staff.본인확인 | sign.staff.본인확인 | 본인확인 | signature | 김원준 |
| seal.staff.담당 | seal.staff.담당 | 담당 | seal | 검인 |
| sign.staff.담당 | sign.staff.담당 | 담당 | signature | 왕혜현 |
| seal.staff.책임자 | seal.staff.책임자 | 책임자 | seal | 확인 |
| sign.staff.책임자 | sign.staff.책임자 | 책임자 | signature | 선우철지 |
| c | c | c | text |  |
| d | d | d | text |  |
| 口EIN口GIIN口기타 | 口EIN口GIIN口기타 | 口EIN口GIIN口기타 | text | 해당 없음 |
| 목록[].실질지배자 | 목록[].실질지배자 | 실질지배자(1) | text |  |
| 목록[].거주관할권 | 목록[].거주관할권 | 거주관할권(국가) | text |  |
| customer.name | customer.name | 이름(GivenName) | text | 박찬연 |
| 목록[].납세자번호 | 목록[].납세자번호 | 납세자번호(TIN) | text | 947168-6884157 |
| customer.name2 | customer.name2 | 이름(GivenName) | text | 박찬연 |
| customer.name3 | customer.name3 | 이름(GivenName) | text | 박찬연 |
| 거주관할권주소 | 거주관할권주소 | 거주관할권주소(영문) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 거주관할권주소2 | 거주관할권주소2 | 거주관할권주소(영문) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| 거주관할권주소3 | 거주관할권주소3 | 거주관할권주소(영문) | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| check.미발급국가 | check.미발급국가 | 미발급국가 | checkbox | 미취득 (사유기재 |
| check.미발급국가2 | check.미발급국가2 | 미발급국가 | checkbox | 미발급국가 |
| check.미발급국가3 | check.미발급국가3 | 미발급국가 | checkbox | 미취득 (사유기재 |
| 지분율 | 지분율 | 지분율(%) | number | 50 |
| 성 | 성 | 성(Surname) | text |  |
| 지분율2 | 지분율2 | 지분율(%) | number | 100 |
| 성2 | 성2 | 성(Surname) | text |  |
| 지분율3 | 지분율3 | 지분율(%) | number | 30 |
| 성3 | 성3 | 성(Surname) | text |  |
| customer.birth | customer.birth | 생년월일 | date | 1990년 2월 10일 |
| customer.birth2 | customer.birth2 | 생년월일 | date | 1990년 2월 10일 |
| customer.birth3 | customer.birth3 | 생년월일 | date | 1990년 2월 10일 |
| 口01주권상장법인 | 口01주권상장법인 | 口01.주권상장법인 | text |  |
| 口03미국정부기관등 | 口03미국정부기관등 | 口03.미국정부기관등 | text |  |
| 口25별정우체국연금관리단 | 口25별정우체국연금관리단 | 口25.별정우체국연금관리단 | text |  |

### hana_personal_agreement · 대출거래약정서(가계용)

그룹: 하나은행 서식(원본) (`hana`)

대출거래약정서(가계용) 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://image.kebhana.com/cont/download/documents/provide/0000003061040_20210325.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.name | customer.name | 본인 | text | 박찬연 |
| official.address | customer.address | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.subject | official.subject | 대출과목 | text | 주택담보대출 |
| official.amount | official.amount | 대출금액 | amount | 292,000,000 |
| terms.method | terms.method | 개별거래 | checkbox | 개별거래 |
| terms.fixed | terms.fixed | 고정금리 | checkbox | 고정금리 |
| terms.fixed_choice | terms.fixed_choice | 확정금리 | checkbox | 확정금리 |
| terms.rate | terms.rate | 약정이율 | number | 3.95 |
| terms.start0 | terms.start0 | 대출개시일년 | number | 2026 |
| terms.start1 | terms.start1 | 대출개시일월 | number | 02 |
| terms.start2 | terms.start2 | 대출개시일일 | number | 16 |
| terms.end0 | terms.end0 | 대출만료일년 | number | 2066 |
| terms.end1 | terms.end1 | 대출만료일월 | number | 02 |
| terms.end2 | terms.end2 | 대출만료일일 | number | 16 |
| terms.late | terms.late | 연체가산율 | number | 3 |
| terms.max_late | terms.max_late | 최고연체율 | amount | 15 |
| terms.execution | terms.execution | 전액실행 | checkbox | 전액실행 |
| terms.repay | terms.repay | 만기일시상환 | checkbox | 만기일시상환 |
| terms.written0 | terms.written0 | 작성일년 | number | 26 |
| terms.written1 | terms.written1 | 작성일월 | number | 02 |
| terms.written2 | terms.written2 | 작성일일 | number | 09 |
| official.amount_won | official.amount_won | 대출(한도)금액(₩) | amount | 292,000,000 |
| official.start_date_check | official.start_date_check | 대출개시일날짜지정 | text | V |
| official.maturity_date_check | official.maturity_date_check | 대출기간만료일날짜지정 | text | V |
| official.prepay_target | official.prepay_target | 중도상환해약금대상 | text | V |
| official.prepay_rate | official.prepay_rate | 중도상환해약금률(%) | amount | 30 |
| official.repay_lump_full | official.repay_lump_full | 일시상환대출기간만료일에전액상환 | text | V |
| official.interest_monthly | official.interest_monthly | 이자지급매월지정일 | text | V |
| official.interest_day | official.interest_day | 이자지급일(매월○일) | amount | 15 |
| official.disburse_account | official.disburse_account | 대출금입금(실행)계좌 | account_no | 기업은행 171-760452-29-611 |
| official.debit_account | official.debit_account | 원(리)금및이자자동이체결제계좌 | account_no | 기업은행 171-760452-29-611 |
| official.fee_consent_sign | official.fee_consent_sign | 비용의납부동의본인서명 | text | 박찬연 |
| official.amount_won_copy | official.amount_won_copy | 대출(한도)금액(₩)(고객교부용) | amount | 292,000,000 |
| official.start_date_check_copy | official.start_date_check_copy | 대출개시일날짜지정(고객교부용) | text | V |
| official.maturity_date_check_copy | official.maturity_date_check_copy | 대출기간만료일날짜지정(고객교부용) | text | V |
| official.prepay_target_copy | official.prepay_target_copy | 중도상환해약금대상(고객교부용) | text | V |
| official.prepay_rate_copy | official.prepay_rate_copy | 중도상환해약금률(%)(고객교부용) | amount | 30 |
| official.repay_lump_full_copy | official.repay_lump_full_copy | 일시상환대출기간만료일에전액상환(고객교부용) | text | V |
| official.interest_monthly_copy | official.interest_monthly_copy | 이자지급매월지정일(고객교부용) | text | V |
| official.interest_day_copy | official.interest_day_copy | 이자지급일(매월○일)(고객교부용) | amount | 15 |
| official.name_copy | official.name_copy | 본인 | text | 박찬연 |
| official.address_copy | official.address_copy | 주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.subject_copy | official.subject_copy | 대출과목 | text | 주택담보대출 |
| official.amount_copy | official.amount_copy | 대출금액 | amount | 292,000,000 |
| terms.method_copy | terms.method_copy | 개별거래 | checkbox | 개별거래 |
| terms.fixed_copy | terms.fixed_copy | 고정금리 | checkbox | 고정금리 |
| terms.fixed_choice_copy | terms.fixed_choice_copy | 확정금리 | checkbox | 확정금리 |
| terms.rate_copy | terms.rate_copy | 약정이율 | number | 3.95 |
| terms.start0_copy | terms.start0_copy | 대출개시일년 | number | 2026 |
| terms.start1_copy | terms.start1_copy | 대출개시일월 | number | 02 |
| terms.start2_copy | terms.start2_copy | 대출개시일일 | number | 16 |
| terms.end0_copy | terms.end0_copy | 대출만료일년 | number | 2066 |
| terms.end1_copy | terms.end1_copy | 대출만료일월 | number | 02 |
| terms.end2_copy | terms.end2_copy | 대출만료일일 | number | 16 |
| terms.late_copy | terms.late_copy | 연체가산율 | number | 3 |
| terms.max_late_copy | terms.max_late_copy | 최고연체율 | amount | 15 |
| terms.execution_copy | terms.execution_copy | 전액실행 | checkbox | 전액실행 |
| terms.repay_copy | terms.repay_copy | 만기일시상환 | checkbox | 만기일시상환 |
| terms.written0_copy | terms.written0_copy | 작성일년 | number | 26 |
| terms.written1_copy | terms.written1_copy | 작성일월 | number | 02 |
| terms.written2_copy | terms.written2_copy | 작성일일 | number | 09 |
| official.disburse_account_copy | official.disburse_account_copy | 대출금입금(실행)계좌(고객교부용) | text | 기업은행 171-760452-29-611 |
| official.debit_account_copy | official.debit_account_copy | 원(리)금및이자자동이체결제계좌(고객교부용) | text | 기업은행 171-760452-29-611 |
| official.fee_consent_sign_copy | official.fee_consent_sign_copy | 비용의납부동의본인서명(고객교부용) | text | 박찬연 |

### hana_specific_guarantee · 보증서(특정채무보증용)

그룹: 하나은행 서식(원본) (`hana`)

보증서(특정채무보증용) 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://image.kebhana.com/cont/download/documents/provide/b000003061059_20210325.pdf

연결 업무: 없음 · 단일 서류 과제로 사용 가능

| 원본 필드 키 | 문항 키 | 항목명 | 타입 | 값 예시 |
|---|---|---|---|---|
| official.guarantor | related.name | 연대보증인 | text | 박찬연 |
| official.address | related.address | 보증인주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.debtor | customer.name | 채무자성명 | text | (주)유니온무역 |
| official.amount | official.amount | 피보증채무금액 | amount | 4,710,000 |
| official.guarantor_copy | official.guarantor_copy | 연대보증인 | text | 박찬연 |
| official.address_copy | official.address_copy | 보증인주소 | text | 서울특별시 서초구 방배로 524, 110동 501호 |
| official.debtor_copy | official.debtor_copy | 채무자성명 | text | (주)유니온무역 |
| official.amount_copy | official.amount_copy | 피보증채무금액 | amount | 4,710,000 |
