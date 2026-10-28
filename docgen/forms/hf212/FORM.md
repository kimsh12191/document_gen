# 해외직접투자 신고서(보고서) (`hf212`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf212 · card-hash: eb0c03151e7a -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 해외직접투자 신고서(보고서)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.212 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 25칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `corp.name` ← `company.name` | 상호 | text | 1쪽 [241, 211, 357, 229] | 늘 | 규칙: '상 호' → `company.name` | 고객 정보 (키 `company.name`) | fields.json:23 | 묻기 |
| `corp.ceo` ← `signer.name` | 대표자 | text | 1쪽 [317, 262, 387, 278] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:35 | 묻기 |
| `corp.biz_item` ← `company.biz_item` | 업종 | text | 1쪽 [246, 331, 316, 348] | 늘 | 규칙: '업 종' → `company.biz_item` | 고객 정보 (키 `company.biz_item`) | fields.json:53 | 묻기 |
| `투자국명` | 투자국명 | text | 1쪽 [242, 363, 311, 379] | 늘 | 항목명 그대로 | 값 종류 `country` (항목명 자동) | fields.json:65 | 묻기 |
| `투자방법` | 투자방법 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:77 | 묻기 |
| `투자업종` | 투자업종 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:89 | 묻기 |
| `투자금액` | 투자금액 | number | 1쪽 [422, 465, 502, 482] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:101 | 묻기 |
| `투자비율` | 투자비율 | number | 1쪽 [362, 499, 381, 515] | 늘 | 항목명 그대로 | 값 종류 `percent` (항목명 자동) | fields.json:113 | 묻기 |
| `투자목적` | 투자목적 | text | 1쪽 [245, 532, 297, 548] | 늘 | 항목명 그대로 | 값 종류 `reason` (항목명 자동) | fields.json:125 | 묻기 |
| `corp.biz_no` ← `company.biz_no` | 사업자등록번호 | biz_no | 1쪽 [668, 194, 778, 211] | 늘 | 규칙: '사 업 자 등 록 번 호' → `company.biz_no` | 고객 정보 (키 `company.biz_no`) | fields.json:137 | 묻기 |
| `corp.corp_reg_no` ← `company.corp_reg_no` | 법인등록번호 | corp_reg_no | 1쪽 [666, 230, 785, 246] | 늘 | 규칙: '법 인 등 록 번 호' → `company.corp_no` | 고객 정보 (키 `company.corp_no`) | fields.json:149 | 묻기 |
| `customer.rrn` | 주민등록번호 | rrn | 1쪽 [666, 263, 804, 281] | 늘 | 규칙: '주 민 등 록 번 호' → `customer.rrn` | 고객 정보 (키 `customer.rrn`) | fields.json:161 | 묻기 |
| `corp.address` ← `company.address` | 소재지 | text | 1쪽 [663, 364, 864, 379] | 늘 | 규칙: '소 재 지' → `company.address` | 고객 정보 (키 `company.address`) | fields.json:173 | 묻기 |
| `자금조달` | 자금조달 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:185 | 묻기 |
| `주요제품` | 주요제품 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:197 | 묻기 |
| `출자금액` | 출자금액 | number | 1쪽 [840, 466, 918, 482] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:209 | 묻기 |
| `결산월` | 결산월 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:221 | 묻기 |
| `투자유형` | 투자유형 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:233 | 묻기 |
| `신고번호` | 신고번호 | text | 1쪽 [668, 698, 823, 715] | 늘 | 항목명 그대로 | 값 종류 `number` (항목명 자동) | fields.json:245 | 묻기 |
| `신고금액` | 신고금액 | amount | 1쪽 [820, 723, 920, 740] | 늘 | 항목명 그대로 | 값 종류 `amount` (항목명 자동) | fields.json:256 | 묻기 |
| `유효기간` | 유효기간 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:267 | 묻기 |
| `해외직접투자신고서` | 해외직접투자신고서(보고서) | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:278 | 묻기 |
| `date` | 작성일 | date | 1쪽 [706, 633, 910, 651] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:289 | 묻기 |
| `company.ceo` | 대표자 | text | 1쪽 [251, 263, 321, 279] | 늘 | 규칙: '대 표 자' → `company.ceo` | 고객 정보 (키 `company.ceo`) | fields.json:314 | 묻기 |
| `위와같이신고되었음을확인함` | 위와같이신고(보고)되었음을확인함 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:326 | 묻기 |

## 체크·도장·서명 (marks) — 2칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.corp` ← `seal.signer` | 대표자 | seal | 1쪽 [462, 252, 498, 290] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:35 | 묻기 |
| `sign.customer` ← `sign.signer` | 대표자 | signature | 1쪽 [468, 264, 493, 279] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:35 | 묻기 |

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
"해외직접투자 신고서(보고서)"
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
 "화학제품",
 "싱가포르",
 "2,300,000",
 "50",
 "의료비",
 "702-81-38348",
 "200112-7951835",
 "850328-2******",
 "제주특별자치도 제주시 첨단로 381-19, 2층",
 "11,850,000",
 "496-449693-47348",
 "39,130,000원"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"39,130,000원"
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
- corp.name: 상호 (법인·사업자 상호)
- corp.ceo: 대표자 (법인·사업자 대표자, 같은 항목명 중 1번째 칸)
- corp.biz_item: 업종 (법인·사업자 업종)
- 투자국명: 투자국명
- 투자방법: 투자방법
- 투자업종: 투자업종
- 투자금액: 투자금액
- 투자비율: 투자비율
- 투자목적: 투자목적
- corp.biz_no: 사업자등록번호 (법인·사업자 사업자등록번호)
- corp.corp_reg_no: 법인등록번호 (법인·사업자 법인등록번호)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- corp.address: 소재지 (법인·사업자 주소)
- 자금조달: 자금조달
- 주요제품: 주요제품
- 출자금액: 출자금액
- 결산월: 결산월
- 투자유형: 투자유형
- 신고번호: 신고번호
- 신고금액: 신고금액
- 유효기간: 유효기간
- 해외직접투자신고서: 해외직접투자신고서(보고서)
- date: 작성일
- company.ceo: 대표자 (법인·사업자의 대표자, 같은 항목명 중 2번째 칸)
- 위와같이신고되었음을확인함: 위와같이신고(보고)되었음을확인함
```

답:

```json
[{"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [241, 211, 357, 229], "page": 1},
 {"key": "corp.ceo", "value": "남궁예태", "bbox_2d": [317, 262, 387, 278], "page": 1},
 {"key": "corp.biz_item", "value": "화학제품", "bbox_2d": [246, 331, 316, 348], "page": 1},
 {"key": "투자국명", "value": "싱가포르", "bbox_2d": [242, 363, 311, 379], "page": 1},
 {"key": "투자방법", "value": null},
 {"key": "투자업종", "value": null},
 {"key": "투자금액", "value": "2,300,000", "bbox_2d": [422, 465, 502, 482], "page": 1},
 {"key": "투자비율", "value": "50", "bbox_2d": [362, 499, 381, 515], "page": 1},
 {"key": "투자목적", "value": "의료비", "bbox_2d": [245, 532, 297, 548], "page": 1},
 {"key": "corp.biz_no", "value": "702-81-38348", "bbox_2d": [668, 194, 778, 211], "page": 1},
 {"key": "corp.corp_reg_no", "value": "200112-7951835", "bbox_2d": [666, 230, 785, 246], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [666, 263, 804, 281], "page": 1},
 {"key": "corp.address", "value": "제주특별자치도 제주시 첨단로 381-19, 2층", "bbox_2d": [663, 364, 864, 379], "page": 1},
 {"key": "자금조달", "value": null},
 {"key": "주요제품", "value": null},
 {"key": "출자금액", "value": "11,850,000", "bbox_2d": [840, 466, 918, 482], "page": 1},
 {"key": "결산월", "value": null},
 {"key": "투자유형", "value": null},
 {"key": "신고번호", "value": "496-449693-47348", "bbox_2d": [668, 698, 823, 715], "page": 1},
 {"key": "신고금액", "value": "39,130,000원", "bbox_2d": [820, 723, 920, 740], "page": 1},
 {"key": "유효기간", "value": null},
 {"key": "해외직접투자신고서", "value": null},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [706, 633, 910, 651], "page": 1},
 {"key": "company.ceo", "value": "남궁예태", "bbox_2d": [251, 263, 321, 279], "page": 1},
 {"key": "위와같이신고되었음을확인함", "value": null}]
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
- seal.corp: 대표자 (법인·사업자 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 대표자 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.corp", "value": true, "bbox_2d": [462, 252, 498, 290], "page": 1},
 {"key": "sign.customer", "value": false}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf212` → `python -m docgen.formdir card hf212` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf212 --show` · `python -m docgen.preview hf212 --out work/hf212`
