#!/bin/sh
# 컨테이너 시작: SSH 호스트 키·접속 계정 준비 후 sshd 실행
set -e

# 호스트 키: /etc/ssh/keys 를 볼륨으로 두면 컨테이너를 새로 만들어도 같은 키를 쓴다 (접속 경고 없음)
for t in ed25519 rsa; do
    f=/etc/ssh/keys/ssh_host_${t}_key
    [ -f "$f" ] || ssh-keygen -q -t "$t" -N '' -f "$f"
done

# 공개키 로그인: SSH_PUBLIC_KEY 환경변수 또는 /etc/docgen/authorized_keys 파일(마운트)
ak=/home/docgen/.ssh/authorized_keys
mkdir -p /home/docgen/.ssh
: > "$ak"
[ -n "$SSH_PUBLIC_KEY" ] && printf '%s\n' "$SSH_PUBLIC_KEY" >> "$ak"
[ -f /etc/docgen/authorized_keys ] && cat /etc/docgen/authorized_keys >> "$ak"
chown -R docgen:docgen /home/docgen/.ssh
chmod 700 /home/docgen/.ssh
chmod 600 "$ak"

# 비밀번호 로그인: DOCGEN_PASSWORD. 공개키도 비밀번호도 없으면 임의 비밀번호를 만들어 로그에 남긴다
if [ -n "$DOCGEN_PASSWORD" ]; then
    echo "docgen:$DOCGEN_PASSWORD" | chpasswd
elif [ ! -s "$ak" ]; then
    pw=$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 16)
    echo "docgen:$pw" | chpasswd
    echo "[docgen] 비밀번호가 지정되지 않아 임의로 만들었습니다: $pw  (DOCGEN_PASSWORD 로 지정 가능)"
else
    usermod -p "*" docgen   # 비밀번호 로그인 막기 (잠금 "!" 은 공개키 로그인도 막을 수 있어 "*" 사용)
    sed -i 's/^PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config.d/docgen.conf
fi

# 결과 폴더: 호스트에서 root 로 만든 폴더를 마운트했으면 docgen 계정이 쓸 수 있게
if ! su docgen -s /bin/sh -c 'test -w /out'; then
    chown docgen:docgen /out
fi

# 코드: 따로 반입한 저장소를 /home/docgen/document_gen 에 마운트해야 한다
code=/home/docgen/document_gen
if [ ! -d "$code/docgen" ]; then
    echo "[docgen] 경고: $code 에 코드가 없습니다. docgen-code-*.tar.gz 를 풀어 -v <폴더>:$code 로 마운트하세요."
elif ! su docgen -s /bin/sh -c "test -w $code"; then
    echo "[docgen] 코드 폴더를 docgen 계정이 고칠 수 있게 소유자를 바꿉니다 (uid $(id -u docgen))"
    chown -R docgen:docgen "$code"
fi

echo "[docgen] SSH 대기 중 (컨테이너 22번 포트). 계정: docgen"
exec /usr/sbin/sshd -D -e
