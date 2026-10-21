# 처음부터 따라하기

이 저장소만으로 **데이터 만들기 → 학습 → 결과 확인**까지 하는 방법을 순서대로 적었습니다. 단계마다 "확인" 항목이 있으니, 확인이 통과한 뒤 다음 단계로 넘어가세요. 막히면 맨 아래 [자주 나는 에러](#자주-나는-에러)를 보세요.

- 프로젝트가 무엇인지 먼저 보려면: [overview.md](overview.md)
- 데이터가 이미 있다면: [4. 학습](#4-학습)부터
- 각 과제의 실제 데이터(질문·정답·필드)를 보려면: [tasks.md](tasks.md)

> 2026-10-21부터 옛 1부 OCR(`ocr/`)과 2부 은행 업무(`bank/`)를 하나로 합쳤습니다. OCR 데이터와 은행 업무 데이터를 섞어 **한 번** 학습합니다. 설계는 [studio/DESIGN.md](../studio/DESIGN.md) 17절.

## 0. 전체 그림: 어디서 무엇을 하나

| 어디서 | 무엇을 | 필요한 것 |
|---|---|---|
| **GPU 서버** (내부망, 학습 환경) | 사내 OCR 서버, 실서류 OCR 준비, 학습·평가(`train/`) | A100 2장 이상, ms-swift 4.x + vLLM이 설치된 파이썬 환경, Qwen3.5-9B 모델 파일 |
| **docgen 도커 컨테이너** (CPU) | 합성 데이터 만들기(`docgen/`), studio 화면(`studio/`: 데이터셋 보기·채점·비교) | docgen 도커 이미지 ([docker/README.md](../docker/README.md)) |

```text
[도커]      bash docgen/scripts/make_bank_data.sh ─→ bench/, bank_train/            (문서 이해·업무 과제)
[GPU 서버]  위 데이터셋 + 실제 서류 이미지 폴더 ─→ python -m train ─→ 모델 + 비교표 (train/runs/exp1/)
              └ 첫 단계 ocr: 이미지 폴더 ─(사내 OCR)→ OCR 준비 ─→ OCR 과제 (처음 한 번, 캐시)
```

GPU 서버의 명령은 모두 `<코드>`(저장소 최상위)에서 실행합니다. 데이터셋은 모두 같은 과제 형식(`meta.json` + `tasks/<과제>.jsonl`)이라 studio ⑥에서 만든 데이터셋도 그대로 씁니다.

이 문서의 경로 표기:

| 표기 | 뜻 | 예 |
|---|---|---|
| `<코드>` | 이 저장소를 받은 폴더 | `/share/<계정>/document_gen` |
| `<데이터>` | 도커 컨테이너의 `/out`과 연결한 서버 폴더 | `/share/<계정>/docgen_data` |
| `<모델>` | 원래 Qwen3.5-9B 모델 폴더 | `/share/cv_share/qwen3.5/9b` |
| `<이미지>` | 실제 서류 쪽 이미지 폴더 (2절) | `/share/data/images` |

---

## 1. 준비 (한 번)

### 1-1. 코드 받기

```bash
git clone -b claude/ocr-banking-benchmark https://github.com/kimsh12191/document_gen.git <코드>
# 내부망이라 git이 안 되면: 인터넷 PC에서 sh docker/build.sh 로 만든 docgen-code-*.tar.gz 를 반입해 풀기
```

폴더 구성:

```text
<코드>/
  docgen/            합성 서류·벤치마크 생성기, 과제 채점(docgen/bench/evaluate.py), OCR 준비(docgen/bench/ocr_*.py)
  train/             학습 실행 하나 (python -m train): 데이터셋 섞기 → SFT → GRPO → 평가 → 비교표
    configs/               설정 예제 (pipeline.example.json, sft·grpo yaml, inference.json)
  studio/            데이터 만들기·검수·데이터셋·평가 화면 (docgen 도커에서 띄움)
  docker/            docgen 도커 이미지 만들기 (Dockerfile, build.sh)
  guide/             사용 가이드 (이 문서)
```

### 1-2. 학습 환경 확인

설치할 패키지는 없습니다. 저장소 최상위에서 `python -m train`으로 실행하면 `docgen`·`train`을 그대로 불러옵니다. 학습용 파이썬 환경(ms-swift가 깔린 가상환경)에 `pillow`, `pyyaml`, `requests`(사내 OCR 호출)가 있으면 됩니다.

**확인**
```bash
cd <코드>
python -c "import swift, vllm, PIL, yaml, docgen.bench.evaluate, train; print('ok')"   # ok 가 나와야 함
swift --help | head -3                                              # 도움말이 나와야 함
ls <모델>/config.json                                               # 모델 파일이 있어야 함
nvidia-smi                                                          # 쓸 GPU가 비어 있는지
```

---

## 2. OCR 데이터 (실서류)

실제 서류 이미지를 사내 OCR에 돌린 결과를 정답으로, 글자와 위치를 읽는 과제를 만듭니다. 과제 8종은 [tasks.md](tasks.md#ocr-과제)에 있습니다. 합성 서류로 OCR 세트를 만들려면 `python -m docgen.ocr_set build`나 studio ⑥(합성 OCR), 가져온 이미지는 studio ④ "OCR 벤치마크로"를 씁니다. 이때는 이 절을 건너뜁니다.

### 2-1. 이미지 모으기

페이지 이미지(PNG/JPG/TIF)를 한 폴더(`<이미지>`)에 둡니다. 하위 폴더까지 읽습니다.
- PDF는 쪽별 이미지로 먼저 바꿉니다.
- **같은 문서의 쪽들은 한 하위 폴더에 둡니다.** 예: `<이미지>/doc123/p001.png`, `<이미지>/doc123/p002.png` → 문서 `doc123`. 학습과 평가를 문서 단위로 나누기 때문입니다. 최상위에 둔 그림은 하나가 한 문서입니다. 폴더 대신 파일 이름으로 묶으려면 4-1의 `documents`에 정규식을 씁니다.

### 2-2. 사내 OCR 서버 띄우기

OCR 결과 JSON을 이미 갖고 있으면 이 단계는 건너뜁니다(4-1의 `ocr_images`에서 폴더마다 `ocr_dir`를 씁니다).

이번 학습에 쓴 사내 OCR은 **`/share/mond/ocr_api/server.py`**입니다. GPU 번호(`GPU_ID`)와 포트(`SERVER_PORT`)를 정해서 띄웁니다.

```bash
# 터미널 1: 사내 OCR 서버. 학습에 안 쓸 GPU를 고릅니다. 켜 둔 채로 둡니다.
cd /share/mond/ocr_api
GPU_ID=7 SERVER_PORT=30107 python server.py
```

```bash
# 터미널 2: 이후 명령을 실행할 터미널. 같은 포트를 알려 줍니다.
export INTERNAL_OCR_BASE_URL=http://localhost:30107
```

**확인:** `curl -s $INTERNAL_OCR_BASE_URL/health`에 응답이 오면 연결된 것입니다(서버가 health를 지원할 때).

### 2-3. OCR은 학습이 한다

이미지 폴더 경로만 정해 두면 됩니다. 4-1 설정의 `data.ocr_images`에 적으면 `python -m train`의 첫 단계(`ocr`)가 폴더를 읽어 사내 OCR을 부르고(캐시에 없는 그림만), OCR 과제를 만들어 학습·평가에 넣습니다. 다음 실험에서 같은 그림은 OCR을 다시 부르지 않습니다(`ocr-cache`).

손으로 따로 만들고 싶으면(다른 실험과 나눠 쓰기 등): `docgen.bench.ocr_data.scan`으로 manifest를 만들고 `python -m docgen.bench.ocr_prepare <설정>`(예시 `docgen/bench/ocr_config.example.json`)을 돌린 뒤, 그 `output_dir`을 `data.train`·`data.benchmark`에 적습니다.

---

## 3. 은행 업무 데이터 (합성, docgen 도커)

도커 컨테이너가 아직 없으면 [docker/README.md](../docker/README.md)대로 띄웁니다. 이때 `-v <데이터>:/out`으로 연결한 서버 폴더에 결과가 생깁니다.

```bash
ssh -p 2222 docgen@<서버IP>                 # 컨테이너 접속 (접속하면 코드 폴더에서 시작)
bash docgen/scripts/make_bank_data.sh              # 백그라운드로 시작. SSH를 끊어도 계속
tail -f /out/logs/make_bank_data.log        # "전부 완료" 가 나오면 끝 (약 1시간 15분)
```

SSH 대신 서버 터미널에서 바로: `docker exec -u docgen docgen bash -lc 'bash ~/document_gen/docgen/scripts/make_bank_data.sh'`

양·출력 위치를 바꾸는 환경변수(`OUT`, `TRAIN_BUNDLES`, `BENCH_BUNDLES` 등)는 `docgen/scripts/make_bank_data.sh` 맨 위 주석에 있습니다.

**확인** (서버에서)
```bash
ls <데이터>/bench/meta.json <데이터>/bank_train/meta.json     # 둘 다 있어야 함
du -sh <데이터>/bench <데이터>/bank_train                       # 약 3GB, 약 16GB
```

studio ⑥ 데이터셋에서 만든 데이터셋(합성·실서류 라벨·OCR)도 같은 형식이라 다음 절의 `data.train`·`data.benchmark`에 그대로 넣습니다.

---

## 4. 학습

### 4-1. 설정 파일

```bash
cd <코드>
cp train/configs/pipeline.example.json train/configs/pipeline.json
```

`train/configs/pipeline.json`에서 바꿀 것 (데이터는 **서버의 절대 경로**로 씁니다):

```jsonc
{
  "workdir": "../runs/exp1",                         // 결과 폴더 (<코드>/train/runs/exp1). 그대로 둬도 됨
  "model": "<모델>",                                  // 출발 모델. 다른 모델에서 출발해도 됨
  "gpus": [5, 6],                                    // OCR 서버 GPU와 겹치지 않게
  "data": {
    "train": [
      {"path": "<데이터>/bank_train"}                           // 3절 학습 데이터
    ],
    "benchmark": ["<데이터>/bench"],                   // 평가 (업무). OCR 평가는 아래 ocr_images 가 더함
    "ocr_images": {                                    // 2절 실서류 OCR: ocr 단계가 OCR·준비해서 학습·평가에 넣음
      "folders": ["<이미지>"],                          // 하위 폴더 하나 = 문서 하나. 평가만: {"path": …, "split": "benchmark"}
      "ocr": {"revision": "ocr-api-2026-10", "base_url": "http://localhost:30107"},  // 사내 OCR 버전(캐시 열쇠)·주소
      "count": 20000                                   // 학습에 쓸 OCR SFT 문항 수
    },
    "output_dir": "../data/mixed-exp1",              // 섞은 결과 (<코드>/train/data/mixed-exp1). 이미 있으면 새 이름
    "task_mix": {…},                                 // 적힌 과제만 sft_max_examples 안에서 그 비율, 나머지는 있는 만큼
    …
  },
  "sft":  {"config": "sft.yaml"},                    // 40GB: sft_a100_40g_x2.yaml
  "grpo": {"config": "grpo_a100x2.yaml", …}          // 40GB: grpo_a100_40g_x2.yaml
}
```

- **OCR 데이터:** `ocr_images`가 이미지 폴더를 OCR해 `<data.output_dir>-ocr/`(예: `train/data/mixed-exp1-ocr`)에 준비하고, 학습(`count`개)·평가(문서 10%를 뗌, `"benchmark": false`면 안 넣음)에 저절로 넣습니다. OCR 결과 JSON을 이미 가졌으면 폴더마다 `"ocr_dir"`(이미지와 같은 이름 `.json`), 문서를 파일 이름으로 묶으려면 `"documents": "(?P<document_id>[^/]+)_p[0-9]+\\.[^.]+$"`, 그림 하나가 문서 하나면 `"page"`. 준비 세부값(보기 수·과제 수·필터)은 `"prepare": {…}`로 `docgen/bench/ocr_config.example.json` 값을 덮습니다. 이미 만든 OCR 데이터셋(studio·합성 OCR)은 `data.train`(개수는 `count`)과 `data.benchmark`에 함께 적습니다. OCR을 빼려면 `ocr_images`를 지웁니다.
- **상대 경로의 기준:** `workdir`, `data.*`, yaml 설정 이름은 설정 파일 폴더(`<코드>/train/configs`) 기준입니다. `model`만은 실행한 폴더(`<코드>`) 기준이라 절대 경로를 권합니다.
- **잘못된 경로:** 경로가 틀리면 실행하자마자 어떤 키가 틀렸는지 한꺼번에 알려 주고 멈춥니다.
- studio ⑥의 "학습 설정 내보내기"를 쓰면 이 칸이 채워진 `train/configs/studio-<이름>.json`과 실행할 명령을 받습니다([studio/TRAINING.md](../studio/TRAINING.md)).

### 4-2. 리허설 → 본 실행

```bash
# 리허설: 학습 5 step, 작은 평가. 명령·메모리·서버 기동을 짧게 확인 (결과는 train/runs/exp1/smoke)
python -m train --config train/configs/pipeline.json --smoke

# 본 실행: 백그라운드로. 터미널을 닫아도 계속
nohup python -m train --config train/configs/pipeline.json > pipeline.log 2>&1 &
tail -f pipeline.log            # 진행 보기 (Ctrl+C 는 보기만 종료)
```

단계: `ocr`(이미지 폴더 OCR·준비, `ocr_images`가 있을 때) → `prepare`(섞기) → `eval_base` → `sft` → `eval_sft` → `select` → `grpo` → `eval_grpo` → `report`.

**확인**
- 리허설 로그 끝에 `timings (h):`가 나오고, `train/runs/exp1/smoke/reports/benchmark.html`이 생기면 성공입니다.
- 본 실행은 A100 2장 기준 데이터 양에 따라 1~2일 걸립니다. 진행 단계는 `cat train/runs/exp1/state.json`의 `done`에서 봅니다.
- 중간에 멈추면 **같은 명령을 다시** 실행합니다. 끝난 단계는 건너뜁니다.

### 4-3. 결과 보기

위치는 `<코드>/train` 기준입니다.

| 무엇 | 위치 |
|---|---|
| 점수표 | `runs/exp1/reports/benchmark.html` (`.csv`, `.md`도). OCR·문서 이해·업무 과제가 한 표. 읽는 법: [results.md](results.md) |
| 학습한 모델 | `runs/exp1/merged/grpo-<버전>-checkpoint-<번호>` |
| 섞은 학습·평가 데이터 | `data/mixed-exp1/` (`train_sft.jsonl`, `benchmark_tasks.jsonl` …) |
| 문항별 답·점수 보기 | studio ⑥ 데이터셋(문항 탭)·⑦ 평가에 `runs/exp1/`을 모델 답으로 붙임 (GPU 불필요) |

studio는 docgen 도커에서 띄웁니다([docker/README.md 4절](../docker/README.md#4-studio-띄우기-같은-컨테이너)). 문항 그림·박스·모델 답·점수를 모든 과제에 대해 같은 화면에서 봅니다. 모델에게 직접 물을 때의 질문 문장은 [questions.md](questions.md)에 있습니다.

---

## 5. 다시 돌릴 때

| 하고 싶은 것 | 명령 |
|---|---|
| 멈춘 곳부터 이어서 | 같은 명령 그대로 (`<코드>`에서) |
| GRPO 설정만 바꿔 다시 | `--from grpo` (비교표에 줄이 추가됨) |
| SFT부터 다시 | `--from sft` |
| 비교표만 다시 | `--only report` |
| 실행할 명령만 보기 | `--dry-run` |
| 완전히 새 실험 | 설정의 `workdir`을 새 이름으로 (예: `../runs/exp2`) |
| 데이터 구성을 바꿈 | `data.output_dir`을 새 이름으로 (OCR 준비 폴더도 `<새 이름>-ocr`로 새로 만들어짐, OCR 캐시는 그대로 씀) |
| 생성기(docgen) 코드가 바뀜 | 아래 [5-1](#5-1-생성기가-바뀌었을-때-예-평가-세트-12) 순서대로 |

### 5-1. 생성기가 바뀌었을 때 (예: 평가 세트 1.2)

> 평가 세트 2.0(kie·marks 답에 위치)도 같은 순서입니다. 아래의 `1.2`를 `2.0`으로 바꿔 읽으세요.

평가 세트 1.2부터 하나은행 원본 서식의 결재란(담당·책임자·본인확인 등)에 직원 도장·서명이 찍힙니다. 1.1까지는 결재란이 항상 비어 있었습니다. 이런 식으로 생성기가 바뀌면 **은행 업무 데이터를 새로 만들고 학습을 처음부터** 다시 합니다. 실서류 OCR 데이터(2절)는 실제 이미지와 사내 OCR을 쓰므로 그대로 둡니다.

1. **코드 받기:** `git pull origin claude/ocr-banking-benchmark`
   - git이 안 되면 인터넷 PC에서 `sh docker/build.sh 1.2`로 만든 `docgen-code-1.2.tar.gz`를 반입해 같은 자리에 풉니다.
   - 도커 실행 환경 이미지는 다시 만들 필요 없습니다.
2. **은행 업무 데이터를 새 폴더에:** 컨테이너 안에서 `OUT=/out/v1.2 bash docgen/scripts/make_bank_data.sh` (약 1시간 15분)
   - `make_bank_data.sh`는 이미 만든 폴더(`meta.json` 있음)를 건너뜁니다. **기존 폴더에 그대로 돌리면 아무것도 바뀌지 않습니다.**
   - 다 되면 `<데이터>/v1.2/bench/meta.json`의 `"version"`이 `"1.2"`인지 확인합니다.
3. **설정 경로 바꾸기:** `<코드>/train/configs/pipeline.json`
   - `data.train`의 `<데이터>/bank_train` → `<데이터>/v1.2/bank_train`
   - `data.benchmark`의 `<데이터>/bench` → `<데이터>/v1.2/bench`
   - `data.output_dir` → 새 이름 (예: `../data/mixed-v1.2`)
   - `workdir` → 새 이름 (예: `../runs/exp2`)
   - OCR 데이터셋 경로는 그대로 둡니다.
4. **학습·평가:** [4-2](#4-2-리허설--본-실행)과 같이 리허설(`--smoke`) 후 본 실행합니다.
5. **점수 비교:** 1.1 세트의 점수와 1.2 세트의 점수는 직접 비교하지 않습니다. 옛 모델과 비교하려면 옛 모델도 1.2 세트로 다시 평가합니다.

**기존 데이터를 일부만 고쳐 쓰면 안 되나?** 바뀌는 범위는 서류 476종 중 원본 서식 154종과, 그 서식이 들어가는 업무 묶음(약 35%)입니다.
- 부분 교체로 아끼는 시간은 40~50분 정도입니다.
- 대신 문항 파일·학습 레코드·이미지·`meta.json`을 맞춰 바꿔 끼워야 하고, 어긋나면 옛 이미지와 새 정답이 섞인 세트가 조용히 만들어집니다.
- 그리고 데이터가 바뀌면 섞기와 학습은 어차피 다시 해야 합니다(1~2일, 전체에서 가장 큼).

그래서 부분 교체 도구는 두지 않고 새로 만듭니다.

---

## 자주 나는 에러

| 에러 메시지 / 증상 | 원인 | 해결 |
|---|---|---|
| `설정(…)의 경로를 확인하세요` | 설정의 경로가 없음 | 메시지에 나온 키를 서버의 절대 경로로 고침 |
| `과제 폴더(meta.json + tasks/)가 아닙니다` | `data.train`·`data.benchmark`가 데이터셋 폴더가 아님 (예: OCR 준비의 `manifest.jsonl`, 그 위 폴더) | `meta.json`이 있는 폴더로 고침 (OCR은 준비의 `output_dir`, 합성 OCR은 `<폴더>/prepared`) |
| `CUDA out of memory` (SFT/GRPO) | 80GB 설정을 40GB에서 씀 | `sft.config`, `grpo.config`를 `*_a100_40g_x2.yaml`로 (`train/configs/`) |
| `Multiple possible model types found` | 모델 종류 자동 판별 실패 | 설정의 `model_type`이 `qwen3_5`인지 확인 |
| `Output already exists` / `already prepared` | OCR 준비·섞기 결과 폴더가 이미 있음 | `output_dir`을 새 이름으로 (지우지 말고) |
| `Reference answers do not score 1.0` | 데이터를 만든 docgen 코드와 지금 코드가 다름 | 같은 코드로 데이터를 다시 만들기 (`make_bank_data.sh`) |
| `training rows share a customer or document with the benchmark` | 학습 데이터를 `--split train` 없이 만듦, 또는 평가 세트를 `data.train`에도 넣음 | `make_bank_data.sh`로 다시 만들기, `data.train` 확인 |
| `Server on port … exited` / `not ready in time` | 평가 서버(vLLM)가 안 뜸: GPU가 다른 작업에 쓰이는 중, 또는 vLLM 옵션 | 에러에 나온 로그 파일(`logs/<단계>-server0.log`) 마지막 줄 확인, `nvidia-smi` |
| `Port … is already in use` | 예전 평가 서버가 그 포트를 쓰는 중 | 그 프로세스를 끄거나 설정의 `eval.port_base`를 바꿈 |
| `ocr` 단계에서 `Error: 500`, 연결 실패 | 사내 OCR 서버가 꺼졌거나 주소가 다름 | 2-2의 서버(`/share/mond/ocr_api/server.py`)가 떠 있는지, `ocr_images.ocr.base_url`(또는 `INTERNAL_OCR_BASE_URL`)의 포트가 `SERVER_PORT`와 같은지 확인 (로그 `logs/ocr.log`) |
| `Regex must match a named document_id group` | `ocr_images.documents` 정규식이 어떤 그림 경로에 안 맞음 | 메시지의 경로를 보고 정규식 고침, 또는 `"folder"`(하위 폴더 = 문서) |
| `has an EXIF rotation; saved OCR coordinates are ambiguous` | 회전 정보가 있는 이미지에 미리 만든 OCR JSON | 그 폴더는 `ocr_dir` 없이 OCR 서버로 다시 |
| `이 docgen 코드에는 --split train 이 없습니다` | 도커에 옛 코드 | 최신 코드로 바꾸기 |
| 로그를 더 보고 싶음 | — | 설정의 `workdir` 아래 `logs/`에 단계별 로그 (기본 `<코드>/train/runs/exp1/logs/`) |

해결이 안 되면 에러 직전의 `(log: logs/….log)` 파일 마지막 20줄을 같이 공유해 주세요.
