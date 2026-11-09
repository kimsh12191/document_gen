# 데이터 만들기

합성 서류로 **평가 세트**와 **학습 데이터**를 만듭니다. 생성은 studio 컨테이너에서만 합니다 (화면, 또는 다른 곳에서 `docker/remote_build.py`).
만든 데이터셋은 폴더 하나이고, 학습([training.md](training.md))에는 그 경로만 적습니다.

- **평가 세트**(`split` `test`, OCR 은 `benchmark`): 모델 비교용. 한 번 만들면 고정해서 계속 씁니다.
- **학습 데이터**(`split` `train`): 평가 세트와 다른 고객(seed)으로 만들어집니다. 같은 데이터셋을 양쪽에 넣지 않습니다.
- 정답은 사람이 적지 않습니다. 서식에 넣은 값과 잰 위치가 곧 정답이라, 서식을 고치면 다음 생성부터 데이터가 따라 바뀝니다 ([서식 폴더 설명서](../docgen/forms/README.md)).

## 1. studio 띄우기·접속

내부망 Linux 서버의 코드 폴더에서 (처음 설치는 [docker/README.md](../docker/README.md) 1·2절):

```bash
sh docker/studio.sh --data /database/docgen_studio    # 처음 한 번: 저장 폴더를 정해 띄우기
sh docker/studio.sh                                   # 다음부터
sh docker/studio.sh --open                            # 다른 컨테이너에서 API(remote_build.py)로 쓸 때 (로그인 없음. 실서류를 다룰 때는 --local)
```

윈도우 PC에서 터널을 열고 브라우저로 `http://localhost:8765` 에 들어갑니다: `ssh -N -L 8765:localhost:8765 <계정>@<서버IP>`.

- 데이터셋은 `<저장 폴더>/workspace/datasets/<이름>/` 에 생깁니다 (컨테이너 안에서는 `/out/...`). 학습 서버와 이 폴더를 공유합니다.
- 왼쪽 메뉴: 사용 가이드 · OCR 예시 · 서식 · 새 서식 추가 · 키 사전 · 표시 요소 · 시나리오·묶음 · 데이터셋.
  복잡하거나 자주 쓰지 않는 화면(가져오기 · 검수 · 평가 · 작업 · 설정)은 일부러 메뉴에서 숨겼습니다 (기능은 그대로, 주소 `#/import` `#/review` `#/eval` `#/jobs` `#/settings`).
  문서와 코드 주석의 ①~⑨ 는 예전 메뉴 번호입니다: ① 서식 ② 표시 요소 ③ 시나리오·묶음 ④ 가져오기 ⑤ 검수 ⑥ 데이터셋 ⑦ 평가 ⑧ 작업 ⑨ 설정.

## 2. 무엇을 만들지 정하기

목적을 과제로 바꿉니다. 한 서류에서 관련 과제를 함께 만들고, 특정 과제만 필요하면 결과의 `tasks/<과제>.jsonl` 만 씁니다.
과제마다 질문·답·채점은 [benchmark.md](benchmark.md#과제), 실제 예시는 [tasks.md](tasks.md).

| 목적 | 트랙 / 과제 | 레시피에서 정하는 것 |
|---|---|---|
| 서류 분류 | bank / `classify` | `types`, `per_doc` |
| 항목 값·위치 추출 | bank / `kie` | `types`, `per_doc`, `max_keys` |
| 체크·도장·서명 | bank / `marks` | 그 표시가 있는 `types` |
| 기타·비고 칸의 대충 쓴 글을 DB 칸으로 정리 | bank / `freetext` | 하나은행 서식(`hf*`)이 들어간 `types` |
| 서식 전용 질문 (계산·판단 등) | bank / `form_qa` | 서식 폴더에 `qa.py` 가 있는 `types` |
| 값 칸 글자 읽기, 전체 받아쓰기 | bank / `ocr_field`, `ocr_page` | `types`, `fields_per_doc` |
| 제출 서류 구비 확인 | bank / `doc_check` | `scenarios`, `bundles`, `bundle` |
| 서류 간 불일치 | bank / `cross_check` | `scenarios`, `bundles`, `cases` |
| 서류 근거 계산·판단 | bank / `review` | `scenarios`, `bundles` |
| 쪽 전체 글자·위치 (OCR 8과제) | ocr / `crop_ocr` `bbox_ocr` `region_ocr` `grounding` `spotting` `relation` `marked_ocr` `marked_box` | `types`, `per_doc`, `unit` |
| 실서류 이미지 OCR | 학습 서버에서 [ocr.md](ocr.md) (사내 OCR) | 이미지 폴더 |

서식·업무 ID 는 추측하지 말고 조회합니다.

```bash
python docker/remote_build.py types --find 재직           # 서식 ID (--group income 으로 그룹)
python docker/remote_build.py catalog --form <서식ID>      # 그 서식의 추출 항목·연결 업무
python docker/remote_build.py scenarios                   # 업무 ID 와 필요 서류 (사람용 표: catalog.md)
```

이름으로 서식 ID 찾기는 [documents.md](documents.md), 업무별 서류·대조 사례·심사 규칙은 [catalog.md](catalog.md).
이미 있는 데이터셋이면 새로 만들지 않고 씁니다: `python docker/remote_build.py jobs`, 학습 서버에서 `find <저장 폴더>/workspace/datasets -maxdepth 3 -name meta.json`.

## 3. studio 화면으로 만들기

화면 전체 흐름은 [studio.md 3절](studio.md#3-데이터셋).

**데이터셋 › 새로 만들기**에서 레시피를 고르고 이름을 정해 **만들기**를 누릅니다. 끝나면 목록에 자동으로 등록됩니다.

| 레시피 | 만드는 것 |
|---|---|
| `bank-bench` | 은행 업무 평가 세트 (서식 문항 + 업무 12종 묶음) |
| `bank-train` | 은행 업무 학습 데이터 |
| `ocr-bench` · `ocr-train` | 합성 OCR 평가 세트 · 학습 데이터 (서식을 그려 쪽 전체 글자를 정답으로) |

- **용도**(평가 세트 / 학습)를 꼭 확인합니다. 서식·업무·수량·촬영 조건·대조 사례는 레시피에서 고칩니다 (칸은 4절 표).
- OCR 레시피는 OCR 준비까지 돌립니다. `<이름>/prepared/DONE.json` 이 생겨야 끝이고, 학습에는 `<이름>/prepared` 경로를 적습니다.
- `bank-*` 레시피는 표 문항(`table` 표 추출, `table_read`, `table_find`, `table_qa`)도 만듭니다. 표(행 수가 서류마다 다른 반복 목록)는 `kie` 가 아니라 표 문항이 묻습니다 ([표의 정의](benchmark.md#표의-정의)). 일부 서류는 값 칸이 검은 상자로 가려져 있고(정답 null), 용도·비고 같은 칸이 비어 있기도 합니다 — 일부러 그런 것입니다.
- `bank-*` 레시피는 `freetext` 문항도 만듭니다. 비고·기타 칸 일부에 `3천 정도 1년, 담달 말까지 서류 낼게요` 처럼 **일부러 대충 쓴 글**이 들어갑니다 (이상한 값이 아님).
- 검수 완료 전의 가져온 서식은 레시피의 `"all"`·그룹 선택에 들어가지 않습니다.
- **처음에는 작게** 만들어 5절대로 본 뒤 크게 만듭니다.

## 4. 명령으로 만들기 (`remote_build.py`)

다른 컨테이너·PC 에서 studio 에 생성을 맡깁니다 (`sh docker/studio.sh --open` 으로 띄운 studio).

```bash
export STUDIO_URL=http://<서버IP>:8765
python docker/remote_build.py recipes                                          # 연결 확인 (레시피 목록)
python docker/remote_build.py build --name <이름>-pilot --file recipe.json     # 소량. 끝날 때까지 기다림
python docker/remote_build.py build --name <이름> --file recipe.json --workers 8 --no-wait   # 본 생성
python docker/remote_build.py status <작업ID>                                  # 진행
python docker/remote_build.py composition <이름> --out composition.json        # 구성·수량
```

자주 쓰는 것은 옵션으로도 됩니다: `build --name x --recipe bank-bench`, `--types income --per-doc 3`, `--scenarios mortgage --bundles 20`, `--track ocr --types identity --unit line`.

레시피 JSON 의 칸:

| 칸 | 뜻 |
|---|---|
| `track` | `bank` (기본) · `ocr` |
| `split` | bank `test`·`train`, ocr `benchmark`·`train` |
| `types`, `exclude`, `reviewed_only` | 서식: `"all"` · ID 목록 · 그룹. 뺄 서식 (업무 묶음에서도 빠짐). 검수 완료 서식만 |
| `per_doc` | 서식마다 문서 수 (문항 수 아님). `0` 이면 단일 서류 과제 없이 업무 묶음만 |
| `scenarios`, `bundles` | 업무 ID 와 업무마다 고객 묶음 수 (`{"default": 4, "mortgage": 20}` 도 됨) |
| `conditions` | 촬영 조건 비율, 합 1: `{"clean": 0.5, "scan": 0.2, "photo": 0.15, "fax": 0.15}` |
| `start` | seed 시작. 같은 설정으로 더 만들 때 앞 양만큼 옮김 (이름만 바꾸면 같은 표본) |
| `fields_per_doc`, `max_keys` | bank: 값 칸 문항 수, kie·marks 한 문항의 최대 항목 수 |
| `bundle` | bank: 빠진 서류 0/1/2건 비율, 타인·불필요 서류, 변조 확률 |
| `cases` | bank: 대조 사례별 `{"enabled", "tamper"}` (사례는 [benchmark.md](benchmark.md#불일치-사례)) |
| `page_view` | bank: 여러 쪽 서류에서 한 쪽만 넣고 그 쪽만 묻는 비율 (기본 0.5, 0 이면 늘 모든 쪽). 문항 `meta.view` 가 `page`/`all` ([benchmark.md](benchmark.md#여러-쪽-서류-한-쪽만--모든-쪽)) |
| `nulls` | bank: 빈 답 배우기 `{"blank": 0.3, "mask": 0.1}` (기본값). 비어 있기도 한 칸(용도·비고 …) 비우는 비율, 값 칸을 검은 상자로 가리는 서류 비율. 0 이면 끔 ([benchmark.md](benchmark.md#빈-답-null-배우기)) |
| `unit`, `heavy`, `special`, `prepare` | ocr: 정답 단위 `word`·`line`, 내용 많음·특수 상황, OCR 준비 설정 덮어쓰기 |

예 (소득 서류 추출 학습, 소량):

```json
{"track": "bank", "split": "train", "types": ["income"], "per_doc": 2,
 "scenarios": [], "bundles": 0, "max_keys": 40, "conditions": {"clean": 0.5, "scan": 0.5}}
```

| 상태 | 뜻 / 할 일 |
|---|---|
| `done` | 끝남. 출력에 데이터셋 경로가 나오고 studio 목록에 등록됨 |
| `running` | 진행 중. `status` 로 다시 봄 |
| `interrupted` | studio 가 다시 떴을 뿐 생성은 계속됨. 기다림 |
| `failed` | `status` 의 로그 끝을 보고 원인 확인. 같은 설정으로 바로 다시 하지 않음 |
| `400 … 모르는 서식` | ID 오류. 아무것도 안 만들어짐. 2절 조회로 고침 |
| `이미 있는 폴더입니다` | 이름이 이미 있음. **기존 데이터셋을 쓸지 먼저 확인**, 새로 만들 때만 새 이름 |

컨테이너 안에서 직접 만들 수도 있습니다 (`sh docker/studio.sh shell`): `python -m docgen.bench build --out /out/<이름> [--recipe docgen/recipes/<이름>.json] [--split train]`,
평가 세트와 학습 데이터를 통째로 만드는 `bash docgen/scripts/make_bank_data.sh` (약 1시간 15분). 이렇게 만든 것은 studio 데이터셋 화면에서 등록합니다.

## 5. 만든 뒤 확인

결과 폴더 (`<저장 폴더>/workspace/datasets/<이름>/`):

| | bank | ocr |
|---|---|---|
| 문항 | `tasks/<과제>.jsonl` | `prepared/tasks/<과제>.jsonl` |
| 학습에 적을 경로 | `<이름>/` | `<이름>/prepared/` |
| 설정·재현 정보 | `meta.json`, `dataset.json` (생성기 커밋·버전) | `ocr_set.json`, `prepared/meta.json` |

문항 한 줄은 `{id, task, images, prompt, answer, eval, meta}` 입니다 (위치 `bbox_2d` 는 0~1000 상대 좌표, `page` 는 1부터. 자세히 [benchmark.md](benchmark.md#문항-형식-tasks과제jsonl)).
bank 학습 데이터에는 ms-swift 형식 `swift/<과제>.jsonl` 도 같이 생깁니다.

**본 생성 전에 소량으로 반드시:**
1. 필요한 `tasks/<과제>.jsonl` 이 있고 비어 있지 않음. 과제별 문항 수 (`composition`).
2. **사람이** studio **데이터셋 › 문항**에서 그림과 정답(박스)이 맞는지 봅니다. 형식 검사 통과는 검수가 아닙니다.

| 보고 싶은 것 | studio |
|---|---|
| 문항의 그림·질문·정답 박스 | 데이터셋 › 문항 |
| 업무·시나리오·과제·정답 구조별 수량 | 데이터셋 › 구성·추적 |
| 학습 설정 파일 만들기 | 데이터셋 › 학습 탭 → `train/configs/studio-<이름>.json` ([training.md](training.md)) |
| 서식 하나의 칸·위치·질문→답 예시 | 서식 › 개요 (카드 원문) / 질문·답 |

## 6. 내 데이터

| 가진 것 | 쓰는 법 |
|---|---|
| 검수한 실서류 추출 데이터 (ms-swift `.jsonl`) | studio 를 거치지 않고 학습 설정에 바로: 평가 세트 [eval.md 1절](eval.md#1-평가-세트-정하기), 학습 데이터 [training.md 2절](training.md#2-설정-파일) |
| 실서류 이미지 (OCR 학습·평가) | 학습 서버에서 [ocr.md](ocr.md). 실서류 이미지는 외부 모델·서비스에 보내지 않습니다 |
| 이미지 + 정답 라벨, 이미 돌린 결과 폴더 | 숨긴 가져오기 화면(`#/import`). 형식은 [archive/studio/](../archive/studio/) (예전 문서) |
