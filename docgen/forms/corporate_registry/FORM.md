# 법인 등기사항전부증명서(현재 유효사항) (`corporate_registry`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card corporate_registry · card-hash: 6a4d0789eda6 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** corporate · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 법인 등기사항전부증명서(현재 유효사항)
- **쓰이는 업무:** 법인 여신
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 인터넷등기소 발급 법인 등기사항전부증명서.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/corporate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 60칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `issue_type` | 발급구분 | text | 1쪽 [869, 47, 913, 59] | 늘 | generate.py | look/template.html.j2:43 | 묻기 |
| `issue_scope` | 증명서구분 | text | 1쪽 [546, 67, 760, 91] | 늘 | generate.py | look/template.html.j2:45 | 묻기 |
| `reg_no` | 등기번호 | number | 1쪽 [179, 106, 227, 119] | 늘 | generate.py | look/template.html.j2:47 | 묻기 |
| `corp_reg_no` | 등록번호 | corp_reg_no | 1쪽 [179, 128, 288, 140] | 늘 | generate.py | look/template.html.j2:48 | 묻기 |
| `corp.name` ← `company_name` | 상호 | text | 1쪽 [271, 157, 413, 170] | 늘 | generate.py | look/template.html.j2:56 | 묻기 |
| `office_history.*.address` | 본점 | text | 1쪽 [271, 178, 724, 191] (1행) | 1/16 | generate.py | look/template.html.j2:59 | 묻기 |
| `head_office` | 본점 | text | 1쪽 [271, 204, 709, 217] | 늘 | generate.py | look/template.html.j2:61 | 묻기 |
| `head_office_change.changed` | 변경연월일 | text | 1쪽 [806, 198, 896, 209] | 2/16 | generate.py | - | 묻기 |
| `head_office_change.registered` | 등기연월일 | text | 1쪽 [806, 211, 896, 221] | 2/16 | generate.py | - | 묻기 |
| `notice_method` | 공고방법 | text | 1쪽 [271, 230, 709, 243] | 늘 | generate.py | look/template.html.j2:62 | 묻기 |
| `par_value` | 1주의금액 | amount | 1쪽 [271, 251, 344, 264] | 늘 | generate.py | look/template.html.j2:63 | 묻기 |
| `authorized_shares` | 발행할주식의총수 | text | 1쪽 [271, 272, 340, 285] | 늘 | generate.py | look/template.html.j2:64 | 묻기 |
| `capital_history.*.issued_shares` | 발행주식의총수 | text | 1쪽 [206, 330, 260, 343] (1행) | 6/16 | generate.py | - | 묻기 |
| `capital_history.*.common_shares` | 보통주식 | text | 1쪽 [183, 345, 237, 357] (1행) | 6/16 | generate.py | - | 묻기 |
| `capital_history.*.capital` | 자본금의액 | amount | 1쪽 [564, 338, 672, 350] (1행) | 6/16 | generate.py | - | 묻기 |
| `issued_shares` | 발행주식의총수 | text | 1쪽 [206, 366, 267, 378] | 늘 | generate.py | look/template.html.j2:69 | 묻기 |
| `common_shares` | 보통주식 | text | 1쪽 [183, 380, 244, 393] | 늘 | generate.py | look/template.html.j2:69 | 묻기 |
| `capital` | 자본금의액 | amount | 1쪽 [560, 373, 676, 386] | 늘 | generate.py | look/template.html.j2:70 | 묻기 |
| `capital_change.changed` | 변경연월일 | text | 1쪽 [786, 367, 877, 378] | 10/16 | generate.py | - | 묻기 |
| `capital_change.registered` | 등기연월일 | text | 1쪽 [786, 380, 877, 390] | 10/16 | generate.py | - | 묻기 |
| `purposes.*` | 목적 | text | 1쪽 [83, 423, 244, 436] (1행) | 늘 | generate.py | - | 묻기 |
| `officers.*.position` | 직위 | text | 1쪽 [83, 549, 114, 562] (1행) | 늘 | generate.py | - | 묻기 |
| `officers.*.name` | 성명 | text | 1쪽 [122, 549, 168, 562] (1행) | 늘 | generate.py | look/template.html.j2:54 | 묻기 |
| `officers.*.rrn` | 주민등록번호 | rrn | 1쪽 [175, 549, 280, 562] (1행) | 늘 | generate.py | - | 묻기 |
| `officers.*.appointed` | 취임일 | date | 1쪽 [234, 563, 356, 575] (1행) | 늘 | generate.py | - | 묻기 |
| `officers.*.appointment_type` | 취임구분 | text | 1쪽 [359, 563, 389, 575] (1행) | 늘 | generate.py | - | 묻기 |
| `officers.*.registered` | 등기일 | date | 1쪽 [411, 563, 532, 575] (1행) | 늘 | generate.py | look/template.html.j2:39 | 묻기 |
| `officers.*.ended` | 퇴임일 | date | 1쪽 [234, 576, 356, 588] (1행) | 7/16 | generate.py | - | 묻기 |
| `officers.*.end_type` | 퇴임구분 | text | 1쪽 [359, 576, 389, 588] (1행) | 7/16 | generate.py | - | 묻기 |
| `officers.*.end_registered` | 등기일 | date | 1쪽 [411, 576, 532, 588] (1행) | 7/16 | generate.py | - | 묻기 |
| `officers.*.address` | 주소 | text | 1쪽 [334, 622, 862, 635] (1행) | 늘 | generate.py | look/template.html.j2:59 | 묻기 |
| `established` | 회사성립연월일 | date | 2쪽 [271, 50, 398, 62] | 늘 | generate.py | look/template.html.j2:117 | 묻기 |
| `opening_reason` | 등기기록개설사유 | text | 2쪽 [271, 78, 302, 91] | 늘 | generate.py | look/template.html.j2:118 | 묻기 |
| `opening_date` | 등기기록개설일 | date | 2쪽 [318, 78, 444, 91] | 늘 | generate.py | look/template.html.j2:118 | 묻기 |
| `fee` | 수수료 | amount | 2쪽 [116, 128, 162, 139] | 10/16 | generate.py | look/template.html.j2:125 | 묻기 |
| `jurisdiction` | 관할등기소 | text | 2쪽 [513, 128, 644, 139] | 늘 | generate.py | look/template.html.j2:122 | 묻기 |
| `issue_date` | 발행일 | text | 2쪽 [425, 163, 575, 176] | 10/16 | generate.py | look/template.html.j2:128 | 묻기 |
| `issue_no` | 발행번호 | number | 2쪽 [130, 258, 243, 268] | 늘 | generate.py | look/template.html.j2:122 | 묻기 |
| `confirm_no` | 발급확인번호 | text | 2쪽 [519, 258, 632, 268] | 10/16 | generate.py | look/template.html.j2:135 | 묻기 |
| `issue_date_short` | 발행일 | date | 2쪽 [865, 258, 929, 268] | 10/16 | generate.py | look/template.html.j2:135 | 묻기 |
| `viewed_at` | 열람일시 | - | - | 6/16 | generate.py | look/template.html.j2:42 | 묻기 |
| `capital_history.*.changed` | 변경연월일 | - | - (1행) | 4/16 | generate.py | look/template.html.j2:39 | 묻기 |
| `capital_history.*.registered` | 등기연월일 | - | - (1행) | 4/16 | generate.py | look/template.html.j2:39 | 묻기 |
| `branches.*.no` | 지점번호 | - | - (1행) | 4/16 | generate.py | - | 묻기 |
| `branches.*.address` | 지점소재지 | - | - (1행) | 4/16 | generate.py | look/template.html.j2:59 | 묻기 |
| `branches.*.opened` | 설치일 | - | - (1행) | 4/16 | generate.py | - | 묻기 |
| `branches.*.opened_registered` | 등기일 | - | - (1행) | 4/16 | generate.py | - | 묻기 |
| `preferred_shares` | 상환전환우선주식 | - | - | 2/16 | generate.py | look/template.html.j2:69 | 묻기 |
| `purpose_history.*.purposes.*` | 목적 | - | - (1행) | 2/16 | generate.py | - | 묻기 |
| `purpose_change.changed` | 변경연월일 | - | - | 2/16 | generate.py | - | 묻기 |
| `purpose_change.registered` | 등기연월일 | - | - | 2/16 | generate.py | - | 묻기 |
| `branches.*.closed` | 폐지일 | - | - (1행) | 1/16 | generate.py | - | 묻기 |
| `branches.*.closed_registered` | 등기일 | - | - (1행) | 1/16 | generate.py | - | 묻기 |
| `company_name_change.changed` | 변경연월일 | - | - | 3/16 | generate.py | - | 묻기 |
| `company_name_change.registered` | 등기연월일 | - | - | 3/16 | generate.py | - | 묻기 |
| `joint_representation` | 공동대표 | - | - | 2/16 | generate.py | look/template.html.j2:98 | 묻기 |
| `joint_registered` | 등기일 | - | - | 2/16 | generate.py | look/template.html.j2:99 | 묻기 |
| `name_history.*.name` | 상호 | - | - (1행) | 1/16 | generate.py | look/template.html.j2:54 | 묻기 |
| `name_history.*.changed` | 변경연월일 | - | - (1행) | 1/16 | generate.py | look/template.html.j2:39 | 묻기 |
| `name_history.*.registered` | 등기연월일 | - | - (1행) | 1/16 | generate.py | look/template.html.j2:39 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 2쪽 [756, 163, 812, 202] | 10/16 | generate.py | - | 묻기 |

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

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- issue_scope: 증명서구분
- corp_reg_no: 등록번호
- corp.name: 상호 (법인·사업자 상호)
- office_history.0.address: 본점 (1행)
- head_office_change.changed: 변경연월일 (같은 항목명 중 1번째 칸)
- notice_method: 공고방법
- par_value: 1주의금액
- capital_history.0.common_shares: 보통주식 (1행)
- purposes.2: 목적 (3번째)
- purposes.4: 목적 (5번째)
- purposes.6: 목적 (7번째)
- officers.0.registered: 등기일 (1행)
- officers.1.registered: 등기일 (2행)
- officers.2.rrn: 주민등록번호 (3행)
- officers.2.appointment_type: 취임구분 (3행)
- officers.2.registered: 등기일 (3행)
- officers.3.position: 직위 (4행)
- officers.3.appointment_type: 취임구분 (4행)
- officers.3.registered: 등기일 (4행)
- officers.4.name: 성명 (5행)
- officers.4.rrn: 주민등록번호 (5행)
- officers.5.appointed: 취임일 (6행)
- officers.6.appointed: 취임일 (7행)
- officers.6.appointment_type: 취임구분 (7행)
- officers.7.name: 성명 (8행)
- officers.7.rrn: 주민등록번호 (8행)
- officers.7.appointed: 취임일 (8행)
- officers.7.registered: 등기일 (8행)
- officers.8.name: 성명 (9행)
- officers.8.rrn: 주민등록번호 (9행)
- officers.8.appointed: 취임일 (9행)
- officers.9.rrn: 주민등록번호 (10행)
- officers.9.registered: 등기일 (10행)
- officers.10.appointed: 취임일 (11행)
- officers.10.registered: 등기일 (11행)
- officers.11.name: 성명 (12행)
- officers.11.appointed: 취임일 (12행)
- officers.11.appointment_type: 취임구분 (12행)
- officers.11.registered: 등기일 (12행)
- established: 회사성립연월일
```

답:

```json
[{"key": "issue_scope", "value": "말소사항 포함", "bbox_2d": [546, 67, 760, 91], "page": 1},
 {"key": "corp_reg_no", "value": "200112-7951835", "bbox_2d": [179, 128, 288, 140], "page": 1},
 {"key": "corp.name", "value": "주식회사 미래케미칼", "bbox_2d": [271, 157, 413, 170], "page": 1},
 {"key": "office_history.0.address", "value": "제주특별자치도 제주시 중앙로 81-2, 20층 (아라동, 글로벌오피스텔)", "bbox_2d": [271, 178, 724, 191], "page": 1},
 {"key": "head_office_change.changed", "value": "2023.10.09 이전", "bbox_2d": [806, 198, 896, 209], "page": 1},
 {"key": "notice_method", "value": "제주특별자치도 내에서 발행되는 일간 서울경제신문에 게재한다.", "bbox_2d": [271, 230, 709, 243], "page": 1},
 {"key": "par_value", "value": "금 5,000 원", "bbox_2d": [271, 251, 344, 264], "page": 1},
 {"key": "capital_history.0.common_shares", "value": "6,000 주", "bbox_2d": [183, 345, 237, 357], "page": 1},
 {"key": "purposes.2", "value": "3. 화학제품 도소매업", "bbox_2d": [83, 451, 225, 464], "page": 1},
 {"key": "purposes.4", "value": "5. 화학제품 수출입업", "bbox_2d": [83, 480, 225, 492], "page": 1},
 {"key": "purposes.6", "value": "7. 위 각 호와 관련된 부대사업 일체", "bbox_2d": [83, 508, 317, 520], "page": 1},
 {"key": "officers.0.registered", "value": "2020 년 06 월 17 일", "bbox_2d": [411, 563, 532, 575], "page": 1},
 {"key": "officers.1.registered", "value": "2020 년 06 월 19 일", "bbox_2d": [411, 606, 532, 618], "page": 1},
 {"key": "officers.2.rrn", "value": "850328-*******", "bbox_2d": [221, 622, 326, 635], "page": 1},
 {"key": "officers.2.appointment_type", "value": "취임", "bbox_2d": [359, 636, 389, 648], "page": 1},
 {"key": "officers.2.registered", "value": "2020 년 06 월 22 일", "bbox_2d": [411, 636, 532, 648], "page": 1},
 {"key": "officers.3.position", "value": "사내이사", "bbox_2d": [83, 652, 145, 665], "page": 1},
 {"key": "officers.3.appointment_type", "value": "취임", "bbox_2d": [359, 666, 389, 678], "page": 1},
 {"key": "officers.3.registered", "value": "2020 년 06 월 25 일", "bbox_2d": [411, 666, 532, 678], "page": 1},
 {"key": "officers.4.name", "value": "원순수", "bbox_2d": [122, 682, 168, 695], "page": 1},
 {"key": "officers.4.rrn", "value": "910616-*******", "bbox_2d": [175, 682, 280, 695], "page": 1},
 {"key": "officers.5.appointed", "value": "2021 년 11 월 04 일", "bbox_2d": [234, 726, 355, 737], "page": 1},
 {"key": "officers.6.appointed", "value": "2022 년 05 월 26 일", "bbox_2d": [234, 756, 356, 767], "page": 1},
 {"key": "officers.6.appointment_type", "value": "취임", "bbox_2d": [359, 756, 389, 767], "page": 1},
 {"key": "officers.7.name", "value": "하혁승", "bbox_2d": [152, 772, 198, 784], "page": 1},
 {"key": "officers.7.rrn", "value": "820702-*******", "bbox_2d": [206, 772, 311, 784], "page": 1},
 {"key": "officers.7.appointed", "value": "2023 년 06 월 15 일", "bbox_2d": [234, 786, 356, 797], "page": 1},
 {"key": "officers.7.registered", "value": "2023 년 06 월 18 일", "bbox_2d": [411, 786, 532, 797], "page": 1},
 {"key": "officers.8.name", "value": "남궁예태", "bbox_2d": [152, 802, 214, 814], "page": 1},
 {"key": "officers.8.rrn", "value": "850328-*******", "bbox_2d": [221, 802, 326, 814], "page": 1},
 {"key": "officers.8.appointed", "value": "2023 년 06 월 15 일", "bbox_2d": [234, 816, 356, 827], "page": 1},
 {"key": "officers.9.rrn", "value": "850328-*******", "bbox_2d": [221, 832, 326, 844], "page": 1},
 {"key": "officers.9.registered", "value": "2023 년 06 월 22 일", "bbox_2d": [411, 846, 532, 857], "page": 1},
 {"key": "officers.10.appointed", "value": "2024 년 10 월 02 일", "bbox_2d": [234, 875, 356, 887], "page": 1},
 {"key": "officers.10.registered", "value": "2024 년 10 월 14 일", "bbox_2d": [411, 875, 532, 887], "page": 1},
 {"key": "officers.11.name", "value": "원승호", "bbox_2d": [152, 891, 198, 904], "page": 1},
 {"key": "officers.11.appointed", "value": "2024 년 11 월 04 일", "bbox_2d": [234, 905, 355, 917], "page": 1},
 {"key": "officers.11.appointment_type", "value": "중임", "bbox_2d": [359, 905, 388, 917], "page": 1},
 {"key": "officers.11.registered", "value": "2024 년 11 월 07 일", "bbox_2d": [410, 905, 531, 917], "page": 1},
 {"key": "established", "value": "2020 년 06 월 15 일", "bbox_2d": [271, 50, 398, 62], "page": 2}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [756, 163, 812, 202], "page": 2}]
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

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions corporate_registry --show` · `python -m docgen.preview corporate_registry --out work/corporate_registry`
