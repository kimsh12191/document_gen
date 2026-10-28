# 개인사업자 — 서류별 항목

키 규칙과 타입은 [README.md](README.md)에 있습니다.


## 사업자등록증 (`business_registration_certificate`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `kind` | 과세유형 | text | 100% | 일반과세자 |
| `biz_no` | 등록번호 | biz_no | 100% | 860-11-55034 |
| `trade_name` | 상호 | text | 100% | 동방학원 |
| `name` | 성명 | text | 100% | 박찬연 |
| `birth` | 생년월일 | date | 100% | 1990년 02월 10일 |
| `opened` | 개업연월일 | date | 100% | 2020년 03월 21일 |
| `address` | 사업장소재지 | text | 100% | 울산광역시 남구 대학로 14, 11층 (달동, 아이엠스퀘어) |
| `biz_type` | 업태 | text | 100% | 서비스업 |
| `biz_item` | 종목 | text | 100% | 학원 |
| `issue_reason` | 발급사유 | text | 100% | 정정(과세유형 전환) |
| `co_owner` | 공동사업자 | text | 100% | 김훈도 |
| `unit_taxation` | 사업자단위과세적용사업자여부 | text | 100% | 부 |
| `issue_date` | 발급일 | date | 100% | 2024년 07월 08일 |
| `issuer` | 발급기관 | text | 100% | 울산세무서장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 울산세무서장인 |
| `einvoice_email` | 전자세금계산서전용전자우편주소 | text | 33% | soonjun606@gmail.com |
| `sub_kinds[].biz_type` | 업태 | text | 13% | 음식점업 |
| `sub_kinds[].biz_item` | 종목 | text | 13% | 커피전문점 |

## 사업자등록증(법인사업자) (`business_registration_certificate_corp`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `biz_no` | 등록번호 | biz_no | 100% | 264-82-36559 |
| `corp_name` | 법인명(단체명) | text | 100% | (주)유니온무역 |
| `ceo` | 대표자 | text | 100% | 박찬연 |
| `opened` | 개업연월일 | date | 100% | 2018년 11월 01일 |
| `corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `address` | 사업장소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| `head_office` | 본점소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| `biz_type` | 업태 | text | 100% | 도매 및 소매업 |
| `biz_item` | 종목 | text | 100% | 무역 |
| `issue_reason` | 발급사유 | text | 100% | 재발급 |
| `unit_taxation` | 사업자단위과세적용사업자여부 | text | 100% | 부 |
| `issue_date` | 발급일 | date | 100% | 2021년 08월 03일 |
| `issuer` | 발급기관 | text | 100% | 중부세무서장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 중부세무서장인 |
| `einvoice_email` | 전자세금계산서전용전자우편주소 | text | 30% | contact@daesung.co.kr |
| `sub_kinds[].biz_type` | 업태 | text | 13% | 소매업 |
| `sub_kinds[].biz_item` | 종목 | text | 13% | 전자상거래 |
| `co_ceo` | 대표자 | text | 7% | 허석주 |

## 사업자등록증명 (`business_registration_proof`) — 키 23개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 5992-133-7220-660 |
| `trade_name` | 상호(법인명) | text | 100% | 동방학원 |
| `biz_no` | 사업자등록번호 | biz_no | 100% | 860-11-55034 |
| `name` | 성명(대표자) | text | 100% | 박찬연 |
| `rrn` | 주민(법인)등록번호 | rrn | 100% | 900210-1****** |
| `address` | 사업장소재지 | text | 100% | 울산광역시 남구 대학로 14, 11층 (달동, 아이엠스퀘어) |
| `opened` | 개업일 | date | 100% | 2020년 03월 21일 |
| `registered` | 사업자등록일 | date | 100% | 2020년 03월 17일 |
| `kind` | 과세유형 | text | 100% | 일반과세자 |
| `joint` | 공동사업자 | text | 100% | 해당없음 |
| `kinds[].biz_type` | 업태 | text | 100% | 서비스업 |
| `kinds[].biz_item` | 종목 | text | 100% | 학원 |
| `kinds[].code` | 업종코드 | number | 100% | 809009 |
| `kinds[].main` | 구분 | text | 100% | 주업종 |
| `purpose` | 사용목적 | text | 100% | 은행 제출 |
| `submit_to` | 제출처 | text | 100% | 기업은행 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 울산세무서장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 울산세무서장인 |
| `co_owners[].name` | 성명 | text | 3% | 김나진 |
| `co_owners[].rrn` | 주민등록번호 | rrn | 3% | 711009-2****** |
| `co_owners[].share` | 지분율 | percent | 3% | 60% |
| `co_owners[].role` | 구분 | text | 3% | 대표공동사업자 |

## 표준재무제표증명 (`standard_financial_statement_proof`) — 키 70개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 6888-572-1183-223 |
| `taxpayer_type` | 개인/법인 | checkbox | 100% | 보기: 개인 / 법인 |
| `taxpayer.trade_name` | 상호(법인명) | text | 100% | 동방학원 |
| `taxpayer.biz_no` | 사업자등록번호 | biz_no | 100% | 860-11-55034 |
| `taxpayer.name` | 성명(대표자) | text | 100% | 박찬연 |
| `taxpayer.rrn` | 주민(법인)등록번호 | rrn | 100% | 900210-1****** |
| `taxpayer.biz_type` | 업태 | text | 100% | 서비스업 |
| `taxpayer.biz_item` | 종목 | text | 100% | 학원 |
| `taxpayer.address` | 사업장 | text | 100% | 울산광역시 남구 대학로 14, 11층 (달동, 아이엠스퀘어) |
| `period` | 사업연도 | text | 100% | 2024-01-01 ~ 2024-12-31 |
| `filing_kind` | 신고구분 | text | 100% | 정기신고 |
| `attachments` | 첨부서류 | text | 100% | 표준재무상태표, 표준손익계산서 |
| `filed_date` | 신고일 | date | 100% | 2025-06-21 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 울산세무서장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 울산세무서장인 |
| `balance_sheet.current` | 유동자산 | amount | 100% | 200,632,487 |
| `balance_sheet.quick` | 당좌자산 | number | 100% | 190,196,447 |
| `balance_sheet.inventory` | 재고자산 | number | 100% | 10,436,040 |
| `balance_sheet.noncurrent` | 비유동자산 | amount | 100% | 158,229,375 |
| `balance_sheet.investment` | 투자자산 | number | 100% | 3,709,694 |
| `balance_sheet.tangible` | 유형자산 | number | 100% | 127,274,649 |
| `balance_sheet.intangible` | 무형자산 | number | 100% | 2,744,699 |
| `balance_sheet.other_noncurrent` | 기타비유동자산 | amount | 100% | 24,500,333 |
| `balance_sheet.assets` | 자산총계 | amount | 100% | 358,861,862 |
| `balance_sheet.current_liab` | 유동부채 | amount | 100% | 101,614,107 |
| `balance_sheet.noncurrent_liab` | 비유동부채 | amount | 100% | 153,194,870 |
| `balance_sheet.liabilities` | 부채총계 | amount | 100% | 254,808,977 |
| `balance_sheet.capital` | 자본금 | amount | 100% | 104,052,885 |
| `balance_sheet.equity` | 자본총계 | amount | 100% | 104,052,885 |
| `balance_sheet.liab_equity` | 부채와자본총계 | amount | 100% | 358,861,862 |
| `income_statement.revenue` | 매출액 | amount | 100% | 417,475,090 |
| `income_statement.cogs` | 매출원가 | number | 100% | 44,004,509 |
| `income_statement.gross` | 매출총이익 | number | 100% | 373,470,581 |
| `income_statement.sga` | 판매비와관리비 | number | 100% | 332,766,929 |
| `income_statement.salary` | 급여 | amount | 100% | 194,386,270 |
| `income_statement.welfare` | 복리후생비 | number | 100% | 23,326,350 |
| `income_statement.rent` | 임차료 | amount | 100% | 59,812,100 |
| `income_statement.depreciation` | 감가상각비 | number | 100% | 20,263,010 |
| `income_statement.other_sga` | 기타판매비와관리비 | number | 73% | 34,979,199 |
| `income_statement.op` | 영업이익 | number | 100% | 40,703,652 |
| `income_statement.non_op_income` | 영업외수익 | amount | 100% | 438,652 |
| `income_statement.non_op_expense` | 영업외비용 | amount | 100% | 2,883,032 |
| `income_statement.net` | 당기순이익 | number | 100% | 38,259,272 |
| `bs_accounts.quick[].account` | 계정과목 | text | 27% | 현금및현금성자산 |
| `bs_accounts.quick[].amount` | 금액 | amount | 27% | 65,982,923 |
| `bs_accounts.inventory[].account` | 계정과목 | text | 27% | 상품 |
| `bs_accounts.inventory[].amount` | 금액 | amount | 27% | 3,607,371 |
| `bs_accounts.investment[].account` | 계정과목 | text | 27% | 장기금융상품 |
| `bs_accounts.investment[].amount` | 금액 | amount | 27% | 6,757,583 |
| `bs_accounts.tangible[].account` | 계정과목 | text | 27% | 차량운반구 |
| `bs_accounts.tangible[].amount` | 금액 | amount | 27% | 59,911,859 |
| `bs_accounts.intangible[].account` | 계정과목 | text | 27% | 상표권 |
| `bs_accounts.intangible[].amount` | 금액 | amount | 27% | 10,397,329 |
| `bs_accounts.other_noncurrent[].account` | 계정과목 | text | 27% | 임차보증금 |
| `bs_accounts.other_noncurrent[].amount` | 금액 | amount | 27% | 19,734,714 |
| `bs_accounts.current_liab[].account` | 계정과목 | text | 27% | 매입채무 |
| `bs_accounts.current_liab[].amount` | 금액 | amount | 27% | 17,965,282 |
| `bs_accounts.noncurrent_liab[].account` | 계정과목 | text | 27% | 장기차입금 |
| `bs_accounts.noncurrent_liab[].amount` | 금액 | amount | 27% | 125,502,355 |
| `pl_accounts.revenue[].account` | 계정과목 | text | 27% | 용역매출 |
| `pl_accounts.revenue[].amount` | 금액 | amount | 27% | 335,244,390 |
| `pl_accounts.cogs[].account` | 계정과목 | text | 27% | 기초재고액 |
| `pl_accounts.cogs[].amount` | 금액 | amount | 27% | 12,295,718 |
| `pl_accounts.sga[].account` | 계정과목 | text | 27% | 퇴직급여 |
| `pl_accounts.sga[].amount` | 금액 | amount | 27% | 1,988,130 |
| `pl_accounts.non_op_income[].account` | 계정과목 | text | 27% | 이자수익 |
| `pl_accounts.non_op_income[].amount` | 금액 | amount | 27% | 584,199 |
| `pl_accounts.non_op_expense[].account` | 계정과목 | text | 27% | 이자비용 |
| `pl_accounts.non_op_expense[].amount` | 금액 | amount | 27% | 2,076,494 |
