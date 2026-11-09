# 처음부터 끝까지 한 번

평가 세트와 학습 데이터를 만들고, 학습하고, 결과를 보는 것까지 한 번 따라 합니다. 단계마다 화면 이름이나 명령 하나이고, 자세한 것은 단계 끝의 문서에 있습니다.
무엇을 하는 저장소인지는 [README](../README.md), studio 화면 쓰는 법은 [studio.md](studio.md).

처음 보는 말(서식·칸·키·문항·레시피·seed·SFT·GRPO …)은 [용어 한 장](terms.md).

## 0. 준비

| 어디 | 확인 |
|---|---|
| studio 서버 | studio 가 떠 있고 브라우저로 `http://localhost:8765` 가 열림 (접속은 [studio.md](studio.md#접속), 처음 설치는 [docker/README.md](../docker/README.md)) |
| GPU 학습 서버 | 코드 폴더에서 `python -c "import swift, vllm, train; print('ok')"`, `nvidia-smi` 로 빈 GPU, studio 저장 폴더가 보임 ([training.md 0절](training.md#0-처음-한-번)) |

## 1. 문항이 어떻게 생겼는지 보기

studio 왼쪽 메뉴 **서식** › 아무 서식 › **개요**(그 서식이 묻는 것: 칸·표·체크, 상태) 와 **질문·답**(실제로 나오는 질문·정답).
OCR 과제는 **OCR 예시** 메뉴. 모든 과제의 실제 문항은 [tasks.md](tasks.md).

## 2. 평가 세트 만들기

studio **데이터셋 › 새로 만들기** 표에서 레시피 `bank-bench` 줄(용도 열이 **평가 세트**)의 이름 칸에 예 `bench-v1` → **만들기**. 용도는 레시피가 정합니다.

- 처음에는 작게 만들어 **데이터셋 › 그 데이터셋 › 문항**에서 그림과 정답 박스가 맞는지 눈으로 봅니다. 괜찮으면 크게 만듭니다.
  작게 만들려면 `bank-bench` 를 고치지 말고 **틀에서 새 레시피 › bank-try** 로 시험용 레시피를 따로 만듭니다 (`bank-bench` 를 고치면 저장소의 `docgen/recipes/bank-bench.json` 이 바뀜).
- 이미 쓰는 평가 세트가 있으면 새로 만들지 않고 그것을 씁니다 (실험끼리 비교하려면 고정).
- 자세히: [data.md](data.md) (레시피 칸, 명령으로 만들기 `remote_build.py`)

## 3. 학습 데이터 만들기

같은 표에서 레시피 `bank-train` 줄(용도 **학습 데이터**), 이름 예 `train-v1` → **만들기**. OCR 능력도 같이 학습하려면 `ocr-train` 도 하나 만듭니다.

- 평가 세트로 만든 데이터셋을 학습에 쓰지 않습니다.
- 자세히: [data.md 2~4절](data.md#2-무엇을-만들지-정하기)

## 4. 학습 설정 만들기

studio **데이터셋 › (평가 세트 하나) › 학습** 탭에서 학습 데이터와 평가 세트를 고르고 **설정 파일 쓰기** → studio 쪽 코드 폴더에 `train/configs/studio-<이름>.json` 이 생깁니다.
학습 서버가 같은 코드 폴더를 보면 그대로 쓰고, 아니면 이 파일을 학습 서버 코드 폴더의 `train/configs/` 로 복사합니다 (데이터 경로는 저장 폴더를 가리키므로 파일만 옮기면 됨. 학습 서버에서 저장 폴더가 `/out` 이 아닌 경로면 [training.md 2절](training.md#2-설정-파일)의 `path_map`).
학습 서버에서 그 파일의 `model`(출발 모델 폴더)·`gpus` 만 확인하고 리허설합니다.

```bash
python -m train --config train/configs/studio-<이름>.json --smoke     # 몇 분. <workdir>/smoke/reports/benchmark.html 이 생기면 됨
```

- 실서류 추출 데이터(`.jsonl`)를 평가 세트로 더하거나 채점 방식을 바꾸려면 [eval.md 1·2절](eval.md#1-평가-세트-정하기).
- 자세히: [training.md 2절](training.md#2-설정-파일)

## 5. 학습

```bash
nohup python -m train --config train/configs/studio-<이름>.json > <이름>.log 2>&1 &
```

섞기 → 출발 모델 평가 → SFT → 평가 → GRPO → 평가 → 보고서까지 한 번에 돕니다. 멈추면 **같은 명령을 다시** 실행합니다 (끝난 단계는 건너뜀).
SFT 까지만은 `--part sft`. 에러는 [training.md 6절](training.md#6-에러).

## 6. 결과 보기

`<workdir>/reports/summary.html` 하나를 엽니다. 평가 세트·과제마다 주 지표 한 줄, 열은 출발 → SFT → GRPO 모델입니다.

1. **답 형식 오류**가 SFT 뒤 거의 0% 인지 (아니면 SFT 가 덜 됐거나 답이 잘림)
2. 과제별 점수가 출발 모델보다 얼마나 올랐는지 (괄호 %p)
3. **찍어도 나오는 점수**(기준선)보다 충분히 높은지, 문항 수가 적은 과제는 오차가 큰지
4. OCR 열이 출발 모델보다 크게 떨어지지 않았는지
5. 이상한 칸은 `reports/answers.html` 에서 문항별 모델 답을 봅니다
6. 실서류 한 장이나 궁금한 그림에 직접 물어보려면 학습 서버에서 `python -m playground` ([playground](../playground/README.md))

자세히: [results.md](results.md)

## 그다음

| 하고 싶은 것 | 문서 |
|---|---|
| 서식의 값·위치·모양·질문이 마음에 안 듦 → 고친 뒤 데이터를 다시 만들기 | [서식 고치기](../docgen/forms/README.md) |
| 없는 서식을 더하기 | [new-forms.md](new-forms.md) |
| 학습률·데이터·출발 모델을 바꾼 모델 여러 개를 한 번에 | [training.md 4절](training.md#4-여러-모델을-한-번에-실험-묶음) |
| 새 평가 세트로 이미 학습한 모델을 평가, 채점 방식만 바꿔 다시 채점 | [eval.md 3·4절](eval.md#3-학습-없이-평가만-하기) |
| 실험 기록 남기기 | [experiments/](../experiments/README.md) |
