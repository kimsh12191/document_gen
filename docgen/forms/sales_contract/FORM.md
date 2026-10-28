# 부동산 매매계약서 (`sales_contract`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card sales_contract · card-hash: e0c978db4c69 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** real_estate · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 부동산 매매계약서
- **쓰이는 업무:** 주택담보대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 부동산(아파트) 매매계약서 (공인중개사 중개).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/real_estate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 36칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `property.location` | 소재지 | text | 1쪽 [141, 102, 669, 115] | 늘 | generate.py | look/template.html.j2:28 | 묻기 |
| `property.land_category` | 지목 | text | 1쪽 [312, 122, 328, 134] | 늘 | generate.py | look/template.html.j2:29 | 묻기 |
| `property.land_right` | 대지권 | text | 1쪽 [542, 122, 761, 134] | 늘 | generate.py | look/template.html.j2:30 | 묻기 |
| `property.land_area` | 면적 | text | 1쪽 [892, 122, 942, 134] | 늘 | generate.py | look/template.html.j2:30 | 묻기 |
| `property.structure` | 구조 | text | 1쪽 [243, 141, 397, 154] | 늘 | generate.py | look/template.html.j2:31 | 묻기 |
| `property.usage` | 용도 | text | 1쪽 [593, 141, 711, 154] | 늘 | generate.py | look/template.html.j2:32 | 묻기 |
| `property.building_area` | 면적 | text | 1쪽 [892, 141, 942, 154] | 늘 | generate.py | look/template.html.j2:32 | 묻기 |
| `payment.price` | 매매대금 | amount | 1쪽 [159, 201, 418, 214] | 늘 | generate.py | look/template.html.j2:38 | 묻기 |
| `payment.down` | 계약금 | amount | 1쪽 [159, 221, 421, 233] | 늘 | generate.py | look/template.html.j2:39 | 묻기 |
| `payment.middle` | 중도금 | amount | 1쪽 [159, 260, 391, 272] | 10/16 | generate.py | look/template.html.j2:42 | 묻기 |
| `payment.middle_date` | 중도금지급일 | date | 1쪽 [414, 260, 529, 272] | 10/16 | generate.py | look/template.html.j2:42 | 묻기 |
| `payment.balance` | 잔금 | amount | 1쪽 [159, 279, 433, 292] | 늘 | generate.py | look/template.html.j2:46 | 묻기 |
| `payment.balance_date` | 잔금지급일 | date | 1쪽 [456, 279, 571, 292] | 늘 | generate.py | look/template.html.j2:46 | 묻기 |
| `specials.*` | 특약사항 | text | 1쪽 [62, 516, 626, 529] (1행) | 늘 | generate.py | - | 묻기 |
| `contract_date` | 계약일 | date | 1쪽 [835, 607, 950, 620] | 늘 | generate.py | look/template.html.j2:62 | 묻기 |
| `counterparty.address` ← `seller.address` | 주소 | text | 1쪽 [229, 628, 743, 640] | 늘 | generate.py | - | 묻기 |
| `seller.rrn` | 주민등록번호 | rrn | 1쪽 [253, 659, 358, 671] | 늘 | generate.py | - | 묻기 |
| `seller.phone` | 전화 | phone | 1쪽 [449, 662, 544, 675] | 늘 | generate.py | - | 묻기 |
| `counterparty.name` ← `seller.name` | 성명 | text | 1쪽 [642, 659, 688, 671] | 늘 | generate.py | - | 묻기 |
| `customer.address` ← `buyer.address` | 주소 | text | 1쪽 [229, 708, 758, 721] | 늘 | generate.py | - | 묻기 |
| `customer.rrn` ← `buyer.rrn` | 주민등록번호 | rrn | 1쪽 [253, 728, 358, 740] | 늘 | generate.py | - | 묻기 |
| `customer.phone` ← `buyer.phone` | 전화 | phone | 1쪽 [465, 728, 559, 740] | 늘 | generate.py | - | 묻기 |
| `customer.name` ← `buyer.name` | 성명 | text | 1쪽 [642, 728, 704, 740] | 늘 | generate.py | look/template.html.j2:21 | 묻기 |
| `brokers.*.office_address` | 사무소소재지 | text | 1쪽 [236, 768, 588, 781] (1행) | 늘 | generate.py | - | 묻기 |
| `brokers.*.office_name` | 사무소명칭 | text | 1쪽 [236, 788, 405, 800] (1행) | 늘 | generate.py | - | 묻기 |
| `brokers.*.representative` | 대표 | text | 1쪽 [236, 807, 282, 820] (1행) | 늘 | generate.py | - | 묻기 |
| `brokers.*.reg_no` | 등록번호 | text | 1쪽 [236, 827, 354, 839] (1행) | 늘 | generate.py | - | 묻기 |
| `brokers.*.phone` | 전화 | phone | 1쪽 [594, 827, 681, 839] (1행) | 늘 | generate.py | look/template.html.j2:70 | 묻기 |
| `brokers.*.assistant` | 소속공인중개사 | text | 1쪽 [236, 846, 282, 859] (1행) | 9/16 | generate.py | - | 묻기 |
| `co_seller.address` | 주소 | - | - | 3/16 | generate.py | - | 묻기 |
| `co_seller.rrn` | 주민등록번호 | - | - | 3/16 | generate.py | - | 묻기 |
| `co_seller.phone` | 전화 | - | - | 3/16 | generate.py | - | 묻기 |
| `co_seller.name` | 성명 | - | - | 3/16 | generate.py | - | 묻기 |
| `seller_agent.address` | 대리인주소 | - | - | 1/16 | generate.py | - | 묻기 |
| `seller_agent.rrn` | 대리인주민등록번호 | - | - | 1/16 | generate.py | - | 묻기 |
| `seller_agent.name` | 대리인성명 | - | - | 1/16 | generate.py | - | 묻기 |

## 체크·도장·서명 (marks) — 8칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.seller` | 매도인 | seal | 1쪽 [892, 645, 949, 685] | 늘 | generate.py | - | 묻기 |
| `sign.seller` | 매도인 | signature | 1쪽 [899, 658, 942, 672] | 늘 | generate.py | - | 묻기 |
| `seal.customer` ← `seal.buyer` | 매수인 | seal | 1쪽 [892, 714, 949, 754] | 늘 | generate.py | - | 묻기 |
| `sign.customer` ← `sign.buyer` | 매수인 | signature | 1쪽 [899, 727, 942, 741] | 늘 | generate.py | - | 묻기 |
| `seal.co_seller` | 공동매도인 | 도장 | - | 3/16 | generate.py | - | 묻기 |
| `sign.co_seller` | 공동매도인 | 서명 | - | 3/16 | generate.py | - | 묻기 |
| `seal.seller_agent` | 매도인대리인 | 도장 | - | 1/16 | generate.py | - | 묻기 |
| `sign.seller_agent` | 매도인대리인 | 서명 | - | 1/16 | generate.py | - | 묻기 |

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
"부동산 매매계약서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "대",
 "소유권대지권 46,962.2분의 46.94",
 "46.94㎡",
 "철근콘크리트벽식구조",
 "공동주택(아파트)",
 "74.95㎡",
 "금 십오억육천만원정 (₩1,560,000,000)",
 "금 일억오천육백만원정 (₩156,000,000)",
 "금 삼억칠천만원정 (₩370,000,000)",
 "2025년 01월 18일",
 "금 십억삼천사백만원정 (₩1,034,000,000)",
 "2025년 03월 02일",
 "1. 현 시설물 상태의 계약이며, 매수인은 등기사항증명서 및 현장을 확인하고 계약함.",
 "2. 매수인은 국민은행 주택담보대출로 잔금 일부를 지급할 예정이며, 매도인은 이에 협조한다.",
 "3. 매도인의 이사 일정상 잔금일은 쌍방 합의로 1주일 범위에서 조정할 수 있다.",
 "2024년 12월 25일",
 "서울특별시 노원구 노원로 459-15, 116동 2102호 (중계동, SK뷰리버뷰아파트)",
 "501031-2509832",
 "010-3389-7730",
 "임채영",
 "850328-2489940",
 "010-6144-1173",
 "남궁예태",
 "서울특별시 서초구 강남대로 155, 1층 107호 (반포동)",
 "힐스테공인중개사사무소",
 "이찬유",
 "20473-2009-00697",
 "02-9965-8484",
 "손옥영"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"소유권대지권 46,962.2분의 46.94"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"금 십오억육천만원정 (₩1,560,000,000)"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- property.location: 소재지 (물건 소재지)
- property.land_category: 지목
- property.land_right: 대지권 (물건 대지권)
- property.land_area: 면적 (같은 항목명 중 1번째 칸)
- property.structure: 구조 (물건 구조)
- property.usage: 용도
- property.building_area: 면적 (같은 항목명 중 2번째 칸)
- payment.price: 매매대금
- payment.down: 계약금
- payment.middle: 중도금
- payment.middle_date: 중도금지급일
- payment.balance: 잔금
- payment.balance_date: 잔금지급일
- specials.0: 특약사항 (1번째)
- specials.1: 특약사항 (2번째)
- specials.2: 특약사항 (3번째)
- contract_date: 계약일
- counterparty.address: 주소 (상대방 주소, 같은 항목명 중 1번째 칸)
- seller.rrn: 주민등록번호 (같은 항목명 중 1번째 칸)
- seller.phone: 전화 (같은 항목명 중 1번째 칸)
- counterparty.name: 성명 (상대방 성명, 같은 항목명 중 1번째 칸)
- customer.address: 주소 (고객 주소, 같은 항목명 중 2번째 칸)
- customer.rrn: 주민등록번호 (고객 주민등록번호, 같은 항목명 중 2번째 칸)
- customer.phone: 전화 (고객 연락처, 같은 항목명 중 2번째 칸)
- customer.name: 성명 (고객 성명, 같은 항목명 중 2번째 칸)
- brokers.0.office_address: 사무소소재지 (1행)
- brokers.0.office_name: 사무소명칭 (1행)
- brokers.0.representative: 대표 (1행)
- brokers.0.reg_no: 등록번호 (1행)
- brokers.0.phone: 전화 (1행)
- brokers.0.assistant: 소속공인중개사 (1행)
```

답:

```json
[{"key": "property.location", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [141, 102, 669, 115], "page": 1},
 {"key": "property.land_category", "value": "대", "bbox_2d": [312, 122, 328, 134], "page": 1},
 {"key": "property.land_right", "value": "소유권대지권 46,962.2분의 46.94", "bbox_2d": [542, 122, 761, 134], "page": 1},
 {"key": "property.land_area", "value": "46.94㎡", "bbox_2d": [892, 122, 942, 134], "page": 1},
 {"key": "property.structure", "value": "철근콘크리트벽식구조", "bbox_2d": [243, 141, 397, 154], "page": 1},
 {"key": "property.usage", "value": "공동주택(아파트)", "bbox_2d": [593, 141, 711, 154], "page": 1},
 {"key": "property.building_area", "value": "74.95㎡", "bbox_2d": [892, 141, 942, 154], "page": 1},
 {"key": "payment.price", "value": "금 십오억육천만원정 (₩1,560,000,000)", "bbox_2d": [159, 201, 418, 214], "page": 1},
 {"key": "payment.down", "value": "금 일억오천육백만원정 (₩156,000,000)", "bbox_2d": [159, 221, 421, 233], "page": 1},
 {"key": "payment.middle", "value": "금 삼억칠천만원정 (₩370,000,000)", "bbox_2d": [159, 260, 391, 272], "page": 1},
 {"key": "payment.middle_date", "value": "2025년 01월 18일", "bbox_2d": [414, 260, 529, 272], "page": 1},
 {"key": "payment.balance", "value": "금 십억삼천사백만원정 (₩1,034,000,000)", "bbox_2d": [159, 279, 433, 292], "page": 1},
 {"key": "payment.balance_date", "value": "2025년 03월 02일", "bbox_2d": [456, 279, 571, 292], "page": 1},
 {"key": "specials.0", "value": "1. 현 시설물 상태의 계약이며, 매수인은 등기사항증명서 및 현장을 확인하고 계약함.", "bbox_2d": [62, 516, 626, 529], "page": 1},
 {"key": "specials.1", "value": "2. 매수인은 국민은행 주택담보대출로 잔금 일부를 지급할 예정이며, 매도인은 이에 협조한다.", "bbox_2d": [62, 532, 687, 545], "page": 1},
 {"key": "specials.2", "value": "3. 매도인의 이사 일정상 잔금일은 쌍방 합의로 1주일 범위에서 조정할 수 있다.", "bbox_2d": [62, 548, 587, 561], "page": 1},
 {"key": "contract_date", "value": "2024년 12월 25일", "bbox_2d": [835, 607, 950, 620], "page": 1},
 {"key": "counterparty.address", "value": "서울특별시 노원구 노원로 459-15, 116동 2102호 (중계동, SK뷰리버뷰아파트)", "bbox_2d": [229, 628, 743, 640], "page": 1},
 {"key": "seller.rrn", "value": "501031-2509832", "bbox_2d": [253, 659, 358, 671], "page": 1},
 {"key": "seller.phone", "value": "010-3389-7730", "bbox_2d": [449, 662, 544, 675], "page": 1},
 {"key": "counterparty.name", "value": "임채영", "bbox_2d": [642, 659, 688, 671], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [229, 708, 758, 721], "page": 1},
 {"key": "customer.rrn", "value": "850328-2489940", "bbox_2d": [253, 728, 358, 740], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [465, 728, 559, 740], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [642, 728, 704, 740], "page": 1},
 {"key": "brokers.0.office_address", "value": "서울특별시 서초구 강남대로 155, 1층 107호 (반포동)", "bbox_2d": [236, 768, 588, 781], "page": 1},
 {"key": "brokers.0.office_name", "value": "힐스테공인중개사사무소", "bbox_2d": [236, 788, 405, 800], "page": 1},
 {"key": "brokers.0.representative", "value": "이찬유", "bbox_2d": [236, 807, 282, 820], "page": 1},
 {"key": "brokers.0.reg_no", "value": "20473-2009-00697", "bbox_2d": [236, 827, 354, 839], "page": 1},
 {"key": "brokers.0.phone", "value": "02-9965-8484", "bbox_2d": [594, 827, 681, 839], "page": 1},
 {"key": "brokers.0.assistant", "value": "손옥영", "bbox_2d": [236, 846, 282, 859], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.seller: 매도인 (같은 항목명 중 1번째 칸, 도장)
- sign.seller: 매도인 (같은 항목명 중 2번째 칸, 서명)
- seal.customer: 매수인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 매수인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.seller", "value": true, "bbox_2d": [892, 645, 949, 685], "page": 1},
 {"key": "sign.seller", "value": false},
 {"key": "seal.customer", "value": true, "bbox_2d": [892, 714, 949, 754], "page": 1},
 {"key": "sign.customer", "value": false}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions sales_contract --show` · `python -m docgen.preview sales_contract --out work/sales_contract`
