# 포페이팅 의뢰서 (`hf277`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf277 · card-hash: e8ff88c78912 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 포페이팅 의뢰서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.277 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 13칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `고객번호` | 고객번호 | text | 1쪽 [691, 211, 893, 236] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:46 | 묻기 |
| `거래번호` | 거래번호 | text | 1쪽 [689, 237, 898, 265] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:57 | 묻기 |
| `ForfaitingAmount` | ForfaitingAmount | number | 1쪽 [804, 404, 917, 429] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `LCNO` | L/CNO. | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `LCIssuingBank` | L/CIssuingBank | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Applicant` | Applicant | text | 1쪽 [292, 505, 441, 529] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:178 | 묻기 |
| `Tenor` | Tenor | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:189 | 묻기 |
| `ExpiryDate` | ExpiryDate | date | 1쪽 [296, 574, 412, 598] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `ShipmentDate` | ShipmentDate | date | 1쪽 [290, 606, 410, 631] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `account` | 입금계좌번호 | account_no | 1쪽 [298, 638, 496, 667] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `date` | 작성일 | date | 1쪽 [378, 750, 580, 769] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:233 | 묻기 |
| `customer.name` ← `signer.name` | 본인 | text | 1쪽 [566, 794, 656, 818] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [506, 836, 830, 860] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

## 체크·도장·서명 (marks) — 7칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `check.Forfaiting종류` | Forfaiting종류(해당항목선택) | checkbox (인수후 비소구조건 매입 / 소구조건 매입후 인수시 비소구조건 전환 / 하이브리드 포페이팅 서비스 / Sight 비소구조건 매입) | 1쪽 [305, 333, 540, 349] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.customer` ← `seal.signer` | 본인 | seal | 1쪽 [727, 799, 757, 815] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.customer` ← `sign.signer` | 본인 | signature | 1쪽 [727, 799, 757, 815] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [735, 43, 786, 79] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [727, 39, 794, 83] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [798, 44, 845, 78] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [794, 39, 848, 83] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

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
"포페이팅 의뢰서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "323-188973-13417",
 "596-343818-42127",
 "32,320,000",
 "(주)미래케미칼",
 "2024.09.17",
 "2024.04.28",
 "540-121210-96628",
 "남궁예태",
 "서울특별시 서초구 강남대로 357, 103동 1301호"
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
"2024.09.17"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- 고객번호: 고객번호
- 거래번호: 거래번호
- ForfaitingAmount: ForfaitingAmount
- LCNO: L/CNO.
- LCIssuingBank: L/CIssuingBank
- Applicant: Applicant
- Tenor: Tenor
- ExpiryDate: ExpiryDate
- ShipmentDate: ShipmentDate
- account: 입금계좌번호
- date: 작성일
- customer.name: 본인 (고객 성명)
- customer.address: 주소 (고객 주소)
```

답:

```json
[{"key": "고객번호", "value": "323-188973-13417", "bbox_2d": [691, 211, 893, 236], "page": 1},
 {"key": "거래번호", "value": "596-343818-42127", "bbox_2d": [689, 237, 898, 265], "page": 1},
 {"key": "ForfaitingAmount", "value": "32,320,000", "bbox_2d": [804, 404, 917, 429], "page": 1},
 {"key": "LCNO", "value": null},
 {"key": "LCIssuingBank", "value": null},
 {"key": "Applicant", "value": "(주)미래케미칼", "bbox_2d": [292, 505, 441, 529], "page": 1},
 {"key": "Tenor", "value": null},
 {"key": "ExpiryDate", "value": "2024.09.17", "bbox_2d": [296, 574, 412, 598], "page": 1},
 {"key": "ShipmentDate", "value": "2024.04.28", "bbox_2d": [290, 606, 410, 631], "page": 1},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [298, 638, 496, 667], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [378, 750, 580, 769], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [566, 794, 656, 818], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [506, 836, 830, 860], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- check.Forfaiting종류: Forfaiting종류(해당항목선택) (체크박스, 보기: 인수후 비소구조건 매입 / 소구조건 매입후 인수시 비소구조건 전환 / 하이브리드 포페이팅 서비스 / Sight 비소구조건 매입)
- seal.customer: 본인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 본인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.Forfaiting종류", "value": "하이브리드 포페이팅 서비스", "bbox_2d": [305, 335, 324, 348], "page": 1},
 {"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [727, 799, 757, 815], "page": 1},
 {"key": "seal.staff.담당", "value": true, "bbox_2d": [735, 43, 786, 79], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [798, 44, 845, 78], "page": 1},
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf277 --show` · `python -m docgen.preview hf277 --out work/hf277`
