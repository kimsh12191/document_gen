# 기업 전자금융서비스 신청서(은행용)(영문) (`hf338`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf338 · card-hash: 2a4f24fe4ffa -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 기업 전자금융서비스 신청서(은행용)(영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.338 (전자금융) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 43칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `Clerk` | Clerk | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:26 | 묻기 |
| `Mgr` | Mgr | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:38 | 묻기 |
| `GM` | GM | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:50 | 묻기 |
| `NameCompanyName` | Name/CompanyName | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.address` | Address | text | 1쪽 [179, 216, 547, 239] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:73 | 묻기 |
| `OtherRequest` | OtherRequest | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `BusinessRegistrationNo` | BusinessRegistrationNo. | biz_no | 1쪽 [720, 174, 833, 191] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DailyKRW` | DailyKRW, | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `KRW` | KRW | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:121 | 묻기 |
| `OnetimeKRW` | One-timeKRW | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `OnetimeKRW2` | One-timeKRW | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `OnetimeKRW3` | One-timeKRW | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `목록.*.OverseasIPBlockingService` | OverseasIPBlockingService | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `OTP` | OTP | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:223 | 묻기 |
| `목록.*.OfficeName` | OfficeName | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `PhoneNoforIdentityVerification` | PhoneNo.forIdentityVerification | phone | 1쪽 [266, 550, 377, 566] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `목록.*.BusinessRegistrationNo` | BusinessRegistrationNo. | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `RequestNotRequest` | RequestNotRequest | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `목록.*.CorporateRegistrationNo` | CorporateRegistrationNo. | text | 1쪽 [446, 638, 526, 654] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `PostpaidFee` | Post-paidFee | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `RequestCancel` | Request(Account:)Cancel | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `OtherChange` | OtherChange | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `GeneralUser` | GeneralUser | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `OTP2` | OTP | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:382 | 묻기 |
| `UserCategory` | UserCategory | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `RequestCancel2` | RequestCancel | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DailyKRW2` | DailyKRW | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `OnetimeKRW4` | One-timeKRW | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `WithdrawalAccount` | WithdrawalAccount | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `WithdrawalAccount2` | WithdrawalAccount | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `WithdrawalAccount_목록.*.UserID` | UserID | text | 2쪽 [528, 740, 579, 746] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DailyKRW3` | DailyKRW | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `OnetimeKRW5` | One-timeKRW | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DesignationofBeneficiaryAccount` | DesignationofBeneficiaryAccount | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DesignationofBeneficiaryAccount2` | DesignationofBeneficiaryAccount | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DesignationofBeneficiaryAccount3` | DesignationofBeneficiaryAccount | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DesignationofBeneficiaryAccount4` | DesignationofBeneficiaryAccount | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name` | Name | text | 2쪽 [270, 856, 342, 873] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:570 | 묻기 |
| `customer.address2` | Address | text | 2쪽 [269, 875, 637, 897] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:582 | 묻기 |
| `Relationship` | Relationship | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:594 | 묻기 |
| `customer.birth` | DateofBirth | date | 2쪽 [563, 855, 647, 872] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Delegator` | Delegator | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:618 | 묻기 |
| `DoNOTAgree` | DoNOTAgree | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

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

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf338 --show` · `python -m docgen.preview hf338 --out work/hf338`
