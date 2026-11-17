# 실험 묶음으로 학습·평가 (sweep)

평가 세트는 고정하고 학습 쪽 설정(데이터·학습률·LoRA·출발 모델)을 바꾼 모델 여러 개를 학습하고, 한 보고서로 비교합니다.
GPU 학습 서버의 저장소 최상위(`document_gen/`)에서 실행합니다. 단계를 하나씩 따로 돌리는 법은 [steps.md](steps.md).

묶음은 **이미 만들어 둔 데이터의 경로**만 받습니다: studio 데이터셋 폴더, OCR 준비 결과 폴더, ms-swift `.jsonl`.
실서류 이미지로 OCR 데이터를 만드는 것(OCR 준비)은 묶음과 상관없이 학습 전에 따로 한 번 합니다 ([ocr.md](ocr.md)).

```bash
python -m train sweep --config train/configs/sweep.json --smoke    # 리허설: 모델마다 5 step, 평가 세트·과제마다 8문항
python -m train sweep --config train/configs/sweep.json            # 돌림 (다시 치면 이어서, 끝난 모델은 건너뜀)
python -m train sweep --config train/configs/sweep.json --status   # 진행 상황 · 모델마다 경로
```

## 1. 설정 파일 두 개

**`pipeline.json`** (base): 모든 모델이 같이 쓰는 것. 예시 [pipeline.example.json](../../train/configs/pipeline.example.json).

| 칸 | 뜻 |
|---|---|
| `model`, `model_type`, `gpus` | 출발 모델 폴더, ms-swift model_type (기본 `qwen3_5`), GPU |
| `data.benchmark` | **평가 세트** (2절). 모든 모델이 이것으로 평가 |
| `data.train` | 학습 데이터 목록 (3절) |
| `data.task_mix` · `sft_max_examples` | 과제 비율 · SFT 문항 수. 적힌 과제는 그 비율, 0 이면 뺌, 안 적힌 과제는 있는 만큼 다 |
| `data.image_max_size` · `max_image_tokens_per_sample` · `sft_max_length` | 그림 하나·문항 하나의 토큰 예산, SFT 최대 길이 (`sft.yaml` 의 `max_length` 와 같게) |
| `sft` | `{"config": "sft.yaml"}` + yaml 위에 덮어쓸 ms-swift 옵션 (`learning_rate`, `lora_rank` …). 40GB GPU 는 `sft_a100_40g_x2.yaml` |
| `eval` | 평가 서버 칸 (`concurrency_per_server`, `port_base`, `deploy_command` …). 보통 그대로 |
| `cache_dir` | (선택) 평가 세트·줄인 그림·모델 답 캐시. 기본 `<root 의 부모>/_cache`. 실험끼리 같은 곳을 쓰면 같은 것을 다시 만들지 않음 |

**`sweep.json`**: 모델 목록. 예시 [sweep.example.json](../../train/configs/sweep.example.json).

```jsonc
{"name": "E02-tune", "about": "무엇을 확인하는 실험인지", "base": "pipeline.json", "root": "../runs/E02-tune",
 "baseline": "a1", "gpu_groups": [[0, 1], [2, 3]],
 "runs": [{"label": "a1", "about": "기준 (base 그대로)"},
          {"label": "a2", "about": "가져온 데이터 더함", "train": ["<데이터셋>", {"path": "<가져온 것>.jsonl", "format": "swift", "count": 20000}]},
          {"label": "a3", "about": "학습률", "sft": {"learning_rate": 5e-5, "num_train_epochs": 2}},
          {"label": "a4", "about": "다른 출발 모델", "model": "/share/…/qwen3-vl-8b", "model_type": "qwen3_vl"}]}
```

- 모델마다 바꿀 수 있는 칸: `model` · `model_type` · `train` · `data`(섞기 칸) · `sft` · `gpus` · `deploy`(평가 서버 명령) · `set`(그 밖의 칸). 안 적은 칸은 base.
- 평가 세트(`data.benchmark`)·`eval.inference_config` 는 모델마다 못 바꿉니다 (비교가 안 되므로).
- `label` 은 영문 소문자·숫자·`-`, 모델 이름이자 폴더 이름(`<root>/<label>/`). `name`·`about` 과 모델마다 `about` 은 꼭 적습니다.
- `gpu_groups` 를 적으면 비는 GPU 묶음에 다음 모델을 넣어 동시에 돌립니다. 없으면 하나씩.
- `baseline`: 보고서 괄호 %p 의 기준 모델 (기본 첫 모델).
- 상대 경로: `sweep.json` 의 칸은 이 파일 기준, `pipeline.json` 의 칸은 그 파일 기준. `train/configs/` 의 기본 yaml 은 이름만 적어도 됩니다.

## 2. 평가 세트 (`data.benchmark`)

`id` 하나가 세트 하나이고 점수가 세트마다 따로 나옵니다.

```jsonc
"benchmark": [
  {"id": "syn", "name": "합성 은행 서류", "group": "synthetic", "paths": ["<studio 평가용 데이터셋 폴더>"]},
  {"id": "real_po_kie", "name": "실서류 매입추심", "group": "real", "format": "swift-fields", "gt": "reviewed",
   "paths": ["/share/…/FE_eval/eval_qa_PO.kie.jsonl"], "scorer": "../scorers/swift_kie_scorer.py:score"}
]
```

| 칸 | 뜻 |
|---|---|
| `paths` | studio 데이터셋 폴더, 또는 ms-swift `.jsonl` (`"format": "swift-fields"`). 여러 개면 합쳐서 한 세트 |
| `group` | 표에서 묶어 보여 줄 분류 (합산하지 않음) |
| `gt` | 정답 출처: `exact`(생성기) · `reviewed`(사람 검수) · `pseudo`(사내 OCR 그대로) |
| `scorer` | 이 세트만 다르게 채점할 함수 `"<파일.py>:<함수>"`. swift 세트에 안 적으면 `swift_default.py` |

- swift `.jsonl` 은 질문을 그대로 묻고, 정답(assistant) 글을 그대로 채점 함수에 넘깁니다.
- 견본 채점 함수 (`train/scorers/`, 복사해 고쳐 씀):

  | 파일 | 붙일 세트 |
  |---|---|
  | `swift_default.py` | swift 추출 (`in order: [필드…]` + 답 배열) — 안 적으면 이것 |
  | `swift_kie_scorer.py` · `kie_list_scorer.py` | `temp/swift_to_kie*_tmp.py` 로 kie 꼴로 바꾼 swift |
  | `vqa_scorer.py` | `qa_to_swift` 로 만든 VQA swift ([steps.md 5절](steps.md#5-실서류-vqa-를-평가-세트로-qa_to_swift)) |
  | `kie_default.py` · `bank_default.py` · `form_qa_example.py` · `ocr_default.py` | 합성 세트를 조금 다르게 채점할 때 |

  함수 꼴: `def score(item, output) -> {"metrics": {"f1": 0~1, …}, "main": "f1", "parse_fail": False}`
  (`item["answer"]` 정답, swift 는 질문이 `item["eval"]["prompt"]`; `output` 모델 답, 생각 블록은 뗀 것).
- 돌리기 전에 세트마다 **정답을 답으로 넣어 만점인지** 봅니다 (데이터와 채점이 맞는지). swift 줄 중 채점 함수가 못 읽는 줄은 경고와 함께 뺍니다.
- 평가 세트와 같은 문서·그림이 학습 데이터에 있으면 멈춥니다.

## 3. 학습 데이터 (`data.train`)

```jsonc
"train": ["<studio 학습용 데이터셋 폴더>",
          {"path": "<OCR 준비 결과 폴더>", "count": 20000},
          {"path": "/share/…/my_swift_train.jsonl", "format": "swift", "count": 5000}]
```

- 폴더: studio 데이터셋, 또는 OCR 준비 결과 폴더 (둘 다 `meta.json` + `tasks/`). 문항 `meta.split` 이 `train` 이면 학습, `val` 이면 검증 (OCR 준비 폴더는 안에서 학습·평가가 나뉘어 있어 `data.benchmark` 에도 같은 경로를 적을 수 있음).
- `"format": "swift"`: 밖에서 가져온 ms-swift `.jsonl`. 줄(`messages`, `images`)을 **그대로** 학습합니다 (system·여러 턴도). 그림만 예산에 맞춰 줄입니다. 과제 이름은 `swift:<파일 이름>` 이라 `task_mix` 에 그 이름으로 비율을 줄 수 있습니다.
- `count`: 그 데이터에서 무작위로 쓸 문항 수.

## 4. 무엇이 어떻게 도나

```text
묶음 시작 ─ 평가 세트 준비 (한 번, cache_dir/sets)
   └ 모델마다:  학습 데이터 섞기 → 출발 모델 평가 → SFT → 병합·SFT 평가 → 보고서 갱신
```

| 단계 | 하는 일 | 다시 하지 않는 조건 |
|---|---|---|
| 평가 세트 준비 | 세트마다 질문·정답·줄인 그림 → `<cache_dir>/sets/<id>-<지문>/` | 원본 파일·채점 함수·그림 예산이 같으면 그 폴더를 씀 (다른 실험도) |
| 섞기 | `<root>/<label>/data/train_sft.jsonl` · `val_sft.jsonl`. 줄인 그림은 `<cache_dir>/images` | `data/DONE.json` |
| 출발 모델 평가 | GPU 마다 vLLM 서버, 세트마다 답 | 같은 모델·같은 세트의 답이 캐시에 있으면 추론 없이 (다른 묶음에서 낸 것도) |
| SFT | ms-swift `swift sft` → `<root>/<label>/sft/v*/checkpoint-N` | `state.json` 의 `done` |
| SFT 평가 | 마지막 체크포인트를 합쳐 `<root>/<label>/merged/sft-…/` 에서 평가 (Qwen3.5 MTP 가중치는 출발 모델에서 채움) | 위와 같음 |

- 모델 하나가 실패해도 다음 모델로 갑니다. 상태 `<root>/sweep.json`, 로그 `<root>/<label>/sweep.log`·`logs/`.
- 끊겼으면 같은 명령을 다시 치면 끝난 단계는 건너뜁니다.
- 이미 돈 모델의 설정을 바꾸면 그 모델은 돌리지 않습니다 → 새 `label` 로 추가합니다.

## 5. 결과

| 파일 (`<root>/`) | 내용 |
|---|---|
| `report.html` | 모델 표(설명·바꾼 설정·학습 데이터·**모델 경로**·SFT 체크포인트), 한눈에 보기(평가 세트·과제마다 주 지표, 기준 모델 대비 %p), 세트별 자세히(모든 지표·답 형식 오류·서식별 등) |
| `answers.html` | **모델 A·B 를 골라** 문항마다 정답·두 답·점수. B 가 좋아진·나빠진 문항 수, 나빠진 문항만 보기 |
| `scores.csv` | 같은 숫자 (평가 세트·과제·지표·모델·값·기준 대비 %p) |
| `results.json` | 모델마다 경로·체크포인트·세트별 답 파일 (평가만 하기의 `{"sweep": …}` 가 읽음) |

읽는 순서:
1. **답 형식 오류**(세트별 자세히): SFT 뒤에는 거의 0% 여야 합니다. 남으면 SFT 가 덜 됐거나 답이 `max_tokens` 에서 잘린 것.
2. **한눈에 보기**: 과제별 주 지표와 기준 대비 %p. 위치까지 답하는 과제(kie·marks)는 **값**(글자를 맞게 읽었나)과 **위치**(박스 IoU 0.5)가 따로 나옵니다 — 출발 모델처럼 좌표 규칙을 배우지 않은 모델은 위치만 낮게 나옵니다. 둘 다 맞아야 하는 값+위치(`vl_f1`)는 세트별 자세히에. 지표 뜻은 [과제와 채점 규칙](../reference/benchmark.md).
3. **차이가 의미 있나**: 문항 수 `n` 에 따른 흔들림(95%, 점수 50% 근처) — 2,000 이상 ±2%p · 500 ±4.5%p · 100 ±10%p · 30 이하 ±18%p. 이보다 작은 차이는 "차이 없음".
4. **answers.html** 에서 나빠진 문항을 직접 봅니다.

- OCR 세트를 평가에 넣어 두면 학습하면서 글자 읽기를 잊었는지(출발 모델 대비 Δ) 같이 보입니다.
- 합성 세트 점수는 학습 데이터와 같은 생성기라 실서류보다 높게 나옵니다. 실서류 세트로 따로 봅니다.

## 6. 에러

| 증상 | 할 일 |
|---|---|
| `돌리기 전에 고칠 것` 목록 | 경로·칸을 고칩니다. 아무 모델도 시작하지 않은 상태. OCR 준비 폴더가 아직 없으면 [ocr.md](ocr.md) 로 먼저 만듭니다 |
| `없어진 칸 … part / from_sft / start_from` | GRPO 는 이 브랜치에 없습니다. 칸을 지웁니다 (출발 모델 평가 공유는 캐시가 대신) |
| `설정의 ocr_prepare 는 쓰지 않습니다` | 경고만 하고 넘어갑니다. 칸을 지우고, 결과 폴더가 없으면 [ocr.md](ocr.md) 로 따로 만듭니다 |
| `정답을 답으로 넣어도 만점이 아닙니다` | 데이터를 만든 docgen 코드와 다르거나, 붙인 채점 함수가 정답을 못 읽음 |
| `학습 문항 … 평가 세트와 같은 문서·그림` | 학습 데이터에서 평가 문서를 빼거나 따로 만듭니다 |
| `Port … is already in use` · 서버가 안 뜸 | 남은 서버를 끄거나 `eval.port_base` 를 바꿉니다. 서버 로그 `<root>/<label>/logs/server-*.log` |
| `다른 실행이 만드는 중이라 끝나기를 기다립니다` | 같은 평가 세트·답을 다른 실행이 만드는 중. 그 실행이 없는데 계속이면 말한 `.lock` 파일을 지웁니다 |
| SFT 메모리 부족 | `sft.config` 를 `sft_a100_40g_x2.yaml` 로, 또는 `data.max_image_tokens_per_sample`·`sft_max_length` 를 줄입니다 |
