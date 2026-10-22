# 벤치마크 생성 구성과 평가 추적

벤치마크는 하나의 과제 폴더로 저장하면서, 업무·시나리오·정답 구조·서식별로 따로 조회하고 채점합니다. 파일을 여러 세트로 복제하지 않고 문항 메타데이터로 같은 집합을 추적합니다.

| 기준 | 예시 | 용도 |
|---|---|---|
| 업무·과제 그룹 `task_group` | `ocr`, `doc`, `work` | OCR / 문서 이해 / 은행 업무 구분 |
| 과제 `task` | `crop_ocr`, `kie`, `doc_check`, `cross_check`, `review` | 같은 채점 방식끼리 비교 |
| 업무 시나리오 `scenario` | `mortgage`, `jeonse_loan` | 주택담보·전세 등 업무별 성능 확인 |
| 정답 구조 `label_format` | `text`, `text_boxes`, `key_values`, `mark_states`, `document_sets`, `consistency_issues`, `scalar`, `text_list` | 텍스트·좌표·추출·표시·업무 판단 구분 |
| 서식 `doc_type` | `employment_certificate` | 어떤 서식에서 실패했는지 확인 |
| 원본 데이터셋 `source_dataset` | `bench-a@<메타데이터 해시>` | train에서 여러 폴더를 섞어도 출처 추적 |

`key_values`와 `mark_states`에는 해당 문항 계약에 따라 위치가 포함됩니다. 실제 답 규격은 문항과 [질문·정답](questions.md)을 확인합니다. 이 구분은 정답 구조이며, 필드 타입(이름·금액·날짜·체크·서명 등)과는 별개입니다.

## Studio에서 확인

1. **데이터셋 → 해당 데이터셋 → 구성·추적**을 엽니다.
2. **전체 문항 / 평가 문항**을 선택해 업무·시나리오·과제·정답 구조별 수량을 확인합니다. 문항 수 버튼으로 해당 구성의 실제 문항을 엽니다.
3. **문항** 탭에서도 그룹·시나리오·정답 구조·서식을 각각 필터링할 수 있습니다. 여러 과제를 함께 보려면 과제 선택을 **과제 전체**로 바꿉니다. 선택한 필터는 모두 동시에 적용됩니다.
4. **모델 답**에서 모델 결과를 연결하고 채점합니다.
5. **구성·추적 → 구분별 평가 결과**에서 채점 결과와 구분을 선택합니다. 업무·과제 그룹별·시나리오별·정답 구조별·서식별로 과제별 지표를 확인합니다.
6. 구분에서 **필드 타입 · 항목 단위**를 선택하면 KIE·체크/도장/서명 문항의 필드별 값 정확도를 확인합니다. 구성표의 필드 수와 평가의 문항 수는 다른 단위입니다.

이전 저장 점수에 구분별 결과가 없으면 재채점이 필요하다고 표시합니다. 이전 데이터셋은 원본을 바꾸지 않고 기록된 메타데이터에서 구성을 읽습니다. 기록하지 않은 시나리오나 서식을 파일 이름으로 추측하지 않습니다.

## 생성 파일에 남는 것

- bank 생성과 OCR 준비의 `meta.json`에는 `composition`이 포함됩니다. 그룹·과제·시나리오·정답 구조별 문항 수와 교차 구성표를 기록합니다.
- 문항의 `meta.task_group`, `meta.label_format`을 함께 기록합니다. 업무 시나리오는 기존 `meta.scenario`를 유지합니다.
- `train`에서 과제 폴더를 읽을 때 `meta.source_dataset`이 없으면 붙이며, 평가 정답 파일에도 유지합니다. 이미 기록된 출처는 보존합니다. 자동 식별자는 폴더 이름과 원본 `meta.json`의 해시로 만들며 이미지 내용의 해시를 대신하지 않습니다.
- 합성 OCR의 서식·촬영 조건·레이아웃 변형 정보는 `manifest.jsonl → pages.jsonl → OCR 문항 → tasks/*.jsonl`까지 유지합니다. 직접 준비한 manifest에도 `doc_type`, `scenario`, `condition`, `template_variant`, `source_dataset`을 명시하면 같은 경로로 전달합니다. 이름으로 추측하지는 않습니다.
- 생성 레시피·생성기 커밋·서식 해시는 기존 `dataset.json`의 기록과 함께 확인합니다.

## train 평가 보고서

기존 `python -m train` 또는 `python -m train.cli score` → `report` 흐름을 그대로 사용합니다.

학습 없이 `python -m docgen.bench eval`로 평가할 때도 `report.md`에 구분별 표와 `report.breakdowns.json`이 생성됩니다.

| 결과 | 내용 |
|---|---|
| 각 단계의 점수 JSON | 전체 과제 점수 + `composition` + `breakdowns` |
| `benchmark.md`, `benchmark.html` | 기존 전체 비교 + 시나리오·정답 구조·서식·원본 데이터셋별 점수와 기준 대비 변화 |
| `benchmark.breakdowns.csv` | 모델·구분·그룹·과제·지표·문항 수·값·변화량·예측 없음·구성 해시를 한 행씩 제공 |
| `benchmark.breakdowns.json` | 모델별 구성과 구분별 전체 지표 |

위 파일명은 `--out benchmark.csv` 기준입니다. 다른 출력 이름을 쓰면 같은 접두사를 사용합니다. CSV의 `value`는 원 지표이고 `delta_pp`는 기준 대비 %p입니다. CER·오탐률은 낮을수록 좋습니다.

CSV의 `unit: items`는 문항 수, `unit: fields`는 필드 항목 수입니다. `dimension: field_kind` 행은 KIE·marks의 값 정확도이며, 해당 점수는 JSON의 `models[].field_type_scores`에도 저장합니다. 업무·과제 그룹별 평가도 같은 CSV·JSON에 포함됩니다.

## 원격 생성 후 확인

저장소 루트에서 현재 Studio 주소를 지정한 뒤 조회합니다. 생성한 데이터셋 ID는 보통 생성 명령의 `--name`과 같습니다.

```powershell
$env:STUDIO_URL = "http://<서버IP>:8765"
python docker/remote_build.py composition my-benchmark
python docker/remote_build.py composition my-benchmark --out my-benchmark-composition.json
```

결과의 `all`은 전체 문항, `evaluation`은 평가 문항, `provenance`는 레시피·생성기 버전·서식 해시입니다. `--out`은 지정 파일을 덮어쓰므로 보관할 스냅샷은 새 파일명을 사용하세요. OCR 데이터셋의 재현 정보는 준비 폴더 상위의 `ocr_set.json`에서도 읽습니다.

서로 다른 벤치마크 문항 집합으로 만든 보고서는 기존처럼 직접 비교하지 않습니다. 같은 구분의 문항 ID 집합 해시도 확인합니다. **과제 사이의 점수를 합쳐 하나의 평균으로 만들지 않습니다.** 구분별 OCR CER은 그 구분의 전체 글자 수로 다시 계산하며, 문항별 CER을 단순 평균하지 않습니다.

## 누락 정보와 수량 단위

- `not_applicable`: 업무 시나리오가 없는 단일 문서·OCR 문항입니다.
- `unknown`: 기존 업무 문항의 시나리오, 서식, 출처 등이 기록되지 않았습니다. 자동으로 복원했다고 가정하지 않습니다.
- 구성표·구분별 평가의 `n`: **문항 수**입니다. 고객 수·문서 수·쪽 수와 다릅니다.
- `field_kind_counts`: 문항의 eval에 정의된 **필드 수**입니다. KIE·marks의 필드 타입별 값 정확도 표도 **항목 단위**이며 문항 단위 위치 F1과 구분합니다.
- 정답 구조만으로 새 과제가 만들어지지는 않습니다. 실제 생성 과제와 비율은 레시피와 구현된 시나리오 처리 설정을 따릅니다.

## 기존 데이터와 서버를 갱신할 때

- 새 데이터셋: 생성 시 구성 정보가 자동으로 기록됩니다.
- 기존 데이터셋: 재생성 없이도 기록된 메타데이터에서 조회합니다. 원본에 없는 정보는 `unknown`으로 남습니다. 이전 OCR 데이터에서 이미 버린 서식 정보는 자동 복원되지 않습니다.
- 기존 채점 결과: 다시 채점하거나 `train.cli score`와 `report`를 실행하면 구분별 보고서를 만듭니다. 과거 점수 파일만으로 없는 구분을 복원하지 않습니다.
- Studio 서버: 코드 갱신 후 재시작하고 브라우저를 새로고침합니다. 실행 중인 생성·채점 작업을 먼저 확인하세요. 새 API가 없는 서버에서도 기존 문항 화면은 열리며 새 기능은 재시작 안내를 표시합니다.
