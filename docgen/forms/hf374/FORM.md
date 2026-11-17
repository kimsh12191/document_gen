# 전자어음 이용(변경,해지) 신청서 (`hf374`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf374 · card-hash: 0fcb7af4939f -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 전자어음 이용(변경,해지) 신청서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf374 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.374 (전자금융) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 21칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `company.name` | 법인명(성명) | text | 1쪽 [363, 247, 496, 269] | 늘 | 파일 key | 고객 정보 (키 `company.name`, 없으면 값 종류 `company`) | fields.json:183 | 묻기 |
| `company.biz_no` | 사업자등록번호(법인) | biz_no | 1쪽 [367, 274, 536, 300] | 늘 | 파일 key | 고객 정보 (키 `company.biz_no`, 없으면 값 종류 `biz_no`) | fields.json:197 | 묻기 |
| `담당부서` | 담당부서 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:289 | 묻기 |
| `employer.phone` | 회사전화 | phone | 1쪽 [366, 389, 498, 411] | 늘 | 파일 key | 고객 정보 (키 `employer.phone`, 없으면 값 종류 `phone`) | fields.json:304 | 묻기 |
| `FAX` | FAX | phone | 1쪽 [365, 409, 499, 433] | 늘 | 파일 key | 값 종류 `phone` | fields.json:318 | 묻기 |
| `company.ceo` | 대표자 | text | 1쪽 [744, 246, 823, 267] | 늘 | 파일 key | 고객 정보 (키 `company.ceo`, 없으면 값 종류 `text`) | fields.json:333 | 묻기 |
| `company.biz_item` | 업종 | text | 1쪽 [745, 273, 839, 300] | 늘 | 파일 key | 고객 정보 (키 `company.biz_item`, 없으면 값 종류 `text`) | fields.json:347 | 묻기 |
| `대표전화` | 대표전화 | phone | 1쪽 [743, 337, 905, 360] | 늘 | 파일 key | 값 종류 `phone` | fields.json:361 | 묻기 |
| `customer.phone` | 휴대폰 | phone | 1쪽 [745, 390, 893, 412] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:376 | 묻기 |
| `customer.email` | E-Mail | text | 1쪽 [740, 412, 894, 432] | 늘 | 파일 key | 고객 정보 (키 `customer.email`, 없으면 값 종류 `email`) | fields.json:390 | 묻기 |
| `발행지정계좌` | 발행(당좌)지정계좌 | text | 1쪽 [263, 487, 468, 508] | 늘 | 파일 key | 값 종류 `account` | fields.json:404 | 묻기 |
| `수취지정계좌` | 수취(요구불)지정계좌 | text | 1쪽 [271, 508, 463, 530] | 늘 | 파일 key | 값 종류 `account` | fields.json:418 | 묻기 |
| `value` | [변경전] | amount | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:456 | 묻기 |
| `변경항목` | 변경항목 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:470 | 묻기 |
| `value2` | [변경후] | amount | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:484 | 묻기 |
| `취급점` | 취급점 | text | 1쪽 [206, 149, 282, 171] | 늘 | 파일 key | 값 종류 `branch` | fields.json:498 | 묻기 |
| `date` | 작성일 | date | 1쪽 [375, 793, 558, 808] | 늘 | 파일 key | 작성일 | fields.json:512 | 묻기 |
| `signer3.name` | 신청인(대리인) | text | 1쪽 [487, 819, 554, 840] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:538 | 묻기 |
| `징구서류` | •징구서류 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:557 | 묻기 |
| `자택` | 자택()- | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:571 | 묻기 |
| `휴대폰` | 휴대폰()- | phone | 1쪽 [501, 619, 679, 646] | 늘 | 파일 key | 값 종류 `phone` | fields.json:586 | 묻기 |

## 체크·도장·서명 (marks) — 13칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.거래구분` | 거래구분 | checkbox (신규가입 / 변경 / 발행해지 / 전체해지) | 1쪽 [614, 209, 681, 222] | 늘 | 파일 key | 보기 중 고름: 신규가입 / 변경 / 발행해지 / 전체해지 | fields.json:43 | 묻기 |
| `check.회원구분` | 회원구분 | checkbox (발행인(수취,배서포함) / 수취/배서인 / 보증인) | 1쪽 [704, 229, 758, 242] | 늘 | 파일 key | 보기 중 고름: 발행인(수취,배서포함) / 수취/배서인 / 보증인 | fields.json:121 | 묻기 |
| `check.규모` | 규모 | checkbox (대기업 / 중소기업 / 개인사업자 / 개인) | 1쪽 [447, 311, 501, 324] | 늘 | 파일 key | 보기 중 고름: 대기업 / 중소기업 / 개인사업자 / 개인 | fields.json:211 | 묻기 |
| `seal.signer` | 거래인감 | seal | 1쪽 [791, 479, 847, 518] | 늘 | 키 설명 그대로 | 값 종류 `seal` | fields.json:432 | 묻기 |
| `sign.signer` | 거래인감 | signature | 1쪽 [714, 488, 924, 509] | 늘 | 키 설명 그대로 | 값 종류 `seal` | fields.json:432 | 묻기 |
| `seal.signer2` | 거래인감 | seal | 1쪽 [793, 501, 845, 538] | 늘 | 키 설명 그대로 | 값 종류 `seal` | fields.json:444 | 묻기 |
| `sign.signer2` | 거래인감 | signature | 1쪽 [714, 509, 924, 530] | 늘 | 키 설명 그대로 | 값 종류 `seal` | fields.json:444 | 묻기 |
| `seal.signer3` | 신청인(대리인) | seal | 1쪽 [629, 823, 681, 836] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:538 | 묻기 |
| `sign.signer3` | 신청인(대리인) | signature | 1쪽 [629, 823, 681, 836] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:538 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [816, 43, 860, 73] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [805, 38, 872, 78] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [876, 43, 919, 73] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [872, 38, 924, 78] | 늘 | - | - | - | 묻기 |

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
"전자어음 이용(변경,해지) 신청서"
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
 "051-509-1176",
 "남궁예태",
 "화학제품",
 "010-6144-1173",
 "yetae741@gmail.com",
 "016-074772-43224",
 "807-736814-85877",
 "센텀지점",
 "남궁찬윤"
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
"010-6144-1173"
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
- company.name: 법인명(성명)
- company.biz_no: 사업자등록번호(법인)
- 담당부서: 담당부서
- employer.phone: 회사전화
- FAX: FAX
- company.ceo: 대표자
- company.biz_item: 업종
- 대표전화: 대표전화
- customer.phone: 휴대폰 (같은 설명 중 1번째 칸)
- customer.email: E-Mail
- 발행지정계좌: 발행(당좌)지정계좌
- 수취지정계좌: 수취(요구불)지정계좌
- value: [변경전]
- 변경항목: 변경항목
- value2: [변경후]
- 취급점: 취급점
- date: 작성일
- signer3.name: 신청인(대리인)
- 징구서류: •징구서류
- 자택: 자택()-
- 휴대폰: 휴대폰()- (같은 설명 중 2번째 칸)
```

답:

```json
[{"key": "company.name", "value": "(주)미래케미칼", "bbox_2d": [363, 247, 496, 269], "page": 1},
 {"key": "company.biz_no", "value": "702-81-38348", "bbox_2d": [367, 274, 536, 300], "page": 1},
 {"key": "담당부서", "value": null},
 {"key": "employer.phone", "value": "051-509-1176", "bbox_2d": [366, 389, 498, 411], "page": 1},
 {"key": "FAX", "value": "051-509-1176", "bbox_2d": [365, 409, 499, 433], "page": 1},
 {"key": "company.ceo", "value": "남궁예태", "bbox_2d": [744, 246, 823, 267], "page": 1},
 {"key": "company.biz_item", "value": "화학제품", "bbox_2d": [745, 273, 839, 300], "page": 1},
 {"key": "대표전화", "value": "010-6144-1173", "bbox_2d": [743, 337, 905, 360], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [745, 390, 893, 412], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [740, 412, 894, 432], "page": 1},
 {"key": "발행지정계좌", "value": "016-074772-43224", "bbox_2d": [263, 487, 468, 508], "page": 1},
 {"key": "수취지정계좌", "value": "807-736814-85877", "bbox_2d": [271, 508, 463, 530], "page": 1},
 {"key": "value", "value": null},
 {"key": "변경항목", "value": null},
 {"key": "value2", "value": null},
 {"key": "취급점", "value": "센텀지점", "bbox_2d": [206, 149, 282, 171], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [375, 793, 558, 808], "page": 1},
 {"key": "signer3.name", "value": "남궁찬윤", "bbox_2d": [487, 819, 554, 840], "page": 1},
 {"key": "징구서류", "value": null},
 {"key": "자택", "value": null},
 {"key": "휴대폰", "value": "010-6144-1173", "bbox_2d": [501, 619, 679, 646], "page": 1}]
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
- check.거래구분: 거래구분 (체크박스, 보기: 신규가입 / 변경 / 발행해지 / 전체해지)
- check.회원구분: 회원구분 (체크박스, 보기: 발행인(수취,배서포함) / 수취/배서인 / 보증인)
- check.규모: 규모 (체크박스, 보기: 대기업 / 중소기업 / 개인사업자 / 개인)
- seal.signer: 거래인감 (같은 설명 중 1번째 칸, 도장)
- sign.signer: 거래인감 (같은 설명 중 2번째 칸, 서명)
- seal.signer2: 거래인감 (같은 설명 중 3번째 칸, 도장)
- sign.signer2: 거래인감 (같은 설명 중 4번째 칸, 서명)
- seal.signer3: 신청인(대리인) (같은 설명 중 1번째 칸, 도장)
- sign.signer3: 신청인(대리인) (같은 설명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 설명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 설명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 설명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.거래구분", "value": "발행해지", "bbox_2d": [614, 209, 627, 222], "page": 1},
 {"key": "check.회원구분", "value": "보증인", "bbox_2d": [704, 229, 717, 242], "page": 1},
 {"key": "check.규모", "value": "대기업", "bbox_2d": [447, 311, 460, 324], "page": 1},
 {"key": "seal.signer", "value": true, "bbox_2d": [791, 479, 847, 518], "page": 1},
 {"key": "sign.signer", "value": false},
 {"key": "seal.signer2", "value": true, "bbox_2d": [793, 501, 845, 538], "page": 1},
 {"key": "sign.signer2", "value": false},
 {"key": "seal.signer3", "value": false},
 {"key": "sign.signer3", "value": true, "bbox_2d": [629, 823, 681, 836], "page": 1},
 {"key": "seal.staff.담당", "value": true, "bbox_2d": [816, 43, 860, 73], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [876, 43, 919, 73], "page": 1},
 {"key": "sign.staff.책임자", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf374 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf374` → `python -m docgen.formdir card hf374` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf374 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf374 --show` · `python -m docgen.preview hf374 --out work/hf374`
