# 질문·답 관리 (서식별 questions.json · 공통 과제 파일)

합성 데이터의 **질문과 정답이 어디서 어떻게 만들어지는지**, 고치려면 어디를 고치는지 정리한 문서입니다.
모델에게 어떻게 물으면 되는지(질문 문장과 답 형식)는 [questions.md](questions.md), 서식 추가는 [new-forms.md](new-forms.md)에 있습니다.

## 1. 한눈에

```
서식 폴더 docgen/forms/<ID>/  (서식마다)                      공통 (모든 서식이 같이 씀)
  template.html.j2   모양·칸 자리                              docgen/bench/prompts.py        질문 지시문
  fields.json        칸: 키·항목명·타입·값 출처                  docgen/bench/tasks/<과제>.py   답 구조·고르는 규칙 (make)
  generate.py        칸끼리 관계 (선택)                          docgen/bench/evaluate.py       채점
  questions.json     이 서식의 질문·답  ← 여기서 관리
        │
        ▼  문서를 그릴 때마다 (고객·seed 마다 값이 다름)
  그린 칸: 키·항목명·값·위치  ──→  과제 파일이 questions.json 대로 질문·정답을 만듦  ──→  tasks/<과제>.jsonl
```

- **정답은 사람이 단 값이 아닙니다.** 문서를 그릴 때 칸에 넣은 값과 그 위치가 그대로 정답입니다. 그래서 `questions.json` 에는 정답 **값**이 아니라 **어느 칸이 답인지**만 적습니다 (같은 서식도 문서마다 고객·값이 다름).
- **서식마다 다른 것은 서식 폴더에, 모든 서식이 같은 것은 공통에.** 질문 지시문·답 구조·채점은 모델이 학습한 꼴이라 서식마다 바꾸지 않습니다.
- `questions.json` 이 없는 서식은 공통 규칙 그대로 묻습니다. 저장소의 545종은 지금 규칙 그대로 만든 파일이 들어 있습니다 (파일이 있어도 문항이 바이트 단위로 같음을 확인).

## 2. 질문·답의 모양

**정보 추출(kie)** — 대출거래신청서의 실제 문항:

```
┌ 공통 지시문 (prompts.py P_KIE — 모든 서식이 같음)
│ 이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. 항목마다 {"key": 키, "value": 문서에 적힌 값 그대로,
│ "bbox_2d": [x1, y1, x2, y2], "page": 쪽 번호} 를 쓰세요. … 문서에 비어 있거나 없는 항목은 {"key": 키, "value": null} 로 답하세요.
│ 항목 (키: 서식의 항목명 (누구의 무엇·몇 번째 행))
└
┌ 항목 줄 (questions.json 의 kie.items — 서식마다)
│ - bank: 은행명
│ - customer.name: 성명 (고객 성명)          ← "- 키: 항목명 (설명)"
│ - debts.0.balance: 잔액 (1행)
└
```

정답:

```json
[{"key": "bank", "value": "국민은행", "bbox_2d": [104, 39, 197, 61], "page": 1},
 {"key": "customer.name", "value": "남궁예태", "bbox_2d": [200, 172, 257, 183], "page": 1},
 {"key": "memo", "value": null}]
```

| 과제 | 질문 | 정답 | 서식에서 정하는 것 (`questions.json`) |
|---|---|---|---|
| `kie` 정보 추출 | 공통 지시문 + 항목 줄 | `[{"key", "value", "bbox_2d", "page"}]` | 묻는 칸, 항목명, 설명 |
| `marks` 체크·도장·서명 | 공통 지시문 + 항목 줄 (종류·보기) | 체크된 보기 / 도장·서명 true·false + 위치 | 묻는 칸, 항목명 |
| `classify` 서류 분류 | 고정 문장 | 문서명 한 줄 | 정답 문서명, 다른 이름 |
| `ocr_field` 값 칸 읽기 | 고정 문장 (칸을 잘라낸 그림) | 칸의 글자 | 고르지 않을 칸 |
| `ocr_page` 전체 받아쓰기 | 고정 문장 | 값 줄 목록 | 정답에서 뺄 칸 |
| `freetext` 기타 칸 정리 | 공통 지시문 + 칸 이름·기준일 | `{"purpose", "amount", …}` | (없음 — 기타 칸에 쓴 글이 정함) |
| `form_qa` 서식 전용 질문 | 서식에서 쓴 문장 | 숫자 / 예·아니오 / 글 한 줄 | 질문 전부 (`extra`) |

질문 지시문 전문은 [questions.md](questions.md), 실제 데이터 예시는 [tasks.md](tasks.md).

## 3. `questions.json`

```json
{
 "kie": {"others": "ask", "items": [
   {"key": "bank", "label": "은행명"},
   {"key": "customer.name", "label": "성명", "from": "applicant.name"},
   {"key": "debts.*.balance", "label": "잔액"},
   {"key": "memo", "label": "비고", "ask": false}
  ]},
 "marks": {"others": "ask", "items": [
   {"key": "housing", "label": "주택소유구분", "kind": "체크박스", "options": ["자가", "전세", "월세", "기타"]}
  ]},
 "ocr_field": {"exclude": ["customer.rrn"]},
 "ocr_page": {"exclude": []},
 "classify": {"answer": "대출거래신청서", "aliases": []},
 "extra": [
   {"id": "amount", "prompt": "대출 신청금액은 얼마입니까? 원 단위 숫자로만 답하세요.", "type": "number", "answer": "{loan.amount}"},
   {"id": "has_guarantor", "prompt": "보증인 성명이 적혀 있습니까? 예/아니오로 답하세요.", "type": "yesno", "when": "guarantor.name"},
   {"id": "branch", "prompt": "취급 은행과 지점을 '은행 지점' 꼴로 답하세요.", "type": "text", "answer": "{bank} {branch}"}
  ]
}
```

**kie·marks 의 `items` (한 줄 = 한 칸)**

| 칸 | 뜻 |
|---|---|
| `key` | 질문에 쓰는 키. 반복 행의 번호는 `*` (`debts.*.balance` → 질문에는 `debts.0.balance`, `debts.1.balance` …) |
| `label` | 질문의 항목명. 고치면 질문이 바뀝니다 |
| `note` | 괄호 설명. 적으면 그대로, 없으면 키 사전에서 자동 (누구의 무엇·몇 행·같은 항목명 중 몇 번째 칸) |
| `ask: false` | 이 칸은 묻지 않습니다 |
| `from` | (읽기용) 답을 가져오는 서식 칸. 공통 키로 묻는 칸만 적혀 있습니다 — 키 사전이 정합니다 |
| `kind`, `options` | (marks, 읽기용) 종류와 보기 |
| `others` | 목록에 없는 칸: `ask` 기본대로 묻기 (기본) / `skip` 묻지 않기 |

- **줄을 지우면** `others` 대로 됩니다 (기본 `ask` 면 기본 항목명으로 그대로 묻습니다). 묻지 않으려면 `"ask": false` 를 적으세요.
- 질문하는 차례는 문서 순서입니다 (줄 순서와 상관없음). 항목이 40개(`max_keys`)를 넘으면 그중 골라 묻는 것은 공통 규칙.

**`extra` (서식 전용 질문 → 과제 `form_qa`)**

| `type` | 정답 | 채점 |
|---|---|---|
| `number` | `answer` 의 `{키}` 를 칸 값으로 채워 숫자로 (`"{loan.amount}"` → 35000000) | 숫자가 같은지 (`tol` 허용 오차, 기본 0) |
| `yesno` | `when` 칸에 값이 있으면 `예`, 비었거나 없으면 `아니오` | 예/아니오 |
| `text` | `answer` 의 `{키}` 를 칸 값으로 채운 글 (`"{bank} {branch}"` → "국민은행 센텀지점") | 띄어쓰기·문장부호를 맞춰 같은지 |

- `{키}` 는 질문 키(공통 키)나 서식의 원래 키 둘 다 됩니다. 칸이 비었거나 없는 문서에서는 그 질문을 만들지 않습니다 (`number`·`text`).
- 질문 문장은 직접 씁니다. 답 꼴(숫자만, 예/아니오로)을 문장에 꼭 적으세요.
- 보고서에는 과제 **서식 전용 질문(form_qa)** 줄로 따로 나옵니다 (주 지표 acc).

## 4. 고치려면 어디를

| 바꾸고 싶은 것 | 고칠 곳 |
|---|---|
| 이 서식에서 어떤 칸을 묻나, 항목명·설명 | `docgen/forms/<ID>/questions.json` 의 `kie`·`marks` |
| 이 서식에서 값 칸 읽기·받아쓰기에서 뺄 칸 | `questions.json` 의 `ocr_field`·`ocr_page` `exclude` |
| 이 서식의 분류 정답 | `questions.json` 의 `classify` |
| 이 서식에만 있는 질문 | `questions.json` 의 `extra` |
| 정답 값이 이상함 (값 자체·칸끼리 관계) | 칸 목록 `fields.json` (값 출처), `generate.py` — 질문 파일이 아님 |
| 칸 위치 (정답 bbox) | studio 영역 편집 / 템플릿 |
| 모든 서식의 질문 지시문 | `docgen/bench/prompts.py` + [questions.md](questions.md) (테스트가 둘을 맞춰 봄) |
| 모든 서식의 답 구조·고르는 규칙 | `docgen/bench/tasks/<과제>.py` 의 `make(doc)` |
| 채점 | `docgen/bench/evaluate.py` |
| 업무 묶음 과제 (구비·대조·심사) | `docgen/bench/build.py`·`cases.py`·`rules.py` ([benchmark.md](benchmark.md)) |

- 공통 지시문·답 구조를 바꾸면 평가 세트가 달라집니다. `build.py` 의 `VERSION` 을 올리고, 예전 점수와 바로 비교하지 않습니다.
- `questions.json` 은 그림을 바꾸지 않아 **서식 해시에 들어가지 않습니다** (고쳐도 재검수 필요로 바뀌지 않음). 데이터셋 기록 `dataset.json` 의 `question_hashes` 에 서식마다 남습니다.

## 5. 만들기·검사

```bash
python -m docgen.formdir questions <ID> --write      # 없으면 지금 규칙 그대로 새로, 있으면 새로 생긴 칸만 더함 (고친 줄은 그대로)
python -m docgen.formdir questions --all --write     # 모든 서식
python -m docgen.formdir questions <ID> --check      # 지금 칸과 맞는지
```

`--check` 가 알려 주는 것:

| | 뜻 | 할 일 |
|---|---|---|
| 문제: 지금 칸에 없는 키 | 칸 키를 바꿨거나 지웠는데 질문 목록은 그대로 | 줄의 `key` 를 고치거나 지움 |
| 문제: extra 의 칸에 없는 키 | `{키}`·`when` 오타 | 고침 |
| 참고: 질문 목록에 없는 칸 | 새로 생긴 칸 (`others` 대로 묻는 중) | `--write` 로 더하고 항목명 확인 |
| 참고: 칸의 항목명과 다르게 묻는 칸 | 질문 파일과 칸 목록의 항목명이 다름 | 일부러 바꾼 것이 아니면 맞춤 |

- 질문 목록은 칸 목록과 **따로** 적힙니다. 칸의 항목명이나 키를 바꾸면 질문 파일도 확인하세요 (`--check`).
- studio **서식 다시 읽기**는 모든 서식의 `questions.json` 형식(JSON·필수 칸·type)을 검사해 문제로 보여 줍니다.

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
