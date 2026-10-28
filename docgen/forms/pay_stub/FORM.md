# 급여명세서 (`pay_stub`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card pay_stub · card-hash: 691994b38e1e -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** income · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 급여명세서
- **쓰이는 업무:** 개인 신용대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 임금명세서 (근로기준법 제48조제2항, 시행령 제27조의2 — 고용노동부 임금명세서 표준 예시 구조).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/income.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 28칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `doc_title` | 서식명 | text | 1쪽 [377, 54, 623, 84] | 늘 | 템플릿 | generate.py | look/template.html.j2:17 · fields.json:15 | 묻기 |
| `title_month` | 귀속연월 | text | 1쪽 [449, 91, 551, 105] | 늘 | 템플릿 | generate.py | look/template.html.j2:18 · fields.json:60 | 묻기 |
| `company` | 회사명 | text | 1쪽 [65, 117, 201, 130] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:5 | 묻기 |
| `pay_date` | 지급일 | date | 1쪽 [861, 117, 935, 130] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:50 | 묻기 |
| `customer.name` ← `employee.name` | 성명 | text | 1쪽 [176, 144, 242, 157] | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:35 | 묻기 |
| `customer.birth` ← `employee.birth` | 생년월일 | date | 1쪽 [471, 144, 545, 157] | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:20 | 묻기 |
| `employee.employee_no` | 사번 | text | 1쪽 [785, 144, 835, 157] | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:30 | 묻기 |
| `employee.department` | 부서 | text | 1쪽 [176, 168, 258, 182] | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:25 | 묻기 |
| `employee.position` | 직급 | text | 1쪽 [785, 168, 818, 182] | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:40 | 묻기 |
| `payments.*.name` | 임금항목 | text | 1쪽 [234, 276, 283, 289] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:145 | 묻기 |
| `payments.*.amount` | 지급금액 | amount | 1쪽 [435, 276, 501, 289] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:140 | 묻기 |
| `deductions.*.name` | 공제항목 | text | 1쪽 [573, 276, 639, 289] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:130 | 묻기 |
| `deductions.*.amount` | 공제금액 | amount | 1쪽 [871, 276, 924, 289] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:125 | 묻기 |
| `payments_irregular.*.name` | 임금항목 | text | 1쪽 [218, 425, 300, 438] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:160 | 묻기 |
| `payments_irregular.*.amount` | 지급금액 | amount | 1쪽 [435, 425, 501, 438] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:155 | 묻기 |
| `pay_total` | 지급액계 | amount | 1쪽 [435, 474, 501, 488] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:55 | 묻기 |
| `deduction_total` | 공제액계 | amount | 1쪽 [859, 474, 924, 488] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:10 | 묻기 |
| `net_pay` | 실수령액 | amount | 1쪽 [849, 500, 924, 514] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:45 | 묻기 |
| `work.days` | 근로일수 | number | 1쪽 [105, 554, 120, 566] | 늘 | 템플릿 | generate.py | look/template.html.j2:50 · fields.json:65 | 묻기 |
| `work.hours` | 총근로시간수 | number | 1쪽 [214, 554, 237, 566] | 늘 | 템플릿 | generate.py | look/template.html.j2:50 · fields.json:85 | 묻기 |
| `work.overtime_hours` | 연장근로시간수 | number | 1쪽 [359, 554, 374, 566] | 늘 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:95 | 묻기 |
| `work.night_hours` | 야간근로시간수 | number | 1쪽 [511, 554, 519, 566] | 늘 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:90 | 묻기 |
| `work.holiday_hours` | 휴일근로시간수 | number | 1쪽 [659, 554, 666, 566] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:75 | 묻기 |
| `work.hourly_wage` | 통상시급(원) | amount | 1쪽 [778, 554, 819, 566] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:80 | 묻기 |
| `work.family` | 가족수 | text | 1쪽 [894, 554, 899, 566] | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:70 | 묻기 |
| `calc_methods.*.item` | 구분 | text | 1쪽 [116, 631, 207, 644] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:110 | 묻기 |
| `calc_methods.*.method` | 산출식또는산출방법 | text | 1쪽 [264, 631, 417, 644] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:115 | 묻기 |
| `calc_methods.*.amount` | 금액(원) | amount | 1쪽 [878, 631, 927, 644] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:105 | 묻기 |

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
"급여명세서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "급여명세서",
 "2025년 03월분",
 "주식회사 다온패션",
 "2025.03.25",
 "남궁예태",
 "1985.03.28",
 "S36992",
 "고객지원팀",
 "대리",
 "기본급",
 "3,908,330",
 "국민연금",
 "175,860",
 "연장근로수당",
 "561,000",
 "건강보험",
 "138,550",
 "식대",
 "200,000",
 "장기요양보험",
 "17,940",
 "자가운전보조금",
 "고용보험",
 "75,390",
 "소득세",
 "859,450",
 "지방소득세",
 "85,940",
 "정기상여금",
 "8,777,660",
 "1,353,130",
 "7,424,530",
 "21",
 "188",
 "20",
 "0",
 "18,700",
 "-",
 "20시간 × 18,700원 × 1.5",
 "기본급 × 100% (연 4회 분할 지급)",
 "기준소득월액 3,908,000원 × 4.5%",
 "보수월액 × 3.545%",
 "건강보험료 × 12.95%",
 "과세대상 임금 × 0.9%",
 "근로소득 간이세액표 적용",
 "소득세 × 10%"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"연장근로수당"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"138,550"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- title_month: 귀속연월
- company: 회사명
- pay_date: 지급일
- customer.birth: 생년월일 (고객 생년월일)
- employee.employee_no: 사번
- employee.position: 직급
- payments.0.name: 임금항목 (1행)
- deductions.0.amount: 공제금액 (1행)
- payments.1.name: 임금항목 (2행)
- deductions.1.name: 공제항목 (2행)
- deductions.2.name: 공제항목 (3행)
- deductions.2.amount: 공제금액 (3행)
- payments.3.amount: 지급금액 (4행)
- deductions.3.name: 공제항목 (4행)
- deductions.3.amount: 공제금액 (4행)
- deductions.4.amount: 공제금액 (5행)
- deductions.5.name: 공제항목 (6행)
- payments_irregular.0.name: 임금항목 (1행)
- payments_irregular.0.amount: 지급금액 (1행)
- pay_total: 지급액계
- deduction_total: 공제액계
- work.hours: 총근로시간수
- work.holiday_hours: 휴일근로시간수
- work.hourly_wage: 통상시급(원)
- work.family: 가족수
- calc_methods.0.method: 산출식또는산출방법 (1행)
- calc_methods.0.amount: 금액(원) (1행)
- calc_methods.1.item: 구분 (2행)
- calc_methods.1.method: 산출식또는산출방법 (2행)
- calc_methods.2.method: 산출식또는산출방법 (3행)
- calc_methods.3.item: 구분 (4행)
- calc_methods.3.method: 산출식또는산출방법 (4행)
- calc_methods.3.amount: 금액(원) (4행)
- calc_methods.4.method: 산출식또는산출방법 (5행)
- calc_methods.4.amount: 금액(원) (5행)
- calc_methods.5.item: 구분 (6행)
- calc_methods.6.method: 산출식또는산출방법 (7행)
- calc_methods.7.item: 구분 (8행)
- calc_methods.7.method: 산출식또는산출방법 (8행)
- calc_methods.7.amount: 금액(원) (8행)
```

답:

```json
[{"key": "title_month", "value": "2025년 03월분", "bbox_2d": [449, 91, 551, 105], "page": 1},
 {"key": "company", "value": "주식회사 다온패션", "bbox_2d": [65, 117, 201, 130], "page": 1},
 {"key": "pay_date", "value": "2025.03.25", "bbox_2d": [861, 117, 935, 130], "page": 1},
 {"key": "customer.birth", "value": "1985.03.28", "bbox_2d": [471, 144, 545, 157], "page": 1},
 {"key": "employee.employee_no", "value": "S36992", "bbox_2d": [785, 144, 835, 157], "page": 1},
 {"key": "employee.position", "value": "대리", "bbox_2d": [785, 168, 818, 182], "page": 1},
 {"key": "payments.0.name", "value": "기본급", "bbox_2d": [234, 276, 283, 289], "page": 1},
 {"key": "deductions.0.amount", "value": "175,860", "bbox_2d": [871, 276, 924, 289], "page": 1},
 {"key": "payments.1.name", "value": "연장근로수당", "bbox_2d": [210, 301, 308, 314], "page": 1},
 {"key": "deductions.1.name", "value": "건강보험", "bbox_2d": [573, 301, 639, 314], "page": 1},
 {"key": "deductions.2.name", "value": "장기요양보험", "bbox_2d": [557, 325, 655, 339], "page": 1},
 {"key": "deductions.2.amount", "value": "17,940", "bbox_2d": [879, 325, 924, 339], "page": 1},
 {"key": "payments.3.amount", "value": "200,000", "bbox_2d": [448, 350, 501, 364], "page": 1},
 {"key": "deductions.3.name", "value": "고용보험", "bbox_2d": [573, 350, 639, 364], "page": 1},
 {"key": "deductions.3.amount", "value": "75,390", "bbox_2d": [879, 350, 924, 364], "page": 1},
 {"key": "deductions.4.amount", "value": "859,450", "bbox_2d": [871, 375, 924, 388], "page": 1},
 {"key": "deductions.5.name", "value": "지방소득세", "bbox_2d": [565, 400, 647, 413], "page": 1},
 {"key": "payments_irregular.0.name", "value": "정기상여금", "bbox_2d": [218, 425, 300, 438], "page": 1},
 {"key": "payments_irregular.0.amount", "value": "3,908,330", "bbox_2d": [435, 425, 501, 438], "page": 1},
 {"key": "pay_total", "value": "8,777,660", "bbox_2d": [435, 474, 501, 488], "page": 1},
 {"key": "deduction_total", "value": "1,353,130", "bbox_2d": [859, 474, 924, 488], "page": 1},
 {"key": "work.hours", "value": "188", "bbox_2d": [214, 554, 237, 566], "page": 1},
 {"key": "work.holiday_hours", "value": "0", "bbox_2d": [659, 554, 666, 566], "page": 1},
 {"key": "work.hourly_wage", "value": "18,700", "bbox_2d": [778, 554, 819, 566], "page": 1},
 {"key": "work.family", "value": "-", "bbox_2d": [894, 554, 899, 566], "page": 1},
 {"key": "calc_methods.0.method", "value": "20시간 × 18,700원 × 1.5", "bbox_2d": [264, 631, 417, 644], "page": 1},
 {"key": "calc_methods.0.amount", "value": "561,000", "bbox_2d": [878, 631, 927, 644], "page": 1},
 {"key": "calc_methods.1.item", "value": "정기상여금", "bbox_2d": [124, 653, 199, 665], "page": 1},
 {"key": "calc_methods.1.method", "value": "기본급 × 100% (연 4회 분할 지급)", "bbox_2d": [264, 653, 484, 665], "page": 1},
 {"key": "calc_methods.2.method", "value": "기준소득월액 3,908,000원 × 4.5%", "bbox_2d": [264, 674, 481, 687], "page": 1},
 {"key": "calc_methods.3.item", "value": "건강보험", "bbox_2d": [131, 696, 192, 709], "page": 1},
 {"key": "calc_methods.3.method", "value": "보수월액 × 3.545%", "bbox_2d": [264, 696, 387, 709], "page": 1},
 {"key": "calc_methods.3.amount", "value": "138,550", "bbox_2d": [878, 696, 927, 709], "page": 1},
 {"key": "calc_methods.4.method", "value": "건강보험료 × 12.95%", "bbox_2d": [264, 718, 402, 730], "page": 1},
 {"key": "calc_methods.4.amount", "value": "17,940", "bbox_2d": [885, 718, 927, 730], "page": 1},
 {"key": "calc_methods.5.item", "value": "고용보험", "bbox_2d": [131, 740, 192, 752], "page": 1},
 {"key": "calc_methods.6.method", "value": "근로소득 간이세액표 적용", "bbox_2d": [264, 761, 438, 774], "page": 1},
 {"key": "calc_methods.7.item", "value": "지방소득세", "bbox_2d": [124, 783, 199, 796], "page": 1},
 {"key": "calc_methods.7.method", "value": "소득세 × 10%", "bbox_2d": [264, 783, 353, 796], "page": 1},
 {"key": "calc_methods.7.amount", "value": "85,940", "bbox_2d": [885, 783, 927, 796], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check pay_stub` → `python -m docgen.formdir card pay_stub` (실제 질문→답 확인).

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
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions pay_stub --show` · `python -m docgen.preview pay_stub --out work/pay_stub`
