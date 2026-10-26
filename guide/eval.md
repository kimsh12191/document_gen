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

## 4. 다른 실험과 한 화면에 (모아 보기)

이 `workdir`도 `python -m train summary`에 실험 하나로 넣을 수 있습니다 ([training.md 4.1절](training.md#실험-여러-개를-한-화면에-모아-보기)).

```bash
python -m train summary ../runs/E01-realocr ../runs/E01-reeval-v2 --out ../runs/summary.html
```

- 줄 순서는 `compare_models` → 출발 모델 → (있으면) SFT·GRPO입니다. 괄호 %p의 기준은 **`compare_models`의 첫 모델**이니, 기준으로 볼 모델을 맨 앞에 적으세요.
- 다시 평가한 결과는 예전 실험과 문항이 다를 수 있습니다 (새 세트를 더했거나 섞기를 새로 함). 평가 세트마다 문항이 다수와 다른 칸은 흐리게 `†`로 표시되고, 그 칸끼리는 비교하지 않습니다. 같은 id의 세트라도 `†`가 붙으면 예전 점수와 섞어 읽지 마세요.
- 이 `workdir`의 자세한 표 링크는 `reports/benchmark.html`입니다 (3절의 `--only report`를 먼저 돌려야 생깁니다).

## 5. 채점 규칙이 바뀌었을 때 다시 채점

추론은 다시 하지 않고, 저장된 모델 답(`predictions/*.jsonl`)을 지금 채점기로 다시 채점합니다. GPU가 필요 없습니다.

```bash
python -m train rescore ../runs/E01-realocr          # 실험 묶음 결과 폴더: 모델마다 + compare.html 다시
python -m train rescore ../runs/E01-reeval-v2        # workdir 하나: reports/*.json + benchmark.html 다시
```

- 예전 보고서는 `reports/before-rescore-<시각>/`에 옮겨 두고, 과제별로 바뀐 점수를 출력합니다.
- 섞은 폴더는 `<workdir>/config.json`의 `data.output_dir`에서 찾습니다. 없으면 `--data <섞은 폴더>`.
- 끝나면 모아 보기(4절)도 다시 만드세요.

## 알아 둘 점

- **모든 문항을 처음부터 다시 추론합니다.** 새 세트만 더했어도 기존 세트까지 다시 답합니다.
- **점수는 같은 평가 세트끼리만 비교합니다.** 새 `workdir`의 표 안에서는 모두 같은 문항이라 비교할 수 있습니다. 예전 실험의 점수표와 줄을 섞어 비교하지 않습니다.
- **새 이름으로 만듭니다.** `workdir`·`output_dir`을 예전 실험 것으로 쓰면 이미 섞은 데이터가 있어 새 세트가 들어가지 않습니다.
- 실험 기록(`experiments/E…md`)에는 평가를 다시 한 날짜, 추가한 세트, 결과 폴더를 적습니다.
