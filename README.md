# document_gen: 은행 서류 VLM (OCR · 문서 이해 · 업무 처리)

실제 서류 이미지와 사내 OCR 결과, 합성 은행 서류로 VLM(Qwen3.5-9B)에 **글자·위치 읽기(OCR)**, **문서 이해**(분류·정보 추출·체크·도장·서명), **업무 처리**(서류 구비 확인, 서류 대조, 심사 질의)를 한 번에 학습시키고 벤치마크로 비교합니다. 데이터는 생성기(docgen)와 화면(studio)이 같은 과제 형식으로 만들고, 학습은 하나(`python -m train`)입니다.

**처음이면 [guide/tutorial.md](guide/tutorial.md)부터 따라 하세요.**

## 세 갈래

| 폴더 | 하는 일 | 어디서 돌리나 | 시작 문서 |
|---|---|---|---|
| [`docgen/`](docgen/README.md) | **데이터 생성·채점**: 서류 545종(기존 HTML 70 + 공식 대조 HTML 69 + 하나은행 원본 서식 406), 문서·업무 평가 세트·학습 데이터(`docgen.bench`), 합성 OCR 세트(`docgen.ocr_set`), 쪽 OCR 문항 만들기(`docgen.bench.ocr_prepare`), 모든 과제의 채점·GRPO 보상(`docgen.bench.evaluate`) | docgen 도커 컨테이너 (Chromium·글꼴) | [docgen/README.md](docgen/README.md) |
| [`studio/`](studio/README.md) | **화면**: 서식·라벨 보고 고치기, 서류 넣기(실서류 묶음 → 서식·시나리오·데이터), 데이터셋 만들기·등록·문항 보기·채점·비교, 학습 설정 내보내기 | docgen 도커 컨테이너 (`python -m studio`, SSH 터널) | [studio/README.md](studio/README.md) |
| [`train/`](train/README.md) | **학습 하나**: studio 데이터셋(OCR·문서·업무 과제 폴더)을 섞어 → SFT·GRPO → 평가 → 비교표 | GPU 학습 컨테이너 (저장소 최상위에서 `python -m train`) | [train/README.md](train/README.md) |

```text
docgen/ ──(과제 폴더: 합성·OCR 준비)──▶ studio/ (만들기·고치기·등록·문항 보기·채점·학습 설정)
                                         │ 데이터셋 경로 + 설정 ▲ 모델 답·점수
                                         ▼                    │
                                       train/ (섞기 → SFT → GRPO → 평가 → 보고서)
```

그 밖: [`guide/`](guide/README.md) 사용 가이드(과제 예시·질문 문장·결과 읽기), [`docker/`](docker/README.md) docgen 도커 이미지와 접속.

## 문서 지도

**시작하기**

| 문서 | 들어 있는 것 |
|---|---|
| [guide/tutorial.md](guide/tutorial.md) | **처음부터 따라하기.** 코드 받기 → 설치 → 사내 OCR 서버 띄우기 → 데이터 만들기 → 학습 → 결과 확인. 단계마다 확인 방법, 맨 끝에 자주 나는 에러 표 |
| [guide/overview.md](guide/overview.md) | 프로젝트 소개 (팀 공유용). 과제 묶음별 컨셉 → 데이터 구조 → 학습 → 평가, 부록에 생성기·벤치마크 상세 |
| [guide/slides/](guide/slides/README.md) | 발표 자료 (`guide/slides/index.html`, 발표자 노트 포함) |

**데이터와 과제 정의**

| 문서 | 들어 있는 것 |
|---|---|
| [guide/tasks.md](guide/tasks.md) | **모든 과제의 실제 데이터 예시.** OCR 8과제, 은행 업무 8과제, 서류 대조 사례 14종, 심사 질의 규칙별 이미지·질문·정답·채점 정보 |
| [guide/questions.md](guide/questions.md) | 학습한 모델에게 묻는 법 (과제별 질문 문장, 넣을 이미지, 답 형식). 쪽 OCR 과제의 질문은 `docgen/bench/ocr_tasks.py` 의 `PROMPTS` |
| [guide/fields/](guide/fields/README.md) | 서류 476종의 항목 키·항목명·타입·체크박스 보기 |
| [guide/documents.md](guide/documents.md) | 서류 정식 명칭 476종, 업무 12종별 필수 서류 |
| [guide/benchmark.md](guide/benchmark.md) | 은행 업무 벤치마크: 과제, 문항 만드는 방법, 불일치 14종과 근거, 채점 규칙 |

**실행과 결과**

| 문서 | 들어 있는 것 |
|---|---|
| [train/README.md](train/README.md) | 학습 실행 (`python -m train`): 설정 항목, 데이터셋 섞기, GPU별(80GB/40GB) 설정, 단계, 결과 폴더 |
| [studio/TRAINING.md](studio/TRAINING.md) | studio 데이터셋으로 학습 설정 만들기, 진행 보기, 결과가 평가에 붙는 과정 |
| [guide/results.md](guide/results.md) | 결과 점수표 읽는 법: 지표 뜻, 찍어도 나오는 점수, 오차 범위, 이상 신호 |
| [docgen/README.md](docgen/README.md) | 생성기 자체 (설치, 명령, 출력 형식, 서식, 서식 추가 방법은 [docgen/manual/TEMPLATE_GUIDE.md](docgen/manual/TEMPLATE_GUIDE.md)) |
| [studio/README.md](studio/README.md) | studio 화면 사용법 (문항·모델 답·점수 보기는 ⑥ 데이터셋 · ⑦ 평가). 설계는 [studio/DESIGN.md](studio/DESIGN.md) |
| [docker/README.md](docker/README.md) | docgen 도커 설치, SSH 접속, 같은 컨테이너에서 studio 띄우기 |

## 테스트

```bash
python -m pytest        # docgen/tests, studio/tests, train/tests (학습은 GPU·ms-swift 없이 리허설까지)
```

## 예전 구조에서 옮겨 올 때

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

**2026-10-20 재배치.** 예전에는 1부·2부가 `training/` 한 폴더에, 생성기 재료가 최상위(`templates/`, `add_template/`, `fonts/`, `samples/`, `scripts/`, `datasets/recipes/`, `docs/`)에 흩어져 있었습니다. 생성기 재료는 `docgen/templates/`, `docgen/forms/`, `docgen/fonts/`, `docgen/samples/`, `docgen/scripts/`, `docgen/assets/`, `docgen/recipes/` 로, `docs/DOCGEN.md`·`docs/DOCKER.md` 는 `docgen/README.md`·`docker/README.md` 로 옮겼습니다.

- docgen 도커 이미지는 그대로 씁니다 (이미지의 `PYTHONPATH` 가 저장소 최상위라 `python -m docgen` 이 그대로 돕니다). 은행 업무 데이터 만들기는 `bash docgen/scripts/make_bank_data.sh`.

## 브랜치

- **이 브랜치에 전부 들어 있습니다.**
- 모든 합성 데이터는 실존 인물·사업자와 무관합니다.

## Studio 서식 역할·값 영역

③ 시나리오에서 같은 제출 역할의 기존 HTML·공식 HTML·PDF 배경 서식 중 하나를 선택할 수 있습니다. ① 서식의 HTML에도 글자 값 **영역 편집**을 추가했습니다. 위치·크기·값 출처를 고쳐 미리보기 후 저장하면 생성 이미지와 정답 좌표에 같이 반영됩니다. 사용 방법은 [Studio README](studio/README.md), 저장 방식과 제약은 [DESIGN 14절](studio/DESIGN.md), 545종의 자동 이미지 검사 결과와 남은 항목은 [값 점검표](docgen/manual/FORM_VALUE_AUDIT.md)를 보세요.
