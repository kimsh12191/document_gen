# 잔액증명서 (`balance_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card balance_certificate · card-hash: 112d724ba1a5 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** finance · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 잔액증명서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 은행 예금잔액증명서 (예금주·고객번호 / 과목·계좌번호·예금잔액·미결제타점권·질권·지급정지·압류 여부 / 합계).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/finance.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 19칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `cert_no` | 증명서번호 | text | 1쪽 [151, 53, 249, 63] | 늘 | generate.py | look/template.html.j2:8 | 묻기 |
| `customer.name` ← `holder.name` | 예금주 | text | 1쪽 [276, 154, 340, 167] | 늘 | generate.py | look/template.html.j2:10 | 묻기 |
| `customer.rrn` ← `holder.rrn` | 고객번호(주민등록번호) | rrn | 1쪽 [659, 154, 769, 167] | 늘 | generate.py | look/template.html.j2:10 | 묻기 |
| `base_date` | 기준일 | text | 1쪽 [276, 184, 432, 196] | 늘 | generate.py | look/template.html.j2:10 | 묻기 |
| `rows.*.kind` | 과목 | text | 1쪽 [131, 276, 195, 289] (1행) | 늘 | generate.py | look/template.html.j2:16 | 묻기 |
| `rows.*.account_no` | 계좌번호 | account_no | 1쪽 [307, 276, 420, 287] (1행) | 늘 | generate.py | look/template.html.j2:17 | 묻기 |
| `rows.*.balance` | 예금잔액 | amount | 1쪽 [543, 276, 615, 289] (1행) | 늘 | generate.py | look/template.html.j2:18 | 묻기 |
| `rows.*.uncleared` | 미결제타점권 | number | 1쪽 [701, 276, 708, 289] (1행) | 늘 | generate.py | look/template.html.j2:19 | 묻기 |
| `rows.*.pledge` | 질권 | text | 1쪽 [748, 276, 764, 289] (1행) | 늘 | generate.py | look/template.html.j2:20 | 묻기 |
| `rows.*.restriction` | 지급정지·압류·가압류 | text | 1쪽 [850, 276, 866, 289] (1행) | 늘 | generate.py | look/template.html.j2:21 | 묻기 |
| `rows.*.fx_amount` | 외화잔액 | amount | 1쪽 [129, 353, 198, 363] (1행) | 1/16 | generate.py | look/template.html.j2:16 | 묻기 |
| `currency` | 통화 | text | 1쪽 [366, 441, 406, 453] | 늘 | generate.py | look/template.html.j2:25 | 묻기 |
| `total` | 합계 | amount | 1쪽 [543, 441, 615, 453] | 늘 | generate.py | look/template.html.j2:25 | 묻기 |
| `total_korean` | 합계금액(한글) | amount_korean | 1쪽 [266, 470, 558, 483] | 늘 | generate.py | look/template.html.j2:26 | 묻기 |
| `purpose` | 용도 | text | 1쪽 [225, 506, 309, 519] | 늘 | generate.py | look/template.html.j2:31 | 묻기 |
| `fx_rate` | 매매기준율 | text | 1쪽 [337, 534, 458, 545] | 1/16 | generate.py | look/template.html.j2:33 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [444, 643, 556, 655] | 늘 | generate.py | look/template.html.j2:37 | 묻기 |
| `issuer` | 발급점 | text | 1쪽 [342, 676, 635, 696] | 늘 | generate.py | look/template.html.j2:36 | 묻기 |
| `remarks.*` | 비고 | - | - (1행) | 2/16 | generate.py | - | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [623, 654, 713, 718] | 늘 | generate.py | - | 묻기 |

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
"잔액증명서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "제 2025-75992 호",
 "남궁예태",
 "850328-2******",
 "2025년 04월 01일 현재",
 "저축예금",
 "478303-40-826627",
 "12,543,666",
 "0",
 "무",
 "주택청약종합저축",
 "763624-10-654057",
 "8,000,000",
 "외화보통예금(JPY)",
 "JPY 348,473",
 "340406-10-148768",
 "3,315,461",
 "KRW",
 "23,859,127",
 "금 이천삼백팔십오만구천일백이십칠원정",
 "유학 신청용",
 "JPY 951.43 (100엔당)",
 "2025년 4월 1일",
 "국민은행 센텀지점장"
]
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

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"저축예금"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- cert_no: 증명서번호
- customer.name: 예금주 (고객 성명)
- customer.rrn: 고객번호(주민등록번호) (고객 주민등록번호)
- base_date: 기준일
- rows.0.kind: 과목 (1행)
- rows.0.account_no: 계좌번호 (1행)
- rows.0.balance: 예금잔액 (1행)
- rows.0.uncleared: 미결제타점권 (1행)
- rows.0.pledge: 질권 (1행)
- rows.0.restriction: 지급정지·압류·가압류 (1행)
- rows.1.kind: 과목 (2행)
- rows.1.account_no: 계좌번호 (2행)
- rows.1.balance: 예금잔액 (2행)
- rows.1.uncleared: 미결제타점권 (2행)
- rows.1.pledge: 질권 (2행)
- rows.1.restriction: 지급정지·압류·가압류 (2행)
- rows.2.kind: 과목 (3행)
- rows.2.fx_amount: 외화잔액 (3행)
- rows.2.account_no: 계좌번호 (3행)
- rows.2.balance: 예금잔액 (3행)
- rows.2.uncleared: 미결제타점권 (3행)
- rows.2.pledge: 질권 (3행)
- rows.2.restriction: 지급정지·압류·가압류 (3행)
- currency: 통화
- total: 합계
- total_korean: 합계금액(한글)
- purpose: 용도
- fx_rate: 매매기준율
- issue_date: 발급일
- issuer: 발급점
```

답:

```json
[{"key": "cert_no", "value": "제 2025-75992 호", "bbox_2d": [151, 53, 249, 63], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [276, 154, 340, 167], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [659, 154, 769, 167], "page": 1},
 {"key": "base_date", "value": "2025년 04월 01일 현재", "bbox_2d": [276, 184, 432, 196], "page": 1},
 {"key": "rows.0.kind", "value": "저축예금", "bbox_2d": [131, 276, 195, 289], "page": 1},
 {"key": "rows.0.account_no", "value": "478303-40-826627", "bbox_2d": [307, 276, 420, 287], "page": 1},
 {"key": "rows.0.balance", "value": "12,543,666", "bbox_2d": [543, 276, 615, 289], "page": 1},
 {"key": "rows.0.uncleared", "value": "0", "bbox_2d": [701, 276, 708, 289], "page": 1},
 {"key": "rows.0.pledge", "value": "무", "bbox_2d": [748, 276, 764, 289], "page": 1},
 {"key": "rows.0.restriction", "value": "무", "bbox_2d": [850, 276, 866, 289], "page": 1},
 {"key": "rows.1.kind", "value": "주택청약종합저축", "bbox_2d": [99, 306, 227, 318], "page": 1},
 {"key": "rows.1.account_no", "value": "763624-10-654057", "bbox_2d": [307, 306, 420, 317], "page": 1},
 {"key": "rows.1.balance", "value": "8,000,000", "bbox_2d": [551, 306, 615, 318], "page": 1},
 {"key": "rows.1.uncleared", "value": "0", "bbox_2d": [701, 306, 708, 318], "page": 1},
 {"key": "rows.1.pledge", "value": "무", "bbox_2d": [748, 306, 764, 318], "page": 1},
 {"key": "rows.1.restriction", "value": "무", "bbox_2d": [850, 306, 866, 318], "page": 1},
 {"key": "rows.2.kind", "value": "외화보통예금(JPY)", "bbox_2d": [97, 335, 230, 348], "page": 1},
 {"key": "rows.2.fx_amount", "value": "JPY 348,473", "bbox_2d": [129, 353, 198, 363], "page": 1},
 {"key": "rows.2.account_no", "value": "340406-10-148768", "bbox_2d": [307, 343, 420, 355], "page": 1},
 {"key": "rows.2.balance", "value": "3,315,461", "bbox_2d": [551, 344, 615, 356], "page": 1},
 {"key": "rows.2.uncleared", "value": "0", "bbox_2d": [701, 344, 708, 356], "page": 1},
 {"key": "rows.2.pledge", "value": "무", "bbox_2d": [748, 344, 764, 356], "page": 1},
 {"key": "rows.2.restriction", "value": "무", "bbox_2d": [850, 344, 866, 356], "page": 1},
 {"key": "currency", "value": "KRW", "bbox_2d": [366, 441, 406, 453], "page": 1},
 {"key": "total", "value": "23,859,127", "bbox_2d": [543, 441, 615, 453], "page": 1},
 {"key": "total_korean", "value": "금 이천삼백팔십오만구천일백이십칠원정", "bbox_2d": [266, 470, 558, 483], "page": 1},
 {"key": "purpose", "value": "유학 신청용", "bbox_2d": [225, 506, 309, 519], "page": 1},
 {"key": "fx_rate", "value": "JPY 951.43 (100엔당)", "bbox_2d": [337, 534, 458, 545], "page": 1},
 {"key": "issue_date", "value": "2025년 4월 1일", "bbox_2d": [444, 643, 556, 655], "page": 1},
 {"key": "issuer", "value": "국민은행 센텀지점장", "bbox_2d": [342, 676, 635, 696], "page": 1}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [623, 654, 713, 718], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions balance_certificate --show` · `python -m docgen.preview balance_certificate --out work/balance_certificate`
