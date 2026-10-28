# 법인 — 서류별 항목

키 규칙과 타입은 [README.md](README.md)에 있습니다.


## 법인 등기사항전부증명서(현재 유효사항) (`corporate_registry`) — 키 65개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `viewed_at` | 열람일시 | datetime | 37% | 2026년01월31일 15시09분03초 |
| `issue_type` | 발급구분 | text | 100% | 열람용 |
| `issue_scope` | 증명서구분 | text | 100% | 현재 유효사항 |
| `reg_no` | 등기번호 | number | 100% | 155825 |
| `corp_reg_no` | 등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `company_name` | 상호 | text | 100% | 주식회사 유니온무역 |
| `head_office` | 본점 | text | 100% | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| `notice_method` | 공고방법 | text | 100% | 서울특별시 내에서 발행되는 일간 서울경제신문에 게재한다. |
| `par_value` | 1주의금액 | amount | 100% | 금 5,000 원 |
| `authorized_shares` | 발행할주식의총수 | text | 100% | 400,000 주 |
| `issued_shares` | 발행주식의총수 | text | 100% | 10,000 주 |
| `common_shares` | 보통주식 | text | 100% | 10,000 주 |
| `capital` | 자본금의액 | amount | 100% | 금 50,000,000 원 |
| `capital_change.changed` | 변경연월일 | text | 60% | 2025.02.08 변경 |
| `capital_change.registered` | 등기연월일 | text | 60% | 2025.02.13 등기 |
| `purposes[]` | 목적 | text | 100% | 1. 무역업 |
| `officers[].position` | 직위 | text | 100% | 사내이사 |
| `officers[].name` | 성명 | text | 100% | 박찬연 |
| `officers[].rrn` | 주민등록번호 | rrn | 100% | 900210-******* |
| `officers[].appointed` | 취임일 | date | 100% | 2024 년 11 월 01 일 |
| `officers[].appointment_type` | 취임구분 | text | 100% | 중임 |
| `officers[].registered` | 등기일 | date | 100% | 2024 년 11 월 14 일 |
| `officers[].address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `established` | 회사성립연월일 | date | 100% | 2018 년 11 월 01 일 |
| `opening_reason` | 등기기록개설사유 | text | 100% | 설립 |
| `opening_date` | 등기기록개설일 | date | 100% | 2018 년 11 월 01 일 |
| `jurisdiction` | 관할등기소 | text | 100% | 서울중앙지방법원 등기국 |
| `issue_no` | 발행번호 | number | 100% | 63538237030711037235 |
| `name_history[].name` | 상호 | text | 3% | 주식회사 한빛코리아 |
| `company_name_change.changed` | 변경연월일 | text | 10% | 2024.02.05 변경 |
| `company_name_change.registered` | 등기연월일 | text | 10% | 2024.02.10 등기 |
| `capital_history[].issued_shares` | 발행주식의총수 | text | 20% | 100,000 주 |
| `capital_history[].common_shares` | 보통주식 | text | 20% | 100,000 주 |
| `capital_history[].capital` | 자본금의액 | amount | 20% | 금 500,000,000 원 |
| `capital_history[].changed` | 변경연월일 | text | 7% | 2022.12.31 변경 |
| `capital_history[].registered` | 등기연월일 | text | 7% | 2023.01.09 등기 |
| `officers[].ended` | 퇴임일 | date | 23% | 2024 년 05 월 11 일 |
| `officers[].end_type` | 퇴임구분 | text | 23% | 사임 |
| `officers[].end_registered` | 등기일 | date | 23% | 2024 년 05 월 15 일 |
| `fee` | 수수료 | amount | 63% | 1,000원 |
| `issue_date` | 발행일 | text | 63% | 서기 2025년 05월 19일 |
| `seal.issuer` | 발급기관직인 | seal | 63% | 전산운영책임관인 |
| `confirm_no` | 발급확인번호 | text | 63% | 2QN6-F8DU-8EAX |
| `issue_date_short` | 발행일 | date | 63% | 2025/05/19 |
| `head_office_change.changed` | 변경연월일 | text | 33% | 2022.10.28 이전 |
| `head_office_change.registered` | 등기연월일 | text | 33% | 2022.11.05 등기 |
| `purpose_change.changed` | 변경연월일 | text | 20% | 2023.06.14 변경 |
| `purpose_change.registered` | 등기연월일 | text | 20% | 2023.06.17 등기 |
| `branches[].no` | 지점번호 | number | 17% | 1 |
| `branches[].address` | 지점소재지 | text | 17% | 제주특별자치도 제주시 중앙로 442, 4층 08호 (연동, 스마트빌딩) |
| `branches[].opened` | 설치일 | date | 17% | 2024 년 01 월 15 일 |
| `branches[].opened_registered` | 등기일 | date | 17% | 2024 년 01 월 19 일 |
| `office_history[].address` | 본점 | text | 20% | 부산광역시 해운대구 해운대로 480, 2층 09호 (재송동, 현대센터) |
| `office_history[].changed` | 변경연월일 | text | 3% | 2021.11.15 이전 |
| `office_history[].registered` | 등기연월일 | text | 3% | 2021.11.18 등기 |
| `purpose_history[].purposes[]` | 목적 | text | 10% | 1. 광고 대행업 |
| `purpose_history[].changed` | 변경연월일 | text | 3% | 2022.11.25 변경 |
| `purpose_history[].registered` | 등기연월일 | text | 3% | 2022.12.04 등기 |
| `preferred_shares` | 상환전환우선주식 | text | 3% | 29,996 주 |
| `branches[].closed` | 폐지일 | date | 0% | 2022 년 09 월 10 일 |
| `branches[].closed_registered` | 등기일 | date | 0% | 2022 년 09 월 18 일 |
| `name_history[].changed` | 변경연월일 | text | 0% | 2022.04.20 변경 |
| `name_history[].registered` | 등기연월일 | text | 0% | 2022.04.26 등기 |
| `joint_representation` | 공동대표 | text | 0% | 대표이사 현예지, 대표이사 정주하는 공동으로 회사를 대표 |
| `joint_registered` | 등기일 | date | 0% | 2024 년 01 월 26 일 |

## 정관 (`articles_of_incorporation`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company_name` | 상호 | text | 100% | 주식회사 유니온무역 |
| `revision_history[]` | 제정·개정일 | text | 100% | 제정 2018.11.01 |
| `company_name_en` | 영문상호 | text | 100% | Union Trading Co., Ltd. |
| `purposes[]` | 목적 | text | 100% | 1. 무역업 |
| `head_office_city` | 본점소재지 | text | 100% | 서울특별시 |
| `notice_method` | 공고방법 | text | 100% | 서울특별시 내에서 발행되는 일간 서울경제신문에 게재한다. |
| `authorized_shares` | 발행예정주식의총수 | text | 100% | 400,000주 |
| `par_value` | 1주의금액 | amount | 100% | 금 5,000원 |
| `initial_shares` | 설립시발행주식총수 | text | 100% | 5,000주 |
| `effective_date` | 시행일 | date | 100% | 2018년 11월 1일 |
| `revision_effective[]` | 시행일 | date | 83% | 2020년 6월 26일 |
| `certify_date` | 증명일 | date | 80% | 2026년 1월 24일 |
| `ceo` | 대표이사 | text | 80% | 박찬연 |
| `seal.corp` | 법인인감 | seal | 80% | 주식회사 유니온무역 대표이사인 |
| `amended.company_name` | 개정일 | date | 10% | 2024.02.05 |
| `amended.purposes` | 개정일 | date | 20% | 2023.06.14 |
| `preferred` | 종류주식 | text | 3% | 상환전환우선주식 |
| `amended.share_types` | 개정일 | date | 3% | 2011.06.28 |

## 주주명부 (`shareholder_registry`) — 키 24개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `base_date` | 기준일 | date | 100% | 2026.01.26 |
| `company_name` | 회사명 | text | 100% | (주)유니온무역 |
| `corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `total_shares` | 발행주식총수 | text | 100% | 10,000주 |
| `head_office` | 본점소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `par_value` | 1주의금액 | amount | 100% | 5,000원 |
| `capital` | 자본금 | amount | 100% | 50,000,000원 |
| `shareholders[].no` | 번호 | number | 100% | 1 |
| `shareholders[].name` | 주주명 | text | 100% | 박찬연 |
| `shareholders[].id_no` | 주민등록번호(사업자번호) | rrn | 100% | 900210-******* |
| `shareholders[].address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `shareholders[].share_type` | 주식종류 | text | 100% | 보통주 |
| `shareholders[].shares` | 소유주식수 | number | 100% | 7,404 |
| `shareholders[].amount` | 금액 | amount | 100% | 37,020,000 |
| `shareholders[].ratio` | 지분율 | percent | 100% | 74.0% |
| `shareholders[].acquired` | 취득일 | date | 100% | 2018.11.01 |
| `shareholders[].note` | 비고 | text | 100% | 대표이사 |
| `sum_shares` | 합계주식수 | amount | 100% | 10,000 |
| `sum_amount` | 합계금액 | amount | 100% | 50,000,000 |
| `sum_ratio` | 합계지분율 | percent | 100% | 100.0% |
| `certify_date` | 확인일 | date | 100% | 2026년 1월 31일 |
| `ceo` | 대표이사 | text | 100% | 박찬연 |
| `seal.corp` | 법인인감 | seal | 100% | 주식회사 유니온무역 대표이사인 |

## 재무제표(재무상태표·손익계산서) (`financial_statements`) — 키 33개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `current_term` | 당기 | text | 100% | 제 7(당)기 |
| `bs_current_date` | 당기말 | text | 100% | 2024년 12월 31일 현재 |
| `prior_term` | 전기 | text | 100% | 제 6(전)기 |
| `bs_prior_date` | 전기말 | text | 100% | 2023년 12월 31일 현재 |
| `company_name` | 회사명 | text | 100% | (주)유니온무역 |
| `unit` | 단위 | text | 100% | (단위 : 원) |
| `assets[].account` | 과목 | text | 100% | Ⅰ. 유동자산 |
| `assets[].current` | 당기 | amount | 100% | 11,122,518,720 |
| `assets[].prior` | 전기 | number | 100% | 8,311,220,220 |
| `liabilities[].account` | 과목 | text | 100% | Ⅰ. 유동부채 |
| `liabilities[].current` | 당기 | amount | 100% | 9,252,827,912 |
| `liabilities[].prior` | 전기 | number | 100% | 4,625,491,116 |
| `equity[].account` | 과목 | text | 100% | Ⅰ. 자본금 |
| `equity[].current` | 당기 | amount | 100% | 50,000,000 |
| `equity[].prior` | 전기 | number | 100% | 50,000,000 |
| `total_liabilities_equity.current` | 부채와자본총계(당기) | amount | 100% | 36,481,679,381 |
| `total_liabilities_equity.prior` | 부채와자본총계(전기) | number | 100% | 27,119,928,475 |
| `is_current_period` | 당기회계기간 | text | 100% | 2024년 01월 01일부터 2024년 12월 31일까지 |
| `is_prior_period` | 전기회계기간 | text | 100% | 2023년 01월 01일부터 2023년 12월 31일까지 |
| `income_statement[].account` | 과목 | text | 100% | Ⅰ. 매출액 |
| `income_statement[].current` | 당기 | amount | 100% | 61,800,000,000 |
| `income_statement[].prior` | 전기 | number | 100% | 49,310,988,871 |
| `appropriation_date_current` | 처분일 | text | 10% | 처분예정일 2025년 03월 27일 |
| `appropriation_date_prior` | 처분일 | text | 10% | 처분확정일 2024년 03월 26일 |
| `appropriation[].account` | 과목 | text | 10% | Ⅰ. 미처분이익잉여금 |
| `appropriation[].current` | 당기 | amount | 10% | 17,163,787,652 |
| `appropriation[].prior` | 전기 | number | 10% | 8,649,782,085 |
| `certify_date` | 확인일 | date | 27% | 2025년 08월 21일 |
| `ceo` | 대표이사 | text | 27% | 이민빈 |
| `seal.corp` | 법인인감 | seal | 27% | 주식회사 스마트에프앤비 대표이사인 |
| `manufacturing_cost[].account` | 과목 | text | 3% | Ⅰ. 재료비 |
| `manufacturing_cost[].current` | 당기 | amount | 3% | 30,291,246,736 |
| `manufacturing_cost[].prior` | 전기 | number | 3% | 23,074,391,287 |

## 법인인감증명서 (`corporate_seal_certificate`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 7988-2706-6500-7892 |
| `reg_no` | 등기번호 | number | 100% | 155825 |
| `seal.registered` | 등록인감 | seal | 100% | 주식회사 유니온무역 대표이사인 |
| `corp_reg_no` | 등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `company_name` | 상호 | text | 100% | 주식회사 유니온무역 |
| `head_office` | 본점 | text | 100% | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| `rep_title` | 자격 | text | 100% | 대표이사 |
| `rep_name` | 성명 | text | 100% | 박찬연 |
| `rep_rrn` | 주민등록번호 | rrn | 100% | 900210-1****** |
| `purpose` | 용도 | text | 100% | 여신거래용 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 25일 |
| `issue_office` | 발급기관 | text | 100% | 서울중앙지방법원 등기국 |
| `registrar` | 등기관 | text | 87% | 이정유 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 등기관인 |
| `fee` | 수수료 | amount | 100% | 1,000원 |
| `confirm_no` | 발급확인번호 | text | 13% | 6HW4-R4PD-T4YS |

## 이사회의사록 (`board_minutes`) — 키 40개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `datetime` | 일시 | text | 100% | 2026년 1월 21일 오후 3시 00분 |
| `venue` | 장소 | text | 100% | 본점 회의실 (서울특별시 중구 다산로 361, 6층) |
| `directors_total` | 이사총수 | text | 100% | 3명 |
| `directors_present` | 출석이사수 | text | 100% | 3명 |
| `auditor_total` | 감사총수 | text | 100% | 1명 |
| `auditor_present` | 출석감사수 | text | 100% | 1명 |
| `chair` | 의장 | text | 100% | 박찬연 |
| `loan.lender` | 차입은행 | text | 100% | 기업은행 |
| `loan.bank` | 차입기관 | text | 100% | 기업은행 범어지점 |
| `loan.kind` | 대출과목 | text | 100% | 일반자금대출 |
| `loan.amount` | 차입금액 | amount | 100% | 금 사십삼억일천만원정 (₩4,310,000,000) |
| `loan.period` | 차입기간 | text | 100% | 1년 (2026.01.28 ~ 2027.01.27) |
| `loan.purpose` | 자금용도 | text | 100% | 운영자금 |
| `loan.rate` | 적용금리 | text | 100% | 변동금리 (CD 91일물 + 가산금리) |
| `loan.collateral` | 담보 | text | 100% | 신용 |
| `agendas[].no` | 의안번호 | text | 100% | 제2호 의안 |
| `agendas[].title` | 의안 | text | 100% | 차입 관련 제반 권한 위임의 건 |
| `agendas[].body` | 결의내용 | text | 100% | 의장은 제1호 의안의 차입과 관련하여 여신거래약정서 등 제반 서류의 작성… |
| `agendas[].detail` | 세부내용 | text | 40% | 지점명 : 제주지점 / 소재지 : 제주특별자치도 제주시 첨단로 541, … |
| `end_time` | 종료시각 | text | 100% | 오후 3시 40분 |
| `minutes_date` | 작성일 | date | 100% | 2026년 1월 21일 |
| `company_name` | 상호 | text | 100% | (주)유니온무역 |
| `head_office` | 본점 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `signers[].title` | 자격 | text | 100% | 의장 대표이사 |
| `signers[].name` | 성명 | text | 100% | 박찬연 |
| `seal.corp` | 법인인감 | seal | 100% | 주식회사 유니온무역 대표이사인 |
| `seal.signer2` | 서명인2 | seal | 100% | 조태재 |
| `seal.signer3` | 서명인3 | seal | 100% | 선옥도 |
| `seal.signer4` | 서명인4 | seal | 83% | 길성은 |
| `seal.signer5` | 서명인5 | seal | 13% | 표진하 |
| `remote_count` | 원격참석 | text | 10% | 원격 참석 2명 포함 |
| `remote_attendees` | 원격참석이사 | text | 10% | 사내이사 김준아, 사내이사 허지태 |
| `remote_method` | 원격참석방법 | text | 10% | 화상회의, Zoom |
| `signers[].remote` | 비고 | text | 10% | (원격 참석) |
| `agendas[].votes` | 표결결과 | text | 7% | 찬성 2명, 반대 1명 (사내이사 김호희) |
| `notary.reg_no` | 등부번호 | text | 7% | 2026년 제331호 |
| `notary.date` | 인증일 | date | 7% | 2026년 4월 13일 |
| `notary.office` | 공증인 | text | 7% | 법무법인 해송 |
| `notary.lawyer` | 공증담당변호사 | text | 7% | 이형윤 |
| `seal.notary` | 공증인직인 | seal | 7% | 공증인 |

## 임시주주총회의사록 (`shareholders_meeting_minutes`) — 키 35개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `meeting_title` | 의사록종류 | text | 100% | 임시주주총회의사록 |
| `datetime` | 일시 | text | 100% | 2026년 1월 16일 오후 4시 30분 |
| `venue` | 장소 | text | 100% | 본점 대회의실 (서울특별시 중구 다산로 361, 6층) |
| `shareholders_total` | 주주의총수 | text | 100% | 3명 |
| `issued_shares` | 발행주식의총수 | text | 100% | 10,000주 |
| `shareholders_present` | 출석주주의수 | text | 100% | 3명 |
| `shares_present` | 출석주주의주식수 | text | 100% | 10,000주 |
| `present_ratio` | 출석비율 | percent | 100% | 100.00% |
| `chair` | 의장 | text | 100% | 박찬연 |
| `agendas[].no` | 의안번호 | text | 100% | 제1호 의안 |
| `agendas[].title` | 의안 | text | 100% | 이사 선임의 건 |
| `agendas[].body` | 결의내용 | text | 100% | 의장은 사내이사 조태재의 임기가 만료됨에 따라 이사를 선임할 필요가 있음… |
| `agendas[].detail` | 세부내용 | text | 100% | 사내이사  조태재 (1985년 3월 8일생)  중임 |
| `end_time` | 종료시각 | text | 100% | 오후 5시 26분 |
| `minutes_date` | 작성일 | date | 100% | 2026년 1월 16일 |
| `company_name` | 상호 | text | 100% | (주)유니온무역 |
| `head_office` | 본점 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `signers[].title` | 자격 | text | 100% | 의장 대표이사 |
| `signers[].name` | 성명 | text | 100% | 박찬연 |
| `seal.corp` | 법인인감 | seal | 100% | 주식회사 유니온무역 대표이사인 |
| `seal.signer2` | 서명인2 | seal | 100% | 김준아 |
| `seal.signer3` | 서명인3 | seal | 53% | 황보형아 |
| `proxy_count` | 대리출석 | text | 27% | 위임장에 의한 대리출석 1명 포함 |
| `treasury_shares` | 자기주식수 | text | 7% | 60,649주 |
| `attendees[].name` | 주주명 | text | 40% | 이욱유 |
| `attendees[].shares` | 소유주식수 | number | 40% | 775,624 |
| `attendees[].method` | 출석구분 | text | 40% | 본인출석 |
| `attendees[].proxy` | 대리인 | text | 40% | 정우승 (대리인) |
| `notary.reg_no` | 등부번호 | text | 10% | 2025년 제3341호 |
| `notary.date` | 인증일 | date | 10% | 2025년 4월 18일 |
| `notary.office` | 공증인 | text | 10% | 법무법인 정명 |
| `notary.lawyer` | 공증담당변호사 | text | 10% | 설소서 |
| `seal.notary` | 공증인직인 | seal | 10% | 공증인 |
| `seal.signer4` | 서명인4 | seal | 17% | 김수예 |
| `agendas[].votes` | 표결결과 | text | 7% | 찬성 48,998주, 반대 11,002주 |

## 위임장 (`power_of_attorney`) — 키 23개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `agent.name` | 성명 | text | 100% | 구은태 |
| `agent.birth` | 생년월일 | date | 100% | 1976.10.04 |
| `agent.relation` | 본인과의관계 | text | 100% | 직원 (회계팀 과장) |
| `agent.phone` | 연락처 | phone | 100% | 010-5160-1926 |
| `agent.address` | 주소 | text | 100% | 서울특별시 노원구 노원로 458-26, 112동 1904호 (하계동, 호… |
| `tasks[]` | 위임내용 | text | 100% | 1. 기업은행 범어지점 여신(대출) 기한연장 신청 및 관련 서류 제출 일… |
| `period` | 위임기간 | text | 90% | 2026.01.31 ~ 2026.03.02 |
| `grant_date` | 작성일 | date | 100% | 2026년 01월 31일 |
| `grantor.type` | 위임인구분 | checkbox | 100% | 보기: 법인 / 개인 |
| `grantor.name` | 상호 | text | 100% | (주)유니온무역 |
| `grantor.ceo` | 대표자 | text | 70% | 박찬연 |
| `grantor.biz_no` | 사업자등록번호 | biz_no | 70% | 264-82-36559 |
| `grantor.corp_reg_no` | 법인등록번호 | corp_reg_no | 70% | 200112-7448551 |
| `grantor.address` | 본점소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `grantor.phone` | 연락처 | phone | 100% | 02-9508-6789 |
| `seal.corp` | 법인인감 | seal | 70% | 주식회사 유니온무역 대표이사인 |
| `attachment` | 첨부서류 | text | 100% | 법인인감증명서 1부 |
| `recipient` | 제출처 | text | 100% | 기업은행 범어지점 귀중 |
| `sub_delegation` | 복대리인선임 | checkbox | 23% | 보기: 허용 / 불허 |
| `grantor.birth` | 생년월일 | date | 30% | 1966년 08월 12일 |
| `seal.grantor` | 위임인 | seal | 30% | 현예지 |
| `tasks_extra` | 위임내용 | text | 20% | 4. 통장 및 OTP 재발급 신청·수령 |
| `use_limit` | 사용제한 | text | 10% | 본 위임장은 위 업무 1회에 한하여 유효함 |
