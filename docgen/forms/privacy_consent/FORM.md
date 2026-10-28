# 개인(신용)정보 수집·이용·제공·조회 동의서 (`privacy_consent`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card privacy_consent · card-hash: fad4dd1edc90 -->

- **종류:** 코드 서식 (값은 generate.py 의 함수, 모양은 템플릿)
- **그룹:** bank_form · **쪽 수:** 1 (seed 1000000 로 그린 것) · **분류 정답:** 개인(신용)정보 수집·이용·제공·조회 동의서 (다른 이름: [필수] 개인(신용)정보 수집·이용·제공_동의서[가계여신_금융거래])
- **쓰이는 업무:** 개인 계좌개설, 개인 신용대출, 주택담보대출, 전세자금대출, 개인사업자 대출, 개인형IRP 개설, 전자금융 가입
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`

> 여신 금융거래용 개인(신용)정보 동의서 (필수/선택 동의).

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `generate.py` | 값 만들기 (코드 서식: 값 전부 / html 서식: adjust 로 칸끼리 관계) |
| `docgen/docs/bank_form_account.py`, `docgen/docs/bank_form_loan.py` (폴더 밖) | 같은 그룹 서식들이 같이 쓰는 도우미 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 12칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `bank.name` | 은행명 | text | 1쪽 [76, 33, 166, 49] | 늘 | generate.py | look/template.html.j2:19 | 묻기 |
| `providers.*.name` | 제공받는자 | text | 1쪽 [73, 359, 244, 368] (1행) | 늘 | generate.py | look/template.html.j2:40 | 묻기 |
| `providers.*.purpose` | 제공받는자의이용목적 | text | 1쪽 [276, 354, 508, 373] (1행) | 늘 | generate.py | look/template.html.j2:40 | 묻기 |
| `providers.*.items` | 제공하는항목 | text | 1쪽 [526, 354, 761, 373] (1행) | 늘 | generate.py | look/template.html.j2:41 | 묻기 |
| `providers.*.period` | 제공받는자의보유이용기간 | text | 1쪽 [782, 359, 938, 368] (1행) | 늘 | generate.py | look/template.html.j2:41 | 묻기 |
| `date` | 작성일 | date | 1쪽 [442, 713, 534, 722] | 늘 | generate.py | look/template.html.j2:69 | 묻기 |
| `customer.birth` ← `applicant.birth` | 생년월일 | date | 1쪽 [608, 713, 663, 722] | 늘 | generate.py | look/template.html.j2:70 | 묻기 |
| `customer.name` ← `applicant.name` | 본인성명 | text | 1쪽 [793, 708, 842, 718] | 늘 | generate.py | look/template.html.j2:16 | 묻기 |
| `bank_use.clerk` | 본인확인 | text | 1쪽 [890, 777, 929, 789] | 늘 | generate.py | look/template.html.j2:84 | 묻기 |
| `marketing.channels.*` | 연락방법 | - | - (1행) | 8/16 | generate.py | - | 묻기 |
| `agent.name` ← `legal_rep.name` | 법정대리인 | - | - | 3/16 | generate.py | look/template.html.j2:16 | 묻기 |
| `agent.relation` ← `legal_rep.relation` | 본인과의관계 | - | - | 3/16 | generate.py | look/template.html.j2:74 | 묻기 |

## 체크·도장·서명 (marks) — 13칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 값 출처 | 정한 곳 | 질문 |
|---|---|---|---|---|---|---|---|
| `consent.collect` | 수집이용동의 | checkbox (동의함 / 동의하지 않음) | 1쪽 [788, 291, 830, 302] | 늘 | generate.py | look/template.html.j2:32 | 묻기 |
| `consent.unique_id` | 고유식별정보처리동의 | checkbox (동의함 / 동의하지 않음) | 1쪽 [788, 307, 830, 318] | 늘 | generate.py | look/template.html.j2:33 | 묻기 |
| `consent.provide` | 제공동의 | checkbox (동의함 / 동의하지 않음) | 1쪽 [788, 437, 830, 448] | 늘 | generate.py | look/template.html.j2:45 | 묻기 |
| `consent.provide_unique_id` | 고유식별정보제공동의 | checkbox (동의함 / 동의하지 않음) | 1쪽 [788, 454, 830, 465] | 늘 | generate.py | look/template.html.j2:46 | 묻기 |
| `consent.inquiry` | 조회동의 | checkbox (동의함 / 동의하지 않음) | 1쪽 [788, 563, 830, 573] | 늘 | generate.py | look/template.html.j2:55 | 묻기 |
| `marketing.collect` | 마케팅수집이용동의 | checkbox (동의함 / 동의하지 않음) | 1쪽 [775, 643, 950, 654] | 늘 | generate.py | look/template.html.j2:63 | 묻기 |
| `marketing.provide` | 마케팅제공동의 | checkbox (동의함 / 동의하지 않음) | 1쪽 [775, 660, 950, 670] | 늘 | generate.py | look/template.html.j2:64 | 묻기 |
| `seal.customer` ← `seal.applicant` | 본인 | seal | 1쪽 [875, 708, 950, 719] | 13/16 | generate.py | - | 묻기 |
| `sign.customer` ← `sign.applicant` | 본인 | signature | 1쪽 [830, 699, 995, 726] | 13/16 | generate.py | - | 묻기 |
| `seal.staff.clerk` | 본인확인 | seal | 1쪽 [882, 764, 936, 802] | 늘 | generate.py | - | 묻기 |
| `marketing.channels` | 연락방법 | checkbox_multi (전화 / 문자메시지 / 이메일 / 우편 / 앱 푸시) | - | 늘 | generate.py | look/template.html.j2:65 | 묻기 |
| `seal.agent` ← `seal.legal_rep` | 법정대리인 | 도장 | - | 3/16 | generate.py | - | 묻기 |
| `sign.agent` ← `sign.legal_rep` | 법정대리인 | 서명 | - | 3/16 | generate.py | - | 묻기 |

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
"개인(신용)정보 수집·이용·제공·조회 동의서"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "국민은행",
 "신용정보집중기관(한국신용정보원)",
 "본인의 신용을 판단하기 위한 자료로 활용하거나 공공기관에서 정책자료로 활용",
 "개인식별정보, 신용거래정보, 신용도판단정보, 신용능력정보, 공공정보",
 "관련 법령 및 규약에서 정한 기간",
 "개인신용평가회사(NICE평가정보, 코리아크레딧뷰로)",
 "개인신용평가, 본인 실명 및 신용도 확인",
 "개인식별정보, 신용거래정보, 신용도판단정보",
 "제공 목적 달성 시까지",
 "지역신용보증재단, 서울보증보험",
 "보증심사 및 보증서 발급·관리",
 "개인식별정보, 신용거래정보, 신용능력정보",
 "보증거래 종료일로부터 5년",
 "2025년 04월 01일",
 "1985.03.28",
 "남궁예태",
 "석정재"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"개인식별정보, 신용거래정보, 신용능력정보"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"보증거래 종료일로부터 5년"
```

### 정보 추출 `kie` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로, "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 키는 그대로 쓰고, 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
- bank.name: 은행명
- providers.0.name: 제공받는자 (1행)
- providers.0.purpose: 제공받는자의이용목적 (1행)
- providers.0.items: 제공하는항목 (1행)
- providers.0.period: 제공받는자의보유이용기간 (1행)
- providers.1.name: 제공받는자 (2행)
- providers.1.purpose: 제공받는자의이용목적 (2행)
- providers.1.items: 제공하는항목 (2행)
- providers.1.period: 제공받는자의보유이용기간 (2행)
- providers.2.name: 제공받는자 (3행)
- providers.2.purpose: 제공받는자의이용목적 (3행)
- providers.2.items: 제공하는항목 (3행)
- providers.2.period: 제공받는자의보유이용기간 (3행)
- date: 작성일
- customer.birth: 생년월일 (고객 생년월일)
- customer.name: 본인성명 (고객 성명)
- bank_use.clerk: 본인확인
```

답:

```json
[{"key": "bank.name", "value": "국민은행", "bbox_2d": [76, 33, 166, 49], "page": 1},
 {"key": "providers.0.name", "value": "신용정보집중기관(한국신용정보원)", "bbox_2d": [73, 359, 244, 368], "page": 1},
 {"key": "providers.0.purpose", "value": "본인의 신용을 판단하기 위한 자료로 활용하거나 공공기관에서 정책자료로 활용", "bbox_2d": [276, 354, 508, 373], "page": 1},
 {"key": "providers.0.items", "value": "개인식별정보, 신용거래정보, 신용도판단정보, 신용능력정보, 공공정보", "bbox_2d": [526, 354, 761, 373], "page": 1},
 {"key": "providers.0.period", "value": "관련 법령 및 규약에서 정한 기간", "bbox_2d": [782, 359, 938, 368], "page": 1},
 {"key": "providers.1.name", "value": "개인신용평가회사(NICE평가정보, 코리아크레딧뷰로)", "bbox_2d": [59, 377, 258, 395], "page": 1},
 {"key": "providers.1.purpose", "value": "개인신용평가, 본인 실명 및 신용도 확인", "bbox_2d": [296, 381, 488, 390], "page": 1},
 {"key": "providers.1.items", "value": "개인식별정보, 신용거래정보, 신용도판단정보", "bbox_2d": [534, 381, 753, 390], "page": 1},
 {"key": "providers.1.period", "value": "제공 목적 달성 시까지", "bbox_2d": [806, 381, 913, 390], "page": 1},
 {"key": "providers.2.name", "value": "지역신용보증재단, 서울보증보험", "bbox_2d": [79, 399, 238, 407], "page": 1},
 {"key": "providers.2.purpose", "value": "보증심사 및 보증서 발급·관리", "bbox_2d": [321, 399, 464, 407], "page": 1},
 {"key": "providers.2.items", "value": "개인식별정보, 신용거래정보, 신용능력정보", "bbox_2d": [540, 399, 748, 407], "page": 1},
 {"key": "providers.2.period", "value": "보증거래 종료일로부터 5년", "bbox_2d": [794, 399, 925, 407], "page": 1},
 {"key": "date", "value": "2025년 04월 01일", "bbox_2d": [442, 713, 534, 722], "page": 1},
 {"key": "customer.birth", "value": "1985.03.28", "bbox_2d": [608, 713, 663, 722], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [793, 708, 842, 718], "page": 1},
 {"key": "bank_use.clerk", "value": "석정재", "bbox_2d": [890, 777, 929, 789], "page": 1}]
```

### 체크·도장·서명 `marks` — 답 꼴 list_box · 채점 vl_f1 (값+위치)

질문:

```
이 문서의 체크박스·도장·서명 상태와 위치를 확인해 JSON 목록으로 답하세요. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다.
- 체크박스: 체크된 보기마다 {"key": 키, "value": 보기 글자, "bbox_2d": 체크된 □ 위치, "page": 쪽}. 체크된 것이 없으면 {"key": 키, "value": null}
- 복수 선택: 체크된 보기마다 한 줄 (위와 같은 꼴)
- 도장·서명: {"key": 키, "value": true 또는 false, "bbox_2d": 찍힌 자리, "page": 쪽} (비어 있으면 value 만 false)
항목
- consent.collect: 수집이용동의 (체크박스, 보기: 동의함 / 동의하지 않음)
- consent.unique_id: 고유식별정보처리동의 (체크박스, 보기: 동의함 / 동의하지 않음)
- consent.provide: 제공동의 (체크박스, 보기: 동의함 / 동의하지 않음)
- consent.provide_unique_id: 고유식별정보제공동의 (체크박스, 보기: 동의함 / 동의하지 않음)
- consent.inquiry: 조회동의 (체크박스, 보기: 동의함 / 동의하지 않음)
- marketing.collect: 마케팅수집이용동의 (체크박스, 보기: 동의함 / 동의하지 않음)
- marketing.provide: 마케팅제공동의 (체크박스, 보기: 동의함 / 동의하지 않음)
- seal.customer: 본인 (고객 도장, 같은 항목명 중 1번째 칸, 도장)
- sign.customer: 본인 (고객 서명, 같은 항목명 중 2번째 칸, 서명)
- seal.staff.clerk: 본인확인 (도장)
- marketing.channels: 연락방법 (복수 선택, 보기: 전화 / 문자메시지 / 이메일 / 우편 / 앱 푸시)
```

답:

```json
[{"key": "consent.collect", "value": "동의함", "bbox_2d": [775, 291, 784, 302], "page": 1},
 {"key": "consent.unique_id", "value": "동의함", "bbox_2d": [775, 307, 784, 318], "page": 1},
 {"key": "consent.provide", "value": "동의함", "bbox_2d": [775, 437, 784, 448], "page": 1},
 {"key": "consent.provide_unique_id", "value": "동의함", "bbox_2d": [775, 454, 784, 465], "page": 1},
 {"key": "consent.inquiry", "value": "동의함", "bbox_2d": [775, 563, 784, 573], "page": 1},
 {"key": "marketing.collect", "value": null},
 {"key": "marketing.provide", "value": null},
 {"key": "seal.customer", "value": false},
 {"key": "sign.customer", "value": true, "bbox_2d": [830, 699, 995, 726], "page": 1},
 {"key": "seal.staff.clerk", "value": true, "bbox_2d": [882, 764, 936, 802], "page": 1},
 {"key": "marketing.channels", "value": null}]
```

이 서식에만 있는 질문(form_qa)은 없습니다 — `questions.json` 의 `extra` 로 더합니다.

## 고치려면

| 하고 싶은 것 | 어디를 | 그다음 |
|---|---|---|
| 항목(칸) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `generate.py` 가 돌려주는 dict 에 그 키 값 | 미리보기로 확인 → 재검수 → 카드 다시 만들기 |
| 칸 키·항목명 바꾸기 | `look/template.html.j2` 의 `f("키", label=…)` (질문만 바꾸려면 `questions.json`) | `questions … --check` |
| 값이 이상함·칸끼리 안 맞음 | `generate.py` (값 만드는 함수) | 재검수 |
| 모양·표·문구 | `look/template.html.j2` (studio html 편집) | 재검수 |
| 질문의 항목명·묻지 않기 | `questions.json`: `{"kie": {"items": [{"key": "…", "label": "…"}, {"key": "…", "ask": false}]}}` | 검수 필요 없음 |
| 질문 문장·답 꼴 | `questions.json`: `{"kie": {"prompt": "…\n{items}", "answer": "list"}}` (답 꼴을 바꾸면 문장도) | `questions … --check` |
| 이 서식만의 질문 | `questions.json`: `{"extra": [{"id", "prompt", "type": "number/yesno/text", "answer": "{키}"}]}` | |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` | 모든 카드 다시 만들기 |

확인: studio ① 서식 › 문항 Q/A · `python -m docgen.formdir questions privacy_consent --show` · `python -m docgen.preview privacy_consent --out work/privacy_consent`
