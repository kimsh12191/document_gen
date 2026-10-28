# 거래내역확인서 (`bank_statement`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card bank_statement · card-hash: 72c069724368 -->

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

## 추출 항목 (정보 추출 kie) — 20칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [133, 53, 227, 62] | 늘 | 템플릿 | generate.py | look/template.html.j2:14 · fields.json:25 | 묻기 |
| `holder` | 예금주 | text | 1쪽 [233, 138, 294, 150] | 늘 | 템플릿 | generate.py | look/template.html.j2:16 · fields.json:15 | 묻기 |
| `birth` | 생년월일 | date | 1쪽 [751, 138, 820, 150] | 늘 | 템플릿 | generate.py | look/template.html.j2:16 · fields.json:10 | 묻기 |
| `account_no` | 계좌번호 | account_no | 1쪽 [233, 163, 351, 175] | 늘 | 템플릿 | generate.py | look/template.html.j2:16 · fields.json:5 | 묻기 |
| `product` | 상품명 | text | 1쪽 [751, 163, 812, 175] | 늘 | 템플릿 | generate.py | look/template.html.j2:16 · fields.json:50 | 묻기 |
| `period` | 조회기간 | text | 1쪽 [233, 188, 387, 200] | 늘 | 템플릿 | generate.py | look/template.html.j2:17 · fields.json:45 | 묻기 |
| `opening_balance` | 조회기간전잔액 | amount | 1쪽 [751, 188, 812, 200] | 늘 | 템플릿 | generate.py | look/template.html.j2:17 · fields.json:35 | 묻기 |
| `rows.*.datetime` | 거래일시 | datetime | 1쪽 [98, 250, 210, 260] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:90 | 묻기 |
| `rows.*.type` | 적요 | text | 1쪽 [259, 250, 305, 260] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:87 | 묻기 |
| `rows.*.memo` | 기재내용 | text | 1쪽 [336, 250, 381, 260] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:100 | 묻기 |
| `rows.*.out` | 찾으신금액 | number | 1쪽 [552, 250, 596, 260] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:105 | 묻기 |
| `rows.*.in` | 맡기신금액 | number | 1쪽 [700, 250, 707, 260] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:95 | 묻기 |
| `rows.*.balance` | 거래후잔액 | amount | 1쪽 [867, 250, 921, 260] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:85 | 묻기 |
| `summary.count` | 거래건수 | text | 1쪽 [269, 545, 295, 556] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:65 | 묻기 |
| `summary.out` | 찾으신금액합계 | number | 1쪽 [542, 545, 596, 556] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:75 | 묻기 |
| `summary.in` | 맡기신금액합계 | number | 1쪽 [653, 545, 707, 556] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:70 | 묻기 |
| `summary.balance` | 최종잔액 | amount | 1쪽 [860, 545, 921, 556] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:60 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [462, 658, 538, 670] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:20 | 묻기 |
| `issuer` | 발급점 | text | 1쪽 [361, 692, 616, 712] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:30 | 묻기 |
| `overdraft_limit` | 대출한도 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:18 · fields.json:40 | 묻기 |

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
- birth: 생년월일
- rows.0.datetime: 거래일시 (1행)
- rows.0.in: 맡기신금액 (1행)
- rows.1.type: 적요 (2행)
- rows.1.memo: 기재내용 (2행)
- rows.2.in: 맡기신금액 (3행)
- rows.2.balance: 거래후잔액 (3행)
- rows.3.type: 적요 (4행)
- rows.3.memo: 기재내용 (4행)
- rows.3.in: 맡기신금액 (4행)
- rows.3.balance: 거래후잔액 (4행)
- rows.4.datetime: 거래일시 (5행)
- rows.4.in: 맡기신금액 (5행)
- rows.5.datetime: 거래일시 (6행)
- rows.5.memo: 기재내용 (6행)
- rows.5.in: 맡기신금액 (6행)
- rows.6.memo: 기재내용 (7행)
- rows.6.in: 맡기신금액 (7행)
- rows.7.out: 찾으신금액 (8행)
- rows.8.type: 적요 (9행)
- rows.8.memo: 기재내용 (9행)
- rows.8.in: 맡기신금액 (9행)
- rows.8.balance: 거래후잔액 (9행)
- rows.9.type: 적요 (10행)
- rows.9.in: 맡기신금액 (10행)
- rows.9.balance: 거래후잔액 (10행)
- rows.10.memo: 기재내용 (11행)
- rows.10.out: 찾으신금액 (11행)
- rows.10.in: 맡기신금액 (11행)
- rows.10.balance: 거래후잔액 (11행)
- rows.11.datetime: 거래일시 (12행)
- rows.11.type: 적요 (12행)
- rows.11.in: 맡기신금액 (12행)
- rows.12.datetime: 거래일시 (13행)
- rows.12.type: 적요 (13행)
- rows.13.type: 적요 (14행)
- rows.13.out: 찾으신금액 (14행)
- rows.13.in: 맡기신금액 (14행)
- summary.count: 거래건수
- summary.in: 맡기신금액합계
```

답:

```json
[{"key": "birth", "value": "1985.03.28", "bbox_2d": [751, 138, 820, 150], "page": 1},
 {"key": "rows.0.datetime", "value": "2025.02.15 21:50:21", "bbox_2d": [98, 250, 210, 260], "page": 1},
 {"key": "rows.0.in", "value": "0", "bbox_2d": [700, 250, 707, 260], "page": 1},
 {"key": "rows.1.type", "value": "자동이체", "bbox_2d": [255, 271, 309, 282], "page": 1},
 {"key": "rows.1.memo", "value": "LGU+통신요금", "bbox_2d": [336, 271, 425, 282], "page": 1},
 {"key": "rows.2.in", "value": "0", "bbox_2d": [700, 292, 707, 303], "page": 1},
 {"key": "rows.2.balance", "value": "5,760,123", "bbox_2d": [867, 292, 921, 303], "page": 1},
 {"key": "rows.3.type", "value": "펌뱅킹", "bbox_2d": [262, 313, 302, 324], "page": 1},
 {"key": "rows.3.memo", "value": "다온패션급여", "bbox_2d": [336, 313, 417, 324], "page": 1},
 {"key": "rows.3.in", "value": "3,957,870", "bbox_2d": [653, 313, 707, 324], "page": 1},
 {"key": "rows.3.balance", "value": "9,717,993", "bbox_2d": [867, 313, 921, 324], "page": 1},
 {"key": "rows.4.datetime", "value": "2025.02.27 19:37:26", "bbox_2d": [98, 334, 210, 345], "page": 1},
 {"key": "rows.4.in", "value": "0", "bbox_2d": [700, 334, 707, 345], "page": 1},
 {"key": "rows.5.datetime", "value": "2025.02.28 20:32:59", "bbox_2d": [98, 355, 210, 366], "page": 1},
 {"key": "rows.5.memo", "value": "GS칼텍스", "bbox_2d": [336, 355, 393, 366], "page": 1},
 {"key": "rows.5.in", "value": "0", "bbox_2d": [700, 355, 707, 366], "page": 1},
 {"key": "rows.6.memo", "value": "토스", "bbox_2d": [336, 376, 363, 387], "page": 1},
 {"key": "rows.6.in", "value": "0", "bbox_2d": [700, 376, 707, 387], "page": 1},
 {"key": "rows.7.out", "value": "22,340", "bbox_2d": [559, 397, 596, 408], "page": 1},
 {"key": "rows.8.type", "value": "자동이체", "bbox_2d": [255, 419, 309, 429], "page": 1},
 {"key": "rows.8.memo", "value": "LGU+통신요금", "bbox_2d": [336, 419, 425, 429], "page": 1},
 {"key": "rows.8.in", "value": "0", "bbox_2d": [700, 419, 707, 429], "page": 1},
 {"key": "rows.8.balance", "value": "9,210,193", "bbox_2d": [867, 419, 921, 429], "page": 1},
 {"key": "rows.9.type", "value": "결산", "bbox_2d": [269, 440, 295, 450], "page": 1},
 {"key": "rows.9.in", "value": "1,193", "bbox_2d": [677, 440, 707, 450], "page": 1},
 {"key": "rows.9.balance", "value": "9,211,386", "bbox_2d": [867, 440, 921, 450], "page": 1},
 {"key": "rows.10.memo", "value": "롯데카드", "bbox_2d": [336, 461, 390, 471], "page": 1},
 {"key": "rows.10.out", "value": "518,040", "bbox_2d": [552, 461, 596, 471], "page": 1},
 {"key": "rows.10.in", "value": "0", "bbox_2d": [700, 461, 707, 471], "page": 1},
 {"key": "rows.10.balance", "value": "8,693,346", "bbox_2d": [867, 461, 921, 471], "page": 1},
 {"key": "rows.11.datetime", "value": "2025.03.25 17:20:18", "bbox_2d": [98, 482, 210, 492], "page": 1},
 {"key": "rows.11.type", "value": "펌뱅킹", "bbox_2d": [262, 482, 302, 492], "page": 1},
 {"key": "rows.11.in", "value": "4,196,230", "bbox_2d": [653, 482, 707, 492], "page": 1},
 {"key": "rows.12.datetime", "value": "2025.03.25 20:35:38", "bbox_2d": [98, 503, 210, 514], "page": 1},
 {"key": "rows.12.type", "value": "자동이체", "bbox_2d": [255, 503, 309, 514], "page": 1},
 {"key": "rows.13.type", "value": "CD출금", "bbox_2d": [259, 524, 305, 535], "page": 1},
 {"key": "rows.13.out", "value": "100,000", "bbox_2d": [552, 524, 596, 535], "page": 1},
 {"key": "rows.13.in", "value": "0", "bbox_2d": [700, 524, 707, 535], "page": 1},
 {"key": "summary.count", "value": "14건", "bbox_2d": [269, 545, 295, 556], "page": 1},
 {"key": "summary.in", "value": "8,155,293", "bbox_2d": [653, 545, 707, 556], "page": 1}]
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
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions bank_statement --show` · `python -m docgen.preview bank_statement --out work/bank_statement`
