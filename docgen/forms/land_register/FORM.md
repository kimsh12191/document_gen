# 토지대장 (`land_register`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card land_register · card-hash: 5104f2645bd1 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** real_estate · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 토지대장
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 토지대장 등본 (집합건물 대지). 소유자 변동 이력이 길면 여러 쪽.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/real_estate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 25칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `unique_no` | 고유번호 | text | 1쪽 [152, 105, 298, 115] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:60 | 묻기 |
| `drawing_no` | 도면번호 | number | 1쪽 [607, 105, 622, 115] | 늘 | 템플릿 | generate.py | look/template.html.j2:29 · fields.json:5 | 묻기 |
| `issue_no` | 발급번호 | number | 1쪽 [761, 105, 848, 115] | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:15 | 묻기 |
| `location` | 토지소재 | text | 1쪽 [152, 131, 318, 142] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:35 | 묻기 |
| `sheet_no` | 장번호 | text | 1쪽 [605, 131, 624, 142] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:55 | 묻기 |
| `processed_time` | 처리시각 | text | 1쪽 [761, 131, 855, 142] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:40 | 묻기 |
| `jibun` | 지번 | number | 1쪽 [152, 158, 174, 168] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:30 | 묻기 |
| `scale` | 축척 | text | 1쪽 [600, 158, 629, 168] | 늘 | 템플릿 | generate.py | look/template.html.j2:35 · fields.json:45 | 묻기 |
| `issuer_name` | 발급자 | text | 1쪽 [761, 158, 863, 168] | 늘 | 템플릿 | generate.py | look/template.html.j2:36 · fields.json:25 | 묻기 |
| `land.*.category` | 지목 | text | 1쪽 [74, 243, 113, 254] (1행) | 늘 | 템플릿 | generate.py | fields.json:95 | 묻기 |
| `land.*.area` | 면적 | number | 1쪽 [165, 243, 216, 254] (1행) | 늘 | 템플릿 | generate.py | fields.json:90 | 묻기 |
| `land.*.reason` | 사유 | text | 1쪽 [230, 243, 363, 268] (1행) | 늘 | 템플릿 | generate.py | fields.json:100 | 묻기 |
| `owners.*.change_date` | 변동일자 | date | 1쪽 [428, 243, 537, 254] (1행) | 늘 | 템플릿 | generate.py | fields.json:135 | 묻기 |
| `owners.*.change_cause` | 변동원인 | text | 1쪽 [434, 257, 531, 268] (1행) | 늘 | 템플릿 | generate.py | fields.json:130 | 묻기 |
| `owners.*.address` | 주소 | text | 1쪽 [560, 243, 744, 254] (1행) | 늘 | 템플릿 | generate.py | fields.json:125 | 묻기 |
| `owners.*.name` | 성명또는명칭 | text | 1쪽 [805, 243, 935, 268] (1행) | 늘 | 템플릿 | generate.py | fields.json:145 | 묻기 |
| `owners.*.reg_no` | 등록번호 | corp_reg_no | 1쪽 [821, 271, 919, 282] (1행) | 늘 | 템플릿 | generate.py | fields.json:150 | 묻기 |
| `owners.*.co_owners` | 공유자 | text | 1쪽 [861, 291, 926, 302] (1행) | 12/16 | 템플릿 | generate.py | fields.json:140 | 묻기 |
| `grades.*.date` | 등급수정년월일 | text | 1쪽 [279, 570, 381, 581] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:63 · fields.json:75 | 묻기 |
| `grades.*.grade` | 토지등급 | number | 1쪽 [320, 604, 341, 615] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:64 · fields.json:80 | 묻기 |
| `land_prices.*.base_date` | 개별공시지가기준일 | date | 1쪽 [216, 636, 282, 647] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:68 · fields.json:110 | 묻기 |
| `land_prices.*.price` | 개별공시지가 | amount | 1쪽 [226, 663, 284, 673] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:115 | 묻기 |
| `zoning` | 용도지역 | text | 1쪽 [806, 689, 929, 700] | 늘 | 템플릿 | generate.py | look/template.html.j2:71 · fields.json:65 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [437, 751, 563, 764] | 늘 | 템플릿 | generate.py | look/template.html.j2:75 · fields.json:10 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [319, 783, 659, 804] | 늘 | 템플릿 | generate.py | look/template.html.j2:74 · fields.json:20 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [647, 762, 736, 825] | 늘 | 템플릿 | generate.py | fields.json:50 | 묻기 |

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
"토지대장"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "1144612000-10661-0000",
 "23",
 "202531326690",
 "서울특별시 서초구 반포동",
 "1-2",
 "10시 29분 19초",
 "661",
 "수치",
 "무인민원발급기",
 "(08)대",
 "46,962.2",
 "(40)1992년 09월 14일",
 "구획정리 완료",
 "1993년 06월 28일",
 "(01)소유권보존",
 "서울특별시 서초구 시청로 60",
 "주식회사한양종합건설",
 "131111-2362356",
 "2004년 02월 17일",
 "(03)소유권이전",
 "서울특별시 노원구 노원로 459-15, 116동 2102호 (중계동, SK뷰리버뷰아파트)",
 "임채영",
 "외 1,395인",
 "501031-2******",
 "2022년 06월 03일",
 "서울특별시 강남구 테헤란로 132",
 "하나자산신탁주식회사",
 "135011-8178151",
 "2023년 10월 23일",
 "2025년 03월 02일",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "남궁예태",
 "850328-2******",
 "1984.07.01. 수정",
 "1987.07.01. 수정",
 "1990.01.01. 수정",
 "211",
 "223",
 "236",
 "2018/01/01",
 "2019/01/01",
 "2020/01/01",
 "2021/01/01",
 "2022/01/01",
 "2023/01/01",
 "2024/01/01",
 "9,476,000",
 "10,001,000",
 "10,829,000",
 "11,312,000",
 "11,697,000",
 "12,017,000",
 "13,065,000",
 "제3종일반주거지역",
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
"23"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"(40)1992년 09월 14일 구획정리 완료"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- unique_no: 고유번호
- drawing_no: 도면번호
- issue_no: 발급번호
- location: 토지소재
- jibun: 지번
- scale: 축척
- issuer_name: 발급자
- land.0.category: 지목 (1행)
- land.0.area: 면적 (1행)
- owners.0.change_date: 변동일자 (1행)
- owners.0.address: 주소 (1행)
- owners.0.name: 성명또는명칭 (1행)
- owners.0.reg_no: 등록번호 (1행)
- owners.1.change_date: 변동일자 (2행)
- owners.1.change_cause: 변동원인 (2행)
- owners.1.address: 주소 (2행)
- owners.1.name: 성명또는명칭 (2행)
- owners.2.change_cause: 변동원인 (3행)
- owners.2.name: 성명또는명칭 (3행)
- owners.2.co_owners: 공유자 (3행)
- owners.3.change_cause: 변동원인 (4행)
- owners.3.name: 성명또는명칭 (4행)
- owners.3.co_owners: 공유자 (4행)
- owners.3.reg_no: 등록번호 (4행)
- owners.4.change_cause: 변동원인 (5행)
- owners.4.address: 주소 (5행)
- owners.4.co_owners: 공유자 (5행)
- owners.4.reg_no: 등록번호 (5행)
- grades.0.date: 등급수정년월일 (1행)
- grades.1.date: 등급수정년월일 (2행)
- grades.2.date: 등급수정년월일 (3행)
- grades.0.grade: 토지등급 (1행)
- land_prices.2.base_date: 개별공시지가기준일 (3행)
- land_prices.3.base_date: 개별공시지가기준일 (4행)
- land_prices.4.base_date: 개별공시지가기준일 (5행)
- land_prices.5.base_date: 개별공시지가기준일 (6행)
- land_prices.1.price: 개별공시지가 (2행)
- land_prices.4.price: 개별공시지가 (5행)
- land_prices.5.price: 개별공시지가 (6행)
- issue_date: 발급일
```

답:

```json
[{"key": "unique_no", "value": "1144612000-10661-0000", "bbox_2d": [152, 105, 298, 115], "page": 1},
 {"key": "drawing_no", "value": "23", "bbox_2d": [607, 105, 622, 115], "page": 1},
 {"key": "issue_no", "value": "202531326690", "bbox_2d": [761, 105, 848, 115], "page": 1},
 {"key": "location", "value": "서울특별시 서초구 반포동", "bbox_2d": [152, 131, 318, 142], "page": 1},
 {"key": "jibun", "value": "661", "bbox_2d": [152, 158, 174, 168], "page": 1},
 {"key": "scale", "value": "수치", "bbox_2d": [600, 158, 629, 168], "page": 1},
 {"key": "issuer_name", "value": "무인민원발급기", "bbox_2d": [761, 158, 863, 168], "page": 1},
 {"key": "land.0.category", "value": "(08)대", "bbox_2d": [74, 243, 113, 254], "page": 1},
 {"key": "land.0.area", "value": "46,962.2", "bbox_2d": [165, 243, 216, 254], "page": 1},
 {"key": "owners.0.change_date", "value": "1993년 06월 28일", "bbox_2d": [428, 243, 537, 254], "page": 1},
 {"key": "owners.0.address", "value": "서울특별시 서초구 시청로 60", "bbox_2d": [560, 243, 744, 254], "page": 1},
 {"key": "owners.0.name", "value": "주식회사한양종합건설", "bbox_2d": [805, 243, 935, 268], "page": 1},
 {"key": "owners.0.reg_no", "value": "131111-2362356", "bbox_2d": [821, 271, 919, 282], "page": 1},
 {"key": "owners.1.change_date", "value": "2004년 02월 17일", "bbox_2d": [428, 291, 537, 302], "page": 1},
 {"key": "owners.1.change_cause", "value": "(03)소유권이전", "bbox_2d": [434, 305, 531, 315], "page": 1},
 {"key": "owners.1.address", "value": "서울특별시 노원구 노원로 459-15, 116동 2102호 (중계동, SK뷰리버뷰아파트)", "bbox_2d": [560, 291, 778, 329], "page": 1},
 {"key": "owners.1.name", "value": "임채영", "bbox_2d": [814, 291, 857, 302], "page": 1},
 {"key": "owners.2.change_cause", "value": "(03)소유권이전", "bbox_2d": [434, 352, 531, 363], "page": 1},
 {"key": "owners.2.name", "value": "하나자산신탁주식회사", "bbox_2d": [805, 339, 935, 363], "page": 1},
 {"key": "owners.2.co_owners", "value": "외 1,395인", "bbox_2d": [846, 352, 912, 363], "page": 1},
 {"key": "owners.3.change_cause", "value": "(03)소유권이전", "bbox_2d": [434, 400, 531, 411], "page": 1},
 {"key": "owners.3.name", "value": "임채영", "bbox_2d": [814, 386, 857, 397], "page": 1},
 {"key": "owners.3.co_owners", "value": "외 1,395인", "bbox_2d": [861, 386, 926, 397], "page": 1},
 {"key": "owners.3.reg_no", "value": "501031-2******", "bbox_2d": [821, 400, 919, 411], "page": 1},
 {"key": "owners.4.change_cause", "value": "(03)소유권이전", "bbox_2d": [434, 448, 531, 459], "page": 1},
 {"key": "owners.4.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [560, 434, 782, 472], "page": 1},
 {"key": "owners.4.co_owners", "value": "외 1,395인", "bbox_2d": [868, 434, 933, 445], "page": 1},
 {"key": "owners.4.reg_no", "value": "850328-2******", "bbox_2d": [821, 448, 919, 459], "page": 1},
 {"key": "grades.0.date", "value": "1984.07.01. 수정", "bbox_2d": [279, 570, 381, 581], "page": 1},
 {"key": "grades.1.date", "value": "1987.07.01. 수정", "bbox_2d": [524, 570, 626, 581], "page": 1},
 {"key": "grades.2.date", "value": "1990.01.01. 수정", "bbox_2d": [769, 570, 871, 581], "page": 1},
 {"key": "grades.0.grade", "value": "211", "bbox_2d": [320, 604, 341, 615], "page": 1},
 {"key": "land_prices.2.base_date", "value": "2020/01/01", "bbox_2d": [384, 636, 449, 647], "page": 1},
 {"key": "land_prices.3.base_date", "value": "2021/01/01", "bbox_2d": [467, 636, 533, 647], "page": 1},
 {"key": "land_prices.4.base_date", "value": "2022/01/01", "bbox_2d": [551, 636, 616, 647], "page": 1},
 {"key": "land_prices.5.base_date", "value": "2023/01/01", "bbox_2d": [634, 636, 700, 647], "page": 1},
 {"key": "land_prices.1.price", "value": "10,001,000", "bbox_2d": [303, 663, 368, 673], "page": 1},
 {"key": "land_prices.4.price", "value": "11,697,000", "bbox_2d": [554, 663, 618, 673], "page": 1},
 {"key": "land_prices.5.price", "value": "12,017,000", "bbox_2d": [637, 663, 702, 673], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [437, 751, 563, 764], "page": 1}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [647, 762, 736, 825], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check land_register` → `python -m docgen.formdir card land_register` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions land_register --show` · `python -m docgen.preview land_register --out work/land_register`
