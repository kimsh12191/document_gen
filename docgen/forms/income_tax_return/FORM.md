# 종합소득세 과세표준확정신고 및 납부계산서 (`income_tax_return`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card income_tax_return · card-hash: d4ece7466638 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** tax · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 종합소득세 과세표준확정신고 및 납부계산서 (다른 이름: 종합소득세 과세표준확정신고 및 납부계산서(일반))
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 종합소득세 확정신고서. 제1쪽(기본사항 + 환급금 계좌 + 세액의 계산)은 항상, 명세(제2·3쪽)는 소득이 여럿이거나

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/business.py`, `docgen/docs/tax.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 62칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `tax_year` | 귀속연도 | number | 1쪽 [387, 90, 422, 103] | 늘 | generate.py | look/template.html.j2:50 | 묻기 |
| `customer.name` ← `taxpayer.name` | 성명 | text | 1쪽 [255, 178, 313, 189] | 늘 | generate.py | look/template.html.j2:43 | 묻기 |
| `customer.rrn` ← `taxpayer.rrn` | 주민등록번호 | rrn | 1쪽 [666, 178, 765, 189] | 늘 | generate.py | look/template.html.j2:62 | 묻기 |
| `customer.address` ← `taxpayer.address` | 주소 | text | 1쪽 [255, 199, 754, 209] | 늘 | generate.py | look/template.html.j2:63 | 묻기 |
| `customer.email` ← `taxpayer.email` | 전자우편주소 | text | 1쪽 [255, 219, 382, 229] | 늘 | generate.py | look/template.html.j2:64 | 묻기 |
| `taxpayer.biz_phone` | 사업장전화번호 | phone | 1쪽 [255, 239, 337, 249] | 늘 | generate.py | look/template.html.j2:65 | 묻기 |
| `customer.mobile` ← `taxpayer.mobile` | 휴대전화번호 | phone | 1쪽 [666, 239, 754, 249] | 늘 | generate.py | look/template.html.j2:65 | 묻기 |
| `filing_type` | 신고유형 | text | 1쪽 [394, 260, 454, 272] | 늘 | generate.py | look/template.html.j2:66 | 묻기 |
| `bookkeeping` | 기장의무 | text | 1쪽 [285, 298, 391, 310] | 늘 | generate.py | look/template.html.j2:67 | 묻기 |
| `filing_kind` | 신고구분 | text | 1쪽 [292, 320, 352, 333] | 늘 | generate.py | look/template.html.j2:68 | 묻기 |
| `refund_account.bank` | 금융기관/체신관서명 | text | 1쪽 [255, 371, 313, 382] | 11/16 | generate.py | look/template.html.j2:73 | 묻기 |
| `refund_account.number` | 계좌번호 | text | 1쪽 [666, 371, 777, 382] | 11/16 | generate.py | look/template.html.j2:74 | 묻기 |
| `national.total_income` | 종합소득금액 | amount | 1쪽 [656, 438, 721, 449] | 늘 | generate.py | look/template.html.j2:138 | 묻기 |
| `national.deduction` | 소득공제 | amount | 1쪽 [663, 455, 721, 465] | 늘 | generate.py | look/template.html.j2:166 | 묻기 |
| `national.base` | 과세표준 | amount | 1쪽 [656, 471, 721, 482] | 늘 | generate.py | - | 묻기 |
| `national.rate` | 세율 | percent | 1쪽 [694, 488, 721, 498] | 늘 | generate.py | - | 묻기 |
| `national.computed` | 산출세액 | number | 1쪽 [663, 504, 721, 515] | 늘 | generate.py | - | 묻기 |
| `national.reduction` | 세액감면 | number | 1쪽 [714, 521, 721, 531] | 늘 | generate.py | - | 묻기 |
| `national.credit` | 세액공제 | amount | 1쪽 [681, 537, 721, 548] | 늘 | generate.py | look/template.html.j2:174 | 묻기 |
| `national.determined` | 결정세액 | number | 1쪽 [663, 554, 721, 564] | 늘 | generate.py | - | 묻기 |
| `national.penalty` | 가산세 | number | 1쪽 [714, 570, 721, 581] | 늘 | generate.py | look/template.html.j2:182 | 묻기 |
| `national.additional` | 추가납부세액 | number | 1쪽 [714, 587, 721, 597] | 늘 | generate.py | - | 묻기 |
| `national.total` | 합계 | amount | 1쪽 [663, 603, 721, 614] | 늘 | generate.py | - | 묻기 |
| `national.prepaid` | 기납부세액 | number | 1쪽 [663, 620, 721, 630] | 늘 | generate.py | look/template.html.j2:191 | 묻기 |
| `national.payable` | 납부(환급)할총세액 | amount | 1쪽 [663, 636, 721, 647] | 늘 | generate.py | - | 묻기 |
| `national.special_deduct` | 납부특례세액차감 | number | 1쪽 [714, 653, 721, 663] | 늘 | generate.py | - | 묻기 |
| `national.special_add` | 납부특례세액가산 | number | 1쪽 [714, 669, 721, 680] | 늘 | generate.py | - | 묻기 |
| `national.installment` | 분납할세액 | number | 1쪽 [714, 685, 721, 696] | 늘 | generate.py | - | 묻기 |
| `national.due_payable` | 신고기한이내납부할세액 | amount | 1쪽 [663, 702, 721, 713] | 늘 | generate.py | - | 묻기 |
| `filed_date` | 신고일 | date | 1쪽 [802, 754, 911, 764] | 늘 | generate.py | look/template.html.j2:45 | 묻기 |
| `related.name` ← `tax_agent.name` | 세무대리인 | text | 1쪽 [771, 801, 814, 812] | 11/16 | generate.py | look/template.html.j2:108 | 묻기 |
| `tax_agent.biz_no` | 세무대리인사업자등록번호 | biz_no | 1쪽 [297, 823, 383, 836] | 11/16 | generate.py | look/template.html.j2:111 | 묻기 |
| `related.phone` ← `tax_agent.phone` | 세무대리인전화번호 | phone | 1쪽 [684, 823, 770, 836] | 11/16 | generate.py | look/template.html.j2:112 | 묻기 |
| `tax_office` | 세무서장 | text | 1쪽 [89, 846, 203, 861] | 늘 | generate.py | look/template.html.j2:114 | 묻기 |
| `incomes.*.type` | 소득구분 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:134 | 묻기 |
| `incomes.*.payer` | 소득의지급자 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:134 | 묻기 |
| `incomes.*.revenue` | 총수입금액 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:135 | 묻기 |
| `incomes.*.expense` | 필요경비 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:135 | 묻기 |
| `incomes.*.amount` | 소득금액 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:136 | 묻기 |
| `incomes.*.withheld` | 원천징수세액 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:136 | 묻기 |
| `business_income.address` | 사업장소재지 | - | - | 14/16 | generate.py | look/template.html.j2:143 | 묻기 |
| `business_income.trade_name` | 상호 | - | - | 14/16 | generate.py | look/template.html.j2:144 | 묻기 |
| `business_income.biz_no` | 사업자등록번호 | - | - | 14/16 | generate.py | look/template.html.j2:144 | 묻기 |
| `business_income.code` | 업종코드 | - | - | 14/16 | generate.py | look/template.html.j2:145 | 묻기 |
| `business_income.revenue` | 총수입금액 | - | - | 14/16 | generate.py | look/template.html.j2:145 | 묻기 |
| `business_income.expense` | 필요경비 | - | - | 14/16 | generate.py | look/template.html.j2:146 | 묻기 |
| `business_income.income` | 소득금액 | - | - | 14/16 | generate.py | look/template.html.j2:146 | 묻기 |
| `dependents.*.relation` | 관계 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:156 | 묻기 |
| `dependents.*.name` | 성명 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:156 | 묻기 |
| `dependents.*.rrn` | 주민등록번호 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:157 | 묻기 |
| `dependents.*.basic` | 기본공제 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:157 | 묻기 |
| `dependents.*.extra` | 추가공제 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:158 | 묻기 |
| `deduction_items.*.item` | 소득공제항목 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:125 | 묻기 |
| `deduction_items.*.amount` | 금액 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:125 | 묻기 |
| `credit_items.*.item` | 세액공제항목 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:125 | 묻기 |
| `credit_items.*.amount` | 금액 | - | - (1행) | 14/16 | generate.py | look/template.html.j2:125 | 묻기 |
| `prepaid_items.*.item` | 기납부세액항목 | - | - (1행) | 13/16 | generate.py | look/template.html.j2:125 | 묻기 |
| `prepaid_items.*.amount` | 금액 | - | - (1행) | 13/16 | generate.py | look/template.html.j2:125 | 묻기 |
| `business_income.partner` | 공동사업자 | - | - | 1/16 | generate.py | look/template.html.j2:148 | 묻기 |
| `business_income.share` | 손익분배비율 | - | - | 1/16 | generate.py | look/template.html.j2:148 | 묻기 |
| `penalty_items.*.item` | 가산세항목 | - | - (1행) | 1/16 | generate.py | look/template.html.j2:125 | 묻기 |
| `penalty_items.*.amount` | 금액 | - | - (1행) | 1/16 | generate.py | look/template.html.j2:125 | 묻기 |

## 체크·도장·서명 (marks) — 6칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `residency` | 거주구분 | checkbox (거주자 / 비거주자) | 1쪽 [742, 89, 785, 99] | 늘 | generate.py | look/template.html.j2:54 | 묻기 |
| `customer.nationality` ← `nationality` | 내ㆍ외국인 | checkbox (내국인 / 외국인) | 1쪽 [742, 111, 785, 122] | 늘 | generate.py | look/template.html.j2:55 | 묻기 |
| `seal.customer` ← `seal.taxpayer` | 신고인 | seal | 1쪽 [821, 767, 911, 781] | 늘 | generate.py | - | 묻기 |
| `sign.customer` ← `sign.taxpayer` | 신고인 | signature | 1쪽 [821, 767, 911, 781] | 늘 | generate.py | - | 묻기 |
| `seal.related` ← `seal.tax_agent` | 세무대리인 | seal | 1쪽 [821, 800, 911, 814] | 11/16 | generate.py | - | 묻기 |
| `sign.related` ← `sign.tax_agent` | 세무대리인 | signature | 1쪽 [821, 800, 911, 814] | 11/16 | generate.py | - | 묻기 |

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
"종합소득세 과세표준확정신고 및 납부계산서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2023",
 "남궁예태",
 "850328-2******",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "yetae741@gmail.com",
 "051-410-9614",
 "010-6144-1173",
 "외부조정",
 "복식부기의무자",
 "정기신고",
 "국민은행",
 "478303-40-826627",
 "65,565,359",
 "7,400,880",
 "58,164,479",
 "24%",
 "8,199,474",
 "0",
 "90,000",
 "8,109,474",
 "2,988,710",
 "5,120,760",
 "2024년 05월 30일",
 "기혁찬",
 "843-44-26624",
 "051-458-0003",
 "반포세무서장"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"90,000"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"0"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- tax_year: 귀속연도
- customer.name: 성명 (고객 성명)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- customer.address: 주소 (고객 주소)
- customer.email: 전자우편주소 (고객 이메일)
- taxpayer.biz_phone: 사업장전화번호
- customer.mobile: 휴대전화번호 (고객 휴대전화)
- filing_type: 신고유형
- bookkeeping: 기장의무
- filing_kind: 신고구분
- refund_account.bank: 금융기관/체신관서명
- refund_account.number: 계좌번호
- national.total_income: 종합소득금액
- national.deduction: 소득공제
- national.base: 과세표준
- national.rate: 세율
- national.computed: 산출세액
- national.reduction: 세액감면
- national.credit: 세액공제
- national.determined: 결정세액
- national.penalty: 가산세
- national.additional: 추가납부세액
- national.total: 합계
- national.prepaid: 기납부세액
- national.payable: 납부(환급)할총세액
- national.special_deduct: 납부특례세액차감
- national.special_add: 납부특례세액가산
- national.installment: 분납할세액
- national.due_payable: 신고기한이내납부할세액
- filed_date: 신고일
- related.name: 세무대리인 (보증인·공동 성명)
- tax_agent.biz_no: 세무대리인사업자등록번호
- related.phone: 세무대리인전화번호 (보증인·공동 연락처)
- tax_office: 세무서장
```

답:

```json
[{"key": "tax_year", "value": "2023", "bbox_2d": [387, 90, 422, 103], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [255, 178, 313, 189], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [666, 178, 765, 189], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [255, 199, 754, 209], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [255, 219, 382, 229], "page": 1},
 {"key": "taxpayer.biz_phone", "value": "051-410-9614", "bbox_2d": [255, 239, 337, 249], "page": 1},
 {"key": "customer.mobile", "value": "010-6144-1173", "bbox_2d": [666, 239, 754, 249], "page": 1},
 {"key": "filing_type", "value": "외부조정", "bbox_2d": [394, 260, 454, 272], "page": 1},
 {"key": "bookkeeping", "value": "복식부기의무자", "bbox_2d": [285, 298, 391, 310], "page": 1},
 {"key": "filing_kind", "value": "정기신고", "bbox_2d": [292, 320, 352, 333], "page": 1},
 {"key": "refund_account.bank", "value": "국민은행", "bbox_2d": [255, 371, 313, 382], "page": 1},
 {"key": "refund_account.number", "value": "478303-40-826627", "bbox_2d": [666, 371, 777, 382], "page": 1},
 {"key": "national.total_income", "value": "65,565,359", "bbox_2d": [656, 438, 721, 449], "page": 1},
 {"key": "national.deduction", "value": "7,400,880", "bbox_2d": [663, 455, 721, 465], "page": 1},
 {"key": "national.base", "value": "58,164,479", "bbox_2d": [656, 471, 721, 482], "page": 1},
 {"key": "national.rate", "value": "24%", "bbox_2d": [694, 488, 721, 498], "page": 1},
 {"key": "national.computed", "value": "8,199,474", "bbox_2d": [663, 504, 721, 515], "page": 1},
 {"key": "national.reduction", "value": "0", "bbox_2d": [714, 521, 721, 531], "page": 1},
 {"key": "national.credit", "value": "90,000", "bbox_2d": [681, 537, 721, 548], "page": 1},
 {"key": "national.determined", "value": "8,109,474", "bbox_2d": [663, 554, 721, 564], "page": 1},
 {"key": "national.penalty", "value": "0", "bbox_2d": [714, 570, 721, 581], "page": 1},
 {"key": "national.additional", "value": "0", "bbox_2d": [714, 587, 721, 597], "page": 1},
 {"key": "national.total", "value": "8,109,474", "bbox_2d": [663, 603, 721, 614], "page": 1},
 {"key": "national.prepaid", "value": "2,988,710", "bbox_2d": [663, 620, 721, 630], "page": 1},
 {"key": "national.payable", "value": "5,120,760", "bbox_2d": [663, 636, 721, 647], "page": 1},
 {"key": "national.special_deduct", "value": "0", "bbox_2d": [714, 653, 721, 663], "page": 1},
 {"key": "national.special_add", "value": "0", "bbox_2d": [714, 669, 721, 680], "page": 1},
 {"key": "national.installment", "value": "0", "bbox_2d": [714, 685, 721, 696], "page": 1},
 {"key": "national.due_payable", "value": "5,120,760", "bbox_2d": [663, 702, 721, 713], "page": 1},
 {"key": "filed_date", "value": "2024년 05월 30일", "bbox_2d": [802, 754, 911, 764], "page": 1},
 {"key": "related.name", "value": "기혁찬", "bbox_2d": [771, 801, 814, 812], "page": 1},
 {"key": "tax_agent.biz_no", "value": "843-44-26624", "bbox_2d": [297, 823, 383, 836], "page": 1},
 {"key": "related.phone", "value": "051-458-0003", "bbox_2d": [684, 823, 770, 836], "page": 1},
 {"key": "tax_office", "value": "반포세무서장", "bbox_2d": [89, 846, 203, 861], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- residency: 거주구분 (체크박스, 보기: 거주자 / 비거주자)
- customer.nationality: 내ㆍ외국인 (고객 국적, 체크박스, 보기: 내국인 / 외국인)
- seal.customer: 신고인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 신고인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.related: 세무대리인 (보증인·공동 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.related: 세무대리인 (보증인·공동 서명, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "residency", "value": "거주자", "bbox_2d": [720, 89, 738, 99], "page": 1},
 {"key": "customer.nationality", "value": "내국인", "bbox_2d": [720, 111, 738, 122], "page": 1},
 {"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": false},
 {"key": "seal.related", "value": false},
 {"key": "sign.related", "value": false}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions income_tax_return --show` · `python -m docgen.preview income_tax_return --out work/income_tax_return`
