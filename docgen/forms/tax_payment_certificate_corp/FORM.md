# 납세증명서(법인) (`tax_payment_certificate_corp`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card tax_payment_certificate_corp · card-hash: c8e9bad4c7be -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** tax · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 납세증명서(법인)
- **쓰이는 업무:** 법인 여신
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 홈택스 발급 국세 납세증명서 (법인).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/business.py`, `docgen/docs/tax.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 20칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [79, 100, 192, 111] | 늘 | generate.py | - | 묻기 |
| `taxpayer.corp_name` | 상호(법인명) | text | 1쪽 [307, 129, 409, 141] | 늘 | generate.py | - | 묻기 |
| `customer.biz_no` ← `taxpayer.biz_no` | 사업자등록번호 | biz_no | 1쪽 [722, 129, 809, 141] | 늘 | generate.py | - | 묻기 |
| `customer.ceo` ← `taxpayer.ceo` | 성명(대표자) | text | 1쪽 [307, 165, 368, 177] | 늘 | generate.py | - | 묻기 |
| `customer.corp_reg_no` ← `taxpayer.corp_reg_no` | 법인등록번호 | corp_reg_no | 1쪽 [722, 165, 827, 177] | 늘 | generate.py | - | 묻기 |
| `customer.address` ← `taxpayer.address` | 주소(본점) | text | 1쪽 [307, 200, 744, 213] | 늘 | generate.py | - | 묻기 |
| `valid_period` | 증명서유효기간 | text | 1쪽 [307, 229, 553, 241] | 늘 | generate.py | - | 묻기 |
| `valid_reason` | 유효기간을정한사유 | text | 1쪽 [307, 257, 712, 270] | 늘 | generate.py | - | 묻기 |
| `purpose` | 사용목적 | text | 1쪽 [573, 285, 669, 298] | 늘 | generate.py | - | 묻기 |
| `payer` | 대금지급자 | amount | - | 늘 | generate.py | - | 묻기 |
| `deferral` | 연장ㆍ유예명세 | text | 1쪽 [472, 411, 528, 421] | 15/16 | generate.py | - | 묻기 |
| `arrears` | 체납액 | text | 1쪽 [307, 452, 337, 464] | 늘 | generate.py | - | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [437, 584, 563, 597] | 늘 | generate.py | - | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [397, 616, 580, 636] | 늘 | generate.py | - | 묻기 |
| `deferrals.*.kind` | 연장ㆍ유예종류 | - | - (1행) | 1/16 | generate.py | - | 묻기 |
| `deferrals.*.period` | 연장ㆍ유예기간 | - | - (1행) | 1/16 | generate.py | - | 묻기 |
| `deferrals.*.tax_period` | 과세기간 | - | - (1행) | 1/16 | generate.py | - | 묻기 |
| `deferrals.*.tax_item` | 세목 | - | - (1행) | 1/16 | generate.py | - | 묻기 |
| `deferrals.*.due` | 납부기한 | - | - (1행) | 1/16 | generate.py | - | 묻기 |
| `deferrals.*.amount` | 세액 | - | - (1행) | 1/16 | generate.py | - | 묻기 |

## 체크·도장·서명 (marks) — 2칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `purpose_type` | 사용목적 | checkbox (대금 수령 / 해외이주 / 기타) | 1쪽 [517, 285, 547, 298] | 늘 | generate.py | - | 묻기 |
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [568, 595, 658, 659] | 늘 | generate.py | - | 묻기 |

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
"납세증명서(법인)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "5793-194-4684-328",
 "(주)미래케미칼",
 "702-81-38348",
 "남궁예태",
 "200112-7951835",
 "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)",
 "2025년 04월 01일 ~ 2025년 04월 25일",
 "2025년 1기 부가가치세 예정 납부기한(2025년 4월 25일) 도래",
 "금융기관 제출",
 "해당없음",
 "없음",
 "2025년 04월 01일",
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
"(주)미래케미칼"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"금융기관 제출"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- issue_no: 발급번호
- taxpayer.corp_name: 상호(법인명)
- customer.biz_no: 사업자등록번호 (고객 사업자등록번호)
- customer.ceo: 성명(대표자) (고객 대표자)
- customer.corp_reg_no: 법인등록번호 (고객 법인등록번호)
- customer.address: 주소(본점) (고객 주소)
- valid_period: 증명서유효기간
- valid_reason: 유효기간을정한사유
- purpose: 사용목적
- payer: 대금지급자
- deferral: 연장ㆍ유예명세
- arrears: 체납액
- issue_date: 발급일
- issuer: 발급기관
```

답:

```json
[{"key": "issue_no", "value": "5793-194-4684-328", "bbox_2d": [79, 100, 192, 111], "page": 1},
 {"key": "taxpayer.corp_name", "value": "(주)미래케미칼", "bbox_2d": [307, 129, 409, 141], "page": 1},
 {"key": "customer.biz_no", "value": "702-81-38348", "bbox_2d": [722, 129, 809, 141], "page": 1},
 {"key": "customer.ceo", "value": "남궁예태", "bbox_2d": [307, 165, 368, 177], "page": 1},
 {"key": "customer.corp_reg_no", "value": "200112-7951835", "bbox_2d": [722, 165, 827, 177], "page": 1},
 {"key": "customer.address", "value": "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)", "bbox_2d": [307, 200, 744, 213], "page": 1},
 {"key": "valid_period", "value": "2025년 04월 01일 ~ 2025년 04월 25일", "bbox_2d": [307, 229, 553, 241], "page": 1},
 {"key": "valid_reason", "value": "2025년 1기 부가가치세 예정 납부기한(2025년 4월 25일) 도래", "bbox_2d": [307, 257, 712, 270], "page": 1},
 {"key": "purpose", "value": "금융기관 제출", "bbox_2d": [573, 285, 669, 298], "page": 1},
 {"key": "payer", "value": null},
 {"key": "deferral", "value": "해당없음", "bbox_2d": [472, 411, 528, 421], "page": 1},
 {"key": "arrears", "value": "없음", "bbox_2d": [307, 452, 337, 464], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [437, 584, 563, 597], "page": 1},
 {"key": "issuer", "value": "제주세무서장", "bbox_2d": [397, 616, 580, 636], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- purpose_type: 사용목적 (체크박스, 보기: 대금 수령 / 해외이주 / 기타)
- seal.issuer: 발급기관직인 (도장)
```

답:

```json
[{"key": "purpose_type", "value": "기타", "bbox_2d": [494, 285, 513, 298], "page": 1},
 {"key": "seal.issuer", "value": true, "bbox_2d": [568, 595, 658, 659], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions tax_payment_certificate_corp --show` · `python -m docgen.preview tax_payment_certificate_corp --out work/tax_payment_certificate_corp`
