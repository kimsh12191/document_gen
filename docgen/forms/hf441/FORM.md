# 법원보관금 납부서(은행제출용) (`hf441`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf441 · card-hash: 1fa7b8093f88 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 3 (seed 1000000 로 그린 것) · **분류 정답:** 법원보관금 납부서(은행제출용)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf441 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.441 (기타) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 40칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `법원명` | 법원명 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:29 | 묻기 |
| `납부금액` | 납부금액 | amount | 1쪽 [385, 214, 470, 225] | 늘 | 파일 key | 값 종류 `amount` | fields.json:43 | 묻기 |
| `납부자성명` | 납부자성명 | text | 1쪽 [199, 248, 246, 259] | 늘 | 파일 key | 값 종류 `person` | fields.json:57 | 묻기 |
| `납부자주소` | 납부자주소 | text | 1쪽 [197, 299, 531, 310] | 늘 | 파일 key | 값 종류 `address` | fields.json:71 | 묻기 |
| `잔액환급계좌번호` | 잔액환급계좌번호 | number | 1쪽 [277, 349, 347, 360] | 늘 | 파일 key | 값 종류 `amount` | fields.json:85 | 묻기 |
| `은행` | 은행 | text | 1쪽 [426, 349, 489, 360] | 늘 | 파일 key | 값 종류 `bank` | fields.json:99 | 묻기 |
| `account` | 계좌번호 | account_no | 1쪽 [427, 383, 560, 394] | 늘 | 파일 key | 고객 정보 (키 `account`, 없으면 값 종류 `account`) | fields.json:114 | 묻기 |
| `사건번호` | 사건번호 | text | 1쪽 [597, 181, 730, 192] | 늘 | 파일 key | 값 종류 `number` | fields.json:128 | 묻기 |
| `보관금종류` | 보관금종류 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:142 | 묻기 |
| `customer.rrn` | 주민등록번호(사업자등록번호) | rrn | 1쪽 [597, 248, 701, 259] | 늘 | 파일 key | 고객 정보 (키 `customer.rrn`, 없으면 값 종류 `number`) | fields.json:156 | 묻기 |
| `customer.phone` | 전화번호 | phone | 1쪽 [720, 299, 826, 310] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:169 | 묻기 |
| `customer.name` | 예금주 | text | 1쪽 [766, 349, 829, 360] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:182 | 묻기 |
| `date` | 작성일 | date | 1쪽 [375, 467, 556, 483] | 늘 | 파일 key | 작성일 | fields.json:196 | 묻기 |
| `signer.name` | 납부당사자 | text | 1쪽 [474, 505, 537, 516] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:222 | 묻기 |
| `법원명2` | 법원명 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:241 | 묻기 |
| `납부금액2` | 납부금액 | number | 2쪽 [383, 214, 470, 225] | 늘 | 파일 key | 값 종류 `amount` | fields.json:255 | 묻기 |
| `납부자성명2` | 납부자성명 | text | 2쪽 [199, 248, 246, 259] | 늘 | 파일 key | 값 종류 `person` | fields.json:269 | 묻기 |
| `납부자주소2` | 납부자주소 | text | 2쪽 [202, 299, 537, 310] | 늘 | 파일 key | 값 종류 `address` | fields.json:283 | 묻기 |
| `잔액환급계좌번호2` | 잔액환급계좌번호 | amount | 2쪽 [261, 349, 347, 360] | 늘 | 파일 key | 값 종류 `amount` | fields.json:297 | 묻기 |
| `은행2` | 은행 | text | 2쪽 [428, 349, 491, 360] | 늘 | 파일 key | 값 종류 `bank` | fields.json:311 | 묻기 |
| `account2` | 계좌번호 | account_no | 2쪽 [428, 383, 561, 394] | 늘 | 파일 key | 고객 정보 (키 `account`, 없으면 값 종류 `account`) | fields.json:326 | 묻기 |
| `사건번호2` | 사건번호 | text | 2쪽 [602, 181, 677, 192] | 늘 | 파일 key | 값 종류 `number` | fields.json:340 | 묻기 |
| `보관금종류2` | 보관금종류 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:354 | 묻기 |
| `customer.rrn2` | 주민등록번호(사업자등록번호) | rrn | 2쪽 [596, 248, 699, 259] | 늘 | 파일 key | 고객 정보 (키 `customer.rrn`, 없으면 값 종류 `number`) | fields.json:368 | 묻기 |
| `customer.phone2` | 전화번호 | phone | 2쪽 [718, 299, 823, 310] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:381 | 묻기 |
| `customer.name2` | 예금주 | text | 2쪽 [765, 349, 828, 360] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:394 | 묻기 |
| `date2` | 작성일 | date | 2쪽 [375, 467, 556, 483] | 늘 | 파일 key | 작성일 | fields.json:408 | 묻기 |
| `법원명3` | 법원명 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:434 | 묻기 |
| `납부금액3` | 납부금액 | number | 3쪽 [400, 214, 470, 225] | 늘 | 파일 key | 값 종류 `amount` | fields.json:448 | 묻기 |
| `납부자성명3` | 납부자성명 | text | 3쪽 [199, 248, 246, 259] | 늘 | 파일 key | 값 종류 `person` | fields.json:462 | 묻기 |
| `납부자주소3` | 납부자주소 | text | 3쪽 [199, 299, 534, 310] | 늘 | 파일 key | 값 종류 `address` | fields.json:476 | 묻기 |
| `잔액환급계좌번호3` | 잔액환급계좌번호 | number | 3쪽 [268, 349, 347, 360] | 늘 | 파일 key | 값 종류 `amount` | fields.json:490 | 묻기 |
| `은행3` | 은행 | text | 3쪽 [430, 349, 493, 360] | 늘 | 파일 key | 값 종류 `bank` | fields.json:504 | 묻기 |
| `account3` | 계좌번호 | account_no | 3쪽 [430, 383, 563, 394] | 늘 | 파일 key | 고객 정보 (키 `account`, 없으면 값 종류 `account`) | fields.json:519 | 묻기 |
| `사건번호3` | 사건번호 | rrn | 3쪽 [596, 181, 715, 192] | 늘 | 파일 key | 값 종류 `number` | fields.json:533 | 묻기 |
| `보관금종류3` | 보관금종류 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:547 | 묻기 |
| `customer.rrn3` | 주민등록번호(사업자등록번호) | rrn | 3쪽 [599, 248, 702, 259] | 늘 | 파일 key | 고객 정보 (키 `customer.rrn`, 없으면 값 종류 `number`) | fields.json:561 | 묻기 |
| `customer.phone3` | 전화번호 | phone | 3쪽 [715, 299, 821, 310] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:574 | 묻기 |
| `customer.name3` | 예금주 | text | 3쪽 [764, 349, 827, 360] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:587 | 묻기 |
| `date3` | 작성일 | date | 3쪽 [375, 467, 556, 483] | 늘 | 파일 key | 작성일 | fields.json:601 | 묻기 |

## 체크·도장·서명 (marks) — 2칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.signer` | 납부당사자 | seal | 1쪽 [629, 503, 689, 518] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:222 | 묻기 |
| `sign.signer` | 납부당사자 | signature | 1쪽 [629, 503, 689, 518] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:222 | 묻기 |

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
"법원보관금 납부서(은행제출용)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2,660,000원",
 "김우예",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "2,050,000",
 "기업은행",
 "540-121210-96628",
 "451-710887-33905",
 "850328-2******",
 "010-6144-1173",
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
"서울특별시 서초구 강남대로 357, 103동 1301호"
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
항목 (키: 설명 (몇 번째 행))
- 납부금액: 납부금액
- 납부자성명: 납부자성명
- 납부자주소: 납부자주소
- 잔액환급계좌번호: 잔액환급계좌번호
- 은행: 은행
- account: 계좌번호
- 사건번호: 사건번호
- customer.rrn: 주민등록번호(사업자등록번호)
- customer.phone: 전화번호
- customer.name: 예금주
- date: 작성일
- signer.name: 납부당사자
```

답:

```json
[{"key": "납부금액", "value": "2,660,000원", "bbox_2d": [385, 214, 470, 225], "page": 1},
 {"key": "납부자성명", "value": "김우예", "bbox_2d": [199, 248, 246, 259], "page": 1},
 {"key": "납부자주소", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [197, 299, 531, 310], "page": 1},
 {"key": "잔액환급계좌번호", "value": "2,050,000", "bbox_2d": [277, 349, 347, 360], "page": 1},
 {"key": "은행", "value": "기업은행", "bbox_2d": [426, 349, 489, 360], "page": 1},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [427, 383, 560, 394], "page": 1},
 {"key": "사건번호", "value": "451-710887-33905", "bbox_2d": [597, 181, 730, 192], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [597, 248, 701, 259], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [720, 299, 826, 310], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [766, 349, 829, 360], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [375, 467, 556, 483], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [474, 505, 537, 516], "page": 1}]
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
- seal.signer: 납부당사자 (같은 설명 중 1번째 칸, 도장)
- sign.signer: 납부당사자 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.signer", "value": false},
 {"key": "sign.signer", "value": true, "bbox_2d": [629, 503, 689, 518], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf441 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf441` → `python -m docgen.formdir card hf441` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf441 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf441 --show` · `python -m docgen.preview hf441 --out work/hf441`
