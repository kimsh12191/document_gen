# 외국환 신고(확인)필증 (`hf252`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf252 · card-hash: b920c54a5d8c -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 외국환 신고(확인)필증
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf252 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.252 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 14칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `반출입구분` | 반출입구분(ExorImport) | text | - | 늘 | 표 행 (묶음·항목명 '반출입구분(Ex or Import)') | 값 종류 `text` (항목명 자동) | fields.json:17 | 묻기 |
| `송금` | 송금(Remitted) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:57 | 묻기 |
| `기타` | 기타(FromOthereligiblesources) | text | 1쪽 [235, 469, 286, 480] | 늘 | 항목명 그대로 | 값 종류 `note` (항목명 자동) | fields.json:68 | 묻기 |
| `국적Nationality` | 국적Nationality | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:339 | 묻기 |
| `확인ResponsibleOfficial` | 확인ResponsibleOfficial | text | - | 늘 | 표 행 (묶음·항목명 '확 인 Responsible Official') | 값 종류 `text` (항목명 자동) | fields.json:375 | 묻기 |
| `통화종류CodeofCurrency` | 통화종류CodeofCurrency | text | 1쪽 [214, 824, 252, 844] | 늘 | 표 행 (묶음·항목명 '통화종류 Code of Currency') | 값 종류 `currency` (항목명 자동) | fields.json:399 | 묻기 |
| `확인기관ConfirmationOffice` | 확인기관ConfirmationOffice | text | - | 늘 | 표 행 (묶음·항목명 '확인기관 Confirmation Office') | 값 종류 `text` (항목명 자동) | fields.json:423 | 묻기 |
| `확인자Signature` | 확인자Signature | text | - | 늘 | 표 행 (묶음·항목명 '확인자 Signature') | 값 종류 `text` (항목명 자동) | fields.json:435 | 묻기 |
| `customer.name` | 성명 | text | 1쪽 [179, 172, 269, 194] | 늘 | 규칙: '성 명' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:459 | 묻기 |
| `customer.name2` | Name | text | 1쪽 [177, 186, 267, 208] | 늘 | 규칙: 'Name' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:471 | 묻기 |
| `Initial` | Initial | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:483 | 묻기 |
| `customer.rrn` | 주민등록번호 | rrn | 1쪽 [241, 236, 401, 258] | 늘 | 규칙: '주민등록번호' → `customer.rrn` | 고객 정보 (키 `customer.rrn`) | fields.json:495 | 묻기 |
| `PassportNo` | PassportNo. | text | 1쪽 [239, 249, 324, 270] | 늘 | 항목명 그대로 | 값 종류 `passport` (항목명 자동) | fields.json:507 | 묻기 |
| `ExpectedTermofStayTo` | ExpectedTermofStayTo | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:519 | 묻기 |

## 표 `휴대_목록` (표 과제 table·table_read·table_find·table_qa) — 6열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `휴대_목록.*.통화종류CodeofCurrency` | 통화종류CodeofCurrency | text | 1쪽 [240, 361, 276, 381] (1행) | 늘 | 표 행 (묶음·항목명 '통화종류 Code of Currency') | 값 종류 `currency` (항목명 자동) | fields.json:29 | 묻기 |
| `휴대_목록.*.형태Form` | 형태Form | text | - (1행) | 늘 | 표 행 (묶음·항목명 '형태 Form') | 값 종류 `text` (항목명 자동) | fields.json:79 | 묻기 |
| `휴대_목록.*.통화별금액AmountineachCurrency` | 통화별금액AmountineachCurrency | amount | 1쪽 [401, 361, 485, 382] (1행) | 늘 | 표 행 (묶음·항목명 '통화별금액 Amount in each Currency') | 값 종류 `amount` (항목명 자동) | fields.json:131 | 묻기 |
| `휴대_목록.*.합계Sum` | 합계(미화상당)Sum(US$equiv) | number | 1쪽 [547, 361, 618, 382] (1행) | 늘 | 표 행 (묶음·항목명 '합계(미화상당) Sum (US$ equiv)') | 값 종류 `amount` (항목명 자동) | fields.json:183 | 묻기 |
| `휴대_목록.*.반출입용도Use` | 반출입용도Use | text | 1쪽 [627, 362, 694, 377] (1행) | 늘 | 표 행 (묶음·항목명 '반출입 용도 Use') | 값 종류 `reason` (항목명 자동) | fields.json:235 | 묻기 |
| `휴대_목록.*.비고` | 비고(Note)(수표번호등) | text | 1쪽 [707, 360, 804, 381] (1행) | 늘 | 표 행 (묶음·항목명 '비 고(Note) (수표번호 등)') | 값 종류 `note` (항목명 자동) | fields.json:287 | 묻기 |

## 표 `목록` (표 과제 table·table_read·table_find·table_qa) — 7열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `목록.*.형태Form` | 형태Form | text | - (1행) | 늘 | 표 행 (묶음·항목명 '형태 Form') | 값 종류 `text` (항목명 자동) | fields.json:107 | 묻기 |
| `목록.*.통화별금액AmountineachCurrency` | 통화별금액AmountineachCurrency | number | 1쪽 [416, 423, 483, 440] (1행) | 늘 | 표 행 (묶음·항목명 '통화별금액 Amount in each Currency') | 값 종류 `amount` (항목명 자동) | fields.json:159 | 묻기 |
| `목록.*.합계Sum` | 합계(미화상당)Sum(US$equiv) | number | 1쪽 [539, 424, 614, 440] (1행) | 늘 | 표 행 (묶음·항목명 '합계(미화상당) Sum (US$ equiv)') | 값 종류 `amount` (항목명 자동) | fields.json:211 | 묻기 |
| `목록.*.반출입용도Use` | 반출입용도Use | text | 1쪽 [628, 426, 695, 439] (1행) | 늘 | 표 행 (묶음·항목명 '반출입 용도 Use') | 값 종류 `reason` (항목명 자동) | fields.json:263 | 묻기 |
| `목록.*.비고` | 비고(Note)(수표번호등) | text | 1쪽 [707, 422, 804, 442] (1행) | 늘 | 표 행 (묶음·항목명 '비 고(Note) (수표번호 등)') | 값 종류 `note` (항목명 자동) | fields.json:315 | 묻기 |
| `목록.*.일자Date` | 일자Date | date | 1쪽 [128, 684, 160, 691] (1행) | 늘 | 표 행 (묶음·항목명 '일자 Date') | 값 종류 `date` (항목명 자동) | fields.json:351 | 묻기 |
| `목록.*.금액Amount` | 금액Amount | number | 1쪽 [204, 682, 253, 692] (1행) | 늘 | 표 행 (묶음·항목명 '금액 Amount') | 값 종류 `amount` (항목명 자동) | fields.json:363 | 묻기 |

## 체크·도장·서명 (marks) — 2칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.customer` ← `seal.signer` | 신고인서명 | seal | 1쪽 [495, 526, 575, 537] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:447 | 묻기 |
| `sign.customer` ← `sign.signer` | 신고인서명 | signature | 1쪽 [495, 526, 575, 537] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:447 | 묻기 |

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
"외국환 신고(확인)필증"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "USD",
 "해당 없음",
 "60,000원",
 "1,310,000",
 "790,000",
 "193,310,000",
 "급여 수령",
 "본인 요청",
 "2024.10.13",
 "87,760,000",
 "AUD",
 "남궁예태",
 "850328-2******",
 "M72862119"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"해당 없음"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"남궁예태"
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
- 반출입구분: 반출입구분(ExorImport)
- 송금: 송금(Remitted)
- 기타: 기타(FromOthereligiblesources)
- 국적Nationality: 국적Nationality
- 확인ResponsibleOfficial: 확인ResponsibleOfficial
- 통화종류CodeofCurrency: 통화종류CodeofCurrency
- 확인기관ConfirmationOffice: 확인기관ConfirmationOffice
- 확인자Signature: 확인자Signature
- customer.name: 성명 (고객 성명)
- customer.name2: Name
- Initial: Initial
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- PassportNo: PassportNo.
- ExpectedTermofStayTo: ExpectedTermofStayTo
```

답:

```json
[{"key": "반출입구분", "value": null},
 {"key": "송금", "value": null},
 {"key": "기타", "value": "해당 없음", "bbox_2d": [235, 469, 286, 480], "page": 1},
 {"key": "국적Nationality", "value": null},
 {"key": "확인ResponsibleOfficial", "value": null},
 {"key": "통화종류CodeofCurrency", "value": "AUD", "bbox_2d": [214, 824, 252, 844], "page": 1},
 {"key": "확인기관ConfirmationOffice", "value": null},
 {"key": "확인자Signature", "value": null},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [179, 172, 269, 194], "page": 1},
 {"key": "customer.name2", "value": "남궁예태", "bbox_2d": [177, 186, 267, 208], "page": 1},
 {"key": "Initial", "value": null},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [241, 236, 401, 258], "page": 1},
 {"key": "PassportNo", "value": "M72862119", "bbox_2d": [239, 249, 324, 270], "page": 1},
 {"key": "ExpectedTermofStayTo", "value": null}]
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
- seal.customer: 신고인서명 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 신고인서명 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": false}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 '통화종류CodeofCurrency'·'합계(미화상당)Sum(US$equiv)' 열이 있는 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 항목명)
- 통화종류CodeofCurrency: 통화종류CodeofCurrency
- 통화별금액AmountineachCurrency: 통화별금액AmountineachCurrency
- 합계Sum: 합계(미화상당)Sum(US$equiv)
- 반출입용도Use: 반출입용도Use
- 비고: 비고(Note)(수표번호등)
- 형태Form: 형태Form
```

답:

```json
{
 "columns": [
  "통화종류CodeofCurrency",
  "통화별금액AmountineachCurrency",
  "합계Sum",
  "반출입용도Use",
  "비고",
  "형태Form"
 ],
 "rows": [
  [
   "USD",
   "60,000원",
   "790,000",
   "급여 수령",
   "해당 없음",
   null
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    240,
    360,
    804,
    382
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
[{"columns": ["통화종류CodeofCurrency", "통화별금액AmountineachCurrency", "합계(미화상당)Sum(US$equiv)", "반출입용도Use", "비고(Note)(수표번호등)", "형태Form"], "bbox_2d": [240, 360, 804, 382], "page": 1, "n_rows": 1},
 {"columns": ["일자Date", "금액Amount", "통화별금액AmountineachCurrency", "합계(미화상당)Sum(US$equiv)", "반출입용도Use", "비고(Note)(수표번호등)", "형태Form"], "bbox_2d": [128, 422, 804, 692], "page": 1, "n_rows": 1}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[240, 360, 804, 382] 위치의 표를 보고 답하세요. '통화별금액AmountineachCurrency' 칸의 값을 모두 더하면 얼마입니까? 빈 칸은 0 으로 봅니다. (쉼표·단위 없이 숫자만 답하세요)
```

답:

```json
60000
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[240, 360, 804, 382] 위치의 표를 보고 답하세요. '통화종류CodeofCurrency' 칸이 'USD'인 행의 '통화별금액AmountineachCurrency' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"60,000원"
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf252 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf252` → `python -m docgen.formdir card hf252` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | studio ① 서식 › 영역 편집에서 그리기 (`fields.json` items 에 한 칸) | 다시 |
| 답의 위치 (박스) | `fields.json` 그 칸의 `rect` [x0, y0, x1, y1] (pt) — 또는 영역 편집 | 다시 |
| 답의 키 | `fields.json` 그 칸에 `"key"` (없으면 규칙이 항목명으로 정함 — 모든 서식 공통 규칙은 studio 키 사전) | 다시 |
| 답의 값 | `fields.json` 그 칸에 `"source"` ([값 출처 목록](../_common/values.md)) 또는 값 종류 `"kind"` | 다시 |
| 칸의 항목명 | `fields.json` 그 칸의 `label` | 다시 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf252 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf252 --show` · `python -m docgen.preview hf252 --out work/hf252`
