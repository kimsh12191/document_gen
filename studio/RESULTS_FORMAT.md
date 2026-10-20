# 결과 폴더 형식 (OCR·추론 결과가 이미 있을 때)

- 판: 2 (2026-10-20). 2판: 업무 묶음 파일(6절), 검수 결과가 어디로 가는지(7절)
- 쓰는 곳: studio 가져오기의 "결과 폴더" 방식 ([DESIGN.md 8.6](DESIGN.md#86-결과-폴더-가져오기--ocr추론-결과가-이미-있을-때))

내부 파이프라인이나 모델이 이미 만든 **OCR 결과와 추론 결과를 저장해 둔 폴더**를 studio에 경로로 알려 주면, studio가
포맷끼리 묶고 사람이 추론 결과를 검수한다. 검수한 결과는 실서류 정답이 되어 벤치마크 점수 계산에 쓴다. 같은 폴더의 이미지·OCR로 OCR 벤치마크도 만든다([DESIGN.md 9.2](DESIGN.md#92-ocr-벤치마크--세-출처-모두-1부-형식으로-만든다)).

**이미지와 OCR은 1부 OCR 준비 단계(`python -m bank_ocr scan --ocr-dir`)와 같은 규칙이다.** 1부에서 쓰던 이미지 폴더·OCR 폴더를
옮기지 않고 `meta.json`에 경로만 적으면 된다. studio는 `training/bank_ocr/data.py`의 함수를 그대로 불러 읽는다.

## 1. 폴더 구조

```
<결과 폴더>/
  meta.json                 결과 정보와 읽는 규칙 (2절)
  images/...                쪽 이미지. 하위 폴더 구조는 자유
  ocr/...                   OCR 결과. 이미지와 같은 상대 경로 또는 같은 파일 이름 + .json (3절)
  pred/<문서ID>.json        추론 결과 (4절). 없어도 된다 (그럼 검수는 빈 라벨에서 시작)
  bundles.jsonl             업무 묶음 (6절). 없어도 된다
```

- `images`, `ocr`, `pred`는 `meta.json`에서 다른 경로(결과 폴더 기준 상대 경로 또는 절대 경로)로 바꿀 수 있다.
- studio는 이 폴더를 **읽기만 한다.** 검수 결과는 studio 설정의 `real_data_dir`에 따로 쓴다.

## 2. `meta.json`

```json
{
  "format": "studio-results/1",
  "name": "2026-10 대출서류 bank9b 추론",
  "real_data": true,
  "images_dir": "images",
  "ocr_dir": "ocr",
  "pred_dir": "pred",
  "document_regex": "^(?P<document_id>[^/]+)/page_\\d+\\.png$",
  "mapping": {
    "items_path": "data.basicData", "success_key": "success", "success_value": "Y",
    "text_key": "text", "confidence_key": "confidence", "box_key": "bounding",
    "box_format": "polygon", "points_key": "vertices"
  },
  "ocr": "사내 OCR v3",
  "model": "bank9b-sft-v3",
  "task": "kie",
  "created": "2026-10-21"
}
```

| 키 | 필수 | 뜻 |
|---|---|---|
| `format` | ● | `studio-results/1` |
| `name` | ● | 결과 묶음 이름 |
| `real_data` | ● | 실서류면 `true`. 외부 분석기로 보낼 수 없고, 검수 결과는 저장소에 넣지 않는다 |
| `images_dir`, `ocr_dir`, `pred_dir` | | 기본 `images`, `ocr`, `pred` |
| `document_regex` | ●(둘 중 하나) | 1부 `scan --document-regex`와 같다. 이미지 상대 경로에 맞는 정규식, `(?P<document_id>…)` 묶음이 문서 ID. 여러 쪽 문서를 한 문서로 묶는다. 쪽 순서는 경로 순서 |
| `single_page` | ●(둘 중 하나) | `true`면 이미지 한 장이 한 문서 (1부 `--single-page-documents`). 문서 ID는 확장자를 뺀 상대 경로 |
| `mapping` | | OCR JSON 해석 규칙. 1부 설정(`training/config.example.json`)의 `mapping`과 같은 키. 없으면 사내 OCR 형식(위 예)을 쓴다 |
| `ocr` | | OCR 이름·버전 (기록용) |
| `model` | | 추론에 쓴 모델. 검수 뒤 이 모델의 점수를 바로 낼 때 쓴다 |
| `task` | | 추론한 과제 (`kie`, `marks`, `classify` …) |

## 3. OCR 결과

- **찾는 규칙 (1부 `find_saved_ocr`와 같음):** 이미지 `images/A/page_1.png`의 OCR은 `ocr/A/page_1.json`, `ocr/A/page_1.png.json`, `ocr/page_1.json`, `ocr/page_1.png.json` 순서로 찾는다.
- **내용:** OCR 서버가 돌려준 원본 응답 그대로. 사내 OCR이면 `{"success": "Y", "data": {"basicData": [...]}}`. 다른 OCR이면 `meta.json`의 `mapping`으로 글자·박스·신뢰도 위치를 알려 준다 (1부 `parse_ocr`와 같은 해석).
- **좌표:** 그 이미지 파일의 픽셀. EXIF 회전 정보가 있는 이미지는 저장된 OCR 좌표와 어긋날 수 있으므로 1부와 같이 쓰지 않고, 설정된 OCR로 다시 읽는다.
- OCR 파일이 없는 이미지는 studio가 설정된 `ocr_callable`로 읽는다. 1부와 같은 캐시 키를 쓰므로 1부에서 이미 돌린 이미지는 다시 부르지 않는다.

## 4. 추론 결과 `pred/<문서ID>.json`

문서마다 하나. 문서 ID에 `/`가 있으면 하위 폴더로 둔다 (`pred/A/B.json`).

```json
{
  "doc_type": "loan_application",
  "doc_name": "대출거래신청서",
  "items": [
    {"key": "applicant.name", "label": "성명", "value": "홍길동", "bbox_2d": [264, 231, 384, 249], "page": 1},
    {"key": "loan.amount", "value": "56,000,000", "bbox_2d": [264, 270, 440, 288], "page": 1},
    {"key": "loan.rate_type", "type": "checkbox", "value": "변동", "bbox_2d": [312, 310, 324, 322], "page": 1},
    {"key": "seal.applicant", "type": "seal", "value": true, "bbox_2d": [760, 840, 835, 905], "page": 2}
  ],
  "raw": "모델이 낸 원래 답 문자열 (선택)"
}
```

- `items`는 **평가 세트의 `kie`·`marks` 답과 같은 모양**이다 ([DESIGN.md 9.3](DESIGN.md#93-은행-업무-벤치마크의-좌표--ocr-단계-형식을-그대로-쓰고-문서-이해-과제는-모두-좌표를-함께-답한다)). `bbox_2d`는 OCR 단계와 같은 **그 쪽 이미지 기준 0~1000 정수**, `page`는 1부터(문서 안 쪽 순서).
- 픽셀 좌표면 `bbox_2d` 대신 `bbox`(픽셀)를 쓴다. 위치가 없으면 둘 다 빼도 된다.
- `key`는 모델이 낸 키 그대로 둔다. 표준 키와 다르면 studio에서 포맷 단위로 한 번 맞춘다(키 대응).
- `doc_type`·`doc_name`은 알면 넣는다(서식 ID나 서류명). 모르면 뺀다.
- 중첩 JSON 답(`{"loan": {"amount": ...}}`)만 있으면 `items` 대신 `answer`에 그대로 넣는다. studio가 점 경로로 펴서 위치 없는 항목으로 읽는다.
- 이 모양과 다르게 저장된 추론 결과는 **가져올 일이 생겼을 때 그 결과에 맞는 변환 스크립트를 그때 만든다.** 미리 여러 모양을 지원하지 않는다.

## 5. 검사

```bash
python -m studio.results check <결과 폴더>
```

필수 키, 이미지마다 OCR 파일 찾기(1부 규칙), OCR 해석(`mapping`), 문서 ID와 `pred` 파일 짝, 좌표 범위를 검사하고 문제를 한 번에 모두 보여 준다.

## 6. 업무 묶음 `bundles.jsonl` (선택)

한 고객이 한 업무로 낸 서류들이 어느 문서인지 알면 적는다. 은행 업무의 여러 서류 과제(구비, 대조, 심사)를 실서류로 만들 때 쓴다([DESIGN.md 9.7](DESIGN.md#97-실서류-평가-세트)). 없으면 studio가 검수한 값(성명, 주민번호, 사업자번호)으로 묶음 후보를 제안하고 사람이 확정한다.

```json
{"bundle_id": "2026-10-0012", "scenario": "jeonse_loan", "documents": ["A0012/id_card", "A0012/resident_copy", "A0012/lease"]}
```

| 키 | 필수 | 뜻 |
|---|---|---|
| `bundle_id` | ● | 묶음 ID (접수번호 등) |
| `documents` | ● | 이 묶음에 든 문서 ID 목록 (`pred/`·이미지의 문서 ID와 같은 것) |
| `scenario` | | 업무 시나리오 ID (`docgen/scenarios.json`). 모르면 빼고 studio에서 고른다 |

## 7. 검수 결과가 가는 곳

studio는 결과 폴더에 쓰지 않는다. 검수 결과는 설정의 `real_data_dir`에 쓴다.

```
<real_data_dir>/
  labels/<결과 폴더 이름>/<문서ID>.json        라벨 검수 결과 (항목마다 자동/수정/확인/추가/삭제, 원래 추론 값 포함)
  ocr_reviewed/<결과 폴더 이름>/<이미지 상대 경로>.json   OCR 검수 결과. 사내 OCR 응답 형식 그대로 (1부 scan --ocr-dir 로 바로 읽힘)
  ocr_reviewed/<결과 폴더 이름>/review.jsonl  쪽마다 검수 상태
  bundles/<결과 폴더 이름>.jsonl              업무 묶음 검수 결과 (묶음, 시나리오, 계산·확인한 구비·대조·심사 답)
```
