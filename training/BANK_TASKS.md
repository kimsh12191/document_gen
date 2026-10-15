# 은행 업무 단계: OCR 모델 → SFT → GRPO → 벤치마크 비교

OCR 단계(`run_pipeline.py`)에서 학습한 모델을 출발점으로 **은행 업무**를 학습합니다. 학습 데이터와 평가 세트는 docgen(합성 은행 서류 생성기)으로 만들고, 평가 세트 채점에는 docgen 벤치마크의 채점기를 그대로 씁니다.

| 영역 | 과제 | 내용 |
|---|---|---|
| OCR | `ocr_field`, `ocr_page` | 값 칸 하나 읽기, 서류 전체 받아쓰기 |
| 문서 이해 | `classify`, `kie`, `marks` | 서류 분류, 항목 값 추출, 체크박스·도장·서명 |
| 은행 업무 | `doc_check` | 제출 서류 첫 쪽들을 보고 빠진 서류·불필요 서류·타인 서류 찾기 |
| 은행 업무 | `cross_check` | 서류 2~3건을 대조해 불일치 찾기 (오기, 타인 서류, 금액·날짜 관계, 임대인≠소유자 등 14종) |
| 은행 업무 | `review` | 심사 질문 (LTV, 소득 대비 배수, 서류 유효기간, 만 나이 등)에 숫자·예/아니오로 답하기 |

과제와 채점 방식은 [guide/benchmark.md](../guide/benchmark.md), 학습한 모델에게 묻는 질문 문장과 답 형식은 [guide/questions.md](../guide/questions.md)에 있습니다.

## 전체 흐름

```text
[docgen 도커, 한 번만]      학습 데이터 생성 (--split train) + 평가 세트 생성       ← 1단계, 파이프라인 밖
[GPU 서버, 한 명령]         prepare → 출발 모델 평가 → SFT → SFT 평가 → GRPO 문제 선정 → GRPO → GRPO 평가 → 비교표
```

데이터 생성은 한 번 해 두면 다시 할 필요가 없어서 파이프라인에 넣지 않았습니다. 파이프라인의 `prepare`는 만들어 둔 폴더를 읽고 검사만 합니다.

- 학습 폴더에 평가 세트를 넣었거나, 평가 세트와 같은 고객이 섞여 있으면 멈춥니다.
- 정답을 모델 출력 형식으로 쓴 답이 만점이 나오는지 확인합니다. docgen 코드와 데이터 버전이 어긋나면 여기서 걸립니다.

## 1. 데이터 만들기 (docgen 도커, 한 번)

데이터 생성은 이 파이프라인에 들어 있지 않습니다. Chromium·한글 글꼴이 든 docgen 도커 이미지에서 따로 한 번 만들어 둡니다(설치는 [docs/DOCKER.md](../docs/DOCKER.md)). 만들어 두면 학습을 몇 번 다시 하든 다시 만들 필요가 없습니다.

docgen 코드 1.2 이상이 필요합니다(`--split train`). 평가 세트를 1.2 이전 코드로 만들었다면 다시 만드세요(증강 노이즈가 이미지마다 고정되도록 바뀜).

### 실행: `scripts/make_bank_data.sh`

docgen 컨테이너에 SSH로 접속해 한 줄로 실행합니다. 평가 세트(`bench`)를 먼저, 학습 데이터(`bank_train`)를 다음에 만듭니다.

```bash
ssh -p 2222 docgen@<서버IP>
bash scripts/make_bank_data.sh           # 백그라운드로 시작, SSH 를 끊어도 계속
tail -f /out/logs/make_bank_data.log     # 진행 보기. "전부 완료" 와 과제별 문항 수가 나오면 끝
```

| 폴더 | 내용 | 시간·용량 (8코어) |
|---|---|---|
| `bench` | 평가: 서류 476종 × 1건 + 업무 12종 × 고객 40명 | 약 15분, 약 3GB |
| `bank_train` | 학습: 서류 476종 × 5건 + 업무 12종 × 고객 200명 (`--split train`) | 약 1시간, 약 16GB |

**스크립트가 하는 일**
- 다 만든 폴더(`meta.json` 있음)는 건너뛰고, 중간에 멈춘 폴더는 다시 만듭니다.
- 디스크가 모자라거나 docgen 코드에 `--split train`이 없으면 시작하지 않습니다.
- 평가 세트가 1.0 버전이면 다시 만들라고 알려 줍니다.
- 단계별 로그를 `/out/logs/`에 남깁니다.

**설정(환경변수, 명령 앞에 붙임)**

| 변수 | 기본 | 뜻 |
|---|---|---|
| `TRAIN_BUNDLES` | 200 | 학습: 업무 12종마다 고객 수 |
| `TRAIN_PER_DOC` | 5 | 학습: 서류 476종마다 건수 (분류·추출·체크·OCR 과제) |
| `BENCH_BUNDLES` | 40 | 평가: 업무 12종마다 고객 수 |
| `WORKERS` | 코어 수 (최대 8) | 동시 렌더링 프로세스 |
| `OUT` | `/out` | 만들 위치 |
| `TYPES`, `SCENARIOS` | all | 시험용으로 서류·업무 줄이기 |

```bash
TRAIN_BUNDLES=300 BENCH_BUNDLES=60 bash scripts/make_bank_data.sh          # 양 바꾸기
OUT=/out/try TYPES=resident_id_card,loan_application SCENARIOS=mortgage \
  TRAIN_PER_DOC=1 TRAIN_BUNDLES=2 BENCH_BUNDLES=1 bash scripts/make_bank_data.sh --fg   # 1분짜리 시험
```

SSH 없이 서버 터미널에서 바로 돌리려면 다음 명령을 씁니다. 컨테이너 쪽 작업 폴더가 코드 폴더가 아니어서 전체 경로를 씁니다.

```bash
docker exec -u docgen docgen bash -lc 'bash ~/document_gen/scripts/make_bank_data.sh'
```

### 양은 얼마나

- **학습 (고객 200명, 서류당 5건 권장):** SFT는 최대 2만 문항(`data.sft_max_examples`)을 과제 비율(`data.task_mix`)대로 뽑습니다. 학습 데이터는 그보다 넉넉해야 비율대로 뽑힙니다.
  - 고객 100명·서류당 2건이면, GRPO용 20%를 빼고 서류 구비 확인 약 960, 정보 추출 약 760(서식 1종당 1.6건), 서류 대조 약 3900문항이라 비율에 모자랍니다.
  - 생성은 학습보다 훨씬 싸니 넉넉히 만드세요.
- **평가 (고객 40명):** 서류 구비 확인 480, 서류 대조 약 2000(변조 약 730), 심사 질의 약 2400문항입니다.
  - 480문항이면 95% 신뢰구간이 약 ±4.5%p, 2000문항이면 약 ±2%p입니다.
  - 불일치 사례별로 나눠 봐도 드문 사례(임대인≠소유자, 송금 수취인 등)가 10문항 안팎은 됩니다.
  - 20명으로 줄이면 평가가 빨라지지만, 드문 사례가 5문항 안팎이라 사례별 점수가 많이 흔들립니다.
- **학습과 평가는 겹치지 않습니다.** `--split train`은 평가 세트와 다른 고객으로 만들고, prepare가 한 번 더 검사합니다.

### 경로: 컨테이너 안 ↔ 서버

컨테이너의 `/out`은 서버의 `~/docgen/data`입니다(`docker run -v ~/docgen/data:/out`). **파이프라인 설정에는 서버 경로를 씁니다.**

| 컨테이너 안 | 서버 (파이프라인 설정) |
|---|---|
| `/out/bank_train` | `~/docgen/data/bank_train` → `data.train` |
| `/out/bench` | `~/docgen/data/bench` → `data.benchmark` |
| `/home/docgen/document_gen` | `~/docgen/document_gen` → `data.docgen_root` |

설정 파일에는 `~` 대신 절대 경로(`/home/<계정>/docgen/data/bank_train`)를 쓰세요.

## 2. GPU 서버 준비

- **docgen 코드:** 채점과 GRPO 보상에 docgen 코드를 씁니다(파이썬 표준 라이브러리만, 설치 불필요). 이 폴더(`training/`)를 저장소째(`document_gen/training/`) 쓰면 설정의 `data.docgen_root` 기본값 `../..`(configs 기준 저장소 최상위) 그대로 됩니다. 예전 `bank-ocr-pipeline` 폴더에서 돌린다면 `data.docgen_root`를 docgen 코드 폴더(예: `/home/<계정>/docgen/document_gen`)로 지정하세요.
- **학습 폴더 위치:** docgen 컨테이너에 마운트한 코드 폴더(`~/docgen/document_gen`)는 컨테이너가 시작할 때 컨테이너의 `docgen` 계정(UID 1000)이 쓸 수 없으면 그 계정 소유로 바뀝니다. 서버 계정이 UID 1000이 아니면, 학습은 그 폴더가 아니라 따로 둔 폴더(기존 `bank-ocr-pipeline` 폴더, 또는 코드 묶음을 따로 푼 곳)에서 돌리세요. 학습 결과(`runs/`, `data/`)를 그 폴더에 쓰기 때문입니다.
- **데이터:** 1단계에서 만든 `bank_train`, `bench` 폴더를 GPU 서버에서 읽을 수 있어야 합니다. 도커와 같은 서버라면 위 경로 표의 서버 경로를 그대로 씁니다.
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

### 눈으로 확인: viewer

모델들의 답을 문항별로 정답과 나란히 보고, 내 서류 파일을 올려 직접 물어볼 수 있습니다. 사용법은 [viewer/README.md](viewer/README.md) 6번에 있습니다.

```bash
bash viewer/bank_start.sh                                              # 저장된 답 보기 (GPU 불필요)
bash viewer/bank_start.sh runs/bank1/merged/sft-<버전>-checkpoint-<번호> 1   # + 다시 풀기·직접 테스트
# 브라우저: http://localhost:7861 (VS Code PORTS 탭에서 7861 포워딩)
```

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

**GPU별 설정:** `bank_pipeline.json`의 `sft.config`, `grpo.config`를 GPU에 맞게 고릅니다.

| GPU | `sft.config` | `grpo.config` |
|---|---|---|
| A100 80GB × 2 | `bank_sft.yaml` | `bank_grpo_a100x2.yaml` (한 문제에 답 8개) |
| A100 40GB × 2 | `bank_sft_a100_40g_x2.yaml` | `bank_grpo_a100_40g_x2.yaml` (답 4개) |

40GB 설정은 메모리를 줄이려고 두 가지를 바꿉니다.
- **비전 인코더를 학습하지 않습니다(`freeze_vit`).** 비전 인코더는 OCR 단계에서 이미 학습했습니다.
- **SFT는 `deepspeed zero3`를 씁니다.** 모델 가중치를 두 GPU에 나눠 올립니다. 대신 조금 느립니다.

그래도 메모리가 부족하면 아래 순서로 줄입니다.
1. **SFT:** `data.max_image_tokens_per_sample`을 8000으로, `data.sft_max_length`와 yaml의 `max_length`를 12288로 낮춥니다. `data.output_dir`을 새 이름으로 바꿔 처음부터 다시 실행합니다(prepare가 이미지를 다시 줄임). 이미지가 작아지는 만큼 평가도 같은 크기로 다시 합니다.
2. **GRPO:** `grpo.max_images`를 2로 낮추고 `--from select`로 다시 실행합니다.

### 평가

GPU마다 vLLM 서버를 띄우고 나눠 보냅니다. 한 문항에 이미지가 최대 13장이라 서버에 `--vllm_limit_mm_per_prompt {"image": 16}`, `--vllm_max_model_len 20480`을 줍니다. 설치된 ms-swift에서 옵션 이름이 다르면 `eval.deploy_command`로 바꾸세요. 리허설(`--smoke`)이 이 명령을 한 번 실행해 봅니다.

## 예상 시간 (A100 80GB × 2, 추정)

실제 값은 리허설과 `state.json`의 `timings`로 확인하세요.

| 단계 | 규모 | 예상 |
|---|---|---|
| prepare | 이미지 줄이기 (CPU 병렬) | 10~30분 |
| 평가 (모델마다) | 약 9천 문항 (짧은 값 칸 OCR 문항 약 2400 포함) + OCR 1000문항, 서버 2대 | 40~80분 (+ 병합·서버 기동 10~20분) |
| SFT | 2만 문항 (+ OCR 3000), 문항당 이미지 3600~12000토큰 | 10~15시간 |
| GRPO | 1000문제 × 생성 8개 = 250 step | step 1~3분이면 4~12시간 |
| 합계 | | 약 1~1.5일 |

시간이 부족하면 `data.sft_max_examples`(예: 10000), `grpo.count`(예: 500)를 먼저 줄이세요. 둘 다 학습 시간에 거의 비례합니다. `data.sft_max_examples`를 바꾸면 `data.output_dir`도 새 이름으로 바꿔야 prepare가 다시 실행됩니다.

## 해석할 때 주의

점수표·학습 로그 읽는 법 전체는 [guide/results.md](../guide/results.md)에 있습니다.


- **합성 서류입니다.** 학습 데이터와 평가 세트는 고객만 다르고, 질문 문장·서식·변조 방식이 같습니다. 은행 업무 점수가 크게 오르는 것은 당연하며, 그 점수는 "이 생성기의 업무 형식을 익혔다"는 뜻입니다. 실제 서류 묶음으로 따로 확인하세요.
- **출발 모델은 이 과제를 배운 적이 없습니다.** 출발 모델의 낮은 점수에는 답 형식(JSON 키 등)을 모르는 몫도 들어 있습니다. 보고서의 "파싱 실패" 비율을 함께 보세요.
- **OCR 능력 유지:** `ocr_retention` 표에서 OCR 점수가 많이 떨어졌다면 `data.replay.count`를 늘리세요.
- **`cross_check`:** "문제없음"만 답해도 정상 문항(절반 이상)은 맞습니다. 종합 점수와 함께 **위치(변조 문항)**와 오탐률을 보세요.
