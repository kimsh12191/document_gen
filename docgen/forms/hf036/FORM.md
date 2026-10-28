# 예금(신탁) 이관 의뢰서 (`hf036`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf036 · card-hash: 2a41992ffd5b -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 예금(신탁) 이관 의뢰서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.36 (예금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 12칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `예금종류` | 예금(신탁)종류 | text | 1쪽 [291, 205, 396, 218] | 늘 | 항목명 그대로 | 값 종류 `product` (항목명 자동) | fields.json:103 | 묻기 |
| `account` | 계좌번호 | account_no | 1쪽 [291, 236, 439, 248] | 늘 | 규칙: '계 좌 번 호' → `account` | 고객 정보 (키 `account`) | fields.json:114 | 묻기 |
| `customer.name` | 예금주(위탁자) | text | 1쪽 [295, 266, 365, 278] | 늘 | 규칙: '예금주(위탁자)' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:125 | 묻기 |
| `예금잔액` | 예금(신탁)잔액 | number | 1쪽 [830, 296, 917, 309] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:136 | 묻기 |
| `현취급점명` | 현취급점명 | text | 1쪽 [290, 327, 360, 339] | 늘 | 항목명 그대로 | 값 종류 `branch` (항목명 자동) | fields.json:147 | 묻기 |
| `비고` | 비고 | text | 1쪽 [294, 405, 511, 417] | 늘 | 항목명 그대로 | 값 종류 `note` (항목명 자동) | fields.json:158 | 묻기 |
| `date` | 작성일 | date | 1쪽 [398, 535, 622, 553] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:169 | 묻기 |
| `signer.name` | 명 | text | 1쪽 [378, 608, 448, 621] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:195 | 묻기 |
| `signer2.name` | 명 | text | 1쪽 [378, 680, 448, 692] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:212 | 묻기 |
| `date2` | 작성일 | date | 1쪽 [398, 802, 622, 820] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:229 | 묻기 |
| `이관점기재란` | 이관점기재란 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:267 | 묻기 |
| `이관서류목록` | 이관서류목록 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:279 | 묻기 |

## 체크·도장·서명 (marks) — 22칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.customer` ← `seal.signer` | 명 | seal | 1쪽 [556, 596, 588, 633] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:195 | 묻기 |
| `sign.customer` ← `sign.signer` | 명 | signature | 1쪽 [557, 606, 587, 622] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:195 | 묻기 |
| `seal.signer2` | 명 | seal | 1쪽 [557, 678, 587, 694] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:212 | 묻기 |
| `sign.signer2` | 명 | signature | 1쪽 [557, 678, 587, 694] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:212 | 묻기 |
| `seal.signer3` | 지점 | seal | 1쪽 [882, 838, 911, 854] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:255 | 묻기 |
| `sign.signer3` | 지점 | signature | 1쪽 [882, 838, 911, 854] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:255 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [74, 56, 141, 101] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [74, 56, 141, 101] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [144, 58, 203, 99] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [141, 56, 207, 101] | 늘 | - | - | - | 묻기 |
| `seal.staff.관리자` | 관리자 | seal | 1쪽 [207, 56, 273, 101] | 늘 | - | - | - | 묻기 |
| `sign.staff.관리자` | 관리자 | signature | 1쪽 [207, 56, 273, 101] | 늘 | - | - | - | 묻기 |
| `seal.staff.부점장` | 부점장 | seal | 1쪽 [280, 60, 332, 97] | 늘 | - | - | - | 묻기 |
| `sign.staff.부점장` | 부점장 | signature | 1쪽 [273, 56, 339, 101] | 늘 | - | - | - | 묻기 |
| `seal.staff.담당2` | 담당 | seal | 1쪽 [670, 62, 716, 95] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당2` | 담당 | signature | 1쪽 [660, 56, 726, 101] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자2` | 책임자 | seal | 1쪽 [732, 59, 787, 98] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자2` | 책임자 | signature | 1쪽 [726, 56, 792, 101] | 늘 | - | - | - | 묻기 |
| `seal.staff.관리자2` | 관리자 | seal | 1쪽 [799, 65, 838, 92] | 늘 | - | - | - | 묻기 |
| `sign.staff.관리자2` | 관리자 | signature | 1쪽 [792, 56, 845, 101] | 늘 | - | - | - | 묻기 |
| `seal.staff.부점장2` | 부점장 | seal | 1쪽 [857, 60, 909, 97] | 늘 | - | - | - | 묻기 |
| `sign.staff.부점장2` | 부점장 | signature | 1쪽 [845, 56, 921, 101] | 늘 | - | - | - | 묻기 |

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
"예금(신탁) 이관 의뢰서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "청년도약계좌",
 "540-121210-96628",
 "남궁예태",
 "36,730,000",
 "센텀지점",
 "월급 통장 변경. 문자로 안내"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"청년도약계좌"
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
- 예금종류: 예금(신탁)종류
- account: 계좌번호
- customer.name: 예금주(위탁자) (고객 성명)
- 예금잔액: 예금(신탁)잔액
- 현취급점명: 현취급점명
- 비고: 비고
- date: 작성일 (같은 항목명 중 1번째 칸)
- signer.name: 명 (고객 본인의 성명, 같은 항목명 중 1번째 칸)
- signer2.name: 명 (같은 항목명 중 2번째 칸)
- date2: 작성일 (같은 항목명 중 2번째 칸)
- 이관점기재란: 이관점기재란
- 이관서류목록: 이관서류목록
```

답:

```json
[{"key": "예금종류", "value": "청년도약계좌", "bbox_2d": [291, 205, 396, 218], "page": 1},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [291, 236, 439, 248], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [295, 266, 365, 278], "page": 1},
 {"key": "예금잔액", "value": "36,730,000", "bbox_2d": [830, 296, 917, 309], "page": 1},
 {"key": "현취급점명", "value": "센텀지점", "bbox_2d": [290, 327, 360, 339], "page": 1},
 {"key": "비고", "value": "월급 통장 변경. 문자로 안내", "bbox_2d": [294, 405, 511, 417], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [398, 535, 622, 553], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [378, 608, 448, 621], "page": 1},
 {"key": "signer2.name", "value": "남궁예태", "bbox_2d": [378, 680, 448, 692], "page": 1},
 {"key": "date2", "value": "2025년 4월 1일", "bbox_2d": [398, 802, 622, 820], "page": 1},
 {"key": "이관점기재란", "value": null},
 {"key": "이관서류목록", "value": null}]
```

### 기타 칸 정리 `freetext` · 채점 f1

질문:

```
이 문서의 '비고' 칸에 적힌 내용을 DB에 넣을 수 있게 정리해 JSON 한 줄로 답하세요. 기준일(서류 작성일)은 2025-04-01 입니다.
쓸 수 있는 키
- purpose: 용도. 보기 중 하나: 생활자금, 주택구입, 전세자금, 사업자금, 학자금, 자녀 교육비, 의료비, 결혼자금, 차량구입
- reason: 사유. 보기 중 하나: 만기 해지, 해외 이주, 타행 이체, 급여 수령, 본인 요청, 계좌 정리, 주소 변경, 분실
- amount: 금액. 원 단위 정수 (3천만원 → 30000000)
- date: 날짜. YYYY-MM-DD. 상대 날짜는 기준일로 계산 (초 = 1일, 중순 = 15일, 말 = 말일, 다음주 = 7일 뒤)
- period_months: 기간. 개월 수 정수 (1년 → 12)
- request: 요청. 보기 중 하나: 서류 추가 제출, 전화 연락, 우편 발송, 문자 안내, 방문 예정
- memo: 위 키에 맞지 않는 내용. 적힌 그대로
- approx: 대략적인 값(정도, 쯤, 약, 초·중순, 다음주 등)을 쓴 키의 목록
적힌 내용만 쓰고 null 은 쓰지 않습니다. 대략적인 값도 가장 그럴듯한 값 하나로 쓰세요.
```

답:

```json
{
 "reason": "급여 수령",
 "request": "문자 안내"
}
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
- seal.customer: 명 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 명 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.signer2: 명 (같은 항목명 중 3번째 칸, 도장)
- sign.signer2: 명 (같은 항목명 중 4번째 칸, 서명)
- seal.signer3: 지점 (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer3: 지점 (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.관리자: 관리자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.관리자: 관리자 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.부점장: 부점장 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.부점장: 부점장 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당2: 담당 (같은 항목명 중 3번째 칸, 도장)
- sign.staff.담당2: 담당 (같은 항목명 중 4번째 칸, 서명)
- seal.staff.책임자2: 책임자 (같은 항목명 중 3번째 칸, 도장)
- sign.staff.책임자2: 책임자 (같은 항목명 중 4번째 칸, 서명)
- seal.staff.관리자2: 관리자 (같은 항목명 중 3번째 칸, 도장)
- sign.staff.관리자2: 관리자 (같은 항목명 중 4번째 칸, 서명)
- seal.staff.부점장2: 부점장 (같은 항목명 중 3번째 칸, 도장)
- sign.staff.부점장2: 부점장 (같은 항목명 중 4번째 칸, 서명)
```

답:

```json
[{"key": "seal.customer", "value": true, "bbox_2d": [556, 596, 588, 633], "page": 1},
 {"key": "sign.customer", "value": false},
 {"key": "seal.signer2", "value": false},
 {"key": "sign.signer2", "value": true, "bbox_2d": [557, 678, 587, 694], "page": 1},
 {"key": "seal.signer3", "value": false},
 {"key": "sign.signer3", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [144, 58, 203, 99], "page": 1},
 {"key": "sign.staff.책임자", "value": false},
 {"key": "seal.staff.관리자", "value": false},
 {"key": "sign.staff.관리자", "value": true, "bbox_2d": [207, 56, 273, 101], "page": 1},
 {"key": "seal.staff.부점장", "value": true, "bbox_2d": [280, 60, 332, 97], "page": 1},
 {"key": "sign.staff.부점장", "value": false},
 {"key": "seal.staff.담당2", "value": true, "bbox_2d": [670, 62, 716, 95], "page": 1},
 {"key": "sign.staff.담당2", "value": false},
 {"key": "seal.staff.책임자2", "value": true, "bbox_2d": [732, 59, 787, 98], "page": 1},
 {"key": "sign.staff.책임자2", "value": false},
 {"key": "seal.staff.관리자2", "value": true, "bbox_2d": [799, 65, 838, 92], "page": 1},
 {"key": "sign.staff.관리자2", "value": false},
 {"key": "seal.staff.부점장2", "value": true, "bbox_2d": [857, 60, 909, 97], "page": 1},
 {"key": "sign.staff.부점장2", "value": false}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf036` → `python -m docgen.formdir card hf036` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf036 --show` · `python -m docgen.preview hf036 --out work/hf036`
