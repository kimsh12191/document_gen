# 신용카드 이용대금명세서 (`card_statement`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card card_statement · card-hash: a35e98ec1c36 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** finance · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 신용카드 이용대금명세서
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 카드사 신용카드 이용대금명세서 (일시불·할부·수수료 합계 일관).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/finance.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 30칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `company` | 카드사 | text | 1쪽 [77, 57, 198, 80] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:10 | 묻기 |
| `statement_month` | 청구월 | month | 1쪽 [77, 86, 185, 104] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:35 | 묻기 |
| `member` | 회원명 | text | 1쪽 [198, 125, 256, 136] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:20 | 묻기 |
| `card_no` | 카드번호 | text | 1쪽 [495, 125, 626, 136] | 늘 | 템플릿 | generate.py | look/template.html.j2:19 · fields.json:5 | 묻기 |
| `pay_date` | 결제일 | date | 1쪽 [198, 146, 263, 157] | 늘 | 템플릿 | generate.py | look/template.html.j2:24 · fields.json:30 | 묻기 |
| `pay_account` | 결제계좌 | text | 1쪽 [495, 146, 668, 157] | 늘 | 템플릿 | generate.py | look/template.html.j2:24 · fields.json:25 | 묻기 |
| `usage_period` | 이용기간 | text | 1쪽 [198, 167, 343, 177] | 늘 | 템플릿 | generate.py | look/template.html.j2:25 · fields.json:100 | 묻기 |
| `summary.total` | 청구금액 | amount | 1쪽 [145, 218, 266, 241] | 늘 | 템플릿 | generate.py | look/template.html.j2:27 · fields.json:95 | 묻기 |
| `summary.lump` | 일시불 | number | 1쪽 [597, 197, 655, 208] | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:75 | 묻기 |
| `summary.installment` | 할부 | number | 1쪽 [858, 197, 916, 208] | 늘 | 템플릿 | generate.py | look/template.html.j2:30 · fields.json:65 | 묻기 |
| `summary.cash` | 현금서비스 | amount | 1쪽 [648, 217, 655, 228] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:55 | 묻기 |
| `summary.fee` | 수수료(이자) | amount | 1쪽 [876, 217, 916, 228] | 늘 | 템플릿 | generate.py | look/template.html.j2:31 · fields.json:60 | 묻기 |
| `summary.next_month` | 다음달결제예정금액 | number | 1쪽 [597, 238, 655, 249] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:80 | 묻기 |
| `summary.limit` | 이용한도 | amount | 1쪽 [850, 238, 916, 249] | 늘 | 템플릿 | generate.py | look/template.html.j2:32 · fields.json:70 | 묻기 |
| `summary.overdue` | 연체금액 | number | 1쪽 [597, 259, 655, 269] | 1/16 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:85 | 묻기 |
| `summary.overdue_fee` | 연체이자 | amount | 1쪽 [876, 259, 916, 269] | 1/16 | 템플릿 | generate.py | look/template.html.j2:33 · fields.json:90 | 묻기 |
| `rows.*.date` | 이용일자 | date | 1쪽 [98, 331, 158, 341] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:42 · fields.json:135 | 묻기 |
| `rows.*.merchant` | 이용하신가맹점 | text | 1쪽 [185, 331, 251, 341] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:43 · fields.json:145 | 묻기 |
| `rows.*.amount` | 이용금액 | amount | 1쪽 [401, 331, 444, 341] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:44 · fields.json:130 | 묻기 |
| `rows.*.months` | 할부 | text | 1쪽 [468, 331, 507, 341] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:45 · fields.json:150 | 묻기 |
| `rows.*.seq` | 회차 | text | 1쪽 [544, 331, 574, 341] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:46 · fields.json:160 | 묻기 |
| `rows.*.principal` | 원금 | amount | 1쪽 [661, 331, 697, 341] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:47 · fields.json:155 | 묻기 |
| `rows.*.fee` | 수수료(이자) | amount | 1쪽 [783, 331, 790, 341] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:48 · fields.json:140 | 묻기 |
| `rows.*.after` | 결제후잔액 | number | 1쪽 [880, 331, 917, 341] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:49 · fields.json:125 | 묻기 |
| `sum.amount` | 이용금액합계 | amount | 2쪽 [380, 348, 439, 357] | 늘 | 템플릿 | generate.py | look/template.html.j2:52 · fields.json:40 | 묻기 |
| `sum.principal` | 결제원금합계 | amount | 2쪽 [612, 348, 665, 357] | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:50 | 묻기 |
| `sum.fee` | 수수료합계 | amount | 2쪽 [756, 348, 793, 357] | 늘 | 템플릿 | generate.py | look/template.html.j2:53 · fields.json:45 | 묻기 |
| `fee_rate` | 할부수수료율 | percent | 2쪽 [204, 373, 254, 383] | 늘 | 템플릿 | generate.py | look/template.html.j2:56 · fields.json:15 | 묻기 |
| `fee_per_100.*.months` | 할부개월 | text | 2쪽 [393, 373, 426, 383] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:115 | 묻기 |
| `fee_per_100.*.fee` | 100원당수수료 | amount | 2쪽 [429, 373, 465, 383] (1행) | 늘 | 템플릿 | generate.py | look/template.html.j2:57 · fields.json:110 | 묻기 |

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
"신용카드 이용대금명세서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "롯데카드",
 "2025년 3월",
 "남궁예태",
 "4256-12**-****-8899",
 "2025.03.15",
 "국민은행 478303-**-**6627",
 "2025.02.01 ~ 2025.02.28",
 "7,041,121",
 "1,506,600",
 "3,722,531",
 "0",
 "37,770",
 "3,722,535",
 "15,000,000",
 "1,748,430",
 "25,790",
 "2024.04.13",
 "애플코리아",
 "919,300",
 "12개월",
 "11/12",
 "76,608",
 "76,612",
 "2024.07.24",
 "서울밝은치과의원",
 "2,330,100",
 "8/12",
 "194,175",
 "12,050",
 "776,700",
 "2024.08.27",
 "롯데하이마트",
 "612,500",
 "10개월",
 "7/10",
 "61,250",
 "183,750",
 "2024.11.10",
 "대한항공",
 "1,193,200",
 "6개월",
 "4/6",
 "198,866",
 "397,736",
 "2025.01.19",
 "LG전자베스트샵",
 "467,400",
 "2/12",
 "38,950",
 "5,310",
 "389,500",
 "2025.02.02",
 "다이소",
 "33,580",
 "일시불",
 "-",
 "쿠팡",
 "21,950",
 "2025.02.03",
 "11번가",
 "140,980",
 "NETFLIX.COM (USD 233.93)",
 "326,850",
 "2025.02.05",
 "이마트",
 "16,040",
 "파리바게뜨",
 "45,000",
 "CU",
 "57,810",
 "CGV",
 "4,270",
 "세븐일레븐",
 "6,630",
 "2025.02.06",
 "홈플러스",
 "12,070",
 "삼성디지털프라자",
 "1,424,900",
 "2개월",
 "1/2",
 "712,450",
 "721,500",
 "1/6",
 "120,250",
 "601,250",
 "2025.02.09",
 "무신사",
 "46,870",
 "2025.02.10",
 "2,486,300",
 "3개월",
 "1/3",
 "828,766",
 "1,657,534",
 "46,230",
 "20,740",
 "10,000",
 "2025.02.12",
 "이케아코리아",
 "203,800",
 "67,933",
 "2,530",
 "135,867",
 "2025.02.13",
 "99,300",
 "42,950",
 "2025.02.15",
 "7,430",
 "2025.02.16",
 "46,200",
 "2025.02.18",
 "5,790",
 "GS칼텍스",
 "12,710",
 "2025.02.19",
 "네이버페이",
 "145,100",
 "57,090",
 "2025.02.20",
 "50,540",
 "2025.02.21",
 "14,850",
 "2025.02.23",
 "아시아나항공",
 "1,440,100",
 "480,033",
 "17,880",
 "960,067",
 "8,620",
 "2025.02.24",
 "53,620",
 "15,110",
 "44,770",
 "2025.02.25",
 "52,000",
 "2025.02.26",
 "1,886,500",
 "943,250",
 "2025.02.27",
 "8,270",
 "2025.02.28",
 "교보문고",
 "38,920",
 "14,310",
 "15,192,200",
 "5,229,131",
 "연 14.9%",
 "1.86원",
 "2.48원",
 "4.35원",
 "6.83원",
 "8.07원"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"-"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"일시불"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- rows.1.after: 결제후잔액 (2행)
- rows.3.date: 이용일자 (4행)
- rows.4.date: 이용일자 (5행)
- rows.4.months: 할부 (5행)
- rows.4.principal: 원금 (5행)
- rows.7.merchant: 이용하신가맹점 (8행)
- rows.7.amount: 이용금액 (8행)
- rows.8.merchant: 이용하신가맹점 (9행)
- rows.8.months: 할부 (9행)
- rows.8.after: 결제후잔액 (9행)
- rows.9.months: 할부 (10행)
- rows.9.fee: 수수료(이자) (10행)
- rows.10.date: 이용일자 (11행)
- rows.10.merchant: 이용하신가맹점 (11행)
- rows.10.seq: 회차 (11행)
- rows.11.principal: 원금 (12행)
- rows.14.date: 이용일자 (15행)
- rows.18.months: 할부 (19행)
- rows.20.amount: 이용금액 (21행)
- rows.21.date: 이용일자 (22행)
- rows.22.merchant: 이용하신가맹점 (23행)
- rows.24.after: 결제후잔액 (25행)
- rows.27.principal: 원금 (28행)
- rows.29.merchant: 이용하신가맹점 (30행)
- rows.29.fee: 수수료(이자) (30행)
- rows.31.fee: 수수료(이자) (32행)
- rows.32.date: 이용일자 (33행)
- rows.32.seq: 회차 (33행)
- rows.33.amount: 이용금액 (34행)
- rows.35.amount: 이용금액 (36행)
- rows.36.date: 이용일자 (37행)
- rows.37.months: 할부 (38행)
- rows.38.principal: 원금 (39행)
- rows.40.date: 이용일자 (41행)
- rows.41.seq: 회차 (42행)
- rows.41.fee: 수수료(이자) (42행)
- rows.42.date: 이용일자 (43행)
- fee_rate: 할부수수료율
- fee_per_100.0.months: 할부개월 (1행)
- fee_per_100.1.months: 할부개월 (2행)
```

답:

```json
[{"key": "rows.1.after", "value": "776,700", "bbox_2d": [874, 351, 917, 360], "page": 1},
 {"key": "rows.3.date", "value": "2024.11.10", "bbox_2d": [99, 389, 158, 399], "page": 1},
 {"key": "rows.4.date", "value": "2025.01.19", "bbox_2d": [98, 409, 158, 418], "page": 1},
 {"key": "rows.4.months", "value": "12개월", "bbox_2d": [468, 409, 507, 418], "page": 1},
 {"key": "rows.4.principal", "value": "38,950", "bbox_2d": [661, 409, 697, 418], "page": 1},
 {"key": "rows.7.merchant", "value": "11번가", "bbox_2d": [185, 466, 224, 476], "page": 1},
 {"key": "rows.7.amount", "value": "140,980", "bbox_2d": [401, 466, 444, 476], "page": 1},
 {"key": "rows.8.merchant", "value": "NETFLIX.COM (USD 233.93)", "bbox_2d": [185, 486, 307, 509], "page": 1},
 {"key": "rows.8.months", "value": "일시불", "bbox_2d": [468, 492, 507, 502], "page": 1},
 {"key": "rows.8.after", "value": "0", "bbox_2d": [910, 492, 917, 502], "page": 1},
 {"key": "rows.9.months", "value": "일시불", "bbox_2d": [468, 518, 507, 528], "page": 1},
 {"key": "rows.9.fee", "value": "0", "bbox_2d": [783, 518, 790, 528], "page": 1},
 {"key": "rows.10.date", "value": "2025.02.05", "bbox_2d": [98, 537, 158, 547], "page": 1},
 {"key": "rows.10.merchant", "value": "파리바게뜨", "bbox_2d": [185, 537, 251, 547], "page": 1},
 {"key": "rows.10.seq", "value": "-", "bbox_2d": [557, 537, 561, 547], "page": 1},
 {"key": "rows.11.principal", "value": "57,810", "bbox_2d": [661, 557, 697, 567], "page": 1},
 {"key": "rows.14.date", "value": "2025.02.06", "bbox_2d": [98, 615, 158, 624], "page": 1},
 {"key": "rows.18.months", "value": "3개월", "bbox_2d": [471, 692, 504, 702], "page": 1},
 {"key": "rows.20.amount", "value": "20,740", "bbox_2d": [407, 731, 444, 740], "page": 1},
 {"key": "rows.21.date", "value": "2025.02.10", "bbox_2d": [98, 750, 158, 760], "page": 1},
 {"key": "rows.22.merchant", "value": "이케아코리아", "bbox_2d": [185, 769, 264, 779], "page": 1},
 {"key": "rows.24.after", "value": "0", "bbox_2d": [910, 808, 917, 818], "page": 1},
 {"key": "rows.27.principal", "value": "5,790", "bbox_2d": [667, 866, 697, 876], "page": 1},
 {"key": "rows.29.merchant", "value": "네이버페이", "bbox_2d": [185, 904, 251, 914], "page": 1},
 {"key": "rows.29.fee", "value": "0", "bbox_2d": [783, 904, 790, 914], "page": 1},
 {"key": "rows.31.fee", "value": "0", "bbox_2d": [786, 116, 793, 126], "page": 2},
 {"key": "rows.32.date", "value": "2025.02.21", "bbox_2d": [100, 135, 160, 145], "page": 2},
 {"key": "rows.32.seq", "value": "-", "bbox_2d": [546, 135, 550, 145], "page": 2},
 {"key": "rows.33.amount", "value": "1,440,100", "bbox_2d": [386, 154, 439, 164], "page": 2},
 {"key": "rows.35.amount", "value": "53,620", "bbox_2d": [403, 193, 439, 203], "page": 2},
 {"key": "rows.36.date", "value": "2025.02.24", "bbox_2d": [100, 212, 160, 222], "page": 2},
 {"key": "rows.37.months", "value": "일시불", "bbox_2d": [463, 232, 503, 241], "page": 2},
 {"key": "rows.38.principal", "value": "52,000", "bbox_2d": [629, 251, 665, 261], "page": 2},
 {"key": "rows.40.date", "value": "2025.02.27", "bbox_2d": [100, 290, 160, 299], "page": 2},
 {"key": "rows.41.seq", "value": "-", "bbox_2d": [546, 309, 550, 319], "page": 2},
 {"key": "rows.41.fee", "value": "0", "bbox_2d": [786, 309, 793, 319], "page": 2},
 {"key": "rows.42.date", "value": "2025.02.28", "bbox_2d": [100, 328, 160, 338], "page": 2},
 {"key": "fee_rate", "value": "연 14.9%", "bbox_2d": [204, 373, 254, 383], "page": 2},
 {"key": "fee_per_100.0.months", "value": "2개월", "bbox_2d": [393, 373, 426, 383], "page": 2},
 {"key": "fee_per_100.1.months", "value": "3개월", "bbox_2d": [477, 373, 510, 383], "page": 2}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check card_statement` → `python -m docgen.formdir card card_statement` (실제 질문→답 확인).

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
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions card_statement --show` · `python -m docgen.preview card_statement --out work/card_statement`
