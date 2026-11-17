# CMSiNet 지사정보 등록신청서 (`hf357`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf357 · card-hash: a854d9584ecd -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** CMSiNet 지사정보 등록신청서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf357 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.357 (전자금융) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 9칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `company.corp_no` | 법인등록번호 | corp_reg_no | 1쪽 [591, 156, 721, 168] | 늘 | 파일 key | 고객 정보 (키 `company.corp_no`, 없으면 값 종류 `number`) | fields.json:17 | 묻기 |
| `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [263, 246, 371, 259] | 늘 | 파일 key | 고객 정보 (키 `company.biz_no`, 없으면 값 종류 `biz_no`) | fields.json:31 | 묻기 |
| `사업자명` | 사업자명 | text | 1쪽 [263, 340, 379, 353] | 늘 | 파일 key | 값 종류 `company` | fields.json:74 | 묻기 |
| `사업자대표` | 사업자대표 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:88 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [264, 388, 633, 401] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:102 | 묻기 |
| `customer.address2` | 주소 | text | 1쪽 [260, 412, 629, 425] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:115 | 묻기 |
| `customer.phone` | 전화번호 | phone | 1쪽 [266, 460, 382, 472] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:128 | 묻기 |
| `팩스번호` | 팩스번호 | phone | 1쪽 [261, 484, 368, 496] | 늘 | 파일 key | 값 종류 `phone` | fields.json:142 | 묻기 |
| `customer.email` | e-mail | text | 1쪽 [263, 508, 431, 520] | 늘 | 파일 key | 고객 정보 (키 `customer.email`, 없으면 값 종류 `text`) | fields.json:157 | 묻기 |

## 표 `목록` (표 과제 table·table_read·table_find·table_qa) — 6열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `목록.*.실행자ID` | 실행자ID | text | 1쪽 [79, 626, 162, 638] (1행) | 늘 | 파일 key | 값 종류 `number` | fields.json:171 | 묻기 |
| `목록.*.통화` | 통화 | text | 1쪽 [213, 626, 250, 638] (1행) | 늘 | 파일 key | 값 종류 `currency` | fields.json:241 | 묻기 |
| `목록.*.계좌번호` | 계좌번호 | text | 1쪽 [275, 627, 396, 637] (1행) | 늘 | 파일 key | 값 종류 `account` | fields.json:311 | 묻기 |
| `목록.*.예금주명` | 예금주명 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:381 | 묻기 |
| `목록.*.인감서명` | 인감/서명 | text | - (1행) | 늘 | 파일 key | 값 종류 `seal` | fields.json:451 | 묻기 |
| `목록.*.개설점` | 개설점 | text | 1쪽 [715, 614, 785, 627] (1행) | 늘 | 파일 key | 값 종류 `branch` | fields.json:521 | 묻기 |

## 체크·도장·서명 (marks) — 3칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.하나해외지점법인주1고객` | 하나해외지점/법인주1)고객 | checkbox (예 (아래내용 필수기입)) | 1쪽 [461, 269, 636, 283] | 늘 | 파일 key | 보기 중 고름: 예 (아래내용 필수기입) | fields.json:44 | 묻기 |
| `check.아래의사업장을CMSiN` | 아래의사업장을CMSiNet지사로등록하여주시기바랍니다. | checkbox (아래의 사업장을 CMS iNet 지사로 등록하여 주시기 바랍니다.) | 1쪽 [71, 223, 492, 237] | 늘 | 파일 key | 보기 중 고름: 아래의 사업장을 CMS iNet 지사로 등록하여 주시기 바랍니다. | fields.json:671 | 묻기 |
| `check.지사출금계좌` | 지사출금계좌 | checkbox (지사 출금계좌) | 1쪽 [71, 564, 186, 579] | 늘 | 파일 key | 보기 중 고름: 지사 출금계좌 | fields.json:695 | 묻기 |

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
"CMSiNet 지사정보 등록신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "200112-7951835",
 "702-81-38348",
 "(주)미래케미칼",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "010-6144-1173",
 "051-509-1176",
 "yetae741@gmail.com",
 "1233-6617",
 "222770-5238335",
 "AUD",
 "CNY",
 "521-964856-91657",
 "983-180523-28876",
 "센텀지점"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"200112-7951835"
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
- company.corp_no: 법인등록번호
- company.biz_no: 사업자등록번호
- 사업자명: 사업자명
- 사업자대표: 사업자대표
- customer.address: 주소 (같은 설명 중 1번째 칸)
- customer.address2: 주소 (같은 설명 중 2번째 칸)
- customer.phone: 전화번호
- 팩스번호: 팩스번호
- customer.email: e-mail
```

답:

```json
[{"key": "company.corp_no", "value": "200112-7951835", "bbox_2d": [591, 156, 721, 168], "page": 1},
 {"key": "company.biz_no", "value": "702-81-38348", "bbox_2d": [263, 246, 371, 259], "page": 1},
 {"key": "사업자명", "value": "(주)미래케미칼", "bbox_2d": [263, 340, 379, 353], "page": 1},
 {"key": "사업자대표", "value": null},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [264, 388, 633, 401], "page": 1},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [260, 412, 629, 425], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [266, 460, 382, 472], "page": 1},
 {"key": "팩스번호", "value": "051-509-1176", "bbox_2d": [261, 484, 368, 496], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [263, 508, 431, 520], "page": 1}]
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
- check.하나해외지점법인주1고객: 하나해외지점/법인주1)고객 (체크박스, 보기: 예 (아래내용 필수기입))
- check.아래의사업장을CMSiN: 아래의사업장을CMSiNet지사로등록하여주시기바랍니다. (체크박스, 보기: 아래의 사업장을 CMS iNet 지사로 등록하여 주시기 바랍니다.)
- check.지사출금계좌: 지사출금계좌 (체크박스, 보기: 지사 출금계좌)
```

답:

```json
[{"key": "check.하나해외지점법인주1고객", "value": null},
 {"key": "check.아래의사업장을CMSiN", "value": null},
 {"key": "check.지사출금계좌", "value": null}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 '계좌번호'·'인감/서명' 열이 있는 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 설명)
- 실행자ID: 실행자ID
- 통화: 통화
- 계좌번호: 계좌번호
- 개설점: 개설점
- 예금주명: 예금주명
- 인감서명: 인감/서명
```

답:

```json
{
 "columns": [
  "실행자ID",
  "통화",
  "계좌번호",
  "개설점",
  "예금주명",
  "인감서명"
 ],
 "rows": [
  [
   "1233-6617",
   "AUD",
   "521-964856-91657",
   "센텀지점",
   null,
   null
  ],
  [
   "222770-5238335",
   "CNY",
   "983-180523-28876",
   "센텀지점",
   null,
   null
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    79,
    614,
    785,
    638
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    79,
    638,
    781,
    686
   ],
   "page": 1
  }
 ]
}
```

### 표 찾기 `table_find` · 채점 f1_iou50 (위치)

질문:

```
이 문서에서 표를 모두 찾아 JSON 목록으로 답하세요. 여기서 표는 같은 항목 묶음(열)이 행마다 되풀이되고 행 수가 서류마다 달라지는 목록입니다. 항목명과 값이 번갈아 있는 신청서 칸, 칸 수가 정해진 결재란은 표가 아닙니다.
표마다 {{"columns": [머리글 글자, …], "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호, "n_rows": 행 수}} 를 쓰고, 여러 쪽에 걸친 표는 쪽마다 따로 씁니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 행 수에는 머리글·합계 행과 모두 빈 행을 넣지 않습니다. 표가 없으면 [] 로 답하세요.
```

답:

```json
[{"columns": ["실행자ID", "통화", "계좌번호", "개설점", "예금주명", "인감/서명"], "bbox_2d": [79, 614, 785, 686], "page": 1, "n_rows": 2}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 표를 보고 답하세요. 표의 행은 모두 몇 개입니까? 머리글·합계 행과 모두 빈 행은 세지 않습니다. (숫자만 답하세요)
```

답:

```json
2
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 표를 보고 답하세요. '실행자ID' 칸이 '1233-6617'인 행의 '예금주명' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
null
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf357 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf357` → `python -m docgen.formdir card hf357` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf357 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf357 --show` · `python -m docgen.preview hf357 --out work/hf357`
