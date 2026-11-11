# 고객확인서(법인·단체) (`corporate_customer_due_diligence`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card corporate_customer_due_diligence · card-hash: 7b20ff9936e2 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 고객확인서(법인·단체) (다른 이름: 고객확인서(법인,고유번호나 납세번호가 있는 임의 단체용))
- **질문·답:** 이 폴더의 `questions.json` 에서 바꾼 것이 있음 (아래 ← 바꿈)
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa corporate_customer_due_diligence --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 법인 고객확인 + 실제소유자 확인 서식.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `questions.json` | 기본 과제의 질문 문장·답 틀 (기본과 다른 것만) |
| `docgen/docs/bank_form_account.py`, `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 22칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank.name` | 은행명 | text | 1쪽 [74, 33, 171, 50] | 늘 | 템플릿 | generate.py | fields.json:20 | 묻기 |
| `corp.name` | 법인명(국문) | text | 1쪽 [182, 193, 283, 206] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:95 | 묻기 |
| `corp.name_en` | 법인명(영문) | text | 1쪽 [739, 193, 894, 206] | 늘 | 템플릿 | generate.py | look/template.html.j2:21 · fields.json:100 | 묻기 |
| `corp.biz_no` | 사업자등록번호 | biz_no | 1쪽 [182, 212, 268, 225] | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:55 | 묻기 |
| `corp.corp_no` | 법인등록번호 | corp_reg_no | 1쪽 [739, 212, 842, 225] | 늘 | 템플릿 | generate.py | look/template.html.j2:22 · fields.json:60 | 묻기 |
| `corp.established` | 설립일 | date | 1쪽 [182, 231, 250, 244] | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:75 | 묻기 |
| `corp.industry` | 업종 | text | 1쪽 [739, 231, 857, 244] | 늘 | 템플릿 | generate.py | look/template.html.j2:23 · fields.json:85 | 묻기 |
| `corp.hq_address` | 본점주소 | text | 1쪽 [182, 250, 613, 263] | 늘 | 템플릿 | generate.py | look/template.html.j2:24 · fields.json:80 | 묻기 |
| `corp.biz_address` | 사업장주소 | text | 1쪽 [182, 269, 262, 281] | 늘 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:50 | 묻기 |
| `corp.phone` | 대표전화 | phone | 1쪽 [182, 288, 268, 300] | 늘 | 템플릿 | generate.py | look/template.html.j2:26 · fields.json:105 | 묻기 |
| `corp.email` | 이메일 | text | 1쪽 [739, 288, 865, 300] | 늘 | 템플릿 | generate.py | look/template.html.j2:26 · fields.json:70 | 묻기 |
| `rep.name` | 대표자성명 | text | 1쪽 [182, 369, 243, 382] | 늘 | 템플릿 | generate.py | look/template.html.j2:11 · fields.json:130 | 묻기 |
| `rep.name_en` | 대표자영문성명 | text | 1쪽 [535, 369, 677, 382] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:135 | 묻기 |
| `rep.birth` | 대표자생년월일 | date | 1쪽 [182, 388, 250, 401] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:125 | 묻기 |
| `rep.nationality` | 대표자국적 | text | 1쪽 [535, 388, 596, 401] | 늘 | 템플릿 | generate.py | look/template.html.j2:34 · fields.json:140 | 묻기 |
| `date` | 작성일 | date | 1쪽 [839, 750, 952, 763] | 늘 | 템플릿 | generate.py | look/template.html.j2:85 · fields.json:110 | 묻기 |
| `bank_use.branch` | 확인영업점 | text | 1쪽 [187, 894, 248, 907] | 늘 | 템플릿 | generate.py | look/template.html.j2:101 · fields.json:25 | 묻기 |
| `bank_use.clerk` | 담당 | text | 1쪽 [801, 883, 840, 895] | 늘 | 템플릿 | generate.py | look/template.html.j2:103 · fields.json:30 | 묻기 |
| `bank_use.manager` | 책임자 | text | 1쪽 [882, 883, 921, 895] | 늘 | 템플릿 | generate.py | look/template.html.j2:103 · fields.json:40 | 묻기 |
| `agent.name` | 거래담당자성명 | - | - | 3/16 | 템플릿 | generate.py | look/template.html.j2:79 · fields.json:5 | 묻기 |
| `agent.rrn` | 거래담당자실명번호 | - | - | 3/16 | 템플릿 | generate.py | look/template.html.j2:79 · fields.json:15 | 묻기 |
| `agent.position` | 직위관계 | - | - | 3/16 | 템플릿 | generate.py | look/template.html.j2:79 · fields.json:10 | 묻기 |

## 표 `owners` (표 과제 table·table_read·table_find·table_qa) — 5열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `owners.*.name` | 성명 | text | 1쪽 [234, 572, 295, 584] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:190 | 묻기 |
| `owners.*.birth` | 생년월일 | date | 1쪽 [478, 572, 546, 584] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:185 | 묻기 |
| `owners.*.nationality` | 국적 | text | 1쪽 [614, 572, 675, 584] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:195 | 묻기 |
| `owners.*.ratio` | 지분율 | percent | 1쪽 [737, 572, 784, 584] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:200 | 묻기 |
| `owners.*.relation` | 법인과의관계 | text | 1쪽 [852, 572, 913, 584] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:205 | 묻기 |

## 표 `bank_use.documents` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank_use.documents.*` | 징구서류 | text | 1쪽 [200, 875, 291, 887] (1행) | 늘 | 템플릿 | generate.py | - | 묻기 |

## 표 `shareholders` (표 과제 table·table_read·table_find·table_qa) — 5열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `shareholders.*.name` | 주주명 | - | - (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:220 | 묻기 |
| `shareholders.*.birth` | 생년월일 | - | - (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:215 | 묻기 |
| `shareholders.*.shares` | 소유주식수 | - | - (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:64 · fields.json:235 | 묻기 |
| `shareholders.*.ratio` | 지분율 | - | - (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:225 | 묻기 |
| `shareholders.*.relation` | 법인과의관계 | - | - (1행) | 3/16 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:230 | 묻기 |

## 체크·도장·서명 (marks) — 11칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `corp.corp_type` | 법인구분 | checkbox (대기업 / 중소기업 / 국가·지자체·공공단체 / 금융기관 / 비영리법인(단체) / 외국법인(단체)) | 1쪽 [264, 307, 324, 319] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:65 | 묻기 |
| `corp.listed` | 상장여부 | checkbox (유가증권시장 / 코스닥 / 코넥스 / 비상장) | 1쪽 [446, 326, 491, 338] | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:90 | 묻기 |
| `transaction.purpose` | 거래목적 | checkbox (사업상 거래(결제) / 운영자금 관리 / 급여 지급 / 대출 / 기타) | 1쪽 [455, 432, 520, 444] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:165 | 묻기 |
| `transaction.fund_source` | 자금원천 | checkbox (영업수익 / 자본금 / 차입금 / 투자수익 / 기타) | 1쪽 [195, 451, 256, 463] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:160 | 묻기 |
| `owner_step` | 실제소유자확인단계 | checkbox (1단계 / 2단계 / 3단계) | 1쪽 [195, 494, 233, 507] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:115 | 묻기 |
| `pep` | 외국의정치적주요인물여부 | checkbox (예 / 아니오) | 1쪽 [822, 668, 867, 680] | 늘 | 템플릿 | generate.py | look/template.html.j2:74 · fields.json:120 | 묻기 |
| `seal.corp` | 법인인감 | seal | 1쪽 [867, 762, 957, 826] | 늘 | 템플릿 | generate.py | fields.json:145 | 묻기 |
| `bank_use.risk_grade` | 고객위험등급 | checkbox (저위험 / 중위험 / 고위험) | 1쪽 [269, 855, 314, 867] | 늘 | 템플릿 | generate.py | look/template.html.j2:99 · fields.json:45 | 묻기 |
| `seal.staff.clerk` | 담당 | seal | 1쪽 [793, 870, 848, 908] | 늘 | 템플릿 | generate.py | fields.json:150 | 묻기 |
| `seal.staff.manager` | 책임자 | seal | 1쪽 [874, 870, 929, 908] | 늘 | 템플릿 | generate.py | fields.json:155 | 묻기 |
| `bank_use.documents` | 징구서류 | checkbox_multi (사업자등록증 / 법인등기사항전부증명서 / 주주명부 / 정관 / 법인인감증명서) | - | 늘 | 템플릿 | generate.py | look/template.html.j2:100 · fields.json:35 | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키는·값은:** 어디서 정해지나. 키·값 종류는 이 서식 파일에 적힌 그대로입니다 (모든 서식 공통 키 사전은 없음). "키 설명 그대로" 는 칸에 `"key"` 가 없어 키 설명이 키로 나가는 것. 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
- **고칠 곳:** html·코드 서식은 템플릿 줄(칸 자리·키·항목명)과 fields.json 줄(값 출처·질문 설정 q), 원본 서식은 fields.json 의 그 칸(박스 `rect`·항목명·키·값·q). html·코드 서식에서 fields.json 에 줄이 없는 칸의 질문 설정은 fields.json 맨 위 `"q": {"키": {…}}` 묶음에.

## 질문 → 답 (seed 1000000 로 그린 실제 문항)

질문은 모델에게 가는 글 전부, 답은 데이터의 정답 (그린 문서의 값·위치). 질문 문장·답 꼴은 이 폴더 `questions.json` 과 공통 `docgen/forms/_common/questions.json`.

### 서류 분류 `classify` · 채점 acc

질문:

```
이 문서는 고객이 은행에 제출한 서류입니다. 서류의 정식 명칭(서류명)을 답하세요. 설명 없이 서류명만 한 줄로 답하세요.
```

답:

```json
"고객확인서(법인·단체)"
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
 "(주)미래케미칼",
 "Mirae Chemical Co., Ltd.",
 "702-81-38348",
 "200112-7951835",
 "2020.06.15",
 "제조업 / 화학제품",
 "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)",
 "본점과 동일",
 "064-756-8800",
 "contact@mirae.co.kr",
 "남궁예태",
 "NAMGOONG YETAE",
 "1985.03.28",
 "대한민국",
 "66.77%",
 "대표이사",
 "2025년 04월 01일",
 "사업자등록증",
 "법인등기사항전부증명서",
 "주주명부",
 "정관",
 "센텀지점",
 "이용주",
 "김형인"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"이용주"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"김형인"
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
- bank.name: 은행명
- corp.name: 법인명(국문)
- corp.name_en: 법인명(영문)
- corp.biz_no: 사업자등록번호
- corp.corp_no: 법인등록번호
- corp.established: 설립일
- corp.industry: 업종
- corp.hq_address: 본점주소
- corp.biz_address: 사업장주소
- corp.phone: 대표전화
- corp.email: 이메일
- rep.name: 대표자성명
- rep.name_en: 대표자영문성명
- rep.birth: 대표자생년월일
- rep.nationality: 대표자국적
- date: 작성일
- bank_use.documents.0: 징구서류 (1번째)
- bank_use.documents.1: 징구서류 (2번째)
- bank_use.documents.2: 징구서류 (3번째)
- bank_use.documents.3: 징구서류 (4번째)
- bank_use.branch: 확인영업점
- bank_use.clerk: 담당
- bank_use.manager: 책임자
```

답:

```json
[{"key": "bank.name", "value": "국민은행", "bbox_2d": [74, 33, 171, 50], "page": 1},
 {"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [182, 193, 283, 206], "page": 1},
 {"key": "corp.name_en", "value": "Mirae Chemical Co., Ltd.", "bbox_2d": [739, 193, 894, 206], "page": 1},
 {"key": "corp.biz_no", "value": "702-81-38348", "bbox_2d": [182, 212, 268, 225], "page": 1},
 {"key": "corp.corp_no", "value": "200112-7951835", "bbox_2d": [739, 212, 842, 225], "page": 1},
 {"key": "corp.established", "value": "2020.06.15", "bbox_2d": [182, 231, 250, 244], "page": 1},
 {"key": "corp.industry", "value": "제조업 / 화학제품", "bbox_2d": [739, 231, 857, 244], "page": 1},
 {"key": "corp.hq_address", "value": "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)", "bbox_2d": [182, 250, 613, 263], "page": 1},
 {"key": "corp.biz_address", "value": "본점과 동일", "bbox_2d": [182, 269, 262, 281], "page": 1},
 {"key": "corp.phone", "value": "064-756-8800", "bbox_2d": [182, 288, 268, 300], "page": 1},
 {"key": "corp.email", "value": "contact@mirae.co.kr", "bbox_2d": [739, 288, 865, 300], "page": 1},
 {"key": "rep.name", "value": "남궁예태", "bbox_2d": [182, 369, 243, 382], "page": 1},
 {"key": "rep.name_en", "value": "NAMGOONG YETAE", "bbox_2d": [535, 369, 677, 382], "page": 1},
 {"key": "rep.birth", "value": "1985.03.28", "bbox_2d": [182, 388, 250, 401], "page": 1},
 {"key": "rep.nationality", "value": "대한민국", "bbox_2d": [535, 388, 596, 401], "page": 1},
 {"key": "date", "value": "2025년 04월 01일", "bbox_2d": [839, 750, 952, 763], "page": 1},
 {"key": "bank_use.documents.0", "value": "사업자등록증", "bbox_2d": [200, 875, 291, 887], "page": 1},
 {"key": "bank_use.documents.1", "value": "법인등기사항전부증명서", "bbox_2d": [314, 875, 480, 887], "page": 1},
 {"key": "bank_use.documents.2", "value": "주주명부", "bbox_2d": [503, 875, 564, 887], "page": 1},
 {"key": "bank_use.documents.3", "value": "정관", "bbox_2d": [587, 875, 617, 887], "page": 1},
 {"key": "bank_use.branch", "value": "센텀지점", "bbox_2d": [187, 894, 248, 907], "page": 1},
 {"key": "bank_use.clerk", "value": "이용주", "bbox_2d": [801, 883, 840, 895], "page": 1},
 {"key": "bank_use.manager", "value": "김형인", "bbox_2d": [882, 883, 921, 895], "page": 1}]
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
- corp.corp_type: 법인구분 (체크박스, 보기: 대기업 / 중소기업 / 국가·지자체·공공단체 / 금융기관 / 비영리법인(단체) / 외국법인(단체))
- corp.listed: 상장여부 (체크박스, 보기: 유가증권시장 / 코스닥 / 코넥스 / 비상장)
- transaction.purpose: 거래목적 (체크박스, 보기: 사업상 거래(결제) / 운영자금 관리 / 급여 지급 / 대출 / 기타)
- transaction.fund_source: 자금원천 (체크박스, 보기: 영업수익 / 자본금 / 차입금 / 투자수익 / 기타)
- owner_step: 실제소유자확인단계 (체크박스, 보기: 1단계 / 2단계 / 3단계)
- pep: 외국의정치적주요인물여부 (체크박스, 보기: 예 / 아니오)
- seal.corp: 법인인감 (도장)
- bank_use.risk_grade: 고객위험등급 (체크박스, 보기: 저위험 / 중위험 / 고위험)
- seal.staff.clerk: 담당 (도장)
- seal.staff.manager: 책임자 (도장)
- bank_use.documents: 징구서류 (복수 선택, 보기: 사업자등록증 / 법인등기사항전부증명서 / 주주명부 / 정관 / 법인인감증명서)
```

답:

```json
[{"key": "corp.corp_type", "value": "중소기업", "bbox_2d": [251, 307, 260, 319], "page": 1},
 {"key": "corp.listed", "value": "비상장", "bbox_2d": [433, 326, 442, 338], "page": 1},
 {"key": "transaction.purpose", "value": "급여 지급", "bbox_2d": [442, 432, 452, 444], "page": 1},
 {"key": "transaction.fund_source", "value": "영업수익", "bbox_2d": [182, 451, 192, 463], "page": 1},
 {"key": "owner_step", "value": "1단계", "bbox_2d": [182, 494, 192, 507], "page": 1},
 {"key": "pep", "value": "아니오", "bbox_2d": [809, 668, 818, 680], "page": 1},
 {"key": "seal.corp", "value": true, "bbox_2d": [867, 762, 957, 826], "page": 1},
 {"key": "bank_use.risk_grade", "value": "중위험", "bbox_2d": [256, 855, 265, 867], "page": 1},
 {"key": "seal.staff.clerk", "value": true, "bbox_2d": [793, 870, 848, 908], "page": 1},
 {"key": "seal.staff.manager", "value": true, "bbox_2d": [874, 870, 929, 908], "page": 1},
 {"key": "bank_use.documents", "value": "사업자등록증", "bbox_2d": [187, 875, 197, 887], "page": 1},
 {"key": "bank_use.documents", "value": "법인등기사항전부증명서", "bbox_2d": [301, 875, 310, 887], "page": 1},
 {"key": "bank_use.documents", "value": "주주명부", "bbox_2d": [490, 875, 499, 887], "page": 1},
 {"key": "bank_use.documents", "value": "정관", "bbox_2d": [574, 875, 583, 887], "page": 1}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 설명)
- name: 성명
- birth: 생년월일
- nationality: 국적
- ratio: 지분율
- relation: 법인과의관계
```

답:

```json
{
 "columns": [
  "name",
  "birth",
  "nationality",
  "ratio",
  "relation"
 ],
 "rows": [
  [
   "남궁예태",
   "1985.03.28",
   "대한민국",
   "66.77%",
   "대표이사"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    234,
    572,
    913,
    584
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
[{"columns": ["성명", "생년월일", "국적", "지분율", "법인과의관계"], "bbox_2d": [86, 550, 952, 584], "page": 1, "n_rows": 1}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[86, 550, 952, 584] 위치의 표를 보고 답하세요. '성명' 칸이 '남궁예태'인 행의 '생년월일' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"1985.03.28"
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[86, 550, 952, 584] 위치의 표를 보고 답하세요. '지분율' 칸의 값을 모두 더하면 얼마입니까? 빈 칸은 0 으로 봅니다. (쉼표·단위 없이 숫자만 답하세요)
```

답:

```json
66.77
```

### 표 그대로 옮기기 `table_read` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 표를 머리글까지 그대로 옮겨 JSON 으로 답하세요.
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
  "No",
  "실제소유자 성명",
  "생년월일",
  "국적",
  "지분율",
  "법인과의 관계"
 ],
 "rows": [
  [
   "1",
   "남궁예태",
   "1985.03.28",
   "대한민국",
   "66.77%",
   "대표이사"
  ],
  [
   "2",
   null,
   null,
   null,
   null,
   null
  ],
  [
   "3",
   null,
   null,
   null,
   null,
   null
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    48,
    569,
    952,
    588
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    48,
    588,
    952,
    606
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    48,
    606,
    952,
    625
   ],
   "page": 1
  }
 ]
}
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa corporate_customer_due_diligence --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check corporate_customer_due_diligence` → `python -m docgen.formdir card corporate_customer_due_diligence` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa corporate_customer_due_diligence --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions corporate_customer_due_diligence --show` · `python -m docgen.preview corporate_customer_due_diligence --out work/corporate_customer_due_diligence`
