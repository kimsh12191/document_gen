# 기업여신 신청서 (`loan_application_corp`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card loan_application_corp · card-hash: e90b73ad711b -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 기업여신 신청서 (다른 이름: 융자상담 및 차입신청서(기업용))
- **쓰이는 업무:** 법인 여신
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa loan_application_corp --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 법인 고객 기업여신 신청서 (은행 자체 서식).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 36칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank` | 은행명 | text | 1쪽 [99, 39, 193, 61] | 늘 | 템플릿 | generate.py | fields.json:30 | 묻기 |
| `branch` | 취급점 | text | 1쪽 [648, 130, 703, 141] | 늘 | 템플릿 | generate.py | look/template.html.j2:11 · fields.json:35 | 묻기 |
| `corp.name` ← `company.name` | 기업명 | text | 1쪽 [207, 173, 302, 183] | 늘 | 템플릿 | generate.py | look/template.html.j2:16 · fields.json:85 | 묻기 |
| `corp.name_en` ← `company.name_en` | 영문명 | text | - | 늘 | 템플릿 | generate.py | look/template.html.j2:16 · fields.json:90 | 묻기 |
| `corp.biz_no` ← `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [207, 193, 288, 203] | 늘 | 템플릿 | generate.py | look/template.html.j2:17 · fields.json:45 | 묻기 |
| `corp.corp_reg_no` ← `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 1쪽 [646, 193, 744, 203] | 늘 | 템플릿 | generate.py | fields.json:60 | 묻기 |
| `corp.ceo` ← `company.ceo` | 대표자 | text | 1쪽 [207, 213, 264, 223] | 늘 | 템플릿 | generate.py | look/template.html.j2:18 · fields.json:55 | 묻기 |
| `corp.established` ← `company.established` | 설립일 | date | 1쪽 [646, 213, 711, 223] | 늘 | 템플릿 | generate.py | look/template.html.j2:18 · fields.json:70 | 묻기 |
| `corp.industry` ← `company.industry` | 업태/종목 | text | 1쪽 [207, 233, 318, 243] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:80 | 묻기 |
| `company.employees` | 종업원수 | text | - | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:65 | 묻기 |
| `company.capital` | 자본금 | amount | 1쪽 [296, 272, 382, 283] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:50 | 묻기 |
| `company.revenue` | 매출액 | amount | 1쪽 [646, 277, 750, 287] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:100 | 묻기 |
| `company.revenue_year` | 결산연도 | text | 1쪽 [758, 277, 800, 287] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:105 | 묻기 |
| `corp.address` ← `company.address` | 본점소재지 | text | 1쪽 [207, 301, 615, 311] | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:40 | 묻기 |
| `corp.phone` ← `company.phone` | 전화번호 | phone | 1쪽 [207, 321, 288, 331] | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:95 | 묻기 |
| `company.fax` | 팩스번호 | phone | - | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:75 | 묻기 |
| `contact.name` | 담당자 | text | 1쪽 [207, 367, 250, 377] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:120 | 묻기 |
| `contact.position` | 부서/직위 | text | 1쪽 [258, 367, 362, 377] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:130 | 묻기 |
| `contact.phone` | 연락처 | phone | 1쪽 [521, 367, 610, 377] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:125 | 묻기 |
| `contact.email` | E-mail | text | 1쪽 [761, 367, 881, 377] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:115 | 묻기 |
| `loan.product` | 상품명 | text | 1쪽 [207, 432, 321, 443] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:170 | 묻기 |
| `loan.amount_korean` | 신청금액(한글) | amount_korean | 1쪽 [207, 452, 311, 463] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:140 | 묻기 |
| `loan.amount` | 신청금액 | amount | 1쪽 [323, 452, 419, 463] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:135 | 묻기 |
| `loan.term` | 여신기간 | text | 1쪽 [207, 472, 257, 483] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:195 | 묻기 |
| `loan.hope_date` | 대출희망일 | date | 1쪽 [647, 472, 712, 483] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:165 | 묻기 |
| `loan.repayment` | 상환방법 | text | 1쪽 [207, 492, 422, 503] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:185 | 묻기 |
| `loan.purpose` | 자금용도 | text | 1쪽 [443, 512, 533, 523] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:175 | 묻기 |
| `loan.deposit_account` | 대출금입금계좌 | account_no | 1쪽 [207, 532, 368, 543] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:155 | 묻기 |
| `loan.collateral_detail` | 담보/보증내용 | text | 1쪽 [207, 572, 447, 583] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:150 | 묻기 |
| `other_loans_total` | 합계 | amount | 1쪽 [663, 873, 697, 885] | 4/16 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:200 | 묻기 |
| `apply_date` | 신청일 | date | 2쪽 [72, 82, 165, 93] | 늘 | 템플릿 | generate.py | look/template.html.j2:72 · fields.json:25 | 묻기 |
| `signature` | 대표이사 | text | 2쪽 [808, 99, 878, 112] | 늘 | 템플릿 | generate.py | look/template.html.j2:7 · fields.json:220 | 묻기 |
| `agent.name` | 대리인성명 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:5 | 묻기 |
| `agent.position` | 대리인직위 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:15 | 묻기 |
| `agent.rrn` | 대리인실명번호 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:20 | 묻기 |
| `agent.phone` | 대리인연락처 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:62 · fields.json:10 | 묻기 |

## 표 `other_loans` (표 과제 table·table_read·table_find·table_qa) — 4열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `other_loans.*.lender` | 금융기관 | text | 1쪽 [146, 638, 221, 651] (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:245 | 묻기 |
| `other_loans.*.kind` | 여신종류 | text | 1쪽 [370, 638, 459, 651] (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:240 | 묻기 |
| `other_loans.*.balance` | 잔액 | amount | 1쪽 [675, 638, 697, 651] (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:230 | 묻기 |
| `other_loans.*.collateral` | 담보 | text | 1쪽 [801, 638, 831, 651] (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:235 | 묻기 |

## 체크·도장·서명 (marks) — 8칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `company.size` | 기업규모 | checkbox (대기업 / 중견기업 / 중소기업 / 소상공인) | 1쪽 [369, 253, 426, 263] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:110 | 묻기 |
| `loan.subject` | 여신과목 | checkbox (일반자금대출 / 시설자금대출 / 한도대출) | 1쪽 [330, 412, 416, 423] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:190 | 묻기 |
| `loan.rate_type` | 금리종류 | checkbox (고정금리 / 변동금리) | 1쪽 [647, 432, 812, 443] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:180 | 묻기 |
| `loan.fund_type` | 자금구분 | checkbox (운전자금 / 시설자금) | 1쪽 [301, 512, 358, 523] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:160 | 묻기 |
| `loan.collateral` | 담보구분 | checkbox (신용 / 부동산 / 보증서 / 예·적금) | 1쪽 [340, 552, 383, 563] | 늘 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:145 | 묻기 |
| `seal.corp` | 법인인감 | seal | 2쪽 [861, 75, 952, 139] | 늘 | 템플릿 | generate.py | fields.json:210 | 묻기 |
| `seal.agent` | 대리인 | 도장 | - | 2/16 | 템플릿 | generate.py | fields.json:205 | 묻기 |
| `sign.agent` | 대리인 | 서명 | - | 2/16 | 템플릿 | generate.py | fields.json:215 | 묻기 |

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
"기업여신 신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "국민은행",
 "센텀지점",
 "(주)미래케미칼",
 "702-81-38348",
 "200112-7951835",
 "남궁예태",
 "2020.06.15",
 "제조업 / 화학제품",
 "300,000,000원",
 "73,589,000,000원",
 "2024년",
 "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)",
 "064-756-8800",
 "방훈원",
 "경영지원팀 차장",
 "010-8349-3877",
 "contact@mirae.co.kr",
 "기업시설자금대출",
 "금 이십일억원정",
 "2,100,000,000원",
 "120개월",
 "2025.04.14",
 "2년 거치 후 8년 원금균등분할상환",
 "공장 신축자금",
 "국민은행 129-04-3353-660",
 "기술보증기금 보증서 (보증비율 100%)",
 "수출입은행",
 "운전자금대출",
 "800",
 "신용",
 "신한은행",
 "480",
 "부동산",
 "현대캐피탈",
 "당좌대출",
 "160",
 "SC제일은행",
 "할인어음",
 "230",
 "예금",
 "시설자금대출",
 "960",
 "신용보증기금",
 "구매자금대출",
 "580",
 "기술보증기금",
 "우리은행",
 "팩토링",
 "1,470",
 "760",
 "iM뱅크",
 "1,320",
 "부산은행",
 "무역금융",
 "750",
 "농협은행",
 "수입신용장(L/C)",
 "1,330",
 "8,840",
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
"공장 신축자금"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"부동산"
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
- bank: 은행명
- branch: 취급점
- corp.name: 기업명 (법인·사업자 상호)
- corp.name_en: 영문명 (법인·사업자 영문 상호)
- corp.biz_no: 사업자등록번호 (법인·사업자 사업자등록번호)
- corp.corp_reg_no: 법인등록번호 (법인·사업자 법인등록번호)
- corp.ceo: 대표자 (법인·사업자 대표자)
- corp.established: 설립일 (법인·사업자 설립일)
- corp.industry: 업태/종목 (법인·사업자 업태·종목)
- company.employees: 종업원수
- company.capital: 자본금
- company.revenue: 매출액
- company.revenue_year: 결산연도
- corp.address: 본점소재지 (법인·사업자 주소)
- corp.phone: 전화번호 (법인·사업자 연락처)
- loan.prepay_fee: 중도상환해약금
- company.fax: 팩스번호
- contact.name: 담당자
- contact.position: 부서/직위
- contact.phone: 연락처
- contact.email: E-mail
- loan.product: 상품명
- loan.amount_korean: 신청금액(한글)
- loan.amount: 신청금액
- loan.term: 여신기간
- loan.hope_date: 대출희망일
- loan.repayment: 상환방법
- loan.purpose: 자금용도
- loan.deposit_account: 대출금입금계좌
- loan.collateral_detail: 담보/보증내용
- other_loans_total: 합계
- apply_date: 신청일
- signature: 대표이사
```

답:

```json
[{"key": "bank", "value": "국민은행", "bbox_2d": [99, 39, 193, 61], "page": 1},
 {"key": "branch", "value": "센텀지점", "bbox_2d": [648, 130, 703, 141], "page": 1},
 {"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [207, 173, 302, 183], "page": 1},
 {"key": "corp.name_en", "value": null},
 {"key": "corp.biz_no", "value": "702-81-38348", "bbox_2d": [207, 193, 288, 203], "page": 1},
 {"key": "corp.corp_reg_no", "value": "200112-7951835", "bbox_2d": [646, 193, 744, 203], "page": 1},
 {"key": "corp.ceo", "value": "남궁예태", "bbox_2d": [207, 213, 264, 223], "page": 1},
 {"key": "corp.established", "value": "2020.06.15", "bbox_2d": [646, 213, 711, 223], "page": 1},
 {"key": "corp.industry", "value": "제조업 / 화학제품", "bbox_2d": [207, 233, 318, 243], "page": 1},
 {"key": "company.employees", "value": null},
 {"key": "company.capital", "value": "300,000,000원", "bbox_2d": [296, 272, 382, 283], "page": 1},
 {"key": "company.revenue", "value": "73,589,000,000원", "bbox_2d": [646, 277, 750, 287], "page": 1},
 {"key": "company.revenue_year", "value": "2024년", "bbox_2d": [758, 277, 800, 287], "page": 1},
 {"key": "corp.address", "value": "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)", "bbox_2d": [207, 301, 615, 311], "page": 1},
 {"key": "corp.phone", "value": "064-756-8800", "bbox_2d": [207, 321, 288, 331], "page": 1},
 {"key": "loan.prepay_fee", "value": null},
 {"key": "company.fax", "value": null},
 {"key": "contact.name", "value": "방훈원", "bbox_2d": [207, 367, 250, 377], "page": 1},
 {"key": "contact.position", "value": "경영지원팀 차장", "bbox_2d": [258, 367, 362, 377], "page": 1},
 {"key": "contact.phone", "value": "010-8349-3877", "bbox_2d": [521, 367, 610, 377], "page": 1},
 {"key": "contact.email", "value": "contact@mirae.co.kr", "bbox_2d": [761, 367, 881, 377], "page": 1},
 {"key": "loan.product", "value": "기업시설자금대출", "bbox_2d": [207, 432, 321, 443], "page": 1},
 {"key": "loan.amount_korean", "value": "금 이십일억원정", "bbox_2d": [207, 452, 311, 463], "page": 1},
 {"key": "loan.amount", "value": "2,100,000,000원", "bbox_2d": [323, 452, 419, 463], "page": 1},
 {"key": "loan.term", "value": "120개월", "bbox_2d": [207, 472, 257, 483], "page": 1},
 {"key": "loan.hope_date", "value": "2025.04.14", "bbox_2d": [647, 472, 712, 483], "page": 1},
 {"key": "loan.repayment", "value": "2년 거치 후 8년 원금균등분할상환", "bbox_2d": [207, 492, 422, 503], "page": 1},
 {"key": "loan.purpose", "value": "공장 신축자금", "bbox_2d": [443, 512, 533, 523], "page": 1},
 {"key": "loan.deposit_account", "value": "국민은행 129-04-3353-660", "bbox_2d": [207, 532, 368, 543], "page": 1},
 {"key": "loan.collateral_detail", "value": "기술보증기금 보증서 (보증비율 100%)", "bbox_2d": [207, 572, 447, 583], "page": 1},
 {"key": "other_loans_total", "value": "8,840", "bbox_2d": [663, 873, 697, 885], "page": 1},
 {"key": "apply_date", "value": "2025년 4월 1일", "bbox_2d": [72, 82, 165, 93], "page": 2},
 {"key": "signature", "value": "남궁예태", "bbox_2d": [808, 99, 878, 112], "page": 2}]
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
- company.size: 기업규모 (체크박스, 보기: 대기업 / 중견기업 / 중소기업 / 소상공인)
- loan.subject: 여신과목 (체크박스, 보기: 일반자금대출 / 시설자금대출 / 한도대출)
- loan.rate_type: 금리종류 (체크박스, 보기: 고정금리 / 변동금리)
- loan.fund_type: 자금구분 (체크박스, 보기: 운전자금 / 시설자금)
- loan.collateral: 담보구분 (체크박스, 보기: 신용 / 부동산 / 보증서 / 예·적금)
- seal.corp: 법인인감 (법인·사업자 도장, 도장)
```

답:

```json
[{"key": "company.size", "value": "중소기업", "bbox_2d": [357, 253, 365, 263], "page": 1},
 {"key": "loan.subject", "value": "시설자금대출", "bbox_2d": [318, 412, 326, 423], "page": 1},
 {"key": "loan.rate_type", "value": null},
 {"key": "loan.fund_type", "value": "시설자금", "bbox_2d": [289, 512, 297, 523], "page": 1},
 {"key": "loan.collateral", "value": "보증서", "bbox_2d": [328, 552, 337, 563], "page": 1},
 {"key": "seal.corp", "value": true, "bbox_2d": [861, 75, 952, 139], "page": 2}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[72, 614, 928, 865] 위치의 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 항목명)
- lender: 금융기관
- kind: 여신종류
- balance: 잔액
- collateral: 담보
```

답:

```json
{
 "columns": [
  "lender",
  "kind",
  "balance",
  "collateral"
 ],
 "rows": [
  [
   "수출입은행",
   "운전자금대출",
   "800",
   "신용"
  ],
  [
   "신한은행",
   "운전자금대출",
   "480",
   "부동산"
  ],
  [
   "현대캐피탈",
   "당좌대출",
   "160",
   "부동산"
  ],
  [
   "SC제일은행",
   "할인어음",
   "230",
   "예금"
  ],
  [
   "수출입은행",
   "시설자금대출",
   "960",
   "신용보증기금"
  ],
  [
   "신한은행",
   "구매자금대출",
   "580",
   "기술보증기금"
  ],
  [
   "우리은행",
   "팩토링",
   "1,470",
   "신용"
  ],
  [
   "신한은행",
   "팩토링",
   "760",
   "신용보증기금"
  ],
  [
   "iM뱅크",
   "당좌대출",
   "1,320",
   "예금"
  ],
  [
   "부산은행",
   "무역금융",
   "750",
   "부동산"
  ],
  [
   "농협은행",
   "수입신용장(L/C)",
   "1,330",
   "부동산"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    146,
    638,
    831,
    651
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    154,
    659,
    839,
    671
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    146,
    679,
    839,
    692
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    144,
    700,
    831,
    712
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    146,
    720,
    861,
    733
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    154,
    741,
    861,
    754
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    154,
    762,
    831,
    774
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    154,
    782,
    861,
    795
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    160,
    803,
    831,
    815
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    154,
    823,
    839,
    840
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    154,
    852,
    839,
    865
   ],
   "page": 1
  }
 ]
}
```

### 표 찾기 `table_find` · 채점 f1_iou50 (위치)

질문:

```
이 문서에서 표를 모두 찾아 JSON 목록으로 답하세요. 여기서 표는 같은 항목 묶음(열)이 행마다 되풀이되고 행 수가 서류마다 달라지는 목록입니다. 항목명과 값이 번갈아 있는 신청서 칸, 칸 수가 정해진 결재란은 표가 아닙니다.
표마다 {{"columns": [머리글 글자, …], "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호, "n_rows": 행 수}} 를 쓰고, 여러 쪽에 걸친 표는 쪽마다 따로 씁니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 행 수에는 머리글·합계 행과 모두 빈 행을 넣지 않습니다. 표가 없으면 [] 로 답하세요.
```

답:

```json
[{"columns": ["금융기관", "여신종류", "잔액", "담보"], "bbox_2d": [72, 614, 928, 865], "page": 1, "n_rows": 11}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 표를 보고 답하세요. 위에서 5번째 행의 '여신종류' 값은 무엇입니까? 머리글은 세지 않습니다. (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"시설자금대출"
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 표를 보고 답하세요. '담보' 칸이 '부동산'인 행은 몇 개입니까? (숫자만 답하세요)
```

답:

```json
4
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa loan_application_corp --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check loan_application_corp` → `python -m docgen.formdir card loan_application_corp` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa loan_application_corp --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions loan_application_corp --show` · `python -m docgen.preview loan_application_corp --out work/loan_application_corp`
