# 외국환거래 UMS통지서비스 (변경)신청서 (`hf243`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf243 · card-hash: cd6f65eb379f -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 외국환거래 UMS통지서비스 (변경)신청서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.243 (외환) 원본 위에 기재

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
| `당발송금` | 당발송금 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:43 | 묻기 |
| `타발송금내도통지` | 타발송금내도통지 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:54 | 묻기 |
| `타발송금입금통지` | 타발송금입금통지 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:65 | 묻기 |
| `외화수표추심` | 외화수표추심 | amount | 1쪽 [198, 515, 296, 534] | 늘 | 항목명 그대로 | 값 종류 `fx_amount` (항목명 자동) | fields.json:76 | 묻기 |
| `로칼서류접수` | 로칼서류접수 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:87 | 묻기 |
| `수출네고특사번호통지` | 수출네고특사번호통지 | text | 1쪽 [265, 589, 343, 606] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:143 | 묻기 |
| `customer.name` | 고객명 | text | 1쪽 [183, 319, 262, 337] | 늘 | 규칙: '고객명' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:154 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [183, 390, 409, 402] | 늘 | 규칙: '주 소' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:165 | 묻기 |
| `corp.biz_no` ← `company.biz_no` | 사업자등록번호(생년월일) | biz_no | 1쪽 [638, 297, 750, 316] | 늘 | 규칙: '사업자등록번호 (생년월일)' → `company.biz_no` | 고객 정보 (키 `company.biz_no`) | fields.json:565 | 묻기 |
| `SMS수신전화번호` | SMS수신전화번호 | phone | 1쪽 [641, 342, 754, 361] | 늘 | 항목명 그대로 | 값 종류 `phone` (항목명 자동) | fields.json:577 | 묻기 |
| `FAX번호` | FAX번호 | phone | 1쪽 [638, 375, 738, 393] | 늘 | 항목명 그대로 | 값 종류 `phone` (항목명 자동) | fields.json:589 | 묻기 |
| `customer.email` | E-MAIL주소 | text | 1쪽 [640, 397, 802, 418] | 늘 | 규칙: 'E-MAIL 주소' → `customer.email` | 고객 정보 (키 `customer.email`) | fields.json:601 | 묻기 |
| `취급점` | 취급점 | text | 1쪽 [149, 204, 229, 224] | 늘 | 항목명 그대로 | 값 종류 `branch` (항목명 자동) | fields.json:613 | 묻기 |
| `date` | 작성일 | date | 1쪽 [423, 777, 597, 796] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:663 | 묻기 |
| `signer.name` | 신청인 | text | 1쪽 [472, 838, 552, 857] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:689 | 묻기 |
| `수출입금통지` | 수출입금통지(매입/추심포함) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:706 | 묻기 |
| `수출인수통지` | 수출인수통지(매입/추심포함) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:718 | 묻기 |

## 체크·도장·서명 (marks) — 17칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.수입선적서류접수` | 수입선적서류접수( | checkbox (건별 / / 고객별) | 1쪽 [223, 565, 288, 580] | 늘 | 체크 (항목명) | 보기 중 고름: 건별 / / 고객별 | fields.json:98 | 묻기 |
| `check.당발송금` | 당발송금 | checkbox (FAX / E-MAIL / SMS) | 1쪽 [826, 447, 878, 462] | 늘 | 체크 (항목명) | 보기 중 고름: FAX / E-MAIL / SMS | fields.json:176 | 묻기 |
| `check.타발송금내도통지` | 타발송금내도통지 | checkbox (E-MAIL / SMS) | 1쪽 [825, 471, 877, 485] | 늘 | 체크 (항목명) | 보기 중 고름: E-MAIL / SMS | fields.json:237 | 묻기 |
| `check.타발송금입금통지` | 타발송금입금통지 | checkbox (FAX) | 1쪽 [522, 495, 571, 509] | 늘 | 체크 (항목명) | 보기 중 고름: FAX | fields.json:282 | 묻기 |
| `check.외화수표추심` | 외화수표추심 | checkbox (FAX / E-MAIL) | 1쪽 [661, 518, 734, 533] | 늘 | 체크 (항목명) | 보기 중 고름: FAX / E-MAIL | fields.json:311 | 묻기 |
| `check.로칼서류접수` | 로칼서류접수 | checkbox (FAX / E-MAIL) | 1쪽 [661, 542, 734, 556] | 늘 | 체크 (항목명) | 보기 중 고름: FAX / E-MAIL | fields.json:356 | 묻기 |
| `check.FAX` | FAX | checkbox (FAX / E-MAIL) | 1쪽 [661, 565, 734, 580] | 늘 | 체크 (항목명) | 보기 중 고름: FAX / E-MAIL | fields.json:401 | 묻기 |
| `check.수출네고특사번호통지` | 수출네고특사번호통지 | checkbox (FAX / E-MAIL) | 1쪽 [522, 589, 571, 603] | 늘 | 체크 (항목명) | 보기 중 고름: FAX / E-MAIL | fields.json:446 | 묻기 |
| `check.수출입금통지` | 수출입금통지(매입/추심포함) | checkbox (FAX) | 1쪽 [522, 612, 571, 627] | 늘 | 체크 (항목명) | 보기 중 고름: FAX | fields.json:491 | 묻기 |
| `check.수출인수통지` | 수출인수통지(매입/추심포함) | checkbox (FAX / E-MAIL) | 1쪽 [661, 636, 734, 650] | 늘 | 체크 (항목명) | 보기 중 고름: FAX / E-MAIL | fields.json:520 | 묻기 |
| `check.외국환업무에대한UMS통지서비스` | 외국환업무에대한UMS통지서비스( | checkbox (신규, / 변경) 를 신청합니다.) | 1쪽 [663, 246, 728, 262] | 늘 | 체크 (항목명) | 보기 중 고름: 신규, / 변경) 를 신청합니다. | fields.json:624 | 묻기 |
| `seal.customer` ← `seal.signer` | 신청인 | seal | 1쪽 [671, 839, 703, 856] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:689 | 묻기 |
| `sign.customer` ← `sign.signer` | 신청인 | signature | 1쪽 [671, 839, 703, 856] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:689 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [796, 40, 862, 84] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [796, 40, 862, 84] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [862, 40, 923, 84] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [862, 40, 923, 84] | 늘 | - | - | - | 묻기 |

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
"외국환거래 UMS통지서비스 (변경)신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "CNY 174,300",
 "6926-9662",
 "남궁예태",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "702-81-38348",
 "010-6144-1173",
 "051-509-1176",
 "yetae741@gmail.com",
 "센텀지점"
]
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

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"010-6144-1173"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- 당발송금: 당발송금
- 타발송금내도통지: 타발송금내도통지
- 타발송금입금통지: 타발송금입금통지
- 외화수표추심: 외화수표추심
- 로칼서류접수: 로칼서류접수
- 수출네고특사번호통지: 수출네고특사번호통지
- customer.name: 고객명 (고객 성명)
- customer.address: 주소 (고객 주소)
- corp.biz_no: 사업자등록번호(생년월일) (법인·사업자 사업자등록번호)
- SMS수신전화번호: SMS수신전화번호
- FAX번호: FAX번호
- customer.email: E-MAIL주소 (고객 이메일)
- 취급점: 취급점
- date: 작성일
- signer.name: 신청인 (고객 본인의 성명)
- 수출입금통지: 수출입금통지(매입/추심포함)
- 수출인수통지: 수출인수통지(매입/추심포함)
```

답:

```json
[{"key": "당발송금", "value": null},
 {"key": "타발송금내도통지", "value": null},
 {"key": "타발송금입금통지", "value": null},
 {"key": "외화수표추심", "value": "CNY 174,300", "bbox_2d": [198, 515, 296, 534], "page": 1},
 {"key": "로칼서류접수", "value": null},
 {"key": "수출네고특사번호통지", "value": "6926-9662", "bbox_2d": [265, 589, 343, 606], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [183, 319, 262, 337], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [183, 390, 409, 402], "page": 1},
 {"key": "corp.biz_no", "value": "702-81-38348", "bbox_2d": [638, 297, 750, 316], "page": 1},
 {"key": "SMS수신전화번호", "value": "010-6144-1173", "bbox_2d": [641, 342, 754, 361], "page": 1},
 {"key": "FAX번호", "value": "051-509-1176", "bbox_2d": [638, 375, 738, 393], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [640, 397, 802, 418], "page": 1},
 {"key": "취급점", "value": "센텀지점", "bbox_2d": [149, 204, 229, 224], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [423, 777, 597, 796], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [472, 838, 552, 857], "page": 1},
 {"key": "수출입금통지", "value": null},
 {"key": "수출인수통지", "value": null}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- check.수입선적서류접수: 수입선적서류접수( (체크박스, 보기: 건별 / / 고객별)
- check.당발송금: 당발송금 (체크박스, 보기: FAX / E-MAIL / SMS)
- check.타발송금내도통지: 타발송금내도통지 (체크박스, 보기: E-MAIL / SMS)
- check.타발송금입금통지: 타발송금입금통지 (체크박스, 보기: FAX)
- check.외화수표추심: 외화수표추심 (체크박스, 보기: FAX / E-MAIL)
- check.로칼서류접수: 로칼서류접수 (체크박스, 보기: FAX / E-MAIL)
- check.FAX: FAX (체크박스, 보기: FAX / E-MAIL)
- check.수출네고특사번호통지: 수출네고특사번호통지 (체크박스, 보기: FAX / E-MAIL)
- check.수출입금통지: 수출입금통지(매입/추심포함) (체크박스, 보기: FAX)
- check.수출인수통지: 수출인수통지(매입/추심포함) (체크박스, 보기: FAX / E-MAIL)
- check.외국환업무에대한UMS통지서비스: 외국환업무에대한UMS통지서비스( (체크박스, 보기: 신규, / 변경) 를 신청합니다.)
- seal.customer: 신청인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 신청인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.수입선적서류접수", "value": "건별 /", "bbox_2d": [223, 567, 240, 580], "page": 1},
 {"key": "check.당발송금", "value": "SMS", "bbox_2d": [826, 450, 843, 462], "page": 1},
 {"key": "check.타발송금내도통지", "value": "SMS", "bbox_2d": [825, 473, 842, 485], "page": 1},
 {"key": "check.타발송금입금통지", "value": null},
 {"key": "check.외화수표추심", "value": "E-MAIL", "bbox_2d": [661, 520, 678, 533], "page": 1},
 {"key": "check.로칼서류접수", "value": "E-MAIL", "bbox_2d": [661, 544, 678, 556], "page": 1},
 {"key": "check.FAX", "value": "E-MAIL", "bbox_2d": [661, 567, 678, 580], "page": 1},
 {"key": "check.수출네고특사번호통지", "value": "FAX", "bbox_2d": [522, 591, 539, 603], "page": 1},
 {"key": "check.수출입금통지", "value": null},
 {"key": "check.수출인수통지", "value": "E-MAIL", "bbox_2d": [661, 638, 678, 650], "page": 1},
 {"key": "check.외국환업무에대한UMS통지서비스", "value": "신규,", "bbox_2d": [663, 249, 680, 261], "page": 1},
 {"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": false},
 {"key": "sign.staff.책임자", "value": true, "bbox_2d": [862, 40, 923, 84], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf243` → `python -m docgen.formdir card hf243` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf243 --show` · `python -m docgen.preview hf243 --out work/hf243`
