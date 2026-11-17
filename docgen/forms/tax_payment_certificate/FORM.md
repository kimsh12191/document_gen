# 납세증명서(국세완납증명) (`tax_payment_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card tax_payment_certificate · card-hash: fbafd5c2cd76 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** tax · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 납세증명서(국세완납증명) (다른 이름: 납세증명서)
- **질문·답:** 이 폴더의 `questions.json` 에서 바꾼 것이 있음 (아래 ← 바꿈)
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa tax_payment_certificate --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 홈택스 발급 국세 납세증명서 (개인사업자).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `questions.json` | 기본 과제의 질문 문장·답 틀 (기본과 다른 것만) |
| `docgen/docs/business.py`, `docgen/docs/tax.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 14칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [78, 96, 192, 107] | 늘 | 템플릿 | generate.py | look/template.html.j2:24 · fields.json:20 | 묻기 |
| `taxpayer.trade_name` | 상호(법인명) | text | 1쪽 [305, 125, 367, 138] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:70 | 묻기 |
| `taxpayer.biz_no` | 사업자등록번호 | biz_no | 1쪽 [724, 125, 811, 138] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:55 | 묻기 |
| `taxpayer.name` | 성명(대표자) | text | 1쪽 [305, 161, 367, 173] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:60 | 묻기 |
| `taxpayer.rrn` | 주민등록번호 | rrn | 1쪽 [724, 161, 829, 173] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:65 | 묻기 |
| `taxpayer.address` | 주소(본점) | text | 1쪽 [305, 197, 838, 209] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:50 | 묻기 |
| `valid_period` | 증명서유효기간 | text | 1쪽 [305, 225, 554, 238] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:75 | 묻기 |
| `valid_reason` | 유효기간을정한사유 | text | - | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:80 | 묻기 |
| `purpose` | 사용목적 | text | 1쪽 [574, 282, 671, 294] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:35 | 묻기 |
| `payer` | 대금지급자 | text | 1쪽 [305, 310, 383, 323] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:30 | 묻기 |
| `deferral` | 연장ㆍ유예명세 | text | 1쪽 [472, 407, 528, 418] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:10 | 묻기 |
| `arrears` | 체납액 | text | 1쪽 [305, 449, 336, 461] | 늘 | 템플릿 | generate.py | look/template.html.j2:56 · fields.json:5 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [437, 581, 563, 594] | 늘 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:15 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [397, 613, 581, 633] | 늘 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:25 | 묻기 |

## 체크·도장·서명 (marks) — 2칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `purpose_type` | 사용목적 | checkbox (대금 수령 / 해외이주 / 기타) | 1쪽 [328, 282, 394, 294] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:40 | 묻기 |
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [569, 592, 658, 656] | 늘 | 템플릿 | generate.py | fields.json:45 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키는·값은:** 어디서 정해지나. 키·값 종류는 이 서식 파일에 적힌 그대로입니다 (모든 서식 공통 키 사전은 없음). "키 설명 그대로" 는 칸에 `"key"` 가 없어 키 설명이 키로 나가는 것. 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
- **고칠 곳:** html·코드 서식은 템플릿 줄(칸 자리·키·항목명)과 fields.json 줄(값 출처·질문 설정 q), 원본 서식은 fields.json 의 그 칸(박스 `rect`·항목명·키·값·q). html·코드 서식에서 fields.json 에 줄이 없는 칸의 질문 설정은 fields.json 맨 위 `"q": {"키": {…}}` 묶음에.

## 질문 → 답 (seed 1000000 로 그린 실제 문항)

질문은 모델에게 가는 글 전부, 답은 데이터의 정답 (그린 문서의 값·위치). 질문 문장·답 꼴은 이 폴더 `questions.json` 과 공통 `docgen/forms/_common/questions.json`.

### 서류 분류 `classify` · 채점 acc

질문:

```
이 문서는 고객이 은행에 제출한 서류입니다. 서류의 정식 명칭(서류명)을 답하세요. 설명 없이 서류명만 한 줄로 답하세요.
```

답:

```json
"납세증명서(국세완납증명)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "7452-462-3773-485",
 "새한커피",
 "133-64-53148",
 "남궁예태",
 "850328-2******",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "2025년 04월 01일 ~ 2025년 04월 30일",
 "용역대금 수령",
 "서울특별시",
 "해당없음",
 "없음",
 "2025년 04월 01일",
 "반포세무서장"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"850328-2******"
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
항목 (키: 설명 (몇 번째 행))
- issue_no: 발급번호
- taxpayer.trade_name: 상호(법인명)
- taxpayer.biz_no: 사업자등록번호
- taxpayer.name: 성명(대표자)
- taxpayer.rrn: 주민등록번호
- taxpayer.address: 주소(본점)
- valid_period: 증명서유효기간
- valid_reason: 유효기간을정한사유
- purpose: 사용목적
- payer: 대금지급자
- deferral: 연장ㆍ유예명세
- arrears: 체납액
- issue_date: 발급일
- issuer: 발급기관
```

답:

```json
[{"key": "issue_no", "value": "7452-462-3773-485", "bbox_2d": [78, 96, 192, 107], "page": 1},
 {"key": "taxpayer.trade_name", "value": "새한커피", "bbox_2d": [305, 125, 367, 138], "page": 1},
 {"key": "taxpayer.biz_no", "value": "133-64-53148", "bbox_2d": [724, 125, 811, 138], "page": 1},
 {"key": "taxpayer.name", "value": "남궁예태", "bbox_2d": [305, 161, 367, 173], "page": 1},
 {"key": "taxpayer.rrn", "value": "850328-2******", "bbox_2d": [724, 161, 829, 173], "page": 1},
 {"key": "taxpayer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [305, 197, 838, 209], "page": 1},
 {"key": "valid_period", "value": "2025년 04월 01일 ~ 2025년 04월 30일", "bbox_2d": [305, 225, 554, 238], "page": 1},
 {"key": "valid_reason", "value": null},
 {"key": "purpose", "value": "용역대금 수령", "bbox_2d": [574, 282, 671, 294], "page": 1},
 {"key": "payer", "value": "서울특별시", "bbox_2d": [305, 310, 383, 323], "page": 1},
 {"key": "deferral", "value": "해당없음", "bbox_2d": [472, 407, 528, 418], "page": 1},
 {"key": "arrears", "value": "없음", "bbox_2d": [305, 449, 336, 461], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [437, 581, 563, 594], "page": 1},
 {"key": "issuer", "value": "반포세무서장", "bbox_2d": [397, 613, 581, 633], "page": 1}]
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
- purpose_type: 사용목적 (체크박스, 보기: 대금 수령 / 해외이주 / 기타)
- seal.issuer: 발급기관직인 (도장)
```

답:

```json
[{"key": "purpose_type", "value": "대금 수령", "bbox_2d": [305, 282, 324, 294], "page": 1},
 {"key": "seal.issuer", "value": true, "bbox_2d": [569, 592, 658, 656], "page": 1}]
```

### 표 찾기 `table_find` · 채점 f1_iou50 (위치)

질문:

```
이 문서에서 표를 모두 찾아 JSON 목록으로 답하세요. 여기서 표는 같은 항목 묶음(열)이 행마다 되풀이되고 행 수가 서류마다 달라지는 목록입니다. 항목명과 값이 번갈아 있는 신청서 칸, 칸 수가 정해진 결재란은 표가 아닙니다.
표마다 {{"columns": [머리글 글자, …], "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호, "n_rows": 행 수}} 를 쓰고, 여러 쪽에 걸친 표는 쪽마다 따로 씁니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 행 수에는 머리글·합계 행과 모두 빈 행을 넣지 않습니다. 표가 없으면 [] 로 답하세요.
```

답:

```json
[]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa tax_payment_certificate --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check tax_payment_certificate` → `python -m docgen.formdir card tax_payment_certificate` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `generate.py` 가 돌려주는 dict 에 그 키 값 | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` | 다시 |
| 답의 값 | `generate.py` (값 만드는 함수). 파이썬 대신 정하려면 `fields.json` 의 그 칸 `source` | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (파일로). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa tax_payment_certificate --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions tax_payment_certificate --show` · `python -m docgen.preview tax_payment_certificate --out work/tax_payment_certificate`
