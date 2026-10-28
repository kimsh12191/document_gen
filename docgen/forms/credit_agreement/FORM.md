# 대출거래약정서(가계용) (`credit_agreement`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card credit_agreement · card-hash: eb21344f9fd0 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 대출거래약정서(가계용)
- **쓰이는 업무:** 개인 신용대출, 주택담보대출, 개인사업자 대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 대출거래약정서(가계용) 첫 장. 은행연합회 표준 구성(제1조 거래조건 ~ 인지세 부담) 기준.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 35칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank` | 은행명 | text | 1쪽 [103, 39, 198, 61] | 늘 | 템플릿 | generate.py | fields.json:5 | 묻기 |
| `creditor` | 채권자 | text | 1쪽 [76, 127, 195, 138] | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:40 | 묻기 |
| `branch` | 취급점 | text | 1쪽 [274, 127, 329, 138] | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:10 | 묻기 |
| `customer.name` ← `debtor.name` | 성명 | text | 1쪽 [277, 202, 335, 212] | 늘 | 템플릿 | generate.py | look/template.html.j2:13 · fields.json:50 | 묻기 |
| `customer.rrn` ← `debtor.rrn` | 실명번호 | rrn | 1쪽 [688, 206, 787, 217] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:60 | 묻기 |
| `customer.address` ← `debtor.address` | 주소 | text | 1쪽 [215, 230, 714, 241] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:45 | 묻기 |
| `customer.phone` ← `debtor.phone` | 연락처 | phone | 1쪽 [739, 230, 824, 241] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:55 | 묻기 |
| `loan.subject` | 대출과목 | text | 1쪽 [215, 273, 302, 284] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:180 | 묻기 |
| `loan.product` | 상품명 | text | 1쪽 [698, 273, 785, 284] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:150 | 묻기 |
| `loan.account_no` | 대출계좌번호 | account_no | 1쪽 [698, 293, 799, 304] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:75 | 묻기 |
| `loan.amount_korean` | 대출(한도)금액(한글) | amount_korean | 1쪽 [215, 313, 349, 324] | 늘 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:85 | 묻기 |
| `loan.amount` | 대출(한도)금액 | amount | 1쪽 [361, 313, 448, 324] | 늘 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:80 | 묻기 |
| `loan.start_date` | 대출개시일 | date | 1쪽 [215, 333, 281, 344] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:175 | 묻기 |
| `loan.maturity` | 대출기간만료일 | date | 1쪽 [698, 333, 763, 344] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:130 | 묻기 |
| `loan.base_rate_name` | 기준금리종류 | text | 1쪽 [537, 376, 661, 386] | 늘 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:100 | 묻기 |
| `loan.base_rate` | 기준금리 | percent | 1쪽 [159, 416, 198, 429] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:95 | 묻기 |
| `loan.spread` | 가산금리 | percent | 1쪽 [344, 416, 383, 429] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:170 | 묻기 |
| `loan.pref_rate` | 우대금리 | percent | 1쪽 [560, 416, 599, 429] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:140 | 묻기 |
| `loan.applied_rate` | 대출이자율 | percent | 1쪽 [788, 416, 848, 429] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:90 | 묻기 |
| `loan.rate_reset` | 금리변동주기 | text | 1쪽 [215, 437, 422, 448] | 늘 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:155 | 묻기 |
| `loan.interest_pay` | 이자지급시기 | text | 1쪽 [731, 437, 828, 448] | 늘 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:120 | 묻기 |
| `loan.interest_calc` | 이자계산방법 | text | 1쪽 [215, 457, 431, 468] | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:115 | 묻기 |
| `loan.installment` | 분할상환횟수 | text | 1쪽 [215, 520, 294, 531] | 늘 | 템플릿 | generate.py | look/template.html.j2:62 · fields.json:110 | 묻기 |
| `loan.debit_account` | 자동이체계좌 | account_no | 1쪽 [535, 520, 708, 531] | 늘 | 템플릿 | generate.py | look/template.html.j2:62 · fields.json:105 | 묻기 |
| `loan.prepay_fee` | 중도상환해약금 | text | 1쪽 [86, 558, 519, 569] | 늘 | 템플릿 | generate.py | look/template.html.j2:66 · fields.json:145 | 묻기 |
| `loan.late_rate` | 지연배상금률 | text | 1쪽 [86, 593, 921, 617] | 늘 | 템플릿 | generate.py | look/template.html.j2:68 · fields.json:125 | 묻기 |
| `stamp_tax` | 인지세 | text | 1쪽 [558, 640, 807, 651] | 늘 | 템플릿 | generate.py | look/template.html.j2:70 · fields.json:210 | 묻기 |
| `special_terms.*` | 특약사항 | text | 2쪽 [99, 404, 713, 415] (1행) | 7/16 | 템플릿 | generate.py | - | 묻기 |
| `handwritten` | 자필기재 | text | 2쪽 [163, 492, 370, 509] | 늘 | 템플릿 | generate.py | look/template.html.j2:86 · fields.json:70 | 묻기 |
| `contract_date` | 약정일 | date | 2쪽 [91, 519, 185, 530] | 늘 | 템플릿 | generate.py | look/template.html.j2:90 · fields.json:35 | 묻기 |
| `signature` | 채무자 | text | 2쪽 [749, 519, 807, 530] | 늘 | 템플릿 | generate.py | look/template.html.j2:91 · fields.json:205 | 묻기 |
| `related.name` ← `co_borrower.name` | 공동차주성명 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:20 | 묻기 |
| `related.rrn` ← `co_borrower.rrn` | 공동차주실명번호 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:30 | 묻기 |
| `related.address` ← `co_borrower.address` | 공동차주주소 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:15 | 묻기 |
| `related.phone` ← `co_borrower.phone` | 공동차주연락처 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:25 | 묻기 |

## 체크·도장·서명 (marks) — 8칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `loan.method` | 거래구분 | checkbox (개별거래 / 한도거래) | 1쪽 [228, 293, 286, 304] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:135 | 묻기 |
| `loan.rate_type` | 금리종류 | checkbox (고정금리 / 변동금리 / 혼합금리) | 1쪽 [394, 376, 452, 386] | 늘 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:160 | 묻기 |
| `loan.repayment` | 상환방법 | checkbox (만기일시상환 / 원금균등분할상환 / 원리금균등분할상환) | 1쪽 [480, 500, 611, 511] | 늘 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:165 | 묻기 |
| `explained` | 설명이해확인 | checkbox (예 / 아니오) | 2쪽 [111, 479, 215, 490] | 늘 | 템플릿 | generate.py | look/template.html.j2:85 · fields.json:65 | 묻기 |
| `seal.customer` ← `seal.debtor` | 채무자 | seal | 2쪽 [835, 518, 924, 532] | 늘 | 템플릿 | generate.py | fields.json:190 | 묻기 |
| `sign.customer` ← `sign.debtor` | 채무자 | signature | 2쪽 [805, 510, 954, 537] | 늘 | 템플릿 | generate.py | fields.json:200 | 묻기 |
| `seal.related` ← `seal.co_borrower` | 공동차주 | 도장 | - | 2/16 | 템플릿 | generate.py | fields.json:185 | 묻기 |
| `sign.related` ← `sign.co_borrower` | 공동차주 | 서명 | - | 2/16 | 템플릿 | generate.py | fields.json:195 | 묻기 |

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
"대출거래약정서(가계용)"
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
 "주식회사 국민은행",
 "센텀지점",
 "남궁예태",
 "850328-2489940",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "010-6144-1173",
 "주택담보대출",
 "783-58-4706-019",
 "일금 삼억일백만원정",
 "301,000,000원",
 "2025.04.10",
 "2055.04.10",
 "금융채 5년물(AAA)",
 "3.15%",
 "1.54%",
 "0.30%",
 "연 4.39%",
 "최초 5년 고정 후 6개월마다 변동",
 "매월 5일 (후취)",
 "연 365일 일할 계산 (윤년은 366일)",
 "360회 (매월)",
 "국민은행 478303-40-826627",
 "중도상환금액 × 0.74% × 잔존일수 ÷ 대출기간일수 (3년 경과 시 면제)",
 "대출이자율 + 연체가산이자율 연 3% (현재 연 7.39%, 최고 연 15%)",
 "150,000원 (고객 75,000원 / 은행 75,000원)",
 "이 대출금은 생활안정자금 용도로만 사용하며, 은행이 요청하는 경우 자금 사용 증빙서류를 제출한다.",
 "채무자는 대출 실행일로부터 1개월 이내에 담보물건에 전입하여 실거주하여야 하며, 이를 이행하지 아니하는 경우 은행은 기한의 이익을 상실시킬 수 있다.",
 "기준금리 변동 시 대출이자율은 매 6개월 단위로 변경되며, 변경된 이자율은 은행 홈페이지 및 문자메시지로 통지한다.",
 "충분히 설명듣고 이해함",
 "2025년 4월 7일"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"최초 5년 고정 후 6개월마다 변동"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"남궁예태"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- bank: 은행명
- creditor: 채권자
- branch: 취급점
- customer.name: 성명 (고객 성명)
- customer.rrn: 실명번호 (고객 주민등록번호)
- customer.address: 주소 (고객 주소)
- customer.phone: 연락처 (고객 연락처)
- loan.subject: 대출과목
- loan.product: 상품명
- loan.account_no: 대출계좌번호
- loan.amount_korean: 대출(한도)금액(한글)
- loan.amount: 대출(한도)금액
- loan.start_date: 대출개시일
- loan.maturity: 대출기간만료일
- loan.base_rate_name: 기준금리종류
- loan.base_rate: 기준금리
- loan.spread: 가산금리
- loan.pref_rate: 우대금리
- loan.applied_rate: 대출이자율
- loan.rate_reset: 금리변동주기
- loan.interest_pay: 이자지급시기
- loan.interest_calc: 이자계산방법
- loan.installment: 분할상환횟수
- loan.debit_account: 자동이체계좌
- loan.prepay_fee: 중도상환해약금
- loan.late_rate: 지연배상금률
- stamp_tax: 인지세
- special_terms.0: 특약사항 (1번째)
- special_terms.1: 특약사항 (2번째)
- special_terms.2: 특약사항 (3번째)
- handwritten: 자필기재
- contract_date: 약정일
- signature: 채무자
```

답:

```json
[{"key": "bank", "value": "국민은행", "bbox_2d": [103, 39, 198, 61], "page": 1},
 {"key": "creditor", "value": "주식회사 국민은행", "bbox_2d": [76, 127, 195, 138], "page": 1},
 {"key": "branch", "value": "센텀지점", "bbox_2d": [274, 127, 329, 138], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [277, 202, 335, 212], "page": 1},
 {"key": "customer.rrn", "value": "850328-2489940", "bbox_2d": [688, 206, 787, 217], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [215, 230, 714, 241], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [739, 230, 824, 241], "page": 1},
 {"key": "loan.subject", "value": "주택담보대출", "bbox_2d": [215, 273, 302, 284], "page": 1},
 {"key": "loan.product", "value": "주택담보대출", "bbox_2d": [698, 273, 785, 284], "page": 1},
 {"key": "loan.account_no", "value": "783-58-4706-019", "bbox_2d": [698, 293, 799, 304], "page": 1},
 {"key": "loan.amount_korean", "value": "일금 삼억일백만원정", "bbox_2d": [215, 313, 349, 324], "page": 1},
 {"key": "loan.amount", "value": "301,000,000원", "bbox_2d": [361, 313, 448, 324], "page": 1},
 {"key": "loan.start_date", "value": "2025.04.10", "bbox_2d": [215, 333, 281, 344], "page": 1},
 {"key": "loan.maturity", "value": "2055.04.10", "bbox_2d": [698, 333, 763, 344], "page": 1},
 {"key": "loan.base_rate_name", "value": "금융채 5년물(AAA)", "bbox_2d": [537, 376, 661, 386], "page": 1},
 {"key": "loan.base_rate", "value": "3.15%", "bbox_2d": [159, 416, 198, 429], "page": 1},
 {"key": "loan.spread", "value": "1.54%", "bbox_2d": [344, 416, 383, 429], "page": 1},
 {"key": "loan.pref_rate", "value": "0.30%", "bbox_2d": [560, 416, 599, 429], "page": 1},
 {"key": "loan.applied_rate", "value": "연 4.39%", "bbox_2d": [788, 416, 848, 429], "page": 1},
 {"key": "loan.rate_reset", "value": "최초 5년 고정 후 6개월마다 변동", "bbox_2d": [215, 437, 422, 448], "page": 1},
 {"key": "loan.interest_pay", "value": "매월 5일 (후취)", "bbox_2d": [731, 437, 828, 448], "page": 1},
 {"key": "loan.interest_calc", "value": "연 365일 일할 계산 (윤년은 366일)", "bbox_2d": [215, 457, 431, 468], "page": 1},
 {"key": "loan.installment", "value": "360회 (매월)", "bbox_2d": [215, 520, 294, 531], "page": 1},
 {"key": "loan.debit_account", "value": "국민은행 478303-40-826627", "bbox_2d": [535, 520, 708, 531], "page": 1},
 {"key": "loan.prepay_fee", "value": "중도상환금액 × 0.74% × 잔존일수 ÷ 대출기간일수 (3년 경과 시 면제)", "bbox_2d": [86, 558, 519, 569], "page": 1},
 {"key": "loan.late_rate", "value": "대출이자율 + 연체가산이자율 연 3% (현재 연 7.39%, 최고 연 15%)", "bbox_2d": [86, 593, 921, 617], "page": 1},
 {"key": "stamp_tax", "value": "150,000원 (고객 75,000원 / 은행 75,000원)", "bbox_2d": [558, 640, 807, 651], "page": 1},
 {"key": "special_terms.0", "value": "이 대출금은 생활안정자금 용도로만 사용하며, 은행이 요청하는 경우 자금 사용 증빙서류를 제출한다.", "bbox_2d": [99, 404, 713, 415], "page": 2},
 {"key": "special_terms.1", "value": "채무자는 대출 실행일로부터 1개월 이내에 담보물건에 전입하여 실거주하여야 하며, 이를 이행하지 아니하는 경우 은행은 기한의 이익을 상실시킬 수 있다.", "bbox_2d": [99, 418, 924, 442], "page": 2},
 {"key": "special_terms.2", "value": "기준금리 변동 시 대출이자율은 매 6개월 단위로 변경되며, 변경된 이자율은 은행 홈페이지 및 문자메시지로 통지한다.", "bbox_2d": [99, 445, 813, 456], "page": 2},
 {"key": "handwritten", "value": "충분히 설명듣고 이해함", "bbox_2d": [163, 492, 370, 509], "page": 2},
 {"key": "contract_date", "value": "2025년 4월 7일", "bbox_2d": [91, 519, 185, 530], "page": 2},
 {"key": "signature", "value": "남궁예태", "bbox_2d": [749, 519, 807, 530], "page": 2}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- loan.method: 거래구분 (체크박스, 보기: 개별거래 / 한도거래)
- loan.rate_type: 금리종류 (체크박스, 보기: 고정금리 / 변동금리 / 혼합금리)
- loan.repayment: 상환방법 (체크박스, 보기: 만기일시상환 / 원금균등분할상환 / 원리금균등분할상환)
- explained: 설명이해확인 (체크박스, 보기: 예 / 아니오)
- seal.customer: 채무자 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 채무자 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "loan.method", "value": "개별거래", "bbox_2d": [215, 293, 224, 304], "page": 1},
 {"key": "loan.rate_type", "value": "혼합금리", "bbox_2d": [381, 376, 390, 386], "page": 1},
 {"key": "loan.repayment", "value": "원리금균등분할상환", "bbox_2d": [468, 500, 477, 511], "page": 1},
 {"key": "explained", "value": null},
 {"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [805, 510, 954, 537], "page": 2}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check credit_agreement` → `python -m docgen.formdir card credit_agreement` (실제 질문→답 확인).

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
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions credit_agreement --show` · `python -m docgen.preview credit_agreement --out work/credit_agreement`
