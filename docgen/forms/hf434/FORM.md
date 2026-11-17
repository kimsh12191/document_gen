# 세종특별자치시 지역개발채권 매입 신청서 (`hf434`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf434 · card-hash: 1790cf4cfcea -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 세종특별자치시 지역개발채권 매입 신청서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf434 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.434 (기타) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 24칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `채권매입금액` | 채권매입금액 | number | 1쪽 [606, 154, 661, 165] | 늘 | 파일 key | 값 종류 `amount` | fields.json:23 | 묻기 |
| `성명법인명` | 성명/법인명 | text | 1쪽 [242, 191, 343, 202] | 늘 | 파일 key | 값 종류 `company` | fields.json:38 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [245, 220, 541, 230] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:52 | 묻기 |
| `agent.name` | 대리인(성명) | text | 1쪽 [246, 243, 307, 254] | 늘 | 파일 key | 고객 정보 (키 `agent.name`, 없으면 값 종류 `text`) | fields.json:65 | 묻기 |
| `customer.rrn` | 주민등록번호(사업자등록번호) | rrn | 1쪽 [674, 191, 774, 202] | 늘 | 파일 key | 고객 정보 (키 `customer.rrn`, 없으면 값 종류 `number`) | fields.json:78 | 묻기 |
| `customer.rrn2` | 주민등록번호 | rrn | 1쪽 [687, 244, 770, 253] | 늘 | 파일 key | 고객 정보 (키 `customer.rrn`, 없으면 값 종류 `number`) | fields.json:91 | 묻기 |
| `customer.phone` | 연락처 | phone | 1쪽 [740, 220, 842, 230] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:104 | 묻기 |
| `징구기관` | 징구기관 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:117 | 묻기 |
| `customer.phone2` | 연락처 | phone | 1쪽 [739, 275, 842, 286] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:131 | 묻기 |
| `증서번호` | 증서번호 | text | 1쪽 [598, 487, 696, 498] | 늘 | 파일 key | 값 종류 `check_no` | fields.json:352 | 묻기 |
| `매출일자` | 매출일자 | date | 1쪽 [601, 503, 679, 514] | 늘 | 파일 key | 값 종류 `date` | fields.json:366 | 묻기 |
| `매출점` | 매출점 | number | 1쪽 [715, 520, 800, 530] | 늘 | 파일 key | 값 종류 `amount` | fields.json:380 | 묻기 |
| `customer.address2` | 주소 | text | 1쪽 [180, 536, 504, 546] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:394 | 묻기 |
| `수납금액` | 수납금액 | number | 1쪽 [724, 552, 800, 562] | 늘 | 파일 key | 값 종류 `amount` | fields.json:407 | 묻기 |
| `소득세` | 소득세 | number | 1쪽 [732, 605, 800, 616] | 늘 | 파일 key | 값 종류 `amount` | fields.json:421 | 묻기 |
| `법인세` | 법인세 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:435 | 묻기 |
| `지방소득세` | 지방소득세 | number | 1쪽 [732, 637, 800, 648] | 늘 | 파일 key | 값 종류 `amount` | fields.json:449 | 묻기 |
| `농특세` | 농특세 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:463 | 묻기 |
| `date` | 작성일 | date | 1쪽 [373, 829, 558, 846] | 늘 | 파일 key | 작성일 | fields.json:477 | 묻기 |
| `signer.name` | 신청인 | text | 1쪽 [355, 869, 416, 880] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:503 | 묻기 |
| `signer2.name` | (대리인 | text | - | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:522 | 묻기 |
| `위탁` | 위탁 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:541 | 묻기 |
| `date2` | 작성일 | date | 2쪽 [698, 731, 907, 748] | 늘 | 파일 key | 작성일 | fields.json:684 | 묻기 |
| `signer3.name` | 성명 | text | 2쪽 [708, 761, 769, 771] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:710 | 묻기 |

## 체크·도장·서명 (marks) — 15칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.즉시매도시` | 즉시매도시 | checkbox (보기1) | 1쪽 [621, 354, 635, 368] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:144 | 묻기 |
| `check.만기시하나은행본인계좌로원리금자동상환` | 만기시하나은행본인계좌로원리금자동상환 | checkbox (하나은행 계좌번호 () | 1쪽 [571, 376, 722, 391] | 늘 | 파일 key | 보기 중 고름: 하나은행 계좌번호 ( | fields.json:174 | 묻기 |
| `check.만기시증권회사본인계좌로원리금자동상환` | 만기시증권회사본인계좌로원리금자동상환 | checkbox (하나금융투자 계좌번호 () | 1쪽 [571, 400, 752, 415] | 늘 | 파일 key | 보기 중 고름: 하나금융투자 계좌번호 ( | fields.json:204 | 묻기 |
| `check.만기시직접내점하여원리금상환` | 만기시직접내점하여원리금상환 | checkbox (보기1) | 1쪽 [571, 424, 585, 438] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:234 | 묻기 |
| `check.자동차신규등록` | 자동차신규등록(1) | checkbox (자동차신규등록(1) / 자동차이전등록(2) / 건설기계등록(3) / 기타허가☞신고(6) / 각종 계약체결(7)) | 1쪽 [565, 321, 706, 336] | 늘 | 파일 key | 보기 중 고름: 자동차신규등록(1) / 자동차이전등록(2) / 건설기계등록(3) / 기타허가☞신고(6) / 각종 계약체결(7) | fields.json:264 | 묻기 |
| `seal.signer` | 신청인 | seal | 1쪽 [484, 867, 547, 882] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:503 | 묻기 |
| `sign.signer` | 신청인 | signature | 1쪽 [484, 867, 547, 882] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:503 | 묻기 |
| `seal.signer2` | (대리인 | seal | 1쪽 [485, 891, 548, 905] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:522 | 묻기 |
| `sign.signer2` | (대리인 | signature | 1쪽 [485, 891, 548, 905] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:522 | 묻기 |
| `check.개인정보수집및이용내역` | 개인정보수집및이용내역 | checkbox (개인정보 수집 및 이용 내역) | 2쪽 [92, 199, 293, 213] | 늘 | 파일 key | 보기 중 고름: 개인정보 수집 및 이용 내역 | fields.json:556 | 묻기 |
| `check.동의함` | 동의함 | checkbox (동의함 / 동의하지 않음) | 2쪽 [637, 355, 909, 369] | 늘 | 파일 key | 보기 중 고름: 동의함 / 동의하지 않음 | fields.json:580 | 묻기 |
| `check.개인정보3자제공내역` | 개인정보3자제공내역 | checkbox (개인정보 3자 제공 내역) | 2쪽 [92, 410, 267, 425] | 늘 | 파일 key | 보기 중 고름: 개인정보 3자 제공 내역 | fields.json:620 | 묻기 |
| `check.동의함2` | 동의함 | checkbox (동의함 / 동의하지 않음) | 2쪽 [795, 586, 909, 601] | 늘 | 파일 key | 보기 중 고름: 동의함 / 동의하지 않음 | fields.json:644 | 묻기 |
| `seal.signer3` | 성명 | seal | 2쪽 [814, 759, 909, 773] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:710 | 묻기 |
| `sign.signer3` | 성명 | signature | 2쪽 [814, 759, 909, 773] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:710 | 묻기 |

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
"세종특별자치시 지역개발채권 매입 신청서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "580,000",
 "(주)미래케미칼",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "남궁찬윤",
 "850328-2******",
 "010-6144-1173",
 "가라15331099",
 "2025-03-30",
 "273,730,000",
 "66,620,000",
 "8,630,000",
 "4,840,000",
 "남궁예태"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"가라15331099"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"66,620,000"
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
- 채권매입금액: 채권매입금액
- 성명법인명: 성명/법인명
- customer.address: 주소 (같은 설명 중 1번째 칸)
- agent.name: 대리인(성명)
- customer.rrn: 주민등록번호(사업자등록번호)
- customer.rrn2: 주민등록번호
- customer.phone: 연락처 (같은 설명 중 1번째 칸)
- customer.phone2: 연락처 (같은 설명 중 2번째 칸)
- 증서번호: 증서번호
- 매출일자: 매출일자
- 매출점: 매출점
- customer.address2: 주소 (같은 설명 중 2번째 칸)
- 수납금액: 수납금액
- 소득세: 소득세
- 지방소득세: 지방소득세
- date: 작성일
- signer.name: 신청인
```

답:

```json
[{"key": "채권매입금액", "value": "580,000", "bbox_2d": [606, 154, 661, 165], "page": 1},
 {"key": "성명법인명", "value": "(주)미래케미칼", "bbox_2d": [242, 191, 343, 202], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [245, 220, 541, 230], "page": 1},
 {"key": "agent.name", "value": "남궁찬윤", "bbox_2d": [246, 243, 307, 254], "page": 1},
 {"key": "customer.rrn", "value": "850328-2******", "bbox_2d": [674, 191, 774, 202], "page": 1},
 {"key": "customer.rrn2", "value": "850328-2******", "bbox_2d": [687, 244, 770, 253], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [740, 220, 842, 230], "page": 1},
 {"key": "customer.phone2", "value": "010-6144-1173", "bbox_2d": [739, 275, 842, 286], "page": 1},
 {"key": "증서번호", "value": "가라15331099", "bbox_2d": [598, 487, 696, 498], "page": 1},
 {"key": "매출일자", "value": "2025-03-30", "bbox_2d": [601, 503, 679, 514], "page": 1},
 {"key": "매출점", "value": "273,730,000", "bbox_2d": [715, 520, 800, 530], "page": 1},
 {"key": "customer.address2", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [180, 536, 504, 546], "page": 1},
 {"key": "수납금액", "value": "66,620,000", "bbox_2d": [724, 552, 800, 562], "page": 1},
 {"key": "소득세", "value": "8,630,000", "bbox_2d": [732, 605, 800, 616], "page": 1},
 {"key": "지방소득세", "value": "4,840,000", "bbox_2d": [732, 637, 800, 648], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [373, 829, 558, 846], "page": 1},
 {"key": "signer.name", "value": "남궁예태", "bbox_2d": [355, 869, 416, 880], "page": 1}]
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
- check.즉시매도시: 즉시매도시 (체크박스, 보기: 보기1)
- check.만기시하나은행본인계좌로원리금자동상환: 만기시하나은행본인계좌로원리금자동상환 (체크박스, 보기: 하나은행 계좌번호 ()
- check.만기시증권회사본인계좌로원리금자동상환: 만기시증권회사본인계좌로원리금자동상환 (체크박스, 보기: 하나금융투자 계좌번호 ()
- check.만기시직접내점하여원리금상환: 만기시직접내점하여원리금상환 (체크박스, 보기: 보기1)
- check.자동차신규등록: 자동차신규등록(1) (체크박스, 보기: 자동차신규등록(1) / 자동차이전등록(2) / 건설기계등록(3) / 기타허가☞신고(6) / 각종 계약체결(7))
- seal.signer: 신청인 (같은 설명 중 1번째 칸, 도장)
- sign.signer: 신청인 (같은 설명 중 2번째 칸, 서명)
- seal.signer2: (대리인 (같은 설명 중 1번째 칸, 도장)
- sign.signer2: (대리인 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.즉시매도시", "value": "보기1", "bbox_2d": [621, 354, 635, 368], "page": 1},
 {"key": "check.만기시하나은행본인계좌로원리금자동상환", "value": "하나은행 계좌번호 (", "bbox_2d": [571, 377, 585, 391], "page": 1},
 {"key": "check.만기시증권회사본인계좌로원리금자동상환", "value": null},
 {"key": "check.만기시직접내점하여원리금상환", "value": "보기1", "bbox_2d": [571, 424, 585, 438], "page": 1},
 {"key": "check.자동차신규등록", "value": "기타허가☞신고(6)", "bbox_2d": [565, 322, 579, 336], "page": 1},
 {"key": "seal.signer", "value": false},
 {"key": "sign.signer", "value": false},
 {"key": "seal.signer2", "value": false},
 {"key": "sign.signer2", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf434 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf434` → `python -m docgen.formdir card hf434` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf434 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf434 --show` · `python -m docgen.preview hf434 --out work/hf434`
