# 은행 서식 — 서류별 항목

키 규칙과 타입은 [README.md](README.md)에 있습니다.


## 대출거래신청서 (`loan_application`) — 키 63개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank` | 은행명 | text | 100% | 기업은행 |
| `branch` | 취급점 | text | 100% | 범어지점 |
| `applicant.name` | 성명 | text | 100% | 박찬연 |
| `applicant.rrn` | 실명번호 | rrn | 100% | 900210-1659382 |
| `applicant.zipcode` | 우편번호 | number | 100% | 06931 |
| `applicant.address` | 자택주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `applicant.mobile` | 휴대전화 | phone | 100% | 010-5907-7253 |
| `applicant.home_phone` | 자택전화 | phone | 100% | 02-5105-8357 |
| `applicant.email` | E-mail | text | 100% | chanyeon363@naver.com |
| `applicant.work_phone` | 직장전화 | phone | 100% | 043-783-2775 |
| `housing` | 주택소유구분 | checkbox | 100% | 보기: 자가 / 전세 / 월세 / 기타 |
| `dwelling` | 주거형태 | checkbox | 100% | 보기: 아파트 / 단독 / 다세대 / 연립·빌라 / 오피스텔 / 기타 |
| `workplace.job_type` | 직업구분 | checkbox | 100% | 보기: 급여소득자 / 공무원 / 전문직 / 자영업자 / 기타 |
| `workplace.name` | 직장명 | text | 100% | 주식회사 태평양무역 |
| `workplace.department` | 근무부서 | text | 100% | 구매팀 |
| `workplace.position` | 직위 | text | 100% | 대리 |
| `workplace.hire_date` | 입사년월일 | date | 100% | 2020-05-08 |
| `workplace.annual_income` | 연소득(본인) | text | 100% | 5,460만원 |
| `workplace.address` | 직장주소 | text | 100% | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 |
| `debts[].lender` | 금융기관 | text | 77% | 국민은행 |
| `debts[].kind` | 대출종류 | text | 77% | 현금서비스 |
| `debts[].balance` | 잔액 | amount | 77% | 5,800,000 |
| `debts[].maturity` | 만기일 | date | 77% | 2027.03.23 |
| `debts[].refinance` | 상환여부 | text | 77% | 유지 |
| `assets[].kind` | 종류 | text | 93% | 자동차 |
| `assets[].location` | 소재지 | text | 93% | 쏘렌토 (2020년식) |
| `assets[].value` | 평가금액 | amount | 93% | 21,800,000 |
| `loan.subject` | 대출과목 | text | 100% | 주택담보대출 |
| `loan.product` | 상품명 | text | 100% | 아파트 담보대출 |
| `loan.amount_korean` | 대출신청금액(한글) | amount_korean | 100% | 일금 이억구천이백만원정 |
| `loan.amount` | 대출신청금액 | amount | 100% | 292,000,000 |
| `loan.term` | 대출기간 | text | 100% | 40년 |
| `loan.hope_date` | 대출희망일 | date | 100% | 2026-02-16 |
| `loan.repayment` | 상환방법 | checkbox | 100% | 보기: 만기일시 / 원금균등분할 / 원리금균등분할 / 혼합 |
| `loan.rate_type` | 금리방식 | checkbox | 100% | 보기: 고정 / 변동 / 혼합 |
| `loan.interest_day` | 이자납입일 | text | 100% | 매월 15일 |
| `loan.purpose_category` | 자금용도구분 | checkbox | 100% | 보기: 주택구입 / 주택임차 / 부채상환 / 생활비 / 교육비 / 기타 |
| `loan.purpose` | 세부용도 | text | 100% | 주택구입자금 |
| `collateral` | 담보구분 | checkbox | 100% | 보기: 신용 / 부동산 / 보증 |
| `collateral_detail` | 담보내용 | text | 100% | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (아파트, 전용… |
| `loan.debit_bank` | 이체은행 | text | 100% | 기업은행 |
| `loan.debit_account` | 이체계좌번호 | account_no | 100% | 171-760452-29-611 |
| `loan.debit_holder` | 예금주 | text | 100% | 박찬연 |
| `agent.name` | 대리인성명 | text | 13% | 우나민 |
| `agent.rrn` | 대리인실명번호 | rrn | 13% | 671023-2****** |
| `agent.relation` | 본인과의관계 | text | 13% | 모 |
| `agent.phone` | 대리인연락처 | phone | 13% | 010-7560-2133 |
| `agent.poa` | 위임장 | checkbox | 13% | 보기: 첨부 / 미첨부 |
| `manual_received` | 설명서수령확인 | checkbox | 100% | 보기: 예 / 아니오 |
| `consent` | 개인(신용)정보동의 | checkbox | 100% | 보기: 동의함 / 동의하지 않음 |
| `apply_date` | 신청일 | date | 100% | 2026년 1월 31일 |
| `signature` | 신청인 | text | 100% | 박찬연 |
| `seal.applicant` | 신청인 | seal | 100% | 김소윤 |
| `sign.applicant` | 신청인 | signature | 100% | 박찬연 |
| `seal.agent` | 대리인 | seal | 13% | 우나민 |
| `sign.agent` | 대리인 | signature | 13% | 강형은 |
| `co_borrower.name` | 공동차주성명 | text | 7% | 설기현 |
| `co_borrower.rrn` | 공동차주실명번호 | rrn | 7% | 851210-1****** |
| `co_borrower.relation` | 신청인과의관계 | text | 7% | 배우자 |
| `co_borrower.mobile` | 공동차주휴대전화 | phone | 7% | 010-2037-1392 |
| `co_borrower.workplace` | 공동차주직장 | text | 7% | 자영업 |
| `seal.co_borrower` | 공동차주 | seal | 7% | 설기현 |
| `sign.co_borrower` | 공동차주 | signature | 7% | 오성원 |

## 기업여신 신청서 (`loan_application_corp`) — 키 48개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank` | 은행명 | text | 100% | 기업은행 |
| `branch` | 취급점 | text | 100% | 범어지점 |
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `company.name_en` | 영문명 | text | 100% | Union Trading Co., Ltd. |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `company.established` | 설립일 | date | 100% | 2018.11.01 |
| `company.industry` | 업태/종목 | text | 100% | 도매 및 소매업 / 무역 |
| `company.employees` | 종업원수 | text | 100% | 312명 |
| `company.size` | 기업규모 | checkbox | 100% | 보기: 대기업 / 중견기업 / 중소기업 / 소상공인 |
| `company.capital` | 자본금 | amount | 100% | 50,000,000원 |
| `company.revenue` | 매출액 | amount | 100% | 61,800,000,000원 |
| `company.revenue_year` | 결산연도 | text | 100% | 2025년 |
| `company.address` | 본점소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| `company.phone` | 전화번호 | phone | 100% | 02-9508-6789 |
| `company.fax` | 팩스번호 | phone | 100% | 02-716-6590 |
| `contact.name` | 담당자 | text | 100% | 길예태 |
| `contact.position` | 부서/직위 | text | 100% | 회계팀 과장 |
| `contact.phone` | 연락처 | phone | 100% | 010-5228-8790 |
| `contact.email` | E-mail | text | 100% | biz@union.co.kr |
| `loan.subject` | 여신과목 | checkbox | 100% | 보기: 일반자금대출 / 시설자금대출 / 한도대출 |
| `loan.product` | 상품명 | text | 100% | 중소기업 운전자금대출 |
| `loan.rate_type` | 금리종류 | checkbox | 100% | 보기: 고정금리 / 변동금리 |
| `loan.amount_korean` | 신청금액(한글) | amount_korean | 100% | 일금 삼십억원정 |
| `loan.amount` | 신청금액 | amount | 100% | 3,000,000,000원 |
| `loan.term` | 여신기간 | text | 100% | 1년 |
| `loan.hope_date` | 대출희망일 | date | 100% | 2026-02-03 |
| `loan.repayment` | 상환방법 | text | 100% | 만기일시상환 |
| `loan.fund_type` | 자금구분 | checkbox | 100% | 보기: 운전자금 / 시설자금 |
| `loan.purpose` | 자금용도 | text | 100% | 매출채권 회수 지연에 따른 운전자금 |
| `loan.deposit_account` | 대출금입금계좌 | account_no | 100% | 기업은행 198-866024-83-977 |
| `loan.collateral` | 담보구분 | checkbox | 100% | 보기: 신용 / 부동산 / 보증서 / 예·적금 |
| `loan.collateral_detail` | 담보/보증내용 | text | 100% | 기술보증기금 보증서 (보증비율 85%) |
| `other_loans[].lender` | 금융기관 | text | 90% | 신한캐피탈 |
| `other_loans[].kind` | 여신종류 | text | 90% | 시설자금대출 |
| `other_loans[].balance` | 잔액 | amount | 90% | 1,140 |
| `other_loans[].collateral` | 담보 | text | 90% | 부동산 |
| `other_loans_total` | 합계 | amount | 33% | 9,330 |
| `agent.name` | 대리인성명 | text | 23% | 길예태 |
| `agent.position` | 대리인직위 | text | 23% | 회계팀 과장 |
| `agent.rrn` | 대리인실명번호 | rrn | 23% | 841126-1****** |
| `agent.phone` | 대리인연락처 | phone | 23% | 010-5228-8790 |
| `apply_date` | 신청일 | date | 100% | 2026년 1월 31일 |
| `signature` | 대표이사 | text | 100% | 박찬연 |
| `seal.corp` | 법인인감 | seal | 100% | 대표이사 |
| `seal.agent` | 대리인 | seal | 23% | 이채재 |
| `sign.agent` | 대리인 | signature | 23% | 길예태 |

## 대출거래약정서(가계용) (`credit_agreement`) — 키 43개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank` | 은행명 | text | 100% | 기업은행 |
| `creditor` | 채권자 | text | 100% | 중소기업은행 |
| `branch` | 취급점 | text | 100% | 범어지점 |
| `debtor.name` | 성명 | text | 100% | 박찬연 |
| `debtor.rrn` | 실명번호 | rrn | 100% | 900210-1659382 |
| `debtor.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `debtor.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `loan.subject` | 대출과목 | text | 100% | 주택담보대출 |
| `loan.product` | 상품명 | text | 100% | 아파트 담보대출 |
| `loan.method` | 거래구분 | checkbox | 100% | 보기: 개별거래 / 한도거래 |
| `loan.account_no` | 대출계좌번호 | account_no | 100% | 740-757492-44-140 |
| `loan.amount_korean` | 대출(한도)금액(한글) | amount_korean | 100% | 금 이억구천이백만원整 |
| `loan.amount` | 대출(한도)금액 | amount | 100% | 292,000,000원 |
| `loan.start_date` | 대출개시일 | date | 100% | 2026.02.16 |
| `loan.maturity` | 대출기간만료일 | date | 100% | 2066.02.16 |
| `loan.rate_type` | 금리종류 | checkbox | 100% | 보기: 고정금리 / 변동금리 / 혼합금리 |
| `loan.base_rate_name` | 기준금리종류 | text | 100% | CD 91일물 |
| `loan.base_rate` | 기준금리 | percent | 100% | 2.87% |
| `loan.spread` | 가산금리 | percent | 100% | 1.58% |
| `loan.pref_rate` | 우대금리 | percent | 100% | 0.50% |
| `loan.applied_rate` | 대출이자율 | percent | 100% | 연 3.95% |
| `loan.rate_reset` | 금리변동주기 | text | 100% | 3개월 |
| `loan.interest_pay` | 이자지급시기 | text | 100% | 매월 15일 (후취) |
| `loan.interest_calc` | 이자계산방법 | text | 100% | 1년을 365일(윤년 366일)로 보고 1일 단위로 계산 |
| `loan.repayment` | 상환방법 | checkbox | 100% | 보기: 만기일시상환 / 원금균등분할상환 / 원리금균등분할상환 |
| `loan.installment` | 분할상환횟수 | text | 100% | 480회 (매월) |
| `loan.debit_account` | 자동이체계좌 | account_no | 100% | 기업은행 171-760452-29-611 |
| `loan.prepay_fee` | 중도상환해약금 | text | 100% | 중도상환금액 × 0.74% × 잔존일수 ÷ 대출기간일수 (3년 경과 시 … |
| `loan.late_rate` | 지연배상금률 | text | 100% | 대출이자율 + 연체가산이자율 연 3% (현재 연 6.95%, 최고 연 1… |
| `stamp_tax` | 인지세 | text | 100% | 150,000원 (고객 75,000원 / 은행 75,000원) |
| `explained` | 설명이해확인 | checkbox | 100% | 보기: 예 / 아니오 |
| `handwritten` | 자필기재 | text | 100% | 설명들었음 |
| `contract_date` | 약정일 | date | 100% | 2026년 2월 9일 |
| `signature` | 채무자 | text | 100% | 박찬연 |
| `seal.debtor` | 채무자 | seal | 100% | 박찬연 |
| `sign.debtor` | 채무자 | signature | 100% | 김소윤 |
| `co_borrower.name` | 공동차주성명 | text | 7% | 김순우 |
| `co_borrower.rrn` | 공동차주실명번호 | rrn | 7% | 810108-2****** |
| `co_borrower.address` | 공동차주주소 | text | 7% | 경기도 수원시 영통구 중부대로 379, 501호 (매탄동) |
| `co_borrower.phone` | 공동차주연락처 | phone | 7% | 010-9897-2197 |
| `seal.co_borrower` | 공동차주 | seal | 7% | 천숙승 |
| `sign.co_borrower` | 공동차주 | signature | 7% | 김순우 |
| `special_terms[]` | 특약사항 | text | 23% | 자동이체계좌 잔액 부족으로 이자를 납입하지 못한 경우 은행은 채무자의 당… |

## 여신거래약정서(기업용) (`credit_agreement_corp`) — 키 43개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank` | 은행명 | text | 100% | 기업은행 |
| `creditor` | 채권자 | text | 100% | 중소기업은행 |
| `branch` | 취급점 | text | 100% | 범어지점 |
| `debtor.name` | 상호(법인명) | text | 100% | (주)유니온무역 |
| `debtor.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `debtor.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `debtor.ceo` | 대표이사 | text | 100% | 박찬연 |
| `debtor.phone` | 전화번호 | phone | 100% | 02-9508-6789 |
| `debtor.address` | 본점소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| `loan.subject` | 여신과목 | text | 100% | 일반자금대출 |
| `loan.product` | 상품명 | text | 100% | 중소기업 운전자금대출 |
| `loan.method` | 거래방법 | checkbox | 100% | 보기: 개별거래 / 한도거래 |
| `loan.account_no` | 여신계좌번호 | account_no | 100% | 203-617585-91-545 |
| `loan.amount_korean` | 여신(한도)금액(한글) | amount_korean | 100% | 금 삼십억원정 |
| `loan.amount` | 여신(한도)금액 | amount | 100% | 3,000,000,000원 |
| `loan.start_date` | 여신개시일 | date | 100% | 2026년 2월 3일 |
| `loan.maturity` | 여신기간만료일 | date | 100% | 2027년 2월 3일 |
| `loan.purpose` | 자금용도 | text | 100% | 매출채권 회수 지연에 따른 운전자금 |
| `loan.rate_type` | 금리종류 | checkbox | 100% | 보기: 고정금리 / 변동금리 |
| `loan.base_rate_name` | 기준금리종류 | text | 100% | 금융채 1년물(AAA) |
| `loan.base_rate` | 기준금리 | percent | 100% | 3.23% |
| `loan.spread` | 가산금리 | percent | 100% | 1.75% |
| `loan.pref_rate` | 우대금리 | percent | 100% | 0.00% |
| `loan.applied_rate` | 여신이자율 | percent | 100% | 연 4.98% |
| `loan.rate_reset` | 금리변동주기 | text | 100% | 해당없음 |
| `loan.interest_pay` | 이자지급시기 | text | 100% | 매월 10일 |
| `loan.interest_calc` | 이자계산방법 | text | 100% | 1년을 365일(윤년 366일)로 보고 1일 단위로 계산 |
| `loan.repayment` | 상환방법 | text | 100% | 만기일시상환 |
| `loan.debit_account` | 자동이체계좌 | account_no | 100% | 기업은행 198-866024-83-977 |
| `loan.prepay_fee` | 중도상환해약금 | text | 100% | 중도상환금액 × 0.50% × 잔존일수 ÷ 대출기간일수 (3년 경과 시 … |
| `loan.late_rate` | 지연배상금률 | text | 100% | 대출이자율 + 연체가산이자율 연 3% (현재 연 7.98%, 최고 연 1… |
| `stamp_tax` | 인지세 | text | 100% | 350,000원 (고객 175,000원 / 은행 175,000원) |
| `explained` | 설명이해확인 | checkbox | 100% | 보기: 예 / 아니오 |
| `contract_date` | 약정일 | date | 100% | 2026년 2월 3일 |
| `signature` | 대표이사 | text | 100% | 박찬연 |
| `seal.corp` | 법인인감 | seal | 100% | 대표이사 |
| `special_terms[]` | 특약사항 | text | 27% | 채무자는 매 반기 종료 후 60일 이내에 부가가치세 과세표준증명 및 국세… |
| `guarantors[].name` | 연대보증인 | text | 13% | 김아진 |
| `guarantors[].rrn` | 실명번호 | rrn | 13% | 880114-2****** |
| `guarantors[].address` | 주소 | text | 13% | 강원특별자치도 춘천시 후석로 147, 120동 801호 |
| `guarantors[].relation` | 채무자와의관계 | text | 13% | 대표이사(실제경영자) |
| `seal.guarantor` | 보증인 | seal | 13% | 김아진인 |
| `seal.guarantor2` | 보증인 | seal | 10% | 천지영인 |

## 근저당권설정계약서 (`collateral_agreement`) — 키 43개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank` | 은행명 | text | 100% | 기업은행 |
| `creditor.name` | 채권자겸근저당권자 | text | 100% | 중소기업은행 |
| `creditor.branch` | 취급점 | text | 100% | 범어지점 |
| `mortgagor.name` | 근저당권설정자 | text | 100% | 박찬연 |
| `mortgagor.rrn` | 실명번호 | rrn | 100% | 900210-1****** |
| `mortgagor.address` | 설정자주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `co_mortgagor.name` | 공동설정자 | text | 23% | 서민진 |
| `co_mortgagor.share` | 지분 | text | 23% | 3분의 1 |
| `co_mortgagor.rrn` | 공동설정자실명번호 | rrn | 23% | 890630-2189779 |
| `co_mortgagor.address` | 공동설정자주소 | text | 23% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `debtor.name` | 채무자 | text | 100% | 박찬연 |
| `debtor.address` | 채무자주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `rank` | 순위 | number | 100% | 1 |
| `max_amount_korean` | 채권최고액(한글) | amount_korean | 100% | 금 삼억팔천만원整 |
| `max_amount` | 채권최고액 | amount | 100% | 380,000,000 |
| `scope` | 피담보채무의범위 | text | 100% | 특정근담보 |
| `secured_debt` | 피담보채무 | text | 100% | 2026년 2월 9일자 대출거래약정서(가계용) |
| `settlement_type` | 결산기유형 | text | 100% | 지정형 |
| `settlement` | 결산기 | text | 100% | 2066.02.16 |
| `property.location` | 소재지 | text | 100% | 경기도 수원시 영통구 원천동 87 한신휴플러스에듀포레 |
| `property.road_address` | 도로명주소 | text | 100% | 경기도 수원시 영통구 매탄로 376 |
| `property.structure` | 구조 | text | 100% | 철근콘크리트구조 |
| `property.floors` | 층수 | text | 100% | 17층 |
| `property.unit` | 건물번호 | text | 100% | 115동 2104호 |
| `property.kind` | 건물종류 | text | 100% | 아파트 |
| `property.exclusive_area` | 전용면적 | text | 100% | 101.84㎡ |
| `property.land_right` | 대지권 | text | 100% | 소유권대지권 9,562.1분의 54.47 |
| `property.unique_no` | 고유번호 | text | 100% | 1792-2013-094176 |
| `scope_handwritten` | 자필기재(피담보채무범위) | text | 100% | 특정근담보 |
| `handwritten_confirm` | 자필기재(확인) | text | 100% | 확인함 |
| `contract_date` | 계약일 | date | 100% | 2026년 2월 9일 |
| `signature_debtor` | 채무자 | text | 100% | 박찬연 |
| `seal.debtor` | 채무자 | seal | 100% | 박찬연 |
| `sign.debtor` | 채무자 | signature | 100% | 이욱유 |
| `signature_mortgagor` | 근저당권설정자 | text | 100% | 박찬연 |
| `seal.mortgagor` | 근저당권설정자 | seal | 100% | 박찬연인 |
| `seal.co_mortgagor` | 인감 | seal | 23% | 서민진인 |
| `joint_collateral[].kind` | 종류 | text | 20% | 토지 |
| `joint_collateral[].location` | 소재지번 | text | 20% | 인천광역시 연수구 송도동 517 |
| `joint_collateral[].detail` | 지목면적 | text | 20% | 잡종지 325.6㎡ |
| `joint_collateral[].unique_no` | 고유번호 | text | 20% | 1236-1995-087174 |
| `special_terms[]` | 특약사항 | text | 20% | 이 근저당권은 공동담보로서 각 담보물건은 피담보채무 전액을 담보하며, 일… |
| `mortgagor_relation` | 채무자와의관계 | text | 7% | 부 |

## 보증약정서 (`guarantee_agreement`) — 키 33개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank` | 은행명 | text | 100% | 기업은행 |
| `creditor` | 채권자 | text | 100% | 중소기업은행 |
| `branch` | 취급점 | text | 100% | 범어지점 |
| `debtor.name` | 채무자 | text | 100% | (주)유니온무역 |
| `debtor.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `debtor.ceo` | 대표자 | text | 100% | 박찬연 |
| `debtor.address` | 소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `guarantor.name` | 보증인 | text | 100% | 박찬연 |
| `guarantor.rrn` | 실명번호 | rrn | 100% | 900210-1****** |
| `guarantor.address` | 보증인주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `guarantor.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `guarantor.relation` | 채무자와의관계 | text | 100% | 대표이사 |
| `method` | 보증방법 | text | 100% | 한정근보증 |
| `secured_debt` | 피보증채무 | text | 100% | 일반자금대출 거래 |
| `max_amount_korean` | 보증채무최고액(한글) | amount_korean | 100% | 금 삼십구억원정 |
| `max_amount` | 보증채무최고액 | amount | 100% | 3,900,000,000 |
| `period` | 보증기간 | text | 100% | 2026년 2월 3일 ~ 2029년 2월 3일 |
| `handwritten.method` | 자필보증방법 | text | 100% | 한정근보증 |
| `handwritten.name` | 자필성명 | text | 100% | 박찬연 |
| `handwritten.max_amount` | 자필보증채무최고액 | amount_korean | 100% | 금 삼십구억원정 |
| `handwritten.confirm` | 자필설명확인 | text | 100% | 충분히 설명듣고 이해함 |
| `explained` | 설명이해확인 | checkbox | 100% | 보기: 예 / 아니오 |
| `contract_date` | 약정일 | date | 100% | 2026년 02월 03일 |
| `signature` | 보증인 | text | 100% | 박찬연 |
| `seal.guarantor` | 보증인 | seal | 100% | 강순준인 |
| `special_terms[]` | 특약사항 | text | 37% | 공동보증인이 있는 경우 각 보증인은 보증채무최고액 2,400,000,00… |
| `co_guarantors[].name` | 보증인 | text | 17% | 정주하 |
| `co_guarantors[].rrn` | 실명번호 | rrn | 17% | 650617-2119564 |
| `co_guarantors[].address` | 보증인주소 | text | 17% | 서울특별시 종로구 자하문로 26, 115동 503호 |
| `co_guarantors[].phone` | 연락처 | phone | 17% | 010-6311-7824 |
| `co_guarantors[].relation` | 채무자와의관계 | text | 17% | 감사 |
| `seal.co_guarantor` | 인감 | seal | 17% | 정주하인 |
| `seal.co_guarantor2` | 인감 | seal | 7% | 원주연인 |

## 자동이체 신청서 (`auto_transfer_application`) — 키 34개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank` | 은행명 | text | 100% | 기업은행 |
| `biller.name` | 수납기관 | text | 100% | 중소기업은행 |
| `branch` | 취급점 | text | 100% | 범어지점 |
| `kind` | 신청구분 | checkbox | 100% | 보기: 신규 / 변경 / 해지 |
| `biller.fee_type` | 요금종류 | text | 100% | 대출원리금(주택담보대출) |
| `target` | 이체대상 | checkbox | 100% | 보기: 대출이자 / 대출원리금 |
| `loan_product` | 대출상품명 | text | 100% | 아파트 담보대출 |
| `loan_account` | 납부자번호(대출계좌번호) | account_no | 100% | 740-757492-44-140 |
| `applicant.name` | 신청인 | text | 100% | 박찬연 |
| `applicant.birth` | 생년월일 | date | 100% | 1990-02-10 |
| `applicant.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `applicant.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `debit.bank` | 출금은행 | text | 100% | 기업은행 |
| `debit.account` | 출금계좌번호 | account_no | 100% | 171-760452-29-611 |
| `debit.holder` | 예금주 | text | 100% | 박찬연 |
| `debit.holder_birth` | 예금주생년월일 | number | 100% | 900210 |
| `debit.holder_phone` | 예금주휴대전화 | phone | 100% | 010-5907-7253 |
| `relation` | 신청인과예금주와의관계 | checkbox | 100% | 보기: 본인 / 가족 / 기타 |
| `transfer_day` | 출금일 | text | 100% | 매월 15일 |
| `start_month` | 이체개시 | text | 100% | 2026년 3월분부터 |
| `amount` | 출금금액 | text | 100% | 청구금액 전액 (약 1,211,320원) |
| `privacy_consent` | 개인정보수집이용동의 | checkbox | 100% | 보기: 동의함 / 동의하지 않음 |
| `third_party_consent` | 제3자제공동의 | checkbox | 100% | 보기: 동의함 / 동의하지 않음 |
| `apply_date` | 신청일 | date | 100% | 2026년 2월 3일 |
| `signature` | 신청인 | text | 100% | 박찬연 |
| `seal.applicant` | 신청인 | seal | 100% | 강순준 |
| `sign.applicant` | 신청인 | signature | 100% | 이욱유 |
| `holder_signature` | 예금주 | text | 100% | 박찬연 |
| `seal.holder` | 예금주 | seal | 100% | 이욱유 |
| `sign.holder` | 예금주 | signature | 100% | 박찬연 |
| `extra_loans[].loan_account` | 납부자번호 | account_no | 13% | 2451-245-638780 |
| `extra_loans[].loan_product` | 대출상품 | text | 13% | 전세자금대출 |
| `extra_loans[].target` | 이체대상 | text | 13% | 대출원리금 |
| `extra_loans[].transfer_day` | 출금일 | text | 13% | 매월 15일 |

## 고객확인서(개인) (`customer_due_diligence`) — 키 51개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank.name` | 은행명 | text | 100% | 기업은행 |
| `customer.name` | 성명(한글) | text | 100% | 존 밀러 |
| `customer.name_en` | 성명(영문) | text | 100% | KANG SOONJUN |
| `customer.rrn` | 실명번호 | rrn | 100% | 950627-5955869 |
| `customer.resident_type` | 구분 | checkbox | 100% | 보기: 내국인 / 재외국민 / 외국인 |
| `customer.gender` | 성별 | checkbox | 100% | 보기: 남 / 여 |
| `customer.nationality` | 국적 | text | 100% | 미국 |
| `customer.address` | 주소(거소) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `customer.mobile` | 휴대전화 | phone | 100% | 010-3055-5155 |
| `customer.email` | E-mail | text | 100% | john89@yahoo.com |
| `job.type` | 직업 | checkbox | 100% | 보기: 급여소득자 / 개인사업자 / 전문직 / 공무원 / 연금소득자 / 주부 / 학생 / 무직 / 기타 |
| `job.company` | 직장명 | text | 83% | 주식회사 태평양무역 |
| `job.department` | 부서/직위 | text | 70% | 구매팀 / 대리 |
| `job.industry` | 업종 | text | 83% | 도매 및 소매업 |
| `job.work_phone` | 직장전화 | phone | 83% | 043-783-2775 |
| `transaction.purpose` | 거래목적 | checkbox | 100% | 보기: 급여 및 생활비 / 저축 및 투자 / 보험료 납부결제 / 공과금 납부결제 / 카드대금 결제 / 대출원리금 상환결제 / 사업상 거래 / 기타 |
| `transaction.fund_source` | 자금의원천 | checkbox | 100% | 보기: 근로 및 연금소득 / 퇴직소득 / 사업소득 / 부동산임대소득 / 부동산양도소득 / 금융소득(이자 및 배당) / 상속·증여 / 일시 재산양도로 인한 소득 / 기타 |
| `transaction.expected_amount` | 예상거래금액 | checkbox | 100% | 보기: 1천만원 미만 / 1천만원~5천만원 / 5천만원~1억원 / 1억원 이상 |
| `transaction.frequency` | 예상거래빈도 | checkbox | 100% | 보기: 월 5회 미만 / 월 5~10회 / 월 10~20회 / 월 20회 이상 |
| `beneficial_owner` | 실제소유자여부 | checkbox | 100% | 보기: 예 / 아니오 |
| `pep` | 외국의정치적주요인물여부 | checkbox | 100% | 보기: 예 / 아니오 |
| `date` | 작성일 | date | 100% | 2026년 01월 31일 |
| `signature` | 고객성명 | text | 100% | MILLER JOHN |
| `seal.customer` | 고객 | seal | 100% | MILL |
| `sign.customer` | 고객 | signature | 100% | 강순준 |
| `bank_use.risk_grade` | 고객위험등급 | checkbox | 100% | 보기: 저위험 / 중위험 / 고위험 |
| `bank_use.id_type` | 실명확인증표 | checkbox | 100% | 보기: 주민등록증 / 운전면허증 / 여권 / 외국인등록증 / 모바일신분증 |
| `bank_use.branch` | 확인영업점 | text | 100% | 범어지점 |
| `seal.staff.clerk` | 담당 | seal | 100% | 김도서 |
| `bank_use.clerk` | 담당 | text | 100% | 김도서 |
| `seal.staff.manager` | 책임자 | seal | 100% | 강예경 |
| `bank_use.manager` | 책임자 | text | 100% | 강예경 |
| `agent.name` | 대리인성명 | text | 20% | 기희호 |
| `agent.rrn` | 대리인실명번호 | rrn | 20% | 700803-2****** |
| `agent.relation` | 본인과의관계 | text | 20% | 모 |
| `seal.agent` | 대리인 | seal | 20% | 김수연 |
| `sign.agent` | 대리인 | signature | 20% | 기희호 |
| `job.biz_no` | 사업자등록번호 | biz_no | 13% | 696-24-15367 |
| `job.opened` | 개업년월일 | date | 13% | 2016.10.11 |
| `edd.annual_income` | 연간소득 | text | 17% | 5,920만원 |
| `edd.assets` | 보유자산규모 | checkbox | 17% | 보기: 5억원 미만 / 5억원~10억원 / 10억원~30억원 / 30억원 이상 |
| `edd.fund_detail` | 자금원천상세 | text | 17% | 부모로부터 증여받은 자금 (증여세 신고서 제출) |
| `edd.purpose_detail` | 거래목적상세 | text | 17% | 주식·가상자산 투자자금 이체 |
| `edd.cash_tx` | 고액현금거래 | text | 17% | 월 1~2회 (1천만원 이상) |
| `edd.overseas_tx` | 해외거래 | text | 17% | 해당 없음 |
| `edd.accounts[].bank` | 금융회사 | text | 17% | 신한은행 |
| `edd.accounts[].kind` | 계좌종류 | text | 17% | 증권위탁 |
| `edd.accounts[].purpose` | 주된용도 | text | 17% | 생활비 |
| `owner.name` | 실제소유자성명 | text | 7% | 김서호 |
| `owner.birth` | 실제소유자생년월일 | date | 7% | 1980.11.12 |
| `owner.nationality` | 실제소유자국적 | text | 7% | 대한민국 |

## 고객확인서(법인·단체) (`corporate_customer_due_diligence`) — 키 44개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank.name` | 은행명 | text | 100% | 기업은행 |
| `corp.name` | 법인명(국문) | text | 100% | (주)유니온무역 |
| `corp.name_en` | 법인명(영문) | text | 100% | Union Trading Co., Ltd. |
| `corp.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `corp.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `corp.established` | 설립일 | date | 100% | 2018년 11월 01일 |
| `corp.industry` | 업종 | text | 100% | 도매 및 소매업 / 무역 |
| `corp.hq_address` | 본점주소 | text | 100% | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| `corp.biz_address` | 사업장주소 | text | 100% | 본점과 동일 |
| `corp.phone` | 대표전화 | phone | 100% | 02-9508-6789 |
| `corp.email` | 이메일 | text | 100% | admin@hanbit.co.kr |
| `corp.corp_type` | 법인구분 | checkbox | 100% | 보기: 대기업 / 중소기업 / 국가·지자체·공공단체 / 금융기관 / 비영리법인(단체) / 외국법인(단체) |
| `corp.listed` | 상장여부 | checkbox | 100% | 보기: 유가증권시장 / 코스닥 / 코넥스 / 비상장 |
| `rep.name` | 대표자성명 | text | 100% | 박찬연 |
| `rep.name_en` | 대표자영문성명 | text | 100% | KANG SOONJUN |
| `rep.birth` | 대표자생년월일 | date | 100% | 1990.02.10 |
| `rep.nationality` | 대표자국적 | text | 100% | 대한민국 |
| `transaction.purpose` | 거래목적 | checkbox | 100% | 보기: 사업상 거래(결제) / 운영자금 관리 / 급여 지급 / 대출 / 기타 |
| `transaction.fund_source` | 자금원천 | checkbox | 100% | 보기: 영업수익 / 자본금 / 차입금 / 투자수익 / 기타 |
| `owner_step` | 실제소유자확인단계 | checkbox | 100% | 보기: 1단계 / 2단계 / 3단계 |
| `owners[].name` | 성명 | text | 100% | 박찬연 |
| `owners[].birth` | 생년월일 | date | 100% | 1990.02.10 |
| `owners[].nationality` | 국적 | text | 100% | 대한민국 |
| `owners[].ratio` | 지분율 | percent | 100% | 74.04% |
| `owners[].relation` | 법인과의관계 | text | 100% | 대표이사 |
| `pep` | 외국의정치적주요인물여부 | checkbox | 100% | 보기: 예 / 아니오 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.corp` | 법인인감 | seal | 100% | 유니온무역대표이사인 |
| `bank_use.risk_grade` | 고객위험등급 | checkbox | 100% | 보기: 저위험 / 중위험 / 고위험 |
| `bank_use.documents[]` | 징구서류 | text | 100% | 사업자등록증 |
| `bank_use.branch` | 확인영업점 | text | 100% | 범어지점 |
| `seal.staff.clerk` | 담당 | seal | 100% | 변찬하 |
| `bank_use.clerk` | 담당 | text | 100% | 변찬하 |
| `seal.staff.manager` | 책임자 | seal | 100% | 이민재 |
| `bank_use.manager` | 책임자 | text | 100% | 이민재 |
| `bank_use.documents` | 징구서류 | checkbox_multi | 100% | 보기: 사업자등록증 / 법인등기사항전부증명서 / 주주명부 / 정관 / 법인인감증명서 |
| `shareholders[].name` | 주주명 | text | 33% | 현예지 |
| `shareholders[].birth` | 생년월일 | date | 33% | 1966.08.12 |
| `shareholders[].shares` | 소유주식수 | number | 33% | 22,821 |
| `shareholders[].ratio` | 지분율 | percent | 33% | 22.82% |
| `shareholders[].relation` | 법인과의관계 | text | 33% | 대표이사 |
| `agent.name` | 거래담당자성명 | text | 17% | 이채지 |
| `agent.rrn` | 거래담당자실명번호 | rrn | 17% | 981116-2****** |
| `agent.position` | 직위관계 | text | 17% | 재무팀 과장 |

## 개인(신용)정보 수집·이용·제공·조회 동의서 (`privacy_consent`) — 키 25개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank.name` | 은행명 | text | 100% | 기업은행 |
| `consent.collect` | 수집이용동의 | checkbox | 100% | 보기: 동의함 / 동의하지 않음 |
| `consent.unique_id` | 고유식별정보처리동의 | checkbox | 100% | 보기: 동의함 / 동의하지 않음 |
| `providers[].name` | 제공받는자 | text | 100% | 신용정보집중기관(한국신용정보원) |
| `providers[].purpose` | 제공받는자의이용목적 | text | 100% | 본인의 신용을 판단하기 위한 자료로 활용하거나 공공기관에서 정책자료로 활… |
| `providers[].items` | 제공하는항목 | text | 100% | 개인식별정보, 신용거래정보, 신용도판단정보, 신용능력정보, 공공정보 |
| `providers[].period` | 제공받는자의보유이용기간 | text | 100% | 관련 법령 및 규약에서 정한 기간 |
| `consent.provide` | 제공동의 | checkbox | 100% | 보기: 동의함 / 동의하지 않음 |
| `consent.provide_unique_id` | 고유식별정보제공동의 | checkbox | 100% | 보기: 동의함 / 동의하지 않음 |
| `consent.inquiry` | 조회동의 | checkbox | 100% | 보기: 동의함 / 동의하지 않음 |
| `marketing.collect` | 마케팅수집이용동의 | checkbox | 100% | 보기: 동의함 / 동의하지 않음 |
| `marketing.provide` | 마케팅제공동의 | checkbox | 100% | 보기: 동의함 / 동의하지 않음 |
| `marketing.channels[]` | 연락방법 | text | 47% | 전화 |
| `date` | 작성일 | date | 100% | 2026.01.31 |
| `applicant.birth` | 생년월일 | date | 100% | 1990년 02월 10일 |
| `applicant.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.applicant` | 본인 | seal | 90% | 박찬연 |
| `sign.applicant` | 본인 | signature | 90% | 강순준 |
| `seal.staff.clerk` | 본인확인 | seal | 100% | 이태경 |
| `bank_use.clerk` | 본인확인 | text | 100% | 이태경 |
| `marketing.channels` | 연락방법 | checkbox_multi | 100% | 보기: 전화 / 문자메시지 / 이메일 / 우편 / 앱 푸시 |
| `legal_rep.name` | 법정대리인 | text | 10% | 정수린 |
| `legal_rep.relation` | 본인과의관계 | text | 10% | 모 |
| `seal.legal_rep` | 법정대리인 | seal | 10% | 정수린 |
| `sign.legal_rep` | 법정대리인 | signature | 10% | 김나진 |

## 예금거래신청서 (`account_opening_application`) — 키 58개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank.name` | 은행명 | text | 100% | 기업은행 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.name_en` | 영문명 | text | 100% | PARK CHANYEON |
| `customer.rrn` | 실명번호 | rrn | 100% | 900210-1659382 |
| `customer.zipcode` | 우편번호 | number | 100% | 06931 |
| `customer.address` | 자택주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `customer.mobile` | 휴대폰 | phone | 100% | 010-5907-7253 |
| `customer.email` | 이메일 | text | 100% | chanyeon363@naver.com |
| `customer.job` | 직업 | text | 100% | 급여소득자 |
| `customer.company` | 직장명 | text | 77% | 주식회사 태평양무역 |
| `product.type` | 예금종류 | checkbox | 100% | 보기: 보통예금 / 저축예금 / 정기예금 / 정기적금 / 주택청약종합저축 |
| `product.name` | 상품명 | text | 100% | 정기예금(일반) |
| `product.amount` | 신규금액 | amount | 100% | 119,000,000원 |
| `product.term` | 계약기간 | text | 47% | 36개월 |
| `product.interest_payment` | 이자지급방법 | text | 10% | 만기일시지급 |
| `product.linked_account` | 출금계좌 | account_no | 47% | 171-760452-29-611 |
| `passbook` | 통장발행 | checkbox | 100% | 보기: 발행 / 미발행 |
| `seal_type` | 인감서명등록 | checkbox | 100% | 보기: 인감 / 서명 / 인감+서명 |
| `check_card` | 체크카드 | checkbox | 100% | 보기: 신청 / 미신청 |
| `ebank.internet` | 인터넷뱅킹 | checkbox | 100% | 보기: 신청 / 미신청 |
| `ebank.mobile` | 모바일뱅킹 | checkbox | 100% | 보기: 신청 / 미신청 |
| `ebank.otp` | 보안매체 | checkbox | 100% | 보기: OTP 발급 / 모바일OTP / 기존 OTP 사용 / 보안카드 / 미신청 |
| `ebank.limit_once` | 1회이체한도 | amount | 87% | 5,000,000원 |
| `ebank.limit_day` | 1일이체한도 | amount | 87% | 5,000,000원 |
| `alert` | 입출금알림 | checkbox | 100% | 보기: SMS / 앱 푸시 / 미신청 |
| `mail_to` | 우편물수령처 | checkbox | 100% | 보기: 자택 / 직장 / 이메일 / 수령 안함 |
| `salary_transfer` | 급여이체지정 | checkbox | 100% | 보기: 지정 / 미지정 |
| `protection_limit` | 예금자보호한도 | text | 93% | 1억원 |
| `signature` | 확인자 | text | 100% | 박찬연 |
| `date` | 신청일 | date | 100% | 2026년 1월 31일 |
| `seal.applicant` | 신청인 | seal | 100% | 이재주 |
| `sign.applicant` | 신청인 | signature | 100% | 박찬연 |
| `bank_use.account_no` | 계좌번호 | account_no | 100% | 956-619004-07-320 |
| `bank_use.branch` | 개설영업점 | text | 100% | 범어지점 |
| `bank_use.id_type` | 실명확인증표 | checkbox | 100% | 보기: 주민등록증 / 운전면허증 / 여권 / 외국인등록증 / 모바일신분증 |
| `seal.staff.clerk` | 담당 | seal | 100% | 위성준 |
| `bank_use.clerk` | 담당 | text | 100% | 위성준 |
| `seal.staff.manager` | 책임자 | seal | 100% | 반찬우 |
| `bank_use.manager` | 책임자 | text | 100% | 반찬우 |
| `legal_rep.name` | 법정대리인성명 | text | 17% | 이민빈 |
| `legal_rep.relation` | 본인과의관계 | text | 17% | 부 |
| `legal_rep.rrn` | 법정대리인실명번호 | rrn | 17% | 720524-1****** |
| `legal_rep.phone` | 법정대리인연락처 | phone | 17% | 010-6144-4077 |
| `legal_rep.documents` | 제출서류 | text | 17% | 가족관계증명서(상세), 법정대리인 신분증 |
| `seal.legal_rep` | 법정대리인 | seal | 17% | 옥영아 |
| `sign.legal_rep` | 법정대리인 | signature | 17% | 이민빈 |
| `agent.name` | 대리인성명 | text | 3% | 김준현 |
| `agent.relation` | 본인과의관계 | text | 3% | 부 |
| `agent.rrn` | 대리인실명번호 | rrn | 3% | 440309-1****** |
| `agent.phone` | 대리인연락처 | phone | 3% | 010-8700-9939 |
| `seal.agent` | 대리인 | seal | 3% |  |
| `sign.agent` | 대리인 | signature | 3% | 김준현 |
| `customer.nationality` | 국적 | text | 7% | 태국 |
| `extra_products[].type` | 예금종류 | text | 13% | 정기예금 |
| `extra_products[].name` | 상품명 | text | 13% | e-정기예금 |
| `extra_products[].amount` | 신규금액 | amount | 13% | 100,000원 |
| `extra_products[].term` | 계약기간 | text | 13% | 24개월 |
| `extra_products[].account_no` | 계좌번호 | account_no | 13% | 199-14-607140 |

## 금융거래목적확인서 (`financial_transaction_purpose`) — 키 23개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank.name` | 은행명 | text | 100% | 기업은행 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.rrn` | 실명번호 | rrn | 100% | 900210-1659382 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `customer.mobile` | 연락처 | phone | 100% | 010-5907-7253 |
| `customer.job` | 직업 | text | 100% | 개인사업자 |
| `customer.company` | 직장명 | text | 93% | 동방학원 |
| `account_type` | 신규예금종류 | checkbox | 100% | 보기: 보통예금 / 저축예금 / 기타 입출금예금 |
| `purpose` | 금융거래목적 | checkbox | 100% | 보기: 급여계좌 / 사업자 거래 / 공과금 이체 / 모임 회비 / 아르바이트 / 기타 |
| `evidence` | 제출증빙서류 | text | 100% | 사업자등록증명 |
| `questions.q1` | 통장양도대여요청여부 | checkbox | 100% | 보기: 예 / 아니오 |
| `questions.q2` | 취업대출빙자요청여부 | checkbox | 100% | 보기: 예 / 아니오 |
| `questions.q3` | 최근타행계좌개설여부 | checkbox | 100% | 보기: 예 / 아니오 |
| `date` | 작성일 | date | 100% | 2026년 01월 31일 |
| `signature` | 고객성명 | text | 100% | 박찬연 |
| `seal.customer` | 고객 | seal | 100% | 박찬연 |
| `sign.customer` | 고객 | signature | 100% | 현예지 |
| `bank_use.result` | 처리결과 | checkbox | 100% | 보기: 일반계좌 개설 / 금융거래한도계좌 개설 / 개설 거절 |
| `seal.staff.clerk` | 담당 | seal | 100% | 구호재 |
| `bank_use.clerk` | 담당 | text | 100% | 구호재 |
| `seal.staff.manager` | 책임자 | seal | 100% | 정연경 |
| `bank_use.manager` | 책임자 | text | 100% | 정연경 |
| `customer.nationality` | 국적 | text | 7% | 베트남 |

## 해외송금신청서 (`overseas_remittance_application`) — 키 52개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank.name` | 은행명 | text | 100% | 기업은행 |
| `remitter.name` | 송금인성명 | text | 100% | 박찬연 |
| `remitter.name_en` | 송금인영문명 | text | 100% | PARK CHANYEON |
| `remitter.rrn` | 실명번호 | rrn | 100% | 900210-1****** |
| `remitter.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `remitter.address` | 송금인주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `remitter.company` | 상호(사업자번호) | text | 57% | 동방학원 (860-11-55034) |
| `beneficiary.name` | 수취인성명 | text | 100% | Mekong Garment JSC |
| `beneficiary.address` | 수취인주소 | text | 100% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `beneficiary.country` | 수취인국가 | text | 100% | VIETNAM |
| `beneficiary.relationship` | 신청인과의관계 | text | 100% | 거래처 |
| `beneficiary.swift` | SWIFTBIC | text | 100% | BFTVVNVX |
| `beneficiary.bank_name` | 수취은행명 | text | 100% | Vietcombank |
| `beneficiary.bank_address` | 수취은행주소 | text | 100% | 198 Tran Quang Khai St, Hoan Kiem, Hanoi… |
| `beneficiary.account_no` | 수취인계좌번호 | account_no | 100% | 884779361534 |
| `remittance.currency` | 송금통화 | text | 100% | USD |
| `remittance.amount` | 송금금액 | amount | 100% | 73,190.66 |
| `remittance.purpose` | 송금사유 | checkbox | 100% | 보기: 수입대금 / 유학생경비 / 해외체재비 / 증여성송금 / 해외이주비 / 국내보수송금 / 기타 |
| `remittance.purpose_code` | 지급사유코드 | number | 77% | 10103 |
| `remittance.charge` | 수수료부담 | checkbox | 100% | 보기: OUR / SHA / BEN |
| `remittance.method` | 송금방법 | checkbox | 100% | 보기: 전신송금(T/T) / 송금수표(D/D) |
| `remittance.message` | 송금메시지 | text | 100% | INVOICE NO. MEK-2026-0068 |
| `remittance.documents` | 지급증빙서류 | text | 100% | Commercial Invoice, B/L 사본 |
| `date` | 신청일 | date | 100% | 2026.01.31 |
| `signature` | 신청인 | text | 100% | 박찬연 |
| `seal.applicant` | 신청인 | seal | 100% | 박찬연 |
| `sign.applicant` | 신청인 | signature | 100% | 강순준 |
| `bank_use.ref_no` | 참조번호 | text | 100% | OR26013115455 |
| `bank_use.branch` | 취급영업점 | text | 100% | 범어지점 |
| `bank_use.rate` | 적용환율 | number | 100% | 1,467.46 |
| `bank_use.krw_amount` | 원화환산액 | amount | 100% | 107,404,366원 |
| `bank_use.fee` | 송금수수료 | amount | 100% | 20,000원 |
| `bank_use.cable_fee` | 전신료 | amount | 100% | 8,000원 |
| `bank_use.total` | 합계 | amount | 100% | 107,432,366원 |
| `seal.staff.clerk` | 담당자 | seal | 100% | 박서주 |
| `bank_use.clerk` | 담당자 | text | 100% | 박서주 |
| `seal.staff.manager` | 결재권자 | seal | 100% | 주아주 |
| `bank_use.manager` | 결재권자 | text | 100% | 주아주 |
| `batch_count` | 송금건수 | text | 17% | 12건 |
| `batch[].beneficiary` | 수취인 | text | 17% | SAIGON TEXTILE JSC |
| `batch[].message` | 송금메시지 | text | 17% | INV 9657 |
| `batch[].country` | 국가 | text | 17% | VIETNAM |
| `batch[].bank` | 수취은행 | text | 17% | VIETCOMBANK HO CHI MINH (BFTVVNVX007) |
| `batch[].account_no` | 계좌번호 | account_no | 17% | 963900390920 |
| `batch[].currency` | 통화 | text | 17% | USD |
| `batch[].amount` | 금액 | amount | 17% | 9,455.88 |
| `agent.name` | 대리인성명 | text | 13% | 위민준 |
| `agent.relation` | 신청인과의관계 | text | 13% | 형제자매 |
| `agent.rrn` | 대리인실명번호 | rrn | 13% | 961009-1****** |
| `agent.phone` | 대리인연락처 | phone | 13% | 010-4083-8691 |
| `seal.agent` | 대리인 | seal | 13% | 위민준 |
| `sign.agent` | 대리인 | signature | 13% | 최경재 |

## 해외금융계좌 납세자 확인서(개인) (`fatca_crs`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank.name` | 은행명 | text | 100% | 기업은행 |
| `holder.name` | 성명(한글) | text | 100% | 박찬연 |
| `holder.surname_en` | 영문성 | text | 100% | PARK |
| `holder.given_en` | 영문이름 | text | 100% | CHANYEON |
| `holder.birth` | 생년월일 | date | 100% | 1990-02-10 |
| `holder.mobile` | 연락처 | phone | 100% | 010-3347-9183 |
| `holder.birth_place` | 출생국가 | text | 100% | 대한민국 (KOREA) |
| `holder.nationality` | 국적 | text | 100% | 대한민국 (KOREA) |
| `holder.address` | 현재거주지주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `residence_category` | 해외거주자여부 | text | 100% | 보기: 미국 시민권자(이중국적자 포함) / 미국 영주권자 / 미국 세법상 미국 거주자 / 미국 이외의 해외 거주자 / 해당사항 없음 |
| `residences[].country` | 거주관할권 | text | 17% | 미국 (U.S.A.) |
| `residences[].tin` | 납세자번호 | number | 10% | 387-79-8629 |
| `date` | 작성일 | date | 100% | 2026.01.31 |
| `signature` | 계좌보유자 | text | 100% | 박찬연 |
| `seal.holder` | 계좌보유자 | seal | 100% | 우지현 |
| `sign.holder` | 계좌보유자 | signature | 100% | 박찬연 |
| `bank_use.branch` | 접수영업점 | text | 100% | 범어지점 |
| `seal.staff.clerk` | 담당 | seal | 100% | 김숙희 |
| `bank_use.clerk` | 담당 | text | 100% | 김숙희 |
| `seal.staff.manager` | 책임자 | seal | 100% | 남궁환인 |
| `bank_use.manager` | 책임자 | text | 100% | 남궁환인 |
| `residences[].no_tin_reason` | 납세자번호미기재사유 | text | 7% | C |
