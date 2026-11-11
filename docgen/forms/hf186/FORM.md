# 퇴직연금_거래신청서(DB) (`hf186`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf186 · card-hash: 0c4ae270d3b0 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 퇴직연금_거래신청서(DB)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf186 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.186 (퇴직연금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 76칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `company.name` | 기업명 | text | 1쪽 [180, 222, 284, 233] | 늘 | 파일 key | 고객 정보 (키 `company.name`, 없으면 값 종류 `company`) | fields.json:58 | 묻기 |
| `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [465, 222, 563, 233] | 늘 | 파일 key | 고객 정보 (키 `company.biz_no`, 없으면 값 종류 `biz_no`) | fields.json:71 | 묻기 |
| `회계결산월` | 회계결산월 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:84 | 묻기 |
| `date` | 제도시행일 | date | 1쪽 [248, 297, 416, 311] | 늘 | 파일 key | 작성일 | fields.json:99 | 묻기 |
| `간사기관` | 간사기관 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:125 | 묻기 |
| `비간사기관` | 비간사기관 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:141 | 묻기 |
| `동의미동의` | 동의󠇧미동의(현금성자산으로운용) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:157 | 묻기 |
| `date2` | 규약수리통보일 | date | 1쪽 [670, 364, 838, 378] | 늘 | 파일 key | 작성일 | fields.json:171 | 묻기 |
| `customer.name` | 이름 | text | 1쪽 [319, 613, 382, 624] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `person`) | fields.json:197 | 묻기 |
| `customer.name2` | 이름 | text | 1쪽 [320, 633, 382, 644] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `person`) | fields.json:210 | 묻기 |
| `customer.phone` | 휴대폰번호 | phone | 1쪽 [321, 653, 425, 664] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:224 | 묻기 |
| `customer.birth` | 생년월일 | number | 1쪽 [674, 613, 726, 624] | 늘 | 파일 key | 고객 정보 (키 `customer.birth`, 없으면 값 종류 `date`) | fields.json:238 | 묻기 |
| `customer.birth2` | 생년월일 | number | 1쪽 [672, 633, 724, 644] | 늘 | 파일 key | 고객 정보 (키 `customer.birth`, 없으면 값 종류 `date`) | fields.json:251 | 묻기 |
| `customer.email` | 이메일주소 | text | 1쪽 [672, 653, 823, 664] | 늘 | 파일 key | 고객 정보 (키 `customer.email`, 없으면 값 종류 `email`) | fields.json:265 | 묻기 |
| `명미만` | 명미만(명)󠇧 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:279 | 묻기 |
| `date3` | 작성일 | date | 1쪽 [712, 195, 922, 209] | 늘 | 파일 key | 작성일 | fields.json:293 | 묻기 |
| `customer.name3` | 성명 | text | 1쪽 [749, 239, 812, 250] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `person`) | fields.json:319 | 묻기 |
| `customer.birth3` | 생년월일 | number | 1쪽 [747, 252, 799, 263] | 늘 | 파일 key | 고객 정보 (키 `customer.birth`, 없으면 값 종류 `date`) | fields.json:332 | 묻기 |
| `customer.name4` | 예금주 | text | 1쪽 [711, 592, 774, 603] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:345 | 묻기 |
| `제도가입이후근무분만` | 제도가입이후근무분만󠇧 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:358 | 묻기 |
| `제도가입이전근무분포함` | 제도가입이전근무분포함󠇧 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:373 | 묻기 |
| `비대상` | 비대상󠇧 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:388 | 묻기 |
| `대상타사가입일자` | 대상(타사가입일자 | date | 1쪽 [784, 400, 864, 411] | 늘 | 파일 key | 값 종류 `date` | fields.json:403 | 묻기 |
| `비대상2` | 비대상󠇧 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:419 | 묻기 |
| `가입자수` | 가입자수 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:434 | 묻기 |
| `signer.name` | 기업명 | text | 2쪽 [460, 868, 564, 879] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:448 | 묻기 |
| `성명` | -성명 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:467 | 묻기 |
| `직원임원촉탁정년초과` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:482 | 묻기 |
| `주민등록번호` | -주민등록번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:497 | 묻기 |
| `입사일중간정산일자` | -입사일:-중간정산일자 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:512 | 묻기 |
| `사원번호이메일` | -사원번호:-이메일:󠇧 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:527 | 묻기 |
| `성명2` | -성명 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:542 | 묻기 |
| `직원임원촉탁정년초과2` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:557 | 묻기 |
| `주민등록번호2` | -주민등록번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:572 | 묻기 |
| `입사일중간정산일자2` | -입사일:-중간정산일자 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:587 | 묻기 |
| `사원번호이메일2` | -사원번호:-이메일:󠇧 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:602 | 묻기 |
| `성명3` | -성명 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:617 | 묻기 |
| `직원임원촉탁정년초과3` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:632 | 묻기 |
| `주민등록번호3` | -주민등록번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:647 | 묻기 |
| `입사일중간정산일자3` | -입사일:-중간정산일자 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:662 | 묻기 |
| `사원번호이메일3` | -사원번호:-이메일:󠇧 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:677 | 묻기 |
| `성명4` | -성명 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:692 | 묻기 |
| `직원임원촉탁정년초과4` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:707 | 묻기 |
| `주민등록번호4` | -주민등록번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:722 | 묻기 |
| `입사일중간정산일자4` | -입사일:-중간정산일자 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:737 | 묻기 |
| `사원번호이메일4` | -사원번호:-이메일:󠇧 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:752 | 묻기 |
| `성명5` | -성명 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:767 | 묻기 |
| `직원임원촉탁정년초과5` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:782 | 묻기 |
| `주민등록번호5` | -주민등록번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:797 | 묻기 |
| `입사일중간정산일자5` | -입사일:-중간정산일자 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:812 | 묻기 |
| `사원번호이메일5` | -사원번호:-이메일:󠇧 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:827 | 묻기 |
| `성명6` | -성명 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:842 | 묻기 |
| `직원임원촉탁정년초과6` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:857 | 묻기 |
| `주민등록번호6` | -주민등록번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:872 | 묻기 |
| `입사일중간정산일자6` | -입사일:-중간정산일자 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:887 | 묻기 |
| `사원번호이메일6` | -사원번호:-이메일:󠇧 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:902 | 묻기 |
| `성명7` | -성명 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:917 | 묻기 |
| `직원임원촉탁정년초과7` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:932 | 묻기 |
| `주민등록번호7` | -주민등록번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:947 | 묻기 |
| `입사일중간정산일자7` | -입사일:-중간정산일자 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:962 | 묻기 |
| `사원번호이메일7` | -사원번호:-이메일:󠇧 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:977 | 묻기 |
| `성명8` | -성명 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:992 | 묻기 |
| `직원임원촉탁정년초과8` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1007 | 묻기 |
| `주민등록번호8` | -주민등록번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:1022 | 묻기 |
| `입사일중간정산일자8` | -입사일:-중간정산일자 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:1037 | 묻기 |
| `사원번호이메일8` | -사원번호:-이메일:󠇧 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:1052 | 묻기 |
| `성명9` | -성명 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:1067 | 묻기 |
| `직원임원촉탁정년초과9` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1082 | 묻기 |
| `주민등록번호9` | -주민등록번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:1097 | 묻기 |
| `입사일중간정산일자9` | -입사일:-중간정산일자 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:1112 | 묻기 |
| `사원번호이메일9` | -사원번호:-이메일:󠇧 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:1127 | 묻기 |
| `성명10` | -성명 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:1142 | 묻기 |
| `직원임원촉탁정년초과10` | 직원󠇧임원󠇧촉탁󠇧정년초과 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1157 | 묻기 |
| `주민등록번호10` | -주민등록번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:1172 | 묻기 |
| `입사일중간정산일자10` | -입사일:-중간정산일자 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:1187 | 묻기 |
| `사원번호이메일10` | -사원번호:-이메일:󠇧 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:1202 | 묻기 |

## 체크·도장·서명 (marks) — 8칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [746, 36, 796, 72] | 늘 | - | - | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [740, 34, 802, 74] | 늘 | - | - | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [802, 34, 871, 74] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [802, 34, 871, 74] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [874, 38, 919, 70] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [871, 34, 922, 74] | 늘 | - | - | - | 묻기 |
| `seal.signer` | 기업명 | seal | 2쪽 [626, 868, 645, 880] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:448 | 묻기 |
| `sign.signer` | 기업명 | signature | 2쪽 [626, 868, 645, 880] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:448 | 묻기 |

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
"퇴직연금_거래신청서(DB)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "(주)미래케미칼",
 "702-81-38348",
 "남궁예태",
 "010-6144-1173",
 "850328",
 "yetae741@gmail.com",
 "2024-06-01"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"850328"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2024-06-01"
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
- company.name: 기업명
- company.biz_no: 사업자등록번호
- date: 제도시행일
- date2: 규약수리통보일
- 대부금액: 대부금액
- customer.name: 이름 (같은 설명 중 1번째 칸)
- customer.name2: 이름 (같은 설명 중 2번째 칸)
- customer.phone: 휴대폰번호
- customer.birth: 생년월일 (같은 설명 중 1번째 칸)
- customer.birth2: 생년월일 (같은 설명 중 2번째 칸)
- customer.email: 이메일주소
- date3: 작성일
- 기발행주식총수: 기발행주식총수
- customer.name3: 성명
- customer.birth3: 생년월일 (같은 설명 중 3번째 칸)
- customer.name4: 예금주
- 대상타사가입일자: 대상(타사가입일자
```

답:

```json
[{"key": "company.name", "value": "(주)미래케미칼", "bbox_2d": [180, 222, 284, 233], "page": 1},
 {"key": "company.biz_no", "value": "702-81-38348", "bbox_2d": [465, 222, 563, 233], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [248, 297, 416, 311], "page": 1},
 {"key": "date2", "value": "2025년 4월 1일", "bbox_2d": [670, 364, 838, 378], "page": 1},
 {"key": "대부금액", "value": null},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [319, 613, 382, 624], "page": 1},
 {"key": "customer.name2", "value": "남궁예태", "bbox_2d": [320, 633, 382, 644], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [321, 653, 425, 664], "page": 1},
 {"key": "customer.birth", "value": "850328", "bbox_2d": [674, 613, 726, 624], "page": 1},
 {"key": "customer.birth2", "value": "850328", "bbox_2d": [672, 633, 724, 644], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [672, 653, 823, 664], "page": 1},
 {"key": "date3", "value": "2025년 4월 1일", "bbox_2d": [712, 195, 922, 209], "page": 1},
 {"key": "기발행주식총수", "value": null},
 {"key": "customer.name3", "value": "남궁예태", "bbox_2d": [749, 239, 812, 250], "page": 1},
 {"key": "customer.birth3", "value": "850328", "bbox_2d": [747, 252, 799, 263], "page": 1},
 {"key": "customer.name4", "value": "남궁예태", "bbox_2d": [711, 592, 774, 603], "page": 1},
 {"key": "대상타사가입일자", "value": "2024-06-01", "bbox_2d": [784, 400, 864, 411], "page": 1}]
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
- seal.staff.본인확인: 본인확인 (같은 설명 중 1번째 칸, 도장)
- sign.staff.본인확인: 본인확인 (같은 설명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 설명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 설명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 설명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.staff.본인확인", "value": true, "bbox_2d": [746, 36, 796, 72], "page": 1},
 {"key": "sign.staff.본인확인", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": true, "bbox_2d": [802, 34, 871, 74], "page": 1},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [874, 38, 919, 70], "page": 1},
 {"key": "sign.staff.책임자", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf186 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf186` → `python -m docgen.formdir card hf186` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf186 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf186 --show` · `python -m docgen.preview hf186 --out work/hf186`
