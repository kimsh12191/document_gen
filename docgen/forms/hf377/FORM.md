# 해외영업점 계좌개설 신청서 (`hf377`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf377 · card-hash: 0c07a159cb72 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 해외영업점 계좌개설 신청서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.377 (전자금융) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 20칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `담당Prepare` | 담당Prepare | text | - | 늘 | 표 행 (묶음·항목명 '담당 Prepare') | 값 종류 `text` (항목명 자동) | fields.json:17 | 묻기 |
| `책임자Approval` | 책임자Approval | text | - | 늘 | 표 행 (묶음·항목명 '책임자 Approval') | 값 종류 `text` (항목명 자동) | fields.json:29 | 묻기 |
| `성명Name` | 성명Name | text | 1쪽 [409, 156, 460, 168] | 늘 | 항목명 그대로 | 값 종류 `person` (항목명 자동) | fields.json:41 | 묻기 |
| `성명Name2` | 성명Name | text | 1쪽 [406, 180, 474, 192] | 늘 | 항목명 그대로 | 값 종류 `person` (항목명 자동) | fields.json:54 | 묻기 |
| `customer.birth` | 생년월일DateofBirth | number | 1쪽 [406, 208, 463, 220] | 늘 | 규칙: '생년월일 Date of Birth' → `customer.birth` | 고객 정보 (키 `customer.birth`) | fields.json:67 | 묻기 |
| `여권번호PassportNo` | 여권번호PassportNo. | text | 1쪽 [406, 240, 496, 252] | 늘 | 항목명 그대로 | 값 종류 `passport` (항목명 자동) | fields.json:79 | 묻기 |
| `국내주소DomesticAddress_목록.*.여권유효기일DateofExpiry` | 여권유효기일DateofExpiry | date | 1쪽 [405, 267, 490, 279] (1행) | 늘 | 표 행 (묶음·항목명 '여권유효기일 Date of Expiry') | 값 종류 `date` (항목명 자동) | fields.json:91 | 묻기 |
| `국내주소DomesticAddress` | 국내주소DomesticAddress | text | 1쪽 [373, 323, 534, 328] | 늘 | 항목명 그대로 | 값 종류 `address` (항목명 자동) | fields.json:121 | 묻기 |
| `해외주소OverseasAddress_목록.*.여권유효기일DateofExpiry` | 여권유효기일DateofExpiry | date | 1쪽 [405, 348, 492, 360] (1행) | 늘 | 표 행 (묶음·항목명 '여권유효기일 Date of Expiry') | 값 종류 `date` (항목명 자동) | fields.json:134 | 묻기 |
| `국적Nationality` | 국적Nationality | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:224 | 묻기 |
| `여권유효기일DateofExpiry` | 여권유효기일DateofExpiry | date | 1쪽 [762, 240, 889, 252] | 늘 | 항목명 그대로 | 값 종류 `date` (항목명 자동) | fields.json:236 | 묻기 |
| `개설신청은행지점명OpeningBankBranch` | 개설신청은행/지점명OpeningBank/Branch | text | 1쪽 [408, 458, 476, 470] | 늘 | 항목명 그대로 | 값 종류 `bank` (항목명 자동) | fields.json:248 | 묻기 |
| `개설통화Currency` | 개설통화Currency | text | 1쪽 [791, 458, 827, 470] | 늘 | 항목명 그대로 | 값 종류 `currency` (항목명 자동) | fields.json:259 | 묻기 |
| `접수은행지점명BankBranch` | 접수은행/지점명Bank/Branch | text | 1쪽 [236, 641, 304, 653] | 늘 | 항목명 그대로 | 값 종류 `bank` (항목명 자동) | fields.json:270 | 묻기 |
| `customer.name` | 고객명(Name) | text | 1쪽 [292, 842, 360, 854] | 늘 | 규칙: '고객명(Name)' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:281 | 묻기 |
| `제출서류` | 제출서류(Document) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:292 | 묻기 |
| `account` | 계좌번호(A/CNo.) | account_no | 1쪽 [717, 842, 860, 854] | 늘 | 규칙: '계좌번호(A/C No.)' → `account` | 고객 정보 (키 `account`) | fields.json:303 | 묻기 |
| `date` | 신청일자(Date) | date | 1쪽 [238, 570, 323, 582] | 늘 | 규칙: '신청일자(Date)' → `date` | 고객 정보 (키 `date`) | fields.json:399 | 묻기 |
| `signer.name` | 담당자(직,성명) | text | - | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:410 | 묻기 |
| `signer3.name` | 담당자(직,성명) | text | - | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:439 | 묻기 |

## 체크·도장·서명 (marks) — 9칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.신청` | 신청(Application) | checkbox (신청(Application) / 취소(Cancellation)) | 1쪽 [281, 120, 452, 136] | 늘 | 체크 (항목명) | 보기 중 고름: 신청(Application) / 취소(Cancellation) | fields.json:314 | 묻기 |
| `check.본인은위와같이예금계좌개` | 본인은위와같이예금계좌개설/취소를신청합니다. | checkbox (본인은 위와 같이 예금계좌 개설/취소를 신청합니다.) | 1쪽 [70, 488, 484, 504] | 늘 | 체크 (항목명) | 보기 중 고름: 본인은 위와 같이 예금계좌 개설/취소를 신청합니다. | fields.json:353 | 묻기 |
| `check.현지국의법규및규제사항거` | 현지국의법규및규제사항,거래약관에따라신청자앞예금계좌가개설되 | checkbox (현지국의 법규 및 규제사항, 거래약관에 따라 신청자 앞 예금계좌가 개설되) | 1쪽 [70, 523, 803, 538] | 늘 | 체크 (항목명) | 보기 중 고름: 현지국의 법규 및 규제사항, 거래약관에 따라 신청자 앞 예금계좌가 개설되 | fields.json:376 | 묻기 |
| `seal.signer` | 담당자(직,성명) | seal | 1쪽 [888, 623, 917, 639] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:410 | 묻기 |
| `sign.signer` | 담당자(직,성명) | signature | 1쪽 [888, 623, 917, 639] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:410 | 묻기 |
| `seal.signer2` | 지점장 | seal | 1쪽 [879, 770, 908, 786] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:427 | 묻기 |
| `sign.signer2` | 지점장 | signature | 1쪽 [879, 770, 908, 786] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:427 | 묻기 |
| `seal.signer3` | 담당자(직,성명) | seal | 1쪽 [416, 880, 445, 896] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:439 | 묻기 |
| `sign.signer3` | 담당자(직,성명) | signature | 1쪽 [416, 880, 445, 896] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:439 | 묻기 |

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
"해외영업점 계좌개설 신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "현규원",
 "남궁예태",
 "850328",
 "M77365463",
 "2026.06.24",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "2028-06-17",
 "2026-06-01",
 "2029년 4월 30일",
 "우리은행",
 "USD",
 "540-121210-96628",
 "2025.04.01"
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
"2026-06-01"
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
- 담당Prepare: 담당Prepare
- 책임자Approval: 책임자Approval
- 성명Name: 성명Name (같은 항목명 중 1번째 칸)
- 성명Name2: 성명Name (같은 항목명 중 2번째 칸)
- customer.birth: 생년월일DateofBirth (고객 생년월일)
- 여권번호PassportNo: 여권번호PassportNo.
- 국내주소DomesticAddress_목록.0.여권유효기일DateofExpiry: 여권유효기일DateofExpiry (국내주소DomesticAddress 목록 1행)
- 국내주소DomesticAddress_목록.1.여권유효기일DateofExpiry: 여권유효기일DateofExpiry (국내주소DomesticAddress 목록 2행)
- 국내주소DomesticAddress: 국내주소DomesticAddress
- 해외주소OverseasAddress_목록.0.여권유효기일DateofExpiry: 여권유효기일DateofExpiry (해외주소OverseasAddress 목록 1행)
- 해외주소OverseasAddress_목록.1.여권유효기일DateofExpiry: 여권유효기일DateofExpiry (해외주소OverseasAddress 목록 2행)
- 해외주소OverseasAddress_목록.2.여권유효기일DateofExpiry: 여권유효기일DateofExpiry (해외주소OverseasAddress 목록 3행)
- 해외주소OverseasAddress_목록.3.여권유효기일DateofExpiry: 여권유효기일DateofExpiry (해외주소OverseasAddress 목록 4행)
- 국내주소DomesticAddress_목록.2.여권유효기일DateofExpiry: 여권유효기일DateofExpiry (국내주소DomesticAddress 목록 3행)
- 국내주소DomesticAddress_목록.3.여권유효기일DateofExpiry: 여권유효기일DateofExpiry (국내주소DomesticAddress 목록 4행)
- 국적Nationality: 국적Nationality
- 여권유효기일DateofExpiry: 여권유효기일DateofExpiry (같은 항목명 중 9번째 칸)
- 개설신청은행지점명OpeningBankBranch: 개설신청은행/지점명OpeningBank/Branch
- 개설통화Currency: 개설통화Currency
- 접수은행지점명BankBranch: 접수은행/지점명Bank/Branch
- customer.name: 고객명(Name) (고객 성명)
- 제출서류: 제출서류(Document)
- account: 계좌번호(A/CNo.)
- date: 신청일자(Date)
- signer.name: 담당자(직,성명) (은행·직원의 성명, 같은 항목명 중 1번째 칸)
- signer3.name: 담당자(직,성명) (은행·직원의 성명, 같은 항목명 중 2번째 칸)
```

답:

```json
[{"key": "담당Prepare", "value": null},
 {"key": "책임자Approval", "value": null},
 {"key": "성명Name", "value": "현규원", "bbox_2d": [409, 156, 460, 168], "page": 1},
 {"key": "성명Name2", "value": "남궁예태", "bbox_2d": [406, 180, 474, 192], "page": 1},
 {"key": "customer.birth", "value": "850328", "bbox_2d": [406, 208, 463, 220], "page": 1},
 {"key": "여권번호PassportNo", "value": "M77365463", "bbox_2d": [406, 240, 496, 252], "page": 1},
 {"key": "국내주소DomesticAddress_목록.0.여권유효기일DateofExpiry", "value": "2026.06.24", "bbox_2d": [405, 267, 490, 279], "page": 1},
 {"key": "국내주소DomesticAddress_목록.1.여권유효기일DateofExpiry", "value": null},
 {"key": "국내주소DomesticAddress", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [373, 323, 534, 328], "page": 1},
 {"key": "해외주소OverseasAddress_목록.0.여권유효기일DateofExpiry", "value": "2028-06-17", "bbox_2d": [405, 348, 492, 360], "page": 1},
 {"key": "해외주소OverseasAddress_목록.1.여권유효기일DateofExpiry", "value": "2026-06-01", "bbox_2d": [410, 372, 496, 384], "page": 1},
 {"key": "해외주소OverseasAddress_목록.2.여권유효기일DateofExpiry", "value": null},
 {"key": "해외주소OverseasAddress_목록.3.여권유효기일DateofExpiry", "value": null},
 {"key": "국내주소DomesticAddress_목록.2.여권유효기일DateofExpiry", "value": null},
 {"key": "국내주소DomesticAddress_목록.3.여권유효기일DateofExpiry", "value": null},
 {"key": "국적Nationality", "value": null},
 {"key": "여권유효기일DateofExpiry", "value": "2029년 4월 30일", "bbox_2d": [762, 240, 889, 252], "page": 1},
 {"key": "개설신청은행지점명OpeningBankBranch", "value": "우리은행", "bbox_2d": [408, 458, 476, 470], "page": 1},
 {"key": "개설통화Currency", "value": "USD", "bbox_2d": [791, 458, 827, 470], "page": 1},
 {"key": "접수은행지점명BankBranch", "value": "우리은행", "bbox_2d": [236, 641, 304, 653], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [292, 842, 360, 854], "page": 1},
 {"key": "제출서류", "value": null},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [717, 842, 860, 854], "page": 1},
 {"key": "date", "value": "2025.04.01", "bbox_2d": [238, 570, 323, 582], "page": 1},
 {"key": "signer.name", "value": null},
 {"key": "signer3.name", "value": null}]
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
- check.신청: 신청(Application) (체크박스, 보기: 신청(Application) / 취소(Cancellation))
- check.본인은위와같이예금계좌개: 본인은위와같이예금계좌개설/취소를신청합니다. (체크박스, 보기: 본인은 위와 같이 예금계좌 개설/취소를 신청합니다.)
- check.현지국의법규및규제사항거: 현지국의법규및규제사항,거래약관에따라신청자앞예금계좌가개설되 (체크박스, 보기: 현지국의 법규 및 규제사항, 거래약관에 따라 신청자 앞 예금계좌가 개설되)
- seal.signer: 담당자(직,성명) (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer: 담당자(직,성명) (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
- seal.signer2: 지점장 (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer2: 지점장 (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
- seal.signer3: 담당자(직,성명) (은행·직원의 신청인, 같은 항목명 중 3번째 칸, 도장)
- sign.signer3: 담당자(직,성명) (은행·직원의 신청인, 같은 항목명 중 4번째 칸, 서명)
```

답:

```json
[{"key": "check.신청", "value": "취소(Cancellation)", "bbox_2d": [281, 122, 299, 136], "page": 1},
 {"key": "check.본인은위와같이예금계좌개", "value": "본인은 위와 같이 예금계좌 개설/취소를 신청합니다.", "bbox_2d": [70, 490, 89, 504], "page": 1},
 {"key": "check.현지국의법규및규제사항거", "value": null},
 {"key": "seal.signer", "value": false},
 {"key": "sign.signer", "value": false},
 {"key": "seal.signer2", "value": false},
 {"key": "sign.signer2", "value": false},
 {"key": "seal.signer3", "value": false},
 {"key": "sign.signer3", "value": false}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf377` → `python -m docgen.formdir card hf377` (실제 질문→답 확인).

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
| 답 모양 | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf377 --show` · `python -m docgen.preview hf377 --out work/hf377`
