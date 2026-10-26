# 평가 세트 구성과 구분별 점수

평가 세트는 과제 폴더 하나로 저장하고, 문항의 메타데이터로 업무·시나리오·정답 구조·서식별로 나눠 세고 채점합니다.

| 기준 | 예시 | 용도 |
|---|---|---|
| 과제 그룹 `task_group` | `ocr`, `doc`, `work` | OCR / 문서 이해 / 은행 업무 구분 |
| 과제 `task` | `crop_ocr`, `kie`, `doc_check`, `cross_check`, `review` | 같은 채점 방식끼리 비교 |
| 업무 시나리오 `scenario` | `mortgage`, `jeonse_loan` | 업무별 성능 |
| 정답 구조 `label_format` | `text`, `text_boxes`, `key_values`, `mark_states`, `document_sets`, `consistency_issues`, `scalar`, `text_list` | 텍스트·좌표·추출·표시·업무 판단 구분 |
| 서식 `doc_type` | `employment_certificate` | 어떤 서식에서 틀리는지 |
| 원본 데이터셋 `source_dataset` | `bench-a@<메타데이터 해시>` | 여러 폴더를 섞어도 출처 추적 |

정답 구조는 답의 꼴이고, 필드 타입(이름·금액·날짜·체크·서명 등)과는 별개입니다. 실제 답 규격은 [questions.md](questions.md)에 있습니다.

## studio에서 보기

1. **⑥ 데이터셋 → 데이터셋 → 구성·추적**: 전체 문항 / 평가 문항별로 업무·시나리오·과제·정답 구조별 수량. 수량을 누르면 그 문항이 열립니다.
2. **문항** 탭: 그룹·시나리오·정답 구조·서식으로 걸러 봅니다. 여러 과제를 함께 보려면 과제를 **과제 전체**로.
3. **모델 답**에서 모델 결과를 붙여 채점한 뒤, **구성·추적 → 구분별 평가 결과**에서 구분별 과제 지표를 봅니다.
4. 구분에서 **필드 타입 · 항목 단위**를 고르면 정보 추출·체크/도장/서명의 필드별 값 정확도가 나옵니다.

명령줄에서는 `python docker/remote_build.py composition <데이터셋 이름> [--out 파일.json]`. `all`은 전체 문항, `evaluation`은 평가 문항, `provenance`는 레시피·생성기 버전·서식 해시입니다.

## 학습 보고서에서 보기

`python -m train`의 보고서(`reports/benchmark.*`)에 구분별 점수가 같이 나옵니다.

| 결과 | 내용 |
|---|---|
| `benchmark.md`, `.html` | 전체 비교 + 시나리오·정답 구조·서식·원본 데이터셋별 점수와 기준 대비 변화 |
| `benchmark.breakdowns.csv` | 모델·구분·그룹·과제·지표·문항 수·값·변화량(`delta_pp`)을 한 행씩 |
| `benchmark.breakdowns.json` | 모델별 구성과 구분별 전체 지표, 필드 타입별 점수(`models[].field_type_scores`) |

- `n`은 **문항 수**입니다. 고객 수·문서 수·쪽 수와 다릅니다. CSV의 `unit: fields` 행(필드 타입별 값 정확도)은 **필드 항목 수**입니다.
- **과제끼리 점수를 합쳐 평균내지 않습니다.** 구분별 OCR CER은 그 구분의 전체 글자 수로 다시 계산합니다.
- `not_applicable`은 시나리오가 없는 단일 서류·OCR 문항, `unknown`은 기록되지 않은 정보입니다. 파일 이름으로 추측해 채우지 않습니다.
