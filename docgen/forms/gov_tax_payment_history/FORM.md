# 납부내역증명 (`gov_tax_payment_history`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card gov_tax_payment_history · card-hash: 4fded530ae0d -->

- **종류:** html 서식 (값은 fields.json 의 값 출처, 모양은 템플릿)
- **그룹:** tax · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 납부내역증명
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 납부내역증명 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://www.law.go.kr/LSW/flDownload.do?flSeq=155626763&flNm=%5B%EB%B3%84%EC%A7%80+19%5D+%EB%82%A9%EB%B6%80%EB%82%B4%EC%97%AD%EC%A6%9D%EB%AA%85%28%EA%B5%AD%EB%AC%B8%29&bylClsCd=200203

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `form.json` | 이름·그룹·출처 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 9칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `customer.name` ← `official.name` | 성명 | text | 1쪽 [275, 160, 335, 175] | 늘 | `profile.person.name` | look/template.html.j2:47 · fields.json:5 | 묻기 |
| `customer.rrn` ← `official.rrn` | 주민등록번호 | rrn | 1쪽 [702, 161, 816, 173] | 늘 | `profile.person.rrn` | look/template.html.j2:48 · fields.json:10 | 묻기 |
| `customer.address` ← `official.address` | 주소 | text | 1쪽 [275, 237, 596, 253] | 늘 | `profile.person.address.road_short` | look/template.html.j2:49 · fields.json:15 | 묻기 |
| `corp.name` ← `official.company` | 상호 | text | 1쪽 [275, 199, 335, 215] | 늘 | `profile.business.name` | look/template.html.j2:50 · fields.json:20 | 묻기 |
| `corp.biz_no` ← `official.biz_no` | 사업자등록번호 | biz_no | 1쪽 [702, 201, 796, 213] | 늘 | `profile.business.biz_no` | look/template.html.j2:51 · fields.json:25 | 묻기 |
| `official.tax_year` | 귀속연도 | number | 1쪽 [110, 417, 140, 428] | 늘 | `rule:fixed` | look/template.html.j2:52 · fields.json:30 | 묻기 |
| `official.tax_kind` | 세목 | text | 1쪽 [184, 416, 251, 428] | 늘 | `rule:fixed` | look/template.html.j2:53 · fields.json:36 | 묻기 |
| `official.paid_on` | 납부일 | date | 1쪽 [355, 418, 414, 427] | 늘 | `rule:fixed` | look/template.html.j2:54 · fields.json:42 | 묻기 |
| `official.paid` | 납부금액 | number | 1쪽 [456, 416, 523, 428] | 늘 | `rule:amount` | look/template.html.j2:55 · fields.json:48 | 묻기 |

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
"납부내역증명"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "남궁예태",
 "850328-2489940",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "새한커피",
 "133-64-53148",
 "2025",
 "종합소득세",
 "2026.05.31",
 "4,880,000"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2025"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"종합소득세"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- customer.name: 성명 (고객 성명)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- customer.address: 주소 (고객 주소)
- corp.name: 상호 (법인·사업자 상호)
- corp.biz_no: 사업자등록번호 (법인·사업자 사업자등록번호)
- official.tax_year: 귀속연도
- official.tax_kind: 세목
- official.paid_on: 납부일
- official.paid: 납부금액
```

답:

```json
[{"key": "customer.name", "value": "남궁예태", "bbox_2d": [275, 160, 335, 175], "page": 1},
 {"key": "customer.rrn", "value": "850328-2489940", "bbox_2d": [702, 161, 816, 173], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [275, 237, 596, 253], "page": 1},
 {"key": "corp.name", "value": "새한커피", "bbox_2d": [275, 199, 335, 215], "page": 1},
 {"key": "corp.biz_no", "value": "133-64-53148", "bbox_2d": [702, 201, 796, 213], "page": 1},
 {"key": "official.tax_year", "value": "2025", "bbox_2d": [110, 417, 140, 428], "page": 1},
 {"key": "official.tax_kind", "value": "종합소득세", "bbox_2d": [184, 416, 251, 428], "page": 1},
 {"key": "official.paid_on", "value": "2026.05.31", "bbox_2d": [355, 418, 414, 427], "page": 1},
 {"key": "official.paid", "value": "4,880,000", "bbox_2d": [456, 416, 523, 428], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions gov_tax_payment_history --show` · `python -m docgen.preview gov_tax_payment_history --out work/gov_tax_payment_history`
