# 퇴직연금 항목등록/변경 신청서 (`hf194`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf194 · card-hash: a7b1f6f76a16 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 퇴직연금 항목등록/변경 신청서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.194 (퇴직연금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 16칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `customer.name` | 성명(업체명) | text | 1쪽 [216, 130, 300, 152] | 늘 | 규칙: '성명(업체명)' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:49 | 묻기 |
| `account` | 계좌번호 | account_no | 1쪽 [217, 153, 402, 178] | 늘 | 규칙: '계좌번호' → `account` | 고객 정보 (키 `account`) | fields.json:60 | 묻기 |
| `customer.birth` | 생년월일(사업자번호) | date | 1쪽 [611, 130, 709, 152] | 늘 | 규칙: '생년월일(사업자번호)' → `customer.birth` | 고객 정보 (키 `customer.birth`) | fields.json:72 | 묻기 |
| `변경전` | 변경전 | text | 1쪽 [79, 495, 170, 518] | 늘 | 표 행 (묶음·항목명 '변경 전') | 값 종류 `note` (항목명 자동) | fields.json:160 | 묻기 |
| `변경후` | 변경후 | text | 1쪽 [513, 496, 604, 518] | 늘 | 표 행 (묶음·항목명 '변경 후') | 값 종류 `note` (항목명 자동) | fields.json:650 | 묻기 |
| `customer.name2` | 성명 | text | 1쪽 [457, 616, 541, 638] | 늘 | 규칙: '성명' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:707 | 묻기 |
| `customer.birth2` | 생년월일 | date | 1쪽 [758, 615, 856, 638] | 늘 | 규칙: '생년월일' → `customer.birth` | 고객 정보 (키 `customer.birth`) | fields.json:718 | 묻기 |
| `customer.name3` | 성명 | text | 1쪽 [219, 710, 303, 734] | 늘 | 규칙: '성명' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:790 | 묻기 |
| `customer.phone` | 휴대폰번호 | phone | 1쪽 [216, 733, 371, 757] | 늘 | 규칙: '휴대폰번호' → `customer.phone` | 고객 정보 (키 `customer.phone`) | fields.json:801 | 묻기 |
| `customer.birth3` | 생년월일 | date | 1쪽 [612, 712, 711, 735] | 늘 | 규칙: '생년월일' → `customer.birth` | 고객 정보 (키 `customer.birth`) | fields.json:873 | 묻기 |
| `customer.email` | 이메일주소 | text | 1쪽 [613, 735, 816, 758] | 늘 | 규칙: '이메일주소' → `customer.email` | 고객 정보 (키 `customer.email`) | fields.json:884 | 묻기 |
| `기업담당자성명` | 기업담당자성명 | text | 1쪽 [182, 806, 247, 830] | 늘 | 항목명 그대로 | 값 종류 `person` (항목명 자동) | fields.json:895 | 묻기 |
| `기업담당자휴대폰번호` | 기업담당자휴대폰번호 | phone | 1쪽 [459, 805, 613, 829] | 늘 | 항목명 그대로 | 값 종류 `phone` (항목명 자동) | fields.json:906 | 묻기 |
| `근로자앞문자발송요청일` | 근로자앞문자발송요청일 | date | 1쪽 [763, 808, 908, 828] | 늘 | 항목명 그대로 | 값 종류 `date` (항목명 자동) | fields.json:917 | 묻기 |
| `date` | 작성일 | date | 1쪽 [356, 847, 557, 864] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:928 | 묻기 |
| `signer.name` | 신청인 | text | 1쪽 [472, 890, 556, 913] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:953 | 묻기 |

## 체크·도장·서명 (marks) — 16칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.제도구분` | 제도구분 | checkbox (DB / DC / 기업형IRP / 개인형IRP) | 1쪽 [676, 157, 715, 172] | 늘 | 체크 (항목명) | 보기 중 고름: DB / DC / 기업형IRP / 개인형IRP | fields.json:83 | 묻기 |
| `check.구분` | 구분 | checkbox (등록 / 변경 / 해제) | 1쪽 [235, 211, 281, 226] | 늘 | 체크 (항목명) | 보기 중 고름: 등록 / 변경 / 해제 | fields.json:172 | 묻기 |
| `check.공통사항` | 공통사항 | checkbox (사업자번호 변경 / 기업반환계좌 변경 / 부담금 납입주기 변경 / 기업담당자 변경(추가항목 필수 기재) / 신탁관리인 변경(추가항목 필수 기재) / 거래인감 변경(거래인감통보서 필수 징구) / 장기할인수수료 적용 / 수수료 감면대상 등록 / 비대면 규약 동의 신청 / 기타 () | 1쪽 [604, 265, 750, 280] | 늘 | 체크 (항목명) | 보기 중 고름: 사업자번호 변경 / 기업반환계좌 변경 / 부담금 납입주기 변경 / 기업담당자 변경(추가항목 필수 기재) / 신탁관리인 변경(추가항목 필수 기재) / 거래인감 변경(거래인감통보서 필수 징구) / 장기할인수수료 적용 / 수수료 감면대상 등록 / 비대면 규약 동의 신청 / 기타 ( | fields.json:233 | 묻기 |
| `check.DB` | DB | checkbox (대체상품 매수 동의) | 1쪽 [294, 321, 436, 336] | 늘 | 체크 (항목명) | 보기 중 고름: 대체상품 매수 동의 | fields.json:406 | 묻기 |
| `check.DC기업형IRP` | DC/기업형IRP | checkbox (임금총액 등록 / 운용상품군(자동라인업)등록 / 표준형DC 등록 / 비대면 DC가입신청 명부 등록) | 1쪽 [294, 346, 698, 376] | 늘 | 체크 (항목명) | 보기 중 고름: 임금총액 등록 / 운용상품군(자동라인업)등록 / 표준형DC 등록 / 비대면 DC가입신청 명부 등록 | fields.json:435 | 묻기 |
| `check.공통사항2` | 공통사항 | checkbox (고객정보 통합관리 동의 / 퇴직연금정보 제3수령처 등록 / 연간납입한도 주1 / 만기 안내 수신여부(택 1) ○이메일 ○알림톡(LMS) ○수신거부 / 기타 () | 1쪽 [294, 418, 349, 433] | 늘 | 체크 (항목명) | 보기 중 고름: 고객정보 통합관리 동의 / 퇴직연금정보 제3수령처 등록 / 연간납입한도 주1 / 만기 안내 수신여부(택 1) ○이메일 ○알림톡(LMS) ○수신거부 / 기타 ( | fields.json:512 | 묻기 |
| `check.개인형IRP` | 개인형IRP | checkbox (개인형IRP 속성 변경 / 가입자격등록(인터넷)) | 1쪽 [294, 443, 440, 458] | 늘 | 체크 (항목명) | 보기 중 고름: 개인형IRP 속성 변경 / 가입자격등록(인터넷) | fields.json:605 | 묻기 |
| `check.구분2` | 구분 | checkbox (등록 / 변경) | 1쪽 [256, 619, 306, 634] | 늘 | 체크 (항목명) | 보기 중 고름: 등록 / 변경 | fields.json:662 | 묻기 |
| `check.신청구분` | 신청구분 | checkbox (등록 / 변경 / 해제) | 1쪽 [219, 691, 266, 706] | 늘 | 체크 (항목명) | 보기 중 고름: 등록 / 변경 / 해제 | fields.json:729 | 묻기 |
| `check.담당자구분` | 담당자구분 | checkbox (주담당자 / 부담당자 / 보고서담당자) | 1쪽 [809, 691, 910, 706] | 늘 | 체크 (항목명) | 보기 중 고름: 주담당자 / 부담당자 / 보고서담당자 | fields.json:812 | 묻기 |
| `seal.customer` ← `seal.signer` | 신청인 | seal | 1쪽 [626, 884, 660, 920] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:953 | 묻기 |
| `sign.customer` ← `sign.signer` | 신청인 | signature | 1쪽 [631, 895, 655, 909] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:953 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [783, 40, 847, 77] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [783, 40, 847, 77] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [862, 43, 907, 74] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [847, 40, 922, 77] | 늘 | - | - | - | 묻기 |

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
"퇴직연금 항목등록/변경 신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "남궁예태",
 "540-121210-96628",
 "1985.03.28",
 "해당 없음",
 "010-6144-1173",
 "yetae741@gmail.com",
 "표채예",
 "2024년 8월 14일"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"표채예"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2024년 8월 14일"
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
- customer.name: 성명(업체명) (고객 성명)
- account: 계좌번호
- customer.birth: 생년월일(사업자번호) (고객 생년월일)
- 변경전: 변경전
- 변경후: 변경후
- customer.name2: 성명 (같은 항목명 중 1번째 칸)
- customer.birth2: 생년월일 (같은 항목명 중 1번째 칸)
- customer.name3: 성명 (같은 항목명 중 2번째 칸)
- customer.phone: 휴대폰번호 (고객 연락처)
- customer.birth3: 생년월일 (같은 항목명 중 2번째 칸)
- customer.email: 이메일주소 (고객 이메일)
- 기업담당자성명: 기업담당자성명
- 기업담당자휴대폰번호: 기업담당자휴대폰번호
- 근로자앞문자발송요청일: 근로자앞문자발송요청일
- date: 작성일
- signer.name: 신청인 (고객 본인의 성명)
```

답:

```json
[{"key": "customer.name", "value": "남궁예태", "bbox_2d": [216, 130, 300, 152], "page": 1},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [217, 153, 402, 178], "page": 1},
 {"key": "customer.birth", "value": "1985.03.28", "bbox_2d": [611, 130, 709, 152], "page": 1},
 {"key": "변경전", "value": "해당 없음", "bbox_2d": [79, 495, 170, 518], "page": 1},
 {"key": "변경후", "value": "해당 없음", "bbox_2d": [513, 496, 604, 518], "page": 1},
 {"key": "customer.name2", "value": "남궁예태", "bbox_2d": [457, 616, 541, 638], "page": 1},
 {"key": "customer.birth2", "value": "1985.03.28", "bbox_2d": [758, 615, 856, 638], "page": 1},
 {"key": "customer.name3", "value": "남궁예태", "bbox_2d": [219, 710, 303, 734], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [216, 733, 371, 757], "page": 1},
 {"key": "customer.birth3", "value": "1985.03.28", "bbox_2d": [612, 712, 711, 735], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [613, 735, 816, 758], "page": 1},
 {"key": "기업담당자성명", "value": "표채예", "bbox_2d": [182, 806, 247, 830], "page": 1},
 {"key": "기업담당자휴대폰번호", "value": "010-6144-1173", "bbox_2d": [459, 805, 613, 829], "page": 1},
 {"key": "근로자앞문자발송요청일", "value": "2024년 8월 14일", "bbox_2d": [763, 808, 908, 828], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [356, 847, 557, 864], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [472, 890, 556, 913], "page": 1}]
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
- check.제도구분: 제도구분 (체크박스, 보기: DB / DC / 기업형IRP / 개인형IRP)
- check.구분: 구분 (같은 항목명 중 1번째 칸, 체크박스, 보기: 등록 / 변경 / 해제)
- check.공통사항: 공통사항 (같은 항목명 중 1번째 칸, 체크박스, 보기: 사업자번호 변경 / 기업반환계좌 변경 / 부담금 납입주기 변경 / 기업담당자 변경(추가항목 필수 기재) / 신탁관리인 변경(추가항목 필수 기재) / 거래인감 변경(거래인감통보서 필수 징구) / 장기할인수수료 적용 / 수수료 감면대상 등록 / 비대면 규약 동의 신청 / 기타 ()
- check.DB: DB (체크박스, 보기: 대체상품 매수 동의)
- check.DC기업형IRP: DC/기업형IRP (체크박스, 보기: 임금총액 등록 / 운용상품군(자동라인업)등록 / 표준형DC 등록 / 비대면 DC가입신청 명부 등록)
- check.공통사항2: 공통사항 (같은 항목명 중 2번째 칸, 체크박스, 보기: 고객정보 통합관리 동의 / 퇴직연금정보 제3수령처 등록 / 연간납입한도 주1 / 만기 안내 수신여부(택 1) ○이메일 ○알림톡(LMS) ○수신거부 / 기타 ()
- check.개인형IRP: 개인형IRP (체크박스, 보기: 개인형IRP 속성 변경 / 가입자격등록(인터넷))
- check.구분2: 구분 (같은 항목명 중 2번째 칸, 체크박스, 보기: 등록 / 변경)
- check.신청구분: 신청구분 (체크박스, 보기: 등록 / 변경 / 해제)
- check.담당자구분: 담당자구분 (체크박스, 보기: 주담당자 / 부담당자 / 보고서담당자)
- seal.customer: 신청인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 신청인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.제도구분", "value": "DC", "bbox_2d": [676, 158, 690, 172], "page": 1},
 {"key": "check.구분", "value": "변경", "bbox_2d": [235, 212, 249, 226], "page": 1},
 {"key": "check.공통사항", "value": "장기할인수수료 적용", "bbox_2d": [604, 266, 618, 280], "page": 1},
 {"key": "check.DB", "value": null},
 {"key": "check.DC기업형IRP", "value": null},
 {"key": "check.공통사항2", "value": "기타 (", "bbox_2d": [294, 419, 308, 433], "page": 1},
 {"key": "check.개인형IRP", "value": "개인형IRP 속성 변경", "bbox_2d": [294, 444, 308, 458], "page": 1},
 {"key": "check.구분2", "value": "변경", "bbox_2d": [256, 620, 270, 634], "page": 1},
 {"key": "check.신청구분", "value": "등록", "bbox_2d": [219, 692, 233, 706], "page": 1},
 {"key": "check.담당자구분", "value": "보고서담당자", "bbox_2d": [809, 692, 823, 706], "page": 1},
 {"key": "seal.customer", "value": true, "bbox_2d": [626, 884, 660, 920], "page": 1},
 {"key": "sign.customer", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": true, "bbox_2d": [783, 40, 847, 77], "page": 1},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [862, 43, 907, 74], "page": 1},
 {"key": "sign.staff.책임자", "value": false}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf194` → `python -m docgen.formdir card hf194` (실제 질문→답 확인).

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
| 답 모양 | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf194 --show` · `python -m docgen.preview hf194 --out work/hf194`
