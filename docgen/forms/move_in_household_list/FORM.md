# 전입세대확인서 (`move_in_household_list`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card move_in_household_list · card-hash: f53e12eba764 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** real_estate · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 전입세대확인서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 전입세대확인서(열람). 해당 주소에 전입신고된 세대주 목록.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/real_estate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 24칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `issue_no` | 발급번호 | text | 1쪽 [173, 62, 326, 75] | 늘 | generate.py | look/template.html.j2:15 | 묻기 |
| `issue_date` | 발급일자 | date | 1쪽 [603, 62, 679, 75] | 늘 | generate.py | look/template.html.j2:15 | 묻기 |
| `kind` | 열람·교부구분 | text | 1쪽 [483, 126, 517, 139] | 늘 | generate.py | look/template.html.j2:17 | 묻기 |
| `address` | 건물또는시설소재지 | text | 1쪽 [261, 169, 846, 182] | 늘 | generate.py | look/template.html.j2:20 | 묻기 |
| `jibun_address` | 지번주소 | text | 1쪽 [304, 188, 582, 199] | 늘 | generate.py | look/template.html.j2:20 | 묻기 |
| `households.*.no` | 순번 | number | 1쪽 [86, 300, 94, 313] (1행) | 늘 | generate.py | - | 묻기 |
| `households.*.head_name` | 세대주성명 | text | 1쪽 [144, 300, 195, 313] (1행) | 늘 | generate.py | - | 묻기 |
| `households.*.move_in_date` | 전입일자 | date | 1쪽 [256, 300, 336, 313] (1행) | 늘 | generate.py | - | 묻기 |
| `households.*.reg_type` | 등록구분 | text | 1쪽 [404, 300, 455, 313] (1행) | 늘 | generate.py | - | 묻기 |
| `households.*.first_name` | 최초전입자성명 | text | 1쪽 [516, 300, 567, 313] (1행) | 늘 | generate.py | - | 묻기 |
| `households.*.first_date` | 최초전입일자 | date | 1쪽 [628, 300, 707, 313] (1행) | 늘 | generate.py | - | 묻기 |
| `households.*.first_reg_type` | 최초전입자등록구분 | text | 1쪽 [775, 300, 826, 313] (1행) | 늘 | generate.py | - | 묻기 |
| `households.*.cohabitants` | 동거인수 | number | 1쪽 [895, 300, 903, 313] (1행) | 늘 | generate.py | - | 묻기 |
| `customer.name` ← `applicant.name` | 성명 | text | 1쪽 [211, 526, 279, 540] | 늘 | generate.py | look/template.html.j2:57 | 묻기 |
| `customer.rrn` ← `applicant.rrn` | 주민등록번호 | rrn | 1쪽 [585, 526, 701, 540] | 늘 | generate.py | look/template.html.j2:57 | 묻기 |
| `customer.address` ← `applicant.address` | 주소 | text | 1쪽 [211, 553, 796, 566] | 늘 | generate.py | look/template.html.j2:57 | 묻기 |
| `applicant.purpose` | 열람·교부목적 | text | 1쪽 [211, 580, 431, 593] | 늘 | generate.py | look/template.html.j2:58 | 묻기 |
| `view_date` | 발급일 | date | 1쪽 [431, 674, 569, 687] | 늘 | generate.py | look/template.html.j2:61 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [369, 708, 608, 729] | 늘 | generate.py | look/template.html.j2:60 | 묻기 |
| `cohabitants.*.no` | 순번 | - | - (1행) | 3/16 | generate.py | - | 묻기 |
| `cohabitants.*.name` | 동거인성명 | - | - (1행) | 3/16 | generate.py | - | 묻기 |
| `cohabitants.*.move_in_date` | 전입일자 | - | - (1행) | 3/16 | generate.py | - | 묻기 |
| `cohabitants.*.reg_type` | 등록구분 | - | - (1행) | 3/16 | generate.py | - | 묻기 |
| `households.*.unit` | 동·호 | - | - (1행) | 2/16 | generate.py | - | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [596, 686, 686, 749] | 늘 | generate.py | - | 묻기 |

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
"전입세대확인서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "0070-4308-7209-9884",
 "2025.04.01",
 "교부",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "서울특별시 서초구 반포동 661 103동 1301호",
 "1",
 "남**태",
 "2025-03-10",
 "거주자",
 "0",
 "남궁예태",
 "850328-2******",
 "금융기관 대출(주택담보대출)",
 "2025년 04월 01일",
 "서초구 반포동장"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"2025.04.01"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"남**태"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- issue_no: 발급번호
- issue_date: 발급일자
- kind: 열람·교부구분
- address: 건물또는시설소재지
- jibun_address: 지번주소
- households.0.no: 순번 (1행)
- households.0.head_name: 세대주성명 (1행)
- households.0.move_in_date: 전입일자 (1행)
- households.0.reg_type: 등록구분 (1행)
- households.0.first_name: 최초전입자성명 (1행)
- households.0.first_date: 최초전입일자 (1행)
- households.0.first_reg_type: 최초전입자등록구분 (1행)
- households.0.cohabitants: 동거인수 (1행)
- customer.name: 성명 (고객 성명)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- customer.address: 주소 (고객 주소)
- applicant.purpose: 열람·교부목적
- view_date: 발급일
- issuer: 발급기관
```

답:

```json
[{"key": "issue_no", "value": "0070-4308-7209-9884", "bbox_2d": [173, 62, 326, 75], "page": 1},
 {"key": "issue_date", "value": "2025.04.01", "bbox_2d": [603, 62, 679, 75], "page": 1},
 {"key": "kind", "value": "교부", "bbox_2d": [483, 126, 517, 139], "page": 1},
 {"key": "address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [261, 169, 846, 182], "page": 1},
 {"key": "jibun_address", "value": "서울특별시 서초구 반포동 661 103동 1301호", "bbox_2d": [304, 188, 582, 199], "page": 1},
 {"key": "households.0.no", "value": "1", "bbox_2d": [86, 300, 94, 313], "page": 1},
 {"key": "households.0.head_name", "value": "남**태", "bbox_2d": [144, 300, 195, 313], "page": 1},
 {"key": "households.0.move_in_date", "value": "2025-03-10", "bbox_2d": [256, 300, 336, 313], "page": 1},
 {"key": "households.0.reg_type", "value": "거주자", "bbox_2d": [404, 300, 455, 313], "page": 1},
 {"key": "households.0.first_name", "value": "남**태", "bbox_2d": [516, 300, 567, 313], "page": 1},
 {"key": "households.0.first_date", "value": "2025-03-10", "bbox_2d": [628, 300, 707, 313], "page": 1},
 {"key": "households.0.first_reg_type", "value": "거주자", "bbox_2d": [775, 300, 826, 313], "page": 1},
 {"key": "households.0.cohabitants", "value": "0", "bbox_2d": [895, 300, 903, 313], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [211, 526, 279, 540], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [585, 526, 701, 540], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [211, 553, 796, 566], "page": 1},
 {"key": "applicant.purpose", "value": "금융기관 대출(주택담보대출)", "bbox_2d": [211, 580, 431, 593], "page": 1},
 {"key": "view_date", "value": "2025년 04월 01일", "bbox_2d": [431, 674, 569, 687], "page": 1},
 {"key": "issuer", "value": "서초구 반포동장", "bbox_2d": [369, 708, 608, 729], "page": 1}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [596, 686, 686, 749], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions move_in_household_list --show` · `python -m docgen.preview move_in_household_list --out work/move_in_household_list`
