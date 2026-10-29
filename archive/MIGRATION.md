# 예전 구조에서 옮겨 올 때 (기록)

예전 README 에 있던 이전 안내입니다. 지금 구조는 저장소 최상위 [README.md](../README.md).

**2026-10-28 서식 폴더 정리.** 서식 하나에 관한 것은 그 서식 폴더에, 모든 서식에 같은 것은 `docgen/forms/_common/` 에 모았습니다.
`docgen/templates/`·`docgen/dictionary/`·`docgen/key_rules.json`·`keys.json`·`marks.json`·`freetext_templates.json` → `docgen/forms/_common/`,
코드 서식의 값 함수 `docgen/docs/<그룹>.py` → 서식 폴더 `generate.py`, 서식 관리 문서 `guide/forms.md`·`guide/qa.md` → [docgen/forms/README.md](../docgen/forms/README.md).
같은 설정으로 만든 데이터셋은 예전과 바이트 단위로 같고, 검수 기록(서식 해시)도 그대로입니다.

**2026-10-21 통합.** 1부 OCR(`ocr/`)과 2부 은행 업무(`bank/`)를 하나로 합쳤습니다 ([studio/DESIGN.md 17절](../studio/DESIGN.md)).

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
- 학습 서버의 옛 결과·데이터 폴더(`ocr/runs`, `ocr/data`, `bank/runs`, `bank/data`)는 git 에 없어 남아 있습니다. 새 학습은 `train/runs`·`train/data`(설정의 `workdir`·`data.output_dir`) 에 씁니다. 옛 설정 파일은 쓸 수 없으니 [train/configs/pipeline.example.json](../train/configs/pipeline.example.json) 으로 다시 만드세요 (studio 학습 탭이 만들어 줍니다).

**2026-10-20 재배치.** 예전에는 1부·2부가 `training/` 한 폴더에, 생성기 재료가 최상위(`templates/`, `add_template/`, `fonts/`, `samples/`, `scripts/`, `datasets/recipes/`, `docs/`)에 흩어져 있었습니다. 생성기 재료는 `docgen/templates/`(지금은 `docgen/forms/_common/templates/`), `docgen/forms/`, `docgen/fonts/`, `docgen/samples/`, `docgen/scripts/`, `docgen/assets/`, `docgen/recipes/` 로, `docs/DOCGEN.md`·`docs/DOCKER.md` 는 `docgen/README.md`·`docker/README.md` 로 옮겼습니다.

- docgen 도커 이미지는 그대로 씁니다 (이미지의 `PYTHONPATH` 가 저장소 최상위라 `python -m docgen` 이 그대로 돕니다). 은행 업무 데이터 만들기는 `bash docgen/scripts/make_bank_data.sh`.
