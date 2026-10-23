# 학습

studio 데이터셋(과 내 이미지로 만든 OCR 데이터)을 `python -m train` 한 번으로 섞어 학습하고 평가합니다.
단계는 섞기 → 출발 모델 평가 → SFT → 평가 → GRPO → 평가 → 비교표입니다.

| 어디서 | 무엇을 |
|---|---|
| **studio 컨테이너** | 데이터셋 만들기 ([studio.md](studio.md)) |
| **학습 서버** (GPU) | OCR 준비 ([ocr.md](ocr.md)), 학습 (이 문서) |

두 곳은 studio 저장 폴더를 공유합니다. 아래 명령은 모두 **학습 서버의 코드 폴더**(`document_gen/`)에서 실행합니다.

## 0. 처음 한 번

```bash
git clone -b claude/docgen-studio https://github.com/kimsh12191/document_gen.git
cd document_gen
python -c "import swift, vllm, PIL, yaml, docgen.bench.evaluate, train; print('ok')"
```

- `ok`가 나오면 됩니다. 설치할 패키지는 없습니다 (ms-swift·vLLM이 있는 학습 환경이면 됨).
- git이 안 되면 인터넷 PC에서 `sh docker/build.sh`로 만든 `docgen-code-*.tar.gz`를 반입해 풉니다.
- 출발 모델 폴더에 `config.json`이 있는지 확인합니다 (예: `/share/cv_share/qwen3.5/9b`).

## 1. 쓸 데이터셋 찾기

```bash
find <studio 저장 폴더>/workspace/datasets -maxdepth 3 -name meta.json
```

- 나온 경로에서 `/meta.json`을 뺀 것이 데이터셋 경로입니다.
- **학습용**은 split `train`으로 만든 것, **평가용**은 평가 세트로 만든 것입니다. 같은 데이터셋을 양쪽에 넣지 않습니다.
- OCR 데이터셋은 `.../<이름>/prepared`가 경로입니다.
- 데이터셋이 아직 없으면 [studio.md 2절](studio.md#2-합성-데이터-만들기)로 만듭니다.

## 2. (선택) 내 이미지로 OCR 데이터

[ocr.md](ocr.md)대로 준비하면 결과 폴더(예: `data/ocr-v1`)가 생깁니다. 이 폴더도 데이터셋입니다.

## 3. 설정 파일

```bash
cp train/configs/pipeline.example.json train/configs/pipeline.json
```

`pipeline.json`에서 아래만 고칩니다. 경로는 절대 경로로 씁니다.

```jsonc
{
  "workdir": "../runs/exp1",                  // 결과 폴더. 실험마다 새 이름
  // "ocr_prepare" 줄은 지웁니다 (OCR은 2에서 따로 준비)
  "model": "/share/cv_share/qwen3.5/9b",
  "gpus": [0, 1],
  "data": {
    "train": [
      {"path": "<studio 학습용 데이터셋>"},
      {"path": "<코드 폴더>/data/ocr-v1", "count": 20000}       // OCR은 쓸 문항 수를 정함
    ],
    "benchmark": [
      "<studio 평가용 데이터셋>",
      "<코드 폴더>/data/ocr-v1"
    ],
    "output_dir": "../data/mixed-exp1",       // 섞은 결과. 데이터가 바뀌면 새 이름
    …나머지 그대로
```

- **OCR 폴더는 학습·평가 양쪽에 적습니다.** 학습 쪽은 학습 문항만, 평가 쪽은 떼어 둔 평가 문항만 가져갑니다.
- **실서류 swift `.jsonl`은 평가에 파일 경로를 그대로 적고 `"format": "swift-fields"`를 붙입니다.** 질문에 `in order: ["필드", …]`가 있고 답이 같은 순서의 문자열 배열인 꼴(`["값", …]`)입니다. 질문은 그대로 묻고, 필드마다 맞았는지로 채점합니다(정보 추출 `kie`: `field_acc`·`f1`, 글자 하나까지 같은 비율 `field_exact`). 읽지 못한 줄은 `WARNING`과 함께 건너뜁니다. `"gt"`에는 정답 출처(`reviewed` 사람 검수 · `pseudo` 사내 OCR·추론 그대로)를 적습니다. 형식을 적지 않은 `.jsonl`은 받지 않습니다:
  ```jsonc
  "benchmark": [
    {"id": "syn", "name": "합성", "group": "synthetic", "paths": ["<studio 평가용 데이터셋>"]},
    {"id": "real-fx", "name": "실서류 외환", "group": "real", "format": "swift-fields", "gt": "reviewed",
     "paths": ["/database/…/eval/eval_qa_PO.jsonl"]},
    {"id": "real-inspect", "name": "실서류 검사부", "group": "real", "format": "swift-fields", "gt": "reviewed",
     "paths": ["/database/…/검사부.jsonl"]}
  ]
  ```
- **40GB GPU**면 `"sft": {"config": "sft_a100_40g_x2.yaml"}`, `"grpo": {"config": "grpo_a100_40g_x2.yaml", …}`.
- 다른 칸(`task_mix`, `grpo`, `eval`)은 [train/README.md](../train/README.md)에 설명이 있습니다. 처음에는 그대로 둡니다.
- studio ⑥ 데이터셋 › 학습 탭에서 데이터셋을 고르면 이 파일을 `train/configs/studio-<이름>.json`으로 써 줍니다. 그때는 `model`·`gpus`만 확인합니다.
  학습 서버에서 저장 폴더가 `/out`이 아닌 경로로 보이면 studio `config.json`에 `{"path_map": {"/out": "<학습 서버 경로>"}}`를 둡니다. 학습이 끝나면 studio가 결과를 평가 세트마다 모델 답으로 붙입니다.

## 4. 실행

```bash
python -m train --config train/configs/pipeline.json --smoke          # 리허설 (5 step, 작은 평가)
nohup python -m train --config train/configs/pipeline.json > train.log 2>&1 &   # 본 실행: SFT + GRPO (A100 2장 1~2일)
```

SFT와 GRPO를 따로 돌릴 수도 있습니다. 둘 다 끝나면 점수표를 만듭니다.

```bash
python -m train --config train/configs/pipeline.json --part sft       # 섞기 → 출발 모델 평가 → SFT → SFT 평가 → 점수표
python -m train --config train/configs/pipeline.json --part grpo      # 위 SFT에서 GRPO → 평가 → 점수표 (출발·SFT·GRPO 한 표)
python -m train --config train/configs/pipeline.json --part grpo --sft-checkpoint <SFT 체크포인트 폴더>   # 다른 SFT에서 GRPO
```

| 확인 | 정상 |
|---|---|
| 리허설 | `train/runs/exp1/smoke/reports/benchmark.html` 생김 |
| 진행 | `cat train/runs/exp1/state.json` 의 `done`에 단계가 쌓임 |
| 끝 | `train/runs/exp1/reports/benchmark.html` 생김 → 읽는 법 [results.md](results.md) |

- 경로가 틀리면 시작하자마자 틀린 칸을 모두 알려 주고 멈춥니다.
- 중간에 멈추면 **같은 명령을 다시** 실행합니다. 끝난 단계는 건너뜁니다.
- 학습한 모델은 `train/runs/exp1/merged/`에 있습니다.

## 4.1 학습 데이터만 바꾼 모델 여러 개 (실험 묶음)

한 번 걸어 두고 나중에 비교표만 봅니다. 모델을 차례로 섞기 → SFT → 평가하고, 하나 끝날 때마다 비교표를 다시 만듭니다.

```bash
cp train/configs/sweep.example.json train/configs/E01-realocr.sweep.json   # name·about·runs 고치기
nohup python -m train sweep --config train/configs/E01-realocr.sweep.json > E01.log 2>&1 &
python -m train sweep --config train/configs/E01-realocr.sweep.json --status   # 진행 상황
```

| 칸 | 뜻 |
|---|---|
| `name`, `about` | 실험 ID와 무엇을 확인하는지 (필수). 비교표 맨 위와 `--status`에 나옴 |
| `record` | 실험 기록 파일 (선택, 예: `experiments/E01-realocr.md`) |
| `base` | 공통 파이프라인 설정 (`model`, `sft`, `data.benchmark`, `eval` …). 3절의 `pipeline.json` |
| `root` | 결과 폴더. 모델마다 `<root>/<label>/`가 `workdir`, `<root>/<label>/data`가 섞은 데이터 |
| `part` | `sft`(SFT까지, 기본) · `all`(SFT + GRPO). `runs`마다 따로 적어 덮어쓸 수 있음 |
| `start_from` | (선택) 다른 묶음의 모델 폴더 (예: `../runs/E01-realocr/a1-syn`). 그 출발 모델 평가를 가져다 쓰고 이 묶음에서는 출발 모델을 평가하지 않음 |
| `runs[]` | `label`(이 실험 안의 모델 이름 = 폴더 이름, 영문 소문자·숫자·`-`), `about`(이 모델이 무엇인지, 필수), `train`(= `data.train`), `part`(선택). 꼭 필요할 때만 `set`으로 그 모델의 설정 칸을 덮어씀 |

**모든 모델은 같은 출발 모델(`base`의 `model`)에서 각자 SFT합니다.** 앞 모델에 이어서 학습하지 않습니다. 학습 설정·seed·평가 세트도 `base`에서 같게 가져옵니다.

- **결과:** `<root>/compare.md`·`.html`·`.csv`. 맨 위에 실험 설명과 모델별 설명·학습 데이터, 아래에 점수표(출발 모델이 Δ의 기준).
- **출발 모델 평가는 첫 모델에서만** 합니다. 나머지는 `eval.skip_start`. 평가 세트를 고정해 실험을 이어 가면 `start_from`으로 앞 실험의 것을 씁니다. 평가 문항·그림 설정이 다르면 쓰지 않고 첫 모델에서 다시 평가합니다.
- **GRPO:** 비교표에 `<label> GRPO` 줄이 붙습니다. SFT로 끝난 모델의 `part`를 `all`로 바꿔 다시 치면 SFT는 건너뛰고 GRPO만 돕니다 (`base`의 `grpo.select`가 `mine`이어야 SFT 평가 때 후보 답을 내 둡니다).
- **시작 전에 모든 모델의 설정을 한꺼번에 검사합니다** (평가 칸 `id`·`format`·`gt`, 출발 모델, 학습·평가 경로, `label`). 틀린 것이 있으면 목록을 보여 주고 하나도 돌리지 않습니다.
- **한 모델이 실패해도 다음으로** 갑니다. `--status`에 실패와 로그(`<root>/<label>/sweep.log`, 자세히는 `<root>/<label>/logs/`)가 나옵니다.
- **같은 명령을 다시 치면 이어서** 돕니다. 끝난 모델은 건너뛰고, 모델을 `runs`에 더하면 그것만 돌아 표에 붙습니다.
- **이미 돈 모델의 설정(base·train·set)을 바꾸면 그 모델은 돌리지 않습니다.** 새 `label`로 추가하세요.
- 평가 문항·그림 설정이 첫 모델과 다른 모델은 표에서 빼고 `compare_notes.txt`에 이유를 남깁니다.
- GRPO를 하지 않을 묶음이면 `base`에 `"grpo": {"select": "random"}`을 두어 SFT 평가 뒤 GRPO 후보 답 내기(추론 수천 건)를 건너뜁니다. 나중에 GRPO를 할 수도 있으면 그대로(`mine`) 둡니다.
- 처음에는 `--smoke`로 리허설합니다 (모델마다 5 step, `<root>/<label>/smoke`).

## 5. 다시 돌릴 때

| 하고 싶은 것 | 방법 |
|---|---|
| 이어서 | 같은 명령 |
| 새 실험 | `workdir` 새 이름 |
| 데이터 구성을 바꿈 | `data.output_dir` 새 이름 |
| SFT까지만 | `--part sft` |
| 끝난 SFT에서 GRPO | `--part grpo` |
| 다른 실험의 SFT에서 GRPO | `--part grpo --sft-checkpoint <폴더>` (SFT 평가부터 다시) |
| GRPO 설정을 바꿔 다시 | `--from grpo` (앞 GRPO 점수도 표에 남음) |
| SFT부터 다시 | `--from sft` |
| 한 단계만 | `--only <단계>` (단계: `prepare` `eval_base` `sft` `eval_sft` `select` `grpo` `eval_grpo` `report`) |
| 명령만 보기 | `--dry-run` (경로 검사는 안 함) |
| 학습 없이 새 평가 세트로 다시 채점 | [eval.md](eval.md) |
| 생성기 코드가 바뀜 | 데이터셋을 새 이름으로 다시 만들고, `data`의 경로·`output_dir`·`workdir`을 새로. 옛 세트와 점수는 직접 비교하지 않음 |

## 6. 에러

| 에러 | 할 일 |
|---|---|
| `설정(…)의 경로를 확인하세요` | 메시지에 나온 칸을 `meta.json`이 있는 폴더의 절대 경로로 |
| `CUDA out of memory` | 40GB yaml로 (3절) |
| `Output already exists` / `already prepared` | `output_dir`을 새 이름으로 (지우지 말 것) |
| `training rows share a customer or document with the benchmark` | 평가용 데이터셋이 `train`에 들어감. 빼기 |
| `Reference answers do not score 1.0` | 데이터를 만든 코드와 지금 코드가 다름. 같은 코드로 데이터 다시 만들기 |
| `Server on port … exited` / `not ready in time` | 평가 서버(vLLM)가 못 뜸. `logs/<단계>-server0.log` 끝과 `nvidia-smi` 확인 |
| `Port … is already in use` | 예전 평가 서버를 끄거나 `eval.port_base` 변경 |
| 평가 중 `HTTP Error 400` (서버 로그 `At most 16 image(s)`) | 그림이 서버 한도(`--vllm_limit_mm_per_prompt`, 기본 16장)보다 많은 문항. 지금은 평가 전에 빼고 `<workdir>/benchmark_over_image_limit.jsonl`에 남깁니다 (로그 `WARNING: 평가 문항 N개는 …`) |
| `Prediction run settings or input changed` | 끊긴 평가의 답 파일이 지금 평가 문항과 다름 (예: 위처럼 문항이 빠짐). `predictions/<run>.jsonl`과 `.meta.json`을 다른 이름으로 옮기고 같은 명령 |
| `Multiple possible model types found` | `model_type`이 `qwen3_5`인지 |

로그는 `train/runs/exp1/logs/<단계>.log`에 있습니다.
