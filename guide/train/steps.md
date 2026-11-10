# 하나씩 따로 돌리기

[실험 묶음](sweep.md)이 하는 일을 따로 돌리는 법입니다. 모두 학습 서버의 저장소 최상위에서 실행합니다.

| 하려는 것 | 명령 |
|---|---|
| 모델 하나만 학습 | `python -m train --config pipeline.json` (1절) |
| 단계 하나만 · 어느 단계부터 다시 | `--only <단계>` · `--from <단계>` (1절) |
| 학습 없이 모델들 평가만 | `python -m train eval --config eval.json` (2절) |
| 저장된 답으로 보고서 다시 · 채점 규칙을 고친 뒤 다시 채점 | `python -m train report <결과 폴더> [--rescore]` (3절) |
| 실서류 OCR 데이터 만들기 | [ocr.md](ocr.md) |
| 섞은 데이터로 ms-swift 만 | `python -m train.launch …` (4절) |

## 1. 학습 실행 하나 (`python -m train`)

묶음의 모델 하나와 같습니다. `pipeline.json` 에 `workdir`(결과 폴더)를 적습니다.

```bash
python -m train --config train/configs/pipeline.json --dry-run     # 명령만 보기
python -m train --config train/configs/pipeline.json --smoke       # 리허설 (workdir/smoke)
python -m train --config train/configs/pipeline.json               # 전부
python -m train --config train/configs/pipeline.json --only prepare      # 평가 세트 준비·섞기만
python -m train --config train/configs/pipeline.json --from eval_sft     # SFT 평가부터 다시
```

단계: `ocr_prepare` → `prepare`(평가 세트 준비 + 섞기) → `eval_start`(출발 모델 평가) → `sft` → `eval_sft`(병합·평가) → `report`.
끝난 단계는 `<workdir>/state.json` 에 적혀 다시 치면 건너뜁니다. 결과는 `<workdir>/report.html`·`answers.html`·`scores.csv`·`results.json`.

- 섞은 데이터는 `<workdir>/data` (`data.output_dir` 로 바꿀 수 있음). 학습 데이터를 바꿨으면 `data/` 를 지우거나 새 `workdir` 로.
- 실험 묶음 안의 모델 폴더(`<root>/<label>/`)에도 같은 명령이 됩니다: `python -m train --config <root>/<label>/config.json --from eval_sft`.

## 2. 평가만 하기 (`python -m train eval`)

모델 경로들과 평가 세트를 적으면 평가하고 보고서를 만듭니다. 예시 [eval.example.json](../../train/configs/eval.example.json).

```jsonc
{"name": "E03-real-po", "about": "실서류 매입추심에서 모델 비교", "root": "../runs/E03-real-po",
 "base": "pipeline.json",                                  // (선택) 평가 세트·gpus·model_type·eval·cache_dir 를 물려받음
 "baseline": "출발 모델",
 "models": [{"sweep": "../runs/E02-tune"},                 // 그 묶음의 출발 모델·모델들 전부 (label 그대로)
            {"label": "other", "path": "/share/…/merged/sft-v0-…-checkpoint-800"},
            {"label": "a3-ck300", "path": "../runs/E02-tune/a3/sft/v0-…/checkpoint-300"}],   // LoRA 체크포인트면 합쳐서
 "benchmark": [{"id": "real_po_kie", "name": "실서류 매입추심", "group": "real", "format": "swift-fields", "gt": "reviewed",
                "paths": ["/share/…/eval_qa_PO.kie.jsonl"], "scorer": "../scorers/swift_kie_scorer.py:score"}]}
```

```bash
python -m train eval --config train/configs/eval.json [--smoke | --dry-run]
```

- `benchmark` 를 안 적으면 `base` 의 `data.benchmark`. 꼴은 [sweep.md 2절](sweep.md#2-평가-세트-databenchmark)과 같습니다.
- 같은 모델·같은 세트의 답이 `cache_dir` 에 있으면 추론하지 않습니다 (학습 때 낸 답 포함). 모델이나 세트를 더해 다시 치면 새 것만 돕니다.
- LoRA 체크포인트(`adapter_config.json`)는 `"base_model"`(없으면 체크포인트에 적힌 것)과 합쳐 `<root>/merged/<label>/` 에서 평가합니다.
- 결과는 `<root>/report.html`·`answers.html`·`scores.csv` (실험 묶음과 같은 꼴).

## 3. 보고서 다시 (`python -m train report`)

```bash
python -m train report runs/E02-tune               # 저장된 답으로 report.html·answers.html·scores.csv 다시
python -m train report runs/E02-tune --rescore     # 채점 함수·채점 규칙을 고친 뒤: 점수 캐시를 버리고 다시 채점
python -m train report runs/E02-tune --all         # answers.html 에 모든 문항 (기본은 세트·과제마다 30개)
```

추론은 하지 않습니다. 결과 폴더는 `results.json` 이 있는 곳 (실험 묶음 root · 학습 실행 workdir · 평가만 하기 root).

## 4. ms-swift 만 (`python -m train.launch`)

섞은 폴더(`train_sft.jsonl`·`DONE.json`)로 SFT 명령을 만들어 돌립니다. 학습 실행의 `sft` 단계가 부르는 것과 같습니다.

```bash
python -m train.launch --config train/configs/sft.yaml --model <출발 모델> --data <workdir>/data --output <폴더> \
  --gpus 0,1 --options '{"learning_rate": 5e-5}'            # --execute 를 붙이면 실행, 없으면 명령만
```

합친 모델에 Qwen3.5 MTP 가중치가 빠졌을 때: `python -m train.fill_weights <출발 모델> <합친 폴더> --out <새 폴더>` (학습 실행은 병합 직후 자동).

## 5. 실서류 VQA 를 평가 세트로 (`qa_to_swift`)

image/qa JSON 폴더(`{"image": "…png", "qa": [{"question", "answer"}, …]}` 파일들)를 ms-swift `.jsonl` 로 바꿉니다.

```bash
python -m train.qa_to_swift <작업 폴더>/vqa/first_masking_1 <작업 폴더>/first_masking_1_swift.jsonl \
  --image-root <작업 폴더> --check-images [--recursive]
```

- QA 한 쌍이 한 줄. 객체·배열 답은 JSON 글로 넣습니다. 원본은 읽기만 하고, 출력 파일이 있으면 멈춥니다.
- 평가 세트로 쓸 때 채점 함수는 `vqa_scorer.py` (기본 `swift_default.py` 는 이 꼴을 못 읽음):
  `{"id": "real_vqa", "format": "swift-fields", "paths": ["…_swift.jsonl"], "scorer": "../scorers/vqa_scorer.py:score"}`
- swift 추출 데이터를 kie 꼴로 바꾸는 스크립트는 [temp/README.md](../../temp/README.md).
