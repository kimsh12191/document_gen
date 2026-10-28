# 근로계약서 (`employment_contract`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card employment_contract · card-hash: 95172a594034 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** income · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 근로계약서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 고용노동부 표준근로계약서 (기간의 정함이 없는 경우) — 1.근로개시일 ~ 11.기타, 사업주·근로자 서명.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/income.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 28칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `employer.name` | 사업주 | text | 1쪽 [78, 115, 211, 128] | 늘 | generate.py | look/template.html.j2:33 | 묻기 |
| `customer.name` ← `employee.name` | 근로자 | text | 1쪽 [418, 114, 484, 128] | 늘 | generate.py | look/template.html.j2:29 | 묻기 |
| `start_date` | 근로개시일 | date | 1쪽 [187, 146, 304, 160] | 늘 | generate.py | look/template.html.j2:38 | 묻기 |
| `workplace` | 근무장소 | text | 1쪽 [183, 170, 359, 185] | 늘 | generate.py | look/template.html.j2:42 | 묻기 |
| `job` | 업무의내용 | text | 1쪽 [191, 193, 439, 209] | 늘 | generate.py | look/template.html.j2:43 | 묻기 |
| `work_start` | 소정근로시간 | text | 1쪽 [203, 218, 279, 232] | 늘 | generate.py | look/template.html.j2:44 | 묻기 |
| `work_end` | 소정근로시간 | text | 1쪽 [331, 218, 407, 232] | 늘 | generate.py | look/template.html.j2:44 | 묻기 |
| `break_time` | 휴게시간 | text | 1쪽 [533, 218, 705, 232] | 늘 | generate.py | look/template.html.j2:44 | 묻기 |
| `work_days` | 근무일 | number | 1쪽 [241, 242, 251, 256] | 늘 | generate.py | look/template.html.j2:45 | 묻기 |
| `weekly_holiday` | 주휴일 | text | 1쪽 [544, 242, 561, 256] | 늘 | generate.py | look/template.html.j2:45 | 묻기 |
| `monthly_salary` | 월(일,시간)급 | amount | 1쪽 [219, 284, 295, 298] | 늘 | generate.py | look/template.html.j2:47 | 묻기 |
| `bonus` | 상여금 | text | 1쪽 [323, 305, 355, 317] | 늘 | generate.py | look/template.html.j2:49 | 묻기 |
| `other_pay` | 기타급여 | text | 1쪽 [256, 324, 288, 337] | 늘 | generate.py | look/template.html.j2:51 | 묻기 |
| `allowances.*.name` | 기타급여(제수당등) | text | 1쪽 [119, 343, 152, 356] (1행) | 늘 | generate.py | look/template.html.j2:53 | 묻기 |
| `allowances.*.amount` | 기타급여(제수당등) | amount | 1쪽 [163, 343, 242, 357] (1행) | 늘 | generate.py | look/template.html.j2:53 | 묻기 |
| `pay_day` | 임금지급일 | amount | 1쪽 [360, 383, 379, 396] | 늘 | generate.py | look/template.html.j2:55 | 묻기 |
| `pay_method` | 지급방법 | text | 1쪽 [377, 403, 582, 415] | 늘 | generate.py | look/template.html.j2:56 | 묻기 |
| `special_terms.*` | 특약사항 | text | 1쪽 [112, 664, 605, 681] (1행) | 3/16 | generate.py | - | 묻기 |
| `contract_date` | 계약일 | date | 2쪽 [442, 67, 558, 81] | 늘 | generate.py | look/template.html.j2:81 | 묻기 |
| `employer.phone` | 전화 | phone | 2쪽 [466, 119, 556, 131] | 늘 | generate.py | look/template.html.j2:84 | 묻기 |
| `employer.address` | 주소 | text | 2쪽 [275, 140, 553, 153] | 늘 | generate.py | look/template.html.j2:85 | 묻기 |
| `employer.ceo` | 대표자 | text | 2쪽 [275, 170, 323, 183] | 늘 | generate.py | look/template.html.j2:86 | 묻기 |
| `customer.address` ← `employee.address` | 주소 | text | 2쪽 [274, 208, 631, 224] | 늘 | generate.py | look/template.html.j2:87 | 묻기 |
| `customer.phone` ← `employee.phone` | 연락처 | phone | 2쪽 [274, 231, 389, 245] | 늘 | generate.py | look/template.html.j2:88 | 묻기 |
| `bonus_amount` | 상여금 | - | - | 9/16 | generate.py | look/template.html.j2:49 | 묻기 |
| `end_date` | 근로계약종료일 | - | - | 3/16 | generate.py | look/template.html.j2:38 | 묻기 |
| `probation.period` | 수습기간 | - | - | 5/16 | generate.py | look/template.html.j2:69 | 묻기 |
| `probation.wage_rate` | 수습기간임금지급률 | - | - | 5/16 | generate.py | look/template.html.j2:69 | 묻기 |

## 체크·도장·서명 (marks) — 3칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.employer` | 사용자 | seal | 2쪽 [383, 158, 439, 197] | 늘 | generate.py | - | 묻기 |
| `seal.customer` ← `seal.employee` | 근로자 | seal | 2쪽 [357, 253, 400, 271] | 늘 | generate.py | - | 묻기 |
| `sign.customer` ← `sign.employee` | 근로자 | signature | 2쪽 [357, 253, 400, 271] | 늘 | generate.py | - | 묻기 |

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
"근로계약서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "주식회사 다온패션",
 "남궁예태",
 "2021년 3월 6일",
 "주식회사 다온패션 본사",
 "고객지원팀 고객 상담 및 CS 관리",
 "08시 00분",
 "17시 00분",
 "12시 00분 ~ 13시 00분",
 "5",
 "일",
 "3,758,330",
 "없음",
 "있음",
 "식대",
 "200,000원",
 "자가운전보조금",
 "25",
 "근로자 명의 예금통장에 입금",
 "근로자는 회사의 사전 승인 없이 다른 사업장에 겸직하지 아니한다.",
 "연봉은 매년 1월 인사평가 결과에 따라 조정하며, 조정된 연봉은 별도 연봉계약서로 정한다.",
 "출장 시 교통비·숙박비는 회사 여비규정에 따라 실비로 지급한다.",
 "개인정보 수집·이용 동의서는 별지로 작성하여 이 계약서에 첨부한다.",
 "월 급여에는 월 20시간분의 고정연장근로수당이 포함되어 있으며, 이를 초과하는 연장근로는 별도 지급한다.",
 "회사가 지급한 노트북 등 업무용 장비는 퇴직 시 즉시 반납한다.",
 "업무상 필요한 경우 근로자의 동의를 얻어 근무장소를 변경할 수 있다.",
 "시용기간 중 근무성적이 현저히 불량한 경우 본채용을 거부할 수 있다.",
 "2021년 3월 1일",
 "051-509-1176",
 "부산광역시 해운대구 해운대로 326, 7층",
 "박정연",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "010-6144-1173"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"고객지원팀 고객 상담 및 CS 관리"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"출장 시 교통비·숙박비는 회사 여비규정에 따라 실비로 지급한다."
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- employer.name: 사업주 (직장 이름)
- customer.name: 근로자 (고객 성명)
- start_date: 근로개시일
- workplace: 근무장소
- job: 업무의내용
- work_start: 소정근로시간 (같은 항목명 중 1번째 칸)
- work_end: 소정근로시간 (같은 항목명 중 2번째 칸)
- break_time: 휴게시간
- work_days: 근무일
- weekly_holiday: 주휴일
- monthly_salary: 월(일,시간)급
- bonus: 상여금
- other_pay: 기타급여
- allowances.0.name: 기타급여(제수당등) (1행)
- allowances.0.amount: 기타급여(제수당등) (1행)
- allowances.1.name: 기타급여(제수당등) (2행)
- allowances.1.amount: 기타급여(제수당등) (2행)
- pay_day: 임금지급일
- pay_method: 지급방법
- special_terms.0: 특약사항 (1번째)
- special_terms.1: 특약사항 (2번째)
- special_terms.2: 특약사항 (3번째)
- special_terms.3: 특약사항 (4번째)
- special_terms.4: 특약사항 (5번째)
- special_terms.5: 특약사항 (6번째)
- special_terms.6: 특약사항 (7번째)
- special_terms.7: 특약사항 (8번째)
- contract_date: 계약일
- employer.phone: 전화 (직장 연락처)
- employer.address: 주소 (직장 주소, 같은 항목명 중 1번째 칸)
- employer.ceo: 대표자
- customer.address: 주소 (고객 주소, 같은 항목명 중 2번째 칸)
- customer.phone: 연락처 (고객 연락처)
```

답:

```json
[{"key": "employer.name", "value": "주식회사 다온패션", "bbox_2d": [78, 115, 211, 128], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [418, 114, 484, 128], "page": 1},
 {"key": "start_date", "value": "2021년 3월 6일", "bbox_2d": [187, 146, 304, 160], "page": 1},
 {"key": "workplace", "value": "주식회사 다온패션 본사", "bbox_2d": [183, 170, 359, 185], "page": 1},
 {"key": "job", "value": "고객지원팀 고객 상담 및 CS 관리", "bbox_2d": [191, 193, 439, 209], "page": 1},
 {"key": "work_start", "value": "08시 00분", "bbox_2d": [203, 218, 279, 232], "page": 1},
 {"key": "work_end", "value": "17시 00분", "bbox_2d": [331, 218, 407, 232], "page": 1},
 {"key": "break_time", "value": "12시 00분 ~ 13시 00분", "bbox_2d": [533, 218, 705, 232], "page": 1},
 {"key": "work_days", "value": "5", "bbox_2d": [241, 242, 251, 256], "page": 1},
 {"key": "weekly_holiday", "value": "일", "bbox_2d": [544, 242, 561, 256], "page": 1},
 {"key": "monthly_salary", "value": "3,758,330", "bbox_2d": [219, 284, 295, 298], "page": 1},
 {"key": "bonus", "value": "없음", "bbox_2d": [323, 305, 355, 317], "page": 1},
 {"key": "other_pay", "value": "있음", "bbox_2d": [256, 324, 288, 337], "page": 1},
 {"key": "allowances.0.name", "value": "식대", "bbox_2d": [119, 343, 152, 356], "page": 1},
 {"key": "allowances.0.amount", "value": "200,000원", "bbox_2d": [163, 343, 242, 357], "page": 1},
 {"key": "allowances.1.name", "value": "자가운전보조금", "bbox_2d": [119, 362, 235, 376], "page": 1},
 {"key": "allowances.1.amount", "value": "200,000원", "bbox_2d": [246, 362, 325, 376], "page": 1},
 {"key": "pay_day", "value": "25", "bbox_2d": [360, 383, 379, 396], "page": 1},
 {"key": "pay_method", "value": "근로자 명의 예금통장에 입금", "bbox_2d": [377, 403, 582, 415], "page": 1},
 {"key": "special_terms.0", "value": "근로자는 회사의 사전 승인 없이 다른 사업장에 겸직하지 아니한다.", "bbox_2d": [112, 664, 605, 681], "page": 1},
 {"key": "special_terms.1", "value": "연봉은 매년 1월 인사평가 결과에 따라 조정하며, 조정된 연봉은 별도 연봉계약서로 정한다.", "bbox_2d": [112, 682, 784, 701], "page": 1},
 {"key": "special_terms.2", "value": "출장 시 교통비·숙박비는 회사 여비규정에 따라 실비로 지급한다.", "bbox_2d": [112, 703, 590, 720], "page": 1},
 {"key": "special_terms.3", "value": "개인정보 수집·이용 동의서는 별지로 작성하여 이 계약서에 첨부한다.", "bbox_2d": [112, 722, 623, 739], "page": 1},
 {"key": "special_terms.4", "value": "월 급여에는 월 20시간분의 고정연장근로수당이 포함되어 있으며, 이를 초과하는 연장근로는 별도 지급한다.", "bbox_2d": [112, 740, 910, 759], "page": 1},
 {"key": "special_terms.5", "value": "회사가 지급한 노트북 등 업무용 장비는 퇴직 시 즉시 반납한다.", "bbox_2d": [112, 761, 577, 778], "page": 1},
 {"key": "special_terms.6", "value": "업무상 필요한 경우 근로자의 동의를 얻어 근무장소를 변경할 수 있다.", "bbox_2d": [112, 780, 627, 797], "page": 1},
 {"key": "special_terms.7", "value": "시용기간 중 근무성적이 현저히 불량한 경우 본채용을 거부할 수 있다.", "bbox_2d": [112, 800, 627, 817], "page": 1},
 {"key": "contract_date", "value": "2021년 3월 1일", "bbox_2d": [442, 67, 558, 81], "page": 2},
 {"key": "employer.phone", "value": "051-509-1176", "bbox_2d": [466, 119, 556, 131], "page": 2},
 {"key": "employer.address", "value": "부산광역시 해운대구 해운대로 326, 7층", "bbox_2d": [275, 140, 553, 153], "page": 2},
 {"key": "employer.ceo", "value": "박정연", "bbox_2d": [275, 170, 323, 183], "page": 2},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [274, 208, 631, 224], "page": 2},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [274, 231, 389, 245], "page": 2}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.employer: 사용자 (도장)
- seal.customer: 근로자 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 근로자 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.employer", "value": true, "bbox_2d": [383, 158, 439, 197], "page": 2},
 {"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": false}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions employment_contract --show` · `python -m docgen.preview employment_contract --out work/employment_contract`
