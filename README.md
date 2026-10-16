# document_gen: 은행 서류 VLM (OCR 학습 → 은행 업무 학습)

실제 서류 이미지와 사내 OCR 결과로 VLM(Qwen3.5-9B)에 **글자·위치 읽기(OCR)**를 학습시키고(1부), 그 모델에서 출발해 합성 은행 서류로 **은행 업무**(서류 구비 확인, 서류 대조, 심사 질의, 정보 추출)를 학습시킨 뒤 벤치마크로 비교합니다(2부).

**처음이면 [guide/tutorial.md](guide/tutorial.md)부터 따라 하세요.** 아래는 어느 문서에 무엇이 있는지입니다.

## 문서 지도

**시작하기**

| 문서 | 들어 있는 것 |
|---|---|
| [guide/tutorial.md](guide/tutorial.md) | **처음부터 따라하기.** 코드 받기 → 설치 → 사내 OCR 서버 띄우기(`/share/mond/ocr_api/server.py`) → OCR 학습 → 합성 데이터 만들기 → 은행 업무 학습 → 결과 확인. 단계마다 확인 방법, 맨 끝에 자주 나는 에러 표 |
| [guide/overview.md](guide/overview.md) | 프로젝트 소개 (팀 공유용 문서판). 1부·2부 각각 컨셉 → 데이터 구조 → 학습 방법 → 평가 방법 → viewer, 부록에 생성기·벤치마크 상세 |
| [guide/slides/](guide/slides/README.md) | 발표 자료. 웹 슬라이드 원본 파일과, 브라우저로 바로 열리는 `guide/slides/index.html` (발표자 노트 포함) |

**데이터와 과제 정의**

| 문서 | 들어 있는 것 |
|---|---|
| [guide/tasks.md](guide/tasks.md) | **모든 과제의 실제 데이터 예시.** OCR 8과제, 은행 업무 8과제, 서류 대조 사례 14종, 심사 질의 규칙별로 이미지·질문 전문·정답·채점 정보·meta·학습 레코드를 줄이지 않고 전부. 비슷한 문제를 새로 만들 때 고칠 곳 |
| [guide/questions.md](guide/questions.md) | 학습한 모델에게 묻는 법 (은행 업무 과제별 질문 문장, 넣을 이미지, 답 형식). OCR 과제는 [training/docs/PROMPTS.md](training/docs/PROMPTS.md) |
| [guide/fields/](guide/fields/README.md) | 서류 476종의 항목 키·항목명·타입·체크박스 보기 (정보 추출·체크 질문에 넣을 항목) |
| [guide/documents.md](guide/documents.md) | 서류 정식 명칭 476종, 업무 12종별 필수 서류 |
| [guide/benchmark.md](guide/benchmark.md) | 은행 업무 벤치마크: 과제, 문항 만드는 방법, 불일치 14종과 근거, 채점 규칙 |

**실행과 결과**

| 문서 | 들어 있는 것 |
|---|---|
| [training/README.md](training/README.md) | 1부 OCR 학습 파이프라인 요약 (`run_pipeline.py`). 상세는 [training/docs/](training/docs/): `SETUP.md` 설치·사내 OCR 서버 연결, `PIPELINE.md` 옵션, `DESIGN.md` 과제·지표·보상 설계, `MANUAL.md` 단계별 수동 실행 |
| [training/BANK_TASKS.md](training/BANK_TASKS.md) | 2부 은행 업무 파이프라인 (`run_bank_pipeline.py`): 설정 항목 전체, GPU별(80GB/40GB) 설정, 단계별 내용, 시간 |
| [guide/results.md](guide/results.md) | 결과 점수표 읽는 법: 지표 뜻, 찍어도 나오는 점수, 오차 범위, 학습 로그, 이상 신호와 대처 |
| [training/viewer/README.md](training/viewer/README.md) | viewer 두 개: OCR viewer(`start.sh`, 포트 7860), 은행 업무 viewer(`bank_start.sh`, 포트 7861) |
| [docs/DOCKER.md](docs/DOCKER.md) | 합성 데이터를 만드는 docgen 도커 설치와 SSH 접속 |
| [docs/DOCGEN.md](docs/DOCGEN.md) | 합성 서류 생성기 자체 (설치, 명령, 출력 형식, 서식) |

## 코드 위치와 브랜치

| 폴더 | 내용 |
|---|---|
| `docgen/`, `scripts/make_bank_data.sh` | 합성 서류 생성기, 2부 데이터 만들기 (도커에서 실행) |
| `training/` | GPU 학습 프로젝트. 1부 `run_pipeline.py`, 2부 `run_bank_pipeline.py`, `viewer/` |
| `guide/` | 위 사용 가이드 |

- **이 브랜치(`claude/ocr-banking-benchmark`)에 전부 들어 있습니다.**
- `training/`의 OCR 코드는 OCR 브랜치(`claude/bank-ocr-pipeline`)와 같습니다. OCR 쪽을 고치면 `git merge -X subtree=training origin/claude/bank-ocr-pipeline`으로 가져옵니다.
- 모든 합성 데이터는 실존 인물·사업자와 무관합니다.
