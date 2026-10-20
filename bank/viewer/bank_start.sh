#!/usr/bin/env bash
# Banking-task viewer: stored benchmark answers of the pipeline's models, and (with a model) your own files.
# Run from bank/ (model paths are relative to it); usage in viewer/README.md.
#
#   bash viewer/bank_start.sh                                          # stored answers only, no GPU
#   bash viewer/bank_start.sh runs/bank1/merged/sft-v0-...-checkpoint-800 1   # + this model on GPU 1
#
# Settings (environment variables): CONFIG=configs/bank_pipeline.json SMOKE=1 (rehearsal run)
#   MODEL_PORT=8011 VIEW_PORT=7861 SWIFT=swift GPU_MEMORY=0.85 IMAGE_MAX_TOKEN_NUM=3600
#   VIEW_HOST=0.0.0.0 opens the page to other PCs as http://<server IP>:VIEW_PORT (default: this machine only)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODEL="${1:-}"
GPU="${2:-0}"
CONFIG="${CONFIG:-$ROOT/configs/bank_pipeline.json}"
MODEL_PORT="${MODEL_PORT:-8011}"
VIEW_PORT="${VIEW_PORT:-7861}"
VIEW_HOST="${VIEW_HOST:-127.0.0.1}"
SWIFT="${SWIFT:-swift}"
LOG="$ROOT/viewer/bank-model-server.log"
ARGS=(--config "$CONFIG" --host "$VIEW_HOST" --port "$VIEW_PORT")
[ -n "${SMOKE:-}" ] && ARGS+=(--smoke)

if [ -n "$MODEL" ]; then
  if curl -sf "http://127.0.0.1:$MODEL_PORT/v1/models" >/dev/null 2>&1; then
    echo "Port $MODEL_PORT already serves a model; using it (stop it first to load a different model)."
  else
    echo "Starting model on GPU $GPU, port $MODEL_PORT: $MODEL  (log: $LOG)"
    # Same server settings as the pipeline's evaluation: up to 16 images per question.
    CUDA_VISIBLE_DEVICES="$GPU" IMAGE_MAX_TOKEN_NUM="${IMAGE_MAX_TOKEN_NUM:-3600}" setsid "$SWIFT" deploy \
      --model "$MODEL" --model_type qwen3_5 --infer_backend vllm \
      --vllm_max_model_len 20480 --vllm_max_num_seqs 8 --vllm_limit_mm_per_prompt '{"image": 16}' \
      --vllm_gpu_memory_utilization "${GPU_MEMORY:-0.85}" \
      --host 127.0.0.1 --port "$MODEL_PORT" --served_model_name bank-ocr \
      --enable_thinking false --max_new_tokens 4096 >"$LOG" 2>&1 &
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
  ARGS+=(--endpoint "http://127.0.0.1:$MODEL_PORT/v1")
fi

if [ "$VIEW_HOST" = "127.0.0.1" ]; then
  echo "Open http://127.0.0.1:$VIEW_PORT in the browser (VS Code: PORTS tab -> Forward a Port -> $VIEW_PORT)"
else
  echo "Open http://$(hostname -I 2>/dev/null | awk '{print $1}'):$VIEW_PORT from another PC (server IP; a Docker container needs this port published)"
fi
python "$ROOT/viewer/bank_viewer.py" "${ARGS[@]}"
