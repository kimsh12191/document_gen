# 원격 생성 매뉴얼 (`remote_build.py`)

**Research agent가 무엇을 만들지 판단하려면 [Research agent 데이터 생성 가이드](../guide/research-agent.md)를 먼저 읽으세요.** 연구 목적별 과제·서식 선택, 조절 가능한 조건, JSON 레시피 예시, 결과 형식과 한계를 안내합니다. 이 문서는 서버 연결과 실행 방법을 설명합니다.

다른 컨테이너(학습 컨테이너 등)나 PC 에서 studio 에 "이런 데이터를 만들어 줘"를 보내고, 끝날 때까지 기다리는 방법입니다.
생성은 studio 컨테이너가 하고, 결과는 공유 폴더에 생겨 studio 데이터셋에 자동 등록됩니다.

```
[학습 컨테이너 등]  python remote_build.py build …  ──HTTP──▶  [studio 컨테이너 <서버IP>:8765]
                                                                  │ 생성 (Chromium·글꼴)
                     공유 폴더에서 그대로 읽음  ◀──  <저장 폴더>/workspace/datasets/<이름>/
```

## 1. 준비

저장소 루트에서는 아래 `python remote_build.py` 대신 `python docker/remote_build.py`를 사용합니다. 파일 하나만 복사한 경우는 아래 명령 그대로 실행합니다.

서류별 추출 항목·연결 업무는 [통합 카탈로그](catalog.md), 기계용 목록은 [catalog.json](catalog.json), 질문·정답은 [questions.md](questions.md)에서 확인합니다.

1. 서버에서 studio 를 열어 둡니다: `sh docker/studio.sh --open` ([서버 설치·실행](../docker/README.md#3-studio-띄우기)).
2. [`docker/remote_build.py`](../docker/remote_build.py) 파일 하나를 쓰는 쪽에 복사합니다. 파이썬 3.8 이상, 설치할 패키지 없음.
3. 주소를 정해 둡니다. 같은 서버의 다른 컨테이너라도 `localhost` 가 아니라 서버 IP 를 씁니다.

```bash
export STUDIO_URL=http://<서버IP>:8765      # 명령마다 --url 로 줘도 됨
python remote_build.py recipes               # 연결 확인 (저장된 레시피가 나오면 됨)
```

## 2. 무엇을 만들 수 있나

만드는 것은 두 종류(`--track`)입니다.

**`bank` (기본) — 은행 업무 벤치마크.** 두 부분으로 되어 있고, 하나만 만들 수도 있습니다.

| 부분 | 정하는 옵션 | 나오는 과제 |
|---|---|---|
| 서식 문항 (서류 한 장씩) | `--types` 어떤 서식, `--per-doc` 서식마다 몇 장 | `ocr_field`(값 칸 글자), `ocr_page`(전체 받아쓰기), `classify`(서류명), `kie`(항목 값·위치), `marks`(체크·도장·서명) |
| 업무 묶음 (고객 한 명의 서류 여러 장) | `--scenarios` 어떤 업무, `--bundles` 업무마다 고객 수 | `doc_check`(빠진·불필요·타인 서류), `cross_check`(서류 간 불일치), `review`(심사 질문) |

**`ocr` — 합성 OCR.** 서식을 그려 쪽 전체 글자를 정답으로 합니다 (단어·줄 박스). `--types`, `--per-doc`, `--unit` 으로 정합니다.

과제마다 질문·정답 형식과 채점은 [benchmark.md](benchmark.md) "과제" 절에 있습니다.

**평가용(`test`)과 학습용(`train`)** 은 `--split`으로 정하며 서로 다른 고객 seed 범위를 사용합니다. 같은 코드·서식·설정·환경에서 seed로 재현합니다. 이름만 바꿔 같은 설정을 실행하면 새 표본이 되지 않습니다. 추가 생성은 레시피의 `start`를 이전 범위 뒤로 옮깁니다. split이 달라도 서식 자체는 같을 수 있으므로 미지 서식 평가는 별도로 분리하고, 다른 생성 경로를 섞을 때도 중복을 확인합니다.

## 3. 서식·업무 ID 찾기

| 무엇 | 명령 | studio 화면 |
|---|---|---|
| 서식 ID | `python remote_build.py types --find 재직` / `--group income` | 서식: 목록 맨 앞 칸 (예: `employment_certificate`) |
| 서식 그룹 | `types` 출력 맨 아래 | 서식: 그룹 필터 (`identity` 신원·신분, `income` 소득·재직, `hana` 하나은행 원본 …) |
| 업무 ID | `python remote_build.py scenarios` (필요 서류도 보여 줌) | 시나리오·묶음: 업무마다 ID 칸 (예: `mortgage`) |
| 저장된 레시피 | `python remote_build.py recipes` | 데이터셋 › 새로 만들기: 레시피 버튼 |
| 서식별 추출 항목·문항 키·연결 업무 | `python remote_build.py catalog --form employment_certificate` | 서식 › 추출·시나리오 |
| 전체 서류·시나리오·질문 계약 JSON 저장 | `python remote_build.py catalog --out catalog.json` | 사용 가이드 › 서류·추출 카탈로그 |
| 생성한 데이터셋의 업무·시나리오·정답 구조별 구성 | `python remote_build.py composition <데이터셋ID> --out composition.json` | 데이터셋 › 구성·추적 |

Research agent는 `types`로 후보를 좁힌 후 `catalog --form <ID>`에서 필드와 연결 시나리오를 확인합니다. 전체 계획이 필요하면 `catalog --out <새 파일 경로>`로 현재 카탈로그를 저장해 분석합니다. `--out`은 지정 파일을 덮어쓰므로 보관할 스냅샷은 새 이름을 사용하세요. 이 명령은 카탈로그 API가 포함된 최신 Studio가 필요합니다.

## 4. 상황별 예

모두 앞에 `python remote_build.py` 를 붙입니다. `--name` 은 결과 폴더 이름이라 매번 새 이름을 씁니다.

| 하고 싶은 것 | 명령 |
|---|---|
| 평가 세트 통째 (선택된 서식 × 1 + 업무 12종 × 고객 40) | `build --name bench-1021 --recipe bank-bench` |
| 학습 데이터 통째 (서식 × 5 + 업무 × 고객 200) | `build --name train-1021 --recipe bank-train --workers 8 --no-wait` |
| 특정 서식 몇 개만, 여러 장 | `build --name id-5 --types resident_id_card,hf169 --per-doc 5` |
| 한 그룹의 서식만 | `build --name income-3 --types income --per-doc 3` |
| 특정 업무만 | `build --name loan-20 --scenarios mortgage,jeonse_loan --bundles 20` |
| 서식 일부 + 업무 전부, 학습용 | `build --name inc-tr --types income --scenarios all --bundles 10 --split train` |
| 팩스·사진처럼 나쁜 조건만 | `build --name hard --types identity --conditions photo=0.5,fax=0.5` |
| 검수 끝난 서식만 평가 세트로 | `build --name rv-bench --types all --scenarios all --reviewed-only` |
| 합성 OCR 평가 세트 | `build --name ocr-bench-1 --recipe ocr-bench` |
| 합성 OCR, 신분증류만 줄 단위 | `build --name ocr-id --track ocr --types identity --per-doc 2 --unit line` |
| 몇 분짜리 시험 | `build --name try1 --types resident_id_card --scenarios account_opening --bundles 1` |
| studio 에서 저장한 레시피 그대로 | `build --name my-1 --recipe <레시피 이름>` |
| 레시피 JSON 파일을 보내서 | `build --name my-2 --file my.json` |

- `--types` 만 주면 업무 묶음은 빼고, `--scenarios` 만 주면 서식 문항은 뺍니다. 둘 다 주면 둘 다 만듭니다.
- 진행은 `서류 3/40` 같은 숫자로 보입니다. `--no-wait` 로 시작만 했으면 `jobs`, `status <작업ID>` 로 봅니다.
- 걸리는 시간: 평가 세트+학습 데이터 전체가 8코어로 약 1시간 15분입니다. 양이 많으면 `--workers` 로 나눠 그립니다.

## 5. 더 자세한 설정은 studio 에서 레시피로

명령줄 옵션은 자주 쓰는 것만 있습니다. 값 칸 문항 수, 묶음 규칙(빠진·타인·불필요 서류 비율), 대조 사례 켜고 끄기, 업무마다 다른 고객 수 같은 것은
studio **데이터셋 › 새로 만들기 › (은행 업무 / 합성 OCR)** 에서 레시피를 편집해 저장하고, `--recipe <이름>` 으로 만듭니다.
반대로 명령줄 옵션으로 만든 설정은 `remote-<name>` 레시피로 저장되므로 studio 에서 열어 고칠 수 있습니다.

은행 업무 레시피 (studio 화면 항목 ↔ 레시피 JSON ↔ 옵션):

| studio 화면 | 레시피 키 | `build` 옵션 |
|---|---|---|
| 용도 (평가 세트 / 학습) | `split`: `test` · `train` | `--split` |
| 단일 서류 과제에 쓸 서식 | `types`: `"all"` · `["ID", …]` · 그룹 | `--types` |
| 서식마다 샘플 수 | `per_doc` | `--per-doc` |
| 빼는 서식 | `exclude` | `--exclude` |
| 검수 완료 서식만 | `reviewed_only` | `--reviewed-only` |
| 촬영 조건 비율 | `conditions`: `{"clean": 0.5, "scan": 0.2, "photo": 0.15, "fax": 0.15}` | `--conditions` |
| 시나리오와 고객 묶음 수 | `scenarios`, `bundles` (숫자 또는 `{"default": 4, "mortgage": 20}`) | `--scenarios`, `--bundles` (모든 업무 같은 수만) |
| 서류마다 값 칸 OCR 문항 수 | `fields_per_doc` (기본 6) | 레시피에서 |
| kie·marks 문항 하나의 최대 항목 수 | `max_keys` (기본 40) | 레시피에서 |
| seed 시작 | `start` (학습 데이터를 더 만들 때 앞의 양만큼) | 레시피에서 |
| 묶음 규칙 (빠진 서류 0/1/2건, 타인·불필요 서류, 대조 변조) | `bundle`: `{"missing": [0.3, 0.5, 0.2], "other_customer": 0.3, "extra_doc": 0.35, "tamper": 0.5}` | 레시피에서 |
| 대조 사례 켜기·변조 비율 | `cases`: `{"<사례 ID>": {"enabled": true, "tamper": 0.5}}` | 레시피에서 |
| 직접 만든 묶음 | `custom_bundles` | 레시피에서 |

합성 OCR 레시피 (`--track ocr`): `split`(`benchmark` · `train`), `types`, `per_doc`(서식마다 고객 수), `exclude`, `reviewed_only`, `conditions`, `unit`(`word` · `line`),
`heavy`·`special`(내용 많음·특수 상황), `prepare`(예: `{"benchmark_fraction": 0.1}` 학습 데이터에서 평가로 떼어 둘 비율), `start`. 형식 전체는 `docgen/ocr_set.py` 머리말.

레시피 파일 예 (`--file my.json`):

```json
{
 "about": "주담대 집중 평가 세트",
 "track": "bank",
 "split": "test",
 "types": ["real_estate_registry", "building_register", "sales_contract"],
 "per_doc": 3,
 "scenarios": ["mortgage", "jeonse_loan"],
 "bundles": {"default": 10, "mortgage": 30},
 "bundle": {"missing": [0.5, 0.4, 0.1], "other_customer": 0.2, "extra_doc": 0.2, "tamper": 0.5}
}
```

## 6. 결과

`build` 가 끝나면 결과 폴더를 컨테이너 안 경로와 서버 경로로 함께 보여 줍니다. 언제든 `python remote_build.py paths` 로 볼 수 있습니다.

데이터셋은 **저장 폴더**(`sh docker/studio.sh --data <폴더>`로 정한 곳, [서버 설치·실행](../docker/README.md#3-studio-띄우기)) 아래 `workspace/datasets/<name>/`에 생깁니다. 예: `/database/docgen_studio/workspace/datasets/<name>/`.
컨테이너 안에서는 같은 곳이 `/out/workspace/datasets/<name>/` 로 보입니다.

| 은행 업무 (`bank`) | 내용 |
|---|---|
| `tasks/<과제>.jsonl` | 문항: 이미지·질문·정답 (학습·평가가 읽는 것) |
| `images/`, `images/bundles/`, `crops/` | 서류 이미지, 업무 묶음 이미지, 값 칸 잘라낸 이미지 |
| `bundles.jsonl` | 업무 묶음마다 고객·서류·변조 내역 |
| `swift/` | (`--split train` 만) 학습용 대화 레코드 |
| `meta.json`, `dataset.json` | 만든 설정·문항 수, 레시피·생성기 커밋·서식 해시 (다시 만들 때 근거) |

- studio 데이터셋에서 문항 이미지·질문·정답을 보고, 모델 답을 붙여 채점합니다.
- 생성 후 `python remote_build.py composition <데이터셋ID>`로 전체/평가 문항 구성을 조회합니다. 같은 분류가 train의 구분별 보고서까지 이어집니다. [벤치마크 구성·추적](benchmark-tracking.md)에 필드·파일 규격과 이전 데이터 처리 방법을 정리했습니다.
- 학습에 쓰는 법: [학습 연결 안내](../studio/TRAINING.md). 학습 컨테이너에서 경로가 다르면 studio 설정의 `path_map`.

## 7. 문제가 생기면

| 증상 | 할 일 |
|---|---|
| `연결하지 못했습니다` | 서버에서 `sh docker/studio.sh --open` 했는지, 주소가 서버 IP·포트인지 (`localhost` 아님), 방화벽 |
| 만든 데이터셋을 못 찾음 | `paths` 로 위치 확인. 서버에서 `sh docker/studio.sh` 를 하면 끝에 저장 폴더가 나옴 |
| `400 … 모르는 서식·그룹` / `모르는 시나리오` | `types`·`scenarios` 로 ID 를 확인. 시작 전에 거절하므로 아무것도 만들어지지 않음 |
| `이미 있는 폴더입니다` | `--name` 을 바꿈 (만든 데이터셋은 덮어쓰지 않음) |
| `interrupted` 가 보임 | studio 가 다시 떴을 뿐 생성은 계속됨. `remote_build.py` 는 끝까지 기다림 |
| `failed` | 출력 끝의 로그를 봄. 같은 내용: `status <작업ID>`, studio 작업 |
| 너무 오래 걸림 | `--workers` 를 서버 코어 수 안에서 늘림. 먼저 작은 시험(`try1` 예)으로 확인 |
| 그만두기 | studio 작업에서 취소 (또는 `curl -X POST $STUDIO_URL/api/jobs/<작업ID>/cancel`) |
| 다 쓴 데이터셋 지우기 | studio 데이터셋에서 등록 해제 후 서버에서 폴더 삭제 |
