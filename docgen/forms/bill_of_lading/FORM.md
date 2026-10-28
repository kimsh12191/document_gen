# 선하증권(B/L) (`bill_of_lading`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card bill_of_lading · card-hash: 8df8f5a90247 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** fx · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 선하증권(B/L)
- **쓰이는 업무:** 해외송금
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa bill_of_lading --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> BILL OF LADING (해상 선하증권). 컨테이너가 많으면 부속 목록(ATTACHED SHEET)이 다음 쪽에 붙는다.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/fx.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 44칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `foreign.name` ← `shipper.name` | Shipper | text | 1쪽 [57, 44, 209, 53] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:150 | 묻기 |
| `foreign.address` ← `shipper.address` | ShipperAddress | text | 1쪽 [57, 55, 372, 65] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:145 | 묻기 |
| `booking_no` | BookingNo | text | 1쪽 [543, 48, 615, 58] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:10 | 묻기 |
| `bl_no` | B/LNo | text | 1쪽 [827, 44, 943, 57] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:5 | 묻기 |
| `carrier` | Carrier | text | 1쪽 [574, 63, 913, 80] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:15 | 묻기 |
| `forwarder` | ForwardingAgent | text | 1쪽 [543, 190, 670, 200] | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:45 | 묻기 |
| `consignee.name` | Consignee | text | 1쪽 [57, 108, 125, 118] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:25 | 묻기 |
| `notify.name` | NotifyParty | text | 1쪽 [57, 151, 236, 161] | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:95 | 묻기 |
| `notify.address` | NotifyPartyAddress | text | 1쪽 [57, 163, 515, 173] | 11/16 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:90 | 묻기 |
| `pre_carriage` | Pre-carriageby | text | 1쪽 [57, 215, 121, 225] | 늘 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:140 | 묻기 |
| `place_of_receipt` | PlaceofReceipt | text | 1쪽 [299, 215, 374, 225] | 늘 | 템플릿 | generate.py | look/template.html.j2:59 · fields.json:125 | 묻기 |
| `origin` | PointandCountryofOrigin | text | 1쪽 [543, 215, 582, 225] | 늘 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:105 | 묻기 |
| `vessel_voyage` | OceanVessel/VoyNo | text | 1쪽 [57, 240, 197, 250] | 늘 | 템플릿 | generate.py | look/template.html.j2:64 · fields.json:170 | 묻기 |
| `port_of_loading` | PortofLoading | text | 1쪽 [299, 240, 399, 250] | 늘 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:135 | 묻기 |
| `port_of_discharge` | PortofDischarge | text | 1쪽 [57, 266, 151, 275] | 늘 | 템플릿 | generate.py | look/template.html.j2:68 · fields.json:130 | 묻기 |
| `place_of_delivery` | PlaceofDelivery | text | 1쪽 [299, 266, 364, 275] | 늘 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:120 | 묻기 |
| `containers.*.no` | ContainerNo | text | 1쪽 [57, 306, 138, 316] (1행) | 늘 | 템플릿 | generate.py | fields.json:225 | 묻기 |
| `containers.*.type` | ContainerType | text | 1쪽 [148, 306, 179, 316] (1행) | 늘 | 템플릿 | generate.py | fields.json:217 | 묻기 |
| `containers.*.seal` | SealNo | text | 1쪽 [96, 318, 149, 328] (1행) | 늘 | 템플릿 | generate.py | fields.json:235 | 묻기 |
| `marks` | MarksandNumbers | text | 1쪽 [57, 337, 153, 382] | 늘 | 템플릿 | generate.py | look/template.html.j2:78 · fields.json:80 | 묻기 |
| `container_count` | No.ofContainers | text | 1쪽 [293, 306, 346, 316] | 늘 | 템플릿 | generate.py | look/template.html.j2:79 · fields.json:30 | 묻기 |
| `packages` | No.ofPackages | text | 1쪽 [295, 329, 344, 339] | 늘 | 템플릿 | generate.py | look/template.html.j2:79 · fields.json:115 | 묻기 |
| `description` | DescriptionofGoods | text | 1쪽 [381, 329, 700, 363] | 늘 | 템플릿 | generate.py | look/template.html.j2:80 · fields.json:35 | 묻기 |
| `freight` | Freight | text | 1쪽 [381, 377, 499, 387] | 늘 | 템플릿 | generate.py | look/template.html.j2:84 · fields.json:50 | 묻기 |
| `gross_weight` | GrossWeight | text | 1쪽 [772, 306, 836, 316] | 늘 | 템플릿 | generate.py | look/template.html.j2:86 · fields.json:60 | 묻기 |
| `measurement` | Measurement | text | 1쪽 [883, 306, 943, 316] | 늘 | 템플릿 | generate.py | look/template.html.j2:87 · fields.json:85 | 묻기 |
| `total_words` | TotalNumberinWords | text | 1쪽 [381, 628, 577, 638] | 늘 | 템플릿 | generate.py | look/template.html.j2:92 · fields.json:165 | 묻기 |
| `freight_payable_at` | FreightPayableat | text | 1쪽 [599, 659, 653, 669] | 늘 | 템플릿 | generate.py | look/template.html.j2:98 · fields.json:55 | 묻기 |
| `issue_place` | PlaceofIssue | text | 1쪽 [806, 659, 860, 669] | 늘 | 템플릿 | generate.py | look/template.html.j2:99 · fields.json:70 | 묻기 |
| `issue_date` | DateofIssue | date | 1쪽 [796, 671, 870, 681] | 늘 | 템플릿 | generate.py | look/template.html.j2:99 · fields.json:65 | 묻기 |
| `originals` | NumberofOriginalB/L | text | 1쪽 [57, 696, 120, 706] | 늘 | 템플릿 | generate.py | look/template.html.j2:100 · fields.json:110 | 묻기 |
| `on_board_date` | OnBoardDate | date | 1쪽 [435, 696, 510, 706] | 늘 | 템플릿 | generate.py | look/template.html.j2:85 · fields.json:100 | 묻기 |
| `charges.*.name` | Charge | text | 1쪽 [57, 761, 158, 771] (1행) | 6/16 | 템플릿 | generate.py | fields.json:185 | 묻기 |
| `charges.*.quantity` | RevenueTons | number | 1쪽 [462, 761, 484, 771] (1행) | 6/16 | 템플릿 | generate.py | fields.json:200 | 묻기 |
| `charges.*.rate` | Rate | number | 1쪽 [548, 761, 583, 771] (1행) | 6/16 | 템플릿 | generate.py | fields.json:205 | 묻기 |
| `charges.*.per` | Per | text | 1쪽 [621, 761, 655, 771] (1행) | 6/16 | 템플릿 | generate.py | fields.json:190 | 묻기 |
| `charges.*.prepaid` | Prepaid | amount | 1쪽 [736, 761, 800, 771] (1행) | 6/16 | 템플릿 | generate.py | fields.json:195 | 묻기 |
| `charges.*.collect` | Collect | - | - (1행) | 3/16 | 템플릿 | generate.py | fields.json:180 | 묻기 |
| `consignee.address` | ConsigneeAddress | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:20 | 묻기 |
| `containers.*.packages` | ContainerPackages | - | - (1행) | 6/16 | 템플릿 | generate.py | fields.json:230 | 묻기 |
| `containers.*.gross_weight` | ContainerGrossWeight | - | - (1행) | 6/16 | 템플릿 | generate.py | fields.json:215 | 묻기 |
| `containers.*.measurement` | ContainerMeasurement | - | - (1행) | 6/16 | 템플릿 | generate.py | fields.json:220 | 묻기 |
| `document_type` | DocumentType | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:40 | 묻기 |
| `lc_no` | L/CNo | - | - | 6/16 | 템플릿 | generate.py | look/template.html.j2:81 · fields.json:75 | 묻기 |

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
"선하증권(B/L)"
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
 "BKG4066755",
 "HBSC80990647",
 "HANBADA SHIPPING CO., LTD.",
 "Daon Logistics Co., Ltd.",
 "TO ORDER",
 "MIRAE CHEMICAL CO., LTD.",
 "2F, DAESUNG PLAZA, 381-19 CHEOMDAN-RO, JEJU-SI, JEJU-DO 63431, KOREA",
 "BY TRUCK",
 "NAGOYA CY",
 "JAPAN",
 "NORTHERN LIGHT 094E",
 "NAGOYA, JAPAN",
 "BUSAN, KOREA",
 "BUSAN CY",
 "HBDU6890876",
 "20'GP",
 "SL292105",
 "MIRAE",
 "C/NO. 1-69",
 "MADE IN JAPAN",
 "1 X 20'GP",
 "69 CTNS",
 "Board-to-Board Connector 0.5mm Pitch 40P  42,000 PCS",
 "Thick Film Chip Resistor 0603 10K OHM 1%  4,700,000 PCS",
 "LED Driver IC, SOP-8  20,000 PCS",
 "FREIGHT PREPAID",
 "565.92 KGS",
 "2.070 CBM",
 "SAY: ONE (1) CONTAINER ONLY",
 "NAGOYA",
 "05 MAR 2025",
 "THREE (3)",
 "OCEAN FREIGHT",
 "1.00",
 "450.00",
 "CNTR",
 "USD 450.00",
 "BUNKER ADJUSTMENT FACTOR (BAF)",
 "100.00",
 "USD 100.00",
 "TERMINAL HANDLING CHARGE (ORIGIN)",
 "220.00",
 "USD 220.00"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"BY TRUCK"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"Board-to-Board Connector 0.5mm Pitch 40P  42,000 PCS Thick Film Chip Resistor 0603 10K OHM 1%  4,700,000 PCS LED Driver IC, SOP-8  20,000 PCS"
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
- foreign.name: Shipper (외국 상대 이름)
- foreign.address: ShipperAddress (외국 상대 주소)
- booking_no: BookingNo
- bl_no: B/LNo
- carrier: Carrier
- consignee.name: Consignee
- notify.name: NotifyParty
- notify.address: NotifyPartyAddress
- pre_carriage: Pre-carriageby
- place_of_receipt: PlaceofReceipt
- origin: PointandCountryofOrigin
- vessel_voyage: OceanVessel/VoyNo
- port_of_loading: PortofLoading
- port_of_discharge: PortofDischarge
- place_of_delivery: PlaceofDelivery
- containers.0.no: ContainerNo (1행)
- containers.0.type: ContainerType (1행)
- marks: MarksandNumbers
- container_count: No.ofContainers
- packages: No.ofPackages
- description: DescriptionofGoods
- freight: Freight
- gross_weight: GrossWeight
- measurement: Measurement
- freight_payable_at: FreightPayableat
- issue_place: PlaceofIssue
- issue_date: DateofIssue
- on_board_date: OnBoardDate
- charges.0.name: Charge (1행)
- charges.0.quantity: RevenueTons (1행)
- charges.0.rate: Rate (1행)
- charges.0.per: Per (1행)
- charges.1.name: Charge (2행)
- charges.1.quantity: RevenueTons (2행)
- charges.1.per: Per (2행)
- charges.1.prepaid: Prepaid (2행)
- charges.2.name: Charge (3행)
- charges.2.quantity: RevenueTons (3행)
- charges.2.rate: Rate (3행)
- charges.2.prepaid: Prepaid (3행)
```

답:

```json
[{"key": "foreign.name", "value": "Tokyo Seimitsu Kogyo K.K.", "bbox_2d": [57, 44, 209, 53], "page": 1},
 {"key": "foreign.address", "value": "2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 163-0001, JAPAN", "bbox_2d": [57, 55, 372, 65], "page": 1},
 {"key": "booking_no", "value": "BKG4066755", "bbox_2d": [543, 48, 615, 58], "page": 1},
 {"key": "bl_no", "value": "HBSC80990647", "bbox_2d": [827, 44, 943, 57], "page": 1},
 {"key": "carrier", "value": "HANBADA SHIPPING CO., LTD.", "bbox_2d": [574, 63, 913, 80], "page": 1},
 {"key": "consignee.name", "value": "TO ORDER", "bbox_2d": [57, 108, 125, 118], "page": 1},
 {"key": "notify.name", "value": "MIRAE CHEMICAL CO., LTD.", "bbox_2d": [57, 151, 236, 161], "page": 1},
 {"key": "notify.address", "value": "2F, DAESUNG PLAZA, 381-19 CHEOMDAN-RO, JEJU-SI, JEJU-DO 63431, KOREA", "bbox_2d": [57, 163, 515, 173], "page": 1},
 {"key": "pre_carriage", "value": "BY TRUCK", "bbox_2d": [57, 215, 121, 225], "page": 1},
 {"key": "place_of_receipt", "value": "NAGOYA CY", "bbox_2d": [299, 215, 374, 225], "page": 1},
 {"key": "origin", "value": "JAPAN", "bbox_2d": [543, 215, 582, 225], "page": 1},
 {"key": "vessel_voyage", "value": "NORTHERN LIGHT 094E", "bbox_2d": [57, 240, 197, 250], "page": 1},
 {"key": "port_of_loading", "value": "NAGOYA, JAPAN", "bbox_2d": [299, 240, 399, 250], "page": 1},
 {"key": "port_of_discharge", "value": "BUSAN, KOREA", "bbox_2d": [57, 266, 151, 275], "page": 1},
 {"key": "place_of_delivery", "value": "BUSAN CY", "bbox_2d": [299, 266, 364, 275], "page": 1},
 {"key": "containers.0.no", "value": "HBDU6890876", "bbox_2d": [57, 306, 138, 316], "page": 1},
 {"key": "containers.0.type", "value": "20'GP", "bbox_2d": [148, 306, 179, 316], "page": 1},
 {"key": "marks", "value": "MIRAE\nBUSAN, KOREA\nC/NO. 1-69\nMADE IN JAPAN", "bbox_2d": [57, 337, 153, 382], "page": 1},
 {"key": "container_count", "value": "1 X 20'GP", "bbox_2d": [293, 306, 346, 316], "page": 1},
 {"key": "packages", "value": "69 CTNS", "bbox_2d": [295, 329, 344, 339], "page": 1},
 {"key": "description", "value": "Board-to-Board Connector 0.5mm Pitch 40P  42,000 PCS\nThick Film Chip Resistor 0603 10K OHM 1%  4,700,000 PCS\nLED Driver IC, SOP-8  20,000 PCS", "bbox_2d": [381, 329, 700, 363], "page": 1},
 {"key": "freight", "value": "FREIGHT PREPAID", "bbox_2d": [381, 377, 499, 387], "page": 1},
 {"key": "gross_weight", "value": "565.92 KGS", "bbox_2d": [772, 306, 836, 316], "page": 1},
 {"key": "measurement", "value": "2.070 CBM", "bbox_2d": [883, 306, 943, 316], "page": 1},
 {"key": "freight_payable_at", "value": "NAGOYA", "bbox_2d": [599, 659, 653, 669], "page": 1},
 {"key": "issue_place", "value": "NAGOYA", "bbox_2d": [806, 659, 860, 669], "page": 1},
 {"key": "issue_date", "value": "05 MAR 2025", "bbox_2d": [796, 671, 870, 681], "page": 1},
 {"key": "on_board_date", "value": "05 MAR 2025", "bbox_2d": [435, 696, 510, 706], "page": 1},
 {"key": "charges.0.name", "value": "OCEAN FREIGHT", "bbox_2d": [57, 761, 158, 771], "page": 1},
 {"key": "charges.0.quantity", "value": "1.00", "bbox_2d": [462, 761, 484, 771], "page": 1},
 {"key": "charges.0.rate", "value": "450.00", "bbox_2d": [548, 761, 583, 771], "page": 1},
 {"key": "charges.0.per", "value": "CNTR", "bbox_2d": [621, 761, 655, 771], "page": 1},
 {"key": "charges.1.name", "value": "BUNKER ADJUSTMENT FACTOR (BAF)", "bbox_2d": [57, 778, 285, 787], "page": 1},
 {"key": "charges.1.quantity", "value": "1.00", "bbox_2d": [462, 778, 484, 787], "page": 1},
 {"key": "charges.1.per", "value": "CNTR", "bbox_2d": [621, 778, 655, 787], "page": 1},
 {"key": "charges.1.prepaid", "value": "USD 100.00", "bbox_2d": [736, 778, 800, 787], "page": 1},
 {"key": "charges.2.name", "value": "TERMINAL HANDLING CHARGE (ORIGIN)", "bbox_2d": [57, 794, 306, 804], "page": 1},
 {"key": "charges.2.quantity", "value": "1.00", "bbox_2d": [462, 794, 484, 804], "page": 1},
 {"key": "charges.2.rate", "value": "220.00", "bbox_2d": [548, 794, 583, 804], "page": 1},
 {"key": "charges.2.prepaid", "value": "USD 220.00", "bbox_2d": [736, 794, 800, 804], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa bill_of_lading --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check bill_of_lading` → `python -m docgen.formdir card bill_of_lading` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa bill_of_lading --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions bill_of_lading --show` · `python -m docgen.preview bill_of_lading --out work/bill_of_lading`
