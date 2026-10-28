# 소득·재직 — 서류별 항목

키 규칙과 타입은 [README.md](README.md)에 있습니다.


## 재직증명서 (`employment_certificate`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `doc_no` | 문서번호 | text | 100% | 제 2026-145 호 |
| `employee.name` | 성명 | text | 100% | 박찬연 |
| `employee.rrn` | 주민등록번호 | rrn | 77% | 900210-1659382 |
| `employee.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `company.name` | 회사명 | text | 100% | 주식회사 태평양무역 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 501-82-42625 |
| `company.address` | 소재지 | text | 100% | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 |
| `employment.department` | 소속 | text | 100% | 구매팀 |
| `employment.position` | 직위 | text | 100% | 대리 |
| `employment.period` | 재직기간 | text | 100% | 2020.05.08 ~ 현재 |
| `employment.duty` | 담당업무 | text | 100% | 자재 구매 및 협력사 관리 |
| `purpose` | 용도 | text | 100% | 금융기관 제출용 |
| `submit_to` | 제출처 | text | 100% | 기업은행 |
| `issue_date` | 발급일 | date | 100% | 2026년 1월 31일 |
| `company.phone` | 전화번호 | phone | 100% | 043-783-2775 |
| `company.ceo` | 대표이사 | text | 100% | 공정태 |
| `seal.company` | 회사직인 | seal | 100% | 대표이사인 |
| `employee.birth` | 생년월일 | date | 23% | 1994.09.26 |
| `employment.employment_type` | 고용형태 | text | 10% | 계약직(기간제) |
| `employment.contract_period` | 계약기간 | text | 10% | 2026.05.27 ~ 2027.05.26 |
| `employment.leave` | 휴직기간 | text | 3% | 2013.04.01 ~ 2013.09.30 (육아휴직) |
| `employment.annual_salary` | 급여(연봉) | amount | 0% | 54,600,000원 |

## 경력증명서 (`career_certificate`) — 키 20개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `doc_no` | 문서번호 | text | 100% | 제 2026-837 호 |
| `person.name` | 성명 | text | 100% | 박찬연 |
| `person.rrn` | 주민등록번호 | rrn | 100% | 900210-1****** |
| `person.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `person.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `hire_date` | 입사일 | date | 100% | 2020년 05월 08일 |
| `careers[].period` | 근무기간 | text | 100% | 2020년 05월 08일 ~ 2021년 12월 31일 |
| `careers[].department` | 근무부서 | text | 100% | 구매팀 |
| `careers[].position` | 직위 | text | 100% | 사원 |
| `careers[].duty` | 담당업무 | text | 100% | 자재 구매 및 협력사 관리 |
| `total_period` | 총근무기간 | text | 100% | 5년 8개월 |
| `purpose` | 용도 | text | 100% | 대출 신청용 |
| `submit_to` | 제출처 | text | 100% | 기업은행 |
| `issue_date` | 발급일 | date | 100% | 2026년 1월 31일 |
| `company.name` | 회사명 | text | 100% | 주식회사 태평양무역 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 501-82-42625 |
| `company.address` | 소재지 | text | 100% | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 |
| `company.phone` | 전화번호 | phone | 100% | 043-783-2775 |
| `company.ceo` | 대표이사 | text | 100% | 공정태 |
| `seal.company` | 회사직인 | seal | 100% | 대표이사인 |

## 급여명세서 (`pay_stub`) — 키 28개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `doc_title` | 서식명 | text | 100% | 급여명세서 |
| `title_month` | 귀속연월 | text | 100% | 2026년 01월분 |
| `company` | 회사명 | text | 100% | 주식회사 태평양무역 |
| `pay_date` | 지급일 | date | 100% | 2026-01-25 |
| `employee.name` | 성명 | text | 100% | 박찬연 |
| `employee.birth` | 생년월일 | date | 100% | 1990-02-10 |
| `employee.employee_no` | 사번 | text | 100% | B88222 |
| `employee.department` | 부서 | text | 100% | 구매팀 |
| `employee.position` | 직급 | text | 100% | 대리 |
| `payments[].name` | 임금항목 | text | 100% | 기본급 |
| `payments[].amount` | 지급금액 | amount | 100% | 4,350,000 |
| `deductions[].name` | 공제항목 | text | 100% | 국민연금 |
| `deductions[].amount` | 공제금액 | amount | 100% | 206,620 |
| `pay_total` | 지급액계 | amount | 100% | 5,174,390 |
| `deduction_total` | 공제액계 | amount | 100% | 807,590 |
| `net_pay` | 실수령액 | amount | 100% | 4,366,800 |
| `work.days` | 근로일수 | number | 100% | 22 |
| `work.hours` | 총근로시간수 | number | 100% | 196 |
| `work.overtime_hours` | 연장근로시간수 | number | 100% | 20 |
| `work.night_hours` | 야간근로시간수 | number | 100% | 0 |
| `work.holiday_hours` | 휴일근로시간수 | number | 100% | 0 |
| `work.hourly_wage` | 통상시급(원) | amount | 100% | 20,813 |
| `work.family` | 가족수 | text | 100% | - |
| `calc_methods[].item` | 구분 | text | 100% | 연장근로수당 |
| `calc_methods[].method` | 산출식또는산출방법 | text | 100% | 20시간 × 20,813원 × 1.5 |
| `calc_methods[].amount` | 금액(원) | amount | 100% | 624,390 |
| `payments_irregular[].name` | 임금항목 | text | 33% | 명절상여금 |
| `payments_irregular[].amount` | 지급금액 | amount | 33% | 1,570,830 |

## 근로계약서 (`employment_contract`) — 키 31개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `employer.name` | 사업주 | text | 100% | 주식회사 태평양무역 |
| `employee.name` | 근로자 | text | 100% | 박찬연 |
| `start_date` | 근로개시일 | date | 100% | 2020년 5월 8일 |
| `workplace` | 근무장소 | text | 100% | 주식회사 태평양무역 본사 |
| `job` | 업무의내용 | text | 100% | 구매팀 자재 구매 및 협력사 관리 |
| `work_start` | 소정근로시간 | text | 100% | 09시 00분 |
| `work_end` | 소정근로시간 | text | 100% | 18시 00분 |
| `break_time` | 휴게시간 | text | 100% | 12시 00분 ~ 13시 00분 |
| `work_days` | 근무일 | number | 100% | 5 |
| `weekly_holiday` | 주휴일 | text | 100% | 일 |
| `monthly_salary` | 월(일,시간)급 | amount | 100% | 3,700,000 |
| `bonus` | 상여금 | text | 100% | 있음 |
| `bonus_amount` | 상여금 | amount | 60% | 3,500,000 |
| `other_pay` | 기타급여 | text | 100% | 있음 |
| `allowances[].name` | 기타급여(제수당등) | text | 100% | 식대 |
| `allowances[].amount` | 기타급여(제수당등) | amount | 100% | 200,000원 |
| `pay_day` | 임금지급일 | amount | 100% | 25 |
| `pay_method` | 지급방법 | text | 100% | 근로자 명의 예금통장에 입금 |
| `special_terms[]` | 특약사항 | text | 47% | 회사가 지급한 노트북 등 업무용 장비는 퇴직 시 즉시 반납한다. |
| `contract_date` | 계약일 | date | 100% | 2020년 5월 7일 |
| `employer.phone` | 전화 | phone | 100% | 043-783-2775 |
| `employer.address` | 주소 | text | 100% | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 |
| `employer.ceo` | 대표자 | text | 100% | 공정태 |
| `seal.employer` | 사용자 | seal | 100% | 대표이사인 |
| `employee.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `employee.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `seal.employee` | 근로자 | seal | 100% | 박찬연 |
| `sign.employee` | 근로자 | signature | 100% | 현예지 |
| `end_date` | 근로계약종료일 | date | 10% | 2020년 05월 27일 |
| `probation.period` | 수습기간 | text | 20% | 2014년 12월 01일 ~ 2015년 02월 28일 (3개월) |
| `probation.wage_rate` | 수습기간임금지급률 | percent | 20% | 100% |

## 근로소득 원천징수영수증 (`withholding_receipt`) — 키 48개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `copy_type` | 보관용구분 | checkbox | 100% | 보기: 소득자 보관용 / 발행자 보관용 / 발행자 보고용 |
| `year` | 귀속연도 | number | 100% | 2024 |
| `resident` | 거주구분 | checkbox | 100% | 보기: 거주자1 / 비거주자2 |
| `nationality` | 내·외국인 | checkbox | 100% | 보기: 내국인1 / 외국인9 |
| `household_head` | 세대주여부 | checkbox | 100% | 보기: 세대주1 / 세대원2 |
| `settlement_type` | 연말정산구분 | checkbox | 100% | 보기: 계속근로1 / 중도퇴사2 |
| `payer.name` | 법인명(상호) | text | 100% | 주식회사 태평양무역 |
| `payer.ceo` | 대표자(성명) | text | 100% | 공정태 |
| `payer.biz_no` | 사업자등록번호 | biz_no | 100% | 501-82-42625 |
| `payer.address` | 소재지(주소) | text | 100% | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 |
| `earner.name` | 성명 | text | 100% | 박찬연 |
| `earner.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `earner.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `work.company` | 근무처명 | text | 100% | 주식회사 태평양무역 |
| `work.biz_no` | 사업자등록번호 | biz_no | 100% | 501-82-42625 |
| `work.period` | 근무기간 | text | 100% | 2024.01.01~2024.12.31 |
| `work.salary` | 급여 | amount | 100% | 40,800,000 |
| `work.bonus` | 상여 | amount | 100% | 7,770,000 |
| `work.total` | 계 | amount | 100% | 48,570,000 |
| `nontax.meal` | 식사대 | number | 100% | 2,400,000 |
| `nontax.total` | 비과세소득계 | amount | 100% | 2,400,000 |
| `tax.final_income` | 결정세액 | amount | 100% | 2,257,830 |
| `tax.final_local` | 결정세액 | number | 100% | 225,780 |
| `tax.prepaid_income` | 주(현)근무지 | amount | 100% | 2,628,600 |
| `tax.prepaid_local` | 주(현)근무지 | number | 100% | 262,860 |
| `tax.diff_income` | 차감징수세액 | amount | 100% | -370,770 |
| `tax.diff_local` | 차감징수세액 | number | 100% | -37,080 |
| `tax.effective_rate` | 실효세율(%) | number | 100% | 4.6 |
| `issue_date` | 발급일 | date | 100% | 2025년 02월 28일 |
| `seal.payer` | 징수의무자 | seal | 100% | 대표이사인 |
| `tax_office` | 세무서장 | text | 100% | 청주세무서장 |
| `work_prev.company` | 종(전)근무처명 | text | 27% | 주식회사 코리아파트너스 |
| `work_prev.biz_no` | 종(전)사업자등록번호 | biz_no | 27% | 558-18-39130 |
| `work_prev.period` | 종(전)근무기간 | text | 27% | 2023.03.01~2023.05.31 |
| `work.reduction_period` | 감면기간 | text | 13% | 2019.02.22~2024.02.21 |
| `work_prev.salary` | 종(전)급여 | amount | 27% | 2,920,000 |
| `work_sum.salary` | 급여합계 | amount | 27% | 40,190,000 |
| `work_prev.bonus` | 종(전)상여 | amount | 27% | 0 |
| `work_sum.bonus` | 상여합계 | amount | 27% | 0 |
| `work_prev.total` | 종(전)계 | amount | 27% | 2,920,000 |
| `work_sum.total` | 계합계 | amount | 27% | 40,190,000 |
| `work_sum.meal` | 식사대합계 | number | 27% | 2,400,000 |
| `nontax.reduction` | 감면소득계 | number | 13% | 37,270,000 |
| `tax_prev.biz_no` | 종(전)근무지사업자등록번호 | biz_no | 27% | 558-18-39130 |
| `tax_prev.income` | 종(전)근무지기납부소득세 | amount | 27% | 0 |
| `tax_prev.local` | 종(전)근무지기납부지방소득세 | number | 27% | 0 |
| `work_prev.meal` | 종(전)식사대 | number | 3% | 1,000,000 |
| `nontax.childcare` | 출산·보육수당 | number | 3% | 2,400,000 |

## 소득금액증명원 (`income_certificate`) — 키 20개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 2145-532-2462-517 |
| `taxpayer.name` | 성명(대표자) | text | 100% | 박찬연 |
| `taxpayer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `taxpayer.address` | 주소(사업장소재지) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `period` | 증명기간 | text | 100% | 2024년 |
| `rows[].year` | 귀속연도 | number | 100% | 2024 |
| `rows[].income_type` | 소득구분 | text | 100% | 근로 |
| `rows[].payer` | 법인명(상호) | text | 100% | 주식회사 태평양무역 |
| `rows[].payer_biz_no` | 사업자등록번호 | biz_no | 100% | 501-82-42625 |
| `rows[].amount` | 소득금액(과세대상급여액) | amount | 100% | 48,570,000 |
| `rows[].tax` | 총결정세액 | amount | 100% | 2,257,830 |
| `purpose` | 용도 | text | 100% | 은행 제출용 |
| `submit_to` | 제출처 | text | 100% | 기업은행 |
| `issue_date` | 발급일 | date | 100% | 2026년 1월 31일 |
| `issuer` | 발급기관 | text | 100% | 서초세무서장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 서초세무서장인 |
| `filing_rows[].year` | 귀속연도 | number | 23% | 2024 |
| `filing_rows[].income_type` | 소득구분 | text | 23% | 근로 |
| `filing_rows[].revenue` | 수입금액 | amount | 23% | 46,390,000 |
| `filing_rows[].income` | 소득금액 | amount | 23% | 34,320,500 |

## 국민연금 가입자 가입증명 (`pension_enrollment_certificate`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 20260131-21521346 |
| `issue_date_head` | 발급일자 | date | 100% | 2026.01.31 |
| `person.name` | 성명 | text | 100% | 박찬연 |
| `person.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `first_acquired` | 최초자격취득일 | date | 100% | 2018.03.15 |
| `total_months` | 가입기간합계 | text | 100% | 88개월 |
| `rows[].kind` | 가입자종류 | text | 100% | 사업장가입자 |
| `rows[].workplace` | 사업장명칭 | text | 100% | (주)우진오토텍 |
| `rows[].start` | 자격취득일 | date | 100% | 2018.03.15 |
| `rows[].end` | 자격상실일 | date | 73% | 2019.11.15 |
| `rows[].wage` | 기준소득월액 | amount | 100% | 2,079,000 |
| `rows[].note` | 비고 | text | 17% | 납부예외(실직) |
| `purpose` | 용도 | text | 100% | 은행 제출용 |
| `issue_date` | 발급일 | date | 100% | 2026년 1월 31일 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 국민연금공단이사장 |

## 건강보험 자격득실확인서 (`health_insurance_qualification`) — 키 10개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 3829-2859-3487-6640 |
| `person.name` | 성명 | text | 100% | 박찬연 |
| `person.rrn` | 주민등록번호 | rrn | 100% | 900210-1****** |
| `rows[].kind` | 가입자구분 | text | 100% | 직장피부양자 |
| `rows[].start` | 자격취득일 | date | 100% | 1990.02.10 |
| `rows[].end` | 자격상실일 | date | 100% | 2018.03.15 |
| `rows[].workplace` | 사업장명칭 | text | 100% | (주)우진오토텍 |
| `purpose` | 용도 | text | 100% | 기타 제출용 |
| `issue_date` | 발급일 | date | 100% | 2026년 1월 31일 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 국민건강보험공단이사장인 |

## 건강보험료 납부확인서 (`health_insurance_payment`) — 키 26개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 85-651171-2643 |
| `person.name` | 성명 | text | 100% | 박찬연 |
| `person.birth` | 생년월일 | date | 63% | 1990.02.10 |
| `person.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `member_kind` | 가입자구분 | text | 100% | 직장가입자 |
| `period` | 대상기간 | text | 100% | 2023.08 ~ 2025.12 |
| `workplace.name` | 사업장명칭 | text | 100% | 주식회사 태평양무역 |
| `workplace.mgmt_no` | 사업장관리번호 | number | 100% | 50182426250 |
| `workplace.address` | 소재지 | text | 100% | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 |
| `rows[].month` | 년월 | month | 100% | 2023.08 |
| `rows[].notice_health` | 고지보험료(건강보험) | number | 100% | 138,400 |
| `rows[].notice_ltc` | 고지보험료(장기요양) | number | 100% | 17,720 |
| `rows[].health` | 납부보험료(건강보험) | number | 100% | 138,400 |
| `rows[].ltc` | 납부보험료(장기요양) | number | 100% | 17,720 |
| `rows[].total` | 납부보험료(계) | amount | 100% | 156,120 |
| `rows[].paid_date` | 납부일자 | date | 100% | 2023.09.11 |
| `rows[].note` | 비고 | text | 93% | 정산 분할 1/10회 |
| `sum.notice_health` | 고지보험료(건강보험)합계 | number | 100% | 4,596,080 |
| `sum.notice_ltc` | 고지보험료(장기요양)합계 | number | 100% | 594,160 |
| `sum.health` | 납부보험료(건강보험)합계 | number | 100% | 4,596,080 |
| `sum.ltc` | 납부보험료(장기요양)합계 | number | 100% | 594,160 |
| `sum.total` | 납부보험료(계)합계 | amount | 100% | 5,190,240 |
| `purpose` | 용도 | text | 100% | 기타 |
| `issue_date` | 발급일 | date | 100% | 2026년 1월 31일 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 국민건강보험공단이사장인 |
| `person.rrn` | 주민등록번호 | rrn | 37% | 660812-2****** |
