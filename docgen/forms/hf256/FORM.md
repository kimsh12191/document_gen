# 외국환업무 등록 신청서 (`hf256`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf256 · card-hash: 699a06638552 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 외국환업무 등록 신청서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.256 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 15칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `corp.name` ← `company.name` | 상호(본점) | text | 1쪽 [265, 200, 412, 223] | 늘 | 규칙: '상 호(본 점)' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:17 | 묻기 |
| `corp.ceo` ← `company.ceo` | 대표자(본점) | text | 1쪽 [270, 246, 357, 267] | 늘 | 규칙: '대 표 자(본 점)' → `company.ceo` | 고객 정보 (키 `company.ceo`) | fields.json:28 | 묻기 |
| `본점소재지주` | 본점소재지주 | text | 1쪽 [271, 285, 705, 313] | 늘 | 항목명 그대로 | 값 종류 `address` (항목명 자동) | fields.json:39 | 묻기 |
| `외국환업무의내용` | 외국환업무의내용 | text | 1쪽 [268, 345, 363, 365] | 늘 | 항목명 그대로 | 값 종류 `note` (항목명 자동) | fields.json:50 | 묻기 |
| `자기자본` | 자기자본 | number | 1쪽 [494, 401, 526, 421] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:61 | 묻기 |
| `영업점수` | 영업점수 | number | 1쪽 [473, 444, 490, 464] | 늘 | 항목명 그대로 | 값 종류 `count` (항목명 자동) | fields.json:73 | 묻기 |
| `외국환업무취급점` | 외국환업무취급점 | number | 1쪽 [476, 490, 492, 509] | 늘 | 항목명 그대로 | 값 종류 `count` (항목명 자동) | fields.json:86 | 묻기 |
| `위험관리전산시스템명` | 위험관리전산시스템명 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:99 | 묻기 |
| `corp.established` ← `company.established` | 설립연월일 | date | 1쪽 [696, 202, 902, 220] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:111 | 묻기 |
| `customer.nationality` | 국적(대표자) | text | 1쪽 [696, 246, 784, 267] | 늘 | 규칙: '국 적(대 표 자)' → `customer.nationality` | 고객 정보 (키 `customer.nationality`) | fields.json:136 | 묻기 |
| `납입자본` | 납입자본 | number | 1쪽 [819, 401, 856, 420] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:147 | 묻기 |
| `처리기간` | 처리기간 | text | - | 늘 | 표 행 (묶음·항목명 '처 리 기 간') | 값 종류 `skip` (항목명 자동) | fields.json:159 | 묻기 |
| `도입시기` | 도입(개발)시기 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:173 | 묻기 |
| `date` | 작성일 | date | 1쪽 [697, 697, 899, 715] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:186 | 묻기 |
| `인력현황` | 인력현황 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:211 | 묻기 |

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
"외국환업무 등록 신청서"
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
 "남궁예태",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "해당 없음",
 "6.31",
 "12",
 "대한민국",
 "0.28"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"6.31"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"0.28"
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
- corp.name: 상호(본점) (법인·사업자 상호)
- corp.ceo: 대표자(본점) (법인·사업자 대표자)
- 본점소재지주: 본점소재지주
- 외국환업무의내용: 외국환업무의내용
- 자기자본: 자기자본
- 영업점수: 영업점수
- 외국환업무취급점: 외국환업무취급점
- 위험관리전산시스템명: 위험관리전산시스템명
- corp.established: 설립연월일 (법인·사업자 설립일)
- customer.nationality: 국적(대표자) (고객 국적)
- 납입자본: 납입자본
- 처리기간: 처리기간
- 도입시기: 도입(개발)시기
- date: 작성일
- 인력현황: 인력현황
```

답:

```json
[{"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [265, 200, 412, 223], "page": 1},
 {"key": "corp.ceo", "value": "남궁예태", "bbox_2d": [270, 246, 357, 267], "page": 1},
 {"key": "본점소재지주", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [271, 285, 705, 313], "page": 1},
 {"key": "외국환업무의내용", "value": "해당 없음", "bbox_2d": [268, 345, 363, 365], "page": 1},
 {"key": "자기자본", "value": "6.31", "bbox_2d": [494, 401, 526, 421], "page": 1},
 {"key": "영업점수", "value": "12", "bbox_2d": [473, 444, 490, 464], "page": 1},
 {"key": "외국환업무취급점", "value": "12", "bbox_2d": [476, 490, 492, 509], "page": 1},
 {"key": "위험관리전산시스템명", "value": null},
 {"key": "corp.established", "value": "2025년 4월 1일", "bbox_2d": [696, 202, 902, 220], "page": 1},
 {"key": "customer.nationality", "value": "대한민국", "bbox_2d": [696, 246, 784, 267], "page": 1},
 {"key": "납입자본", "value": "0.28", "bbox_2d": [819, 401, 856, 420], "page": 1},
 {"key": "처리기간", "value": null},
 {"key": "도입시기", "value": null},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [697, 697, 899, 715], "page": 1},
 {"key": "인력현황", "value": null}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf256` → `python -m docgen.formdir card hf256` (실제 질문→답 확인).

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
| 답 모양 | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf256 --show` · `python -m docgen.preview hf256 --out work/hf256`
