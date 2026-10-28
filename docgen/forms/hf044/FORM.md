# 예금(신탁) 양도승낙 의뢰서 및 양도승낙서 (`hf044`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf044 · card-hash: ec3c8391628b -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 예금(신탁) 양도승낙 의뢰서 및 양도승낙서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.44 (예금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 26칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `customer.name` | 예금주(양도인)(위탁자겸수익자) | text | 1쪽 [297, 411, 375, 432] | 늘 | 규칙: '예금주(양도인) (위탁자겸 수익자)' → `customer.name` | 고객 정보 (키 `customer.name`) | fields.json:111 | 묻기 |
| `deposit.product` | 예금(신탁)종별 | text | 1쪽 [291, 449, 369, 470] | 늘 | 파일 key | 고객 정보 (키 `deposit.product`) | fields.json:122 | 묻기 |
| `deposit.amount` | 금액 | amount | 1쪽 [818, 479, 916, 500] | 늘 | 파일 key | 고객 정보 (키 `deposit.amount`) | fields.json:136 | 묻기 |
| `account` | 계좌번호 | account_no | 1쪽 [294, 510, 466, 534] | 늘 | 규칙: '계 좌 번 호' → `account` | 고객 정보 (키 `account`) | fields.json:150 | 묻기 |
| `deposit.due_date` | 만기일 | date | 1쪽 [293, 541, 387, 562] | 늘 | 파일 key | 고객 정보 (키 `deposit.due_date`) | fields.json:161 | 묻기 |
| `date` | 작성일 | date | 1쪽 [358, 631, 582, 649] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:175 | 묻기 |
| `signer.name` | 명 | text | 1쪽 [471, 749, 549, 770] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:200 | 묻기 |
| `signer2.name` | 명 | text | 1쪽 [473, 891, 551, 912] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:217 | 묻기 |
| `date3` | 작성일(년월일) | date | 1쪽 [313, 633, 409, 645] | 늘 | 파일 key | 고객 정보 (키 `date`) | fields.json:351 | 묻기 |
| `customer.address` | 양도인주소 | text | 1쪽 [414, 692, 790, 714] | 늘 | 파일 key | 고객 정보 (키 `customer.address`) | fields.json:364 | 묻기 |
| `customer.birth2` | 양도인생년월일(사업자등록번호) | date | 1쪽 [483, 721, 626, 742] | 늘 | 파일 key | 고객 정보 (키 `customer.birth`) | fields.json:377 | 묻기 |
| `customer.name2` | 양도인성명 | text | 1쪽 [364, 750, 443, 772] | 늘 | 파일 key | 고객 정보 (키 `customer.name`) | fields.json:390 | 묻기 |
| `related.address` | 양수인주소 | text | 1쪽 [413, 834, 788, 856] | 늘 | 파일 key | 고객 정보 (키 `related.address`) | fields.json:403 | 묻기 |
| `related.birth2` | 양수인생년월일(사업자등록번호) | date | 1쪽 [484, 863, 601, 886] | 늘 | 파일 key | 고객 정보 (키 `related.birth`) | fields.json:417 | 묻기 |
| `related.name` | 양수인성명 | text | 1쪽 [365, 892, 427, 914] | 늘 | 파일 key | 고객 정보 (키 `related.name`) | fields.json:431 | 묻기 |
| `deposit.product2` | 예금(신탁)종별 | text | 2쪽 [290, 394, 427, 415] | 늘 | 파일 key | 고객 정보 (키 `deposit.product`) | fields.json:234 | 묻기 |
| `deposit.amount2` | 금액 | amount | 2쪽 [810, 424, 915, 447] | 늘 | 파일 key | 고객 정보 (키 `deposit.amount`) | fields.json:248 | 묻기 |
| `account2` | 계좌번호 | account_no | 2쪽 [293, 455, 465, 476] | 늘 | 규칙: '계 좌 번 호' → `account` | 고객 정보 (키 `account`) | fields.json:262 | 묻기 |
| `deposit.due_date2` | 만기일 | date | 2쪽 [290, 485, 433, 508] | 늘 | 파일 key | 고객 정보 (키 `deposit.due_date`) | fields.json:273 | 묻기 |
| `date2` | 작성일 | date | 2쪽 [358, 674, 582, 692] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:287 | 묻기 |
| `customer.birth` | 생년월일(사업자등록번호) | date | 2쪽 [301, 284, 444, 305] | 늘 | 규칙: '생년월일(사업자등록번호)' → `customer.birth` | 고객 정보 (키 `customer.birth`) | fields.json:324 | 묻기 |
| `related.birth` | 생년월일(사업자등록번호) | date | 2쪽 [299, 359, 397, 380] | 늘 | 파일 key | 고객 정보 (키 `related.birth`) | fields.json:336 | 묻기 |
| `related.name2` | 양수인귀하 | text | 2쪽 [133, 175, 193, 196] | 늘 | 파일 key | 고객 정보 (키 `related.name`) | fields.json:444 | 묻기 |
| `customer.name3` | 양도인성명(상호) | text | 2쪽 [296, 250, 375, 272] | 늘 | 파일 key | 고객 정보 (키 `customer.name`) | fields.json:457 | 묻기 |
| `related.name3` | 양수인성명(상호) | text | 2쪽 [295, 323, 357, 345] | 늘 | 파일 key | 고객 정보 (키 `related.name`) | fields.json:470 | 묻기 |
| `date4` | 승낙일(년월일) | date | 2쪽 [311, 677, 407, 689] | 늘 | 파일 key | 고객 정보 (키 `date`) | fields.json:483 | 묻기 |

## 체크·도장·서명 (marks) — 22칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.customer` ← `seal.signer` | 명 | seal | 1쪽 [678, 752, 708, 768] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:200 | 묻기 |
| `sign.customer` ← `sign.signer` | 명 | signature | 1쪽 [678, 752, 708, 768] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:200 | 묻기 |
| `seal.signer2` | 명 | seal | 1쪽 [675, 883, 712, 922] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:217 | 묻기 |
| `sign.signer2` | 명 | signature | 1쪽 [678, 895, 708, 911] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:217 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [669, 46, 714, 78] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [659, 40, 725, 84] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [736, 46, 780, 77] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [725, 40, 791, 84] | 늘 | - | - | - | 묻기 |
| `seal.staff.관리자` | 관리자 | seal | 1쪽 [791, 40, 848, 84] | 늘 | - | - | - | 묻기 |
| `sign.staff.관리자` | 관리자 | signature | 1쪽 [791, 40, 848, 84] | 늘 | - | - | - | 묻기 |
| `seal.staff.부점장` | 부점장 | seal | 1쪽 [848, 40, 920, 84] | 늘 | - | - | - | 묻기 |
| `sign.staff.부점장` | 부점장 | signature | 1쪽 [848, 40, 920, 84] | 늘 | - | - | - | 묻기 |
| `seal.signer3` | 부점장 | seal | 2쪽 [712, 765, 742, 781] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:312 | 묻기 |
| `sign.signer3` | 부점장 | signature | 2쪽 [712, 765, 742, 781] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:312 | 묻기 |
| `seal.staff.담당2` | 담당 | seal | 2쪽 [671, 47, 713, 76] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당2` | 담당 | signature | 2쪽 [659, 40, 725, 84] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자2` | 책임자 | seal | 2쪽 [725, 40, 791, 84] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자2` | 책임자 | signature | 2쪽 [725, 40, 791, 84] | 늘 | - | - | - | 묻기 |
| `seal.staff.관리자2` | 관리자 | seal | 2쪽 [798, 46, 842, 77] | 늘 | - | - | - | 묻기 |
| `sign.staff.관리자2` | 관리자 | signature | 2쪽 [791, 40, 848, 84] | 늘 | - | - | - | 묻기 |
| `seal.staff.부점장2` | 부점장 | seal | 2쪽 [848, 40, 919, 84] | 늘 | - | - | - | 묻기 |
| `sign.staff.부점장2` | 부점장 | signature | 2쪽 [848, 40, 919, 84] | 늘 | - | - | - | 묻기 |

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
"예금(신탁) 양도승낙 의뢰서 및 양도승낙서"
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
 "하나 적금",
 "4,770,000",
 "540-121210-96628",
 "2024.10.10",
 "2025년 04월 01일",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "1985년 3월 28일",
 "2024-03-01",
 "김경예",
 "주거래하나 통장",
 "67,070,000",
 "2025년 1월 12일",
 "2024.10.23"
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
"2024-03-01"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- customer.name: 예금주(양도인)(위탁자겸수익자) (고객 성명)
- deposit.product: 예금(신탁)종별 (같은 항목명 중 1번째 칸)
- deposit.amount: 금액 (같은 항목명 중 1번째 칸)
- account: 계좌번호 (같은 항목명 중 1번째 칸)
- deposit.due_date: 만기일 (같은 항목명 중 1번째 칸)
- date: 작성일 (같은 항목명 중 1번째 칸)
- signer.name: 명 (고객 본인의 성명, 같은 항목명 중 1번째 칸)
- signer2.name: 명 (같은 항목명 중 2번째 칸)
- date3: 작성일(년월일)
- customer.address: 양도인주소 (고객 주소)
- customer.birth2: 양도인생년월일(사업자등록번호)
- customer.name2: 양도인성명
- related.address: 양수인주소 (보증인·공동 주소)
- related.birth2: 양수인생년월일(사업자등록번호)
- related.name: 양수인성명 (보증인·공동 성명)
- deposit.product2: 예금(신탁)종별 (같은 항목명 중 2번째 칸)
- deposit.amount2: 금액 (같은 항목명 중 2번째 칸)
- account2: 계좌번호 (같은 항목명 중 2번째 칸)
- deposit.due_date2: 만기일 (같은 항목명 중 2번째 칸)
- date2: 작성일 (같은 항목명 중 2번째 칸)
- customer.birth: 생년월일(사업자등록번호) (고객 생년월일, 같은 항목명 중 1번째 칸)
- related.birth: 생년월일(사업자등록번호) (같은 항목명 중 2번째 칸)
- related.name2: 양수인귀하
- customer.name3: 양도인성명(상호)
- related.name3: 양수인성명(상호)
- date4: 승낙일(년월일)
```

답:

```json
[{"key": "customer.name", "value": "남궁예태", "bbox_2d": [297, 411, 375, 432], "page": 1},
 {"key": "deposit.product", "value": "하나 적금", "bbox_2d": [291, 449, 369, 470], "page": 1},
 {"key": "deposit.amount", "value": "4,770,000", "bbox_2d": [818, 479, 916, 500], "page": 1},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [294, 510, 466, 534], "page": 1},
 {"key": "deposit.due_date", "value": "2024.10.10", "bbox_2d": [293, 541, 387, 562], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [358, 631, 582, 649], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [471, 749, 549, 770], "page": 1},
 {"key": "signer2.name", "value": "남궁예태", "bbox_2d": [473, 891, 551, 912], "page": 1},
 {"key": "date3", "value": "2025년 04월 01일", "bbox_2d": [313, 633, 409, 645], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [414, 692, 790, 714], "page": 1},
 {"key": "customer.birth2", "value": "1985년 3월 28일", "bbox_2d": [483, 721, 626, 742], "page": 1},
 {"key": "customer.name2", "value": "남궁예태", "bbox_2d": [364, 750, 443, 772], "page": 1},
 {"key": "related.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [413, 834, 788, 856], "page": 1},
 {"key": "related.birth2", "value": "2024-03-01", "bbox_2d": [484, 863, 601, 886], "page": 1},
 {"key": "related.name", "value": "김경예", "bbox_2d": [365, 892, 427, 914], "page": 1},
 {"key": "deposit.product2", "value": "주거래하나 통장", "bbox_2d": [290, 394, 427, 415], "page": 2},
 {"key": "deposit.amount2", "value": "67,070,000", "bbox_2d": [810, 424, 915, 447], "page": 2},
 {"key": "account2", "value": "540-121210-96628", "bbox_2d": [293, 455, 465, 476], "page": 2},
 {"key": "deposit.due_date2", "value": "2025년 1월 12일", "bbox_2d": [290, 485, 433, 508], "page": 2},
 {"key": "date2", "value": "2025년 4월 1일", "bbox_2d": [358, 674, 582, 692], "page": 2},
 {"key": "customer.birth", "value": "1985년 3월 28일", "bbox_2d": [301, 284, 444, 305], "page": 2},
 {"key": "related.birth", "value": "2024.10.23", "bbox_2d": [299, 359, 397, 380], "page": 2},
 {"key": "related.name2", "value": "김경예", "bbox_2d": [133, 175, 193, 196], "page": 2},
 {"key": "customer.name3", "value": "남궁예태", "bbox_2d": [296, 250, 375, 272], "page": 2},
 {"key": "related.name3", "value": "김경예", "bbox_2d": [295, 323, 357, 345], "page": 2},
 {"key": "date4", "value": "2025년 04월 01일", "bbox_2d": [311, 677, 407, 689], "page": 2}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.customer: 명 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 명 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.signer2: 명 (같은 항목명 중 3번째 칸, 도장)
- sign.signer2: 명 (같은 항목명 중 4번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.관리자: 관리자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.관리자: 관리자 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.부점장: 부점장 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.부점장: 부점장 (같은 항목명 중 2번째 칸, 서명)
- seal.signer3: 부점장 (은행·직원의 신청인, 같은 항목명 중 3번째 칸, 도장)
- sign.signer3: 부점장 (은행·직원의 신청인, 같은 항목명 중 4번째 칸, 서명)
- seal.staff.담당2: 담당 (같은 항목명 중 3번째 칸, 도장)
- sign.staff.담당2: 담당 (같은 항목명 중 4번째 칸, 서명)
- seal.staff.책임자2: 책임자 (같은 항목명 중 3번째 칸, 도장)
- sign.staff.책임자2: 책임자 (같은 항목명 중 4번째 칸, 서명)
- seal.staff.관리자2: 관리자 (같은 항목명 중 3번째 칸, 도장)
- sign.staff.관리자2: 관리자 (같은 항목명 중 4번째 칸, 서명)
- seal.staff.부점장2: 부점장 (같은 항목명 중 5번째 칸, 도장)
- sign.staff.부점장2: 부점장 (같은 항목명 중 6번째 칸, 서명)
```

답:

```json
[{"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": false},
 {"key": "seal.signer2", "value": true, "bbox_2d": [675, 883, 712, 922], "page": 1},
 {"key": "sign.signer2", "value": false},
 {"key": "seal.staff.담당", "value": true, "bbox_2d": [669, 46, 714, 78], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [736, 46, 780, 77], "page": 1},
 {"key": "sign.staff.책임자", "value": false},
 {"key": "seal.staff.관리자", "value": false},
 {"key": "sign.staff.관리자", "value": false},
 {"key": "seal.staff.부점장", "value": false},
 {"key": "sign.staff.부점장", "value": false},
 {"key": "seal.signer3", "value": false},
 {"key": "sign.signer3", "value": true, "bbox_2d": [712, 765, 742, 781], "page": 2},
 {"key": "seal.staff.담당2", "value": true, "bbox_2d": [671, 47, 713, 76], "page": 2},
 {"key": "sign.staff.담당2", "value": false},
 {"key": "seal.staff.책임자2", "value": false},
 {"key": "sign.staff.책임자2", "value": true, "bbox_2d": [725, 40, 791, 84], "page": 2},
 {"key": "seal.staff.관리자2", "value": true, "bbox_2d": [798, 46, 842, 77], "page": 2},
 {"key": "sign.staff.관리자2", "value": false},
 {"key": "seal.staff.부점장2", "value": false},
 {"key": "sign.staff.부점장2", "value": true, "bbox_2d": [848, 40, 919, 84], "page": 2}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf044` → `python -m docgen.formdir card hf044` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf044 --show` · `python -m docgen.preview hf044 --out work/hf044`
