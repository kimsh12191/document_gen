# 무역 매매계약서(Sales Contract) (`trade_contract`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card trade_contract · card-hash: 5675509f1016 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** fx · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 무역 매매계약서(Sales Contract)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa trade_contract --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> SALES CONTRACT (수출입 매매계약서).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/fx.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 33칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seller.name` | Seller | text | 1쪽 [357, 43, 643, 60] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:150 | 묻기 |
| `seller.address` | SellerAddress | text | 1쪽 [340, 63, 659, 73] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:145 | 묻기 |
| `buyer.name` | Buyer | text | 1쪽 [111, 133, 301, 144] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:10 | 묻기 |
| `buyer.address` | BuyerAddress | text | 1쪽 [65, 146, 551, 157] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:5 | 묻기 |
| `contract_no` | ContractNo | text | 1쪽 [847, 133, 935, 144] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:95 | 묻기 |
| `contract_date` | Date | date | 1쪽 [802, 146, 901, 157] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:90 | 묻기 |
| `total_amount` | TotalAmount | amount | 1쪽 [848, 290, 927, 300] | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:180 | 묻기 |
| `total_words` | TotalAmountinWords | text | 1쪽 [77, 309, 721, 318] | 늘 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:185 | 묻기 |
| `clauses.price_terms` | PriceTerms | text | 1쪽 [228, 333, 540, 343] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:75 | 묻기 |
| `clauses.origin` | Origin | text | 1쪽 [228, 347, 258, 357] | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:55 | 묻기 |
| `clauses.packing` | Packing | text | 1쪽 [228, 362, 587, 372] | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:60 | 묻기 |
| `clauses.shipping_mark` | ShippingMark | text | 1쪽 [222, 376, 319, 424] | 늘 | 템플릿 | generate.py | look/template.html.j2:56 · fields.json:85 | 묻기 |
| `clauses.shipment` | Shipment | text | 1쪽 [228, 428, 673, 438] | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:80 | 묻기 |
| `clauses.port_of_shipment` | PortofShipment | text | 1쪽 [228, 443, 329, 453] | 늘 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:70 | 묻기 |
| `clauses.destination` | Destination | text | 1쪽 [228, 457, 324, 467] | 늘 | 템플릿 | generate.py | look/template.html.j2:59 · fields.json:35 | 묻기 |
| `clauses.payment` | Payment | text | 1쪽 [228, 472, 553, 482] | 늘 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:65 | 묻기 |
| `clauses.insurance` | Insurance | text | 1쪽 [228, 486, 697, 496] | 9/16 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:45 | 묻기 |
| `clauses.inspection` | Inspection | text | 1쪽 [228, 501, 780, 510] | 늘 | 템플릿 | generate.py | look/template.html.j2:62 · fields.json:40 | 묻기 |
| `clauses.arbitration` | Arbitration | text | 1쪽 [228, 515, 635, 525] | 늘 | 템플릿 | generate.py | look/template.html.j2:63 · fields.json:30 | 묻기 |
| `gtc_terms.qty_tolerance` | QuantityTolerance | percent | 1쪽 [361, 588, 377, 597] | 5/16 | 템플릿 | generate.py | fields.json:125 | 묻기 |
| `gtc_terms.late_penalty` | LateShipmentPenalty | percent | 1쪽 [567, 624, 582, 633] | 5/16 | 템플릿 | generate.py | fields.json:120 | 묻기 |
| `gtc_terms.inspection_days` | InspectionPeriod(days) | number | 1쪽 [414, 672, 426, 680] | 2/16 | 템플릿 | generate.py | fields.json:110 | 묻기 |
| `gtc_terms.claim_days` | ClaimPeriod(days) | number | 1쪽 [529, 695, 541, 704] | 5/16 | 템플릿 | generate.py | fields.json:100 | 묻기 |
| `gtc_terms.warranty` | WarrantyPeriod | text | 1쪽 [557, 719, 656, 728] | 4/16 | 템플릿 | generate.py | fields.json:130 | 묻기 |
| `gtc_terms.late_interest` | LatePaymentInterest | percent | 1쪽 [397, 768, 413, 777] | 2/16 | 템플릿 | generate.py | fields.json:115 | 묻기 |
| `gtc_terms.governing_law` | GoverningLaw | text | 1쪽 [545, 819, 635, 828] | 4/16 | 템플릿 | generate.py | fields.json:105 | 묻기 |
| `buyer.signer` | BuyerSignatory | text | 2쪽 [108, 143, 219, 155] | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:20 | 묻기 |
| `buyer.title` | BuyerTitle | text | 2쪽 [101, 157, 131, 168] | 늘 | 템플릿 | generate.py | look/template.html.j2:80 · fields.json:25 | 묻기 |
| `buyer.sign_date` | BuyerSigningDate | date | 2쪽 [102, 170, 182, 181] | 늘 | 템플릿 | generate.py | look/template.html.j2:81 · fields.json:15 | 묻기 |
| `seller.signer` | SellerSignatory | text | 2쪽 [578, 143, 636, 154] | 늘 | 템플릿 | generate.py | look/template.html.j2:87 · fields.json:160 | 묻기 |
| `seller.title` | SellerTitle | text | 2쪽 [571, 157, 665, 167] | 늘 | 템플릿 | generate.py | look/template.html.j2:88 · fields.json:165 | 묻기 |
| `seller.sign_date` | SellerSigningDate | date | 2쪽 [571, 170, 643, 181] | 늘 | 템플릿 | generate.py | look/template.html.j2:89 · fields.json:155 | 묻기 |
| `clauses.manufacturer` | Manufacturer | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:50 | 묻기 |

## 표 `items` (표 과제 table·table_read·table_find·table_qa) — 5열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `items.*.description` | Commodity&Description | text | 1쪽 [128, 233, 360, 243] (1행) | 늘 | 템플릿 | generate.py | fields.json:200 | 묻기 |
| `items.*.model` | Model | text | 1쪽 [464, 233, 514, 243] (1행) | 늘 | 템플릿 | generate.py | fields.json:205 | 묻기 |
| `items.*.quantity` | Quantity | text | 1쪽 [608, 233, 670, 243] (1행) | 늘 | 템플릿 | generate.py | fields.json:210 | 묻기 |
| `items.*.unit_price` | UnitPrice | amount | 1쪽 [728, 233, 781, 243] (1행) | 늘 | 템플릿 | generate.py | fields.json:215 | 묻기 |
| `items.*.amount` | Amount | amount | 1쪽 [851, 233, 927, 243] (1행) | 늘 | 템플릿 | generate.py | fields.json:195 | 묻기 |

## 체크·도장·서명 (marks) — 4칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.buyer` | BuyerSignature | seal | - | 늘 | 템플릿 | generate.py | fields.json:135 | 묻기 |
| `sign.buyer` | BuyerSignature | signature | 2쪽 [123, 115, 387, 134] | 늘 | 템플릿 | generate.py | fields.json:170 | 묻기 |
| `seal.seller` | SellerSignature | seal | - | 늘 | 템플릿 | generate.py | fields.json:140 | 묻기 |
| `sign.seller` | SellerSignature | signature | - | 늘 | 템플릿 | generate.py | fields.json:175 | 묻기 |

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
"무역 매매계약서(Sales Contract)"
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
 "MIRAE CHEMICAL CO., LTD.",
 "2F, DAESUNG PLAZA, 381-19 CHEOMDAN-RO, JEJU-SI, JEJU-DO 63431, KOREA",
 "TSK-SC-25947",
 "January 11, 2025",
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
 "JPY 4,315,580",
 "SAY JAPANESE YEN FOUR MILLION THREE HUNDRED FIFTEEN THOUSAND FIVE HUNDRED EIGHTY ONLY",
 "CIF BUSAN, KOREA (INCOTERMS 2020), prices in JPY.",
 "Japan",
 "Export standard packing in cartons, suitable for ocean transportation.",
 "MIRAE",
 "BUSAN, KOREA",
 "C/NO. 1-UP",
 "MADE IN JAPAN",
 "Not later than March 16, 2025. Partial shipments allowed, transshipment not allowed.",
 "NAGOYA, JAPAN",
 "Documents against payment at sight through the Buyer's bank.",
 "To be covered by the Seller for 110% of invoice value against Institute Cargo Clauses (A).",
 "Inspection by an independent surveyor (SGS or equivalent) at the port of loading; cost borne by the Seller.",
 "Any dispute shall be settled by arbitration in Singapore under the SIAC Rules.",
 "3%",
 "1%",
 "14",
 "eighteen (18) months",
 "8%",
 "England and Wales",
 "Namgoong Yetae",
 "CEO",
 "13 JAN 2025",
 "Kenji Sato",
 "General Manager",
 "11 JAN 2025"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"JPY 4,315,580"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"Documents against payment at sight through the Buyer's bank."
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
- seller.name: Seller
- seller.address: SellerAddress
- buyer.name: Buyer
- buyer.address: BuyerAddress
- contract_no: ContractNo
- contract_date: Date
- total_amount: TotalAmount
- total_words: TotalAmountinWords
- clauses.price_terms: PriceTerms
- clauses.origin: Origin
- clauses.packing: Packing
- clauses.shipping_mark: ShippingMark
- clauses.shipment: Shipment
- clauses.port_of_shipment: PortofShipment
- clauses.destination: Destination
- clauses.payment: Payment
- clauses.insurance: Insurance
- clauses.inspection: Inspection
- clauses.arbitration: Arbitration
- gtc_terms.qty_tolerance: QuantityTolerance
- gtc_terms.late_penalty: LateShipmentPenalty
- gtc_terms.inspection_days: InspectionPeriod(days)
- gtc_terms.claim_days: ClaimPeriod(days)
- gtc_terms.warranty: WarrantyPeriod
- gtc_terms.late_interest: LatePaymentInterest
- gtc_terms.governing_law: GoverningLaw
- buyer.signer: BuyerSignatory
- buyer.title: BuyerTitle
- buyer.sign_date: BuyerSigningDate
- seller.signer: SellerSignatory
- seller.title: SellerTitle
- seller.sign_date: SellerSigningDate
```

답:

```json
[{"key": "seller.name", "value": "Tokyo Seimitsu Kogyo K.K.", "bbox_2d": [357, 43, 643, 60], "page": 1},
 {"key": "seller.address", "value": "2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 163-0001, JAPAN", "bbox_2d": [340, 63, 659, 73], "page": 1},
 {"key": "buyer.name", "value": "MIRAE CHEMICAL CO., LTD.", "bbox_2d": [111, 133, 301, 144], "page": 1},
 {"key": "buyer.address", "value": "2F, DAESUNG PLAZA, 381-19 CHEOMDAN-RO, JEJU-SI, JEJU-DO 63431, KOREA", "bbox_2d": [65, 146, 551, 157], "page": 1},
 {"key": "contract_no", "value": "TSK-SC-25947", "bbox_2d": [847, 133, 935, 144], "page": 1},
 {"key": "contract_date", "value": "January 11, 2025", "bbox_2d": [802, 146, 901, 157], "page": 1},
 {"key": "total_amount", "value": "JPY 4,315,580", "bbox_2d": [848, 290, 927, 300], "page": 1},
 {"key": "total_words", "value": "SAY JAPANESE YEN FOUR MILLION THREE HUNDRED FIFTEEN THOUSAND FIVE HUNDRED EIGHTY ONLY", "bbox_2d": [77, 309, 721, 318], "page": 1},
 {"key": "clauses.price_terms", "value": "CIF BUSAN, KOREA (INCOTERMS 2020), prices in JPY.", "bbox_2d": [228, 333, 540, 343], "page": 1},
 {"key": "clauses.origin", "value": "Japan", "bbox_2d": [228, 347, 258, 357], "page": 1},
 {"key": "clauses.packing", "value": "Export standard packing in cartons, suitable for ocean transportation.", "bbox_2d": [228, 362, 587, 372], "page": 1},
 {"key": "clauses.shipping_mark", "value": "MIRAE\nBUSAN, KOREA\nC/NO. 1-UP\nMADE IN JAPAN", "bbox_2d": [222, 376, 319, 424], "page": 1},
 {"key": "clauses.shipment", "value": "Not later than March 16, 2025. Partial shipments allowed, transshipment not allowed.", "bbox_2d": [228, 428, 673, 438], "page": 1},
 {"key": "clauses.port_of_shipment", "value": "NAGOYA, JAPAN", "bbox_2d": [228, 443, 329, 453], "page": 1},
 {"key": "clauses.destination", "value": "BUSAN, KOREA", "bbox_2d": [228, 457, 324, 467], "page": 1},
 {"key": "clauses.payment", "value": "Documents against payment at sight through the Buyer's bank.", "bbox_2d": [228, 472, 553, 482], "page": 1},
 {"key": "clauses.insurance", "value": "To be covered by the Seller for 110% of invoice value against Institute Cargo Clauses (A).", "bbox_2d": [228, 486, 697, 496], "page": 1},
 {"key": "clauses.inspection", "value": "Inspection by an independent surveyor (SGS or equivalent) at the port of loading; cost borne by the Seller.", "bbox_2d": [228, 501, 780, 510], "page": 1},
 {"key": "clauses.arbitration", "value": "Any dispute shall be settled by arbitration in Singapore under the SIAC Rules.", "bbox_2d": [228, 515, 635, 525], "page": 1},
 {"key": "gtc_terms.qty_tolerance", "value": "3%", "bbox_2d": [361, 588, 377, 597], "page": 1},
 {"key": "gtc_terms.late_penalty", "value": "1%", "bbox_2d": [567, 624, 582, 633], "page": 1},
 {"key": "gtc_terms.inspection_days", "value": "14", "bbox_2d": [414, 672, 426, 680], "page": 1},
 {"key": "gtc_terms.claim_days", "value": "14", "bbox_2d": [529, 695, 541, 704], "page": 1},
 {"key": "gtc_terms.warranty", "value": "eighteen (18) months", "bbox_2d": [557, 719, 656, 728], "page": 1},
 {"key": "gtc_terms.late_interest", "value": "8%", "bbox_2d": [397, 768, 413, 777], "page": 1},
 {"key": "gtc_terms.governing_law", "value": "England and Wales", "bbox_2d": [545, 819, 635, 828], "page": 1},
 {"key": "buyer.signer", "value": "Namgoong Yetae", "bbox_2d": [108, 143, 219, 155], "page": 2},
 {"key": "buyer.title", "value": "CEO", "bbox_2d": [101, 157, 131, 168], "page": 2},
 {"key": "buyer.sign_date", "value": "13 JAN 2025", "bbox_2d": [102, 170, 182, 181], "page": 2},
 {"key": "seller.signer", "value": "Kenji Sato", "bbox_2d": [578, 143, 636, 154], "page": 2},
 {"key": "seller.title", "value": "General Manager", "bbox_2d": [571, 157, 665, 167], "page": 2},
 {"key": "seller.sign_date", "value": "11 JAN 2025", "bbox_2d": [571, 170, 643, 181], "page": 2}]
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
- seal.buyer: BuyerSignature (같은 설명 중 1번째 칸, 도장)
- sign.buyer: BuyerSignature (같은 설명 중 2번째 칸, 서명)
- seal.seller: SellerSignature (같은 설명 중 1번째 칸, 도장)
- sign.seller: SellerSignature (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.buyer", "value": false},
 {"key": "sign.buyer", "value": true, "bbox_2d": [123, 115, 387, 134], "page": 2},
 {"key": "seal.seller", "value": false},
 {"key": "sign.seller", "value": false}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 설명)
- packages: ContainerPackages
- description: Commodity&Description
- model: Model
- quantity: Quantity
- unit_price: UnitPrice
- amount: Amount
```

답:

```json
{
 "columns": [
  "packages",
  "description",
  "model",
  "quantity",
  "unit_price",
  "amount"
 ],
 "rows": [
  [
   null,
   "Board-to-Board Connector 0.5mm Pitch 40P",
   "BB-649B",
   "42,000 PCS",
   "JPY 38.29",
   "JPY 1,608,180"
  ],
  [
   null,
   "Thick Film Chip Resistor 0603 10K OHM 1%",
   "RC-843",
   "4,700,000 PCS",
   "JPY 0.21",
   "JPY 987,000"
  ],
  [
   null,
   "LED Driver IC, SOP-8",
   "LD-392B",
   "20,000 PCS",
   "JPY 86.02",
   "JPY 1,720,400"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    128,
    233,
    927,
    243
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    128,
    252,
    927,
    262
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    128,
    271,
    927,
    281
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
[{"columns": ["Commodity&Description", "Model", "Quantity", "UnitPrice", "Amount"], "bbox_2d": [121, 211, 934, 281], "page": 1, "n_rows": 3}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 표를 보고 답하세요. 위에서 1번째 행의 'Quantity' 값은 무엇입니까? 머리글은 세지 않습니다. (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"42,000 PCS"
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 표를 보고 답하세요. 'UnitPrice' 칸의 값을 모두 더하면 얼마입니까? 빈 칸은 0 으로 봅니다. (쉼표·단위 없이 숫자만 답하세요)
```

답:

```json
124.52
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa trade_contract --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check trade_contract` → `python -m docgen.formdir card trade_contract` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa trade_contract --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions trade_contract --show` · `python -m docgen.preview trade_contract --out work/trade_contract`
