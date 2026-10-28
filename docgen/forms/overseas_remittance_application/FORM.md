# 해외송금신청서 (`overseas_remittance_application`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card overseas_remittance_application · card-hash: 5208aa22ffc9 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 해외송금신청서 (다른 이름: 외화송금신청서)
- **쓰이는 업무:** 해외송금, 유학생 송금
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 당발송금(전신송금 T/T) 신청서 + 은행 사용란(환율/원화환산액).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_account.py`, `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 43칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank.name` | 은행명 | text | 1쪽 [83, 38, 182, 57] | 늘 | 템플릿 | generate.py | look/template.html.j2:73 · fields.json:25 | 묻기 |
| `customer.name` ← `remitter.name` | 송금인성명 | text | 1쪽 [206, 165, 269, 178] | 늘 | 템플릿 | generate.py | look/template.html.j2:11 · fields.json:175 | 묻기 |
| `customer.name_en` ← `remitter.name_en` | 송금인영문명 | text | 1쪽 [608, 165, 755, 178] | 늘 | 템플릿 | generate.py | look/template.html.j2:18 · fields.json:180 | 묻기 |
| `customer.rrn` ← `remitter.rrn` | 실명번호 | rrn | 1쪽 [206, 194, 314, 207] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:190 | 묻기 |
| `customer.phone` ← `remitter.phone` | 전화번호 | phone | 1쪽 [608, 194, 704, 207] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:185 | 묻기 |
| `customer.address` ← `remitter.address` | 송금인주소 | text | 1쪽 [206, 224, 748, 236] | 늘 | 템플릿 | generate.py | look/template.html.j2:20 · fields.json:165 | 묻기 |
| `customer.company` ← `remitter.company` | 상호(사업자번호) | text | 1쪽 [206, 253, 373, 265] | 11/16 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:170 | 묻기 |
| `foreign.name` ← `beneficiary.name` | 수취인성명 | text | 1쪽 [206, 308, 387, 320] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:105 | 묻기 |
| `foreign.address` ← `beneficiary.address` | 수취인주소 | text | 1쪽 [206, 337, 538, 349] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:85 | 묻기 |
| `beneficiary.country` | 수취인국가 | text | 1쪽 [206, 366, 254, 379] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:100 | 묻기 |
| `beneficiary.relationship` | 신청인과의관계 | text | 1쪽 [650, 366, 697, 379] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:110 | 묻기 |
| `foreign.swift` ← `beneficiary.swift` | SWIFTBIC | text | 1쪽 [206, 421, 283, 433] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:115 | 묻기 |
| `beneficiary.bank_name` | 수취은행명 | text | 1쪽 [206, 450, 292, 463] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:95 | 묻기 |
| `beneficiary.bank_address` | 수취은행주소 | text | 1쪽 [206, 479, 543, 492] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:90 | 묻기 |
| `beneficiary.account_no` | 수취인계좌번호 | account_no | 1쪽 [206, 509, 316, 521] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:80 | 묻기 |
| `remittance.currency` | 송금통화 | text | 1쪽 [206, 562, 248, 577] | 늘 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:135 | 묻기 |
| `remittance.amount` | 송금금액 | amount | 1쪽 [596, 562, 680, 577] | 늘 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:125 | 묻기 |
| `remittance.purpose_code` | 지급사유코드 | number | 1쪽 [265, 603, 304, 615] | 12/16 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:160 | 묻기 |
| `remittance.message` | 송금메시지 | text | 1쪽 [206, 656, 411, 669] | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:145 | 묻기 |
| `remittance.documents` | 지급증빙서류 | text | 1쪽 [206, 686, 317, 698] | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:140 | 묻기 |
| `date` | 신청일 | date | 1쪽 [538, 784, 656, 797] | 늘 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:120 | 묻기 |
| `signature` | 신청인 | text | 1쪽 [755, 784, 818, 797] | 늘 | 템플릿 | generate.py | look/template.html.j2:70 · fields.json:225 | 묻기 |
| `bank_use.ref_no` | 참조번호 | text | 1쪽 [216, 848, 325, 860] | 늘 | 템플릿 | generate.py | look/template.html.j2:79 · fields.json:65 | 묻기 |
| `bank_use.branch` | 취급영업점 | text | 1쪽 [532, 848, 595, 860] | 늘 | 템플릿 | generate.py | look/template.html.j2:79 · fields.json:30 | 묻기 |
| `bank_use.rate` | 적용환율 | number | 1쪽 [216, 867, 271, 880] | 늘 | 템플릿 | generate.py | look/template.html.j2:80 · fields.json:60 | 묻기 |
| `bank_use.krw_amount` | 원화환산액 | amount | 1쪽 [573, 867, 659, 880] | 늘 | 템플릿 | generate.py | look/template.html.j2:80 · fields.json:50 | 묻기 |
| `bank_use.fee` | 송금수수료 | amount | 1쪽 [315, 887, 374, 899] | 늘 | 템플릿 | generate.py | look/template.html.j2:81 · fields.json:45 | 묻기 |
| `bank_use.cable_fee` | 전신료 | amount | 1쪽 [608, 887, 659, 899] | 늘 | 템플릿 | generate.py | look/template.html.j2:81 · fields.json:35 | 묻기 |
| `bank_use.total` | 합계 | amount | 1쪽 [573, 906, 659, 919] | 늘 | 템플릿 | generate.py | look/template.html.j2:82 · fields.json:70 | 묻기 |
| `bank_use.clerk` | 담당자 | text | 1쪽 [787, 895, 825, 907] | 늘 | 템플릿 | generate.py | look/template.html.j2:84 · fields.json:40 | 묻기 |
| `bank_use.manager` | 결재권자 | text | 1쪽 [870, 895, 909, 907] | 늘 | 템플릿 | generate.py | look/template.html.j2:84 · fields.json:55 | 묻기 |
| `batch_count` | 송금건수 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:75 | 묻기 |
| `batch.*.beneficiary` | 수취인 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:250 | 묻기 |
| `batch.*.message` | 송금메시지 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:265 | 묻기 |
| `batch.*.country` | 국가 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:255 | 묻기 |
| `batch.*.bank` | 수취은행 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:245 | 묻기 |
| `batch.*.account_no` | 계좌번호 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:235 | 묻기 |
| `batch.*.currency` | 통화 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:260 | 묻기 |
| `batch.*.amount` | 금액 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:240 | 묻기 |
| `agent.name` | 대리인성명 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:5 | 묻기 |
| `agent.relation` | 신청인과의관계 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:15 | 묻기 |
| `agent.rrn` | 대리인실명번호 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:20 | 묻기 |
| `agent.phone` | 대리인연락처 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:10 | 묻기 |

## 체크·도장·서명 (marks) — 9칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `remittance.purpose` | 송금사유 | checkbox (수입대금 / 유학생경비 / 해외체재비 / 증여성송금 / 해외이주비 / 국내보수송금 / 기타) | 1쪽 [220, 588, 282, 600] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:155 | 묻기 |
| `remittance.charge` | 수수료부담 | checkbox (OUR / SHA / BEN) | 1쪽 [276, 627, 308, 640] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:130 | 묻기 |
| `remittance.method` | 송금방법 | checkbox (전신송금(T/T) / 송금수표(D/D)) | 1쪽 [610, 627, 707, 640] | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:150 | 묻기 |
| `seal.customer` ← `seal.applicant` | 신청인 | seal | 1쪽 [867, 771, 924, 811] | 늘 | 템플릿 | generate.py | fields.json:200 | 묻기 |
| `sign.customer` ← `sign.applicant` | 신청인 | signature | 1쪽 [847, 783, 944, 798] | 늘 | 템플릿 | generate.py | fields.json:220 | 묻기 |
| `seal.staff.clerk` | 담당자 | seal | 1쪽 [779, 882, 833, 921] | 늘 | 템플릿 | generate.py | fields.json:205 | 묻기 |
| `seal.staff.manager` | 결재권자 | seal | 1쪽 [862, 882, 917, 921] | 늘 | 템플릿 | generate.py | fields.json:210 | 묻기 |
| `seal.agent` | 대리인 | 도장 | - | 1/16 | 템플릿 | generate.py | fields.json:195 | 묻기 |
| `sign.agent` | 대리인 | 서명 | - | 1/16 | 템플릿 | generate.py | fields.json:215 | 묻기 |

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
"해외송금신청서"
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
 "NAMGOONG YETAE",
 "850328-2******",
 "010-6144-1173",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "새한커피 (133-64-53148)",
 "Tokyo Seimitsu Kogyo K.K.",
 "2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 163-0001",
 "JAPAN",
 "거래처",
 "MHCBJPJT",
 "Mizuho Bank",
 "1-5-5 Otemachi, Chiyoda-ku, Tokyo 100-8176, Japan",
 "28395786990418",
 "USD",
 "28,175.95",
 "10101",
 "INVOICE NO. TOK-2025-0487",
 "Proforma Invoice",
 "2025년 04월 01일",
 "OR25040140089",
 "센텀지점",
 "1,468.93",
 "41,388,498원",
 "20,000원",
 "8,000원",
 "41,416,498원",
 "엄민성",
 "조도예"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"850328-2******"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"28395786990418"
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
- bank.name: 은행명
- customer.name: 송금인성명 (고객 성명)
- customer.name_en: 송금인영문명 (고객 영문 성명)
- customer.rrn: 실명번호 (고객 주민등록번호)
- customer.phone: 전화번호 (고객 연락처)
- customer.address: 송금인주소 (고객 주소)
- customer.company: 상호(사업자번호) (고객 직장명)
- foreign.name: 수취인성명 (외국 상대 이름)
- foreign.address: 수취인주소 (외국 상대 주소)
- beneficiary.country: 수취인국가
- beneficiary.relationship: 신청인과의관계
- foreign.swift: SWIFTBIC (외국 거래 상대 은행 SWIFT(BIC) 코드)
- beneficiary.bank_name: 수취은행명
- beneficiary.bank_address: 수취은행주소
- beneficiary.account_no: 수취인계좌번호
- remittance.currency: 송금통화
- remittance.amount: 송금금액
- remittance.purpose_code: 지급사유코드
- remittance.message: 송금메시지
- remittance.documents: 지급증빙서류
- date: 신청일
- signature: 신청인
- bank_use.ref_no: 참조번호
- bank_use.branch: 취급영업점
- bank_use.rate: 적용환율
- bank_use.krw_amount: 원화환산액
- bank_use.fee: 송금수수료
- bank_use.cable_fee: 전신료
- bank_use.total: 합계
- bank_use.clerk: 담당자
- bank_use.manager: 결재권자
```

답:

```json
[{"key": "bank.name", "value": "국민은행", "bbox_2d": [83, 38, 182, 57], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [206, 165, 269, 178], "page": 1},
 {"key": "customer.name_en", "value": "NAMGOONG YETAE", "bbox_2d": [608, 165, 755, 178], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [206, 194, 314, 207], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [608, 194, 704, 207], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [206, 224, 748, 236], "page": 1},
 {"key": "customer.company", "value": "새한커피 (133-64-53148)", "bbox_2d": [206, 253, 373, 265], "page": 1},
 {"key": "foreign.name", "value": "Tokyo Seimitsu Kogyo K.K.", "bbox_2d": [206, 308, 387, 320], "page": 1},
 {"key": "foreign.address", "value": "2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 163-0001", "bbox_2d": [206, 337, 538, 349], "page": 1},
 {"key": "beneficiary.country", "value": "JAPAN", "bbox_2d": [206, 366, 254, 379], "page": 1},
 {"key": "beneficiary.relationship", "value": "거래처", "bbox_2d": [650, 366, 697, 379], "page": 1},
 {"key": "foreign.swift", "value": "MHCBJPJT", "bbox_2d": [206, 421, 283, 433], "page": 1},
 {"key": "beneficiary.bank_name", "value": "Mizuho Bank", "bbox_2d": [206, 450, 292, 463], "page": 1},
 {"key": "beneficiary.bank_address", "value": "1-5-5 Otemachi, Chiyoda-ku, Tokyo 100-8176, Japan", "bbox_2d": [206, 479, 543, 492], "page": 1},
 {"key": "beneficiary.account_no", "value": "28395786990418", "bbox_2d": [206, 509, 316, 521], "page": 1},
 {"key": "remittance.currency", "value": "USD", "bbox_2d": [206, 562, 248, 577], "page": 1},
 {"key": "remittance.amount", "value": "28,175.95", "bbox_2d": [596, 562, 680, 577], "page": 1},
 {"key": "remittance.purpose_code", "value": "10101", "bbox_2d": [265, 603, 304, 615], "page": 1},
 {"key": "remittance.message", "value": "INVOICE NO. TOK-2025-0487", "bbox_2d": [206, 656, 411, 669], "page": 1},
 {"key": "remittance.documents", "value": "Proforma Invoice", "bbox_2d": [206, 686, 317, 698], "page": 1},
 {"key": "date", "value": "2025년 04월 01일", "bbox_2d": [538, 784, 656, 797], "page": 1},
 {"key": "signature", "value": "남궁예태", "bbox_2d": [755, 784, 818, 797], "page": 1},
 {"key": "bank_use.ref_no", "value": "OR25040140089", "bbox_2d": [216, 848, 325, 860], "page": 1},
 {"key": "bank_use.branch", "value": "센텀지점", "bbox_2d": [532, 848, 595, 860], "page": 1},
 {"key": "bank_use.rate", "value": "1,468.93", "bbox_2d": [216, 867, 271, 880], "page": 1},
 {"key": "bank_use.krw_amount", "value": "41,388,498원", "bbox_2d": [573, 867, 659, 880], "page": 1},
 {"key": "bank_use.fee", "value": "20,000원", "bbox_2d": [315, 887, 374, 899], "page": 1},
 {"key": "bank_use.cable_fee", "value": "8,000원", "bbox_2d": [608, 887, 659, 899], "page": 1},
 {"key": "bank_use.total", "value": "41,416,498원", "bbox_2d": [573, 906, 659, 919], "page": 1},
 {"key": "bank_use.clerk", "value": "엄민성", "bbox_2d": [787, 895, 825, 907], "page": 1},
 {"key": "bank_use.manager", "value": "조도예", "bbox_2d": [870, 895, 909, 907], "page": 1}]
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
- remittance.purpose: 송금사유 (체크박스, 보기: 수입대금 / 유학생경비 / 해외체재비 / 증여성송금 / 해외이주비 / 국내보수송금 / 기타)
- remittance.charge: 수수료부담 (체크박스, 보기: OUR / SHA / BEN)
- remittance.method: 송금방법 (체크박스, 보기: 전신송금(T/T) / 송금수표(D/D))
- seal.customer: 신청인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 신청인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.clerk: 담당자 (도장)
- seal.staff.manager: 결재권자 (도장)
```

답:

```json
[{"key": "remittance.purpose", "value": "수입대금", "bbox_2d": [206, 588, 216, 600], "page": 1},
 {"key": "remittance.charge", "value": "SHA", "bbox_2d": [263, 627, 272, 640], "page": 1},
 {"key": "remittance.method", "value": "전신송금(T/T)", "bbox_2d": [596, 627, 606, 640], "page": 1},
 {"key": "seal.customer", "value": true, "bbox_2d": [867, 771, 924, 811], "page": 1},
 {"key": "sign.customer", "value": false},
 {"key": "seal.staff.clerk", "value": true, "bbox_2d": [779, 882, 833, 921], "page": 1},
 {"key": "seal.staff.manager", "value": true, "bbox_2d": [862, 882, 917, 921], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check overseas_remittance_application` → `python -m docgen.formdir card overseas_remittance_application` (실제 질문→답 확인).

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
| 답 모양 | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions overseas_remittance_application --show` · `python -m docgen.preview overseas_remittance_application --out work/overseas_remittance_application`
