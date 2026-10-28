# 주민등록표 등본 (`resident_registration_copy`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card resident_registration_copy · card-hash: 9268d0578050 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** family · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 주민등록표 등본 (다른 이름: 주민등록표(등본))
- **쓰이는 업무:** 주택담보대출, 전세자금대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 주민등록표 등본 (세대 전체). 부모·형제 동거, 세대주 변경, 동거인, 과거 주소 변동 포함 발급 등.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/family.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 25칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `doc_no` | 발급번호 / 문서확인번호 | text | 1쪽 [150, 73, 216, 84] | 늘 | generate.py | - | 묻기 |
| `officer` | 담당자 | text | 1쪽 [178, 186, 229, 199] | 8/16 | generate.py | - | 묻기 |
| `officer_phone` | 전화 | phone | 1쪽 [294, 186, 390, 199] | 8/16 | generate.py | - | 묻기 |
| `applicant` | 신청인 | text | 1쪽 [187, 205, 255, 218] | 늘 | generate.py | - | 묻기 |
| `purpose` | 용도및목적 | text | 1쪽 [388, 205, 457, 218] | 늘 | generate.py | - | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [780, 225, 919, 238] | 늘 | generate.py | - | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [504, 247, 846, 266] | 늘 | generate.py | - | 묻기 |
| `household_head.name` | 세대주성명 | text | 1쪽 [254, 305, 323, 319] | 늘 | generate.py | look/template.html.j2:11 | 묻기 |
| `household_head.name_hanja` | 세대주성명(한자) | text | 1쪽 [333, 305, 401, 319] | 늘 | generate.py | look/template.html.j2:11 | 묻기 |
| `household_formed.reason` | 세대구성사유 | text | 1쪽 [760, 296, 863, 310] | 늘 | generate.py | look/template.html.j2:12 | 묻기 |
| `household_formed.date` | 세대구성일자 | date | 1쪽 [772, 314, 852, 327] | 늘 | generate.py | look/template.html.j2:12 | 묻기 |
| `past_addresses.*.no` | 번호 | number | 1쪽 [119, 376, 127, 389] (1행) | 7/16 | generate.py | look/template.html.j2:18 | 묻기 |
| `past_addresses.*.address` | 주소 | text | 1쪽 [174, 367, 610, 398] (1행) | 7/16 | generate.py | look/template.html.j2:18 | 묻기 |
| `past_addresses.*.moved_in` | 전입일/변동일 | date | 1쪽 [679, 376, 758, 389] (1행) | 7/16 | generate.py | look/template.html.j2:18 | 묻기 |
| `past_addresses.*.reason` | 변동사유 | text | 1쪽 [849, 376, 883, 389] (1행) | 7/16 | generate.py | look/template.html.j2:18 | 묻기 |
| `customer.address` ← `current_address.address` | 현주소 | text | 1쪽 [174, 410, 612, 441] | 늘 | generate.py | look/template.html.j2:20 | 묻기 |
| `current_address.moved_in` | 전입일/변동일 | date | 1쪽 [679, 419, 758, 432] | 늘 | generate.py | look/template.html.j2:20 | 묻기 |
| `current_address.reason` | 변동사유 | text | 1쪽 [849, 419, 883, 432] | 늘 | generate.py | look/template.html.j2:20 | 묻기 |
| `members.*.no` | 번호 | number | 1쪽 [106, 527, 114, 540] (1행) | 늘 | generate.py | look/template.html.j2:28 | 묻기 |
| `members.*.relation` | 세대주관계 | text | 1쪽 [172, 527, 207, 540] (1행) | 늘 | generate.py | look/template.html.j2:29 | 묻기 |
| `members.*.name` | 성명 | text | 1쪽 [356, 515, 424, 528] (1행) | 늘 | generate.py | look/template.html.j2:30 | 묻기 |
| `members.*.name_hanja` | 한자 | text | 1쪽 [434, 515, 503, 528] (1행) | 늘 | generate.py | look/template.html.j2:30 | 묻기 |
| `members.*.moved_in` | 전입일/변동일 | date | 1쪽 [679, 527, 758, 540] (1행) | 늘 | generate.py | look/template.html.j2:31 | 묻기 |
| `members.*.reason` | 변동사유 | text | 1쪽 [849, 527, 883, 540] (1행) | 늘 | generate.py | look/template.html.j2:32 | 묻기 |
| `members.*.rrn` | 주민등록번호 | rrn | 1쪽 [373, 539, 490, 552] (1행) | 늘 | generate.py | look/template.html.j2:34 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [877, 237, 967, 301] | 늘 | generate.py | - | 묻기 |

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
"주민등록표 등본"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "제 5273 호",
 "박민아",
 "02-1607-2011",
 "남궁예태",
 "대출신청",
 "2025년 04월 01일",
 "서울특별시 서초구 반포동장",
 "南宮叡兌",
 "전입세대구성",
 "2024-02-15",
 "1",
 "대전광역시 유성구 유성대로 96, 113동 1304호 (봉명동, e편한세상아파트)",
 "2018-02-14",
 "전입",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "본인",
 "850328-2******"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"본인"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2024-02-15"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- doc_no: 발급번호
- officer: 담당자
- officer_phone: 전화
- applicant: 신청인
- purpose: 용도및목적
- issue_date: 발급일
- issuer: 발급기관
- household_head.name: 세대주성명
- household_head.name_hanja: 세대주성명(한자)
- household_formed.reason: 세대구성사유
- household_formed.date: 세대구성일자
- past_addresses.0.no: 번호 (1행)
- past_addresses.0.address: 주소 (1행)
- past_addresses.0.moved_in: 전입일/변동일 (1행)
- past_addresses.0.reason: 변동사유 (1행)
- customer.address: 현주소 (고객 주소)
- current_address.moved_in: 전입일/변동일 (같은 항목명 중 2번째 칸)
- current_address.reason: 변동사유 (같은 항목명 중 2번째 칸)
- members.0.no: 번호 (1행)
- members.0.relation: 세대주관계 (1행)
- members.0.name: 성명 (1행)
- members.0.name_hanja: 한자 (1행)
- members.0.moved_in: 전입일/변동일 (1행)
- members.0.reason: 변동사유 (1행)
- members.0.rrn: 주민등록번호 (1행)
```

답:

```json
[{"key": "doc_no", "value": "제 5273 호", "bbox_2d": [150, 73, 216, 84], "page": 1},
 {"key": "officer", "value": "박민아", "bbox_2d": [178, 186, 229, 199], "page": 1},
 {"key": "officer_phone", "value": "02-1607-2011", "bbox_2d": [294, 186, 390, 199], "page": 1},
 {"key": "applicant", "value": "남궁예태", "bbox_2d": [187, 205, 255, 218], "page": 1},
 {"key": "purpose", "value": "대출신청", "bbox_2d": [388, 205, 457, 218], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [780, 225, 919, 238], "page": 1},
 {"key": "issuer", "value": "서울특별시 서초구 반포동장", "bbox_2d": [504, 247, 846, 266], "page": 1},
 {"key": "household_head.name", "value": "남궁예태", "bbox_2d": [254, 305, 323, 319], "page": 1},
 {"key": "household_head.name_hanja", "value": "南宮叡兌", "bbox_2d": [333, 305, 401, 319], "page": 1},
 {"key": "household_formed.reason", "value": "전입세대구성", "bbox_2d": [760, 296, 863, 310], "page": 1},
 {"key": "household_formed.date", "value": "2024-02-15", "bbox_2d": [772, 314, 852, 327], "page": 1},
 {"key": "past_addresses.0.no", "value": "1", "bbox_2d": [119, 376, 127, 389], "page": 1},
 {"key": "past_addresses.0.address", "value": "대전광역시 유성구 유성대로 96, 113동 1304호 (봉명동, e편한세상아파트)", "bbox_2d": [174, 367, 610, 398], "page": 1},
 {"key": "past_addresses.0.moved_in", "value": "2018-02-14", "bbox_2d": [679, 376, 758, 389], "page": 1},
 {"key": "past_addresses.0.reason", "value": "전입", "bbox_2d": [849, 376, 883, 389], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [174, 410, 612, 441], "page": 1},
 {"key": "current_address.moved_in", "value": "2024-02-15", "bbox_2d": [679, 419, 758, 432], "page": 1},
 {"key": "current_address.reason", "value": "전입", "bbox_2d": [849, 419, 883, 432], "page": 1},
 {"key": "members.0.no", "value": "1", "bbox_2d": [106, 527, 114, 540], "page": 1},
 {"key": "members.0.relation", "value": "본인", "bbox_2d": [172, 527, 207, 540], "page": 1},
 {"key": "members.0.name", "value": "남궁예태", "bbox_2d": [356, 515, 424, 528], "page": 1},
 {"key": "members.0.name_hanja", "value": "南宮叡兌", "bbox_2d": [434, 515, 503, 528], "page": 1},
 {"key": "members.0.moved_in", "value": "2024-02-15", "bbox_2d": [679, 527, 758, 540], "page": 1},
 {"key": "members.0.reason", "value": "전입", "bbox_2d": [849, 527, 883, 540], "page": 1},
 {"key": "members.0.rrn", "value": "850328-2******", "bbox_2d": [373, 539, 490, 552], "page": 1}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [877, 237, 967, 301], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions resident_registration_copy --show` · `python -m docgen.preview resident_registration_copy --out work/resident_registration_copy`
