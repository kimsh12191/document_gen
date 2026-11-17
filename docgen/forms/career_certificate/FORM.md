# 경력증명서 (`career_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card career_certificate · card-hash: 0141fc43116a -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** income · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 경력증명서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa career_certificate --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 현 직장이 발급하는 경력증명서 (근로기준법 제39조 사용증명서, 통용 양식: 인적사항 / 경력사항

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/income.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 15칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `doc_no` | 문서번호 | text | 1쪽 [147, 60, 234, 70] | 늘 | 템플릿 | generate.py | look/template.html.j2:9 · fields.json:30 | 묻기 |
| `person.name` | 성명 | text | 1쪽 [234, 171, 299, 183] | 늘 | 템플릿 | generate.py | look/template.html.j2:12 · fields.json:50 | 묻기 |
| `person.rrn` | 주민등록번호 | rrn | 1쪽 [640, 171, 751, 183] | 늘 | 템플릿 | generate.py | look/template.html.j2:12 · fields.json:60 | 묻기 |
| `person.address` | 주소 | text | 1쪽 [234, 202, 793, 214] | 늘 | 템플릿 | generate.py | look/template.html.j2:13 · fields.json:45 | 묻기 |
| `person.phone` | 연락처 | phone | 1쪽 [234, 233, 334, 246] | 늘 | 템플릿 | generate.py | look/template.html.j2:13 · fields.json:55 | 묻기 |
| `hire_date` | 입사일 | date | 1쪽 [640, 233, 713, 246] | 늘 | 템플릿 | generate.py | look/template.html.j2:13 · fields.json:35 | 묻기 |
| `total_period` | 총근무기간 | text | 1쪽 [609, 458, 675, 470] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:80 | 묻기 |
| `purpose` | 용도 | text | 1쪽 [234, 496, 320, 508] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:65 | 묻기 |
| `submit_to` | 제출처 | text | 1쪽 [680, 496, 745, 508] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:75 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [434, 617, 566, 629] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:40 | 묻기 |
| `company.name` | 회사명 | text | 1쪽 [420, 653, 564, 666] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:20 | 묻기 |
| `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [420, 675, 519, 689] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:10 | 묻기 |
| `company.address` | 소재지 | text | 1쪽 [420, 698, 722, 711] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:5 | 묻기 |
| `company.phone` | 전화번호 | phone | 1쪽 [420, 721, 519, 734] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:25 | 묻기 |
| `company.ceo` | 대표이사 | text | 1쪽 [500, 758, 571, 775] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:15 | 묻기 |

## 표 `careers` (표 과제 table·table_read·table_find·table_qa) — 4열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `careers.*.period` | 근무기간 | text | 1쪽 [146, 336, 303, 348] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:100 | 묻기 |
| `careers.*.department` | 근무부서 | text | 1쪽 [410, 336, 465, 348] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:90 | 묻기 |
| `careers.*.position` | 직위 | text | 1쪽 [543, 336, 574, 348] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:105 | 묻기 |
| `careers.*.duty` | 담당업무 | text | 1쪽 [622, 336, 793, 348] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:95 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.company` | 회사직인 | seal | 1쪽 [573, 736, 663, 799] | 늘 | 템플릿 | generate.py | fields.json:70 | 묻기 |

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
"경력증명서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "제 2025-850 호",
 "남궁예태",
 "850328-2******",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "010-6144-1173",
 "2021.03.06",
 "2021.03.06 ~ 2022.12.31",
 "영업1팀",
 "사원",
 "국내 영업 및 거래처 관리",
 "2023.01.01 ~ 2024.12.31",
 "생산관리팀",
 "주임",
 "생산계획 및 공정관리",
 "2025.01.01 ~ 현재",
 "고객지원팀",
 "대리",
 "고객 상담 및 CS 관리",
 "4년 0개월",
 "대출 신청용",
 "국민은행",
 "2025년 04월 01일",
 "주식회사 다온패션",
 "123-88-81212",
 "부산광역시 해운대구 해운대로 326, 7층",
 "051-509-1176",
 "박정연"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"국내 영업 및 거래처 관리"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"국민은행"
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
- doc_no: 문서번호
- person.name: 성명
- person.rrn: 주민등록번호
- person.address: 주소
- person.phone: 연락처
- hire_date: 입사일
- total_period: 총근무기간
- purpose: 용도
- submit_to: 제출처
- issue_date: 발급일
- company.name: 회사명
- company.biz_no: 사업자등록번호
- company.address: 소재지
- company.phone: 전화번호
- company.ceo: 대표이사
```

답:

```json
[{"key": "doc_no", "value": "제 2025-850 호", "bbox_2d": [147, 60, 234, 70], "page": 1},
 {"key": "person.name", "value": "남궁예태", "bbox_2d": [234, 171, 299, 183], "page": 1},
 {"key": "person.rrn", "value": "850328-2******", "bbox_2d": [640, 171, 751, 183], "page": 1},
 {"key": "person.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [234, 202, 793, 214], "page": 1},
 {"key": "person.phone", "value": "010-6144-1173", "bbox_2d": [234, 233, 334, 246], "page": 1},
 {"key": "hire_date", "value": "2021.03.06", "bbox_2d": [640, 233, 713, 246], "page": 1},
 {"key": "total_period", "value": "4년 0개월", "bbox_2d": [609, 458, 675, 470], "page": 1},
 {"key": "purpose", "value": "대출 신청용", "bbox_2d": [234, 496, 320, 508], "page": 1},
 {"key": "submit_to", "value": "국민은행", "bbox_2d": [680, 496, 745, 508], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [434, 617, 566, 629], "page": 1},
 {"key": "company.name", "value": "주식회사 다온패션", "bbox_2d": [420, 653, 564, 666], "page": 1},
 {"key": "company.biz_no", "value": "123-88-81212", "bbox_2d": [420, 675, 519, 689], "page": 1},
 {"key": "company.address", "value": "부산광역시 해운대구 해운대로 326, 7층", "bbox_2d": [420, 698, 722, 711], "page": 1},
 {"key": "company.phone", "value": "051-509-1176", "bbox_2d": [420, 721, 519, 734], "page": 1},
 {"key": "company.ceo", "value": "박정연", "bbox_2d": [500, 758, 571, 775], "page": 1}]
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
- seal.company: 회사직인 (도장)
```

답:

```json
[{"key": "seal.company", "value": true, "bbox_2d": [573, 736, 663, 799], "page": 1}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[82, 296, 918, 409] 위치의 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 설명)
- period: 근무기간
- department: 근무부서
- position: 직위
- duty: 담당업무
```

답:

```json
{
 "columns": [
  "period",
  "department",
  "position",
  "duty"
 ],
 "rows": [
  [
   "2021.03.06 ~ 2022.12.31",
   "영업1팀",
   "사원",
   "국내 영업 및 거래처 관리"
  ],
  [
   "2023.01.01 ~ 2024.12.31",
   "생산관리팀",
   "주임",
   "생산계획 및 공정관리"
  ],
  [
   "2025.01.01 ~ 현재",
   "고객지원팀",
   "대리",
   "고객 상담 및 CS 관리"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    146,
    336,
    793,
    348
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    146,
    366,
    770,
    379
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    166,
    397,
    766,
    409
   ],
   "page": 1
  }
 ]
}
```

### 표 찾기 `table_find` · 채점 f1_iou50 (위치)

질문:

```
이 문서에서 표를 모두 찾아 JSON 목록으로 답하세요. 여기서 표는 같은 항목 묶음(열)이 행마다 되풀이되고 행 수가 서류마다 달라지는 목록입니다. 항목명과 값이 번갈아 있는 신청서 칸, 칸 수가 정해진 결재란은 표가 아닙니다.
표마다 {{"columns": [머리글 글자, …], "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호, "n_rows": 행 수}} 를 쓰고, 여러 쪽에 걸친 표는 쪽마다 따로 씁니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 행 수에는 머리글·합계 행과 모두 빈 행을 넣지 않습니다. 표가 없으면 [] 로 답하세요.
```

답:

```json
[{"columns": ["근무기간", "근무부서", "직위", "담당업무"], "bbox_2d": [82, 296, 918, 409], "page": 1, "n_rows": 3}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '직위'·'담당업무' 열이 있는 표를 보고 답하세요. '근무기간' 칸이 '2025.01.01 ~ 현재'인 행의 '근무부서' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"고객지원팀"
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '직위'·'담당업무' 열이 있는 표를 보고 답하세요. '근무부서' 칸이 '고객지원팀'인 행은 몇 개입니까? (숫자만 답하세요)
```

답:

```json
1
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa career_certificate --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check career_certificate` → `python -m docgen.formdir card career_certificate` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa career_certificate --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions career_certificate --show` · `python -m docgen.preview career_certificate --out work/career_certificate`
