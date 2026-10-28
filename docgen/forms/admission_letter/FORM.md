# 입학허가서(Letter of Admission) (`admission_letter`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card admission_letter · card-hash: 3a95c6fe76bc -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** fx · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 입학허가서(Letter of Admission)
- **쓰이는 업무:** 유학생 송금
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa admission_letter --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 해외 대학 입학허가서 (유학생 송금 증빙). 조건부 입학·장학금·입학 연기는 프로필 단위(_study).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/fx.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 29칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `foreign.name` ← `university.name` | University | text | 1쪽 [181, 54, 511, 78] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:135 | 묻기 |
| `foreign.office` ← `university.office` | Office | text | 1쪽 [181, 85, 296, 96] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:140 | 묻기 |
| `foreign.address` ← `university.address` | UniversityAddress | text | 1쪽 [307, 85, 540, 96] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:125 | 묻기 |
| `university.email` | Email | text | 1쪽 [181, 99, 339, 110] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:130 | 묻기 |
| `letter_date` | Date | date | 1쪽 [798, 145, 912, 158] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:60 | 묻기 |
| `family.name` ← `student.name` | StudentName | text | 1쪽 [88, 178, 203, 192] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:110 | 묻기 |
| `student.address` | StudentAddress | text | 1쪽 [88, 198, 462, 209] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:95 | 묻기 |
| `term` | TermofEntry | text | 1쪽 [607, 308, 672, 322] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:120 | 묻기 |
| `student.birth` | DateofBirth | date | 1쪽 [395, 385, 501, 398] | 늘 | 템플릿 | generate.py | fields.json:100 | 묻기 |
| `student.nationality` | Citizenship | text | 1쪽 [395, 413, 518, 426] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:115 | 묻기 |
| `family.id` ← `student.id` | StudentID | text | 1쪽 [395, 440, 476, 453] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:105 | 묻기 |
| `program` | Program | text | 1쪽 [395, 467, 558, 481] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:65 | 묻기 |
| `degree` | Degree | text | 1쪽 [395, 495, 679, 508] | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:45 | 묻기 |
| `start_date` | ClassesBegin | date | 1쪽 [395, 522, 505, 536] | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:90 | 묻기 |
| `duration` | Duration | text | 1쪽 [395, 550, 516, 563] | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:55 | 묻기 |
| `scholarship.name` | Scholarship | text | 1쪽 [619, 585, 793, 598] | 6/16 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:75 | 묻기 |
| `scholarship.amount` | ScholarshipAmount | text | 1쪽 [88, 603, 255, 616] | 6/16 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:70 | 묻기 |
| `deposit_deadline` | DepositDeadline | date | 1쪽 [156, 663, 268, 676] | 늘 | 템플릿 | generate.py | look/template.html.j2:71 · fields.json:50 | 묻기 |
| `signer` | Signedby | text | 1쪽 [88, 859, 211, 873] | 늘 | 템플릿 | generate.py | look/template.html.j2:90 · fields.json:80 | 묻기 |
| `signer_title` | Title | text | 1쪽 [88, 877, 243, 890] | 늘 | 템플릿 | generate.py | look/template.html.j2:92 · fields.json:85 | 묻기 |
| `admission_type` | AdmissionType | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:5 | 묻기 |
| `condition_deadline` | ConditionDeadline | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:10 | 묻기 |
| `conditions.*` | Condition | - | - (1행) | 5/16 | 템플릿 | generate.py | - | 묻기 |
| `cost.tuition` | EstimatedTuition | - | - | 7/16 | 템플릿 | generate.py | look/template.html.j2:63 · fields.json:35 | 묻기 |
| `cost.living` | EstimatedLivingExpenses | - | - | 7/16 | 템플릿 | generate.py | look/template.html.j2:64 · fields.json:25 | 묻기 |
| `cost.insurance` | EstimatedHealthInsurance | - | - | 7/16 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:20 | 묻기 |
| `cost.books` | EstimatedBooksandSupplies | - | - | 7/16 | 템플릿 | generate.py | look/template.html.j2:66 · fields.json:15 | 묻기 |
| `cost.total` | TotalEstimatedCost | - | - | 7/16 | 템플릿 | generate.py | look/template.html.j2:67 · fields.json:30 | 묻기 |
| `deferred_from` | DeferredFrom | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:40 | 묻기 |

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
"입학허가서(Letter of Admission)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "Northbridge University",
 "Office of Admissions",
 "300 College Ave, Boston, MA 02115, USA",
 "admissions@northbridge.edu",
 "January 30, 2025",
 "Yetae Namgoong",
 "Apt. 103-1301, 357 Gangnam-daero, Seocho-gu, Seoul 06295, Korea",
 "Fall 2025",
 "March 28, 1985",
 "Republic of Korea",
 "M67186886",
 "Business Administration",
 "Master of Business Administration (MBA)",
 "August 23, 2025",
 "2 years (full-time)",
 "Presidential Scholarship",
 "$4,060.00 per semester",
 "March 13, 2025",
 "David L. Morgan",
 "Director of Admissions"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"Yetae Namgoong"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"August 23, 2025"
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
- foreign.name: University (외국 상대 이름)
- foreign.office: Office (외국 상대 사무소)
- foreign.address: UniversityAddress (외국 상대 주소)
- university.email: Email
- letter_date: Date
- family.name: StudentName (가족 성명)
- student.address: StudentAddress
- term: TermofEntry
- student.birth: DateofBirth
- student.nationality: Citizenship
- family.id: StudentID (가족 번호)
- program: Program
- degree: Degree
- start_date: ClassesBegin
- duration: Duration
- scholarship.name: Scholarship
- scholarship.amount: ScholarshipAmount
- deposit_deadline: DepositDeadline
- signer: Signedby
- signer_title: Title
```

답:

```json
[{"key": "foreign.name", "value": "Northbridge University", "bbox_2d": [181, 54, 511, 78], "page": 1},
 {"key": "foreign.office", "value": "Office of Admissions", "bbox_2d": [181, 85, 296, 96], "page": 1},
 {"key": "foreign.address", "value": "300 College Ave, Boston, MA 02115, USA", "bbox_2d": [307, 85, 540, 96], "page": 1},
 {"key": "university.email", "value": "admissions@northbridge.edu", "bbox_2d": [181, 99, 339, 110], "page": 1},
 {"key": "letter_date", "value": "January 30, 2025", "bbox_2d": [798, 145, 912, 158], "page": 1},
 {"key": "family.name", "value": "Yetae Namgoong", "bbox_2d": [88, 178, 203, 192], "page": 1},
 {"key": "student.address", "value": "Apt. 103-1301, 357 Gangnam-daero, Seocho-gu, Seoul 06295, Korea", "bbox_2d": [88, 198, 462, 209], "page": 1},
 {"key": "term", "value": "Fall 2025", "bbox_2d": [607, 308, 672, 322], "page": 1},
 {"key": "student.birth", "value": "March 28, 1985", "bbox_2d": [395, 385, 501, 398], "page": 1},
 {"key": "student.nationality", "value": "Republic of Korea", "bbox_2d": [395, 413, 518, 426], "page": 1},
 {"key": "family.id", "value": "M67186886", "bbox_2d": [395, 440, 476, 453], "page": 1},
 {"key": "program", "value": "Business Administration", "bbox_2d": [395, 467, 558, 481], "page": 1},
 {"key": "degree", "value": "Master of Business Administration (MBA)", "bbox_2d": [395, 495, 679, 508], "page": 1},
 {"key": "start_date", "value": "August 23, 2025", "bbox_2d": [395, 522, 505, 536], "page": 1},
 {"key": "duration", "value": "2 years (full-time)", "bbox_2d": [395, 550, 516, 563], "page": 1},
 {"key": "scholarship.name", "value": "Presidential Scholarship", "bbox_2d": [619, 585, 793, 598], "page": 1},
 {"key": "scholarship.amount", "value": "$4,060.00 per semester", "bbox_2d": [88, 603, 255, 616], "page": 1},
 {"key": "deposit_deadline", "value": "March 13, 2025", "bbox_2d": [156, 663, 268, 676], "page": 1},
 {"key": "signer", "value": "David L. Morgan", "bbox_2d": [88, 859, 211, 873], "page": 1},
 {"key": "signer_title", "value": "Director of Admissions", "bbox_2d": [88, 877, 243, 890], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa admission_letter --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check admission_letter` → `python -m docgen.formdir card admission_letter` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa admission_letter --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions admission_letter --show` · `python -m docgen.preview admission_letter --out work/admission_letter`
