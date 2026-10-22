# 실서류 OCR 준비 → 학습·평가

가진 서류 이미지를 사내 OCR에 돌려 OCR 과제(글자·위치 읽기 8종)의 학습·평가 데이터로 만들고, `python -m train` 한 번에 학습까지 이어 가는 방법입니다. 예전 1부 OCR 파이프라인(`bank_ocr prepare`)과 같은 일을 학습의 첫 단계 `ocr_prepare`가 합니다.

서식별·시나리오별로 결과를 추적하려면 manifest에 `doc_type`·`scenario`를 명시하세요. 선택 항목인 `condition`·`template_variant`·`source_dataset`도 OCR 준비와 과제 폴더까지 보존합니다. 합성 OCR 생성기는 이 정보를 자동으로 기록합니다. 분류를 알 수 없는 실서류는 생략해도 되며 `unknown`으로 표시합니다. [구성·평가 추적](benchmark-tracking.md)을 참고하세요.

- **선택 단계입니다.** OCR 데이터는 합성(`python -m docgen.ocr_set build`, studio 합성 OCR 레시피)이나 studio에서 가져온 이미지(④ "OCR 벤치마크로")로도 만들 수 있습니다. 그런 데이터셋만 쓰면 `ocr_prepare`를 적지 않고 결과 폴더 경로만 `data`에 적습니다.
- 처음부터 따라 하는 순서는 [tutorial.md 2절·4절](tutorial.md#2-ocr-데이터-실서류), 과제 예시는 [tasks.md](tasks.md#ocr-과제)에 있습니다.

## 1. 한눈에

```text
 이미지 폴더 ──scan──▶ manifest.jsonl ─┐
 (쪽 PNG/JPG)          (문서 ID·쪽·split) │
                                      ├─▶ ocr_config.json ──┐
 사내 OCR 서버 또는 저장된 OCR JSON ─────┘   (OCR 준비 설정)     │
                                                           ▼
 pipeline.json ── "ocr_prepare": ["../../ocr_config.json", …]
      │
      │  python -m train --config train/configs/pipeline.json
      ▼
 ① ocr_prepare  이미지 → 사내 OCR(캐시) → OCR 8과제 문항 → <output_dir>/ (DONE.json, meta.json, tasks/)
 ② prepare      data.train · data.benchmark 에 적은 폴더들을 섞음  ← 위 output_dir 경로를 여기 적어 둔다
 ③ eval_base → sft → eval_sft → select → grpo → eval_grpo → report
```

`ocr_prepare`는 결과 폴더에 `DONE.json`이 있으면 건너뜁니다. 그래서 같은 설정으로 다시 돌리거나 `--from sft`로 이어 돌려도 OCR을 다시 하지 않습니다.

## 2. 준비물

| 무엇 | 설명 |
|---|---|
| 쪽 이미지 | PNG·JPG·TIF 등 쪽마다 한 장. PDF·여러 쪽 TIFF는 쪽별 이미지로 먼저 바꿉니다 |
| 문서 ID 규칙 | 같은 문서의 쪽을 묶는 규칙(파일 이름 또는 폴더). 학습·평가를 **문서 단위**로 나누기 때문에 꼭 필요합니다 |
| 사내 OCR | OCR 서버([tutorial 2-2](tutorial.md#2-2-사내-ocr-서버-띄우기), 주소는 `INTERNAL_OCR_BASE_URL`) **또는** 이미 돌려 둔 OCR JSON 폴더 |

## 3. 만드는 순서

### 3-1. manifest (이미지 목록)

**그림 한 장이 문서 한 건이면 manifest는 만들지 않아도 됩니다.** 3-2의 설정에서 `"manifest"` 줄 대신 `"images": "/share/data/images"`(이미지 폴더, 하위 폴더까지 읽음)를 적으면 OCR 준비가 목록을 직접 만듭니다. `"split"`을 생략하면 `train`(일부를 평가·검증으로 떼어 냄), `"split": "benchmark"`면 전부 평가용입니다. 결과 폴더(`cache_dir`·`output_dir`)는 이미지 폴더 밖에 두세요.

여러 쪽 문서를 문서 단위로 묶어야 할 때만 아래처럼 manifest를 만듭니다.

```bash
cd <코드>
python -c "from docgen.bench.ocr_data import scan, write_jsonl; write_jsonl('data/manifest.jsonl', scan(
  '/share/data/images', 'train', r'(?P<document_id>[^/]+)_p[0-9]+\.[^.]+$'))"
```

| `scan` 인자 | 뜻 |
|---|---|
| 첫째 | 이미지 폴더 (하위 폴더까지 읽음) |
| 둘째 `split` | `train`: 학습용(문서 일부를 평가·검증으로 떼어 냄) · `benchmark`: 전부 평가용 |
| 셋째 `document_regex` | 상대 경로에서 문서 ID를 뽑는 정규식. 파일 이름 `doc123_p001.png` → `(?P<document_id>[^/]+)_p[0-9]+\.[^.]+$`, 문서마다 폴더 → `^(?P<document_id>[^/]+)/`. 그림 하나가 문서 하나면 정규식 대신 `single_page=True` |
| `ocr_dir=` (선택) | 이미 돌린 OCR JSON 폴더 (이미지와 같은 상대 경로·이름, 확장자만 `.json`). 이 그림들은 OCR 서버를 부르지 않습니다 |

한 줄이 한 쪽입니다: `{"document_id", "page_id", "image", "split", "ocr_json"?}`.

### 3-2. OCR 준비 설정

```bash
cp docgen/bench/ocr_config.example.json ocr_config.json
```

꼭 볼 칸 (상대 경로는 이 설정 파일이 있는 폴더 기준):

| 칸 | 값 | 설명 |
|---|---|---|
| `manifest` | `data/manifest.jsonl` | 3-1에서 만든 파일 |
| `output_dir` | `data/prepared-v2` | 결과 폴더. **이미 있으면 새 이름** (덮어쓰지 않음) |
| `cache_dir` | `data/ocr-cache` | 정규화한 그림과 OCR 응답 캐시. 여러 준비가 같이 써도 됩니다 |
| `ocr_callable` | `studio.internal_ocr_adapter:ocr_from_file` | 사내 OCR을 부르는 함수 |
| `ocr_revision` | 예: `ocr-api-2026-10` | 캐시 열쇠. **OCR 모델·설정이 바뀌면 이 값도 바꿉니다** (같은 값이면 예전 결과를 다시 씀) |
| `benchmark_fraction` | `0.1` | 학습용 manifest에서 평가로 떼어 둘 문서 비율 |
| `val_fraction` | `0.05` | 검증으로 떼어 둘 문서 비율 |
| `benchmark_only` | `true` (평가 전용일 때만) | manifest 전체를 평가용으로. 이때 manifest의 split이 모두 `benchmark`여야 합니다 |

그 밖의 칸(`views` 깨끗한·변형 보기 수, `tasks_per_view` 과제별 문항 수, `filters` 신뢰도·길이 거르기, `augment`)은 예시 값을 그대로 써도 됩니다. `sft_max_examples`·`task_mix`는 이 폴더 혼자 쓸 때의 값이라 `python -m train`은 쓰지 않습니다. 학습에 쓸 OCR 양은 `pipeline.json`의 `count`로 정합니다.

### 3-3. pipeline.json에 연결

두 군데에 적습니다. `ocr_prepare`는 "무엇을 준비할지", `data`는 "준비된 폴더를 어디에 쓸지"입니다. 상대 경로는 `pipeline.json`이 있는 폴더(`<코드>/train/configs`) 기준입니다.

```jsonc
{
  "ocr_prepare": "../../ocr_config.json",                         // 하나면 문자열, 여럿이면 목록
  "data": {
    "train":     [{"path": "<데이터>/bank_train"},
                  {"path": "../../data/prepared-v2", "count": 20000}],   // 학습: train·val 문서의 문항, SFT 20000개까지
    "benchmark": ["<데이터>/bench", "../../data/prepared-v2"],          // 평가: 떼어 둔 문서의 문항
    "output_dir": "../data/mixed-exp1"
  }
}
```

`python -m train`은 실행하자마자 `ocr_prepare` 설정 파일과 그 안의 manifest가 있는지 확인합니다. 아직 만들어지지 않은 OCR 결과 폴더는 `ocr_prepare` 단계가 만들 것이므로 묻지 않습니다.

## 4. 쓰는 방법 세 가지

| | 하고 싶은 것 | `ocr_prepare` | `data.train` | `data.benchmark` |
|---|---|---|---|---|
| **A** | 이미지 한 묶음으로 학습도 하고 평가도 (기본) | 설정 1개 (`benchmark_fraction` 0.1) | 그 폴더 + `count` | 같은 폴더 |
| **B** | 학습용 이미지와 평가용 이미지가 따로 | 설정 2개: 학습용 + 평가 전용(`benchmark_only`) | 학습용 폴더 | 평가 전용 폴더 (원하면 학습용 폴더도) |
| **C** | 평가만 (출발 모델·다른 모델 비교) | 평가 전용 설정 1개 | — | 평가 전용 폴더 |

B의 예:

```jsonc
"ocr_prepare": ["../../ocr_train.json", "../../ocr_eval.json"],   // 차례로 준비 (로그 ocr_prepare.log, ocr_prepare1.log)
"data": {
  "train":     [{"path": "../../data/ocr-train", "count": 20000}],
  "benchmark": ["../../data/ocr-eval"]                              // ocr_eval.json: "benchmark_only": true, manifest split 모두 benchmark
}
```

평가 전용 manifest는 `scan(…, 'benchmark', …)`로 만듭니다. 평가 세트는 **고정**해 두어야 실험끼리 점수를 비교할 수 있으니, 한 번 만든 평가 폴더는 그대로 두고 새 학습 이미지만 새 `output_dir`로 준비합니다.

## 5. 학습·평가는 어떻게 나뉘나

- **문서 단위.** OCR 준비가 문서마다 split(train·val·benchmark)을 정하고, 모든 문항의 `meta.split`에 적습니다. 같은 문서의 쪽은 한쪽에만 들어갑니다. 픽셀이 같은 그림이 서로 다른 split에 있으면 준비가 멈춥니다.
- **같은 폴더를 두 목록에.** 섞기(`prepare`)는 `data.train`에 적은 폴더에서는 train·val 문항만, `data.benchmark`에 적은 폴더에서는 그 밖(benchmark)의 문항만 가져갑니다. 그래서 A처럼 한 폴더를 두 곳에 적어도 겹치지 않습니다.
- **겹침 검사.** 평가에 쓰는 문서와 같은 문서 ID가 학습 쪽에 있으면 섞기가 멈춥니다(`training rows share a customer or document with the benchmark`). B에서 두 manifest의 문서 ID가 겹치지 않게 하세요.
- **GRPO 후보.** 학습 문서의 일부(`grpo_holdout`, 기본 20%)는 SFT에 넣지 않고 GRPO 후보로 남깁니다. OCR의 GRPO 과제는 `grounding`·`spotting`·`relation`입니다(`grpo.tasks`).
- **점수표.** 평가 결과는 `reports/benchmark.html`의 OCR 열(과제 8종)에 업무·문서 과제와 한 표로 나옵니다. 읽는 법은 [results.md](results.md)입니다.

## 6. 결과 폴더 (`output_dir`)

| 파일 | 내용 |
|---|---|
| `DONE.json` | 끝났다는 표시(마지막에 씀): 쪽 수(split별), 문항 수, OCR 버전, 거른 영역 수 |
| `meta.json`, `tasks/<과제>.jsonl` | 과제 형식 문항(`docgen-tasks/1`). 섞기·studio·채점이 읽는 것 |
| `pages.jsonl` | 쪽마다 원본 경로, split, OCR 결과 |
| `views/`, `crops/`, `tiles/`, `marked/` | 모델이 보는 그림(깨끗한·변형 보기, 잘라낸 칸, 표시한 그림) |
| `config.snapshot.json` | 이 준비에 쓴 설정 |
| `train_sft.jsonl` 등 | 이 폴더 혼자 쓸 때의 학습 파일 (`python -m train`은 `tasks/`를 씀) |

studio ⑥ 데이터셋에 이 폴더를 등록하면 문항·그림·박스를 화면에서 볼 수 있습니다.

## 7. 확인과 다시 돌리기

**확인**
```bash
wc -l data/manifest.jsonl                         # 쪽 수와 같은지
head -2 data/manifest.jsonl                       # document_id 가 문서별로 맞는지
python -m train --config train/configs/pipeline.json --dry-run   # ocr_prepare 명령이 보이는지
cat data/prepared-v2/DONE.json                    # 끝난 뒤: page_counts (train·val·benchmark 쪽 수)
cat data/prepared-v2/meta.json                    # split_counts (split별 문항 수)
```

| 하고 싶은 것 | 방법 |
|---|---|
| OCR 준비만 먼저 | `python -m train --config … --only ocr_prepare` 또는 `python -m docgen.bench.ocr_prepare ocr_config.json` |
| 이미지를 더 넣음 / 설정을 바꿈 | manifest를 다시 만들고 `output_dir`을 새 이름으로. 이미 OCR한 그림은 캐시에서 다시 씀. `data.output_dir`(섞은 결과)도 새 이름으로 |
| 사내 OCR이 바뀜 | `ocr_revision`을 바꾸고 `output_dir` 새 이름 (같은 그림도 다시 OCR) |
| OCR 데이터를 빼고 학습 | `ocr_prepare`와 `data`의 그 경로를 지움 |

| 에러 | 원인 | 해결 |
|---|---|---|
| `설정(…)의 경로를 확인하세요` … `ocr_prepare` | OCR 준비 설정이나 그 안의 manifest가 없음 | 메시지의 경로 확인 (상대 경로 기준: `pipeline.json`은 그 폴더, `ocr_config.json` 안은 그 파일 폴더) |
| `Output already exists` | 결과 폴더가 이미 있는데 `DONE.json`이 없음 (중간에 멈춘 준비) | `output_dir`을 새 이름으로. 캐시는 그대로 쓰므로 OCR은 다시 하지 않음 |
| `Regex must match a named document_id group` | `scan`의 정규식이 어떤 파일에 안 맞음 | 메시지의 경로를 보고 정규식 고침 |
| `Document leakage` / `Duplicate image leakage` | 한 문서가 두 split에, 또는 같은 그림이 두 split에 | manifest의 split·문서 ID 확인 |
| `Manifest must include train and benchmark documents` | 학습용인데 문서가 너무 적어 평가를 못 뗌 | 문서를 늘리거나 평가 전용(`benchmark_only`)으로 |
| `Error: 500`, 연결 실패 (`logs/ocr_prepare.log`) | 사내 OCR 서버가 꺼졌거나 주소가 다름 | 서버와 `INTERNAL_OCR_BASE_URL` 확인 |
| `has an EXIF rotation; saved OCR coordinates are ambiguous` | 회전 정보가 있는 그림에 미리 만든 OCR JSON | 그 그림은 `ocr_dir` 없이 OCR 서버로 |
