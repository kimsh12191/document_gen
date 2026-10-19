# 여러 쪽 문서 추출에서 행이 빠지는 원인

> 여러 쪽짜리 서류(거래내역서, 등기부등본, 주민등록등본, 재무제표, 인보이스·패킹리스트)의 목록을 VLM으로 뽑을 때
> **행이 왜 빠지는지**를 원인별로 떼어 내 측정하고, 밝혀진 원인에 맞는 처방을 찾는다.

이 브랜치(`claude/multipage-bundle-extraction`)는 이 연구만 담는다. 합성 서류 생성기(`docgen/`)는 데이터를 만드는 데
쓰는 의존 코드이고, 연구 코드는 `mpx/`다. 1·2부 학습 파이프라인과 가이드는 `claude/ocr-banking-benchmark` 브랜치에 있다.

- [1. 연구 내용](#1-연구-내용)
- [2. 사용 방법](#2-사용-방법)
- [3. 모듈 설명](#3-모듈-설명)

---

## 1. 연구 내용

### 1.1 문제

은행 업무에서는 고객이 낸 서류 묶음에서 여러 쪽짜리 서류의 내용을 **빠짐없이** 옮겨야 하는 일이 있다
(거래내역 전체, 등기 사항 전부, 재무제표 계정 전부). 그런데 지금 2부 은행 업무 모델의 입력·출력 방식으로는 이것이 어렵다.

| | 2부 설정 | 여러 쪽 서류 전체를 뽑으려면 |
|---|---|---|
| 입력 | 한 문항에 이미지 최대 13장, 이미지 토큰 합 12,000 이하 (13장이면 장당 약 920토큰, 원래 해상도의 1/4) | 쪽이 늘수록 장당 해상도가 더 떨어짐 |
| 출력 | 답 상한 4,096토큰 | 묶음 전체 답이 중앙값 약 8,600토큰, 최대 약 13,500토큰 (생성 데이터에서 정답을 그대로 쓴 길이) |
| 문항 | 묻는 항목만 답하는 질의형(대조, 심사 질문, 항목 추출) | 목록 전체를 옮겨야 함 |

여러 쪽 문서에서 VLM의 추출 점수가 무너지고 행이 빠진다는 보고는 있다(ExtractBench, 50쪽 넘으면 87.9 → 27.9).
그러나 **무엇 때문에 빠지는지**는 분리해서 밝혀진 적이 없다. 실제 서류에서는 원인이 늘 함께 움직이기 때문이다.
쪽이 많으면 해상도도 떨어지고, 이미지도 늘고, 답도 길어진다. 원인을 모르면 처방도 정할 수 없다.

### 1.2 이 연구만 할 수 있는 것

`docgen`은 **같은 내용**을 해상도, 쪽 나눔, 머리글 유무만 바꿔 다시 만들 수 있고, 모든 행의 값과 위치(쪽, 박스)를 안다.
그래서 원인을 하나씩 떼어 볼 수 있다.

### 1.3 후보 원인과 예상

| 단계 | 후보 | 예상 | 근거 |
|---|---|---|---|
| 출력 | **출력 길이** (상한에 잘림, 긴 출력 중간에 건너뜀) | 가장 유력 | 전체 답 중앙값 8,600토큰 > 2부 상한 4,096 |
| 읽기 | **행 간격 < 이미지 토큰 하나** (해상도) | 유력. 누락보다 값 틀림·행 합쳐짐으로 나타날 것 | 토큰 하나 = 32×32px. 한 번에 넣기에서 행 간격 중앙값 0.74토큰, **82%의 행이 1토큰보다 좁음** (원래 해상도는 1.60토큰, 14%) |
| 출력 | 비슷한 행 반복 | 중간. 실제 거래내역에서 더 클 것 | "체크카드 / 자동이체" 같은 행이 연달아 나오면 반복으로 보고 건너뜀 |
| 출력 | 스스로 일찍 끝냄 | 중간 | 학습 때 본 목록 길이 근처에서 멈춤 |
| 여러 쪽 | 쪽 경계 | 중간 | 경계 앞뒤 행이 빠지거나 겹침 |
| 여러 쪽 | 이미지 수 | 낮음 (문서 나누기 실수로는 나타날 수 있음) | |
| 여러 쪽 | 머리글 없는 다음 쪽 | 낮음 (칸 이름을 질문에 알려 주므로) | |
| 채점 착시 | 잘못 읽음, 다른 곳에 넣음 | 따로 셈 | 행은 냈지만 값이 틀려 짝이 안 지어지는 경우를 누락과 구분 |

### 1.4 방법 (3단계)

**1단계 — 관찰: 실제로 어디서, 어떻게 빠지는가.**
묶음을 두 방식으로 돌린다. 하나는 2부처럼 모든 쪽을 한 질문에 넣는 `allatonce`, 다른 하나는 원래 해상도로 한 쪽씩 묻는 `pagewise`다.
정답 행 하나하나에 대해 결과를 아래처럼 나누고, 특징(글자 높이·행 간격을 토큰 단위로, 출력 속 위치, 이웃 행과 같은 칸
비율, 쪽 경계 여부 등)을 함께 기록한다. 그다음 어떤 특징이 누락과 묶이는지 구간별 누락률과 로지스틱 회귀로 순위를 낸다.

| 결과 | 뜻 | 누락 |
|---|---|---|
| 정확 `exact` | 모든 칸 맞음 | |
| 일부 틀림 `partial` | 짝은 지어졌으나 일부 칸 틀림 | |
| 잘못 읽음 `misread` | 그 자리에 행을 냈지만 절반 이상 틀림 | |
| 다른 곳에 `misplaced` | 다른 목록이나 다른 문서에 들어감 | |
| 건너뜀 `skipped` | 앞뒤 행은 냈는데 이 행만 없음 | ● |
| 길이에 잘림 `cut_length` | 답이 길이 상한에 잘려 이 행부터 없음 | ● |
| 스스로 끝냄 `cut_stop` | 상한이 아닌데 모델이 이 행 앞에서 끝냄 | ● |
| 문서 못 찾음 `doc_missing` | 문서 자체를 못 찾음 | ● |

관찰은 상관일 뿐이다. 한 번에 넣기에서는 쪽 수가 늘면 해상도, 이미지 수, 출력 길이가 함께 변하므로 원인 판정은 2단계에서 한다.

**2단계 — 통제 실험: 한 가지만 바꾼다.**
같은 쪽, 같은 행을 두고 조건 하나만 바꿔 그 쪽 행의 누락률을 비교한다. 같은 행끼리 짝지어 "기준 조건에서는 나왔는데
이 조건에서 빠진 행 수"를 센다.

| 실험 | 바꾸는 것 | 고정하는 것 |
|---|---|---|
| A 해상도 | 쪽 이미지 토큰 460 / 920 / 1,800 / 원래(약 3,600) | 그 쪽 한 장, 그 쪽 행만 묻기 |
| B 출력 길이 | 문서 전체 행을 묻기 / 그 쪽 행만 묻기 | 입력 이미지(문서 전 쪽, 쪽당 920토큰) |
| C 이미지 수 | 대상 쪽 + 같은 묶음의 다른 쪽 0 / 2 / 4 / 8장 | 쪽당 920토큰, 대상 쪽 행만 묻기 |
| D 머리글 | 같은 내용을 머리글 반복 없게 / 있게 렌더링한 쌍둥이 판 | 그 쪽 한 장, 원래 해상도 |

**3단계 — 처방.** 원인에 맞는 처방을 고르고 비용과 함께 검증한다.

| 원인이 이것이면 | 처방 |
|---|---|
| 출력 길이 | 쪽·구간 단위로 끊어 출력 (해상도는 그대로 둬도 됨) |
| 해상도 | 원래 해상도로 한 장씩 |
| 이미지 수 | 문서를 먼저 나누고 문서마다 따로 |
| 쪽 사이 의존 | 앞 쪽에서 얻은 것(서류 종류, 마지막 행, 머리글)을 다음 쪽에 넘김 |

실제 서류는 정답이 없으므로 잔액 흐름(앞 잔액 − 출금 + 입금 = 잔액), 품목 합계, 예측 값이 사내 OCR 글자에 있는 비율로
방향을 확인한다(`mpx check`).

### 1.5 데이터

- **평가 묶음.** 벤치마크(`docgen.bench`)의 업무 시나리오 구성을 그대로 쓴다. 주택담보대출, 전세자금대출, 법인 여신, 해외송금이고, 고객 한 명이 한 업무로 낸 서류 전부다.
  고객 프로필과 촬영 조건 비율(원본 50%, 스캔·촬영·팩스 50%)도 벤치마크와 같다. 여기에 이 연구에 필요한 것만 더했다.
  - 대상 서류 70%를 긴 목록으로 (`--heavy`): 거래 30~90줄, 등기 사항 다수 등. 기본 길이면 대상 서류가 거의 1쪽이라 이 연구의 재료가 없다.
  - 시나리오에 없는 거래내역서·패킹리스트를 실무에서 함께 내는 서류로 덧붙임
  - 30%는 이어지는 쪽에 표 머리글을 다시 찍지 않음 (`--no-repeat-header`)
  - 머리글을 뺀 서류마다 머리글을 반복한 쌍둥이 판 (`--twins`, 실험 D)
- 이미 만들어 둔 벤치마크 출력은 그대로 쓰지 않는다. 대상 서류가 대부분 1쪽이고, 행마다의 쪽·위치 정답이 저장돼 있지 않다.
- 평가 고객 seed는 1,500,000부터 쓴다. docgen 기본 생성, 벤치마크와 겹치지 않는다.

### 1.6 판정 기준

- 관찰: 진짜 누락(●)이 정답 행의 몇 %이고, 그중 건너뜀 / 길이에 잘림 / 스스로 끝냄이 각각 얼마인가.
- 통제: 한 가지만 바꿨을 때 누락률 변화가 크고, 짝지은 비교에서 방향이 일관되면 원인으로 본다.
  예) 해상도를 1/4로 줄여도 그 쪽만 물으면 누락이 거의 없고, 같은 입력에서 문서 전체를 물을 때만 늘면 → 출력 길이가 원인.
- 일반성: 다른 계열 모델 하나 이상에서도 같은 방향이어야 한다.
- 처방: 누락을 줄이면서 비용(요청 수, 가장 긴 입력, 출력 토큰, 시간)이 어떤지 같이 보고한다.

### 1.7 현재 상태와 한계

- 모듈과 한 번에 실행하는 파이프라인은 완성됐다. 모델 없이 점검(정답 답 → 모든 행 정확, 일부러 넣은 오류 → 분류가 모두 찾음)은
  통과했다. **실제 모델 결과는 아직 없다** (GPU 서버에서 `run_experiment.sh`).
- 생성 서류와 실제 서류는 다르다. 실제 서류에서는 정답 없는 검사로만 방향을 확인한다.
- 질문에 목록·칸 이름을 알려 준다. 키 이름을 모르는 상황의 누락은 따로 보지 않는다.

---

## 2. 사용 방법

### 2.1 환경

- **생성(Chromium 필요).** 내부망에서는 docgen 도커 이미지를 쓴다([docs/DOCKER.md](docs/DOCKER.md)). 직접 설치하면
  `pip install -r requirements.txt`, 그리고 Chromium 경로를 `CHROMIUM_PATH`에 준다.
- **모델 실행.** OpenAI 호환 서버면 된다(vLLM 등). `run_experiment.sh`는 ms-swift(`swift deploy`)로 vLLM 서버를 띄운다.
  API 키가 필요하면 환경 변수 `INTERNAL_MODEL_API_KEY`.
- 모든 명령은 저장소 루트에서 `python -m mpx <명령>`.

### 2.2 한 번에 실행

```bash
# 모델 없이 점검 (약 1분): 정답 답·오류 주입 답으로 분류·분석·통제 실험·viewer 가 맞는지
python -m mpx pipeline --out runs/check --n-test 6

# 띄워 둔 모델로
python -m mpx pipeline --out runs/obs1 --n-test 100 --base-url http://127.0.0.1:8000/v1 --model bank-ocr

# GPU 서버에서 vLLM 서버까지 띄워 전부 (gen → observe → probe → score)
START_MODEL=/models/bank_sft_merged GPUS=0 ./run_experiment.sh
START_MODEL=... N_TEST=10 PROBE_ITEMS=5 ./run_experiment.sh                 # 리허설
START_MODEL=... MAX_TOKENS=4096 RUNS=runs_4096 ./run_experiment.sh observe  # 2부 답 상한(4096)에서는?
```

`pipeline`은 ① 생성 → ② 관찰 실행 → ③ 행 기록·분류 → ④ 분석 → ⑤ 통제 실험 → ⑥ 종합·viewer를 차례로 한다.
모델 없이 돌리면 각 실행을 정답 답(`oracle_*`)과 오류 주입 답(`simulated_*`)으로 두 번 하고, `summary.json`의
`checks`가 모두 "통과"여야 한다.

### 2.3 결과 보기

| 파일 (`<out>/`) | 내용 |
|---|---|
| `analysis.md` | 1단계: 결과 분포, 특징 구간별 누락률, 회귀 순위 |
| `probes/probes.md` | 2단계: 실험·조건별 결과 분포, 누락률, 짝지은 비교 (모델 없이면 `probes_oracle/`, `probes_simulated/`) |
| `probes/viewer.html` | 통제 실험 viewer: 기준 쪽마다 조건별 행 결과를 기호 줄로 |
| `data/test/viewer/index.html` | 묶음 viewer: 쪽 이미지, 정답, 방법별 답, 행마다 결과 기호 |
| `report/report.md` | 방법별 종합 점수(문서 나누기, 항목, 행, 경계 행)와 비용 |
| `rows.jsonl` | 정답 행마다 결과와 특징 (직접 분석할 때) |
| `summary.json` | 단계별 시간, 점검 결과 |

viewer 기호: ✓ 정확 · △ 일부 틀림 · ≠ 잘못 읽음 · ↷ 다른 곳에 · ✗ 건너뜀 · ✂ 길이에 잘림 · ■ 스스로 끝냄 · ∅ 문서 못 찾음.
다른 PC에서 보려면 `python -m mpx viewer --data <out>/data/test --pred <out>/preds/*.jsonl --serve 7862 --host 0.0.0.0`.

### 2.4 단계별로 돌릴 때

```bash
python -m mpx gen     --out data/test --n 100 --split test --twins --workers 8
python -m mpx stats   --data data/test
python -m mpx run     --data data/test --method allatonce --base-url $URL --model $M --out preds/allatonce.jsonl
python -m mpx run     --data data/test --method pagewise  --base-url $URL --model $M --out preds/pagewise.jsonl
python -m mpx rows    --data data/test --pred preds/*.jsonl --out rows.jsonl
python -m mpx analyze --rows rows.jsonl --out analysis.md
python -m mpx probe   --data data/test --out probes --base-url $URL --model $M        # --kinds resolution,scope 로 일부만
python -m mpx score   --data data/test --pred preds/*.jsonl --out report
python -m mpx viewer  --data data/test --pred preds/*.jsonl
python -m mpx check   --data real_bundles --pred preds/real.jsonl                      # 정답 없는 실제 서류
```

`run`, `probe`는 결과 파일이 있으면 남은 것만 이어서 한다. `--oracle`은 정답을 답으로, `--simulate p`는 오류를 일부러 넣는다(점검용).

### 2.5 테스트

```bash
python -m pytest tests            # 생성기(docgen) + mpx
python -m pytest tests/test_mpx.py
```

---

## 3. 모듈 설명

```
mpx/                 연구 코드
  gen.py             묶음 생성
  pages.py           쪽별 정답, 질문 문장, 쪽 답 병합
  parse.py           답에서 JSON 꺼내기, 잘린 답 살리기
  run.py             모델 실행 (allatonce, pagewise), 정답 답·오류 주입
  score.py           문서 맞추기, 항목·행 채점, 잔액·합계 검사
  rows.py            1단계: 행 결과 분류와 특징
  analyze.py         1단계: 누락 분석
  probe.py           2단계: 통제 실험
  report.py          종합 점수표
  viewer.py          묶음 viewer
  pipeline.py        한 번에 실행
  cli.py             명령줄
  common.py          파일 입출력, 이미지 크기·토큰 계산
run_experiment.sh    GPU 서버 한 바퀴
docgen/              합성 서류 생성기 (의존 코드). paginate.js 에 머리글 반복 끄기 스위치를 더함
templates/ fonts/ add_template/   생성기 서식·글꼴·실제 은행 서식
Dockerfile docker/ docs/DOCKER.md  생성기 실행 환경 (내부망 도커)
tests/               test_docs.py, test_bench.py (생성기), test_mpx.py (연구 코드)
```

### `mpx/gen.py` — 묶음 생성

- `generate(out, n, split, compose, ..., heavy, no_repeat_header, twins, workers)` 묶음 n개를 `<out>/bundles.jsonl`에 이어 쓴다. 이미 있는 seed는 건너뛴다.
- 구성 `compose`:
  - `scenario`(기본): 벤치마크 시나리오를 그대로 쓴다. `docgen.bench.build`의 `Builder.bundle_profile`, `pick_condition`을 쓰고, 제출 순서는 섞는다.
  - `random`: 대상 서류 2~4건과 한 쪽짜리 다른 서류 1~3건을 섞는다.
- `_render_doc`는 서류 한 건을 렌더링한다.
  - 확률적으로 긴 목록(`DOCGEN_HEAVY`)으로 만든다.
  - 머리글 반복을 끈다(`window.__noRepeatHeader`).
  - 촬영 조건대로 증강한다.
  - `twins`면 머리글을 반복한 쌍둥이 판을 만든다. 같은 내용에 같은 증강 난수를 쓴다.
- 출력 형식:
  - `bundles.jsonl` 한 줄: `{id, split, seed, scenario, task_name, docs: [서류ID], pages: [{image, doc, page}]}`
  - `labels/<서류ID>.json`: docgen 정답 `fields`(키, 값, 타입, 쪽, 박스)에 `target, heavy, no_repeat_header, augment, twin`를 더한 것
  - `labels/<서류ID>_twin.json`: 쌍둥이 판 정답
- `load(data)` → (묶음 목록, 서류ID → 정답). `stats(data)` → 묶음 쪽 수, 서류별 쪽 수·행 수.

### `mpx/pages.py` — 쪽별 정답, 질문, 병합

- 키 규칙: 키에 숫자가 처음 나오는 곳까지가 목록 이름이다. `rows.3.balance` → 목록 `rows`, 3번 행, 칸 `balance`.
- `page_views(label)`: 쪽마다 항목과 목록 행을 나눈다. 행은 첫 칸이 놓인 쪽에 속한다.
- `page_answer`: 한 쪽의 정답 답을 만든다. `doc_content`: 문서 전체 정답을 만든다.
- 질문 문장:
  - `all_prompt`: 묶음 전체를 한 질문으로 묻는다. `{"documents": [...]}`
  - `page_prompt`: 한 쪽만 묻는다. `{"document": {..., "continues"}, "fields", "lists"}`
  - `schema_hint(labels)`: 대상 서류 종류별 목록·칸 이름 안내를 만든다. 묶음에 무엇이 들었는지는 알려 주지 않는다.
- `merge_pages(쪽 답들)`: `continues`가 참이고 종류가 같으면 앞 문서에 잇는다. 행마다 어느 쪽 답에서 왔는지 `row_pages`에 남긴다.
- `run_pagewise(answer_fn, n, hint)`: 쪽마다 묻고 합친다.

### `mpx/parse.py` — 잘린 답 살리기

- `parse_output(text)` → (객체, 살렸는지).
- 온전한 JSON이 아니면 마지막으로 닫힌 객체·배열에서 자르고, 열린 괄호를 닫아 잘리기 전까지의 행을 살린다.
- 이렇게 해야 "잘려서 뒤가 없음"과 "처음부터 못 읽음"이 갈린다.

### `mpx/run.py` — 모델 실행

- `Client(base_url, model, max_tokens)`: OpenAI 호환 `chat/completions`. 생각 모드는 끄고 temperature 0으로 묻고, 일시 오류는 재시도한다.
- `run(data, out, method, client, workers, budget, limit, simulate, hint)`:
  - 묶음마다 실행해 jsonl로 쓴다. 결과 파일이 있으면 남은 묶음만 이어서 한다.
  - `allatonce`: 모든 쪽을 같은 비율로 줄여 이미지 토큰 합이 `budget`(12,000) 이하가 되게 한다.
  - `pagewise`: 쪽마다 원래 해상도(긴 변 2300, 짧은 변 1600 상한)로 묻는다.
- 기록 한 줄: `{bundle, method, budget, outputs, truncated(답마다 잘림), docs, usage, image_tokens, latency, injected}`.
- 점검용 두 가지:
  - `oracle_documents`, `oracle_page`: 정답 답(`--oracle`)
  - `simulate_rows`, `simulate_cut`: 오류 주입(`--simulate p`). 행마다 확률 p로 건너뜀, 잘못 읽음, 다른 목록, 칸 틀림을 넣는다. 답마다 확률 p로 길이에서 잘리게 하고, p/2로 끝 행들을 빼고 스스로 끝내게 한다.

### `mpx/score.py` — 채점

- `gt_docs(bundle, labels)`: 채점용 정답. 항목은 `{키: (값, 타입, 정규화값)}`, 목록은 행 목록, `row_page`는 행이 있는 쪽이다.
- `align(정답 행, 예측 행)`: 순서를 지키며 유사도 합이 최대가 되게 짝짓는다(동적 계획법). 칸 절반 이상 같아야 짝이 된다.
- `match_docs`: 정답 문서와 예측 문서를 쪽 집합이 겹치는 정도로 맞춘다.
- `score_bundle`, `summarize`: 쪽 배정, 문서 나누기, 항목 F1, 행 F1·재현율, 빠진 행, 경계 행, 이어지는 행, 잔액 흐름, 품목 합계를 낸다.
- `check_real`, `summarize_real`: 정답 없는 실제 서류를 검사한다. 예측 값이 사내 OCR 글자에 있는 비율, 잔액, 합계를 본다.

### `mpx/rows.py` — 행 결과 분류와 특징 (1단계)

- `classify_list(정답 행, 예측 행)`: `align`으로 짝을 짓는다. 짝 없는 정답 행은 앞뒤 짝 사이의 빈자리에서 예측 행과 순서대로 짝짓는다(잘못 읽음). 그래도 남으면 `missing`이다.
- `classify_bundle(bundle, labels, pred)`: 묶음 하나의 모든 정답 행을 1.4의 결과로 나눈다.
  - 남는 예측 행과 짝이 되면 → 다른 곳에
  - 출력 단위(한 번에 넣기는 답 전체, 쪽 단위는 그 쪽 답)에서 마지막으로 낸 행보다 뒤면 → 잘림(상한) 또는 스스로 끝냄
  - 그 외 → 건너뜀 또는 문서 못 찾음
- `classify_lists(정답 목록들, 답 목록들, 잘림)`: 답 하나를 같은 규칙으로 나눈다(통제 실험용).
- `row_records`: 대상 서류의 정답 행마다 결과와 특징을 기록한다.
  - 특징: `glyph_tok`, `pitch_tok`, `page_tokens`, `y_top`, `n_images`, `rows_before`, `row_frac`, `list_len`, `sim_neighbor`, `n_cells`, `chars`, `boundary`, `cont`, `no_header`, `augmented`, `heavy`
  - 글자 높이·행 간격은 정답 박스를 모델 입력 크기로 줄여 토큰(32px) 단위로 낸다.
- `collect(data, preds, out)` → `rows.jsonl`.

### `mpx/analyze.py` — 누락 분석 (1단계)

- `analyze(rows)`가 내는 것:
  - 실행별 결과 분포
  - 특징 구간별 누락률: 실행들을 합친 4분위 구간, 참/거짓
  - 로지스틱 회귀
- 회귀 방식: 특징은 표준화하고 작은 L2를 둔다(뉴턴법, 외부 패키지 없음). 계수는 1 표준편차당 로그 오즈이고, |z| 순서로 정렬한다.
- 회귀 대상은 두 가지다. "누락 전체"와, 잘림·스스로 끝냄을 뺀 "건너뜀만"이다.
- `run_analysis(rows.jsonl, out.md)` → `analysis.md`, `analysis.json`.

### `mpx/probe.py` — 통제 실험 (2단계)

- `build(data, out, kinds, max_items)`: 대상 서류에서 행이 3개 이상인 쪽을 실험마다 최대 `max_items`개 고르고, 조건별 문항을 만든다.
  - 문항 형식: `{id, kind, cond, doc, label, page, scope, images: [{image, budget}], prompt}`
  - 질문에는 그 서류의 목록·칸 이름을 넣는다.
- `run_probes`: 모델(또는 정답 답·오류 주입)로 답한다. 결과 파일이 있으면 이어서 한다.
- `score_probes`: 대상 쪽 정답 행마다 결과를 `rows.jsonl`에 쓴다. 기록 형식은 `{kind, cond, doc, list, key, outcome, dropped, glyph_tok, page_tokens, out_pos}`.
- `summarize`, `report`: 조건별 결과 분포와 누락률을 낸다. 짝지은 비교는 같은 서류·목록·행 번호끼리 기준 조건과 견준다. 출력은 `probes.md`, `probes.json`.
- `viewer`: `viewer.html`.
- `run_all`: 위 전부를 차례로.

### `mpx/report.py`, `mpx/viewer.py` — 종합표와 viewer

- `report.compare(data, preds, out)`: 방법별 종합 점수와 비용을 서류별, 쪽 수별, 머리글 여부별, 촬영 조건별로 나눠 낸다 → `report.md`.
- `viewer.build(data, preds)` → `<data>/viewer/index.html`, `b_<묶음>.html`.
  - 목록 화면: 묶음마다 방법별 쪽 배정, 행 F1, 누락률
  - 묶음 화면: 쪽 이미지, 방법별 문서 배정, 대상 서류의 항목 표, 행 표(행마다 결과 기호, 틀린 칸)
- 서버 없이 파일로도 열린다.

### `mpx/pipeline.py`, `mpx/cli.py`

- `pipeline.run_all(out, n_test, workers, base_url, model, budget, ..., probe_items)`: 2.2의 한 번에 실행이다.
- 모델 없이 돌리면 다음을 점검해 `summary.json`의 `checks`에 남긴다.
  - 정답 답은 모든 행이 정확하고 종합 지표 100%
  - 오류 주입 답은 넣은 오류 다섯 종류를 분류가 모두 찾음
  - 통제 실험: 정답 답은 누락 0, 오류 주입 답은 누락 > 0
- `cli.py`: 명령 `gen, stats, run, score, viewer, rows, analyze, probe, pipeline, check`. `python -m mpx <명령> -h`로 옵션을 본다.

### `docgen/` 에서 쓰는 것

- `docgen.render`: HTML과 정답 원본. `docgen.image.ImageRenderer`: Chromium으로 PNG를 만들고 박스를 잰다. `docgen.schema.build_fields`: 정답 fields.
- `docgen.augment`, `docgen.cli._aug_fields`: 스캔·촬영·팩스 증강과 박스 변환.
- `docgen.registry.SCENARIOS`, `docgen.bench.build`: 업무 시나리오, 고객 프로필, 촬영 조건.
- `docgen.bench.metrics`: 값 비교(`value_match`, `norm_text`, `to_number`).
- `docgen/paginate.js`: 표가 쪽을 넘으면 행 단위로 나누고 머리글을 반복한다. 이 연구에서 `window.__noRepeatHeader = true`이면 머리글을 반복하지 않는 스위치를 더했다(기본 동작은 그대로).
