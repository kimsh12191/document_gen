# document_gen: 은행 서류 합성 데이터 + 은행 업무 학습

합성 은행 서류(476종)로 VLM에 은행 업무를 학습시키고, 학습 전후를 벤치마크로 비교합니다. 출발 모델은 OCR 학습 단계([training/README.md](training/README.md))의 결과입니다.

배우는 은행 업무는 네 가지입니다.

| 업무 | 내용 |
|---|---|
| 서류 구비 확인 | 제출된 서류 묶음에서 빠진 서류, 불필요한 서류, 다른 사람 서류 찾기 |
| 서류 대조 | 서류 2~3건을 맞대어 불일치 찾기 (오기, 금액·날짜 안 맞음, 임대인≠소유자 등 14종) |
| 심사 질의 | LTV, 소득 대비 배수, 서류 유효기간 같은 질문에 숫자나 예/아니오로 답하기 |
| 정보 추출 | 서류에서 항목 값 뽑기 |

여기에 분류, 체크·도장·서명, 글자 읽기도 함께 배웁니다.

```text
1. 데이터 만들기  docgen 도커 (CPU, 한 번만)  →  bank_train/ (학습)   bench/ (평가)
2. 파이프라인     GPU 서버 (한 명령)          →  prepare → eval_base → sft → eval_sft → select → grpo → eval_grpo → report
3. 결과 보기      비교표 + viewer
```

## 1. 데이터 만들기 (docgen 도커, 한 번만)

한 번 만들어 두면 학습을 몇 번 다시 하든 다시 만들 필요가 없어서 파이프라인에서 뺐습니다.

```bash
ssh -p 2222 docgen@<서버IP>              # docgen 컨테이너 접속
bash scripts/make_bank_data.sh           # 백그라운드 실행. SSH 를 끊어도 계속됩니다
tail -f /out/logs/make_bank_data.log     # "전부 완료" 가 나오면 끝
```

| 만드는 것 (서버 `~/docgen/data/`) | 내용 | 시간 (8코어) |
|---|---|---|
| `bench/` | 평가 세트: 서류 476종 × 1건 + 업무 12종 × 고객 40명의 서류 묶음 | 약 15분 |
| `bank_train/` | 학습 데이터: 서류 476종 × 5건 + 업무 12종 × 고객 200명 | 약 1시간 |

- 두 폴더는 서로 다른 고객으로 만들어서 겹치지 않습니다.
- 양을 바꾸려면 `TRAIN_BUNDLES=300 BENCH_BUNDLES=60 bash scripts/make_bank_data.sh`처럼 앞에 붙입니다.

## 2. 파이프라인 돌리기 (GPU 서버)

**준비물**
- OCR 단계 결과 모델 폴더 (`runs/exp1/merged/grpo-…`)
- 1에서 만든 두 폴더
- A100 2장 (80GB 기준. 40GB면 `grpo.config`를 `bank_grpo_a100_40g_x2.yaml`로 바꿉니다)

```bash
cd training
pip install --no-index --no-build-isolation -e .                    # 한 번
cp configs/bank_pipeline.example.json configs/bank_pipeline.json
#   model           OCR 단계 결과 모델 폴더
#   gpus            사용할 GPU (예: [0, 1])
#   data.train      ["/home/<계정>/docgen/data/bank_train"]
#   data.benchmark  "/home/<계정>/docgen/data/bench"
#   data.replay.path, ocr_check.tasks   OCR 단계 데이터(prepared-v2) 경로. 없으면 data.replay, ocr_check 를 null 로

python run_bank_pipeline.py --config configs/bank_pipeline.json --smoke                          # 리허설
nohup python run_bank_pipeline.py --config configs/bank_pipeline.json > bank_pipeline.log 2>&1 &   # 본 실행
tail -f bank_pipeline.log
```

- **리허설(`--smoke`):** 학습 5 step, 과제마다 8문항 평가, GRPO 8문제로 명령·메모리·서버 기동을 먼저 확인합니다.
- **멈췄을 때:** 같은 명령을 다시 실행하면 끝난 단계는 건너뜁니다. 진행 상태는 `runs/bank1/state.json`에 남습니다.
- **일부만 다시:**
  - `--from grpo`: 그 단계부터 다시 실행합니다.
  - `--only report`: 그 단계 하나만 실행합니다.
  - `--dry-run`: 실행할 명령만 보여 줍니다.

## 3. 단계별로 하는 일

| 단계 | 하는 일 | 만드는 것 | 시간 (추정) |
|---|---|---|---|
| `prepare` | docgen 데이터를 학습 형식으로 바꿉니다. 아래 표에 자세히 적었습니다. | `data/prepared-bank/` | 10~30분 |
| `eval_base` | 출발(OCR) 모델을 GPU마다 서버로 띄워 평가 세트 약 9천 문항을 풀고 채점합니다. OCR 벤치마크 1000문항도 같이 풉니다. 학습 전 기준점입니다. | `reports/start.json` | 1~1.5시간 |
| `sft` | 출발 모델에 LoRA를 붙여 약 2만 문항을 1 epoch 학습합니다. | `sft/…/checkpoint-*` | 10~15시간 |
| `eval_sft` | SFT 모델을 병합해 채점합니다. 같은 서버로 GRPO 후보 3000문제도 미리 풉니다. | `merged/sft-*`, `reports/sft.json` | 1~1.5시간 |
| `select` | 후보 중 SFT가 틀린 문제를 절반 섞어 GRPO 문제 1000개를 고릅니다. 고르는 과제는 서류 대조, 심사 질의, 서류 구비 확인, 정보 추출이고, 문항당 이미지 4장 이하만 씁니다. | `grpo_train.jsonl` | 몇 초 |
| `grpo` | SFT에서 이어 GRPO를 합니다. 한 문제에 답을 8개(40GB 설정은 4개) 만들고, 평가 채점기 점수가 높은 답 쪽으로 학습합니다. | `grpo/…/checkpoint-*` | 4~12시간 |
| `eval_grpo` | GRPO 모델을 병합해 채점합니다. | `merged/grpo-*`, `reports/grpo.json` | 1~1.5시간 |
| `report` | 세 모델을 한 표로 비교합니다. | `reports/benchmark.html`, `reports/ocr_retention.html` | 몇 초 |

`prepare`가 하는 일은 다음과 같습니다.

| 작업 | 내용 |
|---|---|
| 이미지 줄이기 | 한 문항의 이미지 합이 정해진 크기(12000토큰)를 넘지 않게 줄입니다. |
| 문항 뽑기 | 과제 비율에 맞춰 SFT 문항 약 2만 개를 뽑습니다. |
| GRPO 몫 떼기 | 고객 20%는 SFT에서 빼서 GRPO용으로 둡니다. |
| OCR 데이터 섞기 | OCR 학습 데이터 3000개를 섞어 OCR 능력이 떨어지지 않게 합니다. |
| 검사 | 평가 세트와 학습 데이터가 겹치지 않는지, 채점기가 정답에 만점을 주는지 확인합니다. |

- 만드는 것은 모두 `training/runs/bank1/` 아래에 생깁니다. `prepare`의 결과만 `training/data/` 아래에 생깁니다.
- 합계는 약 1~1.5일입니다. 시간이 부족하면 `data.sft_max_examples`와 `grpo.count`를 줄입니다.

## 4. 결과 보기

- **비교표:** `runs/bank1/reports/benchmark.html`
  - 과제별 점수와 출발 모델 대비 변화를 보여 줍니다.
  - 불일치 종류별, 심사 질의 능력별로도 나눠 보여 줍니다.
- **OCR 유지:** `ocr_retention.html`에서 은행 업무를 배우는 동안 OCR 능력이 떨어지지 않았는지 봅니다.
- **viewer:** `training` 폴더에서 띄우고 브라우저에서 `http://localhost:7861`을 엽니다.
  ```bash
  bash viewer/bank_start.sh                                  # 저장된 답만 보기 (GPU 불필요, 학습 중에도 가능)
  bash viewer/bank_start.sh runs/bank1/merged/<모델폴더> 1     # + 내 서류 올려서 물어보기 (GPU 1번)
  ```
  - 문항마다 모델들의 답을 정답과 나란히 봅니다.
  - "SFT는 맞히고 출발 모델은 틀린 문제"처럼 좋아진 문제나 나빠진 문제만 골라 볼 수 있습니다.
  - 사용법은 [training/viewer/README.md](training/viewer/README.md) 6번에 있습니다.
- **해석할 때 주의:** 학습 데이터와 평가 세트는 같은 생성기로 만들어서 고객만 다릅니다. 그래서 점수가 크게 오르는 것은 당연합니다. 실제 서류로는 viewer에서 따로 확인하세요.

## 자세한 문서

| 문서 | 내용 |
|---|---|
| [training/BANK_TASKS.md](training/BANK_TASKS.md) | 은행 업무 파이프라인: 설정 항목 전체, GRPO 보상, 경로 표, 결과 해석 |
| [training/viewer/README.md](training/viewer/README.md) | viewer 사용법 |
| [training/README.md](training/README.md) | OCR 학습 단계 (출발 모델을 만드는 앞 단계) |
| [docs/BENCHMARK.md](docs/BENCHMARK.md) | 벤치마크 과제와 채점 방식 |
| [docs/DOCGEN.md](docs/DOCGEN.md) | 서류 생성기: 설치, 명령, 출력 형식, 서식 |
| [docs/DOCKER.md](docs/DOCKER.md) | docgen 도커 설치와 SSH 접속 |

**브랜치:** 이 브랜치(`claude/ocr-banking-benchmark`)에 전부 들어 있습니다. `training/`의 OCR 코드는 OCR 브랜치(`claude/bank-ocr-pipeline`)와 같습니다. OCR 쪽을 고치면 아래 명령으로 가져옵니다.

```bash
git merge -X subtree=training origin/claude/bank-ocr-pipeline
```

모든 데이터는 학습용 합성 데이터이며 실존 인물·사업자와 무관합니다.
