# document_gen: 은행 서류 VLM (OCR 학습 → 은행 업무 학습)

실제 서류 이미지와 사내 OCR 결과로 VLM(Qwen3.5-9B)에 **글자·위치 읽기(OCR)**를 학습시키고(1부), 그 모델에서 출발해 합성 은행 서류로 **은행 업무**(서류 구비 확인, 서류 대조, 심사 질의, 정보 추출)를 학습시킨 뒤 벤치마크로 비교합니다(2부). 학습에 쓰는 벤치마크·합성 데이터는 생성기(docgen)가 만들고, 화면(studio)에서 서식·라벨을 고치고 데이터셋을 관리합니다.

**처음이면 [guide/tutorial.md](guide/tutorial.md)부터 따라 하세요.**

## 네 갈래

| 폴더 | 하는 일 | 어디서 돌리나 | 시작 문서 |
|---|---|---|---|
| [`ocr/`](ocr/README.md) | **1부 OCR**: 실서류 이미지 + 사내 OCR → 준비(`prepare`) → SFT·GRPO 학습 → 평가 → OCR viewer | GPU 학습 컨테이너 (`cd ocr`) | [ocr/README.md](ocr/README.md) |
| [`bank/`](bank/README.md) | **2부 은행 업무**: 생성기 데이터 → 준비 → SFT·GRPO 학습 → 평가 → 은행 업무 viewer. 1부 코드(`../ocr`)를 그대로 씀 | GPU 학습 컨테이너 (`cd bank`) | [bank/README.md](bank/README.md) |
| [`docgen/`](docgen/README.md) | **벤치마크·합성 데이터 생성**: 서류 545종(기존 HTML 70 + 공식 대조 HTML 69 + 하나은행 원본 서식 406), 은행 업무 평가 세트·학습 데이터(`docgen.bench`), 합성 OCR 세트(`docgen.ocr_set`) | docgen 도커 컨테이너 (Chromium·글꼴) | [docgen/README.md](docgen/README.md) |
| [`studio/`](studio/README.md) | **화면**: 서식·라벨 보고 고치기, 데이터셋 만들기(레시피)·등록·채점·비교, 이미지 가져오기·OCR 검수, 학습 설정 내보내기 | docgen 도커 컨테이너 (`python -m studio`, SSH 터널) | [studio/README.md](studio/README.md) |

```text
docgen/ ──(합성 데이터·평가 세트)──▶ bank/  ◀──(출발 모델)── ocr/
   ▲                                  │                   │
   └──────── studio/ (만들기·고치기·등록·채점·학습 설정) ◀──┘ (모델 답·점수)
```

그 밖: [`guide/`](guide/README.md) 사용 가이드(과제 예시·질문 문장·결과 읽기), [`docker/`](docker/README.md) docgen 도커 이미지와 접속.

## 문서 지도

**시작하기**

| 문서 | 들어 있는 것 |
|---|---|
| [guide/tutorial.md](guide/tutorial.md) | **처음부터 따라하기.** 코드 받기 → 설치 → 사내 OCR 서버 띄우기 → OCR 학습 → 합성 데이터 만들기 → 은행 업무 학습 → 결과 확인. 단계마다 확인 방법, 맨 끝에 자주 나는 에러 표 |
| [guide/overview.md](guide/overview.md) | 프로젝트 소개 (팀 공유용). 1부·2부 각각 컨셉 → 데이터 구조 → 학습 → 평가 → viewer, 부록에 생성기·벤치마크 상세 |
| [guide/slides/](guide/slides/README.md) | 발표 자료 (`guide/slides/index.html`, 발표자 노트 포함) |

**데이터와 과제 정의**

| 문서 | 들어 있는 것 |
|---|---|
| [guide/tasks.md](guide/tasks.md) | **모든 과제의 실제 데이터 예시.** OCR 8과제, 은행 업무 8과제, 서류 대조 사례 14종, 심사 질의 규칙별 이미지·질문·정답·채점 정보 |
| [guide/questions.md](guide/questions.md) | 학습한 모델에게 묻는 법 (은행 업무 과제별 질문 문장, 넣을 이미지, 답 형식). OCR 과제는 [ocr/docs/PROMPTS.md](ocr/docs/PROMPTS.md) |
| [guide/fields/](guide/fields/README.md) | 서류 476종의 항목 키·항목명·타입·체크박스 보기 |
| [guide/documents.md](guide/documents.md) | 서류 정식 명칭 476종, 업무 12종별 필수 서류 |
| [guide/benchmark.md](guide/benchmark.md) | 은행 업무 벤치마크: 과제, 문항 만드는 방법, 불일치 14종과 근거, 채점 규칙 |

**실행과 결과**

| 문서 | 들어 있는 것 |
|---|---|
| [ocr/README.md](ocr/README.md) | 1부 파이프라인 (`run_pipeline.py`). 상세는 [ocr/docs/](ocr/docs/): 설치·사내 OCR 연결, 옵션, 과제·지표·보상 설계, 단계별 수동 실행 |
| [bank/README.md](bank/README.md) | 2부 파이프라인 (`run_bank_pipeline.py`): 설정 항목, GPU별(80GB/40GB) 설정, 단계, 시간 |
| [ocr/viewer/README.md](ocr/viewer/README.md) | viewer 두 개: OCR viewer(`ocr/viewer/start.sh`, 포트 7860), 은행 업무 viewer(`bank/viewer/bank_start.sh`, 포트 7861) |
| [guide/results.md](guide/results.md) | 결과 점수표 읽는 법: 지표 뜻, 찍어도 나오는 점수, 오차 범위, 이상 신호 |
| [docgen/README.md](docgen/README.md) | 생성기 자체 (설치, 명령, 출력 형식, 서식, 서식 추가 방법은 [docgen/manual/TEMPLATE_GUIDE.md](docgen/manual/TEMPLATE_GUIDE.md)) |
| [studio/README.md](studio/README.md) | studio 화면 사용법. 설계는 [studio/DESIGN.md](studio/DESIGN.md), 학습으로 이어 쓰기는 [studio/TRAINING.md](studio/TRAINING.md) |
| [docker/README.md](docker/README.md) | docgen 도커 설치, SSH 접속, 같은 컨테이너에서 studio 띄우기 |

## 테스트

```bash
python -m pytest                                   # docgen/tests, studio/tests (생성기·studio)
cd ocr  && python -m unittest discover -s tests    # 1부
cd bank && python -m unittest discover -s tests    # 2부 (같은 저장소의 docgen 으로 채점 시험까지)
```

## 예전 구조에서 옮겨 올 때 (2026-10-20 재배치)

예전에는 1부·2부가 `training/` 한 폴더에, 생성기 재료가 최상위(`templates/`, `add_template/`, `fonts/`, `samples/`, `scripts/`, `datasets/recipes/`, `docs/`)에 흩어져 있었습니다.

| 예전 | 지금 |
|---|---|
| `training/` (1부: `bank_ocr/`, `run_pipeline.py`, `train.py`, `configs/sft·grpo·inference·pipeline*`, `docs/`, `viewer/start.sh`) | `ocr/` |
| `training/` (2부: `bank_task/`, `run_bank_pipeline.py`, `bank_task_reward.py`, `configs/bank_*`, `BANK_TASKS.md`, `viewer/bank_*`) | `bank/` (`BANK_TASKS.md` → `bank/README.md`) |
| `templates/`, `add_template/`, `fonts/`, `samples/`, `scripts/`, `assets/`, `datasets/recipes/` | `docgen/templates/`, `docgen/forms/`, `docgen/fonts/`, `docgen/samples/`, `docgen/scripts/`, `docgen/assets/`, `docgen/recipes/` |
| `docs/DOCGEN.md`, `docs/DOCKER.md`, `docs/*` (서식 대응표·현실성 점검·변형) | `docgen/README.md`, `docker/README.md`, `docgen/manual/` |
| `tests/`, `Dockerfile`, `requirements.txt` | `docgen/tests/`·`studio/tests/`, `docker/Dockerfile`, `docgen/requirements.txt` |

**학습 서버에서 할 일** (git 에 없는 데이터·결과 폴더는 저절로 옮겨지지 않습니다):

```bash
cd <코드>                                   # git pull 뒤. 예전 training/ 에는 git 에 없는 것만 남아 있다
mkdir -p bank/runs bank/data
mv training/data training/runs ocr/                       # 1부 준비 결과·학습 결과
mv ocr/runs/bank* bank/runs/                              # 2부 결과 (예: runs/bank1)
mv ocr/data/prepared-bank* bank/data/                     # 2부 준비 결과
mv training/configs/bank_pipeline.json bank/configs/      # 직접 만든 2부 설정
mv training/configs/*.json ocr/configs/                   # 직접 만든 1부 설정 (pipeline.json 등)
mv training/config.json ocr/                              # 1부 데이터 설정 (있으면)
cd ocr && pip install --no-index --no-build-isolation -e '.[ocr]'   # 1부 패키지 다시 등록 (2부는 설치 불필요)
```

- 설정 파일 안의 **상대 경로**(`../runs/…`, `../data/…`)는 설정 파일 위치 기준이라, 설정을 같은 자리(`ocr/configs/`, `bank/configs/`)에 두면 그대로 맞습니다. 2부 설정에서 1부 것을 가리키는 칸은 기준이 다릅니다: `data.replay.path`·`ocr_check.tasks`는 설정 파일(`bank/configs/`) 기준이라 `../../ocr/data/…`, `model`(1부 결과 모델)은 실행하는 폴더(`bank/`) 기준이라 `../ocr/runs/…`입니다. 헷갈리면 절대 경로를 쓰세요.
- docgen 도커 이미지는 그대로 씁니다 (이미지의 `PYTHONPATH` 가 저장소 최상위라 `python -m docgen` 이 그대로 돕니다). 2부 데이터 만들기는 `bash docgen/scripts/make_bank_data.sh`.

## 브랜치

- **이 브랜치에 전부 들어 있습니다.** `ocr/`의 OCR 코드는 OCR 브랜치(`claude/bank-ocr-pipeline`)와 같습니다. OCR 쪽을 고치면 `git merge -X subtree=ocr origin/claude/bank-ocr-pipeline`으로 가져옵니다.
- 모든 합성 데이터는 실존 인물·사업자와 무관합니다.

## Studio 서식 역할·값 영역

③ 시나리오에서 같은 제출 역할의 기존 HTML·공식 HTML·PDF 배경 서식 중 하나를 선택할 수 있습니다. ① 서식의 HTML에도 글자 값 **영역 편집**을 추가했습니다. 위치·크기·값 출처를 고쳐 미리보기 후 저장하면 생성 이미지와 정답 좌표에 같이 반영됩니다. 사용 방법은 [Studio README](studio/README.md), 저장 방식과 제약은 [DESIGN 14절](studio/DESIGN.md), 545종의 자동 이미지 검사 결과와 남은 항목은 [값 점검표](docgen/manual/FORM_VALUE_AUDIT.md)를 보세요.
