# 혼인관계증명서 (`marriage_relation_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card marriage_relation_certificate · card-hash: 9c839abfdd5b -->

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

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `cert_type` | 증명서종류 | text | 1쪽 [613, 83, 703, 115] | 늘 | generate.py | look/template.html.j2:7 | 묻기 |
| `reg_base` | 등록기준지 | text | 1쪽 [233, 145, 453, 158] | 늘 | generate.py | look/template.html.j2:8 | 묻기 |
| `customer.relation` ← `self.relation` | 구분 | text | 1쪽 [108, 224, 142, 237] | 늘 | generate.py | - | 묻기 |
| `customer.name` ← `self.name` | 성명 | text | 1쪽 [202, 224, 271, 237] | 늘 | generate.py | - | 묻기 |
| `customer.name_hanja` ← `self.name_hanja` | 성명(한자) | text | 1쪽 [276, 224, 345, 237] | 늘 | generate.py | - | 묻기 |
| `customer.birth` ← `self.birth` | 출생연월일 | date | 1쪽 [407, 224, 536, 237] | 늘 | generate.py | - | 묻기 |
| `customer.rrn` ← `self.rrn` | 주민등록번호 | rrn | 1쪽 [608, 224, 725, 237] | 늘 | generate.py | - | 묻기 |
| `customer.gender` ← `self.gender` | 성별 | text | 1쪽 [796, 224, 813, 237] | 늘 | generate.py | - | 묻기 |
| `customer.bon` ← `self.bon` | 본 | text | 1쪽 [860, 224, 894, 237] | 늘 | generate.py | - | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [430, 318, 570, 332] | 늘 | generate.py | - | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [319, 352, 658, 373] | 늘 | generate.py | - | 묻기 |
| `issue_time` | 발급시각 | text | 1쪽 [194, 402, 261, 415] | 늘 | generate.py | - | 묻기 |
| `officer` | 발급담당자 | text | 1쪽 [194, 421, 242, 434] | 10/16 | generate.py | - | 묻기 |
| `officer_phone` | 전화 | phone | 1쪽 [194, 440, 284, 453] | 10/16 | generate.py | - | 묻기 |
| `applicant` | 신청인 | text | 1쪽 [194, 459, 257, 472] | 늘 | generate.py | - | 묻기 |
| `spouse.relation` | 구분 | - | - | 11/16 | generate.py | - | 묻기 |
| `family.name` ← `spouse.name` | 성명 | - | - | 11/16 | generate.py | - | 묻기 |
| `spouse.name_hanja` | 성명(한자) | - | - | 11/16 | generate.py | - | 묻기 |
| `spouse.birth` | 출생연월일 | - | - | 11/16 | generate.py | - | 묻기 |
| `spouse.rrn` | 주민등록번호 | - | - | 11/16 | generate.py | - | 묻기 |
| `spouse.gender` | 성별 | - | - | 11/16 | generate.py | - | 묻기 |
| `spouse.bon` | 본 | - | - | 11/16 | generate.py | - | 묻기 |
| `marriage.reported` | 신고일 | - | - | 11/16 | generate.py | look/template.html.j2:28 | 묻기 |
| `marriage.spouse_name` | 배우자 | - | - | 11/16 | generate.py | look/template.html.j2:28 | 묻기 |
| `marriage.spouse_rrn` | 배우자의주민등록번호 | - | - | 11/16 | generate.py | look/template.html.j2:28 | 묻기 |
| `marriage.office` | 처리관서 | - | - | 11/16 | generate.py | look/template.html.j2:28 | 묻기 |
| `doc_check_no` | 문서확인번호 | - | - | 6/16 | generate.py | - | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [646, 331, 736, 394] | 늘 | generate.py | - | 묻기 |

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

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

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

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions marriage_relation_certificate --show` · `python -m docgen.preview marriage_relation_certificate --out work/marriage_relation_certificate`
