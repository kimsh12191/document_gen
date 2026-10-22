# OCR 데이터 준비 (내 이미지)

가진 서류 이미지를 사내 OCR에 돌려 OCR 학습·평가 데이터(글자·위치 읽기 8과제)를 만듭니다.
결과 폴더는 studio 데이터셋과 같은 형식이라 학습([training.md](training.md))에 경로만 적으면 됩니다.

- 정답은 **사내 OCR이 읽은 값**입니다. 그래서 점수는 "정확도"가 아니라 "사내 OCR과 얼마나 같게 읽나"입니다.
- 합성 서류로 OCR 데이터를 만들 때는 이 문서가 필요 없습니다. studio `ocr-bench`·`ocr-train` 레시피가 OCR 준비까지 해서 `<이름>/prepared`로 내놓습니다 ([studio.md 2절](studio.md#2-합성-데이터-만들기)).
- 8과제의 질문·정답 예시는 studio **OCR 예시** 메뉴나 [tasks.md](tasks.md#ocr-과제)에 있습니다.

아래 명령은 학습 서버의 코드 폴더(`document_gen/`)에서 실행합니다.

## 1. 사내 OCR 서버 켜기

OCR 결과 JSON을 이미 갖고 있으면 건너뜁니다 (4절).

```bash
# 터미널 1: 켜 둔 채로. 학습에 안 쓸 GPU를 고름
cd /share/mond/ocr_api && GPU_ID=7 SERVER_PORT=30107 python server.py
```
```bash
# 터미널 2: 이후 명령을 실행할 곳
export INTERNAL_OCR_BASE_URL=http://localhost:30107
```

## 2. 설정 파일

```bash
cp docgen/bench/ocr_config.example.json ocr_config.json
```

`ocr_config.json`에서 세 줄만 고칩니다.

```jsonc
"images": "/share/me/ocr_images",   // "manifest" 줄을 지우고 이 줄로. 하위 폴더까지 읽음
"output_dir": "data/ocr-v1",        // 결과 폴더. 새 이름
"ocr_revision": "ocr-2026-10",      // 아무 이름. 사내 OCR이 바뀌면 바꿈
```

- 이미지 한 장을 문서 한 건으로 봅니다. PDF는 쪽마다 이미지로 먼저 바꿉니다.
- 이미지의 10%는 평가용, 5%는 검증용으로 자동으로 떨어집니다. 이미지는 2장 이상이어야 합니다.
- **평가 전용**으로 만들려면 `"split": "benchmark"`를 한 줄 더 적습니다.
- 결과 폴더(`output_dir`, `cache_dir`)는 이미지 폴더 **밖**에 둡니다.
- 상대 경로는 이 설정 파일이 있는 폴더 기준입니다.

## 3. 실행

```bash
python -m docgen.bench.ocr_prepare ocr_config.json
```

`data/ocr-v1/DONE.json`이 생기면 끝입니다. 안의 `page_counts`에 `train`·`val`·`benchmark` 쪽 수가 있습니다.
studio ⑥ 데이터셋 › 폴더 등록에 이 경로를 넣으면 문항·그림을 화면에서 볼 수 있습니다 (선택).

## 4. 경우별

| 경우 | 방법 |
|---|---|
| 학습용 이미지와 평가용 이미지가 따로 있음 | 설정을 두 개 만듦: 학습용(그대로) + 평가용(`"split": "benchmark"`). 학습 설정의 `train`에는 학습용 폴더, `benchmark`에는 평가용 폴더 |
| 이미지를 더 넣음 | `output_dir`만 새 이름으로 다시 실행. 이미 OCR한 그림은 캐시에서 다시 씀 |
| 사내 OCR이 바뀜 | `ocr_revision`과 `output_dir`을 바꿔 다시 실행 |
| OCR JSON이 이미 있음 | manifest 방식으로 (아래) |
| 여러 쪽 문서를 한 문서로 묶어야 함 | manifest 방식으로 (아래) |

**manifest 방식.** `"images"` 대신 이미지 목록 파일을 직접 만들어 `"manifest": "data/manifest.jsonl"`로 적습니다.

```bash
python -c "from docgen.bench.ocr_data import scan, write_jsonl; write_jsonl('data/manifest.jsonl', scan(
  '/share/me/ocr_images', 'train', r'(?P<document_id>[^/]+)_p[0-9]+\.[^.]+$'))"
```

- 셋째 값은 파일 경로에서 문서 ID를 뽑는 규칙입니다. 예시는 `doc123_p001.png` → `doc123`. 문서마다 폴더면 `r'^(?P<document_id>[^/]+)/'`.
- 저장된 OCR JSON을 쓰려면 `ocr_dir='/share/me/ocr_json'` (이미지와 같은 이름, 확장자만 `.json`).
- 평가 전용이면 둘째 값을 `'benchmark'`로, 설정에 `"benchmark_only": true`.

## 5. 에러

| 에러 | 할 일 |
|---|---|
| `Output already exists` | `output_dir`을 새 이름으로. 캐시가 있어 OCR은 다시 안 함 |
| `Manifest must include train and benchmark documents` | 이미지가 너무 적음. 늘리거나 평가 전용으로 |
| `Error: 500`, 연결 실패 | OCR 서버가 꺼졌거나 포트가 다름. `INTERNAL_OCR_BASE_URL` 확인 |
| `Document leakage` / `Duplicate image leakage` | 같은 문서·같은 그림이 학습과 평가에 함께 있음. 평가용 이미지 폴더에서 빼기 |
| `has an EXIF rotation; saved OCR coordinates are ambiguous` | 회전 정보가 있는 그림의 저장된 OCR JSON은 못 씀. 그 그림은 OCR 서버로 |

설정의 나머지 칸(보기 수 `views`, 과제별 문항 수 `tasks_per_view`, 신뢰도 거르기 `filters`, 변형 `augment`)은 예시 값을 그대로 씁니다.
결과 폴더의 파일: `DONE.json`(완료 표시·수량), `meta.json`·`tasks/`(문항), `pages.jsonl`(쪽별 OCR), `views/`·`crops/`(모델이 보는 그림), `config.snapshot.json`(쓴 설정).
