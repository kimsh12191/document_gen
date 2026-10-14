# 금융거래 — 서류별 항목

키 규칙과 타입은 [README.md](README.md)에 있습니다.


## 통장사본 (`bankbook_copy`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank` | 은행명 | text | 100% | 기업은행 |
| `product` | 상품명 | text | 100% | 저축예금 |
| `seal.registered` | 등록인감 | seal | 53% | 박찬연 |
| `passbook_no` | 통장번호 | number | 53% | 03 |
| `account_no` | 계좌번호 | account_no | 100% | 171-760452-29-611 |
| `holder` | 예금주 | text | 100% | 박찬연 |
| `opened` | 신규일 | date | 100% | 2014.06.11 |
| `branch` | 지점명 | text | 100% | 여의도지점 |
| `branch_phone` | 지점전화번호 | phone | 100% | 02-3937-0125 |
| `first_tx.date` | 거래일 | date | 53% | 2014.06.11 |
| `first_tx.memo` | 적요 | text | 53% | 신규 |
| `first_tx.amount` | 맡기신금액 | amount | 53% | 50,000 |
| `first_tx.balance` | 잔액 | amount | 53% | 50,000 |
| `txs[].date` | 거래일 | date | 20% | 2014.06.25 |
| `txs[].memo` | 적요 | text | 20% | 모바일출금 |
| `txs[].out` | 찾으신금액 | number | 20% | 40,000 |
| `txs[].balance` | 잔액 | amount | 20% | 10,000 |
| `status` | 계좌상태 | text | 10% | 해지 |
| `closed_date` | 해지일 | date | 10% | 2014.08.01 |
| `issue_date` | 출력일 | date | 47% | 2025.05.19 |
| `txs[].in` | 맡기신금액 | number | 17% | 2,151,600 |
| `limit_note` | 계좌제한구분 | text | 3% | 금융거래한도계좌 |

## 거래내역확인서 (`bank_statement`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 20260131-215660 |
| `holder` | 예금주 | text | 100% | 박찬연 |
| `birth` | 생년월일 | date | 100% | 1990.02.10 |
| `account_no` | 계좌번호 | account_no | 100% | 171-760452-29-611 |
| `product` | 상품명 | text | 100% | 저축예금 |
| `period` | 조회기간 | text | 100% | 2025.10.29 ~ 2026.01.30 |
| `opening_balance` | 조회기간전잔액 | amount | 100% | 52,145,840 |
| `rows[].datetime` | 거래일시 | datetime | 100% | 2025.11.15 10:54:57 |
| `rows[].type` | 적요 | text | 100% | 자동이체 |
| `rows[].memo` | 기재내용 | text | 100% | 현대카드 |
| `rows[].out` | 찾으신금액 | number | 100% | 1,381,960 |
| `rows[].balance` | 거래후잔액 | amount | 100% | 50,763,880 |
| `rows[].in` | 맡기신금액 | number | 100% | 3,847,280 |
| `summary.count` | 거래건수 | text | 100% | 12건 |
| `summary.out` | 찾으신금액합계 | number | 100% | 4,511,960 |
| `summary.in` | 맡기신금액합계 | number | 100% | 12,380,699 |
| `summary.balance` | 최종잔액 | amount | 100% | 60,014,579 |
| `issue_date` | 발급일 | date | 100% | 2026.01.31 |
| `issuer` | 발급점 | text | 100% | 기업은행 범어지점 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 범어지점장인 |
| `overdraft_limit` | 대출한도 | amount | 7% | 30,000,000 |

## 잔액증명서 (`balance_certificate`) — 키 20개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `cert_no` | 증명서번호 | text | 100% | 제 2026-58458 호 |
| `holder.name` | 예금주 | text | 100% | 박찬연 |
| `holder.rrn` | 고객번호(주민등록번호) | rrn | 100% | 900210-1****** |
| `base_date` | 기준일 | text | 100% | 2026년 01월 30일 현재 |
| `rows[].kind` | 과목 | text | 100% | 보통예금 |
| `rows[].account_no` | 계좌번호 | account_no | 100% | 171-760452-29-611 |
| `rows[].balance` | 예금잔액 | amount | 100% | 60,014,579 |
| `rows[].uncleared` | 미결제타점권 | number | 100% | 0 |
| `rows[].pledge` | 질권 | text | 100% | 무 |
| `rows[].restriction` | 지급정지·압류·가압류 | text | 100% | 무 |
| `currency` | 통화 | text | 100% | KRW |
| `total` | 합계 | amount | 100% | 62,714,579 |
| `total_korean` | 합계금액(한글) | amount_korean | 100% | 금 육천이백칠십일만사천오백칠십구원정 |
| `purpose` | 용도 | text | 100% | 입찰 참가용 |
| `issue_date` | 발급일 | date | 100% | 2026년 1월 31일 |
| `issuer` | 발급점 | text | 100% | 기업은행 범어지점장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 범어지점장인 |
| `remarks[]` | 비고 | text | 23% | 계좌번호 093-105-808241 : 질권설정 (질권자 : 서울보증보험… |
| `rows[].fx_amount` | 외화잔액 | amount | 3% | EUR 2,307.87 |
| `fx_rate` | 매매기준율 | amount | 3% | EUR 1,589.39 |

## 부채증명서 (`debt_certificate`) — 키 23개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `cert_no` | 증명서번호 | text | 100% | 제 2026-75909 호 |
| `borrower.name` | 차주명 | text | 100% | 박찬연 |
| `borrower.rrn` | 주민등록번호 | rrn | 100% | 900210-1****** |
| `borrower.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `base_date` | 기준일 | text | 100% | 2026년 01월 30일 현재 |
| `loans[].subject` | 대출과목 | text | 100% | 주택담보대출 |
| `loans[].account_no` | 계좌번호 | account_no | 100% | 913-249880-40-481 |
| `loans[].loan_date` | 대출일 | date | 100% | 2024.08.11 |
| `loans[].maturity` | 만기일 | date | 100% | 2054.08.11 |
| `loans[].amount` | 대출금액 | amount | 100% | 310,000,000 |
| `loans[].balance` | 대출잔액 | amount | 100% | 301,889,215 |
| `loans[].rate` | 금리 | text | 100% | 3.77% |
| `total_amount` | 대출금액합계 | amount | 100% | 320,000,000 |
| `total_balance` | 대출잔액합계 | amount | 100% | 303,430,084 |
| `total_korean` | 대출잔액합계(한글) | amount_korean | 100% | 금 삼억삼백사십삼만팔십사원정 |
| `guarantee` | 보증채무 | checkbox | 100% | 보기: 있음 / 없음 |
| `overdue` | 연체여부 | text | 100% | 없음 |
| `purpose` | 용도 | text | 100% | 법원 제출용 |
| `issue_date` | 발급일 | date | 100% | 2026년 1월 31일 |
| `issuer` | 발급점 | text | 100% | 기업은행 범어지점장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 범어지점장인 |
| `guarantee_detail` | 보증내역 | text | 20% | 채욱정 차주 전세자금대출 연대보증 10,000,000원 |
| `overdue_detail` | 연체내역 | text | 10% | 개인사업자대출(472-84-246131) 연체 47일, 연체원리금 2,0… |

## 신용카드 이용대금명세서 (`card_statement`) — 키 30개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company` | 카드사 | text | 100% | NH농협카드 |
| `statement_month` | 청구월 | month | 100% | 2026년 1월 |
| `member` | 회원명 | text | 100% | 박찬연 |
| `card_no` | 카드번호 | text | 100% | 5186-69**-****-6103 |
| `pay_date` | 결제일 | date | 100% | 2026.01.15 |
| `pay_account` | 결제계좌 | account_no | 100% | 기업은행 171-760***-*9-611 |
| `usage_period` | 이용기간 | text | 100% | 2025.12.01 ~ 2025.12.31 |
| `summary.total` | 청구금액 | amount | 100% | 1,315,504 |
| `summary.lump` | 일시불 | number | 100% | 658,240 |
| `summary.installment` | 할부 | number | 100% | 636,634 |
| `summary.cash` | 현금서비스 | amount | 100% | 0 |
| `summary.fee` | 수수료(이자) | amount | 100% | 20,630 |
| `summary.next_month` | 다음달결제예정금액 | number | 100% | 239,666 |
| `summary.limit` | 이용한도 | amount | 100% | 8,000,000 |
| `rows[].date` | 이용일자 | date | 100% | 2025.10.22 |
| `rows[].merchant` | 이용하신가맹점 | text | 100% | 신세계백화점 |
| `rows[].amount` | 이용금액 | amount | 100% | 1,190,900 |
| `rows[].months` | 할부 | text | 100% | 3개월 |
| `rows[].seq` | 회차 | text | 100% | 3/3 |
| `rows[].principal` | 원금 | amount | 100% | 396,968 |
| `rows[].fee` | 수수료(이자) | amount | 100% | 4,460 |
| `rows[].after` | 결제후잔액 | number | 100% | 0 |
| `sum.amount` | 이용금액합계 | amount | 100% | 3,287,140 |
| `sum.principal` | 결제원금합계 | amount | 100% | 1,294,874 |
| `sum.fee` | 수수료합계 | amount | 100% | 20,630 |
| `fee_rate` | 할부수수료율 | percent | 100% | 연 13.5% |
| `fee_per_100[].months` | 할부개월 | text | 100% | 2개월 |
| `fee_per_100[].fee` | 100원당수수료 | amount | 100% | 1.69원 |
| `summary.overdue` | 연체금액 | number | 10% | 597,080 |
| `summary.overdue_fee` | 연체이자 | amount | 10% | 6,290 |
