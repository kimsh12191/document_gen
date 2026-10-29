# 외화송금의 내용변경 및 취소, 송금수표 분실신고 등 신청서 (`hf234`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf234 · card-hash: 4c3e1003a266 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 외화송금의 내용변경 및 취소, 송금수표 분실신고 등 신청서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf234 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.234 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 17칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `송금일자` | 송금일자 | date | 1쪽 [313, 262, 390, 273] | 늘 | 항목명 그대로 | 값 종류 `date` (항목명 자동) | fields.json:88 | 묻기 |
| `송금번호` | 송금번호(수표번호) | rrn | 1쪽 [315, 289, 430, 300] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:99 | 묻기 |
| `수취인` | 수취인 | text | 1쪽 [315, 316, 418, 327] | 늘 | 항목명 그대로 | 값 종류 `company` (항목명 자동) | fields.json:110 | 묻기 |
| `value` | [전신송금내용변경기재란] | amount | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:121 | 묻기 |
| `거래은행` | 거래은행 | text | 1쪽 [316, 524, 377, 534] | 늘 | 항목명 그대로 | 값 종류 `bank` (항목명 자동) | fields.json:222 | 묻기 |
| `foreign.account` | 계좌번호 | account_no | 1쪽 [313, 551, 432, 561] | 늘 | 규칙: '계좌번호' → `foreign.account` | 고객 정보 (키 `foreign.account`) | fields.json:234 | 묻기 |
| `foreign.name` | 성명 | text | 1쪽 [313, 577, 497, 588] | 늘 | 규칙: '성명' → `foreign.name` | 고객 정보 (키 `foreign.name`) | fields.json:246 | 묻기 |
| `foreign.address` | 주소 | text | 1쪽 [314, 606, 543, 613] | 늘 | 규칙: '주소' → `foreign.address` | 고객 정보 (키 `foreign.address`) | fields.json:258 | 묻기 |
| `foreign.phone` | 전화번호 | text | 1쪽 [316, 631, 390, 642] | 늘 | 규칙: '전화번호' → `foreign.phone` | 고객 정보 (키 `foreign.phone`) | fields.json:270 | 묻기 |
| `기타` | 기타(사유등) | text | 1쪽 [317, 658, 382, 669] | 늘 | 항목명 그대로 | 값 종류 `note` (항목명 자동) | fields.json:282 | 묻기 |
| `변경후` | 변경후 | text | 1쪽 [624, 658, 690, 669] | 늘 | 표 행 (묶음·항목명 '변경후') | 값 종류 `note` (항목명 자동) | fields.json:363 | 묻기 |
| `송금인` | 송금인 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:375 | 묻기 |
| `customer.birth` | 생년월일/사업자번호 | number | 1쪽 [318, 794, 370, 805] | 늘 | 규칙: '생년월일 / 사업자번호' → `customer.birth` | 고객 정보 (키 `customer.birth`) | fields.json:387 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [317, 821, 643, 831] | 늘 | 규칙: '주소' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:398 | 묻기 |
| `customer.phone` | 전화번호 | phone | 1쪽 [315, 848, 419, 858] | 늘 | 규칙: '전화번호' → `customer.phone` | 고객 정보 (키 `customer.phone`) | fields.json:409 | 묻기 |
| `customer.email` | E-mail주소 | text | 1쪽 [319, 874, 467, 885] | 늘 | 규칙: 'E-mail 주소' → `customer.email` | 고객 정보 (키 `customer.email`) | fields.json:420 | 묻기 |
| `date` | 작성일 | date | 1쪽 [717, 732, 912, 749] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:431 | 묻기 |

## 표 `수취인_목록` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `수취인_목록.*.변경후` | 변경후 | text | 1쪽 [623, 524, 689, 534] (1행) | 늘 | 표 행 (묶음·항목명 '변경후') | 값 종류 `note` (항목명 자동) | fields.json:293 | 묻기 |

## 체크·도장·서명 (marks) — 7칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.송금방법` | 송금방법 | checkbox (전신송금(T/T) / 송금수표(D/D)) | 1쪽 [486, 232, 600, 248] | 늘 | 체크 (항목명) | 보기 중 고름: 전신송금(T/T) / 송금수표(D/D) | fields.json:43 | 묻기 |
| `check.전신송금` | 전신송금 | checkbox (전신송금 지급여부조회 / 전신송금 내용변경 / 전신송금 취소) | 1쪽 [547, 373, 688, 388] | 늘 | 체크 (항목명) | 보기 중 고름: 전신송금 지급여부조회 / 전신송금 내용변경 / 전신송금 취소 | fields.json:132 | 묻기 |
| `check.송금수표` | 송금수표 | checkbox (송금수표 분실신고) | 1쪽 [324, 400, 466, 415] | 늘 | 체크 (항목명) | 보기 중 고름: 송금수표 분실신고 | fields.json:193 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [796, 154, 837, 183] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [785, 147, 848, 191] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [861, 152, 910, 186] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [848, 147, 924, 191] | 늘 | - | - | - | 묻기 |

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
"외화송금의 내용변경 및 취소, 송금수표 분실신고 등 신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2024.05.07",
 "597447-2611346",
 "(주)미래케미칼",
 "기업은행",
 "28395786990418",
 "Tokyo Seimitsu Kogyo K.K.",
 "2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 163-0001",
 "John Miller",
 "해당 없음",
 "850328",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "010-6144-1173",
 "yetae741@gmail.com"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"(주)미래케미칼"
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
- 송금일자: 송금일자
- 송금번호: 송금번호(수표번호)
- 수취인: 수취인
- value: [전신송금내용변경기재란]
- 거래은행: 거래은행
- foreign.account: 계좌번호
- foreign.name: 성명 (외국 상대 이름)
- foreign.address: 주소 (외국 상대 주소, 같은 항목명 중 1번째 칸)
- foreign.phone: 전화번호 (같은 항목명 중 1번째 칸)
- 기타: 기타(사유등)
- 변경후: 변경후
- 송금인: 송금인
- customer.birth: 생년월일/사업자번호 (고객 생년월일)
- customer.address: 주소 (고객 주소, 같은 항목명 중 2번째 칸)
- customer.phone: 전화번호 (고객 연락처, 같은 항목명 중 2번째 칸)
- customer.email: E-mail주소 (고객 이메일)
- date: 작성일
```

답:

```json
[{"key": "송금일자", "value": "2024.05.07", "bbox_2d": [313, 262, 390, 273], "page": 1},
 {"key": "송금번호", "value": "597447-2611346", "bbox_2d": [315, 289, 430, 300], "page": 1},
 {"key": "수취인", "value": "(주)미래케미칼", "bbox_2d": [315, 316, 418, 327], "page": 1},
 {"key": "value", "value": null},
 {"key": "거래은행", "value": "기업은행", "bbox_2d": [316, 524, 377, 534], "page": 1},
 {"key": "foreign.account", "value": "28395786990418", "bbox_2d": [313, 551, 432, 561], "page": 1},
 {"key": "foreign.name", "value": "Tokyo Seimitsu Kogyo K.K.", "bbox_2d": [313, 577, 497, 588], "page": 1},
 {"key": "foreign.address", "value": "2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 163-0001", "bbox_2d": [314, 606, 543, 613], "page": 1},
 {"key": "foreign.phone", "value": "John Miller", "bbox_2d": [316, 631, 390, 642], "page": 1},
 {"key": "기타", "value": "해당 없음", "bbox_2d": [317, 658, 382, 669], "page": 1},
 {"key": "변경후", "value": "해당 없음", "bbox_2d": [624, 658, 690, 669], "page": 1},
 {"key": "송금인", "value": null},
 {"key": "customer.birth", "value": "850328", "bbox_2d": [318, 794, 370, 805], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [317, 821, 643, 831], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [315, 848, 419, 858], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [319, 874, 467, 885], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [717, 732, 912, 749], "page": 1}]
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
- check.송금방법: 송금방법 (체크박스, 보기: 전신송금(T/T) / 송금수표(D/D))
- check.전신송금: 전신송금 (체크박스, 보기: 전신송금 지급여부조회 / 전신송금 내용변경 / 전신송금 취소)
- check.송금수표: 송금수표 (체크박스, 보기: 송금수표 분실신고)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.송금방법", "value": "전신송금(T/T)", "bbox_2d": [486, 233, 501, 248], "page": 1},
 {"key": "check.전신송금", "value": "전신송금 내용변경", "bbox_2d": [547, 374, 561, 388], "page": 1},
 {"key": "check.송금수표", "value": "송금수표 분실신고", "bbox_2d": [324, 401, 339, 415], "page": 1},
 {"key": "seal.staff.담당", "value": true, "bbox_2d": [796, 154, 837, 183], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [861, 152, 910, 186], "page": 1},
 {"key": "sign.staff.책임자", "value": false}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[623, 524, 691, 588] 위치의 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 항목명)
- 변경후: 변경후
```

답:

```json
{
 "columns": [
  "변경후"
 ],
 "rows": [
  [
   "해당 없음"
  ],
  [
   "해당 없음"
  ],
  [
   "해당 없음"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    623,
    524,
    689,
    534
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    624,
    551,
    689,
    561
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    625,
    577,
    691,
    588
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
[{"columns": ["변경후"], "bbox_2d": [623, 524, 691, 588], "page": 1, "n_rows": 3}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 표를 보고 답하세요. 위에서 2번째 행의 '변경후' 값은 무엇입니까? 머리글은 세지 않습니다. (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"해당 없음"
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 표를 보고 답하세요. 마지막 행의 '변경후' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"해당 없음"
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf234 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf234` → `python -m docgen.formdir card hf234` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf234 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf234 --show` · `python -m docgen.preview hf234 --out work/hf234`
