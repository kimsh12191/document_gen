# 은행 업무 단계: OCR 모델 → SFT → GRPO → 벤치마크 비교

OCR 단계(`run_pipeline.py`)에서 학습한 모델을 출발점으로 **은행 업무**를 학습합니다. 학습 데이터와 평가 세트는 docgen(합성 은행 서류 생성기)으로 만들고, 평가 세트 채점에는 docgen 벤치마크의 채점기를 그대로 씁니다.

| 영역 | 과제 | 내용 |
|---|---|---|
| OCR | `ocr_field`, `ocr_page` | 값 칸 하나 읽기, 서류 전체 받아쓰기 |
| 문서 이해 | `classify`, `kie`, `marks` | 서류 분류, 항목 값 추출, 체크박스·도장·서명 |
| 은행 업무 | `doc_check` | 제출 서류 첫 쪽들을 보고 빠진 서류·불필요 서류·타인 서류 찾기 |
| 은행 업무 | `cross_check` | 서류 2~3건을 대조해 불일치 찾기 (오기, 타인 서류, 금액·날짜 관계, 임대인≠소유자 등 14종) |
| 은행 업무 | `review` | 심사 질문 (LTV, 소득 대비 배수, 서류 유효기간, 만 나이 등)에 숫자·예/아니오로 답하기 |

과제와 채점 방식은 docgen의 `docs/BENCHMARK.md`에 있습니다.

## 전체 흐름

```text
[docgen 컨테이너, 한 번만]  학습 데이터 생성 (--split train) + 평가 세트 생성
[GPU 서버, 한 명령]         prepare → 출발 모델 평가 → SFT → SFT 평가 → GRPO 문제 선정 → GRPO → GRPO 평가 → 비교표
```

데이터 생성은 한 번 해 두면 다시 할 필요가 없어서 파이프라인에 넣지 않았습니다. 파이프라인의 `prepare`는 만들어 둔 폴더를 읽고 검사만 합니다.

- 학습 폴더에 평가 세트를 넣었거나, 평가 세트와 같은 고객이 섞여 있으면 멈춥니다.
- 정답을 모델 출력 형식으로 쓴 답이 만점이 나오는지 확인합니다. docgen 코드와 데이터 버전이 어긋나면 여기서 걸립니다.

## 1. 데이터 만들기 (docgen 컨테이너, 한 번)

docgen 코드 1.2 이상이 필요합니다(`--split train`).

```bash
# 학습: 서류 476종 × 2건 + 업무 12종 × 고객 100명. 약 30분(--workers 8), 약 9GB
nohup python -m docgen.bench build --split train --out /out/bank_train \
    --per-doc 2 --bundles 100 --workers 8 > /out/bank_train.log 2>&1 &

# 평가: 서류 476종 × 1건 + 업무 12종 × 고객 20명. 약 10분, 약 2GB
nohup python -m docgen.bench build --out /out/bench --bundles 20 --workers 8 > /out/bench.log 2>&1 &
```

- **`--per-doc 2`:** 서류 한 장짜리 과제(분류, 추출, 체크·도장·서명, OCR)도 학습합니다. OCR 단계에서는 추출을 배우지 않았으므로 넣는 것을 권합니다.
- **`--bundles 20`:** 평가 세트의 은행 업무 문항을 늘립니다. 기본값 4로는 일부 불일치 사례가 1~4문항뿐이라 점수 오차가 큽니다.

## 2. GPU 서버 준비

- **docgen 코드:** 이 폴더(`training/`)의 상위 폴더가 docgen 코드입니다. 채점과 GRPO 보상에 쓰며, 파이썬 표준 라이브러리만 씁니다(설치 불필요). 설정의 `data.docgen_root`는 기본값 `../..`(configs 기준 저장소 최상위) 그대로 두면 됩니다.
- **데이터:** 1단계에서 만든 `bank_train`, `bench` 폴더를 GPU 서버에서 읽을 수 있어야 합니다. 같은 서버라면 `~/docgen/data/...`를 그대로 씁니다.
- **이 프로젝트 업데이트:** 새 파일을 덮어쓴 뒤 `pip install --no-index --no-build-isolation -e .`를 한 번 실행합니다(`bank_task` 패키지 등록).
- **출발 모델:** OCR 단계 결과의 병합 모델 폴더입니다. 예: `runs/exp1/merged/grpo-v1-…-checkpoint-500`. 폴더 안에 `config.json`이 있어야 합니다.

## 3. 설정

```bash
cp configs/bank_pipeline.example.json configs/bank_pipeline.json
```

| 키 | 뜻 |
|---|---|
| `model` | 출발 모델 (OCR 단계의 병합 모델 폴더) |
| `gpus` | 사용할 GPU. 평가 때는 GPU마다 서버 하나, 학습 때는 전부 사용 |
| `data.docgen_root` | `docgen/`이 들어 있는 폴더. 기본 `../..` = 이 저장소 최상위 |
| `data.train` | docgen 학습 폴더 목록 (`--split train` 결과). `docgen generate --png` 결과 폴더도 넣을 수 있습니다(과제 이름 앞에 `gen_`) |
| `data.benchmark` | docgen 평가 세트 폴더 |
| `data.replay` | 앞 단계 OCR 학습 데이터 일부를 섞어 OCR 능력이 떨어지지 않게 함. `{"path": ".../prepared-v2/train_sft.jsonl", "count": 3000}` |
| `data.output_dir` | 변환된 데이터 폴더 |
| `data.sft_max_examples` | SFT 문항 수 상한 (기본 20000). 학습 시간에 거의 비례 |
| `data.task_mix` | 과제별 비율. 목록에 없는 과제는 빠짐. 모자라는 과제의 몫은 다른 과제가 채움 |
| `data.max_image_tokens_per_sample` | 한 문항의 이미지 토큰 합 상한 (기본 12000) |
| `data.sft_max_length` | `bank_sft.yaml`의 `max_length`와 같은 값. 이보다 긴 문항은 버림 |
| `data.grpo_holdout` | GRPO용으로 SFT에서 빼 두는 고객 비율 (기본 0.2) |
| `grpo.tasks`, `grpo.max_images` | GRPO에 쓸 과제와 문항당 최대 이미지 수 (기본 4) |
| `grpo.count`, `grpo.candidates` | GRPO 문제 수 (기본 1000), 그중 어려운 문제를 고를 후보 수 (기본 3000) |
| `eval.compare_models` | 같이 평가할 모델. 예: `[{"label": "Qwen3.5-9B 원본", "model": "/share/cv_share/qwen3.5/9b"}]` |
| `ocr_check` | 각 모델로 OCR 벤치마크 일부를 같이 풀어 OCR 능력 유지 여부를 봄. `{"tasks": ".../prepared-v2/benchmark_tasks.jsonl", "rows": 1000}`. 안 쓰려면 `null` |

설정 파일의 상대 경로는 설정 파일 위치 기준입니다.

## 4. 실행

```bash
# 리허설: 학습 5 step, 과제마다 8문항 평가, GRPO 8문제. 명령·메모리·서버 기동 확인 (runs/bank1/smoke)
python run_bank_pipeline.py --config configs/bank_pipeline.json --smoke

# 본 실행
nohup python run_bank_pipeline.py --config configs/bank_pipeline.json > bank_pipeline.log 2>&1 &
```

옵션은 `run_pipeline.py`와 같습니다: `--from sft`, `--from grpo`(GRPO만 다시, 비교표에 줄이 추가됨), `--only report`, `--dry-run`.

**결과**

| 파일 | 내용 |
|---|---|
| `reports/benchmark.html` (`.md`, `.csv`) | 모델별 과제 점수, 출발 모델 대비 변화(%p), 불일치 분류별·심사 능력별·서식별 점수 |
| `reports/ocr_retention.html` | `ocr_check`를 켰을 때: OCR 벤치마크 일부에서 출발 모델 대비 OCR 점수 변화 |
| `state.json` | 단계별 완료 여부와 소요 시간 |

## 단계별 내용

### prepare

- **이미지 크기:** 한 장은 OCR 단계와 같은 상한(`image_max_size` 2300×1600, 32px 기준 3600토큰)입니다. 한 문항에 이미지가 여러 장이면(최대 13장) 합이 `max_image_tokens_per_sample`을 넘지 않게 장마다 같은 비율로 줄입니다. 예: 12000 / 13장 → 장당 약 920토큰.
- **평가도 같은 규칙:** 평가 세트도 같은 규칙으로 줄여서, 학습과 평가가 같은 픽셀을 봅니다.
- **묶음 학습:** 같은 이미지에 대한 질문(분류·추출·체크 등)은 대화 하나로 묶어 이미지를 한 번만 처리합니다.
- **GRPO용 고객:** 고객 20%(`grpo_holdout`)의 문항은 SFT에서 빼고 GRPO용으로 둡니다. SFT에서 이미 본 문항으로 GRPO를 하면 학습 신호가 약하기 때문입니다.

### SFT

출발 모델에 새 LoRA(rank 32)를 붙여 1 epoch 학습합니다(`configs/bank_sft.yaml`). 설정은 80GB 2장 기준이며, GPU당 1문항 × 누적 4로 업데이트당 8문항입니다. 문항이 길어서(이미지 최대 12000토큰) GPU당 1문항입니다.

### GRPO

SFT 체크포인트에서 이어 학습합니다. **보상은 평가 세트 채점기 그대로**(`bank_task/score.py`)이고, 정답이 분명해서 OCR 단계의 의사정답보다 신호가 깨끗합니다. 전부 맞거나 전부 틀리기 쉬운 과제는 부분 점수를 줍니다.

| 과제 | 보상 |
|---|---|
| `cross_check` 정상 문항 | "문제없음"이라고 하면 1 |
| `cross_check` 변조 문항 | 0.5 × (불일치라고 함) + 0.5 × (맞는 서류와 값·항목까지 짚음) |
| `doc_check` | 0.5 × 완전 일치 + 0.5 × F1 |
| `review` | 정답이면 1 (숫자는 질문에 적힌 허용 오차 안) |
| `kie` | 항목 F1 |
| 출력 형식 오류 | 0 |

**문제 선정:** SFT 평가 때 띄운 서버로 후보 3000개를 먼저 풀고, 보상 0.9 미만인 문제를 절반 섞어 1000개를 고릅니다(`grpo.select: mine`). 이미지가 많은 문항은 GRPO 메모리를 크게 쓰므로 `grpo.max_images`(기본 4) 이하만 씁니다. 그래서 `doc_check`(4~13장)는 일부만 들어갑니다.

**GPU별 설정:**
- 80GB 2장: `configs/bank_grpo_a100x2.yaml` (GPU당 4개 × 2장 = 생성 8개)
- 40GB 2장: `pipeline.json`의 `grpo.config`를 `bank_grpo_a100_40g_x2.yaml`(생성 4개)로 바꾸세요.

### 평가

GPU마다 vLLM 서버를 띄우고 나눠 보냅니다. 한 문항에 이미지가 최대 13장이라 서버에 `--vllm_limit_mm_per_prompt {"image": 16}`, `--vllm_max_model_len 20480`을 줍니다. 설치된 ms-swift에서 옵션 이름이 다르면 `eval.deploy_command`로 바꾸세요. 리허설(`--smoke`)이 이 명령을 한 번 실행해 봅니다.

## 예상 시간 (A100 80GB × 2, 추정)

실제 값은 리허설과 `state.json`의 `timings`로 확인하세요.

| 단계 | 규모 | 예상 |
|---|---|---|
| prepare | 이미지 줄이기 (CPU 병렬) | 10~30분 |
| 평가 (모델마다) | 약 6~7천 문항 (짧은 OCR 문항이 절반) + OCR 1000문항, 서버 2대 | 30~60분 (+ 병합·서버 기동 10~20분) |
| SFT | 2만 문항 (+ OCR 3000), 문항당 이미지 3600~12000토큰 | 10~15시간 |
| GRPO | 1000문제 × 생성 8개 = 250 step | step 1~3분이면 4~12시간 |
| 합계 | | 약 1~1.5일 |

시간이 부족하면 `data.sft_max_examples`(예: 10000), `grpo.count`(예: 500)를 먼저 줄이세요. 둘 다 학습 시간에 거의 비례합니다. `data.sft_max_examples`를 바꾸면 `data.output_dir`도 새 이름으로 바꿔야 prepare가 다시 실행됩니다.

## 해석할 때 주의

- **합성 서류입니다.** 학습 데이터와 평가 세트는 고객만 다르고, 질문 문장·서식·변조 방식이 같습니다. 은행 업무 점수가 크게 오르는 것은 당연하며, 그 점수는 "이 생성기의 업무 형식을 익혔다"는 뜻입니다. 실제 서류 묶음으로 따로 확인하세요.
- **출발 모델은 이 과제를 배운 적이 없습니다.** 출발 모델의 낮은 점수에는 답 형식(JSON 키 등)을 모르는 몫도 들어 있습니다. 보고서의 "파싱 실패" 비율을 함께 보세요.
- **OCR 능력 유지:** `ocr_retention` 표에서 OCR 점수가 많이 떨어졌다면 `data.replay.count`를 늘리세요.
- **`cross_check`:** "문제없음"만 답해도 정상 문항(절반 이상)은 맞습니다. 종합 점수와 함께 탐지·오탐률을 보세요.
