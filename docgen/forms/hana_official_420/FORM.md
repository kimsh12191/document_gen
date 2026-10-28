# 비대면 계좌개설 안심차단 서비스 신청서 (`hana_official_420`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hana_official_420 · card-hash: 771da1eaf833 -->

- **종류:** html 서식 (값은 fields.json 의 값 출처, 모양은 템플릿)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 비대면 계좌개설 안심차단 서비스 신청서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 원문을 대조한 HTML. 비대면 계좌개설 안심차단 서비스 신청서. 기존 hf420 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070106/__icsFiles/afieldfile/2025/05/09/5-08-0737.pdf

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `form.json` | 이름·그룹·출처 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 8칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `customer.name` | 성명 | text | 1쪽 [322, 191, 404, 210] | 늘 | 템플릿 | - | - | 묻기 |
| `customer.rrn` | 주민등록번호 | rrn | 1쪽 [321, 224, 477, 246] | 늘 | 템플릿 | - | - | 묻기 |
| `agent.name` | 성명 | text | 1쪽 [322, 256, 406, 276] | 늘 | 템플릿 | - | - | 묻기 |
| `agent.birth` | 생년월일 | date | 1쪽 [324, 283, 416, 303] | 늘 | 템플릿 | - | - | 묻기 |
| `신청인과의관계` | 신청인과의관계 | text | - | 늘 | 템플릿 | - | - | 묻기 |
| `date` | 작성일 | date | 1쪽 [728, 821, 924, 839] | 늘 | 템플릿 | - | - | 묻기 |
| `signer.name` | 신청인 | text | 1쪽 [692, 867, 775, 886] | 늘 | 템플릿 | - | - | 묻기 |
| `signer2.name` | 대리인 | text | 1쪽 [693, 893, 774, 911] | 늘 | 템플릿 | - | - | 묻기 |

## 체크·도장·서명 (marks) — 14칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.구분` | 구분 | checkbox (신청) | 1쪽 [323, 167, 369, 181] | 늘 | 템플릿 | - | - | 묻기 |
| `check.대리인정보` | 대리인정보 | checkbox (임의대리인 신청시에도 신청내역에 대한 안내는 신청인(본인)에게 통지됩니다) | 1쪽 [186, 319, 686, 333] | 늘 | 템플릿 | - | - | 묻기 |
| `check.해제` | 해제 | checkbox (해제) | 1쪽 [696, 167, 743, 181] | 늘 | 템플릿 | - | - | 묻기 |
| `check.휴대전화번호` | 휴대전화번호 | checkbox (신청내역 통지 동의) | 1쪽 [673, 219, 811, 234] | 늘 | 템플릿 | - | - | 묻기 |
| `seal.customer` ← `seal.signer` | 신청인 | seal | 1쪽 [833, 870, 926, 885] | 늘 | 템플릿 | - | - | 묻기 |
| `sign.customer` ← `sign.signer` | 신청인 | signature | 1쪽 [833, 870, 926, 885] | 늘 | 템플릿 | - | - | 묻기 |
| `seal.agent` ← `seal.signer2` | 대리인 | seal | 1쪽 [854, 883, 905, 919] | 늘 | 템플릿 | - | - | 묻기 |
| `sign.agent` ← `sign.signer2` | 대리인 | signature | 1쪽 [833, 893, 926, 909] | 늘 | 템플릿 | - | - | 묻기 |
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [711, 35, 782, 77] | 늘 | 템플릿 | - | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [711, 35, 782, 77] | 늘 | 템플릿 | - | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [782, 35, 845, 77] | 늘 | 템플릿 | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [782, 35, 845, 77] | 늘 | 템플릿 | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [855, 38, 907, 74] | 늘 | 템플릿 | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [845, 35, 917, 77] | 늘 | 템플릿 | - | - | 묻기 |

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
"비대면 계좌개설 안심차단 서비스 신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "남궁예태",
 "850328-2******",
 "남궁찬윤",
 "1952.10.28"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"850328-2******"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"남궁찬윤"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- customer.name: 성명 (고객 성명, 같은 항목명 중 1번째 칸)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- agent.name: 성명 (대리인 성명, 같은 항목명 중 2번째 칸)
- agent.birth: 생년월일 (대리인 생년월일)
- 신청인과의관계: 신청인과의관계
- date: 작성일
- signer.name: 신청인 (고객 본인의 성명)
- signer2.name: 대리인 (대리인의 성명)
```

답:

```json
[{"key": "customer.name", "value": "남궁예태", "bbox_2d": [322, 191, 404, 210], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [321, 224, 477, 246], "page": 1},
 {"key": "agent.name", "value": "남궁찬윤", "bbox_2d": [322, 256, 406, 276], "page": 1},
 {"key": "agent.birth", "value": "1952.10.28", "bbox_2d": [324, 283, 416, 303], "page": 1},
 {"key": "신청인과의관계", "value": null},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [728, 821, 924, 839], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [692, 867, 775, 886], "page": 1},
 {"key": "signer2.name", "value": "남궁찬윤", "bbox_2d": [693, 893, 774, 911], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- check.구분: 구분 (체크박스, 보기: 신청)
- check.대리인정보: 대리인정보 (체크박스, 보기: 임의대리인 신청시에도 신청내역에 대한 안내는 신청인(본인)에게 통지됩니다)
- check.해제: 해제 (체크박스, 보기: 해제)
- check.휴대전화번호: 휴대전화번호 (체크박스, 보기: 신청내역 통지 동의)
- seal.customer: 신청인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 신청인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.agent: 대리인 (대리인 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.agent: 대리인 (대리인 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.본인확인: 본인확인 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.본인확인: 본인확인 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.구분", "value": null},
 {"key": "check.대리인정보", "value": null},
 {"key": "check.해제", "value": "해제", "bbox_2d": [696, 167, 711, 181], "page": 1},
 {"key": "check.휴대전화번호", "value": null},
 {"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": false},
 {"key": "seal.agent", "value": true, "bbox_2d": [854, 883, 905, 919], "page": 1},
 {"key": "sign.agent", "value": false},
 {"key": "seal.staff.본인확인", "value": false},
 {"key": "sign.staff.본인확인", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": true, "bbox_2d": [782, 35, 845, 77], "page": 1},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [855, 38, 907, 74], "page": 1},
 {"key": "sign.staff.책임자", "value": false}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hana_official_420` → `python -m docgen.formdir card hana_official_420` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `fields.json` 의 `fields` 에 키·source | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` + `fields.json` 의 그 키 | 다시 |
| 답의 값 | `fields.json` 의 그 칸 `source` ([값 출처 목록](../_common/values.md)) | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` 의 `adjust(d, p, rng)` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (studio html 편집). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hana_official_420 --show` · `python -m docgen.preview hana_official_420 --out work/hana_official_420`
