# 근로계약서 (`employment_contract`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card employment_contract · card-hash: c4f51167f858 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** income · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 근로계약서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa employment_contract --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 고용노동부 표준근로계약서 (기간의 정함이 없는 경우) — 1.근로개시일 ~ 11.기타, 사업주·근로자 서명.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/income.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 25칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `employer.name` | 사업주 | text | 1쪽 [78, 115, 211, 128] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:50 | 묻기 |
| `employee.name` | 근로자 | text | 1쪽 [418, 114, 484, 128] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:30 | 묻기 |
| `start_date` | 근로개시일 | date | 1쪽 [187, 146, 304, 160] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:115 | 묻기 |
| `workplace` | 근무장소 | text | 1쪽 [183, 170, 359, 185] | 늘 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:140 | 묻기 |
| `job` | 업무의내용 | text | 1쪽 [191, 193, 439, 209] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:65 | 묻기 |
| `work_start` | 소정근로시간 | text | 1쪽 [203, 218, 279, 232] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:135 | 묻기 |
| `work_end` | 소정근로시간 | text | 1쪽 [331, 218, 407, 232] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:130 | 묻기 |
| `break_time` | 휴게시간 | text | 1쪽 [533, 218, 705, 232] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:15 | 묻기 |
| `work_days` | 근무일 | number | 1쪽 [241, 242, 251, 256] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:125 | 묻기 |
| `weekly_holiday` | 주휴일 | text | 1쪽 [544, 242, 561, 256] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:120 | 묻기 |
| `monthly_salary` | 월(일,시간)급 | amount | 1쪽 [219, 284, 295, 298] | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:70 | 묻기 |
| `bonus` | 상여금 | text | 1쪽 [323, 305, 355, 317] | 늘 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:5 | 묻기 |
| `other_pay` | 기타급여 | text | 1쪽 [256, 324, 288, 337] | 늘 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:75 | 묻기 |
| `pay_day` | 임금지급일 | amount | 1쪽 [360, 383, 379, 396] | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:80 | 묻기 |
| `pay_method` | 지급방법 | text | 1쪽 [377, 403, 582, 415] | 늘 | 템플릿 | generate.py | look/template.html.j2:56 · fields.json:85 | 묻기 |
| `contract_date` | 계약일 | date | 2쪽 [442, 67, 558, 81] | 늘 | 템플릿 | generate.py | look/template.html.j2:81 · fields.json:20 | 묻기 |
| `employer.phone` | 전화 | phone | 2쪽 [466, 119, 556, 131] | 늘 | 템플릿 | generate.py | look/template.html.j2:84 · fields.json:55 | 묻기 |
| `employer.address` | 주소 | text | 2쪽 [275, 140, 553, 153] | 늘 | 템플릿 | generate.py | look/template.html.j2:85 · fields.json:40 | 묻기 |
| `employer.ceo` | 대표자 | text | 2쪽 [275, 170, 323, 183] | 늘 | 템플릿 | generate.py | look/template.html.j2:86 · fields.json:45 | 묻기 |
| `employee.address` | 주소 | text | 2쪽 [274, 208, 631, 224] | 늘 | 템플릿 | generate.py | look/template.html.j2:87 · fields.json:25 | 묻기 |
| `employee.phone` | 연락처 | phone | 2쪽 [274, 231, 389, 245] | 늘 | 템플릿 | generate.py | look/template.html.j2:88 · fields.json:35 | 묻기 |
| `bonus_amount` | 상여금 | - | - | 9/16 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:10 | 묻기 |
| `end_date` | 근로계약종료일 | - | - | 3/16 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:60 | 묻기 |
| `probation.period` | 수습기간 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:90 | 묻기 |
| `probation.wage_rate` | 수습기간임금지급률 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:95 | 묻기 |

## 표 `allowances` (표 과제 table·table_read·table_find·table_qa) — 2열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `allowances.*.name` | 기타급여(제수당등) | text | 1쪽 [119, 343, 152, 356] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:155 | 묻기 |
| `allowances.*.amount` | 기타급여(제수당등) | amount | 1쪽 [163, 343, 242, 357] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:150 | 묻기 |

## 표 `special_terms` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `special_terms.*` | 특약사항 | text | 1쪽 [112, 664, 605, 681] (1행) | 3/16 | 템플릿 | generate.py | - | 묻기 |

## 체크·도장·서명 (marks) — 3칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.employer` | 사용자 | seal | 2쪽 [383, 158, 439, 197] | 늘 | 템플릿 | generate.py | fields.json:105 | 묻기 |
| `seal.employee` | 근로자 | seal | 2쪽 [357, 253, 400, 271] | 늘 | 템플릿 | generate.py | fields.json:100 | 묻기 |
| `sign.employee` | 근로자 | signature | 2쪽 [357, 253, 400, 271] | 늘 | 템플릿 | generate.py | fields.json:110 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키는·값은:** 어디서 정해지나. 키·값 종류는 이 서식 파일에 적힌 그대로입니다 (모든 서식 공통 키 사전은 없음). "키 설명 그대로" 는 칸에 `"key"` 가 없어 키 설명이 키로 나가는 것. 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
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
"근로계약서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2021년 3월 1일",
 "051-509-1176",
 "부산광역시 해운대구 해운대로 326, 7층",
 "박정연",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "010-6144-1173"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"박정연"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"010-6144-1173"
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
- contract_date: 계약일
- employer.phone: 전화
- employer.address: 주소 (같은 설명 중 1번째 칸)
- employer.ceo: 대표자
- employee.address: 주소 (같은 설명 중 2번째 칸)
- employee.phone: 연락처
```

답:

```json
[{"key": "contract_date", "value": "2021년 3월 1일", "bbox_2d": [442, 67, 558, 81], "page": 1},
 {"key": "employer.phone", "value": "051-509-1176", "bbox_2d": [466, 119, 556, 131], "page": 1},
 {"key": "employer.address", "value": "부산광역시 해운대구 해운대로 326, 7층", "bbox_2d": [275, 140, 553, 153], "page": 1},
 {"key": "employer.ceo", "value": "박정연", "bbox_2d": [275, 170, 323, 183], "page": 1},
 {"key": "employee.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [274, 208, 631, 224], "page": 1},
 {"key": "employee.phone", "value": "010-6144-1173", "bbox_2d": [274, 231, 389, 245], "page": 1}]
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
- seal.employer: 사용자 (도장)
- seal.employee: 근로자 (같은 설명 중 1번째 칸, 도장)
- sign.employee: 근로자 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.employer", "value": true, "bbox_2d": [383, 158, 439, 197], "page": 1},
 {"key": "seal.employee", "value": false},
 {"key": "sign.employee", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa employment_contract --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check employment_contract` → `python -m docgen.formdir card employment_contract` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa employment_contract --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions employment_contract --show` · `python -m docgen.preview employment_contract --out work/employment_contract`
