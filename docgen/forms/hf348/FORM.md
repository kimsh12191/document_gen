# 기업관계사 서비스 이용신청서(영문) (`hf348`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf348 · card-hash: e0a8fa235502 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 기업관계사 서비스 이용신청서(영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf348 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.348 (전자금융) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 22칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `CorporateRegistrationNo` | CorporateRegistrationNo. | rrn | 1쪽 [316, 171, 462, 189] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:84 | 묻기 |
| `corp.name` ← `company.name` | CompanyName | text | 1쪽 [316, 194, 415, 208] | 늘 | 규칙: 'Company Name' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:96 | 묻기 |
| `customer.address` | Address | text | 1쪽 [317, 210, 624, 226] | 늘 | 규칙: 'Address' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:108 | 묻기 |
| `CorporateRegistrationNo2` | CorporateRegistrationNo. | text | 1쪽 [311, 231, 412, 251] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:120 | 묻기 |
| `BankBranch` | Bank/Branch | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:132 | 묻기 |
| `company.name2` | CompanyName | text | 1쪽 [312, 271, 412, 286] | 늘 | 규칙: 'Company Name' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:145 | 묻기 |
| `customer.address2` | Address | text | 1쪽 [313, 288, 619, 302] | 늘 | 규칙: 'Address' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:157 | 묻기 |
| `PhoneNo` | PhoneNo. | phone | 1쪽 [315, 304, 408, 319] | 늘 | 항목명 그대로 | 값 종류 `phone` (항목명 자동) | fields.json:169 | 묻기 |
| `customer.email` | e-mail | text | 1쪽 [312, 322, 449, 336] | 늘 | 규칙: 'e-mail' → `customer.email` | 고객 정보 (키 `customer.email`) | fields.json:181 | 묻기 |
| `BusinessRegistrationNo` | BusinessRegistrationNo. | biz_no | 1쪽 [696, 170, 819, 189] | 늘 | 항목명 그대로 | 값 종류 `biz_no` (항목명 자동) | fields.json:239 | 묻기 |
| `Representative` | Representative | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:251 | 묻기 |
| `BusinessRegistrationNo2` | BusinessRegistrationNo. | biz_no | 1쪽 [698, 229, 826, 248] | 늘 | 항목명 그대로 | 값 종류 `biz_no` (항목명 자동) | fields.json:263 | 묻기 |
| `GlobalClientNo` | GlobalClientNo. | rrn | 1쪽 [694, 255, 800, 270] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:275 | 묻기 |
| `Representative2` | Representative | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:288 | 묻기 |
| `Fax` | Fax | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:300 | 묻기 |
| `customer.name` | Name | text | 2쪽 [317, 872, 383, 887] | 늘 | 규칙: 'Name' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:888 | 묻기 |
| `customer.address3` | Address | text | 2쪽 [317, 887, 654, 909] | 늘 | 규칙: 'Address' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:900 | 묻기 |
| `Relationship` | Relationship | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:912 | 묻기 |
| `company.name3` | CompanyName | text | 2쪽 [313, 925, 423, 943] | 늘 | 규칙: 'Company Name' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:924 | 묻기 |
| `customer.birth` | DateofBirth | date | 2쪽 [693, 870, 778, 886] | 늘 | 규칙: 'Date of Birth' → `customer.birth` | 고객 정보 (키 `customer.birth`) | fields.json:935 | 묻기 |
| `Delegator` | Delegator | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:947 | 묻기 |
| `Representative3` | Representative | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:959 | 묻기 |

## 표 `목록` (표 과제 table·table_read·table_find·table_qa) — 4열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `목록.*.ExecutorID` | ExecutorID* | text | 1쪽 [189, 575, 241, 585] (1행) | 늘 | 표 행 (묶음·항목명 'Executor ID*') | 값 종류 `number` (항목명 자동) | fields.json:591 | 묻기 |
| `목록.*.Currency` | Currency | text | 1쪽 [278, 573, 304, 587] (1행) | 늘 | 표 행 (묶음·항목명 'Currency') | 값 종류 `currency` (항목명 자동) | fields.json:615 | 묻기 |
| `목록.*.AccountNo` | AccountNo. | text | 1쪽 [335, 573, 407, 586] (1행) | 늘 | 표 행 (묶음·항목명 'Account No.') | 값 종류 `number` (항목명 자동) | fields.json:639 | 묻기 |
| `목록.*.RegisteredSealSign` | RegisteredSeal/Sign | text | - (1행) | 늘 | 표 행 (묶음·항목명 'Registered Seal/Sign') | 값 종류 `text` (항목명 자동) | fields.json:663 | 묻기 |

## 체크·도장·서명 (marks) — 8칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.ApplicationType` | ApplicationType | checkbox (New / Change / Terminate) | 1쪽 [321, 150, 366, 164] | 늘 | 체크 (항목명) | 보기 중 고름: New / Change / Terminate | fields.json:23 | 묻기 |
| `check.LocationofAffiliate` | LocationofAffiliate | checkbox (In Korea / Outside Korea) | 1쪽 [714, 150, 782, 164] | 늘 | 체크 (항목명) | 보기 중 고름: In Korea / Outside Korea | fields.json:194 | 묻기 |
| `check.Entire` | Entire | checkbox (Entire / Specific / Deposit (Inquiry of / All accounts, / Accounts designated below only), / Foreign exchange, / Export/import, / Loan, / Digital payment, / Cards, / Giro/utility) | 1쪽 [387, 408, 480, 422] | 늘 | 체크 (항목명) | 보기 중 고름: Entire / Specific / Deposit (Inquiry of / All accounts, / Accounts designated below only), / Foreign exchange, / Export/import, / Loan, / Digital payment, / Cards, / Giro/utility | fields.json:312 | 묻기 |
| `check.ID` | ID | checkbox (Executor / OTP) | 1쪽 [875, 682, 913, 695] | 늘 | 체크 (항목명) | 보기 중 고름: Executor / OTP | fields.json:501 | 묻기 |
| `check.ID2` | ID | checkbox (Executor / OTP) | 1쪽 [875, 808, 913, 822] | 늘 | 체크 (항목명) | 보기 중 고름: Executor / OTP | fields.json:546 | 묻기 |
| `check.CorporateBan` | CorporateBanking(IntegratedCMS) | checkbox (Corporate Banking(Integrated CMS) / CMS Plus / CMSiNet) | 1쪽 [717, 52, 820, 73] | 늘 | 체크 (항목명) | 보기 중 고름: Corporate Banking(Integrated CMS) / CMS Plus / CMSiNet | fields.json:759 | 묻기 |
| `check.PrincipalContractor` | PrincipalContractor | checkbox (Consent to the Affiliate’s Use of ID) | 2쪽 [172, 541, 402, 555] | 늘 | 체크 (항목명) | 보기 중 고름: Consent to the Affiliate’s Use of ID | fields.json:814 | 묻기 |
| `check.Affiliate` | Affiliate | checkbox (Consent to the Use of Accounts / Consent to the Users under Control) | 2쪽 [172, 674, 410, 688] | 늘 | 체크 (항목명) | 보기 중 고름: Consent to the Use of Accounts / Consent to the Users under Control | fields.json:843 | 묻기 |

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
"기업관계사 서비스 이용신청서(영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "177500-9976390",
 "(주)미래케미칼",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "2905-2533",
 "010-6144-1173",
 "yetae741@gmail.com",
 "393-51-69387",
 "702-81-38348",
 "621914-9099347",
 "1253-0730",
 "312-223443-87111",
 "EUR",
 "CAD",
 "9763-8503",
 "833-205043-06707",
 "남궁예태",
 "1985-03-28"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"(주)미래케미칼"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"(주)미래케미칼"
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
- CorporateRegistrationNo: CorporateRegistrationNo. (같은 항목명 중 1번째 칸)
- corp.name: CompanyName (법인·사업자 상호, 같은 항목명 중 1번째 칸)
- customer.address: Address (고객 주소, 같은 항목명 중 1번째 칸)
- CorporateRegistrationNo2: CorporateRegistrationNo. (같은 항목명 중 2번째 칸)
- BankBranch: Bank/Branch
- company.name2: CompanyName (같은 항목명 중 2번째 칸)
- customer.address2: Address (같은 항목명 중 2번째 칸)
- PhoneNo: PhoneNo.
- customer.email: e-mail (고객 이메일)
- BusinessRegistrationNo: BusinessRegistrationNo. (같은 항목명 중 1번째 칸)
- Representative: Representative (같은 항목명 중 1번째 칸)
- BusinessRegistrationNo2: BusinessRegistrationNo. (같은 항목명 중 2번째 칸)
- GlobalClientNo: GlobalClientNo.
- Representative2: Representative (같은 항목명 중 2번째 칸)
- Fax: Fax
- customer.name: Name (고객 성명)
- customer.address3: Address (같은 항목명 중 3번째 칸)
- Relationship: Relationship
- company.name3: CompanyName (같은 항목명 중 3번째 칸)
- customer.birth: DateofBirth (고객 생년월일)
- Delegator: Delegator
- Representative3: Representative (같은 항목명 중 3번째 칸)
```

답:

```json
[{"key": "CorporateRegistrationNo", "value": "177500-9976390", "bbox_2d": [316, 171, 462, 189], "page": 1},
 {"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [316, 194, 415, 208], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [317, 210, 624, 226], "page": 1},
 {"key": "CorporateRegistrationNo2", "value": "2905-2533", "bbox_2d": [311, 231, 412, 251], "page": 1},
 {"key": "BankBranch", "value": null},
 {"key": "company.name2", "value": "(주)미래케미칼", "bbox_2d": [312, 271, 412, 286], "page": 1},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [313, 288, 619, 302], "page": 1},
 {"key": "PhoneNo", "value": "010-6144-1173", "bbox_2d": [315, 304, 408, 319], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [312, 322, 449, 336], "page": 1},
 {"key": "BusinessRegistrationNo", "value": "393-51-69387", "bbox_2d": [696, 170, 819, 189], "page": 1},
 {"key": "Representative", "value": null},
 {"key": "BusinessRegistrationNo2", "value": "702-81-38348", "bbox_2d": [698, 229, 826, 248], "page": 1},
 {"key": "GlobalClientNo", "value": "621914-9099347", "bbox_2d": [694, 255, 800, 270], "page": 1},
 {"key": "Representative2", "value": null},
 {"key": "Fax", "value": null},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [317, 872, 383, 887], "page": 2},
 {"key": "customer.address3", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [317, 887, 654, 909], "page": 2},
 {"key": "Relationship", "value": null},
 {"key": "company.name3", "value": "(주)미래케미칼", "bbox_2d": [313, 925, 423, 943], "page": 2},
 {"key": "customer.birth", "value": "1985-03-28", "bbox_2d": [693, 870, 778, 886], "page": 2},
 {"key": "Delegator", "value": null},
 {"key": "Representative3", "value": null}]
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
- check.ApplicationType: ApplicationType (체크박스, 보기: New / Change / Terminate)
- check.LocationofAffiliate: LocationofAffiliate (체크박스, 보기: In Korea / Outside Korea)
- check.Entire: Entire (체크박스, 보기: Entire / Specific / Deposit (Inquiry of / All accounts, / Accounts designated below only), / Foreign exchange, / Export/import, / Loan, / Digital payment, / Cards, / Giro/utility)
- check.ID: ID (같은 항목명 중 1번째 칸, 체크박스, 보기: Executor / OTP)
- check.ID2: ID (같은 항목명 중 2번째 칸, 체크박스, 보기: Executor / OTP)
- check.CorporateBan: CorporateBanking(IntegratedCMS) (체크박스, 보기: Corporate Banking(Integrated CMS) / CMS Plus / CMSiNet)
- check.PrincipalContractor: PrincipalContractor (체크박스, 보기: Consent to the Affiliate’s Use of ID)
- check.Affiliate: Affiliate (체크박스, 보기: Consent to the Use of Accounts / Consent to the Users under Control)
```

답:

```json
[{"key": "check.ApplicationType", "value": "New", "bbox_2d": [321, 151, 334, 164], "page": 1},
 {"key": "check.LocationofAffiliate", "value": "In Korea", "bbox_2d": [714, 151, 728, 164], "page": 1},
 {"key": "check.Entire", "value": "All accounts,", "bbox_2d": [387, 409, 400, 422], "page": 1},
 {"key": "check.ID", "value": "OTP", "bbox_2d": [875, 682, 888, 695], "page": 1},
 {"key": "check.ID2", "value": "OTP", "bbox_2d": [875, 809, 888, 822], "page": 1},
 {"key": "check.CorporateBan", "value": "CMSiNet", "bbox_2d": [717, 53, 737, 73], "page": 1},
 {"key": "check.PrincipalContractor", "value": "Consent to the Affiliate’s Use of ID", "bbox_2d": [172, 542, 185, 555], "page": 2},
 {"key": "check.Affiliate", "value": "Consent to the Users under Control", "bbox_2d": [172, 675, 185, 688], "page": 2}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 항목명)
- ExecutorID: ExecutorID*
- Currency: Currency
- AccountNo: AccountNo.
- RegisteredSealSign: RegisteredSeal/Sign
```

답:

```json
{
 "columns": [
  "ExecutorID",
  "Currency",
  "AccountNo",
  "RegisteredSealSign"
 ],
 "rows": [
  [
   "1253-0730",
   "EUR",
   "9763-8503",
   null
  ],
  [
   "312-223443-87111",
   "CAD",
   "833-205043-06707",
   null
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    189,
    573,
    407,
    587
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    193,
    589,
    452,
    603
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
[{"columns": ["ExecutorID*", "Currency", "AccountNo.", "RegisteredSeal/Sign"], "bbox_2d": [189, 573, 452, 603], "page": 1, "n_rows": 2}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 'ExecutorID*'·'Currency' 열이 있는 표를 보고 답하세요. 표의 행은 모두 몇 개입니까? 머리글·합계 행과 모두 빈 행은 세지 않습니다. (숫자만 답하세요)
```

답:

```json
2
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 'ExecutorID*'·'Currency' 열이 있는 표를 보고 답하세요. 'ExecutorID*' 칸이 '1253-0730'인 행의 'AccountNo.' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"9763-8503"
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf348 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf348` → `python -m docgen.formdir card hf348` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | studio ① 서식 › 영역 편집에서 그리기 (`fields.json` items 에 한 칸) | 다시 |
| 답의 위치 (박스) | `fields.json` 그 칸의 `rect` [x0, y0, x1, y1] (pt) — 또는 영역 편집 | 다시 |
| 답의 키 | `fields.json` 그 칸에 `"key"` (없으면 규칙이 항목명으로 정함 — 모든 서식 공통 규칙은 studio 키 사전) | 다시 |
| 답의 값 | `fields.json` 그 칸에 `"source"` ([값 출처 목록](../_common/values.md)) 또는 값 종류 `"kind"` | 다시 |
| 칸의 항목명 | `fields.json` 그 칸의 `label` | 다시 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf348 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf348 --show` · `python -m docgen.preview hf348 --out work/hf348`
