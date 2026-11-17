# 본인확인서(FATCA CRS 개인,개인사업자용)(영문) (`hf429`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf429 · card-hash: 5a5e0b5acad8 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 본인확인서(FATCA CRS 개인,개인사업자용)(영문)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf429 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.429 (기타) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 17칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `CustomerProfile` | CustomerProfile | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:52 | 묻기 |
| `WhetherOverseasResidentorNot` | WhetherOverseasResidentorNot | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:81 | 묻기 |
| `IdentificationNumberetc` | IdentificationNumber(TIN),etc. | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:95 | 묻기 |
| `Reportingcountry` | Reportingcountry | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:109 | 묻기 |
| `NA` | N/A | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:200 | 묻기 |
| `Surname` | Surname(성) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:216 | 묻기 |
| `Surname2` | Surname(성) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:233 | 묻기 |
| `GivenName` | GivenName(이름) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:250 | 묻기 |
| `Jurisdictionof` | Jurisdictionof | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:388 | 묻기 |
| `Country` | Country*(2) | text | 1쪽 [217, 608, 248, 619] | 늘 | 파일 key | 값 종류 `country` | fields.json:402 | 묻기 |
| `OverseaEnglishaddress` | OverseaEnglishaddress | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:431 | 묻기 |
| `Surname3` | Surname(성) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:460 | 묻기 |
| `GivenName2` | GivenName(이름) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:474 | 묻기 |
| `customer.birth` | DateofBirth | date | 1쪽 [520, 189, 566, 196] | 늘 | 파일 key | 값 종류 `date` | fields.json:488 | 묻기 |
| `customer.birth2` | DateofBirth | date | 1쪽 [520, 199, 563, 206] | 늘 | 파일 key | 값 종류 `date` | fields.json:504 | 묻기 |
| `customer.birth3` | DateofBirth | date | 1쪽 [698, 176, 763, 185] | 늘 | 파일 key | 고객 정보 (키 `customer.birth`, 없으면 값 종류 `date`) | fields.json:674 | 묻기 |
| `PhoneNo` | PhoneNo. | phone | 1쪽 [694, 210, 778, 219] | 늘 | 파일 key | 값 종류 `phone` | fields.json:687 | 묻기 |

## 표 `Name_목록` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `Name_목록.*.value` | (CapitalLetter)* | amount | - (1행) | 늘 | 파일 key | 값 종류 `skip` | fields.json:66 | 묻기 |

## 표 `FATCA_목록` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `FATCA_목록.*.FATCA` | FATCA | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:140 | 묻기 |

## 표 `FATCA2_목록` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `FATCA2_목록.*.CRS` | CRS | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:170 | 묻기 |

## 표 `표7_목록` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `표7_목록.*.value` | (TIN) | amount | - (1행) | 늘 | 파일 key | 값 종류 `skip` | fields.json:416 | 묻기 |

## 표 `GivenName_목록` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `GivenName_목록.*.PhoneNo` | PhoneNo. | phone | 1쪽 [517, 223, 576, 230] (1행) | 늘 | 파일 key | 값 종류 `phone` | fields.json:520 | 묻기 |

## 체크·도장·서명 (marks) — 11칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.UScitizen` | U.S.citizen(includingdualcitizenship) | checkbox (U.S. citizen(including dual citizenship) / U.S. permanent resident / U.S. resident under U.S. tax law) | 1쪽 [194, 293, 427, 306] | 늘 | 파일 key | 보기 중 고름: U.S. citizen(including dual citizenship) / U.S. permanent resident / U.S. resident under U.S. tax law | fields.json:266 | 묻기 |
| `check.Residentinac` | ResidentinacountryotherthanU.S | checkbox (Resident in a country other than U.S) | 1쪽 [194, 361, 417, 374] | 늘 | 파일 key | 보기 중 고름: Resident in a country other than U.S | fields.json:328 | 묻기 |
| `check.AllNA` | AllN/A | checkbox (All N/A) | 1쪽 [194, 395, 259, 409] | 늘 | 파일 key | 보기 중 고름: All N/A | fields.json:358 | 묻기 |
| `check.Nonissuingc` | Non-issuingcountry | checkbox (Non-issuing country / Not requested by tax authority / Not acquired) | 1쪽 [512, 506, 651, 527] | 늘 | 파일 key | 보기 중 고름: Non-issuing country / Not requested by tax authority / Not acquired | fields.json:535 | 묻기 |
| `check.Nonissuingc2` | Non-issuingcountry | checkbox (Non-issuing country / Not requested by tax authority / Not acquired) | 1쪽 [512, 613, 609, 635] | 늘 | 파일 key | 보기 중 고름: Non-issuing country / Not requested by tax authority / Not acquired | fields.json:597 | 묻기 |
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [750, 42, 780, 63] | 늘 | - | - | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [733, 46, 797, 59] | 늘 | - | - | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [797, 46, 861, 59] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [797, 46, 861, 59] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [874, 41, 905, 64] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [861, 46, 918, 59] | 늘 | - | - | - | 묻기 |

- **나옴:** 여러 seed 로 그렸을 때 그 칸이 나온 문서 수 (조건부 칸). **위치:** seed 하나로 그린 것 — 행 수·변형에 따라 달라질 수 있음.
- **키는·값은:** 어디서 정해지나. 키·값 종류는 이 서식 파일에 적힌 그대로입니다 (모든 서식 공통 키 사전은 없음). "키 설명 그대로" 는 칸에 `"key"` 가 없어 키 설명이 키로 나가는 것. 바꾸려면 **고칠 곳** 줄(칸)에 `"key"`·`"kind"`·`"source"` 를 적습니다.
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
"본인확인서(FATCA CRS 개인,개인사업자용)(영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "호주",
 "1985-03-28",
 "010-6144-1173"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"호주"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"1985-03-28"
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
- CustomerProfile: CustomerProfile
- WhetherOverseasResidentorNot: WhetherOverseasResidentorNot
- IdentificationNumberetc: IdentificationNumber(TIN),etc.
- Reportingcountry: Reportingcountry
- NA: N/A
- Surname: Surname(성) (같은 설명 중 1번째 칸)
- Surname2: Surname(성) (같은 설명 중 2번째 칸)
- GivenName: GivenName(이름) (같은 설명 중 1번째 칸)
- Jurisdictionof: Jurisdictionof
- Country: Country*(2)
- OverseaEnglishaddress: OverseaEnglishaddress
- Surname3: Surname(성) (같은 설명 중 3번째 칸)
- GivenName2: GivenName(이름) (같은 설명 중 2번째 칸)
- customer.birth: DateofBirth (같은 설명 중 1번째 칸)
- customer.birth2: DateofBirth (같은 설명 중 2번째 칸)
- customer.birth3: DateofBirth (같은 설명 중 3번째 칸)
- PhoneNo: PhoneNo.
```

답:

```json
[{"key": "CustomerProfile", "value": null},
 {"key": "WhetherOverseasResidentorNot", "value": null},
 {"key": "IdentificationNumberetc", "value": null},
 {"key": "Reportingcountry", "value": null},
 {"key": "NA", "value": null},
 {"key": "Surname", "value": null},
 {"key": "Surname2", "value": null},
 {"key": "GivenName", "value": null},
 {"key": "Jurisdictionof", "value": null},
 {"key": "Country", "value": "호주", "bbox_2d": [217, 608, 248, 619], "page": 1},
 {"key": "OverseaEnglishaddress", "value": null},
 {"key": "Surname3", "value": null},
 {"key": "GivenName2", "value": null},
 {"key": "customer.birth", "value": "1985-03-28", "bbox_2d": [520, 189, 566, 196], "page": 1},
 {"key": "customer.birth2", "value": "1985-03-28", "bbox_2d": [520, 199, 563, 206], "page": 1},
 {"key": "customer.birth3", "value": "1985-03-28", "bbox_2d": [698, 176, 763, 185], "page": 1},
 {"key": "PhoneNo", "value": "010-6144-1173", "bbox_2d": [694, 210, 778, 219], "page": 1}]
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
- check.UScitizen: U.S.citizen(includingdualcitizenship) (체크박스, 보기: U.S. citizen(including dual citizenship) / U.S. permanent resident / U.S. resident under U.S. tax law)
- check.Residentinac: ResidentinacountryotherthanU.S (체크박스, 보기: Resident in a country other than U.S)
- check.AllNA: AllN/A (체크박스, 보기: All N/A)
- check.Nonissuingc: Non-issuingcountry (같은 설명 중 1번째 칸, 체크박스, 보기: Non-issuing country / Not requested by tax authority / Not acquired)
- check.Nonissuingc2: Non-issuingcountry (같은 설명 중 2번째 칸, 체크박스, 보기: Non-issuing country / Not requested by tax authority / Not acquired)
- seal.staff.본인확인: 본인확인 (같은 설명 중 1번째 칸, 도장)
- sign.staff.본인확인: 본인확인 (같은 설명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 설명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 설명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 설명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.UScitizen", "value": "U.S. citizen(including dual citizenship)", "bbox_2d": [194, 293, 209, 306], "page": 1},
 {"key": "check.Residentinac", "value": "Resident in a country other than U.S", "bbox_2d": [194, 361, 209, 374], "page": 1},
 {"key": "check.AllNA", "value": "All N/A", "bbox_2d": [194, 395, 209, 409], "page": 1},
 {"key": "check.Nonissuingc", "value": "Non-issuing country", "bbox_2d": [512, 506, 535, 527], "page": 1},
 {"key": "check.Nonissuingc2", "value": "Not acquired", "bbox_2d": [512, 613, 535, 635], "page": 1},
 {"key": "seal.staff.본인확인", "value": true, "bbox_2d": [750, 42, 780, 63], "page": 1},
 {"key": "sign.staff.본인확인", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": true, "bbox_2d": [797, 46, 861, 59], "page": 1},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [874, 41, 905, 64], "page": 1},
 {"key": "sign.staff.책임자", "value": false}]
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
- PhoneNo: PhoneNo.
- 권한의제한: 권한의제한
```

답:

```json
{
 "columns": [
  "PhoneNo",
  "권한의제한"
 ],
 "rows": [
  [
   "010-6144-1173",
   null
  ],
  [
   "010-6144-1173",
   null
  ]
 ],
 "row_boxes": [
  {
   "bbox_2d": [
    517,
    223,
    576,
    230
   ],
   "page": 1
  },
  {
   "bbox_2d": [
    518,
    650,
    621,
    661
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
[{"columns": ["PhoneNo."], "bbox_2d": [517, 223, 621, 661], "page": 1, "n_rows": 2}]
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 표를 보고 답하세요. 위에서 2번째 행의 'PhoneNo.' 값은 무엇입니까? 머리글은 세지 않습니다. (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"010-6144-1173"
```

### 표 질의 `table_qa` · 채점 acc

질문:

```
이 문서의 표를 보고 답하세요. 마지막 행의 'PhoneNo.' 값은 무엇입니까? (문서에 적힌 그대로 답하고, 비어 있으면 null 로 답하세요)
```

답:

```json
"010-6144-1173"
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf429 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf429` → `python -m docgen.formdir card hf429` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | studio ① 서식 › 영역 편집에서 그리기 (`fields.json` items 에 한 칸) | 다시 |
| 답의 위치 (박스) | `fields.json` 그 칸의 `rect` [x0, y0, x1, y1] (pt) — 또는 영역 편집 | 다시 |
| 답의 키 | `fields.json` 그 칸에 `"key"` (없으면 키 설명이 그대로 키) | 다시 |
| 답의 값 | `fields.json` 그 칸에 `"source"` ([값 출처 목록](../_common/values.md)) 또는 값 종류 `"kind"` | 다시 |
| 칸의 항목명 | `fields.json` 그 칸의 `label` | 다시 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf429 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf429 --show` · `python -m docgen.preview hf429 --out work/hf429`
