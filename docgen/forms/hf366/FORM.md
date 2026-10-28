# Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(국문) (`hf366`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf366 · card-hash: d86295d379dd -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(국문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.366 (전자금융) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 28칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `corp.corp_reg_no` ← `company.corp_reg_no` | 법인등록번호* | corp_reg_no | 1쪽 [206, 310, 309, 319] | 늘 | 규칙: '법인등록번호 *' → `company.corp_no` | 고객 정보 (키 `company.corp_no`) | fields.json:23 | 묻기 |
| `customer.zipcode` | 우편번호* | number | 1쪽 [169, 460, 213, 472] | 늘 | 규칙: '우편번호 *' → `customer.zipcode` | 고객 정보 (키 `customer.zipcode`) | fields.json:34 | 묻기 |
| `customer.address` | 주소* | text | 1쪽 [140, 492, 301, 497] | 늘 | 규칙: '주소 *' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:45 | 묻기 |
| `company.corp_no2` | 법인등록번호* | rrn | 1쪽 [331, 309, 450, 320] | 늘 | 규칙: '법인등록번호 *' → `company.corp_no` | 고객 정보 (키 `company.corp_no`) | fields.json:56 | 묻기 |
| `corp.biz_no` ← `company.biz_no` | 사업자등록번호* | biz_no | 1쪽 [332, 339, 431, 350] | 늘 | 규칙: '사업자 등록번호 *' → `company.biz_no` | 고객 정보 (키 `company.biz_no`) | fields.json:67 | 묻기 |
| `value` | (국문)* | amount | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:79 | 묻기 |
| `value2` | (영문)* | amount | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:91 | 묻기 |
| `교육기관대표자` | 교육기관대표자* | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:103 | 묻기 |
| `customer.zipcode2` | 우편번호* | number | 1쪽 [330, 460, 374, 472] | 늘 | 규칙: '우편번호 *' → `customer.zipcode` | 고객 정보 (키 `customer.zipcode`) | fields.json:114 | 묻기 |
| `customer.address2` | 주소* | text | 1쪽 [331, 491, 668, 502] | 늘 | 규칙: '주소 *' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:125 | 묻기 |
| `customer.phone` | 전화번호* | phone | 1쪽 [334, 551, 440, 563] | 늘 | 규칙: '전화번호 *' → `customer.phone` | 고객 정보 (키 `customer.phone`) | fields.json:136 | 묻기 |
| `팩스번호` | 팩스번호* | phone | 1쪽 [330, 582, 427, 593] | 늘 | 항목명 그대로 | 값 종류 `phone` (항목명 자동) | fields.json:148 | 묻기 |
| `목록.*.통화` | 통화 | text | 1쪽 [80, 709, 114, 720] (1행) | 늘 | 표 행 (묶음·항목명 '통화') | 값 종류 `currency` (항목명 자동) | fields.json:160 | 묻기 |
| `목록.*.계좌번호` | 계좌번호(계좌종류) | text | 1쪽 [214, 709, 348, 720] (1행) | 늘 | 표 행 (묶음·항목명 '계좌번호(계좌종류)') | 값 종류 `account` (항목명 자동) | fields.json:232 | 묻기 |
| `목록.*.예금주명` | 예금주명 | text | - (1행) | 늘 | 표 행 (묶음·항목명 '예금주명') | 값 종류 `text` (항목명 자동) | fields.json:304 | 묻기 |
| `목록.*.인감서명` | 인감/서명 | text | - (1행) | 늘 | 표 행 (묶음·항목명 '인감/서명') | 값 종류 `seal` (항목명 자동) | fields.json:376 | 묻기 |
| `customer.name` | 성명* | text | 2쪽 [197, 153, 261, 164] | 늘 | 규칙: '성명 *' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:514 | 묻기 |
| `customer.address3` | 주소* | text | 2쪽 [149, 184, 309, 189] | 늘 | 규칙: '주소 *' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:525 | 묻기 |
| `agent.name` | 성명* | text | 2쪽 [284, 153, 347, 164] | 늘 | 규칙: '성명 *' → `agent.name` | 고객 정보 (키 `agent.name`) | fields.json:536 | 묻기 |
| `agent.address` | 주소* | text | 2쪽 [288, 183, 624, 194] | 늘 | 규칙: '주소 *' → `agent.address` | 고객 정보 (키 `agent.address`) | fields.json:549 | 묻기 |
| `agent.address2` | 주소* | text | 2쪽 [284, 213, 621, 225] | 늘 | 규칙: '주소 *' → `agent.address` | 고객 정보 (키 `agent.address`) | fields.json:562 | 묻기 |
| `agent.rrn` | 주민등록번호 | rrn | 2쪽 [282, 244, 386, 255] | 늘 | 규칙: '주민등록번호' → `agent.rrn` | 고객 정보 (키 `agent.rrn`) | fields.json:574 | 묻기 |
| `agent.relation` | 관계(부서/직위)* | text | 2쪽 [282, 274, 298, 285] | 늘 | 규칙: '관계 (부서/직위) *' → `agent.relation` | 고객 정보 (키 `agent.relation`) | fields.json:587 | 묻기 |
| `접수일자` | 접수일자* | date | 2쪽 [240, 684, 318, 695] | 늘 | 항목명 그대로 | 값 종류 `date` (항목명 자동) | fields.json:636 | 묻기 |
| `등록일자` | 등록일자* | date | 2쪽 [239, 715, 320, 726] | 늘 | 항목명 그대로 | 값 종류 `date` (항목명 자동) | fields.json:648 | 묻기 |
| `date` | 작성일 | date | 2쪽 [564, 369, 791, 387] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:660 | 묻기 |
| `고객교육기관명` | “고객”교육기관명 | text | 2쪽 [306, 423, 385, 434] | 늘 | 항목명 그대로 | 값 종류 `bank` (항목명 자동) | fields.json:685 | 묻기 |
| `customer.address4` | 주소 | text | 2쪽 [264, 444, 601, 455] | 늘 | 규칙: '주 소' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:696 | 묻기 |

## 체크·도장·서명 (marks) — 9칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.다음과같이` | 다음과같이 | checkbox (신규 / 변경/추가 / 해지 신청합니다.) | 1쪽 [159, 179, 211, 194] | 늘 | 체크 (항목명) | 보기 중 고름: 신규 / 변경/추가 / 해지 신청합니다. | fields.json:448 | 묻기 |
| `seal.customer` ← `seal.signer` | 서명/인감* | seal | 2쪽 [174, 295, 274, 321] | 늘 | 항목명 그대로 | 값 종류 `seal` (항목명 자동) | fields.json:503 | 묻기 |
| `sign.customer` ← `sign.signer` | 서명/인감* | signature | 2쪽 [174, 295, 274, 321] | 늘 | 항목명 그대로 | 값 종류 `seal` (항목명 자동) | fields.json:503 | 묻기 |
| `seal.signer2` | 서명/인감* | seal | 2쪽 [279, 295, 921, 362] | 늘 | 항목명 그대로 | 값 종류 `seal` (항목명 자동) | fields.json:599 | 묻기 |
| `sign.signer2` | 서명/인감* | signature | 2쪽 [279, 295, 921, 362] | 늘 | 항목명 그대로 | 값 종류 `seal` (항목명 자동) | fields.json:599 | 묻기 |
| `seal.signer3` | 서명/인감 | seal | 2쪽 [615, 531, 666, 567] | 늘 | 항목명 그대로 | 값 종류 `seal` (항목명 자동) | fields.json:611 | 묻기 |
| `sign.signer3` | 서명/인감 | signature | 2쪽 [360, 515, 921, 583] | 늘 | 항목명 그대로 | 값 종류 `seal` (항목명 자동) | fields.json:611 | 묻기 |
| `seal.signer4` | 담당자성명/서명* | seal | 2쪽 [231, 644, 921, 675] | 늘 | 항목명 그대로 | 값 종류 `seal` (항목명 자동) | fields.json:624 | 묻기 |
| `sign.signer4` | 담당자성명/서명* | signature | 2쪽 [231, 644, 921, 675] | 늘 | 항목명 그대로 | 값 종류 `seal` (항목명 자동) | fields.json:624 | 묻기 |

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
"Hana 1Q bank CMS iNet 서비스 이용 추가신청서(iSBS)(국문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "200112-7951835",
 "06295",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "702-81-38348",
 "010-6144-1173",
 "051-509-1176",
 "USD",
 "JPY",
 "EUR",
 "CNY",
 "342-713345-81046",
 "256-331534-90013",
 "263-664218-09043",
 "898-399735-44111",
 "330-676660-45101",
 "977-494805-63933",
 "남궁예태",
 "남궁찬윤",
 "521028-1******",
 "부",
 "2024.11.14",
 "2024-08-31",
 "카카오뱅크"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"카카오뱅크"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"서울특별시 서초구 강남대로 357, 103동 1301호"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- corp.corp_reg_no: 법인등록번호* (법인·사업자 법인등록번호, 같은 항목명 중 1번째 칸)
- customer.zipcode: 우편번호* (같은 항목명 중 1번째 칸)
- customer.address: 주소* (고객 주소, 같은 항목명 중 1번째 칸)
- company.corp_no2: 법인등록번호* (같은 항목명 중 2번째 칸)
- corp.biz_no: 사업자등록번호* (법인·사업자 사업자등록번호)
- value: (국문)*
- value2: (영문)*
- 교육기관대표자: 교육기관대표자*
- customer.zipcode2: 우편번호* (같은 항목명 중 2번째 칸)
- customer.address2: 주소* (같은 항목명 중 2번째 칸)
- customer.phone: 전화번호* (고객 연락처)
- 팩스번호: 팩스번호*
- 목록.2.통화: 통화 (목록 3행)
- 목록.3.통화: 통화 (목록 4행)
- 목록.4.통화: 통화 (목록 5행)
- 목록.5.통화: 통화 (목록 6행)
- 목록.0.계좌번호: 계좌번호(계좌종류) (목록 1행)
- 목록.1.계좌번호: 계좌번호(계좌종류) (목록 2행)
- 목록.2.계좌번호: 계좌번호(계좌종류) (목록 3행)
- 목록.4.계좌번호: 계좌번호(계좌종류) (목록 5행)
- 목록.5.계좌번호: 계좌번호(계좌종류) (목록 6행)
- 목록.0.예금주명: 예금주명 (목록 1행)
- 목록.2.예금주명: 예금주명 (목록 3행)
- 목록.3.예금주명: 예금주명 (목록 4행)
- 목록.4.예금주명: 예금주명 (목록 5행)
- 목록.5.예금주명: 예금주명 (목록 6행)
- 목록.0.인감서명: 인감/서명 (목록 1행)
- 목록.1.인감서명: 인감/서명 (목록 2행)
- 목록.2.인감서명: 인감/서명 (목록 3행)
- 목록.4.인감서명: 인감/서명 (목록 5행)
- 목록.5.인감서명: 인감/서명 (목록 6행)
- customer.name: 성명* (고객 성명, 같은 항목명 중 1번째 칸)
- customer.address3: 주소* (같은 항목명 중 3번째 칸)
- agent.name: 성명* (대리인 성명, 같은 항목명 중 2번째 칸)
- agent.address: 주소* (대리인 주소, 같은 항목명 중 4번째 칸)
- agent.relation: 관계(부서/직위)* (대리인 관계)
- 접수일자: 접수일자*
- date: 작성일
- 고객교육기관명: “고객”교육기관명
- customer.address4: 주소 (같은 항목명 중 6번째 칸)
```

답:

```json
[{"key": "corp.corp_reg_no", "value": "200112-7951835", "bbox_2d": [206, 310, 309, 319], "page": 1},
 {"key": "customer.zipcode", "value": "06295", "bbox_2d": [169, 460, 213, 472], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [140, 492, 301, 497], "page": 1},
 {"key": "company.corp_no2", "value": "200112-7951835", "bbox_2d": [331, 309, 450, 320], "page": 1},
 {"key": "corp.biz_no", "value": "702-81-38348", "bbox_2d": [332, 339, 431, 350], "page": 1},
 {"key": "value", "value": null},
 {"key": "value2", "value": null},
 {"key": "교육기관대표자", "value": null},
 {"key": "customer.zipcode2", "value": "06295", "bbox_2d": [330, 460, 374, 472], "page": 1},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [331, 491, 668, 502], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [334, 551, 440, 563], "page": 1},
 {"key": "팩스번호", "value": "051-509-1176", "bbox_2d": [330, 582, 427, 593], "page": 1},
 {"key": "목록.2.통화", "value": "JPY", "bbox_2d": [80, 769, 109, 781], "page": 1},
 {"key": "목록.3.통화", "value": "USD", "bbox_2d": [82, 800, 116, 811], "page": 1},
 {"key": "목록.4.통화", "value": "EUR", "bbox_2d": [80, 830, 113, 841], "page": 1},
 {"key": "목록.5.통화", "value": "CNY", "bbox_2d": [82, 860, 116, 872], "page": 1},
 {"key": "목록.0.계좌번호", "value": "342-713345-81046", "bbox_2d": [214, 709, 348, 720], "page": 1},
 {"key": "목록.1.계좌번호", "value": "256-331534-90013", "bbox_2d": [212, 739, 346, 750], "page": 1},
 {"key": "목록.2.계좌번호", "value": "263-664218-09043", "bbox_2d": [216, 769, 350, 781], "page": 1},
 {"key": "목록.4.계좌번호", "value": "330-676660-45101", "bbox_2d": [213, 830, 347, 841], "page": 1},
 {"key": "목록.5.계좌번호", "value": "977-494805-63933", "bbox_2d": [215, 860, 349, 872], "page": 1},
 {"key": "목록.0.예금주명", "value": null},
 {"key": "목록.2.예금주명", "value": null},
 {"key": "목록.3.예금주명", "value": null},
 {"key": "목록.4.예금주명", "value": null},
 {"key": "목록.5.예금주명", "value": null},
 {"key": "목록.0.인감서명", "value": null},
 {"key": "목록.1.인감서명", "value": null},
 {"key": "목록.2.인감서명", "value": null},
 {"key": "목록.4.인감서명", "value": null},
 {"key": "목록.5.인감서명", "value": null},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [197, 153, 261, 164], "page": 2},
 {"key": "customer.address3", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [149, 184, 309, 189], "page": 2},
 {"key": "agent.name", "value": "남궁찬윤", "bbox_2d": [284, 153, 347, 164], "page": 2},
 {"key": "agent.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [288, 183, 624, 194], "page": 2},
 {"key": "agent.relation", "value": "부", "bbox_2d": [282, 274, 298, 285], "page": 2},
 {"key": "접수일자", "value": "2024.11.14", "bbox_2d": [240, 684, 318, 695], "page": 2},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [564, 369, 791, 387], "page": 2},
 {"key": "고객교육기관명", "value": "카카오뱅크", "bbox_2d": [306, 423, 385, 434], "page": 2},
 {"key": "customer.address4", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [264, 444, 601, 455], "page": 2}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- check.다음과같이: 다음과같이 (체크박스, 보기: 신규 / 변경/추가 / 해지 신청합니다.)
- seal.customer: 서명/인감* (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 서명/인감* (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.signer2: 서명/인감* (같은 항목명 중 3번째 칸, 도장)
- sign.signer2: 서명/인감* (같은 항목명 중 4번째 칸, 서명)
- seal.signer3: 서명/인감 (같은 항목명 중 5번째 칸, 도장)
- sign.signer3: 서명/인감 (같은 항목명 중 6번째 칸, 서명)
- seal.signer4: 담당자성명/서명* (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer4: 담당자성명/서명* (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.다음과같이", "value": "신규", "bbox_2d": [159, 181, 176, 194], "page": 1},
 {"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [174, 295, 274, 321], "page": 2},
 {"key": "seal.signer2", "value": false},
 {"key": "sign.signer2", "value": true, "bbox_2d": [279, 295, 921, 362], "page": 2},
 {"key": "seal.signer3", "value": true, "bbox_2d": [615, 531, 666, 567], "page": 2},
 {"key": "sign.signer3", "value": false},
 {"key": "seal.signer4", "value": false},
 {"key": "sign.signer4", "value": true, "bbox_2d": [231, 644, 921, 675], "page": 2}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf366` → `python -m docgen.formdir card hf366` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf366 --show` · `python -m docgen.preview hf366 --out work/hf366`
