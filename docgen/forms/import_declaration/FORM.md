# 수입신고필증 (`import_declaration`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card import_declaration · card-hash: fe37f54fd81e -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** fx · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 수입신고필증
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 수입신고필증 (UNI-PASS 발행 양식). 과세가격·관세·부가세가 계산상 일치한다.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/fx.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 66칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `decl_no` | 신고번호 | text | 1쪽 [48, 66, 161, 76] | 늘 | generate.py | look/template.html.j2:27 | 묻기 |
| `decl_date` | 신고일 | date | 1쪽 [249, 66, 310, 76] | 늘 | generate.py | look/template.html.j2:37 | 묻기 |
| `customs` | 세관.과 | text | 1쪽 [368, 66, 406, 76] | 늘 | generate.py | look/template.html.j2:38 | 묻기 |
| `arrival_date` | 입항일 | date | 1쪽 [459, 66, 520, 76] | 늘 | generate.py | look/template.html.j2:39 | 묻기 |
| `bl_no` | B/L번호 | text | 1쪽 [48, 90, 137, 100] | 늘 | generate.py | look/template.html.j2:43 | 묻기 |
| `cargo_no` | 화물관리번호 | text | 1쪽 [368, 90, 517, 100] | 늘 | generate.py | look/template.html.j2:44 | 묻기 |
| `warehouse_date` | 반입일 | date | 1쪽 [577, 90, 639, 100] | 늘 | generate.py | look/template.html.j2:45 | 묻기 |
| `collection_type` | 징수형태 | number | 1쪽 [662, 90, 675, 100] | 늘 | generate.py | look/template.html.j2:45 | 묻기 |
| `declarant` | 신고인 | text | 1쪽 [48, 114, 172, 125] | 늘 | generate.py | look/template.html.j2:52 | 묻기 |
| `customer.name` ← `importer.name` | 수입자 | text | 1쪽 [48, 135, 138, 146] | 늘 | generate.py | look/template.html.j2:53 | 묻기 |
| `importer.code` | 수입자통관고유부호 | text | 1쪽 [149, 135, 250, 146] | 늘 | generate.py | look/template.html.j2:53 | 묻기 |
| `taxpayer.code` | 납세의무자통관고유부호 | text | 1쪽 [48, 156, 149, 167] | 늘 | generate.py | look/template.html.j2:55 | 묻기 |
| `customer.address` ← `taxpayer.address` | 납세의무자주소 | text | 1쪽 [48, 168, 298, 179] | 늘 | generate.py | look/template.html.j2:56 | 묻기 |
| `taxpayer.name` | 납세의무자상호 | text | 1쪽 [48, 180, 138, 191] | 늘 | generate.py | look/template.html.j2:57 | 묻기 |
| `customer.ceo` ← `taxpayer.ceo` | 납세의무자성명 | text | 1쪽 [148, 180, 202, 191] | 늘 | generate.py | look/template.html.j2:57 | 묻기 |
| `customer.biz_no` ← `taxpayer.biz_no` | 사업자등록번호 | biz_no | 1쪽 [212, 180, 288, 191] | 늘 | generate.py | look/template.html.j2:57 | 묻기 |
| `forwarder` | 운송주선인 | text | 1쪽 [48, 201, 219, 212] | 늘 | generate.py | look/template.html.j2:58 | 묻기 |
| `supplier` | 해외거래처 | text | 1쪽 [48, 223, 267, 233] | 늘 | generate.py | look/template.html.j2:59 | 묻기 |
| `clearance_plan` | 통관계획 | text | 1쪽 [577, 114, 685, 125] | 늘 | generate.py | look/template.html.j2:61 | 묻기 |
| `origin_cert` | 원산지증명서유무 | text | 1쪽 [577, 138, 587, 149] | 늘 | generate.py | look/template.html.j2:63 | 묻기 |
| `total_weight` | 총중량 | text | 1쪽 [577, 162, 620, 172] | 늘 | generate.py | look/template.html.j2:64 | 묻기 |
| `total_packages` | 총포장갯수 | text | 1쪽 [769, 162, 803, 172] | 늘 | generate.py | look/template.html.j2:64 | 묻기 |
| `arrival_port` | 국내도착항 | text | 1쪽 [577, 186, 665, 196] | 늘 | generate.py | look/template.html.j2:65 | 묻기 |
| `transport` | 운송형태 | text | 1쪽 [769, 186, 811, 196] | 늘 | generate.py | look/template.html.j2:65 | 묻기 |
| `export_country` | 적출국 | text | 1쪽 [577, 209, 634, 220] | 늘 | generate.py | look/template.html.j2:66 | 묻기 |
| `vessel` | 선기명 | text | 1쪽 [769, 209, 885, 220] | 늘 | generate.py | look/template.html.j2:66 | 묻기 |
| `master_bl` | MASTERB/L번호 | text | 1쪽 [577, 233, 666, 244] | 늘 | generate.py | look/template.html.j2:67 | 묻기 |
| `carrier_code` | 운수기관부호 | text | 1쪽 [769, 233, 804, 244] | 늘 | generate.py | look/template.html.j2:67 | 묻기 |
| `inspection_place` | 검사(반입)장소 | text | 1쪽 [577, 257, 841, 268] | 늘 | generate.py | look/template.html.j2:68 | 묻기 |
| `items.*.line_no` | 란번호 | number | 1쪽 [62, 284, 83, 295] (1행) | 늘 | generate.py | - | 묻기 |
| `line_total` | 총란수 | amount | 1쪽 [86, 284, 107, 295] | 늘 | generate.py | look/template.html.j2:75 | 묻기 |
| `items.*.std_name` | 품명 | text | 1쪽 [130, 282, 568, 292] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.trade_name` | 거래품명 | text | 1쪽 [687, 282, 937, 304] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.specs.*.no` | 규격번호 | number | 1쪽 [78, 346, 91, 357] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.specs.*.model` | 모델·규격 | text | 1쪽 [130, 346, 182, 357] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.specs.*.quantity` | 수량 | text | 1쪽 [614, 346, 678, 357] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.specs.*.unit_price` | 단가 | amount | 1쪽 [758, 346, 788, 357] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.specs.*.amount` | 금액 | amount | 1쪽 [898, 346, 952, 357] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.hs_code` | 세번부호 | text | 1쪽 [48, 371, 123, 381] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.net_weight` | 순중량 | text | 1쪽 [194, 371, 247, 381] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.taxable_usd` | 과세가격(USD) | amount | 1쪽 [340, 371, 384, 381] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.taxable_krw` | 과세가격(원화) | amount | 1쪽 [394, 371, 467, 381] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.origin` | 원산지 | text | 1쪽 [705, 371, 746, 381] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.duty_type` | 세종 | text | 1쪽 [102, 399, 115, 410] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.duty_rate` | 관세율 | text | 1쪽 [242, 399, 284, 410] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.duty_amount` | 관세액 | amount | 1쪽 [643, 399, 696, 410] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.vat_rate` | 부가세율 | text | 1쪽 [239, 414, 288, 425] (1행) | 늘 | generate.py | - | 묻기 |
| `items.*.vat_amount` | 부가세액 | amount | 1쪽 [642, 414, 696, 425] (1행) | 늘 | generate.py | - | 묻기 |
| `payment` | 결제금액 | text | 1쪽 [48, 744, 180, 754] | 늘 | generate.py | look/template.html.j2:82 | 묻기 |
| `exchange_rate` | 환율 | number | 1쪽 [358, 744, 395, 754] | 늘 | generate.py | look/template.html.j2:117 | 묻기 |
| `total_taxable` | 총과세가격 | amount | 1쪽 [504, 744, 578, 754] | 늘 | generate.py | look/template.html.j2:118 | 묻기 |
| `freight` | 운임 | amount | 1쪽 [48, 767, 67, 778] | 늘 | generate.py | look/template.html.j2:121 | 묻기 |
| `vat_base` | 부가가치세과표 | amount | 1쪽 [705, 767, 779, 778] | 늘 | generate.py | look/template.html.j2:124 | 묻기 |
| `insurance` | 보험료 | amount | 1쪽 [358, 791, 378, 802] | 늘 | generate.py | look/template.html.j2:128 | 묻기 |
| `tax.duty` | 관세 | amount | 2쪽 [296, 66, 349, 76] | 늘 | generate.py | look/template.html.j2:136 | 묻기 |
| `customs_office` | 세관 | text | 2쪽 [399, 66, 458, 77] | 늘 | generate.py | look/template.html.j2:137 | 묻기 |
| `officer` | 담당자 | text | 2쪽 [438, 79, 483, 90] | 늘 | generate.py | look/template.html.j2:138 | 묻기 |
| `receipt_datetime` | 접수일시 | datetime | 2쪽 [453, 92, 557, 103] | 늘 | generate.py | look/template.html.j2:139 | 묻기 |
| `accept_date` | 수리일자 | date | 2쪽 [453, 105, 520, 116] | 늘 | generate.py | look/template.html.j2:140 | 묻기 |
| `tax.vat` | 부가세 | amount | 2쪽 [296, 153, 349, 164] | 늘 | generate.py | look/template.html.j2:149 | 묻기 |
| `tax.total` | 총세액합계 | amount | 2쪽 [296, 197, 349, 208] | 늘 | generate.py | look/template.html.j2:152 | 묻기 |
| `amendment.date` | 정정승인일자 | - | - | 2/16 | generate.py | look/template.html.j2:141 | 묻기 |
| `amendment.reason` | 정정사유 | - | - | 2/16 | generate.py | look/template.html.j2:141 | 묻기 |
| `items.*.reduction.rate` | 감면율 | - | - (1행) | 1/16 | generate.py | - | 묻기 |
| `items.*.reduction.code` | 감면분납부호 | - | - (1행) | 1/16 | generate.py | - | 묻기 |
| `items.*.reduction.amount` | 감면액 | - | - (1행) | 1/16 | generate.py | - | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 2쪽 [899, 121, 955, 161] | 늘 | generate.py | - | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키 `a` ← `b`:** 질문·정답은 공통 키 a, 서식의 원래 키는 b (키 사전이 정함). **정한 곳:** 템플릿에서 그 칸 자리 (html·코드 서식) / 칸 목록의 그 칸 (원본 서식).

## 질문 → 답 (seed 1000000 로 그린 실제 문항)

질문은 모델에게 가는 글 전부, 답은 데이터의 정답 (그린 문서의 값·위치). 질문 문장·답 꼴은 공통 `docgen/forms/_common/questions.json`.

### 서류 분류 `classify` · 채점 acc

질문:

```
이 문서는 고객이 은행에 제출한 서류입니다. 서류의 정식 명칭(서류명)을 답하세요. 설명 없이 서류명만 한 줄로 답하세요.
```

답:

```json
"수입신고필증"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "46648-25-3526310U",
 "2025/03/09",
 "030-15",
 "2025/03/08",
 "HBSC80990647",
 "25HBSC941313I-3585-007",
 "11",
 "미래관세법인 김경도",
 "(주)미래케미칼",
 "미래케미7698303",
 "제주특별자치도 제주시 첨단로 381-19, 2층",
 "남궁예태",
 "702-81-38348",
 "DAON LOGISTICS CO., LTD.",
 "TOKYO SEIMITSU KOGYO K.K. (JP)",
 "D 보세구역장치후",
 "N",
 "566 KG",
 "69 CT",
 "KRPUS 부산항",
 "10 FCL",
 "JP JAPAN",
 "NORTHERN LIGHT",
 "HBSC",
 "03032487-77370349 동부부산컨테이너터미널",
 "001",
 "003",
 "ELECTRICAL CONNECTORS, FOR A VOLTAGE NOT EXCEEDING 1,000V",
 "BOARD-TO-BOARD CONNECTOR 0.5MM PITCH 40P",
 "01",
 "BB-649B",
 "42,000 PCS",
 "38.29",
 "1,608,180",
 "8536.69-9000",
 "189.0 KG",
 "$10,632",
 "₩15,376,452",
 "JP-G-N",
 "관",
 "8.00(A)",
 "1,230,110",
 "10.00(A)",
 "1,660,650",
 "002",
 "FIXED CARBON RESISTORS, CHIP TYPE",
 "THICK FILM CHIP RESISTOR 0603 10K OHM 1%",
 "RC-843",
 "4,700,000 PCS",
 "0.21",
 "987,000",
 "8533.21-0000",
 "329.0 KG",
 "$6,525",
 "₩9,437,101",
 "0.00(C)",
 "0",
 "943,710",
 "ELECTRONIC INTEGRATED CIRCUITS",
 "LED DRIVER IC, SOP-8",
 "LD-392B",
 "20,000 PCS",
 "86.02",
 "1,720,400",
 "8542.39-1000",
 "6.0 KG",
 "$11,373",
 "₩16,449,432",
 "1,644,940",
 "CIF-JPY-4,315,580-DP",
 "9.5614",
 "₩41,262,985",
 "₩0",
 "₩42,493,095",
 "부산세관",
 "권용우",
 "2025/03/09 09:52",
 "4,249,300",
 "5,479,410"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"002"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"8533.21-0000"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- customs: 세관.과
- arrival_date: 입항일
- cargo_no: 화물관리번호
- warehouse_date: 반입일
- customer.name: 수입자 (고객 성명)
- supplier: 해외거래처
- origin_cert: 원산지증명서유무
- total_packages: 총포장갯수
- export_country: 적출국
- vessel: 선기명
- carrier_code: 운수기관부호
- line_total: 총란수
- items.0.std_name: 품명 (1행)
- items.0.trade_name: 거래품명 (1행)
- items.0.specs.0.model: 모델·규격 (1행)
- items.0.specs.0.unit_price: 단가 (1행)
- items.0.net_weight: 순중량 (1행)
- items.0.taxable_usd: 과세가격(USD) (1행)
- items.1.trade_name: 거래품명 (2행)
- items.1.specs.0.quantity: 수량 (2행)
- items.1.specs.0.unit_price: 단가 (2행)
- items.1.specs.0.amount: 금액 (2행)
- items.1.hs_code: 세번부호 (2행)
- items.1.taxable_usd: 과세가격(USD) (2행)
- items.1.origin: 원산지 (2행)
- items.1.duty_amount: 관세액 (2행)
- items.1.vat_amount: 부가세액 (2행)
- items.2.line_no: 란번호 (3행)
- items.2.std_name: 품명 (3행)
- items.2.specs.0.no: 규격번호 (3행)
- items.2.net_weight: 순중량 (3행)
- items.2.taxable_usd: 과세가격(USD) (3행)
- items.2.taxable_krw: 과세가격(원화) (3행)
- items.2.origin: 원산지 (3행)
- items.2.duty_rate: 관세율 (3행)
- exchange_rate: 환율
- freight: 운임
- tax.duty: 관세
- receipt_datetime: 접수일시
- accept_date: 수리일자
```

답:

```json
[{"key": "customs", "value": "030-15", "bbox_2d": [368, 66, 406, 76], "page": 1},
 {"key": "arrival_date", "value": "2025/03/08", "bbox_2d": [459, 66, 520, 76], "page": 1},
 {"key": "cargo_no", "value": "25HBSC941313I-3585-007", "bbox_2d": [368, 90, 517, 100], "page": 1},
 {"key": "warehouse_date", "value": "2025/03/08", "bbox_2d": [577, 90, 639, 100], "page": 1},
 {"key": "customer.name", "value": "(주)미래케미칼", "bbox_2d": [48, 135, 138, 146], "page": 1},
 {"key": "supplier", "value": "TOKYO SEIMITSU KOGYO K.K. (JP)", "bbox_2d": [48, 223, 267, 233], "page": 1},
 {"key": "origin_cert", "value": "N", "bbox_2d": [577, 138, 587, 149], "page": 1},
 {"key": "total_packages", "value": "69 CT", "bbox_2d": [769, 162, 803, 172], "page": 1},
 {"key": "export_country", "value": "JP JAPAN", "bbox_2d": [577, 209, 634, 220], "page": 1},
 {"key": "vessel", "value": "NORTHERN LIGHT", "bbox_2d": [769, 209, 885, 220], "page": 1},
 {"key": "carrier_code", "value": "HBSC", "bbox_2d": [769, 233, 804, 244], "page": 1},
 {"key": "line_total", "value": "003", "bbox_2d": [86, 284, 107, 295], "page": 1},
 {"key": "items.0.std_name", "value": "ELECTRICAL CONNECTORS, FOR A VOLTAGE NOT EXCEEDING 1,000V", "bbox_2d": [130, 282, 568, 292], "page": 1},
 {"key": "items.0.trade_name", "value": "BOARD-TO-BOARD CONNECTOR 0.5MM PITCH 40P", "bbox_2d": [687, 282, 937, 304], "page": 1},
 {"key": "items.0.specs.0.model", "value": "BB-649B", "bbox_2d": [130, 346, 182, 357], "page": 1},
 {"key": "items.0.specs.0.unit_price", "value": "38.29", "bbox_2d": [758, 346, 788, 357], "page": 1},
 {"key": "items.0.net_weight", "value": "189.0 KG", "bbox_2d": [194, 371, 247, 381], "page": 1},
 {"key": "items.0.taxable_usd", "value": "$10,632", "bbox_2d": [340, 371, 384, 381], "page": 1},
 {"key": "items.1.trade_name", "value": "THICK FILM CHIP RESISTOR 0603 10K OHM 1%", "bbox_2d": [687, 440, 921, 462], "page": 1},
 {"key": "items.1.specs.0.quantity", "value": "4,700,000 PCS", "bbox_2d": [597, 504, 678, 515], "page": 1},
 {"key": "items.1.specs.0.unit_price", "value": "0.21", "bbox_2d": [764, 504, 788, 515], "page": 1},
 {"key": "items.1.specs.0.amount", "value": "987,000", "bbox_2d": [908, 504, 952, 515], "page": 1},
 {"key": "items.1.hs_code", "value": "8533.21-0000", "bbox_2d": [48, 529, 123, 539], "page": 1},
 {"key": "items.1.taxable_usd", "value": "$6,525", "bbox_2d": [340, 529, 377, 539], "page": 1},
 {"key": "items.1.origin", "value": "JP-G-N", "bbox_2d": [705, 529, 746, 539], "page": 1},
 {"key": "items.1.duty_amount", "value": "0", "bbox_2d": [689, 557, 696, 568], "page": 1},
 {"key": "items.1.vat_amount", "value": "943,710", "bbox_2d": [652, 572, 696, 583], "page": 1},
 {"key": "items.2.line_no", "value": "003", "bbox_2d": [62, 600, 83, 611], "page": 1},
 {"key": "items.2.std_name", "value": "ELECTRONIC INTEGRATED CIRCUITS", "bbox_2d": [130, 598, 366, 608], "page": 1},
 {"key": "items.2.specs.0.no", "value": "01", "bbox_2d": [78, 650, 91, 661], "page": 1},
 {"key": "items.2.net_weight", "value": "6.0 KG", "bbox_2d": [194, 675, 234, 685], "page": 1},
 {"key": "items.2.taxable_usd", "value": "$11,373", "bbox_2d": [340, 675, 383, 685], "page": 1},
 {"key": "items.2.taxable_krw", "value": "₩16,449,432", "bbox_2d": [393, 675, 467, 685], "page": 1},
 {"key": "items.2.origin", "value": "JP-G-N", "bbox_2d": [705, 675, 746, 685], "page": 1},
 {"key": "items.2.duty_rate", "value": "0.00(C)", "bbox_2d": [242, 704, 284, 714], "page": 1},
 {"key": "exchange_rate", "value": "9.5614", "bbox_2d": [358, 744, 395, 754], "page": 1},
 {"key": "freight", "value": "₩0", "bbox_2d": [48, 767, 67, 778], "page": 1},
 {"key": "tax.duty", "value": "1,230,110", "bbox_2d": [296, 66, 349, 76], "page": 2},
 {"key": "receipt_datetime", "value": "2025/03/09 09:52", "bbox_2d": [453, 92, 557, 103], "page": 2},
 {"key": "accept_date", "value": "2025/03/09", "bbox_2d": [453, 105, 520, 116], "page": 2}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.issuer: 발급기관직인 (도장)
```

답:

```json
[{"key": "seal.issuer", "value": true, "bbox_2d": [899, 121, 955, 161], "page": 2}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `generate.py` 가 돌려주는 dict 에 그 키 값 | 미리보기로 확인 → 재검수 → 카드 다시 만들기 |
| 칸 키·항목명 바꾸기 | `look/template.html.j2` 의 `f("키", label=…)` (질문만 바꾸려면 `questions.json`) | `questions … --check` |
| 값이 이상함·칸끼리 안 맞음 | `generate.py` (값 만드는 함수) | 재검수 |
| 모양·표·문구 | `look/template.html.j2` (studio html 편집) | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions import_declaration --show` · `python -m docgen.preview import_declaration --out work/import_declaration`
