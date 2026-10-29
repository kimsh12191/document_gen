# 외국인투자기업등록(변경등록)신청서(국문) (`hf235`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf235 · card-hash: a5301bd2d806 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 3 (seed 1000000 로 그린 것) · **분류 정답:** 외국인투자기업등록(변경등록)신청서(국문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf235 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.235 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 30칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `접수일` | 접수일 | text | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:55 | 묻기 |
| `처리일` | 처리일 | text | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:66 | 묻기 |
| `처리기간1일` | 처리기간1일 | date | 1쪽 [793, 102, 855, 111] | 늘 | 항목명 그대로 | 값 종류 `date` (항목명 자동) | fields.json:77 | 묻기 |
| `상호또는명칭` | 상호또는명칭(영문) | text | 1쪽 [347, 128, 438, 139] | 늘 | 항목명 그대로 | 값 종류 `company` (항목명 자동) | fields.json:88 | 묻기 |
| `신고된사업명` | 신고(허가)된사업명 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:99 | 묻기 |
| `자본금` | 자본금(출연금) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:110 | 묻기 |
| `value` | (국문) | amount | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:121 | 묻기 |
| `value2` | (영문) | amount | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:132 | 묻기 |
| `SPC여부예아니오` | (*)SPC여부[]예[]아니오 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:143 | 묻기 |
| `본사` | 본사 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:154 | 묻기 |
| `주공장소재지` | 주공장(주사업장)소재지 | text | 1쪽 [473, 300, 815, 311] | 늘 | 항목명 그대로 | 값 종류 `address` (항목명 자동) | fields.json:166 | 묻기 |
| `홈페이지` | 홈페이지 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:178 | 묻기 |
| `액면총액` | 액면총액 | number | 1쪽 [672, 451, 753, 463] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:189 | 묻기 |
| `상호또는명칭2` | 상호또는명칭(영문) | text | 1쪽 [570, 628, 635, 639] | 늘 | 항목명 그대로 | 값 종류 `company` (항목명 자동) | fields.json:200 | 묻기 |
| `상호또는명칭3` | 상호또는명칭(영문) | text | 1쪽 [569, 668, 634, 680] | 늘 | 항목명 그대로 | 값 종류 `company` (항목명 자동) | fields.json:211 | 묻기 |
| `대표Email` | 대표E-mail | text | 1쪽 [692, 330, 849, 341] | 늘 | 항목명 그대로 | 값 종류 `email` (항목명 자동) | fields.json:222 | 묻기 |
| `customer.nationality` | 국적 | text | 1쪽 [779, 128, 844, 139] | 늘 | 규칙: '국적' → `customer.nationality` | 고객 정보 (키 `customer.nationality`) | fields.json:233 | 묻기 |
| `customer.nationality2` | 국적 | text | 1쪽 [765, 628, 830, 639] | 늘 | 규칙: '국적' → `customer.nationality` | 고객 정보 (키 `customer.nationality`) | fields.json:244 | 묻기 |
| `customer.nationality3` | 국적 | text | 1쪽 [764, 668, 829, 680] | 늘 | 규칙: '국적' → `customer.nationality` | 고객 정보 (키 `customer.nationality`) | fields.json:255 | 묻기 |
| `액면총액2` | 액면총액 | number | 1쪽 [824, 436, 842, 448] | 늘 | 항목명 그대로 | 값 종류 `percent` (항목명 자동) | fields.json:266 | 묻기 |
| `date` | 작성일 | date | 1쪽 [704, 846, 929, 861] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:279 | 묻기 |
| `customer.name` ← `signer.name` | 신고인또는신청인 | text | 1쪽 [700, 875, 764, 886] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:304 | 묻기 |
| `접수번호` | 접수번호 | text | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:321 | 묻기 |
| `투자기업` | 투자기업 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:333 | 묻기 |
| `상당` | 상당 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:345 | 묻기 |
| `등록후예상규모` | 등록후예상규모(신규및변경등록) | number | 1쪽 [852, 482, 861, 493] | 늘 | 항목명 그대로 | 값 종류 `count` (항목명 자동) | fields.json:357 | 묻기 |
| `투자기업2` | 투자기업 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:370 | 묻기 |
| `양도또는감소할` | 양도또는감소할 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:382 | 묻기 |
| `액면총액3` | 액면총액(A×B) | number | 1쪽 [641, 741, 705, 750] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:394 | 묻기 |
| `신규등록인경우` | <신규등록인경우> | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:445 | 묻기 |

## 체크·도장·서명 (marks) — 7칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.customer` ← `seal.signer` | 신고인또는신청인 | seal | 1쪽 [840, 874, 929, 888] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:304 | 묻기 |
| `sign.customer` ← `sign.signer` | 신고인또는신청인 | signature | 1쪽 [840, 874, 929, 888] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:304 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [790, 33, 846, 73] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [786, 31, 850, 75] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [850, 31, 919, 75] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [850, 31, 919, 75] | 늘 | - | - | - | 묻기 |
| `check.송달받는것에대하여` | 송달받는것에대하여 | checkbox (동의합니다. / 동의하지 않습니다.) | 2쪽 [222, 195, 336, 213] | 늘 | 체크 (항목명) | 보기 중 고름: 동의합니다. / 동의하지 않습니다. | fields.json:406 | 묻기 |

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
"외국인투자기업등록(변경등록)신청서(국문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2024-05-16",
 "(주)우진무역",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "40,900,000",
 "한빛물산",
 "다온전자",
 "yetae741@gmail.com",
 "대한민국",
 "60",
 "남궁예태",
 "2",
 "22,370,000"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"(주)우진무역"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"대한민국"
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
- 접수일: 접수일
- 처리일: 처리일
- 처리기간1일: 처리기간1일
- 상호또는명칭: 상호또는명칭(영문) (같은 항목명 중 1번째 칸)
- 신고된사업명: 신고(허가)된사업명
- 자본금: 자본금(출연금)
- value: (국문)
- value2: (영문)
- SPC여부예아니오: (*)SPC여부[]예[]아니오
- 본사: 본사
- 주공장소재지: 주공장(주사업장)소재지
- 홈페이지: 홈페이지
- 액면총액: 액면총액 (같은 항목명 중 1번째 칸)
- 상호또는명칭2: 상호또는명칭(영문) (같은 항목명 중 2번째 칸)
- 상호또는명칭3: 상호또는명칭(영문) (같은 항목명 중 3번째 칸)
- 대표Email: 대표E-mail
- customer.nationality: 국적 (고객 국적, 같은 항목명 중 1번째 칸)
- customer.nationality2: 국적 (같은 항목명 중 2번째 칸)
- customer.nationality3: 국적 (같은 항목명 중 3번째 칸)
- 액면총액2: 액면총액 (같은 항목명 중 2번째 칸)
- date: 작성일
- customer.name: 신고인또는신청인 (고객 성명)
- 접수번호: 접수번호
- 투자기업: 투자기업 (같은 항목명 중 1번째 칸)
- 상당: 상당
- 등록후예상규모: 등록후예상규모(신규및변경등록)
- 투자기업2: 투자기업 (같은 항목명 중 2번째 칸)
- 양도또는감소할: 양도또는감소할
- 액면총액3: 액면총액(A×B)
- 신규등록인경우: <신규등록인경우>
```

답:

```json
[{"key": "접수일", "value": null},
 {"key": "처리일", "value": null},
 {"key": "처리기간1일", "value": "2024-05-16", "bbox_2d": [793, 102, 855, 111], "page": 1},
 {"key": "상호또는명칭", "value": "(주)우진무역", "bbox_2d": [347, 128, 438, 139], "page": 1},
 {"key": "신고된사업명", "value": null},
 {"key": "자본금", "value": null},
 {"key": "value", "value": null},
 {"key": "value2", "value": null},
 {"key": "SPC여부예아니오", "value": null},
 {"key": "본사", "value": null},
 {"key": "주공장소재지", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [473, 300, 815, 311], "page": 1},
 {"key": "홈페이지", "value": null},
 {"key": "액면총액", "value": "40,900,000", "bbox_2d": [672, 451, 753, 463], "page": 1},
 {"key": "상호또는명칭2", "value": "한빛물산", "bbox_2d": [570, 628, 635, 639], "page": 1},
 {"key": "상호또는명칭3", "value": "다온전자", "bbox_2d": [569, 668, 634, 680], "page": 1},
 {"key": "대표Email", "value": "yetae741@gmail.com", "bbox_2d": [692, 330, 849, 341], "page": 1},
 {"key": "customer.nationality", "value": "대한민국", "bbox_2d": [779, 128, 844, 139], "page": 1},
 {"key": "customer.nationality2", "value": "대한민국", "bbox_2d": [765, 628, 830, 639], "page": 1},
 {"key": "customer.nationality3", "value": "대한민국", "bbox_2d": [764, 668, 829, 680], "page": 1},
 {"key": "액면총액2", "value": "60", "bbox_2d": [824, 436, 842, 448], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [704, 846, 929, 861], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [700, 875, 764, 886], "page": 1},
 {"key": "접수번호", "value": null},
 {"key": "투자기업", "value": null},
 {"key": "상당", "value": null},
 {"key": "등록후예상규모", "value": "2", "bbox_2d": [852, 482, 861, 493], "page": 1},
 {"key": "투자기업2", "value": null},
 {"key": "양도또는감소할", "value": null},
 {"key": "액면총액3", "value": "22,370,000", "bbox_2d": [641, 741, 705, 750], "page": 1},
 {"key": "신규등록인경우", "value": null}]
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
- seal.customer: 신고인또는신청인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 신고인또는신청인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
- check.송달받는것에대하여: 송달받는것에대하여 (체크박스, 보기: 동의합니다. / 동의하지 않습니다.)
```

답:

```json
[{"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [840, 874, 929, 888], "page": 1},
 {"key": "seal.staff.담당", "value": true, "bbox_2d": [790, 33, 846, 73], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": false},
 {"key": "sign.staff.책임자", "value": true, "bbox_2d": [850, 31, 919, 75], "page": 1},
 {"key": "check.송달받는것에대하여", "value": "동의합니다.", "bbox_2d": [222, 198, 241, 213], "page": 2}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf235 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf235` → `python -m docgen.formdir card hf235` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf235 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf235 --show` · `python -m docgen.preview hf235 --out work/hf235`
