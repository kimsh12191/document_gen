# 연구: 은행 서류 VLM 추론 속도

> **목표:** 1부 OCR benchmark와 2부 은행 업무 benchmark에서 **점수는 그대로 두고**, 같은 GPU로 더 많이, 더 빨리 처리한다.

브랜치 `claude/vision-token-efficiency`

## 1. 지금 추론에서 시간이 드는 곳

| 항목 | 1부 OCR (`bank_ocr`) | 2부 은행 업무 (`bank_task`, `docgen.bench`) |
|---|---|---|
| 입력 | 페이지 1장 ≈ 3,600 비전 토큰. **한 페이지에 질문 여러 개** | 문항당 이미지 최대 13장, 합 12,000 토큰 이하 |
| 답 길이 | 짧은 글자(`crop_ocr`, `bbox_ocr`, `region_ocr`, `marked_ocr`), 박스 JSON 1~수 개(`grounding`, `relation`, `marked_box`), **박스 JSON 최대 40개(`spotting`)** | 짧은 답(`classify`, `review`, `ocr_field`), JSON(`kie`, `marks`, `cross_check`, `doc_check`), **페이지 받아쓰기(`ocr_page`, 최대 4096)** |
| 서버 | `swift deploy` + vLLM, 서버당 동시 64 | 같음, 서버당 동시 32, `max_model_len 20480` |

- **답이 짧은 과제는 입력 처리(비전 인코더 + prefill)가 대부분**입니다. 입력 토큰을 줄이거나 캐시가 맞아야 빨라집니다.
- **`spotting`, `ocr_page`, `kie`는 답 생성(decode)이 대부분**입니다. 박스 하나(`{"bbox_2d": [x1, y1, x2, y2], "label": "…"}`)가 대략 20토큰이라 `spotting` 40개면 800토큰 안팎입니다. 답을 빨리 만들어야 빨라집니다.
- GPU는 A100입니다. FP8 연산이 없어서 FP8 양자화로는 계산이 빨라지지 않습니다.

### 모델 구조 때문에 먼저 확인할 것 (Qwen3.5-9B)

Qwen3.5-9B는 선형 어텐션(Gated DeltaNet) 3층마다 일반 어텐션 1층을 두는 혼합 구조이고, 다음 토큰을 미리 맞히는 **MTP 머리가 들어 있습니다** ([모델 카드](https://huggingface.co/Qwen/Qwen3.5-9B), [요약](https://apxml.com/models/qwen35-9b)).

1. **프리픽스 캐시가 실제로 맞는지 모릅니다.** 지금 코드는 이미지를 질문 앞에 두고 같은 이미지 질문을 몰아 보내 캐시 재사용을 기대합니다(`bank_ocr/inference.py`). 하지만 vLLM에서 혼합 구조 모델의 프리픽스 캐시는 `mamba_cache_mode align`(블록 경계에서만 이어 쓰기) 방식이고 아직 실험 기능입니다. 공유 구간이 블록 경계에 못 미치면 적중률이 0%로 떨어지는 문제가 보고됐습니다 ([vLLM 문서](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching.html), [#40696](https://github.com/vllm-project/vllm/issues/40696), [#45238](https://github.com/vllm-project/vllm/issues/45238)). 이후 부분 적중을 지원하는 변경([#46384](https://github.com/vllm-project/vllm/pull/46384))이 들어갔지만 **내부망 vLLM 버전에서 직접 재야 합니다.**
2. **MTP 머리로 바로 추측 디코딩을 할 수 있습니다.** 따로 작은 모델이 필요 없습니다. vLLM에서 `{"method": "qwen3_next_mtp", "num_speculative_tokens": 2}` 같은 설정으로 씁니다 ([사례](https://github.com/gpustack/gpustack/issues/4688), [vLLM 포럼](https://discuss.vllm.ai/t/qwen3-5-27b-fp8-speculative-decoding/2447)). 다만 우리 모델은 SFT·GRPO로 바뀌었고 MTP 머리는 원래 모델 그대로라 적중률이 떨어졌을 수 있습니다.

## 2. 관련 연구

### 답 생성 빠르게 (decode)

| 연구 | 내용 | 우리에게 |
|---|---|---|
| MTP 추측 디코딩 (Qwen3.5 내장) | 모델에 붙은 MTP 머리가 다음 몇 토큰을 미리 내고 본 모델이 한 번에 확인. 한 사용자 측정 기준 적중 73%, 토큰당 20.4 → 13.7ms(1.49배) ([사례](https://friendli.ai/models/pottokao/Ornith-1.0-35B-Heretic-NVFP4-MTP)) | **1순위.** temperature 0이면 답이 바뀌지 않음(무손실) |
| [Vision Is Not Overhead (GLANCE)](https://arxiv.org/pdf/2609.00355) (2026) | VLM용 무손실 추측 디코딩. 본 모델의 융합된 표현을 읽어 여러 토큰을 한 번에 초안. **grounding·OCR 출력은 일반 글보다 잘 맞힌다**고 보고, grounding 과제 평균 1.80배(저자 보고) | 우리 출력(박스 JSON, 받아쓰기)이 추측 디코딩에 유리하다는 근거 |
| [FOVEA](https://arxiv.org/pdf/2608.22883) (2026) | 초안 모델이 필요한 이미지 근거만 꺼내 쓰고 KV 캐시는 건드리지 않음. 평균 1.6~1.7배(저자 보고) | 캐시와 함께 쓰는 설계 참고 |
| [ViSpec](https://arxiv.org/pdf/2509.15235), [SpecVLM](https://arxiv.org/pdf/2509.11815) (2025) | VLM 전용 초안 모델. 이미지 정보를 초안 모델에 압축해 넣음. 2.5~2.9배(저자 보고) | MTP 적중이 낮을 때의 대안 |
| [LocateAnything](https://research.nvidia.com/labs/lpr/locate-anything/) (2026), [GroundAnything](https://arxiv.org/html/2609.39600) (2026) | 좌표 4개를 한 토큰씩이 아니라 **박스 하나를 한 번에** 냄. 최대 2.5배, 4.5배(저자 보고) | 박스가 많은 `spotting`에 맞지만 대규모 재학습 필요. 참고만 |

### 입력 줄이기 (인코더 + prefill)

같은 브랜치의 [흰 여백 빼기 계획](../vision-efficiency/README.md)이 이 갈래입니다.

| 연구 | 내용 | 우리에게 |
|---|---|---|
| [PixelPrune](https://github.com/OPPO-Mente-Lab/PixelPrune) (2026) | 같은 픽셀 패치(여백)를 인코더 앞에서 제거, 학습 없음, Qwen3.5 코드 공개 | 흰 여백 빼기의 출발 코드 |
| [Index-Preserving Token Pruning](https://github.com/sujin-1013/index-preserving-lightweight-token-pruning) (2026) | 배경 패치 제거, 남은 토큰은 원래 위치 번호 유지 | 좌표 과제에 필요한 설계 |
| [Grounding-Aware Token Pruning](https://arxiv.org/abs/2506.21873) (2025) | 토큰을 빼면 위치 번호가 어긋나 grounding이 무너짐. 위치 유지로 회복 | 위치 번호 유지는 필수 |
| [RTPrune](https://icml.cc/virtual/2026/poster/62926) (2026) | 문서 OCR에서는 일반 VLM용 가지치기가 무작위보다 나쁨 | 어텐션 기반 일반 기법은 쓰지 않음 |
| [MinerU2.5](https://huggingface.co/papers/2509.22186) (2025) | 저해상도로 배치를 먼저 보고, 필요한 곳만 원래 해상도로 잘라 읽음 | `ocr_page`를 영역별로 나누는 방식의 근거. 캐시와 충돌하므로 나중에 |

### 서빙 설정

| 항목 | 내용 | 우리에게 |
|---|---|---|
| 혼합 구조 프리픽스 캐시 | 위 1절. `--mamba-cache-mode align`, 블록 크기, `prefix_match_unit` | 지금 기대하는 이득이 실제로 있는지부터 확인 |
| 양자화 | A100은 FP8 연산이 없음. 가중치만 줄이는 W8A16·W4A16은 답 생성(메모리 병목)을, INT8 W8A8은 입력 처리를 빠르게 함. 비전 인코더는 BF16으로 두어야 한다는 사례가 있음 ([사례](https://evilpiepirate.org/forge/kent/consciousness/commit/11a7e4043e0b3e58f56566b17b22e7b15a241e49)) | 손실이 있을 수 있어 점수로 판단 |
| [MPIC](https://arxiv.org/abs/2502.01960) (2025) | 이미지 KV를 프롬프트 어디서든 재사용 | 같은 페이지가 여러 문항에 다른 조합으로 들어가는 2부(`doc_check`, `cross_check`)에 해당. 나중에 |

**정리하면**
- 답을 바꾸지 않는 방법(캐시 확인, MTP 추측 디코딩)이 먼저입니다. 점수를 다시 검증할 부담이 거의 없습니다.
- 추측 디코딩의 이득은 **동시 요청이 적을 때 크고, 많을 때 작습니다**(GPU가 이미 바쁨). 지금 평가처럼 서버당 32~64개를 동시에 보내는 처리량 측정과, 실제 업무처럼 한 건씩 기다리는 지연 측정을 둘 다 봐야 합니다.
- 입력 줄이기와 양자화는 점수가 바뀔 수 있어 benchmark로 판단합니다.

## 3. 방향과 순서

| 단계 | 내용 | 학습 | 점수 변화 | 판정 |
|---|---|---|---|---|
| **0. 측정** | 과제별로 입력 토큰, 답 토큰, 첫 토큰까지 시간, 토큰당 시간, 프리픽스 캐시 적중률을 잰다. 처리량(서버당 동시 32~64)과 단건 지연(동시 1~4) 두 조건 | 없음 | 없음 | 시간이 입력 쪽인지 답 쪽인지 과제별로 확정 |
| **1. 캐시 바로잡기** | 적중률이 낮으면 vLLM 버전·`mamba_cache_mode`·블록 크기·`prefix_match_unit` 조정 | 없음 | 없음 | 같은 페이지 두 번째 질문의 첫 토큰 시간이 크게 줄어야 함 |
| **2. MTP 추측 디코딩** | 지금 SFT·GRPO 모델에 내장 MTP 머리를 켠다. `num_speculative_tokens` 1~4, 과제별 적중 길이·속도 | 없음 | 없음(temperature 0) | 답 생성이 긴 과제(`spotting`, `ocr_page`, `kie`)에서 빨라지는지 |
| **3. MTP 머리 다시 맞추기** | 2에서 적중이 낮으면, 지금 모델이 **스스로 낸 답**으로 MTP 머리만 학습(본 모델은 고정) | MTP 머리만 | 없음 | 적중 길이 증가 |
| **4. 입력 줄이기** | [흰 여백 빼기](../vision-efficiency/README.md) | 필요하면 | 있을 수 있음 | 토큰 30% 이상 감소, 과제별 하락 1%p 이내 |
| **5. 양자화** | W8A16(답 생성), INT8 W8A8(입력 처리). 비전 인코더는 BF16 | 없음 | 있을 수 있음 | 과제별 하락 1%p 이내 |

선택 확장(1~5 결과를 보고 결정)
- **답 형식 줄이기:** 박스 JSON의 고정 글자(`{"bbox_2d": `, `"label": `)가 답 토큰에서 차지하는 비율을 0단계에서 잰다. 크면 더 짧은 형식으로 다시 학습하는 것을 검토한다. 다만 Qwen 기본 형식에서 벗어나고 `guide/`의 답 형식도 바뀐다.
- **작은 모델:** 지금 모델의 답으로 Qwen3.5-4B 등을 학습(증류). 이득은 가장 크지만 1·2부 학습을 다시 해야 한다.
- **여러 페이지 문항의 페이지 캐시 재사용**(MPIC 류).

### 3단계: MTP 머리 다시 맞추기

- **왜:** MTP 머리는 원래 Qwen3.5가 낼 다음 토큰을 맞히도록 학습됐습니다. SFT 뒤 모델은 우리 답 형식(박스 JSON, 서류 받아쓰기)을 내므로 적중이 떨어졌을 수 있습니다.
- **라벨이 필요 없습니다.** 생성 데이터와 내부 OCR 데이터의 학습용 이미지에 지금 모델로 답을 생성하고, 그 답을 MTP 머리가 맞히도록 학습합니다(자기 증류). benchmark 이미지는 쓰지 않습니다.
- **본 모델은 고정**이라 temperature 0 답은 그대로이고, benchmark 점수를 다시 검증할 필요가 거의 없습니다.
- 확인할 것: ms-swift에서 MTP 머리만 학습하는 설정, 학습한 MTP 가중치를 vLLM이 읽는 체크포인트 형식.

## 4. 데이터

| 데이터 | 형식 | 쓰임 |
|---|---|---|
| 내부 OCR | 실제 이미지 + 사내 OCR 단어 박스 → `bank_ocr prepare` | 1부 benchmark로 속도·점수 측정. 학습용 이미지는 3단계 MTP 머리 학습 |
| 생성 은행 업무 | `docgen.bench build`, `make_bank_data.sh` | 2부 benchmark로 속도·점수 측정(여러 장 문항 포함). 학습용 분할은 3단계 MTP 머리 학습 |
| 생성 → OCR 형식 | 생성 이미지 + 단어 박스를 사내 OCR 형식으로 → `bank_ocr prepare` | 4단계(흰 여백 빼기)에서 정확한 박스로 근거 커버리지 계산 |

## 5. 측정

- **부하:** 지금 평가와 같은 benchmark 문항을 같은 순서(같은 이미지 질문을 몰아서)로 보낸다. 서버 옵션만 바꿔 가며 같은 문항을 반복한다.
- **조건:** 처리량(서버당 동시 32~64, 지금 평가 설정)과 단건 지연(동시 1~4).
- **지표**

| 구분 | 지표 |
|---|---|
| 점수 | 1부·2부 benchmark 과제별 점수(기존 채점 그대로) |
| 답 동일성 | 기준 설정과 답이 글자까지 같은 문항 비율. 무손실 단계(1~3)는 99% 이상이어야 함(배치에 따른 수치 차이로 100%는 아닐 수 있음) |
| 속도 | 처리량(문항/초), 첫 토큰까지 시간 p50·p95, 답 토큰당 시간, 과제별 문항당 시간 |
| 원인 | 입력·답 토큰 수, 프리픽스 캐시 적중률, 추측 디코딩 적중 길이(vLLM `/metrics`) |

- 지금 예측 코드(`bank_ocr/inference.py`, `docgen/bench/runner.py`)는 응답을 한 번에 받아 첫 토큰 시간을 알 수 없습니다. 측정 도구는 이 폴더에 따로 만들고(스트리밍으로 받기 + `/metrics` 수집), 기존 코드는 고치지 않습니다.

## 6. 실행 환경

- 실제 숫자는 내부망(서류 이미지, SFT·GRPO 모델, vLLM, A100)에서 냅니다. 내부망 vLLM·ms-swift 버전을 먼저 기록합니다. 혼합 구조 캐시와 MTP 지원이 버전마다 다릅니다.
- 이 저장소의 합성 예시 데이터로는 측정 도구가 돌아가는지만 확인합니다.
- 관련 연구의 수치는 모두 저자 또는 사용자 보고 값입니다.
