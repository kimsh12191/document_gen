# 기업관계사 서비스 이용신청서 (`hf346`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf346 · card-hash: 236405c4bb1e -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 기업관계사 서비스 이용신청서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf346 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.346 (전자금융) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 23칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `corp.corp_reg_no` ← `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 1쪽 [320, 170, 472, 194] | 늘 | 규칙: '법인등록번호' → `company.corp_no` | 고객 정보 (키 `company.corp_no`) | fields.json:119 | 묻기 |
| `employer.name` | 회사명 | text | 1쪽 [322, 193, 499, 220] | 늘 | 규칙: '회사명' → `employer.name` | 고객 정보 (키 `employer.name`) | fields.json:131 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [323, 216, 735, 243] | 늘 | 규칙: '주 소' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:143 | 묻기 |
| `company.corp_no2` | 법인등록번호 | rrn | 1쪽 [320, 238, 474, 266] | 늘 | 규칙: '법인등록번호' → `company.corp_no` | 고객 정보 (키 `company.corp_no`) | fields.json:155 | 묻기 |
| `거래은행영업점` | 거래은행/영업점 | text | 1쪽 [321, 264, 399, 289] | 늘 | 항목명 그대로 | 값 종류 `bank` (항목명 자동) | fields.json:167 | 묻기 |
| `employer.name2` | 회사명 | text | 1쪽 [320, 287, 496, 312] | 늘 | 규칙: '회사명' → `employer.name` | 고객 정보 (키 `employer.name`) | fields.json:180 | 묻기 |
| `customer.address2` | 주소 | text | 1쪽 [316, 306, 727, 340] | 늘 | 규칙: '주 소' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:192 | 묻기 |
| `customer.phone` | 전화번호 | phone | 1쪽 [323, 335, 461, 361] | 늘 | 규칙: '전화번호' → `customer.phone` | 고객 정보 (키 `customer.phone`) | fields.json:204 | 묻기 |
| `customer.email` | e-mail | text | 1쪽 [324, 356, 552, 386] | 늘 | 규칙: 'e-mail' → `customer.email` | 고객 정보 (키 `customer.email`) | fields.json:216 | 묻기 |
| `corp.biz_no` ← `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [706, 170, 842, 194] | 늘 | 규칙: '사업자등록번호' → `company.biz_no` | 고객 정보 (키 `company.biz_no`) | fields.json:274 | 묻기 |
| `corp.ceo` ← `company.ceo` | 대표자 | text | 1쪽 [699, 193, 789, 217] | 늘 | 규칙: '대표자' → `company.ceo` | 고객 정보 (키 `company.ceo`) | fields.json:286 | 묻기 |
| `company.biz_no2` | 사업자등록번호 | biz_no | 1쪽 [699, 240, 837, 267] | 늘 | 규칙: '사업자등록번호' → `company.biz_no` | 고객 정보 (키 `company.biz_no`) | fields.json:298 | 묻기 |
| `글로벌고객번호` | 글로벌고객번호 | rrn | 1쪽 [699, 264, 870, 289] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:310 | 묻기 |
| `company.ceo2` | 대표자 | text | 1쪽 [702, 287, 791, 312] | 늘 | 규칙: '대 표 자' → `company.ceo` | 고객 정보 (키 `company.ceo`) | fields.json:323 | 묻기 |
| `Fax` | Fax | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:335 | 묻기 |
| `agent.name` | 성명 | text | 2쪽 [320, 871, 394, 895] | 늘 | 규칙: '성 명' → `agent.name` | 고객 정보 (키 `agent.name`) | fields.json:923 | 묻기 |
| `agent.relation` | 관계 | text | 2쪽 [317, 893, 332, 917] | 늘 | 규칙: '관계' → `agent.relation` | 고객 정보 (키 `agent.relation`) | fields.json:935 | 묻기 |
| `employer.name3` | 회사명 | text | 2쪽 [321, 916, 498, 945] | 늘 | 규칙: '회사명' → `employer.name` | 고객 정보 (키 `employer.name`) | fields.json:947 | 묻기 |
| `agent.birth` | 생년월일 | date | 2쪽 [695, 868, 797, 894] | 늘 | 규칙: '생년월일' → `agent.birth` | 고객 정보 (키 `agent.birth`) | fields.json:958 | 묻기 |
| `agent.address` | 주소 | text | 2쪽 [698, 902, 861, 912] | 늘 | 규칙: '주 소' → `agent.address` | 고객 정보 (키 `agent.address`) | fields.json:970 | 묻기 |
| `company.ceo3` | 대표자 | text | 2쪽 [700, 916, 790, 942] | 늘 | 규칙: '대표자' → `company.ceo` | 고객 정보 (키 `company.ceo`) | fields.json:982 | 묻기 |
| `date` | 작성일 | date | 2쪽 [356, 787, 574, 804] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:1017 | 묻기 |
| `관계사업무위임및관계사ID에대한동의` | ■관계사업무위임및관계사ID에대한동의 | text | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:1042 | 묻기 |

## 표 `목록` (표 과제 table·table_read·table_find·table_qa) — 4열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `목록.*.실행자ID` | 실행자ID* | text | 1쪽 [191, 602, 244, 615] (1행) | 늘 | 표 행 (묶음·항목명 '실행자ID*') | 값 종류 `number` (항목명 자동) | fields.json:626 | 묻기 |
| `목록.*.통화` | 통화 | text | 1쪽 [260, 596, 304, 621] (1행) | 늘 | 표 행 (묶음·항목명 '통화') | 값 종류 `currency` (항목명 자동) | fields.json:650 | 묻기 |
| `목록.*.계좌번호` | 계좌번호 | text | 1쪽 [321, 598, 451, 618] (1행) | 늘 | 표 행 (묶음·항목명 '계좌번호') | 값 종류 `account` (항목명 자동) | fields.json:674 | 묻기 |
| `목록.*.인감서명` | 인감/서명 | text | - (1행) | 늘 | 표 행 (묶음·항목명 '인감/서명') | 값 종류 `seal` (항목명 자동) | fields.json:698 | 묻기 |

## 체크·도장·서명 (marks) — 15칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.신청구분` | 신청구분 | checkbox (신규 / 변경 / 해지) | 1쪽 [408, 152, 454, 164] | 늘 | 체크 (항목명) | 보기 중 고름: 신규 / 변경 / 해지 | fields.json:58 | 묻기 |
| `check.서비스종류` | 서비스종류 | checkbox (국내관계사 / 국외관계사) | 1쪽 [720, 152, 804, 164] | 늘 | 체크 (항목명) | 보기 중 고름: 국내관계사 / 국외관계사 | fields.json:229 | 묻기 |
| `check.조회서비스` | 조회서비스(위임범위) | checkbox (전체 / 부분 / 예금( / 전체 계좌, / 아래에서 지정한 계좌만 조회), / 외환, / 수출입, / 대출, / 전자결제, / 카드, / 지로/공과금) | 1쪽 [181, 426, 912, 454] | 늘 | 체크 (항목명) | 보기 중 고름: 전체 / 부분 / 예금( / 전체 계좌, / 아래에서 지정한 계좌만 조회), / 외환, / 수출입, / 대출, / 전자결제, / 카드, / 지로/공과금 | fields.json:347 | 묻기 |
| `check.아이디` | 아이디(ID) | checkbox (실행자 / OTP) | 1쪽 [789, 691, 847, 703] | 늘 | 체크 (항목명) | 보기 중 고름: 실행자 / OTP | fields.json:536 | 묻기 |
| `check.아이디2` | 아이디(ID) | checkbox (실행자 / OTP) | 1쪽 [789, 814, 847, 827] | 늘 | 체크 (항목명) | 보기 중 고름: 실행자 / OTP | fields.json:581 | 묻기 |
| `check.기업뱅킹` | 기업뱅킹(통합CMS) | checkbox (기업뱅킹(통합CMS) / CMS Plus / CMSiNet) | 1쪽 [170, 57, 380, 78] | 늘 | 체크 (항목명) | 보기 중 고름: 기업뱅킹(통합CMS) / CMS Plus / CMSiNet | fields.json:794 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [728, 34, 794, 75] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [728, 34, 794, 75] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [794, 34, 870, 75] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [794, 34, 870, 75] | 늘 | - | - | - | 묻기 |
| `seal.staff.지점장` | 지점장 | seal | 1쪽 [870, 34, 920, 75] | 늘 | - | - | - | 묻기 |
| `sign.staff.지점장` | 지점장 | signature | 1쪽 [870, 34, 920, 75] | 늘 | - | - | - | 묻기 |
| `check.주계약사` | 주계약사 | checkbox (관계사ID에 대한 동의) | 2쪽 [178, 548, 319, 561] | 늘 | 체크 (항목명) | 보기 중 고름: 관계사ID에 대한 동의 | fields.json:849 | 묻기 |
| `check.관계사` | 관계사 | checkbox (계좌 사용에 대한 동의 / 관리대상 이용자에 대한 동의) | 2쪽 [178, 687, 363, 700] | 늘 | 체크 (항목명) | 보기 중 고름: 계좌 사용에 대한 동의 / 관리대상 이용자에 대한 동의 | fields.json:878 | 묻기 |
| `check.본인은` | 본인은 | checkbox (OTP를 수령하고 “전자금융거래에 필요한 접근매체(OTP, 인증서 암호,) | 2쪽 [112, 739, 928, 752] | 늘 | 체크 (항목명) | 보기 중 고름: OTP를 수령하고 “전자금융거래에 필요한 접근매체(OTP, 인증서 암호, | fields.json:994 | 묻기 |

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
"기업관계사 서비스 이용신청서"
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
 "주식회사 다온패션",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "농협은행",
 "010-6144-1173",
 "yetae741@gmail.com",
 "702-81-38348",
 "남궁예태",
 "539946-6934759",
 "9095-3941",
 "123348-3234237",
 "AUD",
 "JPY",
 "731-219372-48636",
 "369-043479-16910",
 "남궁찬윤",
 "부",
 "1952.10.28"
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
"731-219372-48636"
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
- corp.corp_reg_no: 법인등록번호 (법인·사업자 법인등록번호, 같은 항목명 중 1번째 칸)
- employer.name: 회사명 (직장 이름, 같은 항목명 중 1번째 칸)
- customer.address: 주소 (고객 주소, 같은 항목명 중 1번째 칸)
- company.corp_no2: 법인등록번호 (같은 항목명 중 2번째 칸)
- 거래은행영업점: 거래은행/영업점
- employer.name2: 회사명 (같은 항목명 중 2번째 칸)
- customer.address2: 주소 (같은 항목명 중 2번째 칸)
- customer.phone: 전화번호 (고객 연락처)
- customer.email: e-mail (고객 이메일)
- corp.biz_no: 사업자등록번호 (법인·사업자 사업자등록번호, 같은 항목명 중 1번째 칸)
- corp.ceo: 대표자 (법인·사업자 대표자, 같은 항목명 중 1번째 칸)
- company.biz_no2: 사업자등록번호 (같은 항목명 중 2번째 칸)
- 글로벌고객번호: 글로벌고객번호
- company.ceo2: 대표자 (같은 항목명 중 2번째 칸)
- Fax: Fax
- agent.name: 성명 (대리인 성명)
- agent.relation: 관계 (대리인 관계)
- employer.name3: 회사명 (같은 항목명 중 3번째 칸)
- agent.birth: 생년월일 (대리인 생년월일)
- agent.address: 주소 (대리인 주소, 같은 항목명 중 3번째 칸)
- company.ceo3: 대표자 (같은 항목명 중 3번째 칸)
- date: 작성일
- 관계사업무위임및관계사ID에대한동의: ■관계사업무위임및관계사ID에대한동의
```

답:

```json
[{"key": "corp.corp_reg_no", "value": "200112-7951835", "bbox_2d": [320, 170, 472, 194], "page": 1},
 {"key": "employer.name", "value": "주식회사 다온패션", "bbox_2d": [322, 193, 499, 220], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [323, 216, 735, 243], "page": 1},
 {"key": "company.corp_no2", "value": "200112-7951835", "bbox_2d": [320, 238, 474, 266], "page": 1},
 {"key": "거래은행영업점", "value": "농협은행", "bbox_2d": [321, 264, 399, 289], "page": 1},
 {"key": "employer.name2", "value": "주식회사 다온패션", "bbox_2d": [320, 287, 496, 312], "page": 1},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [316, 306, 727, 340], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [323, 335, 461, 361], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [324, 356, 552, 386], "page": 1},
 {"key": "corp.biz_no", "value": "702-81-38348", "bbox_2d": [706, 170, 842, 194], "page": 1},
 {"key": "corp.ceo", "value": "남궁예태", "bbox_2d": [699, 193, 789, 217], "page": 1},
 {"key": "company.biz_no2", "value": "702-81-38348", "bbox_2d": [699, 240, 837, 267], "page": 1},
 {"key": "글로벌고객번호", "value": "539946-6934759", "bbox_2d": [699, 264, 870, 289], "page": 1},
 {"key": "company.ceo2", "value": "남궁예태", "bbox_2d": [702, 287, 791, 312], "page": 1},
 {"key": "Fax", "value": null},
 {"key": "agent.name", "value": "남궁찬윤", "bbox_2d": [320, 871, 394, 895], "page": 2},
 {"key": "agent.relation", "value": "부", "bbox_2d": [317, 893, 332, 917], "page": 2},
 {"key": "employer.name3", "value": "주식회사 다온패션", "bbox_2d": [321, 916, 498, 945], "page": 2},
 {"key": "agent.birth", "value": "1952.10.28", "bbox_2d": [695, 868, 797, 894], "page": 2},
 {"key": "agent.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [698, 902, 861, 912], "page": 2},
 {"key": "company.ceo3", "value": "남궁예태", "bbox_2d": [700, 916, 790, 942], "page": 2},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [356, 787, 574, 804], "page": 2},
 {"key": "관계사업무위임및관계사ID에대한동의", "value": null}]
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
- check.신청구분: 신청구분 (체크박스, 보기: 신규 / 변경 / 해지)
- check.서비스종류: 서비스종류 (체크박스, 보기: 국내관계사 / 국외관계사)
- check.조회서비스: 조회서비스(위임범위) (체크박스, 보기: 전체 / 부분 / 예금( / 전체 계좌, / 아래에서 지정한 계좌만 조회), / 외환, / 수출입, / 대출, / 전자결제, / 카드, / 지로/공과금)
- check.아이디: 아이디(ID) (같은 항목명 중 1번째 칸, 체크박스, 보기: 실행자 / OTP)
- check.아이디2: 아이디(ID) (같은 항목명 중 2번째 칸, 체크박스, 보기: 실행자 / OTP)
- check.기업뱅킹: 기업뱅킹(통합CMS) (체크박스, 보기: 기업뱅킹(통합CMS) / CMS Plus / CMSiNet)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.지점장: 지점장 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.지점장: 지점장 (같은 항목명 중 2번째 칸, 서명)
- check.주계약사: 주계약사 (체크박스, 보기: 관계사ID에 대한 동의)
- check.관계사: 관계사 (체크박스, 보기: 계좌 사용에 대한 동의 / 관리대상 이용자에 대한 동의)
- check.본인은: 본인은 (체크박스, 보기: OTP를 수령하고 “전자금융거래에 필요한 접근매체(OTP, 인증서 암호,)
```

답:

```json
[{"key": "check.신청구분", "value": "변경", "bbox_2d": [408, 153, 424, 164], "page": 1},
 {"key": "check.서비스종류", "value": "국내관계사", "bbox_2d": [720, 153, 735, 164], "page": 1},
 {"key": "check.조회서비스", "value": null},
 {"key": "check.아이디", "value": "실행자", "bbox_2d": [789, 692, 804, 703], "page": 1},
 {"key": "check.아이디2", "value": "실행자", "bbox_2d": [789, 816, 804, 827], "page": 1},
 {"key": "check.기업뱅킹", "value": "기업뱅킹(통합CMS)", "bbox_2d": [170, 58, 191, 78], "page": 1},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": false},
 {"key": "sign.staff.책임자", "value": false},
 {"key": "seal.staff.지점장", "value": false},
 {"key": "sign.staff.지점장", "value": false},
 {"key": "check.주계약사", "value": null},
 {"key": "check.관계사", "value": "관리대상 이용자에 대한 동의", "bbox_2d": [178, 689, 193, 700], "page": 2},
 {"key": "check.본인은", "value": null}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 '실행자ID*'·'인감/서명' 열이 있는 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 항목명)
- 실행자ID: 실행자ID*
- 통화: 통화
- 계좌번호: 계좌번호
- 인감서명: 인감/서명
```

답:

```json
{
 "columns": [
  "실행자ID",
  "통화",
  "계좌번호",
  "인감서명"
 ],
 "rows": [
  [
   "9095-3941",
   "AUD",
   "731-219372-48636",
   null
  ],
  [
   "123348-3234237",
   "JPY",
   "369-043479-16910",
   null
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    191,
    596,
    451,
    621
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    190,
    619,
    450,
    644
   ],
   "page": 1
  }
 ]
}
```

### 표 찾기 `table_find` · 채점 f1_iou50 (위치)

질문:

```
이 문서에서 표를 모두 찾아 JSON 목록으로 답하세요. 여기서 표는 같은 항목 묶음(열)이 행마다 되풀이되고 행 수가 서류마다 달라지는 목록입니다. 항목명과 값이 번갈아 있는 신청서 칸, 칸 수가 정해진 결재란은 표가 아닙니다.
표마다 {{"columns": [머리글 글자, …], "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호, "n_rows": 행 수}} 를 쓰고, 여러 쪽에 걸친 표는 쪽마다 따로 씁니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 행 수에는 머리글·합계 행과 모두 빈 행을 넣지 않습니다. 표가 없으면 [] 로 답하세요.
```

답:

```json
[{"columns": ["실행자ID*", "통화", "계좌번호", "인감/서명"], "bbox_2d": [190, 596, 451, 644], "page": 1, "n_rows": 2}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '계좌번호'·'인감/서명' 열이 있는 표를 보고 답하세요. '실행자ID*' 칸이 '9095-3941'인 행의 '계좌번호' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"731-219372-48636"
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '계좌번호'·'인감/서명' 열이 있는 표를 보고 답하세요. 표의 행은 모두 몇 개입니까? 머리글·합계 행과 모두 빈 행은 세지 않습니다. (숫자만 답하세요)
```

답:

```json
2
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf346 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf346` → `python -m docgen.formdir card hf346` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf346 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf346 --show` · `python -m docgen.preview hf346 --out work/hf346`
