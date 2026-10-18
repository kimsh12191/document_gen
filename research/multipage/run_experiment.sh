#!/usr/bin/env bash
# 행 누락 원인 연구 (내부망 GPU 서버). research/multipage 에서 실행.
#
#   START_MODEL=/models/bank_sft_merged GPUS=0 ./run_experiment.sh                   # 1·2단계 (기본)
#   START_MODEL=... N_TEST=10 PROBE_ITEMS=5 ./run_experiment.sh                       # 리허설
#   START_MODEL=... ./run_experiment.sh gen sft train merge eval score                # 3단계 처방(학습)까지
#
# 단계 (기본: gen observe probe score. 이미 끝난 결과는 이어서/건너뜀)
#   gen      평가 묶음 N_TEST (머리글 쌍둥이 판 포함). 3단계를 하면 학습 묶음 N_TRAIN 도
#   observe  1단계 관찰: 출발 모델로 한 번에 넣기 + 쪽 단위(STATES) → rows.jsonl → analysis.md
#   probe    2단계 통제 실험: 해상도·출력 길이·이미지 수·머리글 → runs/probes/probes.md, viewer.html
#   score    종합표 runs/report/report.md, 묶음 viewer data/test/viewer/index.html
#   (3단계 처방) sft 학습 데이터, train 쪽 단위+상태 / 한 번에 넣기 학습, merge LoRA 병합, eval 학습 모델 평가
set -euo pipefail
cd "$(dirname "$0")"

START_MODEL=${START_MODEL:?START_MODEL 에 출발 모델(2부 은행 업무 모델, 병합된 폴더)을 주세요}
DATA=${DATA:-data}
RUNS=${RUNS:-runs}
GPUS=${GPUS:-0,1}
N_TRAIN=${N_TRAIN:-2000}
N_TEST=${N_TEST:-200}
PROBE_ITEMS=${PROBE_ITEMS:-40}
WORKERS=${WORKERS:-16}
BUDGET=${BUDGET:-12000}
PORT=${PORT:-8100}
MAX_STEPS=${MAX_STEPS:-}
STATES=${STATES:-"none"}
PY=${PY:-python}
STAGES=${*:-gen observe probe score}

has() { [[ " $STAGES " == *" $1 "* ]]; }
log() { echo "[$(date '+%F %T')] $*"; }
mkdir -p "$RUNS/logs" "$RUNS/preds"

serve() {  # serve <모델 폴더> <max_model_len> : 첫 GPU 에 vLLM 서버를 띄우고 준비될 때까지 기다린다
  local model=$1 len=$2 gpu=${GPUS%%,*}
  log "서버 시작: $model (GPU $gpu, max_model_len $len)"
  CUDA_VISIBLE_DEVICES=$gpu IMAGE_MAX_TOKEN_NUM=3600 swift deploy --model "$model" --model_type qwen3_5 \
    --infer_backend vllm --vllm_max_model_len "$len" --vllm_max_num_seqs 16 \
    --vllm_limit_mm_per_prompt '{"image": 32}' --vllm_gpu_memory_utilization 0.9 \
    --host 127.0.0.1 --port "$PORT" --served_model_name mpx --enable_thinking false --max_new_tokens 16384 \
    > "$RUNS/logs/serve_$(basename "$model").log" 2>&1 &
  SERVER=$!
  for _ in $(seq 1 240); do
    curl -sf "http://127.0.0.1:$PORT/v1/models" >/dev/null && { log "서버 준비됨"; return; }
    kill -0 $SERVER 2>/dev/null || { log "서버가 죽었습니다: $RUNS/logs/serve_$(basename "$model").log"; exit 1; }
    sleep 10
  done
  log "서버가 40분 안에 뜨지 않았습니다"; kill $SERVER; exit 1
}
stop() { kill "$SERVER" 2>/dev/null || true; wait "$SERVER" 2>/dev/null || true; }

evaluate() {  # evaluate <이름 접두어> : 띄운 서버로 평가 세트를 모든 방법으로
  local tag=$1
  $PY -m mpx run --data "$DATA/test" --method allatonce --budget "$BUDGET" --max-tokens 16384 \
    --base-url "http://127.0.0.1:$PORT/v1" --model mpx --out "$RUNS/preds/${tag}_all.jsonl"
  for st in $STATES; do
    $PY -m mpx run --data "$DATA/test" --method pagewise --state "$st" --max-tokens 4096 \
      --base-url "http://127.0.0.1:$PORT/v1" --model mpx --out "$RUNS/preds/${tag}_pw_${st}.jsonl"
  done
}

last_ckpt() { ls -d "$1"/*/checkpoint-* 2>/dev/null | sort -V | tail -1; }

if has gen; then
  log "생성: 평가 $N_TEST 묶음 (쌍둥이 판 포함)"
  $PY -m mpx gen --out "$DATA/test" --n "$N_TEST" --split test --twins --workers "$WORKERS"
  $PY -m mpx stats --data "$DATA/test" > "$RUNS/test_stats.json"
  if has sft || has train; then
    log "생성: 학습 $N_TRAIN 묶음"
    $PY -m mpx gen --out "$DATA/train" --n "$N_TRAIN" --split train --compose random --workers "$WORKERS"
  fi
fi

URL="http://127.0.0.1:$PORT/v1"
if has observe || has probe; then
  serve "$START_MODEL" 40960; trap stop EXIT
  if has observe; then
    log "1단계 관찰"
    evaluate zeroshot
    $PY -m mpx rows --data "$DATA/test" --pred "$RUNS"/preds/zeroshot_*.jsonl --out "$RUNS/rows.jsonl"
    $PY -m mpx analyze --rows "$RUNS/rows.jsonl" --out "$RUNS/analysis.md" > /dev/null
    log "→ $RUNS/analysis.md"
  fi
  if has probe; then
    log "2단계 통제 실험"
    $PY -m mpx probe --data "$DATA/test" --out "$RUNS/probes" --max-items "$PROBE_ITEMS" --base-url "$URL" --model mpx \
      --workers "$WORKERS" > /dev/null
    log "→ $RUNS/probes/probes.md"
  fi
  stop; trap - EXIT
fi

if has sft; then
  log "학습 데이터"
  $PY -m mpx sft --data "$DATA/train" --budget "$BUDGET" | tee "$RUNS/sft_stats.json"
fi

steps=()
[[ -n "$MAX_STEPS" ]] && steps=(--max-steps "$MAX_STEPS")
if has train; then
  for kind in page all; do
    [[ -n "$(last_ckpt "$RUNS/${kind}_sft")" && -z "$MAX_STEPS" ]] && { log "$kind 학습은 이미 있음"; continue; }
    log "학습: $kind"
    $PY ../../training/train.py sft --config "configs/${kind}_sft.yaml" --model "$START_MODEL" \
      --data "$DATA/train/swift_$kind" --output "$RUNS/${kind}_sft" --gpus "$GPUS" "${steps[@]}" --execute \
      2>&1 | tee "$RUNS/logs/train_$kind.log"
  done
fi

if has merge; then
  for kind in page all; do
    [[ -d "$RUNS/${kind}_merged" ]] && continue
    ckpt=$(last_ckpt "$RUNS/${kind}_sft")
    [[ -n "$ckpt" ]] || { log "$kind 체크포인트가 없습니다"; exit 1; }
    log "병합: $ckpt"
    CUDA_VISIBLE_DEVICES=${GPUS%%,*} swift export --model "$START_MODEL" --model_type qwen3_5 --adapters "$ckpt" \
      --merge_lora true --output_dir "$RUNS/${kind}_merged" > "$RUNS/logs/merge_$kind.log" 2>&1
  done
fi

if has eval; then
  serve "$RUNS/page_merged" 16384; trap stop EXIT
  STATES="$STATES" evaluate page_sft
  stop
  serve "$RUNS/all_merged" 40960
  $PY -m mpx run --data "$DATA/test" --method allatonce --budget "$BUDGET" --max-tokens 16384 \
    --base-url "http://127.0.0.1:$PORT/v1" --model mpx --out "$RUNS/preds/all_sft_all.jsonl"
  stop; trap - EXIT
fi

if has score; then
  log "채점"
  $PY -m mpx score --data "$DATA/test" --pred "$RUNS"/preds/*.jsonl --out "$RUNS/report" > /dev/null
  $PY -m mpx viewer --data "$DATA/test" --pred "$RUNS"/preds/*.jsonl > /dev/null
  log "→ $RUNS/report/report.md, $DATA/test/viewer/index.html"
fi
