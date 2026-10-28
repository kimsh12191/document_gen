# 전자적무역결제금융등록(변경,해지)신청서 (`hf334`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf334 · card-hash: 5f3193181d0f -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 전자적무역결제금융등록(변경,해지)신청서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.334 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 36칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `value` | (한글) | amount | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:46 | 묻기 |
| `value2` | (영문) | amount | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:57 | 묻기 |
| `corp.biz_no` ← `company.biz_no` | 사업자번호 | biz_no | 1쪽 [185, 208, 283, 219] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:68 | 묻기 |
| `corp.ceo` ← `company.ceo` | 대표자성명 | text | 1쪽 [184, 231, 247, 242] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:79 | 묻기 |
| `value3` | (한글) | amount | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:90 | 묻기 |
| `value4` | (영문) | amount | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:101 | 묻기 |
| `customer.phone` | 전화번호 | phone | 1쪽 [183, 301, 287, 312] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:112 | 묻기 |
| `customer.name` | 성명 | text | 1쪽 [288, 324, 350, 335] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:123 | 묻기 |
| `customer.email` | E-mail | text | 1쪽 [286, 388, 437, 399] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:135 | 묻기 |
| `corp.corp_reg_no` ← `company.corp_reg_no` | 법인번호 | corp_reg_no | 1쪽 [624, 208, 741, 219] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:147 | 묻기 |
| `대표자생년월일` | 대표자생년월일 | date | 1쪽 [627, 231, 707, 242] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `팩스번호` | 팩스번호 | phone | 1쪽 [624, 301, 720, 312] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:169 | 묻기 |
| `customer.name2` | 성명 | text | 1쪽 [726, 324, 788, 335] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:180 | 묻기 |
| `customer.email2` | E-mail | text | 1쪽 [730, 388, 881, 399] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:192 | 묻기 |
| `원화` | 원화(KRW) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:204 | 묻기 |
| `미화` | 미화(USD) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:215 | 묻기 |
| `위안화` | 위안화(CNY) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:226 | 묻기 |
| `엔화` | 엔화(JPY) | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:237 | 묻기 |
| `목록.*.거래인감` | 거래인감 | text | - (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:248 | 묻기 |
| `목록.*.비고` | 비고 | text | 1쪽 [725, 484, 792, 495] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:296 | 묻기 |
| `value5` | (한글) | amount | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:344 | 묻기 |
| `기업식별번호` | 기업식별번호 | text | 1쪽 [182, 672, 257, 683] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:355 | 묻기 |
| `value6` | (한글) | amount | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:366 | 묻기 |
| `value7` | (영문) | amount | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:377 | 묻기 |
| `customer.phone2` | 전화번호 | phone | 1쪽 [182, 742, 286, 753] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:388 | 묻기 |
| `value8` | (은행명) | amount | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:399 | 묻기 |
| `value9` | (계좌번호) | amount | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:410 | 묻기 |
| `customer.name3` | 성명 | text | 1쪽 [288, 812, 351, 823] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:421 | 묻기 |
| `customer.phone3` | 전화번호 | phone | 1쪽 [287, 835, 392, 846] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:433 | 묻기 |
| `팩스번호2` | 팩스번호 | phone | 1쪽 [598, 742, 694, 753] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:445 | 묻기 |
| `BicCode` | BicCode | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `foreign.address` | 주소(영문) | text | 1쪽 [595, 790, 855, 798] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:468 | 묻기 |
| `팩스번호3` | 팩스번호 | phone | 1쪽 [597, 812, 693, 823] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:480 | 묻기 |
| `customer.email3` | E-mail | text | 1쪽 [598, 835, 749, 846] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:492 | 묻기 |
| `신청인주소` | 신청인(업체)주소 | text | 1쪽 [465, 898, 796, 909] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `corp.name` ← `company.name` | 업체명 | text | 1쪽 [798, 921, 902, 932] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:515 | 묻기 |

## 체크·도장·서명 (marks) — 4칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.staff.담당` | 담당 | seal | 1쪽 [796, 101, 872, 149] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [796, 101, 872, 149] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [881, 106, 934, 144] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [872, 101, 943, 149] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키 `a` ← `b`:** 질문·정답은 공통 키 a, 서식의 원래 키는 b (키 사전이 정함). **정한 곳:** 템플릿에서 그 칸 자리 (html·코드 서식) / 칸 목록의 그 칸 (원본 서식).

## 질문 → 답 (seed 1000000 로 그린 실제 문항)

질문은 모델에게 가는 글 전부, 답은 데이터의 정답 (그린 문서의 값·위치). 질문 문장·답 꼴은 공통 `docgen/forms/_common/questions.json`.

### 서류 분류 `classify` · 채점 acc

질문:

```
이 문서는 고객이 은행에 제출한 서류입니다. 서류의 정식 명칭(서류명)을 답하세요. 설명 없이 서류명만 한 줄로 답하세요.
```

답:

```json
"전자적무역결제금융등록(변경,해지)신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "702-81-38348",
 "남궁예태",
 "010-6144-1173",
 "yetae741@gmail.com",
 "200112-7951835",
 "2024-03-12",
 "051-509-1176",
 "해당 없음",
 "6351-4061",
 "2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 163-0001",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "(주)미래케미칼"
]
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

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2024-03-12"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- value: (한글) (같은 항목명 중 1번째 칸)
- value2: (영문) (같은 항목명 중 1번째 칸)
- corp.biz_no: 사업자번호 (법인·사업자 사업자등록번호)
- corp.ceo: 대표자성명 (법인·사업자 대표자)
- value3: (한글) (같은 항목명 중 2번째 칸)
- value4: (영문) (같은 항목명 중 2번째 칸)
- customer.phone: 전화번호 (고객 연락처, 같은 항목명 중 1번째 칸)
- customer.name: 성명 (고객 성명, 같은 항목명 중 1번째 칸)
- customer.email: E-mail (고객 이메일, 같은 항목명 중 1번째 칸)
- 대표자생년월일: 대표자생년월일
- 팩스번호: 팩스번호 (같은 항목명 중 1번째 칸)
- customer.name2: 성명 (같은 항목명 중 2번째 칸)
- customer.email2: E-mail (같은 항목명 중 2번째 칸)
- 원화: 원화(KRW)
- 미화: 미화(USD)
- 위안화: 위안화(CNY)
- 엔화: 엔화(JPY)
- 목록.0.거래인감: 거래인감 (목록 1행)
- 목록.1.거래인감: 거래인감 (목록 2행)
- 목록.2.거래인감: 거래인감 (목록 3행)
- 목록.3.거래인감: 거래인감 (목록 4행)
- 목록.0.비고: 비고 (목록 1행)
- 목록.1.비고: 비고 (목록 2행)
- 목록.2.비고: 비고 (목록 3행)
- 목록.3.비고: 비고 (목록 4행)
- value5: (한글) (같은 항목명 중 3번째 칸)
- 기업식별번호: 기업식별번호
- value6: (한글) (같은 항목명 중 4번째 칸)
- value7: (영문) (같은 항목명 중 3번째 칸)
- customer.phone2: 전화번호 (같은 항목명 중 2번째 칸)
- value8: (은행명)
- value9: (계좌번호)
- customer.name3: 성명 (같은 항목명 중 3번째 칸)
- customer.phone3: 전화번호 (같은 항목명 중 3번째 칸)
- 팩스번호2: 팩스번호 (같은 항목명 중 2번째 칸)
- BicCode: BicCode
- foreign.address: 주소(영문) (외국 상대 주소)
- customer.email3: E-mail (같은 항목명 중 3번째 칸)
- 신청인주소: 신청인(업체)주소
- corp.name: 업체명 (법인·사업자 상호)
```

답:

```json
[{"key": "value", "value": null},
 {"key": "value2", "value": null},
 {"key": "corp.biz_no", "value": "702-81-38348", "bbox_2d": [185, 208, 283, 219], "page": 1},
 {"key": "corp.ceo", "value": "남궁예태", "bbox_2d": [184, 231, 247, 242], "page": 1},
 {"key": "value3", "value": null},
 {"key": "value4", "value": null},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [183, 301, 287, 312], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [288, 324, 350, 335], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [286, 388, 437, 399], "page": 1},
 {"key": "대표자생년월일", "value": "2024-03-12", "bbox_2d": [627, 231, 707, 242], "page": 1},
 {"key": "팩스번호", "value": "051-509-1176", "bbox_2d": [624, 301, 720, 312], "page": 1},
 {"key": "customer.name2", "value": "남궁예태", "bbox_2d": [726, 324, 788, 335], "page": 1},
 {"key": "customer.email2", "value": "yetae741@gmail.com", "bbox_2d": [730, 388, 881, 399], "page": 1},
 {"key": "원화", "value": null},
 {"key": "미화", "value": null},
 {"key": "위안화", "value": null},
 {"key": "엔화", "value": null},
 {"key": "목록.0.거래인감", "value": null},
 {"key": "목록.1.거래인감", "value": null},
 {"key": "목록.2.거래인감", "value": null},
 {"key": "목록.3.거래인감", "value": null},
 {"key": "목록.0.비고", "value": "해당 없음", "bbox_2d": [725, 484, 792, 495], "page": 1},
 {"key": "목록.1.비고", "value": "해당 없음", "bbox_2d": [727, 508, 793, 519], "page": 1},
 {"key": "목록.2.비고", "value": "해당 없음", "bbox_2d": [726, 531, 793, 542], "page": 1},
 {"key": "목록.3.비고", "value": "해당 없음", "bbox_2d": [730, 554, 797, 565], "page": 1},
 {"key": "value5", "value": null},
 {"key": "기업식별번호", "value": "6351-4061", "bbox_2d": [182, 672, 257, 683], "page": 1},
 {"key": "value6", "value": null},
 {"key": "value7", "value": null},
 {"key": "customer.phone2", "value": "010-6144-1173", "bbox_2d": [182, 742, 286, 753], "page": 1},
 {"key": "value8", "value": null},
 {"key": "value9", "value": null},
 {"key": "customer.name3", "value": "남궁예태", "bbox_2d": [288, 812, 351, 823], "page": 1},
 {"key": "customer.phone3", "value": "010-6144-1173", "bbox_2d": [287, 835, 392, 846], "page": 1},
 {"key": "팩스번호2", "value": "051-509-1176", "bbox_2d": [598, 742, 694, 753], "page": 1},
 {"key": "BicCode", "value": null},
 {"key": "foreign.address", "value": "2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 163-0001", "bbox_2d": [595, 790, 855, 798], "page": 1},
 {"key": "customer.email3", "value": "yetae741@gmail.com", "bbox_2d": [598, 835, 749, 846], "page": 1},
 {"key": "신청인주소", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [465, 898, 796, 909], "page": 1},
 {"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [798, 921, 902, 932], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": true, "bbox_2d": [796, 101, 872, 149], "page": 1},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [881, 106, 934, 144], "page": 1},
 {"key": "sign.staff.책임자", "value": false}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기·위치·항목명 | studio ① 서식 › 영역 편집 (저장하면 `fields.json` items) | 재검수 → 카드 다시 만들기 |
| 값이 이상함 | 영역 편집에서 그 칸의 값 출처·값 종류 | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf334 --show` · `python -m docgen.preview hf334 --out work/hf334`
