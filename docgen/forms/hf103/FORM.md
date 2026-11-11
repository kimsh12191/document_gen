# B2B 전자결제서비스 업무 이용신청서(MP용) (`hf103`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf103 · card-hash: ff7ebae01d0e -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** B2B 전자결제서비스 업무 이용신청서(MP용)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf103 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.103 (대출) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 24칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `company.biz_type` | 업태 | text | 1쪽 [153, 466, 201, 477] | 늘 | 파일 key | 고객 정보 (키 `company.biz_type`, 없으면 값 종류 `text`) | fields.json:23 | 묻기 |
| `company.name` | 기업명(MP상호명) | text | 1쪽 [242, 369, 348, 380] | 늘 | 파일 key | 고객 정보 (키 `company.name`, 없으면 값 종류 `company`) | fields.json:36 | 묻기 |
| `MPURL` | MPURL | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:49 | 묻기 |
| `company.ceo` | 대표자명 | text | 1쪽 [242, 514, 305, 526] | 늘 | 파일 key | 고객 정보 (키 `company.ceo`, 없으면 값 종류 `text`) | fields.json:63 | 묻기 |
| `customer.phone` | 전화번호 | phone | 1쪽 [241, 563, 349, 574] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:76 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [237, 611, 576, 623] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:89 | 묻기 |
| `수수료입금계좌` | 수수료입금계좌 | number | 1쪽 [451, 709, 522, 720] | 늘 | 파일 key | 값 종류 `amount` | fields.json:102 | 묻기 |
| `담당부서` | 담당부서 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:116 | 묻기 |
| `담당자명` | 담당자명 | text | 1쪽 [241, 806, 305, 817] | 늘 | 파일 key | 값 종류 `person` | fields.json:130 | 묻기 |
| `email주소` | e-mail주소 | text | 1쪽 [240, 903, 579, 914] | 늘 | 파일 key | 값 종류 `address` | fields.json:144 | 묻기 |
| `company.biz_item` | 업종 | text | 1쪽 [398, 466, 462, 477] | 늘 | 파일 key | 고객 정보 (키 `company.biz_item`, 없으면 값 종류 `text`) | fields.json:158 | 묻기 |
| `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [708, 369, 808, 380] | 늘 | 파일 key | 고객 정보 (키 `company.biz_no`, 없으면 값 종류 `biz_no`) | fields.json:171 | 묻기 |
| `신용보증` | 신용보증 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:184 | 묻기 |
| `기술보증` | 기술보증 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:199 | 묻기 |
| `지역보증` | 지역보증 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:214 | 묻기 |
| `대표자생년월일` | 대표자생년월일 | date | 1쪽 [706, 514, 786, 526] | 늘 | 파일 key | 값 종류 `date` | fields.json:229 | 묻기 |
| `FAX번호` | FAX번호 | phone | 1쪽 [706, 563, 805, 574] | 늘 | 파일 key | 값 종류 `phone` | fields.json:243 | 묻기 |
| `customer.name` | 예금주명 | text | 1쪽 [708, 709, 772, 720] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:257 | 묻기 |
| `date` | 작성일 | date | 2쪽 [594, 507, 745, 522] | 늘 | 파일 key | 작성일 | fields.json:270 | 묻기 |
| `signer.name` | 성명 | text | 2쪽 [631, 577, 695, 588] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:297 | 묻기 |
| `customer.address2` | 주소 | text | 2쪽 [513, 602, 852, 613] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:316 | 묻기 |
| `선택` | 선택 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:329 | 묻기 |
| `있어야추심등록및대출실행` | 있어야추심등록및대출실행 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:344 | 묻기 |
| `절차필요` | 절차필요 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:359 | 묻기 |

## 체크·도장·서명 (marks) — 2칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.signer` | 성명 | seal | 2쪽 [826, 564, 858, 600] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:297 | 묻기 |
| `sign.signer` | 성명 | signature | 2쪽 [829, 576, 855, 589] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:297 | 묻기 |

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
"B2B 전자결제서비스 업무 이용신청서(MP용)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "제조업",
 "(주)미래케미칼",
 "남궁예태",
 "010-6144-1173",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "7,070,000",
 "화학제품",
 "702-81-38348",
 "2024.04.10",
 "051-509-1176"
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
"서울특별시 서초구 강남대로 357, 103동 1301호"
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
- company.biz_type: 업태
- 홈페이지: 홈페이지
- company.name: 기업명(MP상호명)
- company.ceo: 대표자명
- customer.phone: 전화번호
- customer.address: 주소
- 전문투자자확인증보유자: 전문투자자확인증보유자
- 수수료입금계좌: 수수료입금계좌
- 담당자명: 담당자명
- email주소: e-mail주소
- company.biz_item: 업종
- company.biz_no: 사업자등록번호
- 당좌거래은행: 당좌거래은행
- 대표자생년월일: 대표자생년월일
- FAX번호: FAX번호
- customer.name: 예금주명
```

답:

```json
[{"key": "company.biz_type", "value": "제조업", "bbox_2d": [153, 466, 201, 477], "page": 1},
 {"key": "홈페이지", "value": null},
 {"key": "company.name", "value": "(주)미래케미칼", "bbox_2d": [242, 369, 348, 380], "page": 1},
 {"key": "company.ceo", "value": "남궁예태", "bbox_2d": [242, 514, 305, 526], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [241, 563, 349, 574], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [237, 611, 576, 623], "page": 1},
 {"key": "전문투자자확인증보유자", "value": null},
 {"key": "수수료입금계좌", "value": "7,070,000", "bbox_2d": [451, 709, 522, 720], "page": 1},
 {"key": "담당자명", "value": "남궁예태", "bbox_2d": [241, 806, 305, 817], "page": 1},
 {"key": "email주소", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [240, 903, 579, 914], "page": 1},
 {"key": "company.biz_item", "value": "화학제품", "bbox_2d": [398, 466, 462, 477], "page": 1},
 {"key": "company.biz_no", "value": "702-81-38348", "bbox_2d": [708, 369, 808, 380], "page": 1},
 {"key": "당좌거래은행", "value": null},
 {"key": "대표자생년월일", "value": "2024.04.10", "bbox_2d": [706, 514, 786, 526], "page": 1},
 {"key": "FAX번호", "value": "051-509-1176", "bbox_2d": [706, 563, 805, 574], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [708, 709, 772, 720], "page": 1}]
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

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf103 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf103` → `python -m docgen.formdir card hf103` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf103 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf103 --show` · `python -m docgen.preview hf103 --out work/hf103`
