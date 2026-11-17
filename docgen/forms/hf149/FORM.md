# 《기업》금융거래확인서 (`hf149`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf149 · card-hash: 6acdf107a543 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 《기업》금융거래확인서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf149 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.149 (대출) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 14칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `종류` | 종류 | text | 1쪽 [827, 212, 914, 227] | 늘 | 파일 key | 값 종류 `product` | fields.json:1367 | 묻기 |
| `선정일자` | 선정일자 | date | 1쪽 [828, 247, 913, 265] | 늘 | 파일 key | 값 종류 `date` | fields.json:1381 | 묻기 |
| `유효기간` | 유효기간 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1395 | 묻기 |
| `어음` | 어음 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1409 | 묻기 |
| `수표` | 수표 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1423 | 묻기 |
| `대출종별` | 대출종별 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:2193 | 묻기 |
| `연체발생일` | 연체발생일 | date | 1쪽 [205, 759, 292, 778] | 늘 | 파일 key | 값 종류 `date` | fields.json:2208 | 묻기 |
| `연체발생일2` | 연체발생일 | date | 1쪽 [333, 727, 377, 737] | 늘 | 파일 key | 값 종류 `date` | fields.json:2223 | 묻기 |
| `원금` | 원금 | number | 1쪽 [344, 760, 437, 779] | 늘 | 파일 key | 값 종류 `amount` | fields.json:2238 | 묻기 |
| `이자` | 이자 | amount | 1쪽 [462, 759, 558, 781] | 늘 | 파일 key | 값 종류 `amount` | fields.json:2253 | 묻기 |
| `연체정리일` | 연체정리일 | date | 1쪽 [564, 758, 658, 778] | 늘 | 파일 key | 값 종류 `date` | fields.json:2268 | 묻기 |
| `연체일수` | 연체일수 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:2283 | 묻기 |
| `signer2.name` | 대표자명 | text | 1쪽 [297, 882, 379, 905] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:2325 | 묻기 |
| `company.name` | 기업체명 | text | 1쪽 [253, 867, 393, 893] | 늘 | 파일 key | 고객 정보 (키 `company.name`, 없으면 값 종류 `company`) | fields.json:2344 | 묻기 |

## 표 `목록` (표 과제 table·table_read·table_find·table_qa) — 16열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `목록.*.종별` | 종별 | text | 1쪽 [81, 200, 165, 219] (1행) | 늘 | 파일 key | 값 종류 `product` | fields.json:23 | 묻기 |
| `목록.*.용도` | 용도 | text | 1쪽 [178, 206, 209, 215] (1행) | 늘 | 파일 key | 값 종류 `reason` | fields.json:191 | 묻기 |
| `목록.*.이율` | 이율 | number | 1쪽 [226, 200, 251, 220] (1행) | 늘 | 파일 key | 값 종류 `percent` | fields.json:359 | 묻기 |
| `목록.*.일자` | 일자 | date | 1쪽 [271, 204, 346, 219] (1행) | 늘 | 파일 key | 값 종류 `date` | fields.json:527 | 묻기 |
| `목록.*.금액` | 금액 | number | 1쪽 [384, 200, 447, 220] (1행) | 늘 | 파일 key | 값 종류 `amount` | fields.json:695 | 묻기 |
| `목록.*.잔액` | 잔액 | number | 1쪽 [471, 203, 539, 217] (1행) | 늘 | 파일 key | 값 종류 `amount` | fields.json:863 | 묻기 |
| `목록.*.대출기한` | 대출기한 | date | 1쪽 [553, 203, 629, 219] (1행) | 늘 | 파일 key | 값 종류 `date` | fields.json:1031 | 묻기 |
| `목록.*.비고` | 비고 | text | 1쪽 [645, 200, 718, 220] (1행) | 늘 | 파일 key | 값 종류 `note` | fields.json:1199 | 묻기 |
| `목록.*.소재지` | 소재지 | text | 1쪽 [83, 497, 180, 505] (1행) | 늘 | 파일 key | 값 종류 `address` | fields.json:1437 | 묻기 |
| `목록.*.소유자` | 소유자 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:1521 | 묻기 |
| `목록.*.채무자와의관계` | 채무자와의관계 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:1605 | 묻기 |
| `목록.*.종류` | 종류 | text | - (1행) | 늘 | 파일 key | 값 종류 `product` | fields.json:1689 | 묻기 |
| `목록.*.수량` | 수량 | number | 1쪽 [508, 492, 513, 511] (1행) | 늘 | 파일 key | 값 종류 `count` | fields.json:1773 | 묻기 |
| `목록.*.감정가격` | 감정가격 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:1857 | 묻기 |
| `목록.*.감정일자` | 감정일자 | date | 1쪽 [648, 492, 719, 507] (1행) | 늘 | 파일 key | 값 종류 `date` | fields.json:1941 | 묻기 |
| `목록.*.설정내용` | 설정내용(순위,금액) | text | 1쪽 [743, 490, 815, 509] (1행) | 늘 | 파일 key | 값 종류 `note` | fields.json:2025 | 묻기 |

## 체크·도장·서명 (marks) — 4칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.signer` | (부)점장 | seal | 1쪽 [874, 865, 920, 902] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:2312 | 묻기 |
| `sign.signer` | (부)점장 | signature | 1쪽 [884, 876, 910, 891] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:2312 | 묻기 |
| `seal.signer2` | 대표자명 | seal | 1쪽 [435, 875, 469, 913] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:2325 | 묻기 |
| `sign.signer2` | 대표자명 | signature | 1쪽 [439, 887, 465, 901] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:2325 | 묻기 |

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
"《기업》금융거래확인서"
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

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf149 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf149` → `python -m docgen.formdir card hf149` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf149 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf149 --show` · `python -m docgen.preview hf149 --out work/hf149`
