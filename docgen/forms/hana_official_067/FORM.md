# [필수] 개인(신용)정보 수집 · 이용 동의서[대출이동서비스] (`hana_official_067`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hana_official_067 · card-hash: 6592e23c926d -->

- **종류:** html 서식 (값은 fields.json 의 값 출처, 모양은 템플릿)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** [필수] 개인(신용)정보 수집 · 이용 동의서[대출이동서비스]
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hana_official_067 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 원문을 대조한 HTML. [필수] 개인(신용)정보 수집 · 이용 동의서[대출이동서비스]. 기존 hf067 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2023/05/31/5-16-0364_230531.pdf

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `form.json` | 이름·그룹·출처 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 6칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `신용거래정보` | ■신용거래정보 | text | - | 늘 | 템플릿 | - | - | 묻기 |
| `customer.rrn` | 주민등록번호 | rrn | 1쪽 [389, 592, 520, 612] | 늘 | 템플릿 | - | - | 묻기 |
| `date` | 작성일 | date | 1쪽 [349, 836, 559, 853] | 늘 | 템플릿 | - | - | 묻기 |
| `signer.name` | 본인성명 | text | 1쪽 [771, 834, 850, 853] | 늘 | 템플릿 | - | - | 묻기 |
| `ᄋ금융사고조사분쟁해결민원처리` | ᄋ금융사고조사,분쟁해결,민원처리 | text | - | 늘 | 템플릿 | - | - | 묻기 |
| `ᄋ법령상의무이행` | ᄋ법령상의무이행 | text | - | 늘 | 템플릿 | - | - | 묻기 |

## 체크·도장·서명 (marks) — 10칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox (동의하지 않음 / 동의함) | 1쪽 [723, 623, 835, 638] | 늘 | 템플릿 | - | - | 묻기 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox (동의하지 않음 / 동의함) | 1쪽 [846, 771, 911, 786] | 늘 | 템플릿 | - | - | 묻기 |
| `seal.signer` | 본인성명 | seal | 1쪽 [882, 824, 930, 864] | 늘 | 템플릿 | - | - | 묻기 |
| `sign.signer` | 본인성명 | signature | 1쪽 [886, 837, 926, 852] | 늘 | 템플릿 | - | - | 묻기 |
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [711, 26, 782, 70] | 늘 | 템플릿 | - | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [711, 26, 782, 70] | 늘 | 템플릿 | - | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [782, 26, 847, 70] | 늘 | 템플릿 | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [782, 26, 847, 70] | 늘 | 템플릿 | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [847, 26, 921, 70] | 늘 | 템플릿 | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [847, 26, 921, 70] | 늘 | 템플릿 | - | - | 묻기 |

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
"[필수] 개인(신용)정보 수집 · 이용 동의서[대출이동서비스]"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "850328-2489940",
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
"850328-2489940"
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
- 신용거래정보: ■신용거래정보
- customer.rrn: 주민등록번호
- date: 작성일
- signer.name: 본인성명
- ᄋ금융사고조사분쟁해결민원처리: ᄋ금융사고조사,분쟁해결,민원처리
- ᄋ법령상의무이행: ᄋ법령상의무이행
- 규모에비추어적합합니까: 규모에비추어적합합니까?
```

답:

```json
[{"key": "신용거래정보", "value": null},
 {"key": "customer.rrn", "value": "850328-2489940", "bbox_2d": [389, 592, 520, 612], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [349, 836, 559, 853], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [771, 834, 850, 853], "page": 1},
 {"key": "ᄋ금융사고조사분쟁해결민원처리", "value": null},
 {"key": "ᄋ법령상의무이행", "value": null},
 {"key": "규모에비추어적합합니까", "value": null}]
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
- check.위고유식별정보수집이용에동의하십니까: 위고유식별정보수집·이용에동의하십니까? (체크박스, 보기: 동의하지 않음 / 동의함)
- check.위개인정보수집이용에동의하십니까: 위개인(신용)정보수집·이용에동의하십니까? (체크박스, 보기: 동의하지 않음 / 동의함)
- seal.signer: 본인성명 (같은 설명 중 1번째 칸, 도장)
- sign.signer: 본인성명 (같은 설명 중 2번째 칸, 서명)
- seal.staff.본인확인: 본인확인 (같은 설명 중 1번째 칸, 도장)
- sign.staff.본인확인: 본인확인 (같은 설명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 설명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 설명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 설명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.위고유식별정보수집이용에동의하십니까", "value": "동의하지 않음", "bbox_2d": [723, 625, 739, 637], "page": 1},
 {"key": "check.위개인정보수집이용에동의하십니까", "value": "동의함", "bbox_2d": [846, 773, 862, 786], "page": 1},
 {"key": "seal.signer", "value": true, "bbox_2d": [882, 824, 930, 864], "page": 1},
 {"key": "sign.signer", "value": false},
 {"key": "seal.staff.본인확인", "value": false},
 {"key": "sign.staff.본인확인", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": false},
 {"key": "sign.staff.책임자", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hana_official_067 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hana_official_067` → `python -m docgen.formdir card hana_official_067` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `fields.json` 의 `fields` 에 키·source | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` + `fields.json` 의 그 키 | 다시 |
| 답의 값 | `fields.json` 의 그 칸 `source` ([값 출처 목록](../_common/values.md)) | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` 의 `adjust(d, p, rng)` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (파일로). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hana_official_067 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hana_official_067 --show` · `python -m docgen.preview hana_official_067 --out work/hana_official_067`
