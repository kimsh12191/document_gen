# Agent 작업 절차: 데이터 생성 → 학습 → 평가 → 보고

agent가 요청을 받아 끝까지 수행하는 순서입니다. 규칙은 [AGENTS.md](../AGENTS.md)를 먼저 읽습니다.
단계마다 **어디서 / 무엇을 / 완료 조건 / 실패하면**을 적었습니다. 완료 조건을 확인하기 전에는 다음 단계로 넘어가지 않습니다.

| 기호 | 실행 위치 |
|---|---|
| **[studio]** | studio 서버. 다른 곳에서는 HTTP(`docker/remote_build.py`, `STUDIO_URL`)로만 |
| **[train]** | GPU 학습 서버의 코드 폴더. GPU·ms-swift·vLLM이 있는 곳 |
| **[사람]** | 사람이 화면에서 확인해야 하는 것. agent는 요청하고 기다림 |

---

## 1. 환경 확인

**[어디서든]** 아래를 확인하고, 안 되는 것은 사용자에게 알린 뒤 그 단계를 빼고 계획합니다.

```bash
export STUDIO_URL=http://<서버IP>:8765
python docker/remote_build.py recipes       # studio 연결 (레시피 목록이 나오면 됨)
python docker/remote_build.py paths         # 데이터셋이 생기는 서버 경로
```

**[train]** 학습까지 맡았을 때만:

```bash
python -c "import swift, vllm, train, docgen.bench.evaluate; print('ok')"
nvidia-smi                                  # 비어 있는 GPU
ls <paths 의 서버 경로>                       # 학습 서버에서 데이터셋 폴더가 보이는지 (공유 폴더)
```

| 확인 | 안 되면 |
|---|---|
| studio 연결 | 생성 불가. `sh docker/studio.sh --open`이 필요하다고 보고 |
| 학습 서버에서 데이터셋 경로가 보임 | 학습 불가. 경로가 다르면 studio `config.json`의 `path_map` |
| GPU·학습 환경 | 학습 불가. studio에 접속된다고 학습할 수 있는 것이 아님 |
| 사내 OCR (`INTERNAL_OCR_BASE_URL`), VLM | 실서류 OCR 준비·실문서 추론 불가 |

**완료 조건:** 요청에 필요한 서비스·경로에 모두 접근됨. 안 되는 것은 보고함.

## 2. 데이터 계획

**[어디서든]** 목적을 과제로 바꿉니다.

| 목적 | 경로 / 과제 | 정하는 것 |
|---|---|---|
| 서류 분류 | bank / `classify` | `types`, `per_doc` |
| 항목 값·위치 추출 | bank / `kie` | `types`, `per_doc`, `max_keys` |
| 체크·도장·서명 | bank / `marks` | 그 표시가 있는 `types` |
| 값 칸 글자 읽기 | bank / `ocr_field`, `ocr_page` | `types`, `fields_per_doc` |
| 제출 서류 구비 확인 | bank / `doc_check` | `scenarios`, `bundles`, `bundle` |
| 서류 간 불일치 | bank / `cross_check` | `scenarios`, `bundles`, `cases` |
| 서류 근거 계산·판단 | bank / `review` | `scenarios`, `bundles` |
| 쪽 전체 글자·위치 (OCR 8과제) | ocr / `crop_ocr` `bbox_ocr` `region_ocr` `grounding` `spotting` `relation` `marked_ocr` `marked_box` | `types`, `per_doc`, `unit` |
| 실서류 OCR | [ocr.md](ocr.md) (사내 OCR, [train]) | 이미지 폴더 |

서식·업무 ID는 추측하지 말고 조회합니다.

```bash
python docker/remote_build.py types --find 재직           # 서식 ID (--group income 으로 그룹)
python docker/remote_build.py catalog --form <서식ID>      # 그 서식의 추출 항목·연결 업무
python docker/remote_build.py scenarios                   # 업무 ID와 필요 서류
```

- bank는 한 서류에서 관련 과제를 함께 만듭니다. 특정 과제만 필요하면 결과의 `tasks/<과제>.jsonl`만 씁니다.
- 학습용과 평가용은 따로 만듭니다 (`split`: bank `train`/`test`, ocr `train`/`benchmark`).
- 이미 있는 평가 세트가 있으면 새로 만들지 않고 그것을 씁니다 (실험끼리 비교하려면 고정).

**완료 조건:** 과제, 서식·업무 ID, 학습/평가 구분, 수량이 정해짐. 지원되지 않는 요구(아래 7절)는 보고에 적음.

## 3. 레시피 정하기

레시피 JSON의 칸:

| 칸 | 뜻 |
|---|---|
| `track` | `bank` (기본) · `ocr` |
| `split` | bank `test`·`train`, ocr `benchmark`·`train` |
| `types`, `exclude`, `reviewed_only` | 서식: `"all"` · ID 목록 · 그룹. 검수 완료 서식만. `exclude` 서식은 업무 묶음에서도 빠집니다: 고를 수 있는 다른 서식이 없는 묶음은 건너뛰고 `skipped_bundles.jsonl`·`meta.json`의 `skipped_bundles`에 남습니다 |
| `per_doc` | 서식마다 문서 수 (문항 수 아님) |
| `scenarios`, `bundles` | 업무 ID와 업무마다 고객 묶음 수 (`{"default": 4, "mortgage": 20}`도 됨) |
| `conditions` | 촬영 조건 비율, 합 1: `{"clean": 0.5, "scan": 0.2, "photo": 0.15, "fax": 0.15}` |
| `start` | seed 시작. 같은 설정으로 더 만들 때 앞 양만큼 옮김 (이름만 바꾸면 같은 표본) |
| `fields_per_doc`, `max_keys` | bank: 값 칸 문항 수, kie·marks 한 문항의 최대 항목 수 |
| `bundle` | bank: 빠진 서류 0/1/2건 비율, 타인·불필요 서류, 변조 확률 |
| `cases` | bank: 대조 사례별 `{"enabled", "tamper"}` (사례 ID는 `docgen/bench/cases.py`) |
| `unit`, `heavy`, `special`, `prepare` | ocr: 정답 단위 `word`·`line`, 내용 많음·특수 상황, OCR 준비 설정 덮어쓰기 |

예 (소득 서류 추출 학습, 소량):

```json
{"track": "bank", "split": "train", "types": ["income"], "per_doc": 2,
 "scenarios": [], "bundles": 0, "max_keys": 40, "conditions": {"clean": 0.5, "scan": 0.5}}
```

## 4. 소량 생성 → 확인 → 본 생성

**[studio]** (원격으로)

```bash
python docker/remote_build.py build --name <이름>-pilot --file recipe.json     # 끝날 때까지 기다림
python docker/remote_build.py build --name <이름> --file recipe.json --workers 8 --no-wait   # 본 생성
python docker/remote_build.py status <작업ID>                                  # 진행
python docker/remote_build.py composition <이름> --out composition.json        # 구성·수량
```

자주 쓰는 것은 옵션으로도 됩니다: `build --name x --recipe bank-bench`, `--types income --per-doc 3`, `--scenarios mortgage --bundles 20`, `--track ocr --types identity --unit line`.

| 상태 | 뜻 / 할 일 |
|---|---|
| `done` | 끝남. 출력에 데이터셋 경로가 나옴. ⑥에 자동 등록됨 |
| `running` | 진행 중. `status`로 다시 봄 |
| `interrupted` | studio가 다시 떴을 뿐 생성은 계속됨. 기다림 |
| `failed` | `status`의 로그 끝을 보고 원인 보고. 같은 설정으로 바로 재시도하지 않음 |
| `400 … 모르는 서식` | ID 오류. 아무것도 안 만들어짐. 2절 조회로 고침 |
| `이미 있는 폴더입니다` | 이름이 이미 있음. **기존 데이터셋을 쓸지 먼저 확인**, 새로 만들 때만 새 이름 |

결과 폴더 (`<저장 폴더>/workspace/datasets/<이름>/`):

| | bank | ocr |
|---|---|---|
| 문항 | `tasks/<과제>.jsonl` | `prepared/tasks/<과제>.jsonl` |
| 학습에 적을 경로 | `<이름>/` | `<이름>/prepared/` |
| 설정·재현 정보 | `meta.json`, `dataset.json` | `ocr_set.json`, `prepared/meta.json` |

문항 한 줄: `{id, task, images, prompt, answer, eval, meta}`. 위치 답 `bbox_2d`는 0~1000 상대 좌표, `page`는 1부터.

**소량 확인 (본 생성 전에 반드시):**
1. 필요한 `tasks/<과제>.jsonl`이 있고 비어 있지 않음. 과제별 문항 수를 셈.
2. 문항 몇 개의 이미지 경로가 열리고, 정답에 필요한 필드·표시가 있음.
3. **[사람]** 이미지와 정답이 맞는지 화면(⑥ › 문항)에서 봐 달라고 요청. 형식 검사를 통과한 것을 사람 검수로 보고하지 않음.

**완료 조건:** 본 데이터셋의 이름·경로·`dataset.json`의 생성기 커밋/버전을 확보함.

## 5. 학습 준비

**[train]** 설정 파일 하나를 만듭니다 (자세히: [training.md](training.md) 3절).

```bash
cp train/configs/pipeline.example.json train/configs/<실험>.json
```

- `workdir`, `data.output_dir`은 **새 이름** (이미 있으면 그 결과를 재사용하므로, 재사용이 목적일 때만 같은 이름).
- `data.train`: 학습용 데이터셋들 (OCR은 `count`), `data.benchmark`: 평가 세트들. 평가 세트를 `train`에 넣지 않음.
- 실서류 OCR을 함께 쓰면 [ocr.md](ocr.md)로 먼저 준비하고 그 폴더를 양쪽에 적음. `ocr_prepare` 줄은 지움.
- `model`, `gpus`를 1절에서 확인한 값으로.

```bash
python -m train --config train/configs/<실험>.json --smoke
```

**완료 조건:** 리허설이 끝나고 `<workdir>/smoke/reports/benchmark.html`이 생김.
**실패하면:** 첫 줄이 `설정(…)의 경로를 확인하세요`면 경로를 고쳐 다시. 그 밖은 `<workdir>/smoke/logs/`의 해당 단계 로그 끝을 보고 [training.md 6절](training.md#6-에러)로. 같은 에러가 두 번 나면 멈추고 보고.

## 6. 학습 실행

**[train]** 요청받은 범위만 실행합니다.

| 요청 | 명령 |
|---|---|
| 전부 (SFT + GRPO) | `nohup python -m train --config <설정> > <workdir>.log 2>&1 &` |
| SFT까지만 | `--part sft` |
| 끝난 SFT에서 GRPO | `--part grpo` (SFT 체크포인트가 없으면 멈춤) |
| 다른 실험의 SFT에서 GRPO | `--part grpo --sft-checkpoint <폴더>` |
| GRPO 설정을 바꿔 다시 | `--from grpo` |
| 평가만 (학습 없이) | `--only prepare`, `--only eval_base`, `--only report`. 섞기에 학습 문항이 필요하므로 `data.train`에 학습 데이터셋 하나는 둠 |

- 진행: `<workdir>/state.json`의 `done`(끝난 단계), `timings`(시간). 로그는 `<workdir>/logs/<단계>.log`.
- 멈췄으면 **같은 명령을 다시** 실행합니다 (끝난 단계는 건너뜀). 다시 실행해도 같은 단계에서 같은 에러면 멈추고 보고.
- 결과가 아쉬워도 요청에 없는 GRPO, 추가 학습, 데이터 재생성을 시작하지 않습니다. 제안으로 보고합니다.

**완료 조건:** 요청한 단계가 `state.json`의 `done`에 있고 `<workdir>/reports/benchmark.html`이 생김.

## 7. 결과 분석·보고

**[train]** 읽는 법은 [results.md](results.md).

1. 답 형식 오류율: SFT 뒤 거의 0%인지.
2. 과제별 주 지표의 출발 → SFT (→ GRPO) 변화.
3. 기준선(찍어도 나오는 점수)과 비교, 문항 수에 따른 오차 범위.
4. OCR 열이 출발 모델보다 크게 떨어졌는지.
5. 대표 오답 몇 개: `reports/*.json`과 **[사람]** studio ⑥ › 모델 답에 `<workdir>`를 붙여 확인 요청.

**보고에 넣을 것:**

| 항목 | 예 |
|---|---|
| 요청 범위와 실제 실행한 단계 | SFT까지, `state.json` done |
| 데이터 | 데이터셋 이름·경로, 레시피, 생성기 커밋·버전(`dataset.json`), 과제별 문항 수 |
| 설정 | 설정 파일 경로, 모델, GPU, `data.output_dir`, 바꾼 칸 |
| 결과 | 과제별 주 지표 표 (출발/SFT/GRPO), 형식 오류율, 오차 범위 안의 차이는 "차이 없음" |
| 확인 안 된 것 | 사람 검수를 받지 못한 것, 건너뛴 단계 |
| 경로 | `<workdir>/reports/benchmark.html`, 로그 폴더, 모델 `<workdir>/merged/…` |
| 다음 제안 | 실행하지 않은 추가 실험 |

## 8. 설정으로 안 되는 것

- **목록에 없는 서류 양식:** 서식 추가가 필요 ([docgen/manual/TEMPLATE_GUIDE.md](../docgen/manual/TEMPLATE_GUIDE.md), studio 서식 초안).
- **새 심사 질문·대조 규칙:** 생성·채점 코드 추가가 필요.
- **특정 값·사건의 정확한 개수:** 레시피는 비율만 정함. 생성 후 골라내거나 코드 확장.
- **다른 학습 포맷:** 생성 후 변환. 이미지 경로와 좌표 의미를 보존.
- **실제 고객 데이터 성능:** 합성 데이터 점수는 실서류보다 높게 나옴. 실서류 평가 세트는 studio 실문서 벤치마크로.
