#!/bin/sh
# 내부망 Linux 서버에서 studio 를 띄운다. 컨테이너가 없으면 만들고, 꺼져 있으면 켜고, 떠 있으면 접속 방법만 보여 준다.
# 코드는 이 스크립트가 있는 저장소를 그대로 마운트하므로, 코드를 고치거나 새 코드 묶음을 풀면 studio 가 저절로 다시 뜬다.
#
#   sh docker/studio.sh            띄우기 (서버를 다시 켜도 저절로 뜸). 처음엔 포트 8765
#   sh docker/studio.sh -p 9000    포트를 바꿔 띄우기 (떠 있던 컨테이너는 새 포트로 다시 만든다. 다음부터는 -p 없이도 9000)
#   sh docker/studio.sh logs       로그 보기 (Ctrl+C 는 보기만 종료)
#   sh docker/studio.sh shell      컨테이너 안 터미널 (python -m docgen … 도 여기서)
#   sh docker/studio.sh restart    다시 띄우기 (설정 studio/config.json 을 바꿨을 때)
#   sh docker/studio.sh rm         컨테이너 지우기 (이미지·코드·데이터는 그대로). 이미지를 바꿀 때 지우고 다시 띄운다
#
# 바꿀 수 있는 값 (환경변수): DOCGEN_IMAGE=docgen:1.2  DOCGEN_DATA=~/docgen/data  STUDIO_PORT=8765  STUDIO_NAME=docgen-studio
set -e
img=${DOCGEN_IMAGE:-docgen:1.2}
name=${STUDIO_NAME:-docgen-studio}
port=${STUDIO_PORT:-}
data=${DOCGEN_DATA:-$HOME/docgen/data}
code=$(cd "$(dirname "$0")/.." && pwd)
# 윈도우 Git Bash: 경로를 C:/… 로 넘기고, docker 인자의 경로 자동 변환을 끈다 (-v a:b 가 깨짐)
if pwd -W >/dev/null 2>&1; then
    code=$(cd "$code" && pwd -W)
    mkdir -p "$data" && data=$(cd "$data" && pwd -W)
    export MSYS_NO_PATHCONV=1
fi

cmd=up
while [ $# -gt 0 ]; do
    case $1 in
    -p|--port) port=$2; shift 2 ;;
    *) cmd=$1; shift ;;
    esac
done
case $port in *[!0-9]*) echo "포트는 숫자로: $port"; exit 1 ;; esac

state=$(docker inspect -f '{{.State.Status}}' "$name" 2>/dev/null || true)
# 이미 만든 컨테이너의 포트 (포트를 안 정했으면 그대로 쓴다)
now=
[ -n "$state" ] && now=$(docker inspect -f '{{range (index .HostConfig.PortBindings "8765/tcp")}}{{.HostPort}}{{end}}' "$name")

case $cmd in
logs) exec docker logs -f --tail 100 "$name" ;;
shell) exec docker exec -it -u docgen -w /home/docgen/document_gen "$name" bash -l ;;
restart) docker restart "$name" >/dev/null; port=${now:-8765} ;;
rm) docker rm -f "$name" >/dev/null; echo "지움: $name"; exit 0 ;;
up)
    if [ -n "$state" ] && [ -n "$port" ] && [ "$port" != "$now" ]; then
        docker rm -f "$name" >/dev/null
        echo "포트 $now → $port: 컨테이너를 새로 만듭니다"
        state=
    fi
    port=${port:-${now:-8765}}
    if [ -z "$state" ]; then
        mkdir -p "$data"
        # 127.0.0.1 로만 연다: studio 에는 로그인이 없으므로 다른 PC 는 SSH 터널로만 들어오게
        docker run -d --name "$name" --restart unless-stopped \
            -p "127.0.0.1:$port:8765" --shm-size=1g \
            -e DOCGEN_UID="$(id -u)" -e DOCGEN_GID="$(id -g)" \
            -v "$code:/home/docgen/document_gen" \
            -v "$data:/out" \
            -v docgen-cache:/home/docgen/.cache \
            "$img" studio >/dev/null
        echo "만듦: $name ($img, 포트 $port, 코드 $code, 결과 $data → /out)"
    elif [ "$state" != running ]; then
        docker start "$name" >/dev/null
    fi
    ;;
*) sed -n '2,13p' "$0"; exit 1 ;;
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
echo "윈도우 PC에서 (PowerShell, 켜 둔 동안 브라우저로 http://localhost:$port):"
echo "  ssh -N -L $port:localhost:$port $(id -un)@${ip:-<서버IP>}"
