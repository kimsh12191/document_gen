# 사업자등록증 (`gov_business_registration`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card gov_business_registration · card-hash: ebd6b4e6a55d -->

- **종류:** html 서식 (값은 fields.json 의 값 출처, 모양은 템플릿)
- **그룹:** business · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 사업자등록증
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 사업자등록증 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=162624673&bylClsCd=110202 개인사업자용 서식 및 종된 사업장 부표. 원본의 서식 규격 안내도 유지한다.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `form.json` | 이름·그룹·출처 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 23칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `corp.biz_no` ← `official.biz_no` | 등록번호 | biz_no | 1쪽 [382, 192, 476, 205] | 늘 | `profile.business.biz_no` | look/template.html.j2:27 · fields.json:5 | 묻기 |
| `corp.name` ← `official.company` | 상호 | text | 1쪽 [221, 232, 282, 247] | 늘 | `profile.business.name` | look/template.html.j2:28 · fields.json:10 | 묻기 |
| `customer.name` ← `official.name` | 성명 | text | 1쪽 [718, 232, 779, 247] | 늘 | `profile.person.name` | look/template.html.j2:29 · fields.json:15 | 묻기 |
| `corp.address` ← `official.address` | 사업장소재지 | text | 1쪽 [300, 325, 581, 340] | 늘 | `profile.business.address.road_short` | look/template.html.j2:30 · fields.json:20 | 묻기 |
| `official.industry` | 업태 | text | 1쪽 [308, 401, 369, 416] | 늘 | `profile.business.biz_type` | look/template.html.j2:31 · fields.json:25 | 묻기 |
| `corp.biz_item` ← `official.item` | 종목 | text | 1쪽 [491, 401, 567, 416] | 늘 | `profile.business.biz_item` | look/template.html.j2:32 · fields.json:30 | 묻기 |
| `official.taxpayer_type` | 과세유형 | text | 1쪽 [398, 168, 474, 183] | 늘 | `rule:choice` | look/template.html.j2:33 · fields.json:35 | 묻기 |
| `official.opened0` | 개업연월일년 | number | 1쪽 [321, 277, 355, 289] | 늘 | `profile.business.established` | look/template.html.j2:34 · fields.json:45 | 묻기 |
| `official.opened1` | 개업연월일월 | number | 1쪽 [401, 277, 418, 289] | 늘 | `profile.business.established` | look/template.html.j2:35 · fields.json:52 | 묻기 |
| `official.opened2` | 개업연월일일 | number | 1쪽 [467, 277, 483, 289] | 늘 | `profile.business.established` | look/template.html.j2:36 · fields.json:59 | 묻기 |
| `official.birth` | 생년월일 | date | 1쪽 [748, 277, 824, 289] | 늘 | `profile.person.birth` | look/template.html.j2:37 · fields.json:66 | 묻기 |
| `official.issue_reason` | 발급사유 | text | 1쪽 [284, 429, 330, 444] | 늘 | `rule:choice` | look/template.html.j2:38 · fields.json:71 | 묻기 |
| `official.unit_tax_no` | 사업자단위과세적용여부부(V) | text | 1쪽 [620, 578, 630, 588] | 늘 | `rule:choice` | look/template.html.j2:39 · fields.json:81 | 묻기 |
| `official.einvoice_email` | 전자세금계산서전용전자우편주소 | text | 1쪽 [530, 624, 674, 636] | 늘 | `profile.business.email` | look/template.html.j2:40 · fields.json:89 | 묻기 |
| `official.issue0` | 발급일년 | number | 1쪽 [527, 714, 561, 726] | 늘 | `profile.issue_date` | look/template.html.j2:41 · fields.json:94 | 묻기 |
| `official.issue1` | 발급일월 | number | 1쪽 [653, 714, 670, 726] | 늘 | `profile.issue_date` | look/template.html.j2:42 · fields.json:101 | 묻기 |
| `official.issue2` | 발급일일 | number | 1쪽 [776, 714, 793, 726] | 늘 | `profile.issue_date` | look/template.html.j2:43 · fields.json:108 | 묻기 |
| `official.annex_biz_no0` | 부표사업자등록번호앞 | number | 2쪽 [505, 143, 530, 156] | 늘 | `profile.business.biz_no` | look/template.html.j2:80 · fields.json:115 | 묻기 |
| `official.annex_biz_no1` | 부표사업자등록번호가운데 | number | 2쪽 [551, 143, 568, 156] | 늘 | `profile.business.biz_no` | look/template.html.j2:81 · fields.json:122 | 묻기 |
| `official.annex_biz_no2` | 부표사업자등록번호뒤 | number | 2쪽 [602, 143, 644, 156] | 늘 | `profile.business.biz_no` | look/template.html.j2:82 · fields.json:129 | 묻기 |
| `official.annex_issue0` | 부표발급일년 | number | 2쪽 [636, 785, 670, 797] | 늘 | `profile.issue_date` | look/template.html.j2:83 · fields.json:136 | 묻기 |
| `official.annex_issue1` | 부표발급일월 | number | 2쪽 [711, 785, 728, 797] | 늘 | `profile.issue_date` | look/template.html.j2:84 · fields.json:143 | 묻기 |
| `official.annex_issue2` | 부표발급일일 | number | 2쪽 [784, 785, 801, 797] | 늘 | `profile.issue_date` | look/template.html.j2:85 · fields.json:150 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키 `a` ← `b`:** 질문·정답은 공통 키 a, 서식의 원래 키는 b (키 사전이 정함). **정한 곳:** 템플릿에서 그 칸 자리 (html·코드 서식) / 칸 목록의 그 칸 (원본 서식).

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

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- corp.biz_no: 등록번호 (법인·사업자 사업자등록번호)
- corp.name: 상호 (법인·사업자 상호)
- customer.name: 성명 (고객 성명)
- corp.address: 사업장소재지 (법인·사업자 주소)
- official.industry: 업태
- corp.biz_item: 종목 (법인·사업자 업종)
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
[{"key": "corp.biz_no", "value": "133-64-53148", "bbox_2d": [382, 192, 476, 205], "page": 1},
 {"key": "corp.name", "value": "새한커피", "bbox_2d": [221, 232, 282, 247], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [718, 232, 779, 247], "page": 1},
 {"key": "corp.address", "value": "부산광역시 해운대구 좌동순환로 237, 7층", "bbox_2d": [300, 325, 581, 340], "page": 1},
 {"key": "official.industry", "value": "음식점업", "bbox_2d": [308, 401, 369, 416], "page": 1},
 {"key": "corp.biz_item", "value": "커피전문점", "bbox_2d": [491, 401, 567, 416], "page": 1},
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
 {"key": "official.issue2", "value": "01", "bbox_2d": [776, 714, 793, 726], "page": 1},
 {"key": "official.annex_biz_no0", "value": "133", "bbox_2d": [505, 143, 530, 156], "page": 2},
 {"key": "official.annex_biz_no1", "value": "64", "bbox_2d": [551, 143, 568, 156], "page": 2},
 {"key": "official.annex_biz_no2", "value": "53148", "bbox_2d": [602, 143, 644, 156], "page": 2},
 {"key": "official.annex_issue0", "value": "2025", "bbox_2d": [636, 785, 670, 797], "page": 2},
 {"key": "official.annex_issue1", "value": "04", "bbox_2d": [711, 785, 728, 797], "page": 2},
 {"key": "official.annex_issue2", "value": "01", "bbox_2d": [784, 785, 801, 797], "page": 2}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `fields.json` 의 `fields` 에 키·source | 미리보기로 확인 → 재검수 → 카드 다시 만들기 |
| 칸 키·항목명 바꾸기 | `look/template.html.j2` 의 `f("키", label=…)` + `fields.json` (질문만 바꾸려면 `questions.json`) | `questions … --check` |
| 값이 이상함 / 칸끼리 안 맞음 | `fields.json` 의 source / `generate.py` 의 `adjust(d, p, rng)` | 재검수 |
| 모양·표·문구 | `look/template.html.j2` (studio html 편집) | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions gov_business_registration --show` · `python -m docgen.preview gov_business_registration --out work/gov_business_registration`
