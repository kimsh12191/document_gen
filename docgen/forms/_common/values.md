# 생성 방법 목록 (fields.json 의 source)

<!-- 자동 생성: python -m docgen.formdir values · 코드(docgen/sources.py, docgen/keyrules.py, docgen/entities.py)에서 만든다 -->

서식 칸 목록 `fields.json` 의 `"source"` 에 쓰는 것. 칸 하나의 값을 문서를 그릴 때마다 여기서 만든다.
칸끼리 관계(합계·날짜 순서·조건)는 생성 방법이 아니라 서식 폴더의 `generate.py` 로 맞춘다 (html·overlay 모두, overlay 견본 `python -m docgen.formdir adjust <ID> --new`).
날짜·금액의 표기는 칸의 `"fmt"` (아래 '표기'), 표 묶음의 채우는 행 수는 표 칸의 `"fill"` (few·half·full·any).

## 특별한 것

| source | 값 |
|---|---|
| `rule:choice` | 칸의 `choices` 목록에서 하나 |
| `rule:fixed` | 칸의 `text` 그대로 |
| `rule:free_text` | 짧은 자유 기재 문장 (가끔 빈 칸) |
| `rule:empty` | 늘 빈 칸 |
| `rule:date_seq` | 반복 행에서 행마다 늘어나는 날짜 (`span_days`, `step_days`) |
| `rule:pattern` | 칸의 `pattern` 틀로: `#` 숫자, `A` 대문자, `a` 소문자, `{가\|나}` 하나 고르기 (예: `HN-####-{A\|B}`) |
| `code` | (코드 서식) 값 만드는 함수 generate.py 가 만든 값 그대로 |

## 값 종류 `rule:<종류>` — 코드로 만드는 것 (docgen/realform.py Values.by_kind)

| source | 값 |
|---|---|
| `rule:text` | 자유 글자 (값 출처가 없으면 비움) |
| `rule:date` | 날짜 (만기·기한이면 앞날짜) |
| `rule:amount` | 원화 금액 |
| `rule:fx_amount` | 통화 + 외화 금액 |
| `rule:percent` | 비율·이율 |
| `rule:rate` | 환율 |
| `rule:currency` | 통화 코드 |
| `rule:account` | 국내 계좌번호 |
| `rule:number` | 번호·코드 |
| `rule:count` | 수량·건수·기간 |
| `rule:biz_no` | 사업자등록번호 |
| `rule:passport` | 여권번호 |
| `rule:check_no` | 수표·어음 번호 |
| `rule:goods` | 품목 |
| `rule:product` | 금융 상품명 |
| `rule:check_kind` | 수표 종류 |
| `rule:loan_subject` | 대출 과목 |
| `rule:repay` | 상환 방법 |
| `rule:reason` | 사유·목적 (일부 자유 기재) |
| `rule:bank` | 은행 |
| `rule:branch` | 지점 |
| `rule:country` | 국가 |
| `rule:address` | 주소 |
| `rule:email` | 이메일 |
| `rule:phone` | 전화번호 |
| `rule:company` | 회사명 |
| `rule:person` | 사람 이름 |
| `rule:other_person` | 고객이 아닌 사람 이름 (발급기관 담당자·은행 직원 등) |
| `rule:office_phone` | 기관·회사 일반전화 |
| `rule:note` | 비고 (해당 없음·일부 자유 기재) |

## 값 종류 `rule:<종류>` — 공통 값 종류 (key_rules.json 의 kinds, 파일로 고침)

| source | 뜻 | 만드는 법 |
|---|---|---|
| `rule:swift` | SWIFT(BIC) 코드 | 프로필 `foreign.swift` |
| `rule:iban` | IBAN (국가 2자 + 검사 2자리 + 계좌) | 틀 `{DE|NL|GB|FR|CH|BE}## #### #### #### ##` |
| `rule:incoterms` | 인코텀즈 2020 | 보기 FOB, CIF, CFR, EXW, FCA, DAP |
| `rule:hs_code` | HS 코드 10자리 | 틀 `####.##-####` |
| `rule:port` | 항구 (영문) | 보기 BUSAN, KOREA, INCHEON, KOREA, SHANGHAI, CHINA, LOS ANGELES, USA, HAMBURG, GERMANY, ROTTERDAM, NETHERLANDS |
| `rule:vessel` | 선박명 + 항차 | 틀 `{HMM|EVER|MSC|STAR|SEA} {ALGECIRAS|GIVEN|OSCAR|PIONEER|DREAM} ###{E|W|N|S}` |
| `rule:transfer_day` | 자동이체일(매월) | 보기 5일, 10일, 15일, 20일, 25일 |
| `rule:payday` | 급여일 | 보기 10일, 25일, 말일 |
| `rule:user_id` | 인터넷뱅킹 이용자ID(영문/숫자 6~15자) | 보기 hana2025, kimsh82, leewk1025, parkjy77, choi0315, jhlee2024 |
| `rule:contract_period` | 예금 계약기간 | 보기 12개월, 6개월, 24개월, 36개월 |
| `rule:sell_order` | 매도순위 | 보기 1, 2, 3, 4 |
| `rule:age_years` | 나이(세) | 보기 41, 47, 52, 56, 61 |
| `rule:job_position` | 직업 및 직위 | 보기 회사원/대표이사, 회사원/이사, 자영업/대표, 회사원/부장 |
| `rule:guarantor_relation` | 보증인과 차주(법인)와의 관계 | 보기 대표이사, 이사, 실제경영자, 최대주주, 배우자 |
| `rule:interest_timing` | 이자지급시기 | 보기 매월 후취, 매월 선취, 3개월마다 후취, 만기 일시 |
| `rule:payment_terms` | 결제조건 | 보기 L/C AT SIGHT, USANCE L/C 90 DAYS, D/P, D/A 60 DAYS, T/T IN ADVANCE |
| `rule:relation_en` | 본인과의 관계(영문) | 보기 Spouse, Son, Daughter, Parent, Sibling |
| `rule:poa_power_en` | 위임 업무 상세(영문) | 보기 Inquiry of account balance and transaction history, Reissue of bankbook, Issuance of balance certificate, Withdrawal of deposit |

## 직접 만든 생성기 `rule:<함수>` — 코드 (docgen/forms/_common/generators.py, 설명 docgen/usergen.py)

| source | 뜻 | 설명 |
|---|---|---|
| `rule:card_masked` | 카드번호 (가운데 가림) | 1234-56**-****-7890 꼴 |
| `rule:txn_memo` | 거래 적요 | 입출금 내역의 적요 (이체·급여·카드대금 …), 고객 이름이 들어가기도 |
| `rule:rrn_masked` | 주민등록번호 (뒷자리 가림) | 900210-1****** 꼴, 고객 본인 |

## 표기 (칸의 `fmt`) — 값을 이 꼴로 바꿔 적는다 (읽지 못하는 값은 그대로)

| fmt | 뜻 | 예 |
|---|---|---|
| `date.dot` | 날짜 2025.01.31 | 2025.01.31 |
| `date.dash` | 날짜 2025-01-31 | 2025-01-31 |
| `date.slash` | 날짜 2025/01/31 | 2025/01/31 |
| `date.kor` | 날짜 2025년 01월 31일 | 2025년 01월 31일 |
| `date.kor_short` | 날짜 2025년 1월 31일 | 2025년 1월 31일 |
| `date.yymmdd` | 날짜 250131 (6자리) | 250131 |
| `date.yyyymmdd` | 날짜 20250131 (8자리) | 20250131 |
| `date.yy_dot` | 날짜 25.01.31 | 25.01.31 |
| `amount.comma` | 금액 1,234,000 | 1,234,000 |
| `amount.won` | 금액 1,234,000원 | 1,234,000원 |
| `amount.plain` | 금액 1234000 (쉼표 없음) | 1234000 |
| `amount.korean` | 금액 일백이십삼만사천원 | 일백이십삼만사천원 |
| `amount.korean_full` | 금액 일금 일백이십삼만사천원정 | 일금 일백이십삼만사천원정 |
| `digits.plain` | 숫자만 (- 빼기: 01012345678) | 01012345678 |
| `text.upper` | 영문 대문자 | HONG GILDONG |

## 고객 프로필 `profile.<경로>` (예시 값은 seed 0 고객)

한 문서·한 업무 묶음 안에서 같은 사람의 값이 서로 맞아야 하면 이쪽 (성명·주민번호·주소·직장 …).

| source | 예시 |
|---|---|
| `profile.seed` | 0 |
| `profile.issue_date` | 2026.01.31 |
| `profile.person.name` | 박찬연 |
| `profile.person.hanja` | 朴讚姸 |
| `profile.person.surname_en` | PARK |
| `profile.person.given_en` | CHANYEON |
| `profile.person.gender` | M |
| `profile.person.birth` | 1990.02.10 |
| `profile.person.rrn` | 900210-1659382 |
| `profile.person.address.sido` | 서울특별시 |
| `profile.person.address.sigungu` | 서초구 |
| `profile.person.address.dong` | 방배동 |
| `profile.person.address.road` | 방배로 |
| `profile.person.address.building_no` | 524 |
| `profile.person.address.jibun` | 622 |
| `profile.person.address.detail` | 110동 501호 |
| `profile.person.address.building_name` | 롯데캐슬센트럴 |
| `profile.person.address.zipcode` | 06931 |
| `profile.person.address.road_short` | 서울특별시 서초구 방배로 524, 110동 501호 |
| `profile.person.address.road_full` | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| `profile.person.address.jibun_full` | 서울특별시 서초구 방배동 622 |
| `profile.person.address.region` | 서울특별시 서초구 |
| `profile.person.mobile` | 010-5907-7253 |
| `profile.person.email` | chanyeon363@naver.com |
| `profile.person.nationality` | 대한민국 |
| `profile.person.name_en` | PARK CHANYEON |
| `profile.person.age` | 36 |
| `profile.person.gender_ko` | 남 |
| `profile.father.name` | 박영준 |
| `profile.father.hanja` | 朴英準 |
| `profile.father.surname_en` | PARK |
| `profile.father.given_en` | YOUNGJUN |
| `profile.father.gender` | M |
| `profile.father.birth` | 1962.12.19 |
| `profile.father.rrn` | 621219-1097534 |
| `profile.father.address.sido` | 충청남도 |
| `profile.father.address.sigungu` | 천안시 서북구 |
| `profile.father.address.dong` | 두정동 |
| `profile.father.address.road` | 불당대로 |
| `profile.father.address.building_no` | 65-37 |
| `profile.father.address.jibun` | 455-10 |
| `profile.father.address.detail` | 111동 1704호 |
| `profile.father.address.building_name` | 우성에듀포레아파트 |
| `profile.father.address.zipcode` | 31308 |
| `profile.father.address.road_short` | 충청남도 천안시 서북구 불당대로 65-37, 111동 1704호 |
| `profile.father.address.road_full` | 충청남도 천안시 서북구 불당대로 65-37, 111동 1704호 (두정동, 우성에듀포레아파트) |
| `profile.father.address.jibun_full` | 충청남도 천안시 서북구 두정동 455-10 |
| `profile.father.address.region` | 충청남도 천안시 서북구 |
| `profile.father.mobile` | 010-6515-4769 |
| `profile.father.email` | youngjun641@nate.com |
| `profile.father.nationality` | 대한민국 |
| `profile.father.name_en` | PARK YOUNGJUN |
| `profile.father.age` | 64 |
| `profile.father.gender_ko` | 남 |
| `profile.mother.name` | 우나민 |
| `profile.mother.hanja` | 禹奈民 |
| `profile.mother.surname_en` | WOO |
| `profile.mother.given_en` | NAMIN |
| `profile.mother.gender` | F |
| `profile.mother.birth` | 1967.10.23 |
| `profile.mother.rrn` | 671023-2947198 |
| `profile.mother.address.sido` | 전라남도 |
| `profile.mother.address.sigungu` | 여수시 |
| `profile.mother.address.dong` | 소호동 |
| `profile.mother.address.road` | 시청로 |
| `profile.mother.address.building_no` | 325 |
| `profile.mother.address.jibun` | 595-53 |
| `profile.mother.address.detail` | 122동 904호 |
| `profile.mother.address.building_name` | 힐스테이트 |
| `profile.mother.address.zipcode` | 59091 |
| `profile.mother.address.road_short` | 전라남도 여수시 시청로 325, 122동 904호 |
| `profile.mother.address.road_full` | 전라남도 여수시 시청로 325, 122동 904호 (소호동, 힐스테이트) |
| `profile.mother.address.jibun_full` | 전라남도 여수시 소호동 595-53 |
| `profile.mother.address.region` | 전라남도 여수시 |
| `profile.mother.mobile` | 010-7560-2133 |
| `profile.mother.email` | namin561@hanmail.net |
| `profile.mother.nationality` | 대한민국 |
| `profile.mother.name_en` | WOO NAMIN |
| `profile.mother.age` | 59 |
| `profile.mother.gender_ko` | 여 |
| `profile.employment.company.name` | 주식회사 태평양무역 |
| `profile.employment.company.name_en` | Pacific Trading Co., Ltd. |
| `profile.employment.company.biz_no` | 501-82-42625 |
| `profile.employment.company.corp_no` | 135012-8790490 |
| `profile.employment.company.ceo.name` | 공정태 |
| `profile.employment.company.ceo.hanja` | 孔正泰 |
| `profile.employment.company.ceo.surname_en` | KONG |
| `profile.employment.company.ceo.given_en` | JEONGTAE |
| `profile.employment.company.ceo.gender` | F |
| `profile.employment.company.ceo.birth` | 1972.07.25 |
| `profile.employment.company.ceo.rrn` | 720725-2309894 |
| `profile.employment.company.ceo.mobile` | 010-9951-3030 |
| `profile.employment.company.ceo.email` | jeongtae876@gmail.com |
| `profile.employment.company.ceo.nationality` | 대한민국 |
| `profile.employment.company.ceo.name_en` | KONG JEONGTAE |
| `profile.employment.company.ceo.age` | 54 |
| `profile.employment.company.ceo.gender_ko` | 여 |
| `profile.employment.company.address.sido` | 충청북도 |
| `profile.employment.company.address.sigungu` | 청주시 흥덕구 |
| `profile.employment.company.address.dong` | 복대동 |
| `profile.employment.company.address.road` | 오송생명로 |
| `profile.employment.company.address.building_no` | 491-4 |
| `profile.employment.company.address.jibun` | 1392-28 |
| `profile.employment.company.address.detail` | 10층 03호 |
| `profile.employment.company.address.building_name` | 신영타워 |
| `profile.employment.company.address.zipcode` | 28358 |
| `profile.employment.company.address.road_short` | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 |
| `profile.employment.company.address.road_full` | 충청북도 청주시 흥덕구 오송생명로 491-4, 10층 03호 (복대동, 신영타워) |
| `profile.employment.company.address.jibun_full` | 충청북도 청주시 흥덕구 복대동 1392-28 |
| `profile.employment.company.address.region` | 충청북도 청주시 흥덕구 |
| `profile.employment.company.phone` | 043-783-2775 |
| `profile.employment.company.fax` | 043-914-3332 |
| `profile.employment.company.biz_type` | 도매 및 소매업 |
| `profile.employment.company.biz_item` | 무역 |
| `profile.employment.company.established` | 2020.09.07 |
| `profile.employment.company.capital` | 500,000,000 |
| `profile.employment.company.employees` | 28 |
| `profile.employment.company.revenue` | 8,375,000,000 |
| `profile.employment.company.kind` | 법인 |
| `profile.employment.company.email` | info@pacific.co.kr |
| `profile.employment.department` | 구매팀 |
| `profile.employment.position` | 대리 |
| `profile.employment.job` | 관리직 |
| `profile.employment.hire_date` | 2020.05.08 |
| `profile.employment.annual_salary` | 54,600,000 |
| `profile.employment.employee_no` | B88222 |
| `profile.business.name` | 동방학원 |
| `profile.business.name_en` | 동방학원 |
| `profile.business.biz_no` | 860-11-55034 |
| `profile.business.ceo.name` | 박찬연 |
| `profile.business.ceo.hanja` | 朴讚姸 |
| `profile.business.ceo.surname_en` | PARK |
| `profile.business.ceo.given_en` | CHANYEON |
| `profile.business.ceo.gender` | M |
| `profile.business.ceo.birth` | 1990.02.10 |
| `profile.business.ceo.rrn` | 900210-1659382 |
| `profile.business.ceo.address.sido` | 서울특별시 |
| `profile.business.ceo.address.sigungu` | 서초구 |
| `profile.business.ceo.address.dong` | 방배동 |
| `profile.business.ceo.address.road` | 방배로 |
| `profile.business.ceo.address.building_no` | 524 |
| `profile.business.ceo.address.jibun` | 622 |
| `profile.business.ceo.address.detail` | 110동 501호 |
| `profile.business.ceo.address.building_name` | 롯데캐슬센트럴 |
| `profile.business.ceo.address.zipcode` | 06931 |
| `profile.business.ceo.address.road_short` | 서울특별시 서초구 방배로 524, 110동 501호 |
| `profile.business.ceo.address.road_full` | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| `profile.business.ceo.address.jibun_full` | 서울특별시 서초구 방배동 622 |
| `profile.business.ceo.address.region` | 서울특별시 서초구 |
| `profile.business.ceo.mobile` | 010-5907-7253 |
| `profile.business.ceo.email` | chanyeon363@naver.com |
| `profile.business.ceo.nationality` | 대한민국 |
| `profile.business.ceo.name_en` | PARK CHANYEON |
| `profile.business.ceo.age` | 36 |
| `profile.business.ceo.gender_ko` | 남 |
| `profile.business.address.sido` | 울산광역시 |
| `profile.business.address.sigungu` | 남구 |
| `profile.business.address.dong` | 달동 |
| `profile.business.address.road` | 대학로 |
| `profile.business.address.building_no` | 14 |
| `profile.business.address.jibun` | 840 |
| `profile.business.address.detail` | 11층 |
| `profile.business.address.building_name` | 아이엠스퀘어 |
| `profile.business.address.zipcode` | 44857 |
| `profile.business.address.road_short` | 울산광역시 남구 대학로 14, 11층 |
| `profile.business.address.road_full` | 울산광역시 남구 대학로 14, 11층 (달동, 아이엠스퀘어) |
| `profile.business.address.jibun_full` | 울산광역시 남구 달동 840 |
| `profile.business.address.region` | 울산광역시 남구 |
| `profile.business.phone` | 052-956-0748 |
| `profile.business.fax` | 052-757-4601 |
| `profile.business.biz_type` | 서비스업 |
| `profile.business.biz_item` | 학원 |
| `profile.business.established` | 2020.03.21 |
| `profile.business.capital` | 0 |
| `profile.business.employees` | 8 |
| `profile.business.revenue` | 634,100,000 |
| `profile.business.kind` | 개인 |
| `profile.business.email` | contact@dongbang.co.kr |
| `profile.corporation.name` | (주)유니온무역 |
| `profile.corporation.name_en` | Union Trading Co., Ltd. |
| `profile.corporation.biz_no` | 264-82-36559 |
| `profile.corporation.corp_no` | 200112-7448551 |
| `profile.corporation.ceo.name` | 박찬연 |
| `profile.corporation.ceo.hanja` | 朴讚姸 |
| `profile.corporation.ceo.surname_en` | PARK |
| `profile.corporation.ceo.given_en` | CHANYEON |
| `profile.corporation.ceo.gender` | M |
| `profile.corporation.ceo.birth` | 1990.02.10 |
| `profile.corporation.ceo.rrn` | 900210-1659382 |
| `profile.corporation.ceo.address.sido` | 서울특별시 |
| `profile.corporation.ceo.address.sigungu` | 서초구 |
| `profile.corporation.ceo.address.dong` | 방배동 |
| `profile.corporation.ceo.address.road` | 방배로 |
| `profile.corporation.ceo.address.building_no` | 524 |
| `profile.corporation.ceo.address.jibun` | 622 |
| `profile.corporation.ceo.address.detail` | 110동 501호 |
| `profile.corporation.ceo.address.building_name` | 롯데캐슬센트럴 |
| `profile.corporation.ceo.address.zipcode` | 06931 |
| `profile.corporation.ceo.address.road_short` | 서울특별시 서초구 방배로 524, 110동 501호 |
| `profile.corporation.ceo.address.road_full` | 서울특별시 서초구 방배로 524, 110동 501호 (방배동, 롯데캐슬센트럴) |
| `profile.corporation.ceo.address.jibun_full` | 서울특별시 서초구 방배동 622 |
| `profile.corporation.ceo.address.region` | 서울특별시 서초구 |
| `profile.corporation.ceo.mobile` | 010-5907-7253 |
| `profile.corporation.ceo.email` | chanyeon363@naver.com |
| `profile.corporation.ceo.nationality` | 대한민국 |
| `profile.corporation.ceo.name_en` | PARK CHANYEON |
| `profile.corporation.ceo.age` | 36 |
| `profile.corporation.ceo.gender_ko` | 남 |
| `profile.corporation.address.sido` | 서울특별시 |
| `profile.corporation.address.sigungu` | 중구 |
| `profile.corporation.address.dong` | 신당동 |
| `profile.corporation.address.road` | 다산로 |
| `profile.corporation.address.building_no` | 361 |
| `profile.corporation.address.jibun` | 1380-58 |
| `profile.corporation.address.detail` | 6층 |
| `profile.corporation.address.building_name` | 그린지식산업센터 |
| `profile.corporation.address.zipcode` | 04766 |
| `profile.corporation.address.road_short` | 서울특별시 중구 다산로 361, 6층 |
| `profile.corporation.address.road_full` | 서울특별시 중구 다산로 361, 6층 (신당동, 그린지식산업센터) |
| `profile.corporation.address.jibun_full` | 서울특별시 중구 신당동 1380-58 |
| `profile.corporation.address.region` | 서울특별시 중구 |
| `profile.corporation.phone` | 02-9508-6789 |
| `profile.corporation.fax` | 02-716-6590 |
| `profile.corporation.biz_type` | 도매 및 소매업 |
| `profile.corporation.biz_item` | 무역 |
| `profile.corporation.established` | 2018.11.01 |
| `profile.corporation.capital` | 50,000,000 |
| `profile.corporation.employees` | 312 |
| `profile.corporation.revenue` | 61,800,000,000 |
| `profile.corporation.kind` | 법인 |
| `profile.corporation.email` | biz@union.co.kr |
| `profile.directors.0.name` | 조태재 |
| `profile.directors.0.hanja` | 趙台材 |
| `profile.directors.0.surname_en` | CHO |
| `profile.directors.0.given_en` | TAEJAE |
| `profile.directors.0.gender` | M |
| `profile.directors.0.birth` | 1985.03.08 |
| `profile.directors.0.rrn` | 850308-1007545 |
| `profile.directors.0.address.sido` | 경상북도 |
| `profile.directors.0.address.sigungu` | 포항시 남구 |
| `profile.directors.0.address.dong` | 효자동 |
| `profile.directors.0.address.road` | 지곡로 |
| `profile.directors.0.address.building_no` | 52 |
| `profile.directors.0.address.jibun` | 851-41 |
| `profile.directors.0.address.detail` | 113동 2204호 |
| `profile.directors.0.address.building_name` | 자이2차 |
| `profile.directors.0.address.zipcode` | 37003 |
| `profile.directors.0.address.road_short` | 경상북도 포항시 남구 지곡로 52, 113동 2204호 |
| `profile.directors.0.address.road_full` | 경상북도 포항시 남구 지곡로 52, 113동 2204호 (효자동, 자이2차) |
| `profile.directors.0.address.jibun_full` | 경상북도 포항시 남구 효자동 851-41 |
| `profile.directors.0.address.region` | 경상북도 포항시 남구 |
| `profile.directors.0.mobile` | 010-3749-0234 |
| `profile.directors.0.email` | taejae774@hanmail.net |
| `profile.directors.0.nationality` | 대한민국 |
| `profile.directors.0.name_en` | CHO TAEJAE |
| `profile.directors.0.age` | 41 |
| `profile.directors.0.gender_ko` | 남 |
| `profile.property.address.sido` | 경기도 |
| `profile.property.address.sigungu` | 수원시 영통구 |
| `profile.property.address.dong` | 원천동 |
| `profile.property.address.road` | 매탄로 |
| `profile.property.address.building_no` | 376 |
| `profile.property.address.jibun` | 87 |
| `profile.property.address.detail` | 115동 2104호 |
| `profile.property.address.building_name` | 한신휴플러스에듀포레 |
| `profile.property.address.zipcode` | 16892 |
| `profile.property.address.road_short` | 경기도 수원시 영통구 매탄로 376, 115동 2104호 |
| `profile.property.address.road_full` | 경기도 수원시 영통구 매탄로 376, 115동 2104호 (원천동, 한신휴플러스에듀포레) |
| `profile.property.address.jibun_full` | 경기도 수원시 영통구 원천동 87 |
| `profile.property.address.region` | 경기도 수원시 영통구 |
| `profile.property.kind` | 아파트 |
| `profile.property.land_area` | 54.47 |
| `profile.property.exclusive_area` | 101.84 |
| `profile.property.floor` | 1 |
| `profile.property.total_floors` | 17 |
| `profile.property.structure` | 철근콘크리트구조 |
| `profile.property.completed` | 1994.10.10 |
| `profile.property.price` | 560,000,000 |
| `profile.property.official_price` | 359,000,000 |
| `profile.property.unique_no` | 1792-2013-094176 |
| `profile.property.seller.name` | 박기우 |
| `profile.property.seller.hanja` | 朴基祐 |
| `profile.property.seller.surname_en` | PARK |
| `profile.property.seller.given_en` | GIWOO |
| `profile.property.seller.gender` | M |
| `profile.property.seller.birth` | 1957.05.08 |
| `profile.property.seller.rrn` | 570508-1456825 |
| `profile.property.seller.address.sido` | 부산광역시 |
| `profile.property.seller.address.sigungu` | 부산진구 |
| `profile.property.seller.address.dong` | 부전동 |
| `profile.property.seller.address.road` | 중앙대로 |
| `profile.property.seller.address.building_no` | 490 |
| `profile.property.seller.address.jibun` | 99-55 |
| `profile.property.seller.address.detail` | 111동 1004호 |
| `profile.property.seller.address.building_name` | SK뷰1차아파트 |
| `profile.property.seller.address.zipcode` | 47101 |
| `profile.property.seller.address.road_short` | 부산광역시 부산진구 중앙대로 490, 111동 1004호 |
| `profile.property.seller.address.road_full` | 부산광역시 부산진구 중앙대로 490, 111동 1004호 (부전동, SK뷰1차아파트) |
| `profile.property.seller.address.jibun_full` | 부산광역시 부산진구 부전동 99-55 |
| `profile.property.seller.address.region` | 부산광역시 부산진구 |
| `profile.property.seller.mobile` | 010-6594-7883 |
| `profile.property.seller.email` | giwoo598@gmail.com |
| `profile.property.seller.nationality` | 대한민국 |
| `profile.property.seller.name_en` | PARK GIWOO |
| `profile.property.seller.age` | 69 |
| `profile.property.seller.gender_ko` | 남 |
| `profile.property.lease_deposit` | 360,000,000 |
| `profile.accounts.0.bank` | 기업은행 |
| `profile.accounts.0.branch` | 여의도지점 |
| `profile.accounts.0.number` | 171-760452-29-611 |
| `profile.accounts.0.holder` | 박찬연 |
| `profile.accounts.0.opened` | 2014.06.11 |
| `profile.accounts.0.balance` | 60,014,579 |
| `profile.bank` | 기업은행 |
| `profile.bank_branch` | 범어지점 |
| `profile.foreign.name` | Mekong Garment JSC |
| `profile.foreign.address` | 45 Le Loi St, District 1, Ho Chi Minh City |
| `profile.foreign.country` | VIETNAM |
| `profile.foreign.contact` | John Miller |
| `profile.foreign.email` | sales@mekong.com |
| `profile.foreign.bank` | Vietcombank |
| `profile.foreign.swift` | BFTVVNVX |
| `profile.foreign.account` | 884779361534 |
