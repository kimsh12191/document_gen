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
| `Multiple possible model types found` | `model_type`이 `qwen3_5`인지 |

로그는 `train/runs/exp1/logs/<단계>.log`에 있습니다.
