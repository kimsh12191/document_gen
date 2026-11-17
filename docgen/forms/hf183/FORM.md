# 퇴직연금 통지서비스 신청서(가입자용) (`hf183`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf183 · card-hash: 74b517ed7a3d -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 3 (seed 1000000 로 그린 것) · **분류 정답:** 퇴직연금 통지서비스 신청서(가입자용)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf183 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.183 (퇴직연금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 11칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `customer.name` | 성명(업체명) | text | 1쪽 [605, 175, 675, 187] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `person`) | fields.json:201 | 묻기 |
| `customer.birth` | 생년월일 | date | 1쪽 [630, 200, 826, 214] | 늘 | 파일 key | 작성일 | fields.json:214 | 묻기 |
| `customer.email` | E-mail주소 | text | 1쪽 [597, 276, 921, 302] | 늘 | 파일 key | 고객 정보 (키 `customer.email`, 없으면 값 종류 `email`) | fields.json:302 | 묻기 |
| `자택` | 자택 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:321 | 묻기 |
| `employer.name` | 직장 | text | 1쪽 [605, 332, 749, 344] | 늘 | 파일 key | 고객 정보 (키 `employer.name`, 없으면 값 종류 `text`) | fields.json:336 | 묻기 |
| `customer.home_phone` | 자택전화 | phone | 1쪽 [701, 357, 809, 369] | 늘 | 파일 key | 고객 정보 (키 `customer.home_phone`, 없으면 값 종류 `phone`) | fields.json:351 | 묻기 |
| `employer.phone` | 직장전화 | phone | 1쪽 [701, 384, 808, 396] | 늘 | 파일 key | 고객 정보 (키 `employer.phone`, 없으면 값 종류 `phone`) | fields.json:364 | 묻기 |
| `필수통지` | 필수(법적)통지 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:531 | 묻기 |
| `목표수익률에도달하면펀드자동환매` | 목표수익률에도달하면펀드자동환매 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:547 | 묻기 |
| `date` | 작성일 | date | 1쪽 [719, 110, 927, 124] | 늘 | 파일 key | 작성일 | fields.json:1039 | 묻기 |
| `signer.name` | 가입자 | text | 2쪽 [477, 314, 543, 325] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:1173 | 묻기 |

## 표 `년월일_목록` (표 과제 table·table_read·table_find·table_qa) — 1열

행 수는 서류마다 다르다 (모델이 정함). 표 칸은 kie 가 묻지 않는다. 열의 질문 설정(q)은 kie 칸과 같은 곳.

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `년월일_목록.*.은행사용란` | 은행사용란 | text | - (1행) | 늘 | 파일 key | 값 종류 `skip` | fields.json:64 | 묻기 |

## 체크·도장·서명 (marks) — 23칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.휴대전화` | 휴대전화 | checkbox (SKT  / KT  /  LGU+) | 1쪽 [844, 256, 872, 268] | 늘 | 파일 key | 보기 중 고름: SKT  / KT  /  LGU+ | fields.json:240 | 묻기 |
| `check.우편물수령처` | 우편물수령처 | checkbox (자택 / 직장 / 원치않음) | 1쪽 [605, 416, 663, 428] | 늘 | 파일 key | 보기 중 고름: 자택 / 직장 / 원치않음 | fields.json:377 | 묻기 |
| `check.전화연락처` | 전화연락처 | checkbox (자택 / 직장 / 휴대폰) | 1쪽 [806, 405, 842, 417] | 늘 | 파일 key | 보기 중 고름: 자택 / 직장 / 휴대폰 | fields.json:439 | 묻기 |
| `check.년월일` | 년월일 | checkbox (고객정보 ) | 1쪽 [844, 209, 904, 222] | 늘 | 파일 key | 보기 중 고름: 고객정보  | fields.json:501 | 묻기 |
| `check.상승자동환매` | 상승+%자동환매 | checkbox (하락 - % 자동환매 / 보기2) | 1쪽 [891, 751, 902, 762] | 늘 | 파일 key | 보기 중 고름: 하락 - % 자동환매 / ? | fields.json:561 | 묻기 |
| `check.상승자동환매2` | 상승+%자동환매 | checkbox (하락 - % 자동환매 / 보기2) | 1쪽 [891, 771, 902, 782] | 늘 | 파일 key | 보기 중 고름: 하락 - % 자동환매 / ? | fields.json:607 | 묻기 |
| `check.상승자동환매3` | 상승+%자동환매 | checkbox (하락 - % 자동환매 / 보기2) | 1쪽 [719, 790, 888, 802] | 늘 | 파일 key | 보기 중 고름: 하락 - % 자동환매 / ? | fields.json:653 | 묻기 |
| `check.운용현황보고서발송주기` | 운용현황보고서발송주기(기본값:분기발송) | checkbox (월 / 분기) | 1쪽 [737, 502, 774, 514] | 늘 | 파일 key | 보기 중 고름: 월 / 분기 | fields.json:699 | 묻기 |
| `check.원리금보장상품만기도래시전월통지발송` | 원리금보장상품(정기예금등)만기도래시전월통지발송 | checkbox (이메일 / 알림톡(LMS)) | 1쪽 [758, 525, 836, 537] | 늘 | 파일 key | 보기 중 고름: 이메일 / 알림톡(LMS) | fields.json:745 | 묻기 |
| `check.퇴직연금운용및자산관리약관이변경되는경우통지` | 퇴직연금운용및자산관리약관이변경되는경우통지 | checkbox (수신거부 / 이메일 / 알림톡(LMS)) | 1쪽 [766, 549, 814, 561] | 늘 | 파일 key | 보기 중 고름: 수신거부 / 이메일 / 알림톡(LMS) | fields.json:791 | 묻기 |
| `check.집합투자증권매수시예탁결제원의자산운용보고서수령방법` | 집합투자증권매수시예탁결제원의자산운용보고서수령방법 | checkbox (e-mail / 우편(직장→자택) / 수령거절 / 영업점 수령/홈페이지 확인) | 1쪽 [701, 567, 911, 590] | 늘 | 파일 key | 보기 중 고름: e-mail / 우편(직장→자택) / 수령거절 / 영업점 수령/홈페이지 확인 | fields.json:853 | 묻기 |
| `check.목표수익률에도달하면펀드자동환매` | 목표수익률에도달하면펀드자동환매 | checkbox (신청안함 / 등록/변경 / 해지) | 1쪽 [766, 633, 829, 645] | 늘 | 파일 key | 보기 중 고름: 신청안함 / 등록/변경 / 해지 | fields.json:931 | 묻기 |
| `check.신청` | 신청(미발송) | checkbox (신청(미발송) / 신청안함(발송)) | 1쪽 [701, 822, 778, 834] | 늘 | 파일 key | 보기 중 고름: 신청(미발송) / 신청안함(발송) | fields.json:993 | 묻기 |
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [734, 38, 782, 72] | 늘 | - | - | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [723, 32, 792, 78] | 늘 | - | - | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [800, 41, 839, 69] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [792, 32, 846, 78] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [846, 32, 921, 78] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [846, 32, 921, 78] | 늘 | - | - | - | 묻기 |
| `check.AI포트폴리오가입후매1년마다정기적으로리밸런싱을안내` | AI포트폴리오가입후매1년마다정기적으로리밸런싱을안내 | checkbox (이메일 / 알림톡(LMS)) | 2쪽 [701, 100, 749, 112] | 늘 | 파일 key | 보기 중 고름: 이메일 / 알림톡(LMS) | fields.json:1065 | 묻기 |
| `check.신청여부` | 신청여부 | checkbox (신청안함 / 이메일 / 알림톡(LMS)) | 2쪽 [827, 167, 905, 179] | 늘 | 파일 key | 보기 중 고름: 신청안함 / 이메일 / 알림톡(LMS) | fields.json:1111 | 묻기 |
| `seal.signer` | 가입자 | seal | 2쪽 [600, 302, 631, 338] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:1173 | 묻기 |
| `sign.signer` | 가입자 | signature | 2쪽 [606, 314, 625, 325] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:1173 | 묻기 |

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
"퇴직연금 통지서비스 신청서(가입자용)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
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
"남궁예태"
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
- signer.name: 가입자
```

답:

```json
[{"key": "signer.name", "value": "남궁예태", "bbox_2d": [477, 314, 543, 325], "page": 1}]
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
- check.AI포트폴리오가입후매1년마다정기적으로리밸런싱을안내: AI포트폴리오가입후매1년마다정기적으로리밸런싱을안내 (체크박스, 보기: 이메일 / 알림톡(LMS))
- check.신청여부: 신청여부 (체크박스, 보기: 신청안함 / 이메일 / 알림톡(LMS))
- seal.signer: 가입자 (같은 설명 중 1번째 칸, 도장)
- sign.signer: 가입자 (같은 설명 중 2번째 칸, 서명)
```

답:

```json
[{"key": "check.AI포트폴리오가입후매1년마다정기적으로리밸런싱을안내", "value": "이메일", "bbox_2d": [701, 101, 713, 112], "page": 1},
 {"key": "check.신청여부", "value": "알림톡(LMS)", "bbox_2d": [827, 168, 839, 179], "page": 1},
 {"key": "seal.signer", "value": true, "bbox_2d": [600, 302, 631, 338], "page": 1},
 {"key": "sign.signer", "value": false}]
```

### 표 찾기 `table_find` · 채점 f1_iou50 (위치)

질문:

```
이 문서에서 표를 모두 찾아 JSON 목록으로 답하세요. 여기서 표는 같은 항목 묶음(열)이 행마다 되풀이되고 행 수가 서류마다 달라지는 목록입니다. 항목명과 값이 번갈아 있는 신청서 칸, 칸 수가 정해진 결재란은 표가 아닙니다.
표마다 {{"columns": [머리글 글자, …], "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호, "n_rows": 행 수}} 를 쓰고, 여러 쪽에 걸친 표는 쪽마다 따로 씁니다. 좌표는 그 쪽 이미지 기준 0~1000 정수, 쪽 번호는 1부터입니다. 행 수에는 머리글·합계 행과 모두 빈 행을 넣지 않습니다. 표가 없으면 [] 로 답하세요.
```

답:

```json
[]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf183 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf183` → `python -m docgen.formdir card hf183` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf183 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf183 --show` · `python -m docgen.preview hf183 --out work/hf183`
