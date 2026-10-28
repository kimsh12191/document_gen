# 지방세 세목별 과세증명서 (`local_tax_assessment`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card local_tax_assessment · card-hash: 523fa5afaeac -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** tax · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 지방세 세목별 과세증명서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 주소지 시·군·구청장이 발급하는 지방세 세목별 과세증명서 (재산세·자동차세·주민세 등).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/business.py`, `docgen/docs/tax.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 19칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [248, 84, 377, 94] | 늘 | generate.py | look/template.html.j2:28 | 묻기 |
| `customer.name` ← `taxpayer.name` | 성명(법인명) | text | 1쪽 [378, 168, 443, 180] | 늘 | generate.py | look/template.html.j2:38 | 묻기 |
| `customer.rrn` ← `taxpayer.rrn` | 주민(법인,외국인)등록번호 | rrn | 1쪽 [731, 168, 842, 180] | 늘 | generate.py | look/template.html.j2:39 | 묻기 |
| `customer.address` ← `taxpayer.address` | 주소(영업소) | text | 1쪽 [378, 199, 899, 227] | 늘 | generate.py | look/template.html.j2:40 | 묻기 |
| `period` | 과세연도 | text | 1쪽 [378, 246, 493, 258] | 늘 | generate.py | look/template.html.j2:41 | 묻기 |
| `purpose` | 사용목적 | text | 1쪽 [731, 246, 800, 258] | 늘 | generate.py | look/template.html.j2:42 | 묻기 |
| `items.*.tax_item` | 세목 | text | 1쪽 [101, 343, 193, 354] (1행) | 늘 | generate.py | look/template.html.j2:52 | 묻기 |
| `items.*.levied` | 부과연월 | month | 1쪽 [226, 343, 270, 354] (1행) | 늘 | generate.py | look/template.html.j2:53 | 묻기 |
| `items.*.kind` | 구분 | text | 1쪽 [316, 343, 357, 354] (1행) | 늘 | generate.py | look/template.html.j2:54 | 묻기 |
| `items.*.object` | 과세대상 | text | 1쪽 [389, 343, 474, 354] (1행) | 늘 | generate.py | look/template.html.j2:55 | 묻기 |
| `items.*.base` | 과세표준 | text | 1쪽 [622, 343, 627, 354] (1행) | 늘 | generate.py | look/template.html.j2:56 | 묻기 |
| `items.*.tax` | 세액 | amount | 1쪽 [689, 343, 720, 354] (1행) | 늘 | generate.py | look/template.html.j2:57 | 묻기 |
| `items.*.edu` | 지방교육세 | number | 1쪽 [777, 343, 808, 354] (1행) | 늘 | generate.py | look/template.html.j2:58 | 묻기 |
| `items.*.total` | 합계 | amount | 1쪽 [876, 343, 907, 354] (1행) | 늘 | generate.py | look/template.html.j2:59 | 묻기 |
| `sum.tax` | 세액합계 | amount | 1쪽 [665, 593, 720, 604] | 늘 | generate.py | look/template.html.j2:63 | 묻기 |
| `sum.edu` | 지방교육세합계 | number | 1쪽 [763, 593, 808, 604] | 늘 | generate.py | look/template.html.j2:64 | 묻기 |
| `sum.total` | 총합계 | amount | 1쪽 [852, 593, 907, 604] | 늘 | generate.py | look/template.html.j2:65 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [434, 688, 566, 701] | 늘 | generate.py | look/template.html.j2:70 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [325, 721, 652, 742] | 늘 | generate.py | look/template.html.j2:70 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [640, 700, 730, 763] | 늘 | generate.py | - | 묻기 |

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
"지방세 세목별 과세증명서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "1708-3858-0247-7057",
 "남궁예태",
 "850328-2489940",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "2023년 ~ 2024년",
 "은행 제출",
 "주민세(개인분)",
 "2023.08",
 "정기분",
 "세대주 개인분",
 "-",
 "6,000",
 "1,500",
 "7,500",
 "주민세(사업소분)",
 "사업소 부산광역시 해운대구 좌동순환로 237, 7층",
 "50,000",
 "12,500",
 "62,500",
 "재산세(주택)",
 "2023.09",
 "정기분(2/2)",
 "서초구 반포동 661",
 "535,950,000",
 "756,900",
 "151,380",
 "908,280",
 "자동차세",
 "2023.12",
 "2기분",
 "393구9569 승용",
 "1,353cc",
 "66,290",
 "19,880",
 "86,170",
 "2024.06",
 "1기분",
 "61,560",
 "18,460",
 "80,020",
 "2024.07",
 "정기분(1/2)",
 "520,650,000",
 "726,300",
 "145,260",
 "871,560",
 "2024.08",
 "2024.09",
 "2024.12",
 "2,510,910",
 "526,700",
 "3,037,610",
 "2025년 04월 01일",
 "서울특별시 서초구청장"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"주민세(개인분)"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"520,650,000"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- issue_no: 발급번호
- period: 과세연도
- items.0.tax_item: 세목 (1행)
- items.0.base: 과세표준 (1행)
- items.1.tax: 세액 (2행)
- items.1.edu: 지방교육세 (2행)
- items.2.tax_item: 세목 (3행)
- items.2.kind: 구분 (3행)
- items.2.object: 과세대상 (3행)
- items.2.tax: 세액 (3행)
- items.2.total: 합계 (3행)
- items.3.kind: 구분 (4행)
- items.3.base: 과세표준 (4행)
- items.4.levied: 부과연월 (5행)
- items.4.base: 과세표준 (5행)
- items.4.edu: 지방교육세 (5행)
- items.4.total: 합계 (5행)
- items.5.tax_item: 세목 (6행)
- items.5.levied: 부과연월 (6행)
- items.5.object: 과세대상 (6행)
- items.5.tax: 세액 (6행)
- items.5.edu: 지방교육세 (6행)
- items.6.tax_item: 세목 (7행)
- items.6.levied: 부과연월 (7행)
- items.6.kind: 구분 (7행)
- items.6.tax: 세액 (7행)
- items.7.tax_item: 세목 (8행)
- items.7.levied: 부과연월 (8행)
- items.7.object: 과세대상 (8행)
- items.7.base: 과세표준 (8행)
- items.7.tax: 세액 (8행)
- items.8.levied: 부과연월 (9행)
- items.8.object: 과세대상 (9행)
- items.8.tax: 세액 (9행)
- items.9.tax_item: 세목 (10행)
- items.9.base: 과세표준 (10행)
- items.9.tax: 세액 (10행)
- items.9.edu: 지방교육세 (10행)
- sum.edu: 지방교육세합계
- issue_date: 발급일
```

답:

```json
[{"key": "issue_no", "value": "1708-3858-0247-7057", "bbox_2d": [248, 84, 377, 94], "page": 1},
 {"key": "period", "value": "2023년 ~ 2024년", "bbox_2d": [378, 246, 493, 258], "page": 1},
 {"key": "items.0.tax_item", "value": "주민세(개인분)", "bbox_2d": [101, 343, 193, 354], "page": 1},
 {"key": "items.0.base", "value": "-", "bbox_2d": [622, 343, 627, 354], "page": 1},
 {"key": "items.1.tax", "value": "50,000", "bbox_2d": [682, 376, 720, 387], "page": 1},
 {"key": "items.1.edu", "value": "12,500", "bbox_2d": [770, 376, 808, 387], "page": 1},
 {"key": "items.2.tax_item", "value": "재산세(주택)", "bbox_2d": [108, 409, 186, 420], "page": 1},
 {"key": "items.2.kind", "value": "정기분(2/2)", "bbox_2d": [302, 409, 370, 420], "page": 1},
 {"key": "items.2.object", "value": "서초구 반포동 661", "bbox_2d": [389, 409, 498, 420], "page": 1},
 {"key": "items.2.tax", "value": "756,900", "bbox_2d": [675, 409, 720, 420], "page": 1},
 {"key": "items.2.total", "value": "908,280", "bbox_2d": [862, 409, 907, 420], "page": 1},
 {"key": "items.3.kind", "value": "2기분", "bbox_2d": [319, 429, 353, 439], "page": 1},
 {"key": "items.3.base", "value": "1,353cc", "bbox_2d": [584, 429, 627, 439], "page": 1},
 {"key": "items.4.levied", "value": "2024.06", "bbox_2d": [226, 448, 270, 459], "page": 1},
 {"key": "items.4.base", "value": "1,353cc", "bbox_2d": [584, 448, 627, 459], "page": 1},
 {"key": "items.4.edu", "value": "18,460", "bbox_2d": [770, 448, 808, 459], "page": 1},
 {"key": "items.4.total", "value": "80,020", "bbox_2d": [869, 448, 907, 459], "page": 1},
 {"key": "items.5.tax_item", "value": "재산세(주택)", "bbox_2d": [108, 468, 186, 479], "page": 1},
 {"key": "items.5.levied", "value": "2024.07", "bbox_2d": [226, 468, 270, 479], "page": 1},
 {"key": "items.5.object", "value": "서초구 반포동 661", "bbox_2d": [389, 468, 498, 479], "page": 1},
 {"key": "items.5.tax", "value": "726,300", "bbox_2d": [675, 468, 720, 479], "page": 1},
 {"key": "items.5.edu", "value": "145,260", "bbox_2d": [763, 468, 808, 479], "page": 1},
 {"key": "items.6.tax_item", "value": "주민세(개인분)", "bbox_2d": [101, 488, 193, 498], "page": 1},
 {"key": "items.6.levied", "value": "2024.08", "bbox_2d": [226, 488, 270, 498], "page": 1},
 {"key": "items.6.kind", "value": "정기분", "bbox_2d": [316, 488, 357, 498], "page": 1},
 {"key": "items.6.tax", "value": "6,000", "bbox_2d": [689, 488, 720, 498], "page": 1},
 {"key": "items.7.tax_item", "value": "주민세(사업소분)", "bbox_2d": [94, 521, 200, 531], "page": 1},
 {"key": "items.7.levied", "value": "2024.08", "bbox_2d": [226, 521, 270, 531], "page": 1},
 {"key": "items.7.object", "value": "사업소 부산광역시 해운대구 좌동순환로 237, 7층", "bbox_2d": [389, 507, 509, 545], "page": 1},
 {"key": "items.7.base", "value": "-", "bbox_2d": [622, 521, 627, 531], "page": 1},
 {"key": "items.7.tax", "value": "50,000", "bbox_2d": [682, 521, 720, 531], "page": 1},
 {"key": "items.8.levied", "value": "2024.09", "bbox_2d": [226, 554, 270, 564], "page": 1},
 {"key": "items.8.object", "value": "서초구 반포동 661", "bbox_2d": [389, 554, 498, 564], "page": 1},
 {"key": "items.8.tax", "value": "726,300", "bbox_2d": [675, 554, 720, 564], "page": 1},
 {"key": "items.9.tax_item", "value": "자동차세", "bbox_2d": [120, 573, 174, 584], "page": 1},
 {"key": "items.9.base", "value": "1,353cc", "bbox_2d": [584, 573, 627, 584], "page": 1},
 {"key": "items.9.tax", "value": "61,560", "bbox_2d": [682, 573, 720, 584], "page": 1},
 {"key": "items.9.edu", "value": "18,460", "bbox_2d": [770, 573, 808, 584], "page": 1},
 {"key": "sum.edu", "value": "526,700", "bbox_2d": [763, 593, 808, 604], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [434, 688, 566, 701], "page": 1}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [640, 700, 730, 763], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions local_tax_assessment --show` · `python -m docgen.preview local_tax_assessment --out work/local_tax_assessment`
