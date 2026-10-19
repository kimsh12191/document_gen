#!/usr/bin/env bash
# 행 누락 원인 연구를 GPU 서버에서 한 바퀴. 모델마다 vLLM 서버를 띄워 같은 묶음으로 재고, 끝에 모델끼리 비교한다.
# 저장소 루트에서 실행.
#
#   MODELS="base=/models/Qwen3.5-9B bank=/models/bank_sft_merged" GPUS=0 ./run_experiment.sh
#   MODELS="..." N_TEST=10 PROBE_ITEMS=5 ./run_experiment.sh          # 리허설 (작게)
#   MODELS="..." MAX_TOKENS=4096 RUNS=runs_4096 ./run_experiment.sh   # 답 상한을 바꿔서 한 번 더
#
# 순서
#   1. 평가 묶음 N_TEST 개 생성 (머리글·같은 글자 반복 쌍둥이 판 포함) → $DATA/test   (이미 있으면 이어서)
#   2. 모델마다: 서버 띄움 → mpx pipeline (관찰 실행 → 행 기록 → 분석 → 통제 실험 A~F → 종합·viewer) → $RUNS/<이름>/
#      모델 폴더의 generation_config.json 을 $RUNS/<이름>/ 에 복사해 둔다 (repetition_penalty 기본값 확인용)
#   3. 모델 비교 → $RUNS/compare/ (analysis.md, probes_compare.md, viewer/index.html)
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
URL="http://127.0.0.1:$PORT/v1"

serve() {  # serve <모델 폴더> <로그 이름> : 첫 GPU 에 vLLM 서버를 띄우고 준비될 때까지 기다린다
  local gpu=${GPUS%%,*}
  log "서버 시작: $1 (GPU $gpu)"
  CUDA_VISIBLE_DEVICES=$gpu IMAGE_MAX_TOKEN_NUM=3600 swift deploy --model "$1" --model_type qwen3_5 \
    --infer_backend vllm --vllm_max_model_len "$MAX_MODEL_LEN" --vllm_max_num_seqs 16 \
    --vllm_limit_mm_per_prompt '{"image": 32}' --vllm_gpu_memory_utilization 0.9 \
    --host 127.0.0.1 --port "$PORT" --served_model_name mpx --enable_thinking false --max_new_tokens "$MAX_TOKENS" \
    > "$RUNS/logs/serve_$2.log" 2>&1 &
  SERVER=$!
  for _ in $(seq 1 240); do
    curl -sf "$URL/models" >/dev/null && { log "서버 준비됨"; return; }
    kill -0 $SERVER 2>/dev/null || { log "서버가 죽었습니다: $RUNS/logs/serve_$2.log"; exit 1; }
    sleep 10
  done
  log "서버가 40분 안에 뜨지 않았습니다"; kill $SERVER; exit 1
}
stop() { kill "$SERVER" 2>/dev/null || true; wait "$SERVER" 2>/dev/null || true; }

log "1. 생성: 평가 $N_TEST 묶음"
$PY -m mpx gen --out "$DATA/test" --n "$N_TEST" --split test --twins --workers "$WORKERS"

compare_args=()
for spec in $MODELS; do
  name=${spec%%=*}; path=${spec#*=}
  log "2. 모델 $name ($path)"
  mkdir -p "$RUNS/$name"
  cp "$path/generation_config.json" "$RUNS/$name/" 2>/dev/null || log "generation_config.json 없음"
  serve "$path" "$name"; trap stop EXIT
  $PY -m mpx pipeline --out "$RUNS/$name" --data "$DATA/test" --base-url "$URL" --model mpx \
    --max-tokens "$MAX_TOKENS" --budget "$BUDGET" --probe-items "$PROBE_ITEMS" --workers "$WORKERS" \
    | tee "$RUNS/logs/pipeline_$name.log"
  stop; trap - EXIT
  compare_args+=("$name=$RUNS/$name")
done

log "3. 모델 비교"
$PY -m mpx compare --runs "${compare_args[@]}" --data "$DATA/test" --out "$RUNS/compare"
log "→ $RUNS/compare/analysis.md, $RUNS/compare/probes_compare.md, $RUNS/compare/viewer/index.html"
