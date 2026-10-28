# 등기사항전부증명서(집합건물) (`real_estate_registry`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card real_estate_registry · card-hash: 0c03949f0cc2 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** real_estate · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 등기사항전부증명서(집합건물)
- **쓰이는 업무:** 주택담보대출, 전세자금대출
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 등기사항전부증명서(말소사항 포함) - 집합건물. 표제부·갑구·을구.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/real_estate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 82칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `property` | 부동산의표시 | text | 1쪽 [122, 68, 618, 79] | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:80 | 묻기 |
| `unique_no` | 고유번호 | text | 1쪽 [839, 68, 950, 79] | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:95 | 묻기 |
| `buildings.*.display_no` | 표시번호 | number | 1쪽 [80, 124, 87, 135] (1행) | 15/16 | 템플릿 | generate.py | fields.json:145 | 묻기 |
| `buildings.*.receipt` | 접수 | date | 1쪽 [121, 124, 209, 135] (1행) | 15/16 | 템플릿 | generate.py | fields.json:155 | 묻기 |
| `buildings.*.location` | 소재지번,건물명칭및번호 | text | 1쪽 [242, 124, 480, 147] (1행) | 15/16 | 템플릿 | generate.py | fields.json:150 | 묻기 |
| `buildings.*.detail` | 건물내역 | text | 1쪽 [494, 124, 750, 182] (1행) | 15/16 | 템플릿 | generate.py | fields.json:140 | 묻기 |
| `buildings.*.cause` | 등기원인및기타사항 | text | 1쪽 [791, 124, 934, 147] (1행) | 15/16 | 템플릿 | generate.py | fields.json:135 | 묻기 |
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
| `eulgu.*.rank` | 순위번호 | number | 1쪽 [80, 695, 87, 705] (1행) | 14/16 | 템플릿 | generate.py | fields.json:250 | 묻기 |
| `eulgu.*.purpose` | 등기목적 | text | 1쪽 [121, 695, 203, 705] (1행) | 14/16 | 템플릿 | generate.py | fields.json:245 | 묻기 |
| `eulgu.*.receipt` | 접수 | text | 1쪽 [244, 695, 326, 717] (1행) | 14/16 | 템플릿 | generate.py | fields.json:255 | 묻기 |
| `eulgu.*.cause` | 등기원인 | text | 1쪽 [398, 695, 480, 717] (1행) | 14/16 | 템플릿 | generate.py | fields.json:165 | 묻기 |
| `eulgu.*.max_amount` | 채권최고액 | amount | 1쪽 [626, 695, 732, 705] (1행) | 14/16 | 템플릿 | generate.py | fields.json:220 | 묻기 |
| `eulgu.*.debtor` | 채무자 | text | 1쪽 [599, 706, 654, 717] (1행) | 14/16 | 템플릿 | generate.py | fields.json:180 | 묻기 |
| `eulgu.*.debtor_address` | 채무자주소 | text | 1쪽 [552, 718, 930, 741] (1행) | 14/16 | 템플릿 | generate.py | fields.json:185 | 묻기 |
| `eulgu.*.mortgagee` | 근저당권자 | text | 1쪽 [626, 742, 831, 752] (1행) | 14/16 | 템플릿 | generate.py | fields.json:225 | 묻기 |
| `eulgu.*.mortgagee_address` | 근저당권자주소 | text | 1쪽 [552, 753, 790, 776] (1행) | 14/16 | 템플릿 | generate.py | fields.json:230 | 묻기 |
| `registry_office` | 관할등기소 | text | 1쪽 [120, 806, 269, 815] | 15/16 | 템플릿 | generate.py | look/template.html.j2:232 · fields.json:85 | 묻기 |
| `view_datetime` | 열람일시 | datetime | 1쪽 [111, 979, 277, 988] | 8/16 | 템플릿 | generate.py | look/template.html.j2:246 · fields.json:125 | 묻기 |
| `gapgu.*.claim_amount` | 청구금액 | - | - (1행) | 5/16 | 템플릿 | generate.py | fields.json:295 | 묻기 |
| `gapgu.*.creditor` | 채권자 | - | - (1행) | 5/16 | 템플릿 | generate.py | fields.json:300 | 묻기 |
| `gapgu.*.creditor_address` | 채권자주소 | - | - (1행) | 5/16 | 템플릿 | generate.py | fields.json:305 | 묻기 |
| `eulgu.*.change` | 변경사항 | - | - (1행) | 3/16 | 템플릿 | generate.py | fields.json:170 | 묻기 |
| `fee` | 수수료 | - | - | 7/16 | 템플릿 | generate.py | look/template.html.j2:232 · fields.json:10 | 묻기 |
| `issue_date` | 발행일 | - | - | 7/16 | 템플릿 | generate.py | look/template.html.j2:238 · fields.json:15 | 묻기 |
| `issue_no` | 발행번호 | - | - | 8/16 | 템플릿 | generate.py | look/template.html.j2:248 · fields.json:25 | 묻기 |
| `confirm_no` | 발급확인번호 | - | - | 8/16 | 템플릿 | generate.py | look/template.html.j2:249 · fields.json:5 | 묻기 |
| `issue_date_short` | 발행일 | - | - | 8/16 | 템플릿 | generate.py | look/template.html.j2:249 · fields.json:20 | 묻기 |
| `gapgu.*.change` | 변경사항 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:290 | 묻기 |
| `summary.owners.*.name` | 등기명의인 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:400 | 묻기 |
| `summary.owners.*.reg_no` | (주민)등록번호 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:410 | 묻기 |
| `summary.owners.*.share` | 최종지분 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:415 | 묻기 |
| `summary.owners.*.address` | 주소 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:395 | 묻기 |
| `summary.owners.*.rank` | 순위번호 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:405 | 묻기 |
| `summary.rights.*.rank` | 순위번호 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:435 | 묻기 |
| `summary.rights.*.purpose` | 등기목적 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:430 | 묻기 |
| `summary.rights.*.receipt` | 접수정보 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:440 | 묻기 |
| `summary.rights.*.main` | 주요등기사항 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:425 | 묻기 |
| `summary.rights.*.target_owner` | 대상소유자 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:445 | 묻기 |
| `page_label` | 쪽번호 | - | - | 1/16 | 템플릿 | generate.py | look/template.html.j2:251 · fields.json:75 | 묻기 |
| `gapgu.*.holders.*.role` | 권리자구분 | - | - (1행) | 3/16 | 템플릿 | generate.py | - | 묻기 |
| `gapgu.*.holders.*.share` | 지분 | - | - (1행) | 3/16 | 템플릿 | generate.py | - | 묻기 |
| `gapgu.*.holders.*.name` | 공유자 | - | - (1행) | 3/16 | 템플릿 | generate.py | - | 묻기 |
| `gapgu.*.holders.*.reg_no` | 등록번호 | - | - (1행) | 3/16 | 템플릿 | generate.py | - | 묻기 |
| `gapgu.*.holders.*.address` | 주소 | - | - (1행) | 3/16 | 템플릿 | generate.py | - | 묻기 |
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
| `gapgu.*.note` | 거래가액 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:360 | 묻기 |
| `gapgu.*.right_holder` | 권리자 | - | - (1행) | 1/16 | 템플릿 | generate.py | fields.json:380 | 묻기 |

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

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- property: 부동산의표시
- unique_no: 고유번호
- buildings.0.detail: 건물내역 (1행)
- buildings.1.display_no: 표시번호 (2행)
- buildings.1.location: 소재지번,건물명칭및번호 (2행)
- buildings.1.cause: 등기원인및기타사항 (2행)
- land.area: 면적
- land.cause: 등기원인및기타사항 (같은 항목명 중 3번째 칸)
- land_right.display_no: 표시번호 (같은 항목명 중 5번째 칸)
- property.kind: 대지권종류 (물건 종류)
- land_right.ratio: 대지권비율
- gapgu.0.rank: 순위번호 (1행)
- gapgu.0.holder.name: 소유자 (1행)
- gapgu.1.rank: 순위번호 (2행)
- gapgu.1.holder.reg_no: 등록번호 (2행)
- gapgu.1.holder.address: 주소 (2행)
- gapgu.2.rank: 순위번호 (3행)
- gapgu.2.purpose: 등기목적 (3행)
- gapgu.2.receipt: 접수 (3행)
- gapgu.2.cause: 등기원인 (3행)
- gapgu.2.holder.role: 권리자구분 (3행)
- gapgu.2.holder.name: 소유자 (3행)
- gapgu.2.holder.reg_no: 등록번호 (3행)
- gapgu.2.holder.address: 주소 (3행)
- gapgu.4.rank: 순위번호 (5행)
- gapgu.4.purpose: 등기목적 (5행)
- gapgu.4.receipt: 접수 (5행)
- gapgu.4.cause: 등기원인 (5행)
- gapgu.4.holder.role: 권리자구분 (5행)
- gapgu.4.holder.name: 소유자 (5행)
- gapgu.4.holder.address: 주소 (5행)
- gapgu.5.purpose: 등기목적 (6행)
- gapgu.6.receipt: 접수 (7행)
- gapgu.6.holder.role: 권리자구분 (7행)
- gapgu.6.holder.name: 소유자 (7행)
- gapgu.6.holder.address: 주소 (7행)
- gapgu.6.holder.note: 거래가액 (7행)
- eulgu.0.max_amount: 채권최고액 (1행)
- eulgu.0.mortgagee_address: 근저당권자주소 (1행)
- registry_office: 관할등기소
```

답:

```json
[{"key": "property", "value": "서울특별시 서초구 반포동 661 힐스테이트2차아파트 제103동 제13층 제1301호", "bbox_2d": [122, 68, 618, 79], "page": 1},
 {"key": "unique_no", "value": "2268-2012-072040", "bbox_2d": [839, 68, 950, 79], "page": 1},
 {"key": "buildings.0.detail", "value": "철근콘크리트벽식구조\n(철근)콘크리트지붕 15층 공동주택(아파트)\n지하1층 157.94㎡\n1층 179.36㎡\n2층~15층 각 202.4㎡", "bbox_2d": [494, 124, 750, 182], "page": 1},
 {"key": "buildings.1.display_no", "value": "2", "bbox_2d": [80, 186, 87, 196], "page": 1},
 {"key": "buildings.1.location", "value": "서울특별시 서초구 반포동 661 힐스테이트2차아파트 제103동\n[도로명주소]\n서울특별시 서초구 강남대로 357", "bbox_2d": [242, 186, 480, 231], "page": 1},
 {"key": "buildings.1.cause", "value": "도로명주소\n2012년4월16일 등기", "bbox_2d": [791, 186, 910, 208], "page": 1},
 {"key": "land.area", "value": "46,962.2㎡", "bbox_2d": [718, 272, 780, 283], "page": 1},
 {"key": "land.cause", "value": "1993년6월28일 등기", "bbox_2d": [791, 272, 910, 283], "page": 1},
 {"key": "land_right.display_no", "value": "1", "bbox_2d": [80, 388, 87, 398], "page": 1},
 {"key": "property.kind", "value": "1 소유권대지권", "bbox_2d": [121, 388, 213, 398], "page": 1},
 {"key": "land_right.ratio", "value": "46,962.2분의 46.94", "bbox_2d": [471, 388, 580, 398], "page": 1},
 {"key": "gapgu.0.rank", "value": "1", "bbox_2d": [80, 451, 87, 462], "page": 1},
 {"key": "gapgu.0.holder.name", "value": "주식회사한양종합건설", "bbox_2d": [599, 451, 735, 462], "page": 1},
 {"key": "gapgu.1.rank", "value": "2", "bbox_2d": [80, 477, 87, 488], "page": 1},
 {"key": "gapgu.1.holder.reg_no", "value": "501031-*******", "bbox_2d": [647, 477, 740, 488], "page": 1},
 {"key": "gapgu.1.holder.address", "value": "서울특별시 노원구 노원로 459-15, 116동 2102호 (중계동, SK뷰리버뷰아파트)", "bbox_2d": [552, 489, 938, 511], "page": 1},
 {"key": "gapgu.2.rank", "value": "3", "bbox_2d": [80, 515, 87, 526], "page": 1},
 {"key": "gapgu.2.purpose", "value": "소유권이전", "bbox_2d": [121, 515, 189, 526], "page": 1},
 {"key": "gapgu.2.receipt", "value": "2022년6월3일\n제19108호", "bbox_2d": [244, 515, 326, 537], "page": 1},
 {"key": "gapgu.2.cause", "value": "2022년6월3일\n신탁", "bbox_2d": [398, 515, 480, 537], "page": 1},
 {"key": "gapgu.2.holder.role", "value": "수탁자", "bbox_2d": [552, 515, 592, 526], "page": 1},
 {"key": "gapgu.2.holder.name", "value": "하나자산신탁주식회사", "bbox_2d": [599, 515, 735, 526], "page": 1},
 {"key": "gapgu.2.holder.reg_no", "value": "135011-8178151", "bbox_2d": [742, 515, 834, 526], "page": 1},
 {"key": "gapgu.2.holder.address", "value": "서울특별시 강남구 테헤란로 132", "bbox_2d": [555, 527, 749, 537], "page": 1},
 {"key": "gapgu.4.rank", "value": "4", "bbox_2d": [80, 556, 87, 566], "page": 1},
 {"key": "gapgu.4.purpose", "value": "소유권이전", "bbox_2d": [121, 556, 189, 566], "page": 1},
 {"key": "gapgu.4.receipt", "value": "2023년10월23일\n제23771호", "bbox_2d": [244, 556, 340, 578], "page": 1},
 {"key": "gapgu.4.cause", "value": "2023년10월23일\n신탁재산의귀속", "bbox_2d": [398, 556, 493, 578], "page": 1},
 {"key": "gapgu.4.holder.role", "value": "소유자", "bbox_2d": [552, 556, 592, 566], "page": 1},
 {"key": "gapgu.4.holder.name", "value": "임채영", "bbox_2d": [599, 556, 640, 566], "page": 1},
 {"key": "gapgu.4.holder.address", "value": "서울특별시 노원구 노원로 459-15, 116동 2102호 (중계동, SK뷰리버뷰아파트)", "bbox_2d": [552, 567, 938, 590], "page": 1},
 {"key": "gapgu.5.purpose", "value": "3번신탁등기말소", "bbox_2d": [121, 593, 223, 604], "page": 1},
 {"key": "gapgu.6.receipt", "value": "2025년3월2일\n제58118호", "bbox_2d": [244, 608, 326, 630], "page": 1},
 {"key": "gapgu.6.holder.role", "value": "소유자", "bbox_2d": [552, 608, 592, 618], "page": 1},
 {"key": "gapgu.6.holder.name", "value": "남궁예태", "bbox_2d": [599, 608, 654, 618], "page": 1},
 {"key": "gapgu.6.holder.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호 (반포동, 힐스테이트2차아파트)", "bbox_2d": [552, 620, 930, 642], "page": 1},
 {"key": "gapgu.6.holder.note", "value": "거래가액 금1,560,000,000원", "bbox_2d": [552, 643, 715, 654], "page": 1},
 {"key": "eulgu.0.max_amount", "value": "금1,000,800,000원", "bbox_2d": [626, 695, 732, 705], "page": 1},
 {"key": "eulgu.0.mortgagee_address", "value": "서울특별시 영등포구 국제금융로8길 26\n(센텀지점)", "bbox_2d": [552, 753, 790, 776], "page": 1},
 {"key": "registry_office", "value": "서울중앙지방법원 등기국", "bbox_2d": [120, 806, 269, 815], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

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
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | 필요 없음 |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions real_estate_registry --show` · `python -m docgen.preview real_estate_registry --out work/real_estate_registry`
