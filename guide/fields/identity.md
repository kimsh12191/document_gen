# 신원·신분 — 서류별 항목

키 규칙과 타입은 [README.md](README.md)에 있습니다.


## 주민등록증 (`resident_id_card`) — 키 8개

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

## 운전면허증 (`driver_license`) — 키 12개

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

## 여권 (`passport`) — 키 15개

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

## 외국인등록증 (`alien_registration_card`) — 키 8개

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

## 인감증명서 (`seal_certificate`) — 키 20개

| 키 | 항목명 | 타입 | 채움률 | 예시 |
|---|---|---|---|---|
| `doc_no` | 인감증명서발급사실확인용번호 | text | 100% | 7043-3278-9148 |
| `applicant_type` | 발급구분 | checkbox | 100% | 보기: 본인 / 대리인 |
| `seal.registered` | 등록인감 | seal | 100% | 박찬연인 |
| `seal_name` | 인감 | text | 100% | 박찬연인 |
| `person.name` | 성명 | text | 100% | 박찬연 |
| `person.name_hanja` | 한자 | text | 100% | 朴讚姸 |
| `person.rrn` | 주민등록번호 | rrn | 100% | 900210-1659382 |
| `person.nationality` | 국적 | text | 100% | 대한민국 |
| `person.address` | 주소 | text | 100% | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센… |
| `usage_type` | 용도 | checkbox | 100% | 보기: 일반용 / 부동산 매도용 |
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

## 본인서명사실확인서 (`signature_confirmation`) — 키 15개

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
| `real_estate_usage` | 부동산관련용도및자동차매도용도 | checkbox | 60% | 보기: 소유권 이전(매매, 증여 등) / 제한물권 설정(근저당권 설정, 전세권 설정 등) / 그 밖의 용도(가등기 설정, 가등기 말소 등) |
| `counterparty.name` | 성명(법인명) | text | 57% | 이서우 |
| `counterparty.rrn` | 주민등록번호(법인등록번호) | rrn | 57% | 930301-2699865 |
| `counterparty.address` | 주소 | text | 57% | 전라남도 여수시 시청로 126, 115동 1503호 |
| `delegate.name` | 성명 | text | 10% | 엄주영 |
| `delegate.address` | 주소 | text | 10% | 서울특별시 종로구 자하문로 92, 114동 504호 |
