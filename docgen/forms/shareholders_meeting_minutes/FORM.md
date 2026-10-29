# 임시주주총회의사록 (`shareholders_meeting_minutes`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card shareholders_meeting_minutes · card-hash: 1ea0dcbf42a5 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** corporate · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 임시주주총회의사록
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa shareholders_meeting_minutes --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 임시(또는 정기)주주총회의사록 (이사 선임 / 정관 변경 등).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/corporate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 19칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `meeting_title` | 의사록종류 | text | 1쪽 [279, 69, 721, 99] | 늘 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:35 | 묻기 |
| `datetime` | 일시 | text | 1쪽 [241, 118, 429, 129] | 늘 | 템플릿 | generate.py | look/template.html.j2:26 · fields.json:15 | 묻기 |
| `venue` | 장소 | text | 1쪽 [241, 134, 594, 144] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:120 | 묻기 |
| `shareholders_total` | 주주의총수 | text | 1쪽 [294, 176, 316, 186] | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:105 | 묻기 |
| `issued_shares` | 발행주식의총수 | text | 1쪽 [674, 176, 728, 186] | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:30 | 묻기 |
| `shareholders_present` | 출석주주의수 | text | 1쪽 [294, 202, 316, 213] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:100 | 묻기 |
| `shares_present` | 출석주주의주식수 | text | 1쪽 [674, 202, 728, 213] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:110 | 묻기 |
| `present_ratio` | 출석비율 | percent | 1쪽 [736, 202, 787, 213] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:65 | 묻기 |
| `chair` | 의장 | text | 1쪽 [204, 330, 259, 341] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:5 | 묻기 |
| `end_time` | 종료시각 | text | 1쪽 [740, 836, 829, 847] | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:20 | 묻기 |
| `minutes_date` | 작성일 | date | 2쪽 [452, 73, 548, 84] | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:40 | 묻기 |
| `corp.name` ← `company_name` | 상호 | text | 2쪽 [822, 99, 913, 110] | 늘 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:10 | 묻기 |
| `head_office` | 본점 | text | 2쪽 [670, 116, 913, 126] | 늘 | 템플릿 | generate.py | look/template.html.j2:58 · fields.json:25 | 묻기 |
| `proxy_count` | 대리출석 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:70 | 묻기 |
| `treasury_shares` | 자기주식수 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:115 | 묻기 |
| `notary.reg_no` | 등부번호 | - | - | 3/16 | 템플릿 | generate.py | look/template.html.j2:67 · fields.json:60 | 묻기 |
| `notary.date` | 인증일 | - | - | 3/16 | 템플릿 | generate.py | look/template.html.j2:70 · fields.json:45 | 묻기 |
| `notary.office` | 공증인 | - | - | 3/16 | 템플릿 | generate.py | look/template.html.j2:71 · fields.json:55 | 묻기 |
| `notary.lawyer` | 공증담당변호사 | - | - | 3/16 | 템플릿 | generate.py | look/template.html.j2:72 · fields.json:50 | 묻기 |

## 표 `attendees` (표 과제 table·table_read·table_find·table_qa) — 4열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `attendees.*.name` | 주주명 | text | 1쪽 [259, 263, 316, 274] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:165 | 묻기 |
| `attendees.*.shares` | 소유주식수 | number | 1쪽 [499, 263, 539, 274] (1행) | 6/16 | 템플릿 | generate.py | fields.json:175 | 묻기 |
| `attendees.*.method` | 출석구분 | text | 1쪽 [578, 263, 635, 274] (1행) | 6/16 | 템플릿 | generate.py | fields.json:160 | 묻기 |
| `attendees.*.proxy` | 대리인 | text | - (1행) | 6/16 | 템플릿 | generate.py | fields.json:170 | 묻기 |

## 표 `agendas` (표 과제 table·table_read·table_find·table_qa) — 5열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `agendas.*.no` | 의안번호 | text | 1쪽 [87, 373, 152, 384] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:140 | 묻기 |
| `agendas.*.title` | 의안 | text | 1쪽 [163, 373, 382, 384] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:145 | 묻기 |
| `agendas.*.body` | 결의내용 | text | 1쪽 [87, 396, 913, 422] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:130 | 묻기 |
| `agendas.*.detail` | 세부내용 | text | 1쪽 [144, 507, 410, 518] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:135 | 묻기 |
| `agendas.*.votes` | 표결결과 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:50 · fields.json:150 | 묻기 |

## 표 `signers` (표 과제 table·table_read·table_find·table_qa) — 2열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `signers.*.title` | 자격 | text | 2쪽 [409, 154, 500, 164] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:190 | 묻기 |
| `signers.*.name` | 성명 | text | 2쪽 [560, 154, 626, 164] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:185 | 묻기 |

## 체크·도장·서명 (marks) — 5칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.corp` | 법인인감 | seal | 2쪽 [672, 133, 746, 185] | 늘 | 템플릿 | generate.py | fields.json:75 | 묻기 |
| `seal.signer2` | 서명인2 | seal | 2쪽 [684, 182, 740, 222] | 늘 | 템플릿 | generate.py | fields.json:85 | 묻기 |
| `seal.signer3` | 서명인3 | seal | 2쪽 [684, 225, 740, 265] | 10/16 | 템플릿 | generate.py | fields.json:90 | 묻기 |
| `seal.signer4` | 서명인4 | seal | 2쪽 [684, 268, 740, 307] | 2/16 | 템플릿 | generate.py | fields.json:95 | 묻기 |
| `seal.notary` | 공증인직인 | 도장 | - | 3/16 | 템플릿 | generate.py | fields.json:80 | 묻기 |

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
"임시주주총회의사록"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "정기주주총회의사록",
 "2025년 3월 27일 오전 10시 00분",
 "본점 소회의실 (제주특별자치도 제주시 첨단로 381-19, 2층)",
 "3명",
 "60,000주",
 "100.00%",
 "남궁예태",
 "40,061",
 "본인출석",
 "노도수",
 "8,278",
 "원승호",
 "11,661",
 "제1호 의안",
 "제5기(2024년도) 재무제표 승인의 건",
 "의장은 제출된 재무상태표, 손익계산서 및 이익잉여금처분계산서(안)의 내용을 설명하고 그 승인을 물은바, 출석주주 전원이 이의 없이 찬성하여 원안대로 승인 가결하다.",
 "제2호 의안",
 "감사 보수한도 승인의 건",
 "의장은 당해 사업연도 감사 보수한도액을 아래와 같이 정하고자 함을 설명하고 그 승인을 물은바, 출석주주 전원의 찬성으로 원안대로 승인 가결하다.",
 "감사 보수한도액: 금 오천만원 (₩50,000,000)",
 "제3호 의안",
 "이사 보수한도 승인의 건",
 "의장은 당해 사업연도 이사 보수한도액을 아래와 같이 정하고자 함을 설명하고 그 승인을 물은바, 출석주주 전원이 이의 없이 찬성하여 원안대로 승인 가결하다.",
 "이사 보수한도액: 금 십이억오천만원 (₩1,250,000,000)",
 "제4호 의안",
 "이사 선임의 건",
 "의장은 사내이사 노도수의 임기가 만료됨에 따라 이사를 선임할 필요가 있음을 설명하고 동인을 사내이사로 중임할 것을 물은바, 출석주주 전원의 찬성으로 이를 승인 가결하다. 피선임자는 즉석에서 그 취임을 승낙하다.",
 "사내이사  노도수 (1983년 1월 20일생)  중임",
 "제5호 의안",
 "감사 선임의 건",
 "의장은 감사 원순수의 임기 만료로 감사를 선임하여야 함을 설명하고 그 선임을 물은바, 출석주주 전원의 찬성으로 아래 사람을 감사로 선임하다. 피선임자는 즉석에서 취임을 승낙하다.",
 "감사  원순수 (1991년 6월 16일생)  중임",
 "오전 10시 55분",
 "2025년 3월 27일",
 "(주)미래케미칼",
 "제주특별자치도 제주시 첨단로 381-19, 2층",
 "의장 대표이사",
 "사내이사",
 "하혁승"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"40,061"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"본인출석"
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
- meeting_title: 의사록종류
- datetime: 일시
- venue: 장소
- shareholders_total: 주주의총수
- issued_shares: 발행주식의총수
- shareholders_present: 출석주주의수
- shares_present: 출석주주의주식수
- present_ratio: 출석비율
- chair: 의장
- end_time: 종료시각
- minutes_date: 작성일
- corp.name: 상호 (법인·사업자 상호)
- head_office: 본점
```

답:

```json
[{"key": "meeting_title", "value": "정기주주총회의사록", "bbox_2d": [279, 69, 721, 99], "page": 1},
 {"key": "datetime", "value": "2025년 3월 27일 오전 10시 00분", "bbox_2d": [241, 118, 429, 129], "page": 1},
 {"key": "venue", "value": "본점 소회의실 (제주특별자치도 제주시 첨단로 381-19, 2층)", "bbox_2d": [241, 134, 594, 144], "page": 1},
 {"key": "shareholders_total", "value": "3명", "bbox_2d": [294, 176, 316, 186], "page": 1},
 {"key": "issued_shares", "value": "60,000주", "bbox_2d": [674, 176, 728, 186], "page": 1},
 {"key": "shareholders_present", "value": "3명", "bbox_2d": [294, 202, 316, 213], "page": 1},
 {"key": "shares_present", "value": "60,000주", "bbox_2d": [674, 202, 728, 213], "page": 1},
 {"key": "present_ratio", "value": "100.00%", "bbox_2d": [736, 202, 787, 213], "page": 1},
 {"key": "chair", "value": "남궁예태", "bbox_2d": [204, 330, 259, 341], "page": 1},
 {"key": "end_time", "value": "오전 10시 55분", "bbox_2d": [740, 836, 829, 847], "page": 1},
 {"key": "minutes_date", "value": "2025년 3월 27일", "bbox_2d": [452, 73, 548, 84], "page": 2},
 {"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [822, 99, 913, 110], "page": 2},
 {"key": "head_office", "value": "제주특별자치도 제주시 첨단로 381-19, 2층", "bbox_2d": [670, 116, 913, 126], "page": 2}]
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
- seal.corp: 법인인감 (법인·사업자 도장, 도장)
- seal.signer2: 서명인2 (은행·직원의 신청인, 도장)
- seal.signer3: 서명인3 (은행·직원의 신청인, 도장)
- seal.signer4: 서명인4 (은행·직원의 신청인, 도장)
```

답:

```json
[{"key": "seal.corp", "value": true, "bbox_2d": [672, 133, 746, 185], "page": 2},
 {"key": "seal.signer2", "value": true, "bbox_2d": [684, 182, 740, 222], "page": 2},
 {"key": "seal.signer3", "value": true, "bbox_2d": [684, 225, 740, 265], "page": 2},
 {"key": "seal.signer4", "value": true, "bbox_2d": [684, 268, 740, 307], "page": 2}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 '출석구분'·'대리인' 열이 있는 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 항목명)
- name: 주주명
- shares: 소유주식수
- method: 출석구분
- proxy: 대리인
```

답:

```json
{
 "columns": [
  "name",
  "shares",
  "method",
  "proxy"
 ],
 "rows": [
  [
   "남궁예태",
   "40,061",
   "본인출석",
   null
  ],
  [
   "노도수",
   "8,278",
   "본인출석",
   null
  ],
  [
   "원승호",
   "11,661",
   "본인출석",
   null
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    259,
    263,
    635,
    274
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    266,
    283,
    635,
    294
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    266,
    303,
    635,
    314
   ],
   "page": 1
  }
 ]
}
```

### 표 찾기 `table_find` · 채점 f1_iou50 (위치)

질문:

```
이 문서에서 표를 모두 찾아 JSON 목록으로 답하세요. 여기서 표는 같은 항목 묶음(열)이 행마다 되풀이되고 행 수가 서류마다 달라지는 목록입니다. 항목명과 값이 번갈아 있는 신청서 칸, 칸 수가 정해진 결재란은 표가 아닙니다.
표마다 {{"columns": [머리글 글자, …], "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호, "n_rows": 행 수}} 를 쓰고, 여러 쪽에 걸친 표는 쪽마다 따로 씁니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 행 수에는 머리글·합계 행과 모두 빈 행을 넣지 않습니다. 표가 없으면 [] 로 답하세요.
```

답:

```json
[{"columns": ["주주명", "소유주식수", "출석구분", "대리인"], "bbox_2d": [181, 240, 879, 314], "page": 1, "n_rows": 3},
 {"columns": ["의안번호", "결의내용", "세부내용", "의안"], "bbox_2d": [87, 373, 913, 818], "page": 1, "n_rows": 5},
 {"columns": ["자격", "성명"], "bbox_2d": [409, 154, 626, 292], "page": 2, "n_rows": 4}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '소유주식수'·'대리인' 열이 있는 표를 보고 답하세요. '주주명' 칸이 '원승호'인 행의 '대리인' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
null
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '소유주식수'·'대리인' 열이 있는 표를 보고 답하세요. '소유주식수' 칸의 값을 모두 더하면 얼마입니까? 빈 칸은 0 으로 봅니다. (쉼표·단위 없이 숫자만 답하세요)
```

답:

```json
60000
```

### 표 그대로 옮기기 `table_read` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[181, 240, 879, 314] 위치의 표를 머리글까지 그대로 옮겨 JSON 으로 답하세요.
꼴: {"columns": [머리글 글자, …], "rows": [[칸 글자, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 표의 머리글을 왼쪽부터 쓰고, 머리글이 여러 줄이면 위 칸과 아래 칸 글자를 " > " 로 잇습니다.
- rows 는 행마다 columns 와 같은 순서로 칸 글자를 씁니다. 빈 칸은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 글자를 씁니다.
- 다음 쪽에서 다시 나온 머리글 행과 모두 빈 행은 빼고, 합계·소계 행은 그대로 둡니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
```

답:

```json
{
 "columns": [
  "번호",
  "주주명",
  "소유주식수",
  "출석구분",
  "대리인"
 ],
 "rows": [
  [
   "1",
   "남궁예태",
   "40,061",
   "본인출석",
   null
  ],
  [
   "2",
   "노도수",
   "8,278",
   "본인출석",
   null
  ],
  [
   "3",
   "원승호",
   "11,661",
   "본인출석",
   null
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    121,
    259,
    879,
    279
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    121,
    279,
    879,
    299
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    121,
    299,
    879,
    319
   ],
   "page": 1
  }
 ]
}
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa shareholders_meeting_minutes --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check shareholders_meeting_minutes` → `python -m docgen.formdir card shareholders_meeting_minutes` (실제 질문→답 확인).

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
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa shareholders_meeting_minutes --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions shareholders_meeting_minutes --show` · `python -m docgen.preview shareholders_meeting_minutes --out work/shareholders_meeting_minutes`
