# 내부망 OCR → SFT → GRPO 파이프라인

Qwen3.5-9B 멀티모달 모델을 학습하는 파이프라인입니다. 서버는 **A100 40GB × 8장**이며, 이번 학습에는 **선택한 4장만** 사용합니다.
학습·검증·벤치마크 모두 내부 OCR의 **사람 검수 없는 의사정답**을 사용합니다.
벤치마크 결과는 실제 문서 정답률이 아니라 **내부 OCR과의 일치도**입니다. `GOLD`로 표시하지 않습니다.

이번 단계의 목표는 **글자 내용과 위치(박스 좌표) 이해**와 **현실적인 노이즈 대응**입니다. 정보추출·은행 업무 과제는 다음 단계입니다. 과제·좌표·증강·평가 설계는 [학습 과제와 데이터 설계](#학습-과제와-데이터-설계)를 먼저 읽으세요.

현재 검증 범위: 로컬 데이터 처리, 증강 후 박스 정렬, JSON 파싱, 평가, 보상, 캐시, 분리 검사, 모의 HTTP 추론입니다.
실제 내부 OCR 호출, Qwen 모델 추론, A100 학습은 아직 실행하지 않았습니다.

## 전체 수행 순서

```text
1. 내부망 환경 준비 및 설치
2. 내부 OCR 함수 연결
3. 입력 이미지와 문서 manifest 생성
4. 설정 파일 작성 및 데이터 준비
5. Base 모델 평가
6. SFT 학습
7. SFT 모델 평가
8. GRPO 학습 데이터 선정
9. GRPO 학습
10. GRPO 모델 평가
11. 최종 비교표 생성
```

모든 명령은 내부망 Linux 서버의 프로젝트 최상위 폴더에서 실행합니다. `/share/...`와 `/실제/.../checkpoint-xxx`는 실제 경로로 바꿉니다. 준비 데이터는 `data/prepared-v2`을 기준으로 안내합니다.

평가 서버는 한 번에 하나만 실행합니다. 서버 터미널을 유지한 채 별도 터미널에서 추론·평가하고, 학습 전에는 서버 터미널에서 `Ctrl+C`로 종료하여 GPU를 확보합니다.

**처음이면 [한 번에 실행](#한-번에-실행-run_pipelinepy-a100-80gb--2-기준)을 쓰세요.** 아래 1~11단계는 같은 과정을 한 단계씩 수동으로 실행하는 방법입니다. 기존 v1 프로젝트를 업데이트한다면 부록 C를 먼저 보세요.

## 학습 과제와 데이터 설계

### 좌표 형식

모든 위치는 Qwen-VL grounding 형식을 따릅니다. 좌표는 **모델에 들어가는 그 이미지 기준 0~1000 정수** `[x1, y1, x2, y2]`이고, 박스 출력은 `[{"bbox_2d": [...], "label": "글자"}]` JSON 리스트입니다. 없으면 `[]`입니다. 평가·보상은 ` ```json ` 코드 블록 하나로 감싼 출력도 받아들이고, 그 밖의 형식 오류는 오답으로 셉니다.

학습 전에 5단계 Base 평가의 `grounding` 예측 몇 건을 직접 열어 보세요. 좌표가 0~1000 범위인지(픽셀 좌표가 아닌지), 키가 `bbox_2d`인지 확인합니다. Base 결과의 `valid_json_rate`가 낮거나 박스가 일정 배율로 어긋나 있다면, 모델이 사전학습 때 익힌 형식과 다른 것이므로 학습 전에 형식을 맞춰야 합니다.

### 입력 이미지

OCR은 EXIF 방향만 보정한 원본에서 한 번 실행합니다. 모델 입력 이미지는 `image_max_size`(기본 `[2300, 1600]`, 긴 변 2300·짧은 변 1600 이하)로 줄여 `views/`에 저장합니다. A4 세로 원본(2480×3508)은 1600×2263이 됩니다. 좌표는 비율 좌표라 크기를 바꿔도 그대로 유효합니다.

`IMAGE_MAX_TOKEN_NUM`은 이 크기가 다시 줄어들지 않을 만큼 잡아야 합니다. `train.py`는 모델 `config.json`의 `vision_config.patch_size × spatial_merge_size`로 필요한 수를 계산합니다(32px 기준 2300×1600 → 3600). 평가 서버에도 같은 값을 쓰도록 아래 명령으로 확인합니다.

```bash
python -m bank_ocr image-tokens --model /share/cv_share/qwen3.5/9b --data data/prepared-v2
```

### 노이즈·기하 증강

같은 페이지에서 깨끗한 view(`clean`)와 망가뜨린 view(`aug`)를 함께 만듭니다. 정답은 깨끗한 원본의 OCR이고, 증강의 모든 기하 변환(자르기·±1.5° 회전·여백·축소)은 박스 좌표에도 똑같이 적용됩니다. 자르기로 잘린 글자는 `cut`으로 표시되어 어떤 과제에도 쓰이지 않습니다.

- 기하: 자르기(각 변 70% 이상 유지), 회전, 여백(종이·책상 색), 무작위 축소
- 화질: 흐림, 흔들림, JPEG 압축, 노이즈, 저해상도 후 확대, 대비·밝기, 그림자, 팩스형 이진화, 흑백 중 1~3개

view 수는 `views`(기본 train: clean 1 + aug 2, benchmark: clean 1 + aug 1), 증강 강도는 `augment`로 바꿉니다.

### 과제

| 과제 | 입력 | 출력 | 배우는 것 |
|---|---|---|---|
| `crop_ocr` | 단어를 잘라낸 이미지 | 글자 | 노이즈 속 글자 인식 |
| `bbox_ocr` | 페이지 + 단어 박스 | 글자 | 좌표 → 내용 |
| `grounding` | 페이지 + 글자 | 그 글자의 **모든** 박스 리스트, 없으면 `[]` | 내용 → 좌표, 반복 글자, 없는 글자 |
| `region_ocr` | 페이지 + 여러 단어를 덮는 영역 박스 | 영역 안 글자 전부(줄마다 줄바꿈) | 영역과 읽는 순서 |
| `spotting` | 페이지 또는 페이지에서 잘라낸 타일 | 모든 글자 + 박스 리스트 | 문서 전체 배치 |
| `relation` | 페이지 + 기준 글자(글자 또는 박스로 지정) + 방향 | 바로 오른쪽·왼쪽·위·아래 글자와 박스 | 좌표 사이 관계 |
| `marked_ocr` | 단어에 빨강·파랑·초록 박스를 그린 페이지 + 색 (30%는 좌표도 함께) | 그 박스 안 글자 | 그림으로 표시한 위치 → 내용 |
| `marked_box` | 같은 이미지 + 색 | 그린 박스의 좌표와 글자 | 그림으로 표시한 위치 → 좌표 숫자 |

`marked_*`는 좌표 숫자와 이미지 위치를 이어 주는 보조 과제입니다. `marked_box`의 좌표 정답은 OCR 박스가 아니라 직접 그린 사각형의 바깥 테두리라서 OCR 박스 오차가 없는 정확한 정답입니다. 그린 박스는 그 단어만 감싸야 하므로, 다른 단어나 다른 표시와 겹치는 단어는 고르지 않습니다. view 하나에 색이 다른 박스 최대 3개를 그린 이미지 1장(`marked/`)을 만들고 문항들이 함께 씁니다.

정답이 불완전해지는 영역은 쓰지 않습니다. 영역·타일은 단어를 자르지 않도록 넓히고, 그 안에 confidence가 낮거나 잘린 단어가 하나라도 있으면 버립니다. 단, spotting 타일은 낮은 confidence 단어를 주변 배경색으로 지우고 정답에서 뺍니다(`masked_words`에 개수 기록). 불확실한 단어가 페이지에 흩어져 있으면 여러 줄짜리 타일이 거의 모두 버려지기 때문입니다. `grounding`은 같은 글자가 모두 믿을 만할 때만, `relation`은 가장 가까운 이웃이 분명할 때만 만듭니다. 읽는 순서는 OCR 출력 순서가 아니라 박스 위치로 정합니다. 세로로 겹치는 단어를 한 줄로 묶고, 줄은 위→아래, 줄 안은 왼→오른쪽입니다.

SFT 비율은 `task_mix`(기본 crop 10 / bbox 15 / grounding 20 / region 15 / spotting 15 / relation 15 / marked_ocr 5 / marked_box 5%), view당 과제 수는 `tasks_per_view`로 바꿉니다. `grounding`의 약 10%는 페이지에 없는 글자를 묻는 부정 예시입니다(`negative_grounding_fraction`). 타일 하나의 글자 수는 `spotting_max_items`(기본 40) 이하라서 출력 길이가 제한됩니다.

**알려진 한계:** OCR이 아예 놓친 글자는 정답에도 없으므로, spotting은 그런 글자를 빠뜨리도록 배울 수 있습니다. 낮은 confidence 단어가 섞인 영역은 버리지만, 검출 자체가 안 된 글자는 걸러낼 방법이 없습니다.

### 평가

평가는 과제마다 다음을 계산하고, 전체·`view`(clean/aug)·`confidence`(교사 confidence ≥0.95 / 미만)·`size`(목표 박스 높이 small <12 / medium <25 / large) 별로 나눠 보고합니다. clean과 aug의 차이가 노이즈에 얼마나 견디는지를 보여 줍니다.

- 글자 과제: CER, EM, 숫자 EM. `region_ocr`은 순서와 무관한 단어 F1도 함께 봅니다(순서 오류와 인식 오류 구분).
- 박스 과제: IoU 0.5로 박스를 1:1로 짝지은 precision·recall·F1, IoU 0.75 F1, 두 박스가 서로의 중심을 포함하면 맞은 것으로 보는 F1(교사 박스가 얼마나 꽉 맞는지에 덜 민감), 짝지은 박스의 평균 IoU, 개수 정확도, 부정 예시 정확도, JSON 형식 정상 비율.
- `spotting`·`relation`·`marked_box`는 박스와 글자가 모두 맞아야 맞은 것으로 보는 위치+글자 F1과, 짝지은 박스의 글자 CER도 봅니다. `marked_box`는 정답 좌표가 정확하므로 비교표에 IoU 0.75 F1을 씁니다.

벤치마크 정답도 OCR 의사정답이라 OCR이 틀린 곳에서는 정답이 틀립니다. 노이즈 대응을 제대로 재려면 노이즈가 많은 페이지에서 사람이 검수한 소규모 정답셋을 따로 두는 것을 권합니다.

### GRPO 보상

```text
글자 과제 = 0.7 × 문자유사도 + 0.3 × 숫자유사도   (숫자가 없으면 문자유사도)
박스 과제 = 2 × Σ(짝별 점수) / (예측 박스 수 + 정답 박스 수)
  짝별 점수: grounding                    = min(1, IoU / 0.8)
             spotting·relation·marked_box = 0.5 × min(1, IoU / 0.8) + 0.5 × 글자 유사도
  정답이 []인 경우: 예측도 []이면 1, 아니면 0. JSON 형식 오류는 0.
```

박스는 IoU가 0보다 큰 쌍을 IoU 순으로 1:1로 짝짓습니다. 빠진 박스와 남는 박스는 분모에서 점수를 깎으므로, 박스를 많이 내거나 하나로 크게 덮는 식의 보상 꼼수가 통하지 않습니다. IoU 0.8 이상은 만점으로 둡니다. OCR 박스가 꽉 맞는 정도가 일정하지 않아서, 그 이상을 맞추라고 밀면 교사의 박스 잡음을 학습하게 되기 때문입니다.

GRPO 기본 과제는 출력이 여러 개라 점수 차이가 잘 생기는 `grounding`·`spotting`·`relation`입니다(`grpo_tasks`). 단어 하나짜리 글자 과제는 SFT 뒤 생성한 답이 대부분 같아져 학습 신호가 거의 없습니다.

## 한 번에 실행: run_pipeline.py (A100 80GB × 2 기준)

OCR을 이미 돌려 둔 JSON이 있으면 거기서 시작해 데이터 준비 → Base 평가 → SFT → SFT 평가 → GRPO 데이터 선정 → GRPO → GRPO 평가 → 비교표까지 한 명령으로 실행합니다. 각 단계는 끝나면 `<workdir>/state.json`에 기록되고, 중간에 멈추면 같은 명령으로 다시 실행해 이어 갑니다. 추론 중 멈춘 경우도 이미 받은 응답은 다시 요청하지 않습니다.

```bash
# 1) 이미지 목록. --ocr-dir: 이미 돌린 OCR JSON 폴더 (이미지와 같은 상대경로 또는 같은 파일명, 확장자만 .json)
python -m bank_ocr scan --root /share/data/images --split train \
  --document-regex '(?P<document_id>[^/]+)_p[0-9]+\.[^.]+$' \
  --ocr-dir /share/data/ocr_json --out data/manifest.jsonl

# 2) 설정
cp config.example.json config.json                 # benchmark_fraction 0.1 → 문서 10%를 벤치마크로 자동 분리
cp configs/pipeline.example.json configs/pipeline.json   # model 경로, gpus 확인

# 3) 리허설: 학습 5 step, 평가 60문항. 명령·메모리·서버 기동을 먼저 확인 (runs/exp1/smoke)
python run_pipeline.py --config configs/pipeline.json --smoke

# 4) 본 실행
nohup python run_pipeline.py --config configs/pipeline.json > pipeline.log 2>&1 &
```

결과는 `runs/exp1/reports/benchmark.html`입니다. 단계별 소요 시간은 `state.json`의 `timings`에 시간 단위로 남습니다.

| 옵션 | 의미 |
|---|---|
| `--smoke` | 학습 5 step, 벤치마크 60문항, GRPO 후보 40개. 별도 폴더(`workdir/smoke`) |
| `--from sft` | 그 단계부터 다시 실행 (예: SFT 설정을 바꿔 재학습) |
| `--only eval_base` | 한 단계만 실행 |
| `--dry-run` | 실행할 명령만 출력 |

**저장된 OCR 사용 조건:** JSON은 내부 OCR 응답 그대로(`success`, `data.basicData`, `bounding.vertices`)여야 하고, OCR을 돌린 이미지와 같은 파일이어야 합니다. 이미지에 EXIF 회전 정보가 있으면 좌표 기준이 모호하므로 중단합니다(그 페이지는 OCR을 다시 돌려야 합니다). JSON이 없는 이미지가 있으면 scan이 중단됩니다. manifest에 `ocr_json`이 없는 행만 `ocr_callable`로 OCR을 호출합니다.

**빠른 평가 구성:** GPU마다 추론 서버(vLLM)를 하나씩 띄우고 요청을 나눠 보냅니다. 같은 이미지에 대한 질문은 같은 서버로 보내고 연달아 처리해서, 이미지 처리 결과(prefix cache)를 다시 씁니다. 서버당 동시 요청은 `concurrency_per_server`(기본 16)입니다. SFT·GRPO 체크포인트는 평가 전에 `swift export --merge_lora`로 한 번 병합해 두 서버가 같은 병합 모델을 씁니다. SFT 평가 때 띄운 서버로 GRPO 후보 문제도 함께 풀어 둬서, 어려운 문제 선정에 서버를 다시 띄우지 않습니다.

**GRPO 데이터 선정:** `grpo.select`가 `mine`(기본)이면 `train_grpo.jsonl`에서 후보 6000개를 뽑아 SFT 모델로 풀고, 보상이 0.9 미만인 문제를 절반 섞어 2000개를 고릅니다. `random`은 무작위 2000개, `all`은 전체입니다. 2장 구성용 `configs/grpo_a100x2.yaml`은 GPU당 2개 × 2장 = 4 = `num_generations`가 되도록 batch를 맞춘 설정입니다.

**서버·병합 명령 바꾸기:** `eval.deploy_command`, `eval.merge_command`에 명령 목록을 넣으면 기본값을 대체합니다. `{model}`, `{model_type}`, `{port}`, `{adapter}`, `{output}`은 실행 시 채워집니다. 설치된 MS-SWIFT 버전에서 옵션 이름이 다르면 여기서 맞춥니다. 리허설(`--smoke`)이 이 명령들을 모두 한 번씩 실행해 봅니다.

### 2일 예상 (이미지 1000장, 문서 10% 벤치마크)

아래는 추정치입니다. 실제 값은 리허설과 첫 단계의 `timings`로 확인하세요.

| 단계 | 규모 | 예상 |
|---|---|---|
| 데이터 준비 | 1000장 × view 3장 (OCR 재호출 없음) | 0.5~1시간 |
| Base / SFT / GRPO 평가 | 각 약 4~5천 문항, 서버 2대 | 각 20~40분 (+서버 기동·병합 10~20분) |
| SFT | 최대 3만 문항, 문항당 약 3~4천 토큰 | 7~10시간 |
| GRPO 후보 풀이 | 6000문항 | 20~40분 |
| GRPO | 2000문제 × 생성 4개 | 5~8시간 |
| 합계 | | 약 16~23시간 |

시간이 부족하면 `config.json`의 `sft_max_examples`(예: 20000)와 `pipeline.json`의 `grpo.count`(예: 1000)를 먼저 줄이세요. 둘 다 학습 시간에 거의 비례합니다.

## 1. 내부망 환경 준비 및 설치

압축을 내부망 Linux 서버에 풀고 프로젝트 디렉터리로 이동합니다. 데이터 준비에는 Python 3.10+와 Pillow만 필요하며, 학습 환경은 Python 3.12를 권합니다.

```bash
python -m pip install --no-index --find-links /share/wheelhouse --no-build-isolation -e .
```

`setuptools>=68`, Pillow 및 빌드 도구도 내부 wheelhouse/환경에 준비해야 합니다. 인터넷이 되는 곳에서 대상 Linux/CUDA와 같은 환경으로 wheel 또는 컨테이너를 준비하세요. Windows wheel을 Linux로 복사해서 사용하면 안 됩니다.

`requirements-train.in`은 공식 Qwen3.5 v4.0 문서 기준의 **후보 환경**이며 GPU에서 검증한 lockfile은 아닙니다. CUDA에 맞는 PyTorch, ms-swift 4.x, Transformers, PEFT, DeepSpeed를 준비하세요. Qwen3.5용 커널은 같은 PyTorch/CUDA 환경에서 준비해야 합니다. 런처는 실제 학습 시작 시 설치 버전을 `environment.freeze.txt`에 기록합니다.

모델 경로는 `/share/cv_share/qwen3.5/9b`이며, 이 폴더에 로컬 Qwen3.5-9B 전체 파일이 있어야 합니다. 9B는 멀티모달 모델이며 이름 뒤에 임의로 `-VL`을 붙이지 않습니다.

### 설정 파일과 옵션 변경

| 파일 | 적용 범위 |
|---|---|
| `config.json` | OCR 연결·데이터 준비·분리·필터. 학습 설정과 별개 |
| `configs/sft.yaml` | SFT 학습률·epoch·batch·LoRA·freeze·저장/검증 주기 등 |
| `configs/grpo.yaml` | GRPO 학습 및 rollout 생성 수·temperature·top-p·응답 길이·vLLM 등 |
| `configs/inference.json` | 평가용 HTTP 추론의 서버·모델·timeout·생성 설정 |

YAML을 읽는 런처에는 `PyYAML>=6,<7`이 필요합니다. 학습 의존성은 `requirements-train.in`에 포함되어 있으며 내부망 wheelhouse에서 준비합니다. OCR 준비와 JSON 추론 설정에는 PyYAML이 필요하지 않습니다.

```bash
python -m pip install --no-index --find-links /share/wheelhouse --no-build-isolation -r requirements-train.in
```

학습 YAML은 MS-SWIFT 4.x의 인자 이름을 그대로 사용합니다. 알려진 몇 개 옵션만 허용하는 방식이 아니라 추가 옵션도 SWIFT 명령으로 전달합니다. 지원 여부는 설치된 SWIFT 버전에서 검사합니다. bool·list·dict 값도 지원하며, dict는 JSON 인자로 변환합니다. 예를 들어 SFT 설정에서 다음 값을 변경할 수 있습니다.

```yaml
learning_rate: 2.0e-5
num_train_epochs: 3
per_device_train_batch_size: 1
gradient_accumulation_steps: 8
lora_rank: 32
lora_alpha: 64
freeze_vit: true
save_steps: 200
eval_steps: 200
gradient_checkpointing_kwargs:
  use_reentrant: false
```

`--config`를 생략하면 프로젝트의 `configs/sft.yaml` 또는 `configs/grpo.yaml`을 사용합니다. 다른 실험은 파일을 복사하여 `--config configs/sft-experiment.yaml`로 지정하세요. 사용자 설정 파일은 기본 파일을 대체하며 자동 병합하지 않습니다. 위 예시는 변경할 항목의 발췌입니다.

`--max-steps`와 `--deepspeed` CLI 값은 YAML의 해당 값을 덮어씁니다. DeepSpeed는 `zero2`, `zero3` 또는 사용자 JSON 파일 경로를 받을 수 있습니다. YAML에 있는 추가 파일 경로는 실행 디렉터리 기준으로 지정합니다.

모델·데이터·출력·adapter 경로는 기존 CLI(`--model`, `--data`, `--output`, `--adapter`, `--grpo-dataset`)로 지정합니다. YAML에 `model`, `dataset`, `val_dataset`, `output_dir`, `adapters`, `ref_adapters`, `config`, `ENV`를 넣으면 오류로 안내합니다. SFT validation은 준비된 `val_sft.jsonl`에서 연결하고, GRPO 데이터는 train 여부를 검사합니다. GRPO의 `remove_unused_columns`는 보상 필드를 보존하도록 false로 유지합니다. 기본 보상 플러그인은 자동 연결하며, 별도 플러그인을 지정하려면 `external_plugins`와 `reward_funcs`를 함께 맞춥니다.

실제 실행 시 `launch.json`에 선택 GPU·프로세스 수·명령을, `training.resolved.json`에 최종 학습 옵션을, `environment.freeze.txt`에 설치 버전을 기록합니다. `--execute`를 빼면 학습 없이 최종 명령을 확인합니다.

### 8장 중 사용할 GPU 4장 지정

본문은 0~3번 GPU를 사용합니다. 4~7번을 사용하려면 학습 명령의 `--gpus`를 바꿉니다.

```bash
python train.py sft --config configs/sft.yaml --gpus 4,5,6,7 \
  --model /share/cv_share/qwen3.5/9b --data data/prepared-v2 --output runs/sft --execute
```

선택 우선순위는 **`--gpus` → `CUDA_VISIBLE_DEVICES` 환경변수 → 기본 0,1,2,3**입니다. `NPROC_PER_NODE`는 선택한 GPU 수로 자동 설정합니다. 서버에 8장이 있어도 예제의 명시적인 `--gpus`로 선택한 4장만 학습에 사용합니다. 다른 작업과 동시에 학습할 때는 `MASTER_PORT`도 겹치지 않게 지정하세요.

이미지 토큰 예산은 **`--image-tokens` → `IMAGE_MAX_TOKEN_NUM` 환경변수 → 모델 설정과 `image_max_size`로 계산한 값** 순서입니다. 평가 서버에는 `python -m bank_ocr image-tokens`가 알려 주는 같은 값을 `IMAGE_MAX_TOKEN_NUM`으로 지정합니다. 평가 서버의 `CUDA_VISIBLE_DEVICES=0`도 원하는 GPU 번호로 바꿀 수 있습니다. 학습용 `NPROC_PER_NODE=4`를 export해 두었다면 평가 서버 실행 전 해제합니다.

**완료 기준:** 프로젝트 설치, 학습 의존성, 로컬 모델 파일이 준비되어 있습니다.

## 2. 내부 OCR 함수 연결

`internal_ocr_adapter.py`는 첨부 이미지의 코드를 그대로 사용합니다. `BASE_URL`은 환경변수 `INTERNAL_OCR_BASE_URL`에서 읽으며(기본값 `http://localhost:30107`) `OCR_URL`(`/ocr`)에 multipart `file` 필드로 이미지를 전송합니다. 실행 전에 내부 OCR 서버 주소를 설정합니다(예: `export INTERNAL_OCR_BASE_URL=http://<내부-OCR-호스트>:<포트>`).

첨부 코드에서 import하는 requests와 matplotlib은 OCR 의존성에 포함되어 있습니다.

```bash
python -m pip install --no-index --find-links /share/wheelhouse --no-build-isolation -e '.[ocr]'
```

`config.json`의 `ocr_callable`은 `internal_ocr_adapter:ocr_from_file`로 유지합니다. HTTP 200이면 원본 JSON을 반환하고, 그 외에는 상태 코드와 응답 본문을 출력한 뒤 `None`을 반환합니다. timeout과 자동 재시도는 지정하지 않습니다.

`prepare`는 EXIF 방향을 보정한 PNG를 전달합니다. 어댑터는 이 파일을 그대로 전송하며, 반환값의 `success`·필드·좌표 검사는 기존 데이터 준비 코드가 수행합니다. 실패 응답은 성공 캐시에 저장되지 않습니다.

기본 JSON 매핑은 아래 실제 구조에 맞춰져 있습니다. `basicData`는 평평한 배열과 여러 겹 배열을 모두 지원합니다.

```json
{
  "filename": "page.png",
  "success": "Y",
  "data": {
    "basicData": [[{
      "text": "2024",
      "confidence": 0.9999,
      "bounding": {
        "shape": "rectangle",
        "vertices": [{"x":140,"y":46},{"x":224,"y":46},{"x":224,"y":76},{"x":140,"y":76}]
      },
      "line_num": 0
    }]]
  }
}
```

`success != "Y"`, 잘못된 좌표·신뢰도·필드가 있으면 중단합니다. 실패 응답은 성공 캐시에 저장하지 않습니다. 성공한 빈 페이지는 기록하지만 학습 예제는 만들지 않습니다. 임의의 재시도·누락 처리는 하지 않습니다.

**완료 기준:** OCR 의존성과 어댑터의 `BASE_URL` 설정이 준비되어 있습니다. 실제 호출과 매핑은 4단계에서 소량의 데이터로 확인합니다.

## 3. 입력 이미지와 문서 manifest 생성

사용자가 반입한 페이지 이미지를 그대로 입력합니다. PDF와 다중 페이지 TIFF는 먼저 페이지별 이미지로 렌더링해야 합니다. 자동 페이지 분할은 이 버전에 포함하지 않습니다.

예: `doc123_p001.png`, `doc123_p002.png`에서 `doc123`이 원본 문서 ID라면:

```bash
python -m bank_ocr scan --root /share/data/train --split train \
  --document-regex '(?P<document_id>[^/]+)_p[0-9]+\.[^.]+$' --out data/train-manifest.jsonl

python -m bank_ocr scan --root /share/data/benchmark --split benchmark \
  --document-regex '(?P<document_id>[^/]+)_p[0-9]+\.[^.]+$' --out data/benchmark-manifest.jsonl

python -m bank_ocr merge data/train-manifest.jsonl data/benchmark-manifest.jsonl --out data/manifest.jsonl
```

문서마다 하위 폴더가 있는 구조라면 `--document-regex '^(?P<document_id>[^/]+)/'`를 사용할 수 있습니다.
**이미지 한 장이 독립된 원본 문서인 경우에만** `--single-page-documents`를 사용합니다.
파일명 규칙으로 원본 문서를 알 수 없다면 아래 형식으로 manifest를 직접 만듭니다.

```json
{"document_id":"original_doc_123","page_id":"p001","image":"/share/data/a.png","split":"train"}
{"document_id":"original_doc_456","page_id":"p001","image":"/share/data/b.png","split":"benchmark"}
```

문서 ID는 전체 데이터에서 일관되고 고유해야 합니다. 서로 다른 문서에 같은 ID를 주거나 같은 문서를 서로 다른 ID로 주면 안 됩니다. 근사 복제·스캔 노이즈·동일 템플릿까지 자동 판별하지는 않습니다.

기본으로 학습 문서의 5%를 문서 단위로 validation에 배정합니다. 이미 `val` manifest가 있으면 그 구분을 사용합니다. 벤치마크 문서는 사용자가 지정한 것을 모두 유지하며, view당 과제 수(`tasks_per_view.benchmark`)만큼 고정 seed로 뽑습니다. 별도 hard benchmark 선정이나 1,000페이지 강제 추출은 하지 않습니다.

**완료 기준:** `data/manifest.jsonl`이 생성되어 있습니다.

## 4. 설정 파일 작성 및 데이터 준비

예제 설정은 `manifest=data/manifest.jsonl`, `output_dir=data/prepared-v2`, `cache_dir=data/ocr-cache`, `ocr_callable=internal_ocr_adapter:ocr_from_file`입니다. `ocr_revision`은 실제 OCR 버전으로 변경합니다. 소량 확인과 전체 준비는 서로 다른 `output_dir`를 사용하고, 이후 명령은 전체 준비 결과 경로에 맞춥니다.

```bash
cp config.example.json config.json
# config.json의 manifest / output_dir / cache_dir / ocr_revision 수정
python -m bank_ocr prepare --config config.json
```

설정 파일의 상대경로는 설정 파일 기준입니다. manifest의 상대 이미지 경로는 manifest 기준입니다. 생성 JSONL에는 내부망의 절대 이미지 경로가 들어갑니다. **서버에 반입한 후 prepare를 실행**하세요. 나중에 데이터 위치를 옮기면 경로 재생성이 필요합니다.

주요 결과:

| 파일 | 용도 |
|---|---|
| `pages.jsonl` | 원본 OCR, 좌표, confidence, split, 원본 이미지 경로 |
| `train_sft.jsonl`, `val_sft.jsonl` | MS-SWIFT SFT 입력 |
| `train_grpo.jsonl` | `grpo_tasks` 과제와 reward용 `task`·`target` 필드 |
| `train_tasks.jsonl`, `val_tasks.jsonl`, `benchmark_tasks.jsonl` | 추론·평가 및 분석 입력. `view`(clean/aug)·`view_ops`·`confidence`·`size` 포함 |
| `views/` | 모델 입력 페이지 이미지(clean·aug) |
| `crops/`, `tiles/`, `marked/` | Crop OCR 단어 이미지, spotting 타일, 박스를 그린 이미지 |
| `image_items.jsonl` | 이미지별 교사 OCR 박스(view 좌표). `--with-ocr` 비교군과 점검용 |
| `DONE.json` | 완료 여부, 분리별 개수, 필터 통계, manifest 해시 |
| `config.snapshot.json` | 실행 시 설정 |

OCR 원본과 방향 보정 페이지는 `cache_dir`에 있으므로 **준비가 끝나도 캐시를 지우지 마세요**. 학습·추론이 해당 페이지를 참조합니다.

학습 confidence 기본값은 0.95, 벤치마크는 0.0입니다. 벤치마크에서 낮은 confidence를 숨기지 않습니다. 두 쪽 모두 공백, 길이 범위 밖, 대체문자 `�`를 제외하며, 제외 개수를 기록합니다. 낮은 confidence 단어는 질문 대상이 되지 않고, 그 단어가 걸친 영역·타일·grounding 질문은 만들지 않습니다. 이전 설정 키 `train_regions_per_page`·`benchmark_regions_per_page`는 `tasks_per_view`로 바뀌었고, 남아 있으면 prepare가 중단됩니다.

`output_dir`가 이미 있으면 덮어쓰지 않습니다. 실패한 준비 작업은 새 `output_dir`로 다시 실행하면 성공 OCR 캐시를 재사용합니다. `ocr_revision`은 OCR 모델·전처리·함수 동작이 바뀔 때 변경해야 합니다. 서버를 변경하여 OCR 동작이 달라질 때도 버전을 변경하세요. 어댑터의 서버 주소는 캐시 키에 자동 포함되지 않습니다. 최초 실행은 소량의 train/benchmark 문서로 매핑과 출력량을 확인하는 편이 좋습니다.

**완료 기준:** `data/prepared-v2/DONE.json`과 학습·벤치마크 JSONL이 생성되어 있습니다. 분리별 개수와 필터 통계를 확인합니다.

## 5. Base 모델 평가

로컬 Qwen3.5-9B를 배포할 때는 `--model_type qwen3_5`를 명시합니다. 자동 판별 시 `qwen3_5`와 `ovis_ocr2`가 함께 후보로 잡혀 `Multiple possible model types found` 오류가 발생할 수 있습니다. 아래 Base/SFT/GRPO 배포 명령에 동일하게 적용합니다.

학습 전 기준 성능을 저장합니다. `prepare`는 평가를 자동 실행하지 않습니다.

**세 모델은 같은 벤치마크·이미지·이미지 토큰 예산으로 평가하며 `--with-ocr`를 사용하지 않습니다.** 체크포인트 변경 시 새 `run-id`와 예측 파일을 사용하고 `.meta.json`도 보관합니다. 인증과 자세한 조건은 부록 A를 확인하세요.

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

`--execute`를 빼면 실행할 명령만 표시합니다. 제공한 설정 파일의 기본값은 BF16, LoRA rank 16, ViT·aligner·LLM 학습, microbatch 1, 누적 4, ZeRO-2, gradient checkpointing, 이미지 토큰은 `image_max_size`에 맞춰 자동 계산(2300×1600, 32px 기준 3600), max_length 8192입니다. GRPO의 `max_completion_length`는 spotting 출력을 담기 위해 1536입니다. 인터넷 모델 다운로드와 외부 실험 추적은 기본으로 비활성화합니다.

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

GRPO는 SFT adapter와 ref_adapter에서 시작합니다. `configs/grpo.yaml`의 초기 설정은 `num_generations=4`, `use_vllm=false`이며 변경할 수 있습니다. 처음에는 vLLM rollout 엔진의 추가 메모리와 vision LoRA 동기화 변수를 줄이는 설정입니다. 속도는 이후 측정·개선 대상입니다.

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

프로젝트 최상위 폴더에 `benchmark_report.py`가 있는지 확인하고 실행합니다.

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

## 부록 A. 평가 조건과 지표 해석

### 추론 설정 변경

모든 예측 명령은 `configs/inference.json`을 사용합니다. `endpoint`, `model`, `timeout`, `max_tokens`, `temperature`, `enable_thinking`을 변경할 수 있습니다. 추가 서버 지원 옵션은 `request_options`에 넣습니다.

```json
{
  "endpoint": "http://127.0.0.1:8000/v1",
  "model": "bank-ocr",
  "timeout": 180,
  "max_tokens": 2048,
  "temperature": 0,
  "enable_thinking": false,
  "request_options": {"top_p": 0.95}
}
```

명시한 CLI 옵션이 설정 파일보다 우선합니다. 예: `--max-tokens 128 --temperature 0 --no-enable-thinking`. thinking을 켜려면 `--enable-thinking`을 사용하고 서버 실행 옵션도 맞춥니다. 생성 길이를 늘리면 서버의 `--max_new_tokens` 설정도 확인하세요. 서버 배포 옵션은 `swift deploy` 명령에서 변경합니다. 이 JSON은 HTTP 요청 설정이며 서버를 시작하거나 GPU 배치를 변경하지 않습니다.

`request_options`의 지원 여부는 내부 모델 서버에 따라 다릅니다. `model`, `messages`, `stream`, `temperature`, `max_tokens`, `chat_template_kwargs`는 추가 옵션으로 덮어쓸 수 없습니다. 기본 모델 입력 구성은 유지합니다.

생성 설정은 예측 `.meta.json`에 기록됩니다. 설정이 바뀌면 새 예측 파일을 사용합니다. 비교 보고서는 temperature·max_tokens·thinking뿐 아니라 추가 요청 옵션이 달라도 비교를 중단합니다. Base/SFT/GRPO에는 같은 추론 설정을 사용하세요. `evaluate`는 저장된 예측의 점수를 계산하며 MS-SWIFT 학습 YAML을 읽지 않습니다. 지표 정의와 IoU@0.5 기준은 고정되어 있습니다.

체크포인트가 바뀌면 반드시 새 `run-id`와 예측 파일 경로를 사용하세요. 같은 run-id·입력의 완료된 예측은 재사용합니다. 입력 파일이나 이미지가 바뀌면 같은 예측 파일에 이어 쓰지 않습니다. 재사용 확인을 위해 예측 파일 옆의 `.meta.json`도 보관하세요.

`predict --with-ocr`는 Base+Bank OCR 별도 비교군용입니다. 이 모드는 내부 OCR 텍스트·좌표를 입력에도 제공하므로 **교사 정보를 제공한 비교군**입니다. 여기서 만드는 Base / SFT / GRPO 비교표에는 세 모델 모두 `--with-ocr`를 사용하지 않습니다. 기본 추론에는 target/정답/OCR context를 보내지 않습니다. 필요한 인증 토큰은 `INTERNAL_MODEL_API_KEY` 환경변수로 받습니다.

비교할 보고서는 같은 tasks SHA256을 사용해야 합니다. CER은 전체 문자 편집거리/전체 정답 문자 수이며 삽입 오류가 많으면 1보다 클 수 있습니다. EM은 NFC·양끝 공백 정규화 후 비교하고 숫자는 기호와 토큰 경계를 보존합니다. 박스 과제는 JSON 형식을 엄격히 검사하며, 형식이 틀린 응답은 예측 박스 0개로 셉니다. 박스 지표의 정의는 [평가](#평가)를 확인하세요. 평가 JSON의 `breakdown`에 view·confidence·size별 결과가 있고, 비교 보고서는 clean·aug 표를 따로 보여 줍니다.

HTML·Markdown 점수는 % 단위로 표시합니다. CSV 점수는 원래 비율값이며, 예를 들어 `0.8`은 80%입니다. CER은 오류가 많으면 100%를 넘을 수 있습니다. 변화량 컬럼(`*_delta_pp`)은 세 형식 모두 **해당 모델 − Base의 퍼센트포인트(pp)**입니다. CER은 음수 변화가 개선, 나머지 지표는 양수 변화가 개선입니다. Numeric EM은 BBox→Text에서 숫자가 있는 대상의 숫자 토큰 일치율입니다.

박스 지표의 F1@0.5는 IoU 0.5 이상으로 짝지은 박스 기준이고, 위치+글자 F1은 글자까지 같아야 맞은 것으로 셉니다.

계산 대상이 없는 지표는 HTML·Markdown에서 `—`, CSV에서 빈 값으로 표시합니다. 미측정 점수를 0으로 채우지 않습니다. 보고서에는 사람 검수 없는 OCR 의사정답 기준이라는 설명과 평가 건수도 들어갑니다.

서로 다른 벤치마크 SHA256·평가 건수는 비교를 거부합니다. 추론 메타데이터에 기록된 이미지 해시·temperature·max_tokens·thinking·추가 요청 옵션 조건이 서로 달라도 중단합니다. 메타데이터가 없다면 확인 불가 사실을 표시합니다. 실제 서버 체크포인트와 이미지 토큰 예산은 스크립트가 확인할 수 없으므로 실행 시 맞춰야 합니다.

기존 `python -m bank_ocr compare ... --out reports/comparison.csv`도 그대로 사용할 수 있습니다. 브라우저용 표와 Base 대비 변화량까지 필요할 때는 위 독립 스크립트를 사용합니다. 보고서 생성만 필요하다면 이미 완료한 평가를 다시 실행할 필요는 없습니다. 설정 구조 변경의 반입 파일은 부록 C를 확인하세요.

## 부록 B. GRPO 보상과 rollout 진단

보상 정의는 [GRPO 보상](#grpo-보상)에 있습니다. 학습 중 내부 OCR을 다시 호출하지 않으며, 보상은 교사 OCR 오류도 따라갈 수 있습니다. 8단계 `mine`은 같은 보상이 `--hard-threshold`(기본 0.9)보다 낮은 train 행을 어려운 문제로 고릅니다.

동일 응답으로 GRPO 신호가 사라지는지 확인하려면 rollout 로그를 아래 형식으로 정리해 사용합니다. SWIFT 버전별 원본 로그 자동 변환은 포함하지 않습니다.

```json
{"id":"train_grpo.jsonl에 있는 id","completions":["응답1","응답2","응답3","응답4"]}
```

```bash
python -m bank_ocr rollout-stats --tasks data/prepared-v2/train_grpo.jsonl \
  --rollouts data/rollouts.jsonl --out reports/rollout-stats.json
```

## 부록 C. 이미 반입한 프로젝트 업데이트 (prepared-v1 → v2)

기존 `bank-ocr-pipeline` 폴더에 새 코드를 덮어쓰고, 이미 돌린 OCR 캐시(`data/ocr-cache`)를 그대로 재사용합니다. OCR은 다시 호출하지 않습니다.

```bash
# 1) 백업 후 덮어쓰기. 업데이트 zip에는 internal_ocr_adapter.py·config.json·data/·predictions/·reports/·runs/가 없어 기존 것이 유지됩니다.
cp -r bank-ocr-pipeline bank-ocr-pipeline.bak
cd bank-ocr-pipeline
unzip -o /반입경로/bank-ocr-pipeline-update.zip
pip install --no-index --no-build-isolation -e .

# 2) config.json을 새 형식으로 (OCR 관련 값은 유지, 새 항목 추가, 결과는 data/prepared-v2)
cp config.json config.json.bak
python - <<'PY'
import json
old = json.load(open("config.json")); new = json.load(open("config.example.json"))
keep = ("manifest", "cache_dir", "ocr_callable", "ocr_revision", "mapping", "seed", "val_fraction", "filters", "sft_max_examples")
cfg = {**new, **{k: old[k] for k in keep if k in old}, "output_dir": "data/prepared-v2"}
json.dump(cfg, open("config.json", "w"), ensure_ascii=False, indent=2)
PY

# 3) 실행 (위의 "한 번에 실행" 참고)
cp configs/pipeline.example.json configs/pipeline.json
python run_pipeline.py --config configs/pipeline.json --smoke
nohup python run_pipeline.py --config configs/pipeline.json > pipeline.log 2>&1 &
```

- 캐시는 `이미지 픽셀 + ocr_callable + ocr_revision`으로 찾습니다. `cache_dir`·`ocr_callable`·`ocr_revision`을 바꾸면 OCR을 다시 호출합니다.
- 기존 `prepared-v1`, `predictions/`, `reports/`는 지우지 않아도 됩니다. 새 결과는 `runs/exp1/`에 따로 쌓입니다.
- v1 벤치마크(region 기반) 점수는 v2 벤치마크와 비교할 수 없습니다. run_pipeline이 Base부터 다시 평가합니다.
- benchmark manifest가 이미 있으면 `benchmark_fraction`은 적용되지 않고 기존 벤치마크 문서를 그대로 씁니다.

## 부록 D. 로컬 검사·검증 범위·제약

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

## 부록 E. 공식 참고 문서

- [Qwen3.5 / MS-SWIFT v4.0](https://swift.readthedocs.io/en/v4.0/BestPractices/Qwen3_5-Best-Practice.html)
- [MS-SWIFT reward plugin](https://swift.readthedocs.io/en/latest/Instruction/GRPO/DeveloperGuide/reward_function.html)
- [Inference and deployment](https://swift.readthedocs.io/en/latest/Instruction/Inference-and-deployment.html)
- [사용자 정의 추가 컬럼 보존](https://swift.readthedocs.io/en/latest/Instruction/Frequently-asked-questions.html)

외부 문서 확인은 공개 라이브러리 인터페이스에만 사용했으며, 은행 이미지나 OCR 내용을 외부 모델 API로 보내지 않았습니다.
