#!/usr/bin/env bash
# 행 누락 원인 연구를 GPU 서버에서 한 바퀴 (vLLM 서버를 띄워 모델로 실행). 저장소 루트에서 실행.
#
#   START_MODEL=/models/bank_sft_merged GPUS=0 ./run_experiment.sh          # 전부
#   START_MODEL=... N_TEST=10 PROBE_ITEMS=5 ./run_experiment.sh             # 리허설 (작게)
#   START_MODEL=... ./run_experiment.sh probe score                         # 단계만
#
# 단계 (기본: 전부. 이미 끝난 결과는 이어서/건너뜀)
#   gen      평가 묶음 N_TEST 개 (머리글 쌍둥이 판 포함)
#   observe  1단계 관찰: 한 번에 넣기 + 쪽 단위 실행 → runs/rows.jsonl → runs/analysis.md
#   probe    2단계 통제 실험: 해상도·출력 길이·이미지 수·머리글 → runs/probes/probes.md, viewer.html
#   score    종합표 runs/report/report.md, 묶음 viewer data/test/viewer/index.html
#
# MAX_TOKENS: 답 길이 상한. 기본 16384 는 잘림 없이 무엇이 빠지는지 보기 위함.
#             2부 은행 업무 서버 설정(4096)에서 어떻게 되는지 보려면 MAX_TOKENS=4096 RUNS=runs_4096 으로 한 번 더.
set -euo pipefail
cd "$(dirname "$0")"

START_MODEL=${START_MODEL:?START_MODEL 에 실험할 모델(병합된 폴더)을 주세요}
DATA=${DATA:-data}
RUNS=${RUNS:-runs}
GPUS=${GPUS:-0}
N_TEST=${N_TEST:-200}
PROBE_ITEMS=${PROBE_ITEMS:-40}
WORKERS=${WORKERS:-16}
BUDGET=${BUDGET:-12000}
MAX_TOKENS=${MAX_TOKENS:-16384}
PORT=${PORT:-8100}
PY=${PY:-python}
STAGES=${*:-gen observe probe score}

has() { [[ " $STAGES " == *" $1 "* ]]; }
log() { echo "[$(date '+%F %T')] $*"; }
mkdir -p "$RUNS/logs" "$RUNS/preds"
URL="http://127.0.0.1:$PORT/v1"

serve() {  # 첫 GPU 에 vLLM 서버를 띄우고 준비될 때까지 기다린다
  local gpu=${GPUS%%,*}
  log "서버 시작: $START_MODEL (GPU $gpu)"
  CUDA_VISIBLE_DEVICES=$gpu IMAGE_MAX_TOKEN_NUM=3600 swift deploy --model "$START_MODEL" --model_type qwen3_5 \
    --infer_backend vllm --vllm_max_model_len 40960 --vllm_max_num_seqs 16 \
    --vllm_limit_mm_per_prompt '{"image": 32}' --vllm_gpu_memory_utilization 0.9 \
    --host 127.0.0.1 --port "$PORT" --served_model_name mpx --enable_thinking false --max_new_tokens "$MAX_TOKENS" \
    > "$RUNS/logs/serve.log" 2>&1 &
  SERVER=$!
  for _ in $(seq 1 240); do
    curl -sf "$URL/models" >/dev/null && { log "서버 준비됨"; return; }
    kill -0 $SERVER 2>/dev/null || { log "서버가 죽었습니다: $RUNS/logs/serve.log"; exit 1; }
    sleep 10
  done
  log "서버가 40분 안에 뜨지 않았습니다"; kill $SERVER; exit 1
}
stop() { kill "$SERVER" 2>/dev/null || true; wait "$SERVER" 2>/dev/null || true; }

if has gen; then
  log "생성: 평가 $N_TEST 묶음"
  $PY -m mpx gen --out "$DATA/test" --n "$N_TEST" --split test --twins --workers "$WORKERS"
  $PY -m mpx stats --data "$DATA/test" > "$RUNS/test_stats.json"
fi

if has observe || has probe; then
  serve; trap stop EXIT
  if has observe; then
    log "1단계 관찰"
    for method in allatonce pagewise; do
      $PY -m mpx run --data "$DATA/test" --method "$method" --budget "$BUDGET" --max-tokens "$MAX_TOKENS" \
        --base-url "$URL" --model mpx --workers "$WORKERS" --out "$RUNS/preds/$method.jsonl"
    done
    $PY -m mpx rows --data "$DATA/test" --pred "$RUNS"/preds/*.jsonl --out "$RUNS/rows.jsonl"
    $PY -m mpx analyze --rows "$RUNS/rows.jsonl" --out "$RUNS/analysis.md" > /dev/null
    log "→ $RUNS/analysis.md"
  fi
  if has probe; then
    log "2단계 통제 실험"
    $PY -m mpx probe --data "$DATA/test" --out "$RUNS/probes" --max-items "$PROBE_ITEMS" --max-tokens "$MAX_TOKENS" \
      --base-url "$URL" --model mpx --workers "$WORKERS" > /dev/null
    log "→ $RUNS/probes/probes.md, $RUNS/probes/viewer.html"
  fi
  stop; trap - EXIT
fi

if has score; then
  log "종합"
  $PY -m mpx score --data "$DATA/test" --pred "$RUNS"/preds/*.jsonl --out "$RUNS/report" > /dev/null
  $PY -m mpx viewer --data "$DATA/test" --pred "$RUNS"/preds/*.jsonl > /dev/null
  log "→ $RUNS/report/report.md, $DATA/test/viewer/index.html"
fi
