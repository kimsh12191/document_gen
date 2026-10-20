# 단계별 수동 실행

`run_pipeline.py`가 한 번에 하는 일을 한 단계씩 직접 실행하는 방법입니다. 보통은 [README](../README.md)의 한 번에 실행을 쓰면 됩니다. 아래 번호는 설치·준비([SETUP.md](SETUP.md) 1~4) 다음 단계입니다.

- 모든 명령은 프로젝트 폴더(저장소째 받았다면 `ocr/`)에서 실행합니다. `/share/...`와 `/실제/.../checkpoint-xxx`는 실제 경로로 바꿉니다. 준비 데이터는 `data/prepared-v2` 기준입니다.
- 평가 서버는 한 번에 하나만 실행합니다. 서버 터미널을 유지한 채 별도 터미널에서 추론·평가하고, 학습 전에는 서버 터미널에서 `Ctrl+C`로 종료하여 GPU를 확보합니다.

## 5. Base 모델 평가

로컬 Qwen3.5-9B를 배포할 때는 `--model_type qwen3_5`를 명시합니다. 자동 판별 시 `qwen3_5`와 `ovis_ocr2`가 함께 후보로 잡혀 `Multiple possible model types found` 오류가 발생할 수 있습니다. 아래 Base/SFT/GRPO 배포 명령에 동일하게 적용합니다.

학습 전 기준 성능을 저장합니다. `prepare`는 평가를 자동 실행하지 않습니다.

**세 모델은 같은 벤치마크·이미지·이미지 토큰 예산으로 평가하며 `--with-ocr`를 사용하지 않습니다.** 체크포인트 변경 시 새 `run-id`와 예측 파일을 사용하고 `.meta.json`도 보관합니다. 인증과 자세한 조건은 [DESIGN.md](DESIGN.md#평가-조건과-지표-해석)를 확인하세요.

```bash
# 학습과 같은 이미지 토큰 예산 (7·10단계 서버에도 같은 값을 씁니다)
IMG_TOKENS=$(python -m bank_ocr image-tokens --model /share/cv_share/qwen3.5/9b --data data/prepared-v2 \
  | python -c "import json,sys; print(json.load(sys.stdin)['image_max_token_num'])")

# 학습 전 Base 서버: adapter를 지정하지 않습니다.
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 IMAGE_MAX_TOKEN_NUM=$IMG_TOKENS CUDA_VISIBLE_DEVICES=0 \
swift deploy --model /share/cv_share/qwen3.5/9b --model_type qwen3_5 --infer_backend vllm \
  --vllm_max_model_len 10240 --vllm_max_num_seqs 4 \
  --vllm_gpu_memory_utilization 0.85 \
  --host 127.0.0.1 --port 8000 --served_model_name bank-ocr \
  --enable_thinking false --max_new_tokens 2048
```

별도 터미널에서:

```bash
python -m bank_ocr predict --config configs/inference.json --tasks data/prepared-v2/benchmark_tasks.jsonl \
  --endpoint http://127.0.0.1:8000/v1 --model bank-ocr --run-id base-vllm-v1 --concurrency 4 \
  --out predictions/base.jsonl

python -m bank_ocr evaluate --tasks data/prepared-v2/benchmark_tasks.jsonl \
  --predictions predictions/base.jsonl --label Base --out reports/base.json
```

**완료 기준:** `reports/base.json`이 생성되어 있습니다. Base 서버를 종료하고 SFT 학습을 시작합니다.

### 벤치마크 추론 속도 조절

아래 배포 예시는 vLLM 서버와 동시 요청 4개를 사용합니다. 이미지는 prepare에서 이미 `image_max_size`로 줄여 두었으므로 평가 이미지 예산은 학습과 같은 `$IMG_TOKENS`입니다. 입력+출력 컨텍스트 상한 10240은 이미지 토큰(2300×1600 기준 3600)과 spotting 출력(최대 2048)을 담을 수 있는 크기입니다. Base/SFT/GRPO 평가에 동일한 예산을 사용하세요.

vLLM은 Linux/CUDA 추론 환경에 `requirements-inference.in`으로 별도 준비합니다. 공식 Qwen3.5 문서는 `vllm>=0.17.0`을 안내하지만 학습용 Transformers 5.2와의 호환성 문제도 명시합니다. 학습 환경에 그대로 덮어 설치하지 말고 호환되는 PyTorch/Transformers/vLLM 조합을 별도 환경에서 확인하세요. 폐쇄망 설치 예시는 다음과 같습니다.

```bash
python -m pip install --no-index --find-links /share/wheelhouse -r requirements-inference.in
```

SFT/GRPO는 vision LoRA까지 적용하기 위해 `--merge_lora true`로 병합한 가중치를 배포합니다. 병합 모델 저장을 위한 디스크 공간과 시작 시 메모리가 추가로 필요합니다. 서버 실행은 Linux/A100에서 검증해야 합니다. OOM이면 먼저 클라이언트 `--concurrency 2`와 서버 `--vllm_max_num_seqs 2`를 사용하고, 필요하면 `--vllm_enforce_eager true`를 추가하세요. 이미지 예산을 낮추는 경우 세 모델 평가에 동일하게 적용하세요.

`predict`에 `--concurrency 4`를 추가하면 최대 4개 요청을 동시에 보냅니다. 기본값은 1이며, 추론 설정 JSON에 `"concurrency": 4`를 넣어도 됩니다. GPU 메모리를 확인하면서 2~4개부터 측정하세요. 서버가 순차 처리하면 속도 개선은 제한됩니다.

최근 16개 이미지의 Base64 인코딩을 캐시하고, 완료된 결과를 즉시 저장합니다. 출력 순서는 완료 순서이며 평가는 task ID로 연결합니다. 같은 출력 파일로 재실행하면 저장된 결과는 건너뜁니다. 동시 요청 수만 바꿔도 이어서 실행할 수 있습니다. 기존 predict 프로세스는 종료한 뒤 재실행하세요.

## 6. SFT 학습

`train.py`는 SFT/GRPO 모두 `model_type=qwen3_5`를 기본 적용합니다. 우선순위는 `--model-type` (또는 `--model_type`) > YAML의 `model_type` > 기본값입니다. `Multiple possible model types found` 오류가 발생한 서버에는 수정된 `train.py`와 `configs/sft.yaml`, `configs/grpo.yaml`을 반영하세요. 기존 `train.py`를 그대로 사용해야 한다면 학습 YAML에 `model_type: qwen3_5`를 추가하고, 지원하지 않는 CLI `--model_type`은 빼세요.

5 step smoke 학습으로 GPU 동작을 확인하고 별도 출력 폴더에서 본 학습을 실행합니다.

```bash
# 먼저 5 step 실제 GPU 동작 확인
python train.py sft --config configs/sft.yaml --gpus 0,1,2,3 --model /share/cv_share/qwen3.5/9b \
  --data data/prepared-v2 --output runs/sft-smoke --max-steps 5 --execute

# 이후 본 학습
python train.py sft --config configs/sft.yaml --gpus 0,1,2,3 --model /share/cv_share/qwen3.5/9b \
  --data data/prepared-v2 --output runs/sft --execute
```

`--execute`를 빼면 실행할 명령만 표시합니다. 제공한 설정 파일의 기본값은 BF16, LoRA rank 32·alpha 64, ViT·aligner·LLM 학습, A100 80GB 2장 기준 SFT는 GPU당 2 × 누적 2(업데이트당 8샘플), GRPO는 GPU당 4 × 누적 4, ZeRO-2, gradient checkpointing, 이미지 토큰은 `image_max_size`에 맞춰 자동 계산(2300×1600, 32px 기준 3600)입니다. SFT는 learning rate 1e-4, max_length 10240(묶음 학습 샘플이 이미지 3600토큰 + 질문·답 최대 4000자), GRPO는 learning rate 5e-6(LoRA 기준), beta 0.04, temperature 1.0입니다. GRPO의 `max_completion_length`는 spotting 출력을 담기 위해 1536입니다. 인터넷 모델 다운로드와 외부 실험 추적은 기본으로 비활성화합니다.

40GB에서의 실제 메모리 적합성은 내부망에서 확인해야 합니다. 이미지 3600토큰 + 출력으로 시퀀스가 길어져 이전 설정(2048/4096)보다 메모리를 더 씁니다. OOM이면 먼저 `--deepspeed zero3`를 쓰고, 그래도 안 되면 `image_max_size`를 줄여 prepare를 새 `output_dir`로 다시 실행하세요. `--image-tokens`만 낮추면 모델이 이미지를 다시 축소해 작은 글씨를 잃습니다. 이미지 토큰 수를 바꿨다면 Base/SFT/GRPO 평가에도 같은 값을 적용하고 실험 조건을 기록해야 합니다.

**완료 기준:** SFT adapter 체크포인트가 생성되어 있습니다. 다음 단계에 사용할 실제 `checkpoint-xxx` 경로를 기록합니다.

## 7. SFT 모델 평가

6단계의 SFT 학습을 마친 뒤, 실제 SFT 체크포인트 경로로 서버를 시작합니다. `runs/sft` 최상위 폴더가 아니라 생성된 adapter 체크포인트 폴더를 지정합니다.

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 IMAGE_MAX_TOKEN_NUM=$IMG_TOKENS CUDA_VISIBLE_DEVICES=0 \
swift deploy --model /share/cv_share/qwen3.5/9b --model_type qwen3_5 \
  --adapters /실제/SFT/checkpoint-xxx --merge_lora true --infer_backend vllm \
  --vllm_max_model_len 10240 --vllm_max_num_seqs 4 \
  --vllm_gpu_memory_utilization 0.85 \
  --host 127.0.0.1 --port 8000 --served_model_name bank-ocr \
  --enable_thinking false --max_new_tokens 2048
```

별도 터미널에서:

```bash
python -m bank_ocr predict --config configs/inference.json --tasks data/prepared-v2/benchmark_tasks.jsonl \
  --endpoint http://127.0.0.1:8000/v1 --model bank-ocr --run-id sft-vllm-v1 --concurrency 4 \
  --out predictions/sft.jsonl

python -m bank_ocr evaluate --tasks data/prepared-v2/benchmark_tasks.jsonl \
  --predictions predictions/sft.jsonl --label SFT --out reports/sft.json
```

**완료 기준:** `reports/sft.json`이 생성되어 있습니다. 다음 단계의 train 추론을 위해 SFT 서버를 유지합니다.

## 8. (선택) GRPO 학습 데이터 선정

**기본은 이 단계를 생략하고 9단계로 바로 진행합니다.** 9단계에서 `--grpo-dataset`을 생략하면 `data/prepared-v2/train_grpo.jsonl` 전체로 학습합니다.

mining은 다음 경우에만 고려합니다.

- `train_grpo.jsonl`이 `--count`보다 충분히 클 때. mining은 예제를 중복 복제하지 않으므로, 데이터가 `--count` 이하이면 전체 선택과 같고 train 추론 비용만 듭니다.
- 전체 데이터 GRPO에서 `log_completions` 기준으로 같은 프롬프트의 생성 4개가 같은 reward를 받는 비율이 높을 때. 이런 샘플은 advantage가 0이라 학습 신호가 없습니다.

reference label은 검수되지 않은 OCR이므로 SFT 실패 샘플에는 label 오류가 섞여 있을 수 있습니다. `--hard-fraction`을 높이면 label 오류 비율도 함께 올라가므로, 0.3~0.5부터 시작하고 선택된 실패 샘플 일부를 직접 확인합니다.

SFT adapter를 적용한 내부 서버로 **train_grpo.jsonl**을 먼저 추론한 뒤 mining합니다.

```bash
python -m bank_ocr predict --config configs/inference.json --tasks data/prepared-v2/train_grpo.jsonl \
  --endpoint http://127.0.0.1:8000/v1 --model bank-ocr --run-id sft-train-vllm-v1 --concurrency 4 --out predictions/sft-train.jsonl

python -m bank_ocr mine --tasks data/prepared-v2/train_grpo.jsonl \
  --predictions predictions/sft-train.jsonl --count 10000 --hard-fraction 0.5 \
  --out data/train_grpo_hard.jsonl
```

mining은 train만 허용하고 부족한 예제를 중복 복제하지 않습니다. `--hard-fraction` 비율만큼 실패 샘플을 우선 선택하고, 나머지는 남은 전체 pool에서 random으로 선택합니다.

**완료 기준:** 생략했거나, `data/train_grpo_hard.jsonl`이 준비되었습니다. SFT 서버를 종료한 뒤 학습을 시작합니다.

## 9. GRPO 학습

SFT 추론 서버를 종료하여 GPU를 확보한 다음 smoke test를 실행합니다. `--adapter`(단수형)에는 SFT 체크포인트 디렉터리를 지정합니다.

```bash
python train.py grpo --config configs/grpo.yaml --gpus 0,1,2,3 --model /share/cv_share/qwen3.5/9b \
  --adapter /실제/SFT/checkpoint-xxx --data data/prepared-v2 \
  --output runs/grpo-smoke --max-steps 5 --execute
```

GPU 확인 후 아래 명령으로 본 학습을 실행합니다.

```bash
python train.py grpo --config configs/grpo.yaml --gpus 0,1,2,3 --model /share/cv_share/qwen3.5/9b \
  --adapter /실제/SFT/checkpoint-xxx --data data/prepared-v2 \
  --output runs/grpo --execute
```

8단계에서 mining을 했다면 두 명령 모두에 `--grpo-dataset data/train_grpo_hard.jsonl`을 추가합니다.

`train.py`는 위 옵션 외의 인자(예: `--infer_backend`, `--adapters`)를 MS-SWIFT로 전달하지 않고 오류로 처리합니다. 그 외 MS-SWIFT 옵션은 `configs/grpo.yaml`에서 변경합니다. rollout 생성 backend는 `use_vllm`으로 정하며, `false`이면 transformers로 생성합니다.

GRPO는 SFT adapter와 ref_adapter에서 시작합니다. `configs/grpo.yaml`의 초기 설정은 `num_generations=4`(2장용 `grpo_a100x2.yaml`은 8), `use_vllm=false`이며 변경할 수 있습니다. 처음에는 vLLM rollout 엔진의 추가 메모리와 vision LoRA 동기화 변수를 줄이는 설정입니다. 속도는 이후 측정·개선 대상입니다.

**완료 기준:** GRPO adapter 체크포인트가 생성되어 있습니다. 다음 단계에 사용할 실제 경로를 기록합니다.

## 10. GRPO 모델 평가

GRPO 학습이 끝나면 실제 GRPO adapter 체크포인트로 서버를 시작합니다. **GRPO model은 SFT에서 GRPO를 이어 학습한 모델**입니다. 아래 경로에 SFT 체크포인트를 다시 지정하지 않도록 확인하세요.

```bash
HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 IMAGE_MAX_TOKEN_NUM=$IMG_TOKENS CUDA_VISIBLE_DEVICES=0 \
swift deploy --model /share/cv_share/qwen3.5/9b --model_type qwen3_5 \
  --adapters /실제/GRPO/checkpoint-xxx --merge_lora true --infer_backend vllm \
  --vllm_max_model_len 10240 --vllm_max_num_seqs 4 \
  --vllm_gpu_memory_utilization 0.85 \
  --host 127.0.0.1 --port 8000 --served_model_name bank-ocr \
  --enable_thinking false --max_new_tokens 2048
```

별도 터미널에서:

```bash
python -m bank_ocr predict --config configs/inference.json --tasks data/prepared-v2/benchmark_tasks.jsonl \
  --endpoint http://127.0.0.1:8000/v1 --model bank-ocr --run-id grpo-vllm-v1 --concurrency 4 \
  --out predictions/grpo.jsonl

python -m bank_ocr evaluate --tasks data/prepared-v2/benchmark_tasks.jsonl \
  --predictions predictions/grpo.jsonl --label GRPO --out reports/grpo.json
```

**완료 기준:** `reports/grpo.json`이 생성되어 있습니다. 평가 후 서버를 종료할 수 있습니다.

## 11. 최종 비교표 생성

프로젝트 폴더에 `benchmark_report.py`가 있는지 확인하고 실행합니다.

```bash
python benchmark_report.py \
  --base reports/base.json \
  --sft reports/sft.json \
  --grpo reports/grpo.json \
  --out reports/benchmark.csv
```

각 인수에는 `evaluate`가 만든 **평가 JSON**을 지정합니다. `predictions/*.jsonl`이나 체크포인트 폴더를 넣는 것이 아닙니다. 아직 세 평가 결과가 모두 없다면 나머지 평가를 완료한 뒤 실행합니다.

출력 표는 다음 구조입니다. 아래는 형식 안내이며 실제 성능 수치는 평가 결과에서 채웁니다.

| Model | Crop CER ↓ | BBox→Text EM ↑ | Numeric EM ↑ | Region CER ↓ | Grounding F1@0.5 ↑ | Grounding 없음 정확도 ↑ | Spotting 위치 F1@0.5 ↑ | Spotting 위치+글자 F1 ↑ | Relation 위치+글자 F1 ↑ | 그린 박스→글자 EM ↑ | 그린 박스→좌표 F1@0.75 ↑ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Base model | 평가 결과 | … | | | | | | | | | |
| SFT model | 평가 결과 | … | | | | | | | | | |
| GRPO model | 평가 결과 | … | | | | | | | | | |

같은 표가 전체, Base 대비 변화량, clean 이미지, aug(노이즈·기하 증강) 이미지 기준으로 네 번 나옵니다.

| 결과 파일 | 내용 |
|---|---|
| `reports/benchmark.html` | 브라우저에서 열어 보는 성능표·Base 대비 변화량·평가 조건. 인터넷 연결 불필요 |
| `reports/benchmark.md` | 문서에 붙이거나 버전 관리할 동일 비교표 |
| `reports/benchmark.csv` | 모델별 점수와 변화량 컬럼을 담은 엑셀용 파일 |

**완료 기준:** CSV·Markdown·HTML 비교표가 생성되어 있습니다. HTML을 열어 결과를 확인합니다.

## 부록 A. GRPO 보상과 rollout 진단

보상 정의는 [DESIGN.md](DESIGN.md#grpo-보상)에 있습니다. 학습 중 내부 OCR을 다시 호출하지 않으며, 보상은 교사 OCR 오류도 따라갈 수 있습니다. 8단계 `mine`은 같은 보상이 `--hard-threshold`(기본 0.9)보다 낮은 train 행을 어려운 문제로 고릅니다.

동일 응답으로 GRPO 신호가 사라지는지 확인하려면 rollout 로그를 아래 형식으로 정리해 사용합니다. SWIFT 버전별 원본 로그 자동 변환은 포함하지 않습니다.

```json
{"id":"train_grpo.jsonl에 있는 id","completions":["응답1","응답2","응답3","응답4"]}
```

```bash
python -m bank_ocr rollout-stats --tasks data/prepared-v2/train_grpo.jsonl \
  --rollouts data/rollouts.jsonl --out reports/rollout-stats.json
```

## 부록 B. 로컬 검사·검증 범위·제약

```bash
python -m unittest discover -s tests -v
python demo.py --out demo-run
```

demo는 합성 이미지와 가짜 OCR을 사용하는 연결 검사입니다. 출력에 `SYNTHETIC_ONLY_NO_MODEL_WAS_RUN`을 명시하며 모델 성능을 측정하지 않습니다.

독립 보고 스크립트는 합성 평가 JSON으로 7개 검사를 통과했습니다: 3개 모델 행·변화량 계산, 벤치마크 불일치, 교사 정보 제공 모드, 평가 건수 불일치, 생성 조건 불일치, 프로젝트 외부 독립 실행, 메타데이터 누락·HTML 문자 처리. 실제 모델 성능을 검증한 것은 아닙니다.

이 버전은 다각형의 축 정렬 외접 사각형을 사용하고, 읽는 순서는 박스 위치로 정합니다. 기울어진 개별 글상자 정방향 복원, 템플릿 기반 분리, 병렬 OCR 호출·자동 재시도, 정밀 레이아웃 검증은 포함하지 않습니다. 자동 좌표 검사·통계는 사람 검수와 별개이며 요청대로 사람 검수 단계는 없습니다.

### 포함된 기능

- 기존 `ocr_from_file(image_path)` 함수 연결. 서버 주소나 인증 방식을 임의로 만들지 않습니다.
- 실제 화면의 `success → data.basicData → bounding.vertices` 구조 및 중첩 배열 처리.
- EXIF 방향 보정 후 원본으로 OCR, 모델 입력은 `image_max_size`로 축소한 clean view와 노이즈·기하 증강 view. 박스는 모든 기하 변환을 따라갑니다.
- OCR 원본 캐시, 재실행 시 성공한 호출 재사용, OCR 버전 변경 시 캐시 분리.
- 문서 단위 train/val/benchmark 분리, 분리 사이 동일 디코딩 이미지 검사.
- crop_ocr / bbox_ocr / grounding(반복·부정 포함) / region_ocr / spotting / relation / marked_ocr·marked_box(그린 박스) 생성. 정답이 불완전한 영역은 제외.
- `task_mix` SFT 비율, GRPO의 문자·숫자 유사도와 박스 soft F1 보상.
- 내부 모델 API 추론, 평가 보고서, train 실패 샘플 추출.
- Base / SFT / GRPO 비교표와 Base 대비 변화량: 독립 스크립트로 CSV·Markdown·HTML 생성.
- GRPO rollout별 보상 표준편차와 동일 응답 비율을 확인하는 도구.

## 부록 C. 공식 참고 문서

- [Qwen3.5 / MS-SWIFT v4.0](https://swift.readthedocs.io/en/v4.0/BestPractices/Qwen3_5-Best-Practice.html)
- [MS-SWIFT reward plugin](https://swift.readthedocs.io/en/latest/Instruction/GRPO/DeveloperGuide/reward_function.html)
- [Inference and deployment](https://swift.readthedocs.io/en/latest/Instruction/Inference-and-deployment.html)
- [사용자 정의 추가 컬럼 보존](https://swift.readthedocs.io/en/latest/Instruction/Frequently-asked-questions.html)

외부 문서 확인은 공개 라이브러리 인터페이스에만 사용했으며, 은행 이미지나 OCR 내용을 외부 모델 API로 보내지 않았습니다.
