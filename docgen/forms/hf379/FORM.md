# 주류구매전용카드 가맹점가입신청서 (`hf379`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf379 · card-hash: 572c3e422abb -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 주류구매전용카드 가맹점가입신청서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf379 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.379 (전자금융) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 19칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `corp.name` ← `company.name` | 상호 | text | 1쪽 [360, 366, 475, 385] | 늘 | 규칙: '상호' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:23 | 묻기 |
| `corp.biz_no` ← `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [357, 390, 464, 411] | 늘 | 규칙: '사업자등록번호' → `company.biz_no` | 고객 정보 (키 `company.biz_no`) | fields.json:35 | 묻기 |
| `account` | 계좌번호 | account_no | 1쪽 [362, 480, 530, 505] | 늘 | 규칙: '계좌번호' → `account` | 고객 정보 (키 `account`) | fields.json:156 | 묻기 |
| `customer.name` | 성명 | text | 1쪽 [764, 376, 847, 398] | 늘 | 규칙: '성명' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:167 | 묻기 |
| `customer.name2` | 예금주 | text | 1쪽 [767, 480, 850, 503] | 늘 | 규칙: '예금주' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:179 | 묻기 |
| `corp.established` ← `company.established` | 개업일 | date | 1쪽 [200, 521, 299, 545] | 늘 | 규칙: '개업일' → `company.established` | 고객 정보 (키 `company.established`) | fields.json:190 | 묻기 |
| `자본금` | 자본금 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:201 | 묻기 |
| `corp.biz_item` ← `company.biz_item` | 업종 | text | 1쪽 [480, 521, 559, 545] | 늘 | 규칙: '업종' → `company.biz_item` | 고객 정보 (키 `company.biz_item`) | fields.json:212 | 묻기 |
| `매출액` | 매출액 | number | 1쪽 [503, 547, 584, 565] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:223 | 묻기 |
| `취급품목` | 취급품목 | text | 1쪽 [765, 522, 882, 546] | 늘 | 항목명 그대로 | 값 종류 `goods` (항목명 자동) | fields.json:235 | 묻기 |
| `종업원수` | 종업원수 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:246 | 묻기 |
| `employer.name` | 소속 | text | 1쪽 [569, 822, 680, 838] | 늘 | 규칙: '소속' → `employer.name` | 고객 정보 (키 `employer.name`) | fields.json:318 | 묻기 |
| `employer.name2` | 소속 | text | 1쪽 [572, 848, 683, 864] | 늘 | 규칙: '소속' → `employer.name` | 고객 정보 (키 `employer.name`) | fields.json:329 | 묻기 |
| `customer.name3` | 성명 | text | 1쪽 [768, 819, 852, 843] | 늘 | 규칙: '성명' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:340 | 묻기 |
| `customer.name4` | 성명 | text | 1쪽 [767, 844, 851, 867] | 늘 | 규칙: '성명' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:351 | 묻기 |
| `date` | 작성일 | date | 1쪽 [405, 691, 615, 705] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:401 | 묻기 |
| `signer.name` | 신청인(상호) | text | 1쪽 [478, 716, 595, 735] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:427 | 묻기 |
| `date2` | 작성일 | date | 2쪽 [757, 850, 926, 863] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:444 | 묻기 |
| `signer2.name` | 가맹점신청인 | text | 2쪽 [769, 874, 837, 894] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:470 | 묻기 |

## 체크·도장·서명 (marks) — 9칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.주소` | 주소 | checkbox (보기1 / 보기2 / - / 보기4 / 보기5 / 보기6) | 1쪽 [386, 423, 400, 434] | 늘 | 체크 (항목명) | 보기 중 고름: ? / ? / - / ? / ? / ? | fields.json:47 | 묻기 |
| `check.사업체구분` | 사업체구분 | checkbox (종합 / 수입 / 특정) | 1쪽 [557, 593, 599, 604] | 늘 | 체크 (항목명) | 보기 중 고름: 종합 / 수입 / 특정 | fields.json:257 | 묻기 |
| `check.주류구매전용카드가맹점가입신청서` | 주류구매전용카드가맹점가입신청서( | checkbox (보나뱅크(주) / (주)엔젤넷)) | 1쪽 [728, 101, 877, 122] | 늘 | 체크 (항목명) | 보기 중 고름: 보나뱅크(주) / (주)엔젤넷) | fields.json:362 | 묻기 |
| `seal.corp` ← `seal.signer` | 신청인(상호) | seal | 1쪽 [647, 720, 674, 732] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:427 | 묻기 |
| `sign.customer` ← `sign.signer` | 신청인(상호) | signature | 1쪽 [647, 720, 674, 732] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:427 | 묻기 |
| `seal.customer` ← `seal.signer2` | 가맹점신청인 | seal | 2쪽 [904, 880, 927, 890] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:470 | 묻기 |
| `sign.signer2` | 가맹점신청인 | signature | 2쪽 [904, 880, 927, 890] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:470 | 묻기 |
| `seal.signer3` | 지점장 | seal | 2쪽 [904, 908, 927, 919] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:487 | 묻기 |
| `sign.signer3` | 지점장 | signature | 2쪽 [904, 908, 927, 919] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:487 | 묻기 |

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
"주류구매전용카드 가맹점가입신청서"
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
 "702-81-38348",
 "540-121210-96628",
 "남궁예태",
 "2020.06.15",
 "화학제품",
 "27,620,000",
 "플라스틱 원료",
 "주식회사 다온패션"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"(주)미래케미칼"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"플라스틱 원료"
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
- corp.name: 상호 (법인·사업자 상호)
- corp.biz_no: 사업자등록번호 (법인·사업자 사업자등록번호)
- account: 계좌번호
- customer.name: 성명 (고객 성명, 같은 항목명 중 1번째 칸)
- customer.name2: 예금주
- corp.established: 개업일 (법인·사업자 설립일)
- 자본금: 자본금
- corp.biz_item: 업종 (법인·사업자 업종)
- 매출액: 매출액
- 취급품목: 취급품목
- 종업원수: 종업원수
- employer.name: 소속 (직장 이름, 같은 항목명 중 1번째 칸)
- employer.name2: 소속 (같은 항목명 중 2번째 칸)
- customer.name3: 성명 (같은 항목명 중 2번째 칸)
- customer.name4: 성명 (같은 항목명 중 3번째 칸)
- date: 작성일 (같은 항목명 중 1번째 칸)
- signer.name: 신청인(상호) (법인·사업자의 성명)
- date2: 작성일 (같은 항목명 중 2번째 칸)
- signer2.name: 가맹점신청인 (고객 본인의 성명)
```

답:

```json
[{"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [360, 366, 475, 385], "page": 1},
 {"key": "corp.biz_no", "value": "702-81-38348", "bbox_2d": [357, 390, 464, 411], "page": 1},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [362, 480, 530, 505], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [764, 376, 847, 398], "page": 1},
 {"key": "customer.name2", "value": "남궁예태", "bbox_2d": [767, 480, 850, 503], "page": 1},
 {"key": "corp.established", "value": "2020.06.15", "bbox_2d": [200, 521, 299, 545], "page": 1},
 {"key": "자본금", "value": null},
 {"key": "corp.biz_item", "value": "화학제품", "bbox_2d": [480, 521, 559, 545], "page": 1},
 {"key": "매출액", "value": "27,620,000", "bbox_2d": [503, 547, 584, 565], "page": 1},
 {"key": "취급품목", "value": "플라스틱 원료", "bbox_2d": [765, 522, 882, 546], "page": 1},
 {"key": "종업원수", "value": null},
 {"key": "employer.name", "value": "주식회사 다온패션", "bbox_2d": [569, 822, 680, 838], "page": 1},
 {"key": "employer.name2", "value": "주식회사 다온패션", "bbox_2d": [572, 848, 683, 864], "page": 1},
 {"key": "customer.name3", "value": "남궁예태", "bbox_2d": [768, 819, 852, 843], "page": 1},
 {"key": "customer.name4", "value": "남궁예태", "bbox_2d": [767, 844, 851, 867], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [405, 691, 615, 705], "page": 1},
 {"key": "signer.name", "value": "(주)미래케미칼", "bbox_2d": [478, 716, 595, 735], "page": 1},
 {"key": "date2", "value": "2025년 4월 1일", "bbox_2d": [757, 850, 926, 863], "page": 2},
 {"key": "signer2.name", "value": "남궁예태", "bbox_2d": [769, 874, 837, 894], "page": 2}]
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
- check.주소: 주소 (체크박스, 보기: 보기1 / 보기2 / - / 보기4 / 보기5 / 보기6)
- check.사업체구분: 사업체구분 (체크박스, 보기: 종합 / 수입 / 특정)
- check.주류구매전용카드가맹점가입신청서: 주류구매전용카드가맹점가입신청서( (체크박스, 보기: 보나뱅크(주) / (주)엔젤넷))
- seal.corp: 신청인(상호) (법인·사업자 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 신청인(상호) (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.customer: 가맹점신청인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.signer2: 가맹점신청인 (고객 본인의 신청인, 같은 항목명 중 2번째 칸, 서명)
- seal.signer3: 지점장 (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer3: 지점장 (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.주소", "value": "보기2", "bbox_2d": [386, 423, 400, 434], "page": 1},
 {"key": "check.사업체구분", "value": "특정", "bbox_2d": [557, 593, 570, 604], "page": 1},
 {"key": "check.주류구매전용카드가맹점가입신청서", "value": "(주)엔젤넷)", "bbox_2d": [728, 101, 755, 122], "page": 1},
 {"key": "seal.corp", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [647, 720, 674, 732], "page": 1},
 {"key": "seal.customer", "value": false},
 {"key": "sign.signer2", "value": true, "bbox_2d": [904, 880, 927, 890], "page": 2},
 {"key": "seal.signer3", "value": false},
 {"key": "sign.signer3", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf379 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf379` → `python -m docgen.formdir card hf379` (실제 질문→답 확인).

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
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf379 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf379 --show` · `python -m docgen.preview hf379 --out work/hf379`
