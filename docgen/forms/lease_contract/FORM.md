# 주택임대차표준계약서 (`lease_contract`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card lease_contract · card-hash: 22f20be43223 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** real_estate · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 주택임대차표준계약서
- **쓰이는 업무:** 전세자금대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 주택임대차표준계약서 (전세). 임대인 = 기존 소유자(seller), 임차인 = 본인.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/real_estate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 40칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `counterparty.name` ← `landlord_name` | 임대인 | text | 1쪽 [91, 62, 135, 73] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:145 | 묻기 |
| `customer.name` ← `tenant_name` | 임차인 | text | 1쪽 [206, 62, 264, 73] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:225 | 묻기 |
| `property.location` ← `house.location` | 소재지 | text | 1쪽 [224, 97, 723, 108] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:100 | 묻기 |
| `house.land_category` | 지목 | text | 1쪽 [237, 113, 251, 124] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:90 | 묻기 |
| `house.land_area` | 토지면적 | text | 1쪽 [884, 113, 950, 124] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:85 | 묻기 |
| `house.structure_usage` | 구조·용도 | text | 1쪽 [237, 130, 504, 140] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:105 | 묻기 |
| `house.building_area` | 건물면적 | text | 1쪽 [903, 130, 950, 140] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:80 | 묻기 |
| `house.lease_part` | 임차할부분 | text | 1쪽 [423, 146, 513, 157] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:95 | 묻기 |
| `tax_arrears` | 미납국세·지방세 | text | 1쪽 [63, 199, 91, 210] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:200 | 묻기 |
| `prior_fixed_date` | 선순위확정일자현황 | text | 1쪽 [302, 199, 362, 210] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:155 | 묻기 |
| `fixed_date.date` | 확정일자 | date | 1쪽 [855, 199, 916, 212] | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:60 | 묻기 |
| `fixed_date.no` | 확정일자번호 | text | 1쪽 [829, 212, 888, 225] | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:65 | 묻기 |
| `fixed_date.office` | 확정일자부여기관 | text | 1쪽 [778, 221, 941, 239] | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:70 | 묻기 |
| `deposit` | 보증금 | amount | 1쪽 [151, 277, 382, 288] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:45 | 묻기 |
| `down_payment` | 계약금 | amount | 1쪽 [151, 294, 327, 304] | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:50 | 묻기 |
| `balance` | 잔금 | amount | 1쪽 [151, 326, 370, 337] | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:5 | 묻기 |
| `balance_date` | 잔금지급일 | date | 1쪽 [392, 326, 500, 337] | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:10 | 묻기 |
| `management_fee` | 관리비 | text | 1쪽 [446, 372, 850, 383] | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:150 | 묻기 |
| `handover_date` | 인도일 | date | 1쪽 [541, 389, 640, 399] | 늘 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:75 | 묻기 |
| `end_date` | 임대차종료일 | date | 1쪽 [43, 401, 139, 411] | 늘 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:55 | 묻기 |
| `specials.*` | 특약사항 | text | 1쪽 [54, 643, 939, 665] (1행) | 늘 | 템플릿 | generate.py | - | 묻기 |
| `contract_date` | 계약일 | date | 1쪽 [851, 760, 957, 771] | 늘 | 템플릿 | generate.py | look/template.html.j2:77 · fields.json:35 | 묻기 |
| `counterparty.address` ← `landlord.address` | 주소 | text | 1쪽 [222, 777, 707, 788] | 늘 | 템플릿 | generate.py | fields.json:110 | 묻기 |
| `landlord.rrn` | 주민등록번호 | rrn | 1쪽 [253, 793, 352, 804] | 늘 | 템플릿 | generate.py | fields.json:125 | 묻기 |
| `landlord.phone` | 전화 | phone | 1쪽 [465, 793, 554, 804] | 늘 | 템플릿 | generate.py | fields.json:120 | 묻기 |
| `landlord.name` | 성명 | text | 1쪽 [635, 793, 678, 804] | 늘 | 템플릿 | generate.py | fields.json:115 | 묻기 |
| `customer.address` ← `tenant.address` | 주소 | text | 1쪽 [222, 826, 720, 836] | 늘 | 템플릿 | generate.py | fields.json:205 | 묻기 |
| `customer.rrn` ← `tenant.rrn` | 주민등록번호 | rrn | 1쪽 [253, 842, 352, 853] | 늘 | 템플릿 | generate.py | fields.json:220 | 묻기 |
| `customer.phone` ← `tenant.phone` | 전화 | phone | 1쪽 [465, 842, 554, 853] | 늘 | 템플릿 | generate.py | fields.json:215 | 묻기 |
| `tenant.name` | 성명 | text | 1쪽 [635, 842, 693, 853] | 늘 | 템플릿 | generate.py | look/template.html.j2:24 · fields.json:210 | 묻기 |
| `brokers.*.office_address` | 사무소소재지 | text | 1쪽 [222, 877, 504, 887] (1행) | 늘 | 템플릿 | generate.py | fields.json:240 | 묻기 |
| `brokers.*.office_name` | 사무소명칭 | text | 1쪽 [222, 892, 394, 901] (1행) | 늘 | 템플릿 | generate.py | fields.json:245 | 묻기 |
| `brokers.*.representative` | 대표 | text | 1쪽 [222, 906, 259, 915] (1행) | 늘 | 템플릿 | generate.py | fields.json:260 | 묻기 |
| `brokers.*.reg_no` | 등록번호 | text | 1쪽 [222, 921, 316, 931] (1행) | 늘 | 템플릿 | generate.py | fields.json:255 | 묻기 |
| `brokers.*.phone` | 전화 | phone | 1쪽 [602, 921, 672, 931] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:85 · fields.json:250 | 묻기 |
| `brokers.*.assistant` | 소속공인중개사 | - | - (1행) | 4/16 | 템플릿 | generate.py | fields.json:235 | 묻기 |
| `co_landlord.address` | 주소 | - | - | 3/16 | 템플릿 | generate.py | fields.json:15 | 묻기 |
| `co_landlord.rrn` | 주민등록번호 | - | - | 3/16 | 템플릿 | generate.py | fields.json:30 | 묻기 |
| `co_landlord.phone` | 전화 | - | - | 3/16 | 템플릿 | generate.py | fields.json:25 | 묻기 |
| `co_landlord.name` | 성명 | - | - | 3/16 | 템플릿 | generate.py | fields.json:20 | 묻기 |

## 체크·도장·서명 (marks) — 7칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `contract_type` | 계약의종류 | checkbox (신규 계약 / 합의에 의한 재계약 / 「주택임대차보호법」 제6조의3의 계약갱신요구권 행사에 의한 갱신계약) | 1쪽 [151, 165, 211, 176] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:40 | 묻기 |
| `seal.landlord` | 임대인 | seal | 1쪽 [839, 793, 950, 806] | 늘 | 템플릿 | generate.py | fields.json:165 | 묻기 |
| `sign.landlord` | 임대인 | signature | 1쪽 [826, 780, 962, 815] | 늘 | 템플릿 | generate.py | fields.json:185 | 묻기 |
| `seal.customer` ← `seal.tenant` | 임차인 | seal | 1쪽 [866, 828, 923, 868] | 늘 | 템플릿 | generate.py | fields.json:175 | 묻기 |
| `sign.customer` ← `sign.tenant` | 임차인 | signature | 1쪽 [839, 841, 950, 854] | 늘 | 템플릿 | generate.py | fields.json:195 | 묻기 |
| `seal.co_landlord` | 공동임대인 | 도장 | - | 3/16 | 템플릿 | generate.py | fields.json:160 | 묻기 |
| `sign.co_landlord` | 공동임대인 | 서명 | - | 3/16 | 템플릿 | generate.py | fields.json:180 | 묻기 |

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
"주택임대차표준계약서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "임채영",
 "남궁예태",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "대",
 "46,962.2㎡",
 "철근콘크리트벽식구조 / 공동주택(아파트)",
 "74.95㎡",
 "전부 (74.95㎡)",
 "없음",
 "해당 없음",
 "2025.03.28",
 "2025-2813",
 "서초구 반포동행정복지센터",
 "금 십억오백만원정 (₩1,005,000,000)",
 "금 일억원정 (₩100,000,000)",
 "금 구억오백만원정 (₩905,000,000)",
 "2025년 04월 28일",
 "세대별 사용량 및 관리규약에 따른 부과액(공용관리비 면적 비례)",
 "2027년 04월 27일",
 "1. 주택을 인도받은 임차인은 2025년 4월 28일까지 주민등록(전입신고)과 주택임대차계약서상 확정일자를 받기로 하고, 임대인은 2025년 4월 30일(최소한 임차인의 위 약정일자 이틀 후부터 가능)에 저당권 등 담보권을 설정할 수 있다.",
 "2. 임대인이 위 특약에 위반하여 임차주택에 저당권 등 담보권을 설정한 경우에는 임차인은 임대차계약을 해제 또는 해지할 수 있다.",
 "3. 임대차계약 체결 이후 임대인이 사전에 고지하지 않은 선순위 임대차 정보나 미납·체납한 국세·지방세가 확인되는 경우, 임차인은 위약금 없이 임대차계약을 해제할 수 있다.",
 "4. 임차인은 국민은행 전세자금대출을 신청할 예정이며, 임대인은 이에 협조한다. 임차인의 귀책사유 없이 대출이 불가한 경우 본 계약은 무효로 하고 임대인은 계약금을 즉시 반환한다.",
 "5. 벽걸이TV, 못 자국 등 경미한 훼손은 원상복구 대상에서 제외한다.",
 "2025년 03월 24일",
 "서울특별시 노원구 노원로 459-15, 116동 2102호 (중계동, SK뷰리버뷰아파트)",
 "501031-2509832",
 "010-3389-7730",
 "850328-2489940",
 "010-6144-1173",
 "서울특별시 서초구 강남대로 340, 1층 109호 (반포동)",
 "힐스테부동산공인중개사사무소",
 "나성영",
 "22782-2023-01298",
 "02-8991-4989"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"서초구 반포동행정복지센터"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"010-3389-7730"
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
- counterparty.name: 임대인 (상대방 성명)
- customer.name: 임차인 (고객 성명)
- property.location: 소재지 (물건 소재지)
- house.land_category: 지목
- house.land_area: 토지면적
- house.structure_usage: 구조·용도
- house.building_area: 건물면적
- house.lease_part: 임차할부분
- tax_arrears: 미납국세·지방세
- prior_fixed_date: 선순위확정일자현황
- fixed_date.date: 확정일자
- fixed_date.no: 확정일자번호
- fixed_date.office: 확정일자부여기관
- deposit: 보증금
- down_payment: 계약금
- balance: 잔금
- balance_date: 잔금지급일
- management_fee: 관리비
- handover_date: 인도일
- end_date: 임대차종료일
- specials.0: 특약사항 (1번째)
- specials.1: 특약사항 (2번째)
- specials.2: 특약사항 (3번째)
- specials.3: 특약사항 (4번째)
- specials.4: 특약사항 (5번째)
- contract_date: 계약일
- counterparty.address: 주소 (상대방 주소, 같은 항목명 중 1번째 칸)
- landlord.rrn: 주민등록번호 (같은 항목명 중 1번째 칸)
- landlord.phone: 전화 (같은 항목명 중 1번째 칸)
- landlord.name: 성명 (거래 상대(국내)의 성명, 같은 항목명 중 1번째 칸)
- customer.address: 주소 (고객 주소, 같은 항목명 중 2번째 칸)
- customer.rrn: 주민등록번호 (고객 주민등록번호, 같은 항목명 중 2번째 칸)
- customer.phone: 전화 (고객 연락처, 같은 항목명 중 2번째 칸)
- tenant.name: 성명 (고객 본인의 성명, 같은 항목명 중 2번째 칸)
- brokers.0.office_address: 사무소소재지 (1행)
- brokers.0.office_name: 사무소명칭 (1행)
- brokers.0.representative: 대표 (1행)
- brokers.0.reg_no: 등록번호 (1행)
- brokers.0.phone: 전화 (1행)
```

답:

```json
[{"key": "counterparty.name", "value": "임채영", "bbox_2d": [91, 62, 135, 73], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [206, 62, 264, 73], "page": 1},
 {"key": "property.location", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [224, 97, 723, 108], "page": 1},
 {"key": "house.land_category", "value": "대", "bbox_2d": [237, 113, 251, 124], "page": 1},
 {"key": "house.land_area", "value": "46,962.2㎡", "bbox_2d": [884, 113, 950, 124], "page": 1},
 {"key": "house.structure_usage", "value": "철근콘크리트벽식구조 / 공동주택(아파트)", "bbox_2d": [237, 130, 504, 140], "page": 1},
 {"key": "house.building_area", "value": "74.95㎡", "bbox_2d": [903, 130, 950, 140], "page": 1},
 {"key": "house.lease_part", "value": "전부 (74.95㎡)", "bbox_2d": [423, 146, 513, 157], "page": 1},
 {"key": "tax_arrears", "value": "없음", "bbox_2d": [63, 199, 91, 210], "page": 1},
 {"key": "prior_fixed_date", "value": "해당 없음", "bbox_2d": [302, 199, 362, 210], "page": 1},
 {"key": "fixed_date.date", "value": "2025.03.28", "bbox_2d": [855, 199, 916, 212], "page": 1},
 {"key": "fixed_date.no", "value": "2025-2813", "bbox_2d": [829, 212, 888, 225], "page": 1},
 {"key": "fixed_date.office", "value": "서초구 반포동행정복지센터", "bbox_2d": [778, 221, 941, 239], "page": 1},
 {"key": "deposit", "value": "금 십억오백만원정 (₩1,005,000,000)", "bbox_2d": [151, 277, 382, 288], "page": 1},
 {"key": "down_payment", "value": "금 일억원정 (₩100,000,000)", "bbox_2d": [151, 294, 327, 304], "page": 1},
 {"key": "balance", "value": "금 구억오백만원정 (₩905,000,000)", "bbox_2d": [151, 326, 370, 337], "page": 1},
 {"key": "balance_date", "value": "2025년 04월 28일", "bbox_2d": [392, 326, 500, 337], "page": 1},
 {"key": "management_fee", "value": "세대별 사용량 및 관리규약에 따른 부과액(공용관리비 면적 비례)", "bbox_2d": [446, 372, 850, 383], "page": 1},
 {"key": "handover_date", "value": "2025년 04월 28일", "bbox_2d": [541, 389, 640, 399], "page": 1},
 {"key": "end_date", "value": "2027년 04월 27일", "bbox_2d": [43, 401, 139, 411], "page": 1},
 {"key": "specials.0", "value": "1. 주택을 인도받은 임차인은 2025년 4월 28일까지 주민등록(전입신고)과 주택임대차계약서상 확정일자를 받기로 하고, 임대인은 2025년 4월 30일(최소한 임차인의 위 약정일자 이틀 후부터 가능)에 저당권 등 담보권을 설정할 수 있다.", "bbox_2d": [54, 643, 939, 665], "page": 1},
 {"key": "specials.1", "value": "2. 임대인이 위 특약에 위반하여 임차주택에 저당권 등 담보권을 설정한 경우에는 임차인은 임대차계약을 해제 또는 해지할 수 있다.", "bbox_2d": [54, 667, 789, 677], "page": 1},
 {"key": "specials.2", "value": "3. 임대차계약 체결 이후 임대인이 사전에 고지하지 않은 선순위 임대차 정보나 미납·체납한 국세·지방세가 확인되는 경우, 임차인은 위약금 없이 임대차계약을 해제할 수 있다.", "bbox_2d": [54, 679, 942, 701], "page": 1},
 {"key": "specials.3", "value": "4. 임차인은 국민은행 전세자금대출을 신청할 예정이며, 임대인은 이에 협조한다. 임차인의 귀책사유 없이 대출이 불가한 경우 본 계약은 무효로 하고 임대인은 계약금을 즉시 반환한다.", "bbox_2d": [54, 703, 939, 725], "page": 1},
 {"key": "specials.4", "value": "5. 벽걸이TV, 못 자국 등 경미한 훼손은 원상복구 대상에서 제외한다.", "bbox_2d": [54, 728, 435, 737], "page": 1},
 {"key": "contract_date", "value": "2025년 03월 24일", "bbox_2d": [851, 760, 957, 771], "page": 1},
 {"key": "counterparty.address", "value": "서울특별시 노원구 노원로 459-15, 116동 2102호 (중계동, SK뷰리버뷰아파트)", "bbox_2d": [222, 777, 707, 788], "page": 1},
 {"key": "landlord.rrn", "value": "501031-2509832", "bbox_2d": [253, 793, 352, 804], "page": 1},
 {"key": "landlord.phone", "value": "010-3389-7730", "bbox_2d": [465, 793, 554, 804], "page": 1},
 {"key": "landlord.name", "value": "임채영", "bbox_2d": [635, 793, 678, 804], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [222, 826, 720, 836], "page": 1},
 {"key": "customer.rrn", "value": "850328-2489940", "bbox_2d": [253, 842, 352, 853], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [465, 842, 554, 853], "page": 1},
 {"key": "tenant.name", "value": "남궁예태", "bbox_2d": [635, 842, 693, 853], "page": 1},
 {"key": "brokers.0.office_address", "value": "서울특별시 서초구 강남대로 340, 1층 109호 (반포동)", "bbox_2d": [222, 877, 504, 887], "page": 1},
 {"key": "brokers.0.office_name", "value": "힐스테부동산공인중개사사무소", "bbox_2d": [222, 892, 394, 901], "page": 1},
 {"key": "brokers.0.representative", "value": "나성영", "bbox_2d": [222, 906, 259, 915], "page": 1},
 {"key": "brokers.0.reg_no", "value": "22782-2023-01298", "bbox_2d": [222, 921, 316, 931], "page": 1},
 {"key": "brokers.0.phone", "value": "02-8991-4989", "bbox_2d": [602, 921, 672, 931], "page": 1}]
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
- contract_type: 계약의종류 (체크박스, 보기: 신규 계약 / 합의에 의한 재계약 / 「주택임대차보호법」 제6조의3의 계약갱신요구권 행사에 의한 갱신계약)
- seal.landlord: 임대인 (같은 항목명 중 1번째 칸, 도장)
- sign.landlord: 임대인 (같은 항목명 중 2번째 칸, 서명)
- seal.customer: 임차인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 임차인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "contract_type", "value": "신규 계약", "bbox_2d": [139, 165, 147, 176], "page": 1},
 {"key": "seal.landlord", "value": false},
 {"key": "sign.landlord", "value": true, "bbox_2d": [826, 780, 962, 815], "page": 1},
 {"key": "seal.customer", "value": true, "bbox_2d": [866, 828, 923, 868], "page": 1},
 {"key": "sign.customer", "value": false}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check lease_contract` → `python -m docgen.formdir card lease_contract` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions lease_contract --show` · `python -m docgen.preview lease_contract --out work/lease_contract`
