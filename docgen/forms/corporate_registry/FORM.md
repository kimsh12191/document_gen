# 법인 등기사항전부증명서(현재 유효사항) (`corporate_registry`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card corporate_registry · card-hash: 3893801734f9 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** corporate · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 법인 등기사항전부증명서(현재 유효사항)
- **쓰이는 업무:** 법인 여신
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa corporate_registry --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 인터넷등기소 발급 법인 등기사항전부증명서.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/corporate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 34칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `issue_type` | 발급구분 | text | 1쪽 [869, 47, 913, 59] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:100 | 묻기 |
| `issue_scope` | 증명서구분 | text | 1쪽 [546, 67, 760, 91] | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:95 | 묻기 |
| `reg_no` | 등기번호 | number | 1쪽 [179, 106, 227, 119] | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:145 | 묻기 |
| `corp_reg_no` | 등록번호 | corp_reg_no | 1쪽 [179, 128, 288, 140] | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:50 | 묻기 |
| `corp.name` ← `company_name` | 상호 | text | 1쪽 [271, 157, 413, 170] | 늘 | 템플릿 | generate.py | look/template.html.j2:56 · fields.json:30 | 묻기 |
| `head_office` | 본점 | text | 1쪽 [271, 204, 709, 217] | 늘 | 템플릿 | generate.py | look/template.html.j2:61 · fields.json:65 | 묻기 |
| `head_office_change.changed` | 변경연월일 | text | 1쪽 [806, 198, 896, 209] | 2/16 | 템플릿 | generate.py | fields.json:70 | 묻기 |
| `head_office_change.registered` | 등기연월일 | text | 1쪽 [806, 211, 896, 221] | 2/16 | 템플릿 | generate.py | fields.json:75 | 묻기 |
| `notice_method` | 공고방법 | text | 1쪽 [271, 230, 709, 243] | 늘 | 템플릿 | generate.py | look/template.html.j2:62 · fields.json:115 | 묻기 |
| `par_value` | 1주의금액 | amount | 1쪽 [271, 251, 344, 264] | 늘 | 템플릿 | generate.py | look/template.html.j2:63 · fields.json:130 | 묻기 |
| `authorized_shares` | 발행할주식의총수 | text | 1쪽 [271, 272, 340, 285] | 늘 | 템플릿 | generate.py | look/template.html.j2:64 · fields.json:5 | 묻기 |
| `issued_shares` | 발행주식의총수 | text | 1쪽 [206, 366, 267, 378] | 늘 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:105 | 묻기 |
| `common_shares` | 보통주식 | text | 1쪽 [183, 380, 244, 393] | 늘 | 템플릿 | generate.py | look/template.html.j2:69 · fields.json:25 | 묻기 |
| `capital` | 자본금의액 | amount | 1쪽 [560, 373, 676, 386] | 늘 | 템플릿 | generate.py | look/template.html.j2:70 · fields.json:10 | 묻기 |
| `capital_change.changed` | 변경연월일 | text | 1쪽 [786, 367, 877, 378] | 10/16 | 템플릿 | generate.py | fields.json:15 | 묻기 |
| `capital_change.registered` | 등기연월일 | text | 1쪽 [786, 380, 877, 390] | 10/16 | 템플릿 | generate.py | fields.json:20 | 묻기 |
| `established` | 회사성립연월일 | date | 2쪽 [271, 50, 398, 62] | 늘 | 템플릿 | generate.py | look/template.html.j2:117 · fields.json:55 | 묻기 |
| `opening_reason` | 등기기록개설사유 | text | 2쪽 [271, 78, 302, 91] | 늘 | 템플릿 | generate.py | look/template.html.j2:118 · fields.json:125 | 묻기 |
| `opening_date` | 등기기록개설일 | date | 2쪽 [318, 78, 444, 91] | 늘 | 템플릿 | generate.py | look/template.html.j2:118 · fields.json:120 | 묻기 |
| `fee` | 수수료 | amount | 2쪽 [116, 128, 162, 139] | 10/16 | 템플릿 | generate.py | look/template.html.j2:125 · fields.json:60 | 묻기 |
| `jurisdiction` | 관할등기소 | text | 2쪽 [513, 128, 644, 139] | 늘 | 템플릿 | generate.py | look/template.html.j2:122 · fields.json:110 | 묻기 |
| `issue_date` | 발행일 | text | 2쪽 [425, 163, 575, 176] | 10/16 | 템플릿 | generate.py | look/template.html.j2:128 · fields.json:80 | 묻기 |
| `issue_no` | 발행번호 | number | 2쪽 [130, 258, 243, 268] | 늘 | 템플릿 | generate.py | look/template.html.j2:122 · fields.json:90 | 묻기 |
| `confirm_no` | 발급확인번호 | text | 2쪽 [519, 258, 632, 268] | 10/16 | 템플릿 | generate.py | look/template.html.j2:135 · fields.json:45 | 묻기 |
| `issue_date_short` | 발행일 | date | 2쪽 [865, 258, 929, 268] | 10/16 | 템플릿 | generate.py | look/template.html.j2:135 · fields.json:85 | 묻기 |
| `viewed_at` | 열람일시 | - | - | 6/16 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:155 | 묻기 |
| `preferred_shares` | 상환전환우선주식 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:69 | 묻기 |
| `purpose_history.*.purposes.*` | 목적 | - | - (1행) | 2/16 | 템플릿 | generate.py | - | 묻기 |
| `purpose_change.changed` | 변경연월일 | - | - | 2/16 | 템플릿 | generate.py | fields.json:135 | 묻기 |
| `purpose_change.registered` | 등기연월일 | - | - | 2/16 | 템플릿 | generate.py | fields.json:140 | 묻기 |
| `company_name_change.changed` | 변경연월일 | - | - | 3/16 | 템플릿 | generate.py | fields.json:35 | 묻기 |
| `company_name_change.registered` | 등기연월일 | - | - | 3/16 | 템플릿 | generate.py | fields.json:40 | 묻기 |
| `joint_representation` | 공동대표 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:98 | 묻기 |
| `joint_registered` | 등기일 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:99 | 묻기 |

## 표 `office_history` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `office_history.*.address` | 본점 | text | 1쪽 [271, 178, 724, 191] (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:59 · fields.json:230 | 묻기 |

## 표 `capital_history` (표 과제 table·table_read·table_find·table_qa) — 5열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `capital_history.*.issued_shares` | 발행주식의총수 | text | 1쪽 [206, 330, 260, 343] (1행) | 6/16 | 템플릿 | generate.py | fields.json:205 | 묻기 |
| `capital_history.*.common_shares` | 보통주식 | text | 1쪽 [183, 345, 237, 357] (1행) | 6/16 | 템플릿 | generate.py | fields.json:200 | 묻기 |
| `capital_history.*.capital` | 자본금의액 | amount | 1쪽 [564, 338, 672, 350] (1행) | 6/16 | 템플릿 | generate.py | fields.json:190 | 묻기 |
| `capital_history.*.changed` | 변경연월일 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:195 | 묻기 |
| `capital_history.*.registered` | 등기연월일 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:210 | 묻기 |

## 표 `purposes` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `purposes.*` | 목적 | text | 1쪽 [83, 423, 244, 436] (1행) | 늘 | 템플릿 | generate.py | - | 묻기 |

## 표 `officers` (표 과제 table·table_read·table_find·table_qa) — 10열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `officers.*.position` | 직위 | text | 1쪽 [83, 549, 114, 562] (1행) | 늘 | 템플릿 | generate.py | fields.json:285 | 묻기 |
| `officers.*.name` | 성명 | text | 1쪽 [122, 549, 168, 562] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:280 | 묻기 |
| `officers.*.rrn` | 주민등록번호 | rrn | 1쪽 [175, 549, 280, 562] (1행) | 늘 | 템플릿 | generate.py | fields.json:295 | 묻기 |
| `officers.*.appointed` | 취임일 | date | 1쪽 [234, 563, 356, 575] (1행) | 늘 | 템플릿 | generate.py | fields.json:255 | 묻기 |
| `officers.*.appointment_type` | 취임구분 | text | 1쪽 [359, 563, 389, 575] (1행) | 늘 | 템플릿 | generate.py | fields.json:260 | 묻기 |
| `officers.*.registered` | 등기일 | date | 1쪽 [411, 563, 532, 575] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:290 | 묻기 |
| `officers.*.ended` | 퇴임일 | date | 1쪽 [234, 576, 356, 588] (1행) | 7/16 | 템플릿 | generate.py | fields.json:275 | 묻기 |
| `officers.*.end_type` | 퇴임구분 | text | 1쪽 [359, 576, 389, 588] (1행) | 7/16 | 템플릿 | generate.py | fields.json:270 | 묻기 |
| `officers.*.end_registered` | 등기일 | date | 1쪽 [411, 576, 532, 588] (1행) | 7/16 | 템플릿 | generate.py | fields.json:265 | 묻기 |
| `officers.*.address` | 주소 | text | 1쪽 [334, 622, 862, 635] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:59 · fields.json:250 | 묻기 |

## 표 `branches` (표 과제 table·table_read·table_find·table_qa) — 6열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `branches.*.no` | 지점번호 | - | - (1행) | 4/16 | 템플릿 | generate.py | fields.json:170 | 묻기 |
| `branches.*.address` | 지점소재지 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:59 · fields.json:165 | 묻기 |
| `branches.*.opened` | 설치일 | - | - (1행) | 4/16 | 템플릿 | generate.py | fields.json:175 | 묻기 |
| `branches.*.opened_registered` | 등기일 | - | - (1행) | 4/16 | 템플릿 | generate.py | fields.json:180 | 묻기 |
| `branches.*.closed` | 폐지일 | - | - (1행) | 1/16 | 템플릿 | generate.py | - | 묻기 |
| `branches.*.closed_registered` | 등기일 | - | - (1행) | 1/16 | 템플릿 | generate.py | - | 묻기 |

## 표 `name_history` (표 과제 table·table_read·table_find·table_qa) — 3열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `name_history.*.name` | 상호 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:220 | 묻기 |
| `name_history.*.changed` | 변경연월일 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:39 | 묻기 |
| `name_history.*.registered` | 등기연월일 | - | - (1행) | 1/16 | 템플릿 | generate.py | look/template.html.j2:39 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 2쪽 [756, 163, 812, 202] | 10/16 | 템플릿 | generate.py | fields.json:150 | 묻기 |

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
"법인 등기사항전부증명서(현재 유효사항)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "제출용",
 "말소사항 포함",
 "287744",
 "200112-7951835",
 "주식회사 미래케미칼",
 "제주특별자치도 제주시 중앙로 81-2, 20층 (아라동, 글로벌오피스텔)",
 "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)",
 "2023.10.09 이전",
 "2023.10.12 등기",
 "제주특별자치도 내에서 발행되는 일간 서울경제신문에 게재한다.",
 "금 5,000 원",
 "600,000 주",
 "6,000 주",
 "금 30,000,000 원",
 "60,000 주",
 "금 300,000,000 원",
 "2021.03.20 변경",
 "2021.03.26 등기",
 "1. 기초 화학물질 제조업",
 "2. 합성수지 및 플라스틱 제품 제조업",
 "3. 화학제품 도소매업",
 "4. 도료 및 접착제 제조업",
 "5. 화학제품 수출입업",
 "6. 환경 관련 약품 제조 및 판매업",
 "7. 위 각 호와 관련된 부대사업 일체",
 "감사",
 "오우서",
 "621001-*******",
 "2020 년 06 월 15 일",
 "취임",
 "2020 년 06 월 17 일",
 "2021 년 10 월 02 일",
 "사임",
 "2021 년 10 월 08 일",
 "사내이사",
 "하혁승",
 "820702-*******",
 "2020 년 06 월 19 일",
 "대표이사",
 "남궁예태",
 "850328-*******",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "2020 년 06 월 22 일",
 "2020 년 06 월 25 일",
 "원순수",
 "910616-*******",
 "2021 년 10 월 09 일",
 "원승호",
 "671016-*******",
 "2021 년 11 월 04 일",
 "2021 년 11 월 09 일",
 "노도수",
 "830120-*******",
 "2022 년 05 월 26 일",
 "2022 년 06 월 06 일",
 "2023 년 06 월 15 일",
 "중임",
 "2023 년 06 월 18 일",
 "2023 년 06 월 20 일",
 "2023 년 06 월 22 일",
 "2024 년 10 월 02 일",
 "2024 년 10 월 14 일",
 "2024 년 11 월 04 일",
 "2024 년 11 월 07 일",
 "설립",
 "1,000원",
 "제주지방법원 등기과",
 "서기 2025년 03월 26일",
 "8065263136035593",
 "DJHS-S1CW-K9C1",
 "2025/03/26"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"사내이사"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"대표이사"
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
- issue_type: 발급구분
- issue_scope: 증명서구분
- reg_no: 등기번호
- corp_reg_no: 등록번호
- corp.name: 상호 (법인·사업자 상호)
- head_office: 본점
- head_office_change.changed: 변경연월일 (같은 항목명 중 1번째 칸)
- head_office_change.registered: 등기연월일 (같은 항목명 중 1번째 칸)
- notice_method: 공고방법
- par_value: 1주의금액
- authorized_shares: 발행할주식의총수
- issued_shares: 발행주식의총수
- common_shares: 보통주식
- capital: 자본금의액
- capital_change.changed: 변경연월일 (같은 항목명 중 2번째 칸)
- capital_change.registered: 등기연월일 (같은 항목명 중 2번째 칸)
- established: 회사성립연월일
- opening_reason: 등기기록개설사유
- opening_date: 등기기록개설일
- fee: 수수료
- jurisdiction: 관할등기소
- issue_date: 발행일 (같은 항목명 중 1번째 칸)
- issue_no: 발행번호
- confirm_no: 발급확인번호
- issue_date_short: 발행일 (같은 항목명 중 2번째 칸)
```

답:

```json
[{"key": "issue_type", "value": "제출용", "bbox_2d": [869, 47, 913, 59], "page": 1},
 {"key": "issue_scope", "value": "말소사항 포함", "bbox_2d": [546, 67, 760, 91], "page": 1},
 {"key": "reg_no", "value": "287744", "bbox_2d": [179, 106, 227, 119], "page": 1},
 {"key": "corp_reg_no", "value": "200112-7951835", "bbox_2d": [179, 128, 288, 140], "page": 1},
 {"key": "corp.name", "value": "주식회사 미래케미칼", "bbox_2d": [271, 157, 413, 170], "page": 1},
 {"key": "head_office", "value": "제주특별자치도 제주시 첨단로 381-19, 2층 (이도2동, 대성프라자)", "bbox_2d": [271, 204, 709, 217], "page": 1},
 {"key": "head_office_change.changed", "value": "2023.10.09 이전", "bbox_2d": [806, 198, 896, 209], "page": 1},
 {"key": "head_office_change.registered", "value": "2023.10.12 등기", "bbox_2d": [806, 211, 896, 221], "page": 1},
 {"key": "notice_method", "value": "제주특별자치도 내에서 발행되는 일간 서울경제신문에 게재한다.", "bbox_2d": [271, 230, 709, 243], "page": 1},
 {"key": "par_value", "value": "금 5,000 원", "bbox_2d": [271, 251, 344, 264], "page": 1},
 {"key": "authorized_shares", "value": "600,000 주", "bbox_2d": [271, 272, 340, 285], "page": 1},
 {"key": "issued_shares", "value": "60,000 주", "bbox_2d": [206, 366, 267, 378], "page": 1},
 {"key": "common_shares", "value": "60,000 주", "bbox_2d": [183, 380, 244, 393], "page": 1},
 {"key": "capital", "value": "금 300,000,000 원", "bbox_2d": [560, 373, 676, 386], "page": 1},
 {"key": "capital_change.changed", "value": "2021.03.20 변경", "bbox_2d": [786, 367, 877, 378], "page": 1},
 {"key": "capital_change.registered", "value": "2021.03.26 등기", "bbox_2d": [786, 380, 877, 390], "page": 1},
 {"key": "established", "value": "2020 년 06 월 15 일", "bbox_2d": [271, 50, 398, 62], "page": 2},
 {"key": "opening_reason", "value": "설립", "bbox_2d": [271, 78, 302, 91], "page": 2},
 {"key": "opening_date", "value": "2020 년 06 월 15 일", "bbox_2d": [318, 78, 444, 91], "page": 2},
 {"key": "fee", "value": "1,000원", "bbox_2d": [116, 128, 162, 139], "page": 2},
 {"key": "jurisdiction", "value": "제주지방법원 등기과", "bbox_2d": [513, 128, 644, 139], "page": 2},
 {"key": "issue_date", "value": "서기 2025년 03월 26일", "bbox_2d": [425, 163, 575, 176], "page": 2},
 {"key": "issue_no", "value": "8065263136035593", "bbox_2d": [130, 258, 243, 268], "page": 2},
 {"key": "confirm_no", "value": "DJHS-S1CW-K9C1", "bbox_2d": [519, 258, 632, 268], "page": 2},
 {"key": "issue_date_short", "value": "2025/03/26", "bbox_2d": [865, 258, 929, 268], "page": 2}]
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
- seal.issuer: 발급기관직인 (도장)
```

답:

```json
[{"key": "seal.issuer", "value": true, "bbox_2d": [756, 163, 812, 202], "page": 2}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 '본점' 열이 있는 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 항목명)
- address: 본점
```

답:

```json
{
 "columns": [
  "address"
 ],
 "rows": [
  [
   "제주특별자치도 제주시 중앙로 81-2, 20층 (아라동, 글로벌오피스텔)"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    271,
    178,
    724,
    191
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
[{"columns": ["본점"], "bbox_2d": [72, 174, 724, 226], "page": 1, "n_rows": 1},
 {"columns": ["보통주식", "발행주식의총수", "자본금의액"], "bbox_2d": [72, 291, 736, 357], "page": 1, "n_rows": 1},
 {"columns": ["목적"], "bbox_2d": [72, 399, 928, 520], "page": 1, "n_rows": 7},
 {"columns": ["직위", "성명", "주민등록번호", "취임일", "퇴임일", "주소", "취임구분", "퇴임구분", "등기일", "등기일"], "bbox_2d": [72, 527, 928, 917], "page": 1, "n_rows": 12}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[72, 174, 724, 226] 위치의 표를 보고 답하세요. 표의 행은 모두 몇 개입니까? 머리글·합계 행과 모두 빈 행은 세지 않습니다. (숫자만 답하세요)
```

답:

```json
1
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '발행주식의총수'·'자본금의액' 열이 있는 표를 보고 답하세요. '보통주식' 칸이 '6,000 주'인 행의 '발행주식의총수' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"6,000 주"
```

### 표 그대로 옮기기 `table_read` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[72, 399, 928, 520] 위치의 표를 머리글까지 그대로 옮겨 JSON 으로 답하세요.
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
  "목 적",
  "목 적"
 ],
 "rows": [
  [
   "1. 기초 화학물질 제조업 2. 합성수지 및 플라스틱 제품 제조업 3. 화학제품 도소매업 4. 도료 및 접착제 제조업 5. 화학제품 수출입업 6. 환경 관련 약품 제조 및 판매업 7. 위 각 호와 관련된 부대사업 일체",
   null
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    72,
    420,
    928,
    526
   ],
   "page": 1
  }
 ]
}
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa corporate_registry --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check corporate_registry` → `python -m docgen.formdir card corporate_registry` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa corporate_registry --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions corporate_registry --show` · `python -m docgen.preview corporate_registry --out work/corporate_registry`
