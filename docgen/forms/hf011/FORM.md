# 예금(신탁)잔액증명 의뢰서 (`hf011`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf011 · card-hash: dbe500515d99 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 예금(신탁)잔액증명 의뢰서
- **쓰이는 업무:** 상속예금 지급
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf011 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.11 (예금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 20칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `account` | 계좌번호 | account_no | 1쪽 [247, 325, 374, 341] | 늘 | 규칙: '계좌번호' → `account` | 고객 정보 (키 `account`) | fields.json:289 | 묻기 |
| `account2` | 계좌번호 | account_no | 1쪽 [245, 347, 373, 365] | 늘 | 규칙: '계좌번호' → `account` | 고객 정보 (키 `account`) | fields.json:301 | 묻기 |
| `account3` | 계좌번호 | account_no | 1쪽 [248, 371, 376, 390] | 늘 | 규칙: '계좌번호' → `account` | 고객 정보 (키 `account`) | fields.json:313 | 묻기 |
| `발급기준일` | 발급기준일 | date | 1쪽 [640, 143, 764, 161] | 늘 | 항목명 그대로 | 값 종류 `date` (항목명 자동) | fields.json:489 | 묻기 |
| `국문` | 국문 | number | 1쪽 [666, 171, 683, 187] | 늘 | 항목명 그대로 | 값 종류 `count` (항목명 자동) | fields.json:501 | 묻기 |
| `매` | 매 | number | 1쪽 [665, 195, 682, 211] | 늘 | 표 행 (묶음·항목명 '매') | 값 종류 `count` (항목명 자동) | fields.json:514 | 묻기 |
| `발급부수` | 발급부수 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:616 | 묻기 |
| `발급부수2` | 발급부수 | text | - | 늘 | 항목명 그대로 | 값 종류 `text` (항목명 자동) | fields.json:629 | 묻기 |
| `customer.name` ← `signer.name` | 성명(상호명) | text | 1쪽 [313, 693, 386, 709] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:642 | 묻기 |
| `customer.name_en` | 영문명 | text | 1쪽 [256, 721, 395, 737] | 늘 | 규칙: '영문명' → `customer.name_en` | 고객 정보 (키 `customer.name_en`) | fields.json:660 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [253, 745, 614, 766] | 늘 | 규칙: '주소' → `customer.address` | 고객 정보 (키 `customer.address`) | fields.json:673 | 묻기 |
| `customer.birth` | 생년월일(사업자번호) | date | 1쪽 [639, 692, 712, 709] | 늘 | 규칙: '생년월일 (사업자번호)' → `customer.birth` | 고객 정보 (키 `customer.birth`) | fields.json:686 | 묻기 |
| `customer.phone` | 연락처 | phone | 1쪽 [644, 721, 747, 737] | 늘 | 규칙: '연락처' → `customer.phone` | 고객 정보 (키 `customer.phone`) | fields.json:698 | 묻기 |
| `agent.name` | 대리인성명 | text | 1쪽 [257, 795, 330, 811] | 늘 | 규칙: '대리인성명' → `agent.name` | 고객 정보 (키 `agent.name`) | fields.json:711 | 묻기 |
| `agent.relation` | 본인과의관계 | text | 1쪽 [256, 821, 274, 837] | 늘 | 규칙: '본인과의 관계' → `agent.relation` | 고객 정보 (키 `agent.relation`) | fields.json:723 | 묻기 |
| `agent.address` | 주소 | text | 1쪽 [255, 847, 615, 864] | 늘 | 규칙: '주소' → `agent.address` | 고객 정보 (키 `agent.address`) | fields.json:735 | 묻기 |
| `agent.birth` | 생년월일 | date | 1쪽 [640, 794, 710, 812] | 늘 | 규칙: '생년월일' → `agent.birth` | 고객 정보 (키 `agent.birth`) | fields.json:793 | 묻기 |
| `agent.phone` | 연락처 | phone | 1쪽 [643, 820, 743, 837] | 늘 | 규칙: '연락처' → `agent.phone` | 고객 정보 (키 `agent.phone`) | fields.json:805 | 묻기 |
| `취급점` | 취급점 | text | 1쪽 [256, 109, 329, 126] | 늘 | 항목명 그대로 | 값 종류 `branch` (항목명 자동) | fields.json:818 | 묻기 |
| `date` | 작성일 | date | 1쪽 [375, 647, 586, 664] | 늘 | 날짜 칸 (항목명) | 작성일 | fields.json:829 | 묻기 |

## 표 `계좌번호_목록` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `계좌번호_목록.*.value` | (통화코드:) | amount | - (1행) | 늘 | 표 행 (묶음·항목명 '(통화코드 : )') | 값 종류 `skip` (항목명 자동) | fields.json:529 | 묻기 |

## 체크·도장·서명 (marks) — 20칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.신청구분` | 신청구분 | checkbox (등록 / 변경 / 해제) | 1쪽 [316, 144, 364, 160] | 늘 | 체크 (항목명) | 보기 중 고름: 등록 / 변경 / 해제 | fields.json:61 | 묻기 |
| `check.대상계좌` | 대상계좌(발급세부) | checkbox (지정계좌 / 전체계좌) | 1쪽 [344, 186, 420, 202] | 늘 | 체크 (항목명) | 보기 중 고름: 지정계좌 / 전체계좌 | fields.json:122 | 묻기 |
| `check.대상계좌2` | 대상계좌(발급세부) | checkbox (계좌마스킹(계좌번호 일부숨김) / 발급용도 / 수수료 출금계좌) | 1쪽 [252, 241, 645, 274] | 늘 | 체크 (항목명) | 보기 중 고름: 계좌마스킹(계좌번호 일부숨김) / 발급용도 / 수수료 출금계좌 | fields.json:167 | 묻기 |
| `check.수령방법` | 수령방법 | checkbox (창구수령 / 카카오톡(문자) / E-mail) | 1쪽 [370, 300, 484, 315] | 늘 | 체크 (항목명) | 보기 중 고름: 창구수령 / 카카오톡(문자) / E-mail | fields.json:228 | 묻기 |
| `check.기준일자` | 기준일자 | checkbox (매월) | 1쪽 [252, 400, 308, 415] | 늘 | 체크 (항목명) | 보기 중 고름: 매월 | fields.json:325 | 묻기 |
| `check.유효기간` | 유효기간 | checkbox (보기1) | 1쪽 [252, 430, 267, 444] | 늘 | 체크 (항목명) | 보기 중 고름: ? | fields.json:354 | 묻기 |
| `check.창구수령대리인` | 창구수령대리인 | checkbox (성명 / 생년월일 / 관계) | 1쪽 [252, 455, 308, 470] | 늘 | 체크 (항목명) | 보기 중 고름: 성명 / 생년월일 / 관계 | fields.json:383 | 묻기 |
| `check.우편수령대리인` | 우편수령대리인 | checkbox (성명 / 주소) | 1쪽 [431, 481, 479, 496] | 늘 | 체크 (항목명) | 보기 중 고름: 성명 / 주소 | fields.json:444 | 묻기 |
| `check.수령방법2` | 수령방법 | checkbox (우편수령 ᄆ 창구수령 / E-mail) | 1쪽 [645, 392, 825, 407] | 늘 | 체크 (항목명) | 보기 중 고름: 우편수령 ᄆ 창구수령 / E-mail | fields.json:571 | 묻기 |
| `seal.customer` ← `seal.signer` | 성명(상호명) | seal | 1쪽 [450, 693, 509, 708] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:642 | 묻기 |
| `sign.customer` ← `sign.signer` | 성명(상호명) | signature | 1쪽 [450, 693, 509, 708] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:642 | 묻기 |
| `check.본인은상기계좌의` | 본인은상기계좌의( | checkbox (잔액증명서 발급 / 정기발급 신청) 과 관련한 일체의 행위를 상기 대리인에게) | 1쪽 [393, 875, 515, 890] | 늘 | 체크 (항목명) | 보기 중 고름: 잔액증명서 발급 / 정기발급 신청) 과 관련한 일체의 행위를 상기 대리인에게 | fields.json:748 | 묻기 |
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [597, 41, 655, 82] | 늘 | - | - | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [593, 40, 659, 83] | 늘 | - | - | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [663, 41, 722, 83] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [659, 40, 726, 83] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [734, 44, 784, 79] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [726, 40, 792, 83] | 늘 | - | - | - | 묻기 |
| `seal.staff.부점장` | 부점장 | seal | 1쪽 [868, 46, 913, 78] | 늘 | - | - | - | 묻기 |
| `sign.staff.부점장` | 부점장 | signature | 1쪽 [859, 40, 922, 83] | 늘 | - | - | - | 묻기 |

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
"예금(신탁)잔액증명 의뢰서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "540-121210-96628",
 "2024년 4월 19일",
 "36",
 "60",
 "남궁예태",
 "NAMGOONG YETAE",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "1985.03.28",
 "010-6144-1173",
 "남궁찬윤",
 "부",
 "1952.10.28",
 "010-7568-9115",
 "센텀지점"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"남궁찬윤"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"1952.10.28"
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
- account: 계좌번호 (같은 항목명 중 1번째 칸)
- account2: 계좌번호 (같은 항목명 중 2번째 칸)
- account3: 계좌번호 (같은 항목명 중 3번째 칸)
- 발급기준일: 발급기준일
- 국문: 국문
- 매: 매
- 발급부수: 발급부수 (같은 항목명 중 1번째 칸)
- 발급부수2: 발급부수 (같은 항목명 중 2번째 칸)
- customer.name: 성명(상호명) (고객 성명)
- customer.name_en: 영문명 (고객 영문 성명)
- customer.address: 주소 (고객 주소, 같은 항목명 중 1번째 칸)
- customer.birth: 생년월일(사업자번호) (고객 생년월일)
- customer.phone: 연락처 (고객 연락처, 같은 항목명 중 1번째 칸)
- agent.name: 대리인성명
- agent.relation: 본인과의관계 (대리인 관계)
- agent.address: 주소 (대리인 주소, 같은 항목명 중 2번째 칸)
- agent.birth: 생년월일 (대리인 생년월일)
- agent.phone: 연락처 (대리인 연락처, 같은 항목명 중 2번째 칸)
- 취급점: 취급점
- date: 작성일
```

답:

```json
[{"key": "account", "value": "540-121210-96628", "bbox_2d": [247, 325, 374, 341], "page": 1},
 {"key": "account2", "value": "540-121210-96628", "bbox_2d": [245, 347, 373, 365], "page": 1},
 {"key": "account3", "value": "540-121210-96628", "bbox_2d": [248, 371, 376, 390], "page": 1},
 {"key": "발급기준일", "value": "2024년 4월 19일", "bbox_2d": [640, 143, 764, 161], "page": 1},
 {"key": "국문", "value": "36", "bbox_2d": [666, 171, 683, 187], "page": 1},
 {"key": "매", "value": "60", "bbox_2d": [665, 195, 682, 211], "page": 1},
 {"key": "발급부수", "value": null},
 {"key": "발급부수2", "value": null},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [313, 693, 386, 709], "page": 1},
 {"key": "customer.name_en", "value": "NAMGOONG YETAE", "bbox_2d": [256, 721, 395, 737], "page": 1},
 {"key": "customer.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [253, 745, 614, 766], "page": 1},
 {"key": "customer.birth", "value": "1985.03.28", "bbox_2d": [639, 692, 712, 709], "page": 1},
 {"key": "customer.phone", "value": "010-6144-1173", "bbox_2d": [644, 721, 747, 737], "page": 1},
 {"key": "agent.name", "value": "남궁찬윤", "bbox_2d": [257, 795, 330, 811], "page": 1},
 {"key": "agent.relation", "value": "부", "bbox_2d": [256, 821, 274, 837], "page": 1},
 {"key": "agent.address", "value": "서울특별시 서초구 강남대로 357, 103동 1301호", "bbox_2d": [255, 847, 615, 864], "page": 1},
 {"key": "agent.birth", "value": "1952.10.28", "bbox_2d": [640, 794, 710, 812], "page": 1},
 {"key": "agent.phone", "value": "010-7568-9115", "bbox_2d": [643, 820, 743, 837], "page": 1},
 {"key": "취급점", "value": "센텀지점", "bbox_2d": [256, 109, 329, 126], "page": 1},
 {"key": "date", "value": "2025년 4월 1일", "bbox_2d": [375, 647, 586, 664], "page": 1}]
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
- check.신청구분: 신청구분 (체크박스, 보기: 등록 / 변경 / 해제)
- check.대상계좌: 대상계좌(발급세부) (같은 항목명 중 1번째 칸, 체크박스, 보기: 지정계좌 / 전체계좌)
- check.대상계좌2: 대상계좌(발급세부) (같은 항목명 중 2번째 칸, 체크박스, 보기: 계좌마스킹(계좌번호 일부숨김) / 발급용도 / 수수료 출금계좌)
- check.수령방법: 수령방법 (같은 항목명 중 1번째 칸, 체크박스, 보기: 창구수령 / 카카오톡(문자) / E-mail)
- check.기준일자: 기준일자 (체크박스, 보기: 매월)
- check.유효기간: 유효기간 (체크박스, 보기: 보기1)
- check.창구수령대리인: 창구수령대리인 (체크박스, 보기: 성명 / 생년월일 / 관계)
- check.우편수령대리인: 우편수령대리인 (체크박스, 보기: 성명 / 주소)
- check.수령방법2: 수령방법 (같은 항목명 중 2번째 칸, 체크박스, 보기: 우편수령 ᄆ 창구수령 / E-mail)
- seal.customer: 성명(상호명) (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 성명(상호명) (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- check.본인은상기계좌의: 본인은상기계좌의( (체크박스, 보기: 잔액증명서 발급 / 정기발급 신청) 과 관련한 일체의 행위를 상기 대리인에게)
- seal.staff.본인확인: 본인확인 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.본인확인: 본인확인 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.담당: 담당 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.담당: 담당 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.책임자: 책임자 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.책임자: 책임자 (같은 항목명 중 2번째 칸, 서명)
- seal.staff.부점장: 부점장 (같은 항목명 중 1번째 칸, 도장)
- sign.staff.부점장: 부점장 (같은 항목명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.신청구분", "value": "변경", "bbox_2d": [316, 145, 331, 160], "page": 1},
 {"key": "check.대상계좌", "value": "전체계좌", "bbox_2d": [344, 187, 359, 202], "page": 1},
 {"key": "check.대상계좌2", "value": null},
 {"key": "check.수령방법", "value": "카카오톡(문자)", "bbox_2d": [370, 301, 385, 315], "page": 1},
 {"key": "check.기준일자", "value": "매월", "bbox_2d": [252, 401, 267, 415], "page": 1},
 {"key": "check.유효기간", "value": "보기1", "bbox_2d": [252, 430, 267, 444], "page": 1},
 {"key": "check.창구수령대리인", "value": "성명", "bbox_2d": [252, 456, 267, 470], "page": 1},
 {"key": "check.우편수령대리인", "value": "주소", "bbox_2d": [431, 482, 446, 496], "page": 1},
 {"key": "check.수령방법2", "value": "우편수령 ᄆ 창구수령", "bbox_2d": [645, 393, 660, 407], "page": 1},
 {"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [450, 693, 509, 708], "page": 1},
 {"key": "check.본인은상기계좌의", "value": "잔액증명서 발급", "bbox_2d": [393, 876, 408, 890], "page": 1},
 {"key": "seal.staff.본인확인", "value": true, "bbox_2d": [597, 41, 655, 82], "page": 1},
 {"key": "sign.staff.본인확인", "value": false},
 {"key": "seal.staff.담당", "value": true, "bbox_2d": [663, 41, 722, 83], "page": 1},
 {"key": "sign.staff.담당", "value": false},
 {"key": "seal.staff.책임자", "value": true, "bbox_2d": [734, 44, 784, 79], "page": 1},
 {"key": "sign.staff.책임자", "value": false},
 {"key": "seal.staff.부점장", "value": true, "bbox_2d": [868, 46, 913, 78], "page": 1},
 {"key": "sign.staff.부점장", "value": false}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf011 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf011` → `python -m docgen.formdir card hf011` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | studio ① 서식 › 영역 편집에서 그리기 (`fields.json` items 에 한 칸) | 다시 |
| 답의 위치 (박스) | `fields.json` 그 칸의 `rect` [x0, y0, x1, y1] (pt) — 또는 영역 편집 | 다시 |
| 답의 키 | `fields.json` 그 칸에 `"key"` (없으면 규칙이 항목명으로 정함 — 모든 서식 공통 규칙은 studio 키 사전) | 다시 |
| 답의 값 | `fields.json` 그 칸에 `"source"` ([값 출처 목록](../_common/values.md)) 또는 값 종류 `"kind"` | 다시 |
| 칸의 항목명 | `fields.json` 그 칸의 `label` | 다시 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf011 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf011 --show` · `python -m docgen.preview hf011 --out work/hf011`
