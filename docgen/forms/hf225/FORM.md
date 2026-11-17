# Usance 송금 신청서 (`hf225`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf225 · card-hash: 76ab55b8ab48 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** Usance 송금 신청서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf225 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.225 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 34칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `신청정보` | ♣신청정보 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:43 | 묻기 |
| `신청인정보` | ♣신청인정보 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:57 | 묻기 |
| `영문` | 영문(English) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:71 | 묻기 |
| `한글` | 한글(Korean) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:85 | 묻기 |
| `선적정보` | ♣선적정보 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:253 | 묻기 |
| `계약서번호` | 계약서번호 | text | 1쪽 [291, 505, 454, 524] | 늘 | 파일 key | 값 종류 `number` | fields.json:267 | 묻기 |
| `상품명세` | 상품명세 | text | 1쪽 [293, 528, 426, 547] | 늘 | 파일 key | 값 종류 `product` | fields.json:281 | 묻기 |
| `가격조건` | 가격조건 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:295 | 묻기 |
| `원산지` | 원산지 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:309 | 묻기 |
| `운송서류번호사후송금방식인경우작성` | 운송서류번호(B/LNo등)*사후송금방식인경우작성 | text | 1쪽 [293, 600, 381, 619] | 늘 | 파일 key | 값 종류 `number` | fields.json:323 | 묻기 |
| `선적항` | (예정)선적항(또는공항) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:337 | 묻기 |
| `도착항` | (예정)도착항(또는공항) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:351 | 묻기 |
| `HS코드` | HS코드 | number | 1쪽 [725, 552, 793, 570] | 늘 | 파일 key | 값 종류 `number` | fields.json:365 | 묻기 |
| `수출국` | 수출국 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:379 | 묻기 |
| `date` | 선적(예정)일 | date | 1쪽 [729, 601, 913, 618] | 늘 | 파일 key | 작성일 | fields.json:393 | 묻기 |
| `선적국가` | 선적국가 | text | 1쪽 [726, 626, 766, 644] | 늘 | 파일 key | 값 종류 `country` | fields.json:419 | 묻기 |
| `도착국가` | 도착국가 | text | 1쪽 [724, 651, 763, 669] | 늘 | 파일 key | 값 종류 `country` | fields.json:433 | 묻기 |
| `수취인명` | 수취인명 | text | 1쪽 [292, 701, 423, 719] | 늘 | 파일 key | 값 종류 `company` | fields.json:447 | 묻기 |
| `수취인주소및전화번호` | 수취인주소및전화번호 | phone | 1쪽 [293, 722, 415, 742] | 늘 | 파일 key | 값 종류 `phone` | fields.json:461 | 묻기 |
| `수취인주소및전화번호2` | 수취인주소및전화번호 | phone | 1쪽 [295, 746, 416, 766] | 늘 | 파일 key | 값 종류 `phone` | fields.json:475 | 묻기 |
| `수취인계좌번호` | 수취인계좌번호 | text | 1쪽 [289, 769, 461, 790] | 늘 | 파일 key | 값 종류 `account` | fields.json:489 | 묻기 |
| `수취은행BIC` | 수취은행BIC | text | 1쪽 [291, 797, 390, 814] | 늘 | 파일 key | 값 종류 `bank` | fields.json:503 | 묻기 |
| `송금수취인및수취은행정보` | ♣송금수취인및수취은행정보 | text | 1쪽 [295, 679, 370, 697] | 늘 | 파일 key | 값 종류 `bank` | fields.json:517 | 묻기 |
| `수취은행명` | 수취은행명 | text | 1쪽 [723, 794, 821, 812] | 늘 | 파일 key | 값 종류 `bank` | fields.json:577 | 묻기 |
| `담당자명` | 담당자명 | text | 1쪽 [293, 844, 373, 864] | 늘 | 파일 key | 값 종류 `person` | fields.json:591 | 묻기 |
| `customer.phone` | 전화번호 | phone | 1쪽 [291, 869, 412, 889] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:605 | 묻기 |
| `TELNo` | TELNo | rrn | 1쪽 [672, 283, 781, 298] | 늘 | 파일 key | 값 종류 `number` | fields.json:618 | 묻기 |
| `customer.email` | E-mail | text | 1쪽 [672, 301, 848, 320] | 늘 | 파일 key | 고객 정보 (키 `customer.email`, 없으면 값 종류 `email`) | fields.json:632 | 묻기 |
| `통화금액` | 통화(),금액 | number | 1쪽 [496, 354, 573, 373] | 늘 | 파일 key | 값 종류 `amount` | fields.json:645 | 묻기 |
| `date2` | 작성일 | date | 1쪽 [265, 406, 433, 423] | 늘 | 파일 key | 작성일 | fields.json:659 | 묻기 |
| `SWIFTCode` | SWIFTCode | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:685 | 묻기 |
| `date3` | 작성일 | date | 1쪽 [339, 926, 553, 943] | 늘 | 파일 key | 작성일 | fields.json:699 | 묻기 |
| `signer.name` | 신청인 | text | 1쪽 [686, 924, 762, 942] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:725 | 묻기 |
| `signer2.name` | 신청인 | text | 1쪽 [698, 926, 774, 943] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:744 | 묻기 |

## 체크·도장·서명 (marks) — 12칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.수입형태사전송금방식만작성` | 수입형태*사전송금방식만작성 | checkbox (사전 통관수입 / 사전 무통관수입(중계무역) / 사전 무통관수입(외국인수수입)) | 1쪽 [298, 384, 400, 398] | 늘 | 파일 key | 보기 중 고름: 사전 통관수입 / 사전 무통관수입(중계무역) / 사전 무통관수입(외국인수수입) | fields.json:99 | 묻기 |
| `check.만기` | 만기(상환일) | checkbox (Fixed due date ( / () | 1쪽 [642, 455, 667, 469] | 늘 | 파일 key | 보기 중 고름: Fixed due date ( / ( | fields.json:161 | 묻기 |
| `check.거래방식` | 거래방식(선적구분) | checkbox (사전송금 방식 (선적 전) / 사후송금 방식 (선적 후)) | 1쪽 [696, 362, 852, 377] | 늘 | 파일 key | 보기 중 고름: 사전송금 방식 (선적 전) / 사후송금 방식 (선적 후) | fields.json:207 | 묻기 |
| `check.송금수수료부담자` | 송금수수료부담자 | checkbox (SHA / OUR) | 1쪽 [843, 773, 889, 787] | 늘 | 파일 key | 보기 중 고름: SHA / OUR | fields.json:531 | 묻기 |
| `seal.signer` | 신청인 | seal | 1쪽 [812, 927, 835, 942] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:725 | 묻기 |
| `sign.signer` | 신청인 | signature | 1쪽 [812, 927, 835, 942] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:725 | 묻기 |
| `seal.signer2` | 신청인 | seal | 1쪽 [844, 916, 897, 953] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:744 | 묻기 |
| `sign.signer2` | 신청인 | signature | 1쪽 [838, 927, 904, 942] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:744 | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [766, 102, 845, 155] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [766, 102, 845, 155] | 늘 | - | - | - | 묻기 |
| `seal.staff.부점장` | 부점장 | seal | 1쪽 [845, 102, 922, 155] | 늘 | - | - | - | 묻기 |
| `sign.staff.부점장` | 부점장 | signature | 1쪽 [845, 102, 922, 155] | 늘 | - | - | - | 묻기 |

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
"Usance 송금 신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "824-499051-78019",
 "하나 TDF 2040",
 "6917-9669",
 "485222",
 "미국",
 "독일",
 "(주)우진로지스",
 "010-6144-1173",
 "765-974876-64408",
 "카카오뱅크",
 "농협은행",
 "남궁진빈",
 "600957-0031852",
 "yetae741@gmail.com",
 "9,110,000",
 "남궁예태"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"765-974876-64408"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"yetae741@gmail.com"
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
- 신청정보: ♣신청정보
- 신청인정보: ♣신청인정보
- 영문: 영문(English)
- 한글: 한글(Korean)
- 선적정보: ♣선적정보
- 계약서번호: 계약서번호
- 상품명세: 상품명세
- 가격조건: 가격조건
- 원산지: 원산지
- 운송서류번호사후송금방식인경우작성: 운송서류번호(B/LNo등)*사후송금방식인경우작성
- 선적항: (예정)선적항(또는공항)
- terms.end1_copy: 대출만료일월
- 도착항: (예정)도착항(또는공항)
- HS코드: HS코드
- 수출국: 수출국
- date: 선적(예정)일
- 선적국가: 선적국가
- 도착국가: 도착국가
- 수취인명: 수취인명
- 수취인주소및전화번호: 수취인주소및전화번호 (같은 설명 중 1번째 칸)
- customer.name7: 성명(업체명)
- 수취인주소및전화번호2: 수취인주소및전화번호 (같은 설명 중 2번째 칸)
- 수취인계좌번호: 수취인계좌번호
- LG금액: L/G금액
- 수취은행BIC: 수취은행BIC
- 송금수취인및수취은행정보: ♣송금수취인및수취은행정보
- 수취은행명: 수취은행명
- 담당자명: 담당자명
- customer.phone: 전화번호
- TELNo: TELNo
- customer.email: E-mail
- 통화금액: 통화(),금액
- date2: 작성일 (같은 설명 중 1번째 칸)
- SWIFTCode: SWIFTCode
- date3: 작성일 (같은 설명 중 2번째 칸)
- signer.name: 신청인 (같은 설명 중 1번째 칸)
- signer2.name: 신청인 (같은 설명 중 2번째 칸)
```

답:

```json
[{"key": "신청정보", "value": null},
 {"key": "신청인정보", "value": null},
 {"key": "영문", "value": null},
 {"key": "한글", "value": null},
 {"key": "선적정보", "value": null},
 {"key": "계약서번호", "value": "824-499051-78019", "bbox_2d": [291, 505, 454, 524], "page": 1},
 {"key": "상품명세", "value": "하나 TDF 2040", "bbox_2d": [293, 528, 426, 547], "page": 1},
 {"key": "가격조건", "value": null},
 {"key": "원산지", "value": null},
 {"key": "운송서류번호사후송금방식인경우작성", "value": "6917-9669", "bbox_2d": [293, 600, 381, 619], "page": 1},
 {"key": "선적항", "value": null},
 {"key": "terms.end1_copy", "value": null},
 {"key": "도착항", "value": null},
 {"key": "HS코드", "value": "485222", "bbox_2d": [725, 552, 793, 570], "page": 1},
 {"key": "수출국", "value": null},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [729, 601, 913, 618], "page": 1},
 {"key": "선적국가", "value": "미국", "bbox_2d": [726, 626, 766, 644], "page": 1},
 {"key": "도착국가", "value": "독일", "bbox_2d": [724, 651, 763, 669], "page": 1},
 {"key": "수취인명", "value": "(주)우진로지스", "bbox_2d": [292, 701, 423, 719], "page": 1},
 {"key": "수취인주소및전화번호", "value": "010-6144-1173", "bbox_2d": [293, 722, 415, 742], "page": 1},
 {"key": "customer.name7", "value": null},
 {"key": "수취인주소및전화번호2", "value": "010-6144-1173", "bbox_2d": [295, 746, 416, 766], "page": 1},
 {"key": "수취인계좌번호", "value": "765-974876-64408", "bbox_2d": [289, 769, 461, 790], "page": 1},
 {"key": "LG금액", "value": null},
 {"key": "수취은행BIC", "value": "카카오뱅크", "bbox_2d": [291, 797, 390, 814], "page": 1},
 {"key": "송금수취인및수취은행정보", "value": "농협은행", "bbox_2d": [295, 679, 370, 697], "page": 1},
 {"key": "수취은행명", "value": "카카오뱅크", "bbox_2d": [723, 794, 821, 812], "page": 1},
 {"key": "담당자명", "value": "남궁진빈", "bbox_2d": [293, 844, 373, 864], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [291, 869, 412, 889], "page": 1},
 {"key": "TELNo", "value": "600957-0031852", "bbox_2d": [672, 283, 781, 298], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [672, 301, 848, 320], "page": 1},
 {"key": "통화금액", "value": "9,110,000", "bbox_2d": [496, 354, 573, 373], "page": 1},
 {"key": "date2", "value": "2025년 4월 1일", "bbox_2d": [265, 406, 433, 423], "page": 1},
 {"key": "SWIFTCode", "value": null},
 {"key": "date3", "value": "2025년 4월 1일", "bbox_2d": [339, 926, 553, 943], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [686, 924, 762, 942], "page": 1},
 {"key": "signer2.name", "value": "남궁예태", "bbox_2d": [698, 926, 774, 943], "page": 1}]
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
- check.수입형태사전송금방식만작성: 수입형태*사전송금방식만작성 (체크박스, 보기: 사전 통관수입 / 사전 무통관수입(중계무역) / 사전 무통관수입(외국인수수입))
- check.만기: 만기(상환일) (체크박스, 보기: Fixed due date ( / ()
- check.거래방식: 거래방식(선적구분) (체크박스, 보기: 사전송금 방식 (선적 전) / 사후송금 방식 (선적 후))
- check.송금수수료부담자: 송금수수료부담자 (체크박스, 보기: SHA / OUR)
- seal.signer: 신청인 (같은 설명 중 1번째 칸, 도장)
- sign.signer: 신청인 (같은 설명 중 2번째 칸, 서명)
- seal.signer2: 신청인 (같은 설명 중 3번째 칸, 도장)
- sign.signer2: 신청인 (같은 설명 중 4번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 설명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 설명 중 2번째 칸, 서명)
- seal.staff.부점장: 부점장 (같은 설명 중 1번째 칸, 도장)
- sign.staff.부점장: 부점장 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.수입형태사전송금방식만작성", "value": "사전 통관수입", "bbox_2d": [298, 386, 314, 398], "page": 1},
 {"key": "check.만기", "value": "(", "bbox_2d": [642, 457, 658, 469], "page": 1},
 {"key": "check.거래방식", "value": "사후송금 방식 (선적 후)", "bbox_2d": [696, 365, 711, 377], "page": 1},
 {"key": "check.송금수수료부담자", "value": "OUR", "bbox_2d": [843, 775, 858, 787], "page": 1},
 {"key": "seal.signer", "value": false},
 {"key": "sign.signer", "value": true, "bbox_2d": [812, 927, 835, 942], "page": 1},
 {"key": "seal.signer2", "value": true, "bbox_2d": [844, 916, 897, 953], "page": 1},
 {"key": "sign.signer2", "value": false},
 {"key": "seal.staff.책임자", "value": false},
 {"key": "sign.staff.책임자", "value": false},
 {"key": "seal.staff.부점장", "value": false},
 {"key": "sign.staff.부점장", "value": false}]
```

### 표 찾기 `table_find` · 채점 f1_iou50 (위치)

질문:

```
이 문서에서 표를 모두 찾아 JSON 목록으로 답하세요. 여기서 표는 같은 항목 묶음(열)이 행마다 되풀이되고 행 수가 서류마다 달라지는 목록입니다. 항목명과 값이 번갈아 있는 신청서 칸, 칸 수가 정해진 결재란은 표가 아닙니다.
표마다 {{"columns": [머리글 글자, …], "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호, "n_rows": 행 수}} 를 쓰고, 여러 쪽에 걸친 표는 쪽마다 따로 씁니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 행 수에는 머리글·합계 행과 모두 빈 행을 넣지 않습니다. 표가 없으면 [] 로 답하세요.
```

답:

```json
[]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf225 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf225` → `python -m docgen.formdir card hf225` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf225 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf225 --show` · `python -m docgen.preview hf225 --out work/hf225`
