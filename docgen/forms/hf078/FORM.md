# 통화전환 옵션부 외화대출 원화대출 전환신청서 (`hf078`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf078 · card-hash: 011219177d9b -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 통화전환 옵션부 외화대출 원화대출 전환신청서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf078 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.78 (대출) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 14칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `원화대출전환희망일` | 원화대출전환희망일 | date | 1쪽 [362, 629, 473, 654] | 늘 | 항목명 그대로 | 값 종류 `date` (항목명 자동) | fields.json:17 | 묻기 |
| `신청사유` | 신청사유 | text | 1쪽 [366, 657, 462, 681] | 늘 | 항목명 그대로 | 값 종류 `reason` (항목명 자동) | fields.json:28 | 묻기 |
| `대출과목` | 대출과목 | text | 1쪽 [362, 683, 482, 708] | 늘 | 항목명 그대로 | 값 종류 `loan_subject` (항목명 자동) | fields.json:39 | 묻기 |
| `대출금액` | 대출금액(본건전환후외화대출잔액) | number | 1쪽 [557, 728, 639, 753] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:50 | 묻기 |
| `date` | 대출취급일 | date | 1쪽 [374, 776, 584, 796] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:61 | 묻기 |
| `date2` | 대출만기일 | date | 1쪽 [374, 804, 584, 824] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:86 | 묻기 |
| `대출금리` | 대출금리 | number | 1쪽 [489, 830, 512, 854] | 늘 | 항목명 그대로 | 값 종류 `percent` (항목명 자동) | fields.json:111 | 묻기 |
| `date3` | 일자 | date | 1쪽 [659, 630, 869, 650] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:122 | 묻기 |
| `date4` | 년월일 | date | 1쪽 [651, 656, 828, 681] | 늘 | 표 행 (묶음·항목명 '년 월 일') | 값 종류 `date` (항목명 자동) | fields.json:147 | 묻기 |
| `주1` | 주1 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:159 | 묻기 |
| `date5` | 년월일 | date | 1쪽 [649, 774, 827, 802] | 늘 | 규칙: '년 월 일' → `date` | 고객 정보 (키 `date`) | fields.json:170 | 묻기 |
| `주3` | 주3 | text | - | 늘 | 표 행 (묶음·항목명 '주3') | 값 종류 `text` (항목명 자동) | fields.json:181 | 묻기 |
| `date6` | 작성일 | date | 1쪽 [666, 256, 864, 275] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:193 | 묻기 |
| `customer.name` ← `signer.name` | 채무자본인 | text | 1쪽 [663, 325, 753, 350] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:218 | 묻기 |

## 체크·도장·서명 (marks) — 2칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.customer` ← `seal.signer` | 채무자본인 | seal | 1쪽 [845, 328, 877, 345] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:218 | 묻기 |
| `sign.customer` ← `sign.signer` | 채무자본인 | signature | 1쪽 [845, 328, 877, 345] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:218 | 묻기 |

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
"통화전환 옵션부 외화대출 원화대출 전환신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2024.12.14",
 "만기 해지",
 "일반자금대출",
 "750,000",
 "60",
 "2025년 04월 01일",
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
"만기 해지"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"일반자금대출"
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
- 원화대출전환희망일: 원화대출전환희망일
- 신청사유: 신청사유
- 대출과목: 대출과목
- 대출금액: 대출금액(본건전환후외화대출잔액)
- date: 대출취급일
- date2: 대출만기일
- 대출금리: 대출금리
- date3: 일자
- date4: 년월일 (같은 항목명 중 1번째 칸)
- 주1: 주1
- date5: 년월일 (같은 항목명 중 2번째 칸)
- 주3: 주3
- date6: 작성일
- customer.name: 채무자본인 (고객 성명)
- NET12: NET12
```

답:

```json
[{"key": "원화대출전환희망일", "value": "2024.12.14", "bbox_2d": [362, 629, 473, 654], "page": 1},
 {"key": "신청사유", "value": "만기 해지", "bbox_2d": [366, 657, 462, 681], "page": 1},
 {"key": "대출과목", "value": "일반자금대출", "bbox_2d": [362, 683, 482, 708], "page": 1},
 {"key": "대출금액", "value": "750,000", "bbox_2d": [557, 728, 639, 753], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [374, 776, 584, 796], "page": 1},
 {"key": "date2", "value": "2025년 4월 1일", "bbox_2d": [374, 804, 584, 824], "page": 1},
 {"key": "대출금리", "value": "60", "bbox_2d": [489, 830, 512, 854], "page": 1},
 {"key": "date3", "value": "2025년 4월 1일", "bbox_2d": [659, 630, 869, 650], "page": 1},
 {"key": "date4", "value": "2025년 04월 01일", "bbox_2d": [651, 656, 828, 681], "page": 1},
 {"key": "주1", "value": null},
 {"key": "date5", "value": "2025년 04월 01일", "bbox_2d": [649, 774, 827, 802], "page": 1},
 {"key": "주3", "value": null},
 {"key": "date6", "value": "2025년 4월 1일", "bbox_2d": [666, 256, 864, 275], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [663, 325, 753, 350], "page": 1},
 {"key": "NET12", "value": null}]
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
- seal.customer: 채무자본인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 채무자본인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [845, 328, 877, 345], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf078 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf078` → `python -m docgen.formdir card hf078` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf078 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf078 --show` · `python -m docgen.preview hf078 --out work/hf078`
