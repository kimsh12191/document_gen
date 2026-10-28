# 국민연금 가입자 가입증명 (`pension_enrollment_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card pension_enrollment_certificate · card-hash: 93c3370c517c -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** income · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 국민연금 가입자 가입증명
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 국민연금공단 발급 가입자 가입증명 — 국민연금법 시행규칙 [별지 제11호서식] 국민연금가입자증명서.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/income.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 14칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [242, 164, 378, 177] | 늘 | 템플릿 | generate.py | look/template.html.j2:15 · fields.json:20 | 묻기 |
| `issue_date_head` | 발급일자 | date | 1쪽 [686, 164, 759, 177] | 늘 | 템플릿 | generate.py | look/template.html.j2:15 · fields.json:15 | 묻기 |
| `customer.name` ← `person.name` | 성명 | text | 1쪽 [242, 193, 307, 206] | 늘 | 템플릿 | generate.py | look/template.html.j2:16 · fields.json:25 | 묻기 |
| `customer.rrn` ← `person.rrn` | 주민등록번호 | rrn | 1쪽 [686, 193, 797, 206] | 늘 | 템플릿 | generate.py | look/template.html.j2:16 · fields.json:30 | 묻기 |
| `first_acquired` | 최초자격취득일 | date | 1쪽 [292, 260, 366, 273] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:5 | 묻기 |
| `total_months` | 가입기간합계 | text | 1쪽 [711, 260, 768, 273] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:45 | 묻기 |
| `rows.*.kind` | 가입자종류 | text | 1쪽 [155, 324, 250, 336] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:60 | 묻기 |
| `rows.*.workplace` | 사업장명칭 | text | 1쪽 [342, 324, 447, 336] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:80 | 묻기 |
| `rows.*.start` | 자격취득일 | date | 1쪽 [547, 324, 618, 336] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:70 | 묻기 |
| `rows.*.end` | 자격상실일 | date | 1쪽 [673, 324, 744, 336] (1행) | 11/16 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:55 | 묻기 |
| `rows.*.wage` | 기준소득월액 | amount | 1쪽 [846, 324, 909, 336] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:75 | 묻기 |
| `purpose` | 용도 | text | 1쪽 [242, 498, 328, 512] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:35 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [442, 653, 558, 667] | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:10 | 묻기 |
| `rows.*.note` | 비고 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:65 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [625, 665, 715, 729] | 늘 | 템플릿 | generate.py | fields.json:40 | 묻기 |

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
"국민연금 가입자 가입증명"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "20250401-32717430",
 "2025.04.01",
 "남궁예태",
 "850328-2******",
 "2012.07.01",
 "154개월",
 "사업장가입자",
 "(주)새한메디칼",
 "2021.03.06",
 "1,484,000",
 "주식회사 다온패션",
 "4,108,000",
 "은행 제출용",
 "2025년 4월 1일"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2012.07.01"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"1,484,000"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- issue_no: 발급번호
- issue_date_head: 발급일자
- customer.name: 성명 (고객 성명)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- first_acquired: 최초자격취득일
- total_months: 가입기간합계
- rows.0.kind: 가입자종류 (1행)
- rows.0.workplace: 사업장명칭 (1행)
- rows.0.start: 자격취득일 (1행)
- rows.0.end: 자격상실일 (1행)
- rows.0.wage: 기준소득월액 (1행)
- rows.1.kind: 가입자종류 (2행)
- rows.1.workplace: 사업장명칭 (2행)
- rows.1.start: 자격취득일 (2행)
- rows.1.wage: 기준소득월액 (2행)
- purpose: 용도
- issue_date: 발급일
```

답:

```json
[{"key": "issue_no", "value": "20250401-32717430", "bbox_2d": [242, 164, 378, 177], "page": 1},
 {"key": "issue_date_head", "value": "2025.04.01", "bbox_2d": [686, 164, 759, 177], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [242, 193, 307, 206], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [686, 193, 797, 206], "page": 1},
 {"key": "first_acquired", "value": "2012.07.01", "bbox_2d": [292, 260, 366, 273], "page": 1},
 {"key": "total_months", "value": "154개월", "bbox_2d": [711, 260, 768, 273], "page": 1},
 {"key": "rows.0.kind", "value": "사업장가입자", "bbox_2d": [155, 324, 250, 336], "page": 1},
 {"key": "rows.0.workplace", "value": "(주)새한메디칼", "bbox_2d": [342, 324, 447, 336], "page": 1},
 {"key": "rows.0.start", "value": "2012.07.01", "bbox_2d": [547, 324, 618, 336], "page": 1},
 {"key": "rows.0.end", "value": "2021.03.06", "bbox_2d": [673, 324, 744, 336], "page": 1},
 {"key": "rows.0.wage", "value": "1,484,000", "bbox_2d": [846, 324, 909, 336], "page": 1},
 {"key": "rows.1.kind", "value": "사업장가입자", "bbox_2d": [155, 352, 250, 364], "page": 1},
 {"key": "rows.1.workplace", "value": "주식회사 다온패션", "bbox_2d": [330, 352, 460, 364], "page": 1},
 {"key": "rows.1.start", "value": "2021.03.06", "bbox_2d": [547, 352, 618, 364], "page": 1},
 {"key": "rows.1.wage", "value": "4,108,000", "bbox_2d": [846, 352, 909, 364], "page": 1},
 {"key": "purpose", "value": "은행 제출용", "bbox_2d": [242, 498, 328, 512], "page": 1},
 {"key": "issue_date", "value": "2025년 4월 1일", "bbox_2d": [442, 653, 558, 667], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.issuer: 발급기관직인 (도장)
```

답:

```json
[{"key": "seal.issuer", "value": true, "bbox_2d": [625, 665, 715, 729], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check pension_enrollment_certificate` → `python -m docgen.formdir card pension_enrollment_certificate` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `generate.py` 가 돌려주는 dict 에 그 키 값 | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` | 다시 |
| 답의 값 | `generate.py` (값 만드는 함수). 파이썬 대신 정하려면 `fields.json` 의 그 칸 `source` | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (studio html 편집). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions pension_enrollment_certificate --show` · `python -m docgen.preview pension_enrollment_certificate --out work/pension_enrollment_certificate`
