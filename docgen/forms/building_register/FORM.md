# 집합건축물대장(전유부) (`building_register`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card building_register · card-hash: e8e76a43d50c -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** real_estate · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 집합건축물대장(전유부) (다른 이름: 집합건축물대장(전유부, 갑))
- **쓰이는 업무:** 주택담보대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 집합건축물대장(전유부, 갑) 등본.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/real_estate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 30칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `confirm_no` | 문서확인번호 | text | 1쪽 [99, 54, 188, 70] | 늘 | 템플릿 | generate.py | look/template.html.j2:89 · fields.json:10 | 묻기 |
| `unique_no` | 고유번호 | text | 1쪽 [98, 130, 211, 148] | 늘 | 템플릿 | generate.py | look/template.html.j2:97 · fields.json:60 | 묻기 |
| `building_name` | 명칭 | text | 1쪽 [351, 130, 499, 148] | 늘 | 템플릿 | generate.py | look/template.html.j2:97 · fields.json:5 | 묻기 |
| `unit_name` | 호명칭 | text | 1쪽 [868, 130, 932, 148] | 늘 | 템플릿 | generate.py | look/template.html.j2:97 · fields.json:65 | 묻기 |
| `site_location` | 대지위치 | text | 1쪽 [98, 168, 226, 186] | 늘 | 템플릿 | generate.py | look/template.html.j2:101 · fields.json:55 | 묻기 |
| `jibun` | 지번 | number | 1쪽 [351, 168, 368, 186] | 늘 | 템플릿 | generate.py | look/template.html.j2:101 · fields.json:25 | 묻기 |
| `road_address` | 도로명주소 | text | 1쪽 [538, 168, 697, 186] | 늘 | 템플릿 | generate.py | look/template.html.j2:101 · fields.json:45 | 묻기 |
| `exclusive.*.kind` | 구분 | text | 1쪽 [54, 275, 65, 293] (1행) | 늘 | 템플릿 | generate.py | fields.json:120 | 묻기 |
| `exclusive.*.floor` | 층별 | text | 1쪽 [124, 275, 146, 293] (1행) | 늘 | 템플릿 | generate.py | fields.json:115 | 묻기 |
| `exclusive.*.structure` | 구조 | text | 1쪽 [262, 275, 374, 293] (1행) | 늘 | 템플릿 | generate.py | fields.json:125 | 묻기 |
| `exclusive.*.usage` | 용도 | text | 1쪽 [630, 275, 664, 293] (1행) | 늘 | 템플릿 | generate.py | fields.json:130 | 묻기 |
| `exclusive.*.area` | 면적(㎡) | number | 1쪽 [937, 275, 962, 293] (1행) | 늘 | 템플릿 | generate.py | fields.json:110 | 묻기 |
| `common.*.kind` | 구분 | text | 1쪽 [54, 417, 65, 435] (1행) | 늘 | 템플릿 | generate.py | fields.json:90 | 묻기 |
| `common.*.floor` | 층별 | text | 1쪽 [124, 417, 146, 435] (1행) | 늘 | 템플릿 | generate.py | fields.json:85 | 묻기 |
| `common.*.structure` | 구조 | text | 1쪽 [262, 417, 374, 435] (1행) | 늘 | 템플릿 | generate.py | fields.json:95 | 묻기 |
| `common.*.usage` | 용도 | text | 1쪽 [600, 417, 694, 435] (1행) | 늘 | 템플릿 | generate.py | fields.json:100 | 묻기 |
| `common.*.area` | 면적(㎡) | number | 1쪽 [937, 417, 962, 435] (1행) | 늘 | 템플릿 | generate.py | fields.json:80 | 묻기 |
| `owners.*.name` | 성명(명칭) | text | 1쪽 [41, 665, 141, 704] (1행) | 늘 | 템플릿 | generate.py | fields.json:170 | 묻기 |
| `owners.*.rrn` | 주민(법인)등록번호 | rrn | 1쪽 [54, 708, 128, 725] (1행) | 늘 | 템플릿 | generate.py | fields.json:175 | 묻기 |
| `owners.*.address` | 주소 | text | 1쪽 [154, 687, 296, 704] (1행) | 늘 | 템플릿 | generate.py | fields.json:155 | 묻기 |
| `owners.*.share` | 소유권지분 | text | 1쪽 [854, 687, 868, 704] (1행) | 늘 | 템플릿 | generate.py | fields.json:180 | 묻기 |
| `owners.*.change_date` | 변동일 | date | 1쪽 [901, 676, 951, 694] (1행) | 늘 | 템플릿 | generate.py | fields.json:165 | 묻기 |
| `owners.*.change_cause` | 변동원인 | text | 1쪽 [898, 697, 954, 715] (1행) | 늘 | 템플릿 | generate.py | fields.json:160 | 묻기 |
| `house_prices.*.base_date` | 기준일 | date | 2쪽 [195, 313, 245, 330] (1행) | 14/16 | 템플릿 | generate.py | fields.json:140 | 묻기 |
| `house_prices.*.price` | 공동주택(아파트)가격 | amount | 2쪽 [898, 313, 962, 330] (1행) | 14/16 | 템플릿 | generate.py | fields.json:145 | 묻기 |
| `officer` | 담당자 | text | 2쪽 [66, 535, 110, 548] | 늘 | 템플릿 | generate.py | look/template.html.j2:124 · fields.json:30 | 묻기 |
| `officer_phone` | 전화 | phone | 2쪽 [144, 535, 194, 548] | 늘 | 템플릿 | generate.py | look/template.html.j2:124 · fields.json:35 | 묻기 |
| `issue_date` | 발급일 | date | 2쪽 [499, 500, 583, 517] | 늘 | 템플릿 | generate.py | look/template.html.j2:125 · fields.json:15 | 묻기 |
| `issuer` | 발급기관 | text | 2쪽 [415, 522, 605, 547] | 늘 | 템플릿 | generate.py | look/template.html.j2:126 · fields.json:20 | 묻기 |
| `owners_note` | 비고 | - | - | 5/16 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:40 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 2쪽 [597, 490, 660, 580] | 늘 | 템플릿 | generate.py | fields.json:50 | 묻기 |

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
"집합건축물대장(전유부)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "7935-4470-6001-8620",
 "1144612000-3-06610000",
 "힐스테이트2차아파트 제103동",
 "103동 1301호",
 "서울특별시 서초구 반포동",
 "661",
 "서울특별시 서초구 강남대로 357",
 "주",
 "13층",
 "철근콘크리트벽식구조",
 "아파트",
 "74.95",
 "각층",
 "계단실,복도,승강기",
 "13.84",
 "지1층",
 "주차장",
 "22.40",
 "기계실,전기실",
 "3.17",
 "주식회사한양종합건설",
 "131111-2362356",
 "서울특별시 서초구 시청로 60",
 "1/1",
 "1993.06.28",
 "소유권보존",
 "임채영",
 "501031-2******",
 "서울특별시 노원구 노원로 459-15, 116동 2102호 (중계동, SK뷰리버뷰아파트)",
 "2004.02.17",
 "소유권이전",
 "하나자산신탁주식회사",
 "135011-8178151",
 "서울특별시 강남구 테헤란로 132",
 "2022.06.03",
 "2023.10.23",
 "남궁예태",
 "850328-2******",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "2025.03.02",
 "2024.01.01",
 "1,125,000,000",
 "2023.01.01",
 "1,042,000,000",
 "2022.01.01",
 "955,000,000",
 "민원여권과",
 "02-3472-2780",
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
"남궁예태"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2023.01.01"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- unit_name: 호명칭
- jibun: 지번
- exclusive.0.kind: 구분 (1행)
- exclusive.0.floor: 층별 (1행)
- exclusive.0.structure: 구조 (1행)
- exclusive.0.usage: 용도 (1행)
- common.0.kind: 구분 (1행)
- common.0.floor: 층별 (1행)
- common.0.usage: 용도 (1행)
- common.1.structure: 구조 (2행)
- common.1.usage: 용도 (2행)
- common.1.area: 면적(㎡) (2행)
- common.2.kind: 구분 (3행)
- common.2.floor: 층별 (3행)
- common.2.usage: 용도 (3행)
- common.2.area: 면적(㎡) (3행)
- owners.0.name: 성명(명칭) (1행)
- owners.0.rrn: 주민(법인)등록번호 (1행)
- owners.0.address: 주소 (1행)
- owners.0.change_date: 변동일 (1행)
- owners.0.change_cause: 변동원인 (1행)
- owners.1.name: 성명(명칭) (2행)
- owners.1.rrn: 주민(법인)등록번호 (2행)
- owners.1.share: 소유권지분 (2행)
- owners.2.name: 성명(명칭) (3행)
- owners.2.address: 주소 (3행)
- owners.2.share: 소유권지분 (3행)
- owners.2.change_date: 변동일 (3행)
- owners.3.name: 성명(명칭) (4행)
- owners.3.rrn: 주민(법인)등록번호 (4행)
- owners.3.address: 주소 (4행)
- owners.3.share: 소유권지분 (4행)
- owners.4.address: 주소 (5행)
- owners.4.share: 소유권지분 (5행)
- house_prices.0.base_date: 기준일 (1행)
- house_prices.1.price: 공동주택(아파트)가격 (2행)
- house_prices.2.price: 공동주택(아파트)가격 (3행)
- officer: 담당자
- issue_date: 발급일
- issuer: 발급기관
```

답:

```json
[{"key": "unit_name", "value": "103동 1301호", "bbox_2d": [868, 130, 932, 148], "page": 1},
 {"key": "jibun", "value": "661", "bbox_2d": [351, 168, 368, 186], "page": 1},
 {"key": "exclusive.0.kind", "value": "주", "bbox_2d": [54, 275, 65, 293], "page": 1},
 {"key": "exclusive.0.floor", "value": "13층", "bbox_2d": [124, 275, 146, 293], "page": 1},
 {"key": "exclusive.0.structure", "value": "철근콘크리트벽식구조", "bbox_2d": [262, 275, 374, 293], "page": 1},
 {"key": "exclusive.0.usage", "value": "아파트", "bbox_2d": [630, 275, 664, 293], "page": 1},
 {"key": "common.0.kind", "value": "주", "bbox_2d": [54, 417, 65, 435], "page": 1},
 {"key": "common.0.floor", "value": "각층", "bbox_2d": [124, 417, 146, 435], "page": 1},
 {"key": "common.0.usage", "value": "계단실,복도,승강기", "bbox_2d": [600, 417, 694, 435], "page": 1},
 {"key": "common.1.structure", "value": "철근콘크리트벽식구조", "bbox_2d": [262, 452, 374, 470], "page": 1},
 {"key": "common.1.usage", "value": "주차장", "bbox_2d": [630, 452, 664, 470], "page": 1},
 {"key": "common.1.area", "value": "22.40", "bbox_2d": [937, 452, 962, 470], "page": 1},
 {"key": "common.2.kind", "value": "주", "bbox_2d": [54, 487, 65, 505], "page": 1},
 {"key": "common.2.floor", "value": "지1층", "bbox_2d": [121, 487, 149, 505], "page": 1},
 {"key": "common.2.usage", "value": "기계실,전기실", "bbox_2d": [612, 487, 682, 505], "page": 1},
 {"key": "common.2.area", "value": "3.17", "bbox_2d": [942, 487, 962, 505], "page": 1},
 {"key": "owners.0.name", "value": "주식회사한양종합건설", "bbox_2d": [41, 665, 141, 704], "page": 1},
 {"key": "owners.0.rrn", "value": "131111-2362356", "bbox_2d": [54, 708, 128, 725], "page": 1},
 {"key": "owners.0.address", "value": "서울특별시 서초구 시청로 60", "bbox_2d": [154, 687, 296, 704], "page": 1},
 {"key": "owners.0.change_date", "value": "1993.06.28", "bbox_2d": [901, 676, 951, 694], "page": 1},
 {"key": "owners.0.change_cause", "value": "소유권보존", "bbox_2d": [898, 697, 954, 715], "page": 1},
 {"key": "owners.1.name", "value": "임채영", "bbox_2d": [74, 743, 108, 761], "page": 1},
 {"key": "owners.1.rrn", "value": "501031-2******", "bbox_2d": [53, 764, 129, 782], "page": 1},
 {"key": "owners.1.share", "value": "1/1", "bbox_2d": [854, 754, 868, 771], "page": 1},
 {"key": "owners.2.name", "value": "하나자산신탁주식회사", "bbox_2d": [41, 799, 141, 838], "page": 1},
 {"key": "owners.2.address", "value": "서울특별시 강남구 테헤란로 132", "bbox_2d": [154, 821, 312, 838], "page": 1},
 {"key": "owners.2.share", "value": "1/1", "bbox_2d": [854, 821, 868, 838], "page": 1},
 {"key": "owners.2.change_date", "value": "2022.06.03", "bbox_2d": [901, 810, 951, 828], "page": 1},
 {"key": "owners.3.name", "value": "임채영", "bbox_2d": [74, 877, 108, 895], "page": 1},
 {"key": "owners.3.rrn", "value": "501031-2******", "bbox_2d": [53, 898, 129, 916], "page": 1},
 {"key": "owners.3.address", "value": "서울특별시 노원구 노원로 459-15, 116동 2102호 (중계동, SK뷰리버뷰아파트)", "bbox_2d": [154, 888, 526, 905], "page": 1},
 {"key": "owners.3.share", "value": "1/1", "bbox_2d": [854, 888, 868, 905], "page": 1},
 {"key": "owners.4.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [192, 160, 575, 178], "page": 2},
 {"key": "owners.4.share", "value": "1/1", "bbox_2d": [827, 160, 841, 178], "page": 2},
 {"key": "house_prices.0.base_date", "value": "2024.01.01", "bbox_2d": [195, 313, 245, 330], "page": 2},
 {"key": "house_prices.1.price", "value": "1,042,000,000", "bbox_2d": [898, 348, 962, 365], "page": 2},
 {"key": "house_prices.2.price", "value": "955,000,000", "bbox_2d": [906, 383, 962, 401], "page": 2},
 {"key": "officer", "value": "민원여권과", "bbox_2d": [66, 535, 110, 548], "page": 2},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [499, 500, 583, 517], "page": 2},
 {"key": "issuer", "value": "서울특별시 서초구청장", "bbox_2d": [415, 522, 605, 547], "page": 2}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [597, 490, 660, 580], "page": 2}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check building_register` → `python -m docgen.formdir card building_register` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions building_register --show` · `python -m docgen.preview building_register --out work/building_register`
