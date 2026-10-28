# 「외국환서식관리프로그램」수출대금채권 양도에 따른 대금지급지시서 및 동의통지서 (`hf291`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf291 · card-hash: 38edac9a30d2 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 「외국환서식관리프로그램」수출대금채권 양도에 따른 대금지급지시서 및 동의통지서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.291 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 12칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `customer.name` | Name | text | 1쪽 [571, 602, 638, 614] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:26 | 묻기 |
| `Title` | Title | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:37 | 묻기 |
| `customer.name2` | Name | text | 1쪽 [572, 880, 640, 892] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:48 | 묻기 |
| `Title2` | Title | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:59 | 묻기 |
| `date` | Date | date | 1쪽 [574, 918, 709, 930] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:70 | 묻기 |
| `signer.name` | [수출상] | text | 2쪽 [284, 564, 351, 576] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:81 | 묻기 |
| `customer.name3` | 이름 | text | 2쪽 [590, 583, 657, 595] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:98 | 묻기 |
| `employer.position` | 직위 | text | 2쪽 [589, 602, 623, 614] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:109 | 묻기 |
| `signer2.name` | [수입상] | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:120 | 묻기 |
| `customer.name4` | 이름 | text | 2쪽 [591, 861, 658, 872] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:137 | 묻기 |
| `employer.position2` | 직위 | text | 2쪽 [593, 880, 627, 892] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:148 | 묻기 |
| `date2` | 일자 | date | 2쪽 [590, 899, 725, 911] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:159 | 묻기 |

## 체크·도장·서명 (marks) — 4칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.customer` ← `seal.signer` | [수출상] | seal | 2쪽 [470, 551, 521, 590] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:81 | 묻기 |
| `sign.customer` ← `sign.signer` | [수출상] | signature | 2쪽 [473, 562, 519, 578] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.signer2` | [수입상] | seal | 2쪽 [473, 840, 519, 856] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:120 | 묻기 |
| `sign.signer2` | [수입상] | signature | 2쪽 [473, 840, 519, 856] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

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
"「외국환서식관리프로그램」수출대금채권 양도에 따른 대금지급지시서 및 동의통지서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "남궁예태",
 "2025년 04월 01일",
 "대리"
]
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
- customer.name: Name (고객 성명, 같은 항목명 중 1번째 칸)
- Title: Title (같은 항목명 중 1번째 칸)
- customer.name2: Name (같은 항목명 중 2번째 칸)
- Title2: Title (같은 항목명 중 2번째 칸)
- date: Date
- signer.name: [수출상] (고객 본인의 성명)
- customer.name3: 이름 (같은 항목명 중 1번째 칸)
- employer.position: 직위 (직장 직위, 같은 항목명 중 1번째 칸)
- signer2.name: [수입상] (은행·직원의 성명)
- customer.name4: 이름 (같은 항목명 중 2번째 칸)
- employer.position2: 직위 (같은 항목명 중 2번째 칸)
- date2: 일자
```

답:

```json
[{"key": "customer.name", "value": "남궁예태", "bbox_2d": [571, 602, 638, 614], "page": 1},
 {"key": "Title", "value": null},
 {"key": "customer.name2", "value": "남궁예태", "bbox_2d": [572, 880, 640, 892], "page": 1},
 {"key": "Title2", "value": null},
 {"key": "date", "value": "2025년 04월 01일", "bbox_2d": [574, 918, 709, 930], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [284, 564, 351, 576], "page": 2},
 {"key": "customer.name3", "value": "남궁예태", "bbox_2d": [590, 583, 657, 595], "page": 2},
 {"key": "employer.position", "value": "대리", "bbox_2d": [589, 602, 623, 614], "page": 2},
 {"key": "signer2.name", "value": null},
 {"key": "customer.name4", "value": "남궁예태", "bbox_2d": [591, 861, 658, 872], "page": 2},
 {"key": "employer.position2", "value": "대리", "bbox_2d": [593, 880, 627, 892], "page": 2},
 {"key": "date2", "value": "2025년 04월 01일", "bbox_2d": [590, 899, 725, 911], "page": 2}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.customer: [수출상] (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: [수출상] (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.signer2: [수입상] (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer2: [수입상] (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.customer", "value": true, "bbox_2d": [470, 551, 521, 590], "page": 2},
 {"key": "sign.customer", "value": false},
 {"key": "seal.signer2", "value": false},
 {"key": "sign.signer2", "value": false}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf291 --show` · `python -m docgen.preview hf291 --out work/hf291`
