# 거주자간 해외직접투자 양수도 신고(보고)서 (`hf264`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf264 · card-hash: dfb5f7c68c0a -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 2 (seed 1000000 로 그린 것) · **분류 정답:** 거주자간 해외직접투자 양수도 신고(보고)서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf264 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.264 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 23칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `signer.name` | 상호또는성명 | text | 1쪽 [311, 212, 379, 224] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:23 | 묻기 |
| `company.address` | 소재지(주소) | text | 1쪽 [248, 236, 572, 248] | 늘 | 파일 key | 고객 정보 (키 `company.address`, 없으면 값 종류 `address`) | fields.json:42 | 묻기 |
| `company.biz_no` | 사업자(주민등록)번호 | biz_no | 1쪽 [679, 212, 785, 224] | 늘 | 파일 key | 고객 정보 (키 `company.biz_no`, 없으면 값 종류 `biz_no`) | fields.json:133 | 묻기 |
| `signer2.name` | 상호또는성명 | text | 1쪽 [311, 306, 379, 318] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:146 | 묻기 |
| `company.biz_no2` | 사업자(주민등록)번호 | biz_no | 1쪽 [250, 330, 356, 342] | 늘 | 파일 key | 고객 정보 (키 `company.biz_no`, 없으면 값 종류 `biz_no`) | fields.json:165 | 묻기 |
| `company.address2` | 소재지(주소) | text | 1쪽 [248, 377, 572, 389] | 늘 | 파일 key | 고객 정보 (키 `company.address`, 없으면 값 종류 `address`) | fields.json:178 | 묻기 |
| `company.ceo` | 대표자명 | text | 1쪽 [677, 306, 745, 318] | 늘 | 파일 key | 고객 정보 (키 `company.ceo`, 없으면 값 종류 `text`) | fields.json:269 | 묻기 |
| `company.corp_no` | 법인등록번호 | corp_reg_no | 1쪽 [680, 330, 807, 342] | 늘 | 파일 key | 고객 정보 (키 `company.corp_no`, 없으면 값 종류 `number`) | fields.json:282 | 묻기 |
| `company.name` | 법인명 | text | 1쪽 [248, 471, 361, 483] | 늘 | 파일 key | 고객 정보 (키 `company.name`, 없으면 값 종류 `company`) | fields.json:295 | 묻기 |
| `company.address3` | 소재지(주소) | text | 1쪽 [249, 495, 573, 507] | 늘 | 파일 key | 고객 정보 (키 `company.address`, 없으면 값 종류 `address`) | fields.json:308 | 묻기 |
| `date` | 신고일자 | date | 1쪽 [249, 518, 385, 530] | 늘 | 파일 key | 고객 정보 (키 `date`, 없으면 값 종류 `date`) | fields.json:321 | 묻기 |
| `설립등기일` | 설립등기일 | date | 1쪽 [678, 471, 803, 483] | 늘 | 파일 key | 값 종류 `date` | fields.json:380 | 묻기 |
| `신고번호` | 신고번호 | rrn | 1쪽 [680, 518, 809, 530] | 늘 | 파일 key | 값 종류 `number` | fields.json:394 | 묻기 |
| `양수도일자` | 양수도일자 | date | 1쪽 [252, 613, 337, 625] | 늘 | 파일 key | 값 종류 `date` | fields.json:454 | 묻기 |
| `양수도가액` | 양수도가액 | number | 1쪽 [835, 613, 920, 625] | 늘 | 파일 key | 값 종류 `amount` | fields.json:468 | 묻기 |
| `신고번호2` | 신고번호 | text | 1쪽 [746, 742, 828, 754] | 늘 | 파일 key | 값 종류 `number` | fields.json:482 | 묻기 |
| `date2` | 신고일자 | date | 1쪽 [742, 765, 878, 777] | 늘 | 파일 key | 고객 정보 (키 `date`, 없으면 값 종류 `date`) | fields.json:496 | 묻기 |
| `date3` | 작성일 | date | 1쪽 [405, 680, 597, 697] | 늘 | 파일 key | 작성일 | fields.json:549 | 묻기 |
| `signer3.name` | 신고기관 | text | 1쪽 [772, 796, 823, 808] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:575 | 묻기 |
| `상호또는성명` | 상호또는성명 | text | 1쪽 [254, 212, 411, 224] | 늘 | 파일 key | 값 종류 `company` | fields.json:594 | 묻기 |
| `상호또는성명2` | 상호또는성명 | text | 1쪽 [256, 306, 353, 318] | 늘 | 파일 key | 값 종류 `company` | fields.json:609 | 묻기 |
| `담당자및연락처` | 담당자및연락처 | phone | 1쪽 [256, 353, 371, 365] | 늘 | 파일 key | 값 종류 `phone` | fields.json:624 | 묻기 |
| `지점` | 지점 | text | 1쪽 [782, 401, 850, 413] | 늘 | 파일 key | 값 종류 `branch` | fields.json:639 | 묻기 |

## 체크·도장·서명 (marks) — 11칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `seal.signer` | 상호또는성명 | seal | 1쪽 [449, 210, 476, 225] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:23 | 묻기 |
| `sign.signer` | 상호또는성명 | signature | 1쪽 [449, 210, 476, 225] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:23 | 묻기 |
| `check.투자자규모` | 투자자규모 | checkbox (대기업 / 중소기업 / 개인사업자 / 개인) | 1쪽 [353, 257, 436, 272] | 늘 | 파일 key | 보기 중 고름: 대기업 / 중소기업 / 개인사업자 / 개인 | fields.json:55 | 묻기 |
| `seal.signer2` | 상호또는성명 | seal | 1쪽 [448, 304, 476, 319] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:146 | 묻기 |
| `sign.signer2` | 상호또는성명 | signature | 1쪽 [448, 304, 476, 319] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:146 | 묻기 |
| `check.투자자규모2` | 투자자규모 | checkbox (대기업 / 중소기업 / 개인사업자 / 개인) | 1쪽 [353, 422, 436, 436] | 늘 | 파일 key | 보기 중 고름: 대기업 / 중소기업 / 개인사업자 / 개인 | fields.json:191 | 묻기 |
| `check.투자내역` | 투자내역 | checkbox (투자금액 / 투자비율) | 1쪽 [261, 540, 354, 554] | 늘 | 파일 key | 보기 중 고름: 투자금액 / 투자비율 | fields.json:334 | 묻기 |
| `check.투자지분양도내역` | 투자지분양도내역 | checkbox (투자금액 / 투자비율) | 1쪽 [261, 588, 678, 602] | 늘 | 파일 key | 보기 중 고름: 투자금액 / 투자비율 | fields.json:408 | 묻기 |
| `check.양수도내역` | 양수도내역( | checkbox (전액양수도 / 부분양수도) | 1쪽 [181, 566, 392, 580] | 늘 | 파일 key | 보기 중 고름: 전액양수도 / 부분양수도 | fields.json:509 | 묻기 |
| `seal.signer3` | 신고기관 | seal | 1쪽 [887, 783, 932, 820] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:575 | 묻기 |
| `sign.signer3` | 신고기관 | signature | 1쪽 [896, 794, 923, 809] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:575 | 묻기 |

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
"거주자간 해외직접투자 양수도 신고(보고)서"
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf264 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf264` → `python -m docgen.formdir card hf264` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf264 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf264 --show` · `python -m docgen.preview hf264 --out work/hf264`
