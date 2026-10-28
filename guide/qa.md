# 질문·답 관리 (서식 폴더의 questions.json)

합성 데이터의 **질문과 정답이 어디서 어떻게 만들어지는지**, 고치려면 어디를 고치는지 정리한 문서입니다.
모델에게 어떻게 물으면 되는지(질문 문장과 답 형식)는 [questions.md](questions.md), 서식 추가는 [new-forms.md](new-forms.md)에 있습니다.

## 1. 한눈에

```
서식 폴더 docgen/forms/<ID>/  (서식마다)
  template.html.j2   모양·칸 자리
  fields.json        칸: 키·항목명·타입·값 출처          ← 정답 값을 정함 (값 출처)
  generate.py        칸끼리 관계 (선택)
  questions.json     질문 껍데기·답 껍데기·묻는 칸      ← 질문·답을 정함
        │
        ▼  문서를 그릴 때마다 (고객·seed 마다 값이 다름)
  그린 칸: 키·항목명·값·위치
        │  docgen/bench/tasks/<과제>.py 가 questions.json 대로 채움
        ▼
  질문 = prompt 의 {items} 자리에 line 꼴로 쓴 항목 줄들
  정답 = 같은 칸들의 값(·위치)을 answer 꼴로        ──→  tasks/<과제>.jsonl
```

- **질문과 답의 껍데기는 서식 폴더에 있습니다.** 질문 전문(`prompt`), 항목 한 줄의 꼴(`line`), 답 꼴(`answer`), 묻는 칸(`items`)을 서식마다 `questions.json` 에서 정합니다.
- **정답 값은 파일에 적지 않습니다.** 문서를 그릴 때 칸에 들어간 값과 위치가 그대로 정답입니다 (같은 서식도 문서마다 고객·값이 다름). 값이 이상하면 `fields.json`(값 출처)·`generate.py` 를 고칩니다.
- **공통으로 남는 것:** 새 서식의 기본 문장(`docgen/bench/prompts.py`), 그린 문서에서 값·위치를 꺼내는 코드(`docgen/bench/tasks/<과제>.py`), 채점(`docgen/bench/evaluate.py`). 답 꼴은 채점이 읽을 수 있는 것 중에서 고릅니다.
- 저장소의 545종은 지금 공통 문장 그대로 채운 파일이 들어 있습니다 (파일이 있어도 문항이 바이트 단위로 같음을 확인). 파일이 없는 서식은 공통 문장으로 묻습니다.

## 2. 파일에서 질문·정답까지 (재직증명서)

`docgen/forms/employment_certificate/questions.json`:

```json
{
 "kie": {
   "prompt": "이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {\"key\": 키, \"value\": 문서에 적힌 값 그대로, \"bbox_2d\": [x1, y1, x2, y2], \"page\": 쪽 번호} 를 쓰세요. … 문서에 비어 있거나 없는 항목은 {\"key\": 키, \"value\": null} 로 답하세요.\n항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))\n{items}",
   "line": "- {key}: {label}{note}",
   "answer": "list_box",
   "others": "ask",
   "items": [
     {"key": "doc_no", "label": "문서번호"},
     {"key": "customer.name", "label": "성명", "from": "employee.name"},
     {"key": "purpose", "label": "용도"}
   ]
 },
 ...
}
```

문서 한 건을 그리면 (seed 마다 값이 다름):

```
질문 (모델에게 가는 글 전부)
  이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. … 로 답하세요.      ← prompt
  항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
  - doc_no: 문서번호                                                                    ← {items}: items 한 줄마다 line 꼴로
  - customer.name: 성명 (고객 성명)                                                     ← {note} = 키 사전의 설명 (또는 items 의 note)
  - purpose: 용도

정답 (answer: list_box)
  [{"key": "doc_no", "value": "제250459호", "bbox_2d": [151, 65, 223, 76], "page": 1},   ← 그 칸에 그려진 값·위치
   {"key": "customer.name", "value": "남궁예태", "bbox_2d": [295, 151, 362, 164], "page": 1},
   {"key": "purpose", "value": "은행 제출용", "bbox_2d": [298, 423, 387, 436], "page": 1}]
```

파일을 이렇게 고치면:

| 고친 것 | 질문 | 정답 |
|---|---|---|
| `purpose` 줄에 `"label": "발급 용도"` | `- purpose: 발급 용도` | 그대로 |
| `customer.rrn` 줄에 `"ask": false` | 그 줄이 빠짐 | 그 항목이 빠짐 |
| `"line": "* {label} → {key}"` | `* 문서번호 → doc_no` … | 그대로 |
| `"answer": "object"` + `prompt` 를 "JSON 객체 {키: 값} 하나로 답하세요 …\n{items}" 로 | 새 문장 | `{"doc_no": "제250459호", "customer.name": "남궁예태", …}` |
| `extra` 에 `{"id": "duty", "prompt": "담당업무는 무엇입니까?", "type": "text", "answer": "{employment.duty}"}` | 새 문항 (과제 form_qa) | `"고객 상담 및 CS 관리"` |

## 3. `questions.json`

```json
{
 "kie": {"prompt": "…\n{items}", "line": "- {key}: {label}{note}", "answer": "list_box", "others": "ask", "items": [
     {"key": "bank", "label": "은행명"},
     {"key": "customer.name", "label": "성명", "from": "applicant.name"},
     {"key": "debts.*.balance", "label": "잔액"},
     {"key": "memo", "label": "비고", "ask": false}]},
 "marks": {"prompt": "…\n{items}", "line": "- {key}: {label}{note}", "answer": "list_box", "others": "ask", "items": [
     {"key": "housing", "label": "주택소유구분", "kind": "체크박스", "options": ["자가", "전세", "월세", "기타"]}]},
 "ocr_field": {"prompt": "이미지에 적힌 글자를 그대로 읽어 옮기세요. …", "exclude": ["customer.rrn"]},
 "ocr_page":  {"prompt": "이 문서 이미지에 보이는 모든 글자를 …", "exclude": []},
 "classify":  {"prompt": "이 문서는 고객이 은행에 제출한 서류입니다. …", "answer": "대출거래신청서", "aliases": []},
 "extra": [
   {"id": "amount", "prompt": "대출 신청금액은 얼마입니까? 원 단위 숫자로만 답하세요.", "type": "number", "answer": "{loan.amount}"},
   {"id": "has_guarantor", "prompt": "보증인 성명이 적혀 있습니까? 예/아니오로 답하세요.", "type": "yesno", "when": "guarantor.name"},
   {"id": "branch", "prompt": "취급 은행과 지점을 '은행 지점' 꼴로 답하세요.", "type": "text", "answer": "{bank} {branch}"}]
}
```

**질문 껍데기**

| 칸 | 뜻 |
|---|---|
| `prompt` | 질문 전문. kie·marks 는 `{items}` 자리에 항목 줄이 들어갑니다 (꼭 있어야 함). 줄바꿈은 `\n` |
| `line` | (kie·marks) 항목 한 줄의 꼴. `{key}` 키, `{label}` 항목명(없으면 `-`), `{note}` 괄호 설명(` (고객 성명)` 또는 빈칸) |

**답 껍데기 `answer`** — 채점이 읽을 수 있는 꼴 중에서:

| 과제 | `answer` | 정답 꼴 | 주 지표 |
|---|---|---|---|
| kie | `list_box` (기본) | `[{"key", "value", "bbox_2d", "page"}]`, 빈 칸 `{"key", "value": null}` | 값+위치 vl_f1 |
| kie | `list` | `[{"key", "value"}]` | 값 f1 (위치 점수 뺌) |
| kie | `object` | `{"키": 값, …}` | 값 f1 |
| marks | `list_box` (기본) | 체크된 보기 `{"key", "value": 보기, "bbox_2d", "page"}`, 도장·서명 `{"key", "value": true/false, …}` | 값+위치 vl_f1 |
| marks | `list` | 위와 같고 위치 없음 | acc |
| classify | (정답 칸) | `"answer"`: 문서명, `"aliases"`: 다른 이름도 정답 | acc |
| ocr_field·ocr_page | (고정) | 칸 글자 / 값 줄 목록 | exact / recall |

- **답 꼴을 바꾸면 `prompt` 도 그 꼴로 고칩니다** (`list`·`object` 면 위치 이야기를 빼고 꼴을 설명). `--check` 가 `list_box` 인데 질문에 `bbox_2d` 가 없거나 그 반대면 문제로 알려 줍니다.

**묻는 칸 `items`** (kie·marks, 한 줄 = 한 칸)

| 칸 | 뜻 |
|---|---|
| `key` | 질문·정답의 키. 반복 행의 번호는 `*` (`debts.*.balance` → `debts.0.balance`, `debts.1.balance` …) |
| `label` | 항목명. 고치면 질문이 바뀝니다 |
| `note` | 괄호 설명. 적으면 그대로, 없으면 키 사전에서 자동 (누구의 무엇·몇 행·같은 항목명 중 몇 번째 칸) |
| `ask: false` | 이 칸은 묻지 않습니다 (정답에서도 빠짐) |
| `from` | (읽기용) 정답을 가져오는 서식 칸. 공통 키로 묻는 칸만 적혀 있습니다 — 키 사전이 정합니다 |
| `kind`, `options` | (marks, 읽기용) 종류와 보기 |
| `others` | 목록에 없는 칸: `ask` 기본대로 묻기 (기본) / `skip` 묻지 않기 |

- **줄을 지우면** `others` 대로 됩니다 (기본 `ask` 면 기본 항목명으로 그대로 묻습니다). 묻지 않으려면 `"ask": false`.
- 질문하는 차례는 문서 순서입니다 (줄 순서와 상관없음). 그 문서에 그려진 칸만 묻습니다 (조건부 칸은 문서마다 다름). 40개(`max_keys`)를 넘으면 그중 골라 묻습니다.
- `ocr_field`·`ocr_page` 의 `exclude`: 값 칸 읽기에서 고르지 않을 칸, 받아쓰기 정답에서 뺄 칸.

**`extra` (서식 전용 질문 → 과제 `form_qa`)** — 질문·답을 전부 서식에서:

| `type` | 정답 | 채점 |
|---|---|---|
| `number` | `answer` 의 `{키}` 를 칸 값으로 채워 숫자로 (`"{loan.amount}"` → 35000000) | 숫자가 같은지 (`tol` 허용 오차, 기본 0) |
| `yesno` | `when` 칸에 값이 있으면 `예`, 비었거나 없으면 `아니오` | 예/아니오 |
| `text` | `answer` 의 `{키}` 를 칸 값으로 채운 글 (`"{bank} {branch}"` → "국민은행 센텀지점") | 띄어쓰기·문장부호를 맞춰 같은지 |

- `{키}` 는 질문 키(공통 키)나 서식의 원래 키 둘 다 됩니다. 칸이 비었거나 없는 문서에서는 그 질문을 만들지 않습니다 (`number`·`text`).
- 답 꼴(숫자만, 예/아니오로)을 질문 문장에 꼭 적으세요. 보고서에는 **서식 전용 질문(form_qa)** 줄로 따로 나옵니다.

**문장을 서식마다 바꿀 때 주의:** 모델은 공통 문장으로 학습했습니다. 서식마다 문장·답 꼴이 다르면 그 서식에서 점수가 흔들릴 수 있습니다
(학습 데이터도 같은 파일로 만들어지므로 학습과 평가는 서로 맞습니다). 서식 사이 점수를 비교할 때는 문장·답 꼴이 같은지 먼저 봅니다 (`--check` 가 공통 문장과 다른 서식을 알려 줌).

## 4. 고치려면 어디를

| 바꾸고 싶은 것 | 고칠 곳 |
|---|---|
| 이 서식의 질문 문장 | `questions.json` 의 과제별 `prompt` (kie·marks 는 항목 줄 꼴 `line` 도) |
| 이 서식의 답 꼴 | `questions.json` 의 `answer` (kie·marks) — `prompt` 도 같이 |
| 이 서식에서 어떤 칸을 묻나, 항목명·설명 | `questions.json` 의 `kie`·`marks` `items` |
| 값 칸 읽기·받아쓰기에서 뺄 칸 | `questions.json` 의 `ocr_field`·`ocr_page` `exclude` |
| 분류 정답 | `questions.json` 의 `classify` |
| 이 서식에만 있는 질문 | `questions.json` 의 `extra` |
| 정답 값이 이상함 (값 자체·칸끼리 관계) | 칸 목록 `fields.json` (값 출처), `generate.py` — 질문 파일이 아님 |
| 칸 위치 (정답 bbox) | studio 영역 편집 / 템플릿 |
| 새 서식의 기본 문장 (공통) | `docgen/bench/prompts.py` + [questions.md](questions.md). 있는 서식에 퍼뜨리려면 `--common-prompt` |
| 그린 문서에서 정답을 꺼내는 법·새 답 꼴 (공통) | `docgen/bench/tasks/<과제>.py` 의 `make(doc)` + 채점 `docgen/bench/evaluate.py` |
| 업무 묶음 과제 (구비·대조·심사) | `docgen/bench/build.py`·`cases.py`·`rules.py` ([benchmark.md](benchmark.md)) |

- 질문 문장이나 답 꼴을 바꾸면 그 서식의 문항이 달라집니다. 예전 점수와 바로 비교하지 않습니다 (데이터셋 기록 `dataset.json` 의 `question_hashes` 로 어느 파일로 만들었는지 확인).
- `questions.json` 은 그림을 바꾸지 않아 **서식 해시에 들어가지 않습니다** (고쳐도 재검수 필요로 바뀌지 않음).

## 5. 만들기·검사

```bash
python -m docgen.formdir questions <ID> --write                    # 없으면 공통 문장으로 새로, 있으면 새 칸·빠진 칸만 더함 (고친 것은 그대로)
python -m docgen.formdir questions --all --write                   # 모든 서식
python -m docgen.formdir questions <ID> --write --common-prompt    # 질문 문장·항목 줄 꼴을 지금 공통 문장으로 되돌림 (답 꼴·묻는 칸은 그대로)
python -m docgen.formdir questions <ID> --check                    # 지금 칸과 맞는지
```

`--check` 가 알려 주는 것:

| | 뜻 | 할 일 |
|---|---|---|
| 문제: 지금 칸에 없는 키 | 칸 키를 바꿨거나 지웠는데 질문 목록은 그대로 | 줄의 `key` 를 고치거나 지움 |
| 문제: extra 의 칸에 없는 키 | `{키}`·`when` 오타 | 고침 |
| 문제: 답 꼴과 질문이 안 맞음 | `list_box` 인데 질문에 위치(`bbox_2d`) 요청이 없음, 또는 반대 | `prompt` 나 `answer` 를 맞춤 |
| 참고: 질문 문장이 공통 문장과 다름 | 이 서식만 문장이 다름 | 일부러가 아니면 `--common-prompt` |
| 참고: 질문 목록에 없는 칸 | 새로 생긴 칸 (`others` 대로 묻는 중) | `--write` 로 더하고 항목명 확인 |
| 참고: 칸의 항목명과 다르게 묻는 칸 | 질문 파일과 칸 목록의 항목명이 다름 | 일부러 바꾼 것이 아니면 맞춤 |

- 질문 목록은 칸 목록과 **따로** 적힙니다. 칸의 항목명이나 키를 바꾸면 질문 파일도 확인하세요 (`--check`).
- studio **서식 다시 읽기**는 모든 서식의 `questions.json` 형식(JSON, `{items}` 자리, 답 꼴 이름, extra 의 type 등)을 검사해 문제로 보여 줍니다.

## 6. 확인하기

- **studio ① 서식 › 문항 Q/A 탭**: 위쪽에 이 서식의 `questions.json`, 아래 [실제 문항 예시 만들기] 로 그 서식 한 건의 질문 전문·정답·채점 조건. 파일을 고친 뒤 다시 누르면 바로 반영됩니다.
- 작은 세트로: `python -m docgen.bench build --types <ID> --per-doc 2 --bundles 0 --out work/qa_<ID>` → `work/qa_<ID>/tasks/kie.jsonl`.

## 7. 새 과제 추가 (공통)

서식 한 건에서 만드는 새 과제는 `docgen/bench/tasks/` 에 파일 하나를 더합니다. `kie.py` 를 견본으로:

1. `TASK`·`NAME`·`PROMPT`·`ANSWER`·`EXAMPLE`·`NOTES` 와 `make(doc)` (→ 문항 목록). `doc.fields` 칸, `doc.q` 서식의 질문 파일, `doc.where()` 위치.
2. `tasks/__init__.py` 의 `SINGLE` **끝에** 붙입니다 (과제들이 난수를 이어 쓰므로 중간에 넣으면 다른 과제 문항이 바뀜).
3. 채점 `evaluate.py` (`SCORERS`·`MAIN`·`TASK_ORDER`·`TASK_TITLE`·`TASK_GROUP`), 구분 `tracking.py`, 보고서 `train/report.py`, 화면 이름 `studio/static/js/datasets.js`.
4. 서식마다 다르게 할 것이 있으면 `docgen/formquestions.py` 에 칸을 더합니다.
5. `build.py` 의 `VERSION` 을 올립니다.
