# 외국환 신고(확인)필증 (`hf252`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf252 · card-hash: ff4563c544b4 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 외국환 신고(확인)필증
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.252 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 27칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `반출입구분` | 반출입구분(ExorImport) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `휴대_목록.*.통화종류CodeofCurrency` | 통화종류CodeofCurrency | text | 1쪽 [240, 361, 276, 381] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `송금` | 송금(Remitted) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `기타` | 기타(FromOthereligiblesources) | text | 1쪽 [235, 469, 286, 480] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `휴대_목록.*.형태Form` | 형태Form | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `목록.*.형태Form` | 형태Form | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `휴대_목록.*.통화별금액AmountineachCurrency` | 통화별금액AmountineachCurrency | amount | 1쪽 [401, 361, 485, 382] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `목록.*.통화별금액AmountineachCurrency` | 통화별금액AmountineachCurrency | number | 1쪽 [416, 423, 483, 440] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `휴대_목록.*.합계Sum` | 합계(미화상당)Sum(US$equiv) | number | 1쪽 [547, 361, 618, 382] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `목록.*.합계Sum` | 합계(미화상당)Sum(US$equiv) | number | 1쪽 [539, 424, 614, 440] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `휴대_목록.*.반출입용도Use` | 반출입용도Use | text | 1쪽 [627, 362, 694, 377] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `목록.*.반출입용도Use` | 반출입용도Use | text | 1쪽 [628, 426, 695, 439] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `휴대_목록.*.비고` | 비고(Note)(수표번호등) | text | 1쪽 [707, 360, 804, 381] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `목록.*.비고` | 비고(Note)(수표번호등) | text | 1쪽 [707, 422, 804, 442] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `국적Nationality` | 국적Nationality | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `목록.*.일자Date` | 일자Date | date | 1쪽 [128, 684, 160, 691] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `목록.*.금액Amount` | 금액Amount | number | 1쪽 [204, 682, 253, 692] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `확인ResponsibleOfficial` | 확인ResponsibleOfficial | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `통화종류CodeofCurrency` | 통화종류CodeofCurrency | text | 1쪽 [214, 824, 252, 844] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `확인기관ConfirmationOffice` | 확인기관ConfirmationOffice | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `확인자Signature` | 확인자Signature | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name` | 성명 | text | 1쪽 [179, 172, 269, 194] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name2` | Name | text | 1쪽 [177, 186, 267, 208] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:474 | 묻기 |
| `Initial` | Initial | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:486 | 묻기 |
| `customer.rrn` | 주민등록번호 | rrn | 1쪽 [241, 236, 401, 258] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:498 | 묻기 |
| `PassportNo` | PassportNo. | text | 1쪽 [239, 249, 324, 270] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `ExpectedTermofStayTo` | ExpectedTermofStayTo | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

## 체크·도장·서명 (marks) — 2칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.customer` ← `seal.signer` | 신고인서명 | seal | 1쪽 [495, 526, 575, 537] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.customer` ← `sign.signer` | 신고인서명 | signature | 1쪽 [495, 526, 575, 537] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

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

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- 반출입구분: 반출입구분(ExorImport)
- 휴대_목록.0.통화종류CodeofCurrency: 통화종류CodeofCurrency (휴대 목록 1행)
- 휴대_목록.1.통화종류CodeofCurrency: 통화종류CodeofCurrency (휴대 목록 2행)
- 송금: 송금(Remitted)
- 기타: 기타(FromOthereligiblesources)
- 휴대_목록.0.형태Form: 형태Form (휴대 목록 1행)
- 휴대_목록.1.형태Form: 형태Form (휴대 목록 2행)
- 목록.0.형태Form: 형태Form (목록 1행)
- 목록.1.형태Form: 형태Form (목록 2행)
- 휴대_목록.0.통화별금액AmountineachCurrency: 통화별금액AmountineachCurrency (휴대 목록 1행)
- 휴대_목록.1.통화별금액AmountineachCurrency: 통화별금액AmountineachCurrency (휴대 목록 2행)
- 목록.0.통화별금액AmountineachCurrency: 통화별금액AmountineachCurrency (목록 1행)
- 목록.1.통화별금액AmountineachCurrency: 통화별금액AmountineachCurrency (목록 2행)
- 휴대_목록.0.합계Sum: 합계(미화상당)Sum(US$equiv) (휴대 목록 1행)
- 휴대_목록.1.합계Sum: 합계(미화상당)Sum(US$equiv) (휴대 목록 2행)
- 목록.0.합계Sum: 합계(미화상당)Sum(US$equiv) (목록 1행)
- 목록.1.합계Sum: 합계(미화상당)Sum(US$equiv) (목록 2행)
- 휴대_목록.0.반출입용도Use: 반출입용도Use (휴대 목록 1행)
- 휴대_목록.1.반출입용도Use: 반출입용도Use (휴대 목록 2행)
- 목록.0.반출입용도Use: 반출입용도Use (목록 1행)
- 목록.1.반출입용도Use: 반출입용도Use (목록 2행)
- 휴대_목록.0.비고: 비고(Note)(수표번호등) (휴대 목록 1행)
- 휴대_목록.1.비고: 비고(Note)(수표번호등) (휴대 목록 2행)
- 목록.0.비고: 비고(Note)(수표번호등) (목록 1행)
- 목록.1.비고: 비고(Note)(수표번호등) (목록 2행)
- 국적Nationality: 국적Nationality
- 목록.0.일자Date: 일자Date (목록 1행)
- 목록.0.금액Amount: 금액Amount (목록 1행)
- 확인ResponsibleOfficial: 확인ResponsibleOfficial
- 목록.1.일자Date: 일자Date (목록 2행)
- 통화종류CodeofCurrency: 통화종류CodeofCurrency (같은 항목명 중 3번째 칸)
- 목록.1.금액Amount: 금액Amount (목록 2행)
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
 {"key": "휴대_목록.0.통화종류CodeofCurrency", "value": "USD", "bbox_2d": [240, 361, 276, 381], "page": 1},
 {"key": "휴대_목록.1.통화종류CodeofCurrency", "value": null},
 {"key": "송금", "value": null},
 {"key": "기타", "value": "해당 없음", "bbox_2d": [235, 469, 286, 480], "page": 1},
 {"key": "휴대_목록.0.형태Form", "value": null},
 {"key": "휴대_목록.1.형태Form", "value": null},
 {"key": "목록.0.형태Form", "value": null},
 {"key": "목록.1.형태Form", "value": null},
 {"key": "휴대_목록.0.통화별금액AmountineachCurrency", "value": "60,000원", "bbox_2d": [401, 361, 485, 382], "page": 1},
 {"key": "휴대_목록.1.통화별금액AmountineachCurrency", "value": null},
 {"key": "목록.0.통화별금액AmountineachCurrency", "value": "1,310,000", "bbox_2d": [416, 423, 483, 440], "page": 1},
 {"key": "목록.1.통화별금액AmountineachCurrency", "value": null},
 {"key": "휴대_목록.0.합계Sum", "value": "790,000", "bbox_2d": [547, 361, 618, 382], "page": 1},
 {"key": "휴대_목록.1.합계Sum", "value": null},
 {"key": "목록.0.합계Sum", "value": "193,310,000", "bbox_2d": [539, 424, 614, 440], "page": 1},
 {"key": "목록.1.합계Sum", "value": null},
 {"key": "휴대_목록.0.반출입용도Use", "value": "급여 수령", "bbox_2d": [627, 362, 694, 377], "page": 1},
 {"key": "휴대_목록.1.반출입용도Use", "value": null},
 {"key": "목록.0.반출입용도Use", "value": "본인 요청", "bbox_2d": [628, 426, 695, 439], "page": 1},
 {"key": "목록.1.반출입용도Use", "value": null},
 {"key": "휴대_목록.0.비고", "value": "해당 없음", "bbox_2d": [707, 360, 804, 381], "page": 1},
 {"key": "휴대_목록.1.비고", "value": null},
 {"key": "목록.0.비고", "value": "해당 없음", "bbox_2d": [707, 422, 804, 442], "page": 1},
 {"key": "목록.1.비고", "value": null},
 {"key": "국적Nationality", "value": null},
 {"key": "목록.0.일자Date", "value": "2024.10.13", "bbox_2d": [128, 684, 160, 691], "page": 1},
 {"key": "목록.0.금액Amount", "value": "87,760,000", "bbox_2d": [204, 682, 253, 692], "page": 1},
 {"key": "확인ResponsibleOfficial", "value": null},
 {"key": "목록.1.일자Date", "value": null},
 {"key": "통화종류CodeofCurrency", "value": "AUD", "bbox_2d": [214, 824, 252, 844], "page": 1},
 {"key": "목록.1.금액Amount", "value": null},
 {"key": "확인기관ConfirmationOffice", "value": null},
 {"key": "확인자Signature", "value": null},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [179, 172, 269, 194], "page": 1},
 {"key": "customer.name2", "value": "남궁예태", "bbox_2d": [177, 186, 267, 208], "page": 1},
 {"key": "Initial", "value": null},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [241, 236, 401, 258], "page": 1},
 {"key": "PassportNo", "value": "M72862119", "bbox_2d": [239, 249, 324, 270], "page": 1},
 {"key": "ExpectedTermofStayTo", "value": null}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

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

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기·위치·항목명 | studio ① 서식 › 영역 편집 (저장하면 `fields.json` items) | 재검수 → 카드 다시 만들기 |
| 값이 이상함 | 영역 편집에서 그 칸의 값 출처·값 종류 | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf252 --show` · `python -m docgen.preview hf252 --out work/hf252`
