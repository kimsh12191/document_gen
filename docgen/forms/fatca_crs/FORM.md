# 해외금융계좌 납세자 확인서(개인) (`fatca_crs`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card fatca_crs · card-hash: 6b3968053981 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 해외금융계좌 납세자 확인서(개인) (다른 이름: 본인확인서(FATCA CRS 개인,개인사업자용)(국문))
- **쓰이는 업무:** 개인 계좌개설
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> FATCA/CRS 본인확인서(개인/개인사업자용) — 국제조세조정법·금융정보자동교환 이행규정에 따른 자기확인서.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_account.py`, `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 17칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `bank.name` | 은행명 | text | 1쪽 [64, 27, 162, 45] | 늘 | generate.py | look/template.html.j2:72 | 묻기 |
| `customer.name` ← `holder.name` | 성명(한글) | text | 1쪽 [203, 202, 264, 215] | 늘 | generate.py | look/template.html.j2:13 | 묻기 |
| `holder.surname_en` | 영문성 | text | 1쪽 [203, 231, 295, 244] | 늘 | generate.py | look/template.html.j2:24 | 묻기 |
| `holder.given_en` | 영문이름 | text | 1쪽 [664, 231, 714, 244] | 늘 | generate.py | look/template.html.j2:25 | 묻기 |
| `customer.birth` ← `holder.birth` | 생년월일 | date | 1쪽 [203, 260, 272, 273] | 늘 | generate.py | look/template.html.j2:26 | 묻기 |
| `customer.mobile` ← `holder.mobile` | 연락처 | phone | 1쪽 [664, 260, 759, 273] | 늘 | generate.py | look/template.html.j2:27 | 묻기 |
| `holder.birth_place` | 출생국가 | text | 1쪽 [203, 289, 332, 301] | 늘 | generate.py | look/template.html.j2:28 | 묻기 |
| `customer.nationality` ← `holder.nationality` | 국적 | text | 1쪽 [664, 289, 794, 301] | 늘 | generate.py | look/template.html.j2:29 | 묻기 |
| `customer.address` ← `holder.address` | 현재거주지주소 | text | 1쪽 [203, 318, 736, 330] | 늘 | generate.py | look/template.html.j2:30 | 묻기 |
| `residence_category` | 해외거주자여부 | text | 1쪽 [173, 426, 270, 439] | 늘 | generate.py | look/template.html.j2:34 | 묻기 |
| `date` | 작성일 | date | 1쪽 [464, 710, 534, 723] | 늘 | generate.py | look/template.html.j2:69 | 묻기 |
| `signature` | 계좌보유자 | text | 1쪽 [766, 710, 828, 723] | 늘 | generate.py | look/template.html.j2:70 | 묻기 |
| `bank_use.branch` | 접수영업점 | text | 1쪽 [177, 778, 239, 791] | 늘 | generate.py | look/template.html.j2:78 | 묻기 |
| `bank_use.clerk` | 담당 | text | 1쪽 [811, 802, 850, 814] | 늘 | generate.py | look/template.html.j2:81 | 묻기 |
| `bank_use.manager` | 책임자 | text | 1쪽 [892, 802, 931, 814] | 늘 | generate.py | look/template.html.j2:81 | 묻기 |
| `residences.*.country` | 거주관할권 | - | - (1행) | 3/16 | generate.py | look/template.html.j2:49 | 묻기 |
| `residences.*.tin` | 납세자번호 | - | - (1행) | 3/16 | generate.py | look/template.html.j2:50 | 묻기 |

## 체크·도장·서명 (marks) — 4칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.customer` ← `seal.holder` | 계좌보유자 | seal | 1쪽 [858, 709, 962, 724] | 늘 | generate.py | - | 묻기 |
| `sign.customer` ← `sign.holder` | 계좌보유자 | signature | 1쪽 [835, 698, 985, 732] | 늘 | generate.py | - | 묻기 |
| `seal.staff.clerk` | 담당 | seal | 1쪽 [804, 789, 858, 827] | 늘 | generate.py | - | 묻기 |
| `seal.staff.manager` | 책임자 | seal | 1쪽 [884, 789, 939, 827] | 늘 | generate.py | - | 묻기 |

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
"해외금융계좌 납세자 확인서(개인)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "국민은행",
 "남궁예태",
 "NAMGOONG",
 "YETAE",
 "1985.03.28",
 "010-6144-1173",
 "대한민국 (KOREA)",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "해당사항 없음",
 "2025.04.01",
 "센텀지점",
 "하기윤",
 "옥형희"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"국민은행"
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

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- bank.name: 은행명
- customer.name: 성명(한글) (고객 성명)
- holder.surname_en: 영문성
- holder.given_en: 영문이름
- customer.birth: 생년월일 (고객 생년월일)
- customer.mobile: 연락처 (고객 휴대전화)
- holder.birth_place: 출생국가
- customer.nationality: 국적 (고객 국적)
- customer.address: 현재거주지주소 (고객 주소)
- residence_category: 해외거주자여부
- date: 작성일
- signature: 계좌보유자
- bank_use.branch: 접수영업점
- bank_use.clerk: 담당
- bank_use.manager: 책임자
```

답:

```json
[{"key": "bank.name", "value": "국민은행", "bbox_2d": [64, 27, 162, 45], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [203, 202, 264, 215], "page": 1},
 {"key": "holder.surname_en", "value": "NAMGOONG", "bbox_2d": [203, 231, 295, 244], "page": 1},
 {"key": "holder.given_en", "value": "YETAE", "bbox_2d": [664, 231, 714, 244], "page": 1},
 {"key": "customer.birth", "value": "1985.03.28", "bbox_2d": [203, 260, 272, 273], "page": 1},
 {"key": "customer.mobile", "value": "010-6144-1173", "bbox_2d": [664, 260, 759, 273], "page": 1},
 {"key": "holder.birth_place", "value": "대한민국 (KOREA)", "bbox_2d": [203, 289, 332, 301], "page": 1},
 {"key": "customer.nationality", "value": "대한민국 (KOREA)", "bbox_2d": [664, 289, 794, 301], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [203, 318, 736, 330], "page": 1},
 {"key": "residence_category", "value": "해당사항 없음", "bbox_2d": [173, 426, 270, 439], "page": 1},
 {"key": "date", "value": "2025.04.01", "bbox_2d": [464, 710, 534, 723], "page": 1},
 {"key": "signature", "value": "남궁예태", "bbox_2d": [766, 710, 828, 723], "page": 1},
 {"key": "bank_use.branch", "value": "센텀지점", "bbox_2d": [177, 778, 239, 791], "page": 1},
 {"key": "bank_use.clerk", "value": "하기윤", "bbox_2d": [811, 802, 850, 814], "page": 1},
 {"key": "bank_use.manager", "value": "옥형희", "bbox_2d": [892, 802, 931, 814], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.customer: 계좌보유자 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 계좌보유자 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.clerk: 담당 (도장)
- seal.staff.manager: 책임자 (도장)
```

답:

```json
[{"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [835, 698, 985, 732], "page": 1},
 {"key": "seal.staff.clerk", "value": true, "bbox_2d": [804, 789, 858, 827], "page": 1},
 {"key": "seal.staff.manager", "value": true, "bbox_2d": [884, 789, 939, 827], "page": 1}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions fatca_crs --show` · `python -m docgen.preview fatca_crs --out work/fatca_crs`
