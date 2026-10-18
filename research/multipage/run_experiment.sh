#!/usr/bin/env bash
# 여러 쪽 문서 추출 연구 한 바퀴 (내부망 GPU 서버). research/multipage 에서 실행.
#
#   START_MODEL=/models/bank_sft_merged GPUS=0,1 ./run_experiment.sh                 # 전부
#   START_MODEL=... ./run_experiment.sh gen sft                                       # 단계만
#   START_MODEL=... N_TRAIN=20 N_TEST=10 MAX_STEPS=5 ./run_experiment.sh              # 리허설
#
# 단계: gen sft zeroshot train merge eval score  (기본: 전부. 이미 끝난 결과는 이어서/건너뜀)
#   gen      생성 묶음 (학습 N_TRAIN, 평가 N_TEST)
#   sft      학습 데이터 (data/train/swift_page, data/train/swift_all)
#   zeroshot 출발 모델 그대로: 한 번에 넣기 + 쪽 단위(상태 none/doc/tail/context). 프롬프트만으로 상태를 주는 기준선
#   train    쪽 단위+상태 모델, 한 번에 넣기 모델을 같은 묶음으로 각각 학습 (training/train.py)
#   merge    LoRA 병합 (swift export)
#   eval     학습한 두 모델로 같은 평가
#   score    채점 → runs/report/report.md
set -euo pipefail
cd "$(dirname "$0")"

START_MODEL=${START_MODEL:?START_MODEL 에 출발 모델(2부 은행 업무 모델, 병합된 폴더)을 주세요}
DATA=${DATA:-data}
RUNS=${RUNS:-runs}
GPUS=${GPUS:-0,1}
N_TRAIN=${N_TRAIN:-2000}
N_TEST=${N_TEST:-200}
WORKERS=${WORKERS:-16}
BUDGET=${BUDGET:-12000}
PORT=${PORT:-8100}
MAX_STEPS=${MAX_STEPS:-}
STATES=${STATES:-"none doc tail context"}
PY=${PY:-python}
STAGES=${*:-gen sft zeroshot train merge eval score}

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
  log "생성: 학습 $N_TRAIN, 평가 $N_TEST 묶음"
  $PY -m mpx gen --out "$DATA/train" --n "$N_TRAIN" --split train --workers "$WORKERS"
  $PY -m mpx gen --out "$DATA/test" --n "$N_TEST" --split test --workers "$WORKERS"
  $PY -m mpx stats --data "$DATA/test" > "$RUNS/test_stats.json"
fi

if has sft; then
  log "학습 데이터"
  $PY -m mpx sft --data "$DATA/train" --budget "$BUDGET" | tee "$RUNS/sft_stats.json"
fi

if has zeroshot; then
  serve "$START_MODEL" 40960; trap stop EXIT
  evaluate zeroshot
  stop; trap - EXIT
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
  log "→ $RUNS/report/report.md"
fi
