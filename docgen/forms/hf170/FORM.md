# 퇴직연금 계약이전 신청서(기업형IRP) (`hf170`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf170 · card-hash: 0eb82135f7e2 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 퇴직연금 계약이전 신청서(기업형IRP)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf170 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.170 (퇴직연금) 원본 위에 기재

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
| `corp.name` ← `company.name` | 기업명 | text | 1쪽 [200, 250, 305, 261] | 늘 | 규칙: '기업명' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:43 | 묻기 |
| `customer.name` | 가입자명 | text | 1쪽 [199, 273, 262, 285] | 늘 | 규칙: '가입자명' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:54 | 묻기 |
| `account` | 퇴직연금계좌번호 | account_no | 1쪽 [630, 250, 763, 261] | 늘 | 규칙: '퇴직연금 계좌번호' → `account` | 고객 정보 (키 `account`) | fields.json:65 | 묻기 |
| `customer.birth` | 생년월일 | date | 1쪽 [631, 273, 710, 285] | 늘 | 규칙: '생년월일' → `customer.birth` | 고객 정보 (키 `customer.birth`) | fields.json:76 | 묻기 |
| `예약지급일` | 예약지급일** | date | 1쪽 [196, 402, 275, 414] | 늘 | 항목명 그대로 | 값 종류 `date` (항목명 자동) | fields.json:267 | 묻기 |
| `운용관리기관` | 운용관리기관 | text | 1쪽 [319, 434, 381, 445] | 늘 | 항목명 그대로 | 값 종류 `bank` (항목명 자동) | fields.json:278 | 묻기 |
| `자산관리기관` | 자산관리기관 | text | 1쪽 [322, 457, 385, 468] | 늘 | 항목명 그대로 | 값 종류 `bank` (항목명 자동) | fields.json:290 | 묻기 |
| `현물이전` | 현물이전* | text | - | 늘 | 표 행 (묶음·항목명 '현물이전*') | 값 종류 `text` (항목명 자동) | fields.json:302 | 묻기 |
| `date` | 작성일 | date | 1쪽 [781, 227, 925, 243] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:417 | 묻기 |
| `금융기관` | 금융기관 | text | 1쪽 [618, 430, 681, 441] | 늘 | 항목명 그대로 | 값 종류 `bank` (항목명 자동) | fields.json:443 | 묻기 |
| `account2` | 계좌번호 | account_no | 1쪽 [620, 445, 753, 457] | 늘 | 규칙: '계좌번호' → `account` | 고객 정보 (키 `account`) | fields.json:454 | 묻기 |
| `signer.name` | 가입자 | text | 1쪽 [736, 617, 799, 628] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:465 | 묻기 |
| `signer2.name` | 기업명 | text | 1쪽 [296, 911, 401, 922] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:482 | 묻기 |
| `signer3.name` | 가입자 | text | 1쪽 [632, 911, 695, 922] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:499 | 묻기 |
| `이전받는기업` | 이전받는기업 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:516 | 묻기 |
| `value` | [유의사항] | amount | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:540 | 묻기 |

## 체크·도장·서명 (marks) — 19칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.전부이전` | 전부이전 | checkbox (전부이전) | 1쪽 [101, 346, 166, 360] | 늘 | 체크 (항목명) | 보기 중 고름: 전부이전 | fields.json:87 | 묻기 |
| `check.일부이전` | 일부이전 | checkbox (일부이전) | 1쪽 [101, 371, 166, 385] | 늘 | 체크 (항목명) | 보기 중 고름: 일부이전 | fields.json:116 | 묻기 |
| `check.제도전환` | 제도전환(기업형IRP→DC) | checkbox (제도전환(기업형IRP → DC) / 계열사 이전(과거입사일 인정) / 합병, 분할, 양수도 / 퇴직연금사업자 변경) | 1쪽 [205, 353, 321, 367] | 늘 | 체크 (항목명) | 보기 중 고름: 제도전환(기업형IRP → DC) / 계열사 이전(과거입사일 인정) / 합병, 분할, 양수도 / 퇴직연금사업자 변경 | fields.json:145 | 묻기 |
| `check.계열사이전` | 계열사이전(과거입사일인정) | checkbox (계열사 이전(과거입사일 인정) / 합병, 분할, 양수도) | 1쪽 [408, 371, 524, 385] | 늘 | 체크 (항목명) | 보기 중 고름: 계열사 이전(과거입사일 인정) / 합병, 분할, 양수도 | fields.json:222 | 묻기 |
| `check.수수료연동출금동의` | 수수료연동출금동의 | checkbox (동의(사전에 약정된 경우) / 미동의 (기업별도 입금)) | 1쪽 [637, 393, 791, 407] | 늘 | 체크 (항목명) | 보기 중 고름: 동의(사전에 약정된 경우) / 미동의 (기업별도 입금) | fields.json:314 | 묻기 |
| `check.현물이전` | 현물이전* | checkbox (신청(보유상품 ‘해지 없이’ 이전)) | 1쪽 [732, 320, 920, 334] | 늘 | 체크 (항목명) | 보기 중 고름: 신청(보유상품 ‘해지 없이’ 이전) | fields.json:359 | 묻기 |
| `check.현물이전2` | 현물이전* | checkbox (미신청(보유상품 ‘해지 후’ 이전)) | 1쪽 [732, 346, 920, 360] | 늘 | 체크 (항목명) | 보기 중 고름: 미신청(보유상품 ‘해지 후’ 이전) | fields.json:388 | 묻기 |
| `seal.customer` ← `seal.signer` | 가입자 | seal | 1쪽 [887, 616, 909, 630] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:465 | 묻기 |
| `sign.customer` ← `sign.signer` | 가입자 | signature | 1쪽 [887, 616, 909, 630] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:465 | 묻기 |
| `seal.corp` ← `seal.signer2` | 기업명 | seal | 1쪽 [450, 909, 472, 923] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:482 | 묻기 |
| `sign.signer2` | 기업명 | signature | 1쪽 [450, 909, 472, 923] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:482 | 묻기 |
| `seal.signer3` | 가입자 | seal | 1쪽 [761, 898, 791, 934] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:499 | 묻기 |
| `sign.signer3` | 가입자 | signature | 1쪽 [765, 909, 787, 923] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:499 | 묻기 |
| `seal.signer4` | 이전받는기업의법인인감증명서징구 | seal | 1쪽 [287, 697, 927, 720] | 늘 | 항목명 그대로 | 값 종류 `seal` (항목명 자동) | fields.json:528 | 묻기 |
| `sign.signer4` | 이전받는기업의법인인감증명서징구 | signature | 1쪽 [287, 697, 927, 720] | 늘 | 항목명 그대로 | 값 종류 `seal` (항목명 자동) | fields.json:528 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [795, 48, 854, 89] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [791, 47, 857, 91] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [866, 52, 913, 85] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [857, 47, 921, 91] | 늘 | - | - | - | 묻기 |

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
"퇴직연금 계약이전 신청서(기업형IRP)"
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
 "남궁예태",
 "540-121210-96628",
 "1985.03.28",
 "2025.01.31",
 "국민은행",
 "농협은행"
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
- corp.name: 기업명 (법인·사업자 상호, 같은 항목명 중 1번째 칸)
- customer.name: 가입자명 (고객 성명)
- account: 퇴직연금계좌번호
- customer.birth: 생년월일 (고객 생년월일)
- 예약지급일: 예약지급일**
- 운용관리기관: 운용관리기관
- 자산관리기관: 자산관리기관
- 현물이전: 현물이전*
- date: 작성일
- 금융기관: 금융기관
- account2: 계좌번호
- signer.name: 가입자 (고객 본인의 성명, 같은 항목명 중 1번째 칸)
- signer2.name: 기업명 (법인·사업자의 성명, 같은 항목명 중 2번째 칸)
- signer3.name: 가입자 (고객 본인의 성명, 같은 항목명 중 2번째 칸)
- 이전받는기업: 이전받는기업
- value: [유의사항]
```

답:

```json
[{"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [200, 250, 305, 261], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [199, 273, 262, 285], "page": 1},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [630, 250, 763, 261], "page": 1},
 {"key": "customer.birth", "value": "1985.03.28", "bbox_2d": [631, 273, 710, 285], "page": 1},
 {"key": "예약지급일", "value": "2025.01.31", "bbox_2d": [196, 402, 275, 414], "page": 1},
 {"key": "운용관리기관", "value": "국민은행", "bbox_2d": [319, 434, 381, 445], "page": 1},
 {"key": "자산관리기관", "value": "농협은행", "bbox_2d": [322, 457, 385, 468], "page": 1},
 {"key": "현물이전", "value": null},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [781, 227, 925, 243], "page": 1},
 {"key": "금융기관", "value": "국민은행", "bbox_2d": [618, 430, 681, 441], "page": 1},
 {"key": "account2", "value": "540-121210-96628", "bbox_2d": [620, 445, 753, 457], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [736, 617, 799, 628], "page": 1},
 {"key": "signer2.name", "value": "(주)미래케미칼", "bbox_2d": [296, 911, 401, 922], "page": 1},
 {"key": "signer3.name", "value": "남궁예태", "bbox_2d": [632, 911, 695, 922], "page": 1},
 {"key": "이전받는기업", "value": null},
 {"key": "value", "value": null}]
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
- check.전부이전: 전부이전 (체크박스, 보기: 전부이전)
- check.일부이전: 일부이전 (체크박스, 보기: 일부이전)
- check.제도전환: 제도전환(기업형IRP→DC) (체크박스, 보기: 제도전환(기업형IRP → DC) / 계열사 이전(과거입사일 인정) / 합병, 분할, 양수도 / 퇴직연금사업자 변경)
- check.계열사이전: 계열사이전(과거입사일인정) (체크박스, 보기: 계열사 이전(과거입사일 인정) / 합병, 분할, 양수도)
- check.수수료연동출금동의: 수수료연동출금동의 (체크박스, 보기: 동의(사전에 약정된 경우) / 미동의 (기업별도 입금))
- check.현물이전: 현물이전* (같은 항목명 중 1번째 칸, 체크박스, 보기: 신청(보유상품 ‘해지 없이’ 이전))
- check.현물이전2: 현물이전* (같은 항목명 중 2번째 칸, 체크박스, 보기: 미신청(보유상품 ‘해지 후’ 이전))
- seal.customer: 가입자 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 가입자 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.corp: 기업명 (법인·사업자 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.signer2: 기업명 (고객 본인의 신청인, 같은 항목명 중 2번째 칸, 서명)
- seal.signer3: 가입자 (고객 본인의 신청인, 같은 항목명 중 3번째 칸, 도장)
- sign.signer3: 가입자 (고객 본인의 신청인, 같은 항목명 중 4번째 칸, 서명)
- seal.signer4: 이전받는기업의법인인감증명서징구 (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer4: 이전받는기업의법인인감증명서징구 (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.전부이전", "value": null},
 {"key": "check.일부이전", "value": null},
 {"key": "check.제도전환", "value": "합병, 분할, 양수도", "bbox_2d": [205, 354, 218, 367], "page": 1},
 {"key": "check.계열사이전", "value": "합병, 분할, 양수도", "bbox_2d": [408, 372, 421, 384], "page": 1},
 {"key": "check.수수료연동출금동의", "value": "동의(사전에 약정된 경우)", "bbox_2d": [637, 393, 649, 406], "page": 1},
 {"key": "check.현물이전", "value": "신청(보유상품 ‘해지 없이’ 이전)", "bbox_2d": [732, 321, 745, 334], "page": 1},
 {"key": "check.현물이전2", "value": "미신청(보유상품 ‘해지 후’ 이전)", "bbox_2d": [732, 347, 745, 359], "page": 1},
 {"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [887, 616, 909, 630], "page": 1},
 {"key": "seal.corp", "value": false},
 {"key": "sign.signer2", "value": true, "bbox_2d": [450, 909, 472, 923], "page": 1},
 {"key": "seal.signer3", "value": true, "bbox_2d": [761, 898, 791, 934], "page": 1},
 {"key": "sign.signer3", "value": false},
 {"key": "seal.signer4", "value": false},
 {"key": "sign.signer4", "value": true, "bbox_2d": [287, 697, 927, 720], "page": 1},
 {"key": "seal.staff.담당", "value": true, "bbox_2d": [795, 48, 854, 89], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [866, 52, 913, 85], "page": 1},
 {"key": "sign.staff.책임자", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf170 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf170` → `python -m docgen.formdir card hf170` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf170 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf170 --show` · `python -m docgen.preview hf170 --out work/hf170`
