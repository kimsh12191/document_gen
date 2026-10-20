#!/usr/bin/env bash
# guide/tasks.md 와 발표 부록의 예시 데이터를 처음부터 다시 만듭니다.
#   bash guide/examples/make_examples.sh <작업 폴더>          # 데이터만 (1~5단계)
#   bash guide/examples/make_examples.sh <작업 폴더> --docs   # + tasks.md, 이미지, 부록 슬라이드, index.html 갱신
# 저장소 맨 위에서, docgen·ocr/·bank/ 의존성이 모두 깔린 환경에서 실행합니다. 약 10분, 디스크 약 0.5GB.
set -euo pipefail
W=$(realpath -m "${1:?작업 폴더를 주세요}")
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT"
mkdir -p "$W"

# 1) 합성 서류 3종 × 3건 (페이지 이미지 + 정답 라벨)
python -m docgen generate --types loan_application,withholding_receipt,resident_registration_copy --n 3 --png --out "$W/gen"

# 2) 정답 라벨 → 사내 OCR 응답 형식 JSON (페이지 이미지와 같은 이름). 실제 데이터는 이 자리에 사내 OCR 결과가 옵니다.
python guide/examples/labels_to_ocr.py "$W/gen" "$W/ocr_json"

# 3) 1부 OCR: scan → manifest, 설정 → prepare (실제 학습과 같은 코드)
(cd ocr && python -m bank_ocr scan --root "$W/gen/images" --split train \
  --document-regex '(?P<document_id>[^/]+_\d+)(_p\d+)?\.png$' --ocr-dir "$W/ocr_json" --out "$W/ocr_manifest.jsonl")
python - "$W" <<'EOF'
import json, sys
w = sys.argv[1]
cfg = json.load(open("ocr/config.example.json", encoding="utf-8"))
# 예시용으로 바꾼 값: 경로, OCR 버전 이름, 문서 9건이라 벤치마크·검증 비율을 키우고 SFT 수를 줄임
cfg.update(manifest=f"{w}/ocr_manifest.jsonl", output_dir=f"{w}/ocr_prepared", cache_dir=f"{w}/ocr_cache",
           ocr_revision="example-labels-v1", benchmark_fraction=0.3, sft_max_examples=200, val_fraction=0.15)
json.dump(cfg, open(f"{w}/ocr_config.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
EOF
(cd ocr && python -m bank_ocr prepare --config "$W/ocr_config.json")

# 4) 2부 은행 업무: 평가 세트 (실제 학습 데이터와 같은 build 코드, 업무마다 고객 6묶음)
python -m docgen.bench build --out "$W/bench" --types loan_application --bundles 6 --workers 6

# 5) 끝. 아래는 --docs 일 때만
[ "${2:-}" = "--docs" ] || { echo "데이터: $W  (문서 갱신은 --docs)"; exit 0; }

# 6) 과제별 예시 고르기 → guide/tasks.md, guide/examples/img/, 슬라이드용 examples.json
python guide/examples/make_catalog.py --bench "$W/bench" --ocr "$W/ocr_prepared" --ocr-json "$W/ocr_json" --dump "$W/examples.json"
# 7) 부록 슬라이드. 새 이미지는 웹 슬라이드에 올리고 guide/slides/asset_map.json 에 추가해야 합니다 (guide/slides/README.md)
python guide/slides/make_appendix.py --examples "$W/examples.json" --assets guide/slides/asset_map.json --deck guide/slides/project
python guide/slides/build_html.py
