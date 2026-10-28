# 주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(영문) (`hf248`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf248 · card-hash: 2a2fe3476dc7 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.248 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 24칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `ReceiptNumber` | ReceiptNumber | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DateofReceipt` | DateofReceipt | date | 1쪽 [389, 115, 466, 134] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name` | Name | text | 1쪽 [392, 167, 484, 193] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:74 | 묻기 |
| `customer.address` | Address | text | 1쪽 [405, 195, 781, 223] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:85 | 묻기 |
| `customer.name2` | Name | text | 1쪽 [390, 229, 482, 255] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:97 | 묻기 |
| `customer.nationality` | Nationality | text | 1쪽 [414, 261, 499, 286] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:109 | 묻기 |
| `AcquisitionPriceWon` | AcquisitionPrice:Won(USD) | number | 1쪽 [839, 294, 859, 319] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `NotificationNo` | NotificationNo | text | 1쪽 [188, 573, 281, 597] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DateofCompletion` | DateofCompletion | date | 1쪽 [614, 117, 683, 128] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Changein` | Changein | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Information` | Information | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:167 | 묻기 |
| `changed` | changed | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:179 | 묻기 |
| `ReceiptNumber2` | ReceiptNumber | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DateofReceipt2` | DateofReceipt | date | 2쪽 [384, 117, 472, 130] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name3` | Name | text | 2쪽 [388, 167, 481, 192] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:213 | 묻기 |
| `customer.address2` | Address | text | 2쪽 [402, 194, 779, 223] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:224 | 묻기 |
| `customer.name4` | Name | text | 2쪽 [387, 231, 479, 256] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:236 | 묻기 |
| `customer.nationality2` | Nationality | text | 2쪽 [415, 260, 501, 286] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:248 | 묻기 |
| `AcquisitionPriceWon2` | AcquisitionPrice:Won(USD) | number | 2쪽 [837, 295, 860, 320] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `NotificationNo2` | NotificationNo | rrn | 2쪽 [191, 572, 349, 595] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DateofCompletion2` | DateofCompletion | date | 2쪽 [612, 116, 682, 131] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Changein2` | Changein | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Information2` | Information | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:306 | 묻기 |
| `changed2` | changed | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:318 | 묻기 |

## 체크·도장·서명 (marks) — 4칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.staff.담당` | 담당 | seal | 1쪽 [795, 38, 839, 69] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [786, 31, 849, 75] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [858, 34, 912, 72] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [849, 31, 922, 75] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

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
"주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2024.08.11",
 "남궁예태",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "대한민국",
 "10",
 "0125-4106",
 "2024년 10월 19일",
 "2024년 9월 12일",
 "30",
 "947930-2043562",
 "2024.07.06"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2024.08.11"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"30"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- ReceiptNumber: ReceiptNumber (같은 항목명 중 1번째 칸)
- DateofReceipt: DateofReceipt (같은 항목명 중 1번째 칸)
- customer.name: Name (고객 성명, 같은 항목명 중 1번째 칸)
- customer.address: Address (고객 주소, 같은 항목명 중 1번째 칸)
- customer.name2: Name (같은 항목명 중 2번째 칸)
- customer.nationality: Nationality (고객 국적, 같은 항목명 중 1번째 칸)
- AcquisitionPriceWon: AcquisitionPrice:Won(USD) (같은 항목명 중 1번째 칸)
- NotificationNo: NotificationNo (같은 항목명 중 1번째 칸)
- DateofCompletion: DateofCompletion (같은 항목명 중 1번째 칸)
- Changein: Changein (같은 항목명 중 1번째 칸)
- Information: Information (같은 항목명 중 1번째 칸)
- changed: changed (같은 항목명 중 1번째 칸)
- ReceiptNumber2: ReceiptNumber (같은 항목명 중 2번째 칸)
- DateofReceipt2: DateofReceipt (같은 항목명 중 2번째 칸)
- customer.name3: Name (같은 항목명 중 3번째 칸)
- customer.address2: Address (같은 항목명 중 2번째 칸)
- customer.name4: Name (같은 항목명 중 4번째 칸)
- customer.nationality2: Nationality (같은 항목명 중 2번째 칸)
- AcquisitionPriceWon2: AcquisitionPrice:Won(USD) (같은 항목명 중 2번째 칸)
- NotificationNo2: NotificationNo (같은 항목명 중 2번째 칸)
- DateofCompletion2: DateofCompletion (같은 항목명 중 2번째 칸)
- Changein2: Changein (같은 항목명 중 2번째 칸)
- Information2: Information (같은 항목명 중 2번째 칸)
- changed2: changed (같은 항목명 중 2번째 칸)
```

답:

```json
[{"key": "ReceiptNumber", "value": null},
 {"key": "DateofReceipt", "value": "2024.08.11", "bbox_2d": [389, 115, 466, 134], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [392, 167, 484, 193], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [405, 195, 781, 223], "page": 1},
 {"key": "customer.name2", "value": "남궁예태", "bbox_2d": [390, 229, 482, 255], "page": 1},
 {"key": "customer.nationality", "value": "대한민국", "bbox_2d": [414, 261, 499, 286], "page": 1},
 {"key": "AcquisitionPriceWon", "value": "10", "bbox_2d": [839, 294, 859, 319], "page": 1},
 {"key": "NotificationNo", "value": "0125-4106", "bbox_2d": [188, 573, 281, 597], "page": 1},
 {"key": "DateofCompletion", "value": "2024년 10월 19일", "bbox_2d": [614, 117, 683, 128], "page": 1},
 {"key": "Changein", "value": null},
 {"key": "Information", "value": null},
 {"key": "changed", "value": null},
 {"key": "ReceiptNumber2", "value": null},
 {"key": "DateofReceipt2", "value": "2024년 9월 12일", "bbox_2d": [384, 117, 472, 130], "page": 2},
 {"key": "customer.name3", "value": "남궁예태", "bbox_2d": [388, 167, 481, 192], "page": 2},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [402, 194, 779, 223], "page": 2},
 {"key": "customer.name4", "value": "남궁예태", "bbox_2d": [387, 231, 479, 256], "page": 2},
 {"key": "customer.nationality2", "value": "대한민국", "bbox_2d": [415, 260, 501, 286], "page": 2},
 {"key": "AcquisitionPriceWon2", "value": "30", "bbox_2d": [837, 295, 860, 320], "page": 2},
 {"key": "NotificationNo2", "value": "947930-2043562", "bbox_2d": [191, 572, 349, 595], "page": 2},
 {"key": "DateofCompletion2", "value": "2024.07.06", "bbox_2d": [612, 116, 682, 131], "page": 2},
 {"key": "Changein2", "value": null},
 {"key": "Information2", "value": null},
 {"key": "changed2", "value": null}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.staff.담당", "value": true, "bbox_2d": [795, 38, 839, 69], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [858, 34, 912, 72], "page": 1},
 {"key": "sign.staff.책임자", "value": false}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf248 --show` · `python -m docgen.preview hf248 --out work/hf248`
