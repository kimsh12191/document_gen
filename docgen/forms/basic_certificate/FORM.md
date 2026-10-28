# 기본증명서 (`basic_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card basic_certificate · card-hash: 160ec6874a22 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** family · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 기본증명서
- **쓰이는 업무:** 상속예금 지급
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 기본증명서 (일반/상세). 상세에는 개명·국적취득·성별정정 기록이 나온다.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/family.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 19칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `cert_type` | 증명서종류 | text | 1쪽 [568, 89, 658, 121] | 늘 | 템플릿 | generate.py | look/template.html.j2:6 · fields.json:25 | 묻기 |
| `reg_base` | 등록기준지 | text | 1쪽 [237, 151, 452, 164] | 늘 | 템플릿 | generate.py | look/template.html.j2:7 · fields.json:80 | 묻기 |
| `customer.relation` ← `self.relation` | 구분 | text | 1쪽 [115, 223, 148, 236] | 늘 | 템플릿 | generate.py | fields.json:115 | 묻기 |
| `customer.name` ← `self.name` | 성명 | text | 1쪽 [210, 223, 277, 236] | 늘 | 템플릿 | generate.py | fields.json:105 | 묻기 |
| `customer.name_hanja` ← `self.name_hanja` | 성명(한자) | text | 1쪽 [283, 223, 350, 236] | 늘 | 템플릿 | generate.py | fields.json:110 | 묻기 |
| `customer.birth` ← `self.birth` | 출생연월일 | date | 1쪽 [415, 223, 541, 236] | 늘 | 템플릿 | generate.py | fields.json:90 | 묻기 |
| `customer.rrn` ← `self.rrn` | 주민등록번호 | rrn | 1쪽 [609, 223, 723, 236] | 늘 | 템플릿 | generate.py | fields.json:120 | 묻기 |
| `customer.gender` ← `self.gender` | 성별 | text | 1쪽 [789, 223, 806, 236] | 늘 | 템플릿 | generate.py | fields.json:100 | 묻기 |
| `customer.bon` ← `self.bon` | 본 | text | 1쪽 [854, 223, 888, 236] | 늘 | 템플릿 | generate.py | fields.json:95 | 묻기 |
| `birth.place` | 출생장소 | text | 1쪽 [312, 314, 526, 328] | 늘 | 템플릿 | generate.py | look/template.html.j2:14 · fields.json:10 | 묻기 |
| `birth.reported` | 신고일 | date | 1쪽 [295, 331, 421, 345] | 늘 | 템플릿 | generate.py | look/template.html.j2:14 · fields.json:15 | 묻기 |
| `birth.reporter` | 신고인 | text | 1쪽 [295, 348, 312, 362] | 늘 | 템플릿 | generate.py | look/template.html.j2:14 · fields.json:20 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [432, 442, 568, 456] | 늘 | 템플릿 | generate.py | fields.json:35 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [240, 475, 738, 492] | 늘 | 템플릿 | generate.py | fields.json:45 | 묻기 |
| `issue_time` | 발급시각 | text | 1쪽 [200, 522, 266, 534] | 늘 | 템플릿 | generate.py | fields.json:40 | 묻기 |
| `applicant` | 신청인 | text | 1쪽 [200, 540, 262, 553] | 늘 | 템플릿 | generate.py | fields.json:5 | 묻기 |
| `doc_check_no` | 문서확인번호 | text | 1쪽 [179, 938, 301, 949] | 8/16 | 템플릿 | generate.py | fields.json:30 | 묻기 |
| `officer` | 발급담당자 | - | - | 8/16 | 템플릿 | generate.py | fields.json:70 | 묻기 |
| `officer_phone` | 전화 | - | - | 8/16 | 템플릿 | generate.py | fields.json:75 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [725, 454, 815, 518] | 늘 | 템플릿 | generate.py | fields.json:85 | 묻기 |

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
"기본증명서"
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
 "850328-2******",
 "여",
 "咸悅",
 "경기도 성남시 분당구 서현동",
 "1985년 04월 16일",
 "부",
 "2025년 04월 01일",
 "법원행정처 전산정보중앙관리소 전산운영책임관",
 "22시 29분",
 "1916-5111-8142-6517"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"세종특별자치시 도담동 550-8"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"南宮叡兌"
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
- birth.place: 출생장소
- birth.reported: 신고일
- birth.reporter: 신고인
- issue_date: 발급일
- issuer: 발급기관
- issue_time: 발급시각
- applicant: 신청인
- doc_check_no: 문서확인번호
```

답:

```json
[{"key": "cert_type", "value": "일반", "bbox_2d": [568, 89, 658, 121], "page": 1},
 {"key": "reg_base", "value": "세종특별자치시 도담동 550-8", "bbox_2d": [237, 151, 452, 164], "page": 1},
 {"key": "customer.relation", "value": "본인", "bbox_2d": [115, 223, 148, 236], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [210, 223, 277, 236], "page": 1},
 {"key": "customer.name_hanja", "value": "南宮叡兌", "bbox_2d": [283, 223, 350, 236], "page": 1},
 {"key": "customer.birth", "value": "1985년 03월 28일", "bbox_2d": [415, 223, 541, 236], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [609, 223, 723, 236], "page": 1},
 {"key": "customer.gender", "value": "여", "bbox_2d": [789, 223, 806, 236], "page": 1},
 {"key": "customer.bon", "value": "咸悅", "bbox_2d": [854, 223, 888, 236], "page": 1},
 {"key": "birth.place", "value": "경기도 성남시 분당구 서현동", "bbox_2d": [312, 314, 526, 328], "page": 1},
 {"key": "birth.reported", "value": "1985년 04월 16일", "bbox_2d": [295, 331, 421, 345], "page": 1},
 {"key": "birth.reporter", "value": "부", "bbox_2d": [295, 348, 312, 362], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [432, 442, 568, 456], "page": 1},
 {"key": "issuer", "value": "법원행정처 전산정보중앙관리소 전산운영책임관", "bbox_2d": [240, 475, 738, 492], "page": 1},
 {"key": "issue_time", "value": "22시 29분", "bbox_2d": [200, 522, 266, 534], "page": 1},
 {"key": "applicant", "value": "남궁예태", "bbox_2d": [200, 540, 262, 553], "page": 1},
 {"key": "doc_check_no", "value": "1916-5111-8142-6517", "bbox_2d": [179, 938, 301, 949], "page": 1}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [725, 454, 815, 518], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check basic_certificate` → `python -m docgen.formdir card basic_certificate` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions basic_certificate --show` · `python -m docgen.preview basic_certificate --out work/basic_certificate`
