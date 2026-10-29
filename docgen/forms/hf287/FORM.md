# 「외국환서식관리프로그램」신용장 양도 조건변경/취소 신청서 (Amendment / Cancellation) (`hf287`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf287 · card-hash: 2f72238fa5f1 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 「외국환서식관리프로그램」신용장 양도 조건변경/취소 신청서 (Amendment / Cancellation)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf287 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.287 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 10칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `date` | Date | date | 1쪽 [685, 183, 823, 196] | 늘 | 규칙: 'Date' → `date` | 고객 정보 (키 `date`) | fields.json:63 | 묻기 |
| `LCNo` | L/CNo. | text | 1쪽 [255, 215, 401, 227] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:74 | 묻기 |
| `LCAmount` | L/CAmount | amount | 1쪽 [776, 233, 856, 245] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:85 | 묻기 |
| `IssuingBank` | IssuingBank | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:96 | 묻기 |
| `TSNo` | T/SNo | text | 1쪽 [255, 268, 338, 280] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:107 | 묻기 |
| `TSAmount` | T/SAmount | number | 1쪽 [781, 286, 858, 298] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:118 | 묻기 |
| `Gentlemen` | Gentlemen | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:129 | 묻기 |
| `Amount` | Amount | number | 1쪽 [835, 453, 912, 465] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:241 | 묻기 |
| `Latestshippingdate` | Latestshippingdate | date | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:275 | 묻기 |
| `Expirydate` | Expirydate | date | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:286 | 묻기 |

## 체크·도장·서명 (marks) — 6칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.Amendment` | Amendment | checkbox (Amendment) | 1쪽 [458, 101, 647, 124] | 늘 | 체크 (항목명) | 보기 중 고름: Amendment | fields.json:17 | 묻기 |
| `check.Cancellation` | Cancellation | checkbox (Cancellation) | 1쪽 [458, 125, 647, 148] | 늘 | 체크 (항목명) | 보기 중 고름: Cancellation | fields.json:40 | 묻기 |
| `check.amend` | amend | checkbox (amend / totally) | 1쪽 [308, 355, 796, 369] | 늘 | 체크 (항목명) | 보기 중 고름: amend / totally | fields.json:140 | 묻기 |
| `check.cancel` | cancel | checkbox (cancel / partially) | 1쪽 [308, 373, 375, 387] | 늘 | 체크 (항목명) | 보기 중 고름: cancel / partially | fields.json:179 | 묻기 |
| `check.increasedby` | increasedby | checkbox (increased by) | 1쪽 [351, 443, 465, 457] | 늘 | 체크 (항목명) | 보기 중 고름: increased by | fields.json:218 | 묻기 |
| `check.decreasedby` | decreasedby | checkbox (decreased by) | 1쪽 [351, 460, 469, 475] | 늘 | 체크 (항목명) | 보기 중 고름: decreased by | fields.json:252 | 묻기 |

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
"「외국환서식관리프로그램」신용장 양도 조건변경/취소 신청서 (Amendment / Cancellation)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2025년 04월 01일",
 "599-281579-10081",
 "530,000원",
 "2538-9453",
 "6,100,000",
 "8,200,000"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"599-281579-10081"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2538-9453"
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
- date: Date
- LCNo: L/CNo.
- LCAmount: L/CAmount
- IssuingBank: IssuingBank
- TSNo: T/SNo
- TSAmount: T/SAmount
- 기업규모: 기업규모
- Gentlemen: Gentlemen
- Amount: Amount
- Latestshippingdate: Latestshippingdate
- Expirydate: Expirydate
```

답:

```json
[{"key": "date", "value": "2025년 04월 01일", "bbox_2d": [685, 183, 823, 196], "page": 1},
 {"key": "LCNo", "value": "599-281579-10081", "bbox_2d": [255, 215, 401, 227], "page": 1},
 {"key": "LCAmount", "value": "530,000원", "bbox_2d": [776, 233, 856, 245], "page": 1},
 {"key": "IssuingBank", "value": null},
 {"key": "TSNo", "value": "2538-9453", "bbox_2d": [255, 268, 338, 280], "page": 1},
 {"key": "TSAmount", "value": "6,100,000", "bbox_2d": [781, 286, 858, 298], "page": 1},
 {"key": "기업규모", "value": null},
 {"key": "Gentlemen", "value": null},
 {"key": "Amount", "value": "8,200,000", "bbox_2d": [835, 453, 912, 465], "page": 1},
 {"key": "Latestshippingdate", "value": null},
 {"key": "Expirydate", "value": null}]
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
- check.Amendment: Amendment (체크박스, 보기: Amendment)
- check.Cancellation: Cancellation (체크박스, 보기: Cancellation)
- check.amend: amend (체크박스, 보기: amend / totally)
- check.cancel: cancel (체크박스, 보기: cancel / partially)
- check.increasedby: increasedby (체크박스, 보기: increased by)
- check.decreasedby: decreasedby (체크박스, 보기: decreased by)
```

답:

```json
[{"key": "check.Amendment", "value": "Amendment", "bbox_2d": [458, 105, 485, 124], "page": 1},
 {"key": "check.Cancellation", "value": "Cancellation", "bbox_2d": [458, 128, 485, 148], "page": 1},
 {"key": "check.amend", "value": null},
 {"key": "check.cancel", "value": "cancel", "bbox_2d": [308, 375, 325, 387], "page": 1},
 {"key": "check.increasedby", "value": null},
 {"key": "check.decreasedby", "value": "decreased by", "bbox_2d": [351, 463, 368, 475], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf287 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf287` → `python -m docgen.formdir card hf287` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf287 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf287 --show` · `python -m docgen.preview hf287 --out work/hf287`
