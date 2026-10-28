# 부가가치세 과세표준증명 (`vat_tax_base_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card vat_tax_base_certificate · card-hash: 02a6ea39c9c6 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** tax · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 부가가치세 과세표준증명
- **쓰이는 업무:** 개인사업자 대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 홈택스 발급 부가가치세 과세표준증명 (개인사업자).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/business.py`, `docgen/docs/tax.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 18칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [72, 110, 191, 123] | 늘 | 템플릿 | generate.py | look/template.html.j2:24 · fields.json:10 | 묻기 |
| `customer.name` ← `taxpayer.name` | 성명(대표자) | text | 1쪽 [283, 142, 347, 155] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:50 | 묻기 |
| `customer.rrn` ← `taxpayer.rrn` | 주민(법인)등록번호 | rrn | 1쪽 [729, 142, 839, 155] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:55 | 묻기 |
| `customer.trade_name` ← `taxpayer.trade_name` | 상호(법인명) | text | 1쪽 [283, 172, 347, 184] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:60 | 묻기 |
| `customer.biz_no` ← `taxpayer.biz_no` | 사업자등록번호 | biz_no | 1쪽 [729, 172, 820, 184] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:40 | 묻기 |
| `customer.address` ← `taxpayer.address` | 사업장소재지 | text | 1쪽 [283, 202, 696, 214] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:30 | 묻기 |
| `taxpayer.biz_type` | 업태 | text | 1쪽 [283, 231, 347, 244] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:45 | 묻기 |
| `taxpayer.biz_item` | 종목 | text | 1쪽 [729, 231, 809, 244] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:35 | 묻기 |
| `items.*.period` | 과세기간 | text | 1쪽 [96, 345, 245, 358] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:95 | 묻기 |
| `items.*.kind` | 신고구분 | text | 1쪽 [293, 345, 352, 358] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:90 | 묻기 |
| `items.*.filed` | 신고일 | date | 1쪽 [384, 345, 451, 358] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:85 | 묻기 |
| `items.*.base_total` | 매출과세표준계 | amount | 1쪽 [507, 345, 581, 358] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:80 | 묻기 |
| `items.*.base_taxable` | 과세분 | amount | 1쪽 [620, 345, 694, 358] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:75 | 묻기 |
| `items.*.base_exempt` | 면세수입금액 | amount | 1쪽 [799, 345, 806, 358] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:56 · fields.json:70 | 묻기 |
| `items.*.tax` | 납부할세액(환급받을세액) | amount | 1쪽 [862, 345, 928, 358] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:100 | 묻기 |
| `purpose` | 사용목적 | text | 1쪽 [283, 594, 384, 606] | 늘 | 템플릿 | generate.py | look/template.html.j2:63 · fields.json:20 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [434, 688, 566, 701] | 늘 | 템플릿 | generate.py | look/template.html.j2:67 · fields.json:5 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [379, 724, 599, 745] | 늘 | 템플릿 | generate.py | look/template.html.j2:67 · fields.json:15 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [587, 700, 676, 764] | 늘 | 템플릿 | generate.py | fields.json:25 | 묻기 |

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
"부가가치세 과세표준증명"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "7272-950-4839-229",
 "남궁예태",
 "850328-2******",
 "새한커피",
 "133-64-53148",
 "부산광역시 해운대구 좌동순환로 237, 7층 (우동, 케이타워)",
 "음식점업",
 "커피전문점",
 "2021.01.01 ~ 2021.06.30",
 "정기확정",
 "2021.07.07",
 "242,011,560",
 "0",
 "11,477,360",
 "2021.07.01 ~ 2021.12.31",
 "2022.01.18",
 "291,521,570",
 "14,150,540",
 "2022.01.01 ~ 2022.06.30",
 "2022.07.11",
 "286,242,340",
 "12,136,880",
 "2022.07.01 ~ 2022.12.31",
 "2023.01.25",
 "275,382,780",
 "13,217,160",
 "2023.01.01 ~ 2023.06.30",
 "2023.07.16",
 "293,457,440",
 "12,593,360",
 "2023.07.01 ~ 2023.12.31",
 "2024.01.23",
 "261,838,430",
 "12,094,870",
 "수정신고",
 "2024.04.04",
 "281,426,020",
 "14,053,620",
 "2024.01.01 ~ 2024.06.30",
 "2024.07.16",
 "266,062,620",
 "12,970,860",
 "2024.07.01 ~ 2024.12.31",
 "2025.01.15",
 "275,785,290",
 "14,005,320",
 "금융기관 제출",
 "2025년 04월 01일",
 "해운대세무서장"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"14,150,540"
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

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- issue_no: 발급번호
- customer.name: 성명(대표자) (고객 성명)
- customer.biz_no: 사업자등록번호 (고객 사업자등록번호)
- items.0.period: 과세기간 (1행)
- items.0.filed: 신고일 (1행)
- items.0.base_total: 매출과세표준계 (1행)
- items.0.base_taxable: 과세분 (1행)
- items.0.tax: 납부할세액(환급받을세액) (1행)
- items.1.period: 과세기간 (2행)
- items.1.kind: 신고구분 (2행)
- items.1.filed: 신고일 (2행)
- items.1.base_taxable: 과세분 (2행)
- items.1.base_exempt: 면세수입금액 (2행)
- items.1.tax: 납부할세액(환급받을세액) (2행)
- items.2.kind: 신고구분 (3행)
- items.2.base_taxable: 과세분 (3행)
- items.2.base_exempt: 면세수입금액 (3행)
- items.3.kind: 신고구분 (4행)
- items.3.base_total: 매출과세표준계 (4행)
- items.3.base_taxable: 과세분 (4행)
- items.3.base_exempt: 면세수입금액 (4행)
- items.3.tax: 납부할세액(환급받을세액) (4행)
- items.4.base_taxable: 과세분 (5행)
- items.4.tax: 납부할세액(환급받을세액) (5행)
- items.5.period: 과세기간 (6행)
- items.5.kind: 신고구분 (6행)
- items.5.base_exempt: 면세수입금액 (6행)
- items.5.tax: 납부할세액(환급받을세액) (6행)
- items.6.filed: 신고일 (7행)
- items.6.base_taxable: 과세분 (7행)
- items.7.period: 과세기간 (8행)
- items.7.kind: 신고구분 (8행)
- items.7.base_total: 매출과세표준계 (8행)
- items.7.base_taxable: 과세분 (8행)
- items.7.tax: 납부할세액(환급받을세액) (8행)
- items.8.filed: 신고일 (9행)
- items.8.base_total: 매출과세표준계 (9행)
- items.8.base_exempt: 면세수입금액 (9행)
- items.8.tax: 납부할세액(환급받을세액) (9행)
- issue_date: 발급일
```

답:

```json
[{"key": "issue_no", "value": "7272-950-4839-229", "bbox_2d": [72, 110, 191, 123], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [283, 142, 347, 155], "page": 1},
 {"key": "customer.biz_no", "value": "133-64-53148", "bbox_2d": [729, 172, 820, 184], "page": 1},
 {"key": "items.0.period", "value": "2021.01.01 ~ 2021.06.30", "bbox_2d": [96, 345, 245, 358], "page": 1},
 {"key": "items.0.filed", "value": "2021.07.07", "bbox_2d": [384, 345, 451, 358], "page": 1},
 {"key": "items.0.base_total", "value": "242,011,560", "bbox_2d": [507, 345, 581, 358], "page": 1},
 {"key": "items.0.base_taxable", "value": "242,011,560", "bbox_2d": [620, 345, 694, 358], "page": 1},
 {"key": "items.0.tax", "value": "11,477,360", "bbox_2d": [862, 345, 928, 358], "page": 1},
 {"key": "items.1.period", "value": "2021.07.01 ~ 2021.12.31", "bbox_2d": [96, 372, 245, 384], "page": 1},
 {"key": "items.1.kind", "value": "정기확정", "bbox_2d": [293, 372, 352, 384], "page": 1},
 {"key": "items.1.filed", "value": "2022.01.18", "bbox_2d": [384, 372, 451, 384], "page": 1},
 {"key": "items.1.base_taxable", "value": "291,521,570", "bbox_2d": [619, 372, 694, 384], "page": 1},
 {"key": "items.1.base_exempt", "value": "0", "bbox_2d": [799, 372, 806, 384], "page": 1},
 {"key": "items.1.tax", "value": "14,150,540", "bbox_2d": [861, 372, 928, 384], "page": 1},
 {"key": "items.2.kind", "value": "정기확정", "bbox_2d": [293, 398, 352, 411], "page": 1},
 {"key": "items.2.base_taxable", "value": "286,242,340", "bbox_2d": [619, 398, 694, 411], "page": 1},
 {"key": "items.2.base_exempt", "value": "0", "bbox_2d": [799, 398, 806, 411], "page": 1},
 {"key": "items.3.kind", "value": "정기확정", "bbox_2d": [293, 425, 352, 437], "page": 1},
 {"key": "items.3.base_total", "value": "275,382,780", "bbox_2d": [507, 425, 581, 437], "page": 1},
 {"key": "items.3.base_taxable", "value": "275,382,780", "bbox_2d": [619, 425, 694, 437], "page": 1},
 {"key": "items.3.base_exempt", "value": "0", "bbox_2d": [799, 425, 806, 437], "page": 1},
 {"key": "items.3.tax", "value": "13,217,160", "bbox_2d": [861, 425, 928, 437], "page": 1},
 {"key": "items.4.base_taxable", "value": "293,457,440", "bbox_2d": [619, 451, 694, 464], "page": 1},
 {"key": "items.4.tax", "value": "12,593,360", "bbox_2d": [861, 451, 928, 464], "page": 1},
 {"key": "items.5.period", "value": "2023.07.01 ~ 2023.12.31", "bbox_2d": [96, 478, 245, 490], "page": 1},
 {"key": "items.5.kind", "value": "정기확정", "bbox_2d": [293, 478, 352, 490], "page": 1},
 {"key": "items.5.base_exempt", "value": "0", "bbox_2d": [799, 478, 806, 490], "page": 1},
 {"key": "items.5.tax", "value": "12,094,870", "bbox_2d": [861, 478, 928, 490], "page": 1},
 {"key": "items.6.filed", "value": "2024.04.04", "bbox_2d": [384, 504, 451, 517], "page": 1},
 {"key": "items.6.base_taxable", "value": "281,426,020", "bbox_2d": [619, 504, 694, 517], "page": 1},
 {"key": "items.7.period", "value": "2024.01.01 ~ 2024.06.30", "bbox_2d": [96, 531, 245, 543], "page": 1},
 {"key": "items.7.kind", "value": "정기확정", "bbox_2d": [293, 531, 352, 543], "page": 1},
 {"key": "items.7.base_total", "value": "266,062,620", "bbox_2d": [507, 531, 581, 543], "page": 1},
 {"key": "items.7.base_taxable", "value": "266,062,620", "bbox_2d": [619, 531, 694, 543], "page": 1},
 {"key": "items.7.tax", "value": "12,970,860", "bbox_2d": [861, 531, 928, 543], "page": 1},
 {"key": "items.8.filed", "value": "2025.01.15", "bbox_2d": [384, 557, 451, 570], "page": 1},
 {"key": "items.8.base_total", "value": "275,785,290", "bbox_2d": [507, 557, 581, 570], "page": 1},
 {"key": "items.8.base_exempt", "value": "0", "bbox_2d": [799, 557, 806, 570], "page": 1},
 {"key": "items.8.tax", "value": "14,005,320", "bbox_2d": [861, 557, 928, 570], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [434, 688, 566, 701], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

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
[{"key": "seal.issuer", "value": true, "bbox_2d": [587, 700, 676, 764], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check vat_tax_base_certificate` → `python -m docgen.formdir card vat_tax_base_certificate` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions vat_tax_base_certificate --show` · `python -m docgen.preview vat_tax_base_certificate --out work/vat_tax_base_certificate`
