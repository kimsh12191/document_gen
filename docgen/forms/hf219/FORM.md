# 해외사무소 설치(변경)신고서 (`hf219`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf219 · card-hash: e26dbb322527 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 해외사무소 설치(변경)신고서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.219 (외환) 원본 위에 기재

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
| `corp.name` ← `signer.name` | 상호 | text | 1쪽 [299, 182, 457, 208] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:23 | 묻기 |
| `corp.biz_no` ← `company.biz_no` | 사업자(주민)번호 | biz_no | 1쪽 [278, 209, 446, 238] | 늘 | 규칙: '사업자(주민)번호' → `company.biz_no` | 고객 정보 (키 `company.biz_no`) | fields.json:41 | 묻기 |
| `corp.biz_item` ← `company.biz_item` | 업종 | text | 1쪽 [277, 286, 370, 313] | 늘 | 규칙: '업 종' → `company.biz_item` | 고객 정보 (키 `company.biz_item`) | fields.json:53 | 묻기 |
| `value` | (표준산업분류코드5자리) | amount | - | 늘 | 항목명 그대로 | 값 종류 `skip` (항목명 자동) | fields.json:171 | 묻기 |
| `설치사유` | 설치사유 | text | 1쪽 [279, 541, 363, 568] | 늘 | 항목명 그대로 | 값 종류 `reason` (항목명 자동) | fields.json:182 | 묻기 |
| `내용` | 내용 | text | 1쪽 [276, 571, 379, 597] | 늘 | 항목명 그대로 | 값 종류 `note` (항목명 자동) | fields.json:194 | 묻기 |
| `사유` | 사유 | text | 1쪽 [279, 600, 363, 625] | 늘 | 항목명 그대로 | 값 종류 `reason` (항목명 자동) | fields.json:206 | 묻기 |
| `corp.ceo` ← `company.ceo` | 대표자 | text | 1쪽 [682, 182, 777, 207] | 늘 | 규칙: '대 표 자' → `company.ceo` | 고객 정보 (키 `company.ceo`) | fields.json:218 | 묻기 |
| `corp.corp_reg_no` ← `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 1쪽 [683, 212, 860, 237] | 늘 | 규칙: '법인등록번호' → `company.corp_no` | 고객 정보 (키 `company.corp_no`) | fields.json:230 | 묻기 |
| `신고번호` | 신고번호 | text | 1쪽 [684, 711, 905, 737] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:242 | 묻기 |
| `유효기간` | 유효기간 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:253 | 묻기 |
| `처리기간` | 처리기간 | text | - | 늘 | 표 행 (묶음·항목명 '처 리 기 간') | 값 종류 `skip` (항목명 자동) | fields.json:264 | 묻기 |
| `date` | 작성일 | date | 1쪽 [707, 659, 901, 676] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:278 | 묻기 |
| `date2` | 작성일 | date | 1쪽 [707, 794, 901, 811] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:303 | 묻기 |
| `signer2.name` | 신고(보고)기관 | text | 1쪽 [739, 819, 823, 841] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:328 | 묻기 |
| `company.name` | 상호 | text | 1쪽 [283, 182, 441, 208] | 늘 | 규칙: '상 호' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:345 | 묻기 |
| `위의신청을다음과같이신고필함` | 위의신청을다음과같이신고필함. | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:357 | 묻기 |

## 체크·도장·서명 (marks) — 6칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.corp` ← `seal.signer` | 상호 | seal | 1쪽 [478, 175, 527, 214] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:23 | 묻기 |
| `sign.customer` ← `sign.signer` | 상호 | signature | 1쪽 [489, 187, 515, 201] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:23 | 묻기 |
| `check.기업규모` | 기업규모 | checkbox (대기업 / 중소기업 / 개인사업자) | 1쪽 [291, 320, 561, 335] | 늘 | 체크 (항목명) | 보기 중 고름: 대기업 / 중소기업 / 개인사업자 | fields.json:65 | 묻기 |
| `check.구분` | 구분 | checkbox (설치 / 변경) | 1쪽 [291, 358, 420, 373] | 늘 | 체크 (항목명) | 보기 중 고름: 설치 / 변경 | fields.json:126 | 묻기 |
| `seal.signer2` | 신고(보고)기관 | seal | 1쪽 [883, 823, 909, 837] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:328 | 묻기 |
| `sign.signer2` | 신고(보고)기관 | signature | 1쪽 [883, 823, 909, 837] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:328 | 묻기 |

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
"해외사무소 설치(변경)신고서"
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
 "화학제품",
 "결혼자금",
 "해당 없음",
 "주택구입",
 "남궁예태",
 "200112-7951835",
 "043-383331-46710"
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
"남궁예태"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- corp.name: 상호 (법인·사업자 상호, 같은 항목명 중 1번째 칸)
- corp.biz_no: 사업자(주민)번호 (법인·사업자 사업자등록번호)
- corp.biz_item: 업종 (법인·사업자 업종)
- value: (표준산업분류코드5자리)
- 설치사유: 설치사유
- 내용: 내용
- 사유: 사유
- corp.ceo: 대표자 (법인·사업자 대표자)
- corp.corp_reg_no: 법인등록번호 (법인·사업자 법인등록번호)
- 신고번호: 신고번호
- 유효기간: 유효기간
- 처리기간: 처리기간
- date: 작성일 (같은 항목명 중 1번째 칸)
- date2: 작성일 (같은 항목명 중 2번째 칸)
- signer2.name: 신고(보고)기관
- company.name: 상호 (법인·사업자의 성명, 같은 항목명 중 2번째 칸)
- 위의신청을다음과같이신고필함: 위의신청을다음과같이신고필함.
```

답:

```json
[{"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [299, 182, 457, 208], "page": 1},
 {"key": "corp.biz_no", "value": "702-81-38348", "bbox_2d": [278, 209, 446, 238], "page": 1},
 {"key": "corp.biz_item", "value": "화학제품", "bbox_2d": [277, 286, 370, 313], "page": 1},
 {"key": "value", "value": null},
 {"key": "설치사유", "value": "결혼자금", "bbox_2d": [279, 541, 363, 568], "page": 1},
 {"key": "내용", "value": "해당 없음", "bbox_2d": [276, 571, 379, 597], "page": 1},
 {"key": "사유", "value": "주택구입", "bbox_2d": [279, 600, 363, 625], "page": 1},
 {"key": "corp.ceo", "value": "남궁예태", "bbox_2d": [682, 182, 777, 207], "page": 1},
 {"key": "corp.corp_reg_no", "value": "200112-7951835", "bbox_2d": [683, 212, 860, 237], "page": 1},
 {"key": "신고번호", "value": "043-383331-46710", "bbox_2d": [684, 711, 905, 737], "page": 1},
 {"key": "유효기간", "value": null},
 {"key": "처리기간", "value": null},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [707, 659, 901, 676], "page": 1},
 {"key": "date2", "value": "2025년 4월 1일", "bbox_2d": [707, 794, 901, 811], "page": 1},
 {"key": "signer2.name", "value": "남궁예태", "bbox_2d": [739, 819, 823, 841], "page": 1},
 {"key": "company.name", "value": "(주)미래케미칼", "bbox_2d": [283, 182, 441, 208], "page": 1},
 {"key": "위의신청을다음과같이신고필함", "value": null}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.corp: 상호 (법인·사업자 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 상호 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- check.기업규모: 기업규모 (체크박스, 보기: 대기업 / 중소기업 / 개인사업자)
- check.구분: 구분 (체크박스, 보기: 설치 / 변경)
- seal.signer2: 신고(보고)기관 (같은 항목명 중 1번째 칸, 도장)
- sign.signer2: 신고(보고)기관 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.corp", "value": true, "bbox_2d": [478, 175, 527, 214], "page": 1},
 {"key": "sign.customer", "value": false},
 {"key": "check.기업규모", "value": null},
 {"key": "check.구분", "value": null},
 {"key": "seal.signer2", "value": false},
 {"key": "sign.signer2", "value": true, "bbox_2d": [883, 823, 909, 837], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf219` → `python -m docgen.formdir card hf219` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf219 --show` · `python -m docgen.preview hf219 --out work/hf219`
