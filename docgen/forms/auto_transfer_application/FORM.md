# 자동이체 신청서 (`auto_transfer_application`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card auto_transfer_application · card-hash: a2293e3edd1f -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 자동이체 신청서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa auto_transfer_application --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 대출이자/원리금 자동이체 신청서.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 21칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank` | 은행명 | text | 1쪽 [102, 39, 193, 62] | 늘 | 템플릿 | generate.py | fields.json:35 | 묻기 |
| `biller.name` | 수납기관 | text | 1쪽 [74, 133, 203, 146] | 늘 | 템플릿 | generate.py | look/template.html.j2:14 · fields.json:45 | 묻기 |
| `branch` | 취급점 | text | 1쪽 [281, 135, 333, 145] | 늘 | 템플릿 | generate.py | look/template.html.j2:14 · fields.json:50 | 묻기 |
| `biller.fee_type` | 요금종류 | text | 1쪽 [234, 179, 416, 192] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:40 | 묻기 |
| `loan_product` | 대출상품명 | text | 1쪽 [234, 210, 328, 223] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:95 | 묻기 |
| `loan_account` | 납부자번호(대출계좌번호) | account_no | 1쪽 [652, 210, 762, 223] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:90 | 묻기 |
| `applicant.name` | 신청인 | text | 1쪽 [234, 268, 297, 280] | 늘 | 템플릿 | generate.py | look/template.html.j2:10 · fields.json:20 | 묻기 |
| `applicant.birth` | 생년월일 | date | 1쪽 [522, 268, 595, 280] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:15 | 묻기 |
| `applicant.phone` | 연락처 | phone | 1쪽 [234, 290, 330, 303] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:25 | 묻기 |
| `applicant.address` | 주소 | text | 1쪽 [522, 290, 842, 303] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:10 | 묻기 |
| `debit.bank` | 출금은행 | text | 1쪽 [234, 340, 297, 353] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:60 | 묻기 |
| `debit.account` | 출금계좌번호 | account_no | 1쪽 [590, 340, 710, 353] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:55 | 묻기 |
| `debit.holder` | 예금주 | text | 1쪽 [234, 363, 297, 375] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:65 | 묻기 |
| `debit.holder_birth` | 예금주생년월일 | number | 1쪽 [590, 363, 637, 375] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:70 | 묻기 |
| `debit.holder_phone` | 예금주휴대전화 | phone | 1쪽 [234, 393, 330, 406] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:75 | 묻기 |
| `transfer_day` | 출금일 | text | 1쪽 [234, 424, 293, 437] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:150 | 묻기 |
| `start_month` | 이체개시 | text | 1쪽 [590, 424, 711, 437] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:135 | 묻기 |
| `amount` | 출금금액 | text | 1쪽 [234, 447, 457, 459] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:5 | 묻기 |
| `apply_date` | 신청일 | date | 1쪽 [465, 914, 535, 926] | 늘 | 템플릿 | generate.py | look/template.html.j2:67 · fields.json:30 | 묻기 |
| `signature` | 신청인 | text | 2쪽 [731, 46, 799, 60] | 늘 | 템플릿 | generate.py | look/template.html.j2:68 · fields.json:130 | 묻기 |
| `holder_signature` | 예금주 | text | 2쪽 [731, 69, 799, 83] | 늘 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:80 | 묻기 |

## 표 `extra_loans` (표 과제 table·table_read·table_find·table_qa) — 4열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `extra_loans.*.loan_account` | 납부자번호 | account_no | 1쪽 [203, 518, 303, 528] (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:160 | 묻기 |
| `extra_loans.*.loan_product` | 대출상품 | text | 1쪽 [449, 518, 550, 528] (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:165 | 묻기 |
| `extra_loans.*.target` | 이체대상 | text | 1쪽 [660, 518, 731, 528] (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:170 | 묻기 |
| `extra_loans.*.transfer_day` | 출금일 | text | 1쪽 [818, 518, 879, 528] (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:175 | 묻기 |

## 체크·도장·서명 (marks) — 9칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `kind` | 신청구분 | checkbox (신규 / 변경 / 해지) | 1쪽 [498, 133, 529, 146] | 늘 | 템플릿 | generate.py | look/template.html.j2:15 · fields.json:85 | 묻기 |
| `target` | 이체대상 | checkbox (대출이자 / 대출원리금) | 1쪽 [754, 179, 832, 192] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:140 | 묻기 |
| `relation` | 신청인과예금주와의관계 | checkbox (본인 / 가족 / 기타) | 1쪽 [603, 393, 635, 406] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:105 | 묻기 |
| `privacy_consent` | 개인정보수집이용동의 | checkbox (동의함 / 동의하지 않음) | 1쪽 [373, 800, 416, 810] | 늘 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:100 | 묻기 |
| `third_party_consent` | 제3자제공동의 | checkbox (동의함 / 동의하지 않음) | 1쪽 [638, 800, 681, 810] | 늘 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:145 | 묻기 |
| `seal.applicant` | 신청인 | seal | 2쪽 [849, 33, 906, 73] | 늘 | 템플릿 | generate.py | fields.json:110 | 묻기 |
| `sign.applicant` | 신청인 | signature | 2쪽 [829, 45, 926, 62] | 늘 | 템플릿 | generate.py | fields.json:120 | 묻기 |
| `seal.holder` | 예금주 | seal | 2쪽 [849, 56, 906, 96] | 늘 | 템플릿 | generate.py | fields.json:115 | 묻기 |
| `sign.holder` | 예금주 | signature | 2쪽 [829, 68, 926, 85] | 늘 | 템플릿 | generate.py | fields.json:125 | 묻기 |

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
"자동이체 신청서"
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
 "대출원리금(주택담보대출)",
 "주택담보대출",
 "783-58-4706-019",
 "남궁예태",
 "1985-03-28",
 "010-6144-1173",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "478303-40-826627",
 "850328",
 "매월 5일",
 "2025년 5월분부터",
 "청구금액 전액 / 예상 1,505,510원",
 "596-89-0444-540",
 "예적금담보대출",
 "대출원리금",
 "매월 10일",
 "795-23-4005-534",
 "전세자금대출",
 "대출이자",
 "560-39-5468-502",
 "보금자리론",
 "242-37-0478-701",
 "271-21-4357-930",
 "매월 15일",
 "829-26-3143-075",
 "매월 20일",
 "820-54-2286-142",
 "마이너스통장",
 "매월 25일",
 "590-71-2240-645",
 "2025.04.11"
]
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

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"560-39-5468-502"
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
- biller.name: 수납기관
- branch: 취급점
- biller.fee_type: 요금종류
- loan_product: 대출상품명
- loan_account: 납부자번호(대출계좌번호)
- applicant.name: 신청인
- applicant.birth: 생년월일
- applicant.phone: 연락처
- applicant.address: 주소
- debit.bank: 출금은행
- debit.account: 출금계좌번호
- debit.holder: 예금주
- debit.holder_birth: 예금주생년월일
- debit.holder_phone: 예금주휴대전화
- transfer_day: 출금일
- start_month: 이체개시
- amount: 출금금액
- apply_date: 신청일
```

답:

```json
[{"key": "bank", "value": "국민은행", "bbox_2d": [102, 39, 193, 62], "page": 1},
 {"key": "biller.name", "value": "주식회사 국민은행", "bbox_2d": [74, 133, 203, 146], "page": 1},
 {"key": "branch", "value": "센텀지점", "bbox_2d": [281, 135, 333, 145], "page": 1},
 {"key": "biller.fee_type", "value": "대출원리금(주택담보대출)", "bbox_2d": [234, 179, 416, 192], "page": 1},
 {"key": "loan_product", "value": "주택담보대출", "bbox_2d": [234, 210, 328, 223], "page": 1},
 {"key": "loan_account", "value": "783-58-4706-019", "bbox_2d": [652, 210, 762, 223], "page": 1},
 {"key": "applicant.name", "value": "남궁예태", "bbox_2d": [234, 268, 297, 280], "page": 1},
 {"key": "applicant.birth", "value": "1985-03-28", "bbox_2d": [522, 268, 595, 280], "page": 1},
 {"key": "applicant.phone", "value": "010-6144-1173", "bbox_2d": [234, 290, 330, 303], "page": 1},
 {"key": "applicant.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [522, 290, 842, 303], "page": 1},
 {"key": "debit.bank", "value": "국민은행", "bbox_2d": [234, 340, 297, 353], "page": 1},
 {"key": "debit.account", "value": "478303-40-826627", "bbox_2d": [590, 340, 710, 353], "page": 1},
 {"key": "debit.holder", "value": "남궁예태", "bbox_2d": [234, 363, 297, 375], "page": 1},
 {"key": "debit.holder_birth", "value": "850328", "bbox_2d": [590, 363, 637, 375], "page": 1},
 {"key": "debit.holder_phone", "value": "010-6144-1173", "bbox_2d": [234, 393, 330, 406], "page": 1},
 {"key": "transfer_day", "value": "매월 5일", "bbox_2d": [234, 424, 293, 437], "page": 1},
 {"key": "start_month", "value": "2025년 5월분부터", "bbox_2d": [590, 424, 711, 437], "page": 1},
 {"key": "amount", "value": "청구금액 전액 / 예상 1,505,510원", "bbox_2d": [234, 447, 457, 459], "page": 1},
 {"key": "apply_date", "value": "2025.04.11", "bbox_2d": [465, 914, 535, 926], "page": 1}]
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
- kind: 신청구분 (체크박스, 보기: 신규 / 변경 / 해지)
- target: 이체대상 (체크박스, 보기: 대출이자 / 대출원리금)
- relation: 신청인과예금주와의관계 (체크박스, 보기: 본인 / 가족 / 기타)
- privacy_consent: 개인정보수집이용동의 (체크박스, 보기: 동의함 / 동의하지 않음)
- third_party_consent: 제3자제공동의 (체크박스, 보기: 동의함 / 동의하지 않음)
```

답:

```json
[{"key": "kind", "value": "변경", "bbox_2d": [485, 133, 494, 146], "page": 1},
 {"key": "target", "value": "대출원리금", "bbox_2d": [741, 179, 750, 192], "page": 1},
 {"key": "relation", "value": "본인", "bbox_2d": [590, 393, 599, 406], "page": 1},
 {"key": "privacy_consent", "value": "동의함", "bbox_2d": [361, 800, 370, 810], "page": 1},
 {"key": "third_party_consent", "value": "동의함", "bbox_2d": [626, 800, 635, 810], "page": 1}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 '납부자번호'·'대출상품' 열이 있는 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 설명)
- loan_account: 납부자번호
- loan_product: 대출상품
- target: 이체대상
- location: 소재지
- transfer_day: 출금일
```

답:

```json
{
 "columns": [
  "loan_account",
  "loan_product",
  "target",
  "location",
  "transfer_day"
 ],
 "rows": [
  [
   "596-89-0444-540",
   "예적금담보대출",
   "대출원리금",
   null,
   "매월 10일"
  ],
  [
   "795-23-4005-534",
   "전세자금대출",
   "대출이자",
   null,
   "매월 10일"
  ],
  [
   "560-39-5468-502",
   "보금자리론",
   "대출이자",
   null,
   "매월 10일"
  ],
  [
   "242-37-0478-701",
   "전세자금대출",
   "대출원리금",
   null,
   "매월 10일"
  ],
  [
   "271-21-4357-930",
   "예적금담보대출",
   "대출원리금",
   null,
   "매월 15일"
  ],
  [
   "829-26-3143-075",
   "주택담보대출",
   "대출원리금",
   null,
   "매월 20일"
  ],
  [
   "820-54-2286-142",
   "마이너스통장",
   "대출원리금",
   null,
   "매월 25일"
  ],
  [
   "590-71-2240-645",
   "예적금담보대출",
   "대출원리금",
   null,
   "매월 20일"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    203,
    518,
    879,
    528
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    203,
    539,
    879,
    550
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    203,
    560,
    879,
    571
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    203,
    581,
    879,
    592
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    203,
    603,
    879,
    613
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    203,
    624,
    879,
    635
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    203,
    645,
    879,
    656
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    203,
    666,
    879,
    677
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
[{"columns": ["납부자번호", "대출상품", "이체대상", "출금일"], "bbox_2d": [125, 491, 925, 677], "page": 1, "n_rows": 8}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '이체대상'·'출금일' 열이 있는 표를 보고 답하세요. 표의 행은 모두 몇 개입니까? 머리글·합계 행과 모두 빈 행은 세지 않습니다. (숫자만 답하세요)
```

답:

```json
8
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '이체대상'·'출금일' 열이 있는 표를 보고 답하세요. '출금일' 칸이 '매월 15일'인 행은 몇 개입니까? (숫자만 답하세요)
```

답:

```json
1
```

### 표 그대로 옮기기 `table_read` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 '이체대상'·'출금일' 열이 있는 표를 머리글까지 그대로 옮겨 JSON 으로 답하세요.
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
  "No",
  "납부자번호(대출계좌번호)",
  "대출상품",
  "이체대상",
  "출금일"
 ],
 "rows": [
  [
   "2",
   "596-89-0444-540",
   "예적금담보대출",
   "대출원리금",
   "매월 10일"
  ],
  [
   "3",
   "795-23-4005-534",
   "전세자금대출",
   "대출이자",
   "매월 10일"
  ],
  [
   "4",
   "560-39-5468-502",
   "보금자리론",
   "대출이자",
   "매월 10일"
  ],
  [
   "5",
   "242-37-0478-701",
   "전세자금대출",
   "대출원리금",
   "매월 10일"
  ],
  [
   "6",
   "271-21-4357-930",
   "예적금담보대출",
   "대출원리금",
   "매월 15일"
  ],
  [
   "7",
   "829-26-3143-075",
   "주택담보대출",
   "대출원리금",
   "매월 20일"
  ],
  [
   "8",
   "820-54-2286-142",
   "마이너스통장",
   "대출원리금",
   "매월 25일"
  ],
  [
   "9",
   "590-71-2240-645",
   "예적금담보대출",
   "대출원리금",
   "매월 20일"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    75,
    513,
    925,
    534
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    75,
    534,
    925,
    555
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    75,
    555,
    925,
    576
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    75,
    576,
    925,
    598
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    75,
    598,
    925,
    619
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    75,
    619,
    925,
    640
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    75,
    640,
    925,
    662
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    75,
    662,
    925,
    683
   ],
   "page": 1
  }
 ]
}
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa auto_transfer_application --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check auto_transfer_application` → `python -m docgen.formdir card auto_transfer_application` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa auto_transfer_application --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions auto_transfer_application --show` · `python -m docgen.preview auto_transfer_application --out work/auto_transfer_application`
