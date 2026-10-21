# 원격 생성 매뉴얼 (`remote_build.py`)

다른 컨테이너(학습 컨테이너 등)나 PC 에서 studio 에 "이런 데이터를 만들어 줘"를 보내고, 끝날 때까지 기다리는 방법입니다.
생성은 studio 컨테이너가 하고, 결과는 공유 폴더에 생겨 studio ⑥ 데이터셋에 자동 등록됩니다.

```
[학습 컨테이너 등]  python remote_build.py build …  ──HTTP──▶  [studio 컨테이너 <서버IP>:8765]
                                                                  │ 생성 (Chromium·글꼴)
                     공유 폴더에서 그대로 읽음  ◀──  /out/studio_workspace/datasets/<이름>/
```

## 1. 준비

1. 서버에서 studio 를 열어 둡니다: `sh docker/studio.sh --open` ([README 3절](README.md#3-studio-띄우기)).
2. [`docker/remote_build.py`](remote_build.py) 파일 하나를 쓰는 쪽에 복사합니다. 파이썬 3.8 이상, 설치할 패키지 없음.
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

과제마다 질문·정답 형식과 채점은 [guide/benchmark.md](../guide/benchmark.md) "과제" 절에 있습니다.

**평가용(`test`)과 학습용(`train`)** 은 `--split` 으로 정합니다. 둘은 seed 범위가 달라 같은 서류가 겹치지 않으므로, 학습 데이터로 평가 세트를 오염시키지 않습니다. 같은 설정이면 언제 만들어도 같은 결과가 나옵니다.

## 3. 서식·업무 ID 찾기

| 무엇 | 명령 | studio 화면 |
|---|---|---|
| 서식 ID | `python remote_build.py types --find 재직` / `--group income` | ① 서식: 목록 맨 앞 칸 (예: `employment_certificate`) |
| 서식 그룹 | `types` 출력 맨 아래 | ① 서식: 그룹 필터 (`identity` 신원·신분, `income` 소득·재직, `hana` 하나은행 원본 …) |
| 업무 ID | `python remote_build.py scenarios` (필요 서류도 보여 줌) | ③ 시나리오: 업무마다 ID 칸 (예: `mortgage`) |
| 저장된 레시피 | `python remote_build.py recipes` | ⑥ 데이터셋 › 새로 만들기: 레시피 버튼 |

## 4. 상황별 예

모두 앞에 `python remote_build.py` 를 붙입니다. `--name` 은 결과 폴더 이름이라 매번 새 이름을 씁니다.

| 하고 싶은 것 | 명령 |
|---|---|
| 평가 세트 통째 (서식 476종 × 1 + 업무 12종 × 고객 40) | `build --name bench-1021 --recipe bank-bench` |
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
studio **⑥ 데이터셋 › 새로 만들기 › (은행 업무 / 합성 OCR)** 에서 레시피를 편집해 저장하고, `--recipe <이름>` 으로 만듭니다.
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

| studio 설정 (`studio/config.json`) | 데이터셋 위치 (서버) |
|---|---|
| `"workspace_dir": "/out/studio_workspace"` (권장, [README 2절](README.md#2-내부망-서버-처음-한-번)) | `~/docgen/data/studio_workspace/datasets/<name>/` |
| 설정 없음 | 코드 폴더 안 `~/docgen/document_gen/studio_workspace/datasets/<name>/` (학습 컨테이너와 공유 안 됨) |

컨테이너 안 `/out` = 서버의 `~/docgen/data`, `/home/docgen/document_gen` = 서버의 저장소 폴더입니다. 학습 컨테이너에서 같은 폴더가 다른 경로로 보이면 그 경로로 바꿔 씁니다 (studio 가 내보내는 학습 설정은 `path_map` 으로 자동).

| 은행 업무 (`bank`) | 내용 |
|---|---|
| `tasks/<과제>.jsonl` | 문항: 이미지·질문·정답 (학습·평가가 읽는 것) |
| `images/`, `images/bundles/`, `crops/` | 서류 이미지, 업무 묶음 이미지, 값 칸 잘라낸 이미지 |
| `bundles.jsonl` | 업무 묶음마다 고객·서류·변조 내역 |
| `swift/` | (`--split train` 만) 학습용 대화 레코드 |
| `meta.json`, `dataset.json` | 만든 설정·문항 수, 레시피·생성기 커밋·서식 해시 (다시 만들 때 근거) |

- studio ⑥ 데이터셋에서 문항 이미지·질문·정답을 보고, 모델 답을 붙여 채점합니다.
- 학습에 쓰는 법: [studio/TRAINING.md](../studio/TRAINING.md). 학습 컨테이너에서 경로가 다르면 studio 설정의 `path_map`.

## 7. 문제가 생기면

| 증상 | 할 일 |
|---|---|
| `연결하지 못했습니다` | 서버에서 `sh docker/studio.sh --open` 했는지, 주소가 서버 IP·포트인지 (`localhost` 아님), 방화벽 |
| 만든 데이터셋을 못 찾음 | `paths` 로 위치 확인. `studio/config.json` 이 없으면 코드 폴더 안에 생김 (위 6절 표) |
| `400 … 모르는 서식·그룹` / `모르는 시나리오` | `types`·`scenarios` 로 ID 를 확인. 시작 전에 거절하므로 아무것도 만들어지지 않음 |
| `이미 있는 폴더입니다` | `--name` 을 바꿈 (만든 데이터셋은 덮어쓰지 않음) |
| `interrupted` 가 보임 | studio 가 다시 떴을 뿐 생성은 계속됨. `remote_build.py` 는 끝까지 기다림 |
| `failed` | 출력 끝의 로그를 봄. 같은 내용: `status <작업ID>`, studio ⑧ 작업 |
| 너무 오래 걸림 | `--workers` 를 서버 코어 수 안에서 늘림. 먼저 작은 시험(`try1` 예)으로 확인 |
| 그만두기 | studio ⑧ 작업에서 취소 (또는 `curl -X POST $STUDIO_URL/api/jobs/<작업ID>/cancel`) |
| 다 쓴 데이터셋 지우기 | studio ⑥ 데이터셋에서 등록 해제 후 서버에서 폴더 삭제 |
