# 위임장 (`hana_official_028`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hana_official_028 · card-hash: 4579748ae715 -->

- **종류:** html 서식 (값은 fields.json 의 값 출처, 모양은 템플릿)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 위임장
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hana_official_028 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 원문을 대조한 HTML. 위임장. 기존 hf028 PDF 배경 버전도 유지. 인쇄층은 HTML 글자·SVG 선, 고객 기재란은 기존 생성 규칙. 출처: https://image.kebhana.com/cont/customer/customer07/customer0701/customer070101/__icsFiles/afieldfile/2020/05/29/5_08_0041_20200601.pdf

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `form.json` | 이름·그룹·출처 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 16칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `agent.name` | 성명 | text | 1쪽 [308, 156, 402, 179] | 늘 | 템플릿 | - | - | 묻기 |
| `agent.relation` | 본인과의관계 | text | 1쪽 [309, 189, 332, 210] | 늘 | 템플릿 | - | - | 묻기 |
| `agent.address` | 주소 | text | 1쪽 [311, 223, 775, 247] | 늘 | 템플릿 | - | - | 묻기 |
| `account` | 계좌번호 | account_no | 1쪽 [305, 357, 469, 380] | 늘 | 템플릿 | - | - | 묻기 |
| `기타사항` | 기타사항 | text | 1쪽 [310, 468, 411, 491] | 늘 | 템플릿 | - | - | 묻기 |
| `agent.birth` | 생년월일 | date | 1쪽 [715, 156, 861, 177] | 늘 | 템플릿 | - | - | 묻기 |
| `agent.phone` | 연락처 | phone | 1쪽 [712, 189, 842, 212] | 늘 | 템플릿 | - | - | 묻기 |
| `위임내용확인일시` | 위임내용확인일시 | text | - | 늘 | 템플릿 | - | - | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [193, 861, 314, 869] | 늘 | 템플릿 | - | - | 묻기 |
| `signer.name` | 성명(업체명) | text | 1쪽 [480, 776, 574, 797] | 늘 | 템플릿 | - | - | 묻기 |
| `customer.birth` | 생년월일(사업자번호) | date | 1쪽 [309, 821, 462, 841] | 늘 | 템플릿 | - | - | 묻기 |
| `customer.address2` | 주소 | text | 1쪽 [307, 849, 771, 876] | 늘 | 템플릿 | - | - | 묻기 |
| `customer.phone` | 연락처 | phone | 1쪽 [715, 820, 847, 841] | 늘 | 템플릿 | - | - | 묻기 |
| `취급점` | 취급점 | text | 1쪽 [184, 116, 271, 137] | 늘 | 템플릿 | - | - | 묻기 |
| `date` | 작성일 | date | 1쪽 [433, 630, 599, 649] | 늘 | 템플릿 | - | - | 묻기 |
| `customer.name` | 성명 | text | 1쪽 [231, 771, 291, 785] | 늘 | 템플릿 | - | - | 묻기 |

## 체크·도장·서명 (marks) — 10칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.해당` | 해당 | checkbox (에 √ 표시하며 기타의 경우 구체적인 위임내용을 기재합니다) | 1쪽 [221, 259, 681, 275] | 늘 | 템플릿 | - | - | 묻기 |
| `check.신규계좌개설` | 신규계좌개설 | checkbox (입출금이자유로운예금 / 정기예금 / 적금 / 기타 () | 1쪽 [315, 293, 499, 309] | 늘 | 템플릿 | - | - | 묻기 |
| `check.신규계좌개설2` | 신규계좌개설 | checkbox (개인(신용)정보 수집 이용 및 제공 동의서(상품서비스 안내 등) 작성) | 1쪽 [315, 327, 820, 342] | 늘 | 템플릿 | - | - | 묻기 |
| `check.세부내용` | 세부내용 | checkbox (비밀번호 변경 / 통장/인감 분실 / 계좌해지 / 기타 () | 1쪽 [315, 394, 440, 410] | 늘 | 템플릿 | - | - | 묻기 |
| `seal.customer` ← `seal.signer` | 성명(업체명) | seal | 1쪽 [754, 768, 806, 805] | 늘 | 템플릿 | - | - | 묻기 |
| `sign.customer` ← `sign.signer` | 성명(업체명) | signature | 1쪽 [752, 780, 807, 793] | 늘 | 템플릿 | - | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [772, 39, 846, 83] | 늘 | 템플릿 | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [772, 39, 846, 83] | 늘 | 템플릿 | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [861, 45, 907, 77] | 늘 | 템플릿 | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [846, 39, 922, 83] | 늘 | 템플릿 | - | - | 묻기 |

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
"위임장"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "남궁찬윤",
 "부",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "540-121210-96628",
 "해당 없음",
 "1952년 10월 28일",
 "010-7568-9115",
 "남궁예태",
 "1985년 3월 28일",
 "010-6144-1173",
 "센텀지점"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"남궁찬윤"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"해당 없음"
```

### 정보 추출 `kie` · 채점 vl_f1 (값+위치)

틀 (질문의 항목 한 줄 · 답 항목 하나 · 빈 칸일 때) — `questions.json` 의 `kie`:

```
item:         - {key}: {label}{note}
answer:       {"key": "{key}", "value": "{value}", "bbox_2d": "{bbox_2d}", "page": "{page}"}
answer_empty: {"key": "{key}", "value": null}
```

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- agent.name: 성명 (대리인 성명, 같은 항목명 중 1번째 칸)
- agent.relation: 본인과의관계 (대리인 관계)
- agent.address: 주소 (대리인 주소, 같은 항목명 중 1번째 칸)
- account: 계좌번호
- 기타사항: 기타사항
- agent.birth: 생년월일 (대리인 생년월일)
- agent.phone: 연락처 (대리인 연락처, 같은 항목명 중 1번째 칸)
- 위임내용확인일시: 위임내용확인일시
- customer.address: 주소 (고객 주소, 같은 항목명 중 2번째 칸)
- signer.name: 성명(업체명) (고객 본인의 성명)
- customer.birth: 생년월일(사업자번호) (고객 생년월일)
- customer.address2: 주소 (같은 항목명 중 3번째 칸)
- customer.phone: 연락처 (고객 연락처, 같은 항목명 중 2번째 칸)
- 취급점: 취급점
- date: 작성일
- customer.name: 성명 (고객 성명, 같은 항목명 중 2번째 칸)
```

답:

```json
[{"key": "agent.name", "value": "남궁찬윤", "bbox_2d": [308, 156, 402, 179], "page": 1},
 {"key": "agent.relation", "value": "부", "bbox_2d": [309, 189, 332, 210], "page": 1},
 {"key": "agent.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [311, 223, 775, 247], "page": 1},
 {"key": "account", "value": "540-121210-96628", "bbox_2d": [305, 357, 469, 380], "page": 1},
 {"key": "기타사항", "value": "해당 없음", "bbox_2d": [310, 468, 411, 491], "page": 1},
 {"key": "agent.birth", "value": "1952년 10월 28일", "bbox_2d": [715, 156, 861, 177], "page": 1},
 {"key": "agent.phone", "value": "010-7568-9115", "bbox_2d": [712, 189, 842, 212], "page": 1},
 {"key": "위임내용확인일시", "value": null},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [193, 861, 314, 869], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [480, 776, 574, 797], "page": 1},
 {"key": "customer.birth", "value": "1985년 3월 28일", "bbox_2d": [309, 821, 462, 841], "page": 1},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [307, 849, 771, 876], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [715, 820, 847, 841], "page": 1},
 {"key": "취급점", "value": "센텀지점", "bbox_2d": [184, 116, 271, 137], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [433, 630, 599, 649], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [231, 771, 291, 785], "page": 1}]
```

### 체크·도장·서명 `marks` · 채점 vl_f1 (값+위치)

틀 (질문의 항목 한 줄 · 답 항목 하나 · 빈 칸일 때) — `questions.json` 의 `marks`:

```
item:         - {key}: {label}{note}
answer:       {"key": "{key}", "value": "{value}", "bbox_2d": "{bbox_2d}", "page": "{page}"}
answer_empty: {"key": "{key}", "value": null}
```

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- check.해당: 해당 (체크박스, 보기: 에 √ 표시하며 기타의 경우 구체적인 위임내용을 기재합니다)
- check.신규계좌개설: 신규계좌개설 (같은 항목명 중 1번째 칸, 체크박스, 보기: 입출금이자유로운예금 / 정기예금 / 적금 / 기타 ()
- check.신규계좌개설2: 신규계좌개설 (같은 항목명 중 2번째 칸, 체크박스, 보기: 개인(신용)정보 수집 이용 및 제공 동의서(상품서비스 안내 등) 작성)
- check.세부내용: 세부내용 (체크박스, 보기: 비밀번호 변경 / 통장/인감 분실 / 계좌해지 / 기타 ()
- seal.customer: 성명(업체명) (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 성명(업체명) (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.해당", "value": "에 √ 표시하며 기타의 경우 구체적인 위임내용을 기재합니다", "bbox_2d": [221, 262, 239, 275], "page": 1},
 {"key": "check.신규계좌개설", "value": "입출금이자유로운예금", "bbox_2d": [315, 295, 333, 309], "page": 1},
 {"key": "check.신규계좌개설2", "value": null},
 {"key": "check.세부내용", "value": "비밀번호 변경", "bbox_2d": [315, 396, 333, 410], "page": 1},
 {"key": "seal.customer", "value": true, "bbox_2d": [754, 768, 806, 805], "page": 1},
 {"key": "sign.customer", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": true, "bbox_2d": [772, 39, 846, 83], "page": 1},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [861, 45, 907, 77], "page": 1},
 {"key": "sign.staff.책임자", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hana_official_028 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hana_official_028` → `python -m docgen.formdir card hana_official_028` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `fields.json` 의 `fields` 에 키·source | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` + `fields.json` 의 그 키 | 다시 |
| 답의 값 | `fields.json` 의 그 칸 `source` ([값 출처 목록](../_common/values.md)) | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` 의 `adjust(d, p, rng)` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (studio html 편집). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hana_official_028 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hana_official_028 --show` · `python -m docgen.preview hana_official_028 --out work/hana_official_028`
