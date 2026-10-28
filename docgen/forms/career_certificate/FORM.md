# 경력증명서 (`career_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card career_certificate · card-hash: d02a84f8fc16 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** income · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 경력증명서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa career_certificate --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 현 직장이 발급하는 경력증명서 (근로기준법 제39조 사용증명서, 통용 양식: 인적사항 / 경력사항

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/income.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 19칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `doc_no` | 문서번호 | text | 1쪽 [147, 60, 234, 70] | 늘 | 템플릿 | generate.py | look/template.html.j2:9 · fields.json:30 | 묻기 |
| `customer.name` ← `person.name` | 성명 | text | 1쪽 [234, 171, 299, 183] | 늘 | 템플릿 | generate.py | look/template.html.j2:12 · fields.json:50 | 묻기 |
| `customer.rrn` ← `person.rrn` | 주민등록번호 | rrn | 1쪽 [640, 171, 751, 183] | 늘 | 템플릿 | generate.py | look/template.html.j2:12 · fields.json:60 | 묻기 |
| `customer.address` ← `person.address` | 주소 | text | 1쪽 [234, 202, 793, 214] | 늘 | 템플릿 | generate.py | look/template.html.j2:13 · fields.json:45 | 묻기 |
| `customer.phone` ← `person.phone` | 연락처 | phone | 1쪽 [234, 233, 334, 246] | 늘 | 템플릿 | generate.py | look/template.html.j2:13 · fields.json:55 | 묻기 |
| `hire_date` | 입사일 | date | 1쪽 [640, 233, 713, 246] | 늘 | 템플릿 | generate.py | look/template.html.j2:13 · fields.json:35 | 묻기 |
| `careers.*.period` | 근무기간 | text | 1쪽 [146, 336, 303, 348] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:100 | 묻기 |
| `careers.*.department` | 근무부서 | text | 1쪽 [410, 336, 465, 348] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:90 | 묻기 |
| `careers.*.position` | 직위 | text | 1쪽 [543, 336, 574, 348] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:105 | 묻기 |
| `careers.*.duty` | 담당업무 | text | 1쪽 [622, 336, 793, 348] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:95 | 묻기 |
| `total_period` | 총근무기간 | text | 1쪽 [609, 458, 675, 470] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:80 | 묻기 |
| `purpose` | 용도 | text | 1쪽 [234, 496, 320, 508] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:65 | 묻기 |
| `submit_to` | 제출처 | text | 1쪽 [680, 496, 745, 508] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:75 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [434, 617, 566, 629] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:40 | 묻기 |
| `employer.name` ← `company.name` | 회사명 | text | 1쪽 [420, 653, 564, 666] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:20 | 묻기 |
| `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [420, 675, 519, 689] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:10 | 묻기 |
| `employer.address` ← `company.address` | 소재지 | text | 1쪽 [420, 698, 722, 711] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:5 | 묻기 |
| `employer.phone` ← `company.phone` | 전화번호 | phone | 1쪽 [420, 721, 519, 734] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:25 | 묻기 |
| `company.ceo` | 대표이사 | text | 1쪽 [500, 758, 571, 775] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:15 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.company` | 회사직인 | seal | 1쪽 [573, 736, 663, 799] | 늘 | 템플릿 | generate.py | fields.json:70 | 묻기 |

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
"경력증명서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "제 2025-850 호",
 "남궁예태",
 "850328-2******",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "010-6144-1173",
 "2021.03.06",
 "2021.03.06 ~ 2022.12.31",
 "영업1팀",
 "사원",
 "국내 영업 및 거래처 관리",
 "2023.01.01 ~ 2024.12.31",
 "생산관리팀",
 "주임",
 "생산계획 및 공정관리",
 "2025.01.01 ~ 현재",
 "고객지원팀",
 "대리",
 "고객 상담 및 CS 관리",
 "4년 0개월",
 "대출 신청용",
 "국민은행",
 "2025년 04월 01일",
 "주식회사 다온패션",
 "123-88-81212",
 "부산광역시 해운대구 해운대로 326, 7층",
 "051-509-1176",
 "박정연"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"국내 영업 및 거래처 관리"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"국민은행"
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
- doc_no: 문서번호
- customer.name: 성명 (고객 성명)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- customer.address: 주소 (고객 주소)
- customer.phone: 연락처 (고객 연락처)
- hire_date: 입사일
- careers.0.period: 근무기간 (1행)
- careers.0.department: 근무부서 (1행)
- careers.0.position: 직위 (1행)
- careers.0.duty: 담당업무 (1행)
- careers.1.period: 근무기간 (2행)
- careers.1.department: 근무부서 (2행)
- careers.1.position: 직위 (2행)
- careers.1.duty: 담당업무 (2행)
- careers.2.period: 근무기간 (3행)
- careers.2.department: 근무부서 (3행)
- careers.2.position: 직위 (3행)
- careers.2.duty: 담당업무 (3행)
- total_period: 총근무기간
- purpose: 용도
- submit_to: 제출처
- issue_date: 발급일
- employer.name: 회사명 (직장 이름)
- company.biz_no: 사업자등록번호 (직장의 사업자등록번호)
- employer.address: 소재지 (직장 주소)
- employer.phone: 전화번호 (직장 연락처)
- company.ceo: 대표이사 (직장의 대표자)
```

답:

```json
[{"key": "doc_no", "value": "제 2025-850 호", "bbox_2d": [147, 60, 234, 70], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [234, 171, 299, 183], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [640, 171, 751, 183], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [234, 202, 793, 214], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [234, 233, 334, 246], "page": 1},
 {"key": "hire_date", "value": "2021.03.06", "bbox_2d": [640, 233, 713, 246], "page": 1},
 {"key": "careers.0.period", "value": "2021.03.06 ~ 2022.12.31", "bbox_2d": [146, 336, 303, 348], "page": 1},
 {"key": "careers.0.department", "value": "영업1팀", "bbox_2d": [410, 336, 465, 348], "page": 1},
 {"key": "careers.0.position", "value": "사원", "bbox_2d": [543, 336, 574, 348], "page": 1},
 {"key": "careers.0.duty", "value": "국내 영업 및 거래처 관리", "bbox_2d": [622, 336, 793, 348], "page": 1},
 {"key": "careers.1.period", "value": "2023.01.01 ~ 2024.12.31", "bbox_2d": [146, 366, 303, 379], "page": 1},
 {"key": "careers.1.department", "value": "생산관리팀", "bbox_2d": [398, 366, 476, 379], "page": 1},
 {"key": "careers.1.position", "value": "주임", "bbox_2d": [543, 366, 574, 379], "page": 1},
 {"key": "careers.1.duty", "value": "생산계획 및 공정관리", "bbox_2d": [622, 366, 770, 379], "page": 1},
 {"key": "careers.2.period", "value": "2025.01.01 ~ 현재", "bbox_2d": [166, 397, 283, 409], "page": 1},
 {"key": "careers.2.department", "value": "고객지원팀", "bbox_2d": [398, 397, 476, 409], "page": 1},
 {"key": "careers.2.position", "value": "대리", "bbox_2d": [543, 397, 574, 409], "page": 1},
 {"key": "careers.2.duty", "value": "고객 상담 및 CS 관리", "bbox_2d": [622, 397, 766, 409], "page": 1},
 {"key": "total_period", "value": "4년 0개월", "bbox_2d": [609, 458, 675, 470], "page": 1},
 {"key": "purpose", "value": "대출 신청용", "bbox_2d": [234, 496, 320, 508], "page": 1},
 {"key": "submit_to", "value": "국민은행", "bbox_2d": [680, 496, 745, 508], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [434, 617, 566, 629], "page": 1},
 {"key": "employer.name", "value": "주식회사 다온패션", "bbox_2d": [420, 653, 564, 666], "page": 1},
 {"key": "company.biz_no", "value": "123-88-81212", "bbox_2d": [420, 675, 519, 689], "page": 1},
 {"key": "employer.address", "value": "부산광역시 해운대구 해운대로 326, 7층", "bbox_2d": [420, 698, 722, 711], "page": 1},
 {"key": "employer.phone", "value": "051-509-1176", "bbox_2d": [420, 721, 519, 734], "page": 1},
 {"key": "company.ceo", "value": "박정연", "bbox_2d": [500, 758, 571, 775], "page": 1}]
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
- seal.company: 회사직인 (직장의 신청인, 도장)
```

답:

```json
[{"key": "seal.company", "value": true, "bbox_2d": [573, 736, 663, 799], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa career_certificate --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check career_certificate` → `python -m docgen.formdir card career_certificate` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa career_certificate --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions career_certificate --show` · `python -m docgen.preview career_certificate --out work/career_certificate`
