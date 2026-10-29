# 가족관계증명서 (`family_relation_certificate`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card family_relation_certificate · card-hash: bf07042e63fd -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** family · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 가족관계증명서
- **쓰이는 업무:** 주택담보대출, 유학생 송금, 상속예금 지급
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa family_relation_certificate --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 가족관계증명서 (일반/상세). 사망한 부모, 전혼 자녀, 입양(친생부모) 등.

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/family.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 16칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `cert_type` | 증명서종류 | text | 1쪽 [588, 84, 659, 108] | 늘 | 템플릿 | generate.py | look/template.html.j2:6 · fields.json:10 | 묻기 |
| `reg_base` | 등록기준지 | text | 1쪽 [230, 141, 426, 153] | 늘 | 템플릿 | generate.py | look/template.html.j2:7 · fields.json:45 | 묻기 |
| `customer.relation` ← `self.relation` | 구분 | text | 1쪽 [108, 221, 138, 233] | 늘 | 템플릿 | generate.py | fields.json:80 | 묻기 |
| `customer.name` ← `self.name` | 성명 | text | 1쪽 [208, 221, 269, 233] | 늘 | 템플릿 | generate.py | fields.json:70 | 묻기 |
| `customer.name_hanja` ← `self.name_hanja` | 성명(한자) | text | 1쪽 [274, 221, 335, 233] | 늘 | 템플릿 | generate.py | fields.json:75 | 묻기 |
| `customer.birth` ← `self.birth` | 출생연월일 | date | 1쪽 [412, 221, 526, 233] | 늘 | 템플릿 | generate.py | fields.json:55 | 묻기 |
| `customer.rrn` ← `self.rrn` | 주민등록번호 | rrn | 1쪽 [614, 221, 718, 233] | 늘 | 템플릿 | generate.py | fields.json:85 | 묻기 |
| `customer.gender` ← `self.gender` | 성별 | text | 1쪽 [799, 221, 814, 233] | 늘 | 템플릿 | generate.py | fields.json:65 | 묻기 |
| `customer.bon` ← `self.bon` | 본 | text | 1쪽 [864, 221, 895, 233] | 늘 | 템플릿 | generate.py | fields.json:60 | 묻기 |
| `issue_date` | 발급일 | date | 1쪽 [438, 446, 562, 459] | 늘 | 템플릿 | generate.py | fields.json:20 | 묻기 |
| `issuer` | 발급기관 | text | 1쪽 [257, 481, 721, 497] | 늘 | 템플릿 | generate.py | fields.json:30 | 묻기 |
| `issue_time` | 발급시각 | text | 1쪽 [191, 527, 251, 537] | 늘 | 템플릿 | generate.py | fields.json:25 | 묻기 |
| `applicant` | 신청인 | text | 1쪽 [191, 543, 247, 554] | 늘 | 템플릿 | generate.py | fields.json:5 | 묻기 |
| `doc_check_no` | 문서확인번호 | text | 1쪽 [160, 945, 269, 955] | 4/16 | 템플릿 | generate.py | fields.json:15 | 묻기 |
| `officer` | 발급담당자 | - | - | 12/16 | 템플릿 | generate.py | fields.json:35 | 묻기 |
| `officer_phone` | 전화 | - | - | 12/16 | 템플릿 | generate.py | fields.json:40 | 묻기 |

## 표 `family` (표 과제 table·table_read·table_find·table_qa) — 8열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `family.*.relation` | 구분 | text | 1쪽 [115, 319, 130, 332] (1행) | 늘 | 템플릿 | generate.py | fields.json:120 | 묻기 |
| `family.*.name` | 성명 | text | 1쪽 [208, 319, 269, 332] (1행) | 늘 | 템플릿 | generate.py | fields.json:110 | 묻기 |
| `family.*.name_hanja` | 성명(한자) | text | 1쪽 [274, 319, 335, 332] (1행) | 늘 | 템플릿 | generate.py | fields.json:115 | 묻기 |
| `family.*.birth` | 출생연월일 | date | 1쪽 [412, 319, 526, 332] (1행) | 늘 | 템플릿 | generate.py | fields.json:95 | 묻기 |
| `family.*.rrn` | 주민등록번호 | rrn | 1쪽 [614, 319, 718, 332] (1행) | 늘 | 템플릿 | generate.py | fields.json:125 | 묻기 |
| `family.*.gender` | 성별 | text | 1쪽 [799, 319, 814, 332] (1행) | 늘 | 템플릿 | generate.py | fields.json:105 | 묻기 |
| `family.*.bon` | 본 | text | 1쪽 [864, 319, 895, 332] (1행) | 늘 | 템플릿 | generate.py | fields.json:100 | 묻기 |
| `family.*.status` | 사망 | - | - (1행) | 2/16 | 템플릿 | generate.py | fields.json:130 | 묻기 |

## 체크·도장·서명 (marks) — 1칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.issuer` | 발급기관직인 | seal | 1쪽 [708, 459, 798, 522] | 늘 | 템플릿 | generate.py | fields.json:50 | 묻기 |

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
"가족관계증명서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "일반",
 "세종특별자치시 도담동 550-8",
 "본인",
 "남궁예태",
 "南宮叡兌",
 "1985년 03월 28일",
 "850328-2489940",
 "여",
 "咸悅",
 "부",
 "남궁찬윤",
 "南宮讚允",
 "1952년 10월 28일",
 "521028-1401146",
 "남",
 "모",
 "방옥주",
 "方玉宙",
 "1953년 03월 28일",
 "530328-2814528",
 "溫陽",
 "2025년 04월 01일",
 "법원행정처 전산정보중앙관리소 전산운영책임관",
 "06시 41분",
 "9745-8227-1390-2186"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"1952년 10월 28일"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"06시 41분"
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
- cert_type: 증명서종류
- reg_base: 등록기준지
- customer.relation: 구분 (고객 관계)
- customer.name: 성명 (고객 성명)
- customer.name_hanja: 성명(한자) (고객 한자 성명)
- customer.birth: 출생연월일 (고객 생년월일)
- customer.rrn: 주민등록번호 (고객 주민등록번호)
- customer.gender: 성별 (고객 성별)
- customer.bon: 본 (고객 본관)
- issue_date: 발급일
- issuer: 발급기관
- issue_time: 발급시각
- applicant: 신청인
- doc_check_no: 문서확인번호
```

답:

```json
[{"key": "cert_type", "value": "일반", "bbox_2d": [588, 84, 659, 108], "page": 1},
 {"key": "reg_base", "value": "세종특별자치시 도담동 550-8", "bbox_2d": [230, 141, 426, 153], "page": 1},
 {"key": "customer.relation", "value": "본인", "bbox_2d": [108, 221, 138, 233], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [208, 221, 269, 233], "page": 1},
 {"key": "customer.name_hanja", "value": "南宮叡兌", "bbox_2d": [274, 221, 335, 233], "page": 1},
 {"key": "customer.birth", "value": "1985년 03월 28일", "bbox_2d": [412, 221, 526, 233], "page": 1},
 {"key": "customer.rrn", "value": "850328-2489940", "bbox_2d": [614, 221, 718, 233], "page": 1},
 {"key": "customer.gender", "value": "여", "bbox_2d": [799, 221, 814, 233], "page": 1},
 {"key": "customer.bon", "value": "咸悅", "bbox_2d": [864, 221, 895, 233], "page": 1},
 {"key": "issue_date", "value": "2025년 04월 01일", "bbox_2d": [438, 446, 562, 459], "page": 1},
 {"key": "issuer", "value": "법원행정처 전산정보중앙관리소 전산운영책임관", "bbox_2d": [257, 481, 721, 497], "page": 1},
 {"key": "issue_time", "value": "06시 41분", "bbox_2d": [191, 527, 251, 537], "page": 1},
 {"key": "applicant", "value": "남궁예태", "bbox_2d": [191, 543, 247, 554], "page": 1},
 {"key": "doc_check_no", "value": "9745-8227-1390-2186", "bbox_2d": [160, 945, 269, 955], "page": 1}]
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
[{"key": "seal.issuer", "value": true, "bbox_2d": [708, 459, 798, 522], "page": 1}]
```

### 표 추출 `table` · 채점 cell_f1 (칸)

질문:

```
이 문서에서 1쪽 bbox_2d=[79, 280, 921, 363] 위치의 표의 모든 행을 문서에 보이는 순서대로(위에서 아래, 앞쪽부터) 읽어 JSON 으로 답하세요.
꼴: {"columns": [열 키, …], "rows": [[값, …], …], "row_boxes": [{"bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호}, …]}
- columns 는 아래 열 키를 그 순서 그대로 쓰고, rows 는 행마다 같은 순서로 값을 씁니다.
- 값은 문서에 적힌 그대로 씁니다. 빈 칸과 표에 없는 열은 null, 칸 안의 여러 줄은 공백 하나로 잇고, 여러 행에 걸친 칸은 행마다 같은 값을 씁니다.
- 합계·소계 행, 다음 쪽에서 다시 나온 머리글 행, 모두 빈 행은 뺍니다.
- row_boxes 는 rows 와 같은 순서로 행마다 그 행을 감싸는 상자입니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 그런 표가 없으면 rows 와 row_boxes 를 [] 로 답하세요.
열 (키: 항목명)
- relation: 구분
- name: 성명
- name_hanja: 성명(한자)
- birth: 출생연월일
- rrn: 주민등록번호
- gender: 성별
- bon: 본
```

답:

```json
{
 "columns": [
  "relation",
  "name",
  "name_hanja",
  "birth",
  "rrn",
  "gender",
  "bon"
 ],
 "rows": [
  [
   "부",
   "남궁찬윤",
   "南宮讚允",
   "1952년 10월 28일",
   "521028-1401146",
   "남",
   "咸悅"
  ],
  [
   "모",
   "방옥주",
   "方玉宙",
   "1953년 03월 28일",
   "530328-2814528",
   "여",
   "溫陽"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    115,
    319,
    895,
    332
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    115,
    350,
    895,
    363
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
[{"columns": ["구분", "성명", "성명(한자)", "출생연월일", "주민등록번호", "성별", "본"], "bbox_2d": [79, 280, 921, 363], "page": 1, "n_rows": 2}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 표를 보고 답하세요. 표의 행은 모두 몇 개입니까? 머리글·합계 행과 모두 빈 행은 세지 않습니다. (숫자만 답하세요)
```

답:

```json
2
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 표를 보고 답하세요. '구분' 칸이 '부'인 행의 '성명(한자)' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"南宮讚允"
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
  "구분",
  "성 명",
  "출생연월일",
  "주민등록번호",
  "성별",
  "본"
 ],
 "rows": [
  [
   "부",
   "남궁찬윤(南宮讚允)",
   "1952년 10월 28일",
   "521028-1401146",
   "남",
   "咸悅"
  ],
  [
   "모",
   "방옥주(方玉宙)",
   "1953년 03월 28일",
   "530328-2814528",
   "여",
   "溫陽"
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    79,
    311,
    921,
    342
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    79,
    342,
    921,
    372
   ],
   "page": 1
  }
 ]
}
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa family_relation_certificate --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check family_relation_certificate` → `python -m docgen.formdir card family_relation_certificate` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa family_relation_certificate --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions family_relation_certificate --show` · `python -m docgen.preview family_relation_certificate --out work/family_relation_certificate`
