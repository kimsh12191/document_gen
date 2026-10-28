# 여신거래용 인감명판 등 신고서 (`hana_official_157`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hana_official_157 · card-hash: 15b1897e6fbd -->

- **종류:** html 서식 (값은 fields.json 의 값 출처, 모양은 템플릿)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 여신거래용 인감명판 등 신고서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 원문을 대조한 HTML. 여신거래용 인감명판 등 신고서. 기존 hf157 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2016/07/07/5090002_20160707.pdf

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `form.json` | 이름·그룹·출처 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 7칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `corp.name` ← `company.name` | 상호 | text | 1쪽 [373, 522, 516, 549] | 늘 | - | - | 묻기 |
| `corp.ceo` ← `company.ceo` | 대표자 | text | 1쪽 [373, 550, 461, 574] | 늘 | - | - | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [373, 583, 564, 598] | 늘 | - | - | 묻기 |
| `명판` | 명판 | text | - | 늘 | - | - | 묻기 |
| `목록.*.변경후` | 변경후 | text | 1쪽 [640, 524, 730, 548] (1행) | 늘 | - | - | 묻기 |
| `signer2.name` | 대표자(본인자필) | text | 1쪽 [532, 456, 606, 477] | 늘 | - | - | 묻기 |
| `신고사항` | 신고사항 | text | - | 늘 | - | - | 묻기 |

## 체크·도장·서명 (marks) — 12칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.customer` ← `seal.signer` | 거래용인감또는서명(서명을병용한경우및외국인에한함) | seal | 1쪽 [369, 651, 637, 698] | 늘 | - | - | 묻기 |
| `sign.customer` ← `sign.signer` | 거래용인감또는서명(서명을병용한경우및외국인에한함) | signature | 1쪽 [369, 651, 637, 698] | 늘 | - | - | 묻기 |
| `seal.corp` ← `seal.signer2` | 대표자(본인자필) | seal | 1쪽 [737, 461, 761, 473] | 늘 | - | - | 묻기 |
| `sign.signer2` | 대표자(본인자필) | signature | 1쪽 [737, 461, 761, 473] | 늘 | - | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [646, 182, 696, 217] | 늘 | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [637, 177, 705, 222] | 늘 | - | - | 묻기 |
| `seal.staff.대리` | 대리 | seal | 1쪽 [705, 177, 772, 222] | 늘 | - | - | 묻기 |
| `sign.staff.대리` | 대리 | signature | 1쪽 [705, 177, 772, 222] | 늘 | - | - | 묻기 |
| `seal.staff.차장` | 차장 | seal | 1쪽 [783, 183, 830, 216] | 늘 | - | - | 묻기 |
| `sign.staff.차장` | 차장 | signature | 1쪽 [772, 177, 841, 222] | 늘 | - | - | 묻기 |
| `seal.staff.부점장` | 부점장 | seal | 1쪽 [841, 177, 908, 222] | 늘 | - | - | 묻기 |
| `sign.staff.부점장` | 부점장 | signature | 1쪽 [841, 177, 908, 222] | 늘 | - | - | 묻기 |

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
"여신거래용 인감명판 등 신고서"
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
 "서울특별시 서초구 강남대로 357, 103동 1301호",
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
- corp.name: 상호 (법인·사업자 상호)
- corp.ceo: 대표자 (법인·사업자 대표자)
- customer.address: 주소 (고객 주소)
- 명판: 명판
- 목록.0.변경후: 변경후 (목록 1행)
- 목록.1.변경후: 변경후 (목록 2행)
- 목록.2.변경후: 변경후 (목록 3행)
- 목록.3.변경후: 변경후 (목록 4행)
- 목록.4.변경후: 변경후 (목록 5행)
- signer2.name: 대표자(본인자필) (법인·사업자의 대표자)
- 신고사항: 신고사항
```

답:

```json
[{"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [373, 522, 516, 549], "page": 1},
 {"key": "corp.ceo", "value": "남궁예태", "bbox_2d": [373, 550, 461, 574], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [373, 583, 564, 598], "page": 1},
 {"key": "명판", "value": null},
 {"key": "목록.0.변경후", "value": "해당 없음", "bbox_2d": [640, 524, 730, 548], "page": 1},
 {"key": "목록.1.변경후", "value": "해당 없음", "bbox_2d": [643, 550, 734, 576], "page": 1},
 {"key": "목록.2.변경후", "value": null},
 {"key": "목록.3.변경후", "value": null},
 {"key": "목록.4.변경후", "value": null},
 {"key": "signer2.name", "value": "남궁예태", "bbox_2d": [532, 456, 606, 477], "page": 1},
 {"key": "신고사항", "value": null}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.customer: 거래용인감또는서명(서명을병용한경우및외국인에한함) (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 거래용인감또는서명(서명을병용한경우및외국인에한함) (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.corp: 대표자(본인자필) (법인·사업자 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.signer2: 대표자(본인자필) (고객 본인의 신청인, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.대리: 대리 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.대리: 대리 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.차장: 차장 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.차장: 차장 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.부점장: 부점장 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.부점장: 부점장 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [369, 651, 637, 698], "page": 1},
 {"key": "seal.corp", "value": false},
 {"key": "sign.signer2", "value": true, "bbox_2d": [737, 461, 761, 473], "page": 1},
 {"key": "seal.staff.담당", "value": true, "bbox_2d": [646, 182, 696, 217], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.대리", "value": false},
 {"key": "sign.staff.대리", "value": true, "bbox_2d": [705, 177, 772, 222], "page": 1},
 {"key": "seal.staff.차장", "value": true, "bbox_2d": [783, 183, 830, 216], "page": 1},
 {"key": "sign.staff.차장", "value": false},
 {"key": "seal.staff.부점장", "value": false},
 {"key": "sign.staff.부점장", "value": true, "bbox_2d": [841, 177, 908, 222], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `fields.json` 의 `fields` 에 키·source | 미리보기로 확인 → 재검수 → 카드 다시 만들기 |
| 칸 키·항목명 바꾸기 | `look/template.html.j2` 의 `f("키", label=…)` + `fields.json` (질문만 바꾸려면 `questions.json`) | `questions … --check` |
| 값이 이상함 / 칸끼리 안 맞음 | `fields.json` 의 source / `generate.py` 의 `adjust(d, p, rng)` | 재검수 |
| 모양·표·문구 | `look/template.html.j2` (studio html 편집) | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hana_official_157 --show` · `python -m docgen.preview hana_official_157 --out work/hana_official_157`
