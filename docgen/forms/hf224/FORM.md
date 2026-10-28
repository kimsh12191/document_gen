# Usance 송금 조건변경신청서 (`hf224`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf224 · card-hash: 4786f4b6413a -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** Usance 송금 조건변경신청서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf224 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.224 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 15칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `신청인정보` | ♣신청인정보 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:43 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [291, 360, 690, 393] | 늘 | 규칙: '주소' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:54 | 묻기 |
| `Usance송금번호` | Usance송금번호 | rrn | 1쪽 [291, 391, 444, 417] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:66 | 묻기 |
| `통화금액` | 통화금액 | amount | 1쪽 [776, 419, 914, 443] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:78 | 묻기 |
| `수취인명` | 수취인명 | text | 1쪽 [290, 488, 431, 511] | 늘 | 항목명 그대로 | 값 종류 `company` (항목명 자동) | fields.json:89 | 묻기 |
| `수취인주소및전화번호` | 수취인주소및전화번호 | phone | 1쪽 [296, 513, 431, 537] | 늘 | 항목명 그대로 | 값 종류 `phone` (항목명 자동) | fields.json:100 | 묻기 |
| `수취인주소및전화번호2` | 수취인주소및전화번호 | phone | 1쪽 [292, 540, 426, 565] | 늘 | 항목명 그대로 | 값 종류 `phone` (항목명 자동) | fields.json:111 | 묻기 |
| `수취인계좌번호` | 수취인계좌번호 | text | 1쪽 [291, 567, 474, 594] | 늘 | 항목명 그대로 | 값 종류 `account` (항목명 자동) | fields.json:122 | 묻기 |
| `수취은행BIC` | 수취은행BIC | text | 1쪽 [292, 595, 361, 620] | 늘 | 항목명 그대로 | 값 종류 `bank` (항목명 자동) | fields.json:133 | 묻기 |
| `기타` | 기타 | text | 1쪽 [292, 675, 382, 700] | 늘 | 항목명 그대로 | 값 종류 `note` (항목명 자동) | fields.json:202 | 묻기 |
| `수취은행명` | 수취은행명 | text | 1쪽 [711, 594, 790, 617] | 늘 | 항목명 그대로 | 값 종류 `bank` (항목명 자동) | fields.json:213 | 묻기 |
| `영문` | 영문(English) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:224 | 묻기 |
| `date` | 작성일 | date | 1쪽 [339, 753, 553, 770] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:235 | 묻기 |
| `customer.name` ← `signer.name` | 신청인 | text | 1쪽 [682, 750, 763, 773] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:260 | 묻기 |
| `signer2.name` | 신청인 | text | 1쪽 [694, 750, 775, 772] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:277 | 묻기 |

## 체크·도장·서명 (marks) — 10칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.만기` | 만기(상환일) | checkbox (Fixed due date () | 1쪽 [308, 617, 446, 644] | 늘 | 체크 (항목명) | 보기 중 고름: Fixed due date ( | fields.json:144 | 묻기 |
| `check.만기2` | 만기(상환일) | checkbox (() | 1쪽 [308, 644, 331, 671] | 늘 | 체크 (항목명) | 보기 중 고름: ( | fields.json:173 | 묻기 |
| `seal.customer` ← `seal.signer` | 신청인 | seal | 1쪽 [807, 743, 841, 780] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:260 | 묻기 |
| `sign.customer` ← `sign.signer` | 신청인 | signature | 1쪽 [812, 755, 835, 769] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:260 | 묻기 |
| `seal.signer2` | 신청인 | seal | 1쪽 [843, 742, 899, 782] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:277 | 묻기 |
| `sign.signer2` | 신청인 | signature | 1쪽 [838, 755, 904, 769] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:277 | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [776, 191, 836, 233] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [766, 186, 845, 238] | 늘 | - | - | - | 묻기 |
| `seal.staff.부점장` | 부점장 | seal | 1쪽 [855, 192, 912, 232] | 늘 | - | - | - | 묻기 |
| `sign.staff.부점장` | 부점장 | signature | 1쪽 [845, 186, 921, 238] | 늘 | - | - | - | 묻기 |

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
"Usance 송금 조건변경신청서"
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
 "169828-6868220",
 "203,960,000원",
 "(주)미래케미칼",
 "010-6144-1173",
 "147-125481-80485",
 "우리은행",
 "해당 없음",
 "하나은행",
 "남궁예태"
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
"010-6144-1173"
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
- 신청인정보: ♣신청인정보
- customer.address: 주소 (고객 주소)
- Usance송금번호: Usance송금번호
- 통화금액: 통화금액
- 수취인명: 수취인명
- 수취인주소및전화번호: 수취인주소및전화번호 (같은 항목명 중 1번째 칸)
- 수취인주소및전화번호2: 수취인주소및전화번호 (같은 항목명 중 2번째 칸)
- 수취인계좌번호: 수취인계좌번호
- 수취은행BIC: 수취은행BIC
- 기타: 기타
- 수취은행명: 수취은행명
- 영문: 영문(English)
- date: 작성일
- customer.name: 신청인 (고객 성명, 같은 항목명 중 1번째 칸)
- signer2.name: 신청인 (고객 본인의 성명, 같은 항목명 중 2번째 칸)
```

답:

```json
[{"key": "신청인정보", "value": null},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [291, 360, 690, 393], "page": 1},
 {"key": "Usance송금번호", "value": "169828-6868220", "bbox_2d": [291, 391, 444, 417], "page": 1},
 {"key": "통화금액", "value": "203,960,000원", "bbox_2d": [776, 419, 914, 443], "page": 1},
 {"key": "수취인명", "value": "(주)미래케미칼", "bbox_2d": [290, 488, 431, 511], "page": 1},
 {"key": "수취인주소및전화번호", "value": "010-6144-1173", "bbox_2d": [296, 513, 431, 537], "page": 1},
 {"key": "수취인주소및전화번호2", "value": "010-6144-1173", "bbox_2d": [292, 540, 426, 565], "page": 1},
 {"key": "수취인계좌번호", "value": "147-125481-80485", "bbox_2d": [291, 567, 474, 594], "page": 1},
 {"key": "수취은행BIC", "value": "우리은행", "bbox_2d": [292, 595, 361, 620], "page": 1},
 {"key": "기타", "value": "해당 없음", "bbox_2d": [292, 675, 382, 700], "page": 1},
 {"key": "수취은행명", "value": "하나은행", "bbox_2d": [711, 594, 790, 617], "page": 1},
 {"key": "영문", "value": null},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [339, 753, 553, 770], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [682, 750, 763, 773], "page": 1},
 {"key": "signer2.name", "value": "남궁예태", "bbox_2d": [694, 750, 775, 772], "page": 1}]
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
- check.만기: 만기(상환일) (같은 항목명 중 1번째 칸, 체크박스, 보기: Fixed due date ()
- check.만기2: 만기(상환일) (같은 항목명 중 2번째 칸, 체크박스, 보기: ()
- seal.customer: 신청인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 신청인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.signer2: 신청인 (고객 본인의 신청인, 같은 항목명 중 3번째 칸, 도장)
- sign.signer2: 신청인 (고객 본인의 신청인, 같은 항목명 중 4번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.부점장: 부점장 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.부점장: 부점장 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.만기", "value": null},
 {"key": "check.만기2", "value": null},
 {"key": "seal.customer", "value": true, "bbox_2d": [807, 743, 841, 780], "page": 1},
 {"key": "sign.customer", "value": false},
 {"key": "seal.signer2", "value": true, "bbox_2d": [843, 742, 899, 782], "page": 1},
 {"key": "sign.signer2", "value": false},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [776, 191, 836, 233], "page": 1},
 {"key": "sign.staff.책임자", "value": false},
 {"key": "seal.staff.부점장", "value": true, "bbox_2d": [855, 192, 912, 232], "page": 1},
 {"key": "sign.staff.부점장", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf224 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf224` → `python -m docgen.formdir card hf224` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf224 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf224 --show` · `python -m docgen.preview hf224 --out work/hf224`
