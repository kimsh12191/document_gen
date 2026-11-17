# 고객확인서(개인) (`customer_due_diligence`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card customer_due_diligence · card-hash: 54a95508e154 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 고객확인서(개인)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa customer_due_diligence --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 특정금융정보법 제5조의2에 따른 개인 고객확인(CDD) — 은행 '고객거래확인서(개인·개인사업자용)'.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_account.py`, `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 28칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank.name` | 은행명 | text | 1쪽 [65, 26, 160, 44] | 늘 | 템플릿 | generate.py | look/template.html.j2:96 · fields.json:20 | 묻기 |
| `customer.name` | 성명(한글) | text | 1쪽 [280, 194, 386, 206] | 늘 | 템플릿 | generate.py | look/template.html.j2:11 · fields.json:75 | 묻기 |
| `customer.name_en` | 성명(영문) | text | - | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:80 | 묻기 |
| `customer.rrn` | 실명번호 | rrn | 1쪽 [171, 220, 270, 232] | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:95 | 묻기 |
| `customer.nationality` | 국적 | text | 1쪽 [654, 239, 726, 250] | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:85 | 묻기 |
| `customer.address` | 주소(거소) | text | 1쪽 [171, 257, 673, 269] | 늘 | 템플릿 | generate.py | look/template.html.j2:24 · fields.json:55 | 묻기 |
| `customer.mobile` | 휴대전화 | phone | 1쪽 [264, 276, 354, 287] | 늘 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:70 | 묻기 |
| `customer.email` | E-mail | text | - | 늘 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:60 | 묻기 |
| `job.company` | 직장명 | text | 1쪽 [259, 347, 379, 359] | 13/16 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:140 | 묻기 |
| `job.department` | 부서/직위 | text | 1쪽 [779, 347, 893, 359] | 13/16 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:145 | 묻기 |
| `job.industry` | 업종 | text | 1쪽 [259, 365, 354, 377] | 13/16 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:150 | 묻기 |
| `job.work_phone` | 직장전화 | phone | 1쪽 [779, 365, 861, 377] | 13/16 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:165 | 묻기 |
| `date` | 작성일 | date | 1쪽 [559, 753, 654, 764] | 늘 | 템플릿 | generate.py | look/template.html.j2:92 · fields.json:100 | 묻기 |
| `signature` | 고객성명 | text | 1쪽 [749, 753, 868, 764] | 늘 | 템플릿 | generate.py | look/template.html.j2:93 · fields.json:220 | 묻기 |
| `bank_use.branch` | 확인영업점 | text | 1쪽 [178, 853, 237, 864] | 늘 | 템플릿 | generate.py | look/template.html.j2:104 · fields.json:25 | 묻기 |
| `bank_use.clerk` | 담당 | text | 1쪽 [810, 842, 850, 852] | 늘 | 템플릿 | generate.py | look/template.html.j2:106 · fields.json:30 | 묻기 |
| `bank_use.manager` | 책임자 | text | 1쪽 [891, 842, 931, 852] | 늘 | 템플릿 | generate.py | look/template.html.j2:106 · fields.json:40 | 묻기 |
| `edd.annual_income` | 연간소득 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:77 · fields.json:105 | 묻기 |
| `edd.fund_detail` | 자금원천상세 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:78 · fields.json:120 | 묻기 |
| `edd.purpose_detail` | 거래목적상세 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:79 · fields.json:130 | 묻기 |
| `edd.cash_tx` | 고액현금거래 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:80 · fields.json:115 | 묻기 |
| `edd.overseas_tx` | 해외거래 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:80 · fields.json:125 | 묻기 |
| `agent.name` | 대리인성명 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:70 · fields.json:5 | 묻기 |
| `agent.rrn` | 대리인실명번호 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:70 · fields.json:15 | 묻기 |
| `agent.relation` | 본인과의관계 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:70 · fields.json:10 | 묻기 |
| `owner.name` | 실제소유자성명 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:175 | 묻기 |
| `owner.birth` | 실제소유자생년월일 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:170 | 묻기 |
| `owner.nationality` | 실제소유자국적 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:180 | 묻기 |

## 표 `edd.accounts` (표 과제 table·table_read·table_find·table_qa) — 3열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `edd.accounts.*.bank` | 금융회사 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:86 · fields.json:250 | 묻기 |
| `edd.accounts.*.kind` | 계좌종류 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:86 · fields.json:255 | 묻기 |
| `edd.accounts.*.purpose` | 주된용도 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:86 · fields.json:260 | 묻기 |

## 체크·도장·서명 (marks) — 18칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `customer.resident_type` | 구분 | checkbox (내국인 / 재외국민 / 외국인) | 1쪽 [813, 220, 857, 232] | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:90 | 묻기 |
| `customer.gender` | 성별 | checkbox (남 / 여) | 1쪽 [220, 239, 235, 250] | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:65 | 묻기 |
| `job.type` | 직업 | checkbox (급여소득자 / 개인사업자 / 전문직 / 공무원 / 연금소득자 / 주부 / 학생 / 무직 / 기타) | 1쪽 [183, 327, 256, 339] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:160 | 묻기 |
| `transaction.purpose` | 거래목적 | checkbox (급여 및 생활비 / 저축 및 투자 / 보험료 납부결제 / 공과금 납부결제 / 카드대금 결제 / 대출원리금 상환결제 / 사업상 거래 / 기타) | 1쪽 [183, 446, 278, 457] | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:240 | 묻기 |
| `transaction.fund_source` | 자금의원천 | checkbox (근로 및 연금소득 / 퇴직소득 / 사업소득 / 부동산임대소득 / 부동산양도소득 / 금융소득(이자 및 배당) / 상속·증여 / 일시 재산양도로 인한 소득 / 기타) | 1쪽 [183, 482, 292, 494] | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:235 | 묻기 |
| `transaction.expected_amount` | 예상거래금액 | checkbox (1천만원 미만 / 1천만원~5천만원 / 5천만원~1억원 / 1억원 이상) | 1쪽 [422, 518, 518, 529] | 늘 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:225 | 묻기 |
| `transaction.frequency` | 예상거래빈도 | checkbox (월 5회 미만 / 월 5~10회 / 월 10~20회 / 월 20회 이상) | 1쪽 [464, 532, 534, 543] | 늘 | 템플릿 | generate.py | look/template.html.j2:50 · fields.json:230 | 묻기 |
| `beneficial_owner` | 실제소유자여부 | checkbox (예 / 아니오) | 1쪽 [862, 574, 876, 586] | 늘 | 템플릿 | generate.py | look/template.html.j2:56 · fields.json:50 | 묻기 |
| `pep` | 외국의정치적주요인물여부 | checkbox (예 / 아니오) | 1쪽 [865, 653, 908, 664] | 늘 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:185 | 묻기 |
| `seal.customer` | 고객 | seal | 1쪽 [888, 739, 945, 779] | 늘 | 템플릿 | generate.py | fields.json:195 | 묻기 |
| `sign.customer` | 고객 | signature | 1쪽 [872, 752, 962, 766] | 늘 | 템플릿 | generate.py | fields.json:215 | 묻기 |
| `bank_use.risk_grade` | 고객위험등급 | checkbox (저위험 / 중위험 / 고위험) | 1쪽 [323, 814, 367, 825] | 늘 | 템플릿 | generate.py | look/template.html.j2:102 · fields.json:45 | 묻기 |
| `bank_use.id_type` | 실명확인증표 | checkbox (주민등록증 / 운전면허증 / 여권 / 외국인등록증 / 모바일신분증) | 1쪽 [434, 833, 521, 845] | 늘 | 템플릿 | generate.py | look/template.html.j2:103 · fields.json:35 | 묻기 |
| `seal.staff.clerk` | 담당 | seal | 1쪽 [803, 828, 857, 867] | 늘 | 템플릿 | generate.py | fields.json:200 | 묻기 |
| `seal.staff.manager` | 책임자 | seal | 1쪽 [884, 828, 938, 867] | 늘 | 템플릿 | generate.py | fields.json:205 | 묻기 |
| `edd.assets` | 보유자산규모 | 체크박스 (5억원 미만 / 5억원~10억원 / 10억원~30억원 / 30억원 이상) | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:77 · fields.json:110 | 묻기 |
| `seal.agent` | 대리인 | 도장 | - | 1/16 | 템플릿 | generate.py | fields.json:190 | 묻기 |
| `sign.agent` | 대리인 | 서명 | - | 1/16 | 템플릿 | generate.py | fields.json:210 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키는·값은:** 어디서 정해지나. 키·값 종류는 이 서식 파일에 적힌 그대로입니다 (모든 서식 공통 키 사전은 없음). "키 설명 그대로" 는 칸에 `"key"` 가 없어 키 설명이 키로 나가는 것. 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
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
"고객확인서(개인)"
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
 "시티 누르하야티",
 "890619-6103481",
 "인도네시아",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "010-6088-4593",
 "주식회사 다온패션",
 "고객지원팀 / 대리",
 "도매 및 소매업",
 "051-509-1176",
 "2025년 4월 1일",
 "NURHAYATI SITI",
 "센텀지점",
 "선우훈우",
 "남궁경도"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"인도네시아"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)"
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
- bank.name: 은행명
- customer.name: 성명(한글)
- customer.name_en: 성명(영문)
- customer.rrn: 실명번호
- customer.nationality: 국적
- customer.address: 주소(거소)
- customer.mobile: 휴대전화
- customer.email: E-mail
- job.company: 직장명
- job.department: 부서/직위
- job.industry: 업종
- job.work_phone: 직장전화
- date: 작성일
- signature: 고객성명
- bank_use.branch: 확인영업점
- bank_use.clerk: 담당
- bank_use.manager: 책임자
```

답:

```json
[{"key": "bank.name", "value": "국민은행", "bbox_2d": [65, 26, 160, 44], "page": 1},
 {"key": "customer.name", "value": "시티 누르하야티", "bbox_2d": [280, 194, 386, 206], "page": 1},
 {"key": "customer.name_en", "value": null},
 {"key": "customer.rrn", "value": "890619-6103481", "bbox_2d": [171, 220, 270, 232], "page": 1},
 {"key": "customer.nationality", "value": "인도네시아", "bbox_2d": [654, 239, 726, 250], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [171, 257, 673, 269], "page": 1},
 {"key": "customer.mobile", "value": "010-6088-4593", "bbox_2d": [264, 276, 354, 287], "page": 1},
 {"key": "customer.email", "value": null},
 {"key": "job.company", "value": "주식회사 다온패션", "bbox_2d": [259, 347, 379, 359], "page": 1},
 {"key": "job.department", "value": "고객지원팀 / 대리", "bbox_2d": [779, 347, 893, 359], "page": 1},
 {"key": "job.industry", "value": "도매 및 소매업", "bbox_2d": [259, 365, 354, 377], "page": 1},
 {"key": "job.work_phone", "value": "051-509-1176", "bbox_2d": [779, 365, 861, 377], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [559, 753, 654, 764], "page": 1},
 {"key": "signature", "value": "NURHAYATI SITI", "bbox_2d": [749, 753, 868, 764], "page": 1},
 {"key": "bank_use.branch", "value": "센텀지점", "bbox_2d": [178, 853, 237, 864], "page": 1},
 {"key": "bank_use.clerk", "value": "선우훈우", "bbox_2d": [810, 842, 850, 852], "page": 1},
 {"key": "bank_use.manager", "value": "남궁경도", "bbox_2d": [891, 842, 931, 852], "page": 1}]
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
- customer.resident_type: 구분 (체크박스, 보기: 내국인 / 재외국민 / 외국인)
- customer.gender: 성별 (체크박스, 보기: 남 / 여)
- job.type: 직업 (체크박스, 보기: 급여소득자 / 개인사업자 / 전문직 / 공무원 / 연금소득자 / 주부 / 학생 / 무직 / 기타)
- transaction.purpose: 거래목적 (체크박스, 보기: 급여 및 생활비 / 저축 및 투자 / 보험료 납부결제 / 공과금 납부결제 / 카드대금 결제 / 대출원리금 상환결제 / 사업상 거래 / 기타)
- transaction.fund_source: 자금의원천 (체크박스, 보기: 근로 및 연금소득 / 퇴직소득 / 사업소득 / 부동산임대소득 / 부동산양도소득 / 금융소득(이자 및 배당) / 상속·증여 / 일시 재산양도로 인한 소득 / 기타)
- transaction.expected_amount: 예상거래금액 (체크박스, 보기: 1천만원 미만 / 1천만원~5천만원 / 5천만원~1억원 / 1억원 이상)
- transaction.frequency: 예상거래빈도 (체크박스, 보기: 월 5회 미만 / 월 5~10회 / 월 10~20회 / 월 20회 이상)
- beneficial_owner: 실제소유자여부 (체크박스, 보기: 예 / 아니오)
- pep: 외국의정치적주요인물여부 (체크박스, 보기: 예 / 아니오)
- seal.customer: 고객 (같은 설명 중 1번째 칸, 도장)
- sign.customer: 고객 (같은 설명 중 2번째 칸, 서명)
- bank_use.risk_grade: 고객위험등급 (체크박스, 보기: 저위험 / 중위험 / 고위험)
- bank_use.id_type: 실명확인증표 (체크박스, 보기: 주민등록증 / 운전면허증 / 여권 / 외국인등록증 / 모바일신분증)
- seal.staff.clerk: 담당 (도장)
- seal.staff.manager: 책임자 (도장)
```

답:

```json
[{"key": "customer.resident_type", "value": "외국인", "bbox_2d": [801, 220, 810, 232], "page": 1},
 {"key": "customer.gender", "value": "여", "bbox_2d": [208, 239, 216, 250], "page": 1},
 {"key": "job.type", "value": "급여소득자", "bbox_2d": [171, 327, 179, 339], "page": 1},
 {"key": "transaction.purpose", "value": "급여 및 생활비", "bbox_2d": [171, 446, 179, 457], "page": 1},
 {"key": "transaction.fund_source", "value": "근로 및 연금소득", "bbox_2d": [171, 482, 179, 494], "page": 1},
 {"key": "transaction.expected_amount", "value": "5천만원~1억원", "bbox_2d": [410, 518, 419, 529], "page": 1},
 {"key": "transaction.frequency", "value": "월 10~20회", "bbox_2d": [452, 532, 460, 543], "page": 1},
 {"key": "beneficial_owner", "value": "예", "bbox_2d": [849, 574, 858, 586], "page": 1},
 {"key": "pep", "value": "아니오", "bbox_2d": [852, 653, 861, 664], "page": 1},
 {"key": "seal.customer", "value": true, "bbox_2d": [888, 739, 945, 779], "page": 1},
 {"key": "sign.customer", "value": false},
 {"key": "bank_use.risk_grade", "value": "고위험", "bbox_2d": [311, 814, 320, 825], "page": 1},
 {"key": "bank_use.id_type", "value": "외국인등록증", "bbox_2d": [421, 833, 430, 845], "page": 1},
 {"key": "seal.staff.clerk", "value": true, "bbox_2d": [803, 828, 857, 867], "page": 1},
 {"key": "seal.staff.manager", "value": true, "bbox_2d": [884, 828, 938, 867], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa customer_due_diligence --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check customer_due_diligence` → `python -m docgen.formdir card customer_due_diligence` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa customer_due_diligence --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions customer_due_diligence --show` · `python -m docgen.preview customer_due_diligence --out work/customer_due_diligence`
