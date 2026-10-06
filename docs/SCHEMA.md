# 정답 키 스키마

`python scripts/build_schema.py` 로 자동 생성된 문서입니다. 서류별로 프로필 30개를 렌더링해 집계했습니다.
기계용 목록은 [schema/schema.json](../schema/schema.json) 에 있습니다.

## 키 규칙

- **형식:** 영어 snake_case, 점(.)으로 중첩합니다. `역할.속성` 순서입니다 (예: `applicant.name`, `company.biz_no`, `loan.amount`).
- **반복 항목:** 리스트 순번이 들어갑니다 (`rows.0.amount`, `rows.1.amount`). 이 문서에서는 `rows[].amount` 로 적습니다.
- **같은 뜻은 같은 속성 이름:** 성명 `name`, 주민번호 `rrn`, 생년월일 `birth`, 성별 `gender`, 주소 `address`, 전화 `phone`/`mobile`,
  사업자번호 `biz_no`, 법인등록번호 `corp_reg_no`, 대표자 `ceo`, 발급일 `issue_date`, 발급기관 `issuer`, 발급번호 `issue_no`.
  내보낼 때 바꾸는 동의어: `dob`→`birth`, `date_of_birth`→`birth`, `sex`→`gender`, `corp_no`→`corp_reg_no`, `ceo_name`→`ceo`, `tel`→`phone`
- **도장·서명:** `seal.<자리>` (도장), `sign.<자리>` (서명). 정답 값은 있으면 `true`, 없으면 `false` 입니다.
  자리 이름 예: `issuer` 발급기관 직인, `corp` 법인인감, `applicant` 신청인, `debtor` 채무자, `guarantor` 보증인, `staff.clerk` 담당 행원.
- **빈 칸:** 문서에 항목명은 있는데 값이 비어 있으면 `null` 입니다.
- **체크박스:** 정답 값은 체크된 보기의 글자입니다 (없으면 `null`). 보기 전체와 체크 여부·위치는 라벨의 `options` 에 있습니다.
  복수 선택은 리스트입니다 (`marketing.channels[]`).

## 값 타입

| 타입 | 정규화 값(norm) |
|---|---|
| text | 표시값 그대로 |
| date / month / datetime | `YYYY-MM-DD` / `YYYY-MM` / `YYYY-MM-DDTHH:MM` |
| amount / number / percent | 숫자 (원 단위 정수, 외화는 소수) |
| amount_korean | 한글 금액을 숫자로 (`금 이억일천사백만원정` → 214000000) |
| rrn / biz_no / corp_reg_no | 표시값 그대로 (마스킹 `*` 포함) |
| phone | 숫자만 |
| account_no | 표시값 그대로 |
| checkbox / checkbox_multi | 체크된 보기 |
| seal / signature | `present` (bool) |

"채움률"은 프로필 30개 중 그 키가 문서에 나온 비율입니다 (선택 항목·반복 항목은 100% 미만).
채움률 0% 인 키는 드문 변형(내용이 많은 경우·특수 상황)에서만 나오는 키입니다 (변형을 모두 켠 생성에서 수집). 변형 목록은 [docs/variants/](variants/) 에 있습니다.


## 신원·신분


### 주민등록증 (`resident_id_card`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `name` | 성명 | text | 100% | 박찬연 |
| `name_hanja` | 한자성명 | text | 93% | 朴讚姸 |
| `rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `issue_date` | 발급일 | date | 100% | 2020. 4. 22. |
| `issuer` | 발급기관 | text | 100% | 서울특별시 서초구청장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 서초구청장인 |
| `resident_type` | 재외국민 | text | 3% | 재외국민 |

### 운전면허증 (`driver_license`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `license_type` | 면허종류 | text | 100% | 2종보통 |
| `serial` | 암호일련번호 | text | 100% | X0T6QD |
| `license_no` | 면허번호 | text | 100% | 11-14-634523-71 |
| `name` | 성명 | text | 100% | 박찬연 |
| `rrn` | 주민등록번호 | rrn | 100% | 900210-1****** |
| `address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `renewal_period` | 갱신기간 | text | 67% | 2035.01.01~2035.12.31 |
| `issue_date` | 발급일 | date | 100% | 2025.12.02 |
| `issuer` | 발급기관 | text | 100% | 서울특별시경찰청장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 경찰청장인 |
| `aptitude_period` | 적성검사기간 | text | 33% | 2034.01.01~2034.12.31 |
| `condition` | 조건 | text | 10% | A |

### 여권 (`passport`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `type` | 종류/Type | text | 100% | PM |
| `country_code` | 발행국/Issuingcountry | text | 100% | KOR |
| `passport_no` | 여권번호/PassportNo. | text | 100% | M93151969 |
| `surname` | 성/Surname | text | 100% | PARK |
| `given_names` | 이름/Givennames | text | 100% | CHANYEON |
| `name_korean` | 한글성명 | text | 100% | 박찬연 |
| `nationality` | 국적/Nationality | text | 100% | REPUBLIC OF KOREA |
| `birth` | 생년월일/Dateofbirth | text | 100% | 10 FEB 1990 |
| `gender` | 성별/Sex | text | 100% | M |
| `personal_no` | 주민등록번호/PersonalNo. | text | 47% | 1****** |
| `date_of_issue` | 발급일/Dateofissue | text | 100% | 30 AUG 2018 |
| `date_of_expiry` | 기간만료일/Dateofexpiry | text | 100% | 29 AUG 2028 |
| `authority` | 발행관청/Authority | text | 100% | MINISTRY OF FOREIGN AFFAIRS |
| `mrz.line1` | MRZ | text | 100% | PMKORPARK<<CHANYEON<<<<<<<<<<<<<<<<<<<<<… |
| `mrz.line2` | MRZ | text | 100% | M931519697KOR9002100M2808299<<<<<<<<<<<<… |

### 외국인등록증 (`alien_registration_card`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `registration_no` | 외국인등록번호 | rrn | 100% | 011031-8341376 |
| `name` | 성명 | text | 100% | HOANG NGOC ANH |
| `country` | 국가/지역 | text | 100% | VIETNAM |
| `gender` | 성별 | text | 100% | F |
| `visa_status` | 체류자격 | text | 100% | 비전문취업(E-9) |
| `issue_date` | 발급일자 | date | 100% | 2025.12.09 |
| `issuer` | 발급기관 | text | 100% | 서울남부출입국·외국인사무소장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 출입국장인 |

### 인감증명서 (`seal_certificate`) — 키 20개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `doc_no` | 인감증명서발급사실확인용번호 | text | 100% | 7043-3278-9148 |
| `applicant_type` | 발급구분 | checkbox | 100% | 본인 |
| `seal.registered` | 등록인감 | seal | 100% | 박찬연인 |
| `seal_name` | 인감 | text | 100% | 박찬연인 |
| `person.name` | 성명 | text | 100% | 박찬연 |
| `person.name_hanja` | 한자 | text | 100% | 朴讚姸 |
| `person.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `person.nationality` | 국적 | text | 100% | 대한민국 |
| `person.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `usage_type` | 용도 | checkbox | 100% | 일반용 |
| `issue_date` | 발급일 | date | 100% | 2026년 1월 31일 |
| `issuer` | 발급기관 | text | 100% | 서울특별시 서초구 방배동장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 직인 |
| `buyer.name` | 성명(법인명) | text | 10% | 최다희 |
| `buyer.rrn` | 주민등록번호(법인등록번호) | rrn | 10% | 630929-2087142 |
| `buyer.address` | 주소(법인소재지) | text | 10% | 서울특별시 송파구 송파대로 179 |
| `applicant_signature` | 발급신청자서명 | text | 10% | 송소경 |
| `agent.name` | 성명 | text | 7% | 송소경 |
| `agent.rrn` | 주민등록번호 | rrn | 7% | 580414-2****** |
| `remark` | 비고 | text | 0% | 법정대리인(모) 전영경 동의 |

### 본인서명사실확인서 (`signature_confirmation`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `doc_no` | 문서확인번호 | text | 100% | 2169-2497-2882-0522 |
| `signer.name` | 성명 | text | 100% | 박찬연 |
| `signer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `signer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `other_usage` | 그외의용도 | text | 40% | 대출보증용 |
| `signature` | 서명 | text | 100% | 박찬연 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 서울특별시 서초구 방배동장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 직인 |
| `real_estate_usage` | 부동산관련용도및자동차매도용도 | checkbox | 60% | 소유권 이전(매매, 증여 등) |
| `counterparty.name` | 성명(법인명) | text | 57% | 이서우 |
| `counterparty.rrn` | 주민등록번호(법인등록번호) | rrn | 57% | 930301-2699865 |
| `counterparty.address` | 주소 | text | 57% | 전라남도 여수시 시청로 126, 115동 1503호 |
| `delegate.name` | 성명 | text | 10% | 엄주영 |
| `delegate.address` | 주소 | text | 10% | 서울특별시 종로구 자하문로 92, 114동 504호 |

## 가족관계


### 주민등록표 등본 (`resident_registration_copy`) — 키 26개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `doc_no` | 문서확인번호 | text | 100% | 제 1639 호 |
| `officer` | 담당자 | text | 40% | 양경예 |
| `officer_phone` | 전화 | phone | 40% | 02-4484-9569 |
| `applicant` | 신청인 | text | 100% | 박찬연 |
| `purpose` | 용도및목적 | text | 100% | 대출신청 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 서울특별시 서초구 방배동장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 직인 |
| `household_head.name` | 세대주성명 | text | 100% | 박영준 |
| `household_head.name_hanja` | 세대주성명(한자) | text | 100% | 朴英準 |
| `household_formed.reason` | 세대구성사유 | text | 100% | 전입세대구성 |
| `household_formed.date` | 세대구성일자 | date | 100% | 2007-07-23 |
| `past_addresses[].no` | 번호 | number | 50% | 1 |
| `past_addresses[].address` | 주소 | text | 50% | 서울특별시 송파구 올림픽로 273 (방이동) |
| `past_addresses[].moved_in` | 전입일/변동일 | date | 50% | 1983-06-20 |
| `past_addresses[].reason` | 변동사유 | text | 50% | 전입 |
| `current_address.address` | 현주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `current_address.moved_in` | 전입일/변동일 | date | 100% | 2007-07-23 |
| `current_address.reason` | 변동사유 | text | 100% | 전입 |
| `members[].no` | 번호 | number | 100% | 1 |
| `members[].relation` | 세대주관계 | text | 100% | 본인 |
| `members[].name` | 성명 | text | 100% | 박영준 |
| `members[].name_hanja` | 한자 | text | 100% | 朴英準 |
| `members[].moved_in` | 전입일/변동일 | date | 100% | 2007-07-23 |
| `members[].reason` | 변동사유 | text | 100% | 전입 |
| `members[].rrn` | 주민등록번호 | rrn | 100% | 621219-1****** |

### 주민등록표 초본 (`resident_registration_abstract`) — 키 23개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `doc_no` | 문서확인번호 | text | 100% | 6319-1340-7703-9808 |
| `applicant` | 신청인 | text | 100% | 박찬연 |
| `purpose` | 용도및목적 | text | 100% | 금융기관제출 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 서울특별시 서초구청장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 직인 |
| `person.name` | 성명 | text | 100% | 박찬연 |
| `person.name_hanja` | 한자 | text | 100% | 朴讚姸 |
| `person.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `history_scope` | 주소변동사항 | text | 100% | 최근 5년 |
| `addresses[].no` | 번호 | number | 100% | 1 |
| `addresses[].address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `addresses[].moved_in` | 전입일 | date | 100% | 2018-10-20 |
| `addresses[].changed` | 변동일 | date | 100% | 2018-10-20 |
| `addresses[].head_relation` | 세대주및관계 | text | 100% | 박영준의 자 |
| `addresses[].status` | 등록상태 | text | 100% | 거주자 |
| `addresses[].reason` | 변동사유 | text | 100% | 전입 |
| `officer` | 담당자 | text | 47% | 서규은 |
| `officer_phone` | 전화 | phone | 47% | 02-4755-9378 |
| `person_changes[].no` | 번호 | number | 13% | 1 |
| `person_changes[].content` | 변경내용 | text | 13% | 성명 이태린(李泰麟) → 이민빈(李旻彬) |
| `person_changes[].changed` | 변동일 | date | 13% | 1997-04-13 |
| `person_changes[].reason` | 변동사유 | text | 13% | 개명 |

### 가족관계증명서 (`family_relation_certificate`) — 키 26개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `cert_type` | 증명서종류 | text | 100% | 일반 |
| `reg_base` | 등록기준지 | text | 100% | 서울특별시 종로구 평창동 851-12 |
| `self.relation` | 구분 | text | 100% | 본인 |
| `self.name` | 성명 | text | 100% | 박찬연 |
| `self.name_hanja` | 성명(한자) | text | 100% | 朴讚姸 |
| `self.birth` | 출생연월일 | date | 100% | 1990년 02월 10일 |
| `self.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `self.gender` | 성별 | text | 100% | 남 |
| `self.bon` | 본 | text | 100% | 密陽 |
| `family[].relation` | 구분 | text | 100% | 부 |
| `family[].name` | 성명 | text | 100% | 박영준 |
| `family[].name_hanja` | 성명(한자) | text | 100% | 朴英準 |
| `family[].birth` | 출생연월일 | date | 100% | 1962년 12월 19일 |
| `family[].rrn` | 주민등록번호 | rrn | 100% | 621219-1****** |
| `family[].gender` | 성별 | text | 100% | 남 |
| `family[].bon` | 본 | text | 100% | 密陽 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 법원행정처 전산정보중앙관리소 전산운영책임관 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 전산운영책임관인 |
| `issue_time` | 발급시각 | text | 100% | 16시 15분 |
| `applicant` | 신청인 | text | 100% | 박찬연 |
| `doc_check_no` | 문서확인번호 | text | 47% | 4446-8180-3034-4028 |
| `officer` | 발급담당자 | text | 53% | 최정주 |
| `officer_phone` | 전화 | phone | 53% | 02-6654-0284 |
| `family[].status` | 사망 | text | 20% | 사망 |
| `family[].nationality` | 국적 | text | 0% | 중국 |

### 기본증명서 (`basic_certificate`) — 키 33개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `cert_type` | 증명서종류 | text | 100% | 상세 |
| `reg_base` | 등록기준지 | text | 100% | 서울특별시 종로구 평창동 851-12 |
| `self.relation` | 구분 | text | 100% | 본인 |
| `self.name` | 성명 | text | 100% | 박찬연 |
| `self.name_hanja` | 성명(한자) | text | 100% | 朴讚姸 |
| `self.birth` | 출생연월일 | date | 100% | 1990년 02월 10일 |
| `self.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `self.gender` | 성별 | text | 100% | 남 |
| `self.bon` | 본 | text | 100% | 密陽 |
| `birth.place` | 출생장소 | text | 100% | 부산광역시 부산진구 전포동 |
| `birth.reported` | 신고일 | date | 100% | 1990년 02월 24일 |
| `birth.reporter` | 신고인 | text | 100% | 모 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 법원행정처 전산정보중앙관리소 전산운영책임관 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 전산운영책임관인 |
| `issue_time` | 발급시각 | text | 100% | 06시 20분 |
| `applicant` | 신청인 | text | 100% | 박찬연 |
| `doc_check_no` | 문서확인번호 | text | 33% | 8334-0642-5397-9222 |
| `officer` | 발급담당자 | text | 67% | 채선원 |
| `officer_phone` | 전화 | phone | 67% | 055-748-8832 |
| `name_change.permitted` | 개명허가일 | date | 3% | 1997년 03월 26일 |
| `name_change.court` | 허가법원 | text | 3% | 서울가정법원 |
| `name_change.old_name` | 개명전이름 | text | 3% | 이태린 |
| `name_change.reported` | 신고일 | date | 3% | 1997년 04월 13일 |
| `naturalization.acquired` | 국적취득일 | date | 0% | 2008년 11월 04일 |
| `naturalization.reason` | 국적취득사유 | text | 0% | 귀화허가 |
| `naturalization.prev_nationality` | 종전국적 | text | 0% | 중국 |
| `naturalization.notified` | 통보일 | date | 0% | 2008년 11월 11일 |
| `naturalization.notifier` | 통보자 | text | 0% | 법무부장관 |
| `correction.permitted` | 정정허가일 | date | 0% | 2013년 02월 21일 |
| `correction.court` | 허가법원 | text | 0% | 서울가정법원 |
| `correction.content` | 정정내용 | text | 0% | 성별 여 → 남 |
| `correction.reported` | 신고일 | date | 0% | 2013년 02월 24일 |

### 혼인관계증명서 (`marriage_relation_certificate`) — 키 36개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `cert_type` | 증명서종류 | text | 100% | 일반 |
| `reg_base` | 등록기준지 | text | 100% | 서울특별시 종로구 평창동 851-12 |
| `self.relation` | 구분 | text | 100% | 본인 |
| `self.name` | 성명 | text | 100% | 박찬연 |
| `self.name_hanja` | 성명(한자) | text | 100% | 朴讚姸 |
| `self.birth` | 출생연월일 | date | 100% | 1990년 02월 10일 |
| `self.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `self.gender` | 성별 | text | 100% | 남 |
| `self.bon` | 본 | text | 100% | 密陽 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 서울특별시 서초구청장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 직인 |
| `issue_time` | 발급시각 | text | 100% | 09시 13분 |
| `officer` | 발급담당자 | text | 40% | 황숙율 |
| `officer_phone` | 전화 | phone | 40% | 02-598-1196 |
| `applicant` | 신청인 | text | 100% | 박찬연 |
| `spouse.relation` | 구분 | text | 70% | 배우자 |
| `spouse.name` | 성명 | text | 70% | 이도민 |
| `spouse.name_hanja` | 성명(한자) | text | 70% | 李度民 |
| `spouse.birth` | 출생연월일 | date | 70% | 1967년 09월 21일 |
| `spouse.rrn` | 주민등록번호 | rrn | 70% | 670921-1882767 |
| `spouse.gender` | 성별 | text | 70% | 남 |
| `spouse.bon` | 본 | text | 70% | 廣州 |
| `marriage.reported` | 신고일 | date | 70% | 1995년 05월 07일 |
| `marriage.spouse_name` | 배우자 | text | 70% | 이도민 |
| `marriage.spouse_rrn` | 배우자의주민등록번호 | rrn | 70% | 670921-1882767 |
| `marriage.office` | 처리관서 | text | 70% | 서울특별시 송파구 |
| `doc_check_no` | 문서확인번호 | text | 60% | 5542-8548-2400-0602 |
| `past_events[].kind` | 구분 | text | 0% | 혼인 |
| `past_events[].reported` | 신고일 | date | 0% | 2014년 04월 09일 |
| `past_events[].spouse_name` | 배우자 | text | 0% | 이바노바안나(IVANOVA ANNA) |
| `past_events[].spouse_nationality` | 배우자국적 | text | 0% | 러시아 |
| `past_events[].spouse_birth` | 배우자의출생연월일 | date | 0% | 1991년 01월 11일 |
| `past_events[].office` | 처리관서 | text | 0% | 서울특별시 송파구 |
| `past_events[].judgment_date` | 이혼판결확정일 | date | 0% | 2008년 04월 30일 |
| `past_events[].court` | 법원 | text | 0% | 수원가정법원 |

## 소득·재직


### 재직증명서 (`employment_certificate`) — 키 22개

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

### 경력증명서 (`career_certificate`) — 키 20개

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

### 급여명세서 (`pay_stub`) — 키 28개

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

### 근로계약서 (`employment_contract`) — 키 31개

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

### 근로소득 원천징수영수증 (`withholding_receipt`) — 키 48개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `copy_type` | 보관용구분 | checkbox | 100% | 소득자 보관용 |
| `year` | 귀속연도 | number | 100% | 2024 |
| `resident` | 거주구분 | checkbox | 100% | 거주자1 |
| `nationality` | 내·외국인 | checkbox | 100% | 내국인1 |
| `household_head` | 세대주여부 | checkbox | 100% | 세대주1 |
| `settlement_type` | 연말정산구분 | checkbox | 100% | 계속근로1 |
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

### 소득금액증명원 (`income_certificate`) — 키 20개

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

### 국민연금 가입자 가입증명 (`pension_enrollment_certificate`) — 키 15개

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

### 건강보험 자격득실확인서 (`health_insurance_qualification`) — 키 10개

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

### 건강보험료 납부확인서 (`health_insurance_payment`) — 키 26개

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

## 세금·보험


### 납세증명서(국세완납증명) (`tax_payment_certificate`) — 키 22개

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
| `purpose_type` | 사용목적 | checkbox | 100% | 기타 |
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

### 납세증명서(법인) (`tax_payment_certificate_corp`) — 키 22개

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
| `purpose_type` | 사용목적 | checkbox | 100% | 기타 |
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

### 지방세 납세증명서 (`local_tax_payment_certificate`) — 키 18개

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

### 지방세 세목별 과세증명서 (`local_tax_assessment`) — 키 20개

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

### 부가가치세 과세표준증명 (`vat_tax_base_certificate`) — 키 19개

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

### 종합소득세 과세표준확정신고 및 납부계산서 (`income_tax_return`) — 키 68개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `tax_year` | 귀속연도 | number | 100% | 2024 |
| `residency` | 거주구분 | checkbox | 100% | 거주자 |
| `nationality` | 내ㆍ외국인 | checkbox | 100% | 내국인 |
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

## 금융거래


### 통장사본 (`bankbook_copy`) — 키 22개

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

### 거래내역확인서 (`bank_statement`) — 키 21개

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

### 잔액증명서 (`balance_certificate`) — 키 20개

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

### 부채증명서 (`debt_certificate`) — 키 23개

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
| `guarantee` | 보증채무 | checkbox | 100% | 없음 |
| `overdue` | 연체여부 | text | 100% | 없음 |
| `purpose` | 용도 | text | 100% | 법원 제출용 |
| `issue_date` | 발급일 | date | 100% | 2026년 1월 31일 |
| `issuer` | 발급점 | text | 100% | 기업은행 범어지점장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 범어지점장인 |
| `guarantee_detail` | 보증내역 | text | 20% | 채욱정 차주 전세자금대출 연대보증 10,000,000원 |
| `overdue_detail` | 연체내역 | text | 10% | 개인사업자대출(472-84-246131) 연체 47일, 연체원리금 2,0… |

### 신용카드 이용대금명세서 (`card_statement`) — 키 30개

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

## 부동산


### 등기사항전부증명서(집합건물) (`real_estate_registry`) — 키 84개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `property` | 부동산의표시 | text | 100% | 경기도 수원시 영통구 원천동 87 한신휴플러스에듀포레 제115동 제21층… |
| `unique_no` | 고유번호 | text | 100% | 1792-2013-094176 |
| `buildings[].display_no` | 표시번호 | number | 80% | 1 |
| `buildings[].receipt` | 접수 | date | 80% | 1994년11월4일 |
| `buildings[].location` | 소재지번,건물명칭및번호 | text | 80% | 경기도 수원시 영통구 원천동 87 한신휴플러스에듀포레 제115동 |
| `buildings[].detail` | 건물내역 | text | 80% | 철근콘크리트구조 (철근)콘크리트지붕 21층 공동주택(아파트) 지하1층 1… |
| `buildings[].cause` | 등기원인및기타사항 | text | 80% | 도면편철장 제8책 제698장 |
| `land.display_no` | 표시번호 | number | 80% | 1 |
| `land.location` | 소재지번 | text | 80% | 1. 경기도 수원시 영통구 원천동 87 |
| `land.category` | 지목 | text | 80% | 대 |
| `land.area` | 면적 | text | 80% | 31,054.7㎡ |
| `land.cause` | 등기원인및기타사항 | text | 80% | 1994년11월4일 등기 |
| `unit.display_no` | 표시번호 | number | 80% | 1 |
| `unit.receipt` | 접수 | date | 80% | 1994년11월4일 |
| `unit.unit_no` | 건물번호 | text | 80% | 제21층 제2104호 |
| `unit.detail` | 건물내역 | text | 80% | 철근콘크리트구조 101.84㎡ |
| `unit.cause` | 등기원인및기타사항 | text | 80% | 도면편철장 제8책 제698장 |
| `land_right.display_no` | 표시번호 | number | 80% | 1 |
| `land_right.kind` | 대지권종류 | text | 80% | 1 소유권대지권 |
| `land_right.ratio` | 대지권비율 | text | 80% | 31,054.7분의 54.47 |
| `land_right.cause` | 등기원인및기타사항 | text | 80% | 1994년10월19일 대지권 1994년11월4일 등기 |
| `gapgu[].rank` | 순위번호 | number | 80% | 1 |
| `gapgu[].purpose` | 등기목적 | text | 80% | 소유권보존 |
| `gapgu[].receipt` | 접수 | text | 80% | 1994년11월4일 제30434호 |
| `gapgu[].holder.role` | 권리자구분 | text | 80% | 소유자 |
| `gapgu[].holder.name` | 소유자 | text | 80% | 주식회사쌍용건설 |
| `gapgu[].holder.reg_no` | 등록번호 | text | 80% | 171512-4430096 |
| `gapgu[].holder.address` | 주소 | text | 80% | 경기도 수원시 영통구 시청로 108 |
| `gapgu[].cause` | 등기원인 | text | 80% | 2020년1월13일 매매 |
| `gapgu[].holder.note` | 거래가액 | text | 63% | 거래가액 금410,000,000원 |
| `eulgu[].rank` | 순위번호 | number | 70% | 1 |
| `eulgu[].purpose` | 등기목적 | text | 70% | 근저당권설정 |
| `eulgu[].receipt` | 접수 | text | 70% | 2020년2월18일 제40565호 |
| `eulgu[].cause` | 등기원인 | text | 70% | 2020년2월18일 설정계약 |
| `eulgu[].max_amount` | 채권최고액 | amount | 67% | 금318,000,000원 |
| `eulgu[].debtor` | 채무자 | text | 67% | 박기우 |
| `eulgu[].debtor_address` | 채무자주소 | text | 67% | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신… |
| `eulgu[].mortgagee` | 근저당권자 | text | 67% | 주식회사우리은행 171511-7786133 |
| `eulgu[].mortgagee_address` | 근저당권자주소 | text | 67% | 서울특별시 중구 소공로 51 (송도지점) |
| `registry_office` | 관할등기소 | text | 80% | 수원지방법원 등기과 |
| `view_datetime` | 열람일시 | datetime | 47% | 2026년01월31일 15시31분14초 |
| `gapgu[].holders[].role` | 권리자구분 | text | 17% | 공유자 |
| `gapgu[].holders[].share` | 지분 | text | 17% | 지분 2분의 1 |
| `gapgu[].holders[].name` | 공유자 | text | 17% | 반원인 |
| `gapgu[].holders[].reg_no` | 등록번호 | text | 17% | 580519-******* |
| `gapgu[].holders[].address` | 주소 | text | 17% | 대구광역시 수성구 수성로 401, 107동 2004호 (지산동, 센트레빌… |
| `gapgu[].note` | 거래가액 | text | 13% | 거래가액 금470,000,000원 |
| `gapgu[].claim_amount` | 청구금액 | amount | 30% | 금4,134,361원 |
| `gapgu[].creditor` | 채권자 | text | 33% | 주식회사삼성카드 130111-2186484 |
| `gapgu[].creditor_address` | 채권자주소 | text | 33% | 서울특별시 중구 국제금융로 331 |
| `fee` | 수수료 | amount | 43% | 1,000원 |
| `issue_date` | 발행일 | date | 43% | 2025년 5월 19일 |
| `seal.issuer` | 발급기관직인 | seal | 43% | 전산운영책임관인 |
| `issue_no` | 발행번호 | number | 53% | 88889704605527375125 |
| `confirm_no` | 발급확인번호 | text | 53% | NTOZ-IUSA-4727 |
| `issue_date_short` | 발행일 | date | 53% | 2025/05/19 |
| `eulgu[].deposit` | 전세금 | amount | 17% | 금345,000,000원 |
| `eulgu[].rent` | 차임 | text | 13% | 없음 |
| `eulgu[].scope` | 범위 | text | 17% | 주거용 건물의 전부 |
| `eulgu[].contract_date` | 임대차계약일자 | date | 13% | 2012년9월4일 |
| `eulgu[].resident_date` | 주민등록일자 | date | 13% | 2012년10월6일 |
| `eulgu[].possession_date` | 점유개시일자 | date | 13% | 2012년10월6일 |
| `eulgu[].fixed_date` | 확정일자 | date | 13% | 2012년10월7일 |
| `eulgu[].lessee` | 임차권자 | text | 13% | 박윤성 880417-******* |
| `eulgu[].lessee_address` | 임차권자주소 | text | 13% | 전라남도 여수시 좌수영로 575, 105동 604호 (문수동, 현대파크) |
| `summary.owners[].name` | 등기명의인 | text | 20% | 이민빈 (소유자) |
| `summary.owners[].reg_no` | (주민)등록번호 | text | 20% | 720524-******* |
| `summary.owners[].share` | 최종지분 | text | 20% | 단독소유 |
| `summary.owners[].address` | 주소 | text | 20% | 서울특별시 마포구 월드컵로 491-5, 118동 1203호 (상암동, e… |
| `summary.owners[].rank` | 순위번호 | number | 20% | 4 |
| `summary.rights[].rank` | 순위번호 | number | 13% | 1 |
| `summary.rights[].purpose` | 등기목적 | text | 13% | 근저당권설정 |
| `summary.rights[].receipt` | 접수정보 | text | 13% | 2025년6월21일 제78131호 |
| `summary.rights[].main` | 주요등기사항 | text | 13% | 채권최고액 금361,000,000원  근저당권자 중소기업은행 |
| `summary.rights[].target_owner` | 대상소유자 | text | 13% | 이민빈 |
| `page_label` | 쪽번호 | text | 20% | 2/2 |
| `gapgu[].change` | 변경사항 | text | 13% | 김태유의 주소 세종특별자치시 갈매로 202, 123동 2504호 (보람동… |
| `eulgu[].change` | 변경사항 | text | 27% | 채권최고액 금131,000,000원 |
| `gapgu[].right_holder` | 권리자 | text | 13% | 국민건강보험공단 |
| `gapgu[].trust_no` | 신탁원부 | text | 13% | 신탁원부 제2022-9693호 |
| `eulgu[].period` | 존속기간 | text | 10% | 1996년4월24일부터 1998년4월23일까지 |
| `eulgu[].jeonse_holder` | 전세권자 | text | 10% | 마예태 900930-******* |
| `eulgu[].jeonse_holder_address` | 전세권자주소 | text | 10% | 서울특별시 송파구 백제고분로 29, 120동 903호 (문정동, 롯데캐슬… |
| `gapgu[].agency` | 처분청 | text | 7% | 북대전세무서 |

### 집합건축물대장(전유부) (`building_register`) — 키 32개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `confirm_no` | 문서확인번호 | text | 100% | 3188-4949-1246-2345 |
| `unique_no` | 고유번호 | text | 100% | 4156211400-3-00870000 |
| `building_name` | 명칭 | text | 100% | 한신휴플러스에듀포레 제115동 |
| `unit_name` | 호명칭 | text | 100% | 115동 2104호 |
| `site_location` | 대지위치 | text | 100% | 경기도 수원시 영통구 원천동 |
| `jibun` | 지번 | text | 100% | 87 |
| `road_address` | 도로명주소 | text | 100% | 경기도 수원시 영통구 매탄로 376 |
| `exclusive[].kind` | 구분 | text | 100% | 주 |
| `exclusive[].floor` | 층별 | text | 100% | 21층 |
| `exclusive[].structure` | 구조 | text | 100% | 철근콘크리트구조 |
| `exclusive[].usage` | 용도 | text | 100% | 아파트 |
| `exclusive[].area` | 면적(㎡) | number | 100% | 101.84 |
| `common[].kind` | 구분 | text | 100% | 주 |
| `common[].floor` | 층별 | text | 100% | 각층 |
| `common[].structure` | 구조 | text | 100% | 철근콘크리트구조 |
| `common[].usage` | 용도 | text | 100% | 계단실,복도,승강기 |
| `common[].area` | 면적(㎡) | number | 100% | 24.60 |
| `owners[].name` | 성명(명칭) | text | 100% | 주식회사쌍용건설 |
| `owners[].rrn` | 주민(법인)등록번호 | rrn | 100% | 171512-4430096 |
| `owners[].address` | 주소 | text | 100% | 경기도 수원시 영통구 시청로 108 |
| `owners[].share` | 소유권지분 | text | 100% | 1/1 |
| `owners[].change_date` | 변동일 | date | 100% | 1994.11.04 |
| `owners[].change_cause` | 변동원인 | text | 100% | 소유권보존 |
| `house_prices[].base_date` | 기준일 | date | 87% | 2025.01.01 |
| `house_prices[].price` | 공동주택(아파트)가격 | amount | 87% | 359,000,000 |
| `officer` | 담당자 | text | 100% | 민원여권과 |
| `officer_phone` | 전화 | phone | 100% | 031-410-6139 |
| `issue_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 수원시 영통구청장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 영통구청장인 |
| `owners_note` | 비고 | text | 37% | ※ 이 건축물대장은 현소유자만 표시한 것입니다. |
| `violation` | 위반건축물 | text | 3% | 위반건축물 |

### 토지대장 (`land_register`) — 키 26개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `unique_no` | 고유번호 | text | 100% | 4156211400-10087-0000 |
| `drawing_no` | 도면번호 | number | 100% | 47 |
| `issue_no` | 발급번호 | number | 100% | 202644552441 |
| `location` | 토지소재 | text | 100% | 경기도 수원시 영통구 원천동 |
| `sheet_no` | 장번호 | text | 100% | 1-2 |
| `processed_time` | 처리시각 | text | 100% | 15시 41분 19초 |
| `jibun` | 지번 | text | 100% | 87 |
| `scale` | 축척 | text | 100% | 1:1200 |
| `issuer_name` | 발급자 | text | 100% | 인터넷민원 |
| `land[].category` | 지목 | text | 100% | (08)대 |
| `land[].area` | 면적 | number | 100% | 34,688.3 |
| `land[].reason` | 사유 | text | 100% | (20)1992년 03월 13일 등록전환 |
| `owners[].change_date` | 변동일자 | date | 100% | 1994년 11월 04일 |
| `owners[].change_cause` | 변동원인 | text | 100% | (01)소유권보존 |
| `owners[].address` | 주소 | text | 100% | 경기도 수원시 영통구 시청로 108 |
| `owners[].name` | 성명또는명칭 | text | 100% | 주식회사쌍용건설 |
| `owners[].reg_no` | 등록번호 | text | 100% | 171512-4430096 |
| `owners[].co_owners` | 공유자 | text | 83% | 외 1,344인 |
| `grades[].date` | 등급수정년월일 | text | 100% | 1984.07.01. 수정 |
| `grades[].grade` | 토지등급 | number | 100% | 149 |
| `land_prices[].base_date` | 개별공시지가기준일 | date | 100% | 2020/01/01 |
| `land_prices[].price` | 개별공시지가 | amount | 100% | 2,529,000 |
| `zoning` | 용도지역 | text | 100% | 준주거지역 |
| `issue_date` | 발급일 | date | 100% | 2026년 1월 31일 |
| `issuer` | 발급기관 | text | 100% | 수원시 영통구청장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 영통구청장인 |

### 부동산 매매계약서 (`sales_contract`) — 키 50개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `property.location` | 소재지 | text | 100% | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신… |
| `property.land_category` | 지목 | text | 100% | 대 |
| `property.land_right` | 대지권 | text | 100% | 소유권대지권 31,054.7분의 54.47 |
| `property.land_area` | 면적 | text | 100% | 54.47㎡ |
| `property.structure` | 구조 | text | 100% | 철근콘크리트구조 |
| `property.usage` | 용도 | text | 100% | 공동주택(아파트) |
| `property.building_area` | 면적 | text | 100% | 101.84㎡ |
| `payment.price` | 매매대금 | amount | 100% | 금 오억육천만원정 (₩560,000,000) |
| `payment.down` | 계약금 | amount | 100% | 금 오천육백만원정 (₩56,000,000) |
| `payment.middle` | 중도금 | amount | 63% | 금 일억칠천만원정 (₩170,000,000) |
| `payment.middle_date` | 중도금지급일 | date | 63% | 2025년 10월 14일 |
| `payment.balance` | 잔금 | amount | 100% | 금 삼억삼천사백만원정 (₩334,000,000) |
| `payment.balance_date` | 잔금지급일 | date | 100% | 2025년 11월 03일 |
| `specials[]` | 특약사항 | text | 100% | 1. 현 시설물 상태의 계약이며, 매수인은 등기사항증명서 및 현장을 확인… |
| `contract_date` | 계약일 | date | 100% | 2025년 09월 16일 |
| `seller.address` | 주소 | text | 100% | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신… |
| `seller.rrn` | 주민등록번호 | rrn | 100% | 570508-1456825 |
| `seller.phone` | 전화 | phone | 100% | 010-6594-7883 |
| `seller.name` | 성명 | text | 100% | 박기우 |
| `seal.seller` | 매도인 | seal | 100% | 반원인 |
| `sign.seller` | 매도인 | signature | 100% | 여혜인 |
| `buyer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `buyer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `buyer.phone` | 전화 | phone | 100% | 010-5907-7253 |
| `buyer.name` | 성명 | text | 100% | 박찬연 |
| `seal.buyer` | 매수인 | seal | 100% | 강순준 |
| `sign.buyer` | 매수인 | signature | 100% | 박찬연 |
| `brokers[].office_address` | 사무소소재지 | text | 100% | 경기도 수원시 영통구 매탄로 29, 1층 108호 (원천동) |
| `brokers[].office_name` | 사무소명칭 | text | 100% | 한신휴공인중개사 |
| `brokers[].representative` | 대표 | text | 100% | 문채현 |
| `brokers[].reg_no` | 등록번호 | text | 100% | 29669-2012-02206 |
| `brokers[].phone` | 전화 | phone | 100% | 031-661-0605 |
| `co_seller.address` | 주소 | text | 23% | 대구광역시 수성구 수성로 401, 107동 2004호 (지산동, 센트레빌… |
| `co_seller.rrn` | 주민등록번호 | rrn | 23% | 590110-1645169 |
| `co_seller.phone` | 전화 | phone | 23% | 010-6479-6446 |
| `co_seller.name` | 성명 | text | 23% | 김찬민 |
| `seal.co_seller` | 공동매도인 | seal | 23% | 김찬민 |
| `sign.co_seller` | 공동매도인 | signature | 23% | 최희원 |
| `seller_agent.address` | 대리인주소 | text | 17% | 서울특별시 영등포구 국제금융로 322, 122동 2001호 (신길동, 한… |
| `seller_agent.rrn` | 대리인주민등록번호 | rrn | 17% | 650531-1503031 |
| `seller_agent.name` | 대리인성명 | text | 17% | 우건유 |
| `seal.seller_agent` | 매도인대리인 | seal | 17% | 석진연 |
| `sign.seller_agent` | 매도인대리인 | signature | 17% | 우건유 |
| `brokers[].assistant` | 소속공인중개사 | text | 43% | 현수은 |
| `co_buyer.address` | 주소 | text | 3% | 서울특별시 강남구 도곡로 458-8, 102동 1102호 (논현동, 우성… |
| `co_buyer.rrn` | 주민등록번호 | rrn | 3% | 820218-1260586 |
| `co_buyer.phone` | 전화 | phone | 3% | 010-9382-0528 |
| `co_buyer.name` | 성명 | text | 3% | 이석인 |
| `seal.co_buyer` | 공동매수인 | seal | 3% |  |
| `sign.co_buyer` | 공동매수인 | signature | 3% | 이석인 |

### 주택임대차표준계약서 (`lease_contract`) — 키 52개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `landlord_name` | 임대인 | text | 100% | 박기우 |
| `tenant_name` | 임차인 | text | 100% | 박찬연 |
| `house.location` | 소재지 | text | 100% | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신… |
| `house.land_category` | 지목 | text | 100% | 대 |
| `house.land_area` | 토지면적 | text | 100% | 31,054.7㎡ |
| `house.structure_usage` | 구조·용도 | text | 100% | 철근콘크리트구조 / 공동주택(아파트) |
| `house.building_area` | 건물면적 | text | 100% | 101.84㎡ |
| `house.lease_part` | 임차할부분 | text | 100% | 전부 (101.84㎡) |
| `contract_type` | 계약의종류 | checkbox | 100% | 신규 계약 |
| `tax_arrears` | 미납국세·지방세 | text | 100% | 없음 |
| `prior_fixed_date` | 선순위확정일자현황 | text | 100% | 해당 없음 |
| `fixed_date.date` | 확정일자 | date | 100% | 2026.01.27 |
| `fixed_date.no` | 확정일자번호 | text | 100% | 2026-7849 |
| `fixed_date.office` | 확정일자부여기관 | text | 100% | 영통구 원천동행정복지센터 |
| `deposit` | 보증금 | amount | 100% | 금 삼억육천만원정 (₩360,000,000) |
| `down_payment` | 계약금 | amount | 100% | 금 삼천육백만원정 (₩36,000,000) |
| `balance` | 잔금 | amount | 100% | 금 삼억이천사백만원정 (₩324,000,000) |
| `balance_date` | 잔금지급일 | date | 100% | 2026년 03월 03일 |
| `management_fee` | 관리비 | text | 100% | 관리규약에 따라 관리주체가 부과하는 금액 |
| `handover_date` | 인도일 | date | 100% | 2026년 03월 03일 |
| `end_date` | 임대차종료일 | date | 100% | 2028년 03월 02일 |
| `specials[]` | 특약사항 | text | 100% | 1. 주택을 인도받은 임차인은 2026년 3월 3일까지 주민등록(전입신고… |
| `contract_date` | 계약일 | date | 100% | 2026년 01월 26일 |
| `landlord.address` | 주소 | text | 100% | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신… |
| `landlord.rrn` | 주민등록번호 | rrn | 100% | 570508-1456825 |
| `landlord.phone` | 전화 | phone | 100% | 010-6594-7883 |
| `landlord.name` | 성명 | text | 100% | 박기우 |
| `seal.landlord` | 임대인 | seal | 100% | 박기우 |
| `sign.landlord` | 임대인 | signature | 100% | 반원인 |
| `tenant.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `tenant.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `tenant.phone` | 전화 | phone | 100% | 010-5907-7253 |
| `tenant.name` | 성명 | text | 100% | 박찬연 |
| `seal.tenant` | 임차인 | seal | 100% | 현예지 |
| `sign.tenant` | 임차인 | signature | 100% | 박찬연 |
| `brokers[].office_address` | 사무소소재지 | text | 100% | 경기도 수원시 영통구 매탄로 68, 1층 111호 (원천동) |
| `brokers[].office_name` | 사무소명칭 | text | 100% | 한신휴공인중개사사무소 |
| `brokers[].representative` | 대표 | text | 100% | 위영지 |
| `brokers[].reg_no` | 등록번호 | text | 100% | 41835-2020-01056 |
| `brokers[].phone` | 전화 | phone | 100% | 031-885-2129 |
| `co_landlord.address` | 주소 | text | 17% | 대구광역시 수성구 수성로 401, 107동 2004호 (지산동, 센트레빌… |
| `co_landlord.rrn` | 주민등록번호 | rrn | 17% | 590110-1645169 |
| `co_landlord.phone` | 전화 | phone | 17% | 010-6479-6446 |
| `co_landlord.name` | 성명 | text | 17% | 김찬민 |
| `seal.co_landlord` | 공동임대인 | seal | 17% | 정건수 |
| `sign.co_landlord` | 공동임대인 | signature | 17% | 김찬민 |
| `brokers[].assistant` | 소속공인중개사 | text | 33% | 공건인 |
| `landlord_agent.address` | 대리인주소 | text | 10% | 부산광역시 해운대구 달맞이길 142, 114동 2403호 (중동, 센트레… |
| `landlord_agent.rrn` | 대리인주민등록번호 | rrn | 10% | 790510-2944862 |
| `landlord_agent.name` | 대리인성명 | text | 10% | 심정아 |
| `seal.landlord_agent` | 임대인대리인 | seal | 10% | 송영아 |
| `sign.landlord_agent` | 임대인대리인 | signature | 10% | 심정아 |

### 전입세대확인서 (`move_in_household_list`) — 키 25개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 8136-8334-8254-1287 |
| `issue_date` | 발급일자 | date | 100% | 2026.01.31 |
| `kind` | 열람·교부구분 | text | 100% | 교부 |
| `address` | 건물또는시설소재지 | text | 100% | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신… |
| `jibun_address` | 지번주소 | text | 100% | 경기도 수원시 영통구 원천동 87 115동 2104호 |
| `households[].no` | 순번 | number | 100% | 1 |
| `households[].head_name` | 세대주성명 | text | 100% | 박*연 |
| `households[].move_in_date` | 전입일자 | date | 100% | 2025-11-11 |
| `households[].reg_type` | 등록구분 | text | 100% | 거주자 |
| `households[].first_name` | 최초전입자성명 | text | 100% | 박*연 |
| `households[].first_date` | 최초전입일자 | date | 100% | 2025-11-11 |
| `households[].first_reg_type` | 최초전입자등록구분 | text | 100% | 거주자 |
| `households[].cohabitants` | 동거인수 | number | 100% | 0 |
| `applicant.name` | 성명 | text | 100% | 박찬연 |
| `applicant.rrn` | 주민등록번호 | rrn | 100% | 900210-1****** |
| `applicant.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `applicant.purpose` | 열람·교부목적 | text | 100% | 금융기관 대출(주택담보대출) |
| `view_date` | 발급일 | date | 100% | 2026년 01월 31일 |
| `issuer` | 발급기관 | text | 100% | 영통구 원천동장 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 동장의인 |
| `cohabitants[].no` | 순번 | number | 33% | 1 |
| `cohabitants[].name` | 동거인성명 | text | 33% | 심*민 |
| `cohabitants[].move_in_date` | 전입일자 | date | 33% | 2010-02-25 |
| `cohabitants[].reg_type` | 등록구분 | text | 33% | 거주자 |
| `households[].unit` | 동·호 | text | 3% | 101호 |

## 개인사업자


### 사업자등록증 (`business_registration_certificate`) — 키 18개

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

### 사업자등록증(법인사업자) (`business_registration_certificate_corp`) — 키 18개

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

### 사업자등록증명 (`business_registration_proof`) — 키 23개

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

### 표준재무제표증명 (`standard_financial_statement_proof`) — 키 70개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 100% | 6888-572-1183-223 |
| `taxpayer_type` | 개인/법인 | checkbox | 100% | 개인 |
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

## 법인


### 법인 등기사항전부증명서(현재 유효사항) (`corporate_registry`) — 키 65개

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

### 정관 (`articles_of_incorporation`) — 키 18개

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

### 주주명부 (`shareholder_registry`) — 키 24개

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

### 재무제표(재무상태표·손익계산서) (`financial_statements`) — 키 33개

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

### 법인인감증명서 (`corporate_seal_certificate`) — 키 16개

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

### 이사회의사록 (`board_minutes`) — 키 40개

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

### 임시주주총회의사록 (`shareholders_meeting_minutes`) — 키 35개

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

### 위임장 (`power_of_attorney`) — 키 23개

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
| `grantor.type` | 위임인구분 | checkbox | 100% | 법인 |
| `grantor.name` | 상호 | text | 100% | (주)유니온무역 |
| `grantor.ceo` | 대표자 | text | 70% | 박찬연 |
| `grantor.biz_no` | 사업자등록번호 | biz_no | 70% | 264-82-36559 |
| `grantor.corp_reg_no` | 법인등록번호 | corp_reg_no | 70% | 200112-7448551 |
| `grantor.address` | 본점소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `grantor.phone` | 연락처 | phone | 100% | 02-9508-6789 |
| `seal.corp` | 법인인감 | seal | 70% | 주식회사 유니온무역 대표이사인 |
| `attachment` | 첨부서류 | text | 100% | 법인인감증명서 1부 |
| `recipient` | 제출처 | text | 100% | 기업은행 범어지점 귀중 |
| `sub_delegation` | 복대리인선임 | checkbox | 23% | 불허 |
| `grantor.birth` | 생년월일 | date | 30% | 1966년 08월 12일 |
| `seal.grantor` | 위임인 | seal | 30% | 현예지 |
| `tasks_extra` | 위임내용 | text | 20% | 4. 통장 및 OTP 재발급 신청·수령 |
| `use_limit` | 사용제한 | text | 10% | 본 위임장은 위 업무 1회에 한하여 유효함 |

## 외환·무역


### 상업송장(Commercial Invoice) (`commercial_invoice`) — 키 37개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `shipper.name` | Shipper/Exporter | text | 100% | Mekong Garment JSC |
| `shipper.address` | ShipperAddress | text | 100% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `invoice_no` | InvoiceNo | text | 100% | MGJ-2512-054 |
| `invoice_date` | InvoiceDate | date | 100% | 30 DEC 2025 |
| `consignee.name` | Consignee | text | 100% | UNION TRADING CO., LTD. |
| `consignee.address` | ConsigneeAddress | text | 100% | 6F, GREEN KNOWLEDGE INDUSTRY CENTER, 361… |
| `notify` | NotifyParty | text | 100% | SAME AS ABOVE |
| `terms.delivery` | TermsofDelivery | text | 100% | FOB HO CHI MINH CITY (CAT LAI), VIETNAM … |
| `terms.payment` | TermsofPayment | text | 100% | T/T 60 DAYS AFTER B/L DATE |
| `origin` | CountryofOrigin | text | 100% | VIETNAM |
| `port_of_loading` | PortofLoading | text | 100% | HO CHI MINH CITY (CAT LAI), VIETNAM |
| `final_destination` | FinalDestination | text | 100% | BUSAN, KOREA |
| `carrier` | Carrier | text | 100% | CORAL VOYAGER V.126S |
| `sailing_date` | Sailingonorabout | date | 100% | 01 JAN 2026 |
| `marks` | MarksandNumbers | text | 100% | UNION BUSAN, KOREA C/NO. 1-488 MADE IN V… |
| `items[].description` | DescriptionofGoods | text | 100% | Men's Cotton Crew Neck T-Shirt |
| `items[].model` | Model | text | 100% | MT-277A |
| `items[].quantity` | Quantity/Unit | text | 100% | 18,100 PCS |
| `items[].unit_price` | Unit-price | amount | 100% | USD 3.70 |
| `items[].amount` | Amount | amount | 100% | USD 66,970.00 |
| `total_quantity` | TotalPackages | text | 100% | 488 CTNS |
| `total_amount` | TotalAmount | amount | 100% | USD 193,394.30 |
| `signed_by` | Signedby | text | 100% | Mekong Garment JSC |
| `signer` | Signer | text | 100% | Nguyen Van An |
| `contract_no` | ContractNo | text | 37% | HAN-SC-25529 |
| `lc.no` | L/CNo | text | 50% | M45972508NU76564 |
| `lc.date` | L/CDate | date | 50% | 09 JUL 2025 |
| `lc.bank` | L/CIssuingBank | text | 50% | INDUSTRIAL BANK OF KOREA |
| `manufacturer.name` | Manufacturer | text | 7% | Mekong Garment JSC |
| `manufacturer.address` | ManufacturerAddress | text | 7% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `beneficiary_bank.name` | BeneficiaryBank | text | 7% | BANK OF CHINA (HONG KONG) LIMITED |
| `beneficiary_bank.swift` | BeneficiaryBankSWIFT | text | 7% | BKCHHKHH |
| `beneficiary_bank.account` | BeneficiaryAccountNo | account_no | 7% | 799-657998-874 |
| `price_breakdown.fob` | FOBValue | amount | 3% | USD 142,545.17 |
| `price_breakdown.freight` | OceanFreight | amount | 3% | USD 7,240.21 |
| `price_breakdown.insurance` | InsurancePremium | amount | 3% | USD 115.42 |
| `partial_shipment` | PartialShipment | text | 7% | 1ST LOT OF 2 LOTS |

### 무역 매매계약서(Sales Contract) (`trade_contract`) — 키 42개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `seller.name` | Seller | text | 100% | Mekong Garment JSC |
| `seller.address` | SellerAddress | text | 100% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `buyer.name` | Buyer | text | 100% | UNION TRADING CO., LTD. |
| `buyer.address` | BuyerAddress | text | 100% | 6F, GREEN KNOWLEDGE INDUSTRY CENTER, 361… |
| `contract_no` | ContractNo | text | 100% | MGJ-SC-25461 |
| `contract_date` | Date | date | 100% | November 10, 2025 |
| `items[].description` | Commodity&Description | text | 100% | Men's Cotton Crew Neck T-Shirt |
| `items[].model` | Model | text | 100% | MT-277A |
| `items[].quantity` | Quantity | text | 100% | 18,100 PCS |
| `items[].unit_price` | UnitPrice | amount | 100% | USD 3.70 |
| `items[].amount` | Amount | amount | 100% | USD 66,970.00 |
| `total_amount` | TotalAmount | amount | 100% | USD 193,394.30 |
| `total_words` | TotalAmountinWords | text | 100% | SAY US DOLLARS ONE HUNDRED NINETY THREE … |
| `clauses.price_terms` | PriceTerms | text | 100% | FOB HO CHI MINH CITY (CAT LAI), VIETNAM … |
| `clauses.origin` | Origin | text | 100% | Vietnam |
| `clauses.packing` | Packing | text | 100% | Export standard packing in cartons, suit… |
| `clauses.shipping_mark` | ShippingMark | text | 100% | UNION BUSAN, KOREA C/NO. 1-UP MADE IN VI… |
| `clauses.shipment` | Shipment | text | 100% | Not later than January 09, 2026. Partial… |
| `clauses.port_of_shipment` | PortofShipment | text | 100% | HO CHI MINH CITY (CAT LAI), VIETNAM |
| `clauses.destination` | Destination | text | 100% | BUSAN, KOREA |
| `clauses.payment` | Payment | text | 100% | By telegraphic transfer within 60 days a… |
| `clauses.inspection` | Inspection | text | 100% | Inspection by an independent surveyor (S… |
| `clauses.arbitration` | Arbitration | text | 100% | Any dispute shall be settled by arbitrat… |
| `seal.buyer` | BuyerSignature | seal | 100% |  |
| `sign.buyer` | BuyerSignature | signature | 100% | Akira Tanaka |
| `buyer.signer` | BuyerSignatory | text | 100% | Park Chanyeon |
| `buyer.title` | BuyerTitle | text | 100% | Representative Director |
| `buyer.sign_date` | BuyerSigningDate | date | 100% | 13 NOV 2025 |
| `seal.seller` | SellerSignature | seal | 100% |  |
| `sign.seller` | SellerSignature | signature | 100% | Nguyen Van An |
| `seller.signer` | SellerSignatory | text | 100% | Nguyen Van An |
| `seller.title` | SellerTitle | text | 100% | Export Manager |
| `seller.sign_date` | SellerSigningDate | date | 100% | 10 NOV 2025 |
| `clauses.insurance` | Insurance | text | 27% | To be covered by the Seller for 110% of … |
| `gtc_terms.late_penalty` | LateShipmentPenalty | percent | 30% | 1% |
| `gtc_terms.inspection_days` | InspectionPeriod(days) | number | 30% | 21 |
| `gtc_terms.warranty` | WarrantyPeriod | text | 37% | eighteen (18) months |
| `gtc_terms.late_interest` | LatePaymentInterest | percent | 37% | 6% |
| `gtc_terms.governing_law` | GoverningLaw | text | 30% | the State of New York, U.S.A. |
| `gtc_terms.qty_tolerance` | QuantityTolerance | percent | 33% | 3% |
| `gtc_terms.claim_days` | ClaimPeriod(days) | number | 27% | 90 |
| `clauses.manufacturer` | Manufacturer | text | 7% | Mekong Garment JSC, 45 Le Loi St, Distri… |

### 선하증권(B/L) (`bill_of_lading`) — 키 46개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `shipper.name` | Shipper | text | 100% | Mekong Garment JSC |
| `shipper.address` | ShipperAddress | text | 100% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `booking_no` | BookingNo | text | 100% | BKG3185811 |
| `bl_no` | B/LNo | text | 100% | OCLN15701972 |
| `carrier` | Carrier | text | 100% | OCEANLINK CONTAINER LINES |
| `forwarder` | ForwardingAgent | text | 100% | Daon Logistics Co., Ltd. |
| `consignee.name` | Consignee | text | 100% | UNION TRADING CO., LTD. |
| `consignee.address` | ConsigneeAddress | text | 37% | 6F, GREEN KNOWLEDGE INDUSTRY CENTER, 361… |
| `notify.name` | NotifyParty | text | 100% | SAME AS CONSIGNEE |
| `pre_carriage` | Pre-carriageby | text | 100% | TRUCK |
| `place_of_receipt` | PlaceofReceipt | text | 100% | HO CHI MINH CITY (CAT LAI) CY |
| `origin` | PointandCountryofOrigin | text | 100% | VIETNAM |
| `vessel_voyage` | OceanVessel/VoyNo | text | 100% | CORAL VOYAGER 126S |
| `port_of_loading` | PortofLoading | text | 100% | HO CHI MINH CITY (CAT LAI), VIETNAM |
| `port_of_discharge` | PortofDischarge | text | 100% | BUSAN, KOREA |
| `place_of_delivery` | PlaceofDelivery | text | 100% | BUSAN CY |
| `containers[].no` | ContainerNo | text | 100% | OCLU1212140 |
| `containers[].type` | ContainerType | text | 100% | 40'HC |
| `containers[].seal` | SealNo | text | 100% | H388222 |
| `marks` | MarksandNumbers | text | 100% | UNION BUSAN, KOREA C/NO. 1-488 MADE IN V… |
| `container_count` | No.ofContainers | text | 100% | 1 X 40'HC |
| `packages` | No.ofPackages | text | 100% | 488 CTNS |
| `description` | DescriptionofGoods | text | 100% | Men's Cotton Crew Neck T-Shirt  18,100 P… |
| `freight` | Freight | text | 100% | FREIGHT COLLECT |
| `gross_weight` | GrossWeight | text | 100% | 9,381.96 KGS |
| `measurement` | Measurement | text | 100% | 49.050 CBM |
| `total_words` | TotalNumberinWords | text | 100% | SAY: ONE (1) CONTAINER ONLY |
| `freight_payable_at` | FreightPayableat | text | 100% | BUSAN |
| `issue_place` | PlaceofIssue | text | 100% | HO CHI MINH CITY (CAT LAI) |
| `issue_date` | DateofIssue | date | 100% | 01 JAN 2026 |
| `originals` | NumberofOriginalB/L | text | 100% | THREE (3) |
| `on_board_date` | OnBoardDate | date | 100% | 01 JAN 2026 |
| `document_type` | DocumentType | text | 3% | SEA WAYBILL |
| `surrender` | Surrender | text | 7% | SURRENDERED |
| `surrender_date` | SurrenderDate | date | 7% | 18 AUG 2025 |
| `containers[].packages` | ContainerPackages | text | 30% | 1,571 PKGS |
| `containers[].gross_weight` | ContainerGrossWeight | number | 30% | 41,420.40 |
| `containers[].measurement` | ContainerMeasurement | number | 30% | 44.735 |
| `notify.address` | NotifyPartyAddress | text | 63% | 13F, DN SQUARE, 499 HWAUN-RO, SEO-GU, GW… |
| `lc_no` | L/CNo | text | 50% | M45972508NU76564 |
| `charges[].name` | Charge | text | 27% | OCEAN FREIGHT |
| `charges[].quantity` | RevenueTons | number | 27% | 2.00 |
| `charges[].rate` | Rate | number | 27% | 3,300.00 |
| `charges[].per` | Per | text | 27% | CNTR |
| `charges[].collect` | Collect | amount | 10% | USD 6,600.00 |
| `charges[].prepaid` | Prepaid | amount | 27% | USD 280.00 |

### 포장명세서(Packing List) (`packing_list`) — 키 36개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `shipper.name` | Shipper/Exporter | text | 100% | Mekong Garment JSC |
| `shipper.address` | ShipperAddress | text | 100% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `invoice_no` | InvoiceNo | text | 100% | MGJ-2512-054 |
| `invoice_date` | InvoiceDate | date | 100% | 30 DEC 2025 |
| `consignee.name` | Consignee | text | 100% | UNION TRADING CO., LTD. |
| `consignee.address` | ConsigneeAddress | text | 100% | 6F, GREEN KNOWLEDGE INDUSTRY CENTER, 361… |
| `contract_no` | ContractNo | text | 53% | MGJ-SC-25461 |
| `notify` | NotifyParty | text | 100% | SAME AS CONSIGNEE |
| `port_of_loading` | PortofLoading | text | 100% | HO CHI MINH CITY (CAT LAI), VIETNAM |
| `final_destination` | FinalDestination | text | 100% | BUSAN, KOREA |
| `carrier` | Carrier | text | 100% | CORAL VOYAGER V.126S |
| `sailing_date` | Sailingonorabout | date | 100% | January 01, 2026 |
| `marks` | MarksandNumbers | text | 100% | UNION BUSAN, KOREA C/NO. 1-488 MADE IN V… |
| `items[].ctn_no` | C/TNo | text | 100% | 1-181 |
| `items[].description` | DescriptionofGoods | text | 100% | Men's Cotton Crew Neck T-Shirt |
| `items[].packages` | Packages | text | 100% | 181 CTNS |
| `items[].quantity` | Quantity | text | 100% | 18,100 PCS |
| `items[].net_weight` | NetWeight | number | 100% | 3,258.00 |
| `items[].gross_weight` | GrossWeight | number | 100% | 3,518.64 |
| `items[].measurement` | Measurement | number | 100% | 16.290 |
| `total.packages` | TotalPackages | text | 100% | 488 CTNS |
| `total.net_weight` | TotalNetWeight | text | 100% | 8,687.00 KGS |
| `total.gross_weight` | TotalGrossWeight | text | 100% | 9,381.96 KGS |
| `total.measurement` | TotalMeasurement | text | 100% | 49.050 CBM |
| `signed_by` | Signedby | text | 100% | Mekong Garment JSC |
| `signer` | Signer | text | 100% | Nguyen Van An |
| `containers[].no` | ContainerNo | text | 20% | TPMU9280511 |
| `containers[].seal` | SealNo | text | 20% | SL436094 |
| `containers[].packages` | ContainerPackages | text | 20% | 409 PKGS |
| `containers[].net_weight` | ContainerNetWeight | number | 20% | 15,244.00 |
| `containers[].gross_weight` | ContainerGrossWeight | number | 20% | 15,653.52 |
| `containers[].measurement` | ContainerMeasurement | number | 20% | 51.260 |
| `lc_no` | L/CNo | text | 50% | M45972508NU76564 |
| `manufacturer.name` | Manufacturer | text | 7% | Mekong Garment JSC |
| `manufacturer.address` | ManufacturerAddress | text | 7% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `partial_shipment` | PartialShipment | text | 7% | 1ST LOT OF 2 LOTS |

### 수입신고필증 (`import_declaration`) — 키 67개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `decl_no` | 신고번호 | text | 100% | 20097-26-7868647U |
| `decl_date` | 신고일 | date | 100% | 2026/01/10 |
| `customs` | 세관.과 | text | 100% | 030-17 |
| `arrival_date` | 입항일 | date | 100% | 2026/01/09 |
| `bl_no` | B/L번호 | text | 100% | OCLN15701972 |
| `cargo_no` | 화물관리번호 | text | 100% | 26OCLN610441I-2996-002 |
| `warehouse_date` | 반입일 | date | 100% | 2026/01/10 |
| `collection_type` | 징수형태 | number | 100% | 11 |
| `declarant` | 신고인 | text | 100% | 대한관세법인 정채유 |
| `importer.name` | 수입자 | text | 100% | (주)유니온무역 |
| `importer.code` | 수입자통관고유부호 | text | 100% | 유니온무8255080 |
| `taxpayer.code` | 납세의무자통관고유부호 | text | 100% | 유니온무8255080 |
| `taxpayer.address` | 납세의무자주소 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `taxpayer.name` | 납세의무자상호 | text | 100% | (주)유니온무역 |
| `taxpayer.ceo` | 납세의무자성명 | text | 100% | 박찬연 |
| `taxpayer.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `forwarder` | 운송주선인 | text | 100% | DAON LOGISTICS CO., LTD. |
| `supplier` | 해외거래처 | text | 100% | MEKONG GARMENT JSC (VN) |
| `clearance_plan` | 통관계획 | text | 100% | D 보세구역장치후 |
| `origin_cert` | 원산지증명서유무 | text | 100% | Y |
| `total_weight` | 총중량 | text | 100% | 9,382 KG |
| `total_packages` | 총포장갯수 | text | 100% | 488 CT |
| `arrival_port` | 국내도착항 | text | 100% | KRPUS 부산항 |
| `transport` | 운송형태 | text | 100% | 10 FCL |
| `export_country` | 적출국 | text | 100% | VN VIETNAM |
| `vessel` | 선기명 | text | 100% | CORAL VOYAGER |
| `master_bl` | MASTERB/L번호 | text | 100% | OCLN15701972 |
| `carrier_code` | 운수기관부호 | text | 100% | OCLN |
| `inspection_place` | 검사(반입)장소 | text | 100% | 03055276-55499004 부산신항국제터미널 |
| `items[].line_no` | 란번호 | number | 100% | 001 |
| `line_total` | 총란수 | amount | 100% | 003 |
| `items[].std_name` | 품명 | text | 100% | T-SHIRTS, KNITTED, OF COTTON |
| `items[].trade_name` | 거래품명 | text | 100% | MEN'S COTTON CREW NECK T-SHIRT |
| `items[].specs[].no` | 규격번호 | number | 100% | 01 |
| `items[].specs[].model` | 모델·규격 | text | 100% | MT-277A |
| `items[].specs[].quantity` | 수량 | text | 100% | 18,100 PCS |
| `items[].specs[].unit_price` | 단가 | amount | 100% | 3.70 |
| `items[].specs[].amount` | 금액 | amount | 100% | 66,970.00 |
| `items[].hs_code` | 세번부호 | text | 100% | 6109.10-0000 |
| `items[].net_weight` | 순중량 | text | 100% | 3,258.0 KG |
| `items[].taxable_usd` | 과세가격(USD) | amount | 100% | $67,865 |
| `items[].taxable_krw` | 과세가격(원화) | amount | 100% | ₩98,445,056 |
| `items[].origin` | 원산지 | text | 100% | VN-B-Y |
| `items[].duty_type` | 세종 | text | 100% | 관 |
| `items[].duty_rate` | 관세율 | text | 100% | 0.00(FVN1) |
| `items[].duty_amount` | 관세액 | amount | 100% | 0 |
| `items[].vat_rate` | 부가세율 | text | 100% | 10.00(A) |
| `items[].vat_amount` | 부가세액 | amount | 100% | 9,844,500 |
| `payment` | 결제금액 | text | 100% | FOB-USD-193,394.30-TT |
| `exchange_rate` | 환율 | number | 100% | 1,450.60 |
| `total_taxable` | 총과세가격 | amount | 100% | ₩284,287,194 |
| `freight` | 운임 | amount | 100% | ₩3,553,041 |
| `vat_base` | 부가가치세과표 | amount | 100% | ₩284,287,194 |
| `insurance` | 보험료 | amount | 100% | ₩196,382 |
| `tax.duty` | 관세 | amount | 100% | 0 |
| `customs_office` | 세관 | text | 100% | 부산세관 |
| `officer` | 담당자 | text | 100% | 이도경 |
| `receipt_datetime` | 접수일시 | datetime | 100% | 2026/01/10 12:33 |
| `accept_date` | 수리일자 | date | 100% | 2026/01/11 |
| `seal.issuer` | 발급기관직인 | seal | 100% | 세관장인 |
| `tax.vat` | 부가세 | amount | 100% | 28,428,700 |
| `tax.total` | 총세액합계 | amount | 100% | 28,428,700 |
| `amendment.date` | 정정승인일자 | date | 10% | 2026/04/03 |
| `amendment.reason` | 정정사유 | text | 10% | (42)원산지표시 정정 |
| `items[].reduction.rate` | 감면율 | number | 3% | 50.00 |
| `items[].reduction.code` | 감면분납부호 | text | 3% | Y8010 |
| `items[].reduction.amount` | 감면액 | amount | 3% | 12,607,110 |

### 입학허가서(Letter of Admission) (`admission_letter`) — 키 29개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `university.name` | University | text | 100% | Westlake State University |
| `university.office` | Office | text | 100% | Office of Graduate Admissions |
| `university.address` | UniversityAddress | text | 100% | 1800 Lakeview Dr, Seattle, WA 98105, USA |
| `university.email` | Email | text | 100% | admissions@westlakestate.edu |
| `letter_date` | Date | date | 100% | December 05, 2025 |
| `student.name` | StudentName | text | 100% | Chanyeon Park |
| `student.address` | StudentAddress | text | 100% | Apt. 110-501, 524 Bangbae-ro, Seocho-gu,… |
| `admission_type` | AdmissionType | text | 13% | CONDITIONAL ADMISSION |
| `term` | TermofEntry | text | 100% | Fall 2026 |
| `student.birth` | DateofBirth | date | 100% | 10 FEB 1990 |
| `student.nationality` | Citizenship | text | 100% | Republic of Korea |
| `student.id` | StudentID | text | 100% | M94946101 |
| `program` | Program | text | 100% | Education |
| `degree` | Degree | text | 100% | Master of Education (M.Ed.) |
| `start_date` | ClassesBegin | date | 100% | August 25, 2026 |
| `duration` | Duration | text | 100% | 2 years (full-time) |
| `condition_deadline` | ConditionDeadline | date | 13% | July 20, 2026 |
| `conditions[]` | Condition | text | 13% | Submission of an official TOEFL iBT scor… |
| `deposit_deadline` | DepositDeadline | date | 100% | December 31, 2025 |
| `signer` | Signedby | text | 100% | Emily R. Watson |
| `signer_title` | Title | text | 100% | Director of Admissions |
| `cost.tuition` | EstimatedTuition | number | 43% | $56,000.00 |
| `cost.living` | EstimatedLivingExpenses | number | 43% | $22,000.00 |
| `cost.insurance` | EstimatedHealthInsurance | number | 43% | $3,120.00 |
| `cost.books` | EstimatedBooksandSupplies | number | 43% | $1,620.00 |
| `cost.total` | TotalEstimatedCost | amount | 43% | $82,740.00 |
| `scholarship.name` | Scholarship | text | 23% | International Student Award |
| `scholarship.amount` | ScholarshipAmount | text | 23% | $8,860.00 per semester |
| `deferred_from` | DeferredFrom | text | 7% | Spring 2025 |

### 학비 청구서(Tuition Invoice) (`tuition_invoice`) — 키 29개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `university.name` | University | text | 100% | Westlake State University |
| `university.office` | Office | text | 100% | Student Financial Services |
| `university.address` | UniversityAddress | text | 100% | 1800 Lakeview Dr, Seattle, WA 98105, USA |
| `student.name` | StudentName | text | 100% | Chanyeon Park |
| `student.id` | StudentID | text | 100% | M94946101 |
| `student.program` | Program | text | 100% | Master of Education (M.Ed.) in Education |
| `invoice_no` | InvoiceNo | text | 100% | INV-2026368927 |
| `invoice_date` | InvoiceDate | date | 100% | December 31, 2025 |
| `term` | Term | text | 100% | Fall 2026 |
| `items[].date` | Date | date | 100% | 12/30/2025 |
| `items[].description` | Description | text | 100% | Tuition - Full-time Graduate |
| `items[].charge` | Charges | amount | 100% | $17,430.00 |
| `items[].credit` | Payments/Credits | amount | 50% | $1,000.00 |
| `summary.previous_balance` | PreviousBalance | amount | 100% | $0.00 |
| `summary.charges` | NewCharges | amount | 100% | $21,032.00 |
| `summary.credits` | Payments/Credits | amount | 100% | $10,400.00 |
| `total` | TotalAmountDue | amount | 100% | USD 10,632.00 |
| `due_date` | DueDate | date | 100% | August 03, 2026 |
| `bank.beneficiary` | Beneficiary | text | 100% | Westlake State University |
| `bank.bank_name` | BankName | text | 100% | Bank of America, N.A. |
| `bank.swift` | SWIFT | text | 100% | BOFAUS3N |
| `bank.account` | AccountNumber | account_no | 100% | 212604946606 |
| `bank.routing_label` | RoutingLabel | text | 100% | ABA Routing No. |
| `bank.routing` | RoutingNumber | number | 100% | 036941220 |
| `bank.reference` | PaymentReference | text | 100% | M94946101 Chanyeon Park |
| `amount_due_now` | AmountDueNow | amount | 3% | £2,247.25 |
| `installments[].no` | InstallmentNo | number | 3% | 1 |
| `installments[].due_date` | InstallmentDueDate | date | 3% | January 01, 2026 |
| `installments[].amount` | InstallmentAmount | amount | 3% | £2,247.25 |

## 은행 서식


### 대출거래신청서 (`loan_application`) — 키 63개

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
| `housing` | 주택소유구분 | checkbox | 100% | 월세 |
| `dwelling` | 주거형태 | checkbox | 100% | 아파트 |
| `workplace.job_type` | 직업구분 | checkbox | 100% | 급여소득자 |
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
| `loan.repayment` | 상환방법 | checkbox | 100% | 원리금균등분할 |
| `loan.rate_type` | 금리방식 | checkbox | 100% | 변동 |
| `loan.interest_day` | 이자납입일 | text | 100% | 매월 15일 |
| `loan.purpose_category` | 자금용도구분 | checkbox | 100% | 주택구입 |
| `loan.purpose` | 세부용도 | text | 100% | 주택구입자금 |
| `collateral` | 담보구분 | checkbox | 100% | 부동산 |
| `collateral_detail` | 담보내용 | text | 100% | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (아파트, 전용… |
| `loan.debit_bank` | 이체은행 | text | 100% | 기업은행 |
| `loan.debit_account` | 이체계좌번호 | account_no | 100% | 171-760452-29-611 |
| `loan.debit_holder` | 예금주 | text | 100% | 박찬연 |
| `agent.name` | 대리인성명 | text | 13% | 우나민 |
| `agent.rrn` | 대리인실명번호 | rrn | 13% | 671023-2****** |
| `agent.relation` | 본인과의관계 | text | 13% | 모 |
| `agent.phone` | 대리인연락처 | phone | 13% | 010-7560-2133 |
| `agent.poa` | 위임장 | checkbox | 13% | 첨부 |
| `manual_received` | 설명서수령확인 | checkbox | 100% | 예 |
| `consent` | 개인(신용)정보동의 | checkbox | 100% | 동의함 |
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

### 기업여신 신청서 (`loan_application_corp`) — 키 48개

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
| `company.size` | 기업규모 | checkbox | 100% | 중소기업 |
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
| `loan.subject` | 여신과목 | checkbox | 100% | 일반자금대출 |
| `loan.product` | 상품명 | text | 100% | 중소기업 운전자금대출 |
| `loan.rate_type` | 금리종류 | checkbox | 100% | 고정금리 |
| `loan.amount_korean` | 신청금액(한글) | amount_korean | 100% | 일금 삼십억원정 |
| `loan.amount` | 신청금액 | amount | 100% | 3,000,000,000원 |
| `loan.term` | 여신기간 | text | 100% | 1년 |
| `loan.hope_date` | 대출희망일 | date | 100% | 2026-02-03 |
| `loan.repayment` | 상환방법 | text | 100% | 만기일시상환 |
| `loan.fund_type` | 자금구분 | checkbox | 100% | 운전자금 |
| `loan.purpose` | 자금용도 | text | 100% | 매출채권 회수 지연에 따른 운전자금 |
| `loan.deposit_account` | 대출금입금계좌 | account_no | 100% | 기업은행 198-866024-83-977 |
| `loan.collateral` | 담보구분 | checkbox | 100% | 보증서 |
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

### 대출거래약정서(가계용) (`credit_agreement`) — 키 43개

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
| `loan.method` | 거래구분 | checkbox | 100% | 개별거래 |
| `loan.account_no` | 대출계좌번호 | account_no | 100% | 740-757492-44-140 |
| `loan.amount_korean` | 대출(한도)금액(한글) | amount_korean | 100% | 금 이억구천이백만원整 |
| `loan.amount` | 대출(한도)금액 | amount | 100% | 292,000,000원 |
| `loan.start_date` | 대출개시일 | date | 100% | 2026.02.16 |
| `loan.maturity` | 대출기간만료일 | date | 100% | 2066.02.16 |
| `loan.rate_type` | 금리종류 | checkbox | 100% | 변동금리 |
| `loan.base_rate_name` | 기준금리종류 | text | 100% | CD 91일물 |
| `loan.base_rate` | 기준금리 | percent | 100% | 2.87% |
| `loan.spread` | 가산금리 | percent | 100% | 1.58% |
| `loan.pref_rate` | 우대금리 | percent | 100% | 0.50% |
| `loan.applied_rate` | 대출이자율 | percent | 100% | 연 3.95% |
| `loan.rate_reset` | 금리변동주기 | text | 100% | 3개월 |
| `loan.interest_pay` | 이자지급시기 | text | 100% | 매월 15일 (후취) |
| `loan.interest_calc` | 이자계산방법 | text | 100% | 1년을 365일(윤년 366일)로 보고 1일 단위로 계산 |
| `loan.repayment` | 상환방법 | checkbox | 100% | 원리금균등분할상환 |
| `loan.installment` | 분할상환횟수 | text | 100% | 480회 (매월) |
| `loan.debit_account` | 자동이체계좌 | account_no | 100% | 기업은행 171-760452-29-611 |
| `loan.prepay_fee` | 중도상환해약금 | text | 100% | 중도상환금액 × 0.74% × 잔존일수 ÷ 대출기간일수 (3년 경과 시 … |
| `loan.late_rate` | 지연배상금률 | text | 100% | 대출이자율 + 연체가산이자율 연 3% (현재 연 6.95%, 최고 연 1… |
| `stamp_tax` | 인지세 | text | 100% | 150,000원 (고객 75,000원 / 은행 75,000원) |
| `explained` | 설명이해확인 | checkbox | 100% | 예 |
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

### 여신거래약정서(기업용) (`credit_agreement_corp`) — 키 43개

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
| `loan.method` | 거래방법 | checkbox | 100% | 개별거래 |
| `loan.account_no` | 여신계좌번호 | account_no | 100% | 203-617585-91-545 |
| `loan.amount_korean` | 여신(한도)금액(한글) | amount_korean | 100% | 금 삼십억원정 |
| `loan.amount` | 여신(한도)금액 | amount | 100% | 3,000,000,000원 |
| `loan.start_date` | 여신개시일 | date | 100% | 2026년 2월 3일 |
| `loan.maturity` | 여신기간만료일 | date | 100% | 2027년 2월 3일 |
| `loan.purpose` | 자금용도 | text | 100% | 매출채권 회수 지연에 따른 운전자금 |
| `loan.rate_type` | 금리종류 | checkbox | 100% | 고정금리 |
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
| `explained` | 설명이해확인 | checkbox | 100% | 예 |
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

### 근저당권설정계약서 (`collateral_agreement`) — 키 43개

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

### 보증약정서 (`guarantee_agreement`) — 키 33개

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
| `explained` | 설명이해확인 | checkbox | 100% | 예 |
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

### 자동이체 신청서 (`auto_transfer_application`) — 키 34개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank` | 은행명 | text | 100% | 기업은행 |
| `biller.name` | 수납기관 | text | 100% | 중소기업은행 |
| `branch` | 취급점 | text | 100% | 범어지점 |
| `kind` | 신청구분 | checkbox | 100% | 신규 |
| `biller.fee_type` | 요금종류 | text | 100% | 대출원리금(주택담보대출) |
| `target` | 이체대상 | checkbox | 100% | 대출원리금 |
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
| `relation` | 신청인과예금주와의관계 | checkbox | 100% | 본인 |
| `transfer_day` | 출금일 | text | 100% | 매월 15일 |
| `start_month` | 이체개시 | text | 100% | 2026년 3월분부터 |
| `amount` | 출금금액 | text | 100% | 청구금액 전액 (약 1,211,320원) |
| `privacy_consent` | 개인정보수집이용동의 | checkbox | 100% | 동의함 |
| `third_party_consent` | 제3자제공동의 | checkbox | 100% | 동의함 |
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

### 고객확인서(개인) (`customer_due_diligence`) — 키 51개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank.name` | 은행명 | text | 100% | 기업은행 |
| `customer.name` | 성명(한글) | text | 100% | 존 밀러 |
| `customer.name_en` | 성명(영문) | text | 100% | KANG SOONJUN |
| `customer.rrn` | 실명번호 | rrn | 100% | 950627-5955869 |
| `customer.resident_type` | 구분 | checkbox | 100% | 외국인 |
| `customer.gender` | 성별 | checkbox | 100% | 남 |
| `customer.nationality` | 국적 | text | 100% | 미국 |
| `customer.address` | 주소(거소) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `customer.mobile` | 휴대전화 | phone | 100% | 010-3055-5155 |
| `customer.email` | E-mail | text | 100% | john89@yahoo.com |
| `job.type` | 직업 | checkbox | 100% | 급여소득자 |
| `job.company` | 직장명 | text | 83% | 주식회사 태평양무역 |
| `job.department` | 부서/직위 | text | 70% | 구매팀 / 대리 |
| `job.industry` | 업종 | text | 83% | 도매 및 소매업 |
| `job.work_phone` | 직장전화 | phone | 83% | 043-783-2775 |
| `transaction.purpose` | 거래목적 | checkbox | 100% | 공과금 납부결제 |
| `transaction.fund_source` | 자금의원천 | checkbox | 100% | 근로 및 연금소득 |
| `transaction.expected_amount` | 예상거래금액 | checkbox | 100% | 1천만원 미만 |
| `transaction.frequency` | 예상거래빈도 | checkbox | 100% | 월 5회 미만 |
| `beneficial_owner` | 실제소유자여부 | checkbox | 100% | 예 |
| `pep` | 외국의정치적주요인물여부 | checkbox | 100% | 아니오 |
| `date` | 작성일 | date | 100% | 2026년 01월 31일 |
| `signature` | 고객성명 | text | 100% | MILLER JOHN |
| `seal.customer` | 고객 | seal | 100% | MILL |
| `sign.customer` | 고객 | signature | 100% | 강순준 |
| `bank_use.risk_grade` | 고객위험등급 | checkbox | 100% | 저위험 |
| `bank_use.id_type` | 실명확인증표 | checkbox | 100% | 외국인등록증 |
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
| `edd.assets` | 보유자산규모 | checkbox | 17% | 10억원~30억원 |
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

### 고객확인서(법인·단체) (`corporate_customer_due_diligence`) — 키 44개

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
| `corp.corp_type` | 법인구분 | checkbox | 100% | 중소기업 |
| `corp.listed` | 상장여부 | checkbox | 100% | 비상장 |
| `rep.name` | 대표자성명 | text | 100% | 박찬연 |
| `rep.name_en` | 대표자영문성명 | text | 100% | KANG SOONJUN |
| `rep.birth` | 대표자생년월일 | date | 100% | 1990.02.10 |
| `rep.nationality` | 대표자국적 | text | 100% | 대한민국 |
| `transaction.purpose` | 거래목적 | checkbox | 100% | 대출 |
| `transaction.fund_source` | 자금원천 | checkbox | 100% | 영업수익 |
| `owner_step` | 실제소유자확인단계 | checkbox | 100% | 1단계 |
| `owners[].name` | 성명 | text | 100% | 박찬연 |
| `owners[].birth` | 생년월일 | date | 100% | 1990.02.10 |
| `owners[].nationality` | 국적 | text | 100% | 대한민국 |
| `owners[].ratio` | 지분율 | percent | 100% | 74.04% |
| `owners[].relation` | 법인과의관계 | text | 100% | 대표이사 |
| `pep` | 외국의정치적주요인물여부 | checkbox | 100% | 아니오 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.corp` | 법인인감 | seal | 100% | 유니온무역대표이사인 |
| `bank_use.risk_grade` | 고객위험등급 | checkbox | 100% | 저위험 |
| `bank_use.documents[]` | 징구서류 | text | 100% | 사업자등록증 |
| `bank_use.branch` | 확인영업점 | text | 100% | 범어지점 |
| `seal.staff.clerk` | 담당 | seal | 100% | 변찬하 |
| `bank_use.clerk` | 담당 | text | 100% | 변찬하 |
| `seal.staff.manager` | 책임자 | seal | 100% | 이민재 |
| `bank_use.manager` | 책임자 | text | 100% | 이민재 |
| `bank_use.documents` | 징구서류 | checkbox_multi | 100% |  |
| `shareholders[].name` | 주주명 | text | 33% | 현예지 |
| `shareholders[].birth` | 생년월일 | date | 33% | 1966.08.12 |
| `shareholders[].shares` | 소유주식수 | number | 33% | 22,821 |
| `shareholders[].ratio` | 지분율 | percent | 33% | 22.82% |
| `shareholders[].relation` | 법인과의관계 | text | 33% | 대표이사 |
| `agent.name` | 거래담당자성명 | text | 17% | 이채지 |
| `agent.rrn` | 거래담당자실명번호 | rrn | 17% | 981116-2****** |
| `agent.position` | 직위관계 | text | 17% | 재무팀 과장 |

### 개인(신용)정보 수집·이용·제공·조회 동의서 (`privacy_consent`) — 키 25개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank.name` | 은행명 | text | 100% | 기업은행 |
| `consent.collect` | 수집이용동의 | checkbox | 100% | 동의함 |
| `consent.unique_id` | 고유식별정보처리동의 | checkbox | 100% | 동의함 |
| `providers[].name` | 제공받는자 | text | 100% | 신용정보집중기관(한국신용정보원) |
| `providers[].purpose` | 제공받는자의이용목적 | text | 100% | 본인의 신용을 판단하기 위한 자료로 활용하거나 공공기관에서 정책자료로 활… |
| `providers[].items` | 제공하는항목 | text | 100% | 개인식별정보, 신용거래정보, 신용도판단정보, 신용능력정보, 공공정보 |
| `providers[].period` | 제공받는자의보유이용기간 | text | 100% | 관련 법령 및 규약에서 정한 기간 |
| `consent.provide` | 제공동의 | checkbox | 100% | 동의함 |
| `consent.provide_unique_id` | 고유식별정보제공동의 | checkbox | 100% | 동의함 |
| `consent.inquiry` | 조회동의 | checkbox | 100% | 동의함 |
| `marketing.collect` | 마케팅수집이용동의 | checkbox | 100% | 동의함 |
| `marketing.provide` | 마케팅제공동의 | checkbox | 100% | 동의하지 않음 |
| `marketing.channels[]` | 연락방법 | text | 47% | 전화 |
| `date` | 작성일 | date | 100% | 2026.01.31 |
| `applicant.birth` | 생년월일 | date | 100% | 1990년 02월 10일 |
| `applicant.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.applicant` | 본인 | seal | 90% | 박찬연 |
| `sign.applicant` | 본인 | signature | 90% | 강순준 |
| `seal.staff.clerk` | 본인확인 | seal | 100% | 이태경 |
| `bank_use.clerk` | 본인확인 | text | 100% | 이태경 |
| `marketing.channels` | 연락방법 | checkbox_multi | 100% |  |
| `legal_rep.name` | 법정대리인 | text | 10% | 정수린 |
| `legal_rep.relation` | 본인과의관계 | text | 10% | 모 |
| `seal.legal_rep` | 법정대리인 | seal | 10% | 정수린 |
| `sign.legal_rep` | 법정대리인 | signature | 10% | 김나진 |

### 예금거래신청서 (`account_opening_application`) — 키 58개

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
| `product.type` | 예금종류 | checkbox | 100% | 정기예금 |
| `product.name` | 상품명 | text | 100% | 정기예금(일반) |
| `product.amount` | 신규금액 | amount | 100% | 119,000,000원 |
| `product.term` | 계약기간 | text | 47% | 36개월 |
| `product.interest_payment` | 이자지급방법 | text | 10% | 만기일시지급 |
| `product.linked_account` | 출금계좌 | account_no | 47% | 171-760452-29-611 |
| `passbook` | 통장발행 | checkbox | 100% | 미발행 |
| `seal_type` | 인감서명등록 | checkbox | 100% | 인감 |
| `check_card` | 체크카드 | checkbox | 100% | 미신청 |
| `ebank.internet` | 인터넷뱅킹 | checkbox | 100% | 신청 |
| `ebank.mobile` | 모바일뱅킹 | checkbox | 100% | 미신청 |
| `ebank.otp` | 보안매체 | checkbox | 100% | 모바일OTP |
| `ebank.limit_once` | 1회이체한도 | amount | 87% | 5,000,000원 |
| `ebank.limit_day` | 1일이체한도 | amount | 87% | 5,000,000원 |
| `alert` | 입출금알림 | checkbox | 100% | 앱 푸시 |
| `mail_to` | 우편물수령처 | checkbox | 100% | 자택 |
| `salary_transfer` | 급여이체지정 | checkbox | 100% | 미지정 |
| `protection_limit` | 예금자보호한도 | text | 93% | 1억원 |
| `signature` | 확인자 | text | 100% | 박찬연 |
| `date` | 신청일 | date | 100% | 2026년 1월 31일 |
| `seal.applicant` | 신청인 | seal | 100% | 이재주 |
| `sign.applicant` | 신청인 | signature | 100% | 박찬연 |
| `bank_use.account_no` | 계좌번호 | account_no | 100% | 956-619004-07-320 |
| `bank_use.branch` | 개설영업점 | text | 100% | 범어지점 |
| `bank_use.id_type` | 실명확인증표 | checkbox | 100% | 주민등록증 |
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

### 금융거래목적확인서 (`financial_transaction_purpose`) — 키 23개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `bank.name` | 은행명 | text | 100% | 기업은행 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.rrn` | 실명번호 | rrn | 100% | 900210-1659382 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `customer.mobile` | 연락처 | phone | 100% | 010-5907-7253 |
| `customer.job` | 직업 | text | 100% | 개인사업자 |
| `customer.company` | 직장명 | text | 93% | 동방학원 |
| `account_type` | 신규예금종류 | checkbox | 100% | 저축예금 |
| `purpose` | 금융거래목적 | checkbox | 100% | 사업자 거래 |
| `evidence` | 제출증빙서류 | text | 100% | 사업자등록증명 |
| `questions.q1` | 통장양도대여요청여부 | checkbox | 100% | 아니오 |
| `questions.q2` | 취업대출빙자요청여부 | checkbox | 100% | 아니오 |
| `questions.q3` | 최근타행계좌개설여부 | checkbox | 100% | 아니오 |
| `date` | 작성일 | date | 100% | 2026년 01월 31일 |
| `signature` | 고객성명 | text | 100% | 박찬연 |
| `seal.customer` | 고객 | seal | 100% | 박찬연 |
| `sign.customer` | 고객 | signature | 100% | 현예지 |
| `bank_use.result` | 처리결과 | checkbox | 100% | 일반계좌 개설 |
| `seal.staff.clerk` | 담당 | seal | 100% | 구호재 |
| `bank_use.clerk` | 담당 | text | 100% | 구호재 |
| `seal.staff.manager` | 책임자 | seal | 100% | 정연경 |
| `bank_use.manager` | 책임자 | text | 100% | 정연경 |
| `customer.nationality` | 국적 | text | 7% | 베트남 |

### 해외송금신청서 (`overseas_remittance_application`) — 키 52개

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
| `remittance.purpose` | 송금사유 | checkbox | 100% | 수입대금 |
| `remittance.purpose_code` | 지급사유코드 | number | 77% | 10103 |
| `remittance.charge` | 수수료부담 | checkbox | 100% | SHA |
| `remittance.method` | 송금방법 | checkbox | 100% | 전신송금(T/T) |
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

### 해외금융계좌 납세자 확인서(개인) (`fatca_crs`) — 키 22개

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
| `residence_category` | 해외거주자여부 | text | 100% | 미국 세법상 미국 거주자 |
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

## 하나은행 서식(원본)


### 본인확인서(FATCA CRS 법인,임의단체용) 본문 설명서(영문) (`hf407`) — 키 23개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `followingbusinesses` | followingbusinesses). | text | 100% |  |
| `bankruptcy` | bankruptcy | text | 100% |  |
| `RevenueCode` | RevenueCode | text | 100% |  |
| `USbank` | (6)U.S.bank | text | 100% |  |
| `FATCANonReporting` | FATCANon-Reporting | text | 100% |  |
| `requirements` | requirements | text | 100% |  |
| `Investment` | Investment | text | 100% |  |
| `BActiveNFFEs` | B.ActiveNFFEs | text | 100% |  |
| `Participation` | Participation | text | 100% |  |
| `Retirement` | Retirement | text | 100% |  |
| `Fund` | Fund | text | 100% |  |
| `NonReportingFI` | Non-ReportingFI | text | 100% |  |
| `Investment2` | Investment | text | 100% |  |
| `Office` | Office | text | 100% |  |
| `Retirement2` | Retirement | text | 100% |  |
| `Fund2` | Fund | text | 100% |  |
| `CRSNonReporting` | CRSNon-Reporting | text | 100% |  |
| `Services` | Services | text | 100% |  |
| `Commission` | Commission | text | 100% |  |
| `Vehicle` | Vehicle | text | 100% |  |
| `Office2` | Office | text | 100% |  |
| `Retirement3` | Retirement | text | 100% |  |
| `Fund3` | Fund | text | 100% |  |

### 본인확인서(FATCA CRS 개인,개인사업자용)(국문) (`hf408`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `성` | 성(SurName) | text | 100% |  |
| `customer.name` | 이름(GivenName) | text | 100% | 박찬연 |
| `customer.birth` | 생년월일 | date | 100% | 1990년 2월 10일 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `check.FATCA` | FATCA | checkbox | 100% | 미국세법상 미국거주자 |
| `check.CRS` | CRS | checkbox | 100% | 미국이외의 해외거주자 |
| `check.해당없음` | 해당없음 | checkbox | 100% | 모두 해당사항없음 |
| `거주관할권` | 거주관할권*(1) | text | 100% |  |
| `거주관할권2` | 거주관할권*(2) | text | 100% |  |
| `목록[].납세자번호` | 납세자번호(TIN) | text | 100% | 801-860243-72961 |
| `해외영문주소` | 해외영문주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `check.미발급국가` | 미발급국가 | checkbox | 100% | 미취득 |
| `check.미발급국가2` | 미발급국가 | checkbox | 100% | 미취득 |
| `내국인또는거주자증명서또는반증증표을제출한경우` | 내국인또는거주자증명서*또는반증증표*을제출한경우 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 인성명 | text | 100% | 박찬연 |
| `seal.signer` | 인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 인성명 | signature | 100% | 강순준 |
| `signer2.name` | 대리인성명 | text | 100% | 이주원 |
| `seal.signer2` | 대리인성명 | seal | 100% | 김아진 |
| `sign.signer2` | 대리인성명 | signature | 100% | 이주원 |

### 본인확인서(FATCA CRS 법인,임의단체용) 본문 설명서(국문) (`hf409`) — 키 52개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `는기관` | 는기관 | text | 100% |  |
| `능동적비금융법인여부` | 능동적비금융법인여부 | text | 100% |  |
| `미함` | 미함. | text | 100% |  |
| `재개하려는의도로조직변경중인경우` | 재개하려는의도로조직변경중인경우 | text | 100% |  |
| `된관계회사그룹` | 된관계회사그룹 | text | 100% |  |
| `위법인에귀속될것을요구할것` | 위법인에귀속될것을요구할것 | text | 100% |  |
| `미국미국정부소유기관미국정부대행기관` | 미국,미국정부소유기관,미국정부대행기관 | text | 100% |  |
| `미국연방세법제581조에정의된은행` | 미국연방세법제581조에정의된은행 | text | 100% | 국민은행 |
| `미국연방세법제6045조에정의된중개인` | 미국연방세법제6045(c)조에정의된중개인 | text | 100% |  |
| `유기관또는대행기관` | 유기관또는대행기관 | text | 100% |  |
| `라미국증권거래위원회에등록된법인` | 라미국증권거래위원회에등록된법인 | text | 100% |  |
| `신탁` | 신탁 | text | 100% |  |
| `여등록된자` | 여등록된자 | text | 100% |  |
| `다음의요건을모두충족하는금융기관` | 다음의요건을모두충족하는금융기관 | text | 100% | 기업은행 |
| `다음의요건을모두충족하는금융기관2` | 다음의요건을모두충족하는금융기관 | text | 100% | 신한은행 |
| `구분` | 구분[FATCA비보고대상유형] | text | 100% |  |
| `가법에따라금융회사로인가받고규제될것` | 가.법에따라금융회사로인가받고규제될것 | text | 100% | 신한은행 |
| `관행을가지지아니할것` | 관행을가지지아니할것 | text | 100% |  |
| `다음의요건을모두충족하는금융기관3` | 다음의요건을모두충족하는금융기관 | text | 100% | 신한은행 |
| `다음의요건을모두충족하는투자기구` | 다음의요건을모두충족하는투자기구 | text | 100% |  |
| `가투자법인이아닐것` | 가.투자법인이아닐것 | text | 100% |  |
| `의정보를보고하는신탁` | 의정보를보고하는신탁 | text | 100% |  |
| `사에해당하는경우로한정한다` | 사에해당하는경우로한정한다 | text | 100% |  |
| `부여받을것` | 부여받을것 | text | 100% |  |
| `별번호를포함할것` | 별번호를포함할것 | text | 100% | 606-443412-29918 |
| `바후원자로서의지위를취소하지아니할것` | 바.후원자로서의지위를취소하지아니할것 | text | 100% |  |
| `요건을충족하는피지배외국회사` | 요건을충족하는피지배외국회사 | text | 100% |  |
| `해완전히소유되는금융회사일것` | 해완전히소유되는금융회사일것 | text | 100% | 하나은행 |
| `후원자로서의지위를취소하지아니할것` | 후원자로서의지위를취소하지아니할것 | text | 100% |  |
| `법인` | 법인 | text | 100% |  |
| `가투자자문제공` | 가.투자자문제공 | text | 100% |  |
| `용을포함한다` | 용을포함한다 | text | 100% |  |
| `다음의요건을모두충족해야함` | 다음의요건을모두충족해야함 | text | 100% |  |
| `다음의요건을모두충족해야함2` | 다음의요건을모두충족해야함 | text | 100% |  |
| `가한국에서설립된펀드일것` | 가.한국에서설립된펀드일것 | text | 100% |  |
| `에만분배또는인출이가능할것` | 에만분배또는인출이가능할것 | text | 100% |  |
| `다음의요건을모두충족해야함3` | 다음의요건을모두충족해야함 | text | 100% |  |
| `별정우체국법에의한별정우체국연금관리단` | 별정우체국법에의한별정우체국연금관리단 | text | 100% |  |
| `다음각목의요건을모두충족하는금융회사` | 다음각목의요건을모두충족하는금융회사 | text | 100% | 국민은행 |
| `가한국에서설립된펀드일것2` | 가.한국에서설립된펀드일것 | text | 100% |  |
| `할것` | 할것 | text | 100% |  |
| `수익자또는참가자` | 수익자또는참가자 | text | 100% |  |
| `가투자법인라는이유만으로금융회사일것` | 가.투자법인라는이유만으로금융회사일것 | text | 100% | 신한은행 |
| `채권지분을소유할것` | 채권지분을소유할것 | text | 100% |  |
| `연금관리단` | 연금관리단 | text | 100% |  |
| `구분2` | 구분[CRS비보고대상유형] | text | 100% |  |
| `금융회사` | 금융회사 | text | 100% | 카카오뱅크 |
| `를보고하는신탁` | 를보고하는신탁 | text | 100% |  |
| `다음의요건을모두충족해야함4` | 다음의요건을모두충족해야함 | text | 100% |  |
| `다음의요건을모두충족해야함5` | 다음의요건을모두충족해야함 | text | 100% |  |
| `별정우체국법에의한별정우체국연금관리단2` | 별정우체국법에의한별정우체국연금관리단 | text | 100% |  |
| `연금간리단` | 연금간리단 | text | 100% |  |

### 본인확인서(FATCA CRS 법인,임의단체용)(영문) (`hf410`) — 키 31개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `NameofEntity` | NameofEntity | text | 100% |  |
| `BusinessRegistrationNo` | BusinessRegistrationNo. | biz_no | 100% | 264-82-36559 |
| `PhoneNo` | PhoneNo. | phone | 100% | 010-5907-7253 |
| `TaxpayerIdentificationNo` | TaxpayerIdentificationNo | text | 100% | 222-787118-55738 |
| `customer.address` | Address(HeadOffice'sAddress) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `NameofEntity2` | NameofEntity | text | 100% |  |
| `GIINKIINEINNO` | GIIN/KIIN/EINNO | text | 100% |  |
| `JurisdictionofResidence` | JurisdictionofResidence | text | 100% |  |
| `JurisdictionofResidence2` | JurisdictionofResidence | text | 100% |  |
| `JurisdictionofResidence3` | JurisdictionofResidence | text | 100% |  |
| `GivenName` | GivenName | text | 100% |  |
| `TaxpayerIdentificationNO` | TaxpayerIdentificationNO | amount | 100% |  |
| `Overseaaddress` | Overseaaddress | text | 100% |  |
| `GivenName2` | GivenName | text | 100% |  |
| `TaxpayerIdentificationNO2` | TaxpayerIdentificationNO | amount | 100% |  |
| `Overseaaddress2` | Overseaaddress | text | 100% |  |
| `GivenName3` | GivenName | text | 100% |  |
| `TaxpayerIdentificationNO3` | TaxpayerIdentificationNO | amount | 100% |  |
| `Overseaaddress3` | Overseaaddress | text | 100% |  |
| `check.Nonissuingc` | Non-issuingcountry | checkbox | 100% | Not required by tax authority |
| `check.Nonissuingc2` | Non-issuingcountry | checkbox | 100% | Not aqucired (write the reason |
| `check.Nonissuingc3` | Non-issuingcountry | checkbox | 100% | Non-issuing country |
| `SareRatio` | SareRatio(%)* | text | 100% |  |
| `Surname` | Surname | text | 100% |  |
| `SareRatio2` | SareRatio(%)* | text | 100% |  |
| `Surname2` | Surname | text | 100% |  |
| `SareRatio3` | SareRatio(%)* | text | 100% |  |
| `Surname3` | Surname | text | 100% |  |
| `customer.birth` | DateofBirth | date | 100% | 1990년 2월 10일 |
| `customer.birth2` | DateofBirth | date | 100% | 1990년 2월 10일 |
| `customer.birth3` | DateofBirth | date | 100% | 1990년 2월 10일 |

### [필수]본인 행정정보 제공 요구서(공공마이데이터 수신 묶음정보用 - 주민등록표 등·초본 조회) (`hf411`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.birth` | 생년월일 | date | 100% | 1990-02-10 |
| `customer.phone` | 연락처 | phone | 100% | 010-7321-8870 |
| `이용기관` | 이용기관 | text | 100% |  |
| `제공유형` | 제공유형 | text | 100% |  |
| `customer.name2` | 성명 | text | 100% | 박찬연 |
| `customer.birth2` | 생년월일 | date | 100% | 1990-02-10 |
| `customer.phone2` | 연락처 | phone | 100% | 010-7321-8870 |
| `하나은행` | (주)하나은행 | text | 100% | 국민은행 |
| `수신` | 수신 | text | 100% |  |
| `일회성제공` | 일회성제공 | text | 100% |  |
| `check.보기1` | 보기1 | checkbox | 100% | 보기1 |
| `check.제공요구하지않습니다` | 제공요구하지않습니다(아니오) | checkbox | 100% | 제공 요구하지 않습니다 (아니오) |
| `check.에는해당되는곳에표를합` | 에는해당되는곳에√표를합니다. | checkbox | 100% | 에는 해당되는 곳에 √ 표를 합니다. |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 강순준 |
| `금융수신` | ¶금융수신 | text | 100% |  |
| `금융거래의설정유지이행관리` | -금융거래의설정·유지·이행·관리 | text | 100% |  |
| `본인정보에관한사항` | [별지]본인정보에관한사항(상세항목) | text | 100% |  |

### [필수]본인 행정정보 제공 요구서(공공마이데이터 수신 묶음정보用 - 사업자등록증명 조회) (`hf412`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `이용기관` | 이용기관 | text | 100% |  |
| `제공유형` | 제공유형 | text | 100% |  |
| `customer.name2` | 성명 | text | 100% | 박찬연 |
| `customer.birth2` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.phone2` | 연락처 | phone | 100% | 010-5907-7253 |
| `하나은행` | (주)하나은행 | text | 100% | 농협은행 |
| `수신` | 수신 | text | 100% |  |
| `일회성제공` | 일회성제공 | text | 100% |  |
| `check.보기1` | 보기1 | checkbox | 100% | 보기1 |
| `check.제공요구하지않습니다` | 제공요구하지않습니다(아니오) | checkbox | 100% | 제공 요구하지 않습니다 (아니오) |
| `check.에는해당되는곳에표를합` | 에는해당되는곳에√표를합니다. | checkbox | 100% | 에는 해당되는 곳에 √ 표를 합니다. |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 이민빈 |
| `sign.signer` | 본인성명 | signature | 100% | 현예지 |
| `금융수신` | ¶금융수신 | text | 100% |  |
| `금융거래의설정유지이행관리` | -금융거래의설정·유지·이행·관리 | text | 100% |  |
| `본인정보에관한사항` | [별지]본인정보에관한사항(상세항목) | text | 100% |  |

### 고객확인서(법인,고유번호나 납세번호가 있는 임의 단체용) (`hf413`) — 키 70개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].사업장` | 사업장(국내) | text | 100% |  |
| `대표자3` | 대표자3 | text | 100% |  |
| `전화` | 전화 | phone | 100% | 010-5907-7253 |
| `대표자1` | 대표자1 | text | 100% |  |
| `대표자2` | 대표자2 | text | 100% |  |
| `대표자32` | 대표자3 | text | 100% |  |
| `한글명` | 한글명 | text | 100% | 신현예 |
| `customer.name_en` | 영문명(외국법인필수) | text | 100% | PARK CHANYEON |
| `company.biz_item` | 업종(업태/종목) | text | 100% | 의류 도매 |
| `customer.address` | 주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `전화2` | 전화 | phone | 100% | 010-5907-7253 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `전화3` | 전화 | phone | 100% | 010-5907-7253 |
| `company.established` | 설립일 | date | 100% | 2018.11.01 |
| `check.기업규모` | 기업규모 | checkbox | 100% | 중소기업 |
| `check.상장여부` | 상장여부 | checkbox | 100% | 상장 |
| `목록[].영문명` | 영문명 | text | 100% |  |
| `FAX` | FAX | phone | 100% | 043-783-2775 |
| `company.biz_no` | 사업자등록번호(고유번호및납세번호등포함) | biz_no | 100% | 264-82-36559 |
| `설립목적` | 설립목적(비영리법인,단체) | text | 100% | 주택구입 |
| `FAX2` | FAX | phone | 100% | 043-783-2775 |
| `FAX3` | FAX | phone | 100% | 043-783-2775 |
| `홈페이지` | 홈페이지 | text | 100% |  |
| `check.국내` | 국내 | checkbox | 100% | 코스닥시장 |
| `목록[].생년월일` | 생년월일(사업자번호) | text | 100% | 2025년 10월 18일 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `목록[].국적` | 국적(본점소재지) | text | 100% |  |
| `check.일회성거래` | 일회성거래(무통장입금,수표발행☞지급등) | checkbox | 100% | 상속 / 증여성거래 |
| `check.대표자정보` | 대표자정보 | checkbox | 100% | 단독대표 |
| `check.뉴욕증권거래소` | 뉴욕증권거래소 | checkbox | 100% | 뉴욕증권거래소 |
| `check.홍콩증권거래소` | 홍콩증권거래소 | checkbox | 100% | 홍콩증권거래소 |
| `check.예` | 예(비영리단체) | checkbox | 100% | 아니오(비영리단체 해당안됨) |
| `check.계좌개설` | 계좌개설 | checkbox | 100% | 공과금 납부결제 |
| `check.대출원리금상환결제` | (예금,대출등) | checkbox | 100% | 대출원리금 상환 결제 |
| `check.사업소득` | 사업소득 | checkbox | 100% | 사업소득 |
| `check.상속증여` | 상속/증여 | checkbox | 100% | 상속 / 증여 |
| `check.추가확인` | 추가확인 | checkbox | 100% | 대부업자 |
| `check.필요업종` | 필요업종 | checkbox | 100% | 공인회계사업 |
| `check.대표자` | 대표자 | checkbox | 100% | 대리인 성명 |
| `거래목적` | 거래목적 | text | 100% | 자녀 교육비 |
| `25이상의결권이있는주식출자지분을보유한사람` | 25%이상의결권이있는주식/출자지분을보유한사람 | text | 100% |  |
| `의결권있는주식및출자지분의최대소유자` | 의결권있는주식및출자지분의최대소유자 | text | 100% |  |
| `대표자또는임원등의과반수를선임한주주` | 대표자또는임원등의과반수를선임한주주 | text | 100% |  |
| `법인단체를사실상지배하는자` | 법인•단체를사실상지배하는자 | text | 100% |  |
| `법인단체의대표자중1인` | 법인•단체의대표자중1인 | text | 100% |  |
| `목록[].한글명` | 한글명(상호명) | text | 100% | 박찬연 |
| `check.25이상의결권이있는주식출자지분을보유한사람` | 25%이상의결권이있는주식/출자지분을보유한사람 | checkbox | 100% | 보기1 |
| `check.의결권있는주식및출자지분의최대소유자` | 의결권있는주식및출자지분의최대소유자 | checkbox | 100% | 보기1 |
| `check.대표자또는임원등의과반수를선임한주주` | 대표자또는임원등의과반수를선임한주주 | checkbox | 100% | 보기1 |
| `check.법인단체를사실상지배하는자` | 법인•단체를사실상지배하는자 | checkbox | 100% | 보기1 |
| `check.법인단체의대표자중1인` | 법인•단체의대표자중1인 | checkbox | 100% | 보기1 |
| `목록[].지분율` | 지분율 | number | 100% | 35 |
| `항목` | 항목 | text | 100% |  |
| `목록[].Y` | Y | text | 100% |  |
| `목록[].N` | N | text | 100% |  |
| `지배자` | 지배자 | text | 100% |  |
| `목록[].지배형태` | 지배형태 | text | 100% |  |
| `agent.name` | 성명 | text | 100% | 강석호 |
| `agent.relation` | 본인과의관계 | text | 100% | 부 |
| `agent.birth` | 생년월일 | date | 100% | 1962년 12월 19일 |
| `agent.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `agent.phone` | 전화번호 | phone | 100% | 010-6515-4769 |
| `check.국가또는지방자치단체1` | 국가또는지방자치단체1 | checkbox | 100% | 사업보고서 제출대상 법인 (상장법인 1) 등) |
| `check.실제소유자와사실상지배자` | 실제소유자와사실상지배자가동일합니다 | checkbox | 100% | 실제소유자와 사실상지배자가 동일합니다 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 법인/단체명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 법인/단체명 | seal | 100% | (주)유니온무역 |
| `sign.signer` | 법인/단체명 | signature | 100% | 주식회사 한빛패션 |
| `check.작성자` | 작성자( | checkbox | 100% | 대리인) 성명 |
| `customer.name` | 위임인(법인/단체명) | text | 100% | 박찬연 |

### [필수] 개인(신용)정보 수집·이용·제공 동의서 [공공마이데이터 주민등록 등·초본 조회용] (`hf414`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `일반개인정보` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `수집이용목적` | 수집·이용목적 | text | 100% | 생활자금 |
| `제공일로부터5년이내보유이용` | -제공일로부터5년이내보유·이용 | text | 100% |  |
| `일반개인정보2` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 이욱유 |
| `signer2.name` | 대리인성명 | text | 100% | 이하지 |
| `seal.signer2` | 대리인성명 | seal | 100% | 선영빈 |
| `sign.signer2` | 대리인성명 | signature | 100% | 이하지 |

### [필수] 개인(신용)정보 제3자 제공 동의서 [공공마이데이터 주민등록 등·초본 조회용] (`hf415`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `하나은행` | -(주)하나은행 | text | 100% |  |
| `고유식별정보` | ■고유식별정보 | text | 100% |  |
| `공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 이욱유 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `signer2.name` | 대리인성명 | text | 100% | 옥영아 |
| `seal.signer2` | 대리인성명 | seal | 100% | 옥영아 |
| `sign.signer2` | 대리인성명 | signature | 100% |  |
| `산정보` | 산정보 | text | 100% |  |
| `본과동일한공공마이데이터` | 본과동일한공공마이데이터 | text | 100% |  |
| `행정안전부주민등록등초본` | ■행정안전부:주민등록등·초본 | text | 100% |  |

### [필수] 개인(신용)정보 수집·이용·제공 동의서 [공공마이데이터 사업자정보 조회용] (`hf416`) — 키 17개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `고유식별정보` | ■고유식별정보 | text | 100% |  |
| `일반개인정보` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집☞이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집☞이용에동의하십니까? | checkbox | 100% | 동의함 |
| `수집이용목적` | 수집·이용목적 | text | 100% | 결혼자금 |
| `제공일로부터5년이내보유이용` | -제공일로부터5년이내보유·이용 | text | 100% |  |
| `고유식별정보2` | ■고유식별정보 | text | 100% |  |
| `일반개인정보2` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 강순준 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `signer2.name` | 대리인성명 | text | 100% | 강순준 |
| `seal.signer2` | 대리인성명 | seal | 100% | 강순준 |
| `sign.signer2` | 대리인성명 | signature | 100% | 이민빈 |

### [필수] 개인(신용)정보 제3자 제공 동의서 [공공마이데이터 사업자정보 조회용] (`hf417`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `하나은행` | -(주)하나은행 | text | 100% |  |
| `고유식별정보` | ■고유식별정보 | text | 100% |  |
| `공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 강순준 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `signer2.name` | 대리인성명 | text | 100% | 강순준 |
| `seal.signer2` | 대리인성명 | seal | 100% | 우지현 |
| `sign.signer2` | 대리인성명 | signature | 100% | 이주원 |
| `산정보` | 산정보 | text | 100% |  |
| `본과동일한공공마이데이터` | 본과동일한공공마이데이터 | text | 100% |  |
| `국세청사업자등록증명` | ■국세청:사업자등록증명 | text | 100% |  |

### [필수] 개인(신용)정보 수집·이용 동의서 [비대면 스크래핑 서비스] (`hf418`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `고유식별정보` | ■고유식별정보 | text | 100% |  |
| `일반개인정보` | ■■일반개인정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `성명휴대전화번호자녀성명` | 성명,휴대전화번호,자녀성명 | phone | 100% | 010-7321-8870 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 현예지 |
| `sign.signer` | 본인성명 | signature | 100% | 강순준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 김연지 |
| `seal.signer2` | 대리인성명 | seal | 100% | 김나우 |
| `sign.signer2` | 대리인성명 | signature | 100% | 김연지 |

### [필수] 개인(신용)정보 수집 · 이용 동의서 (비여신 금융거래) (`hf419`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 김소윤 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 박찬연 |
| `seal.signer2` | 대리인성명 | seal | 100% | 박찬연 |
| `sign.signer2` | 대리인성명 | signature | 100% | 이주원 |
| `signer3.name` | 법정대리인성명 | text | 100% | 현예지 |
| `seal.signer3` | 법정대리인성명 | seal | 100% | 이주원 |
| `sign.signer3` | 법정대리인성명 | signature | 100% | 현예지 |
| `온오프라인거래연계및본인식별` | -온·오프라인(금융)거래연계및본인식별 | text | 100% |  |
| `금융사고조사분쟁해결민원처리` | -금융사고조사,분쟁해결,민원처리 | text | 100% |  |

### 비대면 계좌개설 안심차단 서비스 신청서 (`hf420`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.구분` | 구분 | checkbox | 100% | 신청 |
| `check.대리인정보` | 대리인정보 | checkbox | 100% | 임의대리인 신청시에도 신청내역에 대한 안내는 신청인(본인)에게 통지됩니다 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.rrn` | 주민등록번호 | rrn | 100% | 900210-1****** |
| `agent.name` | 성명 | text | 100% | 박영준 |
| `agent.birth` | 생년월일 | date | 100% | 1962년 12월 19일 |
| `check.해제` | 해제 | checkbox | 100% | 해제 |
| `check.휴대전화번호` | 휴대전화번호 | checkbox | 100% | 신청내역 통지 동의 |
| `신청인과의관계` | 신청인과의관계 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 강순준 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |
| `signer2.name` | 대리인 | text | 100% | 전영경 |
| `seal.signer2` | 대리인 | seal | 100% | 전영경 |
| `sign.signer2` | 대리인 | signature | 100% | 오예아 |

### [필수] 개인(신용)정보 수집·이용·제공·조회 동의서 [비대면 계좌개설 안심차단 서비스] (`hf421`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `고유식별정보` | ■고유식별정보 | text | 100% |  |
| `공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `수집이용목적` | 수집·이용목적 | text | 100% | 주택구입 |
| `금융사고조사분쟁해결민원처리` | -금융사고조사,분쟁해결,민원처리 | text | 100% |  |
| `거부권리및불이익` | 거부권리및불이익 | text | 100% |  |
| `목록[].고유식별정보` | ■고유식별정보 | text | 100% |  |
| `목록[].공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위고유식별정보조회에동의하십니까` | 위고유식별정보조회에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보조회에동의하십니까` | 위개인(신용)정보조회에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 최우빈 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 전영경 |
| `seal.signer2` | 대리인성명 | seal | 100% | 전영경 |
| `sign.signer2` | 대리인성명 | signature | 100% | 하숙인 |
| `거부권리및불이익2` | 거부권리및불이익 | text | 100% |  |

### [필수] 개인(신용)정보 수집·이용·조회 동의서[비대면 계좌개설 안심차단 신청여부 조회용] (`hf422`) — 키 19개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].고유식별정보` | ■고유식별정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `비대면계좌개설안심차단신청여부조회` | -비대면계좌개설안심차단신청여부조회 | text | 100% |  |
| `수집이용목적` | 수집·이용목적 | text | 100% | 해외 이주 |
| `금융사고조사분쟁해결민원처리` | -금융사고조사,분쟁해결,민원처리 | text | 100% |  |
| `보유및이용기간` | 보유및이용기간 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까2` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보조회에동의하십니까` | 위고유식별정보조회에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보조회에동의하십니까` | 위개인(신용)정보조회에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 강순준 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 박찬연 |
| `seal.signer2` | 대리인성명 | seal | 100% |  |
| `sign.signer2` | 대리인성명 | signature | 100% | 민환은 |

### [선택] 개인(신용)정보 수집ㆍ이용 및 제공동의서 (상품서비스 안내 등) (`hf423`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위개인정보수집이용에동의하십니까안심` | 위개인(신용)정보수집·이용에동의하십니까?안심 | checkbox | 100% | 동의함 |
| `check.광고성정보의수신을동의하시겠습니까` | 광고성정보의수신을동의하시겠습니까? | checkbox | 100% | 동의하지 않음 |
| `check.14전체` | 1~4전체 | checkbox | 100% | 보기1 |
| `check.문자메시지` | 문자메시지(SMS,LMS,모바일메시지등) | checkbox | 100% | 보기1 |
| `check.전자우편` | 전자우편(이메일) | checkbox | 100% | 보기1 |
| `수집이용목적` | 수집·이용목적 | text | 100% | 결혼자금 |
| `일반개인정보` | ■일반개인정보 | text | 100% |  |
| `성명생년월일` | 성명,생년월일 | date | 100% | 2026.01.03 |
| `check.위개인정보제공에동의하십니까안심` | 위개인(신용)정보제공에동의하십니까?안심 | checkbox | 100% | 동의함 |
| `하나금융그룹계열사` | -하나금융그룹계열사 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer` | 성명 | seal | 100% | 전영경 |
| `sign.signer` | 성명 | signature | 100% | 현예지 |
| `signer2.name` | 법정대리인 | text | 100% | 현예지 |
| `seal.signer2` | 법정대리인 | seal | 100% | 전영경 |
| `sign.signer2` | 법정대리인 | signature | 100% | 현예지 |

### [필수] 개인(신용)정보 제3자제공 동의서 [하나카드 발급_미성년자용] (`hf424`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `하나카드` | 하나카드 | text | 100% |  |
| `고유식별정보` | ■고유식별정보 | text | 100% |  |
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 김소윤 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 여기준 |
| `seal.signer2` | 대리인성명 | seal | 100% | 이하지 |
| `sign.signer2` | 대리인성명 | signature | 100% | 하숙인 |
| `제공받는자의이용목적` | 제공받는자의이용목적 | text | 100% | 사업자금 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |

### [필수] 개인(신용)정보 제3자제공 동의서 [하나카드 발급_법정대리인용] (`hf425`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `하나카드` | 하나카드 | text | 100% |  |
| `제공일로부터5년까지보유이용` | -제공일로부터5년까지보유·이용 | text | 100% |  |
| `고유식별정보` | ■고유식별정보 | text | 100% |  |
| `일반개인정보` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 강순준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 정현윤 |
| `seal.signer2` | 대리인성명 | seal | 100% |  |
| `sign.signer2` | 대리인성명 | signature | 100% |  |
| `제공받는자의이용목적` | 제공받는자의이용목적 | text | 100% | 만기 해지 |
| `우그기간을따름` | 우그기간을따름 | text | 100% |  |
| `휴대전화번호email주소` | 휴대전화번호,e-mail주소 | phone | 100% | 010-5907-7253 |

### 이의제기 신청서 (`hf426`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `전자우편주소` | 전자우편주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `개설점포` | 개설점포 | text | 100% | 범어지점 |
| `예금종별` | 예금종별 | text | 100% | 하나 MMF |
| `customer.name` | 명의인 | text | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인성명 | text | 100% | 박찬연 |
| `seal.signer` | 신청인성명 | seal | 100% | 강순준 |
| `sign.signer` | 신청인성명 | signature | 100% | 박찬연 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `customer.phone2` | 휴대전화번호 | phone | 100% | 010-5907-7253 |
| `금융회사` | 금융회사 | text | 100% | 기업은행 |
| `지급정지` | 지급정지 | text | 100% |  |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |

### 아이부자 선불전자지급수단 잔액 상속(지급) 및 서비스 해지 요청서(위임장 겸용) (`hf427`) — 키 19개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.birth` | 생년월일 | date | 100% | 900210 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `주된상속인` | 주된상속인(소득귀속인) | text | 100% |  |
| `customer.birth2` | 생년월일 | date | 100% | 900210 |
| `customer.phone2` | 연락처 | phone | 100% | 010-5907-7253 |
| `account` | 계좌번호 | account_no | 100% | 774-646914-96117 |
| `check.상속인` | 상속인 | checkbox | 100% | 본인 |
| `check.상속인2` | 상속인 | checkbox | 100% | 본인 |
| `check.상속인3` | 상속인 | checkbox | 100% | 위임(별도위임장 작성) |
| `check.상속인4` | 상속인 | checkbox | 100% | 본인 |
| `check.상속인5` | 상속인 | checkbox | 100% | 본인 |
| `check.상속인6` | 상속인 | checkbox | 100% | 본인 |
| `check.상속인7` | 상속인 | checkbox | 100% | 본인 |
| `check.상속인8` | 상속인 | checkbox | 100% | 본인 |
| `check.상속인9` | 상속인 | checkbox | 100% | 위임(별도위임장 작성) |
| `목록[].성명` | 성명 | text | 100% | 여형지 |
| `목록[].생년월일` | 생년월일 | text | 100% | 2025.08.25 |
| `목록[].연락처` | 연락처 | text | 100% | 010-5907-7253 |

### 본인확인서(FATCA CRS 법인,임의단체용)(국문) (`hf428`) — 키 43개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `가고객정보` | 가.고객정보 | text | 100% |  |
| `company.name` | 법인(단체)명 | text | 100% | (주)유니온무역 |
| `구분선택` | 구분선택(☑) | text | 100% |  |
| `company.name2` | 법인(단체)명 | text | 100% | (주)유니온무역 |
| `口국내법인` | 口국내법인(단체) | text | 100% |  |
| `company.biz_no` | 사업자번호 | biz_no | 100% | 264-82-36559 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `거주관할권` | 거주관할권 | text | 100% |  |
| `납세자번호` | 납세자번호(TIN) | text | 100% | 255140-5994012 |
| `관할권주소` | 관할권(소재지)주소(본점,설립관할권) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 법인명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 법인명 | seal | 100% | (주)유니온무역 |
| `sign.signer` | 법인명 | signature | 100% | 주식회사 한빛패션 |
| `나확인사항` | 나.확인사항 | text | 100% |  |
| `口11공익적법인` | 口11.공익적법인(단체) | text | 100% |  |
| `c` | c | text | 100% |  |
| `d` | d | text | 100% |  |
| `口EIN口GIIN口기타` | 口EIN口GIIN口기타 | text | 100% | 급여 수령 |
| `목록[].실질지배자` | 실질지배자(1) | text | 100% |  |
| `목록[].거주관할권` | 거주관할권(국가) | text | 100% |  |
| `customer.name` | 이름(GivenName) | text | 100% | 박찬연 |
| `목록[].납세자번호` | 납세자번호(TIN) | text | 100% | 8493-2873 |
| `customer.name2` | 이름(GivenName) | text | 100% | 박찬연 |
| `customer.name3` | 이름(GivenName) | text | 100% | 박찬연 |
| `거주관할권주소` | 거주관할권주소(영문) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `거주관할권주소2` | 거주관할권주소(영문) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `거주관할권주소3` | 거주관할권주소(영문) | text | 100% | 서울특별시 송파구 중대로 174, 119동 2202호 |
| `check.미발급국가` | 미발급국가 | checkbox | 100% | 미취득 (사유기재 |
| `check.미발급국가2` | 미발급국가 | checkbox | 100% | 미발급국가 |
| `check.미발급국가3` | 미발급국가 | checkbox | 100% | 미취득 (사유기재 |
| `지분율` | 지분율(%) | number | 100% | 50 |
| `성` | 성(Surname) | text | 100% |  |
| `지분율2` | 지분율(%) | number | 100% | 70 |
| `성2` | 성(Surname) | text | 100% |  |
| `지분율3` | 지분율(%) | number | 100% | 60 |
| `성3` | 성(Surname) | text | 100% |  |
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.birth2` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.birth3` | 생년월일 | date | 100% | 1990.02.10 |
| `口01주권상장법인` | 口01.주권상장법인 | text | 100% |  |
| `口03미국정부기관등` | 口03.미국정부기관등 | text | 100% |  |
| `口25별정우체국연금관리단` | 口25.별정우체국연금관리단 | text | 100% |  |

### 본인확인서(FATCA CRS 개인,개인사업자용)(영문) (`hf429`) — 키 26개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `CustomerProfile` | CustomerProfile | text | 100% |  |
| `목록[].value` | (CapitalLetter)* | amount | 100% |  |
| `WhetherOverseasResidentorNot` | WhetherOverseasResidentorNot | text | 100% |  |
| `IdentificationNumberetc` | IdentificationNumber(TIN),etc. | text | 100% |  |
| `Reportingcountry` | Reportingcountry | text | 100% |  |
| `목록[].FATCA` | FATCA | text | 100% |  |
| `목록[].CRS` | CRS | text | 100% |  |
| `NA` | N/A | text | 100% |  |
| `Surname` | Surname(성) | text | 100% |  |
| `Surname2` | Surname(성) | text | 100% |  |
| `GivenName` | GivenName(이름) | text | 100% |  |
| `check.UScitizen` | U.S.citizen(includingdualcitizenship) | checkbox | 100% | U.S. permanent resident |
| `check.Residentinac` | ResidentinacountryotherthanU.S | checkbox | 100% | Resident in a country other than U.S |
| `check.AllNA` | AllN/A | checkbox | 100% | All N/A |
| `Jurisdictionof` | Jurisdictionof | text | 100% |  |
| `Country` | Country*(2) | text | 100% | 필리핀 |
| `OverseaEnglishaddress` | OverseaEnglishaddress | text | 100% |  |
| `Surname3` | Surname(성) | text | 100% |  |
| `GivenName2` | GivenName(이름) | text | 100% |  |
| `customer.birth` | DateofBirth | date | 100% | 1997.05.14 |
| `customer.birth2` | DateofBirth | date | 100% | 1990.02.10 |
| `목록[].PhoneNo` | PhoneNo. | phone | 100% | 010-5907-7253 |
| `check.Nonissuingc` | Non-issuingcountry | checkbox | 100% | Non-issuing country |
| `check.Nonissuingc2` | Non-issuingcountry | checkbox | 100% | Non-issuing country |
| `customer.birth3` | DateofBirth | date | 100% | 1990.02.10 |
| `PhoneNo` | PhoneNo. | phone | 100% | 010-5907-7253 |

### 민원신청서 (`hf430`) — 키 36개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].기타` | 기타 | text | 100% | 전세자금 |
| `기타` | 기타 | text | 100% | 타행 이체 |
| `기타2` | 기타 | text | 100% | 주택구입 |
| `customer.email` | e-mail | text | 100% | chanyeon363@naver.com |
| `agent.email` | e-mail | text | 100% | youngjun641@nate.com |
| `signer.name` | 본인확인(직원기재) | text | 100% | 박찬연 |
| `seal.signer` | 본인확인(직원기재) | seal | 100% | 박찬연 |
| `sign.signer` | 본인확인(직원기재) | signature | 100% | 이욱유 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.name` | 신청인 | text | 100% | 박찬연 |
| `본인확인` | 본인확인(직원기재) | text | 100% |  |
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `신용거래정보2` | ■신용거래정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까2` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer2` | 본인성명 | seal | 100% | 강순준 |
| `sign.signer2` | 본인성명 | signature | 100% | 현예지 |
| `signer3.name` | 대리인성명 | text | 100% | 최우빈 |
| `seal.signer3` | 대리인성명 | seal | 100% | 김소윤 |
| `sign.signer3` | 대리인성명 | signature | 100% | 여기준 |
| `기타3` | 기타 | text | 100% | 의료비 |
| `기타4` | 기타 | text | 100% | 결혼자금 |
| `customer.email2` | e-mail | text | 100% | chanyeon363@naver.com |
| `agent.email2` | e-mail | text | 100% | youngjun641@nate.com |
| `signer4.name` | 본인확인(직원기재) | text | 100% | 박찬연 |
| `seal.signer4` | 본인확인(직원기재) | seal | 100% | 현예지 |
| `sign.signer4` | 본인확인(직원기재) | signature | 100% | 박찬연 |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer5.name` | 위임자(본인) | text | 100% | 박찬연 |
| `seal.signer5` | 위임자(본인) | seal | 100% | 이민빈 |
| `sign.signer5` | 위임자(본인) | signature | 100% | 박찬연 |
| `본인확인2` | 본인확인(직원기재) | text | 100% |  |

### 전자금융거래 사고 피해 신고서(통합서류) (`hf431`) — 키 112개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `company.name` | 법인명 | text | 100% | (주)유니온무역 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `check.진행관련SMS수신동의여부` | 진행관련SMS수신동의여부】 | checkbox | 100% | 동의함 |
| `check.이용자본인이직접지급지시` | 이용자본인이직접지급지시한금융거래(가족사칭,협박,대출사기등 | checkbox | 100% | 이용자 본인이 직접 지급지시한 금융거래(가족 사칭, 협박, 대출사기 등  |
| `check.동거가족또는지인에의한거` | 동거가족또는지인에의한거래 | checkbox | 100% | 동거가족 또는 지인에 의한 거래 |
| `check.이용자가접근매체를양도양` | 이용자가접근매체를양도·양수하거나질권을설정하는등전자금융거래법제 | checkbox | 100% | 이용자가 접근매체를 양도·양수하거나 질권을 설정하는 등 전자금융거래법 제 |
| `check.법인인이용자의기관내지는` | 법인인이용자의기관내지는피용자로서법인을위한금융거래 | checkbox | 100% | 법인인 이용자의 기관 내지는 피용자로서 법인을 위한 금융거래 |
| `check.재화의공급을가장한상거래` | 재화의공급을가장한상거래로서이용자본인의의지로신청·계약한금융거 | checkbox | 100% | 재화의 공급을 가장한 상거래로서 이용자 본인의 의지로 신청·계약한 금융거 |
| `check.용역의제공을가장한거래로` | 용역의제공을가장한거래로서이용자본인의의지로신청·계약한금융거래 | checkbox | 100% | 용역의 제공을 가장한 거래로서 이용자 본인의 의지로 신청·계약한 금융거래 |
| `check.불법적이거나비정상적인재` | 불법적이거나비정상적인재화의공급또는용역의제공등과관련된금융거 | checkbox | 100% | 불법적이거나 비정상적인 재화의 공급 또는 용역의 제공 등과 관련된 금융거 |
| `check.간편송금업체를통한금융거` | 간편송금업체(OO페이)를통한금융거래 | checkbox | 100% | 간편송금업체(OO페이)를 통한 금융거래 |
| `check.영업점창구를통한거래등대` | 영업점창구를통한거래등대면금융거래 | checkbox | 100% | 영업점 창구를 통한 거래 등 대면 금융거래 |
| `check.은행의보이스피싱의심거래` | 은행의보이스피싱의심거래감지등에따른피해예방안내에도불구하고 | checkbox | 100% | 은행의 보이스피싱 의심거래 감지 등에 따른 피해 예방 안내에도 불구하고  |
| `check.본사고발생이전에사고발` | 본사고발생이전에사고발생은행에서「전기통신금융사기피해방지및 | checkbox | 100% | 본 사고 발생 이전에 사고발생 은행에서 「전기통신금융사기 피해 방지 및 |
| `check.신용체크카드물품구입단` | 신용/체크카드물품구입,단기카드대출(현금서비스)및장기카드대출(카드 | checkbox | 100% | 신용/체크카드 물품 구입, 단기카드대출(현금서비스) 및 장기카드대출(카드 |
| `check.사실관계확인결과전자금융` | 사실관계확인결과전자금융사고로보기어려운경우 | checkbox | 100% | 사실관계 확인 결과 전자금융사고로 보기 어려운 경우 |
| `check.소송등법적분쟁이진행중이` | 소송등법적분쟁이진행중이거나판결이확정된경우 | checkbox | 100% | 소송 등 법적 분쟁이 진행중이거나 판결이 확정된 경우 |
| `피해신고제외대상확인` | 피해신고제외대상확인 | text | 100% |  |
| `출금은행` | 출금은행 | text | 100% | 농협은행 |
| `입금은행` | 입금은행(상대은행) | text | 100% | 국민은행 |
| `출금은행2` | 출금은행 | text | 100% | 하나은행 |
| `입금은행2` | 입금은행(상대은행) | text | 100% | 우리은행 |
| `출금은행3` | 출금은행 | text | 100% | 카카오뱅크 |
| `입금은행3` | 입금은행(상대은행) | text | 100% | 신한은행 |
| `사고발생총피해금액` | 사고발생총피해금액 | number | 100% | 5,180,000 |
| `account` | 출금계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.입금계좌예금주` | 입금(상대)계좌예금주 | checkbox | 100% | 타인( |
| `account2` | 출금계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.입금계좌예금주2` | 입금(상대)계좌예금주 | checkbox | 100% | 본인 |
| `account3` | 출금계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.입금계좌예금주3` | 입금(상대)계좌예금주 | checkbox | 100% | 타인( |
| `check.신분증분실신고` | 신분증분실신고(해당기관앞) | checkbox | 100% | 아니오 |
| `check.명의도용휴대전화개설신고` | 명의도용휴대전화개설신고(통신사앞) | checkbox | 100% | 예 (신고일 |
| `check.휴대전화분실신고` | 휴대전화분실신고(통신사앞) | checkbox | 100% | 아니오 |
| `기타` | 기타 | text | 100% | 계좌 정리 |
| `check.피해구제환급신청` | 피해구제환급신청 | checkbox | 100% | 기타( |
| `수사기관` | 수사기관 | text | 100% |  |
| `check.이용자와은행사이에민법제` | 이용자와은행사이에민법제731조소정의화해(합의)가이미성립된 | checkbox | 100% | 이용자와 은행 사이에 민법 제731조 소정의 화해(합의)가 이미 성립된  |
| `check.수사기관등의수사를통해전` | 수사기관등의수사를통해전자금융사고가아닌경우로판명된경우 | checkbox | 100% | 수사기관 등의 수사를 통해 전자금융사고가 아닌 경우로 판명된 경우 |
| `check.기타비대면금융사고책임` | 기타(비대면금융사고책임분담협약참여은행외금융회사를통한비대면 | checkbox | 100% | 기타(비대면 금융사고 책임분담 협약 참여은행 외 금융회사를 통한 비대면  |
| `check.사고유형중한가지이상이라도` | 사고유형중한가지이상이라도【 | checkbox | 100% | ( |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 이욱유 |
| `check.손님본인` | 손님본인 | checkbox | 100% | 지인 |
| `check.예` | 예 | checkbox | 100% | 기타( |
| `check.예2` | 예 | checkbox | 100% | 예 |
| `check.신분증SMS문자메시지` | 신분증(SMS문자메시지또는카톡등을통한신분증사본사진,파일 | checkbox | 100% | 신분증 (SMS 문자메시지 또는 카톡 등을 통한 신분증 사본 사진, 파일 |
| `check.개인정보` | 개인정보(이름,휴대전화번호,주민등록번호등) | checkbox | 100% | 개인정보(이름, 휴대전화번호, 주민등록번호 등) |
| `check.전자적장치` | 전자적장치(휴대전화등,휴대전화를빌려준경우포함) | checkbox | 100% | 전자적 장치(휴대전화 등, 휴대전화를 빌려준 경우 포함) |
| `check.계좌번호및계좌용비밀번호` | 계좌번호및계좌용비밀번호 | checkbox | 100% | 계좌번호 및 계좌용 비밀번호 |
| `check.보안매체제공또는보안매체` | 보안매체(OTP,보안카드,인증서등)제공또는보안매체용비밀번호 | checkbox | 100% | 보안매체(OTP, 보안카드, 인증서 등) 제공 또는 보안매체용 비밀번호  |
| `check.기타전자금융관련정보` | 기타전자금융관련정보( | checkbox | 100% | 기타 전자금융 관련정보( |
| `check.예3` | 예 | checkbox | 100% | 아니오 |
| `check.보관방식` | 보관방식 | checkbox | 100% | 아니오 |
| `check.예4` | 예 | checkbox | 100% | 예 |
| `check.경우해당기관앞신분증분실신고를` | 경우,해당기관앞신분증분실신고를 | checkbox | 100% | 예 |
| `check.해당없음` | 해당없음 | checkbox | 100% | 해당없음 |
| `check.사본을휴대전화PC클라우드` | 사본(사진,파일등)을휴대전화,PC,클라우드 | checkbox | 100% | 예 |
| `check.있었습니까` | 있었습니까? | checkbox | 100% | 기타( |
| `check.계좌용비밀번호를휴대전화PC클라우드` | 계좌용비밀번호를휴대전화,PC,클라우드 | checkbox | 100% | 아니오 |
| `check.있었습니까2` | 있었습니까? | checkbox | 100% | 기타( |
| `check.방식이설정되어있었습니까` | 방식*이설정되어있었습니까? | checkbox | 100% | 예 |
| `check.지문얼굴인식등` | 지문/얼굴인식등 | checkbox | 100% | 기타( |
| `등에저장하여보관하고있었습니까` | 등에저장하여보관하고있었습니까? | text | 100% |  |
| `등에저장하고있었습니까` | 등에저장(메모)하고있었습니까? | text | 100% |  |
| `행번` | 행번 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer2` | 신청인 | seal | 100% | 현예지 |
| `sign.signer2` | 신청인 | signature | 100% | 박찬연 |
| `signer3.name` | 직원명 | text | 100% | 박찬연 |
| `seal.signer3` | 직원명 | seal | 100% | 강순준 |
| `sign.signer3` | 직원명 | signature | 100% | 이욱유 |
| `전자금융거래사고발생경위및사유` | 전자금융거래사고발생경위및사유 | text | 100% | 결혼자금 |
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `신용거래정보2` | ■신용거래정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer4.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer4` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer4` | 본인성명 | signature | 100% | 강순준 |
| `signer5.name` | 대리인성명 | text | 100% | 김나우 |
| `seal.signer5` | 대리인성명 | seal | 100% | 김나우 |
| `sign.signer5` | 대리인성명 | signature | 100% | 하숙인 |
| `신분증사본` | 신분증사본 | text | 100% |  |
| `seal.signer6` | 본인서명사실확인서 | seal | 100% | 박찬연 |
| `sign.signer6` | 본인서명사실확인서 | signature | 100% | 강순준 |
| `목록[].출입국사실증명원또는여권사본` | 출입국사실증명원또는여권사본 | text | 100% |  |
| `수사기관의결정문내지는처분서` | 수사기관의결정문내지는처분서 | text | 100% |  |
| `시간이상지연` | 시간이상지연 | text | 100% |  |
| `연계여부등포함` | 연계여부등)포함 | text | 100% |  |
| `customer.name2` | 성명 | text | 100% | 박찬연 |
| `company.name2` | 법인명 | text | 100% | (주)유니온무역 |
| `customer.phone2` | 전화번호 | phone | 100% | 010-7321-8870 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `agent.name` | 성명 | text | 100% | 박영준 |
| `agent.phone` | 전화번호 | phone | 100% | 010-6515-4769 |
| `agent.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `지점명` | 지점명 | text | 100% | 범어지점 |
| `행번2` | 행번 | text | 100% |  |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer7.name` | 위임자(본인) | text | 100% | 박찬연 |
| `seal.signer7` | 위임자(본인) | seal | 100% | 박찬연 |
| `sign.signer7` | 위임자(본인) | signature | 100% | 강순준 |
| `signer8.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer8` | 성명 | seal | 100% | 강순준 |
| `sign.signer8` | 성명 | signature | 100% | 박찬연 |

### [필수] 개인(신용)정보 제3자 제공 동의서 (하나원큐 공모주 정보제공 제휴서비스용) (`hf432`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `엠엘투자자문` | -엠엘투자자문(주) | text | 100% |  |
| `회원탈회시까지보유이용` | -회원탈회시까지보유·이용 | text | 100% |  |
| `일반개인정보` | ■일반개인정보 | text | 100% |  |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 현예지 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 최우빈 |
| `seal.signer2` | 대리인성명 | seal | 100% | 최우빈 |
| `sign.signer2` | 대리인성명 | signature | 100% | 박형민 |

### 추심지급 신청서 (`hf433`) — 키 19개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `접수점` | 접수점 | text | 100% |  |
| `signer.name` | 본인및서류확인 | text | 100% | 박찬연 |
| `seal.signer` | 본인및서류확인 | seal | 100% | 박찬연 |
| `sign.signer` | 본인및서류확인 | signature | 100% | 강순준 |
| `법원명` | 법원명 | text | 100% |  |
| `채권자` | 채권자 | text | 100% |  |
| `check.최소추심요청금액` | 최소추심요청금액 | checkbox | 100% | 기타 (수수료 제외 후 |
| `사건번호` | 사건번호 | text | 100% | 406-026825-33318 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `customer.email` | E-mail | text | 100% | chanyeon363@naver.com |
| `agent.name` | 성명 | text | 100% | 박영준 |
| `agent.birth` | 생년월일 | date | 100% | 1962년 12월 19일 |
| `agent.phone` | 연락처 | phone | 100% | 010-6515-4769 |
| `agent.relation` | 본인과의관계 | text | 100% | 부 |
| `customer.name` | 위임인 | text | 100% | 박찬연 |
| `은행계좌번호` | 은행▣계좌번호 | text | 100% | 107-666166-25262 |
| `예금주명` | ▣예금주명 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `본인및서류확인` | 본인및서류확인 | text | 100% |  |

### 세종특별자치시 지역개발채권 매입 신청서 (`hf434`) — 키 39개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `채권매입금액` | 채권매입금액 | number | 100% | 270,000 |
| `성명법인명` | 성명/법인명 | text | 100% | (주)유니온무역 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `agent.name` | 대리인(성명) | text | 100% | 박영준 |
| `customer.rrn` | 주민등록번호(사업자등록번호) | rrn | 100% | 900210-1659382 |
| `customer.rrn2` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `징구기관` | 징구기관 | text | 100% |  |
| `customer.phone2` | 연락처 | phone | 100% | 010-5907-7253 |
| `check.즉시매도시` | 즉시매도시 | checkbox | 100% | 보기1 |
| `check.만기시하나은행본인계좌로원리금자동상환` | 만기시하나은행본인계좌로원리금자동상환 | checkbox | 100% | 하나은행 계좌번호 ( |
| `check.만기시증권회사본인계좌로원리금자동상환` | 만기시증권회사본인계좌로원리금자동상환 | checkbox | 100% | 하나금융투자 계좌번호 ( |
| `check.만기시직접내점하여원리금상환` | 만기시직접내점하여원리금상환 | checkbox | 100% | 보기1 |
| `check.자동차신규등록` | 자동차신규등록(1) | checkbox | 100% | 각종 계약체결(7) |
| `증서번호` | 증서번호 | text | 100% | 마바83135935 |
| `매출일자` | 매출일자 | date | 100% | 2025년 1월 2일 |
| `매출점` | 매출점 | number | 100% | 2,990,000 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `수납금액` | 수납금액 | number | 100% | 9,430,000원 |
| `소득세` | 소득세 | number | 100% | 93,690,000 |
| `법인세` | 법인세 | text | 100% |  |
| `지방소득세` | 지방소득세 | number | 100% | 60,000 |
| `농특세` | 농특세 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 이욱유 |
| `sign.signer` | 신청인 | signature | 100% | 강순준 |
| `signer2.name` | (대리인 | text | 100% | 현예지 |
| `seal.signer2` | (대리인 | seal | 100% | 김나우 |
| `sign.signer2` | (대리인 | signature | 100% |  |
| `위탁` | 위탁 | text | 100% |  |
| `check.개인정보수집및이용내역` | 개인정보수집및이용내역 | checkbox | 100% | 개인정보 수집 및 이용 내역 |
| `check.동의함` | 동의함 | checkbox | 100% | 동의하지 않음 |
| `check.개인정보3자제공내역` | 개인정보3자제공내역 | checkbox | 100% | 개인정보 3자 제공 내역 |
| `check.동의함2` | 동의함 | checkbox | 100% | 동의하지 않음 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer3.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer3` | 성명 | seal | 100% | 최우빈 |
| `sign.signer3` | 성명 | signature | 100% | 박찬연 |

### 대전광역시 지역개발채권 매입 신청서 (`hf435`) — 키 39개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `채권매입금액` | 채권매입금액 | number | 100% | 50,850,000 |
| `성명법인명` | 성명/법인명 | text | 100% | (주)유니온무역 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `agent.name` | 대리인(성명) | text | 100% | 박영준 |
| `customer.rrn` | 주민등록번호(사업자등록번호) | rrn | 100% | 900210-1****** |
| `customer.rrn2` | 주민등록번호 | rrn | 100% | 900210-1****** |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `징구기관` | 징구기관 | text | 100% |  |
| `customer.phone2` | 연락처 | phone | 100% | 010-7321-8870 |
| `check.즉시매도시` | 즉시매도시 | checkbox | 100% | 보기1 |
| `check.만기시하나은행본인계좌로원리금자동상환` | 만기시하나은행본인계좌로원리금자동상환 | checkbox | 100% | 하나은행 계좌번호 ( |
| `check.만기시증권회사본인계좌로원리금자동상환` | 만기시증권회사본인계좌로원리금자동상환 | checkbox | 100% | 하나금융투자 계좌번호 ( |
| `check.만기시직접내점하여원리금상환` | 만기시직접내점하여원리금상환 | checkbox | 100% | 보기1 |
| `check.자동차신규등록` | 자동차신규등록(1) | checkbox | 100% | 각종 계약체결(7) |
| `증서번호` | 증서번호 | text | 100% | 아마13516284 |
| `매출일자` | 매출일자 | date | 100% | 2025년 4월 30일 |
| `매출점` | 매출점 | number | 100% | 7,470,000원 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `수납금액` | 수납금액 | number | 100% | 9,340,000 |
| `소득세` | 소득세 | number | 100% | 225,560,000 |
| `법인세` | 법인세 | text | 100% |  |
| `지방소득세` | 지방소득세 | number | 100% | 22,940,000 |
| `농특세` | 농특세 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 이욱유 |
| `sign.signer` | 신청인 | signature | 100% | 강순준 |
| `signer2.name` | (대리인 | text | 100% | 현예지 |
| `seal.signer2` | (대리인 | seal | 100% | 현예지 |
| `sign.signer2` | (대리인 | signature | 100% | 김나우 |
| `위탁` | 위탁 | text | 100% |  |
| `check.개인정보수집및이용내역` | 개인정보수집및이용내역 | checkbox | 100% | 개인정보 수집 및 이용 내역 |
| `check.동의함` | 동의함 | checkbox | 100% | 동의하지 않음 |
| `check.개인정보3자제공내역` | 개인정보3자제공내역 | checkbox | 100% | 개인정보 3자 제공 내역 |
| `check.동의함2` | 동의함 | checkbox | 100% | 동의함 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer3.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer3` | 성명 | seal | 100% | 강순준 |
| `sign.signer3` | 성명 | signature | 100% | 박찬연 |

### 주주명부(법인 비대면 실명확인 서비스 용) (`hf436`) — 키 9개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].주주명` | 주주명 | text | 100% | 박찬연 |
| `목록[].생년월일` | 생년월일(YYYY-MM-DD) | date | 100% | 2025.01.21 |
| `목록[].주식의종류` | 주식의종류(보통주등) | text | 100% |  |
| `목록[].지분율` | 지분율(%) | number | 100% | 10 |
| `목록[].주식수` | 주식수(주) | text | 100% |  |
| `목록[].주당액면가액` | 주당액면가액(원) | text | 100% | 36,550,000 |
| `목록[].자본금액` | 자본금액(원) | text | 100% | 3,250,000원 |
| `목록[].국적` | 국적 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 고객정보 활용 동의서(매출채권보험_모집대행업무용) (`hf437`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `매출채권보험추천등모집대행업무수행` | ▪매출채권보험추천등모집대행업무수행 | number | 100% | 18,570,000 |
| `필수사항` | 필수사항 | text | 100% |  |
| `필수사항2` | 필수사항 | text | 100% |  |
| `company.name` | 업체명 | text | 100% | (주)유니온무역 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `signer.name` | 대표자 | text | 100% | 박찬연 |
| `seal.signer` | 대표자 | seal | 100% | 이민빈 |
| `sign.signer` | 대표자 | signature | 100% | 강순준 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `signer2.name` | 본인확인 | text | 100% | 박찬연 |
| `seal.signer2` | 본인확인 | seal | 100% | 박찬연 |
| `sign.signer2` | 본인확인 | signature | 100% | 이욱유 |
| `customer.phone2` | 연락처(전화번호,핸드폰,E-mail) | phone | 100% | 010-5907-7253 |

### 매출채권보험 상담 신청서(신청기업용) (`hf438`) — 키 32개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업체명 | text | 100% | (주)유니온무역 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 120111-4500915 |
| `company.address` | 사업장주소 | text | 100% | 서울특별시 노원구 한글비석로 388-7, 8층 13호 |
| `당기매출액` | 당기매출액(최근1년매출액) | number | 100% | 77,630,000원 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 261-82-53694 |
| `업종업종분류코드` | 업종/업종분류코드 | number | 100% | 563576 |
| `company.established` | 설립일 | date | 100% | 2018.11.01 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `customer.email` | E-mail | text | 100% | chanyeon363@naver.com |
| `품목` | 품목 | text | 100% | 화장품 |
| `년` | 년 | number | 100% | 12 |
| `년2` | 년 | text | 100% |  |
| `년3` | 년 | text | 100% |  |
| `월` | 월 | text | 100% |  |
| `월2` | 월 | text | 100% |  |
| `일` | 일 | text | 100% |  |
| `일2` | 일 | text | 100% |  |
| `신청기업담당자` | 신청기업담당자 | text | 100% | 최민하 |
| `employer.position` | 직위 | text | 100% | 대리 |
| `customer.phone2` | 연락처 | phone | 100% | 010-5907-7253 |
| `company.name2` | 기업체명 | text | 100% | (주)유니온무역 |
| `company.biz_no2` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `company.corp_no2` | 법인등록번호 | rrn | 100% | 120111-4500915 |
| `signer.name` | 대표자명 | text | 100% | 박찬연 |
| `seal.signer` | 대표자명 | seal | 100% | 박찬연 |
| `sign.signer` | 대표자명 | signature | 100% | 현예지 |
| `signer2.name` | 본인확인 | text | 100% | 박찬연 |
| `seal.signer2` | 본인확인 | seal | 100% | 이민빈 |
| `sign.signer2` | 본인확인 | signature | 100% | 강순준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `신용보험센터` | 신용보험센터 | text | 100% |  |

### 상조회사 선수금 예치확인서 (`hf439`) — 키 9개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `상조회사명` | 상조회사명 | text | 100% | 청솔상사(주) |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.biz_no` | 사업자번호 | biz_no | 100% | 264-82-36559 |
| `목록[].예금과목` | 예금과목 | text | 100% | 하나 단기채 펀드 |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 114-369150-90757 |
| `목록[].금액` | 금액 | text | 100% | 259,470,000원 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer` | 지점장 | seal | 100% | 박찬연 |
| `sign.signer` | 지점장 | signature | 100% | 위나아 |

### 금융사고예방을 위한 문자통지(SMS) 서비스 신청서 (`hf440`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.phone` | 핸드폰번호 | phone | 100% | 010-7321-8870 |
| `signer.name` | 고객명 | text | 100% | 박찬연 |
| `seal.signer` | 고객명 | seal | 100% | 박찬연 |
| `sign.signer` | 고객명 | signature | 100% | 강순준 |
| `요구불예금` | 요구불예금(금액제한없음) | text | 100% |  |
| `중도해지금액제한없음` | 중도해지:금액제한없음 | number | 100% | 350,000원 |
| `건당1억원이상` | 건당1억원이상 | text | 100% |  |
| `통장재발급` | 통장재발급 | text | 100% |  |
| `계좌비밀번호변경` | 계좌비밀번호변경 | text | 100% | 087-733258-91455 |
| `현금IC카드재발급` | 현금IC카드재발급 | text | 100% |  |
| `통장MS훼손재기록` | 통장M/S훼손재기록 | text | 100% |  |
| `customer.phone2` | 휴대폰번호(변경전/후번호로통지) | phone | 100% | 010-5907-7253 |

### 법원보관금 납부서(은행제출용) (`hf441`) — 키 42개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `법원명` | 법원명 | text | 100% |  |
| `납부금액` | 납부금액 | number | 100% | 5,110,000원 |
| `납부자성명` | 납부자성명 | text | 100% | 박동율 |
| `납부자주소` | 납부자주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `잔액환급계좌번호` | 잔액환급계좌번호 | number | 100% | 40,100,000원 |
| `은행` | 은행 | text | 100% | 신한은행 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `사건번호` | 사건번호 | text | 100% | 8341-5958 |
| `보관금종류` | 보관금종류 | text | 100% |  |
| `customer.rrn` | 주민등록번호(사업자등록번호) | rrn | 100% | 900210-1659382 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `customer.name` | 예금주 | text | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 납부당사자 | text | 100% | 박찬연 |
| `seal.signer` | 납부당사자 | seal | 100% | 이욱유 |
| `sign.signer` | 납부당사자 | signature | 100% | 박찬연 |
| `법원명2` | 법원명 | text | 100% |  |
| `납부금액2` | 납부금액 | number | 100% | 1,390,000 |
| `납부자성명2` | 납부자성명 | text | 100% | 박찬연 |
| `납부자주소2` | 납부자주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `잔액환급계좌번호2` | 잔액환급계좌번호 | number | 100% | 490,000원 |
| `은행2` | 은행 | text | 100% | 농협은행 |
| `account2` | 계좌번호 | account_no | 100% | 774-646914-96117 |
| `사건번호2` | 사건번호 | text | 100% | 7683-3678 |
| `보관금종류2` | 보관금종류 | text | 100% |  |
| `customer.rrn2` | 주민등록번호(사업자등록번호) | rrn | 100% | 970514-2****** |
| `customer.phone2` | 전화번호 | phone | 100% | 010-5907-7253 |
| `customer.name2` | 예금주 | text | 100% | 박찬연 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `법원명3` | 법원명 | text | 100% |  |
| `납부금액3` | 납부금액 | number | 100% | 640,000 |
| `납부자성명3` | 납부자성명 | text | 100% | 박찬연 |
| `납부자주소3` | 납부자주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `잔액환급계좌번호3` | 잔액환급계좌번호 | number | 100% | 4,230,000 |
| `은행3` | 은행 | text | 100% | 기업은행 |
| `account3` | 계좌번호 | account_no | 100% | 774-646914-96117 |
| `사건번호3` | 사건번호 | text | 100% | 678-403775-06876 |
| `보관금종류3` | 보관금종류 | text | 100% |  |
| `customer.rrn3` | 주민등록번호(사업자등록번호) | rrn | 100% | 900210-1659382 |
| `customer.phone3` | 전화번호 | phone | 100% | 010-5907-7253 |
| `customer.name3` | 예금주 | text | 100% | 박찬연 |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |

### 대출상담 및 신청서(한국주택금융공사채권유동화목적 보금자리론용) (`hf047`) — 키 100개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신청금액` | 신청금액 | number | 100% | 710,000 |
| `check.자금용도` | 자금용도 | checkbox | 100% | 구입 |
| `check.주택보유수` | 주택보유수(본건담보주택제외) | checkbox | 100% | 주택(처분 예정) |
| `check.담보제공자` | 담보제공자 | checkbox | 100% | 본인 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.rrn` | 주민번호앞6자리 | number | 100% | 900210 |
| `check.결혼여부` | 결혼여부 | checkbox | 100% | 기혼 |
| `employer.name` | 직장명 | text | 100% | 주식회사 태평양무역 |
| `부서직위` | 부서/직위 | text | 100% |  |
| `check.직업구분` | 직업구분 | checkbox | 100% | 기타( |
| `근무기간` | 근무기간(업력) | number | 100% | 6 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `소득` | 소득(합계) | number | 100% | 81,390,000 |
| `부채` | 부채(합계) | number | 100% | 6,180,000 |
| `금융기관` | 금융기관 | text | 100% | 하나은행 |
| `금융기관2` | 금융기관 | text | 100% | 국민은행 |
| `customer.name2` | 성명 | text | 100% | 박찬연 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.rrn2` | 주민번호앞6자리 | number | 100% | 900210 |
| `employer.name2` | 직장명 | text | 100% | 주식회사 태평양무역 |
| `부서직위2` | 부서/직위 | text | 100% |  |
| `check.직업구분2` | 직업구분 | checkbox | 100% | 사업소득자 |
| `근무기간2` | 근무기간(업력) | number | 100% | 36 |
| `customer.phone2` | 전화번호 | phone | 100% | 010-5907-7253 |
| `소득2` | 소득(합계) | number | 100% | 530,000 |
| `부채2` | 부채(합계) | number | 100% | 2,350,000원 |
| `금융기관3` | 금융기관 | text | 100% | 국민은행 |
| `금융기관4` | 금융기관 | text | 100% | 농협은행 |
| `check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까` | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 100% | 안내 받음 (구두, 우편, 이메일, 팩스, 직접 수령) |
| `check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2` | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 100% | 원하지 않음 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인(본인) | text | 100% | 박찬연 |
| `seal.signer` | 신청인(본인) | seal | 100% | 박찬연 |
| `sign.signer` | 신청인(본인) | signature | 100% | 현예지 |
| `signer2.name` | 상담자확인 | text | 100% | 박찬연 |
| `seal.signer2` | 상담자확인 | seal | 100% | 이욱유 |
| `sign.signer2` | 상담자확인 | signature | 100% | 박찬연 |
| `계약기간` | 계약기간 | text | 100% |  |
| `자택` | 자택 | text | 100% |  |
| `customer.phone3` | 핸드폰 | phone | 100% | 010-5907-7253 |
| `대출금액` | 대출금액 | number | 100% | 23,390,000 |
| `대출금액2` | 대출금액 | number | 100% | 80,970,000 |
| `자택2` | 자택 | text | 100% |  |
| `customer.phone4` | 핸드폰 | phone | 100% | 010-5907-7253 |
| `대출금액3` | 대출금액 | number | 100% | 72,530,000 |
| `대출금액4` | 대출금액 | number | 100% | 270,000 |
| `customer.name3` | 성명 | text | 100% | 박찬연 |
| `customer.address3` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `employer.name3` | 직장명 | text | 100% | 주식회사 태평양무역 |
| `check.상담희망전화` | 상담희망전화 | checkbox | 100% | 휴대폰 |
| `customer.phone5` | 전화번호 | phone | 100% | 010-5907-7253 |
| `check.주택보유수2` | 주택보유수(본건담보주택제외) | checkbox | 100% | 무주택 |
| `대출신청금액` | 대출신청금액 | number | 100% | 8,800,000 |
| `check.대출만기` | 대출만기 | checkbox | 100% | 년 / |
| `희망취급기관` | 희망취급기관 | text | 100% |  |
| `대출희망일` | 대출희망일 | date | 100% | 2025년 1월 28일 |
| `거치기간` | 거치기간 | text | 100% |  |
| `소유권이전등기일` | 소유권이전등기일 | date | 100% | 2027.11.14 |
| `담보주택소재지` | 담보주택소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `check.주택유형` | 주택유형 | checkbox | 100% | 오피스텔 |
| `check.소유자` | 소유(예정)자 | checkbox | 100% | 본인 |
| `check.담보제공자2` | 담보제공자 | checkbox | 100% | 배우자 |
| `check.본건설정순위` | 본건설정순위 | checkbox | 100% | 순위 |
| `임대계약건수` | 임대계약건수 | number | 100% | 60 |
| `임대보증금합계액` | 임대보증금합계액 | number | 100% | 460,000 |
| `check.전용면적` | 전용면적 | checkbox | 100% | m2초과 |
| `check.규제지역해당` | 규제지역해당 | checkbox | 100% | 예 |
| `check.소득증명` | 소득증명 | checkbox | 100% | 배우자 |
| `본인부채` | 본인부채 | text | 100% |  |
| `제외부채` | 제외부채 | text | 100% |  |
| `02p` | 0.2%p | text | 100% |  |
| `customer.rrn3` | 주민번호앞6자리 | number | 100% | 900210 |
| `check.결혼여부2` | 결혼여부 | checkbox | 100% | 미혼 |
| `check.배우자세대분리` | 배우자세대분리 | checkbox | 100% | 아니오 |
| `배우자성명` | 배우자성명 | text | 100% | 박찬연 |
| `배우자주민번호앞6자리` | 배우자주민번호앞6자리 | text | 100% | 072-043732-82816 |
| `check.상환방식` | 상환방식 | checkbox | 100% | 원금균등 |
| `희망취급지점` | 희망취급지점 | text | 100% | 범어지점 |
| `변동금리기간` | 변동금리기간 | number | 100% | 6.16 |
| `check.자금용도2` | 자금용도 | checkbox | 100% | 상환 |
| `check.최저층여부` | 최저층여부 | checkbox | 100% | 예 |
| `check.선순위종류` | 선순위종류 | checkbox | 100% | 나라사랑대출 |
| `선순위설정금액` | 선순위설정금액 | number | 100% | 7,500,000 |
| `총방수` | 총방수 | text | 100% |  |
| `임대방수` | 임대방수 | text | 100% |  |
| `check.건물등기부등본` | 건물등기부등본 | checkbox | 100% | 있음 |
| `check.녹색건축물여부` | 녹색건축물여부 | checkbox | 100% | 아니오 |
| `배우자부채` | 배우자부채 | text | 100% |  |
| `제외대출` | 제외대출 | text | 100% |  |
| `종류` | 종류 | text | 100% | 하나 TDF 2040 |
| `employer.name4` | 소속 | text | 100% | 주식회사 태평양무역 |
| `발급기관` | 발급기관 | text | 100% |  |
| `발급일자` | 발급일자 | date | 100% | 2025.09.07 |
| `customer.name4` | 성명 | text | 100% | 박찬연 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer3.name` | 신청인(본인) | text | 100% | 박찬연 |
| `seal.signer3` | 신청인(본인) | seal | 100% | 현예지 |
| `sign.signer3` | 신청인(본인) | signature | 100% | 박찬연 |
| `협회코드` | 협회코드(대출상담사) | number | 100% | 32952 |

### 가계형소호 여신차입신청서 (`hf048`) — 키 65개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.신청구분` | 신청구분 | checkbox | 100% | 대환(재약정) |
| `check.신청인구분` | 신청인구분 | checkbox | 100% | 담보제공자 |
| `check.여신신청인의` | 여신신청인()의 | checkbox | 100% | 동료 |
| `고객번호` | 고객번호 | text | 100% | 296-021235-19158 |
| `check.우편물수령처` | 우편물수령처 | checkbox | 100% | 사업장 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.address` | 자택주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.address` | 사업장주소 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `customer.email` | E-mail | text | 100% | soonjun606@gmail.com |
| `check.직업군` | 직업군 | checkbox | 100% | 전문직 |
| `company.name` | 업체명(상호) | text | 100% | (주)유니온무역 |
| `check.매출정보` | 매출(소득)정보 | checkbox | 100% | 세무서신고 |
| `check.사업장소유여부` | 사업장소유여부 | checkbox | 100% | 아니오 |
| `월임차료` | 월임차료 | number | 100% | 26,480,000 |
| `check.자가` | 자가( | checkbox | 100% | 본인 |
| `check.주거형태코드` | 주거형태코드 | checkbox | 100% | 아파트 |
| `check.부채현황취급예정포함` | 부채현황(단위:백만원)【취급예정포함】 | checkbox | 100% | 자금용도( |
| `종류` | 종류 | text | 100% | 하나 적금 |
| `평가금액` | 평가금액 | number | 100% | 6,480,000 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `월관리비` | 월관리비 | number | 100% | 330,000 |
| `면적` | 면적 | text | 100% |  |
| `customer.birth` | 생년월일 | date | 100% | 900210 |
| `customer.home_phone` | 자택전화번호 | phone | 100% | 02-8556-8366 |
| `사업장전화번호` | 사업장전화번호 | phone | 100% | 010-5907-7253 |
| `check.국적` | 국적 | checkbox | 100% | 기타 ( |
| `company.biz_item` | 업종(주요제품) | text | 100% | 무역 |
| `연매출` | 연매출(연소득) | number | 100% | 8,780,000 |
| `임차보증금` | 임차보증금 | number | 100% | 8,570,000 |
| `company.address2` | 소재지 | text | 100% | 서울특별시 노원구 한글비석로 388-7, 8층 13호 |
| `check.공동대표여부` | 공동대표여부 | checkbox | 100% | 예 |
| `종업원수` | 종업원수 | number | 100% | 1 |
| `check.담보종류` | 담보종류 | checkbox | 100% | 대지 |
| `check.임대차확인` | 임대차확인 | checkbox | 100% | 있음(임대보증금 백만원) |
| `소유자명` | 소유자명 | text | 100% |  |
| `신청금액` | 신청금액 | number | 100% | 34,210,000 |
| `check.상환방법` | 상환방법 | checkbox | 100% | 만기일시 |
| `check.자금용도` | 자금용도 | checkbox | 100% | 기타( |
| `date` | 대출희망일 | date | 100% | 2026년 1월 31일 |
| `대출과목` | 대출과목 | text | 100% | 일반자금대출 |
| `check.거래구분` | 거래구분 | checkbox | 100% | 건별 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 여신신청인(본인) | text | 100% | 박찬연 |
| `seal.signer` | 여신신청인(본인) | seal | 100% | 현예지 |
| `sign.signer` | 여신신청인(본인) | signature | 100% | 박찬연 |
| `signer2.name` | 담보제공자(또는연대보증인또는공동사업자) | text | 100% | 박찬연 |
| `seal.signer2` | 담보제공자(또는연대보증인또는공동사업자) | seal | 100% | 박찬연 |
| `sign.signer2` | 담보제공자(또는연대보증인또는공동사업자) | signature | 100% | 김소윤 |
| `check.신규증액처리시안내` | 신규,증액처리시안내 | checkbox | 100% | 원치않음 |
| `check.동의함` | 동의함( | checkbox | 100% | 이메일 |
| `check.중도상환해약금면제시점도래안내문자통지` | 중도상환해약금면제시점도래안내문자통지 | checkbox | 100% | 원치않음 |
| `check.우편` | 우편 | checkbox | 100% | 직장 |
| `check.문자` | 문자 | checkbox | 100% | 원치않음 |
| `check.이메일` | 이메일 | checkbox | 100% | 동의함 |
| `대출금입금계좌` | 대출금입금(실행)계좌 | text | 100% | 426-738031-21264 |
| `check.예금담보등상계후잔액반환계좌번호` | 예금담보등상계후잔액반환계좌번호(담보제공자기준) | checkbox | 100% | 자동이체 결제 계좌 |
| `원금및이자자동이체결제계좌` | 원(리)금및이자자동이체결제계좌 | number | 100% | 50,980,000원 |
| `seal.signer3` | 신청인:____________________________ | seal | 100% | 박찬연 |
| `sign.signer3` | 신청인:____________________________ | signature | 100% | 현예지 |
| `설정순위` | •설정순위(설정일자) | text | 100% |  |
| `signer4.name` | •접수번호(등기부등본을구기준) | text | 100% | 박찬연 |
| `seal.signer4` | •접수번호(등기부등본을구기준) | seal | 100% | 박찬연 |
| `sign.signer4` | •접수번호(등기부등본을구기준) | signature | 100% | 이민빈 |
| `중도상환해약금면제시점도래안내문자통지` | 중도상환해약금면제시점도래안내문자통지 | text | 100% |  |
| `채권최고액` | •채권최고액 | number | 100% | 6,900,000원 |

### 《개인》대출신청서(가계용) (`hf049`) — 키 66개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.신청구분` | 신청구분 | checkbox | 100% | 채무인수 |
| `check.신청인구분` | 신청인구분 | checkbox | 100% | 연대보증인 |
| `check.대출신청인의` | 대출신청인()의 | checkbox | 100% | 친인척 |
| `고객번호` | 고객번호 | text | 100% | 362-609810-15116 |
| `check.우편물수령처` | 우편물수령처 | checkbox | 100% | 직장 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.address` | 자택주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `employer.address` | 직장주소 | text | 100% | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태… |
| `customer.email` | E-mail | text | 100% | chanyeon363@naver.com |
| `check.직업군` | 직업군 | checkbox | 100% | 급여소득자 |
| `employer.name` | 직장명 | text | 100% | 주식회사 태평양무역 |
| `근무부서` | 근무부서 | text | 100% |  |
| `입사년월` | 입사년월 | text | 100% |  |
| `check.자가` | 자가( | checkbox | 100% | 가족 |
| `check.주거형태코드` | 주거형태코드 | checkbox | 100% | 기타( |
| `check.부채현황취급예정포함` | 부채현황(단위:백만원)【취급예정포함】 | checkbox | 100% | 미상환 |
| `종류` | 종류 | text | 100% | 하나 적금 |
| `평가금액` | 평가금액 | number | 100% | 31,040,000 |
| `check.고용형태` | 고용형태 | checkbox | 100% | 정규직 |
| `employer.position` | 직위 | text | 100% | 대리 |
| `check.직무구분` | 직무구분 | checkbox | 100% | 자영업자 |
| `면적` | 면적 | text | 100% |  |
| `company.address` | 소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `check.연소득` | 연소득 | checkbox | 100% | 배우자( |
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.home_phone` | 자택전화번호 | phone | 100% | 02-5426-0645 |
| `employer.phone` | 직장전화번호 | phone | 100% | 033-364-7301 |
| `check.국적` | 국적 | checkbox | 100% | 대한민국 |
| `check.담보종류` | 담보종류 | checkbox | 100% | 상가 |
| `check.임대차확인` | 임대차확인 | checkbox | 100% | 없 |
| `소유자명` | 소유자명 | text | 100% |  |
| `check.결혼여부` | 결혼여부 | checkbox | 100% | 기혼 |
| `date` | 대출희망일 | date | 100% | 2026년 1월 31일 |
| `check.상환방법` | 상환방법 | checkbox | 100% | 기타( |
| `check.주택` | 주택( | checkbox | 100% | 구입 |
| `check.기타부동산` | 기타부동산( | checkbox | 100% | 임차 |
| `check.거래구분` | 거래구분 | checkbox | 100% | 한도 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 대출신청인(본인) | text | 100% | 박찬연 |
| `seal.signer` | 대출신청인(본인) | seal | 100% | 박찬연 |
| `sign.signer` | 대출신청인(본인) | signature | 100% | 현예지 |
| `signer2.name` | 담보제공자(또는연대보증인) | text | 100% | 박찬연 |
| `seal.signer2` | 담보제공자(또는연대보증인) | seal | 100% | 하숙인 |
| `sign.signer2` | 담보제공자(또는연대보증인) | signature | 100% | 박찬연 |
| `check.신규증액채무인수한도감액한도완제처리시안내` | 신규,증액,채무인수,한도감액,한도완제처리시안내 | checkbox | 100% | 문자 |
| `check.신청대출승인완료시안내문자통지` | 신청대출승인완료시안내문자통지 | checkbox | 100% | 원치않음 |
| `check.동의함` | 동의함( | checkbox | 100% | 문자 |
| `check.중도상환해약금면제시점도래안내문자통지` | 중도상환해약금면제시점도래안내문자통지 | checkbox | 100% | 동의함 |
| `check.우편` | 우편 | checkbox | 100% | 원치않음 |
| `check.문자` | 문자 | checkbox | 100% | 원치않음 |
| `check.이메일` | 이메일 | checkbox | 100% | 원치않음 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.name2` | 예금주 | text | 100% | 박찬연 |
| `check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까` | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 100% | 원치않음 |
| `check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2` | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 100% | 이메일 |
| `이관희망점` | 이관희망점 | text | 100% |  |
| `설정순위` | •설정순위(설정일자) | text | 100% |  |
| `접수번호` | •접수번호(등기부등본을구기준) | text | 100% | 860-824245-06741 |
| `signer3.name` | 담보제공 | text | 100% | 박찬연 |
| `seal.signer3` | 담보제공 | seal | 100% | 강순준 |
| `sign.signer3` | 담보제공 | signature | 100% | 박찬연 |
| `customer.name3` | 성명 | text | 100% | 박찬연 |
| `신청대출승인완료시안내문자통지` | 신청대출승인완료시안내문자통지 | text | 100% |  |
| `대출부수거래충족여부안내통지` | 대출부수거래충족여부안내통지(문자만) | text | 100% |  |
| `중도상환해약금면제시점도래안내문자통지` | 중도상환해약금면제시점도래안내문자통지 | text | 100% |  |
| `거절사유에대해안내를받으시겠습니까` | 거절사유에대해안내를받으시겠습니까? | text | 100% | 사업자금 |

### [필수]개인(신용)정보 제3자 제공 동의서(토지분양대금 대출 약정_대구도시개발공사) (`hf050`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `대구도시개발공사` | -대구도시개발공사 | text | 100% |  |
| `제공일로부터5년까지보유이용` | -제공일로부터5년까지보유·이용 | text | 100% |  |
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 이민빈 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 최우빈 |
| `seal.signer2` | 대리인성명 | seal | 100% | 최우빈 |
| `sign.signer2` | 대리인성명 | signature | 100% | 여기준 |

### 대출계약 철회신청서 (`hf051`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 차주 | text | 100% | 박찬연 |
| `상품명` | 상품명 | text | 100% | 전자부품 |
| `실행일` | 실행일 | date | 100% | 2025년 12월 13일 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `금액` | 금액 | number | 100% | 5,690,000원 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 강순준 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |
| `check.중도상환이나철회하지않고` | 중도상환이나철회하지않고대출유지함 | checkbox | 100% | 중도상환이나 철회하지 않고 대출 유지함 |
| `check.기타` | 기타( | checkbox | 100% | 기타 ( |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer2` | 신청인 | seal | 100% | 현예지 |
| `sign.signer2` | 신청인 | signature | 100% | 강순준 |

### [필수] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택전월세자금대출용) (`hf052`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `목록[].공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `부채금액` | ¶부채금액 | number | 100% | 260,310,000 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보제공에동의하십니까2` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `보유현황공공임대주택계약정보` | 보유현황,공공임대주택계약정보 | text | 100% |  |
| `업권등의공시가액` | 업권등의공시가액 | number | 100% | 31,180,000 |
| `제공받는자와동일` | -제공받는자와동일 | text | 100% |  |
| `check.위고유식별정보조회에동의하십니까` | 위고유식별정보조회에동의하십니까? | checkbox | 100% | 동의함 |
| `정보전월세거래정보` | 정보,전·월세거래정보 | text | 100% |  |
| `check.위개인정보조회에동의하십니까` | 위개인(신용)정보조회에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보조회에동의하십니까2` | 위개인(신용)정보조회에동의하십니까? | checkbox | 100% | 동의함 |
| `check.이용동의여부` | 이용동의여부 | checkbox | 100% | 보기1 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 이욱유 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `signer2.name` | 배우자성명 | text | 100% | 박찬연 |
| `seal.signer2` | 배우자성명 | seal | 100% | 현예지 |
| `sign.signer2` | 배우자성명 | signature | 100% | 박찬연 |

### [필수] 개인(신용)정보 수집·이용·제공 및 조회 동의서(주택도시기금 주택구입자금대출용) (`hf053`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `재지및면적유형가격임대차현황등` | 재지및면적,유형,가격,임대차현황등 | text | 100% |  |
| `목록[].공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `부채금액` | ¶부채금액 | number | 100% | 820,000원 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보제공에동의하십니까2` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `보유현황공공주택계약정보` | 보유현황,공공주택계약(입주)정보 | text | 100% |  |
| `권등의공시가액` | 권등의공시가액 | number | 100% | 1,820,000 |
| `제공받는자와동일` | -제공받는자와동일 | text | 100% |  |
| `check.위고유식별정보조회에동의하십니까` | 위고유식별정보조회에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보조회에동의하십니까` | 위개인(신용)정보조회에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보조회에동의하십니까2` | 위개인(신용)정보조회에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.이용동의여부` | 이용동의여부 | checkbox | 100% | 동의함 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 강순준 |
| `signer2.name` | 배우자성명 | text | 100% | 박찬연 |
| `seal.signer2` | 배우자성명 | seal | 100% | 현예지 |
| `sign.signer2` | 배우자성명 | signature | 100% | 김소윤 |

### 주택도시기금 대출 신청서(가계용) (`hf054`) — 키 81개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `주택가격` | 주택가격 | text | 100% |  |
| `순담보가액` | 순담보가액 | number | 100% | 33,100,000원 |
| `선순위설정액` | 선순위설정액 | text | 100% |  |
| `대출가능액` | 대출가능액 | text | 100% |  |
| `check.신청구분` | 신청구분 | checkbox | 100% | 대환(재약정) |
| `check.신청인구분` | 신청인구분 | checkbox | 100% | 연대보증인 |
| `check.대출신청인의` | 대출신청인()의 | checkbox | 100% | 가족 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `주민등록지` | 주민등록지 | text | 100% |  |
| `현거주지` | 현거주지 | text | 100% |  |
| `전세보증금` | 전세보증금 | number | 100% | 200,000원 |
| `이사예정지` | 이사예정지 | text | 100% |  |
| `전세보증금2` | 전세보증금 | number | 100% | 43,610,000원 |
| `employer.name` | 직장명 | text | 100% | 주식회사 태평양무역 |
| `employer.address` | 직장주소 | text | 100% | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태… |
| `배우자명` | 배우자명 | text | 100% |  |
| `다자녀가구다문화가구장애인가구` | ▢다자녀가구▢다문화가구▢장애인가구 | text | 100% |  |
| `원리금자동이체계좌번호` | 원리금자동이체계좌번호 | text | 100% | 101-353133-69816 |
| `대출신청금액` | 대출신청금액 | number | 100% | 44,010,000 |
| `대출과목` | 대출과목 | text | 100% | 주택담보대출 |
| `대출기간` | 대출기간 | text | 100% |  |
| `대출이율` | 대출이율 | number | 100% | 5.48 |
| `목록[].임차보증금` | 임차보증금 | number | 100% | 8,050,000 |
| `customer.name2` | 본인 | text | 100% | 박찬연 |
| `자기자금` | 자기자금 | number | 100% | 970,000원 |
| `방수` | 방수 | number | 100% | 1 |
| `목록[].소액보증금` | 소액보증금 | number | 100% | 450,000 |
| `customer.birth` | 생년월일 | date | 100% | 1990-02-10 |
| `employer.department` | 부서명 | text | 100% | 구매팀 |
| `월세보증금` | 월세보증금 | number | 100% | 22,100,000 |
| `월세보증금2` | 월세보증금 | number | 100% | 3,120,000 |
| `만기일시원리금균등분할원금균등분할` | ▢만기일시▢원리금균등분할▢원금균등분할 | date | 100% | 2029-02-22 |
| `소액보증금` | 소액보증금 | number | 100% | 212,870,000원 |
| `배우자` | 배우자 | number | 100% | 224,190,000 |
| `본건대출` | 본건대출(기금) | number | 100% | 6,010,000 |
| `배우자직장번호` | 배우자직장번호(핸드폰번호) | text | 100% | 086181-2647914 |
| `대출희망일` | 대출희망일 | date | 100% | 2026.01.22 |
| `목록[].금액` | 금액 | number | 100% | 2,810,000 |
| `customer.phone` | 휴대폰번호 | phone | 100% | 010-5907-7253 |
| `customer.email` | e-mail | text | 100% | chanyeon363@naver.com |
| `customer.phone2` | 전화번호 | phone | 100% | 010-5907-7253 |
| `employer.position` | 직위 | text | 100% | 대리 |
| `목록[].자금용도` | 자금용도 | text | 100% | 하나 TDF 2040 |
| `고객번호` | 고객번호 | text | 100% | 7210-5778 |
| `check.우편물수령처` | 우편물수령처 | checkbox | 100% | 자택 |
| `월임대료` | 월임대료 | number | 100% | 920,000 |
| `주거방수` | 주거방수 | number | 100% | 3 |
| `월임대료2` | 월임대료 | number | 100% | 89,490,000원 |
| `employer.phone` | 직장전화번호 | phone | 100% | 043-783-2775 |
| `가구총소득` | 가구총소득 | number | 100% | 380,000 |
| `기타조달` | 기타조달 | number | 100% | 7,200,000원 |
| `결혼일` | 결혼(예정)일 | date | 100% | 2025.01.11 |
| `employer.hire_date` | 입사일자 | date | 100% | 2020.05.08 |
| `목록[].담보종류` | 담보종류 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `분양가격` | ▢분양가격 | text | 100% |  |
| `customer.name3` | 신청인(본인) | text | 100% | 박찬연 |
| `customer.name4` | 차주 | text | 100% | 박찬연 |
| `의담보제공자` | 의담보제공자(또는연대보증인) | text | 100% |  |
| `신청대출승인완료시안내문자통지` | 신청대출승인완료시안내문자통지 | text | 100% |  |
| `check.신규증액채무인수한도감액한도완제처리시안내` | 신규,증액,채무인수,한도감액,한도완제처리시안내 | checkbox | 100% | 원치않음 |
| `check.신청대출승인완료시안내문자통지` | 신청대출승인완료시안내문자통지 | checkbox | 100% | 원치않음 |
| `check.동의함` | 동의함( | checkbox | 100% | 동의함( |
| `check.중도상환해약금면제시점도래안내문자통지` | 중도상환해약금면제시점도래안내문자통지 | checkbox | 100% | 원치않음 |
| `check.우편` | 우편 | checkbox | 100% | 원치않음 |
| `check.문자` | 문자 | checkbox | 100% | 원치않음 |
| `check.이메일` | 이메일 | checkbox | 100% | 원치않음 |
| `대출금입금계좌` | 대출금입금(실행)계좌 | text | 100% | 411-449461-07296 |
| `check.예금담보등상계후잔액반환계좌번호` | 예금담보등상계후잔액반환계좌번호(담보제공자기준) | checkbox | 100% | 별도 지정(은행명 |
| `check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까` | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 100% | 원치않음 |
| `check.대출신청이거절되는경우거절사유에대해안내를받으시겠습니까2` | 대출신청이거절되는경우,거절사유에대해안내를받으시겠습니까? | checkbox | 100% | 이메일 |
| `설정순위` | •설정순위(설정일자) | text | 100% |  |
| `접수번호` | •접수번호(등기부등본을구기준) | text | 100% | 022-981909-35670 |
| `signer.name` | (담보제공자기준) | text | 100% | 박찬연 |
| `seal.signer` | (담보제공자기준) | seal | 100% | 박찬연 |
| `sign.signer` | (담보제공자기준) | signature | 100% | 강순준 |
| `대출부수거래충족여부안내통지` | 대출부수거래충족여부안내통지(문자만) | text | 100% |  |
| `중도상환해약금면제시점도래안내문자통지` | 중도상환해약금면제시점도래안내문자통지 | text | 100% |  |
| `대출신청이거절되는경우` | 대출신청이거절되는경우, | text | 100% |  |
| `거절사유에대해안내를받으시겠습니까` | 거절사유에대해안내를받으시겠습니까? | text | 100% | 자녀 교육비 |
| `채권최고액` | •채권최고액 | text | 100% |  |

### 주택도시기금 대출상담 및 신청서(내집마련 디딤돌 대출용) (`hf055`) — 키 68개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.근저당권과관련된모든대출` | 근저당권과관련된모든대출금을상환하고말소를원하는경우영업점에방 | checkbox | 100% | 근저당권과 관련된 모든 대출금을 상환하고 말소를 원하는 경우 영업점에 방 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `주민등록지` | 주민등록지 | text | 100% |  |
| `현거주지` | 현거주지 | text | 100% |  |
| `check.주택유형` | 주택유형 | checkbox | 100% | 연립주택 |
| `전세보증금` | 전세보증금 | number | 100% | 570,000 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `check.소유자` | 소유자 | checkbox | 100% | 부부공동 |
| `check.주택유형2` | 주택유형 | checkbox | 100% | 단독주택(다가구 포함) |
| `임대방수` | 임대방수 | number | 100% | 1 |
| `employer.name` | 직장명 | text | 100% | 주식회사 태평양무역 |
| `check.직업` | 직업 | checkbox | 100% | 관리/사무 |
| `employer.address` | 직장주소 | text | 100% | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태… |
| `배우자성명` | 배우자성명 | text | 100% | 강순준 |
| `check.우편물배달장소` | 우편물배달장소 | checkbox | 100% | 직장 |
| `원리금자동이체계좌번호` | 원리금자동이체계좌번호 | text | 100% | 762-939327-57078 |
| `대출신청금액` | 대출신청금액 | number | 100% | 4,700,000 |
| `대출과목` | 대출과목 | text | 100% | 주택담보대출 |
| `check.대출기간` | 대출기간 | checkbox | 100% | 년 |
| `check.거치기간` | 거치기간 | checkbox | 100% | 비거치 |
| `check.상환방법` | 상환방법 | checkbox | 100% | 원리금균등분할 |
| `check.대출금리` | 대출금리 | checkbox | 100% | 년 단위 변동금리 연 |
| `check.우대금리` | 우대금리 | checkbox | 100% | 없음 |
| `check.대출가부` | 대출가부 | checkbox | 100% | 가 |
| `customer.name2` | 본인 | text | 100% | 박찬연 |
| `customer.name3` | 본인 | text | 100% | 박찬연 |
| `자기자금` | 자기자금 | number | 100% | 9,760,000 |
| `check.배우자` | 배우자 | checkbox | 100% | 무 |
| `방수` | 방수 | number | 100% | 2 |
| `월세보증금` | 월세보증금 | number | 100% | 7,610,000 |
| `방수2` | 방수 | number | 100% | 1 |
| `임대보증금` | 임대보증금 | number | 100% | 42,590,000 |
| `employer.department` | 부서명 | text | 100% | 구매팀 |
| `목록[].차입기관명` | 차입기관명 | text | 100% | 카카오뱅크 |
| `배우자` | 배우자 | number | 100% | 8,240,000 |
| `배우자2` | 배우자 | number | 100% | 9,230,000 |
| `본건대출` | 본건대출 | number | 100% | 7,500,000 |
| `목록[].금액` | 금액 | number | 100% | 58,530,000 |
| `customer.rrn` | 주민등록번호앞6자리 | number | 100% | 900210 |
| `customer.phone` | 휴대폰번호 | phone | 100% | 010-7321-8870 |
| `customer.phone2` | 전화번호 | phone | 100% | 010-5907-7253 |
| `check.주거형태` | 주거형태 | checkbox | 100% | 기타 |
| `월임대료` | 월임대료 | number | 100% | 430,000원 |
| `check.주택보유수` | 주택보유수 | checkbox | 100% | 본건 담보주택을 제외하고는 없음 |
| `선순위설정금액` | 선순위설정금액 | number | 100% | 450,000원 |
| `check.무상거주` | 무상거주 | checkbox | 100% | 무 |
| `employer.position` | 직위 | text | 100% | 대리 |
| `배우자주민등록번호앞6자리` | 배우자주민등록번호앞6자리 | text | 100% | 668-748827-23091 |
| `대출희망일` | 대출희망일 | date | 100% | 2025.02.06 |
| `check.본대출과관련된비용및수수료를무통장무인감으로인출함에동의` | 본대출과관련된비용및수수료를무통장,무인감으로인출함에동의 | checkbox | 100% | 동의함 |
| `상담자` | 상담자(직위/성명) | text | 100% |  |
| `목록[].자금용도` | 자금용도 | text | 100% | 하나 정기예금 |
| `employer.phone` | 직장전화번호 | phone | 100% | 043-783-2775 |
| `가구총소득` | 가구총소득 | number | 100% | 46,900,000 |
| `제외부채` | 제외부채 | number | 100% | 9,780,000 |
| `기타조달` | 기타조달 | number | 100% | 80,620,000 |
| `목록[].담보종류` | 담보종류 | text | 100% |  |
| `employer.hire_date` | 입사일자 | date | 100% | 2021.09.26 |
| `신청대출승인완료시안내문자통지` | 신청대출승인완료시안내문자통지 | text | 100% |  |
| `check.신규증액채무인수한도감액한도완제처리시안내` | 신규,증액,채무인수,한도감액,한도완제처리시안내 | checkbox | 100% | 원치않음 |
| `check.신청대출승인완료시안내문자통지` | 신청대출승인완료시안내문자통지 | checkbox | 100% | 원치않음 |
| `check.동의함` | 동의함( | checkbox | 100% | 이메일 |
| `check.중도상환해약금면제시점도래안내문자통지` | 중도상환해약금면제시점도래안내문자통지 | checkbox | 100% | 동의함 |
| `check.우편` | 우편 | checkbox | 100% | 자택 |
| `check.문자` | 문자 | checkbox | 100% | 동의함 |
| `check.이메일` | 이메일 | checkbox | 100% | 원치않음 |
| `대출부수거래충족여부안내통지` | 대출부수거래충족여부안내통지(문자만) | text | 100% |  |
| `중도상환해약금면제시점도래안내문자통지` | 중도상환해약금면제시점도래안내문자통지 | text | 100% |  |

### [필수] 개인(신용)정보 제3자 제공 동의서(하나더넥스트 내집연금용_역모기지) (`hf056`) — 키 5개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `제공항목` | 제공항목 | text | 100% |  |
| `하나생명` | 하나생명 | text | 100% |  |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 융자상담 및 차입신청서(기업용) (`hf058`) — 키 44개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.신청구분` | 신청구분 | checkbox | 100% | 채무인수 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 강순준 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |
| `company.address` | 사업장주소 | text | 100% | 서울특별시 노원구 한글비석로 388-7, 8층 13호 |
| `company.biz_no` | 사업자번호(생년월일) | biz_no | 100% | 264-82-36559 |
| `사업장전화번호` | 사업장전화번호 | phone | 100% | 010-5907-7253 |
| `대출과목` | 대출과목 | text | 100% | 시설자금대출 |
| `신청금액` | 신청금액 | number | 100% | 52,520,000원 |
| `check.대출기간만료일` | 대출기간만료일 | checkbox | 100% | 대출실행(한도약정)일로부터 |
| `거치기간` | 거치기간 | number | 100% | 2 |
| `check.상환방법` | 상환방법 | checkbox | 100% | 기타( |
| `check.자금용도` | 자금용도 | checkbox | 100% | 운영자금(급여, 원자재매입 등) |
| `check.거래구분` | 거래구분 | checkbox | 100% | 한도 |
| `check.금리적용방식` | 금리적용방식 | checkbox | 100% | 변동 |
| `부채현황_목록[].금융기관명` | 금융기관명 | text | 100% | 농협은행 |
| `company.address2` | 소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `종류` | 종류 | text | 100% | 하나 정기예금 |
| `employer.name` | 직장명(직위) | text | 100% | (주)케이소프트 |
| `부채현황_목록[].금액` | 금액 | text | 100% | 140,000원 |
| `수량` | 수량 | number | 100% | 24 |
| `차주와의관계` | 차주와의관계 | text | 100% |  |
| `부채현황_목록[].담보` | 담보 | text | 100% |  |
| `추정가액` | 추정가액 | number | 100% | 85,700,000 |
| `실재산` | 실재산 | text | 100% |  |
| `담보제공자` | 담보제공자 | text | 100% |  |
| `나이` | 나이 | text | 100% |  |
| `부채현황_목록[].자금용도` | 자금용도 | text | 100% | 하나 단기채 펀드 |
| `신청인과의관계` | 신청인과의관계 | text | 100% |  |
| `보증종류` | 보증종류 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `check.신규처리시안내` | 신규처리시안내 | checkbox | 100% | 문자 |
| `customer.phone` | 휴대폰번호 | phone | 100% | 010-7321-8870 |
| `customer.email` | E-mail | text | 100% | chanyeon363@naver.com |
| `check.동의함` | 동의함( | checkbox | 100% | 동의함 ( |
| `customer.phone2` | 휴대폰번호 | phone | 100% | 010-5907-7253 |
| `customer.email2` | E-mail | text | 100% | chanyeon363@naver.com |
| `check.확인서` | 확인서(담보제공자용) | checkbox | 100% | 해당 |
| `check.확인서2` | 확인서(담보제공자용) | checkbox | 100% | 미해당 |
| `대출금입금계좌` | 대출금입금(실행)계좌 | text | 100% | 295-702848-88938 |
| `원금및이자자동이체결제계좌` | 원(리)금및이자자동이체결제계좌 | number | 100% | 42,900,000 |
| `설정순위` | ●설정순위(설정일자) | text | 100% |  |
| `부동산담보대출접수번호` | 부동산담보대출●접수번호(등기부등본기준) | text | 100% | 782446-6734277 |

### 개인(신용)정보 조회 동의서 (`hf059`) — 키 23개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `거래와관련한개인정보조회` | (금융)거래와관련한개인(신용)정보조회 | text | 100% |  |
| `일반개인정보` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `국내거소신고번호성명주소전화번호` | 국내거소신고번호,성명,주소,전화번호 | phone | 100% | 010-5907-7253 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `이용목적` | 이용목적 | text | 100% | 전세자금 |
| `일반개인정보2` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `국내거소신고번호성명` | 국내거소신고번호,성명 | text | 100% | 482-617944-55681 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `제공받는자와동일` | 제공받는자와동일 | date | 100% | 2025.12.07 |
| `공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보조회에동의하십니까` | 위고유식별정보조회에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보조회에동의하십니까` | 위개인(신용)정보조회에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 현예지 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 강순준 |
| `seal.signer2` | 대리인성명 | seal | 100% | 이욱유 |
| `sign.signer2` | 대리인성명 | signature | 100% | 강순준 |
| `이용목적2` | 이용목적 | text | 100% | 의료비 |
| `재산채무소득의총액납세실적등` | 재산·채무·소득의총액,납세실적등 | number | 100% | 5,210,000 |

### [필수] 개인(신용)정보 수집이용 동의서(대출성상품 적합성적정성 판단용) (`hf060`) — 키 10개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 강순준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 현예지 |
| `seal.signer2` | 대리인성명 | seal | 100% | 현예지 |
| `sign.signer2` | 대리인성명 | signature | 100% | 옥영아 |

### 적합성, 적정성 고객정보 확인서(개인 및 개인사업자용) (`hf061`) — 키 23개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.email` | Email | text | 100% | soonjun606@gmail.com |
| `check.후견인여부` | 후견인여부 | checkbox | 100% | 피한정후견인 |
| `check.대출용도` | 대출용도 | checkbox | 100% | 경조자금 |
| `check.총자산규모` | 총자산규모(순자산) | checkbox | 100% | 자산없음 |
| `check.담보제공계획` | 담보제공계획 | checkbox | 100% | 없음 |
| `check.담보제공계획2` | 담보제공계획 | checkbox | 100% | 있음 |
| `check.소득없음` | 소득없음 | checkbox | 100% | 천만원 미만 |
| `check.부채` | 부채 | checkbox | 100% | 천만원 미만 |
| `check.연체여부` | 연체여부 | checkbox | 100% | 연체정보 없음 |
| `check.신용점수` | 신용점수 | checkbox | 100% | KCB |
| `check.근로소득` | 근로소득 | checkbox | 100% | 담보의 처분(매매, 경매등) |
| `customer.birth` | 생년월일 | date | 100% | 900210 |
| `기거래건전성` | 기거래건전성 | text | 100% |  |
| `신용상태` | 신용상태 | text | 100% |  |
| `상환능력및변제계획` | 상환능력및변제계획 | text | 100% |  |
| `진단결과번호` | 진단결과번호 | text | 100% | 415-601396-67052 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 최우빈 |
| `signer2.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer2` | 신청인 | seal | 100% | 이민빈 |
| `sign.signer2` | 신청인 | signature | 100% | 박찬연 |

### 적합성, 적정성 고객정보 확인서(법인용) (`hf062`) — 키 31개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 업체명 | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표자명 | text | 100% | 박찬연 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `대표자연락처` | 대표자연락처 | phone | 100% | 010-7321-8870 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `상시근로자수` | 상시근로자수 | text | 100% |  |
| `customer.email` | E-mail | text | 100% | soonjun606@gmail.com |
| `check.전문금융소비자여부` | 전문금융소비자여부 | checkbox | 100% | 주권을 국내외 증권시장에 상장한 법인 |
| `check.전문금융소비자여부2` | 전문금융소비자여부 | checkbox | 100% | 일반금융소비자 |
| `업력` | 업력 | number | 100% | 1 |
| `check.총자산규모` | 총자산규모(순자산) | checkbox | 100% | 억원 이상 |
| `check.주택증권지식재산권등의담보제공예정` | 주택,증권(주식,채권등),지식재산권등의담보제공예정 | checkbox | 100% | 있음 |
| `check.담보제공계획` | 담보제공계획 | checkbox | 100% | 없음 |
| `check.매출액` | 매출액 | checkbox | 100% | 억원 이상 |
| `check.순이익` | 순이익 | checkbox | 100% | 억원 이상 5억원 미만 |
| `check.부채` | 부채 | checkbox | 100% | 억원 이상 10억원 미만 |
| `check.연체여부` | 연체여부 | checkbox | 100% | 연체정보 있음 |
| `check.변제방법` | 변제방법 | checkbox | 100% | 사업소득 |
| `check.대출용도` | 대출용도 | checkbox | 100% | 시설자금 |
| `check.최근3년간연속자본잠식` | 최근3년간연속자본잠식 | checkbox | 100% | 비해당 |
| `기거래건전성` | 기거래건전성 | text | 100% |  |
| `신용상태` | 신용상태 | text | 100% |  |
| `상환능력및변제계획` | 상환능력및변제계획 | text | 100% |  |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 강순준 |
| `sign.signer` | 신청인 | signature | 100% | 위나아 |
| `signer2.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer2` | 신청인 | seal | 100% | 이민빈 |
| `sign.signer2` | 신청인 | signature | 100% | 박찬연 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `agent.relation` | 관계 | text | 100% | 부 |

### 대출정보 열람청구, 상환 및 말소접수 위임장(주택담보대출 대출이동서비스) (`hf064`) — 키 7개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.birth` | 생년월일 | date | 100% | 900210 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 위임인(본인) | text | 100% | 박찬연 |
| `seal.signer` | 위임인(본인) | seal | 100% | 이민빈 |
| `sign.signer` | 위임인(본인) | signature | 100% | 박찬연 |

### 국토교통부 주택소유확인 시스템 등 이용 관련 [필수] 개인(신용)정보 수집·이용·제공 동의서 (`hf065`) — 키 25개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `일반개인정보` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `일반개인정보2` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 최우빈 |
| `signer2.name` | 세대원성명 | text | 100% | 박찬연 |
| `seal.signer2` | 세대원성명 | seal | 100% | 현예지 |
| `sign.signer2` | 세대원성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer3.name` | 세대원성명 | text | 100% | 박찬연 |
| `seal.signer3` | 세대원성명 | seal | 100% | 박찬연 |
| `sign.signer3` | 세대원성명 | signature | 100% | 현예지 |
| `signer4.name` | 세대원성명 | text | 100% | 박찬연 |
| `seal.signer4` | 세대원성명 | seal | 100% | 이주원 |
| `sign.signer4` | 세대원성명 | signature | 100% | 박찬연 |
| `signer5.name` | 세대원성명 | text | 100% | 박찬연 |
| `seal.signer5` | 세대원성명 | seal | 100% | 현예지 |
| `sign.signer5` | 세대원성명 | signature | 100% | 박찬연 |
| `signer6.name` | 세대원성명 | text | 100% | 박찬연 |
| `seal.signer6` | 세대원성명 | seal | 100% | 박찬연 |
| `sign.signer6` | 세대원성명 | signature | 100% | 강순준 |

### 대출정보 열람청구 및 상환 위임장(대출이동서비스) (`hf066`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.birth` | 생년월일 | date | 100% | 900210 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 위임자(본인) | text | 100% | 박찬연 |
| `seal.signer` | 위임자(본인) | seal | 100% | 강순준 |
| `sign.signer` | 위임자(본인) | signature | 100% | 박찬연 |

### [필수] 개인(신용)정보 수집 · 이용 동의서[대출이동서비스] (`hf067`) — 키 10개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `customer.rrn` | 주민등록번호 | rrn | 100% | 970514-2150000 |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 현예지 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `ᄋ금융사고조사분쟁해결민원처리` | ᄋ금융사고조사,분쟁해결,민원처리 | text | 100% |  |
| `ᄋ법령상의무이행` | ᄋ법령상의무이행 | text | 100% |  |

### 계약 체결 이행 등을 위한 필수 동의서(개인금융성 신용보험용) (`hf068`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `대위변제시대위권행사` | -대위변제시대위권행사 | text | 100% |  |
| `인의관계등기타개인신용정보분리보관정보` | 인의관계등기타개인신용정보,분리보관정보 | text | 100% |  |
| `신용도판단정보` | ■신용도판단정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공*에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `공공정보등2` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보조회에동의하십니까` | 위고유식별정보조회에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인신용정보조회에동의하십니까` | 위개인신용정보조회에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인 | text | 100% | 박찬연 |
| `seal.signer` | 본인 | seal | 100% | 현예지 |
| `sign.signer` | 본인 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 법정대리인 | text | 100% | 위나아 |
| `seal.signer2` | 법정대리인 | seal | 100% | 위나아 |
| `sign.signer2` | 법정대리인 | signature | 100% | 여기준 |

### 기업간결제 제신고(약정해지,변경) 신청서 (`hf069`) — 키 20개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 업체명 | text | 100% | (주)유니온무역 |
| `customer.phone` | 연락처(선택) | phone | 100% | 010-5907-7253 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 261-82-53694 |
| `대표자생년월일` | 대표자/생년월일 | date | 100% | 2025년 8월 18일 |
| `customer.address` | 주소(선택) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `check.신청내용` | 신청내용 | checkbox | 100% | 세금계산서 본지사정보 등록/해제 |
| `변경내용` | 변경내용 | text | 100% | 학자금 |
| `약정상품명` | 약정상품명 | text | 100% | 의류 원단 |
| `약정번호` | 약정번호 | text | 100% | 472435-8232120 |
| `변경후` | 변경후 | text | 100% | 생활자금 |
| `customer.name` | 위임인 | text | 100% | 박찬연 |
| `agent.name` | 대리인성명 | text | 100% | 이도민 |
| `customer.phone2` | 연락처 | phone | 100% | 010-5907-7253 |
| `위임내용` | 위임내용 | text | 100% | 의료비 |
| `customer.birth` | 생년월일 | date | 100% | 900210 |
| `agent.relation` | 본인과의관계 | text | 100% | 부 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 업체명 | text | 100% | 박찬연 |
| `seal.signer` | 업체명 | seal | 100% | 강순준 |
| `sign.signer` | 업체명 | signature | 100% | 박찬연 |

### 전자방식 외상매출채권 결제제도 이용신청서(외담대,동반성장론,e-안심팩토링대출용) (`hf072`) — 키 31개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 법인명(또는상호명) | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표이사(또는대표자명) | text | 100% | 박찬연 |
| `company.biz_type` | 업태 | text | 100% | 도매 및 소매업 |
| `주요취급품목` | 주요취급품목 | text | 100% | 반도체 소자 |
| `value` | (우편번호:) | amount | 100% |  |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `check.기업규모` | 기업규모 | checkbox | 100% | 중기업 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `company.corp_reg_no` | 법인등록번호(법인의경우) | corp_reg_no | 100% | 200112-7448551 |
| `대표이사생년월일` | 대표이사(대표자)생년월일 | date | 100% | 2026-01-18 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `팩스번호` | 팩스번호 | phone | 100% | 033-364-7301 |
| `check.구매기업` | 구매기업(중심기업) | checkbox | 100% | 구매기업 (중심기업) |
| `check.구매기업2` | 구매기업(온라인마켓) | checkbox | 100% | 구매기업(온라인마켓) |
| `check.판매기업` | 판매기업(1차협력기업) | checkbox | 100% | 판매기업(1차협력기업) |
| `check.입점Seller` | 입점Seller(판매기업) | checkbox | 100% | 입점 Seller(판매기업) |
| `check.동반협력기업` | 동반협력기업 | checkbox | 100% | 동반협력기업 |
| `check.협력기업` | 협력기업 | checkbox | 100% | 협력기업 |
| `협력기업을위한채권발행및Exposure약정` | 협력기업(판매기업)을위한채권발행및Exposure약정 | text | 100% | (주)세진시스템즈 |
| `입점Seller를위한채권발행` | 입점Seller(판매기업)를위한채권발행 | text | 100% |  |
| `목록[].비고` | 비고 | text | 100% | 본인 요청 |
| `동반협력기업간상생매출채권발행및수취약정` | 동반협력기업간상생매출채권발행및수취약정 | number | 100% | 283,300,000 |
| `공급망상생결제협력기업간상생매출채권발행및수취약정` | 공급망상생결제협력기업간상생매출채권발행및수취약정 | number | 100% | 93,120,000 |
| `담당부서` | 담당부서 | text | 100% |  |
| `check.SKT` | SKT | checkbox | 100% | SKT |
| `check.해당되는` | 해당되는“ | checkbox | 100% | ”에 “V” 표시 합니다. |
| `담당자팩스번호` | 담당자팩스번호 | phone | 100% | 033-364-7301 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 강순준 |

### [필수] 개인(신용)정보 제3자 제공 동의서(안전망대출Ⅱ) (`hf073`) — 키 6개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `안전망대출II보증업무수행` | 안전망대출II보증업무수행 | text | 100% |  |
| `신용도판단정보` | ■신용도판단정보 | text | 100% |  |
| `customer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### [필수] 개인(신용)정보 제3자 제공 동의서(햇살론17) (`hf074`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `햇살론17보증업무수행` | -햇살론17보증업무수행 | text | 100% |  |
| `신용능력정보` | ■신용능력정보 | text | 100% |  |
| `customer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 위나아 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `signer2.name` | 대리인성명 | text | 100% | 이욱유 |
| `seal.signer2` | 대리인성명 | seal | 100% | 이주원 |
| `sign.signer2` | 대리인성명 | signature | 100% | 정현윤 |

### [필수]개인(신용)정보 제3자 제공 동의서(토지분양대금대출약정_대전광역시,대전도시공사) (`hf077`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `대전광역시대전도시공사` | -대전광역시,대전도시공사 | text | 100% |  |
| `제공일로부터5년까지보유이용` | -제공일로부터5년까지보유·이용 | text | 100% |  |
| `신용거래정보` | ■■신용거래정보 | text | 100% |  |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 현예지 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 최우빈 |
| `seal.signer2` | 대리인성명 | seal | 100% |  |
| `sign.signer2` | 대리인성명 | signature | 100% | 최우빈 |
| `이용목적` | 이용목적 | text | 100% | 투자 목적 |

### 통화전환 옵션부 외화대출 원화대출 전환신청서 (`hf078`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `원화대출전환희망일` | 원화대출전환희망일 | date | 100% | 2025-03-31 |
| `신청사유` | 신청사유 | text | 100% | 자녀 교육비 |
| `대출과목` | 대출과목 | text | 100% | 운전자금대출 |
| `대출금액` | 대출금액(본건전환후외화대출잔액) | number | 100% | 39,770,000 |
| `date` | 대출취급일 | date | 100% | 2026년 1월 31일 |
| `date2` | 대출만기일 | date | 100% | 2026년 1월 31일 |
| `대출금리` | 대출금리 | number | 100% | 100 |
| `date3` | 일자 | date | 100% | 2026년 1월 31일 |
| `date4` | 년월일 | date | 100% | 2026.01.31 |
| `주1` | 주1 | text | 100% |  |
| `date5` | 년월일 | date | 100% | 2026.01.31 |
| `주3` | 주3 | text | 100% |  |
| `date6` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 채무자본인 | text | 100% | 박찬연 |
| `seal.signer` | 채무자본인 | seal | 100% | 이욱유 |
| `sign.signer` | 채무자본인 | signature | 100% | 박찬연 |

### 정보교환 기업구매자금어음금 미결제통보확인서 (`hf079`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `미결제통보번호` | 미결제통보번호 | text | 100% | 947-828885-42526 |
| `추심의뢰일` | 추심의뢰일 | date | 100% | 2025.09.22 |
| `금융결제원어음번호` | 금융결제원어음번호 | text | 100% | 다다12694400 |
| `어음금액` | 어음금액 | number | 100% | 3,060,000원 |
| `발행인` | 발행인 | text | 100% | 주식회사 동방푸드 |
| `사유` | 사유 | text | 100% | 학자금 |
| `미결제확인번호` | 미결제확인번호 | text | 100% | 194464-7734071 |
| `Fax` | Fax()- | text | 100% |  |
| `Fax2` | Fax()- | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer` | _____________________부(지점) | seal | 100% | 강순준 |
| `sign.signer` | _____________________부(지점) | signature | 100% | 박찬연 |
| `seal.signer2` | _____________________부(지점) | seal | 100% | 이민빈 |
| `sign.signer2` | _____________________부(지점) | signature | 100% | 박찬연 |

### 정보교환 기업구매자금어음 부도통보확인서 (`hf080`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `부도통보번호` | 부도통보번호 | text | 100% | 952328-8622468 |
| `추심의뢰일` | 추심의뢰일 | date | 100% | 2025-12-06 |
| `금융결제원어음번호` | 금융결제원어음번호 | text | 100% | 차라65803979 |
| `어음금액` | 어음금액 | number | 100% | 31,840,000원 |
| `발행인` | 발행인 | text | 100% | (주)유니온메디칼 |
| `사유` | 사유 | text | 100% | 해외 이주 |
| `부도확인번호` | 부도확인번호 | text | 100% | 217968-2393602 |
| `Fax` | Fax()- | text | 100% |  |
| `Fax2` | Fax()- | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer` | _____________________부(지점) | seal | 100% | 강순준 |
| `sign.signer` | _____________________부(지점) | signature | 100% | 박찬연 |
| `seal.signer2` | _____________________부(지점) | seal | 100% | 현예지 |
| `sign.signer2` | _____________________부(지점) | signature | 100% | 박찬연 |

### 정보교환 기업구매자금어음 인수거절통보확인서 (`hf081`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `인수거절통보번호` | 인수거절통보번호 | text | 100% | 022-198273-53789 |
| `추심의뢰일` | 추심의뢰일 | date | 100% | 2025-06-26 |
| `금융결제원어음번호` | 금융결제원어음번호 | text | 100% | 아나39852455 |
| `어음금액` | 어음금액 | number | 100% | 5,080,000 |
| `발행인` | 발행인 | text | 100% | 미래물산 |
| `사유` | 사유 | text | 100% | 사업자금 |
| `인수거절확인번호` | 인수거절확인번호 | text | 100% | 306-977410-26873 |
| `Fax` | Fax()- | text | 100% |  |
| `Fax2` | Fax()- | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer` | _____________________부(지점) | seal | 100% | 박찬연 |
| `sign.signer` | _____________________부(지점) | signature | 100% | 현예지 |
| `seal.signer2` | _____________________부(지점) | seal | 100% | 박찬연 |
| `sign.signer2` | _____________________부(지점) | signature | 100% | 현예지 |

### 채권발행 등록 신청서 (`hf082`) — 키 24개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `구매기업명` | 구매기업명 | text | 100% | (주)동방화학 |
| `총처리건수` | 총처리건수 | number | 100% | 60 |
| `구매기업사업자등록번호` | 구매기업사업자등록번호 | biz_no | 100% | 781-77-32938 |
| `총처리금액` | 총처리금액 | number | 100% | 17,280,000 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `호` | 호 | text | 100% |  |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `signer.name` | 자 | text | 100% | 박찬연 |
| `seal.signer` | 자 | seal | 100% | 현예지 |
| `sign.signer` | 자 | signature | 100% | 박찬연 |
| `소` | 소 | text | 100% |  |
| `signer2.name` | 명 | text | 100% | 박찬연 |
| `seal.signer2` | 명 | seal | 100% | 박찬연 |
| `sign.signer2` | 명 | signature | 100% | 강순준 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `목록[].중심업체코드` | 중심업체코드 | text | 100% | 26365 |
| `목록[].판매기업사업자번호` | 판매기업사업자번호 | text | 100% | 149-25-25124 |
| `목록[].판매기업명` | 판매기업명 | text | 100% | 미래시스템즈(주) |
| `목록[].채권발행일자채권만기일자` | 채권발행일자채권만기일자 | text | 100% | 2029.12.01 |
| `목록[].채권금액` | 채권금액 | text | 100% | 10,700,000 |
| `목록[].세금계산서승인번호` | 세금계산서승인번호 | text | 100% | 5310-3453 |
| `목록[].세금계산서합계금액` | 세금계산서합계금액 | text | 100% | 6,880,000 |
| `목록[].세금계산서작성일자` | 세금계산서작성일자 | text | 100% | 2025.04.10 |

### 전자방식 외상매출채권 결제제도 이용신청서 (서울시농수산식품공사용) (`hf083`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 법인명(또는상호명) | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표이사(또는대표자명) | text | 100% | 박찬연 |
| `company.biz_type` | 업태 | text | 100% | 도매 및 소매업 |
| `주요취급품목` | 주요취급품목 | text | 100% | 철강 코일 |
| `value` | (우편번호:) | amount | 100% |  |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `check.기업규모` | 기업규모 | checkbox | 100% | 공공 및 기타 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `company.corp_reg_no` | 법인등록번호(법인인경우) | corp_reg_no | 100% | 200112-7448551 |
| `대표이사생년월일` | 대표이사(대표자)생년월일 | date | 100% | 2025.12.29 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `팩스번호` | 팩스번호 | phone | 100% | 043-783-2775 |
| `check.외상매출채권의` | 외상매출채권의 | checkbox | 100% | 외상매출채권의 |
| `check.판매기업` | 판매기업 | checkbox | 100% | 판매기업 |
| `목록[].비고` | 비고 | text | 100% | 본인 요청 |
| `담당부서` | 담당부서 | text | 100% |  |
| `check.SKT` | SKT | checkbox | 100% | LGU+ |
| `담당자팩스번호` | 담당자팩스번호 | phone | 100% | 043-783-2775 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 강순준 |

### 외상매출채권 양도통지서(장래채권양도통지용) (`hf084`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 주식회사하나은행 | text | 100% | (주)유니온무역 |
| `seal.signer` | 주식회사하나은행 | seal | 100% | (주)유니온무역 |
| `sign.signer` | 주식회사하나은행 | signature | 100% | 주식회사 대성패션 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer2.name` | 주식회사하나은행 | text | 100% | (주)유니온무역 |
| `seal.signer2` | 주식회사하나은행 | seal | 100% | 주식회사 한빛패션 |
| `sign.signer2` | 주식회사하나은행 | signature | 100% | (주)유니온무역 |
| `customer.address3` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |

### 신용정보 제공 동의서(외담대,e-안심팩토링,동반성장론 구매기업용) (`hf085`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].상품명` | 상품명 | text | 100% | PCB 기판 |
| `목록[].중심업체코드` | 중심업체코드 | number | 100% | 803603 |
| `목록[].한도승인번호` | 한도승인번호 | number | 100% | 196,620,000 |
| `목록[].정보제공내용` | 정보제공내용 | text | 100% | 만기 해지 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `신용거래정보의제공목적` | ■신용거래정보의제공목적 | text | 100% |  |
| `신용거래정보의제공받을자` | ■신용거래정보의제공받을자 | text | 100% |  |
| `제공할신용거래정보등의내용및범위` | ■제공할신용거래정보등의내용및범위 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 동의자본인회사명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 동의자본인회사명 | seal | 100% | 주식회사 대성패션 |
| `sign.signer` | 동의자본인회사명 | signature | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `customer.phone` | 전화번호(선택항목) | phone | 100% | 010-5907-7253 |

### 미래채권담보대출 협력기업 일괄추천서 (`hf086`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].업체명` | 업체명 | text | 100% | (주)유니온물산 |
| `목록[].대표자` | 대표자 | text | 100% |  |
| `목록[].법인번호` | 법인번호 | text | 100% | 661657-8908194 |
| `목록[].사업자번호` | 사업자번호 | text | 100% | 255-40-68284 |
| `총계` | 총계 | text | 100% |  |
| `목록[].최초거래일자` | 최초거래일자 | text | 100% | 2024-09-03 |
| `목록[].납품실적` | 납품실적* | text | 100% |  |
| `목록[].평균결제기간` | 평균결제기간* | text | 100% |  |
| `목록[].주소` | 주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `목록[].전화` | 전화 | text | 100% | 010-7321-8870 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | (회사명) | text | 100% | 박찬연 |
| `seal.signer` | (회사명) | seal | 100% | 박찬연 |
| `sign.signer` | (회사명) | signature | 100% | 현예지 |

### 미래채권담보대출 추천서 (`hf087`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `최초거래일자` | 최초거래일자 | date | 100% | 2025년 2월 16일 |
| `연간` | 연간 | text | 100% |  |
| `계약서` | 계약서(주1) | text | 100% |  |
| `평균결제기간` | 평균결제기간(주2) | text | 100% |  |
| `백만원` | ()백만원 | text | 100% |  |
| `전자결제방식` | 전자결제방식 | text | 100% |  |
| `전자방식외상매출채권전자어음구매전용카드` | ()전자방식외상매출채권()전자어음()구매전용카드 | number | 100% | 5,070,000원 |
| `customer.phone` | 연락처(핸드폰번호) | phone | 100% | 010-5907-7253 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 업체명 | text | 100% | 박찬연 |
| `seal.signer` | 업체명 | seal | 100% | 박찬연 |
| `sign.signer` | 업체명 | signature | 100% | 현예지 |
| `signer2.name` | 대표자 | text | 100% | 박찬연 |
| `seal.signer2` | 대표자 | seal | 100% | 이민빈 |
| `sign.signer2` | 대표자 | signature | 100% | 박찬연 |
| `납품` | 납품 | text | 100% |  |

### 기업구매자금어음 추심취소 및 반환의뢰서 (`hf088`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].사업자번호` | 사업자번호 | text | 100% | 268-16-18451 |
| `목록[].사업자명` | 사업자명 | text | 100% | (주)유니온무역 |
| `목록[].추심금액` | 추심금액 | text | 100% | 1,730,000 |
| `건` | 건 | text | 100% |  |
| `목록[].추심의뢰일` | 추심의뢰일 | text | 100% | 2025.03.31 |
| `목록[].지급은행` | 지급은행 | text | 100% | 카카오뱅크 |
| `목록[].대표품명` | 대표품명 | text | 100% | 포장재 |
| `목록[].공급가액` | 공급가액 | text | 100% | 156,220,000 |
| `목록[].반환사유` | 반환사유 | text | 100% | 하나 단기채 펀드 |
| `check.아래의기업구매자금어음을` | 아래의기업구매자금어음을( | checkbox | 100% | 반환) 하여 주시기 바랍니다. |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |

### 외상매출채권 양도통지서(e-안심팩토링대출용) (`hf089`) — 키 6개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.address3` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |

### 납품대금 선입금(벤더입금) 신청서 (`hf090`) — 키 26개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `선입금신청금액` | 선입금(벤더입금)신청금액 | number | 100% | 17,600,000 |
| `판매기업입금일` | 판매기업입금일(또는결제일) | date | 100% | 2025년 3월 20일 |
| `벤더기업명` | 벤더기업명 | text | 100% | 주식회사 제일화학 |
| `check.벤더취급수수료부담주체` | 벤더취급수수료부담주체(벤더입금건별₩1,000) | checkbox | 100% | 벤더기업 |
| `지급승인금액` | 지급승인금액 | number | 100% | 720,000 |
| `벤더기업사업자등록번호` | 벤더기업사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `check.벤더입금이자부담주체` | 벤더입금이자부담주체 | checkbox | 100% | 판매기업 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `company.name` | 상호 | text | 100% | (주)유니온무역 |
| `signer.name` | 대표자 | text | 100% | 박찬연 |
| `seal.signer` | 대표자 | seal | 100% | 박찬연 |
| `sign.signer` | 대표자 | signature | 100% | 현예지 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer2.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer2` | 성명 | seal | 100% | 박찬연 |
| `sign.signer2` | 성명 | signature | 100% | 강순준 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `목록[].선입금신청금액` | 선입금신청금액 | text | 100% | 2,200,000원 |
| `목록[].채권번호` | 채권번호 | text | 100% | 7096-2057 |
| `목록[].채권금액` | 채권금액 | text | 100% | 45,540,000 |
| `목록[].발행일` | 발행일 | text | 100% | 2025년 12월 12일 |
| `목록[].결제일` | 결제일 | text | 100% | 2026.01.13 |
| `목록[].중심업체코드` | 중심업체코드 | text | 100% | 7719 |
| `목록[].구매기업사업자번호` | 구매기업사업자번호 | text | 100% | 264-82-36559 |
| `목록[].구매기업명` | 구매기업명 | text | 100% | (주)유니온무역 |

### 기업구매자금 결제제도 이용 신청서 (`hf091`) — 키 19개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 법인명(또는상호명) | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표이사(또는대표자명) | text | 100% | 박찬연 |
| `company.biz_type` | 업태 | text | 100% | 도매 및 소매업 |
| `주요취급품목` | 주요취급품목 | text | 100% | 철강 코일 |
| `value` | (우편번호:) | amount | 100% |  |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `대표이사생년월일` | 대표이사(대표자)생년월일 | date | 100% | 2025년 9월 28일 |
| `company.biz_item` | 종목 | text | 100% | 무역 |
| `팩스번호` | 팩스번호 | phone | 100% | 043-783-2775 |
| `일반구매자금결제제도` |  일반구매자금결제제도 | text | 100% |  |
| `담당부서` | 담당부서 | text | 100% |  |
| `담당자전화번호` | 담당자전화번호 | phone | 100% | 010-5907-7253 |
| `담당자팩스번호` | 담당자팩스번호 | phone | 100% | 02-279-2475 |
| `담당자명` | 담당자명 | text | 100% | 박찬연 |
| `담당자휴대전화번호` | 담당자휴대전화번호 | phone | 100% | 010-5907-7253 |
| `담당자이메일` | 담당자이메일 | date | 100% | 2024년 4월 19일 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 외상매출채권양도통지서(개별채권양도통지용) (`hf092`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `발신인주소` | 발신인주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `발신인` | 발신인 | text | 100% |  |
| `수신인주소` | 수신인주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `수신인` | 수신인 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 주식회사하나은행 | text | 100% | (주)유니온무역 |
| `seal.signer` | 주식회사하나은행 | seal | 100% | (주)유니온무역 |
| `sign.signer` | 주식회사하나은행 | signature | 100% | 주식회사 한빛패션 |
| `customer.address` | 주소 | text | 100% | 서울특별시 송파구 중대로 174, 119동 2202호 |
| `목록[].외상매출채권번호` | 외상매출채권번호 | text | 100% | 6,680,000 |
| `목록[].채권양도인사업자번호` | 채권양도인사업자번호 | text | 100% | 264-82-36559 |
| `목록[].채권양도인` | 채권양도인 | text | 100% | 미래화학(주) |
| `목록[].채권양도금액` | 채권양도금액 | text | 100% | 24,040,000 |
| `목록[].채권발행일` | 채권발행일 | text | 100% | 2025년 9월 28일 |
| `목록[].채권지급일` | 채권지급일 | text | 100% | 2025년 11월 25일 |
| `목록[].비고` | 비고 | text | 100% | 사업자금 |

### 미결제 전자채권대금 입금확인서 (`hf093`) — 키 10개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].전자채권번호` | 전자채권번호 | text | 100% | 797-718221-16886 |
| `목록[].구매기업명` | 구매기업명(사업자번호) | text | 100% | 가온상사(주) |
| `목록[].발행일` | 발행일 | text | 100% | 2025.01.15 |
| `목록[].만기일` | 만기일(미결제일) | text | 100% | 2025-05-18 |
| `목록[].입금액` | 입금액 | text | 100% | 380,000 |
| `목록[].입금일` | 입금일 | text | 100% | 2025.01.10 |
| `목록[].판매기업명` | 판매기업명 | text | 100% | 우진메디칼 |
| `목록[].판매기업계좌번호` | 판매기업계좌번호 | text | 100% | 903-453809-53231 |
| `seal.signer` | 지점장 | seal | 100% | 박찬연 |
| `sign.signer` | 지점장 | signature | 100% | 현예지 |

### 상생벤더구매론 승인명세 등록신청서 (`hf094`) — 키 30개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `차협력기업명` | 차협력기업명 | text | 100% | 새한시스템즈 |
| `총처리건수` | 총처리건수 | number | 100% | 1 |
| `차협력기업사업자등록번호` | 차협력기업사업자등록번호 | biz_no | 100% | 615-22-78976 |
| `총처리금액` | 총처리금액 | number | 100% | 9,980,000 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `호` | 호 | text | 100% |  |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `signer.name` | 자 | text | 100% | 박찬연 |
| `seal.signer` | 자 | seal | 100% | 현예지 |
| `sign.signer` | 자 | signature | 100% | 박찬연 |
| `소` | 소 | text | 100% |  |
| `signer2.name` | 명 | text | 100% | 박찬연 |
| `seal.signer2` | 명 | seal | 100% | 이욱유 |
| `sign.signer2` | 명 | signature | 100% | 박찬연 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `목록[].원청채권종류` | 원청채권종류 | text | 100% |  |
| `목록[].원청채권번호` | 원청채권번호 | text | 100% | 743628-4600635 |
| `목록[].원청구매기업명` | 원청구매기업명 | text | 100% | 주식회사 청솔산업 |
| `목록[].사업자등록번호` | 사업자등록번호 | text | 100% | 494-13-94630 |
| `목록[].원청채권금액` | 원청채권금액 | text | 100% | 460,000 |
| `목록[].원청채권발행일` | 원청채권발행일 | text | 100% | 2024.10.15 |
| `목록[].원청채권만기일` | 원청채권만기일 | text | 100% | 2028년 6월 20일 |
| `목록[].차협력기업명` | 차협력기업명 | text | 100% | 주식회사 대성패션 |
| `목록[].승인금액` | 승인금액 | text | 100% | 4,560,000 |
| `목록[].선입금가능일` | 선입금가능일 | text | 100% | 2024-04-06 |
| `목록[].세금계산서승인번호` | 세금계산서승인번호 | text | 100% | 136-157360-65984 |
| `목록[].세금계산서합계금액` | 세금계산서합계금액 | text | 100% | 520,000 |
| `목록[].세금계산서작성일자` | 세금계산서작성일자 | text | 100% | 2024.10.10 |
| `목록[].품목명` | 품목명 | text | 100% | 자동차 부품 |

### 벤더승인명세 등록 신청서 (`hf095`) — 키 20개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].하위벤더기업명` | 하위벤더기업명 | text | 100% | (주)제일푸드 |
| `목록[].사업자등록번호` | 사업자등록번호 | text | 100% | 476-10-37265 |
| `목록[].벤더승인금액` | 벤더승인금액 | text | 100% | 140,000 |
| `목록[].세금계산서발행일` | 세금계산서발행일 | text | 100% | 2025-12-29 |
| `목록[].세금계산서발행금액` | 세금계산서발행금액 | text | 100% | 150,740,000 |
| `목록[].세금계산서승인번호` | 세금계산서승인번호 | text | 100% | 9739-1377 |
| `목록[].품목명` | 품목명 | text | 100% | 의류 원단 |
| `목록[].비고` | 비고 | text | 100% | 만기 해지 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `호` | 호 | text | 100% |  |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `signer.name` | 자 | text | 100% | 박찬연 |
| `seal.signer` | 자 | seal | 100% | 박찬연 |
| `sign.signer` | 자 | signature | 100% | 이욱유 |
| `소` | 소 | text | 100% |  |
| `signer2.name` | 명 | text | 100% | 박찬연 |
| `seal.signer2` | 명 | seal | 100% | 박찬연 |
| `sign.signer2` | 명 | signature | 100% | 강순준 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |

### 발주명세 등록신청서 (`hf096`) — 키 25개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `중심기업명` | 중심기업명 | text | 100% | 신영산업(주) |
| `총처리건수` | 총처리건수 | number | 100% | 36 |
| `중심기업사업자등록번호` | 중심기업사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `총처리금액` | 총처리금액 | number | 100% | 157,930,000 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `호` | 호 | text | 100% |  |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `signer.name` | 자 | text | 100% | 박찬연 |
| `seal.signer` | 자 | seal | 100% | 박찬연 |
| `sign.signer` | 자 | signature | 100% | 강순준 |
| `소` | 소 | text | 100% |  |
| `signer2.name` | 명 | text | 100% | 박찬연 |
| `seal.signer2` | 명 | seal | 100% | 현예지 |
| `sign.signer2` | 명 | signature | 100% | 박찬연 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `목록[].차협력기업명` | 차협력기업명 | text | 100% | 주식회사 누리시스템즈 |
| `목록[].사업자등록번호` | 사업자등록번호 | text | 100% | 473-76-35755 |
| `목록[].발주번호` | 발주번호 | text | 100% | 450590-9899679 |
| `목록[].발주금액` | 발주금액 | text | 100% | 7,200,000 |
| `목록[].납품기한` | 납품기한 | text | 100% | 2027년 11월 30일 |
| `목록[].대금지급일` | 대금지급일 | text | 100% | 2025.07.16 |
| `목록[].대금지급확약비율` | 대금지급확약비율 | text | 100% | 100 |
| `목록[].품목명` | 품목명 | text | 100% | 전자부품 |
| `목록[].비고` | 비고 | text | 100% | 전세자금 |

### 미래채권 대출신청서(미래대,상생미래대용) (`hf097`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].대출실행일` | 대출실행일 | text | 100% | 2025-01-24 |
| `목록[].대출신청금액` | 대출신청금액 | text | 100% | 10,990,000 |
| `목록[].의뢰일` | 의뢰일 | text | 100% | 2025.11.09 |
| `목록[].발주번호` | 발주번호 | text | 100% | 057359-2046993 |
| `목록[].발주금액` | 발주금액 | text | 100% | 33,370,000 |
| `목록[].납품기한` | 납품기한 | text | 100% | 2028-03-29 |
| `목록[].대금지급일` | 대금지급일 | text | 100% | 2025.01.05 |
| `목록[].대금지급확약비율` | 대금지급확약비율 | text | 100% | 100 |
| `목록[].구매기업사업자등록번호` | 구매기업사업자등록번호 | text | 100% | 174-15-09742 |
| `목록[].구매기업명` | 구매기업명 | text | 100% | (주)가온정밀 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `소` | 소 | text | 100% |  |

### 기업구매자금어음 지급제시 명세 (`hf098`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].결제원어음번호` | 결제원어음번호 | text | 100% | 사나69668304 |
| `목록[].어음금액` | 어음금액 | text | 100% | 187,170,000 |
| `목록[].인수거절여부` | 인수거절여부 | text | 100% |  |
| `목록[].인수거절사유` | 인수거절사유 | text | 100% | 하나 TDF 2040 |
| `목록[].대출일` | 대출일 | text | 100% | 2025.01.01 |
| `목록[].대출신청금액` | 대출신청금액 | text | 100% | 6,970,000 |
| `목록[].대출만기일` | 대출만기일 | text | 100% | 2029.10.25 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |

### 지급승인명세 등록 신청서 (`hf099`) — 키 25개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `중심기업명` | 중심기업명 | text | 100% | (주)유니온무역 |
| `중심기업사업자등록번호` | 중심기업사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `총처리금액` | 총처리금액 | number | 100% | 249,670,000 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `호` | 호 | text | 100% |  |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `signer.name` | 자 | text | 100% | 박찬연 |
| `seal.signer` | 자 | seal | 100% | 강순준 |
| `sign.signer` | 자 | signature | 100% | 이민빈 |
| `소` | 소 | text | 100% |  |
| `signer2.name` | 명 | text | 100% | 박찬연 |
| `seal.signer2` | 명 | seal | 100% | 김나우 |
| `sign.signer2` | 명 | signature | 100% | 박찬연 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `목록[].판매기업사업자번호` | 판매기업사업자번호 | text | 100% | 264-82-36559 |
| `목록[].판매기업명` | 판매기업명 | text | 100% | 청솔푸드 |
| `목록[].구매기업결제일자` | 구매기업결제일자 | text | 100% | 2025.02.09 |
| `목록[].판매기업입금일자` | 판매기업입금일자 | text | 100% | 2025.01.23 |
| `목록[].승인금액` | 승인금액 | text | 100% | 8,500,000 |
| `목록[].선입금가능일자` | 선입금가능일자 | text | 100% | 2025.04.04 |
| `목록[].세금계산서승인번호` | 세금계산서승인번호 | text | 100% | 103074-0173351 |
| `목록[].세금계산서합계금액` | 세금계산서합계금액 | text | 100% | 7,350,000 |
| `목록[].세금계산서작성일자` | 세금계산서작성일자 | text | 100% | 2025년 12월 26일 |
| `목록[].품목명` | 품목명 | text | 100% | 냉동 수산물 |

### 창구대출신청서(전자채권담보대출용) (`hf100`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].채권번호` | 채권번호 | text | 100% | 777-228980-77775 |
| `목록[].구매기업명` | 구매기업명 | text | 100% | 주식회사 우진시스템즈 |
| `목록[].대표자` | 대표자 | text | 100% |  |
| `목록[].공급물품명` | 공급물품명 | text | 100% | 냉동 수산물 |
| `목록[].세금계산서발행일` | 세금계산서발행일 | text | 100% | 2025.09.26 |
| `목록[].전자채권금액` | 전자채권금액 | text | 100% | 620,000 |
| `목록[].만기일` | 만기일 | text | 100% | 2028.05.16 |
| `목록[].대출신청액` | 대출신청액 | text | 100% |  |
| `목록[].대출만기일` | 대출만기일 | text | 100% | 2029.06.09 |
| `목록[].입금계좌번호` | 입금계좌번호 | text | 100% | 427-579298-43874 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 인 | text | 100% | 박찬연 |
| `seal.signer` | 인 | seal | 100% | 박찬연 |
| `sign.signer` | 인 | signature | 100% | 이욱유 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `소` | 소 | text | 100% |  |

### 기업현황서(B2B전자결제서비스 업무, MP용) (`hf102`) — 키 64개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `signer.name` | 대표이사 | text | 100% | 박찬연 |
| `seal.signer` | 대표이사 | seal | 100% | 박찬연 |
| `sign.signer` | 대표이사 | signature | 100% | 이민빈 |
| `employer.position` | 직위 | text | 100% | 대리 |
| `signer2.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer2` | 성명 | seal | 100% | 박찬연 |
| `sign.signer2` | 성명 | signature | 100% | 김소윤 |
| `연락처TEL` | 연락처:TEL | phone | 100% | 010-5907-7253 |
| `customer.phone` | HP | phone | 100% | 010-5907-7253 |
| `FAX` | FAX | phone | 100% | 043-783-2775 |
| `company.name2` | 기업체명 | text | 100% | (주)유니온무역 |
| `본사` | 본사 | text | 100% |  |
| `주사무소` | 주사무소 | text | 100% |  |
| `사업장` | 사업장 | text | 100% |  |
| `company.biz_item` | 업종(표준산업분류기호) | text | 100% | 무역 |
| `종업원수` | 종업원수 | text | 100% |  |
| `사업모델및특성_목록[].모델명` | 모델명 | text | 100% | 식품 원재료 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `협회및단체가입` | 협회및단체가입 | text | 100% |  |
| `인허가등록` | 인허가등록 | text | 100% |  |
| `주거래은행` | 주거래은행 | text | 100% | 농협은행 |
| `총자산` | 총자산 | text | 100% |  |
| `자본금` | 자본금 | text | 100% |  |
| `자기자본` | 자기자본 | text | 100% |  |
| `매출액` | 매출액 | number | 100% | 320,000 |
| `경상이익` | 경상이익 | text | 100% |  |
| `당기순이익` | 당기순이익 | text | 100% |  |
| `사업모델및특성_목록[].내용` | 내용 | text | 100% | 계좌 정리 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `TEL` | TEL | text | 100% |  |
| `FAX2` | FAX | phone | 100% | 043-783-2775 |
| `TEL2` | TEL | text | 100% |  |
| `TEL3` | TEL | text | 100% |  |
| `설립년월` | 설립년월 | text | 100% |  |
| `사업모델및특성_목록[].특성` | 특성 | text | 100% |  |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `정부기관및금융기관우대` | 정부기관및금융기관우대 | text | 100% | 하나은행 |
| `요약재무현황_목록[].년` | 년 | text | 100% |  |
| `당좌거래은행` | 당좌거래은행 | text | 100% | 국민은행 |
| `목록[].주주명` | 주주명 | text | 100% | 홍채혜 |
| `목록[].소유주식수` | 소유주식수 | text | 100% |  |
| `목록[].지분율` | 지분율 | text | 100% | 100 |
| `목록[].대주주와의관계` | 대주주와의관계 | text | 100% |  |
| `목록[].회사와의관계` | 회사와의관계 | text | 100% |  |
| `목록[].성명` | 성명 | text | 100% | 허수지 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `주요경력_목록[].기간` | 기간 | text | 100% |  |
| `주요경력_목록[].근무처` | 근무처 | text | 100% |  |
| `주요경력_목록[].담당업무` | 담당업무 | text | 100% |  |
| `주요경력_목록[].최종직위` | 최종직위 | text | 100% |  |
| `목록[].직위` | 직위 | text | 100% |  |
| `목록[].관계` | 관계 | text | 100% |  |
| `목록[].주요경력` | 주요경력 | text | 100% |  |
| `목록[].연월일` | 연월일 | text | 100% | 2025.12.23 |
| `목록[].내용` | 내용 | text | 100% | 전세자금 |
| `제품명` | 제품명 | text | 100% | 전자부품 |
| `판매처` | 판매처 | text | 100% |  |
| `목록[].년` | 년 | text | 100% |  |
| `판매조건` | 판매조건 | text | 100% |  |
| `원재료명` | 원재료명 | text | 100% |  |
| `구매처` | 구매처 | text | 100% |  |
| `구매조건` | 구매조건 | text | 100% |  |

### B2B 전자결제서비스 업무 이용신청서(MP용) (`hf103`) — 키 26개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.biz_type` | 업태 | text | 100% | 도매 및 소매업 |
| `company.name` | 기업명(MP상호명) | text | 100% | (주)유니온무역 |
| `MPURL` | MPURL | text | 100% |  |
| `company.ceo` | 대표자명 | text | 100% | 박찬연 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `수수료입금계좌` | 수수료입금계좌 | number | 100% | 53,500,000 |
| `담당부서` | 담당부서 | text | 100% |  |
| `담당자명` | 담당자명 | text | 100% | 신순서 |
| `email주소` | e-mail주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `신용보증` | 신용보증 | text | 100% |  |
| `기술보증` | 기술보증 | text | 100% |  |
| `지역보증` | 지역보증 | text | 100% |  |
| `대표자생년월일` | 대표자생년월일 | date | 100% | 2025-12-01 |
| `FAX번호` | FAX번호 | phone | 100% | 043-783-2775 |
| `customer.name` | 예금주명 | text | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer` | 성명 | seal | 100% | 위나아 |
| `sign.signer` | 성명 | signature | 100% | 박찬연 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `선택` | 선택 | text | 100% |  |
| `있어야추심등록및대출실행` | 있어야추심등록및대출실행 | text | 100% |  |
| `절차필요` | 절차필요 | text | 100% |  |

### 기업구매자금어음 추심의뢰서 (`hf104`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].사업자번호` | 사업자번호 | text | 100% | 264-82-36559 |
| `목록[].사업자명` | 사업자명 | text | 100% | 누리전자(주) |
| `목록[].어음금액` | 어음금액 | text | 100% | 70,970,000 |
| `목록[].발행일` | 발행일 | text | 100% | 2025.10.29 |
| `목록[].대표품명` | 대표품명 | text | 100% | LED 모듈 |
| `목록[].공급가액` | 공급가액 | text | 100% | 201,630,000 |
| `목록[].지급은행` | 지급은행 | text | 100% | 농협은행 |
| `건수` | 건수 | number | 100% | 36 |
| `금액` | 금액 | number | 100% | 12,100,000 |
| `수수료` | 수수료 | number | 100% | 9,690,000원 |
| `비고` | 비고 | text | 100% | 자녀 교육비 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 인 | text | 100% | 박찬연 |
| `seal.signer` | 인 | seal | 100% | 현예지 |
| `sign.signer` | 인 | signature | 100% | 박찬연 |
| `signer2.name` | 사업자번호 | text | 100% | 박찬연 |
| `seal.signer2` | 사업자번호 | seal | 100% | 박찬연 |
| `sign.signer2` | 사업자번호 | signature | 100% | 이욱유 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer3` | 지점 | seal | 100% | 현예지 |
| `sign.signer3` | 지점 | signature | 100% | 이민빈 |

### 전자채권미결제 확인의뢰서 및 확인서 (`hf105`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].전자채권번호` | 전자채권번호 | text | 100% | 7375-4584 |
| `목록[].발행기업명` | 발행기업명(사업자등록번호) | text | 100% | 주식회사 세진테크 |
| `목록[].금액` | 금액 | number | 100% | 680,000 |
| `목록[].발행일` | 발행일 | date | 100% | 2025년 2월 6일 |
| `목록[].만기일` | 만기일 | date | 100% | 2029.11.11 |
| `목록[].미결제사유` | 미결제사유 | text | 100% | 하나 MMF |
| `전자채권지급장소` | 전자채권지급장소 | text | 100% |  |
| `발행은행지점` | 발행은행지점 | text | 100% | 국민은행 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.name` | 의뢰인 | text | 100% | 박찬연 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer` | 지점 | seal | 100% | 박찬연 |
| `sign.signer` | 지점 | signature | 100% | 이민빈 |

### 기업구매자금어음(기업구매자금용) (`hf106`) — 키 4개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 발행인 | text | 100% | 박찬연 |
| `seal.signer` | 발행인 | seal | 100% | 강순준 |
| `sign.signer` | 발행인 | signature | 100% | 박찬연 |

### 기업구매자금대출 연장신청서 (`hf107`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].계좌번호` | 계좌번호 | text | 100% | 005-785664-39470 |
| `목록[].추심의뢰인` | 추심의뢰인 | text | 100% | (주)다온시스템즈 |
| `목록[].대출금액` | 대출금액 | text | 100% | 50,000 |
| `목록[].대출취급일` | 대출취급일 | text | 100% | 2025.03.25 |
| `목록[].당초만기일` | 당초만기일 | text | 100% | 2028년 5월 29일 |
| `목록[].기한연장일` | 기한연장일 | text | 100% | 2027년 9월 16일 |
| `목록[].비고` | 비고 | text | 100% | 투자 목적 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 이욱유 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |

### 외상매출채권 대출신청서(외담대,e-안심팩토링대출 겸용) (`hf108`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].대출실행일` | 대출실행일 | text | 100% | 2025.12.18 |
| `목록[].대출신청금액` | 대출신청금액 | text | 100% | 870,000 |
| `목록[].의뢰일` | 의뢰일 | text | 100% | 2025년 1월 26일 |
| `목록[].의뢰번호` | 의뢰번호 | text | 100% | 459-639898-31801 |
| `목록[].매출금액` | 매출금액 | text | 100% | 225,780,000원 |
| `목록[].지급기일` | 지급기일 | text | 100% | 2028.12.17 |
| `목록[].구매기업사업자번호` | 구매기업사업자번호 | text | 100% | 622-32-65823 |
| `목록[].구매기업명` | 구매기업명 | text | 100% | (주)세진산업 |
| `목록[].발행일` | 발행일 | text | 100% | 2025.06.01 |
| `목록[].공급금액` | 공급금액 | text | 100% | 44,380,000 |
| `목록[].총공급금액` | 총공급금액(세금포함) | text | 100% | 119,790,000 |
| `목록[].거래품목` | 거래품목 | text | 100% | 식품 원재료 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 인 | text | 100% | 박찬연 |
| `seal.signer` | 인 | seal | 100% | 박찬연 |
| `sign.signer` | 인 | signature | 100% | 강순준 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `소` | 소 | text | 100% |  |

### 전자채권사고신고(취하)서 (`hf109`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `전자채권번호` | 전자채권번호 | text | 100% | 857-148214-67489 |
| `발행일` | 발행일 | date | 100% | 2025.09.06 |
| `판매기업기업명` | 판매기업기업명 | text | 100% | (주)유니온무역 |
| `담보금입금유무` | 담보금입금유무 | text | 100% |  |
| `사고신고사유` | 사고신고(취하)사유 | text | 100% | 급여 수령 |
| `금액` | 금액 | number | 100% | 187,170,000 |
| `만기일` | 만기일 | date | 100% | 2025-08-15 |
| `판매기업사업자번호` | 판매기업사업자번호 | biz_no | 100% | 264-82-36559 |
| `check.사고신고구분` | 사고신고구분 | checkbox | 100% | 신고 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 발행인 | text | 100% | 박찬연 |
| `seal.signer` | 발행인 | seal | 100% | 현예지 |
| `sign.signer` | 발행인 | signature | 100% | 박찬연 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |

### 전자방식 외상매출채권 발행취소 신청서(외담대,e-안심팩토링용) (`hf110`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].채권번호` | 채권번호 | text | 100% | 4540-9276 |
| `목록[].판매기업명` | 판매기업명 | text | 100% | 가온메디칼 |
| `목록[].판매기업사업자번호` | 판매기업사업자번호 | text | 100% | 842-09-95879 |
| `목록[].발행일` | 발행일 | text | 100% | 2025년 8월 6일 |
| `목록[].만기일` | 만기일 | text | 100% | 2026.04.08 |
| `목록[].채권금액` | 채권금액 | text | 100% | 640,000원 |
| `목록[].취소사유` | 취소사유 | text | 100% | 하나 정기예금 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `구매기업주소` | 구매기업:주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.name` | 업체명 | text | 100% | (주)유니온무역 |
| `signer.name` | 대표자 | text | 100% | 박찬연 |
| `seal.signer` | 대표자 | seal | 100% | 박찬연 |
| `sign.signer` | 대표자 | signature | 100% | 강순준 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `company.name2` | 업체명 | text | 100% | (주)유니온무역 |
| `signer2.name` | 대표자 | text | 100% | 박찬연 |
| `seal.signer2` | 대표자 | seal | 100% | 박찬연 |
| `sign.signer2` | 대표자 | signature | 100% | 강순준 |

### 《개인》위임장(해외체제자 담보대출용) (`hf111`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `customer.address` | 현주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `agent.name` | 성명 | text | 100% | 박영준 |
| `agent.address` | 주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `영주권번호` | 영주권번호 | text | 100% | 044-515544-78718 |
| `여권번호` | 여권번호 | text | 100% | M16402743 |
| `agent.birth` | 생년월일 | date | 100% | 1962.12.19 |
| `agent.relation` | 본인과의관계 | text | 100% | 부 |
| `대출금용도` | 대출금용도 | text | 100% | 투자 목적 |
| `대출기간` | 대출기간 | text | 100% |  |
| `customer.name` | 채무자(대출신청인) | text | 100% | 박찬연 |
| `설정최고액` | 설정최고액(대출금액의120%기재) | text | 100% |  |
| `설정자` | 설정자(소유자) | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.name2` | 성명(본인) | text | 100% | 박찬연 |
| `seal.signer` | 서명 | seal | 100% | 박찬연 |
| `sign.signer` | 서명 | signature | 100% | 현예지 |

### [필수]개인(신용)정보 제공동의서(서민맞춤대출용) (`hf112`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신청일로부터10년까지보유이용` | -신청일로부터10년까지보유·이용 | text | 100% |  |
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 강순준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 이민빈 |
| `seal.signer2` | 대리인성명 | seal | 100% | 최우빈 |
| `sign.signer2` | 대리인성명 | signature | 100% | 이민빈 |
| `이용목적` | 이용목적 | text | 100% | 결혼자금 |

### 개인(신용)정보 수집.이용 및 제공 동의서[필수적 동의](적격대출용) (`hf113`) — 키 37개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `금융사고조사분쟁해결민원처리` | ■금융사고조사,분쟁해결,민원처리 | text | 100% |  |
| `일반개인정보` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `제공받는자와동일` | -제공받는자와동일 | text | 100% |  |
| `공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보조회에동의하십니까` | 위고유식별정보조회에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인신용정보조회에동의하십니까` | 위개인신용정보조회에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `공사및하나은행` | 공사및(주)하나은행 | text | 100% | 카카오뱅크 |
| `미수채권소멸시까지` | 미수채권소멸시까지 | text | 100% |  |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 현예지 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 배우자성명 | text | 100% | 박찬연 |
| `seal.signer2` | 배우자성명 | seal | 100% | 현예지 |
| `sign.signer2` | 배우자성명 | signature | 100% | 박찬연 |
| `재산채무소득의총액납세실적` | 재산·채무·소득의총액,납세실적 | number | 100% | 60,000 |
| `신용등급및평점정보` | 신용등급및평점정보 | text | 100% |  |
| `일반개인정보2` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까2` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인신용정보제공에동의하십니까2` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `공사및하나은행2` | 공사및(주)하나은행 | text | 100% | 신한은행 |
| `공공정보등2` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까3` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인신용정보제공에동의하십니까3` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer3.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer3` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer3` | 본인성명 | signature | 100% | 강순준 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer4.name` | 배우자성명 | text | 100% | 박찬연 |
| `seal.signer4` | 배우자성명 | seal | 100% | 박찬연 |
| `sign.signer4` | 배우자성명 | signature | 100% | 강순준 |
| `재산채무소득의총액납세실적2` | 재산·채무·소득의총액,납세실적 | number | 100% | 134,990,000 |
| `신용등급및평점정보2` | 신용등급및평점정보 | text | 100% |  |

### 개인(신용)정보 수집.이용 제공 동의서(주택보유수 확인등) (`hf114`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `본인과배우자의주택보유수확인` | -본인과배우자의주택보유수확인 | text | 100% |  |
| `일반개인정보` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `일반개인정보2` | ■■일반개인정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 강순준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 배우자성명 | text | 100% | 박찬연 |
| `seal.signer2` | 배우자성명 | seal | 100% | 강순준 |
| `sign.signer2` | 배우자성명 | signature | 100% | 현예지 |

### [필수] 개인(신용)정보 수집이용, 제공 동의서(핀크생활비대출용) (`hf115`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `일반개인정보` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `금융사고조사분쟁해결민원처리` | ■금융사고조사,분쟁해결,민원처리 | text | 100% |  |
| `핀크` | (주)핀크[WWW.FINNQ.COM] | text | 100% |  |
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 강순준 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 강순준 |
| `seal.signer2` | 대리인성명 | seal | 100% | 강순준 |
| `sign.signer2` | 대리인성명 | signature | 100% | 이하지 |
| `이용목적` | 이용목적 | text | 100% | 주택구입 |

### [필수] 개인(신용)정보 수집이용, 제공 동의서(공무원대출) (`hf116`) — 키 19개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `금융거래관계의설정유지이행관리` | ■금융거래관계의설정·유지·이행·관리 | text | 100% |  |
| `금융사고조사분쟁해결민원처리` | ■금융사고조사,분쟁해결,민원처리 | text | 100% |  |
| `공무원연금공단이제공하는대출정보` | 공무원연금공단이제공하는대출정보 | text | 100% |  |
| `공무원연금공단` | 공무원연금공단 | text | 100% |  |
| `신용거래정보2` | ■신용거래정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 강순준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 최우빈 |
| `seal.signer2` | 대리인성명 | seal | 100% | 전영경 |
| `sign.signer2` | 대리인성명 | signature | 100% | 최우빈 |
| `이용목적` | 이용목적 | text | 100% | 타행 이체 |
| `customer.name` | 성명 | text | 100% | 박찬연 |

### [필수] 개인(신용)정보 수집이용, 제공 동의서(군인생활안정자금) (`hf117`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `금융거래관계의설정여부판단` | ■금융거래관계의설정여부판단 | text | 100% |  |
| `금융거래관계의설정유지이행관리` | ■금융거래관계의설정·유지·이행·관리 | text | 100% |  |
| `국군재정관리단` | 국군재정관리단 | text | 100% |  |
| `신용거래정보2` | ■신용거래정보 | text | 100% |  |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 현예지 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 하숙인 |
| `seal.signer2` | 대리인성명 | seal | 100% | 하숙인 |
| `sign.signer2` | 대리인성명 | signature | 100% |  |

### [필수] 개인(신용)정보 수집·이용·제공_동의서[가계여신_금융거래] (`hf118`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `금융사고조사분쟁해결민원처리` | -금융사고조사,분쟁해결,민원처리 | text | 100% |  |
| `공공정보등2` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 강순준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 이민빈 |
| `seal.signer2` | 대리인성명 | seal | 100% | 이민빈 |
| `sign.signer2` | 대리인성명 | signature | 100% | 표나경 |
| `성명국내거소신고번호` | 성명,국내거소신고번호 | text | 100% | 614692-6653479 |
| `있는정보` | 있는정보 | text | 100% |  |

### 필수 개인(신용)정보_수집·이용·제공_동의서[하나_사잇돌_중금리대출용] (`hf119`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `금융사고조사분쟁해결민원처리` | -금융사고조사,분쟁해결,민원처리 | text | 100% |  |
| `성명주소전화번호직장정보` | 성명,주소,전화번호,직장정보 | phone | 100% | 043-783-2775 |
| `고유식별정보` | ■고유식별정보 | text | 100% |  |
| `신용거래정보2` | ■신용거래정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 이욱유 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 박찬연 |
| `seal.signer2` | 대리인성명 | seal | 100% | 박찬연 |
| `sign.signer2` | 대리인성명 | signature | 100% | 이민빈 |

### 필수 개인(신용)정보수집·이용및제공동의서(하나원클릭모기지,원클릭전세론,e금리고정형적격) (`hf120`) — 키 27개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `금융사고조사분쟁해결민원처리` | -금융사고조사,분쟁해결,민원처리 | text | 100% |  |
| `성명생년월일주소전화번호` | 성명,생년월일,주소,전화번호 | date | 100% | 2025.10.22 |
| `공공정보등2` | ■공공정보등 | text | 100% |  |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 현예지 |
| `sign.signer` | 본인성명 | signature | 100% | 강순준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 이욱유 |
| `seal.signer2` | 대리인성명 | seal | 100% | 이욱유 |
| `sign.signer2` | 대리인성명 | signature | 100% | 이하지 |
| `성명생년월일주소전화번호2` | 성명,생년월일,주소,전화번호 | date | 100% | 2025.07.31 |
| `공공정보등3` | ■공공정보등 | text | 100% |  |
| `check.위개인정보수집이용에동의하십니까2` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `성명생년월일주소전화번호3` | 성명,생년월일,주소,전화번호 | date | 100% | 2025년 2월 19일 |
| `공공정보등4` | ■공공정보등 | text | 100% |  |
| `check.위개인정보제공에동의하십니까2` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `signer3.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer3` | 본인성명 | seal | 100% | 현예지 |
| `sign.signer3` | 본인성명 | signature | 100% | 박찬연 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer4.name` | 대리인성명 | text | 100% | 김소윤 |
| `seal.signer4` | 대리인성명 | seal | 100% | 우지현 |
| `sign.signer4` | 대리인성명 | signature | 100% | 김소윤 |
| `성명생년월일주소전화번호4` | 성명,생년월일,주소,전화번호 | date | 100% | 2025.02.27 |

### [필수] 개인(신용)정보 제3차 제공 동의서(우량주택전세론,군간부전세자금대출) (`hf121`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `서울보증보험` | 서울보증보험(주)(www.sgic.co.kr) | text | 100% |  |
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 강순준 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 이욱유 |
| `seal.signer2` | 대리인성명 | seal | 100% | 전영경 |
| `sign.signer2` | 대리인성명 | signature | 100% | 이욱유 |
| `이용목적` | 이용목적 | text | 100% | 만기 해지 |

### [필수] 개인(신용)정보 수집·이용 및 제공 동의서(전세자금대출 권리보험가입용) (`hf122`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `금융사고조사분쟁해결민원처리` | ■금융사고조사,분쟁해결,민원처리 | text | 100% |  |
| `정보질권통지업무상필요한정보` | 정보,질권통지업무상필요한정보 | text | 100% |  |
| `개인대출현황대출한도금액` | 개인대출현황(본건),대출한도금액 | number | 100% | 9,780,000 |
| `신용거래정보2` | ■신용거래정보 | text | 100% |  |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 이욱유 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 황보훈경 |
| `seal.signer2` | 대리인성명 | seal | 100% | 황보훈경 |
| `sign.signer2` | 대리인성명 | signature | 100% |  |
| `제공목적` | 제공목적 | text | 100% | 의료비 |
| `개인대출현황대출한도금액2` | 개인대출현황(본건),대출한도금액 | number | 100% | 100,000 |

### [필수] 개인(신용)정보 수집·이용 동의서 [전세자금대출-주택금융보증서용] (`hf123`) — 키 10개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신용능력정보` | ■신용능력정보 | text | 100% |  |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 현예지 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 옥영아 |
| `seal.signer2` | 대리인성명 | seal | 100% | 황보훈경 |
| `sign.signer2` | 대리인성명 | signature | 100% | 옥영아 |
| `금융사고조사분쟁해결민원처리` | -금융사고조사,분쟁해결,민원처리 | text | 100% |  |

### [필수] 개인(신용)정보 처리 동의서(전세자금대출 권리보험가입용) (`hf124`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `체결유지관리목적` | 체결·유지·관리목적 | text | 100% | 만기 해지 |
| `보험계약관련분쟁대응민원처리` | 보험계약관련분쟁대응,민원처리 | text | 100% |  |
| `질권통지업무수행` | 질권통지업무수행 | text | 100% |  |
| `정보등기타보험계약운영상필요정보` | 정보등기타보험계약운영상필요정보 | text | 100% |  |
| `신용거래정보2` | ■신용거래정보 | text | 100% |  |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 현예지 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### [필수] 개인(신용)정보 수집·이용 및 제공동의서[군간부전세자금대출기본),군간부월세자금대출] (`hf125`) — 키 19개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `customer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `금융거래관계의설정여부판단` | ■금융거래관계의설정여부판단 | text | 100% |  |
| `금융거래관계의설정유지이행관리` | ■금융거래관계의설정·유지·이행·관리 | text | 100% |  |
| `제공하는재직정보` | 제공하는재직정보 | text | 100% |  |
| `대출정보퇴직정보` | 대출정보,퇴직정보 | text | 100% |  |
| `국방부` | 국방부 | text | 100% |  |
| `신용거래정보2` | ■신용거래정보 | text | 100% |  |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 강순준 |
| `sign.signer` | 본인성명 | signature | 100% | 현예지 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 강순준 |
| `seal.signer2` | 대리인성명 | seal | 100% | 강순준 |
| `sign.signer2` | 대리인성명 | signature | 100% | 위나아 |
| `제공목적` | 제공목적 | text | 100% | 만기 해지 |

### [필수] 상품별 개인(신용)정보 수집·이용·제공 동의서[목돈안드는 행복전세,목돈 안다는 드림전세(집주인담보대출)용] (`hf126`) — 키 26개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `일반개인정보` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `금융사고조사분쟁해결민원처리` | ■금융사고조사,분쟁해결,민원처리 | text | 100% |  |
| `성명` | ■성명 | text | 100% |  |
| `개인식별정보외에고객이제공한정보` | ■개인식별정보외에고객이제공한정보 | text | 100% |  |
| `국토교통부` | 국토교통부 | text | 100% |  |
| `일반개인정보2` | ■일반개인정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 강순준 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer2` | 성명 | seal | 100% | 강순준 |
| `sign.signer2` | 성명 | signature | 100% | 박찬연 |
| `signer3.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer3` | 성명 | seal | 100% | 현예지 |
| `sign.signer3` | 성명 | signature | 100% | 박찬연 |
| `signer4.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer4` | 성명 | seal | 100% | 강순준 |
| `sign.signer4` | 성명 | signature | 100% | 박찬연 |
| `이용목적` | 이용목적 | text | 100% | 학자금 |
| `성명2` | ■성명 | text | 100% |  |
| `개인식별정보외에고객이제공한정보2` | ■개인식별정보외에고객이제공한정보 | text | 100% |  |

### 상품별 필수 개인(신용)정보 제공동의서(하나V-Plus대출) (`hf127`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신용보증기금` | 신용보증기금 | text | 100% |  |
| `신용도판단정보` | ■신용도판단정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 강순준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 옥영아 |
| `seal.signer2` | 대리인성명 | seal | 100% | 옥영아 |
| `sign.signer2` | 대리인성명 | signature | 100% | 민환은 |
| `이용목적` | 이용목적 | text | 100% | 학자금 |

### 필수 개인(신용)정보 수집, 이용 및 제공 동의서(소호여신) (`hf128`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `금융사고조사분쟁해결민원처리` | -금융사고조사,분쟁해결,민원처리 | text | 100% |  |
| `공공정보등2` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 위나아 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 위나아 |
| `seal.signer2` | 대리인성명 | seal | 100% | 위나아 |
| `sign.signer2` | 대리인성명 | signature | 100% | 김나진 |
| `이용목적` | 이용목적 | text | 100% | 학자금 |

### 필수 개인(신용)정보 수집, 이용 및 제공 동의서(법인여신) (`hf129`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `공공정보등` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `금융사고조사분쟁해결민원처리` | -금융사고조사,분쟁해결,민원처리 | text | 100% |  |
| `공공정보등2` | ■공공정보등 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 강순준 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 김연지 |
| `seal.signer2` | 대리인성명 | seal | 100% | 김연지 |
| `sign.signer2` | 대리인성명 | signature | 100% | 여기준 |

### 기업가치 및 기업정보 제공활용 동의서 (`hf130`) — 키 5개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `company.name` | 기업체명 | text | 100% | (주)유니온무역 |
| `signer.name` | 대표자 | text | 100% | 박찬연 |
| `seal.signer` | 대표자 | seal | 100% | 강순준 |
| `sign.signer` | 대표자 | signature | 100% | 박찬연 |

### 전세자금대출 이용 확약서(서울보증보험증권 담보 전세자금대출용) (`hf131`) — 키 5개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.birth` | 생년월일 | date | 100% | 900210 |
| `signer.name` | 명 | text | 100% | 박찬연 |
| `seal.signer` | 명 | seal | 100% | 최우빈 |
| `sign.signer` | 명 | signature | 100% | 박찬연 |

### 다주택처분확약서(서울보증보험) (`hf132`) — 키 7개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 본인 | text | 100% | 박찬연 |
| `대출계좌번호` | 대출계좌번호 | text | 100% | 039-306661-61881 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `signer.name` | 명 | text | 100% | 박찬연 |
| `seal.signer` | 명 | seal | 100% | 강순준 |
| `sign.signer` | 명 | signature | 100% | 박찬연 |

### 금융거래 정보제공 동의서(연대보증 면제 신용보증서 담보대출용) (`hf133`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.제공받는자` | 제공받는자 | checkbox | 100% | 지역신용보증재단 |
| `보증서담보대출입금전용계좌번호` | ▦보증서담보대출입금전용계좌번호 | text | 100% | 라가85871764 |
| `check.금융거래정보제공동의여부` | 금융거래정보제공동의여부 | checkbox | 100% | 보기2 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 법인명(채무자) | text | 100% | (주)유니온무역 |
| `seal.signer` | 법인명(채무자) | seal | 100% | (주)유니온무역 |
| `sign.signer` | 법인명(채무자) | signature | 100% | (주)스마트에프앤비 |
| `연대보증제도폐지에따른사후관리강화` | ▦연대보증제도폐지에따른사후관리강화 | text | 100% |  |

### 개인(신용)정보 수집.이용 동의서(매도인,무상거주인등 제3자용)(적격대출용) (`hf134`) — 키 17개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.해당되는` | ■해당되는 | checkbox | 100% | 세대원 |
| `check.수집ᆞ이용동의여부` | 수집ᆞ이용동의여부 | checkbox | 100% | 보기2 |
| `check.고유식별정보동의여부` | 고유식별정보동의여부 | checkbox | 100% | 보기2 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인 | text | 100% | 박찬연 |
| `seal.signer` | 본인 | seal | 100% | 박찬연 |
| `sign.signer` | 본인 | signature | 100% | 강순준 |
| `signer2.name` | 본인 | text | 100% | 박찬연 |
| `seal.signer2` | 본인 | seal | 100% | 이민빈 |
| `sign.signer2` | 본인 | signature | 100% | 현예지 |
| `signer3.name` | 본인 | text | 100% | 박찬연 |
| `seal.signer3` | 본인 | seal | 100% | 현예지 |
| `sign.signer3` | 본인 | signature | 100% | 박찬연 |
| `signer4.name` | 본인 | text | 100% | 박찬연 |
| `seal.signer4` | 본인 | seal | 100% | 현예지 |
| `sign.signer4` | 본인 | signature | 100% | 박찬연 |
| `개인식별정보` | ■개인식별정보 | text | 100% |  |

### 동의서(대출비용지급용) (`hf135`) — 키 7개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `check.한국주택금융공사보증료` | 한국주택금융공사보증료【출금된보증료는한국주택금융공사로납부됩니다.】 | checkbox | 100% | 한국주택금융공사 보증료【출금된 보증료는 한국주택금융공사로 납부됩니다.】 |
| `check.주택도시보증공사보증료` | 주택도시보증공사보증료【출금된보증료는주택도시보증공사로납부됩니다.】 | checkbox | 100% | 주택도시보증공사 보증료【출금된 보증료는 주택도시보증공사로 납부됩니다.】 |
| `check.수입인지대금출금된수입` | 수입인지대금【출금된수입인지대금은수입인지세금으로납부됩니다.】 | checkbox | 100% | 수입인지대금【출금된 수입인지대금은 수입인지세금으로 납부됩니다.】 |
| `check.국민주택채권매입비용` | 국민주택채권매입(할인)비용 | checkbox | 100% | 국민주택채권 매입(할인) 비용 |
| `check.기타` | 기타( | checkbox | 100% | 기타( |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |

### 《기업》차입신청서(한도내 개별/분할실행용) (`hf136`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.신청구분` | 신청구분 | checkbox | 100% | 연장(계좌번호 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `여신과목` | 여신과목 | text | 100% | 무역금융 |
| `신청금액` | 신청금액 | number | 100% | 44,360,000 |
| `기한` | 기한 | date | 100% | 2025년 7월 11일 |
| `금리` | 금리 | number | 100% | 30 |
| `자금용도` | 자금용도 | text | 100% | 사업자금 |
| `승인금액` | 승인금액(A) | number | 100% | 46,010,000 |
| `여신잔액` | 여신잔액(B) | number | 100% | 7,380,000 |
| `본건신청액` | 본건신청액(C) | text | 100% |  |
| `본건취급후` | 본건취급후 | text | 100% |  |
| `잔액` | 잔액(A-B-C) | number | 100% | 170,880,000 |

### 대출금 분할실행 신청서(에듀큐론용) (`hf137`) — 키 10개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `총대출한도` | 총대출한도(A) | number | 100% | 660,000원 |
| `기사용한도` | 기사용한도(B) | number | 100% | 650,000 |
| `분할실행신청액` | 분할실행신청액(C) | text | 100% |  |
| `미사용한도` | 미사용한도(A-B-C) | number | 100% | 50,950,000 |
| `비고` | 비고 | text | 100% | 학자금 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `분할실행신청액2` | ◦분할실행신청액 | text | 100% |  |
| `signer.name` | 채무자 | text | 100% | 박찬연 |
| `seal.signer` | 채무자 | seal | 100% | 강순준 |
| `sign.signer` | 채무자 | signature | 100% | 박찬연 |

### 대출금 수령위임동의서 (`hf138`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `용도` | 용도 | text | 100% | 계좌 정리 |
| `수령금액` | 수령금액 | number | 100% | 28,390,000 |
| `customer.name` | 예금주 | text | 100% | 박찬연 |
| `check.차주와의관계` | 차주와의관계 | checkbox | 100% | 차주를 대신하여 당타행 대출의 상환을 위임받은 자 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 수령위임인 | text | 100% | 박찬연 |
| `seal.signer` | 수령위임인 | seal | 100% | 이욱유 |
| `sign.signer` | 수령위임인 | signature | 100% | 박찬연 |
| `signer2.name` | 수령위임인의대리인 | text | 100% | 전영경 |
| `seal.signer2` | 수령위임인의대리인 | seal | 100% |  |
| `sign.signer2` | 수령위임인의대리인 | signature | 100% | 전영경 |

### 《기업》 지급보증거래 신청서(서면.전자 지급보증 겸용) (`hf139`) — 키 20개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `보증금액` | 보증금액 | number | 100% | 890,000 |
| `피보증채무의종류` | 피보증채무의종류 | text | 100% |  |
| `피보증채무의종류2` | 피보증채무의종류 | text | 100% |  |
| `seal.signer` | 인감(서명)대조 | seal | 100% | 박찬연 |
| `sign.signer` | 인감(서명)대조 | signature | 100% | 현예지 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 본인 | text | 100% | 박찬연 |
| `seal.signer2` | 본인 | seal | 100% | 강순준 |
| `sign.signer2` | 본인 | signature | 100% | 박찬연 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `상호` | •상호(성명) | text | 100% | (주)세진화학 |
| `사업자번호` | •사업자번호 | biz_no | 100% | 715-51-28572 |
| `주소` | •주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `전화번호및팩스번호` | •전화번호및팩스번호(또는E-Mail) | phone | 100% | 043-783-2775 |
| `계좌번호` | •계좌번호 | text | 100% | 987-662967-24251 |
| `특정채무` | 특정채무 | text | 100% |  |
| `보증` | 보증 | text | 100% |  |
| `근보증` | 근보증 | text | 100% |  |
| `예금주` | •예금주 | text | 100% |  |

### 매출채권 잔액 확인서 (`hf140`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `판매기업에대한정보` | 판매기업에대한정보 | text | 100% |  |
| `본인에대한정보` | 본인(구매기업)에대한정보 | text | 100% |  |
| `판매기업명` | 판매기업명 | text | 100% | 주식회사 가온화학 |
| `판매기업결제계좌` | 판매기업결제계좌 | text | 100% | 359-667676-98385 |
| `employer.name` | 회사명 | text | 100% | 주식회사 태평양무역 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `담당부서` | 담당부서 | text | 100% |  |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `입금은행명` | 입금은행명 | text | 100% | 농협은행 |
| `company.biz_no2` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `목록[].일련번호` | 일련번호 | text | 100% | 461355-7266243 |
| `목록[].매출채권금액` | 매출채권금액 | text | 100% | 138,450,000 |
| `목록[].발생일` | 발생일 | text | 100% | 2025.07.01 |
| `목록[].지급기일` | 지급기일 | text | 100% | 2027.06.16 |
| `목록[].다른권리존재여부` | 다른권리존재여부 | text | 100% |  |
| `목록[].특기사항` | 특기사항 | text | 100% | 생활자금 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `물품공급계약내용` | 물품공급계약내용[ | text | 100% | 의류 원단 |
| `계약일자` | 계약일자[..] | date | 100% | 2025.09.26 |
| `지급이확정된미지급매출채권내용` | 지급이확정된미지급매출채권내용 | text | 100% | 계좌 정리 |

### 매출채권 잔액 확인서(사전확인용) (`hf141`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `판매기업에대한정보` | 판매기업에대한정보 | text | 100% |  |
| `본인에대한정보` | 본인(구매기업)에대한정보 | text | 100% |  |
| `판매기업명` | 판매기업명 | text | 100% | 주식회사 다온상사 |
| `판매기업결제계좌` | 판매기업결제계좌 | text | 100% | 186-224269-99215 |
| `employer.name` | 회사명 | text | 100% | 주식회사 태평양무역 |
| `company.ceo` | 대표자 | text | 100% | 강순준 |
| `담당부서` | 담당부서 | text | 100% |  |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `입금은행명` | 입금은행명 | text | 100% | 하나은행 |
| `company.biz_no2` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `목록[].일련번호` | 일련번호 | text | 100% | 7431-3256 |
| `목록[].매출채권금액` | 매출채권금액 | text | 100% | 10,690,000 |
| `목록[].발생일` | 발생(예정)일 | text | 100% | 2025.04.12 |
| `목록[].지급기일` | 지급기일 | text | 100% | 2027.01.21 |
| `목록[].매출채권확정여부` | 매출채권확정여부 | text | 100% | 7,570,000원 |
| `목록[].다른권리존재여부` | 다른권리존재여부 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `물품공급계약내용` | 물품공급계약내용[ | text | 100% | 커피 원두 |
| `계약일자` | 계약일자[..] | date | 100% | 2024-07-06 |
| `미지급매출채권잔액` | 미지급매출채권잔액 | number | 100% | 72,400,000원 |

### 매출채권설정등기통지서 (`hf142`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].일련번호` | 일련번호 | text | 100% | 212021-3735477 |
| `목록[].발생일` | 발생일 | date | 100% | 2025.03.24 |
| `목록[].만기일` | 만기일 | date | 100% | 2029-03-21 |
| `목록[].채권금액` | 채권금액 | number | 100% | 7,570,000 |
| `목록[].비고` | 비고 | text | 100% | 전세자금 |
| `가계약내용` | 가.계약내용 | text | 100% | 의료비 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 은행 | text | 100% | 박찬연 |
| `seal.signer` | 은행 | seal | 100% | 강순준 |
| `sign.signer` | 은행 | signature | 100% | 현예지 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `절취선` | 절취선 | text | 100% |  |
| `절취선2` | 절취선 | text | 100% |  |

### 동산담보 제공 예정내역서(개별동산용) (`hf144`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.address` | 소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `보관장소명` | 보관장소명(주) | text | 100% |  |
| `목록[].제품명` | 제품명 | text | 100% | 기계 부품 |
| `목록[].식별번호` | 식별번호(주) | text | 100% | 801-156779-86345 |
| `목록[].모델명` | 모델명 | text | 100% | 전자부품 |
| `목록[].제조사` | 제조사 | text | 100% | 플라스틱 원료 |
| `목록[].제조년월` | 제조년월 | text | 100% |  |
| `목록[].비고` | 비고 | text | 100% | 학자금 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 채무자(담보제공자) | text | 100% | 박찬연 |
| `seal.signer` | 채무자(담보제공자) | seal | 100% | 박찬연 |
| `sign.signer` | 채무자(담보제공자) | signature | 100% | 이욱유 |

### 동산담보 제공 예정내역서(집합동산용) (`hf145`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.address` | 소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `보관장소명` | 보관장소명(주) | text | 100% |  |
| `목록[].동산의명칭` | 동산의명칭 | text | 100% | (주)유니온무역 |
| `목록[].규격` | 규격 | text | 100% | 철강 코일 |
| `목록[].수량` | 수량(주1) | text | 100% | 60 |
| `목록[].수량단위` | 수량단위 | text | 100% | 2 |
| `목록[].단가` | 단가(주2) | text | 100% | 2,070,000 |
| `목록[].제조사` | 제조사 | text | 100% | 산업용 펌프 |
| `목록[].비고` | 비고 | text | 100% | 급여 수령 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 채무자(담보제공자) | text | 100% | 박찬연 |
| `seal.signer` | 채무자(담보제공자) | seal | 100% | 박찬연 |
| `sign.signer` | 채무자(담보제공자) | signature | 100% | 현예지 |

### 《기업》금융거래확인서 (`hf149`) — 키 34개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].종별` | 종별 | text | 100% | 하나 단기채 펀드 |
| `목록[].용도` | 용도 | text | 100% | 하나 단기채 펀드 |
| `목록[].이율` | 이율 | text | 100% | 5 |
| `목록[].일자` | 일자 | text | 100% | 2025-03-14 |
| `목록[].금액` | 금액 | text | 100% | 110,000 |
| `목록[].잔액` | 잔액 | text | 100% | 530,000 |
| `목록[].대출기한` | 대출기한 | text | 100% | 2029-12-06 |
| `목록[].비고` | 비고 | text | 100% | 투자 목적 |
| `종류` | 종류 | text | 100% | 하나 단기채 펀드 |
| `선정일자` | 선정일자 | date | 100% | 2025.08.08 |
| `유효기간` | 유효기간 | text | 100% |  |
| `어음` | 어음 | text | 100% |  |
| `수표` | 수표 | text | 100% |  |
| `목록[].소재지` | 소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `목록[].소유자` | 소유자 | text | 100% |  |
| `목록[].채무자와의관계` | 채무자와의관계 | text | 100% |  |
| `목록[].종류` | 종류 | text | 100% | 하나 MMF |
| `목록[].수량` | 수량 | text | 100% | 1 |
| `목록[].감정가격` | 감정가격 | text | 100% |  |
| `목록[].감정일자` | 감정일자 | text | 100% | 2025.08.09 |
| `목록[].설정내용` | 설정내용(순위,금액) | text | 100% | 주택구입 |
| `대출종별` | 대출종별 | text | 100% |  |
| `연체발생일` | 연체발생일 | date | 100% | 2025.05.09 |
| `연체발생일2` | 연체발생일 | date | 100% | 2025-05-11 |
| `원금` | 원금 | number | 100% | 8,740,000 |
| `이자` | 이자 | number | 100% | 7,650,000원 |
| `연체정리일` | 연체정리일 | date | 100% | 2025-06-02 |
| `연체일수` | 연체일수 | text | 100% |  |
| `seal.signer` | (부)점장 | seal | 100% | 박찬연 |
| `sign.signer` | (부)점장 | signature | 100% | 이민빈 |
| `signer2.name` | 대표자명 | text | 100% | 박찬연 |
| `seal.signer2` | 대표자명 | seal | 100% | 박찬연 |
| `sign.signer2` | 대표자명 | signature | 100% | 강순준 |
| `company.name` | 기업체명 | text | 100% | (주)유니온무역 |

### 《기업》근저당권유용합의서 (`hf150`) — 키 29개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `근저당권설정내역` | 근저당권설정내역 | text | 100% |  |
| `채권최고액` | 채권최고액 | text | 100% |  |
| `customer.name` | 채무자 | text | 100% | 박찬연 |
| `근저당권설정자` | 근저당권설정자 | text | 100% |  |
| `seal.signer` | 인 | seal | 100% | 박찬연 |
| `sign.signer` | 인 | signature | 100% | 최우빈 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 채무자 | text | 100% | 박찬연 |
| `seal.signer2` | 채무자 | seal | 100% | 위나아 |
| `sign.signer2` | 채무자 | signature | 100% | 박찬연 |
| `signer3.name` | 후순위근저당권자 | text | 100% | 박찬연 |
| `seal.signer3` | 후순위근저당권자 | seal | 100% | 현예지 |
| `sign.signer3` | 후순위근저당권자 | signature | 100% | 박찬연 |
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer4.name` | 근저당권자 | text | 100% | 박찬연 |
| `seal.signer4` | 근저당권자 | seal | 100% | 이민빈 |
| `sign.signer4` | 근저당권자 | signature | 100% | 강순준 |
| `signer5.name` | 주택임차인 | text | 100% | 박찬연 |
| `seal.signer5` | 주택임차인 | seal | 100% | 박찬연 |
| `sign.signer5` | 주택임차인 | signature | 100% | 강순준 |
| `customer.birth2` | 생년월일 | date | 100% | 1997.05.14 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer6.name` | 근저당권설정자 | text | 100% | 박찬연 |
| `seal.signer6` | 근저당권설정자 | seal | 100% | 박찬연 |
| `sign.signer6` | 근저당권설정자 | signature | 100% | 현예지 |
| `customer.birth3` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.address3` | 주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |

### 《기업》무역어음인수·할인신청서 (`hf151`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `어음번호` | 어음번호 | text | 100% | 바다27884561 |
| `년` | 년 | text | 100% |  |
| `목록[].월` | 월 | text | 100% |  |
| `목록[].일` | 일 | text | 100% |  |
| `년2` | 년 | text | 100% |  |
| `년3` | 년 | number | 100% | 70 |
| `일` | 일 | text | 100% |  |
| `년4` | 년 | text | 100% |  |
| `지급기일` | 지급기일 | date | 100% | 2028-03-07 |
| `비` | 비 | text | 100% |  |
| `선적기일할인료율` | 선적기일할인료율 | number | 100% | 60 |
| `주소본인` | 주소:본인 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |

### 《기업》연대보증인(교체·면제)증서 (`hf152`) — 키 6개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].약정일자` | 약정일자 | date | 100% | 2025-03-27 |
| `목록[].거래약정서류명` | 거래약정서류명(또는어음채무내용) | text | 100% |  |
| `목록[].채무한도액` | 채무한도액 | text | 100% | 1,450,000 |
| `목록[].보증종류` | 보증종류 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `구연대보증인의보증채무내용` | ○구연대보증인의보증채무내용 | text | 100% | 계좌 정리 |

### 《기업》질권설정등록청구서 (`hf153`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].종류` | 종류 | text | 100% | 하나 단기채 펀드 |
| `목록[].기호` | 기호 | text | 100% |  |
| `목록[].번호` | 번호 | text | 100% | 9150-1354 |
| `목록[].액면금액` | 액면금액 | text | 100% | 340,000 |
| `목록[].매수` | 매수 | text | 100% | 12 |
| `목록[].총액` | 총액 | text | 100% | 32,610,000원 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `check.주권` | 주권 | checkbox | 100% | 주 권 |
| `check.사채권` | 사채권 | checkbox | 100% | 사채권 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `check.증권` | 증권 | checkbox | 100% | 증 권 |
| `check.예금` | 예금 | checkbox | 100% | 예 금 |
| `signer.name` | 명 | text | 100% | 박찬연 |
| `seal.signer` | 명 | seal | 100% | 박찬연 |
| `sign.signer` | 명 | signature | 100% | 강순준 |

### 차입신청서(무역금융용) (`hf154`) — 키 77개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `보증인_목록[].성명` | 성명 | text | 100% | 강순준 |
| `융자금산출근거_목록[].수량` | 수량 | text | 100% | 36 |
| `결정의견_목록[].수량` | 수량 | text | 100% | 24 |
| `금액` | 금액 | number | 100% | 129,380,000 |
| `check.과목` | 과목 | checkbox | 100% | 보기4 |
| `이자지급시기` | 이자지급시기 | number | 100% | 4,840,000원 |
| `보증인_목록[].연령` | 연령 | text | 100% |  |
| `LCNo` | L/C(계약서)No | text | 100% | 2279-1799 |
| `금액2` | 금액 | number | 100% | 16,380,000 |
| `품목` | 품목 | text | 100% | 포장재 |
| `수량` | 수량 | number | 100% | 24 |
| `보증인_목록[].직업및직위` | 직업및직위 | text | 100% |  |
| `보증인_목록[].차주와의관계` | 차주와의관계 | text | 100% |  |
| `보증인_목록[].월평균수입` | 월평균수입 | text | 100% |  |
| `보증인_목록[].실자산` | 실자산 | text | 100% |  |
| `선적기일` | 선적(납품)기일 | date | 100% | 2026.03.10 |
| `가격조건` | 가격조건 | text | 100% |  |
| `결제조건` | 결제조건 | text | 100% |  |
| `기타특수조건` | 기타특수조건 | text | 100% | 타행 이체 |
| `check.자금용도` | 자금용도 | checkbox | 100% | 원자재수입자금 |
| `기한` | 기한 | date | 100% | 2025.09.13 |
| `상환자원및방법` | 상환자원및방법 | text | 100% |  |
| `보증인_목록[].주소` | 주소(전화번호) | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `승인일자` | 승인일자 | date | 100% | 2025.04.22 |
| `승인기한` | 승인기한 | date | 100% | 2025.07.04 |
| `U` | U$ | text | 100% |  |
| `U2` | U$ | text | 100% |  |
| `U3` | U$ | text | 100% |  |
| `유효기일` | 유효기일 | date | 100% | 2029년 9월 22일 |
| `무역금융신청건포함명세_목록[].수입신용장발행` | 수입신용장발행 | text | 100% |  |
| `운전자금_목록[].상업어음` | 상업어음 | text | 100% |  |
| `시설자금_목록[].외화대출` | 외화대출 | amount | 100% | GBP 134,300 |
| `기타외화표시` | 기타외화표시 | text | 100% | 투자 목적 |
| `생산` | 생산 | text | 100% |  |
| `원자재수입` | 원자재수입 | text | 100% |  |
| `원자재구매` | 원자재구매 | text | 100% |  |
| `완제품구매` | 완제품구매 | text | 100% |  |
| `포괄금융` | 포괄금융 | text | 100% |  |
| `농수산물수출준비` | 농수산물수출준비 | text | 100% |  |
| `내국신용장발행` | 내국신용장발행 | text | 100% |  |
| `수입신용장발행` | 수입신용장발행 | text | 100% |  |
| `무역금융신청건포함명세_목록[].당행` | 당행 | text | 100% |  |
| `계` | 계 | text | 100% |  |
| `무역금융` | 무역금융 | text | 100% |  |
| `일반자금대출` | 일반자금대출 | text | 100% |  |
| `당좌대출` | 당좌대출 | text | 100% |  |
| `상업어음` | 상업어음 | text | 100% |  |
| `운전자금_목록[].당행` | 당행 | text | 100% |  |
| `소계` | 소계 | text | 100% |  |
| `일반자금대출2` | 일반자금대출 | text | 100% |  |
| `외화대출` | 외화대출 | amount | 100% | USD 199,700 |
| `시설자금_목록[].당행` | 당행 | text | 100% |  |
| `소계2` | 소계 | text | 100% |  |
| `무역금융관계` | 무역금융관계 | text | 100% |  |
| `기타원화표시` | 기타원화표시 | text | 100% | 본인 요청 |
| `기타외화표시2` | 기타외화표시 | text | 100% | 타행 이체 |
| `당행` | 당행 | text | 100% |  |
| `무역금융신청건포함명세_목록[].타행` | 타행 | text | 100% |  |
| `운전자금_목록[].타행` | 타행 | text | 100% |  |
| `시설자금_목록[].타행` | 타행 | text | 100% |  |
| `지급보증_목록[].타행` | 타행 | text | 100% |  |
| `타행` | 타행 | text | 100% |  |
| `금년도수출실적` | 금년도수출실적:(당행Nego액:)(예정액:) | text | 100% |  |
| `무역금융신청건포함명세_목록[].정기예금` | 정기예금 | text | 100% |  |
| `예금_목록[].정기예금` | 정기예금 | text | 100% |  |
| `부동산` | 부동산 | text | 100% |  |
| `기타` | 기타 | text | 100% | 계좌 정리 |
| `보통예금` | 보통예금 | text | 100% |  |
| `정기예금` | 정기예금 | text | 100% |  |
| `무역금융신청건포함명세_목록[].월말잔액` | 월말잔액 | number | 100% | 5,960,000원 |
| `계2` | 계 | text | 100% |  |
| `정기예금2` | 정기예금 | text | 100% |  |
| `예금_목록[].담보제공액` | 담보제공액 | text | 100% |  |
| `목록[].담보제공액` | 담보제공액 | text | 100% |  |
| `무역금융신청건포함명세_목록[].담보제공액` | 담보제공액 | text | 100% |  |
| `무역금융신청건포함명세_목록[].비고` | 비고 | text | 100% | 학자금 |
| `전년도실적` | 전년도실적 | text | 100% |  |

### 채권양도통지서(외국법인용)(K-biz파트너론) (`hf155`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 채무자(Obligor) | text | 100% | 박찬연 |
| `특기사항` | 특기사항(Specialnote) | text | 100% | 급여 수령 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `양도인주소` | 양도인(Assignor)주소(Address) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.name` | 상호(TradeName) | text | 100% | (주)유니온무역 |
| `양수인주소` | 양수인(Assignee)주소(Address) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `미화` | 미화(USD) | text | 100% |  |
| `달러` | 달러 | text | 100% |  |

### 여신거래용 인감명판 등 신고서 (`hf157`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 상호 | text | 100% | 주식회사 한빛패션 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `명판` | 명판 | text | 100% |  |
| `seal.signer` | 거래용인감또는서명(서명을병용한경우및외국인에한함) | seal | 100% | 박찬연 |
| `sign.signer` | 거래용인감또는서명(서명을병용한경우및외국인에한함) | signature | 100% | 강순준 |
| `목록[].변경후` | 변경후 | text | 100% | 의료비 |
| `signer2.name` | 대표자(본인자필) | text | 100% | 박찬연 |
| `seal.signer2` | 대표자(본인자필) | seal | 100% | 김소윤 |
| `sign.signer2` | 대표자(본인자필) | signature | 100% | 박찬연 |
| `신고사항` | 신고사항 | text | 100% |  |

### 위임장(하나골드신탁 만기 연장 접수용) (`hf158`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.address` | 주소 | text | 100% | 서울특별시 송파구 중대로 174, 119동 2202호 |
| `agent.relation` | 본인과의관계 | text | 100% | 부 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `signer.name` | ■기타※하나골드신탁만기연장외기타위임거래를구체적으로명시 | text | 100% | 박찬연 |
| `seal.signer` | ■기타※하나골드신탁만기연장외기타위임거래를구체적으로명시 | seal | 100% | 이욱유 |
| `sign.signer` | ■기타※하나골드신탁만기연장외기타위임거래를구체적으로명시 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 본인(위임인)성명 | text | 100% | 박찬연 |
| `seal.signer2` | 본인(위임인)성명 | seal | 100% | 이욱유 |
| `sign.signer2` | 본인(위임인)성명 | signature | 100% | 박찬연 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `소` | 소 | text | 100% |  |
| `customer.phone2` | 연락처 | phone | 100% | 010-5907-7253 |
| `본인의투자성향파악여부에대한의사결정` | -본인의투자성향파악여부에대한의사결정 | text | 100% |  |
| `본인의투자성향분석결과를확인하는행위` | -본인의투자성향분석결과를확인하는행위 | text | 100% |  |
| `하나골드신탁만기연장과관련한일체의사항` | ■하나골드신탁만기연장과관련한일체의사항 | text | 100% |  |

### [필수] 개인(신용)정보 수집·이용 동의서(일임형ISA) (`hf159`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신용능력정보` | ■신용능력정보 | text | 100% |  |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `금융사고조사분쟁해결민원처리` | -금융사고조사,분쟁해결,민원처리 | text | 100% |  |
| `직업에관한정보` | 직업에관한정보 | text | 100% |  |
| `연소득` | 연소득 | number | 100% | 16,990,000 |
| `agent.name` | 대리인 | text | 100% | 박영준 |
| `agent.name2` | 대리인 | text | 100% | 박영준 |

### 계약대상자확인서(일임형ISA용) (`hf160`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `가입대상` | 가입대상 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `agent.name` | 대리인 | text | 100% | 박영준 |
| `agent.name2` | 대리인 | text | 100% | 박영준 |
| `가입대상2` | 가입대상 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `agent.name3` | 대리인 | text | 100% | 박영준 |
| `agent.name4` | 대리인 | text | 100% | 박영준 |

### 위임장 (특정금전신탁용) (`hf161`) — 키 17개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `agent.relation` | 본인과의관계 | text | 100% | 부 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `signer.name` | ■기타※신규외기타위임거래를구체적으로명시1.2.3. | text | 100% | 박찬연 |
| `seal.signer` | ■기타※신규외기타위임거래를구체적으로명시1.2.3. | seal | 100% | 이민빈 |
| `sign.signer` | ■기타※신규외기타위임거래를구체적으로명시1.2.3. | signature | 100% | 강순준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `소` | 소 | text | 100% |  |
| `처` | 처 | text | 100% |  |
| `signer2.name` | 직원명 | text | 100% | 박찬연 |
| `seal.signer2` | 직원명 | seal | 100% | 박찬연 |
| `sign.signer2` | 직원명 | signature | 100% | 강순준 |
| `본인의투자성향파악여부에대한의사결정` | -본인의투자성향파악여부에대한의사결정 | text | 100% |  |
| `본인의투자성향분석결과를확인하는행위` | -본인의투자성향분석결과를확인하는행위 | text | 100% |  |
| `특정금전신탁상품가입과관련한일체의사항` | ■특정금전신탁상품가입과관련한일체의사항 | text | 100% |  |

### ISA계약만기연장 확인서 (`hf162`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 고객명(고객번호) | text | 100% | 박찬연 |
| `ISA계좌번호` | ISA계좌번호 | text | 100% | 249-348810-98202 |
| `연장전계약만기일` | 연장전계약만기일 | date | 100% | 2026년 6월 16일 |
| `둥록점명` | 둥록점명(등록점번호) | text | 100% |  |
| `연장후계약만기일` | 연장후계약만기일 | date | 100% | 2028.06.30 |
| `상담직원명` | 상담직원명(직원번호) | text | 100% |  |
| `customer.name2` | 고객명(고객번호) | text | 100% | 박찬연 |
| `ISA계좌번호2` | ISA계좌번호 | text | 100% | 273-145800-48052 |
| `연장전계약만기일2` | 연장전계약만기일 | date | 100% | 2030-02-10 |
| `둥록점명2` | 둥록점명(등록점번호) | text | 100% |  |
| `연장후계약만기일2` | 연장후계약만기일 | date | 100% | 2028-08-10 |
| `상담직원명2` | 상담직원명(직원번호) | text | 100% |  |

### 위임장(일임형 개인종합자산관리계좌(ISA)용) (`hf163`) — 키 20개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.address` | 주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `agent.relation` | 본인과의관계 | text | 100% | 부 |
| `customer.phone` | 연락처 | phone | 100% | 010-7321-8870 |
| `signer.name` | ■기타※신규외기타위임거래를구체적으로명시1.2.3. | text | 100% | 박찬연 |
| `seal.signer` | ■기타※신규외기타위임거래를구체적으로명시1.2.3. | seal | 100% | 현예지 |
| `sign.signer` | ■기타※신규외기타위임거래를구체적으로명시1.2.3. | signature | 100% | 강순준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.birth2` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.phone2` | 연락처 | phone | 100% | 010-5907-7253 |
| `손실가능` | 손실가능 | text | 100% |  |
| `본인의투자성향파악여부에대한의사결정` | -본인의투자성향파악여부에대한의사결정 | text | 100% |  |
| `본인의투자성향분석결과를확인하는행위` | -본인의투자성향분석결과를확인하는행위 | text | 100% |  |
| `agent.name` | 대리인 | text | 100% | 강석호 |
| `seal.signer2` | 사용인감,일임형ISA위임장 | seal | 100% | 박찬연 |
| `sign.signer2` | 사용인감,일임형ISA위임장 | signature | 100% | 강순준 |
| `seal.signer3` | 인감도장,일임형ISA위임장 | seal | 100% | 박찬연 |
| `sign.signer3` | 인감도장,일임형ISA위임장 | signature | 100% | 강순준 |

### 상속예금 명의변경(지급) 의뢰서 및 손해담보 확약서(상속예금 지급 위임장 겸용) (`hf001`) — 키 34개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 예금주 | text | 100% | 박찬연 |
| `check.지급구분` | 지급구분 | checkbox | 100% | 소액지급 ( |
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `사망일자` | 사망일자 | date | 100% | 2025년 4월 7일 |
| `목록[].상품명` | 상품명 | text | 100% | 플라스틱 원료 |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 885-942883-70337 |
| `목록[].금액` | 금액 | text | 100% | 850,000 |
| `check.보기1` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기12` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기13` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기14` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기15` | 보기1 | checkbox | 100% | 보기1 |
| `check.명의변경` | 명의변경 | checkbox | 100% | □ |
| `취급점` | 취급점 | text | 100% | 둔산지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `기타특약사항` | 기타특약사항 | text | 100% | 본인 요청 |
| `check.주된상속인` | 주된상속인(소득귀속인) | checkbox | 100% | 위임(별도 위임장 작성) |
| `check.상속인` | 상속인 | checkbox | 100% | 본인 |
| `check.상속인2` | 상속인 | checkbox | 100% | 위임(주된 상속인 앞) |
| `check.상속인3` | 상속인 | checkbox | 100% | 본인 |
| `check.상속인4` | 상속인 | checkbox | 100% | 위임(주된 상속인 앞) |
| `check.상속인5` | 상속인 | checkbox | 100% | 위임(주된 상속인 앞) |
| `목록[].성명` | 성명 | text | 100% | 박찬연 |
| `목록[].생년월일` | 생년월일 | text | 100% | 2026.01.28 |
| `목록[].연락처` | 연락처 | text | 100% | 010-5907-7253 |
| `목록[].예금잔액` | 예금잔액 | text | 100% | 6,440,000 |
| `목록[].미지급사유주1` | 미지급사유주1 | text | 100% | 주거래하나 통장 |
| `목록[].상속인확인` | 상속인확인 | text | 100% |  |
| `signer.name` | 확인담당자 | text | 100% | 박찬연 |
| `seal.signer` | 확인담당자 | seal | 100% | 박찬연 |
| `sign.signer` | 확인담당자 | signature | 100% | 현예지 |
| `signer2.name` | 확인책임자 | text | 100% | 박찬연 |
| `seal.signer2` | 확인책임자 | seal | 100% | 현예지 |
| `sign.signer2` | 확인책임자 | signature | 100% | 박찬연 |

### 은행거래신청서(영문) (`hf002`) — 키 68개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.email` | E-mail | text | 100% | chanyeon363@naver.com |
| `Home` | Home | text | 100% |  |
| `Office` | Office | text | 100% |  |
| `Home2` | Home | text | 100% |  |
| `Office2` | Office | text | 100% |  |
| `Occupation` | Occupation | text | 100% |  |
| `Occupation2` | Occupation | text | 100% |  |
| `Payday` | Payday | text | 100% |  |
| `Nochangeincustomerinformation` | Nochangeincustomerinformation | text | 100% |  |
| `RequestforSMSmaturitynotice` | RequestforSMSmaturitynotice | text | 100% |  |
| `갋` | 갋 | text | 100% |  |
| `갋2` | 갋 | text | 100% |  |
| `갋3` | 갋 | text | 100% |  |
| `목록[].FixedFloating` | FixedFloating(mth) | text | 100% |  |
| `AccountItem` | AccountItem | text | 100% |  |
| `PaymentDeadline` | PaymentDeadline | text | 100% |  |
| `mthcapitalizationLimit` | ()mthcapitalizationLimit | amount | 100% | 6,060,000 |
| `mthcapitalizationLimit2` | ()mthcapitalizationLimit | amount | 100% | 21,570,000 |
| `mthcapitalizationLimit3` | ()mthcapitalizationLimit | amount | 100% | 70,210,000 |
| `check.Irequestagr` | Irequest/agreetoaninquiryofmyfina | checkbox | 100% | I request/agree to an inquiry of my fina |
| `check.Ishallraisen` | Ishallraisenoobjectiontoaset-off | checkbox | 100% | I shall raise no objection to a set-off  |
| `check.Ihavereceive` | Ihavereceivedanexplanationthatcust | checkbox | 100% | I have received an explanation that cust |
| `Bankbook` | Bankbook | text | 100% |  |
| `Annual` | Annual | text | 100% |  |
| `Bankbook2` | Bankbook | text | 100% |  |
| `Annual2` | Annual | text | 100% |  |
| `Annual3` | Annual | text | 100% |  |
| `Bankbook3` | Bankbook | text | 100% |  |
| `WithdrawalAccount` | WithdrawalAccount[ | text | 100% |  |
| `Applicant` | Applicant | text | 100% | 미래메디칼 |
| `YYYY` | YYYY | text | 100% |  |
| `account` | AccountNo. | account_no | 100% | 000-287736-52424 |
| `DateofOpening` | DateofOpening | date | 100% | 2024년 5월 20일 |
| `Category` | Category | text | 100% |  |
| `Time` | Time | text | 100% |  |
| `EmployeeNumber` | EmployeeNumber | text | 100% |  |
| `NewWithdrawalAccountAddition` | NewWithdrawalAccountAddition | text | 100% |  |
| `YesNo` | YesNo | text | 100% | 6847-6957 |
| `Statusofassets` | Statusofassets | amount | 100% |  |
| `Sourcesoffinancing` | Sourcesoffinancing | text | 100% |  |
| `YesNo2` | YesNo | text | 100% | 353-944363-95188 |
| `BusinessName` | BusinessName | text | 100% |  |
| `Industry` | Industry(BusinessType/Item) | text | 100% |  |
| `BusinessRegistrationNo` | BusinessRegistrationNo. | biz_no | 100% | 311-09-83199 |
| `BusinessCommencementDate` | BusinessCommencementDate | date | 100% | 2025.02.18 |
| `DepositAccount` | DepositAccount | text | 100% |  |
| `customer.name` | Name | text | 100% | 박찬연 |
| `RelationtoPrincipal` | RelationtoPrincipal | text | 100% |  |
| `customer.birth` | DateofBirth | date | 100% | 1990.02.10 |
| `customer.address` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `PhoneNo` | PhoneNo. | phone | 100% | 010-5907-7253 |
| `AccountItem2` | AccountItem | text | 100% |  |
| `PaymentDeadline2` | PaymentDeadline | text | 100% |  |
| `PhoneBanking` | PhoneBanking | text | 100% |  |
| `Applicant2` | Applicant | text | 100% | (주)유니온물산 |
| `Applicant3` | Applicant | text | 100% | (주)대성화학 |
| `Publicfeepayment` | Publicfeepayment | amount | 100% |  |
| `Other` | Other() | text | 100% |  |
| `Applicant4` | Applicant | text | 100% | 주식회사 동방메디칼 |
| `thedateofrenewal` | thedateofrenewal | date | 100% |  |
| `Depositor` | Depositor | text | 100% |  |
| `Proxy` | Proxy | text | 100% |  |
| `Delegator` | Delegator(Depositor) | text | 100% |  |
| `account2` | AccountNo. | account_no | 100% | 000-287736-52424 |
| `DateofOpening2` | DateofOpening | date | 100% | 2024.11.18 |
| `Category2` | Category | text | 100% |  |
| `Time2` | Time | text | 100% |  |
| `EmployeeNumber2` | EmployeeNumber | text | 100% |  |

### 은행거래신청서 (`hf003`) — 키 83개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].통장발행` | 통장발행 | text | 100% |  |
| `만기안내문자통지신청` | 만기안내문자통지신청 | date | 100% | 2029-06-22 |
| `목록[].갋` | 갋 | text | 100% |  |
| `갋` | 갋 | text | 100% |  |
| `갋2` | 갋 | text | 100% |  |
| `갋3` | 갋 | text | 100% |  |
| `갋_목록[].전화` | 전화 | text | 100% | 010-5907-7253 |
| `정기자유` | 정기자유 | text | 100% |  |
| `정기자유2` | 정기자유 | text | 100% |  |
| `목록[].확정형연동형` | 확정형연동형(개월) | text | 100% |  |
| `정기자유3` | 정기자유 | text | 100% |  |
| `정기자유4` | 정기자유 | text | 100% |  |
| `정기자유5` | 정기자유 | text | 100% |  |
| `정기자유6` | 정기자유 | text | 100% |  |
| `customer.email` | E-mail | text | 100% | chanyeon363@naver.com |
| `customer.email2` | E-mail | text | 100% | soonjun606@gmail.com |
| `customer.email3` | E-mail | text | 100% | chanyeon363@naver.com |
| `한도` | 한도:₩..~.. | number | 100% | 31,030,000 |
| `한도2` | 한도:₩..~.. | number | 100% | 890,000 |
| `한도3` | 한도:₩..~.. | number | 100% | 92,700,000 |
| `customer.name_en` | 영문명 | text | 100% | KANG SOONJUN |
| `customer.email4` | 이메일 | text | 100% | chanyeon363@naver.com |
| `자택` | 자택 | text | 100% |  |
| `employer.name` | 직장 | text | 100% | 주식회사 태평양무역 |
| `자택2` | 자택 | text | 100% |  |
| `employer.name2` | 직장 | text | 100% | 주식회사 태평양무역 |
| `급여일` | 급여일 | date | 100% | 2025년 6월 24일 |
| `고객정보변경없음` | 고객정보변경없음 | text | 100% |  |
| `자동이체계좌번호` | 자동이체계좌번호 | text | 100% | 323-274459-25590 |
| `과목명` | 과목명 | text | 100% | 시설자금대출 |
| `계약금액` | 계약(확인)금액 | number | 100% | 5,950,000 |
| `지급기일` | 지급기일 | date | 100% | 2027.02.05 |
| `check.비과세종합저축재형저축` | 비과세종합저축/재형저축/주택청약상품의계약금액/한도/중복 | checkbox | 100% | 비과세종합저축 / 재형저축 / 주택청약상품의 계약금액 / 한도 / 중복  |
| `check.귀행에대한제대출금보증채` | 귀행에대한제대출금,보증채무,신용카드채무에대하여변제기가도래하 | checkbox | 100% | 귀행에 대한 제 대출금, 보증채무, 신용카드채무에 대하여 변제기가 도래하 |
| `check.본인은금융지주회사법제4` | 본인은금융지주회사법제48조의2에근거하여하나금융그룹내지주사및자 | checkbox | 100% | 본인은 금융지주회사법 제48조의2에 근거하여 하나금융그룹내 지주사 및 자 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `연원가식` | 연원가식 | text | 100% |  |
| `연원가식2` | 연원가식 | text | 100% |  |
| `연원가식3` | 연원가식 | text | 100% |  |
| `출금계좌` | 출금계좌[ | text | 100% | 375-306864-77229 |
| `customer.name` | 신청인 | text | 100% | 박찬연 |
| `account` | 계좌번호 | account_no | 100% | 996-316834-99379 |
| `최초거래일` | 최초거래일 | date | 100% | 2025.02.01 |
| `신규일` | 신규일 | date | 100% | 2025.09.08 |
| `입금액` | 입금(수탁)액 | number | 100% | 38,430,000 |
| `종별` | 종별 | text | 100% | 하나의정기예금 |
| `권유직원번호` | 권유직원번호 | text | 100% | 739264-5706503 |
| `이용자ID` | 이용자ID | text | 100% | 484-601636-96779 |
| `인터넷스마트폰뱅킹` | 인터넷/스마트폰뱅킹(1일:원)(1회:원) | text | 100% |  |
| `예아니오` | 예아니오 | text | 100% |  |
| `company.name` | 상호명 | text | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 261-82-53694 |
| `개업년월일` | 개업년월일 | date | 100% | 2025년 1월 5일 |
| `account2` | 입금계좌 | account_no | 100% | 774-646914-96117 |
| `agent.name` | 성명 | text | 100% | 박영준 |
| `agent.relation` | 본인과의관계 | text | 100% | 부 |
| `agent.birth` | 생년월일 | date | 100% | 1962.12.19 |
| `agent.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `agent.phone` | 전화번호 | phone | 100% | 010-6515-4769 |
| `자동이체계좌번호2` | 자동이체계좌번호 | text | 100% | 740-569557-60427 |
| `과목명2` | 과목명 | text | 100% | 시설자금대출 |
| `계약금액2` | 계약(확인)금액 | number | 100% | 18,550,000 |
| `지급기일2` | 지급기일 | date | 100% | 2028-12-15 |
| `원1회` | 원)(1회 | number | 100% | 100,000 |
| `customer.name2` | 신청인 | text | 100% | 박찬연 |
| `customer.name3` | 신청인 | text | 100% | 박찬연 |
| `재산현황` | 재산현황 | text | 100% |  |
| `1000억원이상` | 1,000억원이상 | text | 100% |  |
| `아니오실제소유자성명` | 아니오(실제소유자성명 | text | 100% | 박찬연 |
| `카드대금결제` | 카드대금결제 | number | 100% | 9,380,000 |
| `부동산양도소득` | 부동산양도소득 | number | 100% | 7,840,000원 |
| `귀금속판매상` | 귀금속판매상 | text | 100% |  |
| `1` | [신청상품]1 | text | 100% |  |
| `customer.name4` | 신청인 | text | 100% | 박찬연 |
| `customer.name5` | 예금주 | text | 100% | 박찬연 |
| `agent.name2` | 대리인 | text | 100% | 박영준 |
| `customer.name6` | 위임인(예금주) | text | 100% | 박찬연 |
| `account3` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `최초거래일2` | 최초거래일 | date | 100% | 2025-03-07 |
| `신규일2` | 신규일 | date | 100% | 2025.08.08 |
| `입금액2` | 입금(수탁)액 | number | 100% | 70,480,000원 |
| `종별2` | 종별 | text | 100% | 하나 정기예금 |
| `권유직원번호2` | 권유직원번호 | text | 100% | 330069-0817452 |

### 보호예수품 반환 의뢰서 (`hf004`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `일련번호` | 일련번호 | text | 100% | 964-747488-99943 |
| `check.예수방법` | 예수방법 | checkbox | 100% | 봉함예수 |
| `예수품명` | 예수품명 | text | 100% | PCB 기판 |
| `예수금액` | 예수금액 | number | 100% | 154,470,000 |
| `증권번호` | 증권번호 | text | 100% | 884681-2926582 |
| `예수수량` | 예수수량 | number | 100% | 2 |
| `signer.name` | 성명(상호명) | text | 100% | 박찬연 |
| `seal.signer` | 성명(상호명) | seal | 100% | 박찬연 |
| `sign.signer` | 성명(상호명) | signature | 100% | 강순준 |
| `customer.address` | 주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `customer.birth` | 생년월일(사업자등록번호) | date | 100% | 1990.02.10 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 보호예수 의뢰서 (`hf005`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.예수종류` | 예수종류 | checkbox | 100% | 봉함예수 |
| `예수수량` | 예수수량 | number | 100% | 3 |
| `check.만기일자` | 만기일자 | checkbox | 100% | 예적금 만기일( |
| `예수품명` | 예수품명 | text | 100% | 철강 코일 |
| `예수금액` | 예수금액 | number | 100% | 99,200,000 |
| `증권번호` | 증권번호 | text | 100% | 803-587953-68618 |
| `check.수령방법` | 수령방법 | checkbox | 100% | 영업점 |
| `signer.name` | 성명(상호명) | text | 100% | 박찬연 |
| `seal.signer` | 성명(상호명) | seal | 100% | 이욱유 |
| `sign.signer` | 성명(상호명) | signature | 100% | 박찬연 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.birth` | 생년월일(사업자등록번호) | date | 100% | 1990.02.10 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `취급점` | 취급점 | text | 100% | 둔산지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 자동이체 신청서 (`hf006`) — 키 50개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 예금자성명 | text | 100% | 박찬연 |
| `seal.signer` | 예금자성명 | seal | 100% | 김소윤 |
| `sign.signer` | 예금자성명 | signature | 100% | 현예지 |
| `account` | 출금계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `변경후출금계좌번호` | 변경후출금계좌번호 | text | 100% | 투자 목적 |
| `check.신청구분` | 신청구분( | checkbox | 100% | 해지 |
| `check.이체일이휴일인경우` | [당행요구불계좌이체,타행자동이체]이체일이휴일인경우 | checkbox | 100% | 전 영업일 |
| `check.신청구분2` | 신청구분( | checkbox | 100% | 변경 |
| `check.이체일이휴일인경우2` | [당행요구불계좌이체,타행자동이체]이체일이휴일인경우 | checkbox | 100% | 익 영업일 이체를 신청합니다. |
| `은행` | 은행 | text | 100% | 우리은행 |
| `지급인자내용` | 지급인자내용 | text | 100% | 투자 목적 |
| `은행2` | 은행 | text | 100% | 하나은행 |
| `지급인자내용2` | 지급인자내용 | text | 100% | 타행 이체 |
| `check.자동이체기간만료SMS통지` | 자동이체기간만료SMS통지( | checkbox | 100% | 미신청 |
| `목록[].예금주명` | 예금주명 | text | 100% |  |
| `check.자동이체기간만료SMS통지2` | 자동이체기간만료SMS통지( | checkbox | 100% | 미신청 |
| `목록[].이체일` | 이체일 | date | 100% | 2024.11.01 |
| `목록[].이체주기` | 이체주기(일☞주☞월☞년) | text | 100% |  |
| `목록[].이체금액` | 이체금액 | number | 100% | 14,250,000 |
| `입금인자내용` | 입금인자내용 | text | 100% | 주택구입 |
| `입금인자내용2` | 입금인자내용 | text | 100% | 계좌 정리 |
| `check.수수료포함출금` | 수수료포함출금( | checkbox | 100% | 신청 |
| `date` | 일자 | date | 100% | 2026년 1월 31일 |
| `check.수수료포함출금2` | 수수료포함출금( | checkbox | 100% | 미신청 |
| `date2` | 일자 | date | 100% | 2026년 1월 31일 |
| `date3` | 년월일 | date | 100% | 2026년 1월 31일 |
| `date4` | 년월일 | date | 100% | 2026년 1월 31일 |
| `account2` | 입금계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.만기이연시선택` | [정액적립식]만기이연시선택 | checkbox | 100% | 만기일 |
| `check.갱신구분` | 갱신구분 | checkbox | 100% | 원리금지급 |
| `check.계약서류수령방법` | 계약서류*수령방법 | checkbox | 100% | 별도 연락처로 수령( |
| `account3` | 입금계좌 | account_no | 100% | 000-287736-52424 |
| `check.자동이체정지` | 자동이체정지 | checkbox | 100% | 해제 |
| `구분` | 구분 | text | 100% |  |
| `관리비지로공과금기타_목록[].수납기관` | 수납기관(아파트,상가) | text | 100% |  |
| `수납기관` | 수납기관(아파트,상가) | text | 100% |  |
| `관리비지로공과금기타_목록[].납부자번호` | 납부자번호(동,호수,수용가번호,등) | text | 100% | 3065-6312 |
| `납부자번호` | 납부자번호(동,호수,수용가번호,등) | text | 100% | 199125-7997364 |
| `관리비지로공과금기타_목록[].지로번호기관코드` | 지로번호/기관코드 | text | 100% | 60962 |
| `지로번호기관코드` | 지로번호/기관코드 | number | 100% | 0603 |
| `관리비지로공과금기타_목록[].납부희망일` | 납부희망일 | text | 100% | 2025.02.06 |
| `date5` | 작성일 | date | 100% | 2026년 1월 31일 |
| `check.계좌간자동이체` | 계좌간자동이체( | checkbox | 100% | 납부자 자동이체 |
| `check.만기해지자동이체` | 만기해지자동이체( | checkbox | 100% | 변경 |
| `check.자동갱신자동이체` | 자동갱신(재예치)자동이체( | checkbox | 100% | 해지 |
| `check.기타자동이체` | 기타자동이체( | checkbox | 100% | 변경 |
| `check.계좌번호` | 계좌번호 | checkbox | 100% | 미적용 |
| `check.조회` | 조회 | checkbox | 100% | 일괄해지 1 |
| `check.고객명` | 고객명 | checkbox | 100% | 미적용 |

### 질권실행 의뢰서(수신_제3자 질권용) (`hf007`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].예금종류` | 예금종류 | text | 100% | 하나 적금 |
| `목록[].예금주` | 예금주(위탁자/수탁자) | text | 100% |  |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 266-088931-03327 |
| `목록[].예금액` | 예금액 | number | 100% | 6,050,000 |
| `목록[].만기일주1` | 만기일주1 | date | 100% | 2027.12.30 |
| `목록[].질권설정금액` | 질권설정금액 | text | 100% | 260,000원 |
| `목록[].변제기일주1` | 변제기일주1 | date | 100% | 2029년 7월 9일 |
| `signer.name` | 성명(업체명) | text | 100% | 박찬연 |
| `seal.signer` | 성명(업체명) | seal | 100% | 이욱유 |
| `sign.signer` | 성명(업체명) | signature | 100% | 현예지 |
| `customer.birth` | 생년월일(사업자등록번호) | date | 100% | 970514 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 질권해지 통지서(수신_제3자 질권용) (`hf008`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].예금종류` | 예금종류 | text | 100% | 하나 적금 |
| `목록[].예금주` | 예금주(위탁자/수탁자) | text | 100% |  |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 538-829499-23588 |
| `목록[].예금액` | 예금액 | text | 100% | 5,060,000원 |
| `목록[].만기일` | 만기일 | date | 100% | 2028.07.27 |
| `목록[].질권설정금액` | 질권설정금액 | text | 100% | 3,040,000원 |
| `목록[].변제기일` | 변제기일 | date | 100% | 2026년 12월 29일 |
| `signer.name` | 성명(업체명) | text | 100% | 박찬연 |
| `seal.signer` | 성명(업체명) | seal | 100% | 김나우 |
| `sign.signer` | 성명(업체명) | signature | 100% | 박찬연 |
| `customer.birth` | 생년월일(사업자등록번호) | date | 100% | 1990-02-10 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 질권설정 승낙의뢰서(수신_제3자 질권용) (`hf009`) — 키 26개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].예금종류` | 예금종류 | text | 100% | 급여하나 통장 |
| `목록[].예금주` | 예금주(위탁자/수탁자) | text | 100% |  |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 903-550493-89454 |
| `목록[].금액주1` | 금액주1 | number | 100% | 720,000 |
| `목록[].만기일주2` | 만기일주2 | date | 100% | 2026년 10월 23일 |
| `목록[].질권설정금액` | 질권설정금액 | number | 100% | 470,000원 |
| `목록[].변제기일주2` | 변제기일주2 | date | 100% | 2030.02.18 |
| `signer.name` | 성명(업체명) | text | 100% | 박찬연 |
| `seal.signer` | 성명(업체명) | seal | 100% | 이욱유 |
| `sign.signer` | 성명(업체명) | signature | 100% | 박찬연 |
| `customer.birth` | 생년월일(사업자등록번호) | date | 100% | 1990-02-10 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `signer2.name` | 성명(업체명) | text | 100% | 박찬연 |
| `seal.signer2` | 성명(업체명) | seal | 100% | 박찬연 |
| `sign.signer2` | 성명(업체명) | signature | 100% | 이민빈 |
| `customer.birth2` | 생년월일(사업자등록번호) | date | 100% | 1990-02-10 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.phone2` | 연락처 | phone | 100% | 010-5907-7253 |
| `signer3.name` | 질권설정자(예금주) | text | 100% | 박찬연 |
| `seal.signer3` | 질권설정자(예금주) | seal | 100% | 현예지 |
| `sign.signer3` | 질권설정자(예금주) | signature | 100% | 박찬연 |
| `signer4.name` | 질권자 | text | 100% | 박찬연 |
| `seal.signer4` | 질권자 | seal | 100% | 강순준 |
| `sign.signer4` | 질권자 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 주식(사채)납입금 수납대행의뢰서(보관증명서 발급의뢰서 겸용) (`hf010`) — 키 23개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `책임자` | 책임자(관리자) | text | 100% |  |
| `영업점장` | 영업점장 | text | 100% |  |
| `date` | 납입기일 | date | 100% | 2026년 1월 31일 |
| `check.주식납입금수납` | 주식납입금수납 | checkbox | 100% | 신주발행 |
| `check.사채납입금수납` | 사채납입금수납 | checkbox | 100% | 사채발행 |
| `주식수` | 주식수 | number | 100% | 1 |
| `발행가액` | 발행가액(1주당) | number | 100% | 83,040,000 |
| `발행주식총수` | 발행주식총수 | number | 100% | 36 |
| `주주배정` | 주주배정 | number | 100% | 3 |
| `check.증명서종류` | 증명서종류 | checkbox | 100% | 보관증명서 |
| `check.증명서종류2` | 증명서종류 | checkbox | 100% | 납입완료사실증명서 |
| `금액` | 금액 | number | 100% | 9,310,000 |
| `액면가액` | 액면가액(1주당) | number | 100% | 191,340,000 |
| `기발행주식총수` | 기발행주식총수 | number | 100% | 24 |
| `공모` | 공모 | number | 100% | 24 |
| `signer.name` | 발기인대표(또는)대표이사 | text | 100% | 박찬연 |
| `seal.signer` | 발기인대표(또는)대표이사 | seal | 100% | 강순준 |
| `sign.signer` | 발기인대표(또는)대표이사 | signature | 100% | 박찬연 |
| `위탁회사주소` | 위탁회사주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `employer.name` | 회사명 | text | 100% | (주)케이소프트 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `또는주주총회결의록사본` | 또는주주총회결의록사본 | text | 100% |  |

### 예금(신탁)잔액증명 의뢰서 (`hf011`) — 키 33개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.신청구분` | 신청구분 | checkbox | 100% | 해제 |
| `check.대상계좌` | 대상계좌(발급세부) | checkbox | 100% | 지정계좌 |
| `check.대상계좌2` | 대상계좌(발급세부) | checkbox | 100% | 계좌마스킹(계좌번호 일부숨김) |
| `check.수령방법` | 수령방법 | checkbox | 100% | 카카오톡(문자) |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `account2` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `account3` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.기준일자` | 기준일자 | checkbox | 100% | 매월 |
| `check.유효기간` | 유효기간 | checkbox | 100% | 보기1 |
| `check.창구수령대리인` | 창구수령대리인 | checkbox | 100% | 성명 |
| `check.우편수령대리인` | 우편수령대리인 | checkbox | 100% | 성명 |
| `발급기준일` | 발급기준일 | date | 100% | 2025-01-29 |
| `국문` | 국문 | number | 100% | 6 |
| `매` | 매 | number | 100% | 3 |
| `계좌번호_목록[].value` | (통화코드:) | amount | 100% |  |
| `check.수령방법2` | 수령방법 | checkbox | 100% | E-mail |
| `발급부수` | 발급부수 | text | 100% |  |
| `발급부수2` | 발급부수 | text | 100% |  |
| `signer.name` | 성명(상호명) | text | 100% | 박찬연 |
| `seal.signer` | 성명(상호명) | seal | 100% | 이욱유 |
| `sign.signer` | 성명(상호명) | signature | 100% | 박찬연 |
| `customer.name_en` | 영문명 | text | 100% | PARK CHANYEON |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.birth` | 생년월일(사업자번호) | date | 100% | 1990-02-10 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `agent.name` | 대리인성명 | text | 100% | 박영준 |
| `agent.relation` | 본인과의관계 | text | 100% | 부 |
| `agent.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `check.본인은상기계좌의` | 본인은상기계좌의( | checkbox | 100% | 잔액증명서 발급 |
| `agent.birth` | 생년월일 | date | 100% | 1962.12.19 |
| `agent.phone` | 연락처 | phone | 100% | 010-6515-4769 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 통합제신고서 (`hf015`) — 키 31개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.성명휴대폰번호자택주소직장원본수익자수익수익자` | 성명(업체명)휴대폰번호자택주소직장원본수익자수익수익자 | checkbox | 100% | KT |
| `신청내용` | 신청내용 | text | 100% | 투자 목적 |
| `변경내용` | 변경내용 | text | 100% | 투자 목적 |
| `변경전` | 변경전 | text | 100% | 계좌 정리 |
| `seal.signer` | 인감(서명) | seal | 100% | 강순준 |
| `sign.signer` | 인감(서명) | signature | 100% | 현예지 |
| `변경후` | 변경후 | text | 100% | 해외 이주 |
| `Email또는휴대폰번호` | E-mail또는휴대폰번호 | phone | 100% | 010-5907-7253 |
| `연락처Email기타` | 연락처,E-mail,기타 | text | 100% | 결혼자금 |
| `수령확인` | 수령확인 | text | 100% |  |
| `account` | 출금계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.name` | 성명(업체명) | text | 100% | 박찬연 |
| `신고인` | ⇁신고인 | text | 100% |  |
| `본인과의관계` | ⇁본인과의관계 | text | 100% |  |
| `연락처` | )⇁연락처 | phone | 100% | 010-5907-7253 |
| `상품명` | ⇁상품명 | text | 100% | 산업용 펌프 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인 | text | 100% | 김나우 |
| `seal.signer2` | 대리인 | seal | 100% | 제갈용희 |
| `sign.signer2` | 대리인 | signature | 100% | 김나우 |
| `제신고내용` | ⇁제신고(내용 | text | 100% | 주택구입 |
| `value` | [유선신고사항] | amount | 100% |  |
| `agent.name` | 대리인성명 | text | 100% | 박영준 |
| `agent.phone` | 연락처 | phone | 100% | 010-6515-4769 |
| `위임내용` | 위임내용 | text | 100% | 생활자금 |
| `customer.birth` | 생년월일 | date | 100% | 1997년 5월 14일 |
| `agent.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer3.name` | 위임인 | text | 100% | 박찬연 |
| `seal.signer3` | 위임인 | seal | 100% | 박찬연 |
| `sign.signer3` | 위임인 | signature | 100% | 강순준 |
| `위임장` | 위임장 | text | 100% |  |

### 종합금융상품 ON-LINE 거래 약정서 (`hf016`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 예금주 | text | 100% | 박찬연 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.biz_no` | 사업자등록번호(생년월일) | biz_no | 100% | 264-82-36559 |
| `seal.signer` | 통장인감 | seal | 100% | 이민빈 |
| `sign.signer` | 통장인감 | signature | 100% | 박찬연 |
| `seal.signer2` | 통장인감 | seal | 100% | 이욱유 |
| `sign.signer2` | 통장인감 | signature | 100% | 현예지 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.name2` | 예금주 | text | 100% | 박찬연 |
| `account2` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.name3` | 예금주 | text | 100% | 박찬연 |
| `참고사항` | 참고사항(신청내용등) | text | 100% |  |
| `목록[].은행지점` | 은행지점 | text | 100% | 국민은행 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer3.name` | 본인(예금주) | text | 100% | 박찬연 |
| `seal.signer3` | 본인(예금주) | seal | 100% | 강순준 |
| `sign.signer3` | 본인(예금주) | signature | 100% | 박찬연 |

### 종합금융상품 ON-LINE_거래 (이체)신청서 (`hf017`) — 키 26개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명(회사명) | text | 100% | 박찬연 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `Fax번호` | Fax번호 | text | 100% | 9456-8903 |
| `check.입금` | 입금 | checkbox | 100% | 입 금 |
| `check.예금종류` | 예금종류 | checkbox | 100% | CMA |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `입금금액` | 입금금액 | number | 100% | 6,080,000 |
| `기간` | 기간(만기일) | text | 100% |  |
| `이율` | 이율 | number | 100% | 6.70 |
| `check.입금방법` | 입금방법 | checkbox | 100% | 지준 |
| `지준입금액` | 지준입금액 | number | 100% | 880,000 |
| `전금입금액` | 전금입금액 | number | 100% | 15,750,000 |
| `계좌입금액` | 계좌입금액 | number | 100% | 2,580,000원 |
| `check.당일출금` | 당일출금 | checkbox | 100% | 당일 출금 |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 864-994425-43118 |
| `check.예금종류2` | 예금종류 | checkbox | 100% | CMA |
| `account2` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `인출금액` | 인출금액 | number | 100% | 24,220,000원 |
| `check.이체방법` | 이체방법 | checkbox | 100% | 전금 |
| `목록[].은행명` | 은행명 | text | 100% | 농협은행 |
| `check.인출방법` | 인출방법 | checkbox | 100% | 부리식 |
| `목록[].금액` | 금액 | number | 100% | 1,310,000 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인(예금주) | text | 100% | 박찬연 |
| `seal.signer` | 신청인(예금주) | seal | 100% | 이욱유 |
| `sign.signer` | 신청인(예금주) | signature | 100% | 박찬연 |

### 본인계좌 일괄지급정지 조회신청서 (`hf018`) — 키 19개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 신청인 | text | 100% | 박찬연 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `customer.address` | 주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `customer.birth` | 생년월일 | date | 100% | 1990년 2월 10일 |
| `customer.email` | E-mail | text | 100% | chanyeon363@naver.com |
| `check.금융기관별조회` | ■금융기관별조회(※요청기관V체크) | checkbox | 100% | 전북 |
| `check.수령함` | 수령함 | checkbox | 100% | 수령거절 |
| `customer.name2` | 신청인성명 | text | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `서비스신청일로부터5년까지` | -서비스신청일로부터5년까지 | text | 100% |  |
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 현예지 |
| `sign.signer` | 본인성명 | signature | 100% | 이민빈 |
| `고객상담분쟁조정및민원처리` | -고객상담,분쟁조정및민원처리 | text | 100% |  |
| `성명연락처` | 성명,연락처 | phone | 100% | 010-5907-7253 |

### 본인계좌 일괄지급정지(해제)신청서 (`hf019`) — 키 7개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].개설기관명` | 개설기관명 | text | 100% | 국민은행 |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 857-873265-13818 |
| `customer.name` | 이름 | text | 100% | 박찬연 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `customer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `지급정지시` | 지급정지시 | text | 100% |  |
| `지급정지해제시` | 지급정지해제시 | text | 100% |  |

### 노무비닷컴계좌 개설 및 지급이체서비스 이용 신청서 (`hf020`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `employer.department` | 부서 | text | 100% | 구매팀 |
| `TEL` | TEL | text | 100% |  |
| `company.biz_no` | 사업자번호 | biz_no | 100% | 261-82-53694 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `FAX` | FAX | phone | 100% | 043-783-2775 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.name2` | 예금주 | text | 100% | 박찬연 |
| `원청기업사업자번호` | 원청기업사업자번호 | biz_no | 100% | 155-17-04624 |
| `원청기업명` | 원청기업명 | text | 100% | 동방물산 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | (신청인)신청기업명 | text | 100% | 박찬연 |
| `seal.signer` | (신청인)신청기업명 | seal | 100% | 강순준 |
| `sign.signer` | (신청인)신청기업명 | signature | 100% | 박찬연 |
| `청구서류` | 청구서류 | text | 100% |  |
| `사업자등록증대표자실명확인증표` | 사업자등록증,대표자실명확인증표 | text | 100% |  |
| `개인사업자` | 개인사업자 | text | 100% |  |

### 일괄처리(지급)요청서 (`hf021`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.현금` | 현금 | checkbox | 100% | 이체 (수수료차감 후 입금) |
| `check.현금2` | 현금 | checkbox | 100% | 이체 |
| `check.현금3` | 현금 | checkbox | 100% | 이체 |
| `check.현금4` | 현금 | checkbox | 100% | 현금 |
| `check.현금5` | 현금 | checkbox | 100% | 대체 |
| `check.현금6` | 현금 | checkbox | 100% | 현금 |
| `check.현금7` | 현금 | checkbox | 100% | 이체 |
| `check.현금8` | 현금 | checkbox | 100% | 대체 |
| `check.현금9` | 현금 | checkbox | 100% | 이체 |
| `check.현금10` | 현금 | checkbox | 100% | 대체 |
| `목록[].거래금액` | 거래금액(원) | text | 100% | 70,000 |
| `check.수수료` | 수수료 | checkbox | 100% | 대체(계좌출금) |
| `목록[].지급적요` | 지급적요 | text | 100% |  |
| `목록[].입금은행` | 입금은행 | text | 100% | 하나은행 |
| `목록[].입금계좌번호` | 입금계좌번호 | text | 100% | 319-359450-84249 |
| `목록[].수취인명` | 수취인명 | text | 100% | 주식회사 미래전자 |
| `목록[].입금적요` | 입금적요 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 강순준 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |

### 하도급협력대금통장(상생결제 노무비) 지급이체서비스 이용신청서 (`hf023`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 업체명 | text | 100% | (주)유니온무역 |
| `customer.zipcode` | 우편번호 | number | 100% | 06931 |
| `employer.department` | 부서 | text | 100% | 구매팀 |
| `TEL` | TEL | text | 100% |  |
| `company.biz_no` | 사업자번호 | biz_no | 100% | 264-82-36559 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `FAX` | FAX | phone | 100% | 010-5907-7253 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.name2` | 예금주 | text | 100% | 박찬연 |
| `비고` | 비고 | text | 100% | 급여 수령 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | (신청인)신청기관명 | text | 100% | 박찬연 |
| `seal.signer` | (신청인)신청기관명 | seal | 100% | 이민빈 |
| `sign.signer` | (신청인)신청기관명 | signature | 100% | 박찬연 |

### 금융거래정보제공(요구·동의)서 (`hf024`) — 키 33개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.구분` | 구분 | checkbox | 100% | 요구 |
| `check.신청항목` | 신청항목 | checkbox | 100% | 거래내역 조회 |
| `check.신청항목2` | 신청항목 | checkbox | 100% | 한도조회 및 |
| `check.신청항목3` | 신청항목 | checkbox | 100% | 기타 조회 |
| `check.전금융기관한도및중복가입` | 전금융기관한도및중복가입제한상품 | checkbox | 100% | 기타 ( |
| `check.금융거래종합보고서` | 금융거래종합보고서 | checkbox | 100% | 공직자잔액조회서 |
| `check.계좌번호` | 계좌번호 | checkbox | 100% | 전체 |
| `check.대상기간` | 대상기간 | checkbox | 100% | 최근 3개월 |
| `check.대상기간2` | 대상기간 | checkbox | 100% | 출금내역 |
| `check.신청추가` | 신청추가 | checkbox | 100% | 추가요청사항 |
| `check.신청추가2` | 신청추가 | checkbox | 100% | 수수료 출금동의 |
| `check.계좌번호마스킹제외` | 계좌번호마스킹제외 | checkbox | 100% | 영문주소 표시 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `출금금액` | 출금금액 | number | 100% | 33,700,000 |
| `거래정보등의제공목적` | 거래정보등의제공목적 | text | 100% | 해외 이주 |
| `check.동의서유효기간` | 동의서유효기간 | checkbox | 100% | 보기1 |
| `check.정보제공사실의통보여부` | 정보제공사실의통보여부 | checkbox | 100% | 통보 요청 |
| `customer.name` | 성명(사업자명) | text | 100% | 박찬연 |
| `customer.birth` | 생년월일(사업자번호) | date | 100% | 1990년 2월 10일 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `signer.name` | 성명(사업자명) | text | 100% | 박찬연 |
| `seal.signer` | 성명(사업자명) | seal | 100% | 이욱유 |
| `sign.signer` | 성명(사업자명) | signature | 100% | 강순준 |
| `customer.phone2` | 연락처 | phone | 100% | 010-7321-8870 |
| `customer.birth2` | 생년월일(사업자번호) | date | 100% | 1990년 2월 10일 |
| `반출신청email` | 반출신청e-mail | text | 100% |  |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `signer2.name` | 예금주 | text | 100% | 박찬연 |
| `seal.signer2` | 예금주 | seal | 100% | 이욱유 |
| `sign.signer2` | 예금주 | signature | 100% | 박찬연 |
| `check.대리인을통하여금융거래정보제공을요청하는경우` | 대리인을통하여금융거래정보제공을요청하는경우 | checkbox | 100% | 요구에 체크 표시한 후 금융거래자 본인란을 기재한다. |
| `check.본인이제3자앞정보제공에동의하는경우` | 본인이제3자앞정보제공에동의하는경우 | checkbox | 100% | 동의에 체크 표시한 후 금융거래정보 등의 제공 동의시 기재사항을 기재하고 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 대여금고(신규·변경·해지)신청서 (`hf025`) — 키 26개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `금고번호` | 금고번호 | text | 100% | 006609-2744680 |
| `보증금` | 보증금 | number | 100% | 45,070,000 |
| `원` | 원 | text | 100% |  |
| `signer.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer` | 성명 | seal | 100% | 박찬연 |
| `sign.signer` | 성명 | signature | 100% | 옥영아 |
| `agent.birth` | 생년월일 | date | 100% | 1962.12.19 |
| `agent.phone` | 연락처 | phone | 100% | 010-7910-8205 |
| `agent.address` | 주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `agent.relation` | 관계 | text | 100% | 부 |
| `signer2.name` | 성명 | text | 100% | 최우빈 |
| `seal.signer2` | 성명 | seal | 100% |  |
| `sign.signer2` | 성명 | signature | 100% | 최우빈 |
| `agent.birth2` | 생년월일 | date | 100% | 1967년 12월 2일 |
| `agent.phone2` | 연락처 | phone | 100% | 010-6515-4769 |
| `agent.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `agent.relation2` | 관계 | text | 100% | 부 |
| `customer.name` | 성명(사업자명) | text | 100% | 박찬연 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer3.name` | 성명(사업자명) | text | 100% | 박찬연 |
| `seal.signer3` | 성명(사업자명) | seal | 100% | 박찬연 |
| `sign.signer3` | 성명(사업자명) | signature | 100% | 강순준 |
| `customer.birth` | 생년월일(사업자번호) | date | 100% | 1990.02.10 |
| `customer.email` | e-mail | text | 100% | chanyeon363@naver.com |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### [필수]개인(신용)정보 제3자 제공동의서(하나미소드림적금가입자용) (`hf026`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신용거래정보` | ■신용거래정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 이민빈 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 김소윤 |
| `seal.signer2` | 대리인성명 | seal | 100% | 선영빈 |
| `sign.signer2` | 대리인성명 | signature | 100% | 김소윤 |
| `이용목적` | 이용목적 | text | 100% | 계좌 정리 |
| `계좌번호거래일입금금액` | 계좌번호,거래일,입금금액 | number | 100% | 1,570,000 |

### 위임장(영문) (`hf027`) — 키 17개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `Verificationofidentitysignature` | Verificationofidentity&signature | text | 100% |  |
| `Clerk` | Clerk | text | 100% |  |
| `Manager` | Manager | text | 100% |  |
| `check.Pleasetickintherelevantbox` | Pleasetick√intherelevantbox | checkbox | 100% | . |
| `customer.name` | Name | text | 100% | 박찬연 |
| `RelationshiptoPrincipal` | RelationshiptoPrincipal | text | 100% |  |
| `customer.address` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `check.AccountOpening` | AccountOpening | checkbox | 100% | Savings Deposit |
| `account` | AccountNo. | account_no | 100% | 000-287736-52424 |
| `check.Details` | Details | checkbox | 100% | Change of password |
| `Others` | Others | text | 100% |  |
| `customer.birth` | DateofBirth | date | 100% | 1990년 2월 10일 |
| `ContactInformation` | ContactInformation | text | 100% |  |
| `DateofConfirmingPowersGiven` | DateofConfirmingPowersGiven | date | 100% | 2025년 3월 3일 |
| `customer.name2` | Name | text | 100% | 박찬연 |
| `customer.address2` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `ContactInformation2` | ContactInformation | text | 100% |  |

### 위임장 (`hf028`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.해당` | 해당 | checkbox | 100% | 에 √ 표시하며 기타의 경우 구체적인 위임내용을 기재합니다 |
| `agent.name` | 성명 | text | 100% | 박영준 |
| `agent.relation` | 본인과의관계 | text | 100% | 부 |
| `agent.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `check.신규계좌개설` | 신규계좌개설 | checkbox | 100% | 입출금이자유로운예금 |
| `check.신규계좌개설2` | 신규계좌개설 | checkbox | 100% | 개인(신용)정보 수집 이용 및 제공 동의서(상품서비스 안내 등) 작성 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.세부내용` | 세부내용 | checkbox | 100% | 비밀번호 변경 |
| `기타사항` | 기타사항 | text | 100% | 결혼자금 |
| `agent.birth` | 생년월일 | date | 100% | 1962.12.19 |
| `agent.phone` | 연락처 | phone | 100% | 010-6515-4769 |
| `위임내용확인일시` | 위임내용확인일시 | text | 100% |  |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer.name` | 성명(업체명) | text | 100% | 박찬연 |
| `seal.signer` | 성명(업체명) | seal | 100% | 강순준 |
| `sign.signer` | 성명(업체명) | signature | 100% | 박찬연 |
| `customer.birth` | 생년월일(사업자번호) | date | 100% | 1990년 2월 10일 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.name` | 성명 | text | 100% | 박찬연 |

### 사용인감계(금융계좌개설용) (`hf029`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `seal.signer` | 사용인감 | seal | 100% | 박찬연 |
| `sign.signer` | 사용인감 | signature | 100% | 이주원 |
| `agent.name` | 성명 | text | 100% | 박영준 |
| `agent.phone` | 연락처(선택항목) | phone | 100% | 010-6515-4769 |
| `agent.address` | 주소(선택항목) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `agent.birth` | 생년월일 | date | 100% | 1962.12.19 |
| `agent.relation` | 본인과의관계 | text | 100% | 부 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `company.name` | 법인명 | text | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `customer.address` | 주소(선택항목) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.ceo` | 대표자명 | text | 100% | 박찬연 |

### 국내원천소득 제한세율 적용신청서(외국법인용-영문) (`hf030`) — 키 17개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `FilingNo` | FilingNo. | text | 100% | 078-596794-06881 |
| `ApplicantInformation` | ApplicantInformation | text | 100% | 한빛무역 |
| `NameofCorporation` | NameofCorporation | text | 100% |  |
| `NameofRepresentative` | NameofRepresentative | text | 100% |  |
| `TaxpayerIdentificationNo` | TaxpayerIdentificationNo. | text | 100% | 682-806786-63327 |
| `DateofIncorporation` | DateofIncorporation | date | 100% | 2026.01.22 |
| `FilingDate` | FilingDate | date | 100% | 2025년 4월 10일 |
| `customer.address` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.address2` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `CountryofResidence` | CountryofResidence | text | 100% | 독일 |
| `CountryCode` | CountryCode | text | 100% | 중국 |
| `TelephoneNumber` | TelephoneNumber | phone | 100% | 010-3347-9183 |
| `AddressorLocation` | AddressorLocation | text | 100% |  |
| `To` | To | text | 100% |  |
| `Type` | Type | text | 100% |  |
| `TaxAdministrator` | []TaxAdministrator | text | 100% |  |
| `Other` | []Other | text | 100% |  |

### 국내원천소득 제한세율 적용신청서(외국법인용) (`hf031`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 법인명 | text | 100% | 주식회사 한빛패션 |
| `company.ceo` | 대표자성명 | text | 100% | 박찬연 |
| `납세자번호` | 납세자번호 | text | 100% | 115-496202-47345 |
| `설립년월일` | 설립년월일 | date | 100% | 2024.12.27 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `거주지국` | 거주지국 | text | 100% |  |
| `국가코드` | 국가코드 | number | 100% | 660254 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `거주지국의세법상납세의무가있습니까` | 거주지국의세법상납세의무가있습니까? | text | 100% |  |
| `지급받는국내원천소득의실질귀속자입니까` | 지급받는국내원천소득의실질귀속자입니까? | number | 100% | 2,880,000원 |
| `목록[].예` | 예 | text | 100% |  |
| `거주지국의세법상납세의무가있습니까2` | 거주지국의세법상납세의무가있습니까? | text | 100% |  |
| `지급받는국내원천소득의실질귀속자입니까2` | 지급받는국내원천소득의실질귀속자입니까? | number | 100% | 4,240,000원 |
| `목록[].아니오` | 아니오 | text | 100% |  |
| `주소또는소재지` | 주소또는소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `성명또는법인명` | 성명또는법인명 | text | 100% | (주)제일산업 |
| `company.biz_no` | 사업자(주민)등록번호 | biz_no | 100% | 264-82-36559 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인(대표자) | text | 100% | 박찬연 |
| `seal.signer` | 신청인(대표자) | seal | 100% | 강순준 |
| `sign.signer` | 신청인(대표자) | signature | 100% | 박찬연 |
| `법인연금기금` | []법인,[]연금,[]기금, | text | 100% |  |

### 국내원천소득 제한세율 적용신청서(비거주자용) (`hf032`) — 키 25개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `납세자번호` | 납세자번호 | text | 100% | 9086-2118 |
| `거주지국` | 거주지국 | text | 100% |  |
| `value` | (거주지전화)(국내전화) | amount | 100% |  |
| `customer.birth` | 생년월일 | date | 100% | 1966.08.12 |
| `거주지국코드` | 거주지국코드 | number | 100% | 91440 |
| `가국내에주소를두고있습니까` | 가국내에주소를두고있습니까? | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `나국내에계속하여183일이상거주하고있습니까` | 나국내에계속하여183일이상거주하고있습니까? | text | 100% |  |
| `바대한민국의공무원입니까` | 바대한민국의공무원입니까? | text | 100% |  |
| `가국내에주소를두고있습니까2` | 가국내에주소를두고있습니까? | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `나국내에계속하여183일이상거주하고있습니까2` | 나국내에계속하여183일이상거주하고있습니까? | text | 100% |  |
| `다최근1년동안국내에체재한날이183일이상입니까` | 다최근1년동안국내에체재한날이183일이상입니까? | text | 100% |  |
| `목록[].예` | 예 | text | 100% |  |
| `마국내에계속하여183일이상거주할것을필요로하는직업이있습니까` | 마국내에계속하여183일이상거주할것을필요로하는직업이있습니까? | text | 100% |  |
| `바대한민국의공무원입니까2` | 바대한민국의공무원입니까? | text | 100% |  |
| `목록[].아니오` | 아니오 | text | 100% |  |
| `주소또는소재지` | 주소또는소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `성명또는법인명` | 성명또는법인명 | text | 100% | 가온화학(주) |
| `company.biz_no` | 사업자(주민)등록번호 | biz_no | 100% | 264-82-36559 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 현예지 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |
| `signer2.name` | 고객명 | text | 100% | 박찬연 |
| `seal.signer2` | 고객명 | seal | 100% | 박찬연 |
| `sign.signer2` | 고객명 | signature | 100% | 강순준 |

### 국내원천소득 제한세율 적용신청서(비거주자용-영문) (`hf033`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `FilingNo` | FilingNo. | text | 100% | 445-769435-05551 |
| `FilingDate` | FilingDate | date | 100% | 2026년 1월 20일 |
| `TaxpayerIdentificationNo` | TaxpayerIdentificationNo. | text | 100% | 808-005849-85936 |
| `CountryofResidence` | CountryofResidence | text | 100% | 캐나다 |
| `customer.birth` | DateofBirth | date | 100% | 900210 |
| `CountryCode` | CountryCode | text | 100% | 영국 |
| `목록[].Yes` | Yes | text | 100% |  |
| `목록[].No` | No | text | 100% |  |
| `AddressorLocation` | AddressorLocation | text | 100% |  |
| `NameofIndividualorCorporation` | NameofIndividualorCorporation | text | 100% |  |
| `Applicant` | Applicant | text | 100% | 세진산업 |

### 확인서(잔액통보생략용) (`hf034`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `감사통할` | 감사통할 | text | 100% |  |
| `영업점장` | 영업점장 | text | 100% |  |
| `목록[].예금종별` | 예금종별 | text | 100% | 주거래하나 통장 |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 174-956837-60545 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 예금주 | text | 100% | 박찬연 |
| `seal.signer` | 예금주 | seal | 100% | 현예지 |
| `sign.signer` | 예금주 | signature | 100% | 강순준 |

### 수표·어음용지 폐기신고서 (`hf035`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `기호및번호` | 기호및번호 | text | 100% | 259-424231-88167 |
| `수령일자` | 수령일자 | date | 100% | 2025년 8월 14일 |
| `폐기일자` | 폐기일자 | date | 100% | 2025.09.11 |
| `폐기경위` | 폐기경위 | text | 100% |  |
| `취급점` | 취급점 | text | 100% | 둔산지점 |
| `signer.name` | 명 | text | 100% | 박찬연 |
| `seal.signer` | 명 | seal | 100% | 이민빈 |
| `sign.signer` | 명 | signature | 100% | 현예지 |
| `customer.birth` | 생년월일(사업자등록번호) | date | 100% | 1990-02-10 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 예금(신탁) 이관 의뢰서 (`hf036`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `예금종류` | 예금(신탁)종류 | text | 100% | 청년도약계좌 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.name` | 예금주(위탁자) | text | 100% | 박찬연 |
| `예금잔액` | 예금(신탁)잔액 | number | 100% | 44,990,000원 |
| `현취급점명` | 현취급점명 | text | 100% | 범어지점 |
| `비고` | 비고 | text | 100% | 학자금 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 명 | text | 100% | 박찬연 |
| `seal.signer` | 명 | seal | 100% | 박찬연 |
| `sign.signer` | 명 | signature | 100% | 강순준 |
| `signer2.name` | 명 | text | 100% | 박찬연 |
| `seal.signer2` | 명 | seal | 100% | 박찬연 |
| `sign.signer2` | 명 | signature | 100% | 이민빈 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer3` | 지점 | seal | 100% | 김나우 |
| `sign.signer3` | 지점 | signature | 100% | 강순준 |
| `이관점기재란` | 이관점기재란 | text | 100% |  |
| `이관서류목록` | 이관서류목록 | text | 100% |  |

### 위탁유가증권 반환청구서 (`hf037`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `유가증권수탁통장번호` | 유가증권수탁통장번호 | text | 100% | 281982-7764138 |
| `목록[].위탁일자` | 위탁일자 | text | 100% | 2025.04.16 |
| `목록[].수탁번호` | 수탁번호 | text | 100% | 3331-6554 |
| `목록[].종류` | 종류 | text | 100% | 주거래하나 통장 |
| `목록[].증서어음번호` | 증서【어음】번호 | text | 100% | 마가75001144 |
| `목록[].지급지` | 지급지 | text | 100% | 범어지점 |
| `목록[].발행인` | 발행인 | text | 100% | 세진화학 |
| `목록[].만기일` | 만기일 | text | 100% | 2029-12-28 |
| `목록[].금액` | 금액 | text | 100% | 269,400,000원 |
| `목록[].비고` | 비고 | text | 100% | 투자 목적 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 명 | text | 100% | 박찬연 |
| `seal.signer` | 명 | seal | 100% | 이욱유 |
| `sign.signer` | 명 | signature | 100% | 강순준 |
| `customer.birth` | 생년월일(사업자등록번호) | date | 100% | 1990년 2월 10일 |
| `customer.phone` | 전화번호(선택항목) | phone | 100% | 010-7321-8870 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer2` | 성명 | seal | 100% | 박찬연 |
| `sign.signer2` | 성명 | signature | 100% | 이욱유 |

### 수표(어음)발행사실 확인의뢰서 (`hf038`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].수표어음` | 수표어음 | text | 100% | 약속어음 |
| `목록[].번호` | 번호 | text | 100% | 051-428869-55715 |
| `목록[].발행일` | 발행일 | text | 100% | 2025-09-27 |
| `목록[].지급일` | 지급일 | text | 100% | 2025.12.14 |
| `목록[].금액` | 금액 | text | 100% | 590,000원 |
| `목록[].수취인` | 수취인 | text | 100% | 주식회사 대성로지스 |
| `목록[].용도` | 용도 | text | 100% | 급여하나 통장 |
| `목록[].확인여부` | 확인여부(결제일등) | text | 100% |  |
| `목록[].담당자인` | 담당자인 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 상호및대표자 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자 | seal | 100% | (주)유니온무역 |
| `sign.signer` | 상호및대표자 | signature | 100% | (주)삼정전자 |

### 유가증권 수탁약정서 (`hf039`) — 키 10개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 신청인성명(예금주) | text | 100% | 박찬연 |
| `추심대전입금계좌번호` | 추심대전입금계좌번호 | text | 100% | 859-407547-07284 |
| `check.주소` | 주소(선택또는전부기재) | checkbox | 100% | 직장 |
| `check.연락처` | 연락처(선택또는전부기재) | checkbox | 100% | 자택 |
| `seal.signer` | 거래인감(또는서명) | seal | 100% | 현예지 |
| `sign.signer` | 거래인감(또는서명) | signature | 100% | 박찬연 |
| `customer.birth` | 생년월일(사업자등록번호) | date | 100% | 1990.02.10 |
| `check.보관어음월별잔고현황통지여부` | 보관어음월별잔고현황통지여부 | checkbox | 100% | E-MAIL |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 사고신고 담보금 지급정지가처분담보금 처리를 위한 약정서 (`hf041`) — 키 6개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 명 | text | 100% | 박찬연 |
| `seal.signer` | 명 | seal | 100% | 강순준 |
| `sign.signer` | 명 | signature | 100% | 박찬연 |
| `seal.signer2` | 지점 | seal | 100% | 박찬연 |
| `sign.signer2` | 지점 | signature | 100% | 강순준 |

### 사채원리금 지급대행 계약서 (`hf042`) — 키 25개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `사채의명칭` | 사채의명칭 | text | 100% | 유니온화학(주) |
| `사채의종류` | 사채의종류 | text | 100% |  |
| `사채의전자등록총액` | 사채의전자등록총액 | number | 100% | 84,070,000 |
| `사채의발행가액` | 사채의발행가액 | number | 100% | 114,350,000 |
| `사채의발행가액총액` | 사채의발행가액총액 | number | 100% | 44,600,000 |
| `사채의거래단위` | 사채의거래단위 | text | 100% |  |
| `사채의이율` | 사채의이율 | number | 100% | 3.44 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `이자지급기일` | 이자지급기일 | date | 100% | 2026.05.19 |
| `연체이자` | 연체이자 | number | 100% | 60,450,000 |
| `사채관리회사` | 사채관리회사 | text | 100% |  |
| `기타` | 기타 | text | 100% | 해외 이주 |
| `목록[].예금주` | 예금주 | text | 100% |  |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 343-445601-24898 |
| `담당자성명` | 담당자성명 | text | 100% | 박경현 |
| `customer.phone` | 핸드폰번호(SMS교환안내수신번호) | phone | 100% | 010-5907-7253 |
| `회사전화번호` | 회사전화번호 | phone | 100% | 02-279-2475 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer.name` | 대표이사 | text | 100% | 박찬연 |
| `seal.signer` | 대표이사 | seal | 100% | 박찬연 |
| `sign.signer` | 대표이사 | signature | 100% | 강순준 |
| `signer2.name` | 지점지점장 | text | 100% | 박찬연 |
| `seal.signer2` | 지점지점장 | seal | 100% | 박찬연 |
| `sign.signer2` | 지점지점장 | signature | 100% | 강순준 |

### 세금우대종합저축(비과세저축) 제변경신고서(비과세공용) (`hf043`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `예금신탁종류` | 예금/신탁종류 | text | 100% |  |
| `check.신청구분` | 신청구분 | checkbox | 100% | 장애인 해제 |
| `한도설정` | 한도설정 | number | 100% | 214,480,000 |
| `한도증액` | 한도증액 | number | 100% | 28,210,000원 |
| `한도감액` | 한도감액 | number | 100% | 46,810,000 |
| `상속인등록` | 상속인등록 | text | 100% |  |
| `기타` | 기타 | text | 100% | 자녀 교육비 |
| `signer.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer` | 성명 | seal | 100% | 이욱유 |
| `sign.signer` | 성명 | signature | 100% | 강순준 |
| `customer.address` | 주소(선택항목) | text | 100% | 서울특별시 송파구 중대로 174, 119동 2202호 |
| `signer2.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer2` | 성명 | seal | 100% | 이민빈 |
| `sign.signer2` | 성명 | signature | 100% | 박찬연 |
| `customer.address2` | 주소(선택항목) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `목록[].변경후` | 변경후 | text | 100% | 학자금 |
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.birth2` | 생년월일 | date | 100% | 1990.02.10 |
| `check.한도설정` | 한도설정 | checkbox | 100% | 한도증액 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |

### 예금(신탁) 양도승낙 의뢰서 및 양도승낙서 (`hf044`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 예금주(양도인)(위탁자겸수익자) | text | 100% | 박찬연 |
| `예금종별` | 예금(신탁)종별 | text | 100% | 청년도약계좌 |
| `금액` | 금액 | number | 100% | 10,060,000 |
| `account` | 계좌번호 | account_no | 100% | 774-646914-96117 |
| `만기일` | 만기일 | date | 100% | 2025.04.01 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 명 | text | 100% | 박찬연 |
| `seal.signer` | 명 | seal | 100% | 현예지 |
| `sign.signer` | 명 | signature | 100% | 박찬연 |
| `signer2.name` | 명 | text | 100% | 박찬연 |
| `seal.signer2` | 명 | seal | 100% | 박찬연 |
| `sign.signer2` | 명 | signature | 100% | 강순준 |
| `예금종별2` | 예금(신탁)종별 | text | 100% | 하나의정기예금 |
| `금액2` | 금액 | number | 100% | 282,290,000 |
| `account2` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `만기일2` | 만기일 | date | 100% | 2025.02.16 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer3` | 부점장 | seal | 100% | 박찬연 |
| `sign.signer3` | 부점장 | signature | 100% | 이민빈 |
| `customer.birth` | 생년월일(사업자등록번호) | date | 100% | 1966.08.12 |
| `customer.birth2` | 생년월일(사업자등록번호) | date | 100% | 1997.05.14 |

### 야간금고입금의뢰서 (`hf045`) — 키 47개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `만원권` | 만원권 | number | 100% | 24 |
| `천원권` | 천원권 | number | 100% | 60 |
| `천원권2` | 천원권 | number | 100% | 24 |
| `원` | 원 | number | 100% | 24 |
| `원2` | 원 | number | 100% | 12 |
| `원3` | 원 | number | 100% | 36 |
| `원4` | 원 | number | 100% | 36 |
| `소계` | 소계(A) | number | 100% | 4,870,000원 |
| `매` | 매 | number | 100% | 38,750,000원 |
| `매2` | 매 | number | 100% | 187,840,000 |
| `매3` | 매 | number | 100% | 131,170,000원 |
| `개` | 개 | number | 100% | 90,000 |
| `개2` | 개 | number | 100% | 6,230,000 |
| `개3` | 개 | number | 100% | 16,380,000 |
| `개4` | 개 | number | 100% | 9,670,000 |
| `약속어음` | 약속어음 | text | 100% |  |
| `당점권` | 당점권 | number | 100% | 6 |
| `자기앞수표` | 자기앞수표 | number | 100% | 12 |
| `송금수표` | 송금수표 | number | 100% | 24 |
| `당좌수표` | 당좌수표 | number | 100% | 12 |
| `가계수표` | 가계수표 | number | 100% | 2 |
| `약속어음2` | 약속어음 | number | 100% | 2 |
| `매4` | 매 | number | 100% | 6 |
| `소계2` | 소계(B) | number | 100% | 93,610,000원 |
| `총계` | 총계(A+B) | number | 100% | 3,810,000원 |
| `매5` | 매 | number | 100% | 9,120,000원 |
| `매6` | 매 | number | 100% | 16,280,000 |
| `매7` | 매 | number | 100% | 184,110,000 |
| `매8` | 매 | number | 100% | 8,670,000 |
| `매9` | 매 | number | 100% | 2,830,000 |
| `매10` | 매 | number | 100% | 8,720,000 |
| `매11` | 매 | number | 100% | 42,050,000원 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `예금과목` | 예금과목 | text | 100% | 하나 적금 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `signer.name` | 의뢰인성명 | text | 100% | 박찬연 |
| `seal.signer` | 의뢰인성명 | seal | 100% | 이욱유 |
| `sign.signer` | 의뢰인성명 | signature | 100% | 강순준 |
| `원整` | 원整 | text | 100% |  |
| `목록[].수표종류` | 수표종류 | text | 100% | 당좌수표 |
| `목록[].지급은행` | 지급은행 | text | 100% | 카카오뱅크 |
| `목록[].수표번호` | 수표번호 | text | 100% | 가다17590535 |
| `목록[].발행일자` | 발행일자 | text | 100% | 2024년 5월 25일 |
| `목록[].지급일자` | 지급일자 | text | 100% | 2024.09.24 |
| `목록[].발행인` | 발행인 | text | 100% | 주식회사 한빛패션 |
| `목록[].비고` | 비고 | text | 100% | 생활자금 |

### 목돈을 불리는 통장 거래신청서 (`hf046`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `자택` | 자택 | text | 100% |  |
| `employer.name` | 근무처 | text | 100% | 주식회사 태평양무역 |
| `모계좌계좌번호` | 모계좌(이체지정계좌)계좌번호 | text | 100% | 112-561952-67519 |
| `customer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `통장번호` | 통장번호 | text | 100% | 398-576729-89634 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `목록[].일자` | 일자 | text | 100% | 2026.01.12 |
| `목록[].내용` | 내용 | text | 100% | 타행 이체 |
| `date2` | 일자 | date | 100% | 2026년 01월 31일 |
| `seal.signer` | 변경인감 | seal | 100% | 강순준 |
| `sign.signer` | 변경인감 | signature | 100% | 박찬연 |

### 외화송금신청서 (`hf199`) — 키 60개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `담당` | 담당(실명확인) | text | 100% |  |
| `check.송금방법` | 송금방법 | checkbox | 100% | 금융결제원이체(국가간송금) |
| `check.송금정보등록` | 송금정보등록 | checkbox | 100% | 신규 |
| `영문` | 영문(English) | text | 100% |  |
| `국문` | 국문(Korean) | text | 100% |  |
| `customer.rrn` | 주민(사업자)번호(I.DNo./PassportNo.) | rrn | 100% | 900210-1659382 |
| `과거송금번호` | 과거송금번호(EXISTINGREF.NO) | text | 100% | 8437-6676 |
| `check.결제은행수수료부담` | 결제은행수수료부담(REIMBURSINGBANKCHG.) | checkbox | 100% | 송금인 (DEBT) |
| `check.받으실분` | 받으실분(Beneficiary) | checkbox | 100% | HAPPY E-MAIL 서비스 신청 (무료) |
| `송금목적` | 송금목적(송금사유)(PURPOSEOFPAYMENT) | text | 100% | 계좌 정리 |
| `적요` | 적요(DETAILSOFPAYMENT) | text | 100% |  |
| `은행코드` | 은행코드(SWIFTBIC) | number | 100% | 02686 |
| `은행명` | 은행명(BANKNAME) | text | 100% | 신한은행 |
| `은행명2` | 은행명(BANKNAME) | text | 100% | 농협은행 |
| `통화금액` | 통화(CURRENCY):금액(AMOUNT) | number | 100% | 8,370,000 |
| `은행코드2` | 은행코드(BANKCODE) | number | 100% | 8563 |
| `수취인계좌번호` | 수취인계좌번호(BNF'sA/CNo.) | text | 100% | 350-152554-47311 |
| `foreign.name` | 성명(Name) | text | 100% | Mekong Garment JSC |
| `신청인과의관계` | 신청인과의관계(RELATIONTOAPPLICANT) | text | 100% |  |
| `check.송금정보등록건송금결과통지` | 송금정보등록건송금결과통지 | checkbox | 100% | SMS |
| `check.통화금액` | 통화(CURRENCY):금액(AMOUNT) | checkbox | 100% | 수수료 별도납부 |
| `보내는분계좌번호` | 보내는분계좌번호(A/CNO) | text | 100% | 947-036642-25863 |
| `check.수수료차감후송금` | 수수료차감후송금 | checkbox | 100% | 수수료차감후 송금 |
| `신청인과의관계2` | 신청인과의관계(RELATIONTOAPPLICANT) | text | 100% |  |
| `check.귀행을` | ●귀행을 | checkbox | 100% | 해외체재비 |
| `signer.name` | 예금주명(A/CHOLDERNAME) | text | 100% | 박찬연 |
| `seal.signer` | 예금주명(A/CHOLDERNAME) | seal | 100% | 이민빈 |
| `sign.signer` | 예금주명(A/CHOLDERNAME) | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신청인(Applicant) | text | 100% | 박찬연 |
| `seal.signer2` | 신청인(Applicant) | seal | 100% | 박찬연 |
| `sign.signer2` | 신청인(Applicant) | signature | 100% | 현예지 |
| `signer3.name` | 대리인(Agent) | text | 100% | 이민빈 |
| `seal.signer3` | 대리인(Agent) | seal | 100% |  |
| `sign.signer3` | 대리인(Agent) | signature | 100% | 이민빈 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer4` | 지점장 | seal | 100% | 강순준 |
| `sign.signer4` | 지점장 | signature | 100% | 박찬연 |
| `대리인실명번호` | 대리인실명번호(AGENTID.NO) | text | 100% | 5655-7694 |
| `check.자동화기기를이용한외화송금서비스신청` | ◈자동화기기를이용한외화송금서비스신청( | checkbox | 100% | 신규 |
| `check.송금항목` | 송금항목 | checkbox | 100% | 거주자의 무증빙 해외송금 |
| `check.송금항목2` | 송금항목 | checkbox | 100% | 체재비 송금 |
| `인출계좌번호` | 인출계좌번호 | text | 100% | 936-061429-50847 |
| `check.송금결과통보` | 송금결과통보 | checkbox | 100% | E-MAIL |
| `check.유학생송금` | 유학생송금 | checkbox | 100% | 유학생 송금 |
| `check.외국인근로자의보수송금` | 외국인근로자의보수송금 | checkbox | 100% | 외국인 근로자의 보수 송금 |
| `check.국내전신송금` | 국내전신송금 | checkbox | 100% | 국내 전신 송금 |
| `사전송금방식국내통관전수입대금을지급` | 사전송금방식:국내통관(물품인수)전수입대금을지급 | number | 100% | 174,780,000원 |
| `check.대금송금후물품수령예정일` | 대금송금후물품(선적서류)수령예정일 | checkbox | 100% | 년 이내 |
| `check.대금송금후물품수령예정일2` | 대금송금후물품(선적서류)수령예정일 | checkbox | 100% | 년 초과 ( |
| `check.일반수입` | 일반수입 | checkbox | 100% | 일반 수입 |
| `check.중계무역` | 중계무역 | checkbox | 100% | 중계 무역 |
| `check.외국인수수입` | 외국인수수입 | checkbox | 100% | 외국인수 수입 |
| `check.현재수출계약체결` | 현재수출계약체결 | checkbox | 100% | 현재 수출계약 체결 |
| `check.현재수출계약미체결` | 현재수출계약미체결 | checkbox | 100% | 현재 수출계약 미체결 |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer5.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer5` | 신청인 | seal | 100% | 강순준 |
| `sign.signer5` | 신청인 | signature | 100% | 박찬연 |
| `대금송금후물품수령예정일` | 대금송금후물품(선적서류)수령예정일 | date | 100% | 2026년 1월 15일 |

### 거래외국환지정(변경)신청서(영문) (`hf201`) — 키 6개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `Staff` | Staff | text | 100% |  |
| `Manager` | Manager | text | 100% |  |
| `PhoneNo` | PhoneNo | phone | 100% | 010-5907-7253 |
| `PhoneNo2` | PhoneNo | phone | 100% | 010-5907-7253 |
| `of` | of | text | 100% |  |
| `Bank` | Bank | text | 100% |  |

### 거래외국환지정(변경)신청서 (`hf202`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 지정인성명(상호) | text | 100% | 박찬연 |
| `seal.signer` | 지정인성명(상호) | seal | 100% | 박찬연 |
| `sign.signer` | 지정인성명(상호) | signature | 100% | 현예지 |
| `소` | 소 | text | 100% |  |
| `EMail주소` | E-Mail주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer2.name` | 대리인성명(상호) | text | 100% | 최우빈 |
| `seal.signer2` | 대리인성명(상호) | seal | 100% | 김소윤 |
| `sign.signer2` | 대리인성명(상호) | signature | 100% | 최우빈 |
| `소2` | 소 | text | 100% |  |
| `EMail주소2` | E-Mail주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `seal.signer3` | 장 | seal | 100% | 현예지 |
| `sign.signer3` | 장 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer4` | 지점장 | seal | 100% | 강순준 |
| `sign.signer4` | 지점장 | signature | 100% | 박찬연 |

### 주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(영문) (`hf203`) — 키 43개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `DateofReceipt` | DateofReceipt | date | 100% | 2025년 5월 19일 |
| `check.Individual` | Individual | checkbox | 100% | 보기2 |
| `check.ForeignInvestor` | ForeignInvestor | checkbox | 100% | 보기1 |
| `customer.address` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `value` | (Korean) | amount | 100% |  |
| `value2` | (English) | amount | 100% |  |
| `Headquarter` | Headquarter | text | 100% |  |
| `Mainfactory` | Mainfactory(Mainplaceofbusiness) | text | 100% |  |
| `customer.nationality` | Nationality | text | 100% | 대한민국 |
| `AcquisitionPricewon` | AcquisitionPrice:won(USD) | number | 100% | 70 |
| `check.보기1` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기12` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기13` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기14` | 보기1 | checkbox | 100% | 보기1 |
| `NotificationNo` | NotificationNo | text | 100% | 280920-6972638 |
| `NumberofReceipt` | NumberofReceipt | text | 100% |  |
| `DateofCompletion` | DateofCompletion | date | 100% | 2025.06.30 |
| `won` | won | text | 100% |  |
| `Capital` | Capital | text | 100% |  |
| `wonUSD` | won(USD | amount | 100% | JPY 140,000 |
| `DateofReceipt2` | DateofReceipt | date | 100% | 2026.01.03 |
| `check.Individual2` | Individual | checkbox | 100% | 보기2 |
| `check.ForeignInvestor2` | ForeignInvestor | checkbox | 100% | 보기1 |
| `customer.address2` | Address | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `value3` | (Korean) | amount | 100% |  |
| `value4` | (English) | amount | 100% |  |
| `Headquarter2` | Headquarter | text | 100% |  |
| `Mainfactory2` | Mainfactory(Mainplaceofbusiness) | text | 100% |  |
| `customer.nationality2` | Nationality | text | 100% | 대한민국 |
| `AcquisitionPricewon2` | AcquisitionPrice:won(USD) | number | 100% | 70 |
| `check.보기15` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기16` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기17` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기18` | 보기1 | checkbox | 100% | 보기1 |
| `NotificationNo2` | NotificationNo | text | 100% | 204422-6569354 |
| `NumberofReceipt2` | NumberofReceipt | text | 100% |  |
| `DateofCompletion2` | DateofCompletion | date | 100% | 2025.04.04 |
| `won2` | won | text | 100% |  |
| `Capital2` | Capital | text | 100% |  |
| `wonUSD2` | won(USD | amount | 100% | USD 116,500 |
| `Delegated` | Delegated | text | 100% |  |
| `Delegated2` | Delegated | text | 100% |  |
| `Delegated3` | Delegated | text | 100% |  |

### 주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(국문) (`hf204`) — 키 60개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `접수일` | 접수일 | text | 100% |  |
| `처리일` | 처리일 | text | 100% |  |
| `check.개인` | 개인 | checkbox | 100% | 외국법인 |
| `customer.address` | 주소(영문) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `하려는사업` | 하려는(하고있는)사업 | text | 100% |  |
| `value` | (국문) | amount | 100% |  |
| `value2` | (영문) | amount | 100% |  |
| `본사` | 본사 | text | 100% |  |
| `주공장소재지` | 주공장(주사업장)소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `금번투자지역` | 금번투자지역(신주취득및출연의경우) | text | 100% |  |
| `액면총액` | 액면총액(A×B) | number | 100% | 2,620,000 |
| `금번투자에따른예상근로자수` | 금번투자에따른예상근로자수 | text | 100% |  |
| `취득총액` | 취득총액(A×C) | number | 100% | 6,380,000원 |
| `customer.nationality` | 국적 | text | 100% | 대한민국 |
| `취득총액원` | 취득총액:원(USD상당) | number | 100% | 70 |
| `check.방위사업법제3조제7호에따른방위산업물자를생산하는기업` | 「방위사업법」제3조제7호에따른방위산업물자를생산하는기업 | checkbox | 100% | 보기1 |
| `check.보기1` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기12` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기13` | 보기1 | checkbox | 100% | 보기1 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신고인또는신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신고인또는신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신고인또는신청인 | signature | 100% | 이욱유 |
| `신고번호` | 신고(허가)번호 | text | 100% | 714361-7064964 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `접수번호` | 접수번호 | text | 100% |  |
| `기존주취득시` | 기존주취득시 | number | 100% | 56,130,000원 |
| `취득전` | 취득(출연)전 | number | 100% | 1,280,000 |
| `취득후` | 취득(출연)후 | number | 100% | 360,000 |
| `의내용` | 의내용 | text | 100% | 생활자금 |
| `접수일2` | 접수일 | text | 100% |  |
| `처리일2` | 처리일 | text | 100% |  |
| `check.개인2` | 개인 | checkbox | 100% | 국제경제협력기구 |
| `customer.address2` | 주소(영문) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `하려는사업2` | 하려는(하고있는)사업 | text | 100% |  |
| `value3` | (국문) | amount | 100% |  |
| `value4` | (영문) | amount | 100% |  |
| `본사2` | 본사 | text | 100% |  |
| `주공장소재지2` | 주공장(주사업장)소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `금번투자지역2` | 금번투자지역(신주취득및출연의경우) | text | 100% |  |
| `액면총액2` | 액면총액(A×B) | number | 100% | 400,000 |
| `금번투자에따른예상근로자수2` | 금번투자에따른예상근로자수 | text | 100% |  |
| `취득총액2` | 취득총액(A×C) | number | 100% | 297,340,000 |
| `customer.nationality2` | 국적 | text | 100% | 대한민국 |
| `취득총액원2` | 취득총액:원(USD상당) | number | 100% | 60 |
| `check.방위사업법제3조제7호에따른방위산업물자를생산하는기업2` | 「방위사업법」제3조제7호에따른방위산업물자를생산하는기업 | checkbox | 100% | 보기1 |
| `check.보기14` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기15` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기16` | 보기1 | checkbox | 100% | 보기1 |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고인또는신청인 | text | 100% | 박찬연 |
| `seal.signer2` | 신고인또는신청인 | seal | 100% | 박찬연 |
| `sign.signer2` | 신고인또는신청인 | signature | 100% | 강순준 |
| `신고번호2` | 신고(허가)번호 | text | 100% | 5447-3048 |
| `date4` | 작성일 | date | 100% | 2026년 1월 31일 |
| `접수번호2` | 접수번호 | text | 100% |  |
| `기존주취득시2` | 기존주취득시 | number | 100% | 21,120,000 |
| `취득전2` | 취득(출연)전 | number | 100% | 1,500,000원 |
| `취득후2` | 취득(출연)후 | number | 100% | 8,190,000 |
| `의내용2` | 의내용 | text | 100% | 급여 수령 |

### 외국환거래법시행령상 거주성확인서 (`hf205`) — 키 34개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `여권번호` | 여권번호 | text | 100% | M67845442 |
| `customer.nationality` | 국적 | text | 100% | 대한민국 |
| `가외국에서영업활동에종사하고있습니까` | 가외국에서영업활동에종사하고있습니까? | text | 100% |  |
| `나외국에있는국제기구에서근무하고있습니까` | 나외국에있는국제기구에서근무하고있습니까? | text | 100% |  |
| `예` | 예(YES) | text | 100% |  |
| `예2` | 예(YES) | text | 100% |  |
| `마외국정부또는국제기구의공무로입국하는자입니까` | 마외국정부또는국제기구의공무로입국하는자입니까? | text | 100% |  |
| `바거주자였던외국인으로서출국하여외국에서3개월이상체재중입니까` | 바거주자였던외국인으로서출국하여외국에서3개월이상체재중입니까? | text | 100% |  |
| `예3` | 예(YES) | text | 100% |  |
| `국민_목록[].아니오` | 아니오(NO) | text | 100% |  |
| `외국인_목록[].아니오` | 아니오(NO) | text | 100% |  |
| `아니오` | 아니오(NO) | text | 100% |  |
| `check.판정방법` | 판정방법 | checkbox | 100% | 판정방법 |
| `항목` | 항목 | text | 100% |  |
| `외국인` | 외국인 | text | 100% |  |
| `예4` | 예(YES) | text | 100% |  |
| `나비거주자이었던자로서입국하여국내에3개월이상체재중입니까` | 나비거주자이었던자로서입국하여국내에3개월이상체재중입니까? | text | 100% |  |
| `다국내에서영업활동에종사하고있습니까` | 다국내에서영업활동에종사하고있습니까? | text | 100% |  |
| `라6개월이상국내에서체재하고있습니까` | 라6개월이상국내에서체재하고있습니까? | text | 100% |  |
| `check.판정방법2` | 판정방법 | checkbox | 100% | 판정방법 |
| `거주성판정결과` | 거주성판정결과 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 현예지 |
| `항목2` | 항목 | text | 100% |  |
| `가외국에서영업활동에종사하고있는자` | 가.외국에서영업활동에종사하고있는자 | text | 100% |  |
| `나외국에있는국제기구에서근무하고있는자` | 나.외국에있는국제기구에서근무하고있는자 | text | 100% |  |
| `자로서재정경제부장관이정하는자` | 자로서재정경제부장관이정하는자 | text | 100% |  |
| `수행원이나사용인` | 수행원이나사용인 | text | 100% |  |
| `비거주자입증서류` | ■비거주자입증서류(다음중택1) | text | 100% |  |
| `영업활동입증서류` | 영업활동입증서류 | text | 100% |  |

### 연간사업실적보고서(투자잔액 1,000만불 초과 기업) (`hf206`) — 키 86개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `투자자명담당자` | 투자자명담당자 | text | 100% | 안기은 |
| `company.biz_item` | 업종(중분류) | text | 100% | 무역 |
| `check.투자자법인성격` | 투자자법인성격 | checkbox | 100% | 실제영업법인 |
| `check.외국인투자기업2여부` | 외국인투자기업2)여부 | checkbox | 100% | 아니오 |
| `check.예` | 예 | checkbox | 100% | 예 |
| `자기자본` | 자기자본 | number | 100% | 3,940,000 |
| `계열명` | 계열명 | text | 100% |  |
| `사후관리은행` | 사후관리은행 | text | 100% | 하나은행 |
| `법인명1` | 법인명1 | text | 100% | (주)가온정밀 |
| `소재지2` | 소재지(국가,주,성)2) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `투자업종3` | 투자업종3 | text | 100% |  |
| `설립등기일` | 설립등기일 | date | 100% | 2027년 7월 29일 |
| `check.법인성격` | 법인성격 | checkbox | 100% | 실제영업법인 |
| `check.투자형태6` | 투자형태6 | checkbox | 100% | 공동투자 |
| `check.지배구조` | 지배구조 | checkbox | 100% | 지주회사 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `주요취급품목4` | 주요취급품목4 | text | 100% | 기계 부품 |
| `영업개시일` | 영업개시일 | date | 100% | 2025.10.16 |
| `check.설립형태` | 설립형태 | checkbox | 100% | 기존법인 지분인수 |
| `전화` | 전화 | phone | 100% | 010-5907-7253 |
| `임원` | 임원 | text | 100% |  |
| `주주현황7_목록[].국가` | 국가 | text | 100% | 미국 |
| `주주현황7_목록[].상호또는성명` | 상호또는성명 | text | 100% | (주)유니온무역 |
| `상호또는성명` | 상호또는성명 | text | 100% | 새한푸드 |
| `한국투자자지분율합` | 한국투자자지분율합(B) | number | 100% | 60 |
| `주주현황7_목록[].금기말` | 금기말 | text | 100% |  |
| `주주현황7_목록[].전기말` | 전기말 | text | 100% |  |
| `천미불` | 천미불 | number | 100% | 30 |
| `주주현황7_목록[].계열여부` | 계열여부 | text | 100% |  |
| `기타` | 기타 | text | 100% | 계좌 정리 |
| `기타2` | 기타 | text | 100% | 결혼자금 |
| `지분율10이상투자자` | -지분율10%이상투자자 | text | 100% |  |
| `주투자자관계사1` | 주투자자관계사1 | text | 100% |  |
| `기타3` | 기타 | text | 100% | 학자금 |
| `계` | 계(A) | text | 100% |  |
| `지분율10이상투자자2` | -지분율10%이상투자자 | text | 100% |  |
| `주투자자관계사12` | 주투자자관계사1 | text | 100% |  |
| `기타4` | 기타 | text | 100% | 주택구입 |
| `계2` | 계(B) | text | 100% |  |
| `합계` | 합계(A+B) | number | 100% | 4,190,000 |
| `대부투자_목록[].금기말` | 금기말 | text | 100% |  |
| `지분율10미만_목록[].금기말` | 금기말 | text | 100% |  |
| `지분투자` | 지분투자 | text | 100% |  |
| `대부투자` | 대부투자(대여금및채권인수) | text | 100% |  |
| `매출채권` | 매출채권 | number | 100% | 191,110,000원 |
| `목록[].금기말` | 금기말 | text | 100% |  |
| `목록[].전기말` | 전기말 | text | 100% |  |
| `배당금` | 배당금 | text | 100% |  |
| `목록[].이자` | 이자 | number | 100% | 36,300,000 |
| `지급총액` | 지급총액 | number | 100% | 80,410,000원 |
| `한국투자자앞지급액` | 한국투자자앞지급액 | text | 100% |  |
| `한국투자자앞대부이자지급액` | 한국투자자앞대부이자지급액 | number | 100% | 630,000 |
| `한국투자자앞로얄티등기타지급액` | 한국투자자앞로얄티등기타지급액 | text | 100% |  |
| `한국인근로자앞임금지급액` | 한국인근로자앞임금지급액 | text | 100% |  |
| `채권인수` | 채권인수(단위:천미불) | text | 100% |  |
| `목록[].차입처` | 차입처 | text | 100% | 대성정밀(주) |
| `차입처` | 차입처 | text | 100% | 미래메디칼 |
| `목록[].코드1` | 코드1 | text | 100% | 8241 |
| `목록[].차입금액` | 차입금액 | text | 100% | 920,000 |
| `목록[].보증자` | 보증자 | text | 100% | (주)유니온무역 |
| `보증자` | 보증자 | text | 100% | 주식회사 우진전자 |
| `목록[].년미만` | 년미만 | text | 100% |  |
| `목록[].년이상` | 년이상 | text | 100% |  |
| `목록[].변동2` | 변동2 | text | 100% |  |
| `목록[].고정` | 고정 | text | 100% |  |
| `목록[].용도3` | 용도3 | text | 100% | 하나 정기예금 |
| `금액` | 금액 | number | 100% | 8,520,000 |
| `비중` | 비중 | text | 100% |  |
| `목록[].기타` | 기타 | text | 100% | 투자 목적 |
| `목록[].한국투자자앞` | 한국투자자앞 | text | 100% |  |
| `목록[].관계회사앞` | 관계회사앞 | text | 100% |  |
| `목록[].계` | 계 | text | 100% |  |
| `금액2` | 금액 | number | 100% | 17,180,000원 |
| `비중2` | 비중 | text | 100% |  |
| `목록[].전기` | 전기 | text | 100% |  |
| `자산총계` | 자산총계 | text | 100% |  |
| `목록[].금기` | 금기 | text | 100% |  |
| `부채총계` | 부채총계 | text | 100% |  |
| `자본총계` | 자본총계 | text | 100% |  |
| `부채및자본총계` | 부채및자본총계 | text | 100% |  |
| `check.현지법인운영상애로사항` | 현지법인운영상애로사항(복수선택가능) | checkbox | 100% | 분쟁해결 절차 |
| `대정부건의사항` | 대정부건의사항 | text | 100% |  |
| `철수` | 철수 | text | 100% |  |
| `투자축소` | 투자축소 | text | 100% |  |
| `현상유지` | 현상유지 | text | 100% |  |
| `국가명` | 국가명 | text | 100% | 영국 |

### 연간사업실적보고서(투자잔액 300만불 초과 1,000만불 이하 기업) (`hf207`) — 키 67개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `투자자명담당자` | 투자자명담당자 | text | 100% | 선민인 |
| `업종1` | 업종(중분류)1) | text | 100% |  |
| `check.투자자법인성격` | 투자자법인성격 | checkbox | 100% | 특수목적회사(SPC) |
| `check.외국인투자기업2여부` | 외국인투자기업2)여부 | checkbox | 100% | 아니오 |
| `check.예` | 예 | checkbox | 100% | 예 |
| `자기자본` | 자기자본 | number | 100% | 31,050,000원 |
| `계열명` | 계열명 | text | 100% |  |
| `사후관리은행` | 사후관리은행 | text | 100% | 신한은행 |
| `check.법인성격` | 법인성격 | checkbox | 100% | 특수목적회사(SPC) |
| `check.투자형태7` | 투자형태7 | checkbox | 100% | 단독투자 |
| `check.지배구조` | 지배구조 | checkbox | 100% | 비지주회사 |
| `법인명1` | 법인명1 | text | 100% | 우진정밀 |
| `소재지2` | 소재지(국가,주,성)2) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `투자업종3` | 투자업종3 | text | 100% |  |
| `설립등기일` | 설립등기일 | date | 100% | 2027.07.04 |
| `주주구성_목록[].상호또는성명` | 상호또는성명 | text | 100% | 주식회사 한빛패션 |
| `주주구성_목록[].국가` | 국가 | text | 100% | 캐나다 |
| `주주구성_목록[].지분율` | 지분율(%) | number | 100% | 70 |
| `check.설립형태` | 설립형태 | checkbox | 100% | 기존법인 지분인수 |
| `company.ceo` | 대표자 | text | 100% | 강순준 |
| `주요취급품목4` | 주요취급품목4 | text | 100% | 산업용 펌프 |
| `영업개시일` | 영업개시일 | date | 100% | 2025.05.24 |
| `주주구성_목록[].순투자액5` | 순투자액(천미불)5) | text | 100% |  |
| `전화` | 전화 | phone | 100% | 010-3347-9183 |
| `임원` | 임원 | text | 100% |  |
| `지분투자` | 지분투자 | text | 100% |  |
| `대부투자` | 대부투자(대여금및채권인수) | text | 100% |  |
| `목록[].금기말` | 금기말 | text | 100% |  |
| `목록[].전기말` | 전기말 | text | 100% |  |
| `배당금` | 배당금 | text | 100% |  |
| `이자` | 이자 | number | 100% | 590,000 |
| `지급총액` | 지급총액 | number | 100% | 47,920,000 |
| `한국투자자앞지급액` | 한국투자자앞지급액 | text | 100% |  |
| `한국투자자앞대부이자지급액` | 한국투자자앞대부이자지급액 | number | 100% | 920,000 |
| `한국투자자앞로얄티등기타지급액` | 한국투자자앞로얄티등기타지급액 | text | 100% |  |
| `한국인근로자앞임금지급액` | 한국인근로자앞임금지급액 | text | 100% |  |
| `목록[].차입처` | 차입처 | text | 100% | (주)유니온무역 |
| `차입처` | 차입처 | text | 100% | (주)유니온무역 |
| `목록[].코드1` | 코드1 | text | 100% | 42099 |
| `목록[].차입금액` | 차입금액 | text | 100% | 48,810,000 |
| `목록[].보증자` | 보증자 | text | 100% | (주)유니온무역 |
| `보증자` | 보증자 | text | 100% | 삼정정밀 |
| `목록[].년미만` | 년미만 | text | 100% |  |
| `목록[].년이상` | 년이상 | text | 100% |  |
| `목록[].변동2` | 변동2 | text | 100% |  |
| `목록[].고정` | 고정 | text | 100% |  |
| `목록[].용도3` | 용도3 | text | 100% | 하나 적금 |
| `금액` | 금액 | number | 100% | 39,010,000 |
| `비중` | 비중 | text | 100% |  |
| `목록[].기타` | 기타 | text | 100% | 투자 목적 |
| `목록[].한국투자자앞` | 한국투자자앞 | text | 100% |  |
| `목록[].관계회사앞` | 관계회사앞 | text | 100% |  |
| `목록[].계` | 계 | text | 100% |  |
| `금액2` | 금액 | number | 100% | 29,250,000원 |
| `비중2` | 비중 | text | 100% |  |
| `목록[].전기` | 전기 | text | 100% |  |
| `자산총계` | 자산총계 | text | 100% |  |
| `목록[].금기` | 금기 | text | 100% |  |
| `부채총계` | 부채총계 | text | 100% |  |
| `자본총계` | 자본총계 | text | 100% |  |
| `부채및자본총계` | 부채및자본총계 | text | 100% |  |
| `check.현지법인운영상애로사항` | 현지법인운영상애로사항(복수선택가능) | checkbox | 100% | 금융 |
| `대정부건의사항` | 대정부건의사항 | text | 100% |  |
| `철수` | 철수 | text | 100% |  |
| `투자축소` | 투자축소 | text | 100% |  |
| `현상유지` | 현상유지 | text | 100% |  |
| `국가명` | 국가명 | text | 100% | 캐나다 |

### 지급확인서 (`hf208`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `지급사유` | 지급사유 | text | 100% | 의료비 |
| `수취인` | 수취인 | text | 100% | (주)유니온무역 |
| `수취인과의관계` | 수취인과의관계 | text | 100% | 한빛테크(주) |
| `customer.rrn` | 주민번호(사업자등록번호) | rrn | 100% | 900210-1659382 |
| `customer.phone` | 전화번호 | phone | 100% | 010-3347-9183 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 강순준 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 지정거래외국환은행의장 | text | 100% | 박찬연 |
| `seal.signer2` | 지정거래외국환은행의장 | seal | 100% | 박찬연 |
| `sign.signer2` | 지정거래외국환은행의장 | signature | 100% | 강순준 |

### 영수확인서 (`hf209`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `무역` | 무역 | text | 100% |  |
| `용역및서비스` | 용역및서비스 | text | 100% |  |
| `증여` | 증여 | text | 100% |  |
| `기타` | 기타 | text | 100% | 의료비 |
| `송금인` | 송금인 | text | 100% |  |
| `송금인과관계` | 송금인과관계 | text | 100% |  |
| `customer.rrn` | 주민번호(사업자등록번호) | rrn | 100% | 900210-1659382 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 인 | text | 100% | 박찬연 |
| `seal.signer` | 인 | seal | 100% | 현예지 |
| `sign.signer` | 인 | signature | 100% | 박찬연 |

### 대북투자 신고 및 투자실적 보고서 (`hf210`) — 키 40개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `date` | 일자 | date | 100% | 2026.01.31 |
| `목록[].투자자` | 투자자 | text | 100% |  |
| `기업규모1` | 기업규모1 | text | 100% |  |
| `목록[].현지법인명` | 현지법인명 | text | 100% | (주)유니온물산 |
| `투자지역2` | 투자지역2 | text | 100% |  |
| `업종3` | 업종3 | text | 100% |  |
| `투자방법4` | 투자방법4 | text | 100% |  |
| `비율` | 비율 | number | 100% | 40 |
| `목록[].현금` | 현금 | text | 100% |  |
| `현물` | 현물 | text | 100% |  |
| `기타` | 기타 | text | 100% | 학자금 |
| `합작투자자` | 합작(합영)투자자 | text | 100% |  |
| `신고기관` | 신고기관 | text | 100% |  |
| `비고4` | 비고4 | text | 100% | 만기 해지 |
| `목록[].신고일자` | 신고일자 | date | 100% | 2025년 6월 21일 |
| `목록[].신고금액` | 신고금액 | number | 100% | 470,000 |
| `투자일자` | 투자일자 | date | 100% | 2025.03.29 |
| `투자방법주` | 투자방법주 | text | 100% |  |
| `이익잉여금등기타` | 이익잉여금등기타 | text | 100% | 결혼자금 |
| `신규증액` | 신규·증액 | text | 100% |  |
| `투자자명` | 투자자명 | text | 100% |  |
| `구분주` | 구분주 | text | 100% |  |
| `취득일` | 취득일 | date | 100% | 2025년 6월 2일 |
| `취득금액` | 취득금액 | number | 100% | 3,840,000 |
| `date2` | 신고일자 | date | 100% | 2026.01.31 |
| `외환매입일자` | 외환매입일자 | date | 100% | 2025.03.25 |
| `매입금액` | 매입금액 | number | 100% | 1,270,000 |
| `투자국` | 투자국 | text | 100% |  |
| `date3` | 일자 | date | 100% | 2026.01.31 |
| `투자지역` | 투자지역 | text | 100% |  |
| `투자방법` | 투자방법 | text | 100% |  |
| `비율2` | 비율 | number | 100% | 50 |
| `회수내역주` | 회수내역주 | text | 100% |  |
| `회수금액` | 회수(실효)금액 | number | 100% | 99,510,000 |
| `합작투자자2` | 합작(합영)투자자 | text | 100% |  |
| `비고` | 비고 | text | 100% | 주택구입 |
| `구분주2` | 구분주 | text | 100% |  |
| `변경일자` | 변경일자 | date | 100% | 2025.06.04 |
| `변경전` | 변경전 | text | 100% | 급여 수령 |
| `변경후` | 변경후 | text | 100% | 의료비 |

### 사업계획서 (`hf211`) — 키 60개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `상호또는성명` | 상호또는성명 | text | 100% | (주)유니온무역 |
| `company.address` | 소재지(주소) | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `check.투자자규모` | 투자자규모 | checkbox | 100% | 개인사업자 |
| `check.투자자법인성격` | 투자자법인성격 | checkbox | 100% | 특수목적회사(SPC)1) |
| `check.외국인투자기업2여부` | 외국인투자기업2)여부 | checkbox | 100% | 아니오 |
| `총자산` | 총자산 | number | 100% | 98,520,000 |
| `company.biz_item` | 업종(제품) | text | 100% | 무역 |
| `check.예` | 예 | checkbox | 100% | 예 |
| `설립년월일` | 설립년월일 | date | 100% | 2025.03.05 |
| `자기자본` | 자기자본(자본금) | text | 100% |  |
| `담당자및연락처` | 담당자및연락처 | phone | 100% | 010-5907-7253 |
| `company.name` | 법인명 | text | 100% | (주)유니온무역 |
| `check.법인형태` | 법인형태 | checkbox | 100% | 법인 |
| `check.법인형태2` | 법인형태 | checkbox | 100% | 법인설립 |
| `총자본금` | 총자본금 | text | 100% |  |
| `check.투자형태1` | 투자형태1 | checkbox | 100% | 단독투자 |
| `check.투자유형2` | 투자유형2 | checkbox | 100% | M&A |
| `check.법인성격` | 법인성격 | checkbox | 100% | 실제 영업법인 |
| `check.지배구조` | 지배구조 | checkbox | 100% | 지주회사 |
| `check.투자목적` | 투자목적(택일) | checkbox | 100% | 수출촉진 |
| `company.name2` | 상호 | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표자명 | text | 100% | 박찬연 |
| `company.ceo2` | 대표자 | text | 100% | 박찬연 |
| `check.년월일` | 년월일 | checkbox | 100% | 자본금 미납입 |
| `company.biz_no` | 사업자번호 | biz_no | 100% | 264-82-36559 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 120111-4500915 |
| `check.설립형태` | 설립형태 | checkbox | 100% | 신설법인 설립 |
| `check.증권투자` | 증권투자(1.신규투자2.증액투자) | checkbox | 100% | 제재기관 보고후 사후신고 |
| `지분율이50를초과할경우최대주주의최대주주소속국가` | 지분율이50%를초과할경우최대주주의최대주주소속국가 | number | 100% | 60 |
| `취득증권_목록[].증권종류` | 증권종류 | text | 100% |  |
| `취득증권_목록[].주수` | 주수 | text | 100% |  |
| `주당액면` | 주당액면 | text | 100% |  |
| `취득가액이액면과상이할경우그산출근거1` | 취득가액이액면과상이할경우그산출근거1 | number | 100% | 21,600,000원 |
| `취득증권_목록[].주당가액` | 주당가액 | number | 100% | 297,320,000 |
| `현금` | 현금 | text | 100% |  |
| `주식` | 주식 | text | 100% |  |
| `기술투자` | 기술투자 | text | 100% |  |
| `현물` | 현물 | text | 100% |  |
| `이익잉여금` | 이익잉여금 | text | 100% |  |
| `기타` | 기타() | text | 100% | 타행 이체 |
| `한국측` | 한국측(1) | text | 100% |  |
| `한국측2` | 한국측(1) | text | 100% |  |
| `한국측3` | 한국측(1) | text | 100% |  |
| `한국측4` | 한국측(1) | text | 100% |  |
| `한국측5` | 한국측(1) | text | 100% |  |
| `현지측` | 현지측(2) | text | 100% |  |
| `제3국` | 제3국(3) | text | 100% |  |
| `한국측_목록[].금액` | 금액 | text | 100% | 2,140,000 |
| `목록[].금액` | 금액 | text | 100% | 3,060,000 |
| `합계` | 합계(1+2+3) | number | 100% | 24,520,000 |
| `한국측_목록[].비율` | 비율(%) | text | 100% | 100 |
| `목록[].비율` | 비율(%) | text | 100% | 100 |
| `대부액` | 대부액 | text | 100% |  |
| `이율` | 이율 | number | 100% | 10 |
| `원금상환방법` | 원금상환방법 | number | 100% | 820,000 |
| `자기자금` | 자기자금 | text | 100% |  |
| `자금용도` | 자금용도 | text | 100% | 급여 수령 |
| `기간` | 기간 | text | 100% |  |
| `이자징수방법` | 이자징수방법 | number | 100% | 27,060,000 |
| `차입금` | 차입금 | text | 100% |  |

### 해외직접투자 신고서(보고서) (`hf212`) — 키 27개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 상호 | text | 100% | (주)유니온무역 |
| `signer.name` | 대표자 | text | 100% | 박찬연 |
| `seal.signer` | 대표자 | seal | 100% | 박찬연 |
| `sign.signer` | 대표자 | signature | 100% | 강순준 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `투자국명` | 투자국명 | text | 100% | 독일 |
| `투자방법` | 투자방법 | text | 100% |  |
| `투자업종` | 투자업종 | text | 100% |  |
| `투자금액` | 투자금액 | number | 100% | 32,970,000 |
| `투자비율` | 투자비율 | number | 100% | 100 |
| `투자목적` | 투자목적 | text | 100% | 주택구입 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `customer.rrn` | 주민등록번호 | rrn | 100% | 900210-1****** |
| `company.address` | 소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `자금조달` | 자금조달 | text | 100% |  |
| `주요제품` | 주요제품 | text | 100% |  |
| `출자금액` | 출자금액 | number | 100% | 5,230,000원 |
| `결산월` | 결산월 | text | 100% |  |
| `투자유형` | 투자유형 | text | 100% |  |
| `신고번호` | 신고번호 | text | 100% | 4529-4504 |
| `신고금액` | 신고금액 | number | 100% | 5,130,000 |
| `유효기간` | 유효기간 | text | 100% |  |
| `해외직접투자신고서` | 해외직접투자신고서(보고서) | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `위와같이신고되었음을확인함` | 위와같이신고(보고)되었음을확인함 | text | 100% |  |

### 사전 송금방식 수입대금 지급시 (`hf213`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.사전송금방식` | 사전송금방식 | checkbox | 100% | 사전 송금방식 |
| `check.대금송금후물품수령예정일` | 대금송금후물품(선적서류)수령예정일 | checkbox | 100% | 년 이내 |
| `check.대금송금후물품수령예정일2` | 대금송금후물품(선적서류)수령예정일 | checkbox | 100% | 년 초과 |
| `check.중계무역` | 중계무역 | checkbox | 100% | 중계무역 |
| `check.현재수출계약체결` | 현재수출계약체결 | checkbox | 100% | 현재 수출계약 체결 |
| `check.현재수출계약미체결` | 현재수출계약미체결 | checkbox | 100% | 현재 수출계약 미체결 |
| `check.사후송금방식` | 사후송금방식 | checkbox | 100% | 사후 송금방식 |
| `check.일반수입` | 일반수입 | checkbox | 100% | 일반 수입 |
| `check.외국인수수입` | 외국인수수입 | checkbox | 100% | 외국인수수입 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 고객명 | text | 100% | 박찬연 |
| `seal.signer` | 고객명 | seal | 100% | 최우빈 |
| `sign.signer` | 고객명 | signature | 100% | 이욱유 |
| `본서식의작성대상이아님` | →본서식의작성대상이아님 | text | 100% |  |
| `수입물품을국내에서인수하는경우` | :수입물품을국내에서인수하는경우 | text | 100% | 포장재 |

### 자본거래 사후보고 확인서 (`hf214`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 신청인 | text | 100% | 박찬연 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.rrn` | 주민(사업자)번호 | rrn | 100% | 900210-1659382 |
| `customer.email` | 이메일주소 | text | 100% | chanyeon363@naver.com |
| `check.거주자의미화5천만불이하` | 거주자의미화5천만불이하외화자금차입(증권발행포함)(규정제7- | checkbox | 100% | 거주자의 미화 5천만불 이하 외화자금 차입(증권발행 포함) (규정 제7- |
| `check.현지법인등의외화자금차입` | 현지법인등의외화자금차입(규정제7-14조의2,제7-18조) | checkbox | 100% | 현지법인등의 외화자금 차입 (규정 제7-14조의2, 제7-18조) |
| `check.현지법인에대한1년미만의` | 현지법인에대한1년미만의금전대여(규정제7-16조) | checkbox | 100% | 현지법인에 대한 1년 미만의 금전대여 (규정 제7-16조) |
| `check.거주자와비거주자간채무의` | 거주자와비거주자간채무의보증계약에따른자본거래(규정제7-18조) | checkbox | 100% | 거주자와 비거주자간 채무의 보증계약에 따른 자본거래 (규정 제7-18조) |
| `check.거주자의외국부동산시설물` | 거주자의외국부동산·시설물이용에관한권리취득(규정제7-21조 | checkbox | 100% | 거주자의 외국부동산 · 시설물 이용에 관한 권리 취득 (규정 제7-21조 |
| `check.거자와비거주자간임대차계` | 거자와비거주자간임대차계약(규정제7-46조) | checkbox | 100% | 거자와 비거주자간 임대차 계약 (규정 제7-46조) |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 이욱유 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |

### 상호계산계정 결산대차기잔액처분(변경)신고서 (`hf215`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `금액` | 금액 | number | 100% | 146,380,000 |
| `송금처` | 송금처 | text | 100% |  |
| `송금방법` | 송금방법 | text | 100% |  |
| `송금은행` | 송금은행 | text | 100% | 하나은행 |
| `신고번호` | 신고번호 | text | 100% | 3859-0629 |
| `유효기간` | 유효기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 명 | text | 100% | 박찬연 |
| `seal.signer` | 명 | seal | 100% | 강순준 |
| `sign.signer` | 명 | signature | 100% | 박찬연 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer2` | 은행장 | seal | 100% | 강순준 |
| `sign.signer2` | 은행장 | signature | 100% | 박찬연 |

### 해외부동산 취득신고(수리)서 (`hf216`) — 키 36개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.본신고` | 본신고 | checkbox | 100% | 내신고 |
| `취득가액` | 취득가액 | number | 100% | 330,000 |
| `총취득금액` | 총취득금액(A=B+C) | number | 100% | 53,190,000 |
| `signer.name` | 성명(법인명) | text | 100% | 박찬연 |
| `seal.signer` | 성명(법인명) | seal | 100% | 최우빈 |
| `sign.signer` | 성명(법인명) | signature | 100% | 박찬연 |
| `company.biz_item` | 업종(직업) | text | 100% | 무역 |
| `check.부동산의종류` | 부동산의종류 | checkbox | 100% | 상가 |
| `check.취득목적` | 취득목적 | checkbox | 100% | 주거이외(투자등) |
| `company.address` | 소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `면적` | 면적 | text | 100% |  |
| `수취인명` | 수취인명 | text | 100% | 우진테크(주) |
| `신고인과의관계` | 신고인과의관계 | text | 100% |  |
| `총취득금액2` | 총취득금액(A=B+C) | number | 100% | 26,090,000 |
| `취득자금국내송금액` | 취득자금국내송금액 | number | 100% | 54,720,000 |
| `모기지론` | 모기지론(원리금상환송금예정금액) | text | 100% |  |
| `모기지론2` | 모기지론(원리금상환현지조달금액) | text | 100% |  |
| `기타` | 기타:() | text | 100% | 계좌 정리 |
| `수취인명2` | 수취인명 | text | 100% | (주)제일상사 |
| `check.신고인과의관계` | 신고인과의관계 | checkbox | 100% | 본인 |
| `customer.rrn` | 주민(사업자)등록번호 | rrn | 100% | 900210-1****** |
| `신고번호` | 신고(수리)번호 | text | 100% | 8096-6616 |
| `신고금액` | 신고(수리)금액 | number | 100% | 7,580,000 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `미달러환산액` | 미달러환산액 | text | 100% |  |
| `국내송금액_목록[].미달러환산액` | 미달러환산액 | text | 100% |  |
| `현지조달액_목록[].미달러환산액` | 미달러환산액 | text | 100% |  |
| `미달러환산액2` | 미달러환산액 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고수리기관 | text | 100% | 박찬연 |
| `seal.signer2` | 신고수리기관 | seal | 100% | 현예지 |
| `sign.signer2` | 신고수리기관 | signature | 100% | 박찬연 |
| `명` | 명(법인명) | text | 100% |  |
| `위의신고를다음과같이신고수리함` | 위의신고를다음과같이신고수리함. | text | 100% |  |

### 해외직접투자 내용변경 신고(보고)서 (`hf217`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `변경사항` | 변경사항 | text | 100% |  |
| `변경사유` | 변경사유(요약) | text | 100% | 학자금 |
| `목록[].변경후` | 변경후 | text | 100% | 투자 목적 |
| `신고번호` | 신고번호 | text | 100% | 3081-1770 |
| `check.현지법인내용변경` | 현지법인내용변경 | checkbox | 100% | 기타 |
| `signer.name` | 상호또는성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호또는성명 | seal | 100% | 주식회사 대성패션 |
| `sign.signer` | 상호또는성명 | signature | 100% | 주식회사 한빛패션 |
| `변경대상현지법인명` | 변경대상현지법인명 | text | 100% | (주)유니온무역 |
| `signer2.name` | 신고기관 | text | 100% | 박찬연 |
| `seal.signer2` | 신고기관 | seal | 100% | 강순준 |
| `sign.signer2` | 신고기관 | signature | 100% | 이욱유 |
| `company.biz_no` | 사업자(주민)번호 | biz_no | 100% | 264-82-36559 |
| `소재지또는주소` | 소재지또는주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `전화` | 전화 | phone | 100% | 010-5907-7253 |
| `대상신고번호` | 대상신고번호 | text | 100% | 2130-2477 |
| `date` | 신고일자 | date | 100% | 2026.01.31 |
| `신고금액` | 신고금액 | number | 100% | 85,450,000 |

### 서약서(개인의 외국주택 취득) (`hf218`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 신고인성명 | text | 100% | 박찬연 |
| `seal.signer` | 신고인성명 | seal | 100% | 이민빈 |
| `sign.signer` | 신고인성명 | signature | 100% | 박찬연 |
| `signer2.name` | 배우자성명* | text | 100% | 박찬연 |
| `seal.signer2` | 배우자성명* | seal | 100% | 박찬연 |
| `sign.signer2` | 배우자성명* | signature | 100% | 강순준 |
| `check.지정거래외국환은행의장으` | 지정거래외국환은행의장으로부터신고수리를받아외국주택을취득한자는외 | checkbox | 100% | 지정거래외국환은행의 장으로부터 신고수리를 받아 외국주택을 취득한 자는 외 |
| `check.사후보고서의제출등추가적` | 사후보고서의제출등추가적인문의사항이있거나,신고인의주소(해외체 | checkbox | 100% | 사후 보고서의 제출 등 추가적인 문의사항이 있거나, 신고인의 주소(해외체 |
| `부동산취득자금송금후3개월이내` | 부동산취득자금송금후3개월이내 | text | 100% |  |
| `부동산처분후3개월이내` | 부동산처분(변경)후3개월이내 | text | 100% |  |
| `수시보고서` | 수시보고서* | text | 100% |  |
| `매2년마다보유사실입증서류` | 매2년마다보유사실입증서류 | text | 100% |  |

### 해외사무소 설치(변경)신고서 (`hf219`) — 키 23개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호 | seal | 100% | 주식회사 한빛패션 |
| `sign.signer` | 상호 | signature | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자(주민)번호 | biz_no | 100% | 264-82-36559 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `check.기업규모` | 기업규모 | checkbox | 100% | 중소기업 |
| `check.구분` | 구분 | checkbox | 100% | 변경 |
| `value` | (표준산업분류코드5자리) | amount | 100% |  |
| `설치사유` | 설치사유 | text | 100% | 의료비 |
| `내용` | 내용 | text | 100% | 전세자금 |
| `사유` | 사유 | text | 100% | 타행 이체 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `신고번호` | 신고번호 | text | 100% | 297-598748-80207 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고(보고)기관 | text | 100% | 박찬연 |
| `seal.signer2` | 신고(보고)기관 | seal | 100% | 이욱유 |
| `sign.signer2` | 신고(보고)기관 | signature | 100% | 박찬연 |
| `company.name` | 상호 | text | 100% | (주)유니온무역 |
| `위의신청을다음과같이신고필함` | 위의신청을다음과같이신고필함. | text | 100% |  |

### 해외지점 설치(변경)신고서 (`hf220`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호 | seal | 100% | 주식회사 미래커뮤니케이션 |
| `sign.signer` | 상호 | signature | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자(주민)번호 | biz_no | 100% | 264-82-36559 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `check.기업규모` | 기업규모 | checkbox | 100% | 대기업 |
| `check.구분` | 구분 | checkbox | 100% | 설치 |
| `value` | (표준산업분류코드5자리) | amount | 100% |  |
| `설치사유` | 설치사유 | text | 100% | 의료비 |
| `내용` | 내용 | text | 100% | 해외 이주 |
| `사유` | 사유 | text | 100% | 전세자금 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 120111-4500915 |
| `신고번호` | 신고번호 | text | 100% | 450550-7671658 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고(보고)기관 | text | 100% | 박찬연 |
| `seal.signer2` | 신고(보고)기관 | seal | 100% | 박찬연 |
| `sign.signer2` | 신고(보고)기관 | signature | 100% | 현예지 |
| `company.name` | 상호 | text | 100% | (주)유니온무역 |

### 해외지사 설치·현황 보고서 (`hf221`) — 키 26개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `date` | 일자 | date | 100% | 2026.01.31 |
| `목록[].신고자` | 신고자 | text | 100% | 가온상사(주) |
| `목록[].사업자번호` | 사업자(주민)번호 | biz_no | 100% | 264-82-36559 |
| `기업규모1` | 기업규모1 | text | 100% |  |
| `목록[].지사명` | 지사명 | text | 100% | 청솔물산 |
| `목록[].설치국가` | 설치국가 | text | 100% | 중국 |
| `구분2` | 구분2 | text | 100% |  |
| `신고기관` | 신고기관 | text | 100% |  |
| `date2` | 신고일자 | date | 100% | 2026.01.31 |
| `송금일자` | 송금일자 | date | 100% | 2025.09.20 |
| `송금내역` | 송금내역 | text | 100% |  |
| `date3` | 일자 | date | 100% | 2026.01.31 |
| `해외지사명` | 해외지사명 | text | 100% | (주)누리시스템즈 |
| `설치국가` | 설치국가 | text | 100% | 독일 |
| `회수구분주` | 회수구분주 | text | 100% |  |
| `회수금액` | 회수금액 | number | 100% | 282,980,000 |
| `비고` | 비고 | text | 100% | 본인 요청 |
| `구분주` | 구분주 | text | 100% |  |
| `변경일자` | 변경일자 | date | 100% | 2025-03-18 |
| `변경전` | 변경전 | text | 100% | 본인 요청 |
| `변경후` | 변경후 | text | 100% | 급여 수령 |
| `지사명` | 지사명 | text | 100% | (주)신영전자 |
| `취득일` | 취득일 | date | 100% | 2025.10.16 |
| `취득금액` | 취득금액 | number | 100% | 110,000 |
| `처분일` | 처분일 | date | 100% | 2025.09.30 |
| `처분금액` | 처분금액 | number | 100% | 320,000 |

### 해외 부동산 취득 보고서 (`hf222`) — 키 19개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `부동산취득명의인` | 부동산취득명의인 | text | 100% | 심주연 |
| `가성명또는법인명` | 가.성명또는법인명 | text | 100% | (주)유니온무역 |
| `나주민등록번호` | 나.주민등록번호(사업자등록번호) | text | 100% | 225895-1031150 |
| `다주소또는소재지` | 다.주소또는소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `가성명또는법인명2` | 가.성명또는법인명 | text | 100% | 주식회사 새한시스템즈 |
| `나주민등록번호2` | 나.주민등록번호(사업자등록번호) | text | 100% | 4160-6080 |
| `다주소또는소재지2` | 다.주소또는소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `가상호또는성명` | 가.상호또는성명 | text | 100% | (주)유니온무역 |
| `나주소또는소재지` | 나.주소또는소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `가신고수리에관한사항` | 가.신고수리에관한사항 | text | 100% |  |
| `부동산취득신고수리일및신고수리번호` | (1)부동산취득신고수리일및신고수리번호 | text | 100% | 256985-0621949 |
| `부동산취득등기일` | (2)부동산취득등기일 | date | 100% | 2025.07.04 |
| `종류` | (가)종류 | text | 100% | 하나 적금 |
| `건평` | (나)건평 | text | 100% |  |
| `대지` | (다)대지 | text | 100% |  |
| `company.address` | (2)소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `건물가격` | (가)건물가격 | text | 100% |  |
| `대지가격` | (나)대지가격 | text | 100% |  |
| `부대비` | (다)부대비 | text | 100% |  |

### 「외국환서식관리프로그램」전자무역업무이용(신규,변경,해지)신청서 (`hf223`) — 키 78개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.이용신청` | 이용신청 | checkbox | 100% | 지급지시업무 ( |
| `check.이용신청2` | 이용신청 | checkbox | 100% | goGlobal 전용 지급지시업무 |
| `변경신청_목록[].변경항목` | 변경항목 | text | 100% |  |
| `check.지정사업자` | 지정사업자 | checkbox | 100% | KTNet |
| `check.EDI` | EDI | checkbox | 100% | 일반응답 |
| `check.계산서발신업무` | 계산서발신업무 | checkbox | 100% | 신용장개설 |
| `check.기반사업자` | 기반사업자 | checkbox | 100% | uTradeHub |
| `check.eNego` | e-Nego | checkbox | 100% | e-Nego 업무 |
| `check.자동승인` | 자동승인 | checkbox | 100% | 내국신용장개설승인 |
| `지급지시업무관련출금계좌_목록[].예금과목` | 예금과목 | text | 100% | 하나 TDF 2040 |
| `신청인_목록[].수발신인식별자` | 수발신인식별자 | text | 100% |  |
| `지급지시업무관련출금계좌_목록[].계좌번호` | 계좌번호 | text | 100% | 373-577804-90189 |
| `수수료결제계좌번호` | 수수료결제계좌번호 | number | 100% | 176,360,000 |
| `변경신청_목록[].변경전` | 변경전 | text | 100% | 학자금 |
| `신청인_목록[].상세수발신식별자` | 상세수발신식별자 | text | 100% |  |
| `NET12` | NET12 | text | 100% |  |
| `지급지시업무관련출금계좌_목록[].예금주` | 예금주 | text | 100% |  |
| `변경신청_목록[].변경후` | 변경후 | text | 100% | 만기 해지 |
| `신청인_목록[].전자문서인증키` | 전자문서인증키 | text | 100% |  |
| `전자문서인증키` | 전자문서인증키 | text | 100% |  |
| `지급지시업무관련출금계좌_목록[].통화` | 통화 | text | 100% | USD |
| `seal.signer` | 인감대조 | seal | 100% | 강순준 |
| `sign.signer` | 인감대조 | signature | 100% | 최우빈 |
| `signer2.name` | 전자무역업무기본약관수령필 | text | 100% | 박찬연 |
| `seal.signer2` | 전자무역업무기본약관수령필 | seal | 100% | 강순준 |
| `sign.signer2` | 전자무역업무기본약관수령필 | signature | 100% | 박찬연 |
| `check.전자무역업무기본약관에따라아래와같이` | 『전자무역업무기본약관』에따라아래와같이( | checkbox | 100% | 변경, |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer3.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer3` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer3` | 신청인 | signature | 100% | 강순준 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `기재사항` | 기재사항 | text | 100% |  |
| `계산서` | 계산서 | text | 100% |  |
| `발신업무` | 발신업무 | text | 100% |  |
| `eNego` | e-Nego | text | 100% |  |
| `check.승인업무` | 승인업무 | checkbox | 100% | 승인업무 |
| `check.수입업무` | 수입업무 | checkbox | 100% | 수입업무 |
| `check.LC통지업무` | L/C통지업무(EDI) | checkbox | 100% | L/C 통지업무(EDI) |
| `check.내국신용장업무` | 내국신용장업무 | checkbox | 100% | 내국신용장업무 |
| `check.계산서및입출금통지업무` | 계산서및입출금통지업무 | checkbox | 100% | 계산서 및 입출금 통지업무 |
| `check.지급지시업무` | 지급지시업무 | checkbox | 100% | 지급지시업무 |
| `check.수출업무` | 수출업무 | checkbox | 100% | 수출업무 |
| `check.외화지급보증업무` | 외화지급보증업무 | checkbox | 100% | 외화지급보증업무 |
| `check.상호대사` | 상호대사 | checkbox | 100% | 일반응답 |
| `check.계산서발신업무2` | 계산서발신업무 | checkbox | 100% | 계산서발신업무 |
| `check.자동승인업무` | 자동승인업무 | checkbox | 100% | 자동승인업무 |
| `check.eLC통지업무` | e-L/C통지업무 | checkbox | 100% | e-L/C 통지업무 |
| `check.eNego업무` | e-Nego업무 | checkbox | 100% | e-Nego 업무 |
| `외화지급보증조건변경신청업무` | 외화지급보증/조건변경신청업무 | amount | 100% | AUD 169,500 |
| `상호대사일반응답` | 상호대사,일반응답 | text | 100% | 주식회사 대성정밀 |
| `check.Ο처리하실업무의` | Ο처리하실업무의 | checkbox | 100% | 에 V 표시를 하십시오 |
| `계산서업무입금통지업무출금통지업무` | 계산서업무,입금통지업무,출금통지업무 | text | 100% |  |
| `계좌입금통지출금통지당발송금출금통지` | 계좌입금통지,출금통지,당발송금출금통지 | text | 100% | 503-327712-82976 |
| `전자적매입신청업무` | 전자적매입신청업무 | text | 100% |  |
| `EDI` | EDI | text | 100% |  |
| `계산서발급업무` | 계산서발급업무 | text | 100% |  |
| `eLC` | e-L/C | text | 100% |  |
| `자동승인` | 자동승인 | text | 100% |  |
| `지급지시업무` | 지급지시업무 | text | 100% | 범어지점 |
| `수수료결제계좌번호2` | 수수료결제계좌번호 | number | 100% | 3,670,000 |
| `NET122` | NET12 | text | 100% |  |
| `전자문서인증키2` | 전자문서인증키 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer4` | 지점 | seal | 100% | 이욱유 |
| `sign.signer4` | 지점 | signature | 100% | 강순준 |
| `기재사항2` | 기재사항 | text | 100% |  |
| `약정항목eLC통지업무` | 약정항목:e-L/C통지업무 | text | 100% |  |
| `customer.name` | 신청인 | text | 100% | 박찬연 |
| `하나은행` | 하나은행 | text | 100% | 하나은행 |
| `수수료결제계좌번호3` | 수수료결제계좌번호 | number | 100% | 7,890,000 |
| `상세수발신인식별자` | 상세수발신인식별자 | text | 100% |  |
| `상세수발신인식별자2` | 상세수발신인식별자 | text | 100% |  |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer5` | 지점 | seal | 100% | 최우빈 |
| `sign.signer5` | 지점 | signature | 100% | 강순준 |
| `기재사항3` | 기재사항 | text | 100% |  |
| `계산서2` | 계산서 | text | 100% |  |

### Usance 송금 조건변경신청서 (`hf224`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신청인정보` | ♣신청인정보 | text | 100% |  |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `Usance송금번호` | Usance송금번호 | text | 100% | 7123-0491 |
| `통화금액` | 통화금액 | number | 100% | 150,000 |
| `수취인명` | 수취인명 | text | 100% | (주)삼정로지스 |
| `수취인주소및전화번호` | 수취인주소및전화번호 | phone | 100% | 010-5907-7253 |
| `수취인주소및전화번호2` | 수취인주소및전화번호 | phone | 100% | 010-5907-7253 |
| `수취인계좌번호` | 수취인계좌번호 | text | 100% | 389-373464-81713 |
| `수취은행BIC` | 수취은행BIC | text | 100% | 국민은행 |
| `check.만기` | 만기(상환일) | checkbox | 100% | Fixed due date ( |
| `check.만기2` | 만기(상환일) | checkbox | 100% | ( |
| `기타` | 기타 | text | 100% | 자녀 교육비 |
| `수취은행명` | 수취은행명 | text | 100% | 신한은행 |
| `영문` | 영문(English) | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 현예지 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |
| `signer2.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer2` | 신청인 | seal | 100% | 강순준 |
| `sign.signer2` | 신청인 | signature | 100% | 박찬연 |

### Usance 송금 신청서 (`hf225`) — 키 42개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신청정보` | ♣신청정보 | text | 100% |  |
| `신청인정보` | ♣신청인정보 | text | 100% |  |
| `영문` | 영문(English) | text | 100% |  |
| `한글` | 한글(Korean) | text | 100% |  |
| `check.수입형태사전송금방식만작성` | 수입형태*사전송금방식만작성 | checkbox | 100% | 사전 무통관수입(중계무역) |
| `check.만기` | 만기(상환일) | checkbox | 100% | Fixed due date ( |
| `check.거래방식` | 거래방식(선적구분) | checkbox | 100% | 사전송금 방식 (선적 전) |
| `선적정보` | ♣선적정보 | text | 100% |  |
| `계약서번호` | 계약서번호 | text | 100% | 930-181939-33410 |
| `상품명세` | 상품명세 | text | 100% | 전자부품 |
| `가격조건` | 가격조건 | text | 100% |  |
| `원산지` | 원산지 | text | 100% |  |
| `운송서류번호사후송금방식인경우작성` | 운송서류번호(B/LNo등)*사후송금방식인경우작성 | text | 100% | 231521-7711964 |
| `선적항` | (예정)선적항(또는공항) | text | 100% |  |
| `도착항` | (예정)도착항(또는공항) | text | 100% |  |
| `HS코드` | HS코드 | number | 100% | 2536 |
| `수출국` | 수출국 | text | 100% |  |
| `date` | 선적(예정)일 | date | 100% | 2026년 1월 31일 |
| `선적국가` | 선적국가 | text | 100% | 독일 |
| `도착국가` | 도착국가 | text | 100% | 필리핀 |
| `수취인명` | 수취인명 | text | 100% | (주)유니온무역 |
| `수취인주소및전화번호` | 수취인주소및전화번호 | phone | 100% | 010-5907-7253 |
| `수취인주소및전화번호2` | 수취인주소및전화번호 | phone | 100% | 010-7321-8870 |
| `수취인계좌번호` | 수취인계좌번호 | text | 100% | 714-595903-00985 |
| `수취은행BIC` | 수취은행BIC | text | 100% | 기업은행 |
| `송금수취인및수취은행정보` | ♣송금수취인및수취은행정보 | text | 100% | 농협은행 |
| `check.송금수수료부담자` | 송금수수료부담자 | checkbox | 100% | OUR |
| `수취은행명` | 수취은행명 | text | 100% | 국민은행 |
| `담당자명` | 담당자명 | text | 100% | 양승주 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `TELNo` | TELNo | text | 100% | 447-831247-23595 |
| `customer.email` | E-mail | text | 100% | chanyeon363@naver.com |
| `통화금액` | 통화(),금액 | number | 100% | 247,840,000 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `SWIFTCode` | SWIFTCode | text | 100% |  |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 현예지 |
| `signer2.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer2` | 신청인 | seal | 100% | 현예지 |
| `sign.signer2` | 신청인 | signature | 100% | 이욱유 |

### 거주자의 외화자금 차입 및 상환 현황보고서 (`hf226`) — 키 47개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].차주명` | 차주명 | text | 100% |  |
| `목록[].사업자등록번호` | 사업자등록번호 | biz_no | 100% | 125-18-88620 |
| `목록[].담당자성명` | 담당자성명 | text | 100% | 주욱성 |
| `목록[].담당자전화번호` | 담당자전화번호 | phone | 100% | 010-5907-7253 |
| `목록[].대주명` | 대주명 | text | 100% |  |
| `목록[].대주소재국` | 대주소재국 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `목록[].차입근거법1` | 차입근거법1 | text | 100% |  |
| `목록[].신고번호` | 신고번호 | text | 100% | 6507-9856 |
| `목록[].지정거래외국환은행지점명` | 지정거래외국환은행지점명 | text | 100% | 우리은행 |
| `목록[].자금용도` | 자금용도 | text | 100% | 하나 TDF 2040 |
| `목록[].계약통화` | 계약통화 | text | 100% | USD |
| `목록[].계약금액` | 계약금액(A) | text | 100% | 74,290,000 |
| `목록[].최초차입일자` | 최초차입일자 | date | 100% | 2025.04.26 |
| `목록[].만기일자` | 만기일자 | date | 100% | 2029년 6월 16일 |
| `목록[].기차입액` | 기차입액(B) | text | 100% |  |
| `목록[].당월차입일자` | 당월차입일자 | date | 100% | 2025-07-14 |
| `목록[].당월차입액` | 당월차입액(국내예치액)(C) | text | 100% |  |
| `목록[].차입누계` | 차입누계(D=B+C+L) | text | 100% |  |
| `목록[].미차입액` | 미차입액(E=A-D) | text | 100% |  |
| `목록[].기원금상환액` | 기원금상환액(F) | text | 100% | 640,000 |
| `목록[].당월상환일자` | 당월상환일자 | date | 100% | 2025.11.05 |
| `목록[].당월원금상환액` | 당월원금상환액(해외송금분)(G) | text | 100% | 191,360,000 |
| `목록[].상환잔액` | 상환잔액(I=D-F-G-H) | number | 100% | 5,790,000 |
| `목록[].당월이자상환액` | 당월이자상환액 | number | 100% | 6,060,000 |
| `목록[].해외예치일자` | 해외예치일자 | date | 100% | 2025.10.06 |
| `목록[].해외예치은행명` | 해외예치은행명 | text | 100% | 기업은행 |
| `목록[].해외예치은행BIC코드` | 해외예치은행BIC코드 | number | 100% | 1590 |
| `목록[].전월말예치잔액` | 전월말예치잔액(J) | text | 100% | 2,600,000 |
| `제출자` | 제출자 | text | 100% |  |
| `목록[].당월예치액` | 당월예치액(K=L+M) | text | 100% |  |
| `목록[].당월예치이자` | 당월예치이자(M) | text | 100% | 14,530,000 |
| `목록[].당월인출액` | 당월인출액(N=O+P) | text | 100% |  |
| `목록[].국내입금액` | 국내입금액(O) | text | 100% | 44,030,000원 |
| `목록[].해외사용액` | 해외사용액(P) | text | 100% |  |
| `목록[].당월예치잔액` | 당월예치잔액(Q=J+K-N) | text | 100% | 29,180,000 |
| `목록[].이자유형2` | 이자유형2 | text | 100% | 13,070,000 |
| `목록[].변동금리구분3` | 변동금리구분3 | text | 100% | 100 |
| `목록[].금리통화` | 금리통화 | text | 100% | 100 |
| `목록[].금리수준4` | 금리수준4 | text | 100% | 100 |
| `목록[].금리스프레드5` | 금리스프레드(변동금리)5) | text | 100% | 100 |
| `목록[].이자지급주기6` | 이자지급주기6 | text | 100% | 43,640,000 |
| `목록[].Option종류7` | Option종류7 | text | 100% |  |
| `목록[].Option행사일` | Option행사일 | text | 100% | 2025-02-18 |
| `목록[].상환방법` | 상환방법 | text | 100% | 원금균등분할상환 |
| `목록[].지급보증기관8` | 지급보증기관8 | text | 100% |  |
| `목록[].지급보증기관본점국적국` | 지급보증기관본점국적국 | text | 100% |  |
| `목록[].지급보증기관명` | 지급보증기관명 | text | 100% | 농협은행 |

### 거주자의 해외 증권발행 및 상환 현황 보고서 (`hf227`) — 키 51개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].발행자명` | 발행자명 | text | 100% |  |
| `목록[].사업자등록번호` | 사업자등록번호 | text | 100% | 549-35-19291 |
| `목록[].담당자성명` | 담당자성명 | text | 100% | 박찬연 |
| `목록[].담당자전화번호` | 담당자전화번호 | text | 100% | 010-5907-7253 |
| `목록[].대주명` | 대주명 | text | 100% |  |
| `목록[].대주소재국` | 대주소재국 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `목록[].신고번호` | 신고번호 | text | 100% | 483-317921-44124 |
| `목록[].지정거래외국환은행지점명` | 지정거래외국환은행지점명 | text | 100% | 국민은행 |
| `목록[].발행일자` | 발행일자 | text | 100% | 2025-06-05 |
| `목록[].발행시장소재국` | 발행시장소재국 | text | 100% |  |
| `목록[].자금용도` | 자금용도 | text | 100% | 하나 TDF 2040 |
| `목록[].증권종류1` | 증권종류1 | text | 100% |  |
| `목록[].발행통화` | 발행통화 | text | 100% | CAD |
| `목록[].발행금액` | 발행금액(A) | text | 100% | 271,650,000 |
| `목록[].만기일자` | 만기일자 | text | 100% | 2027년 4월 26일 |
| `목록[].당월국내예치일자` | 당월국내예치일자 | text | 100% | 2025년 5월 18일 |
| `목록[].당월국내예치액` | 당월국내예치액 | text | 100% |  |
| `목록[].기원금상환액` | 기원금상환액(B) | text | 100% | 138,850,000 |
| `목록[].당월상환일자` | 당월상환일자 | text | 100% | 2025.11.24 |
| `목록[].상환잔액` | 상환잔액(E=A-B-C-D) | text | 100% | 22,510,000원 |
| `목록[].당월이자상환액` | 당월이자상환액 | text | 100% | 220,000 |
| `목록[].당월주식전환액2` | 당월주식전환액2 | text | 100% |  |
| `목록[].당월말주식전환누계액3` | 당월말주식전환누계액3 | text | 100% |  |
| `목록[].해외예치일자` | 해외예치일자 | text | 100% | 2026-01-15 |
| `목록[].해외예치은행명` | 해외예치은행명 | text | 100% | 신한은행 |
| `목록[].해외예치은행BIC코드` | 해외예치은행BIC코드 | text | 100% | 8604 |
| `목록[].전월말예치잔액` | 전월말예치잔액(F) | text | 100% | 420,000 |
| `제출자` | 제출자 | text | 100% |  |
| `목록[].당월예치액` | 당월예치액(G=H+I) | text | 100% |  |
| `목록[].당월발행대금` | 당월발행대금(H) | number | 100% | 60,000 |
| `목록[].당월예치이자` | 당월예치이자(I) | number | 100% | 570,000 |
| `목록[].당월인출액` | 당월인출액(J=K+L) | text | 100% |  |
| `목록[].국내입금액` | 국내입금액(K) | number | 100% | 2,560,000 |
| `목록[].해외사용액` | 해외사용액(L) | text | 100% |  |
| `목록[].당월말예치잔액` | 당월말예치잔액(M=F+G-J) | number | 100% | 28,710,000 |
| `목록[].표면금리` | 표면금리 | number | 100% | 100 |
| `목록[].발행비용` | 발행비용(%) | text | 100% |  |
| `목록[].이자유형4` | 이자유형4 | text | 100% | 710,000 |
| `목록[].변동금리구분5` | 변동금리구분5 | number | 100% | 100 |
| `목록[].금리통화` | 금리통화 | number | 100% | 100 |
| `목록[].금리수준6` | 금리수준6 | number | 100% | 100 |
| `목록[].금리스프레드7` | 금리스프레드(변동금리)7) | number | 100% | 100 |
| `목록[].이자지급주기8` | 이자지급주기8 | number | 100% | 3,680,000 |
| `목록[].Option종류9` | Option종류9 | text | 100% |  |
| `목록[].Option행사일10` | Option행사일10 | text | 100% |  |
| `목록[].SWAP종류11` | SWAP종류11 | text | 100% |  |
| `목록[].권리행사일12` | 권리행사일(CB,BW)12) | text | 100% |  |
| `목록[].상환방법` | 상환방법 | text | 100% | 만기일시상환 |
| `목록[].지급보증기관13` | 지급보증기관13 | text | 100% |  |
| `목록[].지급보증기관본점국적국` | 지급보증기관본점국적국 | text | 100% |  |
| `목록[].지급보증기관명` | 지급보증기관명 | text | 100% | 우리은행 |

### 담보제공신고(보고)서 (`hf228`) — 키 24개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | (주)다온커뮤니케이션 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | (주)유니온무역 |
| `company.biz_item` | 업종(직업) | text | 100% | 무역 |
| `담보제공자` | 담보제공자 | text | 100% |  |
| `담보취득자` | 담보취득자 | text | 100% |  |
| `담보제공수혜자` | 담보제공수혜자 | text | 100% |  |
| `check.담보물종류` | 담보물종류 | checkbox | 100% | 기타( |
| `담보소재지` | 담보소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `수량` | 수량 | number | 100% | 3 |
| `담보제공기간` | 담보제공기간 | text | 100% |  |
| `check.담보제공용도` | 담보제공용도 | checkbox | 100% | 증권회사 현지법인의 현지차입에 대한 담보제공 |
| `담보가액` | 담보가액 | number | 100% | 277,720,000 |
| `신고번호` | 신고번호 | text | 100% | 3910-1810 |
| `신고금액` | 신고금액 | number | 100% | 2,460,000 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `신고조건` | 신고조건 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고기관 | text | 100% | 박찬연 |
| `seal.signer2` | 신고기관 | seal | 100% | 현예지 |
| `sign.signer2` | 신고기관 | signature | 100% | 박찬연 |
| `위의신청을다음과같이신고필함` | 위의신청을다음과같이신고필함. | text | 100% |  |

### 매매신고(보고)서 (`hf229`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | 주식회사 한빛패션 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | (주)유니온무역 |
| `company.biz_item` | 업종(직업) | text | 100% | 무역 |
| `매매대상물종류` | 매매대상물종류 | text | 100% |  |
| `매매사유` | 매매사유 | text | 100% | 자녀 교육비 |
| `신고번호` | 신고번호 | text | 100% | 905969-3141073 |
| `신고금액` | 신고금액 | number | 100% | 400,000 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer2` | 은행장 | seal | 100% | 박찬연 |
| `sign.signer2` | 은행장 | signature | 100% | 강순준 |

### 보증계약신고(보고)서 (`hf230`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | (주)유니온무역 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | (주)스마트에프앤비 |
| `company.biz_item` | 업종(직업) | text | 100% | 무역 |
| `보증채권자` | 보증채권자 | text | 100% |  |
| `보증채무자` | 보증채무자 | text | 100% |  |
| `보증수혜자` | 보증수혜자 | text | 100% |  |
| `보증금액` | 보증금액 | number | 100% | 8,570,000원 |
| `보증기간` | 보증기간 | text | 100% |  |
| `check.보증용도` | 보증용도 | checkbox | 100% | 기타( |
| `상환방법` | 상환방법 | text | 100% | 만기일시상환 |
| `신고번호` | 신고번호 | text | 100% | 6828-8711 |
| `신고금액` | 신고금액 | number | 100% | 8,150,000 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `신고조건` | 신고조건 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고기관 | text | 100% | 박찬연 |
| `seal.signer2` | 신고기관 | seal | 100% | 강순준 |
| `sign.signer2` | 신고기관 | signature | 100% | 위나아 |
| `위의신청을다음과같이신고필함` | 위의신청을다음과같이신고필함. | text | 100% |  |

### 현지금융 차입·상환·보증등 한도 운영현황 보고서 (`hf231`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].보고업체명1` | 보고업체명1)(본사명) | text | 100% | (주)유니온무역 |
| `목록[].사업자번호법인번호` | 사업자번호/법인번호 | text | 100% | 817-29-07998 |
| `계` | 계 | text | 100% |  |
| `목록[].차주2` | 차주2 | text | 100% |  |
| `목록[].대주3대주지역` | 대주3)대주지역 | text | 100% |  |
| `목록[].차입구분4외화증권5` | 차입구분4)외화증권5 | text | 100% | EUR 59,800 |
| `목록[].차입잔액6` | 차입잔액6 | text | 100% | 3,860,000 |
| `목록[].금리7` | 금리7)(bp) | text | 100% | 35 |
| `목록[].차입일8` | 차입일8 | text | 100% |  |
| `목록[].만기일8` | 만기일8 | text | 100% | 2028-07-21 |
| `목록[].보증9` | 보증9 | text | 100% |  |
| `목록[].용도10` | 용도10 | text | 100% | 하나 적금 |
| `제출자` | 제출자 | text | 100% |  |

### 증권발행 신고(보고)서 (`hf232`) — 키 29개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | (주)삼정전자 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | (주)유니온무역 |
| `company.biz_item` | 업종(직업) | text | 100% | 무역 |
| `상호기타명칭` | 상호기타명칭 | text | 100% | (주)유니온무역 |
| `증권종류` | 증권종류 | text | 100% |  |
| `발행금액` | 발행금액 | number | 100% | 209,060,000 |
| `계약체결시기및장소` | 계약체결시기및장소 | text | 100% |  |
| `표면금리` | 표면금리 | number | 100% | 40 |
| `만기` | 만기 | date | 100% | 2025년 11월 15일 |
| `배당금지급시기및방법` | 배당금지급시기및방법 | text | 100% |  |
| `원리금상환방법` | 원리금상환방법 | text | 100% | 원리금균등분할상환 |
| `자금용도` | 자금용도 | text | 100% | 사업자금 |
| `발행관련기관` | 발행관련기관 | text | 100% |  |
| `액면금액및수량` | 액면금액및수량 | number | 100% | 48,540,000 |
| `발행시기및장소` | 발행시기및장소 | text | 100% |  |
| `발행가격` | 발행가격 | text | 100% |  |
| `해외판매여부` | 해외판매여부 | text | 100% |  |
| `신고번호` | 신고번호 | text | 100% | 1448-0651 |
| `신고금액` | 신고금액 | number | 100% | 860,000 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `신고조건` | 신고조건 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고기관 | text | 100% | 박찬연 |
| `seal.signer2` | 신고기관 | seal | 100% | 이민빈 |
| `sign.signer2` | 신고기관 | signature | 100% | 박찬연 |
| `위의신청을다음과같이신고필함` | 위의신청을다음과같이신고필함. | text | 100% |  |

### 금전의 대차계약 신고(보고)서 (`hf233`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | (주)유니온무역 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | (주)스마트에프앤비 |
| `company.biz_item` | 업종(직업) | text | 100% | 의류 도매 |
| `customer.name` | 차주 | text | 100% | 박찬연 |
| `대주` | 대주 | text | 100% |  |
| `통화및금액` | 통화및금액 | number | 100% | 6,790,000원 |
| `차입일대출일` | 차입일/대출일 | date | 100% | 2025.07.07 |
| `대차기간` | 대차기간 | text | 100% |  |
| `사용용도` | 사용용도 | text | 100% | 타행 이체 |
| `상환방법` | 상환방법 | text | 100% | 원리금균등분할상환 |
| `신고번호` | 신고번호 | text | 100% | 759-873959-67379 |
| `신고금액` | 신고금액 | number | 100% | 192,200,000 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `신고조건` | 신고조건 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고기관 | text | 100% | 박찬연 |
| `seal.signer2` | 신고기관 | seal | 100% | 박찬연 |
| `sign.signer2` | 신고기관 | signature | 100% | 이욱유 |
| `위의신청을다음과같이신고필함` | 위의신청을다음과같이신고필함. | text | 100% |  |

### 외화송금의 내용변경 및 취소, 송금수표 분실신고 등 신청서 (`hf234`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.송금방법` | 송금방법 | checkbox | 100% | 송금수표(D/D) |
| `송금일자` | 송금일자 | date | 100% | 2025년 4월 3일 |
| `송금번호` | 송금번호(수표번호) | text | 100% | 427-131116-01217 |
| `수취인` | 수취인 | text | 100% | 신영정밀 |
| `value` | [전신송금내용변경기재란] | amount | 100% |  |
| `check.전신송금` | 전신송금 | checkbox | 100% | 전신송금 지급여부조회 |
| `check.송금수표` | 송금수표 | checkbox | 100% | 송금수표 분실신고 |
| `거래은행` | 거래은행 | text | 100% | 카카오뱅크 |
| `foreign.account` | 계좌번호 | account_no | 100% | 884779361534 |
| `foreign.name` | 성명 | text | 100% | Tokyo Seimitsu Kogyo K.K. |
| `foreign.address` | 주소 | text | 100% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `foreign.phone` | 전화번호 | text | 100% | Klaus Weber |
| `기타` | 기타(사유등) | text | 100% | 만기 해지 |
| `수취인_목록[].변경후` | 변경후 | text | 100% | 급여 수령 |
| `변경후` | 변경후 | text | 100% | 본인 요청 |
| `송금인` | 송금인 | text | 100% |  |
| `customer.birth` | 생년월일/사업자번호 | date | 100% | 1990년 2월 10일 |
| `customer.address` | 주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `customer.phone` | 전화번호 | phone | 100% | 010-7321-8870 |
| `Email주소` | E-mail주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 외국인투자기업등록(변경등록)신청서(국문) (`hf235`) — 키 33개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `접수일` | 접수일 | text | 100% |  |
| `처리일` | 처리일 | text | 100% |  |
| `처리기간1일` | 처리기간1일 | date | 100% | 2024.12.28 |
| `상호또는명칭` | 상호또는명칭(영문) | text | 100% | (주)유니온무역 |
| `신고된사업명` | 신고(허가)된사업명 | text | 100% |  |
| `자본금` | 자본금(출연금) | text | 100% |  |
| `value` | (국문) | amount | 100% |  |
| `value2` | (영문) | amount | 100% |  |
| `SPC여부예아니오` | (*)SPC여부[]예[]아니오 | text | 100% |  |
| `본사` | 본사 | text | 100% |  |
| `주공장소재지` | 주공장(주사업장)소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `홈페이지` | 홈페이지 | text | 100% |  |
| `액면총액` | 액면총액 | number | 100% | 44,830,000 |
| `상호또는명칭2` | 상호또는명칭(영문) | text | 100% | (주)누리상사 |
| `상호또는명칭3` | 상호또는명칭(영문) | text | 100% | 주식회사 신영화학 |
| `대표Email` | 대표E-mail | text | 100% |  |
| `customer.nationality` | 국적 | text | 100% | 대한민국 |
| `customer.nationality2` | 국적 | text | 100% | 대한민국 |
| `customer.nationality3` | 국적 | text | 100% | 대한민국 |
| `액면총액2` | 액면총액 | number | 100% | 40 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신고인또는신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신고인또는신청인 | seal | 100% | 강순준 |
| `sign.signer` | 신고인또는신청인 | signature | 100% | 박찬연 |
| `접수번호` | 접수번호 | text | 100% |  |
| `투자기업` | 투자기업 | text | 100% |  |
| `상당` | 상당 | text | 100% |  |
| `등록후예상규모` | 등록후예상규모(신규및변경등록) | number | 100% | 36 |
| `투자기업2` | 투자기업 | text | 100% |  |
| `양도또는감소할` | 양도또는감소할 | text | 100% |  |
| `액면총액3` | 액면총액(A×B) | number | 100% | 4,650,000 |
| `check.송달받는것에대하여` | 송달받는것에대하여 | checkbox | 100% | 동의하지 않습니다. |
| `신규등록인경우` | <신규등록인경우> | text | 100% |  |

### 해외예금 및 신탁 잔액 보고서 (`hf236`) — 키 29개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `개설인명` | 개설인명 | text | 100% |  |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.biz_no` | 사업자(주민)등록번호 | biz_no | 100% | 264-82-36559 |
| `직위성명` | 직위‧성명 | text | 100% | 김철도 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `예금종류1` | 예금종류1 | text | 100% | 하나 단기채 펀드 |
| `예금기관명2` | 예금기관명2 | text | 100% | 농협은행 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `국가명3` | 국가명3 | text | 100% | 독일 |
| `전년말잔액` | 전년말잔액(A) | number | 100% | 39,990,000 |
| `국내송금` | 국내송금 | text | 100% |  |
| `해외입금수출대금외화증권처분예금신탁처분기타계` | 해외입금수출대금외화증권처분예금‧신탁처분기타계 | amount | 100% | USD 37,600 |
| `해외입금수출대금외화증권처분예금신탁처분기타계2` | 해외입금수출대금외화증권처분예금‧신탁처분기타계 | amount | 100% | USD 83,600 |
| `해외입금수출대금외화증권처분예금신탁처분기타계3` | 해외입금수출대금외화증권처분예금‧신탁처분기타계 | amount | 100% | USD 143,300 |
| `해외입금수출대금외화증권처분예금신탁처분기타계4` | 해외입금수출대금외화증권처분예금‧신탁처분기타계 | amount | 100% | AUD 69,100 |
| `해외입금수출대금외화증권처분예금신탁처분기타계5` | 해외입금수출대금외화증권처분예금‧신탁처분기타계 | amount | 100% | CAD 199,600 |
| `해외입금수출대금외화증권처분예금신탁처분기타계6` | 해외입금수출대금외화증권처분예금‧신탁처분기타계 | amount | 100% | USD 81,400 |
| `목록[].금액` | 금액 | text | 100% | 690,000 |
| `금액` | 금액 | number | 100% | 10,580,000 |
| `국내회수` | 국내회수 | text | 100% |  |
| `해외처분수입대금지급외화증권취득예금신탁예치기타계` | 해외처분수입대금지급외화증권취득예금‧신탁예치기타계 | amount | 100% | USD 22,500 |
| `해외처분수입대금지급외화증권취득예금신탁예치기타계2` | 해외처분수입대금지급외화증권취득예금‧신탁예치기타계 | amount | 100% | EUR 118,700 |
| `해외처분수입대금지급외화증권취득예금신탁예치기타계3` | 해외처분수입대금지급외화증권취득예금‧신탁예치기타계 | amount | 100% | USD 112,000 |
| `해외처분수입대금지급외화증권취득예금신탁예치기타계4` | 해외처분수입대금지급외화증권취득예금‧신탁예치기타계 | amount | 100% | USD 104,900 |
| `해외처분수입대금지급외화증권취득예금신탁예치기타계5` | 해외처분수입대금지급외화증권취득예금‧신탁예치기타계 | amount | 100% | USD 24,400 |
| `해외처분수입대금지급외화증권취득예금신탁예치기타계6` | 해외처분수입대금지급외화증권취득예금‧신탁예치기타계 | amount | 100% | EUR 193,600 |
| `연중이자` | 연중이자(D) | number | 100% | 7,620,000 |
| `금년말잔액` | 금년말잔액(A+B-C+D) | number | 100% | 83,260,000 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 해외예금 입금보고서 (`hf237`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `개설인명` | 개설인명 | text | 100% |  |
| `customer.rrn` | 주민등록번호(사업자등록번호) | rrn | 100% | 900210-1****** |
| `입금일자` | 입금일자 | date | 100% | 2025-08-30 |
| `예금종류2` | 예금종류2 | text | 100% | 하나 단기채 펀드 |
| `예금기관명` | 예금기관명 | text | 100% | 하나은행 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `입금액3` | 입금액3 | number | 100% | 2,550,000 |
| `입금재원4` | 입금재원4 | text | 100% |  |
| `국가명5` | 국가명5 | text | 100% | 일본 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer.name` | 대표자성명1 | text | 100% | 박찬연 |
| `seal.signer` | 대표자성명1 | seal | 100% | 강순준 |
| `sign.signer` | 대표자성명1 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |

### 해외직접투자사업 청산 및 대부채권 회수보고서 (`hf238`) — 키 27개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `상호또는성명` | 상호또는성명 | text | 100% | 주식회사 한빛패션 |
| `company.address` | 소재지(주소) | text | 100% | 서울특별시 노원구 한글비석로 388-7, 8층 13호 |
| `company.biz_no` | 사업자(주민)등록번호 | biz_no | 100% | 261-82-53694 |
| `현지법인명` | 현지법인명 | text | 100% | (주)유니온무역 |
| `company.address2` | 소재지(주소) | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `check.법인형태` | 법인형태 | checkbox | 100% | 개인기업 |
| `check.투자형태주1` | 투자형태주1 | checkbox | 100% | 공동투자 |
| `납입자본금` | 납입자본금 | text | 100% |  |
| `대부금액` | 대부금액 | number | 100% | 68,500,000원 |
| `기회수금액` | 기회수금액 | number | 100% | 4,460,000 |
| `금회회수금액` | 금회회수금액 | number | 100% | 45,620,000 |
| `잔액` | 잔액 | number | 100% | 67,730,000 |
| `date` | 일자 | date | 100% | 2026년 01월 31일 |
| `목록[].원금` | 원금 | number | 100% | 147,050,000원 |
| `회수금액_목록[].원금` | 원금 | number | 100% | 1,540,000 |
| `유동자산투자및기타자산고정자산이연자산` | 유동자산투자및기타자산고정자산이연자산 | text | 100% |  |
| `유동부채고정부채이연부채자본금잉여금` | 유동부채고정부채이연부채자본금잉여금 | text | 100% |  |
| `check.청산` | 청산 | checkbox | 100% | 청산 |
| `청산종료일` | 청산종료일 | date | 100% | 2027.03.18 |
| `목록[].구분회수일자` | 구분회수일자 | date | 100% | 2025.12.11 |
| `목록[].회수재산의종류` | 회수재산의종류 | text | 100% |  |
| `계` | 계 | text | 100% |  |
| `목록[].금액` | 금액 | text | 100% | 107,230,000 |
| `목록[].비고` | 비고 | text | 100% | 투자 목적 |
| `다청산손익` | 다.청산손익(해산일로부터청산종료일까지의손익) | text | 100% |  |
| `바회수가불가능한재산이있을경우그내역및사유` | 바.회수가불가능한재산이있을경우그내역및사유 | text | 100% | 결혼자금 |
| `회수되어야할재산` | -회수되어야할재산 | text | 100% |  |

### 해외 부동산 처분(변경)신고서 (`hf239`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `처분전부동산명의인` | 처분(변경)전부동산명의인 | text | 100% | 최아우 |
| `가성명또는법인명` | 가.성명또는법인명 | text | 100% | 미래로지스(주) |
| `나주민등록번호` | 나.주민등록번호(사업자등록번호) | rrn | 100% | 377965-7968729 |
| `다주소또는소재지` | 다.주소또는소재지 | text | 100% | 서울특별시 송파구 중대로 174, 119동 2202호 |
| `가성명또는법인명2` | 가.성명또는법인명 | text | 100% | (주)동방산업 |
| `나주민등록번호2` | 나.주민등록번호(사업자등록번호) | text | 100% | 9401-1913 |
| `다주소또는소재지2` | 다.주소또는소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `가부동산의명세` | 가.부동산의명세(종류,수량,가격등) | text | 100% |  |
| `나부동산의소재지` | 나.부동산의소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `가부동산처분등기일` | 가.부동산처분등기일 | date | 100% | 2027.02.18 |
| `나처분가격` | 나.처분가격 | text | 100% |  |
| `다기타지급비용` | 다.기타지급비용 | text | 100% |  |
| `라국내회수금액` | 라.국내회수금액 | number | 100% | 400,000 |
| `바신고인과국내회수금액수취인과의관계` | 바.신고인과국내회수금액수취인과의관계 | number | 100% | 480,000 |
| `해외부동산변경내용` | 해외부동산변경내용 | text | 100% | 학자금 |

### 외화증권(채권)취득보고서(법인 및 개인기업 설립보고서 포함) (`hf240`) — 키 25개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `상호또는성명` | 상호또는성명 | text | 100% | 세진테크(주) |
| `company.address` | 소재지(주소) | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `check.투자자규모` | 투자자규모 | checkbox | 100% | 중소기업 |
| `date` | 신고일자 | date | 100% | 2026.01.31 |
| `설립년월일` | 설립년월일 | date | 100% | 2024-12-30 |
| `신고번호` | 신고번호 | text | 100% | 925515-2779752 |
| `company.name` | 법인명 | text | 100% | (주)유니온무역 |
| `company.address2` | 소재지(주소) | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `check.법인형태` | 법인형태 | checkbox | 100% | 해외자원개발사업 |
| `check.투자형태주1` | 투자형태주1 | checkbox | 100% | 단독투자 |
| `설립등기일` | 설립등기일 | date | 100% | 2024.07.29 |
| `납입자본금` | 납입자본금 | text | 100% |  |
| `영업개시일` | 영업개시(예정)일 | date | 100% | 2025.04.23 |
| `결산일` | 결산일 | date | 100% | 2025.10.14 |
| `증권취득일` | 증권취득일(자본금출자일) | date | 100% | 2025-10-03 |
| `액면가액합계` | 액면가액합계 | number | 100% | 15,250,000 |
| `check.증권발행여부` | 증권발행여부 | checkbox | 100% | 증권발행 |
| `증권종류` | 증권종류 | text | 100% |  |
| `취득가액합계` | 취득가액합계 | number | 100% | 294,400,000원 |
| `채권취득일` | 채권취득일 | date | 100% | 2025.06.11 |
| `이자율` | 이자율 | number | 100% | 10 |
| `check.원금회수방법` | 원금회수방법 | checkbox | 100% | 분할회수( |
| `대부원금` | 대부원금 | number | 100% | 110,440,000 |
| `대부기간` | 대부기간 | text | 100% |  |
| `check.외화증권` | 외화증권 | checkbox | 100% | 외화증권 |

### 대외지급보증 조건변경 신청서(SWIFT 방식)(2D) (`hf241`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.전문사본요청합니다` | 전문사본요청합니다. | checkbox | 100% | 전문 사본 요청합니다. |
| `FAXorEMAIL` | FAXorE-MAIL | phone | 100% | 043-783-2775 |
| `보증서번호` | 보증서번호 | text | 100% | 가마17634470 |
| `보증서증액` | 보증서증액 | text | 100% |  |
| `보증서감액` | 보증서감액 | text | 100% |  |
| `만기일자` | (변경후)만기일자(년/월/일) | date | 100% | 2029-05-23 |
| `기타조건변경` | 기타조건변경 | text | 100% | 자녀 교육비 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 이욱유 |

### 대외지급보증 발급 신청서(SWIFT 방식)(2D) (`hf242`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.전문사본요청합니다` | 전문사본요청합니다. | checkbox | 100% | 전문 사본 요청합니다. |
| `FAXorEMAIL` | FAXorE-MAIL | phone | 100% | 043-783-2775 |
| `ExpiryDate` | ExpiryDate(년/월/일) | date | 100% | 2025.07.02 |
| `Applicant` | Applicant | text | 100% | 주식회사 세진산업 |
| `Beneficiary` | Beneficiary | text | 100% |  |
| `Beneficiary2` | Beneficiary | text | 100% |  |
| `Beneficiary3` | Beneficiary | text | 100% |  |
| `AdvisingBank` | AdvisingBank | text | 100% |  |
| `UndertakingAmount` | UndertakingAmount(보증금액) | text | 100% |  |
| `UndertakingtermsandConditions` | UndertakingtermsandConditions | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 위나아 |
| `sign.signer` | 신청인 | signature | 100% | 강순준 |

### 외국환거래 UMS통지서비스 (변경)신청서 (`hf243`) — 키 30개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `당발송금` | 당발송금 | text | 100% |  |
| `타발송금내도통지` | 타발송금내도통지 | text | 100% |  |
| `타발송금입금통지` | 타발송금입금통지 | text | 100% |  |
| `외화수표추심` | 외화수표추심 | amount | 100% | CNY 101,400 |
| `로칼서류접수` | 로칼서류접수 | text | 100% |  |
| `check.수입선적서류접수` | 수입선적서류접수( | checkbox | 100% | 건별 / |
| `수출네고특사번호통지` | 수출네고특사번호통지 | text | 100% | 436109-0476538 |
| `customer.name` | 고객명 | text | 100% | 박찬연 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `check.당발송금` | 당발송금 | checkbox | 100% | E-MAIL |
| `check.타발송금내도통지` | 타발송금내도통지 | checkbox | 100% | E-MAIL |
| `check.타발송금입금통지` | 타발송금입금통지 | checkbox | 100% | FAX |
| `check.외화수표추심` | 외화수표추심 | checkbox | 100% | E-MAIL |
| `check.로칼서류접수` | 로칼서류접수 | checkbox | 100% | E-MAIL |
| `check.FAX` | FAX | checkbox | 100% | E-MAIL |
| `check.수출네고특사번호통지` | 수출네고특사번호통지 | checkbox | 100% | E-MAIL |
| `check.수출입금통지` | 수출입금통지(매입/추심포함) | checkbox | 100% | FAX |
| `check.수출인수통지` | 수출인수통지(매입/추심포함) | checkbox | 100% | E-MAIL |
| `company.biz_no` | 사업자등록번호(생년월일) | biz_no | 100% | 261-82-53694 |
| `SMS수신전화번호` | SMS수신전화번호 | phone | 100% | 010-5907-7253 |
| `FAX번호` | FAX번호 | phone | 100% | 043-783-2775 |
| `EMAIL주소` | E-MAIL주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `check.외국환업무에대한UMS통지서비스` | 외국환업무에대한UMS통지서비스( | checkbox | 100% | 변경) 를 신청합니다. |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 현예지 |
| `수출입금통지` | 수출입금통지(매입/추심포함) | text | 100% |  |
| `수출인수통지` | 수출인수통지(매입/추심포함) | text | 100% |  |

### 자본재 등 도입물품명세 검토ㆍ확인신청서 (`hf244`) — 키 63개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `접수일` | 접수일 | text | 100% |  |
| `처리일` | 처리일 | text | 100% |  |
| `신고된사업명` | 신고된사업명 | text | 100% |  |
| `상호또는명칭` | 상호또는명칭(영문) | text | 100% | (주)유니온무역 |
| `customer.nationality` | 국적 | text | 100% | 대한민국 |
| `HSK분류번호` | HSK분류번호 | text | 100% | 252967-3213880 |
| `품명` | 품명 | text | 100% | 화장품 |
| `수량` | 수량 | number | 100% | 6 |
| `규격` | 규격 | text | 100% | 식품 원재료 |
| `제작자` | 제작자 | text | 100% |  |
| `금액` | 금액(기준통화ᆞ도입통화) | number | 100% | 9,800,000 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신고인(또는대리인) | text | 100% | 박찬연 |
| `seal.signer` | 신고인(또는대리인) | seal | 100% | 강순준 |
| `sign.signer` | 신고인(또는대리인) | signature | 100% | 박찬연 |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `접수번호` | 접수번호 | text | 100% |  |
| `상호또는명칭2` | 상호또는명칭(영문) | text | 100% | 주식회사 동방테크 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `외국인투자금액및비율` | 외국인투자금액및비율 | number | 100% | 50 |
| `접수일2` | 접수일 | text | 100% |  |
| `처리일2` | 처리일 | text | 100% |  |
| `신고된사업명2` | 신고된사업명 | text | 100% |  |
| `상호또는명칭3` | 상호또는명칭(영문) | text | 100% | 유니온로지스(주) |
| `customer.nationality2` | 국적 | text | 100% | 대한민국 |
| `HSK분류번호2` | HSK분류번호 | text | 100% | 189394-2829342 |
| `품명2` | 품명 | text | 100% | 커피 원두 |
| `수량2` | 수량 | number | 100% | 6 |
| `규격2` | 규격 | text | 100% | 화장품 |
| `제작자2` | 제작자 | text | 100% |  |
| `금액2` | 금액(기준통화ᆞ도입통화) | number | 100% | 212,710,000 |
| `date4` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date5` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고인(또는대리인) | text | 100% | 박찬연 |
| `seal.signer2` | 신고인(또는대리인) | seal | 100% | 현예지 |
| `sign.signer2` | 신고인(또는대리인) | signature | 100% | 박찬연 |
| `date6` | 작성일 | date | 100% | 2026년 1월 31일 |
| `접수번호2` | 접수번호 | text | 100% |  |
| `상호또는명칭4` | 상호또는명칭(영문) | text | 100% | 유니온테크(주) |
| `company.biz_no2` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `외국인투자금액및비율2` | 외국인투자금액및비율 | number | 100% | 60 |
| `접수일3` | 접수일 | text | 100% |  |
| `처리일3` | 처리일 | text | 100% |  |
| `신고된사업명3` | 신고된사업명 | text | 100% |  |
| `상호또는명칭5` | 상호또는명칭(영문) | text | 100% | (주)유니온무역 |
| `customer.nationality3` | 국적 | text | 100% | 대한민국 |
| `HSK분류번호3` | HSK분류번호 | text | 100% | 720276-2611603 |
| `품명3` | 품명 | text | 100% | 의류 원단 |
| `수량3` | 수량 | number | 100% | 60 |
| `규격3` | 규격 | text | 100% | 포장재 |
| `제작자3` | 제작자 | text | 100% |  |
| `금액3` | 금액(기준통화ᆞ도입통화) | number | 100% | 950,000 |
| `date7` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date8` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer3.name` | 신고인(또는대리인) | text | 100% | 박찬연 |
| `seal.signer3` | 신고인(또는대리인) | seal | 100% | 박찬연 |
| `sign.signer3` | 신고인(또는대리인) | signature | 100% | 이욱유 |
| `date9` | 작성일 | date | 100% | 2026년 1월 31일 |
| `접수번호3` | 접수번호 | text | 100% |  |
| `상호또는명칭6` | 상호또는명칭(영문) | text | 100% | 신영산업 |
| `company.biz_no3` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `외국인투자금액및비율3` | 외국인투자금액및비율 | number | 100% | 70 |

### 장기차관 방식의 외국인투자신고서, 변경신고서(영문) (`hf245`) — 키 36개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | Name | text | 100% | 박찬연 |
| `customer.address` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.name2` | Name | text | 100% | 박찬연 |
| `customer.address2` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `Cash` | Cash | text | 100% |  |
| `PurposeofLoan` | PurposeofLoan | text | 100% |  |
| `RateofInterest` | RateofInterest | text | 100% |  |
| `Capitalinkind` | Capitalinkind | text | 100% |  |
| `customer.nationality` | Nationality | text | 100% | 대한민국 |
| `AverageLoanPeriod` | AverageLoanPeriod | text | 100% |  |
| `Other` | Other | text | 100% |  |
| `Other2` | Other | text | 100% |  |
| `LocationofInvestment` | LocationofInvestment | text | 100% |  |
| `ChangeinInformation` | ChangeinInformation | text | 100% |  |
| `InformationAfterChange` | InformationAfterChange | text | 100% |  |
| `NotificationNo` | NotificationNo | text | 100% | 890-606547-81554 |
| `ReceiptNumber` | ReceiptNumber | text | 100% |  |
| `DateofReceipt` | DateofReceipt | date | 100% | 2025년 1월 13일 |
| `customer.name3` | Name | text | 100% | 박찬연 |
| `customer.address3` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.name4` | Name | text | 100% | 박찬연 |
| `customer.address4` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `Cash2` | Cash | text | 100% |  |
| `PurposeofLoan2` | PurposeofLoan | text | 100% |  |
| `RateofInterest2` | RateofInterest | text | 100% |  |
| `Capitalinkind2` | Capitalinkind | text | 100% |  |
| `customer.nationality2` | Nationality | text | 100% | 대한민국 |
| `AverageLoanPeriod2` | AverageLoanPeriod | text | 100% |  |
| `Other3` | Other | text | 100% |  |
| `Other4` | Other | text | 100% |  |
| `LocationofInvestment2` | LocationofInvestment | text | 100% |  |
| `ChangeinInformation2` | ChangeinInformation | text | 100% |  |
| `InformationAfterChange2` | InformationAfterChange | text | 100% |  |
| `NotificationNo2` | NotificationNo | rrn | 100% | 297374-1140417 |
| `ReceiptNumber2` | ReceiptNumber | text | 100% |  |
| `DateofReceipt2` | DateofReceipt | date | 100% | 2025.09.18 |

### 장기차관 방식의 외국인투자신고서, 변경신고서(국문) (`hf246`) — 키 50개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `접수일` | 접수일 | text | 100% |  |
| `처리일` | 처리일 | text | 100% |  |
| `상호또는명칭` | 상호또는명칭 | text | 100% | 청솔전자 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `상호또는명칭2` | 상호또는명칭(영문) | text | 100% | 우진로지스(주) |
| `customer.address2` | 주소(영문) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `현금` | 현금 | text | 100% |  |
| `차관용도` | 차관용도 | text | 100% | 전세자금 |
| `연이자율` | 연이자율 | number | 100% | 50 |
| `자본재` | 자본재 | text | 100% |  |
| `customer.nationality` | 국적 | text | 100% | 대한민국 |
| `평균차관기간` | 평균차관기간 | text | 100% |  |
| `기타` | 기타 | text | 100% | 의료비 |
| `기타2` | 기타 | text | 100% | 만기 해지 |
| `금번투자지역` | 금번투자지역 | text | 100% |  |
| `변경신고의경우변경내용` | 변경신고의경우변경내용 | text | 100% | 만기 해지 |
| `변경후내용` | 변경후내용 | text | 100% | 의료비 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신고인(또는대리인) | text | 100% | 박찬연 |
| `seal.signer` | 신고인(또는대리인) | seal | 100% | 박찬연 |
| `sign.signer` | 신고인(또는대리인) | signature | 100% | 강순준 |
| `신고번호` | 신고번호 | text | 100% | 925438-4849145 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `접수번호` | 접수번호 | text | 100% |  |
| `신고인경우` | <신고인경우> | text | 100% |  |
| `접수일2` | 접수일 | text | 100% |  |
| `처리일2` | 처리일 | text | 100% |  |
| `상호또는명칭3` | 상호또는명칭 | text | 100% | (주)미래전자 |
| `customer.address3` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `상호또는명칭4` | 상호또는명칭(영문) | text | 100% | (주)유니온무역 |
| `customer.address4` | 주소(영문) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `현금2` | 현금 | text | 100% |  |
| `차관용도2` | 차관용도 | text | 100% | 주택구입 |
| `연이자율2` | 연이자율 | number | 100% | 60 |
| `자본재2` | 자본재 | text | 100% |  |
| `customer.nationality2` | 국적 | text | 100% | 대한민국 |
| `평균차관기간2` | 평균차관기간 | text | 100% |  |
| `기타3` | 기타 | text | 100% | 투자 목적 |
| `기타4` | 기타 | text | 100% | 해외 이주 |
| `금번투자지역2` | 금번투자지역 | text | 100% |  |
| `변경신고의경우변경내용2` | 변경신고의경우변경내용 | text | 100% | 전세자금 |
| `변경후내용2` | 변경후내용 | text | 100% | 타행 이체 |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고인(또는대리인) | text | 100% | 박찬연 |
| `seal.signer2` | 신고인(또는대리인) | seal | 100% | 박찬연 |
| `sign.signer2` | 신고인(또는대리인) | signature | 100% | 이욱유 |
| `신고번호2` | 신고번호 | text | 100% | 871-305719-14503 |
| `date4` | 작성일 | date | 100% | 2026년 1월 31일 |
| `접수번호2` | 접수번호 | text | 100% |  |
| `신고인경우2` | <신고인경우> | text | 100% |  |

### 외국인투자기업등록(변경등록)신청서(영문) (`hf247`) — 키 25개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `ReceiptNumber` | ReceiptNumber | text | 100% |  |
| `DateofReceipt` | DateofReceipt | date | 100% | 2024-11-27 |
| `customer.name` | Name | text | 100% | 박찬연 |
| `Capital` | Capital(ContributionAmount) | text | 100% |  |
| `value` | (Korean) | amount | 100% |  |
| `value2` | (English) | amount | 100% |  |
| `SPCYesNo` | (*)SPC[]Yes[]No | text | 100% | 0751-9517 |
| `Headquarters` | Headquarters | text | 100% |  |
| `MainFactory` | MainFactory(MainPlaceofBusiness) | text | 100% |  |
| `Homepage` | Homepage(website) | text | 100% |  |
| `customer.name2` | Name | text | 100% | 박찬연 |
| `customer.name3` | Name | text | 100% | 박찬연 |
| `customer.email` | E-mail | text | 100% | soonjun606@gmail.com |
| `customer.nationality` | Nationality | text | 100% | 대한민국 |
| `customer.nationality2` | Nationality | text | 100% | 대한민국 |
| `customer.nationality3` | Nationality | text | 100% | 대한민국 |
| `AcquisitionPricewon` | AcquisitionPrice:won(*USD) | number | 100% | 60 |
| `InvestmentandParValueofStocks` | InvestmentandParValueofStocks | text | 100% |  |
| `DateofCompletion` | DateofCompletion | date | 100% | 2025-09-11 |
| `Investor` | Investor | text | 100% |  |
| `customer.name4` | Name | text | 100% | 박찬연 |
| `Foreign` | Foreign- | text | 100% |  |
| `Invested` | Invested | text | 100% |  |
| `Changeof` | Changeof | text | 100% |  |
| `check.agrees` | agrees | checkbox | 100% | doesn’t agree to receive a |

### 주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(영문) (`hf248`) — 키 24개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `ReceiptNumber` | ReceiptNumber | text | 100% |  |
| `DateofReceipt` | DateofReceipt | date | 100% | 2025.09.15 |
| `customer.name` | Name | text | 100% | 박찬연 |
| `customer.address` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.name2` | Name | text | 100% | 박찬연 |
| `customer.nationality` | Nationality | text | 100% | 대한민국 |
| `AcquisitionPriceWon` | AcquisitionPrice:Won(USD) | number | 100% | 20 |
| `NotificationNo` | NotificationNo | text | 100% | 0676-7663 |
| `DateofCompletion` | DateofCompletion | date | 100% | 2025-09-21 |
| `Changein` | Changein | text | 100% |  |
| `Information` | Information | text | 100% |  |
| `changed` | changed | text | 100% |  |
| `ReceiptNumber2` | ReceiptNumber | text | 100% |  |
| `DateofReceipt2` | DateofReceipt | date | 100% | 2025.07.16 |
| `customer.name3` | Name | text | 100% | 박찬연 |
| `customer.address2` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.name4` | Name | text | 100% | 박찬연 |
| `customer.nationality2` | Nationality | text | 100% | 대한민국 |
| `AcquisitionPriceWon2` | AcquisitionPrice:Won(USD) | number | 100% | 60 |
| `NotificationNo2` | NotificationNo | text | 100% | 940-348098-71692 |
| `DateofCompletion2` | DateofCompletion | date | 100% | 2026.01.26 |
| `Changein2` | Changein | text | 100% |  |
| `Information2` | Information | text | 100% |  |
| `changed2` | changed | text | 100% |  |

### 주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(국문) (`hf249`) — 키 42개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `접수일` | 접수일 | text | 100% |  |
| `처리일` | 처리일 | text | 100% |  |
| `date` | 신고(허가)일 | date | 100% | 2026.01.31 |
| `하려는` | 하려는(하고있는사업) | text | 100% |  |
| `상호또는명칭` | 상호또는명칭 | text | 100% | (주)유니온무역 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `상호또는명칭2` | 상호또는명칭 | text | 100% | 제일무역(주) |
| `customer.nationality` | 국적 | text | 100% | 대한민국 |
| `변경후내용` | 변경후내용 | text | 100% | 만기 해지 |
| `취득총액원` | 취득총액:원(USD상당) | number | 100% | 50 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신고인또는신청인(또는대리인) | text | 100% | 박찬연 |
| `seal.signer` | 신고인또는신청인(또는대리인) | seal | 100% | 박찬연 |
| `sign.signer` | 신고인또는신청인(또는대리인) | signature | 100% | 강순준 |
| `신고번호` | 신고(허가)번호 | text | 100% | 829503-2644480 |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `접수번호` | 접수번호 | text | 100% |  |
| `외국인` | 외국인 | text | 100% |  |
| `변경사항` | 변경사항 | text | 100% |  |
| `이미신고된내용` | 이미신고(허가)된내용 | text | 100% | 자녀 교육비 |
| `변경내용` | 변경내용 | text | 100% | 타행 이체 |
| `접수일2` | 접수일 | text | 100% |  |
| `처리일2` | 처리일 | text | 100% |  |
| `date4` | 신고(허가)일 | date | 100% | 2026.01.31 |
| `하려는2` | 하려는(하고있는사업) | text | 100% |  |
| `상호또는명칭3` | 상호또는명칭 | text | 100% | 누리푸드 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `상호또는명칭4` | 상호또는명칭 | text | 100% | (주)유니온무역 |
| `customer.nationality2` | 국적 | text | 100% | 대한민국 |
| `변경후내용2` | 변경후내용 | text | 100% | 해외 이주 |
| `취득총액원2` | 취득총액:원(USD상당) | number | 100% | 100 |
| `date5` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고인또는신청인(또는대리인) | text | 100% | 박찬연 |
| `seal.signer2` | 신고인또는신청인(또는대리인) | seal | 100% | 박찬연 |
| `sign.signer2` | 신고인또는신청인(또는대리인) | signature | 100% | 이욱유 |
| `신고번호2` | 신고(허가)번호 | text | 100% | 045-960772-53289 |
| `date6` | 작성일 | date | 100% | 2026년 1월 31일 |
| `접수번호2` | 접수번호 | text | 100% |  |
| `외국인2` | 외국인 | text | 100% |  |
| `변경사항2` | 변경사항 | text | 100% |  |
| `이미신고된내용2` | 이미신고(허가)된내용 | text | 100% | 급여 수령 |
| `변경내용2` | 변경내용 | text | 100% | 사업자금 |

### [필수] 개인(신용)정보 수집 이용 동의서(외투용)_영문 (`hf250`) — 키 3개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `GeneralPersonalInformation` | ■■GeneralPersonalInformation | text | 100% |  |
| `check.identityverificationinformation` | identityverificationinformation? | checkbox | 100% | Agree |
| `check.personalcreditinformation` | personalcreditinformation? | checkbox | 100% | Agree |

### [필수] 개인(신용)정보 수집 이용 동의서(외투용)_국문 (`hf251`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `일반개인정보` | ■■일반개인정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 강순준 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 강순준 |
| `seal.signer2` | 대리인성명 | seal | 100% | 강순준 |
| `sign.signer2` | 대리인성명 | signature | 100% | 이주원 |
| `대리인은일반개인정보제공에한함` | 대리인은일반개인정보제공에한함 | text | 100% |  |

### 외국환 신고(확인)필증 (`hf252`) — 키 29개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `반출입구분` | 반출입구분(ExorImport) | text | 100% |  |
| `휴대_목록[].통화종류CodeofCurrency` | 통화종류CodeofCurrency | text | 100% | USD |
| `송금` | 송금(Remitted) | text | 100% |  |
| `기타` | 기타(FromOthereligiblesources) | text | 100% | 주택구입 |
| `휴대_목록[].형태Form` | 형태Form | text | 100% |  |
| `목록[].형태Form` | 형태Form | text | 100% |  |
| `휴대_목록[].통화별금액AmountineachCurrency` | 통화별금액AmountineachCurrency | number | 100% | 41,540,000 |
| `목록[].통화별금액AmountineachCurrency` | 통화별금액AmountineachCurrency | number | 100% | 7,390,000 |
| `휴대_목록[].합계Sum` | 합계(미화상당)Sum(US$equiv) | number | 100% | 288,590,000원 |
| `목록[].합계Sum` | 합계(미화상당)Sum(US$equiv) | number | 100% | 46,600,000 |
| `휴대_목록[].반출입용도Use` | 반출입용도Use | text | 100% | 하나 정기예금 |
| `목록[].반출입용도Use` | 반출입용도Use | text | 100% | 하나 MMF |
| `휴대_목록[].비고` | 비고(Note)(수표번호등) | text | 100% | 해외 이주 |
| `목록[].비고` | 비고(Note)(수표번호등) | text | 100% | 결혼자금 |
| `국적Nationality` | 국적Nationality | text | 100% |  |
| `목록[].일자Date` | 일자Date | date | 100% | 2025년 6월 21일 |
| `목록[].금액Amount` | 금액Amount | number | 100% | 14,460,000 |
| `확인ResponsibleOfficial` | 확인ResponsibleOfficial | text | 100% |  |
| `통화종류CodeofCurrency` | 통화종류CodeofCurrency | text | 100% | CNY |
| `확인기관ConfirmationOffice` | 확인기관ConfirmationOffice | text | 100% |  |
| `확인자Signature` | 확인자Signature | text | 100% |  |
| `seal.signer` | 신고인서명 | seal | 100% | 박찬연 |
| `sign.signer` | 신고인서명 | signature | 100% | 강순준 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.name2` | Name | text | 100% | 박찬연 |
| `Initial` | Initial | text | 100% |  |
| `customer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `PassportNo` | PassportNo. | text | 100% | M94858247 |
| `ExpectedTermofStayTo` | ExpectedTermofStayTo | text | 100% |  |

### ( ) 변경신고(수리)서 (`hf253`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `변경사유` | 변경사유(요약) | text | 100% | 투자 목적 |
| `변경내용` | 변경내용 | text | 100% | 자녀 교육비 |
| `변경후` | 변경후 | text | 100% | 타행 이체 |
| `신고번호` | 신고(수리)번호 | text | 100% | 344671-9047798 |
| `신고금액` | 신고(수리)금액 | number | 100% | 77,380,000 |
| `유효기간` | 유효기간 | text | 100% |  |
| `signer.name` | 상호또는성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호또는성명 | seal | 100% | (주)스마트에프앤비 |
| `sign.signer` | 상호또는성명 | signature | 100% | (주)유니온무역 |
| `주소또는소재지` | 주소또는소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `기신고사항` | 기신고(수리)사항 | text | 100% |  |
| `나금액` | 나.금액 | number | 100% | 33,120,000 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 외국환은행의장 | text | 100% | 박찬연 |
| `seal.signer2` | 외국환은행의장 | seal | 100% | 박찬연 |
| `sign.signer2` | 외국환은행의장 | signature | 100% | 강순준 |
| `가신고번호` | 가.신고(수리)번호 | text | 100% | 5524-1965 |

### 금전의 대차계약 신고서 (`hf254`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | (주)유니온무역 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | 주식회사 한빛패션 |
| `company.biz_item` | 업종(직업) | text | 100% | 무역 |
| `check.차주` | 차주 | checkbox | 100% | 기관투자가 |
| `check.대주` | 대주 | checkbox | 100% | 기관투자가 |
| `check.통화및금액` | 통화및금액 | checkbox | 100% | 외화(1미화 1천만달러 이하 2미화 1천만달러 초과) |
| `차입대출일` | 차입/대출일 | date | 100% | 2024-12-31 |
| `적용금리` | 적용금리 | number | 100% | 50 |
| `대차기간` | 대차기간 | text | 100% |  |
| `사용용도` | 사용용도 | text | 100% | 사업자금 |
| `상환방법` | 상환방법 | text | 100% | 원금균등분할상환 |
| `check.거주자의보증또는담보유무` | 거주자의보증또는담보유무 | checkbox | 100% | 보증제공 |
| `신고번호` | 신고번호 | text | 100% | 0847-0320 |
| `신고금액` | 신고금액 | number | 100% | 3,000,000원 |
| `date` | 신고일자 | date | 100% | 2026.01.31 |
| `유효기간` | 유효기간 | text | 100% |  |
| `기타참고사항` | 기타참고사항 | text | 100% | 타행 이체 |
| `처리기간` | 처리기간 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `신고기관` | 신고기관 | text | 100% |  |

### 자(손자)회사 사업계획서 (`hf255`) — 키 41개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `현지법인명` | 현지법인명 | text | 100% | (주)우진시스템즈 |
| `company.address` | 소재지(주소) | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `총자산` | 총자산 | text | 100% |  |
| `company.biz_item` | 업종(제품) | text | 100% | 무역 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `자본금` | 자본금 | text | 100% |  |
| `설립등기일` | 설립등기일 | date | 100% | 2026년 10월 29일 |
| `자회사명` | 자(손자)회사명 | text | 100% | 주식회사 대성패션 |
| `company.address2` | 소재지(주소) | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `자본금2` | 자본금 | text | 100% |  |
| `check.투자형태` | 투자형태 | checkbox | 100% | 단독투자 |
| `check.법인성격` | 법인성격 | checkbox | 100% | 특수목적회사(SPC) |
| `company.ceo2` | 대표자 | text | 100% | 강순준 |
| `company.established` | 설립(예정)일 | date | 100% | 2022.05.19 |
| `company.biz_item2` | 업종(제품) | text | 100% | 무역 |
| `check.설립형태` | 설립형태 | checkbox | 100% | 신설법인 설립 |
| `증권종류` | 증권종류 | text | 100% |  |
| `주수` | 주수 | text | 100% |  |
| `주당액면` | 주당액면 | text | 100% |  |
| `취득가액이액면과상이할경우그산출근거` | 취득가액이액면과상이할경우그산출근거 | number | 100% | 7,120,000 |
| `주당가액` | 주당가액 | number | 100% | 4,050,000원 |
| `check.자회사설립` | 자회사설립 | checkbox | 100% | 손자회사 설립 |
| `투자형태` | 투자형태 | text | 100% |  |
| `법인성격` | 법인성격 | text | 100% |  |
| `현금` | 현금 | text | 100% |  |
| `주식` | 주식 | text | 100% |  |
| `기술투자` | 기술투자 | text | 100% |  |
| `현물` | 현물 | text | 100% |  |
| `이익잉여금` | 이익잉여금 | text | 100% |  |
| `기타` | 기타() | text | 100% | 해외 이주 |
| `한국측_목록[].출자자명` | 출자자명 | text | 100% |  |
| `현지측` | 현지측(2) | text | 100% |  |
| `제3국` | 제3국(3) | text | 100% |  |
| `한국측_목록[].금액` | 금액 | text | 100% | 4,430,000 |
| `소계` | 소계(1) | text | 100% |  |
| `목록[].금액` | 금액 | text | 100% | 49,620,000 |
| `합계` | 합계(1+2+3) | number | 100% | 3,260,000 |
| `한국측_목록[].비율` | 비율(%) | text | 100% | 100 |
| `목록[].비율` | 비율(%) | text | 100% | 100 |
| `토지건물기계설비운영자금` | 토지건물기계설비운영자금 | text | 100% |  |
| `차입금자본금` | 차입금자본금 | text | 100% |  |

### 외국환업무 등록 신청서 (`hf256`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 상호(본점) | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표자(본점) | text | 100% | 박찬연 |
| `본점소재지주` | 본점소재지주 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `외국환업무의내용` | 외국환업무의내용 | text | 100% | 사업자금 |
| `자기자본` | 자기자본 | number | 100% | 7,080,000 |
| `영업점수` | 영업점수 | number | 100% | 36 |
| `외국환업무취급점` | 외국환업무취급점 | number | 100% | 1 |
| `위험관리전산시스템명` | 위험관리전산시스템명 | text | 100% |  |
| `company.established` | 설립연월일 | date | 100% | 2026년 1월 31일 |
| `customer.nationality` | 국적(대표자) | text | 100% | 대한민국 |
| `납입자본` | 납입자본 | number | 100% | 890,000 |
| `처리기간` | 처리기간 | text | 100% |  |
| `도입시기` | 도입(개발)시기 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `인력현황` | 인력현황 | text | 100% |  |

### 환전업무 등록신청서 (`hf258`) — 키 9개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 상호 | text | 100% | (주)유니온무역 |
| `customer.address` | 주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `check.등록구분` | 등록구분 | checkbox | 100% | 무인환전기기 |
| `기타` | 기타 | text | 100% | 해외 이주 |
| `check.동의함` | 동의함 | checkbox | 100% | 동의함 |
| `환전업시작일` | 환전업시작일 | date | 100% | 2025-01-23 |
| `근거법령` | 근거법령 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `행정정보공동` | 행정정보공동 | text | 100% |  |

### 환전업무 등록내용 변경 신고서 (`hf259`) — 키 10개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `변경전` | 변경전 | text | 100% | 만기 해지 |
| `company.name` | 상호 | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `변경사유` | 변경사유 | text | 100% | 생활자금 |
| `변경후` | 변경후 | text | 100% | 사업자금 |
| `check.동의함` | 동의함 | checkbox | 100% | 동의하지않음 |
| `company.established` | 설립연월일 | date | 100% | 2026년 1월 31일 |
| `근거법령` | 근거법령 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 외국환업무 등록내용 변경 신고서 (`hf260`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 상호(본점) | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표자(본점) | text | 100% | 박찬연 |
| `본점소재지주` | 본점소재지주 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `위험관리시스템명` | 위험관리시스템명 | text | 100% |  |
| `자기자본` | 자기자본 | text | 100% |  |
| `명칭` | 명칭 | text | 100% | 주식회사 한빛패션 |
| `company.address` | 본점소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `외국환업무의내용` | 외국환업무의내용 | text | 100% | 전세자금 |
| `company.established` | 설립연월일 | date | 100% | 2026년 1월 31일 |
| `customer.nationality` | 국적(대표자) | text | 100% | 대한민국 |
| `납입자본` | 납입자본 | number | 100% | 8,530,000 |
| `도입시기` | 도입(개발)시기 | text | 100% |  |
| `목록[].변경후` | 변경후 | text | 100% | 전세자금 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 환전업무 폐지 신고서 (`hf261`) — 키 6개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `폐지사유` | 폐지사유 | text | 100% | 타행 이체 |
| `company.name` | 상호 | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.established` | 설립연월일 | date | 100% | 2026년 1월 31일 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 상호계산신고서 (`hf262`) — 키 17개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `상호대표자성명` | 상호,대표자성명 | text | 100% | 주식회사 미래로지스 |
| `주소및전화번호` | 주소및전화번호 | phone | 100% | 010-7321-8870 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 729-81-00871 |
| `상호및대표자` | 상호및대표자(지정) | text | 100% | (주)유니온무역 |
| `foreign.address` | 주소 | text | 100% | 45 Le Loi St, District 1, Ho Chi Minh Ci… |
| `company.biz_item2` | 업종 | text | 100% | 무역 |
| `자본금` | 자본금(영업기금) | text | 100% |  |
| `본지사여부` | 본지사여부 | text | 100% |  |
| `회계기간` | 회계기간 | text | 100% |  |
| `변경내용` | 변경내용 | text | 100% | 전세자금 |
| `지사설치유효기간` | 지사설치유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신고인 | text | 100% | 박찬연 |
| `seal.signer` | 신고인 | seal | 100% | 박찬연 |
| `sign.signer` | 신고인 | signature | 100% | 이민빈 |

### 지급등의 방법(변경)신고(보고)서 (`hf263`) — 키 30개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `변경` | 변경 | text | 100% |  |
| `company.name` | 상호 | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표자성명 | text | 100% | 박찬연 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 729-81-00871 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `check.거래종류` | 거래종류 | checkbox | 100% | 자본거래 |
| `check.결제방법` | 결제방법 | checkbox | 100% | 기타( |
| `계약금액` | 계약금액 | number | 100% | 298,970,000 |
| `check.결제방법2` | 결제방법 | checkbox | 100% | 기타( |
| `check.결제방법3` | 결제방법 | checkbox | 100% | 외국환은행을 통한 방법 |
| `check.구분` | 구분 | checkbox | 100% | 외국환은행을 통하지 아니하는 지급 |
| `결제시기` | 결제시기 | text | 100% |  |
| `상호및대표자성명` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `주소전화번호` | 주소,전화번호 | phone | 100% | 010-5907-7253 |
| `당초기간` | 당초기간 | text | 100% |  |
| `당초시기` | 당초시기 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `신고금액` | 신고금액 | number | 100% | 61,150,000 |
| `변경2` | 변경 | text | 100% |  |
| `변경3` | 변경 | text | 100% |  |
| `잔액` | 잔액 | number | 100% | 219,200,000원 |
| `신고번호` | 신고번호 | text | 100% | 831-089587-41851 |
| `신고금액2` | 신고금액 | number | 100% | 3,800,000 |
| `유효기간` | 유효기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신고인 | text | 100% | 박찬연 |
| `seal.signer` | 신고인 | seal | 100% | 강순준 |
| `sign.signer` | 신고인 | signature | 100% | 박찬연 |
| `seal.signer2` | 지점 | seal | 100% | 박찬연 |
| `sign.signer2` | 지점 | signature | 100% | 이욱유 |

### 거주자간 해외직접투자 양수도 신고(보고)서 (`hf264`) — 키 34개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호또는성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호또는성명 | seal | 100% | (주)스마트에프앤비 |
| `sign.signer` | 상호또는성명 | signature | 100% | (주)유니온무역 |
| `company.address` | 소재지(주소) | text | 100% | 서울특별시 노원구 한글비석로 388-7, 8층 13호 |
| `check.투자자규모` | 투자자규모 | checkbox | 100% | 개인사업자 |
| `company.biz_no` | 사업자(주민등록)번호 | biz_no | 100% | 264-82-36559 |
| `signer2.name` | 상호또는성명 | text | 100% | (주)유니온무역 |
| `seal.signer2` | 상호또는성명 | seal | 100% | (주)유니온무역 |
| `sign.signer2` | 상호또는성명 | signature | 100% | 주식회사 대성패션 |
| `company.biz_no2` | 사업자(주민등록)번호 | biz_no | 100% | 264-82-36559 |
| `company.address2` | 소재지(주소) | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `check.투자자규모2` | 투자자규모 | checkbox | 100% | 개인 |
| `company.ceo` | 대표자명 | text | 100% | 박찬연 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `company.name` | 법인명 | text | 100% | (주)유니온무역 |
| `company.address3` | 소재지(주소) | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `date` | 신고일자 | date | 100% | 2026년 01월 31일 |
| `check.투자내역` | 투자내역 | checkbox | 100% | 투자비율 |
| `설립등기일` | 설립등기일 | date | 100% | 2029-09-06 |
| `신고번호` | 신고번호 | text | 100% | 962306-6681312 |
| `check.투자지분양도내역` | 투자지분양도내역 | checkbox | 100% | 투자비율 |
| `양수도일자` | 양수도일자 | date | 100% | 2025-08-16 |
| `양수도가액` | 양수도가액 | number | 100% | 4,090,000원 |
| `신고번호2` | 신고번호 | text | 100% | 789233-1294575 |
| `date2` | 신고일자 | date | 100% | 2026년 01월 31일 |
| `check.양수도내역` | 양수도내역( | checkbox | 100% | 전액양수도 |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer3.name` | 신고기관 | text | 100% | 박찬연 |
| `seal.signer3` | 신고기관 | seal | 100% | 박찬연 |
| `sign.signer3` | 신고기관 | signature | 100% | 강순준 |
| `상호또는성명` | 상호또는성명 | text | 100% | 동방로지스 |
| `상호또는성명2` | 상호또는성명 | text | 100% | 주식회사 누리무역 |
| `담당자및연락처` | 담당자및연락처 | phone | 100% | 010-5907-7253 |
| `지점` | 지점 | text | 100% | 범어지점 |

### 수탁기관 변경 신청서 (`hf265`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `상호또는명칭` | 상호또는명칭 | text | 100% | (주)유니온무역 |
| `상호또는명칭2` | 상호또는명칭 | text | 100% | (주)대성푸드 |
| `상호또는명칭3` | 상호또는명칭 | text | 100% | (주)유니온무역 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인(대표자) | text | 100% | 박찬연 |
| `seal.signer` | 신청인(대표자) | seal | 100% | 박찬연 |
| `sign.signer` | 신청인(대표자) | signature | 100% | 강순준 |
| `신고번호` | 신고번호 | text | 100% | 045-492725-08548 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |

### 수출대금채권 매입의뢰서 (`hf266`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `RM` | RM | text | 100% |  |
| `영업점장` | 영업점장 | text | 100% |  |
| `고객번호` | 고객번호 | text | 100% | 8414-4358 |
| `매입번호` | 매입번호 | text | 100% | 349-108495-23052 |
| `상품명` | 상품명 | text | 100% | PCB 기판 |
| `수출신고번호` | 수출신고번호 | text | 100% | 7014-7040 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인 | text | 100% | 박찬연 |
| `seal.signer` | 본인 | seal | 100% | 강순준 |
| `sign.signer` | 본인 | signature | 100% | 박찬연 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `OATNET기타` | OAT()/NET()/기타() | text | 100% | 학자금 |

### 외국환거래용 인감(서명)신고서 (`hf267`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `한글` | 한글(한문) | text | 100% |  |
| `영문` | 영문 | text | 100% |  |
| `무역업고유번호` | 무역업고유번호 | text | 100% | 184-784824-68581 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `한글2` | 한글 | text | 100% |  |
| `영문2` | 영문 | text | 100% |  |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `agent.name` | 대리인 | text | 100% | 박영준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인 | text | 100% | 박찬연 |
| `seal.signer` | 본인 | seal | 100% | 이욱유 |
| `sign.signer` | 본인 | signature | 100% | 현예지 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |

### 수입선적서류 도착통지 및 수입신용장 조건불일치에 관한 조회 (`hf268`) — 키 9개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `LCNO` | L/CNO(REFNO) | text | 100% |  |
| `선적서류금액` | 선적서류금액 | number | 100% | 17,780,000 |
| `통보내역` | [은행사용란]통보내역 | text | 100% |  |
| `신용장번호` | 신용장번호 | text | 100% | 304182-4395399 |
| `선적서류금액2` | 선적서류금액 | number | 100% | 198,950,000 |
| `불일치내용` | 불일치내용 | text | 100% | 투자 목적 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |

### REDEMPTION OF OUR LETTERS OF GUARANTEE (`hf272`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `NumberofLG` | NumberofL/G | text | 100% |  |
| `NumberofCredit` | NumberofCredit | text | 100% |  |
| `LGAmount` | L/GAmount | text | 100% |  |
| `NumberofBL` | NumberofB/L | text | 100% |  |
| `VesselName` | VesselName | text | 100% |  |
| `Gentlemen` | Gentlemen | text | 100% |  |
| `NumberofLG2` | NumberofL/G | text | 100% |  |
| `NumberofCredit2` | NumberofCredit | text | 100% |  |
| `LGAmount2` | L/GAmount | text | 100% |  |
| `NumberofBL2` | NumberofB/L | text | 100% |  |
| `VesselName2` | VesselName | text | 100% |  |
| `Gentlemen2` | Gentlemen | text | 100% |  |
| `NumberofLG3` | NumberofL/G | text | 100% |  |
| `NumberofCredit3` | NumberofCredit | text | 100% |  |
| `LGAmount3` | L/GAmount | text | 100% |  |
| `NumberofBL3` | NumberofB/L | text | 100% |  |
| `VesselName3` | VesselName | text | 100% |  |
| `Gentlemen3` | Gentlemen | text | 100% |  |

### [서식관리프로그램] 수입신용장 취소 및 수입보증금 환급 신청서 (`hf273`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `번호` | 번호 | text | 100% | 346569-4725193 |
| `금액` | 금액 | number | 100% | 277,880,000 |
| `유효기일` | 유효기일 | date | 100% | 2027.11.23 |
| `취소신청금액` | 취소신청금액 | number | 100% | 39,400,000원 |
| `환급신청금액` | 환급신청금액 | number | 100% | 39,550,000 |
| `account` | 입금계좌 | account_no | 100% | 000-287736-52424 |
| `기타` | 기타 | text | 100% | 주택구입 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 강순준 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |

### 「외국환서식관리프로그램」신용장 분실신고 및 재발행 신청서 (`hf274`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `분실사유` | 분실사유 | text | 100% | 사업자금 |
| `첨부서류분실신용장사본` | 첨부서류:분실신용장사본 | text | 100% |  |
| `통지번호` | 통지번호 | text | 100% | 8043-9317 |
| `LC번호` | L/C번호 | text | 100% | 348-004031-93969 |
| `금액` | 금액 | number | 100% | 540,000 |
| `유효기일` | 유효기일 | date | 100% | 2026.11.26 |
| `발행은행` | 발행은행 | text | 100% | 농협은행 |
| `수익자` | 수익자 | text | 100% |  |
| `개설의뢰인` | 개설의뢰인 | text | 100% |  |
| `발행일` | 발행일 | date | 100% | 2025.04.01 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 이욱유 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |

### 수입신용장 재개설 및 중계에 관한 약정서 (`hf275`) — 키 17개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `RM` | RM | text | 100% |  |
| `영업점장` | 영업점장 | text | 100% |  |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `은행명` | 은행명 | text | 100% | 국민은행 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `은행명2` | 은행명 | text | 100% | 하나은행 |
| `나개설의뢰인` | 나.개설의뢰인 | text | 100% |  |
| `다개설금액` | 다.개설금액 | number | 100% | 4,220,000 |
| `라신용장번호` | 라.신용장번호 | text | 100% | 730723-3854518 |
| `나포괄약정인경우` | 나.포괄약정인경우 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 갑 | text | 100% | 박찬연 |
| `seal.signer` | 갑 | seal | 100% | 강순준 |
| `sign.signer` | 갑 | signature | 100% | 이민빈 |
| `signer2.name` | 을 | text | 100% | 박찬연 |
| `seal.signer2` | 을 | seal | 100% | 이민빈 |
| `sign.signer2` | 을 | signature | 100% | 박찬연 |

### 확약서(단기수출보험(본지사금융)) (`hf276`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `소` | 소 | text | 100% |  |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `company.name` | 업체명 | text | 100% | (주)유니온무역 |
| `signer.name` | 자 | text | 100% | 박찬연 |
| `seal.signer` | 자 | seal | 100% | 강순준 |
| `sign.signer` | 자 | signature | 100% | 박찬연 |

### 포페이팅 의뢰서 (`hf277`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `고객번호` | 고객번호 | text | 100% | 6756-0270 |
| `거래번호` | 거래번호 | text | 100% | 505-927028-62208 |
| `check.Forfaiting종류` | Forfaiting종류(해당항목선택) | checkbox | 100% | 인수후 비소구조건 매입 |
| `ForfaitingAmount` | ForfaitingAmount | text | 100% |  |
| `LCNO` | L/CNO. | text | 100% |  |
| `LCIssuingBank` | L/CIssuingBank | text | 100% |  |
| `Applicant` | Applicant | text | 100% | (주)새한화학 |
| `Tenor` | Tenor | text | 100% |  |
| `ExpiryDate` | ExpiryDate | date | 100% | 2025.01.23 |
| `ShipmentDate` | ShipmentDate | date | 100% | 2025.04.14 |
| `account` | 입금계좌번호 | account_no | 100% | 000-287736-52424 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인 | text | 100% | 박찬연 |
| `seal.signer` | 본인 | seal | 100% | 박찬연 |
| `sign.signer` | 본인 | signature | 100% | 현예지 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |

### 판매대금추심의뢰서 매입(취소) 등록 요청/확인서 (`hf278`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].번호` | 번호 | text | 100% | 795-985854-17872 |
| `목록[].종류` | 종류 | text | 100% | 하나 적금 |
| `목록[].통화코드` | 통화코드 | text | 100% | AUD |
| `목록[].매입금액` | 매입(추심)금액 | text | 100% | 610,000 |
| `목록[].판매대금추심의뢰서번호` | 판매대금추심의뢰서번호 | text | 100% | 88,450,000원 |
| `목록[].매입점포코드` | 매입(추심)점포코드 | text | 100% | 80593 |
| `FAX` | FAX()- | phone | 100% | 043-783-2775 |
| `FAX2` | FAX()- | phone | 100% | 043-783-2775 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 부(지점) | text | 100% | 박찬연 |
| `seal.signer` | 부(지점) | seal | 100% | 강순준 |
| `sign.signer` | 부(지점) | signature | 100% | 박찬연 |
| `signer2.name` | 부(지점) | text | 100% | 박찬연 |
| `seal.signer2` | 부(지점) | seal | 100% | 현예지 |
| `sign.signer2` | 부(지점) | signature | 100% | 박찬연 |
| `추심의뢰` | 추심의뢰 | text | 100% |  |
| `개설점포` | 개설점포 | text | 100% | 범어지점 |
| `점포` | 점포 | text | 100% |  |

### 추심의뢰서(Renego) (`hf279`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].OurRefNo` | OurRef.No. | text | 100% | 683-418491-97938 |
| `목록[].Amount` | Amount | text | 100% | USD 141,400 |
| `목록[].사유` | 사유(하자내용등) | text | 100% | 하나 적금 |
| `수신` | 수신 | text | 100% |  |
| `참조` | 참조 | text | 100% |  |
| `발신` | 발신 | text | 100% |  |
| `목록[].Discrepancies` | Discrepancies | text | 100% |  |
| `To` | To | text | 100% |  |
| `Attn` | Attn | text | 100% |  |
| `From` | From | text | 100% |  |
| `date` | Date | date | 100% | 2026.01.31 |

### 추심 수출환어음 종결처리(유예) 요청서 (`hf280`) — 키 25개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `거래번호` | 거래번호 | text | 100% | 7495-7697 |
| `추심금액` | 추심금액 | number | 100% | 89,940,000 |
| `추심의뢰일` | 추심의뢰일 | date | 100% | 2025년 1월 3일 |
| `신용장번호계약서번호` | 신용장번호/계약서번호 | text | 100% | 110-021637-46328 |
| `개설일자` | 개설일자 | date | 100% | 2025.05.17 |
| `유효기일` | 유효기일 | date | 100% | 2025.03.14 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 상호(명판및직인) | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호(명판및직인) | seal | 100% | (주)스마트에프앤비 |
| `sign.signer` | 상호(명판및직인) | signature | 100% | (주)유니온무역 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `거래번호2` | 거래번호 | text | 100% | 362-158718-14069 |
| `추심금액2` | 추심금액 | number | 100% | 19,330,000원 |
| `추심의뢰일2` | 추심의뢰일 | date | 100% | 2026-01-17 |
| `신용장번호계약서번호2` | 신용장번호/계약서번호 | text | 100% | 6878-2031 |
| `개설일자2` | 개설일자 | date | 100% | 2025-01-28 |
| `유효기일2` | 유효기일 | date | 100% | 2025-06-23 |
| `취급점2` | 취급점 | text | 100% | 범어지점 |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 상호(명판및직인) | text | 100% | (주)유니온무역 |
| `seal.signer2` | 상호(명판및직인) | seal | 100% | 주식회사 한빛패션 |
| `sign.signer2` | 상호(명판및직인) | signature | 100% | (주)유니온무역 |
| `customer.phone2` | 전화번호 | phone | 100% | 010-7321-8870 |

### 「외국환서식관리프로그램」조건변경부 신용장양도(SKY T/S) 조건변경.취소 신청서 (`hf281`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.전문사본요청합니다` | 전문사본요청합니다. | checkbox | 100% | 전문사본 요청합니다. |
| `FAX` | FAX | phone | 100% | 043-783-2775 |
| `유효기일` | 유효기일 | date | 100% | 2026.03.27 |
| `제시기일` | 제시기일 | date | 100% | 2030년 1월 17일 |
| `선적기일` | 선적기일 | date | 100% | 2028-06-13 |
| `부보비율` | 부보비율 | number | 100% | 10 |
| `목록[].변경후` | 변경후 | text | 100% | 결혼자금 |
| `check.신용장양도` | 신용장양도(SKYT/S) | checkbox | 100% | 조건변경 신청서 |
| `check.취소` | 취소 | checkbox | 100% | 취소 |
| `기발행SKYTS번호` | 기발행SKYT/S번호 | text | 100% | 8826-1228 |
| `본건양도후신용장잔액` | 본건양도후신용장잔액 | number | 100% | 18,610,000 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 강순준 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |

### 「외국환서식관리프로그램」조건변경부 신용장양도(SKY T/S) 신청서 (`hf282`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.전문사본요청합니다` | 전문사본요청합니다. | checkbox | 100% | 전문사본 요청합니다. |
| `FAX` | FAX | phone | 100% | 043-783-2775 |
| `유효기일` | 유효기일 | date | 100% | 2028-08-06 |
| `제시기일` | 제시기일 | date | 100% | 2028.03.20 |
| `선적기일` | 선적기일 | date | 100% | 2029.08.16 |
| `부보비율` | 부보비율 | number | 100% | 100 |
| `목록[].조건변경부신용장내용` | 조건변경부신용장내용 | text | 100% | 해외 이주 |
| `제2수익자상호` | 제2수익자상호 | text | 100% | 한빛물산 |
| `제2수익자주소` | 제2수익자주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `통지은행명및주소` | 통지은행명및주소 | text | 100% | 기업은행 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 강순준 |

### 인감증(외국환업무) (`hf283`) — 키 6개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `seal.signer` | 인감증번호 | seal | 100% | 박찬연 |
| `sign.signer` | 인감증번호 | signature | 100% | 강순준 |
| `유효기간` | 유효기간 | text | 100% |  |
| `한글` | 한글(한문) | text | 100% |  |
| `영문` | 영문 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 인감증 분실신고 및 재발급 신청서(외국환업무) (`hf284`) — 키 7개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `각영업점앞통보` | 각영업점앞통보 | text | 100% | 둔산지점 |
| `재발급` | 재발급 | text | 100% |  |
| `분실사유` | 분실사유 | text | 100% | 의료비 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 인 | text | 100% | 박찬연 |
| `seal.signer` | 인 | seal | 100% | 이욱유 |
| `sign.signer` | 인 | signature | 100% | 박찬연 |

### 인감증 발급신청서(외국환업무) (`hf285`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `seal.signer` | 인감증번호 | seal | 100% | 현예지 |
| `sign.signer` | 인감증번호 | signature | 100% | 박찬연 |
| `발급일자` | 발급일자 | date | 100% | 2025-01-15 |
| `유효기간` | 유효기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 인 | text | 100% | 박찬연 |
| `seal.signer2` | 인 | seal | 100% | 박찬연 |
| `sign.signer2` | 인 | signature | 100% | 강순준 |

### 신용장 확인 신청 및 확약서 (`hf286`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `check.CREDITNO` | CREDITNO.(신용장번호) | checkbox | 100% | CREDIT NO. (신용장번호) |
| `check.ADVICENO` | ADVICENO.(신용장통지번호) | checkbox | 100% | ADVICE NO.(신용장통지번호) |
| `check.ISSUINGBANK` | ISSUINGBANK(개설은행) | checkbox | 100% | ISSUING BANK(개설은행) |
| `check.ISSUINGDATE` | ISSUINGDATE(개설일) | checkbox | 100% | ISSUING DATE(개설일) |
| `check.AMOUNT` | AMOUNT(금액) | checkbox | 100% | AMOUNT(금액) |
| `signer.name` | (본인) | text | 100% | 박찬연 |
| `seal.signer` | (본인) | seal | 100% | 박찬연 |
| `sign.signer` | (본인) | signature | 100% | 강순준 |
| `check.CREDITNO2` | CREDITNO.(신용장번호) | checkbox | 100% | CREDIT NO. (신용장번호) |
| `check.ADVICENO2` | ADVICENO.(신용장통지번호) | checkbox | 100% | ADVICE NO.(신용장통지번호) |
| `check.ISSUINGBANK2` | ISSUINGBANK(개설은행) | checkbox | 100% | ISSUING BANK(개설은행) |
| `check.ISSUINGDATE2` | ISSUINGDATE(개설일) | checkbox | 100% | ISSUING DATE(개설일) |
| `check.AMOUNT2` | AMOUNT(금액) | checkbox | 100% | AMOUNT(금액) |

### 「외국환서식관리프로그램」신용장 양도 조건변경/취소 신청서 (Amendment / Cancellation) (`hf287`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.Amendment` | Amendment | checkbox | 100% | Amendment |
| `check.Cancellation` | Cancellation | checkbox | 100% | Cancellation |
| `date` | Date | date | 100% | 2026년 01월 31일 |
| `LCNo` | L/CNo. | text | 100% | 2474-7930 |
| `LCAmount` | L/CAmount | text | 100% |  |
| `IssuingBank` | IssuingBank | text | 100% |  |
| `TSNo` | T/SNo | text | 100% | 7833-2441 |
| `TSAmount` | T/SAmount | text | 100% |  |
| `Gentlemen` | Gentlemen | text | 100% |  |
| `check.amend` | amend | checkbox | 100% | amend |
| `check.cancel` | cancel | checkbox | 100% | partially |
| `check.increasedby` | increasedby | checkbox | 100% | increased by |
| `Amount` | Amount | amount | 100% | USD 129,000 |
| `check.decreasedby` | decreasedby | checkbox | 100% | decreased by |
| `Latestshippingdate` | Latestshippingdate | date | 100% |  |
| `Expirydate` | Expirydate | date | 100% |  |

### 「외국환서식관리프로그램」신용장 양도 신청서(Application for Total/Partial transfer) (`hf288`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.Total` | Total | checkbox | 100% | Total |
| `check.Partial` | Partial | checkbox | 100% | Partial |
| `date` | Date | date | 100% | 2026.01.31 |
| `LCNo` | L/CNo. | text | 100% | 4185-2150 |
| `Dated` | Dated | date | 100% | 2025.11.08 |
| `IssuingBank` | IssuingBank | text | 100% |  |
| `Amount` | Amount | amount | 100% | USD 143,400 |
| `Beneficiary` | Beneficiary | text | 100% |  |
| `Accountee` | Accountee | text | 100% |  |
| `Gentlemen` | Gentlemen | text | 100% |  |
| `Amounttobetransferred` | Amounttobetransferred | text | 100% |  |
| `Latestshippingdate` | Latestshippingdate | date | 100% |  |
| `Expirydate` | Expirydate | date | 100% |  |
| `check.thefirstbene` | thefirstbeneficiary. | checkbox | 100% | the first beneficiary. |
| `check.thesecondben` | thesecondbeneficiary. | checkbox | 100% | the second beneficiary. |

### 수출환어음등의 재매입을 위한 약정서 (`hf289`) — 키 6개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `RM` | RM | text | 100% |  |
| `영업점장` | 영업점장 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인 | text | 100% | 박찬연 |
| `seal.signer` | 본인 | seal | 100% | 강순준 |
| `sign.signer` | 본인 | signature | 100% | 박찬연 |

### 수출환어음 추심 후 매입전환 신청서 (`hf290`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `RM` | RM | text | 100% |  |
| `영업점장` | 영업점장 | text | 100% |  |
| `거래번호` | 거래번호(추심번호) | text | 100% | 131295-0106660 |
| `추심의뢰일자` | 추심의뢰일자 | date | 100% | 2025.10.22 |
| `추심금액` | 추심금액 | number | 100% | 279,150,000 |
| `예정만기일` | 예정(확정)만기일 | date | 100% | 2028.03.29 |
| `신용장번호` | 신용장번호 | text | 100% | 711351-2171261 |
| `신용장개설은행` | 신용장개설은행 | text | 100% | 신한은행 |
| `신용장개설의뢰인` | 신용장개설의뢰인 | text | 100% |  |
| `signer.name` | 본인 | text | 100% | 박찬연 |
| `seal.signer` | 본인 | seal | 100% | 현예지 |
| `sign.signer` | 본인 | signature | 100% | 강순준 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `거래형태` | 거래형태 | text | 100% |  |

### 「외국환서식관리프로그램」수출대금채권 양도에 따른 대금지급지시서 및 동의통지서 (`hf291`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | Name | text | 100% | 박찬연 |
| `Title` | Title | text | 100% |  |
| `customer.name2` | Name | text | 100% | 박찬연 |
| `Title2` | Title | text | 100% |  |
| `date` | Date | date | 100% | 2026.01.31 |
| `signer.name` | [수출상] | text | 100% | 박찬연 |
| `seal.signer` | [수출상] | seal | 100% | 강순준 |
| `sign.signer` | [수출상] | signature | 100% | 박찬연 |
| `customer.name3` | 이름 | text | 100% | 박찬연 |
| `employer.position` | 직위 | text | 100% | 대리 |
| `signer2.name` | [수입상] | text | 100% | 박찬연 |
| `seal.signer2` | [수입상] | seal | 100% | 박찬연 |
| `sign.signer2` | [수입상] | signature | 100% | 현예지 |
| `customer.name4` | 이름 | text | 100% | 박찬연 |
| `employer.position2` | 직위 | text | 100% | 대리 |
| `date2` | 일자 | date | 100% | 2026.01.31 |

### 수입통관도우미서비스 이용신청서 (`hf292`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 업체명 | text | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `신용장번호` | 신용장(또는당발송금)번호 | text | 100% | 642-327668-63356 |
| `선적일` | 선적(예정)일 | date | 100% | 2025-11-23 |
| `품목` | 품목 | text | 100% | LED 모듈 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 이민빈 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer2` | 지점 | seal | 100% | 강순준 |
| `sign.signer2` | 지점 | signature | 100% | 박찬연 |
| `TEL` | TEL | text | 100% |  |

### 「외국환서식관리프로그램」선적서류 수령증 및 수입화물 대도(T/R)신청서 (`hf293`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].신용장번호` | 신용장번호 | text | 100% | 401-758730-48160 |
| `목록[].통화` | 통화 | text | 100% | GBP |
| `목록[].금액` | 금액 | text | 100% | 7,080,000원 |
| `목록[].선하증권` | 선하증권 | text | 100% |  |
| `목록[].항공화물운송장` | 항공화물운송장 | text | 100% |  |
| `목록[].상업송장보험서류` | 상업송장보험서류 | text | 100% |  |
| `목록[].선하증권번호항공화물운송장번호` | 선하증권번호/항공화물운송장번호 | text | 100% | 955-079500-39388 |
| `목록[].대도금액` | 대도금액 | text | 100% | 154,120,000 |
| `check.선적서류수령증` | 선적서류수령증 | checkbox | 100% | 선적서류 수령증 |
| `check.수입화물대도신청서` | 수입화물대도(T/R)신청서 | checkbox | 100% | 수입화물 대도(T/R) 신청서 |
| `check.본인은아래신용장에의한선` | 본인은아래신용장에의한선적서류를정히수령하였습니다. | checkbox | 100% | 본인은 아래 신용장에 의한 선적서류를 정히 수령하였습니다. |
| `check.본인은아래신용장등에의하` | 본인은아래신용장등에의하여도착된수입화물을대도(T/R)신청함에 | checkbox | 100% | 본인은 아래 신용장 등에 의하여 도착된 수입화물을 대도(T/R) 신청함에 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 강순준 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `구분` | 구분 | text | 100% |  |

### 「외국환서식관리프로그램」선적서류 (일부)매입(추심) 의뢰서(2D용) (`hf294`) — 키 42개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `RM` | RM | text | 100% |  |
| `영업점장` | 영업점장 | text | 100% |  |
| `고객번호` | 고객번호 | text | 100% | 017-097529-18689 |
| `매입번호` | 매입번호 | text | 100% | 740-840328-51567 |
| `일부매입금액` | 일부매입금액 | number | 100% | 8,080,000 |
| `일부추심금액` | 일부추심금액 | number | 100% | 2,980,000 |
| `AMOUNT` | AMOUNT | text | 100% |  |
| `COMMODITY` | COMMODITY | text | 100% |  |
| `ACCOUNTEE` | ACCOUNTEE(drawee) | text | 100% |  |
| `PRICETERM` | PRICETERM | text | 100% |  |
| `수출상대국` | 수출상대국 | text | 100% |  |
| `수출신고번호` | 수출신고번호 | text | 100% | 496-281851-55016 |
| `TENORMATURITY` | TENOR&MATURITY | text | 100% |  |
| `HSCODE` | H.S.CODE | text | 100% |  |
| `BENEFICIARY` | BENEFICIARY(drawer) | text | 100% |  |
| `FOB금액` | FOB금액 | number | 100% | 229,450,000 |
| `TOISSUINGBANK_목록[].BENE` | BENE | text | 100% |  |
| `TOREIMBANK` | TOREIM.BANK | text | 100% |  |
| `TOISSUINGBANK_목록[].BANK` | BANK | text | 100% |  |
| `BANK` | BANK | text | 100% |  |
| `TOISSUINGBANK_목록[].COMM` | COMM | text | 100% |  |
| `TOISSUINGBANK_목록[].CUST` | CUST | text | 100% |  |
| `TOISSUINGBANK_목록[].BL` | B/L | text | 100% |  |
| `TOISSUINGBANK_목록[].AWB` | AWB | text | 100% |  |
| `TOISSUINGBANK_목록[].PL` | P/L | text | 100% |  |
| `TOISSUINGBANK_목록[].IP` | I/P | text | 100% |  |
| `TOISSUINGBANK_목록[].CO` | C/O | text | 100% |  |
| `TOISSUINGBANK_목록[].IC` | I/C | text | 100% |  |
| `TOISSUINGBANK_목록[].BENECERT` | BENECERT | text | 100% |  |
| `BENECERT` | BENECERT | text | 100% |  |
| `외화계정대체` | 외화계정대체 | amount | 100% | USD 28,900 |
| `원화계정대체` | 원화계정대체 | text | 100% |  |
| `A` | A | text | 100% |  |
| `B` | B | text | 100% |  |
| `수입보증금` | 수입보증금 | number | 100% | 45,250,000 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인 | text | 100% | 박찬연 |
| `seal.signer` | 본인 | seal | 100% | 현예지 |
| `sign.signer` | 본인 | signature | 100% | 박찬연 |
| `MAILTO` | MAILTO | text | 100% |  |
| `NO` | NO | text | 100% |  |
| `FROM` | FROM | text | 100% |  |

### 보증서(수출환어음등 재매입용) (`hf295`) — 키 10개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `발행은행` | 발행은행 | text | 100% | 기업은행 |
| `신용장번호` | 신용장(계약서)번호 | text | 100% | 291-912297-03734 |
| `신용장금액` | 신용장(계약서)금액 | number | 100% | 98,560,000 |
| `발행일자` | 발행일자 | date | 100% | 2025년 10월 23일 |
| `매입금액` | 매입금액 | number | 100% | 10,240,000 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 이욱유 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |

### 매입제한 해제 신청서 (`hf296`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `신용장통지번호` | 신용장통지번호 | text | 100% | 7319-3919 |
| `신용장번호` | 신용장번호 | text | 100% | 653863-4241678 |
| `신용장금액` | 신용장금액 | number | 100% | 5,170,000 |
| `발행은행` | 발행은행 | text | 100% | 우리은행 |
| `발행일자` | 발행일자 | date | 100% | 2024.07.18 |
| `해제신청금액` | 해제신청금액 | number | 100% | 320,000 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.name` | 신청인 | text | 100% | 박찬연 |

### 단기수출보험(수출채권유동화) 청약 확인서 (`hf297`) — 키 48개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.청약종류` | 청약종류 | checkbox | 100% | 신규 |
| `한도신청액` | 한도신청액 | number | 100% | 450,000 |
| `check.일반구분1` | 일반구분1 | checkbox | 100% | 일반수출 |
| `company.name` | 상호 | text | 100% | (주)유니온무역 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `company.name2` | 상호 | text | 100% | (주)유니온무역 |
| `주소_목록[].대표자` | 대표자 | text | 100% |  |
| `company.ceo2` | 대표자 | text | 100% | 박찬연 |
| `소재국` | 소재국 | text | 100% |  |
| `check.수출자와수입자관계의본지사해당하는지여부` | 수출자와수입자관계의본지사해당하는지여부 | checkbox | 100% | 여 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `수출자명` | 수출자명 | text | 100% |  |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer.name` | 대표 | text | 100% | 박찬연 |
| `seal.signer` | 대표 | seal | 100% | 현예지 |
| `sign.signer` | 대표 | signature | 100% | 박찬연 |
| `담당자성명` | 담당자성명 | text | 100% | 여다희 |
| `check.종류` | 종류 | checkbox | 100% | CONFIRMED L/C |
| `company.name3` | 상호 | text | 100% | 주식회사 한빛패션 |
| `customer.address3` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.name4` | 상호 | text | 100% | (주)유니온무역 |
| `company.ceo3` | 대표자 | text | 100% | 박찬연 |
| `소재국2` | 소재국 | text | 100% |  |
| `소재국3` | 소재국 | text | 100% |  |
| `결제조건` | 결제조건 | text | 100% |  |
| `check.이면계약또는대응구매계약존재여부` | 이면계약또는대응구매계약존재여부 | checkbox | 100% | 있음 |
| `수출상품명` | 수출상품명 | text | 100% | 의류 원단 |
| `건수` | 건수 | number | 100% | 36 |
| `CLAIM사유및결과` | CLAIM사유및결과 | text | 100% | 사업자금 |
| `신용장방식` | 신용장방식 | text | 100% |  |
| `무신용장방식` | 무신용장방식 | text | 100% |  |
| `총거래실적` | 총거래실적 | text | 100% |  |
| `최근1년간거래실적_목록[].결제금액` | 결제금액 | number | 100% | 8,790,000 |
| `금액` | 금액 | number | 100% | 3,080,000원 |
| `최근1년간거래실적_목록[].만기경과미결제액` | 만기경과미결제액 | date | 100% | 2025.10.28 |
| `존재여부` | 존재여부 | text | 100% |  |
| `company.name5` | 상호 | text | 100% | (주)유니온무역 |
| `customer.address4` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `계약서상수입자와의관계` | 계약서상수입자와의관계 | text | 100% |  |
| `계약서상대금지급책임인` | 계약서상대금지급책임인 | number | 100% | 17,360,000 |
| `대행수입사유` | 대행수입사유 | text | 100% | 투자 목적 |
| `check.대행수입여부` | 대행수입여부 | checkbox | 100% | 여 |
| `company.ceo4` | 대표자 | text | 100% | 박찬연 |
| `소재국4` | 소재국 | text | 100% |  |
| `check.이자보상특약가입여부` | 이자보상특약가입여부 | checkbox | 100% | 미가입 |
| `이자보상특약가입여부` | 이자보상특약가입여부 | number | 100% | 1,090,000 |

### LG 보증금 환급 신청 및 확약서 (`hf300`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `RM` | RM | text | 100% |  |
| `영업점장` | 영업점장 | text | 100% |  |
| `신용장번호` | (무)신용장번호 | text | 100% | 115-842353-26102 |
| `신용장유효기일` | 신용장유효기일 | date | 100% | 2026년 7월 30일 |
| `수출상` | 수출상(Beneficiary) | text | 100% |  |
| `LG금액` | L/G금액 | number | 100% | 24,230,000 |
| `LG발행일자` | L/G발행일자 | date | 100% | 2026.01.14 |
| `BL번호및선적일자` | B/L번호및선적일자 | date | 100% | 2025.06.20 |
| `LG보증금금액` | L/G보증금금액 | number | 100% | 2,300,000원 |
| `account` | 입금계좌번호 | account_no | 100% | 000-287736-52424 |
| `signer.name` | 본인 | text | 100% | 박찬연 |
| `seal.signer` | 본인 | seal | 100% | 이민빈 |
| `sign.signer` | 본인 | signature | 100% | 박찬연 |
| `LG번호` | L/G번호 | text | 100% | 699-825726-72219 |

### Cable Nego 신청서 (`hf301`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `RM` | RM | text | 100% |  |
| `영업점장` | 영업점장 | text | 100% |  |
| `신용장번호` | 신용장번호 | text | 100% | 503-004983-93044 |
| `개설은행` | 개설은행(SWIFTCODE) | text | 100% | 기업은행 |
| `신청통화및금액` | 신청통화및금액 | number | 100% | 6,350,000 |
| `신용장유효기일` | 신용장유효기일 | date | 100% | 2028년 4월 23일 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인명 | text | 100% | 박찬연 |
| `seal.signer` | 신청인명 | seal | 100% | 이민빈 |
| `sign.signer` | 신청인명 | signature | 100% | 박찬연 |
| `담당자명` | 담당자명 | text | 100% | 박찬연 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `FAX번호` | FAX번호 | phone | 100% | 043-783-2775 |

### 「외국환서식관리프로그램」BILL OF EXCHANGE (환어음 고객용) (`hf302`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `TO` | TO | text | 100% |  |
| `TO2` | TO | text | 100% |  |
| `FOR` | FOR | text | 100% |  |
| `AT` | AT | text | 100% |  |
| `DATED` | DATED | text | 100% |  |
| `FOR2` | FOR | text | 100% |  |
| `AT2` | AT | text | 100% |  |
| `DATED2` | DATED | text | 100% |  |

### 수입실적 확인 및 증명 발급신청서(별지 제11호 서식) (`hf303`) — 키 7개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `증명발급번호` | 증명발급번호 | text | 100% | 795959-6886560 |
| `발급용도` | 발급용도 | text | 100% | 본인 요청 |
| `customer.name` | 신청인(상호,주소성명) | text | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer` | 지점장 | seal | 100% | 박찬연 |
| `sign.signer` | 지점장 | signature | 100% | 강순준 |
| `비고` | 비고 | text | 100% | 투자 목적 |

### 수출실적 확인 및 증명 발급신청서(별지 제10호 서식) (`hf304`) — 키 7개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `증명발급번호` | 증명발급번호 | text | 100% | 7907-7262 |
| `발급용도` | 발급용도 | text | 100% | 생활자금 |
| `customer.name` | 신청인(상호,주소성명) | text | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer` | 지점장 | seal | 100% | 현예지 |
| `sign.signer` | 지점장 | signature | 100% | 박찬연 |
| `비고` | 비고 | text | 100% | 해외 이주 |

### ( )예금/신탁 거래신고서 (`hf305`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | 주식회사 한빛패션 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | 주식회사 대성패션 |
| `company.biz_item` | 업종(직업) | text | 100% | 무역 |
| `예치금액` | 예치(처분)금액 | number | 100% | 4,990,000 |
| `예치후잔액` | 예치(처분)후잔액 | number | 100% | 6,000,000원 |
| `예치사유` | 예치(처분)사유 | text | 100% | 만기 해지 |
| `송금은행` | 송금은행 | text | 100% | 카카오뱅크 |
| `신고번호` | 신고번호 | text | 100% | 436-812494-79262 |
| `신고금액` | 신고금액 | number | 100% | 25,690,000원 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고기관:한국은행총재 | text | 100% | 박찬연 |
| `seal.signer2` | 신고기관:한국은행총재 | seal | 100% | 강순준 |
| `sign.signer2` | 신고기관:한국은행총재 | signature | 100% | 최우빈 |

### 증권대차계약 신고서 (`hf306`) — 키 19개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | (주)스마트에프앤비 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | 주식회사 한빛패션 |
| `company.biz_item` | 업종(직업) | text | 100% | 의류 도매 |
| `차입자` | 차입자 | text | 100% |  |
| `대여자` | 대여자 | text | 100% |  |
| `대차대상증권종류` | 대차대상증권종류 | text | 100% |  |
| `차입금액` | 차입(한도)금액 | number | 100% | 770,000 |
| `차입수량` | 차입수량 | number | 100% | 2 |
| `check.차입목적` | 차입목적 | checkbox | 100% | 위험회피거래 |
| `차입기간` | 차입기간 | text | 100% |  |
| `신고번호` | 신고번호 | text | 100% | 221-202046-02486 |
| `신고금액` | 신고금액 | number | 100% | 20,180,000 |
| `date` | 신고일자 | date | 100% | 2026년 01월 31일 |
| `유효기간` | 유효기간 | text | 100% |  |
| `기타참고사항` | 기타참고사항 | text | 100% | 계좌 정리 |
| `처리기간` | 처리기간 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `신고기관` | 신고기관 | text | 100% |  |

### 지급수단등의 수출입(변경)신고서 (`hf307`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `종류` | 종류 | text | 100% | 하나 단기채 펀드 |
| `수량` | 수량 | number | 100% | 3 |
| `수출입금액` | 수출입금액 | number | 100% | 870,000 |
| `대가결제방법` | 대가결제방법 | text | 100% |  |
| `company.name` | 상호 | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `company.address` | 소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `기타` | 기타(또는변경내용) | text | 100% | 해외 이주 |
| `신고번호` | 신고번호 | text | 100% | 785739-8542438 |
| `신고금액` | 신고금액 | number | 100% | 216,900,000 |
| `date` | 신고일자 | date | 100% | 2026년 01월 31일 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `company.name2` | 상호 | text | 100% | (주)유니온무역 |
| `company.ceo2` | 대표자 | text | 100% | 박찬연 |

### 대북투자사업계획서 (`hf308`) — 키 40개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `상호또는성명` | 상호또는성명 | text | 100% | (주)가온푸드 |
| `company.address` | 소재지(주소) | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `check.투자자규모` | 투자자규모 | checkbox | 100% | 개인사업자 |
| `총자산` | 총자산 | number | 100% | 810,000 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `설립년월일` | 설립년월일 | date | 100% | 2025.08.31 |
| `자기자본` | 자기자본(자본금) | text | 100% |  |
| `담당자및연락처` | 담당자및연락처 | phone | 100% | 010-5907-7253 |
| `company.name` | 법인명 | text | 100% | (주)유니온무역 |
| `check.법인형태` | 법인형태 | checkbox | 100% | 법인 |
| `총자본금` | 총자본금 | text | 100% |  |
| `check.투자형태주` | 투자형태주 | checkbox | 100% | 합작투자(지분율 ; |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `company.established` | 설립(예정)일 | date | 100% | 2018.11.01 |
| `현금` | 현금 | text | 100% |  |
| `주식` | 주식 | text | 100% |  |
| `기술투자` | 기술투자 | text | 100% |  |
| `자기자금` | 자기자금 | text | 100% |  |
| `현물` | 현물 | text | 100% |  |
| `이익잉여금` | 이익잉여금 | text | 100% |  |
| `기타` | 기타() | text | 100% | 주택구입 |
| `차입금` | 차입금 | text | 100% |  |
| `한국측_목록[].출자자명` | 출자자명 | text | 100% |  |
| `현지측` | 현지측(2) | text | 100% |  |
| `제3국` | 제3국(3) | text | 100% |  |
| `한국측_목록[].금액` | 금액 | text | 100% | 5,650,000 |
| `소계` | 소계(1) | text | 100% |  |
| `목록[].금액` | 금액 | text | 100% | 28,880,000 |
| `합계` | 합계(1+2+3) | number | 100% | 5,850,000 |
| `한국측_목록[].비율` | 비율(%) | text | 100% | 100 |
| `목록[].비율` | 비율(%) | text | 100% | 100 |
| `법인형태` | 법인형태 | text | 100% |  |
| `대부액` | 대부액 | text | 100% |  |
| `이율` | 이율 | number | 100% | 70 |
| `자기자금2` | 자기자금 | text | 100% |  |
| `자금용도` | 자금용도 | text | 100% | 학자금 |
| `기간` | 기간 | number | 100% | 24 |
| `차입금2` | 차입금 | text | 100% |  |
| `토지건물기계설비운영자금` | 토지건물기계설비운영자금... | text | 100% |  |
| `차입금자기자본` | 차입금자기자본 | text | 100% |  |

### 파생상품거래 신고서 (`hf309`) — 키 20개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | (주)삼정전자 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | (주)유니온무역 |
| `company.biz_item` | 업종(직업) | text | 100% | 의류 도매 |
| `상호및대표자성명` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `company.biz_item2` | 업종(직업) | text | 100% | 무역 |
| `check.거래기초자산` | 거래기초자산 | checkbox | 100% | 신용 |
| `check.거래종류` | 거래종류 | checkbox | 100% | 보장매입 |
| `계약금액` | 계약(명목)금액 | number | 100% | 48,730,000 |
| `만기` | 만기 | date | 100% | 2025-11-10 |
| `세부내용` | 세부내용 | text | 100% | 만기 해지 |
| `check.거래특이사항` | 거래특이사항 | checkbox | 100% | 자본거래시 해당자본거래와 직접 관련되는 파생상품거래를 해당자본거래의 |
| `신고번호` | 신고번호 | text | 100% | 899-075839-26450 |
| `신고금액` | 신고금액 | number | 100% | 22,000,000 |
| `date` | 신고일자 | date | 100% | 2026.01.31 |
| `유효기간` | 유효기간 | text | 100% |  |
| `기타참고사항` | 기타참고사항 | text | 100% | 만기 해지 |
| `처리기간` | 처리기간 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `신고기관` | 신고기관 | text | 100% |  |

### 대북투자사업 청산 및 대부채권 회수보고서 (`hf310`) — 키 28개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `상호또는성명` | 상호또는성명 | text | 100% | 다온정밀(주) |
| `company.biz_no` | 사업자(주민)등록번호 | biz_no | 100% | 264-82-36559 |
| `현지법인명` | 현지법인명 | text | 100% | (주)유니온무역 |
| `customer.address` | 주소(소재지) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `check.법인형태` | 법인형태 | checkbox | 100% | 기타 |
| `check.투자형태주` | 투자형태주 | checkbox | 100% | 단독투자 |
| `납입자본금` | 납입자본금 | text | 100% |  |
| `대부금액` | 대부금액 | number | 100% | 3,610,000 |
| `기회수금액` | 기회수금액 | number | 100% | 67,680,000 |
| `금회회수금액` | 금회회수금액 | number | 100% | 3,000,000 |
| `잔액` | 잔액 | number | 100% | 530,000 |
| `date` | 일자 | date | 100% | 2026.01.31 |
| `목록[].원금` | 원금 | number | 100% | 9,540,000 |
| `회수금액_목록[].원금` | 원금 | number | 100% | 200,000 |
| `check.청산` | 청산 | checkbox | 100% | 대부채권 회수 |
| `법인형태` | 법인형태 | text | 100% |  |
| `유동자산투자및기타자산고정자산이연자산` | 유동자산투자및기타자산고정자산이연자산 | text | 100% |  |
| `계` | 계 | text | 100% |  |
| `유동부채고정부채자본금잉여금` | 유동부채고정부채자본금잉여금 | text | 100% |  |
| `계2` | 계 | text | 100% |  |
| `목록[].구분회수일자` | 구분회수일자 | date | 100% | 2025-03-12 |
| `목록[].회수재산의종류` | 회수재산의종류 | text | 100% |  |
| `계3` | 계 | text | 100% |  |
| `목록[].금액` | 금액 | text | 100% | 8,600,000원 |
| `목록[].비고` | 비고 | text | 100% | 생활자금 |
| `청산종료일` | 청산종료일 | date | 100% | 2028.01.14 |
| `다청산손익` | 다.청산손익(해산일로부터청산종료일까지의손익) | text | 100% |  |
| `바회수가불가능한재산이있을경우그내역및사유` | 바.회수가불가능한재산이있을경우그내역및사유 | text | 100% | 자녀 교육비 |

### 상호계산계정 폐쇄 신고서 (`hf311`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `계정상대방` | 계정상대방 | text | 100% |  |
| `대차기잔고` | 대차기잔고 | text | 100% |  |
| `폐쇄사유` | 폐쇄사유 | text | 100% | 전세자금 |
| `기타` | 기타 | text | 100% | 자녀 교육비 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 명 | text | 100% | 박찬연 |
| `seal.signer` | 명 | seal | 100% | 박찬연 |
| `sign.signer` | 명 | signature | 100% | 강순준 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer2` | 은행장 | seal | 100% | 강순준 |
| `sign.signer2` | 은행장 | signature | 100% | 박찬연 |

### 비거주자원화계정을 통한 송금(투자)보고서 (`hf312`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `가신고수리일자및신고수리번호` | 가.신고수리일자및신고수리번호 | date | 100% | 2025.03.28 |
| `나투자국명` | 나.투자국명 | text | 100% | 독일 |
| `다투자업종` | 다.투자업종 | text | 100% |  |
| `라북한현지법인명` | 라.북한현지법인명 | text | 100% | (주)유니온무역 |
| `가수취인` | 가.수취인 | text | 100% | 주식회사 한빛패션 |
| `나비거주자원화계정계좌번호` | 나.비거주자원화계정계좌번호 | text | 100% | 096-329565-35804 |
| `송금일자` | (1)송금일자 | date | 100% | 2025-04-20 |
| `투자내용` | (3)투자내용 | text | 100% | 계좌 정리 |

### 북한지사 설치·현황 보고서 (`hf313`) — 키 37개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `date` | 일자 | date | 100% | 2026년 01월 31일 |
| `목록[].신고자` | 신고자 | text | 100% | (주)미래정밀 |
| `기업규모` | 기업규모 | text | 100% |  |
| `목록[].지사명` | 지사명 | text | 100% | (주)신영무역 |
| `목록[].설치지역` | 설치지역 | text | 100% |  |
| `구분` | 구분 | text | 100% |  |
| `투자금구분` | 투자금구분 | text | 100% |  |
| `목록[].신고금액` | 신고금액 | number | 100% | 22,630,000 |
| `신고기관` | 신고기관 | text | 100% |  |
| `date2` | 신고일자 | date | 100% | 2026년 01월 31일 |
| `송금일자` | 송금일자 | date | 100% | 2024년 8월 19일 |
| `영업기금` | 영업기금 | text | 100% |  |
| `설치비` | 설치비 | text | 100% |  |
| `기본경비` | 기본경비 | text | 100% |  |
| `기타경비` | 기타경비 | text | 100% | 계좌 정리 |
| `최초추가` | 최초,추가 | text | 100% |  |
| `지사명` | 지사명 | text | 100% | 제일푸드 |
| `구분2` | 구분(증권/부동산) | text | 100% |  |
| `취득일` | 취득일 | date | 100% | 2025.11.11 |
| `취득금액` | 취득금액 | number | 100% | 9,050,000원 |
| `처분일` | 처분일 | date | 100% | 2025-12-19 |
| `처분금액` | 처분금액 | number | 100% | 42,790,000 |
| `투자자명` | 투자자명 | text | 100% |  |
| `date3` | 신고일자 | date | 100% | 2026년 01월 31일 |
| `목록[].북한지사명` | 북한지사명 | text | 100% | (주)대성테크 |
| `주구분` | 주)구분 | text | 100% |  |
| `설치일` | 설치일 | date | 100% | 2025.08.30 |
| `date4` | 일자 | date | 100% | 2026년 01월 31일 |
| `설치지역` | 설치지역 | text | 100% |  |
| `신고금액` | 신고금액 | number | 100% | 210,000 |
| `회수구분주` | 회수구분주 | text | 100% |  |
| `회수금액` | 회수금액 | number | 100% | 299,060,000 |
| `비고` | 비고 | text | 100% | 급여 수령 |
| `구분주` | 구분주 | text | 100% |  |
| `변경일자` | 변경일자 | date | 100% | 2025-04-06 |
| `변경전` | 변경전 | text | 100% | 해외 이주 |
| `변경후` | 변경후 | text | 100% | 의료비 |

### 북한지사 설치(변경) 신고서 (`hf314`) — 키 24개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호 | seal | 100% | (주)다온커뮤니케이션 |
| `sign.signer` | 상호 | signature | 100% | (주)유니온무역 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `check.신고구분` | 신고구분 | checkbox | 100% | 설 치 |
| `check.지사구분` | 지사구분 | checkbox | 100% | 사 무 소 |
| `지사명` | 지사명 | text | 100% | (주)한빛전자 |
| `company.address` | 소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `회계기간` | 회계기간 | text | 100% |  |
| `check.설치사유` | 설치사유 | checkbox | 100% | 저임활용 |
| `내용` | 내용 | text | 100% | 생활자금 |
| `사유` | 사유 | text | 100% | 결혼자금 |
| `신고번호` | 신고번호 | text | 100% | 1269-1131 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `customer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고기관 | text | 100% | 박찬연 |
| `seal.signer2` | 신고기관 | seal | 100% | 이욱유 |
| `sign.signer2` | 신고기관 | signature | 100% | 박찬연 |
| `위의신청을다음과같이신고필함` | 위의신청을다음과같이신고필함. | text | 100% |  |

### 증권(채권)취득 보고서 (`hf315`) — 키 23개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호또는성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호또는성명 | seal | 100% | (주)유니온무역 |
| `sign.signer` | 상호또는성명 | signature | 100% | 주식회사 한빛패션 |
| `check.투자자규모` | 투자자규모 | checkbox | 100% | 개인사업자 |
| `신고수리일자` | 신고수리일자 | date | 100% | 2025년 5월 24일 |
| `설립년월일` | 설립년월일 | date | 100% | 2025.05.13 |
| `신고수리번호` | 신고수리번호 | text | 100% | 513-801972-85269 |
| `company.name` | 법인명 | text | 100% | 주식회사 한빛패션 |
| `설립등기일` | 설립등기일 | date | 100% | 2025.02.17 |
| `영업개시일` | 영업개시(예정)일 | date | 100% | 2024.06.17 |
| `결산일` | 결산일 | date | 100% | 2025.05.07 |
| `증권취득일` | 증권취득일(자본금출자일) | date | 100% | 2025년 4월 16일 |
| `액면가액합계` | 액면가액합계 | number | 100% | 9,710,000 |
| `check.증권발행여부` | 증권발행여부 | checkbox | 100% | 증권미발행 |
| `증권종류` | 증권종류 | text | 100% |  |
| `취득가액합계` | 취득가액합계 | number | 100% | 68,720,000 |
| `채권취득일` | 채권취득일 | date | 100% | 2024.08.25 |
| `이자율` | 이자율 | number | 100% | 10 |
| `check.원금회수방법` | 원금회수방법 | checkbox | 100% | 분할회수(총 |
| `대부원금` | 대부원금 | number | 100% | 2,700,000원 |
| `대부기간` | 대부기간 | text | 100% |  |
| `check.증권` | 증권 | checkbox | 100% | 증권 |
| `상호또는성명` | 상호또는성명 | text | 100% | (주)대성물산 |

### 북한지사 등의 영업활동 보고서 (`hf316`) — 키 19개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `상호또는성명` | 상호또는성명 | text | 100% | 청솔푸드(주) |
| `company.biz_no` | 사업자(주민)등록번호 | biz_no | 100% | 264-82-36559 |
| `지사명` | 지사명 | text | 100% | (주)대성시스템즈 |
| `company.address` | 소재지(주소) | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `설치일` | 설치일 | date | 100% | 2025-09-16 |
| `설치지역` | 설치지역 | text | 100% |  |
| `check.구분` | 구분 | checkbox | 100% | 사무소 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `총자산` | 총자산 | text | 100% |  |
| `매출액` | 매출액 | number | 100% | 4,970,000 |
| `순이익금` | 순이익(결손)금 | text | 100% |  |
| `영업기금잔액` | 영업기금잔액 | number | 100% | 5,440,000 |
| `영업손익금` | 영업손익금 | text | 100% |  |
| `자금차입현황` | 자금차입현황 | text | 100% |  |
| `자금대여현황` | 자금대여현황 | text | 100% |  |
| `영업기금` | 영업기금 | text | 100% |  |
| `설치비` | 설치비 | text | 100% |  |
| `유지활동비` | 유지활동비 | text | 100% |  |
| `남한파견명` | 남한파견:명 | text | 100% |  |

### 증권발행 보고서 (`hf317`) — 키 24개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `명칭` | 명칭 | text | 100% | 주식회사 미래시스템즈 |
| `signer.name` | 대표자성명 | text | 100% | 박찬연 |
| `seal.signer` | 대표자성명 | seal | 100% | 박찬연 |
| `sign.signer` | 대표자성명 | signature | 100% | 이민빈 |
| `signer2.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer2` | 상호및대표자성명 | seal | 100% | (주)유니온무역 |
| `sign.signer2` | 상호및대표자성명 | signature | 100% | (주)한빛식품 |
| `증권종류` | 증권종류 | text | 100% |  |
| `발행금액` | 발행금액 | number | 100% | 6,280,000원 |
| `계약체결시및장소` | 계약체결시및장소 | text | 100% |  |
| `표면금리` | 표면금리 | number | 100% | 20 |
| `만기` | 만기 | date | 100% | 2025.04.27 |
| `배당금지급시기및방법` | 배당금지급시기및방법 | text | 100% |  |
| `원리금상환방법` | 원리금상환방법 | text | 100% | 원금균등분할상환 |
| `자금용도` | 자금용도 | text | 100% | 결혼자금 |
| `발행관련기관` | 발행관련기관 | text | 100% |  |
| `기타` | 기타 | text | 100% | 투자 목적 |
| `액면금액및수량` | 액면금액및수량 | number | 100% | 3,090,000원 |
| `발행시기및장소` | 발행시기및장소 | text | 100% |  |
| `발행가격` | 발행가격 | text | 100% |  |
| `해외판매여부` | 해외판매여부 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `상장여부` | 상장여부 | text | 100% |  |
| `발행비용` | 발행비용 | text | 100% |  |

### 대북투자(변경)신고서 (`hf318`) — 키 30개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 상호 | text | 100% | (주)유니온무역 |
| `signer.name` | 대표자 | text | 100% | 박찬연 |
| `seal.signer` | 대표자 | seal | 100% | 박찬연 |
| `sign.signer` | 대표자 | signature | 100% | 강순준 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `check.투자구분` | 투자구분 | checkbox | 100% | 감액 |
| `check.투자방식` | 투자방식 | checkbox | 100% | 대부채권취득 |
| `투자업종` | 투자업종 | text | 100% |  |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `customer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `주요제품` | 주요제품 | text | 100% |  |
| `신고수리번호` | 신고수리번호 | rrn | 100% | 216-642241-52609 |
| `value` | (U$) | amount | 100% |  |
| `date` | 유효기간 | date | 100% | 2026년 1월 31일 |
| `처리기간` | 처리기간 | text | 100% |  |
| `현금` | 현금(U$) | text | 100% |  |
| `현물` | 현물(U$) | text | 100% |  |
| `합계` | 합계(U$) | number | 100% | 27,020,000 |
| `목록[].대부투자` | 대부투자 | text | 100% |  |
| `목록[].총투자액` | 총투자액 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고기관 | text | 100% | 박찬연 |
| `seal.signer2` | 신고기관 | seal | 100% | 강순준 |
| `sign.signer2` | 신고기관 | signature | 100% | 박찬연 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `현지법인명` | 현지법인명 | text | 100% | 새한전자 |
| `위의신고를다음과같이신고필함` | 위의신고를다음과같이신고필함. | text | 100% |  |
| `유효기간` | 유효기간 | text | 100% |  |

### 증권취득 신고서 (`hf319`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | (주)유니온무역 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | 주식회사 한빛패션 |
| `company.biz_item` | 업종(직업) | text | 100% | 무역 |
| `증권취득자` | 증권취득자 | text | 100% |  |
| `증권취득상대방` | 증권취득상대방 | text | 100% |  |
| `check.증권취득방법` | 증권취득방법 | checkbox | 100% | 현금 매수방식 |
| `check.증권종류` | 증권종류 | checkbox | 100% | 비거주자발행 1년미만 원화 또는 원화연계외화증권 |
| `액면가액` | 액면가액 | number | 100% | 87,400,000 |
| `수량` | 수량 | number | 100% | 6 |
| `취득단가` | 취득단가 | number | 100% | 42,370,000원 |
| `취득가액` | 취득가액 | number | 100% | 2,330,000 |
| `취득사유` | 취득사유 | text | 100% | 투자 목적 |
| `신고번호` | 신고번호 | text | 100% | 671634-4177699 |
| `신고금액` | 신고금액 | number | 100% | 164,880,000 |
| `date` | 신고일자 | date | 100% | 2026년 01월 31일 |
| `유효기간` | 유효기간 | text | 100% |  |
| `기타참고사항` | 기타참고사항 | text | 100% | 결혼자금 |
| `처리기간` | 처리기간 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `신고기관` | 신고기관 | text | 100% |  |

### 재환전 신청서 (`hf320`) — 키 3개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명(NAME) | text | 100% | 박찬연 |
| `여권번호` | 여권번호(PASSPORTNUMBER) | text | 100% | M69449394 |
| `입국일자` | 입국일자(ENTRANCEDATEINTOKOREA) | date | 100% | 2025.08.01 |

### 부동산취득신고(수리)서 (`hf321`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | 주식회사 한빛패션 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | (주)유니온무역 |
| `company.biz_item` | 업종(직업) | text | 100% | 무역 |
| `부동산의종류` | 부동산의종류 | text | 100% |  |
| `company.address` | 소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `면적` | 면적 | text | 100% |  |
| `취득기간` | 취득기간 | text | 100% |  |
| `취득사유` | 취득사유 | text | 100% | 본인 요청 |
| `신고번호` | 신고(수리)번호 | text | 100% | 289-004351-06976 |
| `신고금액` | 신고(수리)금액 | number | 100% | 390,000원 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `신고수리조건` | 신고수리조건 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer2` | 신고수리기관:한국은행총재 | seal | 100% | 김소윤 |
| `sign.signer2` | 신고수리기관:한국은행총재 | signature | 100% | 강순준 |
| `소` | 소(소재지) | text | 100% |  |
| `취득가액` | 취득가액 | number | 100% | 2,870,000원 |
| `위의신고를다음과같이신고수리함` | 위의신고를다음과같이신고수리함. | text | 100% |  |

### 북한사무소 경비지급신고서 (`hf322`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.신청내역` | 신청내역 | checkbox | 100% | 설 치 비 |
| `check.신청내역2` | 신청내역 | checkbox | 100% | 유지활동비 |
| `signer.name` | 성명(법인명) | text | 100% | 박찬연 |
| `seal.signer` | 성명(법인명) | seal | 100% | 박찬연 |
| `sign.signer` | 성명(법인명) | signature | 100% | 현예지 |
| `영업내용` | 영업내용 | text | 100% | 전세자금 |
| `사무소명` | 사무소명 | text | 100% |  |
| `customer.address` | 주소(소재지) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `value` | (주소)(전화번호)(e-mail) | amount | 100% |  |
| `value2` | (기본경비) | amount | 100% |  |
| `value3` | (기타경비) | amount | 100% |  |
| `customer.rrn` | 주민(사업자)등록번호 | rrn | 100% | 900210-1****** |
| `신고번호` | 신고번호 | text | 100% | 0354-1925 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고기관 | text | 100% | 박찬연 |
| `seal.signer2` | 신고기관 | seal | 100% | 강순준 |
| `sign.signer2` | 신고기관 | signature | 100% | 현예지 |
| `customer.name` | 성명(법인명) | text | 100% | 박찬연 |

### 북한지점 경비지급신고서 (`hf323`) — 키 24개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 성명(법인명) | text | 100% | 박찬연 |
| `seal.signer` | 성명(법인명) | seal | 100% | 강순준 |
| `sign.signer` | 성명(법인명) | signature | 100% | 박찬연 |
| `영업내용` | 영업내용 | text | 100% | 만기 해지 |
| `check.지점구분` | 지점구분 | checkbox | 100% | 비독립채산지점 |
| `지점명` | 지점명 | text | 100% | 범어지점 |
| `customer.address` | 주소(소재지) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `check.비독립채산지점` | 비독립채산지점 | checkbox | 100% | 설 치 비 |
| `check.비독립채산지점2` | 비독립채산지점 | checkbox | 100% | 유지활동비 |
| `영업기금` | 영업기금 | text | 100% |  |
| `비독립채산지점_목록[].value` | (주소)(전화번호)(e-mail) | amount | 100% |  |
| `value` | (기본경비) | amount | 100% |  |
| `value2` | (기본경비) | amount | 100% |  |
| `customer.rrn` | 주민(사업자)등록번호 | rrn | 100% | 900210-1659382 |
| `신고번호` | 신고번호 | text | 100% | 0845-8826 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고기관 | text | 100% | 박찬연 |
| `seal.signer2` | 신고기관 | seal | 100% | 현예지 |
| `sign.signer2` | 신고기관 | signature | 100% | 박찬연 |
| `customer.name` | 성명(법인명) | text | 100% | 박찬연 |

### 임대차계약신고서 (`hf324`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | (주)삼정전자 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | (주)유니온무역 |
| `company.biz_item` | 업종(직업) | text | 100% | 무역 |
| `임대차물종류` | 임대차물종류 | text | 100% |  |
| `company.address` | 소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `수량` | 수량 | number | 100% | 3 |
| `임대차기간` | 임대차기간 | text | 100% |  |
| `임대차사유` | 임대차사유 | text | 100% | 생활자금 |
| `신고번호` | 신고번호 | text | 100% | 3167-8700 |
| `date` | 신고일자 | date | 100% | 2026년 01월 31일 |
| `처리기간` | 처리기간 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |

### 증권취득신고서 (`hf325`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | (주)유니온무역 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | 주식회사 대성패션 |
| `company.biz_item` | 업종(직업) | text | 100% | 무역 |
| `액면가액` | 액면가액 | number | 100% | 73,980,000 |
| `수량` | 수량 | number | 100% | 6 |
| `취득단가` | 취득단가 | number | 100% | 41,940,000원 |
| `취득사유` | 취득사유 | text | 100% | 투자 목적 |
| `신고번호` | 신고번호 | text | 100% | 4120-5058 |
| `신고금액` | 신고금액 | number | 100% | 17,910,000 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer2` | 신고기관:외국환은행의장 | seal | 100% | 박찬연 |
| `sign.signer2` | 신고기관:외국환은행의장 | signature | 100% | 현예지 |

### ( )매매 신고서 (`hf326`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | (주)유니온무역 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | 주식회사 한빛패션 |
| `company.biz_item` | 업종(직업) | text | 100% | 의류 도매 |
| `매매대상물종류` | 매매대상물종류 | text | 100% |  |
| `매매사유` | 매매사유 | text | 100% | 사업자금 |
| `신고번호` | 신고번호 | text | 100% | 7284-4114 |
| `신고금액` | 신고금액 | number | 100% | 340,000원 |
| `유효기간` | 유효기간 | text | 100% |  |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 신고기관:한국은행총재 | text | 100% | 박찬연 |
| `seal.signer2` | 신고기관:한국은행총재 | seal | 100% | 현예지 |
| `sign.signer2` | 신고기관:한국은행총재 | signature | 100% | 박찬연 |
| `매매금액` | 매매금액 | number | 100% | 9,370,000 |

### 담보제공 신고서 (`hf327`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `signer.name` | 상호및대표자성명 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호및대표자성명 | seal | 100% | (주)유니온무역 |
| `sign.signer` | 상호및대표자성명 | signature | 100% | (주)스마트에프앤비 |
| `company.biz_item` | 업종(직업) | text | 100% | 의류 도매 |
| `check.담보제공자` | 담보제공자 | checkbox | 100% | 거주자/ |
| `check.담보취득자` | 담보취득자 | checkbox | 100% | 거주자/ |
| `check.담보제공수혜자` | 담보제공수혜자 | checkbox | 100% | 거주자/ |
| `check.담보물종류` | 담보물종류 | checkbox | 100% | 기타( |
| `담보소재지` | 담보소재지 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `수량` | 수량 | number | 100% | 3 |
| `담보가액` | 담보가액 | number | 100% | 640,000 |
| `담보제공기간` | 담보제공기간 | text | 100% |  |
| `check.담보제공용도` | 담보제공용도 | checkbox | 100% | 주채무계열소속 30대 계열기업체의 단기외화차입에 대한 담보제공 |
| `신고번호` | 신고번호 | text | 100% | 006352-1615394 |
| `신고금액` | 신고금액 | number | 100% | 760,000 |
| `date` | 신고일자 | date | 100% | 2026.01.31 |
| `유효기간` | 유효기간 | text | 100% |  |
| `기타참고사항` | 기타참고사항 | text | 100% | 사업자금 |
| `처리기간` | 처리기간 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `신고기관` | 신고기관 | text | 100% |  |

### 외국기업 국내지사 폐쇄신고서 (`hf328`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 상호 | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `company.address` | 소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `check.폐쇄구분` | 폐쇄구분 | checkbox | 100% | 사무소 |
| `폐쇄일자` | 폐쇄일자 | date | 100% | 2025년 8월 23일 |
| `폐쇄사유` | 폐쇄사유 | text | 100% | 생활자금 |
| `신고번호` | 신고번호 | text | 100% | 125-702414-61662 |
| `date` | 신고일자 | date | 100% | 2026년 01월 31일 |
| `처리기간` | 처리기간 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신고인 | text | 100% | 박찬연 |
| `seal.signer` | 신고인 | seal | 100% | 박찬연 |
| `sign.signer` | 신고인 | signature | 100% | 강순준 |
| `폐쇄구분` | 폐쇄구분 | text | 100% |  |
| `위와같이신고되었음을확인함` | 위와같이신고되었음을확인함. | text | 100% |  |

### 외국기업 국내지사 설치신고서 (`hf329`) — 키 20개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 상호(본점) | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표자(본점) | text | 100% | 박찬연 |
| `company.address` | 소재지(본점) | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `사업내용` | 사업내용 | text | 100% | 해외 이주 |
| `자본금` | 자본금 | text | 100% |  |
| `company.name2` | 상호 | text | 100% | (주)유니온무역 |
| `company.ceo2` | 대표자 | text | 100% | 박찬연 |
| `company.address2` | 소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `영위업종` | 영위업종 | text | 100% |  |
| `check.설치구분` | 설치구분 | checkbox | 100% | 지점 |
| `date` | 설치년월일 | date | 100% | 2026년 1월 31일 |
| `customer.rrn` | 주민등록번호(또는국적) | rrn | 100% | 900210-1****** |
| `신고번호` | 신고번호 | text | 100% | 431585-1963822 |
| `date2` | 신고일자 | date | 100% | 2026년 01월 31일 |
| `처리기간` | 처리기간 | text | 100% |  |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신고인 | text | 100% | 박찬연 |
| `seal.signer` | 신고인 | seal | 100% | 강순준 |
| `sign.signer` | 신고인 | signature | 100% | 현예지 |
| `신고기관기획재정부장관` | 신고기관:기획재정부장관 | text | 100% |  |

### 외국기업 국내지사 변경신고서 (`hf330`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `이미신고된사항` | 이미신고된사항 | text | 100% |  |
| `company.name` | 상호 | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표자 | text | 100% | 강순준 |
| `company.address` | 소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `변경사유` | 변경사유 | text | 100% | 만기 해지 |
| `변경하고자하는사항` | 변경하고자하는사항 | text | 100% |  |
| `신고번호` | 신고번호 | text | 100% | 608-140028-14355 |
| `date` | 신고일자 | date | 100% | 2026년 01월 31일 |
| `처리기간` | 처리기간 | text | 100% |  |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신고인 | text | 100% | 박찬연 |
| `seal.signer` | 신고인 | seal | 100% | 강순준 |
| `sign.signer` | 신고인 | signature | 100% | 이욱유 |
| `신고기관기획재정부장관` | 신고기관:기획재정부장관 | text | 100% |  |

### 해외지점의 영업활동 보고서 (`hf331`) — 키 17개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `상호또는성명` | 상호또는성명 | text | 100% | 삼정산업(주) |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.biz_no` | 사업자(주민)등록번호 | biz_no | 100% | 264-82-36559 |
| `지점명` | 지점명 | text | 100% | 범어지점 |
| `customer.address2` | 주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `설치일` | 설치일 | date | 100% | 2025.08.24 |
| `설치국가` | 설치국가 | text | 100% | 일본 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `총자산` | 총자산 | text | 100% |  |
| `매출액` | 매출액 | number | 100% | 20,090,000 |
| `순이익금` | 순이익(결손)금 | text | 100% |  |
| `영업기금잔액` | 영업기금잔액 | number | 100% | 740,000 |
| `영업손익금` | 영업손익금 | text | 100% |  |
| `자금차입현황` | 자금차입현황 | text | 100% |  |
| `자금대여현황` | 자금대여현황 | text | 100% |  |
| `영업기금` | 영업기금 | text | 100% |  |
| `본국파견명` | 본국파견:명 | text | 100% |  |

### 외국기업 국내 결산순이익금 송금신청서 (`hf332`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 상호(본점) | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표자(본점) | text | 100% | 박찬연 |
| `company.address` | 본점소재지 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `송금예정일자` | 송금예정일자 | date | 100% | 2024년 7월 2일 |
| `송금액산출근거` | 송금액산출근거 | number | 100% | 670,000 |
| `결산기간` | 결산기간 | number | 100% | 24 |
| `처리기간` | 처리기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 현예지 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |
| `금액` | 금액 | number | 100% | 1,210,000 |

### 송금(투자)보고서 (`hf333`) — 키 10개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `현금현물주식이익잉여금기술투자기타` | 현금현물주식이익잉여금기술투자기타() | text | 100% | 자녀 교육비 |
| `투자액` | 투자(송금)액(U$환산액) | text | 100% |  |
| `투자방법` | 투자방법 | text | 100% |  |
| `비고` | 비고(현지화) | text | 100% | 의료비 |
| `가신고일자및신고번호` | 가.신고일자및신고번호 | date | 100% | 2025.04.16 |
| `나투자국명` | 나.투자국명 | text | 100% | 필리핀 |
| `다투자업종` | 다.투자업종 | text | 100% |  |
| `라현지법인명` | 라.현지법인명 | text | 100% | (주)유니온무역 |
| `가수취인` | 가.수취인 | text | 100% | 미래테크 |
| `나구좌번호` | 나.구좌번호 | text | 100% | 2201-7126 |

### 전자적무역결제금융등록(변경,해지)신청서 (`hf334`) — 키 36개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `value` | (한글) | amount | 100% |  |
| `value2` | (영문) | amount | 100% |  |
| `company.biz_no` | 사업자번호 | biz_no | 100% | 261-82-53694 |
| `company.ceo` | 대표자성명 | text | 100% | 박찬연 |
| `value3` | (한글) | amount | 100% |  |
| `value4` | (영문) | amount | 100% |  |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.email` | E-mail | text | 100% | chanyeon363@naver.com |
| `company.corp_reg_no` | 법인번호 | corp_reg_no | 100% | 200112-7448551 |
| `대표자생년월일` | 대표자생년월일 | date | 100% | 2025-04-16 |
| `팩스번호` | 팩스번호 | phone | 100% | 043-783-2775 |
| `customer.name2` | 성명 | text | 100% | 박찬연 |
| `customer.email2` | E-mail | text | 100% | chanyeon363@naver.com |
| `원화` | 원화(KRW) | text | 100% |  |
| `미화` | 미화(USD) | text | 100% |  |
| `위안화` | 위안화(CNY) | text | 100% |  |
| `엔화` | 엔화(JPY) | text | 100% |  |
| `목록[].거래인감` | 거래인감 | text | 100% |  |
| `목록[].비고` | 비고 | text | 100% | 학자금 |
| `value5` | (한글) | amount | 100% |  |
| `기업식별번호` | 기업식별번호 | text | 100% | 2456-4520 |
| `value6` | (한글) | amount | 100% |  |
| `value7` | (영문) | amount | 100% |  |
| `customer.phone2` | 전화번호 | phone | 100% | 010-5907-7253 |
| `value8` | (은행명) | amount | 100% |  |
| `value9` | (계좌번호) | amount | 100% |  |
| `customer.name3` | 성명 | text | 100% | 박찬연 |
| `customer.phone3` | 전화번호 | phone | 100% | 010-5907-7253 |
| `팩스번호2` | 팩스번호 | phone | 100% | 043-783-2775 |
| `BicCode` | BicCode | text | 100% |  |
| `foreign.address` | 주소(영문) | text | 100% | 2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo… |
| `팩스번호3` | 팩스번호 | phone | 100% | 043-783-2775 |
| `customer.email3` | E-mail | text | 100% | wookyu882@nate.com |
| `신청인주소` | 신청인(업체)주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.name` | 업체명 | text | 100% | 주식회사 한빛패션 |

### 하나 입출금 거래내역 문자통지서비스 신청서 (`hf335`) — 키 43개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명(업체명) | text | 100% | 박찬연 |
| `check.신청구분` | 신청구분 | checkbox | 100% | 등록 |
| `customer.birth` | 생년월일(사업자등록번호) | date | 100% | 1990.02.10 |
| `check.이용료미납시문자통지` | 이용료미납시문자통지 | checkbox | 100% | 신청 |
| `통지대상계좌` | 통지대상계좌 | text | 100% | 982-904171-30859 |
| `이용료출금계좌` | 이용료출금계좌 | text | 100% | 522-910644-08875 |
| `check.요금제` | 요금제 | checkbox | 100% | 종량제(건당 20원 부과) |
| `check.통지대상거래유형` | 통지대상거래유형 | checkbox | 100% | 출금 |
| `check.통지대상거래금액` | 통지대상거래금액 | checkbox | 100% | 입금 ( |
| `check.통지범위` | 통지범위 | checkbox | 100% | 모든거래 |
| `check.통지시간` | 통지시간 | checkbox | 100% | 실시간 (즉시) |
| `check.심야자동이체통지시작시간` | 심야자동이체(C/C)통지시작시간 | checkbox | 100% | 실시간 (00시) |
| `check.계좌잔액` | 계좌잔액 | checkbox | 100% | 표시 |
| `check.통지언어` | 통지언어 | checkbox | 100% | 한글 |
| `문자통지대상휴대폰번호` | 문자통지대상휴대폰번호 | phone | 100% | 010-5907-7253 |
| `문자통지대상휴대폰번호2` | 문자통지대상휴대폰번호 | phone | 100% | 010-5907-7253 |
| `문자통지대상휴대폰번호3` | 문자통지대상휴대폰번호 | phone | 100% | 010-5907-7253 |
| `목록[].문자통지신청계좌2` | 문자통지신청계좌2 | text | 100% | 569-325353-61810 |
| `check.정액제` | 정액제(월800원) | checkbox | 100% | 정액제(월 800원) |
| `check.입금` | 입금 | checkbox | 100% | 출금 |
| `check.입금2` | 입금( | checkbox | 100% | 출금 ( |
| `check.모든거래` | 모든거래 | checkbox | 100% | 자동이체(C/C)제외 |
| `check[]` | 08:00~24:00(심야시간지연통지) | checkbox | 100% | 실시간 (즉시) |
| `check.지정시간` | 지정시간( | checkbox | 100% | 실시간 (00시) |
| `check.표시` | 표시 | checkbox | 100% | 미표시 |
| `check.한글` | 한글 | checkbox | 100% | 영어 |
| `목록[].문자통지신청계좌3` | 문자통지신청계좌3 | text | 100% | 866-401568-69437 |
| `check.정액제2` | 정액제(월800원) | checkbox | 100% | 종량제(건당 20원 부과) |
| `check.입금3` | 입금 | checkbox | 100% | 출금 |
| `check.입금4` | 입금( | checkbox | 100% | 출금 ( |
| `check.모든거래2` | 모든거래 | checkbox | 100% | 자동이체(C/C)제외 |
| `check.지정시간2` | 지정시간( | checkbox | 100% | 지정시간 ( |
| `check.표시2` | 표시 | checkbox | 100% | 미표시 |
| `check.한글2` | 한글 | checkbox | 100% | 한글 |
| `agent.relation` | 관계 | text | 100% | 부 |
| `agent.name` | 성명 | text | 100% | 박영준 |
| `agent.phone` | 연락처 | phone | 100% | 010-6515-4769 |
| `agent.birth` | 생년월일 | date | 100% | 1962.12.19 |
| `agent.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청및수령인 | text | 100% | 박찬연 |
| `seal.signer` | 신청및수령인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청및수령인 | signature | 100% | 강순준 |

### 개인 전자금융 서비스 신청서(영문) (`hf336`) — 키 40개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | Name | text | 100% | 박찬연 |
| `customer.address` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `EMail` | E-Mail | text | 100% |  |
| `UserID` | UserID | text | 100% | 750-938350-35687 |
| `customer.birth` | DateofBirth | date | 100% | 900210 |
| `HomePhone` | HomePhone | text | 100% |  |
| `GMgr` | GMgr | text | 100% |  |
| `Manager` | Manager | text | 100% |  |
| `Clerk` | Clerk | text | 100% |  |
| `목록[].BankName` | BankName | text | 100% |  |
| `목록[].AccountNo` | AccountNo. | text | 100% | 502-508432-80229 |
| `목록[].SpeedDialNumberforPhoneBanking` | SpeedDialNumberforPhoneBanking | text | 100% |  |
| `customer.name2` | Name | text | 100% | 박찬연 |
| `customer.birth2` | DateofBirth | date | 100% | 900210 |
| `Delegator` | Delegator | text | 100% |  |
| `ToHanaBank` | To:HanaBank | text | 100% |  |
| `BranchGeneralManager` | BranchGeneralManager | text | 100% |  |
| `OTPManufacturer` | ) OTP(Manufacturer | text | 100% |  |
| `Applicant` | Applicant | text | 100% | 가온푸드(주) |
| `KRW` | KRW), | text | 100% |  |
| `Category` | Category | text | 100% |  |
| `DesignateChange` |  Designate Change | text | 100% |  |
| `OtherRequests` | ■OtherRequests | text | 100% |  |
| `PowerofAttorney` | ■PowerofAttorney | text | 100% |  |
| `customer.name3` | Name | text | 100% | 박찬연 |
| `customer.address2` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `EMail2` | E-Mail | text | 100% |  |
| `UserID2` | UserID | text | 100% | 5181-4021 |
| `customer.birth3` | DateofBirth | date | 100% | 900210 |
| `HomePhone2` | HomePhone | text | 100% |  |
| `customer.name4` | Name | text | 100% | 박찬연 |
| `customer.birth4` | DateofBirth | date | 100% | 970514 |
| `Delegator2` | Delegator | text | 100% |  |
| `OTPManufacturer2` | ) OTP(Manufacturer | text | 100% |  |
| `Applicant2` | Applicant | text | 100% | (주)한빛테크 |
| `KRW2` | KRW), | text | 100% |  |
| `Category2` | Category | text | 100% |  |
| `DesignateChange2` |  Designate Change | text | 100% |  |
| `OtherRequests2` | ■OtherRequests | text | 100% |  |
| `PowerofAttorney2` | ■PowerofAttorney | text | 100% |  |

### 개인 전자금융 서비스 신청서 (`hf337`) — 키 48개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `EMail주소` | E-Mail주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `이용자ID` | 이용자ID | text | 100% | 367453-9750781 |
| `customer.birth` | 생년월일 | date | 100% | 900210 |
| `customer.home_phone` | 자택전화(직장전화) | phone | 100% | 02-2611-9326 |
| `customer.phone` | 휴대전화 | phone | 100% | 010-7321-8870 |
| `목록[].은행명` | 은행명 | text | 100% | 하나은행 |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 301-185399-67613 |
| `목록[].폰뱅킹단축번호` | 폰뱅킹단축번호 | text | 100% | 551-434959-92476 |
| `목록[].통장인감서명` | 통장인감/서명 | text | 100% |  |
| `agent.name` | 성명 | text | 100% | 박영준 |
| `계` | 계 | text | 100% |  |
| `명` | 명 | text | 100% |  |
| `소` | 소 | text | 100% |  |
| `customer.name2` | 위임인 | text | 100% | 박찬연 |
| `seal.signer` | 실명증표진위여부확인필 | seal | 100% | 박찬연 |
| `sign.signer` | 실명증표진위여부확인필 | signature | 100% | 현예지 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `지점장` | 지점장 | text | 100% | 범어지점 |
| `자물쇠카드일련번호` |  자물쇠카드(일련번호 | text | 100% | 600981-8157456 |
| `OTP제조업체` | ) OTP(제조업체 | text | 100% |  |
| `일련번호` | ,일련번호 | text | 100% | 5957-7430 |
| `customer.name3` | 신청인 | text | 100% | 박찬연 |
| `구분` | 구분 | text | 100% |  |
| `3시간지연4시간지연` |  3시간지연, 4시간지연 | text | 100% |  |
| `위임장` | ■위임장 | text | 100% |  |
| `실명확인증표사본` | 실명확인증표사본 | text | 100% |  |
| `customer.name4` | 성명 | text | 100% | 박찬연 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `EMail주소2` | E-Mail주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `이용자ID2` | 이용자ID | text | 100% | 160-203162-40366 |
| `customer.birth2` | 생년월일 | date | 100% | 900210 |
| `customer.home_phone2` | 자택전화(직장전화) | phone | 100% | 02-2611-9326 |
| `customer.phone2` | 휴대전화 | phone | 100% | 010-5907-7253 |
| `agent.name2` | 성명 | text | 100% | 박영준 |
| `계2` | 계 | text | 100% |  |
| `명2` | 명 | text | 100% |  |
| `소2` | 소 | text | 100% |  |
| `customer.name5` | 위임인 | text | 100% | 박찬연 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `자물쇠카드일련번호2` |  자물쇠카드(일련번호 | text | 100% | 947-274842-44589 |
| `OTP제조업체2` | ) OTP(제조업체 | text | 100% |  |
| `일련번호2` | ,일련번호 | text | 100% | 718-369474-91474 |
| `customer.name6` | 신청인 | text | 100% | 박찬연 |
| `구분2` | 구분 | text | 100% |  |
| `3시간지연4시간지연2` |  3시간지연, 4시간지연 | text | 100% |  |
| `위임장2` | ■위임장 | text | 100% |  |

### 기업 전자금융서비스 신청서(은행용)(영문) (`hf338`) — 키 43개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `Clerk` | Clerk | text | 100% |  |
| `Mgr` | Mgr | text | 100% |  |
| `GM` | GM | text | 100% |  |
| `NameCompanyName` | Name/CompanyName | text | 100% |  |
| `customer.address` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `OtherRequest` | OtherRequest | text | 100% |  |
| `BusinessRegistrationNo` | BusinessRegistrationNo. | biz_no | 100% | 264-82-36559 |
| `DailyKRW` | DailyKRW, | text | 100% |  |
| `KRW` | KRW | text | 100% |  |
| `OnetimeKRW` | One-timeKRW | text | 100% |  |
| `OnetimeKRW2` | One-timeKRW | text | 100% |  |
| `OnetimeKRW3` | One-timeKRW | text | 100% |  |
| `목록[].OverseasIPBlockingService` | OverseasIPBlockingService | text | 100% |  |
| `OTP` | OTP | text | 100% |  |
| `목록[].OfficeName` | OfficeName | text | 100% |  |
| `PhoneNoforIdentityVerification` | PhoneNo.forIdentityVerification | phone | 100% | 010-5907-7253 |
| `목록[].BusinessRegistrationNo` | BusinessRegistrationNo. | text | 100% | 264-82-36559 |
| `RequestNotRequest` | RequestNotRequest | text | 100% |  |
| `목록[].CorporateRegistrationNo` | CorporateRegistrationNo. | text | 100% | 283-639918-22868 |
| `PostpaidFee` | Post-paidFee | text | 100% |  |
| `RequestCancel` | Request(Account:)Cancel | text | 100% |  |
| `OtherChange` | OtherChange | text | 100% |  |
| `GeneralUser` | GeneralUser | text | 100% |  |
| `OTP2` | OTP | text | 100% |  |
| `UserCategory` | UserCategory | text | 100% |  |
| `RequestCancel2` | RequestCancel | text | 100% |  |
| `DailyKRW2` | DailyKRW | text | 100% |  |
| `OnetimeKRW4` | One-timeKRW | text | 100% |  |
| `WithdrawalAccount` | WithdrawalAccount | text | 100% |  |
| `WithdrawalAccount2` | WithdrawalAccount | text | 100% |  |
| `WithdrawalAccount_목록[].UserID` | UserID | text | 100% | 626676-0853919 |
| `DailyKRW3` | DailyKRW | text | 100% |  |
| `OnetimeKRW5` | One-timeKRW | text | 100% |  |
| `DesignationofBeneficiaryAccount` | DesignationofBeneficiaryAccount | text | 100% |  |
| `DesignationofBeneficiaryAccount2` | DesignationofBeneficiaryAccount | text | 100% |  |
| `DesignationofBeneficiaryAccount3` | DesignationofBeneficiaryAccount | text | 100% |  |
| `DesignationofBeneficiaryAccount4` | DesignationofBeneficiaryAccount | text | 100% |  |
| `customer.name` | Name | text | 100% | 박찬연 |
| `customer.address2` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `Relationship` | Relationship | text | 100% |  |
| `customer.birth` | DateofBirth | date | 100% | 970514 |
| `Delegator` | Delegator | text | 100% |  |
| `DoNOTAgree` | DoNOTAgree | text | 100% |  |

### 기업 전자금융서비스 신청서(은행용) (`hf340`) — 키 55개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `성명업체명` | 성명/업체명 | text | 100% | 주식회사 한빛패션 |
| `customer.address` | 주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `기타신청사항` | 기타신청사항 | text | 100% | 생활자금 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `customer.birth` | 생년월일(법인등록번호) | date | 100% | 1990.02.10 |
| `일원` | 일원, | text | 100% |  |
| `출금계좌지정` | 출금계좌지정(괄호는폰뱅킹단축번호***) | text | 100% | 953-334064-35410 |
| `기업뱅킹업체총이체한도` | 기업뱅킹업체총이체한도(1일) | number | 100% | 107,480,000 |
| `회원` | 회원 | text | 100% |  |
| `입금계좌지정신청신청안함_목록[].해외IP차단` | 해외IP차단 | text | 100% |  |
| `OTP` | OTP | text | 100% |  |
| `기업뱅킹본지사서비스신청해지_목록[].지사명` | 지사명 | text | 100% | (주)유니온무역 |
| `본인인증전화번호` | 본인인증전화번호 | phone | 100% | 010-5907-7253 |
| `기업뱅킹본지사서비스신청해지_목록[].사업자번호` | 사업자번호 | biz_no | 100% | 320-66-35976 |
| `신청미신청` | 신청미신청 | text | 100% |  |
| `기업뱅킹본지사서비스신청해지_목록[].법인등록번호` | 법인등록번호 | text | 100% | 579-385734-05328 |
| `수수료후취` | 수수료후취 | number | 100% | 960,000 |
| `신청해지` | 신청(계좌:)해지 | text | 100% |  |
| `signer.name` | 대표자 | text | 100% | 박찬연 |
| `seal.signer` | 대표자 | seal | 100% | 강순준 |
| `sign.signer` | 대표자 | signature | 100% | 박찬연 |
| `signer2.name` | 확인자명 | text | 100% | 박찬연 |
| `seal.signer2` | 확인자명 | seal | 100% | 박찬연 |
| `sign.signer2` | 확인자명 | signature | 100% | 현예지 |
| `signer3.name` | 대표자 | text | 100% | 박찬연 |
| `seal.signer3` | 대표자 | seal | 100% | 강순준 |
| `sign.signer3` | 대표자 | signature | 100% | 박찬연 |
| `signer4.name` | 확인자명 | text | 100% | 박찬연 |
| `seal.signer4` | 확인자명 | seal | 100% | 이욱유 |
| `sign.signer4` | 확인자명 | signature | 100% | 현예지 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer5.name` | 신청및수령인 | text | 100% | 박찬연 |
| `seal.signer5` | 신청및수령인 | seal | 100% | 이욱유 |
| `sign.signer5` | 신청및수령인 | signature | 100% | 박찬연 |
| `signer6.name` | 대리인 | text | 100% | 이욱유 |
| `seal.signer6` | 대리인 | seal | 100% | 이욱유 |
| `sign.signer6` | 대리인 | signature | 100% | 선영빈 |
| `signer7.name` | 대리인 | text | 100% | 이주원 |
| `seal.signer7` | 대리인 | seal | 100% | 김아진 |
| `sign.signer7` | 대리인 | signature | 100% | 이주원 |
| `OTP2` | OTP | text | 100% |  |
| `사용자구분` | 사용자구분 | text | 100% |  |
| `account` | 출금계좌 | account_no | 100% | 000-287736-52424 |
| `account2` | 출금계좌 | account_no | 100% | 000-287736-52424 |
| `출금계좌_목록[].대량이체한도iNetCMS에한함` | 대량이체한도iNet*CMS에한함 | number | 100% | 60,830,000 |
| `입금계좌지정` | 입금계좌지정 | text | 100% | 308-304997-01939 |
| `입금계좌지정2` | 입금계좌지정 | text | 100% | 631-969644-00203 |
| `입금계좌지정3` | 입금계좌지정 | text | 100% | 162-531619-47917 |
| `입금계좌지정4` | 입금계좌지정 | text | 100% | 280-421601-29917 |
| `agent.name` | 성명 | text | 100% | 박영준 |
| `agent.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `agent.relation` | 관계 | text | 100% | 부 |
| `agent.birth` | 생년월일 | date | 100% | 1962년 12월 19일 |
| `agent.name2` | 위임인 | text | 100% | 박영준 |
| `해지` | 해지 | text | 100% |  |

### 기업 전자금융서비스 신청확인서(고객용) (`hf341`) — 키 4개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `전국대표번호1599111115881111` | 전국대표번호|1599-1111,1588-1111 | text | 100% | 0499-6689 |
| `기업모바일뱅킹` | 기업모바일뱅킹 | text | 100% |  |
| `기업인터넷뱅킹` | 기업인터넷뱅킹 | text | 100% |  |
| `해외이용시82425202500` | 해외이용시|82-42-520-2500 | text | 100% |  |

### 해외은행 계좌정보 수신서비스(SWIFT MT940) 이용신청서 (`hf342`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 고객명 | text | 100% | 박찬연 |
| `이용자ID` | 이용자ID | text | 100% | 3984-4102 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `employer.address` | 회사주소 | text | 100% | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태… |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `담당자` | 담당자(직위/성명) | text | 100% | 이소빈 |
| `eMail주소` | e-Mail주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `통지은행명` | 통지은행명 | text | 100% | 신한은행 |
| `BankCode` | BankCode(BIC) | text | 100% |  |
| `통지계좌_목록[].통화` | 통화 | text | 100% | USD |
| `통지계좌_목록[].계좌번호` | 계좌번호 | text | 100% | 437-215076-16022 |
| `통지계좌_목록[].예금주` | 예금주 | text | 100% |  |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `seal.signer` | 거래인감 | seal | 100% | 현예지 |
| `sign.signer` | 거래인감 | signature | 100% | 이민빈 |
| `check.신청종류` | 신청종류 | checkbox | 100% | 해지 |
| `check.이용채널` | 이용채널 | checkbox | 100% | 기업뱅킹(통합CMS) |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 금융거래정보 이용제공 동의서(기업관계사서비스용)(영문) (`hf343`) — 키 4개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `HanaBank` | HanaBank | text | 100% |  |
| `HanaBank2` | HanaBank | text | 100% |  |
| `Emailaddresstobenotified` | E-mailaddresstobenotified | text | 100% |  |
| `BusinessRegistrationNo` | BusinessRegistrationNo. | biz_no | 100% | 533-50-23527 |

### 기업관계사 서비스 이용계약서(영문) (`hf344`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `Affiliate` | Affiliate | text | 100% |  |
| `Bank` | Bank | text | 100% |  |
| `company.name` | CompanyName | text | 100% | (주)유니온무역 |
| `customer.address` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `CEO` | CEO | text | 100% |  |
| `date` | Date | date | 100% | 2026년 01월 31일 |
| `company.name2` | CompanyName | text | 100% | (주)유니온무역 |
| `customer.address2` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `CEO2` | CEO | text | 100% |  |
| `date2` | Date | date | 100% | 2026년 01월 31일 |
| `customer.address3` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `GeneralManager` | GeneralManager | text | 100% |  |
| `date3` | Date | date | 100% | 2026년 01월 31일 |

### 금융거래정보 이용제공 동의서(기업관계사서비스용) (`hf345`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `주식회사하나은행` | 주식회사하나은행 | text | 100% | 하나은행 |
| `거래정보등을제공받을자` | 거래정보등을제공받을자(주계약사명) | text | 100% |  |
| `통지받을이메일주소` | 통지받을이메일주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 동의자(관계사)성명(사업자명) | text | 100% | 박찬연 |
| `seal.signer` | 동의자(관계사)성명(사업자명) | seal | 100% | 이욱유 |
| `sign.signer` | 동의자(관계사)성명(사업자명) | signature | 100% | 박찬연 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `등` | 등)(이하“거래정보”) | text | 100% |  |
| `계사서비스의이행` | 계사서비스의이행 | text | 100% |  |
| `관련서비스를제공받을수없게됨` | 관련서비스를제공받을수없게됨. | text | 100% |  |

### 기업관계사 서비스 이용신청서 (`hf346`) — 키 36개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.신청구분` | 신청구분 | checkbox | 100% | 변경 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `employer.name` | 회사명 | text | 100% | 주식회사 태평양무역 |
| `customer.address` | 주소 | text | 100% | 서울특별시 송파구 중대로 174, 119동 2202호 |
| `company.corp_no2` | 법인등록번호 | rrn | 100% | 200112-7448551 |
| `거래은행영업점` | 거래은행/영업점 | text | 100% | 우리은행 |
| `employer.name2` | 회사명 | text | 100% | 주식회사 태평양무역 |
| `customer.address2` | 주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `customer.email` | e-mail | text | 100% | chanyeon363@naver.com |
| `check.서비스종류` | 서비스종류 | checkbox | 100% | 국외관계사 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `company.biz_no2` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `글로벌고객번호` | 글로벌고객번호 | text | 100% | 241786-1027388 |
| `company.ceo2` | 대표자 | text | 100% | 박찬연 |
| `Fax` | Fax | text | 100% |  |
| `check.조회서비스` | 조회서비스(위임범위) | checkbox | 100% | 카드, |
| `check.아이디` | 아이디(ID) | checkbox | 100% | OTP |
| `check.아이디2` | 아이디(ID) | checkbox | 100% | 실행자 |
| `목록[].실행자ID` | 실행자ID* | text | 100% | 230-391859-29422 |
| `목록[].통화` | 통화 | text | 100% | AUD |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 790-526616-62979 |
| `목록[].인감서명` | 인감/서명 | text | 100% |  |
| `check.기업뱅킹` | 기업뱅킹(통합CMS) | checkbox | 100% | CMS Plus |
| `check.주계약사` | 주계약사 | checkbox | 100% | 관계사ID에 대한 동의 |
| `check.관계사` | 관계사 | checkbox | 100% | 관리대상 이용자에 대한 동의 |
| `agent.name` | 성명 | text | 100% | 박영준 |
| `agent.relation` | 관계 | text | 100% | 부 |
| `employer.name3` | 회사명 | text | 100% | 주식회사 태평양무역 |
| `agent.birth` | 생년월일 | date | 100% | 1967.09.21 |
| `agent.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.ceo3` | 대표자 | text | 100% | 강순준 |
| `check.본인은` | 본인은 | checkbox | 100% | OTP를 수령하고 “전자금융거래에 필요한 접근매체(OTP, 인증서 암호, |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `관계사업무위임및관계사ID에대한동의` | ■관계사업무위임및관계사ID에대한동의 | text | 100% |  |

### 기업관계사 서비스 이용계약서 (`hf347`) — 키 14개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `employer.name` | 회사명 | text | 100% | 주식회사 태평양무역 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer.name` | 대표이사 | text | 100% | 박찬연 |
| `seal.signer` | 대표이사 | seal | 100% | 강순준 |
| `sign.signer` | 대표이사 | signature | 100% | 박찬연 |
| `employer.name2` | 회사명 | text | 100% | 주식회사 태평양무역 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer2.name` | 대표이사 | text | 100% | 박찬연 |
| `seal.signer2` | 대표이사 | seal | 100% | 이민빈 |
| `sign.signer2` | 대표이사 | signature | 100% | 박찬연 |
| `customer.address3` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer3.name` | 대표이사 | text | 100% | 박찬연 |
| `seal.signer3` | 대표이사 | seal | 100% | 박찬연 |
| `sign.signer3` | 대표이사 | signature | 100% | 현예지 |

### 기업관계사 서비스 이용신청서(영문) (`hf348`) — 키 34개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.ApplicationType` | ApplicationType | checkbox | 100% | New |
| `CorporateRegistrationNo` | CorporateRegistrationNo. | text | 100% | 6236-1901 |
| `company.name` | CompanyName | text | 100% | (주)유니온무역 |
| `customer.address` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `CorporateRegistrationNo2` | CorporateRegistrationNo. | text | 100% | 4871-1290 |
| `BankBranch` | Bank/Branch | text | 100% |  |
| `company.name2` | CompanyName | text | 100% | (주)유니온무역 |
| `customer.address2` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `PhoneNo` | PhoneNo. | phone | 100% | 010-5907-7253 |
| `customer.email` | e-mail | text | 100% | chanyeon363@naver.com |
| `check.LocationofAffiliate` | LocationofAffiliate | checkbox | 100% | Outside Korea |
| `BusinessRegistrationNo` | BusinessRegistrationNo. | biz_no | 100% | 555-26-47276 |
| `Representative` | Representative | text | 100% |  |
| `BusinessRegistrationNo2` | BusinessRegistrationNo. | biz_no | 100% | 781-64-28453 |
| `GlobalClientNo` | GlobalClientNo. | text | 100% | 145454-9725355 |
| `Representative2` | Representative | text | 100% |  |
| `Fax` | Fax | text | 100% |  |
| `check.Entire` | Entire | checkbox | 100% | Entire |
| `check.ID` | ID | checkbox | 100% | Executor |
| `check.ID2` | ID | checkbox | 100% | OTP |
| `목록[].ExecutorID` | ExecutorID* | text | 100% | 375-802441-18876 |
| `목록[].Currency` | Currency | text | 100% | CNY |
| `목록[].AccountNo` | AccountNo. | text | 100% | 968262-6488276 |
| `목록[].RegisteredSealSign` | RegisteredSeal/Sign | text | 100% |  |
| `check.CorporateBan` | CorporateBanking(IntegratedCMS) | checkbox | 100% | CMSiNet |
| `check.PrincipalContractor` | PrincipalContractor | checkbox | 100% | Consent to the Affiliate’s Use of ID |
| `check.Affiliate` | Affiliate | checkbox | 100% | Consent to the Use of Accounts |
| `customer.name` | Name | text | 100% | 박찬연 |
| `customer.address3` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `Relationship` | Relationship | text | 100% |  |
| `company.name3` | CompanyName | text | 100% | (주)유니온무역 |
| `customer.birth` | DateofBirth | date | 100% | 1990.02.10 |
| `Delegator` | Delegator | text | 100% |  |
| `Representative3` | Representative | text | 100% |  |

### 펌뱅킹 출금전용계좌이용 동의서 (`hf349`) — 키 2개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.동의` | 동의 | checkbox | 100% | 동의 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 아이부자 걷기챌린지 서비스 동의서 (`hf350`) — 키 10개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `일반개인정보` | ■일반개인정보 | text | 100% |  |
| `걸음정보` | 걸음정보(걸음수) | text | 100% |  |
| `check.위개인정보수집이용에동의하십니까` | 위개인정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 박찬연 |
| `sign.signer` | 본인성명 | signature | 100% | 강순준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 강순준 |
| `seal.signer2` | 대리인성명 | seal | 100% | 강순준 |
| `sign.signer2` | 대리인성명 | signature | 100% | 김소윤 |

### 하나 sERP 상담신청서 (`hf352`) — 키 10개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `사업장전화번호` | 사업장전화번호 | phone | 100% | 010-5907-7253 |
| `company.address` | 사업장주소 | text | 100% | 서울특별시 중구 다산로 361, 6층 |
| `company.ceo` | 대표자명 | text | 100% | 박찬연 |
| `담당자명` | 담당자명 | text | 100% | 도숙경 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 이욱유 |

### CMS Plus 이용신청서(지사) (`hf353`) — 키 40개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.해외고객여부` | 해외고객여부 | checkbox | 100% | 아니오 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `사업자명` | 사업자명 | text | 100% | 다온무역(주) |
| `주소_목록[].대표자` | 대표자 | text | 100% |  |
| `check.대표연락처` | 대표연락처(선택또는전부기재) | checkbox | 100% | 전화번호 |
| `check.대표연락처2` | 대표연락처(선택또는전부기재) | checkbox | 100% | e-Mail |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `거래은행영업점` | 거래은행/영업점 | text | 100% | 농협은행 |
| `고객번호` | 고객번호 | text | 100% | 8878-0604 |
| `목록[].통화` | 통화 | text | 100% | AUD |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 835-724341-66029 |
| `목록[].예금주명` | 예금주명 | text | 100% |  |
| `목록[].인감서명` | 인감/서명 | text | 100% |  |
| `목록[].실행자아이디` | 실행자아이디(ID) | text | 100% |  |
| `목록[].개설점` | 개설점 | text | 100% | 범어지점 |
| `check.신청구분` | 신청구분 | checkbox | 100% | 변경 |
| `check.전체예금외환수출입대출` | 전체(예금,외환,수출입,대출,전자결제,카드,지로/공과금등 | checkbox | 100% | 전체 (예금, 외환, 수출입, 대출, 전자결제, 카드, 지로/공과금 등  |
| `check.부분` | 부분( | checkbox | 100% | 부분 ( |
| `check.신청일현재및미래에보유한` | 신청일현재및미래에보유한모든계좌에대하여조회허용 | checkbox | 100% | 신청일 현재 및 미래에 보유한 모든 계좌에 대하여 조회 허용 |
| `check.아래에서지정한계좌에대해` | 아래에서지정한계좌에대해서만조회허용 | checkbox | 100% | 아래에서 지정한 계좌에 대해서만 조회 허용 |
| `check.구분` | 구분 | checkbox | 100% | 실행자 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `개별1회` | 개별1회 | text | 100% |  |
| `개별1일` | 개별1일 | date | 100% | 2025년 8월 1일 |
| `대량1회` | 대량1회 | text | 100% |  |
| `대량1일` | 대량1일 | date | 100% | 2025-07-08 |
| `보안카드No` | 보안(OTP)카드No | text | 100% | 2154-7754 |
| `check.실행자` | 실행자 | checkbox | 100% | 실행자 |
| `목록[].value` | (영문+숫자혼합6~10자리) | amount | 100% |  |
| `이체한도_목록[].value` | (영문+숫자혼합6~10자리) | amount | 100% |  |
| `목록[].지사의실행자아이디` | 지사의실행자아이디(ID) | text | 100% |  |
| `목록[].통장인감` | 통장인감 | text | 100% |  |
| `등록일자` | 등록일자 | date | 100% | 2025-04-21 |
| `agent.name` | 성명 | text | 100% | 박영준 |
| `주소_목록[].생년월일` | 생년월일 | date | 100% | 2025.02.19 |
| `agent.relation` | 관계 | text | 100% | 부 |
| `주소_목록[].대표이사` | 대표이사 | text | 100% |  |
| `agent.birth` | 생년월일 | date | 100% | 1962년 12월 19일 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### CMS Plus 이용계약서 (`hf354`) — 키 20개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `기타` | 기타 | text | 100% | 해외 이주 |
| `설치장소` | 설치장소 | text | 100% |  |
| `Server` | Server | text | 100% |  |
| `PC` | PC | text | 100% |  |
| `모니터` | 모니터 | text | 100% |  |
| `목록[].명세` | 명세 | text | 100% |  |
| `HW_목록[].수량` | 수량 | number | 100% | 3 |
| `목록[].수량` | 수량 | number | 100% | 12 |
| `키보드마우스포함` | 키보드,마우스포함 | text | 100% |  |
| `목록[].키보드마우스포함` | 키보드,마우스포함 | text | 100% |  |
| `customer.name` | ,예금주 | text | 100% | 박찬연 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 대표이사 | text | 100% | 박찬연 |
| `seal.signer` | 대표이사 | seal | 100% | 강순준 |
| `sign.signer` | 대표이사 | signature | 100% | 박찬연 |
| `seal.signer2` | 지점장 | seal | 100% | 강순준 |
| `sign.signer2` | 지점장 | signature | 100% | 박찬연 |
| `employer.name` | 회사명 | text | 100% | 주식회사 태평양무역 |

### CMS Mega 이용계약서 (`hf355`) — 키 9개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 예금주 | text | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 대표이사 | text | 100% | 박찬연 |
| `seal.signer` | 대표이사 | seal | 100% | 박찬연 |
| `sign.signer` | 대표이사 | signature | 100% | 강순준 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `seal.signer2` | 지점장 | seal | 100% | 최우빈 |
| `sign.signer2` | 지점장 | signature | 100% | 강순준 |
| `customer.address2` | 주소 | text | 100% | 경기도 수원시 영통구 중부대로 379, 501호 |

### CMS Plus 이용신청서 (`hf356`) — 키 50개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `employer.name` | 회사명(대표자) | text | 100% | 주식회사 태평양무역 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |
| `주소_목록[].사업자등록번호` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 261-82-53694 |
| `check.이용Model` | 이용Model | checkbox | 100% | 인터넷 |
| `맞춤서비스_목록[].value` | (맞춤기능또는시스템연계내용) | amount | 100% |  |
| `check.전용선` | 전용선(VAN) | checkbox | 100% | 전용선(VAN) |
| `check.인터넷전용선` | 인터넷+전용선(VAN) | checkbox | 100% | 인터넷+전용선(VAN) |
| `check.인터넷` | 인터넷 | checkbox | 100% | 인터넷 |
| `check.전용선2` | 전용선(VAN) | checkbox | 100% | 전용선(VAN) |
| `check.인터넷전용선2` | 인터넷+전용선(VAN) | checkbox | 100% | 인터넷+전용선(VAN) |
| `check[]` | ₩300,000(매월) | checkbox | 100% | ₩300,000 (매월) |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.name` | 예금주 | text | 100% | 박찬연 |
| `seal.signer` | 거래인감(서명) | seal | 100% | 박찬연 |
| `sign.signer` | 거래인감(서명) | signature | 100% | 이민빈 |
| `관리점` | 관리점 | text | 100% |  |
| `check.신청구분` | 신청구분 | checkbox | 100% | 신규 |
| `check.구분` | 구분 | checkbox | 100% | 총괄관리자 |
| `customer.name2` | 성명 | text | 100% | 박찬연 |
| `부서직위` | 부서/직위 | text | 100% |  |
| `customer.phone2` | 연락처 | phone | 100% | 010-5907-7253 |
| `개별1회` | 개별1회 | text | 100% |  |
| `개별1일` | 개별1일 | date | 100% | 2025.06.20 |
| `대량1회` | 대량1회 | text | 100% |  |
| `대량1일` | 대량1일 | date | 100% | 2025.11.10 |
| `보안카드No` | 보안(OTP)카드No | text | 100% | 016-000399-57855 |
| `check.일반이용자` | 일반이용자 | checkbox | 100% | 실행자 |
| `목록[].value` | (영문+숫자혼합6~10자리) | amount | 100% |  |
| `이체한도_목록[].value` | (영문+숫자혼합6~10자리) | amount | 100% |  |
| `check.일반이용자2` | 일반이용자 | checkbox | 100% | 일반이용자 |
| `check.일반이용자3` | 일반이용자 | checkbox | 100% | 실행자 |
| `총괄관리자용` | 총괄관리자용 | text | 100% |  |
| `일반이용자용` | 일반이용자용 | text | 100% |  |
| `목록[].일련번호` | 일련번호(은행영업점직원이기입) | text | 100% | 5075-3361 |
| `목록[].실행자아이디` | 실행자아이디(ID) | text | 100% |  |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 444-172654-37394 |
| `목록[].통장인감` | 통장인감 | text | 100% |  |
| `목록[].개설점` | 개설점 | text | 100% | 범어지점 |
| `check.입금계좌` | 입금계좌( | checkbox | 100% | 지정 |
| `목록[].은행` | 은행 | text | 100% | 카카오뱅크 |
| `목록[].예금주` | 예금주 | text | 100% |  |
| `등록일자` | 등록일자 | date | 100% | 2024.10.10 |
| `agent.name` | 성명 | text | 100% | 박영준 |
| `주소_목록[].생년월일` | 생년월일 | date | 100% | 2025.02.25 |
| `agent.relation` | 관계 | text | 100% | 부 |
| `주소_목록[].대표이사` | 대표이사 | text | 100% |  |
| `agent.birth` | 생년월일 | date | 100% | 1962.12.19 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### CMSiNet 지사정보 등록신청서 (`hf357`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 160111-3910167 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 261-82-53694 |
| `check.하나해외지점법인주1고객` | 하나해외지점/법인주1)고객 | checkbox | 100% | 예 (아래내용 필수기입) |
| `사업자명` | 사업자명 | text | 100% | 주식회사 가온정밀 |
| `사업자대표` | 사업자대표 | text | 100% |  |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `팩스번호` | 팩스번호 | phone | 100% | 043-783-2775 |
| `customer.email` | e-mail | text | 100% | soonjun606@gmail.com |
| `목록[].실행자ID` | 실행자ID | text | 100% | 821077-3667101 |
| `목록[].통화` | 통화 | text | 100% | USD |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 372-346918-78328 |
| `목록[].예금주명` | 예금주명 | text | 100% |  |
| `목록[].인감서명` | 인감/서명 | text | 100% |  |
| `목록[].개설점` | 개설점 | text | 100% | 상무지점 |
| `check.아래의사업장을CMSiN` | 아래의사업장을CMSiNet지사로등록하여주시기바랍니다. | checkbox | 100% | 아래의 사업장을 CMS iNet 지사로 등록하여 주시기 바랍니다. |
| `check.지사출금계좌` | 지사출금계좌 | checkbox | 100% | 지사 출금계좌 |

### CMS Global 이용신청서 (`hf358`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.biz_no` | 사업자등록번호* | biz_no | 100% | 264-82-36559 |
| `employer.name` | 회사명(대표자)* | text | 100% | 주식회사 태평양무역 |
| `customer.address` | 주소* | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.address2` | 주소* | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `email주소` | e-mail주소* | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.name` | 예금주 | text | 100% | 박찬연 |
| `seal.signer` | 거래인감 | seal | 100% | 최우빈 |
| `sign.signer` | 거래인감 | signature | 100% | 강순준 |
| `口KRW100000` | 口KRW100,000(한국외국가1개)- | text | 100% |  |
| `口초과1개국가당KRW50000` | 口초과1개국가당KRW50,000- | text | 100% | 싱가포르 |
| `이용수수료1_목록[].조회집금서비스2신청국가` | 조회+집금서비스2)신청국가 | text | 100% | 독일 |
| `ID` | ID* | text | 100% | 044454-3828165 |
| `customer.name2` | 성명 | text | 100% | 박찬연 |
| `employer.position` | 직위 | text | 100% | 대리 |
| `employer.department` | 부서 | text | 100% | 구매팀 |
| `customer.phone` | 휴대폰 | phone | 100% | 010-7321-8870 |
| `직통전화` | 직통전화* | phone | 100% | 010-7321-8870 |
| `email주소2` | e-mail주소* | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.name3` | 신청인 | text | 100% | 박찬연 |

### 하나 sERP 이용신청서 (`hf359`) — 키 19개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.신청구분` | 신청구분 | checkbox | 100% | 변경 |
| `기업인터넷뱅킹ID` | 기업인터넷뱅킹ID | text | 100% | 4567-6991 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 261-82-53694 |
| `company.ceo` | 대표자명 | text | 100% | 강순준 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `담당자명` | 담당자명 | text | 100% | 나하정 |
| `담당부서연락처` | 담당부서연락처 | phone | 100% | 010-5907-7253 |
| `employer.name` | 회사명 | text | 100% | 주식회사 태평양무역 |
| `업태종목` | 업태/종목 | text | 100% |  |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `담당부서` | 담당부서 | text | 100% |  |
| `세금계산서교부용eMail` | 세금계산서교부용e-Mail | text | 100% |  |
| `account` | 출금계좌(하나은행) | account_no | 100% | 000-287736-52424 |
| `customer.name` | 예금주 | text | 100% | 박찬연 |
| `seal.signer` | 본인및인감확인 | seal | 100% | 현예지 |
| `sign.signer` | 본인및인감확인 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.name2` | 성명 | text | 100% | 박찬연 |
| `기타필요서류` | 기타필요서류 | text | 100% | 계좌 정리 |

### 개인(신용)정보 및 금융거래정보 제3자 제공동의서(모임통장서비스용) (`hf360`) — 키 7개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `일반개인정보` | └일반개인정보 | text | 100% |  |
| `check.위금융거래정보제공에동의하십니까` | 위금융거래정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인정보제공에동의하십니까` | 위개인(신용)정보제공에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 강순준 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |

### 자동화기기 이용(신규,해지,변경)신청서 (`hf362`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `이용계좌번호` | 이용계좌번호 | text | 100% | 467-770658-47293 |
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.phone` | 전화번호 | phone | 100% | 010-7321-8870 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 위나아 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |
| `signer2.name` | 대리인 | text | 100% | 이욱유 |
| `seal.signer2` | 대리인 | seal | 100% |  |
| `sign.signer2` | 대리인 | signature | 100% | 이욱유 |
| `customer.name2` | 성명 | text | 100% | 박찬연 |
| `이용계좌번호2` | 이용계좌번호 | text | 100% | 651-625529-39679 |
| `customer.birth2` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.phone2` | 전화번호 | phone | 100% | 010-5907-7253 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer3.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer3` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer3` | 신청인 | signature | 100% | 강순준 |
| `signer4.name` | 대리인 | text | 100% | 위나아 |
| `seal.signer4` | 대리인 | seal | 100% | 위나아 |
| `sign.signer4` | 대리인 | signature | 100% | 김도예 |

### 개인(신용)정보 수집이용 동의서[은행공동인증서비스(BankSign)] (`hf363`) — 키 17개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].수집이용목적` | 수집·이용목적 | text | 100% | 하나 적금 |
| `보유및이용기간` | 보유및이용기간 | text | 100% |  |
| `목록[].고유식별정보` | 고유식별정보 | text | 100% |  |
| `목록[].개인정보` | 개인(신용)정보 | text | 100% |  |
| `목록[].일반개인정보` | 일반개인정보 | text | 100% |  |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 현예지 |
| `sign.signer` | 본인성명 | signature | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 일 | text | 100% | 박찬연 |
| `seal.signer2` | 일 | seal | 100% | 박찬연 |
| `sign.signer2` | 일 | signature | 100% | 이욱유 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `위한인증처리` | 위한인증처리 | text | 100% |  |
| `불이익` | 불이익 | text | 100% |  |

### 개인(신용)정보 제3자 제공 동의서[은행공동인증서비스(BankSign)] (`hf364`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].제공받는자` | 제공받는자 | text | 100% |  |
| `목록[].이용목적` | 이용목적 | text | 100% | 하나 MMF |
| `보유및이용기간` | 보유및이용기간 | text | 100% |  |
| `고유식별정보` | 고유식별정보 | text | 100% |  |
| `일반개인정보` | 일반개인정보 | text | 100% |  |
| `개인정보` | 개인(신용)정보 | text | 100% |  |
| `check.위고유식별정보제공에동의하십니까` | 위고유식별정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `check.위개인신용정보제공에동의하십니까` | 위개인신용정보제공에동의하십니까? | checkbox | 100% | 동의함 |
| `signer.name` | 본인성명 | text | 100% | 박찬연 |
| `seal.signer` | 본인성명 | seal | 100% | 이욱유 |
| `sign.signer` | 본인성명 | signature | 100% | 현예지 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 대리인성명 | text | 100% | 이주원 |
| `seal.signer2` | 대리인성명 | seal | 100% | 이주원 |
| `sign.signer2` | 대리인성명 | signature | 100% |  |
| `불이익` | 불이익 | text | 100% |  |

### Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(영문) (`hf365`) — 키 29개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `PostalCode` | PostalCode* | text | 100% |  |
| `customer.address` | Address* | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `CorporateIdentificationNo` | CorporateIdentificationNo.* | text | 100% | 046203-2420310 |
| `BusinessRegistrationNo` | BusinessRegistrationNo.* | biz_no | 100% | 890-46-47269 |
| `value` | (Korean)* | amount | 100% |  |
| `value2` | (English)* | amount | 100% |  |
| `PostalCode2` | PostalCode* | text | 100% |  |
| `customer.address2` | Address* | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `PhoneNo` | PhoneNo.* | phone | 100% | 010-5907-7253 |
| `FaxNo` | FaxNo.* | text | 100% | 671-587902-20584 |
| `목록[].Currency` | Currency | text | 100% | USD |
| `목록[].AccountNo` | AccountNo.(AccountType) | text | 100% | 758176-2931373 |
| `목록[].AccountHolderName` | AccountHolderName | text | 100% |  |
| `목록[].SealSignature` | Seal/Signature | text | 100% |  |
| `check.Iherebywishto` | Iherebywishto | checkbox | 100% | Change/Add |
| `Representative` | Representative* | text | 100% |  |
| `customer.name` | Name* | text | 100% | 박찬연 |
| `customer.address3` | Address* | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.address4` | Address* | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `ResidentRegistrationNo` | ResidentRegistrationNo. | text | 100% | 565106-5565964 |
| `Relation` | Relation(Dept./Position) | text | 100% |  |
| `SignatureSeal` | Signature/Seal* | text | 100% |  |
| `SignatureSeal2` | Signature/Seal | text | 100% |  |
| `BankVerifiersNameSignature` | BankVerifier’sName/Signature* | text | 100% |  |
| `DateSubmitted` | DateSubmitted* | date | 100% | 2025.08.08 |
| `DateRegistered` | DateRegistered* | date | 100% | 2025.03.08 |
| `customer.address5` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `PROXY` | PROXY | text | 100% |  |
| `date` | Date | date | 100% | 2026년 01월 31일 |

### Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(국문) (`hf366`) — 키 37개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.corp_reg_no` | 법인등록번호* | corp_reg_no | 100% | 200112-7448551 |
| `customer.zipcode` | 우편번호* | number | 100% | 06931 |
| `customer.address` | 주소* | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.corp_no2` | 법인등록번호* | rrn | 100% | 200112-7448551 |
| `company.biz_no` | 사업자등록번호* | biz_no | 100% | 264-82-36559 |
| `value` | (국문)* | amount | 100% |  |
| `value2` | (영문)* | amount | 100% |  |
| `교육기관대표자` | 교육기관대표자* | text | 100% |  |
| `customer.zipcode2` | 우편번호* | number | 100% | 06931 |
| `customer.address2` | 주소* | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `customer.phone` | 전화번호* | phone | 100% | 010-3347-9183 |
| `팩스번호` | 팩스번호* | phone | 100% | 043-783-2775 |
| `목록[].통화` | 통화 | text | 100% | GBP |
| `목록[].계좌번호` | 계좌번호(계좌종류) | text | 100% | 639-806561-60946 |
| `목록[].예금주명` | 예금주명 | text | 100% |  |
| `목록[].인감서명` | 인감/서명 | text | 100% |  |
| `check.다음과같이` | 다음과같이 | checkbox | 100% | 해지 신청합니다. |
| `seal.signer` | 서명/인감* | seal | 100% | 강순준 |
| `sign.signer` | 서명/인감* | signature | 100% | 박찬연 |
| `customer.name` | 성명* | text | 100% | 박찬연 |
| `customer.address3` | 주소* | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `agent.name` | 성명* | text | 100% | 박영준 |
| `agent.address` | 주소* | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `agent.address2` | 주소* | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `agent.rrn` | 주민등록번호 | rrn | 100% | 621219-1****** |
| `agent.relation` | 관계(부서/직위)* | text | 100% | 부 |
| `seal.signer2` | 서명/인감* | seal | 100% | 강순준 |
| `sign.signer2` | 서명/인감* | signature | 100% | 박찬연 |
| `seal.signer3` | 서명/인감 | seal | 100% | 박찬연 |
| `sign.signer3` | 서명/인감 | signature | 100% | 현예지 |
| `seal.signer4` | 담당자성명/서명* | seal | 100% | 강순준 |
| `sign.signer4` | 담당자성명/서명* | signature | 100% | 박찬연 |
| `접수일자` | 접수일자* | date | 100% | 2025.03.05 |
| `등록일자` | 등록일자* | date | 100% | 2025.06.09 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `고객교육기관명` | “고객”교육기관명 | text | 100% | 카카오뱅크 |
| `customer.address4` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |

### Hana 1Q bank CMS iNet 서비스 이용 추가 계약서(iSBS) (`hf367`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `교육기관명` | 교육기관명 | text | 100% | 카카오뱅크 |
| `signer.name` | 대표자(학교장) | text | 100% | 박찬연 |
| `seal.signer` | 대표자(학교장) | seal | 100% | 강순준 |
| `sign.signer` | 대표자(학교장) | signature | 100% | 박찬연 |
| `signer2.name` | 지점장 | text | 100% | 박찬연 |
| `seal.signer2` | 지점장 | seal | 100% | 현예지 |
| `sign.signer2` | 지점장 | signature | 100% | 박찬연 |
| `고객` | “고객” | text | 100% |  |

### 가상계좌서비스 이용계약서(외화) (`hf368`) — 키 22개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `입금모계좌` | 입금모계좌 | text | 100% | 278-541555-90995 |
| `수수료인출계좌` | 수수료인출계좌 | number | 100% | 2,610,000 |
| `외화` | 외화 | amount | 100% | USD 131,600 |
| `원화` | 원화 | text | 100% |  |
| `목록[].예금주` | 예금주 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 대표이사 | text | 100% | 박찬연 |
| `seal.signer` | 대표이사 | seal | 100% | 박찬연 |
| `sign.signer` | 대표이사 | signature | 100% | 강순준 |
| `만원이상` | 만원이상 | number | 100% | 40,650,000 |
| `check.정산일` | 정산일 | checkbox | 100% | 입금후 |
| `check.정산방식` | 정산방식 | checkbox | 100% | 실시간 입금 |
| `영업일기준` | 영업일기준 | text | 100% |  |
| `check.예금주명표기방식` | 예금주명표기방식 | checkbox | 100% | 예금주명 +부기명 |
| `check.가상계좌재사용여부` | 가상계좌재사용여부 | checkbox | 100% | 재사용 |
| `check.가상계좌별입금횟수제한` | 가상계좌별입금횟수제한 | checkbox | 100% | 제한없음 |
| `사유` | 사유 | text | 100% | 만기 해지 |
| `부기명표기사유및부기명내용` | 부기명표기사유및부기명내용 | text | 100% | 본인 요청 |
| `가상계좌개설후최초입금시1회징구` | 가상계좌개설후최초입금시1회징구 | text | 100% | 420-346418-25580 |
| `가상계좌로입금거래발생시매회징구` | 가상계좌로입금거래발생시매회징구 | text | 100% | 411-024069-89447 |
| `신청좌수` | 신청좌수 | text | 100% |  |
| `동일가상계좌에입금가능한횟수를의미함` | 동일가상계좌에입금가능한횟수를의미함 | text | 100% | 231-121052-84569 |

### 가상계좌서비스 이용계약서(원화) (`hf369`) — 키 21개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `입금모계좌` | 입금모계좌 | text | 100% | 342-228530-85813 |
| `수수료인출계좌` | 수수료인출계좌 | number | 100% | 6,750,000 |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 538-483819-71934 |
| `목록[].예금주` | 예금주 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 대표이사 | text | 100% | 박찬연 |
| `seal.signer` | 대표이사 | seal | 100% | 박찬연 |
| `sign.signer` | 대표이사 | signature | 100% | 강순준 |
| `만원이상` | 만원이상 | number | 100% | 40,130,000 |
| `check.정산일` | 정산일 | checkbox | 100% | 입금당일정산 |
| `check.정산방식` | 정산방식 | checkbox | 100% | 실시간 입금 |
| `영업일기준` | 영업일기준 | text | 100% |  |
| `check.예금주명표기방식` | 예금주명표기방식 | checkbox | 100% | 예금주명 +부기명 |
| `check.가상계좌재사용여부` | 가상계좌재사용여부 | checkbox | 100% | 회만 사용 |
| `check.가상계좌별입금횟수제한` | 가상계좌별입금횟수제한 | checkbox | 100% | 제한없음 |
| `사유` | 사유 | text | 100% | 사업자금 |
| `부기명표기사유및부기명내용` | 부기명표기사유및부기명내용 | text | 100% |  |
| `가상계좌개설후최초입금시1회징구` | 가상계좌개설후최초입금시1회징구 | text | 100% | 845-961652-88507 |
| `가상계좌로입금거래발생시매회징구` | 가상계좌로입금거래발생시매회징구 | text | 100% | 489-075607-35335 |
| `신청좌수` | 신청좌수 | text | 100% |  |
| `동일가상계좌에입금가능한횟수를의미함` | 동일가상계좌에입금가능한횟수를의미함 | text | 100% | 805-363222-57515 |

### 전산기기 임대차계약서(Hana 1Q bank CMS) (`hf372`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `기타` | 기타 | text | 100% | 생활자금 |
| `설치장소` | 설치장소 | text | 100% |  |
| `Server` | Server | text | 100% |  |
| `PC` | PC | text | 100% |  |
| `모니터` | 모니터 | text | 100% |  |
| `목록[].명세` | 명세 | text | 100% |  |
| `HW_목록[].수량` | 수량 | number | 100% | 60 |
| `목록[].수량` | 수량 | number | 100% | 3 |
| `키보드마우스포함` | 키보드,마우스포함 | text | 100% |  |
| `목록[].키보드마우스포함` | 키보드,마우스포함 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.address` | (고객)주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer.name` | 대표이사 | text | 100% | 박찬연 |
| `seal.signer` | 대표이사 | seal | 100% | 박찬연 |
| `sign.signer` | 대표이사 | signature | 100% | 강순준 |
| `customer.address2` | (은행)주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `seal.signer2` | 지점장 | seal | 100% | 강순준 |
| `sign.signer2` | 지점장 | signature | 100% | 박찬연 |

### 전자어음 교부 신청서 (`hf373`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 법인명(성명) | text | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자등록번호(법인) | biz_no | 100% | 264-82-36559 |
| `당좌계좌번호` | 당좌계좌번호 | text | 100% | 358-011745-84676 |
| `교부신청매수` | 교부신청매수 | number | 100% | 1 |
| `company.ceo` | 대표자명 | text | 100% | 강순준 |
| `customer.birth` | 생년월일(개인/개인사업자) | date | 100% | 1990년 2월 10일 |
| `회수신청매수` | 회수신청매수 | number | 100% | 2 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 강순준 |
| `sign.signer` | 신청인 | signature | 100% | 현예지 |

### 전자어음 이용(변경,해지) 신청서 (`hf374`) — 키 30개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.거래구분` | 거래구분 | checkbox | 100% | 발행해지 |
| `check.회원구분` | 회원구분 | checkbox | 100% | 발행인(수취,배서포함) |
| `company.name` | 법인명(성명) | text | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자등록번호(법인) | biz_no | 100% | 264-82-36559 |
| `check.규모` | 규모 | checkbox | 100% | 중소기업 |
| `담당부서` | 담당부서 | text | 100% |  |
| `employer.phone` | 회사전화 | phone | 100% | 043-783-2775 |
| `FAX` | FAX | phone | 100% | 043-783-2775 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `대표전화` | 대표전화 | phone | 100% | 010-5907-7253 |
| `customer.phone` | 휴대폰 | phone | 100% | 010-5907-7253 |
| `EMail` | E-Mail | text | 100% |  |
| `발행지정계좌` | 발행(당좌)지정계좌 | text | 100% | 103-165676-74864 |
| `수취지정계좌` | 수취(요구불)지정계좌 | text | 100% | 095-020779-84508 |
| `seal.signer` | 거래인감 | seal | 100% | 박찬연 |
| `sign.signer` | 거래인감 | signature | 100% | 위나아 |
| `seal.signer2` | 거래인감 | seal | 100% | 현예지 |
| `sign.signer2` | 거래인감 | signature | 100% | 강순준 |
| `value` | [변경전] | amount | 100% |  |
| `변경항목` | 변경항목 | text | 100% |  |
| `value2` | [변경후] | amount | 100% |  |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer3.name` | 신청인(대리인) | text | 100% | 박찬연 |
| `seal.signer3` | 신청인(대리인) | seal | 100% | 최우빈 |
| `sign.signer3` | 신청인(대리인) | signature | 100% | 박찬연 |
| `징구서류` | •징구서류 | text | 100% |  |
| `자택` | 자택()- | text | 100% |  |
| `휴대폰` | 휴대폰()- | phone | 100% | 010-7321-8870 |

### 자금관리서비스 이용계약서 (`hf375`) — 키 9개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.phone` | 휴대폰 | phone | 100% | 010-5907-7253 |
| `직위성명` | 직위/성명 | text | 100% | 김정현 |
| `employer.address` | 회사주소 | text | 100% | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태… |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 대표이사 | text | 100% | 박찬연 |
| `seal.signer` | 대표이사 | seal | 100% | 강순준 |
| `sign.signer` | 대표이사 | signature | 100% | 박찬연 |
| `seal.signer2` | 지점장 | seal | 100% | 강순준 |
| `sign.signer2` | 지점장 | signature | 100% | 박찬연 |

### 위임장(해외체류자 전자금융용) (`hf376`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `agent.name` | 성명 | text | 100% | 박영준 |
| `agent.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `agent.birth` | 생년월일 | date | 100% | 1962.12.19 |
| `agent.relation` | 본인과의관계 | text | 100% | 부 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 명: | text | 100% | 박찬연 |
| `seal.signer` | 명: | seal | 100% | 박찬연 |
| `sign.signer` | 명: | signature | 100% | 이욱유 |
| `해외영업점` | 해외영업점 | text | 100% | 범어지점 |
| `signer2.name` | 확인자 | text | 100% | 박찬연 |
| `seal.signer2` | 확인자 | seal | 100% | 강순준 |
| `sign.signer2` | 확인자 | signature | 100% | 현예지 |
| `비밀번호재등록` | 비밀번호재등록 | text | 100% | 284074-1299093 |
| `보안매체재발급` | 보안매체재발급(OTP/자물쇠카드) | text | 100% |  |
| `employer.position` | 직위 | text | 100% | 대리 |

### 해외영업점 계좌개설 신청서 (`hf377`) — 키 29개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `담당Prepare` | 담당Prepare | text | 100% |  |
| `책임자Approval` | 책임자Approval | text | 100% |  |
| `성명Name` | 성명Name | text | 100% | 박찬연 |
| `성명Name2` | 성명Name | text | 100% | 조희원 |
| `customer.birth` | 생년월일DateofBirth | date | 100% | 1990.02.10 |
| `여권번호PassportNo` | 여권번호PassportNo. | text | 100% | M90428366 |
| `국내주소DomesticAddress_목록[].여권유효기일DateofExpiry` | 여권유효기일DateofExpiry | text | 100% | 2026년 7월 30일 |
| `국내주소DomesticAddress` | 국내주소DomesticAddress | text | 100% | 서울특별시 송파구 중대로 174, 119동 2202호 |
| `해외주소OverseasAddress_목록[].여권유효기일DateofExpiry` | 여권유효기일DateofExpiry | text | 100% | 2029.03.17 |
| `국적Nationality` | 국적Nationality | text | 100% |  |
| `여권유효기일DateofExpiry` | 여권유효기일DateofExpiry | date | 100% | 2028.03.31 |
| `개설신청은행지점명OpeningBankBranch` | 개설신청은행/지점명OpeningBank/Branch | text | 100% | 기업은행 |
| `개설통화Currency` | 개설통화Currency | text | 100% | GBP |
| `접수은행지점명BankBranch` | 접수은행/지점명Bank/Branch | text | 100% | 신한은행 |
| `customer.name` | 고객명(Name) | text | 100% | 박찬연 |
| `제출서류` | 제출서류(Document) | text | 100% |  |
| `account` | 계좌번호(A/CNo.) | account_no | 100% | 000-287736-52424 |
| `check.신청` | 신청(Application) | checkbox | 100% | 신청(Application) |
| `check.본인은위와같이예금계좌개` | 본인은위와같이예금계좌개설/취소를신청합니다. | checkbox | 100% | 본인은 위와 같이 예금계좌 개설/취소를 신청합니다. |
| `check.현지국의법규및규제사항거` | 현지국의법규및규제사항,거래약관에따라신청자앞예금계좌가개설되 | checkbox | 100% | 현지국의 법규 및 규제사항, 거래약관에 따라 신청자 앞 예금계좌가 개설되 |
| `date` | 신청일자(Date) | date | 100% | 2026.01.31 |
| `signer.name` | 담당자(직,성명) | text | 100% | 박찬연 |
| `seal.signer` | 담당자(직,성명) | seal | 100% | 박찬연 |
| `sign.signer` | 담당자(직,성명) | signature | 100% | 강순준 |
| `seal.signer2` | 지점장 | seal | 100% | 이민빈 |
| `sign.signer2` | 지점장 | signature | 100% | 박찬연 |
| `signer3.name` | 담당자(직,성명) | text | 100% | 박찬연 |
| `seal.signer3` | 담당자(직,성명) | seal | 100% | 박찬연 |
| `sign.signer3` | 담당자(직,성명) | signature | 100% | 강순준 |

### 글로벌뱅킹서비스 이용,변경,해지 신청서 (`hf378`) — 키 25개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `담당Prepare` | 담당Prepare | text | 100% |  |
| `책임자Approval` | 책임자Approval | text | 100% |  |
| `성명Name` | 성명Name | text | 100% | 박찬연 |
| `성명Name2` | 성명Name | text | 100% | 안은혜 |
| `customer.birth` | 생년월일DateofBirth | date | 100% | 1990.02.10 |
| `해외주소OverseasAddress_목록[].직장Company` | 직장Company | text | 100% |  |
| `자택House_목록[].여권번호PassportNo` | 여권번호PassportNo. | text | 100% | M86917012 |
| `직장Company_목록[].여권번호PassportNo` | 여권번호PassportNo. | text | 100% | M36773767 |
| `여권번호PassportNo` | 여권번호PassportNo. | text | 100% | M66521053 |
| `인터넷뱅킹이용자IDInternetBankingUserID` | 인터넷뱅킹이용자IDInternetBankingUserID | text | 100% | 8408-2334 |
| `서비스이용계좌번호ACNo` | 서비스이용계좌번호A/CNo. | text | 100% | 370-850247-96433 |
| `개설은행지점명BankBranch` | 개설은행/지점명Bank/Branch | text | 100% | 우리은행 |
| `seal.signer` | 서명/인감Signature | seal | 100% | 현예지 |
| `sign.signer` | 서명/인감Signature | signature | 100% | 박찬연 |
| `직장Company` | 직장Company | text | 100% |  |
| `eMail` | e-Mail | text | 100% |  |
| `signer2.name` | 실명확인자 | text | 100% | 박찬연 |
| `seal.signer2` | 실명확인자 | seal | 100% | 강순준 |
| `sign.signer2` | 실명확인자 | signature | 100% | 박찬연 |
| `조회` | ‌조회 | text | 100% |  |
| `조회2` | ‌조회 | text | 100% |  |
| `조회3` | ‌조회 | text | 100% |  |
| `Inquiry` | Inquiry | text | 100% |  |
| `Inquiry2` | Inquiry | text | 100% |  |
| `Inquiry3` | Inquiry | text | 100% |  |

### 주류구매전용카드 가맹점가입신청서 (`hf379`) — 키 28개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 상호 | text | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 261-82-53694 |
| `check.주소` | 주소 | checkbox | 100% | 보기2 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.name2` | 예금주 | text | 100% | 박찬연 |
| `company.established` | 개업일 | date | 100% | 2022.05.19 |
| `자본금` | 자본금 | text | 100% |  |
| `company.biz_item` | 업종 | text | 100% | 무역 |
| `매출액` | 매출액 | number | 100% | 6,540,000 |
| `취급품목` | 취급품목 | text | 100% | 커피 원두 |
| `종업원수` | 종업원수 | text | 100% |  |
| `check.사업체구분` | 사업체구분 | checkbox | 100% | 수입 |
| `employer.name` | 소속 | text | 100% | 주식회사 태평양무역 |
| `employer.name2` | 소속 | text | 100% | 주식회사 태평양무역 |
| `customer.name3` | 성명 | text | 100% | 박찬연 |
| `customer.name4` | 성명 | text | 100% | 박찬연 |
| `check.주류구매전용카드가맹점가입신청서` | 주류구매전용카드가맹점가입신청서( | checkbox | 100% | (주)엔젤넷) |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인(상호) | text | 100% | 박찬연 |
| `seal.signer` | 신청인(상호) | seal | 100% | 박찬연 |
| `sign.signer` | 신청인(상호) | signature | 100% | 강순준 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 가맹점신청인 | text | 100% | 박찬연 |
| `seal.signer2` | 가맹점신청인 | seal | 100% | 강순준 |
| `sign.signer2` | 가맹점신청인 | signature | 100% | 이민빈 |
| `seal.signer3` | 지점장 | seal | 100% | 이욱유 |
| `sign.signer3` | 지점장 | signature | 100% | 박찬연 |

### 금융결제원CMS 이용계약서 (`hf380`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `출금이체` | 출금이체 | text | 100% |  |
| `입금이체` | 입금이체 | text | 100% |  |
| `목록[].예금주명` | 예금주명 | text | 100% |  |
| `원` | 원 | text | 100% |  |
| `이체건당` | 이체건당 | text | 100% |  |
| `원2` | 원 | text | 100% |  |
| `원3` | 원 | text | 100% |  |
| `원4` | 원 | text | 100% |  |
| `계약지점코드` | 계약지점코드 | number | 100% | 702947 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `signer.name` | 지점장 | text | 100% | 박찬연 |
| `seal.signer` | 지점장 | seal | 100% | 강순준 |
| `sign.signer` | 지점장 | signature | 100% | 박찬연 |
| `signer2.name` | 대표자 | text | 100% | 박찬연 |
| `seal.signer2` | 대표자 | seal | 100% | 강순준 |
| `sign.signer2` | 대표자 | signature | 100% | 박찬연 |

### 퇴직연금 퇴직급여 지급신청서(DC,기업형IRP) (`hf164`) — 키 51개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `employer.hire_date` | 입사일자 | date | 100% | 2020.05.08 |
| `account` | 퇴직연금계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.birth` | 생년월일 | date | 100% | 900210 |
| `중간정산일자` | 중간정산일자 | date | 100% | 2026-01-17 |
| `check.제도구분` | 제도구분 | checkbox | 100% | 기업형IRP |
| `check.임원여부` | 임원여부 | checkbox | 100% | 근로자 |
| `퇴직급여입금총액` | 퇴직급여입금총액* | number | 100% | 9,310,000원 |
| `퇴직일자` | 퇴직일자 | date | 100% | 2025.10.19 |
| `check.지급형태` | 지급형태 | checkbox | 100% | 개인형IRP(의무) |
| `check.지급형태2` | 지급형태 | checkbox | 100% | 입출금계좌 |
| `check.잔여부담금` | 잔여부담금*** | checkbox | 100% | 없음 |
| `check.잔여부담금2` | 잔여부담금*** | checkbox | 100% | 있음 (금액 |
| `check.기업반환신청` | 기업반환신청***** | checkbox | 100% | 국민연금 전환금 |
| `check.현물이전` | 현물이전** | checkbox | 100% | 미신청 (보유상품 ‘해지 후’ IRP로 이전 (특별중도해지이율 적용)) |
| `check.예외사유` | 예외사유 | checkbox | 100% | 만원이하 퇴직금 지급 |
| `check.연동출금신청` | 연동출금신청(사전에약정된경우) | checkbox | 100% | 미신청(기업별도입금) |
| `예약지급일` | 예약지급일* | date | 100% | 2025.03.05 |
| `check.당해연도이전에중간정산한금액이있는경우` | 당해연도이전에중간정산(중도인출)한금액이있는경우 | checkbox | 100% | 해당사항 없음 |
| `check.해당사항없음` | 해당사항없음 | checkbox | 100% | 해당사항 없음 |
| `금융기관명` | 금융기관명 | text | 100% | 우리은행 |
| `금융기관명2` | 금융기관명 | text | 100% | 기업은행 |
| `account2` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `account3` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.퇴직소득세계산을위한근속연수산정시제외가산월수있는경우기재` | 퇴직소득세계산을위한근속연수산정시제외·가산월수있는경우기재 | checkbox | 100% | 제외월수( |
| `check.개인적립금과세제외신청` | 개인적립금과세제외신청 | checkbox | 100% | 과세제외 미신청 |
| `check.가입자단독청구` | 가입자단독청구 | checkbox | 100% | 기타 (사용자 지급거절 등) |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer` | 가입자 | seal | 100% | 현예지 |
| `sign.signer` | 가입자 | signature | 100% | 강순준 |
| `signer2.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer2` | 가입자 | seal | 100% | 강순준 |
| `sign.signer2` | 가입자 | signature | 100% | 박찬연 |
| `signer3.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer3` | 기업명 | seal | 100% | 강순준 |
| `sign.signer3` | 기업명 | signature | 100% | 박찬연 |
| `signer4.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer4` | 가입자 | seal | 100% | 현예지 |
| `sign.signer4` | 가입자 | signature | 100% | 박찬연 |
| `타금융기관IRP통장사본` | 타금융기관IRP통장사본(가입확인서) | text | 100% | 우리은행 |
| `퇴직금전환금부과내역서` | 퇴직금전환금부과내역서(국민연금공단발급) | text | 100% |  |
| `연금보험료등소득세액공제확인서` | 연금보험료등소득☞세액공제확인서 | number | 100% | 70,000 |
| `signer5.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer5` | 가입자 | seal | 100% | 강순준 |
| `sign.signer5` | 가입자 | signature | 100% | 현예지 |
| `signer6.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer6` | 가입자 | seal | 100% | 강순준 |
| `sign.signer6` | 가입자 | signature | 100% | 박찬연 |
| `아래양식중한가지` | 아래양식중한가지 | text | 100% |  |

### 퇴직연금 계약이전신청서(DB) (`hf165`) — 키 54개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `예약지급일` | 예약지급일 | date | 100% | 2024-10-14 |
| `account` | 퇴직연금계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.전부이전` | 전부이전 | checkbox | 100% | 전부이전 |
| `이전구분` | 이전구분 | text | 100% |  |
| `check.일부이전` | 일부이전 | checkbox | 100% | 일부이전 |
| `check.금액이전` | 금액이전 | checkbox | 100% | 금액이전 |
| `check.퇴직연금사업자변경` | 퇴직연금사업자변경 | checkbox | 100% | 퇴직연금 사업자 변경 |
| `check.계열사이전` | 계열사이전(과거입사일인정) | checkbox | 100% | 계열사이전(과거입사일 인정) |
| `이전사유` | 이전사유 | text | 100% | 해외 이주 |
| `check.퇴직연금사업자변경2` | 퇴직연금사업자변경 | checkbox | 100% | 계열사이전(과거입사일 인정) |
| `check.퇴직연금사업자변경3` | 퇴직연금사업자변경 | checkbox | 100% | 퇴직연금 사업자 변경 |
| `이전받는금융기관` | 이전받는금융기관 | text | 100% | 신한은행 |
| `자산관리기관` | 자산관리기관 | text | 100% | 농협은행 |
| `이전방식` | 이전방식 | text | 100% |  |
| `현물이전` | 현물이전* | text | 100% |  |
| `check.금액지정방식` | 금액지정방식 | checkbox | 100% | 상품지정방식(뒷장 필수 기재) |
| `금융기관명` | 금융기관명 | text | 100% | 카카오뱅크 |
| `foreign.account` | 계좌번호 | account_no | 100% | 884779361534 |
| `foreign.name` | 예금주 | text | 100% | Tokyo Seimitsu Kogyo K.K. |
| `check.현물이전` | 현물이전* | checkbox | 100% | 신청(보유상품 ‘해지 없이’ 이전) |
| `check.현물이전2` | 현물이전* | checkbox | 100% | 미신청(보유상품 ‘해지 후’ 이전) |
| `목록[].가입자명` | 가입자명* | text | 100% |  |
| `목록[].생년월일` | 생년월일(주민번호) | text | 100% | 2024.10.29 |
| `목록[].제도전환전출일자` | 제도전환/전출일자 | text | 100% | 2024.11.11 |
| `signer.name` | 제도전환/전출일자 | text | 100% | 박찬연 |
| `seal.signer` | 제도전환/전출일자 | seal | 100% | 박찬연 |
| `sign.signer` | 제도전환/전출일자 | signature | 100% | 현예지 |
| `목록[].서명또는` | 서명또는(인) | text | 100% |  |
| `목록[].지급요청금액` | 지급요청금액 | text | 100% | 49,220,000 |
| `목록[].매도순위` | 매도순위 | text | 100% |  |
| `목록[].상품명` | 상품명 | text | 100% | 플라스틱 원료 |
| `목록[].상품계좌번호` | 상품계좌번호 | text | 100% | 971-723674-58860 |
| `목록[].매도금액` | 매도금액(원/좌) | text | 100% | 8,720,000 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `매도상품_목록[].상품명` | 상품명 | text | 100% | 자동차 부품 |
| `입금비율` | 입금비율* | number | 100% | 100 |
| `금융기관명2` | 금융기관명 | text | 100% | 농협은행 |
| `foreign.account2` | 계좌번호 | account_no | 100% | 870195264202 |
| `foreign.name2` | 예금주 | text | 100% | Mekong Garment JSC |
| `매도상품_목록[].상품계좌번호` | 상품계좌번호 | text | 100% | 739-375338-44145 |
| `이전받는금융기관_목록[].상품계좌번호` | 상품계좌번호 | text | 100% | 800-233826-96382 |
| `매도상품_목록[].만기일` | 만기일 | text | 100% | 2028-12-17 |
| `이전받는금융기관_목록[].만기일` | 만기일 | text | 100% | 2026.10.21 |
| `signer2.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer2` | 기업명 | seal | 100% | 강순준 |
| `sign.signer2` | 기업명 | signature | 100% | 박찬연 |
| `signer3.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer3` | 기업명 | seal | 100% | 이민빈 |
| `sign.signer3` | 기업명 | signature | 100% | 박찬연 |
| `signer4.name` | 신탁관리인 | text | 100% | 박찬연 |
| `seal.signer4` | 신탁관리인 | seal | 100% | 박찬연 |
| `sign.signer4` | 신탁관리인 | signature | 100% | 강순준 |
| `value` | [유의사항] | amount | 100% |  |

### 퇴직연금 계약이전신청서(DC) (`hf166`) — 키 39개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `서류확인및접수확인자` | 서류확인및접수확인자 | text | 100% |  |
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `예약지급일` | 예약지급일* | date | 100% | 2025-01-13 |
| `account` | 퇴직연금계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.수수료연동출금` | 수수료연동출금 | checkbox | 100% | 동의 (사전에 약정된 경우) |
| `check.퇴직연금사업자변경` | 퇴직연금사업자변경 | checkbox | 100% | 계열사이전(과거입사일 인정) |
| `이전받는금융기관` | 이전받는금융기관 | text | 100% | 카카오뱅크 |
| `자산관리기관` | 자산관리기관 | text | 100% | 우리은행 |
| `check.일부이전` | 일부이전(현물이전은3번항목에서개별신청) | checkbox | 100% | 일부이전(현물이전은 3번 항목에서 개별 신청) |
| `check.전부이전` | 전부이전 | checkbox | 100% | 전부이전 |
| `금융기관` | 금융기관 | text | 100% | 국민은행 |
| `foreign.account` | 계좌번호 | account_no | 100% | 884779361534 |
| `foreign.name` | 예금주 | text | 100% | Mekong Garment JSC |
| `check.현물이전` | 현물이전** | checkbox | 100% | 신청(보유상품 ‘해지 없이’ 이전) |
| `check.현물이전2` | 현물이전** | checkbox | 100% | 미신청(보유상품 ‘해지 후’ 이전) |
| `목록[].가입자성명` | 가입자성명 | text | 100% | 박찬연 |
| `signer.name` | 가입자성명 | text | 100% | 박찬연 |
| `seal.signer` | 가입자성명 | seal | 100% | 박찬연 |
| `sign.signer` | 가입자성명 | signature | 100% | 강순준 |
| `목록[].서명또는` | 서명또는(인) | text | 100% |  |
| `목록[].생년월일` | 생년월일(주민번호) | text | 100% | 2026.01.31 |
| `목록[].제도전환전출일자` | 제도전환/전출일자 | text | 100% | 2025.07.12 |
| `check.미신청` | 미신청 | checkbox | 100% | 미신청 |
| `check.미신청2` | 미신청 | checkbox | 100% | 신청 |
| `check.미신청3` | 미신청 | checkbox | 100% | 신청 |
| `check.미신청4` | 미신청 | checkbox | 100% | 신청 |
| `check.미신청5` | 미신청 | checkbox | 100% | 신청 |
| `check.미신청6` | 미신청 | checkbox | 100% | 미신청 |
| `check.미신청7` | 미신청 | checkbox | 100% | 신청 |
| `목록[].현물이전유의사항확인` | 현물이전유의사항확인 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer2` | 기업명 | seal | 100% | 강순준 |
| `sign.signer2` | 기업명 | signature | 100% | 박찬연 |
| `signer3.name` | 신탁관리인 | text | 100% | 박찬연 |
| `seal.signer3` | 신탁관리인 | seal | 100% | 강순준 |
| `sign.signer3` | 신탁관리인 | signature | 100% | 박찬연 |
| `seal.signer4` | 이전받는기업의법인인감증명서징구 | seal | 100% | 강순준 |
| `sign.signer4` | 이전받는기업의법인인감증명서징구 | signature | 100% | 박찬연 |

### 퇴직연금 사전지정운용제도 신청서(디폴트옵션, 기업용) (`hf167`) — 키 9개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `check.등록구분` | 등록구분 | checkbox | 100% | 변경 |
| `company.biz_no` | 사업자번호 | biz_no | 100% | 264-82-36559 |
| `check.일괄선택` | 일괄선택 | checkbox | 100% | 전체 상품 일괄 선택 |
| `check.체크` | 체크 | checkbox | 100% | 하나은행 디폴트옵션 안정형 포트폴리오 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer` | 기업명 | seal | 100% | 위나아 |
| `sign.signer` | 기업명 | signature | 100% | 박찬연 |

### 퇴직연금 사전지정운용방법 지정 신청서(디폴트옵션 지정) (`hf168`) — 키 23개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `check.제도` | 제도 | checkbox | 100% | DC/기업형IRP(회사명 또는 계좌번호 |
| `customer.birth` | 생년월일 | date | 100% | 1990-02-10 |
| `check.택1` | 택1 | checkbox | 100% | 전화 |
| `check.선택` | 선택(1개) | checkbox | 100% | 하나은행 디폴트옵션 중립투자형 포트폴리오 1 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `check.투자권유를희망함` | 투자권유를희망함 | checkbox | 100% | 투자권유를 희망함 |
| `check.투자권유를희망하지않음` | 투자권유를희망하지않음 | checkbox | 100% | 투자권유를 희망하지 않음 |
| `handwritten` | 아래내용에대해 | text | 100% | 설명을듣고이해하였음 |
| `check.일반금융소비자` | 일반금융소비자 | checkbox | 100% | 만 65세 이상 고령자 |
| `check.전문금융소비자` | 전문금융소비자 | checkbox | 100% | 만 19세 이상 ~ 만 65세 미만 성년자 |
| `check.일반금융소비자2` | 일반금융소비자 | checkbox | 100% | 일반투자자(투자자정보확인서에서 일반투자자 선택) |
| `check.전문금융소비자2` | 전문금융소비자 | checkbox | 100% | 전문투자자(투자자정보확인서에서 전문투자자 선택) |
| `check.약관및상품설명서` | 약관및상품설명서 | checkbox | 100% | 서면 수령 |
| `signer.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer` | 가입자 | seal | 100% | 박찬연 |
| `sign.signer` | 가입자 | signature | 100% | 이욱유 |
| `signer2.name` | 대리인 | text | 100% | 최우빈 |
| `seal.signer2` | 대리인 | seal | 100% | 최우빈 |
| `sign.signer2` | 대리인 | signature | 100% | 박형민 |
| `handwritten2` | 가입자자필기재 | text | 100% | 설명듣고이해함 |
| `handwritten3` | 가입자자필기재 | text | 100% | 계약서,약관,상품설명서를수령함 |
| `handwritten4` | 가입자자필기재 | text | 100% | 설명을듣고이해 |

### 퇴직연금 가입자 거래신청서(DC/기업형IRP) (`hf169`) — 키 43개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `employer.name` | 회사명 | text | 100% | 주식회사 태평양무역 |
| `customer.birth` | 생년월일 | date | 100% | 1990년 2월 10일 |
| `check.휴대전화` | 휴대전화 | checkbox | 100% | LG U+ |
| `customer.address` | 자택주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `employer.address` | 직장주소 | text | 100% | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 주식회사 태… |
| `customer.home_phone` | 자택전화 | phone | 100% | 02-6588-1442 |
| `check.우편물수령처` | 우편물수령처 | checkbox | 100% | 자택 |
| `customer.email` | 이메일주소 | text | 100% | chanyeon363@naver.com |
| `employer.phone` | 직장전화 | phone | 100% | 043-783-2775 |
| `check.전화연락처` | 전화연락처 | checkbox | 100% | 자택 |
| `check.원리금보장상품만기도래시전월통지발송` | 원리금보장상품(정기예금등)만기도래시전월통지발송 | checkbox | 100% | 이메일 |
| `check.신청` | 신청(미발송) | checkbox | 100% | 신청(미발송) |
| `check.퇴직연금운용및자산관리약관이변경되는경우통지` | 퇴직연금운용및자산관리약관이변경되는경우통지 | checkbox | 100% | 알림톡(LMS) |
| `check.전화` | 전화(휴대폰) | checkbox | 100% | 온라인(모바일 웹) |
| `기업부담금_목록[].상품명` | 상품명 | text | 100% | 산업용 펌프 |
| `check.개인부담금` | 개인부담금 | checkbox | 100% | 개인부담금에 대하여 기업부담금(퇴직금)과 동일한 운용지시(체크 후 아래  |
| `개인부담금_목록[].상품명` | 상품명 | text | 100% | 기계 부품 |
| `기업부담금_목록[].매수비율` | 매수비율(%) | text | 100% | 30 |
| `개인부담금_목록[].매수비율` | 매수비율(%) | text | 100% | 25 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `목록[].상품명` | 상품명 | text | 100% | 플라스틱 원료 |
| `check.부담금구분` | 부담금구분 | checkbox | 100% | 개인부담금 |
| `목록[].매수비율` | 매수비율(%) | number | 100% | 95 |
| `check.선택` | 선택(1개) | checkbox | 100% | 하나은행 디폴트옵션 안정투자형 포트폴리오 3 |
| `check.보험성상품` | 보험성상품(GIC) | checkbox | 100% | 일반금융소비자 |
| `check.일반금융소비자` | 일반금융소비자 | checkbox | 100% | 피한정후견인 |
| `check.전문금융소비자` | 전문금융소비자 | checkbox | 100% | 전문금융소비자이나 상품설명을 희망 |
| `check.일반금융소비자2` | 일반금융소비자 | checkbox | 100% | 일반투자자(투자자정보확인서에서 일반투자자 선택) |
| `check.전문금융소비자2` | 전문금융소비자 | checkbox | 100% | 전문투자자(투자자정보확인서에서 전문투자자 선택) |
| `check.약관및상품설명서` | 약관및상품설명서 | checkbox | 100% | 알림톡(발송실패시 LMS 발송) |
| `check.투자권유를희망함` | 투자권유를희망함 | checkbox | 100% | 투자권유를 희망함 |
| `check.투자권유를희망하지않음` | 투자권유를희망하지않음 | checkbox | 100% | 투자권유를 희망하지 않음 |
| `handwritten` | 아래내용에대해 | text | 100% | 설명을듣고이해하였음 |
| `handwritten2` | 가입자자필기재 | text | 100% | 설명듣고이해함 |
| `handwritten3` | 가입자자필기재 | text | 100% | 계약서,약관,상품설명서를수령함 |
| `signer.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer` | 가입자 | seal | 100% | 박찬연 |
| `sign.signer` | 가입자 | signature | 100% | 현예지 |
| `signer2.name` | 대리인 | text | 100% | 박찬연 |
| `seal.signer2` | 대리인 | seal | 100% | 위나아 |
| `sign.signer2` | 대리인 | signature | 100% | 박찬연 |
| `handwritten4` | 가입자자필기재 | text | 100% | 설명을듣고이해 |

### 퇴직연금 계약이전 신청서(기업형IRP) (`hf170`) — 키 31개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `customer.name` | 가입자명 | text | 100% | 박찬연 |
| `account` | 퇴직연금계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `check.전부이전` | 전부이전 | checkbox | 100% | 전부이전 |
| `check.일부이전` | 일부이전 | checkbox | 100% | 일부이전 |
| `check.제도전환` | 제도전환(기업형IRP→DC) | checkbox | 100% | 제도전환(기업형IRP → DC) |
| `check.계열사이전` | 계열사이전(과거입사일인정) | checkbox | 100% | 계열사 이전(과거입사일 인정) |
| `예약지급일` | 예약지급일** | date | 100% | 2025년 3월 2일 |
| `운용관리기관` | 운용관리기관 | text | 100% | 하나은행 |
| `자산관리기관` | 자산관리기관 | text | 100% | 기업은행 |
| `현물이전` | 현물이전* | text | 100% |  |
| `check.수수료연동출금동의` | 수수료연동출금동의 | checkbox | 100% | 미동의 (기업별도 입금) |
| `check.현물이전` | 현물이전* | checkbox | 100% | 신청(보유상품 ‘해지 없이’ 이전) |
| `check.현물이전2` | 현물이전* | checkbox | 100% | 미신청(보유상품 ‘해지 후’ 이전) |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `금융기관` | 금융기관 | text | 100% | 카카오뱅크 |
| `account2` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `signer.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer` | 가입자 | seal | 100% | 이욱유 |
| `sign.signer` | 가입자 | signature | 100% | 박찬연 |
| `signer2.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer2` | 기업명 | seal | 100% | 현예지 |
| `sign.signer2` | 기업명 | signature | 100% | 박찬연 |
| `signer3.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer3` | 가입자 | seal | 100% | 이욱유 |
| `sign.signer3` | 가입자 | signature | 100% | 박찬연 |
| `이전받는기업` | 이전받는기업 | text | 100% |  |
| `seal.signer4` | 이전받는기업의법인인감증명서징구 | seal | 100% | 박찬연 |
| `sign.signer4` | 이전받는기업의법인인감증명서징구 | signature | 100% | 김소윤 |
| `value` | [유의사항] | amount | 100% |  |

### 퇴직연금 거래신청서(개인형IRP) (`hf171`) — 키 38개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.phone` | 휴대전화 | phone | 100% | 010-5907-7253 |
| `check.해피콜방식` | 해피콜방식 | checkbox | 100% | 온라인(모바일 웹) |
| `customer.birth` | 생년월일 | date | 100% | 1990-02-10 |
| `customer.email` | 이메일주소 | text | 100% | chanyeon363@naver.com |
| `check.신청용도` | 신청용도 | checkbox | 100% | 퇴직금용 |
| `check.신청용도2` | 신청용도 | checkbox | 100% | 퇴직금용+ |
| `퇴직급여수령을위한계좌개설` | 퇴직급여수령을위한계좌개설 | text | 100% | 542-054528-31217 |
| `check.할인대상정보` | 할인대상정보(증빙첨부) | checkbox | 100% | 장기할인(타사IRP이전시, 타사IRP가입일 |
| `check.가입자격` | 가입자격 | checkbox | 100% | 퇴직금제도 적용 근로자 |
| `check.원리금보장상품만기도래시전월통지발송` | 원리금보장상품(정기예금등)만기도래시전월통지발송 | checkbox | 100% | 이메일 |
| `check.서비스통지발송제외신청` | 서비스통지발송제외신청 | checkbox | 100% | 신청안함(발송) |
| `check.퇴직연금운용및자산관리약관이변경되는경우통지` | 퇴직연금운용및자산관리약관이변경되는경우통지 | checkbox | 100% | 이메일 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `check.투자권유를희망함` | 투자권유를희망함 | checkbox | 100% | 투자권유를 희망함 |
| `check.투자권유를희망하지않음` | 투자권유를희망하지않음 | checkbox | 100% | 투자권유를 희망하지 않음 |
| `handwritten` | 아래내용에대해 | text | 100% | 설명을듣고이해하였음 |
| `check.선택` | 선택(1개) | checkbox | 100% | 하나은행 디폴트옵션 중립투자형 포트폴리오 1 |
| `기업부담금_목록[].상품명` | 상품명 | text | 100% | 커피 원두 |
| `check.개인부담금` | 개인부담금 | checkbox | 100% | 개인부담금에 대하여 기업부담금(퇴직금)과 동일한 운용지시(체크 후 아래  |
| `개인부담금_목록[].상품명` | 상품명 | text | 100% | 전자부품 |
| `기업부담금_목록[].매수비율` | 매수비율(%) | text | 100% | 25 |
| `개인부담금_목록[].매수비율` | 매수비율(%) | text | 100% | 100 |
| `check.보험성상품` | 보험성상품(GIC) | checkbox | 100% | 일반금융소비자 |
| `check.일반금융소비자` | 일반금융소비자 | checkbox | 100% | 만 65세 이상 고령자 |
| `check.전문금융소비자` | 전문금융소비자 | checkbox | 100% | 전문금융소비자이나 상품설명을 희망 |
| `check.일반금융소비자2` | 일반금융소비자 | checkbox | 100% | 일반투자자(투자자정보확인서에서 일반투자자 선택) |
| `check.전문금융소비자2` | 전문금융소비자 | checkbox | 100% | 전문투자자(투자자정보확인서에서 전문투자자 선택) |
| `handwritten2` | 가입자자필기재 | text | 100% | 설명듣고이해함 |
| `check.약관및상품설명서` | 약관및상품설명서 | checkbox | 100% | 알림톡(발송실패시 LMS 발송) |
| `signer.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer` | 가입자 | seal | 100% | 박찬연 |
| `sign.signer` | 가입자 | signature | 100% | 현예지 |
| `signer2.name` | 대리인 | text | 100% | 강순준 |
| `seal.signer2` | 대리인 | seal | 100% | 김소윤 |
| `sign.signer2` | 대리인 | signature | 100% | 강순준 |
| `handwritten3` | 가입자자필기재 | text | 100% | 계약서,약관,상품설명서를수령함 |
| `handwritten4` | 가입자자필기재 | text | 100% | 설명을듣고이해수령 |

### 퇴직연금 거래신청서(DC, 기업형IRP) (`hf172`) — 키 49개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `check.제도구분` | 제도구분 | checkbox | 100% | DC |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `check.기업구분` | 기업구분 | checkbox | 100% | 개인사업자 |
| `회계결산월` | 회계결산월 | text | 100% |  |
| `check.근로자대표` | 근로자대표 | checkbox | 100% | 근로자과반수 |
| `check.제도가입대상` | 제도가입대상 | checkbox | 100% | 입사후 1년 경과가입 |
| `check.제도가입대상2` | 제도가입대상 | checkbox | 100% | 임원제외 |
| `check.부담금납입주기` | 부담금납입주기 | checkbox | 100% | 반기납 |
| `check.표준형DC대상여부` | 표준형DC대상여부 | checkbox | 100% |  대상 |
| `check.장기할인수수료대상여부` | 장기할인수수료대상여부* | checkbox | 100% |  대상 (타사 가일입자 |
| `date` | 제도시행일 | date | 100% | 2026년 1월 31일 |
| `check.퇴직연금가입기간` | 퇴직연금가입기간 | checkbox | 100% | 제도가입 이전 근무분 포함 |
| `date2` | 규약수리통보일 | date | 100% | 2026년 1월 31일 |
| `check.약관변경통지방법` | 약관변경통지방법 | checkbox | 100% |  알림톡(LMS) |
| `check.중소기업수수료할인대상여부` | 중소기업수수료할인대상여부 | checkbox | 100% | 대상(중소기업확인서 |
| `customer.name` | 이름 | text | 100% | 박찬연 |
| `customer.name2` | 이름 | text | 100% | 박찬연 |
| `customer.phone` | 휴대폰번호 | phone | 100% | 010-5907-7253 |
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.birth2` | 생년월일 | date | 100% | 1990.02.10 |
| `customer.email` | 이메일주소 | text | 100% | chanyeon363@naver.com |
| `check.일괄선택` | 일괄선택 | checkbox | 100% | 전체 상품 일괄 선택 |
| `check.체크` | 체크 | checkbox | 100% | 하나은행 디폴트옵션 적극투자형 BF 3 |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.name3` | 성명 | text | 100% | 박찬연 |
| `customer.birth3` | 생년월일 | date | 100% | 1990.02.10 |
| `금융기관` | 금융기관 | text | 100% | 우리은행 |
| `customer.name4` | 예금주 | text | 100% | 박찬연 |
| `check.사원번호임직원구분` | -사원번호:-임직원구분 | checkbox | 100% | 직원 |
| `check.사원번호임직원구분2` | -사원번호:-임직원구분 | checkbox | 100% | 직원 |
| `check.사원번호임직원구분3` | -사원번호:-임직원구분 | checkbox | 100% | 직원 |
| `check.사원번호임직원구분4` | -사원번호:-임직원구분 | checkbox | 100% | 직원 |
| `가입자수` | 가입자수 | number | 100% | 12 |
| `check.등록정보` | 등록정보 | checkbox | 100% | 개별등록(아래표 작성) |
| `기업부담금합계` | 기업부담금합계 | number | 100% | 4,320,000 |
| `check.신청` | 신청 | checkbox | 100% | 신청 |
| `check.신청2` | 신청 | checkbox | 100% | 신청 |
| `account` | 출금계좌번호 | account_no | 100% | 000-287736-52424 |
| `account2` | 출금계좌번호 | account_no | 100% | 996-316834-99379 |
| `이체개시일` | 이체개시일 | date | 100% | 2025년 4월 15일 |
| `이체종료일` | 이체종료일 | date | 100% | 2028년 8월 23일 |
| `check.신청3` | 신청 | checkbox | 100% | 신청 |
| `check.신청4` | 신청 | checkbox | 100% | 신청 |
| `account3` | 출금계좌번호 | account_no | 100% | 000-287736-52424 |
| `account4` | 출금계좌번호 | account_no | 100% | 774-646914-96117 |
| `signer.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer` | 기업명 | seal | 100% | 박찬연 |
| `sign.signer` | 기업명 | signature | 100% | 이민빈 |

### 투자자확인서(퇴직연금용) (`hf173`) — 키 32개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 투자자 | text | 100% | 박찬연 |
| `seal.signer` | 투자자 | seal | 100% | 박찬연 |
| `sign.signer` | 투자자 | signature | 100% | 최우빈 |
| `signer2.name` | 대리인 | text | 100% | 위나아 |
| `seal.signer2` | 대리인 | seal | 100% | 위나아 |
| `sign.signer2` | 대리인 | signature | 100% | 전영경 |
| `check.원금손실위험이거의없거나` | 원금손실위험이거의없거나경미한수준이다. | checkbox | 100% | 원금손실위험이 거의 없거나 경미한 수준이다. |
| `check.원금손실위험이있지만높은` | 원금손실위험이있지만높은수익률을위해감수할수있다. | checkbox | 100% | 원금손실위험이 있지만 높은 수익률을 위해 감수할 수 있다. |
| `check.경미한수준일것이다` | 경미한수준일것이다. | checkbox | 100% | 경미한 수준일 것이다. |
| `check.원금의최대100손실이` | 원금의최대100%(원금전액)손실이발생할수있다. | checkbox | 100% | 원금의 최대 100%(원금 전액) 손실이 발생할 수 있다. |
| `check.예` | 예 | checkbox | 100% | 아니오 |
| `check.email` | e-mail | checkbox | 100% | e-mail |
| `signer3.name` | 판매직원 | text | 100% | 박찬연 |
| `seal.signer3` | 판매직원 | seal | 100% | 이민빈 |
| `sign.signer3` | 판매직원 | signature | 100% | 강순준 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer4.name` | 투자자 | text | 100% | 박찬연 |
| `seal.signer4` | 투자자 | seal | 100% | 현예지 |
| `sign.signer4` | 투자자 | signature | 100% | 박찬연 |
| `signer5.name` | 대리인 | text | 100% | 강순준 |
| `seal.signer5` | 대리인 | seal | 100% | 강순준 |
| `sign.signer5` | 대리인 | signature | 100% | 위나아 |
| `check.원금손실위험이거의없거나2` | 원금손실위험이거의없거나경미한수준이다. | checkbox | 100% | 원금손실위험이 거의 없거나 경미한 수준이다. |
| `check.원금손실위험이있지만높은2` | 원금손실위험이있지만높은수익률을위해감수할수있다. | checkbox | 100% | 원금손실위험이 있지만 높은 수익률을 위해 감수할 수 있다. |
| `check.경미한수준일것이다2` | 경미한수준일것이다. | checkbox | 100% | 경미한 수준일 것이다. |
| `check.원금의최대100손실이2` | 원금의최대100%(원금전액)손실이발생할수있다. | checkbox | 100% | 원금의 최대 100%(원금 전액) 손실이 발생할 수 있다. |
| `check.예2` | 예 | checkbox | 100% | 아니오 |
| `check.email2` | e-mail | checkbox | 100% | 수령거절 |
| `signer6.name` | 판매직원 | text | 100% | 박찬연 |
| `seal.signer6` | 판매직원 | seal | 100% | 강순준 |
| `sign.signer6` | 판매직원 | signature | 100% | 박찬연 |

### 퇴직연금 계약이전 동의서 (`hf174`) — 키 62개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | 주식회사 한빛패션 |
| `check.동의주체` | 동의주체 | checkbox | 100% | 노동조합(근로자 과반수로 조직된 노동조합이 있는 경우) |
| `check.제도구분` | 제도구분 | checkbox | 100% | DC |
| `check.동의` | 동의 | checkbox | 100% | 동의 |
| `check.동의2` | 동의 | checkbox | 100% | 미동의 |
| `check.동의3` | 동의 | checkbox | 100% | 미동의 |
| `check.동의4` | 동의 | checkbox | 100% | 동의 |
| `check.동의5` | 동의 | checkbox | 100% | 미동의 |
| `check.동의6` | 동의 | checkbox | 100% | 동의 |
| `check.동의7` | 동의 | checkbox | 100% | 동의 |
| `check.동의8` | 동의 | checkbox | 100% | 미동의 |
| `check.동의9` | 동의 | checkbox | 100% | 미동의 |
| `check.동의10` | 동의 | checkbox | 100% | 미동의 |
| `check.동의11` | 동의 | checkbox | 100% | 미동의 |
| `check.동의12` | 동의 | checkbox | 100% | 미동의 |
| `check.동의13` | 동의 | checkbox | 100% | 미동의 |
| `check.동의14` | 동의 | checkbox | 100% | 동의 |
| `check.동의15` | 동의 | checkbox | 100% | 동의 |
| `check.동의16` | 동의 | checkbox | 100% | 미동의 |
| `check.동의17` | 동의 | checkbox | 100% | 미동의 |
| `check.동의18` | 동의 | checkbox | 100% | 동의 |
| `check.동의19` | 동의 | checkbox | 100% | 미동의 |
| `check.동의20` | 동의 | checkbox | 100% | 동의 |
| `목록[].성명` | 성명 | text | 100% | 이민예 |
| `목록[].생년월일` | 생년월일 | text | 100% | 2025-08-28 |
| `signer.name` | 생년월일 | text | 100% | 박찬연 |
| `seal.signer` | 생년월일 | seal | 100% | 강순준 |
| `sign.signer` | 생년월일 | signature | 100% | 박찬연 |
| `목록[].인서명` | 인/서명 | text | 100% |  |
| `check.동의21` | 동의 | checkbox | 100% | 미동의 |
| `check.동의22` | 동의 | checkbox | 100% | 미동의 |
| `check.동의23` | 동의 | checkbox | 100% | 미동의 |
| `check.동의24` | 동의 | checkbox | 100% | 미동의 |
| `check.동의25` | 동의 | checkbox | 100% | 미동의 |
| `check.동의26` | 동의 | checkbox | 100% | 동의 |
| `check.동의27` | 동의 | checkbox | 100% | 동의 |
| `check.동의28` | 동의 | checkbox | 100% | 동의 |
| `check.동의29` | 동의 | checkbox | 100% | 동의 |
| `check.동의30` | 동의 | checkbox | 100% | 미동의 |
| `check.동의31` | 동의 | checkbox | 100% | 동의 |
| `check.동의32` | 동의 | checkbox | 100% | 동의 |
| `check.동의33` | 동의 | checkbox | 100% | 동의 |
| `check.동의34` | 동의 | checkbox | 100% | 미동의 |
| `check.동의35` | 동의 | checkbox | 100% | 동의 |
| `check.동의36` | 동의 | checkbox | 100% | 미동의 |
| `check.동의37` | 동의 | checkbox | 100% | 동의 |
| `check.동의38` | 동의 | checkbox | 100% | 동의 |
| `check.동의39` | 동의 | checkbox | 100% | 동의 |
| `check.동의40` | 동의 | checkbox | 100% | 미동의 |
| `signer2.name` | 생년월일 | text | 100% | 박찬연 |
| `seal.signer2` | 생년월일 | seal | 100% | 박찬연 |
| `sign.signer2` | 생년월일 | signature | 100% | 강순준 |
| `signer3.name` | 대표자 | text | 100% | 박찬연 |
| `seal.signer3` | 대표자 | seal | 100% | 강순준 |
| `sign.signer3` | 대표자 | signature | 100% | 현예지 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `check.근로자동의` | 근로자동의 | checkbox | 100% | 근로자 동의 |
| `check.노동조합동의` | 노동조합동의 | checkbox | 100% | 노동조합 동의 |
| `signer4.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer4` | 기업명 | seal | 100% | 박찬연 |
| `sign.signer4` | 기업명 | signature | 100% | 이욱유 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |

### 퇴직연금 AI 포트폴리오 설계(신규 리밸런싱)신청서 (`hf175`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `check.제도구분` | 제도구분 | checkbox | 100% | 기업형IRP |
| `customer.birth` | 생년월일 | date | 100% | 1990년 2월 10일 |
| `계좌번호또는회사명` | 계좌번호또는회사명 | text | 100% | 243-274729-33607 |
| `하나연금닥터AI연금투자솔루션` | 하나연금닥터AI연금투자솔루션 | text | 100% |  |
| `check.포트폴리오매수또는리밸런싱후6개월마다리밸런싱안내` | 포트폴리오매수또는리밸런싱후6개월마다리밸런싱안내 | checkbox | 100% | 이메일 |
| `check.신청여부` | 신청여부 | checkbox | 100% | 알림톡(LMS) |
| `상승` | 상승+( | text | 100% |  |
| `하락` | )%하락–( | text | 100% |  |
| `handwritten` | 설계신청을동의합니다. | text | 100% | (동의함) |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인(본인) | text | 100% | 박찬연 |
| `seal.signer` | 신청인(본인) | seal | 100% | 박찬연 |
| `sign.signer` | 신청인(본인) | signature | 100% | 강순준 |
| `에도달할경우통지` | 에도달할경우통지 | text | 100% |  |

### 퇴직연금 퇴직급여 지급신청서(DC,기업형IRP) (`hf176`) — 키 47개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `employer.hire_date` | 입사일자 | date | 100% | 2020.05.08 |
| `account` | 퇴직연금계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.birth` | 생년월일 | date | 100% | 1990-02-10 |
| `중간정산일자` | 중간정산일자 | date | 100% | 2025-12-09 |
| `check.제도구분` | 제도구분 | checkbox | 100% | 기업형IRP |
| `check.임원여부` | 임원여부 | checkbox | 100% | 임원 |
| `퇴직급여입금총액` | 퇴직급여입금총액* | number | 100% | 3,560,000 |
| `퇴직일자` | 퇴직일자 | date | 100% | 2025.02.04 |
| `check.지급형태` | 지급형태 | checkbox | 100% | 개인형IRP(의무) |
| `check.지급형태2` | 지급형태 | checkbox | 100% | 입출금계좌 |
| `check.잔여부담금` | 잔여부담금*** | checkbox | 100% | 없음 |
| `check.잔여부담금2` | 잔여부담금*** | checkbox | 100% | 있음 (금액 |
| `check.기업반환신청` | 기업반환신청***** | checkbox | 100% | 계속근로기간 1년 미만 퇴직 |
| `check.현물이전` | 현물이전** | checkbox | 100% | 미신청 (보유상품 ‘해지 후’ IRP로 이전 (특별중도해지이율 적용)) |
| `check.예외사유` | 예외사유 | checkbox | 100% | 한시적 체류자격외국인의 출국 |
| `check.연동출금신청` | 연동출금신청(사전에약정된경우) | checkbox | 100% | 미신청(기업별도입금) |
| `예약지급일` | 예약지급일* | date | 100% | 2025.05.01 |
| `check.당해연도이전에중간정산한금액이있는경우` | 당해연도이전에중간정산(중도인출)한금액이있는경우 | checkbox | 100% | 합산과세 미적용 |
| `check.해당사항없음` | 해당사항없음 | checkbox | 100% | 해당사항 없음 |
| `금융기관명` | 금융기관명 | text | 100% | 우리은행 |
| `금융기관명2` | 금융기관명 | text | 100% | 국민은행 |
| `account2` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `account3` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.퇴직소득세계산을위한근속연수산정시제외가산월수있는경우기재` | 퇴직소득세계산을위한근속연수산정시제외·가산월수있는경우기재 | checkbox | 100% | 가산월수( |
| `check.개인적립금과세제외신청` | 개인적립금과세제외신청 | checkbox | 100% | 과세제외 미신청 |
| `check.가입자단독청구` | 가입자단독청구 | checkbox | 100% | 업체 폐업 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer` | 가입자 | seal | 100% | 강순준 |
| `sign.signer` | 가입자 | signature | 100% | 박찬연 |
| `signer2.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer2` | 가입자 | seal | 100% | 현예지 |
| `sign.signer2` | 가입자 | signature | 100% | 박찬연 |
| `signer3.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer3` | 기업명 | seal | 100% | 박찬연 |
| `sign.signer3` | 기업명 | signature | 100% | 현예지 |
| `signer4.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer4` | 가입자 | seal | 100% | 박찬연 |
| `sign.signer4` | 가입자 | signature | 100% | 강순준 |
| `타금융기관IRP통장사본` | 타금융기관IRP통장사본(가입확인서) | text | 100% | 국민은행 |
| `연금보험료등소득세액공제확인서` | 연금보험료등소득☞세액공제확인서 | number | 100% | 200,000 |
| `signer5.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer5` | 가입자 | seal | 100% | 현예지 |
| `sign.signer5` | 가입자 | signature | 100% | 박찬연 |
| `아래양식중한가지` | 아래양식중한가지 | text | 100% |  |

### 퇴직연금 운용상품지정 신청서(DC) (`hf177`) — 키 57개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자번호 | biz_no | 100% | 264-82-36559 |
| `check.아래의상품을퇴직연금운용상품으로` | 아래의상품을퇴직연금운용상품으로 | checkbox | 100% |  제외 요청합니다. |
| `상품선택` | 상품선택 | text | 100% | 하나 IRP 정기예금 3년 |
| `상품명` | 상품명 | text | 100% | 자동차 부품 |
| `경남은행정기예금` | 경남은행정기예금 | text | 100% | 기업은행 |
| `수익증권_목록[].경남은행정기예금` | 경남은행정기예금 | text | 100% | 기업은행 |
| `부산은행정기예금` | 부산은행정기예금 | text | 100% | 하나은행 |
| `정기예금_목록[].년` | 년 | text | 100% |  |
| `상품명2` | 상품명 | text | 100% | 플라스틱 원료 |
| `저축은행정기예금_목록[].JT저축은행정기예금` | JT저축은행정기예금 | text | 100% | 국민은행 |
| `하나저축은행정기예금` | 하나저축은행정기예금 | text | 100% | 농협은행 |
| `신한저축은행정기예금` | 신한저축은행정기예금 | text | 100% | 농협은행 |
| `NH저축은행정기예금` | NH저축은행정기예금 | text | 100% | 국민은행 |
| `KB저축은행정기예금` | KB저축은행정기예금 | text | 100% | 우리은행 |
| `IBK저축은행정기예금` | IBK저축은행정기예금 | text | 100% | 농협은행 |
| `한화저축은행정기예금` | 한화저축은행정기예금 | text | 100% | 카카오뱅크 |
| `SBI저축은행정기예금` | SBI저축은행정기예금 | text | 100% | 기업은행 |
| `OK저축은행정기예금` | OK저축은행정기예금 | text | 100% | 국민은행 |
| `키움저축은행정기예금` | 키움저축은행정기예금 | text | 100% | 하나은행 |
| `키움예스저축은행정기예금` | 키움예스저축은행정기예금 | text | 100% | 국민은행 |
| `페퍼저축은행정기예금` | 페퍼저축은행정기예금 | text | 100% | 카카오뱅크 |
| `모아저축은행정기예금` | 모아저축은행정기예금 | text | 100% | 기업은행 |
| `유진저축은행정기예금` | 유진저축은행정기예금 | text | 100% | 국민은행 |
| `OSB저축은행정기예금` | OSB저축은행정기예금 | text | 100% | 카카오뱅크 |
| `JT저축은행정기예금` | JT저축은행정기예금 | text | 100% | 기업은행 |
| `check.보기1` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기12` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기13` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기14` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기15` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기16` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기17` | 보기1 | checkbox | 100% | 보기1 |
| `저축은행정기예금_목록[].년` | 년 | text | 100% |  |
| `check.보기18` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기19` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기110` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기111` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기112` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기113` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기114` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기115` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기116` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기117` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기118` | 보기1 | checkbox | 100% | 보기1 |
| `check.개월` | 개월 | checkbox | 100% | □ |
| `check.년` | 년 | checkbox | 100% | □ |
| `check.년2` | 년 | checkbox | 100% | □ |
| `check.년3` | 년 | checkbox | 100% | □ |
| `check.년4` | 년 | checkbox | 100% | 저 축 은 행 정 기 예 금 |
| `check.개월2` | 개월 | checkbox | 100% | □ |
| `check.년5` | 년 | checkbox | 100% | □ |
| `check.년6` | 년 | checkbox | 100% | □ |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer` | 기업명 | seal | 100% | 박찬연 |
| `sign.signer` | 기업명 | signature | 100% | 현예지 |

### 퇴직연금 입금예정상품등록/변경 신청서 (`hf178`) — 키 31개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명(기업명) | text | 100% | 박찬연 |
| `check.제도구분` | 제도구분 | checkbox | 100% | DC |
| `customer.birth` | 생년월일(사업자등록번호) | date | 100% | 1990년 2월 10일 |
| `계좌번호또는회사명` | 계좌번호또는회사명 | text | 100% | 640-301927-71029 |
| `check.상품구분` | 상품구분 | checkbox | 100% | 일반상품 |
| `기업부담금_목록[].상품명` | 상품명 | text | 100% | PCB 기판 |
| `check.개인부담금` | 개인부담금 | checkbox | 100% | 개인부담금에 대하여 기업부담금(퇴직금)과 동일한 운용지시(√체크 후 아래 |
| `개인부담금_목록[].상품명` | 상품명 | text | 100% | 포장재 |
| `기업부담금_목록[].매수비율` | 매수비율(%) | number | 100% | 45 |
| `개인부담금_목록[].매수비율` | 매수비율(%) | text | 100% | 95 |
| `목록[].상품명` | 상품명 | text | 100% | 철강 코일 |
| `check.등록구분` | 등록구분 | checkbox | 100% | 기업부담금(퇴직금) |
| `목록[].매수비율` | 매수비율(%) | number | 100% | 30 |
| `check.일반금융소비자` | 일반금융소비자 | checkbox | 100% | 피성년후견인 |
| `check.전문금융소비자` | 전문금융소비자 | checkbox | 100% | 만 19세 이상 ~ 만 65세 미만 성년자 |
| `check.일반금융소비자2` | 일반금융소비자 | checkbox | 100% | 전문금융소비자 외 금융소비자 |
| `check.전문금융소비자2` | 전문금융소비자 | checkbox | 100% | 국가, 금융회사, 보험 관계 단체, 보험요율산출 기관, 공공기관 등 |
| `check.일반금융소비자3` | 일반금융소비자 | checkbox | 100% | 일반투자자(투자자정보확인서에서 일반투자자 선택) |
| `check.전문금융소비자3` | 전문금융소비자 | checkbox | 100% | 전문투자자(투자자정보확인서에서 전문투자자 선택) |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `check.약관및상품설명서` | 약관및상품설명서 | checkbox | 100% | 서면 수령 |
| `handwritten` | 가입자자필기재 | text | 100% | 설명듣고이해함 |
| `handwritten2` | 가입자자필기재 | text | 100% | 계약서,약관,상품설명서를수령함 |
| `check.전화해피콜` | 전화(휴대폰)해피콜 | checkbox | 100% | 전화(휴대폰) 해피콜 |
| `handwritten3` | 가입자자필기재 | text | 100% | 설명을듣고이해 |
| `signer.name` | 가입자(기업명) | text | 100% | 박찬연 |
| `seal.signer` | 가입자(기업명) | seal | 100% | 강순준 |
| `sign.signer` | 가입자(기업명) | signature | 100% | 박찬연 |
| `signer2.name` | 대리인 | text | 100% | 이주원 |
| `seal.signer2` | 대리인 | seal | 100% | 김나우 |
| `sign.signer2` | 대리인 | signature | 100% | 이주원 |

### 퇴직연금 퇴직급여 지급신청서(DB) (`hf179`) — 키 37개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `customer.name` | 가입자성명 | text | 100% | 박찬연 |
| `employer.hire_date` | 입사일자 | date | 100% | 2020.05.08 |
| `DB계좌번호` | DB계좌번호 | text | 100% | 326-668155-97230 |
| `customer.birth` | 생년월일 | date | 100% | 1990년 2월 10일 |
| `퇴직일자` | 퇴직일자 | date | 100% | 2025-07-30 |
| `check.지급형태` | 지급형태 | checkbox | 100% | IRP이전(의무) |
| `check.지급형태2` | 지급형태 | checkbox | 100% | 요구불계좌 |
| `예약지급일주1` | 예약지급일주1 | text | 100% |  |
| `check.만55세이후퇴직` | 만55세이후퇴직 | checkbox | 100% | 한시적 체류자격 외국인 |
| `퇴직급여총액` | 퇴직급여총액 | number | 100% | 4,250,000 |
| `지급신청금액` | 지급신청금액 | number | 100% | 9,410,000 |
| `check.기업으로반환신청` | (필요시기재)기업으로반환신청 | checkbox | 100% | 퇴직소득세  |
| `check.지급방식` | 지급방식 | checkbox | 100% | 적립비율지급 |
| `금융기관명` | 금융기관명 | text | 100% | 농협은행 |
| `금융기관명2` | 금융기관명 | text | 100% | 하나은행 |
| `account` | 계좌번호 | account_no | 100% | 774-646914-96117 |
| `account2` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `목록[].매도순위` | 매도순위 | text | 100% |  |
| `목록[].상품명` | 상품명 | text | 100% | 커피 원두 |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 789-760323-44291 |
| `목록[].매도금액` | 매도금액(원/좌) | number | 100% | 29,750,000 |
| `check.가입자단독청구` | 가입자단독청구 | checkbox | 100% | 기타 (사용자 지급 거절 등) |
| `영업점본인확인` | 영업점본인확인 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer` | 가입자 | seal | 100% | 박찬연 |
| `sign.signer` | 가입자 | signature | 100% | 이욱유 |
| `signer2.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer2` | 기업명 | seal | 100% | 강순준 |
| `sign.signer2` | 기업명 | signature | 100% | 박찬연 |
| `signer3.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer3` | 가입자 | seal | 100% | 박찬연 |
| `sign.signer3` | 가입자 | signature | 100% | 강순준 |
| `필수서류` | 필수서류 | text | 100% |  |
| `퇴직소득원천징수영수증` | 퇴직소득원천징수영수증 | number | 100% | 28,270,000 |
| `타금융기관IRP또는요구불계좌사본` | 타금융기관IRP또는요구불계좌사본 | text | 100% | 336-412010-05148 |

### DB 적립금 이전 요청서 (`hf180`) — 키 5개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].이전하는금융회사` | 이전하는금융회사(운용관리기관명) | text | 100% | 우리은행 |
| `목록[].운용관리기관명` | 운용관리기관명 | text | 100% | 하나은행 |
| `목록[].자산관리기관명` | 자산관리기관명 | text | 100% | 카카오뱅크 |
| `목록[].적립금이전액` | 적립금이전액* | text | 100% | 7,640,000 |
| `목록[].실물이전여부` | 실물이전여부 | text | 100% |  |

### 이전 가입자 명부(DC,기업형 IRP용) (`hf181`) — 키 7개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].이전하는금융회사` | 이전하는금융회사(운용관리기관명) | text | 100% | 기업은행 |
| `목록[].운용관리기관명자산관리기관명` | 운용관리기관명자산관리기관명 | text | 100% | 카카오뱅크 |
| `목록[].성명` | 성명 | text | 100% | 변환승 |
| `목록[].주민번호` | 주민번호 | text | 100% | 803846-5982335 |
| `목록[].연락처` | 연락처 | text | 100% | 010-5907-7253 |
| `목록[].실물이전여부1현금2실물` | 실물이전여부1.현금2.실물 | text | 100% |  |
| `목록[].서명날인` | 서명/날인 | text | 100% |  |

### 이전신청(취소)서(DB,DC,기업형IRP 이전용) (`hf182`) — 키 30개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.신청내용` | 신청내용 | checkbox | 100% | 이전 신청 취소( |
| `check.이전의사확인` | 이전의사확인* | checkbox | 100% | 이전하는 금융회사 방문 |
| `check.신청서제출처` | 신청서제출처 | checkbox | 100% | 이전하는 금융회사 |
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자번호 | biz_no | 100% | 261-82-53694 |
| `담당자성명` | 담당자성명 | text | 100% | 이유희 |
| `customer.phone` | 전화번호 | phone | 100% | 010-5907-7253 |
| `check.제도유형` | 제도유형 | checkbox | 100% | 기업형IRP |
| `check.이전계약` | 이전계약 | checkbox | 100% | 운용관리계약+자산관리계약 |
| `check.이전유형` | 이전유형 | checkbox | 100% | 일부(적립금, 가입자)이전 |
| `check.이전대상` | 이전대상** | checkbox | 100% | 실물 |
| `이전금액` | 이전금액***(DB일부이전) | number | 100% | 238,390,000 |
| `금융회사명` | 금융회사명 | text | 100% | 국민은행 |
| `signer.name` | 금융기관명:지점명 | text | 100% | 박찬연 |
| `seal.signer` | 금융기관명:지점명 | seal | 100% | 박찬연 |
| `sign.signer` | 금융기관명:지점명 | signature | 100% | 강순준 |
| `금융회사명2` | 금융회사명 | text | 100% | 카카오뱅크 |
| `관리번호` | (운용관리기관관리번호)관리번호 | text | 100% | 513-824150-00976 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer2.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer2` | 기업명 | seal | 100% | 현예지 |
| `sign.signer2` | 기업명 | signature | 100% | 박찬연 |
| `signer3.name` | 지점명 | text | 100% | 박찬연 |
| `seal.signer3` | 지점명 | seal | 100% | 박찬연 |
| `sign.signer3` | 지점명 | signature | 100% | 강순준 |
| `이전받을기관` | 이전받을기관 | text | 100% |  |
| `agent.name` | 대리인 | text | 100% | 박영준 |
| `금융기관명` | 금융기관명 | text | 100% | 신한은행 |
| `customer.phone2` | 전화번호 | phone | 100% | 010-5907-7253 |
| `팩스번호` | 팩스번호 | phone | 100% | 043-783-2775 |

### 퇴직연금 통지서비스 신청서(가입자용) (`hf183`) — 키 29개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].은행사용란` | 은행사용란 | text | 100% |  |
| `customer.name` | 성명(업체명) | text | 100% | 박찬연 |
| `customer.birth` | 생년월일 | date | 100% | 2026년 1월 31일 |
| `check.휴대전화` | 휴대전화 | checkbox | 100% | SKT  |
| `Email주소` | E-mail주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `자택` | 자택 | text | 100% |  |
| `employer.name` | 직장 | text | 100% | 주식회사 태평양무역 |
| `customer.home_phone` | 자택전화 | phone | 100% | 02-1244-9090 |
| `employer.phone` | 직장전화 | phone | 100% | 043-783-2775 |
| `check.우편물수령처` | 우편물수령처 | checkbox | 100% | 자택 |
| `check.전화연락처` | 전화연락처 | checkbox | 100% | 휴대폰 |
| `check.년월일` | 년월일 | checkbox | 100% | 고객정보  |
| `필수통지` | 필수(법적)통지 | text | 100% |  |
| `목표수익률에도달하면펀드자동환매` | 목표수익률에도달하면펀드자동환매 | text | 100% |  |
| `check.상승자동환매` | 상승+%자동환매 | checkbox | 100% | 하락 - % 자동환매 |
| `check.상승자동환매2` | 상승+%자동환매 | checkbox | 100% | 보기2 |
| `check.상승자동환매3` | 상승+%자동환매 | checkbox | 100% | 하락 - % 자동환매 |
| `check.운용현황보고서발송주기` | 운용현황보고서발송주기(기본값:분기발송) | checkbox | 100% | 분기 |
| `check.원리금보장상품만기도래시전월통지발송` | 원리금보장상품(정기예금등)만기도래시전월통지발송 | checkbox | 100% | 이메일 |
| `check.퇴직연금운용및자산관리약관이변경되는경우통지` | 퇴직연금운용및자산관리약관이변경되는경우통지 | checkbox | 100% | 수신거부 |
| `check.집합투자증권매수시예탁결제원의자산운용보고서수령방법` | 집합투자증권매수시예탁결제원의자산운용보고서수령방법 | checkbox | 100% | 영업점 수령/홈페이지 확인 |
| `check.목표수익률에도달하면펀드자동환매` | 목표수익률에도달하면펀드자동환매 | checkbox | 100% | 신청안함 |
| `check.신청` | 신청(미발송) | checkbox | 100% | 신청(미발송) |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `check.AI포트폴리오가입후매1년마다정기적으로리밸런싱을안내` | AI포트폴리오가입후매1년마다정기적으로리밸런싱을안내 | checkbox | 100% | 알림톡(LMS) |
| `check.신청여부` | 신청여부 | checkbox | 100% | 알림톡(LMS) |
| `signer.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer` | 가입자 | seal | 100% | 박찬연 |
| `sign.signer` | 가입자 | signature | 100% | 현예지 |

### 퇴직연금 계약해지 신청서(개인형IRP) (`hf184`) — 키 16개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `account` | 퇴직연금계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.birth` | 생년월일 | date | 100% | 1997.05.14 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `check.일반사유` | 일반사유 | checkbox | 100% | 일반 중도해지 |
| `check.부득이한사유` | 부득이한사유 | checkbox | 100% | 가입자의 사망 |
| `금융기관명` | 금융기관명 | text | 100% | 하나은행 |
| `account2` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `당해년도납입액` | 당해년도납입액 | text | 100% |  |
| `퇴직금` | 퇴직금 | text | 100% |  |
| `연금계좌의운용소득` | 연금계좌의운용소득 | number | 100% | 870,000 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 전영경 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |
| `소득공제받은납입금액` | 소득(세액)공제받은납입금액 | number | 100% | 600,000 |

### 퇴직연금 DC 기업부담금 자동이체 신청서 (`hf185`) — 키 17개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `check.신청구분` | 신청구분 | checkbox | 100% | 변경 |
| `date` | 이체개시일 | date | 100% | 2026년 1월 31일 |
| `date2` | 이체종료일 | date | 100% | 2026년 1월 31일 |
| `account` | 출금계좌번호 | account_no | 100% | 000-287736-52424 |
| `account2` | 입금계좌번호 | account_no | 100% | 000-287736-52424 |
| `date3` | 년월일 | date | 100% | 2026년 01월 31일 |
| `목록[].가입자명` | 가입자명 | text | 100% |  |
| `총가입자수` | 총가입자수 | text | 100% |  |
| `목록[].생년월일` | 생년월일 | text | 100% | 2025.10.28 |
| `목록[].이체금액` | 이체금액 | number | 100% | 7,190,000 |
| `목록[].원` | 원 | text | 100% | 41,260,000 |
| `총액` | 총액 | number | 100% | 9,360,000원 |
| `date4` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer` | 서명또는 | seal | 100% | 현예지 |
| `sign.signer` | 서명또는 | signature | 100% | 박찬연 |

### 퇴직연금_거래신청서(DB) (`hf186`) — 키 78개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 261-82-53694 |
| `회계결산월` | 회계결산월 | text | 100% |  |
| `date` | 제도시행일 | date | 100% | 2026년 1월 31일 |
| `간사기관` | 간사기관 | text | 100% |  |
| `비간사기관` | 비간사기관 | text | 100% |  |
| `동의미동의` | 동의󠇧미동의(현금성자산으로운용) | text | 100% |  |
| `date2` | 규약수리통보일 | date | 100% | 2026년 1월 31일 |
| `customer.name` | 이름 | text | 100% | 박찬연 |
| `customer.name2` | 이름 | text | 100% | 박찬연 |
| `customer.phone` | 휴대폰번호 | phone | 100% | 010-5907-7253 |
| `customer.birth` | 생년월일 | date | 100% | 1990년 2월 10일 |
| `customer.birth2` | 생년월일 | date | 100% | 1990년 2월 10일 |
| `customer.email` | 이메일주소 | text | 100% | chanyeon363@naver.com |
| `명미만` | 명미만(명)󠇧 | text | 100% |  |
| `date3` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.name3` | 성명 | text | 100% | 박찬연 |
| `customer.birth3` | 생년월일 | date | 100% | 1990년 2월 10일 |
| `customer.name4` | 예금주 | text | 100% | 박찬연 |
| `제도가입이후근무분만` | 제도가입이후근무분만󠇧 | text | 100% |  |
| `제도가입이전근무분포함` | 제도가입이전근무분포함󠇧 | text | 100% |  |
| `비대상` | 비대상󠇧 | text | 100% |  |
| `대상타사가입일자` | 대상(타사가입일자 | date | 100% | 2025.11.10 |
| `비대상2` | 비대상󠇧 | text | 100% |  |
| `가입자수` | 가입자수 | text | 100% |  |
| `signer.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer` | 기업명 | seal | 100% | 김아진 |
| `sign.signer` | 기업명 | signature | 100% | 박찬연 |
| `성명` | -성명 | text | 100% |  |
| `직원임원촉탁정년초과` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | 100% |  |
| `주민등록번호` | -주민등록번호 | text | 100% |  |
| `입사일중간정산일자` | -입사일:-중간정산일자 | text | 100% |  |
| `사원번호이메일` | -사원번호:-이메일:󠇧 | text | 100% |  |
| `성명2` | -성명 | text | 100% |  |
| `직원임원촉탁정년초과2` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | 100% |  |
| `주민등록번호2` | -주민등록번호 | text | 100% |  |
| `입사일중간정산일자2` | -입사일:-중간정산일자 | text | 100% |  |
| `사원번호이메일2` | -사원번호:-이메일:󠇧 | text | 100% |  |
| `성명3` | -성명 | text | 100% |  |
| `직원임원촉탁정년초과3` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | 100% |  |
| `주민등록번호3` | -주민등록번호 | text | 100% |  |
| `입사일중간정산일자3` | -입사일:-중간정산일자 | text | 100% |  |
| `사원번호이메일3` | -사원번호:-이메일:󠇧 | text | 100% |  |
| `성명4` | -성명 | text | 100% |  |
| `직원임원촉탁정년초과4` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | 100% |  |
| `주민등록번호4` | -주민등록번호 | text | 100% |  |
| `입사일중간정산일자4` | -입사일:-중간정산일자 | text | 100% |  |
| `사원번호이메일4` | -사원번호:-이메일:󠇧 | text | 100% |  |
| `성명5` | -성명 | text | 100% |  |
| `직원임원촉탁정년초과5` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | 100% |  |
| `주민등록번호5` | -주민등록번호 | text | 100% |  |
| `입사일중간정산일자5` | -입사일:-중간정산일자 | text | 100% |  |
| `사원번호이메일5` | -사원번호:-이메일:󠇧 | text | 100% |  |
| `성명6` | -성명 | text | 100% |  |
| `직원임원촉탁정년초과6` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | 100% |  |
| `주민등록번호6` | -주민등록번호 | text | 100% |  |
| `입사일중간정산일자6` | -입사일:-중간정산일자 | text | 100% |  |
| `사원번호이메일6` | -사원번호:-이메일:󠇧 | text | 100% |  |
| `성명7` | -성명 | text | 100% |  |
| `직원임원촉탁정년초과7` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | 100% |  |
| `주민등록번호7` | -주민등록번호 | text | 100% |  |
| `입사일중간정산일자7` | -입사일:-중간정산일자 | text | 100% |  |
| `사원번호이메일7` | -사원번호:-이메일:󠇧 | text | 100% |  |
| `성명8` | -성명 | text | 100% |  |
| `직원임원촉탁정년초과8` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | 100% |  |
| `주민등록번호8` | -주민등록번호 | text | 100% |  |
| `입사일중간정산일자8` | -입사일:-중간정산일자 | text | 100% |  |
| `사원번호이메일8` | -사원번호:-이메일:󠇧 | text | 100% |  |
| `성명9` | -성명 | text | 100% |  |
| `직원임원촉탁정년초과9` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | 100% |  |
| `주민등록번호9` | -주민등록번호 | text | 100% |  |
| `입사일중간정산일자9` | -입사일:-중간정산일자 | text | 100% |  |
| `사원번호이메일9` | -사원번호:-이메일:󠇧 | text | 100% |  |
| `성명10` | -성명 | text | 100% |  |
| `직원임원촉탁정년초과10` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | 100% |  |
| `주민등록번호10` | -주민등록번호 | text | 100% |  |
| `입사일중간정산일자10` | -입사일:-중간정산일자 | text | 100% |  |
| `사원번호이메일10` | -사원번호:-이메일:󠇧 | text | 100% |  |

### 퇴직연금 중도인출신청서(DC,기업형·개인형IRP) (`hf188`) — 키 81개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `check.제도` | 제도 | checkbox | 100% | 기업형IRP |
| `employer.hire_date` | 입사일 | date | 100% | 2020.05.08 |
| `customer.birth` | 생년월일 | date | 100% | 1990.02.10 |
| `계좌번호또는회사명` | 계좌번호또는회사명 | text | 100% | 344-697682-34689 |
| `중간정산일` | 중간정산일 | date | 100% | 2025-08-31 |
| `customer.phone` | 휴대전화 | phone | 100% | 010-5907-7253 |
| `check.신청금액` | 신청금액 | checkbox | 100% | 전부 |
| `check.임원여부` | 임원여부 | checkbox | 100% | 임원 |
| `check.가입자부담금여부` | 가입자부담금여부 | checkbox | 100% | 가입자부담금(적립금) 없음 |
| `check.추가부담금입금여부` | 추가부담금입금여부 | checkbox | 100% | 해당사항 없음 |
| `check.해당사항있음금액` | 해당사항있음(금액 | checkbox | 100% | 해당사항 있음 ( 금액 |
| `check.당해연도이전에중간정산한금액이있는경우` | 당해연도이전에중간정산(중도인출)한금액이있는경우 | checkbox | 100% | 합산과세 미적용 |
| `check.해당사항없음` | 해당사항없음 | checkbox | 100% | 해당사항 없음 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `value` | [일부신청시유의사항] | amount | 100% |  |
| `value2` | [가입자부담금이있는경우유의사항] | amount | 100% |  |
| `부득이한사유의세율적용` | 부득이한사유의세율적용 | text | 100% | 주택구입 |
| `금융기관명` | 금융기관명 | text | 100% | 우리은행 |
| `customer.name2` | 예금주 | text | 100% | 박찬연 |
| `목록[].매도순위` | 매도순위 | text | 100% |  |
| `목록[].상품명` | 상품명 | text | 100% | 철강 코일 |
| `목록[].계좌번호` | 계좌번호 | text | 100% | 748-445122-14066 |
| `목록[].매도금액` | 매도금액(원/좌) | text | 100% | 9,060,000 |
| `check.무주택자인가입자가본인명` | 무주택자인가입자가본인명의로주택구입하는경우 | checkbox | 100% | 무주택자인 가입자가 본인 명의로 주택 구입하는 경우 |
| `check.무주택자인가입자의주거목` | 무주택자인가입자의주거목적의전세금(임차보증금)부담하는경우 | checkbox | 100% | 무주택자인 가입자의 주거 목적의 전세금(임차보증금) 부담하는 경우 |
| `check.개월이상요양을필요로하는` | 개월이상요양을필요로하는본인또는부양가족(배우자의부양가족포함 | checkbox | 100% | 개월 이상 요양을 필요로 하는 본인 또는 부양가족(배우자의 부양가족 포함 |
| `check.년이내에채무자회생및파` | 년이내에「채무자회생및파산에관한법률」에따라파산선고를받은 | checkbox | 100% | 년 이내에 「채무자 회생 및 파산에 관한 법률」에 따라 파산선고를 받은  |
| `check.년이내에채무자회생및파2` | 년이내에「채무자회생및파산에관한법률」에따라개인회생절차개시 | checkbox | 100% | 년 이내에 「채무자 회생 및 파산에 관한 법률」에 따라 개인회생절차 개시 |
| `check.가입자가입자의배우자또는` | 가입자,가입자의배우자또는부양가족이「재난및안전관리기본법」에따 | checkbox | 100% | 가입자, 가입자의 배우자 또는 부양가족이 「재난 및 안전관리기본법」에 따 |
| `check.퇴직급여를담보로제공하여` | 퇴직급여를담보로제공하여대출을받은가입자가그대출상환을하기위한 | checkbox | 100% | 퇴직급여를 담보로 제공하여 대출을 받은 가입자가 그 대출상환을 하기 위한 |
| `value3` | [무주택서약서] | amount | 100% |  |
| `customer.name3` | 가입자 | text | 100% | 박찬연 |
| `customer.name4` | 가입자 | text | 100% | 박찬연 |
| `customer.name5` | 가입자 | text | 100% | 박찬연 |
| `customer.name6` | 가입자 | text | 100% | 박찬연 |
| `customer.name7` | 가입자 | text | 100% | 박찬연 |
| `company.name` | 기업명 | text | 100% | (주)삼정전자 |
| `customer.name8` | 가입자 | text | 100% | 박찬연 |
| `년이내에채무자회생및파산에관한법률에따라파산선고를받은경우` | 년이내에“채무자회생및파산에관한법률”에따라파산선고를받은경우 | text | 100% |  |
| `check.신청시기` | 신청시기 | checkbox | 100% | 계약 체결일로부터 소유권 이전 등기 후 1개월 이내 |
| `check.공통서류` | 공통서류 | checkbox | 100% | 지방세 세목별 과세증명서 (지역 |
| `check.주택매매` | 주택매매 | checkbox | 100% | 매수할 부동산의 등기사항전부증명서-건물 또는 건축물관리대장 (1개월 이내 |
| `check.분양분양전환` | 분양/분양전환 | checkbox | 100% | 분양(공급) 계약서 (동/호수 배정, 권리의무 승계 내역 포함한 계약서  |
| `check.분양권매수` | 분양권매수 | checkbox | 100% | 주택분양(공급)계약서 및 분양권 매매계약서 (동/호수 배정, 권리의무 승 |
| `check.주택청약당첨` | 주택청약당첨 | checkbox | 100% | 계약금 납부일정 확인서류 |
| `check.주택신축` | 주택신축 | checkbox | 100% | 공사계약서 |
| `check.경매취득` | 경매취득 | checkbox | 100% | 대금지급기한통지서 |
| `check.오피스텔` | 오피스텔 | checkbox | 100% | 건축물관리대장 –건물 용도 |
| `check.소유권이전후` | 소유권이전후 | checkbox | 100% | 소유권 이전 완료 된 등기사항전부증명서-건물 또는 건축물관리대장 (1개월 |
| `check.신청시기2` | 신청시기 | checkbox | 100% | 주택임대차계약 체결일로부터 잔금 지급일 이후 1개월 이내 |
| `check.공통서류2` | 공통서류 | checkbox | 100% | 전(월)세 계약서 (부동산 중개인을 통한 거래) |
| `check.연장` | 연장 | checkbox | 100% | 연장 전/후 전(월)세 임대차 계약서 (부동산 중개인을 통한 거래 ) |
| `check.주택이외` | 주택이외 | checkbox | 100% | 전입 후 주민등록등본 ( 임차부동산 전입신고 후 신청 가능) |
| `check.잔금지급후` | 잔금지급후 | checkbox | 100% | 전입 후 주민등록등본 |
| `check.신청시기3` | 신청시기 | checkbox | 100% | 요양 중이거나 요양 종료일로부터 1개월 이내 |
| `check.요양필요확인서류` | 요양필요확인서류 | checkbox | 100% | 중도인출신청서 (회사 명판 및 거래인감 날인, 가입자 날인) , 가입자  |
| `check.의료비지출확인서류` | 의료비지출확인서류 | checkbox | 100% | 의료기관 등에서 발급한 영수증, 진료비 청구서, 진료비 납입확인서, 진료 |
| `check.연간임금총액확인서류` | 연간임금총액확인서류 | checkbox | 100% | 가입자의 직전연도 근로소득원천징수영수증 또는 급여명세서 |
| `check.배우자또는부양가족요양비용의경우확인서류` | 배우자또는부양가족요양비용의경우확인서류 | checkbox | 100% | 주민등록등본 또는 가족관계증명서 (1개월 이내) |
| `check.신청시기4` | 신청시기 | checkbox | 100% | 신청일 기준 개인회생 개시결정일로부터 5년 이내 |
| `check.필요서류` | 필요서류 | checkbox | 100% | 개인회생절차 개시결정문 또는 개인회생절차변제인가 확정증명원(변제계획서 포 |
| `check.신청시기5` | 신청시기 | checkbox | 100% | 신청일 기준 파산 선고일로부터 5년 이내 |
| `check.필요서류2` | 필요서류 | checkbox | 100% | 중도인출신청서 (회사 명판 및 거래인감 날인, 가입자 날인) , 가입자  |
| `주택신축` | 주택신축 | text | 100% |  |
| `연장` | 연장 | text | 100% |  |
| `요양필요` | 요양필요 | text | 100% |  |
| `연간임금총액` | 연간임금총액 | number | 100% | 660,000 |
| `배우자또는` | 배우자또는 | text | 100% |  |
| `부양가족` | 부양가족 | text | 100% |  |
| `요양비용의경우` | 요양비용의경우 | text | 100% |  |
| `check.과세제외및환급신청서` | 과세제외및환급신청서 | checkbox | 100% | 연금보험료 등 소득 · 세액공제 확인서 |
| `check.신청시기6` | 신청시기 | checkbox | 100% | 피해발생일로부터 3개월 이내 |
| `check.물적피해` | 물적피해 | checkbox | 100% | 중도인출신청서 (회사 명판 및 거래인감 날인, 가입자 날인) , 가입자  |
| `check.인적피해` | 인적피해 | checkbox | 100% | 사망/실종 된 경우 |
| `check.배우자또는부양가족재난의경우확인서류` | 배우자또는부양가족재난의경우확인서류 | checkbox | 100% | 주민등록등본 또는 가족관계증명서 (1개월 이내) |
| `발급기준` | 발급기준 | text | 100% |  |
| `물적피해` | 물적피해 | text | 100% |  |
| `배우자또는2` | 배우자또는 | text | 100% |  |
| `예인천광역시남동구` | 예)인천광역시남동구 | text | 100% |  |
| `재산세` | 재산세(주택) | text | 100% |  |

### 퇴직연금 부담금 등록 신청서(DC,기업형IRP) (`hf189`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `account` | 퇴직연금계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.신청구분` | 신청구분 | checkbox | 100% | 취소 |
| `check.부담금종류` | 부담금종류 | checkbox | 100% | 지연이자 |
| `부담금등록가입자수` | 부담금등록가입자수 | number | 100% | 3 |
| `check.납부방법` | 납부방법 | checkbox | 100% | 예약연동납부 [예약일 |
| `check.부담금등록구분` | 부담금등록구분 | checkbox | 100% | 일괄(파일) 신청 |
| `목록[].성명` | 성명 | text | 100% | 김혁예 |
| `목록[].생년월일주1` | 생년월일주1 | text | 100% | 2025-05-02 |
| `목록[].기업부담금` | 기업부담금 | text | 100% | 190,000 |
| `목록[].개인부담금` | 개인부담금 | text | 100% | 15,180,000 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer` | 기업명 | seal | 100% | 이민빈 |
| `sign.signer` | 기업명 | signature | 100% | 박찬연 |

### 퇴직연금 계약해지 신청서(DB,DC) (`hf191`) — 키 35개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `account` | 퇴직연금계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.제도` | 제도 | checkbox | 100% | DB |
| `해지사유` | 해지사유 | text | 100% | 만기 해지 |
| `check.해지사유` | 해지사유 | checkbox | 100% | 사업장의 인수합병 |
| `check.수수료연동출금` | 수수료연동출금**(DC형만해당) | checkbox | 100% | 연동출금 미동의(기업별도입금) |
| `목록[].성명` | 성명 | text | 100% | 김재희 |
| `check.개인형IRP` | 개인형IRP | checkbox | 100% | 요구불계좌 |
| `금융기관명` | 금융기관명 | text | 100% | 카카오뱅크 |
| `account2` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.개인형IRP2` | 개인형IRP | checkbox | 100% | 개인형IRP |
| `금융기관명2` | 금융기관명 | text | 100% | 신한은행 |
| `account3` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `signer.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer` | 성명 | seal | 100% | 현예지 |
| `sign.signer` | 성명 | signature | 100% | 강순준 |
| `목록[].서명또는` | 서명또는(인) | text | 100% |  |
| `signer2.name` | 성명 | text | 100% | 박찬연 |
| `seal.signer2` | 성명 | seal | 100% | 이민빈 |
| `sign.signer2` | 성명 | signature | 100% | 박찬연 |
| `check.만55세이후퇴직` | 만55세이후퇴직 | checkbox | 100% | 만55세이후 퇴직 |
| `check.만55세이후퇴직2` | 만55세이후퇴직 | checkbox | 100% | 만원 이하 퇴직금 지급 |
| `목록[].생년월일` | 생년월일 | date | 100% | 2026년 1월 30일 |
| `목록[].입사일자` | 입사일자 | date | 100% | 2025년 12월 2일 |
| `목록[].잔여부담금` | 잔여부담금(DC형만기재) | number | 100% | 4,760,000 |
| `check.기업반환` | 기업반환(기업반환계좌로반환) | checkbox | 100% | 퇴직소득세 |
| `check.기업반환2` | 기업반환(기업반환계좌로반환) | checkbox | 100% | 계속근로기간 1년 미만 |
| `목록[].중간정산일자` | 중간정산일자 | date | 100% | 2025년 8월 12일 |
| `check.적용` | 적용 | checkbox | 100% | 적용 |
| `check.적용2` | 적용 | checkbox | 100% | 적용 |
| `목록[].퇴직일자` | 퇴직일자 | date | 100% | 2025년 11월 27일 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer3.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer3` | 기업명 | seal | 100% | 강순준 |
| `sign.signer3` | 기업명 | signature | 100% | 박찬연 |

### 퇴직연금 통지서비스 신청서(기업용) (`hf192`) — 키 25개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `check.제도구분` | 제도구분 | checkbox | 100% | DC |
| `주담당자` | 주담당자 | text | 100% | 구승연 |
| `부담당자` | 부담당자 | text | 100% | 정우찬 |
| `목록[].휴대폰번호` | 휴대폰번호 | phone | 100% | 010-5907-7253 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `account` | 퇴직연금계좌번호 | account_no | 100% | 000-287736-52424 |
| `목록[].이메일주소` | 이메일주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `check.상승자동환매` | 상승+%자동환매 | checkbox | 100% | 하락 - % 자동환매 |
| `check.상승자동환매2` | 상승+%자동환매 | checkbox | 100% | 보기2 |
| `check.상승자동환매3` | 상승+%자동환매 | checkbox | 100% | 보기2 |
| `check.운용현황보고서발송주기` | 운용현황보고서발송주기(기본값:분기발송) | checkbox | 100% | 월 |
| `check.원리금보장상품만기도래시전월통지발송` | 원리금보장상품(정기예금등)만기도래시전월통지발송 | checkbox | 100% | 알림톡(LMS) |
| `check.퇴직연금운용및자산관리약관이변경되는경우통지` | 퇴직연금운용및자산관리약관이변경되는경우통지 | checkbox | 100% | 이메일 |
| `check.집합투자증권매수시예탁결제원의자산운용보고서수령방법` | 집합투자증권매수시예탁결제원의자산운용보고서수령방법 | checkbox | 100% | 수령거절 |
| `check.신청안함` | 신청안함 | checkbox | 100% | 알림톡(LMS) |
| `check.매월말전체적립금에대한운용내역을익월초통지` | 매월말전체적립금에대한운용내역을익월초통지 | checkbox | 100% | 신청안함 |
| `check.목표수익률에도달하면펀드자동환매` | 목표수익률에도달하면펀드자동환매 | checkbox | 100% | 등록/변경 |
| `check.신청` | 신청(미발송) | checkbox | 100% | 신청안함(발송) |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer` | 기업명 | seal | 100% | 이욱유 |
| `sign.signer` | 기업명 | signature | 100% | 박찬연 |
| `목표수익률에도달하면펀드자동환매` | 목표수익률에도달하면펀드자동환매 | text | 100% |  |
| `거래내용` | 거래내용 | text | 100% | 자녀 교육비 |

### 퇴직연금 계약해지 신청서(기업형IRP) (`hf193`) — 키 24개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `서류확인및접수확인자` | 서류확인및접수확인자 | text | 100% |  |
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `account` | 퇴직연금계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.해지사유` | 해지사유 | checkbox | 100% | 제도폐지 |
| `check.수수료연동출금` | 수수료연동출금** | checkbox | 100% | 연동출금 동의 (사전에 약정된 경우) |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `check.개인형IRP` | 개인형IRP | checkbox | 100% | 개인형 IRP |
| `금융기관명` | 금융기관명 | text | 100% | 우리은행 |
| `account2` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.birth` | 생년월일 | date | 100% | 1966년 8월 12일 |
| `check.만55세이후퇴직` | 만55세이후퇴직 | checkbox | 100% | 만원 이하 퇴직금 지급 |
| `employer.hire_date` | 입사일자 | date | 100% | 2020.05.08 |
| `중간정산일자` | 중간정산일자 | date | 100% | 2025.07.31 |
| `잔여부담금` | 잔여부담금 | number | 100% | 5,130,000 |
| `check.계좌번호` | 계좌번호 | checkbox | 100% | 계속근로기관 1년 미만 |
| `퇴직일자` | 퇴직일자 | date | 100% | 2025-01-26 |
| `check.적용` | 적용 | checkbox | 100% | 적용 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer` | 기업명 | seal | 100% | 강순준 |
| `sign.signer` | 기업명 | signature | 100% | 박찬연 |
| `signer2.name` | 가입자 | text | 100% | 박찬연 |
| `seal.signer2` | 가입자 | seal | 100% | 박찬연 |
| `sign.signer2` | 가입자 | signature | 100% | 현예지 |

### 퇴직연금 항목등록/변경 신청서 (`hf194`) — 키 28개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명(업체명) | text | 100% | 박찬연 |
| `account` | 계좌번호 | account_no | 100% | 000-287736-52424 |
| `customer.birth` | 생년월일(사업자번호) | date | 100% | 970514 |
| `check.제도구분` | 제도구분 | checkbox | 100% | 개인형IRP |
| `변경전` | 변경전 | text | 100% | 학자금 |
| `check.구분` | 구분 | checkbox | 100% | 등록 |
| `check.공통사항` | 공통사항 | checkbox | 100% | 신탁관리인 변경(추가항목 필수 기재) |
| `check.DB` | DB | checkbox | 100% | 대체상품 매수 동의 |
| `check.DC기업형IRP` | DC/기업형IRP | checkbox | 100% | 운용상품군(자동라인업)등록 |
| `check.공통사항2` | 공통사항 | checkbox | 100% | 기타 ( |
| `check.개인형IRP` | 개인형IRP | checkbox | 100% | 개인형IRP 속성 변경 |
| `변경후` | 변경후 | text | 100% | 전세자금 |
| `check.구분2` | 구분 | checkbox | 100% | 등록 |
| `customer.name2` | 성명 | text | 100% | 박찬연 |
| `customer.birth2` | 생년월일 | date | 100% | 1990년 2월 10일 |
| `check.신청구분` | 신청구분 | checkbox | 100% | 등록 |
| `customer.name3` | 성명 | text | 100% | 박찬연 |
| `customer.phone` | 휴대폰번호 | phone | 100% | 010-5907-7253 |
| `check.담당자구분` | 담당자구분 | checkbox | 100% | 주담당자 |
| `customer.birth3` | 생년월일 | date | 100% | 1990년 2월 10일 |
| `customer.email` | 이메일주소 | text | 100% | chanyeon363@naver.com |
| `기업담당자성명` | 기업담당자성명 | text | 100% | 손상인 |
| `기업담당자휴대폰번호` | 기업담당자휴대폰번호 | phone | 100% | 010-7321-8870 |
| `근로자앞문자발송요청일` | 근로자앞문자발송요청일 | date | 100% | 2025.10.12 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 현예지 |

### 퇴직연금 가입자(등록·변경·삭제) 신청서(DB,DC,기업형IRP) (`hf195`) — 키 43개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `check.퇴직연금가입제도` | 퇴직연금가입제도 | checkbox | 100% | 기업형IRP |
| `account` | 퇴직연금계좌번호 | account_no | 100% | 000-287736-52424 |
| `check.신청구분` | 신청구분 | checkbox | 100% | 등록 |
| `check.신청구분2` | 신청구분 | checkbox | 100% | 변경 |
| `가입자수` | 가입자수 | text | 100% |  |
| `check.가입자` | 가입자 | checkbox | 100% | 가입자 |
| `check.가입자등록구분` | 가입자등록구분 | checkbox | 100% | 개별 신청 |
| `가입자명부산정기준일자` | 가입자명부산정기준일자 | date | 100% | 2024년 11월 2일 |
| `check.기준급여원` | 기준급여:원 | checkbox | 100% | 촉탁 |
| `check.기준급여원2` | 기준급여:원 | checkbox | 100% | 임원 |
| `check.기준급여원3` | 기준급여:원 | checkbox | 100% | 촉탁 |
| `check.기준급여원4` | 기준급여:원 | checkbox | 100% | 임원 |
| `check.기준급여원5` | 기준급여:원 | checkbox | 100% | 정년초과 |
| `check.직원` | 직원 | checkbox | 100% | 직원 |
| `check.직원2` | 직원 | checkbox | 100% | 임원 |
| `check.직원3` | 직원 | checkbox | 100% | 임원 |
| `check.직원4` | 직원 | checkbox | 100% | 임원 |
| `check.직원5` | 직원 | checkbox | 100% | 직원 |
| `check.퇴직일전환일사유` | 퇴직일/전환일:사유 | checkbox | 100% | 선지급(회사지급) |
| `check.퇴직일전환일사유2` | 퇴직일/전환일:사유 | checkbox | 100% | 근속기간1년미만(DB) |
| `check.퇴직일전환일사유3` | 퇴직일/전환일:사유 | checkbox | 100% | 무급부(대표지급)(DB) |
| `check.퇴직일전환일사유4` | 퇴직일/전환일:사유 | checkbox | 100% | 선지급(회사지급) |
| `check.퇴직일전환일사유5` | 퇴직일/전환일:사유 | checkbox | 100% | 기타( |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `사원번호` | 사원번호 | text | 100% | 752-562926-86438 |
| `customer.name2` | 성명 | text | 100% | 박찬연 |
| `customer.rrn2` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `사원번호2` | 사원번호 | rrn | 100% | 395643-1020752 |
| `customer.name3` | 성명 | text | 100% | 박찬연 |
| `customer.rrn3` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `사원번호3` | 사원번호 | text | 100% | 2832-3493 |
| `customer.name4` | 성명 | text | 100% | 박찬연 |
| `customer.rrn4` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `사원번호4` | 사원번호 | text | 100% | 300800-2966865 |
| `customer.name5` | 성명 | text | 100% | 박찬연 |
| `customer.rrn5` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `사원번호5` | 사원번호 | text | 100% | 7606-4272 |
| `signer.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer` | 기업명 | seal | 100% | 박찬연 |
| `sign.signer` | 기업명 | signature | 100% | 이민빈 |

### 기업형IRP 가입대상 근로자 확인서 (`hf196`) — 키 9개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.name` | 기업명 | text | 100% | (주)유니온무역 |
| `company.biz_no` | 사업자번호 | biz_no | 100% | 264-82-36559 |
| `상시근로자수` | (A)상시근로자수 | number | 100% | 6 |
| `명` | 명 | number | 100% | 2 |
| `기업형IRP가입대상근로자수` | (C)=(A)-(B)기업형IRP가입대상근로자수 | number | 100% | 24 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 기업명 | text | 100% | 박찬연 |
| `seal.signer` | 기업명 | seal | 100% | 현예지 |
| `sign.signer` | 기업명 | signature | 100% | 박찬연 |

### 장외파생상품 일반투자자 (부)적정성 판단보고서 (`hf381`) — 키 46개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 고객명 | text | 100% | 박찬연 |
| `customer.birth` | 생년월일및나이 | date | 100% | 1990.02.10 |
| `고객유형` | 고객유형 | text | 100% |  |
| `미성년자고령초고령구분` | 미성년자/고령/초고령구분 | text | 100% |  |
| `check.예` | 예 | checkbox | 100% | 보기1 |
| `check.예2` | 예 | checkbox | 100% | 보기1 |
| `check.예3` | 예 | checkbox | 100% | 보기1 |
| `check.예4` | 예 | checkbox | 100% | 보기1 |
| `check.하` | 하 | checkbox | 100% | 보기1 |
| `check.5미만` | 5%미만 | checkbox | 100% | 보기1 |
| `check.년미만` | 년미만 | checkbox | 100% | 보기1 |
| `check.아니오` | 아니오 | checkbox | 100% | 보기1 |
| `check.아니오2` | 아니오 | checkbox | 100% | 보기1 |
| `check.아니오3` | 아니오 | checkbox | 100% | 보기1 |
| `check.아니오4` | 아니오 | checkbox | 100% | 보기1 |
| `check.중` | 중 | checkbox | 100% | 보기1 |
| `check.10미만` | 10%미만 | checkbox | 100% | 보기1 |
| `check.년미만2` | 년미만 | checkbox | 100% | 보기1 |
| `check.상` | 상 | checkbox | 100% | 보기1 |
| `check.10이상` | 10%이상 | checkbox | 100% | 보기1 |
| `check.년이상` | 년이상 | checkbox | 100% | 보기1 |
| `고객등급` | 고객등급 | text | 100% |  |
| `거래가능상품의위험등급` | 거래가능상품의위험등급 | text | 100% | 하나 적금 |
| `거래목적위험회피목적여부` | 거래목적-위험회피목적여부 | text | 100% | 학자금 |
| `위험의속성및규모에따른적합여부` | 위험의속성및규모에따른적합여부 | text | 100% |  |
| `장외파생상품에대한지식보유정도` | 장외파생상품에대한지식보유정도 | text | 100% | 하나 적금 |
| `장외파생상품을취득처분한경험` | 장외파생상품을취득·처분한경험 | text | 100% | 하나 TDF 2040 |
| `check.적정` | 적정 | checkbox | 100% | 보기1 |
| `check.부적정` | 부적정 | checkbox | 100% | 보기1 |
| `check.미충족항목존재` | 미충족항목존재 | checkbox | 100% | 보기1 |
| `check.상품위험등급대비고객등급미달` | 상품위험등급대비고객등급미달 | checkbox | 100% | 보기1 |
| `check.충족` | 충족 | checkbox | 100% | 보기1 |
| `check.충족2` | 충족 | checkbox | 100% | 보기1 |
| `check.충족3` | 충족 | checkbox | 100% | 보기1 |
| `check.충족4` | 충족 | checkbox | 100% | 보기1 |
| `check.미충족` | 미충족 | checkbox | 100% | 보기1 |
| `check.미충족2` | 미충족 | checkbox | 100% | 보기1 |
| `check.미충족3` | 미충족 | checkbox | 100% | 보기1 |
| `check.미충족4` | 미충족 | checkbox | 100% | 보기1 |
| `항목점수` | 항목점수 | text | 100% |  |
| `거래목적위험회피목적여부2` | 거래목적-위험회피목적여부 | text | 100% | 학자금 |
| `customer.name2` | 고객명 | text | 100% | 박찬연 |
| `agent.name` | 대리인 | text | 100% | 박영준 |
| `담당자` | 담당자(파생상품투자권유자문인력) | text | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |

### 장외파생상품 일반투자자 투자자정보 분석결과표 (`hf382`) — 키 32개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 고객명 | text | 100% | 박찬연 |
| `customer.birth` | 생년월일및나이 | date | 100% | 1990-02-10 |
| `고객유형` | 고객유형 | text | 100% |  |
| `미성년자고령초고령구분` | 미성년자/고령/초고령구분 | text | 100% |  |
| `check.예` | 예 | checkbox | 100% | 보기1 |
| `check.예2` | 예 | checkbox | 100% | 보기1 |
| `check.예3` | 예 | checkbox | 100% | 보기1 |
| `check.예4` | 예 | checkbox | 100% | 보기1 |
| `check.하` | 하 | checkbox | 100% | 보기1 |
| `check.5미만` | 5%미만 | checkbox | 100% | 보기1 |
| `check.년미만` | 년미만 | checkbox | 100% | 보기1 |
| `check.아니오` | 아니오 | checkbox | 100% | 보기1 |
| `check.아니오2` | 아니오 | checkbox | 100% | 보기1 |
| `check.아니오3` | 아니오 | checkbox | 100% | 보기1 |
| `check.아니오4` | 아니오 | checkbox | 100% | 보기1 |
| `check.중` | 중 | checkbox | 100% | 보기1 |
| `check.10미만` | 10%미만 | checkbox | 100% | 보기1 |
| `check.년미만2` | 년미만 | checkbox | 100% | 보기1 |
| `check.상` | 상 | checkbox | 100% | 보기1 |
| `check.10이상` | 10%이상 | checkbox | 100% | 보기1 |
| `check.년이상` | 년이상 | checkbox | 100% | 보기1 |
| `고객등급` | 고객등급 | text | 100% |  |
| `거래가능상품의위험등급` | 거래가능상품의위험등급 | text | 100% | 하나 단기채 펀드 |
| `거래목적위험회피목적여부` | 거래목적-위험회피목적여부 | text | 100% | 학자금 |
| `위험의속성및규모에따른적합여부` | 위험의속성및규모에따른적합여부 | text | 100% |  |
| `장외파생상품에대한지식보유정도` | 장외파생상품에대한지식보유정도 | text | 100% | 하나 MMF |
| `장외파생상품을취득처분한경험` | 장외파생상품을취득·처분한경험 | text | 100% | 하나 MMF |
| `customer.name2` | 고객명 | text | 100% | 박찬연 |
| `agent.name` | 대리인 | text | 100% | 박영준 |
| `담당자` | 담당자(파생상품투자권유자문인력) | text | 100% | 강순준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |

### 장외파생상품 투자성향에 적정하지 않은 거래확인서 (`hf383`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `고객등급` | 고객등급 | text | 100% |  |
| `거래가능상품의위험등급` | 거래가능상품의위험등급 | text | 100% | 하나 적금 |
| `거래희망상품명` | 거래희망상품명 | text | 100% | 플라스틱 원료 |
| `거래희망상품의위험등급` | 거래희망상품의위험등급 | text | 100% | 하나 TDF 2040 |
| `customer.name` | 본인 | text | 100% | 박찬연 |
| `customer.name2` | 고객명 | text | 100% | 박찬연 |
| `agent.name` | 대리인 | text | 100% | 박영준 |
| `담당자` | 담당자(파생상품투자권유자문인력) | text | 100% | 정혁유 |
| `영업점장` | 영업점장(파생상품영업관리자) | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |

### 장외파생상품 일반투자자 투자자정보 확인서(법인 및 개인사업자 고객용) (`hf384`) — 키 59개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.비상장기업` | 비상장기업 | checkbox | 100% | 보기1 |
| `상장거래소명` | 상장거래소명 | text | 100% |  |
| `상장거래소명2` | 상장거래소명 | text | 100% |  |
| `종목코드` | 종목코드 | number | 100% | 747546 |
| `check.선택` | 선택 | checkbox | 100% | 상장거래소명 |
| `자산총계` | 자산총계 | text | 100% |  |
| `부채총계` | 부채총계 | text | 100% |  |
| `check.보기1` | 보기1 | checkbox | 100% | 보기1 |
| `check.` | □ | checkbox | 100% | □ |
| `check[]` | □ | checkbox | 100% | □ |
| `check.보기12` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기13` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기14` | 보기1 | checkbox | 100% | 보기1 |
| `check.선택2` | 선택 | checkbox | 100% | □ |
| `check.개월이하` | 개월이하 | checkbox | 100% | □ |
| `check.개월이하2` | 개월이하 | checkbox | 100% | □ |
| `check.년이하` | 년이하 | checkbox | 100% | □ |
| `check.보기15` | 보기1 | checkbox | 100% | 보기1 |
| `하금융투자상품에투자해본경험이없음` | 하:금융투자상품에투자해본경험이없음 | text | 100% | 하나 TDF 2040 |
| `employer.department` | 소속부서 | text | 100% | 법무팀 |
| `관련경력` | 관련경력 | text | 100% |  |
| `employer.position` | 직급 | text | 100% | 대리 |
| `관련자격` | 관련자격 | text | 100% |  |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `check.보기16` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기17` | 보기1 | checkbox | 100% | 보기1 |
| `check.하금융투자상품에투자해본경험이없음` | 하:금융투자상품에투자해본경험이없음 | checkbox | 100% | 보기1 |
| `하금융투자상품에투자해본경험이없음2` | 하:금융투자상품에투자해본경험이없음 | text | 100% | 하나 정기예금 |
| `employer.department2` | 소속부서 | text | 100% | 구매팀 |
| `관련경력2` | 관련경력 | text | 100% |  |
| `employer.position2` | 직급 | text | 100% | 대리 |
| `관련자격2` | 관련자격 | text | 100% |  |
| `customer.name2` | 성명 | text | 100% | 박찬연 |
| `check.보기18` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기19` | 보기1 | checkbox | 100% | 보기1 |
| `check.하금융투자상품에투자해본경험이없음2` | 하:금융투자상품에투자해본경험이없음 | checkbox | 100% | 보기1 |
| `check.보기110` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기111` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기112` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기113` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기114` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기115` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기116` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기117` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기118` | 보기1 | checkbox | 100% | 보기1 |
| `check.거래경험있음` | 거래경험있음 | checkbox | 100% | □ |
| `check.년미만` | 년미만 | checkbox | 100% | □ |
| `check.년이상3년미만` | 년이상~3년미만 | checkbox | 100% | □ |
| `check.예` | 예 | checkbox | 100% | □ |
| `check.아니오` | 아니오 | checkbox | 100% | 규정명 |
| `구조화통화옵션` | 구조화통화옵션(ExoticFXOption) | text | 100% | CNY |
| `규모에비추어적합합니까` | 규모에비추어적합합니까? | text | 100% |  |
| `업무절차보유여부` | 업무절차보유여부 | text | 100% |  |
| `check.보기119` | 보기1 | checkbox | 100% | 보기1 |
| `customer.name3` | 고객명 | text | 100% | 박찬연 |
| `agent.name` | 대리인 | text | 100% | 박영준 |
| `담당자` | 담당자(파생상품투자권유자문인력) | text | 100% | 진경희 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |

### 장외파생상품 일반투자자 투자자정보 확인서(개인 고객용) (`hf385`) — 키 35개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `자산총계` | 자산총계 | text | 100% |  |
| `부채총계` | 부채총계 | text | 100% |  |
| `check.보기1` | 보기1 | checkbox | 100% | 보기1 |
| `check.` | □ | checkbox | 100% | □ |
| `check[]` | □ | checkbox | 100% | □ |
| `check.보기12` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기13` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기14` | 보기1 | checkbox | 100% | 보기1 |
| `check.선택` | 선택 | checkbox | 100% | □ |
| `check.개월이하` | 개월이하 | checkbox | 100% | □ |
| `check.개월이하2` | 개월이하 | checkbox | 100% | □ |
| `check.년이하` | 년이하 | checkbox | 100% | □ |
| `check.보기15` | 보기1 | checkbox | 100% | 보기1 |
| `하금융투자상품에투자해본경험이없음` | 하:금융투자상품에투자해본경험이없음 | text | 100% | 하나 TDF 2040 |
| `check.보기16` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기17` | 보기1 | checkbox | 100% | 보기1 |
| `check.하금융투자상품에투자해본경험이없음` | 하:금융투자상품에투자해본경험이없음 | checkbox | 100% | 보기1 |
| `check.보기18` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기19` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기110` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기111` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기112` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기113` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기114` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기115` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기116` | 보기1 | checkbox | 100% | 보기1 |
| `check.거래경험있음` | 거래경험있음 | checkbox | 100% | □ |
| `check.년미만` | 년미만 | checkbox | 100% | □ |
| `check.년이상3년미만` | 년이상~3년미만 | checkbox | 100% | □ |
| `구조화통화옵션` | 구조화통화옵션(ExoticFXOption) | text | 100% | USD |
| `규모에비추어적합합니까` | 규모에비추어적합합니까? | text | 100% |  |
| `customer.name` | 고객명 | text | 100% | 박찬연 |
| `담당자` | 담당자(파생상품투자권유자문인력) | text | 100% | 우민준 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `date2` | 작성일 | date | 100% | 2026년 1월 31일 |

### 외환파생상품거래 헤지 수요 현황 및 거래 실행에 따른 확인서 (`hf386`) — 키 20개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.해당` | (해당 | checkbox | 100% | 란에 체크 |
| `check.기타` | 기타(향후예상경상/재무거래등) | checkbox | 100% | 기타 (향후 예상 경상/재무거래 등) |
| `check.택일` | 택일 | checkbox | 100% | 과거 수출입 실적기준 |
| `check.택일2` | 택일 | checkbox | 100% | 개별 계약건별 기준 |
| `택일_목록[].수출` | 수출(투자포함) | text | 100% |  |
| `수출` | 수출(투자포함) | text | 100% |  |
| `헤지대상금액합계` | 헤지대상금액합계(헤지비율분모에해당) | number | 100% | 8,620,000 |
| `통화선도` | 통화선도(외환스왑,NDF포함) | text | 100% | EUR |
| `통화옵션` | 통화옵션 | text | 100% | CNY |
| `통화스왑` | 통화스왑 | text | 100% | AUD |
| `환변동보험및기타` | 환변동보험및기타() | text | 100% | 만기 해지 |
| `기헤지거래금액합계` | 기헤지거래금액합계(헤지비율분자에해당) | number | 100% | 6,350,000 |
| `택일_목록[].수입` | 수입(조달포함) | text | 100% |  |
| `목록[].수입` | 수입(조달포함) | text | 100% |  |
| `기체결외환파생상품거래금액_목록[].수입` | 수입(조달포함) | text | 100% |  |
| `택일_목록[].비고` | 비고 | text | 100% | 주택구입 |
| `목록[].비고` | 비고 | text | 100% | 생활자금 |
| `기체결외환파생상품거래금액_목록[].비고` | 비고 | text | 100% | 투자 목적 |
| `거래금액` | 거래금액 | number | 100% | 46,980,000 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### HANA FX TRADING SYSTEM 자동결제 이용신청서 (`hf387`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `원화계좌_목록[].통화` | 통화 | text | 100% | EUR |
| `외화계좌_목록[].통화` | 통화 | text | 100% | USD |
| `원화계좌_목록[].계좌번호` | 계좌번호 | text | 100% | 915-014977-34907 |
| `외화계좌_목록[].계좌번호` | 계좌번호 | text | 100% | 027-377289-13112 |
| `원화계좌_목록[].통장용인감` | 통장용인감(서명) | text | 100% |  |
| `외화계좌_목록[].통장용인감` | 통장용인감(서명) | text | 100% |  |
| `check.신청` | 신청 | checkbox | 100% | 해지 |
| `check.신청2` | 신청 | checkbox | 100% | 해지 |
| `check.신청3` | 신청 | checkbox | 100% | 신청 |
| `check.신청4` | 신청 | checkbox | 100% | 해지 |
| `check.신청5` | 신청 | checkbox | 100% | 해지 |
| `check.신청6` | 신청 | checkbox | 100% | 해지 |
| `check.신청7` | 신청 | checkbox | 100% | 신청 |
| `check.신청8` | 신청 | checkbox | 100% | 신청 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `check.HANAFXTRADINGSYSTEM일괄예약결제` | ■HANAFXTRADINGSYSTEM일괄예약결제 | checkbox | 100% | 미신청 |

### HANA FX TRADING SYSTEM 이용신청서 (`hf388`) — 키 18개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `employer.name` | 회사명 | text | 100% | 주식회사 태평양무역 |
| `company.biz_no` | 사업자등록번호 | biz_no | 100% | 264-82-36559 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `company.ceo` | 대표자 | text | 100% | 박찬연 |
| `대표전화번호` | 대표전화번호 | phone | 100% | 010-5907-7253 |
| `현물환거래한도` | 현물환거래한도 | number | 100% | 5,360,000 |
| `check.신청구분` | 신청구분 | checkbox | 100% | 해지 |
| `아이디` | 아이디(ID) | text | 100% |  |
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `부서직위` | 부서/직위 | text | 100% |  |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `check.신청` | 신청 | checkbox | 100% | 해지 |
| `check.신청2` | 신청 | checkbox | 100% | 해지 |
| `check.신청3` | 신청 | checkbox | 100% | 신청 |
| `취급점` | 취급점 | text | 100% | 범어지점 |
| `check.동의하십니까` | 동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `개인정보` | ■개인(신용)정보 | text | 100% |  |

### 위임장(장외파생상품 일반투자자용) (`hf389`) — 키 9개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 이름 | text | 100% | 박찬연 |
| `customer.birth` | 생년월일 | date | 100% | 900210 |
| `customer.address` | 주소 | text | 100% | 경상남도 창원시 성산구 원이대로 262-29, 104호 |
| `agent.relation` | 본인과의관계 | text | 100% | 부 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `customer.name2` | 고객명(위임인) | text | 100% | 박찬연 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `본인의투자성향파악여부에대한의사결정` | -본인의투자성향파악여부에대한의사결정 | text | 100% |  |
| `본인의투자성향분석결과를확인하는행위` | -본인의투자성향분석결과를확인하는행위 | text | 100% |  |

### 매매내역 등의 통지방법에 대한 고객확인서(장외파생상품) (`hf390`) — 키 17개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].담당자명` | 담당자명 | text | 100% | 도준찬 |
| `목록[].부서및직급` | 부서및직급 | text | 100% |  |
| `목록[].전화번호` | 전화번호 | text | 100% | 010-5907-7253 |
| `check.전화번호` | 전화번호 | checkbox | 100% | 팩스 |
| `check.이메일` | 이메일 | checkbox | 100% | 이메일 |
| `check.기타` | 기타 | checkbox | 100% | 기타 |
| `check.V원하는항목의박스에체크` | V원하는항목의박스에체크 | checkbox | 100% | V 원하는 항목의 박스에 체크 |
| `check.수령` | 수령 | checkbox | 100% | 수령 |
| `customer.address` | 주소(필수,상세주소명기) | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `팩스` | 팩스(선택) | phone | 100% | 010-5907-7253 |
| `customer.email` | 이메일(선택) | text | 100% | chanyeon363@naver.com |
| `check.수령거부` | 수령거부 | checkbox | 100% | 수령거부 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | (고객명) | text | 100% | 박찬연 |
| `seal.signer` | (고객명) | seal | 100% | 박찬연 |
| `sign.signer` | (고객명) | signature | 100% | 강순준 |
| `value` | (법인등록번호/생년월일) | amount | 100% |  |

### 고령투자자확인서(장외파생상품용) (`hf391`) — 키 7개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `일반개인정보` | ■일반개인정보 | text | 100% |  |
| `check.위개인신용정보수집이용에동의하십니까` | 위개인신용정보수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `check.조력자연락처제공` | [조력자방문]조력자연락처제공 | checkbox | 100% | [조력자 방문] 조력자 연락처 제공 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `조력자연락처작성` | ■[조력자방문]조력자연락처작성 | text | 100% |  |
| `장외파생상품만기일까지보유이용` | -장외파생상품만기일까지보유·이용 | text | 100% |  |
| `거래목적및숙려기간제외대상사전확인` | ■거래목적및숙려기간제외대상사전확인 | text | 100% |  |

### 초고령투자자확인서(장외파생상품용) (`hf392`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `check.조력자연락처제공` | [조력자방문]조력자연락처제공 | checkbox | 100% | [조력자 방문] 조력자 연락처 제공 |
| `check.수집이용에동의하십니까` | 수집·이용에동의하십니까? | checkbox | 100% | 동의하지 않음 |
| `조력자연락처` | 조력자연락처 | phone | 100% | 010-5907-7253 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `조력자연락처작성` | ■[조력자방문]조력자연락처작성 | text | 100% |  |
| `조력자와고객과의관계` | 조력자와고객과의관계 | text | 100% |  |
| `장외파생상품거래불가` | ■[조력자미방문]장외파생상품거래불가 | text | 100% |  |
| `거래목적및숙려기간제외대상사전확인` | ■거래목적및숙려기간제외대상사전확인 | text | 100% |  |

### 이자율스왑 연계 대출 분할상환 원금 및 이자율스왑 정산이자 출금서비스 특약 (`hf393`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `여신과목` | 여신과목 | text | 100% | 일반자금대출 |
| `여신개시일` | 여신개시일 | date | 100% | 2025.12.30 |
| `여신금액` | 여신(한도)금액 | number | 100% | 4,160,000 |
| `여신기간만료일` | 여신기간만료일 | date | 100% | 2025.06.19 |
| `거래일` | 거래일 | date | 100% | 2025.04.08 |
| `발효일` | 발효일 | date | 100% | 2025년 1월 25일 |
| `지급고정금리` | 지급고정금리 | number | 100% | 2.57 |
| `금액` | 금액 | number | 100% | 207,330,000 |
| `종료일` | 종료일 | date | 100% | 2027.03.22 |
| `수취변동금리` | 수취변동금리 | number | 100% | 6.55 |
| `account` | 출금계좌번호 | account_no | 100% | 000-287736-52424 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 강순준 |
| `sign.signer` | 신청인 | signature | 100% | 박찬연 |

### 적정성원칙 투자자확인서 (`hf394`) — 키 3개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `A등급` | A등급 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `법인등록번호생년월일` | 법인등록번호/생년월일 | date | 100% | 2025.09.20 |

### 금융거래정보이용제공동의서(영문) (`hf397`) — 키 9개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `KEBHanaBank` | KEBHanaBank | text | 100% |  |
| `NameNameoftheCorporation` | Name/NameoftheCorporation | text | 100% |  |
| `customer.address` | Address | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `Consentedby` | Consentedby | text | 100% |  |
| `CustomerWhoConsents` | CustomerWhoConsents | text | 100% |  |
| `FinancialCompanies` | FinancialCompanies, | text | 100% |  |
| `etcWhichWillProvide` | etc.WhichWillProvide | text | 100% |  |
| `toWhichTransaction` | toWhichTransaction | text | 100% |  |
| `Signedon` | Signedon | text | 100% |  |

### 금융거래정보이용제공동의서 (`hf398`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `주식회사하나은행` | 주식회사하나은행 | text | 100% | 신한은행 |
| `거래정보저장소` | 거래정보저장소(한국거래소) | text | 100% |  |
| `법인명이름` | 법인명/이름 | text | 100% | 주식회사 한빛패션 |
| `명의인의인적사항사업자등록증번호생년월일` | 명의인의인적사항사업자등록증번호/생년월일 | date | 100% | 2025-07-02 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `seal.signer` | 서명또는 | seal | 100% | 박찬연 |
| `sign.signer` | 서명또는 | signature | 100% | 현예지 |
| `명의인에대한정보` | 명의인에대한정보 | text | 100% | 선성빈 |
| `금융거래관련정보` | 금융거래관련정보 | text | 100% |  |
| `법령및금융투자업규정에따른보고의무이행` | 법령및금융투자업규정에따른보고의무이행 | text | 100% |  |
| `일로동의를철회할수있음` | 일로동의를철회할수있음 | text | 100% |  |
| `으로봄` | 으로봄 | text | 100% |  |

### 파생상품거래 손실한도 초과 및 증거담보 요청 통지서 (`hf399`) — 키 9개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `company.ceo` | [수신]대표이사 | text | 100% | 박찬연 |
| `company.name` | 상호 | text | 100% | (주)유니온무역 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `참조` | 참조 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer.name` | 상호:주식회사하나은행 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호:주식회사하나은행 | seal | 100% | (주)그린케미칼 |
| `sign.signer` | 상호:주식회사하나은행 | signature | 100% | (주)유니온무역 |

### 파생상품거래 손실한도 감액통지서 (`hf400`) — 키 8개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `signer.name` | 상호 | text | 100% | (주)유니온무역 |
| `seal.signer` | 상호 | seal | 100% | 주식회사 대성패션 |
| `sign.signer` | 상호 | signature | 100% | (주)유니온무역 |
| `signer2.name` | 상호:주식회사하나은행 | text | 100% | (주)유니온무역 |
| `seal.signer2` | 상호:주식회사하나은행 | seal | 100% | (주)유니온무역 |
| `sign.signer2` | 상호:주식회사하나은행 | signature | 100% | 주식회사 대성패션 |

### 전문투자자 전환신청서 (`hf401`) — 키 12개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `전문투자자확인증보유자` | 전문투자자확인증보유자 | text | 100% |  |
| `등록번호` | 등록번호 | text | 100% | 3873-7667 |
| `발급일자` | 발급일자 | date | 100% | 2025.03.25 |
| `유효기간` | 유효기간 | text | 100% |  |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.name` | 고객명 | text | 100% | 박찬연 |
| `company.ceo` | 대표이사 | text | 100% | 박찬연 |
| `법인등록번호생년월일` | 법인등록번호/생년월일(고객번호) | date | 100% | 2025.07.20 |
| `signer.name` | 신청담당자성명 | text | 100% | 박찬연 |
| `seal.signer` | 신청담당자성명 | seal | 100% | 김소윤 |
| `sign.signer` | 신청담당자성명 | signature | 100% | 박찬연 |
| `신청담당자생년월일` | 신청담당자생년월일 | date | 100% | 2025.02.27 |

### 장외파생상품 거래 담당자 지정 통지서 (`hf402`) — 키 11개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `목록[].성명` | 성명 | text | 100% | 구동현 |
| `목록[].소속부서및직급` | 소속부서및직급 | text | 100% |  |
| `목록[].생년월일` | 생년월일 | text | 100% | 2025-02-20 |
| `목록[].인감` | 인감(서명) | text | 100% |  |
| `목록[].권한의제한` | 권한의제한 | text | 100% |  |
| `목록[].전화번호팩스번호` | 전화번호&팩스번호 | text | 100% | 043-783-2775 |
| `목록[].비고` | 비고 | text | 100% | 해외 이주 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `company.name` | 법인명 | text | 100% | (주)유니온무역 |
| `company.ceo` | 대표이사 | text | 100% | 박찬연 |
| `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 100% | 200112-7448551 |

### 일반투자자 전환신청서 (`hf403`) — 키 10개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.nationality` | 국적 | text | 100% | 대한민국 |
| `주권상장거래소명` | 주권상장거래소명 | text | 100% |  |
| `설립근거법` | 설립근거법 | text | 100% |  |
| `customer.name` | 고객명 | text | 100% | 박찬연 |
| `company.ceo` | 대표이사 | text | 100% | 박찬연 |
| `법인등록번호생년월일` | 법인등록번호/생년월일(고객번호) | date | 100% | 2024.09.22 |
| `signer.name` | 신청담당자성명 | text | 100% | 박찬연 |
| `seal.signer` | 신청담당자성명 | seal | 100% | 박찬연 |
| `sign.signer` | 신청담당자성명 | signature | 100% | 이민빈 |
| `신청담당자생년월일` | 신청담당자생년월일 | date | 100% | 2024.08.10 |

### 외환파생상품 거래 금액 확인서 (`hf405`) — 키 13개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `통화선도` | 통화선도(외환스왑,NDF포함) | text | 100% | CNY |
| `통화옵션` | 통화옵션 | text | 100% | EUR |
| `통화스왑` | 통화스왑 | text | 100% | EUR |
| `환변동보험` | 환변동보험 | text | 100% |  |
| `통화선도2` | 통화선도(외환스왑,NDF포함) | text | 100% | USD |
| `통화옵션2` | 통화옵션 | text | 100% | USD |
| `통화스왑2` | 통화스왑 | text | 100% | USD |
| `환변동보험2` | 환변동보험 | text | 100% |  |
| `헤지거래한도` | 헤지거래한도(a) | number | 100% | 290,000 |
| `기체결외환파생거래금액` | 기체결외환파생거래금액(b) | number | 100% | 14,250,000 |
| `금번거래예정금액` | 금번거래예정금액(c) | number | 100% | 136,270,000 |
| `위험헤지비율100` | 위험헤지비율((b+c)/(a)*100) | number | 100% | 30 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |

### 위임장(집합투자증권 및 연금저축계좌 투자용) (`hf197`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `customer.birth` | 생년월일 | date | 100% | 1990년 2월 10일 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `agent.relation` | 본인과의관계 | text | 100% | 부 |
| `customer.phone` | 연락처 | phone | 100% | 010-5907-7253 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `customer.birth2` | 생년월일/사업자번호 | date | 100% | 1990년 2월 10일 |
| `customer.address2` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `customer.phone2` | 연락처 | phone | 100% | 010-5907-7253 |
| `signer.name` | 직원명 | text | 100% | 박찬연 |
| `seal.signer` | 직원명 | seal | 100% | 현예지 |
| `sign.signer` | 직원명 | signature | 100% | 박찬연 |
| `본인의투자성향파악여부에대한의사결정` | -본인의투자성향파악여부에대한의사결정 | text | 100% |  |
| `본인의투자성향분석결과를확인하는행위` | -본인의투자성향분석결과를확인하는행위 | text | 100% |  |
| `신규외기타위임거래를구체적으로명시` | 신규외기타위임거래를구체적으로명시 | text | 100% |  |

### 공모부동산집합투자증권 과세특례신청서 (`hf198`) — 키 15개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `customer.name` | 성명 | text | 100% | 박찬연 |
| `check.보기1` | 보기1 | checkbox | 100% | 보기1 |
| `check.보기12` | 보기1 | checkbox | 100% | 보기1 |
| `금융기관펀드계좌번호` | 금융기관펀드계좌번호 | text | 100% | 869-918596-51054 |
| `투자대상` | 투자대상(펀드명) | text | 100% |  |
| `투자금액` | 투자금액(투자한도금액) | number | 100% | 150,000 |
| `customer.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 |
| `date` | 작성일 | date | 100% | 2026년 1월 31일 |
| `signer.name` | 신청인 | text | 100% | 박찬연 |
| `seal.signer` | 신청인 | seal | 100% | 박찬연 |
| `sign.signer` | 신청인 | signature | 100% | 현예지 |
| `signer2.name` | 대리인 | text | 100% | 여기준 |
| `seal.signer2` | 대리인 | seal | 100% | 여기준 |
| `sign.signer2` | 대리인 | signature | 100% |  |
| `customer.birth` | 생년월일:... | date | 100% | 1990-02-10 |
