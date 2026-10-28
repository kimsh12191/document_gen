# 근저당권설정계약서 (`collateral_agreement`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card collateral_agreement · card-hash: 58a372ac721a -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 근저당권설정계약서 (다른 이름: 근저당권설정계약서(근담보용))
- **쓰이는 업무:** 주택담보대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 주택담보대출용 근저당권설정계약서 (개인).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 38칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `bank` | 은행명 | text | 1쪽 [101, 41, 198, 64] | 늘 | 템플릿 | generate.py | fields.json:5 | 묻기 |
| `counterparty.name` ← `creditor.name` | 채권자겸근저당권자 | text | 1쪽 [73, 134, 199, 147] | 늘 | 템플릿 | generate.py | look/template.html.j2:17 · fields.json:40 | 묻기 |
| `creditor.branch` | 취급점 | text | 1쪽 [282, 135, 340, 147] | 늘 | 템플릿 | generate.py | look/template.html.j2:17 · fields.json:35 | 묻기 |
| `related.name` ← `mortgagor.name` | 근저당권설정자 | text | 1쪽 [286, 207, 349, 221] | 늘 | 템플릿 | generate.py | look/template.html.j2:24 · fields.json:75 | 묻기 |
| `related.rrn` ← `mortgagor.rrn` | 실명번호 | rrn | 1쪽 [491, 208, 595, 220] | 늘 | 템플릿 | generate.py | look/template.html.j2:24 · fields.json:80 | 묻기 |
| `related.address` ← `mortgagor.address` | 설정자주소 | text | 1쪽 [286, 227, 624, 243] | 늘 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:70 | 묻기 |
| `customer.name` ← `debtor.name` | 채무자 | text | 1쪽 [286, 249, 349, 262] | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:50 | 묻기 |
| `customer.address` ← `debtor.address` | 채무자주소 | text | 1쪽 [491, 248, 828, 263] | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:45 | 묻기 |
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
| `joint_collateral.*.kind` | 종류 | text | 1쪽 [140, 768, 172, 781] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:76 · fields.json:205 | 묻기 |
| `joint_collateral.*.location` | 소재지번 | text | 1쪽 [198, 768, 429, 781] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:76 · fields.json:210 | 묻기 |
| `joint_collateral.*.detail` | 지목면적 | text | 1쪽 [490, 768, 561, 781] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:76 · fields.json:200 | 묻기 |
| `joint_collateral.*.unique_no` | 고유번호 | text | 1쪽 [771, 768, 893, 781] (1행) | 6/16 | 템플릿 | generate.py | look/template.html.j2:76 · fields.json:215 | 묻기 |
| `special_terms.*` | 특약사항 | text | 2쪽 [98, 509, 762, 520] (1행) | 6/16 | 템플릿 | generate.py | - | 묻기 |
| `scope_handwritten` | 자필기재(피담보채무범위) | text | - | 늘 | 템플릿 | generate.py | look/template.html.j2:89 · fields.json:145 | 묻기 |
| `handwritten_confirm` | 자필기재(확인) | text | 2쪽 [480, 618, 694, 635] | 늘 | 템플릿 | generate.py | look/template.html.j2:90 · fields.json:55 | 묻기 |
| `contract_date` | 계약일 | date | 2쪽 [88, 664, 187, 676] | 늘 | 템플릿 | generate.py | look/template.html.j2:94 · fields.json:30 | 묻기 |
| `signature_debtor` | 채무자 | text | 2쪽 [799, 652, 860, 664] | 늘 | 템플릿 | generate.py | look/template.html.j2:96 · fields.json:185 | 묻기 |
| `signature_mortgagor` | 근저당권설정자 | text | 2쪽 [799, 675, 860, 688] | 늘 | 템플릿 | generate.py | look/template.html.j2:13 · fields.json:190 | 묻기 |
| `co_mortgagor.name` | 공동설정자 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:15 | 묻기 |
| `co_mortgagor.share` | 지분 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:25 | 묻기 |
| `co_mortgagor.rrn` | 공동설정자실명번호 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:20 | 묻기 |
| `co_mortgagor.address` | 공동설정자주소 | - | - | 2/16 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:10 | 묻기 |

## 체크·도장·서명 (marks) — 4칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.customer` ← `seal.debtor` | 채무자 | seal | 2쪽 [884, 646, 927, 670] | 늘 | 템플릿 | generate.py | fields.json:155 | 묻기 |
| `sign.customer` ← `sign.debtor` | 채무자 | signature | 2쪽 [884, 646, 927, 670] | 늘 | 템플릿 | generate.py | fields.json:180 | 묻기 |
| `seal.related` ← `seal.mortgagor` | 근저당권설정자 | seal | 2쪽 [860, 650, 951, 714] | 늘 | 템플릿 | generate.py | fields.json:160 | 묻기 |
| `seal.co_mortgagor` | 인감 | 도장 | - | 2/16 | 템플릿 | generate.py | fields.json:150 | 묻기 |

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
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- counterparty.name: 채권자겸근저당권자 (상대방 성명)
- related.rrn: 실명번호 (보증인·공동 주민등록번호)
- secured_debt: 피담보채무
- settlement: 결산기
- property.location: 소재지 (물건 소재지)
- property.road_address: 도로명주소
- property.kind: 건물종류 (물건 종류)
- property.land_right: 대지권 (물건 대지권)
- joint_collateral.0.location: 소재지번 (1행)
- joint_collateral.0.detail: 지목면적 (1행)
- joint_collateral.0.unique_no: 고유번호 (1행)
- joint_collateral.1.kind: 종류 (2행)
- joint_collateral.1.location: 소재지번 (2행)
- joint_collateral.1.detail: 지목면적 (2행)
- joint_collateral.2.kind: 종류 (3행)
- joint_collateral.2.location: 소재지번 (3행)
- joint_collateral.2.detail: 지목면적 (3행)
- joint_collateral.3.location: 소재지번 (4행)
- joint_collateral.3.detail: 지목면적 (4행)
- joint_collateral.3.unique_no: 고유번호 (4행)
- joint_collateral.4.kind: 종류 (5행)
- joint_collateral.4.location: 소재지번 (5행)
- joint_collateral.5.location: 소재지번 (6행)
- joint_collateral.5.unique_no: 고유번호 (6행)
- joint_collateral.6.kind: 종류 (7행)
- joint_collateral.6.location: 소재지번 (7행)
- joint_collateral.6.detail: 지목면적 (7행)
- joint_collateral.7.unique_no: 고유번호 (8행)
- joint_collateral.8.location: 소재지번 (9행)
- joint_collateral.9.kind: 종류 (10행)
- joint_collateral.9.location: 소재지번 (10행)
- joint_collateral.9.detail: 지목면적 (10행)
- joint_collateral.9.unique_no: 고유번호 (10행)
- special_terms.1: 특약사항 (2번째)
- special_terms.3: 특약사항 (4번째)
- scope_handwritten: 자필기재(피담보채무범위)
- handwritten_confirm: 자필기재(확인)
- contract_date: 계약일
- signature_debtor: 채무자 (같은 항목명 중 2번째 칸)
- signature_mortgagor: 근저당권설정자 (같은 항목명 중 2번째 칸)
```

답:

```json
[{"key": "counterparty.name", "value": "주식회사 국민은행", "bbox_2d": [73, 134, 199, 147], "page": 1},
 {"key": "related.rrn", "value": "850328-2489940", "bbox_2d": [491, 208, 595, 220], "page": 1},
 {"key": "secured_debt", "value": "2025년 4월 7일자 대출거래약정서(가계용)", "bbox_2d": [251, 387, 550, 403], "page": 1},
 {"key": "settlement", "value": "정하지 아니함", "bbox_2d": [378, 540, 469, 552], "page": 1},
 {"key": "property.location", "value": "서울특별시 서초구 반포동 661 힐스테이트2차아파트", "bbox_2d": [336, 579, 687, 592], "page": 1},
 {"key": "property.road_address", "value": "서울특별시 서초구 강남대로 357", "bbox_2d": [336, 600, 553, 612], "page": 1},
 {"key": "property.kind", "value": "아파트", "bbox_2d": [801, 641, 846, 654], "page": 1},
 {"key": "property.land_right", "value": "소유권대지권 14,114.0분의 46.94", "bbox_2d": [336, 683, 553, 695], "page": 1},
 {"key": "joint_collateral.0.location", "value": "서울특별시 서초구 반포동 669-21", "bbox_2d": [198, 768, 429, 781], "page": 1},
 {"key": "joint_collateral.0.detail", "value": "대 211.0㎡", "bbox_2d": [490, 768, 561, 781], "page": 1},
 {"key": "joint_collateral.0.unique_no", "value": "2759-2002-054633", "bbox_2d": [771, 768, 893, 781], "page": 1},
 {"key": "joint_collateral.1.kind", "value": "토지", "bbox_2d": [140, 790, 172, 802], "page": 1},
 {"key": "joint_collateral.1.location", "value": "서울특별시 서초구 반포동 677-13", "bbox_2d": [198, 790, 429, 802], "page": 1},
 {"key": "joint_collateral.1.detail", "value": "전 904.6㎡", "bbox_2d": [490, 790, 561, 802], "page": 1},
 {"key": "joint_collateral.2.kind", "value": "토지", "bbox_2d": [140, 811, 172, 824], "page": 1},
 {"key": "joint_collateral.2.location", "value": "서울특별시 서초구 반포동 665-37", "bbox_2d": [198, 811, 429, 824], "page": 1},
 {"key": "joint_collateral.2.detail", "value": "대 936.6㎡", "bbox_2d": [490, 811, 561, 824], "page": 1},
 {"key": "joint_collateral.3.location", "value": "서울특별시 서초구 반포동 668", "bbox_2d": [198, 833, 408, 845], "page": 1},
 {"key": "joint_collateral.3.detail", "value": "답 536.5㎡", "bbox_2d": [490, 833, 561, 845], "page": 1},
 {"key": "joint_collateral.3.unique_no", "value": "1361-2014-086596", "bbox_2d": [771, 833, 893, 845], "page": 1},
 {"key": "joint_collateral.4.kind", "value": "토지", "bbox_2d": [140, 854, 172, 866], "page": 1},
 {"key": "joint_collateral.4.location", "value": "서울특별시 서초구 반포동 632", "bbox_2d": [198, 854, 408, 866], "page": 1},
 {"key": "joint_collateral.5.location", "value": "서울특별시 서초구 반포동 668", "bbox_2d": [198, 890, 408, 903], "page": 1},
 {"key": "joint_collateral.5.unique_no", "value": "2371-2023-035325", "bbox_2d": [771, 887, 893, 899], "page": 1},
 {"key": "joint_collateral.6.kind", "value": "토지", "bbox_2d": [140, 920, 172, 932], "page": 1},
 {"key": "joint_collateral.6.location", "value": "서울특별시 서초구 반포동 645-31", "bbox_2d": [198, 920, 429, 932], "page": 1},
 {"key": "joint_collateral.6.detail", "value": "답 702.1㎡", "bbox_2d": [490, 920, 561, 932], "page": 1},
 {"key": "joint_collateral.7.unique_no", "value": "2824-2015-028833", "bbox_2d": [772, 88, 893, 100], "page": 2},
 {"key": "joint_collateral.8.location", "value": "서울특별시 서초구 반포동 653", "bbox_2d": [213, 109, 423, 121], "page": 2},
 {"key": "joint_collateral.9.kind", "value": "토지", "bbox_2d": [156, 130, 188, 143], "page": 2},
 {"key": "joint_collateral.9.location", "value": "서울특별시 서초구 반포동 640", "bbox_2d": [213, 130, 423, 143], "page": 2},
 {"key": "joint_collateral.9.detail", "value": "답 867.9㎡", "bbox_2d": [521, 130, 592, 143], "page": 2},
 {"key": "joint_collateral.9.unique_no", "value": "1673-2016-024539", "bbox_2d": [772, 130, 893, 143], "page": 2},
 {"key": "special_terms.1", "value": "설정자는 담보물건의 재건축·리모델링 등 사업계획이 확정된 경우 지체 없이 은행에 통지한다.", "bbox_2d": [98, 524, 698, 535], "page": 2},
 {"key": "special_terms.3", "value": "이 근저당권은 공동담보로서 각 담보물건은 피담보채무 전액을 담보하며, 일부 담보물건의 해지는 은행의 승낙을 받아야 한다.", "bbox_2d": [98, 567, 901, 579], "page": 2},
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
- seal.customer: 채무자 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 채무자 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.related: 근저당권설정자 (보증인·공동 도장, 도장)
```

답:

```json
[{"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": false},
 {"key": "seal.related", "value": true, "bbox_2d": [860, 650, 951, 714], "page": 2}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check collateral_agreement` → `python -m docgen.formdir card collateral_agreement` (실제 질문→답 확인).

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
| 답 모양 | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions collateral_agreement --show` · `python -m docgen.preview collateral_agreement --out work/collateral_agreement`
