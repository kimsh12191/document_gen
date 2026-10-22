# 학습 따라하기: studio 데이터 + 내 이미지

명령은 모두 학습 서버의 코드 폴더(`document_gen/`)에서 실행합니다.

## 1. studio 데이터 위치 찾기

```bash
find <studio 저장 폴더>/workspace/datasets -name meta.json
```

나온 경로에서 `/meta.json`을 뺀 것이 데이터셋 경로입니다. 학습용과 평가용을 메모해 둡니다.

## 2. 내 이미지로 OCR 데이터 만들기

```bash
export INTERNAL_OCR_BASE_URL=http://localhost:30107        # 사내 OCR 서버 주소
cp docgen/bench/ocr_config.example.json ocr_config.json
```

`ocr_config.json`에서 세 줄만 고칩니다.

```jsonc
"images": "/share/me/ocr_images",   // "manifest" 줄을 이걸로 바꿈
"output_dir": "data/ocr-v1",        // 결과 폴더 (새 이름)
"ocr_revision": "ocr-2026-10",      // 아무 이름
```

```bash
python -m docgen.bench.ocr_prepare ocr_config.json
```

`data/ocr-v1/DONE.json`이 생기면 끝입니다. 이미지의 10%는 자동으로 평가용이 됩니다.

## 3. 학습 설정

```bash
cp train/configs/pipeline.example.json train/configs/pipeline.json
```

`pipeline.json`에서 아래만 고칩니다. `"ocr_prepare"` 줄은 지웁니다.

```jsonc
"model": "/share/cv_share/qwen3.5/9b",
"gpus": [5, 6],
"data": {
  "train": [
    {"path": "<1의 studio 학습용 경로>"},
    {"path": "<코드 폴더>/data/ocr-v1", "count": 20000}
  ],
  "benchmark": [
    "<1의 studio 평가용 경로>",
    "<코드 폴더>/data/ocr-v1"
  ],
  "output_dir": "../data/mixed-exp1",
```

2의 폴더는 학습·평가 양쪽에 적습니다. 학습 쪽은 학습 문항만, 평가 쪽은 평가 문항만 가져가서 겹치지 않습니다.

## 4. 학습

```bash
python -m train --config train/configs/pipeline.json --smoke          # 리허설
nohup python -m train --config train/configs/pipeline.json > pipeline.log 2>&1 &
```

- 리허설이 끝나면 `train/runs/exp1/smoke/reports/benchmark.html`이 생깁니다.
- 결과 점수표는 `train/runs/exp1/reports/benchmark.html`에 생깁니다.
- 멈추면 같은 명령을 다시 실행합니다.

## 막히면

| 에러 | 할 일 |
|---|---|
| `Output already exists` | `output_dir`을 새 이름으로 |
| `설정(…)의 경로를 확인하세요` | 메시지에 나온 경로를 고침 (`meta.json`이 있는 폴더) |
| OCR `Error: 500` | 사내 OCR 서버와 `INTERNAL_OCR_BASE_URL` 확인 |
| `CUDA out of memory` | 40GB GPU면 `sft_a100_40g_x2.yaml`, `grpo_a100_40g_x2.yaml` 사용 |
