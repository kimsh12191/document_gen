# 공식 원문과 HTML 서식 대조 (2026-10-20)

기존 HTML 70종과 하나은행 PDF 배경 서식 406종을 유지하고 **공식 대조 HTML 69종**을 별도로 추가했다. 하나은행 44종, 정부·공공 별지 25종이다. 제목이 비슷해도 실제로 다른 서류는 동일 매칭하지 않았다. 이 문서의 “추가”는 원문을 대조한 HTML이 있다는 뜻이며, Studio의 사람 검수 완료 표시와는 별개다.

## 화면에서 찾기

① 서식에서 `공식대조 HTML`로 검색한다. 하나은행 항목은 하나은행 그룹, 정부 항목은 해당 업무 그룹에 있다. 종류는 모두 HTML이다. 화면의 `공식대조 HTML` 배지는 출처 표시이며, 문서명과 분류 정답에는 포함하지 않는다. 기존 서식·PDF 버전도 남아 있다. ③ 시나리오의 구성 서류에서 새 ID를 선택할 수 있다. 기존 시나리오는 자동 교체하지 않았다.

## 원문과 달라지는 부분

- 인쇄 문구는 HTML 글자, 표 선·음영은 SVG 도형이다. 원본이 글자를 윤곽선으로 저장한 부분은 SVG 윤곽선으로 보존되어 문구 편집과 DOM 기반 OCR 정답에 한계가 있다(특히 특정채무 보증서).
- 시스템 글꼴로 대체하고 글자 폭을 맞춘다. 실제 로고·QR·바코드·직인 이미지와 문서 보안 표식은 복제하지 않는다. `합성 데이터 · 견본` 표시는 항상 넣는다.
- 하나은행 40종은 해당 hf###의 기재란 생성 규칙을 잇는다. 자동 추출된 기재란의 의미·빠진 키까지 모두 사람 검수된 것은 아니다. 과도하게 큰 체크 영역은 새 HTML에서 제외하고, 은행거래신청서의 주요 고객 칸은 별도 배치로 보정했다.
- 정부 서류와 추가 약정서는 주요 기재란을 연결했다. 모든 빈칸을 채운 제출 완성본이나 세액 계산 결과를 뜻하지 않는다. 표준재무제표증명은 표지이며 첨부 재무제표 전체가 아니다. 건축물 현황도도 임의로 그리지 않는다.
- 국민연금 가입자 증명서(법령 별지)와 전자민원 가입이력 증명, 잔액증명 의뢰서와 잔액증명서, 금융거래확인서와 부채증명서를 구분한다.

## 개발·검증

원본 PDF·URL·개정 표기·SHA-256·기재란 좌표는 [official_html_sources.json](official_html_sources.json)에 있고, 각 서식의 `form.json`에도 출처를 남겼다. 66개 고유 공식 URL(공유 원문 제외)의 응답과 보관 원문 해시를 대조했다.

```powershell
python -m docgen.scripts.build_official_html --id hana_official_003
python -m docgen.scripts.update_official_schema
python -m docgen.scripts.verify_official_html --out studio_cache/official_html/verification
```

빌더는 기본적으로 기존 HTML 폴더를 덮어쓰지 않는다. 명시적으로 재생성할 때만 `--overwrite`를 쓴다. Studio에서 고친 템플릿은 재생성 전에 변경분을 보존해야 한다. 새 서식은 `guide/fields/fields.json`에도 추가해 문항의 항목 선택에 연결했다. Q/A 문장 형식과 라벨 내보내기는 기존 생성기를 그대로 따른다.

검증 결과와 원문/HTML 비교 그림은 `studio_cache/official_html/verification/`에 저장한다. 기존 70개 HTML의 내용은 Git 기준 버전과 동일한지 확인하고 작업 시점 파일 해시를 기록했다. 공식 출처 확인으로 사람 검수 완료를 자동 처리하지 않는다.

아래 대조표의 “미확보”는 공개되지 않는다는 단정이 아니다. 이번에 배치까지 검증할 원본을 확보하지 못했다는 뜻이다. 해당 기존 서식을 공식 재현본으로 표시하지 않았다.

최종 확인: 69종·170쪽의 페이지 수, 쪽 넘침, 정답 좌표, 선언한 기재값을 자동 검사했다. 기존 서식·편집 테스트는 677개 통과(4개 건너뜀), 최종 출처 표시·Studio 문항 연결 검사도 통과했다. 실제 서버 목록은 545종 중 공식 대조 HTML 69종이며, 소득금액증명 예시의 분류 정답이 출처 배지 없이 `소득금액증명`으로 생성되는 것을 확인했다. 자동 검사는 인쇄층 재현과 코드 연결 확인이며 기재 내용 전체의 의미 검수 완료를 뜻하지 않는다.

## 기존 HTML 70종 검토 결과

| 기존 ID | 서류 | 결과 | 추가/관련 HTML | 비고 |
|---|---|---|---|---|
| `loan_application` | 대출거래신청서 | 공식 HTML 추가 | `hana_official_049` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `loan_application_corp` | 기업여신 신청서 | 공식 HTML 추가 | `hana_official_058` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `credit_agreement` | 대출거래약정서(가계용) | 공식 HTML 추가 | `hana_personal_agreement` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `credit_agreement_corp` | 여신거래약정서(기업용) | 공식 HTML 추가 | `hana_corporate_agreement` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `collateral_agreement` | 근저당권설정계약서 | 공식 HTML 추가 | `hana_collateral_agreement` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `guarantee_agreement` | 보증약정서 | 공식 HTML 추가 | `hana_specific_guarantee` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `auto_transfer_application` | 자동이체 신청서 | 공식 HTML 추가 | `hana_official_006` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `customer_due_diligence` | 고객확인서(개인) | 관련 서식 | `hana_official_003`, `hana_official_061` | 개인 고객확인은 은행거래신청서·적합성 확인서에 관련 칸이 있으나 독립 고객확인서와 동일시하지 않음. |
| `corporate_customer_due_diligence` | 고객확인서(법인·단체) | 공식 HTML 추가 | `hana_official_413` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `privacy_consent` | 개인(신용)정보 수집·이용·제공·조회 동의서 | 공식 HTML 추가 | `hana_official_118` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `account_opening_application` | 예금거래신청서 | 공식 HTML 추가 | `hana_official_003` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `financial_transaction_purpose` | 금융거래목적확인서 | 관련 서식 | `hana_official_003` | 하나은행 013은 목적 확인 안내장으로 고객이 쓰는 확인서와 다름. |
| `overseas_remittance_application` | 해외송금신청서 | 공식 HTML 추가 | `hana_official_199` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `fatca_crs` | 해외금융계좌 납세자 확인서(개인) | 공식 HTML 추가 | `hana_official_408` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `business_registration_certificate` | 사업자등록증 | 공식 HTML 추가 | `gov_business_registration` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `business_registration_certificate_corp` | 사업자등록증(법인사업자) | 공식 HTML 추가 | `gov_business_registration_corp` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `business_registration_proof` | 사업자등록증명 | 공식 HTML 추가 | `gov_business_proof` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `standard_financial_statement_proof` | 표준재무제표증명 | 공식 HTML 추가 | `gov_financial_proof` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `corporate_registry` | 법인 등기사항전부증명서(현재 유효사항) | 발급형 원문 미확보 | — | 발급 출력 전체의 모양을 검증할 원본 미확보. 기존 HTML 유지. |
| `articles_of_incorporation` | 정관 | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `shareholder_registry` | 주주명부 | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `financial_statements` | 재무제표(재무상태표·손익계산서) | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `corporate_seal_certificate` | 법인인감증명서 | 발급형 원문 미확보 | — | 발급 출력 전체의 모양을 검증할 원본 미확보. 기존 HTML 유지. |
| `board_minutes` | 이사회의사록 | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `shareholders_meeting_minutes` | 임시주주총회의사록 | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `power_of_attorney` | 위임장 | 공식 HTML 추가 | `hana_official_028` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `resident_registration_copy` | 주민등록표 등본 | 공식 HTML 추가 | `gov_resident_copy` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `resident_registration_abstract` | 주민등록표 초본 | 공식 HTML 추가 | `gov_resident_abstract` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `family_relation_certificate` | 가족관계증명서 | 공식 HWP 확인 | — | 대법원 예규 제562호의 일반·상세·특정 양식 확인. HWP의 배치 검증 미완료로 공식 HTML 미추가. |
| `basic_certificate` | 기본증명서 | 공식 HWP 확인 | — | 대법원 예규 제562호의 일반·상세·특정 양식 확인. HWP의 배치 검증 미완료로 공식 HTML 미추가. |
| `marriage_relation_certificate` | 혼인관계증명서 | 공식 HWP 확인 | — | 대법원 예규 제562호의 일반·상세·특정 양식 확인. HWP의 배치 검증 미완료로 공식 HTML 미추가. |
| `employment_certificate` | 재직증명서 | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `career_certificate` | 경력증명서 | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `pay_stub` | 급여명세서 | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `employment_contract` | 근로계약서 | 공식 HWP 확인 | — | 고용노동부 2025 개정 HWP 링크·뷰어 확인. 변환 본문을 확보하지 못해 공식 HTML 미추가. |
| `withholding_receipt` | 근로소득 원천징수영수증 | 공식 HTML 추가 | `gov_withholding` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `income_certificate` | 소득금액증명원 | 공식 HTML 추가 | `gov_income` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `pension_enrollment_certificate` | 국민연금 가입자 가입증명 | 관련 별지 추가 | `gov_pension` | 국민연금 법령 별지 가입자 증명서. 전자민원의 전체 가입이력 출력과는 다름. |
| `health_insurance_qualification` | 건강보험 자격득실확인서 | 발급형 원문 미확보 | — | 발급 출력 전체의 모양을 검증할 원본 미확보. 기존 HTML 유지. |
| `health_insurance_payment` | 건강보험료 납부확인서 | 발급형 원문 미확보 | — | 발급 출력 전체의 모양을 검증할 원본 미확보. 기존 HTML 유지. |
| `bankbook_copy` | 통장사본 | 발급형 원문 미확보 | — | 발급 출력 전체의 모양을 검증할 원본 미확보. 기존 HTML 유지. |
| `bank_statement` | 거래내역확인서 | 발급형 원문 미확보 | — | 발급 출력 전체의 모양을 검증할 원본 미확보. 기존 HTML 유지. |
| `balance_certificate` | 잔액증명서 | 발급형 원문 미확보 | `hana_official_011` | 예금잔액증명 의뢰서는 발급 신청서. 증명서 자체와 구분. |
| `debt_certificate` | 부채증명서 | 발급형 원문 미확보 | `hana_official_149` | 금융거래확인서와 부채증명서는 별개 서류. |
| `card_statement` | 신용카드 이용대금명세서 | 발급형 원문 미확보 | — | 발급 출력 전체의 모양을 검증할 원본 미확보. 기존 HTML 유지. |
| `commercial_invoice` | 상업송장(Commercial Invoice) | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `trade_contract` | 무역 매매계약서(Sales Contract) | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `bill_of_lading` | 선하증권(B/L) | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `packing_list` | 포장명세서(Packing List) | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `import_declaration` | 수입신고필증 | 발급형 원문 미확보 | — | 발급 출력 전체의 모양을 검증할 원본 미확보. 기존 HTML 유지. |
| `admission_letter` | 입학허가서(Letter of Admission) | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `tuition_invoice` | 학비 청구서(Tuition Invoice) | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `resident_id_card` | 주민등록증 | 발급형 원문 미확보 | — | 발급 출력 전체의 모양을 검증할 원본 미확보. 기존 HTML 유지. |
| `driver_license` | 운전면허증 | 발급형 원문 미확보 | — | 발급 출력 전체의 모양을 검증할 원본 미확보. 기존 HTML 유지. |
| `passport` | 여권 | 발급형 원문 미확보 | — | 발급 출력 전체의 모양을 검증할 원본 미확보. 기존 HTML 유지. |
| `alien_registration_card` | 외국인등록증 | 발급형 원문 미확보 | — | 발급 출력 전체의 모양을 검증할 원본 미확보. 기존 HTML 유지. |
| `seal_certificate` | 인감증명서 | 공식 HTML 추가 | `gov_seal` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `signature_confirmation` | 본인서명사실확인서 | 공식 HTML 추가 | `gov_signature` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `real_estate_registry` | 등기사항전부증명서(집합건물) | 발급형 원문 미확보 | — | 발급 출력 전체의 모양을 검증할 원본 미확보. 기존 HTML 유지. |
| `building_register` | 집합건축물대장(전유부) | 공식 HTML 추가 | `gov_building_unit` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `land_register` | 토지대장 | 공식 HTML 추가 | `gov_land` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `sales_contract` | 부동산 매매계약서 | 제출 주체별 양식 유지 | — | 회사·학교·운송사·당사자별 형식. 하나의 정부·은행 공식 양식으로 확정하지 않음. |
| `lease_contract` | 주택임대차표준계약서 | 공식 다운로드 실패 | — | 법무부 2023.10.06 PDF 링크를 확인했으나 307 리디렉션 반복으로 미수집. |
| `move_in_household_list` | 전입세대확인서 | 공식 HTML 추가 | `gov_move_in` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `tax_payment_certificate` | 납세증명서(국세완납증명) | 공식 HTML 추가 | `gov_national_tax` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `tax_payment_certificate_corp` | 납세증명서(법인) | 공식 HTML 추가 | `gov_national_tax` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `local_tax_payment_certificate` | 지방세 납세증명서 | 공식 HTML 추가 | `gov_local_tax` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `local_tax_assessment` | 지방세 세목별 과세증명서 | 공식 HTML 추가 | `gov_local_assessment` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `vat_tax_base_certificate` | 부가가치세 과세표준증명 | 공식 HTML 추가 | `gov_vat_base` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |
| `income_tax_return` | 종합소득세 과세표준확정신고 및 납부계산서 | 공식 HTML 추가 | `gov_income_tax_return` | 공식 원문 인쇄층 대조. 세부 생성값의 사람 검수와는 별개. |

## 추가한 서식과 공식 출처

| 새 ID | 서식 | 원문 버전 | 공식 출처 |
|---|---|---|---|
| `hana_official_001` | 상속예금 명의변경(지급) 의뢰서 및 손해담보 확약서(상속예금 지급 위임장 겸용) | (2026.09 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2026/09/07/5-08-0084.pdf) |
| `hana_official_003` | 은행거래신청서 | (2026.06 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2026/06/19/3-08-1016.pdf) |
| `hana_official_006` | 자동이체 신청서 | (2025.11 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2025/11/27/3-11-0012.pdf) |
| `hana_official_011` | 예금(신탁)잔액증명 의뢰서 | (2025.01 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2025/01/07/5-08-0094.pdf) |
| `hana_official_015` | 통합제신고서 | (2023.07 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2024/02/02/3-08-1280_240202.pdf) |
| `hana_official_024` | 금융거래정보제공(요구·동의)서 | (2021.09 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2021/09/07/5-08-0016_200508.pdf) |
| `hana_official_028` | 위임장 | (2020.05 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/29/5_08_0041_20200601.pdf) |
| `hana_official_029` | 사용인감계(금융계좌개설용) | (2016.04 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/08/5-08-0056_200508.pdf) |
| `hana_official_047` | 대출상담 및 신청서(한국주택금융공사채권유동화목적 보금자리론용) | (2026.07 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2026/07/30/3-06-1104.pdf) |
| `hana_official_048` | 가계형소호 여신차입신청서 | (2025.10 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/10/20/b000005060519_20251020.pdf) |
| `hana_official_049` | 《개인》대출신청서(가계용) | (2025.10 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/10/20/5160178_20251020.pdf) |
| `hana_official_051` | 대출계약 철회신청서 | (2025.07 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/30/5-06-0681.pdf) |
| `hana_official_052` | [필수] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택전월세자금대출용) | (2025.06 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/23/5-06-0920.pdf) |
| `hana_official_053` | [필수] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택구입자금대출용) | (2025.06 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/23/5-06-0919.pdf) |
| `hana_official_054` | 주택도시기금 대출 신청서(가계용) | (2025.06 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/23/5-16-0177.pdf) |
| `hana_official_055` | 주택도시기금 대출상담 및 신청서(내집마련 디딤돌 대출용) | (2025.06 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/23/5-16-0139.pdf) |
| `hana_official_058` | 융자상담 및 차입신청서(기업용) | (2024.09 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/10/10/3-06-0201_1.pdf) |
| `hana_official_059` | 개인(신용)정보 조회 동의서 | (2024.06 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/06/27/5-06-0548.pdf) |
| `hana_official_060` | [필수] 개인(신용)정보 수집이용 동의서(대출성상품 적합성적정성 판단용) | (2021.09 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/06/14/3-06-0151.pdf) |
| `hana_official_061` | 적합성, 적정성 고객정보 확인서(개인 및 개인사업자용) | (2021.05 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/06/14/5-06-0967.pdf) |
| `hana_official_062` | 적합성, 적정성 고객정보 확인서(법인용) | (2021.05 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2024/06/14/5-06-0970.pdf) |
| `hana_official_064` | 대출정보 열람청구, 상환 및 말소접수 위임장(주택담보대출 대출이동서비스) | 원본 PDF 인쇄 개정 표기 및 출처 URL 기준 | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/12/08/5-16-0401.pdf) |
| `hana_official_065` | 국토교통부 주택소유확인 시스템 등 이용 관련 [필수] 개인(신용)정보 수집·이용·제공 동의서 | (2023.06 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/06/13/5-06-0893.pdf) |
| `hana_official_066` | 대출정보 열람청구 및 상환 위임장(대출이동서비스) | 원본 PDF 인쇄 개정 표기 및 출처 URL 기준 | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/05/31/5-16-0365_230531.pdf) |
| `hana_official_067` | [필수] 개인(신용)정보 수집 · 이용 동의서[대출이동서비스] | 원본 PDF 인쇄 개정 표기 및 출처 URL 기준 | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/05/31/5-16-0364_230531.pdf) |
| `hana_official_118` | [필수] 개인(신용)정보 수집·이용·제공_동의서[가계여신_금융거래] | (2021.02 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/03/02/5-16-0179_20210302.pdf) |
| `hana_official_128` | 필수 개인(신용)정보 수집, 이용 및 제공 동의서(소호여신) | (2021.02 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/02/25/5_06_0724.pdf) |
| `hana_official_129` | 필수 개인(신용)정보 수집, 이용 및 제공 동의서(법인여신) | (2021.02 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2021/02/25/5-06-0734.pdf) |
| `hana_official_138` | 대출금 수령위임동의서 | 원본 PDF 인쇄 개정 표기 및 출처 URL 기준 | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5-06-0741_20150901.pdf) |
| `hana_official_139` | 《기업》 지급보증거래 신청서(서면.전자 지급보증 겸용) | 원본 PDF 인쇄 개정 표기 및 출처 URL 기준 | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5060703_20160707.pdf) |
| `hana_official_149` | 《기업》금융거래확인서 | 원본 PDF 인쇄 개정 표기 및 출처 URL 기준 | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5060189_20160707.pdf) |
| `hana_official_157` | 여신거래용 인감명판 등 신고서 | 원본 PDF 인쇄 개정 표기 및 출처 URL 기준 | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5090002_20160707.pdf) |
| `hana_official_199` | 외화송금신청서 | (2026.05 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070103/__icsFiles/afieldfile/2026/06/02/3-09-0131_260602.pdf) |
| `hana_official_408` | 본인확인서(FATCA CRS 개인,개인사업자용)(국문) | (2024.10 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/07/29/5-08-0334.pdf) |
| `hana_official_413` | 고객확인서(법인,고유번호나 납세번호가 있는 임의 단체용) | (2026.06 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/06/17/3-08-1301.pdf) |
| `hana_official_414` | [필수] 개인(신용)정보 수집·이용·제공 동의서 [공공마이데이터 주민등록 등·초본 조회용] | 원본 PDF 인쇄 개정 표기 및 출처 URL 기준 | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/06/10/7-08-0039.pdf) |
| `hana_official_416` | [필수] 개인(신용)정보 수집·이용·제공 동의서 [공공마이데이터 사업자정보 조회용] | 원본 PDF 인쇄 개정 표기 및 출처 URL 기준 | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2026/06/10/7-08-0035.pdf) |
| `hana_official_419` | [필수] 개인(신용)정보 수집 · 이용 동의서 (비여신 금융거래) | (2025.08 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2025/08/20/3-08-1294.pdf) |
| `hana_official_420` | 비대면 계좌개설 안심차단 서비스 신청서 | (2025.05 개정) | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2025/05/09/5-08-0737.pdf) |
| `hana_official_428` | 본인확인서(FATCA CRS 법인,임의단체용)(국문) | 원본 PDF 인쇄 개정 표기 및 출처 URL 기준 | [원문](https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2024/01/05/5-08-0335.pdf) |
| `gov_business_registration` | 사업자등록증 | <개정 2014.3.14> | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=162624673&bylClsCd=110202) |
| `gov_business_proof` | 사업자등록증명 | < 2025. 08. 12.개정> | [원문](https://www.law.go.kr/LSW/flDownload.do?flSeq=155626677&flNm=%5B%EB%B3%84%EC%A7%80+5%5D+%EC%82%AC%EC%97%85%EC%9E%90%EB%93%B1%EB%A1%9D%EC%A6%9D%EB%AA%85%28%EA%B5%AD%EB%AC%B8%29&bylClsCd=200203) |
| `gov_vat_base` | 부가가치세 과세표준증명 | <2020. 11. 1. 개정> | [원문](https://www.law.go.kr/LSW/flDownload.do?flSeq=155626701&flNm=%5B%EB%B3%84%EC%A7%80+9%5D+%EB%B6%80%EA%B0%80%EA%B0%80%EC%B9%98%EC%84%B8%EA%B3%BC%EC%84%B8%ED%91%9C%EC%A4%80%EC%A6%9D%EB%AA%85%28%EA%B5%AD%EB%AC%B8%29&bylClsCd=200203) |
| `gov_vat_exempt_income` | 면세사업자 수입금액증명 | 원문에 인쇄된 서식 번호·개정 표기 기준 | [원문](https://www.law.go.kr/LSW/flDownload.do?flSeq=155626713&flNm=%5B%EB%B3%84%EC%A7%80+11%5D+%EB%B6%80%EA%B0%80%EA%B0%80%EC%B9%98%EC%84%B8%EB%A9%B4%EC%84%B8%EC%82%AC%EC%97%85%EC%9E%90+%EC%88%98%EC%9E%85%EA%B8%88%EC%95%A1%EC%A6%9D%EB%AA%85%28%EA%B5%AD%EB%AC%B8%29&bylClsCd=200203) |
| `gov_financial_proof` | 표준재무제표증명 | <2024. 4. 17. 개정> | [원문](https://www.law.go.kr/LSW/flDownload.do?flSeq=155626725&flNm=%5B%EB%B3%84%EC%A7%80+13%5D+%ED%91%9C%EC%A4%80%EC%9E%AC%EB%AC%B4%EC%A0%9C%ED%91%9C%EC%A6%9D%EB%AA%85%28%EA%B5%AD%EB%AC%B8%29&bylClsCd=200203) |
| `gov_income` | 소득금액증명 | <2024. 4. 17. 개정> | [원문](https://www.law.go.kr/LSW/flDownload.do?flSeq=155626737&flNm=%5B%EB%B3%84%EC%A7%80+15%5D+%EC%86%8C%EB%93%9D%EA%B8%88%EC%95%A1%EC%A6%9D%EB%AA%85%28%EA%B5%AD%EB%AC%B8%29&bylClsCd=200203) |
| `gov_tax_payment_history` | 납부내역증명 | <2024. 4. 17. 개정> | [원문](https://www.law.go.kr/LSW/flDownload.do?flSeq=155626763&flNm=%5B%EB%B3%84%EC%A7%80+19%5D+%EB%82%A9%EB%B6%80%EB%82%B4%EC%97%AD%EC%A6%9D%EB%AA%85%28%EA%B5%AD%EB%AC%B8%29&bylClsCd=200203) |
| `gov_national_tax` | 납세증명서 | 원문에 인쇄된 서식 번호·개정 표기 기준 | [원문](https://www.law.go.kr/flDownload.do?bylClsCd=110202&flSeq=114053165&gubun=) |
| `gov_seal` | 인감증명서 | <개정 2024. 5. 7.> | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=145953337&bylClsCd=110202) |
| `gov_signature` | 본인서명사실확인서 | <개정 2024. 4. 2.> | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=145951719&bylClsCd=110202) |
| `gov_pension` | 국민연금가입자 증명서 | <개정2011.12.8> | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=161706061&bylClsCd=110202) |
| `gov_building_unit` | 집합건축물대장(전유부, 갑) | <개정 2023. 8. 1.> | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=155204921&bylClsCd=110202) |
| `gov_building_general` | 일반건축물대장(갑) | <개정 2023. 8. 1.> | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=155204859&bylClsCd=110202) |
| `gov_land` | 토지대장 | <개정2017. 1. 31.> | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=162454805&bylClsCd=110202) |
| `gov_local_assessment` | 지방세 세목별 과세증명서 | <개정 2024. 12. 31.> | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169943579&bylClsCd=110202) |
| `gov_foreign_household` | 외국인체류확인서 | 원문에 인쇄된 서식 번호·개정 표기 기준 | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169477471&bylClsCd=110202) |
| `gov_resident_copy` | 주민등록표(등본) | <개정 2026. 4. 28.> | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=167818361&bylClsCd=110202) |
| `gov_resident_abstract` | 주민등록표(초본) | <개정 2026. 4. 28.> | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=167818367&bylClsCd=110202) |
| `gov_move_in` | 전입세대확인서 | <개정 2026. 4. 28.> | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=167818343&bylClsCd=110202) |
| `gov_local_tax` | 지방세 납세증명(신청)서 | <개정 2024. 12. 31.> | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=169946943&bylClsCd=110202) |
| `hana_personal_agreement` | 대출거래약정서(가계용) | (10-1) (210×297) NCR74g/㎡ (2021.03 개정) | [원문](https://image.kebhana.com/cont/download/documents/provide/0000003061040_20210325.pdf) |
| `hana_corporate_agreement` | 여신거래약정서(기업용) | (4-1) (2026.06 개정) | [원문](https://image.kebhana.com/cont/download/documents/provide/0000003061032_20260630.pdf) |
| `hana_collateral_agreement` | 근저당권설정계약서(근담보용) | (6-1) (2021.10 개정) | [원문](https://image.kebhana.com/cont/download/documents/provide/0000000001049_20211126.pdf) |
| `hana_specific_guarantee` | 보증서(특정채무보증용) | (4-1) (2021.03 개정) | [원문](https://image.kebhana.com/cont/download/documents/provide/b000003061059_20210325.pdf) |
| `gov_withholding` | 근로소득 원천징수영수증 | <개정 2025. 3. 21.> | [원문](https://www.law.go.kr/flDownload.do?gubun=&flSeq=150204063&bylClsCd=110202) |
| `gov_retirement_withholding` | 퇴직소득 원천징수영수증 | <개정 2025. 3. 21.> | [원문](https://www.law.go.kr/flDownload.do?gubun=&flSeq=150204063&bylClsCd=110202) |
| `gov_pension_withholding` | 연금소득 원천징수영수증 | <개정 2019. 3. 20.> | [원문](https://www.law.go.kr/flDownload.do?gubun=&flSeq=150204063&bylClsCd=110202) |
| `gov_business_registration_corp` | 사업자등록증(법인사업자) | <개정 2014.3.14> | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=162624673&bylClsCd=110202) |
| `gov_income_tax_return` | 종합소득세 과세표준확정신고 및 납부계산서(일반) | 2026.03.20 개정, 별지 제40호서식(1) | [원문](https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=164463209&bylClsCd=110202) |
