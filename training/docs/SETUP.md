# 설치와 준비

처음 서버에 반입했을 때 한 번 하는 일입니다: 설치, 내부 OCR 연결, 이미지 목록(manifest), 설정 파일. `run_pipeline.py`는 4번의 데이터 준비(prepare)를 직접 실행하므로 4번 명령은 따로 돌리지 않아도 됩니다.

## 1. 내부망 환경 준비 및 설치

압축을 내부망 Linux 서버에 풀고 프로젝트 디렉터리로 이동합니다. 데이터 준비에는 Python 3.10+와 Pillow만 필요하며, 학습 환경은 Python 3.12를 권합니다.

```bash
python -m pip install --no-index --find-links /share/wheelhouse --no-build-isolation -e .
```

`setuptools>=68`, Pillow 및 빌드 도구도 내부 wheelhouse/환경에 준비해야 합니다. 인터넷이 되는 곳에서 대상 Linux/CUDA와 같은 환경으로 wheel 또는 컨테이너를 준비하세요. Windows wheel을 Linux로 복사해서 사용하면 안 됩니다.

`requirements-train.in`은 공식 Qwen3.5 v4.0 문서 기준의 **후보 환경**이며 GPU에서 검증한 lockfile은 아닙니다. CUDA에 맞는 PyTorch, ms-swift 4.x, Transformers, PEFT, DeepSpeed를 준비하세요. Qwen3.5용 커널은 같은 PyTorch/CUDA 환경에서 준비해야 합니다. 런처는 실제 학습 시작 시 설치 버전을 `environment.freeze.txt`에 기록합니다.

모델 경로는 `/share/cv_share/qwen3.5/9b`이며, 이 폴더에 로컬 Qwen3.5-9B 전체 파일이 있어야 합니다. 9B는 멀티모달 모델이며 이름 뒤에 임의로 `-VL`을 붙이지 않습니다.

### 설정 파일과 옵션 변경

| 파일 | 적용 범위 |
|---|---|
| `config.json` | OCR 연결·데이터 준비·분리·필터. 학습 설정과 별개 |
| `configs/sft.yaml` | SFT 학습률·epoch·batch·LoRA·freeze·저장/검증 주기 등 |
| `configs/grpo.yaml` | GRPO 학습 및 rollout 생성 수·temperature·top-p·응답 길이·vLLM 등 |
| `configs/inference.json` | 평가용 HTTP 추론의 서버·모델·timeout·생성 설정 |

YAML을 읽는 런처에는 `PyYAML>=6,<7`이 필요합니다. 학습 의존성은 `requirements-train.in`에 포함되어 있으며 내부망 wheelhouse에서 준비합니다. OCR 준비와 JSON 추론 설정에는 PyYAML이 필요하지 않습니다.

```bash
python -m pip install --no-index --find-links /share/wheelhouse --no-build-isolation -r requirements-train.in
```

학습 YAML은 MS-SWIFT 4.x의 인자 이름을 그대로 사용합니다. 알려진 몇 개 옵션만 허용하는 방식이 아니라 추가 옵션도 SWIFT 명령으로 전달합니다. 지원 여부는 설치된 SWIFT 버전에서 검사합니다. bool·list·dict 값도 지원하며, dict는 JSON 인자로 변환합니다. 예를 들어 SFT 설정에서 다음 값을 변경할 수 있습니다.

```yaml
learning_rate: 2.0e-5
num_train_epochs: 3
per_device_train_batch_size: 1
gradient_accumulation_steps: 8
lora_rank: 32
lora_alpha: 64
freeze_vit: true
save_steps: 200
eval_steps: 200
gradient_checkpointing_kwargs:
  use_reentrant: false
```

`--config`를 생략하면 프로젝트의 `configs/sft.yaml` 또는 `configs/grpo.yaml`을 사용합니다. 다른 실험은 파일을 복사하여 `--config configs/sft-experiment.yaml`로 지정하세요. 사용자 설정 파일은 기본 파일을 대체하며 자동 병합하지 않습니다. 위 예시는 변경할 항목의 발췌입니다.

`--max-steps`와 `--deepspeed` CLI 값은 YAML의 해당 값을 덮어씁니다. DeepSpeed는 `zero2`, `zero3` 또는 사용자 JSON 파일 경로를 받을 수 있습니다. YAML에 있는 추가 파일 경로는 실행 디렉터리 기준으로 지정합니다.

모델·데이터·출력·adapter 경로는 기존 CLI(`--model`, `--data`, `--output`, `--adapter`, `--grpo-dataset`)로 지정합니다. YAML에 `model`, `dataset`, `val_dataset`, `output_dir`, `adapters`, `ref_adapters`, `config`, `ENV`를 넣으면 오류로 안내합니다. SFT validation은 준비된 `val_sft.jsonl`에서 연결하고, GRPO 데이터는 train 여부를 검사합니다. GRPO의 `remove_unused_columns`는 보상 필드를 보존하도록 false로 유지합니다. 기본 보상 플러그인은 자동 연결하며, 별도 플러그인을 지정하려면 `external_plugins`와 `reward_funcs`를 함께 맞춥니다.

실제 실행 시 `launch.json`에 선택 GPU·프로세스 수·명령을, `training.resolved.json`에 최종 학습 옵션을, `environment.freeze.txt`에 설치 버전을 기록합니다. `--execute`를 빼면 학습 없이 최종 명령을 확인합니다.

### 8장 중 사용할 GPU 4장 지정

본문은 0~3번 GPU를 사용합니다. 4~7번을 사용하려면 학습 명령의 `--gpus`를 바꿉니다.

```bash
python train.py sft --config configs/sft.yaml --gpus 4,5,6,7 \
  --model /share/cv_share/qwen3.5/9b --data data/prepared-v2 --output runs/sft --execute
```

선택 우선순위는 **`--gpus` → `CUDA_VISIBLE_DEVICES` 환경변수 → 기본 0,1,2,3**입니다. `NPROC_PER_NODE`는 선택한 GPU 수로 자동 설정합니다. 서버에 8장이 있어도 예제의 명시적인 `--gpus`로 선택한 4장만 학습에 사용합니다. 다른 작업과 동시에 학습할 때는 `MASTER_PORT`도 겹치지 않게 지정하세요.

이미지 토큰 예산은 **`--image-tokens` → `IMAGE_MAX_TOKEN_NUM` 환경변수 → 모델 설정과 `image_max_size`로 계산한 값** 순서입니다. 평가 서버에는 `python -m bank_ocr image-tokens`가 알려 주는 같은 값을 `IMAGE_MAX_TOKEN_NUM`으로 지정합니다. 평가 서버의 `CUDA_VISIBLE_DEVICES=0`도 원하는 GPU 번호로 바꿀 수 있습니다. 학습용 `NPROC_PER_NODE=4`를 export해 두었다면 평가 서버 실행 전 해제합니다.

**완료 기준:** 프로젝트 설치, 학습 의존성, 로컬 모델 파일이 준비되어 있습니다.

## 2. 내부 OCR 함수 연결

`internal_ocr_adapter.py`는 첨부 이미지의 코드를 그대로 사용합니다. `BASE_URL`은 환경변수 `INTERNAL_OCR_BASE_URL`에서 읽으며(기본값 `http://localhost:30107`) `OCR_URL`(`/ocr`)에 multipart `file` 필드로 이미지를 전송합니다. 실행 전에 내부 OCR 서버 주소를 설정합니다(예: `export INTERNAL_OCR_BASE_URL=http://<내부-OCR-호스트>:<포트>`).

**사내 OCR 서버 띄우기** (OCR JSON을 미리 만들어 두지 않았을 때만 필요합니다)

사내 OCR API 서버 폴더에서 GPU 번호와 포트를 정해 띄우고, 같은 포트를 `INTERNAL_OCR_BASE_URL`로 알려 줍니다. 학습·평가에 쓸 GPU와 겹치지 않는 GPU를 고릅니다.

```bash
# 터미널 1: 사내 OCR 서버 (켜 둔 채로)
cd <사내 OCR API 폴더>
GPU_ID=7 SERVER_PORT=30107 python server.py

# 터미널 2: 파이프라인 (prepare가 이 서버에 페이지를 보냄)
export INTERNAL_OCR_BASE_URL=http://localhost:30107
curl -s $INTERNAL_OCR_BASE_URL/health        # 서버가 health를 지원하면 응답이 옴
python run_pipeline.py --config configs/pipeline.json --smoke
```

- OCR 결과는 `cache_dir`에 이미지 픽셀·OCR 함수·`ocr_revision` 기준으로 저장됩니다. 다시 실행하면 서버를 다시 부르지 않으므로, prepare가 끝나면 OCR 서버를 꺼도 됩니다.
- OCR 서버 버전이나 설정을 바꿨다면 `config.json`의 `ocr_revision`도 바꿉니다. 그래야 예전 캐시를 쓰지 않습니다.

첨부 코드에서 import하는 requests와 matplotlib은 OCR 의존성에 포함되어 있습니다.

```bash
python -m pip install --no-index --find-links /share/wheelhouse --no-build-isolation -e '.[ocr]'
```

`config.json`의 `ocr_callable`은 `internal_ocr_adapter:ocr_from_file`로 유지합니다. HTTP 200이면 원본 JSON을 반환하고, 그 외에는 상태 코드와 응답 본문을 출력한 뒤 `None`을 반환합니다. timeout과 자동 재시도는 지정하지 않습니다.

`prepare`는 EXIF 방향을 보정한 PNG를 전달합니다. 어댑터는 이 파일을 그대로 전송하며, 반환값의 `success`·필드·좌표 검사는 기존 데이터 준비 코드가 수행합니다. 실패 응답은 성공 캐시에 저장되지 않습니다.

기본 JSON 매핑은 아래 실제 구조에 맞춰져 있습니다. `basicData`는 평평한 배열과 여러 겹 배열을 모두 지원합니다.

```json
{
  "filename": "page.png",
  "success": "Y",
  "data": {
    "basicData": [[{
      "text": "2024",
      "confidence": 0.9999,
      "bounding": {
        "shape": "rectangle",
        "vertices": [{"x":140,"y":46},{"x":224,"y":46},{"x":224,"y":76},{"x":140,"y":76}]
      },
      "line_num": 0
    }]]
  }
}
```

`success != "Y"`, 잘못된 좌표·신뢰도·필드가 있으면 중단합니다. 실패 응답은 성공 캐시에 저장하지 않습니다. 성공한 빈 페이지는 기록하지만 학습 예제는 만들지 않습니다. 임의의 재시도·누락 처리는 하지 않습니다.

**완료 기준:** OCR 의존성과 어댑터의 `BASE_URL` 설정이 준비되어 있습니다. 실제 호출과 매핑은 4단계에서 소량의 데이터로 확인합니다.

## 3. 입력 이미지와 문서 manifest 생성

사용자가 반입한 페이지 이미지를 그대로 입력합니다. PDF와 다중 페이지 TIFF는 먼저 페이지별 이미지로 렌더링해야 합니다. 자동 페이지 분할은 이 버전에 포함하지 않습니다.

예: `doc123_p001.png`, `doc123_p002.png`에서 `doc123`이 원본 문서 ID라면:

```bash
python -m bank_ocr scan --root /share/data/train --split train \
  --document-regex '(?P<document_id>[^/]+)_p[0-9]+\.[^.]+$' --out data/train-manifest.jsonl

python -m bank_ocr scan --root /share/data/benchmark --split benchmark \
  --document-regex '(?P<document_id>[^/]+)_p[0-9]+\.[^.]+$' --out data/benchmark-manifest.jsonl

python -m bank_ocr merge data/train-manifest.jsonl data/benchmark-manifest.jsonl --out data/manifest.jsonl
```

문서마다 하위 폴더가 있는 구조라면 `--document-regex '^(?P<document_id>[^/]+)/'`를 사용할 수 있습니다.
**이미지 한 장이 독립된 원본 문서인 경우에만** `--single-page-documents`를 사용합니다.
파일명 규칙으로 원본 문서를 알 수 없다면 아래 형식으로 manifest를 직접 만듭니다.

```json
{"document_id":"original_doc_123","page_id":"p001","image":"/share/data/a.png","split":"train"}
{"document_id":"original_doc_456","page_id":"p001","image":"/share/data/b.png","split":"benchmark"}
```

문서 ID는 전체 데이터에서 일관되고 고유해야 합니다. 서로 다른 문서에 같은 ID를 주거나 같은 문서를 서로 다른 ID로 주면 안 됩니다. 근사 복제·스캔 노이즈·동일 템플릿까지 자동 판별하지는 않습니다.

기본으로 학습 문서의 5%를 문서 단위로 validation에 배정합니다. 이미 `val` manifest가 있으면 그 구분을 사용합니다. 벤치마크 문서는 사용자가 지정한 것을 모두 유지하며, view당 과제 수(`tasks_per_view.benchmark`)만큼 고정 seed로 뽑습니다. 별도 hard benchmark 선정이나 1,000페이지 강제 추출은 하지 않습니다.

**완료 기준:** `data/manifest.jsonl`이 생성되어 있습니다.

## 4. 설정 파일 작성 및 데이터 준비

예제 설정은 `manifest=data/manifest.jsonl`, `output_dir=data/prepared-v2`, `cache_dir=data/ocr-cache`, `ocr_callable=internal_ocr_adapter:ocr_from_file`입니다. `ocr_revision`은 실제 OCR 버전으로 변경합니다. 소량 확인과 전체 준비는 서로 다른 `output_dir`를 사용하고, 이후 명령은 전체 준비 결과 경로에 맞춥니다.

```bash
cp config.example.json config.json
# config.json의 manifest / output_dir / cache_dir / ocr_revision 수정
python -m bank_ocr prepare --config config.json
```

설정 파일의 상대경로는 설정 파일 기준입니다. manifest의 상대 이미지 경로는 manifest 기준입니다. 생성 JSONL에는 내부망의 절대 이미지 경로가 들어갑니다. **서버에 반입한 후 prepare를 실행**하세요. 나중에 데이터 위치를 옮기면 경로 재생성이 필요합니다.

주요 결과:

| 파일 | 용도 |
|---|---|
| `pages.jsonl` | 원본 OCR, 좌표, confidence, split, 원본 이미지 경로 |
| `train_sft.jsonl`, `val_sft.jsonl` | MS-SWIFT SFT 입력 |
| `train_grpo.jsonl` | `grpo_tasks` 과제와 reward용 `task`·`target` 필드 |
| `train_tasks.jsonl`, `val_tasks.jsonl`, `benchmark_tasks.jsonl` | 추론·평가 및 분석 입력. `view`(clean/aug)·`view_ops`·`confidence`·`size` 포함 |
| `views/` | 모델 입력 페이지 이미지(clean·aug) |
| `crops/`, `tiles/`, `marked/` | Crop OCR 단어 이미지, spotting 타일, 박스를 그린 이미지 |
| `image_items.jsonl` | 이미지별 교사 OCR 박스(view 좌표). `--with-ocr` 비교군과 점검용 |
| `DONE.json` | 완료 여부, 분리별 개수, 필터 통계, manifest 해시 |
| `config.snapshot.json` | 실행 시 설정 |

OCR 원본과 방향 보정 페이지는 `cache_dir`에 있으므로 **준비가 끝나도 캐시를 지우지 마세요**. 학습·추론이 해당 페이지를 참조합니다.

학습 confidence 기본값은 0.95, 벤치마크는 0.0입니다. 벤치마크에서 낮은 confidence를 숨기지 않습니다. 두 쪽 모두 공백, 길이 범위 밖, 대체문자 `�`를 제외하며, 제외 개수를 기록합니다. 낮은 confidence 단어는 질문 대상이 되지 않고, 그 단어가 걸친 영역·타일·grounding 질문은 만들지 않습니다. 이전 설정 키 `train_regions_per_page`·`benchmark_regions_per_page`는 `tasks_per_view`로 바뀌었고, 남아 있으면 prepare가 중단됩니다.

`output_dir`가 이미 있으면 덮어쓰지 않습니다. 실패한 준비 작업은 새 `output_dir`로 다시 실행하면 성공 OCR 캐시를 재사용합니다. `ocr_revision`은 OCR 모델·전처리·함수 동작이 바뀔 때 변경해야 합니다. 서버를 변경하여 OCR 동작이 달라질 때도 버전을 변경하세요. 어댑터의 서버 주소는 캐시 키에 자동 포함되지 않습니다. 최초 실행은 소량의 train/benchmark 문서로 매핑과 출력량을 확인하는 편이 좋습니다.

**완료 기준:** `data/prepared-v2/DONE.json`과 학습·벤치마크 JSONL이 생성되어 있습니다. 분리별 개수와 필터 통계를 확인합니다.

## 5. 이미 반입한 프로젝트 업데이트 (prepared-v1 → v2)

기존 `bank-ocr-pipeline` 폴더에 새 코드를 덮어쓰고, 이미 돌린 OCR 캐시(`data/ocr-cache`)를 그대로 재사용합니다. OCR은 다시 호출하지 않습니다.

```bash
# 1) 백업 후 덮어쓰기. 업데이트 zip에는 internal_ocr_adapter.py·config.json·data/·predictions/·reports/·runs/가 없어 기존 것이 유지됩니다.
cp -r bank-ocr-pipeline bank-ocr-pipeline.bak
cd bank-ocr-pipeline
unzip -o /반입경로/bank-ocr-pipeline-update.zip
pip install --no-index --no-build-isolation -e .

# 2) config.json을 새 형식으로 (OCR 관련 값은 유지, 새 항목 추가, 결과는 data/prepared-v2)
cp config.json config.json.bak
python - <<'PY'
import json
old = json.load(open("config.json")); new = json.load(open("config.example.json"))
keep = ("manifest", "cache_dir", "ocr_callable", "ocr_revision", "mapping", "seed", "val_fraction", "filters", "sft_max_examples")
cfg = {**new, **{k: old[k] for k in keep if k in old}, "output_dir": "data/prepared-v2"}
json.dump(cfg, open("config.json", "w"), ensure_ascii=False, indent=2)
PY

# 2-1) 이미 만든 prepared-v2가 예전 코드로 만들어졌다면: SFT 파일만 묶음 형식으로 변환 (몇 초, 원본은 *.single.jsonl로 보관)
python -m bank_ocr group-sft --data data/prepared-v2

# 3) 실행 (README의 "실행" 참고)
cp configs/pipeline.example.json configs/pipeline.json
python run_pipeline.py --config configs/pipeline.json --smoke
nohup python run_pipeline.py --config configs/pipeline.json > pipeline.log 2>&1 &
```

- 캐시는 `이미지 픽셀 + ocr_callable + ocr_revision`으로 찾습니다. `cache_dir`·`ocr_callable`·`ocr_revision`을 바꾸면 OCR을 다시 호출합니다.
- 기존 `prepared-v1`, `predictions/`, `reports/`는 지우지 않아도 됩니다. 새 결과는 `runs/exp1/`에 따로 쌓입니다.
- v1 벤치마크(region 기반) 점수는 v2 벤치마크와 비교할 수 없습니다. run_pipeline이 Base부터 다시 평가합니다.
- benchmark manifest가 이미 있으면 `benchmark_fraction`은 적용되지 않고 기존 벤치마크 문서를 그대로 씁니다.
