# OCR 학습 파이프라인 (Qwen3.5-9B)

실제 서류 이미지와 내부 OCR 결과로 **글자 내용과 위치(박스)** 읽기를 학습합니다. 한 명령으로 데이터 준비부터 SFT, GRPO, 학습 전후 비교표까지 만듭니다.

- **정답:** 내부 OCR 결과를 그대로 정답으로 씁니다(사람 검수 없음). 그래서 점수는 실제 정답률이 아니라 **내부 OCR과 얼마나 같은지**입니다.
- **검증 범위:** 데이터 처리·평가·보상은 로컬에서 검증했습니다. 실제 GPU 학습은 서버에서 처음 돌리므로 본 실행 전에 `--smoke` 리허설을 하세요.

## 1. 파이프라인 돌리기

**준비물**
- 페이지 이미지와, 이미 돌려 둔 내부 OCR 결과 JSON
- 원래 모델 폴더 (`/share/cv_share/qwen3.5/9b`)
- A100 2장 (80GB 기준. 40GB면 아래 설정 하나를 바꿉니다)

```bash
# 0) 설치 (한 번)
python -m pip install --no-index --find-links /share/wheelhouse --no-build-isolation -e .

# 1) 이미지 목록 만들기. --ocr-dir: 이미 돌려 둔 OCR JSON 폴더
python -m bank_ocr scan --root /share/data/images --split train \
  --document-regex '(?P<document_id>[^/]+)_p[0-9]+\.[^.]+$' \
  --ocr-dir /share/data/ocr_json --out data/manifest.jsonl

# 2) 설정 복사 → configs/pipeline.json 의 model 경로, gpus 확인
cp config.example.json config.json
cp configs/pipeline.example.json configs/pipeline.json

# 3) 리허설 (학습 5 step, 평가 60문항) → 본 실행
python run_pipeline.py --config configs/pipeline.json --smoke
nohup python run_pipeline.py --config configs/pipeline.json > pipeline.log 2>&1 &
tail -f pipeline.log
```

- **멈췄을 때:** 같은 명령을 다시 실행하면 끝난 단계는 건너뜁니다. 진행 상태는 `runs/exp1/state.json`에 남습니다.
- **일부만 다시:**
  - `--from grpo`: 그 단계부터 다시 실행합니다.
  - `--only report`: 그 단계 하나만 실행합니다.
  - `--dry-run`: 실행할 명령만 보여 줍니다.
- **40GB GPU:** `configs/pipeline.json`의 `grpo.config`를 `grpo_a100_40g_x2.yaml`로 바꿉니다.

## 2. 단계별로 하는 일

| 단계 | 하는 일 | 만드는 것 | 시간 (추정) |
|---|---|---|---|
| `prepare` | 이미지를 모델 입력 크기(2300×1600 이하)로 줄이고, 페이지마다 깨끗한 사본 1장과 노이즈를 넣은 사본 2장을 만듭니다. OCR 결과로 8가지 과제의 문항을 만듭니다(글자 읽기, 박스 찾기, 영역 읽기, 전체 받아쓰기 등). 문서의 10%는 벤치마크로 떼어 둡니다. | `data/prepared-v2/` | 0.5~1시간 |
| `eval_base` | 원래 모델을 GPU마다 서버로 띄워 벤치마크(약 4~5천 문항)를 풀고 채점합니다. 학습 전 기준점입니다. | `reports/base.json` | 20~40분 |
| `sft` | 원래 모델에 LoRA를 붙여 최대 3만 문항을 학습합니다. | `sft/…/checkpoint-*` | 7~10시간 |
| `eval_sft` | SFT 모델을 병합해 벤치마크를 채점합니다. 같은 서버로 GRPO 후보 6000문제도 미리 풉니다. | `merged/sft-*`, `reports/sft.json` | 40~80분 |
| `select` | 후보 중 SFT가 틀린 문제를 절반 섞어 GRPO 문제 2000개를 고릅니다. 다 맞히는 문제로는 GRPO가 배울 게 없기 때문입니다. | `grpo_train.jsonl` | 몇 초 |
| `grpo` | SFT에서 이어 GRPO를 합니다. 한 문제에 답을 8개(40GB 설정은 4개) 만들고, 박스·글자가 OCR 정답과 잘 맞는 답 쪽으로 학습합니다. | `grpo/…/checkpoint-*` | 6~12시간 |
| `eval_grpo` | GRPO 모델을 병합해 벤치마크를 채점합니다. | `merged/grpo-*`, `reports/grpo.json` | 20~40분 |
| `report` | 세 모델을 한 표로 비교합니다. | `reports/benchmark.html` | 몇 초 |

- 만드는 것은 모두 `runs/exp1/` 아래에 생깁니다. `prepare`의 결과만 `data/` 아래에 생깁니다.
- 합계는 이미지 1000장 기준 약 16~23시간입니다.

## 3. 결과 보기

- **비교표:** `runs/exp1/reports/benchmark.html`
  - 과제별 점수와 Base 대비 변화를 보여 줍니다.
  - 같은 표를 깨끗한 이미지와 노이즈 이미지로 나눠서도 보여 줍니다. 둘의 차이가 노이즈에 얼마나 강한지를 뜻합니다.
- **viewer:** `bash viewer/start.sh runs/exp1/merged/<모델폴더> 1`을 실행하고 `http://localhost:7860`을 엽니다.
  - 이미지나 PDF를 올려 질문하면 답의 박스를 이미지 위에 그려 줍니다. → [viewer/README.md](viewer/README.md)
- **다음 단계:** `runs/exp1/merged/grpo-*` 폴더가 은행 업무 학습의 출발 모델이 됩니다. → [저장소 README](../README.md), [BANK_TASKS.md](BANK_TASKS.md)

## 자세한 문서

| 문서 | 내용 |
|---|---|
| [docs/SETUP.md](docs/SETUP.md) | 설치, 내부 OCR 연결, 이미지 목록 규칙, `config.json` 항목, 기존 프로젝트 업데이트 |
| [docs/PIPELINE.md](docs/PIPELINE.md) | 파이프라인 옵션, GRPO 문제 선정, GRPO만 다시 돌리기 |
| [docs/DESIGN.md](docs/DESIGN.md) | 학습 과제 8종, 좌표 형식, 노이즈 증강, 평가 지표, GRPO 보상 |
| [docs/MANUAL.md](docs/MANUAL.md) | 파이프라인 없이 한 단계씩 직접 실행하는 명령, 로컬 테스트 |
