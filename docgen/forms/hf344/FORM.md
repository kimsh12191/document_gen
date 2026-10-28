# 기업관계사 서비스 이용계약서(영문) (`hf344`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf344 · card-hash: 29f29e863fb4 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 4 (seed 1000000 로 그린 것) · **분류 정답:** 기업관계사 서비스 이용계약서(영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.344 (전자금융) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 13칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `Affiliate` | Affiliate | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:38 | 묻기 |
| `Bank` | Bank | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:49 | 묻기 |
| `corp.name` ← `company.name` | CompanyName | text | 4쪽 [409, 622, 541, 645] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.address` | Address | text | 4쪽 [353, 642, 732, 669] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:71 | 묻기 |
| `CEO` | CEO | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:82 | 묻기 |
| `date` | Date | date | 4쪽 [332, 691, 495, 715] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:93 | 묻기 |
| `company.name2` | CompanyName | text | 4쪽 [409, 724, 541, 745] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.address2` | Address | text | 4쪽 [349, 747, 728, 769] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:115 | 묻기 |
| `CEO2` | CEO | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:126 | 묻기 |
| `date2` | Date | date | 4쪽 [332, 791, 495, 816] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:137 | 묻기 |
| `customer.address3` | Address | text | 4쪽 [346, 846, 725, 870] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:148 | 묻기 |
| `GeneralManager` | GeneralManager | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `date3` | Date | date | 4쪽 [327, 895, 489, 917] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:170 | 묻기 |

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
"기업관계사 서비스 이용계약서(영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "(주)미래케미칼",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "2025년 04월 01일"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"서울특별시 서초구 강남대로 357, 103동 1301호"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2025년 04월 01일"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- Affiliate: Affiliate
- Bank: Bank
- corp.name: CompanyName (법인·사업자 상호, 같은 항목명 중 1번째 칸)
- customer.address: Address (고객 주소, 같은 항목명 중 1번째 칸)
- CEO: CEO (같은 항목명 중 1번째 칸)
- date: Date (같은 항목명 중 1번째 칸)
- company.name2: CompanyName (같은 항목명 중 2번째 칸)
- customer.address2: Address (같은 항목명 중 2번째 칸)
- CEO2: CEO (같은 항목명 중 2번째 칸)
- date2: Date (같은 항목명 중 2번째 칸)
- customer.address3: Address (같은 항목명 중 3번째 칸)
- GeneralManager: GeneralManager
- date3: Date (같은 항목명 중 3번째 칸)
```

답:

```json
[{"key": "Affiliate", "value": null},
 {"key": "Bank", "value": null},
 {"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [409, 622, 541, 645], "page": 4},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [353, 642, 732, 669], "page": 4},
 {"key": "CEO", "value": null},
 {"key": "date", "value": "2025년 04월 01일", "bbox_2d": [332, 691, 495, 715], "page": 4},
 {"key": "company.name2", "value": "(주)미래케미칼", "bbox_2d": [409, 724, 541, 745], "page": 4},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [349, 747, 728, 769], "page": 4},
 {"key": "CEO2", "value": null},
 {"key": "date2", "value": "2025년 04월 01일", "bbox_2d": [332, 791, 495, 816], "page": 4},
 {"key": "customer.address3", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [346, 846, 725, 870], "page": 4},
 {"key": "GeneralManager", "value": null},
 {"key": "date3", "value": "2025년 04월 01일", "bbox_2d": [327, 895, 489, 917], "page": 4}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf344 --show` · `python -m docgen.preview hf344 --out work/hf344`
