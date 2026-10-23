# AGENTS.md

이 저장소에서 일하는 agent가 먼저 읽는 안내입니다. 실제 수행 절차는 [guide/agent-workflow.md](guide/agent-workflow.md)에 있습니다.

## 프로젝트

은행 서류 VLM(Qwen3.5-9B)을 OCR·문서 이해·업무 처리 과제로 학습하고 평가합니다.

| 폴더 | 하는 일 | 어디서 실행 |
|---|---|---|
| `docgen/` | 합성 서류·문항 생성, 채점(`docgen.bench.evaluate`), OCR 준비 | studio 컨테이너 (생성), 학습 서버 (OCR 준비) |
| `studio/` | 웹 화면 + API: 데이터셋 생성·등록·채점, 학습 설정 내보내기 | studio 컨테이너 |
| `train/` | `python -m train`: 섞기 → SFT → GRPO → 평가 → 비교표 | GPU 학습 서버 |
| `docker/` | studio 컨테이너, 원격 생성 클라이언트 `remote_build.py` | |
| `guide/` | 사용 설명서 | |

## 작업별 문서

| 작업 | 문서 |
|---|---|
| 데이터 생성 → 학습 → 평가 → 보고 (전체 절차) | [guide/agent-workflow.md](guide/agent-workflow.md) |
| 학습 설정·실행·에러 | [guide/training.md](guide/training.md), 설정 칸 [train/README.md](train/README.md) |
| 학습한 모델을 새 평가 세트로 다시 채점 | [guide/eval.md](guide/eval.md) |
| 실서류 이미지 OCR 준비 | [guide/ocr.md](guide/ocr.md) |
| 결과 지표 해석 | [guide/results.md](guide/results.md) |
| 실험 기록 (가설·설계·결과) | [experiments/README.md](experiments/README.md) |
| 서식 ID·추출 항목·연결 업무 | [guide/catalog.json](guide/catalog.json), `remote_build.py catalog` |
| 과제별 질문·정답 형식 | [guide/questions.md](guide/questions.md), 실제 예시 [guide/tasks.md](guide/tasks.md) |
| 과제·채점 규칙 | [guide/benchmark.md](guide/benchmark.md) |
| studio 화면 기능 | [guide/studio.md](guide/studio.md), 전체 [studio/README.md](studio/README.md) |
| 코드 설계 | [studio/DESIGN.md](studio/DESIGN.md), [docgen/README.md](docgen/README.md) |

## 규칙

1. **요청 범위만 실행합니다.** 받은 범위(예: "SFT 한 번 + 분석")를 작업 시작 때 적어 두고, 결과가 아쉬워도 GRPO·추가 학습·대규모 생성을 스스로 시작하지 않습니다. 제안으로 보고합니다.
2. **실행 위치를 구분합니다.** studio에 접속된다고 GPU 학습을 할 수 있는 것이 아닙니다. 학습은 학습 서버에서만, 생성은 studio(직접 또는 `remote_build.py`)로만 합니다.
3. **지원되는 API·CLI로 작업합니다.** studio 저장 폴더의 파일(`registry.json`, 데이터셋 폴더)을 직접 고치지 않습니다.
4. **덮어쓰지 않습니다.** 평가 세트, 원본 서류, 기존 데이터셋·`workdir`·`output_dir`은 지우거나 덮어쓰지 않습니다. 새 결과는 새 이름으로.
5. **있는 것은 재사용합니다.** 만들기 전에 같은 데이터셋·결과가 있는지 확인합니다 (`remote_build.py jobs`, `find … -name meta.json`, `<workdir>/state.json`). 평가 세트는 실험 간 비교를 위해 고정합니다.
6. **평가 세트를 학습에 넣지 않습니다.** `data.train`과 `data.benchmark`에 같은 데이터셋을 넣지 않습니다 (실서류 OCR 준비 폴더는 예외: 안에서 나뉨).
7. **사람 검수와 자동 검사를 구분합니다.** 형식 검사 통과를 "검수 완료"로 보고하지 않습니다. 이미지·정답의 시각적 확인은 사람에게 요청합니다.
8. **ID는 조회합니다.** 서식·업무·데이터셋 ID를 추측하지 않고 `remote_build.py types|scenarios|jobs`로 확인합니다.
9. **실패는 두 번까지.** 같은 단계에서 같은 에러가 두 번 나면 멈추고 로그 끝과 함께 보고합니다.
10. **실서류는 밖으로 보내지 않습니다.** 실서류 이미지를 외부 모델·서비스에 보내지 않습니다.

## 검증

```bash
python -m pytest                    # 코드를 고쳤을 때 (docgen/tests, studio/tests, train/tests)
python -m train --config <설정> --smoke   # 학습 설정을 만들었을 때
```

완료 보고 항목(데이터 버전, 설정, 모델, 점수, 경로)은 [agent-workflow.md 7절](guide/agent-workflow.md#7-결과-분석보고)에 있습니다.
