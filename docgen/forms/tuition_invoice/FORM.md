# 학비 청구서(Tuition Invoice) (`tuition_invoice`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card tuition_invoice · card-hash: 5388b882b6c2 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** fx · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 학비 청구서(Tuition Invoice)
- **쓰이는 업무:** 유학생 송금
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 해외 대학 학비 청구서 (Statement of Fees). 장학금은 입학허가서와 같은 프로필 단위 값.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/fx.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 29칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `foreign.name` ← `university.name` | University | text | 1쪽 [76, 47, 353, 69] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:105 | 묻기 |
| `foreign.office` ← `university.office` | Office | text | 1쪽 [76, 74, 227, 85] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:110 | 묻기 |
| `foreign.address` ← `university.address` | UniversityAddress | text | 1쪽 [76, 88, 315, 99] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:100 | 묻기 |
| `family.name` ← `student.name` | StudentName | text | 1쪽 [181, 130, 295, 142] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:65 | 묻기 |
| `family.id` ← `student.id` | StudentID | text | 1쪽 [181, 148, 258, 160] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:60 | 묻기 |
| `student.program` | Program | text | 1쪽 [181, 166, 451, 178] | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:70 | 묻기 |
| `invoice_no` | InvoiceNo | text | 1쪽 [798, 130, 909, 142] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:55 | 묻기 |
| `invoice_date` | InvoiceDate | date | 1쪽 [798, 148, 914, 160] | 늘 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:50 | 묻기 |
| `term` | Term | text | 1쪽 [798, 166, 858, 178] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:90 | 묻기 |
| `items.*.date` | Date | date | 1쪽 [86, 218, 157, 231] (1행) | 늘 | 템플릿 | generate.py | fields.json:150 | 묻기 |
| `items.*.description` | Description | text | 1쪽 [212, 218, 328, 231] (1행) | 늘 | 템플릿 | generate.py | fields.json:155 | 묻기 |
| `items.*.charge` | Charges | amount | 1쪽 [680, 218, 751, 231] (1행) | 늘 | 템플릿 | generate.py | fields.json:140 | 묻기 |
| `items.*.credit` | Payments/Credits | amount | 1쪽 [851, 339, 914, 352] (1행) | 13/16 | 템플릿 | generate.py | fields.json:145 | 묻기 |
| `summary.previous_balance` | PreviousBalance | amount | 1쪽 [879, 370, 914, 382] | 늘 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:85 | 묻기 |
| `summary.charges` | NewCharges | amount | 1쪽 [844, 394, 914, 406] | 늘 | 템플릿 | generate.py | look/template.html.j2:66 · fields.json:75 | 묻기 |
| `summary.credits` | Payments/Credits | amount | 1쪽 [851, 418, 914, 430] | 늘 | 템플릿 | generate.py | look/template.html.j2:67 · fields.json:80 | 묻기 |
| `total` | TotalAmountDue | amount | 1쪽 [816, 443, 914, 455] | 늘 | 템플릿 | generate.py | look/template.html.j2:68 · fields.json:95 | 묻기 |
| `due_date` | DueDate | date | 1쪽 [228, 472, 357, 487] | 늘 | 템플릿 | generate.py | look/template.html.j2:70 · fields.json:45 | 묻기 |
| `bank.beneficiary` | Beneficiary | text | 1쪽 [331, 537, 479, 549] | 늘 | 템플릿 | generate.py | look/template.html.j2:87 · fields.json:20 | 묻기 |
| `bank.bank_name` | BankName | text | 1쪽 [331, 554, 514, 567] | 늘 | 템플릿 | generate.py | look/template.html.j2:88 · fields.json:15 | 묻기 |
| `bank.swift` | SWIFT | text | 1쪽 [331, 572, 409, 585] | 늘 | 템플릿 | generate.py | look/template.html.j2:89 · fields.json:40 | 묻기 |
| `bank.account` | AccountNumber | account_no | 1쪽 [331, 590, 426, 603] | 늘 | 템플릿 | generate.py | look/template.html.j2:90 · fields.json:10 | 묻기 |
| `bank.routing_label` | RoutingLabel | text | 1쪽 [92, 608, 210, 621] | 늘 | 템플릿 | generate.py | look/template.html.j2:91 · fields.json:35 | 묻기 |
| `bank.routing` | RoutingNumber | number | 1쪽 [331, 608, 402, 621] | 늘 | 템플릿 | generate.py | look/template.html.j2:91 · fields.json:30 | 묻기 |
| `bank.reference` | PaymentReference | text | 1쪽 [331, 626, 526, 639] | 늘 | 템플릿 | generate.py | look/template.html.j2:92 · fields.json:25 | 묻기 |
| `amount_due_now` | AmountDueNow | - | - | 4/16 | 템플릿 | generate.py | look/template.html.j2:75 · fields.json:5 | 묻기 |
| `installments.*.no` | InstallmentNo | - | - (1행) | 4/16 | 템플릿 | generate.py | fields.json:130 | 묻기 |
| `installments.*.due_date` | InstallmentDueDate | - | - (1행) | 4/16 | 템플릿 | generate.py | fields.json:125 | 묻기 |
| `installments.*.amount` | InstallmentAmount | - | - (1행) | 4/16 | 템플릿 | generate.py | fields.json:120 | 묻기 |

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
"학비 청구서(Tuition Invoice)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "Northbridge University",
 "Office of Student Accounts",
 "300 College Ave, Boston, MA 02115, USA",
 "Yetae Namgoong",
 "M67186886",
 "Master of Business Administration (MBA)",
 "INV-2025797204",
 "February 19, 2025",
 "Fall 2025",
 "02/18/2025",
 "Tuition - Graduate",
 "$27,090.00",
 "02/19/2025",
 "Student Activity Fee",
 "$352.00",
 "02/16/2025",
 "Technology Fee",
 "$305.00",
 "Student Health Insurance Plan",
 "$2,400.00",
 "International Student Service Fee",
 "$162.00",
 "Presidential Scholarship",
 "$4,060.00",
 "$0.00",
 "$30,309.00",
 "USD 26,249.00",
 "August 09, 2025",
 "JPMorgan Chase Bank, N.A.",
 "CHASUS33",
 "528122845524",
 "ABA Routing No.",
 "024679354",
 "M67186886 Yetae Namgoong"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"Student Activity Fee"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"International Student Service Fee"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- foreign.name: University (외국 상대 이름)
- foreign.office: Office (외국 상대 사무소)
- foreign.address: UniversityAddress (외국 상대 주소)
- family.name: StudentName (가족 성명)
- family.id: StudentID (가족 번호)
- student.program: Program
- invoice_no: InvoiceNo
- invoice_date: InvoiceDate
- term: Term
- items.0.date: Date (1행)
- items.0.description: Description (1행)
- items.0.charge: Charges (1행)
- items.1.date: Date (2행)
- items.1.description: Description (2행)
- items.1.charge: Charges (2행)
- items.2.date: Date (3행)
- items.2.description: Description (3행)
- items.2.charge: Charges (3행)
- items.3.date: Date (4행)
- items.3.description: Description (4행)
- items.3.charge: Charges (4행)
- items.4.date: Date (5행)
- items.4.description: Description (5행)
- items.4.charge: Charges (5행)
- items.5.date: Date (6행)
- items.5.description: Description (6행)
- items.5.credit: Payments/Credits (6행)
- summary.previous_balance: PreviousBalance
- summary.charges: NewCharges
- summary.credits: Payments/Credits (같은 항목명 중 2번째 칸)
- total: TotalAmountDue
- due_date: DueDate
- bank.beneficiary: Beneficiary
- bank.bank_name: BankName
- bank.swift: SWIFT
- bank.account: AccountNumber
- bank.routing_label: RoutingLabel
- bank.routing: RoutingNumber
- bank.reference: PaymentReference
```

답:

```json
[{"key": "foreign.name", "value": "Northbridge University", "bbox_2d": [76, 47, 353, 69], "page": 1},
 {"key": "foreign.office", "value": "Office of Student Accounts", "bbox_2d": [76, 74, 227, 85], "page": 1},
 {"key": "foreign.address", "value": "300 College Ave, Boston, MA 02115, USA", "bbox_2d": [76, 88, 315, 99], "page": 1},
 {"key": "family.name", "value": "Yetae Namgoong", "bbox_2d": [181, 130, 295, 142], "page": 1},
 {"key": "family.id", "value": "M67186886", "bbox_2d": [181, 148, 258, 160], "page": 1},
 {"key": "student.program", "value": "Master of Business Administration (MBA)", "bbox_2d": [181, 166, 451, 178], "page": 1},
 {"key": "invoice_no", "value": "INV-2025797204", "bbox_2d": [798, 130, 909, 142], "page": 1},
 {"key": "invoice_date", "value": "February 19, 2025", "bbox_2d": [798, 148, 914, 160], "page": 1},
 {"key": "term", "value": "Fall 2025", "bbox_2d": [798, 166, 858, 178], "page": 1},
 {"key": "items.0.date", "value": "02/18/2025", "bbox_2d": [86, 218, 157, 231], "page": 1},
 {"key": "items.0.description", "value": "Tuition - Graduate", "bbox_2d": [212, 218, 328, 231], "page": 1},
 {"key": "items.0.charge", "value": "$27,090.00", "bbox_2d": [680, 218, 751, 231], "page": 1},
 {"key": "items.1.date", "value": "02/19/2025", "bbox_2d": [86, 243, 157, 255], "page": 1},
 {"key": "items.1.description", "value": "Student Activity Fee", "bbox_2d": [212, 243, 341, 255], "page": 1},
 {"key": "items.1.charge", "value": "$352.00", "bbox_2d": [699, 243, 751, 255], "page": 1},
 {"key": "items.2.date", "value": "02/16/2025", "bbox_2d": [86, 267, 157, 279], "page": 1},
 {"key": "items.2.description", "value": "Technology Fee", "bbox_2d": [212, 267, 312, 279], "page": 1},
 {"key": "items.2.charge", "value": "$305.00", "bbox_2d": [699, 267, 751, 279], "page": 1},
 {"key": "items.3.date", "value": "02/19/2025", "bbox_2d": [86, 291, 157, 303], "page": 1},
 {"key": "items.3.description", "value": "Student Health Insurance Plan", "bbox_2d": [212, 291, 403, 303], "page": 1},
 {"key": "items.3.charge", "value": "$2,400.00", "bbox_2d": [688, 291, 751, 303], "page": 1},
 {"key": "items.4.date", "value": "02/19/2025", "bbox_2d": [86, 315, 157, 328], "page": 1},
 {"key": "items.4.description", "value": "International Student Service Fee", "bbox_2d": [212, 315, 422, 328], "page": 1},
 {"key": "items.4.charge", "value": "$162.00", "bbox_2d": [699, 315, 751, 328], "page": 1},
 {"key": "items.5.date", "value": "02/16/2025", "bbox_2d": [86, 339, 157, 352], "page": 1},
 {"key": "items.5.description", "value": "Presidential Scholarship", "bbox_2d": [212, 339, 364, 352], "page": 1},
 {"key": "items.5.credit", "value": "$4,060.00", "bbox_2d": [851, 339, 914, 352], "page": 1},
 {"key": "summary.previous_balance", "value": "$0.00", "bbox_2d": [879, 370, 914, 382], "page": 1},
 {"key": "summary.charges", "value": "$30,309.00", "bbox_2d": [844, 394, 914, 406], "page": 1},
 {"key": "summary.credits", "value": "$4,060.00", "bbox_2d": [851, 418, 914, 430], "page": 1},
 {"key": "total", "value": "USD 26,249.00", "bbox_2d": [816, 443, 914, 455], "page": 1},
 {"key": "due_date", "value": "August 09, 2025", "bbox_2d": [228, 472, 357, 487], "page": 1},
 {"key": "bank.beneficiary", "value": "Northbridge University", "bbox_2d": [331, 537, 479, 549], "page": 1},
 {"key": "bank.bank_name", "value": "JPMorgan Chase Bank, N.A.", "bbox_2d": [331, 554, 514, 567], "page": 1},
 {"key": "bank.swift", "value": "CHASUS33", "bbox_2d": [331, 572, 409, 585], "page": 1},
 {"key": "bank.account", "value": "528122845524", "bbox_2d": [331, 590, 426, 603], "page": 1},
 {"key": "bank.routing_label", "value": "ABA Routing No.", "bbox_2d": [92, 608, 210, 621], "page": 1},
 {"key": "bank.routing", "value": "024679354", "bbox_2d": [331, 608, 402, 621], "page": 1},
 {"key": "bank.reference", "value": "M67186886 Yetae Namgoong", "bbox_2d": [331, 626, 526, 639], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check tuition_invoice` → `python -m docgen.formdir card tuition_invoice` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions tuition_invoice --show` · `python -m docgen.preview tuition_invoice --out work/tuition_invoice`
