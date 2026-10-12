#!/usr/bin/env bash
# Start a model server and the OCR viewer page together; Ctrl+C stops both.
#
#   bash viewer/start.sh                                   # base model, GPU 0
#   bash viewer/start.sh runs/exp1/merged/sft-v0-...-checkpoint-800 1
#
# Settings (environment variables): MODEL_PORT=8010 VIEW_PORT=7860 SWIFT=swift
#   IMAGE_MAX_TOKEN_NUM=3600 TASKS=data/prepared-v2/benchmark_tasks.jsonl GPU_MEMORY=0.85
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODEL="${1:-/share/cv_share/qwen3.5/9b}"
GPU="${2:-0}"
MODEL_PORT="${MODEL_PORT:-8010}"
VIEW_PORT="${VIEW_PORT:-7860}"
SWIFT="${SWIFT:-swift}"
TASKS="${TASKS:-$ROOT/data/prepared-v2/benchmark_tasks.jsonl}"
LOG="$ROOT/viewer/model-server.log"

if curl -sf "http://127.0.0.1:$MODEL_PORT/v1/models" >/dev/null 2>&1; then
  echo "Port $MODEL_PORT already serves a model; using it (stop it first to load a different model)."
  SERVER_PID=""
else
  echo "Starting model on GPU $GPU, port $MODEL_PORT: $MODEL  (log: $LOG)"
  CUDA_VISIBLE_DEVICES="$GPU" IMAGE_MAX_TOKEN_NUM="${IMAGE_MAX_TOKEN_NUM:-3600}" setsid "$SWIFT" deploy \
    --model "$MODEL" --model_type qwen3_5 --infer_backend vllm \
    --vllm_max_model_len 10240 --vllm_max_num_seqs 8 --vllm_gpu_memory_utilization "${GPU_MEMORY:-0.85}" \
    --host 127.0.0.1 --port "$MODEL_PORT" --served_model_name bank-ocr \
    --enable_thinking false --max_new_tokens 2048 >"$LOG" 2>&1 &
  SERVER_PID=$!
  trap 'echo "Stopping model server"; kill -TERM -- "-$SERVER_PID" 2>/dev/null || kill -TERM "$SERVER_PID" 2>/dev/null || true' EXIT
  printf "Waiting for the model to load"
  until curl -sf "http://127.0.0.1:$MODEL_PORT/v1/models" >/dev/null 2>&1; do
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
      echo; echo "Model server exited. Last lines of $LOG:"; tail -30 "$LOG"; exit 1
    fi
    printf "."; sleep 5
  done
  echo " ready"
fi

ARGS=(--endpoint "http://127.0.0.1:$MODEL_PORT/v1" --port "$VIEW_PORT")
[ -f "$TASKS" ] && ARGS+=(--tasks "$TASKS")
echo "Open http://127.0.0.1:$VIEW_PORT in the browser (VS Code: PORTS tab -> Forward a Port -> $VIEW_PORT)"
python "$ROOT/viewer/ocr_viewer.py" "${ARGS[@]}"
