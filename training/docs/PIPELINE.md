# run_pipeline.py 자세히

기본 사용법은 [README](../README.md)에 있습니다. 여기는 옵션, 단계별 동작, GRPO 다시 돌리기, 예상 시간입니다.

## 옵션

| 옵션 | 의미 |
|---|---|
| `--smoke` | 학습 5 step, 벤치마크 60문항, GRPO 후보 40개. 별도 폴더(`workdir/smoke`) |
| `--from sft` | 그 단계부터 다시 실행 (예: SFT 설정을 바꿔 재학습). GRPO만 다시 하려면 `--from grpo` (아래 참고) |
| `--only eval_base` | 한 단계만 실행 |
| `--dry-run` | 실행할 명령만 출력 |

**저장된 OCR 사용 조건:** JSON은 내부 OCR 응답 그대로(`success`, `data.basicData`, `bounding.vertices`)여야 하고, OCR을 돌린 이미지와 같은 파일이어야 합니다. 이미지에 EXIF 회전 정보가 있으면 좌표 기준이 모호하므로 중단합니다(그 페이지는 OCR을 다시 돌려야 합니다). JSON이 없는 이미지가 있으면 scan이 중단됩니다. manifest에 `ocr_json`이 없는 행만 `ocr_callable`로 OCR을 호출합니다.

**빠른 평가 구성:** GPU마다 추론 서버(vLLM)를 하나씩 띄우고 요청을 나눠 보냅니다. 같은 이미지에 대한 질문은 같은 서버로 보내고 연달아 처리해서, 이미지 처리 결과(prefix cache)를 다시 씁니다. 서버당 동시 요청은 `concurrency_per_server`(기본 32, vLLM `--vllm_max_num_seqs` 64)입니다. SFT·GRPO 체크포인트는 평가 전에 `swift export --merge_lora`로 한 번 병합해 두 서버가 같은 병합 모델을 씁니다. SFT 평가 때 띄운 서버로 GRPO 후보 문제도 함께 풀어 둬서, 어려운 문제 선정에 서버를 다시 띄우지 않습니다.

**GRPO 데이터 선정:** `grpo.select`가 `mine`(기본)이면 `train_grpo.jsonl`에서 후보 6000개를 뽑아 SFT 모델로 풀고, 보상이 0.9 미만인 문제를 절반 섞어 2000개를 고릅니다. `random`은 무작위 2000개, `all`은 전체입니다. `grpo.tasks`(예: `["grounding","relation"]`)를 주면 데이터를 다시 만들지 않고 GRPO 후보를 그 과제로만 좁힙니다. 답이 긴 spotting을 빼면 GRPO가 크게 빨라집니다(`select: all`에는 적용되지 않음). 2장 구성용 `configs/grpo_a100x2.yaml`은 GPU당 4개 × 2장 = 8 = `num_generations`가 되도록 batch를 맞추고, 누적 4로 optimizer step마다 4문제를 씁니다. 메모리가 부족하면 파일 머리 주석대로 GPU당 2개·누적 2·`num_generations` 4로 되돌리세요. A100 40GB 2장이면 `grpo.config`를 `grpo_a100_40g_x2.yaml`(GPU당 2개 × 누적 4, `num_generations` 4)로 바꿉니다. step당 문제 수(4)와 step 수는 같고, 문제당 답이 4개라 학습 신호가 조금 약한 대신 step은 덜 무겁습니다.

**GRPO만 다시 돌리기:** SFT 결과는 그대로 두고 GRPO 설정만 바꿔 다시 학습·평가할 수 있습니다. 새 GRPO는 이전 GRPO가 아니라 SFT 체크포인트에서 다시 시작합니다. 비교표에는 GRPO 실행마다 한 줄씩(`GRPO v1-…-checkpoint-500` 형식) 쌓입니다.

| 바꾼 것 | 명령 |
|---|---|
| GRPO yaml만 (lr, beta, temperature, `num_generations` 등) | `--from grpo` |
| `grpo.count`, `grpo.hard_fraction`, `grpo.select` | `--from select` |
| `grpo.tasks`, `grpo.candidates` | `rm runs/exp1/grpo_candidates.jsonl runs/exp1/predictions/sft-grpo-candidates-*` 후 `--from eval_sft` (SFT 벤치마크 답은 저장된 것을 다시 쓰고, 서버 기동과 새 후보 풀이만 합니다) |

- yaml은 고쳐 쓰기보다 `configs/grpo_try2.yaml`처럼 복사해 고치고, `pipeline.json`의 `grpo.config`를 그 파일로 바꾸는 편이 기록이 남아 좋습니다. 각 실행에서 실제로 쓴 설정은 `runs/exp1/grpo/<버전>/args.json`에 남습니다.
- 실행별 점수는 `reports/grpo-<버전>-checkpoint-<번호>.json`에 따로 남고, `reports/grpo.json`은 가장 최근 실행입니다. 평가 답은 `predictions/grpo-<버전>-….jsonl`입니다.
- 비교표에서 어떤 실행을 빼려면 그 `reports/grpo-….json`을 다른 폴더로 옮기고 `--only report`를 실행합니다.
- 병합 모델이 실행마다 `merged/grpo-…`에 약 20GB씩 생깁니다. 디스크가 부족하면 다 쓴 폴더를 지웁니다.

**서버·병합 명령 바꾸기:** `eval.deploy_command`, `eval.merge_command`에 명령 목록을 넣으면 기본값을 대체합니다. `{model}`, `{model_type}`, `{port}`, `{adapter}`, `{output}`은 실행 시 채워집니다. 설치된 MS-SWIFT 버전에서 옵션 이름이 다르면 여기서 맞춥니다. 리허설(`--smoke`)이 이 명령들을 모두 한 번씩 실행해 봅니다.

## 2일 예상 (이미지 1000장, 문서 10% 벤치마크)

아래는 추정치입니다. 실제 값은 리허설과 첫 단계의 `timings`로 확인하세요.

| 단계 | 규모 | 예상 |
|---|---|---|
| 데이터 준비 | 1000장 × view 3장 (OCR 재호출 없음) | 0.5~1시간 |
| Base / SFT / GRPO 평가 | 각 약 4~5천 문항, 서버 2대 | 각 20~40분 (+서버 기동·병합 10~20분) |
| SFT | 최대 3만 문항, 문항당 약 3~4천 토큰 | 7~10시간 |
| GRPO 후보 풀이 | 6000문항 | 20~40분 |
| GRPO | 2000문제 × 생성 8개 = 500 step (step당 4문제) | step 시간 × 500 (step 45~90초면 6~12시간) |
| 합계 | | 약 16~23시간 |

시간이 부족하면 `config.json`의 `sft_max_examples`(예: 20000)와 `pipeline.json`의 `grpo.count`(예: 1000)를 먼저 줄이세요. 둘 다 학습 시간에 거의 비례합니다.
