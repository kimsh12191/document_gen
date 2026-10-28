# 납세증명서(국세완납증명) (`tax_payment_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card tax_payment_certificate · card-hash: 0904b1b925ef -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** tax · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 납세증명서(국세완납증명) (다른 이름: 납세증명서)
- **쓰이는 업무:** 개인사업자 대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 홈택스 발급 국세 납세증명서 (개인사업자).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/business.py`, `docgen/docs/tax.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 14칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [78, 96, 192, 107] | 늘 | generate.py | look/template.html.j2:24 | 묻기 |
| `customer.trade_name` ← `taxpayer.trade_name` | 상호(법인명) | text | 1쪽 [305, 125, 367, 138] | 늘 | generate.py | look/template.html.j2:31 | 묻기 |
| `customer.biz_no` ← `taxpayer.biz_no` | 사업자등록번호 | biz_no | 1쪽 [724, 125, 811, 138] | 늘 | generate.py | look/template.html.j2:32 | 묻기 |
| `customer.name` ← `taxpayer.name` | 성명(대표자) | text | 1쪽 [305, 161, 367, 173] | 늘 | generate.py | look/template.html.j2:33 | 묻기 |
| `customer.rrn` ← `taxpayer.rrn` | 주민등록번호 | rrn | 1쪽 [724, 161, 829, 173] | 늘 | generate.py | look/template.html.j2:35 | 묻기 |
| `customer.address` ← `taxpayer.address` | 주소(본점) | text | 1쪽 [305, 197, 838, 209] | 늘 | generate.py | look/template.html.j2:36 | 묻기 |
| `valid_period` | 증명서유효기간 | text | 1쪽 [305, 225, 554, 238] | 늘 | generate.py | look/template.html.j2:37 | 묻기 |
| `valid_reason` | 유효기간을정한사유 | text | - | 늘 | generate.py | look/template.html.j2:38 | 묻기 |
| `purpose` | 사용목적 | text | 1쪽 [574, 282, 671, 294] | 늘 | generate.py | look/template.html.j2:40 | 묻기 |
| `payer` | 대금지급자 | text | 1쪽 [305, 310, 383, 323] | 늘 | generate.py | look/template.html.j2:41 | 묻기 |
| `deferral` | 연장ㆍ유예명세 | text | 1쪽 [472, 407, 528, 418] | 늘 | generate.py | look/template.html.j2:52 | 묻기 |
| `arrears` | 체납액 | text | 1쪽 [305, 449, 336, 461] | 늘 | generate.py | look/template.html.j2:56 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [437, 581, 563, 594] | 늘 | generate.py | look/template.html.j2:60 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [397, 613, 581, 633] | 늘 | generate.py | look/template.html.j2:60 | 묻기 |

## 체크·도장·서명 (marks) — 2칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `purpose_type` | 사용목적 | checkbox (대금 수령 / 해외이주 / 기타) | 1쪽 [328, 282, 394, 294] | 늘 | generate.py | look/template.html.j2:39 | 묻기 |
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [569, 592, 658, 656] | 늘 | generate.py | - | 묻기 |

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
"납세증명서(국세완납증명)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "7452-462-3773-485",
 "새한커피",
 "133-64-53148",
 "남궁예태",
 "850328-2******",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "2025년 04월 01일 ~ 2025년 04월 30일",
 "용역대금 수령",
 "서울특별시",
 "해당없음",
 "없음",
 "2025년 04월 01일",
 "반포세무서장"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"850328-2******"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2025년 04월 01일"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- issue_no: 발급번호
- customer.trade_name: 상호(법인명) (고객 상호)
- customer.biz_no: 사업자등록번호 (고객 사업자등록번호)
- customer.name: 성명(대표자) (고객 성명)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
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
[{"key": "issue_no", "value": "7452-462-3773-485", "bbox_2d": [78, 96, 192, 107], "page": 1},
 {"key": "customer.trade_name", "value": "새한커피", "bbox_2d": [305, 125, 367, 138], "page": 1},
 {"key": "customer.biz_no", "value": "133-64-53148", "bbox_2d": [724, 125, 811, 138], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [305, 161, 367, 173], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [724, 161, 829, 173], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [305, 197, 838, 209], "page": 1},
 {"key": "valid_period", "value": "2025년 04월 01일 ~ 2025년 04월 30일", "bbox_2d": [305, 225, 554, 238], "page": 1},
 {"key": "valid_reason", "value": null},
 {"key": "purpose", "value": "용역대금 수령", "bbox_2d": [574, 282, 671, 294], "page": 1},
 {"key": "payer", "value": "서울특별시", "bbox_2d": [305, 310, 383, 323], "page": 1},
 {"key": "deferral", "value": "해당없음", "bbox_2d": [472, 407, 528, 418], "page": 1},
 {"key": "arrears", "value": "없음", "bbox_2d": [305, 449, 336, 461], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [437, 581, 563, 594], "page": 1},
 {"key": "issuer", "value": "반포세무서장", "bbox_2d": [397, 613, 581, 633], "page": 1}]
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
[{"key": "purpose_type", "value": "대금 수령", "bbox_2d": [305, 282, 324, 294], "page": 1},
 {"key": "seal.issuer", "value": true, "bbox_2d": [569, 592, 658, 656], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions tax_payment_certificate --show` · `python -m docgen.preview tax_payment_certificate --out work/tax_payment_certificate`
