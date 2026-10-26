# 학습

데이터셋을 `python -m train` 한 번으로 섞어 학습하고 평가합니다.
순서는 섞기 → 출발 모델 평가 → SFT → 평가 → GRPO → 평가 → 보고서입니다.

| 어디서 | 무엇을 |
|---|---|
| **studio 컨테이너** | 데이터셋 만들기 ([studio.md](studio.md)) |
| **학습 서버** (GPU) | 내 이미지 OCR 준비 ([ocr.md](ocr.md)), 학습 (이 문서) |

두 곳은 studio 저장 폴더를 공유합니다. 아래 명령은 모두 **학습 서버의 코드 폴더**(`document_gen/`)에서 실행합니다.

## 0. 처음 한 번

```bash
git clone -b claude/docgen-studio https://github.com/kimsh12191/document_gen.git
cd document_gen
python -c "import swift, vllm, PIL, yaml, docgen.bench.evaluate, train; print('ok')"
```

- `ok`가 나오면 됩니다. 따로 설치할 패키지는 없습니다 (ms-swift·vLLM이 있는 학습 환경).
- git이 안 되는 망이면 인터넷 PC에서 `sh docker/build.sh`로 만든 `docgen-code-*.tar.gz`를 반입해 풉니다.
- 출발 모델 폴더에 `config.json`이 있는지 확인합니다 (예: `/share/cv_share/qwen3.5/9b`).

## 1. 쓸 데이터셋 찾기

```bash
find <studio 저장 폴더>/workspace/datasets -maxdepth 3 -name meta.json
```

- 나온 경로에서 `/meta.json`을 뺀 것이 데이터셋 경로입니다. OCR 데이터셋은 `.../<이름>/prepared`입니다.
- **학습용**(split `train`)과 **평가용**(평가 세트)을 따로 만듭니다. 같은 데이터셋을 양쪽에 넣지 않습니다.
- 데이터셋이 없으면 [studio.md 2절](studio.md#2-합성-데이터-만들기)로 만듭니다. 내 이미지로 OCR 데이터를 만들려면 [ocr.md](ocr.md).

## 2. 설정 파일

```bash
cp train/configs/pipeline.example.json train/configs/pipeline.json
```

`pipeline.json`에서 아래만 고칩니다. 경로는 절대 경로로 씁니다.

```jsonc
{
  "workdir": "../runs/exp1",                  // 결과 폴더. 실험마다 새 이름
  // "ocr_prepare" 줄은 지웁니다 (OCR은 따로 준비)
  "model": "/share/cv_share/qwen3.5/9b",
  "gpus": [0, 1],
  "data": {
    "train": [
      {"path": "<studio 학습용 데이터셋>"},
      {"path": "<OCR 데이터셋>", "count": 20000}       // OCR은 쓸 문항 수를 정함
    ],
    "benchmark": [
      {"id": "syn", "name": "합성", "group": "synthetic", "paths": ["<studio 평가용 데이터셋>"]},
      {"id": "ocr", "name": "OCR", "group": "ocr", "paths": ["<OCR 데이터셋>"]}
    ],
    "output_dir": "../data/mixed-exp1",       // 섞은 결과. 데이터가 바뀌면 새 이름
    …나머지 그대로
```

- **평가 세트(`benchmark`)는 `id`를 붙여 나눕니다.** 점수가 세트마다 따로 나옵니다. 실서류 swift `.jsonl`을 넣는 법, 세트마다 채점 방식을 바꾸는 법은 [eval.md 1·2절](eval.md#1-평가-세트-정하기).
- **OCR 데이터셋은 학습·평가 양쪽에 적어도 됩니다.** 학습 쪽은 학습 문항만, 평가 쪽은 떼어 둔 평가 문항만 가져갑니다.
- **40GB GPU**면 `"sft": {"config": "sft_a100_40g_x2.yaml"}`, `"grpo": {"config": "grpo_a100_40g_x2.yaml", …}`.
- 다른 칸(`task_mix`, `grpo`, `eval`)은 [train/README.md](../train/README.md)에 있습니다. 처음에는 그대로 둡니다.
- 학습률 같은 yaml 값은 yaml을 복사하지 않고 `"sft": {"config": "sft.yaml", "learning_rate": 5e-5}`처럼 칸 하나씩 덮어쓸 수 있습니다 (4절 표).
- studio ⑥ 데이터셋 › 학습 탭에서 데이터셋을 고르면 이 파일을 `train/configs/studio-<이름>.json`으로 써 줍니다. 그때는 `model`·`gpus`만 확인합니다. 학습 서버에서 저장 폴더가 `/out`이 아닌 경로로 보이면 studio `config.json`에 `{"path_map": {"/out": "<학습 서버 경로>"}}`를 둡니다.

## 3. 실행

```bash
python -m train --config train/configs/pipeline.json --smoke          # 리허설 (5 step, 작은 평가)
nohup python -m train --config train/configs/pipeline.json > train.log 2>&1 &   # 본 실행: SFT + GRPO (A100 2장 1~2일)
```

SFT와 GRPO를 나눠 돌릴 수도 있습니다.

```bash
python -m train --config train/configs/pipeline.json --part sft       # 섞기 → 출발 모델 평가 → SFT → 평가 → 보고서
python -m train --config train/configs/pipeline.json --part grpo      # 위 SFT에서 GRPO → 평가 → 보고서 (출발·SFT·GRPO 한 표)
```

| 확인 | 정상 |
|---|---|
| 리허설 | `<workdir>/smoke/reports/benchmark.html` 생김 |
| 진행 | `<workdir>/state.json`의 `done`에 단계가 쌓임 |
| 끝 | `<workdir>/reports/summary.html`·`benchmark.html`·`answers.html` 생김 → 읽는 법 [results.md](results.md) |

- 경로가 틀리면 시작하자마자 틀린 칸을 모두 알려 주고 멈춥니다.
- 중간에 멈추면 **같은 명령을 다시** 실행합니다. 끝난 단계는 건너뜁니다.
- 학습한 모델은 `<workdir>/merged/`에 있습니다.

## 4. 여러 모델을 한 번에 (실험 묶음)

평가 세트는 고정하고, 학습 쪽 설정은 모델마다 바꿔서 여러 모델을 학습·평가한 뒤 표 하나로 비교합니다. 한 번 걸어 두면 차례로 돌고(GPU가 남으면 동시에), 모델 하나가 끝날 때마다 비교표를 다시 만듭니다.

```bash
cp train/configs/sweep.example.json train/configs/E02.sweep.json   # name·about·runs 고치기
python -m train sweep --config train/configs/E02.sweep.json --smoke    # 리허설 (모델마다 5 step)
nohup python -m train sweep --config train/configs/E02.sweep.json > E02.log 2>&1 &
python -m train sweep --config train/configs/E02.sweep.json --status   # 진행 상황
```

### 묶음 파일

`base`(2절의 `pipeline.json`)가 공통 설정이고, `runs`에는 모델마다 **바꿀 칸만** 적습니다.

```jsonc
{
  "name": "E02-tune", "about": "평가 세트 고정, 데이터·학습률·출발 모델·GRPO 비교",
  "base": "pipeline.json", "root": "../runs/E02-tune",
  "gpu_groups": [[0, 1], [2, 3]],                       // GPU 2장씩 두 모델을 동시에 (빼면 하나씩)
  "runs": [
    {"label": "a1-base", "about": "기준: base 그대로"},
    {"label": "a2-realocr", "about": "실서류 OCR 더함", "train": ["<데이터셋>", {"path": "<OCR 준비>", "count": 20000}]},
    {"label": "a3-mix", "about": "과제 비율·그림 예산", "data": {"task_mix": {"kie": 0.3}, "image_max_size": [1800, 1300]}},
    {"label": "a4-lr", "about": "학습률·에폭·LoRA", "sft": {"learning_rate": 5e-5, "num_train_epochs": 2, "lora_rank": 64}},
    {"label": "a5-4b", "about": "다른 출발 모델", "model": "/share/cv_share/qwen3.5/4b"},
    {"label": "a6-grpo", "about": "a1의 SFT에서 GRPO", "from_sft": "a1-base", "grpo": {"beta": 0.08, "count": 1500}},
    {"label": "a7-full", "about": "SFT + GRPO", "part": "all", "sft": {"learning_rate": 5e-5}}
  ]
}
```

전체 예시는 [`train/configs/sweep.example.json`](../train/configs/sweep.example.json)입니다.

### 모델마다 바꿀 수 있는 칸

| 칸 | 무엇 | 예 |
|---|---|---|
| `model`, `model_type` | 출발 모델 폴더와 ms-swift 모델 종류. 다르면 그 출발 모델도 한 번 평가해 표에 넣음 | `"model": "/share/…/qwen3.5/4b"` |
| `train` | 학습 데이터셋 목록 (= `data.train`) | `["<폴더>", {"path": "<폴더>", "count": 20000}]` |
| `data` | 섞기 칸: `task_mix`(과제 비율), `sft_max_examples`(SFT 문항 수), `grpo_holdout`, `image_max_size`·`max_image_tokens_per_sample`(학습 그림 예산), `sft_max_length`, `seed` | `{"task_mix": {"kie": 0.3}}` |
| `sft` | `config`(yaml 파일) + yaml 안의 ms-swift 옵션을 칸 하나씩: `learning_rate`, `num_train_epochs`, `lora_rank`·`lora_alpha`, `tuner_type`(`lora`·`full`), `freeze_vit`·`freeze_aligner`·`freeze_llm`, `per_device_train_batch_size`·`gradient_accumulation_steps`, `warmup_ratio`, `deepspeed`, `save_steps` … | `{"learning_rate": 5e-5}` |
| `grpo` | `sft`와 같은 꼴 (`beta`, `num_generations`, `temperature`, `max_completion_length`, `learning_rate` …) + 후보 고르기 `select`·`candidates`·`count`·`hard_fraction`·`tasks`·`max_images`·`seed` | `{"beta": 0.08}` |
| `part` | `sft`(SFT까지, 기본) · `all`(SFT + GRPO). 묶음 전체에 적어도 됨 | `"all"` |
| `from_sft` | 앞에 적힌 모델의 `label`(또는 다른 묶음의 모델 폴더). 그 SFT 결과에서 GRPO만 돌림. 그 모델의 칸을 물려받고, 그 모델의 SFT가 끝나면 시작 | `"a1-base"` |
| `gpus` | 이 모델만 쓸 GPU (큰 모델 등). 그 GPU가 모두 비면 들어감 | `[0, 1, 2, 3]` |
| `deploy` | 평가 서버 명령 (`eval.deploy_command`). 다른 계열 모델이 옵션을 모를 때 | |
| `set` | 위에 없는 파이프라인 칸 덮어쓰기 | `{"eval": {"concurrency_per_server": 8}}` |
| `label`, `about` | 모델 이름(= 폴더 `<root>/<label>/`, 영문 소문자·숫자·`-`)과 설명. **꼭 적음** | |

**공통값(기본)을 쓰려면 그 칸을 적지 않습니다.**
- 적지 않은 칸은 `base` 값을 씁니다. `sft`·`grpo`·`data`는 칸 하나씩 덮어써서, `"sft": {"learning_rate": 5e-5}`만 적으면 나머지는 yaml 그대로입니다.
- `train`을 적지 않으면 `base`의 `data.train`을 씁니다.
- 모든 모델에 같은 값을 쓰려면 `base`(`pipeline.json`)에 적습니다. 예: 모든 모델의 학습률은 `pipeline.json`의 `"sft": {"learning_rate": 5e-5}`. 이 칸은 묶음 없이 `python -m train`으로 돌릴 때도 같게 됩니다.
- yaml의 기본값은 [`train/configs/sft.yaml`](../train/configs/sft.yaml), [`grpo_a100x2.yaml`](../train/configs/grpo_a100x2.yaml)에 있습니다. 모델을 바꾸면 yaml의 `model_type`은 `model_type` 칸 값으로 덮어씁니다 (기본 `qwen3_5`).

**모델마다 못 바꾸는 것 (평가 고정)**
- `data.benchmark`(평가 세트·채점 함수), `eval.inference_config`(답 내기 설정), `eval.compare_models`는 `base`에서만 정합니다. `set`·`data`로 바꾸면 시작 전에 멈춥니다.
- 평가 그림은 `base`의 그림 예산으로 만듭니다. 모델마다 `data.image_max_size`를 바꿔도 학습 그림만 바뀝니다.
- 출발 모델 계열이 달라 그림 조각 크기가 다르면(예: 32px, 28px) 평가 그림 크기가 조금 다릅니다. 문항은 같아서 표에 넣고 비교표 위에 메모를 붙입니다.

### 묶음 전체 칸

| 칸 | 뜻 |
|---|---|
| `name`, `about` | 실험 ID와 무엇을 확인하는지 (필수). 비교표 맨 위와 `--status`에 나옴 |
| `record` | 실험 기록 파일 (선택, 예: `experiments/E02.md`) |
| `base` | 공통 파이프라인 설정 (2절의 `pipeline.json`) |
| `root` | 결과 폴더. 모델마다 `<root>/<label>/`가 `workdir` |
| `part` | 모든 모델의 기본 `part` |
| `baseline` | 비교표 괄호(%p)의 기준 모델 `label` (기본 첫 모델) |
| `gpu_groups` | 동시에 돌릴 GPU 묶음 (예: `[[0,1],[2,3]]`). 빼면 `base`의 `gpus`로 하나씩 |
| `start_from` | (선택) 다른 묶음의 모델 폴더. 출발 모델이 같으면 그 출발 모델 평가를 가져다 씀 |

### 동시에 돌리기

- `gpu_groups`의 묶음마다 모델 하나가 들어가고, 끝나면 다음 모델이 들어갑니다. 묶음 하나의 GPU 수가 그 모델의 학습·평가 GPU 수입니다.
- 묶음마다 평가 서버 포트(`port_base` + 10×첫 GPU 번호)와 학습 포트(`MASTER_PORT`)를 다르게 잡습니다. 따로 할 일은 없습니다.
- 메모리가 더 필요한 모델은 `gpus`로 GPU를 더 줍니다. 그 GPU가 모두 빌 때까지 기다립니다.
- GPU 묶음 크기가 다르면 같은 yaml이라도 배치 크기(GPU 수 × `per_device_train_batch_size` × `gradient_accumulation_steps`)가 달라집니다. 비교할 모델끼리는 같은 크기의 묶음을 쓰거나 `gradient_accumulation_steps`로 맞춥니다.

### 결과

| 파일 | 내용 |
|---|---|
| `<root>/summary.html` | **한 화면.** 평가 세트·과제마다 주 지표, 열은 모델, 괄호는 `baseline` 대비 %p. 위쪽 표에 모델마다 **바꾼 설정**이 나옴 |
| `<root>/compare.html` | 자세한 비교표 (평가 세트별, 답 형식 오류, 세부 표) |
| `<root>/answers.html` | **문항별 모델 답.** 평가 세트·과제마다 표본 30개(모델끼리 점수가 갈린 문항 먼저)의 질문·그림·정답·모델마다 답과 점수 |

읽는 법은 [results.md](results.md#어디서-보나)입니다.

### 그 밖에

- 시작 전에 모든 모델의 설정을 한꺼번에 검사합니다. 틀린 것이 있으면 하나도 돌리지 않습니다.
- 출발 모델 평가는 서로 다른 출발 모델마다 한 번씩만 합니다.
- 한 모델이 실패해도 다음으로 갑니다. 그 모델에서 `from_sft`한 모델은 돌리지 않습니다. `--status`에 실패와 로그(`<root>/<label>/sweep.log`)가 나옵니다.
- 같은 명령을 다시 치면 이어서 돕니다. 모델을 `runs`에 더하면 그것만 돌아 표에 붙습니다. 이미 돈 모델의 설정을 바꾸면 그 모델은 돌리지 않으니 새 `label`로 추가합니다.
- GRPO를 하지 않을 묶음이면 `base`에 `"grpo": {"select": "random"}`을 두어 SFT 평가 뒤 GRPO 후보 답 내기를 건너뜁니다.

## 5. 다시 돌릴 때

| 하고 싶은 것 | 방법 |
|---|---|
| 이어서 | 같은 명령 |
| 새 실험 | `workdir` 새 이름 |
| 데이터 구성을 바꿈 | `data.output_dir` 새 이름 |
| 끝난 SFT에서 GRPO | `--part grpo` |
| 다른 실험의 SFT에서 GRPO | `--part grpo --sft-checkpoint <폴더>` |
| GRPO 설정을 바꿔 다시 | `--from grpo` (앞 GRPO 점수도 표에 남음) |
| SFT부터 다시 | `--from sft` |
| 한 단계만 | `--only <단계>` (`prepare` `eval_base` `sft` `eval_sft` `select` `grpo` `eval_grpo` `report`) |
| 명령만 보기 | `--dry-run` |
| 학습 없이 평가만, 다시 채점 | [eval.md](eval.md) |
| 생성기 코드가 바뀜 | 데이터셋을 새 이름으로 다시 만들고 `data` 경로·`output_dir`·`workdir`을 새로. 옛 세트와 점수는 직접 비교하지 않음 |

## 6. 에러

| 에러 | 할 일 |
|---|---|
| `설정(…)의 경로를 확인하세요` | 메시지에 나온 칸을 `meta.json`이 있는 폴더의 절대 경로로 |
| `CUDA out of memory` | 40GB yaml로 (2절) |
| `Output already exists` / `already prepared` | `output_dir`을 새 이름으로 (지우지 말 것) |
| `training rows share a customer or document with the benchmark` | 평가용 데이터셋이 `train`에 들어감. 빼기 |
| `Reference answers do not score 1.0` | 데이터를 만든 코드와 지금 코드가 다름(같은 코드로 데이터 다시 만들기), 또는 붙인 채점 함수가 정답에 만점을 주지 않음 |
| `Server on port … exited` / `not ready in time` | 평가 서버(vLLM)가 못 뜸. `logs/<단계>-server0.log` 끝과 `nvidia-smi` 확인 |
| `Port … is already in use` | 예전 평가 서버를 끄거나 `eval.port_base` 변경 |
| `WARNING: 평가 문항 N개는 …` | 그림이 서버 한도(기본 16장)보다 많은 문항을 빼고 `<workdir>/benchmark_over_image_limit.jsonl`에 남김 |
| `Prediction run settings or input changed` | 끊긴 평가의 답 파일이 지금 평가 문항과 다름. `predictions/<run>.jsonl`과 `.meta.json`을 다른 이름으로 옮기고 같은 명령 |
| `Multiple possible model types found` | `model_type`이 `qwen3_5`인지 |

로그는 `<workdir>/logs/<단계>.log`에 있습니다.
