# 기업 전자금융서비스 신청서(은행용)(영문) (`hf338`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf338 · card-hash: 501dafa3b71d -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 기업 전자금융서비스 신청서(은행용)(영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf338 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.338 (전자금융) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 43칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `Clerk` | Clerk | text | - | 늘 | 표 행 (묶음·항목명 'Clerk') | 값 종류 `text` (항목명 자동) | fields.json:23 | 묻기 |
| `Mgr` | Mgr | text | - | 늘 | 표 행 (묶음·항목명 'Mgr') | 값 종류 `text` (항목명 자동) | fields.json:35 | 묻기 |
| `GM` | GM | text | - | 늘 | 표 행 (묶음·항목명 'GM') | 값 종류 `text` (항목명 자동) | fields.json:47 | 묻기 |
| `NameCompanyName` | Name/CompanyName | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:59 | 묻기 |
| `customer.address` | Address | text | 1쪽 [179, 216, 547, 239] | 늘 | 규칙: 'Address' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:70 | 묻기 |
| `OtherRequest` | OtherRequest | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:81 | 묻기 |
| `BusinessRegistrationNo` | BusinessRegistrationNo. | biz_no | 1쪽 [720, 174, 833, 191] | 늘 | 항목명 그대로 | 값 종류 `biz_no` (항목명 자동) | fields.json:93 | 묻기 |
| `DailyKRW` | DailyKRW, | text | - | 늘 | 표 행 (묶음·항목명 'Daily KRW ,') | 값 종류 `text` (항목명 자동) | fields.json:104 | 묻기 |
| `KRW` | KRW | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:118 | 묻기 |
| `OnetimeKRW` | One-timeKRW | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:130 | 묻기 |
| `OnetimeKRW2` | One-timeKRW | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:142 | 묻기 |
| `OnetimeKRW3` | One-timeKRW | text | - | 늘 | 표 행 (묶음·항목명 'One-time KRW') | 값 종류 `text` (항목명 자동) | fields.json:154 | 묻기 |
| `목록.*.OverseasIPBlockingService` | OverseasIPBlockingService | text | - (1행) | 늘 | 표 행 (묶음·항목명 'Overseas IP Blocking Service') | 값 종류 `text` (항목명 자동) | fields.json:168 | 묻기 |
| `OTP` | OTP | text | - | 늘 | 표 행 (묶음·항목명 'OTP') | 값 종류 `text` (항목명 자동) | fields.json:220 | 묻기 |
| `목록.*.OfficeName` | OfficeName | text | - (1행) | 늘 | 표 행 (묶음·항목명 'Office Name') | 값 종류 `text` (항목명 자동) | fields.json:234 | 묻기 |
| `PhoneNoforIdentityVerification` | PhoneNo.forIdentityVerification | phone | 1쪽 [266, 550, 377, 566] | 늘 | 항목명 그대로 | 값 종류 `phone` (항목명 자동) | fields.json:258 | 묻기 |
| `목록.*.BusinessRegistrationNo` | BusinessRegistrationNo. | text | - (1행) | 늘 | 표 행 (묶음·항목명 'Business Registration No.') | 값 종류 `biz_no` (항목명 자동) | fields.json:269 | 묻기 |
| `RequestNotRequest` | RequestNotRequest | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:293 | 묻기 |
| `목록.*.CorporateRegistrationNo` | CorporateRegistrationNo. | text | 1쪽 [446, 638, 526, 654] (1행) | 늘 | 표 행 (묶음·항목명 'Corporate Registration No.') | 값 종류 `number` (항목명 자동) | fields.json:305 | 묻기 |
| `PostpaidFee` | Post-paidFee | text | - | 늘 | 표 행 (묶음·항목명 'Post-paid Fee') | 값 종류 `text` (항목명 자동) | fields.json:329 | 묻기 |
| `RequestCancel` | Request(Account:)Cancel | text | - | 늘 | 표 행 (묶음·항목명 'Request(Account: ) Cancel') | 값 종류 `text` (항목명 자동) | fields.json:342 | 묻기 |
| `OtherChange` | OtherChange | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:355 | 묻기 |
| `GeneralUser` | GeneralUser | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:367 | 묻기 |
| `OTP2` | OTP | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:379 | 묻기 |
| `UserCategory` | UserCategory | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:391 | 묻기 |
| `RequestCancel2` | RequestCancel | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:402 | 묻기 |
| `DailyKRW2` | DailyKRW | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:413 | 묻기 |
| `OnetimeKRW4` | One-timeKRW | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:425 | 묻기 |
| `WithdrawalAccount` | WithdrawalAccount | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:437 | 묻기 |
| `WithdrawalAccount2` | WithdrawalAccount | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:449 | 묻기 |
| `WithdrawalAccount_목록.*.UserID` | UserID | text | 2쪽 [528, 740, 579, 746] (1행) | 늘 | 표 행 (묶음·항목명 'User ID') | 값 종류 `number` (항목명 자동) | fields.json:461 | 묻기 |
| `DailyKRW3` | DailyKRW | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:491 | 묻기 |
| `OnetimeKRW5` | One-timeKRW | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:503 | 묻기 |
| `DesignationofBeneficiaryAccount` | DesignationofBeneficiaryAccount | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:515 | 묻기 |
| `DesignationofBeneficiaryAccount2` | DesignationofBeneficiaryAccount | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:528 | 묻기 |
| `DesignationofBeneficiaryAccount3` | DesignationofBeneficiaryAccount | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:541 | 묻기 |
| `DesignationofBeneficiaryAccount4` | DesignationofBeneficiaryAccount | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:554 | 묻기 |
| `customer.name` | Name | text | 2쪽 [270, 856, 342, 873] | 늘 | 규칙: 'Name' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:567 | 묻기 |
| `customer.address2` | Address | text | 2쪽 [269, 875, 637, 897] | 늘 | 규칙: 'Address' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:579 | 묻기 |
| `Relationship` | Relationship | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:591 | 묻기 |
| `customer.birth` | DateofBirth | date | 2쪽 [563, 855, 647, 872] | 늘 | 규칙: 'Date of Birth' → `customer.birth` | 고객 정보 (키 `customer.birth`) | fields.json:603 | 묻기 |
| `Delegator` | Delegator | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:615 | 묻기 |
| `DoNOTAgree` | DoNOTAgree | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:628 | 묻기 |

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
"기업 전자금융서비스 신청서(은행용)(영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "702-81-38348",
 "010-6144-1173",
 "5147-1499",
 "397-920111-08640",
 "남궁예태",
 "1985.03.28"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"남궁예태"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"1985.03.28"
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
- NameCompanyName: Name/CompanyName
- OtherRequest: OtherRequest
- BusinessRegistrationNo: BusinessRegistrationNo. (같은 항목명 중 1번째 칸)
- KRW: KRW
- OnetimeKRW: One-timeKRW (같은 항목명 중 1번째 칸)
- OnetimeKRW3: One-timeKRW (같은 항목명 중 3번째 칸)
- 목록.0.OverseasIPBlockingService: OverseasIPBlockingService (목록 1행)
- 목록.1.OverseasIPBlockingService: OverseasIPBlockingService (목록 2행)
- 목록.2.OverseasIPBlockingService: OverseasIPBlockingService (목록 3행)
- OTP: OTP (같은 항목명 중 1번째 칸)
- 목록.0.OfficeName: OfficeName (목록 1행)
- PhoneNoforIdentityVerification: PhoneNo.forIdentityVerification
- 목록.1.BusinessRegistrationNo: BusinessRegistrationNo. (목록 2행)
- 목록.2.BusinessRegistrationNo: BusinessRegistrationNo. (목록 3행)
- RequestNotRequest: RequestNotRequest
- 목록.0.CorporateRegistrationNo: CorporateRegistrationNo. (목록 1행)
- 목록.1.CorporateRegistrationNo: CorporateRegistrationNo. (목록 2행)
- PostpaidFee: Post-paidFee
- OtherChange: OtherChange
- GeneralUser: GeneralUser
- OTP2: OTP (같은 항목명 중 2번째 칸)
- UserCategory: UserCategory
- RequestCancel2: RequestCancel
- DailyKRW2: DailyKRW (같은 항목명 중 2번째 칸)
- OnetimeKRW4: One-timeKRW (같은 항목명 중 4번째 칸)
- WithdrawalAccount: WithdrawalAccount (같은 항목명 중 1번째 칸)
- WithdrawalAccount_목록.0.UserID: UserID (WithdrawalAccount 목록 1행)
- WithdrawalAccount_목록.1.UserID: UserID (WithdrawalAccount 목록 2행)
- DailyKRW3: DailyKRW (같은 항목명 중 3번째 칸)
- OnetimeKRW5: One-timeKRW (같은 항목명 중 5번째 칸)
- DesignationofBeneficiaryAccount: DesignationofBeneficiaryAccount (같은 항목명 중 1번째 칸)
- DesignationofBeneficiaryAccount2: DesignationofBeneficiaryAccount (같은 항목명 중 2번째 칸)
- DesignationofBeneficiaryAccount3: DesignationofBeneficiaryAccount (같은 항목명 중 3번째 칸)
- DesignationofBeneficiaryAccount4: DesignationofBeneficiaryAccount (같은 항목명 중 4번째 칸)
- customer.name: Name (고객 성명)
- customer.address2: Address (같은 항목명 중 2번째 칸)
- Relationship: Relationship
- customer.birth: DateofBirth (고객 생년월일)
- Delegator: Delegator
- DoNOTAgree: DoNOTAgree
```

답:

```json
[{"key": "NameCompanyName", "value": null},
 {"key": "OtherRequest", "value": null},
 {"key": "BusinessRegistrationNo", "value": "702-81-38348", "bbox_2d": [720, 174, 833, 191], "page": 1},
 {"key": "KRW", "value": null},
 {"key": "OnetimeKRW", "value": null},
 {"key": "OnetimeKRW3", "value": null},
 {"key": "목록.0.OverseasIPBlockingService", "value": null},
 {"key": "목록.1.OverseasIPBlockingService", "value": null},
 {"key": "목록.2.OverseasIPBlockingService", "value": null},
 {"key": "OTP", "value": null},
 {"key": "목록.0.OfficeName", "value": null},
 {"key": "PhoneNoforIdentityVerification", "value": "010-6144-1173", "bbox_2d": [266, 550, 377, 566], "page": 1},
 {"key": "목록.1.BusinessRegistrationNo", "value": null},
 {"key": "목록.2.BusinessRegistrationNo", "value": null},
 {"key": "RequestNotRequest", "value": null},
 {"key": "목록.0.CorporateRegistrationNo", "value": "5147-1499", "bbox_2d": [446, 638, 526, 654], "page": 1},
 {"key": "목록.1.CorporateRegistrationNo", "value": null},
 {"key": "PostpaidFee", "value": null},
 {"key": "OtherChange", "value": null},
 {"key": "GeneralUser", "value": null},
 {"key": "OTP2", "value": null},
 {"key": "UserCategory", "value": null},
 {"key": "RequestCancel2", "value": null},
 {"key": "DailyKRW2", "value": null},
 {"key": "OnetimeKRW4", "value": null},
 {"key": "WithdrawalAccount", "value": null},
 {"key": "WithdrawalAccount_목록.0.UserID", "value": "397-920111-08640", "bbox_2d": [528, 740, 579, 746], "page": 2},
 {"key": "WithdrawalAccount_목록.1.UserID", "value": null},
 {"key": "DailyKRW3", "value": null},
 {"key": "OnetimeKRW5", "value": null},
 {"key": "DesignationofBeneficiaryAccount", "value": null},
 {"key": "DesignationofBeneficiaryAccount2", "value": null},
 {"key": "DesignationofBeneficiaryAccount3", "value": null},
 {"key": "DesignationofBeneficiaryAccount4", "value": null},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [270, 856, 342, 873], "page": 2},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [269, 875, 637, 897], "page": 2},
 {"key": "Relationship", "value": null},
 {"key": "customer.birth", "value": "1985.03.28", "bbox_2d": [563, 855, 647, 872], "page": 2},
 {"key": "Delegator", "value": null},
 {"key": "DoNOTAgree", "value": null}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf338 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf338` → `python -m docgen.formdir card hf338` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf338 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf338 --show` · `python -m docgen.preview hf338 --out work/hf338`
