# 처음부터 따라하기

이 저장소만으로 **OCR 학습 → 은행 업무 학습 → 결과 확인**까지 하는 방법을 순서대로 적었습니다. 단계마다 "확인" 항목이 있으니, 확인이 통과한 뒤 다음 단계로 넘어가세요. 막히면 맨 아래 [자주 나는 에러](#자주-나는-에러)를 보세요.

- 프로젝트가 무엇인지 먼저 보려면: [overview.md](overview.md)
- 이미 OCR 학습을 끝냈다면: [3. 은행 업무 학습](#3-은행-업무-학습)부터
- 각 과제의 실제 데이터(질문·정답·필드)를 보려면: [tasks.md](tasks.md)

## 0. 전체 그림: 어디서 무엇을 하나

| 어디서 | 무엇을 | 필요한 것 |
|---|---|---|
| **GPU 서버** (내부망, 학습 환경) | 사내 OCR 서버, OCR 학습, 은행 업무 학습, 평가, viewer | A100 2장 이상, ms-swift 4.x + vLLM이 설치된 파이썬 환경, Qwen3.5-9B 모델 파일 |
| **docgen 도커 컨테이너** (CPU) | 은행 업무용 합성 데이터 만들기 | docgen 도커 이미지 ([docs/DOCKER.md](../docs/DOCKER.md)) |

```text
1부  [GPU 서버]  실제 서류 이미지 ─(사내 OCR)→ manifest ─→ run_pipeline.py      ─→ OCR 모델
2부  [도커]      make_bank_data.sh ─→ bench/, bank_train/
     [GPU 서버]  OCR 모델 + 위 두 폴더 ─→ run_bank_pipeline.py                  ─→ 은행 업무 모델 + 비교표
```

이 문서의 경로 표기:

| 표기 | 뜻 | 예 |
|---|---|---|
| `<코드>` | 이 저장소를 받은 폴더 | `/share/<계정>/document_gen` |
| `<데이터>` | 도커 컨테이너의 `/out`과 연결한 서버 폴더 | `/share/<계정>/docgen_data` |
| `<모델>` | 원래 Qwen3.5-9B 모델 폴더 | `/share/cv_share/qwen3.5/9b` |

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
  docgen/            합성 서류 생성기 (2부 데이터)
  scripts/           make_bank_data.sh (2부 데이터 만들기)
  guide/             사용 가이드 (이 문서)
  training/          GPU 학습 프로젝트 — 1부와 2부 모두 여기서 실행
    run_pipeline.py        1부 OCR 학습
    run_bank_pipeline.py   2부 은행 업무 학습
    configs/               설정 예제
    viewer/                결과 보는 화면
```

### 1-2. 학습 환경에 설치

GPU 서버의 학습용 파이썬 환경(ms-swift가 깔린 가상환경)에서:

```bash
cd <코드>/training
pip install --no-index --no-build-isolation -e '.[ocr]'
```

- 인터넷이 없으면 `--find-links <wheel 폴더>`를 붙입니다.
- `[ocr]`는 사내 OCR 서버를 부를 때 쓰는 `requests`입니다.

**확인**
```bash
python -c "import swift, vllm, bank_ocr, bank_task; print('ok')"     # ok 가 나와야 함
swift --help | head -3                                              # 도움말이 나와야 함
ls <모델>/config.json                                               # 모델 파일이 있어야 함
nvidia-smi                                                          # 쓸 GPU가 비어 있는지
```

---

## 2. OCR 학습 (1부)

실제 서류 이미지를 사내 OCR에 돌린 결과를 정답으로, 글자와 위치를 읽는 법을 학습합니다. 자세한 설계는 [training/docs/DESIGN.md](../training/docs/DESIGN.md)에 있습니다.

### 2-1. 이미지 모으기

페이지 이미지(PNG/JPG)를 한 폴더에 둡니다.
- PDF는 쪽별 이미지로 먼저 바꿉니다.
- **같은 문서의 쪽들은 파일 이름으로 묶을 수 있어야 합니다.** 예: `doc123_p001.png`, `doc123_p002.png` → 문서 ID `doc123`. 학습과 평가를 문서 단위로 나누기 때문입니다.

### 2-2. 사내 OCR 서버 띄우기

OCR 결과 JSON을 이미 갖고 있으면 이 단계는 건너뜁니다(2-3에서 `--ocr-dir`를 씁니다).

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

### 2-3. 이미지 목록(manifest) 만들기

```bash
cd <코드>/training
python -m bank_ocr scan --root /share/data/images --split train \
  --document-regex '(?P<document_id>[^/]+)_p[0-9]+\.[^.]+$' \
  --out data/manifest.jsonl
# OCR JSON을 미리 만들어 뒀다면 --ocr-dir /share/data/ocr_json 추가 (이미지와 같은 이름, 확장자만 .json)
```

- `--document-regex`는 파일 이름에서 문서 ID를 뽑는 규칙입니다. 이름 규칙이 다르면 고칩니다.
- 문서마다 폴더가 따로 있으면 `'^(?P<document_id>[^/]+)/'`를 씁니다.

**확인**
```bash
wc -l data/manifest.jsonl          # 이미지 수와 같아야 함
head -2 data/manifest.jsonl        # document_id 가 문서별로 맞게 뽑혔는지
```

### 2-4. 설정 파일 두 개

```bash
cp config.example.json config.json
cp configs/pipeline.example.json configs/pipeline.json
```

`config.json` (데이터 준비 설정)에서 바꿀 것:

| 키 | 값 |
|---|---|
| `manifest` | `data/manifest.jsonl` (2-3에서 만든 파일) |
| `output_dir` | `data/prepared-v2` (이미 있으면 새 이름) |
| `ocr_revision` | 사내 OCR 버전을 알아볼 이름. 예: `ocr-api-2026-10`. OCR을 바꾸면 이 값도 바꿉니다 |
| `benchmark_fraction` | `0.1` 그대로 두면 문서 10%를 벤치마크로 뗍니다 |

`configs/pipeline.json` (학습 설정)에서 바꿀 것:

| 키 | 값 |
|---|---|
| `model` | `<모델>` |
| `gpus` | 쓸 GPU 번호. 예: `[5, 6]`. OCR 서버 GPU와 겹치지 않게 |
| `grpo.config` | A100 80GB면 `grpo_a100x2.yaml`, 40GB면 `grpo_a100_40g_x2.yaml` |

설정 파일 안의 상대 경로는 **그 설정 파일이 있는 폴더 기준**입니다.

### 2-5. 리허설 → 본 실행

```bash
# 리허설: 학습 5 step, 평가 60문항. 명령·메모리·서버 기동을 짧게 확인 (결과는 runs/exp1/smoke)
python run_pipeline.py --config configs/pipeline.json --smoke

# 본 실행: 백그라운드로. 터미널을 닫아도 계속
nohup python run_pipeline.py --config configs/pipeline.json > pipeline.log 2>&1 &
tail -f pipeline.log            # 진행 보기 (Ctrl+C 는 보기만 종료)
```

**확인**
- 리허설 로그 끝에 `timings (h):`가 나오고, `runs/exp1/smoke/reports/benchmark.html`이 생기면 성공입니다.
- 본 실행은 이미지 1000장 기준 약 16~23시간 걸립니다. 진행 단계는 `cat runs/exp1/state.json`의 `done`에서 봅니다.
- 중간에 멈추면 **같은 명령을 다시** 실행합니다. 끝난 단계는 건너뜁니다.

### 2-6. 결과

| 무엇 | 위치 |
|---|---|
| 점수표 | `runs/exp1/reports/benchmark.html` (Base·SFT·GRPO, 깨끗한/노이즈 이미지별) |
| **2부의 출발 모델** | `runs/exp1/merged/grpo-<버전>-checkpoint-<번호>` (폴더 전체 경로를 적어 둡니다) |
| OCR 학습 데이터 (2부에서 섞어 씀) | `data/prepared-v2/train_sft.jsonl`, `data/prepared-v2/benchmark_tasks.jsonl` |
| 눈으로 보기 | `bash viewer/start.sh runs/exp1/merged/<모델폴더> 1` → `http://localhost:7860` |

---

## 3. 은행 업무 학습 (2부)

1부 모델에서 출발해 합성 서류로 은행 업무를 학습합니다.

### 3-1. 합성 데이터 만들기 (docgen 도커, 한 번)

도커 컨테이너가 아직 없으면 [docs/DOCKER.md](../docs/DOCKER.md)대로 띄웁니다. 이때 `-v <데이터>:/out`으로 연결한 서버 폴더에 결과가 생깁니다.

```bash
ssh -p 2222 docgen@<서버IP>                 # 컨테이너 접속 (접속하면 코드 폴더에서 시작)
bash scripts/make_bank_data.sh              # 백그라운드로 시작. SSH를 끊어도 계속
tail -f /out/logs/make_bank_data.log        # "전부 완료" 가 나오면 끝 (약 1시간 15분)
```

SSH 대신 서버 터미널에서 바로: `docker exec -u docgen docgen bash -lc 'bash ~/document_gen/scripts/make_bank_data.sh'`

**확인** (서버에서)
```bash
ls <데이터>/bench/meta.json <데이터>/bank_train/meta.json     # 둘 다 있어야 함
du -sh <데이터>/bench <데이터>/bank_train                       # 약 3GB, 약 16GB
```

### 3-2. 설정 파일

```bash
cd <코드>/training
cp configs/bank_pipeline.example.json configs/bank_pipeline.json
```

`configs/bank_pipeline.json`에서 바꿀 것 (경로는 모두 **서버의 절대 경로**):

```jsonc
{
  "workdir": "../runs/bank1",                        // 결과 폴더. 그대로 둬도 됨
  "model": "<코드>/training/runs/exp1/merged/grpo-…-checkpoint-…",   // 2-6의 출발 모델
  "gpus": [5, 6],
  "data": {
    "docgen_root": "../..",                          // 그대로 (이 저장소의 docgen/)
    "train": ["<데이터>/bank_train"],                 // 3-1에서 만든 학습 데이터
    "benchmark": "<데이터>/bench",                    // 3-1에서 만든 평가 세트
    "replay": {"path": "<OCR 학습 폴더>/data/prepared-v2/train_sft.jsonl", "count": 3000},
    "output_dir": "../data/prepared-bank",           // 이미 있으면 새 이름
    …
  },
  "sft":  {"config": "bank_sft.yaml"},               // 40GB: bank_sft_a100_40g_x2.yaml
  "grpo": {"config": "bank_grpo_a100x2.yaml", …},    // 40GB: bank_grpo_a100_40g_x2.yaml
  "ocr_check": {"tasks": "<OCR 학습 폴더>/data/prepared-v2/benchmark_tasks.jsonl", "rows": 1000}
}
```

- **`replay`, `ocr_check`:** 1부를 돌린 폴더의 파일입니다. OCR 데이터를 섞지 않거나 OCR 유지 확인을 안 하려면 각각 `null`로 둡니다.
- **잘못된 경로:** 경로가 틀리면 실행하자마자 어떤 키가 틀렸는지 한꺼번에 알려 주고 멈춥니다.

### 3-3. 리허설 → 본 실행

```bash
python run_bank_pipeline.py --config configs/bank_pipeline.json --smoke     # 학습 5 step, 과제마다 8문항
nohup python run_bank_pipeline.py --config configs/bank_pipeline.json > bank_pipeline.log 2>&1 &
tail -f bank_pipeline.log
```

**확인**
- 리허설이 `runs/bank1/smoke/reports/benchmark.html`까지 만들면 성공입니다.
- 본 실행은 A100 2장 기준 약 1~1.5일 걸립니다. 진행은 `cat runs/bank1/state.json`에서 봅니다.
- 멈추면 같은 명령을 다시 실행합니다.

### 3-4. 결과 보기

| 무엇 | 위치 |
|---|---|
| 점수표 | `runs/bank1/reports/benchmark.html` — 읽는 법: [results.md](results.md) |
| OCR 능력 유지 | `runs/bank1/reports/ocr_retention.html` |
| 문항별 답 보기 (GPU 불필요) | `bash viewer/bank_start.sh` → `http://localhost:7861` |
| 내 서류로 물어보기 | `bash viewer/bank_start.sh runs/bank1/merged/<모델폴더> <GPU>` → 직접 테스트 탭 |

**브라우저 연결:** viewer는 서버 안에서 열리므로 내 PC 브라우저로 보려면 포트를 연결합니다.
- VS Code: 아래 PORTS 탭에서 `7861`을 Forward
- MobaXterm: Tunneling에서 7861 → 서버 127.0.0.1:7861

모델에게 직접 물을 때의 질문 문장은 [questions.md](questions.md)에 있습니다.

---

## 4. 다시 돌릴 때

| 하고 싶은 것 | 명령 |
|---|---|
| 멈춘 곳부터 이어서 | 같은 명령 그대로 |
| GRPO 설정만 바꿔 다시 | `--from grpo` (비교표에 줄이 추가됨) |
| SFT부터 다시 | `--from sft` |
| 비교표만 다시 | `--only report` |
| 실행할 명령만 보기 | `--dry-run` |
| 완전히 새 실험 | 설정의 `workdir`을 새 이름으로 (예: `../runs/bank2`) |
| 데이터 준비 설정을 바꿈 | `output_dir`(1부는 `config.json`, 2부는 `data.output_dir`)을 새 이름으로 |

---

## 자주 나는 에러

| 에러 메시지 / 증상 | 원인 | 해결 |
|---|---|---|
| `설정(…)의 경로를 확인하세요` | 설정의 경로가 없음 | 메시지에 나온 키를 서버의 절대 경로로 고침 |
| `FileNotFoundError: …/prepared-v2/train_sft.jsonl` | `replay`·`ocr_check` 경로가 1부 폴더를 가리키지 않음 | 1부를 돌린 폴더의 `data/prepared-v2/`로 고치거나 `null` |
| `CUDA out of memory` (2부 SFT/GRPO) | 80GB 설정을 40GB에서 씀 | `sft.config`, `grpo.config`를 `*_a100_40g_x2.yaml`로 ([BANK_TASKS.md](../training/BANK_TASKS.md) GPU별 설정) |
| `Multiple possible model types found` | 모델 종류 자동 판별 실패 | 설정의 `model_type`이 `qwen3_5`인지 확인 |
| `Output already exists` / `already prepared` | 데이터 준비 폴더가 이미 있음 | `output_dir`을 새 이름으로 (지우지 말고) |
| `Reference answers do not score 1.0` | 데이터를 만든 docgen 코드와 지금 코드가 다름 | 같은 코드로 데이터를 다시 만들기 (`make_bank_data.sh`) |
| `training rows share a customer with the benchmark` | 학습 데이터를 `--split train` 없이 만듦 | `make_bank_data.sh`로 다시 만들기 |
| `Server on port … exited` / `not ready in time` | 평가 서버(vLLM)가 안 뜸: GPU가 다른 작업에 쓰이는 중, 또는 vLLM 옵션 | 에러에 나온 로그 파일(`logs/<단계>-server0.log`) 마지막 줄 확인, `nvidia-smi` |
| `Port … is already in use` | 예전 평가 서버나 viewer가 그 포트를 쓰는 중 | 그 프로세스를 끄거나 설정의 `eval.port_base`를 바꿈 |
| prepare에서 OCR `Error: 500`, 연결 실패 | 사내 OCR 서버가 꺼졌거나 주소가 다름 | 2-2의 서버(`/share/mond/ocr_api/server.py`)가 떠 있는지, `INTERNAL_OCR_BASE_URL`의 포트가 `SERVER_PORT`와 같은지 확인 |
| `has an EXIF rotation; saved OCR coordinates are ambiguous` | 회전 정보가 있는 이미지에 미리 만든 OCR JSON | 그 이미지는 `--ocr-dir` 없이 OCR 서버로 다시 |
| `이 docgen 코드에는 --split train 이 없습니다` | 도커에 옛 코드 | 최신 코드로 바꾸기 |
| 로그를 더 보고 싶음 | — | `runs/<workdir>/logs/` 에 단계별 로그 |

해결이 안 되면 에러 직전의 `(log: logs/….log)` 파일 마지막 20줄을 같이 공유해 주세요.
