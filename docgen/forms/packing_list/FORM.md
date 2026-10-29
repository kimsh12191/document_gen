# 포장명세서(Packing List) (`packing_list`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card packing_list · card-hash: 88d60fefbafa -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** fx · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 포장명세서(Packing List)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa packing_list --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> PACKING LIST (포장명세서). 상업송장과 같은 선적 정보. 품목이 많으면 여러 쪽, 컨테이너별로 나눠 적기도 한다.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/fx.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 23칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `foreign.name` ← `shipper.name` | Shipper/Exporter | text | 1쪽 [68, 100, 230, 111] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:85 | 묻기 |
| `foreign.address` ← `shipper.address` | ShipperAddress | text | 1쪽 [68, 115, 403, 126] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:80 | 묻기 |
| `invoice_no` | InvoiceNo | text | 1쪽 [552, 100, 636, 111] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:35 | 묻기 |
| `invoice_date` | InvoiceDate | date | 1쪽 [552, 115, 631, 126] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:30 | 묻기 |
| `consignee.name` | Consignee | text | 1쪽 [68, 149, 258, 159] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:15 | 묻기 |
| `consignee.address` | ConsigneeAddress | text | 1쪽 [68, 164, 504, 189] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:10 | 묻기 |
| `notify` | NotifyParty | text | 1쪽 [68, 212, 206, 223] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:60 | 묻기 |
| `port_of_loading` | PortofLoading | text | 1쪽 [68, 246, 173, 257] | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:70 | 묻기 |
| `final_destination` | FinalDestination | text | 1쪽 [314, 246, 414, 257] | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:25 | 묻기 |
| `carrier` | Carrier | text | 1쪽 [68, 280, 228, 290] | 늘 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:5 | 묻기 |
| `sailing_date` | Sailingonorabout | date | 1쪽 [314, 280, 401, 290] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:75 | 묻기 |
| `marks` | MarksandNumbers | text | 1쪽 [65, 332, 158, 382] | 늘 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:55 | 묻기 |
| `total.packages` | TotalPackages | text | 1쪽 [534, 633, 582, 643] | 늘 | 템플릿 | generate.py | look/template.html.j2:80 · fields.json:115 | 묻기 |
| `total.net_weight` | TotalNetWeight | text | 1쪽 [705, 633, 768, 643] | 늘 | 템플릿 | generate.py | look/template.html.j2:81 · fields.json:110 | 묻기 |
| `total.gross_weight` | TotalGrossWeight | text | 1쪽 [793, 633, 856, 643] | 늘 | 템플릿 | generate.py | look/template.html.j2:82 · fields.json:100 | 묻기 |
| `total.measurement` | TotalMeasurement | text | 1쪽 [875, 633, 935, 643] | 늘 | 템플릿 | generate.py | look/template.html.j2:83 · fields.json:105 | 묻기 |
| `signed_by` | Signedby | text | 1쪽 [564, 690, 726, 700] | 늘 | 템플릿 | generate.py | look/template.html.j2:87 · fields.json:90 | 묻기 |
| `signer` | Signer | text | 1쪽 [564, 740, 622, 751] | 늘 | 템플릿 | generate.py | look/template.html.j2:88 · fields.json:95 | 묻기 |
| `contract_no` | ContractNo | - | - | 7/16 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:20 | 묻기 |
| `partial_shipment` | PartialShipment | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:65 | 묻기 |
| `manufacturer.name` | Manufacturer | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:50 | 묻기 |
| `manufacturer.address` | ManufacturerAddress | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:45 | 묻기 |
| `lc_no` | L/CNo | - | - | 6/16 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:40 | 묻기 |

## 표 `items` (표 과제 table·table_read·table_find·table_qa) — 7열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `items.*.ctn_no` | C/TNo | text | 1쪽 [237, 332, 260, 342] (1행) | 늘 | 템플릿 | generate.py | fields.json:160 | 묻기 |
| `items.*.description` | DescriptionofGoods | text | 1쪽 [294, 332, 493, 355] (1행) | 늘 | 템플릿 | generate.py | fields.json:165 | 묻기 |
| `items.*.packages` | Packages | text | 1쪽 [536, 332, 582, 342] (1행) | 늘 | 템플릿 | generate.py | fields.json:185 | 묻기 |
| `items.*.quantity` | Quantity | text | 1쪽 [621, 332, 679, 342] (1행) | 늘 | 템플릿 | generate.py | fields.json:190 | 묻기 |
| `items.*.net_weight` | NetWeight | number | 1쪽 [734, 332, 768, 342] (1행) | 늘 | 템플릿 | generate.py | fields.json:180 | 묻기 |
| `items.*.gross_weight` | GrossWeight | number | 1쪽 [822, 332, 856, 342] (1행) | 늘 | 템플릿 | generate.py | fields.json:170 | 묻기 |
| `items.*.measurement` | Measurement | number | 1쪽 [907, 332, 935, 342] (1행) | 늘 | 템플릿 | generate.py | fields.json:175 | 묻기 |

## 표 `containers` (표 과제 table·table_read·table_find·table_qa) — 6열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `containers.*.no` | ContainerNo | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:140 | 묻기 |
| `containers.*.seal` | SealNo | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:150 | 묻기 |
| `containers.*.packages` | ContainerPackages | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:145 | 묻기 |
| `containers.*.net_weight` | ContainerNetWeight | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:135 | 묻기 |
| `containers.*.gross_weight` | ContainerGrossWeight | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:125 | 묻기 |
| `containers.*.measurement` | ContainerMeasurement | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:130 | 묻기 |

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
"포장명세서(Packing List)"
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
 "NAGOYA, JAPAN",
 "BUSAN, KOREA",
 "NORTHERN LIGHT V.094E",
 "March 05, 2025",
 "MIRAE",
 "C/NO. 1-69",
 "MADE IN JAPAN",
 "1-21",
 "Board-to-Board Connector 0.5mm Pitch 40P",
 "21 CTNS",
 "42,000 PCS",
 "189.00",
 "204.12",
 "0.630",
 "22-68",
 "Thick Film Chip Resistor 0603 10K OHM 1%",
 "47 CTNS",
 "4,700,000 PCS",
 "329.00",
 "355.32",
 "1.410",
 "69",
 "LED Driver IC, SOP-8",
 "1 CTNS",
 "20,000 PCS",
 "6.00",
 "6.48",
 "0.030",
 "69 CTNS",
 "524.00 KGS",
 "565.92 KGS",
 "2.070 CBM",
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
"MIRAE CHEMICAL CO., LTD."
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"189.00"
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
- port_of_loading: PortofLoading
- final_destination: FinalDestination
- carrier: Carrier
- sailing_date: Sailingonorabout
- marks: MarksandNumbers
- total.packages: TotalPackages
- total.net_weight: TotalNetWeight
- total.gross_weight: TotalGrossWeight
- total.measurement: TotalMeasurement
- signed_by: Signedby
- signer: Signer
```

답:

```json
[{"key": "foreign.name", "value": "Tokyo Seimitsu Kogyo K.K.", "bbox_2d": [68, 100, 230, 111], "page": 1},
 {"key": "foreign.address", "value": "2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 163-0001, JAPAN", "bbox_2d": [68, 115, 403, 126], "page": 1},
 {"key": "invoice_no", "value": "TSK-2503-183", "bbox_2d": [552, 100, 636, 111], "page": 1},
 {"key": "invoice_date", "value": "03 MAR 2025", "bbox_2d": [552, 115, 631, 126], "page": 1},
 {"key": "consignee.name", "value": "MIRAE CHEMICAL CO., LTD.", "bbox_2d": [68, 149, 258, 159], "page": 1},
 {"key": "consignee.address", "value": "2F, DAESUNG PLAZA, 381-19 CHEOMDAN-RO, JEJU-SI, JEJU-DO 63431, KOREA", "bbox_2d": [68, 164, 504, 189], "page": 1},
 {"key": "notify", "value": "SAME AS CONSIGNEE", "bbox_2d": [68, 212, 206, 223], "page": 1},
 {"key": "port_of_loading", "value": "NAGOYA, JAPAN", "bbox_2d": [68, 246, 173, 257], "page": 1},
 {"key": "final_destination", "value": "BUSAN, KOREA", "bbox_2d": [314, 246, 414, 257], "page": 1},
 {"key": "carrier", "value": "NORTHERN LIGHT V.094E", "bbox_2d": [68, 280, 228, 290], "page": 1},
 {"key": "sailing_date", "value": "March 05, 2025", "bbox_2d": [314, 280, 401, 290], "page": 1},
 {"key": "marks", "value": "MIRAE\nBUSAN, KOREA\nC/NO. 1-69\nMADE IN JAPAN", "bbox_2d": [65, 332, 158, 382], "page": 1},
 {"key": "total.packages", "value": "69 CTNS", "bbox_2d": [534, 633, 582, 643], "page": 1},
 {"key": "total.net_weight", "value": "524.00 KGS", "bbox_2d": [705, 633, 768, 643], "page": 1},
 {"key": "total.gross_weight", "value": "565.92 KGS", "bbox_2d": [793, 633, 856, 643], "page": 1},
 {"key": "total.measurement", "value": "2.070 CBM", "bbox_2d": [875, 633, 935, 643], "page": 1},
 {"key": "signed_by", "value": "Tokyo Seimitsu Kogyo K.K.", "bbox_2d": [564, 690, 726, 700], "page": 1},
 {"key": "signer", "value": "Kenji Sato", "bbox_2d": [564, 740, 622, 751], "page": 1}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[209, 298, 941, 434] 위치의 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 항목명)
- ctn_no: C/TNo
- no: ContainerNo
- description: DescriptionofGoods
- packages: Packages
- quantity: Quantity
- net_weight: NetWeight
- gross_weight: GrossWeight
- measurement: Measurement
```

답:

```json
{
 "columns": [
  "ctn_no",
  "no",
  "description",
  "packages",
  "quantity",
  "net_weight",
  "gross_weight",
  "measurement"
 ],
 "rows": [
  [
   "1-21",
   null,
   "Board-to-Board Connector 0.5mm Pitch 40P",
   "21 CTNS",
   "42,000 PCS",
   "189.00",
   "204.12",
   "0.630"
  ],
  [
   "22-68",
   null,
   "Thick Film Chip Resistor 0603 10K OHM 1%",
   "47 CTNS",
   "4,700,000 PCS",
   "329.00",
   "355.32",
   "1.410"
  ],
  [
   "69",
   null,
   "LED Driver IC, SOP-8",
   "1 CTNS",
   "20,000 PCS",
   "6.00",
   "6.48",
   "0.030"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    237,
    332,
    935,
    355
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    234,
    392,
    935,
    415
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    243,
    424,
    935,
    434
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
[{"columns": ["C/TNo", "DescriptionofGoods", "Packages", "Quantity", "NetWeight", "GrossWeight", "Measurement"], "bbox_2d": [209, 298, 941, 434], "page": 1, "n_rows": 3}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 'C/TNo'·'Quantity' 열이 있는 표를 보고 답하세요. 'GrossWeight' 칸이 '6.48'인 행은 몇 개입니까? (숫자만 답하세요)
```

답:

```json
1
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 'C/TNo'·'Quantity' 열이 있는 표를 보고 답하세요. 위에서 2번째 행의 'Quantity' 값은 무엇입니까? 머리글은 세지 않습니다. (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"4,700,000 PCS"
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa packing_list --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check packing_list` → `python -m docgen.formdir card packing_list` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa packing_list --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions packing_list --show` · `python -m docgen.preview packing_list --out work/packing_list`
