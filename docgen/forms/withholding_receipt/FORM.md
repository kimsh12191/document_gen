# 근로소득 원천징수영수증 (`withholding_receipt`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card withholding_receipt · card-hash: 027de449b779 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** income · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 근로소득 원천징수영수증
- **쓰이는 업무:** 개인 신용대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa withholding_receipt --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 근로소득 원천징수영수증(근로소득 지급명세서) 제1쪽 — 소득세법 시행규칙 [별지 제24호서식(1)].

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/income.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 42칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `year` | 귀속연도 | number | 1쪽 [340, 168, 366, 178] | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:240 | 묻기 |
| `customer.name` ← `payer.name` | 법인명(상호) | text | 1쪽 [282, 206, 385, 216] | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:75 | 묻기 |
| `customer.ceo` ← `payer.ceo` | 대표자(성명) | text | 1쪽 [667, 206, 704, 216] | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:70 | 묻기 |
| `customer.biz_no` ← `payer.biz_no` | 사업자등록번호 | biz_no | 1쪽 [282, 221, 353, 230] | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:65 | 묻기 |
| `customer.address` ← `payer.address` | 소재지(주소) | text | 1쪽 [282, 250, 497, 260] | 늘 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:60 | 묻기 |
| `earner.name` | 성명 | text | 1쪽 [282, 270, 332, 280] | 늘 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:15 | 묻기 |
| `customer.rrn` ← `earner.rrn` | 주민등록번호 | rrn | 1쪽 [667, 270, 752, 280] | 늘 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:20 | 묻기 |
| `earner.address` | 주소 | text | 1쪽 [282, 290, 711, 300] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:10 | 묻기 |
| `work.company` | 근무처명 | text | 1쪽 [366, 321, 469, 331] | 늘 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:160 | 묻기 |
| `work.biz_no` | 사업자등록번호 | biz_no | 1쪽 [382, 336, 453, 345] | 늘 | 템플릿 | generate.py | look/template.html.j2:59 · fields.json:150 | 묻기 |
| `employer.period` ← `work.period` | 근무기간 | text | 1쪽 [364, 351, 471, 360] | 늘 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:165 | 묻기 |
| `work.salary` | 급여 | amount | 1쪽 [435, 379, 491, 389] | 늘 | 템플릿 | generate.py | look/template.html.j2:62 · fields.json:175 | 묻기 |
| `work.bonus` | 상여 | amount | 1쪽 [441, 394, 491, 404] | 늘 | 템플릿 | generate.py | look/template.html.j2:63 · fields.json:155 | 묻기 |
| `work.total` | 계 | amount | 1쪽 [435, 481, 491, 491] | 늘 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:180 | 묻기 |
| `nontax.meal` | 식사대 | number | 1쪽 [441, 559, 491, 569] | 늘 | 템플릿 | generate.py | look/template.html.j2:75 · fields.json:45 | 묻기 |
| `nontax.total` | 비과세소득계 | amount | 1쪽 [441, 590, 491, 600] | 늘 | 템플릿 | generate.py | look/template.html.j2:77 · fields.json:55 | 묻기 |
| `tax.final_income` | 결정세액 | amount | 1쪽 [644, 637, 694, 647] | 늘 | 템플릿 | generate.py | look/template.html.j2:84 · fields.json:110 | 묻기 |
| `tax.final_local` | 결정세액 | number | 1쪽 [762, 637, 803, 647] | 늘 | 템플릿 | generate.py | look/template.html.j2:84 · fields.json:115 | 묻기 |
| `tax.prepaid_income` | 주(현)근무지 | amount | 1쪽 [644, 678, 694, 688] | 늘 | 템플릿 | generate.py | look/template.html.j2:87 · fields.json:120 | 묻기 |
| `tax.prepaid_local` | 주(현)근무지 | number | 1쪽 [762, 678, 803, 688] | 늘 | 템플릿 | generate.py | look/template.html.j2:87 · fields.json:125 | 묻기 |
| `tax.diff_income` | 차감징수세액 | amount | 1쪽 [650, 707, 694, 717] | 늘 | 템플릿 | generate.py | look/template.html.j2:89 · fields.json:95 | 묻기 |
| `tax.diff_local` | 차감징수세액 | number | 1쪽 [765, 707, 803, 717] | 늘 | 템플릿 | generate.py | look/template.html.j2:89 · fields.json:100 | 묻기 |
| `tax.effective_rate` | 실효세율(%) | number | 1쪽 [886, 721, 902, 731] | 늘 | 템플릿 | generate.py | look/template.html.j2:90 · fields.json:105 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [823, 760, 904, 770] | 늘 | 템플릿 | generate.py | look/template.html.j2:94 · fields.json:30 | 묻기 |
| `tax_office` | 세무서장 | text | 1쪽 [96, 818, 223, 832] | 늘 | 템플릿 | generate.py | look/template.html.j2:96 · fields.json:130 | 묻기 |
| `work_prev.company` | 종(전)근무처명 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:195 | 묻기 |
| `work_prev.biz_no` | 종(전)사업자등록번호 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:59 · fields.json:185 | 묻기 |
| `work_prev.period` | 종(전)근무기간 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:205 | 묻기 |
| `work_prev.salary` | 종(전)급여 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:62 · fields.json:210 | 묻기 |
| `work_sum.salary` | 급여합계 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:62 · fields.json:230 | 묻기 |
| `work_prev.bonus` | 종(전)상여 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:63 · fields.json:190 | 묻기 |
| `work_sum.bonus` | 상여합계 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:63 · fields.json:220 | 묻기 |
| `work_prev.total` | 종(전)계 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:215 | 묻기 |
| `work_sum.total` | 계합계 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:235 | 묻기 |
| `work_sum.meal` | 식사대합계 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:75 · fields.json:225 | 묻기 |
| `tax_prev.biz_no` | 종(전)근무지사업자등록번호 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:85 · fields.json:135 | 묻기 |
| `tax_prev.income` | 종(전)근무지기납부소득세 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:86 · fields.json:140 | 묻기 |
| `tax_prev.local` | 종(전)근무지기납부지방소득세 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:86 · fields.json:145 | 묻기 |
| `work.reduction_period` | 감면기간 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:170 | 묻기 |
| `nontax.reduction` | 감면소득계 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:78 · fields.json:50 | 묻기 |
| `work_prev.meal` | 종(전)식사대 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:75 · fields.json:200 | 묻기 |
| `nontax.childcare` | 출산·보육수당 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:73 · fields.json:40 | 묻기 |

## 체크·도장·서명 (marks) — 6칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `copy_type` | 보관용구분 | checkbox (소득자 보관용 / 발행자 보관용 / 발행자 보고용) | 1쪽 [404, 151, 485, 161] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:5 | 묻기 |
| `resident` | 거주구분 | checkbox (거주자1 / 비거주자2) | 1쪽 [760, 74, 797, 82] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:80 | 묻기 |
| `customer.nationality` ← `nationality` | 내·외국인 | checkbox (내국인1 / 외국인9) | 1쪽 [760, 103, 797, 111] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:35 | 묻기 |
| `household_head` | 세대주여부 | checkbox (세대주1 / 세대원2) | 1쪽 [760, 176, 797, 184] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:25 | 묻기 |
| `settlement_type` | 연말정산구분 | checkbox (계속근로1 / 중도퇴사2) | 1쪽 [760, 190, 807, 198] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:90 | 묻기 |
| `seal.customer` ← `seal.payer` | 징수의무자 | seal | 1쪽 [851, 774, 907, 814] | 늘 | 템플릿 | generate.py | fields.json:85 | 묻기 |

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
"근로소득 원천징수영수증"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2024",
 "주식회사 다온패션",
 "박정연",
 "123-88-81212",
 "부산광역시 해운대구 해운대로 326, 7층",
 "남궁예태",
 "850328-2489940",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "2024.01.01~2024.12.31",
 "39,940,000",
 "7,610,000",
 "47,550,000",
 "2,400,000",
 "2,132,740",
 "213,270",
 "2,497,560",
 "249,750",
 "-364,820",
 "-36,480",
 "4.5",
 "2025년 3월 3일",
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
"부산광역시 해운대구 해운대로 326, 7층"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)"
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
- year: 귀속연도
- work.hours: 총근로시간수
- customer.name: 법인명(상호) (고객 성명)
- customer.ceo: 대표자(성명) (고객 대표자)
- customer.biz_no: 사업자등록번호 (고객 사업자등록번호, 같은 항목명 중 1번째 칸)
- customer.address: 소재지(주소) (고객 주소)
- earner.name: 성명 (고객 본인의 성명)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- earner.address: 주소 (고객 본인의 주소)
- work.company: 근무처명
- work.biz_no: 사업자등록번호 (같은 항목명 중 2번째 칸)
- employer.period: 근무기간 (직장 재직기간)
- work.salary: 급여
- work.bonus: 상여
- work.total: 계
- official.issuer_phone: 증명발급자연락처
- nontax.meal: 식사대
- nontax.total: 비과세소득계
- tax.final_income: 결정세액 (같은 항목명 중 1번째 칸)
- tax.final_local: 결정세액 (같은 항목명 중 2번째 칸)
- tax.prepaid_income: 주(현)근무지 (같은 항목명 중 1번째 칸)
- tax.prepaid_local: 주(현)근무지 (같은 항목명 중 2번째 칸)
- tax.diff_income: 차감징수세액 (같은 항목명 중 1번째 칸)
- tax.diff_local: 차감징수세액 (같은 항목명 중 2번째 칸)
- tax.effective_rate: 실효세율(%)
- sum.total: 납부보험료(계)합계
- issue_date: 발급일
- tax_office: 세무서장
```

답:

```json
[{"key": "year", "value": "2024", "bbox_2d": [340, 168, 366, 178], "page": 1},
 {"key": "work.hours", "value": null},
 {"key": "customer.name", "value": "주식회사 다온패션", "bbox_2d": [282, 206, 385, 216], "page": 1},
 {"key": "customer.ceo", "value": "박정연", "bbox_2d": [667, 206, 704, 216], "page": 1},
 {"key": "customer.biz_no", "value": "123-88-81212", "bbox_2d": [282, 221, 353, 230], "page": 1},
 {"key": "customer.address", "value": "부산광역시 해운대구 해운대로 326, 7층", "bbox_2d": [282, 250, 497, 260], "page": 1},
 {"key": "earner.name", "value": "남궁예태", "bbox_2d": [282, 270, 332, 280], "page": 1},
 {"key": "customer.rrn", "value": "850328-2489940", "bbox_2d": [667, 270, 752, 280], "page": 1},
 {"key": "earner.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [282, 290, 711, 300], "page": 1},
 {"key": "work.company", "value": "주식회사 다온패션", "bbox_2d": [366, 321, 469, 331], "page": 1},
 {"key": "work.biz_no", "value": "123-88-81212", "bbox_2d": [382, 336, 453, 345], "page": 1},
 {"key": "employer.period", "value": "2024.01.01~2024.12.31", "bbox_2d": [364, 351, 471, 360], "page": 1},
 {"key": "work.salary", "value": "39,940,000", "bbox_2d": [435, 379, 491, 389], "page": 1},
 {"key": "work.bonus", "value": "7,610,000", "bbox_2d": [441, 394, 491, 404], "page": 1},
 {"key": "work.total", "value": "47,550,000", "bbox_2d": [435, 481, 491, 491], "page": 1},
 {"key": "official.issuer_phone", "value": null},
 {"key": "nontax.meal", "value": "2,400,000", "bbox_2d": [441, 559, 491, 569], "page": 1},
 {"key": "nontax.total", "value": "2,400,000", "bbox_2d": [441, 590, 491, 600], "page": 1},
 {"key": "tax.final_income", "value": "2,132,740", "bbox_2d": [644, 637, 694, 647], "page": 1},
 {"key": "tax.final_local", "value": "213,270", "bbox_2d": [762, 637, 803, 647], "page": 1},
 {"key": "tax.prepaid_income", "value": "2,497,560", "bbox_2d": [644, 678, 694, 688], "page": 1},
 {"key": "tax.prepaid_local", "value": "249,750", "bbox_2d": [762, 678, 803, 688], "page": 1},
 {"key": "tax.diff_income", "value": "-364,820", "bbox_2d": [650, 707, 694, 717], "page": 1},
 {"key": "tax.diff_local", "value": "-36,480", "bbox_2d": [765, 707, 803, 717], "page": 1},
 {"key": "tax.effective_rate", "value": "4.5", "bbox_2d": [886, 721, 902, 731], "page": 1},
 {"key": "sum.total", "value": null},
 {"key": "issue_date", "value": "2025년 3월 3일", "bbox_2d": [823, 760, 904, 770], "page": 1},
 {"key": "tax_office", "value": "해운대세무서장", "bbox_2d": [96, 818, 223, 832], "page": 1}]
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
- copy_type: 보관용구분 (체크박스, 보기: 소득자 보관용 / 발행자 보관용 / 발행자 보고용)
- resident: 거주구분 (체크박스, 보기: 거주자1 / 비거주자2)
- customer.nationality: 내·외국인 (고객 국적, 체크박스, 보기: 내국인1 / 외국인9)
- household_head: 세대주여부 (체크박스, 보기: 세대주1 / 세대원2)
- settlement_type: 연말정산구분 (체크박스, 보기: 계속근로1 / 중도퇴사2)
- seal.customer: 징수의무자 (고객 도장, 도장)
```

답:

```json
[{"key": "copy_type", "value": "발행자 보고용", "bbox_2d": [378, 151, 400, 161], "page": 1},
 {"key": "resident", "value": "거주자1", "bbox_2d": [740, 74, 757, 82], "page": 1},
 {"key": "customer.nationality", "value": "내국인1", "bbox_2d": [740, 103, 757, 111], "page": 1},
 {"key": "household_head", "value": "세대주1", "bbox_2d": [740, 176, 757, 184], "page": 1},
 {"key": "settlement_type", "value": "계속근로1", "bbox_2d": [740, 190, 757, 198], "page": 1},
 {"key": "seal.customer", "value": true, "bbox_2d": [851, 774, 907, 814], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa withholding_receipt --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check withholding_receipt` → `python -m docgen.formdir card withholding_receipt` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa withholding_receipt --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions withholding_receipt --show` · `python -m docgen.preview withholding_receipt --out work/withholding_receipt`
