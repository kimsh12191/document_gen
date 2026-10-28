# 주주명부 (`shareholder_registry`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card shareholder_registry · card-hash: 087667189de5 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** corporate · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 주주명부
- **쓰이는 업무:** 법인 여신
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 법인 주주명부 (대표이사 확인 날인).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/corporate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 23칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `base_date` | 기준일 | date | 1쪽 [809, 91, 932, 105] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:5 | 묻기 |
| `corp.name` ← `company_name` | 회사명 | text | 1쪽 [214, 122, 323, 135] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:30 | 묻기 |
| `corp_reg_no` | 법인등록번호 | corp_reg_no | 1쪽 [648, 122, 759, 135] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:35 | 묻기 |
| `biz_no` | 사업자등록번호 | biz_no | 1쪽 [214, 149, 307, 163] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:10 | 묻기 |
| `total_shares` | 발행주식총수 | text | 1쪽 [648, 149, 710, 163] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:70 | 묻기 |
| `head_office` | 본점소재지 | text | 1쪽 [214, 177, 518, 190] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:40 | 묻기 |
| `par_value` | 1주의금액 | amount | 1쪽 [214, 204, 267, 217] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:45 | 묻기 |
| `capital` | 자본금 | amount | 1쪽 [648, 204, 746, 217] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:15 | 묻기 |
| `shareholders.*.no` | 번호 | number | 1쪽 [82, 285, 89, 295] (1행) | 늘 | 템플릿 | generate.py | fields.json:105 | 묻기 |
| `shareholders.*.name` | 주주명 | text | 1쪽 [119, 285, 174, 295] (1행) | 늘 | 템플릿 | generate.py | fields.json:100 | 묻기 |
| `shareholders.*.id_no` | 주민등록번호(사업자번호) | rrn | 1쪽 [199, 285, 294, 295] (1행) | 늘 | 템플릿 | generate.py | fields.json:95 | 묻기 |
| `shareholders.*.address` | 주소 | text | 1쪽 [312, 279, 478, 301] (1행) | 늘 | 템플릿 | generate.py | fields.json:85 | 묻기 |
| `shareholders.*.share_type` | 주식종류 | text | 1쪽 [505, 285, 547, 295] (1행) | 늘 | 템플릿 | generate.py | fields.json:120 | 묻기 |
| `shareholders.*.shares` | 소유주식수 | number | 1쪽 [580, 285, 618, 295] (1행) | 늘 | 템플릿 | generate.py | fields.json:125 | 묻기 |
| `shareholders.*.amount` | 금액 | amount | 1쪽 [645, 285, 714, 295] (1행) | 늘 | 템플릿 | generate.py | fields.json:90 | 묻기 |
| `shareholders.*.ratio` | 지분율 | percent | 1쪽 [732, 285, 775, 295] (1행) | 늘 | 템플릿 | generate.py | fields.json:115 | 묻기 |
| `shareholders.*.acquired` | 취득일 | date | 1쪽 [792, 285, 854, 295] (1행) | 늘 | 템플릿 | generate.py | fields.json:80 | 묻기 |
| `shareholders.*.note` | 비고 | text | 1쪽 [874, 285, 929, 295] (1행) | 늘 | 템플릿 | generate.py | fields.json:110 | 묻기 |
| `sum_shares` | 합계주식수 | amount | 1쪽 [580, 440, 618, 451] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:65 | 묻기 |
| `sum_amount` | 합계금액 | amount | 1쪽 [645, 440, 714, 451] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:55 | 묻기 |
| `sum_ratio` | 합계지분율 | percent | 1쪽 [723, 440, 775, 451] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:60 | 묻기 |
| `certify_date` | 확인일 | date | 1쪽 [442, 535, 558, 549] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:25 | 묻기 |
| `ceo` | 대표이사 | text | 1쪽 [468, 609, 547, 624] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:20 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.corp` | 법인인감 | seal | 1쪽 [562, 575, 693, 668] | 늘 | 템플릿 | generate.py | fields.json:50 | 묻기 |

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
"주주명부"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2025년 03월 26일",
 "(주)미래케미칼",
 "200112-7951835",
 "702-81-38348",
 "60,000주",
 "제주특별자치도 제주시 첨단로 381-19, 2층",
 "5,000원",
 "300,000,000원",
 "1",
 "남궁예태",
 "850328-2******",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "보통주",
 "40,061",
 "200,305,000",
 "66.77%",
 "2020.06.15",
 "대표이사",
 "2",
 "노도수",
 "830120-*******",
 "충청남도 천안시 서북구 봉정로 505-12, 114동 2201호",
 "8,278",
 "41,390,000",
 "13.80%",
 "사내이사",
 "3",
 "원승호",
 "671016-1******",
 "경기도 성남시 분당구 분당로 72-27, 117동 1403호",
 "11,661",
 "58,305,000",
 "19.43%",
 "2023.12.11",
 "60,000",
 "300,000,000",
 "100.00%",
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
"200112-7951835"
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
- base_date: 기준일
- corp.name: 회사명 (법인·사업자 상호)
- corp_reg_no: 법인등록번호
- biz_no: 사업자등록번호
- total_shares: 발행주식총수
- par_value: 1주의금액
- capital: 자본금
- shareholders.0.no: 번호 (1행)
- shareholders.0.name: 주주명 (1행)
- shareholders.0.id_no: 주민등록번호(사업자번호) (1행)
- shareholders.0.address: 주소 (1행)
- shareholders.0.share_type: 주식종류 (1행)
- shareholders.0.shares: 소유주식수 (1행)
- shareholders.0.amount: 금액 (1행)
- shareholders.0.acquired: 취득일 (1행)
- shareholders.0.note: 비고 (1행)
- shareholders.1.no: 번호 (2행)
- shareholders.1.id_no: 주민등록번호(사업자번호) (2행)
- shareholders.1.address: 주소 (2행)
- shareholders.1.share_type: 주식종류 (2행)
- shareholders.1.shares: 소유주식수 (2행)
- shareholders.1.amount: 금액 (2행)
- shareholders.1.ratio: 지분율 (2행)
- shareholders.1.acquired: 취득일 (2행)
- shareholders.1.note: 비고 (2행)
- shareholders.2.no: 번호 (3행)
- shareholders.2.name: 주주명 (3행)
- shareholders.2.id_no: 주민등록번호(사업자번호) (3행)
- shareholders.2.address: 주소 (3행)
- shareholders.2.share_type: 주식종류 (3행)
- shareholders.2.shares: 소유주식수 (3행)
- shareholders.2.amount: 금액 (3행)
- shareholders.2.ratio: 지분율 (3행)
- shareholders.2.acquired: 취득일 (3행)
- shareholders.2.note: 비고 (3행)
- sum_shares: 합계주식수
- sum_amount: 합계금액
- sum_ratio: 합계지분율
- certify_date: 확인일
- ceo: 대표이사
```

답:

```json
[{"key": "base_date", "value": "2025년 03월 26일", "bbox_2d": [809, 91, 932, 105], "page": 1},
 {"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [214, 122, 323, 135], "page": 1},
 {"key": "corp_reg_no", "value": "200112-7951835", "bbox_2d": [648, 122, 759, 135], "page": 1},
 {"key": "biz_no", "value": "702-81-38348", "bbox_2d": [214, 149, 307, 163], "page": 1},
 {"key": "total_shares", "value": "60,000주", "bbox_2d": [648, 149, 710, 163], "page": 1},
 {"key": "par_value", "value": "5,000원", "bbox_2d": [214, 204, 267, 217], "page": 1},
 {"key": "capital", "value": "300,000,000원", "bbox_2d": [648, 204, 746, 217], "page": 1},
 {"key": "shareholders.0.no", "value": "1", "bbox_2d": [82, 285, 89, 295], "page": 1},
 {"key": "shareholders.0.name", "value": "남궁예태", "bbox_2d": [119, 285, 174, 295], "page": 1},
 {"key": "shareholders.0.id_no", "value": "850328-2******", "bbox_2d": [199, 285, 294, 295], "page": 1},
 {"key": "shareholders.0.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [312, 279, 478, 301], "page": 1},
 {"key": "shareholders.0.share_type", "value": "보통주", "bbox_2d": [505, 285, 547, 295], "page": 1},
 {"key": "shareholders.0.shares", "value": "40,061", "bbox_2d": [580, 285, 618, 295], "page": 1},
 {"key": "shareholders.0.amount", "value": "200,305,000", "bbox_2d": [645, 285, 714, 295], "page": 1},
 {"key": "shareholders.0.acquired", "value": "2020.06.15", "bbox_2d": [792, 285, 854, 295], "page": 1},
 {"key": "shareholders.0.note", "value": "대표이사", "bbox_2d": [874, 285, 929, 295], "page": 1},
 {"key": "shareholders.1.no", "value": "2", "bbox_2d": [82, 317, 89, 327], "page": 1},
 {"key": "shareholders.1.id_no", "value": "830120-*******", "bbox_2d": [199, 317, 294, 327], "page": 1},
 {"key": "shareholders.1.address", "value": "충청남도 천안시 서북구 봉정로 505-12, 114동 2201호", "bbox_2d": [312, 311, 494, 333], "page": 1},
 {"key": "shareholders.1.share_type", "value": "보통주", "bbox_2d": [505, 317, 547, 327], "page": 1},
 {"key": "shareholders.1.shares", "value": "8,278", "bbox_2d": [587, 317, 618, 327], "page": 1},
 {"key": "shareholders.1.amount", "value": "41,390,000", "bbox_2d": [652, 317, 714, 327], "page": 1},
 {"key": "shareholders.1.ratio", "value": "13.80%", "bbox_2d": [732, 317, 775, 327], "page": 1},
 {"key": "shareholders.1.acquired", "value": "2020.06.15", "bbox_2d": [792, 317, 854, 327], "page": 1},
 {"key": "shareholders.1.note", "value": "사내이사", "bbox_2d": [874, 317, 929, 327], "page": 1},
 {"key": "shareholders.2.no", "value": "3", "bbox_2d": [82, 349, 89, 360], "page": 1},
 {"key": "shareholders.2.name", "value": "원승호", "bbox_2d": [126, 349, 167, 360], "page": 1},
 {"key": "shareholders.2.id_no", "value": "671016-1******", "bbox_2d": [199, 349, 294, 360], "page": 1},
 {"key": "shareholders.2.address", "value": "경기도 성남시 분당구 분당로 72-27, 117동 1403호", "bbox_2d": [312, 344, 481, 366], "page": 1},
 {"key": "shareholders.2.share_type", "value": "보통주", "bbox_2d": [505, 349, 547, 360], "page": 1},
 {"key": "shareholders.2.shares", "value": "11,661", "bbox_2d": [580, 349, 618, 360], "page": 1},
 {"key": "shareholders.2.amount", "value": "58,305,000", "bbox_2d": [652, 349, 714, 360], "page": 1},
 {"key": "shareholders.2.ratio", "value": "19.43%", "bbox_2d": [732, 349, 775, 360], "page": 1},
 {"key": "shareholders.2.acquired", "value": "2023.12.11", "bbox_2d": [792, 349, 854, 360], "page": 1},
 {"key": "shareholders.2.note", "value": "사내이사", "bbox_2d": [874, 349, 929, 360], "page": 1},
 {"key": "sum_shares", "value": "60,000", "bbox_2d": [580, 440, 618, 451], "page": 1},
 {"key": "sum_amount", "value": "300,000,000", "bbox_2d": [645, 440, 714, 451], "page": 1},
 {"key": "sum_ratio", "value": "100.00%", "bbox_2d": [723, 440, 775, 451], "page": 1},
 {"key": "certify_date", "value": "2025년 4월 1일", "bbox_2d": [442, 535, 558, 549], "page": 1},
 {"key": "ceo", "value": "남궁예태", "bbox_2d": [468, 609, 547, 624], "page": 1}]
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
- seal.corp: 법인인감 (법인·사업자 도장, 도장)
```

답:

```json
[{"key": "seal.corp", "value": true, "bbox_2d": [562, 575, 693, 668], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check shareholder_registry` → `python -m docgen.formdir card shareholder_registry` (실제 질문→답 확인).

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
| 답 모양 | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions shareholder_registry --show` · `python -m docgen.preview shareholder_registry --out work/shareholder_registry`
