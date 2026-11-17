# 자본재 등 도입물품명세 검토ㆍ확인신청서 (`hf244`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf244 · card-hash: 9ebadb64e860 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 3 (seed 1000000 로 그린 것) · **분류 정답:** 자본재 등 도입물품명세 검토ㆍ확인신청서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf244 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.244 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 57칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `접수일` | 접수일 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:64 | 묻기 |
| `처리일` | 처리일 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:78 | 묻기 |
| `신고된사업명` | 신고된사업명 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:92 | 묻기 |
| `상호또는명칭` | 상호또는명칭(영문) | text | 1쪽 [399, 291, 513, 309] | 늘 | 파일 key | 값 종류 `company` | fields.json:106 | 묻기 |
| `customer.nationality` | 국적 | text | 1쪽 [290, 326, 370, 344] | 늘 | 파일 key | 고객 정보 (키 `customer.nationality`, 없으면 값 종류 `text`) | fields.json:120 | 묻기 |
| `HSK분류번호` | HSK분류번호 | rrn | 1쪽 [226, 416, 316, 429] | 늘 | 파일 key | 값 종류 `number` | fields.json:133 | 묻기 |
| `품명` | 품명 | text | 1쪽 [367, 416, 430, 427] | 늘 | 파일 key | 값 종류 `goods` | fields.json:150 | 묻기 |
| `수량` | 수량 | number | 1쪽 [476, 414, 486, 431] | 늘 | 파일 key | 값 종류 `count` | fields.json:167 | 묻기 |
| `규격` | 규격 | text | 1쪽 [530, 416, 595, 430] | 늘 | 파일 key | 값 종류 `goods` | fields.json:184 | 묻기 |
| `제작자` | 제작자 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:201 | 묻기 |
| `금액` | 금액(기준통화ᆞ도입통화) | number | 1쪽 [835, 411, 918, 431] | 늘 | 파일 key | 값 종류 `amount` | fields.json:218 | 묻기 |
| `date` | 작성일 | date | 1쪽 [380, 217, 556, 234] | 늘 | 파일 key | 작성일 | fields.json:235 | 묻기 |
| `date2` | 작성일 | date | 1쪽 [723, 479, 924, 496] | 늘 | 파일 key | 작성일 | fields.json:261 | 묻기 |
| `signer.name` | 신고인(또는대리인) | text | 1쪽 [646, 498, 727, 516] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:287 | 묻기 |
| `date3` | 작성일 | date | 1쪽 [723, 604, 924, 620] | 늘 | 파일 key | 작성일 | fields.json:306 | 묻기 |
| `접수번호` | 접수번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:332 | 묻기 |
| `상호또는명칭2` | 상호또는명칭(영문) | text | 1쪽 [399, 144, 500, 163] | 늘 | 파일 key | 값 종류 `company` | fields.json:347 | 묻기 |
| `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [726, 144, 838, 161] | 늘 | 파일 key | 고객 정보 (키 `company.biz_no`, 없으면 값 종류 `biz_no`) | fields.json:362 | 묻기 |
| `외국인투자금액및비율` | 외국인투자금액및비율 | number | 1쪽 [515, 253, 541, 271] | 늘 | 파일 key | 값 종류 `percent` | fields.json:376 | 묻기 |
| `접수일2` | 접수일 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:391 | 묻기 |
| `처리일2` | 처리일 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:405 | 묻기 |
| `신고된사업명2` | 신고된사업명 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:419 | 묻기 |
| `상호또는명칭3` | 상호또는명칭(영문) | text | 2쪽 [399, 291, 566, 311] | 늘 | 파일 key | 값 종류 `company` | fields.json:433 | 묻기 |
| `customer.nationality2` | 국적 | text | 2쪽 [293, 326, 373, 344] | 늘 | 파일 key | 고객 정보 (키 `customer.nationality`, 없으면 값 종류 `text`) | fields.json:447 | 묻기 |
| `HSK분류번호2` | HSK분류번호 | text | 2쪽 [226, 413, 310, 432] | 늘 | 파일 key | 값 종류 `number` | fields.json:460 | 묻기 |
| `품명2` | 품명 | text | 2쪽 [365, 417, 428, 429] | 늘 | 파일 key | 값 종류 `goods` | fields.json:477 | 묻기 |
| `수량2` | 수량 | number | 2쪽 [476, 414, 481, 432] | 늘 | 파일 key | 값 종류 `count` | fields.json:494 | 묻기 |
| `규격2` | 규격 | text | 2쪽 [527, 416, 593, 428] | 늘 | 파일 key | 값 종류 `goods` | fields.json:511 | 묻기 |
| `제작자2` | 제작자 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:528 | 묻기 |
| `금액2` | 금액(기준통화ᆞ도입통화) | number | 2쪽 [836, 413, 916, 432] | 늘 | 파일 key | 값 종류 `amount` | fields.json:545 | 묻기 |
| `date4` | 작성일 | date | 2쪽 [380, 217, 556, 234] | 늘 | 파일 key | 작성일 | fields.json:562 | 묻기 |
| `date5` | 작성일 | date | 2쪽 [723, 479, 924, 496] | 늘 | 파일 key | 작성일 | fields.json:588 | 묻기 |
| `signer2.name` | 신고인(또는대리인) | text | 2쪽 [646, 496, 726, 515] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:614 | 묻기 |
| `date6` | 작성일 | date | 2쪽 [723, 604, 924, 620] | 늘 | 파일 key | 작성일 | fields.json:633 | 묻기 |
| `접수번호2` | 접수번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:659 | 묻기 |
| `상호또는명칭4` | 상호또는명칭(영문) | text | 2쪽 [398, 143, 513, 163] | 늘 | 파일 key | 값 종류 `company` | fields.json:674 | 묻기 |
| `company.biz_no2` | 사업자등록번호 | biz_no | 2쪽 [726, 145, 838, 163] | 늘 | 파일 key | 고객 정보 (키 `company.biz_no`, 없으면 값 종류 `biz_no`) | fields.json:689 | 묻기 |
| `외국인투자금액및비율2` | 외국인투자금액및비율 | number | 2쪽 [521, 253, 541, 271] | 늘 | 파일 key | 값 종류 `percent` | fields.json:703 | 묻기 |
| `접수일3` | 접수일 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:718 | 묻기 |
| `처리일3` | 처리일 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:732 | 묻기 |
| `신고된사업명3` | 신고된사업명 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:746 | 묻기 |
| `상호또는명칭5` | 상호또는명칭(영문) | text | 3쪽 [402, 290, 517, 311] | 늘 | 파일 key | 값 종류 `company` | fields.json:760 | 묻기 |
| `customer.nationality3` | 국적 | text | 3쪽 [291, 325, 371, 344] | 늘 | 파일 key | 고객 정보 (키 `customer.nationality`, 없으면 값 종류 `text`) | fields.json:774 | 묻기 |
| `HSK분류번호3` | HSK분류번호 | text | 3쪽 [225, 416, 316, 429] | 늘 | 파일 key | 값 종류 `number` | fields.json:787 | 묻기 |
| `품명3` | 품명 | text | 3쪽 [367, 412, 427, 430] | 늘 | 파일 key | 값 종류 `goods` | fields.json:804 | 묻기 |
| `수량3` | 수량 | number | 3쪽 [476, 414, 486, 432] | 늘 | 파일 key | 값 종류 `count` | fields.json:821 | 묻기 |
| `규격3` | 규격 | text | 3쪽 [527, 412, 597, 429] | 늘 | 파일 key | 값 종류 `goods` | fields.json:838 | 묻기 |
| `제작자3` | 제작자 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:855 | 묻기 |
| `금액3` | 금액(기준통화ᆞ도입통화) | number | 3쪽 [818, 413, 916, 430] | 늘 | 파일 key | 값 종류 `amount` | fields.json:872 | 묻기 |
| `date7` | 작성일 | date | 3쪽 [380, 217, 556, 234] | 늘 | 파일 key | 작성일 | fields.json:889 | 묻기 |
| `date8` | 작성일 | date | 3쪽 [723, 479, 924, 496] | 늘 | 파일 key | 작성일 | fields.json:915 | 묻기 |
| `signer3.name` | 신고인(또는대리인) | text | 3쪽 [646, 497, 727, 515] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:941 | 묻기 |
| `date9` | 작성일 | date | 3쪽 [723, 604, 924, 620] | 늘 | 파일 key | 작성일 | fields.json:960 | 묻기 |
| `접수번호3` | 접수번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:986 | 묻기 |
| `상호또는명칭6` | 상호또는명칭(영문) | text | 3쪽 [397, 144, 511, 162] | 늘 | 파일 key | 값 종류 `company` | fields.json:1001 | 묻기 |
| `company.biz_no3` | 사업자등록번호 | biz_no | 3쪽 [729, 143, 841, 163] | 늘 | 파일 key | 고객 정보 (키 `company.biz_no`, 없으면 값 종류 `biz_no`) | fields.json:1016 | 묻기 |
| `외국인투자금액및비율3` | 외국인투자금액및비율 | number | 3쪽 [517, 253, 543, 271] | 늘 | 파일 key | 값 종류 `percent` | fields.json:1030 | 묻기 |

## 체크·도장·서명 (marks) — 12칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.signer` | 신고인(또는대리인) | seal | 1쪽 [853, 489, 904, 525] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:287 | 묻기 |
| `sign.signer` | 신고인(또는대리인) | signature | 1쪽 [831, 499, 926, 514] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:287 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [726, 35, 770, 66] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [712, 29, 784, 72] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [794, 35, 838, 66] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [784, 29, 849, 72] | 늘 | - | - | - | 묻기 |
| `seal.staff.부점장` | 부점장 | seal | 1쪽 [864, 36, 904, 65] | 늘 | - | - | - | 묻기 |
| `sign.staff.부점장` | 부점장 | signature | 1쪽 [849, 29, 920, 72] | 늘 | - | - | - | 묻기 |
| `seal.signer2` | 신고인(또는대리인) | seal | 2쪽 [831, 499, 926, 514] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:614 | 묻기 |
| `sign.signer2` | 신고인(또는대리인) | signature | 2쪽 [831, 499, 926, 514] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:614 | 묻기 |
| `seal.signer3` | 신고인(또는대리인) | seal | 3쪽 [853, 489, 904, 525] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:941 | 묻기 |
| `sign.signer3` | 신고인(또는대리인) | signature | 3쪽 [831, 499, 926, 514] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:941 | 묻기 |

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
"자본재 등 도입물품명세 검토ㆍ확인신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "주식회사 동방전자",
 "대한민국",
 "6240-4561",
 "자동차 부품",
 "1",
 "냉동 수산물",
 "3,470,000",
 "남궁예태",
 "미래테크(주)",
 "702-81-38348",
 "50"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"주식회사 동방전자"
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
항목 (키: 설명 (몇 번째 행))
- 상호또는명칭3: 상호또는명칭(영문) (같은 설명 중 1번째 칸)
- customer.nationality2: 국적
- HSK분류번호2: HSK분류번호
- 품명2: 품명
- 수량2: 수량
- 규격2: 규격
- 금액2: 금액(기준통화ᆞ도입통화)
- date4: 작성일 (같은 설명 중 1번째 칸)
- date5: 작성일 (같은 설명 중 2번째 칸)
- signer2.name: 신고인(또는대리인)
- date6: 작성일 (같은 설명 중 3번째 칸)
- 상호또는명칭4: 상호또는명칭(영문) (같은 설명 중 2번째 칸)
- company.biz_no2: 사업자등록번호
- 외국인투자금액및비율2: 외국인투자금액및비율
```

답:

```json
[{"key": "상호또는명칭3", "value": "주식회사 동방전자", "bbox_2d": [399, 291, 566, 311], "page": 1},
 {"key": "customer.nationality2", "value": "대한민국", "bbox_2d": [293, 326, 373, 344], "page": 1},
 {"key": "HSK분류번호2", "value": "6240-4561", "bbox_2d": [226, 413, 310, 432], "page": 1},
 {"key": "품명2", "value": "자동차 부품", "bbox_2d": [365, 417, 428, 429], "page": 1},
 {"key": "수량2", "value": "1", "bbox_2d": [476, 414, 481, 432], "page": 1},
 {"key": "규격2", "value": "냉동 수산물", "bbox_2d": [527, 416, 593, 428], "page": 1},
 {"key": "금액2", "value": "3,470,000", "bbox_2d": [836, 413, 916, 432], "page": 1},
 {"key": "date4", "value": "2025년 4월 1일", "bbox_2d": [380, 217, 556, 234], "page": 1},
 {"key": "date5", "value": "2025년 4월 1일", "bbox_2d": [723, 479, 924, 496], "page": 1},
 {"key": "signer2.name", "value": "남궁예태", "bbox_2d": [646, 496, 726, 515], "page": 1},
 {"key": "date6", "value": "2025년 4월 1일", "bbox_2d": [723, 604, 924, 620], "page": 1},
 {"key": "상호또는명칭4", "value": "미래테크(주)", "bbox_2d": [398, 143, 513, 163], "page": 1},
 {"key": "company.biz_no2", "value": "702-81-38348", "bbox_2d": [726, 145, 838, 163], "page": 1},
 {"key": "외국인투자금액및비율2", "value": "50", "bbox_2d": [521, 253, 541, 271], "page": 1}]
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
- seal.signer2: 신고인(또는대리인) (같은 설명 중 1번째 칸, 도장)
- sign.signer2: 신고인(또는대리인) (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.signer2", "value": false},
 {"key": "sign.signer2", "value": true, "bbox_2d": [831, 499, 926, 514], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf244 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf244` → `python -m docgen.formdir card hf244` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf244 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf244 --show` · `python -m docgen.preview hf244 --out work/hf244`
