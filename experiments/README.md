# 실험 기록

실험 하나에 파일 하나: `experiments/E<번호>-<짧은이름>.md` (예: `E01-realgap.md`). 새 실험은 [_template.md](_template.md)를 복사해 시작합니다.

## 목록

| ID | 가설 | 상태 | 결론 |
|---|---|---|---|
| [E01_add-realocr](E01_add-realocr.md) | 합성만으로 실서류가 좋아지나 · 다른 도메인 OCR 추가가 추출·OCR(같은/다른 도메인)에 주는 효과 | 진행 | |

상태: 계획 · 진행 · 완료 · 중단

## 이름 규칙

| 대상 | 꼴 | 예 |
|---|---|---|
| 실험 | `E<번호>-<짧은이름>` | `E01-realgap` |
| 모델 (= `workdir`, 비교표 라벨) | `e<번호>-<팔>-<데이터>`, seed 여러 번이면 `-s1` | `e01-a2-synreal` |
| 학습 데이터셋 | `<종류>-v<버전>` | `syn-v1`, `real-masked-v1` |
| 평가 세트 | `eval-<종류>-v<버전>` (실험 간 고정) | `eval-real-v1` |

이미 쓴 이름은 고치지 않고 버전을 올립니다. 영문 소문자·숫자·`-`만.

## 적는 원칙

- 학습 데이터만 바꾼 모델 여러 개는 실험 묶음으로 돌립니다 ([training.md 4.1절](../guide/training.md#41-학습-데이터만-바꾼-모델-여러-개-실험-묶음)). 묶음 파일의 `name`은 실험 ID, `record`는 이 폴더의 기록 파일로 적고, 결과는 `<root>/compare.md`에서 옮깁니다.

- 결과에는 데이터 버전·설정 파일·모델·`workdir` 경로를 함께 적습니다 ([agent-workflow.md 7절](../guide/agent-workflow.md#7-결과-분석보고)).
- 점수는 `<workdir>/reports/*.json`에서 옮깁니다. 지표 해석은 [guide/results.md](../guide/results.md).
- 평가에서 빠진 문항(그림 한도 초과 `benchmark_over_image_limit.jsonl`, 건너뛴 묶음 `skipped_bundles.jsonl`)이 있으면 수를 적습니다.
- 사람이 본 것(검수)과 자동 검사를 구분해 적습니다.
