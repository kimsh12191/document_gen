# studio 데이터 + 내 이미지 OCR → 학습 (따라하기)

studio에서 만든 데이터셋과 내가 가진 이미지로 만든 OCR 데이터를 합쳐 한 번에 학습·평가하는 순서입니다. 아래 4단계를 차례로 하고, 단계마다 **확인**이 통과하면 다음으로 넘어가세요.

```text
① studio 데이터셋 경로 확인 ─┐
② 내 이미지 → OCR 준비 ───────┼─▶ ③ pipeline.json 에 경로 적기 ─▶ ④ python -m train
   (사내 OCR)                  ┘
```

모든 명령은 학습 서버의 저장소 최상위(`<코드>`)에서 실행합니다. 처음 설치(코드 받기, 학습 환경 확인)가 안 됐다면 [tutorial.md 1절](tutorial.md#1-준비-한-번)부터 하세요.

| 표기 | 뜻 | 예 |
|---|---|---|
| `<코드>` | 이 저장소 폴더 | `/share/me/document_gen` |
| `<studio>` | studio 저장 폴더 (`sh docker/studio.sh --data <폴더>`로 정한 곳) | `/database/docgen_studio` |
| `<이미지>` | 내가 가진 이미지 폴더 | `/share/me/ocr_images` |

---

## ① studio 데이터셋 경로 확인

studio ⑥ 데이터셋에서 만든 데이터셋은 `<studio>/workspace/datasets/` 아래에 있습니다. 학습에 적을 경로는 **`meta.json`이 들어 있는 폴더**입니다.

```bash
find <studio>/workspace/datasets -maxdepth 3 -name meta.json
```

출력 예:
```text
/database/docgen_studio/workspace/datasets/bank-train/meta.json          ← 학습용 (split train 으로 만든 것)
/database/docgen_studio/workspace/datasets/bank-bench/meta.json          ← 평가용
/database/docgen_studio/workspace/datasets/ocr-synth/prepared/meta.json  ← OCR 데이터셋은 prepared/ 아래
```

`/meta.json`을 뺀 앞부분이 경로입니다. 어느 것을 학습에 넣고 어느 것을 평가에 넣을지 적어 두세요.

- 학습용은 studio에서 **split train**으로 만든 데이터셋, 평가용은 평가 세트로 만든 데이터셋입니다. 같은 데이터셋을 양쪽에 넣으면 안 됩니다 (OCR 준비 결과는 예외, ③ 참고).
- 학습 서버에서 이 경로가 보여야 합니다. studio 컨테이너와 학습 서버가 같은 폴더를 공유하는지 `ls`로 확인하세요.

**확인:** 위 `find`에 쓸 데이터셋이 모두 나온다.

## ② 내 이미지 → OCR 학습·평가 데이터

### 2-1. 사내 OCR 서버 켜기

OCR 결과는 사내 OCR이 읽은 값을 정답으로 씁니다. 서버를 띄우는 법은 [tutorial.md 2-2](tutorial.md#2-2-사내-ocr-서버-띄우기)를 따르세요.

```bash
export INTERNAL_OCR_BASE_URL=http://localhost:30107     # 띄운 서버의 포트
```

### 2-2. 설정 파일 만들기

```bash
cp docgen/bench/ocr_config.example.json ocr_config.json
```

`ocr_config.json`에서 **세 군데만** 고칩니다. 나머지는 그대로 둡니다.

```jsonc
"images": "<이미지>",              // "manifest" 줄을 지우고 이 줄로 바꿈. 하위 폴더까지 읽음
"output_dir": "data/ocr-mine-v1",  // 결과 폴더. 이미 있는 이름은 안 됨
"ocr_revision": "ocr-2026-10",     // 아무 이름. 사내 OCR이 바뀌면 바꿈
```

- 그림 한 장을 문서 한 건으로 봅니다. 문서 ID 같은 건 적지 않아도 됩니다.
- 이미지의 10%는 자동으로 평가용, 5%는 검증용으로 떨어지고 나머지가 학습용입니다.
- 결과 폴더(`output_dir`, `cache_dir`)는 이미지 폴더 **밖**에 둡니다.
- 쪽이 여러 장인 문서를 한 문서로 묶어야 하면 [ocr_prepare.md 3-1](ocr_prepare.md#3-1-manifest-이미지-목록)을 보세요.

### 2-3. 실행

```bash
python -m docgen.bench.ocr_prepare ocr_config.json
```

**확인:** `cat data/ocr-mine-v1/DONE.json`이 나오고, 그 안의 `page_counts`에 `train`·`val`·`benchmark`가 모두 있다.

이 폴더도 studio 데이터셋과 같은 형식입니다. studio ⑥에 등록하면 문항·그림을 화면에서 볼 수 있습니다(선택).

## ③ pipeline.json 에 경로 적기

```bash
cp train/configs/pipeline.example.json train/configs/pipeline.json
```

`train/configs/pipeline.json`에서 아래를 고칩니다. **경로는 절대 경로**로 적는 게 안전합니다.

```jsonc
{
  "workdir": "../runs/exp1",                 // 결과 폴더. 새 실험이면 새 이름
  // "ocr_prepare" 줄은 지웁니다 (② 에서 이미 준비했으므로)
  "model": "/share/cv_share/qwen3.5/9b",     // 출발 모델
  "gpus": [5, 6],                            // OCR 서버와 겹치지 않는 GPU
  "data": {
    "train": [
      {"path": "<studio>/workspace/datasets/bank-train"},                     // ① studio 학습용
      {"path": "<코드>/data/ocr-mine-v1", "count": 20000}                     // ② 내 OCR (쓸 문항 수)
    ],
    "benchmark": [
      "<studio>/workspace/datasets/bank-bench",                               // ① studio 평가용
      "<코드>/data/ocr-mine-v1"                                               // ② 내 OCR (떼어 둔 10%만 평가에 씀)
    ],
    "output_dir": "../data/mixed-exp1",      // 섞은 결과. 데이터 구성이 바뀌면 새 이름
    …나머지는 그대로
  },
  …나머지는 그대로
}
```

- **② 폴더는 학습·평가 양쪽에 적습니다.** 학습 쪽에서는 train·val 문항만, 평가 쪽에서는 benchmark 문항만 가져가서 겹치지 않습니다.
- studio 데이터셋을 더 넣으려면 `train`이나 `benchmark` 목록에 줄을 추가하면 됩니다. OCR 데이터셋은 `prepared` 폴더까지 적습니다.
- 40GB GPU면 `sft.config`를 `sft_a100_40g_x2.yaml`로, `grpo.config`를 `grpo_a100_40g_x2.yaml`로 바꿉니다.

**확인:** `data`에 적은 폴더마다 `meta.json`이 있어야 합니다.
```bash
ls <studio>/workspace/datasets/bank-train/meta.json <studio>/workspace/datasets/bank-bench/meta.json <코드>/data/ocr-mine-v1/meta.json
```
경로가 틀린 채로 ④를 시작해도 학습 전에 어느 칸이 틀렸는지 한꺼번에 알려 주고 멈춥니다.

## ④ 학습

```bash
# 리허설: 5 step 학습 + 작은 평가 (몇십 분)
python -m train --config train/configs/pipeline.json --smoke

# 본 실행: 백그라운드 (A100 2장 기준 1~2일)
nohup python -m train --config train/configs/pipeline.json > pipeline.log 2>&1 &
tail -f pipeline.log
```

**확인:**
- 리허설이 끝나면 `train/runs/exp1/smoke/reports/benchmark.html`이 생긴다.
- 본 실행 진행은 `cat train/runs/exp1/state.json`의 `done`.
- 중간에 멈추면 **같은 명령을 다시** 실행합니다. 끝난 단계는 건너뜁니다.

결과:

| 무엇 | 위치 |
|---|---|
| 점수표 (studio 과제 + OCR 8과제가 한 표) | `train/runs/exp1/reports/benchmark.html` · 읽는 법 [results.md](results.md) |
| 학습한 모델 | `train/runs/exp1/merged/grpo-…-checkpoint-…` |
| 문항별 답 보기 | studio ⑥ 데이터셋 › 모델 답 탭에 `train/runs/exp1/` 붙이기 |

---

## 다시 돌릴 때

| 하고 싶은 것 | 할 일 |
|---|---|
| 이미지를 더 넣음 | ②의 `output_dir`을 새 이름으로 다시 준비 (이미 OCR한 그림은 캐시에서 다시 씀) → ③의 경로와 `data.output_dir`을 새 이름으로 |
| studio 데이터셋을 바꿈 | ③의 경로 수정 + `data.output_dir` 새 이름 |
| 새 실험 | `workdir` 새 이름 |
| 사내 OCR이 바뀜 | ②의 `ocr_revision`과 `output_dir`을 바꿔 다시 준비 |

## 자주 나는 에러

| 에러 | 원인 | 해결 |
|---|---|---|
| `Output already exists` | ②의 결과 폴더가 이미 있음 | `output_dir`을 새 이름으로 |
| `Manifest must include train and benchmark documents` | 이미지가 너무 적음 (2장 미만) | 이미지를 늘림 |
| OCR `Error: 500`, 연결 실패 | 사내 OCR 서버가 꺼졌거나 포트가 다름 | 서버와 `INTERNAL_OCR_BASE_URL` 확인 |
| `설정(…)의 경로를 확인하세요` | ③의 경로가 학습 서버에 없거나, `meta.json`이 없는 폴더를 적음 | 메시지에 나온 칸을 ①의 `find`로 나온 폴더(OCR 데이터셋은 `prepared`)의 절대 경로로 |
| `training rows share a customer or document with the benchmark` | 같은 데이터셋을 학습·평가에 함께 넣음 | studio 평가용 데이터셋을 `train`에서 뺌 |
| `CUDA out of memory` | 40GB GPU에 80GB 설정 | ③의 40GB yaml로 |

더 자세한 설명: OCR 준비 [ocr_prepare.md](ocr_prepare.md) · 학습 설정 [train/README.md](../train/README.md) · studio에서 설정 내보내기 [studio/TRAINING.md](../studio/TRAINING.md) · 전체 설치 [tutorial.md](tutorial.md)
