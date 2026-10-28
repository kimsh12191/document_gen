# 은행거래신청서(영문) (`hf002`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf002 · card-hash: 5f2288fa89f4 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 은행거래신청서(영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.2 (예금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 65칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `customer.email` | E-mail | text | 1쪽 [477, 191, 725, 219] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:26 | 묻기 |
| `Home` | Home | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:43 | 묻기 |
| `Office` | Office | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:55 | 묻기 |
| `Home2` | Home | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:68 | 묻기 |
| `Office2` | Office | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:80 | 묻기 |
| `Occupation` | Occupation | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:92 | 묻기 |
| `Occupation2` | Occupation | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:103 | 묻기 |
| `Payday` | Payday | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:114 | 묻기 |
| `Nochangeincustomerinformation` | Nochangeincustomerinformation | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `RequestforSMSmaturitynotice` | RequestforSMSmaturitynotice | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `갋` | 갋 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:149 | 묻기 |
| `갋2` | 갋 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:160 | 묻기 |
| `갋3` | 갋 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:171 | 묻기 |
| `목록.*.FixedFloating` | FixedFloating(mth) | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `AccountItem` | AccountItem | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `PaymentDeadline` | PaymentDeadline | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `mthcapitalizationLimit` | ()mthcapitalizationLimit | amount | 1쪽 [860, 433, 917, 450] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `mthcapitalizationLimit2` | ()mthcapitalizationLimit | amount | 1쪽 [826, 503, 916, 520] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `mthcapitalizationLimit3` | ()mthcapitalizationLimit | amount | 1쪽 [807, 576, 916, 593] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Bankbook` | Bankbook | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:345 | 묻기 |
| `Annual` | Annual | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:357 | 묻기 |
| `Bankbook2` | Bankbook | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:369 | 묻기 |
| `Annual2` | Annual | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:381 | 묻기 |
| `Annual3` | Annual | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:393 | 묻기 |
| `Bankbook3` | Bankbook | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:405 | 묻기 |
| `WithdrawalAccount` | WithdrawalAccount[ | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Applicant` | Applicant | text | 1쪽 [811, 702, 918, 717] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:429 | 묻기 |
| `YYYY` | YYYY | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:441 | 묻기 |
| `account` | AccountNo. | account_no | 1쪽 [114, 908, 223, 922] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DateofOpening` | DateofOpening | date | 1쪽 [862, 907, 927, 920] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Category` | Category | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:477 | 묻기 |
| `Time` | Time | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:489 | 묻기 |
| `EmployeeNumber` | EmployeeNumber | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `NewWithdrawalAccountAddition` | NewWithdrawalAccountAddition | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `YesNo` | YesNo | text | 2쪽 [268, 130, 348, 141] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Statusofassets` | Statusofassets | amount | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Sourcesoffinancing` | Sourcesoffinancing | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `YesNo2` | YesNo | rrn | 2쪽 [345, 425, 468, 441] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `BusinessName` | BusinessName | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Industry` | Industry(BusinessType/Item) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `BusinessRegistrationNo` | BusinessRegistrationNo. | biz_no | 2쪽 [532, 448, 630, 463] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `BusinessCommencementDate` | BusinessCommencementDate | date | 2쪽 [874, 449, 935, 461] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DepositAccount` | DepositAccount | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name` | Name | text | 2쪽 [200, 764, 272, 781] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:631 | 묻기 |
| `RelationtoPrincipal` | RelationtoPrincipal | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.birth` | DateofBirth | number | 2쪽 [484, 763, 543, 780] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.address` | Address | text | 2쪽 [485, 785, 842, 803] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:667 | 묻기 |
| `PhoneNo` | PhoneNo. | phone | 2쪽 [738, 763, 850, 782] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `AccountItem2` | AccountItem | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `PaymentDeadline2` | PaymentDeadline | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `PhoneBanking` | PhoneBanking | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Applicant2` | Applicant | text | 2쪽 [803, 161, 913, 176] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:727 | 묻기 |
| `Applicant3` | Applicant | text | 2쪽 [799, 240, 890, 256] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:739 | 묻기 |
| `Publicfeepayment` | Publicfeepayment | amount | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Other` | Other() | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Applicant4` | Applicant | text | 2쪽 [800, 548, 907, 563] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:775 | 묻기 |
| `thedateofrenewal` | thedateofrenewal | date | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Depositor` | Depositor | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:799 | 묻기 |
| `Proxy` | Proxy | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:811 | 묻기 |
| `Delegator` | Delegator(Depositor) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `account2` | AccountNo. | account_no | 2쪽 [118, 907, 227, 921] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DateofOpening2` | DateofOpening | date | 2쪽 [857, 908, 930, 921] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Category2` | Category | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:859 | 묻기 |
| `Time2` | Time | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:871 | 묻기 |
| `EmployeeNumber2` | EmployeeNumber | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

## 체크·도장·서명 (marks) — 3칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `check.Irequestagr` | Irequest/agreetoaninquiryofmyfina | checkbox (I request/agree to an inquiry of my fina) | 1쪽 [59, 694, 730, 702] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.Ishallraisen` | Ishallraisenoobjectiontoaset-off | checkbox (I shall raise no objection to a set-off ) | 1쪽 [59, 701, 695, 709] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.Ihavereceive` | Ihavereceivedanexplanationthatcust | checkbox (I have received an explanation that cust) | 1쪽 [59, 708, 588, 716] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

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
"은행거래신청서(영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "60,000",
 "89,370,000",
 "92,600,000원",
 "(주)미래케미칼",
 "540-121210-96628",
 "2024.07.17",
 "195-682164-55116",
 "125413-2181408",
 "414-15-41989",
 "2025.01.08",
 "남궁예태",
 "850328",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "010-6144-1173",
 "제일시스템즈(주)",
 "(주)삼정산업",
 "2024-10-28"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"540-121210-96628"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"850328"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- customer.email: E-mail (고객 이메일)
- Home: Home (같은 항목명 중 1번째 칸)
- Office: Office (은행·직원, 같은 항목명 중 1번째 칸)
- Home2: Home (같은 항목명 중 2번째 칸)
- Occupation: Occupation (같은 항목명 중 1번째 칸)
- Payday: Payday
- RequestforSMSmaturitynotice: RequestforSMSmaturitynotice
- 갋: 갋 (같은 항목명 중 1번째 칸)
- 갋3: 갋 (같은 항목명 중 3번째 칸)
- 목록.2.FixedFloating: FixedFloating(mth) (목록 3행)
- AccountItem: AccountItem (같은 항목명 중 1번째 칸)
- mthcapitalizationLimit: ()mthcapitalizationLimit (같은 항목명 중 1번째 칸)
- mthcapitalizationLimit2: ()mthcapitalizationLimit (같은 항목명 중 2번째 칸)
- Bankbook2: Bankbook (같은 항목명 중 2번째 칸)
- Bankbook3: Bankbook (같은 항목명 중 3번째 칸)
- WithdrawalAccount: WithdrawalAccount[
- DateofOpening: DateofOpening (같은 항목명 중 1번째 칸)
- Time: Time (같은 항목명 중 1번째 칸)
- EmployeeNumber: EmployeeNumber (같은 항목명 중 1번째 칸)
- NewWithdrawalAccountAddition: NewWithdrawalAccountAddition
- YesNo: YesNo (같은 항목명 중 1번째 칸)
- Statusofassets: Statusofassets
- Sourcesoffinancing: Sourcesoffinancing
- BusinessName: BusinessName
- BusinessCommencementDate: BusinessCommencementDate
- customer.birth: DateofBirth (고객 생년월일)
- AccountItem2: AccountItem (같은 항목명 중 2번째 칸)
- PaymentDeadline2: PaymentDeadline (같은 항목명 중 2번째 칸)
- PhoneBanking: PhoneBanking
- Applicant2: Applicant (같은 항목명 중 2번째 칸)
- Applicant3: Applicant (같은 항목명 중 3번째 칸)
- Other: Other()
- Applicant4: Applicant (같은 항목명 중 4번째 칸)
- thedateofrenewal: thedateofrenewal
- Depositor: Depositor
- Proxy: Proxy
- Delegator: Delegator(Depositor)
- account2: AccountNo. (같은 항목명 중 2번째 칸)
- DateofOpening2: DateofOpening (같은 항목명 중 2번째 칸)
- Time2: Time (같은 항목명 중 2번째 칸)
```

답:

```json
[{"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [477, 191, 725, 219], "page": 1},
 {"key": "Home", "value": null},
 {"key": "Office", "value": null},
 {"key": "Home2", "value": null},
 {"key": "Occupation", "value": null},
 {"key": "Payday", "value": null},
 {"key": "RequestforSMSmaturitynotice", "value": null},
 {"key": "갋", "value": null},
 {"key": "갋3", "value": null},
 {"key": "목록.2.FixedFloating", "value": null},
 {"key": "AccountItem", "value": null},
 {"key": "mthcapitalizationLimit", "value": "60,000", "bbox_2d": [860, 433, 917, 450], "page": 1},
 {"key": "mthcapitalizationLimit2", "value": "89,370,000", "bbox_2d": [826, 503, 916, 520], "page": 1},
 {"key": "Bankbook2", "value": null},
 {"key": "Bankbook3", "value": null},
 {"key": "WithdrawalAccount", "value": null},
 {"key": "DateofOpening", "value": "2024.07.17", "bbox_2d": [862, 907, 927, 920], "page": 1},
 {"key": "Time", "value": null},
 {"key": "EmployeeNumber", "value": null},
 {"key": "NewWithdrawalAccountAddition", "value": null},
 {"key": "YesNo", "value": "195-682164-55116", "bbox_2d": [268, 130, 348, 141], "page": 2},
 {"key": "Statusofassets", "value": null},
 {"key": "Sourcesoffinancing", "value": null},
 {"key": "BusinessName", "value": null},
 {"key": "BusinessCommencementDate", "value": "2025.01.08", "bbox_2d": [874, 449, 935, 461], "page": 2},
 {"key": "customer.birth", "value": "850328", "bbox_2d": [484, 763, 543, 780], "page": 2},
 {"key": "AccountItem2", "value": null},
 {"key": "PaymentDeadline2", "value": null},
 {"key": "PhoneBanking", "value": null},
 {"key": "Applicant2", "value": "제일시스템즈(주)", "bbox_2d": [803, 161, 913, 176], "page": 2},
 {"key": "Applicant3", "value": "(주)삼정산업", "bbox_2d": [799, 240, 890, 256], "page": 2},
 {"key": "Other", "value": null},
 {"key": "Applicant4", "value": "(주)미래케미칼", "bbox_2d": [800, 548, 907, 563], "page": 2},
 {"key": "thedateofrenewal", "value": null},
 {"key": "Depositor", "value": null},
 {"key": "Proxy", "value": null},
 {"key": "Delegator", "value": null},
 {"key": "account2", "value": "540-121210-96628", "bbox_2d": [118, 907, 227, 921], "page": 2},
 {"key": "DateofOpening2", "value": "2024-10-28", "bbox_2d": [857, 908, 930, 921], "page": 2},
 {"key": "Time2", "value": null}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- check.Irequestagr: Irequest/agreetoaninquiryofmyfina (체크박스, 보기: I request/agree to an inquiry of my fina)
- check.Ishallraisen: Ishallraisenoobjectiontoaset-off (체크박스, 보기: I shall raise no objection to a set-off )
- check.Ihavereceive: Ihavereceivedanexplanationthatcust (체크박스, 보기: I have received an explanation that cust)
```

답:

```json
[{"key": "check.Irequestagr", "value": "I request/agree to an inquiry of my fina", "bbox_2d": [59, 694, 67, 701], "page": 1},
 {"key": "check.Ishallraisen", "value": "I shall raise no objection to a set-off ", "bbox_2d": [59, 701, 67, 708], "page": 1},
 {"key": "check.Ihavereceive", "value": null}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기·위치·항목명 | studio ① 서식 › 영역 편집 (저장하면 `fields.json` items) | 재검수 → 카드 다시 만들기 |
| 값이 이상함 | 영역 편집에서 그 칸의 값 출처·값 종류 | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf002 --show` · `python -m docgen.preview hf002 --out work/hf002`
