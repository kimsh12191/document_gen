# 주민등록표 초본 (`resident_registration_abstract`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card resident_registration_abstract · card-hash: eec1096967a0 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** family · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 주민등록표 초본 (다른 이름: 주민등록표(초본))
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa resident_registration_abstract --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 주민등록표 초본 (개인 인적사항 + 주소 변동 이력). 이사가 잦은 사람은 여러 쪽이 된다.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/family.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 11칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `doc_no` | 발급번호 / 문서확인번호 | text | 1쪽 [132, 62, 193, 72] | 늘 | 템플릿 | generate.py | fields.json:10 | 묻기 |
| `officer` | 담당자 | text | 1쪽 [154, 159, 196, 170] | 5/16 | 템플릿 | generate.py | fields.json:30 | 묻기 |
| `officer_phone` | 전화 | phone | 1쪽 [249, 159, 329, 170] | 5/16 | 템플릿 | generate.py | fields.json:35 | 묻기 |
| `applicant` | 신청인 | text | 1쪽 [161, 174, 217, 185] | 늘 | 템플릿 | generate.py | fields.json:5 | 묻기 |
| `purpose` | 용도및목적 | text | 1쪽 [327, 174, 412, 185] | 늘 | 템플릿 | generate.py | fields.json:55 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [817, 191, 932, 201] | 늘 | 템플릿 | generate.py | fields.json:20 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [534, 210, 859, 227] | 늘 | 템플릿 | generate.py | fields.json:25 | 묻기 |
| `customer.name` ← `person.name` | 성명 | text | 1쪽 [219, 258, 276, 268] | 늘 | 템플릿 | generate.py | look/template.html.j2:15 · fields.json:40 | 묻기 |
| `customer.name_hanja` ← `person.name_hanja` | 한자 | text | 1쪽 [284, 258, 340, 268] | 늘 | 템플릿 | generate.py | look/template.html.j2:15 · fields.json:45 | 묻기 |
| `customer.rrn` ← `person.rrn` | 주민등록번호 | rrn | 1쪽 [764, 258, 860, 268] | 늘 | 템플릿 | generate.py | look/template.html.j2:15 · fields.json:50 | 묻기 |
| `history_scope` | 주소변동사항 | text | 1쪽 [868, 289, 923, 300] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:15 | 묻기 |

## 표 `addresses` (표 과제 table·table_read·table_find·table_qa) — 7열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `addresses.*.no` | 번호 | number | 1쪽 [94, 367, 101, 378] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:90 | 묻기 |
| `addresses.*.address` | 주소 | text | 1쪽 [139, 358, 623, 369] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:70 | 묻기 |
| `addresses.*.moved_in` | 전입일 | date | 1쪽 [768, 358, 831, 369] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:85 | 묻기 |
| `addresses.*.changed` | 변동일 | date | 1쪽 [842, 358, 906, 369] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:75 | 묻기 |
| `addresses.*.head_relation` | 세대주및관계 | text | 1쪽 [139, 376, 241, 387] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:80 | 묻기 |
| `addresses.*.status` | 등록상태 | text | 1쪽 [652, 376, 694, 387] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:100 | 묻기 |
| `addresses.*.reason` | 변동사유 | text | 1쪽 [823, 376, 851, 387] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:95 | 묻기 |

## 표 `person_changes` (표 과제 table·table_read·table_find·table_qa) — 4열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `person_changes.*.no` | 번호 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:120 | 묻기 |
| `person_changes.*.content` | 변경내용 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:115 | 묻기 |
| `person_changes.*.changed` | 변동일 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:110 | 묻기 |
| `person_changes.*.reason` | 변동사유 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:125 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [890, 200, 979, 264] | 늘 | 템플릿 | generate.py | fields.json:60 | 묻기 |

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
"주민등록표 초본"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "제 8109 호",
 "정민빈",
 "02-3180-0289",
 "남궁예태",
 "금융기관제출",
 "2025년 04월 01일",
 "서울특별시 서초구 반포동장",
 "南宮叡兌",
 "850328-2******",
 "최근 5년",
 "1",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "2024.02.15",
 "남궁예태의 본인",
 "거주자",
 "전입"
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
"전입"
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
- correction.permitted: 정정허가일
- doc_no: 발급번호
- officer: 담당자
- officer_phone: 전화
- applicant: 신청인
- purpose: 용도및목적
- issue_date: 발급일
- issuer: 발급기관
- customer.name: 성명 (고객 성명)
- naturalization.notifier: 통보자
- customer.name_hanja: 한자 (고객 한자 성명)
- name_change.court: 허가법원
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- history_scope: 주소변동사항
```

답:

```json
[{"key": "correction.permitted", "value": null},
 {"key": "doc_no", "value": "제 8109 호", "bbox_2d": [132, 62, 193, 72], "page": 1},
 {"key": "officer", "value": "정민빈", "bbox_2d": [154, 159, 196, 170], "page": 1},
 {"key": "officer_phone", "value": "02-3180-0289", "bbox_2d": [249, 159, 329, 170], "page": 1},
 {"key": "applicant", "value": "남궁예태", "bbox_2d": [161, 174, 217, 185], "page": 1},
 {"key": "purpose", "value": "금융기관제출", "bbox_2d": [327, 174, 412, 185], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [817, 191, 932, 201], "page": 1},
 {"key": "issuer", "value": "서울특별시 서초구 반포동장", "bbox_2d": [534, 210, 859, 227], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [219, 258, 276, 268], "page": 1},
 {"key": "naturalization.notifier", "value": null},
 {"key": "customer.name_hanja", "value": "南宮叡兌", "bbox_2d": [284, 258, 340, 268], "page": 1},
 {"key": "name_change.court", "value": null},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [764, 258, 860, 268], "page": 1},
 {"key": "history_scope", "value": "최근 5년", "bbox_2d": [868, 289, 923, 300], "page": 1}]
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
- seal.issuer: 발급기관직인 (도장)
```

답:

```json
[{"key": "seal.issuer", "value": true, "bbox_2d": [890, 200, 979, 264], "page": 1}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 '번호'·'세대주및관계' 열이 있는 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 항목명)
- no: 번호
- address: 주소
- head_relation: 세대주및관계
- status: 등록상태
- moved_in: 전입일
- reason: 변동사유
- changed: 변동일
```

답:

```json
{
 "columns": [
  "no",
  "address",
  "head_relation",
  "status",
  "moved_in",
  "reason",
  "changed"
 ],
 "rows": [
  [
   "1",
   "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
   "남궁예태의 본인",
   "거주자",
   "2024.02.15",
   "전입",
   "2024.02.15"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    94,
    358,
    906,
    387
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
[{"columns": ["번호", "주소", "세대주및관계", "등록상태", "전입일", "변동사유", "변동일"], "bbox_2d": [94, 305, 931, 387], "page": 1, "n_rows": 1}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[94, 305, 931, 387] 위치의 표를 보고 답하세요. '번호' 칸이 '1'인 행의 '세대주및관계' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"남궁예태의 본인"
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[94, 305, 931, 387] 위치의 표를 보고 답하세요. 표의 행은 모두 몇 개입니까? 머리글·합계 행과 모두 빈 행은 세지 않습니다. (숫자만 답하세요)
```

답:

```json
1
```

### 표 그대로 옮기기 `table_read` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[94, 305, 931, 387] 위치의 표를 머리글까지 그대로 옮겨 JSON 으로 답하세요.
꼴: {"columns": [머리글 글자, …], "rows": [[칸 글자, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 표의 머리글을 왼쪽부터 쓰고, 머리글이 여러 줄이면 위 칸과 아래 칸 글자를 " > " 로 잇습니다.
- rows 는 행마다 columns 와 같은 순서로 칸 글자를 씁니다. 빈 칸은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 글자를 씁니다.
- 다음 쪽에서 다시 나온 머리글 행과 모두 빈 행은 빼고, 합계·소계 행은 그대로 둡니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
```

답:

```json
{
 "columns": [
  "번호",
  "주 소 > 세대주 및 관계",
  "주 소 > 등록상태",
  "전입일 / 변동일 > 변 동 사 유"
 ],
 "rows": [
  [
   "1",
   "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
   null,
   "2024.02.15 / 2024.02.15"
  ],
  [
   "1",
   "남궁예태의 본인",
   "거주자",
   "전입"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    69,
    355,
    931,
    391
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    127,
    373,
    931,
    391
   ],
   "page": 1
  }
 ]
}
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa resident_registration_abstract --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check resident_registration_abstract` → `python -m docgen.formdir card resident_registration_abstract` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa resident_registration_abstract --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions resident_registration_abstract --show` · `python -m docgen.preview resident_registration_abstract --out work/resident_registration_abstract`
