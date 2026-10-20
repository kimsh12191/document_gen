# Docker (내부망 반입)

인터넷 없는 내부망 Linux 서버에서 docgen·벤치마크를 돌리고, 윈도우 PC 에서 SSH 로 컨테이너에 접속해 쓰는 방법입니다.
이미지에는 실행 환경(파이썬·글꼴·Chromium·SSH)만 들어가고, 코드는 따로 반입해 마운트합니다.

## 1. 반입 파일 만들기 (인터넷 되는 PC, Linux 또는 WSL)

```bash
sh docker/build.sh 1.1
#  docgen-image-1.1.tar.gz  실행 환경 (약 390MB). 코드가 바뀌어도 다시 만들 필요 없음
#  docgen-code-1.1.tar.gz   코드·서식 (약 60MB)
```

사내 프록시가 HTTPS 를 검사하는 망이면 `docker build` 에 `--secret id=ca,src=회사CA.crt` 를, 사내 Ubuntu 미러를 쓰려면
`--build-arg APT_MIRROR=https://미러/ubuntu` 를 붙이세요 (둘 다 빌드 중에만 쓰이고 이미지에는 남지 않습니다).
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

은행 업무 학습(SFT → GRPO → 벤치마크 비교)에 쓸 학습 데이터·평가 세트를 만드는 방법은 [training/BANK_TASKS.md](../training/BANK_TASKS.md)의 1단계에 있습니다. SSH 없이 서버에서 `docker exec`로 바로 만들 수도 있습니다.

## 4. studio 띄우기 (같은 컨테이너)

studio(서식·데이터셋 관리 웹 화면, [studio/README.md](../studio/README.md))도 이 컨테이너에서 띄웁니다. Chromium·글꼴이 이미 있어 미리보기가 실제 생성 데이터와 같은 이미지로 나옵니다. **이미지를 새로 반입하지 않아도 됩니다.** 학습 컨테이너는 따로 두고, 폴더만 공유합니다.

```
[윈도우 PC 브라우저] ──SSH 터널 (2222)──▶ [docgen 컨테이너: studio + Chromium + 글꼴]
                                              │ 공유 폴더 (/out = 서버의 ~/docgen/data …)
[학습 컨테이너: training/] ◀── 같은 데이터·결과 폴더 ──┘
```

**① 처음 한 번: studio 패키지 설치.** 1.1 이미지에는 fastapi·uvicorn이 없습니다. 코드 묶음에 Linux용 설치 파일(`studio/wheels/`, 약 3.4MB)이 들어 있으므로 컨테이너 안에서 설치만 합니다(인터넷 불필요).

```bash
ssh -p 2222 docgen@<서버IP>
python -m studio.deps install          # → ~/document_gen/studio_deps/ (코드 폴더 안이라 컨테이너를 새로 만들어도 남음)
```

새 코드 묶음을 풀어도 `studio_deps/`는 그대로 남습니다. `studio/requirements.txt`가 바뀐 코드를 받았을 때만 다시 설치합니다. 다음에 이미지를 새로 만들면 studio 패키지가 이미지에 들어가므로(`docker/requirements.lock`) 이 단계가 필요 없습니다.

**② 설정** — 코드 폴더의 `studio/config.json` (예시: [studio/config.example.json](../studio/config.example.json)). 데이터셋과 검수 결과는 공유 폴더에 둡니다.

```json
{
  "workspace_dir": "/out/studio_workspace",
  "real_data_dir": "/out/real",
  "path_map": {"/out": "<학습 컨테이너에서 같은 폴더가 보이는 경로>"}
}
```

`path_map`: 두 컨테이너가 같은 폴더를 다른 경로로 볼 때, studio가 학습 설정을 내보내며 경로를 바꿔 씁니다.

**③ 띄우기** (컨테이너 안). SSH를 끊어도 계속 돕니다.

```bash
mkdir -p /out/logs
setsid nohup python -m studio > /out/logs/studio.log 2>&1 < /dev/null &
tail -f /out/logs/studio.log          # "docgen studio → http://localhost:8765" 가 보이면 됨 (Ctrl+C 는 보기만 종료)
```

끄기: `pkill -f "python -m studio"`. 컨테이너가 다시 시작되면 studio도 꺼지므로 ③을 다시 합니다.

**④ 윈도우에서 접속** — SSH 터널. 이 창을 켜 둔 동안 브라우저에서 `http://localhost:8765`로 들어갑니다.

```powershell
ssh -p 2222 -N -L 8765:localhost:8765 docgen@<서버IP>
```

- 터널은 지금 열려 있는 SSH 포트(2222)만 쓰므로 컨테이너를 다시 만들 필요가 없습니다.
- studio에는 로그인이 없습니다. 포트를 바로 열어(`docker run … -p 8765:8765`, `python -m studio --host 0.0.0.0`) 쓰면 같은 망의 누구나 들어올 수 있으니 터널을 권합니다.

## 참고

- VS Code Remote-SSH 는 처음 접속할 때 인터넷에서 서버 프로그램을 내려받으므로 내부망에서는 따로 준비해야 합니다.
  터미널 `ssh` 와 WinSCP 는 그대로 됩니다.
- 원본 서식 배경은 처음 그릴 때 `~/.cache/docgen/bg` 에 만들어집니다 (약 165MB). 컨테이너를 새로 만들 때마다
  다시 만들어지는 게 싫으면 `-v docgen-cache:/home/docgen/.cache` 를 추가하세요.
- 글꼴은 Playwright 기본 환경(`playwright install --with-deps`)과 같은 이미지가 나오도록 맞췄습니다 (픽셀 비교로 확인).
