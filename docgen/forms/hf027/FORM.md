# 위임장(영문) (`hf027`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf027 · card-hash: 929cf48e5585 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 위임장(영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.27 (예금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 14칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `agent.name_en` | Name | text | 1쪽 [343, 170, 550, 192] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:49 | 묻기 |
| `agent.relation_en` | RelationshiptoPrincipal | text | 1쪽 [341, 213, 407, 234] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `agent.address` | Address | text | 1쪽 [342, 254, 796, 282] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:78 | 묻기 |
| `account` | AccountNo. | account_no | 1쪽 [343, 389, 506, 410] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `poa.other_powers_en` | Others | text | 1쪽 [343, 509, 716, 527] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:260 | 묻기 |
| `agent.birth` | DateofBirth | date | 1쪽 [732, 171, 861, 190] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `agent.phone` | ContactInformation | phone | 1쪽 [734, 213, 852, 234] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `bank.confirm_date` | DateofConfirmingPowersGiven | date | 1쪽 [703, 703, 804, 724] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name_en` | Name | text | 1쪽 [358, 770, 538, 795] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:320 | 묻기 |
| `customer.address` | Address | text | 1쪽 [357, 851, 797, 879] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:335 | 묻기 |
| `customer.phone` | ContactInformation | phone | 1쪽 [737, 815, 858, 835] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `bank.branch` | HanaBank___Branch | text | 1쪽 [260, 132, 307, 143] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `date` | Date(MM-DD-YYYY) | date | 1쪽 [384, 633, 556, 656] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.birth` | PrincipalDateofBirth | date | 1쪽 [362, 813, 468, 835] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

## 체크·도장·서명 (marks) — 3칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `check.Pleasetickintherelevantbox` | Pleasetick√intherelevantbox | checkbox (.) | 1쪽 [445, 295, 468, 311] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.AccountOpening` | AccountOpening | checkbox (Savings Deposit / Time Deposit / Installment Deposit / Others () | 1쪽 [579, 339, 708, 355] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.Details` | Details | checkbox (Change of password / Bankbook / Seal loss / Account closing / Others () | 1쪽 [578, 443, 666, 459] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:183 | 묻기 |

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
"위임장(영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "NAMGOONG CHANYUN",
 "Parent",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "540-121210-96628",
 "Inquiry of account balance and transaction history",
 "1952년 10월 28일",
 "010-7568-9115",
 "2024.09.09",
 "NAMGOONG YETAE",
 "010-6144-1173",
 "센텀지점",
 "2025년 04월 01일",
 "1985-03-28"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"NAMGOONG CHANYUN"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"Parent"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- agent.name_en: Name (같은 항목명 중 1번째 칸)
- agent.relation_en: RelationshiptoPrincipal
- agent.address: Address (대리인 주소, 같은 항목명 중 1번째 칸)
- account: AccountNo.
- poa.other_powers_en: Others
- agent.birth: DateofBirth (대리인 생년월일)
- agent.phone: ContactInformation (대리인 연락처, 같은 항목명 중 1번째 칸)
- bank.confirm_date: DateofConfirmingPowersGiven
- customer.name_en: Name (고객 영문 성명, 같은 항목명 중 2번째 칸)
- customer.address: Address (고객 주소, 같은 항목명 중 2번째 칸)
- customer.phone: ContactInformation (고객 연락처, 같은 항목명 중 2번째 칸)
- bank.branch: HanaBank___Branch
- date: Date(MM-DD-YYYY)
- customer.birth: PrincipalDateofBirth (고객 생년월일)
```

답:

```json
[{"key": "agent.name_en", "value": "NAMGOONG CHANYUN", "bbox_2d": [343, 170, 550, 192], "page": 1},
 {"key": "agent.relation_en", "value": "Parent", "bbox_2d": [341, 213, 407, 234], "page": 1},
 {"key": "agent.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [342, 254, 796, 282], "page": 1},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [343, 389, 506, 410], "page": 1},
 {"key": "poa.other_powers_en", "value": "Inquiry of account balance and transaction history", "bbox_2d": [343, 509, 716, 527], "page": 1},
 {"key": "agent.birth", "value": "1952년 10월 28일", "bbox_2d": [732, 171, 861, 190], "page": 1},
 {"key": "agent.phone", "value": "010-7568-9115", "bbox_2d": [734, 213, 852, 234], "page": 1},
 {"key": "bank.confirm_date", "value": "2024.09.09", "bbox_2d": [703, 703, 804, 724], "page": 1},
 {"key": "customer.name_en", "value": "NAMGOONG YETAE", "bbox_2d": [358, 770, 538, 795], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [357, 851, 797, 879], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [737, 815, 858, 835], "page": 1},
 {"key": "bank.branch", "value": "센텀지점", "bbox_2d": [260, 132, 307, 143], "page": 1},
 {"key": "date", "value": "2025년 04월 01일", "bbox_2d": [384, 633, 556, 656], "page": 1},
 {"key": "customer.birth", "value": "1985-03-28", "bbox_2d": [362, 813, 468, 835], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- check.Pleasetickintherelevantbox: Pleasetick√intherelevantbox (체크박스, 보기: .)
- check.AccountOpening: AccountOpening (체크박스, 보기: Savings Deposit / Time Deposit / Installment Deposit / Others ()
- check.Details: Details (체크박스, 보기: Change of password / Bankbook / Seal loss / Account closing / Others ()
```

답:

```json
[{"key": "check.Pleasetickintherelevantbox", "value": ".", "bbox_2d": [445, 298, 462, 311], "page": 1},
 {"key": "check.AccountOpening", "value": "Time Deposit", "bbox_2d": [579, 341, 596, 354], "page": 1},
 {"key": "check.Details", "value": "Others (", "bbox_2d": [578, 446, 595, 459], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf027 --show` · `python -m docgen.preview hf027 --out work/hf027`
