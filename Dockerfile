# docgen 실행 환경 이미지 (파이썬·글꼴·Chromium·SSH). 인터넷 없는 내부망에서 쓰도록 필요한 것을 모두 담는다.
# 코드(이 저장소)는 이미지에 넣지 않고 따로 반입해 /home/docgen/document_gen 에 마운트한다.
#
#   빌드(인터넷 되는 PC):  sh docker/build.sh 1.1   → 이미지 파일 + 코드 파일
#   실행·접속 방법:        docs/DOCKER.md
ARG PW_VERSION=1.63.0

# Chromium 은 Microsoft 공식 Playwright 이미지에서 가져온다 (Playwright 다운로드 서버가 막힌 망에서도 빌드되게).
# headless 렌더링에 쓰는 chromium_headless_shell 만 남긴다.
FROM mcr.microsoft.com/playwright/python:v${PW_VERSION}-noble AS browsers
RUN rm -rf /ms-playwright/firefox-* /ms-playwright/webkit-* /ms-playwright/chromium-[0-9]*

FROM ubuntu:24.04
ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright \
    PYTHONPATH=/home/docgen/document_gen \
    PATH=/opt/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# 파이썬, 글꼴, Chromium(headless) 실행 라이브러리, SSH 서버, 터미널 도구.
# playwright install-deps 는 쓰지 않는다: 중·일 글꼴, 가상 화면(Xvfb) 등 렌더링에 안 쓰는 것까지 깔린다.
# 나눔 글꼴은 서식이 쓰는 것만 남긴다 (Barunpen·옛한글·Eco·NanumSquare·Light 류는 안 씀).
# libgbm1 이 끌고 오는 Mesa GPU 드라이버(LLVM, ~180MB)는 지운다: Chromium 은 내장 SwiftShader 로 그린다.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      python3 python3-venv \
      fontconfig fonts-nanum fonts-nanum-extra fonts-nanum-coding fonts-noto-cjk fonts-liberation \
      libasound2t64 libatk-bridge2.0-0t64 libatk1.0-0t64 libatspi2.0-0t64 libcairo2 libcups2t64 libdbus-1-3 \
      libdrm2 libgbm1 libglib2.0-0t64 libnspr4 libnss3 libpango-1.0-0 libx11-6 libxcb1 libxcomposite1 \
      libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2 \
      openssh-server \
      ca-certificates less nano vim-tiny procps tini \
 && cd /usr/share/fonts/truetype/nanum \
 && rm -f NanumBarunpen* *YetHangul* *Eco* NanumSquare_* NanumSquare[A-Z]* NanumPen.ttf NanumBrush.ttf *Light*.ttf \
 && fc-cache -f \
 && rm -rf /usr/lib/x86_64-linux-gnu/libLLVM* /usr/lib/x86_64-linux-gnu/libgallium* /usr/lib/x86_64-linux-gnu/dri \
 && rm -rf /var/lib/apt/lists/*

# 파이썬 패키지 (판 번호는 검증한 판으로 고정)
COPY docker/requirements.lock /tmp/requirements.lock
RUN python3 -m venv /opt/venv \
 && pip install -r /tmp/requirements.lock \
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

EXPOSE 22
VOLUME ["/out"]
ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/docgen-entrypoint"]
