# 상생벤더구매론 승인명세 등록신청서 (`hf094`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf094 · card-hash: 7e281a6fa237 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 상생벤더구매론 승인명세 등록신청서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf094 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.94 (대출) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 12칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `차협력기업명` | 차협력기업명 | text | 1쪽 [275, 275, 431, 293] | 늘 | 파일 key | 값 종류 `company` | fields.json:49 | 묻기 |
| `총처리건수` | 총처리건수 | number | 1쪽 [370, 320, 387, 336] | 늘 | 파일 key | 값 종류 `count` | fields.json:63 | 묻기 |
| `차협력기업사업자등록번호` | 차협력기업사업자등록번호 | biz_no | 1쪽 [700, 275, 819, 294] | 늘 | 파일 key | 값 종류 `biz_no` | fields.json:78 | 묻기 |
| `총처리금액` | 총처리금액 | number | 1쪽 [784, 321, 870, 338] | 늘 | 파일 key | 값 종류 `amount` | fields.json:92 | 묻기 |
| `취급점` | 취급점 | text | 1쪽 [236, 216, 311, 233] | 늘 | 파일 key | 값 종류 `branch` | fields.json:107 | 묻기 |
| `date` | 작성일 | date | 1쪽 [416, 408, 604, 425] | 늘 | 파일 key | 작성일 | fields.json:121 | 묻기 |
| `호` | 호 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:148 | 묻기 |
| `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [444, 503, 552, 521] | 늘 | 파일 key | 고객 정보 (키 `company.biz_no`, 없으면 값 종류 `biz_no`) | fields.json:162 | 묻기 |
| `signer.name` | 자 | text | 1쪽 [538, 526, 606, 541] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:175 | 묻기 |
| `소` | 소 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:194 | 묻기 |
| `signer2.name` | 명 | text | 1쪽 [537, 609, 606, 625] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:208 | 묻기 |
| `customer.phone` | 연락처 | phone | 1쪽 [447, 650, 552, 667] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:225 | 묻기 |

## 표 `목록` (표 과제 table·table_read·table_find·table_qa) — 14열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `목록.*.원청채권종류` | 원청채권종류 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:238 | 묻기 |
| `목록.*.원청채권번호` | 원청채권번호 | text | 2쪽 [140, 194, 178, 202] (1행) | 늘 | 파일 key | 값 종류 `number` | fields.json:518 | 묻기 |
| `목록.*.원청구매기업명` | 원청구매기업명 | text | 2쪽 [193, 197, 233, 204] (1행) | 늘 | 파일 key | 값 종류 `company` | fields.json:798 | 묻기 |
| `목록.*.사업자등록번호` | 사업자등록번호 | biz_no | 2쪽 [252, 197, 290, 203] (1행) | 늘 | 파일 key | 값 종류 `biz_no` | fields.json:1078 | 묻기 |
| `목록.*.원청채권금액` | 원청채권금액 | number | 2쪽 [319, 196, 354, 204] (1행) | 늘 | 파일 key | 값 종류 `amount` | fields.json:1358 | 묻기 |
| `목록.*.원청채권발행일` | 원청채권발행일 | date | 2쪽 [368, 196, 405, 203] (1행) | 늘 | 파일 key | 값 종류 `date` | fields.json:1638 | 묻기 |
| `목록.*.원청채권만기일` | 원청채권만기일 | date | 2쪽 [417, 195, 465, 201] (1행) | 늘 | 파일 key | 값 종류 `date` | fields.json:1918 | 묻기 |
| `목록.*.차협력기업명` | 차협력기업명 | text | 2쪽 [480, 197, 522, 204] (1행) | 늘 | 파일 key | 값 종류 `company` | fields.json:2198 | 묻기 |
| `목록.*.승인금액` | 승인금액 | number | 2쪽 [605, 196, 640, 203] (1행) | 늘 | 파일 key | 값 종류 `amount` | fields.json:2758 | 묻기 |
| `목록.*.선입금가능일` | 선입금가능일 | date | 2쪽 [650, 196, 689, 203] (1행) | 늘 | 파일 key | 값 종류 `date` | fields.json:3038 | 묻기 |
| `목록.*.세금계산서승인번호` | 세금계산서승인번호 | rrn | 2쪽 [708, 198, 750, 203] (1행) | 늘 | 파일 key | 값 종류 `number` | fields.json:3318 | 묻기 |
| `목록.*.세금계산서합계금액` | 세금계산서합계금액 | number | 2쪽 [772, 195, 808, 202] (1행) | 늘 | 파일 key | 값 종류 `amount` | fields.json:3598 | 묻기 |
| `목록.*.세금계산서작성일자` | 세금계산서작성일자 | date | 2쪽 [818, 197, 864, 203] (1행) | 늘 | 파일 key | 값 종류 `date` | fields.json:3878 | 묻기 |
| `목록.*.품목명` | 품목명 | text | 2쪽 [879, 194, 919, 206] (1행) | 늘 | 파일 key | 값 종류 `goods` | fields.json:4158 | 묻기 |

## 체크·도장·서명 (marks) — 8칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.signer` | 자 | seal | 1쪽 [712, 527, 734, 539] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:175 | 묻기 |
| `sign.signer` | 자 | signature | 1쪽 [712, 527, 734, 539] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:175 | 묻기 |
| `seal.signer2` | 명 | seal | 1쪽 [707, 600, 739, 636] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:208 | 묻기 |
| `sign.signer2` | 명 | signature | 1쪽 [711, 612, 734, 624] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:208 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [812, 172, 872, 209] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [812, 172, 872, 209] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [872, 172, 918, 209] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [872, 172, 918, 209] | 늘 | - | - | - | 묻기 |

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
"상생벤더구매론 승인명세 등록신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "주식회사 세진산업",
 "12",
 "702-81-38348",
 "37,200,000",
 "센텀지점",
 "남궁예태",
 "010-6144-1173"
]
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
- 차협력기업명: 차협력기업명
- 총처리건수: 총처리건수
- 차협력기업사업자등록번호: 차협력기업사업자등록번호
- 총처리금액: 총처리금액
- 취급점: 취급점
- date: 작성일
- company.biz_no: 사업자등록번호
- signer.name: 자
- signer2.name: 명
- customer.phone: 연락처
```

답:

```json
[{"key": "차협력기업명", "value": "주식회사 세진산업", "bbox_2d": [275, 275, 431, 293], "page": 1},
 {"key": "총처리건수", "value": "12", "bbox_2d": [370, 320, 387, 336], "page": 1},
 {"key": "차협력기업사업자등록번호", "value": "702-81-38348", "bbox_2d": [700, 275, 819, 294], "page": 1},
 {"key": "총처리금액", "value": "37,200,000", "bbox_2d": [784, 321, 870, 338], "page": 1},
 {"key": "취급점", "value": "센텀지점", "bbox_2d": [236, 216, 311, 233], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [416, 408, 604, 425], "page": 1},
 {"key": "company.biz_no", "value": "702-81-38348", "bbox_2d": [444, 503, 552, 521], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [538, 526, 606, 541], "page": 1},
 {"key": "signer2.name", "value": "남궁예태", "bbox_2d": [537, 609, 606, 625], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [447, 650, 552, 667], "page": 1}]
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
- seal.signer: 자 (같은 설명 중 1번째 칸, 도장)
- sign.signer: 자 (같은 설명 중 2번째 칸, 서명)
- seal.signer2: 명 (같은 설명 중 1번째 칸, 도장)
- sign.signer2: 명 (같은 설명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 설명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 설명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 설명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.signer", "value": false},
 {"key": "sign.signer", "value": true, "bbox_2d": [712, 527, 734, 539], "page": 1},
 {"key": "seal.signer2", "value": true, "bbox_2d": [707, 600, 739, 636], "page": 1},
 {"key": "sign.signer2", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": false},
 {"key": "sign.staff.책임자", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf094 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf094` → `python -m docgen.formdir card hf094` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf094 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf094 --show` · `python -m docgen.preview hf094 --out work/hf094`
