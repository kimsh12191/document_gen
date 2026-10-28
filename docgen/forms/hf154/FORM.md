# 차입신청서(무역금융용) (`hf154`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf154 · card-hash: 57fbe3d71025 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 차입신청서(무역금융용)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf154 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.154 (대출) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 84칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `related_list.*.name` | 성명 | text | 1쪽 [128, 472, 180, 484] (1행) | 늘 | 파일 key | 값 종류 `person` (파일) | fields.json:58 | 묻기 |
| `loan.basis_list.*.line` | 수량 | text | 1쪽 [129, 620, 203, 633] (1행) | 늘 | 파일 key | 값 종류 `note` (파일) | fields.json:92 | 묻기 |
| `bank.opinion_list.*.line` | 수량 | text | 1쪽 [126, 738, 200, 751] (1행) | 늘 | 파일 key | 값 종류 `note` (파일) | fields.json:177 | 묻기 |
| `loan.amount` | 금액 | amount | 1쪽 [440, 319, 527, 331] | 늘 | 파일 key | 고객 정보 (키 `loan.amount`) | fields.json:228 | 묻기 |
| `loan.interest_timing` | 이자지급시기 | text | 1쪽 [253, 425, 326, 437] | 늘 | 파일 key | 고객 정보 (키 `loan.interest_timing`) | fields.json:320 | 묻기 |
| `related_list.*.age` | 연령 | number | 1쪽 [267, 472, 286, 484] (1행) | 늘 | 파일 key | 값 종류 `age_years` (파일) | fields.json:335 | 묻기 |
| `trade.lc_no` | L/C(계약서)No | rrn | 1쪽 [268, 519, 397, 532] | 늘 | 파일 key | 고객 정보 (키 `trade.lc_no`) | fields.json:369 | 묻기 |
| `trade.amount` | 금액 | amount | 1쪽 [272, 543, 366, 555] | 늘 | 파일 key | 고객 정보 (키 `trade.amount`) | fields.json:384 | 묻기 |
| `trade.goods` | 품목 | text | 1쪽 [268, 567, 376, 579] | 늘 | 파일 key | 고객 정보 (키 `trade.goods`) | fields.json:399 | 묻기 |
| `trade.quantity` | 수량 | number | 1쪽 [368, 594, 378, 606] | 늘 | 파일 key | 고객 정보 (키 `trade.quantity`) | fields.json:414 | 묻기 |
| `related_list.*.job` | 직업및직위 | text | 1쪽 [312, 474, 376, 483] (1행) | 늘 | 파일 key | 값 종류 `job_position` (파일) | fields.json:429 | 묻기 |
| `related_list.*.relation` | 차주와의관계 | text | 1쪽 [388, 472, 457, 484] (1행) | 늘 | 파일 key | 값 종류 `guarantor_relation` (파일) | fields.json:463 | 묻기 |
| `related_list.*.monthly_income` | 월평균수입 | amount | 1쪽 [475, 473, 527, 483] (1행) | 늘 | 파일 key | 값 종류 `amount` (파일) | fields.json:497 | 묻기 |
| `related_list.*.net_assets` | 실자산 | amount | 1쪽 [569, 472, 646, 484] (1행) | 늘 | 파일 key | 값 종류 `amount` (파일) | fields.json:531 | 묻기 |
| `trade.shipment_date` | 선적(납품)기일 | date | 1쪽 [630, 520, 744, 531] | 늘 | 파일 key | 고객 정보 (키 `trade.shipment_date`) | fields.json:565 | 묻기 |
| `trade.incoterms` | 가격조건 | text | 1쪽 [625, 543, 660, 555] | 늘 | 파일 key | 고객 정보 (키 `trade.incoterms`) | fields.json:580 | 묻기 |
| `trade.payment_terms` | 결제조건 | text | 1쪽 [627, 567, 729, 579] | 늘 | 파일 key | 고객 정보 (키 `trade.payment_terms`) | fields.json:594 | 묻기 |
| `trade.special_terms` | 기타특수조건 | text | 1쪽 [626, 594, 700, 606] | 늘 | 파일 key | 고객 정보 (키 `trade.special_terms`) | fields.json:609 | 묻기 |
| `loan.due_date` | 기한 | date | 1쪽 [656, 370, 744, 382] | 늘 | 파일 key | 고객 정보 (키 `loan.due_date`) | fields.json:717 | 묻기 |
| `loan.repay` | 상환자원및방법 | text | 1쪽 [653, 425, 808, 437] | 늘 | 파일 key | 고객 정보 (키 `loan.repay`) | fields.json:732 | 묻기 |
| `related_list.*.address` | 주소(전화번호) | text | 1쪽 [656, 475, 889, 482] (1행) | 늘 | 파일 key | 값 종류 `address` (파일) | fields.json:747 | 묻기 |
| `bank.approval_date` | 승인일자 | date | 1쪽 [705, 691, 791, 703] | 늘 | 파일 key | 고객 정보 (키 `bank.approval_date`) | fields.json:781 | 묻기 |
| `bank.approval_expiry` | 승인기한 | date | 1쪽 [707, 715, 793, 727] | 늘 | 파일 key | 고객 정보 (키 `bank.approval_expiry`) | fields.json:796 | 묻기 |
| `bank.proper_limit_usd` | U$ | amount | 1쪽 [828, 738, 914, 751] | 늘 | 파일 key | 고객 정보 (키 `bank.proper_limit_usd`) | fields.json:811 | 묻기 |
| `bank.used_usd` | U$ | amount | 1쪽 [861, 765, 914, 778] | 늘 | 파일 key | 고객 정보 (키 `bank.used_usd`) | fields.json:825 | 묻기 |
| `bank.limit_remaining_usd` | U$ | amount | 1쪽 [820, 792, 914, 804] | 늘 | 파일 key | 고객 정보 (키 `bank.limit_remaining_usd`) | fields.json:839 | 묻기 |
| `trade.expiry_date` | 유효기일 | date | 1쪽 [841, 520, 911, 531] | 늘 | 파일 key | 고객 정보 (키 `trade.expiry_date`) | fields.json:853 | 묻기 |
| `date` | 작성일(년월일) | date | 1쪽 [396, 149, 464, 159] | 늘 | 파일 key | 고객 정보 (키 `date`) | fields.json:1834 | 묻기 |
| `company.address` | 신청인주소 | text | 1쪽 [253, 222, 582, 234] | 늘 | 파일 key | 고객 정보 (키 `company.address`) | fields.json:1847 | 묻기 |
| `company.name` | 신청인상호 | text | 1쪽 [258, 249, 373, 261] | 늘 | 파일 key | 고객 정보 (키 `company.name`) | fields.json:1860 | 묻기 |
| `company.phone` | 신청인전화번호 | phone | 1쪽 [543, 251, 622, 260] | 늘 | 파일 key | `profile.corporation.phone` (파일) | fields.json:1873 | 묻기 |
| `company.ceo` | 신청인대표자 | text | 1쪽 [258, 271, 327, 284] | 늘 | 파일 key | 고객 정보 (키 `company.ceo`) | fields.json:1887 | 묻기 |
| `loan.rate` | 이자율연이율(%) | number | 1쪽 [349, 401, 382, 413] | 늘 | 파일 key | 고객 정보 (키 `loan.rate`) | fields.json:1900 | 묻기 |
| `loan.overdue_rate` | 지연배상금이율연(%) | number | 1쪽 [752, 401, 786, 413] | 늘 | 파일 key | 고객 정보 (키 `loan.overdue_rate`) | fields.json:1914 | 묻기 |
| `bank.trade_limit` | 무역금융승인한도(천원) | amount | 1쪽 [807, 620, 894, 632] | 늘 | 파일 key | 고객 정보 (키 `bank.trade_limit`) | fields.json:1928 | 묻기 |
| `bank.trade_used` | 사용액(본건포함)(천원) | number | 1쪽 [817, 644, 894, 656] | 늘 | 파일 key | 고객 정보 (키 `bank.trade_used`) | fields.json:1942 | 묻기 |
| `bank.trade_remaining` | 여유액(본건취급후)(천원) | amount | 1쪽 [800, 667, 894, 679] | 늘 | 파일 key | 고객 정보 (키 `bank.trade_remaining`) | fields.json:1956 | 묻기 |
| `credit.trade.production` | 생산 | amount | 2쪽 [279, 121, 373, 133] | 늘 | 파일 key | 고객 정보 (키 `credit.trade.production`) | fields.json:868 | 묻기 |
| `credit.trade.raw_import` | 원자재수입 | number | 2쪽 [287, 154, 373, 166] | 늘 | 파일 key | 고객 정보 (키 `credit.trade.raw_import`) | fields.json:883 | 묻기 |
| `credit.trade.raw_purchase` | 원자재구매 | number | 2쪽 [287, 194, 373, 207] | 늘 | 파일 key | 고객 정보 (키 `credit.trade.raw_purchase`) | fields.json:898 | 묻기 |
| `credit.trade.product_purchase` | 완제품구매 | amount | 2쪽 [278, 228, 373, 238] | 늘 | 파일 key | 고객 정보 (키 `credit.trade.product_purchase`) | fields.json:913 | 묻기 |
| `credit.trade.comprehensive` | 포괄금융 | number | 2쪽 [287, 252, 373, 265] | 늘 | 파일 key | 고객 정보 (키 `credit.trade.comprehensive`) | fields.json:928 | 묻기 |
| `credit.trade.agri_export` | 농수산물수출준비 | number | 2쪽 [296, 278, 373, 290] | 늘 | 파일 key | 고객 정보 (키 `credit.trade.agri_export`) | fields.json:943 | 묻기 |
| `credit.trade.local_lc` | 내국신용장발행 | number | 2쪽 [287, 303, 373, 315] | 늘 | 파일 key | 고객 정보 (키 `credit.trade.local_lc`) | fields.json:958 | 묻기 |
| `credit.trade.import_lc` | 수입신용장발행 | number | 2쪽 [287, 328, 373, 340] | 늘 | 파일 key | 고객 정보 (키 `credit.trade.import_lc`) | fields.json:973 | 묻기 |
| `무역금융신청건포함명세_목록.*.당행` | 당행 | text | - (1행) | 늘 | 표 행 (묶음·항목명 '당 행') | 값 종류 `skip` (항목명 자동) | fields.json:988 | 묻기 |
| `계` | 계 | text | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:1016 | 묻기 |
| `credit.working.trade_finance` | 무역금융 | number | 2쪽 [296, 455, 373, 467] | 늘 | 파일 key | 고객 정보 (키 `credit.working.trade_finance`) | fields.json:1028 | 묻기 |
| `credit.working.general` | 일반자금대출 | amount | 2쪽 [279, 480, 373, 492] | 늘 | 파일 key | 고객 정보 (키 `credit.working.general`) | fields.json:1043 | 묻기 |
| `credit.working.overdraft` | 당좌대출 | number | 2쪽 [287, 505, 373, 517] | 늘 | 파일 key | 고객 정보 (키 `credit.working.overdraft`) | fields.json:1058 | 묻기 |
| `credit.working.commercial_bill` | 상업어음 | number | 2쪽 [287, 530, 373, 543] | 늘 | 파일 key | 고객 정보 (키 `credit.working.commercial_bill`) | fields.json:1073 | 묻기 |
| `운전자금_목록.*.당행` | 당행 | text | - (1행) | 늘 | 표 행 (묶음·항목명 '당 행') | 값 종류 `skip` (항목명 자동) | fields.json:1088 | 묻기 |
| `credit.facility.general` | 일반자금대출 | number | 2쪽 [287, 631, 373, 644] | 늘 | 파일 key | 고객 정보 (키 `credit.facility.general`) | fields.json:1116 | 묻기 |
| `credit.facility.fx_loan` | 외화대출 | amount | 2쪽 [265, 657, 366, 669] | 늘 | 파일 key | 고객 정보 (키 `credit.facility.fx_loan`) | fields.json:1131 | 묻기 |
| `시설자금_목록.*.당행` | 당행 | text | - (1행) | 늘 | 표 행 (묶음·항목명 '당 행') | 값 종류 `skip` (항목명 자동) | fields.json:1146 | 묻기 |
| `credit.guarantee.trade` | 무역금융관계 | number | 2쪽 [287, 783, 373, 795] | 늘 | 파일 key | 고객 정보 (키 `credit.guarantee.trade`) | fields.json:1188 | 묻기 |
| `credit.guarantee.other_krw` | 기타원화표시 | amount | 2쪽 [278, 809, 373, 820] | 늘 | 파일 key | 고객 정보 (키 `credit.guarantee.other_krw`) | fields.json:1203 | 묻기 |
| `credit.guarantee.other_fx` | 기타외화표시 | amount | 2쪽 [261, 834, 362, 846] | 늘 | 파일 key | 고객 정보 (키 `credit.guarantee.other_fx`) | fields.json:1218 | 묻기 |
| `당행` | 당행 | text | - | 늘 | 표 행 (묶음·항목명 '당 행') | 값 종류 `skip` (항목명 자동) | fields.json:1233 | 묻기 |
| `무역금융신청건포함명세_목록.*.타행` | 타행 | text | - (1행) | 늘 | 표 행 (묶음·항목명 '타 행') | 값 종류 `skip` (항목명 자동) | fields.json:1247 | 묻기 |
| `운전자금_목록.*.타행` | 타행 | text | - (1행) | 늘 | 표 행 (묶음·항목명 '타 행') | 값 종류 `skip` (항목명 자동) | fields.json:1401 | 묻기 |
| `시설자금_목록.*.타행` | 타행 | text | - (1행) | 늘 | 표 행 (묶음·항목명 '타 행') | 값 종류 `skip` (항목명 자동) | fields.json:1499 | 묻기 |
| `지급보증_목록.*.타행` | 타행 | text | - (1행) | 늘 | 표 행 (묶음·항목명 '타 행') | 값 종류 `skip` (항목명 자동) | fields.json:1583 | 묻기 |
| `타행` | 타행 | text | - | 늘 | 표 행 (묶음·항목명 '타 행') | 값 종류 `skip` (항목명 자동) | fields.json:1639 | 묻기 |
| `property.location` | 부동산 | text | - | 늘 | 파일 key | `rule:free_text` (파일) | fields.json:1651 | 묻기 |
| `collateral.other` | 기타 | text | 2쪽 [548, 808, 622, 820] | 늘 | 파일 key | 고객 정보 (키 `collateral.other`) | fields.json:1665 | 묻기 |
| `deposit.savings_balance` | 보통예금 | amount | 2쪽 [658, 303, 721, 315] | 늘 | 파일 key | 고객 정보 (키 `deposit.savings_balance`) | fields.json:1679 | 묻기 |
| `deposit.time_balance` | 정기예금 | amount | 2쪽 [658, 328, 721, 340] | 늘 | 파일 key | 고객 정보 (키 `deposit.time_balance`) | fields.json:1694 | 묻기 |
| `계2` | 계 | text | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:1709 | 묻기 |
| `collateral.time_deposit` | 정기예금 | amount | 2쪽 [845, 455, 921, 467] | 늘 | 파일 key | 고객 정보 (키 `collateral.time_deposit`) | fields.json:1721 | 묻기 |
| `collateral_list.i.property_amount` | 담보제공액 | amount | 2쪽 [825, 631, 921, 644] | 늘 | 파일 key | 값 종류 `amount` (파일) | fields.json:1736 | 묻기 |
| `deposit_list.*.savings_pledged` | 담보제공액 | number | 2쪽 [764, 303, 840, 315] (1행) | 늘 | 파일 key | 값 종류 `amount` (파일) | fields.json:1751 | 묻기 |
| `deposit_list.*.time_pledged` | 담보제공액 | number | 2쪽 [778, 328, 840, 340] (1행) | 늘 | 파일 key | 값 종류 `amount` (파일) | fields.json:1768 | 묻기 |
| `deposit_list.*.savings_note` | 비고 | text | 2쪽 [852, 304, 918, 315] (1행) | 늘 | 파일 key | 값 종류 `note` (파일) | fields.json:1785 | 묻기 |
| `deposit_list.*.time_note` | 비고 | text | 2쪽 [852, 329, 918, 340] (1행) | 늘 | 파일 key | 값 종류 `note` (파일) | fields.json:1802 | 묻기 |
| `export.last_year` | 전년도실적 | amount | 2쪽 [645, 124, 718, 134] | 늘 | 파일 key | 고객 정보 (키 `export.last_year`) | fields.json:1819 | 묻기 |
| `export.last_year_nego` | 전년도실적당행Nego액 | amount | 2쪽 [849, 124, 895, 130] | 늘 | 파일 key | 고객 정보 (키 `export.last_year_nego`) | fields.json:1970 | 묻기 |
| `export.past_year` | 과거1년간실적 | amount | 2쪽 [659, 145, 731, 153] | 늘 | 파일 key | 고객 정보 (키 `export.past_year`) | fields.json:1984 | 묻기 |
| `export.past_year_nego` | 과거1년간당행Nego액 | amount | 2쪽 [850, 146, 900, 152] | 늘 | 파일 key | 고객 정보 (키 `export.past_year_nego`) | fields.json:1998 | 묻기 |
| `export.recent_3m` | 최근3개월실적 | amount | 2쪽 [659, 165, 726, 173] | 늘 | 파일 key | 고객 정보 (키 `export.recent_3m`) | fields.json:2012 | 묻기 |
| `export.recent_3m_nego` | 최근3개월당행Nego액 | amount | 2쪽 [849, 167, 895, 172] | 늘 | 파일 key | 고객 정보 (키 `export.recent_3m_nego`) | fields.json:2026 | 묻기 |
| `export.this_year` | 금년도수출실적 | amount | 2쪽 [668, 186, 727, 194] | 늘 | 파일 key | 고객 정보 (키 `export.this_year`) | fields.json:2040 | 묻기 |
| `export.this_year_nego` | 금년도당행Nego액 | amount | 2쪽 [850, 187, 894, 193] | 늘 | 파일 key | 고객 정보 (키 `export.this_year_nego`) | fields.json:2054 | 묻기 |
| `export.this_year_plan` | 금년도예정액 | amount | 2쪽 [836, 206, 893, 213] | 늘 | 파일 key | 고객 정보 (키 `export.this_year_plan`) | fields.json:2068 | 묻기 |

## 체크·도장·서명 (marks) — 8칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.과목` | 과목 | checkbox (무역어음대 / 수입신용장 발행 / 내국신용장 발행 / 보기4) | 1쪽 [256, 359, 348, 373] | 늘 | 체크 (항목명) | 보기 중 고름: 무역어음대 / 수입신용장 발행 / 내국신용장 발행 / ? | fields.json:243 | 묻기 |
| `check.자금용도` | 자금용도 | checkbox (생산자금 / 원자재구매자금 / 원자재수입자금 / 완제품구매자금 / 포괄금융) | 1쪽 [656, 299, 734, 314] | 늘 | 체크 (항목명) | 보기 중 고름: 생산자금 / 원자재구매자금 / 원자재수입자금 / 완제품구매자금 / 포괄금융 | fields.json:624 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [729, 101, 795, 144] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [729, 101, 795, 144] | 늘 | - | - | - | 묻기 |
| `seal.staff.팀장` | 팀장 | seal | 1쪽 [806, 107, 850, 138] | 늘 | - | - | - | 묻기 |
| `sign.staff.팀장` | 팀장 | signature | 1쪽 [795, 101, 861, 144] | 늘 | - | - | - | 묻기 |
| `seal.staff.부점장` | 부점장 | seal | 1쪽 [867, 105, 917, 140] | 늘 | - | - | - | 묻기 |
| `sign.staff.부점장` | 부점장 | signature | 1쪽 [861, 101, 923, 144] | 늘 | - | - | - | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키 `a` ← `b`:** 질문·정답은 공통 키 a, 서식의 원래 키는 b (키 사전이 정함).
- **키는·값은:** 어디서 정해지나. 원본 서식의 "규칙"·"항목명 자동" 은 키 사전(studio 키 사전 화면, `_common/key_rules.json`)이 항목명으로 정한 것 — 모든 서식에 같이 적용. 이 서식의 그 칸만 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
- **고칠 곳:** html·코드 서식은 템플릿 줄(칸 자리·키·항목명)과 fields.json 줄(값 출처·질문 설정 q), 원본 서식은 fields.json 의 그 칸(박스 `rect`·항목명·키·값·q). html·코드 서식에서 fields.json 에 줄이 없는 칸의 질문 설정은 fields.json 맨 위 `"q": {"키": {…}}` 묶음에.

## 질문 → 답 (seed 1000000 로 그린 실제 문항)

질문은 모델에게 가는 글 전부, 답은 데이터의 정답 (그린 문서의 값·위치). 질문 문장·답 꼴은 공통 `docgen/forms/_common/questions.json`.

### 서류 분류 `classify` · 채점 acc

질문:

```
이 문서는 고객이 은행에 제출한 서류입니다. 서류의 정식 명칭(서류명)을 답하세요. 설명 없이 서류명만 한 줄로 답하세요.
```

답:

```json
"차입신청서(무역금융용)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "성예율",
 "해당 없음",
 "18,240,000",
 "만기 일시",
 "47",
 "478199-9117030",
 "GBP 31,800",
 "플라스틱 원료",
 "2",
 "자영업/대표",
 "대표이사",
 "350,000",
 "5,390,000",
 "2026년 2월 21일",
 "FCA",
 "D/A 60 DAYS",
 "2024-07-06",
 "원리금균등분할상환",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "2024.03.29",
 "2024.12.14",
 "39,310,000",
 "90,000",
 "5,560,000원",
 "2025.11.30",
 "2025.04.01",
 "제주특별자치도 제주시 첨단로 381-19, 2층",
 "(주)미래케미칼",
 "064-756-8800",
 "남궁예태",
 "4.97",
 "4.53",
 "30,780,000",
 "7,220,000",
 "3,380,000원",
 "5,730,000원",
 "13,370,000",
 "28,960,000",
 "129,020,000원",
 "31,540,000",
 "7,540,000",
 "14,510,000",
 "20,520,000",
 "2,920,000",
 "9,150,000원",
 "65,920,000",
 "64,710,000",
 "28,330,000",
 "USD 178,500",
 "38,040,000",
 "168,970,000원",
 "USD 131,800",
 "760,000",
 "610,000",
 "5,910,000",
 "129,830,000",
 "5,000,000",
 "390,000",
 "GBP 51,500",
 "GBP 132,200",
 "CAD 139,500",
 "GBP 101,400",
 "USD 167,600",
 "CAD 122,300",
 "EUR 80,600",
 "USD 24,400",
 "CNY 112,900"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"5,730,000원"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"760,000"
```

### 정보 추출 `kie` · 채점 vl_f1 (값+위치)

틀 (질문의 항목 한 줄 · 답 항목 하나 · 빈 칸일 때) — `questions.json` 의 `kie`:

```
item:         - {key}: {label}{note}
answer:       {"key": "{key}", "value": "{value}", "bbox_2d": "{bbox_2d}", "page": "{page}"}
answer_empty: {"key": "{key}", "value": null}
```

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- loan.basis_list.0.line: 수량 (1행)
- loan.basis_list.4.line: 수량 (5행)
- related_list.0.age: 연령 (1행)
- related_list.1.age: 연령 (2행)
- related_list.1.job: 직업및직위 (2행)
- bank.proper_limit_usd: U$ (같은 항목명 중 1번째 칸)
- bank.limit_remaining_usd: U$ (같은 항목명 중 3번째 칸)
- company.address: 신청인주소
- loan.overdue_rate: 지연배상금이율연(%)
- bank.trade_limit: 무역금융승인한도(천원)
- bank.trade_used: 사용액(본건포함)(천원)
- bank.trade_remaining: 여유액(본건취급후)(천원)
- credit.trade.production: 생산
- credit.trade.raw_purchase: 원자재구매
- 무역금융신청건포함명세_목록.0.당행: 당행 (무역금융신청건포함명세 목록 1행)
- credit.working.general: 일반자금대출 (같은 항목명 중 1번째 칸)
- credit.working.commercial_bill: 상업어음
- credit.facility.fx_loan: 외화대출
- 시설자금_목록.0.당행: 당행 (시설자금 목록 1행)
- credit.guarantee.trade: 무역금융관계
- 당행: 당행 (같은 항목명 중 8번째 칸)
- 무역금융신청건포함명세_목록.1.타행: 타행 (무역금융신청건포함명세 목록 2행)
- 무역금융신청건포함명세_목록.2.타행: 타행 (무역금융신청건포함명세 목록 3행)
- 무역금융신청건포함명세_목록.4.타행: 타행 (무역금융신청건포함명세 목록 5행)
- 운전자금_목록.1.타행: 타행 (운전자금 목록 2행)
- 운전자금_목록.4.타행: 타행 (운전자금 목록 5행)
- 시설자금_목록.1.타행: 타행 (시설자금 목록 2행)
- 지급보증_목록.3.타행: 타행 (지급보증 목록 4행)
- property.location: 부동산 (물건 소재지)
- deposit.savings_balance: 보통예금
- 계2: 계 (같은 항목명 중 2번째 칸)
- deposit_list.0.savings_pledged: 담보제공액 (1행)
- deposit_list.0.savings_note: 비고 (1행)
- deposit_list.1.time_note: 비고 (2행)
- export.last_year: 전년도실적
- export.last_year_nego: 전년도실적당행Nego액
- export.recent_3m: 최근3개월실적
- export.recent_3m_nego: 최근3개월당행Nego액
- export.this_year_nego: 금년도당행Nego액
- export.this_year_plan: 금년도예정액
```

답:

```json
[{"key": "loan.basis_list.0.line", "value": "해당 없음", "bbox_2d": [129, 620, 203, 633], "page": 1},
 {"key": "loan.basis_list.4.line", "value": null},
 {"key": "related_list.0.age", "value": "47", "bbox_2d": [267, 472, 286, 484], "page": 1},
 {"key": "related_list.1.age", "value": null},
 {"key": "related_list.1.job", "value": null},
 {"key": "bank.proper_limit_usd", "value": "39,310,000", "bbox_2d": [828, 738, 914, 751], "page": 1},
 {"key": "bank.limit_remaining_usd", "value": "5,560,000원", "bbox_2d": [820, 792, 914, 804], "page": 1},
 {"key": "company.address", "value": "제주특별자치도 제주시 첨단로 381-19, 2층", "bbox_2d": [253, 222, 582, 234], "page": 1},
 {"key": "loan.overdue_rate", "value": "4.53", "bbox_2d": [752, 401, 786, 413], "page": 1},
 {"key": "bank.trade_limit", "value": "30,780,000", "bbox_2d": [807, 620, 894, 632], "page": 1},
 {"key": "bank.trade_used", "value": "7,220,000", "bbox_2d": [817, 644, 894, 656], "page": 1},
 {"key": "bank.trade_remaining", "value": "3,380,000원", "bbox_2d": [800, 667, 894, 679], "page": 1},
 {"key": "credit.trade.production", "value": "5,730,000원", "bbox_2d": [279, 121, 373, 133], "page": 2},
 {"key": "credit.trade.raw_purchase", "value": "28,960,000", "bbox_2d": [287, 194, 373, 207], "page": 2},
 {"key": "무역금융신청건포함명세_목록.0.당행", "value": null},
 {"key": "credit.working.general", "value": "9,150,000원", "bbox_2d": [279, 480, 373, 492], "page": 2},
 {"key": "credit.working.commercial_bill", "value": "64,710,000", "bbox_2d": [287, 530, 373, 543], "page": 2},
 {"key": "credit.facility.fx_loan", "value": "USD 178,500", "bbox_2d": [265, 657, 366, 669], "page": 2},
 {"key": "시설자금_목록.0.당행", "value": null},
 {"key": "credit.guarantee.trade", "value": "38,040,000", "bbox_2d": [287, 783, 373, 795], "page": 2},
 {"key": "당행", "value": null},
 {"key": "무역금융신청건포함명세_목록.1.타행", "value": null},
 {"key": "무역금융신청건포함명세_목록.2.타행", "value": null},
 {"key": "무역금융신청건포함명세_목록.4.타행", "value": null},
 {"key": "운전자금_목록.1.타행", "value": null},
 {"key": "운전자금_목록.4.타행", "value": null},
 {"key": "시설자금_목록.1.타행", "value": null},
 {"key": "지급보증_목록.3.타행", "value": null},
 {"key": "property.location", "value": null},
 {"key": "deposit.savings_balance", "value": "760,000", "bbox_2d": [658, 303, 721, 315], "page": 2},
 {"key": "계2", "value": null},
 {"key": "deposit_list.0.savings_pledged", "value": "5,000,000", "bbox_2d": [764, 303, 840, 315], "page": 2},
 {"key": "deposit_list.0.savings_note", "value": "해당 없음", "bbox_2d": [852, 304, 918, 315], "page": 2},
 {"key": "deposit_list.1.time_note", "value": "해당 없음", "bbox_2d": [852, 329, 918, 340], "page": 2},
 {"key": "export.last_year", "value": "GBP 51,500", "bbox_2d": [645, 124, 718, 134], "page": 2},
 {"key": "export.last_year_nego", "value": "GBP 132,200", "bbox_2d": [849, 124, 895, 130], "page": 2},
 {"key": "export.recent_3m", "value": "USD 167,600", "bbox_2d": [659, 165, 726, 173], "page": 2},
 {"key": "export.recent_3m_nego", "value": "CAD 122,300", "bbox_2d": [849, 167, 895, 172], "page": 2},
 {"key": "export.this_year_nego", "value": "USD 24,400", "bbox_2d": [850, 187, 894, 193], "page": 2},
 {"key": "export.this_year_plan", "value": "CNY 112,900", "bbox_2d": [836, 206, 893, 213], "page": 2}]
```

### 체크·도장·서명 `marks` · 채점 vl_f1 (값+위치)

틀 (질문의 항목 한 줄 · 답 항목 하나 · 빈 칸일 때) — `questions.json` 의 `marks`:

```
item:         - {key}: {label}{note}
answer:       {"key": "{key}", "value": "{value}", "bbox_2d": "{bbox_2d}", "page": "{page}"}
answer_empty: {"key": "{key}", "value": null}
```

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- check.과목: 과목 (체크박스, 보기: 무역어음대 / 수입신용장 발행 / 내국신용장 발행 / 보기4)
- check.자금용도: 자금용도 (체크박스, 보기: 생산자금 / 원자재구매자금 / 원자재수입자금 / 완제품구매자금 / 포괄금융)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.팀장: 팀장 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.팀장: 팀장 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.부점장: 부점장 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.부점장: 부점장 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.과목", "value": "무역어음대", "bbox_2d": [256, 361, 273, 373], "page": 1},
 {"key": "check.자금용도", "value": "생산자금", "bbox_2d": [656, 301, 673, 314], "page": 1},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": true, "bbox_2d": [729, 101, 795, 144], "page": 1},
 {"key": "seal.staff.팀장", "value": true, "bbox_2d": [806, 107, 850, 138], "page": 1},
 {"key": "sign.staff.팀장", "value": false},
 {"key": "seal.staff.부점장", "value": true, "bbox_2d": [867, 105, 917, 140], "page": 1},
 {"key": "sign.staff.부점장", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf154 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf154` → `python -m docgen.formdir card hf154` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | studio ① 서식 › 영역 편집에서 그리기 (`fields.json` items 에 한 칸) | 다시 |
| 답의 위치 (박스) | `fields.json` 그 칸의 `rect` [x0, y0, x1, y1] (pt) — 또는 영역 편집 | 다시 |
| 답의 키 | `fields.json` 그 칸에 `"key"` (없으면 규칙이 항목명으로 정함 — 모든 서식 공통 규칙은 studio 키 사전) | 다시 |
| 답의 값 | `fields.json` 그 칸에 `"source"` ([값 출처 목록](../_common/values.md)) 또는 값 종류 `"kind"` | 다시 |
| 칸의 항목명 | `fields.json` 그 칸의 `label` | 다시 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf154 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf154 --show` · `python -m docgen.preview hf154 --out work/hf154`
