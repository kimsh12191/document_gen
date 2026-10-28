# 가족관계 — 서류별 항목

키 규칙과 타입은 [README.md](README.md)에 있습니다.


## 주민등록표 등본 (`resident_registration_copy`) — 키 26개

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

## 주민등록표 초본 (`resident_registration_abstract`) — 키 23개

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

## 가족관계증명서 (`family_relation_certificate`) — 키 26개

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

## 기본증명서 (`basic_certificate`) — 키 33개

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

## 혼인관계증명서 (`marriage_relation_certificate`) — 키 36개

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
