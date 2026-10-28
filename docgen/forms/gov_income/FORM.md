# 소득금액증명 (`gov_income`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card gov_income · card-hash: 211ec78f51f5 -->

- **종류:** html 서식 (값은 fields.json 의 값 출처, 모양은 템플릿)
- **그룹:** income · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 소득금액증명원 (다른 이름: 소득금액증명)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 소득금액증명 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?flSeq=155626737&flNm=%5B%EB%B3%84%EC%A7%80+15%5D+%EC%86%8C%EB%93%9D%EA%B8%88%EC%95%A1%EC%A6%9D%EB%AA%85%28%EA%B5%AD%EB%AC%B8%29&bylClsCd=200203 종합과세와 연말정산을 구분한 2024 개정 서식. 같은 근로소득을 두 구역에 중복 기재하지 않는다.

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
| `customer.name` ← `official.name` | 성명 | text | 1쪽 [214, 169, 275, 184] | 늘 | `profile.person.name` | look/template.html.j2:140 · fields.json:5 | 묻기 |
| `customer.rrn` ← `official.rrn` | 주민등록번호 | rrn | 1쪽 [670, 170, 784, 183] | 늘 | `profile.person.rrn` | look/template.html.j2:141 · fields.json:10 | 묻기 |
| `customer.address` ← `official.address` | 주소 | text | 1쪽 [214, 188, 535, 203] | 늘 | `profile.person.address.road_short` | look/template.html.j2:142 · fields.json:15 | 묻기 |
| `employer.name` ← `official.company` | 근로소득발생처 | text | 1쪽 [185, 469, 283, 481] | 늘 | `profile.employment.company.name` | look/template.html.j2:143 · fields.json:20 | 묻기 |
| `official.biz_no` | 발생처사업자등록번호 | biz_no | 1쪽 [321, 478, 392, 487] | 늘 | `profile.employment.company.biz_no` | look/template.html.j2:144 · fields.json:25 | 묻기 |
| `official.salary` | 지급받은총액 | amount | 1쪽 [431, 478, 490, 487] | 늘 | `parent.rows.0.amount` | look/template.html.j2:145 · fields.json:30 | 묻기 |
| `official.year` | 귀속연도 | number | 1쪽 [385, 148, 415, 159] | 늘 | `parent.rows.0.year` | look/template.html.j2:146 · fields.json:35 | 묻기 |
| `official.tax` | 총결정세액 | amount | 1쪽 [693, 478, 746, 487] | 늘 | `parent.rows.0.tax` | look/template.html.j2:147 · fields.json:41 | 묻기 |
| `official.number` | 발급번호 | text | 1쪽 [105, 143, 193, 151] | 늘 | `parent.issue_no` | look/template.html.j2:148 · fields.json:46 | 묻기 |
| `official.office` | 관할지역 | text | 1쪽 [601, 630, 627, 643] | 늘 | `parent.issuer` | look/template.html.j2:149 · fields.json:51 | 묻기 |
| `official.issue0` | 발급일년 | number | 1쪽 [544, 607, 570, 616] | 늘 | `profile.issue_date` | look/template.html.j2:150 · fields.json:57 | 묻기 |
| `official.issue1` | 발급일월 | number | 1쪽 [619, 607, 632, 616] | 늘 | `profile.issue_date` | look/template.html.j2:151 · fields.json:63 | 묻기 |
| `official.issue2` | 발급일일 | number | 1쪽 [681, 607, 694, 616] | 늘 | `profile.issue_date` | look/template.html.j2:152 · fields.json:69 | 묻기 |
| `official.salary_income` | 근로소득소득금액 | amount | 1쪽 [555, 478, 612, 487] | 늘 | `rule:amount` | look/template.html.j2:153 · fields.json:75 | 묻기 |
| `official.period_from` | 납세자가신청한증명귀속연도시작 | number | 1쪽 [579, 548, 604, 557] | 늘 | `parent.period` | look/template.html.j2:154 · fields.json:80 | 묻기 |
| `official.period_to` | 납세자가신청한증명귀속연도끝 | number | 1쪽 [636, 548, 661, 557] | 늘 | `parent.period` | look/template.html.j2:155 · fields.json:87 | 묻기 |
| `official.receipt_no` | 접수번호 | text | 1쪽 [103, 905, 156, 914] | 늘 | `rule:number` | look/template.html.j2:156 · fields.json:94 | 묻기 |
| `official.issuer_department` | 증명발급자담당부서 | text | 1쪽 [327, 893, 383, 907] | 늘 | `rule:choice` | look/template.html.j2:157 · fields.json:99 | 묻기 |
| `official.issuer_person` | 증명발급자담당자 | text | 1쪽 [514, 893, 555, 907] | 늘 | `rule:other_person` | look/template.html.j2:158 · fields.json:109 | 묻기 |
| `official.issuer_phone` | 증명발급자연락처 | phone | 1쪽 [668, 895, 755, 905] | 늘 | `rule:office_phone` | look/template.html.j2:159 · fields.json:114 | 묻기 |
| `official.tax_officer_department` | 세적담당자담당부서 | text | 1쪽 [327, 911, 418, 926] | 늘 | `rule:choice` | look/template.html.j2:160 · fields.json:119 | 묻기 |
| `official.tax_officer_person` | 세적담당자담당자 | text | 1쪽 [514, 911, 559, 926] | 늘 | `rule:other_person` | look/template.html.j2:161 · fields.json:129 | 묻기 |
| `official.tax_officer_phone` | 세적담당자연락처 | phone | 1쪽 [668, 912, 763, 924] | 늘 | `rule:office_phone` | look/template.html.j2:162 · fields.json:134 | 묻기 |

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
 "남궁예태",
 "850328-2489940",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "주식회사 다온패션",
 "123-88-81212",
 "47,550,000",
 "2024",
 "2,132,740",
 "8906-955-1735-796",
 "반포",
 "2025",
 "04",
 "01",
 "12,820,000",
 "2022",
 "8111-5978",
 "소득세과",
 "정서경",
 "051-675-9542",
 "재산법인세과",
 "장현승",
 "051-242-4681"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"04"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"소득세과"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- customer.name: 성명 (고객 성명)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- customer.address: 주소 (고객 주소)
- employer.name: 근로소득발생처 (직장 이름)
- official.biz_no: 발생처사업자등록번호 (직장의 사업자등록번호)
- official.salary: 지급받은총액
- official.year: 귀속연도
- official.tax: 총결정세액
- official.number: 발급번호
- official.office: 관할지역
- official.issue0: 발급일년
- official.issue1: 발급일월
- official.issue2: 발급일일
- official.salary_income: 근로소득소득금액
- official.period_from: 납세자가신청한증명귀속연도시작
- official.period_to: 납세자가신청한증명귀속연도끝
- official.receipt_no: 접수번호
- official.issuer_department: 증명발급자담당부서
- official.issuer_person: 증명발급자담당자
- official.issuer_phone: 증명발급자연락처
- official.tax_officer_department: 세적담당자담당부서
- official.tax_officer_person: 세적담당자담당자
- official.tax_officer_phone: 세적담당자연락처
```

답:

```json
[{"key": "customer.name", "value": "남궁예태", "bbox_2d": [214, 169, 275, 184], "page": 1},
 {"key": "customer.rrn", "value": "850328-2489940", "bbox_2d": [670, 170, 784, 183], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [214, 188, 535, 203], "page": 1},
 {"key": "employer.name", "value": "주식회사 다온패션", "bbox_2d": [185, 469, 283, 481], "page": 1},
 {"key": "official.biz_no", "value": "123-88-81212", "bbox_2d": [321, 478, 392, 487], "page": 1},
 {"key": "official.salary", "value": "47,550,000", "bbox_2d": [431, 478, 490, 487], "page": 1},
 {"key": "official.year", "value": "2024", "bbox_2d": [385, 148, 415, 159], "page": 1},
 {"key": "official.tax", "value": "2,132,740", "bbox_2d": [693, 478, 746, 487], "page": 1},
 {"key": "official.number", "value": "8906-955-1735-796", "bbox_2d": [105, 143, 193, 151], "page": 1},
 {"key": "official.office", "value": "반포", "bbox_2d": [601, 630, 627, 643], "page": 1},
 {"key": "official.issue0", "value": "2025", "bbox_2d": [544, 607, 570, 616], "page": 1},
 {"key": "official.issue1", "value": "04", "bbox_2d": [619, 607, 632, 616], "page": 1},
 {"key": "official.issue2", "value": "01", "bbox_2d": [681, 607, 694, 616], "page": 1},
 {"key": "official.salary_income", "value": "12,820,000", "bbox_2d": [555, 478, 612, 487], "page": 1},
 {"key": "official.period_from", "value": "2022", "bbox_2d": [579, 548, 604, 557], "page": 1},
 {"key": "official.period_to", "value": "2024", "bbox_2d": [636, 548, 661, 557], "page": 1},
 {"key": "official.receipt_no", "value": "8111-5978", "bbox_2d": [103, 905, 156, 914], "page": 1},
 {"key": "official.issuer_department", "value": "소득세과", "bbox_2d": [327, 893, 383, 907], "page": 1},
 {"key": "official.issuer_person", "value": "정서경", "bbox_2d": [514, 893, 555, 907], "page": 1},
 {"key": "official.issuer_phone", "value": "051-675-9542", "bbox_2d": [668, 895, 755, 905], "page": 1},
 {"key": "official.tax_officer_department", "value": "재산법인세과", "bbox_2d": [327, 911, 418, 926], "page": 1},
 {"key": "official.tax_officer_person", "value": "장현승", "bbox_2d": [514, 911, 559, 926], "page": 1},
 {"key": "official.tax_officer_phone", "value": "051-242-4681", "bbox_2d": [668, 912, 763, 924], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions gov_income --show` · `python -m docgen.preview gov_income --out work/gov_income`
