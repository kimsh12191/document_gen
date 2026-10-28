# 전자방식 외상매출채권 결제제도 이용신청서 (서울시농수산식품공사용) (`hf083`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf083 · card-hash: fc8135dc2007 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 전자방식 외상매출채권 결제제도 이용신청서 (서울시농수산식품공사용)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf083 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.83 (대출) 원본 위에 기재

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
| `corp.name` ← `company.name` | 법인명(또는상호명) | text | 1쪽 [248, 210, 349, 221] | 늘 | 규칙: '법인명 (또는 상호명)' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:52 | 묻기 |
| `corp.ceo` ← `company.ceo` | 대표이사(또는대표자명) | text | 1쪽 [248, 254, 309, 265] | 늘 | 규칙: '대표이사 (또는 대표자명)' → `company.ceo` | 고객 정보 (키 `company.ceo`) | fields.json:63 | 묻기 |
| `company.biz_type` | 업태 | text | 1쪽 [249, 288, 295, 299] | 늘 | 규칙: '업 태' → `company.biz_type` | 고객 정보 (키 `company.biz_type`) | fields.json:74 | 묻기 |
| `주요취급품목` | 주요취급품목 | text | 1쪽 [247, 315, 293, 326] | 늘 | 항목명 그대로 | 값 종류 `goods` (항목명 자동) | fields.json:85 | 묻기 |
| `value` | (우편번호:) | amount | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:96 | 묻기 |
| `customer.phone` | 전화번호 | phone | 1쪽 [251, 379, 353, 390] | 늘 | 규칙: '전화번호' → `customer.phone` | 고객 정보 (키 `customer.phone`) | fields.json:107 | 묻기 |
| `corp.biz_no` ← `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [688, 199, 783, 209] | 늘 | 규칙: '사업자등록번호' → `company.biz_no` | 고객 정보 (키 `company.biz_no`) | fields.json:211 | 묻기 |
| `corp.corp_reg_no` ← `company.corp_reg_no` | 법인등록번호(법인인경우) | corp_reg_no | 1쪽 [688, 222, 802, 233] | 늘 | 규칙: '법인등록번호(법인인경우)' → `company.corp_no` | 고객 정보 (키 `company.corp_no`) | fields.json:223 | 묻기 |
| `대표이사생년월일` | 대표이사(대표자)생년월일 | date | 1쪽 [686, 254, 808, 265] | 늘 | 항목명 그대로 | 값 종류 `date` (항목명 자동) | fields.json:235 | 묻기 |
| `corp.biz_item` ← `company.biz_item` | 업종 | text | 1쪽 [686, 288, 747, 299] | 늘 | 규칙: '업 종' → `company.biz_item` | 고객 정보 (키 `company.biz_item`) | fields.json:246 | 묻기 |
| `팩스번호` | 팩스번호 | phone | 1쪽 [685, 379, 778, 390] | 늘 | 항목명 그대로 | 값 종류 `phone` (항목명 자동) | fields.json:257 | 묻기 |
| `목록.*.비고` | 비고 | text | 1쪽 [838, 487, 903, 498] (1행) | 늘 | 표 행 (묶음·항목명 '비고') | 값 종류 `note` (항목명 자동) | fields.json:326 | 묻기 |
| `담당부서` | 담당부서 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:350 | 묻기 |
| `담당자팩스번호` | 담당자팩스번호 | phone | 1쪽 [669, 684, 763, 695] | 늘 | 항목명 그대로 | 값 종류 `phone` (항목명 자동) | fields.json:422 | 묻기 |
| `date` | 작성일 | date | 1쪽 [420, 895, 600, 912] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:433 | 묻기 |
| `customer.name` ← `signer.name` | 신청인 | text | 1쪽 [484, 923, 545, 934] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:459 | 묻기 |

## 체크·도장·서명 (marks) — 12칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.기업규모` | 기업규모 | checkbox (대기업 / 중견기업 / 중기업 / 소기업 / 공공 및 기타) | 1쪽 [755, 403, 862, 418] | 늘 | 체크 (항목명) | 보기 중 고름: 대기업 / 중견기업 / 중기업 / 소기업 / 공공 및 기타 | fields.json:118 | 묻기 |
| `check.외상매출채권의` | 외상매출채권의 | checkbox (외상매출채권의) | 1쪽 [107, 476, 235, 490] | 늘 | 체크 (항목명) | 보기 중 고름: 외상매출채권의 | fields.json:268 | 묻기 |
| `check.판매기업` | 판매기업 | checkbox (판매기업) | 1쪽 [130, 533, 212, 547] | 늘 | 체크 (항목명) | 보기 중 고름: 판매기업 | fields.json:297 | 묻기 |
| `check.SKT` | SKT | checkbox (SKT / KT / LGU+) | 1쪽 [703, 657, 758, 676] | 늘 | 체크 (항목명) | 보기 중 고름: SKT / KT / LGU+ | fields.json:361 | 묻기 |
| `seal.customer` ← `seal.signer` | 신청인 | seal | 1쪽 [641, 911, 672, 947] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:459 | 묻기 |
| `sign.customer` ← `sign.signer` | 신청인 | signature | 1쪽 [643, 922, 670, 936] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:459 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [643, 128, 714, 172] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [643, 128, 714, 172] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [714, 128, 785, 172] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [714, 128, 785, 172] | 늘 | - | - | - | 묻기 |
| `seal.staff.관리자` | 관리자 | seal | 1쪽 [785, 128, 848, 172] | 늘 | - | - | - | 묻기 |
| `sign.staff.관리자` | 관리자 | signature | 1쪽 [785, 128, 848, 172] | 늘 | - | - | - | 묻기 |

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
"전자방식 외상매출채권 결제제도 이용신청서 (서울시농수산식품공사용)"
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
 "남궁예태",
 "제조업",
 "포장재",
 "010-6144-1173",
 "702-81-38348",
 "200112-7951835",
 "2024년 12월 31일",
 "화학제품",
 "051-509-1176",
 "해당 없음"
]
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
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- corp.name: 법인명(또는상호명) (법인·사업자 상호)
- corp.ceo: 대표이사(또는대표자명) (법인·사업자 대표자)
- company.biz_type: 업태
- 주요취급품목: 주요취급품목
- value: (우편번호:)
- customer.phone: 전화번호 (고객 연락처)
- corp.biz_no: 사업자등록번호 (법인·사업자 사업자등록번호)
- corp.corp_reg_no: 법인등록번호(법인인경우) (법인·사업자 법인등록번호)
- 대표이사생년월일: 대표이사(대표자)생년월일
- corp.biz_item: 업종 (법인·사업자 업종)
- 팩스번호: 팩스번호
- 목록.0.비고: 비고 (목록 1행)
- 목록.1.비고: 비고 (목록 2행)
- 담당부서: 담당부서
- 담당자팩스번호: 담당자팩스번호
- date: 작성일
- customer.name: 신청인 (고객 성명)
```

답:

```json
[{"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [248, 210, 349, 221], "page": 1},
 {"key": "corp.ceo", "value": "남궁예태", "bbox_2d": [248, 254, 309, 265], "page": 1},
 {"key": "company.biz_type", "value": "제조업", "bbox_2d": [249, 288, 295, 299], "page": 1},
 {"key": "주요취급품목", "value": "포장재", "bbox_2d": [247, 315, 293, 326], "page": 1},
 {"key": "value", "value": null},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [251, 379, 353, 390], "page": 1},
 {"key": "corp.biz_no", "value": "702-81-38348", "bbox_2d": [688, 199, 783, 209], "page": 1},
 {"key": "corp.corp_reg_no", "value": "200112-7951835", "bbox_2d": [688, 222, 802, 233], "page": 1},
 {"key": "대표이사생년월일", "value": "2024년 12월 31일", "bbox_2d": [686, 254, 808, 265], "page": 1},
 {"key": "corp.biz_item", "value": "화학제품", "bbox_2d": [686, 288, 747, 299], "page": 1},
 {"key": "팩스번호", "value": "051-509-1176", "bbox_2d": [685, 379, 778, 390], "page": 1},
 {"key": "목록.0.비고", "value": "해당 없음", "bbox_2d": [838, 487, 903, 498], "page": 1},
 {"key": "목록.1.비고", "value": null},
 {"key": "담당부서", "value": null},
 {"key": "담당자팩스번호", "value": "051-509-1176", "bbox_2d": [669, 684, 763, 695], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [420, 895, 600, 912], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [484, 923, 545, 934], "page": 1}]
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
- check.기업규모: 기업규모 (체크박스, 보기: 대기업 / 중견기업 / 중기업 / 소기업 / 공공 및 기타)
- check.외상매출채권의: 외상매출채권의 (체크박스, 보기: 외상매출채권의)
- check.판매기업: 판매기업 (체크박스, 보기: 판매기업)
- check.SKT: SKT (체크박스, 보기: SKT / KT / LGU+)
- seal.customer: 신청인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 신청인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.관리자: 관리자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.관리자: 관리자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.기업규모", "value": "공공 및 기타", "bbox_2d": [755, 405, 772, 417], "page": 1},
 {"key": "check.외상매출채권의", "value": null},
 {"key": "check.판매기업", "value": null},
 {"key": "check.SKT", "value": "SKT", "bbox_2d": [703, 659, 721, 676], "page": 1},
 {"key": "seal.customer", "value": true, "bbox_2d": [641, 911, 672, 947], "page": 1},
 {"key": "sign.customer", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": true, "bbox_2d": [643, 128, 714, 172], "page": 1},
 {"key": "seal.staff.책임자", "value": false},
 {"key": "sign.staff.책임자", "value": true, "bbox_2d": [714, 128, 785, 172], "page": 1},
 {"key": "seal.staff.관리자", "value": false},
 {"key": "sign.staff.관리자", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf083 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf083` → `python -m docgen.formdir card hf083` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf083 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf083 --show` · `python -m docgen.preview hf083 --out work/hf083`
