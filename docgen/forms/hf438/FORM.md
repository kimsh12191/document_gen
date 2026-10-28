# 매출채권보험 상담 신청서(신청기업용) (`hf438`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf438 · card-hash: 8fd61b043a41 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 매출채권보험 상담 신청서(신청기업용)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.438 (기타) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 28칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `corp.name` ← `company.name` | 기업체명 | text | 1쪽 [220, 192, 372, 218] | 늘 | 규칙: '기업체명' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:17 | 묻기 |
| `corp.corp_reg_no` ← `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 1쪽 [219, 232, 360, 253] | 늘 | 규칙: '법인등록번호' → `company.corp_no` | 고객 정보 (키 `company.corp_no`) | fields.json:28 | 묻기 |
| `corp.address` ← `company.address` | 사업장주소 | text | 1쪽 [217, 264, 616, 292] | 늘 | 규칙: '사업장주소' → `company.address` | 고객 정보 (키 `company.address`) | fields.json:39 | 묻기 |
| `당기매출액` | 당기매출액(최근1년매출액) | number | 1쪽 [273, 304, 383, 329] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:50 | 묻기 |
| `corp.ceo` ← `company.ceo` | 대표자 | text | 1쪽 [536, 192, 630, 217] | 늘 | 규칙: '대표자' → `company.ceo` | 고객 정보 (키 `company.ceo`) | fields.json:61 | 묻기 |
| `corp.biz_no` ← `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [534, 230, 687, 254] | 늘 | 규칙: '사업자등록번호' → `company.biz_no` | 고객 정보 (키 `company.biz_no`) | fields.json:72 | 묻기 |
| `업종업종분류코드` | 업종/업종분류코드 | number | 1쪽 [532, 302, 596, 328] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:83 | 묻기 |
| `corp.established` ← `company.established` | 설립일 | date | 1쪽 [830, 196, 906, 213] | 늘 | 규칙: '설립일' → `company.established` | 고객 정보 (키 `company.established`) | fields.json:94 | 묻기 |
| `customer.phone` | 전화번호 | phone | 1쪽 [824, 236, 913, 250] | 늘 | 규칙: '전화번호' → `customer.phone` | 고객 정보 (키 `customer.phone`) | fields.json:105 | 묻기 |
| `customer.email` | E-mail | text | 1쪽 [829, 275, 913, 284] | 늘 | 규칙: 'E-mail' → `customer.email` | 고객 정보 (키 `customer.email`) | fields.json:116 | 묻기 |
| `품목` | 품목 | text | 1쪽 [820, 305, 915, 329] | 늘 | 항목명 그대로 | 값 종류 `goods` (항목명 자동) | fields.json:127 | 묻기 |
| `년` | 년 | number | 1쪽 [298, 412, 324, 437] | 늘 | 표 행 (묶음·항목명 '년') | 값 종류 `count` (항목명 자동) | fields.json:138 | 묻기 |
| `년2` | 년 | text | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:153 | 묻기 |
| `년3` | 년 | text | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:166 | 묻기 |
| `월` | 월 | text | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:179 | 묻기 |
| `월2` | 월 | text | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:192 | 묻기 |
| `일` | 일 | text | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:205 | 묻기 |
| `일2` | 일 | text | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:218 | 묻기 |
| `신청기업담당자` | 신청기업담당자 | text | 1쪽 [220, 513, 314, 539] | 늘 | 항목명 그대로 | 값 종류 `person` (항목명 자동) | fields.json:231 | 묻기 |
| `employer.position` | 직위 | text | 1쪽 [503, 514, 549, 539] | 늘 | 규칙: '직위' → `employer.position` | 고객 정보 (키 `employer.position`) | fields.json:242 | 묻기 |
| `customer.phone2` | 연락처 | phone | 1쪽 [742, 515, 904, 540] | 늘 | 규칙: '연락처' → `customer.phone` | 고객 정보 (키 `customer.phone`) | fields.json:253 | 묻기 |
| `company.name2` | 기업체명 | text | 1쪽 [583, 728, 741, 757] | 늘 | 규칙: '기업체명' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:264 | 묻기 |
| `company.biz_no2` | 사업자등록번호 | biz_no | 1쪽 [585, 756, 752, 783] | 늘 | 규칙: '사업자등록번호' → `company.biz_no` | 고객 정보 (키 `company.biz_no`) | fields.json:275 | 묻기 |
| `company.corp_no2` | 법인등록번호 | rrn | 1쪽 [580, 784, 756, 809] | 늘 | 규칙: '법인등록번호' → `company.corp_no` | 고객 정보 (키 `company.corp_no`) | fields.json:286 | 묻기 |
| `signer.name` | 대표자명 | text | 1쪽 [684, 811, 778, 836] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:297 | 묻기 |
| `signer2.name` | 본인확인 | text | 1쪽 [761, 855, 817, 881] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:314 | 묻기 |
| `date` | 작성일 | date | 1쪽 [360, 652, 560, 670] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:331 | 묻기 |
| `신용보험센터` | 신용보험센터 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:356 | 묻기 |

## 체크·도장·서명 (marks) — 4칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.corp` ← `seal.signer` | 대표자명 | seal | 1쪽 [891, 815, 916, 829] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:297 | 묻기 |
| `sign.customer` ← `sign.signer` | 대표자명 | signature | 1쪽 [891, 815, 916, 829] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:297 | 묻기 |
| `seal.signer2` | 본인확인 | seal | 1쪽 [891, 860, 916, 875] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:314 | 묻기 |
| `sign.signer2` | 본인확인 | signature | 1쪽 [891, 860, 916, 875] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:314 | 묻기 |

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
"매출채권보험 상담 신청서(신청기업용)"
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
 "200112-7951835",
 "제주특별자치도 제주시 첨단로 381-19, 2층",
 "6,790,000",
 "남궁예태",
 "702-81-38348",
 "72912",
 "2020.06.15",
 "010-6144-1173",
 "yetae741@gmail.com",
 "PCB 기판",
 "60",
 "대리",
 "천기유"
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
"천기유"
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
- corp.name: 기업체명 (법인·사업자 상호, 같은 항목명 중 1번째 칸)
- corp.corp_reg_no: 법인등록번호 (법인·사업자 법인등록번호, 같은 항목명 중 1번째 칸)
- corp.address: 사업장주소 (법인·사업자 주소)
- 당기매출액: 당기매출액(최근1년매출액)
- corp.ceo: 대표자 (법인·사업자 대표자)
- corp.biz_no: 사업자등록번호 (법인·사업자 사업자등록번호, 같은 항목명 중 1번째 칸)
- 업종업종분류코드: 업종/업종분류코드
- corp.established: 설립일 (법인·사업자 설립일)
- customer.phone: 전화번호 (고객 연락처)
- customer.email: E-mail (고객 이메일)
- 품목: 품목
- 년: 년 (같은 항목명 중 1번째 칸)
- 년2: 년 (같은 항목명 중 2번째 칸)
- 년3: 년 (같은 항목명 중 3번째 칸)
- 월: 월 (같은 항목명 중 1번째 칸)
- 월2: 월 (같은 항목명 중 2번째 칸)
- 일: 일 (같은 항목명 중 1번째 칸)
- 일2: 일 (같은 항목명 중 2번째 칸)
- 신청기업담당자: 신청기업담당자
- employer.position: 직위 (직장 직위)
- customer.phone2: 연락처
- company.name2: 기업체명 (같은 항목명 중 2번째 칸)
- company.biz_no2: 사업자등록번호 (같은 항목명 중 2번째 칸)
- company.corp_no2: 법인등록번호 (같은 항목명 중 2번째 칸)
- signer.name: 대표자명 (법인·사업자의 대표자)
- signer2.name: 본인확인 (은행·직원의 성명)
- date: 작성일
- 신용보험센터: 신용보험센터
```

답:

```json
[{"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [220, 192, 372, 218], "page": 1},
 {"key": "corp.corp_reg_no", "value": "200112-7951835", "bbox_2d": [219, 232, 360, 253], "page": 1},
 {"key": "corp.address", "value": "제주특별자치도 제주시 첨단로 381-19, 2층", "bbox_2d": [217, 264, 616, 292], "page": 1},
 {"key": "당기매출액", "value": "6,790,000", "bbox_2d": [273, 304, 383, 329], "page": 1},
 {"key": "corp.ceo", "value": "남궁예태", "bbox_2d": [536, 192, 630, 217], "page": 1},
 {"key": "corp.biz_no", "value": "702-81-38348", "bbox_2d": [534, 230, 687, 254], "page": 1},
 {"key": "업종업종분류코드", "value": "72912", "bbox_2d": [532, 302, 596, 328], "page": 1},
 {"key": "corp.established", "value": "2020.06.15", "bbox_2d": [830, 196, 906, 213], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [824, 236, 913, 250], "page": 1},
 {"key": "customer.email", "value": "yetae741@gmail.com", "bbox_2d": [829, 275, 913, 284], "page": 1},
 {"key": "품목", "value": "PCB 기판", "bbox_2d": [820, 305, 915, 329], "page": 1},
 {"key": "년", "value": "60", "bbox_2d": [298, 412, 324, 437], "page": 1},
 {"key": "년2", "value": null},
 {"key": "년3", "value": null},
 {"key": "월", "value": null},
 {"key": "월2", "value": null},
 {"key": "일", "value": null},
 {"key": "일2", "value": null},
 {"key": "신청기업담당자", "value": "남궁예태", "bbox_2d": [220, 513, 314, 539], "page": 1},
 {"key": "employer.position", "value": "대리", "bbox_2d": [503, 514, 549, 539], "page": 1},
 {"key": "customer.phone2", "value": "010-6144-1173", "bbox_2d": [742, 515, 904, 540], "page": 1},
 {"key": "company.name2", "value": "(주)미래케미칼", "bbox_2d": [583, 728, 741, 757], "page": 1},
 {"key": "company.biz_no2", "value": "702-81-38348", "bbox_2d": [585, 756, 752, 783], "page": 1},
 {"key": "company.corp_no2", "value": "200112-7951835", "bbox_2d": [580, 784, 756, 809], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [684, 811, 778, 836], "page": 1},
 {"key": "signer2.name", "value": "천기유", "bbox_2d": [761, 855, 817, 881], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [360, 652, 560, 670], "page": 1},
 {"key": "신용보험센터", "value": null}]
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
- seal.corp: 대표자명 (법인·사업자 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 대표자명 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.signer2: 본인확인 (은행·직원의 신청인, 같은 항목명 중 1번째 칸, 도장)
- sign.signer2: 본인확인 (은행·직원의 신청인, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.corp", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [891, 815, 916, 829], "page": 1},
 {"key": "seal.signer2", "value": false},
 {"key": "sign.signer2", "value": true, "bbox_2d": [891, 860, 916, 875], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf438` → `python -m docgen.formdir card hf438` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf438 --show` · `python -m docgen.preview hf438 --out work/hf438`
