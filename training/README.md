# OCR 학습 파이프라인 (Qwen3.5-9B)

실제 서류 이미지와 내부 OCR 결과로 **글자 내용과 위치(박스)** 읽기를 학습합니다. SFT → GRPO 순서이며, 학습 전후를 같은 벤치마크로 비교합니다.

- **정답:** 내부 OCR 결과를 그대로 정답으로 씁니다(사람 검수 없음). 그래서 점수는 실제 정답률이 아니라 **내부 OCR과 얼마나 같은지**입니다.
- **검증 범위:** 데이터 처리·평가·보상은 로컬에서 검증했습니다. 실제 내부 OCR 호출과 GPU 학습은 서버에서 처음 돌립니다. 그래서 본 실행 전에 `--smoke` 리허설을 하세요.

**다음 단계(은행 업무):** 이 OCR 모델에서 출발해 서류 구비 확인·서류 대조·심사 질의·정보 추출을 학습합니다. → [BANK_TASKS.md](BANK_TASKS.md)

## 흐름

```text
이미지 + OCR JSON → prepare → Base 평가 → SFT → SFT 평가 → GRPO 문제 선정 → GRPO → GRPO 평가 → 비교표
                    └──────────────────── run_pipeline.py 한 명령 ────────────────────┘
```

## 실행

```bash
# 0) 설치 (한 번)
python -m pip install --no-index --find-links /share/wheelhouse --no-build-isolation -e .

# 1) 이미지 목록 만들기. --ocr-dir: 이미 돌려 둔 OCR JSON 폴더
python -m bank_ocr scan --root /share/data/images --split train \
  --document-regex '(?P<document_id>[^/]+)_p[0-9]+\.[^.]+$' \
  --ocr-dir /share/data/ocr_json --out data/manifest.jsonl

# 2) 설정 복사 → model 경로, gpus 확인
cp config.example.json config.json
cp configs/pipeline.example.json configs/pipeline.json

# 3) 리허설 (학습 5 step, 평가 60문항) → 본 실행
python run_pipeline.py --config configs/pipeline.json --smoke
nohup python run_pipeline.py --config configs/pipeline.json > pipeline.log 2>&1 &
```

- **멈췄을 때:** 같은 명령을 다시 실행하면 끝난 단계는 건너뜁니다.
- **일부만 다시:** `--from grpo`는 그 단계부터, `--only report`는 한 단계만 실행합니다. `--dry-run`은 실행할 명령만 보여 줍니다.
- **40GB GPU:** `pipeline.json`의 `grpo.config`를 `grpo_a100_40g_x2.yaml`로 바꿉니다.
- **예상 시간:** A100 80GB 2장, 이미지 1000장 기준 약 16~23시간입니다.

## 결과

| 파일 | 내용 |
|---|---|
| `runs/exp1/reports/benchmark.html` | Base·SFT·GRPO 점수표와 Base 대비 변화. 깨끗한 이미지와 노이즈 이미지를 따로 보여 줍니다 |
| `runs/exp1/merged/` | 평가에 쓴 병합 모델 (다음 단계인 은행 업무 학습의 출발 모델) |
| `runs/exp1/state.json` | 단계별 완료 여부와 걸린 시간 |

**눈으로 확인:** `bash viewer/start.sh runs/exp1/merged/<모델폴더> 1`을 실행하고 브라우저에서 `http://localhost:7860`을 엽니다. 이미지를 올려 질문하면 답의 박스가 이미지 위에 그려집니다. → [viewer/README.md](viewer/README.md)

## 자세한 문서

| 문서 | 내용 |
|---|---|
| [docs/SETUP.md](docs/SETUP.md) | 설치, 내부 OCR 연결, 이미지 목록 규칙, `config.json` 항목, 기존 프로젝트 업데이트 |
| [docs/PIPELINE.md](docs/PIPELINE.md) | `run_pipeline.py` 옵션, GRPO 문제 선정, GRPO만 다시 돌리기, 단계별 예상 시간 |
| [docs/DESIGN.md](docs/DESIGN.md) | 학습 과제 8종, 좌표 형식, 증강, 평가 지표, GRPO 보상 |
| [docs/MANUAL.md](docs/MANUAL.md) | 파이프라인 없이 한 단계씩 직접 실행하는 명령, 로컬 테스트 |
