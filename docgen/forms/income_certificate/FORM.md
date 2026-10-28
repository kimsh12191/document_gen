# 소득금액증명원 (`income_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card income_certificate · card-hash: b79d255ce179 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** income · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 소득금액증명원 (다른 이름: 소득금액증명)
- **쓰이는 업무:** 개인 신용대출, 주택담보대출, 전세자금대출, 개인사업자 대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 국세청(홈택스) 발급 소득금액증명.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/income.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 19칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [156, 60, 280, 72] | 늘 | 템플릿 | generate.py | look/template.html.j2:13 · fields.json:10 | 묻기 |
| `customer.name` ← `taxpayer.name` | 성명(대표자) | text | 1쪽 [318, 144, 385, 157] | 늘 | 템플릿 | generate.py | look/template.html.j2:18 · fields.json:45 | 묻기 |
| `customer.rrn` ← `taxpayer.rrn` | 주민등록번호 | rrn | 1쪽 [712, 144, 826, 157] | 늘 | 템플릿 | generate.py | look/template.html.j2:18 · fields.json:50 | 묻기 |
| `customer.address` ← `taxpayer.address` | 주소(사업장소재지) | text | 1쪽 [318, 176, 894, 189] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:40 | 묻기 |
| `period` | 증명기간 | text | 1쪽 [318, 241, 436, 254] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:20 | 묻기 |
| `filing_rows.*.year` | 귀속연도 | number | 1쪽 [120, 342, 154, 355] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:75 | 묻기 |
| `filing_rows.*.income_type` | 소득구분 | text | 1쪽 [229, 342, 262, 355] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:65 | 묻기 |
| `filing_rows.*.revenue` | 수입금액 | amount | 1쪽 [687, 342, 762, 355] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:70 | 묻기 |
| `filing_rows.*.income` | 소득금액 | amount | 1쪽 [829, 342, 904, 355] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:60 | 묻기 |
| `rows.*.year` | 귀속연도 | number | 1쪽 [112, 637, 146, 650] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:110 | 묻기 |
| `rows.*.income_type` | 소득구분 | text | 1쪽 [206, 637, 239, 650] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:90 | 묻기 |
| `rows.*.payer` | 법인명(상호) | text | 1쪽 [301, 637, 439, 650] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:50 · fields.json:95 | 묻기 |
| `rows.*.payer_biz_no` | 사업자등록번호 | biz_no | 1쪽 [494, 637, 589, 650] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:100 | 묻기 |
| `rows.*.amount` | 소득금액(과세대상급여액) | amount | 1쪽 [692, 637, 767, 650] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:85 | 묻기 |
| `rows.*.tax` | 총결정세액 | amount | 1쪽 [837, 637, 904, 650] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:105 | 묻기 |
| `purpose` | 용도 | text | 1쪽 [246, 739, 367, 753] | 늘 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:25 | 묻기 |
| `submit_to` | 제출처 | text | 1쪽 [663, 739, 730, 753] | 늘 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:35 | 묻기 |
| `issue_date` | 발급일 | date | 2쪽 [441, 142, 559, 155] | 늘 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:5 | 묻기 |
| `issuer` | 발급기관 | text | 2쪽 [400, 177, 577, 199] | 늘 | 템플릿 | generate.py | look/template.html.j2:68 · fields.json:15 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 2쪽 [565, 155, 655, 218] | 늘 | 템플릿 | generate.py | fields.json:30 | 묻기 |

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
"소득금액증명원"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2275-478-7266-401",
 "남궁예태",
 "850328-2489940",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "2022년 ~ 2024년",
 "2024",
 "근로",
 "47,550,000",
 "35,422,500",
 "사업",
 "10,026,080",
 "3,599,360",
 "2023",
 "45,860,000",
 "33,817,000",
 "기타",
 "1,614,560",
 "645,820",
 "2022",
 "44,230,000",
 "32,345,500",
 "19,852,620",
 "7,127,090",
 "주식회사 다온패션",
 "123-88-81212",
 "2,132,740",
 "2,203,990",
 "1,980,500",
 "금융기관 제출용",
 "국민은행",
 "2025년 4월 1일",
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
"2024"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"주식회사 다온패션"
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
- customer.name: 성명(대표자) (고객 성명)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- customer.address: 주소(사업장소재지) (고객 주소)
- period: 증명기간
- filing_rows.0.year: 귀속연도 (1행)
- filing_rows.0.revenue: 수입금액 (1행)
- filing_rows.0.income: 소득금액 (1행)
- filing_rows.1.year: 귀속연도 (2행)
- filing_rows.1.revenue: 수입금액 (2행)
- filing_rows.1.income: 소득금액 (2행)
- filing_rows.2.year: 귀속연도 (3행)
- filing_rows.2.income_type: 소득구분 (3행)
- filing_rows.2.revenue: 수입금액 (3행)
- filing_rows.2.income: 소득금액 (3행)
- filing_rows.3.year: 귀속연도 (4행)
- filing_rows.3.income_type: 소득구분 (4행)
- filing_rows.4.year: 귀속연도 (5행)
- filing_rows.4.revenue: 수입금액 (5행)
- filing_rows.4.income: 소득금액 (5행)
- filing_rows.5.year: 귀속연도 (6행)
- filing_rows.5.income_type: 소득구분 (6행)
- rows.0.year: 귀속연도 (1행)
- rows.0.payer: 법인명(상호) (1행)
- rows.0.payer_biz_no: 사업자등록번호 (1행)
- rows.0.amount: 소득금액(과세대상급여액) (1행)
- rows.0.tax: 총결정세액 (1행)
- rows.1.income_type: 소득구분 (2행)
- rows.1.payer: 법인명(상호) (2행)
- rows.1.payer_biz_no: 사업자등록번호 (2행)
- rows.1.amount: 소득금액(과세대상급여액) (2행)
- rows.1.tax: 총결정세액 (2행)
- rows.2.year: 귀속연도 (3행)
- rows.2.income_type: 소득구분 (3행)
- rows.2.payer: 법인명(상호) (3행)
- rows.2.payer_biz_no: 사업자등록번호 (3행)
- rows.2.tax: 총결정세액 (3행)
- purpose: 용도
- submit_to: 제출처
- issuer: 발급기관
```

답:

```json
[{"key": "issue_no", "value": "2275-478-7266-401", "bbox_2d": [156, 60, 280, 72], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [318, 144, 385, 157], "page": 1},
 {"key": "customer.rrn", "value": "850328-2489940", "bbox_2d": [712, 144, 826, 157], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [318, 176, 894, 189], "page": 1},
 {"key": "period", "value": "2022년 ~ 2024년", "bbox_2d": [318, 241, 436, 254], "page": 1},
 {"key": "filing_rows.0.year", "value": "2024", "bbox_2d": [120, 342, 154, 355], "page": 1},
 {"key": "filing_rows.0.revenue", "value": "47,550,000", "bbox_2d": [687, 342, 762, 355], "page": 1},
 {"key": "filing_rows.0.income", "value": "35,422,500", "bbox_2d": [829, 342, 904, 355], "page": 1},
 {"key": "filing_rows.1.year", "value": "2024", "bbox_2d": [120, 374, 154, 388], "page": 1},
 {"key": "filing_rows.1.revenue", "value": "10,026,080", "bbox_2d": [687, 374, 762, 388], "page": 1},
 {"key": "filing_rows.1.income", "value": "3,599,360", "bbox_2d": [837, 374, 904, 388], "page": 1},
 {"key": "filing_rows.2.year", "value": "2023", "bbox_2d": [120, 406, 154, 420], "page": 1},
 {"key": "filing_rows.2.income_type", "value": "근로", "bbox_2d": [229, 406, 262, 420], "page": 1},
 {"key": "filing_rows.2.revenue", "value": "45,860,000", "bbox_2d": [687, 406, 762, 420], "page": 1},
 {"key": "filing_rows.2.income", "value": "33,817,000", "bbox_2d": [829, 406, 904, 420], "page": 1},
 {"key": "filing_rows.3.year", "value": "2023", "bbox_2d": [120, 439, 154, 452], "page": 1},
 {"key": "filing_rows.3.income_type", "value": "기타", "bbox_2d": [229, 439, 262, 452], "page": 1},
 {"key": "filing_rows.4.year", "value": "2022", "bbox_2d": [120, 471, 154, 484], "page": 1},
 {"key": "filing_rows.4.revenue", "value": "44,230,000", "bbox_2d": [687, 471, 762, 484], "page": 1},
 {"key": "filing_rows.4.income", "value": "32,345,500", "bbox_2d": [829, 471, 904, 484], "page": 1},
 {"key": "filing_rows.5.year", "value": "2022", "bbox_2d": [120, 503, 154, 516], "page": 1},
 {"key": "filing_rows.5.income_type", "value": "사업", "bbox_2d": [229, 503, 262, 516], "page": 1},
 {"key": "rows.0.year", "value": "2024", "bbox_2d": [112, 637, 146, 650], "page": 1},
 {"key": "rows.0.payer", "value": "주식회사 다온패션", "bbox_2d": [301, 637, 439, 650], "page": 1},
 {"key": "rows.0.payer_biz_no", "value": "123-88-81212", "bbox_2d": [494, 637, 589, 650], "page": 1},
 {"key": "rows.0.amount", "value": "47,550,000", "bbox_2d": [692, 637, 767, 650], "page": 1},
 {"key": "rows.0.tax", "value": "2,132,740", "bbox_2d": [837, 637, 904, 650], "page": 1},
 {"key": "rows.1.income_type", "value": "근로", "bbox_2d": [206, 669, 239, 682], "page": 1},
 {"key": "rows.1.payer", "value": "주식회사 다온패션", "bbox_2d": [301, 669, 439, 682], "page": 1},
 {"key": "rows.1.payer_biz_no", "value": "123-88-81212", "bbox_2d": [494, 669, 589, 682], "page": 1},
 {"key": "rows.1.amount", "value": "45,860,000", "bbox_2d": [692, 669, 767, 682], "page": 1},
 {"key": "rows.1.tax", "value": "2,203,990", "bbox_2d": [837, 669, 904, 682], "page": 1},
 {"key": "rows.2.year", "value": "2022", "bbox_2d": [112, 701, 146, 714], "page": 1},
 {"key": "rows.2.income_type", "value": "근로", "bbox_2d": [206, 701, 239, 714], "page": 1},
 {"key": "rows.2.payer", "value": "주식회사 다온패션", "bbox_2d": [301, 701, 439, 714], "page": 1},
 {"key": "rows.2.payer_biz_no", "value": "123-88-81212", "bbox_2d": [494, 701, 589, 714], "page": 1},
 {"key": "rows.2.tax", "value": "1,980,500", "bbox_2d": [837, 701, 904, 714], "page": 1},
 {"key": "purpose", "value": "금융기관 제출용", "bbox_2d": [246, 739, 367, 753], "page": 1},
 {"key": "submit_to", "value": "국민은행", "bbox_2d": [663, 739, 730, 753], "page": 1},
 {"key": "issuer", "value": "반포세무서장", "bbox_2d": [400, 177, 577, 199], "page": 2}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [565, 155, 655, 218], "page": 2}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check income_certificate` → `python -m docgen.formdir card income_certificate` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions income_certificate --show` · `python -m docgen.preview income_certificate --out work/income_certificate`
