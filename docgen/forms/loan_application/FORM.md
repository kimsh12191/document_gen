# 대출거래신청서 (`loan_application`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card loan_application · card-hash: c76485c10870 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 대출거래신청서 (다른 이름: 《개인》대출신청서(가계용))
- **질문·답:** 이 폴더의 `questions.json` 에서 바꾼 것이 있음 (아래 ← 바꿈)
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa loan_application --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 개인 고객 대출신청서(가계용). 하나은행 「대출신청서(가계용)」, 신한은행 「대출상담및신청서(가계용)」 항목 구성 참고.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `questions.json` | 기본 과제의 질문 문장·답 틀 (기본과 다른 것만) |
| `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 39칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank` | 은행명 | text | 1쪽 [101, 39, 194, 61] | 늘 | 템플릿 | generate.py | fields.json:75 | 묻기 |
| `branch` | 취급점 | text | 1쪽 [725, 130, 780, 141] | 늘 | 템플릿 | generate.py | look/template.html.j2:15 · fields.json:80 | 묻기 |
| `applicant.name` | 성명 | text | 1쪽 [198, 172, 255, 183] | 늘 | 템플릿 | generate.py | look/template.html.j2:11 · fields.json:50 | 묻기 |
| `applicant.rrn` | 실명번호 | rrn | 1쪽 [644, 172, 742, 183] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:55 | 묻기 |
| `applicant.zipcode` | 우편번호 | text | - | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:65 | 묻기 |
| `applicant.address` | 자택주소 | text | 1쪽 [229, 192, 723, 203] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:30 | 묻기 |
| `applicant.mobile` | 휴대전화 | phone | 1쪽 [198, 212, 286, 223] | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:45 | 묻기 |
| `applicant.home_phone` | 자택전화 | phone | - | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:40 | 묻기 |
| `applicant.email` | E-mail | text | - | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:35 | 묻기 |
| `applicant.work_phone` | 직장전화 | phone | - | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:60 | 묻기 |
| `workplace.name` | 직장명 | text | 1쪽 [198, 331, 316, 342] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:270 | 묻기 |
| `workplace.department` | 근무부서 | text | 1쪽 [644, 331, 715, 342] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:255 | 묻기 |
| `workplace.position` | 직위 | text | 1쪽 [198, 351, 226, 362] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:275 | 묻기 |
| `workplace.hire_date` | 입사년월일 | date | 1쪽 [644, 351, 711, 362] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:260 | 묻기 |
| `workplace.annual_income` | 연소득(본인) | text | 1쪽 [198, 371, 259, 382] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:250 | 묻기 |
| `workplace.address` | 직장주소 | text | 1쪽 [644, 371, 891, 382] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:245 | 묻기 |
| `loan.subject` | 대출과목 | text | 1쪽 [198, 502, 284, 513] | 늘 | 템플릿 | generate.py | look/template.html.j2:78 · fields.json:195 | 묻기 |
| `loan.product` | 상품명 | text | 1쪽 [644, 502, 730, 513] | 늘 | 템플릿 | generate.py | look/template.html.j2:78 · fields.json:170 | 묻기 |
| `loan.amount_korean` | 대출신청금액(한글) | amount_korean | 1쪽 [198, 522, 330, 533] | 늘 | 템플릿 | generate.py | look/template.html.j2:79 · fields.json:140 | 묻기 |
| `loan.amount` | 대출신청금액 | amount | 1쪽 [360, 522, 431, 533] | 늘 | 템플릿 | generate.py | look/template.html.j2:79 · fields.json:135 | 묻기 |
| `loan.term` | 대출기간 | text | 1쪽 [198, 542, 226, 553] | 늘 | 템플릿 | generate.py | look/template.html.j2:80 · fields.json:200 | 묻기 |
| `loan.hope_date` | 대출희망일 | date | 1쪽 [644, 542, 711, 553] | 늘 | 템플릿 | generate.py | look/template.html.j2:80 · fields.json:160 | 묻기 |
| `loan.interest_day` | 이자납입일 | text | 1쪽 [644, 582, 697, 593] | 늘 | 템플릿 | generate.py | look/template.html.j2:82 · fields.json:165 | 묻기 |
| `loan.purpose` | 세부용도 | text | 1쪽 [260, 616, 346, 626] | 늘 | 템플릿 | generate.py | look/template.html.j2:83 · fields.json:175 | 묻기 |
| `collateral_detail` | 담보내용 | text | 1쪽 [644, 636, 891, 660] | 늘 | 템플릿 | generate.py | look/template.html.j2:84 · fields.json:115 | 묻기 |
| `loan.debit_bank` | 이체은행 | text | 1쪽 [230, 676, 287, 687] | 늘 | 템플릿 | generate.py | look/template.html.j2:85 · fields.json:150 | 묻기 |
| `loan.debit_account` | 이체계좌번호 | account_no | 1쪽 [359, 676, 469, 687] | 늘 | 템플릿 | generate.py | look/template.html.j2:85 · fields.json:145 | 묻기 |
| `loan.debit_holder` | 예금주 | text | 1쪽 [526, 676, 584, 687] | 늘 | 템플릿 | generate.py | look/template.html.j2:85 · fields.json:155 | 묻기 |
| `apply_date` | 신청일 | date | 1쪽 [584, 780, 677, 791] | 늘 | 템플릿 | generate.py | look/template.html.j2:118 · fields.json:70 | 묻기 |
| `signature` | 신청인 | text | 1쪽 [759, 780, 817, 791] | 늘 | 템플릿 | generate.py | look/template.html.j2:118 · fields.json:240 | 묻기 |
| `agent.name` | 대리인성명 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:101 · fields.json:5 | 묻기 |
| `agent.rrn` | 대리인실명번호 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:101 · fields.json:25 | 묻기 |
| `agent.relation` | 본인과의관계 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:102 · fields.json:20 | 묻기 |
| `agent.phone` | 대리인연락처 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:102 · fields.json:10 | 묻기 |
| `co_borrower.name` | 공동차주성명 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:92 · fields.json:90 | 묻기 |
| `co_borrower.rrn` | 공동차주실명번호 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:92 · fields.json:100 | 묻기 |
| `co_borrower.relation` | 신청인과의관계 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:93 · fields.json:95 | 묻기 |
| `co_borrower.mobile` | 공동차주휴대전화 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:93 · fields.json:85 | 묻기 |
| `co_borrower.workplace` | 공동차주직장 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:94 · fields.json:105 | 묻기 |

## 표 `debts` (표 과제 table·table_read·table_find·table_qa) — 5열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `debts.*.lender` | 금융기관 | text | 1쪽 [96, 437, 153, 448] (1행) | 12/16 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:315 | 묻기 |
| `debts.*.kind` | 대출종류 | text | 1쪽 [196, 437, 253, 448] (1행) | 12/16 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:310 | 묻기 |
| `debts.*.balance` | 잔액 | amount | 1쪽 [288, 437, 352, 448] (1행) | 12/16 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:305 | 묻기 |
| `debts.*.maturity` | 만기일 | date | 1쪽 [373, 437, 440, 448] (1행) | 12/16 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:320 | 묻기 |
| `debts.*.refinance` | 상환여부 | text | 1쪽 [475, 437, 504, 448] (1행) | 12/16 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:325 | 묻기 |

## 표 `assets` (표 과제 table·table_read·table_find·table_qa) — 3열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `assets.*.kind` | 종류 | text | 1쪽 [547, 437, 590, 448] (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:285 | 묻기 |
| `assets.*.location` | 소재지 | text | 1쪽 [607, 437, 812, 448] (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:290 | 묻기 |
| `assets.*.value` | 평가금액 | amount | 1쪽 [838, 437, 921, 448] (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:295 | 묻기 |

## 체크·도장·서명 (marks) — 16칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `housing` | 주택소유구분 | checkbox (자가 / 전세 / 월세 / 기타) | 1쪽 [210, 259, 239, 269] | 늘 | 템플릿 | generate.py | look/template.html.j2:24 · fields.json:130 | 묻기 |
| `dwelling` | 주거형태 | checkbox (아파트 / 단독 / 다세대 / 연립·빌라 / 오피스텔 / 기타) | 1쪽 [656, 252, 699, 263] | 늘 | 템플릿 | generate.py | look/template.html.j2:24 · fields.json:125 | 묻기 |
| `workplace.job_type` | 직업구분 | checkbox (급여소득자 / 공무원 / 전문직 / 자영업자 / 기타) | 1쪽 [210, 311, 282, 322] | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:265 | 묻기 |
| `loan.repayment` | 상환방법 | checkbox (만기일시 / 원금균등분할 / 원리금균등분할 / 혼합) | 1쪽 [403, 562, 504, 573] | 늘 | 템플릿 | generate.py | look/template.html.j2:81 · fields.json:190 | 묻기 |
| `loan.rate_type` | 금리방식 | checkbox (고정 / 변동 / 혼합) | 1쪽 [317, 582, 346, 593] | 늘 | 템플릿 | generate.py | look/template.html.j2:82 · fields.json:185 | 묻기 |
| `loan.purpose_category` | 자금용도구분 | checkbox (주택구입 / 주택임차 / 부채상환 / 생활비 / 교육비 / 기타) | 1쪽 [457, 602, 500, 613] | 늘 | 템플릿 | generate.py | look/template.html.j2:83 · fields.json:180 | 묻기 |
| `collateral` | 담보구분 | checkbox (신용 / 부동산 / 보증) | 1쪽 [264, 642, 307, 653] | 늘 | 템플릿 | generate.py | look/template.html.j2:84 · fields.json:110 | 묻기 |
| `manual_received` | 설명서수령확인 | checkbox (예 / 아니오) | 1쪽 [336, 760, 350, 771] | 늘 | 템플릿 | generate.py | look/template.html.j2:113 · fields.json:205 | 묻기 |
| `consent` | 개인(신용)정보동의 | checkbox (동의함 / 동의하지 않음) | 1쪽 [640, 760, 681, 771] | 늘 | 템플릿 | generate.py | look/template.html.j2:113 · fields.json:120 | 묻기 |
| `seal.applicant` | 신청인 | seal | 1쪽 [854, 766, 911, 806] | 늘 | 템플릿 | generate.py | fields.json:215 | 묻기 |
| `sign.applicant` | 신청인 | signature | 1쪽 [839, 779, 927, 793] | 늘 | 템플릿 | generate.py | fields.json:230 | 묻기 |
| `agent.poa` | 위임장 | 체크박스 (첨부 / 미첨부) | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:103 · fields.json:15 | 묻기 |
| `seal.agent` | 대리인 | 도장 | - | 5/16 | 템플릿 | generate.py | fields.json:210 | 묻기 |
| `sign.agent` | 대리인 | 서명 | - | 5/16 | 템플릿 | generate.py | fields.json:225 | 묻기 |
| `seal.co_borrower` | 공동차주 | 도장 | - | 2/16 | 템플릿 | generate.py | fields.json:220 | 묻기 |
| `sign.co_borrower` | 공동차주 | 서명 | - | 2/16 | 템플릿 | generate.py | fields.json:235 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키는·값은:** 어디서 정해지나. 키·값 종류는 이 서식 파일에 적힌 그대로입니다 (모든 서식 공통 키 사전은 없음). "키 설명 그대로" 는 칸에 `"key"` 가 없어 키 설명이 키로 나가는 것. 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
- **고칠 곳:** html·코드 서식은 템플릿 줄(칸 자리·키·항목명)과 fields.json 줄(값 출처·질문 설정 q), 원본 서식은 fields.json 의 그 칸(박스 `rect`·항목명·키·값·q). html·코드 서식에서 fields.json 에 줄이 없는 칸의 질문 설정은 fields.json 맨 위 `"q": {"키": {…}}` 묶음에.

## 질문 → 답 (seed 1000000 로 그린 실제 문항)

질문은 모델에게 가는 글 전부, 답은 데이터의 정답 (그린 문서의 값·위치). 질문 문장·답 꼴은 이 폴더 `questions.json` 과 공통 `docgen/forms/_common/questions.json`.

### 서류 분류 `classify` · 채점 acc

질문:

```
이 문서는 고객이 은행에 제출한 서류입니다. 서류의 정식 명칭(서류명)을 답하세요. 설명 없이 서류명만 한 줄로 답하세요.
```

답:

```json
"대출거래신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "국민은행",
 "센텀지점",
 "남궁예태",
 "850328-2******",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "010-6144-1173",
 "주식회사 다온패션",
 "고객지원팀",
 "대리",
 "2021-03-06",
 "5,170만원",
 "부산광역시 해운대구 해운대로 326, 7층",
 "농협은행",
 "신용대출",
 "12,500,000",
 "2028-01-19",
 "유지",
 "새마을금고",
 "학자금대출",
 "13,100,000",
 "2030-04-13",
 "아파트",
 "서울특별시 서초구 강남대로 357",
 "1,560,000,000",
 "예금",
 "국민은행, 카카오뱅크",
 "70,700,000",
 "주택담보대출",
 "일금 삼억일백만원정",
 "301,000,000",
 "30년",
 "2025-04-10",
 "매월 5일",
 "생활안정자금",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (아파트, 전용 74.95㎡)",
 "478303-40-826627",
 "2025년 4월 1일"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"새마을금고"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"주택담보대출"
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
항목 (키: 설명 (몇 번째 행))
- bank: 은행명
- branch: 취급점
- applicant.name: 성명
- applicant.rrn: 실명번호
- applicant.zipcode: 우편번호
- applicant.address: 자택주소
- applicant.mobile: 휴대전화
- applicant.home_phone: 자택전화
- applicant.email: E-mail
- applicant.work_phone: 직장전화
- workplace.name: 직장명
- workplace.department: 근무부서
- workplace.position: 직위
- workplace.hire_date: 입사년월일
- workplace.annual_income: 연소득(본인)
- workplace.address: 직장주소
- loan.subject: 대출과목
- loan.product: 상품명
- loan.amount_korean: 대출신청금액(한글)
- loan.amount: 대출신청금액
- loan.term: 대출기간
- loan.hope_date: 대출희망일
- loan.interest_day: 이자납입일
- loan.purpose: 세부용도
- collateral_detail: 담보내용
- loan.debit_bank: 이체은행
- loan.debit_account: 이체계좌번호
- loan.debit_holder: 예금주
- apply_date: 신청일
- signature: 신청인
```

답:

```json
[{"key": "bank", "value": "국민은행", "bbox_2d": [101, 39, 194, 61], "page": 1},
 {"key": "branch", "value": "센텀지점", "bbox_2d": [725, 130, 780, 141], "page": 1},
 {"key": "applicant.name", "value": "남궁예태", "bbox_2d": [198, 172, 255, 183], "page": 1},
 {"key": "applicant.rrn", "value": "850328-2******", "bbox_2d": [644, 172, 742, 183], "page": 1},
 {"key": "applicant.zipcode", "value": null},
 {"key": "applicant.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [229, 192, 723, 203], "page": 1},
 {"key": "applicant.mobile", "value": "010-6144-1173", "bbox_2d": [198, 212, 286, 223], "page": 1},
 {"key": "applicant.home_phone", "value": null},
 {"key": "applicant.email", "value": null},
 {"key": "applicant.work_phone", "value": null},
 {"key": "workplace.name", "value": "주식회사 다온패션", "bbox_2d": [198, 331, 316, 342], "page": 1},
 {"key": "workplace.department", "value": "고객지원팀", "bbox_2d": [644, 331, 715, 342], "page": 1},
 {"key": "workplace.position", "value": "대리", "bbox_2d": [198, 351, 226, 362], "page": 1},
 {"key": "workplace.hire_date", "value": "2021-03-06", "bbox_2d": [644, 351, 711, 362], "page": 1},
 {"key": "workplace.annual_income", "value": "5,170만원", "bbox_2d": [198, 371, 259, 382], "page": 1},
 {"key": "workplace.address", "value": "부산광역시 해운대구 해운대로 326, 7층", "bbox_2d": [644, 371, 891, 382], "page": 1},
 {"key": "loan.subject", "value": "주택담보대출", "bbox_2d": [198, 502, 284, 513], "page": 1},
 {"key": "loan.product", "value": "주택담보대출", "bbox_2d": [644, 502, 730, 513], "page": 1},
 {"key": "loan.amount_korean", "value": "일금 삼억일백만원정", "bbox_2d": [198, 522, 330, 533], "page": 1},
 {"key": "loan.amount", "value": "301,000,000", "bbox_2d": [360, 522, 431, 533], "page": 1},
 {"key": "loan.term", "value": "30년", "bbox_2d": [198, 542, 226, 553], "page": 1},
 {"key": "loan.hope_date", "value": "2025-04-10", "bbox_2d": [644, 542, 711, 553], "page": 1},
 {"key": "loan.interest_day", "value": "매월 5일", "bbox_2d": [644, 582, 697, 593], "page": 1},
 {"key": "loan.purpose", "value": "생활안정자금", "bbox_2d": [260, 616, 346, 626], "page": 1},
 {"key": "collateral_detail", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (아파트, 전용 74.95㎡)", "bbox_2d": [644, 636, 891, 660], "page": 1},
 {"key": "loan.debit_bank", "value": "국민은행", "bbox_2d": [230, 676, 287, 687], "page": 1},
 {"key": "loan.debit_account", "value": "478303-40-826627", "bbox_2d": [359, 676, 469, 687], "page": 1},
 {"key": "loan.debit_holder", "value": "남궁예태", "bbox_2d": [526, 676, 584, 687], "page": 1},
 {"key": "apply_date", "value": "2025년 4월 1일", "bbox_2d": [584, 780, 677, 791], "page": 1},
 {"key": "signature", "value": "남궁예태", "bbox_2d": [759, 780, 817, 791], "page": 1}]
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
- housing: 주택소유구분 (체크박스, 보기: 자가 / 전세 / 월세 / 기타)
- dwelling: 주거형태 (체크박스, 보기: 아파트 / 단독 / 다세대 / 연립·빌라 / 오피스텔 / 기타)
- workplace.job_type: 직업구분 (체크박스, 보기: 급여소득자 / 공무원 / 전문직 / 자영업자 / 기타)
- loan.repayment: 상환방법 (체크박스, 보기: 만기일시 / 원금균등분할 / 원리금균등분할 / 혼합)
- loan.rate_type: 금리방식 (체크박스, 보기: 고정 / 변동 / 혼합)
- loan.purpose_category: 자금용도구분 (체크박스, 보기: 주택구입 / 주택임차 / 부채상환 / 생활비 / 교육비 / 기타)
- collateral: 담보구분 (체크박스, 보기: 신용 / 부동산 / 보증)
- manual_received: 설명서수령확인 (체크박스, 보기: 예 / 아니오)
- consent: 개인(신용)정보동의 (체크박스, 보기: 동의함 / 동의하지 않음)
- seal.applicant: 신청인 (같은 설명 중 1번째 칸, 도장)
- sign.applicant: 신청인 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "housing", "value": "자가", "bbox_2d": [198, 259, 206, 269], "page": 1},
 {"key": "dwelling", "value": "아파트", "bbox_2d": [644, 252, 652, 263], "page": 1},
 {"key": "workplace.job_type", "value": "급여소득자", "bbox_2d": [198, 311, 206, 322], "page": 1},
 {"key": "loan.repayment", "value": "원리금균등분할", "bbox_2d": [391, 562, 400, 573], "page": 1},
 {"key": "loan.rate_type", "value": "혼합", "bbox_2d": [305, 582, 314, 593], "page": 1},
 {"key": "loan.purpose_category", "value": "생활비", "bbox_2d": [444, 602, 453, 613], "page": 1},
 {"key": "collateral", "value": "부동산", "bbox_2d": [251, 642, 260, 653], "page": 1},
 {"key": "manual_received", "value": "예", "bbox_2d": [324, 760, 333, 771], "page": 1},
 {"key": "consent", "value": "동의함", "bbox_2d": [628, 760, 636, 771], "page": 1},
 {"key": "seal.applicant", "value": true, "bbox_2d": [854, 766, 911, 806], "page": 1},
 {"key": "sign.applicant", "value": false}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 '금융기관'·'잔액' 열이 있는 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 설명)
- lender: 금융기관
- kind: 대출종류
- balance: 잔액
- maturity: 만기일
- refinance: 상환여부
```

답:

```json
{
 "columns": [
  "lender",
  "kind",
  "balance",
  "maturity",
  "refinance"
 ],
 "rows": [
  [
   "농협은행",
   "신용대출",
   "12,500,000",
   "2028-01-19",
   "유지"
  ],
  [
   "새마을금고",
   "학자금대출",
   "13,100,000",
   "2030-04-13",
   "유지"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    96,
    437,
    504,
    448
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    89,
    455,
    504,
    465
   ],
   "page": 1
  }
 ]
}
```

### 표 찾기 `table_find` · 채점 f1_iou50 (위치)

질문:

```
이 문서에서 표를 모두 찾아 JSON 목록으로 답하세요. 여기서 표는 같은 항목 묶음(열)이 행마다 되풀이되고 행 수가 서류마다 달라지는 목록입니다. 항목명과 값이 번갈아 있는 신청서 칸, 칸 수가 정해진 결재란은 표가 아닙니다.
표마다 {{"columns": [머리글 글자, …], "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호, "n_rows": 행 수}} 를 쓰고, 여러 쪽에 걸친 표는 쪽마다 따로 씁니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 행 수에는 머리글·합계 행과 모두 빈 행을 넣지 않습니다. 표가 없으면 [] 로 답하세요.
```

답:

```json
[{"columns": ["금융기관", "대출종류", "잔액", "만기일", "상환여부"], "bbox_2d": [74, 416, 524, 465], "page": 1, "n_rows": 2},
 {"columns": ["종류", "소재지", "평가금액"], "bbox_2d": [535, 416, 926, 465], "page": 1, "n_rows": 2}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[74, 416, 524, 465] 위치의 표를 보고 답하세요. '금융기관' 칸이 '새마을금고'인 행의 '잔액' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"13,100,000"
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[74, 416, 524, 465] 위치의 표를 보고 답하세요. 마지막 행의 '금융기관' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"새마을금고"
```

### 표 그대로 옮기기 `table_read` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 '금융기관'·'대출종류' 열이 있는 표를 머리글까지 그대로 옮겨 JSON 으로 답하세요.
꼴: {"columns": [머리글 글자, …], "rows": [[칸 글자, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 표의 머리글을 왼쪽부터 쓰고, 머리글이 여러 줄이면 위 칸과 아래 칸 글자를 " > " 로 잇습니다.
- rows 는 행마다 columns 와 같은 순서로 칸 글자를 씁니다. 빈 칸은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 글자를 씁니다.
- 다음 쪽에서 다시 나온 머리글 행과 모두 빈 행은 빼고, 합계·소계 행은 그대로 둡니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
```

답:

```json
{
 "columns": [
  "금융기관",
  "대출종류",
  "잔액(원)",
  "만기일",
  "상환여부"
 ],
 "rows": [
  [
   "농협은행",
   "신용대출",
   "12,500,000",
   "2028-01-19",
   "유지"
  ],
  [
   "새마을금고",
   "학자금대출",
   "13,100,000",
   "2030-04-13",
   "유지"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    74,
    434,
    524,
    452
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    74,
    452,
    524,
    470
   ],
   "page": 1
  }
 ]
}
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa loan_application --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check loan_application` → `python -m docgen.formdir card loan_application` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `generate.py` 가 돌려주는 dict 에 그 키 값 | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` | 다시 |
| 답의 값 | `generate.py` (값 만드는 함수). 파이썬 대신 정하려면 `fields.json` 의 그 칸 `source` | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (파일로). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa loan_application --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions loan_application --show` · `python -m docgen.preview loan_application --out work/loan_application`
