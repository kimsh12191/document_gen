# 여신거래약정서(기업용) (`credit_agreement_corp`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card credit_agreement_corp · card-hash: 60bbc6fa545f -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 여신거래약정서(기업용)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa credit_agreement_corp --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 기업 여신거래약정서 첫 페이지.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 32칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank` | 은행명 | text | 1쪽 [88, 41, 186, 64] | 늘 | 템플릿 | generate.py | fields.json:5 | 묻기 |
| `creditor` | 채권자 | text | 1쪽 [60, 131, 186, 143] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:20 | 묻기 |
| `branch` | 취급점 | text | 1쪽 [269, 132, 328, 143] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:10 | 묻기 |
| `debtor.name` | 상호(법인명) | text | 1쪽 [200, 222, 302, 234] | 늘 | 템플릿 | generate.py | look/template.html.j2:26 · fields.json:45 | 묻기 |
| `debtor.biz_no` | 사업자등록번호 | biz_no | 1쪽 [200, 242, 287, 255] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:30 | 묻기 |
| `debtor.corp_no` | 법인등록번호 | corp_reg_no | 1쪽 [610, 242, 713, 255] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:40 | 묻기 |
| `debtor.ceo` | 대표이사 | text | 1쪽 [200, 263, 261, 276] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:35 | 묻기 |
| `debtor.phone` | 전화번호 | phone | 1쪽 [610, 263, 696, 276] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:50 | 묻기 |
| `debtor.address` | 본점소재지 | text | 1쪽 [200, 284, 634, 297] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:25 | 묻기 |
| `loan.subject` | 여신과목 | text | 1쪽 [200, 327, 292, 340] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:165 | 묻기 |
| `loan.product` | 상품명 | text | 1쪽 [684, 327, 806, 340] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:130 | 묻기 |
| `loan.account_no` | 여신계좌번호 | account_no | 1쪽 [684, 348, 791, 361] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:60 | 묻기 |
| `loan.amount_korean` | 여신(한도)금액(한글) | amount_korean | 1쪽 [200, 369, 311, 381] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:70 | 묻기 |
| `loan.amount` | 여신(한도)금액 | amount | 1쪽 [323, 369, 426, 381] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:65 | 묻기 |
| `loan.start_date` | 여신개시일 | date | 1쪽 [200, 390, 271, 402] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:160 | 묻기 |
| `loan.maturity` | 여신기간만료일 | date | 1쪽 [684, 390, 755, 402] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:110 | 묻기 |
| `loan.purpose` | 자금용도 | text | 1쪽 [200, 410, 295, 423] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:135 | 묻기 |
| `loan.base_rate_name` | 기준금리종류 | text | 1쪽 [450, 454, 598, 466] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:85 | 묻기 |
| `loan.base_rate` | 기준금리 | percent | 1쪽 [146, 496, 187, 508] | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:80 | 묻기 |
| `loan.spread` | 가산금리 | percent | 1쪽 [338, 496, 379, 508] | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:155 | 묻기 |
| `loan.pref_rate` | 우대금리 | percent | 1쪽 [562, 496, 603, 508] | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:120 | 묻기 |
| `loan.applied_rate` | 여신이자율 | percent | 1쪽 [798, 496, 861, 508] | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:75 | 묻기 |
| `loan.rate_reset` | 금리변동주기 | text | 1쪽 [200, 517, 238, 530] | 늘 | 템플릿 | generate.py | look/template.html.j2:50 · fields.json:140 | 묻기 |
| `loan.interest_pay` | 이자지급시기 | text | 1쪽 [573, 517, 637, 530] | 늘 | 템플릿 | generate.py | look/template.html.j2:50 · fields.json:100 | 묻기 |
| `loan.interest_calc` | 이자계산방법 | text | 1쪽 [200, 538, 523, 550] | 늘 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:95 | 묻기 |
| `loan.repayment` | 상환방법 | text | 1쪽 [200, 581, 429, 594] | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:150 | 묻기 |
| `loan.debit_account` | 자동이체계좌 | account_no | 1쪽 [200, 602, 372, 614] | 늘 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:90 | 묻기 |
| `loan.prepay_fee` | 중도상환해약금 | text | 1쪽 [71, 640, 526, 652] | 늘 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:125 | 묻기 |
| `loan.late_rate` | 지연배상금률 | text | 1쪽 [494, 688, 921, 700] | 늘 | 템플릿 | generate.py | look/template.html.j2:63 · fields.json:105 | 묻기 |
| `stamp_tax` | 인지세 | text | 1쪽 [159, 750, 435, 762] | 늘 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:190 | 묻기 |
| `contract_date` | 약정일 | date | 1쪽 [76, 826, 182, 839] | 늘 | 템플릿 | generate.py | look/template.html.j2:76 · fields.json:15 | 묻기 |
| `signature` | 대표이사 | text | 1쪽 [787, 837, 861, 851] | 늘 | 템플릿 | generate.py | look/template.html.j2:11 · fields.json:185 | 묻기 |

## 표 `special_terms` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `special_terms.*` | 특약사항 | - | - (1행) | 3/16 | 템플릿 | generate.py | - | 묻기 |

## 표 `guarantors` (표 과제 table·table_read·table_find·table_qa) — 4열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `guarantors.*.name` | 연대보증인 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:89 · fields.json:205 | 묻기 |
| `guarantors.*.rrn` | 실명번호 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:89 · fields.json:215 | 묻기 |
| `guarantors.*.address` | 주소 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:89 · fields.json:200 | 묻기 |
| `guarantors.*.relation` | 채무자와의관계 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:89 · fields.json:210 | 묻기 |

## 체크·도장·서명 (marks) — 6칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `loan.method` | 거래방법 | checkbox (개별거래 / 한도거래) | 1쪽 [213, 348, 274, 361] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:115 | 묻기 |
| `loan.rate_type` | 금리종류 | checkbox (고정금리 / 변동금리) | 1쪽 [300, 454, 361, 466] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:145 | 묻기 |
| `explained` | 설명이해확인 | checkbox (예 / 아니오) | 1쪽 [183, 786, 197, 797] | 늘 | 템플릿 | generate.py | look/template.html.j2:72 · fields.json:55 | 묻기 |
| `seal.corp` | 법인인감 | seal | 1쪽 [858, 813, 949, 877] | 늘 | 템플릿 | generate.py | fields.json:170 | 묻기 |
| `seal.guarantor` | 보증인 | 도장 | - | 1/16 | 템플릿 | generate.py | fields.json:175 | 묻기 |
| `seal.guarantor2` | 보증인 | 도장 | - | 1/16 | 템플릿 | generate.py | fields.json:180 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키는·값은:** 어디서 정해지나. 키·값 종류는 이 서식 파일에 적힌 그대로입니다 (모든 서식 공통 키 사전은 없음). "키 설명 그대로" 는 칸에 `"key"` 가 없어 키 설명이 키로 나가는 것. 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
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
"여신거래약정서(기업용)"
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
 "(주)미래케미칼",
 "702-81-38348",
 "200112-7951835",
 "남궁예태",
 "064-756-8800",
 "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)",
 "시설자금대출",
 "기업시설자금대출",
 "713-61-4840-673",
 "금 이십일억원整",
 "2,100,000,000원",
 "2025-04-14",
 "2035-04-14",
 "공장 신축자금",
 "시장금리(MOR) 6개월",
 "3.10%",
 "2.98%",
 "0.00%",
 "연 6.08%",
 "6개월",
 "매월 15일",
 "1년을 365일(윤년 366일)로 보고 1일 단위로 계산",
 "2년 거치 후 8년 원금균등분할상환",
 "국민은행 129-04-3353-660",
 "중도상환금액 × 0.70% × 잔존일수 ÷ 대출기간일수 (3년 경과 시 면제)",
 "대출이자율 + 연체가산이자율 연 3% (현재 연 9.08%, 최고 연 15%)",
 "350,000원 (고객 175,000원 / 은행 175,000원)",
 "2025년 4월 14일"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"연 6.08%"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2년 거치 후 8년 원금균등분할상환"
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
- creditor: 채권자
- branch: 취급점
- debtor.name: 상호(법인명)
- debtor.biz_no: 사업자등록번호
- debtor.corp_no: 법인등록번호
- debtor.ceo: 대표이사 (같은 설명 중 1번째 칸)
- debtor.phone: 전화번호
- debtor.address: 본점소재지
- loan.subject: 여신과목
- loan.product: 상품명
- loan.account_no: 여신계좌번호
- loan.amount_korean: 여신(한도)금액(한글)
- loan.amount: 여신(한도)금액
- loan.start_date: 여신개시일
- loan.maturity: 여신기간만료일
- loan.purpose: 자금용도
- loan.base_rate_name: 기준금리종류
- loan.base_rate: 기준금리
- loan.spread: 가산금리
- loan.pref_rate: 우대금리
- loan.applied_rate: 여신이자율
- loan.rate_reset: 금리변동주기
- loan.interest_pay: 이자지급시기
- loan.interest_calc: 이자계산방법
- loan.repayment: 상환방법
- loan.debit_account: 자동이체계좌
- loan.prepay_fee: 중도상환해약금
- loan.late_rate: 지연배상금률
- stamp_tax: 인지세
- contract_date: 약정일
- signature: 대표이사 (같은 설명 중 2번째 칸)
```

답:

```json
[{"key": "bank", "value": "국민은행", "bbox_2d": [88, 41, 186, 64], "page": 1},
 {"key": "creditor", "value": "주식회사 국민은행", "bbox_2d": [60, 131, 186, 143], "page": 1},
 {"key": "branch", "value": "센텀지점", "bbox_2d": [269, 132, 328, 143], "page": 1},
 {"key": "debtor.name", "value": "(주)미래케미칼", "bbox_2d": [200, 222, 302, 234], "page": 1},
 {"key": "debtor.biz_no", "value": "702-81-38348", "bbox_2d": [200, 242, 287, 255], "page": 1},
 {"key": "debtor.corp_no", "value": "200112-7951835", "bbox_2d": [610, 242, 713, 255], "page": 1},
 {"key": "debtor.ceo", "value": "남궁예태", "bbox_2d": [200, 263, 261, 276], "page": 1},
 {"key": "debtor.phone", "value": "064-756-8800", "bbox_2d": [610, 263, 696, 276], "page": 1},
 {"key": "debtor.address", "value": "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)", "bbox_2d": [200, 284, 634, 297], "page": 1},
 {"key": "loan.subject", "value": "시설자금대출", "bbox_2d": [200, 327, 292, 340], "page": 1},
 {"key": "loan.product", "value": "기업시설자금대출", "bbox_2d": [684, 327, 806, 340], "page": 1},
 {"key": "loan.account_no", "value": "713-61-4840-673", "bbox_2d": [684, 348, 791, 361], "page": 1},
 {"key": "loan.amount_korean", "value": "금 이십일억원整", "bbox_2d": [200, 369, 311, 381], "page": 1},
 {"key": "loan.amount", "value": "2,100,000,000원", "bbox_2d": [323, 369, 426, 381], "page": 1},
 {"key": "loan.start_date", "value": "2025-04-14", "bbox_2d": [200, 390, 271, 402], "page": 1},
 {"key": "loan.maturity", "value": "2035-04-14", "bbox_2d": [684, 390, 755, 402], "page": 1},
 {"key": "loan.purpose", "value": "공장 신축자금", "bbox_2d": [200, 410, 295, 423], "page": 1},
 {"key": "loan.base_rate_name", "value": "시장금리(MOR) 6개월", "bbox_2d": [450, 454, 598, 466], "page": 1},
 {"key": "loan.base_rate", "value": "3.10%", "bbox_2d": [146, 496, 187, 508], "page": 1},
 {"key": "loan.spread", "value": "2.98%", "bbox_2d": [338, 496, 379, 508], "page": 1},
 {"key": "loan.pref_rate", "value": "0.00%", "bbox_2d": [562, 496, 603, 508], "page": 1},
 {"key": "loan.applied_rate", "value": "연 6.08%", "bbox_2d": [798, 496, 861, 508], "page": 1},
 {"key": "loan.rate_reset", "value": "6개월", "bbox_2d": [200, 517, 238, 530], "page": 1},
 {"key": "loan.interest_pay", "value": "매월 15일", "bbox_2d": [573, 517, 637, 530], "page": 1},
 {"key": "loan.interest_calc", "value": "1년을 365일(윤년 366일)로 보고 1일 단위로 계산", "bbox_2d": [200, 538, 523, 550], "page": 1},
 {"key": "loan.repayment", "value": "2년 거치 후 8년 원금균등분할상환", "bbox_2d": [200, 581, 429, 594], "page": 1},
 {"key": "loan.debit_account", "value": "국민은행 129-04-3353-660", "bbox_2d": [200, 602, 372, 614], "page": 1},
 {"key": "loan.prepay_fee", "value": "중도상환금액 × 0.70% × 잔존일수 ÷ 대출기간일수 (3년 경과 시 면제)", "bbox_2d": [71, 640, 526, 652], "page": 1},
 {"key": "loan.late_rate", "value": "대출이자율 + 연체가산이자율 연 3% (현재 연 9.08%, 최고 연 15%)", "bbox_2d": [494, 688, 921, 700], "page": 1},
 {"key": "stamp_tax", "value": "350,000원 (고객 175,000원 / 은행 175,000원)", "bbox_2d": [159, 750, 435, 762], "page": 1},
 {"key": "contract_date", "value": "2025년 4월 14일", "bbox_2d": [76, 826, 182, 839], "page": 1},
 {"key": "signature", "value": "남궁예태", "bbox_2d": [787, 837, 861, 851], "page": 1}]
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
- loan.method: 거래방법 (체크박스, 보기: 개별거래 / 한도거래)
- loan.rate_type: 금리종류 (체크박스, 보기: 고정금리 / 변동금리)
- explained: 설명이해확인 (체크박스, 보기: 예 / 아니오)
- seal.corp: 법인인감 (도장)
```

답:

```json
[{"key": "loan.method", "value": "개별거래", "bbox_2d": [200, 348, 209, 361], "page": 1},
 {"key": "loan.rate_type", "value": "변동금리", "bbox_2d": [287, 454, 296, 466], "page": 1},
 {"key": "explained", "value": "예", "bbox_2d": [170, 786, 179, 797], "page": 1},
 {"key": "seal.corp", "value": true, "bbox_2d": [858, 813, 949, 877], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa credit_agreement_corp --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check credit_agreement_corp` → `python -m docgen.formdir card credit_agreement_corp` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa credit_agreement_corp --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions credit_agreement_corp --show` · `python -m docgen.preview credit_agreement_corp --out work/credit_agreement_corp`
