# Studio 사용법

studio는 서식을 보고 고치고, 합성·실서류 데이터셋을 만들어 등록하고, 모델 답을 채점해 비교하는 웹 화면입니다.
만든 데이터셋은 학습([training.md](training.md))에 경로만 적어 씁니다.

## 1. 띄우기·접속

내부망 Linux 서버의 코드 폴더에서 (처음 설치는 [docker/README.md](../docker/README.md) 1·2절):

```bash
sh docker/studio.sh --data /database/docgen_studio    # 처음 한 번: 저장 폴더를 정해 띄우기
sh docker/studio.sh                                   # 다음부터
```

윈도우 PC에서 터널을 열고 브라우저로 `http://localhost:8765`에 들어갑니다.

```powershell
ssh -N -L 8765:localhost:8765 <계정>@<서버IP>
```

- 데이터셋은 `<저장 폴더>/workspace/datasets/<이름>/`에 생깁니다. 컨테이너 안에서는 `/out/...`으로 보입니다.
- 다른 컨테이너에서 API로 쓰려면 `sh docker/studio.sh --open` (로그인 없음. 실서류를 다룰 때는 `--local`로).
- 그 밖의 명령(로그, 셸, 포트, 코드 업데이트)은 [docker/README.md](../docker/README.md) 3·4절.

## 2. 합성 데이터 만들기

**⑥ 데이터셋 › 새로 만들기**에서 레시피를 고르고 이름을 정해 **만들기**를 누릅니다. 끝나면 아래 목록에 자동으로 등록됩니다.

| 레시피 | 만드는 것 |
|---|---|
| `bank-bench` | 은행 업무 평가 세트 (서식 문항 + 업무 12종 묶음) |
| `bank-train` | 은행 업무 학습 데이터 |
| `ocr-bench` · `ocr-train` | 합성 OCR 평가 세트 · 학습 데이터 (서식을 그려 쪽 전체 글자를 정답으로) |

- OCR 레시피는 만들 때 OCR 준비(`docgen.bench.ocr_prepare`)까지 studio가 돌립니다. 서류를 다 그린 뒤 작업 진행이 "그림 확인 → OCR → 문항 만들기"로 이어지고, `<이름>/prepared/DONE.json`이 생겨야 끝입니다 (그 전에는 목록에 안 뜸). 학습에는 `<이름>/prepared` 경로를 적습니다.
- **용도**를 꼭 확인합니다: 평가 세트(`test`/`benchmark`) 또는 학습(`train`). 학습과 평가는 서로 다른 고객으로 만들어집니다.
- 서식·업무·수량·촬영 조건·대조 사례는 레시피에서 고칩니다. 칸의 뜻은 [agent-workflow.md 3절](agent-workflow.md#3-레시피-정하기)에 표로 있습니다.
- 처음에는 작게 만들어 ⑥ › 문항에서 그림과 정답을 본 뒤 크게 만듭니다.
- `bank-*` 레시피는 **기타 칸 정리**(`freetext`) 문항도 만듭니다. 비고·기타·사유·용도 칸 일부에 `3천 정도 1년, 담달 말까지 서류 낼게요`처럼 **일부러 대충 쓴 글**이 들어갑니다 (이상한 값이 아님). 이 칸은 대부분 하나은행 서식에 있어서, 하나은행 서식을 빼면 거의 생기지 않습니다. 질문·채점은 [questions.md](questions.md#freetext--기타-칸-정리).
- 명령줄로 만들기: 다른 컨테이너에서 `docker/remote_build.py` ([agent-workflow.md](agent-workflow.md)), 컨테이너 안에서 `bash docgen/scripts/make_bank_data.sh` (평가 세트 + 학습 데이터 통째, 약 1시간 15분).

## 3. 내 서류 넣기

| 가진 것 | 메뉴 | 결과 |
|---|---|---|
| 서류 이미지만 (OCR 데이터로) | ④ 가져오기 › 이미지 묶음 → (⑤ OCR 검수) → **OCR 벤치마크로** | OCR 데이터셋. 명령줄로는 [ocr.md](ocr.md) |
| 이미지 + 정답 라벨 JSON | ④ 가져오기 › 라벨 있는 데이터 | 은행 업무·OCR 데이터셋. 라벨 형식 [LABEL_FORMAT.md](../studio/LABEL_FORMAT.md) |
| 이미 돌린 OCR·추론 결과 폴더 | ④ 가져오기 › 결과 폴더 | 묶음. 형식 [RESULTS_FORMAT.md](../studio/RESULTS_FORMAT.md) |
| 새 양식 (합성에 추가) | ④ 포맷 열기 › 템플릿으로 → ① 영역 편집·검수 | 새 서식 |

파일 배치·설정 예시는 [DATA_IMPORT.md](../studio/DATA_IMPORT.md)에 있습니다.

검수한 실서류 추출 데이터(swift `.jsonl`)는 studio를 거치지 않고 학습 설정에 바로 넣습니다. 평가 세트로는 [eval.md 1절](eval.md#1-평가-세트-정하기), 학습 데이터로는 [training.md 2절](training.md#2-설정-파일).

## 4. 보기·채점·비교

| 하고 싶은 것 | 메뉴 |
|---|---|
| 문항의 그림·질문·정답 박스 보기 | ⑥ 데이터셋 › 데이터셋 › 문항 |
| 모델 답 붙여 채점 | ⑥ › 모델 답 (학습 `workdir` 또는 답 파일) |
| 여러 모델·데이터셋 점수 한 표 | ⑦ 평가 |
| 구성(업무·시나리오·정답 구조별 수량) | ⑥ › 구성·추적 ([benchmark-tracking.md](benchmark-tracking.md)) |
| 학습 설정 만들기 | ⑥ › 학습 탭 → `train/configs/studio-<이름>.json` ([training.md](training.md)) |
| OCR 8과제 예시 (데이터셋 없이) | **OCR 예시** 메뉴 |
| 서식별 추출 항목·연결 업무 | ① 서식 › 추출·시나리오, 사용 가이드 › 카탈로그 ([catalog.md](catalog.md)) |
| 서식 하나 한눈에: 항목·위치·정한 곳·질문→답 예시·고치는 곳 | ① 서식 › **카드** (서식 폴더의 `FORM.md`, [다시 만들기]) — [서식 폴더 설명서](../docgen/forms/README.md) |
| 실제로 나오는 질문·정답, 이 서식에서 바꾼 질문 `questions.json`·이 서식만의 질문 `qa.py` | ① 서식 › 문항 Q/A ([questions.md](questions.md), 고치기 [서식 폴더 설명서](../docgen/forms/README.md)) |

채점은 학습 보고서와 같은 함수(`docgen.bench.evaluate`)라 점수가 같습니다. 평가 세트에 채점 함수(`scorer`)를 붙인 경우는 학습 보고서 쪽 점수를 봅니다.

## 5. 서식 고치기·만들기

| 하고 싶은 것 | 메뉴 |
|---|---|
| 서식 미리보기, 값 영역 옮기기·추가 | ① 서식 › 미리보기 / 영역 편집 |
| 검수 완료 표시, 학습·평가 배정 | ① 서식 › 검수 |
| html 서식 복제·편집 | ① 서식 › 복제 / html 편집 |
| 폴더로 넣은 새 서식을 목록에 올리기 (다시 띄우지 않고) | ① 서식 › **서식 다시 읽기** ([new-forms.md](new-forms.md)) |
| 새 서식 추가 절차 한 화면 (모델 지시문 복사, 검사·넣기 명령, 서식 다시 읽기) | 왼쪽 메뉴 **새 서식 추가** |
| 업무별 필요 서류·대조·심사 설정 | ③ 시나리오·묶음 |
| 체크·도장·서명 확률과 모양 | ② 표시 요소 |

검수 완료 전의 가져온 서식은 레시피의 `"all"`·그룹 선택에 들어가지 않습니다.
메뉴별 전체 기능과 고친 것이 저장되는 파일은 [studio/README.md](../studio/README.md)에 있습니다.
