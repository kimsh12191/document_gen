# 주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(국문) (`hf204`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf204 · card-hash: b548b27fcb70 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 4 (seed 1000000 로 그린 것) · **분류 정답:** 주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(국문)
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf204 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.204 (외환) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 46칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `접수일` | 접수일 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:61 | 묻기 |
| `처리일` | 처리일 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:75 | 묻기 |
| `customer.address` | 주소(영문) | text | 1쪽 [264, 152, 712, 180] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:151 | 묻기 |
| `하려는사업` | 하려는(하고있는)사업 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:165 | 묻기 |
| `value` | (국문) | amount | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:179 | 묻기 |
| `value2` | (영문) | amount | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:193 | 묻기 |
| `본사` | 본사 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:207 | 묻기 |
| `주공장소재지` | 주공장(주사업장)소재지 | text | 1쪽 [402, 259, 807, 291] | 늘 | 파일 key | 값 종류 `address` | fields.json:222 | 묻기 |
| `금번투자지역` | 금번투자지역(신주취득및출연의경우) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:237 | 묻기 |
| `액면총액` | 액면총액(A×B) | number | 1쪽 [503, 673, 621, 697] | 늘 | 파일 key | 값 종류 `amount` | fields.json:252 | 묻기 |
| `금번투자에따른예상근로자수` | 금번투자에따른예상근로자수 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:266 | 묻기 |
| `취득총액` | 취득총액(A×C) | number | 1쪽 [809, 674, 913, 698] | 늘 | 파일 key | 값 종류 `amount` | fields.json:281 | 묻기 |
| `customer.nationality` | 국적 | text | 1쪽 [770, 125, 852, 150] | 늘 | 파일 key | 고객 정보 (키 `customer.nationality`, 없으면 값 종류 `text`) | fields.json:295 | 묻기 |
| `취득총액원` | 취득총액:원(USD상당) | number | 1쪽 [849, 706, 875, 730] | 늘 | 파일 key | 값 종류 `percent` | fields.json:308 | 묻기 |
| `date` | 작성일 | date | 1쪽 [704, 820, 929, 836] | 늘 | 파일 key | 작성일 | fields.json:444 | 묻기 |
| `signer.name` | 신고인또는신청인 | text | 1쪽 [669, 829, 748, 851] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:470 | 묻기 |
| `신고번호` | 신고(허가)번호 | text | 1쪽 [184, 888, 369, 911] | 늘 | 파일 key | 값 종류 `number` | fields.json:489 | 묻기 |
| `date2` | 작성일 | date | 1쪽 [696, 925, 929, 940] | 늘 | 파일 key | 작성일 | fields.json:503 | 묻기 |
| `접수번호` | 접수번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:529 | 묻기 |
| `기존주취득시` | 기존주취득시 | number | 1쪽 [635, 355, 731, 378] | 늘 | 파일 key | 값 종류 `amount` | fields.json:544 | 묻기 |
| `취득전` | 취득(출연)전 | number | 1쪽 [500, 370, 599, 395] | 늘 | 파일 key | 값 종류 `amount` | fields.json:560 | 묻기 |
| `취득후` | 취득(출연)후 | number | 1쪽 [750, 370, 882, 394] | 늘 | 파일 key | 값 종류 `amount` | fields.json:576 | 묻기 |
| `의내용` | 의내용 | text | 1쪽 [307, 679, 355, 691] | 늘 | 파일 key | 값 종류 `note` | fields.json:592 | 묻기 |
| `접수일2` | 접수일 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:607 | 묻기 |
| `처리일2` | 처리일 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:621 | 묻기 |
| `customer.address2` | 주소(영문) | text | 2쪽 [265, 152, 713, 182] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:697 | 묻기 |
| `하려는사업2` | 하려는(하고있는)사업 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:711 | 묻기 |
| `value3` | (국문) | amount | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:725 | 묻기 |
| `value4` | (영문) | amount | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:739 | 묻기 |
| `본사2` | 본사 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:753 | 묻기 |
| `주공장소재지2` | 주공장(주사업장)소재지 | text | 2쪽 [406, 262, 809, 288] | 늘 | 파일 key | 값 종류 `address` | fields.json:768 | 묻기 |
| `금번투자지역2` | 금번투자지역(신주취득및출연의경우) | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:783 | 묻기 |
| `액면총액2` | 액면총액(A×B) | number | 2쪽 [538, 673, 624, 698] | 늘 | 파일 key | 값 종류 `amount` | fields.json:798 | 묻기 |
| `금번투자에따른예상근로자수2` | 금번투자에따른예상근로자수 | text | - | 늘 | 파일 key | 값 종류 `text` | fields.json:812 | 묻기 |
| `취득총액2` | 취득총액(A×C) | number | 2쪽 [792, 672, 910, 697] | 늘 | 파일 key | 값 종류 `amount` | fields.json:827 | 묻기 |
| `customer.nationality2` | 국적 | text | 2쪽 [774, 125, 856, 150] | 늘 | 파일 key | 고객 정보 (키 `customer.nationality`, 없으면 값 종류 `text`) | fields.json:841 | 묻기 |
| `취득총액원2` | 취득총액:원(USD상당) | number | 2쪽 [848, 706, 874, 730] | 늘 | 파일 key | 값 종류 `percent` | fields.json:854 | 묻기 |
| `date3` | 작성일 | date | 2쪽 [704, 820, 929, 836] | 늘 | 파일 key | 작성일 | fields.json:990 | 묻기 |
| `signer2.name` | 신고인또는신청인 | text | 2쪽 [673, 829, 751, 850] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:1016 | 묻기 |
| `신고번호2` | 신고(허가)번호 | rrn | 2쪽 [183, 891, 352, 912] | 늘 | 파일 key | 값 종류 `number` | fields.json:1035 | 묻기 |
| `date4` | 작성일 | date | 2쪽 [696, 925, 929, 940] | 늘 | 파일 key | 작성일 | fields.json:1049 | 묻기 |
| `접수번호2` | 접수번호 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:1075 | 묻기 |
| `기존주취득시2` | 기존주취득시 | number | 2쪽 [616, 356, 729, 379] | 늘 | 파일 key | 값 종류 `amount` | fields.json:1090 | 묻기 |
| `취득전2` | 취득(출연)전 | number | 2쪽 [500, 371, 601, 393] | 늘 | 파일 key | 값 종류 `amount` | fields.json:1106 | 묻기 |
| `취득후2` | 취득(출연)후 | number | 2쪽 [772, 370, 880, 395] | 늘 | 파일 key | 값 종류 `amount` | fields.json:1122 | 묻기 |
| `의내용2` | 의내용 | text | 2쪽 [307, 680, 355, 692] | 늘 | 파일 key | 값 종류 `note` | fields.json:1138 | 묻기 |

## 체크·도장·서명 (marks) — 18칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.개인` | 개인 | checkbox (외국법인 / 국제경제협력기구 / 보기3) | 1쪽 [214, 136, 437, 149] | 늘 | 파일 key | 보기 중 고름: 외국법인 / 국제경제협력기구 / ? | fields.json:89 | 묻기 |
| `check.방위사업법제3조제7호에따른방위산업물자를생산하는기업` | 「방위사업법」제3조제7호에따른방위산업물자를생산하는기업 | checkbox (보기1) | 1쪽 [894, 400, 908, 411] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:324 | 묻기 |
| `check.보기1` | 보기1 | checkbox (보기1) | 1쪽 [894, 418, 908, 429] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:354 | 묻기 |
| `check.보기12` | 보기1 | checkbox (보기1) | 1쪽 [894, 435, 908, 446] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:384 | 묻기 |
| `check.보기13` | 보기1 | checkbox (보기1) | 1쪽 [894, 453, 908, 464] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:414 | 묻기 |
| `seal.signer` | 신고인또는신청인 | seal | 1쪽 [863, 823, 915, 859] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:470 | 묻기 |
| `sign.signer` | 신고인또는신청인 | signature | 1쪽 [849, 835, 929, 848] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:470 | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [798, 39, 843, 71] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [785, 33, 856, 77] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [863, 38, 913, 73] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [856, 33, 920, 77] | 늘 | - | - | - | 묻기 |
| `check.개인2` | 개인 | checkbox (외국법인 / 국제경제협력기구 / 보기3) | 2쪽 [292, 136, 418, 149] | 늘 | 파일 key | 보기 중 고름: 외국법인 / 국제경제협력기구 / ? | fields.json:635 | 묻기 |
| `check.방위사업법제3조제7호에따른방위산업물자를생산하는기업2` | 「방위사업법」제3조제7호에따른방위산업물자를생산하는기업 | checkbox (보기1) | 2쪽 [894, 400, 908, 411] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:870 | 묻기 |
| `check.보기14` | 보기1 | checkbox (보기1) | 2쪽 [894, 418, 908, 429] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:900 | 묻기 |
| `check.보기15` | 보기1 | checkbox (보기1) | 2쪽 [894, 435, 908, 446] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:930 | 묻기 |
| `check.보기16` | 보기1 | checkbox (보기1) | 2쪽 [894, 453, 908, 464] | 늘 | 파일 key | 보기 중 고름: ? | fields.json:960 | 묻기 |
| `seal.signer2` | 신고인또는신청인 | seal | 2쪽 [849, 835, 929, 848] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:1016 | 묻기 |
| `sign.signer2` | 신고인또는신청인 | signature | 2쪽 [849, 835, 929, 848] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:1016 | 묻기 |

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
"주식등의 취득 또는 출연방식에 의한 외국인투자 신고서, 허가신청서(국문)"
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf204 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf204` → `python -m docgen.formdir card hf204` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf204 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf204 --show` · `python -m docgen.preview hf204 --out work/hf204`
