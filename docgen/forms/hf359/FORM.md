# 하나 sERP 이용신청서 (`hf359`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf359 · card-hash: d7210ea6c351 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 하나 sERP 이용신청서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.359 (전자금융) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 16칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `기업인터넷뱅킹ID` | 기업인터넷뱅킹ID | rrn | 1쪽 [204, 223, 334, 235] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:78 | 묻기 |
| `corp.biz_no` ← `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [206, 252, 313, 265] | 늘 | 규칙: '사 업 자 등 록 번 호' → `company.biz_no` | 고객 정보 (키 `company.biz_no`) | fields.json:89 | 묻기 |
| `corp.ceo` ← `company.ceo` | 대표자명 | text | 1쪽 [206, 282, 275, 294] | 늘 | 규칙: '대 표 자 명' → `company.ceo` | 고객 정보 (키 `company.ceo`) | fields.json:100 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [334, 311, 700, 323] | 늘 | 규칙: '주 소' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:111 | 묻기 |
| `담당자명` | 담당자명 | text | 1쪽 [201, 340, 270, 352] | 늘 | 항목명 그대로 | 값 종류 `person` (항목명 자동) | fields.json:122 | 묻기 |
| `담당부서연락처` | 담당부서연락처 | phone | 1쪽 [207, 369, 322, 382] | 늘 | 항목명 그대로 | 값 종류 `phone` (항목명 자동) | fields.json:133 | 묻기 |
| `employer.name` | 회사명 | text | 1쪽 [656, 223, 798, 235] | 늘 | 규칙: '회 사 명' → `employer.name` | 고객 정보 (키 `employer.name`) | fields.json:144 | 묻기 |
| `업태종목` | 업태/종목 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:155 | 묻기 |
| `customer.phone` | 전화번호 | phone | 1쪽 [828, 282, 927, 293] | 늘 | 규칙: '전 화 번 호' → `customer.phone` | 고객 정보 (키 `customer.phone`) | fields.json:166 | 묻기 |
| `담당부서` | 담당부서 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:177 | 묻기 |
| `세금계산서교부용eMail` | 세금계산서교부용e-Mail | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:188 | 묻기 |
| `account` | 출금계좌(하나은행) | account_no | 1쪽 [204, 492, 349, 504] | 늘 | 규칙: '출금계좌(하나은행)' → `account` | 고객 정보 (키 `account`) | fields.json:199 | 묻기 |
| `customer.name` | 예금주 | text | 1쪽 [679, 492, 748, 504] | 늘 | 규칙: '예 금 주' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:210 | 묻기 |
| `date` | 작성일 | date | 1쪽 [219, 623, 426, 640] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:232 | 묻기 |
| `customer.name2` | 성명 | text | 1쪽 [769, 815, 838, 828] | 늘 | 규칙: '성명' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:257 | 묻기 |
| `기타필요서류` | 기타필요서류 | text | 1쪽 [406, 741, 480, 753] | 늘 | 항목명 그대로 | 값 종류 `note` (항목명 자동) | fields.json:268 | 묻기 |

## 체크·도장·서명 (marks) — 3칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.신청구분` | 신청구분 | checkbox (신고 / 해지 / 변경) | 1쪽 [457, 142, 510, 158] | 늘 | 체크 (항목명) | 보기 중 고름: 신고 / 해지 / 변경 | fields.json:17 | 묻기 |
| `seal.signer` | 본인및인감확인 | seal | 1쪽 [317, 803, 372, 842] | 늘 | 항목명 그대로 | 값 종류 `seal` (항목명 자동) | fields.json:221 | 묻기 |
| `sign.signer` | 본인및인감확인 | signature | 1쪽 [246, 809, 444, 836] | 늘 | 항목명 그대로 | 값 종류 `seal` (항목명 자동) | fields.json:221 | 묻기 |

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
"하나 sERP 이용신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "081769-4126143",
 "702-81-38348",
 "남궁예태",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "010-6144-1173",
 "주식회사 다온패션",
 "540-121210-96628",
 "해당 없음"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"081769-4126143"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"남궁예태"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- 기업인터넷뱅킹ID: 기업인터넷뱅킹ID
- corp.biz_no: 사업자등록번호 (법인·사업자 사업자등록번호)
- corp.ceo: 대표자명 (법인·사업자 대표자)
- customer.address: 주소 (고객 주소)
- 담당자명: 담당자명
- 담당부서연락처: 담당부서연락처
- employer.name: 회사명 (직장 이름)
- 업태종목: 업태/종목
- customer.phone: 전화번호 (고객 연락처)
- 담당부서: 담당부서
- 세금계산서교부용eMail: 세금계산서교부용e-Mail
- account: 출금계좌(하나은행)
- customer.name: 예금주 (고객 성명)
- date: 작성일
- customer.name2: 성명
- 기타필요서류: 기타필요서류
```

답:

```json
[{"key": "기업인터넷뱅킹ID", "value": "081769-4126143", "bbox_2d": [204, 223, 334, 235], "page": 1},
 {"key": "corp.biz_no", "value": "702-81-38348", "bbox_2d": [206, 252, 313, 265], "page": 1},
 {"key": "corp.ceo", "value": "남궁예태", "bbox_2d": [206, 282, 275, 294], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [334, 311, 700, 323], "page": 1},
 {"key": "담당자명", "value": "남궁예태", "bbox_2d": [201, 340, 270, 352], "page": 1},
 {"key": "담당부서연락처", "value": "010-6144-1173", "bbox_2d": [207, 369, 322, 382], "page": 1},
 {"key": "employer.name", "value": "주식회사 다온패션", "bbox_2d": [656, 223, 798, 235], "page": 1},
 {"key": "업태종목", "value": null},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [828, 282, 927, 293], "page": 1},
 {"key": "담당부서", "value": null},
 {"key": "세금계산서교부용eMail", "value": null},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [204, 492, 349, 504], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [679, 492, 748, 504], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [219, 623, 426, 640], "page": 1},
 {"key": "customer.name2", "value": "남궁예태", "bbox_2d": [769, 815, 838, 828], "page": 1},
 {"key": "기타필요서류", "value": "해당 없음", "bbox_2d": [406, 741, 480, 753], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- check.신청구분: 신청구분 (체크박스, 보기: 신고 / 해지 / 변경)
- seal.signer: 본인및인감확인 (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer: 본인및인감확인 (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.신청구분", "value": "해지", "bbox_2d": [457, 142, 478, 158], "page": 1},
 {"key": "seal.signer", "value": true, "bbox_2d": [317, 803, 372, 842], "page": 1},
 {"key": "sign.signer", "value": false}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf359` → `python -m docgen.formdir card hf359` (실제 질문→답 확인).

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
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf359 --show` · `python -m docgen.preview hf359 --out work/hf359`
