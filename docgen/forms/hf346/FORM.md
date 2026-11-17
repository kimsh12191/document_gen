# 기업관계사 서비스 이용신청서 (`hf346`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf346 · card-hash: 9f10b52096f3 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 3 (seed 1000000 로 그린 것) · **분류 정답:** 기업관계사 서비스 이용신청서
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
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 23칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `company.corp_no` | 법인등록번호 | corp_reg_no | 1쪽 [320, 170, 472, 194] | 늘 | 파일 key | 고객 정보 (키 `company.corp_no`, 없으면 값 종류 `number`) | fields.json:120 | 묻기 |
| `employer.name` | 회사명 | text | 1쪽 [322, 193, 499, 220] | 늘 | 파일 key | 고객 정보 (키 `employer.name`, 없으면 값 종류 `company`) | fields.json:134 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [323, 216, 735, 243] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:148 | 묻기 |
| `company.corp_no2` | 법인등록번호 | rrn | 1쪽 [320, 238, 474, 266] | 늘 | 파일 key | 고객 정보 (키 `company.corp_no`, 없으면 값 종류 `number`) | fields.json:162 | 묻기 |
| `거래은행영업점` | 거래은행/영업점 | text | 1쪽 [321, 264, 399, 289] | 늘 | 파일 key | 값 종류 `bank` | fields.json:176 | 묻기 |
| `employer.name2` | 회사명 | text | 1쪽 [320, 287, 496, 312] | 늘 | 파일 key | 고객 정보 (키 `employer.name`, 없으면 값 종류 `company`) | fields.json:192 | 묻기 |
| `customer.address2` | 주소 | text | 1쪽 [316, 306, 727, 340] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:206 | 묻기 |
| `customer.phone` | 전화번호 | phone | 1쪽 [323, 335, 461, 361] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:220 | 묻기 |
| `customer.email` | e-mail | text | 1쪽 [324, 356, 552, 386] | 늘 | 파일 key | 고객 정보 (키 `customer.email`, 없으면 값 종류 `text`) | fields.json:234 | 묻기 |
| `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [706, 170, 842, 194] | 늘 | 파일 key | 고객 정보 (키 `company.biz_no`, 없으면 값 종류 `biz_no`) | fields.json:295 | 묻기 |
| `company.ceo` | 대표자 | text | 1쪽 [699, 193, 789, 217] | 늘 | 파일 key | 고객 정보 (키 `company.ceo`, 없으면 값 종류 `text`) | fields.json:309 | 묻기 |
| `company.biz_no2` | 사업자등록번호 | biz_no | 1쪽 [699, 240, 837, 267] | 늘 | 파일 key | 고객 정보 (키 `company.biz_no`, 없으면 값 종류 `biz_no`) | fields.json:323 | 묻기 |
| `글로벌고객번호` | 글로벌고객번호 | rrn | 1쪽 [699, 264, 870, 289] | 늘 | 파일 key | 값 종류 `number` | fields.json:337 | 묻기 |
| `company.ceo2` | 대표자 | text | 1쪽 [702, 287, 791, 312] | 늘 | 파일 key | 고객 정보 (키 `company.ceo`, 없으면 값 종류 `text`) | fields.json:353 | 묻기 |
| `Fax` | Fax | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:367 | 묻기 |
| `agent.name` | 성명 | text | 2쪽 [320, 871, 394, 895] | 늘 | 파일 key | 고객 정보 (키 `agent.name`, 없으면 값 종류 `person`) | fields.json:992 | 묻기 |
| `agent.relation` | 관계 | text | 2쪽 [321, 895, 336, 919] | 늘 | 파일 key | 고객 정보 (키 `agent.relation`, 없으면 값 종류 `text`) | fields.json:1006 | 묻기 |
| `employer.name3` | 회사명 | text | 2쪽 [321, 918, 497, 942] | 늘 | 파일 key | 고객 정보 (키 `employer.name`, 없으면 값 종류 `company`) | fields.json:1020 | 묻기 |
| `agent.birth` | 생년월일 | date | 2쪽 [698, 870, 799, 894] | 늘 | 파일 key | 고객 정보 (키 `agent.birth`, 없으면 값 종류 `date`) | fields.json:1033 | 묻기 |
| `agent.address` | 주소 | text | 2쪽 [696, 902, 859, 913] | 늘 | 파일 key | 고객 정보 (키 `agent.address`, 없으면 값 종류 `address`) | fields.json:1047 | 묻기 |
| `company.ceo3` | 대표자 | text | 2쪽 [694, 917, 784, 943] | 늘 | 파일 key | 고객 정보 (키 `company.ceo`, 없으면 값 종류 `text`) | fields.json:1061 | 묻기 |
| `date` | 작성일 | date | 2쪽 [356, 787, 574, 804] | 늘 | 파일 key | 작성일 | fields.json:1099 | 묻기 |
| `관계사업무위임및관계사ID에대한동의` | ■관계사업무위임및관계사ID에대한동의 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:1125 | 묻기 |

## 표 `목록` (표 과제 table·table_read·table_find·table_qa) — 4열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `목록.*.실행자ID` | 실행자ID* | text | 1쪽 [191, 602, 244, 615] (1행) | 늘 | 파일 key | 값 종류 `number` | fields.json:664 | 묻기 |
| `목록.*.통화` | 통화 | text | 1쪽 [260, 596, 304, 621] (1행) | 늘 | 파일 key | 값 종류 `currency` | fields.json:692 | 묻기 |
| `목록.*.계좌번호` | 계좌번호 | text | 1쪽 [321, 598, 451, 618] (1행) | 늘 | 파일 key | 값 종류 `account` | fields.json:720 | 묻기 |
| `목록.*.인감서명` | 인감/서명 | text | - (1행) | 늘 | 파일 key | 값 종류 `seal` | fields.json:748 | 묻기 |

## 체크·도장·서명 (marks) — 15칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.신청구분` | 신청구분 | checkbox (신규 / 변경 / 해지) | 1쪽 [408, 152, 454, 164] | 늘 | 파일 key | 보기 중 고름: 신규 / 변경 / 해지 | fields.json:58 | 묻기 |
| `check.서비스종류` | 서비스종류 | checkbox (국내관계사 / 국외관계사) | 1쪽 [720, 152, 804, 164] | 늘 | 파일 key | 보기 중 고름: 국내관계사 / 국외관계사 | fields.json:249 | 묻기 |
| `check.조회서비스` | 조회서비스(위임범위) | checkbox (전체 / 부분 / 예금( / 전체 계좌, / 아래에서 지정한 계좌만 조회), / 외환, / 수출입, / 대출, / 전자결제, / 카드, / 지로/공과금) | 1쪽 [181, 426, 912, 454] | 늘 | 파일 key | 보기 중 고름: 전체 / 부분 / 예금( / 전체 계좌, / 아래에서 지정한 계좌만 조회), / 외환, / 수출입, / 대출, / 전자결제, / 카드, / 지로/공과금 | fields.json:382 | 묻기 |
| `check.아이디` | 아이디(ID) | checkbox (실행자 / OTP) | 1쪽 [789, 691, 847, 703] | 늘 | 파일 key | 보기 중 고름: 실행자 / OTP | fields.json:572 | 묻기 |
| `check.아이디2` | 아이디(ID) | checkbox (실행자 / OTP) | 1쪽 [789, 814, 847, 827] | 늘 | 파일 key | 보기 중 고름: 실행자 / OTP | fields.json:618 | 묻기 |
| `check.기업뱅킹` | 기업뱅킹(통합CMS) | checkbox (기업뱅킹(통합CMS) / CMS Plus / CMSiNet) | 1쪽 [170, 57, 629, 78] | 늘 | 파일 key | 보기 중 고름: 기업뱅킹(통합CMS) / CMS Plus / CMSiNet | fields.json:860 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [728, 34, 794, 75] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [728, 34, 794, 75] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [794, 34, 870, 75] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [794, 34, 870, 75] | 늘 | - | - | - | 묻기 |
| `seal.staff.지점장` | 지점장 | seal | 1쪽 [875, 40, 915, 68] | 늘 | - | - | - | 묻기 |
| `sign.staff.지점장` | 지점장 | signature | 1쪽 [870, 34, 920, 75] | 늘 | - | - | - | 묻기 |
| `check.주계약사` | 주계약사 | checkbox (관계사ID에 대한 동의) | 2쪽 [178, 548, 319, 561] | 늘 | 파일 key | 보기 중 고름: 관계사ID에 대한 동의 | fields.json:916 | 묻기 |
| `check.관계사` | 관계사 | checkbox (계좌 사용에 대한 동의 / 관리대상 이용자에 대한 동의) | 2쪽 [178, 602, 324, 615] | 늘 | 파일 key | 보기 중 고름: 계좌 사용에 대한 동의 / 관리대상 이용자에 대한 동의 | fields.json:946 | 묻기 |
| `check.본인은` | 본인은 | checkbox (OTP를 수령하고 “전자금융거래에 필요한 접근매체(OTP, 인증서 암호,) | 2쪽 [112, 739, 928, 752] | 늘 | 파일 key | 보기 중 고름: OTP를 수령하고 “전자금융거래에 필요한 접근매체(OTP, 인증서 암호, | fields.json:1075 | 묻기 |

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
 "USD",
 "183-443612-61625",
 "055-537466-39751",
 "남궁찬윤",
 "부",
 "1952.10.28",
 "823512-8308612",
 "513-100088-99844",
 "4723-0599",
 "146-749815-07387",
 "139-831026-73766",
 "686-822047-72822",
 "0576-1987",
 "547-690912-79142",
 "0003-0504",
 "EUR",
 "436-483479-57420"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"9095-3941"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"139-831026-73766"
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
- company.corp_no: 법인등록번호 (같은 설명 중 1번째 칸)
- employer.name: 회사명 (같은 설명 중 1번째 칸)
- customer.address: 주소 (같은 설명 중 1번째 칸)
- company.corp_no2: 법인등록번호 (같은 설명 중 2번째 칸)
- 거래은행영업점: 거래은행/영업점
- employer.name2: 회사명 (같은 설명 중 2번째 칸)
- customer.address2: 주소 (같은 설명 중 2번째 칸)
- customer.phone: 전화번호
- customer.email: e-mail
- company.biz_no: 사업자등록번호 (같은 설명 중 1번째 칸)
- company.ceo: 대표자 (같은 설명 중 1번째 칸)
- company.biz_no2: 사업자등록번호 (같은 설명 중 2번째 칸)
- 글로벌고객번호: 글로벌고객번호
- company.ceo2: 대표자 (같은 설명 중 2번째 칸)
- Fax: Fax
- agent.name: 성명
- agent.relation: 관계
- employer.name3: 회사명 (같은 설명 중 3번째 칸)
- agent.birth: 생년월일
- agent.address: 주소 (같은 설명 중 3번째 칸)
- company.ceo3: 대표자 (같은 설명 중 3번째 칸)
- date: 작성일
- 관계사업무위임및관계사ID에대한동의: ■관계사업무위임및관계사ID에대한동의
```

답:

```json
[{"key": "company.corp_no", "value": "200112-7951835", "bbox_2d": [320, 170, 472, 194], "page": 1},
 {"key": "employer.name", "value": "주식회사 다온패션", "bbox_2d": [322, 193, 499, 220], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [323, 216, 735, 243], "page": 1},
 {"key": "company.corp_no2", "value": "200112-7951835", "bbox_2d": [320, 238, 474, 266], "page": 1},
 {"key": "거래은행영업점", "value": "농협은행", "bbox_2d": [321, 264, 399, 289], "page": 1},
 {"key": "employer.name2", "value": "주식회사 다온패션", "bbox_2d": [320, 287, 496, 312], "page": 1},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [316, 306, 727, 340], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [323, 335, 461, 361], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [324, 356, 552, 386], "page": 1},
 {"key": "company.biz_no", "value": "702-81-38348", "bbox_2d": [706, 170, 842, 194], "page": 1},
 {"key": "company.ceo", "value": "남궁예태", "bbox_2d": [699, 193, 789, 217], "page": 1},
 {"key": "company.biz_no2", "value": "702-81-38348", "bbox_2d": [699, 240, 837, 267], "page": 1},
 {"key": "글로벌고객번호", "value": "539946-6934759", "bbox_2d": [699, 264, 870, 289], "page": 1},
 {"key": "company.ceo2", "value": "남궁예태", "bbox_2d": [702, 287, 791, 312], "page": 1},
 {"key": "Fax", "value": null},
 {"key": "agent.name", "value": "남궁찬윤", "bbox_2d": [320, 871, 394, 895], "page": 2},
 {"key": "agent.relation", "value": "부", "bbox_2d": [321, 895, 336, 919], "page": 2},
 {"key": "employer.name3", "value": "주식회사 다온패션", "bbox_2d": [321, 918, 497, 942], "page": 2},
 {"key": "agent.birth", "value": "1952.10.28", "bbox_2d": [698, 870, 799, 894], "page": 2},
 {"key": "agent.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [696, 902, 859, 913], "page": 2},
 {"key": "company.ceo3", "value": "남궁예태", "bbox_2d": [694, 917, 784, 943], "page": 2},
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
- check.아이디: 아이디(ID) (같은 설명 중 1번째 칸, 체크박스, 보기: 실행자 / OTP)
- check.아이디2: 아이디(ID) (같은 설명 중 2번째 칸, 체크박스, 보기: 실행자 / OTP)
- check.기업뱅킹: 기업뱅킹(통합CMS) (체크박스, 보기: 기업뱅킹(통합CMS) / CMS Plus / CMSiNet)
- seal.staff.담당: 담당 (같은 설명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 설명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 설명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 설명 중 2번째 칸, 서명)
- seal.staff.지점장: 지점장 (같은 설명 중 1번째 칸, 도장)
- sign.staff.지점장: 지점장 (같은 설명 중 2번째 칸, 서명)
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
 {"key": "check.기업뱅킹", "value": null},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": true, "bbox_2d": [728, 34, 794, 75], "page": 1},
 {"key": "seal.staff.책임자", "value": false},
 {"key": "sign.staff.책임자", "value": true, "bbox_2d": [794, 34, 870, 75], "page": 1},
 {"key": "seal.staff.지점장", "value": true, "bbox_2d": [875, 40, 915, 68], "page": 1},
 {"key": "sign.staff.지점장", "value": false},
 {"key": "check.주계약사", "value": "관계사ID에 대한 동의", "bbox_2d": [178, 550, 193, 561], "page": 2},
 {"key": "check.관계사", "value": "계좌 사용에 대한 동의", "bbox_2d": [178, 604, 193, 615], "page": 2},
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
열 (키: 설명)
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
   null,
   "USD",
   "183-443612-61625",
   null
  ],
  [
   "123348-3234237",
   "JPY",
   "369-043479-16910",
   null
  ],
  [
   null,
   "USD",
   "055-537466-39751",
   null
  ],
  [
   "823512-8308612",
   "USD",
   "513-100088-99844",
   null
  ],
  [
   "4723-0599",
   "JPY",
   "146-749815-07387",
   null
  ],
  [
   "139-831026-73766",
   "USD",
   "686-822047-72822",
   null
  ],
  [
   "0576-1987",
   "USD",
   "547-690912-79142",
   null
  ],
  [
   "0003-0504",
   "EUR",
   "436-483479-57420",
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
    594,
    596,
    777,
    620
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
  },
  {
   "bbox_2d": [
    595,
    620,
    786,
    644
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    132,
    168,
    553,
    179
   ],
   "page": 3
  },
  {
   "bbox_2d": [
    132,
    192,
    552,
    202
   ],
   "page": 3
  },
  {
   "bbox_2d": [
    132,
    215,
    557,
    225
   ],
   "page": 3
  },
  {
   "bbox_2d": [
    132,
    238,
    555,
    249
   ],
   "page": 3
  },
  {
   "bbox_2d": [
    132,
    261,
    560,
    272
   ],
   "page": 3
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
[{"columns": ["실행자ID*", "통화", "계좌번호", "인감/서명"], "bbox_2d": [190, 596, 786, 644], "page": 1, "n_rows": 4},
 {"columns": ["실행자ID*", "통화", "계좌번호", "인감/서명"], "bbox_2d": [124, 138, 923, 272], "page": 3, "n_rows": 5}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '계좌번호'·'인감/서명' 열이 있는 표를 보고 답하세요. '통화' 칸이 'AUD'인 행은 몇 개입니까? (숫자만 답하세요)
```

답:

```json
1
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '계좌번호'·'인감/서명' 열이 있는 표를 보고 답하세요. 위에서 1번째 행의 '통화' 값은 무엇입니까? 머리글은 세지 않습니다. (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"AUD"
```

### 표 그대로 옮기기 `table_read` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 '통화'·'계좌번호' 열이 있는 표를 머리글까지 그대로 옮겨 JSON 으로 답하세요.
꼴: {"columns": [머리글 글자, …], "rows": [[칸 글자, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 표의 머리글을 왼쪽부터 쓰고, 머리글이 여러 줄이면 위 칸과 아래 칸 글자를 " > " 로 잇습니다.
- rows 는 행마다 columns 와 같은 순서로 칸 글자를 씁니다. 빈 칸은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 글자를 씁니다.
- 다음 쪽에서 다시 나온 머리글 행과 모두 빈 행은 빼고, 합계·소계 행은 그대로 둡니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
```

답:

```json
{
 "columns": [
  "번호",
  "실행자ID*",
  "통화",
  "계좌번호",
  "인감/서명"
 ],
 "rows": [
  [
   "5",
   "823512-8308612",
   "USD",
   "513-100088-99844",
   null
  ],
  [
   "6",
   "4723-0599",
   "JPY",
   "146-749815-07387",
   null
  ],
  [
   "7",
   "139-831026-73766",
   "USD",
   "686-822047-72822",
   null
  ],
  [
   "8",
   "0576-1987",
   "USD",
   "547-690912-79142",
   null
  ],
  [
   "9",
   "0003-0504",
   "EUR",
   "436-483479-57420",
   null
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    76,
    163,
    923,
    186
   ],
   "page": 3
  },
  {
   "bbox_2d": [
    76,
    186,
    923,
    209
   ],
   "page": 3
  },
  {
   "bbox_2d": [
    76,
    209,
    923,
    232
   ],
   "page": 3
  },
  {
   "bbox_2d": [
    76,
    232,
    923,
    255
   ],
   "page": 3
  },
  {
   "bbox_2d": [
    76,
    255,
    923,
    279
   ],
   "page": 3
  }
 ]
}
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
| 답의 키 | `fields.json` 그 칸에 `"key"` (없으면 키 설명이 그대로 키) | 다시 |
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
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf346 --show` · `python -m docgen.preview hf346 --out work/hf346`
