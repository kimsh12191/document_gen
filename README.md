# document_gen: 은행 서류 VLM (OCR · 문서 이해 · 업무 처리)

은행 서류 이미지로 VLM(Qwen3.5-9B)에 글자·위치 읽기(OCR), 문서 이해(분류·추출·체크·도장·서명), 업무 처리(구비 확인·서류 대조·심사 질의)를 학습시키고 같은 평가 세트로 비교합니다.

## 이 저장소는 무엇인가

세 부분이 한 줄로 이어집니다.

| 부분 | 하는 일 | 어디서 실행 |
|---|---|---|
| [`docgen/`](docgen/README.md) | **서식별 합성 데이터 생성기.** 서식 545종(서식 하나 = 폴더 `docgen/forms/<ID>/` 하나)에 가짜 고객 값을 채워 그리고, 그림마다 질문·정답을 만든다. 평가 세트와 학습 데이터를 같은 코드로 만들고, 채점도 여기서 | studio 컨테이너 (생성) / 학습 서버 (채점·OCR 준비) |
| [`studio/`](studio/README.md) | 위 작업을 하는 웹 화면: 서식 검수·편집, 데이터셋 만들기·등록, 채점, 학습 설정 내보내기 | studio 도커 컨테이너 ([docker/README.md](docker/README.md)) |
| [`train/`](train/README.md) | `python -m train`: 데이터 섞기 → SFT → GRPO → 평가 → 비교표 | GPU 학습 서버 |

```text
서식 폴더 docgen/forms/<ID>/            생성 (studio ⑥ 또는 python -m docgen.bench build)        학습·평가 (train/)
  모양·칸·값 (look/, fields.json,   ─►  서식 × 고객마다 그리기 → 칸(키·값·위치)             ─►  SFT·GRPO → 평가 세트 채점
  generate.py)                          → 과제별 질문·정답 (docgen/bench/tasks/)                    → summary·answers·benchmark.html
  질문·답 (questions.json, qa.py)       → 데이터셋 폴더 tasks/*.jsonl, swift/*.jsonl              (채점 함수 train/scorers/)
                                          + 서류 여러 장 묶음 업무 과제 (구비·대조·심사)
실서류 이미지 ──────────────────────────► OCR 준비 (docgen/bench/ocr_prepare) ─────────────────────► 같은 학습·평가에
```

정답은 사람이 적지 않습니다. 그릴 때 넣은 값과 잰 위치가 곧 정답이라, 서식을 고치면 데이터도 그대로 따라 바뀝니다.

## 시작

| 하려는 일 | 시작 문서 |
|---|---|
| studio 로 데이터 만들기·학습·결과 보기 (사람) | [guide/README.md](guide/README.md) |
| 서식 하나 고치기: 칸·값·모양, 질문·답 모양, 이 서식만의 질문 | [docgen/forms/README.md](docgen/forms/README.md) (서식 폴더 설명서), 그 서식의 카드 `docgen/forms/<ID>/FORM.md` |
| 새 서식 추가 | [guide/new-forms.md](guide/new-forms.md) |
| 코드 구조 | [docgen/README.md](docgen/README.md), [studio/DESIGN.md](studio/DESIGN.md), [train/README.md](train/README.md) |
| agent 에게 맡기기 | [AGENTS.md](AGENTS.md): 작업 규칙과 문서 위치, 절차는 [guide/agent-workflow.md](guide/agent-workflow.md) |

그 밖의 폴더: [`docker/`](docker/README.md) 내부망 반입·studio 컨테이너·원격 생성(`remote_build.py`), [`guide/`](guide/README.md) 사용 설명서,
`experiments/` 실험 기록, `temp/` 임시 변환 스크립트.

## 테스트

```bash
python -m pytest        # docgen/tests, studio/tests, train/tests (학습은 GPU 없이 리허설까지)
```

모든 합성 데이터는 실존 인물·사업자와 무관합니다.

## 예전 구조에서 옮겨 올 때

**2026-10-28 서식 폴더 정리.** 서식 하나에 관한 것은 그 서식 폴더에, 모든 서식에 같은 것은 `docgen/forms/_common/` 에 모았습니다.
`docgen/templates/`·`docgen/dictionary/`·`docgen/key_rules.json`·`keys.json`·`marks.json`·`freetext_templates.json` → `docgen/forms/_common/`,
코드 서식의 값 함수 `docgen/docs/<그룹>.py` → 서식 폴더 `generate.py`, 서식 관리 문서 `guide/forms.md`·`guide/qa.md` → [docgen/forms/README.md](docgen/forms/README.md).
같은 설정으로 만든 데이터셋은 예전과 바이트 단위로 같고, 검수 기록(서식 해시)도 그대로입니다.

**2026-10-21 통합.** 1부 OCR(`ocr/`)과 2부 은행 업무(`bank/`)를 하나로 합쳤습니다 ([studio/DESIGN.md 17절](studio/DESIGN.md)).

| 예전 | 지금 |
|---|---|
| `ocr/bank_ocr/{data,augment,tasks,pipeline,metrics}.py`, `python -m bank_ocr prepare --config …` | `docgen/bench/ocr_{data,augment,tasks,prepare,metrics}.py`, `python -m docgen.bench.ocr_prepare <설정>` (설정 예시 `docgen/bench/ocr_config.example.json`) |
| `ocr/run_pipeline.py`, `bank/run_bank_pipeline.py` | `python -m train --config train/configs/<이름>.json` (저장소 최상위에서) |
| `ocr/train.py`, `bank_ocr_reward.py`·`bank_task_reward.py` | `train/launch.py`, `train/reward_plugin.py` (`reward_funcs: ["docgen"]`) |
| `bank_ocr predict`·`evaluate`, `bank_task prepare`·`score`·`mine`·`report` | `python -m train.cli {predict,score,mine,report,mix}` |
| 2부 `data.replay`(OCR 섞기)·`ocr_check`(OCR 유지 확인) | OCR 데이터셋을 `data.train`(문항 수 `count`)·`data.benchmark` 목록에 그대로 넣는다 |
| OCR viewer(`ocr/viewer`, 7860), 은행 업무 viewer(`bank/viewer`, 7861) | studio ⑥ 데이터셋 › 문항·모델 답, ⑦ 평가 |
| `ocr/internal_ocr_adapter.py` | `studio/internal_ocr_adapter.py` (옛 이름 `internal_ocr_adapter:ocr_from_file` 도 받음) |

- 이미 만든 OCR 준비 폴더(`prepared/`, `DONE.json`)는 studio 에 등록할 때 과제 형식 `tasks/` 를 그 자리에 만들어 그대로 씁니다.
- 학습 서버의 옛 결과·데이터 폴더(`ocr/runs`, `ocr/data`, `bank/runs`, `bank/data`)는 git 에 없어 남아 있습니다. 새 학습은 `train/runs`·`train/data`(설정의 `workdir`·`data.output_dir`) 에 씁니다. 옛 설정 파일은 쓸 수 없으니 [train/configs/pipeline.example.json](train/configs/pipeline.example.json) 으로 다시 만드세요 (studio 학습 탭이 만들어 줍니다).

**2026-10-20 재배치.** 예전에는 1부·2부가 `training/` 한 폴더에, 생성기 재료가 최상위(`templates/`, `add_template/`, `fonts/`, `samples/`, `scripts/`, `datasets/recipes/`, `docs/`)에 흩어져 있었습니다. 생성기 재료는 `docgen/templates/`(지금은 `docgen/forms/_common/templates/`), `docgen/forms/`, `docgen/fonts/`, `docgen/samples/`, `docgen/scripts/`, `docgen/assets/`, `docgen/recipes/` 로, `docs/DOCGEN.md`·`docs/DOCKER.md` 는 `docgen/README.md`·`docker/README.md` 로 옮겼습니다.

- docgen 도커 이미지는 그대로 씁니다 (이미지의 `PYTHONPATH` 가 저장소 최상위라 `python -m docgen` 이 그대로 돕니다). 은행 업무 데이터 만들기는 `bash docgen/scripts/make_bank_data.sh`.
