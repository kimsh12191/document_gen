# 퇴직연금 계약해지 신청서(기업형IRP) (`hf193`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf193 · card-hash: 9c55046271dd -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 퇴직연금 계약해지 신청서(기업형IRP)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.193 (퇴직연금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 14칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `서류확인및접수확인자` | 서류확인및접수확인자 | text | - | 늘 | 표 행 (묶음·항목명 '서류확인 및 접수확인자') | 값 종류 `text` (항목명 자동) | fields.json:17 | 묻기 |
| `corp.name` ← `company.name` | 기업명 | text | 1쪽 [243, 278, 379, 299] | 늘 | 규칙: '기업명' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:29 | 묻기 |
| `account` | 퇴직연금계좌번호 | account_no | 1쪽 [665, 278, 807, 296] | 늘 | 규칙: '퇴직연금 계좌번호' → `account` | 고객 정보 (키 `account`) | fields.json:40 | 묻기 |
| `customer.name` | 성명 | text | 1쪽 [105, 483, 186, 501] | 늘 | 표 행 (묶음·항목명 '성명') | 값 종류 `person` (항목명 자동) | fields.json:173 | 묻기 |
| `금융기관명` | 금융기관명 | text | 1쪽 [204, 627, 285, 645] | 늘 | 항목명 그대로 | 값 종류 `bank` (항목명 자동) | fields.json:230 | 묻기 |
| `account2` | 계좌번호 | account_no | 1쪽 [187, 653, 330, 674] | 늘 | 규칙: '계좌번호' → `account` | 고객 정보 (키 `account`) | fields.json:241 | 묻기 |
| `customer.birth` | 생년월일 | date | 1쪽 [243, 483, 376, 502] | 늘 | 표 행 (묶음·항목명 '생년월일') | 값 종류 `date` (항목명 자동) | fields.json:252 | 묻기 |
| `employer.hire_date` | 입사일자 | date | 1쪽 [436, 483, 521, 502] | 늘 | 표 행 (묶음·항목명 '입사일자') | 값 종류 `date` (항목명 자동) | fields.json:309 | 묻기 |
| `중간정산일자` | 중간정산일자 | date | 1쪽 [582, 484, 673, 503] | 늘 | 표 행 (묶음·항목명 '중간정산일자') | 값 종류 `date` (항목명 자동) | fields.json:321 | 묻기 |
| `잔여부담금` | 잔여부담금 | number | 1쪽 [685, 563, 766, 581] | 늘 | 표 행 (묶음·항목명 '잔여부담금') | 값 종류 `amount` (항목명 자동) | fields.json:333 | 묻기 |
| `퇴직일자` | 퇴직일자 | date | 1쪽 [773, 483, 863, 501] | 늘 | 표 행 (묶음·항목명 '퇴직일자') | 값 종류 `date` (항목명 자동) | fields.json:390 | 묻기 |
| `date` | 작성일 | date | 1쪽 [697, 226, 904, 243] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:447 | 묻기 |
| `signer.name` | 기업명 | text | 1쪽 [249, 882, 383, 900] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:473 | 묻기 |
| `signer2.name` | 가입자 | text | 1쪽 [678, 880, 759, 898] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:490 | 묻기 |

## 체크·도장·서명 (marks) — 10칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.해지사유` | 해지사유 | checkbox (제도폐지 / 사업장 파산/폐업 / 사업장의 인수합병 / 법령 변경) | 1쪽 [363, 339, 492, 355] | 늘 | 체크 (항목명) | 보기 중 고름: 제도폐지 / 사업장 파산/폐업 / 사업장의 인수합병 / 법령 변경 | fields.json:51 | 묻기 |
| `check.수수료연동출금` | 수수료연동출금** | checkbox (연동출금 동의 (사전에 약정된 경우) / 연동출금 미동의(기업별도입금)) | 1쪽 [519, 366, 738, 381] | 늘 | 체크 (항목명) | 보기 중 고름: 연동출금 동의 (사전에 약정된 경우) / 연동출금 미동의(기업별도입금) | fields.json:128 | 묻기 |
| `check.개인형IRP` | 개인형IRP | checkbox (개인형 IRP / 요구불계좌) | 1쪽 [105, 555, 193, 570] | 늘 | 체크 (항목명) | 보기 중 고름: 개인형 IRP / 요구불계좌 | fields.json:185 | 묻기 |
| `check.만55세이후퇴직` | 만55세이후퇴직 | checkbox (만55세이후 퇴직 / 만원 이하 퇴직금 지급) | 1쪽 [248, 555, 376, 570] | 늘 | 체크 (항목명) | 보기 중 고름: 만55세이후 퇴직 / 만원 이하 퇴직금 지급 | fields.json:264 | 묻기 |
| `check.계좌번호` | 계좌번호 | checkbox (국민연금전환금 / 계속근로기관 1년 미만) | 1쪽 [586, 651, 756, 666] | 늘 | 체크 (항목명) | 보기 중 고름: 국민연금전환금 / 계속근로기관 1년 미만 | fields.json:345 | 묻기 |
| `check.적용` | 적용 | checkbox (적용 / 미적용) | 1쪽 [776, 555, 825, 570] | 늘 | 체크 (항목명) | 보기 중 고름: 적용 / 미적용 | fields.json:402 | 묻기 |
| `seal.corp` ← `seal.signer` | 기업명 | seal | 1쪽 [434, 883, 459, 897] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:473 | 묻기 |
| `sign.customer` ← `sign.signer` | 기업명 | signature | 1쪽 [434, 883, 459, 897] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:473 | 묻기 |
| `seal.customer` ← `seal.signer2` | 가입자 | seal | 1쪽 [835, 883, 860, 897] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:490 | 묻기 |
| `sign.signer2` | 가입자 | signature | 1쪽 [835, 883, 860, 897] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:490 | 묻기 |

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
"퇴직연금 계약해지 신청서(기업형IRP)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "(주)미래케미칼",
 "540-121210-96628",
 "남궁예태",
 "농협은행",
 "1985년 3월 28일",
 "2021.03.06",
 "2024.09.24",
 "6,740,000",
 "2024.06.05"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"540-121210-96628"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2024.06.05"
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
- 서류확인및접수확인자: 서류확인및접수확인자
- corp.name: 기업명 (법인·사업자 상호, 같은 항목명 중 1번째 칸)
- account: 퇴직연금계좌번호
- customer.name: 성명 (고객 성명)
- 금융기관명: 금융기관명
- account2: 계좌번호
- customer.birth: 생년월일 (고객 생년월일)
- employer.hire_date: 입사일자 (직장 입사일)
- 중간정산일자: 중간정산일자
- 잔여부담금: 잔여부담금
- 퇴직일자: 퇴직일자
- date: 작성일
- signer.name: 기업명 (법인·사업자의 성명, 같은 항목명 중 2번째 칸)
- signer2.name: 가입자 (고객 본인의 성명)
```

답:

```json
[{"key": "서류확인및접수확인자", "value": null},
 {"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [243, 278, 379, 299], "page": 1},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [665, 278, 807, 296], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [105, 483, 186, 501], "page": 1},
 {"key": "금융기관명", "value": "농협은행", "bbox_2d": [204, 627, 285, 645], "page": 1},
 {"key": "account2", "value": "540-121210-96628", "bbox_2d": [187, 653, 330, 674], "page": 1},
 {"key": "customer.birth", "value": "1985년 3월 28일", "bbox_2d": [243, 483, 376, 502], "page": 1},
 {"key": "employer.hire_date", "value": "2021.03.06", "bbox_2d": [436, 483, 521, 502], "page": 1},
 {"key": "중간정산일자", "value": "2024.09.24", "bbox_2d": [582, 484, 673, 503], "page": 1},
 {"key": "잔여부담금", "value": "6,740,000", "bbox_2d": [685, 563, 766, 581], "page": 1},
 {"key": "퇴직일자", "value": "2024.06.05", "bbox_2d": [773, 483, 863, 501], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [697, 226, 904, 243], "page": 1},
 {"key": "signer.name", "value": "(주)미래케미칼", "bbox_2d": [249, 882, 383, 900], "page": 1},
 {"key": "signer2.name", "value": "남궁예태", "bbox_2d": [678, 880, 759, 898], "page": 1}]
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
- check.해지사유: 해지사유 (체크박스, 보기: 제도폐지 / 사업장 파산/폐업 / 사업장의 인수합병 / 법령 변경)
- check.수수료연동출금: 수수료연동출금** (체크박스, 보기: 연동출금 동의 (사전에 약정된 경우) / 연동출금 미동의(기업별도입금))
- check.개인형IRP: 개인형IRP (체크박스, 보기: 개인형 IRP / 요구불계좌)
- check.만55세이후퇴직: 만55세이후퇴직 (체크박스, 보기: 만55세이후 퇴직 / 만원 이하 퇴직금 지급)
- check.계좌번호: 계좌번호 (체크박스, 보기: 국민연금전환금 / 계속근로기관 1년 미만)
- check.적용: 적용 (체크박스, 보기: 적용 / 미적용)
- seal.corp: 기업명 (법인·사업자 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 기업명 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.customer: 가입자 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.signer2: 가입자 (고객 본인의 신청인, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.해지사유", "value": "사업장 파산/폐업", "bbox_2d": [363, 340, 377, 355], "page": 1},
 {"key": "check.수수료연동출금", "value": "연동출금 미동의(기업별도입금)", "bbox_2d": [519, 367, 534, 381], "page": 1},
 {"key": "check.개인형IRP", "value": "개인형 IRP", "bbox_2d": [105, 556, 120, 570], "page": 1},
 {"key": "check.만55세이후퇴직", "value": "만55세이후 퇴직", "bbox_2d": [248, 556, 263, 570], "page": 1},
 {"key": "check.계좌번호", "value": "계속근로기관 1년 미만", "bbox_2d": [586, 652, 601, 666], "page": 1},
 {"key": "check.적용", "value": "적용", "bbox_2d": [776, 556, 791, 570], "page": 1},
 {"key": "seal.corp", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [434, 883, 459, 897], "page": 1},
 {"key": "seal.customer", "value": false},
 {"key": "sign.signer2", "value": false}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf193` → `python -m docgen.formdir card hf193` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | studio ① 서식 › 영역 편집에서 그리기 (`fields.json` items 에 한 칸) | 다시 |
| 답의 위치 (박스) | `fields.json` 그 칸의 `rect` [x0, y0, x1, y1] (pt) — 또는 영역 편집 | 다시 |
| 답의 키 | `fields.json` 그 칸에 `"key"` (없으면 규칙이 항목명으로 정함 — 모든 서식 공통 규칙은 studio 키 사전) | 다시 |
| 답의 값 | `fields.json` 그 칸에 `"source"` ([값 출처 목록](../_common/values.md)) 또는 값 종류 `"kind"` | 다시 |
| 칸의 항목명 | `fields.json` 그 칸의 `label` | 다시 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf193 --show` · `python -m docgen.preview hf193 --out work/hf193`
