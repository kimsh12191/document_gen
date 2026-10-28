# 신용장 확인 신청 및 확약서 (`hf286`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf286 · card-hash: 71a6649c13c6 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 신용장 확인 신청 및 확약서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.286 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 2칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `취급점` | 취급점 | text | 1쪽 [198, 200, 288, 226] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:26 | 묻기 |
| `customer.name` ← `signer.name` | (본인) | text | 1쪽 [713, 784, 802, 807] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

## 체크·도장·서명 (marks) — 12칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `check.CREDITNO` | CREDITNO.(신용장번호) | checkbox (CREDIT NO. (신용장번호)) | 1쪽 [112, 271, 343, 287] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.ADVICENO` | ADVICENO.(신용장통지번호) | checkbox (ADVICE NO.(신용장통지번호)) | 1쪽 [112, 338, 373, 354] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.ISSUINGBANK` | ISSUINGBANK(개설은행) | checkbox (ISSUING BANK(개설은행)) | 1쪽 [112, 405, 341, 420] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.ISSUINGDATE` | ISSUINGDATE(개설일) | checkbox (ISSUING DATE(개설일)) | 1쪽 [112, 471, 322, 487] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.AMOUNT` | AMOUNT(금액) | checkbox (AMOUNT(금액)) | 1쪽 [112, 538, 268, 554] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.customer` ← `seal.signer` | (본인) | seal | 1쪽 [873, 788, 902, 804] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.customer` ← `sign.signer` | (본인) | signature | 1쪽 [873, 788, 902, 804] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.CREDITNO2` | CREDITNO.(신용장번호) | checkbox (CREDIT NO. (신용장번호)) | 2쪽 [112, 271, 343, 287] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.ADVICENO2` | ADVICENO.(신용장통지번호) | checkbox (ADVICE NO.(신용장통지번호)) | 2쪽 [112, 338, 373, 354] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.ISSUINGBANK2` | ISSUINGBANK(개설은행) | checkbox (ISSUING BANK(개설은행)) | 2쪽 [112, 405, 341, 420] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.ISSUINGDATE2` | ISSUINGDATE(개설일) | checkbox (ISSUING DATE(개설일)) | 2쪽 [112, 471, 322, 487] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.AMOUNT2` | AMOUNT(금액) | checkbox (AMOUNT(금액)) | 2쪽 [112, 538, 268, 554] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키 `a` ← `b`:** 질문·정답은 공통 키 a, 서식의 원래 키는 b (키 사전이 정함). **정한 곳:** 템플릿에서 그 칸 자리 (html·코드 서식) / 칸 목록의 그 칸 (원본 서식).

## 질문 → 답 (seed 1000000 로 그린 실제 문항)

질문은 모델에게 가는 글 전부, 답은 데이터의 정답 (그린 문서의 값·위치). 질문 문장·답 꼴은 공통 `docgen/forms/_common/questions.json`.

### 서류 분류 `classify` · 채점 acc

질문:

```
이 문서는 고객이 은행에 제출한 서류입니다. 서류의 정식 명칭(서류명)을 답하세요. 설명 없이 서류명만 한 줄로 답하세요.
```

답:

```json
"신용장 확인 신청 및 확약서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "센텀지점",
 "남궁예태"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"센텀지점"
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
- 취급점: 취급점
- customer.name: (본인) (고객 성명)
```

답:

```json
[{"key": "취급점", "value": "센텀지점", "bbox_2d": [198, 200, 288, 226], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [713, 784, 802, 807], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- check.CREDITNO: CREDITNO.(신용장번호) (같은 항목명 중 1번째 칸, 체크박스, 보기: CREDIT NO. (신용장번호))
- check.ADVICENO: ADVICENO.(신용장통지번호) (같은 항목명 중 1번째 칸, 체크박스, 보기: ADVICE NO.(신용장통지번호))
- check.ISSUINGBANK: ISSUINGBANK(개설은행) (같은 항목명 중 1번째 칸, 체크박스, 보기: ISSUING BANK(개설은행))
- check.ISSUINGDATE: ISSUINGDATE(개설일) (같은 항목명 중 1번째 칸, 체크박스, 보기: ISSUING DATE(개설일))
- check.AMOUNT: AMOUNT(금액) (같은 항목명 중 1번째 칸, 체크박스, 보기: AMOUNT(금액))
- seal.customer: (본인) (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: (본인) (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- check.CREDITNO2: CREDITNO.(신용장번호) (같은 항목명 중 2번째 칸, 체크박스, 보기: CREDIT NO. (신용장번호))
- check.ADVICENO2: ADVICENO.(신용장통지번호) (같은 항목명 중 2번째 칸, 체크박스, 보기: ADVICE NO.(신용장통지번호))
- check.ISSUINGBANK2: ISSUINGBANK(개설은행) (같은 항목명 중 2번째 칸, 체크박스, 보기: ISSUING BANK(개설은행))
- check.ISSUINGDATE2: ISSUINGDATE(개설일) (같은 항목명 중 2번째 칸, 체크박스, 보기: ISSUING DATE(개설일))
- check.AMOUNT2: AMOUNT(금액) (같은 항목명 중 2번째 칸, 체크박스, 보기: AMOUNT(금액))
```

답:

```json
[{"key": "check.CREDITNO", "value": "CREDIT NO. (신용장번호)", "bbox_2d": [112, 271, 129, 287], "page": 1},
 {"key": "check.ADVICENO", "value": "ADVICE NO.(신용장통지번호)", "bbox_2d": [112, 338, 129, 354], "page": 1},
 {"key": "check.ISSUINGBANK", "value": "ISSUING BANK(개설은행)", "bbox_2d": [112, 405, 129, 420], "page": 1},
 {"key": "check.ISSUINGDATE", "value": null},
 {"key": "check.AMOUNT", "value": "AMOUNT(금액)", "bbox_2d": [112, 538, 129, 554], "page": 1},
 {"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [873, 788, 902, 804], "page": 1},
 {"key": "check.CREDITNO2", "value": null},
 {"key": "check.ADVICENO2", "value": null},
 {"key": "check.ISSUINGBANK2", "value": null},
 {"key": "check.ISSUINGDATE2", "value": "ISSUING DATE(개설일)", "bbox_2d": [112, 471, 129, 487], "page": 2},
 {"key": "check.AMOUNT2", "value": null}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기·위치·항목명 | studio ① 서식 › 영역 편집 (저장하면 `fields.json` items) | 재검수 → 카드 다시 만들기 |
| 값이 이상함 | 영역 편집에서 그 칸의 값 출처·값 종류 | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf286 --show` · `python -m docgen.preview hf286 --out work/hf286`
