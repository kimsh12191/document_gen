# 본인확인서(FATCA CRS 개인,개인사업자용)(영문) (`hf429`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf429 · card-hash: 35443029bd1c -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 본인확인서(FATCA CRS 개인,개인사업자용)(영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.429 (기타) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 21칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `CustomerProfile` | CustomerProfile | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `목록.*.value` | (CapitalLetter)* / (TIN) | amount | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `WhetherOverseasResidentorNot` | WhetherOverseasResidentorNot | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `IdentificationNumberetc` | IdentificationNumber(TIN),etc. | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Reportingcountry` | Reportingcountry | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `목록.*.FATCA` | FATCA | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:124 | 묻기 |
| `목록.*.CRS` | CRS | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:148 | 묻기 |
| `NA` | N/A | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:172 | 묻기 |
| `Surname` | Surname(성) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:184 | 묻기 |
| `Surname2` | Surname(성) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:198 | 묻기 |
| `GivenName` | GivenName(이름) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Jurisdictionof` | Jurisdictionof | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Country` | Country*(2) | text | 1쪽 [209, 608, 255, 619] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `OverseaEnglishaddress` | OverseaEnglishaddress | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Surname3` | Surname(성) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:400 | 묻기 |
| `GivenName2` | GivenName(이름) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.birth` | DateofBirth | number | 1쪽 [519, 189, 549, 196] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.birth2` | DateofBirth | number | 1쪽 [516, 199, 544, 206] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `목록.*.PhoneNo` | PhoneNo. | phone | 1쪽 [516, 223, 574, 230] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.birth3` | DateofBirth | number | 1쪽 [694, 176, 736, 185] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `PhoneNo` | PhoneNo. | phone | 1쪽 [699, 210, 783, 219] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

## 체크·도장·서명 (marks) — 11칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `check.UScitizen` | U.S.citizen(includingdualcitizenship) | checkbox (U.S. citizen(including dual citizenship) / U.S. permanent resident / U.S. resident under U.S. tax law) | 1쪽 [194, 311, 354, 325] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.Residentinac` | ResidentinacountryotherthanU.S | checkbox (Resident in a country other than U.S) | 1쪽 [194, 361, 417, 374] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.AllNA` | AllN/A | checkbox (All N/A) | 1쪽 [194, 395, 259, 409] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.Nonissuingc` | Non-issuingcountry | checkbox (Non-issuing country / Not requested by tax authority / Not acquired) | 1쪽 [512, 506, 651, 527] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.Nonissuingc2` | Non-issuingcountry | checkbox (Non-issuing country / Not requested by tax authority / Not acquired) | 1쪽 [512, 589, 651, 611] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [750, 42, 780, 63] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [733, 46, 797, 59] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [797, 46, 861, 59] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [797, 46, 861, 59] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [875, 42, 905, 63] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [861, 46, 918, 59] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

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

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

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

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf429 --show` · `python -m docgen.preview hf429 --out work/hf429`
