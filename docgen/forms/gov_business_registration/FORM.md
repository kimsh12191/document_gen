# 사업자등록증 (`gov_business_registration`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card gov_business_registration · card-hash: c536fe89445f -->

- **종류:** html 서식 (값은 fields.json 의 값 출처, 모양은 템플릿)
- **그룹:** business · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 사업자등록증
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa gov_business_registration --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 사업자등록증 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=162624673&bylClsCd=110202 개인사업자용 서식 및 종된 사업장 부표. 원본의 서식 규격 안내도 유지한다.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `form.json` | 이름·그룹·출처 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 23칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `official.biz_no` | 등록번호 | biz_no | 1쪽 [382, 192, 476, 205] | 늘 | 템플릿 | `profile.business.biz_no` | look/template.html.j2:27 · fields.json:5 | 묻기 |
| `official.company` | 상호 | text | 1쪽 [221, 232, 282, 247] | 늘 | 템플릿 | `profile.business.name` | look/template.html.j2:28 · fields.json:10 | 묻기 |
| `official.name` | 성명 | text | 1쪽 [718, 232, 779, 247] | 늘 | 템플릿 | `profile.person.name` | look/template.html.j2:29 · fields.json:15 | 묻기 |
| `official.address` | 사업장소재지 | text | 1쪽 [300, 325, 581, 340] | 늘 | 템플릿 | `profile.business.address.road_short` | look/template.html.j2:30 · fields.json:20 | 묻기 |
| `official.industry` | 업태 | text | 1쪽 [308, 401, 369, 416] | 늘 | 템플릿 | `profile.business.biz_type` | look/template.html.j2:31 · fields.json:25 | 묻기 |
| `official.item` | 종목 | text | 1쪽 [491, 401, 567, 416] | 늘 | 템플릿 | `profile.business.biz_item` | look/template.html.j2:32 · fields.json:30 | 묻기 |
| `official.taxpayer_type` | 과세유형 | text | 1쪽 [398, 168, 474, 183] | 늘 | 템플릿 | `rule:choice` | look/template.html.j2:33 · fields.json:35 | 묻기 |
| `official.opened0` | 개업연월일년 | number | 1쪽 [321, 277, 355, 289] | 늘 | 템플릿 | `profile.business.established` | look/template.html.j2:34 · fields.json:45 | 묻기 |
| `official.opened1` | 개업연월일월 | number | 1쪽 [401, 277, 418, 289] | 늘 | 템플릿 | `profile.business.established` | look/template.html.j2:35 · fields.json:52 | 묻기 |
| `official.opened2` | 개업연월일일 | number | 1쪽 [467, 277, 483, 289] | 늘 | 템플릿 | `profile.business.established` | look/template.html.j2:36 · fields.json:59 | 묻기 |
| `official.birth` | 생년월일 | date | 1쪽 [748, 277, 824, 289] | 늘 | 템플릿 | `profile.person.birth` | look/template.html.j2:37 · fields.json:66 | 묻기 |
| `official.issue_reason` | 발급사유 | text | 1쪽 [284, 429, 330, 444] | 늘 | 템플릿 | `rule:choice` | look/template.html.j2:38 · fields.json:71 | 묻기 |
| `official.unit_tax_no` | 사업자단위과세적용여부부(V) | text | 1쪽 [620, 578, 630, 588] | 늘 | 템플릿 | `rule:choice` | look/template.html.j2:39 · fields.json:81 | 묻기 |
| `official.einvoice_email` | 전자세금계산서전용전자우편주소 | text | 1쪽 [530, 624, 674, 636] | 늘 | 템플릿 | `profile.business.email` | look/template.html.j2:40 · fields.json:89 | 묻기 |
| `official.issue0` | 발급일년 | number | 1쪽 [527, 714, 561, 726] | 늘 | 템플릿 | `profile.issue_date` | look/template.html.j2:41 · fields.json:94 | 묻기 |
| `official.issue1` | 발급일월 | number | 1쪽 [653, 714, 670, 726] | 늘 | 템플릿 | `profile.issue_date` | look/template.html.j2:42 · fields.json:101 | 묻기 |
| `official.issue2` | 발급일일 | number | 1쪽 [776, 714, 793, 726] | 늘 | 템플릿 | `profile.issue_date` | look/template.html.j2:43 · fields.json:108 | 묻기 |
| `official.annex_biz_no0` | 부표사업자등록번호앞 | number | 2쪽 [505, 143, 530, 156] | 늘 | 템플릿 | `profile.business.biz_no` | look/template.html.j2:80 · fields.json:115 | 묻기 |
| `official.annex_biz_no1` | 부표사업자등록번호가운데 | number | 2쪽 [551, 143, 568, 156] | 늘 | 템플릿 | `profile.business.biz_no` | look/template.html.j2:81 · fields.json:122 | 묻기 |
| `official.annex_biz_no2` | 부표사업자등록번호뒤 | number | 2쪽 [602, 143, 644, 156] | 늘 | 템플릿 | `profile.business.biz_no` | look/template.html.j2:82 · fields.json:129 | 묻기 |
| `official.annex_issue0` | 부표발급일년 | number | 2쪽 [636, 785, 670, 797] | 늘 | 템플릿 | `profile.issue_date` | look/template.html.j2:83 · fields.json:136 | 묻기 |
| `official.annex_issue1` | 부표발급일월 | number | 2쪽 [711, 785, 728, 797] | 늘 | 템플릿 | `profile.issue_date` | look/template.html.j2:84 · fields.json:143 | 묻기 |
| `official.annex_issue2` | 부표발급일일 | number | 2쪽 [784, 785, 801, 797] | 늘 | 템플릿 | `profile.issue_date` | look/template.html.j2:85 · fields.json:150 | 묻기 |

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
"사업자등록증"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "133-64-53148",
 "새한커피",
 "남궁예태",
 "부산광역시 해운대구 좌동순환로 237, 7층",
 "음식점업",
 "커피전문점",
 "간이과세자",
 "2018",
 "04",
 "23",
 "1985.03.28",
 "재발급",
 "V",
 "admin@saehan.co.kr",
 "2025",
 "01",
 "133",
 "64",
 "53148"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"133-64-53148"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"간이과세자"
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
- official.biz_no: 등록번호
- official.company: 상호
- official.name: 성명
- official.address: 사업장소재지
- balance_sheet.liab_equity: 부채와자본총계
- official.industry: 업태
- official.item: 종목
- official.taxpayer_type: 과세유형
- official.opened0: 개업연월일년
- official.opened1: 개업연월일월
- official.opened2: 개업연월일일
- official.birth: 생년월일
- official.issue_reason: 발급사유
- official.unit_tax_no: 사업자단위과세적용여부부(V)
- official.einvoice_email: 전자세금계산서전용전자우편주소
- official.issue0: 발급일년
- official.issue1: 발급일월
- income_statement.revenue: 매출액
- official.issue2: 발급일일
- official.annex_biz_no0: 부표사업자등록번호앞
- official.annex_biz_no1: 부표사업자등록번호가운데
- official.annex_biz_no2: 부표사업자등록번호뒤
- official.annex_issue0: 부표발급일년
- official.annex_issue1: 부표발급일월
- official.annex_issue2: 부표발급일일
```

답:

```json
[{"key": "official.biz_no", "value": "133-64-53148", "bbox_2d": [382, 192, 476, 205], "page": 1},
 {"key": "official.company", "value": "새한커피", "bbox_2d": [221, 232, 282, 247], "page": 1},
 {"key": "official.name", "value": "남궁예태", "bbox_2d": [718, 232, 779, 247], "page": 1},
 {"key": "official.address", "value": "부산광역시 해운대구 좌동순환로 237, 7층", "bbox_2d": [300, 325, 581, 340], "page": 1},
 {"key": "balance_sheet.liab_equity", "value": null},
 {"key": "official.industry", "value": "음식점업", "bbox_2d": [308, 401, 369, 416], "page": 1},
 {"key": "official.item", "value": "커피전문점", "bbox_2d": [491, 401, 567, 416], "page": 1},
 {"key": "official.taxpayer_type", "value": "간이과세자", "bbox_2d": [398, 168, 474, 183], "page": 1},
 {"key": "official.opened0", "value": "2018", "bbox_2d": [321, 277, 355, 289], "page": 1},
 {"key": "official.opened1", "value": "04", "bbox_2d": [401, 277, 418, 289], "page": 1},
 {"key": "official.opened2", "value": "23", "bbox_2d": [467, 277, 483, 289], "page": 1},
 {"key": "official.birth", "value": "1985.03.28", "bbox_2d": [748, 277, 824, 289], "page": 1},
 {"key": "official.issue_reason", "value": "재발급", "bbox_2d": [284, 429, 330, 444], "page": 1},
 {"key": "official.unit_tax_no", "value": "V", "bbox_2d": [620, 578, 630, 588], "page": 1},
 {"key": "official.einvoice_email", "value": "admin@saehan.co.kr", "bbox_2d": [530, 624, 674, 636], "page": 1},
 {"key": "official.issue0", "value": "2025", "bbox_2d": [527, 714, 561, 726], "page": 1},
 {"key": "official.issue1", "value": "04", "bbox_2d": [653, 714, 670, 726], "page": 1},
 {"key": "income_statement.revenue", "value": null},
 {"key": "official.issue2", "value": "01", "bbox_2d": [776, 714, 793, 726], "page": 1},
 {"key": "official.annex_biz_no0", "value": "133", "bbox_2d": [505, 143, 530, 156], "page": 2},
 {"key": "official.annex_biz_no1", "value": "64", "bbox_2d": [551, 143, 568, 156], "page": 2},
 {"key": "official.annex_biz_no2", "value": "53148", "bbox_2d": [602, 143, 644, 156], "page": 2},
 {"key": "official.annex_issue0", "value": "2025", "bbox_2d": [636, 785, 670, 797], "page": 2},
 {"key": "official.annex_issue1", "value": "04", "bbox_2d": [711, 785, 728, 797], "page": 2},
 {"key": "official.annex_issue2", "value": "01", "bbox_2d": [784, 785, 801, 797], "page": 2}]
```

### 표 찾기 `table_find` · 채점 f1_iou50 (위치)

질문:

```
이 문서에서 표를 모두 찾아 JSON 목록으로 답하세요. 여기서 표는 같은 항목 묶음(열)이 행마다 되풀이되고 행 수가 서류마다 달라지는 목록입니다. 항목명과 값이 번갈아 있는 신청서 칸, 칸 수가 정해진 결재란은 표가 아닙니다.
표마다 {{"columns": [머리글 글자, …], "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호, "n_rows": 행 수}} 를 쓰고, 여러 쪽에 걸친 표는 쪽마다 따로 씁니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 행 수에는 머리글·합계 행과 모두 빈 행을 넣지 않습니다. 표가 없으면 [] 로 답하세요.
```

답:

```json
[]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa gov_business_registration --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check gov_business_registration` → `python -m docgen.formdir card gov_business_registration` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `fields.json` 의 `fields` 에 키·source | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` + `fields.json` 의 그 키 | 다시 |
| 답의 값 | `fields.json` 의 그 칸 `source` ([값 출처 목록](../_common/values.md)) | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` 의 `adjust(d, p, rng)` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (파일로). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa gov_business_registration --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions gov_business_registration --show` · `python -m docgen.preview gov_business_registration --out work/gov_business_registration`
