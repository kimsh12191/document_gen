# 본인확인서(FATCA CRS 법인,임의단체용)(영문) (`hf410`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf410 · card-hash: 6b08ea73b796 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 본인확인서(FATCA CRS 법인,임의단체용)(영문)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 하나은행 공개 서식 No.410 (기타) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 28칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `NameofEntity` | NameofEntity | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `BusinessRegistrationNo` | BusinessRegistrationNo. | biz_no | 1쪽 [707, 182, 825, 200] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `PhoneNo` | PhoneNo. | phone | 1쪽 [710, 203, 821, 220] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `TaxpayerIdentificationNo` | TaxpayerIdentificationNo | text | 1쪽 [372, 735, 509, 752] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.address` | Address(HeadOffice'sAddress) | text | 1쪽 [373, 756, 782, 782] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `NameofEntity2` | NameofEntity | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `GIINKIINEINNO` | GIIN/KIIN/EINNO | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `JurisdictionofResidence` | JurisdictionofResidence | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `JurisdictionofResidence2` | JurisdictionofResidence | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `JurisdictionofResidence3` | JurisdictionofResidence | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `GivenName` | GivenName | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `TaxpayerIdentificationNO` | TaxpayerIdentificationNO | amount | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Overseaaddress` | Overseaaddress | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `GivenName2` | GivenName | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `TaxpayerIdentificationNO2` | TaxpayerIdentificationNO | amount | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Overseaaddress2` | Overseaaddress | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `GivenName3` | GivenName | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `TaxpayerIdentificationNO3` | TaxpayerIdentificationNO | amount | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Overseaaddress3` | Overseaaddress | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `SareRatio` | SareRatio(%)* | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Surname` | Surname | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:492 | 묻기 |
| `SareRatio2` | SareRatio(%)* | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Surname2` | Surname | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:516 | 묻기 |
| `SareRatio3` | SareRatio(%)* | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `Surname3` | Surname | text | - | 늘 | 원본 칸 (항목명 → 값 종류) | fields.json:540 | 묻기 |
| `customer.birth` | DateofBirth | date | 2쪽 [805, 646, 882, 661] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.birth2` | DateofBirth | date | 2쪽 [807, 755, 884, 772] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `customer.birth3` | DateofBirth | date | 2쪽 [809, 867, 886, 882] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

## 체크·도장·서명 (marks) — 9칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [727, 40, 772, 72] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [713, 34, 785, 78] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [785, 34, 848, 78] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [785, 34, 848, 78] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [863, 40, 908, 72] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [848, 34, 923, 78] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.Nonissuingc` | Non-issuingcountry | checkbox (Non-issuing country / Not required by tax authority / Not aqucired (write the reason) | 2쪽 [693, 684, 853, 695] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.Nonissuingc2` | Non-issuingcountry | checkbox (Non-issuing country / Not required by tax authority / Not aqucired (write the reason) | 2쪽 [505, 793, 620, 805] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |
| `check.Nonissuingc3` | Non-issuingcountry | checkbox (Non-issuing country / Not required by tax authority / Not aqucired (write the reason) | 2쪽 [505, 914, 678, 926] | 늘 | 원본 칸 (항목명 → 값 종류) | - | 묻기 |

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
"본인확인서(FATCA CRS 법인,임의단체용)(영문)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "482-70-93626",
 "010-6144-1173",
 "175-313998-45181",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "1985.03.28"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"1985.03.28"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"1985.03.28"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- NameofEntity: NameofEntity (같은 항목명 중 1번째 칸)
- BusinessRegistrationNo: BusinessRegistrationNo.
- PhoneNo: PhoneNo.
- TaxpayerIdentificationNo: TaxpayerIdentificationNo (같은 항목명 중 1번째 칸)
- customer.address: Address(HeadOffice'sAddress) (고객 주소)
- NameofEntity2: NameofEntity (같은 항목명 중 2번째 칸)
- GIINKIINEINNO: GIIN/KIIN/EINNO
- JurisdictionofResidence: JurisdictionofResidence (같은 항목명 중 1번째 칸)
- JurisdictionofResidence2: JurisdictionofResidence (같은 항목명 중 2번째 칸)
- JurisdictionofResidence3: JurisdictionofResidence (같은 항목명 중 3번째 칸)
- GivenName: GivenName (같은 항목명 중 1번째 칸)
- TaxpayerIdentificationNO: TaxpayerIdentificationNO (같은 항목명 중 2번째 칸)
- Overseaaddress: Overseaaddress (같은 항목명 중 1번째 칸)
- GivenName2: GivenName (같은 항목명 중 2번째 칸)
- TaxpayerIdentificationNO2: TaxpayerIdentificationNO (같은 항목명 중 3번째 칸)
- Overseaaddress2: Overseaaddress (같은 항목명 중 2번째 칸)
- GivenName3: GivenName (같은 항목명 중 3번째 칸)
- TaxpayerIdentificationNO3: TaxpayerIdentificationNO (같은 항목명 중 4번째 칸)
- Overseaaddress3: Overseaaddress (같은 항목명 중 3번째 칸)
- SareRatio: SareRatio(%)* (같은 항목명 중 1번째 칸)
- Surname: Surname (같은 항목명 중 1번째 칸)
- SareRatio2: SareRatio(%)* (같은 항목명 중 2번째 칸)
- Surname2: Surname (같은 항목명 중 2번째 칸)
- SareRatio3: SareRatio(%)* (같은 항목명 중 3번째 칸)
- Surname3: Surname (같은 항목명 중 3번째 칸)
- customer.birth: DateofBirth (고객 생년월일, 같은 항목명 중 1번째 칸)
- customer.birth2: DateofBirth (같은 항목명 중 2번째 칸)
- customer.birth3: DateofBirth (같은 항목명 중 3번째 칸)
```

답:

```json
[{"key": "NameofEntity", "value": null},
 {"key": "BusinessRegistrationNo", "value": "482-70-93626", "bbox_2d": [707, 182, 825, 200], "page": 1},
 {"key": "PhoneNo", "value": "010-6144-1173", "bbox_2d": [710, 203, 821, 220], "page": 1},
 {"key": "TaxpayerIdentificationNo", "value": "175-313998-45181", "bbox_2d": [372, 735, 509, 752], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [373, 756, 782, 782], "page": 1},
 {"key": "NameofEntity2", "value": null},
 {"key": "GIINKIINEINNO", "value": null},
 {"key": "JurisdictionofResidence", "value": null},
 {"key": "JurisdictionofResidence2", "value": null},
 {"key": "JurisdictionofResidence3", "value": null},
 {"key": "GivenName", "value": null},
 {"key": "TaxpayerIdentificationNO", "value": null},
 {"key": "Overseaaddress", "value": null},
 {"key": "GivenName2", "value": null},
 {"key": "TaxpayerIdentificationNO2", "value": null},
 {"key": "Overseaaddress2", "value": null},
 {"key": "GivenName3", "value": null},
 {"key": "TaxpayerIdentificationNO3", "value": null},
 {"key": "Overseaaddress3", "value": null},
 {"key": "SareRatio", "value": null},
 {"key": "Surname", "value": null},
 {"key": "SareRatio2", "value": null},
 {"key": "Surname2", "value": null},
 {"key": "SareRatio3", "value": null},
 {"key": "Surname3", "value": null},
 {"key": "customer.birth", "value": "1985.03.28", "bbox_2d": [805, 646, 882, 661], "page": 2},
 {"key": "customer.birth2", "value": "1985.03.28", "bbox_2d": [807, 755, 884, 772], "page": 2},
 {"key": "customer.birth3", "value": "1985.03.28", "bbox_2d": [809, 867, 886, 882], "page": 2}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- seal.staff.본인확인: 본인확인 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.본인확인: 본인확인 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
- check.Nonissuingc: Non-issuingcountry (같은 항목명 중 1번째 칸, 체크박스, 보기: Non-issuing country / Not required by tax authority / Not aqucired (write the reason)
- check.Nonissuingc2: Non-issuingcountry (같은 항목명 중 2번째 칸, 체크박스, 보기: Non-issuing country / Not required by tax authority / Not aqucired (write the reason)
- check.Nonissuingc3: Non-issuingcountry (같은 항목명 중 3번째 칸, 체크박스, 보기: Non-issuing country / Not required by tax authority / Not aqucired (write the reason)
```

답:

```json
[{"key": "seal.staff.본인확인", "value": true, "bbox_2d": [727, 40, 772, 72], "page": 1},
 {"key": "sign.staff.본인확인", "value": false},
 {"key": "seal.staff.담당", "value": false},
 {"key": "sign.staff.담당", "value": true, "bbox_2d": [785, 34, 848, 78], "page": 1},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [863, 40, 908, 72], "page": 1},
 {"key": "sign.staff.책임자", "value": false},
 {"key": "check.Nonissuingc", "value": "Not required by tax authority", "bbox_2d": [693, 684, 705, 695], "page": 2},
 {"key": "check.Nonissuingc2", "value": "Non-issuing country", "bbox_2d": [505, 793, 516, 805], "page": 2},
 {"key": "check.Nonissuingc3", "value": "Not aqucired (write the reason", "bbox_2d": [505, 914, 516, 926], "page": 2}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기·위치·항목명 | studio ① 서식 › 영역 편집 (저장하면 `fields.json` items) | 재검수 → 카드 다시 만들기 |
| 값이 이상함 | 영역 편집에서 그 칸의 값 출처·값 종류 | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions hf410 --show` · `python -m docgen.preview hf410 --out work/hf410`
