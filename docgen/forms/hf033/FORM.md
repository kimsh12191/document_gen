# 국내원천소득 제한세율 적용신청서(비거주자용-영문) (`hf033`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf033 · card-hash: e8700abb52cf -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 국내원천소득 제한세율 적용신청서(비거주자용-영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.33 (예금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 11칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `FilingNo` | FilingNo. | text | 1쪽 [231, 125, 454, 153] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `FilingDate` | FilingDate | date | 1쪽 [663, 126, 776, 150] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `TaxpayerIdentificationNo` | TaxpayerIdentificationNo. | text | 1쪽 [261, 248, 479, 273] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `CountryofResidence` | CountryofResidence | text | 1쪽 [258, 271, 295, 296] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.birth` | DateofBirth | number | 1쪽 [673, 247, 748, 272] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `CountryCode` | CountryCode | text | 1쪽 [669, 271, 703, 296] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `목록.*.Yes` | Yes | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:92 | 묻기 |
| `목록.*.No` | No | rrn | 1쪽 [861, 497, 922, 506] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:188 | 묻기 |
| `AddressorLocation` | AddressorLocation | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `NameofIndividualorCorporation` | NameofIndividualorCorporation | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Applicant` | Applicant | text | 1쪽 [666, 919, 761, 941] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:296 | 묻기 |

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
"국내원천소득 제한세율 적용신청서(비거주자용-영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "532-733653-79964",
 "2024.09.18",
 "717-062999-88907",
 "일본",
 "850328",
 "중국",
 "390865-4400292",
 "839-994355-55009",
 "(주)가온무역"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2024.09.18"
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
- FilingDate: FilingDate
- TaxpayerIdentificationNo: TaxpayerIdentificationNo.
- CountryofResidence: CountryofResidence
- customer.birth: DateofBirth (고객 생년월일)
- CountryCode: CountryCode
- 목록.0.Yes: Yes (목록 1행)
- 목록.1.Yes: Yes (목록 2행)
- 목록.2.Yes: Yes (목록 3행)
- 목록.3.Yes: Yes (목록 4행)
- 목록.4.Yes: Yes (목록 5행)
- 목록.5.Yes: Yes (목록 6행)
- 목록.6.Yes: Yes (목록 7행)
- 목록.7.Yes: Yes (목록 8행)
- 목록.0.No: No (목록 1행)
- 목록.1.No: No (목록 2행)
- 목록.2.No: No (목록 3행)
- 목록.3.No: No (목록 4행)
- 목록.4.No: No (목록 5행)
- 목록.5.No: No (목록 6행)
- 목록.6.No: No (목록 7행)
- AddressorLocation: AddressorLocation
- NameofIndividualorCorporation: NameofIndividualorCorporation
- Applicant: Applicant
```

답:

```json
[{"key": "FilingNo", "value": "532-733653-79964", "bbox_2d": [231, 125, 454, 153], "page": 1},
 {"key": "FilingDate", "value": "2024.09.18", "bbox_2d": [663, 126, 776, 150], "page": 1},
 {"key": "TaxpayerIdentificationNo", "value": "717-062999-88907", "bbox_2d": [261, 248, 479, 273], "page": 1},
 {"key": "CountryofResidence", "value": "일본", "bbox_2d": [258, 271, 295, 296], "page": 1},
 {"key": "customer.birth", "value": "850328", "bbox_2d": [673, 247, 748, 272], "page": 1},
 {"key": "CountryCode", "value": "중국", "bbox_2d": [669, 271, 703, 296], "page": 1},
 {"key": "목록.0.Yes", "value": null},
 {"key": "목록.1.Yes", "value": null},
 {"key": "목록.2.Yes", "value": null},
 {"key": "목록.3.Yes", "value": null},
 {"key": "목록.4.Yes", "value": null},
 {"key": "목록.5.Yes", "value": null},
 {"key": "목록.6.Yes", "value": null},
 {"key": "목록.7.Yes", "value": null},
 {"key": "목록.0.No", "value": "390865-4400292", "bbox_2d": [861, 497, 922, 506], "page": 1},
 {"key": "목록.1.No", "value": "839-994355-55009", "bbox_2d": [860, 522, 920, 529], "page": 1},
 {"key": "목록.2.No", "value": null},
 {"key": "목록.3.No", "value": null},
 {"key": "목록.4.No", "value": null},
 {"key": "목록.5.No", "value": null},
 {"key": "목록.6.No", "value": null},
 {"key": "AddressorLocation", "value": null},
 {"key": "NameofIndividualorCorporation", "value": null},
 {"key": "Applicant", "value": "(주)가온무역", "bbox_2d": [666, 919, 761, 941], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf033 --show` · `python -m docgen.preview hf033 --out work/hf033`
