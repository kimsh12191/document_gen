# docgen 실행 환경 이미지 (파이썬·글꼴·Chromium·studio 패키지·SSH). 인터넷 없는 내부망에서 쓰도록 필요한 것을 모두 담는다.
# 코드(이 저장소)는 이미지에 넣지 않고 따로 반입해 /home/docgen/document_gen 에 마운트한다.
#
#   빌드(인터넷 되는 PC):  sh docker/build.sh 1.2   → 이미지 파일 + 코드 파일
#   띄우기(서버):          sh docker/studio.sh      → studio 컨테이너 (인자 studio). 인자 없이 띄우면 SSH 서버
#   자세히:                docker/README.md
ARG PW_VERSION=1.63.0

# Chromium 은 Microsoft 공식 Playwright 이미지에서 가져온다 (Playwright 다운로드 서버가 막힌 망에서도 빌드되게).
# headless 렌더링에 쓰는 chromium_headless_shell 만 남긴다 (ffmpeg 는 동영상 녹화용이라 뺌).
FROM mcr.microsoft.com/playwright/python:v${PW_VERSION}-noble AS browsers
RUN rm -rf /ms-playwright/firefox-* /ms-playwright/webkit-* /ms-playwright/chromium-[0-9]* /ms-playwright/ffmpeg-*

FROM ubuntu:24.04
ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright \
    PYTHONPATH=/home/docgen/document_gen \
    PATH=/opt/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# 파이썬, 글꼴, Chromium(headless) 실행 라이브러리, SSH 서버, 터미널 도구.
# playwright install-deps 는 쓰지 않는다: 가상 화면(Xvfb), 일본어·태국어 글꼴 등 렌더링에 안 쓰는 것까지 깔린다.
# 글꼴은 지우지 않는다: install-deps 환경과 같은 이미지가 나오는지 픽셀 비교로 확인했다.
#   fonts-wqy-zenhei 는 서식의 기본(sans-serif·serif) 글꼴로 잡혀 숫자·영문 모양을 정하고,
#   fonts-freefont-ttf 는 체크 표시(✔ ☑ ☒)를 그리고, 나눔 글꼴 변형(Light 등)도 일부 서식이 쓴다.
#   하나라도 빠지면 글자 모양·줄바꿈이 달라지거나 체크 표시가 빈칸이 된다.
# libgbm1 이 끌고 오는 Mesa GPU 드라이버(LLVM, ~180MB)는 지운다: Chromium 은 내장 SwiftShader 로 그린다.
#
# 사내 프록시가 HTTPS 를 검사하면 그 인증서를 빌드 비밀로 넘긴다:  --secret id=ca,src=회사CA.crt
# 패키지 저장소를 바꾸려면 (사내 미러 등):                     --build-arg APT_MIRROR=https://미러/ubuntu
# 둘 다 빌드 중에만 쓰고 이미지에는 남지 않는다.
ARG APT_MIRROR=
RUN --mount=type=secret,id=ca,mode=0444 \
    set -e; src=/etc/apt/sources.list.d/ubuntu.sources; cp $src /tmp/sources.bak; \
    if [ -n "$APT_MIRROR" ]; then sed -i -E "s#https?://[^ ]*(archive|security)\.ubuntu\.com/ubuntu/?#$APT_MIRROR#g" $src; fi; \
    ca=; [ -s /run/secrets/ca ] && ca="-o Acquire::https::CAInfo=/run/secrets/ca"; \
    apt-get $ca update \
 && apt-get $ca install -y --no-install-recommends \
      python3 python3-venv \
      fontconfig fonts-nanum fonts-nanum-extra fonts-nanum-coding fonts-noto-cjk fonts-liberation fonts-wqy-zenhei fonts-freefont-ttf \
      libasound2t64 libatk-bridge2.0-0t64 libatk1.0-0t64 libatspi2.0-0t64 libcairo2 libcups2t64 libdbus-1-3 \
      libdrm2 libgbm1 libglib2.0-0t64 libnspr4 libnss3 libpango-1.0-0 libx11-6 libxcb1 libxcomposite1 \
      libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2 \
      openssh-server \
      ca-certificates less nano vim-tiny procps tini \
 && mv /tmp/sources.bak $src \
 && rm -rf /usr/lib/x86_64-linux-gnu/libLLVM* /usr/lib/x86_64-linux-gnu/libgallium* /usr/lib/x86_64-linux-gnu/dri \
 && rm -rf /var/lib/apt/lists/*

# 파이썬 패키지 (판 번호는 검증한 판으로 고정). 내부망에선 받을 곳이 없어 pip 는 지운다
COPY docker/requirements.lock /tmp/requirements.lock
RUN --mount=type=secret,id=ca,mode=0444 \
    python3 -m venv /opt/venv \
 && if [ -s /run/secrets/ca ]; then export PIP_CERT=/run/secrets/ca; fi \
 && pip install -r /tmp/requirements.lock \
 && pip uninstall -y -q pip \
 && rm -rf /tmp/requirements.lock /root/.cache
COPY --from=browsers /ms-playwright /opt/ms-playwright

# 접속 계정 (호스트 폴더 권한을 맞추려면 --build-arg UID=$(id -u))
ARG UID=1000
RUN (userdel -r ubuntu 2>/dev/null || true) \
 && useradd -m -u ${UID} -s /bin/bash docgen \
 && mkdir -p /out /home/docgen/document_gen /etc/ssh/keys /run/sshd \
 && chown docgen:docgen /out /home/docgen/document_gen \
 && rm -f /etc/ssh/ssh_host_*

COPY docker/sshd_config /etc/ssh/sshd_config.d/docgen.conf
COPY docker/profile.sh /etc/profile.d/docgen.sh
COPY docker/entrypoint.sh /usr/local/bin/docgen-entrypoint
# SSH 로그인 셸에는 docker ENV 가 넘어가지 않으므로 /etc/environment 에도 적는다 (PAM 이 읽음)
RUN chmod 755 /usr/local/bin/docgen-entrypoint \
 && printf 'PATH="%s"\nLANG=C.UTF-8\nPLAYWRIGHT_BROWSERS_PATH=%s\nPYTHONPATH=%s\nPYTHONUNBUFFERED=1\n' \
      "$PATH" "$PLAYWRIGHT_BROWSERS_PATH" "$PYTHONPATH" > /etc/environment

EXPOSE 22 8765
VOLUME ["/out"]
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/docgen-entrypoint"]
