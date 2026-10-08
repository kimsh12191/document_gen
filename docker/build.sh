#!/bin/sh
# 인터넷 되는 PC 에서 내부망 반입용 파일 두 개를 만든다.
#   sh docker/build.sh 1.1
#     docgen-image-1.1.tar.gz  실행 환경 (파이썬·글꼴·Chromium·SSH). 코드가 바뀌어도 다시 만들 필요 없음
#     docgen-code-1.1.tar.gz   이 저장소 코드·서식 (견본 이미지 samples/, 서식 원본 중 안 쓰는 exe·xls·doc 제외)
set -e
ver=${1:-latest}
cd "$(dirname "$0")/.."
docker build --platform linux/amd64 -t "docgen:$ver" .
git archive --format=tar.gz --prefix=document_gen/ -o "docgen-code-$ver.tar.gz" HEAD -- . \
    ':(exclude)samples' ':(exclude,glob)add_template/**/*.exe' ':(exclude,glob)add_template/**/*.xls' \
    ':(exclude,glob)add_template/**/*.doc'
# 이미지 + 코드로 테스트 (네트워크 끊고)
tmp=$(mktemp -d)
tar -xzf "docgen-code-$ver.tar.gz" -C "$tmp"
docker run --rm --network none --shm-size=1g -u docgen -w /home/docgen/document_gen \
    -v "$tmp/document_gen:/home/docgen/document_gen" --entrypoint python "docgen:$ver" \
    -B -m pytest -q -x -p no:cacheprovider tests
rm -rf "$tmp"
docker save "docgen:$ver" | gzip > "docgen-image-$ver.tar.gz"
ls -lh "docgen-image-$ver.tar.gz" "docgen-code-$ver.tar.gz"
