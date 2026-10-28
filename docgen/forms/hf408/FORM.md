# 본인확인서(FATCA CRS 개인,개인사업자용)(국문) (`hf408`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf408 · card-hash: c526f661cc5d -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 해외금융계좌 납세자 확인서(개인) (다른 이름: 본인확인서(FATCA CRS 개인,개인사업자용)(국문))
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.408 (기타) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 15칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `customer.surname_en` | 성(SurName) | text | 1쪽 [322, 211, 421, 222] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:55 | 묻기 |
| `customer.given_name_en` | 이름(GivenName) | text | 1쪽 [321, 238, 374, 249] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:70 | 묻기 |
| `customer.birth` | 생년월일 | date | 1쪽 [689, 211, 811, 222] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:85 | 묻기 |
| `customer.phone` | 연락처 | phone | 1쪽 [686, 238, 795, 249] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:97 | 묻기 |
| `tax.residence_list.*.country` | 거주관할권*(1) / 거주관할권*(2) | text | 1쪽 [257, 550, 290, 562] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:228 | 묻기 |
| `tax.residence_list.*.tin` | 납세자번호(TIN) | text | 1쪽 [341, 550, 479, 562] (1행) | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:256 | 묻기 |
| `customer.overseas_address` | 해외영문주소 | text | 1쪽 [338, 580, 705, 592] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:271 | 묻기 |
| `tax.no_tin_reason` | 내국인또는거주자증명서*또는반증증표*을제출한경우 | text | 1쪽 [582, 638, 647, 650] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `date` | 작성일 | date | 1쪽 [195, 890, 395, 907] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:437 | 묻기 |
| `signer.name` | 인성명 | text | 1쪽 [585, 893, 651, 904] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `signer2.name` | 대리인성명 | text | 1쪽 [584, 915, 649, 927] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `date2` | 작성일(년월일) | date | 1쪽 [192, 895, 247, 903] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.name` | 본인성명 | text | 1쪽 [539, 894, 593, 904] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `agent.name` | 대리인성명 | text | 1쪽 [537, 914, 591, 924] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `agent.relation` | 대리인관계 | text | 1쪽 [853, 914, 866, 924] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

## 체크·도장·서명 (marks) — 15칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `check.FATCA` | FATCA | checkbox (미국시민권자(이중국적자포함) / 미국영주권자 / 미국세법상 미국거주자) | 1쪽 [223, 364, 404, 395] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:109 | 묻기 |
| `check.CRS` | CRS | checkbox (미국이외의 해외거주자) | 1쪽 [223, 396, 405, 426] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:170 | 묻기 |
| `check.해당없음` | 해당없음 | checkbox (모두 해당사항없음) | 1쪽 [223, 426, 374, 456] | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:199 | 묻기 |
| `check.미발급국가` | 미발급국가 | checkbox (미발급국가 / 조세당국이 요구하지 않음 / 미취득) | 1쪽 [678, 538, 857, 566] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.미발급국가2` | 미발급국가 | checkbox (미발급국가 / 조세당국이 요구하지 않음 / 미취득) | 1쪽 [584, 599, 675, 627] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.customer` ← `seal.signer` | 인성명 | seal | 1쪽 [713, 879, 769, 919] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.customer` ← `sign.signer` | 인성명 | signature | 1쪽 [709, 892, 774, 906] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.agent` ← `seal.signer2` | 대리인성명 | seal | 1쪽 [708, 914, 773, 928] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.agent` ← `sign.signer2` | 대리인성명 | signature | 1쪽 [708, 914, 773, 928] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [736, 43, 812, 79] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [736, 43, 812, 79] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [812, 43, 872, 79] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [812, 43, 872, 79] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [874, 45, 920, 78] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [872, 43, 923, 79] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

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
 "NAMGOONG",
 "YETAE",
 "1985년 3월 28일",
 "010-6144-1173",
 "호주",
 "중국",
 "138-220990-58092",
 "2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 163-0001",
 "638-594871-15351",
 "사업자금",
 "남궁예태",
 "남궁찬윤",
 "2025.04.01",
 "부"
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
"남궁찬윤"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- customer.surname_en: 성(SurName)
- customer.given_name_en: 이름(GivenName)
- customer.birth: 생년월일 (고객 생년월일)
- customer.phone: 연락처 (고객 연락처)
- tax.residence_list.0.country: 거주관할권*(1) (1행)
- tax.residence_list.1.country: 거주관할권*(2) (2행)
- tax.residence_list.0.tin: 납세자번호(TIN) (1행)
- customer.overseas_address: 해외영문주소
- tax.residence_list.1.tin: 납세자번호(TIN) (2행)
- tax.no_tin_reason: 내국인또는거주자증명서*또는반증증표*을제출한경우
- date: 작성일
- signer.name: 인성명 (고객 본인의 성명)
- signer2.name: 대리인성명 (대리인의 성명, 같은 항목명 중 1번째 칸)
- date2: 작성일(년월일)
- customer.name: 본인성명 (고객 성명)
- agent.name: 대리인성명 (같은 항목명 중 2번째 칸)
- agent.relation: 대리인관계
```

답:

```json
[{"key": "customer.surname_en", "value": "NAMGOONG", "bbox_2d": [322, 211, 421, 222], "page": 1},
 {"key": "customer.given_name_en", "value": "YETAE", "bbox_2d": [321, 238, 374, 249], "page": 1},
 {"key": "customer.birth", "value": "1985년 3월 28일", "bbox_2d": [689, 211, 811, 222], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [686, 238, 795, 249], "page": 1},
 {"key": "tax.residence_list.0.country", "value": "호주", "bbox_2d": [257, 550, 290, 562], "page": 1},
 {"key": "tax.residence_list.1.country", "value": "중국", "bbox_2d": [257, 611, 290, 622], "page": 1},
 {"key": "tax.residence_list.0.tin", "value": "138-220990-58092", "bbox_2d": [341, 550, 479, 562], "page": 1},
 {"key": "customer.overseas_address", "value": "2-3-1 Nishi-Shinjuku, Shinjuku-ku, Tokyo 163-0001", "bbox_2d": [338, 580, 705, 592], "page": 1},
 {"key": "tax.residence_list.1.tin", "value": "638-594871-15351", "bbox_2d": [340, 611, 478, 622], "page": 1},
 {"key": "tax.no_tin_reason", "value": "사업자금", "bbox_2d": [582, 638, 647, 650], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [195, 890, 395, 907], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [585, 893, 651, 904], "page": 1},
 {"key": "signer2.name", "value": "남궁찬윤", "bbox_2d": [584, 915, 649, 927], "page": 1},
 {"key": "date2", "value": "2025.04.01", "bbox_2d": [192, 895, 247, 903], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [539, 894, 593, 904], "page": 1},
 {"key": "agent.name", "value": "남궁찬윤", "bbox_2d": [537, 914, 591, 924], "page": 1},
 {"key": "agent.relation", "value": "부", "bbox_2d": [853, 914, 866, 924], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- check.FATCA: FATCA (체크박스, 보기: 미국시민권자(이중국적자포함) / 미국영주권자 / 미국세법상 미국거주자)
- check.CRS: CRS (체크박스, 보기: 미국이외의 해외거주자)
- check.해당없음: 해당없음 (체크박스, 보기: 모두 해당사항없음)
- check.미발급국가: 미발급국가 (같은 항목명 중 1번째 칸, 체크박스, 보기: 미발급국가 / 조세당국이 요구하지 않음 / 미취득)
- check.미발급국가2: 미발급국가 (같은 항목명 중 2번째 칸, 체크박스, 보기: 미발급국가 / 조세당국이 요구하지 않음 / 미취득)
- seal.customer: 인성명 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 인성명 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.agent: 대리인성명 (대리인 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.agent: 대리인성명 (대리인 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.본인확인: 본인확인 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.본인확인: 본인확인 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.FATCA", "value": "미국세법상 미국거주자", "bbox_2d": [223, 364, 240, 395], "page": 1},
 {"key": "check.CRS", "value": "미국이외의 해외거주자", "bbox_2d": [223, 396, 240, 426], "page": 1},
 {"key": "check.해당없음", "value": "모두 해당사항없음", "bbox_2d": [223, 426, 240, 456], "page": 1},
 {"key": "check.미발급국가", "value": "조세당국이 요구하지 않음", "bbox_2d": [678, 538, 695, 566], "page": 1},
 {"key": "check.미발급국가2", "value": "미발급국가", "bbox_2d": [584, 599, 601, 627], "page": 1},
 {"key": "seal.customer", "value": true, "bbox_2d": [713, 879, 769, 919], "page": 1},
 {"key": "sign.customer", "value": false},
 {"key": "seal.agent", "value": false},
 {"key": "sign.agent", "value": false},
 {"key": "seal.staff.본인확인", "value": false},
 {"key": "sign.staff.본인확인", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": true, "bbox_2d": [812, 43, 872, 79], "page": 1},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [874, 45, 920, 78], "page": 1},
 {"key": "sign.staff.책임자", "value": false}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기·위치·항목명 | studio ① 서식 › 영역 편집 (저장하면 `fields.json` items) | 재검수 → 카드 다시 만들기 |
| 값이 이상함 | 영역 편집에서 그 칸의 값 출처·값 종류 | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf408 --show` · `python -m docgen.preview hf408 --out work/hf408`
