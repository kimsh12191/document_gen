# OCR Viewer: 모델의 OCR 결과를 눈으로 확인

학습한 모델에 이미지를 보여 주고 질문한 뒤, 답으로 받은 위치를 이미지 위에 박스로 그려 주는 웹 화면입니다.
추가 설치는 필요 없습니다. PDF를 열 때만 `pypdfium2` 또는 `PyMuPDF`가 필요합니다.

viewer는 두 가지입니다. 이 문서는 1부 **OCR viewer**(아래 1~5)입니다. 2부 **은행 업무 viewer**는 [bank/viewer/README.md](../../bank/viewer/README.md)에 있습니다([6번](#6-은행-업무-viewer)).

| viewer | 띄우기 | 화면 | 보는 것 |
|---|---|---|---|
| **OCR viewer** | `ocr/`에서 `bash viewer/start.sh` | `http://localhost:7860` | 글자와 위치(박스). OCR 단계 모델 — 아래 1~5 |
| **은행 업무 viewer** | `bank/`에서 `bash viewer/bank_start.sh` | `http://localhost:7861` | 은행 업무 벤치마크 답 비교, 서류 올려서 물어보기 — [bank/viewer/README.md](../../bank/viewer/README.md) |

| 파일 | 역할 |
|---|---|
| `start.sh` | 모델 서버와 화면을 한 번에 띄웁니다. Ctrl+C를 누르면 둘 다 꺼집니다. |
| `ocr_viewer.py` | 화면을 띄우는 프로그램입니다. 모델 서버에 질문을 보내고 답의 좌표를 정리합니다. 은행 업무 viewer도 이 파일의 PDF 그리기를 같이 씁니다. |
| `index.html` | 화면 자체입니다. `ocr_viewer.py`가 이 파일을 보여 줍니다. 고친 뒤 새로고침하면 바로 반영됩니다. |
| `model-server.log` | `start.sh`가 띄운 모델 서버의 로그입니다. 실행하면 생깁니다. |

## 1. 띄우기

`ocr/` 폴더(OCR 브랜치를 따로 반입했다면 `bank-ocr-pipeline` 폴더)에서 vLLM이 설치된 환경으로 실행합니다.

```bash
# 원래 모델(Base)을 GPU 0에
bash viewer/start.sh

# 학습한 모델: run_pipeline이 병합해 둔 폴더를 넘깁니다. 두 번째 값은 GPU 번호입니다.
ls runs/exp1/merged/
bash viewer/start.sh runs/exp1/merged/sft-<버전>-checkpoint-<번호> 1
```

`Waiting for the model to load....` 다음에 `ready`가 나오고, 이어서 `OCR viewer on http://127.0.0.1:7860`이 보이면 준비된 것입니다.
모델을 불러오는 데 1~3분 걸립니다.

- GPU가 비어 있어야 합니다. run_pipeline이 학습이나 평가 중이면 GPU가 차 있어서 모델이 뜨지 않습니다. 그럴 때는 아래 3번(저장된 답 보기)을 쓰세요.
- vLLM이 다른 가상환경에 있다면 `SWIFT=/경로/vllm-venv/bin/swift bash viewer/start.sh`처럼 실행합니다.
- 포트를 바꾸려면 `MODEL_PORT=8020 VIEW_PORT=7870 bash viewer/start.sh`처럼 실행합니다. 기본값은 모델 8010, 화면 7860입니다.
- 모델이 이미 8010에 떠 있으면 새로 띄우지 않고 그 모델을 씁니다.

## 2. 브라우저로 열기

화면은 서버 안에서 돌기 때문에 포트를 내 PC로 연결해야 합니다.

- **VS Code:** 아래쪽 패널의 **PORTS** 탭을 열고 `Forward a Port`에 `7860`을 입력한 뒤, PC 브라우저에서 `http://localhost:7860`을 엽니다.
- **MobaXterm:** `Tunneling`(MobaSSHTunnel)에서 Local port forwarding을 추가합니다. 내 PC의 7860을 서버의 `127.0.0.1:7860`으로 연결한 뒤 `http://localhost:7860`을 엽니다.

### 서버 IP로 바로 열기

기본값 `127.0.0.1`은 "이 서버 자신만" 접속할 수 있다는 뜻이라, 다른 PC에서 IP로 들어올 수 없습니다(그래서 위의 포트 연결이 필요합니다).
IP로 바로 열려면 화면을 `0.0.0.0`으로 띄웁니다.

```bash
VIEW_HOST=0.0.0.0 bash viewer/start.sh
# 브라우저: http://<서버 IP>:7860   (서버 IP는 hostname -I 로 확인)
```

- 도커 컨테이너 안이라면 컨테이너를 만들 때 7860 포트를 열어 두었거나(`-p 7860:7860`) `--network host`로 띄운 경우에만 밖에서 보입니다. 안 열리면 위의 VS Code 포트 연결을 쓰세요.
- 이렇게 열면 같은 망의 누구나 화면에 들어와 모델에 질문하고, 서버 경로 칸으로 서버에 있는 이미지·PDF를 볼 수 있습니다. 필요할 때만 켜고 끝나면 Ctrl+C로 닫으세요.
- 모델 서버(8010)는 계속 `127.0.0.1`에만 열립니다. 화면이 서버 안에서 모델에 대신 질문하므로 모델 포트를 열 필요는 없습니다.

## 3. 화면 사용법

### 자유 테스트: 새 이미지나 PDF로 물어보기

1. **파일 업로드**에서 PNG·JPG·TIF·PDF를 고릅니다. 서버에 있는 파일이면 **서버의 파일 경로** 칸에 경로를 넣어도 됩니다.
   PDF나 여러 장짜리 TIF는 **페이지** 번호로 몇 쪽을 볼지 고릅니다.
2. **질문**을 고르고 **실행**을 누릅니다.

| 질문 | 하는 일 | 학습한 과제 |
|---|---|---|
| 전체 글자 + 위치 | 페이지를 타일로 나눠 모든 글자를 박스와 함께 읽습니다. 기본 3x2이고, 답이 잘린다는 경고가 뜨면 더 잘게 나눕니다. | spotting |
| 글자 찾기 | 입력한 글자가 있는 곳을 모두 찾습니다. | grounding |
| 드래그한 영역 읽기 | 그림 위에서 마우스로 영역을 끌어 정하면 그 안의 글자를 읽습니다. | region_ocr |
| 기준 글자 옆 찾기 | 입력한 글자의 오른쪽·왼쪽·위·아래 글자를 찾습니다. | relation |
| 직접 입력 질문 | 원하는 질문을 그대로 보냅니다. 예시 질문을 골라 고쳐 써도 됩니다. | (학습 범위 밖) |

**직접 입력 질문으로 위치 받기**

- 예시 질문 목록에서 `위치 요청: 계좌번호`, `금액`, `날짜`, `이름`, `도장·서명`, `표 제목 행` 등을 고르면, 답을 `[{"bbox_2d": [x1, y1, x2, y2], "label": "..."}]` 형식으로 달라는 질문이 채워집니다.
- 답에 `bbox_2d`나 `[x1, y1, x2, y2]` 모양의 좌표가 들어 있으면, 형식이 조금 달라도 찾아서 빨간 박스로 그립니다. 오른쪽 **찾은 위치** 표에 마우스를 올리면 해당 박스가 굵게 표시됩니다.
- 질문에 `{box}`를 넣으면 드래그한 영역의 좌표로 바뀝니다. 예: `bbox_2d={box} 영역 안의 글자를 모두 찾아 ...`. 이 경우 먼저 다른 질문으로 한 번 실행해 그림을 띄운 뒤 드래그합니다.
- **답의 좌표 기준**은 기본값이 0~1000(Qwen3.5 방식)입니다. 박스가 엉뚱하게 작거나 한쪽에 몰려 그려지면 `픽셀`로 바꿔 보세요.
- 계좌번호·금액 같은 정보 찾기는 이번 학습 범위(글자와 위치, 노이즈)가 아닙니다. 이 답은 원래 Qwen 모델의 능력이고, 학습 효과는 위 네 가지 질문으로 보는 것이 정확합니다.

**참고**

- 이미지는 학습 때와 똑같이 2300×1600 안으로 줄여서 보냅니다. 휴대폰 사진의 회전 정보도 반영합니다.
- PDF는 200 DPI로 그림으로 바꾼 뒤 같은 크기로 줄입니다. DPI를 바꾸려면 `ocr_viewer.py --pdf-dpi`를 씁니다.

### 벤치마크 문제: 정답과 비교

`start.sh`는 `data/prepared-v2/benchmark_tasks.jsonl`이 있으면 이 칸을 자동으로 켭니다.
**무작위 문제**를 누르면 벤치마크 문제 하나를 모델에게 풀게 하고 다음을 보여 줍니다.

- 초록 박스와 글자: 정답(내부 OCR 기준)
- 빨간 박스와 글자: 모델 답
- 파란 박스: 질문에 들어 있던 영역
- GRPO 보상 점수: 0~1, 1이 정답과 같음

과제(grounding, spotting 등)와 화면(clean 원본 / aug 노이즈)으로 거를 수 있습니다.

## 4. GPU 없이 이미 받은 평가 답 보기

run_pipeline 평가가 끝나면 `runs/exp1/predictions/`에 모델 답이 저장됩니다. 모델 서버 없이 이 답을 정답과 비교해 볼 수 있어서, 학습 중에도 쓸 수 있습니다.

```bash
ls runs/exp1/predictions/
python viewer/ocr_viewer.py --tasks data/prepared-v2/benchmark_tasks.jsonl \
    --predictions runs/exp1/predictions/base.jsonl
```

이 모드에서는 **보상 이하만** 칸에 `0.5`처럼 넣어 틀린 문제만 골라 볼 수 있습니다. 모델이 없으므로 자유 테스트는 꺼집니다.

## 5. 문제가 생기면

| 증상 | 확인 |
|---|---|
| `Model server exited` | `viewer/model-server.log` 마지막 줄을 확인합니다. GPU가 다른 작업에 쓰이고 있는지 `nvidia-smi`로 보거나, `GPU_MEMORY=0.7`로 낮춰 봅니다. |
| 화면이 안 열림 | 포트 연결(2번)을 확인합니다. 화면 포트를 바꿨다면 연결한 포트도 같은지 봅니다. |
| `PDF needs pypdfium2` | `pip install pypdfium2`로 설치하거나, PDF를 PNG로 바꿔 올립니다. |
| ⚠ 답이 길이 제한에서 잘림 | 전체 글자 질문이면 타일을 3x3, 4x3으로 더 잘게 나눕니다. |
| 박스 위치가 이상함 | 직접 입력 질문이면 **답의 좌표 기준**을 바꿔 봅니다. |

## 6. 은행 업무 viewer

2부 은행 업무 viewer(벤치마크 답 비교, **직접 테스트**)의 설명은 [bank/viewer/README.md](../../bank/viewer/README.md)로 옮겼습니다. `bank/` 폴더에서 `bash viewer/bank_start.sh`로 띄우고, 화면은 `http://localhost:7861`입니다. 브라우저 연결은 위 2번과 같습니다.

