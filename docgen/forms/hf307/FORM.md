# 지급수단등의 수출입(변경)신고서 (`hf307`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf307 · card-hash: 7f7d667b3edc -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 지급수단등의 수출입(변경)신고서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf307 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.307 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 16칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `종류` | 종류 | text | 1쪽 [316, 200, 426, 212] | 늘 | 항목명 그대로 | 값 종류 `product` (항목명 자동) | fields.json:17 | 묻기 |
| `수량` | 수량 | number | 1쪽 [615, 237, 624, 249] | 늘 | 항목명 그대로 | 값 종류 `count` (항목명 자동) | fields.json:29 | 묻기 |
| `수출입금액` | 수출입금액 | number | 1쪽 [875, 274, 925, 286] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:41 | 묻기 |
| `대가결제방법` | 대가결제방법 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:53 | 묻기 |
| `corp.name` ← `company.name` | 상호 | text | 1쪽 [317, 348, 426, 360] | 늘 | 규칙: '상 호' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:65 | 묻기 |
| `corp.ceo` ← `company.ceo` | 대표자 | text | 1쪽 [315, 385, 381, 397] | 늘 | 규칙: '대 표 자' → `company.ceo` | 고객 정보 (키 `company.ceo`) | fields.json:77 | 묻기 |
| `corp.address` ← `company.address` | 소재지 | text | 1쪽 [314, 422, 626, 434] | 늘 | 규칙: '소 재 지' → `company.address` | 고객 정보 (키 `company.address`) | fields.json:89 | 묻기 |
| `기타` | 기타(또는변경내용) | text | 1쪽 [316, 459, 386, 471] | 늘 | 항목명 그대로 | 값 종류 `note` (항목명 자동) | fields.json:101 | 묻기 |
| `신고번호` | 신고번호 | rrn | 1쪽 [712, 701, 836, 712] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:112 | 묻기 |
| `신고금액` | 신고금액 | number | 1쪽 [866, 738, 925, 750] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:123 | 묻기 |
| `date` | 신고일자 | date | 1쪽 [713, 775, 844, 787] | 늘 | 규칙: '신 고 일 자' → `date` | 고객 정보 (키 `date`) | fields.json:134 | 묻기 |
| `유효기간` | 유효기간 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:145 | 묻기 |
| `처리기간` | 처리기간 | text | - | 늘 | 표 행 (묶음·항목명 '처 리 기 간') | 값 종류 `skip` (항목명 자동) | fields.json:156 | 묻기 |
| `date2` | 작성일 | date | 1쪽 [694, 528, 897, 547] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:170 | 묻기 |
| `company.name2` | 상호 | text | 1쪽 [299, 589, 409, 600] | 늘 | 규칙: '상 호' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:195 | 묻기 |
| `company.ceo2` | 대표자 | text | 1쪽 [476, 608, 541, 619] | 늘 | 규칙: '대 표 자' → `company.ceo` | 고객 정보 (키 `company.ceo`) | fields.json:206 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키 `a` ← `b`:** 질문·정답은 공통 키 a, 서식의 원래 키는 b (키 사전이 정함).
- **키는·값은:** 어디서 정해지나. 원본 서식의 "규칙"·"항목명 자동" 은 키 사전(studio 키 사전 화면, `_common/key_rules.json`)이 항목명으로 정한 것 — 모든 서식에 같이 적용. 이 서식의 그 칸만 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
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
"지급수단등의 수출입(변경)신고서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "하나 TDF 2040",
 "3",
 "80,000",
 "(주)미래케미칼",
 "남궁예태",
 "제주특별자치도 제주시 첨단로 381-19, 2층",
 "해당 없음",
 "525941-2392358",
 "350,000",
 "2025년 04월 01일"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"3"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"525941-2392358"
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
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- 종류: 종류
- 수량: 수량
- 수출입금액: 수출입금액
- 대가결제방법: 대가결제방법
- corp.name: 상호 (법인·사업자 상호, 같은 항목명 중 1번째 칸)
- corp.ceo: 대표자 (법인·사업자 대표자, 같은 항목명 중 1번째 칸)
- corp.address: 소재지 (법인·사업자 주소)
- 기타: 기타(또는변경내용)
- 신고번호: 신고번호
- 신고금액: 신고금액
- date: 신고일자
- 유효기간: 유효기간
- 처리기간: 처리기간
- date2: 작성일
- company.name2: 상호 (같은 항목명 중 2번째 칸)
- company.ceo2: 대표자 (같은 항목명 중 2번째 칸)
```

답:

```json
[{"key": "종류", "value": "하나 TDF 2040", "bbox_2d": [316, 200, 426, 212], "page": 1},
 {"key": "수량", "value": "3", "bbox_2d": [615, 237, 624, 249], "page": 1},
 {"key": "수출입금액", "value": "80,000", "bbox_2d": [875, 274, 925, 286], "page": 1},
 {"key": "대가결제방법", "value": null},
 {"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [317, 348, 426, 360], "page": 1},
 {"key": "corp.ceo", "value": "남궁예태", "bbox_2d": [315, 385, 381, 397], "page": 1},
 {"key": "corp.address", "value": "제주특별자치도 제주시 첨단로 381-19, 2층", "bbox_2d": [314, 422, 626, 434], "page": 1},
 {"key": "기타", "value": "해당 없음", "bbox_2d": [316, 459, 386, 471], "page": 1},
 {"key": "신고번호", "value": "525941-2392358", "bbox_2d": [712, 701, 836, 712], "page": 1},
 {"key": "신고금액", "value": "350,000", "bbox_2d": [866, 738, 925, 750], "page": 1},
 {"key": "date", "value": "2025년 04월 01일", "bbox_2d": [713, 775, 844, 787], "page": 1},
 {"key": "유효기간", "value": null},
 {"key": "처리기간", "value": null},
 {"key": "date2", "value": "2025년 4월 1일", "bbox_2d": [694, 528, 897, 547], "page": 1},
 {"key": "company.name2", "value": "(주)미래케미칼", "bbox_2d": [299, 589, 409, 600], "page": 1},
 {"key": "company.ceo2", "value": "남궁예태", "bbox_2d": [476, 608, 541, 619], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf307 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf307` → `python -m docgen.formdir card hf307` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | studio ① 서식 › 영역 편집에서 그리기 (`fields.json` items 에 한 칸) | 다시 |
| 답의 위치 (박스) | `fields.json` 그 칸의 `rect` [x0, y0, x1, y1] (pt) — 또는 영역 편집 | 다시 |
| 답의 키 | `fields.json` 그 칸에 `"key"` (없으면 규칙이 항목명으로 정함 — 모든 서식 공통 규칙은 studio 키 사전) | 다시 |
| 답의 값 | `fields.json` 그 칸에 `"source"` ([값 출처 목록](../_common/values.md)) 또는 값 종류 `"kind"` | 다시 |
| 칸의 항목명 | `fields.json` 그 칸의 `label` | 다시 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf307 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf307 --show` · `python -m docgen.preview hf307 --out work/hf307`
