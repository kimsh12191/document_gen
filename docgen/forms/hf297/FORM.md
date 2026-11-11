# 단기수출보험(수출채권유동화) 청약 확인서 (`hf297`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf297 · card-hash: fc81a5894e2f -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 4 (seed 1000000 로 그린 것) · **분류 정답:** 단기수출보험(수출채권유동화) 청약 확인서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf297 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.297 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 36칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `한도신청액` | 한도신청액 | number | 1쪽 [842, 442, 919, 460] | 늘 | 파일 key | 값 종류 `amount` | fields.json:75 | 묻기 |
| `company.name` | 상호 | text | 1쪽 [190, 657, 324, 675] | 늘 | 파일 key | 고객 정보 (키 `company.name`, 없으면 값 종류 `company`) | fields.json:135 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [187, 690, 513, 708] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:148 | 묻기 |
| `company.ceo` | 대표자 | text | 1쪽 [720, 655, 799, 673] | 늘 | 파일 key | 고객 정보 (키 `company.ceo`, 없으면 값 종류 `text`) | fields.json:161 | 묻기 |
| `customer.phone` | 전화번호 | phone | 1쪽 [721, 690, 834, 708] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:174 | 묻기 |
| `company.name2` | 상호 | text | 1쪽 [157, 787, 290, 805] | 늘 | 파일 key | 고객 정보 (키 `company.name`, 없으면 값 종류 `company`) | fields.json:187 | 묻기 |
| `company.ceo2` | 대표자 | text | 1쪽 [659, 787, 739, 805] | 늘 | 파일 key | 고객 정보 (키 `company.ceo`, 없으면 값 종류 `text`) | fields.json:232 | 묻기 |
| `소재국` | 소재국 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:245 | 묻기 |
| `date` | 작성일 | date | 1쪽 [618, 191, 851, 213] | 늘 | 파일 key | 작성일 | fields.json:305 | 묻기 |
| `수출자명` | 수출자명 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:331 | 묻기 |
| `customer.address2` | 주소 | text | 1쪽 [561, 291, 839, 304] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:345 | 묻기 |
| `signer.name` | 대표 | text | 1쪽 [636, 311, 715, 329] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:358 | 묻기 |
| `담당자성명` | 담당자성명 | text | 1쪽 [621, 347, 681, 366] | 늘 | 파일 key | 값 종류 `person` | fields.json:377 | 묻기 |
| `company.name3` | 상호 | text | 2쪽 [258, 170, 392, 191] | 늘 | 파일 key | 고객 정보 (키 `company.name`, 없으면 값 종류 `company`) | fields.json:454 | 묻기 |
| `customer.address3` | 주소 | text | 2쪽 [256, 204, 605, 227] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:468 | 묻기 |
| `company.name4` | 상호 | text | 2쪽 [257, 239, 391, 258] | 늘 | 파일 key | 고객 정보 (키 `company.name`, 없으면 값 종류 `company`) | fields.json:482 | 묻기 |
| `company.ceo3` | 대표자 | text | 2쪽 [713, 173, 793, 190] | 늘 | 파일 key | 고객 정보 (키 `company.ceo`, 없으면 값 종류 `text`) | fields.json:495 | 묻기 |
| `소재국2` | 소재국 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:509 | 묻기 |
| `소재국3` | 소재국 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:524 | 묻기 |
| `결제조건` | 결제조건 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:538 | 묻기 |
| `수출상품명` | 수출상품명 | text | 2쪽 [726, 369, 878, 388] | 늘 | 파일 key | 값 종류 `product` | fields.json:598 | 묻기 |
| `건수` | 건수 | number | 2쪽 [460, 702, 466, 719] | 늘 | 파일 key | 값 종류 `count` | fields.json:612 | 묻기 |
| `CLAIM사유및결과` | CLAIM사유및결과 | text | 2쪽 [265, 768, 345, 788] | 늘 | 파일 key | 값 종류 `reason` | fields.json:626 | 묻기 |
| `신용장방식` | 신용장방식 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:643 | 묻기 |
| `무신용장방식` | 무신용장방식 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:658 | 묻기 |
| `총거래실적` | 총거래실적 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:673 | 묻기 |
| `금액` | 금액 | number | 2쪽 [835, 701, 914, 720] | 늘 | 파일 key | 값 종류 `amount` | fields.json:719 | 묻기 |
| `존재여부` | 존재여부 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:765 | 묻기 |
| `company.name5` | 상호 | text | 3쪽 [307, 172, 441, 192] | 늘 | 파일 key | 고객 정보 (키 `company.name`, 없으면 값 종류 `company`) | fields.json:780 | 묻기 |
| `customer.address4` | 주소 | text | 3쪽 [308, 206, 619, 224] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:793 | 묻기 |
| `계약서상수입자와의관계` | 계약서상수입자와의관계 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:806 | 묻기 |
| `계약서상대금지급책임인` | 계약서상대금지급책임인 | number | 3쪽 [835, 273, 918, 292] | 늘 | 파일 key | 값 종류 `amount` | fields.json:820 | 묻기 |
| `대행수입사유` | 대행수입사유 | text | 3쪽 [307, 307, 393, 326] | 늘 | 파일 key | 값 종류 `reason` | fields.json:834 | 묻기 |
| `company.ceo4` | 대표자 | text | 3쪽 [713, 173, 792, 191] | 늘 | 파일 key | 고객 정보 (키 `company.ceo`, 없으면 값 종류 `text`) | fields.json:894 | 묻기 |
| `소재국4` | 소재국 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:907 | 묻기 |
| `이자보상특약가입여부` | 이자보상특약가입여부 | number | 3쪽 [411, 438, 491, 456] | 늘 | 파일 key | 값 종류 `amount` | fields.json:967 | 묻기 |

## 표 `주소_목록` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `주소_목록.*.대표자` | 대표자 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:200 | 묻기 |

## 표 `최근1년간거래실적_목록` (표 과제 table·table_read·table_find·table_qa) — 2열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `최근1년간거래실적_목록.*.결제금액` | 결제금액 | amount | 2쪽 [646, 633, 756, 652] (1행) | 늘 | 파일 key | 값 종류 `amount` | fields.json:687 | 묻기 |
| `최근1년간거래실적_목록.*.만기경과미결제액` | 만기경과미결제액 | date | 2쪽 [768, 636, 877, 653] (1행) | 늘 | 파일 key | 값 종류 `date` | fields.json:733 | 묻기 |

## 체크·도장·서명 (marks) — 9칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.청약종류` | 청약종류 | checkbox (신규 / 갱신) | 1쪽 [262, 449, 320, 465] | 늘 | 파일 key | 보기 중 고름: 신규 / 갱신 | fields.json:29 | 묻기 |
| `check.일반구분1` | 일반구분1 | checkbox (일반수출 / 위탁가공무역) | 1쪽 [401, 532, 525, 548] | 늘 | 파일 key | 보기 중 고름: 일반수출 / 위탁가공무역 | fields.json:89 | 묻기 |
| `check.수출자와수입자관계의본지사해당하는지여부` | 수출자와수입자관계의본지사해당하는지여부 | checkbox (여 / 부) | 1쪽 [847, 889, 888, 905] | 늘 | 파일 key | 보기 중 고름: 여 / 부 | fields.json:259 | 묻기 |
| `seal.signer` | 대표 | seal | 1쪽 [796, 301, 831, 338] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:358 | 묻기 |
| `sign.signer` | 대표 | signature | 1쪽 [799, 312, 829, 328] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:358 | 묻기 |
| `check.종류` | 종류 | checkbox (L/C / CONFIRMED L/C / 기타 () | 2쪽 [276, 139, 429, 155] | 늘 | 파일 key | 보기 중 고름: L/C / CONFIRMED L/C / 기타 ( | fields.json:392 | 묻기 |
| `check.이면계약또는대응구매계약존재여부` | 이면계약또는대응구매계약존재여부 | checkbox (있음 / 없음) | 2쪽 [640, 445, 702, 461] | 늘 | 파일 key | 보기 중 고름: 있음 / 없음 | fields.json:552 | 묻기 |
| `check.대행수입여부` | 대행수입여부 | checkbox (여 / 부) | 3쪽 [685, 139, 725, 155] | 늘 | 파일 key | 보기 중 고름: 여 / 부 | fields.json:848 | 묻기 |
| `check.이자보상특약가입여부` | 이자보상특약가입여부 | checkbox (가입 / 미가입) | 3쪽 [610, 438, 673, 454] | 늘 | 파일 key | 보기 중 고름: 가입 / 미가입 | fields.json:921 | 묻기 |

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
"단기수출보험(수출채권유동화) 청약 확인서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2,930,000",
 "(주)미래케미칼",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "남궁예태",
 "010-6144-1173",
 "이준정"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2,930,000"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"(주)미래케미칼"
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
- 한도신청액: 한도신청액
- company.name: 상호 (같은 설명 중 1번째 칸)
- customer.address: 주소 (같은 설명 중 1번째 칸)
- 업종3: 업종3
- company.ceo: 대표자 (같은 설명 중 1번째 칸)
- customer.phone: 전화번호
- company.name2: 상호 (같은 설명 중 2번째 칸)
- company.ceo2: 대표자 (같은 설명 중 2번째 칸)
- date: 작성일
- customer.address2: 주소 (같은 설명 중 2번째 칸)
- signer.name: 대표
- 담당자성명: 담당자성명
- 구분: 구분[FATCA비보고대상유형]
```

답:

```json
[{"key": "한도신청액", "value": "2,930,000", "bbox_2d": [842, 442, 919, 460], "page": 1},
 {"key": "company.name", "value": "(주)미래케미칼", "bbox_2d": [190, 657, 324, 675], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [187, 690, 513, 708], "page": 1},
 {"key": "업종3", "value": null},
 {"key": "company.ceo", "value": "남궁예태", "bbox_2d": [720, 655, 799, 673], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [721, 690, 834, 708], "page": 1},
 {"key": "company.name2", "value": "(주)미래케미칼", "bbox_2d": [157, 787, 290, 805], "page": 1},
 {"key": "company.ceo2", "value": "남궁예태", "bbox_2d": [659, 787, 739, 805], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [618, 191, 851, 213], "page": 1},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [561, 291, 839, 304], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [636, 311, 715, 329], "page": 1},
 {"key": "담당자성명", "value": "이준정", "bbox_2d": [621, 347, 681, 366], "page": 1},
 {"key": "구분", "value": null}]
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
- check.청약종류: 청약종류 (체크박스, 보기: 신규 / 갱신)
- check.일반구분1: 일반구분1 (체크박스, 보기: 일반수출 / 위탁가공무역)
- check.수출자와수입자관계의본지사해당하는지여부: 수출자와수입자관계의본지사해당하는지여부 (체크박스, 보기: 여 / 부)
- seal.signer: 대표 (같은 설명 중 1번째 칸, 도장)
- sign.signer: 대표 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.청약종류", "value": "갱신", "bbox_2d": [262, 451, 281, 465], "page": 1},
 {"key": "check.일반구분1", "value": "위탁가공무역", "bbox_2d": [401, 534, 420, 548], "page": 1},
 {"key": "check.수출자와수입자관계의본지사해당하는지여부", "value": "부", "bbox_2d": [847, 892, 865, 905], "page": 1},
 {"key": "seal.signer", "value": true, "bbox_2d": [796, 301, 831, 338], "page": 1},
 {"key": "sign.signer", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf297 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf297` → `python -m docgen.formdir card hf297` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf297 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf297 --show` · `python -m docgen.preview hf297 --out work/hf297`
