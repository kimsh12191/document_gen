# 종합소득세 과세표준확정신고 및 납부계산서 (`income_tax_return`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card income_tax_return · card-hash: 0643fb0b04eb -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** tax · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 종합소득세 과세표준확정신고 및 납부계산서 (다른 이름: 종합소득세 과세표준확정신고 및 납부계산서(일반))
- **질문·답:** 이 폴더의 `questions.json` 에서 바꾼 것이 있음 (아래 ← 바꿈)
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa income_tax_return --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 종합소득세 확정신고서. 제1쪽(기본사항 + 환급금 계좌 + 세액의 계산)은 항상, 명세(제2·3쪽)는 소득이 여럿이거나

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `questions.json` | 기본 과제의 질문 문장·답 틀 (기본과 다른 것만) |
| `docgen/docs/business.py`, `docgen/docs/tax.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 43칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `tax_year` | 귀속연도 | number | 1쪽 [387, 90, 422, 103] | 늘 | 템플릿 | generate.py | look/template.html.j2:50 · fields.json:215 | 묻기 |
| `taxpayer.name` | 성명 | text | 1쪽 [255, 178, 313, 189] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:240 | 묻기 |
| `taxpayer.rrn` | 주민등록번호 | rrn | 1쪽 [666, 178, 765, 189] | 늘 | 템플릿 | generate.py | look/template.html.j2:62 · fields.json:245 | 묻기 |
| `taxpayer.address` | 주소 | text | 1쪽 [255, 199, 754, 209] | 늘 | 템플릿 | generate.py | look/template.html.j2:63 · fields.json:220 | 묻기 |
| `taxpayer.email` | 전자우편주소 | text | 1쪽 [255, 219, 382, 229] | 늘 | 템플릿 | generate.py | look/template.html.j2:64 · fields.json:230 | 묻기 |
| `taxpayer.biz_phone` | 사업장전화번호 | phone | 1쪽 [255, 239, 337, 249] | 늘 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:225 | 묻기 |
| `taxpayer.mobile` | 휴대전화번호 | phone | 1쪽 [666, 239, 754, 249] | 늘 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:235 | 묻기 |
| `filing_type` | 신고유형 | text | 1쪽 [394, 260, 454, 272] | 늘 | 템플릿 | generate.py | look/template.html.j2:66 · fields.json:65 | 묻기 |
| `bookkeeping` | 기장의무 | text | 1쪽 [285, 298, 391, 310] | 늘 | 템플릿 | generate.py | look/template.html.j2:67 · fields.json:5 | 묻기 |
| `filing_kind` | 신고구분 | text | 1쪽 [292, 320, 352, 333] | 늘 | 템플릿 | generate.py | look/template.html.j2:68 · fields.json:60 | 묻기 |
| `refund_account.bank` | 금융기관/체신관서명 | text | 1쪽 [255, 371, 313, 382] | 11/16 | 템플릿 | generate.py | look/template.html.j2:73 · fields.json:160 | 묻기 |
| `refund_account.number` | 계좌번호 | text | 1쪽 [666, 371, 777, 382] | 11/16 | 템플릿 | generate.py | look/template.html.j2:74 · fields.json:165 | 묻기 |
| `national.total_income` | 종합소득금액 | amount | 1쪽 [656, 438, 721, 449] | 늘 | 템플릿 | generate.py | look/template.html.j2:138 · fields.json:150 | 묻기 |
| `national.deduction` | 소득공제 | amount | 1쪽 [663, 455, 721, 465] | 늘 | 템플릿 | generate.py | look/template.html.j2:166 · fields.json:90 | 묻기 |
| `national.base` | 과세표준 | amount | 1쪽 [656, 471, 721, 482] | 늘 | 템플릿 | generate.py | fields.json:75 | 묻기 |
| `national.rate` | 세율 | percent | 1쪽 [694, 488, 721, 498] | 늘 | 템플릿 | generate.py | fields.json:125 | 묻기 |
| `national.computed` | 산출세액 | number | 1쪽 [663, 504, 721, 515] | 늘 | 템플릿 | generate.py | fields.json:80 | 묻기 |
| `national.reduction` | 세액감면 | number | 1쪽 [714, 521, 721, 531] | 늘 | 템플릿 | generate.py | fields.json:130 | 묻기 |
| `national.credit` | 세액공제 | amount | 1쪽 [681, 537, 721, 548] | 늘 | 템플릿 | generate.py | look/template.html.j2:174 · fields.json:85 | 묻기 |
| `national.determined` | 결정세액 | number | 1쪽 [663, 554, 721, 564] | 늘 | 템플릿 | generate.py | fields.json:95 | 묻기 |
| `national.penalty` | 가산세 | number | 1쪽 [714, 570, 721, 581] | 늘 | 템플릿 | generate.py | look/template.html.j2:182 · fields.json:115 | 묻기 |
| `national.additional` | 추가납부세액 | number | 1쪽 [714, 587, 721, 597] | 늘 | 템플릿 | generate.py | fields.json:70 | 묻기 |
| `national.total` | 합계 | amount | 1쪽 [663, 603, 721, 614] | 늘 | 템플릿 | generate.py | fields.json:145 | 묻기 |
| `national.prepaid` | 기납부세액 | number | 1쪽 [663, 620, 721, 630] | 늘 | 템플릿 | generate.py | look/template.html.j2:191 · fields.json:120 | 묻기 |
| `national.payable` | 납부(환급)할총세액 | amount | 1쪽 [663, 636, 721, 647] | 늘 | 템플릿 | generate.py | fields.json:110 | 묻기 |
| `national.special_deduct` | 납부특례세액차감 | number | 1쪽 [714, 653, 721, 663] | 늘 | 템플릿 | generate.py | fields.json:140 | 묻기 |
| `national.special_add` | 납부특례세액가산 | number | 1쪽 [714, 669, 721, 680] | 늘 | 템플릿 | generate.py | fields.json:135 | 묻기 |
| `national.installment` | 분납할세액 | number | 1쪽 [714, 685, 721, 696] | 늘 | 템플릿 | generate.py | fields.json:105 | 묻기 |
| `national.due_payable` | 신고기한이내납부할세액 | amount | 1쪽 [663, 702, 721, 713] | 늘 | 템플릿 | generate.py | fields.json:100 | 묻기 |
| `filed_date` | 신고일 | date | 1쪽 [802, 754, 911, 764] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:55 | 묻기 |
| `tax_agent.name` | 세무대리인 | text | 1쪽 [771, 801, 814, 812] | 11/16 | 템플릿 | generate.py | look/template.html.j2:108 · fields.json:200 | 묻기 |
| `tax_agent.biz_no` | 세무대리인사업자등록번호 | biz_no | 1쪽 [297, 823, 383, 836] | 11/16 | 템플릿 | generate.py | look/template.html.j2:111 · fields.json:195 | 묻기 |
| `tax_agent.phone` | 세무대리인전화번호 | phone | 1쪽 [684, 823, 770, 836] | 11/16 | 템플릿 | generate.py | look/template.html.j2:112 · fields.json:205 | 묻기 |
| `tax_office` | 세무서장 | text | 1쪽 [89, 846, 203, 861] | 늘 | 템플릿 | generate.py | look/template.html.j2:114 · fields.json:210 | 묻기 |
| `business_income.address` | 사업장소재지 | - | - | 14/16 | 템플릿 | generate.py | look/template.html.j2:143 · fields.json:10 | 묻기 |
| `business_income.trade_name` | 상호 | - | - | 14/16 | 템플릿 | generate.py | look/template.html.j2:144 · fields.json:50 | 묻기 |
| `business_income.biz_no` | 사업자등록번호 | - | - | 14/16 | 템플릿 | generate.py | look/template.html.j2:144 · fields.json:15 | 묻기 |
| `business_income.code` | 업종코드 | - | - | 14/16 | 템플릿 | generate.py | look/template.html.j2:145 · fields.json:20 | 묻기 |
| `business_income.revenue` | 총수입금액 | - | - | 14/16 | 템플릿 | generate.py | look/template.html.j2:145 · fields.json:40 | 묻기 |
| `business_income.expense` | 필요경비 | - | - | 14/16 | 템플릿 | generate.py | look/template.html.j2:146 · fields.json:25 | 묻기 |
| `business_income.income` | 소득금액 | - | - | 14/16 | 템플릿 | generate.py | look/template.html.j2:146 · fields.json:30 | 묻기 |
| `business_income.partner` | 공동사업자 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:148 · fields.json:35 | 묻기 |
| `business_income.share` | 손익분배비율 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:148 · fields.json:45 | 묻기 |

## 표 `incomes` (표 과제 table·table_read·table_find·table_qa) — 6열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `incomes.*.type` | 소득구분 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:134 · fields.json:317 | 묻기 |
| `incomes.*.payer` | 소득의지급자 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:134 · fields.json:325 | 묻기 |
| `incomes.*.revenue` | 총수입금액 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:135 · fields.json:330 | 묻기 |
| `incomes.*.expense` | 필요경비 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:135 · fields.json:320 | 묻기 |
| `incomes.*.amount` | 소득금액 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:136 · fields.json:315 | 묻기 |
| `incomes.*.withheld` | 원천징수세액 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:136 · fields.json:340 | 묻기 |

## 표 `dependents` (표 과제 table·table_read·table_find·table_qa) — 5열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `dependents.*.relation` | 관계 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:156 · fields.json:300 | 묻기 |
| `dependents.*.name` | 성명 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:156 · fields.json:295 | 묻기 |
| `dependents.*.rrn` | 주민등록번호 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:157 · fields.json:305 | 묻기 |
| `dependents.*.basic` | 기본공제 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:157 · fields.json:285 | 묻기 |
| `dependents.*.extra` | 추가공제 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:158 · fields.json:290 | 묻기 |

## 표 `deduction_items` (표 과제 table·table_read·table_find·table_qa) — 2열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `deduction_items.*.item` | 소득공제항목 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:125 · fields.json:275 | 묻기 |
| `deduction_items.*.amount` | 금액 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:125 · fields.json:270 | 묻기 |

## 표 `credit_items` (표 과제 table·table_read·table_find·table_qa) — 2열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `credit_items.*.item` | 세액공제항목 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:125 · fields.json:260 | 묻기 |
| `credit_items.*.amount` | 금액 | - | - (1행) | 14/16 | 템플릿 | generate.py | look/template.html.j2:125 · fields.json:255 | 묻기 |

## 표 `prepaid_items` (표 과제 table·table_read·table_find·table_qa) — 2열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `prepaid_items.*.item` | 기납부세액항목 | - | - (1행) | 13/16 | 템플릿 | generate.py | look/template.html.j2:125 · fields.json:370 | 묻기 |
| `prepaid_items.*.amount` | 금액 | - | - (1행) | 13/16 | 템플릿 | generate.py | look/template.html.j2:125 · fields.json:365 | 묻기 |

## 표 `penalty_items` (표 과제 table·table_read·table_find·table_qa) — 2열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `penalty_items.*.item` | 가산세항목 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:125 · fields.json:355 | 묻기 |
| `penalty_items.*.amount` | 금액 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:125 · fields.json:350 | 묻기 |

## 체크·도장·서명 (marks) — 6칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `residency` | 거주구분 | checkbox (거주자 / 비거주자) | 1쪽 [742, 89, 785, 99] | 늘 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:170 | 묻기 |
| `nationality` | 내ㆍ외국인 | checkbox (내국인 / 외국인) | 1쪽 [742, 111, 785, 122] | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:155 | 묻기 |
| `seal.taxpayer` | 신고인 | seal | 1쪽 [821, 767, 911, 781] | 늘 | 템플릿 | generate.py | fields.json:180 | 묻기 |
| `sign.taxpayer` | 신고인 | signature | 1쪽 [821, 767, 911, 781] | 늘 | 템플릿 | generate.py | fields.json:190 | 묻기 |
| `seal.tax_agent` | 세무대리인 | seal | 1쪽 [821, 800, 911, 814] | 11/16 | 템플릿 | generate.py | fields.json:175 | 묻기 |
| `sign.tax_agent` | 세무대리인 | signature | 1쪽 [821, 800, 911, 814] | 11/16 | 템플릿 | generate.py | fields.json:185 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키는·값은:** 어디서 정해지나. 키·값 종류는 이 서식 파일에 적힌 그대로입니다 (모든 서식 공통 키 사전은 없음). "키 설명 그대로" 는 칸에 `"key"` 가 없어 키 설명이 키로 나가는 것. 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
- **고칠 곳:** html·코드 서식은 템플릿 줄(칸 자리·키·항목명)과 fields.json 줄(값 출처·질문 설정 q), 원본 서식은 fields.json 의 그 칸(박스 `rect`·항목명·키·값·q). html·코드 서식에서 fields.json 에 줄이 없는 칸의 질문 설정은 fields.json 맨 위 `"q": {"키": {…}}` 묶음에.

## 질문 → 답 (seed 1000000 로 그린 실제 문항)

질문은 모델에게 가는 글 전부, 답은 데이터의 정답 (그린 문서의 값·위치). 질문 문장·답 꼴은 이 폴더 `questions.json` 과 공통 `docgen/forms/_common/questions.json`.

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
항목 (키: 설명 (몇 번째 행))
- tax_year: 귀속연도
- taxpayer.name: 성명
- taxpayer.rrn: 주민등록번호
- taxpayer.address: 주소
- taxpayer.email: 전자우편주소
- taxpayer.biz_phone: 사업장전화번호
- taxpayer.mobile: 휴대전화번호
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
- tax_agent.name: 세무대리인
- tax_agent.biz_no: 세무대리인사업자등록번호
- tax_agent.phone: 세무대리인전화번호
- tax_office: 세무서장
```

답:

```json
[{"key": "tax_year", "value": "2023", "bbox_2d": [387, 90, 422, 103], "page": 1},
 {"key": "taxpayer.name", "value": "남궁예태", "bbox_2d": [255, 178, 313, 189], "page": 1},
 {"key": "taxpayer.rrn", "value": "850328-2******", "bbox_2d": [666, 178, 765, 189], "page": 1},
 {"key": "taxpayer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [255, 199, 754, 209], "page": 1},
 {"key": "taxpayer.email", "value": "yetae741@gmail.com", "bbox_2d": [255, 219, 382, 229], "page": 1},
 {"key": "taxpayer.biz_phone", "value": "051-410-9614", "bbox_2d": [255, 239, 337, 249], "page": 1},
 {"key": "taxpayer.mobile", "value": "010-6144-1173", "bbox_2d": [666, 239, 754, 249], "page": 1},
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
 {"key": "tax_agent.name", "value": "기혁찬", "bbox_2d": [771, 801, 814, 812], "page": 1},
 {"key": "tax_agent.biz_no", "value": "843-44-26624", "bbox_2d": [297, 823, 383, 836], "page": 1},
 {"key": "tax_agent.phone", "value": "051-458-0003", "bbox_2d": [684, 823, 770, 836], "page": 1},
 {"key": "tax_office", "value": "반포세무서장", "bbox_2d": [89, 846, 203, 861], "page": 1}]
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
- residency: 거주구분 (체크박스, 보기: 거주자 / 비거주자)
- nationality: 내ㆍ외국인 (체크박스, 보기: 내국인 / 외국인)
- seal.taxpayer: 신고인 (같은 설명 중 1번째 칸, 도장)
- sign.taxpayer: 신고인 (같은 설명 중 2번째 칸, 서명)
- seal.tax_agent: 세무대리인 (같은 설명 중 1번째 칸, 도장)
- sign.tax_agent: 세무대리인 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "residency", "value": "거주자", "bbox_2d": [720, 89, 738, 99], "page": 1},
 {"key": "nationality", "value": "내국인", "bbox_2d": [720, 111, 738, 122], "page": 1},
 {"key": "seal.taxpayer", "value": false},
 {"key": "sign.taxpayer", "value": false},
 {"key": "seal.tax_agent", "value": false},
 {"key": "sign.tax_agent", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa income_tax_return --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check income_tax_return` → `python -m docgen.formdir card income_tax_return` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `generate.py` 가 돌려주는 dict 에 그 키 값 | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` | 다시 |
| 답의 값 | `generate.py` (값 만드는 함수). 파이썬 대신 정하려면 `fields.json` 의 그 칸 `source` | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (파일로). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa income_tax_return --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions income_tax_return --show` · `python -m docgen.preview income_tax_return --out work/income_tax_return`
