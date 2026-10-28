# 이전신청(취소)서(DB,DC,기업형IRP 이전용) (`hf182`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf182 · card-hash: 8521eb52415c -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 이전신청(취소)서(DB,DC,기업형IRP 이전용)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf182 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.182 (퇴직연금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 17칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `corp.name` ← `company.name` | 기업명 | text | 1쪽 [437, 287, 568, 310] | 늘 | 규칙: '기업명' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:194 | 묻기 |
| `corp.biz_no` ← `company.biz_no` | 사업자번호 | biz_no | 1쪽 [438, 308, 577, 331] | 늘 | 규칙: '사업자 번호' → `company.biz_no` | 고객 정보 (키 `company.biz_no`) | fields.json:206 | 묻기 |
| `담당자성명` | 담당자성명 | text | 1쪽 [440, 330, 481, 350] | 늘 | 항목명 그대로 | 값 종류 `person` (항목명 자동) | fields.json:218 | 묻기 |
| `customer.phone` | 전화번호 | phone | 1쪽 [439, 349, 584, 372] | 늘 | 규칙: '전화번호' → `customer.phone` | 고객 정보 (키 `customer.phone`) | fields.json:230 | 묻기 |
| `이전금액` | 이전금액***(DB일부이전) | amount | 1쪽 [785, 509, 893, 532] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:438 | 묻기 |
| `금융회사명` | 금융회사명 | text | 1쪽 [539, 567, 600, 586] | 늘 | 항목명 그대로 | 값 종류 `bank` (항목명 자동) | fields.json:451 | 묻기 |
| `signer.name` | 금융기관명:지점명 | text | 1쪽 [499, 901, 554, 925] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:462 | 묻기 |
| `금융회사명2` | 금융회사명 | text | 1쪽 [536, 527, 627, 552] | 늘 | 항목명 그대로 | 값 종류 `bank` (항목명 자동) | fields.json:480 | 묻기 |
| `관리번호` | (운용관리기관관리번호)관리번호 | rrn | 1쪽 [522, 543, 700, 570] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:491 | 묻기 |
| `date` | 작성일 | date | 1쪽 [366, 710, 574, 727] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:502 | 묻기 |
| `signer2.name` | 기업명 | text | 1쪽 [441, 728, 580, 751] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:527 | 묻기 |
| `signer3.name` | 지점명 | text | 1쪽 [300, 909, 356, 931] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:544 | 묻기 |
| `이전받을기관` | 이전받을기관 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:561 | 묻기 |
| `agent.name` | 대리인 | text | 1쪽 [409, 760, 461, 776] | 늘 | 규칙: '대리인' → `agent.name` | 고객 정보 (키 `agent.name`) | fields.json:573 | 묻기 |
| `금융기관명` | 금융기관명 | text | 1쪽 [296, 897, 364, 921] | 늘 | 항목명 그대로 | 값 종류 `bank` (항목명 자동) | fields.json:585 | 묻기 |
| `customer.phone2` | 전화번호 | phone | 1쪽 [725, 896, 884, 920] | 늘 | 규칙: '전화번호' → `customer.phone` | 고객 정보 (키 `customer.phone`) | fields.json:597 | 묻기 |
| `팩스번호` | 팩스번호 | phone | 1쪽 [724, 904, 871, 928] | 늘 | 항목명 그대로 | 값 종류 `phone` (항목명 자동) | fields.json:609 | 묻기 |

## 체크·도장·서명 (marks) — 17칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.신청내용` | 신청내용 | checkbox (이전 신청 / 이전 신청 취소( / 에 하나만 √표시합니다.) | 1쪽 [227, 231, 307, 246] | 늘 | 체크 (항목명) | 보기 중 고름: 이전 신청 / 이전 신청 취소( / 에 하나만 √표시합니다. | fields.json:43 | 묻기 |
| `check.이전의사확인` | 이전의사확인* | checkbox (전화통화 등 / 이전하는 금융회사 방문) | 1쪽 [613, 251, 783, 267] | 늘 | 체크 (항목명) | 보기 중 고름: 전화통화 등 / 이전하는 금융회사 방문 | fields.json:104 | 묻기 |
| `check.신청서제출처` | 신청서제출처 | checkbox (이전하는 금융회사 / 이전받을 금융회사) | 1쪽 [614, 272, 750, 287] | 늘 | 체크 (항목명) | 보기 중 고름: 이전하는 금융회사 / 이전받을 금융회사 | fields.json:149 | 묻기 |
| `check.제도유형` | 제도유형 | checkbox (DB / DC / 기업형IRP) | 1쪽 [507, 406, 546, 421] | 늘 | 체크 (항목명) | 보기 중 고름: DB / DC / 기업형IRP | fields.json:242 | 묻기 |
| `check.이전계약` | 이전계약 | checkbox (운용관리계약+자산관리계약 / 운용관리계약) | 1쪽 [443, 442, 547, 457] | 늘 | 체크 (항목명) | 보기 중 고름: 운용관리계약+자산관리계약 / 운용관리계약 | fields.json:303 | 묻기 |
| `check.이전유형` | 이전유형 | checkbox (전부(계약)이전 / 일부(적립금, 가입자)이전) | 1쪽 [443, 459, 623, 490] | 늘 | 체크 (항목명) | 보기 중 고름: 전부(계약)이전 / 일부(적립금, 가입자)이전 | fields.json:348 | 묻기 |
| `check.이전대상` | 이전대상** | checkbox (전액 현금 / 실물) | 1쪽 [573, 494, 620, 509] | 늘 | 체크 (항목명) | 보기 중 고름: 전액 현금 / 실물 | fields.json:393 | 묻기 |
| `seal.signer` | 금융기관명:지점명 | seal | 1쪽 [612, 905, 637, 919] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:462 | 묻기 |
| `sign.signer` | 금융기관명:지점명 | signature | 1쪽 [612, 905, 637, 919] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:462 | 묻기 |
| `seal.corp` ← `seal.signer2` | 기업명 | seal | 1쪽 [627, 734, 652, 748] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:527 | 묻기 |
| `sign.customer` ← `sign.signer2` | 기업명 | signature | 1쪽 [627, 734, 652, 748] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:527 | 묻기 |
| `seal.signer3` | 지점명 | seal | 1쪽 [397, 902, 443, 939] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:544 | 묻기 |
| `sign.signer3` | 지점명 | signature | 1쪽 [407, 913, 432, 928] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:544 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [791, 54, 835, 85] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [783, 49, 844, 90] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [844, 49, 924, 90] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [844, 49, 924, 90] | 늘 | - | - | - | 묻기 |

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
"이전신청(취소)서(DB,DC,기업형IRP 이전용)"
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
 "이우도",
 "010-6144-1173",
 "3,090,000원",
 "기업은행",
 "김지호",
 "카카오뱅크",
 "007622-5493166",
 "류형희",
 "남궁찬윤",
 "국민은행",
 "051-509-1176"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"010-6144-1173"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"010-6144-1173"
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
- corp.biz_no: 사업자번호 (법인·사업자 사업자등록번호)
- 담당자성명: 담당자성명
- customer.phone: 전화번호 (고객 연락처, 같은 항목명 중 1번째 칸)
- 이전금액: 이전금액***(DB일부이전)
- 금융회사명: 금융회사명 (같은 항목명 중 1번째 칸)
- signer.name: 금융기관명:지점명 (은행·직원의 성명)
- 금융회사명2: 금융회사명 (같은 항목명 중 2번째 칸)
- 관리번호: (운용관리기관관리번호)관리번호
- date: 작성일
- signer2.name: 기업명 (법인·사업자의 성명, 같은 항목명 중 2번째 칸)
- signer3.name: 지점명 (은행·직원의 성명)
- 이전받을기관: 이전받을기관
- agent.name: 대리인 (대리인 성명)
- 금융기관명: 금융기관명
- customer.phone2: 전화번호 (같은 항목명 중 2번째 칸)
- 팩스번호: 팩스번호
```

답:

```json
[{"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [437, 287, 568, 310], "page": 1},
 {"key": "corp.biz_no", "value": "702-81-38348", "bbox_2d": [438, 308, 577, 331], "page": 1},
 {"key": "담당자성명", "value": "이우도", "bbox_2d": [440, 330, 481, 350], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [439, 349, 584, 372], "page": 1},
 {"key": "이전금액", "value": "3,090,000원", "bbox_2d": [785, 509, 893, 532], "page": 1},
 {"key": "금융회사명", "value": "기업은행", "bbox_2d": [539, 567, 600, 586], "page": 1},
 {"key": "signer.name", "value": "김지호", "bbox_2d": [499, 901, 554, 925], "page": 1},
 {"key": "금융회사명2", "value": "카카오뱅크", "bbox_2d": [536, 527, 627, 552], "page": 1},
 {"key": "관리번호", "value": "007622-5493166", "bbox_2d": [522, 543, 700, 570], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [366, 710, 574, 727], "page": 1},
 {"key": "signer2.name", "value": "(주)미래케미칼", "bbox_2d": [441, 728, 580, 751], "page": 1},
 {"key": "signer3.name", "value": "류형희", "bbox_2d": [300, 909, 356, 931], "page": 1},
 {"key": "이전받을기관", "value": null},
 {"key": "agent.name", "value": "남궁찬윤", "bbox_2d": [409, 760, 461, 776], "page": 1},
 {"key": "금융기관명", "value": "국민은행", "bbox_2d": [296, 897, 364, 921], "page": 1},
 {"key": "customer.phone2", "value": "010-6144-1173", "bbox_2d": [725, 896, 884, 920], "page": 1},
 {"key": "팩스번호", "value": "051-509-1176", "bbox_2d": [724, 904, 871, 928], "page": 1}]
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
- check.신청내용: 신청내용 (체크박스, 보기: 이전 신청 / 이전 신청 취소( / 에 하나만 √표시합니다.)
- check.이전의사확인: 이전의사확인* (체크박스, 보기: 전화통화 등 / 이전하는 금융회사 방문)
- check.신청서제출처: 신청서제출처 (체크박스, 보기: 이전하는 금융회사 / 이전받을 금융회사)
- check.제도유형: 제도유형 (체크박스, 보기: DB / DC / 기업형IRP)
- check.이전계약: 이전계약 (체크박스, 보기: 운용관리계약+자산관리계약 / 운용관리계약)
- check.이전유형: 이전유형 (체크박스, 보기: 전부(계약)이전 / 일부(적립금, 가입자)이전)
- check.이전대상: 이전대상** (체크박스, 보기: 전액 현금 / 실물)
- seal.signer: 금융기관명:지점명 (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer: 금융기관명:지점명 (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
- seal.corp: 기업명 (법인·사업자 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 기업명 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.signer3: 지점명 (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer3: 지점명 (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.신청내용", "value": "이전 신청", "bbox_2d": [227, 232, 242, 246], "page": 1},
 {"key": "check.이전의사확인", "value": "이전하는 금융회사 방문", "bbox_2d": [613, 252, 628, 267], "page": 1},
 {"key": "check.신청서제출처", "value": "이전받을 금융회사", "bbox_2d": [614, 272, 628, 287], "page": 1},
 {"key": "check.제도유형", "value": "DC", "bbox_2d": [507, 407, 522, 421], "page": 1},
 {"key": "check.이전계약", "value": "운용관리계약", "bbox_2d": [443, 443, 457, 457], "page": 1},
 {"key": "check.이전유형", "value": null},
 {"key": "check.이전대상", "value": "실물", "bbox_2d": [573, 495, 587, 509], "page": 1},
 {"key": "seal.signer", "value": false},
 {"key": "sign.signer", "value": true, "bbox_2d": [612, 905, 637, 919], "page": 1},
 {"key": "seal.corp", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [627, 734, 652, 748], "page": 1},
 {"key": "seal.signer3", "value": true, "bbox_2d": [397, 902, 443, 939], "page": 1},
 {"key": "sign.signer3", "value": false},
 {"key": "seal.staff.담당", "value": true, "bbox_2d": [791, 54, 835, 85], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": false},
 {"key": "sign.staff.책임자", "value": true, "bbox_2d": [844, 49, 924, 90], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf182 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf182` → `python -m docgen.formdir card hf182` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf182 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf182 --show` · `python -m docgen.preview hf182 --out work/hf182`
