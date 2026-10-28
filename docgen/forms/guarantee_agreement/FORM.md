# 보증약정서 (`guarantee_agreement`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card guarantee_agreement · card-hash: 31bffbaac4a1 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 보증약정서 (다른 이름: 보증서(특정채무보증용))
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa guarantee_agreement --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 법인 여신에 대한 대표이사 보증약정서.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 29칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank` | 은행명 | text | 1쪽 [105, 41, 200, 63] | 늘 | 템플릿 | generate.py | fields.json:5 | 묻기 |
| `creditor` | 채권자 | text | 1쪽 [77, 132, 199, 145] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:20 | 묻기 |
| `branch` | 취급점 | text | 1쪽 [280, 133, 337, 144] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:10 | 묻기 |
| `customer.name` ← `debtor.name` | 채무자 | text | 1쪽 [290, 191, 389, 204] | 늘 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:40 | 묻기 |
| `customer.biz_no` ← `debtor.biz_no` | 사업자등록번호 | biz_no | 1쪽 [560, 191, 644, 204] | 늘 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:30 | 묻기 |
| `customer.ceo` ← `debtor.ceo` | 대표자 | text | 1쪽 [290, 212, 350, 224] | 늘 | 템플릿 | generate.py | look/template.html.j2:26 · fields.json:35 | 묻기 |
| `customer.address` ← `debtor.address` | 소재지 | text | 1쪽 [560, 212, 836, 224] | 늘 | 템플릿 | generate.py | look/template.html.j2:26 · fields.json:25 | 묻기 |
| `related.name` ← `guarantor.name` | 보증인 | text | 1쪽 [290, 232, 352, 245] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:55 | 묻기 |
| `related.rrn` ← `guarantor.rrn` | 실명번호 | rrn | 1쪽 [560, 232, 662, 244] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:70 | 묻기 |
| `related.address` ← `guarantor.address` | 보증인주소 | text | 1쪽 [290, 251, 619, 267] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:50 | 묻기 |
| `related.phone` ← `guarantor.phone` | 연락처 | phone | 1쪽 [290, 273, 381, 285] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:60 | 묻기 |
| `guarantor.relation` | 채무자와의관계 | text | 1쪽 [560, 273, 620, 285] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:65 | 묻기 |
| `co_guarantors.*.name` | 보증인 | text | 1쪽 [290, 293, 336, 306] (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:78 · fields.json:150 | 묻기 |
| `co_guarantors.*.rrn` | 실명번호 | rrn | 1쪽 [560, 293, 662, 306] (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:165 | 묻기 |
| `co_guarantors.*.address` | 보증인주소 | text | 1쪽 [290, 312, 661, 328] (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:145 | 묻기 |
| `co_guarantors.*.phone` | 연락처 | phone | 1쪽 [290, 334, 382, 346] (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:155 | 묻기 |
| `co_guarantors.*.relation` | 채무자와의관계 | text | 1쪽 [560, 334, 659, 346] (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:160 | 묻기 |
| `method` | 보증방법 | text | 1쪽 [250, 412, 335, 423] | 늘 | 템플릿 | generate.py | look/template.html.j2:17 · fields.json:105 | 묻기 |
| `secured_debt` | 피보증채무 | text | 1쪽 [334, 495, 749, 513] | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:130 | 묻기 |
| `max_amount_korean` | 보증채무최고액(한글) | amount_korean | 1쪽 [237, 518, 442, 536] | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:100 | 묻기 |
| `max_amount` | 보증채무최고액 | amount | 1쪽 [472, 522, 557, 535] | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:95 | 묻기 |
| `period` | 보증기간 | text | 1쪽 [237, 543, 387, 556] | 늘 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:110 | 묻기 |
| `handwritten.method` | 자필보증방법 | text | 1쪽 [237, 676, 364, 693] | 늘 | 템플릿 | generate.py | look/template.html.j2:66 · fields.json:85 | 묻기 |
| `handwritten.name` | 자필성명 | text | 1쪽 [700, 676, 785, 693] | 늘 | 템플릿 | generate.py | look/template.html.j2:66 · fields.json:90 | 묻기 |
| `handwritten.max_amount` | 자필보증채무최고액 | amount_korean | 1쪽 [237, 701, 455, 720] | 늘 | 템플릿 | generate.py | look/template.html.j2:67 · fields.json:80 | 묻기 |
| `handwritten.confirm` | 자필설명확인 | text | 1쪽 [237, 728, 301, 745] | 늘 | 템플릿 | generate.py | look/template.html.j2:68 · fields.json:75 | 묻기 |
| `contract_date` | 약정일 | date | 1쪽 [92, 805, 203, 817] | 늘 | 템플릿 | generate.py | look/template.html.j2:76 · fields.json:15 | 묻기 |
| `signature` | 보증인 | text | 1쪽 [790, 790, 862, 804] | 늘 | 템플릿 | generate.py | look/template.html.j2:14 · fields.json:135 | 묻기 |
| `special_terms.*` | 특약사항 | - | - (1행) | 4/16 | 템플릿 | generate.py | - | 묻기 |

## 체크·도장·서명 (marks) — 4칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `explained` | 설명이해확인 | checkbox (예 / 아니오) | 1쪽 [814, 758, 829, 770] | 늘 | 템플릿 | generate.py | look/template.html.j2:72 · fields.json:45 | 묻기 |
| `seal.related` ← `seal.guarantor` | 보증인 | seal | 1쪽 [856, 766, 947, 830] | 늘 | 템플릿 | generate.py | fields.json:125 | 묻기 |
| `seal.co_guarantor` | 인감 | seal | 1쪽 [856, 795, 947, 860] | 3/16 | 템플릿 | generate.py | fields.json:115 | 묻기 |
| `seal.co_guarantor2` | 인감 | 도장 | - | 2/16 | 템플릿 | generate.py | fields.json:120 | 묻기 |

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
"보증약정서"
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
 "주식회사 국민은행",
 "센텀지점",
 "(주)미래케미칼",
 "702-81-38348",
 "남궁예태",
 "제주특별자치도 제주시 첨단로 381-19, 2층",
 "850328-2******",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "010-6144-1173",
 "대표이사",
 "노도수",
 "830120-1******",
 "충청남도 천안시 서북구 봉정로 505-12, 114동 2201호",
 "010-9992-7546",
 "최대주주(이사)",
 "특정채무보증",
 "2025년 4월 14일자 시설자금대출 금 2,100,000,000원",
 "금 이십오억이천만원정",
 "2,520,000,000",
 "2025.04.14 ~ 2035.04.14",
 "확인함",
 "2025년 04월 14일"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"제주특별자치도 제주시 첨단로 381-19, 2층"
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
- bank: 은행명
- creditor: 채권자
- branch: 취급점
- customer.name: 채무자 (고객 성명)
- customer.biz_no: 사업자등록번호 (고객 사업자등록번호)
- customer.ceo: 대표자 (고객 대표자)
- customer.address: 소재지 (고객 주소)
- related.name: 보증인 (보증인·공동 성명, 같은 항목명 중 1번째 칸)
- related.rrn: 실명번호 (보증인·공동 주민등록번호, 같은 항목명 중 1번째 칸)
- related.address: 보증인주소 (보증인·공동 주소, 같은 항목명 중 1번째 칸)
- related.phone: 연락처 (보증인·공동 연락처, 같은 항목명 중 1번째 칸)
- guarantor.relation: 채무자와의관계 (같은 항목명 중 1번째 칸)
- co_guarantors.0.name: 보증인 (1행)
- co_guarantors.0.rrn: 실명번호 (1행)
- co_guarantors.0.address: 보증인주소 (1행)
- co_guarantors.0.phone: 연락처 (1행)
- co_guarantors.0.relation: 채무자와의관계 (1행)
- method: 보증방법
- secured_debt: 피보증채무
- max_amount_korean: 보증채무최고액(한글)
- max_amount: 보증채무최고액
- period: 보증기간
- handwritten.method: 자필보증방법
- handwritten.name: 자필성명
- handwritten.max_amount: 자필보증채무최고액
- handwritten.confirm: 자필설명확인
- contract_date: 약정일
- signature: 보증인 (같은 항목명 중 3번째 칸)
```

답:

```json
[{"key": "bank", "value": "국민은행", "bbox_2d": [105, 41, 200, 63], "page": 1},
 {"key": "creditor", "value": "주식회사 국민은행", "bbox_2d": [77, 132, 199, 145], "page": 1},
 {"key": "branch", "value": "센텀지점", "bbox_2d": [280, 133, 337, 144], "page": 1},
 {"key": "customer.name", "value": "(주)미래케미칼", "bbox_2d": [290, 191, 389, 204], "page": 1},
 {"key": "customer.biz_no", "value": "702-81-38348", "bbox_2d": [560, 191, 644, 204], "page": 1},
 {"key": "customer.ceo", "value": "남궁예태", "bbox_2d": [290, 212, 350, 224], "page": 1},
 {"key": "customer.address", "value": "제주특별자치도 제주시 첨단로 381-19, 2층", "bbox_2d": [560, 212, 836, 224], "page": 1},
 {"key": "related.name", "value": "남궁예태", "bbox_2d": [290, 232, 352, 245], "page": 1},
 {"key": "related.rrn", "value": "850328-2******", "bbox_2d": [560, 232, 662, 244], "page": 1},
 {"key": "related.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [290, 251, 619, 267], "page": 1},
 {"key": "related.phone", "value": "010-6144-1173", "bbox_2d": [290, 273, 381, 285], "page": 1},
 {"key": "guarantor.relation", "value": "대표이사", "bbox_2d": [560, 273, 620, 285], "page": 1},
 {"key": "co_guarantors.0.name", "value": "노도수", "bbox_2d": [290, 293, 336, 306], "page": 1},
 {"key": "co_guarantors.0.rrn", "value": "830120-1******", "bbox_2d": [560, 293, 662, 306], "page": 1},
 {"key": "co_guarantors.0.address", "value": "충청남도 천안시 서북구 봉정로 505-12, 114동 2201호", "bbox_2d": [290, 312, 661, 328], "page": 1},
 {"key": "co_guarantors.0.phone", "value": "010-9992-7546", "bbox_2d": [290, 334, 382, 346], "page": 1},
 {"key": "co_guarantors.0.relation", "value": "최대주주(이사)", "bbox_2d": [560, 334, 659, 346], "page": 1},
 {"key": "method", "value": "특정채무보증", "bbox_2d": [250, 412, 335, 423], "page": 1},
 {"key": "secured_debt", "value": "2025년 4월 14일자 시설자금대출 금 2,100,000,000원", "bbox_2d": [334, 495, 749, 513], "page": 1},
 {"key": "max_amount_korean", "value": "금 이십오억이천만원정", "bbox_2d": [237, 518, 442, 536], "page": 1},
 {"key": "max_amount", "value": "2,520,000,000", "bbox_2d": [472, 522, 557, 535], "page": 1},
 {"key": "period", "value": "2025.04.14 ~ 2035.04.14", "bbox_2d": [237, 543, 387, 556], "page": 1},
 {"key": "handwritten.method", "value": "특정채무보증", "bbox_2d": [237, 676, 364, 693], "page": 1},
 {"key": "handwritten.name", "value": "남궁예태", "bbox_2d": [700, 676, 785, 693], "page": 1},
 {"key": "handwritten.max_amount", "value": "금 이십오억이천만원정", "bbox_2d": [237, 701, 455, 720], "page": 1},
 {"key": "handwritten.confirm", "value": "확인함", "bbox_2d": [237, 728, 301, 745], "page": 1},
 {"key": "contract_date", "value": "2025년 04월 14일", "bbox_2d": [92, 805, 203, 817], "page": 1},
 {"key": "signature", "value": "남궁예태", "bbox_2d": [790, 790, 862, 804], "page": 1}]
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
- explained: 설명이해확인 (체크박스, 보기: 예 / 아니오)
- seal.related: 보증인 (보증인·공동 도장, 도장)
- seal.co_guarantor: 인감 (보증인·공동 당사자의 신청인, 도장)
```

답:

```json
[{"key": "explained", "value": "예", "bbox_2d": [802, 758, 811, 770], "page": 1},
 {"key": "seal.related", "value": true, "bbox_2d": [856, 766, 947, 830], "page": 1},
 {"key": "seal.co_guarantor", "value": true, "bbox_2d": [856, 795, 947, 860], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa guarantee_agreement --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check guarantee_agreement` → `python -m docgen.formdir card guarantee_agreement` (실제 질문→답 확인).

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
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa guarantee_agreement --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions guarantee_agreement --show` · `python -m docgen.preview guarantee_agreement --out work/guarantee_agreement`
