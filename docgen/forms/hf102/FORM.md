# 기업현황서(B2B전자결제서비스 업무, MP용) (`hf102`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf102 · card-hash: c9a450dd7f4e -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 6 (seed 1000000 로 그린 것) · **분류 정답:** 기업현황서(B2B전자결제서비스 업무, MP용)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf102 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.102 (대출) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 40칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `date` | 작성일 | date | 1쪽 [417, 321, 558, 339] | 늘 | 파일 key | 작성일 | fields.json:41 | 묻기 |
| `company.name` | 기업명 | text | 1쪽 [379, 399, 508, 422] | 늘 | 파일 key | 고객 정보 (키 `company.name`, 없으면 값 종류 `company`) | fields.json:68 | 묻기 |
| `signer.name` | 대표이사 | text | 1쪽 [486, 435, 565, 457] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:81 | 묻기 |
| `employer.position` | 직위 | text | 1쪽 [379, 550, 418, 572] | 늘 | 파일 key | 고객 정보 (키 `employer.position`, 없으면 값 종류 `text`) | fields.json:100 | 묻기 |
| `signer2.name` | 성명 | text | 1쪽 [483, 574, 563, 598] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:113 | 묻기 |
| `연락처TEL` | 연락처:TEL | phone | 1쪽 [371, 644, 494, 666] | 늘 | 파일 key | 값 종류 `phone` | fields.json:132 | 묻기 |
| `customer.phone` | HP | phone | 1쪽 [370, 668, 493, 692] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `text`) | fields.json:146 | 묻기 |
| `FAX` | FAX | phone | 1쪽 [376, 692, 491, 715] | 늘 | 파일 key | 값 종류 `phone` | fields.json:159 | 묻기 |
| `company.name2` | 기업체명 | text | 2쪽 [254, 102, 383, 124] | 늘 | 파일 key | 고객 정보 (키 `company.name`, 없으면 값 종류 `company`) | fields.json:173 | 묻기 |
| `본사` | 본사 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:186 | 묻기 |
| `주사무소` | 주사무소 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:201 | 묻기 |
| `사업장` | 사업장 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:216 | 묻기 |
| `company.biz_item` | 업종(표준산업분류기호) | text | 2쪽 [252, 247, 327, 269] | 늘 | 파일 key | 고객 정보 (키 `company.biz_item`, 없으면 값 종류 `text`) | fields.json:231 | 묻기 |
| `종업원수` | 종업원수 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:244 | 묻기 |
| `company.biz_no` | 사업자등록번호 | biz_no | 2쪽 [255, 466, 377, 489] | 늘 | 파일 key | 고객 정보 (키 `company.biz_no`, 없으면 값 종류 `biz_no`) | fields.json:306 | 묻기 |
| `협회및단체가입` | 협회및단체가입 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:319 | 묻기 |
| `인허가등록` | 인허가등록 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:333 | 묻기 |
| `주거래은행` | 주거래은행 | text | 2쪽 [257, 831, 325, 853] | 늘 | 파일 key | 값 종류 `bank` | fields.json:347 | 묻기 |
| `총자산` | 총자산 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:361 | 묻기 |
| `자본금` | 자본금 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:376 | 묻기 |
| `자기자본` | 자기자본 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:391 | 묻기 |
| `매출액` | 매출액 | number | 2쪽 [583, 720, 672, 742] | 늘 | 파일 key | 값 종류 `amount` | fields.json:406 | 묻기 |
| `경상이익` | 경상이익 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:421 | 묻기 |
| `당기순이익` | 당기순이익 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:436 | 묻기 |
| `company.ceo` | 대표자 | text | 2쪽 [686, 101, 765, 123] | 늘 | 파일 key | 고객 정보 (키 `company.ceo`, 없으면 값 종류 `text`) | fields.json:499 | 묻기 |
| `TEL` | TEL | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:512 | 묻기 |
| `FAX2` | FAX | phone | 2쪽 [681, 159, 795, 182] | 늘 | 파일 key | 값 종류 `phone` | fields.json:527 | 묻기 |
| `TEL2` | TEL | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:542 | 묻기 |
| `TEL3` | TEL | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:557 | 묻기 |
| `설립년월` | 설립년월 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:572 | 묻기 |
| `company.corp_no` | 법인등록번호 | corp_reg_no | 2쪽 [683, 466, 819, 488] | 늘 | 파일 key | 고객 정보 (키 `company.corp_no`, 없으면 값 종류 `number`) | fields.json:634 | 묻기 |
| `정부기관및금융기관우대` | 정부기관및금융기관우대 | text | 2쪽 [679, 502, 751, 525] | 늘 | 파일 key | 값 종류 `bank` | fields.json:647 | 묻기 |
| `당좌거래은행` | 당좌거래은행 | text | 2쪽 [683, 831, 745, 852] | 늘 | 파일 key | 값 종류 `bank` | fields.json:757 | 묻기 |
| `customer.name` | 성명 | text | 3쪽 [221, 455, 300, 476] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `person`) | fields.json:1281 | 묻기 |
| `제품명` | 제품명 | text | 5쪽 [84, 399, 160, 423] | 늘 | 파일 key | 값 종류 `goods` | fields.json:1906 | 묻기 |
| `판매처` | 판매처 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1922 | 묻기 |
| `판매조건` | 판매조건 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1983 | 묻기 |
| `원재료명` | 원재료명 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:1999 | 묻기 |
| `구매처` | 구매처 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:2015 | 묻기 |
| `구매조건` | 구매조건 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:2076 | 묻기 |

## 표 `사업모델및특성_목록` (표 과제 table·table_read·table_find·table_qa) — 3열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `사업모델및특성_목록.*.모델명` | 모델명 | text | 2쪽 [251, 356, 325, 379] (1행) | 늘 | 파일 key | 값 종류 `goods` | fields.json:258 | 묻기 |
| `사업모델및특성_목록.*.내용` | 내용 | text | 2쪽 [439, 356, 520, 377] (1행) | 늘 | 파일 key | 값 종류 `note` | fields.json:451 | 묻기 |
| `사업모델및특성_목록.*.특성` | 특성 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:586 | 묻기 |

## 표 `요약재무현황_목록` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `요약재무현황_목록.*.년` | 년 | text | - (1행) | 늘 | 파일 key | 값 종류 `skip` | fields.json:661 | 묻기 |

## 표 `관계_목록` (표 과제 table·table_read·table_find·table_qa) — 5열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `관계_목록.*.주주명` | 주주명 | text | 3쪽 [66, 150, 116, 172] (1행) | 늘 | 파일 key | 값 종류 `person` | fields.json:771 | 묻기 |
| `관계_목록.*.소유주식수` | 소유주식수 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:861 | 묻기 |
| `관계_목록.*.지분율` | 지분율 | number | 3쪽 [526, 149, 549, 171] (1행) | 늘 | 파일 key | 값 종류 `percent` | fields.json:951 | 묻기 |
| `관계_목록.*.대주주와의관계` | 대주주와의관계 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:1056 | 묻기 |
| `관계_목록.*.회사와의관계` | 회사와의관계 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:1161 | 묻기 |

## 표 `대표자_목록` (표 과제 table·table_read·table_find·table_qa) — 4열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `대표자_목록.*.성명` | 성명 | text | 3쪽 [64, 486, 114, 508] (1행) | 늘 | 파일 key | 값 종류 `person` | fields.json:1266 | 묻기 |
| `대표자_목록.*.직위` | 직위 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:1486 | 묻기 |
| `대표자_목록.*.관계` | 관계 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:1606 | 묻기 |
| `대표자_목록.*.주요경력` | 주요경력 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:1666 | 묻기 |

## 표 `주요경력_목록` (표 과제 table·table_read·table_find·table_qa) — 4열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `주요경력_목록.*.기간` | 기간 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:1294 | 묻기 |
| `주요경력_목록.*.근무처` | 근무처 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:1342 | 묻기 |
| `주요경력_목록.*.담당업무` | 담당업무 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:1390 | 묻기 |
| `주요경력_목록.*.최종직위` | 최종직위 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:1438 | 묻기 |

## 표 `연월일_목록` (표 과제 table·table_read·table_find·table_qa) — 2열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `연월일_목록.*.연월일` | 연월일 | date | 4쪽 [61, 156, 155, 179] (1행) | 늘 | 파일 key | 값 종류 `date` | fields.json:1726 | 묻기 |
| `연월일_목록.*.내용` | 내용 | text | 4쪽 [223, 156, 305, 178] (1행) | 늘 | 파일 key | 값 종류 `note` | fields.json:1816 | 묻기 |

## 표 `연간판매금액_목록` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `연간판매금액_목록.*.년` | 년 | text | - (1행) | 늘 | 파일 key | 값 종류 `skip` | fields.json:1938 | 묻기 |

## 체크·도장·서명 (marks) — 4칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.signer` | 대표이사 | seal | 1쪽 [682, 439, 712, 455] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:81 | 묻기 |
| `sign.signer` | 대표이사 | signature | 1쪽 [682, 439, 712, 455] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:81 | 묻기 |
| `seal.signer2` | 성명 | seal | 1쪽 [681, 578, 715, 593] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:113 | 묻기 |
| `sign.signer2` | 성명 | signature | 1쪽 [681, 578, 715, 593] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:113 | 묻기 |

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
"기업현황서(B2B전자결제서비스 업무, MP용)"
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
 "화학제품",
 "의류 원단",
 "화장품",
 "702-81-38348",
 "신한은행",
 "81,710,000",
 "해당 없음",
 "남궁예태",
 "051-509-1176",
 "200112-7951835",
 "하나은행",
 "우리은행"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"해당 없음"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"051-509-1176"
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
- company.name2: 기업체명
- company.biz_item: 업종(표준산업분류기호)
- company.biz_no: 사업자등록번호
- 주거래은행: 주거래은행
- 매출액: 매출액
- company.ceo: 대표자
- FAX2: FAX
- company.corp_no: 법인등록번호
- 정부기관및금융기관우대: 정부기관및금융기관우대
- 당좌거래은행: 당좌거래은행
```

답:

```json
[{"key": "company.name2", "value": "(주)미래케미칼", "bbox_2d": [254, 102, 383, 124], "page": 1},
 {"key": "company.biz_item", "value": "화학제품", "bbox_2d": [252, 247, 327, 269], "page": 1},
 {"key": "company.biz_no", "value": "702-81-38348", "bbox_2d": [255, 466, 377, 489], "page": 1},
 {"key": "주거래은행", "value": "신한은행", "bbox_2d": [257, 831, 325, 853], "page": 1},
 {"key": "매출액", "value": "81,710,000", "bbox_2d": [583, 720, 672, 742], "page": 1},
 {"key": "company.ceo", "value": "남궁예태", "bbox_2d": [686, 101, 765, 123], "page": 1},
 {"key": "FAX2", "value": "051-509-1176", "bbox_2d": [681, 159, 795, 182], "page": 1},
 {"key": "company.corp_no", "value": "200112-7951835", "bbox_2d": [683, 466, 819, 488], "page": 1},
 {"key": "정부기관및금융기관우대", "value": "하나은행", "bbox_2d": [679, 502, 751, 525], "page": 1},
 {"key": "당좌거래은행", "value": "우리은행", "bbox_2d": [683, 831, 745, 852], "page": 1}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 '모델명'·'내용' 열이 있는 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 설명)
- 모델명: 모델명
- 내용: 내용
```

답:

```json
{
 "columns": [
  "모델명",
  "내용"
 ],
 "rows": [
  [
   "의류 원단",
   "해당 없음"
  ],
  [
   "화장품",
   "해당 없음"
  ],
  [
   "의류 원단",
   "해당 없음"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    251,
    356,
    520,
    379
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    254,
    394,
    520,
    415
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    251,
    429,
    524,
    452
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
[{"columns": ["모델명", "내용"], "bbox_2d": [251, 356, 524, 452], "page": 1, "n_rows": 3}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '모델명'·'내용' 열이 있는 표를 보고 답하세요. 위에서 1번째 행의 '내용' 값은 무엇입니까? 머리글은 세지 않습니다. (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"해당 없음"
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '모델명'·'내용' 열이 있는 표를 보고 답하세요. 표의 행은 모두 몇 개입니까? 머리글·합계 행과 모두 빈 행은 세지 않습니다. (숫자만 답하세요)
```

답:

```json
3
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf102 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf102` → `python -m docgen.formdir card hf102` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf102 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf102 --show` · `python -m docgen.preview hf102 --out work/hf102`
