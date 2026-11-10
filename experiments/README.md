# 실험 기록

실험 하나에 파일 하나: `experiments/E<번호>-<짧은이름>.md` (예: `E01-realgap.md`; E01 은 예전 꼴 `E01_add-realocr.md` 그대로 둠). 새 실험은 [_template.md](_template.md)를 복사해 시작합니다.

## 목록

| ID | 가설 | 상태 | 결론 |
|---|---|---|---|
| [E01_add-realocr](E01_add-realocr.md) | 합성만으로 실서류가 좋아지나 · 다른 도메인 OCR 추가가 추출·OCR(같은/다른 도메인)에 주는 효과 | 진행 | |

상태: 계획 · 진행 · 완료 · 중단

## 이름 규칙

| 대상 | 꼴 | 예 |
|---|---|---|
| 실험 | `E<번호>-<짧은이름>` | `E01-realgap` |
| 모델 (= 묶음의 `label`·비교표 라벨, `workdir`는 `<root>/<label>/`) | `<팔>-<데이터>` (묶음 밖 단독 실행은 `e<번호>-<팔>-<데이터>`), seed 여러 번이면 `-s1` | `a2-synreal`, `e01-a2-synreal` |
| 학습 데이터셋 | `<종류>-v<버전>` | `syn-v1`, `real-masked-v1` |
| 평가 세트 | `eval-<종류>-v<버전>` (실험 간 고정) | `eval-real-v1` |

이미 쓴 이름은 고치지 않고 버전을 올립니다. 영문 소문자·숫자·`-`만.

## 적는 원칙

- 설정을 바꾼 모델 여러 개는 실험 묶음으로 돌립니다 ([sweep.md](../guide/train/sweep.md)). 묶음 파일의 `name`은 실험 ID, `record`는 이 폴더의 기록 파일로 적고, 결과는 `<root>/report.html`·`scores.csv`에서 옮깁니다. 여러 실험 비교는 평가만 하기에 묶음 결과 폴더를 같이 적습니다 ([steps.md 2절](../guide/train/steps.md#2-평가만-하기-python--m-train-eval)).
- 결과에는 데이터 버전·설정 파일·모델 경로(`results.json`)를 함께 적습니다 ([AGENTS.md 보고](../AGENTS.md#보고)).
- 점수는 `<root>/scores.csv`에서 옮깁니다. 지표 해석은 [guide/train/sweep.md](../guide/train/sweep.md#5-결과).
- 평가에서 빠진 문항(그림이 서버 한도보다 많은 문항, 보고서 알림)이 있으면 수를 적습니다.
- 사람이 본 것(검수)과 자동 검사를 구분해 적습니다.
