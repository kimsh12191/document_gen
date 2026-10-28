# 건강보험료 납부확인서 (`health_insurance_payment`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card health_insurance_payment · card-hash: be82fc9175d7 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** income · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 건강보험료 납부확인서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 국민건강보험공단 발급 건강보험료 납부확인서 (직장가입자 본인부담분, 월별 고지·납부 보험료를 건강/장기요양 구분).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/income.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 25칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [144, 57, 237, 68] | 늘 | generate.py | look/template.html.j2:9 | 묻기 |
| `customer.name` ← `person.name` | 성명 | text | 1쪽 [228, 170, 293, 184] | 늘 | generate.py | look/template.html.j2:14 | 묻기 |
| `customer.rrn` ← `person.rrn` | 주민등록번호 | rrn | 1쪽 [660, 170, 772, 184] | 7/16 | generate.py | look/template.html.j2:16 | 묻기 |
| `customer.address` ← `person.address` | 주소 | text | 1쪽 [228, 199, 564, 212] | 늘 | generate.py | look/template.html.j2:17 | 묻기 |
| `member_kind` | 가입자구분 | text | 1쪽 [228, 227, 310, 240] | 늘 | generate.py | look/template.html.j2:18 | 묻기 |
| `period` | 대상기간 | text | 1쪽 [660, 227, 784, 240] | 늘 | generate.py | look/template.html.j2:18 | 묻기 |
| `employer.name` ← `workplace.name` | 사업장명칭 | text | 1쪽 [228, 255, 363, 268] | 늘 | generate.py | look/template.html.j2:19 | 묻기 |
| `workplace.mgmt_no` | 사업장관리번호 | number | 1쪽 [660, 255, 750, 268] | 늘 | generate.py | look/template.html.j2:19 | 묻기 |
| `employer.address` ← `workplace.address` | 소재지 | text | 1쪽 [228, 283, 510, 297] | 늘 | generate.py | look/template.html.j2:20 | 묻기 |
| `rows.*.month` | 년월 | month | 1쪽 [101, 393, 150, 405] (1행) | 늘 | generate.py | look/template.html.j2:34 | 묻기 |
| `rows.*.notice_health` | 고지보험료(건강보험) | number | 1쪽 [225, 393, 274, 405] (1행) | 늘 | generate.py | look/template.html.j2:35 | 묻기 |
| `rows.*.notice_ltc` | 고지보험료(장기요양) | number | 1쪽 [334, 393, 375, 405] (1행) | 늘 | generate.py | look/template.html.j2:36 | 묻기 |
| `rows.*.health` | 납부보험료(건강보험) | number | 1쪽 [436, 393, 485, 405] (1행) | 늘 | generate.py | look/template.html.j2:37 | 묻기 |
| `rows.*.ltc` | 납부보험료(장기요양) | number | 1쪽 [544, 393, 586, 405] (1행) | 늘 | generate.py | look/template.html.j2:38 | 묻기 |
| `rows.*.total` | 납부보험료(계) | amount | 1쪽 [655, 393, 704, 405] (1행) | 늘 | generate.py | look/template.html.j2:39 | 묻기 |
| `rows.*.paid_date` | 납부일자 | date | 1쪽 [782, 393, 850, 405] (1행) | 늘 | generate.py | look/template.html.j2:40 | 묻기 |
| `sum.notice_health` | 고지보험료(건강보험)합계 | number | 1쪽 [213, 671, 274, 684] | 늘 | generate.py | look/template.html.j2:45 | 묻기 |
| `sum.notice_ltc` | 고지보험료(장기요양)합계 | number | 1쪽 [326, 671, 375, 684] | 늘 | generate.py | look/template.html.j2:45 | 묻기 |
| `sum.health` | 납부보험료(건강보험)합계 | number | 1쪽 [424, 671, 485, 684] | 늘 | generate.py | look/template.html.j2:46 | 묻기 |
| `sum.ltc` | 납부보험료(장기요양)합계 | number | 1쪽 [537, 671, 586, 684] | 늘 | generate.py | look/template.html.j2:46 | 묻기 |
| `sum.total` | 납부보험료(계)합계 | amount | 1쪽 [643, 671, 704, 684] | 늘 | generate.py | look/template.html.j2:47 | 묻기 |
| `purpose` | 용도 | text | 1쪽 [228, 703, 314, 716] | 늘 | generate.py | look/template.html.j2:52 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [442, 829, 558, 842] | 늘 | generate.py | look/template.html.j2:63 | 묻기 |
| `customer.birth` ← `person.birth` | 생년월일 | - | - | 9/16 | generate.py | look/template.html.j2:15 | 묻기 |
| `rows.*.note` | 비고 | - | - (1행) | 2/16 | generate.py | look/template.html.j2:41 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [630, 841, 748, 925] | 늘 | generate.py | - | 묻기 |

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
"건강보험료 납부확인서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "63-848670-4594",
 "남궁예태",
 "850328-2******",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "직장가입자",
 "2024.03 ~ 2025.02",
 "주식회사 다온패션",
 "12388812120",
 "부산광역시 해운대구 해운대로 326, 7층",
 "2024.03",
 "140,470",
 "18,190",
 "158,660",
 "2024.04.10",
 "2024.04",
 "2024.05.10",
 "2024.05",
 "2024.06.10",
 "2024.06",
 "2024.07.10",
 "2024.07",
 "2024.08.12",
 "2024.08",
 "2024.09.10",
 "2024.09",
 "2024.10.10",
 "2024.10",
 "2024.11.11",
 "2024.11",
 "2024.12.10",
 "2024.12",
 "2025.01.10",
 "2025.01",
 "145,640",
 "18,860",
 "164,500",
 "2025.02.10",
 "2025.02",
 "2025.03.10",
 "1,695,980",
 "219,620",
 "1,915,600",
 "은행 제출용",
 "2025년 4월 1일"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"18,190"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"140,470"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- customer.name: 성명 (고객 성명)
- employer.name: 사업장명칭 (직장 이름)
- workplace.mgmt_no: 사업장관리번호
- rows.0.total: 납부보험료(계) (1행)
- rows.1.paid_date: 납부일자 (2행)
- rows.2.month: 년월 (3행)
- rows.3.ltc: 납부보험료(장기요양) (4행)
- rows.3.total: 납부보험료(계) (4행)
- rows.4.month: 년월 (5행)
- rows.4.notice_health: 고지보험료(건강보험) (5행)
- rows.4.notice_ltc: 고지보험료(장기요양) (5행)
- rows.4.health: 납부보험료(건강보험) (5행)
- rows.4.paid_date: 납부일자 (5행)
- rows.5.health: 납부보험료(건강보험) (6행)
- rows.5.paid_date: 납부일자 (6행)
- rows.6.notice_health: 고지보험료(건강보험) (7행)
- rows.6.notice_ltc: 고지보험료(장기요양) (7행)
- rows.6.health: 납부보험료(건강보험) (7행)
- rows.6.ltc: 납부보험료(장기요양) (7행)
- rows.7.month: 년월 (8행)
- rows.7.notice_health: 고지보험료(건강보험) (8행)
- rows.7.health: 납부보험료(건강보험) (8행)
- rows.7.ltc: 납부보험료(장기요양) (8행)
- rows.7.total: 납부보험료(계) (8행)
- rows.7.paid_date: 납부일자 (8행)
- rows.8.notice_health: 고지보험료(건강보험) (9행)
- rows.9.month: 년월 (10행)
- rows.9.health: 납부보험료(건강보험) (10행)
- rows.9.ltc: 납부보험료(장기요양) (10행)
- rows.9.total: 납부보험료(계) (10행)
- rows.9.paid_date: 납부일자 (10행)
- rows.10.health: 납부보험료(건강보험) (11행)
- rows.10.total: 납부보험료(계) (11행)
- rows.10.paid_date: 납부일자 (11행)
- rows.11.month: 년월 (12행)
- rows.11.paid_date: 납부일자 (12행)
- sum.notice_health: 고지보험료(건강보험)합계
- sum.notice_ltc: 고지보험료(장기요양)합계
- purpose: 용도
- issue_date: 발급일
```

답:

```json
[{"key": "customer.name", "value": "남궁예태", "bbox_2d": [228, 170, 293, 184], "page": 1},
 {"key": "employer.name", "value": "주식회사 다온패션", "bbox_2d": [228, 255, 363, 268], "page": 1},
 {"key": "workplace.mgmt_no", "value": "12388812120", "bbox_2d": [660, 255, 750, 268], "page": 1},
 {"key": "rows.0.total", "value": "158,660", "bbox_2d": [655, 393, 704, 405], "page": 1},
 {"key": "rows.1.paid_date", "value": "2024.05.10", "bbox_2d": [782, 416, 850, 428], "page": 1},
 {"key": "rows.2.month", "value": "2024.05", "bbox_2d": [101, 439, 150, 452], "page": 1},
 {"key": "rows.3.ltc", "value": "18,190", "bbox_2d": [544, 462, 586, 475], "page": 1},
 {"key": "rows.3.total", "value": "158,660", "bbox_2d": [655, 462, 704, 475], "page": 1},
 {"key": "rows.4.month", "value": "2024.07", "bbox_2d": [101, 486, 150, 498], "page": 1},
 {"key": "rows.4.notice_health", "value": "140,470", "bbox_2d": [225, 486, 274, 498], "page": 1},
 {"key": "rows.4.notice_ltc", "value": "18,190", "bbox_2d": [334, 486, 375, 498], "page": 1},
 {"key": "rows.4.health", "value": "140,470", "bbox_2d": [436, 486, 485, 498], "page": 1},
 {"key": "rows.4.paid_date", "value": "2024.08.12", "bbox_2d": [782, 486, 850, 498], "page": 1},
 {"key": "rows.5.health", "value": "140,470", "bbox_2d": [436, 509, 485, 521], "page": 1},
 {"key": "rows.5.paid_date", "value": "2024.09.10", "bbox_2d": [782, 509, 850, 521], "page": 1},
 {"key": "rows.6.notice_health", "value": "140,470", "bbox_2d": [225, 532, 274, 545], "page": 1},
 {"key": "rows.6.notice_ltc", "value": "18,190", "bbox_2d": [334, 532, 375, 545], "page": 1},
 {"key": "rows.6.health", "value": "140,470", "bbox_2d": [436, 532, 485, 545], "page": 1},
 {"key": "rows.6.ltc", "value": "18,190", "bbox_2d": [544, 532, 586, 545], "page": 1},
 {"key": "rows.7.month", "value": "2024.10", "bbox_2d": [101, 555, 150, 568], "page": 1},
 {"key": "rows.7.notice_health", "value": "140,470", "bbox_2d": [225, 555, 274, 568], "page": 1},
 {"key": "rows.7.health", "value": "140,470", "bbox_2d": [436, 555, 485, 568], "page": 1},
 {"key": "rows.7.ltc", "value": "18,190", "bbox_2d": [544, 555, 586, 568], "page": 1},
 {"key": "rows.7.total", "value": "158,660", "bbox_2d": [655, 555, 704, 568], "page": 1},
 {"key": "rows.7.paid_date", "value": "2024.11.11", "bbox_2d": [782, 555, 849, 568], "page": 1},
 {"key": "rows.8.notice_health", "value": "140,470", "bbox_2d": [225, 579, 274, 591], "page": 1},
 {"key": "rows.9.month", "value": "2024.12", "bbox_2d": [101, 602, 150, 614], "page": 1},
 {"key": "rows.9.health", "value": "140,470", "bbox_2d": [436, 602, 485, 614], "page": 1},
 {"key": "rows.9.ltc", "value": "18,190", "bbox_2d": [544, 602, 586, 614], "page": 1},
 {"key": "rows.9.total", "value": "158,660", "bbox_2d": [655, 602, 704, 614], "page": 1},
 {"key": "rows.9.paid_date", "value": "2025.01.10", "bbox_2d": [782, 602, 850, 614], "page": 1},
 {"key": "rows.10.health", "value": "145,640", "bbox_2d": [436, 625, 485, 637], "page": 1},
 {"key": "rows.10.total", "value": "164,500", "bbox_2d": [655, 625, 704, 637], "page": 1},
 {"key": "rows.10.paid_date", "value": "2025.02.10", "bbox_2d": [782, 625, 850, 637], "page": 1},
 {"key": "rows.11.month", "value": "2025.02", "bbox_2d": [101, 648, 150, 661], "page": 1},
 {"key": "rows.11.paid_date", "value": "2025.03.10", "bbox_2d": [782, 648, 850, 661], "page": 1},
 {"key": "sum.notice_health", "value": "1,695,980", "bbox_2d": [213, 671, 274, 684], "page": 1},
 {"key": "sum.notice_ltc", "value": "219,620", "bbox_2d": [326, 671, 375, 684], "page": 1},
 {"key": "purpose", "value": "은행 제출용", "bbox_2d": [228, 703, 314, 716], "page": 1},
 {"key": "issue_date", "value": "2025년 4월 1일", "bbox_2d": [442, 829, 558, 842], "page": 1}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [630, 841, 748, 925], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions health_insurance_payment --show` · `python -m docgen.preview health_insurance_payment --out work/health_insurance_payment`
