# 주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(영문) (`hf203`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf203 · card-hash: 15538dc9c98b -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 4 (seed 1000000 로 그린 것) · **분류 정답:** 주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(영문)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf203 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.203 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 31칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `DateofReceipt` | DateofReceipt | date | 1쪽 [367, 91, 441, 103] | 늘 | 파일 key | 값 종류 `date` | fields.json:61 | 묻기 |
| `customer.address` | Address | text | 1쪽 [270, 148, 639, 170] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `text`) | fields.json:151 | 묻기 |
| `value` | (Korean) | amount | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:165 | 묻기 |
| `value2` | (English) | amount | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:179 | 묻기 |
| `Headquarter` | Headquarter | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:193 | 묻기 |
| `Mainfactory` | Mainfactory(Mainplaceofbusiness) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:208 | 묻기 |
| `customer.nationality` | Nationality | text | 1쪽 [753, 117, 829, 140] | 늘 | 파일 key | 고객 정보 (키 `customer.nationality`, 없으면 값 종류 `text`) | fields.json:223 | 묻기 |
| `AcquisitionPricewon` | AcquisitionPrice:won(USD) | number | 1쪽 [843, 724, 864, 746] | 늘 | 파일 key | 값 종류 `percent` | fields.json:236 | 묻기 |
| `NotificationNo` | NotificationNo | text | 1쪽 [182, 902, 331, 925] | 늘 | 파일 key | 값 종류 `number` | fields.json:371 | 묻기 |
| `NumberofReceipt` | NumberofReceipt | text | 1쪽 [187, 88, 246, 102] | 늘 | 파일 key | 값 종류 `number` | fields.json:385 | 묻기 |
| `DateofCompletion` | DateofCompletion | date | 1쪽 [577, 90, 637, 99] | 늘 | 파일 key | 값 종류 `date` | fields.json:400 | 묻기 |
| `won` | won | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:415 | 묻기 |
| `Capital` | Capital | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:430 | 묻기 |
| `wonUSD` | won(USD | amount | 1쪽 [823, 652, 892, 666] | 늘 | 파일 key | 값 종류 `fx_amount` | fields.json:445 | 묻기 |
| `DateofReceipt2` | DateofReceipt | date | 2쪽 [365, 87, 438, 103] | 늘 | 파일 key | 값 종류 `date` | fields.json:461 | 묻기 |
| `customer.address2` | Address | text | 2쪽 [266, 144, 635, 173] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `text`) | fields.json:551 | 묻기 |
| `value3` | (Korean) | amount | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:565 | 묻기 |
| `value4` | (English) | amount | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:579 | 묻기 |
| `Headquarter2` | Headquarter | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:593 | 묻기 |
| `Mainfactory2` | Mainfactory(Mainplaceofbusiness) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:608 | 묻기 |
| `customer.nationality2` | Nationality | text | 2쪽 [756, 117, 832, 140] | 늘 | 파일 key | 고객 정보 (키 `customer.nationality`, 없으면 값 종류 `text`) | fields.json:623 | 묻기 |
| `AcquisitionPricewon2` | AcquisitionPrice:won(USD) | number | 2쪽 [844, 724, 862, 746] | 늘 | 파일 key | 값 종류 `percent` | fields.json:636 | 묻기 |
| `NotificationNo2` | NotificationNo | rrn | 2쪽 [177, 904, 327, 926] | 늘 | 파일 key | 값 종류 `number` | fields.json:771 | 묻기 |
| `NumberofReceipt2` | NumberofReceipt | text | 2쪽 [191, 91, 248, 99] | 늘 | 파일 key | 값 종류 `number` | fields.json:785 | 묻기 |
| `DateofCompletion2` | DateofCompletion | date | 2쪽 [577, 90, 640, 102] | 늘 | 파일 key | 값 종류 `date` | fields.json:800 | 묻기 |
| `won2` | won | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:815 | 묻기 |
| `Capital2` | Capital | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:830 | 묻기 |
| `wonUSD2` | won(USD | amount | 2쪽 [828, 650, 895, 664] | 늘 | 파일 key | 값 종류 `fx_amount` | fields.json:845 | 묻기 |
| `Delegated` | Delegated | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:861 | 묻기 |
| `Delegated2` | Delegated | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:876 | 묻기 |
| `Delegated3` | Delegated | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:891 | 묻기 |

## 체크·도장·서명 (marks) — 16칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.Individual` | Individual | checkbox (Foreign company / 보기2) | 1쪽 [266, 122, 391, 135] | 늘 | 파일 key | 보기 중 고름: Foreign company / ? | fields.json:75 | 묻기 |
| `check.ForeignInvestor` | ForeignInvestor | checkbox (보기1) | 1쪽 [504, 134, 518, 145] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:121 | 묻기 |
| `check.보기1` | 보기1 | checkbox (보기1) | 1쪽 [900, 372, 914, 383] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:251 | 묻기 |
| `check.보기12` | 보기1 | checkbox (보기1) | 1쪽 [900, 402, 914, 413] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:281 | 묻기 |
| `check.보기13` | 보기1 | checkbox (보기1) | 1쪽 [900, 433, 914, 443] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:311 | 묻기 |
| `check.보기14` | 보기1 | checkbox (보기1) | 1쪽 [900, 463, 914, 473] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:341 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [786, 24, 857, 68] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [786, 24, 857, 68] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [857, 24, 920, 68] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [857, 24, 920, 68] | 늘 | - | - | - | 묻기 |
| `check.Individual2` | Individual | checkbox (Foreign company / 보기2) | 2쪽 [394, 124, 409, 134] | 늘 | 파일 key | 보기 중 고름: Foreign company / ? | fields.json:475 | 묻기 |
| `check.ForeignInvestor2` | ForeignInvestor | checkbox (보기1) | 2쪽 [504, 134, 518, 145] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:521 | 묻기 |
| `check.보기15` | 보기1 | checkbox (보기1) | 2쪽 [900, 372, 914, 383] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:651 | 묻기 |
| `check.보기16` | 보기1 | checkbox (보기1) | 2쪽 [900, 402, 914, 413] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:681 | 묻기 |
| `check.보기17` | 보기1 | checkbox (보기1) | 2쪽 [900, 433, 914, 443] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:711 | 묻기 |
| `check.보기18` | 보기1 | checkbox (보기1) | 2쪽 [900, 463, 914, 473] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:741 | 묻기 |

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
"주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2024년 6월 6일",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "대한민국",
 "60",
 "280-406662-13211",
 "3158-0255",
 "2024년 9월 12일",
 "CNY 117,500",
 "2025.02.02",
 "10",
 "454497-3849919",
 "517-812881-55526",
 "2024-12-20",
 "AUD 186,100"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"3158-0255"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"454497-3849919"
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
- DateofReceipt: DateofReceipt (같은 설명 중 1번째 칸)
- customer.address: Address (같은 설명 중 1번째 칸)
- value: (Korean) (같은 설명 중 1번째 칸)
- value2: (English) (같은 설명 중 1번째 칸)
- Headquarter: Headquarter (같은 설명 중 1번째 칸)
- Mainfactory: Mainfactory(Mainplaceofbusiness) (같은 설명 중 1번째 칸)
- customer.nationality: Nationality (같은 설명 중 1번째 칸)
- AcquisitionPricewon: AcquisitionPrice:won(USD) (같은 설명 중 1번째 칸)
- NotificationNo: NotificationNo (같은 설명 중 1번째 칸)
- NumberofReceipt: NumberofReceipt (같은 설명 중 1번째 칸)
- DateofCompletion: DateofCompletion (같은 설명 중 1번째 칸)
- won: won (같은 설명 중 1번째 칸)
- Capital: Capital (같은 설명 중 1번째 칸)
- wonUSD: won(USD (같은 설명 중 1번째 칸)
- DateofReceipt2: DateofReceipt (같은 설명 중 2번째 칸)
- customer.address2: Address (같은 설명 중 2번째 칸)
- value3: (Korean) (같은 설명 중 2번째 칸)
- value4: (English) (같은 설명 중 2번째 칸)
- Headquarter2: Headquarter (같은 설명 중 2번째 칸)
- Mainfactory2: Mainfactory(Mainplaceofbusiness) (같은 설명 중 2번째 칸)
- customer.nationality2: Nationality (같은 설명 중 2번째 칸)
- AcquisitionPricewon2: AcquisitionPrice:won(USD) (같은 설명 중 2번째 칸)
- NotificationNo2: NotificationNo (같은 설명 중 2번째 칸)
- NumberofReceipt2: NumberofReceipt (같은 설명 중 2번째 칸)
- DateofCompletion2: DateofCompletion (같은 설명 중 2번째 칸)
- won2: won (같은 설명 중 2번째 칸)
- Capital2: Capital (같은 설명 중 2번째 칸)
- wonUSD2: won(USD (같은 설명 중 2번째 칸)
- Delegated: Delegated (같은 설명 중 1번째 칸)
- Delegated2: Delegated (같은 설명 중 2번째 칸)
- Delegated3: Delegated (같은 설명 중 3번째 칸)
```

답:

```json
[{"key": "DateofReceipt", "value": "2024년 6월 6일", "bbox_2d": [367, 91, 441, 103], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [270, 148, 639, 170], "page": 1},
 {"key": "value", "value": null},
 {"key": "value2", "value": null},
 {"key": "Headquarter", "value": null},
 {"key": "Mainfactory", "value": null},
 {"key": "customer.nationality", "value": "대한민국", "bbox_2d": [753, 117, 829, 140], "page": 1},
 {"key": "AcquisitionPricewon", "value": "60", "bbox_2d": [843, 724, 864, 746], "page": 1},
 {"key": "NotificationNo", "value": "280-406662-13211", "bbox_2d": [182, 902, 331, 925], "page": 1},
 {"key": "NumberofReceipt", "value": "3158-0255", "bbox_2d": [187, 88, 246, 102], "page": 1},
 {"key": "DateofCompletion", "value": "2024년 9월 12일", "bbox_2d": [577, 90, 637, 99], "page": 1},
 {"key": "won", "value": null},
 {"key": "Capital", "value": null},
 {"key": "wonUSD", "value": "CNY 117,500", "bbox_2d": [823, 652, 892, 666], "page": 1},
 {"key": "DateofReceipt2", "value": "2025.02.02", "bbox_2d": [365, 87, 438, 103], "page": 2},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [266, 144, 635, 173], "page": 2},
 {"key": "value3", "value": null},
 {"key": "value4", "value": null},
 {"key": "Headquarter2", "value": null},
 {"key": "Mainfactory2", "value": null},
 {"key": "customer.nationality2", "value": "대한민국", "bbox_2d": [756, 117, 832, 140], "page": 2},
 {"key": "AcquisitionPricewon2", "value": "10", "bbox_2d": [844, 724, 862, 746], "page": 2},
 {"key": "NotificationNo2", "value": "454497-3849919", "bbox_2d": [177, 904, 327, 926], "page": 2},
 {"key": "NumberofReceipt2", "value": "517-812881-55526", "bbox_2d": [191, 91, 248, 99], "page": 2},
 {"key": "DateofCompletion2", "value": "2024-12-20", "bbox_2d": [577, 90, 640, 102], "page": 2},
 {"key": "won2", "value": null},
 {"key": "Capital2", "value": null},
 {"key": "wonUSD2", "value": "AUD 186,100", "bbox_2d": [828, 650, 895, 664], "page": 2},
 {"key": "Delegated", "value": null},
 {"key": "Delegated2", "value": null},
 {"key": "Delegated3", "value": null}]
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
- check.Individual: Individual (같은 설명 중 1번째 칸, 체크박스, 보기: Foreign company / 보기2)
- check.ForeignInvestor: ForeignInvestor (같은 설명 중 1번째 칸, 체크박스, 보기: 보기1)
- check.보기1: 보기1 (같은 설명 중 1번째 칸, 체크박스, 보기: 보기1)
- check.보기12: 보기1 (같은 설명 중 2번째 칸, 체크박스, 보기: 보기1)
- check.보기13: 보기1 (같은 설명 중 3번째 칸, 체크박스, 보기: 보기1)
- check.보기14: 보기1 (같은 설명 중 4번째 칸, 체크박스, 보기: 보기1)
- seal.staff.담당: 담당 (같은 설명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 설명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 설명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 설명 중 2번째 칸, 서명)
- check.Individual2: Individual (같은 설명 중 2번째 칸, 체크박스, 보기: Foreign company / 보기2)
- check.ForeignInvestor2: ForeignInvestor (같은 설명 중 2번째 칸, 체크박스, 보기: 보기1)
- check.보기15: 보기1 (같은 설명 중 5번째 칸, 체크박스, 보기: 보기1)
- check.보기16: 보기1 (같은 설명 중 6번째 칸, 체크박스, 보기: 보기1)
- check.보기17: 보기1 (같은 설명 중 7번째 칸, 체크박스, 보기: 보기1)
- check.보기18: 보기1 (같은 설명 중 8번째 칸, 체크박스, 보기: 보기1)
```

답:

```json
[{"key": "check.Individual", "value": "Foreign company", "bbox_2d": [266, 124, 281, 134], "page": 1},
 {"key": "check.ForeignInvestor", "value": null},
 {"key": "check.보기1", "value": null},
 {"key": "check.보기12", "value": "보기1", "bbox_2d": [900, 402, 914, 413], "page": 1},
 {"key": "check.보기13", "value": null},
 {"key": "check.보기14", "value": "보기1", "bbox_2d": [900, 463, 914, 473], "page": 1},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": false},
 {"key": "sign.staff.책임자", "value": false},
 {"key": "check.Individual2", "value": "보기2", "bbox_2d": [394, 124, 409, 134], "page": 2},
 {"key": "check.ForeignInvestor2", "value": "보기1", "bbox_2d": [504, 134, 518, 145], "page": 2},
 {"key": "check.보기15", "value": "보기1", "bbox_2d": [900, 372, 914, 383], "page": 2},
 {"key": "check.보기16", "value": "보기1", "bbox_2d": [900, 402, 914, 413], "page": 2},
 {"key": "check.보기17", "value": null},
 {"key": "check.보기18", "value": null}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf203 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf203` → `python -m docgen.formdir card hf203` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | studio ① 서식 › 영역 편집에서 그리기 (`fields.json` items 에 한 칸) | 다시 |
| 답의 위치 (박스) | `fields.json` 그 칸의 `rect` [x0, y0, x1, y1] (pt) — 또는 영역 편집 | 다시 |
| 답의 키 | `fields.json` 그 칸에 `"key"` (없으면 키 설명이 그대로 키) | 다시 |
| 답의 값 | `fields.json` 그 칸에 `"source"` ([값 출처 목록](../_common/values.md)) 또는 값 종류 `"kind"` | 다시 |
| 칸의 항목명 | `fields.json` 그 칸의 `label` | 다시 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf203 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf203 --show` · `python -m docgen.preview hf203 --out work/hf203`
