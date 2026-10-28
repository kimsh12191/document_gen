#!/bin/sh
# 내부망 Linux 서버에서 studio 를 띄운다. 컨테이너가 없으면 만들고, 꺼져 있으면 켜고, 떠 있으면 접속 방법만 보여 준다.
# 코드는 이 스크립트가 있는 저장소를 그대로 마운트하므로, 코드를 고치거나 새 코드 묶음을 풀면 studio 가 저절로 다시 뜬다.
#
#   sh docker/studio.sh --data /database/docgen_studio   저장 폴더를 정해 띄우기 (처음 한 번)
#                                  데이터셋·작업 기록 → <저장 폴더>/workspace/, 실서류 → <저장 폴더>/real_data/
#   sh docker/studio.sh            띄우기 (정한 저장 폴더·포트 그대로. 서버를 다시 켜도 저절로 뜸)
#   sh docker/studio.sh -p 9000    포트 바꾸기 (처음엔 8765)
#   sh docker/studio.sh --open     다른 PC·컨테이너에서 http://<서버IP>:<포트> 로 바로 들어오게 (로그인 없음: 같은 망 누구나)
#   sh docker/studio.sh --local    다시 이 서버에서만 (처음 값. 다른 PC 는 SSH 터널)
#     저장 폴더·포트·주소를 바꾸면 컨테이너를 새로 만들고, 다음부터는 옵션 없이도 그대로 뜬다
#   sh docker/studio.sh logs       로그 보기 (Ctrl+C 는 보기만 종료)
#   sh docker/studio.sh shell      컨테이너 안 터미널 (python -m docgen … 도 여기서. 저장 폴더는 /out)
#   sh docker/studio.sh restart    다시 띄우기
#   sh docker/studio.sh rm         컨테이너 지우기 (이미지·코드·저장 폴더는 그대로)
#
# 바꿀 수 있는 값 (환경변수): DOCGEN_IMAGE=docgen:1.2  STUDIO_NAME=docgen-studio
set -e
img=${DOCGEN_IMAGE:-docgen:1.2}
name=${STUDIO_NAME:-docgen-studio}
port=${STUDIO_PORT:-}
code=$(cd "$(dirname "$0")/.." && pwd)
win=
# 윈도우 Git Bash: 경로를 C:/… 로 넘기고, docker 인자의 경로 자동 변환을 끈다 (-v a:b 가 깨짐)
if pwd -W >/dev/null 2>&1; then
    win=1
    code=$(cd "$code" && pwd -W)
    export MSYS_NO_PATHCONV=1
fi

cmd=up
bind=
data=
while [ $# -gt 0 ]; do
    case $1 in
    -p|--port) port=$2; shift 2 ;;
    -d|--data) data=$2; shift 2 ;;
    --open) bind=0.0.0.0; shift ;;
    --local) bind=127.0.0.1; shift ;;
    *) cmd=$1; shift ;;
    esac
done
case $port in *[!0-9]*) echo "포트는 숫자로: $port"; exit 1 ;; esac
given=$data
if [ -n "$data" ]; then   # 절대 경로로 (없으면 만든다)
    mkdir -p "$data"
    data=$(cd "$data" && if [ -n "$win" ]; then pwd -W; else pwd; fi)
fi

state=$(docker inspect -f '{{.State.Status}}' "$name" 2>/dev/null || true)
# 이미 만든 컨테이너의 포트·여는 주소·저장 폴더 (옵션을 안 주면 그대로 쓴다)
now= now_bind= now_data=
if [ -n "$state" ]; then
    now=$(docker inspect -f '{{range (index .HostConfig.PortBindings "8765/tcp")}}{{.HostPort}}{{end}}' "$name")
    now_bind=$(docker inspect -f '{{range (index .HostConfig.PortBindings "8765/tcp")}}{{.HostIp}}{{end}}' "$name")
    now_bind=${now_bind:-0.0.0.0}
    now_data=$(docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' "$name" | sed -n 's/^DOCGEN_HOST_DATA=//p')
fi

case $cmd in
logs) exec docker logs -f --tail 100 "$name" ;;
shell) exec docker exec -it -u docgen -w /home/docgen/document_gen "$name" bash -l ;;
restart) docker restart "$name" >/dev/null; port=$now; bind=$now_bind; data=$now_data ;;
rm) docker rm -f "$name" >/dev/null; echo "지움: $name"; exit 0 ;;
up)
    port=${port:-${now:-8765}}
    bind=${bind:-${now_bind:-127.0.0.1}}
    if [ -z "$data" ]; then
        data=${now_data:-${DOCGEN_DATA:-$HOME/docgen/data}}
        [ -z "$state" ] && [ -z "$DOCGEN_DATA" ] && echo "저장 폴더를 정하지 않아 $data 를 씁니다 (정하려면 --data <폴더>)"
        mkdir -p "$data" && data=$(cd "$data" && if [ -n "$win" ]; then pwd -W; else pwd; fi)
    fi
    if [ -n "$state" ] && { [ "$bind:$port" != "$now_bind:$now" ] || { [ -n "$given" ] && [ "$data" != "$now_data" ]; }; }; then
        docker rm -f "$name" >/dev/null
        echo "바뀜 ($now_bind:$now ${now_data:-?} → $bind:$port $data): 컨테이너를 새로 만듭니다"
        state=
    fi
    if [ -z "$state" ]; then
        # 기본은 127.0.0.1 로만 연다: studio 에는 로그인이 없으므로 다른 PC 는 SSH 터널로 (--open 이면 모든 주소)
        # STUDIO_DATA=/out: studio 가 데이터셋을 /out/workspace, 실서류를 /out/real_data 에 둔다 (studio/config.py)
        docker run -d --name "$name" --restart unless-stopped \
            -p "$bind:$port:8765" --shm-size=1g \
            -e DOCGEN_UID="$(id -u)" -e DOCGEN_GID="$(id -g)" \
            -e STUDIO_DATA=/out -e DOCGEN_HOST_CODE="$code" -e DOCGEN_HOST_DATA="$data" \
            -v "$code:/home/docgen/document_gen" \
            -v "$data:/out" \
            -v docgen-cache:/home/docgen/.cache \
            "$img" studio >/dev/null
        echo "만듦: $name ($img, $bind:$port)"
    elif [ "$state" != running ]; then
        docker start "$name" >/dev/null
    fi
    ;;
*) sed -n '2,16p' "$0"; exit 1 ;;
esac

# 뜰 때까지 기다린다 (처음엔 몇 초)
i=0
command -v curl >/dev/null || sleep 5
until ! command -v curl >/dev/null || curl -fs "http://127.0.0.1:$port/" >/dev/null; do
    i=$((i + 1))
    if [ $i -gt 60 ] || [ "$(docker inspect -f '{{.State.Running}}' "$name")" != true ]; then
        echo "studio 가 뜨지 않았습니다. 로그:"; docker logs --tail 30 "$name"; exit 1
    fi
    sleep 1
done
ip=$(hostname -I 2>/dev/null | awk '{print $1}')
echo "studio 떠 있음 → 이 서버에서 http://localhost:$port"
ws=$(curl -fs "http://127.0.0.1:$port/api/paths" 2>/dev/null | sed -n 's/.*"datasets_host": *"\([^"]*\)".*/\1/p')
echo "저장 폴더: ${data:-?}  (컨테이너 안 /out)"
[ -n "$ws" ] && echo "  데이터셋 → $ws/<이름>/"
if [ "$bind" = 0.0.0.0 ]; then
    echo "다른 PC·컨테이너에서: http://${ip:-<서버IP>}:$port  (로그인 없음. 그만 열려면 sh docker/studio.sh --local)"
else
    echo "윈도우 PC에서 (PowerShell, 켜 둔 동안 브라우저로 http://localhost:$port):"
    echo "  ssh -N -L $port:localhost:$port $(id -un)@${ip:-<서버IP>}"
fi
