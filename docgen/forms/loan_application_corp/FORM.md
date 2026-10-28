# 기업여신 신청서 (`loan_application_corp`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card loan_application_corp · card-hash: 4417a8d2bfdc -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 기업여신 신청서 (다른 이름: 융자상담 및 차입신청서(기업용))
- **쓰이는 업무:** 법인 여신
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 법인 고객 기업여신 신청서 (은행 자체 서식).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 40칸

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
| `other_loans.*.lender` | 금융기관 | text | 1쪽 [146, 638, 221, 651] (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:245 | 묻기 |
| `other_loans.*.kind` | 여신종류 | text | 1쪽 [370, 638, 459, 651] (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:240 | 묻기 |
| `other_loans.*.balance` | 잔액 | amount | 1쪽 [675, 638, 697, 651] (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:230 | 묻기 |
| `other_loans.*.collateral` | 담보 | text | 1쪽 [801, 638, 831, 651] (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:235 | 묻기 |
| `other_loans_total` | 합계 | amount | 1쪽 [663, 873, 697, 885] | 4/16 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:200 | 묻기 |
| `apply_date` | 신청일 | date | 2쪽 [72, 82, 165, 93] | 늘 | 템플릿 | generate.py | look/template.html.j2:72 · fields.json:25 | 묻기 |
| `signature` | 대표이사 | text | 2쪽 [808, 99, 878, 112] | 늘 | 템플릿 | generate.py | look/template.html.j2:7 · fields.json:220 | 묻기 |
| `agent.name` | 대리인성명 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:5 | 묻기 |
| `agent.position` | 대리인직위 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:15 | 묻기 |
| `agent.rrn` | 대리인실명번호 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:20 | 묻기 |
| `agent.phone` | 대리인연락처 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:62 · fields.json:10 | 묻기 |

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

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- bank: 은행명
- corp.name: 기업명 (법인·사업자 상호)
- corp.name_en: 영문명 (법인·사업자 영문 상호)
- corp.industry: 업태/종목 (법인·사업자 업태·종목)
- company.capital: 자본금
- company.revenue_year: 결산연도
- corp.address: 본점소재지 (법인·사업자 주소)
- corp.phone: 전화번호 (법인·사업자 연락처)
- company.fax: 팩스번호
- contact.name: 담당자
- contact.position: 부서/직위
- contact.phone: 연락처
- loan.product: 상품명
- loan.amount_korean: 신청금액(한글)
- loan.amount: 신청금액
- loan.hope_date: 대출희망일
- loan.purpose: 자금용도
- loan.deposit_account: 대출금입금계좌
- loan.collateral_detail: 담보/보증내용
- other_loans.0.balance: 잔액 (1행)
- other_loans.1.kind: 여신종류 (2행)
- other_loans.1.balance: 잔액 (2행)
- other_loans.1.collateral: 담보 (2행)
- other_loans.2.balance: 잔액 (3행)
- other_loans.2.collateral: 담보 (3행)
- other_loans.3.lender: 금융기관 (4행)
- other_loans.3.balance: 잔액 (4행)
- other_loans.4.balance: 잔액 (5행)
- other_loans.4.collateral: 담보 (5행)
- other_loans.5.lender: 금융기관 (6행)
- other_loans.5.balance: 잔액 (6행)
- other_loans.6.balance: 잔액 (7행)
- other_loans.7.kind: 여신종류 (8행)
- other_loans.8.lender: 금융기관 (9행)
- other_loans.8.balance: 잔액 (9행)
- other_loans.8.collateral: 담보 (9행)
- other_loans.9.lender: 금융기관 (10행)
- other_loans.9.balance: 잔액 (10행)
- other_loans.10.balance: 잔액 (11행)
- apply_date: 신청일
```

답:

```json
[{"key": "bank", "value": "국민은행", "bbox_2d": [99, 39, 193, 61], "page": 1},
 {"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [207, 173, 302, 183], "page": 1},
 {"key": "corp.name_en", "value": null},
 {"key": "corp.industry", "value": "제조업 / 화학제품", "bbox_2d": [207, 233, 318, 243], "page": 1},
 {"key": "company.capital", "value": "300,000,000원", "bbox_2d": [296, 272, 382, 283], "page": 1},
 {"key": "company.revenue_year", "value": "2024년", "bbox_2d": [758, 277, 800, 287], "page": 1},
 {"key": "corp.address", "value": "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)", "bbox_2d": [207, 301, 615, 311], "page": 1},
 {"key": "corp.phone", "value": "064-756-8800", "bbox_2d": [207, 321, 288, 331], "page": 1},
 {"key": "company.fax", "value": null},
 {"key": "contact.name", "value": "방훈원", "bbox_2d": [207, 367, 250, 377], "page": 1},
 {"key": "contact.position", "value": "경영지원팀 차장", "bbox_2d": [258, 367, 362, 377], "page": 1},
 {"key": "contact.phone", "value": "010-8349-3877", "bbox_2d": [521, 367, 610, 377], "page": 1},
 {"key": "loan.product", "value": "기업시설자금대출", "bbox_2d": [207, 432, 321, 443], "page": 1},
 {"key": "loan.amount_korean", "value": "금 이십일억원정", "bbox_2d": [207, 452, 311, 463], "page": 1},
 {"key": "loan.amount", "value": "2,100,000,000원", "bbox_2d": [323, 452, 419, 463], "page": 1},
 {"key": "loan.hope_date", "value": "2025.04.14", "bbox_2d": [647, 472, 712, 483], "page": 1},
 {"key": "loan.purpose", "value": "공장 신축자금", "bbox_2d": [443, 512, 533, 523], "page": 1},
 {"key": "loan.deposit_account", "value": "국민은행 129-04-3353-660", "bbox_2d": [207, 532, 368, 543], "page": 1},
 {"key": "loan.collateral_detail", "value": "기술보증기금 보증서 (보증비율 100%)", "bbox_2d": [207, 572, 447, 583], "page": 1},
 {"key": "other_loans.0.balance", "value": "800", "bbox_2d": [675, 638, 697, 651], "page": 1},
 {"key": "other_loans.1.kind", "value": "운전자금대출", "bbox_2d": [370, 659, 459, 671], "page": 1},
 {"key": "other_loans.1.balance", "value": "480", "bbox_2d": [675, 659, 697, 671], "page": 1},
 {"key": "other_loans.1.collateral", "value": "부동산", "bbox_2d": [794, 659, 839, 671], "page": 1},
 {"key": "other_loans.2.balance", "value": "160", "bbox_2d": [675, 679, 697, 692], "page": 1},
 {"key": "other_loans.2.collateral", "value": "부동산", "bbox_2d": [794, 679, 839, 692], "page": 1},
 {"key": "other_loans.3.lender", "value": "SC제일은행", "bbox_2d": [144, 700, 223, 712], "page": 1},
 {"key": "other_loans.3.balance", "value": "230", "bbox_2d": [675, 700, 697, 712], "page": 1},
 {"key": "other_loans.4.balance", "value": "960", "bbox_2d": [675, 720, 697, 733], "page": 1},
 {"key": "other_loans.4.collateral", "value": "신용보증기금", "bbox_2d": [771, 720, 861, 733], "page": 1},
 {"key": "other_loans.5.lender", "value": "신한은행", "bbox_2d": [154, 741, 213, 754], "page": 1},
 {"key": "other_loans.5.balance", "value": "580", "bbox_2d": [675, 741, 697, 754], "page": 1},
 {"key": "other_loans.6.balance", "value": "1,470", "bbox_2d": [663, 762, 697, 774], "page": 1},
 {"key": "other_loans.7.kind", "value": "팩토링", "bbox_2d": [392, 782, 437, 795], "page": 1},
 {"key": "other_loans.8.lender", "value": "iM뱅크", "bbox_2d": [160, 803, 207, 815], "page": 1},
 {"key": "other_loans.8.balance", "value": "1,320", "bbox_2d": [663, 803, 697, 815], "page": 1},
 {"key": "other_loans.8.collateral", "value": "예금", "bbox_2d": [801, 803, 831, 815], "page": 1},
 {"key": "other_loans.9.lender", "value": "부산은행", "bbox_2d": [154, 828, 213, 840], "page": 1},
 {"key": "other_loans.9.balance", "value": "750", "bbox_2d": [644, 823, 667, 836], "page": 1},
 {"key": "other_loans.10.balance", "value": "1,330", "bbox_2d": [663, 852, 697, 865], "page": 1},
 {"key": "apply_date", "value": "2025년 4월 1일", "bbox_2d": [72, 82, 165, 93], "page": 2}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

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

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

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
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions loan_application_corp --show` · `python -m docgen.preview loan_application_corp --out work/loan_application_corp`
