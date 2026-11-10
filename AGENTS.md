# AGENTS.md

이 저장소에서 일하는 agent(LLM)가 먼저 읽는 안내입니다. 무엇을 하는 저장소인지는 [README.md](README.md), 말 뜻은 [guide/terms.md](guide/terms.md) (같은 것의 여러 이름 정리).

## 작업별 문서

받은 일에 맞는 문서 하나를 끝까지 따릅니다.

| 작업 | 문서 |
|---|---|
| studio 화면이 무엇을 하는지 (서식 · 새 서식 추가 · 데이터셋) | [guide/studio.md](guide/studio.md) |
| 데이터셋 만들기 (평가 세트·학습 데이터, `docker/remote_build.py`) | [guide/data.md](guide/data.md) |
| 학습 (설정·실행·실험 묶음·에러) | [guide/training.md](guide/training.md), 설정 칸 [train/README.md](train/README.md) |
| 평가 세트·채점 함수, 학습 없이 평가만, 다시 채점 | [guide/eval.md](guide/eval.md) |
| 결과 분석·보고 | [guide/results.md](guide/results.md), 아래 "보고" |
| 모델을 그림 한 장으로 써 보기 (사람이 보는 화면) | [playground/README.md](playground/README.md) |
| **서식 하나 고치기** (값·위치·모양·칸·질문·답·채점) | [docgen/forms/README.md](docgen/forms/README.md) 0절 표 → 그 서식의 카드 `docgen/forms/<ID>/FORM.md` |
| 새 서식 추가 (그림 위에 칸 그리기, overlay 만) | 절차 [guide/new-forms.md](guide/new-forms.md), 칸의 키 [guide/keys.md](guide/keys.md), 값 만드는 코드 [guide/generators.md](guide/generators.md) |
| 이미 있는 html 서식을 코드로 고치기 | 형식 [docgen/manual/NEW_FORM_SPEC.md](docgen/manual/NEW_FORM_SPEC.md), 모양만 [docgen/manual/FORM_SHELL_GUIDE.md](docgen/manual/FORM_SHELL_GUIDE.md) |
| 서식 모양(껍데기)만 원본에 맞게 | [docgen/manual/FORM_SHELL_GUIDE.md](docgen/manual/FORM_SHELL_GUIDE.md) |
| 실서류 이미지 OCR 준비 | [guide/ocr.md](guide/ocr.md) |
| 과제별 질문·답·채점 규칙 (참고) | [guide/benchmark.md](guide/benchmark.md), 질문 원문 [guide/questions.md](guide/questions.md) |
| 실험 기록 | [experiments/README.md](experiments/README.md) |

`archive/` 는 지난 기록입니다. 지금 절차로 읽지 않습니다.

## 어디서 실행하나

| | 하는 일 |
|---|---|
| **studio 컨테이너** | 데이터 생성. 다른 곳에서는 HTTP 로만 (`STUDIO_URL`, `python docker/remote_build.py`) |
| **GPU 학습 서버** | 학습·평가 (`python -m train`), 실서류 OCR 준비. ms-swift·vLLM·GPU 가 있는 곳 |
| **사람** | 그림·정답의 눈 확인, 검수 완료 표시. agent 는 요청하고 기다림 |

시작할 때 필요한 곳에 닿는지 확인하고, 안 되는 것은 보고한 뒤 그 단계를 빼고 계획합니다
(`python docker/remote_build.py recipes` · 학습 서버 `python -c "import swift, vllm, train; print('ok')"`, `nvidia-smi`).

## 규칙

1. **요청 범위만 실행합니다.** 받은 범위(예: "SFT 한 번 + 분석")를 작업 시작 때 적어 두고, 결과가 아쉬워도 GRPO·추가 학습·대규모 생성을 스스로 시작하지 않습니다. 제안으로 보고합니다.
2. **실행 위치를 구분합니다.** studio에 접속된다고 GPU 학습을 할 수 있는 것이 아닙니다. 학습은 학습 서버에서만, 생성은 studio(직접 또는 `remote_build.py`)로만 합니다.
3. **지원되는 API·CLI로 작업합니다.** studio 저장 폴더의 파일(`registry.json`, 데이터셋 폴더)을 직접 고치지 않습니다.
4. **덮어쓰지 않습니다.** 평가 세트, 원본 서류, 기존 데이터셋·`workdir`·`output_dir`은 지우거나 덮어쓰지 않습니다. 새 결과는 새 이름으로.
5. **있는 것은 재사용합니다.** 만들기 전에 같은 데이터셋·결과가 있는지 확인합니다 (`remote_build.py jobs`, `find … -name meta.json`, `<workdir>/state.json`). 평가 세트는 실험 간 비교를 위해 고정합니다.
6. **평가 세트를 학습에 넣지 않습니다.** `data.train`과 `data.benchmark`에 같은 데이터셋을 넣지 않습니다 (실서류 OCR 준비 폴더는 예외: 안에서 나뉨).
7. **사람 검수와 자동 검사를 구분합니다.** 형식 검사 통과를 "검수 완료"로 보고하지 않습니다. 이미지·정답의 시각적 확인은 사람에게 요청합니다 — 요청할 때 화면을 적습니다: 서식은 studio **서식 › <서식> › 그림·검수 › 미리보기/검수**, 데이터셋은 **데이터셋 › <이름> › 문항**.
8. **ID는 조회합니다.** 서식·업무·데이터셋 ID를 추측하지 않고 `remote_build.py types|scenarios|jobs`로 확인합니다.
9. **실패는 두 번까지.** 같은 단계에서 같은 에러가 두 번 나면 멈추고 로그 끝과 함께 보고합니다.
10. **실서류는 밖으로 보내지 않습니다.** 실서류 이미지를 외부 모델·서비스에 보내지 않습니다.

## 설정으로 안 되는 것

- 목록에 없는 서식 → 서식 추가 ([guide/new-forms.md](guide/new-forms.md)).
- 서식 하나에만 묻는 질문 → 그 서식의 `qa.py` (과제 `form_qa`). 모든 서식에 같은 새 과제, 새 대조 사례·심사 규칙 → 생성·채점 코드 추가 (사람과 상의).
- 특정 값·사건의 정확한 개수 → 레시피는 비율만 정함. 생성 후 골라냄.
- 고르기 창에 없는 칸 값 → 보기·틀(화면) 먼저. 함수가 필요하면 `docgen/forms/_common/generators.py` 에 **함수를 더하는 것만** 허용 (모든 서식에 영향 — 기존 함수는 고치지 않고, 더한 함수를 보고). 칸끼리 관계는 그 서식 폴더의 `generate.py` ([guide/generators.md](guide/generators.md)).
- 실제 고객 데이터 성능 → 합성 점수는 실서류보다 높게 나옴. 검수한 실서류 평가 세트로 따로 봄 ([guide/eval.md 1절](guide/eval.md#1-평가-세트-정하기)).

## 검증

```bash
python -m pytest                                  # 코드를 고쳤을 때 (docgen/tests, studio/tests, train/tests, playground/tests)
python -m docgen.formdir check <ID>               # 서식을 고쳤을 때 (+ card <ID>)
python -m train --config <설정> --smoke            # 학습 설정을 만들었을 때
```

## 보고

학습·평가를 맡았으면 끝날 때 아래를 적습니다. 결과는 `<workdir>/reports/summary.html` 부터 [results.md](guide/results.md) 의 읽는 순서로 봅니다
(형식 오류율 → 출발 대비 변화 → 기준선·오차 → OCR 열 → 대표 오답).

| 항목 | 예 |
|---|---|
| 요청 범위와 실제 실행한 단계 | SFT까지, `state.json` 의 `done` |
| 데이터 | 데이터셋 이름·경로, 레시피, 생성기 커밋·버전(`dataset.json`), 과제별 문항 수 |
| 설정 | 설정 파일 경로, 모델, GPU, `data.output_dir`, 바꾼 칸, 평가 세트별 채점 함수(`scorer`, 없으면 기본) |
| 결과 | 과제별 주 지표 표 (출발/SFT/GRPO), 형식 오류율. 오차 범위 안의 차이는 "차이 없음" |
| 확인 안 된 것 | 사람 검수를 받지 못한 것, 건너뛴 단계 |
| 경로 | `<workdir>/reports/summary.html`·`benchmark.html`·`answers.html` (묶음은 `<root>/summary.html`·`compare.html`), 로그 폴더, 모델 `<workdir>/merged/…` |
| 다음 제안 | 실행하지 않은 추가 실험 |

서식을 고쳤으면: 바꾼 파일, `formdir check` 결과, 미리보기 그림 경로, 판단이 안 선 곳, 사람이 볼 것(그림·정답).
