# 대출거래약정서(가계용) (`hana_personal_agreement`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hana_personal_agreement · card-hash: 78c64ab84a2e -->

- **종류:** html 서식 (값은 fields.json 의 값 출처, 모양은 템플릿)
- **그룹:** hana · **쪽 수:** 10 (seed 1000000 로 그린 것) · **분류 정답:** 대출거래약정서(가계용)
- **쓰이는 업무:** 없음 (서류 한 건 과제에만)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hana_personal_agreement --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 대출거래약정서(가계용) 공식 공개 서식의 인쇄 문구·표 배치를 대조한 HTML 견본. 원본 이미지·QR·직인은 제외, 기재값은 합성. 출처: https://image.kebhana.com/cont/download/documents/provide/0000003061040_20210325.pdf

## 파일

| 파일 | 정하는 것 |
|---|---|
| `look/template.html.j2` | 모양·칸 자리 (`{{ f("키", label="항목명") }}`) |
| `fields.json` | 칸 목록·값 출처 |
| `form.json` | 이름·그룹·출처 |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·키 사전·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 54칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `customer.name` ← `official.name` | 본인 | text | 1쪽 [98, 287, 158, 302] | 늘 | 템플릿 | `profile.person.name` | look/template.html.j2:202 · fields.json:5 | 묻기 |
| `customer.address` ← `official.address` | 주소 | text | 1쪽 [368, 287, 689, 302] | 늘 | 템플릿 | `profile.person.address.road_short` | look/template.html.j2:203 · fields.json:10 | 묻기 |
| `official.subject` | 대출과목 | text | 1쪽 [199, 335, 289, 350] | 늘 | 템플릿 | `parent.loan.subject` | look/template.html.j2:204 · fields.json:15 | 묻기 |
| `official.amount` | 대출금액 | amount | 1쪽 [232, 363, 316, 376] | 늘 | 템플릿 | `parent.loan.amount` | look/template.html.j2:205 · fields.json:21 | 묻기 |
| `terms.rate` | 약정이율 | number | 1쪽 [395, 424, 421, 435] | 늘 | 템플릿 | `parent.loan.applied_rate` | look/template.html.j2:209 · fields.json:85 | 묻기 |
| `terms.start0` | 대출개시일년 | number | 1쪽 [234, 399, 260, 408] | 늘 | 템플릿 | `parent.loan.start_date` | look/template.html.j2:210 · fields.json:97 | 묻기 |
| `terms.start1` | 대출개시일월 | number | 1쪽 [311, 398, 324, 407] | 늘 | 템플릿 | `parent.loan.start_date` | look/template.html.j2:211 · fields.json:109 | 묻기 |
| `terms.start2` | 대출개시일일 | number | 1쪽 [370, 398, 383, 407] | 늘 | 템플릿 | `parent.loan.start_date` | look/template.html.j2:212 · fields.json:121 | 묻기 |
| `terms.end0` | 대출만료일년 | number | 1쪽 [657, 398, 683, 407] | 늘 | 템플릿 | `parent.loan.maturity` | look/template.html.j2:213 · fields.json:133 | 묻기 |
| `terms.end1` | 대출만료일월 | number | 1쪽 [739, 398, 752, 407] | 늘 | 템플릿 | `parent.loan.maturity` | look/template.html.j2:214 · fields.json:145 | 묻기 |
| `terms.end2` | 대출만료일일 | number | 1쪽 [800, 398, 813, 407] | 늘 | 템플릿 | `parent.loan.maturity` | look/template.html.j2:215 · fields.json:157 | 묻기 |
| `terms.late` | 연체가산율 | number | 1쪽 [548, 656, 555, 667] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:216 · fields.json:169 | 묻기 |
| `terms.max_late` | 최고연체율 | amount | 1쪽 [756, 657, 771, 667] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:217 · fields.json:181 | 묻기 |
| `terms.written0` | 작성일년 | number | 1쪽 [761, 30, 774, 39] | 늘 | 템플릿 | `parent.contract_date` | look/template.html.j2:220 · fields.json:217 | 묻기 |
| `terms.written1` | 작성일월 | number | 1쪽 [830, 30, 837, 39] | 늘 | 템플릿 | `parent.contract_date` | look/template.html.j2:221 · fields.json:231 | 묻기 |
| `terms.written2` | 작성일일 | number | 1쪽 [894, 30, 900, 39] | 늘 | 템플릿 | `parent.contract_date` | look/template.html.j2:222 · fields.json:243 | 묻기 |
| `official.amount_won` | 대출(한도)금액(₩) | amount | 1쪽 [533, 364, 603, 374] | 늘 | 템플릿 | `parent.loan.amount` | look/template.html.j2:223 · fields.json:255 | 묻기 |
| `official.start_date_check` | 대출개시일날짜지정 | text | 1쪽 [203, 399, 209, 407] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:224 · fields.json:267 | 묻기 |
| `official.maturity_date_check` | 대출기간만료일날짜지정 | text | 1쪽 [634, 398, 640, 407] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:225 · fields.json:279 | 묻기 |
| `official.prepay_target` | 중도상환해약금대상 | text | 1쪽 [203, 675, 209, 683] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:226 · fields.json:291 | 묻기 |
| `official.prepay_rate` | 중도상환해약금률(%) | amount | 1쪽 [448, 687, 462, 697] | 늘 | 템플릿 | `rule:percent` | look/template.html.j2:227 · fields.json:303 | 묻기 |
| `official.repay_lump_full` | 일시상환대출기간만료일에전액상환 | text | 1쪽 [342, 752, 349, 760] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:228 · fields.json:315 | 묻기 |
| `official.interest_monthly` | 이자지급매월지정일 | text | 1쪽 [203, 901, 209, 909] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:229 · fields.json:327 | 묻기 |
| `official.interest_day` | 이자지급일(매월○일) | amount | 1쪽 [253, 900, 260, 910] | 늘 | 템플릿 | `parent.loan.interest_pay` | look/template.html.j2:230 · fields.json:339 | 묻기 |
| `official.disburse_account` | 대출금입금(실행)계좌 | account_no | 3쪽 [303, 722, 495, 737] | 늘 | 템플릿 | `parent.loan.debit_account` | look/template.html.j2:420 · fields.json:353 | 묻기 |
| `official.debit_account` | 원(리)금및이자자동이체결제계좌 | account_no | 3쪽 [664, 722, 857, 737] | 늘 | 템플릿 | `parent.loan.debit_account` | look/template.html.j2:421 · fields.json:363 | 묻기 |
| `official.fee_consent_sign` | 비용의납부동의본인서명 | text | 3쪽 [754, 819, 805, 832] | 늘 | 템플릿 | `profile.person.name` | look/template.html.j2:422 · fields.json:373 | 묻기 |
| `official.amount_won_copy` | 대출(한도)금액(₩)(고객교부용) | amount | 4쪽 [533, 364, 603, 374] | 늘 | 템플릿 | `parent.loan.amount` | look/template.html.j2:614 · fields.json:261 | 묻기 |
| `official.start_date_check_copy` | 대출개시일날짜지정(고객교부용) | text | 4쪽 [203, 400, 209, 408] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:615 · fields.json:273 | 묻기 |
| `official.maturity_date_check_copy` | 대출기간만료일날짜지정(고객교부용) | text | 4쪽 [634, 398, 640, 407] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:616 · fields.json:285 | 묻기 |
| `official.prepay_target_copy` | 중도상환해약금대상(고객교부용) | text | 4쪽 [203, 674, 210, 682] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:617 · fields.json:297 | 묻기 |
| `official.prepay_rate_copy` | 중도상환해약금률(%)(고객교부용) | amount | 4쪽 [448, 687, 463, 698] | 늘 | 템플릿 | `rule:percent` | look/template.html.j2:618 · fields.json:309 | 묻기 |
| `official.repay_lump_full_copy` | 일시상환대출기간만료일에전액상환(고객교부용) | text | 4쪽 [342, 753, 349, 761] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:619 · fields.json:321 | 묻기 |
| `official.interest_monthly_copy` | 이자지급매월지정일(고객교부용) | text | 4쪽 [203, 899, 210, 907] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:620 · fields.json:333 | 묻기 |
| `official.interest_day_copy` | 이자지급일(매월○일)(고객교부용) | amount | 4쪽 [253, 897, 261, 909] | 늘 | 템플릿 | `parent.loan.interest_pay` | look/template.html.j2:621 · fields.json:346 | 묻기 |
| `official.name_copy` | 본인 | text | 6쪽 [98, 288, 139, 303] | 늘 | 템플릿 | `profile.person.name` | look/template.html.j2:811 · fields.json:27 | 묻기 |
| `official.address_copy` | 주소 | text | 6쪽 [371, 288, 661, 303] | 늘 | 템플릿 | `profile.person.address.road_short` | look/template.html.j2:812 · fields.json:32 | 묻기 |
| `official.subject_copy` | 대출과목 | text | 6쪽 [202, 332, 285, 347] | 늘 | 템플릿 | `parent.loan.subject` | look/template.html.j2:813 · fields.json:37 | 묻기 |
| `official.amount_copy` | 대출금액 | amount | 6쪽 [236, 364, 306, 374] | 늘 | 템플릿 | `parent.loan.amount` | look/template.html.j2:814 · fields.json:43 | 묻기 |
| `terms.rate_copy` | 약정이율 | number | 6쪽 [399, 421, 418, 433] | 늘 | 템플릿 | `parent.loan.applied_rate` | look/template.html.j2:818 · fields.json:91 | 묻기 |
| `terms.start0_copy` | 대출개시일년 | number | 6쪽 [237, 395, 256, 408] | 늘 | 템플릿 | `parent.loan.start_date` | look/template.html.j2:819 · fields.json:103 | 묻기 |
| `terms.start1_copy` | 대출개시일월 | number | 6쪽 [321, 396, 337, 408] | 늘 | 템플릿 | `parent.loan.start_date` | look/template.html.j2:820 · fields.json:115 | 묻기 |
| `terms.start2_copy` | 대출개시일일 | number | 6쪽 [373, 399, 380, 408] | 늘 | 템플릿 | `parent.loan.start_date` | look/template.html.j2:821 · fields.json:127 | 묻기 |
| `terms.end0_copy` | 대출만료일년 | number | 6쪽 [661, 395, 679, 408] | 늘 | 템플릿 | `parent.loan.maturity` | look/template.html.j2:822 · fields.json:139 | 묻기 |
| `terms.end1_copy` | 대출만료일월 | number | 6쪽 [743, 396, 749, 408] | 늘 | 템플릿 | `parent.loan.maturity` | look/template.html.j2:823 · fields.json:151 | 묻기 |
| `terms.end2_copy` | 대출만료일일 | number | 6쪽 [804, 399, 810, 408] | 늘 | 템플릿 | `parent.loan.maturity` | look/template.html.j2:824 · fields.json:163 | 묻기 |
| `terms.late_copy` | 연체가산율 | number | 6쪽 [552, 657, 558, 666] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:825 · fields.json:175 | 묻기 |
| `terms.max_late_copy` | 최고연체율 | amount | 6쪽 [760, 658, 768, 666] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:826 · fields.json:187 | 묻기 |
| `terms.written0_copy` | 작성일년 | number | 6쪽 [764, 30, 770, 38] | 늘 | 템플릿 | `parent.contract_date` | look/template.html.j2:829 · fields.json:224 | 묻기 |
| `terms.written1_copy` | 작성일월 | number | 6쪽 [834, 30, 839, 38] | 늘 | 템플릿 | `parent.contract_date` | look/template.html.j2:830 · fields.json:237 | 묻기 |
| `terms.written2_copy` | 작성일일 | number | 6쪽 [897, 30, 903, 38] | 늘 | 템플릿 | `parent.contract_date` | look/template.html.j2:831 · fields.json:249 | 묻기 |
| `official.disburse_account_copy` | 대출금입금(실행)계좌(고객교부용) | text | 6쪽 [303, 722, 495, 737] | 늘 | 템플릿 | `parent.loan.debit_account` | look/template.html.j2:832 · fields.json:358 | 묻기 |
| `official.debit_account_copy` | 원(리)금및이자자동이체결제계좌(고객교부용) | text | 6쪽 [664, 722, 857, 737] | 늘 | 템플릿 | `parent.loan.debit_account` | look/template.html.j2:833 · fields.json:368 | 묻기 |
| `official.fee_consent_sign_copy` | 비용의납부동의본인서명(고객교부용) | text | 6쪽 [754, 819, 805, 832] | 늘 | 템플릿 | `profile.person.name` | look/template.html.j2:834 · fields.json:378 | 묻기 |

## 체크·도장·서명 (marks) — 10칸

| 키 | 항목명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `terms.method` | 개별거래 | checkbox (개별거래) | 1쪽 [724, 341, 729, 342] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:206 · fields.json:49 | 묻기 |
| `terms.fixed` | 고정금리 | checkbox (고정금리) | 1쪽 [200, 420, 205, 421] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:207 · fields.json:61 | 묻기 |
| `terms.fixed_choice` | 확정금리 | checkbox (확정금리) | 1쪽 [341, 428, 346, 429] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:208 · fields.json:73 | 묻기 |
| `terms.execution` | 전액실행 | checkbox (전액실행) | 1쪽 [200, 707, 205, 708] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:218 · fields.json:193 | 묻기 |
| `terms.repay` | 만기일시상환 | checkbox (만기일시상환) | 1쪽 [200, 756, 208, 757] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:219 · fields.json:205 | 묻기 |
| `terms.method_copy` | 개별거래 | checkbox (개별거래) | 6쪽 [724, 341, 729, 342] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:815 · fields.json:55 | 묻기 |
| `terms.fixed_copy` | 고정금리 | checkbox (고정금리) | 6쪽 [200, 420, 205, 421] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:816 · fields.json:67 | 묻기 |
| `terms.fixed_choice_copy` | 확정금리 | checkbox (확정금리) | 6쪽 [341, 428, 346, 429] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:817 · fields.json:79 | 묻기 |
| `terms.execution_copy` | 전액실행 | checkbox (전액실행) | 6쪽 [200, 707, 205, 708] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:827 · fields.json:199 | 묻기 |
| `terms.repay_copy` | 만기일시상환 | checkbox (만기일시상환) | 6쪽 [200, 756, 208, 757] | 늘 | 템플릿 | `rule:fixed` | look/template.html.j2:828 · fields.json:211 | 묻기 |

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
"대출거래약정서(가계용)"
```

### 전체 받아쓰기 `ocr_page` · 채점 recall

질문:

```
이 문서 이미지에 보이는 모든 글자를 빠짐없이 읽어 텍스트로 옮기세요. 위에서 아래, 왼쪽에서 오른쪽 순서로 쓰고, 표는 한 행을 한 줄로 쓰세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
[
 "남궁예태",
 "서울특별시 서초구 강남대로 357, 103동 1301호",
 "주택담보대출",
 "301,000,000",
 "4.39",
 "2025",
 "04",
 "10",
 "2055",
 "3",
 "15",
 "25",
 "4",
 "7",
 "V",
 "20",
 "5",
 "국민은행 478303-40-826627"
]
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"서울특별시 서초구 강남대로 357, 103동 1301호"
```

### 값 칸 읽기 `ocr_field` · 채점 exact

질문:

```
이미지에 적힌 글자를 그대로 읽어 옮기세요. 설명 없이 읽은 글자만 출력하세요.
```

답:

```json
"4"
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
- customer.name: 본인 (고객 성명, 같은 항목명 중 1번째 칸)
- official.subject: 대출과목 (같은 항목명 중 1번째 칸)
- terms.rate: 약정이율 (같은 항목명 중 1번째 칸)
- terms.start1: 대출개시일월 (같은 항목명 중 1번째 칸)
- terms.start2: 대출개시일일 (같은 항목명 중 1번째 칸)
- terms.end0: 대출만료일년 (같은 항목명 중 1번째 칸)
- terms.end2: 대출만료일일 (같은 항목명 중 1번째 칸)
- terms.late: 연체가산율 (같은 항목명 중 1번째 칸)
- terms.max_late: 최고연체율 (같은 항목명 중 1번째 칸)
- terms.written0: 작성일년 (같은 항목명 중 1번째 칸)
- terms.written2: 작성일일 (같은 항목명 중 1번째 칸)
- official.amount_won: 대출(한도)금액(₩)
- official.start_date_check: 대출개시일날짜지정
- official.prepay_target: 중도상환해약금대상
- official.repay_lump_full: 일시상환대출기간만료일에전액상환
- official.interest_monthly: 이자지급매월지정일
- official.interest_day: 이자지급일(매월○일)
- official.disburse_account: 대출금입금(실행)계좌
- official.debit_account: 원(리)금및이자자동이체결제계좌
- official.fee_consent_sign: 비용의납부동의본인서명
- official.start_date_check_copy: 대출개시일날짜지정(고객교부용)
- official.maturity_date_check_copy: 대출기간만료일날짜지정(고객교부용)
- official.prepay_target_copy: 중도상환해약금대상(고객교부용)
- official.prepay_rate_copy: 중도상환해약금률(%)(고객교부용)
- official.interest_monthly_copy: 이자지급매월지정일(고객교부용)
- official.name_copy: 본인 (같은 항목명 중 2번째 칸)
- official.subject_copy: 대출과목 (같은 항목명 중 2번째 칸)
- terms.rate_copy: 약정이율 (같은 항목명 중 2번째 칸)
- terms.start0_copy: 대출개시일년 (같은 항목명 중 2번째 칸)
- terms.start1_copy: 대출개시일월 (같은 항목명 중 2번째 칸)
- terms.start2_copy: 대출개시일일 (같은 항목명 중 2번째 칸)
- terms.end0_copy: 대출만료일년 (같은 항목명 중 2번째 칸)
- terms.end1_copy: 대출만료일월 (같은 항목명 중 2번째 칸)
- terms.max_late_copy: 최고연체율 (같은 항목명 중 2번째 칸)
- terms.written0_copy: 작성일년 (같은 항목명 중 2번째 칸)
- terms.written1_copy: 작성일월 (같은 항목명 중 2번째 칸)
- terms.written2_copy: 작성일일 (같은 항목명 중 2번째 칸)
- official.disburse_account_copy: 대출금입금(실행)계좌(고객교부용)
- official.debit_account_copy: 원(리)금및이자자동이체결제계좌(고객교부용)
- official.fee_consent_sign_copy: 비용의납부동의본인서명(고객교부용)
```

답:

```json
[{"key": "customer.name", "value": "남궁예태", "bbox_2d": [98, 287, 158, 302], "page": 1},
 {"key": "official.subject", "value": "주택담보대출", "bbox_2d": [199, 335, 289, 350], "page": 1},
 {"key": "terms.rate", "value": "4.39", "bbox_2d": [395, 424, 421, 435], "page": 1},
 {"key": "terms.start1", "value": "04", "bbox_2d": [311, 398, 324, 407], "page": 1},
 {"key": "terms.start2", "value": "10", "bbox_2d": [370, 398, 383, 407], "page": 1},
 {"key": "terms.end0", "value": "2055", "bbox_2d": [657, 398, 683, 407], "page": 1},
 {"key": "terms.end2", "value": "10", "bbox_2d": [800, 398, 813, 407], "page": 1},
 {"key": "terms.late", "value": "3", "bbox_2d": [548, 656, 555, 667], "page": 1},
 {"key": "terms.max_late", "value": "15", "bbox_2d": [756, 657, 771, 667], "page": 1},
 {"key": "terms.written0", "value": "25", "bbox_2d": [761, 30, 774, 39], "page": 1},
 {"key": "terms.written2", "value": "7", "bbox_2d": [894, 30, 900, 39], "page": 1},
 {"key": "official.amount_won", "value": "301,000,000", "bbox_2d": [533, 364, 603, 374], "page": 1},
 {"key": "official.start_date_check", "value": "V", "bbox_2d": [203, 399, 209, 407], "page": 1},
 {"key": "official.prepay_target", "value": "V", "bbox_2d": [203, 675, 209, 683], "page": 1},
 {"key": "official.repay_lump_full", "value": "V", "bbox_2d": [342, 752, 349, 760], "page": 1},
 {"key": "official.interest_monthly", "value": "V", "bbox_2d": [203, 901, 209, 909], "page": 1},
 {"key": "official.interest_day", "value": "5", "bbox_2d": [253, 900, 260, 910], "page": 1},
 {"key": "official.disburse_account", "value": "국민은행 478303-40-826627", "bbox_2d": [303, 722, 495, 737], "page": 3},
 {"key": "official.debit_account", "value": "국민은행 478303-40-826627", "bbox_2d": [664, 722, 857, 737], "page": 3},
 {"key": "official.fee_consent_sign", "value": "남궁예태", "bbox_2d": [754, 819, 805, 832], "page": 3},
 {"key": "official.start_date_check_copy", "value": "V", "bbox_2d": [203, 400, 209, 408], "page": 4},
 {"key": "official.maturity_date_check_copy", "value": "V", "bbox_2d": [634, 398, 640, 407], "page": 4},
 {"key": "official.prepay_target_copy", "value": "V", "bbox_2d": [203, 674, 210, 682], "page": 4},
 {"key": "official.prepay_rate_copy", "value": "20", "bbox_2d": [448, 687, 463, 698], "page": 4},
 {"key": "official.interest_monthly_copy", "value": "V", "bbox_2d": [203, 899, 210, 907], "page": 4},
 {"key": "official.name_copy", "value": "남궁예태", "bbox_2d": [98, 288, 139, 303], "page": 6},
 {"key": "official.subject_copy", "value": "주택담보대출", "bbox_2d": [202, 332, 285, 347], "page": 6},
 {"key": "terms.rate_copy", "value": "4.39", "bbox_2d": [399, 421, 418, 433], "page": 6},
 {"key": "terms.start0_copy", "value": "2025", "bbox_2d": [237, 395, 256, 408], "page": 6},
 {"key": "terms.start1_copy", "value": "04", "bbox_2d": [321, 396, 337, 408], "page": 6},
 {"key": "terms.start2_copy", "value": "10", "bbox_2d": [373, 399, 380, 408], "page": 6},
 {"key": "terms.end0_copy", "value": "2055", "bbox_2d": [661, 395, 679, 408], "page": 6},
 {"key": "terms.end1_copy", "value": "04", "bbox_2d": [743, 396, 749, 408], "page": 6},
 {"key": "terms.max_late_copy", "value": "15", "bbox_2d": [760, 658, 768, 666], "page": 6},
 {"key": "terms.written0_copy", "value": "25", "bbox_2d": [764, 30, 770, 38], "page": 6},
 {"key": "terms.written1_copy", "value": "4", "bbox_2d": [834, 30, 839, 38], "page": 6},
 {"key": "terms.written2_copy", "value": "7", "bbox_2d": [897, 30, 903, 38], "page": 6},
 {"key": "official.disburse_account_copy", "value": "국민은행 478303-40-826627", "bbox_2d": [303, 722, 495, 737], "page": 6},
 {"key": "official.debit_account_copy", "value": "국민은행 478303-40-826627", "bbox_2d": [664, 722, 857, 737], "page": 6},
 {"key": "official.fee_consent_sign_copy", "value": "남궁예태", "bbox_2d": [754, 819, 805, 832], "page": 6}]
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
- terms.method: 개별거래 (같은 항목명 중 1번째 칸, 체크박스, 보기: 개별거래)
- terms.fixed: 고정금리 (같은 항목명 중 1번째 칸, 체크박스, 보기: 고정금리)
- terms.fixed_choice: 확정금리 (같은 항목명 중 1번째 칸, 체크박스, 보기: 확정금리)
- terms.execution: 전액실행 (같은 항목명 중 1번째 칸, 체크박스, 보기: 전액실행)
- terms.repay: 만기일시상환 (같은 항목명 중 1번째 칸, 체크박스, 보기: 만기일시상환)
- terms.method_copy: 개별거래 (같은 항목명 중 2번째 칸, 체크박스, 보기: 개별거래)
- terms.fixed_copy: 고정금리 (같은 항목명 중 2번째 칸, 체크박스, 보기: 고정금리)
- terms.fixed_choice_copy: 확정금리 (같은 항목명 중 2번째 칸, 체크박스, 보기: 확정금리)
- terms.execution_copy: 전액실행 (같은 항목명 중 2번째 칸, 체크박스, 보기: 전액실행)
- terms.repay_copy: 만기일시상환 (같은 항목명 중 2번째 칸, 체크박스, 보기: 만기일시상환)
```

답:

```json
[{"key": "terms.method", "value": "개별거래", "bbox_2d": [720, 336, 736, 347], "page": 1},
 {"key": "terms.fixed", "value": "고정금리", "bbox_2d": [196, 416, 210, 425], "page": 1},
 {"key": "terms.fixed_choice", "value": "확정금리", "bbox_2d": [338, 424, 351, 433], "page": 1},
 {"key": "terms.execution", "value": "전액실행", "bbox_2d": [196, 703, 210, 712], "page": 1},
 {"key": "terms.repay", "value": "만기일시상환", "bbox_2d": [196, 752, 210, 761], "page": 1},
 {"key": "terms.method_copy", "value": "개별거래", "bbox_2d": [720, 336, 736, 347], "page": 6},
 {"key": "terms.fixed_copy", "value": "고정금리", "bbox_2d": [196, 416, 210, 425], "page": 6},
 {"key": "terms.fixed_choice_copy", "value": "확정금리", "bbox_2d": [338, 424, 351, 433], "page": 6},
 {"key": "terms.execution_copy", "value": "전액실행", "bbox_2d": [196, 703, 210, 712], "page": 6},
 {"key": "terms.repay_copy", "value": "만기일시상환", "bbox_2d": [196, 752, 210, 761], "page": 6}]
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hana_personal_agreement --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hana_personal_agreement` → `python -m docgen.formdir card hana_personal_agreement` (실제 질문→답 확인).

| 바꾸고 싶은 것 (데이터에서) | 어디를 | 검수 |
|---|---|---|
| 칸(추출 항목) 더하기 | `look/template.html.j2` 에 `{{ f("키", label="항목명") }}` + `fields.json` 의 `fields` 에 키·source | 다시 |
| 답의 키·칸의 항목명 | `look/template.html.j2` 의 `f("키", label=…)` + `fields.json` 의 그 키 | 다시 |
| 답의 값 | `fields.json` 의 그 칸 `source` ([값 출처 목록](../_common/values.md)) | 다시 |
| 칸끼리 관계 (합계·날짜 순서·조건) | `generate.py` 의 `adjust(d, p, rng)` | 다시 |
| 답의 위치 (박스) | `look/template.html.j2` 배치 (studio html 편집). 숫자로 고정하려면 `fields.json` `regions` | 다시 |
| (칸 줄이 없는 칸의 질문 설정) | `fields.json` 맨 위에 `"q": {"키": {"ask": false}}` (반복 행은 `rows.*.amount`) | 필요 없음 |
| 질문에서 이 칸을 빼기 | `fields.json` 그 칸에 `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | `fields.json` 그 칸에 `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸에 `"q": {"ocr": false}` | 필요 없음 |
| 질문 문장 | `questions.json`: `{"kie": {"prompt": "…\n{items}"}}` | 필요 없음 |
| 답 모양 (JSON) | `questions.json`: `{"kie": {"answer": {"key": "{key}", "value": "{value}"}}}` (답 항목 하나의 틀. 위 예는 위치 없이 — 질문 문장도 같은 꼴로) | 필요 없음 |
| 답 모양 (줄글) | `questions.json`: `{"kie": {"answer": "{label}: {value}"}}` (칸마다 한 줄) | 필요 없음 |
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hana_personal_agreement --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·키 사전·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hana_personal_agreement --show` · `python -m docgen.preview hana_personal_agreement --out work/hana_personal_agreement`
