# 본인확인서(FATCA CRS 개인,개인사업자용)(영문) (`hf429`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf429 · card-hash: 6df047364a01 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 본인확인서(FATCA CRS 개인,개인사업자용)(영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf429 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.429 (기타) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 21칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `CustomerProfile` | CustomerProfile | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:52 | 묻기 |
| `목록.*.value` | (CapitalLetter)* / (TIN) | amount | - (1행) | 늘 | 표 행 (묶음·항목명 '(Capital Letter)*') | 값 종류 `skip` (항목명 자동) | fields.json:63 | 묻기 |
| `WhetherOverseasResidentorNot` | WhetherOverseasResidentorNot | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:75 | 묻기 |
| `IdentificationNumberetc` | IdentificationNumber(TIN),etc. | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:86 | 묻기 |
| `Reportingcountry` | Reportingcountry | text | - | 늘 | 표 행 (묶음·항목명 'Reporting country') | 값 종류 `text` (항목명 자동) | fields.json:97 | 묻기 |
| `목록.*.FATCA` | FATCA | text | - (1행) | 늘 | 표 행 (묶음·항목명 'FATCA') | 값 종류 `text` (항목명 자동) | fields.json:121 | 묻기 |
| `목록.*.CRS` | CRS | text | - (1행) | 늘 | 표 행 (묶음·항목명 'CRS') | 값 종류 `text` (항목명 자동) | fields.json:145 | 묻기 |
| `NA` | N/A | text | - | 늘 | 표 행 (묶음·항목명 'N/A') | 값 종류 `text` (항목명 자동) | fields.json:169 | 묻기 |
| `Surname` | Surname(성) | text | - | 늘 | 표 행 (묶음·항목명 'Surname(성)') | 값 종류 `text` (항목명 자동) | fields.json:181 | 묻기 |
| `Surname2` | Surname(성) | text | - | 늘 | 표 행 (묶음·항목명 'Surname(성)') | 값 종류 `text` (항목명 자동) | fields.json:195 | 묻기 |
| `GivenName` | GivenName(이름) | text | - | 늘 | 표 행 (묶음·항목명 'Given Name(이름)') | 값 종류 `text` (항목명 자동) | fields.json:209 | 묻기 |
| `Jurisdictionof` | Jurisdictionof | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:340 | 묻기 |
| `Country` | Country*(2) | text | 1쪽 [209, 608, 255, 619] | 늘 | 항목명 그대로 | 값 종류 `country` (항목명 자동) | fields.json:351 | 묻기 |
| `OverseaEnglishaddress` | OverseaEnglishaddress | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:374 | 묻기 |
| `Surname3` | Surname(성) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:397 | 묻기 |
| `GivenName2` | GivenName(이름) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:408 | 묻기 |
| `customer.birth` | DateofBirth | number | 1쪽 [519, 189, 549, 196] | 늘 | 표 행 (묶음·항목명 'Date of Birth') | 값 종류 `date` (항목명 자동) | fields.json:419 | 묻기 |
| `customer.birth2` | DateofBirth | number | 1쪽 [516, 199, 544, 206] | 늘 | 표 행 (묶음·항목명 'Date of Birth') | 값 종류 `date` (항목명 자동) | fields.json:433 | 묻기 |
| `목록.*.PhoneNo` | PhoneNo. | phone | 1쪽 [516, 223, 574, 230] (1행) | 늘 | 표 행 (묶음·항목명 'Phone No.') | 값 종류 `phone` (항목명 자동) | fields.json:447 | 묻기 |
| `customer.birth3` | DateofBirth | number | 1쪽 [694, 176, 736, 185] | 늘 | 규칙: 'Date of Birth' → `customer.birth` | 고객 정보 (키 `customer.birth`) | fields.json:593 | 묻기 |
| `PhoneNo` | PhoneNo. | phone | 1쪽 [699, 210, 783, 219] | 늘 | 항목명 그대로 | 값 종류 `phone` (항목명 자동) | fields.json:604 | 묻기 |

## 체크·도장·서명 (marks) — 11칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.UScitizen` | U.S.citizen(includingdualcitizenship) | checkbox (U.S. citizen(including dual citizenship) / U.S. permanent resident / U.S. resident under U.S. tax law) | 1쪽 [194, 311, 354, 325] | 늘 | 체크 (항목명) | 보기 중 고름: U.S. citizen(including dual citizenship) / U.S. permanent resident / U.S. resident under U.S. tax law | fields.json:221 | 묻기 |
| `check.Residentinac` | ResidentinacountryotherthanU.S | checkbox (Resident in a country other than U.S) | 1쪽 [194, 361, 417, 374] | 늘 | 체크 (항목명) | 보기 중 고름: Resident in a country other than U.S | fields.json:282 | 묻기 |
| `check.AllNA` | AllN/A | checkbox (All N/A) | 1쪽 [194, 395, 259, 409] | 늘 | 체크 (항목명) | 보기 중 고름: All N/A | fields.json:311 | 묻기 |
| `check.Nonissuingc` | Non-issuingcountry | checkbox (Non-issuing country / Not requested by tax authority / Not acquired) | 1쪽 [512, 506, 651, 527] | 늘 | 체크 (항목명) | 보기 중 고름: Non-issuing country / Not requested by tax authority / Not acquired | fields.json:459 | 묻기 |
| `check.Nonissuingc2` | Non-issuingcountry | checkbox (Non-issuing country / Not requested by tax authority / Not acquired) | 1쪽 [512, 589, 651, 611] | 늘 | 체크 (항목명) | 보기 중 고름: Non-issuing country / Not requested by tax authority / Not acquired | fields.json:520 | 묻기 |
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [750, 42, 780, 63] | 늘 | - | - | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [733, 46, 797, 59] | 늘 | - | - | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [797, 46, 861, 59] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [797, 46, 861, 59] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [875, 42, 905, 63] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [861, 46, 918, 59] | 늘 | - | - | - | 묻기 |

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
"본인확인서(FATCA CRS 개인,개인사업자용)(영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "베트남",
 "850328",
 "010-6144-1173"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"베트남"
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
- CustomerProfile: CustomerProfile
- 목록.0.value: (CapitalLetter)* (목록 1행)
- WhetherOverseasResidentorNot: WhetherOverseasResidentorNot
- IdentificationNumberetc: IdentificationNumber(TIN),etc.
- Reportingcountry: Reportingcountry
- 목록.1.value: (CapitalLetter)* (목록 2행)
- 목록.0.FATCA: FATCA (목록 1행)
- 목록.1.FATCA: FATCA (목록 2행)
- 목록.0.CRS: CRS (목록 1행)
- 목록.1.CRS: CRS (목록 2행)
- NA: N/A
- Surname: Surname(성) (같은 항목명 중 1번째 칸)
- Surname2: Surname(성) (같은 항목명 중 2번째 칸)
- GivenName: GivenName(이름) (같은 항목명 중 1번째 칸)
- Jurisdictionof: Jurisdictionof
- Country: Country*(2)
- 목록.2.value: (TIN) (목록 3행)
- OverseaEnglishaddress: OverseaEnglishaddress
- 목록.3.value: (TIN) (목록 4행)
- Surname3: Surname(성) (같은 항목명 중 3번째 칸)
- GivenName2: GivenName(이름) (같은 항목명 중 2번째 칸)
- customer.birth: DateofBirth (고객 생년월일, 같은 항목명 중 1번째 칸)
- customer.birth2: DateofBirth (같은 항목명 중 2번째 칸)
- 목록.0.PhoneNo: PhoneNo. (목록 1행)
- 목록.1.PhoneNo: PhoneNo. (목록 2행)
- customer.birth3: DateofBirth (같은 항목명 중 3번째 칸)
- PhoneNo: PhoneNo. (같은 항목명 중 3번째 칸)
```

답:

```json
[{"key": "CustomerProfile", "value": null},
 {"key": "목록.0.value", "value": null},
 {"key": "WhetherOverseasResidentorNot", "value": null},
 {"key": "IdentificationNumberetc", "value": null},
 {"key": "Reportingcountry", "value": null},
 {"key": "목록.1.value", "value": null},
 {"key": "목록.0.FATCA", "value": null},
 {"key": "목록.1.FATCA", "value": null},
 {"key": "목록.0.CRS", "value": null},
 {"key": "목록.1.CRS", "value": null},
 {"key": "NA", "value": null},
 {"key": "Surname", "value": null},
 {"key": "Surname2", "value": null},
 {"key": "GivenName", "value": null},
 {"key": "Jurisdictionof", "value": null},
 {"key": "Country", "value": "베트남", "bbox_2d": [209, 608, 255, 619], "page": 1},
 {"key": "목록.2.value", "value": null},
 {"key": "OverseaEnglishaddress", "value": null},
 {"key": "목록.3.value", "value": null},
 {"key": "Surname3", "value": null},
 {"key": "GivenName2", "value": null},
 {"key": "customer.birth", "value": "850328", "bbox_2d": [519, 189, 549, 196], "page": 1},
 {"key": "customer.birth2", "value": "850328", "bbox_2d": [516, 199, 544, 206], "page": 1},
 {"key": "목록.0.PhoneNo", "value": "010-6144-1173", "bbox_2d": [516, 223, 574, 230], "page": 1},
 {"key": "목록.1.PhoneNo", "value": "010-6144-1173", "bbox_2d": [515, 650, 618, 661], "page": 1},
 {"key": "customer.birth3", "value": "850328", "bbox_2d": [694, 176, 736, 185], "page": 1},
 {"key": "PhoneNo", "value": "010-6144-1173", "bbox_2d": [699, 210, 783, 219], "page": 1}]
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
- check.UScitizen: U.S.citizen(includingdualcitizenship) (체크박스, 보기: U.S. citizen(including dual citizenship) / U.S. permanent resident / U.S. resident under U.S. tax law)
- check.Residentinac: ResidentinacountryotherthanU.S (체크박스, 보기: Resident in a country other than U.S)
- check.AllNA: AllN/A (체크박스, 보기: All N/A)
- check.Nonissuingc: Non-issuingcountry (같은 항목명 중 1번째 칸, 체크박스, 보기: Non-issuing country / Not requested by tax authority / Not acquired)
- check.Nonissuingc2: Non-issuingcountry (같은 항목명 중 2번째 칸, 체크박스, 보기: Non-issuing country / Not requested by tax authority / Not acquired)
- seal.staff.본인확인: 본인확인 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.본인확인: 본인확인 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.UScitizen", "value": "U.S. permanent resident", "bbox_2d": [194, 311, 209, 325], "page": 1},
 {"key": "check.Residentinac", "value": null},
 {"key": "check.AllNA", "value": "All N/A", "bbox_2d": [194, 395, 209, 409], "page": 1},
 {"key": "check.Nonissuingc", "value": "Non-issuing country", "bbox_2d": [512, 506, 535, 527], "page": 1},
 {"key": "check.Nonissuingc2", "value": "Non-issuing country", "bbox_2d": [512, 589, 535, 611], "page": 1},
 {"key": "seal.staff.본인확인", "value": true, "bbox_2d": [750, 42, 780, 63], "page": 1},
 {"key": "sign.staff.본인확인", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [875, 42, 905, 63], "page": 1},
 {"key": "sign.staff.책임자", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf429 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf429` → `python -m docgen.formdir card hf429` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf429 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf429 --show` · `python -m docgen.preview hf429 --out work/hf429`
