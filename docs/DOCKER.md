# Docker (내부망 반입)

인터넷 없는 내부망 Linux 서버에서 docgen·벤치마크를 돌리고, 윈도우 PC 에서 SSH 로 컨테이너에 접속해 쓰는 방법입니다.
이미지에는 실행 환경(파이썬·글꼴·Chromium·SSH)만 들어가고, 코드는 따로 반입해 마운트합니다.

## 1. 반입 파일 만들기 (인터넷 되는 PC, Linux 또는 WSL)

```bash
sh docker/build.sh 1.1
#  docgen-image-1.1.tar.gz  실행 환경 (약 390MB). 코드가 바뀌어도 다시 만들 필요 없음
#  docgen-code-1.1.tar.gz   코드·서식 (약 60MB)
```

빌드 후 네트워크를 끊은 컨테이너에서 테스트까지 돌립니다. Chromium 은 Microsoft 공식 Playwright 이미지
(`mcr.microsoft.com/playwright/python`)에서 가져오므로 Playwright 다운로드 서버가 막힌 망에서도 빌드됩니다.

## 2. 내부망 서버에 설치

```bash
docker load -i docgen-image-1.1.tar.gz
mkdir -p ~/docgen && tar -xzf docgen-code-1.1.tar.gz -C ~/docgen    # ~/docgen/document_gen
mkdir -p ~/docgen/data

docker run -d --name docgen --restart unless-stopped \
  -p 2222:22 --shm-size=1g \
  -e DOCGEN_PASSWORD='비밀번호' \
  -v ~/docgen/document_gen:/home/docgen/document_gen \
  -v ~/docgen/data:/out \
  -v docgen-ssh:/etc/ssh/keys \
  docgen:1.1
```

- `--shm-size=1g`: Chromium 이 공유 메모리가 모자라면 죽습니다.
- `docgen-ssh` 볼륨: SSH 호스트 키를 보관해, 이미지를 바꿔 컨테이너를 새로 만들어도 접속 경고가 나지 않습니다.
- 비밀번호 대신 공개키: `-e SSH_PUBLIC_KEY="$(cat id_ed25519.pub)"` 또는 `-v <파일>:/etc/docgen/authorized_keys:ro`.
  둘 다 없고 `DOCGEN_PASSWORD` 도 없으면 임의 비밀번호를 만들어 `docker logs docgen` 에 남깁니다.
- 코드 업데이트: 새 `docgen-code-*.tar.gz` 를 같은 자리에 풀고 끝 (컨테이너 재시작 불필요).

## 3. 윈도우에서 접속

윈도우 10/11 에는 OpenSSH 클라이언트가 기본으로 있습니다 (PowerShell).

```powershell
ssh -p 2222 docgen@<서버IP>
scp -P 2222 -r docgen@<서버IP>:/out/bench_out .\     # 결과 가져오기 (WinSCP 도 SFTP 로 접속 가능)
```

접속하면 코드 폴더에서 시작합니다. 결과는 `/out` (서버의 `~/docgen/data`)에 저장하세요.

```bash
python -m docgen generate --types all --n 3 --out /out/gen --png --augment 2
python -m docgen.bench build --out /out/bench
python -m docgen.bench run --bench /out/bench --pred /out/preds/m1 --base-url http://<모델서버>:8001/v1 --model <모델>
python -m docgen.bench eval --bench /out/bench --pred /out/preds/m1
```

모델 서버가 같은 서버에 있으면 `<모델서버>` 에 서버의 내부망 IP 를 쓰세요 (컨테이너 안의 `localhost` 는 컨테이너 자신입니다).

## 참고

- VS Code Remote-SSH 는 처음 접속할 때 인터넷에서 서버 프로그램을 내려받으므로 내부망에서는 따로 준비해야 합니다.
  터미널 `ssh` 와 WinSCP 는 그대로 됩니다.
- 원본 서식 배경은 처음 그릴 때 `~/.cache/docgen/bg` 에 만들어집니다 (약 165MB). 컨테이너를 새로 만들 때마다
  다시 만들어지는 게 싫으면 `-v docgen-cache:/home/docgen/.cache` 를 추가하세요.
- 이미지 안의 글꼴은 서식이 쓰는 것만 남겼습니다 (Playwright 기본 중·일 글꼴, 나눔 글꼴 변형 등 제외).
