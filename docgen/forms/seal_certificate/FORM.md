# 인감증명서 (`seal_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card seal_certificate · card-hash: b2de030bc418 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** identity · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 인감증명서
- **쓰이는 업무:** 주택담보대출, 상속예금 지급
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa seal_certificate --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 인감증명서 (인감증명법 시행령 별지 제14호서식 / 전자발급 제14호의2서식). 일반용 / 부동산 매도용.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/identity.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 13칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `doc_no` | 인감증명서발급사실확인용번호 / 문서확인번호 | text | 1쪽 [288, 65, 382, 76] | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:40 | 묻기 |
| `seal_name` | 인감 | text | 1쪽 [139, 281, 194, 289] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:90 | 묻기 |
| `customer.name` ← `person.name` | 성명 | text | 1쪽 [421, 162, 483, 174] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:60 | 묻기 |
| `customer.name_hanja` ← `person.name_hanja` | 한자 | text | 1쪽 [492, 162, 554, 174] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:65 | 묻기 |
| `customer.rrn` ← `person.rrn` | 주민등록번호 | rrn | 1쪽 [421, 215, 527, 227] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:75 | 묻기 |
| `customer.nationality` ← `person.nationality` | 국적 | text | 1쪽 [787, 215, 848, 227] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:70 | 묻기 |
| `customer.address` ← `person.address` | 주소 | text | 1쪽 [421, 255, 903, 283] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:55 | 묻기 |
| `counterparty.name` ← `buyer.name` | 성명(법인명) | text | 1쪽 [421, 334, 522, 346] | 4/16 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:30 | 묻기 |
| `buyer.rrn` | 주민등록번호(법인등록번호) | text | 1쪽 [787, 326, 896, 354] | 4/16 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:35 | 묻기 |
| `counterparty.address` ← `buyer.address` | 주소(법인소재지) | text | 1쪽 [421, 372, 677, 385] | 4/16 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:25 | 묻기 |
| `applicant_signature` | 발급신청자서명 | text | 1쪽 [421, 404, 554, 426] | 4/16 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:15 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [441, 509, 559, 522] | 늘 | 템플릿 | generate.py | look/template.html.j2:50 · fields.json:45 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [310, 540, 665, 558] | 늘 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:50 | 묻기 |

## 체크·도장·서명 (marks) — 4칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `applicant_type` | 발급구분 | checkbox (본인 / 대리인) | 1쪽 [836, 65, 865, 76] | 늘 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:20 | 묻기 |
| `seal.registered` | 등록인감 | seal | 1쪽 [100, 174, 233, 268] | 늘 | 템플릿 | generate.py | fields.json:85 | 묻기 |
| `usage_type` | 용도 | checkbox (일반용 / 부동산 매도용) | 1쪽 [507, 303, 604, 315] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:95 | 묻기 |
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [655, 519, 745, 582] | 늘 | 템플릿 | generate.py | fields.json:80 | 묻기 |

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
"인감증명서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "7762-9513-0409",
 "남궁예태인",
 "남궁예태",
 "南宮叡兌",
 "850328-2489940",
 "대한민국",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "장예태, 길동도",
 "830421-2925200, 830523-1356723",
 "경기도 수원시 영통구 광교중앙로 248",
 "2025년 4월 1일",
 "서울특별시 서초구 반포동장"
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
"서울특별시 서초구 반포동장"
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
- doc_no: 인감증명서발급사실확인용번호
- seal_name: 인감
- customer.name: 성명 (고객 성명)
- customer.name_hanja: 한자 (고객 한자 성명)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- customer.nationality: 국적 (고객 국적)
- customer.address: 주소 (고객 주소)
- counterparty.name: 성명(법인명) (상대방 성명)
- buyer.rrn: 주민등록번호(법인등록번호)
- counterparty.address: 주소(법인소재지) (상대방 주소)
- applicant_signature: 발급신청자서명
- issue_date: 발급일
- issuer: 발급기관
```

답:

```json
[{"key": "doc_no", "value": "7762-9513-0409", "bbox_2d": [288, 65, 382, 76], "page": 1},
 {"key": "seal_name", "value": "남궁예태인", "bbox_2d": [139, 281, 194, 289], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [421, 162, 483, 174], "page": 1},
 {"key": "customer.name_hanja", "value": "南宮叡兌", "bbox_2d": [492, 162, 554, 174], "page": 1},
 {"key": "customer.rrn", "value": "850328-2489940", "bbox_2d": [421, 215, 527, 227], "page": 1},
 {"key": "customer.nationality", "value": "대한민국", "bbox_2d": [787, 215, 848, 227], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [421, 255, 903, 283], "page": 1},
 {"key": "counterparty.name", "value": "장예태, 길동도", "bbox_2d": [421, 334, 522, 346], "page": 1},
 {"key": "buyer.rrn", "value": "830421-2925200, 830523-1356723", "bbox_2d": [787, 326, 896, 354], "page": 1},
 {"key": "counterparty.address", "value": "경기도 수원시 영통구 광교중앙로 248", "bbox_2d": [421, 372, 677, 385], "page": 1},
 {"key": "applicant_signature", "value": "남궁예태", "bbox_2d": [421, 404, 554, 426], "page": 1},
 {"key": "issue_date", "value": "2025년 4월 1일", "bbox_2d": [441, 509, 559, 522], "page": 1},
 {"key": "issuer", "value": "서울특별시 서초구 반포동장", "bbox_2d": [310, 540, 665, 558], "page": 1}]
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
- applicant_type: 발급구분 (체크박스, 보기: 본인 / 대리인)
- seal.registered: 등록인감 (도장)
- usage_type: 용도 (체크박스, 보기: 일반용 / 부동산 매도용)
- seal.issuer: 발급기관직인 (도장)
```

답:

```json
[{"key": "applicant_type", "value": "본인", "bbox_2d": [825, 65, 832, 76], "page": 1},
 {"key": "seal.registered", "value": true, "bbox_2d": [100, 174, 233, 268], "page": 1},
 {"key": "usage_type", "value": "부동산 매도용", "bbox_2d": [494, 303, 503, 315], "page": 1},
 {"key": "seal.issuer", "value": true, "bbox_2d": [655, 519, 745, 582], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa seal_certificate --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check seal_certificate` → `python -m docgen.formdir card seal_certificate` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `generate.py` 가 돌려주는 dict 에 그 키 값 | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` | 다시 |
| 답의 값 | `generate.py` (값 만드는 함수). 파이썬 대신 정하려면 `fields.json` 의 그 칸 `source` | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (studio html 편집). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa seal_certificate --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions seal_certificate --show` · `python -m docgen.preview seal_certificate --out work/seal_certificate`
