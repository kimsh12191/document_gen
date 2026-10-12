# document_gen: 은행 서류 합성 데이터 + 은행 업무 학습

합성 은행 서류(476종)로 VLM에 은행 업무를 학습시키고, 학습 전후를 벤치마크로 비교합니다. 출발 모델은 OCR 학습 단계의 결과입니다.

```text
1. 데이터 생성   docgen 도커 (CPU, 한 번만)  →  bank_train/ (학습)  bench/ (평가)
2. 파이프라인    GPU 서버 (한 명령)          →  prepare → 출발 모델 평가 → SFT → 평가 → GRPO → 평가 → 비교표
3. viewer       GPU 서버                    →  문항별로 모델 답 보기, 내 서류 올려서 물어보기
```

## 1. 데이터 생성 (docgen 도커, 한 번만)

```bash
ssh -p 2222 docgen@<서버IP>              # docgen 컨테이너 접속
bash scripts/make_bank_data.sh           # 백그라운드 실행. SSH 를 끊어도 계속됩니다
tail -f /out/logs/make_bank_data.log     # "전부 완료" 가 나오면 끝
```

- **만들어지는 것:** 서버의 `~/docgen/data/` 아래에 두 폴더가 생깁니다. 두 폴더는 서로 다른 고객으로 만들어서 겹치지 않습니다.
  - `bench`: 평가용, 고객 40명, 약 15분
  - `bank_train`: 학습용, 고객 200명, 약 1시간
- **양 바꾸기:** `TRAIN_BUNDLES=300 BENCH_BUNDLES=60 bash scripts/make_bank_data.sh`처럼 앞에 붙입니다.

## 2. 파이프라인 (GPU 서버)

```bash
cd training
pip install --no-index --no-build-isolation -e .                    # 한 번
cp configs/bank_pipeline.example.json configs/bank_pipeline.json    # model, gpus, data 경로 수정
python run_bank_pipeline.py --config configs/bank_pipeline.json --smoke                        # 리허설
nohup python run_bank_pipeline.py --config configs/bank_pipeline.json > bank_pipeline.log 2>&1 &   # 본 실행
```

- **결과:** `training/runs/bank1/reports/benchmark.html`에 출발 모델·SFT·GRPO 점수와 변화가 나옵니다.
- **멈췄을 때:** 같은 명령을 다시 실행하면 끝난 단계는 건너뜁니다.
- **걸리는 시간:** A100 80GB 2장 기준 약 1~1.5일입니다.

## 3. viewer

```bash
cd training
bash viewer/bank_start.sh                                       # 저장된 답만 보기 (GPU 불필요)
bash viewer/bank_start.sh runs/bank1/merged/<모델폴더> 1          # + 내 서류 올려서 물어보기 (GPU 1번)
# 브라우저: http://localhost:7861
```

## 자세한 문서

| 문서 | 내용 |
|---|---|
| [training/BANK_TASKS.md](training/BANK_TASKS.md) | 은행 업무 파이프라인: 설정 항목, 단계별 내용, 시간, 결과 해석 |
| [training/viewer/README.md](training/viewer/README.md) | viewer 사용법 |
| [training/README.md](training/README.md) | OCR 학습 단계 (은행 업무의 출발 모델을 만드는 앞 단계) |
| [docs/BENCHMARK.md](docs/BENCHMARK.md) | 벤치마크 과제와 채점 방식 |
| [docs/DOCGEN.md](docs/DOCGEN.md) | 서류 생성기: 설치, 명령, 출력 형식, 서식 |
| [docs/DOCKER.md](docs/DOCKER.md) | docgen 도커 설치와 SSH 접속 |

**브랜치:** 이 브랜치(`claude/ocr-banking-benchmark`)에 전부 들어 있습니다. `training/`에는 OCR 브랜치(`claude/bank-ocr-pipeline`)와 같은 OCR 코드가 들어 있고, OCR 쪽을 고치면 아래 명령으로 가져옵니다.

```bash
git merge -X subtree=training origin/claude/bank-ocr-pipeline
```

모든 데이터는 학습용 합성 데이터이며 실존 인물·사업자와 무관합니다.
