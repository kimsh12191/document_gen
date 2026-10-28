# 외국인투자기업등록(변경등록)신청서(영문) (`hf247`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf247 · card-hash: 9875e2f9935c -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 3 (seed 1000000 로 그린 것) · **분류 정답:** 외국인투자기업등록(변경등록)신청서(영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.247 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 24칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `ReceiptNumber` | ReceiptNumber | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:55 | 묻기 |
| `DateofReceipt` | DateofReceipt | date | 1쪽 [401, 119, 457, 132] | 늘 | 항목명 그대로 | 값 종류 `date` (항목명 자동) | fields.json:66 | 묻기 |
| `customer.name` | Name | text | 1쪽 [237, 143, 313, 161] | 늘 | 규칙: 'Name' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:77 | 묻기 |
| `Capital` | Capital(ContributionAmount) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:88 | 묻기 |
| `value` | (Korean) | amount | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:99 | 묻기 |
| `value2` | (English) | amount | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:110 | 묻기 |
| `SPCYesNo` | (*)SPC[]Yes[]No | text | 1쪽 [461, 248, 517, 260] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:121 | 묻기 |
| `Headquarters` | Headquarters | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:132 | 묻기 |
| `MainFactory` | MainFactory(MainPlaceofBusiness) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:144 | 묻기 |
| `Homepage` | Homepage(website) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:156 | 묻기 |
| `customer.name2` | Name | text | 1쪽 [448, 637, 525, 656] | 늘 | 규칙: 'Name' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:167 | 묻기 |
| `customer.name3` | Name | text | 1쪽 [445, 676, 522, 695] | 늘 | 규칙: 'Name' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:178 | 묻기 |
| `customer.email` | E-mail | text | 1쪽 [637, 334, 792, 351] | 늘 | 규칙: 'E-mail' → `customer.email` | 고객 정보 (키 `customer.email`) | fields.json:189 | 묻기 |
| `customer.nationality` | Nationality | text | 1쪽 [818, 144, 894, 161] | 늘 | 규칙: 'Nationality' → `customer.nationality` | 고객 정보 (키 `customer.nationality`) | fields.json:200 | 묻기 |
| `customer.nationality2` | Nationality | text | 1쪽 [785, 636, 861, 653] | 늘 | 규칙: 'Nationality' → `customer.nationality` | 고객 정보 (키 `customer.nationality`) | fields.json:211 | 묻기 |
| `customer.nationality3` | Nationality | text | 1쪽 [791, 677, 867, 695] | 늘 | 규칙: 'Nationality' → `customer.nationality` | 고객 정보 (키 `customer.nationality`) | fields.json:222 | 묻기 |
| `AcquisitionPricewon` | AcquisitionPrice:won(*USD) | number | 1쪽 [847, 450, 865, 466] | 늘 | 항목명 그대로 | 값 종류 `percent` (항목명 자동) | fields.json:233 | 묻기 |
| `InvestmentandParValueofStocks` | InvestmentandParValueofStocks | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:246 | 묻기 |
| `DateofCompletion` | DateofCompletion | date | 1쪽 [615, 118, 679, 131] | 늘 | 항목명 그대로 | 값 종류 `date` (항목명 자동) | fields.json:257 | 묻기 |
| `Investor` | Investor | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:269 | 묻기 |
| `customer.name4` | Name | text | 1쪽 [613, 171, 690, 189] | 늘 | 규칙: 'Name' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:281 | 묻기 |
| `Foreign` | Foreign- | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:293 | 묻기 |
| `Invested` | Invested | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:305 | 묻기 |
| `Changeof` | Changeof | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:317 | 묻기 |

## 체크·도장·서명 (marks) — 5칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.staff.담당` | 담당 | seal | 1쪽 [794, 36, 842, 70] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [786, 31, 850, 75] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [850, 31, 919, 75] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [850, 31, 919, 75] | 늘 | - | - | - | 묻기 |
| `check.agrees` | agrees | checkbox (agrees / doesn’t agree to receive a) | 2쪽 [547, 128, 622, 142] | 늘 | 체크 (항목명) | 보기 중 고름: agrees / doesn’t agree to receive a | fields.json:329 | 묻기 |

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
"외국인투자기업등록(변경등록)신청서(영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2024.03.19",
 "남궁예태",
 "4930-5015",
 "yetae741@gmail.com",
 "대한민국",
 "70",
 "2024-12-02"
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
"대한민국"
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
- ReceiptNumber: ReceiptNumber
- DateofReceipt: DateofReceipt
- customer.name: Name (고객 성명, 같은 항목명 중 1번째 칸)
- Capital: Capital(ContributionAmount)
- value: (Korean)
- value2: (English)
- SPCYesNo: (*)SPC[]Yes[]No
- Headquarters: Headquarters
- MainFactory: MainFactory(MainPlaceofBusiness)
- Homepage: Homepage(website)
- customer.name2: Name (같은 항목명 중 2번째 칸)
- customer.name3: Name (같은 항목명 중 3번째 칸)
- customer.email: E-mail (고객 이메일)
- customer.nationality: Nationality (고객 국적, 같은 항목명 중 1번째 칸)
- customer.nationality2: Nationality (같은 항목명 중 2번째 칸)
- customer.nationality3: Nationality (같은 항목명 중 3번째 칸)
- AcquisitionPricewon: AcquisitionPrice:won(*USD)
- InvestmentandParValueofStocks: InvestmentandParValueofStocks
- DateofCompletion: DateofCompletion
- Investor: Investor
- customer.name4: Name (같은 항목명 중 4번째 칸)
- Foreign: Foreign-
- Invested: Invested
- Changeof: Changeof
```

답:

```json
[{"key": "ReceiptNumber", "value": null},
 {"key": "DateofReceipt", "value": "2024.03.19", "bbox_2d": [401, 119, 457, 132], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [237, 143, 313, 161], "page": 1},
 {"key": "Capital", "value": null},
 {"key": "value", "value": null},
 {"key": "value2", "value": null},
 {"key": "SPCYesNo", "value": "4930-5015", "bbox_2d": [461, 248, 517, 260], "page": 1},
 {"key": "Headquarters", "value": null},
 {"key": "MainFactory", "value": null},
 {"key": "Homepage", "value": null},
 {"key": "customer.name2", "value": "남궁예태", "bbox_2d": [448, 637, 525, 656], "page": 1},
 {"key": "customer.name3", "value": "남궁예태", "bbox_2d": [445, 676, 522, 695], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [637, 334, 792, 351], "page": 1},
 {"key": "customer.nationality", "value": "대한민국", "bbox_2d": [818, 144, 894, 161], "page": 1},
 {"key": "customer.nationality2", "value": "대한민국", "bbox_2d": [785, 636, 861, 653], "page": 1},
 {"key": "customer.nationality3", "value": "대한민국", "bbox_2d": [791, 677, 867, 695], "page": 1},
 {"key": "AcquisitionPricewon", "value": "70", "bbox_2d": [847, 450, 865, 466], "page": 1},
 {"key": "InvestmentandParValueofStocks", "value": null},
 {"key": "DateofCompletion", "value": "2024-12-02", "bbox_2d": [615, 118, 679, 131], "page": 1},
 {"key": "Investor", "value": null},
 {"key": "customer.name4", "value": "남궁예태", "bbox_2d": [613, 171, 690, 189], "page": 1},
 {"key": "Foreign", "value": null},
 {"key": "Invested", "value": null},
 {"key": "Changeof", "value": null}]
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
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
- check.agrees: agrees (체크박스, 보기: agrees / doesn’t agree to receive a)
```

답:

```json
[{"key": "seal.staff.담당", "value": true, "bbox_2d": [794, 36, 842, 70], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": false},
 {"key": "sign.staff.책임자", "value": true, "bbox_2d": [850, 31, 919, 75], "page": 1},
 {"key": "check.agrees", "value": "agrees", "bbox_2d": [547, 130, 564, 142], "page": 2}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf247` → `python -m docgen.formdir card hf247` (실제 질문→답 확인).

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
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf247 --show` · `python -m docgen.preview hf247 --out work/hf247`
