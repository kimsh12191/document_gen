# 대출거래신청서 (`loan_application`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card loan_application · card-hash: ba6cbec90ea3 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 대출거래신청서 (다른 이름: 《개인》대출신청서(가계용))
- **쓰이는 업무:** 개인 신용대출, 주택담보대출, 전세자금대출, 개인사업자 대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa loan_application --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 개인 고객 대출신청서(가계용). 하나은행 「대출신청서(가계용)」, 신한은행 「대출상담및신청서(가계용)」 항목 구성 참고.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 47칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank` | 은행명 | text | 1쪽 [101, 39, 194, 61] | 늘 | 템플릿 | generate.py | fields.json:75 | 묻기 |
| `branch` | 취급점 | text | 1쪽 [725, 130, 780, 141] | 늘 | 템플릿 | generate.py | look/template.html.j2:15 · fields.json:80 | 묻기 |
| `customer.name` ← `applicant.name` | 성명 | text | 1쪽 [198, 172, 255, 183] | 늘 | 템플릿 | generate.py | look/template.html.j2:11 · fields.json:50 | 묻기 |
| `customer.rrn` ← `applicant.rrn` | 실명번호 | rrn | 1쪽 [644, 172, 742, 183] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:55 | 묻기 |
| `applicant.zipcode` | 우편번호 | text | - | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:65 | 묻기 |
| `customer.address` ← `applicant.address` | 자택주소 | text | 1쪽 [229, 192, 723, 203] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:30 | 묻기 |
| `customer.mobile` ← `applicant.mobile` | 휴대전화 | phone | 1쪽 [198, 212, 286, 223] | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:45 | 묻기 |
| `customer.home_phone` ← `applicant.home_phone` | 자택전화 | phone | - | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:40 | 묻기 |
| `customer.email` ← `applicant.email` | E-mail | text | - | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:35 | 묻기 |
| `applicant.work_phone` | 직장전화 | phone | - | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:60 | 묻기 |
| `employer.name` ← `workplace.name` | 직장명 | text | 1쪽 [198, 331, 316, 342] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:270 | 묻기 |
| `employer.department` ← `workplace.department` | 근무부서 | text | 1쪽 [644, 331, 715, 342] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:255 | 묻기 |
| `employer.position` ← `workplace.position` | 직위 | text | 1쪽 [198, 351, 226, 362] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:275 | 묻기 |
| `employer.hire_date` ← `workplace.hire_date` | 입사년월일 | date | 1쪽 [644, 351, 711, 362] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:260 | 묻기 |
| `workplace.annual_income` | 연소득(본인) | text | 1쪽 [198, 371, 259, 382] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:250 | 묻기 |
| `employer.address` ← `workplace.address` | 직장주소 | text | 1쪽 [644, 371, 891, 382] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:245 | 묻기 |
| `debts.*.lender` | 금융기관 | text | 1쪽 [96, 437, 153, 448] (1행) | 12/16 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:315 | 묻기 |
| `debts.*.kind` | 대출종류 | text | 1쪽 [196, 437, 253, 448] (1행) | 12/16 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:310 | 묻기 |
| `debts.*.balance` | 잔액 | amount | 1쪽 [288, 437, 352, 448] (1행) | 12/16 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:305 | 묻기 |
| `debts.*.maturity` | 만기일 | date | 1쪽 [373, 437, 440, 448] (1행) | 12/16 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:320 | 묻기 |
| `debts.*.refinance` | 상환여부 | text | 1쪽 [475, 437, 504, 448] (1행) | 12/16 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:325 | 묻기 |
| `assets.*.kind` | 종류 | text | 1쪽 [547, 437, 590, 448] (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:285 | 묻기 |
| `assets.*.location` | 소재지 | text | 1쪽 [607, 437, 812, 448] (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:290 | 묻기 |
| `assets.*.value` | 평가금액 | amount | 1쪽 [838, 437, 921, 448] (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:295 | 묻기 |
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
| `related.name` ← `co_borrower.name` | 공동차주성명 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:92 · fields.json:90 | 묻기 |
| `related.rrn` ← `co_borrower.rrn` | 공동차주실명번호 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:92 · fields.json:100 | 묻기 |
| `co_borrower.relation` | 신청인과의관계 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:93 · fields.json:95 | 묻기 |
| `co_borrower.mobile` | 공동차주휴대전화 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:93 · fields.json:85 | 묻기 |
| `co_borrower.workplace` | 공동차주직장 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:94 · fields.json:105 | 묻기 |

## 체크·도장·서명 (marks) — 16칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
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
| `seal.customer` ← `seal.applicant` | 신청인 | seal | 1쪽 [854, 766, 911, 806] | 늘 | 템플릿 | generate.py | fields.json:215 | 묻기 |
| `sign.customer` ← `sign.applicant` | 신청인 | signature | 1쪽 [839, 779, 927, 793] | 늘 | 템플릿 | generate.py | fields.json:230 | 묻기 |
| `agent.poa` | 위임장 | 체크박스 (첨부 / 미첨부) | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:103 · fields.json:15 | 묻기 |
| `seal.agent` | 대리인 | 도장 | - | 5/16 | 템플릿 | generate.py | fields.json:210 | 묻기 |
| `sign.agent` | 대리인 | 서명 | - | 5/16 | 템플릿 | generate.py | fields.json:225 | 묻기 |
| `seal.related` ← `seal.co_borrower` | 공동차주 | 도장 | - | 2/16 | 템플릿 | generate.py | fields.json:220 | 묻기 |
| `sign.related` ← `sign.co_borrower` | 공동차주 | 서명 | - | 2/16 | 템플릿 | generate.py | fields.json:235 | 묻기 |

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
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- bank: 은행명
- branch: 취급점
- customer.name: 성명 (고객 성명)
- customer.rrn: 실명번호 (고객 주민등록번호)
- applicant.zipcode: 우편번호
- customer.address: 자택주소 (고객 주소)
- customer.mobile: 휴대전화 (고객 휴대전화)
- customer.home_phone: 자택전화 (고객 자택전화)
- customer.email: E-mail (고객 이메일)
- applicant.work_phone: 직장전화
- employer.name: 직장명 (직장 이름)
- employer.department: 근무부서 (직장 부서)
- employer.address: 직장주소
- debts.0.lender: 금융기관 (1행)
- debts.0.kind: 대출종류 (1행)
- debts.0.balance: 잔액 (1행)
- debts.0.maturity: 만기일 (1행)
- debts.0.refinance: 상환여부 (1행)
- debts.1.lender: 금융기관 (2행)
- debts.1.kind: 대출종류 (2행)
- debts.1.balance: 잔액 (2행)
- debts.1.maturity: 만기일 (2행)
- assets.0.kind: 종류 (1행)
- assets.0.value: 평가금액 (1행)
- assets.1.kind: 종류 (2행)
- assets.1.location: 소재지 (2행)
- assets.1.value: 평가금액 (2행)
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
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [198, 172, 255, 183], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [644, 172, 742, 183], "page": 1},
 {"key": "applicant.zipcode", "value": null},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [229, 192, 723, 203], "page": 1},
 {"key": "customer.mobile", "value": "010-6144-1173", "bbox_2d": [198, 212, 286, 223], "page": 1},
 {"key": "customer.home_phone", "value": null},
 {"key": "customer.email", "value": null},
 {"key": "applicant.work_phone", "value": null},
 {"key": "employer.name", "value": "주식회사 다온패션", "bbox_2d": [198, 331, 316, 342], "page": 1},
 {"key": "employer.department", "value": "고객지원팀", "bbox_2d": [644, 331, 715, 342], "page": 1},
 {"key": "employer.address", "value": "부산광역시 해운대구 해운대로 326, 7층", "bbox_2d": [644, 371, 891, 382], "page": 1},
 {"key": "debts.0.lender", "value": "농협은행", "bbox_2d": [96, 437, 153, 448], "page": 1},
 {"key": "debts.0.kind", "value": "신용대출", "bbox_2d": [196, 437, 253, 448], "page": 1},
 {"key": "debts.0.balance", "value": "12,500,000", "bbox_2d": [288, 437, 352, 448], "page": 1},
 {"key": "debts.0.maturity", "value": "2028-01-19", "bbox_2d": [373, 437, 440, 448], "page": 1},
 {"key": "debts.0.refinance", "value": "유지", "bbox_2d": [475, 437, 504, 448], "page": 1},
 {"key": "debts.1.lender", "value": "새마을금고", "bbox_2d": [89, 455, 160, 465], "page": 1},
 {"key": "debts.1.kind", "value": "학자금대출", "bbox_2d": [188, 455, 260, 465], "page": 1},
 {"key": "debts.1.balance", "value": "13,100,000", "bbox_2d": [288, 455, 352, 465], "page": 1},
 {"key": "debts.1.maturity", "value": "2030-04-13", "bbox_2d": [373, 455, 440, 465], "page": 1},
 {"key": "assets.0.kind", "value": "아파트", "bbox_2d": [547, 437, 590, 448], "page": 1},
 {"key": "assets.0.value", "value": "1,560,000,000", "bbox_2d": [838, 437, 921, 448], "page": 1},
 {"key": "assets.1.kind", "value": "예금", "bbox_2d": [554, 455, 583, 465], "page": 1},
 {"key": "assets.1.location", "value": "국민은행, 카카오뱅크", "bbox_2d": [607, 455, 744, 465], "page": 1},
 {"key": "assets.1.value", "value": "70,700,000", "bbox_2d": [856, 455, 921, 465], "page": 1},
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
- seal.customer: 신청인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 신청인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
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
 {"key": "seal.customer", "value": true, "bbox_2d": [854, 766, 911, 806], "page": 1},
 {"key": "sign.customer", "value": false}]
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
| 답의 위치 (박스) | `look/template.html.j2` 배치 (studio html 편집). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa loan_application --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions loan_application --show` · `python -m docgen.preview loan_application --out work/loan_application`
