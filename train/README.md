# train — 코드 지도

학습·평가(SFT 까지)의 코드입니다. 쓰는 법은 [guide/train/sweep.md](../guide/train/sweep.md) (실험 묶음), [steps.md](../guide/train/steps.md) (하나씩), [ocr.md](../guide/train/ocr.md).

```text
python -m train sweep --config sweep.json      sweep.py      모델마다 아래 학습 실행을 (차례로 / GPU 묶음마다 동시에), 보고서 하나
python -m train --config pipeline.json         pipeline.py   학습 실행 하나: prepare → eval_start → sft → eval_sft → report
python -m train eval --config eval.json        evaluate.py   학습 없이 모델 경로들 평가
python -m train report <결과 폴더>             report.py     저장된 답으로 report.html · scores.csv (+ answers.py → answers.html)
```

| 파일 | 하는 일 |
|---|---|
| `pipeline.py` | 학습 설정 읽기(`resolve`, 없어진 칸 알림 `drop_removed`), 단계, 평가 세트 준비(`benchmark_sets`) |
| `sweep.py` | 묶음 파일 검사(`load`·`preflight`), 모델마다 설정(`run_config`), GPU 나누기, `results.json`·보고서 |
| `evaluate.py` | 평가만 하기: 모델 목록(`{"sweep": …}`·LoRA 체크포인트 합치기), 평가 세트 |
| `benchmarks.py` | `data.benchmark`·`data.train` 칸 검사 (`normalize`, `train_entries`, 상대 경로 `resolve`) |
| `mix.py` | 평가 세트 준비 `prepare_sets` (`<cache_dir>/sets/<id>-<지문>/`), 학습 데이터 섞기 `mix`, 그림 줄이기 `Fitter` (`<cache_dir>/images`) |
| `swift_import.py` | ms-swift `.jsonl` 읽기: 평가(`load_swift`, 채점 함수에 정답 글 그대로), 학습(`load_swift_train`, 줄 그대로) |
| `serve.py` | 평가 서버(vLLM, GPU 마다 하나)·LoRA 합치기·모델 답 캐시 `Evaluator.answer` (`<cache_dir>/answers/`, 잠금) |
| `predict.py` | OpenAI 호환 서버에 질문 보내기 (그림별로 서버 나눔, 끊기면 이어서) |
| `score.py` | 세트 하나 채점 (`docgen.bench.evaluate` + 구분별 점수) |
| `report.py` · `answers.py` | `report.html`·`scores.csv` (점수는 `<답>.scores.json` 에 캐시) · `answers.html` (두 모델 견주기) |
| `launch.py` | ms-swift `swift sft` 명령 만들기·실행 |
| `fill_weights.py` | 합친 모델에 빠진 가중치(Qwen3.5 MTP `mtp.*`)를 출발 모델에서 채움 |
| `qa_to_swift.py` | image/qa JSON 폴더 → ms-swift `.jsonl` |
| `settings.py` | 설정 읽기·겹치기, 로그, 그림 토큰 계산, 파일 잠금 |
| `configs/` | `pipeline.example.json` · `sweep.example.json` · `eval.example.json` · `sft.yaml`(A100 80GB×2) · `sft_a100_40g_x2.yaml` · `inference.json` |
| `scorers/` | 평가 세트마다 붙이는 채점 함수 견본 ([sweep.md 2절](../guide/train/sweep.md#2-평가-세트-databenchmark)) |

## 캐시 (`cache_dir`)

```text
<cache_dir>/sets/<세트 id>-<지문>/       tasks.jsonl (질문) · items.jsonl (정답) · images/ · DONE.json
<cache_dir>/answers/<세트 폴더 이름>/<모델>-<지문>.jsonl   모델 답 (+ .meta.json · .done · .scores.json)
<cache_dir>/images/                       학습 그림의 줄인 사본
```

- 세트 지문: 세트 칸 + 원본 파일 크기·시각 + 채점 함수 파일 + 그림 예산. 답 지문: 모델 폴더(경로·`config.json` 시각)·model_type·평가 서버 명령·`inference.json`·질문 파일.
- 같은 것을 두 실행이 동시에 만들면 `<대상>.lock` 으로 한쪽이 기다립니다.
- 지워도 됩니다 (다음 실행이 다시 만듦). 이미 끝난 결과 폴더의 `results.json` 이 그 답 파일을 가리키므로, 지운 뒤에는 그 결과의 보고서를 다시 만들 수 없습니다.

## 결과 폴더

| 폴더 | 안의 것 |
|---|---|
| 학습 실행 `<workdir>/` | `config.json`(쓴 설정) · `state.json`(끝난 단계·모델 경로·세트별 답) · `data/`(섞은 학습 데이터) · `sft/` · `merged/` · `logs/` · `results.json` · 보고서 |
| 실험 묶음 `<root>/` | 모델마다 `<label>/`(위 workdir) · `sweep.config.json` · `sweep.json`(상태) · `results.json` · `report.html` · `answers.html` · `scores.csv` |
| 평가만 `<root>/` | `eval.config.json` · `results.json` · `merged/`(합친 LoRA) · 보고서 |

시험: `python -m pytest train/tests` (GPU·ms-swift 없이, 가짜 모델 서버로).
