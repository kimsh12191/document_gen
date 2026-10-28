# 대출계약 철회신청서 (`hana_official_051`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hana_official_051 · card-hash: b1dea3ce527c -->

- **종류:** html 서식 (값은 fields.json 의 값 출처, 모양은 템플릿)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 대출계약 철회신청서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 원문을 대조한 HTML. 대출계약 철회신청서. 기존 hf051 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070102/__icsFiles/afieldfile/2025/06/30/5-06-0681.pdf

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
| `customer.name` | 차주 | text | 1쪽 [220, 272, 286, 283] | 늘 | - | - | 묻기 |
| `상품명` | 상품명 | text | 1쪽 [220, 299, 331, 310] | 늘 | - | - | 묻기 |
| `실행일` | 실행일 | date | 1쪽 [225, 332, 308, 344] | 늘 | - | - | 묻기 |
| `account` | 계좌번호 | account_no | 1쪽 [676, 272, 816, 283] | 늘 | - | - | 묻기 |
| `금액` | 금액 | number | 1쪽 [840, 299, 914, 310] | 늘 | - | - | 묻기 |
| `date` | 작성일 | date | 1쪽 [698, 584, 923, 602] | 늘 | - | - | 묻기 |
| `signer.name` | 신청인 | text | 1쪽 [692, 611, 758, 623] | 늘 | - | - | 묻기 |
| `date2` | 작성일 | date | 1쪽 [698, 884, 923, 902] | 늘 | - | - | 묻기 |
| `signer2.name` | 신청인 | text | 1쪽 [692, 911, 758, 922] | 늘 | - | - | 묻기 |

## 체크·도장·서명 (marks) — 12칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.customer` ← `seal.signer` | 신청인 | seal | 1쪽 [819, 609, 926, 625] | 늘 | - | - | 묻기 |
| `sign.customer` ← `sign.signer` | 신청인 | signature | 1쪽 [819, 609, 926, 625] | 늘 | - | - | 묻기 |
| `check.중도상환이나철회하지않고` | 중도상환이나철회하지않고대출유지함 | checkbox (중도상환이나 철회하지 않고 대출 유지함) | 1쪽 [98, 790, 428, 806] | 늘 | - | - | 묻기 |
| `check.기타` | 기타( | checkbox (기타 () | 1쪽 [98, 809, 168, 825] | 늘 | - | - | 묻기 |
| `seal.signer2` | 신청인 | seal | 1쪽 [819, 909, 926, 924] | 늘 | - | - | 묻기 |
| `sign.signer2` | 신청인 | signature | 1쪽 [819, 909, 926, 924] | 늘 | - | - | 묻기 |
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [711, 27, 783, 71] | 늘 | - | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [711, 27, 783, 71] | 늘 | - | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [789, 32, 837, 65] | 늘 | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [783, 27, 844, 71] | 늘 | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [844, 27, 918, 71] | 늘 | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [844, 27, 918, 71] | 늘 | - | - | 묻기 |

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
"대출계약 철회신청서"
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
 "하나 TDF 2040",
 "2024.10.03",
 "540-121210-96628",
 "3,130,000"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"3,130,000"
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
- customer.name: 차주 (고객 성명)
- 상품명: 상품명
- 실행일: 실행일
- account: 계좌번호
- 금액: 금액
- date: 작성일 (같은 항목명 중 1번째 칸)
- signer.name: 신청인 (고객 본인의 성명, 같은 항목명 중 1번째 칸)
- date2: 작성일 (같은 항목명 중 2번째 칸)
- signer2.name: 신청인 (고객 본인의 성명, 같은 항목명 중 2번째 칸)
```

답:

```json
[{"key": "customer.name", "value": "남궁예태", "bbox_2d": [220, 272, 286, 283], "page": 1},
 {"key": "상품명", "value": "하나 TDF 2040", "bbox_2d": [220, 299, 331, 310], "page": 1},
 {"key": "실행일", "value": "2024.10.03", "bbox_2d": [225, 332, 308, 344], "page": 1},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [676, 272, 816, 283], "page": 1},
 {"key": "금액", "value": "3,130,000", "bbox_2d": [840, 299, 914, 310], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [698, 584, 923, 602], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [692, 611, 758, 623], "page": 1},
 {"key": "date2", "value": "2025년 4월 1일", "bbox_2d": [698, 884, 923, 902], "page": 1},
 {"key": "signer2.name", "value": "남궁예태", "bbox_2d": [692, 911, 758, 922], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.customer: 신청인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 신청인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- check.중도상환이나철회하지않고: 중도상환이나철회하지않고대출유지함 (체크박스, 보기: 중도상환이나 철회하지 않고 대출 유지함)
- check.기타: 기타( (체크박스, 보기: 기타 ()
- seal.signer2: 신청인 (고객 본인의 신청인, 같은 항목명 중 3번째 칸, 도장)
- sign.signer2: 신청인 (고객 본인의 신청인, 같은 항목명 중 4번째 칸, 서명)
- seal.staff.본인확인: 본인확인 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.본인확인: 본인확인 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": false},
 {"key": "check.중도상환이나철회하지않고", "value": null},
 {"key": "check.기타", "value": "기타 (", "bbox_2d": [98, 811, 117, 825], "page": 1},
 {"key": "seal.signer2", "value": false},
 {"key": "sign.signer2", "value": true, "bbox_2d": [819, 909, 926, 924], "page": 1},
 {"key": "seal.staff.본인확인", "value": false},
 {"key": "sign.staff.본인확인", "value": false},
 {"key": "seal.staff.담당", "value": true, "bbox_2d": [789, 32, 837, 65], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": false},
 {"key": "sign.staff.책임자", "value": false}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hana_official_051 --show` · `python -m docgen.preview hana_official_051 --out work/hana_official_051`
