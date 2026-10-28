#!/bin/sh
# 인터넷 되는 PC 에서 내부망 반입용 파일 두 개를 만든다 (docker/README.md 1절).
#   sh docker/build.sh 1.2
#     docgen-image-1.2.tar.gz  실행 환경 (파이썬·글꼴·Chromium·studio 패키지·SSH). 코드가 바뀌어도 다시 만들 필요 없음
#     docgen-code-1.2.tar.gz   이 저장소의 마지막 커밋 (docgen/ 생성기·서식·채점, train/ 학습 실행, studio/). 견본 이미지 docgen/samples/,
#                              서식 원본 중 안 쓰는 exe·xls·doc 는 뺀다
set -e
ver=${1:-latest}
cd "$(dirname "$0")/.."
if ! git diff --quiet HEAD -- . ':(exclude)*.tar.gz'; then
    echo "[build] 경고: 커밋하지 않은 변경은 코드 묶음에 들어가지 않습니다 (git archive HEAD)"
fi
docker build --platform linux/amd64 -f docker/Dockerfile -t "docgen:$ver" .
git archive --format=tar.gz --prefix=document_gen/ -o "docgen-code-$ver.tar.gz" HEAD -- . \
    ':(exclude)docgen/samples' ':(exclude,glob)docgen/forms/**/*.exe' ':(exclude,glob)docgen/forms/**/*.xls' \
    ':(exclude,glob)docgen/forms/**/*.doc'
# 이미지 + 코드로 테스트 (네트워크 끊고)
tmp=$(mktemp -d)
tar -xzf "docgen-code-$ver.tar.gz" -C "$tmp"
src=$tmp/document_gen
# 윈도우 Git Bash: 경로를 C:/… 로 넘기고 docker 인자의 경로 자동 변환을 끈다 (-v a:b 가 깨짐)
if pwd -W >/dev/null 2>&1; then src=$(cd "$src" && pwd -W); export MSYS_NO_PATHCONV=1; fi
docker run --rm --network none --shm-size=1g -u docgen -w /home/docgen/document_gen \
    -v "$src:/home/docgen/document_gen" --entrypoint python "docgen:$ver" \
    -B -m pytest -q -x -p no:cacheprovider docgen/tests studio/tests
rm -rf "$tmp"
docker save "docgen:$ver" | gzip > "docgen-image-$ver.tar.gz"
ls -lh "docgen-image-$ver.tar.gz" "docgen-code-$ver.tar.gz"
