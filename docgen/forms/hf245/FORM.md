# 장기차관 방식의 외국인투자신고서, 변경신고서(영문) (`hf245`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf245 · card-hash: a74f8c4a6216 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 장기차관 방식의 외국인투자신고서, 변경신고서(영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.245 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 36칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `customer.name` | Name | text | 1쪽 [271, 136, 364, 163] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:52 | 묻기 |
| `customer.address` | Address | text | 1쪽 [285, 168, 704, 193] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:63 | 묻기 |
| `customer.name2` | Name | text | 1쪽 [275, 197, 368, 224] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:75 | 묻기 |
| `customer.address2` | Address | text | 1쪽 [286, 225, 705, 255] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:86 | 묻기 |
| `Cash` | Cash | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:97 | 묻기 |
| `PurposeofLoan` | PurposeofLoan | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `RateofInterest` | RateofInterest | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Capitalinkind` | Capitalinkind | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.nationality` | Nationality | text | 1쪽 [782, 197, 867, 223] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:148 | 묻기 |
| `AverageLoanPeriod` | AverageLoanPeriod | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Other` | Other | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:171 | 묻기 |
| `Other2` | Other | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:183 | 묻기 |
| `LocationofInvestment` | LocationofInvestment | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `ChangeinInformation` | ChangeinInformation | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `InformationAfterChange` | InformationAfterChange | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `NotificationNo` | NotificationNo | text | 1쪽 [194, 632, 332, 654] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `ReceiptNumber` | ReceiptNumber | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DateofReceipt` | DateofReceipt | date | 1쪽 [373, 111, 450, 125] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name3` | Name | text | 2쪽 [274, 137, 366, 162] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:266 | 묻기 |
| `customer.address3` | Address | text | 2쪽 [287, 164, 706, 198] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:277 | 묻기 |
| `customer.name4` | Name | text | 2쪽 [273, 197, 365, 223] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:289 | 묻기 |
| `customer.address4` | Address | text | 2쪽 [282, 223, 702, 257] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:300 | 묻기 |
| `Cash2` | Cash | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:311 | 묻기 |
| `PurposeofLoan2` | PurposeofLoan | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `RateofInterest2` | RateofInterest | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Capitalinkind2` | Capitalinkind | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.nationality2` | Nationality | text | 2쪽 [781, 199, 865, 223] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:362 | 묻기 |
| `AverageLoanPeriod2` | AverageLoanPeriod | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Other3` | Other | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:385 | 묻기 |
| `Other4` | Other | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:397 | 묻기 |
| `LocationofInvestment2` | LocationofInvestment | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `ChangeinInformation2` | ChangeinInformation | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `InformationAfterChange2` | InformationAfterChange | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `NotificationNo2` | NotificationNo | text | 2쪽 [191, 632, 351, 656] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `ReceiptNumber2` | ReceiptNumber | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `DateofReceipt2` | DateofReceipt | date | 2쪽 [375, 114, 444, 127] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

## 체크·도장·서명 (marks) — 4칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.staff.담당` | 담당 | seal | 1쪽 [729, 41, 770, 70] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [714, 34, 785, 77] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [792, 38, 842, 73] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [785, 34, 849, 77] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

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
"장기차관 방식의 외국인투자신고서, 변경신고서(영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "남궁예태",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "대한민국",
 "110-758641-11396",
 "2024-04-22",
 "036-622010-49556",
 "2024년 7월 6일"
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
"2024-04-22"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- customer.name: Name (고객 성명, 같은 항목명 중 1번째 칸)
- customer.address: Address (고객 주소, 같은 항목명 중 1번째 칸)
- customer.name2: Name (같은 항목명 중 2번째 칸)
- customer.address2: Address (같은 항목명 중 2번째 칸)
- Cash: Cash (같은 항목명 중 1번째 칸)
- PurposeofLoan: PurposeofLoan (같은 항목명 중 1번째 칸)
- RateofInterest: RateofInterest (같은 항목명 중 1번째 칸)
- Capitalinkind: Capitalinkind (같은 항목명 중 1번째 칸)
- customer.nationality: Nationality (고객 국적, 같은 항목명 중 1번째 칸)
- AverageLoanPeriod: AverageLoanPeriod (같은 항목명 중 1번째 칸)
- Other: Other (같은 항목명 중 1번째 칸)
- Other2: Other (같은 항목명 중 2번째 칸)
- LocationofInvestment: LocationofInvestment (같은 항목명 중 1번째 칸)
- ChangeinInformation: ChangeinInformation (같은 항목명 중 1번째 칸)
- InformationAfterChange: InformationAfterChange (같은 항목명 중 1번째 칸)
- NotificationNo: NotificationNo (같은 항목명 중 1번째 칸)
- ReceiptNumber: ReceiptNumber (같은 항목명 중 1번째 칸)
- DateofReceipt: DateofReceipt (같은 항목명 중 1번째 칸)
- customer.name3: Name (같은 항목명 중 3번째 칸)
- customer.address3: Address (같은 항목명 중 3번째 칸)
- customer.name4: Name (같은 항목명 중 4번째 칸)
- customer.address4: Address (같은 항목명 중 4번째 칸)
- Cash2: Cash (같은 항목명 중 2번째 칸)
- PurposeofLoan2: PurposeofLoan (같은 항목명 중 2번째 칸)
- RateofInterest2: RateofInterest (같은 항목명 중 2번째 칸)
- Capitalinkind2: Capitalinkind (같은 항목명 중 2번째 칸)
- customer.nationality2: Nationality (같은 항목명 중 2번째 칸)
- AverageLoanPeriod2: AverageLoanPeriod (같은 항목명 중 2번째 칸)
- Other3: Other (같은 항목명 중 3번째 칸)
- Other4: Other (같은 항목명 중 4번째 칸)
- LocationofInvestment2: LocationofInvestment (같은 항목명 중 2번째 칸)
- ChangeinInformation2: ChangeinInformation (같은 항목명 중 2번째 칸)
- InformationAfterChange2: InformationAfterChange (같은 항목명 중 2번째 칸)
- NotificationNo2: NotificationNo (같은 항목명 중 2번째 칸)
- ReceiptNumber2: ReceiptNumber (같은 항목명 중 2번째 칸)
- DateofReceipt2: DateofReceipt (같은 항목명 중 2번째 칸)
```

답:

```json
[{"key": "customer.name", "value": "남궁예태", "bbox_2d": [271, 136, 364, 163], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [285, 168, 704, 193], "page": 1},
 {"key": "customer.name2", "value": "남궁예태", "bbox_2d": [275, 197, 368, 224], "page": 1},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [286, 225, 705, 255], "page": 1},
 {"key": "Cash", "value": null},
 {"key": "PurposeofLoan", "value": null},
 {"key": "RateofInterest", "value": null},
 {"key": "Capitalinkind", "value": null},
 {"key": "customer.nationality", "value": "대한민국", "bbox_2d": [782, 197, 867, 223], "page": 1},
 {"key": "AverageLoanPeriod", "value": null},
 {"key": "Other", "value": null},
 {"key": "Other2", "value": null},
 {"key": "LocationofInvestment", "value": null},
 {"key": "ChangeinInformation", "value": null},
 {"key": "InformationAfterChange", "value": null},
 {"key": "NotificationNo", "value": "110-758641-11396", "bbox_2d": [194, 632, 332, 654], "page": 1},
 {"key": "ReceiptNumber", "value": null},
 {"key": "DateofReceipt", "value": "2024-04-22", "bbox_2d": [373, 111, 450, 125], "page": 1},
 {"key": "customer.name3", "value": "남궁예태", "bbox_2d": [274, 137, 366, 162], "page": 2},
 {"key": "customer.address3", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [287, 164, 706, 198], "page": 2},
 {"key": "customer.name4", "value": "남궁예태", "bbox_2d": [273, 197, 365, 223], "page": 2},
 {"key": "customer.address4", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [282, 223, 702, 257], "page": 2},
 {"key": "Cash2", "value": null},
 {"key": "PurposeofLoan2", "value": null},
 {"key": "RateofInterest2", "value": null},
 {"key": "Capitalinkind2", "value": null},
 {"key": "customer.nationality2", "value": "대한민국", "bbox_2d": [781, 199, 865, 223], "page": 2},
 {"key": "AverageLoanPeriod2", "value": null},
 {"key": "Other3", "value": null},
 {"key": "Other4", "value": null},
 {"key": "LocationofInvestment2", "value": null},
 {"key": "ChangeinInformation2", "value": null},
 {"key": "InformationAfterChange2", "value": null},
 {"key": "NotificationNo2", "value": "036-622010-49556", "bbox_2d": [191, 632, 351, 656], "page": 2},
 {"key": "ReceiptNumber2", "value": null},
 {"key": "DateofReceipt2", "value": "2024년 7월 6일", "bbox_2d": [375, 114, 444, 127], "page": 2}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.staff.담당", "value": true, "bbox_2d": [729, 41, 770, 70], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [792, 38, 842, 73], "page": 1},
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf245 --show` · `python -m docgen.preview hf245 --out work/hf245`
