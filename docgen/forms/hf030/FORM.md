# 국내원천소득 제한세율 적용신청서(외국법인용-영문) (`hf030`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf030 · card-hash: 07e1032e2bda -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 국내원천소득 제한세율 적용신청서(외국법인용-영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.30 (예금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 17칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `FilingNo` | FilingNo. | text | 1쪽 [155, 185, 241, 207] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `ApplicantInformation` | ApplicantInformation | text | 1쪽 [254, 209, 341, 229] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `NameofCorporation` | NameofCorporation | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `NameofRepresentative` | NameofRepresentative | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `TaxpayerIdentificationNo` | TaxpayerIdentificationNo. | rrn | 1쪽 [268, 352, 440, 381] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DateofIncorporation` | DateofIncorporation | date | 1쪽 [266, 378, 392, 406] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `FilingDate` | FilingDate | date | 1쪽 [589, 186, 728, 209] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.address` | Address | text | 1쪽 [589, 308, 680, 314] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:103 | 묻기 |
| `customer.address2` | Address | text | 1쪽 [698, 305, 863, 315] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:114 | 묻기 |
| `CountryofResidence` | CountryofResidence | text | 1쪽 [696, 326, 731, 352] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `CountryCode` | CountryCode | text | 1쪽 [695, 353, 732, 379] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `TelephoneNumber` | TelephoneNumber | phone | 1쪽 [694, 379, 839, 405] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `AddressorLocation` | AddressorLocation | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `To` | To | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:169 | 묻기 |
| `Type` | Type | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:180 | 묻기 |
| `TaxAdministrator` | []TaxAdministrator | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Other` | []Other | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

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
"국내원천소득 제한세율 적용신청서(외국법인용-영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "8861-3145",
 "(주)우진테크",
 "306582-6807900",
 "2024-08-31",
 "2025년 1월 21일",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "중국",
 "미국",
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
"2025년 1월 21일"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"중국"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- FilingNo: FilingNo.
- ApplicantInformation: ApplicantInformation
- NameofCorporation: NameofCorporation
- NameofRepresentative: NameofRepresentative
- TaxpayerIdentificationNo: TaxpayerIdentificationNo.
- DateofIncorporation: DateofIncorporation
- FilingDate: FilingDate
- customer.address: Address (고객 주소, 같은 항목명 중 1번째 칸)
- customer.address2: Address (같은 항목명 중 2번째 칸)
- CountryofResidence: CountryofResidence
- CountryCode: CountryCode
- TelephoneNumber: TelephoneNumber
- AddressorLocation: AddressorLocation
- To: To
- Type: Type
- TaxAdministrator: []TaxAdministrator
- Other: []Other
```

답:

```json
[{"key": "FilingNo", "value": "8861-3145", "bbox_2d": [155, 185, 241, 207], "page": 1},
 {"key": "ApplicantInformation", "value": "(주)우진테크", "bbox_2d": [254, 209, 341, 229], "page": 1},
 {"key": "NameofCorporation", "value": null},
 {"key": "NameofRepresentative", "value": null},
 {"key": "TaxpayerIdentificationNo", "value": "306582-6807900", "bbox_2d": [268, 352, 440, 381], "page": 1},
 {"key": "DateofIncorporation", "value": "2024-08-31", "bbox_2d": [266, 378, 392, 406], "page": 1},
 {"key": "FilingDate", "value": "2025년 1월 21일", "bbox_2d": [589, 186, 728, 209], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [589, 308, 680, 314], "page": 1},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [698, 305, 863, 315], "page": 1},
 {"key": "CountryofResidence", "value": "중국", "bbox_2d": [696, 326, 731, 352], "page": 1},
 {"key": "CountryCode", "value": "미국", "bbox_2d": [695, 353, 732, 379], "page": 1},
 {"key": "TelephoneNumber", "value": "010-6144-1173", "bbox_2d": [694, 379, 839, 405], "page": 1},
 {"key": "AddressorLocation", "value": null},
 {"key": "To", "value": null},
 {"key": "Type", "value": null},
 {"key": "TaxAdministrator", "value": null},
 {"key": "Other", "value": null}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf030 --show` · `python -m docgen.preview hf030 --out work/hf030`
