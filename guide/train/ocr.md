# OCR 데이터 준비 (내 이미지)

가진 서류 이미지를 사내 OCR에 돌려 OCR 학습·평가 데이터(글자·위치 읽기 8과제)를 만듭니다.
결과 폴더는 studio 데이터셋과 같은 형식이라 학습 설정의 `data.train`·`data.benchmark` 에 경로만 적으면 됩니다 ([sweep.md](sweep.md)).

- 정답은 **사내 OCR이 읽은 값**입니다. 그래서 점수는 "정확도"가 아니라 "사내 OCR과 얼마나 같게 읽나"입니다.
- 합성 서류로 OCR 데이터를 만들 때는 이 문서가 필요 없습니다. studio `ocr-bench`·`ocr-train` 레시피가 OCR 준비까지 해서 `<이름>/prepared`로 내놓습니다 ([데이터셋 만들기](../studio/data.md#1-화면으로-만들기)).
- 8과제의 질문·정답 예시는 studio **OCR 예시** 메뉴나 [tasks.md](../reference/tasks.md#ocr-과제)에 있습니다.

아래 명령은 학습 서버의 코드 폴더(`document_gen/`)에서 실행합니다.

## 0. 무엇을 준비하나

**시작점은 서류 이미지가 있는 폴더입니다.** 기본 사용에서는 `manifest.jsonl`을 만들 필요가 없습니다.

```text
이미지 폴더 (images)
  → 문서 단위로 train / val / benchmark 분리
  → 사내 OCR로 글자·좌표 읽기 (이미 처리한 이미지는 캐시 재사용)
  → 원본 기반 보기·변형 보기와 질문·정답 만들기
  → 준비된 데이터 폴더 (output_dir)
  → 학습·평가 설정에서 이 폴더 사용
```

| 입력 방식 | 언제 쓰나 | 설정 |
|---|---|---|
| 이미지 폴더 | 한 이미지가 독립된 문서이고 OCR을 새로 돌릴 때 | `"images": "/share/me/ocr_images"` |
| 이미지 목록 파일 | 여러 페이지를 같은 문서로 묶거나, 저장된 OCR JSON·분할을 지정할 때 | `"manifest": "data/manifest.jsonl"` |

두 방식 중 하나만 적습니다. `manifest`는 이미지 자체나 OCR 결과가 아니라 **어떤 이미지가 어떤 문서·분할에 속하는지 적은 목록**입니다 (4절).
같은 문서의 여러 페이지가 있는 경우에는 manifest로 문서 ID를 묶어야 학습과 평가에 나뉘어 들어가지 않습니다.

입력은 PNG, JPG/JPEG, 단일 페이지 TIF/TIFF, BMP, WEBP입니다. PDF와 여러 페이지 TIFF는 먼저 페이지별 이미지로 변환합니다.
실서류는 외부 모델·서비스에 보내지 않고 사내 OCR만 사용합니다.

## 1. 사내 OCR 서버 켜기

OCR 결과 JSON을 이미 갖고 있으면 건너뜁니다 (4절).
이미 운영 중인 사내 OCR 서버를 사용할 때도 새 서버를 켤 필요 없이 아래 주소만 지정합니다.

```bash
# 터미널 1: 켜 둔 채로. 학습에 안 쓸 GPU를 고름
cd <사내 OCR 서버 폴더> && GPU_ID=7 SERVER_PORT=30107 python server.py
```
```bash
# 터미널 2: 이후 명령을 실행할 곳
export INTERNAL_OCR_BASE_URL=http://localhost:30107
```

`localhost`는 **준비 명령을 실행하는 학습 서버 자신**입니다. OCR 서버가 다른 장비라면 그 장비의 사내 주소로 바꿉니다.
기본 어댑터는 이 주소의 `/ocr`에 이미지 파일을 전송합니다. 이미지 폴더도 학습 서버에서 읽을 수 있는 경로여야 합니다.

## 2. 설정 파일

```bash
cp docgen/bench/ocr_config.example.json ocr_config.json
```

복사한 `ocr_config.json`에서 입력·출력 경로와 OCR 버전을 실제 환경에 맞춥니다. 아래는 바꿀 항목만 발췌한 것이며, 나머지 설정은 복사한 예제에 그대로 둡니다.

```jsonc
"images": "/share/me/ocr_images",   // 입력 이미지 폴더. 하위 폴더까지 읽음
"output_dir": "data/ocr-v1",        // 결과 폴더. 새 이름
"cache_dir": "data/ocr-cache",      // 반복 실행에서 재사용할 OCR 캐시
"ocr_revision": "ocr-2026-10",      // 사용한 사내 OCR 모델·설정 버전. 바뀌면 새 값
```

위 설명의 `//` 주석은 실제 JSON 파일에 넣지 않습니다. 이전 예제에 `manifest`가 있다면 그 줄을 지우고 `images`로 바꿉니다.

예를 들어 저장소 루트에 설정을 두면 다음과 같습니다.

```text
document_gen/
  ocr_config.json
  data/
    ocr_images/       ← 원본 이미지 (images가 data/ocr_images일 때)
      page001.png
      page002.jpg
      page003.png
    ocr-cache/        ← 자동 생성·재사용
    ocr-v1/           ← 실행 전에는 없어야 함
```

| 설정 | 의미 |
|---|---|
| `ocr_callable` | OCR 호출 함수. 기본값 `studio.internal_ocr_adapter:ocr_from_file`은 사내 OCR API를 사용 |
| `mapping` | OCR 응답 JSON에서 글자·신뢰도·좌표를 찾는 규칙. 기본값은 `data.basicData` 아래의 `text`, `confidence`, `bounding.vertices`를 읽음. 다른 응답 형식이면 맞춰야 함 |
| `ocr_revision` | OCR 캐시 구분에 쓰는 버전. 모델이나 OCR 설정을 바꾸고도 같은 값을 쓰면 이전 결과가 재사용될 수 있음 |

- 이미지 한 장을 문서 한 건으로 봅니다. PDF는 쪽마다 이미지로 먼저 바꿉니다.
- 기본값은 전체 문서의 약 10%를 평가용으로 먼저 떼고, 남은 학습 후보의 약 5%를 검증용으로 뗍니다. 반올림과 최소 1건 규칙이 있어 작은 입력에서는 비율이 달라집니다. 기본 설정은 독립된 문서가 최소 3건 필요합니다 (`val_fraction: 0`이면 최소 2건).
- **평가 전용**으로 만들려면 `"split": "benchmark"`를 한 줄 더 적습니다.
- 결과 폴더(`output_dir`, `cache_dir`)는 이미지 폴더 **밖**에 둡니다.
- 상대 경로는 이 설정 파일이 있는 폴더 기준입니다.

## 3. 실행

학습(실험 묶음)과 상관없이 **한 번만** 돌립니다.

```bash
python -m docgen.bench.ocr_prepare ocr_config.json
```

만든 결과 폴더(`output_dir`)를 학습 설정의 `data.train`·`data.benchmark` 에 경로로 적습니다. 실험마다 다시 만들지 않습니다.

`data/ocr-v1/DONE.json`이 생기면 처리가 끝난 것입니다. **모든 이미지가 성공했다거나 사람이 검수했다는 뜻은 아닙니다.** 이미지 읽기·OCR·보기 생성에 실패한 페이지는 기록하고 나머지 페이지로 계속 진행할 수 있습니다.

1. `DONE.json`의 `page_counts`에서 `train`·`val`·`benchmark`별 실제 페이지 수를 확인합니다.
2. `skipped_pages`와 `skipped_by_stage`를 확인합니다. 누락이 있으면 `skipped.jsonl`의 이미지 경로·단계·오류를 확인합니다.
3. studio **데이터셋 › <이름> › 문항**에서 사람이 그림·질문·정답을 확인합니다. 사내 OCR이 잘못 읽으면 그 값이 정답으로 들어갈 수 있습니다.

`DONE.json`이 없는 결과 폴더는 미완료이므로 학습에 쓰지 않습니다.
studio 데이터셋 › 폴더 등록 (맨 아래)에 이 경로를 넣으면 문항·그림을 화면에서 볼 수 있습니다 (선택).

## 4. 경우별

| 경우 | 방법 |
|---|---|
| 학습용 이미지와 평가용 이미지가 따로 있음 | 설정을 두 개 만듦: 학습용(그대로) + 평가용(`"split": "benchmark"`). `data.train` 에는 학습용 폴더, `data.benchmark` 에는 평가용 폴더 |
| 이미지를 더 넣음 | `output_dir`만 새 이름으로 다시 실행. 이미 OCR한 그림은 캐시에서 다시 씀 |
| 사내 OCR이 바뀜 | `ocr_revision`과 `output_dir`을 바꿔 다시 실행 |
| OCR JSON이 이미 있음 | manifest 방식으로 (아래) |
| 여러 쪽 문서를 한 문서로 묶어야 함 | manifest 방식으로 (아래) |

**manifest 방식.** `"images"` 대신 이미지 목록 파일을 직접 만들어 `"manifest": "data/manifest.jsonl"`로 적습니다.

JSONL은 한 줄에 JSON 객체 하나를 적는 형식입니다. 예를 들어 같은 문서의 두 페이지는 다음처럼 같은 `document_id`로 묶습니다.

```jsonl
{"document_id":"doc123","page_id":"p001","image":"/share/me/ocr_images/doc123_p001.png","split":"train"}
{"document_id":"doc123","page_id":"p002","image":"/share/me/ocr_images/doc123_p002.png","split":"train"}
```

| 필드 | 의미 |
|---|---|
| `document_id` | 문서 ID. 같은 문서의 모든 페이지는 같은 ID·분할 사용 |
| `page_id` | 해당 문서 안에서 중복되지 않는 페이지 ID |
| `image` | 이미지 파일 경로. 상대 경로는 **manifest 파일이 있는 폴더** 기준 |
| `split` | `train`, `val`, `benchmark`. 평가·검증 분할이 없으면 설정 비율에 따라 train 문서에서 자동 분리 |
| `ocr_json` | 선택 사항. 저장된 OCR 응답 JSON 경로. 해당 행은 서버 호출 대신 이 파일을 읽음. 상대 경로 기준은 manifest 폴더 |

위 두 줄은 문서 묶기 예시입니다. 기본 분할 설정으로 실행하려면 독립된 문서가 더 필요합니다.
`images`를 지우고 `manifest`를 지정하며, 나머지 OCR·문항 생성 설정은 그대로 사용합니다.

파일 이름에서 문서 ID를 뽑아 목록을 자동으로 만드는 예:

```bash
python -c "from docgen.bench.ocr_data import scan, write_jsonl; write_jsonl('data/manifest.jsonl', scan(
  '/share/me/ocr_images', 'train', r'(?P<document_id>[^/]+)_p[0-9]+\.[^.]+$'))"
```

- 셋째 값은 파일 경로에서 문서 ID를 뽑는 규칙입니다. 예시는 `doc123_p001.png` → `doc123`. 문서마다 폴더면 `r'^(?P<document_id>[^/]+)/'`.
- 저장된 OCR JSON을 쓰려면 `ocr_dir='/share/me/ocr_json'` (이미지와 같은 이름, 확장자만 `.json`).
- 평가 전용이면 둘째 값을 `'benchmark'`로, 설정에 `"benchmark_only": true`.

한 이미지가 한 문서이고 저장된 OCR JSON이 있는 경우에는 다음처럼 만듭니다. OCR JSON은 예제의 `mapping`으로 읽을 수 있는 응답 구조여야 합니다.

```bash
python -c "from docgen.bench.ocr_data import scan, write_jsonl; write_jsonl('data/manifest.jsonl', scan('/share/me/ocr_images', 'train', single_page=True, ocr_dir='/share/me/ocr_json'))"
```

모든 행에 `ocr_json`이 있으면 OCR 서버는 필요 없습니다. 일부 행에만 있으면 나머지 이미지는 `ocr_callable`로 처리합니다.

## 5. 에러

| 에러 | 할 일 |
|---|---|
| `Output already exists` | `output_dir`을 새 이름으로. 캐시가 있어 OCR은 다시 안 함 |
| `Manifest must include train and benchmark documents` | 이미지가 너무 적음. 늘리거나 평가 전용으로 |
| `Need at least two training documents for validation` | 평가용 분리 후 학습 후보가 1건뿐임. 독립된 문서를 늘리거나 `val_fraction`을 `0`으로 |
| `Error: 500`, 연결 실패 | OCR 서버가 꺼졌거나 포트가 다름. `INTERNAL_OCR_BASE_URL` 확인 |
| `Document leakage` / `Duplicate image leakage` | 같은 문서·같은 그림이 학습과 평가에 함께 있음. 평가용 이미지 폴더에서 빼기 |
| `has an EXIF rotation; saved OCR coordinates are ambiguous` | 회전 정보가 있는 그림의 저장된 OCR JSON은 못 씀. 그 그림은 OCR 서버로 |

설정의 나머지 칸(보기 수 `views`, 과제별 문항 수 `tasks_per_view`, 신뢰도 거르기 `filters`, 변형 `augment`)은 예시 값을 그대로 씁니다.
결과 폴더의 파일: `DONE.json`(완료 표시·수량·누락 수), `meta.json`·`tasks/`(문항), `pages.jsonl`(쪽별 OCR), `skipped.jsonl`(실패한 페이지·이유), `views/`·`crops/`(모델이 보는 그림), `config.snapshot.json`(쓴 설정).
