# 금융거래목적확인서 (`financial_transaction_purpose`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card financial_transaction_purpose · card-hash: fe805a211fb7 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 금융거래목적확인서
- **쓰이는 업무:** 개인 계좌개설
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 입출금계좌 신규 시 금융거래 목적과 증빙서류를 확인하는 서식 (대포통장 예방).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_account.py`, `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 14칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank.name` | 은행명 | text | 1쪽 [79, 36, 177, 54] | 늘 | 템플릿 | generate.py | look/template.html.j2:72 · fields.json:10 | 묻기 |
| `customer.name` | 성명 | text | 1쪽 [183, 196, 265, 209] | 늘 | 템플릿 | generate.py | look/template.html.j2:15 · fields.json:50 | 묻기 |
| `customer.nationality` | 국적 | text | 1쪽 [311, 196, 341, 209] | 2/16 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:55 | 묻기 |
| `customer.rrn` | 실명번호 | rrn | 1쪽 [691, 197, 796, 209] | 늘 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:60 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [183, 218, 716, 230] | 늘 | 템플릿 | generate.py | look/template.html.j2:26 · fields.json:30 | 묻기 |
| `customer.mobile` | 연락처 | phone | 1쪽 [183, 239, 279, 251] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:45 | 묻기 |
| `customer.job` | 직업 | text | 1쪽 [691, 239, 722, 251] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:40 | 묻기 |
| `evidence` | 제출증빙서류 | text | 1쪽 [183, 327, 354, 339] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:70 | 묻기 |
| `date` | 작성일 | date | 1쪽 [542, 710, 643, 723] | 늘 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:65 | 묻기 |
| `signature` | 고객성명 | text | 1쪽 [751, 710, 832, 723] | 늘 | 템플릿 | generate.py | look/template.html.j2:70 · fields.json:115 | 묻기 |
| `bank_use.clerk` | 담당 | text | 1쪽 [797, 806, 836, 818] | 늘 | 템플릿 | generate.py | look/template.html.j2:81 · fields.json:15 | 묻기 |
| `bank_use.manager` | 책임자 | text | 1쪽 [877, 806, 916, 818] | 늘 | 템플릿 | generate.py | look/template.html.j2:81 · fields.json:20 | 묻기 |
| `customer.company` | 직장명 | - | - | 11/16 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:35 | 묻기 |
| `purpose_detail` | 기타금융거래목적 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:35 | 묻기 |

## 체크·도장·서명 (marks) — 10칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `account_type` | 신규예금종류 | checkbox (보통예금 / 저축예금 / 기타 입출금예금) | 1쪽 [282, 260, 344, 272] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:5 | 묻기 |
| `purpose` | 금융거래목적 | checkbox (급여계좌 / 사업자 거래 / 공과금 이체 / 모임 회비 / 아르바이트 / 기타) | 1쪽 [491, 306, 557, 318] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:75 | 묻기 |
| `questions.q1` | 통장양도대여요청여부 | checkbox (예 / 아니오) | 1쪽 [864, 508, 911, 520] | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:80 | 묻기 |
| `questions.q2` | 취업대출빙자요청여부 | checkbox (예 / 아니오) | 1쪽 [864, 536, 911, 549] | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:85 | 묻기 |
| `questions.q3` | 최근타행계좌개설여부 | checkbox (예 / 아니오) | 1쪽 [825, 557, 841, 570] | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:90 | 묻기 |
| `seal.customer` | 고객 | seal | 1쪽 [872, 697, 928, 737] | 늘 | 템플릿 | generate.py | fields.json:95 | 묻기 |
| `sign.customer` | 고객 | signature | 1쪽 [852, 709, 948, 724] | 늘 | 템플릿 | generate.py | fields.json:110 | 묻기 |
| `bank_use.result` | 처리결과 | checkbox (일반계좌 개설 / 금융거래한도계좌 개설 / 개설 거절) | 1쪽 [207, 775, 303, 788] | 늘 | 템플릿 | generate.py | look/template.html.j2:78 · fields.json:25 | 묻기 |
| `seal.staff.clerk` | 담당 | seal | 1쪽 [789, 792, 843, 831] | 늘 | 템플릿 | generate.py | fields.json:100 | 묻기 |
| `seal.staff.manager` | 책임자 | seal | 1쪽 [869, 792, 924, 831] | 늘 | 템플릿 | generate.py | fields.json:105 | 묻기 |

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
"금융거래목적확인서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "국민은행",
 "다나카 유키",
 "일본",
 "020727-8158133",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "010-2686-9570",
 "주부",
 "모임 회칙 및 구성원 명부",
 "2025년 4월 1일",
 "명호혜",
 "성선영"
]
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

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2025년 4월 1일"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- bank.name: 은행명
- customer.name: 성명 (고객 성명)
- customer.nationality: 국적 (고객 국적)
- customer.rrn: 실명번호 (고객 주민등록번호)
- customer.address: 주소 (고객 주소)
- customer.mobile: 연락처 (고객 휴대전화)
- customer.job: 직업 (고객 직업)
- evidence: 제출증빙서류
- date: 작성일
- signature: 고객성명
- bank_use.clerk: 담당
- bank_use.manager: 책임자
```

답:

```json
[{"key": "bank.name", "value": "국민은행", "bbox_2d": [79, 36, 177, 54], "page": 1},
 {"key": "customer.name", "value": "다나카 유키", "bbox_2d": [183, 196, 265, 209], "page": 1},
 {"key": "customer.nationality", "value": "일본", "bbox_2d": [311, 196, 341, 209], "page": 1},
 {"key": "customer.rrn", "value": "020727-8158133", "bbox_2d": [691, 197, 796, 209], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [183, 218, 716, 230], "page": 1},
 {"key": "customer.mobile", "value": "010-2686-9570", "bbox_2d": [183, 239, 279, 251], "page": 1},
 {"key": "customer.job", "value": "주부", "bbox_2d": [691, 239, 722, 251], "page": 1},
 {"key": "evidence", "value": "모임 회칙 및 구성원 명부", "bbox_2d": [183, 327, 354, 339], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [542, 710, 643, 723], "page": 1},
 {"key": "signature", "value": "다나카 유키", "bbox_2d": [751, 710, 832, 723], "page": 1},
 {"key": "bank_use.clerk", "value": "명호혜", "bbox_2d": [797, 806, 836, 818], "page": 1},
 {"key": "bank_use.manager", "value": "성선영", "bbox_2d": [877, 806, 916, 818], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- account_type: 신규예금종류 (체크박스, 보기: 보통예금 / 저축예금 / 기타 입출금예금)
- purpose: 금융거래목적 (체크박스, 보기: 급여계좌 / 사업자 거래 / 공과금 이체 / 모임 회비 / 아르바이트 / 기타)
- questions.q1: 통장양도대여요청여부 (체크박스, 보기: 예 / 아니오)
- questions.q2: 취업대출빙자요청여부 (체크박스, 보기: 예 / 아니오)
- questions.q3: 최근타행계좌개설여부 (체크박스, 보기: 예 / 아니오)
- seal.customer: 고객 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 고객 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- bank_use.result: 처리결과 (체크박스, 보기: 일반계좌 개설 / 금융거래한도계좌 개설 / 개설 거절)
- seal.staff.clerk: 담당 (도장)
- seal.staff.manager: 책임자 (도장)
```

답:

```json
[{"key": "account_type", "value": "저축예금", "bbox_2d": [269, 260, 278, 272], "page": 1},
 {"key": "purpose", "value": "모임 회비", "bbox_2d": [478, 306, 487, 318], "page": 1},
 {"key": "questions.q1", "value": "아니오", "bbox_2d": [851, 508, 860, 520], "page": 1},
 {"key": "questions.q2", "value": "아니오", "bbox_2d": [851, 536, 860, 549], "page": 1},
 {"key": "questions.q3", "value": "예", "bbox_2d": [812, 557, 822, 570], "page": 1},
 {"key": "seal.customer", "value": true, "bbox_2d": [872, 697, 928, 737], "page": 1},
 {"key": "sign.customer", "value": false},
 {"key": "bank_use.result", "value": "일반계좌 개설", "bbox_2d": [193, 775, 203, 788], "page": 1},
 {"key": "seal.staff.clerk", "value": true, "bbox_2d": [789, 792, 843, 831], "page": 1},
 {"key": "seal.staff.manager", "value": true, "bbox_2d": [869, 792, 924, 831], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check financial_transaction_purpose` → `python -m docgen.formdir card financial_transaction_purpose` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions financial_transaction_purpose --show` · `python -m docgen.preview financial_transaction_purpose --out work/financial_transaction_purpose`
