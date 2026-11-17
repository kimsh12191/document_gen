# 지방세 세목별 과세증명서 (`local_tax_assessment`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card local_tax_assessment · card-hash: 86de9b569700 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** tax · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 지방세 세목별 과세증명서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa local_tax_assessment --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 주소지 시·군·구청장이 발급하는 지방세 세목별 과세증명서 (재산세·자동차세·주민세 등).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/business.py`, `docgen/docs/tax.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 11칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [248, 84, 377, 94] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:10 | 묻기 |
| `taxpayer.name` | 성명(법인명) | text | 1쪽 [378, 168, 443, 180] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:55 | 묻기 |
| `taxpayer.rrn` | 주민(법인,외국인)등록번호 | rrn | 1쪽 [731, 168, 842, 180] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:60 | 묻기 |
| `taxpayer.address` | 주소(영업소) | text | 1쪽 [378, 199, 899, 227] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:50 | 묻기 |
| `period` | 과세연도 | text | 1쪽 [378, 246, 493, 258] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:20 | 묻기 |
| `purpose` | 사용목적 | text | 1쪽 [731, 246, 800, 258] | 늘 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:25 | 묻기 |
| `sum.tax` | 세액합계 | amount | 1쪽 [665, 593, 720, 604] | 늘 | 템플릿 | generate.py | look/template.html.j2:63 · fields.json:40 | 묻기 |
| `sum.edu` | 지방교육세합계 | number | 1쪽 [763, 593, 808, 604] | 늘 | 템플릿 | generate.py | look/template.html.j2:64 · fields.json:35 | 묻기 |
| `sum.total` | 총합계 | amount | 1쪽 [852, 593, 907, 604] | 늘 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:45 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [434, 688, 566, 701] | 늘 | 템플릿 | generate.py | look/template.html.j2:70 · fields.json:5 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [325, 721, 652, 742] | 늘 | 템플릿 | generate.py | look/template.html.j2:70 · fields.json:15 | 묻기 |

## 표 `items` (표 과제 table·table_read·table_find·table_qa) — 8열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `items.*.tax_item` | 세목 | text | 1쪽 [101, 343, 193, 354] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:100 | 묻기 |
| `items.*.levied` | 부과연월 | month | 1쪽 [226, 343, 270, 354] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:85 | 묻기 |
| `items.*.kind` | 구분 | text | 1쪽 [316, 343, 357, 354] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:80 | 묻기 |
| `items.*.object` | 과세대상 | text | 1쪽 [389, 343, 474, 354] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:90 | 묻기 |
| `items.*.base` | 과세표준 | text | 1쪽 [622, 343, 627, 354] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:56 · fields.json:70 | 묻기 |
| `items.*.tax` | 세액 | amount | 1쪽 [689, 343, 720, 354] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:95 | 묻기 |
| `items.*.edu` | 지방교육세 | number | 1쪽 [777, 343, 808, 354] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:75 | 묻기 |
| `items.*.total` | 합계 | amount | 1쪽 [876, 343, 907, 354] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:59 · fields.json:105 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [640, 700, 730, 763] | 늘 | 템플릿 | generate.py | fields.json:30 | 묻기 |

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
"지방세 세목별 과세증명서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "1708-3858-0247-7057",
 "남궁예태",
 "850328-2489940",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "2023년 ~ 2024년",
 "은행 제출",
 "주민세(개인분)",
 "2023.08",
 "정기분",
 "세대주 개인분",
 "-",
 "6,000",
 "1,500",
 "7,500",
 "주민세(사업소분)",
 "사업소 부산광역시 해운대구 좌동순환로 237, 7층",
 "50,000",
 "12,500",
 "62,500",
 "재산세(주택)",
 "2023.09",
 "정기분(2/2)",
 "서초구 반포동 661",
 "535,950,000",
 "756,900",
 "151,380",
 "908,280",
 "자동차세",
 "2023.12",
 "2기분",
 "393구9569 승용",
 "1,353cc",
 "66,290",
 "19,880",
 "86,170",
 "2024.06",
 "1기분",
 "61,560",
 "18,460",
 "80,020",
 "2024.07",
 "정기분(1/2)",
 "520,650,000",
 "726,300",
 "145,260",
 "871,560",
 "2024.08",
 "2024.09",
 "2024.12",
 "2,510,910",
 "526,700",
 "3,037,610",
 "2025년 04월 01일",
 "서울특별시 서초구청장"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"주민세(개인분)"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"520,650,000"
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
- taxpayer.name: 성명(법인명)
- taxpayer.rrn: 주민(법인,외국인)등록번호
- taxpayer.address: 주소(영업소)
- period: 과세연도
- purpose: 사용목적
- sum.tax: 세액합계
- sum.edu: 지방교육세합계
- sum.total: 총합계
- issue_date: 발급일
- issuer: 발급기관
```

답:

```json
[{"key": "issue_no", "value": "1708-3858-0247-7057", "bbox_2d": [248, 84, 377, 94], "page": 1},
 {"key": "taxpayer.name", "value": "남궁예태", "bbox_2d": [378, 168, 443, 180], "page": 1},
 {"key": "taxpayer.rrn", "value": "850328-2489940", "bbox_2d": [731, 168, 842, 180], "page": 1},
 {"key": "taxpayer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [378, 199, 899, 227], "page": 1},
 {"key": "period", "value": "2023년 ~ 2024년", "bbox_2d": [378, 246, 493, 258], "page": 1},
 {"key": "purpose", "value": "은행 제출", "bbox_2d": [731, 246, 800, 258], "page": 1},
 {"key": "sum.tax", "value": "2,510,910", "bbox_2d": [665, 593, 720, 604], "page": 1},
 {"key": "sum.edu", "value": "526,700", "bbox_2d": [763, 593, 808, 604], "page": 1},
 {"key": "sum.total", "value": "3,037,610", "bbox_2d": [852, 593, 907, 604], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [434, 688, 566, 701], "page": 1},
 {"key": "issuer", "value": "서울특별시 서초구청장", "bbox_2d": [325, 721, 652, 742], "page": 1}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [640, 700, 730, 763], "page": 1}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[88, 311, 912, 584] 위치의 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 설명)
- tax_item: 세목
- levied: 부과연월
- kind: 구분
- object: 과세대상
- base: 과세표준
- tax: 세액
- edu: 지방교육세
- total: 합계
```

답:

```json
{
 "columns": [
  "tax_item",
  "levied",
  "kind",
  "object",
  "base",
  "tax",
  "edu",
  "total"
 ],
 "rows": [
  [
   "주민세(개인분)",
   "2023.08",
   "정기분",
   "세대주 개인분",
   "-",
   "6,000",
   "1,500",
   "7,500"
  ],
  [
   "주민세(사업소분)",
   "2023.08",
   "정기분",
   "사업소 부산광역시 해운대구 좌동순환로 237, 7층",
   "-",
   "50,000",
   "12,500",
   "62,500"
  ],
  [
   "재산세(주택)",
   "2023.09",
   "정기분(2/2)",
   "서초구 반포동 661",
   "535,950,000",
   "756,900",
   "151,380",
   "908,280"
  ],
  [
   "자동차세",
   "2023.12",
   "2기분",
   "393구9569 승용",
   "1,353cc",
   "66,290",
   "19,880",
   "86,170"
  ],
  [
   "자동차세",
   "2024.06",
   "1기분",
   "393구9569 승용",
   "1,353cc",
   "61,560",
   "18,460",
   "80,020"
  ],
  [
   "재산세(주택)",
   "2024.07",
   "정기분(1/2)",
   "서초구 반포동 661",
   "520,650,000",
   "726,300",
   "145,260",
   "871,560"
  ],
  [
   "주민세(개인분)",
   "2024.08",
   "정기분",
   "세대주 개인분",
   "-",
   "6,000",
   "1,500",
   "7,500"
  ],
  [
   "주민세(사업소분)",
   "2024.08",
   "정기분",
   "사업소 부산광역시 해운대구 좌동순환로 237, 7층",
   "-",
   "50,000",
   "12,500",
   "62,500"
  ],
  [
   "재산세(주택)",
   "2024.09",
   "정기분(2/2)",
   "서초구 반포동 661",
   "520,650,000",
   "726,300",
   "145,260",
   "871,560"
  ],
  [
   "자동차세",
   "2024.12",
   "2기분",
   "393구9569 승용",
   "1,353cc",
   "61,560",
   "18,460",
   "80,020"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    101,
    343,
    907,
    354
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    94,
    363,
    907,
    400
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    108,
    409,
    907,
    420
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    120,
    429,
    907,
    439
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    120,
    448,
    907,
    459
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    108,
    468,
    907,
    479
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    101,
    488,
    907,
    498
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    94,
    507,
    907,
    545
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    108,
    554,
    907,
    564
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    120,
    573,
    907,
    584
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
[{"columns": ["세목", "부과연월", "구분", "과세대상", "과세표준", "세액", "지방교육세", "합계"], "bbox_2d": [88, 311, 912, 584], "page": 1, "n_rows": 10}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[88, 311, 912, 584] 위치의 표를 보고 답하세요. '세액' 칸의 값을 모두 더하면 얼마입니까? 빈 칸은 0 으로 봅니다. (쉼표·단위 없이 숫자만 답하세요)
```

답:

```json
2510910
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[88, 311, 912, 584] 위치의 표를 보고 답하세요. '지방교육세' 칸이 '12,500'인 행은 몇 개입니까? (숫자만 답하세요)
```

답:

```json
2
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa local_tax_assessment --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check local_tax_assessment` → `python -m docgen.formdir card local_tax_assessment` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa local_tax_assessment --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions local_tax_assessment --show` · `python -m docgen.preview local_tax_assessment --out work/local_tax_assessment`
