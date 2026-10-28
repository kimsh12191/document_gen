# 재무제표(재무상태표·손익계산서) (`financial_statements`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card financial_statements · card-hash: 7b8726648848 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** corporate · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 재무제표(재무상태표·손익계산서)
- **쓰이는 업무:** 법인 여신
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 최근 결산 2개년 비교 재무상태표 + 손익계산서 (일반기업회계기준 과목 배열, 자산 = 부채 + 자본).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/corporate.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 32칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `current_term` | 당기 | text | 1쪽 [388, 56, 456, 69] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:40 | 묻기 |
| `bs_current_date` | 당기말 | text | 1쪽 [463, 56, 612, 69] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:15 | 묻기 |
| `prior_term` | 전기 | text | 1쪽 [388, 70, 456, 83] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:55 | 묻기 |
| `bs_prior_date` | 전기말 | text | 1쪽 [463, 70, 612, 83] | 늘 | 템플릿 | generate.py | look/template.html.j2:38 · fields.json:20 | 묻기 |
| `corp.name` ← `company_name` | 회사명 | text | 1쪽 [124, 89, 226, 101] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:35 | 묻기 |
| `unit` | 단위 | text | 1쪽 [850, 89, 933, 101] | 늘 | 템플릿 | generate.py | look/template.html.j2:39 · fields.json:75 | 묻기 |
| `assets.*.account` | 과목 | text | 1쪽 [76, 144, 156, 156] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:105 | 묻기 |
| `assets.*.current` | 당기 | amount | 1쪽 [582, 144, 648, 156] (1행) | 늘 | 템플릿 | generate.py | fields.json:110 | 묻기 |
| `assets.*.prior` | 전기 | number | 1쪽 [859, 144, 924, 156] (1행) | 늘 | 템플릿 | generate.py | fields.json:115 | 묻기 |
| `liabilities.*.account` | 과목 | text | 1쪽 [76, 418, 156, 429] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:165 | 묻기 |
| `liabilities.*.current` | 당기 | amount | 1쪽 [582, 418, 648, 429] (1행) | 늘 | 템플릿 | generate.py | fields.json:170 | 묻기 |
| `liabilities.*.prior` | 전기 | number | 1쪽 [866, 418, 924, 429] (1행) | 늘 | 템플릿 | generate.py | fields.json:175 | 묻기 |
| `equity.*.account` | 과목 | text | 1쪽 [76, 542, 141, 554] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:125 | 묻기 |
| `equity.*.current` | 당기 | amount | 1쪽 [600, 542, 648, 554] (1행) | 늘 | 템플릿 | generate.py | fields.json:130 | 묻기 |
| `equity.*.prior` | 전기 | number | 1쪽 [877, 542, 924, 554] (1행) | 늘 | 템플릿 | generate.py | fields.json:135 | 묻기 |
| `total_liabilities_equity.current` | 부채와자본총계(당기) | amount | 1쪽 [582, 606, 648, 618] | 늘 | 템플릿 | generate.py | look/template.html.j2:50 · fields.json:65 | 묻기 |
| `total_liabilities_equity.prior` | 부채와자본총계(전기) | number | 1쪽 [859, 606, 924, 618] | 늘 | 템플릿 | generate.py | look/template.html.j2:50 · fields.json:70 | 묻기 |
| `is_current_period` | 당기회계기간 | text | 1쪽 [391, 657, 684, 669] | 늘 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:45 | 묻기 |
| `is_prior_period` | 전기회계기간 | text | 1쪽 [391, 671, 684, 683] | 늘 | 템플릿 | generate.py | look/template.html.j2:54 · fields.json:50 | 묻기 |
| `income_statement.*.account` | 과목 | text | 1쪽 [76, 732, 141, 744] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:145 | 묻기 |
| `income_statement.*.current` | 당기 | amount | 1쪽 [582, 732, 648, 744] (1행) | 늘 | 템플릿 | generate.py | fields.json:150 | 묻기 |
| `income_statement.*.prior` | 전기 | number | 1쪽 [859, 732, 924, 744] (1행) | 늘 | 템플릿 | generate.py | fields.json:155 | 묻기 |
| `certify_date` | 확인일 | - | - | 4/16 | 템플릿 | generate.py | look/template.html.j2:78 · fields.json:30 | 묻기 |
| `ceo` | 대표이사 | - | - | 4/16 | 템플릿 | generate.py | fields.json:25 | 묻기 |
| `appropriation_date_current` | 처분일 | - | - | 4/16 | 템플릿 | generate.py | look/template.html.j2:74 · fields.json:5 | 묻기 |
| `appropriation_date_prior` | 처분일 | - | - | 4/16 | 템플릿 | generate.py | look/template.html.j2:74 · fields.json:10 | 묻기 |
| `appropriation.*.account` | 과목 | - | - (1행) | 4/16 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:85 | 묻기 |
| `appropriation.*.current` | 당기 | - | - (1행) | 4/16 | 템플릿 | generate.py | fields.json:90 | 묻기 |
| `appropriation.*.prior` | 전기 | - | - (1행) | 4/16 | 템플릿 | generate.py | fields.json:95 | 묻기 |
| `manufacturing_cost.*.account` | 과목 | - | - (1행) | 2/16 | 템플릿 | generate.py | look/template.html.j2:28 · fields.json:185 | 묻기 |
| `manufacturing_cost.*.current` | 당기 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:190 | 묻기 |
| `manufacturing_cost.*.prior` | 전기 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:195 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.corp` | 법인인감 | 도장 | - | 4/16 | 템플릿 | generate.py | fields.json:60 | 묻기 |

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
"재무제표(재무상태표·손익계산서)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "제 5(당)기",
 "2024년 12월 31일 현재",
 "제 4(전)기",
 "2023년 12월 31일 현재",
 "(주)미래케미칼",
 "(단위 : 천원)",
 "Ⅰ. 유동자산",
 "17,074,325",
 "10,601,237",
 "(1) 당좌자산",
 "11,506,187",
 "8,642,403",
 "현금및현금성자산",
 "7,122,285",
 "5,072,999",
 "매출채권",
 "2,914,042",
 "1,328,659",
 "대손충당금",
 "(17,065)",
 "(8,831)",
 "선급금",
 "1,486,925",
 "2,249,576",
 "(2) 재고자산",
 "5,568,138",
 "1,958,834",
 "제품",
 "4,299,887",
 "1,439,997",
 "원재료",
 "1,268,251",
 "518,837",
 "Ⅱ. 비유동자산",
 "33,028,637",
 "15,694,024",
 "(1) 유형자산",
 "23,858,427",
 "13,826,976",
 "토지",
 "12,399,243",
 "5,206,078",
 "기계장치",
 "8,008,061",
 "4,579,669",
 "감가상각누계액",
 "(1,583,564)",
 "(1,197,862)",
 "차량운반구",
 "7,874,678",
 "7,409,148",
 "(2,839,991)",
 "(2,170,057)",
 "(2) 무형자산",
 "1,402,025",
 "475,748",
 "개발비",
 "(3) 기타비유동자산",
 "7,768,185",
 "1,391,300",
 "임차보증금",
 "자산총계",
 "50,102,962",
 "26,295,261",
 "Ⅰ. 유동부채",
 "10,881,199",
 "6,641,875",
 "매입채무",
 "5,190,868",
 "3,417,666",
 "미지급금",
 "2,336,763",
 "817,239",
 "예수금",
 "1,581,994",
 "906,986",
 "단기차입금",
 "1,771,574",
 "1,499,984",
 "Ⅱ. 비유동부채",
 "21,458,426",
 "9,194,615",
 "장기차입금",
 "12,680,737",
 "6,050,458",
 "퇴직급여충당부채",
 "8,777,689",
 "3,144,157",
 "부채총계",
 "32,339,625",
 "15,836,490",
 "Ⅰ. 자본금",
 "300,000",
 "보통주자본금",
 "Ⅱ. 이익잉여금",
 "17,463,337",
 "10,158,771",
 "미처분이익잉여금",
 "자본총계",
 "17,763,337",
 "10,458,771",
 "2024년 01월 01일부터 2024년 12월 31일까지",
 "2023년 01월 01일부터 2023년 12월 31일까지",
 "Ⅰ. 매출액",
 "73,589,000",
 "63,001,998",
 "제품매출",
 "Ⅱ. 매출원가",
 "58,167,100",
 "53,190,998",
 "Ⅲ. 매출총이익",
 "15,421,900",
 "9,811,000",
 "Ⅳ. 판매비와관리비",
 "6,989,386",
 "6,283,433",
 "Ⅴ. 영업이익(손실)",
 "8,432,514",
 "3,527,567",
 "Ⅵ. 영업외수익",
 "757,932",
 "358,370",
 "이자수익",
 "448,064",
 "252,740",
 "Ⅶ. 영업외비용",
 "1,162,609",
 "1,178,691",
 "이자비용",
 "965,591",
 "903,607",
 "Ⅷ. 법인세비용차감전순이익(손실)",
 "8,027,837",
 "2,707,246",
 "Ⅸ. 법인세비용",
 "723,271",
 "281,105",
 "Ⅹ. 당기순이익(손실)",
 "7,304,566",
 "2,426,141"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"원재료"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"252,740"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- current_term: 당기 (같은 항목명 중 1번째 칸)
- corp.name: 회사명 (법인·사업자 상호)
- assets.0.current: 당기 (1행)
- assets.2.account: 과목 (3행)
- assets.7.prior: 전기 (8행)
- assets.8.prior: 전기 (9행)
- assets.9.prior: 전기 (10행)
- assets.10.prior: 전기 (11행)
- assets.11.current: 당기 (12행)
- assets.12.current: 당기 (13행)
- assets.13.account: 과목 (14행)
- assets.14.current: 당기 (15행)
- assets.16.account: 과목 (17행)
- assets.19.current: 당기 (20행)
- assets.20.current: 당기 (21행)
- liabilities.1.account: 과목 (2행)
- liabilities.1.prior: 전기 (2행)
- liabilities.2.account: 과목 (3행)
- liabilities.2.prior: 전기 (3행)
- liabilities.3.account: 과목 (4행)
- liabilities.5.account: 과목 (6행)
- liabilities.6.current: 당기 (7행)
- liabilities.6.prior: 전기 (7행)
- liabilities.8.current: 당기 (9행)
- equity.0.account: 과목 (1행)
- equity.1.account: 과목 (2행)
- equity.2.current: 당기 (3행)
- equity.4.prior: 전기 (5행)
- total_liabilities_equity.prior: 부채와자본총계(전기)
- is_current_period: 당기회계기간
- is_prior_period: 전기회계기간
- income_statement.1.account: 과목 (2행)
- income_statement.1.current: 당기 (2행)
- income_statement.2.prior: 전기 (3행)
- income_statement.4.account: 과목 (5행)
- income_statement.7.account: 과목 (8행)
- income_statement.8.current: 당기 (9행)
- income_statement.10.current: 당기 (11행)
- income_statement.10.prior: 전기 (11행)
- income_statement.11.prior: 전기 (12행)
```

답:

```json
[{"key": "current_term", "value": "제 5(당)기", "bbox_2d": [388, 56, 456, 69], "page": 1},
 {"key": "corp.name", "value": "(주)미래케미칼", "bbox_2d": [124, 89, 226, 101], "page": 1},
 {"key": "assets.0.current", "value": "17,074,325", "bbox_2d": [582, 144, 648, 156], "page": 1},
 {"key": "assets.2.account", "value": "현금및현금성자산", "bbox_2d": [106, 169, 223, 181], "page": 1},
 {"key": "assets.7.prior", "value": "1,439,997", "bbox_2d": [728, 231, 786, 242], "page": 1},
 {"key": "assets.8.prior", "value": "518,837", "bbox_2d": [739, 243, 786, 255], "page": 1},
 {"key": "assets.9.prior", "value": "15,694,024", "bbox_2d": [859, 256, 924, 267], "page": 1},
 {"key": "assets.10.prior", "value": "13,826,976", "bbox_2d": [859, 268, 924, 280], "page": 1},
 {"key": "assets.11.current", "value": "12,399,243", "bbox_2d": [443, 280, 509, 292], "page": 1},
 {"key": "assets.12.current", "value": "8,008,061", "bbox_2d": [451, 293, 509, 304], "page": 1},
 {"key": "assets.13.account", "value": "감가상각누계액", "bbox_2d": [106, 305, 208, 317], "page": 1},
 {"key": "assets.14.current", "value": "7,874,678", "bbox_2d": [451, 318, 509, 329], "page": 1},
 {"key": "assets.16.account", "value": "(2) 무형자산", "bbox_2d": [86, 342, 165, 354], "page": 1},
 {"key": "assets.19.current", "value": "7,768,185", "bbox_2d": [451, 380, 509, 391], "page": 1},
 {"key": "assets.20.current", "value": "50,102,962", "bbox_2d": [582, 393, 648, 404], "page": 1},
 {"key": "liabilities.1.account", "value": "매입채무", "bbox_2d": [106, 430, 164, 441], "page": 1},
 {"key": "liabilities.1.prior", "value": "3,417,666", "bbox_2d": [728, 430, 786, 441], "page": 1},
 {"key": "liabilities.2.account", "value": "미지급금", "bbox_2d": [106, 442, 164, 454], "page": 1},
 {"key": "liabilities.2.prior", "value": "817,239", "bbox_2d": [739, 442, 786, 454], "page": 1},
 {"key": "liabilities.3.account", "value": "예수금", "bbox_2d": [106, 455, 150, 466], "page": 1},
 {"key": "liabilities.5.account", "value": "Ⅱ. 비유동부채", "bbox_2d": [76, 480, 171, 491], "page": 1},
 {"key": "liabilities.6.current", "value": "12,680,737", "bbox_2d": [443, 492, 509, 503], "page": 1},
 {"key": "liabilities.6.prior", "value": "6,050,458", "bbox_2d": [728, 492, 786, 503], "page": 1},
 {"key": "liabilities.8.current", "value": "32,339,625", "bbox_2d": [582, 518, 648, 529], "page": 1},
 {"key": "equity.0.account", "value": "Ⅰ. 자본금", "bbox_2d": [76, 542, 141, 554], "page": 1},
 {"key": "equity.1.account", "value": "보통주자본금", "bbox_2d": [106, 555, 193, 566], "page": 1},
 {"key": "equity.2.current", "value": "17,463,337", "bbox_2d": [582, 567, 648, 579], "page": 1},
 {"key": "equity.4.prior", "value": "10,458,771", "bbox_2d": [859, 593, 924, 604], "page": 1},
 {"key": "total_liabilities_equity.prior", "value": "26,295,261", "bbox_2d": [859, 606, 924, 618], "page": 1},
 {"key": "is_current_period", "value": "2024년 01월 01일부터 2024년 12월 31일까지", "bbox_2d": [391, 657, 684, 669], "page": 1},
 {"key": "is_prior_period", "value": "2023년 01월 01일부터 2023년 12월 31일까지", "bbox_2d": [391, 671, 684, 683], "page": 1},
 {"key": "income_statement.1.account", "value": "제품매출", "bbox_2d": [106, 745, 164, 756], "page": 1},
 {"key": "income_statement.1.current", "value": "73,589,000", "bbox_2d": [443, 745, 509, 756], "page": 1},
 {"key": "income_statement.2.prior", "value": "53,190,998", "bbox_2d": [859, 757, 924, 769], "page": 1},
 {"key": "income_statement.4.account", "value": "Ⅳ. 판매비와관리비", "bbox_2d": [76, 782, 200, 794], "page": 1},
 {"key": "income_statement.7.account", "value": "이자수익", "bbox_2d": [106, 819, 164, 831], "page": 1},
 {"key": "income_statement.8.current", "value": "1,162,609", "bbox_2d": [589, 832, 648, 843], "page": 1},
 {"key": "income_statement.10.current", "value": "8,027,837", "bbox_2d": [589, 856, 648, 868], "page": 1},
 {"key": "income_statement.10.prior", "value": "2,707,246", "bbox_2d": [866, 856, 924, 868], "page": 1},
 {"key": "income_statement.11.prior", "value": "281,105", "bbox_2d": [877, 869, 924, 880], "page": 1}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check financial_statements` → `python -m docgen.formdir card financial_statements` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions financial_statements --show` · `python -m docgen.preview financial_statements --out work/financial_statements`
