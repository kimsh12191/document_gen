# 서식 관리 (서식 폴더 · 공통 폴더 · 카드)

서식을 **이해하고 고치는 법**을 한곳에 정리한 문서입니다. 서식 하나에 관한 것은 그 서식 폴더에, 모든 서식에 영향을 주는 것은
공통 폴더 하나에 있습니다. 서식 작업은 이 두 곳만 봅니다.

- 새 서식 추가 절차: [new-forms.md](new-forms.md) · 질문·답 고치기 자세히: [qa.md](qa.md) · 결과물 형식: [NEW_FORM_SPEC.md](../docgen/manual/NEW_FORM_SPEC.md)

## 1. 두 폴더

```
docgen/forms/<ID>/               ← 서식 하나 (그 서식만의 것 전부)
  FORM.md                          카드 (자동 생성 — 읽는 곳): 항목·위치·정한 곳·질문→답 예시·고치는 곳
  look/template.html.j2            모양·칸 자리 {{ f("키", label="항목명") }}   (원본 서식: look/original.pdf + layout.json)
  fields.json                      칸 목록 — 칸 하나 = 한 줄: 키·항목명·값 출처·박스(원본 서식 rect)·질문 설정 q
  generate.py                      값 만들기 — 코드 서식: @doc 함수가 값 전부 / html 서식: adjust(d, p, rng) 로 칸끼리 관계
  questions.json                   질문 껍데기 — 문장·답 꼴·전용 질문, 기본과 다르게 할 것만 (없으면 모두 기본)
  form.json, variants/, source.png …

docgen/forms/_common/            ← 모든 서식 (README.md)
  questions.json                   기본 질문 문장·항목 줄 꼴·답 꼴
  dictionary/                      키 사전 (공통 키, 괄호 설명, 문서명 = 분류 정답)
  templates/                       바탕 틀 (_base·_macros·_real_form·_official_*) + 그룹 부품
  key_rules.json, keys.json        항목명 → 키 규칙·값 종류, 키 목록
  marks.json, freetext_templates.json   체크·도장·서명 표시, 기타 칸 문장 틀
  values.md                        값 출처 목록 (자동)
```

폴더 밖에서 서식이 쓰는 코드는 둘뿐입니다: `docgen/docs/<그룹>.py`(같은 그룹 **코드 서식**의 도우미)와 `docgen/docs/_common.py`(모든 코드 서식의 도우미).
그 밖(그리기·채점·업무 묶음·데이터셋 설정)은 엔진이라 서식 작업에서 보지 않습니다 ([_common/README](../docgen/forms/_common/README.md#서식-작업에서-안-보는-것-엔진데이터셋-설정)).

## 2. 서식 종류

폴더 꼴은 같고 모양·값을 만드는 곳만 다릅니다. 카드 첫 줄에 종류가 적혀 있습니다.

| 종류 | 수 | 모양 | 값 | 칸 추가·수정 |
|---|---|---|---|---|
| 코드 서식 | 70 | `look/template.html.j2` | `generate.py` 의 @doc 함수 (fields.json 에 적으면 덮어씀) | 템플릿 + generate.py |
| html 서식 (공식 대조·복제·새로 추가) | 69 | `look/template.html.j2` | `fields.json` 의 값 출처 (+ `generate.py` 의 adjust) | 템플릿 + fields.json |
| 원본 서식 (하나은행 `hf###`·`hana_*`) | 406 | 원본 PDF 그림 | 칸 자리의 항목명 → 값 종류 | studio 영역 편집 (fields.json items) |
| 가져온 그림 서식 (`img_*`) | — | 견본 그림 | 같음 | 같음 |

## 3. 생성할 때 일어나는 일

studio ⑥ 데이터셋 › 만들기는 레시피(`docgen/recipes/<이름>.json`)로 명령줄과 같은 `python -m docgen.bench build --recipe …` 를 돌립니다.
서식 하나·고객 하나(seed)마다:

```
① 고객       make_profile(seed) — 한 사람의 이름·주민번호·주소·직장·소득·계좌 (서로 맞음)
② 값         코드 서식: generate.py 의 @doc 함수 / html 서식: fields.json 의 값 출처 → generate.py 의 adjust / 원본 서식: 항목명 → 값 종류
③ html       템플릿에 값을 넣는다. f("키", label=…) 자리마다 "이 키 = 이 값, 이 항목명" 이 기록된다 (원본 서식은 PDF 위에 얹음)
④ 그림       브라우저로 그려 칸마다 위치(쪽·박스)를 잰다 → 촬영 조건(스캔·사진·팩스)으로 흔든다
⑤ 칸         {키, 항목명, 타입, 값, 위치}. 키 사전으로 공통 키로 (employee.name → customer.name)
⑥ 문항       과제마다 (docgen/bench/tasks/<과제>.py): 질문 = 문장(questions.json ⊕ 공통) + 칸마다 한 줄(fields.json 의 q), 정답 = ⑤의 값·위치
⑦ 업무 묶음  한 고객의 서류 여러 장 → 구비 확인·대조·심사 문항 (docgen/bench/build.py)
```

**정답은 사람이 적은 값이 아니라 ②에서 넣은 값과 ④에서 잰 위치입니다.** 그래서 정답 값이 틀리면 ②(값)를, 질문이 이상하면 `questions.json` 을 고칩니다.
결과 폴더: `images/`, `crops/`, `tasks/<과제>.jsonl`(한 줄 = 질문·정답·채점 정보), 학습 데이터는 `swift/all.jsonl`, `dataset.json`(서식 해시·질문 파일 해시).

## 4. 고치려면 (서식 하나)

먼저 그 서식의 **카드 `FORM.md`** 를 엽니다 (studio ① 서식 › **카드** 탭). 칸마다 키·항목명·위치·값 출처·**정한 곳(파일:줄)**·질문 여부가 있고,
실제 질문 전문과 정답, 그 서식 종류에 맞는 "고치려면" 표가 있습니다.

| 하고 싶은 것 | 코드 서식 | html 서식 | 원본 서식 | 그다음 |
|---|---|---|---|---|
| 칸(추출 항목) 더하기 | 템플릿에 `{{ f("키", label="항목명") }}` + generate.py 가 그 키 값을 돌려줌 | 템플릿에 `f(…)` + fields.json `fields` 에 키·source | 영역 편집에서 칸 그리기 | 미리보기 → 재검수 → 카드 |
| 칸 키·항목명 바꾸기 | 템플릿의 `f("키", label=…)` | 템플릿 + fields.json | 영역 편집 | 재검수 → 카드 |
| 값이 이상함 | generate.py | fields.json 의 `source` ([값 출처 목록](../docgen/forms/_common/values.md)) | 영역 편집의 값 출처·값 종류 | 재검수 |
| 칸끼리 안 맞음 (합계·날짜 순서) | generate.py | generate.py 의 `adjust(d, p, rng)` | — | 재검수 |
| 모양·표·문구 | 템플릿 (studio html 편집) | 같음 | 바꾸지 않음 | 재검수 |
| 이 칸을 묻지 않기·질문의 항목명·설명 | `fields.json` 그 칸 `"q"` (줄이 없으면 맨 위 `"q"` 묶음) | 같음 | `fields.json` 그 칸 `"q"` | 검수 필요 없음 ([qa.md](qa.md)) |
| 질문 문장·답 꼴·서식 전용 질문·분류 정답 | `questions.json` | 같음 | 같음 | 검수 필요 없음 |
| 답의 박스 | 템플릿 배치 | 같음 | `fields.json` 그 칸 `rect` | 재검수 |

- **그림을 바꾸는 것**(템플릿·generate.py·fields.json 의 키·값·박스)을 고치면 그 서식이 "재검수 필요"로 바뀝니다. 질문 설정(`fields.json` 의 `q`)·`questions.json` 은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
- 고친 뒤 카드를 다시 만듭니다: studio 카드 탭 [카드 다시 만들기] 또는 `python -m docgen.formdir card <ID>`. 테스트(`docgen/tests/test_formcard.py`)가 오래된 카드를 잡습니다.
- LLM 에게 맡길 때: "`docgen/forms/<ID>/FORM.md` 와 `docgen/forms/_common/README.md` 를 읽고 …를 고쳐" — 두 폴더 안에서 끝납니다.

## 5. 고치려면 (모든 서식)

`docgen/forms/_common/` 의 파일. 무엇이 어디에 영향을 주는지는 [_common/README](../docgen/forms/_common/README.md).
기본 질문 문장(`_common/questions.json`)을 바꾸면 모든 서식의 문항이 바뀌므로 평가 세트 버전(`docgen/bench/build.py` 의 `VERSION`)을 올리고
[questions.md](questions.md) 도 같이 고칩니다. 공통을 고친 뒤에는 카드를 모두 다시 만듭니다 (`card --all --stale --workers 4`).

## 6. 명령

```bash
python -m docgen.formdir path <ID>                         # 이 서식의 파일들
python -m docgen.formdir card <ID>                         # 카드 FORM.md 만들기 (그림을 그려 위치를 잰다)
python -m docgen.formdir card --all --stale --workers 4    # 오래된 카드만 다시
python -m docgen.formdir card --all --check                # 오래된 카드 목록 (만들지 않음)
python -m docgen.formdir questions <ID> --show             # 질문·답 전체 (기본 + 이 서식에서 바꾼 것)
python -m docgen.formdir check <ID>                        # 고친 뒤 이것 하나: 칸 목록·박스·값 출처·질문 설정·questions.json·카드
python -m docgen.formdir check --all                       # 모든 서식
python -m docgen.formdir values                            # 값 출처 목록 _common/values.md 다시 만들기
python -m docgen.preview <ID> --rows max --out work/<ID>   # 그려 보기
```

studio: ① 서식 › 카드 · 미리보기 · 문항 Q/A · 영역 편집 · html 편집 · 검수 · 파일. [서식 다시 읽기] 는 새 폴더 등록과 함께
`questions.json` 형식 문제, 카드가 없거나 오래된 서식을 알려 줍니다.

## 7. 예전 구조에서 바뀐 것 (2026-10-28)

| 예전 | 지금 |
|---|---|
| `docgen/templates/` | `docgen/forms/_common/templates/` |
| `docgen/dictionary/` | `docgen/forms/_common/dictionary/` |
| `docgen/keys.json`, `key_rules.json`, `marks.json`, `freetext_templates.json` | `docgen/forms/_common/` |
| 기본 질문 문장 `docgen/bench/prompts.py` 안 | `docgen/forms/_common/questions.json` (prompts.py 는 읽기만) |
| 코드 서식 값 함수 `docgen/docs/<그룹>.py` 안 | 서식 폴더 `generate.py` (그룹 파일에는 같이 쓰는 도우미만) |
| 서식마다 `questions.json` 전체 사본 | 바꾼 것만 (없으면 기본). 칸별 설정(묻기·항목명·설명·OCR 빼기)은 `fields.json` 의 칸 `q` |

옮기기만 한 서식은 서식 해시가 그대로입니다 (`_common/hash_moves.json`) — 검수 기록·데이터셋 기록이 그대로 맞습니다.
같은 설정으로 만든 평가 세트·학습 데이터는 예전과 바이트 단위로 같습니다.
