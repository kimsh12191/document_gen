# 이사회의사록 (`board_minutes`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card board_minutes · card-hash: 707fa7fd9663 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** corporate · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 이사회의사록
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa board_minutes --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 은행 차입 승인 이사회의사록 (출석 이사 기명날인).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/corporate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 26칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `datetime` | 일시 | text | 1쪽 [186, 102, 372, 112] | 늘 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:25 | 묻기 |
| `venue` | 장소 | text | 1쪽 [186, 118, 564, 128] | 늘 | 템플릿 | generate.py | look/template.html.j2:26 · fields.json:160 | 묻기 |
| `directors_total` | 이사총수 | text | 1쪽 [186, 134, 207, 144] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:35 | 묻기 |
| `directors_present` | 출석이사수 | text | 1쪽 [342, 134, 363, 144] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:30 | 묻기 |
| `remote_count` | 원격참석 | text | 1쪽 [371, 134, 486, 144] | 4/16 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:120 | 묻기 |
| `auditor_total` | 감사총수 | text | 1쪽 [186, 150, 207, 160] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:10 | 묻기 |
| `auditor_present` | 출석감사수 | text | 1쪽 [342, 150, 363, 160] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:5 | 묻기 |
| `remote_attendees` | 원격참석이사 | text | 1쪽 [98, 173, 308, 183] | 4/16 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:115 | 묻기 |
| `remote_method` | 원격참석방법 | text | 1쪽 [772, 173, 930, 183] | 4/16 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:125 | 묻기 |
| `chair` | 의장 | text | 1쪽 [249, 213, 305, 224] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:15 | 묻기 |
| `loan.lender` | 차입은행 | text | 1쪽 [143, 256, 199, 267] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:70 | 묻기 |
| `loan.bank` | 차입기관 | text | 1쪽 [264, 323, 384, 334] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:55 | 묻기 |
| `loan.kind` | 대출과목 | text | 1쪽 [264, 343, 351, 354] | 늘 | 템플릿 | generate.py | look/template.html.j2:37 · fields.json:65 | 묻기 |
| `loan.amount` | 차입금액 | amount | 1쪽 [264, 363, 525, 375] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:50 | 묻기 |
| `loan.period` | 차입기간 | text | 1쪽 [264, 383, 446, 395] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:75 | 묻기 |
| `loan.purpose` | 자금용도 | text | 1쪽 [264, 403, 370, 415] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:80 | 묻기 |
| `loan.rate` | 적용금리 | text | 1쪽 [264, 424, 322, 435] | 늘 | 템플릿 | generate.py | look/template.html.j2:41 · fields.json:85 | 묻기 |
| `loan.collateral` | 담보 | text | 1쪽 [264, 444, 399, 455] | 늘 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:60 | 묻기 |
| `end_time` | 종료시각 | text | 1쪽 [730, 537, 814, 548] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:40 | 묻기 |
| `minutes_date` | 작성일 | date | 1쪽 [451, 605, 549, 616] | 늘 | 템플릿 | generate.py | look/template.html.j2:56 · fields.json:90 | 묻기 |
| `company_name` | 상호 | text | 1쪽 [841, 632, 935, 643] | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:20 | 묻기 |
| `head_office` | 본점 | text | 1쪽 [687, 649, 935, 658] | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:45 | 묻기 |
| `notary.reg_no` | 등부번호 | text | 2쪽 [566, 70, 668, 82] | 2/16 | 템플릿 | generate.py | look/template.html.j2:66 · fields.json:110 | 묻기 |
| `notary.date` | 인증일 | date | 2쪽 [537, 133, 628, 145] | 2/16 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:95 | 묻기 |
| `notary.office` | 공증인 | text | 2쪽 [582, 148, 670, 159] | 2/16 | 템플릿 | generate.py | look/template.html.j2:70 · fields.json:105 | 묻기 |
| `notary.lawyer` | 공증담당변호사 | text | 2쪽 [639, 172, 681, 183] | 2/16 | 템플릿 | generate.py | look/template.html.j2:71 · fields.json:100 | 묻기 |

## 표 `agendas` (표 과제 table·table_read·table_find·table_qa) — 5열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `agendas.*.no` | 의안번호 | text | 1쪽 [65, 474, 132, 484] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:180 | 묻기 |
| `agendas.*.title` | 의안 | text | 1쪽 [144, 474, 329, 484] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:185 | 묻기 |
| `agendas.*.body` | 결의내용 | text | 1쪽 [65, 497, 935, 523] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:170 | 묻기 |
| `agendas.*.detail` | 세부내용 | - | - (1행) | 7/16 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:175 | 묻기 |
| `agendas.*.votes` | 표결결과 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:190 | 묻기 |

## 표 `signers` (표 과제 table·table_read·table_find·table_qa) — 3열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `signers.*.title` | 자격 | text | 1쪽 [431, 686, 523, 697] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:210 | 묻기 |
| `signers.*.name` | 성명 | text | 1쪽 [582, 686, 649, 697] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:200 | 묻기 |
| `signers.*.remote` | 비고 | text | 1쪽 [758, 729, 824, 739] (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:60 · fields.json:205 | 묻기 |

## 체크·도장·서명 (marks) — 6칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.corp` | 법인인감 | seal | 1쪽 [693, 666, 768, 718] | 늘 | 템플릿 | generate.py | fields.json:130 | 묻기 |
| `seal.signer2` | 서명인2 | seal | 1쪽 [705, 715, 761, 755] | 늘 | 템플릿 | generate.py | fields.json:140 | 묻기 |
| `seal.signer3` | 서명인3 | seal | 1쪽 [705, 758, 761, 798] | 늘 | 템플릿 | generate.py | fields.json:145 | 묻기 |
| `seal.signer4` | 서명인4 | seal | 1쪽 [705, 801, 761, 840] | 12/16 | 템플릿 | generate.py | fields.json:150 | 묻기 |
| `seal.notary` | 공증인직인 | seal | 2쪽 [681, 158, 738, 198] | 2/16 | 템플릿 | generate.py | fields.json:135 | 묻기 |
| `seal.signer5` | 서명인5 | 도장 | - | 5/16 | 템플릿 | generate.py | fields.json:155 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키는·값은:** 어디서 정해지나. 키·값 종류는 이 서식 파일에 적힌 그대로입니다 (모든 서식 공통 키 사전은 없음). "키 설명 그대로" 는 칸에 `"key"` 가 없어 키 설명이 키로 나가는 것. 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
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
"이사회의사록"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "2025년 제4380호",
 "2025년 4월 3일",
 "법무법인 동인",
 "장혜인"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2025년 4월 3일"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"법무법인 동인"
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
항목 (키: 설명 (몇 번째 행))
- notary.reg_no: 등부번호
- notary.date: 인증일
- notary.office: 공증인
- notary.lawyer: 공증담당변호사
```

답:

```json
[{"key": "notary.reg_no", "value": "2025년 제4380호", "bbox_2d": [566, 70, 668, 82], "page": 1},
 {"key": "notary.date", "value": "2025년 4월 3일", "bbox_2d": [537, 133, 628, 145], "page": 1},
 {"key": "notary.office", "value": "법무법인 동인", "bbox_2d": [582, 148, 670, 159], "page": 1},
 {"key": "notary.lawyer", "value": "장혜인", "bbox_2d": [639, 172, 681, 183], "page": 1}]
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
- seal.notary: 공증인직인 (도장)
```

답:

```json
[{"key": "seal.notary", "value": true, "bbox_2d": [681, 158, 738, 198], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa board_minutes --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check board_minutes` → `python -m docgen.formdir card board_minutes` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `generate.py` 가 돌려주는 dict 에 그 키 값 | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` | 다시 |
| 답의 값 | `generate.py` (값 만드는 함수). 파이썬 대신 정하려면 `fields.json` 의 그 칸 `source` | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (파일로). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa board_minutes --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions board_minutes --show` · `python -m docgen.preview board_minutes --out work/board_minutes`
