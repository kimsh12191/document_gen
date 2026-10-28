# 「외국환서식관리프로그램」선적서류 (일부)매입(추심) 의뢰서(2D용) (`hf294`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf294 · card-hash: e8eeff56d381 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 「외국환서식관리프로그램」선적서류 (일부)매입(추심) 의뢰서(2D용)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.294 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 40칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `RM` | RM | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:20 | 묻기 |
| `영업점장` | 영업점장 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:32 | 묻기 |
| `고객번호` | 고객번호 | text | 1쪽 [764, 164, 851, 185] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:44 | 묻기 |
| `매입번호` | 매입번호 | text | 1쪽 [763, 187, 850, 208] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:55 | 묻기 |
| `일부매입금액` | 일부매입금액 | amount | 1쪽 [473, 218, 578, 240] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `일부추심금액` | 일부추심금액 | number | 1쪽 [831, 219, 918, 240] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `AMOUNT` | AMOUNT | number | 1쪽 [399, 254, 495, 275] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:88 | 묻기 |
| `COMMODITY` | COMMODITY | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:99 | 묻기 |
| `ACCOUNTEE` | ACCOUNTEE(drawee) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `PRICETERM` | PRICETERM | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `수출상대국` | 수출상대국 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `수출신고번호` | 수출신고번호 | rrn | 1쪽 [508, 396, 624, 414] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:143 | 묻기 |
| `TENORMATURITY` | TENOR&MATURITY | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `HSCODE` | H.S.CODE | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `BENEFICIARY` | BENEFICIARY(drawer) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `FOB금액` | FOB금액 | number | 1쪽 [833, 395, 917, 416] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `TOISSUINGBANK_목록.*.BENE` | BENE | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:198 | 묻기 |
| `TOREIMBANK` | TOREIM.BANK | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `TOISSUINGBANK_목록.*.BANK` | BANK | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:237 | 묻기 |
| `BANK` | BANK | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:251 | 묻기 |
| `TOISSUINGBANK_목록.*.COMM` | COMM | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:277 | 묻기 |
| `TOISSUINGBANK_목록.*.CUST` | CUST | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:305 | 묻기 |
| `TOISSUINGBANK_목록.*.BL` | B/L | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:333 | 묻기 |
| `TOISSUINGBANK_목록.*.AWB` | AWB | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:361 | 묻기 |
| `TOISSUINGBANK_목록.*.PL` | P/L | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:389 | 묻기 |
| `TOISSUINGBANK_목록.*.IP` | I/P | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:417 | 묻기 |
| `TOISSUINGBANK_목록.*.CO` | C/O | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:445 | 묻기 |
| `TOISSUINGBANK_목록.*.IC` | I/C | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:473 | 묻기 |
| `TOISSUINGBANK_목록.*.BENECERT` | BENECERT | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `BENECERT` | BENECERT | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `외화계정대체` | 외화계정대체 | amount | 1쪽 [233, 587, 344, 610] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `원화계정대체` | 원화계정대체 | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `A` | A | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:562 | 묻기 |
| `B` | B | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:574 | 묻기 |
| `수입보증금` | 수입보증금 | number | 1쪽 [409, 704, 495, 725] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:586 | 묻기 |
| `date` | 작성일 | date | 1쪽 [583, 752, 774, 768] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:598 | 묻기 |
| `customer.name` ← `signer.name` | 본인 | text | 1쪽 [627, 771, 704, 792] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:623 | 묻기 |
| `MAILTO` | MAILTO | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `NO` | NO | rrn | 1쪽 [280, 288, 362, 302] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:652 | 묻기 |
| `FROM` | FROM | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:664 | 묻기 |

## 체크·도장·서명 (marks) — 2칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.customer` ← `seal.signer` | 본인 | seal | 1쪽 [794, 775, 821, 789] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:623 | 묻기 |
| `sign.customer` ← `sign.signer` | 본인 | signature | 1쪽 [794, 775, 821, 789] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

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
"「외국환서식관리프로그램」선적서류 (일부)매입(추심) 의뢰서(2D용)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "1296-8572",
 "5706-3377",
 "5,430,000원",
 "5,290,000",
 "127,180,000",
 "792133-7070952",
 "1,450,000",
 "CNY 134,400",
 "11,850,000",
 "남궁예태",
 "728785-2994930"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"127,180,000"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"792133-7070952"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- 영업점장: 영업점장
- 고객번호: 고객번호
- 매입번호: 매입번호
- 일부매입금액: 일부매입금액
- AMOUNT: AMOUNT
- COMMODITY: COMMODITY
- ACCOUNTEE: ACCOUNTEE(drawee)
- PRICETERM: PRICETERM
- 수출상대국: 수출상대국
- TENORMATURITY: TENOR&MATURITY
- HSCODE: H.S.CODE
- BENEFICIARY: BENEFICIARY(drawer)
- TOISSUINGBANK_목록.0.BENE: BENE (TOISSUINGBANK 목록 1행)
- TOISSUINGBANK_목록.1.BENE: BENE (TOISSUINGBANK 목록 2행)
- TOREIMBANK: TOREIM.BANK
- TOISSUINGBANK_목록.0.BANK: BANK (TOISSUINGBANK 목록 1행)
- TOISSUINGBANK_목록.1.BANK: BANK (TOISSUINGBANK 목록 2행)
- BANK: BANK (같은 항목명 중 3번째 칸)
- TOISSUINGBANK_목록.1.COMM: COMM (TOISSUINGBANK 목록 2행)
- TOISSUINGBANK_목록.0.CUST: CUST (TOISSUINGBANK 목록 1행)
- TOISSUINGBANK_목록.0.BL: B/L (TOISSUINGBANK 목록 1행)
- TOISSUINGBANK_목록.1.BL: B/L (TOISSUINGBANK 목록 2행)
- TOISSUINGBANK_목록.0.AWB: AWB (TOISSUINGBANK 목록 1행)
- TOISSUINGBANK_목록.0.PL: P/L (TOISSUINGBANK 목록 1행)
- TOISSUINGBANK_목록.1.PL: P/L (TOISSUINGBANK 목록 2행)
- TOISSUINGBANK_목록.0.IP: I/P (TOISSUINGBANK 목록 1행)
- TOISSUINGBANK_목록.0.CO: C/O (TOISSUINGBANK 목록 1행)
- TOISSUINGBANK_목록.0.IC: I/C (TOISSUINGBANK 목록 1행)
- TOISSUINGBANK_목록.1.IC: I/C (TOISSUINGBANK 목록 2행)
- TOISSUINGBANK_목록.1.BENECERT: BENECERT (TOISSUINGBANK 목록 2행)
- BENECERT: BENECERT (같은 항목명 중 3번째 칸)
- 외화계정대체: 외화계정대체
- A: A
- B: B
- 수입보증금: 수입보증금
- date: 작성일
- customer.name: 본인 (고객 성명)
- MAILTO: MAILTO
- NO: NO
- FROM: FROM
```

답:

```json
[{"key": "영업점장", "value": null},
 {"key": "고객번호", "value": "1296-8572", "bbox_2d": [764, 164, 851, 185], "page": 1},
 {"key": "매입번호", "value": "5706-3377", "bbox_2d": [763, 187, 850, 208], "page": 1},
 {"key": "일부매입금액", "value": "5,430,000원", "bbox_2d": [473, 218, 578, 240], "page": 1},
 {"key": "AMOUNT", "value": "127,180,000", "bbox_2d": [399, 254, 495, 275], "page": 1},
 {"key": "COMMODITY", "value": null},
 {"key": "ACCOUNTEE", "value": null},
 {"key": "PRICETERM", "value": null},
 {"key": "수출상대국", "value": null},
 {"key": "TENORMATURITY", "value": null},
 {"key": "HSCODE", "value": null},
 {"key": "BENEFICIARY", "value": null},
 {"key": "TOISSUINGBANK_목록.0.BENE", "value": null},
 {"key": "TOISSUINGBANK_목록.1.BENE", "value": null},
 {"key": "TOREIMBANK", "value": null},
 {"key": "TOISSUINGBANK_목록.0.BANK", "value": null},
 {"key": "TOISSUINGBANK_목록.1.BANK", "value": null},
 {"key": "BANK", "value": null},
 {"key": "TOISSUINGBANK_목록.1.COMM", "value": null},
 {"key": "TOISSUINGBANK_목록.0.CUST", "value": null},
 {"key": "TOISSUINGBANK_목록.0.BL", "value": null},
 {"key": "TOISSUINGBANK_목록.1.BL", "value": null},
 {"key": "TOISSUINGBANK_목록.0.AWB", "value": null},
 {"key": "TOISSUINGBANK_목록.0.PL", "value": null},
 {"key": "TOISSUINGBANK_목록.1.PL", "value": null},
 {"key": "TOISSUINGBANK_목록.0.IP", "value": null},
 {"key": "TOISSUINGBANK_목록.0.CO", "value": null},
 {"key": "TOISSUINGBANK_목록.0.IC", "value": null},
 {"key": "TOISSUINGBANK_목록.1.IC", "value": null},
 {"key": "TOISSUINGBANK_목록.1.BENECERT", "value": null},
 {"key": "BENECERT", "value": null},
 {"key": "외화계정대체", "value": "CNY 134,400", "bbox_2d": [233, 587, 344, 610], "page": 1},
 {"key": "A", "value": null},
 {"key": "B", "value": null},
 {"key": "수입보증금", "value": "11,850,000", "bbox_2d": [409, 704, 495, 725], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [583, 752, 774, 768], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [627, 771, 704, 792], "page": 1},
 {"key": "MAILTO", "value": null},
 {"key": "NO", "value": "728785-2994930", "bbox_2d": [280, 288, 362, 302], "page": 1},
 {"key": "FROM", "value": null}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.customer: 본인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 본인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [794, 775, 821, 789], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf294 --show` · `python -m docgen.preview hf294 --out work/hf294`
