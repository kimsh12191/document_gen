# 보호예수 의뢰서 (`hf005`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf005 · card-hash: 313b34cd8e6d -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 보호예수 의뢰서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf005 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.5 (예금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 10칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `예수수량` | 예수수량 | number | 1쪽 [570, 292, 586, 308] | 늘 | 파일 key | 값 종류 `count` | fields.json:107 | 묻기 |
| `예수품명` | 예수품명 | text | 1쪽 [361, 352, 439, 369] | 늘 | 파일 key | 값 종류 `goods` | fields.json:168 | 묻기 |
| `예수금액` | 예수금액 | number | 1쪽 [850, 380, 917, 397] | 늘 | 파일 key | 값 종류 `amount` | fields.json:184 | 묻기 |
| `증권번호` | 증권번호 | text | 1쪽 [358, 412, 445, 428] | 늘 | 파일 key | 값 종류 `number` | fields.json:200 | 묻기 |
| `signer.name` | 성명(상호명) | text | 1쪽 [309, 884, 381, 901] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:246 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [240, 918, 464, 932] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:265 | 묻기 |
| `customer.birth` | 생년월일(사업자등록번호) | number | 1쪽 [658, 883, 717, 899] | 늘 | 파일 key | 고객 정보 (키 `customer.birth`, 없으면 값 종류 `date`) | fields.json:278 | 묻기 |
| `customer.phone` | 연락처 | phone | 1쪽 [659, 915, 770, 933] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:291 | 묻기 |
| `취급점` | 취급점 | text | 1쪽 [211, 174, 283, 191] | 늘 | 파일 key | 값 종류 `branch` | fields.json:304 | 묻기 |
| `date` | 작성일 | date | 1쪽 [354, 816, 577, 834] | 늘 | 파일 key | 작성일 | fields.json:318 | 묻기 |

## 체크·도장·서명 (marks) — 13칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.예수종류` | 예수종류 | checkbox (봉함예수 / 개봉예수) | 1쪽 [251, 264, 328, 279] | 늘 | 파일 key | 보기 중 고름: 봉함예수 / 개봉예수 | fields.json:61 | 묻기 |
| `check.만기일자` | 만기일자 | checkbox (개월( / 예적금 만기일() | 1쪽 [489, 324, 604, 339] | 늘 | 파일 key | 보기 중 고름: 개월( / 예적금 만기일( | fields.json:122 | 묻기 |
| `check.수령방법` | 수령방법 | checkbox (영업점) | 1쪽 [823, 445, 886, 460] | 늘 | 파일 key | 보기 중 고름: 영업점 | fields.json:216 | 묻기 |
| `seal.signer` | 성명(상호명) | seal | 1쪽 [458, 884, 520, 900] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:246 | 묻기 |
| `sign.signer` | 성명(상호명) | signature | 1쪽 [458, 884, 520, 900] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:246 | 묻기 |
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [656, 40, 699, 71] | 늘 | - | - | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [642, 34, 713, 76] | 늘 | - | - | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [713, 34, 785, 76] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [713, 34, 785, 76] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [797, 39, 844, 72] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [785, 34, 856, 76] | 늘 | - | - | - | 묻기 |
| `seal.staff.부점장` | 부점장 | seal | 1쪽 [867, 39, 912, 71] | 늘 | - | - | - | 묻기 |
| `sign.staff.부점장` | 부점장 | signature | 1쪽 [856, 34, 922, 76] | 늘 | - | - | - | 묻기 |

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
"보호예수 의뢰서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "12",
 "철강 코일",
 "230,000",
 "2953-3297",
 "남궁예태",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "850328",
 "010-6144-1173",
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
"230,000"
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
항목 (키: 설명 (몇 번째 행))
- 예수수량: 예수수량
- 벤더기업명: 벤더기업명
- 기호및번호: 기호및번호
- 예수품명: 예수품명
- 예수금액: 예수금액
- 증권번호: 증권번호
- signer.name: 성명(상호명)
- customer.address: 주소
- customer.birth: 생년월일(사업자등록번호)
- customer.phone: 연락처
- 취급점: 취급점
- date: 작성일
- 임대계약건수: 임대계약건수
```

답:

```json
[{"key": "예수수량", "value": "12", "bbox_2d": [570, 292, 586, 308], "page": 1},
 {"key": "벤더기업명", "value": null},
 {"key": "기호및번호", "value": null},
 {"key": "예수품명", "value": "철강 코일", "bbox_2d": [361, 352, 439, 369], "page": 1},
 {"key": "예수금액", "value": "230,000", "bbox_2d": [850, 380, 917, 397], "page": 1},
 {"key": "증권번호", "value": "2953-3297", "bbox_2d": [358, 412, 445, 428], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [309, 884, 381, 901], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [240, 918, 464, 932], "page": 1},
 {"key": "customer.birth", "value": "850328", "bbox_2d": [658, 883, 717, 899], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [659, 915, 770, 933], "page": 1},
 {"key": "취급점", "value": "센텀지점", "bbox_2d": [211, 174, 283, 191], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [354, 816, 577, 834], "page": 1},
 {"key": "임대계약건수", "value": null}]
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
- check.예수종류: 예수종류 (체크박스, 보기: 봉함예수 / 개봉예수)
- check.만기일자: 만기일자 (체크박스, 보기: 개월( / 예적금 만기일()
- check.수령방법: 수령방법 (체크박스, 보기: 영업점)
- seal.signer: 성명(상호명) (같은 설명 중 1번째 칸, 도장)
- sign.signer: 성명(상호명) (같은 설명 중 2번째 칸, 서명)
- seal.staff.본인확인: 본인확인 (같은 설명 중 1번째 칸, 도장)
- sign.staff.본인확인: 본인확인 (같은 설명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 설명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 설명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 설명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 설명 중 2번째 칸, 서명)
- seal.staff.부점장: 부점장 (같은 설명 중 1번째 칸, 도장)
- sign.staff.부점장: 부점장 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.예수종류", "value": "봉함예수", "bbox_2d": [251, 265, 267, 277], "page": 1},
 {"key": "check.만기일자", "value": "예적금 만기일(", "bbox_2d": [489, 325, 505, 338], "page": 1},
 {"key": "check.수령방법", "value": "영업점", "bbox_2d": [823, 446, 839, 458], "page": 1},
 {"key": "seal.signer", "value": false},
 {"key": "sign.signer", "value": false},
 {"key": "seal.staff.본인확인", "value": true, "bbox_2d": [656, 40, 699, 71], "page": 1},
 {"key": "sign.staff.본인확인", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": true, "bbox_2d": [713, 34, 785, 76], "page": 1},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [797, 39, 844, 72], "page": 1},
 {"key": "sign.staff.책임자", "value": false},
 {"key": "seal.staff.부점장", "value": true, "bbox_2d": [867, 39, 912, 71], "page": 1},
 {"key": "sign.staff.부점장", "value": false}]
```

### 표 찾기 `table_find` · 채점 f1_iou50 (위치)

질문:

```
이 문서에서 표를 모두 찾아 JSON 목록으로 답하세요. 여기서 표는 같은 항목 묶음(열)이 행마다 되풀이되고 행 수가 서류마다 달라지는 목록입니다. 항목명과 값이 번갈아 있는 신청서 칸, 칸 수가 정해진 결재란은 표가 아닙니다.
표마다 {{"columns": [머리글 글자, …], "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호, "n_rows": 행 수}} 를 쓰고, 여러 쪽에 걸친 표는 쪽마다 따로 씁니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 행 수에는 머리글·합계 행과 모두 빈 행을 넣지 않습니다. 표가 없으면 [] 로 답하세요.
```

답:

```json
[]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf005 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf005` → `python -m docgen.formdir card hf005` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf005 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf005 --show` · `python -m docgen.preview hf005 --out work/hf005`
