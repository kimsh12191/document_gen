# 상업송장(Commercial Invoice) (`commercial_invoice`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card commercial_invoice · card-hash: 9f78a03a82e2 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** fx · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 상업송장(Commercial Invoice)
- **쓰이는 업무:** 해외송금
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> COMMERCIAL INVOICE (수출입 상업송장). 품목이 많으면(heavy, 프로필 단위) 여러 쪽, 합계는 마지막 쪽.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/fx.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 37칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `foreign.name` ← `shipper.name` | Shipper/Exporter | text | 1쪽 [68, 95, 235, 106] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:130 | 묻기 |
| `foreign.address` ← `shipper.address` | ShipperAddress | text | 1쪽 [68, 109, 415, 120] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:125 | 묻기 |
| `invoice_no` | InvoiceNo | text | 1쪽 [552, 95, 639, 106] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:50 | 묻기 |
| `invoice_date` | InvoiceDate | date | 1쪽 [552, 109, 634, 120] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:45 | 묻기 |
| `consignee.name` | Consignee | text | 1쪽 [68, 141, 265, 152] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:30 | 묻기 |
| `consignee.address` | ConsigneeAddress | text | 1쪽 [68, 155, 519, 180] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:25 | 묻기 |
| `notify` | NotifyParty | text | 1쪽 [68, 205, 211, 215] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:85 | 묻기 |
| `terms.delivery` | TermsofDelivery | text | 1쪽 [660, 205, 924, 215] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:145 | 묻기 |
| `terms.payment` | TermsofPayment | text | 1쪽 [662, 219, 753, 229] | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:150 | 묻기 |
| `origin` | CountryofOrigin | text | 1쪽 [658, 233, 701, 243] | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:90 | 묻기 |
| `port_of_loading` | PortofLoading | text | 1쪽 [68, 237, 177, 247] | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:100 | 묻기 |
| `final_destination` | FinalDestination | text | 1쪽 [314, 237, 418, 247] | 늘 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:40 | 묻기 |
| `carrier` | Carrier | text | 1쪽 [68, 269, 234, 279] | 늘 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:20 | 묻기 |
| `sailing_date` | Sailingonorabout | date | 1쪽 [314, 269, 404, 279] | 늘 | 템플릿 | generate.py | look/template.html.j2:62 · fields.json:120 | 묻기 |
| `marks` | MarksandNumbers | text | 1쪽 [67, 327, 159, 373] | 늘 | 템플릿 | generate.py | look/template.html.j2:71 · fields.json:80 | 묻기 |
| `items.*.description` | DescriptionofGoods | text | 1쪽 [251, 327, 504, 338] (1행) | 늘 | 템플릿 | generate.py | fields.json:175 | 묻기 |
| `items.*.model` | Model | text | 1쪽 [306, 341, 358, 352] (1행) | 늘 | 템플릿 | generate.py | fields.json:180 | 묻기 |
| `items.*.quantity` | Quantity/Unit | text | 1쪽 [593, 327, 661, 338] (1행) | 늘 | 템플릿 | generate.py | fields.json:185 | 묻기 |
| `items.*.unit_price` | Unit-price | amount | 1쪽 [717, 327, 775, 338] (1행) | 늘 | 템플릿 | generate.py | fields.json:190 | 묻기 |
| `items.*.amount` | Amount | amount | 1쪽 [850, 327, 933, 338] (1행) | 늘 | 템플릿 | generate.py | fields.json:170 | 묻기 |
| `total_quantity` | TotalPackages | text | 1쪽 [473, 641, 528, 652] | 늘 | 템플릿 | generate.py | look/template.html.j2:84 · fields.json:160 | 묻기 |
| `total_amount` | TotalAmount | amount | 1쪽 [848, 641, 933, 652] | 늘 | 템플릿 | generate.py | look/template.html.j2:85 · fields.json:155 | 묻기 |
| `signed_by` | Signedby | text | 1쪽 [564, 697, 732, 707] | 늘 | 템플릿 | generate.py | look/template.html.j2:89 · fields.json:135 | 묻기 |
| `signer` | Signer | text | 1쪽 [564, 746, 624, 757] | 늘 | 템플릿 | generate.py | look/template.html.j2:90 · fields.json:140 | 묻기 |
| `contract_no` | ContractNo | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:35 | 묻기 |
| `partial_shipment` | PartialShipment | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:50 · fields.json:95 | 묻기 |
| `manufacturer.name` | Manufacturer | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:75 | 묻기 |
| `manufacturer.address` | ManufacturerAddress | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:70 | 묻기 |
| `foreign.bank` ← `beneficiary_bank.name` | BeneficiaryBank | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:10 | 묻기 |
| `foreign.swift` ← `beneficiary_bank.swift` | BeneficiaryBankSWIFT | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:15 | 묻기 |
| `beneficiary_bank.account` | BeneficiaryAccountNo | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:5 | 묻기 |
| `price_breakdown.fob` | FOBValue | - | - | 3/16 | 템플릿 | generate.py | look/template.html.j2:80 · fields.json:105 | 묻기 |
| `price_breakdown.freight` | OceanFreight | - | - | 3/16 | 템플릿 | generate.py | look/template.html.j2:81 · fields.json:110 | 묻기 |
| `price_breakdown.insurance` | InsurancePremium | - | - | 3/16 | 템플릿 | generate.py | look/template.html.j2:82 · fields.json:115 | 묻기 |
| `lc.no` | L/CNo | - | - | 6/16 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:65 | 묻기 |
| `lc.date` | L/CDate | - | - | 6/16 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:60 | 묻기 |
| `lc.bank` | L/CIssuingBank | - | - | 6/16 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:55 | 묻기 |

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
"상업송장(Commercial Invoice)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "Tokyo Seimitsu Kogyo K.K.",
 "2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 163-0001, JAPAN",
 "TSK-2503-183",
 "03 MAR 2025",
 "MIRAE CHEMICAL CO., LTD.",
 "2F, DAESUNG PLAZA, 381-19 CHEOMDAN-RO, JEJU-SI, JEJU-DO 63431, KOREA",
 "SAME AS CONSIGNEE",
 "CIF BUSAN, KOREA (INCOTERMS 2020)",
 "D/P AT SIGHT",
 "JAPAN",
 "NAGOYA, JAPAN",
 "BUSAN, KOREA",
 "NORTHERN LIGHT V.094E",
 "March 05, 2025",
 "MIRAE",
 "C/NO. 1-69",
 "MADE IN JAPAN",
 "Board-to-Board Connector 0.5mm Pitch 40P",
 "BB-649B",
 "42,000 PCS",
 "JPY 38.29",
 "JPY 1,608,180",
 "Thick Film Chip Resistor 0603 10K OHM 1%",
 "RC-843",
 "4,700,000 PCS",
 "JPY 0.21",
 "JPY 987,000",
 "LED Driver IC, SOP-8",
 "LD-392B",
 "20,000 PCS",
 "JPY 86.02",
 "JPY 1,720,400",
 "69 CTNS",
 "JPY 4,315,580",
 "Kenji Sato"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"D/P AT SIGHT"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"JPY 1,720,400"
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
- foreign.name: Shipper/Exporter (외국 상대 이름)
- foreign.address: ShipperAddress (외국 상대 주소)
- invoice_no: InvoiceNo
- invoice_date: InvoiceDate
- consignee.name: Consignee
- consignee.address: ConsigneeAddress
- notify: NotifyParty
- terms.delivery: TermsofDelivery
- terms.payment: TermsofPayment
- origin: CountryofOrigin
- port_of_loading: PortofLoading
- final_destination: FinalDestination
- carrier: Carrier
- sailing_date: Sailingonorabout
- marks: MarksandNumbers
- items.0.description: DescriptionofGoods (1행)
- items.0.model: Model (1행)
- items.0.quantity: Quantity/Unit (1행)
- items.0.unit_price: Unit-price (1행)
- items.0.amount: Amount (1행)
- items.1.description: DescriptionofGoods (2행)
- items.1.model: Model (2행)
- items.1.quantity: Quantity/Unit (2행)
- items.1.unit_price: Unit-price (2행)
- items.1.amount: Amount (2행)
- items.2.description: DescriptionofGoods (3행)
- items.2.model: Model (3행)
- items.2.quantity: Quantity/Unit (3행)
- items.2.unit_price: Unit-price (3행)
- items.2.amount: Amount (3행)
- total_quantity: TotalPackages
- total_amount: TotalAmount
- signed_by: Signedby
- signer: Signer
```

답:

```json
[{"key": "foreign.name", "value": "Tokyo Seimitsu Kogyo K.K.", "bbox_2d": [68, 95, 235, 106], "page": 1},
 {"key": "foreign.address", "value": "2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 163-0001, JAPAN", "bbox_2d": [68, 109, 415, 120], "page": 1},
 {"key": "invoice_no", "value": "TSK-2503-183", "bbox_2d": [552, 95, 639, 106], "page": 1},
 {"key": "invoice_date", "value": "03 MAR 2025", "bbox_2d": [552, 109, 634, 120], "page": 1},
 {"key": "consignee.name", "value": "MIRAE CHEMICAL CO., LTD.", "bbox_2d": [68, 141, 265, 152], "page": 1},
 {"key": "consignee.address", "value": "2F, DAESUNG PLAZA, 381-19 CHEOMDAN-RO, JEJU-SI, JEJU-DO 63431, KOREA", "bbox_2d": [68, 155, 519, 180], "page": 1},
 {"key": "notify", "value": "SAME AS CONSIGNEE", "bbox_2d": [68, 205, 211, 215], "page": 1},
 {"key": "terms.delivery", "value": "CIF BUSAN, KOREA (INCOTERMS 2020)", "bbox_2d": [660, 205, 924, 215], "page": 1},
 {"key": "terms.payment", "value": "D/P AT SIGHT", "bbox_2d": [662, 219, 753, 229], "page": 1},
 {"key": "origin", "value": "JAPAN", "bbox_2d": [658, 233, 701, 243], "page": 1},
 {"key": "port_of_loading", "value": "NAGOYA, JAPAN", "bbox_2d": [68, 237, 177, 247], "page": 1},
 {"key": "final_destination", "value": "BUSAN, KOREA", "bbox_2d": [314, 237, 418, 247], "page": 1},
 {"key": "carrier", "value": "NORTHERN LIGHT V.094E", "bbox_2d": [68, 269, 234, 279], "page": 1},
 {"key": "sailing_date", "value": "March 05, 2025", "bbox_2d": [314, 269, 404, 279], "page": 1},
 {"key": "marks", "value": "MIRAE\nBUSAN, KOREA\nC/NO. 1-69\nMADE IN JAPAN", "bbox_2d": [67, 327, 159, 373], "page": 1},
 {"key": "items.0.description", "value": "Board-to-Board Connector 0.5mm Pitch 40P", "bbox_2d": [251, 327, 504, 338], "page": 1},
 {"key": "items.0.model", "value": "BB-649B", "bbox_2d": [306, 341, 358, 352], "page": 1},
 {"key": "items.0.quantity", "value": "42,000 PCS", "bbox_2d": [593, 327, 661, 338], "page": 1},
 {"key": "items.0.unit_price", "value": "JPY 38.29", "bbox_2d": [717, 327, 775, 338], "page": 1},
 {"key": "items.0.amount", "value": "JPY 1,608,180", "bbox_2d": [850, 327, 933, 338], "page": 1},
 {"key": "items.1.description", "value": "Thick Film Chip Resistor 0603 10K OHM 1%", "bbox_2d": [251, 381, 513, 391], "page": 1},
 {"key": "items.1.model", "value": "RC-843", "bbox_2d": [306, 395, 349, 405], "page": 1},
 {"key": "items.1.quantity", "value": "4,700,000 PCS", "bbox_2d": [576, 381, 661, 391], "page": 1},
 {"key": "items.1.unit_price", "value": "JPY 0.21", "bbox_2d": [724, 381, 775, 391], "page": 1},
 {"key": "items.1.amount", "value": "JPY 987,000", "bbox_2d": [861, 381, 933, 391], "page": 1},
 {"key": "items.2.description", "value": "LED Driver IC, SOP-8", "bbox_2d": [251, 414, 381, 425], "page": 1},
 {"key": "items.2.model", "value": "LD-392B", "bbox_2d": [306, 428, 358, 439], "page": 1},
 {"key": "items.2.quantity", "value": "20,000 PCS", "bbox_2d": [593, 414, 661, 425], "page": 1},
 {"key": "items.2.unit_price", "value": "JPY 86.02", "bbox_2d": [717, 414, 775, 425], "page": 1},
 {"key": "items.2.amount", "value": "JPY 1,720,400", "bbox_2d": [850, 414, 933, 425], "page": 1},
 {"key": "total_quantity", "value": "69 CTNS", "bbox_2d": [473, 641, 528, 652], "page": 1},
 {"key": "total_amount", "value": "JPY 4,315,580", "bbox_2d": [848, 641, 933, 652], "page": 1},
 {"key": "signed_by", "value": "Tokyo Seimitsu Kogyo K.K.", "bbox_2d": [564, 697, 732, 707], "page": 1},
 {"key": "signer", "value": "Kenji Sato", "bbox_2d": [564, 746, 624, 757], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check commercial_invoice` → `python -m docgen.formdir card commercial_invoice` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions commercial_invoice --show` · `python -m docgen.preview commercial_invoice --out work/commercial_invoice`
