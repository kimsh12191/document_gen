# 여신거래약정서(기업용) (`hana_corporate_agreement`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hana_corporate_agreement · card-hash: 338e43267a96 -->

- **종류:** html 서식 (값은 fields.json 의 값 출처, 모양은 템플릿)
- **그룹:** hana · **쪽 수:** 4 (seed 1000000 로 그린 것) · **분류 정답:** 여신거래약정서(기업용)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hana_corporate_agreement --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 여신거래약정서(기업용) 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://image.kebhana.com/cont/download/documents/provide/0000003061032_20260630.pdf

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `form.json` | 이름·그룹·출처 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 28칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `customer.name` ← `official.name` | 채무자 | text | 1쪽 [539, 233, 640, 248] | 늘 | 템플릿 | `profile.corporation.name` | look/template.html.j2:125 · fields.json:5 | 묻기 |
| `customer.address` ← `official.address` | 주소 | text | 1쪽 [539, 259, 827, 274] | 늘 | 템플릿 | `profile.corporation.address.road_short` | look/template.html.j2:126 · fields.json:10 | 묻기 |
| `official.amount` | 여신금액 | amount | 1쪽 [279, 422, 376, 435] | 늘 | 템플릿 | `parent.loan.amount` | look/template.html.j2:127 · fields.json:15 | 묻기 |
| `official.subject` | 여신과목 | text | 1쪽 [261, 393, 341, 406] | 늘 | 템플릿 | `parent.loan.subject` | look/template.html.j2:128 · fields.json:37 | 묻기 |
| `terms.rate` | 약정이율 | number | 1쪽 [524, 486, 551, 496] | 늘 | 템플릿 | `parent.loan.applied_rate` | look/template.html.j2:132 · fields.json:83 | 묻기 |
| `terms.start0` | 개시일년 | number | 1쪽 [271, 457, 284, 466] | 늘 | 템플릿 | `parent.loan.start_date` | look/template.html.j2:135 · fields.json:119 | 묻기 |
| `terms.start1` | 개시일월 | number | 1쪽 [316, 457, 329, 466] | 늘 | 템플릿 | `parent.loan.start_date` | look/template.html.j2:136 · fields.json:133 | 묻기 |
| `terms.start2` | 개시일일 | number | 1쪽 [360, 457, 373, 466] | 늘 | 템플릿 | `parent.loan.start_date` | look/template.html.j2:137 · fields.json:145 | 묻기 |
| `terms.end0` | 만료일년 | number | 1쪽 [598, 457, 611, 466] | 늘 | 템플릿 | `parent.loan.maturity` | look/template.html.j2:138 · fields.json:157 | 묻기 |
| `terms.end1` | 만료일월 | number | 1쪽 [645, 457, 658, 466] | 늘 | 템플릿 | `parent.loan.maturity` | look/template.html.j2:139 · fields.json:171 | 묻기 |
| `terms.end2` | 만료일일 | number | 1쪽 [689, 457, 702, 466] | 늘 | 템플릿 | `parent.loan.maturity` | look/template.html.j2:140 · fields.json:183 | 묻기 |
| `terms.written0` | 작성일년 | number | 1쪽 [743, 184, 756, 193] | 늘 | 템플릿 | `parent.contract_date` | look/template.html.j2:141 · fields.json:195 | 묻기 |
| `terms.written1` | 작성일월 | number | 1쪽 [813, 184, 826, 193] | 늘 | 템플릿 | `parent.contract_date` | look/template.html.j2:142 · fields.json:209 | 묻기 |
| `terms.written2` | 작성일일 | number | 1쪽 [877, 184, 890, 193] | 늘 | 템플릿 | `parent.contract_date` | look/template.html.j2:143 · fields.json:221 | 묻기 |
| `official.name_copy` | 채무자 | text | 3쪽 [539, 233, 640, 248] | 늘 | 템플릿 | `profile.corporation.name` | look/template.html.j2:325 · fields.json:21 | 묻기 |
| `official.address_copy` | 주소 | text | 3쪽 [539, 259, 827, 274] | 늘 | 템플릿 | `profile.corporation.address.road_short` | look/template.html.j2:326 · fields.json:26 | 묻기 |
| `official.amount_copy` | 여신금액 | amount | 3쪽 [279, 422, 376, 435] | 늘 | 템플릿 | `parent.loan.amount` | look/template.html.j2:327 · fields.json:31 | 묻기 |
| `official.subject_copy` | 여신과목 | text | 3쪽 [261, 393, 341, 406] | 늘 | 템플릿 | `parent.loan.subject` | look/template.html.j2:328 · fields.json:42 | 묻기 |
| `terms.rate_copy` | 약정이율 | number | 3쪽 [524, 486, 551, 496] | 늘 | 템플릿 | `parent.loan.applied_rate` | look/template.html.j2:332 · fields.json:89 | 묻기 |
| `terms.start0_copy` | 개시일년 | number | 3쪽 [271, 457, 284, 466] | 늘 | 템플릿 | `parent.loan.start_date` | look/template.html.j2:335 · fields.json:126 | 묻기 |
| `terms.start1_copy` | 개시일월 | number | 3쪽 [316, 457, 329, 466] | 늘 | 템플릿 | `parent.loan.start_date` | look/template.html.j2:336 · fields.json:139 | 묻기 |
| `terms.start2_copy` | 개시일일 | number | 3쪽 [360, 457, 373, 466] | 늘 | 템플릿 | `parent.loan.start_date` | look/template.html.j2:337 · fields.json:151 | 묻기 |
| `terms.end0_copy` | 만료일년 | number | 3쪽 [598, 457, 611, 466] | 늘 | 템플릿 | `parent.loan.maturity` | look/template.html.j2:338 · fields.json:164 | 묻기 |
| `terms.end1_copy` | 만료일월 | number | 3쪽 [645, 457, 658, 466] | 늘 | 템플릿 | `parent.loan.maturity` | look/template.html.j2:339 · fields.json:177 | 묻기 |
| `terms.end2_copy` | 만료일일 | number | 3쪽 [689, 457, 702, 466] | 늘 | 템플릿 | `parent.loan.maturity` | look/template.html.j2:340 · fields.json:189 | 묻기 |
| `terms.written0_copy` | 작성일년 | number | 3쪽 [743, 184, 756, 193] | 늘 | 템플릿 | `parent.contract_date` | look/template.html.j2:341 · fields.json:202 | 묻기 |
| `terms.written1_copy` | 작성일월 | number | 3쪽 [813, 184, 826, 193] | 늘 | 템플릿 | `parent.contract_date` | look/template.html.j2:342 · fields.json:215 | 묻기 |
| `terms.written2_copy` | 작성일일 | number | 3쪽 [877, 184, 890, 193] | 늘 | 템플릿 | `parent.contract_date` | look/template.html.j2:343 · fields.json:227 | 묻기 |

## 체크·도장·서명 (marks) — 10칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `terms.method` | 개별거래 | checkbox (개별거래) | 1쪽 [659, 401, 664, 402] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:129 · fields.json:47 | 묻기 |
| `terms.fixed` | 고정금리 | checkbox (고정금리) | 1쪽 [234, 476, 239, 477] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:130 · fields.json:59 | 묻기 |
| `terms.fixed_choice` | 확정금리 | checkbox (확정금리) | 1쪽 [296, 492, 301, 493] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:131 · fields.json:71 | 묻기 |
| `terms.repay` | 만기일시상환 | checkbox (만기일시상환) | 1쪽 [234, 814, 241, 815] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:133 · fields.json:95 | 묻기 |
| `terms.execution` | 전액실행 | checkbox (전액실행) | 1쪽 [234, 743, 239, 744] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:134 · fields.json:107 | 묻기 |
| `terms.method_copy` | 개별거래 | checkbox (개별거래) | 3쪽 [659, 401, 664, 402] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:329 · fields.json:53 | 묻기 |
| `terms.fixed_copy` | 고정금리 | checkbox (고정금리) | 3쪽 [234, 476, 239, 477] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:330 · fields.json:65 | 묻기 |
| `terms.fixed_choice_copy` | 확정금리 | checkbox (확정금리) | 3쪽 [296, 492, 301, 493] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:331 · fields.json:77 | 묻기 |
| `terms.repay_copy` | 만기일시상환 | checkbox (만기일시상환) | 3쪽 [234, 814, 241, 815] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:333 · fields.json:101 | 묻기 |
| `terms.execution_copy` | 전액실행 | checkbox (전액실행) | 3쪽 [234, 743, 239, 744] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:334 · fields.json:113 | 묻기 |

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
"여신거래약정서(기업용)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "(주)미래케미칼",
 "제주특별자치도 제주시 첨단로 381-19, 2층",
 "2,100,000,000",
 "시설자금대출",
 "6.08",
 "25",
 "04",
 "14",
 "35"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"시설자금대출"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"25"
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
- customer.name: 채무자 (고객 성명, 같은 항목명 중 1번째 칸)
- customer.address: 주소 (고객 주소, 같은 항목명 중 1번째 칸)
- official.amount: 여신금액 (같은 항목명 중 1번째 칸)
- official.subject: 여신과목 (같은 항목명 중 1번째 칸)
- terms.rate: 약정이율 (같은 항목명 중 1번째 칸)
- terms.start0: 개시일년 (같은 항목명 중 1번째 칸)
- terms.start1: 개시일월 (같은 항목명 중 1번째 칸)
- terms.start2: 개시일일 (같은 항목명 중 1번째 칸)
- terms.end0: 만료일년 (같은 항목명 중 1번째 칸)
- terms.end1: 만료일월 (같은 항목명 중 1번째 칸)
- terms.end2: 만료일일 (같은 항목명 중 1번째 칸)
- terms.written0: 작성일년 (같은 항목명 중 1번째 칸)
- terms.written1: 작성일월 (같은 항목명 중 1번째 칸)
- terms.written2: 작성일일 (같은 항목명 중 1번째 칸)
- official.name_copy: 채무자 (같은 항목명 중 2번째 칸)
- official.address_copy: 주소 (같은 항목명 중 2번째 칸)
- official.amount_copy: 여신금액 (같은 항목명 중 2번째 칸)
- official.subject_copy: 여신과목 (같은 항목명 중 2번째 칸)
- terms.rate_copy: 약정이율 (같은 항목명 중 2번째 칸)
- terms.start0_copy: 개시일년 (같은 항목명 중 2번째 칸)
- terms.start1_copy: 개시일월 (같은 항목명 중 2번째 칸)
- terms.start2_copy: 개시일일 (같은 항목명 중 2번째 칸)
- terms.end0_copy: 만료일년 (같은 항목명 중 2번째 칸)
- terms.end1_copy: 만료일월 (같은 항목명 중 2번째 칸)
- terms.end2_copy: 만료일일 (같은 항목명 중 2번째 칸)
- terms.written0_copy: 작성일년 (같은 항목명 중 2번째 칸)
- terms.written1_copy: 작성일월 (같은 항목명 중 2번째 칸)
- terms.written2_copy: 작성일일 (같은 항목명 중 2번째 칸)
```

답:

```json
[{"key": "customer.name", "value": "(주)미래케미칼", "bbox_2d": [539, 233, 640, 248], "page": 1},
 {"key": "customer.address", "value": "제주특별자치도 제주시 첨단로 381-19, 2층", "bbox_2d": [539, 259, 827, 274], "page": 1},
 {"key": "official.amount", "value": "2,100,000,000", "bbox_2d": [279, 422, 376, 435], "page": 1},
 {"key": "official.subject", "value": "시설자금대출", "bbox_2d": [261, 393, 341, 406], "page": 1},
 {"key": "terms.rate", "value": "6.08", "bbox_2d": [524, 486, 551, 496], "page": 1},
 {"key": "terms.start0", "value": "25", "bbox_2d": [271, 457, 284, 466], "page": 1},
 {"key": "terms.start1", "value": "04", "bbox_2d": [316, 457, 329, 466], "page": 1},
 {"key": "terms.start2", "value": "14", "bbox_2d": [360, 457, 373, 466], "page": 1},
 {"key": "terms.end0", "value": "35", "bbox_2d": [598, 457, 611, 466], "page": 1},
 {"key": "terms.end1", "value": "04", "bbox_2d": [645, 457, 658, 466], "page": 1},
 {"key": "terms.end2", "value": "14", "bbox_2d": [689, 457, 702, 466], "page": 1},
 {"key": "terms.written0", "value": "25", "bbox_2d": [743, 184, 756, 193], "page": 1},
 {"key": "terms.written1", "value": "04", "bbox_2d": [813, 184, 826, 193], "page": 1},
 {"key": "terms.written2", "value": "14", "bbox_2d": [877, 184, 890, 193], "page": 1},
 {"key": "official.name_copy", "value": "(주)미래케미칼", "bbox_2d": [539, 233, 640, 248], "page": 3},
 {"key": "official.address_copy", "value": "제주특별자치도 제주시 첨단로 381-19, 2층", "bbox_2d": [539, 259, 827, 274], "page": 3},
 {"key": "official.amount_copy", "value": "2,100,000,000", "bbox_2d": [279, 422, 376, 435], "page": 3},
 {"key": "official.subject_copy", "value": "시설자금대출", "bbox_2d": [261, 393, 341, 406], "page": 3},
 {"key": "terms.rate_copy", "value": "6.08", "bbox_2d": [524, 486, 551, 496], "page": 3},
 {"key": "terms.start0_copy", "value": "25", "bbox_2d": [271, 457, 284, 466], "page": 3},
 {"key": "terms.start1_copy", "value": "04", "bbox_2d": [316, 457, 329, 466], "page": 3},
 {"key": "terms.start2_copy", "value": "14", "bbox_2d": [360, 457, 373, 466], "page": 3},
 {"key": "terms.end0_copy", "value": "35", "bbox_2d": [598, 457, 611, 466], "page": 3},
 {"key": "terms.end1_copy", "value": "04", "bbox_2d": [645, 457, 658, 466], "page": 3},
 {"key": "terms.end2_copy", "value": "14", "bbox_2d": [689, 457, 702, 466], "page": 3},
 {"key": "terms.written0_copy", "value": "25", "bbox_2d": [743, 184, 756, 193], "page": 3},
 {"key": "terms.written1_copy", "value": "04", "bbox_2d": [813, 184, 826, 193], "page": 3},
 {"key": "terms.written2_copy", "value": "14", "bbox_2d": [877, 184, 890, 193], "page": 3}]
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
- terms.method: 개별거래 (같은 항목명 중 1번째 칸, 체크박스, 보기: 개별거래)
- terms.fixed: 고정금리 (같은 항목명 중 1번째 칸, 체크박스, 보기: 고정금리)
- terms.fixed_choice: 확정금리 (같은 항목명 중 1번째 칸, 체크박스, 보기: 확정금리)
- terms.repay: 만기일시상환 (같은 항목명 중 1번째 칸, 체크박스, 보기: 만기일시상환)
- terms.execution: 전액실행 (같은 항목명 중 1번째 칸, 체크박스, 보기: 전액실행)
- terms.method_copy: 개별거래 (같은 항목명 중 2번째 칸, 체크박스, 보기: 개별거래)
- terms.fixed_copy: 고정금리 (같은 항목명 중 2번째 칸, 체크박스, 보기: 고정금리)
- terms.fixed_choice_copy: 확정금리 (같은 항목명 중 2번째 칸, 체크박스, 보기: 확정금리)
- terms.repay_copy: 만기일시상환 (같은 항목명 중 2번째 칸, 체크박스, 보기: 만기일시상환)
- terms.execution_copy: 전액실행 (같은 항목명 중 2번째 칸, 체크박스, 보기: 전액실행)
```

답:

```json
[{"key": "terms.method", "value": "개별거래", "bbox_2d": [655, 395, 670, 408], "page": 1},
 {"key": "terms.fixed", "value": "고정금리", "bbox_2d": [230, 471, 243, 481], "page": 1},
 {"key": "terms.fixed_choice", "value": "확정금리", "bbox_2d": [292, 486, 307, 499], "page": 1},
 {"key": "terms.repay", "value": "만기일시상환", "bbox_2d": [230, 810, 243, 819], "page": 1},
 {"key": "terms.execution", "value": "전액실행", "bbox_2d": [230, 738, 243, 748], "page": 1},
 {"key": "terms.method_copy", "value": "개별거래", "bbox_2d": [655, 395, 670, 408], "page": 3},
 {"key": "terms.fixed_copy", "value": "고정금리", "bbox_2d": [230, 471, 243, 481], "page": 3},
 {"key": "terms.fixed_choice_copy", "value": "확정금리", "bbox_2d": [292, 486, 307, 499], "page": 3},
 {"key": "terms.repay_copy", "value": "만기일시상환", "bbox_2d": [230, 810, 243, 819], "page": 3},
 {"key": "terms.execution_copy", "value": "전액실행", "bbox_2d": [230, 738, 243, 748], "page": 3}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hana_corporate_agreement --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hana_corporate_agreement` → `python -m docgen.formdir card hana_corporate_agreement` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `fields.json` 의 `fields` 에 키·source | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` + `fields.json` 의 그 키 | 다시 |
| 답의 값 | `fields.json` 의 그 칸 `source` ([값 출처 목록](../_common/values.md)) | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` 의 `adjust(d, p, rng)` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (studio html 편집). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hana_corporate_agreement --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hana_corporate_agreement --show` · `python -m docgen.preview hana_corporate_agreement --out work/hana_corporate_agreement`
