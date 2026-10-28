# 예금거래신청서 (`account_opening_application`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card account_opening_application · card-hash: 5c7e27df8a1c -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 예금거래신청서 (다른 이름: 은행거래신청서)
- **쓰이는 업무:** 개인 계좌개설, 전자금융 가입
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 계좌개설(신규) 신청서 — 상품, 통장, 전자금융, 알림 서비스.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_account.py`, `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 35칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `bank.name` | 은행명 | text | 1쪽 [66, 27, 162, 45] | 늘 | generate.py | look/template.html.j2:92 | 묻기 |
| `customer.name` | 성명 | text | 1쪽 [170, 142, 229, 155] | 늘 | generate.py | look/template.html.j2:17 | 묻기 |
| `customer.name_en` | 영문명 | text | - | 늘 | generate.py | look/template.html.j2:17 | 묻기 |
| `customer.rrn` | 실명번호 | rrn | 1쪽 [170, 161, 271, 174] | 늘 | generate.py | look/template.html.j2:18 | 묻기 |
| `customer.zipcode` | 우편번호 | text | - | 늘 | generate.py | look/template.html.j2:19 | 묻기 |
| `customer.address` | 자택주소 | text | 1쪽 [202, 180, 713, 192] | 늘 | generate.py | look/template.html.j2:19 | 묻기 |
| `customer.mobile` | 휴대폰 | phone | 1쪽 [170, 198, 261, 211] | 늘 | generate.py | look/template.html.j2:20 | 묻기 |
| `customer.email` | 이메일 | text | 1쪽 [569, 198, 700, 211] | 늘 | generate.py | look/template.html.j2:20 | 묻기 |
| `customer.job` | 직업 | text | 1쪽 [170, 217, 199, 229] | 늘 | generate.py | look/template.html.j2:21 | 묻기 |
| `product.name` | 상품명 | text | 1쪽 [170, 279, 262, 291] | 늘 | generate.py | look/template.html.j2:27 | 묻기 |
| `product.amount` | 신규금액 | amount | 1쪽 [552, 279, 608, 291] | 늘 | generate.py | look/template.html.j2:27 | 묻기 |
| `ebank.limit_once` | 1회이체한도 | amount | 1쪽 [203, 437, 285, 450] | 늘 | generate.py | look/template.html.j2:51 | 묻기 |
| `ebank.limit_day` | 1일이체한도 | amount | 1쪽 [349, 437, 430, 450] | 늘 | generate.py | look/template.html.j2:52 | 묻기 |
| `protection_limit` | 예금자보호한도 | text | 1쪽 [455, 572, 501, 582] | 13/16 | generate.py | look/template.html.j2:76 | 묻기 |
| `signature` | 확인자 / 신청인 | text | 1쪽 [860, 620, 917, 631] | 늘 | generate.py | look/template.html.j2:10 | 묻기 |
| `date` | 신청일 | date | 1쪽 [569, 666, 680, 678] | 늘 | generate.py | look/template.html.j2:87 | 묻기 |
| `bank_use.account_no` | 계좌번호 | account_no | 1쪽 [180, 727, 293, 740] | 늘 | generate.py | look/template.html.j2:98 | 묻기 |
| `bank_use.branch` | 개설영업점 | text | 1쪽 [180, 747, 239, 759] | 늘 | generate.py | look/template.html.j2:99 | 묻기 |
| `bank_use.clerk` | 담당 | text | 1쪽 [809, 756, 848, 768] | 늘 | generate.py | look/template.html.j2:102 | 묻기 |
| `bank_use.manager` | 책임자 | text | 1쪽 [890, 756, 929, 768] | 늘 | generate.py | look/template.html.j2:102 | 묻기 |
| `extra_products.*.type` | 예금종류 | - | - (1행) | 2/16 | generate.py | look/template.html.j2:42 | 묻기 |
| `extra_products.*.name` | 상품명 | - | - (1행) | 2/16 | generate.py | look/template.html.j2:42 | 묻기 |
| `extra_products.*.amount` | 신규금액 | - | - (1행) | 2/16 | generate.py | look/template.html.j2:42 | 묻기 |
| `extra_products.*.term` | 계약기간 | - | - (1행) | 2/16 | generate.py | look/template.html.j2:42 | 묻기 |
| `extra_products.*.account_no` | 계좌번호 | - | - (1행) | 2/16 | generate.py | look/template.html.j2:42 | 묻기 |
| `agent.name` ← `legal_rep.name` | 법정대리인성명 | - | - | 2/16 | generate.py | look/template.html.j2:10 | 묻기 |
| `agent.relation` ← `legal_rep.relation` | 본인과의관계 | - | - | 2/16 | generate.py | look/template.html.j2:67 | 묻기 |
| `agent.rrn` ← `legal_rep.rrn` | 법정대리인실명번호 | - | - | 2/16 | generate.py | look/template.html.j2:67 | 묻기 |
| `agent.phone` ← `legal_rep.phone` | 법정대리인연락처 | - | - | 2/16 | generate.py | look/template.html.j2:68 | 묻기 |
| `legal_rep.documents` | 제출서류 | - | - | 2/16 | generate.py | look/template.html.j2:68 | 묻기 |
| `customer.company` | 직장명 | - | - | 10/16 | generate.py | look/template.html.j2:21 | 묻기 |
| `product.term` | 계약기간 | - | - | 9/16 | generate.py | look/template.html.j2:28 | 묻기 |
| `product.linked_account` | 출금계좌 | - | - | 9/16 | generate.py | look/template.html.j2:29 | 묻기 |
| `product.interest_payment` | 이자지급방법 | - | - | 4/16 | generate.py | look/template.html.j2:28 | 묻기 |
| `customer.nationality` | 국적 | - | - | 1/16 | generate.py | look/template.html.j2:18 | 묻기 |

## 체크·도장·서명 (marks) — 17칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `product.type` | 예금종류 | checkbox (보통예금 / 저축예금 / 정기예금 / 정기적금 / 주택청약종합저축) | 1쪽 [182, 260, 242, 273] | 늘 | generate.py | look/template.html.j2:26 | 묻기 |
| `passbook` | 통장발행 | checkbox (발행 / 미발행) | 1쪽 [182, 316, 212, 329] | 늘 | generate.py | look/template.html.j2:30 | 묻기 |
| `seal_type` | 인감서명등록 | checkbox (인감 / 서명 / 인감+서명) | 1쪽 [565, 316, 594, 329] | 늘 | generate.py | look/template.html.j2:31 | 묻기 |
| `check_card` | 체크카드 | checkbox (신청 / 미신청) | 1쪽 [235, 357, 279, 369] | 늘 | generate.py | look/template.html.j2:34 | 묻기 |
| `ebank.internet` | 인터넷뱅킹 | checkbox (신청 / 미신청) | 1쪽 [235, 400, 279, 413] | 늘 | generate.py | look/template.html.j2:48 | 묻기 |
| `ebank.mobile` | 모바일뱅킹 | checkbox (신청 / 미신청) | 1쪽 [636, 400, 665, 413] | 늘 | generate.py | look/template.html.j2:49 | 묻기 |
| `ebank.otp` | 보안매체 | checkbox (OTP 발급 / 모바일OTP / 기존 OTP 사용 / 보안카드 / 미신청) | 1쪽 [479, 419, 538, 431] | 늘 | generate.py | look/template.html.j2:50 | 묻기 |
| `alert` | 입출금알림 | checkbox (SMS / 앱 푸시 / 미신청) | 1쪽 [235, 456, 283, 469] | 늘 | generate.py | look/template.html.j2:54 | 묻기 |
| `mail_to` | 우편물수령처 | checkbox (자택 / 직장 / 이메일 / 수령 안함) | 1쪽 [355, 499, 418, 512] | 늘 | generate.py | look/template.html.j2:59 | 묻기 |
| `salary_transfer` | 급여이체지정 | checkbox (지정 / 미지정) | 1쪽 [805, 499, 849, 512] | 늘 | generate.py | look/template.html.j2:60 | 묻기 |
| `seal.customer` ← `seal.applicant` | 신청인 | seal | 1쪽 [869, 666, 960, 680] | 늘 | generate.py | - | 묻기 |
| `sign.customer` ← `sign.applicant` | 신청인 | signature | 1쪽 [834, 656, 994, 687] | 늘 | generate.py | - | 묻기 |
| `bank_use.id_type` | 실명확인증표 | checkbox (주민등록증 / 운전면허증 / 여권 / 외국인등록증 / 모바일신분증) | 1쪽 [192, 767, 267, 779] | 늘 | generate.py | look/template.html.j2:100 | 묻기 |
| `seal.staff.clerk` | 담당 | seal | 1쪽 [801, 743, 856, 781] | 늘 | generate.py | - | 묻기 |
| `seal.staff.manager` | 책임자 | seal | 1쪽 [882, 743, 937, 781] | 늘 | generate.py | - | 묻기 |
| `seal.agent` ← `seal.legal_rep` | 법정대리인 | 도장 | - | 2/16 | generate.py | - | 묻기 |
| `sign.agent` ← `sign.legal_rep` | 법정대리인 | 서명 | - | 2/16 | generate.py | - | 묻기 |

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
"예금거래신청서"
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
 "남궁예태",
 "850328-2489940",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "010-6144-1173",
 "yetae741@gmail.com",
 "주부",
 "급여 우대통장",
 "50,000원",
 "10,000,000원",
 "20,000,000원",
 "5천만원",
 "2025년 04월 01일",
 "428083-43-810930",
 "센텀지점",
 "길영희",
 "전도태"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"50,000원"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"20,000,000원"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- bank.name: 은행명
- customer.name: 성명 (고객 성명)
- customer.name_en: 영문명 (고객 영문 성명)
- customer.rrn: 실명번호 (고객 주민등록번호)
- customer.zipcode: 우편번호
- customer.address: 자택주소 (고객 주소)
- customer.mobile: 휴대폰 (고객 휴대전화)
- customer.email: 이메일 (고객 이메일)
- customer.job: 직업 (고객 직업)
- product.name: 상품명
- product.amount: 신규금액
- ebank.limit_once: 1회이체한도
- ebank.limit_day: 1일이체한도
- protection_limit: 예금자보호한도
- signature: 확인자
- date: 신청일
- bank_use.account_no: 계좌번호
- bank_use.branch: 개설영업점
- bank_use.clerk: 담당
- bank_use.manager: 책임자
```

답:

```json
[{"key": "bank.name", "value": "국민은행", "bbox_2d": [66, 27, 162, 45], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [170, 142, 229, 155], "page": 1},
 {"key": "customer.name_en", "value": null},
 {"key": "customer.rrn", "value": "850328-2489940", "bbox_2d": [170, 161, 271, 174], "page": 1},
 {"key": "customer.zipcode", "value": null},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [202, 180, 713, 192], "page": 1},
 {"key": "customer.mobile", "value": "010-6144-1173", "bbox_2d": [170, 198, 261, 211], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [569, 198, 700, 211], "page": 1},
 {"key": "customer.job", "value": "주부", "bbox_2d": [170, 217, 199, 229], "page": 1},
 {"key": "product.name", "value": "급여 우대통장", "bbox_2d": [170, 279, 262, 291], "page": 1},
 {"key": "product.amount", "value": "50,000원", "bbox_2d": [552, 279, 608, 291], "page": 1},
 {"key": "ebank.limit_once", "value": "10,000,000원", "bbox_2d": [203, 437, 285, 450], "page": 1},
 {"key": "ebank.limit_day", "value": "20,000,000원", "bbox_2d": [349, 437, 430, 450], "page": 1},
 {"key": "protection_limit", "value": "5천만원", "bbox_2d": [455, 572, 501, 582], "page": 1},
 {"key": "signature", "value": "남궁예태", "bbox_2d": [860, 620, 917, 631], "page": 1},
 {"key": "date", "value": "2025년 04월 01일", "bbox_2d": [569, 666, 680, 678], "page": 1},
 {"key": "bank_use.account_no", "value": "428083-43-810930", "bbox_2d": [180, 727, 293, 740], "page": 1},
 {"key": "bank_use.branch", "value": "센텀지점", "bbox_2d": [180, 747, 239, 759], "page": 1},
 {"key": "bank_use.clerk", "value": "길영희", "bbox_2d": [809, 756, 848, 768], "page": 1},
 {"key": "bank_use.manager", "value": "전도태", "bbox_2d": [890, 756, 929, 768], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- product.type: 예금종류 (체크박스, 보기: 보통예금 / 저축예금 / 정기예금 / 정기적금 / 주택청약종합저축)
- passbook: 통장발행 (체크박스, 보기: 발행 / 미발행)
- seal_type: 인감서명등록 (체크박스, 보기: 인감 / 서명 / 인감+서명)
- check_card: 체크카드 (체크박스, 보기: 신청 / 미신청)
- ebank.internet: 인터넷뱅킹 (체크박스, 보기: 신청 / 미신청)
- ebank.mobile: 모바일뱅킹 (체크박스, 보기: 신청 / 미신청)
- ebank.otp: 보안매체 (체크박스, 보기: OTP 발급 / 모바일OTP / 기존 OTP 사용 / 보안카드 / 미신청)
- alert: 입출금알림 (체크박스, 보기: SMS / 앱 푸시 / 미신청)
- mail_to: 우편물수령처 (체크박스, 보기: 자택 / 직장 / 이메일 / 수령 안함)
- salary_transfer: 급여이체지정 (체크박스, 보기: 지정 / 미지정)
- seal.customer: 신청인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 신청인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- bank_use.id_type: 실명확인증표 (체크박스, 보기: 주민등록증 / 운전면허증 / 여권 / 외국인등록증 / 모바일신분증)
- seal.staff.clerk: 담당 (도장)
- seal.staff.manager: 책임자 (도장)
```

답:

```json
[{"key": "product.type", "value": "보통예금", "bbox_2d": [170, 260, 179, 273], "page": 1},
 {"key": "passbook", "value": "발행", "bbox_2d": [170, 316, 179, 329], "page": 1},
 {"key": "seal_type", "value": "인감", "bbox_2d": [552, 316, 561, 329], "page": 1},
 {"key": "check_card", "value": "미신청", "bbox_2d": [222, 357, 231, 369], "page": 1},
 {"key": "ebank.internet", "value": "미신청", "bbox_2d": [222, 400, 231, 413], "page": 1},
 {"key": "ebank.mobile", "value": "신청", "bbox_2d": [623, 400, 632, 413], "page": 1},
 {"key": "ebank.otp", "value": "보안카드", "bbox_2d": [466, 419, 475, 431], "page": 1},
 {"key": "alert", "value": "앱 푸시", "bbox_2d": [222, 456, 231, 469], "page": 1},
 {"key": "mail_to", "value": "수령 안함", "bbox_2d": [342, 499, 351, 512], "page": 1},
 {"key": "salary_transfer", "value": "미지정", "bbox_2d": [792, 499, 801, 512], "page": 1},
 {"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [834, 656, 994, 687], "page": 1},
 {"key": "bank_use.id_type", "value": "주민등록증", "bbox_2d": [180, 767, 189, 779], "page": 1},
 {"key": "seal.staff.clerk", "value": true, "bbox_2d": [801, 743, 856, 781], "page": 1},
 {"key": "seal.staff.manager", "value": true, "bbox_2d": [882, 743, 937, 781], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions account_opening_application --show` · `python -m docgen.preview account_opening_application --out work/account_opening_application`
