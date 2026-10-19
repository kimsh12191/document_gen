#!/usr/bin/env bash
# 행 누락 원인 연구를 GPU 서버에서 한 바퀴. 모델마다 vLLM 서버를 동시에 띄우고, 한 pipeline 이 같은 묶음으로
# 모든 모델을 동시에 재고 끝에 비교까지 낸다. 저장소 루트에서 실행.
#
#   MODELS="base=/models/Qwen3.5-9B bank=/models/bank_sft_merged" GPUS=0,1 ./run_experiment.sh
#   MODELS="..." N_TEST=10 PROBE_ITEMS=5 ./run_experiment.sh          # 리허설 (작게)
#   MODELS="..." MAX_TOKENS=4096 RUNS=runs_4096 ./run_experiment.sh   # 답 상한을 바꿔서 한 번 더
#
# GPU 배치: 모델 i 는 GPUS 의 (i mod GPU 수) 번째 GPU. GPU 가 모델보다 적으면 한 GPU 에 서버 여럿을 올리고
# 메모리 비율(0.9)을 나눠 준다 (9B 둘이면 80GB 한 장에 0.45 씩).
#
# 순서
#   1. 평가 묶음 N_TEST 개 생성 (머리글·같은 글자 반복 쌍둥이 판 포함) → $DATA/test   (이미 있으면 이어서)
#   2. 모델마다 서버를 동시에 띄움 (포트 PORT, PORT+1, ...; 모델 폴더의 generation_config.json 을 $RUNS/<이름>/ 에 복사)
#   3. mpx pipeline --models : 모델마다 관찰 실행 → 행 기록 → 분석 → 통제 실험 A~F → 종합·viewer 를 동시에 → $RUNS/<이름>/
#      이어서 모델 비교 → $RUNS/compare/ (report.md, paired.md, probes_compare.md, analysis.md, viewer/index.html)
#   4. 결과 첫 화면 $RUNS/index.html. 보기: python -m mpx serve $RUNS --host 0.0.0.0
set -euo pipefail
cd "$(dirname "$0")"

MODELS=${MODELS:?MODELS 에 '이름=모델폴더' 를 공백으로 (예: base=/models/Qwen3.5-9B bank=/models/bank_sft_merged)}
DATA=${DATA:-data}
RUNS=${RUNS:-runs}
GPUS=${GPUS:-0}
N_TEST=${N_TEST:-200}
PROBE_ITEMS=${PROBE_ITEMS:-40}
WORKERS=${WORKERS:-16}
BUDGET=${BUDGET:-12000}
MAX_TOKENS=${MAX_TOKENS:-20480}
MAX_MODEL_LEN=${MAX_MODEL_LEN:-40960}   # 이미지 12,000 + 질문 + 답 MAX_TOKENS 가 들어가야 함
PORT=${PORT:-8100}
PY=${PY:-python}

log() { echo "[$(date '+%F %T')] $*"; }
mkdir -p "$RUNS/logs"

IFS=, read -ra gpu_list <<< "$GPUS"
read -ra specs <<< "$MODELS"
declare -A per_gpu=()
for i in "${!specs[@]}"; do g=${gpu_list[$((i % ${#gpu_list[@]}))]}; per_gpu[$g]=$(( ${per_gpu[$g]:-0} + 1 )); done

SERVERS=()
stop() { for pid in "${SERVERS[@]}"; do kill "$pid" 2>/dev/null || true; done; wait 2>/dev/null || true; }
trap stop EXIT

command -v swift >/dev/null || { log "swift(ms-swift) 가 PATH 에 없습니다"; exit 1; }
have=$(cat "$DATA/test/bundles.jsonl" 2>/dev/null | grep -c . || true)
if [ "$have" -ge "$N_TEST" ]; then
  log "1. 생성 건너뜀: $DATA/test 에 이미 $have 묶음"
else
  log "1. 생성: 평가 $N_TEST 묶음 (Chromium 필요. GPU 환경에 없으면 docgen 도커에서 먼저 만들어 $DATA/test 에 두기)"
  $PY -m mpx gen --out "$DATA/test" --n "$N_TEST" --split test --twins --workers "$WORKERS"
fi
# 한 번에 넣기는 묶음의 모든 쪽을 한 요청에 넣으므로, 서버의 요청당 이미지 수 상한을 가장 큰 묶음 이상으로
MAX_PAGES=$($PY -c "import json; print(max(len(json.loads(l)['pages']) for l in open('$DATA/test/bundles.jsonl') if l.strip()))")
MM_LIMIT=$(( MAX_PAGES > 32 ? MAX_PAGES : 32 ))
log "가장 큰 묶음 $MAX_PAGES 쪽 → 요청당 이미지 상한 $MM_LIMIT"

model_args=()
for i in "${!specs[@]}"; do
  name=${specs[$i]%%=*}; path=${specs[$i]#*=}
  gpu=${gpu_list[$((i % ${#gpu_list[@]}))]}; port=$((PORT + i))
  util=$(awk "BEGIN{printf \"%.2f\", 0.9 / ${per_gpu[$gpu]}}")
  mkdir -p "$RUNS/$name"
  cp "$path/generation_config.json" "$RUNS/$name/" 2>/dev/null || log "$name: generation_config.json 없음"
  log "2. 서버 시작: $name ($path) GPU $gpu, 포트 $port, 메모리 $util"
  CUDA_VISIBLE_DEVICES=$gpu IMAGE_MAX_TOKEN_NUM=3600 swift deploy --model "$path" --model_type qwen3_5 \
    --infer_backend vllm --vllm_max_model_len "$MAX_MODEL_LEN" --vllm_max_num_seqs 16 \
    --vllm_limit_mm_per_prompt "{\"image\": $MM_LIMIT}" --vllm_gpu_memory_utilization "$util" \
    --host 127.0.0.1 --port "$port" --served_model_name "$name" --enable_thinking false --max_new_tokens "$MAX_TOKENS" \
    > "$RUNS/logs/serve_$name.log" 2>&1 &
  SERVERS+=($!)
  model_args+=("$name=http://127.0.0.1:$port/v1")
done

for i in "${!specs[@]}"; do
  name=${specs[$i]%%=*}; url=${model_args[$i]#*=}
  for t in $(seq 1 241); do
    curl -sf "$url/models" >/dev/null && { log "서버 준비됨: $name"; break; }
    kill -0 "${SERVERS[$i]}" 2>/dev/null || { log "서버가 죽었습니다: $RUNS/logs/serve_$name.log"; exit 1; }
    [ "$t" -eq 241 ] && { log "$name 서버가 40분 안에 뜨지 않았습니다"; exit 1; }
    sleep 10
  done
done

log "3. pipeline: ${model_args[*]}"
$PY -m mpx pipeline --out "$RUNS" --data "$DATA/test" --models "${model_args[@]}" \
  --max-tokens "$MAX_TOKENS" --budget "$BUDGET" --probe-items "$PROBE_ITEMS" --workers "$WORKERS" \
  | tee "$RUNS/logs/pipeline.log"
log "→ 결과 첫 화면 $RUNS/index.html  (띄우기: $PY -m mpx serve $RUNS --host 0.0.0.0)"
