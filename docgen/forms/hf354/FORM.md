# CMS Plus 이용계약서 (`hf354`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf354 · card-hash: 35a32888e658 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 4 (seed 1000000 로 그린 것) · **분류 정답:** CMS Plus 이용계약서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.354 (전자금융) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 16칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `기타` | 기타 | text | 2쪽 [217, 220, 285, 231] | 늘 | 항목명 그대로 | 값 종류 `note` (항목명 자동) | fields.json:35 | 묻기 |
| `설치장소` | 설치장소 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:46 | 묻기 |
| `Server` | Server | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:57 | 묻기 |
| `PC` | PC | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:69 | 묻기 |
| `모니터` | 모니터 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:81 | 묻기 |
| `목록.*.명세` | 명세 | text | - (1행) | 늘 | 표 행 (묶음·항목명 '명세') | 값 종류 `text` (항목명 자동) | fields.json:93 | 묻기 |
| `HW_목록.*.수량` | 수량 | number | 2쪽 [710, 149, 718, 160] (1행) | 늘 | 표 행 (묶음·항목명 '수량') | 값 종류 `count` (항목명 자동) | fields.json:117 | 묻기 |
| `목록.*.수량` | 수량 | number | 2쪽 [710, 220, 718, 231] (1행) | 늘 | 표 행 (묶음·항목명 '수량') | 값 종류 `count` (항목명 자동) | fields.json:159 | 묻기 |
| `키보드마우스포함` | 키보드,마우스포함 | text | - | 늘 | 표 행 (묶음·항목명 '키보드, 마우스 포함') | 값 종류 `text` (항목명 자동) | fields.json:183 | 묻기 |
| `목록.*.키보드마우스포함` | 키보드,마우스포함 | text | - (1행) | 늘 | 표 행 (묶음·항목명 '키보드, 마우스 포함') | 값 종류 `text` (항목명 자동) | fields.json:197 | 묻기 |
| `customer.name` | ,예금주 | text | 2쪽 [558, 888, 604, 896] | 늘 | 규칙: ', 예금주' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:221 | 묻기 |
| `customer.address` | 주소 | text | 4쪽 [291, 821, 625, 832] | 늘 | 규칙: '주 소' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:233 | 묻기 |
| `customer.address2` | 주소 | text | 4쪽 [289, 892, 623, 904] | 늘 | 규칙: '주 소' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:244 | 묻기 |
| `date` | 작성일 | date | 4쪽 [732, 748, 927, 764] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:255 | 묻기 |
| `corp.ceo` ← `signer.name` | 대표이사 | text | 4쪽 [644, 793, 707, 804] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:280 | 묻기 |
| `employer.name` | 회사명 | text | 4쪽 [287, 794, 417, 805] | 늘 | 규칙: '회사명' → `employer.name` | 고객 정보 (키 `employer.name`) | fields.json:309 | 묻기 |

## 체크·도장·서명 (marks) — 4칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.corp` ← `seal.signer` | 대표이사 | seal | 4쪽 [791, 779, 831, 819] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:280 | 묻기 |
| `sign.customer` ← `sign.signer` | 대표이사 | signature | 4쪽 [798, 792, 824, 806] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:280 | 묻기 |
| `seal.signer2` | 지점장 | seal | 4쪽 [798, 863, 824, 877] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:297 | 묻기 |
| `sign.signer2` | 지점장 | signature | 4쪽 [798, 863, 824, 877] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:297 | 묻기 |

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
"CMS Plus 이용계약서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "해당 없음",
 "6",
 "36",
 "남궁예태",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "주식회사 다온패션"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"6"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"36"
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
- 기타: 기타
- 설치장소: 설치장소
- Server: Server
- PC: PC
- 모니터: 모니터
- 목록.0.명세: 명세 (목록 1행)
- 목록.1.명세: 명세 (목록 2행)
- HW_목록.0.수량: 수량 (HW 목록 1행)
- HW_목록.1.수량: 수량 (HW 목록 2행)
- HW_목록.2.수량: 수량 (HW 목록 3행)
- 목록.0.수량: 수량 (목록 1행)
- 목록.1.수량: 수량 (목록 2행)
- 키보드마우스포함: 키보드,마우스포함 (같은 항목명 중 1번째 칸)
- 목록.0.키보드마우스포함: 키보드,마우스포함 (목록 1행)
- 목록.1.키보드마우스포함: 키보드,마우스포함 (목록 2행)
- customer.name: ,예금주 (고객 성명)
- customer.address: 주소 (고객 주소, 같은 항목명 중 1번째 칸)
- customer.address2: 주소 (같은 항목명 중 2번째 칸)
- date: 작성일
- corp.ceo: 대표이사 (법인·사업자 대표자)
- employer.name: 회사명 (직장 이름)
```

답:

```json
[{"key": "기타", "value": "해당 없음", "bbox_2d": [217, 220, 285, 231], "page": 2},
 {"key": "설치장소", "value": null},
 {"key": "Server", "value": null},
 {"key": "PC", "value": null},
 {"key": "모니터", "value": null},
 {"key": "목록.0.명세", "value": null},
 {"key": "목록.1.명세", "value": null},
 {"key": "HW_목록.0.수량", "value": "6", "bbox_2d": [710, 149, 718, 160], "page": 2},
 {"key": "HW_목록.1.수량", "value": null},
 {"key": "HW_목록.2.수량", "value": null},
 {"key": "목록.0.수량", "value": "6", "bbox_2d": [710, 220, 718, 231], "page": 2},
 {"key": "목록.1.수량", "value": "36", "bbox_2d": [705, 244, 723, 255], "page": 2},
 {"key": "키보드마우스포함", "value": null},
 {"key": "목록.0.키보드마우스포함", "value": null},
 {"key": "목록.1.키보드마우스포함", "value": null},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [558, 888, 604, 896], "page": 2},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [291, 821, 625, 832], "page": 4},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [289, 892, 623, 904], "page": 4},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [732, 748, 927, 764], "page": 4},
 {"key": "corp.ceo", "value": "남궁예태", "bbox_2d": [644, 793, 707, 804], "page": 4},
 {"key": "employer.name", "value": "주식회사 다온패션", "bbox_2d": [287, 794, 417, 805], "page": 4}]
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
- seal.corp: 대표이사 (법인·사업자 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 대표이사 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.signer2: 지점장 (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer2: 지점장 (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.corp", "value": true, "bbox_2d": [791, 779, 831, 819], "page": 4},
 {"key": "sign.customer", "value": false},
 {"key": "seal.signer2", "value": false},
 {"key": "sign.signer2", "value": false}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf354` → `python -m docgen.formdir card hf354` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf354 --show` · `python -m docgen.preview hf354 --out work/hf354`
