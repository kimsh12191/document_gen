# 세금·보험 — 서류별 항목

키 규칙과 타입은 [README.md](README.md)에 있습니다.


## 납세증명서(국세완납증명) (`tax_payment_certificate`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 6377-316-8893-532 |
| `taxpayer.trade_name` | 상호(법인명) | text | 100% | 동방학원 |
| `taxpayer.biz_no` | 사업자등록번호 | biz_no | 100% | 860-11-55034 |
| `taxpayer.name` | 성명(대표자) | text | 100% | 박찬연 |
| `taxpayer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `taxpayer.address` | 주소(본점) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `valid_period` | 증명서유효기간 | text | 100% | 2026년 01월 31일 ~ 2026년 03월 01일 |
| `valid_reason` | 유효기간을정한사유 | text | 100% | 2024년 귀속 종합소득세 납부기한(2025년 5월 31일) 도래 |
| `purpose_type` | 사용목적 | checkbox | 100% | 보기: 대금 수령 / 해외이주 / 기타 |
| `purpose` | 사용목적 | text | 100% | 금융기관 제출용 |
| `payer` | 대금지급자 | amount | 100% | 서울특별시 |
| `deferral` | 연장ㆍ유예명세 | text | 90% | 해당없음 |
| `arrears` | 체납액 | text | 100% | 없음 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 서초세무서장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 서초세무서장인 |
| `deferrals[].kind` | 연장ㆍ유예종류 | text | 10% | 납부기한등 연장 |
| `deferrals[].period` | 연장ㆍ유예기간 | text | 10% | 2025.06.01 ~ 2026.03.01 |
| `deferrals[].tax_period` | 과세기간 | text | 10% | 2024년 귀속 |
| `deferrals[].tax_item` | 세목 | text | 10% | 종합소득세 |
| `deferrals[].due` | 납부기한 | date | 10% | 2025.05.31 |
| `deferrals[].amount` | 세액 | amount | 10% | 1,507,330 |

## 납세증명서(법인) (`tax_payment_certificate_corp`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 2207-657-1657-159 |
| `taxpayer.corp_name` | 상호(법인명) | text | 100% | (주)유니온무역 |
| `taxpayer.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `taxpayer.ceo` | 성명(대표자) | text | 100% | 박찬연 |
| `taxpayer.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `taxpayer.address` | 주소(본점) | text | 100% | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| `valid_period` | 증명서유효기간 | text | 100% | 2026년 01월 31일 ~ 2026년 03월 01일 |
| `valid_reason` | 유효기간을정한사유 | text | 100% | 2026사업연도 법인세 중간예납 납부기한(2026년 8월 31일) 도래 |
| `purpose_type` | 사용목적 | checkbox | 100% | 보기: 대금 수령 / 해외이주 / 기타 |
| `purpose` | 사용목적 | text | 100% | 금융기관 제출용 |
| `payer` | 대금지급자 | amount | 100% | 한국전력공사 |
| `deferral` | 연장ㆍ유예명세 | text | 100% | 해당없음 |
| `arrears` | 체납액 | text | 100% | 없음 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 중부세무서장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 중부세무서장인 |
| `deferrals[].kind` | 연장ㆍ유예종류 | text | 0% | 납부고지의 유예 |
| `deferrals[].period` | 연장ㆍ유예기간 | text | 0% | 2025.04.01 ~ 2025.09.30 |
| `deferrals[].tax_period` | 과세기간 | text | 0% | 2024.01.01 ~ 2024.12.31 |
| `deferrals[].tax_item` | 세목 | text | 0% | 법인세 |
| `deferrals[].due` | 납부기한 | date | 0% | 2025.03.31 |
| `deferrals[].amount` | 세액 | amount | 0% | 21,334,860 |

## 지방세 납세증명서 (`local_tax_payment_certificate`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 9572-3737-4206-7656 |
| `taxpayer.name` | 성명(법인명) | text | 100% | 박찬연 |
| `taxpayer.rrn` | 주민등록번호(법인등록번호) | rrn | 100% | 900210-1****** |
| `taxpayer.address` | 주소(영업소) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `purpose` | 증명서사용목적 | text | 100% | 금융기관 제출용 |
| `valid_period` | 증명서유효기간 | text | 100% | 2026년 01월 31일 ~ 2026년 03월 01일 |
| `deferrals[].tax_year` | 과세연도 | number | 3% | 2025 |
| `deferrals[].tax_item` | 세목 | text | 3% | 지방소득세 |
| `deferrals[].due` | 납부기한 | date | 3% | 2025.05.31 |
| `deferrals[].amount` | 세액 | amount | 3% | 2,199,610 |
| `deferrals[].period` | 유예기간 | text | 3% | 2025.11.22 ~ 2026.08.22 |
| `arrears` | 체납액 | text | 100% | 없음 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 서울특별시 서초구청장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 서초구청장인 |
| `deferral` | 징수유예등또는체납처분유예의내역 | text | 97% | 해당없음 |
| `taxpayer.trade_name` | 상호 | text | 30% | 한빛세무회계 |
| `taxpayer.biz_no` | 사업자등록번호 | biz_no | 30% | 696-24-15367 |

## 지방세 세목별 과세증명서 (`local_tax_assessment`) — 키 20개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 6934-2589-5434-0275 |
| `taxpayer.name` | 성명(법인명) | text | 100% | 박찬연 |
| `taxpayer.rrn` | 주민(법인,외국인)등록번호 | rrn | 100% | 900210-1659382 |
| `taxpayer.address` | 주소(영업소) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `period` | 과세연도 | text | 100% | 2024년 ~ 2025년 |
| `purpose` | 사용목적 | text | 100% | 은행 제출 |
| `items[].tax_item` | 세목 | text | 100% | 지방소득세 |
| `items[].levied` | 부과연월 | month | 100% | 2024.05 |
| `items[].kind` | 구분 | text | 100% | 확정신고 |
| `items[].object` | 과세대상 | text | 100% | 2023년 귀속 종합소득 |
| `items[].base` | 과세표준 | text | 100% | 60,297,716 |
| `items[].tax` | 세액 | amount | 100% | 864,140 |
| `items[].edu` | 지방교육세 | number | 100% | 0 |
| `items[].total` | 합계 | amount | 100% | 864,140 |
| `sum.tax` | 세액합계 | amount | 100% | 1,548,330 |
| `sum.edu` | 지방교육세합계 | number | 100% | 73,990 |
| `sum.total` | 총합계 | amount | 100% | 1,622,320 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 서울특별시 서초구청장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 서초구청장인 |

## 부가가치세 과세표준증명 (`vat_tax_base_certificate`) — 키 19개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 5373-520-1909-420 |
| `taxpayer.name` | 성명(대표자) | text | 100% | 박찬연 |
| `taxpayer.rrn` | 주민(법인)등록번호 | rrn | 100% | 900210-1****** |
| `taxpayer.trade_name` | 상호(법인명) | text | 100% | 동방학원 |
| `taxpayer.biz_no` | 사업자등록번호 | biz_no | 100% | 860-11-55034 |
| `taxpayer.address` | 사업장소재지 | text | 100% | 울산광역시 남구 대학로 14, 11층 (달동, 아이엠스퀘어) |
| `taxpayer.biz_type` | 업태 | text | 100% | 서비스업 |
| `taxpayer.biz_item` | 종목 | text | 100% | 학원 |
| `items[].period` | 과세기간 | text | 100% | 2024.01.01 ~ 2024.06.30 |
| `items[].kind` | 신고구분 | text | 100% | 정기확정 |
| `items[].filed` | 신고일 | date | 100% | 2024.07.13 |
| `items[].base_total` | 매출과세표준계 | amount | 100% | 307,114,710 |
| `items[].base_taxable` | 과세분 | amount | 100% | 15,015,130 |
| `items[].base_exempt` | 면세수입금액 | amount | 100% | 292,099,580 |
| `items[].tax` | 납부할세액(환급받을세액) | amount | 100% | 313,810 |
| `purpose` | 사용목적 | text | 100% | 대출 신청 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 울산세무서장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 울산세무서장인 |

## 종합소득세 과세표준확정신고 및 납부계산서 (`income_tax_return`) — 키 68개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `tax_year` | 귀속연도 | number | 100% | 2024 |
| `residency` | 거주구분 | checkbox | 100% | 보기: 거주자 / 비거주자 |
| `nationality` | 내ㆍ외국인 | checkbox | 100% | 보기: 내국인 / 외국인 |
| `taxpayer.name` | 성명 | text | 100% | 박찬연 |
| `taxpayer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `taxpayer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `taxpayer.email` | 전자우편주소 | text | 100% | chanyeon363@naver.com |
| `taxpayer.biz_phone` | 사업장전화번호 | phone | 100% | 052-956-0748 |
| `taxpayer.mobile` | 휴대전화번호 | phone | 100% | 010-5907-7253 |
| `filing_type` | 신고유형 | text | 100% | 성실신고확인 |
| `bookkeeping` | 기장의무 | text | 100% | 복식부기의무자 |
| `filing_kind` | 신고구분 | text | 100% | 정기신고 |
| `national.total_income` | 종합소득금액 | amount | 100% | 38,259,272 |
| `national.deduction` | 소득공제 | amount | 100% | 6,443,320 |
| `national.base` | 과세표준 | amount | 100% | 31,815,952 |
| `national.rate` | 세율 | percent | 100% | 15% |
| `national.computed` | 산출세액 | number | 100% | 3,512,392 |
| `national.reduction` | 세액감면 | number | 100% | 0 |
| `national.credit` | 세액공제 | amount | 100% | 90,000 |
| `national.determined` | 결정세액 | number | 100% | 3,422,392 |
| `national.penalty` | 가산세 | number | 100% | 0 |
| `national.additional` | 추가납부세액 | number | 100% | 0 |
| `national.total` | 합계 | amount | 100% | 3,422,392 |
| `national.prepaid` | 기납부세액 | number | 100% | 922,970 |
| `national.payable` | 납부(환급)할총세액 | amount | 100% | 2,499,420 |
| `national.special_deduct` | 납부특례세액차감 | number | 100% | 0 |
| `national.special_add` | 납부특례세액가산 | number | 100% | 0 |
| `national.installment` | 분납할세액 | number | 100% | 0 |
| `national.due_payable` | 신고기한이내납부할세액 | amount | 100% | 2,499,420 |
| `filed_date` | 신고일 | date | 100% | 2025년 06월 21일 |
| `seal.taxpayer` | 신고인 | seal | 100% | 이욱유 |
| `sign.taxpayer` | 신고인 | signature | 100% | 위나아 |
| `tax_agent.name` | 세무대리인 | text | 73% | 지선수 |
| `seal.tax_agent` | 세무대리인 | seal | 73% | 최원하 |
| `sign.tax_agent` | 세무대리인 | signature | 73% | 지선수 |
| `tax_agent.biz_no` | 세무대리인사업자등록번호 | biz_no | 73% | 388-36-49294 |
| `tax_agent.phone` | 세무대리인전화번호 | phone | 73% | 052-673-9329 |
| `tax_office` | 세무서장 | text | 100% | 서초세무서장 |
| `incomes[].type` | 소득구분 | text | 50% | 사업소득 |
| `incomes[].payer` | 소득의지급자 | text | 50% | 넥스트학원 |
| `incomes[].revenue` | 총수입금액 | amount | 50% | 390,549,770 |
| `incomes[].expense` | 필요경비 | amount | 50% | 347,059,995 |
| `incomes[].amount` | 소득금액 | amount | 50% | 43,489,775 |
| `incomes[].withheld` | 원천징수세액 | number | 50% | 0 |
| `business_income.address` | 사업장소재지 | text | 50% | 강원특별자치도 춘천시 공지로 647, 11층 03호 (효자동, 케이타워) |
| `business_income.trade_name` | 상호 | text | 50% | 넥스트학원 |
| `business_income.biz_no` | 사업자등록번호 | biz_no | 50% | 234-02-91864 |
| `business_income.code` | 업종코드 | number | 50% | 809009 |
| `business_income.revenue` | 총수입금액 | amount | 50% | 390,549,770 |
| `business_income.expense` | 필요경비 | amount | 50% | 347,059,995 |
| `business_income.income` | 소득금액 | amount | 50% | 43,489,775 |
| `dependents[].relation` | 관계 | text | 50% | 본인 |
| `dependents[].name` | 성명 | text | 50% | 강순준 |
| `dependents[].rrn` | 주민등록번호 | rrn | 50% | 970514-2150000 |
| `dependents[].basic` | 기본공제 | text | 50% | ○ |
| `dependents[].extra` | 추가공제 | text | 50% | 경로우대 |
| `deduction_items[].item` | 소득공제항목 | text | 50% | 기본공제 |
| `deduction_items[].amount` | 금액 | amount | 50% | 1,500,000 |
| `credit_items[].item` | 세액공제항목 | text | 50% | 표준세액공제 |
| `credit_items[].amount` | 금액 | amount | 50% | 70,000 |
| `refund_account.bank` | 금융기관/체신관서명 | text | 43% | 기업은행 |
| `refund_account.number` | 계좌번호 | text | 43% | 941-473791-23-142 |
| `prepaid_items[].item` | 기납부세액항목 | text | 47% | 중간예납세액 |
| `prepaid_items[].amount` | 금액 | amount | 47% | 2,291,860 |
| `penalty_items[].item` | 가산세항목 | text | 3% | 무신고가산세 |
| `penalty_items[].amount` | 금액 | amount | 3% | 681,530 |
| `business_income.partner` | 공동사업자 | text | 3% | 김훈도 |
| `business_income.share` | 손익분배비율 | percent | 3% | 60% |
