# 대여금고(신규·변경·해지)신청서 (`hf025`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf025 · card-hash: 9d9e1cf2e608 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 대여금고(신규·변경·해지)신청서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf025 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.25 (예금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 20칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `금고번호` | 금고번호 | rrn | 1쪽 [183, 200, 300, 216] | 늘 | 파일 key | 값 종류 `number` | fields.json:67 | 묻기 |
| `보증금` | 보증금 | number | 1쪽 [481, 199, 566, 217] | 늘 | 파일 key | 값 종류 `amount` | fields.json:81 | 묻기 |
| `원` | 원 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:96 | 묻기 |
| `signer.name` | 성명 | text | 1쪽 [266, 470, 347, 489] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:111 | 묻기 |
| `agent.birth` | 생년월일 | date | 1쪽 [211, 496, 301, 515] | 늘 | 파일 key | 고객 정보 (키 `agent.birth`, 없으면 값 종류 `date`) | fields.json:131 | 묻기 |
| `agent.phone` | 연락처 | phone | 1쪽 [210, 524, 333, 542] | 늘 | 파일 key | 고객 정보 (키 `agent.phone`, 없으면 값 종류 `phone`) | fields.json:145 | 묻기 |
| `agent.address` | 주소 | text | 1쪽 [214, 555, 434, 567] | 늘 | 파일 key | 고객 정보 (키 `agent.address`, 없으면 값 종류 `address`) | fields.json:160 | 묻기 |
| `agent.relation` | 관계 | text | 1쪽 [447, 496, 467, 514] | 늘 | 파일 key | 고객 정보 (키 `agent.relation`, 없으면 값 종류 `text`) | fields.json:175 | 묻기 |
| `signer2.name` | 성명 | text | 1쪽 [696, 471, 775, 489] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:189 | 묻기 |
| `agent.birth2` | 생년월일 | date | 1쪽 [638, 496, 727, 515] | 늘 | 파일 key | 고객 정보 (키 `agent.birth`, 없으면 값 종류 `date`) | fields.json:209 | 묻기 |
| `agent.phone2` | 연락처 | phone | 1쪽 [639, 525, 762, 543] | 늘 | 파일 key | 고객 정보 (키 `agent.phone`, 없으면 값 종류 `phone`) | fields.json:223 | 묻기 |
| `agent.address2` | 주소 | text | 1쪽 [638, 553, 859, 567] | 늘 | 파일 key | 고객 정보 (키 `agent.address`, 없으면 값 종류 `address`) | fields.json:238 | 묻기 |
| `agent.relation2` | 관계 | text | 1쪽 [875, 497, 896, 515] | 늘 | 파일 key | 고객 정보 (키 `agent.relation`, 없으면 값 종류 `text`) | fields.json:253 | 묻기 |
| `customer.name` | 성명(사업자명) | text | 1쪽 [214, 604, 293, 621] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `person`) | fields.json:267 | 묻기 |
| `customer.phone` | 연락처 | phone | 1쪽 [210, 631, 333, 651] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:281 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [210, 653, 617, 681] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:296 | 묻기 |
| `signer3.name` | 성명(사업자명) | text | 1쪽 [556, 818, 635, 835] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:311 | 묻기 |
| `customer.birth` | 생년월일(사업자번호) | date | 1쪽 [616, 605, 718, 623] | 늘 | 파일 key | 고객 정보 (키 `customer.birth`, 없으면 값 종류 `date`) | fields.json:331 | 묻기 |
| `customer.email` | e-mail | text | 1쪽 [613, 630, 797, 650] | 늘 | 파일 key | 고객 정보 (키 `customer.email`, 없으면 값 종류 `text`) | fields.json:345 | 묻기 |
| `date` | 작성일 | date | 1쪽 [362, 434, 567, 452] | 늘 | 파일 key | 작성일 | fields.json:360 | 묻기 |

## 체크·도장·서명 (marks) — 14칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.signer` | 성명 | seal | 1쪽 [412, 472, 474, 486] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:111 | 묻기 |
| `sign.signer` | 성명 | signature | 1쪽 [412, 472, 474, 486] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:111 | 묻기 |
| `seal.signer2` | 성명 | seal | 1쪽 [842, 458, 901, 500] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:189 | 묻기 |
| `sign.signer2` | 성명 | signature | 1쪽 [840, 472, 902, 486] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:189 | 묻기 |
| `seal.signer3` | 성명(사업자명) | seal | 1쪽 [829, 804, 888, 846] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:311 | 묻기 |
| `sign.signer3` | 성명(사업자명) | signature | 1쪽 [827, 818, 889, 833] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:311 | 묻기 |
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [649, 46, 686, 72] | 늘 | - | - | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [632, 41, 703, 78] | 늘 | - | - | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [771, 41, 825, 78] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [771, 41, 825, 78] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [825, 41, 875, 78] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [825, 41, 875, 78] | 늘 | - | - | - | 묻기 |
| `seal.staff.부점장` | 부점장 | seal | 1쪽 [875, 41, 925, 78] | 늘 | - | - | - | 묻기 |
| `sign.staff.부점장` | 부점장 | signature | 1쪽 [875, 41, 925, 78] | 늘 | - | - | - | 묻기 |

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
"대여금고(신규·변경·해지)신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "146357-3725869",
 "1,230,000",
 "남궁예태",
 "1952.10.28",
 "010-7568-9115",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "부",
 "010-6144-1173",
 "1985-03-28",
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
"010-7568-9115"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"1985-03-28"
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
- 금고번호: 금고번호
- 보증금: 보증금
- signer.name: 성명 (같은 설명 중 1번째 칸)
- agent.birth: 생년월일 (같은 설명 중 1번째 칸)
- agent.phone: 연락처 (같은 설명 중 1번째 칸)
- agent.address: 주소 (같은 설명 중 1번째 칸)
- agent.relation: 관계 (같은 설명 중 1번째 칸)
- signer2.name: 성명 (같은 설명 중 2번째 칸)
- agent.birth2: 생년월일 (같은 설명 중 2번째 칸)
- agent.phone2: 연락처 (같은 설명 중 2번째 칸)
- agent.address2: 주소 (같은 설명 중 2번째 칸)
- agent.relation2: 관계 (같은 설명 중 2번째 칸)
- customer.name: 성명(사업자명) (같은 설명 중 1번째 칸)
- customer.phone: 연락처 (같은 설명 중 3번째 칸)
- customer.address: 주소 (같은 설명 중 3번째 칸)
- signer3.name: 성명(사업자명) (같은 설명 중 2번째 칸)
- customer.birth: 생년월일(사업자번호)
- customer.email: e-mail
- date: 작성일
```

답:

```json
[{"key": "금고번호", "value": "146357-3725869", "bbox_2d": [183, 200, 300, 216], "page": 1},
 {"key": "보증금", "value": "1,230,000", "bbox_2d": [481, 199, 566, 217], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [266, 470, 347, 489], "page": 1},
 {"key": "agent.birth", "value": "1952.10.28", "bbox_2d": [211, 496, 301, 515], "page": 1},
 {"key": "agent.phone", "value": "010-7568-9115", "bbox_2d": [210, 524, 333, 542], "page": 1},
 {"key": "agent.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [214, 555, 434, 567], "page": 1},
 {"key": "agent.relation", "value": "부", "bbox_2d": [447, 496, 467, 514], "page": 1},
 {"key": "signer2.name", "value": "남궁예태", "bbox_2d": [696, 471, 775, 489], "page": 1},
 {"key": "agent.birth2", "value": "1952.10.28", "bbox_2d": [638, 496, 727, 515], "page": 1},
 {"key": "agent.phone2", "value": "010-7568-9115", "bbox_2d": [639, 525, 762, 543], "page": 1},
 {"key": "agent.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [638, 553, 859, 567], "page": 1},
 {"key": "agent.relation2", "value": "부", "bbox_2d": [875, 497, 896, 515], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [214, 604, 293, 621], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [210, 631, 333, 651], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [210, 653, 617, 681], "page": 1},
 {"key": "signer3.name", "value": "남궁예태", "bbox_2d": [556, 818, 635, 835], "page": 1},
 {"key": "customer.birth", "value": "1985-03-28", "bbox_2d": [616, 605, 718, 623], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [613, 630, 797, 650], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [362, 434, 567, 452], "page": 1}]
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
- seal.signer: 성명 (같은 설명 중 1번째 칸, 도장)
- sign.signer: 성명 (같은 설명 중 2번째 칸, 서명)
- seal.signer2: 성명 (같은 설명 중 3번째 칸, 도장)
- sign.signer2: 성명 (같은 설명 중 4번째 칸, 서명)
- seal.signer3: 성명(사업자명) (같은 설명 중 1번째 칸, 도장)
- sign.signer3: 성명(사업자명) (같은 설명 중 2번째 칸, 서명)
- seal.staff.본인확인: 본인확인 (같은 설명 중 1번째 칸, 도장)
- sign.staff.본인확인: 본인확인 (같은 설명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 설명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 설명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 설명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 설명 중 2번째 칸, 서명)
- seal.staff.부점장: 부점장 (같은 설명 중 1번째 칸, 도장)
- sign.staff.부점장: 부점장 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.signer", "value": false},
 {"key": "sign.signer", "value": false},
 {"key": "seal.signer2", "value": true, "bbox_2d": [842, 458, 901, 500], "page": 1},
 {"key": "sign.signer2", "value": false},
 {"key": "seal.signer3", "value": true, "bbox_2d": [829, 804, 888, 846], "page": 1},
 {"key": "sign.signer3", "value": false},
 {"key": "seal.staff.본인확인", "value": true, "bbox_2d": [649, 46, 686, 72], "page": 1},
 {"key": "sign.staff.본인확인", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": true, "bbox_2d": [771, 41, 825, 78], "page": 1},
 {"key": "seal.staff.책임자", "value": false},
 {"key": "sign.staff.책임자", "value": true, "bbox_2d": [825, 41, 875, 78], "page": 1},
 {"key": "seal.staff.부점장", "value": false},
 {"key": "sign.staff.부점장", "value": true, "bbox_2d": [875, 41, 925, 78], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf025 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf025` → `python -m docgen.formdir card hf025` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf025 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf025 --show` · `python -m docgen.preview hf025 --out work/hf025`
