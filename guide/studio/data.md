# 데이터셋 만들기

합성 서류로 **평가 세트**와 **학습 데이터**를 만듭니다. 생성은 studio 에서만 합니다 (화면, 또는 다른 곳에서 명령 `docker/remote_build.py`).
만든 데이터셋은 폴더 하나이고, 학습 설정에는 그 경로만 적습니다 (학습 서버의 [sweep.md](../train/sweep.md)).

- **평가 세트**: 모델 비교용. 한 번 만들면 고정해서 계속 씁니다.
- **학습 데이터**: 평가 세트와 다른 가짜 고객(seed)으로 만들어집니다. 같은 데이터셋을 양쪽에 넣지 않습니다.
- 정답은 서식에 넣은 값과 잰 위치입니다. 서식을 고치면 다음 생성부터 데이터가 따라 바뀝니다.

## 1. 화면으로 만들기

**데이터셋 › 새로 만들기**에서 레시피를 고르고 이름을 정해 **[만들기]**. 끝나면 **등록된 데이터셋**에 저절로 들어갑니다.

| 레시피 | 만드는 것 | 학습 설정에 적을 경로 |
|---|---|---|
| `bank-bench` · `bank-train` | 은행 서류 평가 세트 (서식마다 1건) · 학습 데이터 (서식마다 5건) | `<이름>/` |
| `ocr-bench` · `ocr-train` | 쪽 전체 글자·위치 OCR 평가 세트 · 학습 데이터 | `<이름>/prepared/` |
| `bank-try` | 몇 분짜리 시험 | |

- **처음에는 작게** 만들어 3절대로 본 뒤 크게 만듭니다.
- 레시피 이름을 누르면 서식·수량·촬영 조건을 고칩니다 (칸은 2절 표). 기본 레시피를 고치면 저장소 파일이 바뀌므로 다른 설정은 **틀에서 새 레시피**로.
- 검수 완료 전의 새 서식은 레시피의 `"all"`·그룹에 들어가지 않습니다.
- `bank-*` 에는 일부러 넣은 것이 있습니다: 값 칸을 검은 상자로 가린 서류(정답 null), 비어 있는 용도·비고 칸, 대충 쓴 비고 글(`3천 정도 1년, 담달 말까지 …`, `freetext` 과제).

과제와 레시피: bank 레시피 하나가 서류마다 `classify`·`kie`·`marks`·`freetext`·`form_qa`(서식에 `qa.py` 가 있을 때)·`ocr_field`·`ocr_page`·표 4종을 함께 만들고,
ocr 레시피는 OCR 8과제를 만듭니다. 특정 과제만 필요하면 학습 설정의 `task_mix` 로 고릅니다. 과제마다 질문·답은 [benchmark.md](../reference/benchmark.md).

## 2. 명령으로 만들기 (`remote_build.py`)

다른 컨테이너·PC 에서 studio 에 생성을 맡깁니다 (studio 를 `sh docker/studio.sh --open` 으로 띄운 경우).

```bash
export STUDIO_URL=http://<서버IP>:8765
python docker/remote_build.py recipes                                          # 연결 확인
python docker/remote_build.py types --find 재직                                # 서식 ID 찾기 (추측하지 않음)
python docker/remote_build.py jobs                                             # 이미 있는 것 (있으면 새로 만들지 않음)
python docker/remote_build.py build --name <이름>-pilot --file recipe.json     # 소량, 끝날 때까지 기다림
python docker/remote_build.py build --name <이름> --file recipe.json --workers 8 --no-wait
python docker/remote_build.py status <작업ID>
```

레시피 JSON (예: 소득 서류 학습, 소량 `{"track": "bank", "split": "train", "types": ["income"], "per_doc": 2, "conditions": {"clean": 0.5, "scan": 0.5}}`):

| 칸 | 뜻 |
|---|---|
| `track` · `split` | `bank`(기본) · `ocr`. bank `test`·`train`, ocr `benchmark`·`train` |
| `types`, `exclude`, `reviewed_only` | 서식: `"all"` · ID 목록 · 그룹. 뺄 서식. 검수 완료 서식만 |
| `per_doc` | 서식마다 서류 수 (문항 수 아님) |
| `conditions` | 촬영 조건 비율 (합 1): `{"clean": 0.5, "scan": 0.2, "photo": 0.15, "fax": 0.15}` |
| `start` | seed 시작. 같은 설정으로 더 만들 때 앞 양만큼 옮김 |
| `fields_per_doc`, `max_keys` | bank: 값 칸 문항 수, kie·marks 한 문항의 최대 항목 수 |
| `page_view`, `nulls` | bank: 여러 쪽 서류에서 한 쪽만 묻는 비율(기본 0.5), 빈 답 배우기 `{"blank": 0.3, "mask": 0.1}` |
| `unit` | ocr: 정답 단위 `word`·`line` |

| 상태 | 할 일 |
|---|---|
| `done` | 출력의 데이터셋 경로를 씀 (studio 목록에도 등록됨) |
| `running` · `interrupted` | 기다림 (`interrupted` 는 studio 가 다시 떴을 뿐 생성은 계속) |
| `failed` | `status` 의 로그 끝을 보고 원인부터. 같은 설정으로 바로 다시 하지 않음 |
| `400 … 모르는 서식` · `이미 있는 폴더입니다` | ID 를 조회해 고침 · 기존 데이터셋을 쓸지 먼저 확인 |

## 3. 만든 뒤 확인

1. **데이터셋 › <이름> › 구성**: 과제별 문항 수가 있고 비어 있지 않은지.
2. **데이터셋 › <이름> › 문항**: **사람이** 그림과 정답(박스)이 맞는지 몇 개 봅니다. 형식 검사 통과는 검수가 아닙니다.

결과 폴더 `<저장 폴더>/workspace/datasets/<이름>/` (학습 서버와 공유):
문항 `tasks/<과제>.jsonl` (ocr 는 `prepared/tasks/`), 한 줄 `{id, task, images, prompt, answer, eval, meta}` (위치 `bbox_2d` 는 0~1000 상대 좌표).
재현 정보는 `dataset.json` (생성기 버전·커밋). 버전이 다른 세트끼리는 점수를 바로 비교하지 않습니다.

## 4. studio 를 거치지 않는 데이터

| 가진 것 | 쓰는 법 (학습 서버) |
|---|---|
| 검수한 실서류 추출 데이터 (ms-swift `.jsonl`) | 학습 설정에 바로: 평가 세트 [sweep.md 2절](../train/sweep.md#2-평가-세트-databenchmark), 학습 데이터 [3절](../train/sweep.md#3-학습-데이터-datatrain) |
| 실서류 이미지 (OCR 학습·평가) | [ocr.md](../train/ocr.md). 실서류 이미지는 외부 모델·서비스에 보내지 않습니다 |
