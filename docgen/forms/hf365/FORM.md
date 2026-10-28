# Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(영문) (`hf365`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf365 · card-hash: 02dbe1130792 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.365 (전자금융) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 28칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `PostalCode` | PostalCode* | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:23 | 묻기 |
| `customer.address` | Address* | text | 1쪽 [163, 556, 288, 561] | 늘 | 규칙: 'Address *' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:34 | 묻기 |
| `CorporateIdentificationNo` | CorporateIdentificationNo.* | rrn | 1쪽 [336, 315, 448, 333] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:45 | 묻기 |
| `BusinessRegistrationNo` | BusinessRegistrationNo.* | biz_no | 1쪽 [334, 340, 445, 360] | 늘 | 항목명 그대로 | 값 종류 `biz_no` (항목명 자동) | fields.json:56 | 묻기 |
| `value` | (Korean)* | amount | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:68 | 묻기 |
| `value2` | (English)* | amount | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:80 | 묻기 |
| `PostalCode2` | PostalCode* | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:91 | 묻기 |
| `customer.address2` | Address* | text | 1쪽 [332, 548, 724, 572] | 늘 | 규칙: 'Address *' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:102 | 묻기 |
| `PhoneNo` | PhoneNo.* | phone | 1쪽 [329, 604, 440, 623] | 늘 | 항목명 그대로 | 값 종류 `phone` (항목명 자동) | fields.json:113 | 묻기 |
| `FaxNo` | FaxNo.* | text | 1쪽 [329, 631, 406, 650] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:125 | 묻기 |
| `목록.*.Currency` | Currency | text | 1쪽 [83, 752, 115, 769] (1행) | 늘 | 표 행 (묶음·항목명 'Currency') | 값 종류 `currency` (항목명 자동) | fields.json:137 | 묻기 |
| `목록.*.AccountNo` | AccountNo.(AccountType) | phone | 1쪽 [214, 751, 298, 769] (1행) | 늘 | 표 행 (묶음·항목명 'Account No. (Account Type)') | 값 종류 `number` (항목명 자동) | fields.json:209 | 묻기 |
| `목록.*.AccountHolderName` | AccountHolderName | text | - (1행) | 늘 | 표 행 (묶음·항목명 'Account Holder Name') | 값 종류 `text` (항목명 자동) | fields.json:281 | 묻기 |
| `목록.*.SealSignature` | Seal/Signature | text | - (1행) | 늘 | 표 행 (묶음·항목명 'Seal / Signature') | 값 종류 `text` (항목명 자동) | fields.json:353 | 묻기 |
| `Representative` | Representative* | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:480 | 묻기 |
| `customer.name` | Name* | text | 2쪽 [284, 147, 363, 165] | 늘 | 규칙: 'Name *' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:492 | 묻기 |
| `customer.address3` | Address* | text | 2쪽 [287, 171, 678, 197] | 늘 | 규칙: 'Address *' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:505 | 묻기 |
| `customer.address4` | Address* | text | 2쪽 [286, 198, 677, 220] | 늘 | 규칙: 'Address *' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:518 | 묻기 |
| `ResidentRegistrationNo` | ResidentRegistrationNo. | text | 2쪽 [286, 242, 368, 260] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:530 | 묻기 |
| `Relation` | Relation(Dept./Position) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:543 | 묻기 |
| `SignatureSeal` | Signature/Seal* | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:554 | 묻기 |
| `SignatureSeal2` | Signature/Seal | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:565 | 묻기 |
| `BankVerifiersNameSignature` | BankVerifier’sName/Signature* | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:578 | 묻기 |
| `DateSubmitted` | DateSubmitted* | date | 2쪽 [235, 717, 368, 735] | 늘 | 항목명 그대로 | 값 종류 `date` (항목명 자동) | fields.json:590 | 묻기 |
| `DateRegistered` | DateRegistered* | date | 2쪽 [237, 743, 332, 761] | 늘 | 항목명 그대로 | 값 종류 `date` (항목명 자동) | fields.json:602 | 묻기 |
| `customer.address5` | Address | text | 2쪽 [287, 446, 678, 471] | 늘 | 규칙: 'Address' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:614 | 묻기 |
| `PROXY` | PROXY | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:625 | 묻기 |
| `date` | Date | date | 2쪽 [806, 380, 895, 392] | 늘 | 규칙: 'Date' → `date` | 고객 정보 (키 `date`) | fields.json:637 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.Iherebywishto` | Iherebywishto | checkbox (Subscribe to / Change/Add / Terminate the service) | 1쪽 [307, 179, 416, 194] | 늘 | 체크 (항목명) | 보기 중 고름: Subscribe to / Change/Add / Terminate the service | fields.json:425 | 묻기 |

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
"Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "657531-6811393",
 "264-69-40618",
 "010-6144-1173",
 "3955-3969",
 "CNY",
 "USD",
 "1570-6440",
 "837-150072-49231",
 "679862-8730090",
 "남궁예태",
 "7207-6459",
 "2024년 6월 15일",
 "2024-05-01",
 "2025년 04월 01일"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"서울특별시 서초구 강남대로 357, 103동 1301호"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"USD"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- PostalCode: PostalCode* (같은 항목명 중 1번째 칸)
- customer.address: Address* (고객 주소, 같은 항목명 중 1번째 칸)
- CorporateIdentificationNo: CorporateIdentificationNo.*
- value2: (English)*
- PostalCode2: PostalCode* (같은 항목명 중 2번째 칸)
- PhoneNo: PhoneNo.*
- FaxNo: FaxNo.*
- 목록.0.Currency: Currency (목록 1행)
- 목록.1.Currency: Currency (목록 2행)
- 목록.2.Currency: Currency (목록 3행)
- 목록.3.Currency: Currency (목록 4행)
- 목록.4.Currency: Currency (목록 5행)
- 목록.5.Currency: Currency (목록 6행)
- 목록.0.AccountNo: AccountNo.(AccountType) (목록 1행)
- 목록.2.AccountNo: AccountNo.(AccountType) (목록 3행)
- 목록.3.AccountNo: AccountNo.(AccountType) (목록 4행)
- 목록.4.AccountNo: AccountNo.(AccountType) (목록 5행)
- 목록.5.AccountNo: AccountNo.(AccountType) (목록 6행)
- 목록.0.AccountHolderName: AccountHolderName (목록 1행)
- 목록.1.AccountHolderName: AccountHolderName (목록 2행)
- 목록.2.AccountHolderName: AccountHolderName (목록 3행)
- 목록.3.AccountHolderName: AccountHolderName (목록 4행)
- 목록.4.AccountHolderName: AccountHolderName (목록 5행)
- 목록.5.AccountHolderName: AccountHolderName (목록 6행)
- 목록.0.SealSignature: Seal/Signature (목록 1행)
- 목록.1.SealSignature: Seal/Signature (목록 2행)
- 목록.2.SealSignature: Seal/Signature (목록 3행)
- 목록.3.SealSignature: Seal/Signature (목록 4행)
- 목록.4.SealSignature: Seal/Signature (목록 5행)
- 목록.5.SealSignature: Seal/Signature (목록 6행)
- customer.name: Name* (고객 성명)
- customer.address3: Address* (같은 항목명 중 3번째 칸)
- customer.address4: Address* (같은 항목명 중 4번째 칸)
- Relation: Relation(Dept./Position)
- SignatureSeal: Signature/Seal* (같은 항목명 중 1번째 칸)
- SignatureSeal2: Signature/Seal (같은 항목명 중 2번째 칸)
- DateSubmitted: DateSubmitted*
- DateRegistered: DateRegistered*
- PROXY: PROXY
- date: Date
```

답:

```json
[{"key": "PostalCode", "value": null},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [163, 556, 288, 561], "page": 1},
 {"key": "CorporateIdentificationNo", "value": "657531-6811393", "bbox_2d": [336, 315, 448, 333], "page": 1},
 {"key": "value2", "value": null},
 {"key": "PostalCode2", "value": null},
 {"key": "PhoneNo", "value": "010-6144-1173", "bbox_2d": [329, 604, 440, 623], "page": 1},
 {"key": "FaxNo", "value": "3955-3969", "bbox_2d": [329, 631, 406, 650], "page": 1},
 {"key": "목록.0.Currency", "value": "CNY", "bbox_2d": [83, 752, 115, 769], "page": 1},
 {"key": "목록.1.Currency", "value": "CNY", "bbox_2d": [83, 779, 116, 796], "page": 1},
 {"key": "목록.2.Currency", "value": "USD", "bbox_2d": [76, 806, 107, 824], "page": 1},
 {"key": "목록.3.Currency", "value": null},
 {"key": "목록.4.Currency", "value": null},
 {"key": "목록.5.Currency", "value": null},
 {"key": "목록.0.AccountNo", "value": "1570-6440", "bbox_2d": [214, 751, 298, 769], "page": 1},
 {"key": "목록.2.AccountNo", "value": "679862-8730090", "bbox_2d": [212, 805, 337, 824], "page": 1},
 {"key": "목록.3.AccountNo", "value": null},
 {"key": "목록.4.AccountNo", "value": null},
 {"key": "목록.5.AccountNo", "value": null},
 {"key": "목록.0.AccountHolderName", "value": null},
 {"key": "목록.1.AccountHolderName", "value": null},
 {"key": "목록.2.AccountHolderName", "value": null},
 {"key": "목록.3.AccountHolderName", "value": null},
 {"key": "목록.4.AccountHolderName", "value": null},
 {"key": "목록.5.AccountHolderName", "value": null},
 {"key": "목록.0.SealSignature", "value": null},
 {"key": "목록.1.SealSignature", "value": null},
 {"key": "목록.2.SealSignature", "value": null},
 {"key": "목록.3.SealSignature", "value": null},
 {"key": "목록.4.SealSignature", "value": null},
 {"key": "목록.5.SealSignature", "value": null},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [284, 147, 363, 165], "page": 2},
 {"key": "customer.address3", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [287, 171, 678, 197], "page": 2},
 {"key": "customer.address4", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [286, 198, 677, 220], "page": 2},
 {"key": "Relation", "value": null},
 {"key": "SignatureSeal", "value": null},
 {"key": "SignatureSeal2", "value": null},
 {"key": "DateSubmitted", "value": "2024년 6월 15일", "bbox_2d": [235, 717, 368, 735], "page": 2},
 {"key": "DateRegistered", "value": "2024-05-01", "bbox_2d": [237, 743, 332, 761], "page": 2},
 {"key": "PROXY", "value": null},
 {"key": "date", "value": "2025년 04월 01일", "bbox_2d": [806, 380, 895, 392], "page": 2}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- check.Iherebywishto: Iherebywishto (체크박스, 보기: Subscribe to / Change/Add / Terminate the service)
```

답:

```json
[{"key": "check.Iherebywishto", "value": "Change/Add", "bbox_2d": [307, 181, 323, 194], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf365` → `python -m docgen.formdir card hf365` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | studio ① 서식 › 영역 편집에서 그리기 (`fields.json` items 에 한 칸) | 다시 |
| 답의 위치 (박스) | `fields.json` 그 칸의 `rect` [x0, y0, x1, y1] (pt) — 또는 영역 편집 | 다시 |
| 답의 키 | `fields.json` 그 칸에 `"key"` (없으면 규칙이 항목명으로 정함 — 모든 서식 공통 규칙은 studio 키 사전) | 다시 |
| 답의 값 | `fields.json` 그 칸에 `"source"` ([값 출처 목록](../_common/values.md)) 또는 값 종류 `"kind"` | 다시 |
| 칸의 항목명 | `fields.json` 그 칸의 `label` | 다시 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf365 --show` · `python -m docgen.preview hf365 --out work/hf365`
