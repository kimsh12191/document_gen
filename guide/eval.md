# 학습 없이 평가만 하기

이미 학습한 모델을 새 평가 세트로 다시 채점합니다. 예: 실험이 끝난 뒤 실서류 검사부 평가 세트가 새로 생겼을 때.
결과는 새 `workdir`에 쌓이고 기존 학습·점수는 건드리지 않습니다. 학습 서버에서 합니다.

## 1. 평가할 모델 찾기

학습한 모델은 학습 `workdir`의 `merged/` 아래에 있습니다 (LoRA를 합친 전체 모델).

```bash
ls <workdir>/merged/                 # sft-<버전>-checkpoint-<N>, grpo-<버전>-checkpoint-<N>
cat <workdir>/state.json             # sft_checkpoint·grpo_checkpoint 가 마지막으로 쓴 체크포인트
```

실험 묶음(`python -m train sweep`)으로 돌린 모델은 `<root>/<label>/merged/`입니다.

## 2. 평가 전용 설정

학습에 쓴 파이프라인 설정을 복사해 아래 칸만 바꿉니다.

```jsonc
// train/configs/E01-reeval-v2.json
{
  "workdir": "../runs/E01-reeval-v2",                 // 새 이름
  "model": "/share/cv_share/qwen3.5/9b",               // 출발 모델 (같이 평가됨)
  "data": {
    "train": [{"path": "<학습에 쓴 데이터셋 하나>", "count": 100}],   // 섞기가 학습 칸을 요구해서 둠. 학습은 안 함
    "benchmark": [
      …기존 평가 세트 그대로…,
      {"id": "real-inspect", "name": "실서류 검사부", "group": "real", "format": "swift-fields", "gt": "reviewed",
       "paths": ["/share/…/FE_eval/eval_qa_검사부.jsonl"]}
    ],
    "output_dir": "../data/mixed-E01-reeval-v2"        // 새 이름
  },
  "eval": {
    "compare_models": [
      {"label": "a1-syn SFT",     "model": "/share/…/runs/E01-realocr/a1-syn/merged/sft-v0-20261023-checkpoint-3000"},
      {"label": "a2-synreal SFT", "model": "/share/…/runs/E01-realocr/a2-synreal/merged/sft-v0-20261024-checkpoint-3000"}
    ]
  }
}
```

- `compare_models`의 `label`은 비교표의 줄 이름입니다. 겹치지 않게, 실험 안의 모델 이름(`label`)과 SFT·GRPO를 함께 적습니다.
- 출발 모델 점수가 필요 없으면 `"eval": {"skip_start": true, "compare_models": [...]}`.
- 학습 칸(`data.train`)은 학습에 썼던 데이터셋 하나를 `count`를 작게 해 둡니다. 평가 세트와 겹치는 데이터는 넣지 않습니다 (섞기가 멈춤).

## 3. 실행

```bash
python -m train --config train/configs/E01-reeval-v2.json --only prepare     # 평가 문항 만들기
python -m train --config train/configs/E01-reeval-v2.json --only eval_base   # 출발 모델 + compare_models 평가
python -m train --config train/configs/E01-reeval-v2.json --only report      # 비교표
```

결과는 `../runs/E01-reeval-v2/reports/benchmark.md`·`.html`입니다. 줄은 출발 모델과 `compare_models`, 열은 평가 세트별입니다. 읽는 법은 [results.md](results.md).
모델마다 평가 서버를 띄웠다 내리므로 모델 하나에 평가 한 번 분량의 시간이 듭니다. 끊기면 같은 명령을 다시 실행하면 답을 낸 데까지 이어서 합니다.

## 알아 둘 점

- **모든 문항을 처음부터 다시 추론합니다.** 새 세트만 더했어도 기존 세트까지 다시 답합니다.
- **점수는 같은 평가 세트끼리만 비교합니다.** 새 `workdir`의 표 안에서는 모두 같은 문항이라 비교할 수 있습니다. 예전 실험의 점수표와 줄을 섞어 비교하지 않습니다.
- **새 이름으로 만듭니다.** `workdir`·`output_dir`을 예전 실험 것으로 쓰면 이미 섞은 데이터가 있어 새 세트가 들어가지 않습니다.
- 실험 기록(`experiments/E…md`)에는 평가를 다시 한 날짜, 추가한 세트, 결과 폴더를 적습니다.
