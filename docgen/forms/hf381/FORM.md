# 장외파생상품 일반투자자 (부)적정성 판단보고서 (`hf381`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf381 · card-hash: 22250deb3c82 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 3 (seed 1000000 로 그린 것) · **분류 정답:** 장외파생상품 일반투자자 (부)적정성 판단보고서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf381 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.381 (파생상품) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 17칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `customer.name` | 고객명 | text | 1쪽 [239, 198, 304, 210] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:29 | 묻기 |
| `customer.birth` | 생년월일및나이 | date | 1쪽 [245, 225, 365, 237] | 늘 | 파일 key | 고객 정보 (키 `customer.birth`, 없으면 값 종류 `date`) | fields.json:42 | 묻기 |
| `고객유형` | 고객유형 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:55 | 묻기 |
| `미성년자고령초고령구분` | 미성년자/고령/초고령구분 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:69 | 묻기 |
| `고객등급` | 고객등급 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:593 | 묻기 |
| `거래가능상품의위험등급` | 거래가능상품의위험등급 | text | 1쪽 [654, 861, 756, 872] | 늘 | 파일 key | 값 종류 `product` | fields.json:607 | 묻기 |
| `거래목적위험회피목적여부` | 거래목적-위험회피목적여부 | text | 1쪽 [314, 524, 384, 535] | 늘 | 파일 key | 값 종류 `reason` | fields.json:621 | 묻기 |
| `위험의속성및규모에따른적합여부` | 위험의속성및규모에따른적합여부 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:636 | 묻기 |
| `장외파생상품에대한지식보유정도` | 장외파생상품에대한지식보유정도 | text | 1쪽 [351, 699, 460, 711] | 늘 | 파일 key | 값 종류 `product` | fields.json:651 | 묻기 |
| `장외파생상품을취득처분한경험` | 장외파생상품을취득·처분한경험 | text | 1쪽 [331, 787, 433, 798] | 늘 | 파일 key | 값 종류 `product` | fields.json:666 | 묻기 |
| `항목점수` | 항목점수 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1041 | 묻기 |
| `거래목적위험회피목적여부2` | 거래목적-위험회피목적여부 | text | 2쪽 [307, 256, 377, 268] | 늘 | 파일 key | 값 종류 `reason` | fields.json:1056 | 묻기 |
| `customer.name2` | 고객명 | text | 3쪽 [382, 425, 447, 437] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:1071 | 묻기 |
| `agent.name` | 대리인 | text | 3쪽 [385, 486, 450, 497] | 늘 | 파일 key | 고객 정보 (키 `agent.name`, 없으면 값 종류 `text`) | fields.json:1084 | 묻기 |
| `담당자` | 담당자(파생상품투자권유자문인력) | text | 3쪽 [379, 795, 428, 806] | 늘 | 파일 key | 값 종류 `person` | fields.json:1097 | 묻기 |
| `date` | 작성일 | date | 3쪽 [442, 364, 619, 381] | 늘 | 파일 key | 작성일 | fields.json:1111 | 묻기 |
| `date2` | 작성일 | date | 3쪽 [442, 673, 619, 690] | 늘 | 파일 key | 작성일 | fields.json:1137 | 묻기 |

## 체크·도장·서명 (marks) — 29칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.예` | 예 | checkbox (보기1) | 1쪽 [575, 517, 591, 529] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:83 | 묻기 |
| `check.예2` | 예 | checkbox (보기1) | 1쪽 [575, 561, 591, 573] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:113 | 묻기 |
| `check.예3` | 예 | checkbox (보기1) | 1쪽 [575, 604, 591, 616] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:143 | 묻기 |
| `check.예4` | 예 | checkbox (보기1) | 1쪽 [575, 648, 591, 660] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:173 | 묻기 |
| `check.하` | 하 | checkbox (보기1) | 1쪽 [575, 692, 591, 704] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:203 | 묻기 |
| `check.5미만` | 5%미만 | checkbox (보기1) | 1쪽 [596, 736, 613, 748] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:233 | 묻기 |
| `check.년미만` | 년미만 | checkbox (보기1) | 1쪽 [595, 780, 612, 792] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:263 | 묻기 |
| `check.아니오` | 아니오 | checkbox (보기1) | 1쪽 [732, 517, 748, 529] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:293 | 묻기 |
| `check.아니오2` | 아니오 | checkbox (보기1) | 1쪽 [732, 561, 748, 573] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:323 | 묻기 |
| `check.아니오3` | 아니오 | checkbox (보기1) | 1쪽 [732, 604, 748, 616] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:353 | 묻기 |
| `check.아니오4` | 아니오 | checkbox (보기1) | 1쪽 [732, 648, 748, 660] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:383 | 묻기 |
| `check.중` | 중 | checkbox (보기1) | 1쪽 [718, 692, 734, 704] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:413 | 묻기 |
| `check.10미만` | 10%미만 | checkbox (보기1) | 1쪽 [744, 745, 760, 757] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:443 | 묻기 |
| `check.년미만2` | 년미만 | checkbox (보기1) | 1쪽 [738, 789, 755, 800] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:473 | 묻기 |
| `check.상` | 상 | checkbox (보기1) | 1쪽 [858, 692, 874, 704] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:503 | 묻기 |
| `check.10이상` | 10%이상 | checkbox (보기1) | 1쪽 [884, 736, 900, 748] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:533 | 묻기 |
| `check.년이상` | 년이상 | checkbox (보기1) | 1쪽 [879, 780, 895, 792] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:563 | 묻기 |
| `check.적정` | 적정 | checkbox (보기1) | 2쪽 [293, 143, 309, 155] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:681 | 묻기 |
| `check.부적정` | 부적정 | checkbox (보기1) | 2쪽 [445, 143, 462, 155] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:711 | 묻기 |
| `check.미충족항목존재` | 미충족항목존재 | checkbox (보기1) | 2쪽 [833, 134, 850, 146] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:741 | 묻기 |
| `check.상품위험등급대비고객등급미달` | 상품위험등급대비고객등급미달 | checkbox (보기1) | 2쪽 [888, 152, 904, 164] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:771 | 묻기 |
| `check.충족` | 충족 | checkbox (보기1) | 2쪽 [501, 249, 518, 261] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:801 | 묻기 |
| `check.충족2` | 충족 | checkbox (보기1) | 2쪽 [501, 293, 518, 305] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:831 | 묻기 |
| `check.충족3` | 충족 | checkbox (보기1) | 2쪽 [501, 337, 518, 349] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:861 | 묻기 |
| `check.충족4` | 충족 | checkbox (보기1) | 2쪽 [501, 381, 518, 393] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:891 | 묻기 |
| `check.미충족` | 미충족 | checkbox (보기1) | 2쪽 [613, 249, 629, 261] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:921 | 묻기 |
| `check.미충족2` | 미충족 | checkbox (보기1) | 2쪽 [613, 293, 629, 305] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:951 | 묻기 |
| `check.미충족3` | 미충족 | checkbox (보기1) | 2쪽 [613, 337, 629, 349] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:981 | 묻기 |
| `check.미충족4` | 미충족 | checkbox (보기1) | 2쪽 [613, 381, 629, 393] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:1011 | 묻기 |

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
"장외파생상품 일반투자자 (부)적정성 판단보고서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "타행 이체"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"타행 이체"
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
- 거래목적위험회피목적여부2: 거래목적-위험회피목적여부
```

답:

```json
[{"key": "거래목적위험회피목적여부2", "value": "타행 이체", "bbox_2d": [307, 256, 377, 268], "page": 1}]
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
- check.적정: 적정 (체크박스, 보기: 보기1)
- check.부적정: 부적정 (체크박스, 보기: 보기1)
- check.미충족항목존재: 미충족항목존재 (체크박스, 보기: 보기1)
- check.상품위험등급대비고객등급미달: 상품위험등급대비고객등급미달 (체크박스, 보기: 보기1)
- check.충족: 충족 (같은 설명 중 1번째 칸, 체크박스, 보기: 보기1)
- check.충족2: 충족 (같은 설명 중 2번째 칸, 체크박스, 보기: 보기1)
- check.충족3: 충족 (같은 설명 중 3번째 칸, 체크박스, 보기: 보기1)
- check.충족4: 충족 (같은 설명 중 4번째 칸, 체크박스, 보기: 보기1)
- check.미충족: 미충족 (같은 설명 중 1번째 칸, 체크박스, 보기: 보기1)
- check.미충족2: 미충족 (같은 설명 중 2번째 칸, 체크박스, 보기: 보기1)
- check.미충족3: 미충족 (같은 설명 중 3번째 칸, 체크박스, 보기: 보기1)
- check.미충족4: 미충족 (같은 설명 중 4번째 칸, 체크박스, 보기: 보기1)
```

답:

```json
[{"key": "check.적정", "value": null},
 {"key": "check.부적정", "value": null},
 {"key": "check.미충족항목존재", "value": null},
 {"key": "check.상품위험등급대비고객등급미달", "value": "보기1", "bbox_2d": [888, 152, 904, 164], "page": 1},
 {"key": "check.충족", "value": "보기1", "bbox_2d": [501, 249, 518, 261], "page": 1},
 {"key": "check.충족2", "value": null},
 {"key": "check.충족3", "value": "보기1", "bbox_2d": [501, 337, 518, 349], "page": 1},
 {"key": "check.충족4", "value": null},
 {"key": "check.미충족", "value": null},
 {"key": "check.미충족2", "value": "보기1", "bbox_2d": [613, 293, 629, 305], "page": 1},
 {"key": "check.미충족3", "value": null},
 {"key": "check.미충족4", "value": null}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf381 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf381` → `python -m docgen.formdir card hf381` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | studio ① 서식 › 영역 편집에서 그리기 (`fields.json` items 에 한 칸) | 다시 |
| 답의 위치 (박스) | `fields.json` 그 칸의 `rect` [x0, y0, x1, y1] (pt) — 또는 영역 편집 | 다시 |
| 답의 키 | `fields.json` 그 칸에 `"key"` (없으면 키 설명이 그대로 키) | 다시 |
| 답의 값 | `fields.json` 그 칸에 `"source"` ([값 출처 목록](../_common/values.md)) 또는 값 종류 `"kind"` | 다시 |
| 칸의 항목명 | `fields.json` 그 칸의 `label` | 다시 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf381 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf381 --show` · `python -m docgen.preview hf381 --out work/hf381`
