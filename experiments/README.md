# 실험 기록

실험 하나에 파일 하나: `experiments/E<번호>-<짧은이름>.md` (예: `E01-realgap.md`). 새 실험은 [_template.md](_template.md)를 복사해 시작합니다.

## 목록

| ID | 가설 | 상태 | 결론 |
|---|---|---|---|
| [E01-realocr](E01-realocr.md) | 하나은행 서식 없이 학습해도 키 설명으로 추출 가능 · 실서류 OCR 추가 효과 · 대상 문서 OCR만으로 추출 향상 | 계획 | |

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

- 결과에는 데이터 버전·설정 파일·모델·`workdir` 경로를 함께 적습니다 ([agent-workflow.md 7절](../guide/agent-workflow.md#7-결과-분석보고)).
- 점수는 `<workdir>/reports/*.json`에서 옮깁니다. 지표 해석은 [guide/results.md](../guide/results.md).
- 평가에서 빠진 문항(그림 한도 초과 `benchmark_over_image_limit.jsonl`, 건너뛴 묶음 `skipped_bundles.jsonl`)이 있으면 수를 적습니다.
- 사람이 본 것(검수)과 자동 검사를 구분해 적습니다.
