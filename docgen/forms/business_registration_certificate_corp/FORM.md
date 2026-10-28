# 사업자등록증(법인사업자) (`business_registration_certificate_corp`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card business_registration_certificate_corp · card-hash: 7feea1ce5084 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** business · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 사업자등록증(법인사업자)
- **쓰이는 업무:** 법인 여신
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 세무서가 발급하는 법인사업자 사업자등록증.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/business.py`, `docgen/docs/corporate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 17칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `biz_no` | 등록번호 | biz_no | 1쪽 [489, 206, 619, 223] | 늘 | generate.py | look/template.html.j2:23 | 묻기 |
| `corp.name` ← `corp_name` | 법인명(단체명) | text | 1쪽 [321, 264, 435, 277] | 늘 | generate.py | look/template.html.j2:25 | 묻기 |
| `ceo` | 대표자 | text | 1쪽 [321, 300, 389, 313] | 늘 | generate.py | look/template.html.j2:26 | 묻기 |
| `opened` | 개업연월일 | date | 1쪽 [321, 335, 462, 349] | 늘 | generate.py | look/template.html.j2:27 | 묻기 |
| `corp_reg_no` | 법인등록번호 | corp_reg_no | 1쪽 [598, 335, 714, 349] | 늘 | generate.py | look/template.html.j2:28 | 묻기 |
| `address` | 사업장소재지 | text | 1쪽 [321, 371, 806, 384] | 늘 | generate.py | look/template.html.j2:29 | 묻기 |
| `head_office` | 본점소재지 | text | 1쪽 [321, 407, 806, 420] | 늘 | generate.py | look/template.html.j2:30 | 묻기 |
| `biz_type` | 업태 | text | 1쪽 [368, 442, 419, 456] | 늘 | generate.py | look/template.html.j2:32 | 묻기 |
| `biz_item` | 종목 | text | 1쪽 [491, 442, 559, 456] | 늘 | generate.py | look/template.html.j2:33 | 묻기 |
| `issue_reason` | 발급사유 | text | 1쪽 [321, 498, 439, 511] | 늘 | generate.py | look/template.html.j2:37 | 묻기 |
| `unit_taxation` | 사업자단위과세적용사업자여부 | text | 1쪽 [467, 533, 484, 547] | 늘 | generate.py | look/template.html.j2:39 | 묻기 |
| `einvoice_email` | 전자세금계산서전용전자우편주소 | text | 1쪽 [417, 569, 559, 583] | 8/16 | generate.py | look/template.html.j2:40 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [418, 685, 582, 699] | 늘 | generate.py | look/template.html.j2:43 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [368, 729, 599, 753] | 늘 | generate.py | look/template.html.j2:44 | 묻기 |
| `sub_kinds.*.biz_type` | 업태 | - | - (1행) | 1/16 | generate.py | look/template.html.j2:34 | 묻기 |
| `sub_kinds.*.biz_item` | 종목 | - | - (1행) | 1/16 | generate.py | look/template.html.j2:35 | 묻기 |
| `co_ceo` | 대표자 | - | - | 2/16 | generate.py | look/template.html.j2:26 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [571, 705, 689, 789] | 늘 | generate.py | - | 묻기 |

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
"사업자등록증(법인사업자)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "702-81-38348",
 "(주)미래케미칼",
 "남궁예태",
 "2020 년 06 월 15 일",
 "200112-7951835",
 "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)",
 "제조업",
 "화학제품",
 "정정(본점 이전)",
 "부",
 "contact@mirae.co.kr",
 "2023 년 11 월 05 일",
 "제주세무서장"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2020 년 06 월 15 일"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"정정(본점 이전)"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- biz_no: 등록번호
- corp.name: 법인명(단체명) (법인·사업자 상호)
- ceo: 대표자
- opened: 개업연월일
- corp_reg_no: 법인등록번호
- address: 사업장소재지
- head_office: 본점소재지
- biz_type: 업태
- biz_item: 종목
- issue_reason: 발급사유
- unit_taxation: 사업자단위과세적용사업자여부
- einvoice_email: 전자세금계산서전용전자우편주소
- issue_date: 발급일
- issuer: 발급기관
```

답:

```json
[{"key": "biz_no", "value": "702-81-38348", "bbox_2d": [489, 206, 619, 223], "page": 1},
 {"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [321, 264, 435, 277], "page": 1},
 {"key": "ceo", "value": "남궁예태", "bbox_2d": [321, 300, 389, 313], "page": 1},
 {"key": "opened", "value": "2020 년 06 월 15 일", "bbox_2d": [321, 335, 462, 349], "page": 1},
 {"key": "corp_reg_no", "value": "200112-7951835", "bbox_2d": [598, 335, 714, 349], "page": 1},
 {"key": "address", "value": "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)", "bbox_2d": [321, 371, 806, 384], "page": 1},
 {"key": "head_office", "value": "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)", "bbox_2d": [321, 407, 806, 420], "page": 1},
 {"key": "biz_type", "value": "제조업", "bbox_2d": [368, 442, 419, 456], "page": 1},
 {"key": "biz_item", "value": "화학제품", "bbox_2d": [491, 442, 559, 456], "page": 1},
 {"key": "issue_reason", "value": "정정(본점 이전)", "bbox_2d": [321, 498, 439, 511], "page": 1},
 {"key": "unit_taxation", "value": "부", "bbox_2d": [467, 533, 484, 547], "page": 1},
 {"key": "einvoice_email", "value": "contact@mirae.co.kr", "bbox_2d": [417, 569, 559, 583], "page": 1},
 {"key": "issue_date", "value": "2023 년 11 월 05 일", "bbox_2d": [418, 685, 582, 699], "page": 1},
 {"key": "issuer", "value": "제주세무서장", "bbox_2d": [368, 729, 599, 753], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.issuer: 발급기관직인 (도장)
```

답:

```json
[{"key": "seal.issuer", "value": true, "bbox_2d": [571, 705, 689, 789], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `generate.py` 가 돌려주는 dict 에 그 키 값 | 미리보기로 확인 → 재검수 → 카드 다시 만들기 |
| 칸 키·항목명 바꾸기 | `look/template.html.j2` 의 `f("키", label=…)` (질문만 바꾸려면 `questions.json`) | `questions … --check` |
| 값이 이상함·칸끼리 안 맞음 | `generate.py` (값 만드는 함수) | 재검수 |
| 모양·표·문구 | `look/template.html.j2` (studio html 편집) | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions business_registration_certificate_corp --show` · `python -m docgen.preview business_registration_certificate_corp --out work/business_registration_certificate_corp`
