# 혼인관계증명서 (`marriage_relation_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card marriage_relation_certificate · card-hash: e04ec575cb20 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** family · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 혼인관계증명서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 혼인관계증명서 (일반/상세). 일반은 현재 혼인만, 상세는 이혼한 혼인(외국인 배우자 포함)까지 표시.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/family.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 27칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `cert_type` | 증명서종류 | text | 1쪽 [613, 83, 703, 115] | 늘 | 템플릿 | generate.py | look/template.html.j2:7 · fields.json:10 | 묻기 |
| `reg_base` | 등록기준지 | text | 1쪽 [233, 145, 453, 158] | 늘 | 템플릿 | generate.py | look/template.html.j2:8 · fields.json:65 | 묻기 |
| `customer.relation` ← `self.relation` | 구분 | text | 1쪽 [108, 224, 142, 237] | 늘 | 템플릿 | generate.py | fields.json:100 | 묻기 |
| `customer.name` ← `self.name` | 성명 | text | 1쪽 [202, 224, 271, 237] | 늘 | 템플릿 | generate.py | fields.json:90 | 묻기 |
| `customer.name_hanja` ← `self.name_hanja` | 성명(한자) | text | 1쪽 [276, 224, 345, 237] | 늘 | 템플릿 | generate.py | fields.json:95 | 묻기 |
| `customer.birth` ← `self.birth` | 출생연월일 | date | 1쪽 [407, 224, 536, 237] | 늘 | 템플릿 | generate.py | fields.json:75 | 묻기 |
| `customer.rrn` ← `self.rrn` | 주민등록번호 | rrn | 1쪽 [608, 224, 725, 237] | 늘 | 템플릿 | generate.py | fields.json:105 | 묻기 |
| `customer.gender` ← `self.gender` | 성별 | text | 1쪽 [796, 224, 813, 237] | 늘 | 템플릿 | generate.py | fields.json:85 | 묻기 |
| `customer.bon` ← `self.bon` | 본 | text | 1쪽 [860, 224, 894, 237] | 늘 | 템플릿 | generate.py | fields.json:80 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [430, 318, 570, 332] | 늘 | 템플릿 | generate.py | fields.json:20 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [319, 352, 658, 373] | 늘 | 템플릿 | generate.py | fields.json:30 | 묻기 |
| `issue_time` | 발급시각 | text | 1쪽 [194, 402, 261, 415] | 늘 | 템플릿 | generate.py | fields.json:25 | 묻기 |
| `officer` | 발급담당자 | text | 1쪽 [194, 421, 242, 434] | 10/16 | 템플릿 | generate.py | fields.json:55 | 묻기 |
| `officer_phone` | 전화 | phone | 1쪽 [194, 440, 284, 453] | 10/16 | 템플릿 | generate.py | fields.json:60 | 묻기 |
| `applicant` | 신청인 | text | 1쪽 [194, 459, 257, 472] | 늘 | 템플릿 | generate.py | fields.json:5 | 묻기 |
| `spouse.relation` | 구분 | - | - | 11/16 | 템플릿 | generate.py | fields.json:135 | 묻기 |
| `family.name` ← `spouse.name` | 성명 | - | - | 11/16 | 템플릿 | generate.py | fields.json:125 | 묻기 |
| `spouse.name_hanja` | 성명(한자) | - | - | 11/16 | 템플릿 | generate.py | fields.json:130 | 묻기 |
| `spouse.birth` | 출생연월일 | - | - | 11/16 | 템플릿 | generate.py | fields.json:110 | 묻기 |
| `spouse.rrn` | 주민등록번호 | - | - | 11/16 | 템플릿 | generate.py | fields.json:140 | 묻기 |
| `spouse.gender` | 성별 | - | - | 11/16 | 템플릿 | generate.py | fields.json:120 | 묻기 |
| `spouse.bon` | 본 | - | - | 11/16 | 템플릿 | generate.py | fields.json:115 | 묻기 |
| `marriage.reported` | 신고일 | - | - | 11/16 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:40 | 묻기 |
| `marriage.spouse_name` | 배우자 | - | - | 11/16 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:45 | 묻기 |
| `marriage.spouse_rrn` | 배우자의주민등록번호 | - | - | 11/16 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:50 | 묻기 |
| `marriage.office` | 처리관서 | - | - | 11/16 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:35 | 묻기 |
| `doc_check_no` | 문서확인번호 | - | - | 6/16 | 템플릿 | generate.py | fields.json:15 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [646, 331, 736, 394] | 늘 | 템플릿 | generate.py | fields.json:70 | 묻기 |

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
"혼인관계증명서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "일반",
 "세종특별자치시 도담동 550-8",
 "본인",
 "남궁예태",
 "南宮叡兌",
 "1985년 03월 28일",
 "850328-2489940",
 "여",
 "咸悅",
 "2025년 04월 01일",
 "서울특별시 서초구청장",
 "15시 16분",
 "류형아",
 "02-9834-9083"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"여"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"서울특별시 서초구청장"
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
- cert_type: 증명서종류
- reg_base: 등록기준지
- customer.relation: 구분 (고객 관계)
- customer.name: 성명 (고객 성명)
- customer.name_hanja: 성명(한자) (고객 한자 성명)
- customer.birth: 출생연월일 (고객 생년월일)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- customer.gender: 성별 (고객 성별)
- customer.bon: 본 (고객 본관)
- issue_date: 발급일
- issuer: 발급기관
- issue_time: 발급시각
- officer: 발급담당자
- officer_phone: 전화
- applicant: 신청인
```

답:

```json
[{"key": "cert_type", "value": "일반", "bbox_2d": [613, 83, 703, 115], "page": 1},
 {"key": "reg_base", "value": "세종특별자치시 도담동 550-8", "bbox_2d": [233, 145, 453, 158], "page": 1},
 {"key": "customer.relation", "value": "본인", "bbox_2d": [108, 224, 142, 237], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [202, 224, 271, 237], "page": 1},
 {"key": "customer.name_hanja", "value": "南宮叡兌", "bbox_2d": [276, 224, 345, 237], "page": 1},
 {"key": "customer.birth", "value": "1985년 03월 28일", "bbox_2d": [407, 224, 536, 237], "page": 1},
 {"key": "customer.rrn", "value": "850328-2489940", "bbox_2d": [608, 224, 725, 237], "page": 1},
 {"key": "customer.gender", "value": "여", "bbox_2d": [796, 224, 813, 237], "page": 1},
 {"key": "customer.bon", "value": "咸悅", "bbox_2d": [860, 224, 894, 237], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [430, 318, 570, 332], "page": 1},
 {"key": "issuer", "value": "서울특별시 서초구청장", "bbox_2d": [319, 352, 658, 373], "page": 1},
 {"key": "issue_time", "value": "15시 16분", "bbox_2d": [194, 402, 261, 415], "page": 1},
 {"key": "officer", "value": "류형아", "bbox_2d": [194, 421, 242, 434], "page": 1},
 {"key": "officer_phone", "value": "02-9834-9083", "bbox_2d": [194, 440, 284, 453], "page": 1},
 {"key": "applicant", "value": "남궁예태", "bbox_2d": [194, 459, 257, 472], "page": 1}]
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
- seal.issuer: 발급기관직인 (도장)
```

답:

```json
[{"key": "seal.issuer", "value": true, "bbox_2d": [646, 331, 736, 394], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check marriage_relation_certificate` → `python -m docgen.formdir card marriage_relation_certificate` (실제 질문→답 확인).

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
| 답 모양 | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions marriage_relation_certificate --show` · `python -m docgen.preview marriage_relation_certificate --out work/marriage_relation_certificate`
