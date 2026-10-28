# 「외국환서식관리프로그램」신용장 양도 조건변경/취소 신청서 (Amendment / Cancellation) (`hf287`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf287 · card-hash: 24fe39004008 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 「외국환서식관리프로그램」신용장 양도 조건변경/취소 신청서 (Amendment / Cancellation)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.287 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 10칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `date` | Date | date | 1쪽 [685, 183, 823, 196] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:66 | 묻기 |
| `LCNo` | L/CNo. | text | 1쪽 [255, 215, 401, 227] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `LCAmount` | L/CAmount | amount | 1쪽 [776, 233, 856, 245] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `IssuingBank` | IssuingBank | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `TSNo` | T/SNo | text | 1쪽 [255, 268, 338, 280] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `TSAmount` | T/SAmount | number | 1쪽 [781, 286, 858, 298] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Gentlemen` | Gentlemen | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:132 | 묻기 |
| `Amount` | Amount | number | 1쪽 [835, 453, 912, 465] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:244 | 묻기 |
| `Latestshippingdate` | Latestshippingdate | date | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Expirydate` | Expirydate | date | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

## 체크·도장·서명 (marks) — 6칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `check.Amendment` | Amendment | checkbox (Amendment) | 1쪽 [458, 101, 647, 124] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.Cancellation` | Cancellation | checkbox (Cancellation) | 1쪽 [458, 125, 647, 148] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.amend` | amend | checkbox (amend / totally) | 1쪽 [308, 355, 796, 369] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.cancel` | cancel | checkbox (cancel / partially) | 1쪽 [308, 373, 375, 387] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.increasedby` | increasedby | checkbox (increased by) | 1쪽 [351, 443, 465, 457] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.decreasedby` | decreasedby | checkbox (decreased by) | 1쪽 [351, 460, 469, 475] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

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

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

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
 {"key": "Gentlemen", "value": null},
 {"key": "Amount", "value": "8,200,000", "bbox_2d": [835, 453, 912, 465], "page": 1},
 {"key": "Latestshippingdate", "value": null},
 {"key": "Expirydate", "value": null}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf287 --show` · `python -m docgen.preview hf287 --out work/hf287`
