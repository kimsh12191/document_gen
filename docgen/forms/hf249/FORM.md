# 주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(국문) (`hf249`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf249 · card-hash: 33056434c48a -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(국문)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf249 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.249 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 38칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `접수일` | 접수일 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:49 | 묻기 |
| `처리일` | 처리일 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:63 | 묻기 |
| `date` | 신고(허가)일 | date | 1쪽 [289, 141, 405, 167] | 늘 | 파일 key | 고객 정보 (키 `date`, 없으면 값 종류 `date`) | fields.json:77 | 묻기 |
| `하려는` | 하려는(하고있는사업) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:90 | 묻기 |
| `상호또는명칭` | 상호또는명칭 | text | 1쪽 [434, 165, 611, 194] | 늘 | 파일 key | 값 종류 `company` | fields.json:104 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [375, 197, 771, 223] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:118 | 묻기 |
| `상호또는명칭2` | 상호또는명칭 | text | 1쪽 [431, 230, 601, 258] | 늘 | 파일 key | 값 종류 `company` | fields.json:132 | 묻기 |
| `customer.nationality` | 국적 | text | 1쪽 [372, 262, 458, 288] | 늘 | 파일 key | 고객 정보 (키 `customer.nationality`, 없으면 값 종류 `text`) | fields.json:147 | 묻기 |
| `변경후내용` | 변경후내용 | text | 1쪽 [743, 368, 839, 394] | 늘 | 파일 key | 값 종류 `note` | fields.json:160 | 묻기 |
| `취득총액원` | 취득총액:원(USD상당) | number | 1쪽 [829, 302, 858, 327] | 늘 | 파일 key | 값 종류 `percent` | fields.json:174 | 묻기 |
| `date2` | 작성일 | date | 1쪽 [675, 475, 924, 490] | 늘 | 파일 key | 작성일 | fields.json:190 | 묻기 |
| `signer.name` | 신고인또는신청인(또는대리인) | text | 1쪽 [636, 495, 712, 517] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:216 | 묻기 |
| `신고번호` | 신고(허가)번호 | text | 1쪽 [174, 580, 266, 602] | 늘 | 파일 key | 값 종류 `number` | fields.json:235 | 묻기 |
| `date3` | 작성일 | date | 1쪽 [675, 626, 924, 642] | 늘 | 파일 key | 작성일 | fields.json:249 | 묻기 |
| `접수번호` | 접수번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:275 | 묻기 |
| `외국인` | 외국인 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:290 | 묻기 |
| `변경사항` | 변경사항 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:305 | 묻기 |
| `이미신고된내용` | 이미신고(허가)된내용 | text | 1쪽 [509, 374, 587, 395] | 늘 | 파일 key | 값 종류 `note` | fields.json:320 | 묻기 |
| `변경내용` | 변경내용 | text | 1쪽 [180, 400, 276, 426] | 늘 | 파일 key | 값 종류 `note` | fields.json:335 | 묻기 |
| `접수일2` | 접수일 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:350 | 묻기 |
| `처리일2` | 처리일 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:364 | 묻기 |
| `date4` | 신고(허가)일 | date | 2쪽 [286, 139, 402, 167] | 늘 | 파일 key | 고객 정보 (키 `date`, 없으면 값 종류 `date`) | fields.json:378 | 묻기 |
| `하려는2` | 하려는(하고있는사업) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:391 | 묻기 |
| `상호또는명칭3` | 상호또는명칭 | text | 2쪽 [440, 167, 561, 193] | 늘 | 파일 key | 값 종류 `company` | fields.json:405 | 묻기 |
| `customer.address2` | 주소 | text | 2쪽 [373, 195, 768, 227] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:419 | 묻기 |
| `상호또는명칭4` | 상호또는명칭 | text | 2쪽 [432, 231, 583, 259] | 늘 | 파일 key | 값 종류 `company` | fields.json:433 | 묻기 |
| `customer.nationality2` | 국적 | text | 2쪽 [376, 261, 462, 287] | 늘 | 파일 key | 고객 정보 (키 `customer.nationality`, 없으면 값 종류 `text`) | fields.json:448 | 묻기 |
| `변경후내용2` | 변경후내용 | text | 2쪽 [741, 369, 837, 395] | 늘 | 파일 key | 값 종류 `note` | fields.json:461 | 묻기 |
| `취득총액원2` | 취득총액:원(USD상당) | number | 2쪽 [829, 303, 856, 328] | 늘 | 파일 key | 값 종류 `percent` | fields.json:475 | 묻기 |
| `date5` | 작성일 | date | 2쪽 [675, 475, 924, 490] | 늘 | 파일 key | 작성일 | fields.json:491 | 묻기 |
| `signer2.name` | 신고인또는신청인(또는대리인) | text | 2쪽 [636, 494, 713, 516] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:517 | 묻기 |
| `신고번호2` | 신고(허가)번호 | text | 2쪽 [173, 580, 269, 601] | 늘 | 파일 key | 값 종류 `number` | fields.json:536 | 묻기 |
| `date6` | 작성일 | date | 2쪽 [675, 626, 924, 642] | 늘 | 파일 key | 작성일 | fields.json:550 | 묻기 |
| `접수번호2` | 접수번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:576 | 묻기 |
| `외국인2` | 외국인 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:591 | 묻기 |
| `변경사항2` | 변경사항 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:606 | 묻기 |
| `이미신고된내용2` | 이미신고(허가)된내용 | text | 2쪽 [508, 376, 585, 396] | 늘 | 파일 key | 값 종류 `note` | fields.json:621 | 묻기 |
| `변경내용2` | 변경내용 | text | 2쪽 [178, 399, 274, 426] | 늘 | 파일 key | 값 종류 `note` | fields.json:636 | 묻기 |

## 체크·도장·서명 (marks) — 8칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.signer` | 신고인또는신청인(또는대리인) | seal | 1쪽 [841, 499, 924, 512] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:216 | 묻기 |
| `sign.signer` | 신고인또는신청인(또는대리인) | signature | 1쪽 [841, 499, 924, 512] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:216 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [791, 36, 840, 70] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [786, 31, 845, 75] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [856, 34, 910, 72] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [845, 31, 920, 75] | 늘 | - | - | - | 묻기 |
| `seal.signer2` | 신고인또는신청인(또는대리인) | seal | 2쪽 [841, 499, 924, 512] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:517 | 묻기 |
| `sign.signer2` | 신고인또는신청인(또는대리인) | signature | 2쪽 [841, 499, 924, 512] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:517 | 묻기 |

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
"주식등의 취득 또는 출연방식에 의한 외국인투자 내용변경 신고서, 허가신청서(국문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2025.04.01",
 "제일물산(주)",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "(주)미래케미칼",
 "대한민국",
 "해당 없음",
 "50",
 "남궁예태",
 "5054-0268"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"제일물산(주)"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"50"
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
- date4: 신고(허가)일
- 라신용장번호: 라.신용장번호
- 상호또는명칭3: 상호또는명칭 (같은 설명 중 1번째 칸)
- customer.address2: 주소
- 상호또는명칭4: 상호또는명칭 (같은 설명 중 2번째 칸)
- customer.nationality2: 국적
- 변경후내용2: 변경후내용
- 취득총액원2: 취득총액:원(USD상당)
- date5: 작성일 (같은 설명 중 1번째 칸)
- signer2.name: 신고인또는신청인(또는대리인)
- 신고번호2: 신고(허가)번호
- date6: 작성일 (같은 설명 중 2번째 칸)
- 이미신고된내용2: 이미신고(허가)된내용
- 변경내용2: 변경내용
```

답:

```json
[{"key": "date4", "value": "2025.04.01", "bbox_2d": [286, 139, 402, 167], "page": 1},
 {"key": "라신용장번호", "value": null},
 {"key": "상호또는명칭3", "value": "제일물산(주)", "bbox_2d": [440, 167, 561, 193], "page": 1},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [373, 195, 768, 227], "page": 1},
 {"key": "상호또는명칭4", "value": "(주)미래케미칼", "bbox_2d": [432, 231, 583, 259], "page": 1},
 {"key": "customer.nationality2", "value": "대한민국", "bbox_2d": [376, 261, 462, 287], "page": 1},
 {"key": "변경후내용2", "value": "해당 없음", "bbox_2d": [741, 369, 837, 395], "page": 1},
 {"key": "취득총액원2", "value": "50", "bbox_2d": [829, 303, 856, 328], "page": 1},
 {"key": "date5", "value": "2025년 4월 1일", "bbox_2d": [675, 475, 924, 490], "page": 1},
 {"key": "signer2.name", "value": "남궁예태", "bbox_2d": [636, 494, 713, 516], "page": 1},
 {"key": "신고번호2", "value": "5054-0268", "bbox_2d": [173, 580, 269, 601], "page": 1},
 {"key": "date6", "value": "2025년 4월 1일", "bbox_2d": [675, 626, 924, 642], "page": 1},
 {"key": "이미신고된내용2", "value": "해당 없음", "bbox_2d": [508, 376, 585, 396], "page": 1},
 {"key": "변경내용2", "value": "해당 없음", "bbox_2d": [178, 399, 274, 426], "page": 1}]
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
- seal.signer2: 신고인또는신청인(또는대리인) (같은 설명 중 1번째 칸, 도장)
- sign.signer2: 신고인또는신청인(또는대리인) (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.signer2", "value": false},
 {"key": "sign.signer2", "value": true, "bbox_2d": [841, 499, 924, 512], "page": 1}]
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

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf249 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf249` → `python -m docgen.formdir card hf249` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf249 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf249 --show` · `python -m docgen.preview hf249 --out work/hf249`
