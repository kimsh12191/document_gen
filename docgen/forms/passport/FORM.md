# 여권 (`passport`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card passport · card-hash: 2fac1f13c9bb -->

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

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `type` | 종류/Type | text | 1쪽 [260, 133, 297, 169] | 늘 | generate.py | look/template.html.j2:31 | 묻기 |
| `country_code` | 발행국/Issuingcountry | text | 1쪽 [481, 133, 533, 169] | 늘 | generate.py | look/template.html.j2:32 | 묻기 |
| `passport_no` | 여권번호/PassportNo. | text | 1쪽 [703, 133, 847, 169] | 늘 | generate.py | look/template.html.j2:33 | 묻기 |
| `surname` | 성/Surname | text | 1쪽 [260, 197, 408, 233] | 늘 | generate.py | look/template.html.j2:34 | 묻기 |
| `given_names` | 이름/Givennames | text | 1쪽 [260, 261, 336, 297] | 늘 | generate.py | look/template.html.j2:35 | 묻기 |
| `name_korean` | 한글성명 | text | 1쪽 [260, 328, 356, 362] | 늘 | generate.py | look/template.html.j2:36 | 묻기 |
| `customer.nationality` ← `nationality` | 국적/Nationality | text | 1쪽 [703, 326, 923, 356] | 늘 | generate.py | look/template.html.j2:37 | 묻기 |
| `customer.birth` ← `birth` | 생년월일/Dateofbirth | date | 1쪽 [260, 390, 423, 426] | 늘 | generate.py | - | 묻기 |
| `customer.gender` ← `gender` | 성별/Sex | text | 1쪽 [481, 390, 496, 426] | 늘 | generate.py | - | 묻기 |
| `personal_no` | 주민등록번호/PersonalNo. | text | 1쪽 [703, 390, 788, 426] | 9/16 | generate.py | look/template.html.j2:40 | 묻기 |
| `date_of_issue` | 발급일/Dateofissue | date | 1쪽 [260, 454, 420, 490] | 늘 | generate.py | look/template.html.j2:41 | 묻기 |
| `date_of_expiry` | 기간만료일/Dateofexpiry | date | 1쪽 [481, 454, 642, 490] | 늘 | generate.py | look/template.html.j2:42 | 묻기 |
| `authority` | 발행관청/Authority | text | 1쪽 [260, 519, 598, 549] | 늘 | generate.py | look/template.html.j2:43 | 묻기 |
| `mrz.line1` | MRZ | text | 1쪽 [35, 848, 893, 900] | 늘 | generate.py | look/template.html.j2:46 | 묻기 |
| `mrz.line2` | MRZ | text | 1쪽 [35, 909, 893, 961] | 늘 | generate.py | look/template.html.j2:47 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키 `a` ← `b`:** 질문·정답은 공통 키 a, 서식의 원래 키는 b (키 사전이 정함). **정한 곳:** 템플릿에서 그 칸 자리 (html·코드 서식) / 칸 목록의 그 칸 (원본 서식).

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

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `generate.py` 가 돌려주는 dict 에 그 키 값 | 미리보기로 확인 → 재검수 → 카드 다시 만들기 |
| 칸 키·항목명 바꾸기 | `look/template.html.j2` 의 `f("키", label=…)` (질문만 바꾸려면 `questions.json`) | `questions … --check` |
| 값이 이상함·칸끼리 안 맞음 | `generate.py` (값 만드는 함수) | 재검수 |
| 모양·표·문구 | `look/template.html.j2` (studio html 편집) | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions passport --show` · `python -m docgen.preview passport --out work/passport`
