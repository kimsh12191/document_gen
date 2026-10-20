# studio 데이터셋으로 학습하기

studio에서 만들거나 등록한 데이터셋을 1부(OCR)·2부(은행 업무) 학습에 넣고, 학습 결과를 다시 studio에서 보는 방법이다. 설계는 [DESIGN.md 9.9](DESIGN.md#99-학습으로-이어-쓰기).

- **학습 코드는 그대로다.** studio 데이터셋은 학습 파이프라인이 원래 읽는 폴더 형식이라, 설정 파일의 경로만 바꾸면 된다.
- 학습은 GPU 서버(내부망)에서 돌린다. **studio도 같은 서버에 띄워야** 화면에 보이는 경로가 학습 설정에 그대로 쓰인다.
- 처음부터 끝까지 명령줄로 하는 방법은 [guide/tutorial.md](../guide/tutorial.md)에 있다. 이 문서는 그중 "데이터를 어디서 가져오는지"만 studio로 바꾼다.

> 지금 상태 (2026-10-20): studio는 1단계(서식 보기)까지 구현됐다. 아래의 ⑥ 데이터셋·⑦ 평가 화면과 "학습 설정 내보내기"는 3~5단계에서 생긴다([DESIGN.md 11절](DESIGN.md#11-구현-단계)). 그 전까지는 tutorial의 명령줄 방법을 쓴다.

## 전체 그림

```
studio ⑥ 데이터셋                         training/ (GPU 서버)                      studio ⑦ 평가
───────────────────                       ─────────────────────                    ──────────────
OCR 데이터셋 (1부 prepare 결과) ───────▶  run_pipeline.py      → runs/exp1/  ───▶  답·점수 보기, 비교
은행 업무 학습·평가 데이터셋 ──────────▶  run_bank_pipeline.py → runs/bank1/ ───▶  답·점수 보기, 비교
        "학습 설정 내보내기"가 아래 경로 칸을 채워 준다          "학습 결과 붙이기"
```

## 1. 1부 OCR 학습

### 1-1. 데이터셋 고르기

⑥ 데이터셋에서 `track: ocr`인 데이터셋을 고른다. 학습에 쓰려면 train split이 있어야 한다(평가 전용 `benchmark_only`로 만든 것은 학습에 못 쓴다).

| 출처 | 정답 | 언제 쓰나 |
|---|---|---|
| 합성 | 생성 정답 (정확) | 실서류가 적은 서식을 보충할 때 |
| 이미지 묶음·결과 폴더 | 사내 OCR (의사정답) | 지금 1부와 같은 학습 |
| 이미지 묶음·결과 폴더 + OCR 검수 | 사람이 고친 OCR | 사내 OCR이 자주 틀리는 서식을 바로잡아 학습할 때 |

실서류와 합성을 함께 학습하려면, ⑥에서 두 데이터셋을 골라 **"합쳐서 새 데이터셋"**을 만든다. 내부적으로 1부 `bank_ocr merge`로 이미지 목록을 합친 뒤 `prepare`를 한 번 돌린다. 같은 이미지가 학습과 평가에 함께 들어가면 `prepare`가 멈춘다.

### 1-2. 설정에 넣기

1부 파이프라인은 `configs/pipeline.json`의 `data_config`가 가리키는 1부 설정(`config.json`)을 읽는다. 그 설정의 `output_dir`을 studio 데이터셋 폴더로 바꾼다.

```jsonc
// training/config.json (1부 데이터 설정) — 바꾸는 칸만
{
  "output_dir": "/share/studio_workspace/datasets/ocr-mix-v1"
}
```

폴더에 `DONE.json`이 있으면 파이프라인은 준비 단계를 건너뛰고 바로 학습한다(`run_pipeline.py`의 `stage_prepare`). "학습 설정 내보내기"를 쓰면 이 칸이 채워진 파일을 받는다.

### 1-3. 학습

```bash
cd training
python run_pipeline.py --config configs/pipeline.json --smoke   # 리허설
nohup python run_pipeline.py --config configs/pipeline.json > pipeline.log 2>&1 &
```

## 2. 2부 은행 업무 학습

### 2-1. 데이터셋 고르기

| 칸 | 고르는 데이터셋 |
|---|---|
| `data.train` | `track: bank`, train split 데이터셋 (`docgen.bench --split train` 폴더). 여러 개 넣을 수 있다 |
| `data.benchmark` | `track: bank`, **고정한** 평가 세트. 학습 데이터와 같은 생성기 버전이어야 한다 |
| `data.replay.path` | 1부 OCR 데이터셋의 `train_sft.jsonl` (OCR 능력 유지용) |
| `ocr_check.tasks` | 1부 OCR 데이터셋의 `benchmark_tasks.jsonl` (학습 뒤 OCR 점수가 떨어지지 않았는지) |

### 2-2. 설정에 넣기

```jsonc
// training/configs/bank_pipeline.json — 바꾸는 칸만
{
  "data": {
    "train": ["/share/studio_workspace/datasets/bank-train-1.3"],
    "benchmark": "/share/studio_workspace/datasets/bank-bench-1.3",
    "replay": {"path": "/share/studio_workspace/datasets/ocr-mix-v1/train_sft.jsonl", "count": 3000},
    "output_dir": "../data/prepared-bank-1.3"
  },
  "ocr_check": {"tasks": "/share/studio_workspace/datasets/ocr-mix-v1/benchmark_tasks.jsonl", "rows": 1000}
}
```

- `data.output_dir`은 2부 준비 결과가 생기는 곳이다. 데이터셋이 바뀌면 **새 이름**으로 한다(이미 있으면 파이프라인이 멈춘다).
- 생성기가 바뀌어 평가 세트 버전이 올라갔으면 학습 데이터와 평가 세트를 둘 다 새 버전으로 바꾼다([guide/tutorial.md 4-1](../guide/tutorial.md)).

### 2-3. 학습

```bash
cd training
python run_bank_pipeline.py --config configs/bank_pipeline.json --smoke
nohup python run_bank_pipeline.py --config configs/bank_pipeline.json > bank_pipeline.log 2>&1 &
```

## 3. 학습이 끝난 뒤

1. ⑥에서 평가 세트를 열고 **"학습 결과 붙이기"**에 결과 폴더(`runs/exp1/` 또는 `runs/bank1/`)를 준다.
2. ⑦ 평가에서 모델별 점수, 문항마다 정답과 답, 틀린 것부터 보기를 본다. 점수는 파이프라인의 `reports/*.json`과 같은 숫자다.
3. 내보낸 설정과 결과 폴더가 등록부의 학습 기록으로 이어진다. 데이터셋 설명서의 "이 데이터셋을 쓴 학습"에 그 학습이 생긴다.

## 확인 목록

- [ ] studio를 학습 서버에 띄웠다 (경로가 같다)
- [ ] 평가 세트는 고정했다
- [ ] 학습 데이터와 평가 세트의 생성기 버전이 같다
- [ ] 실서류 평가 세트에 쓴 결과 폴더가 1부 학습 데이터에 들어가 있지 않다 (studio가 검사하지 않는다. DESIGN.md 13절)
- [ ] 준비 결과 폴더(`output_dir`)는 새 이름이다
