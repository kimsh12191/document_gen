# train — 학습 하나 (OCR · 문서 이해 · 업무 처리)

studio 데이터셋(과제 폴더)을 섞어 SFT·GRPO 로 학습하고, 같은 평가 세트로 출발·SFT·GRPO 모델을 비교합니다. 예전의 1부 OCR(`ocr/`)·2부 은행 업무(`bank/`) 학습을 하나로 합친 것입니다 ([studio/DESIGN.md 17절](../studio/DESIGN.md)).

```bash
# 학습 컨테이너, 저장소 최상위에서
python -m train --config train/configs/<이름>.json --smoke     # 리허설: 5 step 학습, 과제마다 8문항 평가 (workdir/smoke)
python -m train --config train/configs/<이름>.json             # 전부
python -m train --config train/configs/<이름>.json --from grpo # GRPO 다시 (앞 GRPO 점수도 보고서에 남음)
python -m train --config train/configs/<이름>.json --dry-run   # 명령만 보기
```

설정은 studio ⑥ 데이터셋 › 학습 탭이 `train/configs/studio-<이름>.json` 으로 만들어 줍니다 ([studio/TRAINING.md](../studio/TRAINING.md)). 손으로 쓸 때는 [configs/pipeline.example.json](configs/pipeline.example.json) 을 복사합니다.

## 데이터: 과제 폴더 섞기

데이터셋은 모두 같은 형식입니다: `meta.json` + `tasks/<과제>.jsonl`, 문항 `{id, task, images, prompt, answer, eval, meta}`.

| 만드는 곳 | 과제 |
|---|---|
| `python -m docgen.bench build` (`bash docgen/scripts/make_bank_data.sh`), studio 레시피 bank-* | 문서 이해(classify·kie·marks), 업무 처리(doc_check·cross_check·review), 값 칸 OCR(ocr_field·ocr_page) |
| `python -m docgen.ocr_set build` (합성), 설정의 `ocr_prepare` 단계·`python -m docgen.bench.ocr_prepare` (실서류 + 사내 OCR), studio 레시피 ocr-*·가져오기 | 쪽 OCR 8과제 (crop_ocr·bbox_ocr·region_ocr·marked_ocr·grounding·spotting·relation·marked_box) |
| studio ④ 라벨 있는 데이터·서류 넣기(원본 데이터로) | 위 과제 중 고른 것 |

설정의 `data` 칸 (상대 경로는 설정 파일 기준):

| 칸 | 뜻 |
|---|---|
| `train` | 학습 데이터셋 목록. 경로 또는 `{"path", "count"}` (그 데이터셋에서 SFT 문항을 count 개만 무작위로). 문항 `meta.split` 이 train 이면 학습, val 이면 검증 (`docgen.bench build --split train` 폴더는 표시 없는 문항도 학습) |
| `benchmark` | 평가 데이터셋 목록. 문항 `meta.split` 이 train·val 이 아닌 것. OCR 준비 폴더 하나를 학습·평가 둘 다에 넣어도 된다 (문서 단위로 나뉘어 있음) |
| `output_dir` | 섞은 폴더 (`DONE.json` 이 있으면 다시 섞지 않음) |
| `task_mix` | `{과제: 비율}`. 적힌 과제는 `sft_max_examples` 안에서 그 비율, 0 이면 뺌, **적히지 않은 과제는 있는 만큼 다** (OCR 은 보통 `count` 로만 줄인다) |
| `grpo_holdout` | 학습 문항 중 이 비율의 고객(업무 묶음)·문서는 SFT 에 넣지 않고 GRPO 후보로 (기본 0.2) |
| `image_max_size`, `max_image_tokens_per_sample`, `sft_max_length` | 그림 하나·문항 하나의 토큰 예산 (여러 서류는 고르게 줄임), SFT 최대 길이 (`configs/sft.yaml` 의 `max_length` 와 같게) |

평가 세트와 같은 고객·문서가 학습에 있으면 멈춥니다. 정답을 답으로 넣었을 때 만점이 아니면(데이터와 채점 코드가 안 맞음) 멈춥니다.

## 단계와 결과

| 단계 | 하는 일 | 결과 (`workdir` 아래) |
|---|---|---|
| ocr_prepare | (선택) 설정 최상위 `ocr_prepare` 에 OCR 준비 설정(`docgen/bench/ocr_config.example.json` 꼴, 하나 또는 목록)을 적으면, 가진 이미지를 사내 OCR 해 OCR 학습·평가 데이터로 (`python -m docgen.bench.ocr_prepare`, 차례로). 결과 폴더(그 설정의 `output_dir`)는 `data.train`·`data.benchmark` 에 경로로 적어 둔다 (평가 전용 `benchmark_only` 는 `data.benchmark` 에만). 합성 OCR·studio 데이터셋만 쓰면 빼 둔다. 설명서 [guide/ocr_prepare.md](../guide/ocr_prepare.md) | 그 설정의 `output_dir/` (`DONE.json` 이 있으면 건너뜀) |
| prepare | 섞기 (`train/mix.py`) | `data.output_dir/`: `train_sft.jsonl`, `val_sft.jsonl`, `train_grpo.jsonl`, `benchmark_tasks.jsonl`·`benchmark_items.jsonl`, `DONE.json` |
| eval_base | 출발 모델 평가 (`eval.compare_models` 도) | `predictions/start.jsonl`, `reports/start.json` |
| sft | SFT (`python -m train.launch sft`) | `sft/…/checkpoint-N` |
| eval_sft | SFT 병합·평가, GRPO 후보에 답 | `reports/sft.json` |
| select | GRPO 문항 고르기: `mine`(반은 SFT 보상이 낮은 것) · `random` · `all` | `grpo_train.jsonl` |
| grpo | GRPO, 보상 = `docgen.bench.evaluate.reward` (`train/reward_plugin.py`) | `grpo/…/checkpoint-N` |
| eval_grpo | GRPO 병합·평가 | `reports/grpo-<체크포인트>.json` |
| report | 비교표 (OCR·문서·업무 열 한 표) | `reports/benchmark.{csv,md,html}` — 읽는 법 [guide/results.md](../guide/results.md) |

평가는 GPU 마다 vLLM 서버를 하나씩 띄우고 같은 그림의 질문을 같은 서버로 보냅니다. 끝나면(report) studio 학습 기록이 평가 세트마다 모델 답으로 붙여 ⑦ 평가에 점수가 뜹니다.

## 설정 파일 (`train/configs/`)

| 파일 | 뜻 |
|---|---|
| `pipeline.example.json` | 파이프라인 설정 예시 (모델, GPU, data, sft·grpo·eval) |
| `sft.yaml` · `sft_a100_40g_x2.yaml` | SFT (A100 80GB×2 / 40GB×2) |
| `grpo_a100x2.yaml` · `grpo_a100_40g_x2.yaml` | GRPO, `reward_funcs: ["docgen"]` |
| `inference.json` | 평가 답 내기 (`max_tokens` 4096, `timeout` 600) |

`grpo.tasks` 로 GRPO 후보 과제를 고릅니다 (기본: cross_check·review·doc_check·kie·grounding·spotting·relation), `grpo.max_images` 로 그림이 많은 문항을 뺍니다.

## 하나씩 돌리기 (`python -m train.cli`)

```bash
python -m train.cli mix     --config <설정>                     # 섞기만
python -m train.cli predict --config train/configs/inference.json --tasks <섞은 폴더>/benchmark_tasks.jsonl \
                            --endpoint http://127.0.0.1:8000/v1 --run-id base --out preds/base.jsonl
python -m train.cli score   --items <섞은 폴더>/benchmark_items.jsonl --tasks <같은 문항 파일> --predictions preds/base.jsonl \
                            --label base --out reports/base.json
python -m train.cli report  --reports reports/base.json reports/sft.json --out reports/benchmark.csv
```

시험: `python -m pytest train/tests` (GPU·ms-swift 없이 섞기·보상·답 내기·리허설).
