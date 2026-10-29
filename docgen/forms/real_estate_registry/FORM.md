# 등기사항전부증명서(집합건물) (`real_estate_registry`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card real_estate_registry · card-hash: e6c4784441f4 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** real_estate · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 등기사항전부증명서(집합건물)
- **쓰이는 업무:** 주택담보대출, 전세자금대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa real_estate_registry --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 등기사항전부증명서(말소사항 포함) - 집합건물. 표제부·갑구·을구.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/real_estate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 29칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `property` | 부동산의표시 | text | 1쪽 [122, 68, 618, 79] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:80 | 묻기 |
| `unique_no` | 고유번호 | text | 1쪽 [839, 68, 950, 79] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:95 | 묻기 |
| `land.display_no` | 표시번호 | number | 1쪽 [80, 272, 87, 283] | 15/16 | 템플릿 | generate.py | look/template.html.j2:121 · fields.json:45 | 묻기 |
| `property.location` ← `land.location` | 소재지번 | text | 1쪽 [121, 272, 315, 283] | 15/16 | 템플릿 | generate.py | look/template.html.j2:122 · fields.json:50 | 묻기 |
| `land.category` | 지목 | text | 1쪽 [615, 272, 628, 283] | 15/16 | 템플릿 | generate.py | look/template.html.j2:123 · fields.json:35 | 묻기 |
| `land.area` | 면적 | text | 1쪽 [718, 272, 780, 283] | 15/16 | 템플릿 | generate.py | look/template.html.j2:124 · fields.json:30 | 묻기 |
| `land.cause` | 등기원인및기타사항 | text | 1쪽 [791, 272, 910, 283] | 15/16 | 템플릿 | generate.py | look/template.html.j2:125 · fields.json:40 | 묻기 |
| `unit.display_no` | 표시번호 | number | 1쪽 [80, 324, 87, 335] | 15/16 | 템플릿 | generate.py | look/template.html.j2:134 · fields.json:110 | 묻기 |
| `unit.receipt` | 접수 | date | 1쪽 [121, 324, 209, 335] | 15/16 | 템플릿 | generate.py | look/template.html.j2:135 · fields.json:115 | 묻기 |
| `unit.unit_no` | 건물번호 | text | 1쪽 [242, 324, 340, 335] | 15/16 | 템플릿 | generate.py | look/template.html.j2:136 · fields.json:120 | 묻기 |
| `unit.detail` | 건물내역 | text | 1쪽 [431, 324, 567, 347] | 15/16 | 템플릿 | generate.py | look/template.html.j2:137 · fields.json:105 | 묻기 |
| `unit.cause` | 등기원인및기타사항 | text | 1쪽 [791, 324, 934, 347] | 15/16 | 템플릿 | generate.py | look/template.html.j2:138 · fields.json:100 | 묻기 |
| `land_right.display_no` | 표시번호 | number | 1쪽 [80, 388, 87, 398] | 15/16 | 템플릿 | generate.py | look/template.html.j2:146 · fields.json:60 | 묻기 |
| `property.kind` ← `land_right.kind` | 대지권종류 | text | 1쪽 [121, 388, 213, 398] | 15/16 | 템플릿 | generate.py | look/template.html.j2:147 · fields.json:65 | 묻기 |
| `land_right.ratio` | 대지권비율 | text | 1쪽 [471, 388, 580, 398] | 15/16 | 템플릿 | generate.py | look/template.html.j2:148 · fields.json:70 | 묻기 |
| `land_right.cause` | 등기원인및기타사항 | text | 1쪽 [753, 388, 886, 410] | 15/16 | 템플릿 | generate.py | look/template.html.j2:149 · fields.json:55 | 묻기 |
| `registry_office` | 관할등기소 | text | 1쪽 [120, 806, 269, 815] | 15/16 | 템플릿 | generate.py | look/template.html.j2:232 · fields.json:85 | 묻기 |
| `view_datetime` | 열람일시 | datetime | 1쪽 [111, 979, 277, 988] | 8/16 | 템플릿 | generate.py | look/template.html.j2:246 · fields.json:125 | 묻기 |
| `fee` | 수수료 | - | - | 7/16 | 템플릿 | generate.py | look/template.html.j2:232 · fields.json:10 | 묻기 |
| `issue_date` | 발행일 | - | - | 7/16 | 템플릿 | generate.py | look/template.html.j2:238 · fields.json:15 | 묻기 |
| `issue_no` | 발행번호 | - | - | 8/16 | 템플릿 | generate.py | look/template.html.j2:248 · fields.json:25 | 묻기 |
| `confirm_no` | 발급확인번호 | - | - | 8/16 | 템플릿 | generate.py | look/template.html.j2:249 · fields.json:5 | 묻기 |
| `issue_date_short` | 발행일 | - | - | 8/16 | 템플릿 | generate.py | look/template.html.j2:249 · fields.json:20 | 묻기 |
| `page_label` | 쪽번호 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:251 · fields.json:75 | 묻기 |
| `gapgu.*.holders.*.role` | 권리자구분 | - | - (1행) | 3/16 | 템플릿 | generate.py | - | 묻기 |
| `gapgu.*.holders.*.share` | 지분 | - | - (1행) | 3/16 | 템플릿 | generate.py | - | 묻기 |
| `gapgu.*.holders.*.name` | 공유자 | - | - (1행) | 3/16 | 템플릿 | generate.py | - | 묻기 |
| `gapgu.*.holders.*.reg_no` | 등록번호 | - | - (1행) | 3/16 | 템플릿 | generate.py | - | 묻기 |
| `gapgu.*.holders.*.address` | 주소 | - | - (1행) | 3/16 | 템플릿 | generate.py | - | 묻기 |

## 표 `buildings` (표 과제 table·table_read·table_find·table_qa) — 5열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `buildings.*.display_no` | 표시번호 | number | 1쪽 [80, 124, 87, 135] (1행) | 15/16 | 템플릿 | generate.py | fields.json:145 | 묻기 |
| `buildings.*.receipt` | 접수 | date | 1쪽 [121, 124, 209, 135] (1행) | 15/16 | 템플릿 | generate.py | fields.json:155 | 묻기 |
| `buildings.*.location` | 소재지번,건물명칭및번호 | text | 1쪽 [242, 124, 480, 147] (1행) | 15/16 | 템플릿 | generate.py | fields.json:150 | 묻기 |
| `buildings.*.detail` | 건물내역 | text | 1쪽 [494, 124, 750, 182] (1행) | 15/16 | 템플릿 | generate.py | fields.json:140 | 묻기 |
| `buildings.*.cause` | 등기원인및기타사항 | text | 1쪽 [791, 124, 934, 147] (1행) | 15/16 | 템플릿 | generate.py | fields.json:135 | 묻기 |

## 표 `gapgu` (표 과제 table·table_read·table_find·table_qa) — 16열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `gapgu.*.rank` | 순위번호 | number | 1쪽 [80, 451, 87, 462] (1행) | 15/16 | 템플릿 | generate.py | fields.json:370 | 묻기 |
| `gapgu.*.purpose` | 등기목적 | text | 1쪽 [121, 451, 189, 462] (1행) | 15/16 | 템플릿 | generate.py | fields.json:365 | 묻기 |
| `gapgu.*.receipt` | 접수 | text | 1쪽 [244, 451, 333, 473] (1행) | 15/16 | 템플릿 | generate.py | fields.json:375 | 묻기 |
| `gapgu.*.holder.role` | 권리자구분 | text | 1쪽 [552, 451, 592, 462] (1행) | 15/16 | 템플릿 | generate.py | fields.json:330 | 묻기 |
| `gapgu.*.holder.name` | 소유자 | text | 1쪽 [599, 451, 735, 462] (1행) | 15/16 | 템플릿 | generate.py | fields.json:315 | 묻기 |
| `gapgu.*.holder.reg_no` | 등록번호 | corp_reg_no | 1쪽 [742, 451, 834, 462] (1행) | 15/16 | 템플릿 | generate.py | fields.json:325 | 묻기 |
| `gapgu.*.holder.address` | 주소 | text | 1쪽 [555, 463, 728, 473] (1행) | 15/16 | 템플릿 | generate.py | fields.json:310 | 묻기 |
| `gapgu.*.cause` | 등기원인 | text | 1쪽 [398, 477, 493, 500] (1행) | 15/16 | 템플릿 | generate.py | fields.json:285 | 묻기 |
| `gapgu.*.trust_no` | 신탁원부 | text | 1쪽 [552, 541, 696, 552] (1행) | 1/16 | 템플릿 | generate.py | fields.json:385 | 묻기 |
| `gapgu.*.holder.note` | 거래가액 | text | 1쪽 [552, 643, 715, 654] (1행) | 14/16 | 템플릿 | generate.py | fields.json:320 | 묻기 |
| `gapgu.*.claim_amount` | 청구금액 | - | - (1행) | 5/16 | 템플릿 | generate.py | fields.json:295 | 묻기 |
| `gapgu.*.creditor` | 채권자 | - | - (1행) | 5/16 | 템플릿 | generate.py | fields.json:300 | 묻기 |
| `gapgu.*.creditor_address` | 채권자주소 | - | - (1행) | 5/16 | 템플릿 | generate.py | fields.json:305 | 묻기 |
| `gapgu.*.change` | 변경사항 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:290 | 묻기 |
| `gapgu.*.note` | 거래가액 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:360 | 묻기 |
| `gapgu.*.right_holder` | 권리자 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:380 | 묻기 |

## 표 `eulgu` (표 과제 table·table_read·table_find·table_qa) — 22열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `eulgu.*.rank` | 순위번호 | number | 1쪽 [80, 695, 87, 705] (1행) | 14/16 | 템플릿 | generate.py | fields.json:250 | 묻기 |
| `eulgu.*.purpose` | 등기목적 | text | 1쪽 [121, 695, 203, 705] (1행) | 14/16 | 템플릿 | generate.py | fields.json:245 | 묻기 |
| `eulgu.*.receipt` | 접수 | text | 1쪽 [244, 695, 326, 717] (1행) | 14/16 | 템플릿 | generate.py | fields.json:255 | 묻기 |
| `eulgu.*.cause` | 등기원인 | text | 1쪽 [398, 695, 480, 717] (1행) | 14/16 | 템플릿 | generate.py | fields.json:165 | 묻기 |
| `eulgu.*.max_amount` | 채권최고액 | amount | 1쪽 [626, 695, 732, 705] (1행) | 14/16 | 템플릿 | generate.py | fields.json:220 | 묻기 |
| `eulgu.*.debtor` | 채무자 | text | 1쪽 [599, 706, 654, 717] (1행) | 14/16 | 템플릿 | generate.py | fields.json:180 | 묻기 |
| `eulgu.*.debtor_address` | 채무자주소 | text | 1쪽 [552, 718, 930, 741] (1행) | 14/16 | 템플릿 | generate.py | fields.json:185 | 묻기 |
| `eulgu.*.mortgagee` | 근저당권자 | text | 1쪽 [626, 742, 831, 752] (1행) | 14/16 | 템플릿 | generate.py | fields.json:225 | 묻기 |
| `eulgu.*.mortgagee_address` | 근저당권자주소 | text | 1쪽 [552, 753, 790, 776] (1행) | 14/16 | 템플릿 | generate.py | fields.json:230 | 묻기 |
| `eulgu.*.change` | 변경사항 | - | - (1행) | 3/16 | 템플릿 | generate.py | fields.json:170 | 묻기 |
| `eulgu.*.deposit` | 임차보증금 / 전세금 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:190 | 묻기 |
| `eulgu.*.rent` | 차임 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:260 | 묻기 |
| `eulgu.*.scope` | 범위 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:270 | 묻기 |
| `eulgu.*.contract_date` | 임대차계약일자 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:175 | 묻기 |
| `eulgu.*.resident_date` | 주민등록일자 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:265 | 묻기 |
| `eulgu.*.possession_date` | 점유개시일자 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:240 | 묻기 |
| `eulgu.*.fixed_date` | 확정일자 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:195 | 묻기 |
| `eulgu.*.lessee` | 임차권자 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:210 | 묻기 |
| `eulgu.*.lessee_address` | 임차권자주소 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:215 | 묻기 |
| `eulgu.*.period` | 존속기간 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:235 | 묻기 |
| `eulgu.*.jeonse_holder` | 전세권자 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:200 | 묻기 |
| `eulgu.*.jeonse_holder_address` | 전세권자주소 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:205 | 묻기 |

## 표 `summary.owners` (표 과제 table·table_read·table_find·table_qa) — 5열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `summary.owners.*.name` | 등기명의인 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:400 | 묻기 |
| `summary.owners.*.reg_no` | (주민)등록번호 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:410 | 묻기 |
| `summary.owners.*.share` | 최종지분 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:415 | 묻기 |
| `summary.owners.*.address` | 주소 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:395 | 묻기 |
| `summary.owners.*.rank` | 순위번호 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:405 | 묻기 |

## 표 `summary.rights` (표 과제 table·table_read·table_find·table_qa) — 5열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `summary.rights.*.rank` | 순위번호 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:435 | 묻기 |
| `summary.rights.*.purpose` | 등기목적 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:430 | 묻기 |
| `summary.rights.*.receipt` | 접수정보 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:440 | 묻기 |
| `summary.rights.*.main` | 주요등기사항 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:425 | 묻기 |
| `summary.rights.*.target_owner` | 대상소유자 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:445 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | 도장 | - | 7/16 | 템플릿 | generate.py | fields.json:90 | 묻기 |

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
"등기사항전부증명서(집합건물)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "서울특별시 서초구 반포동 661 힐스테이트2차아파트 제103동 제13층 제1301호",
 "2268-2012-072040",
 "1",
 "1993년6월28일",
 "서울특별시 서초구 반포동 661 힐스테이트2차아파트 제103동",
 "철근콘크리트벽식구조",
 "(철근)콘크리트지붕 15층 공동주택(아파트)",
 "지하1층 157.94㎡",
 "1층 179.36㎡",
 "2층~15층 각 202.4㎡",
 "도면편철장 제9책 제655장",
 "2",
 "[도로명주소]",
 "서울특별시 서초구 강남대로 357",
 "도로명주소",
 "2012년4월16일 등기",
 "1. 서울특별시 서초구 반포동 661",
 "대",
 "46,962.2㎡",
 "1993년6월28일 등기",
 "제13층 제1301호",
 "74.95㎡",
 "1 소유권대지권",
 "46,962.2분의 46.94",
 "1993년6월12일 대지권",
 "소유권보존",
 "제12168호",
 "소유자",
 "주식회사한양종합건설",
 "131111-2362356",
 "서울특별시 서초구 시청로 60",
 "소유권이전",
 "2004년2월17일",
 "제49924호",
 "2003년12월27일",
 "매매",
 "임채영",
 "501031-*******",
 "서울특별시 노원구 노원로 459-15, 116동 2102호 (중계동, SK뷰리버뷰아파트)",
 "3",
 "2022년6월3일",
 "제19108호",
 "신탁",
 "수탁자",
 "하나자산신탁주식회사",
 "135011-8178151",
 "서울특별시 강남구 테헤란로 132",
 "신탁원부 제2022-3396호",
 "4",
 "2023년10월23일",
 "제23771호",
 "신탁재산의귀속",
 "3번신탁등기말소",
 "5",
 "2025년3월2일",
 "제58118호",
 "2024년12월25일",
 "남궁예태",
 "850328-*******",
 "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)",
 "거래가액 금1,560,000,000원",
 "근저당권설정",
 "제58119호",
 "설정계약",
 "금1,000,800,000원",
 "주식회사국민은행 200111-1603385",
 "서울특별시 영등포구 국제금융로8길 26",
 "(센텀지점)",
 "서울중앙지방법원 등기국",
 "2025년04월01일 13시01분56초"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"금1,000,800,000원"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"주식회사국민은행 200111-1603385"
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
- property: 부동산의표시
- unique_no: 고유번호
- land.display_no: 표시번호 (같은 항목명 중 1번째 칸)
- property.location: 소재지번 (물건 소재지)
- land.category: 지목
- land.area: 면적
- land.cause: 등기원인및기타사항 (같은 항목명 중 1번째 칸)
- unit.display_no: 표시번호 (같은 항목명 중 2번째 칸)
- unit.receipt: 접수
- unit.unit_no: 건물번호
- unit.detail: 건물내역
- unit.cause: 등기원인및기타사항 (같은 항목명 중 2번째 칸)
- land_right.display_no: 표시번호 (같은 항목명 중 3번째 칸)
- property.kind: 대지권종류 (물건 종류)
- land_right.ratio: 대지권비율
- land_right.cause: 등기원인및기타사항 (같은 항목명 중 3번째 칸)
- registry_office: 관할등기소
- view_datetime: 열람일시
```

답:

```json
[{"key": "property", "value": "서울특별시 서초구 반포동 661 힐스테이트2차아파트 제103동 제13층 제1301호", "bbox_2d": [122, 68, 618, 79], "page": 1},
 {"key": "unique_no", "value": "2268-2012-072040", "bbox_2d": [839, 68, 950, 79], "page": 1},
 {"key": "land.display_no", "value": "1", "bbox_2d": [80, 272, 87, 283], "page": 1},
 {"key": "property.location", "value": "1. 서울특별시 서초구 반포동 661", "bbox_2d": [121, 272, 315, 283], "page": 1},
 {"key": "land.category", "value": "대", "bbox_2d": [615, 272, 628, 283], "page": 1},
 {"key": "land.area", "value": "46,962.2㎡", "bbox_2d": [718, 272, 780, 283], "page": 1},
 {"key": "land.cause", "value": "1993년6월28일 등기", "bbox_2d": [791, 272, 910, 283], "page": 1},
 {"key": "unit.display_no", "value": "1", "bbox_2d": [80, 324, 87, 335], "page": 1},
 {"key": "unit.receipt", "value": "1993년6월28일", "bbox_2d": [121, 324, 209, 335], "page": 1},
 {"key": "unit.unit_no", "value": "제13층 제1301호", "bbox_2d": [242, 324, 340, 335], "page": 1},
 {"key": "unit.detail", "value": "철근콘크리트벽식구조\n74.95㎡", "bbox_2d": [431, 324, 567, 347], "page": 1},
 {"key": "unit.cause", "value": "도면편철장 제9책 제655장", "bbox_2d": [791, 324, 934, 347], "page": 1},
 {"key": "land_right.display_no", "value": "1", "bbox_2d": [80, 388, 87, 398], "page": 1},
 {"key": "property.kind", "value": "1 소유권대지권", "bbox_2d": [121, 388, 213, 398], "page": 1},
 {"key": "land_right.ratio", "value": "46,962.2분의 46.94", "bbox_2d": [471, 388, 580, 398], "page": 1},
 {"key": "land_right.cause", "value": "1993년6월12일 대지권\n1993년6월28일 등기", "bbox_2d": [753, 388, 886, 410], "page": 1},
 {"key": "registry_office", "value": "서울중앙지방법원 등기국", "bbox_2d": [120, 806, 269, 815], "page": 1},
 {"key": "view_datetime", "value": "2025년04월01일 13시01분56초", "bbox_2d": [111, 979, 277, 988], "page": 1}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 '접수'·'등기원인및기타사항' 열이 있는 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 항목명)
- display_no: 표시번호
- receipt: 접수
- location: 소재지번,건물명칭및번호
- detail: 건물내역
- cause: 등기원인및기타사항
```

답:

```json
{
 "columns": [
  "display_no",
  "receipt",
  "location",
  "detail",
  "cause"
 ],
 "rows": [
  [
   "1",
   "1993년6월28일",
   "서울특별시 서초구 반포동 661 힐스테이트2차아파트 제103동",
   "철근콘크리트벽식구조 (철근)콘크리트지붕 15층 공동주택(아파트) 지하1층 157.94㎡ 1층 179.36㎡ 2층~15층 각 202.4㎡",
   "도면편철장 제9책 제655장"
  ],
  [
   "2",
   null,
   "서울특별시 서초구 반포동 661 힐스테이트2차아파트 제103동 [도로명주소] 서울특별시 서초구 강남대로 357",
   null,
   "도로명주소 2012년4월16일 등기"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    80,
    124,
    934,
    182
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    80,
    186,
    910,
    231
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
[{"columns": ["표시번호", "접수", "소재지번,건물명칭및번호", "건물내역", "등기원인및기타사항"], "bbox_2d": [51, 107, 949, 231], "page": 1, "n_rows": 2},
 {"columns": ["순위번호", "등기목적", "접수", "등기원인", "권리자구분", "주소", "신탁원부", "거래가액", "소유자", "등록번호"], "bbox_2d": [51, 434, 949, 654], "page": 1, "n_rows": 7},
 {"columns": ["순위번호", "등기목적", "접수", "등기원인", "채무자주소", "근저당권자주소", "채무자", "채권최고액", "근저당권자"], "bbox_2d": [51, 677, 949, 776], "page": 1, "n_rows": 1}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[51, 107, 949, 231] 위치의 표를 보고 답하세요. '표시번호' 칸의 값을 모두 더하면 얼마입니까? 빈 칸은 0 으로 봅니다. (쉼표·단위 없이 숫자만 답하세요)
```

답:

```json
3
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 1쪽 bbox_2d=[51, 107, 949, 231] 위치의 표를 보고 답하세요. 위에서 2번째 행의 '등기원인및기타사항' 값은 무엇입니까? 머리글은 세지 않습니다. (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"도로명주소 2012년4월16일 등기"
```

### 표 그대로 옮기기 `table_read` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[51, 107, 949, 231] 위치의 표를 머리글까지 그대로 옮겨 JSON 으로 답하세요.
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
  "【 표 제 부 】 ( 1동의 건물의 표시 ) > 표시번호",
  "【 표 제 부 】 ( 1동의 건물의 표시 ) > 접 수",
  "【 표 제 부 】 ( 1동의 건물의 표시 ) > 소재지번,건물명칭 및 번호",
  "【 표 제 부 】 ( 1동의 건물의 표시 ) > 건 물 내 역",
  "【 표 제 부 】 ( 1동의 건물의 표시 ) > 등기원인 및 기타사항"
 ],
 "rows": [
  [
   "1",
   "1993년6월28일",
   "서울특별시 서초구 반포동 661 힐스테이트2차아파트 제103동",
   "철근콘크리트벽식구조 (철근)콘크리트지붕 15층 공동주택(아파트) 지하1층 157.94㎡ 1층 179.36㎡ 2층~15층 각 202.4㎡",
   "도면편철장 제9책 제655장"
  ],
  [
   "2",
   null,
   "서울특별시 서초구 반포동 661 힐스테이트2차아파트 제103동 [도로명주소] 서울특별시 서초구 강남대로 357",
   null,
   "도로명주소 2012년4월16일 등기"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    51,
    123,
    949,
    184
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    51,
    184,
    949,
    234
   ],
   "page": 1
  }
 ]
}
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa real_estate_registry --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check real_estate_registry` → `python -m docgen.formdir card real_estate_registry` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa real_estate_registry --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions real_estate_registry --show` · `python -m docgen.preview real_estate_registry --out work/real_estate_registry`
