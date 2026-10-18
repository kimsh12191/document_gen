# 연구: 서류 묶음 속 여러 쪽 문서 추출

> **문제:** 임의의 서류 묶음에서 여러 쪽짜리 문서(등기부등본, 주민등록등본, 거래내역서, 인보이스, 패킹리스트, 재무제표)의 내용을 빠짐없이 추출해야 한다. 지금처럼 모든 쪽을 한 질문에 넣으면 쪽마다 1/4 크기로 줄어 작은 글씨를 잃고, 답이 수천~1만 토큰으로 길어져 행을 빠뜨린다.
>
> **가설:** 쪽을 원래 해상도로 한 장씩 읽고, 앞 쪽에서 얻은 것(서류 종류, 지금까지의 행 수와 마지막 행, 계좌·물건 같은 문서 정보)을 짧은 상태로 넘겨주도록 학습하면, 모든 쪽을 한 번에 넣는 방식보다 행을 덜 빠뜨리고 쪽 경계에서도 맞게 이어 붙인다.

브랜치 `claude/multipage-bundle-extraction`

## 비교하는 방법

| 방법 | 입력 | 상태 | 관련 연구 |
|---|---|---|---|
| 한 번에 넣기 (`allatonce`) | 묶음 전체, 이미지 합 12,000토큰 (쪽마다 같은 비율로 축소) | — | 지금 2부 방식, ExtractBench의 VLM 한 번 넣기 |
| 쪽 단위, 상태 없음 (`pagewise --state none`) | 한 쪽, 원래 해상도 | 없음. 모델이 "앞 쪽에서 이어짐"만 판단해 이어 붙임 | POTATR, PubTables-v2의 쪽 단위 + 병합 |
| 쪽 단위 + 상태 (`--state doc / tail / context`) | 한 쪽, 원래 해상도 | `doc` 서류 종류·읽은 쪽 수 → `tail` + 목록별 행 수와 마지막 행 → `context` + 계좌·물건·송장번호 같은 문서 정보 | 학습 없이 프롬프트로만 주면 2511.10659(재정 문서)와 같음. **학습한 상태**가 이 연구 |

학습 전 출발 모델(2부 은행 업무 모델)로 모든 방법을 한 번 재고(`zeroshot`), 같은 학습 묶음으로 쪽 단위+상태 모델과 한 번에 넣기 모델을 각각 학습해 다시 잽니다.

## 데이터

- **생성 묶음** (`python -m mpx gen`): 고객 한 명의 대상 서류 2~4건(여러 쪽) + 한 쪽짜리 다른 서류 1~3건(신분증, 재직증명서 등)을 섞은 묶음. 정답은 docgen이 렌더링한 그대로라 모든 행·칸·쪽이 정확합니다.
  - `--heavy` (기본 0.7): 목록이 긴 경우(거래 30~90줄, 품목 20~60개, 등기 사항 다수)로 만들 확률
  - `--no-repeat-header` (기본 0.3): 이어지는 쪽에 표 머리글을 다시 찍지 않을 확률. 앞 쪽을 봐야 무슨 표인지 아는 쪽이 생깁니다.
  - `--augment` (기본 0.3): 스캔·촬영·팩스 증강
  - 학습 고객(seed 500,000~)과 평가 고객(1,500,000~)은 겹치지 않습니다.
- **학습 데이터** (`python -m mpx sft`): `swift_page/`는 쪽마다 문항 하나, 상태 종류를 고루 섞고 20%는 상태를 일부러 틀리게(행 수 ±1, 마지막 행 지움, 목록 정보 빠뜨림) 해서 앞 쪽 실수에서 회복하도록. `swift_all/`은 같은 묶음의 한 번에 넣기 문항. 둘 다 `training/train.py`가 그대로 읽습니다.
- **실제 서류** (`python -m mpx check`): 정답이 없으므로 예측 값이 그 쪽의 사내 OCR 글자에 있는 비율, 거래내역 잔액 흐름, 인보이스 품목 합계로 봅니다. `bundles.jsonl`에 `pages: [{image, ocr}]`만 있으면 됩니다.

생성 데이터 실측(묶음 12개): 묶음당 5~11쪽, 거래내역 최대 71행, 재무제표 최대 95행. 답 길이는 쪽 단위 중앙값 약 1,000토큰(최대 2,600), 한 번에 넣기 중앙값 약 8,600토큰(최대 13,500).

## 지표 (`python -m mpx score`)

| 지표 | 뜻 |
|---|---|
| 문서 나누기 정확, 쪽 배정 | 묶음에서 문서별 쪽을 정확히 묶었는지 |
| 항목 F1 | 행이 아닌 항목(계좌번호, 송장번호 등) |
| 행 F1 · 재현율 · 빠진 행 | 순서를 지키며 정답 행과 맞춤(칸 절반 이상 같아야 짝). 모든 칸이 맞아야 맞은 행 |
| 칸 재현율 | 행 안의 칸 단위 |
| **경계 행** | 목록이 쪽을 넘어갈 때 앞 쪽 마지막 행과 다음 쪽 첫 행 |
| **이어지는 행** | 목록이 시작된 쪽 다음 쪽부터 나오는 행 (앞 쪽 정보가 필요한 행) |
| 잔액 흐름, 품목 합계 | 예측만으로 하는 검사: 앞 잔액 − 출금 + 입금 = 잔액, 품목 금액 합 = 합계 |
| 비용 | 묶음당 요청 수, 이미지 토큰, 가장 긴 입력, 출력 토큰, 시간 |

서류별, 서류 쪽 수별, 머리글 반복 여부별로도 나눠 봅니다.

## 실행

이 저장소에서(Chromium 필요, 이 폴더에서):

```bash
python -m mpx gen   --out data/test --n 20 --split test --workers 4
python -m mpx run   --data data/test --method pagewise --state context --oracle --out preds/oracle.jsonl   # 파이프라인 확인 (100%)
python -m mpx score --data data/test --pred preds/oracle.jsonl --out reports/oracle
```

내부망 GPU 서버에서 한 바퀴 (생성 → 학습 데이터 → 출발 모델 평가 → 학습 2종 → 병합 → 평가 → 채점):

```bash
START_MODEL=/path/to/bank_sft_merged GPUS=0,1 ./run_experiment.sh
START_MODEL=... N_TRAIN=20 N_TEST=10 MAX_STEPS=5 ./run_experiment.sh      # 리허설
```

모델 서버를 따로 띄워 둔 경우:

```bash
python -m mpx run --data data/test --method allatonce --budget 12000 --base-url http://127.0.0.1:8000/v1 --model bank-ocr --out preds/all.jsonl
python -m mpx run --data data/test --method pagewise --state tail    --base-url http://127.0.0.1:8000/v1 --model bank-ocr --out preds/pw_tail.jsonl
python -m mpx score --data data/test --pred preds/*.jsonl --out reports/compare
```

## 판정

- 쪽 단위 + 상태(학습)가 한 번에 넣기(학습)보다 **행 F1과 이어지는 행**에서 높고, 빠진 행이 적다.
- 상태 종류 비교(`none < doc < tail < context`)로 무엇이 필요한지 밝힌다. 머리글 반복 없는 쪽에서 차이가 커야 한다.
- 상태를 일부러 틀리게 한 학습이 틀린 상태에서 회복하는지(평가 때 상태 손상 실험).
- 비용: 쪽 단위는 요청 수가 쪽 수만큼 늘지만 한 요청의 입력·출력이 짧다. 묶음당 시간과 GPU 메모리 상한을 같이 보고한다.

## 폴더

```
mpx/gen.py      묶음 생성 (docgen 렌더링, 병렬)
mpx/pages.py    쪽 나누기, 쪽 정답, 상태, 질문 문장, 쪽 답 병합
mpx/run.py      실행 (OpenAI 호환 서버, --oracle)
mpx/sft.py      학습 데이터 (swift_page, swift_all)
mpx/score.py    채점, 정답 없는 실제 서류 검사
configs/        page_sft.yaml, all_sft.yaml (training/train.py 용)
run_experiment.sh  내부망 한 바퀴
```

테스트: 저장소 루트에서 `python -m pytest tests/test_mpx.py`.
