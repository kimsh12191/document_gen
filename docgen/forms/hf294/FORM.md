# 「외국환서식관리프로그램」선적서류 (일부)매입(추심) 의뢰서(2D용) (`hf294`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf294 · card-hash: 209c949b5cc4 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 「외국환서식관리프로그램」선적서류 (일부)매입(추심) 의뢰서(2D용)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf294 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.294 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 29칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `RM` | RM | text | - | 늘 | 표 행 (묶음·항목명 'RM') | 값 종류 `text` (항목명 자동) | fields.json:17 | 묻기 |
| `영업점장` | 영업점장 | text | - | 늘 | 표 행 (묶음·항목명 '영업점장') | 값 종류 `skip` (항목명 자동) | fields.json:29 | 묻기 |
| `고객번호` | 고객번호 | text | 1쪽 [764, 164, 851, 185] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:41 | 묻기 |
| `매입번호` | 매입번호 | text | 1쪽 [763, 187, 850, 208] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:52 | 묻기 |
| `일부매입금액` | 일부매입금액 | amount | 1쪽 [473, 218, 578, 240] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:63 | 묻기 |
| `일부추심금액` | 일부추심금액 | number | 1쪽 [831, 219, 918, 240] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:74 | 묻기 |
| `AMOUNT` | AMOUNT | number | 1쪽 [399, 254, 495, 275] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:85 | 묻기 |
| `COMMODITY` | COMMODITY | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:96 | 묻기 |
| `ACCOUNTEE` | ACCOUNTEE(drawee) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:107 | 묻기 |
| `PRICETERM` | PRICETERM | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:118 | 묻기 |
| `수출상대국` | 수출상대국 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:129 | 묻기 |
| `수출신고번호` | 수출신고번호 | rrn | 1쪽 [508, 396, 624, 414] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:140 | 묻기 |
| `TENORMATURITY` | TENOR&MATURITY | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:151 | 묻기 |
| `HSCODE` | H.S.CODE | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:162 | 묻기 |
| `BENEFICIARY` | BENEFICIARY(drawer) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:173 | 묻기 |
| `FOB금액` | FOB금액 | number | 1쪽 [833, 395, 917, 416] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:184 | 묻기 |
| `TOREIMBANK` | TOREIM.BANK | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:223 | 묻기 |
| `BANK` | BANK | text | - | 늘 | 표 행 (묶음·항목명 'BANK') | 값 종류 `text` (항목명 자동) | fields.json:262 | 묻기 |
| `BENECERT` | BENECERT | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:526 | 묻기 |
| `외화계정대체` | 외화계정대체 | amount | 1쪽 [233, 587, 344, 610] | 늘 | 항목명 그대로 | 값 종류 `fx_amount` (항목명 자동) | fields.json:537 | 묻기 |
| `원화계정대체` | 원화계정대체 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:548 | 묻기 |
| `A` | A | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:559 | 묻기 |
| `B` | B | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:571 | 묻기 |
| `수입보증금` | 수입보증금 | number | 1쪽 [409, 704, 495, 725] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:583 | 묻기 |
| `date` | 작성일 | date | 1쪽 [583, 752, 774, 768] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:595 | 묻기 |
| `customer.name` ← `signer.name` | 본인 | text | 1쪽 [627, 771, 704, 792] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:620 | 묻기 |
| `MAILTO` | MAILTO | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:637 | 묻기 |
| `NO` | NO | rrn | 1쪽 [280, 288, 362, 302] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:649 | 묻기 |
| `FROM` | FROM | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:661 | 묻기 |

## 표 `TOISSUINGBANK_목록` (표 과제 table·table_read·table_find·table_qa) — 11열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `TOISSUINGBANK_목록.*.BENE` | BENE | text | - (1행) | 늘 | 표 행 (묶음·항목명 'BENE') | 값 종류 `text` (항목명 자동) | fields.json:195 | 묻기 |
| `TOISSUINGBANK_목록.*.BANK` | BANK | text | - (1행) | 늘 | 표 행 (묶음·항목명 'BANK') | 값 종류 `text` (항목명 자동) | fields.json:234 | 묻기 |
| `TOISSUINGBANK_목록.*.COMM` | COMM | text | - (1행) | 늘 | 표 행 (묶음·항목명 'COMM') | 값 종류 `text` (항목명 자동) | fields.json:274 | 묻기 |
| `TOISSUINGBANK_목록.*.CUST` | CUST | text | - (1행) | 늘 | 표 행 (묶음·항목명 'CUST') | 값 종류 `text` (항목명 자동) | fields.json:302 | 묻기 |
| `TOISSUINGBANK_목록.*.BL` | B/L | text | - (1행) | 늘 | 표 행 (묶음·항목명 'B/L') | 값 종류 `text` (항목명 자동) | fields.json:330 | 묻기 |
| `TOISSUINGBANK_목록.*.AWB` | AWB | text | - (1행) | 늘 | 표 행 (묶음·항목명 'AWB') | 값 종류 `text` (항목명 자동) | fields.json:358 | 묻기 |
| `TOISSUINGBANK_목록.*.PL` | P/L | text | - (1행) | 늘 | 표 행 (묶음·항목명 'P/L') | 값 종류 `text` (항목명 자동) | fields.json:386 | 묻기 |
| `TOISSUINGBANK_목록.*.IP` | I/P | text | - (1행) | 늘 | 표 행 (묶음·항목명 'I/P') | 값 종류 `text` (항목명 자동) | fields.json:414 | 묻기 |
| `TOISSUINGBANK_목록.*.CO` | C/O | text | - (1행) | 늘 | 표 행 (묶음·항목명 'C/O') | 값 종류 `text` (항목명 자동) | fields.json:442 | 묻기 |
| `TOISSUINGBANK_목록.*.IC` | I/C | text | - (1행) | 늘 | 표 행 (묶음·항목명 'I/C') | 값 종류 `text` (항목명 자동) | fields.json:470 | 묻기 |
| `TOISSUINGBANK_목록.*.BENECERT` | BENECERT | text | - (1행) | 늘 | 표 행 (묶음·항목명 'BENE CERT') | 값 종류 `text` (항목명 자동) | fields.json:498 | 묻기 |

## 체크·도장·서명 (marks) — 2칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.customer` ← `seal.signer` | 본인 | seal | 1쪽 [794, 775, 821, 789] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:620 | 묻기 |
| `sign.customer` ← `sign.signer` | 본인 | signature | 1쪽 [794, 775, 821, 789] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:620 | 묻기 |

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
- RM: RM
- 영업점장: 영업점장
- 고객번호: 고객번호
- 매입번호: 매입번호
- 일부매입금액: 일부매입금액
- 일부추심금액: 일부추심금액
- AMOUNT: AMOUNT
- COMMODITY: COMMODITY
- ACCOUNTEE: ACCOUNTEE(drawee)
- PRICETERM: PRICETERM
- 수출상대국: 수출상대국
- 수출신고번호: 수출신고번호
- TENORMATURITY: TENOR&MATURITY
- HSCODE: H.S.CODE
- BENEFICIARY: BENEFICIARY(drawer)
- FOB금액: FOB금액
- TOREIMBANK: TOREIM.BANK
- BANK: BANK
- BENECERT: BENECERT
- 외화계정대체: 외화계정대체
- 원화계정대체: 원화계정대체
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
[{"key": "RM", "value": null},
 {"key": "영업점장", "value": null},
 {"key": "고객번호", "value": "1296-8572", "bbox_2d": [764, 164, 851, 185], "page": 1},
 {"key": "매입번호", "value": "5706-3377", "bbox_2d": [763, 187, 850, 208], "page": 1},
 {"key": "일부매입금액", "value": "5,430,000원", "bbox_2d": [473, 218, 578, 240], "page": 1},
 {"key": "일부추심금액", "value": "5,290,000", "bbox_2d": [831, 219, 918, 240], "page": 1},
 {"key": "AMOUNT", "value": "127,180,000", "bbox_2d": [399, 254, 495, 275], "page": 1},
 {"key": "COMMODITY", "value": null},
 {"key": "ACCOUNTEE", "value": null},
 {"key": "PRICETERM", "value": null},
 {"key": "수출상대국", "value": null},
 {"key": "수출신고번호", "value": "792133-7070952", "bbox_2d": [508, 396, 624, 414], "page": 1},
 {"key": "TENORMATURITY", "value": null},
 {"key": "HSCODE", "value": null},
 {"key": "BENEFICIARY", "value": null},
 {"key": "FOB금액", "value": "1,450,000", "bbox_2d": [833, 395, 917, 416], "page": 1},
 {"key": "TOREIMBANK", "value": null},
 {"key": "BANK", "value": null},
 {"key": "BENECERT", "value": null},
 {"key": "외화계정대체", "value": "CNY 134,400", "bbox_2d": [233, 587, 344, 610], "page": 1},
 {"key": "원화계정대체", "value": null},
 {"key": "A", "value": null},
 {"key": "B", "value": null},
 {"key": "수입보증금", "value": "11,850,000", "bbox_2d": [409, 704, 495, 725], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [583, 752, 774, 768], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [627, 771, 704, 792], "page": 1},
 {"key": "MAILTO", "value": null},
 {"key": "NO", "value": "728785-2994930", "bbox_2d": [280, 288, 362, 302], "page": 1},
 {"key": "FROM", "value": null}]
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
- seal.customer: 본인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 본인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [794, 775, 821, 789], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf294 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf294` → `python -m docgen.formdir card hf294` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf294 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf294 --show` · `python -m docgen.preview hf294 --out work/hf294`
