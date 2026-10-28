# 자동이체 신청서 (`auto_transfer_application`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card auto_transfer_application · card-hash: 737656dc8baa -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 자동이체 신청서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 대출이자/원리금 자동이체 신청서.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 25칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank` | 은행명 | text | 1쪽 [102, 39, 193, 62] | 늘 | 템플릿 | generate.py | fields.json:35 | 묻기 |
| `counterparty.name` ← `biller.name` | 수납기관 | text | 1쪽 [74, 133, 203, 146] | 늘 | 템플릿 | generate.py | look/template.html.j2:14 · fields.json:45 | 묻기 |
| `branch` | 취급점 | text | 1쪽 [281, 135, 333, 145] | 늘 | 템플릿 | generate.py | look/template.html.j2:14 · fields.json:50 | 묻기 |
| `biller.fee_type` | 요금종류 | text | 1쪽 [234, 179, 416, 192] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:40 | 묻기 |
| `loan_product` | 대출상품명 | text | 1쪽 [234, 210, 328, 223] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:95 | 묻기 |
| `loan_account` | 납부자번호(대출계좌번호) | account_no | 1쪽 [652, 210, 762, 223] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:90 | 묻기 |
| `customer.name` ← `applicant.name` | 신청인 | text | 1쪽 [234, 268, 297, 280] | 늘 | 템플릿 | generate.py | look/template.html.j2:10 · fields.json:20 | 묻기 |
| `customer.birth` ← `applicant.birth` | 생년월일 | date | 1쪽 [522, 268, 595, 280] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:15 | 묻기 |
| `customer.phone` ← `applicant.phone` | 연락처 | phone | 1쪽 [234, 290, 330, 303] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:25 | 묻기 |
| `customer.address` ← `applicant.address` | 주소 | text | 1쪽 [522, 290, 842, 303] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:10 | 묻기 |
| `debit.bank` | 출금은행 | text | 1쪽 [234, 340, 297, 353] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:60 | 묻기 |
| `debit.account` | 출금계좌번호 | account_no | 1쪽 [590, 340, 710, 353] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:55 | 묻기 |
| `debit.holder` | 예금주 | text | 1쪽 [234, 363, 297, 375] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:65 | 묻기 |
| `debit.holder_birth` | 예금주생년월일 | number | 1쪽 [590, 363, 637, 375] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:70 | 묻기 |
| `debit.holder_phone` | 예금주휴대전화 | phone | 1쪽 [234, 393, 330, 406] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:75 | 묻기 |
| `transfer_day` | 출금일 | text | 1쪽 [234, 424, 293, 437] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:150 | 묻기 |
| `start_month` | 이체개시 | text | 1쪽 [590, 424, 711, 437] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:135 | 묻기 |
| `amount` | 출금금액 | text | 1쪽 [234, 447, 457, 459] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:5 | 묻기 |
| `extra_loans.*.loan_account` | 납부자번호 | account_no | 1쪽 [203, 518, 303, 528] (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:160 | 묻기 |
| `extra_loans.*.loan_product` | 대출상품 | text | 1쪽 [449, 518, 550, 528] (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:165 | 묻기 |
| `extra_loans.*.target` | 이체대상 | text | 1쪽 [660, 518, 731, 528] (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:170 | 묻기 |
| `extra_loans.*.transfer_day` | 출금일 | text | 1쪽 [818, 518, 879, 528] (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:175 | 묻기 |
| `apply_date` | 신청일 | date | 1쪽 [465, 914, 535, 926] | 늘 | 템플릿 | generate.py | look/template.html.j2:67 · fields.json:30 | 묻기 |
| `signature` | 신청인 | text | 2쪽 [731, 46, 799, 60] | 늘 | 템플릿 | generate.py | look/template.html.j2:68 · fields.json:130 | 묻기 |
| `holder_signature` | 예금주 | text | 2쪽 [731, 69, 799, 83] | 늘 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:80 | 묻기 |

## 체크·도장·서명 (marks) — 9칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `kind` | 신청구분 | checkbox (신규 / 변경 / 해지) | 1쪽 [498, 133, 529, 146] | 늘 | 템플릿 | generate.py | look/template.html.j2:15 · fields.json:85 | 묻기 |
| `target` | 이체대상 | checkbox (대출이자 / 대출원리금) | 1쪽 [754, 179, 832, 192] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:140 | 묻기 |
| `relation` | 신청인과예금주와의관계 | checkbox (본인 / 가족 / 기타) | 1쪽 [603, 393, 635, 406] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:105 | 묻기 |
| `privacy_consent` | 개인정보수집이용동의 | checkbox (동의함 / 동의하지 않음) | 1쪽 [373, 800, 416, 810] | 늘 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:100 | 묻기 |
| `third_party_consent` | 제3자제공동의 | checkbox (동의함 / 동의하지 않음) | 1쪽 [638, 800, 681, 810] | 늘 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:145 | 묻기 |
| `seal.customer` ← `seal.applicant` | 신청인 | seal | 2쪽 [849, 33, 906, 73] | 늘 | 템플릿 | generate.py | fields.json:110 | 묻기 |
| `sign.customer` ← `sign.applicant` | 신청인 | signature | 2쪽 [829, 45, 926, 62] | 늘 | 템플릿 | generate.py | fields.json:120 | 묻기 |
| `seal.holder` | 예금주 | seal | 2쪽 [849, 56, 906, 96] | 늘 | 템플릿 | generate.py | fields.json:115 | 묻기 |
| `sign.holder` | 예금주 | signature | 2쪽 [829, 68, 926, 85] | 늘 | 템플릿 | generate.py | fields.json:125 | 묻기 |

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
"795-23-4005-534"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"매월 20일"
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
- counterparty.name: 수납기관 (상대방 성명)
- branch: 취급점
- biller.fee_type: 요금종류
- loan_product: 대출상품명
- loan_account: 납부자번호(대출계좌번호)
- customer.name: 신청인 (고객 성명, 같은 항목명 중 1번째 칸)
- customer.birth: 생년월일 (고객 생년월일)
- customer.phone: 연락처 (고객 연락처)
- debit.bank: 출금은행
- debit.account: 출금계좌번호
- debit.holder_birth: 예금주생년월일
- debit.holder_phone: 예금주휴대전화
- amount: 출금금액
- extra_loans.0.loan_account: 납부자번호 (1행)
- extra_loans.0.loan_product: 대출상품 (1행)
- extra_loans.0.target: 이체대상 (1행)
- extra_loans.0.transfer_day: 출금일 (1행)
- extra_loans.1.loan_account: 납부자번호 (2행)
- extra_loans.1.loan_product: 대출상품 (2행)
- extra_loans.1.transfer_day: 출금일 (2행)
- extra_loans.2.loan_account: 납부자번호 (3행)
- extra_loans.2.loan_product: 대출상품 (3행)
- extra_loans.2.transfer_day: 출금일 (3행)
- extra_loans.3.loan_product: 대출상품 (4행)
- extra_loans.3.target: 이체대상 (4행)
- extra_loans.3.transfer_day: 출금일 (4행)
- extra_loans.4.loan_account: 납부자번호 (5행)
- extra_loans.4.loan_product: 대출상품 (5행)
- extra_loans.4.target: 이체대상 (5행)
- extra_loans.4.transfer_day: 출금일 (5행)
- extra_loans.5.loan_account: 납부자번호 (6행)
- extra_loans.5.loan_product: 대출상품 (6행)
- extra_loans.5.transfer_day: 출금일 (6행)
- extra_loans.6.loan_account: 납부자번호 (7행)
- extra_loans.6.loan_product: 대출상품 (7행)
- extra_loans.6.target: 이체대상 (7행)
- extra_loans.6.transfer_day: 출금일 (7행)
- extra_loans.7.loan_product: 대출상품 (8행)
- signature: 신청인 (같은 항목명 중 2번째 칸)
```

답:

```json
[{"key": "bank", "value": "국민은행", "bbox_2d": [102, 39, 193, 62], "page": 1},
 {"key": "counterparty.name", "value": "주식회사 국민은행", "bbox_2d": [74, 133, 203, 146], "page": 1},
 {"key": "branch", "value": "센텀지점", "bbox_2d": [281, 135, 333, 145], "page": 1},
 {"key": "biller.fee_type", "value": "대출원리금(주택담보대출)", "bbox_2d": [234, 179, 416, 192], "page": 1},
 {"key": "loan_product", "value": "주택담보대출", "bbox_2d": [234, 210, 328, 223], "page": 1},
 {"key": "loan_account", "value": "783-58-4706-019", "bbox_2d": [652, 210, 762, 223], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [234, 268, 297, 280], "page": 1},
 {"key": "customer.birth", "value": "1985-03-28", "bbox_2d": [522, 268, 595, 280], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [234, 290, 330, 303], "page": 1},
 {"key": "debit.bank", "value": "국민은행", "bbox_2d": [234, 340, 297, 353], "page": 1},
 {"key": "debit.account", "value": "478303-40-826627", "bbox_2d": [590, 340, 710, 353], "page": 1},
 {"key": "debit.holder_birth", "value": "850328", "bbox_2d": [590, 363, 637, 375], "page": 1},
 {"key": "debit.holder_phone", "value": "010-6144-1173", "bbox_2d": [234, 393, 330, 406], "page": 1},
 {"key": "amount", "value": "청구금액 전액 / 예상 1,505,510원", "bbox_2d": [234, 447, 457, 459], "page": 1},
 {"key": "extra_loans.0.loan_account", "value": "596-89-0444-540", "bbox_2d": [203, 518, 303, 528], "page": 1},
 {"key": "extra_loans.0.loan_product", "value": "예적금담보대출", "bbox_2d": [449, 518, 550, 528], "page": 1},
 {"key": "extra_loans.0.target", "value": "대출원리금", "bbox_2d": [660, 518, 731, 528], "page": 1},
 {"key": "extra_loans.0.transfer_day", "value": "매월 10일", "bbox_2d": [818, 518, 879, 528], "page": 1},
 {"key": "extra_loans.1.loan_account", "value": "795-23-4005-534", "bbox_2d": [203, 539, 303, 550], "page": 1},
 {"key": "extra_loans.1.loan_product", "value": "전세자금대출", "bbox_2d": [457, 539, 543, 550], "page": 1},
 {"key": "extra_loans.1.transfer_day", "value": "매월 10일", "bbox_2d": [818, 539, 879, 550], "page": 1},
 {"key": "extra_loans.2.loan_account", "value": "560-39-5468-502", "bbox_2d": [203, 560, 303, 571], "page": 1},
 {"key": "extra_loans.2.loan_product", "value": "보금자리론", "bbox_2d": [464, 560, 536, 571], "page": 1},
 {"key": "extra_loans.2.transfer_day", "value": "매월 10일", "bbox_2d": [818, 560, 879, 571], "page": 1},
 {"key": "extra_loans.3.loan_product", "value": "전세자금대출", "bbox_2d": [457, 581, 543, 592], "page": 1},
 {"key": "extra_loans.3.target", "value": "대출원리금", "bbox_2d": [660, 581, 731, 592], "page": 1},
 {"key": "extra_loans.3.transfer_day", "value": "매월 10일", "bbox_2d": [818, 581, 879, 592], "page": 1},
 {"key": "extra_loans.4.loan_account", "value": "271-21-4357-930", "bbox_2d": [203, 603, 303, 613], "page": 1},
 {"key": "extra_loans.4.loan_product", "value": "예적금담보대출", "bbox_2d": [449, 603, 550, 613], "page": 1},
 {"key": "extra_loans.4.target", "value": "대출원리금", "bbox_2d": [660, 603, 731, 613], "page": 1},
 {"key": "extra_loans.4.transfer_day", "value": "매월 15일", "bbox_2d": [818, 603, 879, 613], "page": 1},
 {"key": "extra_loans.5.loan_account", "value": "829-26-3143-075", "bbox_2d": [203, 624, 303, 635], "page": 1},
 {"key": "extra_loans.5.loan_product", "value": "주택담보대출", "bbox_2d": [457, 624, 543, 635], "page": 1},
 {"key": "extra_loans.5.transfer_day", "value": "매월 20일", "bbox_2d": [818, 624, 879, 635], "page": 1},
 {"key": "extra_loans.6.loan_account", "value": "820-54-2286-142", "bbox_2d": [203, 645, 303, 656], "page": 1},
 {"key": "extra_loans.6.loan_product", "value": "마이너스통장", "bbox_2d": [457, 645, 543, 656], "page": 1},
 {"key": "extra_loans.6.target", "value": "대출원리금", "bbox_2d": [660, 645, 731, 656], "page": 1},
 {"key": "extra_loans.6.transfer_day", "value": "매월 25일", "bbox_2d": [818, 645, 879, 656], "page": 1},
 {"key": "extra_loans.7.loan_product", "value": "예적금담보대출", "bbox_2d": [449, 666, 550, 677], "page": 1},
 {"key": "signature", "value": "남궁예태", "bbox_2d": [731, 46, 799, 60], "page": 2}]
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
- seal.customer: 신청인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 신청인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.holder: 예금주 (고객 본인의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.holder: 예금주 (고객 본인의 신청인, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "kind", "value": "변경", "bbox_2d": [485, 133, 494, 146], "page": 1},
 {"key": "target", "value": "대출원리금", "bbox_2d": [741, 179, 750, 192], "page": 1},
 {"key": "relation", "value": "본인", "bbox_2d": [590, 393, 599, 406], "page": 1},
 {"key": "privacy_consent", "value": "동의함", "bbox_2d": [361, 800, 370, 810], "page": 1},
 {"key": "third_party_consent", "value": "동의함", "bbox_2d": [626, 800, 635, 810], "page": 1},
 {"key": "seal.customer", "value": true, "bbox_2d": [849, 33, 906, 73], "page": 2},
 {"key": "sign.customer", "value": false},
 {"key": "seal.holder", "value": true, "bbox_2d": [849, 56, 906, 96], "page": 2},
 {"key": "sign.holder", "value": false}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check auto_transfer_application` → `python -m docgen.formdir card auto_transfer_application` (실제 질문→답 확인).

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
| 답 모양 | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions auto_transfer_application --show` · `python -m docgen.preview auto_transfer_application --out work/auto_transfer_application`
