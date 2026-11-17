# 통장사본 (`bankbook_copy`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card bankbook_copy · card-hash: 9f1464f5f00c -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** finance · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 통장사본
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa bankbook_copy --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 예금통장 첫 면 사본 (스캔본 또는 인터넷 출력본).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 13칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank` | 은행명 | text | 1쪽 [112, 88, 232, 110] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:10 | 묻기 |
| `product` | 상품명 | text | 1쪽 [112, 119, 188, 133] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:75 | 묻기 |
| `passbook_no` | 통장번호 | number | 1쪽 [874, 87, 888, 98] | 10/16 | 템플릿 | generate.py | look/template.html.j2:50 · fields.json:70 | 묻기 |
| `account_no` | 계좌번호 | account_no | 1쪽 [621, 110, 757, 123] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:5 | 묻기 |
| `holder` | 예금주 | text | 1쪽 [621, 134, 702, 149] | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:50 | 묻기 |
| `opened` | 신규일 | date | 1쪽 [621, 160, 697, 173] | 늘 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:65 | 묻기 |
| `branch` | 지점명 / 관리점 | text | 1쪽 [621, 183, 686, 196] | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:15 | 묻기 |
| `branch_phone` | 지점전화번호 / 관리점전화번호 | phone | 1쪽 [621, 206, 714, 220] | 늘 | 템플릿 | generate.py | look/template.html.j2:56 · fields.json:20 | 묻기 |
| `first_tx.date` | 거래일 | date | 1쪽 [540, 258, 596, 268] | 10/16 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:40 | 묻기 |
| `first_tx.memo` | 적요 | text | 1쪽 [619, 258, 644, 268] | 10/16 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:45 | 묻기 |
| `first_tx.amount` | 맡기신금액 | amount | 1쪽 [811, 258, 839, 268] | 10/16 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:30 | 묻기 |
| `first_tx.balance` | 잔액 | amount | 1쪽 [857, 258, 885, 268] | 10/16 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:35 | 묻기 |
| `issue_date` | 출력일 | - | - | 6/16 | 템플릿 | generate.py | look/template.html.j2:77 · fields.json:55 | 묻기 |

## 표 `txs` (표 과제 table·table_read·table_find·table_qa) — 5열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `txs.*.date` | 거래일 | - | - (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:64 · fields.json:100 | 묻기 |
| `txs.*.memo` | 적요 | - | - (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:64 · fields.json:110 | 묻기 |
| `txs.*.in` | 맡기신금액 | - | - (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:66 · fields.json:105 | 묻기 |
| `txs.*.balance` | 잔액 | - | - (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:67 · fields.json:95 | 묻기 |
| `txs.*.out` | 찾으신금액 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:115 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.registered` | 등록인감 | seal | 1쪽 [178, 385, 235, 425] | 10/16 | 템플릿 | generate.py | fields.json:80 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키는·값은:** 어디서 정해지나. 키·값 종류는 이 서식 파일에 적힌 그대로입니다 (모든 서식 공통 키 사전은 없음). "키 설명 그대로" 는 칸에 `"key"` 가 없어 키 설명이 키로 나가는 것. 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
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
항목 (키: 설명 (몇 번째 행))
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
- seal.registered: 등록인감 (도장)
```

답:

```json
[{"key": "seal.registered", "value": true, "bbox_2d": [178, 385, 235, 425], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa bankbook_copy --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check bankbook_copy` → `python -m docgen.formdir card bankbook_copy` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `generate.py` 가 돌려주는 dict 에 그 키 값 | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` | 다시 |
| 답의 값 | `generate.py` (값 만드는 함수). 파이썬 대신 정하려면 `fields.json` 의 그 칸 `source` | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (파일로). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa bankbook_copy --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions bankbook_copy --show` · `python -m docgen.preview bankbook_copy --out work/bankbook_copy`
