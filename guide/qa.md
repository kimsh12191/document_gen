# 질문·답 관리

합성 데이터 한 건은 **질문 + 답** 한 쌍입니다. 이 문서는 서식마다 그 질문과 답이 어떻게 만들어지고, 어디를 고치면 어디가 바뀌는지 다룹니다.
서식 관리 전체는 [forms.md](forms.md), 모델에게 묻는 문장 전문은 [questions.md](questions.md)에 있습니다.

## 1. 한 건이 만들어지는 길

kie(정보 추출), 원본 서식 한 건:

```
질문 ─────────────────────────────────────────────────────────────────
이 문서에서 아래 항목의 값과 위치를 찾아 JSON 목록으로 답하세요. …    ← ① questions.json  kie.prompt (없으면 공통)
항목 (키: 서식의 항목명 …)
- customer.name: 예금주 성명 (고객 성명)                           ← ② fields.json 그 칸: 키 · q.label (없으면 칸 label) · q.note
- account.number: 계좌번호                                          ← ② 다른 칸 (q.ask:false 면 이 줄이 없음)

답 ───────────────────────────────────────────────────────────────────
[{"key": "customer.name",                                          ← ② fields.json 그 칸: key (원본 서식은 없으면 규칙이 항목명으로)
  "value": "남궁예태",                                              ← ③ fields.json 그 칸: source (코드 서식은 generate.py) — 그릴 때마다 채움
  "bbox_2d": [188, 314, 253, 326], "page": 1},                     ← ④ fields.json 그 칸: rect (html·코드 서식은 템플릿 배치)
 …]
 꼴 [{key,value,bbox_2d,page}] / [{key,value}] / {키: 값}            ← ⑤ questions.json  kie.answer (없으면 공통 list_box)
```

| 바꾸고 싶은 것 | 고칠 곳 | 재검수 |
|---|---|---|
| 질문 문장 전체 | ① `questions.json` → `kie.prompt` (marks·classify·ocr_* 도 같은 꼴) | 필요 없음 |
| 이 칸을 묻지 않기 | ② `fields.json` 그 칸 → `"q": {"ask": false}` | 필요 없음 |
| 질문의 항목명·괄호 설명 | ② `fields.json` 그 칸 → `"q": {"label": "…", "note": "…"}` | 필요 없음 |
| 값 칸 읽기·받아쓰기에서 빼기 | `fields.json` 그 칸 → `"q": {"ocr": false}` | 필요 없음 |
| 답의 키 | ② 템플릿 `f("키")` (html·코드) / `fields.json` 그 칸 `"key"` (원본) | 다시 |
| 답의 값 | ③ `fields.json` 그 칸 `"source"` / `generate.py` (코드 서식) | 다시 |
| 답의 위치 | ④ `fields.json` 그 칸 `"rect"` (원본) / 템플릿 배치 (html·코드) | 다시 |
| 답의 모양 | ⑤ `questions.json` → `kie.answer` | 필요 없음 |
| 이 서식에만 있는 질문·답 | `questions.json` → `extra` | 필요 없음 |
| 분류 정답 | `questions.json` → `classify` | 필요 없음 |

- **정답 값은 파일에 적지 않습니다.** 문서를 그릴 때마다 고객이 바뀌므로, 파일에는 "어디서 채우나"(`source`)만 있습니다.
- **기본:** 질문 문장·항목 줄 꼴·답 꼴은 공통 `docgen/forms/_common/questions.json`, 항목명은 칸의 항목명, 괄호 설명은 키 사전.
  서식에서는 **다르게 할 것만** 적습니다 (지금 545종 모두 바꾼 것이 없음).
- 칸 하나에 관한 것(박스·키·값·질문 설정 `q`)은 모두 `fields.json` 의 **그 칸 한 줄**에 있습니다. 카드(`FORM.md`)의 "고칠 곳" 열이 그 줄 번호입니다.
- **확인:** 카드의 "질문 → 답"(다시 만들기: `python -m docgen.formdir card <ID>`), studio 문항 Q/A 탭, `python -m docgen.formdir questions <ID> --show`.

## 2. 칸의 질문 설정 `q` (`fields.json`)

```json
// 원본 서식: items 의 한 칸
{"t": "text", "page": 0, "label": "주민등록번호", "rect": [352.9, 178.8, 549.6, 195.8],
 "q": {"ask": false}}

// html·코드 서식: fields 의 한 칸 (반복 표는 lists.<이름>.fields.<칸>)
"purpose": {"label": "용도", "type": "text", "source": "code",
            "q": {"label": "발급 용도", "note": "제출 목적"}}
```

| `q` 안 | 뜻 |
|---|---|
| `ask: false` | kie·marks 질문과 정답에서 뺌 |
| `label` | 질문의 항목명 (없으면 칸의 항목명) |
| `note` | 괄호 설명 (없으면 키 사전에서 자동: 누구의 무엇·몇 행·같은 항목명 중 몇 번째 칸) |
| `ocr: false` | 값 칸 읽기(ocr_field)에서 고르지 않고, 받아쓰기(ocr_page) 정답에서 뺌 |

- `q` 는 그림을 바꾸지 않아 **서식 해시(재검수)에 들어가지 않습니다.** studio 영역 편집·html 편집으로 저장해도 남습니다.
- 반복 표 칸의 `q` 는 그 열 전체(모든 행)에 적용됩니다.
- html·코드 서식에서 `fields.json` 에 **줄이 없는 칸**(부모 서식이 값을 만드는 복제 서식, 체크·도장·서명, 글자 목록 …)은
  `fields.json` 맨 위 `"q"` 묶음에 키로 적습니다: `"q": {"special_terms.*": {"ask": false}, "seal.company": {"label": "회사 직인"}}`.
  (칸 줄을 새로 만들면 값 출처가 바뀌므로 줄을 더하지 않습니다.) 카드의 키 열이 그 키입니다 (`a ← b` 면 서식 키 b).

## 3. 서식의 질문 껍데기 `questions.json`

```json
{
 "kie": {
   "prompt": "이 증명서에서 아래 항목 값을 JSON 객체 {키: 값} 하나로 답하세요.\n{items}",
   "line": "* {label} → {key}",
   "answer": "object",
   "others": "skip"
 },
 "marks": {"answer": "list", "prompt": "…\n{items}"},
 "classify": {"answer": "재직증명서", "aliases": ["재직 증명서"]},
 "extra": [
   {"id": "amount", "prompt": "대출 신청금액은 얼마입니까? 원 단위 숫자로만 답하세요.", "type": "number", "answer": "{loan.amount}"},
   {"id": "has_guarantor", "prompt": "보증인 성명이 적혀 있습니까? 예/아니오로 답하세요.", "type": "yesno", "when": "guarantor.name"},
   {"id": "branch", "prompt": "취급 은행과 지점을 '은행 지점' 꼴로 답하세요.", "type": "text", "answer": "{bank} {branch}"}
 ]
}
```

| 칸 | 뜻 |
|---|---|
| `prompt` | 질문 전문 (과제마다: kie·marks·classify·ocr_field·ocr_page). kie·marks 는 `{items}` 자리에 항목 줄 (꼭 있어야 함). 줄바꿈은 `\n` |
| `line` | (kie·marks) 항목 한 줄 꼴. `{key}`, `{label}`(없으면 `-`), `{note}`(` (설명)` 또는 빈칸) |
| `answer` | 답 꼴 — 아래 표 |
| `others: "skip"` | (kie·marks) `q` 를 적은 칸만 묻기. 기본은 모든 칸 |
| `classify` | 분류 정답 `answer`, 정답으로 인정할 다른 이름 `aliases` (없으면 키 사전의 문서명) |
| `extra` | 서식 전용 질문 (아래) |

| 과제 | `answer` | 정답 꼴 | 주 지표 |
|---|---|---|---|
| kie | `list_box` (기본) | `[{"key", "value", "bbox_2d", "page"}]`, 빈 칸 `{"key", "value": null}` | 값+위치 vl_f1 |
| kie | `list` | `[{"key", "value"}]` | 값 f1 (위치 점수 뺌) |
| kie | `object` | `{"키": 값, …}` | 값 f1 |
| marks | `list_box` (기본) / `list` | 체크된 보기·도장 유무 (+ 위치) | vl_f1 / acc |

답 꼴을 바꾸면 질문 문장도 그 꼴로 고칩니다 (`list`·`object` 면 위치 이야기를 빼고 꼴을 설명). `check` 가 안 맞으면 알려 줍니다.

**`extra` (서식 전용 질문 → 과제 `form_qa`)**

| `type` | 정답 | 채점 |
|---|---|---|
| `number` | `answer` 의 `{키}` 를 칸 값으로 채워 숫자로 (`"{loan.amount}"` → 35000000) | 숫자가 같은지 (`tol` 허용 오차, 기본 0) |
| `yesno` | `when` 칸에 값이 있으면 `예`, 비었거나 없으면 `아니오` | 예/아니오 |
| `text` | `answer` 의 `{키}` 를 칸 값으로 채운 글 (`"{bank} {branch}"` → "국민은행 센텀지점") | 띄어쓰기·문장부호를 맞춰 같은지 |

`{키}` 는 질문 키(공통 키)나 서식의 원래 키 둘 다 됩니다. 칸이 비었거나 없는 문서에서는 그 질문을 만들지 않습니다 (`number`·`text`).
답 꼴(숫자만, 예/아니오로)을 질문 문장에 꼭 적으세요. 보고서에는 **서식 전용 질문(form_qa)** 줄로 따로 나옵니다.

**문장을 서식마다 바꿀 때 주의:** 모델은 공통 문장으로 학습했습니다. 서식마다 문장·답 꼴이 다르면 그 서식에서 점수가 흔들릴 수 있습니다
(학습 데이터도 같은 파일로 만들어져 학습과 평가는 서로 맞습니다). 서식 사이 점수를 비교할 때는 카드·`check` 로 문장이 같은지 먼저 봅니다.

## 4. 모든 서식에 같은 것

| 바꾸고 싶은 것 | 고칠 곳 |
|---|---|
| 기본 질문 문장·항목 줄 꼴·답 꼴 | `docgen/forms/_common/questions.json` + [questions.md](questions.md) (테스트가 둘을 맞춰 봄). 평가 세트 `VERSION` 을 올림 |
| 괄호 설명·공통 키·문서명 | 키 사전 `docgen/forms/_common/dictionary/` (studio 키 사전 화면) |
| 원본 서식의 항목명 → 키·값 종류 규칙 | `docgen/forms/_common/key_rules.json` (studio 키 사전 화면) |
| 그린 문서에서 정답을 꺼내는 법·새 답 꼴 (엔진) | `docgen/bench/tasks/<과제>.py` 의 `make(doc)` + 채점 `docgen/bench/evaluate.py` |
| 업무 묶음 과제 (구비·대조·심사) | `docgen/bench/build.py`·`cases.py`·`rules.py` ([benchmark.md](benchmark.md)) |

## 5. 명령

```bash
python -m docgen.formdir check <ID>                            # 고친 뒤 이것 하나: 칸 목록·박스·값 출처·q·questions.json·카드
python -m docgen.formdir questions <ID> --show                 # 질문·답 전체 (기본 / 바꿈 표시)
python -m docgen.formdir card <ID>                             # 카드 다시 (실제 질문→답)
python -m docgen.formdir questions --all --slim [--write]      # questions.json 에서 기본과 같은 줄 지우기
```

`check` 가 알려 주는 것 (문제 = 고쳐야 함, 참고 = 알아 둘 것):

| | 뜻 |
|---|---|
| 문제: `q` 에 모르는 칸 / 형식 | `q` 는 `ask`·`label`·`note`·`ocr` 만 |
| 문제: source … | 값 출처가 틀림 ([값 출처 목록](../docgen/forms/_common/values.md)) |
| 문제: 박스가 쪽 밖 | 원본 서식 칸의 `rect` |
| 문제: extra 의 칸에 없는 키 | `{키}`·`when` 오타 |
| 문제: 답 꼴과 질문이 안 맞음 | `list_box` 인데 질문에 위치(`bbox_2d`) 요청이 없음, 또는 반대 |
| 문제: questions.json 의 items·exclude | 칸 설정은 `fields.json` 의 `q` 로 옮겨 적음 |
| 참고: 묻지 않는 칸·항목명을 바꾼 칸·문장이 공통과 다름 | 일부러 바꾼 것인지 확인 |
| 참고: 카드가 오래됨 | `card <ID>` |

studio **서식 다시 읽기**는 모든 서식의 `questions.json` 형식을 검사하고, 카드가 오래된 서식을 알려 줍니다.

## 6. 새 과제 추가 (엔진)

서식 한 건에서 만드는 새 과제는 `docgen/bench/tasks/` 에 파일 하나를 더합니다. `kie.py` 를 견본으로:

1. `TASK`·`NAME`·`PROMPT`·`ANSWER`·`EXAMPLE`·`NOTES` 와 `make(doc)` (→ 문항 목록). `doc.fields` 칸, `doc.q` 서식의 questions.json,
   `doc.fq` 칸마다 질문 설정(q), `doc.where()` 위치.
2. `tasks/__init__.py` 의 `SINGLE` **끝에** 붙입니다 (과제들이 난수를 이어 쓰므로 중간에 넣으면 다른 과제 문항이 바뀜).
3. 채점 `evaluate.py` (`SCORERS`·`MAIN`·`TASK_ORDER`·`TASK_TITLE`·`TASK_GROUP`), 구분 `tracking.py`, 보고서 `train/report.py`, 화면 이름 `studio/static/js/datasets.js`.
4. 기본 문장은 `docgen/forms/_common/questions.json` 에. 칸마다 다르게 할 것이 있으면 `q` 에 칸을 더합니다 (`docgen/fieldinfo.py` `Q_KEYS`).
5. `build.py` 의 `VERSION` 을 올립니다.
