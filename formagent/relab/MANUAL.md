# ReLab CLI 설치·설정 안내

VS Code 없이 터미널에서 ReLab 코딩 에이전트를 쓰는 방법입니다. 요청을 입력하면 ReLab이 파일을 읽고,
코드를 쓰고, 명령을 실행해 확인하며, 파일 변경이나 명령 실행처럼 물어야 할 것은 그 자리에서 묻습니다.
VS Code 확장(VSIX)을 설치할 수 없는 컴퓨터를 위해 명령줄만 따로 묶어 배포합니다.

이 문서는 0.3.46 기준입니다.

## 1. 준비물

| 항목 | 내용 |
|---|---|
| 운영체제 | Windows 10/11 x64, Linux x86_64 |
| Python | 3.10, 3.11, 3.12, 3.13 중 하나 (묶음에 이 네 버전의 wheel이 들어 있음) |
| 모델 | 사내 vLLM·Ollama 서버 주소, 또는 OpenRouter·OpenAI API 키 |
| 터미널 | Windows Terminal 권장 (색·한글·로고가 제대로 나옴). Linux는 보통의 터미널이면 됩니다 |

인터넷은 필요 없습니다. 설치에 쓰는 파일은 모두 묶음 안에 있습니다. 모델 서버나 API에는 당연히 연결되어야
합니다.

## 2. 받은 파일 확인

배포 파일은 두 개입니다.

- `relab-cli-0.3.46.zip`: 설치 묶음
- `relab-cli-0.3.46.zip.sha256`: 파일이 온전한지 확인하는 값

받은 파일이 손상되지 않았는지 확인하려면, 아래 명령의 결과가 `.sha256` 파일 안의 값과 같은지 봅니다.

```powershell
Get-FileHash .\relab-cli-0.3.46.zip -Algorithm SHA256
```

```bash
sha256sum relab-cli-0.3.46.zip
```

## 3. 설치

### Windows

1. `relab-cli-0.3.46.zip`을 마우스 오른쪽 버튼 → **압축 풀기**로 풉니다. `relab-cli-0.3.46` 폴더가 생깁니다.
2. 그 폴더에서 주소창에 `cmd`를 입력해 명령 창을 열고 실행합니다.

   ```bat
   install.cmd -AddToPath
   ```

3. `Done.`이 나오면 끝입니다. **새 터미널을 열고** 확인합니다.

   ```powershell
   relab chat --help
   ```

- 설치 위치는 `%LOCALAPPDATA%\relab-cli`입니다. 다른 곳에 두려면 `install.cmd -Into D:\tools\relab -AddToPath`처럼 지정합니다.
- `-AddToPath`는 `relab` 명령 하나만 내 PATH에 넣습니다. Python이나 pip는 넣지 않으므로 이미 쓰던 Python과 섞이지 않습니다.
- PATH에 넣지 않았다면 설치가 끝날 때 알려 주는 전체 경로(`...\relab-cli\Scripts\relab.exe`)로 실행합니다.
- `install.cmd`가 PowerShell 실행 정책을 우회해 `install.ps1`을 실행하므로, 실행 정책 설정을 바꿀 필요는 없습니다.

### Linux

```bash
unzip relab-cli-0.3.46.zip
cd relab-cli-0.3.46
sh install.sh --link
```

- `~/.local/share/relab-cli`에 설치하고 `~/.local/bin/relab` 링크를 만듭니다. `~/.local/bin`이 PATH에 없다면
  `~/.bashrc`에 `export PATH="$HOME/.local/bin:$PATH"`를 추가합니다.
- 다른 곳에 설치하려면 `sh install.sh --link /opt/relab-cli`처럼 폴더를 지정합니다.

### 새 버전으로 올리기와 지우기

- 새 버전의 묶음을 풀고 같은 명령(`install.cmd -AddToPath`, `sh install.sh --link`)을 다시 실행하면 덮어 설치합니다.
- 지울 때는 설치 폴더를 지웁니다. Windows에서 `-AddToPath`를 썼다면 사용자 환경 변수 Path에서 `...\relab-cli\bin`도 지웁니다.
- 대화 기록과 설정(`~/.relab`)은 설치 폴더와 따로 있어서, 다시 설치해도 그대로 남습니다.

## 4. 설정

### 설정 파일 위치

설정은 JSON 파일에 적습니다. 두 곳을 읽으며, 같은 항목이 있으면 프로젝트 쪽이 이깁니다.

| 파일 | 용도 |
|---|---|
| `~/.relab/config.json` (Windows: `C:\Users\<이름>\.relab\config.json`) | 내 기본 설정 |
| `<작업 폴더>/.relab/config.json` | 그 프로젝트에서만 쓸 설정 (예: 다른 모델) |

`~`는 홈 폴더입니다. 파일이 없으면 만들면 되고, 묶음 안의 `config.example.json`을 복사해 고쳐 써도 됩니다.
적은 값이 틀렸거나 모르는 항목이면 `relab chat`을 시작할 때 노란 글씨로 알려 주고 그 항목은 빼고 씁니다.

### 예시 1: 사내 vLLM 서버

```json
{
  "provider": "vllm",
  "codingModel": "Qwen/Qwen3-32B",
  "vllmEndpoint": "http://10.0.0.5:8000/v1",
  "modelContextWindows": { "Qwen/Qwen3-32B": 32768 },
  "language": "ko"
}
```

### 예시 2: 모델마다 서버가 다를 때, 막히면 큰 모델로

```json
{
  "provider": "vllm",
  "codingModel": "Qwen/Qwen3-32B",
  "vllmEndpoint": "http://10.0.0.5:8000/v1",
  "vllmModelEndpoints": {
    "Qwen/Qwen3-32B": "http://10.0.0.5:8000/v1",
    "Qwen/Qwen3.5-397B-A17B": "http://10.0.0.9:8000/v1"
  },
  "modelLadder": ["Qwen/Qwen3.5-397B-A17B"],
  "language": "ko"
}
```

`modelLadder`에 적은 모델은 작업이 막혔을 때(같은 검사가 계속 실패, 응답을 읽을 수 없음 등) 올라갈 더 큰
모델입니다. 묻기 모드에서는 올라갈지 먼저 물어봅니다.

### 예시 3: OpenRouter

```json
{
  "provider": "openrouter",
  "codingModel": "deepseek/deepseek-v4.1-flash-1017",
  "modelContextWindows": { "deepseek/deepseek-v4.1-flash-1017": 1000000 },
  "language": "ko"
}
```

### API 키

API 키는 설정 파일에 적지 않고 환경 변수로 지정합니다.

| 공급자 | 환경 변수 |
|---|---|
| OpenRouter | `OPENROUTER_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| vLLM (키를 요구하는 서버만) | `VLLM_API_KEY` |

Windows에서 계속 쓰도록 저장하려면 아래처럼 실행하고 **새 터미널을 엽니다**.

```powershell
setx OPENROUTER_API_KEY "sk-or-..."
```

Linux에서는 `~/.bashrc`에 추가합니다.

```bash
export OPENROUTER_API_KEY="sk-or-..."
```

### 설정 항목

이름은 VS Code ReLab 설정 화면과 같습니다.

| 항목 | 기본값 | 설명 |
|---|---|---|
| `provider` | `"openrouter"` | `vllm`, `ollama`, `openrouter`, `openai` 중 하나 |
| `codingProvider` | `""` | 코딩에만 다른 공급자를 쓸 때. 비우면 `provider` |
| `codingModel` | `""` | 코딩 모델 이름. **꼭 적어야 합니다** |
| `vllmEndpoint` | `""` | vLLM 서버 주소. 비우면 `http://127.0.0.1:8000/v1` |
| `vllmModelEndpoints` | `{}` | 모델별 vLLM 서버 주소 |
| `ollamaEndpoint` | `""` | Ollama 서버 주소. 비우면 `http://127.0.0.1:11434` |
| `modelLadder` | `[]` | 막혔을 때 올라갈 더 큰 모델들, 작은 것부터 (최대 5개) |
| `ladderMoveOn` | `"all"` | 올라가는 조건: `all`, `failures`(검사 실패·읽을 수 없는 응답), `checks`(검사 실패만) |
| `ladderAfterFailures` | `3` | 같은 검사가 몇 번 연속 실패하면 막힌 것으로 볼지 |
| `modelContextWindows` | `{}` | 모델별 컨텍스트 크기(토큰). 이 크기에 가까워지면 앞부분을 요약합니다 |
| `modelSampling` | `{}` | 모델별 temperature와 top_p. 예: `{"qwen3-coder": "temperature=0.6, top_p=0.95"}`. 적지 않은 모델에는 보내지 않음(0.3.38). 명령 옵션은 `--model-sampling MODEL=temperature=0.6,top_p=0.95` |
| `contextBudget` | `0` | 프롬프트를 이 토큰 수 가까이로 유지(0.3.37). 컨텍스트 크기가 1M처럼 클 때 긴 작업이 느려지지 않게 합니다. 파일 읽기와 응답은 전체 크기를 씁니다. `0`은 전체 크기, 그 밖에는 16000 이상. 명령 옵션은 `--context-budget` |
| `approvalMode` | `"ask"` | `ask`: 명령·변경·계획을 물어봄, `auto`: 묻지 않고 진행(금지된 것은 그대로 막힘) |
| `reviewEdits` | `true` | 파일을 쓰기 전에 diff를 보여 주고 물어봄 (`ask` 모드에서) |
| `planFirst` | `true` | 새 코드를 쓰기 전에 계획을 먼저 승인받음 |
| `maxModelCalls` | `0` | 한 번 실행에 쓸 모델 호출 수. `0`이면 자동: 이 컴퓨터·사설망 서버 300(승인한 계획 구현은 400), 그 밖 40. 직접 정하면 최대 500 |
| `codingRunHours` | `6` | 한 번 실행의 시간 한도(시간). 넘으면 멈추고 `/resume`으로 이어갑니다 |
| `commandMinutes` | `30` | 명령 하나가 돌 수 있는 시간(분) |
| `maxTaskCost` | `0` | 큰 모델로 올라가지 않는 비용 한도(달러, 공급자가 알려 준 값 기준). `0`은 한도 없음 |
| `modelTimeoutSeconds` | `600` | 모델 호출 하나를 기다리는 최대 시간(초) |
| `idleTimeoutSeconds` | `120` | 스트리밍 응답이 이만큼 조용하면 포기 |
| `reasoningEffort` | `"default"` | 생각하는 모델의 생각 정도: `minimal`, `low`, `medium`, `high` |
| `openrouterProviderSort` | `"default"` | OpenRouter 공급자 우선순위: `throughput`, `latency`, `price` |
| `projectOnlyReads` | `false` | 프로젝트 폴더 안에서만 읽기·검색 |
| `heldOutPaths` | `[]` | 평가용으로 숨겨 둘 경로(실행만 하고 읽지 않음) |
| `defaultRules` | `true` | ReLab 기본 규칙(문서는 `docs/`에 두기 등) 사용 |
| `privateStore` | `""` | 대화 기록 폴더. 비우면 `~/.relab`. 편집기의 "ReLab: Use Settings in Terminal"이 편집기의 기록 위치를 적어 줍니다. 0.3.40부터 `relab chat`뿐 아니라 모든 `relab` 명령(`code list`, `lessons`, `stats` 등)이 이 값을 따릅니다. `RELAB_PRIVATE_HOME`이 있으면 그쪽이 우선 |
| `language` | `"auto"` | 화면 언어: `ko`, `en`, `auto`(시스템 언어) |

`relab chat` 안에서 `/config`를 입력하면 읽은 설정 파일과 기본값과 다른 항목을 보여 줍니다.

### 터미널 안에서 바꾸기

파일을 열지 않고 `relab chat` 안에서 바로 바꿀 수도 있습니다. 저장한 값은 그 자리에서 적용되고, 파일의 다른
항목은 그대로 둡니다.

| 입력 | 하는 일 |
|---|---|
| `/config set codingModel qwen/qwen3-coder` | 내 설정(`~/.relab/config.json`)에 저장 |
| `/config set --project approvalMode auto` | 이 프로젝트 설정(`<작업 폴더>/.relab/config.json`)에 저장 |
| `/config unset codingModel` | 내 설정에서 지움 (프로젝트는 `--project`를 붙임) |

- 켜고 끄는 항목은 `on`/`off`(또는 `true`/`false`), 목록은 쉼표로 나눠 `mid, big`처럼 적습니다.
  `vllmModelEndpoints`, `modelContextWindows`처럼 짝을 적는 항목은 JSON으로 적습니다.
  예: `/config set modelContextWindows {"Qwen/Qwen3-32B": 32768}`
- 없는 이름이나 쓸 수 없는 값이면 저장하지 않고 쓸 수 있는 값을 알려 줍니다. `/config set ` 뒤에서 <kbd>Tab</kbd>을
  누르면 설정 이름이 완성됩니다.
- 같은 항목이 프로젝트 설정에 있으면 내 설정에 저장해도 프로젝트 값이 우선한다고 알려 줍니다.
- `privateStore`(기록 폴더)는 다음에 시작할 때부터 적용됩니다.

### VS Code ReLab을 함께 쓰는 경우

VS Code에 ReLab 확장이 있으면 대화창 … 메뉴의 **ReLab: Use These Settings in the Terminal (relab chat)**을
누르면 됩니다. 지금 설정과 대화 기록 폴더가 `~/.relab/config.json`에 저장되어, 터미널에서 한 대화가 VS Code
대화 목록에도 나오고 반대도 마찬가지입니다. API 키는 저장하지 않으니 환경 변수로 따로 지정합니다.

## 5. 쓰기

### 시작

작업할 프로젝트 폴더로 가서 실행합니다.

```powershell
cd C:\work\my-project
relab chat
```

먼저 터미널 화면을 `clear`처럼 지웁니다(지운 내용은 위로 스크롤하면 보입니다). 그다음 RELAB 로고 아래에
모델, 공급자, 승인 방식, 작업 폴더가 나오고 입력 상자가 뜹니다. 요청을 입력하고 Enter를 누르면 됩니다. 이어서 입력하면 같은 대화로 이어집니다.

### 입력 상자

| 키 | 하는 일 |
|---|---|
| Enter | 보내기 |
| Esc 다음 Enter | 줄 바꾸기 (붙여넣은 여러 줄은 그대로 한 메시지) |
| `/` | 명령 목록이 뜨고 Tab으로 고름 |
| 위·아래 화살표 | 지난 입력 다시 쓰기 |
| Ctrl+C | 작업 중이면 멈춤. 입력 중에 두 번 누르면 끝내기 |
| Ctrl+D (Windows: Ctrl+Z 후 Enter) | 끝내기 |

### 화면 읽기

- `●` 모델이 하는 말입니다.
- `⎿` 그 아래 실제로 한 일입니다: 읽은 파일, 바꾼 파일, 실행한 명령과 결과(`✓ 0 · 1.2s`).
- 일하는 동안 맨 아래 스피너가 지금 하는 일과 경과 시간을, 보고서를 쓰는 중이면 그 끝부분을 보여 줍니다.
- 끝나면 보고서나 요약, 그리고 판정 줄이 나옵니다. 예: `✓ 완료 · 지정 검사 통과   호출 6회 · 41s · 18k/1M`.
  판정은 모델의 말이 아니라 ReLab이 실제로 돌린 검사에서 나온 것입니다.

### 물어볼 때

| 무엇을 | 답 |
|---|---|
| 파일 변경 (diff 상자) | `y` 적용, `a` 이후 모두 적용, `n` 거절 |
| 명령 실행 | `y` 실행, `n` 거절, `A` 같은 모양의 명령은 앞으로 항상 허용 |
| 계획 | `y` 승인하고 구현, 바꿀 점을 입력하면 그대로 전달 |
| 질문 | 선택지 번호, 또는 직접 쓴 답 |

`y` 대신 `네`도 됩니다. 다른 말을 입력하면 그 말을 대신 전합니다. Enter만 누르면 답을 미루고, 다음에 입력하는
말이 답이 됩니다.

### 명령

| 명령 | 하는 일 |
|---|---|
| `/new` | 새 대화 |
| `/list`, `/open <번호>` | 이 폴더의 대화 목록, 대화 열기 |
| `/resume [모델]` | 멈추거나 호출 한도가 끝난 작업 이어서 하기 (모델을 주면 그 모델로) |
| `/undo` | 마지막 작업이 쓴 파일 되돌리기 (그 뒤에 직접 고친 파일은 건드리지 않음) |
| `/image <경로>`, `/image clear` | 다음 요청에 이미지 첨부, 첨부 취소 (아래 "이미지 첨부") |
| `/model [이름]` | 이 대화의 코딩 모델 보기·바꾸기 |
| `/auto on`, `/auto off` | 묻지 않고 승인 켜기·끄기 |
| `/config` | 설정 파일과 적용 중인 값 |
| `/config set [--project] <이름> <값>`, `/config unset [--project] <이름>` | 설정 저장·지우기 (4장 "터미널 안에서 바꾸기") |
| `/help`, `/exit` | 도움말, 끝내기 |

### 이미지 첨부

화면 캡처나 오류 화면을 모델에게 보여 줄 수 있습니다(0.3.29). 이미지를 읽는 모델이어야 합니다.

- **요청에 경로 적기**: `"~/Downloads/error shot.png" 이 오류를 고쳐줘`. 작업 폴더 밖이어도 되고, 공백이 있으면
  따옴표로 감쌉니다. VS Code 터미널에 파일을 끌어다 놓으면 경로가 입력되므로 그대로 보내면 됩니다. 경로로
  시작하는 요청(`/home/me/a.png 이게 뭐야?`)은 명령이 아니라 요청으로 받습니다.
- **`/image <경로>`**: 다음 요청에 붙일 이미지를 미리 정합니다. 여러 개를 줄 수 있고, `/image clear`로 뺍니다.
  `y`·`n` 같은 선택 답에는 붙지 않고 다음 요청을 기다립니다.
- 작업 폴더 안의 이미지는 `@screens/a.png`처럼 적어도 됩니다. 밖의 이미지는 내 기록 폴더(`attachments/`)에
  복사해 보내며, 편집기에 붙여 넣은 이미지와 같은 곳입니다.
- png·jpg·gif·webp, 한 장 2MB, 요청당 4장까지입니다. 넘는 이미지는 보내기 전에 "보내지 않음"으로 알려 줍니다.
- 터미널에는 클립보드 이미지를 붙여 넣을 수 없습니다. 파일로 저장해 경로를 주세요. SSH 서버에서는 VS Code
  탐색기로 파일을 올리거나 터미널에 끌어다 놓으면 됩니다.

### 시작할 때 쓰는 옵션

| 옵션 | 하는 일 |
|---|---|
| `-p "요청"` | 요청 하나만 처리하고 끝냄. 종료 코드 0 완료, 1 미완료, 2 시작하지 못함(작업 폴더가 없음 등), 3 답을 기다림 |
| `-c` | 이 폴더의 가장 최근 대화를 열어 이어감 (`-p`가 3으로 끝났을 때 등) |
| `--model`, `--provider`, `--endpoint` | 설정 파일 대신 이번에만 쓸 모델·공급자·서버 |
| `--auto` | 이번에는 묻지 않고 승인 |
| `--no-clear` | 시작할 때 터미널 화면을 지우지 않음 (`-p`는 원래 지우지 않음) |
| `--workspace <폴더>` | 현재 폴더 대신 이 폴더에서 작업. 없는 폴더면 만들지 물어봄(`-p`에서는 묻지 않고 멈춤) |

## 6. 기록이 남는 곳

| 무엇 | 위치 |
|---|---|
| 대화 기록 | `~/.relab/workspaces/<폴더별 이름>/` (`privateStore`나 `RELAB_PRIVATE_HOME`으로 바꿀 수 있음) |
| 입력 기록 | `~/.relab/chat_history` |
| 설정 | `~/.relab/config.json`, `<작업 폴더>/.relab/config.json` |

작업 폴더 안에는 프로젝트 설정(`.relab/config.json`)과 규칙 파일(`.relab/RELAB.md`)처럼 사람이 쓴 것만 남고,
기록은 남지 않습니다.

## 7. 문제 해결

| 증상 | 해결 |
|---|---|
| `Python 3.10 or newer is needed` | python.org에서 3.10~3.13을 설치하고 다시 실행. Windows에서는 설치 때 "py launcher"를 켭니다 |
| `pip could not install relab ...` | Python 3.14 이상이면 묶음에 맞는 wheel이 없습니다. 3.13 이하로 설치 |
| `relab`을 찾을 수 없음 | 새 터미널을 열었는지 확인. `-AddToPath` 없이 설치했다면 전체 경로로 실행 |
| `작업 폴더가 없습니다` | `--workspace`로 준 폴더가 없는 경우입니다. 대화형이면 `y`로 만들고 시작하고, `-p`라면 안내된 `mkdir` 명령으로 먼저 만듭니다 |
| 코딩 모델이 없다고 나옴 | `~/.relab/config.json`에 `codingModel`을 적거나 `/model <이름>` |
| 모델 서버에 연결되지 않음 | `vllmEndpoint` 주소와 끝의 `/v1` 확인. 다른 컴퓨터의 서버도 설정에 적은 주소면 연결합니다 |
| "the model could not be reached: ValueError: model request exceeds 1 MiB", 또는 "the request ... is past the 1 MiB" | 대화가 요청 하나에 담을 수 있는 크기(1 MiB)를 넘었습니다. 0.3.34부터는 그 전에 오래된 결과를 줄이지만, 그래도 넘으면 새 대화에서 이어 가세요(바뀐 파일은 그대로 있습니다). 컨텍스트 창을 아주 크게(예: 1000000) 적어도 요청 하나는 1 MiB까지입니다 |
| "the arguments of the write_file call were not a JSON object (Unterminated string ...)"가 반복되며 멈춤 | 컨텍스트가 거의 찬 상태에서 큰 파일을 한 번에 쓰다 응답이 잘린 것입니다. 0.3.40까지는 이것을 형식 오류로 보고 같은 시도를 반복했습니다. 0.3.41부터는 출력 한도로 보고 "큰 파일은 나눠서 쓰라"고 알립니다. 자주 나면 컨텍스트 예산(`contextBudget`, 예: 64000)을 정해 응답할 공간을 넉넉히 두세요 |
| "Model response exceeds 4 MiB" | 0.3.34까지는 생각을 길게 하는 모델의 응답이 약 2만 토큰에서 끊기고, 같은 요청을 두 번 더 보냈습니다. 0.3.35부터는 요청한 길이(32,768 토큰)까지 받고, 그래도 넘으면 모델에게 "응답이 길었다"고 알려 다시 묻습니다 |
| `relab code ...`에서 "is on another machine ... add --allow-endpoint" | `relab chat`과 달리 `relab code`(bench, prompt-compare 등)는 설정의 주소를 쓰지 않습니다. 오류에 나온 대로 `--endpoint <주소>`와 같은 주소를 `--allow-endpoint <주소>`로 한 번 더 줍니다(`/v1`은 있어도 없어도 같은 서버). 도커 컨테이너 안에서는 `127.0.0.1`이 컨테이너 자신이므로 호스트의 실제 주소를 씁니다 |
| 401, 인증 오류 | API 키 환경 변수 이름과 값 확인. `setx` 뒤에는 새 터미널 |
| 색·로고가 깨지거나 한글 폭이 어긋남 | Windows Terminal에서 실행. 오래된 콘솔은 로고 대신 글자만 나옵니다. 색을 끄려면 `NO_COLOR=1` |
| `the model does not take images` | 이미지를 받지 않는 모델(텍스트 전용)에 이미지를 보낸 것입니다. 이미지를 읽는 모델로 바꾸거나(`/model`), 이미지 내용을 글로 적어 다시 요청하세요. 이때 도구 호출 방식은 꺼지지 않습니다(0.3.29) |
| `the model's replies were not steps 3 times` | 모델이 형식에 맞지 않는 답을 세 번 보낸 것입니다. `/resume`으로 이어가거나 `modelLadder`의 더 큰 모델로 `/resume <모델>`. 0.3.9에서 빈 값(null)을 보내던 경우를 고쳤습니다 |
| 작업이 끝나지 않고 멈춘 것 같음 | 스피너의 경과 시간을 확인. Ctrl+C로 멈추고 `/resume` |

문제를 알릴 때는 끝에 나오는 `loop-...` id와 화면을 함께 보내 주세요.

## 8. 배포하는 사람용: 묶음 만들기

저장소에서 VSIX를 만들면 같은 wheel로 CLI 묶음을 만들 수 있습니다.

```bash
cd apps/vscode && npm run package
```

```bash
.venv/Scripts/python scripts/cli_bundle.py --out artifacts/fast-path-v3
```

`relab-cli-<버전>.zip`과 `.sha256`이 생깁니다. 묶음에는 relab과 의존 wheel(Windows·Linux, Python
3.10~3.13), 설치 스크립트, 이 안내서(`MANUAL.md`), 설정 예시가 들어 있습니다.
