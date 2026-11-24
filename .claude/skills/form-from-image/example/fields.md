# 예금(신탁) 잔액증명 의뢰서 (deposit_balance_cert_request) — 1쪽, group=bank_form, category=internal, 원본=빈 서식(하나은행 공개 서식)

## 칸
| 쪽 | 원본 항목명 | 키 | type | source | 이 칸이 무엇인지 | 값 예시·형식 | 확신 |
|---|---|---|---|---|---|---|---|
| 1 | 지점(부) 앞 | bank.branch | text | rule:branch | 의뢰서를 받는 지점 | 센텀지점 | 중간 (원본은 "○○ 지점(부) 앞"이라 값에 "지점"이 겹칠 수 있음) |
| 1 | 신청구분 □등록 □변경 □해제 | apply_type | checkbox | rule:choice [등록, 변경, 해제] | 정기발급 신청의 등록·변경·해제 중 하나 | 등록 | 높음 |
| 1 | 발급기준일 | base_date | date | rule:date | 잔액을 증명할 기준 날짜 | 2025.09.01 | 높음 |
| 1 | 대상계좌 □지정계좌 □전체계좌 | target_scope | checkbox | rule:choice [지정계좌, 전체계좌] | 증명할 계좌 범위 | 지정계좌 | 높음 |
| 1 | 신청부수 국문 매 | copies.kor | number | rule:choice [1, 2, 3] | 국문 증명서 부수 | 1 | 높음 |
| 1 | 신청부수 영문 매 | copies.eng | number | rule:choice [1, 2] | 영문 증명서 부수 | 1 | 중간 (영문은 안 쓰는 경우가 많음) |
| 1 | (통화코드 : ) | currency | text | rule:currency | 영문 증명서 표시 통화 | USD | 중간 |
| 1 | □계좌마스킹(계좌번호 일부숨김) | account_mask | checkbox | rule:choice [계좌마스킹(계좌번호 일부숨김)] | 계좌번호 일부 가림 요청 여부 | 체크 | 낮음 (보기 하나짜리 체크 — 안 체크된 경우가 안 나옴) |
| 1 | 발급용도 | purpose | text | rule:choice [대출신청용, 입찰참가용, 비자발급용, 관공서 제출용] | 증명서를 쓸 곳 | 대출신청용 | 중간 |
| 1 | 수수료 출금계좌 | fee_account | text | rule:account | 발급 수수료를 뺄 계좌 | 123-456789-01234 | 높음 |
| 1 | 수령방법 □창구수령 □카카오톡(문자) □E-mail | receive_method | checkbox | rule:choice [창구수령, 카카오톡(문자), E-mail] | 증명서를 받는 방법 | 창구수령 | 높음 |
| 1 | E-mail : @ | receive_email | text | profile.person.email | 이메일 수령 주소 | abc@naver.com | 높음 |
| 1 | 기준일자 □매월 : 일 | periodic.day | text | rule:transfer_day | 정기발급 기준일(매월 며칠) | 10일 | 중간 (원본 "일" 글자와 겹침 → 숫자만이어야) |
| 1 | 수령방법(정기) □우편수령 □창구수령 □E-mail | periodic.receive_method | checkbox | rule:choice [우편수령, 창구수령, E-mail] | 정기발급 증명서 받는 방법 | 우편수령 | 높음 |
| 1 | E-mail(정기) : @ | periodic.email | text | profile.person.email | 정기발급 이메일 주소 | abc@naver.com | 높음 |
| 1 | 유효기간 시작 년 | periodic.start_y | number | rule:date part 0 | 정기발급 유효기간 시작 년 | 2025 | 높음 |
| 1 | 유효기간 시작 월 | periodic.start_m | number | rule:date part 1 | 〃 월 | 09 | 높음 |
| 1 | 유효기간 시작 일 | periodic.start_d | number | rule:date part 2 | 〃 일 | 01 | 높음 |
| 1 | 유효기간 끝 년·월·일 | periodic.end_y · end_m · end_d | number | rule:date part 0·1·2 | 정기발급 유효기간 끝 (시작 뒤, 3년 이내) | 2026 / 08 / 31 | 높음 |
| 1 | 창구수령대리인 성명 | pickup_agent.name | text | rule:other_person | 창구에서 대신 받을 사람 | 김민수 | 높음 |
| 1 | 창구수령대리인 생년월일 | pickup_agent.birth | date | rule:date | 〃 생년월일 | 1985.03.02 | 중간 (rule:date 가 앞날짜를 낼 수 있음) |
| 1 | 창구수령대리인 관계 | pickup_agent.relation | text | rule:choice [배우자, 자녀, 부모, 직원] | 예금주와의 관계 | 배우자 | 높음 |
| 1 | 우편수령대리인 성명 | mail_agent.name | text | rule:other_person | 우편으로 대신 받을 사람 | 박지영 | 중간 |
| 1 | 신청일 년 | apply_y | number | profile.issue_date part 0 | 의뢰서 작성일 년 | 2025 | 높음 |
| 1 | 신청일 월 | apply_m | number | profile.issue_date part 1 | 〃 월 | 09 | 높음 |
| 1 | 신청일 일 | apply_d | number | profile.issue_date part 2 | 〃 일 | 02 | 높음 |
| 1 | 성명(상호명) | customer.name | text | profile.person.name | 예금주(신청인) 이름 | 홍길동 | 높음 |
| 1 | 생년월일(사업자번호) | customer.birth | date | profile.person.birth | 예금주 생년월일 | 1982.10.25 | 높음 |
| 1 | 영문명 | customer.name_en | text | profile.person.name_en | 예금주 영문 이름 (영문 증명서용) | LEE WOOKYU | 높음 |
| 1 | 연락처 | customer.phone | text | profile.person.mobile | 예금주 연락처 | 010-1234-5678 | 높음 |
| 1 | 주소 | customer.address | text | profile.person.address.road_short | 예금주 주소 | 경기도 수원시 … | 높음 |
| 1 | 대리인성명 | agent.name | text | rule:other_person | 위임받은 대리인 이름 | 김민수 | 높음 |
| 1 | 생년월일(대리인) | agent.birth | date | rule:date | 대리인 생년월일 | 1985.03.02 | 중간 |
| 1 | 본인과의 관계 | agent.relation | text | rule:choice [배우자, 자녀, 부모, 직원] | 예금주와 대리인의 관계 | 배우자 | 높음 |
| 1 | 연락처(대리인) | agent.phone | text | rule:pattern 010-####-#### | 대리인 연락처 | 010-… | 높음 |
| 1 | 주소(대리인) | agent.address | text | rule:address | 대리인 주소 | 서울특별시 … | 높음 |
| 1 | 위임 범위 □잔액증명서 발급 □정기발급 신청 | delegation_scope | checkbox | rule:choice [잔액증명서 발급, 정기발급 신청] | 대리인에게 맡기는 일 | 잔액증명서 발급 | 높음 |
| 1 | 위임인 | delegator.name | text | profile.person.name | 위임하는 예금주 이름 (= 성명) | 홍길동 | 높음 |

질문 설명 `q`: 같은 항목명이 여러 곳 → `periodic.receive_method` "정기발급 수령방법", `periodic.email` "정기발급 E-mail", `agent.birth` "대리인 생년월일", `agent.phone` "대리인 연락처", `agent.address` "대리인 주소", `pickup_agent.*` "창구수령대리인 …", `mail_agent.name` "우편수령대리인 성명".

## 반복 표 accounts — 원본 계좌번호 칸 6개(왼쪽 3·오른쪽 3) → min 1, max 6
| 열 | 원본 머리글 | 열 키 | type | source | 이 열이 무엇인지 |
|---|---|---|---|---|---|
| 1 | 계좌번호 | number | text | rule:account | 잔액을 증명할 계좌 (지정계좌일 때) |

## 도장·서명
| 원본 표시 | 키 | 매크로 |
|---|---|---|
| 성명 옆 (서명/인) | seal.customer · sign.customer | m.sigspot("customer", val("customer.name"), mark="(서명/인)", label="예금주") |
| 위임인 옆 (서명/인) | seal.delegator · sign.delegator | m.sigspot("delegator", val("delegator.name"), mark="(서명/인)", label="위임인") |
| 결재란 (본인확인·담당·책임자·감사통할·부점장) | — | 칸만 그린 표 (은행 직원 칸, 값 없음) |

## 칸끼리 관계 (→ generate.py)
- 유효기간 시작 ≤ 끝, 끝은 시작부터 3년 이내 (원본 "※ 최대 3년이하로 설정 가능").
- 위임인 = 성명 (같은 source 라 이미 같음).
- 대상계좌가 "전체계좌"면 계좌번호를 비움 (원본 "※ 전체계좌 선택시 계좌번호 작성 불요").

## 고정 글자 (값 아님)
- 제목, "주식회사 하나은행", 결재란 머리, 모든 항목명, "※ 전체계좌 선택시 계좌번호 작성 불요", "※ 잔액증명서 발급에 따른 수수료를 …", "※ 최대 3년이하로 설정 가능", 발급부수 "전산인자"(회색), "계좌번호 자필기재"(회색), "선택항목"(회색 안내 글자)
- 고객 확인 사항 1~6, "귀 은행의 본인(당사) 명의에 대하여 …", "※ 영문명은 …", "본인은 상기 계좌의 (…) 과 관련한 일체의 행위를 …", "※ 개인은 인감증명서/…", 서식 번호 "5-08-0094(1-1) (2025.01 개정) (보존년한 : 5년)"

## 판단이 안 선 것
- `account_mask`: 보기 하나짜리 체크라 rule:choice 로는 늘 체크됨. 안 체크된 서류도 나오게 하려면 generate.py 에서 가끔 비워야 함.
- 발급용도 앞 □, 우편수령대리인 "□ 주소" 의 □ 는 값으로 만들지 않고 고정 글자로 둠.
- 회색 안내 글자("선택항목", "계좌번호 자필기재", "전산인자")는 값이 들어가면 겹침 → 값이 있는 칸에서는 안내 글자를 빼고 그림.
- 바코드·하나은행 로고는 넣지 않음 (로고 자리는 "하나은행" 글자).
