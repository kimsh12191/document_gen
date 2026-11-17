# 본인계좌 일괄지급정지 조회신청서 (`hf018`)

<!-- 자동 생성 — 직접 고치지 마세요. 다시 만들기: python -m docgen.formdir card hf018 · card-hash: 827aba32f251 -->

- **종류:** 원본 서식 (하나은행 원본 PDF 위에 칸을 얹음, 칸은 fields.json items)
- **그룹:** hana · **쪽 수:** 4 (seed 1000000 로 그린 것) · **분류 정답:** 본인계좌 일괄지급정지 조회신청서
- **질문·답:** 모두 기본 (공통 `docgen/forms/_common/questions.json` + 칸의 항목명). 바꾸려면 이 폴더에 `questions.json`
- **이 서식만의 질문:** 없음. 더하려면 이 폴더에 `qa.py` (견본: `python -m docgen.formdir qa hf018 --new`)
- **설명서:** [docgen/forms/README.md](../README.md) — 이 폴더의 파일마다 무엇이고 무엇을 고치면 데이터가 어떻게 바뀌는지

> 하나은행 공개 서식 No.18 (예금) 원본 위에 기재

## 파일

| 파일 | 정하는 것 |
|---|---|
| `fields.json` | 칸 목록·값 출처 |
| `layout.json` | 원본에서 자동 추출한 칸 자리 (초안) |
| `look/original.pdf` | 원본 PDF |
| `docgen/forms/_common/` (폴더 밖) | 모든 서식 공통: 기본 질문·바탕 틀 ([README](../_common/README.md)) |

## 추출 항목 (정보 추출 kie) — 13칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `customer.name` | 신청인 | text | 1쪽 [201, 245, 270, 257] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `text`) | fields.json:70 | 묻기 |
| `customer.phone` | 연락처 | phone | 1쪽 [199, 279, 314, 291] | 늘 | 파일 key | 고객 정보 (키 `customer.phone`, 없으면 값 종류 `phone`) | fields.json:84 | 묻기 |
| `customer.address` | 주소 | text | 1쪽 [200, 312, 564, 324] | 늘 | 파일 key | 고객 정보 (키 `customer.address`, 없으면 값 종류 `address`) | fields.json:98 | 묻기 |
| `customer.birth` | 생년월일 | date | 1쪽 [636, 245, 721, 257] | 늘 | 파일 key | 고객 정보 (키 `customer.birth`, 없으면 값 종류 `date`) | fields.json:112 | 묻기 |
| `customer.email` | E-mail | text | 1쪽 [636, 279, 802, 291] | 늘 | 파일 key | 고객 정보 (키 `customer.email`, 없으면 값 종류 `email`) | fields.json:126 | 묻기 |
| `customer.name2` | 신청인성명 | text | 1쪽 [644, 887, 712, 899] | 늘 | 파일 key | 고객 정보 (키 `customer.name`, 없으면 값 종류 `person`) | fields.json:536 | 묻기 |
| `date` | 작성일 | date | 1쪽 [357, 836, 573, 855] | 늘 | 파일 key | 작성일 | fields.json:550 | 묻기 |
| `서비스신청일로부터5년까지` | -서비스신청일로부터5년까지 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:576 | 묻기 |
| `신용거래정보` | ■신용거래정보 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:590 | 묻기 |
| `date2` | 작성일 | date | 2쪽 [331, 724, 540, 741] | 늘 | 파일 key | 작성일 | fields.json:697 | 묻기 |
| `signer.name` | 본인성명 | text | 2쪽 [758, 726, 827, 738] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:723 | 묻기 |
| `고객상담분쟁조정및민원처리` | -고객상담,분쟁조정및민원처리 | text | - | 늘 | 파일 key | 값 종류 `skip` | fields.json:742 | 묻기 |
| `성명연락처` | 성명,연락처 | phone | 2쪽 [366, 544, 481, 556] | 늘 | 파일 key | 값 종류 `phone` | fields.json:757 | 묻기 |

## 체크·도장·서명 (marks) — 12칸

| 키 | 키 설명 | 타입 | 위치 (쪽, 0~1000) | 나옴 | 키는 | 값은 | 고칠 곳 | 질문 |
|---|---|---|---|---|---|---|---|---|
| `check.금융기관별조회` | ■금융기관별조회(※요청기관V체크) | checkbox (전체 금융기관 / 전체 은행 / 하나 / 신한 / 국민 / 우리 / 기업 / 농협 / 수협 / SC제일 / 시티 / 산업 / 대구 / 부산 / 광주 / 제주 / 전북 / 경남 / 케이 / 카카오 / 기타 () | 1쪽 [422, 435, 478, 449] | 늘 | 파일 key | 보기 중 고름: 전체 금융기관 / 전체 은행 / 하나 / 신한 / 국민 / 우리 / 기업 / 농협 / 수협 / SC제일 / 시티 / 산업 / 대구 / 부산 / 광주 / 제주 / 전북 / 경남 / 케이 / 카카오 / 기타 ( | fields.json:140 | 묻기 |
| `check.수령함` | 수령함 | checkbox (수령함 / 수령거절) | 1쪽 [788, 792, 863, 807] | 늘 | 파일 key | 보기 중 고름: 수령함 / 수령거절 | fields.json:490 | 묻기 |
| `seal.staff.본인확인` | 본인확인 | seal | 1쪽 [725, 40, 792, 81] | 늘 | - | - | - | 묻기 |
| `sign.staff.본인확인` | 본인확인 | signature | 1쪽 [725, 40, 792, 81] | 늘 | - | - | - | 묻기 |
| `seal.staff.담당` | 담당 | seal | 1쪽 [796, 43, 844, 77] | 늘 | - | - | - | 묻기 |
| `sign.staff.담당` | 담당 | signature | 1쪽 [792, 40, 848, 81] | 늘 | - | - | - | 묻기 |
| `seal.staff.책임자` | 책임자 | seal | 1쪽 [862, 45, 907, 76] | 늘 | - | - | - | 묻기 |
| `sign.staff.책임자` | 책임자 | signature | 1쪽 [848, 40, 921, 81] | 늘 | - | - | - | 묻기 |
| `check.위고유식별정보수집이용에동의하십니까` | 위고유식별정보수집·이용에동의하십니까? | checkbox (동의하지 않음 / 동의함) | 2쪽 [848, 494, 912, 508] | 늘 | 파일 key | 보기 중 고름: 동의하지 않음 / 동의함 | fields.json:605 | 묻기 |
| `check.위개인정보수집이용에동의하십니까` | 위개인(신용)정보수집·이용에동의하십니까? | checkbox (동의하지 않음 / 동의함) | 2쪽 [721, 634, 910, 648] | 늘 | 파일 key | 보기 중 고름: 동의하지 않음 / 동의함 | fields.json:651 | 묻기 |
| `seal.signer` | 본인성명 | seal | 2쪽 [877, 725, 916, 739] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:723 | 묻기 |
| `sign.signer` | 본인성명 | signature | 2쪽 [877, 725, 916, 739] | 늘 | 서명 자리 | 도장·서명 (표시 확률 marks.json) | fields.json:723 | 묻기 |

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
"본인계좌 일괄지급정지 조회신청서"
```

## 이 서식만의 질문 `qa.py` (과제 form_qa)

없습니다. 더하려면 이 폴더에 `qa.py` 를 만들고 함수 하나에 질문 하나 (견본: `python -m docgen.formdir qa hf018 --new`):

```python
def 직위(v):                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 위 표의 키)
    return "직위만 답하세요.", v["employer.position"]   # (질문, 정답) → 평가 세트·학습 데이터에 들어감
```

## 고치려면

칸 하나에 관한 것(박스·키·값·질문)은 `fields.json` 의 그 칸, 질문 문장·답 꼴·전용 질문은 `questions.json`.
고친 뒤 `python -m docgen.formdir check hf018` → `python -m docgen.formdir card hf018` (실제 질문→답 확인).

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
| 이 서식만의 질문 | 이 폴더 `qa.py` 에 함수 하나 = 질문 하나 (견본 `python -m docgen.formdir qa hf018 --new`) | 필요 없음 |
| 분류 정답 | `questions.json`: `{"classify": {"answer": "…", "aliases": […]}}` | 필요 없음 |
| 표를 가리키는 제목 (표 과제 질문) | `questions.json`: `{"table": {"<묶음>": {"title": "…"}}}` (묶음 = 키의 행 번호 앞, `rows.0.x` → `rows`) | 필요 없음 |
| 개수가 정해진 격자를 표가 아니라 kie 로 | `questions.json`: `{"table": {"<묶음>": {"ask": false}}}` | 필요 없음 |
| 모든 서식에 같은 것 (기본 문장·바탕 틀) | `docgen/forms/_common/` ([README](../_common/README.md)) | 바탕 틀이면 다시 |

"다시" = 그림이 바뀌어 재검수 필요로 바뀝니다. 질문 설정(`q`)·`questions.json`·`qa.py` 는 그림을 바꾸지 않아 검수 상태가 그대로입니다.
확인: studio ① 서식 › 카드·문항 Q/A · `python -m docgen.formdir questions hf018 --show` · `python -m docgen.preview hf018 --out work/hf018`
