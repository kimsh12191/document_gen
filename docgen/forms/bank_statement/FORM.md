# 거래내역확인서 (`bank_statement`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card bank_statement · card-hash: a7f2cda96a51 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** finance · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 거래내역확인서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa bank_statement --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 은행 발급 예금 거래내역확인서 (조회기간 거래 목록, 잔액 일관).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/finance.py`, `docgen/docs/income.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 14칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [133, 53, 227, 62] | 늘 | 템플릿 | generate.py | look/template.html.j2:14 · fields.json:25 | 묻기 |
| `holder` | 예금주 | text | 1쪽 [233, 138, 294, 150] | 늘 | 템플릿 | generate.py | look/template.html.j2:16 · fields.json:15 | 묻기 |
| `birth` | 생년월일 | date | 1쪽 [751, 138, 820, 150] | 늘 | 템플릿 | generate.py | look/template.html.j2:16 · fields.json:10 | 묻기 |
| `account_no` | 계좌번호 | account_no | 1쪽 [233, 163, 351, 175] | 늘 | 템플릿 | generate.py | look/template.html.j2:16 · fields.json:5 | 묻기 |
| `product` | 상품명 | text | 1쪽 [751, 163, 812, 175] | 늘 | 템플릿 | generate.py | look/template.html.j2:16 · fields.json:50 | 묻기 |
| `period` | 조회기간 | text | 1쪽 [233, 188, 387, 200] | 늘 | 템플릿 | generate.py | look/template.html.j2:17 · fields.json:45 | 묻기 |
| `opening_balance` | 조회기간전잔액 | amount | 1쪽 [751, 188, 812, 200] | 늘 | 템플릿 | generate.py | look/template.html.j2:17 · fields.json:35 | 묻기 |
| `summary.count` | 거래건수 | text | 1쪽 [269, 545, 295, 556] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:65 | 묻기 |
| `summary.out` | 찾으신금액합계 | number | 1쪽 [542, 545, 596, 556] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:75 | 묻기 |
| `summary.in` | 맡기신금액합계 | number | 1쪽 [653, 545, 707, 556] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:70 | 묻기 |
| `summary.balance` | 최종잔액 | amount | 1쪽 [860, 545, 921, 556] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:60 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [462, 658, 538, 670] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:20 | 묻기 |
| `issuer` | 발급점 | text | 1쪽 [361, 692, 616, 712] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:30 | 묻기 |
| `overdraft_limit` | 대출한도 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:18 · fields.json:40 | 묻기 |

## 표 `rows` (표 과제 table·table_read·table_find·table_qa) — 6열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `rows.*.datetime` | 거래일시 | datetime | 1쪽 [98, 250, 210, 260] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:90 | 묻기 |
| `rows.*.type` | 적요 | text | 1쪽 [259, 250, 305, 260] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:87 | 묻기 |
| `rows.*.memo` | 기재내용 | text | 1쪽 [336, 250, 381, 260] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:100 | 묻기 |
| `rows.*.out` | 찾으신금액 | number | 1쪽 [552, 250, 596, 260] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:105 | 묻기 |
| `rows.*.in` | 맡기신금액 | number | 1쪽 [700, 250, 707, 260] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:95 | 묻기 |
| `rows.*.balance` | 거래후잔액 | amount | 1쪽 [867, 250, 921, 260] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:85 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [604, 669, 694, 733] | 늘 | 템플릿 | generate.py | fields.json:55 | 묻기 |

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
"거래내역확인서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "20250401-142112",
 "남궁예태",
 "1985.03.28",
 "478303-40-826627",
 "저축예금",
 "2025.01.29 ~ 2025.03.31",
 "6,531,023",
 "2025.02.15 21:50:21",
 "CD출금",
 "200,000",
 "0",
 "6,331,023",
 "2025.02.20 14:00:51",
 "자동이체",
 "LGU+통신요금",
 "111,060",
 "6,219,963",
 "2025.02.25 14:29:14",
 "롯데카드",
 "459,840",
 "5,760,123",
 "2025.02.25 19:45:25",
 "펌뱅킹",
 "다온패션급여",
 "3,957,870",
 "9,717,993",
 "2025.02.27 19:37:26",
 "아파트관리비",
 "150,590",
 "9,567,403",
 "2025.02.28 20:32:59",
 "체크카드",
 "GS칼텍스",
 "104,720",
 "9,462,683",
 "2025.03.14 13:40:36",
 "모바일",
 "토스",
 "169,460",
 "9,293,223",
 "2025.03.14 14:25:08",
 "카카오T",
 "22,340",
 "9,270,883",
 "2025.03.21 08:58:00",
 "60,690",
 "9,210,193",
 "2025.03.21 20:56:58",
 "결산",
 "예금결산이자",
 "1,193",
 "9,211,386",
 "2025.03.25 14:37:57",
 "518,040",
 "8,693,346",
 "2025.03.25 17:20:18",
 "다온패션",
 "4,196,230",
 "12,889,576",
 "2025.03.25 20:35:38",
 "245,910",
 "12,643,666",
 "2025.03.31 12:54:30",
 "100,000",
 "12,543,666",
 "14건",
 "2,142,650",
 "8,155,293",
 "2025.04.01",
 "국민은행 센텀지점"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"CD출금"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"0"
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
- holder: 예금주
- birth: 생년월일
- account_no: 계좌번호
- product: 상품명
- period: 조회기간
- opening_balance: 조회기간전잔액
- summary.count: 거래건수
- summary.out: 찾으신금액합계
- summary.in: 맡기신금액합계
- summary.balance: 최종잔액
- issue_date: 발급일
- issuer: 발급점
```

답:

```json
[{"key": "issue_no", "value": "20250401-142112", "bbox_2d": [133, 53, 227, 62], "page": 1},
 {"key": "holder", "value": "남궁예태", "bbox_2d": [233, 138, 294, 150], "page": 1},
 {"key": "birth", "value": "1985.03.28", "bbox_2d": [751, 138, 820, 150], "page": 1},
 {"key": "account_no", "value": "478303-40-826627", "bbox_2d": [233, 163, 351, 175], "page": 1},
 {"key": "product", "value": "저축예금", "bbox_2d": [751, 163, 812, 175], "page": 1},
 {"key": "period", "value": "2025.01.29 ~ 2025.03.31", "bbox_2d": [233, 188, 387, 200], "page": 1},
 {"key": "opening_balance", "value": "6,531,023", "bbox_2d": [751, 188, 812, 200], "page": 1},
 {"key": "summary.count", "value": "14건", "bbox_2d": [269, 545, 295, 556], "page": 1},
 {"key": "summary.out", "value": "2,142,650", "bbox_2d": [542, 545, 596, 556], "page": 1},
 {"key": "summary.in", "value": "8,155,293", "bbox_2d": [653, 545, 707, 556], "page": 1},
 {"key": "summary.balance", "value": "12,543,666", "bbox_2d": [860, 545, 921, 556], "page": 1},
 {"key": "issue_date", "value": "2025.04.01", "bbox_2d": [462, 658, 538, 670], "page": 1},
 {"key": "issuer", "value": "국민은행 센텀지점", "bbox_2d": [361, 692, 616, 712], "page": 1}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [604, 669, 694, 733], "page": 1}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 항목명)
- datetime: 거래일시
- type: 적요
- memo: 기재내용
- out: 찾으신금액
- amount: 대출금액
- in: 맡기신금액
- balance: 거래후잔액
```

답:

```json
{
 "columns": [
  "datetime",
  "type",
  "memo",
  "out",
  "amount",
  "in",
  "balance"
 ],
 "rows": [
  [
   "2025.02.15 21:50:21",
   "CD출금",
   "CD출금",
   "200,000",
   null,
   "0",
   "6,331,023"
  ],
  [
   "2025.02.20 14:00:51",
   "자동이체",
   "LGU+통신요금",
   "111,060",
   null,
   "0",
   "6,219,963"
  ],
  [
   "2025.02.25 14:29:14",
   "자동이체",
   "롯데카드",
   "459,840",
   null,
   "0",
   "5,760,123"
  ],
  [
   "2025.02.25 19:45:25",
   "펌뱅킹",
   "다온패션급여",
   "0",
   null,
   "3,957,870",
   "9,717,993"
  ],
  [
   "2025.02.27 19:37:26",
   "자동이체",
   "아파트관리비",
   "150,590",
   null,
   "0",
   "9,567,403"
  ],
  [
   "2025.02.28 20:32:59",
   "체크카드",
   "GS칼텍스",
   "104,720",
   null,
   "0",
   "9,462,683"
  ],
  [
   "2025.03.14 13:40:36",
   "모바일",
   "토스",
   "169,460",
   null,
   "0",
   "9,293,223"
  ],
  [
   "2025.03.14 14:25:08",
   "체크카드",
   "카카오T",
   "22,340",
   null,
   "0",
   "9,270,883"
  ],
  [
   "2025.03.21 08:58:00",
   "자동이체",
   "LGU+통신요금",
   "60,690",
   null,
   "0",
   "9,210,193"
  ],
  [
   "2025.03.21 20:56:58",
   "결산",
   "예금결산이자",
   "0",
   null,
   "1,193",
   "9,211,386"
  ],
  [
   "2025.03.25 14:37:57",
   "자동이체",
   "롯데카드",
   "518,040",
   null,
   "0",
   "8,693,346"
  ],
  [
   "2025.03.25 17:20:18",
   "펌뱅킹",
   "다온패션",
   "0",
   null,
   "4,196,230",
   "12,889,576"
  ],
  [
   "2025.03.25 20:35:38",
   "자동이체",
   "아파트관리비",
   "245,910",
   null,
   "0",
   "12,643,666"
  ],
  [
   "2025.03.31 12:54:30",
   "CD출금",
   "CD출금",
   "100,000",
   null,
   "0",
   "12,543,666"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    98,
    250,
    921,
    260
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    98,
    271,
    921,
    282
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    98,
    292,
    921,
    303
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    98,
    313,
    921,
    324
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    98,
    334,
    921,
    345
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    98,
    355,
    921,
    366
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    98,
    376,
    921,
    387
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    98,
    397,
    921,
    408
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    98,
    419,
    921,
    429
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    98,
    440,
    921,
    450
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    98,
    461,
    921,
    471
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    98,
    482,
    921,
    492
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    98,
    503,
    921,
    514
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    98,
    524,
    921,
    535
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
[{"columns": ["거래일시", "적요", "기재내용", "찾으신금액", "맡기신금액", "거래후잔액"], "bbox_2d": [72, 224, 928, 535], "page": 1, "n_rows": 14}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '찾으신금액'·'맡기신금액' 열이 있는 표를 보고 답하세요. '맡기신금액' 칸이 '4,196,230'인 행은 몇 개입니까? (숫자만 답하세요)
```

답:

```json
1
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '찾으신금액'·'맡기신금액' 열이 있는 표를 보고 답하세요. 위에서 6번째 행의 '맡기신금액' 값은 무엇입니까? 머리글은 세지 않습니다. (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"0"
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa bank_statement --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check bank_statement` → `python -m docgen.formdir card bank_statement` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa bank_statement --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions bank_statement --show` · `python -m docgen.preview bank_statement --out work/bank_statement`
