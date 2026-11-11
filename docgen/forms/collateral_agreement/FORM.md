# 근저당권설정계약서 (`collateral_agreement`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card collateral_agreement · card-hash: 3f71d87cd429 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 근저당권설정계약서 (다른 이름: 근저당권설정계약서(근담보용))
- **질문·답:** 이 폴더의 `questions.json` 에서 바꾼 것이 있음 (아래 ← 바꿈)
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa collateral_agreement --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 주택담보대출용 근저당권설정계약서 (개인).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `questions.json` | 기본 과제의 질문 문장·답 틀 (기본과 다른 것만) |
| `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 33칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank` | 은행명 | text | 1쪽 [101, 41, 198, 64] | 늘 | 템플릿 | generate.py | fields.json:5 | 묻기 |
| `creditor.name` | 채권자겸근저당권자 | text | 1쪽 [73, 134, 199, 147] | 늘 | 템플릿 | generate.py | look/template.html.j2:17 · fields.json:40 | 묻기 |
| `creditor.branch` | 취급점 | text | 1쪽 [282, 135, 340, 147] | 늘 | 템플릿 | generate.py | look/template.html.j2:17 · fields.json:35 | 묻기 |
| `mortgagor.name` | 근저당권설정자 | text | 1쪽 [286, 207, 349, 221] | 늘 | 템플릿 | generate.py | look/template.html.j2:24 · fields.json:75 | 묻기 |
| `mortgagor.rrn` | 실명번호 | rrn | 1쪽 [491, 208, 595, 220] | 늘 | 템플릿 | generate.py | look/template.html.j2:24 · fields.json:80 | 묻기 |
| `mortgagor.address` | 설정자주소 | text | 1쪽 [286, 227, 624, 243] | 늘 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:70 | 묻기 |
| `debtor.name` | 채무자 | text | 1쪽 [286, 249, 349, 262] | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:50 | 묻기 |
| `debtor.address` | 채무자주소 | text | 1쪽 [491, 248, 828, 263] | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:45 | 묻기 |
| `rank` | 순위 | number | 1쪽 [724, 272, 732, 284] | 늘 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:135 | 묻기 |
| `max_amount_korean` | 채권최고액(한글) | amount_korean | 1쪽 [449, 325, 671, 344] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:65 | 묻기 |
| `max_amount` | 채권최고액 | amount | 1쪽 [732, 331, 808, 343] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:60 | 묻기 |
| `scope` | 피담보채무의범위 | text | 1쪽 [234, 360, 310, 372] | 늘 | 템플릿 | generate.py | look/template.html.j2:40 · fields.json:140 | 묻기 |
| `secured_debt` | 피담보채무 | text | 1쪽 [251, 387, 550, 403] | 늘 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:165 | 묻기 |
| `settlement_type` | 결산기유형 | text | 1쪽 [93, 526, 166, 538] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:175 | 묻기 |
| `settlement` | 결산기 | text | 1쪽 [378, 540, 469, 552] | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:170 | 묻기 |
| `property.location` | 소재지 | text | 1쪽 [336, 579, 687, 592] | 늘 | 템플릿 | generate.py | look/template.html.j2:62 · fields.json:110 | 묻기 |
| `property.road_address` | 도로명주소 | text | 1쪽 [336, 600, 553, 612] | 늘 | 템플릿 | generate.py | look/template.html.j2:63 · fields.json:115 | 묻기 |
| `property.structure` | 구조 | text | 1쪽 [336, 621, 489, 633] | 늘 | 템플릿 | generate.py | look/template.html.j2:64 · fields.json:120 | 묻기 |
| `property.floors` | 층수 | text | 1쪽 [801, 621, 831, 633] | 늘 | 템플릿 | generate.py | look/template.html.j2:64 · fields.json:95 | 묻기 |
| `property.unit` | 건물번호 | text | 1쪽 [336, 641, 424, 654] | 늘 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:130 | 묻기 |
| `property.kind` | 건물종류 | text | 1쪽 [801, 641, 846, 654] | 늘 | 템플릿 | generate.py | look/template.html.j2:65 · fields.json:100 | 묻기 |
| `property.exclusive_area` | 전용면적 | text | 1쪽 [336, 662, 386, 675] | 늘 | 템플릿 | generate.py | look/template.html.j2:66 · fields.json:90 | 묻기 |
| `property.land_right` | 대지권 | text | 1쪽 [336, 683, 553, 695] | 늘 | 템플릿 | generate.py | look/template.html.j2:67 · fields.json:105 | 묻기 |
| `property.unique_no` | 고유번호 | text | 1쪽 [220, 704, 337, 716] | 늘 | 템플릿 | generate.py | look/template.html.j2:68 · fields.json:125 | 묻기 |
| `scope_handwritten` | 자필기재(피담보채무범위) | text | - | 늘 | 템플릿 | generate.py | look/template.html.j2:89 · fields.json:145 | 묻기 |
| `handwritten_confirm` | 자필기재(확인) | text | 2쪽 [480, 618, 694, 635] | 늘 | 템플릿 | generate.py | look/template.html.j2:90 · fields.json:55 | 묻기 |
| `contract_date` | 계약일 | date | 2쪽 [88, 664, 187, 676] | 늘 | 템플릿 | generate.py | look/template.html.j2:94 · fields.json:30 | 묻기 |
| `signature_debtor` | 채무자 | text | 2쪽 [799, 652, 860, 664] | 늘 | 템플릿 | generate.py | look/template.html.j2:96 · fields.json:185 | 묻기 |
| `signature_mortgagor` | 근저당권설정자 | text | 2쪽 [799, 675, 860, 688] | 늘 | 템플릿 | generate.py | look/template.html.j2:13 · fields.json:190 | 묻기 |
| `co_mortgagor.name` | 공동설정자 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:15 | 묻기 |
| `co_mortgagor.share` | 지분 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:25 | 묻기 |
| `co_mortgagor.rrn` | 공동설정자실명번호 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:20 | 묻기 |
| `co_mortgagor.address` | 공동설정자주소 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:10 | 묻기 |

## 표 `joint_collateral` (표 과제 table·table_read·table_find·table_qa) — 4열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `joint_collateral.*.kind` | 종류 | text | 1쪽 [140, 768, 172, 781] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:76 · fields.json:205 | 묻기 |
| `joint_collateral.*.location` | 소재지번 | text | 1쪽 [198, 768, 429, 781] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:76 · fields.json:210 | 묻기 |
| `joint_collateral.*.detail` | 지목면적 | text | 1쪽 [490, 768, 561, 781] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:76 · fields.json:200 | 묻기 |
| `joint_collateral.*.unique_no` | 고유번호 | text | 1쪽 [771, 768, 893, 781] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:76 · fields.json:215 | 묻기 |

## 표 `special_terms` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `special_terms.*` | 특약사항 | text | 2쪽 [98, 509, 762, 520] (1행) | 6/16 | 템플릿 | generate.py | - | 묻기 |

## 체크·도장·서명 (marks) — 4칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.debtor` | 채무자 | seal | 2쪽 [884, 646, 927, 670] | 늘 | 템플릿 | generate.py | fields.json:155 | 묻기 |
| `sign.debtor` | 채무자 | signature | 2쪽 [884, 646, 927, 670] | 늘 | 템플릿 | generate.py | fields.json:180 | 묻기 |
| `seal.mortgagor` | 근저당권설정자 | seal | 2쪽 [860, 650, 951, 714] | 늘 | 템플릿 | generate.py | fields.json:160 | 묻기 |
| `seal.co_mortgagor` | 인감 | 도장 | - | 2/16 | 템플릿 | generate.py | fields.json:150 | 묻기 |

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
"근저당권설정계약서"
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
 "주식회사 국민은행",
 "센텀지점",
 "남궁예태",
 "850328-2489940",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "1",
 "금 삼억육천일백만원정",
 "361,000,000",
 "특정근담보",
 "2025년 4월 7일자 대출거래약정서(가계용)",
 "장래지정형",
 "정하지 아니함",
 "서울특별시 서초구 반포동 661 힐스테이트2차아파트",
 "서울특별시 서초구 강남대로 357",
 "철근콘크리트벽식구조",
 "15층",
 "103동 1301호",
 "아파트",
 "74.95㎡",
 "소유권대지권 14,114.0분의 46.94",
 "2268-2012-072040",
 "토지",
 "서울특별시 서초구 반포동 669-21",
 "대 211.0㎡",
 "2759-2002-054633",
 "서울특별시 서초구 반포동 677-13",
 "전 904.6㎡",
 "2114-2023-048770",
 "서울특별시 서초구 반포동 665-37",
 "대 936.6㎡",
 "1942-2010-039093",
 "서울특별시 서초구 반포동 668",
 "답 536.5㎡",
 "1361-2014-086596",
 "서울특별시 서초구 반포동 632",
 "답 622.7㎡",
 "1204-2006-037636",
 "건물",
 "경량철골조 근린생활시설 194.85㎡",
 "2371-2023-035325",
 "서울특별시 서초구 반포동 645-31",
 "답 702.1㎡",
 "1168-1990-093548",
 "서울특별시 서초구 반포동 677",
 "대 772.6㎡",
 "2824-2015-028833",
 "서울특별시 서초구 반포동 653",
 "임야 91.4㎡",
 "1840-1998-012736",
 "서울특별시 서초구 반포동 640",
 "답 867.9㎡",
 "1673-2016-024539",
 "담보물건에 대한 화재보험은 은행을 제1순위 질권자로 하여 가입하고 보험증권 사본을 은행에 제출한다.",
 "설정자는 담보물건의 재건축·리모델링 등 사업계획이 확정된 경우 지체 없이 은행에 통지한다.",
 "채무자가 피담보채무 전액을 상환한 경우에도 결산기 전까지 근저당권은 존속하며, 설정자의 해지 요청 시 은행은 지체 없이 말소에 협조한다.",
 "이 근저당권은 공동담보로서 각 담보물건은 피담보채무 전액을 담보하며, 일부 담보물건의 해지는 은행의 승낙을 받아야 한다.",
 "충분히 설명듣고 이해함",
 "2025년 4월 7일"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"서울특별시 서초구 강남대로 357, 103동 1301호"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"토지"
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
- bank: 은행명
- creditor.name: 채권자겸근저당권자
- creditor.branch: 취급점
- mortgagor.name: 근저당권설정자 (같은 설명 중 1번째 칸)
- mortgagor.rrn: 실명번호
- mortgagor.address: 설정자주소
- debtor.name: 채무자 (같은 설명 중 1번째 칸)
- debtor.address: 채무자주소
- rank: 순위
- max_amount_korean: 채권최고액(한글)
- max_amount: 채권최고액
- scope: 피담보채무의범위
- secured_debt: 피담보채무
- settlement_type: 결산기유형
- settlement: 결산기
- property.location: 소재지
- property.road_address: 도로명주소
- property.structure: 구조
- property.floors: 층수
- property.unit: 건물번호
- property.kind: 건물종류
- property.exclusive_area: 전용면적
- property.land_right: 대지권
- property.unique_no: 고유번호
- scope_handwritten: 자필기재(피담보채무범위)
- handwritten_confirm: 자필기재(확인)
- contract_date: 계약일
- signature_debtor: 채무자 (같은 설명 중 2번째 칸)
- signature_mortgagor: 근저당권설정자 (같은 설명 중 2번째 칸)
```

답:

```json
[{"key": "bank", "value": "국민은행", "bbox_2d": [101, 41, 198, 64], "page": 1},
 {"key": "creditor.name", "value": "주식회사 국민은행", "bbox_2d": [73, 134, 199, 147], "page": 1},
 {"key": "creditor.branch", "value": "센텀지점", "bbox_2d": [282, 135, 340, 147], "page": 1},
 {"key": "mortgagor.name", "value": "남궁예태", "bbox_2d": [286, 207, 349, 221], "page": 1},
 {"key": "mortgagor.rrn", "value": "850328-2489940", "bbox_2d": [491, 208, 595, 220], "page": 1},
 {"key": "mortgagor.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [286, 227, 624, 243], "page": 1},
 {"key": "debtor.name", "value": "남궁예태", "bbox_2d": [286, 249, 349, 262], "page": 1},
 {"key": "debtor.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [491, 248, 828, 263], "page": 1},
 {"key": "rank", "value": "1", "bbox_2d": [724, 272, 732, 284], "page": 1},
 {"key": "max_amount_korean", "value": "금 삼억육천일백만원정", "bbox_2d": [449, 325, 671, 344], "page": 1},
 {"key": "max_amount", "value": "361,000,000", "bbox_2d": [732, 331, 808, 343], "page": 1},
 {"key": "scope", "value": "특정근담보", "bbox_2d": [234, 360, 310, 372], "page": 1},
 {"key": "secured_debt", "value": "2025년 4월 7일자 대출거래약정서(가계용)", "bbox_2d": [251, 387, 550, 403], "page": 1},
 {"key": "settlement_type", "value": "장래지정형", "bbox_2d": [93, 526, 166, 538], "page": 1},
 {"key": "settlement", "value": "정하지 아니함", "bbox_2d": [378, 540, 469, 552], "page": 1},
 {"key": "property.location", "value": "서울특별시 서초구 반포동 661 힐스테이트2차아파트", "bbox_2d": [336, 579, 687, 592], "page": 1},
 {"key": "property.road_address", "value": "서울특별시 서초구 강남대로 357", "bbox_2d": [336, 600, 553, 612], "page": 1},
 {"key": "property.structure", "value": "철근콘크리트벽식구조", "bbox_2d": [336, 621, 489, 633], "page": 1},
 {"key": "property.floors", "value": "15층", "bbox_2d": [801, 621, 831, 633], "page": 1},
 {"key": "property.unit", "value": "103동 1301호", "bbox_2d": [336, 641, 424, 654], "page": 1},
 {"key": "property.kind", "value": "아파트", "bbox_2d": [801, 641, 846, 654], "page": 1},
 {"key": "property.exclusive_area", "value": "74.95㎡", "bbox_2d": [336, 662, 386, 675], "page": 1},
 {"key": "property.land_right", "value": "소유권대지권 14,114.0분의 46.94", "bbox_2d": [336, 683, 553, 695], "page": 1},
 {"key": "property.unique_no", "value": "2268-2012-072040", "bbox_2d": [220, 704, 337, 716], "page": 1},
 {"key": "scope_handwritten", "value": null},
 {"key": "handwritten_confirm", "value": "충분히 설명듣고 이해함", "bbox_2d": [480, 618, 694, 635], "page": 2},
 {"key": "contract_date", "value": "2025년 4월 7일", "bbox_2d": [88, 664, 187, 676], "page": 2},
 {"key": "signature_debtor", "value": "남궁예태", "bbox_2d": [799, 652, 860, 664], "page": 2},
 {"key": "signature_mortgagor", "value": "남궁예태", "bbox_2d": [799, 675, 860, 688], "page": 2}]
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
- seal.debtor: 채무자 (같은 설명 중 1번째 칸, 도장)
- sign.debtor: 채무자 (같은 설명 중 2번째 칸, 서명)
- seal.mortgagor: 근저당권설정자 (도장)
```

답:

```json
[{"key": "seal.debtor", "value": false},
 {"key": "sign.debtor", "value": false},
 {"key": "seal.mortgagor", "value": true, "bbox_2d": [860, 650, 951, 714], "page": 2}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[122, 743, 926, 932] 위치의 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 설명)
- kind: 종류
- location: 소재지번
- detail: 지목면적
- unique_no: 고유번호
```

답:

```json
{
 "columns": [
  "kind",
  "location",
  "detail",
  "unique_no"
 ],
 "rows": [
  [
   "토지",
   "서울특별시 서초구 반포동 669-21",
   "대 211.0㎡",
   "2759-2002-054633"
  ],
  [
   "토지",
   "서울특별시 서초구 반포동 677-13",
   "전 904.6㎡",
   "2114-2023-048770"
  ],
  [
   "토지",
   "서울특별시 서초구 반포동 665-37",
   "대 936.6㎡",
   "1942-2010-039093"
  ],
  [
   "토지",
   "서울특별시 서초구 반포동 668",
   "답 536.5㎡",
   "1361-2014-086596"
  ],
  [
   "토지",
   "서울특별시 서초구 반포동 632",
   "답 622.7㎡",
   "1204-2006-037636"
  ],
  [
   "건물",
   "서울특별시 서초구 반포동 668",
   "경량철골조 근린생활시설 194.85㎡",
   "2371-2023-035325"
  ],
  [
   "토지",
   "서울특별시 서초구 반포동 645-31",
   "답 702.1㎡",
   "1168-1990-093548"
  ],
  [
   "토지",
   "서울특별시 서초구 반포동 677",
   "대 772.6㎡",
   "2824-2015-028833"
  ],
  [
   "토지",
   "서울특별시 서초구 반포동 653",
   "임야 91.4㎡",
   "1840-1998-012736"
  ],
  [
   "토지",
   "서울특별시 서초구 반포동 640",
   "답 867.9㎡",
   "1673-2016-024539"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    140,
    768,
    893,
    781
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    140,
    790,
    892,
    802
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    140,
    811,
    893,
    824
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    140,
    833,
    893,
    845
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    140,
    854,
    893,
    866
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    140,
    879,
    893,
    907
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    140,
    920,
    892,
    932
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    156,
    88,
    893,
    100
   ],
   "page": 2
  },
  {
   "bbox_2d": [
    156,
    109,
    893,
    121
   ],
   "page": 2
  },
  {
   "bbox_2d": [
    156,
    130,
    893,
    143
   ],
   "page": 2
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
[{"columns": ["종류", "소재지번", "지목면적", "고유번호"], "bbox_2d": [122, 743, 926, 932], "page": 1, "n_rows": 7},
 {"columns": ["종류", "소재지번", "지목면적", "고유번호"], "bbox_2d": [139, 62, 926, 143], "page": 2, "n_rows": 3},
 {"columns": ["특약사항"], "bbox_2d": [98, 509, 919, 579], "page": 2, "n_rows": 4}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '지목면적'·'고유번호' 열이 있는 표를 보고 답하세요. 표의 행은 모두 몇 개입니까? 머리글·합계 행과 모두 빈 행은 세지 않습니다. (숫자만 답하세요)
```

답:

```json
10
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 '지목면적'·'고유번호' 열이 있는 표를 보고 답하세요. '종류' 칸이 '토지'인 행은 몇 개입니까? (숫자만 답하세요)
```

답:

```json
9
```

### 표 그대로 옮기기 `table_read` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[74, 764, 926, 937] 위치의 표를 머리글까지 그대로 옮겨 JSON 으로 답하세요.
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
  "번호",
  "종류",
  "소재지번",
  "지목·면적 / 구조·용도",
  "부동산 고유번호"
 ],
 "rows": [
  [
   "2",
   "토지",
   "서울특별시 서초구 반포동 669-21",
   "대 211.0㎡",
   "2759-2002-054633"
  ],
  [
   "3",
   "토지",
   "서울특별시 서초구 반포동 677-13",
   "전 904.6㎡",
   "2114-2023-048770"
  ],
  [
   "4",
   "토지",
   "서울특별시 서초구 반포동 665-37",
   "대 936.6㎡",
   "1942-2010-039093"
  ],
  [
   "5",
   "토지",
   "서울특별시 서초구 반포동 668",
   "답 536.5㎡",
   "1361-2014-086596"
  ],
  [
   "6",
   "토지",
   "서울특별시 서초구 반포동 632",
   "답 622.7㎡",
   "1204-2006-037636"
  ],
  [
   "7",
   "건물",
   "서울특별시 서초구 반포동 868 서울특별시 서초구 반포동 668남궁예",
   "경량철골조 근린생활시설 194.85㎡",
   "2371-2023-035325"
  ],
  [
   "8",
   "토지",
   "서울특별시 서초구 반포동 645-31",
   "답 702.1㎡",
   "1168-1990-093548"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    74,
    764,
    926,
    786
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    74,
    786,
    926,
    807
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    74,
    807,
    926,
    828
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    74,
    828,
    926,
    850
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    74,
    850,
    926,
    871
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    74,
    871,
    926,
    916
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    74,
    916,
    926,
    937
   ],
   "page": 1
  }
 ]
}
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa collateral_agreement --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check collateral_agreement` → `python -m docgen.formdir card collateral_agreement` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa collateral_agreement --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions collateral_agreement --show` · `python -m docgen.preview collateral_agreement --out work/collateral_agreement`
