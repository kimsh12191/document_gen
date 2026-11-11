# 퇴직연금 퇴직급여 지급신청서(DB) (`hf179`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf179 · card-hash: d58b24297a60 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 퇴직연금 퇴직급여 지급신청서(DB)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf179 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.179 (퇴직연금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 21칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `company.name` | 기업명 | text | 1쪽 [204, 243, 327, 263] | 늘 | 파일 key | 고객 정보 (키 `company.name`, 없으면 값 종류 `company`) | fields.json:49 | 묻기 |
| `customer.name` | 가입자성명 | text | 1쪽 [210, 269, 284, 286] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `person`) | fields.json:62 | 묻기 |
| `employer.hire_date` | 입사일자 | date | 1쪽 [209, 291, 298, 308] | 늘 | 파일 key | 고객 정보 (키 `employer.hire_date`, 없으면 값 종류 `date`) | fields.json:75 | 묻기 |
| `DB계좌번호` | DB계좌번호 | text | 1쪽 [579, 243, 737, 261] | 늘 | 파일 key | 값 종류 `account` | fields.json:88 | 묻기 |
| `customer.birth` | 생년월일 | date | 1쪽 [576, 267, 664, 286] | 늘 | 파일 key | 고객 정보 (키 `customer.birth`, 없으면 값 종류 `date`) | fields.json:102 | 묻기 |
| `퇴직일자` | 퇴직일자 | date | 1쪽 [190, 334, 284, 351] | 늘 | 파일 key | 값 종류 `date` | fields.json:116 | 묻기 |
| `예약지급일주1` | 예약지급일주1 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:190 | 묻기 |
| `퇴직급여총액` | 퇴직급여총액 | amount | 1쪽 [650, 344, 731, 358] | 늘 | 파일 key | 값 종류 `amount` | fields.json:282 | 묻기 |
| `지급신청금액` | 지급신청금액 | number | 1쪽 [726, 372, 805, 389] | 늘 | 파일 key | 값 종류 `amount` | fields.json:296 | 묻기 |
| `금융기관명` | 금융기관명 | text | 1쪽 [289, 533, 363, 550] | 늘 | 파일 key | 값 종류 `bank` | fields.json:403 | 묻기 |
| `금융기관명2` | 금융기관명 | text | 1쪽 [289, 557, 363, 574] | 늘 | 파일 key | 값 종류 `bank` | fields.json:417 | 묻기 |
| `account` | 계좌번호 | account_no | 1쪽 [583, 533, 732, 552] | 늘 | 파일 key | 고객 정보 (키 `account`, 없으면 값 종류 `account`) | fields.json:431 | 묻기 |
| `account2` | 계좌번호 | account_no | 1쪽 [581, 558, 730, 575] | 늘 | 파일 key | 고객 정보 (키 `account`, 없으면 값 종류 `account`) | fields.json:444 | 묻기 |
| `영업점본인확인` | 영업점본인확인 | text | 1쪽 [830, 848, 905, 865] | 늘 | 파일 key | 값 종류 `branch` | fields.json:671 | 묻기 |
| `date` | 작성일 | date | 1쪽 [781, 204, 926, 220] | 늘 | 파일 key | 작성일 | fields.json:685 | 묻기 |
| `signer.name` | 가입자 | text | 1쪽 [763, 818, 835, 833] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:712 | 묻기 |
| `signer2.name` | 기업명 | text | 1쪽 [286, 900, 404, 916] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:731 | 묻기 |
| `signer3.name` | 가입자 | text | 1쪽 [629, 899, 702, 916] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:750 | 묻기 |
| `필수서류` | 필수서류 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:769 | 묻기 |
| `퇴직소득원천징수영수증` | 퇴직소득원천징수영수증 | number | 2쪽 [832, 258, 907, 275] | 늘 | 파일 key | 값 종류 `amount` | fields.json:783 | 묻기 |
| `타금융기관IRP또는요구불계좌사본` | 타금융기관IRP또는요구불계좌사본 | text | 2쪽 [552, 283, 699, 300] | 늘 | 파일 key | 값 종류 `account` | fields.json:797 | 묻기 |

## 표 `목록` (표 과제 table·table_read·table_find·table_qa) — 4열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `목록.*.매도순위` | 매도순위 | text | - (1행) | 늘 | 파일 key | 값 종류 `text` | fields.json:457 | 묻기 |
| `목록.*.상품명` | 상품명 | text | 1쪽 [158, 703, 319, 722] (1행) | 늘 | 파일 key | 값 종류 `product` | fields.json:499 | 묻기 |
| `목록.*.계좌번호` | 계좌번호 | text | - (1행) | 늘 | 파일 key | 값 종류 `account` | fields.json:541 | 묻기 |
| `목록.*.매도금액` | 매도금액(원/좌) | number | 1쪽 [818, 703, 920, 720] (1행) | 늘 | 파일 key | 값 종류 `amount` | fields.json:583 | 묻기 |

## 체크·도장·서명 (marks) — 16칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.지급형태` | 지급형태 | checkbox (IRP이전(의무)) | 1쪽 [191, 360, 285, 374] | 늘 | 파일 key | 보기 중 고름: IRP이전(의무) | fields.json:130 | 묻기 |
| `check.지급형태2` | 지급형태 | checkbox (요구불계좌) | 1쪽 [191, 414, 272, 428] | 늘 | 파일 key | 보기 중 고름: 요구불계좌 | fields.json:160 | 묻기 |
| `check.만55세이후퇴직` | 만55세이후퇴직 | checkbox (만55세 이후 퇴직 / 만원 이하 퇴직금 지급 / 가입자 사망 / 한시적 체류자격 외국인) | 1쪽 [295, 433, 380, 447] | 늘 | 파일 key | 보기 중 고름: 만55세 이후 퇴직 / 만원 이하 퇴직금 지급 / 가입자 사망 / 한시적 체류자격 외국인 | fields.json:204 | 묻기 |
| `check.기업으로반환신청` | (필요시기재)기업으로반환신청 | checkbox (퇴직소득세  / 국민연금전환금) | 1쪽 [628, 463, 742, 476] | 늘 | 파일 key | 보기 중 고름: 퇴직소득세  / 국민연금전환금 | fields.json:311 | 묻기 |
| `check.지급방식` | 지급방식 | checkbox (전액지급 / 적립비율지급) | 1쪽 [813, 335, 907, 364] | 늘 | 파일 key | 보기 중 고름: 전액지급 / 적립비율지급 | fields.json:357 | 묻기 |
| `check.가입자단독청구` | 가입자단독청구 | checkbox (업체 폐업 / 기타 (사용자 지급 거절 등)) | 1쪽 [186, 857, 353, 870] | 늘 | 파일 key | 보기 중 고름: 업체 폐업 / 기타 (사용자 지급 거절 등) | fields.json:625 | 묻기 |
| `seal.signer` | 가입자 | seal | 1쪽 [893, 820, 915, 832] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:712 | 묻기 |
| `sign.signer` | 가입자 | signature | 1쪽 [893, 820, 915, 832] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:712 | 묻기 |
| `seal.signer2` | 기업명 | seal | 1쪽 [432, 888, 483, 928] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:731 | 묻기 |
| `sign.signer2` | 기업명 | signature | 1쪽 [447, 902, 469, 915] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:731 | 묻기 |
| `seal.signer3` | 가입자 | seal | 1쪽 [759, 890, 795, 927] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:750 | 묻기 |
| `sign.signer3` | 가입자 | signature | 1쪽 [766, 902, 788, 915] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:750 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [791, 56, 837, 89] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [783, 48, 846, 96] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [852, 49, 916, 95] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [846, 48, 922, 96] | 늘 | - | - | - | 묻기 |

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
"퇴직연금 퇴직급여 지급신청서(DB)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "4,110,000",
 "661-023479-10631"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"4,110,000"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"661-023479-10631"
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
- 퇴직소득원천징수영수증: 퇴직소득원천징수영수증
- 타금융기관IRP또는요구불계좌사본: 타금융기관IRP또는요구불계좌사본
```

답:

```json
[{"key": "퇴직소득원천징수영수증", "value": "4,110,000", "bbox_2d": [832, 258, 907, 275], "page": 1},
 {"key": "타금융기관IRP또는요구불계좌사본", "value": "661-023479-10631", "bbox_2d": [552, 283, 699, 300], "page": 1}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf179 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf179` → `python -m docgen.formdir card hf179` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf179 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf179 --show` · `python -m docgen.preview hf179 --out work/hf179`
