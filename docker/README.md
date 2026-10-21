# docgen 도커 이미지 (내부망 반입)

인터넷 없는 내부망 Linux 서버에서 studio(서식·데이터셋 관리 웹 화면)와 docgen(합성 서류·벤치마크 생성기)을 돌리는 방법입니다.
윈도우 PC 에서 Linux 서버로 SSH 접속하고, 서버에서 컨테이너 하나(`docgen-studio`)를 띄워 씁니다.
GPU 학습(`train/`, `python -m train`)은 이 컨테이너가 아니라 따로 있는 학습 컨테이너에서 하고, 결과 폴더만 공유합니다.

```
[윈도우 PC 브라우저] ──SSH 터널──▶ [내부망 Linux 서버 127.0.0.1:8765]
                                          │
                     [docgen-studio 컨테이너: studio + Chromium + 글꼴 + 파이썬]
                       코드 = 서버의 ~/docgen/document_gen (마운트, 고치면 studio 가 저절로 다시 뜸)
                       /out = 저장 폴더 (--data 로 정함, 예: /database/docgen_studio) ──▶ 학습 컨테이너와 공유
```

이미지에는 실행 환경만 들어가고, 코드(이 저장소)는 따로 반입해 컨테이너에 마운트합니다.
그래서 코드가 바뀌면 코드 묶음만 다시 반입하면 되고, 이미지는 다시 만들 필요가 없습니다.

| 파일 | 역할 |
|---|---|
| `docker/studio.sh` | **서버에서 직접 쓰는 것.** studio 컨테이너 만들기·켜기, 포트·여는 주소, 로그, 셸, 지우기 |
| `docker/remote_build.py`, `docker/REMOTE_BUILD.md` | 다른 컨테이너·PC 에서 studio 에 데이터 생성을 맡기기, 그 매뉴얼 |
| `docker/build.sh` | 인터넷 되는 PC 에서 반입 파일 두 개 만들기 (이미지 빌드 + 코드 묶음 + 네트워크를 끊은 테스트) |
| `docker/Dockerfile` | 이미지: 파이썬·글꼴·Chromium·studio 패키지·SSH 서버 |
| `docker/requirements.lock` | 이미지에 넣는 파이썬 패키지 (판 고정) |
| `docker/entrypoint.sh` | 컨테이너 시작. `studio` 인자면 studio, 없으면 SSH 서버([6절](#6-선택-컨테이너에-ssh-로-바로-들어가기)) |
| `docker/sshd_config`, `docker/profile.sh` | SSH 서버 설정, 로그인하면 환경변수를 잡고 코드 폴더로 이동 |

## 1. 반입 파일 만들기 (인터넷 되는 PC)

저장소 최상위에서 (Linux·WSL, 또는 Docker Desktop 이 있는 윈도우의 Git Bash). 코드 묶음은 git 의 마지막 커밋으로 만드니 먼저 커밋합니다.

```bash
sh docker/build.sh 1.2
#  docgen-image-1.2.tar.gz  실행 환경 (약 410MB). 코드가 바뀌어도 다시 만들 필요 없음
#  docgen-code-1.2.tar.gz   코드 (이 저장소 전체: docgen/·train/·studio/ …, 약 80MB). 견본 이미지 docgen/samples/ 는 뺌
```

`1.2` 는 붙일 버전 이름입니다. 빌드 뒤 네트워크를 끊은 컨테이너에서 테스트까지 돌립니다 (약 15분).

- 사내 프록시가 HTTPS 를 검사하는 망이면 `build.sh` 의 `docker build` 줄에 `--secret id=ca,src=회사CA.crt` 를,
  사내 Ubuntu 미러를 쓰려면 `--build-arg APT_MIRROR=https://미러/ubuntu` 를 붙이세요 (둘 다 빌드 중에만 쓰이고 이미지에는 남지 않습니다).
- Chromium 은 Microsoft 공식 Playwright 이미지(`mcr.microsoft.com/playwright/python`)에서 가져오므로 Playwright 다운로드 서버가 막힌 망에서도 빌드됩니다.
- 이미지 크기는 대부분 렌더링에 꼭 필요한 것입니다: Chromium 260MB, Playwright 의 Node 120MB, 한글·CJK 글꼴 240MB (압축 전).

## 2. 내부망 서버: 처음 한 번

```bash
docker load -i docgen-image-1.2.tar.gz
mkdir -p ~/docgen && tar -xzf docgen-code-1.2.tar.gz -C ~/docgen    # → ~/docgen/document_gen
```

설정 파일은 필요 없습니다. 저장 폴더는 다음 절에서 `--data` 로 정합니다.

## 3. studio 띄우기

Linux 서버에서 (컨테이너 밖):

```bash
cd ~/docgen/document_gen
sh docker/studio.sh --data /database/docgen_studio    # 처음 한 번: 저장 폴더를 정해 띄우기
sh docker/studio.sh                                   # 그다음부터: 정한 저장 폴더·포트 그대로
```

저장 폴더 안은 studio 가 알아서 나눠 씁니다.

```
/database/docgen_studio/          (컨테이너 안에서는 /out)
  workspace/datasets/<이름>/      만든 데이터셋 (⑥ 새로 만들기, remote_build.py)
  workspace/registry.json, jobs/  ⑥ 데이터셋 목록, ⑧ 작업 기록
  real_data/                      실서류 검수 결과
```

윈도우 PC 에서 (PowerShell). 이 창을 켜 둔 동안 브라우저에서 `http://localhost:8765` 로 들어갑니다. `studio.sh` 가 끝에 맞는 명령을 보여 줍니다.

```powershell
ssh -N -L 8765:localhost:8765 <서버 계정>@<서버IP>
```

| 명령 | 하는 일 |
|---|---|
| `sh docker/studio.sh --data <폴더>` | 저장 폴더 정하기·바꾸기 (컨테이너를 새로 만듦. 폴더 내용은 그대로) |
| `sh docker/studio.sh` | 띄우기 (정한 값 그대로) |
| `sh docker/studio.sh -p <포트>` | 포트 바꾸기 (기본 8765) |
| `sh docker/studio.sh --open` | 다른 PC·컨테이너에서 `http://<서버IP>:<포트>` 로 바로 접속 (아래 주의) |
| `sh docker/studio.sh --local` | 다시 이 서버에서만 (기본) |
| `sh docker/studio.sh logs` | 로그 보기 (Ctrl+C 는 보기만 종료) |
| `sh docker/studio.sh shell` | 컨테이너 안 터미널 ([5절](#5-명령줄로-데이터-만들기)) |
| `sh docker/studio.sh restart` | 다시 띄우기 |
| `sh docker/studio.sh rm` | 컨테이너 지우기 (이미지·코드·데이터는 그대로). 새 이미지를 반입했으면 지우고 다시 띄움 |

- 컨테이너는 `--restart unless-stopped` 라 서버를 다시 켜도 studio 가 저절로 뜹니다.
- 기본은 서버의 `127.0.0.1` 에만 엽니다. 서버에 원격 데스크톱으로 들어가 있다면 서버의 브라우저에서 바로 `http://localhost:8765`.
- **`--open`:** 터널 없이 `http://<서버IP>:<포트>` 로 화면과 API 를 씁니다 (다른 컨테이너에서 생성 맡기기도 이것). studio 에는 로그인이 없어 **같은 망에서 그 주소를 아는 누구나** 서식·레시피를 고치고 생성을 돌릴 수 있습니다. 실서류를 다루는 동안에는 `--local` 로 두세요.
- 저장 폴더·포트·주소는 한 번 정하면 컨테이너에 남아, 다음부터는 옵션 없이 `sh docker/studio.sh` 만 해도 그대로 뜹니다. `--data` 를 안 주고 처음 띄우면 `~/docgen/data` 를 씁니다.
- 컨테이너 안 계정 번호를 서버 사용자와 맞춰 띄우므로, studio 가 만든 파일도 서버 사용자 것입니다.
- studio 화면·로그에 나오는 경로는 컨테이너 안 경로입니다: `/out` = 저장 폴더, `/home/docgen/document_gen` = 코드 폴더. `studio.sh` 가 끝에 데이터셋이 생기는 서버 경로를 보여 주고, 다른 곳에서는 `python remote_build.py paths` 로 봅니다.
- 다른 이미지·컨테이너 이름: 환경변수 `DOCGEN_IMAGE=docgen:1.2`, `STUDIO_NAME=docgen-studio`.
- 학습 컨테이너가 저장 폴더를 `/out` 이 아닌 다른 경로로 연결했다면, studio 가 내보내는 학습 설정의 경로를 바꿔 쓰도록 코드 폴더에 `studio/config.json` 을 둡니다: `{"path_map": {"/out": "<학습 컨테이너에서 보이는 경로>"}}` (그 밖의 설정은 필요 없음).
- 원본 서식 배경 캐시(약 165MB)는 `docgen-cache` 볼륨에 남아, 컨테이너를 다시 만들어도 새로 그리지 않습니다.

## 4. 코드 업데이트

새 `docgen-code-*.tar.gz` 를 같은 자리에 풀면 끝입니다. 컨테이너·이미지는 그대로 둡니다.

```bash
tar -xzf docgen-code-1.3.tar.gz -C ~/docgen
```

- `studio/`·`docgen/` 의 `.py` 가 바뀌면 studio 가 몇 초 안에 다시 뜹니다. 화면 파일(`studio/static`)은 브라우저 새로고침만 하면 됩니다. 서버에서 파일을 직접 고쳐도 같습니다.
- 다시 뜰 때 돌고 있던 ⑧ 작업은 "끊김"으로 표시됩니다 (생성은 끝까지 돌고, 끝난 데이터셋은 ⑥ 목록에서 자동 등록이 복구됨). 긴 빌드 중에는 코드 반입을 미루세요.
- 풀어도 지워진 파일은 남습니다. 2026-10-20 재배치·2026-10-21 학습 통합(`ocr/`·`bank/` → `train/`) 전 코드에서 넘어왔다면 옛 폴더(`scripts/`, `templates/`, `training/`, `ocr/`, `bank/` …)가 남지만 쓰이지 않습니다. `training/` 아래 git 에 없는 데이터·결과를 옮기는 방법은 [저장소 README](../README.md#예전-구조에서-옮겨-올-때)에 있습니다.
- 이미지는 `docker/Dockerfile`·`docker/requirements.lock`·`studio/requirements.txt` 가 바뀌었을 때만 새로 반입합니다. 반입 뒤 `sh docker/studio.sh rm` → `DOCGEN_IMAGE=docgen:<새 버전> sh docker/studio.sh`.

## 5. 명령줄로 데이터 만들기

같은 컨테이너에서 합니다. `sh docker/studio.sh shell` 로 들어가면 코드 폴더에서 시작하고, 결과는 `/out` (저장 폴더)에 둡니다.

```bash
python -m docgen generate --types all --n 3 --out /out/gen --png --augment 2
python -m docgen.bench build --out /out/bench
python -m docgen.bench run --bench /out/bench --pred /out/preds/m1 --base-url http://<모델서버>:8001/v1 --model <모델>
python -m docgen.bench eval --bench /out/bench --pred /out/preds/m1
```

모델 서버가 같은 서버에 있으면 `<모델서버>` 에 서버의 내부망 IP 를 쓰세요 (컨테이너 안의 `localhost` 는 컨테이너 자신입니다).

### 다른 컨테이너에서 생성 맡기기 (HTTP)

studio 를 `--open` 으로 띄워 두면, 다른 컨테이너(학습 컨테이너 등)나 PC 에서 [`docker/remote_build.py`](remote_build.py) 로 생성을 맡기고 끝날 때까지 기다릴 수 있습니다. 포트는 studio 포트 하나로 됩니다.
**무엇을 넣으면 무엇이 나오는지, studio 화면의 어디와 대응하는지는 [REMOTE_BUILD.md](REMOTE_BUILD.md) 에 있습니다.**

```bash
export STUDIO_URL=http://<서버IP>:8765
python remote_build.py build --name bench-1021 --recipe bank-bench                     # 평가 세트 통째
python remote_build.py build --name id-5 --types resident_id_card,hf169 --per-doc 5     # 특정 서식만
python remote_build.py build --name loan-20 --scenarios mortgage --bundles 20           # 특정 업무만
```

### 은행 업무 데이터 만들기

학습(`python -m train`)에 쓸 평가 세트(`/out/bench`)와 학습 데이터(`/out/bank_train`)를 한 번 만들어 둡니다 (8코어 약 1시간 15분, 약 19GB).

```bash
bash docgen/scripts/make_bank_data.sh          # 백그라운드로 시작. 셸을 나가도 계속
tail -f /out/logs/make_bank_data.log           # "전부 완료" 가 나오면 끝
```

양·출력 위치(`OUT`, `TRAIN_BUNDLES`, `BENCH_BUNDLES` …)는 `docgen/scripts/make_bank_data.sh` 맨 위 주석에 있습니다. 컨테이너의 `/out` 은 저장 폴더이므로, 학습 설정(`data.train`·`data.benchmark`)에는 서버 경로(예: `/database/docgen_studio/bench`)를 씁니다 ([guide/tutorial.md](../guide/tutorial.md) 4절).

결과 파일을 윈도우로 가져오기: `scp -r <서버 계정>@<서버IP>:docgen/data/bench_out .\` (WinSCP 도 SFTP 로 접속 가능).

## 6. (선택) 컨테이너에 SSH 로 바로 들어가기

서버 계정 없이 컨테이너에 직접 SSH 로 들어가야 할 때만 씁니다. 같은 이미지를 인자 없이 띄우면 SSH 서버가 뜹니다.

```bash
docker run -d --name docgen --restart unless-stopped \
  -p 2222:22 --shm-size=1g \
  -e DOCGEN_PASSWORD='비밀번호' \
  -v ~/docgen/document_gen:/home/docgen/document_gen \
  -v ~/docgen/data:/out \
  -v docgen-ssh:/etc/ssh/keys \
  -v docgen-cache:/home/docgen/.cache \
  docgen:1.2
```

```powershell
ssh -p 2222 docgen@<서버IP>
```

- `--shm-size=1g`: Chromium 이 공유 메모리가 모자라면 죽습니다.
- `docgen-ssh` 볼륨: SSH 호스트 키를 보관해, 이미지를 바꿔 컨테이너를 새로 만들어도 접속 경고가 나지 않습니다.
- 비밀번호 대신 공개키: `-e SSH_PUBLIC_KEY="$(cat id_ed25519.pub)"` 또는 `-v <파일>:/etc/docgen/authorized_keys:ro`.
  둘 다 없고 `DOCGEN_PASSWORD` 도 없으면 임의 비밀번호를 만들어 `docker logs docgen` 에 남깁니다.
- studio 패키지가 없는 1.1 이미지만 있을 때는 이 컨테이너 안에서 `python -m studio.deps install`(코드 묶음의 `studio/wheels/` 에서 설치) 후
  `python -m studio --reload` 로 띄우고, 윈도우에서 `ssh -p 2222 -N -L 8765:localhost:8765 docgen@<서버IP>` 로 접속합니다.

## 참고

- VS Code Remote-SSH 는 처음 접속할 때 인터넷에서 서버 프로그램을 내려받으므로 내부망에서는 따로 준비해야 합니다.
  터미널 `ssh` 와 WinSCP 는 그대로 됩니다.
- 글꼴은 Playwright 기본 환경(`playwright install --with-deps`)과 같은 이미지가 나오도록 맞췄습니다 (픽셀 비교로 확인).
  글꼴을 빼면 글자 모양·줄바꿈이 달라지거나 체크 표시가 빈칸이 됩니다.
- 윈도우 PC 에서도 `sh docker/studio.sh` 가 됩니다 (Docker Desktop + Git Bash). 이 PC 에서 바로 `http://localhost:8765`.
