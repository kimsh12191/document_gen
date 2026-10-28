# 질문·답 관리 (서식 폴더의 questions.json)

합성 데이터의 **질문과 정답이 어떻게 만들어지는지**, 서식마다 어떻게 바꾸는지 정리한 문서입니다.
서식 관리 전체는 [forms.md](forms.md), 모델에게 어떻게 물으면 되는지(질문 문장 전문)는 [questions.md](questions.md)에 있습니다.

## 1. 한눈에

```
기본 (모든 서식)  docgen/forms/_common/questions.json   질문 문장 · 항목 줄 꼴 · 답 꼴 (과제마다)
                 칸의 항목명                             (템플릿 label= / 원본 서식 칸)
                 키 사전 docgen/forms/_common/dictionary  공통 키 · 괄호 설명 · 문서명(분류 정답)
     ⊕
서식에서 바꾼 것  docgen/forms/<ID>/questions.json       다르게 할 것만 (없으면 모두 기본)
     │
     ▼  문서를 그릴 때마다 (고객·seed 마다 값이 다름)
질문 = prompt 의 {items} 자리에 칸마다 line 꼴로 쓴 항목 줄
정답 = 같은 칸들의 그린 값·위치를 answer 꼴로        ──→  tasks/<과제>.jsonl
```

- **정답 값은 파일에 적지 않습니다.** 문서를 그릴 때 칸에 넣은 값과 그 위치가 그대로 정답입니다. 값이 이상하면 값 출처(`fields.json`·`generate.py`)를 고칩니다.
- **합친 전체**(실제로 쓰이는 것)는 서식 카드 `FORM.md` 의 "질문 → 답", `python -m docgen.formdir questions <ID> --show`, studio 문항 Q/A 탭에서 봅니다.
- 지금 545종 모두 바꾼 것이 없어 `questions.json` 이 없습니다 (모두 기본).

## 2. 모양 (재직증명서, 모두 기본일 때)

```
질문 (모델에게 가는 글 전부)
  이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. … 로 답하세요.      ← kie.prompt (공통)
  항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
  - doc_no: 문서번호                                                                    ← {items}: 칸마다 line 꼴 "- {key}: {label}{note}"
  - customer.name: 성명 (고객 성명)                                                     ← label = 칸의 항목명, note = 키 사전의 설명

정답 (answer: list_box)
  [{"key": "doc_no", "value": "제250459호", "bbox_2d": [151, 65, 223, 76], "page": 1},  ← 그 칸에 그려진 값·위치
   {"key": "customer.name", "value": "남궁예태", "bbox_2d": [295, 151, 362, 164], "page": 1}, …]
```

이 서식 폴더에 `questions.json` 을 이렇게 두면:

```json
{"kie": {"items": [{"key": "customer.rrn", "ask": false},
                   {"key": "purpose", "label": "발급 용도"}]},
 "extra": [{"id": "duty", "prompt": "담당업무는 무엇입니까? 적힌 그대로 답하세요.", "type": "text", "answer": "{employment.duty}"}]}
```

| 바꾼 것 | 질문 | 정답 |
|---|---|---|
| `customer.rrn` 에 `"ask": false` | 그 줄이 빠짐 | 그 항목이 빠짐 |
| `purpose` 에 `"label": "발급 용도"` | `- purpose: 발급 용도` | 그대로 |
| `extra` 에 duty | 새 문항 (과제 form_qa): "담당업무는 무엇입니까? …" | `"고객 상담 및 CS 관리"` |

## 3. `questions.json` — 바꿀 것만

```json
{
 "kie": {
   "prompt": "이 증명서에서 아래 항목 값을 JSON 객체 {키: 값} 하나로 답하세요.\n{items}",
   "line": "* {label} → {key}",
   "answer": "object",
   "others": "skip",
   "items": [
     {"key": "customer.rrn", "ask": false},
     {"key": "purpose", "label": "발급 용도"},
     {"key": "debts.*.balance", "note": "1행부터 잔액"}
   ]
 },
 "marks": {"answer": "list", "prompt": "…\n{items}"},
 "ocr_field": {"exclude": ["customer.rrn"]},
 "ocr_page": {"exclude": []},
 "classify": {"answer": "재직증명서", "aliases": ["재직 증명서"]},
 "extra": [
   {"id": "amount", "prompt": "대출 신청금액은 얼마입니까? 원 단위 숫자로만 답하세요.", "type": "number", "answer": "{loan.amount}"},
   {"id": "has_guarantor", "prompt": "보증인 성명이 적혀 있습니까? 예/아니오로 답하세요.", "type": "yesno", "when": "guarantor.name"},
   {"id": "branch", "prompt": "취급 은행과 지점을 '은행 지점' 꼴로 답하세요.", "type": "text", "answer": "{bank} {branch}"}
 ]
}
```

**질문·답 껍데기** (적지 않으면 공통 `docgen/forms/_common/questions.json`)

| 칸 | 뜻 |
|---|---|
| `prompt` | 질문 전문. kie·marks 는 `{items}` 자리에 항목 줄이 들어갑니다 (꼭 있어야 함). 줄바꿈은 `\n` |
| `line` | (kie·marks) 항목 한 줄 꼴. `{key}` 키, `{label}` 항목명(없으면 `-`), `{note}` 괄호 설명(` (고객 성명)` 또는 빈칸) |
| `answer` | 답 꼴 — 아래 표 |

| 과제 | `answer` | 정답 꼴 | 주 지표 |
|---|---|---|---|
| kie | `list_box` (기본) | `[{"key", "value", "bbox_2d", "page"}]`, 빈 칸 `{"key", "value": null}` | 값+위치 vl_f1 |
| kie | `list` | `[{"key", "value"}]` | 값 f1 (위치 점수 뺌) |
| kie | `object` | `{"키": 값, …}` | 값 f1 |
| marks | `list_box` (기본) / `list` | 체크된 보기·도장 유무 (+ 위치) | vl_f1 / acc |
| classify | (`answer`·`aliases` 칸) | 문서명 (다른 이름도 정답) | acc |
| ocr_field·ocr_page | (고정) | 칸 글자 / 값 줄 목록 | exact / recall |

답 꼴을 바꾸면 질문 문장도 그 꼴로 고칩니다 (`list`·`object` 면 위치 이야기를 빼고 꼴을 설명). `--check` 가 안 맞으면 알려 줍니다.

**묻는 칸 `items`** (kie·marks) — 바꿀 칸만 한 줄씩

| 칸 | 뜻 |
|---|---|
| `key` | 질문·정답의 키 (카드의 키 열). 반복 행 번호는 `*` (`debts.*.balance` → `debts.0.balance`, `debts.1.balance` …) |
| `label` | 질문의 항목명 (없으면 칸의 항목명) |
| `note` | 괄호 설명 (없으면 키 사전에서 자동: 누구의 무엇·몇 행·같은 항목명 중 몇 번째 칸) |
| `ask: false` | 이 칸은 묻지 않음 (정답에서도 빠짐) |
| `others: "skip"` | (과제 칸) `items` 에 적은 칸만 묻기. 기본 `ask` 는 적지 않은 칸도 기본대로 묻기 |

- 묻는 차례는 문서 순서입니다. 그 문서에 그려진 칸만 묻고(조건부 칸은 문서마다 다름), 40개(`max_keys`)를 넘으면 골라 묻습니다.
- `ocr_field`·`ocr_page` 의 `exclude`: 값 칸 읽기에서 고르지 않을 칸, 받아쓰기 정답에서 뺄 칸.

**`extra` (서식 전용 질문 → 과제 `form_qa`)** — 질문·답 모두 서식에서

| `type` | 정답 | 채점 |
|---|---|---|
| `number` | `answer` 의 `{키}` 를 칸 값으로 채워 숫자로 (`"{loan.amount}"` → 35000000) | 숫자가 같은지 (`tol` 허용 오차, 기본 0) |
| `yesno` | `when` 칸에 값이 있으면 `예`, 비었거나 없으면 `아니오` | 예/아니오 |
| `text` | `answer` 의 `{키}` 를 칸 값으로 채운 글 (`"{bank} {branch}"` → "국민은행 센텀지점") | 띄어쓰기·문장부호를 맞춰 같은지 |

- `{키}` 는 질문 키(공통 키)나 서식의 원래 키 둘 다 됩니다. 칸이 비었거나 없는 문서에서는 그 질문을 만들지 않습니다 (`number`·`text`).
- 답 꼴(숫자만, 예/아니오로)을 질문 문장에 꼭 적으세요. 보고서에는 **서식 전용 질문(form_qa)** 줄로 따로 나옵니다.

**문장을 서식마다 바꿀 때 주의:** 모델은 공통 문장으로 학습했습니다. 서식마다 문장·답 꼴이 다르면 그 서식에서 점수가 흔들릴 수 있습니다
(학습 데이터도 같은 파일로 만들어져 학습과 평가는 서로 맞습니다). 서식 사이 점수를 비교할 때는 `--check`·카드로 문장이 같은지 먼저 봅니다.

## 4. 고치려면 어디를

| 바꾸고 싶은 것 | 고칠 곳 |
|---|---|
| 이 서식의 질문 문장·답 꼴·묻는 칸·항목명·뺄 칸·분류 정답·전용 질문 | 서식 폴더 `questions.json` |
| 정답 값이 이상함 (값 자체·칸끼리 관계) | `fields.json` 값 출처, `generate.py` — [forms.md 4절](forms.md#4-고치려면-서식-하나) |
| 칸 위치 (정답 bbox) | 템플릿 / studio 영역 편집 |
| 모든 서식의 기본 문장·항목 줄 꼴·답 꼴 | `docgen/forms/_common/questions.json` + [questions.md](questions.md) (테스트가 둘을 맞춰 봄). 평가 세트 `VERSION` 을 올림 |
| 괄호 설명·공통 키·문서명 | 키 사전 `docgen/forms/_common/dictionary/` (studio 키 사전 화면) |
| 그린 문서에서 정답을 꺼내는 법·새 답 꼴 (엔진) | `docgen/bench/tasks/<과제>.py` 의 `make(doc)` + 채점 `docgen/bench/evaluate.py` |
| 업무 묶음 과제 (구비·대조·심사) | `docgen/bench/build.py`·`cases.py`·`rules.py` ([benchmark.md](benchmark.md)) |

- `questions.json` 은 그림을 바꾸지 않아 **서식 해시에 들어가지 않습니다** (고쳐도 재검수 필요로 바뀌지 않음). 데이터셋 기록 `dataset.json` 의 `question_hashes` 에 남습니다.
- 고친 뒤 카드를 다시 만듭니다 (`python -m docgen.formdir card <ID>`).

## 5. 명령

```bash
python -m docgen.formdir questions <ID> --show                 # 합친 전체 (기본 / 이 서식에서 바꿈 표시)
python -m docgen.formdir questions <ID> --check                # 칸과 맞는지
python -m docgen.formdir questions --all --slim [--write]      # 기본과 같은 줄을 파일에서 지움 (예전 꼴의 전체 사본 정리)
```

`--check` 가 알려 주는 것:

| | 뜻 | 할 일 |
|---|---|---|
| 문제: 지금 칸에 없는 키 | 칸 키를 바꿨거나 지웠는데 `items` 는 그대로 | 줄의 `key` 를 고치거나 지움 |
| 문제: extra·exclude 의 칸에 없는 키 | 오타 | 고침 |
| 문제: 답 꼴과 질문이 안 맞음 | `list_box` 인데 질문에 위치(`bbox_2d`) 요청이 없음, 또는 반대 | `prompt` 나 `answer` 를 맞춤 |
| 참고: 질문 문장이 공통 문장과 다름 | 이 서식만 문장이 다름 | 일부러가 아니면 `prompt` 를 지움 |
| 참고: 칸의 항목명과 다르게 묻는 칸 | `label` 로 바꾼 칸 | 확인 |
| 참고: 기본과 같은 줄 | 지워도 같은 줄 | `--slim --write` |

studio **서식 다시 읽기**는 모든 서식의 `questions.json` 형식(JSON, `{items}` 자리, 답 꼴 이름, extra 의 type 등)을 검사해 문제로 보여 줍니다.

## 6. 새 과제 추가 (엔진)

서식 한 건에서 만드는 새 과제는 `docgen/bench/tasks/` 에 파일 하나를 더합니다. `kie.py` 를 견본으로:

1. `TASK`·`NAME`·`PROMPT`·`ANSWER`·`EXAMPLE`·`NOTES` 와 `make(doc)` (→ 문항 목록). `doc.fields` 칸, `doc.q` 서식의 questions.json, `doc.where()` 위치.
2. `tasks/__init__.py` 의 `SINGLE` **끝에** 붙입니다 (과제들이 난수를 이어 쓰므로 중간에 넣으면 다른 과제 문항이 바뀜).
3. 채점 `evaluate.py` (`SCORERS`·`MAIN`·`TASK_ORDER`·`TASK_TITLE`·`TASK_GROUP`), 구분 `tracking.py`, 보고서 `train/report.py`, 화면 이름 `studio/static/js/datasets.js`.
4. 기본 문장은 `docgen/forms/_common/questions.json` 에, 서식마다 다르게 할 것이 있으면 `docgen/formquestions.py` 에 칸을 더합니다.
5. `build.py` 의 `VERSION` 을 올립니다.
