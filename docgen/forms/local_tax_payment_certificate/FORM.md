# 지방세 납세증명서 (`local_tax_payment_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card local_tax_payment_certificate · card-hash: 3453f6cc8eb2 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** tax · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 지방세 납세증명서 (다른 이름: 지방세 납세증명(신청)서)
- **쓰이는 업무:** 개인사업자 대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 정부24·위택스 발급 지방세 납세증명서 (체납 없음). 개인사업자면 상호·사업자등록번호도 적는다.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/tax.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 17칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [78, 96, 221, 108] | 늘 | 템플릿 | generate.py | look/template.html.j2:18 · fields.json:20 | 묻기 |
| `customer.name` ← `taxpayer.name` | 성명(법인명) | text | 1쪽 [305, 136, 374, 150] | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:50 | 묻기 |
| `customer.rrn` ← `taxpayer.rrn` | 주민등록번호(법인등록번호) | rrn | 1쪽 [724, 136, 841, 150] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:55 | 묻기 |
| `customer.address` ← `taxpayer.address` | 주소(영업소) | text | 1쪽 [305, 208, 895, 221] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:40 | 묻기 |
| `purpose` | 증명서사용목적 | text | 1쪽 [305, 239, 412, 252] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:30 | 묻기 |
| `valid_period` | 증명서유효기간 | text | 1쪽 [305, 270, 580, 283] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:65 | 묻기 |
| `deferral` | 징수유예등또는체납처분유예의내역 | text | 1쪽 [468, 375, 532, 387] | 15/16 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:10 | 묻기 |
| `arrears` | 체납액 | text | 1쪽 [305, 419, 340, 432] | 늘 | 템플릿 | generate.py | look/template.html.j2:51 · fields.json:5 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [430, 538, 570, 551] | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:15 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [319, 573, 658, 594] | 늘 | 템플릿 | generate.py | look/template.html.j2:55 · fields.json:25 | 묻기 |
| `customer.trade_name` ← `taxpayer.trade_name` | 상호 | - | - | 8/16 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:60 | 묻기 |
| `customer.biz_no` ← `taxpayer.biz_no` | 사업자등록번호 | - | - | 8/16 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:45 | 묻기 |
| `deferrals.*.tax_year` | 과세연도 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:95 | 묻기 |
| `deferrals.*.tax_item` | 세목 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:90 | 묻기 |
| `deferrals.*.due` | 납부기한 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:80 | 묻기 |
| `deferrals.*.amount` | 세액 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:75 | 묻기 |
| `deferrals.*.period` | 유예기간 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:85 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [646, 551, 736, 614] | 늘 | 템플릿 | generate.py | fields.json:35 | 묻기 |

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
"지방세 납세증명서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "5038-7344-4678-6904",
 "남궁예태",
 "850328-2******",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "국민은행 제출",
 "2025년 04월 01일 ~ 2025년 04월 30일",
 "해당없음",
 "없음",
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
"2025년 04월 01일 ~ 2025년 04월 30일"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"서울특별시 서초구청장"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- issue_no: 발급번호
- customer.name: 성명(법인명) (고객 성명)
- customer.rrn: 주민등록번호(법인등록번호) (고객 주민등록번호)
- customer.address: 주소(영업소) (고객 주소)
- purpose: 증명서사용목적
- valid_period: 증명서유효기간
- deferral: 징수유예등또는체납처분유예의내역
- arrears: 체납액
- issue_date: 발급일
- issuer: 발급기관
```

답:

```json
[{"key": "issue_no", "value": "5038-7344-4678-6904", "bbox_2d": [78, 96, 221, 108], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [305, 136, 374, 150], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [724, 136, 841, 150], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [305, 208, 895, 221], "page": 1},
 {"key": "purpose", "value": "국민은행 제출", "bbox_2d": [305, 239, 412, 252], "page": 1},
 {"key": "valid_period", "value": "2025년 04월 01일 ~ 2025년 04월 30일", "bbox_2d": [305, 270, 580, 283], "page": 1},
 {"key": "deferral", "value": "해당없음", "bbox_2d": [468, 375, 532, 387], "page": 1},
 {"key": "arrears", "value": "없음", "bbox_2d": [305, 419, 340, 432], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [430, 538, 570, 551], "page": 1},
 {"key": "issuer", "value": "서울특별시 서초구청장", "bbox_2d": [319, 573, 658, 594], "page": 1}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [646, 551, 736, 614], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check local_tax_payment_certificate` → `python -m docgen.formdir card local_tax_payment_certificate` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `generate.py` 가 돌려주는 dict 에 그 키 값 | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` | 다시 |
| 답의 값 | `generate.py` (값 만드는 함수). 파이썬 대신 정하려면 `fields.json` 의 그 칸 `source` | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (studio html 편집). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions local_tax_payment_certificate --show` · `python -m docgen.preview local_tax_payment_certificate --out work/local_tax_payment_certificate`
