# 수입신고필증 (`import_declaration`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card import_declaration · card-hash: b19cd2eec06e -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** fx · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 수입신고필증
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa import_declaration --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 수입신고필증 (UNI-PASS 발행 양식). 과세가격·관세·부가세가 계산상 일치한다.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/fx.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 50칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `decl_no` | 신고번호 | text | 1쪽 [48, 66, 161, 76] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:70 | 묻기 |
| `decl_date` | 신고일 | date | 1쪽 [249, 66, 310, 76] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:65 | 묻기 |
| `customs` | 세관.과 | text | 1쪽 [368, 66, 406, 76] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:55 | 묻기 |
| `arrival_date` | 입항일 | date | 1쪽 [459, 66, 520, 76] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:20 | 묻기 |
| `bl_no` | B/L번호 | text | 1쪽 [48, 90, 137, 100] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:30 | 묻기 |
| `cargo_no` | 화물관리번호 | text | 1쪽 [368, 90, 517, 100] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:35 | 묻기 |
| `warehouse_date` | 반입일 | date | 1쪽 [577, 90, 639, 100] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:230 | 묻기 |
| `collection_type` | 징수형태 | number | 1쪽 [662, 90, 675, 100] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:50 | 묻기 |
| `declarant` | 신고인 | text | 1쪽 [48, 114, 172, 125] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:75 | 묻기 |
| `customer.name` ← `importer.name` | 수입자 | text | 1쪽 [48, 135, 138, 146] | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:105 | 묻기 |
| `importer.code` | 수입자통관고유부호 | text | 1쪽 [149, 135, 250, 146] | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:100 | 묻기 |
| `taxpayer.code` | 납세의무자통관고유부호 | text | 1쪽 [48, 156, 149, 167] | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:190 | 묻기 |
| `customer.address` ← `taxpayer.address` | 납세의무자주소 | text | 1쪽 [48, 168, 298, 179] | 늘 | 템플릿 | generate.py | look/template.html.j2:56 · fields.json:175 | 묻기 |
| `taxpayer.name` | 납세의무자상호 | text | 1쪽 [48, 180, 138, 191] | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:195 | 묻기 |
| `customer.ceo` ← `taxpayer.ceo` | 납세의무자성명 | text | 1쪽 [148, 180, 202, 191] | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:185 | 묻기 |
| `customer.biz_no` ← `taxpayer.biz_no` | 사업자등록번호 | biz_no | 1쪽 [212, 180, 288, 191] | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:180 | 묻기 |
| `forwarder` | 운송주선인 | text | 1쪽 [48, 201, 219, 212] | 늘 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:90 | 묻기 |
| `supplier` | 해외거래처 | text | 1쪽 [48, 223, 267, 233] | 늘 | 템플릿 | generate.py | look/template.html.j2:59 · fields.json:155 | 묻기 |
| `clearance_plan` | 통관계획 | text | 1쪽 [577, 114, 685, 125] | 늘 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:45 | 묻기 |
| `origin_cert` | 원산지증명서유무 | text | 1쪽 [577, 138, 587, 149] | 늘 | 템플릿 | generate.py | look/template.html.j2:63 · fields.json:135 | 묻기 |
| `total_weight` | 총중량 | text | 1쪽 [577, 162, 620, 172] | 늘 | 템플릿 | generate.py | look/template.html.j2:64 · fields.json:210 | 묻기 |
| `total_packages` | 총포장갯수 | text | 1쪽 [769, 162, 803, 172] | 늘 | 템플릿 | generate.py | look/template.html.j2:64 · fields.json:200 | 묻기 |
| `arrival_port` | 국내도착항 | text | 1쪽 [577, 186, 665, 196] | 늘 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:25 | 묻기 |
| `transport` | 운송형태 | text | 1쪽 [769, 186, 811, 196] | 늘 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:215 | 묻기 |
| `export_country` | 적출국 | text | 1쪽 [577, 209, 634, 220] | 늘 | 템플릿 | generate.py | look/template.html.j2:66 · fields.json:85 | 묻기 |
| `vessel` | 선기명 | text | 1쪽 [769, 209, 885, 220] | 늘 | 템플릿 | generate.py | look/template.html.j2:66 · fields.json:225 | 묻기 |
| `master_bl` | MASTERB/L번호 | text | 1쪽 [577, 233, 666, 244] | 늘 | 템플릿 | generate.py | look/template.html.j2:67 · fields.json:125 | 묻기 |
| `carrier_code` | 운수기관부호 | text | 1쪽 [769, 233, 804, 244] | 늘 | 템플릿 | generate.py | look/template.html.j2:67 · fields.json:40 | 묻기 |
| `inspection_place` | 검사(반입)장소 | text | 1쪽 [577, 257, 841, 268] | 늘 | 템플릿 | generate.py | look/template.html.j2:68 · fields.json:110 | 묻기 |
| `line_total` | 총란수 | amount | 1쪽 [86, 284, 107, 295] | 늘 | 템플릿 | generate.py | look/template.html.j2:75 · fields.json:120 | 묻기 |
| `items.*.specs.*.no` | 규격번호 | number | 1쪽 [78, 346, 91, 357] (1행) | 늘 | 템플릿 | generate.py | - | 묻기 |
| `items.*.specs.*.model` | 모델·규격 | text | 1쪽 [130, 346, 182, 357] (1행) | 늘 | 템플릿 | generate.py | - | 묻기 |
| `items.*.specs.*.quantity` | 수량 | text | 1쪽 [614, 346, 678, 357] (1행) | 늘 | 템플릿 | generate.py | - | 묻기 |
| `items.*.specs.*.unit_price` | 단가 | amount | 1쪽 [758, 346, 788, 357] (1행) | 늘 | 템플릿 | generate.py | - | 묻기 |
| `items.*.specs.*.amount` | 금액 | amount | 1쪽 [898, 346, 952, 357] (1행) | 늘 | 템플릿 | generate.py | - | 묻기 |
| `payment` | 결제금액 | text | 1쪽 [48, 744, 180, 754] | 늘 | 템플릿 | generate.py | look/template.html.j2:82 · fields.json:140 | 묻기 |
| `exchange_rate` | 환율 | number | 1쪽 [358, 744, 395, 754] | 늘 | 템플릿 | generate.py | look/template.html.j2:117 · fields.json:80 | 묻기 |
| `total_taxable` | 총과세가격 | amount | 1쪽 [504, 744, 578, 754] | 늘 | 템플릿 | generate.py | look/template.html.j2:118 · fields.json:205 | 묻기 |
| `freight` | 운임 | amount | 1쪽 [48, 767, 67, 778] | 늘 | 템플릿 | generate.py | look/template.html.j2:121 · fields.json:95 | 묻기 |
| `vat_base` | 부가가치세과표 | amount | 1쪽 [705, 767, 779, 778] | 늘 | 템플릿 | generate.py | look/template.html.j2:124 · fields.json:220 | 묻기 |
| `insurance` | 보험료 | amount | 1쪽 [358, 791, 378, 802] | 늘 | 템플릿 | generate.py | look/template.html.j2:128 · fields.json:115 | 묻기 |
| `tax.duty` | 관세 | amount | 2쪽 [296, 66, 349, 76] | 늘 | 템플릿 | generate.py | look/template.html.j2:136 · fields.json:160 | 묻기 |
| `customs_office` | 세관 | text | 2쪽 [399, 66, 458, 77] | 늘 | 템플릿 | generate.py | look/template.html.j2:137 · fields.json:60 | 묻기 |
| `officer` | 담당자 | text | 2쪽 [438, 79, 483, 90] | 늘 | 템플릿 | generate.py | look/template.html.j2:138 · fields.json:130 | 묻기 |
| `receipt_datetime` | 접수일시 | datetime | 2쪽 [453, 92, 557, 103] | 늘 | 템플릿 | generate.py | look/template.html.j2:139 · fields.json:145 | 묻기 |
| `accept_date` | 수리일자 | date | 2쪽 [453, 105, 520, 116] | 늘 | 템플릿 | generate.py | look/template.html.j2:140 · fields.json:5 | 묻기 |
| `tax.vat` | 부가세 | amount | 2쪽 [296, 153, 349, 164] | 늘 | 템플릿 | generate.py | look/template.html.j2:149 · fields.json:170 | 묻기 |
| `tax.total` | 총세액합계 | amount | 2쪽 [296, 197, 349, 208] | 늘 | 템플릿 | generate.py | look/template.html.j2:152 · fields.json:165 | 묻기 |
| `amendment.date` | 정정승인일자 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:141 · fields.json:10 | 묻기 |
| `amendment.reason` | 정정사유 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:141 · fields.json:15 | 묻기 |

## 표 `items` (표 과제 table·table_read·table_find·table_qa) — 16열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `items.*.line_no` | 란번호 | number | 1쪽 [62, 284, 83, 295] (1행) | 늘 | 템플릿 | generate.py | fields.json:260 | 묻기 |
| `items.*.std_name` | 품명 | text | 1쪽 [130, 282, 568, 292] (1행) | 늘 | 템플릿 | generate.py | fields.json:315 | 묻기 |
| `items.*.trade_name` | 거래품명 | text | 1쪽 [687, 282, 937, 304] (1행) | 늘 | 템플릿 | generate.py | fields.json:330 | 묻기 |
| `items.*.hs_code` | 세번부호 | text | 1쪽 [48, 371, 123, 381] (1행) | 늘 | 템플릿 | generate.py | fields.json:255 | 묻기 |
| `items.*.net_weight` | 순중량 | text | 1쪽 [194, 371, 247, 381] (1행) | 늘 | 템플릿 | generate.py | fields.json:265 | 묻기 |
| `items.*.taxable_usd` | 과세가격(USD) | amount | 1쪽 [340, 371, 384, 381] (1행) | 늘 | 템플릿 | generate.py | fields.json:325 | 묻기 |
| `items.*.taxable_krw` | 과세가격(원화) | amount | 1쪽 [394, 371, 467, 381] (1행) | 늘 | 템플릿 | generate.py | fields.json:320 | 묻기 |
| `items.*.origin` | 원산지 | text | 1쪽 [705, 371, 746, 381] (1행) | 늘 | 템플릿 | generate.py | fields.json:270 | 묻기 |
| `items.*.duty_type` | 세종 | text | 1쪽 [102, 399, 115, 410] (1행) | 늘 | 템플릿 | generate.py | fields.json:250 | 묻기 |
| `items.*.duty_rate` | 관세율 | text | 1쪽 [242, 399, 284, 410] (1행) | 늘 | 템플릿 | generate.py | fields.json:245 | 묻기 |
| `items.*.duty_amount` | 관세액 | amount | 1쪽 [643, 399, 696, 410] (1행) | 늘 | 템플릿 | generate.py | fields.json:240 | 묻기 |
| `items.*.vat_rate` | 부가세율 | text | 1쪽 [239, 414, 288, 425] (1행) | 늘 | 템플릿 | generate.py | fields.json:340 | 묻기 |
| `items.*.vat_amount` | 부가세액 | amount | 1쪽 [642, 414, 696, 425] (1행) | 늘 | 템플릿 | generate.py | fields.json:335 | 묻기 |
| `items.*.reduction.rate` | 감면율 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:285 | 묻기 |
| `items.*.reduction.code` | 감면분납부호 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:280 | 묻기 |
| `items.*.reduction.amount` | 감면액 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:275 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 2쪽 [899, 121, 955, 161] | 늘 | 템플릿 | generate.py | fields.json:150 | 묻기 |

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
- decl_no: 신고번호
- decl_date: 신고일
- arrival_date: 입항일
- bl_no: B/L번호
- cargo_no: 화물관리번호
- warehouse_date: 반입일
- collection_type: 징수형태
- declarant: 신고인
- customer.name: 수입자 (고객 성명)
- importer.code: 수입자통관고유부호
- taxpayer.code: 납세의무자통관고유부호
- customer.address: 납세의무자주소 (고객 주소)
- taxpayer.name: 납세의무자상호 (고객 본인의 성명)
- customer.ceo: 납세의무자성명 (고객 대표자)
- customer.biz_no: 사업자등록번호 (고객 사업자등록번호)
- forwarder: 운송주선인
- supplier: 해외거래처
- clearance_plan: 통관계획
- origin_cert: 원산지증명서유무
- total_weight: 총중량
- total_packages: 총포장갯수
- arrival_port: 국내도착항
- transport: 운송형태
- export_country: 적출국
- vessel: 선기명
- master_bl: MASTERB/L번호
- carrier_code: 운수기관부호
- inspection_place: 검사(반입)장소
- line_total: 총란수
- payment: 결제금액
- exchange_rate: 환율
- total_taxable: 총과세가격
- freight: 운임
- vat_base: 부가가치세과표
- insurance: 보험료
- tax.duty: 관세
- customs_office: 세관
- officer: 담당자
- receipt_datetime: 접수일시
- tax.total: 총세액합계
```

답:

```json
[{"key": "decl_no", "value": "46648-25-3526310U", "bbox_2d": [48, 66, 161, 76], "page": 1},
 {"key": "decl_date", "value": "2025/03/09", "bbox_2d": [249, 66, 310, 76], "page": 1},
 {"key": "arrival_date", "value": "2025/03/08", "bbox_2d": [459, 66, 520, 76], "page": 1},
 {"key": "bl_no", "value": "HBSC80990647", "bbox_2d": [48, 90, 137, 100], "page": 1},
 {"key": "cargo_no", "value": "25HBSC941313I-3585-007", "bbox_2d": [368, 90, 517, 100], "page": 1},
 {"key": "warehouse_date", "value": "2025/03/08", "bbox_2d": [577, 90, 639, 100], "page": 1},
 {"key": "collection_type", "value": "11", "bbox_2d": [662, 90, 675, 100], "page": 1},
 {"key": "declarant", "value": "미래관세법인 김경도", "bbox_2d": [48, 114, 172, 125], "page": 1},
 {"key": "customer.name", "value": "(주)미래케미칼", "bbox_2d": [48, 135, 138, 146], "page": 1},
 {"key": "importer.code", "value": "미래케미7698303", "bbox_2d": [149, 135, 250, 146], "page": 1},
 {"key": "taxpayer.code", "value": "미래케미7698303", "bbox_2d": [48, 156, 149, 167], "page": 1},
 {"key": "customer.address", "value": "제주특별자치도 제주시 첨단로 381-19, 2층", "bbox_2d": [48, 168, 298, 179], "page": 1},
 {"key": "taxpayer.name", "value": "(주)미래케미칼", "bbox_2d": [48, 180, 138, 191], "page": 1},
 {"key": "customer.ceo", "value": "남궁예태", "bbox_2d": [148, 180, 202, 191], "page": 1},
 {"key": "customer.biz_no", "value": "702-81-38348", "bbox_2d": [212, 180, 288, 191], "page": 1},
 {"key": "forwarder", "value": "DAON LOGISTICS CO., LTD.", "bbox_2d": [48, 201, 219, 212], "page": 1},
 {"key": "supplier", "value": "TOKYO SEIMITSU KOGYO K.K. (JP)", "bbox_2d": [48, 223, 267, 233], "page": 1},
 {"key": "clearance_plan", "value": "D 보세구역장치후", "bbox_2d": [577, 114, 685, 125], "page": 1},
 {"key": "origin_cert", "value": "N", "bbox_2d": [577, 138, 587, 149], "page": 1},
 {"key": "total_weight", "value": "566 KG", "bbox_2d": [577, 162, 620, 172], "page": 1},
 {"key": "total_packages", "value": "69 CT", "bbox_2d": [769, 162, 803, 172], "page": 1},
 {"key": "arrival_port", "value": "KRPUS 부산항", "bbox_2d": [577, 186, 665, 196], "page": 1},
 {"key": "transport", "value": "10 FCL", "bbox_2d": [769, 186, 811, 196], "page": 1},
 {"key": "export_country", "value": "JP JAPAN", "bbox_2d": [577, 209, 634, 220], "page": 1},
 {"key": "vessel", "value": "NORTHERN LIGHT", "bbox_2d": [769, 209, 885, 220], "page": 1},
 {"key": "master_bl", "value": "HBSC80990647", "bbox_2d": [577, 233, 666, 244], "page": 1},
 {"key": "carrier_code", "value": "HBSC", "bbox_2d": [769, 233, 804, 244], "page": 1},
 {"key": "inspection_place", "value": "03032487-77370349 동부부산컨테이너터미널", "bbox_2d": [577, 257, 841, 268], "page": 1},
 {"key": "line_total", "value": "003", "bbox_2d": [86, 284, 107, 295], "page": 1},
 {"key": "payment", "value": "CIF-JPY-4,315,580-DP", "bbox_2d": [48, 744, 180, 754], "page": 1},
 {"key": "exchange_rate", "value": "9.5614", "bbox_2d": [358, 744, 395, 754], "page": 1},
 {"key": "total_taxable", "value": "₩41,262,985", "bbox_2d": [504, 744, 578, 754], "page": 1},
 {"key": "freight", "value": "₩0", "bbox_2d": [48, 767, 67, 778], "page": 1},
 {"key": "vat_base", "value": "₩42,493,095", "bbox_2d": [705, 767, 779, 778], "page": 1},
 {"key": "insurance", "value": "₩0", "bbox_2d": [358, 791, 378, 802], "page": 1},
 {"key": "tax.duty", "value": "1,230,110", "bbox_2d": [296, 66, 349, 76], "page": 2},
 {"key": "customs_office", "value": "부산세관", "bbox_2d": [399, 66, 458, 77], "page": 2},
 {"key": "officer", "value": "권용우", "bbox_2d": [438, 79, 483, 90], "page": 2},
 {"key": "receipt_datetime", "value": "2025/03/09 09:52", "bbox_2d": [453, 92, 557, 103], "page": 2},
 {"key": "tax.total", "value": "5,479,410", "bbox_2d": [296, 197, 349, 208], "page": 2}]
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
- seal.issuer: 발급기관직인 (도장)
```

답:

```json
[{"key": "seal.issuer", "value": true, "bbox_2d": [899, 121, 955, 161], "page": 2}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[45, 272, 952, 729] 위치의 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 항목명)
- hs_code: 세번부호
- line_no: 란번호
- duty_type: 세종
- std_name: 품명
- net_weight: 순중량
- vat_rate: 부가세율
- duty_rate: 관세율
- taxable_usd: 과세가격(USD)
- taxable_krw: 과세가격(원화)
- vat_amount: 부가세액
- trade_name: 거래품명
- charge: Charges
- duty_amount: 관세액
- origin: 원산지
```

답:

```json
{
 "columns": [
  "hs_code",
  "line_no",
  "duty_type",
  "std_name",
  "net_weight",
  "vat_rate",
  "duty_rate",
  "taxable_usd",
  "taxable_krw",
  "vat_amount",
  "trade_name",
  "charge",
  "duty_amount",
  "origin"
 ],
 "rows": [
  [
   "8536.69-9000",
   "001",
   "관",
   "ELECTRICAL CONNECTORS, FOR A VOLTAGE NOT EXCEEDING 1,000V",
   "189.0 KG",
   "10.00(A)",
   "8.00(A)",
   "$10,632",
   "₩15,376,452",
   "1,660,650",
   "BOARD-TO-BOARD CONNECTOR 0.5MM PITCH 40P",
   null,
   "1,230,110",
   "JP-G-N"
  ],
  [
   "8533.21-0000",
   "002",
   "관",
   "FIXED CARBON RESISTORS, CHIP TYPE",
   "329.0 KG",
   "10.00(A)",
   "0.00(C)",
   "$6,525",
   "₩9,437,101",
   "943,710",
   "THICK FILM CHIP RESISTOR 0603 10K OHM 1%",
   null,
   "0",
   "JP-G-N"
  ],
  [
   "8542.39-1000",
   "003",
   "관",
   "ELECTRONIC INTEGRATED CIRCUITS",
   "6.0 KG",
   "10.00(A)",
   "0.00(C)",
   "$11,373",
   "₩16,449,432",
   "1,644,940",
   "LED DRIVER IC, SOP-8",
   null,
   "0",
   "JP-G-N"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    48,
    282,
    937,
    425
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    48,
    440,
    921,
    583
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    48,
    598,
    826,
    729
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
[{"columns": ["세번부호", "란번호", "세종", "품명", "순중량", "부가세율", "관세율", "과세가격(USD)", "과세가격(원화)", "부가세액", "거래품명", "관세액", "원산지"], "bbox_2d": [45, 272, 952, 729], "page": 1, "n_rows": 3}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 표를 보고 답하세요. 마지막 행의 '거래품명' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"LED DRIVER IC, SOP-8"
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 표를 보고 답하세요. '과세가격(USD)' 칸의 값을 모두 더하면 얼마입니까? 빈 칸은 0 으로 봅니다. (쉼표·단위 없이 숫자만 답하세요)
```

답:

```json
28530
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa import_declaration --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check import_declaration` → `python -m docgen.formdir card import_declaration` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa import_declaration --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions import_declaration --show` · `python -m docgen.preview import_declaration --out work/import_declaration`
