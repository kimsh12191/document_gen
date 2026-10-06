# 하나은행 공개 서식 441건 — 템플릿 전수 분류 지도

`python scripts/form_map.py > docs/FORM_MAP.md` 로 자동 생성된다. 판정 기준은 [scripts/form_map.py](../scripts/form_map.py) 안의 표에 있다.

원본은 `add_template/하나은행_서식자료/` (하나은행 홈페이지 공개 서식). '기재란'·'보기'·'쪽' 은 `scripts/extract_form_fields.py` 가 PDF 에서 뽑아 `add_template/field_specs/` 에 넣은 수치다 — 서식을 만들 때의 작업지시서가 된다.

## 판정 구분

| 판정 | 뜻 | 건수 |
|---|---|---:|
| **기존** | 이미 만들어 둔 서류로 덮인다 (문구·변형 차이만 있다) | 88 |
| **P1** | 1차 신규 구현 — 수제 템플릿 | 10 |
| **P2** | 신규 그룹(퇴직연금·전자금융) 구현 — 수제 템플릿 | 10 |
| **P3** | 선언형 폼 스펙으로 넣는다 (공용 템플릿이 렌더) | 312 |
| **제외** | 템플릿화 대상 아님 (약관 전문·안내 인쇄물·내부 점검표 등) | 21 |
| | **합계** | **441** |

## 분류별 판정

| 분류 | 기존 | P1 | P2 | P3 | 제외 | 합계 | P3 스펙 모듈 |
|---|---:|---:|---:|---:|---:|---:|---|
| 예금 | 6 | 6 | 0 | 30 | 4 | 46 | `forms_deposit.py` |
| 대출 | 42 | 4 | 0 | 57 | 8 | 111 | `forms_loan.py` |
| 신탁/ISA | 1 | 0 | 0 | 5 | 0 | 6 | `forms_trust.py` |
| 퇴직연금 | 2 | 0 | 6 | 23 | 2 | 33 | `forms_retirement.py` |
| 펀드 | 0 | 0 | 0 | 2 | 0 | 2 | `forms_trust.py` |
| 외환 | 3 | 0 | 0 | 130 | 3 | 136 | `forms_fx.py` |
| 전자금융 | 10 | 0 | 4 | 31 | 1 | 46 | `forms_efinance.py` |
| 파생상품 | 2 | 0 | 0 | 20 | 3 | 25 | `forms_derivative.py` |
| 기타 | 22 | 0 | 0 | 14 | 0 | 36 | `forms_etc.py` |
| **합계** | **88** | **10** | **10** | **312** | **21** | **441** | |

기재란 추출: 433건에서 총 3779개 (서식당 평균 8.7개)

## 1차 구현 대상 (P1 · P2)

| No | 판정 | 서식명 | 만들 서류 | 쪽 | 기재란 | 비고 |
|---:|---|---|---|---:|---:|---|
| 1 | P1 | 상속예금 명의변경(지급) 의뢰서 및 손해담보 확약서(상속예금 지급 위임장 겸용) | `bank_form/inheritance_deposit_claim` | 2 | 6 | 상속예금 지급·명의변경 의뢰서 — bank_form_deposit.py |
| 11 | P1 | 예금(신탁)잔액증명 의뢰서 | `bank_form/balance_certificate_request` | 1 | 18 | 예금(신탁)잔액증명 의뢰서 — bank_form_deposit.py |
| 15 | P1 | 통합제신고서 | `bank_form/integrated_change_report` | 2 | 14 | 통합제신고서 — bank_form_deposit.py |
| 24 | P1 | 금융거래정보제공(요구·동의)서 | `bank_form/financial_info_disclosure` | 1 | 12 | 금융거래정보제공(요구·동의)서 — bank_form_deposit.py |
| 25 | P1 | 대여금고(신규·변경·해지)신청서 | `bank_form/safe_deposit_box_application` | 2 | 8 | 대여금고 신규·변경·해지 신청서 — bank_form_deposit.py |
| 28 | P1 | 위임장 | `bank_form/bank_power_of_attorney` | 1 | 11 | 위임장(은행 거래용) — bank_form_deposit.py |
| 51 | P1 | 대출계약 철회신청서 | `bank_form/loan_withdrawal_request` | 1 | 5 | 대출계약 철회신청서 — bank_form_loan2.py |
| 61 | P1 | 적합성, 적정성 고객정보 확인서(개인 및 개인사업자용) | `bank_form/suitability_check` | 1 | 15 | 적합성·적정성 고객정보 확인서(개인) — bank_form_loan2.py |
| 62 | P1 | 적합성, 적정성 고객정보 확인서(법인용) | `bank_form/suitability_check_corp` | 2 | 20 | 적합성·적정성 고객정보 확인서(법인) — bank_form_loan2.py |
| 63 | P1 | 대출상품설명서(권유용) | `bank_form/loan_product_description` | 6 | 4 | 대출상품설명서(권유용) — bank_form_loan2.py |
| 168 | P2 | 퇴직연금 사전지정운용방법 지정 신청서(디폴트옵션 지정) | `retirement/default_option_designation` | 2 | 7 | 퇴직연금 사전지정운용방법(디폴트옵션) 지정 신청서 |
| 169 | P2 | 퇴직연금 가입자 거래신청서(DC/기업형IRP) | `retirement/dc_participant_application` | 3 | 16 | 퇴직연금 가입자 거래신청서(DC·기업형IRP) |
| 171 | P2 | 퇴직연금 거래신청서(개인형IRP) | `retirement/irp_account_application` | 3 | 14 | 퇴직연금 거래신청서(개인형IRP) |
| 173 | P2 | 투자자확인서(퇴직연금용) | `retirement/investor_profile_retirement` | 2 | 0 | 투자자확인서(퇴직연금용) |
| 177 | P2 | 퇴직연금 운용상품지정 신청서(DC) | `retirement/dc_product_selection` | 1 | 22 | 퇴직연금 운용상품지정 신청서(DC) |
| 179 | P2 | 퇴직연금 퇴직급여 지급신청서(DB) | `retirement/retirement_benefit_claim` | 2 | 14 | 퇴직연금 퇴직급여 지급신청서(DB) |
| 335 | P2 | 하나 입출금 거래내역 문자통지서비스 신청서 | `efinance/sms_notice_application` | 4 | 24 | 입출금 거래내역 문자통지서비스 신청서 |
| 337 | P2 | 개인 전자금융 서비스 신청서 | `efinance/efinance_application_personal` | 3 | 13 | 개인 전자금융 서비스 신청서 |
| 340 | P2 | 기업 전자금융서비스 신청서(은행용) | `efinance/efinance_application_corp` | 2 | 41 | 기업 전자금융서비스 신청서(은행용) |
| 373 | P2 | 전자어음 교부 신청서 | `efinance/electronic_note_issue` | 1 | 7 | 전자어음 교부 신청서 |

## 전체 목록

### 예금 (46건)

| No | 서식명 | 형식 | 쪽 | 기재란 | 보기 | 판정 | 대상 | 비고 |
|---:|---|---|---:|---:|---:|---|---|---|
| 1 | [상속예금 명의변경(지급) 의뢰서 및 손해담보 확약서(상속예금 지급 위임장 겸용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2026/09/07/5-08-0084.pdf) | PDF | 2 | 6 | 13 | P1 | `bank_form/inheritance_deposit_claim` | 상속예금 지급·명의변경 의뢰서 — bank_form_deposit.py |
| 2 | [은행거래신청서(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2026/06/19/3-08-0026.pdf) | PDF | 2 | 47 | 0 | 기존 | `account_opening_application` | 영문 서식 변형 |
| 3 | [은행거래신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2026/06/19/3-08-1016.pdf) | PDF | 2 | 87 | 0 | 기존 | `account_opening_application` | 하나은행의 계좌개설 서식 본체 |
| 4 | [보호예수품 반환 의뢰서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2026/03/27/5-08-0776.pdf) | PDF | 1 | 6 | 1 | P3 | `forms_deposit` |  |
| 5 | [보호예수 의뢰서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2026/03/27/5-08-0026.pdf) | PDF | 1 | 10 | 3 | P3 | `forms_deposit` |  |
| 6 | [자동이체 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2025/11/27/3-11-0012.pdf) | PDF | 2 | 16 | 19 | 기존 | `auto_transfer_application` |  |
| 7 | [질권실행 의뢰서(수신_제3자 질권용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2025/10/29/5-08-0765.pdf) | PDF | 1 | 4 | 0 | P3 | `forms_deposit` |  |
| 8 | [질권해지 통지서(수신_제3자 질권용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2025/10/29/5-08-0099.pdf) | PDF | 1 | 4 | 0 | P3 | `forms_deposit` |  |
| 9 | [질권설정 승낙의뢰서(수신_제3자 질권용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2025/10/29/5-08-0075.pdf) | PDF | 1 | 4 | 0 | P3 | `forms_deposit` |  |
| 10 | [주식(사채)납입금 수납대행의뢰서(보관증명서 발급의뢰서 겸용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2025/05/15/5-08-0045_250516.pdf) | PDF | 1 | 8 | 5 | P3 | `forms_deposit` |  |
| 11 | [예금(신탁)잔액증명 의뢰서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2025/01/07/5-08-0094.pdf) | PDF | 1 | 18 | 12 | P1 | `bank_form/balance_certificate_request` | 예금(신탁)잔액증명 의뢰서 — bank_form_deposit.py |
| 12 | [보이스피싱 피해 예방 안내장](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2024/12/18/GuidesForPreventingVoicePhishing-20241216.pdf) | PDF | 2 | 1 | 0 | 제외 |  | 보이스피싱 피해 예방 안내 인쇄물 |
| 13 | [금융거래 목적 확인 안내장](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2024/08/29/240827-0283_1.pdf) | PDF | 1 | 2 | 0 | 제외 |  | 금융거래 목적 확인 안내 인쇄물 (서식 본체는 financial_transaction_purpose 로 이미 있다) |
| 14 | [금융거래 한도계좌 개설 안내장](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2024/08/29/240827-0284.pdf) | PDF | 1 | 1 | 0 | 제외 |  | 한도계좌 개설 안내 인쇄물 |
| 15 | [통합제신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2024/02/02/3-08-1280_240202.pdf) | PDF | 2 | 14 | 2 | P1 | `bank_form/integrated_change_report` | 통합제신고서 — bank_form_deposit.py |
| 16 | [종합금융상품 ON-LINE 거래 약정서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2023/07/26/5-08-0702.pdf) | PDF | 2 | 7 | 2 | P3 | `forms_deposit` |  |
| 17 | [종합금융상품 ON-LINE_거래 (이체)신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2023/07/26/5-08-0701.pdf) | PDF | 1 | 16 | 7 | P3 | `forms_deposit` |  |
| 18 | [본인계좌 일괄지급정지 조회신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2023/06/08/5-08-0690.pdf) | PDF | 4 | 2 | 12 | P3 | `forms_deposit` |  |
| 19 | [본인계좌 일괄지급정지(해제)신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2023/05/30/5-08-0691.pdf) | PDF | 1 | 3 | 0 | P3 | `forms_deposit` |  |
| 20 | [노무비닷컴계좌 개설 및 지급이체서비스 이용 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2022/07/26/5-08-0553_20220728_1.pdf) | PDF | 1 | 8 | 4 | P3 | `forms_deposit` |  |
| 21 | [일괄처리(지급)요청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2022/04/14/5-08-0591.pdf) | PDF | 1 | 2 | 31 | P3 | `forms_deposit` |  |
| 22 | [통합제신고서(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2022/02/09/3-08-0029.pdf) | PDF | 2 | 15 | 0 | 기존 | `integrated_change_report` | 영문 변형 — P1 서식과 같은 서식 |
| 23 | [하도급협력대금통장(상생결제 노무비) 지급이체서비스 이용신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2022/07/29/5-08-0552.pdf) | PDF | 1 | 8 | 3 | P3 | `forms_deposit` |  |
| 24 | [금융거래정보제공(요구·동의)서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2021/09/07/5-08-0016_200508.pdf) | PDF | 1 | 12 | 21 | P1 | `bank_form/financial_info_disclosure` | 금융거래정보제공(요구·동의)서 — bank_form_deposit.py |
| 25 | [대여금고(신규·변경·해지)신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2021/09/03/3-08-1282_210903.pdf) | PDF | 2 | 8 | 0 | P1 | `bank_form/safe_deposit_box_application` | 대여금고 신규·변경·해지 신청서 — bank_form_deposit.py |
| 26 | [[필수]개인(신용)정보 제3자 제공동의서(하나미소드림적금가입자용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2021/03/11/5-08-0440_20210311.pdf) | PDF | 1 | 0 | 6 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 27 | [위임장(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/07/01/5-08-0506_20200702.pdf) | PDF | 1 | 8 | 5 | 기존 | `bank_power_of_attorney` | 영문 변형 — P1 서식과 같은 서식 |
| 28 | [위임장](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/29/5_08_0041_20200601.pdf) | PDF | 1 | 11 | 2 | P1 | `bank_form/bank_power_of_attorney` | 위임장(은행 거래용) — bank_form_deposit.py |
| 29 | [사용인감계(금융계좌개설용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0056_200508.pdf) | PDF | 1 | 6 | 0 | P3 | `forms_deposit` |  |
| 30 | [국내원천소득 제한세율 적용신청서(외국법인용-영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0276_200508.pdf) | PDF | 2 | 11 | 0 | P3 | `forms_deposit` |  |
| 31 | [국내원천소득 제한세율 적용신청서(외국법인용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/3-08-1298_200508.pdf) | PDF | 2 | 13 | 0 | P3 | `forms_deposit` |  |
| 32 | [국내원천소득 제한세율 적용신청서(비거주자용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/3-08-1297_200508.pdf) | PDF | 2 | 11 | 0 | P3 | `forms_deposit` |  |
| 33 | [국내원천소득 제한세율 적용신청서(비거주자용-영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0177_200508.pdf) | PDF | 2 | 6 | 0 | P3 | `forms_deposit` |  |
| 34 | [확인서(잔액통보생략용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0067_200508.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_deposit` |  |
| 35 | [수표·어음용지 폐기신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0030_200508.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_deposit` |  |
| 36 | [예금(신탁) 이관 의뢰서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0038_200508.pdf) | PDF | 1 | 8 | 0 | P3 | `forms_deposit` |  |
| 37 | [위탁유가증권 반환청구서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0042_200508.pdf) | PDF | 1 | 1 | 0 | P3 | `forms_deposit` |  |
| 38 | [수표(어음)발행사실 확인의뢰서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0029_200508.pdf) | PDF | 1 | 1 | 0 | P3 | `forms_deposit` |  |
| 39 | [유가증권 수탁약정서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0043_200508.pdf) | PDF | 1 | 7 | 9 | P3 | `forms_deposit` |  |
| 40 | [고발장](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0013_200508.pdf) | PDF | 2 | 0 | 4 | 제외 |  | 고발장 — 은행이 수사기관에 내는 문서 |
| 41 | [사고신고 담보금 지급정지가처분담보금 처리를 위한 약정서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0001_200508.pdf) | PDF | 2 | 0 | 0 | P3 | `forms_deposit` |  |
| 42 | [사채원리금 지급대행 계약서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0027_200508.pdf) | PDF | 4 | 0 | 0 | P3 | `forms_deposit` |  |
| 43 | [세금우대종합저축(비과세저축) 제변경신고서(비과세공용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0155_200508.pdf) | PDF | 1 | 14 | 3 | P3 | `forms_deposit` |  |
| 44 | [예금(신탁) 양도승낙 의뢰서 및 양도승낙서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0037_200508.pdf) | PDF | 2 | 5 | 0 | P3 | `forms_deposit` |  |
| 45 | [야간금고입금의뢰서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0035_200508.pdf) | PDF | 2 | 14 | 0 | P3 | `forms_deposit` |  |
| 46 | [목돈을 불리는 통장 거래신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2013/08/19/20130819.pdf) | PDF | 2 | 8 | 4 | P3 | `forms_deposit` |  |

### 대출 (111건)

| No | 서식명 | 형식 | 쪽 | 기재란 | 보기 | 판정 | 대상 | 비고 |
|---:|---|---|---:|---:|---:|---|---|---|
| 47 | [대출상담 및 신청서(한국주택금융공사채권유동화목적 보금자리론용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2026/07/30/3-06-1104.pdf) | PDF | 2 | 38 | 0 | 기존 | `loan_application` | 보금자리론 상담·신청 변형 |
| 48 | [가계형소호 여신차입신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/10/20/b000005060519_20251020.pdf) | PDF | 2 | 23 | 1 | 기존 | `loan_application` | 가계형 소호 차입신청 변형 |
| 49 | [《개인》대출신청서(가계용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/10/20/5160178_20251020.pdf) | PDF | 2 | 22 | 1 | 기존 | `loan_application` | 가계 대출신청서 본체 |
| 50 | [[필수]개인(신용)정보 제3자 제공 동의서(토지분양대금 대출 약정_대구도시개발공사)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/07/24/daegu_250721.pdf) | PDF | 1 | 0 | 4 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 51 | [대출계약 철회신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/30/5-06-0681.pdf) | PDF | 1 | 5 | 2 | P1 | `bank_form/loan_withdrawal_request` | 대출계약 철회신청서 — bank_form_loan2.py |
| 52 | [[필수] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택전월세자금대출용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/23/5-06-0920.pdf) | PDF | 5 | 1 | 31 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 53 | [[필수] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택구입자금대출용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/23/5-06-0919.pdf) | PDF | 5 | 1 | 31 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 54 | [주택도시기금 대출 신청서(가계용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/23/5-16-0177.pdf) | PDF | 2 | 81 | 1 | 기존 | `loan_application` | 주택도시기금 가계 변형 |
| 55 | [주택도시기금 대출상담 및 신청서(내집마련 디딤돌 대출용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/23/5-16-0139.pdf) | PDF | 2 | 57 | 26 | 기존 | `loan_application` | 디딤돌 상담·신청 변형 |
| 56 | [[필수] 개인(신용)정보 제3자 제공 동의서(하나더넥스트 내집연금용_역모기지)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/05/23/20250526_01.pdf) | PDF | 1 | 8 | 5 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 57 | [근저당권설정비 계산서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/10/10/20241010.xls) | XLS |  |  |  | 제외 |  | 엑셀 계산 시트 — 서식이 아니다 |
| 58 | [융자상담 및 차입신청서(기업용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/10/10/3-06-0201_1.pdf) | PDF | 2 | 25 | 16 | 기존 | `loan_application_corp` | 기업 융자상담·차입신청 본체 |
| 59 | [개인(신용)정보 조회 동의서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/06/27/5-06-0548.pdf) | PDF | 2 | 0 | 19 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 60 | [[필수] 개인(신용)정보 수집이용 동의서(대출성상품 적합성적정성 판단용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/06/14/3-06-0151.pdf) | PDF | 1 | 0 | 8 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 61 | [적합성, 적정성 고객정보 확인서(개인 및 개인사업자용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/06/14/5-06-0967.pdf) | PDF | 1 | 15 | 12 | P1 | `bank_form/suitability_check` | 적합성·적정성 고객정보 확인서(개인) — bank_form_loan2.py |
| 62 | [적합성, 적정성 고객정보 확인서(법인용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/06/14/5-06-0970.pdf) | PDF | 2 | 20 | 16 | P1 | `bank_form/suitability_check_corp` | 적합성·적정성 고객정보 확인서(법인) — bank_form_loan2.py |
| 63 | [대출상품설명서(권유용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/12/14/3060148_231214.pdf) | PDF | 6 | 4 | 0 | P1 | `bank_form/loan_product_description` | 대출상품설명서(권유용) — bank_form_loan2.py |
| 64 | [대출정보 열람청구, 상환 및 말소접수 위임장(주택담보대출 대출이동서비스)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/12/08/5-16-0401.pdf) | PDF | 1 | 3 | 0 | P3 | `forms_loan` |  |
| 65 | [국토교통부 주택소유확인 시스템 등 이용 관련 [필수] 개인(신용)정보 수집·이용·제공 동의서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/06/13/5-06-0893.pdf) | PDF | 2 | 0 | 10 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 66 | [대출정보 열람청구 및 상환 위임장(대출이동서비스)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/05/31/5-16-0365_230531.pdf) | PDF | 1 | 4 | 0 | P3 | `forms_loan` |  |
| 67 | [[필수] 개인(신용)정보 수집 · 이용 동의서[대출이동서비스]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/05/31/5-16-0364_230531.pdf) | PDF | 1 | 0 | 6 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 68 | [계약 체결 이행 등을 위한 필수 동의서(개인금융성 신용보험용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/11/23/5060748_20221201.pdf) | PDF | 3 | 0 | 24 | P3 | `forms_loan` |  |
| 69 | [기업간결제 제신고(약정해지,변경) 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0568_220629.pdf) | PDF | 2 | 10 | 7 | P3 | `forms_loan` |  |
| 70 | [개별동산 담보 취득용 체크리스트](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/05/17/20220517_ab1.pdf) | PDF | 1 | 1 | 0 | 제외 |  | 은행 내부 점검표 — 고객 기재란이 없다 |
| 71 | [집합동산 담보 취득용 체크리스트](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/05/17/20220517_ab2.pdf) | PDF | 1 | 1 | 0 | 제외 |  | 은행 내부 점검표 — 고객 기재란이 없다 |
| 72 | [전자방식 외상매출채권 결제제도 이용신청서(외담대,동반성장론,e-안심팩토링대출용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0733_211203.pdf) | PDF | 2 | 19 | 9 | P3 | `forms_loan` |  |
| 73 | [[필수] 개인(신용)정보 제3자 제공 동의서(안전망대출Ⅱ)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/12/03/5-16-0313.pdf) | PDF | 1 | 0 | 7 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 74 | [[필수] 개인(신용)정보 제3자 제공 동의서(햇살론17)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/12/03/5-06-0913.pdf) | PDF | 1 | 0 | 7 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 75 | [기업신용평가 의뢰서 법인사업자용](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/11/16/5-06-0710.xls) | XLS |  |  |  | P3 | `forms_loan` | XLS 원본 — 레이아웃 근거 확인 필요 |
| 76 | [기업신용평가 의뢰서 개인사업자용](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/11/16/5-06-0711.xls) | XLS |  |  |  | P3 | `forms_loan` | XLS 원본 — 레이아웃 근거 확인 필요 |
| 77 | [[필수]개인(신용)정보 제3자 제공 동의서(토지분양대금대출약정_대전광역시,대전도시공사)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/09/29/5060981_20210924.pdf) | PDF | 1 | 0 | 4 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 78 | [통화전환 옵션부 외화대출 원화대출 전환신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/09/24/5-06-0147_210924.pdf) | PDF | 1 | 6 | 0 | P3 | `forms_loan` |  |
| 79 | [정보교환 기업구매자금어음금 미결제통보확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0429_210924.pdf) | PDF | 1 | 1 | 0 | P3 | `forms_loan` |  |
| 80 | [정보교환 기업구매자금어음 부도통보확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0428_210924.pdf) | PDF | 1 | 1 | 0 | P3 | `forms_loan` |  |
| 81 | [정보교환 기업구매자금어음 인수거절통보확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0427_210924.pdf) | PDF | 1 | 1 | 0 | P3 | `forms_loan` |  |
| 82 | [채권발행 등록 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0978_210917.pdf) | PDF | 2 | 2 | 0 | P3 | `forms_loan` |  |
| 83 | [전자방식 외상매출채권 결제제도 이용신청서 (서울시농수산식품공사용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0898_210917.pdf) | PDF | 1 | 17 | 4 | P3 | `forms_loan` |  |
| 84 | [외상매출채권 양도통지서(장래채권양도통지용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0406.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_loan` |  |
| 85 | [신용정보 제공 동의서(외담대,e-안심팩토링,동반성장론 구매기업용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0906.pdf) | PDF | 1 | 0 | 4 | 기존 | `privacy_consent` | 동의서 변형 |
| 86 | [미래채권담보대출 협력기업 일괄추천서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0404.pdf) | PDF | 1 | 1 | 0 | P3 | `forms_loan` |  |
| 87 | [미래채권담보대출 추천서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0417.pdf) | PDF | 1 | 3 | 0 | P3 | `forms_loan` |  |
| 88 | [기업구매자금어음 추심취소 및 반환의뢰서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0293.pdf) | PDF | 1 | 4 | 0 | P3 | `forms_loan` |  |
| 89 | [외상매출채권 양도통지서(e-안심팩토링대출용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0579.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_loan` |  |
| 90 | [납품대금 선입금(벤더입금) 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0564.pdf) | PDF | 2 | 6 | 4 | P3 | `forms_loan` |  |
| 91 | [기업구매자금 결제제도 이용 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0585.pdf) | PDF | 1 | 19 | 0 | P3 | `forms_loan` |  |
| 92 | [외상매출채권양도통지서(개별채권양도통지용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0546.pdf) | PDF | 2 | 0 | 0 | P3 | `forms_loan` |  |
| 93 | [미결제 전자채권대금 입금확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0641.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_loan` |  |
| 94 | [상생벤더구매론 승인명세 등록신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0615.pdf) | PDF | 2 | 2 | 0 | P3 | `forms_loan` |  |
| 95 | [벤더승인명세 등록 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0614.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_loan` |  |
| 96 | [발주명세 등록신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0613.pdf) | PDF | 2 | 2 | 0 | P3 | `forms_loan` |  |
| 97 | [미래채권 대출신청서(미래대,상생미래대용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0612.pdf) | PDF | 1 | 1 | 0 | P3 | `forms_loan` |  |
| 98 | [기업구매자금어음 지급제시 명세](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0195.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_loan` |  |
| 99 | [지급승인명세 등록 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0565_210917.pdf) | PDF | 2 | 2 | 0 | P3 | `forms_loan` |  |
| 100 | [창구대출신청서(전자채권담보대출용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0269_210917.pdf) | PDF | 1 | 0 | 0 | 기존 | `loan_application` | 창구대출신청서 변형 |
| 101 | [전자방식 외상매출채권담보대출 통합약정서 중요내용 설명서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0687_210917.pdf) | PDF | 4 | 0 | 0 | 제외 |  | 설명 인쇄물 |
| 102 | [기업현황서(B2B전자결제서비스 업무, MP용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0653.pdf) | PDF | 5 | 33 | 0 | P3 | `forms_loan` |  |
| 103 | [B2B 전자결제서비스 업무 이용신청서(MP용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0652.pdf) | PDF | 2 | 31 | 0 | P3 | `forms_loan` |  |
| 104 | [기업구매자금어음 추심의뢰서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0196.pdf) | PDF | 1 | 3 | 0 | P3 | `forms_loan` |  |
| 105 | [전자채권미결제 확인의뢰서 및 확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0259_210917.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_loan` |  |
| 106 | [기업구매자금어음(기업구매자금용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0292.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_loan` |  |
| 107 | [기업구매자금대출 연장신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0426.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_loan` |  |
| 108 | [외상매출채권 대출신청서(외담대,e-안심팩토링대출 겸용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0581.pdf) | PDF | 1 | 2 | 0 | P3 | `forms_loan` |  |
| 109 | [전자채권사고신고(취하)서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0261_210917.pdf) | PDF | 1 | 9 | 1 | P3 | `forms_loan` |  |
| 110 | [전자방식 외상매출채권 발행취소 신청서(외담대,e-안심팩토링용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2022/07/29/5-06-0550_210917.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_loan` |  |
| 111 | [《개인》위임장(해외체제자 담보대출용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/08/31/Loan_form02.pdf) | PDF | 1 | 9 | 0 | P3 | `forms_loan` |  |
| 112 | [[필수]개인(신용)정보 제공동의서(서민맞춤대출용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/03/11/5-16-0156_20210311.pdf) | PDF | 1 | 0 | 4 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 113 | [개인(신용)정보 수집.이용 및 제공 동의서[필수적 동의](적격대출용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/03/02/5-16-0112_20210302.pdf) | PDF | 5 | 1 | 41 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 114 | [개인(신용)정보 수집.이용 제공 동의서(주택보유수 확인등)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/03/02/5-06-0813_20210302.pdf) | PDF | 2 | 0 | 10 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 115 | [[필수] 개인(신용)정보 수집이용, 제공 동의서(핀크생활비대출용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/03/02/5-06-0857_20210302_2.pdf) | PDF | 2 | 1 | 11 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 116 | [[필수] 개인(신용)정보 수집이용, 제공 동의서(공무원대출)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/03/02/5-16-0136_20210302_2.pdf) | PDF | 2 | 1 | 14 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 117 | [[필수] 개인(신용)정보 수집이용, 제공 동의서(군인생활안정자금)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/03/02/5-06-0820_20210302_2.pdf) | PDF | 2 | 1 | 10 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 118 | [[필수] 개인(신용)정보 수집·이용·제공_동의서[가계여신_금융거래]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/03/02/5-16-0179_20210302.pdf) | PDF | 2 | 1 | 20 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 119 | [필수 개인(신용)정보_수집·이용·제공_동의서[하나_사잇돌_중금리대출용]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/02/23/pdf_sw_20210223.pdf) | PDF | 2 | 0 | 10 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 120 | [필수 개인(신용)정보수집·이용및제공동의서(하나원클릭모기지,원클릭전세론,e금리고정형적격)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/02/23/pdf_sw_20210223_01.pdf) | PDF | 4 | 1 | 22 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 121 | [[필수] 개인(신용)정보 제3차 제공 동의서(우량주택전세론,군간부전세자금대출)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/02/08/5-16-0259_210205.pdf) | PDF | 1 | 0 | 4 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 122 | [[필수] 개인(신용)정보 수집·이용 및 제공 동의서(전세자금대출 권리보험가입용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/02/08/5-16-0241_210205.pdf) | PDF | 2 | 1 | 10 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 123 | [[필수] 개인(신용)정보 수집·이용 동의서 [전세자금대출-주택금융보증서용]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/02/08/5-16-0180_210205.pdf) | PDF | 1 | 0 | 4 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 124 | [[필수] 개인(신용)정보 처리 동의서(전세자금대출 권리보험가입용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/02/08/5-16-0238_210205.pdf) | PDF | 3 | 0 | 8 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 125 | [[필수] 개인(신용)정보 수집·이용 및 제공동의서[군간부전세자금대출기본),군간부월세자금대출]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/02/08/5-16-0235_210205.pdf) | PDF | 2 | 1 | 12 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 126 | [[필수] 상품별 개인(신용)정보 수집·이용·제공 동의서[목돈안드는 행복전세,목돈 안다는 드림전세(집주인담보대출)용]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/02/08/5-16-0132_210205.pdf) | PDF | 2 | 2 | 18 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 127 | [상품별 필수 개인(신용)정보 제공동의서(하나V-Plus대출)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/08/20/5160313_210820.pdf) | PDF | 1 | 0 | 7 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 128 | [필수 개인(신용)정보 수집, 이용 및 제공 동의서(소호여신)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/02/25/5_06_0724.pdf) | PDF | 2 | 1 | 20 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 129 | [필수 개인(신용)정보 수집, 이용 및 제공 동의서(법인여신)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/02/25/5-06-0734.pdf) | PDF | 2 | 1 | 20 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 130 | [기업가치 및 기업정보 제공활용 동의서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/08/20/5160313_210820_2.pdf) | PDF | 1 | 0 | 0 | 기존 | `privacy_consent` | 동의서 변형 |
| 131 | [전세자금대출 이용 확약서(서울보증보험증권 담보 전세자금대출용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2020/07/10/5-06-0943.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_loan` |  |
| 132 | [다주택처분확약서(서울보증보험)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2020/07/02/5-06-0896.pdf) | PDF | 1 | 2 | 0 | P3 | `forms_loan` |  |
| 133 | [금융거래 정보제공 동의서(연대보증 면제 신용보증서 담보대출용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2020/01/13/5-06-0876.pdf) | PDF | 1 | 0 | 0 | 기존 | `privacy_consent` | 동의서 변형 |
| 134 | [개인(신용)정보 수집.이용 동의서(매도인,무상거주인등 제3자용)(적격대출용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2017/10/20/pdf_sw_20171020_03.pdf) | PDF | 1 | 3 | 9 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 135 | [동의서(대출비용지급용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/04/19/5-06-0738_20170922.pdf) | PDF | 1 | 0 | 2 | P3 | `forms_loan` |  |
| 136 | [《기업》차입신청서(한도내 개별/분할실행용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2017/03/17/5060330_20170317.pdf) | PDF | 1 | 1 | 1 | 기존 | `loan_application_corp` | 한도 내 개별·분할실행 변형 |
| 137 | [대출금 분할실행 신청서(에듀큐론용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/20/5-06-0135.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_loan` |  |
| 138 | [대출금 수령위임동의서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5-06-0741_20150901.pdf) | PDF | 1 | 3 | 5 | P3 | `forms_loan` |  |
| 139 | [《기업》 지급보증거래 신청서(서면.전자 지급보증 겸용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5060703_20160707.pdf) | PDF | 1 | 12 | 0 | P3 | `forms_loan` |  |
| 140 | [매출채권 잔액 확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/document4_20160707.pdf) | PDF | 1 | 12 | 0 | P3 | `forms_loan` |  |
| 141 | [매출채권 잔액 확인서(사전확인용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/document3_20160707.pdf) | PDF | 1 | 12 | 0 | P3 | `forms_loan` |  |
| 142 | [매출채권설정등기통지서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/document2_20160707.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_loan` |  |
| 143 | [기업여신과목분류표](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/document1_20160707.pdf) | PDF | 1 | 21 | 0 | 제외 |  | 기업여신과목분류표 — 내부 분류표 |
| 144 | [동산담보 제공 예정내역서(개별동산용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/20160707_a1.pdf) | PDF | 1 | 2 | 0 | P3 | `forms_loan` |  |
| 145 | [동산담보 제공 예정내역서(집합동산용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/20160707_a2.pdf) | PDF | 1 | 2 | 0 | P3 | `forms_loan` |  |
| 146 | [동산담보물 관리대장](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/20160707_a3.pdf) | PDF | 1 | 3 | 0 | 제외 |  | 영업점 관리대장 — 고객 서식이 아니다 |
| 147 | [담보물 관리 체크리스트(개별동산용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/20160707_a6.pdf) | PDF | 1 | 6 | 0 | 제외 |  | 은행 내부 점검표 — 고객 기재란이 없다 |
| 148 | [담보물 관리 체크리스트(집합동산용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/20160707_a7.pdf) | PDF | 1 | 6 | 0 | 제외 |  | 은행 내부 점검표 — 고객 기재란이 없다 |
| 149 | [《기업》금융거래확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5060189_20160707.pdf) | PDF | 2 | 11 | 0 | P3 | `forms_loan` |  |
| 150 | [《기업》근저당권유용합의서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5060015_20160707.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_loan` |  |
| 151 | [《기업》무역어음인수·할인신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5060381_20160707.pdf) | PDF | 1 | 6 | 0 | P3 | `forms_loan` |  |
| 152 | [《기업》연대보증인(교체·면제)증서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5060451_20160707.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_loan` |  |
| 153 | [《기업》질권설정등록청구서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5060457_20160707.pdf) | PDF | 1 | 0 | 4 | P3 | `forms_loan` |  |
| 154 | [차입신청서(무역금융용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/3090174_20160707.pdf) | PDF | 2 | 66 | 5 | 기존 | `loan_application_corp` | 무역금융 차입신청 변형 |
| 155 | [채권양도통지서(외국법인용)(K-biz파트너론)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/06/03/FORM_K-biz.pdf) | PDF | 1 | 2 | 0 | P3 | `forms_loan` |  |
| 156 | [기업신용평가 의뢰서 기타단체용](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/08/13/creditform_orther_210813.xls) | XLS |  |  |  | P3 | `forms_loan` | XLS 원본 — 레이아웃 근거 확인 필요 |
| 157 | [여신거래용 인감명판 등 신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5090002_20160707.pdf) | PDF | 1 | 4 | 0 | P3 | `forms_loan` |  |

### 신탁/ISA (6건)

| No | 서식명 | 형식 | 쪽 | 기재란 | 보기 | 판정 | 대상 | 비고 |
|---:|---|---|---:|---:|---:|---|---|---|
| 158 | [위임장(하나골드신탁 만기 연장 접수용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070107/__icsFiles/afieldfile/2026/07/29/5-14-0298.pdf) | PDF | 1 | 6 | 3 | P3 | `forms_trust` |  |
| 159 | [[필수] 개인(신용)정보 수집·이용 동의서(일임형ISA)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070107/__icsFiles/afieldfile/2025/08/29/3-21-0004_20210510.pdf) | PDF | 1 | 0 | 5 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 160 | [계약대상자확인서(일임형ISA용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070107/__icsFiles/afieldfile/2024/08/20/3-14-0034_20240821.pdf) | PDF | 2 | 4 | 0 | P3 | `forms_trust` |  |
| 161 | [위임장 (특정금전신탁용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070107/__icsFiles/afieldfile/2023/12/18/5-14-0062.pdf) | PDF | 1 | 6 | 2 | P3 | `forms_trust` |  |
| 162 | [ISA계약만기연장 확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070107/__icsFiles/afieldfile/2021/08/26/5210001_20210706.pdf) | PDF | 2 | 6 | 0 | P3 | `forms_trust` |  |
| 163 | [위임장(일임형 개인종합자산관리계좌(ISA)용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070107/__icsFiles/afieldfile/2021/08/26/5210001_20210115.pdf) | PDF | 1 | 6 | 3 | P3 | `forms_trust` |  |

### 퇴직연금 (33건)

| No | 서식명 | 형식 | 쪽 | 기재란 | 보기 | 판정 | 대상 | 비고 |
|---:|---|---|---:|---:|---:|---|---|---|
| 164 | [퇴직연금 퇴직급여 지급신청서(DC,기업형IRP)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2026/09/18/5-14-0037.pdf) | PDF | 2 | 16 | 17 | P3 | `forms_retirement` |  |
| 165 | [퇴직연금 계약이전신청서(DB)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2026/06/22/5-14-0022.pdf) | PDF | 2 | 11 | 12 | P3 | `forms_retirement` |  |
| 166 | [퇴직연금 계약이전신청서(DC)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2026/06/22/5-14-0196.pdf) | PDF | 2 | 11 | 15 | P3 | `forms_retirement` |  |
| 167 | [퇴직연금 사전지정운용제도 신청서(디폴트옵션, 기업용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2026/06/22/5-20-0027.pdf) | PDF | 1 | 4 | 2 | P3 | `forms_retirement` |  |
| 168 | [퇴직연금 사전지정운용방법 지정 신청서(디폴트옵션 지정)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2026/06/22/5-20-0026.pdf) | PDF | 2 | 7 | 10 | P2 | `retirement/default_option_designation` | 퇴직연금 사전지정운용방법(디폴트옵션) 지정 신청서 |
| 169 | [퇴직연금 가입자 거래신청서(DC/기업형IRP)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2026/06/22/5-20-0025_1.pdf) | PDF | 3 | 16 | 18 | P2 | `retirement/dc_participant_application` | 퇴직연금 가입자 거래신청서(DC·기업형IRP) |
| 170 | [퇴직연금 계약이전 신청서(기업형IRP)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2026/06/22/5-14-0140.pdf) | PDF | 1 | 11 | 9 | 기존 | `retirement/dc_participant_application` | 기업형IRP 계약이전 변형 |
| 171 | [퇴직연금 거래신청서(개인형IRP)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2026/06/22/5-14-0020.pdf) | PDF | 3 | 14 | 20 | P2 | `retirement/irp_account_application` | 퇴직연금 거래신청서(개인형IRP) |
| 172 | [퇴직연금 거래신청서(DC, 기업형IRP)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2026/06/22/5-14-0121.pdf) | PDF | 4 | 24 | 27 | P3 | `forms_retirement` |  |
| 173 | [투자자확인서(퇴직연금용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2026/06/01/5-14-0134.pdf) | PDF | 2 | 0 | 14 | P2 | `retirement/investor_profile_retirement` | 투자자확인서(퇴직연금용) |
| 174 | [퇴직연금 계약이전 동의서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2026/04/29/5-20-0004.pdf) | PDF | 1 | 3 | 44 | P3 | `forms_retirement` |  |
| 175 | [퇴직연금 AI 포트폴리오 설계(신규 리밸런싱)신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2025/11/27/5-20-0041_2.pdf) | PDF | 1 | 8 | 3 | P3 | `forms_retirement` |  |
| 176 | [퇴직연금 퇴직급여 지급신청서(DC,기업형IRP)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2025/10/14/5-14-0037.pdf) | PDF | 2 | 16 | 17 | P3 | `forms_retirement` |  |
| 177 | [퇴직연금 운용상품지정 신청서(DC)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2025/08/27/5-14-0120.pdf) | PDF | 1 | 22 | 1 | P2 | `retirement/dc_product_selection` | 퇴직연금 운용상품지정 신청서(DC) |
| 178 | [퇴직연금 입금예정상품등록/변경 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2025/08/27/5-14-0016.pdf) | PDF | 2 | 12 | 11 | P3 | `forms_retirement` |  |
| 179 | [퇴직연금 퇴직급여 지급신청서(DB)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2025/05/30/5-14-0036_20250530.pdf) | PDF | 2 | 14 | 12 | P2 | `retirement/retirement_benefit_claim` | 퇴직연금 퇴직급여 지급신청서(DB) |
| 180 | [DB 적립금 이전 요청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2024/12/23/5-20-0021.pdf) | PDF | 1 | 2 | 0 | P3 | `forms_retirement` |  |
| 181 | [이전 가입자 명부(DC,기업형 IRP용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2024/12/23/5-20-0012.pdf) | PDF | 1 | 4 | 0 | P3 | `forms_retirement` |  |
| 182 | [이전신청(취소)서(DB,DC,기업형IRP 이전용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2024/12/23/5-20-0011.pdf) | PDF | 1 | 13 | 9 | P3 | `forms_retirement` |  |
| 183 | [퇴직연금 통지서비스 신청서(가입자용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2024/10/02/5-14-0128.pdf) | PDF | 2 | 20 | 15 | P3 | `forms_retirement` |  |
| 184 | [퇴직연금 계약해지 신청서(개인형IRP)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2024/07/18/5-14-0044.pdf) | PDF | 1 | 9 | 2 | P3 | `forms_retirement` |  |
| 185 | [퇴직연금 DC 기업부담금 자동이체 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2024/05/02/5-14-0124.pdf) | PDF | 2 | 8 | 1 | P3 | `forms_retirement` |  |
| 186 | [퇴직연금_거래신청서(DB)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2024/04/02/5-20-0028.pdf) | PDF | 2 | 19 | 0 | 기존 | `retirement/dc_participant_application` | DB 거래신청 변형 |
| 187 | [퇴직연금 금융투자상품 상품설명서(핵심 요약)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2024/03/04/5-20-0018.pdf) | PDF | 8 | 10 | 2 | 제외 |  | 상품설명 인쇄물 |
| 188 | [퇴직연금 중도인출신청서(DC,기업형·개인형IRP)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2024/01/31/5-14-0021_240131.pdf) | PDF | 4 | 24 | 39 | P3 | `forms_retirement` |  |
| 189 | [퇴직연금 부담금 등록 신청서(DC,기업형IRP)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2024/01/31/5-14-0015_240131.pdf) | PDF | 1 | 7 | 6 | P3 | `forms_retirement` |  |
| 190 | [금융투자상품 판매점검 체크리스트(퇴직연금용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2023/04/28/5-20-0015.pdf) | PDF | 1 | 15 | 0 | 제외 |  | 은행 내부 점검표 — 고객 기재란이 없다 |
| 191 | [퇴직연금 계약해지 신청서(DB,DC)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2023/05/09/5-14-0040.pdf) | PDF | 1 | 16 | 15 | P3 | `forms_retirement` |  |
| 192 | [퇴직연금 통지서비스 신청서(기업용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2023/02/17/5-14-0127.pdf) | PDF | 2 | 8 | 10 | P3 | `forms_retirement` |  |
| 193 | [퇴직연금 계약해지 신청서(기업형IRP)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2022/12/30/5-14-0139_230102.pdf) | PDF | 1 | 9 | 10 | P3 | `forms_retirement` |  |
| 194 | [퇴직연금 항목등록/변경 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2022/12/30/5-14-0129.pdf) | PDF | 2 | 19 | 16 | P3 | `forms_retirement` |  |
| 195 | [퇴직연금 가입자(등록·변경·삭제) 신청서(DB,DC,기업형IRP)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2020/11/16/5-14-0119_201029.pdf) | PDF | 1 | 7 | 41 | P3 | `forms_retirement` |  |
| 196 | [기업형IRP 가입대상 근로자 확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070108/__icsFiles/afieldfile/2020/04/09/5-14-0111_200331.pdf) | PDF | 1 | 2 | 0 | P3 | `forms_retirement` |  |

### 펀드 (2건)

| No | 서식명 | 형식 | 쪽 | 기재란 | 보기 | 판정 | 대상 | 비고 |
|---:|---|---|---:|---:|---:|---|---|---|
| 197 | [위임장(집합투자증권 및 연금저축계좌 투자용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070109/__icsFiles/afieldfile/2021/08/19/3-14-0231_20210819.pdf) | PDF | 1 | 6 | 1 | P3 | `forms_trust` |  |
| 198 | [공모부동산집합투자증권 과세특례신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070109/__icsFiles/afieldfile/2021/01/15/5190014_20210104.pdf) | PDF | 2 | 0 | 0 | P3 | `forms_trust` |  |

### 외환 (136건)

| No | 서식명 | 형식 | 쪽 | 기재란 | 보기 | 판정 | 대상 | 비고 |
|---:|---|---|---:|---:|---:|---|---|---|
| 199 | [외화송금신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/06/02/3-09-0131_260602.pdf) | PDF | 2 | 16 | 24 | 기존 | `overseas_remittance_application` | 해외송금 본체 |
| 200 | [외화송금신청서(2D)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/06/02/HanaBank2DSetup.exe) | EXE |  |  |  | 제외 |  | EXE(서식 뷰어 설치파일) — 서식 원본이 아니다 |
| 201 | [거래외국환지정(변경)신청서(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/02/25/5-09-0450_260225.pdf) | PDF | 1 | 1 | 0 | P3 | `forms_fx` |  |
| 202 | [거래외국환지정(변경)신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/02/25/3-09-1048_260225.pdf) | PDF | 1 | 1 | 0 | P3 | `forms_fx` |  |
| 203 | [주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/02/20/5-29-0206_1.pdf) | PDF | 4 | 11 | 2 | P3 | `forms_fx` |  |
| 204 | [주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(국문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/02/20/5-29-0206_2.pdf) | PDF | 4 | 23 | 2 | P3 | `forms_fx` |  |
| 205 | [외국환거래법시행령상 거주성확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/02/09/5-09-0545.pdf) | PDF | 3 | 10 | 4 | P3 | `forms_fx` |  |
| 206 | [연간사업실적보고서(투자잔액 1,000만불 초과 기업)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/02/09/5-09-0201.pdf) | PDF | 6 | 64 | 22 | P3 | `forms_fx` |  |
| 207 | [연간사업실적보고서(투자잔액 300만불 초과 1,000만불 이하 기업)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/02/09/5-09-0023.pdf) | PDF | 5 | 55 | 22 | P3 | `forms_fx` |  |
| 208 | [지급확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/02/09/5-09-0365.pdf) | PDF | 1 | 4 | 0 | P3 | `forms_fx` |  |
| 209 | [영수확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/02/09/5-09-0343_260209.pdf) | PDF | 1 | 8 | 0 | P3 | `forms_fx` |  |
| 210 | [대북투자 신고 및 투자실적 보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/02/09/5-09-0334.pdf) | PDF | 2 | 5 | 0 | P3 | `forms_fx` |  |
| 211 | [사업계획서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/02/09/5-09-0191.pdf) | PDF | 4 | 49 | 19 | P3 | `forms_fx` |  |
| 212 | [해외직접투자 신고서(보고서)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2025/12/31/5-09-0290.pdf) | PDF | 2 | 23 | 0 | P3 | `forms_fx` |  |
| 213 | [사전 송금방식 수입대금 지급시](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2025/04/16/5-09-0519.pdf) | PDF | 1 | 1 | 9 | P3 | `forms_fx` |  |
| 214 | [자본거래 사후보고 확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2025/04/16/5-09-0528.pdf) | PDF | 1 | 5 | 1 | P3 | `forms_fx` |  |
| 215 | [상호계산계정 결산대차기잔액처분(변경)신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2025/04/16/5-09-0193.pdf) | PDF | 1 | 6 | 0 | P3 | `forms_fx` |  |
| 216 | [해외부동산 취득신고(수리)서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2025/04/16/5-09-0292.pdf) | PDF | 2 | 20 | 4 | P3 | `forms_fx` |  |
| 217 | [해외직접투자 내용변경 신고(보고)서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2025/04/16/5-09-0289.pdf) | PDF | 2 | 2 | 1 | P3 | `forms_fx` |  |
| 218 | [서약서(개인의 외국주택 취득)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2025/04/16/5-09-0272.pdf) | PDF | 2 | 0 | 0 | P3 | `forms_fx` |  |
| 219 | [해외사무소 설치(변경)신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2025/04/16/5-09-0271.pdf) | PDF | 2 | 24 | 2 | P3 | `forms_fx` |  |
| 220 | [해외지점 설치(변경)신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2025/04/16/5-09-0270.pdf) | PDF | 2 | 24 | 2 | P3 | `forms_fx` |  |
| 221 | [해외지사 설치·현황 보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2025/04/16/5-09-0213.pdf) | PDF | 2 | 1 | 0 | P3 | `forms_fx` |  |
| 222 | [해외 부동산 취득 보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2025/04/16/5-09-0211.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_fx` |  |
| 223 | [「외국환서식관리프로그램」전자무역업무이용(신규,변경,해지)신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2025/01/16/5-09-0054_170831_1.pdf) | PDF | 4 | 28 | 27 | P3 | `forms_fx` |  |
| 224 | [Usance 송금 조건변경신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2023/11/10/5-09-0515.pdf) | PDF | 1 | 13 | 2 | P3 | `forms_fx` |  |
| 225 | [Usance 송금 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2023/11/10/5-09-0516.pdf) | PDF | 1 | 36 | 5 | P3 | `forms_fx` |  |
| 226 | [거주자의 외화자금 차입 및 상환 현황보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2023/10/13/5-09-0318.pdf) | PDF | 2 | 6 | 0 | P3 | `forms_fx` |  |
| 227 | [거주자의 해외 증권발행 및 상환 현황 보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2023/10/13/5-09-0317_1.pdf) | PDF | 2 | 7 | 0 | P3 | `forms_fx` |  |
| 228 | [담보제공신고(보고)서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2023/09/07/5-09-0274.pdf) | PDF | 1 | 16 | 4 | P3 | `forms_fx` |  |
| 229 | [매매신고(보고)서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2023/09/07/5-09-0276.pdf) | PDF | 1 | 12 | 0 | P3 | `forms_fx` |  |
| 230 | [보증계약신고(보고)서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2023/09/07/5-09-0277.pdf) | PDF | 1 | 14 | 6 | P3 | `forms_fx` |  |
| 231 | [현지금융 차입·상환·보증등 한도 운영현황 보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2023/09/07/5-09-0342.pdf) | PDF | 1 | 5 | 0 | P3 | `forms_fx` |  |
| 232 | [증권발행 신고(보고)서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2023/09/07/5-09-0286.pdf) | PDF | 1 | 24 | 0 | P3 | `forms_fx` |  |
| 233 | [금전의 대차계약 신고(보고)서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2023/09/07/5-09-0273_1.pdf) | PDF | 1 | 15 | 0 | P3 | `forms_fx` |  |
| 234 | [외화송금의 내용변경 및 취소, 송금수표 분실신고 등 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2022/12/21/5-09-0064.pdf) | PDF | 1 | 16 | 3 | P3 | `forms_fx` |  |
| 235 | [외국인투자기업등록(변경등록)신청서(국문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2022/11/11/5_09_0206_8.pdf) | PDF | 3 | 27 | 1 | P3 | `forms_fx` |  |
| 236 | [해외예금 및 신탁 잔액 보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2022/01/24/5-09-0212.pdf) | PDF | 1 | 19 | 0 | P3 | `forms_fx` |  |
| 237 | [해외예금 입금보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2022/01/24/5-09-0363.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_fx` |  |
| 238 | [해외직접투자사업 청산 및 대부채권 회수보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2022/01/25/5-09-0215.pdf) | PDF | 3 | 12 | 4 | P3 | `forms_fx` |  |
| 239 | [해외 부동산 처분(변경)신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2022/01/24/5-09-0210.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_fx` |  |
| 240 | [외화증권(채권)취득보고서(법인 및 개인기업 설립보고서 포함)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2022/01/24/5-09-0206.pdf) | PDF | 2 | 23 | 7 | P3 | `forms_fx` |  |
| 241 | [대외지급보증 조건변경 신청서(SWIFT 방식)(2D)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2022/01/20/5-09-0505.pdf) | PDF | 2 | 0 | 1 | P3 | `forms_fx` |  |
| 242 | [대외지급보증 발급 신청서(SWIFT 방식)(2D)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2022/01/20/5-09-0504.pdf) | PDF | 3 | 0 | 1 | P3 | `forms_fx` |  |
| 243 | [외국환거래 UMS통지서비스 (변경)신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2021/12/22/5-09-0049_211222.pdf) | PDF | 1 | 17 | 11 | P3 | `forms_fx` |  |
| 244 | [자본재 등 도입물품명세 검토ㆍ확인신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2021/07/20/5-09-0173_1.pdf) | PDF | 3 | 2 | 0 | P3 | `forms_fx` |  |
| 245 | [장기차관 방식의 외국인투자신고서, 변경신고서(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2021/07/20/5-09-0486_1.pdf) | PDF | 2 | 11 | 0 | P3 | `forms_fx` |  |
| 246 | [장기차관 방식의 외국인투자신고서, 변경신고서(국문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2021/07/20/5-09-0486_2.pdf) | PDF | 2 | 14 | 2 | P3 | `forms_fx` |  |
| 247 | [외국인투자기업등록(변경등록)신청서(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2021/08/13/5_09_0206_7.pdf) | PDF | 3 | 16 | 1 | P3 | `forms_fx` |  |
| 248 | [주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2025/03/07/5-09-0433.pdf) | PDF | 2 | 3 | 0 | P3 | `forms_fx` |  |
| 249 | [주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(국문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2021/07/20/5_09_0206_4_1.pdf) | PDF | 2 | 9 | 0 | P3 | `forms_fx` |  |
| 250 | [[필수] 개인(신용)정보 수집 이용 동의서(외투용)_영문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2021/03/12/5-09-0163.pdf) | PDF | 1 | 0 | 5 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 251 | [[필수] 개인(신용)정보 수집 이용 동의서(외투용)_국문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2021/03/12/5-09-0162.pdf) | PDF | 1 | 0 | 5 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 252 | [외국환 신고(확인)필증](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2020/12/17/5-09-0377.pdf) | PDF | 1 | 9 | 0 | P3 | `forms_fx` |  |
| 253 | [( ) 변경신고(수리)서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2020/12/17/5-09-0188.pdf) | PDF | 1 | 4 | 0 | P3 | `forms_fx` |  |
| 254 | [금전의 대차계약 신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2020/09/17/5-09-0319.pdf) | PDF | 1 | 18 | 6 | P3 | `forms_fx` |  |
| 255 | [자(손자)회사 사업계획서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2020/09/17/5-09-0207.pdf) | PDF | 2 | 34 | 7 | P3 | `forms_fx` |  |
| 256 | [외국환업무 등록 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2020/08/12/5-09-0376.pdf) | PDF | 1 | 18 | 0 | P3 | `forms_fx` |  |
| 257 | [환전장부](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2020/08/12/5-09-0373.pdf) | PDF | 1 | 8 | 0 | 제외 |  | 영업점 장부 |
| 258 | [환전업무 등록신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2020/08/12/5-09-0371.pdf) | PDF | 1 | 9 | 3 | P3 | `forms_fx` |  |
| 259 | [환전업무 등록내용 변경 신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2020/08/12/5-09-0370.pdf) | PDF | 1 | 11 | 2 | P3 | `forms_fx` |  |
| 260 | [외국환업무 등록내용 변경 신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2020/08/12/5-09-0362.pdf) | PDF | 1 | 18 | 0 | P3 | `forms_fx` |  |
| 261 | [환전업무 폐지 신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2020/08/12/5-09-0372.pdf) | PDF | 1 | 6 | 0 | P3 | `forms_fx` |  |
| 262 | [상호계산신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2020/08/12/5-09-0281_1.pdf) | PDF | 1 | 12 | 0 | P3 | `forms_fx` |  |
| 263 | [지급등의 방법(변경)신고(보고)서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2020/08/12/5-09-0291.pdf) | PDF | 1 | 25 | 6 | P3 | `forms_fx` |  |
| 264 | [거주자간 해외직접투자 양수도 신고(보고)서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2020/08/12/5-09-0185.pdf) | PDF | 2 | 18 | 5 | P3 | `forms_fx` |  |
| 265 | [수탁기관 변경 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2020/03/26/5-09-0164_1.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_fx` |  |
| 266 | [수출대금채권 매입의뢰서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2018/01/10/5-09-0198_170807.pdf) | PDF | 1 | 11 | 0 | P3 | `forms_fx` |  |
| 267 | [외국환거래용 인감(서명)신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2017/04/28/3-09-0240.pdf) | PDF | 1 | 7 | 0 | P3 | `forms_fx` |  |
| 268 | [수입선적서류 도착통지 및 수입신용장 조건불일치에 관한 조회](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2017/11/22/5-09-0328_171122.pdf) | PDF | 1 | 4 | 0 | P3 | `forms_fx` |  |
| 269 | [「외국환서식관리프로그램」수입화물선취보증신청서(Application For Letter of Guarantee)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/11/01/5-09-0111.xls) | XLS |  |  |  | P3 | `forms_fx` | XLS 원본 — 레이아웃 근거 확인 필요 |
| 270 | [대외지급보증서 (발급.조건변경) 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/11/01/5-09-0061.doc) | DOC |  |  |  | P3 | `forms_fx` | DOC 원본 — 레이아웃 근거 확인 필요 |
| 271 | [「외국환서식관리프로그램」항공화물운송장에 의한 수입물품 인도승낙(신청)서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/10/28/5-09-0010.xls) | XLS |  |  |  | P3 | `forms_fx` | XLS 원본 — 레이아웃 근거 확인 필요 |
| 272 | [REDEMPTION OF OUR LETTERS OF GUARANTEE](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/06/5-09-0014.pdf) | PDF | 3 | 0 | 0 | P3 | `forms_fx` |  |
| 273 | [[서식관리프로그램] 수입신용장 취소 및 수입보증금 환급 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/06/5-09-0003.pdf) | PDF | 1 | 7 | 0 | P3 | `forms_fx` |  |
| 274 | [「외국환서식관리프로그램」신용장 분실신고 및 재발행 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0349_0603.pdf) | PDF | 1 | 10 | 0 | P3 | `forms_fx` |  |
| 275 | [수입신용장 재개설 및 중계에 관한 약정서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0197_0603.pdf) | PDF | 2 | 0 | 0 | P3 | `forms_fx` |  |
| 276 | [확약서(단기수출보험(본지사금융))](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0360_0603.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_fx` |  |
| 277 | [포페이팅 의뢰서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0315_0603.pdf) | PDF | 1 | 11 | 4 | P3 | `forms_fx` |  |
| 278 | [판매대금추심의뢰서 매입(취소) 등록 요청/확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2017/11/22/5-09-0029_171122.pdf) | PDF | 1 | 3 | 0 | P3 | `forms_fx` |  |
| 279 | [추심의뢰서(Renego)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0333_0603.pdf) | PDF | 2 | 0 | 0 | P3 | `forms_fx` |  |
| 280 | [추심 수출환어음 종결처리(유예) 요청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0332_0603.pdf) | PDF | 2 | 7 | 0 | P3 | `forms_fx` |  |
| 281 | [「외국환서식관리프로그램」조건변경부 신용장양도(SKY T/S) 조건변경.취소 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0324_0603.pdf) | PDF | 1 | 4 | 3 | P3 | `forms_fx` |  |
| 282 | [「외국환서식관리프로그램」조건변경부 신용장양도(SKY T/S) 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0323_0603.pdf) | PDF | 1 | 4 | 1 | P3 | `forms_fx` |  |
| 283 | [인감증(외국환업무)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0329_0603.pdf) | PDF | 1 | 3 | 0 | P3 | `forms_fx` |  |
| 284 | [인감증 분실신고 및 재발급 신청서(외국환업무)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0331_0603.pdf) | PDF | 1 | 2 | 0 | P3 | `forms_fx` |  |
| 285 | [인감증 발급신청서(외국환업무)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0330_0603.pdf) | PDF | 1 | 3 | 0 | P3 | `forms_fx` |  |
| 286 | [신용장 확인 신청 및 확약서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/11/01/5-09-0108.pdf) | PDF | 2 | 0 | 10 | P3 | `forms_fx` |  |
| 287 | [「외국환서식관리프로그램」신용장 양도 조건변경/취소 신청서 (Amendment / Cancellation)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0308_0603.pdf) | PDF | 1 | 0 | 8 | P3 | `forms_fx` |  |
| 288 | [「외국환서식관리프로그램」신용장 양도 신청서(Application for Total/Partial transfer)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0309_0603.pdf) | PDF | 1 | 0 | 4 | P3 | `forms_fx` |  |
| 289 | [수출환어음등의 재매입을 위한 약정서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0402_0603.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_fx` |  |
| 290 | [수출환어음 추심 후 매입전환 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0200_0603.pdf) | PDF | 1 | 7 | 0 | P3 | `forms_fx` |  |
| 291 | [「외국환서식관리프로그램」수출대금채권 양도에 따른 대금지급지시서 및 동의통지서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0307_0603.pdf) | PDF | 2 | 0 | 0 | P3 | `forms_fx` |  |
| 292 | [수입통관도우미서비스 이용신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0327_0603.pdf) | PDF | 1 | 6 | 0 | P3 | `forms_fx` |  |
| 293 | [「외국환서식관리프로그램」선적서류 수령증 및 수입화물 대도(T/R)신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/02/5-09-0005_0603.pdf) | PDF | 1 | 3 | 2 | P3 | `forms_fx` |  |
| 294 | [「외국환서식관리프로그램」선적서류 (일부)매입(추심) 의뢰서(2D용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0295_0603.pdf) | PDF | 1 | 27 | 0 | P3 | `forms_fx` |  |
| 295 | [보증서(수출환어음등 재매입용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0325_0603.pdf) | PDF | 1 | 5 | 0 | P3 | `forms_fx` |  |
| 296 | [매입제한 해제 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0314_0603.pdf) | PDF | 1 | 6 | 0 | P3 | `forms_fx` |  |
| 297 | [단기수출보험(수출채권유동화) 청약 확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0357_0603.pdf) | PDF | 3 | 26 | 8 | P3 | `forms_fx` |  |
| 298 | [단기수출보험(수출채권유동화) 보상심사 제출서류 목록](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0354_0603.pdf) | PDF | 9 | 36 | 8 | 제외 |  | 서류 목록 인쇄물 |
| 299 | [관리계좌확약서(수출대금)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0353_0603.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_fx` |  |
| 300 | [LG 보증금 환급 신청 및 확약서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0184_0603.pdf) | PDF | 1 | 8 | 0 | P3 | `forms_fx` |  |
| 301 | [Cable Nego 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0316_0603.pdf) | PDF | 1 | 5 | 0 | P3 | `forms_fx` |  |
| 302 | [「외국환서식관리프로그램」BILL OF EXCHANGE (환어음 고객용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0047_0603.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_fx` |  |
| 303 | [수입실적 확인 및 증명 발급신청서(별지 제11호 서식)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0129_0603.pdf) | PDF | 1 | 2 | 0 | P3 | `forms_fx` |  |
| 304 | [수출실적 확인 및 증명 발급신청서(별지 제10호 서식)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/06/03/5-09-0128_0603.pdf) | PDF | 1 | 2 | 0 | P3 | `forms_fx` |  |
| 305 | [( )예금/신탁 거래신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0182.pdf) | PDF | 1 | 13 | 0 | P3 | `forms_fx` |  |
| 306 | [증권대차계약 신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0368.pdf) | PDF | 1 | 16 | 2 | P3 | `forms_fx` |  |
| 307 | [지급수단등의 수출입(변경)신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0366.pdf) | PDF | 1 | 13 | 0 | P3 | `forms_fx` |  |
| 308 | [대북투자사업계획서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0186.pdf) | PDF | 2 | 37 | 5 | P3 | `forms_fx` |  |
| 309 | [파생상품거래 신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0364.pdf) | PDF | 1 | 15 | 4 | P3 | `forms_fx` |  |
| 310 | [대북투자사업 청산 및 대부채권 회수보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0187.pdf) | PDF | 2 | 13 | 5 | P3 | `forms_fx` |  |
| 311 | [상호계산계정 폐쇄 신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0194.pdf) | PDF | 1 | 4 | 0 | P3 | `forms_fx` |  |
| 312 | [비거주자원화계정을 통한 송금(투자)보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0338.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_fx` |  |
| 313 | [북한지사 설치·현황 보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0337.pdf) | PDF | 2 | 4 | 0 | P3 | `forms_fx` |  |
| 314 | [북한지사 설치(변경) 신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0336.pdf) | PDF | 1 | 20 | 3 | P3 | `forms_fx` |  |
| 315 | [증권(채권)취득 보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0209.pdf) | PDF | 1 | 19 | 4 | P3 | `forms_fx` |  |
| 316 | [북한지사 등의 영업활동 보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0335.pdf) | PDF | 1 | 21 | 1 | P3 | `forms_fx` |  |
| 317 | [증권발행 보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0383.pdf) | PDF | 1 | 21 | 0 | P3 | `forms_fx` |  |
| 318 | [대북투자(변경)신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0275.pdf) | PDF | 1 | 18 | 2 | P3 | `forms_fx` |  |
| 319 | [증권취득 신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0382.pdf) | PDF | 1 | 18 | 4 | P3 | `forms_fx` |  |
| 320 | [재환전 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0379.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_fx` |  |
| 321 | [부동산취득신고(수리)서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0278.pdf) | PDF | 1 | 14 | 0 | P3 | `forms_fx` |  |
| 322 | [북한사무소 경비지급신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0279.pdf) | PDF | 1 | 12 | 2 | P3 | `forms_fx` |  |
| 323 | [북한지점 경비지급신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0280.pdf) | PDF | 1 | 14 | 3 | P3 | `forms_fx` |  |
| 324 | [임대차계약신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0285.pdf) | PDF | 1 | 13 | 0 | P3 | `forms_fx` |  |
| 325 | [증권취득신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0287.pdf) | PDF | 1 | 14 | 0 | P3 | `forms_fx` |  |
| 326 | [( )매매 신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0321.pdf) | PDF | 1 | 12 | 0 | P3 | `forms_fx` |  |
| 327 | [담보제공 신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0320.pdf) | PDF | 1 | 19 | 6 | P3 | `forms_fx` |  |
| 328 | [외국기업 국내지사 폐쇄신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0284.pdf) | PDF | 1 | 9 | 1 | P3 | `forms_fx` |  |
| 329 | [외국기업 국내지사 설치신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0283.pdf) | PDF | 1 | 14 | 1 | P3 | `forms_fx` |  |
| 330 | [외국기업 국내지사 변경신고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0282.pdf) | PDF | 1 | 10 | 0 | P3 | `forms_fx` |  |
| 331 | [해외지점의 영업활동 보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0214.pdf) | PDF | 1 | 17 | 0 | P3 | `forms_fx` |  |
| 332 | [외국기업 국내 결산순이익금 송금신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0202.pdf) | PDF | 1 | 9 | 0 | P3 | `forms_fx` |  |
| 333 | [송금(투자)보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2016/05/20/5-09-0195.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_fx` |  |
| 334 | [전자적무역결제금융등록(변경,해지)신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2015/09/04/5-09-0114.pdf) | PDF | 1 | 20 | 0 | P3 | `forms_fx` |  |

### 전자금융 (46건)

| No | 서식명 | 형식 | 쪽 | 기재란 | 보기 | 판정 | 대상 | 비고 |
|---:|---|---|---:|---:|---:|---|---|---|
| 335 | [하나 입출금 거래내역 문자통지서비스 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2026/05/29/3-08-1296.pdf) | PDF | 4 | 24 | 47 | P2 | `efinance/sms_notice_application` | 입출금 거래내역 문자통지서비스 신청서 |
| 336 | [개인 전자금융 서비스 신청서(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2026/05/15/5-08-0523.pdf) | PDF | 3 | 13 | 4 | 기존 | `efinance/efinance_application_personal` | 영문 변형 |
| 337 | [개인 전자금융 서비스 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2026/05/15/3-08-0221.pdf) | PDF | 3 | 13 | 4 | P2 | `efinance/efinance_application_personal` | 개인 전자금융 서비스 신청서 |
| 338 | [기업 전자금융서비스 신청서(은행용)(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2026/03/13/5-08-0556.pdf) | PDF | 2 | 29 | 0 | 기존 | `efinance/efinance_application_corp` | 영문 변형 |
| 339 | [기업 전자금융서비스 신청확인서(고객용)(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2026/03/13/5-08-0555.pdf) | PDF | 2 | 0 | 0 | 기존 | `efinance/efinance_application_corp` | 고객용 신청확인서 — 영문 변형 |
| 340 | [기업 전자금융서비스 신청서(은행용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2026/02/13/3-08-0024_260213.pdf) | PDF | 2 | 41 | 0 | P2 | `efinance/efinance_application_corp` | 기업 전자금융서비스 신청서(은행용) |
| 341 | [기업 전자금융서비스 신청확인서(고객용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2026/02/13/3-08-0025_260213.pdf) | PDF | 2 | 0 | 0 | 기존 | `efinance/efinance_application_corp` | 고객용 신청확인서 변형 |
| 342 | [해외은행 계좌정보 수신서비스(SWIFT MT940) 이용신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2025/09/23/5-08-0488.pdf) | PDF | 1 | 11 | 2 | P3 | `forms_efinance` |  |
| 343 | [금융거래정보 이용제공 동의서(기업관계사서비스용)(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2025/05/16/5-08-0752.pdf) | PDF | 1 | 0 | 0 | 기존 | `privacy_consent` | 동의서 변형 |
| 344 | [기업관계사 서비스 이용계약서(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2025/05/16/5-08-0501.pdf) | PDF | 4 | 0 | 0 | P3 | `forms_efinance` |  |
| 345 | [금융거래정보 이용제공 동의서(기업관계사서비스용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2025/05/16/5-99-0086.pdf) | PDF | 1 | 1 | 0 | 기존 | `privacy_consent` | 동의서 변형 |
| 346 | [기업관계사 서비스 이용신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2025/05/16/5-08-0484.pdf) | PDF | 2 | 19 | 14 | P3 | `forms_efinance` |  |
| 347 | [기업관계사 서비스 이용계약서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2025/05/16/5-08-0498.pdf) | PDF | 4 | 0 | 0 | P3 | `forms_efinance` |  |
| 348 | [기업관계사 서비스 이용신청서(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2025/05/16/5-08-0491.pdf) | PDF | 2 | 15 | 12 | P3 | `forms_efinance` |  |
| 349 | [펌뱅킹 출금전용계좌이용 동의서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2025/05/14/5-08-0708.pdf) | PDF | 1 | 0 | 2 | P3 | `forms_efinance` |  |
| 350 | [아이부자 걷기챌린지 서비스 동의서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2024/11/13/7-99-0062.pdf) | PDF | 1 | 0 | 3 | P3 | `forms_efinance` |  |
| 351 | [잔액충전서비스 이용약관](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2024/06/18/2024-076_20240613.pdf) | PDF | 4 | 0 | 0 | 제외 |  | 약관 전문 — 고객이 기재하는 항목이 없다 |
| 352 | [하나 sERP 상담신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2024/06/14/5-08-0576.pdf) | PDF | 1 | 6 | 0 | P3 | `forms_efinance` |  |
| 353 | [CMS Plus 이용신청서(지사)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2024/06/14/5-08-0479.pdf) | PDF | 2 | 22 | 9 | P3 | `forms_efinance` |  |
| 354 | [CMS Plus 이용계약서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2024/06/14/5-08-0500.pdf) | PDF | 4 | 5 | 0 | P3 | `forms_efinance` |  |
| 355 | [CMS Mega 이용계약서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2024/06/14/5-08-0499.pdf) | PDF | 4 | 0 | 0 | P3 | `forms_efinance` |  |
| 356 | [CMS Plus 이용신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2024/06/14/5-08-0478.pdf) | PDF | 3 | 30 | 21 | P3 | `forms_efinance` |  |
| 357 | [CMSiNet 지사정보 등록신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2024/06/14/5-08-0481.pdf) | PDF | 1 | 7 | 2 | P3 | `forms_efinance` |  |
| 358 | [CMS Global 이용신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2024/06/14/5-08-0391.pdf) | PDF | 1 | 12 | 0 | P3 | `forms_efinance` |  |
| 359 | [하나 sERP 이용신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2024/06/14/5-08-0313.pdf) | PDF | 1 | 14 | 1 | P3 | `forms_efinance` |  |
| 360 | [개인(신용)정보 및 금융거래정보 제3자 제공동의서(모임통장서비스용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2023/12/05/5-16-0000.pdf) | PDF | 1 | 7 | 2 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 361 | [개인 전자금융 서비스 신청 확인서(고객용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2023/09/12/3-08-1289.pdf) | PDF | 2 | 5 | 0 | 기존 | `efinance/efinance_application_personal` | 고객용 신청확인서 변형 |
| 362 | [자동화기기 이용(신규,해지,변경)신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2023/02/23/3081245_20230223.pdf) | PDF | 3 | 3 | 0 | P3 | `forms_efinance` |  |
| 363 | [개인(신용)정보 수집이용 동의서[은행공동인증서비스(BankSign)]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2021/02/04/2021_20210204_01.pdf) | PDF | 1 | 8 | 2 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 364 | [개인(신용)정보 제3자 제공 동의서[은행공동인증서비스(BankSign)]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2021/02/04/2021_20210204_02.pdf) | PDF | 1 | 10 | 2 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 365 | [Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2021/01/08/5-08-0490_210108.pdf) | PDF | 2 | 7 | 1 | P3 | `forms_efinance` |  |
| 366 | [Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(국문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2021/01/08/5-08-0489_210108.pdf) | PDF | 2 | 13 | 1 | P3 | `forms_efinance` |  |
| 367 | [Hana 1Q bank CMS iNet 서비스 이용 추가 계약서(iSBS)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2021/01/08/5-08-0502_210108.pdf) | PDF | 2 | 0 | 0 | P3 | `forms_efinance` |  |
| 368 | [가상계좌서비스 이용계약서(외화)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2020/08/07/5-08-0418_20200807.pdf) | PDF | 5 | 9 | 8 | P3 | `forms_efinance` |  |
| 369 | [가상계좌서비스 이용계약서(원화)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2020/08/07/5-08-0397_20200807.pdf) | PDF | 4 | 7 | 8 | P3 | `forms_efinance` |  |
| 370 | [펌뱅킹서비스 계약서(외화)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2020/08/07/5-08-0257_20200807.pdf) | PDF | 6 | 0 | 0 | P3 | `forms_efinance` |  |
| 371 | [펌뱅킹서비스 계약서(원화)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2020/08/07/5-08-0256_20200807.pdf) | PDF | 8 | 0 | 0 | P3 | `forms_efinance` |  |
| 372 | [전산기기 임대차계약서(Hana 1Q bank CMS)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2021/01/08/5-08-0483_210108.pdf) | PDF | 2 | 5 | 0 | P3 | `forms_efinance` |  |
| 373 | [전자어음 교부 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2020/06/12/5_08_0135.pdf) | PDF | 1 | 7 | 0 | P2 | `efinance/electronic_note_issue` | 전자어음 교부 신청서 |
| 374 | [전자어음 이용(변경,해지) 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2020/06/12/5_08_0134.pdf) | PDF | 1 | 19 | 10 | P3 | `forms_efinance` |  |
| 375 | [자금관리서비스 이용계약서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2017/03/14/20170314_08.pdf) | PDF | 4 | 0 | 0 | P3 | `forms_efinance` |  |
| 376 | [위임장(해외체류자 전자금융용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2016/06/05/5-08-0487.pdf) | PDF | 1 | 4 | 0 | P3 | `forms_efinance` |  |
| 377 | [해외영업점 계좌개설 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2016/06/05/5-08-0485.pdf) | PDF | 1 | 11 | 4 | P3 | `forms_efinance` |  |
| 378 | [글로벌뱅킹서비스 이용,변경,해지 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2016/06/05/5-08-0480.pdf) | PDF | 2 | 9 | 0 | P3 | `forms_efinance` |  |
| 379 | [주류구매전용카드 가맹점가입신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2014/08/07/cccc005080209_20140807.pdf) | PDF | 2 | 12 | 1 | P3 | `forms_efinance` |  |
| 380 | [금융결제원CMS 이용계약서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070104/__icsFiles/afieldfile/2021/07/01/b000020130313_20090921.pdf) | PDF | 2 | 11 | 0 | P3 | `forms_efinance` |  |

### 파생상품 (25건)

| No | 서식명 | 형식 | 쪽 | 기재란 | 보기 | 판정 | 대상 | 비고 |
|---:|---|---|---:|---:|---:|---|---|---|
| 381 | [장외파생상품 일반투자자 (부)적정성 판단보고서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2025/12/12/5-09-0527.pdf) | PDF | 3 | 14 | 2 | P3 | `forms_derivative` |  |
| 382 | [장외파생상품 일반투자자 투자자정보 분석결과표](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2025/12/12/5-09-0526.pdf) | PDF | 2 | 9 | 0 | P3 | `forms_derivative` |  |
| 383 | [장외파생상품 투자성향에 적정하지 않은 거래확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2025/12/12/5-09-0525.pdf) | PDF | 2 | 8 | 0 | P3 | `forms_derivative` |  |
| 384 | [장외파생상품 일반투자자 투자자정보 확인서(법인 및 개인사업자 고객용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2025/12/12/5-09-0098.pdf) | PDF | 4 | 19 | 2 | P3 | `forms_derivative` |  |
| 385 | [장외파생상품 일반투자자 투자자정보 확인서(개인 고객용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2025/12/12/5-09-0095.pdf) | PDF | 3 | 9 | 0 | P3 | `forms_derivative` |  |
| 386 | [외환파생상품거래 헤지 수요 현황 및 거래 실행에 따른 확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2025/08/21/5-09-0101.pdf) | PDF | 2 | 11 | 4 | P3 | `forms_derivative` |  |
| 387 | [HANA FX TRADING SYSTEM 자동결제 이용신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2025/10/13/5-09-0514.pdf) | PDF | 1 | 3 | 9 | P3 | `forms_derivative` |  |
| 388 | [HANA FX TRADING SYSTEM 이용신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2025/10/13/5-09-0476.pdf) | PDF | 1 | 10 | 9 | P3 | `forms_derivative` |  |
| 389 | [위임장(장외파생상품 일반투자자용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2023/08/18/5-09-0524.pdf) | PDF | 1 | 6 | 0 | P3 | `forms_derivative` |  |
| 390 | [매매내역 등의 통지방법에 대한 고객확인서(장외파생상품)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2022/12/29/5-10-0012.pdf) | PDF | 1 | 0 | 6 | P3 | `forms_derivative` |  |
| 391 | [고령투자자확인서(장외파생상품용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2022/04/06/5-09-0465_1.pdf) | PDF | 1 | 0 | 8 | P3 | `forms_derivative` |  |
| 392 | [초고령투자자확인서(장외파생상품용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2022/04/06/5-09-0463_1.pdf) | PDF | 1 | 2 | 9 | P3 | `forms_derivative` |  |
| 393 | [이자율스왑 연계 대출 분할상환 원금 및 이자율스왑 정산이자 출금서비스 특약](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2021/11/30/5-09-0511.pdf) | PDF | 1 | 10 | 0 | P3 | `forms_derivative` |  |
| 394 | [적정성원칙 투자자확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2021/11/08/5-09-0510.pdf) | PDF | 1 | 1 | 0 | P3 | `forms_derivative` |  |
| 395 | [장외파생상품 일반투자자(개인)체크리스트](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2021/11/08/5-09-0099_1.pdf) | PDF | 1 | 0 | 0 | 제외 |  | 은행 내부 점검표 — 고객 기재란이 없다 |
| 396 | [(초)고령투자자 체크리스트(장외파생상품용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2021/08/18/5-09-0464.pdf) | PDF | 1 | 2 | 0 | 제외 |  | 은행 내부 점검표 — 고객 기재란이 없다 |
| 397 | [금융거래정보이용제공동의서(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2021/04/19/5-09-0492_210419.pdf) | PDF | 1 | 0 | 0 | 기존 | `privacy_consent` | 동의서 변형 |
| 398 | [금융거래정보이용제공동의서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2021/04/19/5-09-0489_210419.pdf) | PDF | 1 | 0 | 0 | 기존 | `privacy_consent` | 동의서 변형 |
| 399 | [파생상품거래 손실한도 초과 및 증거담보 요청 통지서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2020/05/25/5-09-0094.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_derivative` |  |
| 400 | [파생상품거래 손실한도 감액통지서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2020/05/25/5-09-0092.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_derivative` |  |
| 401 | [전문투자자 전환신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2020/05/25/5-09-0104.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_derivative` |  |
| 402 | [장외파생상품 거래 담당자 지정 통지서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2020/05/25/5-09-0090.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_derivative` |  |
| 403 | [일반투자자 전환신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2020/05/25/5-09-0096.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_derivative` |  |
| 404 | [일반위험고지문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2020/05/25/5-09-0089.pdf) | PDF | 2 | 0 | 0 | 제외 |  | 고지 인쇄물 |
| 405 | [외환파생상품 거래 금액 확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070105/__icsFiles/afieldfile/2020/05/25/5-09-0102.pdf) | PDF | 1 | 5 | 0 | P3 | `forms_derivative` |  |

### 기타 (36건)

| No | 서식명 | 형식 | 쪽 | 기재란 | 보기 | 판정 | 대상 | 비고 |
|---:|---|---|---:|---:|---:|---|---|---|
| 406 | [하나카드 금융상품 판매대리 중개업자 증서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/08/05/2026-686.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_etc` |  |
| 407 | [본인확인서(FATCA CRS 법인,임의단체용) 본문 설명서(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/07/29/5-08-0763.pdf) | PDF | 10 | 2 | 0 | 기존 | `fatca_crs` | FATCA/CRS 본인확인서 변형 |
| 408 | [본인확인서(FATCA CRS 개인,개인사업자용)(국문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/07/29/5-08-0334.pdf) | PDF | 1 | 12 | 7 | 기존 | `fatca_crs` | FATCA/CRS 본인확인서 변형 |
| 409 | [본인확인서(FATCA CRS 법인,임의단체용) 본문 설명서(국문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/07/29/5-08-0366.pdf) | PDF | 8 | 2 | 0 | 기존 | `fatca_crs` | FATCA/CRS 본인확인서 변형 |
| 410 | [본인확인서(FATCA CRS 법인,임의단체용)(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/07/29/5-08-0649.pdf) | PDF | 2 | 7 | 0 | 기존 | `fatca_crs` | FATCA/CRS 본인확인서 변형 |
| 411 | [[필수]본인 행정정보 제공 요구서(공공마이데이터 수신 묶음정보用 - 주민등록표 등·초본 조회)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/06/22/7-08-0036.pdf) | PDF | 2 | 3 | 1 | 기존 | `privacy_consent` | 공공마이데이터 제공요구 — 동의서 변형 |
| 412 | [[필수]본인 행정정보 제공 요구서(공공마이데이터 수신 묶음정보用 - 사업자등록증명 조회)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/06/22/7-08-0033.pdf) | PDF | 2 | 3 | 1 | 기존 | `privacy_consent` | 공공마이데이터 제공요구 — 동의서 변형 |
| 413 | [고객확인서(법인,고유번호나 납세번호가 있는 임의 단체용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/06/17/3-08-1301.pdf) | PDF | 2 | 36 | 18 | 기존 | `corporate_customer_due_diligence` |  |
| 414 | [[필수] 개인(신용)정보 수집·이용·제공 동의서 [공공마이데이터 주민등록 등·초본 조회용]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/06/10/7-08-0039.pdf) | PDF | 2 | 0 | 10 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 415 | [[필수] 개인(신용)정보 제3자 제공 동의서 [공공마이데이터 주민등록 등·초본 조회용]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/06/10/7-08-0037.pdf) | PDF | 1 | 0 | 7 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 416 | [[필수] 개인(신용)정보 수집·이용·제공 동의서 [공공마이데이터 사업자정보 조회용]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/06/10/7-08-0035.pdf) | PDF | 2 | 0 | 10 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 417 | [[필수] 개인(신용)정보 제3자 제공 동의서 [공공마이데이터 사업자정보 조회용]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/06/10/7-08-0034.pdf) | PDF | 1 | 0 | 7 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 418 | [[필수] 개인(신용)정보 수집·이용 동의서 [비대면 스크래핑 서비스]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2025/11/26/7-08-0031.pdf) | PDF | 1 | 0 | 5 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 419 | [[필수] 개인(신용)정보 수집 · 이용 동의서 (비여신 금융거래)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2025/08/20/3-08-1294.pdf) | PDF | 1 | 0 | 6 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 420 | [비대면 계좌개설 안심차단 서비스 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2025/05/09/5-08-0737.pdf) | PDF | 1 | 6 | 1 | P3 | `forms_etc` |  |
| 421 | [[필수] 개인(신용)정보 수집·이용·제공·조회 동의서 [비대면 계좌개설 안심차단 서비스]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2025/03/11/5-08-0740.pdf) | PDF | 2 | 0 | 18 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 422 | [[필수] 개인(신용)정보 수집·이용·조회 동의서[비대면 계좌개설 안심차단 신청여부 조회용]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2025/03/11/5-08-0739.pdf) | PDF | 2 | 0 | 12 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 423 | [[선택] 개인(신용)정보 수집ㆍ이용 및 제공동의서 (상품서비스 안내 등)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2024/10/14/3-08-1295.pdf) | PDF | 2 | 0 | 10 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 424 | [[필수] 개인(신용)정보 제3자제공 동의서 [하나카드 발급_미성년자용]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2024/10/10/7-08-0018.pdf) | PDF | 1 | 0 | 6 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 425 | [[필수] 개인(신용)정보 제3자제공 동의서 [하나카드 발급_법정대리인용]](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2024/10/10/7-08-0019.pdf) | PDF | 1 | 0 | 5 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 426 | [이의제기 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2024/08/21/5-08-0246.pdf) | PDF | 1 | 0 | 0 | P3 | `forms_etc` |  |
| 427 | [아이부자 선불전자지급수단 잔액 상속(지급) 및 서비스 해지 요청서(위임장 겸용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2024/04/25/5-99-0088.pdf) | PDF | 2 | 5 | 18 | P3 | `forms_etc` |  |
| 428 | [본인확인서(FATCA CRS 법인,임의단체용)(국문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2024/01/05/5-08-0335.pdf) | PDF | 2 | 29 | 0 | 기존 | `fatca_crs` | FATCA/CRS 본인확인서 변형 |
| 429 | [본인확인서(FATCA CRS 개인,개인사업자용)(영문)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2024/01/05/5-08-0584.pdf) | PDF | 1 | 17 | 6 | 기존 | `fatca_crs` | FATCA/CRS 본인확인서 변형 |
| 430 | [민원신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2024/06/20/minwon_211115.pdf) | PDF | 4 | 12 | 12 | P3 | `forms_etc` |  |
| 431 | [전자금융거래 사고 피해 신고서(통합서류)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2024/06/12/5-99-0002.pdf) | PDF | 8 | 31 | 52 | P3 | `forms_etc` |  |
| 432 | [[필수] 개인(신용)정보 제3자 제공 동의서 (하나원큐 공모주 정보제공 제휴서비스용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2023/11/07/7-99-0039.pdf) | PDF | 1 | 0 | 3 | 기존 | `privacy_consent` | 상품·용도별 동의서 변형 (문구만 다르다) |
| 433 | [추심지급 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2023/03/07/5-08-0205.pdf) | PDF | 1 | 9 | 1 | P3 | `forms_etc` |  |
| 434 | [세종특별자치시 지역개발채권 매입 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2022/02/21/5-08-0344.pdf) | PDF | 2 | 7 | 7 | P3 | `forms_etc` |  |
| 435 | [대전광역시 지역개발채권 매입 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2022/02/21/5-08-0230.pdf) | PDF | 2 | 7 | 7 | P3 | `forms_etc` |  |
| 436 | [주주명부(법인 비대면 실명확인 서비스 용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2021/11/22/stockholder_211122.pdf) | PDF | 1 | 1 | 0 | P3 | `forms_etc` |  |
| 437 | [고객정보 활용 동의서(매출채권보험_모집대행업무용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2021/09/24/5-99-0039_210924.pdf) | PDF | 1 | 8 | 0 | 기존 | `privacy_consent` | 동의서 변형 |
| 438 | [매출채권보험 상담 신청서(신청기업용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2021/09/24/5-99-0040_210924.pdf) | PDF | 1 | 15 | 0 | P3 | `forms_etc` |  |
| 439 | [상조회사 선수금 예치확인서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2022/07/29/5-99-0020.pdf) | PDF | 1 | 3 | 0 | P3 | `forms_etc` |  |
| 440 | [금융사고예방을 위한 문자통지(SMS) 서비스 신청서](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2020/05/08/5-08-0320-200508.pdf) | PDF | 1 | 1 | 0 | P3 | `forms_etc` |  |
| 441 | [법원보관금 납부서(은행제출용)](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2018/12/21/5080258.pdf) | PDF | 3 | 12 | 0 | P3 | `forms_etc` |  |

