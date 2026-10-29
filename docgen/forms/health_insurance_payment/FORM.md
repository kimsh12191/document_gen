# 건강보험료 납부확인서 (`health_insurance_payment`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card health_insurance_payment · card-hash: e30bd6bbb6f3 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** income · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 건강보험료 납부확인서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa health_insurance_payment --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 국민건강보험공단 발급 건강보험료 납부확인서 (직장가입자 본인부담분, 월별 고지·납부 보험료를 건강/장기요양 구분).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/income.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 17칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [144, 57, 237, 68] | 늘 | 템플릿 | generate.py | look/template.html.j2:9 · fields.json:10 | 묻기 |
| `customer.name` ← `person.name` | 성명 | text | 1쪽 [228, 170, 293, 184] | 늘 | 템플릿 | generate.py | look/template.html.j2:14 · fields.json:35 | 묻기 |
| `customer.rrn` ← `person.rrn` | 주민등록번호 | rrn | 1쪽 [660, 170, 772, 184] | 7/16 | 템플릿 | generate.py | look/template.html.j2:16 · fields.json:40 | 묻기 |
| `customer.address` ← `person.address` | 주소 | text | 1쪽 [228, 199, 564, 212] | 늘 | 템플릿 | generate.py | look/template.html.j2:17 · fields.json:25 | 묻기 |
| `member_kind` | 가입자구분 | text | 1쪽 [228, 227, 310, 240] | 늘 | 템플릿 | generate.py | look/template.html.j2:18 · fields.json:15 | 묻기 |
| `period` | 대상기간 | text | 1쪽 [660, 227, 784, 240] | 늘 | 템플릿 | generate.py | look/template.html.j2:18 · fields.json:20 | 묻기 |
| `employer.name` ← `workplace.name` | 사업장명칭 | text | 1쪽 [228, 255, 363, 268] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:90 | 묻기 |
| `workplace.mgmt_no` | 사업장관리번호 | number | 1쪽 [660, 255, 750, 268] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:85 | 묻기 |
| `employer.address` ← `workplace.address` | 소재지 | text | 1쪽 [228, 283, 510, 297] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:80 | 묻기 |
| `sum.notice_health` | 고지보험료(건강보험)합계 | number | 1쪽 [213, 671, 274, 684] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:65 | 묻기 |
| `sum.notice_ltc` | 고지보험료(장기요양)합계 | number | 1쪽 [326, 671, 375, 684] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:70 | 묻기 |
| `sum.health` | 납부보험료(건강보험)합계 | number | 1쪽 [424, 671, 485, 684] | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:55 | 묻기 |
| `sum.ltc` | 납부보험료(장기요양)합계 | number | 1쪽 [537, 671, 586, 684] | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:60 | 묻기 |
| `sum.total` | 납부보험료(계)합계 | amount | 1쪽 [643, 671, 704, 684] | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:75 | 묻기 |
| `purpose` | 용도 | text | 1쪽 [228, 703, 314, 716] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:45 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [442, 829, 558, 842] | 늘 | 템플릿 | generate.py | look/template.html.j2:63 · fields.json:5 | 묻기 |
| `customer.birth` ← `person.birth` | 생년월일 | - | - | 9/16 | 템플릿 | generate.py | look/template.html.j2:15 · fields.json:30 | 묻기 |

## 표 `rows` (표 과제 table·table_read·table_find·table_qa) — 8열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `rows.*.month` | 년월 | month | 1쪽 [101, 393, 150, 405] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:110 | 묻기 |
| `rows.*.notice_health` | 고지보험료(건강보험) | number | 1쪽 [225, 393, 274, 405] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:120 | 묻기 |
| `rows.*.notice_ltc` | 고지보험료(장기요양) | number | 1쪽 [334, 393, 375, 405] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:125 | 묻기 |
| `rows.*.health` | 납부보험료(건강보험) | number | 1쪽 [436, 393, 485, 405] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:100 | 묻기 |
| `rows.*.ltc` | 납부보험료(장기요양) | number | 1쪽 [544, 393, 586, 405] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:105 | 묻기 |
| `rows.*.total` | 납부보험료(계) | amount | 1쪽 [655, 393, 704, 405] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:135 | 묻기 |
| `rows.*.paid_date` | 납부일자 | date | 1쪽 [782, 393, 850, 405] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:130 | 묻기 |
| `rows.*.note` | 비고 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:115 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [630, 841, 748, 925] | 늘 | 템플릿 | generate.py | fields.json:50 | 묻기 |

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
"건강보험료 납부확인서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "63-848670-4594",
 "남궁예태",
 "850328-2******",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "직장가입자",
 "2024.03 ~ 2025.02",
 "주식회사 다온패션",
 "12388812120",
 "부산광역시 해운대구 해운대로 326, 7층",
 "2024.03",
 "140,470",
 "18,190",
 "158,660",
 "2024.04.10",
 "2024.04",
 "2024.05.10",
 "2024.05",
 "2024.06.10",
 "2024.06",
 "2024.07.10",
 "2024.07",
 "2024.08.12",
 "2024.08",
 "2024.09.10",
 "2024.09",
 "2024.10.10",
 "2024.10",
 "2024.11.11",
 "2024.11",
 "2024.12.10",
 "2024.12",
 "2025.01.10",
 "2025.01",
 "145,640",
 "18,860",
 "164,500",
 "2025.02.10",
 "2025.02",
 "2025.03.10",
 "1,695,980",
 "219,620",
 "1,915,600",
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
"18,190"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"140,470"
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
- customer.name: 성명 (고객 성명)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- customer.address: 주소 (고객 주소)
- member_kind: 가입자구분
- period: 대상기간
- employer.name: 사업장명칭 (직장 이름)
- workplace.mgmt_no: 사업장관리번호
- employer.address: 소재지 (직장 주소)
- sum.notice_health: 고지보험료(건강보험)합계
- sum.notice_ltc: 고지보험료(장기요양)합계
- sum.health: 납부보험료(건강보험)합계
- sum.ltc: 납부보험료(장기요양)합계
- sum.total: 납부보험료(계)합계
- purpose: 용도
- issue_date: 발급일
```

답:

```json
[{"key": "issue_no", "value": "63-848670-4594", "bbox_2d": [144, 57, 237, 68], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [228, 170, 293, 184], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [660, 170, 772, 184], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [228, 199, 564, 212], "page": 1},
 {"key": "member_kind", "value": "직장가입자", "bbox_2d": [228, 227, 310, 240], "page": 1},
 {"key": "period", "value": "2024.03 ~ 2025.02", "bbox_2d": [660, 227, 784, 240], "page": 1},
 {"key": "employer.name", "value": "주식회사 다온패션", "bbox_2d": [228, 255, 363, 268], "page": 1},
 {"key": "workplace.mgmt_no", "value": "12388812120", "bbox_2d": [660, 255, 750, 268], "page": 1},
 {"key": "employer.address", "value": "부산광역시 해운대구 해운대로 326, 7층", "bbox_2d": [228, 283, 510, 297], "page": 1},
 {"key": "sum.notice_health", "value": "1,695,980", "bbox_2d": [213, 671, 274, 684], "page": 1},
 {"key": "sum.notice_ltc", "value": "219,620", "bbox_2d": [326, 671, 375, 684], "page": 1},
 {"key": "sum.health", "value": "1,695,980", "bbox_2d": [424, 671, 485, 684], "page": 1},
 {"key": "sum.ltc", "value": "219,620", "bbox_2d": [537, 671, 586, 684], "page": 1},
 {"key": "sum.total", "value": "1,915,600", "bbox_2d": [643, 671, 704, 684], "page": 1},
 {"key": "purpose", "value": "은행 제출용", "bbox_2d": [228, 703, 314, 716], "page": 1},
 {"key": "issue_date", "value": "2025년 4월 1일", "bbox_2d": [442, 829, 558, 842], "page": 1}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [630, 841, 748, 925], "page": 1}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[101, 341, 921, 661] 위치의 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 항목명)
- month: 년월
- notice_health: 고지보험료(건강보험)
- notice_ltc: 고지보험료(장기요양)
- health: 납부보험료(건강보험)
- ltc: 납부보험료(장기요양)
- total: 납부보험료(계)
- paid_date: 납부일자
```

답:

```json
{
 "columns": [
  "month",
  "notice_health",
  "notice_ltc",
  "health",
  "ltc",
  "total",
  "paid_date"
 ],
 "rows": [
  [
   "2024.03",
   "140,470",
   "18,190",
   "140,470",
   "18,190",
   "158,660",
   "2024.04.10"
  ],
  [
   "2024.04",
   "140,470",
   "18,190",
   "140,470",
   "18,190",
   "158,660",
   "2024.05.10"
  ],
  [
   "2024.05",
   "140,470",
   "18,190",
   "140,470",
   "18,190",
   "158,660",
   "2024.06.10"
  ],
  [
   "2024.06",
   "140,470",
   "18,190",
   "140,470",
   "18,190",
   "158,660",
   "2024.07.10"
  ],
  [
   "2024.07",
   "140,470",
   "18,190",
   "140,470",
   "18,190",
   "158,660",
   "2024.08.12"
  ],
  [
   "2024.08",
   "140,470",
   "18,190",
   "140,470",
   "18,190",
   "158,660",
   "2024.09.10"
  ],
  [
   "2024.09",
   "140,470",
   "18,190",
   "140,470",
   "18,190",
   "158,660",
   "2024.10.10"
  ],
  [
   "2024.10",
   "140,470",
   "18,190",
   "140,470",
   "18,190",
   "158,660",
   "2024.11.11"
  ],
  [
   "2024.11",
   "140,470",
   "18,190",
   "140,470",
   "18,190",
   "158,660",
   "2024.12.10"
  ],
  [
   "2024.12",
   "140,470",
   "18,190",
   "140,470",
   "18,190",
   "158,660",
   "2025.01.10"
  ],
  [
   "2025.01",
   "145,640",
   "18,860",
   "145,640",
   "18,860",
   "164,500",
   "2025.02.10"
  ],
  [
   "2025.02",
   "145,640",
   "18,860",
   "145,640",
   "18,860",
   "164,500",
   "2025.03.10"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    101,
    393,
    850,
    405
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    101,
    416,
    850,
    428
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    101,
    439,
    850,
    452
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    101,
    462,
    850,
    475
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    101,
    486,
    850,
    498
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    101,
    509,
    850,
    521
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    101,
    532,
    850,
    545
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    101,
    555,
    849,
    568
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    101,
    579,
    850,
    591
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    101,
    602,
    850,
    614
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    101,
    625,
    850,
    637
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    101,
    648,
    850,
    661
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
[{"columns": ["년월", "고지보험료(건강보험)", "고지보험료(장기요양)", "납부보험료(건강보험)", "납부보험료(장기요양)", "납부보험료(계)", "납부일자"], "bbox_2d": [101, 341, 921, 661], "page": 1, "n_rows": 12}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[101, 341, 921, 661] 위치의 표를 보고 답하세요. '납부보험료(건강보험)' 칸의 값을 모두 더하면 얼마입니까? 빈 칸은 0 으로 봅니다. (쉼표·단위 없이 숫자만 답하세요)
```

답:

```json
1695980
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[101, 341, 921, 661] 위치의 표를 보고 답하세요. '년월' 칸이 '2024.10'인 행의 '납부보험료(계)' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"158,660"
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa health_insurance_payment --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check health_insurance_payment` → `python -m docgen.formdir card health_insurance_payment` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa health_insurance_payment --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions health_insurance_payment --show` · `python -m docgen.preview health_insurance_payment --out work/health_insurance_payment`
