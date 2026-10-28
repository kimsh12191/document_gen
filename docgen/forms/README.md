# 서식 폴더 설명서

서식 하나 = 폴더 하나 (`docgen/forms/<ID>/`). 이 문서 하나에 서식 폴더의 파일마다 무엇이고, 무엇을 고치면 만들어지는 데이터가
어떻게 바뀌는지를 모았습니다. 사람이든 코드를 읽는 LLM 이든 **그 서식의 카드 `FORM.md` 와 이 문서**만 읽으면 서식을 고칠 수 있습니다.

> LLM 에게 맡길 때: "`docgen/forms/<ID>/FORM.md` 와 `docgen/forms/README.md` 를 읽고 …를 고쳐. 고친 뒤
> `python -m docgen.formdir check <ID>` 와 `python -m docgen.formdir card <ID>`."

## 1. 무엇을 하는 곳인가

이 저장소의 `docgen` 은 **서식별 합성 데이터 생성기**입니다. 서식(은행·관공서 서류) 하나에 가짜 고객의 값을 채워 그림을 그리고,
그 그림을 보고 답할 **질문 + 정답**을 만듭니다. 같은 코드가 평가 세트와 학습 데이터를 만들고, 채점도 합니다.

```
서식 폴더 (이 문서)          생성 (studio ⑥ 데이터셋 / python -m docgen.bench build)       학습·평가 (train/)
  모양·칸·값·질문   ──────►   서식 × 고객마다: 그리기 → 칸(키·값·위치) → 과제별 질문·정답  ──────►  SFT·GRPO, 채점·비교표
```

정답은 사람이 적지 않습니다. **그릴 때 넣은 값과 잰 위치가 곧 정답**입니다. 그래서 파일에는 "값을 어디서 채우나"만 있고, 정답 값은 없습니다.

## 2. 폴더 구성

```
docgen/forms/<ID>/
  FORM.md            카드 (자동 생성 — 읽는 곳): 뽑는 칸·위치·값 출처·정한 곳(파일:줄)·질문→답 실제 예시·고치는 곳
  look/template.html.j2   모양과 칸 자리 {{ f("키", label="항목명") }}       (원본 서식: look/original.pdf + layout.json)
  fields.json        칸 목록 — 칸 하나 = 한 줄: 키·항목명·값 출처(source)·박스(원본 서식 rect)·질문 설정(q)
  generate.py        값 만들기 — 코드 서식: @doc 함수가 값 전부 / html 서식: adjust(d, p, rng) 로 칸끼리 관계 (없어도 됨)
  questions.json     기본 과제의 질문 문장·답 모양을 이 서식만 다르게 (없으면 기본) — 5.2절
  qa.py              이 서식만의 질문과 정답 (없으면 없음) — 5.3절
  form.json, variants/, source.png …   이름·그룹, 레이아웃 변형, 원본 그림

docgen/forms/_common/      모든 서식이 같이 쓰는 것 (README.md): 기본 질문(questions.json), 키 사전(dictionary/),
                           바탕 틀(templates/), 키 규칙(key_rules.json), 체크·도장 확률(marks.json), 값 출처 목록(values.md)
```

폴더 밖에서 서식이 쓰는 코드는 둘뿐입니다: `docgen/docs/<그룹>.py`(같은 그룹 코드 서식의 도우미), `docgen/docs/_common.py`(날짜·금액 표기 도우미).
그 밖(그리기·채점·업무 묶음)은 엔진이라 서식 작업에서 보지 않습니다 ([_common/README](_common/README.md)).

## 3. 서식 종류

폴더 꼴은 같고 모양·값을 만드는 곳만 다릅니다. 카드 첫 줄에 종류가 있습니다.

| 종류 | 모양 | 값 | 칸 더하기·고치기 |
|---|---|---|---|
| 코드 서식 (70) | `look/template.html.j2` | `generate.py` 의 @doc 함수 | 템플릿 + `generate.py` |
| html 서식 (69, 공식 대조·복제·새로 추가) | `look/template.html.j2` | `fields.json` 의 `source` (+ `generate.py` 의 adjust) | 템플릿 + `fields.json` |
| 원본 서식 (406, 하나은행 `hf###`·`hana_*`, 가져온 그림 `img_*`) | 원본 PDF·그림 | 칸 자리의 항목명 → 값 종류 (키 규칙) | studio 영역 편집 (`fields.json` items) |

## 4. 데이터가 만들어지는 길

studio ⑥ 데이터셋 › 만들기와 명령줄 `python -m docgen.bench build` 는 같은 코드입니다. 서식 하나·고객 하나(seed)마다:

```
① 고객   make_profile(seed): 한 사람의 이름·주민번호·주소·직장·소득·계좌 (서로 맞음)
② 값     코드 서식: generate.py / html 서식: fields.json 의 source → generate.py 의 adjust / 원본 서식: 항목명 → 값 종류
③ 그림   템플릿에 값을 넣어 그리고, 칸마다 위치(쪽·박스)를 잰다 → 촬영 조건(스캔·사진·팩스)으로 흔든다
④ 칸     {키, 항목명, 타입, 값, 위치}. 키 사전으로 공통 키로 (employee.name → customer.name)
⑤ 문항   과제마다 질문·정답 (docgen/bench/tasks/<과제>.py) — 아래 표
⑥ 묶음   한 고객의 서류 여러 장 → 구비 확인·대조·심사 (서식 하나를 넘는 업무 과제, docgen/bench/build.py)
```

| 과제 | 묻는 것 | 질문·답 모양을 정하는 곳 |
|---|---|---|
| `classify` | 무슨 서류인가 | 문장: `questions.json` / 정답(문서명): 키 사전 또는 `questions.json` 의 `classify` |
| `ocr_page` · `ocr_field` | 전체 받아쓰기 · 값 칸 하나 읽기 | 문장: `questions.json`. 뺄 칸: `fields.json` 칸의 `q.ocr` |
| `kie` | 칸마다 값과 위치 | 문장·항목 줄·답 틀: `questions.json` / 묻는 칸·항목명: `fields.json` 칸의 `q` |
| `marks` | 체크박스·도장·서명 | kie 와 같음 |
| `freetext` | 기타·비고 칸의 자유 기재 정리 | `_common/freetext_templates.json` |
| `form_qa` | **이 서식만의 질문** | `qa.py` |

결과 폴더: `images/`, `tasks/<과제>.jsonl`(한 줄 = 그림·질문·정답·채점 정보), 학습용이면 `swift/all.jsonl`.
과제가 만드는 문항은 모두 평가 세트와 학습 데이터에 같이 들어갑니다 (어느 쪽인지는 데이터셋을 만들 때 `split` 으로).

## 5. 질문과 답 고치기

### 5.1 칸마다: `fields.json` 의 그 칸 `"q"`

```json
// 원본 서식: items 의 한 칸
{"t": "text", "page": 0, "label": "주민등록번호", "rect": [352.9, 178.8, 549.6, 195.8], "q": {"ask": false}}
// html·코드 서식: fields 의 한 칸 (반복 표는 lists.<이름>.fields.<칸>)
"purpose": {"label": "용도", "type": "text", "source": "code", "q": {"label": "발급 용도", "note": "제출 목적"}}
```

| `q` 안 | 뜻 |
|---|---|
| `ask: false` | kie·marks 질문과 정답에서 뺌 |
| `label` | 질문의 항목명 (없으면 칸의 항목명) |
| `note` | 괄호 설명 (없으면 키 사전에서 자동: 누구의 무엇·몇 행) |
| `ocr: false` | 값 칸 읽기(ocr_field)에서 고르지 않고, 받아쓰기(ocr_page) 정답에서 뺌 |

- html·코드 서식에서 `fields.json` 에 줄이 없는 칸(부모 서식 값, 체크·도장·서명)은 맨 위 `"q"` 묶음에 키로: `"q": {"seal.company": {"label": "회사 직인"}}`.
- 반복 표 칸의 `q` 는 그 열 전체에 적용됩니다.

### 5.2 기본 과제의 질문 문장·답 모양: `questions.json`

기본은 `_common/questions.json` 입니다. 서식 폴더의 `questions.json` 에는 **다르게 할 것만** 적습니다. kie 의 기본:

```json
"kie": {
  "prompt": "이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. …\n{items}",
  "item":   "- {key}: {label}{note}",
  "answer": {"key": "{key}", "value": "{value}", "bbox_2d": "{bbox_2d}", "page": "{page}"},
  "answer_empty": {"key": "{key}", "value": null}
}
```

- **질문** = `prompt` 의 `{items}` 자리에 물을 칸마다 `item` 한 줄.
- **답** = 물은 칸마다 `answer` 하나를 채운 것. 값이 비었으면 `answer_empty`.

`answer` 는 보이는 그대로 적습니다. 두 가지 꼴이 있습니다.

| 꼴 | 적는 법 | 나오는 답 | 채점 |
|---|---|---|---|
| JSON | `{"항목": "{key}", "값": "{value}"}` — 칸 이름은 마음대로, 자리 `"{key}"`·`"{value}"`·`"{bbox_2d}"`·`"{page}"` | `[{"항목": "customer.name", "값": "남궁예태"}, …]` | 칸 이름을 거꾸로 읽어 기본과 같게. `{bbox_2d}` 가 없으면 위치 점수 없이 값 f1 |
| 줄글 | `"{label}: {value}"` — 자리 `{label}`·`{key}`·`{value}` | 칸마다 한 줄: `성명: 남궁예태` ⏎ `회사명: 주식회사 다온패션` | 틀로 줄에서 값을 찾아 값 f1 (위치 없음). 빈 칸 틀이 없으면 `{value}` 자리에 "없음" |

예: 재직증명서의 kie 를 줄글로

```json
{"kie": {"prompt": "이 재직증명서에 적힌 아래 항목을 한 줄에 하나씩 '항목명: 값' 으로 답하세요. 없으면 '없음'.\n{items}",
         "answer": "{label}: {value}"}}
```

| 칸 | 뜻 |
|---|---|
| `prompt` | 질문 전문 (kie·marks·classify·ocr_field·ocr_page). kie·marks 는 `{items}` 가 꼭 있어야 함. 줄바꿈은 `\n` |
| `item` | (kie·marks) 질문 항목 한 줄. `{key}`, `{label}`(없으면 `-`), `{note}`(` (설명)` 또는 빈칸) |
| `answer`, `answer_empty` | (kie·marks) 답 항목 하나의 틀 (위 표) |
| `classify` | 분류 정답 `answer`, 정답으로 인정할 다른 이름 `aliases` |

- 답 모양을 바꾸면 **질문 문장도 그 꼴로** 고칩니다 (JSON 틀의 칸 이름을 질문에 적기, 위치를 빼면 위치 이야기도 빼기). `check` 가 안 맞으면 알려 줍니다.
- 모델은 공통 문장으로 학습했으므로, 서식마다 문장을 바꾸면 그 서식 점수가 흔들릴 수 있습니다 (학습 데이터도 같은 파일로 만들어지므로 새로 학습하면 맞춰짐).

### 5.3 이 서식만의 질문: `qa.py`

기본 과제와 따로, 이 서식에서만 묻고 싶은 질문을 **함수 하나 = 질문 하나**로 적습니다. 정답은 그린 문서의 칸 값으로 함수가 만듭니다.

```python
# docgen/forms/employment_certificate/qa.py
from docgen.formqa import date, months, number   # 도우미: 금액 글자 → 숫자, 날짜 글자 → 날짜, 두 날짜 사이 개월 수


def 직위(v):                                       # v = 이 문서에 그린 칸 값 {키: 값} (키는 카드의 키 열)
    return "직위만 답하세요.", v["employer.position"]


def 회사와_성명(v):                                 # JSON 정답
    return '회사명과 성명을 {"회사": …, "성명": …} 로 답하세요.', {"회사": v["employer.name"], "성명": v["customer.name"]}


def 전화번호_있음(v):                               # True/False → 예/아니오
    return "회사 전화번호가 적혀 있습니까? 예/아니오로 답하세요.", v.get("employer.phone") is not None


def 재직개월(v):                                    # 계산: 재직기간 "2021.03.06 ~ 현재" 의 입사일부터 발급일까지
    start = v["employer.period"].split("~")[0]
    return "발급일 기준 재직 기간은 몇 개월입니까? 숫자로만 답하세요.", months(start, v["issue_date"])
```

- **돌려주기:** `(질문, 정답)`. `None` 이면 그 문서에서는 묻지 않습니다. `_` 로 시작하는 함수는 질문이 아니라 도우미입니다.
- **v:** 질문 키(공통 키)와 서식의 원래 키 둘 다로 읽힙니다. 체크박스는 체크된 보기 글자(복수 선택은 목록), 도장·서명은 True/False.
  **빈 칸은 v 에 없습니다** — `v["키"]` 로 읽으면 그 칸이 빈 문서에서는 그 질문을 묻지 않고, 있는지 물으려면 `v.get("키")`.
- **데이터:** 만들 때 자동으로 과제 `form_qa` 문항이 되어 평가 세트·학습 데이터에 들어갑니다. 문항의 `meta.question` = `"<서식ID>.<함수 이름>"`.
- **기본 채점 (정답 꼴로):** 숫자 → 숫자가 같은지 · 예/아니오 → 그대로 · 글 → 띄어쓰기·문장부호 무시하고 같은지 · JSON → 칸마다 같은지. 주 지표 acc.
- **견본:** `python -m docgen.formdir qa <ID> --new` (이 서식의 칸 키로 쓴 예시가 주석으로). 확인: `python -m docgen.formdir qa <ID>`.
- 실행되는 파이썬 코드입니다 (`generate.py` 와 같음). 읽고 확인한 파일만 넣습니다.

### 5.4 채점을 다르게: `train/scorers`

채점은 서식 폴더가 아니라 **`train/scorers` 의 채점 함수 한 곳**에서 정합니다. 평가 세트(또는 학습 데이터)에 붙이면 평가 점수와 GRPO 보상이 그 함수로 계산됩니다.

```json
{"id": "syn", "paths": ["<데이터셋>"], "scorer": "../scorers/my_form_qa.py:score"}
```

- `qa.py` 질문 몇 개만 다르게: 견본 [`train/scorers/form_qa_example.py`](../../train/scorers/form_qa_example.py) (`meta.question` 으로 가르고 나머지는 기본 채점).
- 과제 전체를 다르게: [`train/scorers/bank_default.py`](../../train/scorers/bank_default.py) (과제마다 함수 하나). 규칙은 [guide/eval.md](../../guide/eval.md).

## 6. 칸·모양·값 고치기

| 하고 싶은 것 | 코드 서식 | html 서식 | 원본 서식 | 재검수 |
|---|---|---|---|---|
| 칸(추출 항목) 더하기 | 템플릿에 `{{ f("키", label="항목명") }}` + `generate.py` 가 그 키 값 | 템플릿에 `f(…)` + `fields.json` `fields` 에 키·source | studio 영역 편집에서 칸 그리기 | 다시 |
| 칸 키·항목명 | 템플릿의 `f("키", label=…)` | 템플릿 + `fields.json` | 영역 편집 (`fields.json` 그 칸 `key`·`label`) | 다시 |
| 값 | `generate.py` | `fields.json` 의 `source` ([값 출처 목록](_common/values.md)) | 값 출처·값 종류 (`source`·`kind`) | 다시 |
| 칸끼리 관계 (합계·날짜 순서) | `generate.py` | `generate.py` 의 `adjust(d, p, rng)` | — | 다시 |
| 모양·표·문구 | 템플릿 (studio html 편집) | 같음 | 바꾸지 않음 | 다시 |
| 답의 위치 (박스) | 템플릿 배치 | 같음 | `fields.json` 그 칸 `rect` | 다시 |
| 질문 설정·질문 문장·답 모양·전용 질문 | 5절 | 5절 | 5절 | 필요 없음 |

- **그림을 바꾸는 것**을 고치면 그 서식이 "재검수 필요"로 바뀝니다. 질문(`q`·`questions.json`·`qa.py`)은 그림을 바꾸지 않아 검수 상태가 그대로입니다.
- 새 서식을 처음부터 만드는 절차는 [guide/new-forms.md](../../guide/new-forms.md), 결과물 형식은 [NEW_FORM_SPEC.md](../manual/NEW_FORM_SPEC.md).

## 7. 고친 뒤

```bash
python -m docgen.formdir check <ID>        # 이것 하나: 칸 목록·박스·값 출처·q·questions.json·qa.py·카드가 오래됐는지
python -m docgen.formdir card <ID>         # 카드 FORM.md 다시 만들기 (실제 질문→답이 바뀐 것을 확인)
python -m pytest docgen/tests              # 코드를 고쳤으면. 오래된 카드도 잡는다
```

`check` 가 알려 주는 것 (문제 = 고쳐야 함, 참고 = 알아 둘 것):

| | 뜻 |
|---|---|
| 문제: `q` 에 모르는 칸 | `q` 는 `ask`·`label`·`note`·`ocr` 만 |
| 문제: source … · 박스가 쪽 밖 | 값 출처([목록](_common/values.md))·`rect` |
| 문제: 답 틀 형식 · 칸 이름이 질문 문장에 없음 | 5.2절 |
| 문제: qa.py 함수 오류 · 한 번도 묻지 않음(없는 키) · 정답을 답으로 넣어도 만점이 아님 | 5.3절 |
| 문제: `extra`·`line`·`others`·`items` (예전 이름) | `extra` → `qa.py`, `line` → `item`, `others`·`items` → 칸의 `q` |
| 참고: 묻지 않는 칸·항목명을 바꾼 칸·문장이 공통과 다름·일부 문서에서만 묻는 질문 | 일부러 바꾼 것인지 확인 |

검사 통과는 형식 확인일 뿐 **검수가 아닙니다.** 그림과 정답이 맞는지는 studio ① 서식 › 검수에서 사람이 봅니다.

## 8. 모든 서식에 같은 것

`docgen/forms/_common/` — 무엇이 어디에 영향을 주는지는 [_common/README](_common/README.md).
기본 질문 문장(`_common/questions.json`)을 바꾸면 모든 서식의 문항이 바뀌므로 평가 세트 버전(`docgen/bench/build.py` 의 `VERSION`)을 올리고
[guide/questions.md](../../guide/questions.md) 도 같이 고칩니다. 공통을 고친 뒤에는 카드를 모두 다시 만듭니다 (`card --all --stale --workers 4`).

새 과제(모든 서식에 같은 새 질문 종류)는 엔진 일입니다: `docgen/bench/tasks/` 에 파일 하나 (`kie.py` 견본), `tasks/__init__.py` 의 `SINGLE` **끝에**
붙이고, 채점 `docgen/bench/evaluate.py`, `build.py` 의 `VERSION` 을 올립니다.

## 9. 명령

```bash
python -m docgen.formdir path <ID>                         # 이 서식의 파일들
python -m docgen.formdir check <ID> | --all                # 서식 검사
python -m docgen.formdir card <ID> | --all --stale --workers 4   # 카드 FORM.md
python -m docgen.formdir questions <ID> --show             # 질문·답 전체 (기본 + 이 서식에서 바꾼 것 + qa.py)
python -m docgen.formdir qa <ID> [--new]                   # 이 서식만의 질문 보기 / 견본 만들기
python -m docgen.formdir values                            # 값 출처 목록 _common/values.md 다시 만들기
python -m docgen.preview <ID> --rows max --out work/<ID>   # 그려 보기
python -m docgen.bench build --types <ID> --per-doc 2 --bundles 0 --out work/qa_<ID>   # 이 서식만 데이터 만들어 보기
```

studio: ① 서식 › 카드 · 미리보기 · 문항 Q/A(질문 파일과 qa.py 도 보임) · 영역 편집 · html 편집 · 검수 · 파일.
[서식 다시 읽기]는 새 폴더 등록과 함께 `questions.json`·`qa.py` 형식 문제, 카드가 없거나 오래된 서식을 알려 줍니다.
