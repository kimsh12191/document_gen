# 법인인감증명서 (`corporate_seal_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card corporate_seal_certificate · card-hash: 162b83be6e9a -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** corporate · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 법인인감증명서
- **쓰이는 업무:** 법인 여신
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa corporate_seal_certificate --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 등기소 발급 법인 인감증명서.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/corporate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 14칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [146, 60, 265, 69] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:35 | 묻기 |
| `reg_no` | 등기번호 | number | 1쪽 [264, 173, 311, 186] | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:50 | 묻기 |
| `corp_reg_no` | 등록번호 | corp_reg_no | 1쪽 [264, 206, 371, 218] | 늘 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:15 | 묻기 |
| `corp.name` ← `company_name` | 상호 | text | 1쪽 [264, 239, 409, 251] | 늘 | 템플릿 | generate.py | look/template.html.j2:26 · fields.json:5 | 묻기 |
| `head_office` | 본점 | text | 1쪽 [264, 271, 625, 299] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:25 | 묻기 |
| `rep_title` | 자격 | text | 1쪽 [264, 320, 327, 332] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:70 | 묻기 |
| `corp.ceo` ← `rep_name` | 성명 | text | 1쪽 [335, 320, 398, 332] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:60 | 묻기 |
| `rep_rrn` | 주민등록번호 | rrn | 1쪽 [264, 352, 371, 365] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:65 | 묻기 |
| `purpose` | 용도 | text | 1쪽 [264, 385, 346, 397] | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:45 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [435, 479, 565, 491] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:30 | 묻기 |
| `issue_office` | 발급기관 | text | 1쪽 [264, 515, 490, 533] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:40 | 묻기 |
| `registrar` | 등기관 | text | 1쪽 [593, 515, 666, 533] | 11/16 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:55 | 묻기 |
| `fee` | 수수료 | amount | 1쪽 [124, 578, 165, 588] | 늘 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:20 | 묻기 |
| `confirm_no` | 발급확인번호 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:10 | 묻기 |

## 체크·도장·서명 (marks) — 2칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.registered` | 등록인감 | seal | 1쪽 [692, 233, 874, 362] | 늘 | 템플릿 | generate.py | fields.json:80 | 묻기 |
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [702, 494, 791, 557] | 늘 | 템플릿 | generate.py | fields.json:75 | 묻기 |

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
"법인인감증명서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "8778-2916-9695-4198",
 "287744",
 "200112-7951835",
 "주식회사 미래케미칼",
 "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)",
 "대표이사",
 "남궁예태",
 "850328-2******",
 "은행 제출용",
 "2025년 03월 30일",
 "제주지방법원 등기과",
 "현진윤",
 "1,000원"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"200112-7951835"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"대표이사"
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
- issue_no: 발급번호
- reg_no: 등기번호
- corp_reg_no: 등록번호
- corp.name: 상호 (법인·사업자 상호)
- head_office: 본점
- rep_title: 자격
- corp.ceo: 성명 (법인·사업자 대표자)
- rep_rrn: 주민등록번호
- purpose: 용도
- issue_date: 발급일
- issue_office: 발급기관
- registrar: 등기관
- fee: 수수료
```

답:

```json
[{"key": "issue_no", "value": "8778-2916-9695-4198", "bbox_2d": [146, 60, 265, 69], "page": 1},
 {"key": "reg_no", "value": "287744", "bbox_2d": [264, 173, 311, 186], "page": 1},
 {"key": "corp_reg_no", "value": "200112-7951835", "bbox_2d": [264, 206, 371, 218], "page": 1},
 {"key": "corp.name", "value": "주식회사 미래케미칼", "bbox_2d": [264, 239, 409, 251], "page": 1},
 {"key": "head_office", "value": "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)", "bbox_2d": [264, 271, 625, 299], "page": 1},
 {"key": "rep_title", "value": "대표이사", "bbox_2d": [264, 320, 327, 332], "page": 1},
 {"key": "corp.ceo", "value": "남궁예태", "bbox_2d": [335, 320, 398, 332], "page": 1},
 {"key": "rep_rrn", "value": "850328-2******", "bbox_2d": [264, 352, 371, 365], "page": 1},
 {"key": "purpose", "value": "은행 제출용", "bbox_2d": [264, 385, 346, 397], "page": 1},
 {"key": "issue_date", "value": "2025년 03월 30일", "bbox_2d": [435, 479, 565, 491], "page": 1},
 {"key": "issue_office", "value": "제주지방법원 등기과", "bbox_2d": [264, 515, 490, 533], "page": 1},
 {"key": "registrar", "value": "현진윤", "bbox_2d": [593, 515, 666, 533], "page": 1},
 {"key": "fee", "value": "1,000원", "bbox_2d": [124, 578, 165, 588], "page": 1}]
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
- seal.registered: 등록인감 (도장)
- seal.issuer: 발급기관직인 (도장)
```

답:

```json
[{"key": "seal.registered", "value": true, "bbox_2d": [692, 233, 874, 362], "page": 1},
 {"key": "seal.issuer", "value": true, "bbox_2d": [702, 494, 791, 557], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa corporate_seal_certificate --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check corporate_seal_certificate` → `python -m docgen.formdir card corporate_seal_certificate` (실제 질문→답 확인).

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
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa corporate_seal_certificate --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions corporate_seal_certificate --show` · `python -m docgen.preview corporate_seal_certificate --out work/corporate_seal_certificate`
