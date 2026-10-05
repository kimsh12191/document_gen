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
