# 표준재무제표증명 (`standard_financial_statement_proof`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card standard_financial_statement_proof · card-hash: 52b7d84ed074 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** business · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 표준재무제표증명
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 홈택스 발급 표준재무제표증명(개인): 표준재무상태표 + 표준손익계산서.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/business.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 68칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [72, 98, 200, 111] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:165 | 묻기 |
| `customer.trade_name` ← `taxpayer.trade_name` | 상호(법인명) | text | 1쪽 [283, 126, 344, 138] | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:215 | 묻기 |
| `customer.biz_no` ← `taxpayer.biz_no` | 사업자등록번호 | biz_no | 1쪽 [741, 126, 828, 138] | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:195 | 묻기 |
| `customer.name` ← `taxpayer.name` | 성명(대표자) | text | 1쪽 [283, 149, 344, 161] | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:205 | 묻기 |
| `customer.rrn` ← `taxpayer.rrn` | 주민(법인)등록번호 | rrn | 1쪽 [741, 149, 846, 161] | 늘 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:210 | 묻기 |
| `taxpayer.biz_type` | 업태 | text | 1쪽 [283, 171, 344, 184] | 늘 | 템플릿 | generate.py | look/template.html.j2:50 · fields.json:200 | 묻기 |
| `taxpayer.biz_item` | 종목 | text | 1쪽 [741, 171, 818, 184] | 늘 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:190 | 묻기 |
| `customer.address` ← `taxpayer.address` | 사업장 | text | 1쪽 [283, 194, 677, 206] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:185 | 묻기 |
| `period` | 사업연도 | text | 1쪽 [283, 217, 437, 229] | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:175 | 묻기 |
| `filing_kind` | 신고구분 | text | 1쪽 [741, 217, 803, 229] | 늘 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:90 | 묻기 |
| `attachments` | 첨부서류 | text | 1쪽 [283, 239, 505, 252] | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:5 | 묻기 |
| `filed_date` | 신고일 | date | 1쪽 [741, 239, 810, 252] | 늘 | 템플릿 | generate.py | look/template.html.j2:56 · fields.json:85 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [437, 295, 563, 308] | 늘 | 템플릿 | generate.py | look/template.html.j2:59 · fields.json:160 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [374, 320, 603, 341] | 늘 | 템플릿 | generate.py | look/template.html.j2:59 · fields.json:170 | 묻기 |
| `balance_sheet.current` | 유동자산 | amount | 1쪽 [406, 444, 485, 456] | 늘 | 템플릿 | generate.py | fields.json:20 | 묻기 |
| `balance_sheet.quick` | 당좌자산 | number | 1쪽 [413, 465, 485, 478] | 늘 | 템플릿 | generate.py | fields.json:75 | 묻기 |
| `balance_sheet.inventory` | 재고자산 | number | 1쪽 [414, 487, 485, 499] | 늘 | 템플릿 | generate.py | fields.json:40 | 묻기 |
| `balance_sheet.noncurrent` | 비유동자산 | amount | 1쪽 [405, 508, 485, 520] | 늘 | 템플릿 | generate.py | fields.json:60 | 묻기 |
| `balance_sheet.investment` | 투자자산 | number | 1쪽 [413, 530, 485, 542] | 늘 | 템플릿 | generate.py | fields.json:45 | 묻기 |
| `balance_sheet.tangible` | 유형자산 | number | 1쪽 [413, 551, 485, 563] | 늘 | 템플릿 | generate.py | fields.json:80 | 묻기 |
| `balance_sheet.intangible` | 무형자산 | number | 1쪽 [421, 573, 485, 585] | 늘 | 템플릿 | generate.py | fields.json:35 | 묻기 |
| `balance_sheet.other_noncurrent` | 기타비유동자산 | amount | 1쪽 [413, 594, 485, 607] | 늘 | 템플릿 | generate.py | fields.json:70 | 묻기 |
| `balance_sheet.assets` | 자산총계 | amount | 1쪽 [405, 615, 485, 628] | 늘 | 템플릿 | generate.py | fields.json:10 | 묻기 |
| `balance_sheet.current_liab` | 유동부채 | amount | 1쪽 [413, 637, 485, 650] | 늘 | 템플릿 | generate.py | fields.json:25 | 묻기 |
| `balance_sheet.noncurrent_liab` | 비유동부채 | amount | 1쪽 [413, 659, 485, 671] | 늘 | 템플릿 | generate.py | fields.json:65 | 묻기 |
| `balance_sheet.liabilities` | 부채총계 | amount | 1쪽 [413, 680, 485, 693] | 늘 | 템플릿 | generate.py | fields.json:55 | 묻기 |
| `balance_sheet.capital` | 자본금 | amount | 1쪽 [405, 702, 485, 714] | 늘 | 템플릿 | generate.py | fields.json:15 | 묻기 |
| `balance_sheet.equity` | 자본총계 | amount | 1쪽 [405, 723, 485, 736] | 늘 | 템플릿 | generate.py | fields.json:30 | 묻기 |
| `balance_sheet.liab_equity` | 부채와자본총계 | amount | 1쪽 [405, 745, 485, 757] | 늘 | 템플릿 | generate.py | fields.json:50 | 묻기 |
| `income_statement.revenue` | 매출액 | amount | 1쪽 [845, 444, 924, 456] | 늘 | 템플릿 | generate.py | fields.json:140 | 묻기 |
| `income_statement.cogs` | 매출원가 | number | 1쪽 [845, 465, 924, 478] | 늘 | 템플릿 | generate.py | fields.json:95 | 묻기 |
| `income_statement.gross` | 매출총이익 | number | 1쪽 [845, 487, 924, 499] | 늘 | 템플릿 | generate.py | fields.json:105 | 묻기 |
| `income_statement.sga` | 판매비와관리비 | number | 1쪽 [845, 508, 924, 520] | 늘 | 템플릿 | generate.py | fields.json:150 | 묻기 |
| `income_statement.salary` | 급여 | amount | 1쪽 [845, 530, 924, 542] | 늘 | 템플릿 | generate.py | fields.json:145 | 묻기 |
| `income_statement.welfare` | 복리후생비 | number | 1쪽 [853, 551, 924, 563] | 늘 | 템플릿 | generate.py | fields.json:155 | 묻기 |
| `income_statement.rent` | 임차료 / 지급임차료 | amount | 1쪽 [853, 573, 924, 585] | 늘 | 템플릿 | generate.py | fields.json:135 | 묻기 |
| `income_statement.depreciation` | 감가상각비 | number | 1쪽 [853, 594, 924, 607] | 늘 | 템플릿 | generate.py | fields.json:100 | 묻기 |
| `income_statement.other_sga` | 기타판매비와관리비 | number | 1쪽 [853, 615, 924, 628] | 12/16 | 템플릿 | generate.py | fields.json:130 | 묻기 |
| `income_statement.op` | 영업이익 | number | 1쪽 [853, 637, 924, 650] | 늘 | 템플릿 | generate.py | fields.json:125 | 묻기 |
| `income_statement.non_op_income` | 영업외수익 | amount | 1쪽 [860, 659, 924, 671] | 늘 | 템플릿 | generate.py | fields.json:120 | 묻기 |
| `income_statement.non_op_expense` | 영업외비용 | amount | 1쪽 [860, 680, 924, 693] | 늘 | 템플릿 | generate.py | fields.json:115 | 묻기 |
| `income_statement.net` | 당기순이익 | number | 1쪽 [853, 702, 924, 714] | 늘 | 템플릿 | generate.py | fields.json:110 | 묻기 |
| `bs_accounts.quick.*.account` | 계정과목 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:320 | 묻기 |
| `bs_accounts.quick.*.amount` | 금액 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:325 | 묻기 |
| `bs_accounts.inventory.*.account` | 계정과목 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:260 | 묻기 |
| `bs_accounts.inventory.*.amount` | 금액 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:265 | 묻기 |
| `bs_accounts.investment.*.account` | 계정과목 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:275 | 묻기 |
| `bs_accounts.investment.*.amount` | 금액 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:280 | 묻기 |
| `bs_accounts.tangible.*.account` | 계정과목 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:335 | 묻기 |
| `bs_accounts.tangible.*.amount` | 금액 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:340 | 묻기 |
| `bs_accounts.intangible.*.account` | 계정과목 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:245 | 묻기 |
| `bs_accounts.intangible.*.amount` | 금액 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:250 | 묻기 |
| `bs_accounts.other_noncurrent.*.account` | 계정과목 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:305 | 묻기 |
| `bs_accounts.other_noncurrent.*.amount` | 금액 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:310 | 묻기 |
| `bs_accounts.current_liab.*.account` | 계정과목 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:230 | 묻기 |
| `bs_accounts.current_liab.*.amount` | 금액 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:235 | 묻기 |
| `bs_accounts.noncurrent_liab.*.account` | 계정과목 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:290 | 묻기 |
| `bs_accounts.noncurrent_liab.*.amount` | 금액 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:295 | 묻기 |
| `pl_accounts.revenue.*.account` | 계정과목 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:395 | 묻기 |
| `pl_accounts.revenue.*.amount` | 금액 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:400 | 묻기 |
| `pl_accounts.cogs.*.account` | 계정과목 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:350 | 묻기 |
| `pl_accounts.cogs.*.amount` | 금액 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:355 | 묻기 |
| `pl_accounts.sga.*.account` | 계정과목 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:101 · fields.json:410 | 묻기 |
| `pl_accounts.sga.*.amount` | 금액 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:101 · fields.json:415 | 묻기 |
| `pl_accounts.non_op_income.*.account` | 계정과목 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:380 | 묻기 |
| `pl_accounts.non_op_income.*.amount` | 금액 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:385 | 묻기 |
| `pl_accounts.non_op_expense.*.account` | 계정과목 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:365 | 묻기 |
| `pl_accounts.non_op_expense.*.amount` | 금액 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:370 | 묻기 |

## 체크·도장·서명 (marks) — 2칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `taxpayer_type` | 개인/법인 | checkbox (개인 / 법인) | 1쪽 [494, 98, 526, 111] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:220 | 묻기 |
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [591, 299, 681, 362] | 늘 | 템플릿 | generate.py | fields.json:180 | 묻기 |

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
"표준재무제표증명"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "7374-861-5557-188",
 "새한커피",
 "133-64-53148",
 "남궁예태",
 "850328-2******",
 "음식점업",
 "커피전문점",
 "부산광역시 해운대구 좌동순환로 237, 7층 (우동, 케이타워)",
 "2023.01.01 ~ 2023.12.31",
 "정기신고",
 "표준재무상태표, 표준손익계산서",
 "2024.05.30",
 "2025년 04월 01일",
 "해운대세무서장",
 "116,831,009",
 "91,720,364",
 "25,110,645",
 "100,844,919",
 "10,829,497",
 "58,142,617",
 "3,857,297",
 "28,015,508",
 "217,675,928",
 "59,978,958",
 "30,645,463",
 "90,624,421",
 "127,051,507",
 "555,295,870",
 "207,099,214",
 "348,196,656",
 "274,422,342",
 "145,138,240",
 "17,416,580",
 "41,438,980",
 "20,651,820",
 "49,776,722",
 "73,774,314",
 "1,099,585",
 "9,308,540",
 "65,565,359"
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
"25,110,645"
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
- customer.trade_name: 상호(법인명) (고객 상호)
- customer.biz_no: 사업자등록번호 (고객 사업자등록번호)
- customer.name: 성명(대표자) (고객 성명)
- taxpayer.biz_type: 업태
- taxpayer.biz_item: 종목
- customer.address: 사업장 (고객 주소)
- period: 사업연도
- filing_kind: 신고구분
- attachments: 첨부서류
- filed_date: 신고일
- issue_date: 발급일
- issuer: 발급기관
- balance_sheet.current: 유동자산
- balance_sheet.quick: 당좌자산
- balance_sheet.inventory: 재고자산
- balance_sheet.noncurrent: 비유동자산
- balance_sheet.investment: 투자자산
- balance_sheet.tangible: 유형자산
- balance_sheet.intangible: 무형자산
- balance_sheet.other_noncurrent: 기타비유동자산
- balance_sheet.assets: 자산총계
- balance_sheet.current_liab: 유동부채
- balance_sheet.noncurrent_liab: 비유동부채
- balance_sheet.liabilities: 부채총계
- balance_sheet.capital: 자본금
- balance_sheet.equity: 자본총계
- balance_sheet.liab_equity: 부채와자본총계
- income_statement.revenue: 매출액
- income_statement.cogs: 매출원가
- income_statement.gross: 매출총이익
- income_statement.sga: 판매비와관리비
- income_statement.salary: 급여
- income_statement.rent: 임차료
- income_statement.depreciation: 감가상각비
- income_statement.other_sga: 기타판매비와관리비
- income_statement.op: 영업이익
- income_statement.non_op_income: 영업외수익
- income_statement.non_op_expense: 영업외비용
- income_statement.net: 당기순이익
```

답:

```json
[{"key": "issue_no", "value": "7374-861-5557-188", "bbox_2d": [72, 98, 200, 111], "page": 1},
 {"key": "customer.trade_name", "value": "새한커피", "bbox_2d": [283, 126, 344, 138], "page": 1},
 {"key": "customer.biz_no", "value": "133-64-53148", "bbox_2d": [741, 126, 828, 138], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [283, 149, 344, 161], "page": 1},
 {"key": "taxpayer.biz_type", "value": "음식점업", "bbox_2d": [283, 171, 344, 184], "page": 1},
 {"key": "taxpayer.biz_item", "value": "커피전문점", "bbox_2d": [741, 171, 818, 184], "page": 1},
 {"key": "customer.address", "value": "부산광역시 해운대구 좌동순환로 237, 7층 (우동, 케이타워)", "bbox_2d": [283, 194, 677, 206], "page": 1},
 {"key": "period", "value": "2023.01.01 ~ 2023.12.31", "bbox_2d": [283, 217, 437, 229], "page": 1},
 {"key": "filing_kind", "value": "정기신고", "bbox_2d": [741, 217, 803, 229], "page": 1},
 {"key": "attachments", "value": "표준재무상태표, 표준손익계산서", "bbox_2d": [283, 239, 505, 252], "page": 1},
 {"key": "filed_date", "value": "2024.05.30", "bbox_2d": [741, 239, 810, 252], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [437, 295, 563, 308], "page": 1},
 {"key": "issuer", "value": "해운대세무서장", "bbox_2d": [374, 320, 603, 341], "page": 1},
 {"key": "balance_sheet.current", "value": "116,831,009", "bbox_2d": [406, 444, 485, 456], "page": 1},
 {"key": "balance_sheet.quick", "value": "91,720,364", "bbox_2d": [413, 465, 485, 478], "page": 1},
 {"key": "balance_sheet.inventory", "value": "25,110,645", "bbox_2d": [414, 487, 485, 499], "page": 1},
 {"key": "balance_sheet.noncurrent", "value": "100,844,919", "bbox_2d": [405, 508, 485, 520], "page": 1},
 {"key": "balance_sheet.investment", "value": "10,829,497", "bbox_2d": [413, 530, 485, 542], "page": 1},
 {"key": "balance_sheet.tangible", "value": "58,142,617", "bbox_2d": [413, 551, 485, 563], "page": 1},
 {"key": "balance_sheet.intangible", "value": "3,857,297", "bbox_2d": [421, 573, 485, 585], "page": 1},
 {"key": "balance_sheet.other_noncurrent", "value": "28,015,508", "bbox_2d": [413, 594, 485, 607], "page": 1},
 {"key": "balance_sheet.assets", "value": "217,675,928", "bbox_2d": [405, 615, 485, 628], "page": 1},
 {"key": "balance_sheet.current_liab", "value": "59,978,958", "bbox_2d": [413, 637, 485, 650], "page": 1},
 {"key": "balance_sheet.noncurrent_liab", "value": "30,645,463", "bbox_2d": [413, 659, 485, 671], "page": 1},
 {"key": "balance_sheet.liabilities", "value": "90,624,421", "bbox_2d": [413, 680, 485, 693], "page": 1},
 {"key": "balance_sheet.capital", "value": "127,051,507", "bbox_2d": [405, 702, 485, 714], "page": 1},
 {"key": "balance_sheet.equity", "value": "127,051,507", "bbox_2d": [405, 723, 485, 736], "page": 1},
 {"key": "balance_sheet.liab_equity", "value": "217,675,928", "bbox_2d": [405, 745, 485, 757], "page": 1},
 {"key": "income_statement.revenue", "value": "555,295,870", "bbox_2d": [845, 444, 924, 456], "page": 1},
 {"key": "income_statement.cogs", "value": "207,099,214", "bbox_2d": [845, 465, 924, 478], "page": 1},
 {"key": "income_statement.gross", "value": "348,196,656", "bbox_2d": [845, 487, 924, 499], "page": 1},
 {"key": "income_statement.sga", "value": "274,422,342", "bbox_2d": [845, 508, 924, 520], "page": 1},
 {"key": "income_statement.salary", "value": "145,138,240", "bbox_2d": [845, 530, 924, 542], "page": 1},
 {"key": "income_statement.rent", "value": "41,438,980", "bbox_2d": [853, 573, 924, 585], "page": 1},
 {"key": "income_statement.depreciation", "value": "20,651,820", "bbox_2d": [853, 594, 924, 607], "page": 1},
 {"key": "income_statement.other_sga", "value": "49,776,722", "bbox_2d": [853, 615, 924, 628], "page": 1},
 {"key": "income_statement.op", "value": "73,774,314", "bbox_2d": [853, 637, 924, 650], "page": 1},
 {"key": "income_statement.non_op_income", "value": "1,099,585", "bbox_2d": [860, 659, 924, 671], "page": 1},
 {"key": "income_statement.non_op_expense", "value": "9,308,540", "bbox_2d": [860, 680, 924, 693], "page": 1},
 {"key": "income_statement.net", "value": "65,565,359", "bbox_2d": [853, 702, 924, 714], "page": 1}]
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
- taxpayer_type: 개인/법인 (체크박스, 보기: 개인 / 법인)
- seal.issuer: 발급기관직인 (도장)
```

답:

```json
[{"key": "taxpayer_type", "value": "개인", "bbox_2d": [481, 98, 490, 111], "page": 1},
 {"key": "seal.issuer", "value": true, "bbox_2d": [591, 299, 681, 362], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check standard_financial_statement_proof` → `python -m docgen.formdir card standard_financial_statement_proof` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions standard_financial_statement_proof --show` · `python -m docgen.preview standard_financial_statement_proof --out work/standard_financial_statement_proof`
