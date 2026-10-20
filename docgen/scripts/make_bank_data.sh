#!/bin/bash
# 은행 업무 학습 데이터 + 평가 세트를 만든다 (docgen 컨테이너 안에서 실행).
#
#   bash docgen/scripts/make_bank_data.sh                 기본값으로 만들기 (백그라운드, SSH 끊어도 계속)
#   bash docgen/scripts/make_bank_data.sh --fg            이 터미널에서 실행
#   TRAIN_BUNDLES=300 BENCH_BUNDLES=60 bash docgen/scripts/make_bank_data.sh    양 바꾸기
#   OUT=/out/try TYPES=resident_id_card,loan_application SCENARIOS=mortgage TRAIN_BUNDLES=2 BENCH_BUNDLES=1 \
#       bash docgen/scripts/make_bank_data.sh --fg                                 몇 분짜리 시험
#
# 만드는 것 (OUT 아래):
#   bench/        평가 세트  : 서류 476종 x 1건 + 업무 12종 x 고객 BENCH_BUNDLES 명
#   bank_train/   학습 데이터: 서류 476종 x TRAIN_PER_DOC 건 + 업무 12종 x 고객 TRAIN_BUNDLES 명 (--split train)
#   logs/         단계별 로그
# 이미 다 만든 폴더(meta.json 있음)는 건너뛰고, 중간에 멈춘 폴더는 다시 만든다.
set -euo pipefail

OUT=${OUT:-/out}
TRAIN_PER_DOC=${TRAIN_PER_DOC:-5}
TRAIN_BUNDLES=${TRAIN_BUNDLES:-200}
BENCH_BUNDLES=${BENCH_BUNDLES:-40}
TYPES=${TYPES:-all}
SCENARIOS=${SCENARIOS:-all}
WORKERS=${WORKERS:-$(( $(nproc) < 8 ? $(nproc) : 8 ))}
CODE=$(cd "$(dirname "$0")/../.." && pwd)   # 저장소 최상위
LOG=$OUT/logs/make_bank_data.log

if [ "${1:-}" != "--fg" ] && [ -z "${MAKE_BANK_DATA_CHILD:-}" ]; then
    mkdir -p "$OUT/logs"
    MAKE_BANK_DATA_CHILD=1 nohup setsid bash "$0" --fg > "$LOG" 2>&1 < /dev/null &
    echo "백그라운드로 시작했습니다 (PID $!). SSH 를 끊어도 계속됩니다."
    echo "  진행 보기: tail -f $LOG        (Ctrl+C 는 보기만 종료)"
    echo "  완료 확인: ls $OUT/bank_train/meta.json $OUT/bench/meta.json"
    exit 0
fi

cd "$CODE"
mkdir -p "$OUT/logs"
say() { echo "[$(date '+%F %T')] $*"; }

if ! python -m docgen.bench build --help 2>/dev/null | grep -q -- '--split'; then
    say "이 docgen 코드에는 --split train 이 없습니다. docgen 코드 1.2 이상으로 바꾸세요 ($CODE)."
    exit 1
fi

# 필요한 디스크 (실측: 묶음 하나 약 6MB, 서류 한 건 약 0.7MB) + 여유 20%
need_mb=$(( (TRAIN_BUNDLES * 12 + BENCH_BUNDLES * 12) * 6 + (TRAIN_PER_DOC + 1) * 476 * 7 / 10 ))
need_mb=$(( need_mb * 12 / 10 ))
avail_mb=$(df -Pm "$OUT" | awk 'NR==2 {print $4}')
say "설정: 학습 per-doc=$TRAIN_PER_DOC bundles=$TRAIN_BUNDLES / 평가 bundles=$BENCH_BUNDLES / workers=$WORKERS"
gb() { awk -v m="$1" 'BEGIN { printf "%.1fGB", m / 1024 }'; }
say "디스크: 필요 약 $(gb "$need_mb"), 남은 공간 $(gb "$avail_mb") ($OUT)"
if [ "$avail_mb" -lt "$need_mb" ]; then
    say "디스크가 부족합니다. TRAIN_BUNDLES·TRAIN_PER_DOC 를 줄이거나 공간을 확보하세요."
    exit 1
fi

# build <이름> <인자...>: 다 만든 폴더는 건너뛰고, 멈춘 폴더는 --force 로 다시
build() {
    local name=$1; shift
    local dir=$OUT/$name
    if [ -f "$dir/meta.json" ]; then
        say "$name: 이미 있음, 건너뜀 (다시 만들려면 rm -rf $dir)"
        local ver
        ver=$(python -c "import json; print(json.load(open('$dir/meta.json')).get('version', '?'))")
        if [ "$name" = bench ] && [ "$ver" = "1.0" ]; then
            say "  주의: $name 은 1.0 세트입니다. 1.1 부터 증강 노이즈가 고정되므로 지우고 다시 만드세요."
        fi
        return
    fi
    local force=()
    [ -d "$dir" ] && force=(--force) && say "$name: 멈춘 흔적이 있어 다시 만듭니다"
    say "$name: 시작 (로그 $OUT/logs/$name.log)"
    local t0=$SECONDS
    python -m docgen.bench build --out "$dir" --types "$TYPES" --scenarios "$SCENARIOS" --workers "$WORKERS" \
        "${force[@]}" "$@" > "$OUT/logs/$name.log" 2>&1 \
        || { say "$name: 실패. 로그 끝부분:"; tail -20 "$OUT/logs/$name.log"; exit 1; }
    say "$name: 완료 ($(( (SECONDS - t0) / 60 ))분, $(du -sh "$dir" | cut -f1))"
}

start=$SECONDS
build bench --bundles "$BENCH_BUNDLES"
build bank_train --split train --per-doc "$TRAIN_PER_DOC" --bundles "$TRAIN_BUNDLES"

say "전부 완료 ($(( (SECONDS - start) / 60 ))분). 과제별 문항 수:"
python - "$OUT" <<'EOF'
import json, sys
from pathlib import Path
out = Path(sys.argv[1])
for name in ("bench", "bank_train"):
    m = json.loads((out / name / "meta.json").read_text(encoding="utf-8"))
    print(f"  {name:11s} " + ", ".join(f"{t} {n}" for t, n in m["counts"].items()))
EOF
say "GPU 서버 파이프라인 설정: data.train = [\"<서버의 $OUT>/bank_train\"], data.benchmark = \"<서버의 $OUT>/bench\""
