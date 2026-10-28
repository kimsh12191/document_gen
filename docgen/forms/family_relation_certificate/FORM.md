# 가족관계증명서 (`family_relation_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card family_relation_certificate · card-hash: b3f4d42dd317 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** family · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 가족관계증명서
- **쓰이는 업무:** 주택담보대출, 유학생 송금, 상속예금 지급
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 가족관계증명서 (일반/상세). 사망한 부모, 전혼 자녀, 입양(친생부모) 등.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/family.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 24칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `cert_type` | 증명서종류 | text | 1쪽 [588, 84, 659, 108] | 늘 | generate.py | look/template.html.j2:6 | 묻기 |
| `reg_base` | 등록기준지 | text | 1쪽 [230, 141, 426, 153] | 늘 | generate.py | look/template.html.j2:7 | 묻기 |
| `customer.relation` ← `self.relation` | 구분 | text | 1쪽 [108, 221, 138, 233] | 늘 | generate.py | - | 묻기 |
| `customer.name` ← `self.name` | 성명 | text | 1쪽 [208, 221, 269, 233] | 늘 | generate.py | - | 묻기 |
| `customer.name_hanja` ← `self.name_hanja` | 성명(한자) | text | 1쪽 [274, 221, 335, 233] | 늘 | generate.py | - | 묻기 |
| `customer.birth` ← `self.birth` | 출생연월일 | date | 1쪽 [412, 221, 526, 233] | 늘 | generate.py | - | 묻기 |
| `customer.rrn` ← `self.rrn` | 주민등록번호 | rrn | 1쪽 [614, 221, 718, 233] | 늘 | generate.py | - | 묻기 |
| `customer.gender` ← `self.gender` | 성별 | text | 1쪽 [799, 221, 814, 233] | 늘 | generate.py | - | 묻기 |
| `customer.bon` ← `self.bon` | 본 | text | 1쪽 [864, 221, 895, 233] | 늘 | generate.py | - | 묻기 |
| `family.*.relation` | 구분 | text | 1쪽 [115, 319, 130, 332] (1행) | 늘 | generate.py | - | 묻기 |
| `family.*.name` | 성명 | text | 1쪽 [208, 319, 269, 332] (1행) | 늘 | generate.py | - | 묻기 |
| `family.*.name_hanja` | 성명(한자) | text | 1쪽 [274, 319, 335, 332] (1행) | 늘 | generate.py | - | 묻기 |
| `family.*.birth` | 출생연월일 | date | 1쪽 [412, 319, 526, 332] (1행) | 늘 | generate.py | - | 묻기 |
| `family.*.rrn` | 주민등록번호 | rrn | 1쪽 [614, 319, 718, 332] (1행) | 늘 | generate.py | - | 묻기 |
| `family.*.gender` | 성별 | text | 1쪽 [799, 319, 814, 332] (1행) | 늘 | generate.py | - | 묻기 |
| `family.*.bon` | 본 | text | 1쪽 [864, 319, 895, 332] (1행) | 늘 | generate.py | - | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [438, 446, 562, 459] | 늘 | generate.py | - | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [257, 481, 721, 497] | 늘 | generate.py | - | 묻기 |
| `issue_time` | 발급시각 | text | 1쪽 [191, 527, 251, 537] | 늘 | generate.py | - | 묻기 |
| `applicant` | 신청인 | text | 1쪽 [191, 543, 247, 554] | 늘 | generate.py | - | 묻기 |
| `doc_check_no` | 문서확인번호 | text | 1쪽 [160, 945, 269, 955] | 4/16 | generate.py | - | 묻기 |
| `officer` | 발급담당자 | - | - | 12/16 | generate.py | - | 묻기 |
| `officer_phone` | 전화 | - | - | 12/16 | generate.py | - | 묻기 |
| `family.*.status` | 사망 | - | - (1행) | 2/16 | generate.py | - | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [708, 459, 798, 522] | 늘 | generate.py | - | 묻기 |

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
"가족관계증명서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "일반",
 "세종특별자치시 도담동 550-8",
 "본인",
 "남궁예태",
 "南宮叡兌",
 "1985년 03월 28일",
 "850328-2489940",
 "여",
 "咸悅",
 "부",
 "남궁찬윤",
 "南宮讚允",
 "1952년 10월 28일",
 "521028-1401146",
 "남",
 "모",
 "방옥주",
 "方玉宙",
 "1953년 03월 28일",
 "530328-2814528",
 "溫陽",
 "2025년 04월 01일",
 "법원행정처 전산정보중앙관리소 전산운영책임관",
 "06시 41분",
 "9745-8227-1390-2186"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"1952년 10월 28일"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"06시 41분"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- cert_type: 증명서종류
- reg_base: 등록기준지
- customer.relation: 구분 (고객 관계, 같은 항목명 중 1번째 칸)
- customer.name: 성명 (고객 성명, 같은 항목명 중 1번째 칸)
- customer.name_hanja: 성명(한자) (고객 한자 성명, 같은 항목명 중 1번째 칸)
- customer.birth: 출생연월일 (고객 생년월일, 같은 항목명 중 1번째 칸)
- customer.rrn: 주민등록번호 (고객 주민등록번호, 같은 항목명 중 1번째 칸)
- customer.gender: 성별 (고객 성별, 같은 항목명 중 1번째 칸)
- customer.bon: 본 (고객 본관, 같은 항목명 중 1번째 칸)
- family.0.relation: 구분 (1행)
- family.0.name: 성명 (1행)
- family.0.name_hanja: 성명(한자) (1행)
- family.0.birth: 출생연월일 (1행)
- family.0.rrn: 주민등록번호 (1행)
- family.0.gender: 성별 (1행)
- family.0.bon: 본 (1행)
- family.1.relation: 구분 (2행)
- family.1.name: 성명 (2행)
- family.1.name_hanja: 성명(한자) (2행)
- family.1.birth: 출생연월일 (2행)
- family.1.rrn: 주민등록번호 (2행)
- family.1.gender: 성별 (2행)
- family.1.bon: 본 (2행)
- issue_date: 발급일
- issuer: 발급기관
- issue_time: 발급시각
- applicant: 신청인
- doc_check_no: 문서확인번호
```

답:

```json
[{"key": "cert_type", "value": "일반", "bbox_2d": [588, 84, 659, 108], "page": 1},
 {"key": "reg_base", "value": "세종특별자치시 도담동 550-8", "bbox_2d": [230, 141, 426, 153], "page": 1},
 {"key": "customer.relation", "value": "본인", "bbox_2d": [108, 221, 138, 233], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [208, 221, 269, 233], "page": 1},
 {"key": "customer.name_hanja", "value": "南宮叡兌", "bbox_2d": [274, 221, 335, 233], "page": 1},
 {"key": "customer.birth", "value": "1985년 03월 28일", "bbox_2d": [412, 221, 526, 233], "page": 1},
 {"key": "customer.rrn", "value": "850328-2489940", "bbox_2d": [614, 221, 718, 233], "page": 1},
 {"key": "customer.gender", "value": "여", "bbox_2d": [799, 221, 814, 233], "page": 1},
 {"key": "customer.bon", "value": "咸悅", "bbox_2d": [864, 221, 895, 233], "page": 1},
 {"key": "family.0.relation", "value": "부", "bbox_2d": [115, 319, 130, 332], "page": 1},
 {"key": "family.0.name", "value": "남궁찬윤", "bbox_2d": [208, 319, 269, 332], "page": 1},
 {"key": "family.0.name_hanja", "value": "南宮讚允", "bbox_2d": [274, 319, 335, 332], "page": 1},
 {"key": "family.0.birth", "value": "1952년 10월 28일", "bbox_2d": [412, 319, 526, 332], "page": 1},
 {"key": "family.0.rrn", "value": "521028-1401146", "bbox_2d": [614, 319, 718, 332], "page": 1},
 {"key": "family.0.gender", "value": "남", "bbox_2d": [799, 319, 814, 332], "page": 1},
 {"key": "family.0.bon", "value": "咸悅", "bbox_2d": [864, 319, 895, 332], "page": 1},
 {"key": "family.1.relation", "value": "모", "bbox_2d": [115, 350, 130, 363], "page": 1},
 {"key": "family.1.name", "value": "방옥주", "bbox_2d": [223, 350, 269, 363], "page": 1},
 {"key": "family.1.name_hanja", "value": "方玉宙", "bbox_2d": [274, 350, 320, 363], "page": 1},
 {"key": "family.1.birth", "value": "1953년 03월 28일", "bbox_2d": [412, 350, 526, 363], "page": 1},
 {"key": "family.1.rrn", "value": "530328-2814528", "bbox_2d": [614, 350, 718, 363], "page": 1},
 {"key": "family.1.gender", "value": "여", "bbox_2d": [799, 350, 814, 363], "page": 1},
 {"key": "family.1.bon", "value": "溫陽", "bbox_2d": [864, 350, 895, 363], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [438, 446, 562, 459], "page": 1},
 {"key": "issuer", "value": "법원행정처 전산정보중앙관리소 전산운영책임관", "bbox_2d": [257, 481, 721, 497], "page": 1},
 {"key": "issue_time", "value": "06시 41분", "bbox_2d": [191, 527, 251, 537], "page": 1},
 {"key": "applicant", "value": "남궁예태", "bbox_2d": [191, 543, 247, 554], "page": 1},
 {"key": "doc_check_no", "value": "9745-8227-1390-2186", "bbox_2d": [160, 945, 269, 955], "page": 1}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [708, 459, 798, 522], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions family_relation_certificate --show` · `python -m docgen.preview family_relation_certificate --out work/family_relation_certificate`
