# 평가

평가 세트를 정하고, 어떻게 채점할지 정하고, 학습 없이 평가만 하거나 다시 채점하는 방법입니다. 학습 서버에서 합니다.
점수 읽는 법은 [results.md](results.md), 과제별 채점 규칙은 [benchmark.md](benchmark.md)에 있습니다.

## 1. 평가 세트 정하기

학습 설정의 `data.benchmark`에 평가 세트를 적습니다. `id` 하나가 세트 하나이고, 점수가 세트마다 따로 나옵니다.

```jsonc
"benchmark": [
  {"id": "syn", "name": "합성", "group": "synthetic", "paths": ["<studio 평가용 데이터셋>"]},
  {"id": "ocr", "name": "OCR", "group": "ocr", "paths": ["<OCR 데이터셋>"]},
  {"id": "real-po", "name": "실서류 매입추심", "group": "real", "format": "swift-fields", "gt": "reviewed",
   "paths": ["/share/…/FE_eval/eval_qa_PO.jsonl"]}
]
```

| 칸 | 뜻 |
|---|---|
| `id`, `name` | 세트 이름 (영문 `id`는 겹치지 않게) |
| `group` | 표에서 묶어 보여 줄 분류. 합산하지는 않음 |
| `paths` | 데이터셋 폴더 또는 swift `.jsonl`. 여러 개면 합쳐서 한 세트 |
| `format` | 생략하면 studio 데이터셋 폴더. swift `.jsonl`은 `"swift-fields"` |
| `gt` | 정답 출처: `exact`(생성기) · `reviewed`(사람 검수) · `pseudo`(사내 OCR·추론 그대로) |
| `scorer` | (선택) 이 세트만 다르게 채점할 함수 (2절) |

- **실서류 swift `.jsonl`**: ms-swift 형식(`messages` user·assistant + `images`)이면 내용과 상관없이 읽습니다. 질문은 그대로 묻고, 정답(assistant) 글은 그대로 채점 함수에 넘깁니다. `scorer`를 적지 않으면 견본 `swift_default.py`로 채점합니다 (2절).
- swift `.jsonl` 은 학습 데이터(`data.train`)에도 같은 `format`·`scorer` 로 넣을 수 있습니다 ([training.md 2절](training.md#2-설정-파일)).
- 평가 세트와 같은 고객·문서가 학습 데이터에 있으면 섞기에서 멈춥니다. swift 는 같은 그림 파일인지도 봅니다.
- 실험끼리 비교하려면 평가 세트를 고정합니다.

## 2. 채점

기본 채점은 `docgen.bench.evaluate` 하나입니다. studio 채점, 학습 보고서, GRPO 보상이 모두 같은 함수입니다.

- 답 앞의 생각 블록(`<think>…</think>`)은 떼고 채점합니다.
- 답이 없거나 형식을 못 읽으면 그 문항은 0점(CER은 최댓값)이고, 답 형식 오류로 따로 셉니다.
- 과제마다 주 지표가 하나 있습니다. 규칙은 [benchmark.md](benchmark.md#과제).
- 서식 폴더의 `questions.json`으로 kie·marks 답 틀을 바꾼 문항(칸 이름을 바꾼 JSON 틀은 `eval.answer_fields`, 줄글 틀은 `eval.text`·`eval.gold`)도 기본 채점이 읽습니다. 틀에 `{bbox_2d}`가 없으면 위치 점수를 빼고 주 지표가 값 `f1`(marks는 `acc`)입니다 ([docgen/forms/README.md](../docgen/forms/README.md) 5.2절).
- 서식 폴더 `qa.py`의 서식 전용 질문(과제 `form_qa`)은 정답 꼴(숫자·예/아니오·글·JSON)대로 채점하고 주 지표는 `acc`입니다.

### 세트마다 채점 함수 붙이기 (`scorer`)

실서류처럼 맞음의 기준이 세트마다 다르면 그 세트에 채점 함수를 붙입니다.

```json
{"id": "real-po", …, "format": "swift-fields", "paths": ["…/eval_qa_PO.jsonl"], "scorer": "../scorers/po.py:score"}
```

- 경로는 설정 파일 기준이고(`train/configs/`의 설정이면 `../scorers/…`), `:함수`를 빼면 `score`입니다. 설정 예시는 [`pipeline.example.json`](../train/configs/pipeline.example.json)의 `real_po_kie`(kie 꼴로 바꾼 swift 세트에 `swift_kie_scorer.py`를 붙임)입니다.
- 돌리기 전에 파일·함수가 있는지 보고, 섞을 때 정답을 답으로 넣어 그 함수로 만점인지 확인합니다. 함수가 정답을 못 읽는 swift 줄은 경고와 함께 건너뜁니다.
- 그 세트의 평가 점수에만 씁니다. 학습 데이터와 GRPO 보상은 그대로입니다. GRPO 보상까지 바꾸는 것은 swift `.jsonl` 학습 데이터(`data.train`)에 붙인 `scorer`뿐입니다 (studio 데이터셋 폴더인 학습 데이터에는 붙일 수 없음).

**견본** (`train/scorers/`): 모두 기본 채점과 같은 점수를 냅니다. 복사해서 고쳐 씁니다.

| 파일 | 붙일 세트 | 고치는 곳 |
|---|---|---|
| [`swift_default.py`](../train/scorers/swift_default.py) | swift `.jsonl` (안 적으면 이것) | `score` |
| [`swift_kie_scorer.py`](../train/scorers/swift_kie_scorer.py) | `temp/swift_to_kie_tmp.py`(v1)·`swift_to_kie_v2_tmp.py`(v2)로 kie 꼴로 바꾼 swift `.jsonl` | `score` |
| [`kie_list_scorer.py`](../train/scorers/kie_list_scorer.py) | `temp/swift_to_kie_v3_tmp.py`로 **합성 kie 와 같은 꼴**(같은 질문, `[{"key", "value"}]` 정답)로 바꾼 `.jsonl`. 합성과 같은 값 채점, 위치 정답이 없으니 주 지표 `f1` | `score` |
| [`kie_default.py`](../train/scorers/kie_default.py) | 값만 보는 정보 추출 | 위쪽 `FIELD_TYPES`에 항목별 비교 기준(`text`·`amount`·`date`·`digits`) |
| [`bank_default.py`](../train/scorers/bank_default.py) | 합성 은행 서류 세트 | 과제마다 함수 하나 (`classify`, `kie` …) |
| [`form_qa_example.py`](../train/scorers/form_qa_example.py) | 합성 은행 서류 세트에서 서식 전용 질문(`form_qa`) 몇 개만 다르게 | `RULES` (`meta.question` = `"<서식ID>.<qa.py 함수 이름>"` → 채점 함수). 나머지 문항은 기본 채점 |
| [`ocr_default.py`](../train/scorers/ocr_default.py) | 합성 OCR·OCR 준비 폴더 | `page_ocr` |

- `swift_default.py`: 질문의 `in order: ["필드", …]`와 답 배열(또는 `{키: 값}` 객체)을 짝지어 필드마다 비교합니다. 대소문자·공백·문장부호는 무시합니다.
- `ocr_default.py`는 문항마다 점수를 내 평균하므로, 과제 전체로 계산하는 기본 표와 CER 등이 조금 다릅니다.

**함수 꼴**

```python
def score(item, output):
    # item["answer"]: 정답 (swift 세트는 정답 글 그대로, 질문은 item["eval"]["prompt"])
    # output: 모델 답 (생각 블록은 뗀 것, 답이 없으면 "")
    return {"metrics": {"f1": 0.83, "field_acc": 0.8}, "main": "f1", "parse_fail": False}
```

- `metrics`는 문항마다 0~1입니다. 세트 점수는 문항 평균이고, `main`이 보고서의 주 지표입니다.
- `parse_fail`이 참이면 그 문항은 0점이고 답 형식 오류로 셉니다.
- 채점 함수가 다른 세트끼리는 점수를 같은 기준으로 비교하지 않습니다.

## 3. 학습 없이 평가만 하기

이미 학습한 모델을 평가합니다. 예: 실험이 끝난 뒤 새 평가 세트가 생겼을 때. 결과는 새 `workdir`에 쌓이고 기존 결과는 건드리지 않습니다.

학습한 모델은 `<workdir>/merged/`(실험 묶음은 `<root>/<label>/merged/`)에 있습니다. 마지막 체크포인트는 `<workdir>/state.json`의 `sft_checkpoint`·`grpo_checkpoint`입니다.

학습 설정을 복사해 아래 칸만 바꿉니다.

```jsonc
{
  "workdir": "../runs/E01-reeval",                       // 새 이름
  "model": "/share/cv_share/qwen3.5/9b",                  // 출발 모델 (같이 평가됨)
  "data": {
    "train": [{"path": "<학습에 쓴 데이터셋 하나>", "count": 100}],   // 섞기가 요구해서 둠. 학습은 안 함
    "benchmark": [ …평가 세트… ],
    "output_dir": "../data/mixed-E01-reeval"              // 새 이름
  },
  "eval": {
    "compare_models": [
      {"label": "a1 SFT", "model": "/share/…/runs/E01/a1/merged/sft-v0-…-checkpoint-3000"},
      {"label": "a2 SFT", "model": "/share/…/runs/E01/a2/merged/sft-v0-…-checkpoint-3000"}
    ]
  }
}
```

```bash
python -m train --config train/configs/E01-reeval.json --only prepare     # 평가 문항 만들기
python -m train --config train/configs/E01-reeval.json --only eval_base   # 출발 모델 + compare_models 평가
python -m train --config train/configs/E01-reeval.json --only report      # 보고서
```

- 결과는 `<workdir>/reports/benchmark.html`·`summary.html`입니다. `summary.html`의 기준(괄호 %p)은 `compare_models`의 첫 모델이니, 기준으로 볼 모델을 맨 앞에 적습니다.
- 출발 모델 점수가 필요 없으면 `"eval": {"skip_start": true, …}`.
- 모델마다 평가 서버를 띄웠다 내립니다. 끊기면 같은 명령으로 이어서 합니다.
- 모든 문항을 처음부터 다시 추론합니다.

## 4. 저장된 답으로 다시 채점 (`rescore`)

채점 코드나 채점 함수를 고쳤을 때, 추론 없이 저장된 모델 답(`predictions/*.jsonl`)으로 다시 채점합니다. GPU가 필요 없습니다.

```bash
python -m train rescore ../runs/exp1 --data ../data/mixed-exp1   # workdir 하나: reports/*.json·benchmark.html·summary.html
python -m train rescore ../runs/E01           # 실험 묶음 결과 폴더: 모델마다 + compare.html·summary.html
```

- 예전 보고서는 `reports/before-rescore-<시각>/`에 옮겨 두고, 과제별로 바뀐 점수를 출력합니다.
- 채점 함수 경로는 섞을 때 문항에 적힙니다. 그 파일을 고치면 됩니다. 다른 파일로 바꾸거나 새로 붙이려면 새 `data.output_dir`로 다시 섞습니다.
- 섞은 폴더는 `<workdir>/config.json`의 `data.output_dir`에서 찾습니다. 이 파일은 실험 묶음의 모델 폴더에만 생기므로, `python -m train`으로 돌린 workdir에는 `--data <섞은 폴더>`(설정의 `data.output_dir`)를 줍니다. 실험 묶음 결과 폴더는 모델마다 `<root>/<label>/data`를 씁니다.
