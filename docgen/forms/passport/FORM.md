# 여권 (`passport`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card passport · card-hash: 6b261191238d -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** identity · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 여권
- **쓰이는 업무:** 유학생 송금
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 대한민국 여권 사진정보면 (MRZ 포함).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/identity.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 15칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `type` | 종류/Type | text | 1쪽 [260, 133, 297, 169] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:7 | 묻기 |
| `country_code` | 발행국/Issuingcountry | text | 1쪽 [481, 133, 533, 169] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:10 | 묻기 |
| `passport_no` | 여권번호/PassportNo. | text | 1쪽 [703, 133, 847, 169] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:55 | 묻기 |
| `surname` | 성/Surname | text | 1쪽 [260, 197, 408, 233] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:70 | 묻기 |
| `given_names` | 이름/Givennames | text | 1쪽 [260, 261, 336, 297] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:30 | 묻기 |
| `name_korean` | 한글성명 | text | 1쪽 [260, 328, 356, 362] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:45 | 묻기 |
| `customer.nationality` ← `nationality` | 국적/Nationality | text | 1쪽 [703, 326, 923, 356] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:50 | 묻기 |
| `customer.birth` ← `birth` | 생년월일/Dateofbirth | date | 1쪽 [260, 390, 423, 426] | 늘 | 템플릿 | generate.py | fields.json:15 | 묻기 |
| `customer.gender` ← `gender` | 성별/Sex | text | 1쪽 [481, 390, 496, 426] | 늘 | 템플릿 | generate.py | fields.json:65 | 묻기 |
| `personal_no` | 주민등록번호/PersonalNo. | text | 1쪽 [703, 390, 788, 426] | 9/16 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:60 | 묻기 |
| `date_of_issue` | 발급일/Dateofissue | date | 1쪽 [260, 454, 420, 490] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:25 | 묻기 |
| `date_of_expiry` | 기간만료일/Dateofexpiry | date | 1쪽 [481, 454, 642, 490] | 늘 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:20 | 묻기 |
| `authority` | 발행관청/Authority | text | 1쪽 [260, 519, 598, 549] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:5 | 묻기 |
| `mrz.line1` | MRZ | text | 1쪽 [35, 848, 893, 900] | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:35 | 묻기 |
| `mrz.line2` | MRZ | text | 1쪽 [35, 909, 893, 961] | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:40 | 묻기 |

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
"여권"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "PM",
 "KOR",
 "M93568812",
 "NAMGOONG",
 "YETAE",
 "남궁예태",
 "REPUBLIC OF KOREA",
 "28 MAR 1985",
 "F",
 "2******",
 "12 MAY 2018",
 "12 MAY 2028",
 "MINISTRY OF FOREIGN AFFAIRS",
 "PMKORNAMGOONG<<YETAE<<<<<<<<<<<<<<<<<<<<<<<<",
 "M935688126KOR8503286F2805128<<<<<<<<<<<<<<<6"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2******"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"12 MAY 2028"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- type: 종류/Type
- country_code: 발행국/Issuingcountry
- passport_no: 여권번호/PassportNo.
- surname: 성/Surname
- given_names: 이름/Givennames
- name_korean: 한글성명
- customer.nationality: 국적/Nationality (고객 국적)
- customer.birth: 생년월일/Dateofbirth (고객 생년월일)
- customer.gender: 성별/Sex (고객 성별)
- personal_no: 주민등록번호/PersonalNo.
- date_of_issue: 발급일/Dateofissue
- date_of_expiry: 기간만료일/Dateofexpiry
- authority: 발행관청/Authority
- mrz.line1: MRZ (같은 항목명 중 1번째 칸)
- mrz.line2: MRZ (같은 항목명 중 2번째 칸)
```

답:

```json
[{"key": "type", "value": "PM", "bbox_2d": [260, 133, 297, 169], "page": 1},
 {"key": "country_code", "value": "KOR", "bbox_2d": [481, 133, 533, 169], "page": 1},
 {"key": "passport_no", "value": "M93568812", "bbox_2d": [703, 133, 847, 169], "page": 1},
 {"key": "surname", "value": "NAMGOONG", "bbox_2d": [260, 197, 408, 233], "page": 1},
 {"key": "given_names", "value": "YETAE", "bbox_2d": [260, 261, 336, 297], "page": 1},
 {"key": "name_korean", "value": "남궁예태", "bbox_2d": [260, 328, 356, 362], "page": 1},
 {"key": "customer.nationality", "value": "REPUBLIC OF KOREA", "bbox_2d": [703, 326, 923, 356], "page": 1},
 {"key": "customer.birth", "value": "28 MAR 1985", "bbox_2d": [260, 390, 423, 426], "page": 1},
 {"key": "customer.gender", "value": "F", "bbox_2d": [481, 390, 496, 426], "page": 1},
 {"key": "personal_no", "value": "2******", "bbox_2d": [703, 390, 788, 426], "page": 1},
 {"key": "date_of_issue", "value": "12 MAY 2018", "bbox_2d": [260, 454, 420, 490], "page": 1},
 {"key": "date_of_expiry", "value": "12 MAY 2028", "bbox_2d": [481, 454, 642, 490], "page": 1},
 {"key": "authority", "value": "MINISTRY OF FOREIGN AFFAIRS", "bbox_2d": [260, 519, 598, 549], "page": 1},
 {"key": "mrz.line1", "value": "PMKORNAMGOONG<<YETAE<<<<<<<<<<<<<<<<<<<<<<<<", "bbox_2d": [35, 848, 893, 900], "page": 1},
 {"key": "mrz.line2", "value": "M935688126KOR8503286F2805128<<<<<<<<<<<<<<<6", "bbox_2d": [35, 909, 893, 961], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check passport` → `python -m docgen.formdir card passport` (실제 질문→답 확인).

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
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions passport --show` · `python -m docgen.preview passport --out work/passport`
