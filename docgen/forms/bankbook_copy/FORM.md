# 통장사본 (`bankbook_copy`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card bankbook_copy · card-hash: c0b279d39ea0 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** finance · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 통장사본
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 예금통장 첫 면 사본 (스캔본 또는 인터넷 출력본).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 18칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `bank` | 은행명 | text | 1쪽 [112, 88, 232, 110] | 늘 | generate.py | look/template.html.j2:40 | 묻기 |
| `product` | 상품명 | text | 1쪽 [112, 119, 188, 133] | 늘 | generate.py | look/template.html.j2:41 | 묻기 |
| `passbook_no` | 통장번호 | number | 1쪽 [874, 87, 888, 98] | 10/16 | generate.py | look/template.html.j2:50 | 묻기 |
| `account_no` | 계좌번호 | account_no | 1쪽 [621, 110, 757, 123] | 늘 | generate.py | look/template.html.j2:52 | 묻기 |
| `holder` | 예금주 | text | 1쪽 [621, 134, 702, 149] | 늘 | generate.py | look/template.html.j2:47 | 묻기 |
| `opened` | 신규일 | date | 1쪽 [621, 160, 697, 173] | 늘 | generate.py | look/template.html.j2:54 | 묻기 |
| `branch` | 지점명 / 관리점 | text | 1쪽 [621, 183, 686, 196] | 늘 | generate.py | look/template.html.j2:55 | 묻기 |
| `branch_phone` | 지점전화번호 / 관리점전화번호 | phone | 1쪽 [621, 206, 714, 220] | 늘 | generate.py | look/template.html.j2:56 | 묻기 |
| `first_tx.date` | 거래일 | date | 1쪽 [540, 258, 596, 268] | 10/16 | generate.py | look/template.html.j2:60 | 묻기 |
| `first_tx.memo` | 적요 | text | 1쪽 [619, 258, 644, 268] | 10/16 | generate.py | look/template.html.j2:60 | 묻기 |
| `first_tx.amount` | 맡기신금액 | amount | 1쪽 [811, 258, 839, 268] | 10/16 | generate.py | look/template.html.j2:61 | 묻기 |
| `first_tx.balance` | 잔액 | amount | 1쪽 [857, 258, 885, 268] | 10/16 | generate.py | look/template.html.j2:61 | 묻기 |
| `issue_date` | 출력일 | - | - | 6/16 | generate.py | look/template.html.j2:77 | 묻기 |
| `txs.*.date` | 거래일 | - | - (1행) | 3/16 | generate.py | look/template.html.j2:64 | 묻기 |
| `txs.*.memo` | 적요 | - | - (1행) | 3/16 | generate.py | look/template.html.j2:64 | 묻기 |
| `txs.*.in` | 맡기신금액 | - | - (1행) | 3/16 | generate.py | look/template.html.j2:66 | 묻기 |
| `txs.*.balance` | 잔액 | - | - (1행) | 3/16 | generate.py | look/template.html.j2:67 | 묻기 |
| `txs.*.out` | 찾으신금액 | - | - (1행) | 2/16 | generate.py | look/template.html.j2:65 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.registered` | 등록인감 | seal | 1쪽 [178, 385, 235, 425] | 10/16 | generate.py | - | 묻기 |

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
"통장사본"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "국민은행",
 "급여통장",
 "03",
 "478303-40-826627",
 "남궁예태",
 "2019-04-27",
 "분당지점",
 "02-6471-1830",
 "2019.04.27",
 "신규",
 "1,000"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"478303-40-826627"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"분당지점"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- bank: 은행명
- product: 상품명
- passbook_no: 통장번호
- account_no: 계좌번호
- holder: 예금주
- opened: 신규일
- branch: 지점명
- branch_phone: 지점전화번호
- first_tx.date: 거래일
- first_tx.memo: 적요
- first_tx.amount: 맡기신금액
- first_tx.balance: 잔액
```

답:

```json
[{"key": "bank", "value": "국민은행", "bbox_2d": [112, 88, 232, 110], "page": 1},
 {"key": "product", "value": "급여통장", "bbox_2d": [112, 119, 188, 133], "page": 1},
 {"key": "passbook_no", "value": "03", "bbox_2d": [874, 87, 888, 98], "page": 1},
 {"key": "account_no", "value": "478303-40-826627", "bbox_2d": [621, 110, 757, 123], "page": 1},
 {"key": "holder", "value": "남궁예태", "bbox_2d": [621, 134, 702, 149], "page": 1},
 {"key": "opened", "value": "2019-04-27", "bbox_2d": [621, 160, 697, 173], "page": 1},
 {"key": "branch", "value": "분당지점", "bbox_2d": [621, 183, 686, 196], "page": 1},
 {"key": "branch_phone", "value": "02-6471-1830", "bbox_2d": [621, 206, 714, 220], "page": 1},
 {"key": "first_tx.date", "value": "2019.04.27", "bbox_2d": [540, 258, 596, 268], "page": 1},
 {"key": "first_tx.memo", "value": "신규", "bbox_2d": [619, 258, 644, 268], "page": 1},
 {"key": "first_tx.amount", "value": "1,000", "bbox_2d": [811, 258, 839, 268], "page": 1},
 {"key": "first_tx.balance", "value": "1,000", "bbox_2d": [857, 258, 885, 268], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.registered: 등록인감 (도장)
```

답:

```json
[{"key": "seal.registered", "value": true, "bbox_2d": [178, 385, 235, 425], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `generate.py` 가 돌려주는 dict 에 그 키 값 | 미리보기로 확인 → 재검수 → 카드 다시 만들기 |
| 칸 키·항목명 바꾸기 | `look/template.html.j2` 의 `f("키", label=…)` (질문만 바꾸려면 `questions.json`) | `questions … --check` |
| 값이 이상함·칸끼리 안 맞음 | `generate.py` (값 만드는 함수) | 재검수 |
| 모양·표·문구 | `look/template.html.j2` (studio html 편집) | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions bankbook_copy --show` · `python -m docgen.preview bankbook_copy --out work/bankbook_copy`
