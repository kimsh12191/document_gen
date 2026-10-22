# Research agent 데이터 생성 가이드

이 프로젝트는 은행 서류의 합성 이미지와 정답을 만든다. Research agent는 연구 목적에 맞는 서식·과제·난이도·수량을 선택하고, JSON 레시피를 Studio에 보내 데이터를 생성할 수 있다. Studio 화면을 조작할 필요는 없다.

이 문서는 **무엇을 만들 수 있는지와 선택 방법**을 설명한다. 서버 준비·명령 옵션·장애 해결은 [원격 생성 매뉴얼](remote-build.md)을 참고한다. 아래 명령은 저장소 루트 기준이다.

## 1. 연구 목적에 맞는 생성 경로 선택

| 연구 목적 | 생성 경로 | 입력 이미지와 질문 | 정답 | 선택할 설정 |
|---|---|---|---|---|
| 서류 분류 | `bank` / `classify` | 서류 이미지 + 종류 질문 | 문서명 | `types`, `per_doc` |
| 항목 값·위치 추출 | `bank` / `kie` | 서류 이미지 + 추출 항목 목록 | 항목별 키·값·위치 | `types`, `per_doc`, `max_keys` |
| 체크·도장·서명 인식 | `bank` / `marks` | 해당 표시가 있는 서류 + 항목 질문 | 체크 상태·도장/서명 여부·위치 | 해당 항목이 있는 `types`, `per_doc` |
| 값 칸 글자 읽기 | `bank` / `ocr_field` | 값 칸을 잘라낸 이미지 | 글자 | `types`, `per_doc`, `fields_per_doc` |
| 서류에 채운 값 읽기 | `bank` / `ocr_page` | 서류 이미지 | 보이는 값 필드의 문자열 목록 | `types`, `per_doc` |
| 제출 서류 구비 확인 | `bank` / `doc_check` | 같은 고객의 제출 서류 묶음 + 필수 목록 | 누락·불필요·타인 서류 | `scenarios`, `bundles`, `bundle` |
| 서류 사이 불일치 찾기 | `bank` / `cross_check` | 비교할 서류 2~3건 | 불일치 여부·문제 서류·항목·값 | `scenarios`, `bundles`, `cases` |
| 서류를 근거로 계산·판단 | `bank` / `review` | 관련 서류 + 구현된 심사 질문 | 숫자 또는 예/아니오 등 | `scenarios`, `bundles` |
| 쪽 전체 OCR·글자 위치·공간 관계 | `ocr` / 아래 8과제 | 페이지·영역·잘린 이미지 + 과제별 질문 | 글자 또는 글자·위치 목록 | `types`, `per_doc`, `unit`, `prepare` |

`bank`의 `ocr_page`는 고정 인쇄 문구까지 포함한 완전한 페이지 전사가 아니다. 전체 글자와 위치가 필요하면 `ocr` 경로를 선택한다.

`bank`는 단일 서류를 만들 때 관련 과제를 함께 생성한다. 특정 과제만 필요하면 생성 후 `tasks/kie.jsonl`처럼 해당 과제 파일을 선택한다. `bank` 레시피에 임의의 `tasks` 키를 추가하지 않는다. 표시나 유효한 값이 없는 서식에서는 일부 과제가 생성되지 않을 수 있다.

### OCR 8과제

**Studio의 OCR 예시 메뉴**에서 아래 8과제의 입력 이미지·질문·모델 답과 정답 위치 표시를 바로 확인할 수 있다. [예시 화면 안내](ocr-examples.md), [동일한 문서 예시](tasks.md#ocr-과제)를 참고한다. 데이터셋 생성·등록 없이 열 수 있다.

| 과제 ID | 무엇을 배우거나 평가하나 | 정답 |
|---|---|---|
| `crop_ocr` | 잘린 이미지 글자 읽기 | 문자열 |
| `bbox_ocr` | 지정한 좌표 안의 글자 읽기 | 문자열 |
| `region_ocr` | 지정 영역의 여러 줄 읽기 | 줄바꿈이 있는 문자열 |
| `grounding` | 지정한 글자의 모든 위치 찾기 | 글자·박스 목록, 없으면 `[]` |
| `spotting` | 이미지의 전체 글자와 위치 찾기 | 읽기 순서의 글자·박스 목록 |
| `relation` | 기준 글자의 위·아래·왼쪽·오른쪽 글자 찾기 | 글자·박스 목록 |
| `marked_ocr` | 색 박스로 표시한 글자 읽기 | 문자열 |
| `marked_box` | 색 박스의 위치와 글자 찾기 | 글자·박스 목록 |

실제 질문과 정답 예시는 [tasks.md](tasks.md), 질문 원본은 [ocr_tasks.py](../docgen/bench/ocr_tasks.py)에 있다.

## 2. 어떤 문서와 업무를 선택할 수 있나

**[통합 카탈로그](catalog.md)**에 모든 서류의 원본 필드·공통 문항 키·연결 업무·추출/비교 설정을 모았다. 기계용은 **[catalog.json](catalog.json)**이다. Studio에서도 사용 가이드와 서식 상세의 추출·시나리오 탭에서 같은 구조의 현재 내용을 확인한다.

종수나 ID를 추측하지 말고 연결한 Studio에서 현재 목록을 조회한다. Studio에서 추가·수정한 서식과 시나리오가 있을 수 있다.

```powershell
$env:STUDIO_URL = "http://<서버IP>:8765"
python docker/remote_build.py types
python docker/remote_build.py types --find 재직
python docker/remote_build.py types --group income
python docker/remote_build.py catalog --form employment_certificate
python docker/remote_build.py catalog --out research-catalog.json
python docker/remote_build.py scenarios
python docker/remote_build.py recipes
```

| 찾는 자료 | 예시 | 선택 방법 |
|---|---|---|
| 신원·신분 서류 | 신분증, 등·초본, 가족관계증명서 | `types`로 서식 ID·그룹 확인 |
| 소득·재직 서류 | 소득금액증명, 급여명세서, 재직증명서 | `types --group income` |
| 사업자·법인 서류 | 사업자등록증, 법인등기, 재무제표 | `types --find <검색어>` |
| 부동산 서류 | 등기부, 건축물대장, 매매·임대차계약 | `types --find <검색어>` |
| 은행 서식 | 대출신청서, 약정서, 고객확인서 | `types --find <검색어>` |
| 외환·무역 서류 | 송장, 송금신청서 등 | `types --group fx` |
| 같은 고객의 업무 묶음 | 주택담보·전세·개인신용·법인대출, 계좌개설, 해외송금 등 | `scenarios`로 ID와 필요 서류 확인 |

서류별 생성 필드·타입은 [fields/](fields/README.md), 기계가 읽을 전체 목록은 [fields.json](fields/fields.json)을 참고한다. KIE에 쓰는 공통 키는 [키 사전 구현](../docgen/dictionary)과 실제 생성 문항으로 확인한다. 필드 목록의 원래 키와 문항의 공통 키가 다를 수 있다.

업무 묶음은 같은 가상 고객의 이름·주소·소득 등을 공유한다. 서로 일치하는 서류, 누락된 서류, 타인 서류, 의도적으로 불일치하게 바꾼 서류를 만들 수 있다. 지원하는 대조 사례와 근거는 [benchmark.md](benchmark.md), 정확한 사례 ID는 [cases.py의 CASES](../docgen/bench/cases.py)에 있다. 예: `income_inflated`(소득 부풀리기), `lease_owner`(임대인·소유자 불일치), `format_only`(표기만 다른 정상 사례).

## 3. 무엇을 얼마나 조절할 수 있나

| 조절 대상 | 레시피 설정 | 의미·주의점 |
|---|---|---|
| 문서 선택 | `types`, `exclude`, `reviewed_only` | ID·그룹 또는 `"all"`; 검수 완료 서식만 선택 가능 |
| 단일 서류 수 | `per_doc` | 서식당 고객/문서 건수. 페이지 수나 문항 수가 아님 |
| 업무 묶음 수 | `scenarios`, `bundles` | 업무당 고객 묶음 수. 업무별 다른 수량도 가능 |
| 학습/평가 | `split` | bank: `train`/`test`, OCR: `train`/`benchmark` |
| 촬영 조건 | `conditions` | `clean`, `scan`, `photo`, `fax`의 비율. 합은 1 |
| 추가 생성 | `start` | seed 오프셋. 같은 설정을 이름만 바꿔 실행하면 새 표본이 되지 않음 |
| 값 칸 문항 수 | bank: `fields_per_doc` | 서류당 최대 샘플 수. 읽을 수 있는 필드 수에 따라 적어질 수 있음 |
| 추출 항목 수 | bank: `max_keys` | KIE·marks 문항의 최대 항목 수. 특정 키를 지정하는 옵션은 아님 |
| 서류 누락·혼입 | bank: `bundle` | 누락 0/1/2건 비율, 타인·불필요 서류 확률 |
| 대조 사례 | bank: `cases` | 사례별 `enabled`, `tamper` 설정. 지정하지 않은 사례는 기본 설정 유지 |
| 직접 구성한 묶음 | bank: `custom_bundles` | 상세 구조는 [레시피 로더·묶음 생성 코드](../docgen/bench/build.py) 확인 |
| OCR 정답 단위 | OCR: `unit` | `word` 또는 `line` |
| OCR 복잡한 내용·특수 상황 | OCR: `heavy`, `special` | `default`/`on`/`off` |
| OCR 과제별 수·분리·필터 | OCR: `prepare` | [설정 예시](../docgen/bench/ocr_config.example.json)의 준비 설정 덮어쓰기 |

OCR의 `prepare.tasks_per_view`는 split별·과제별 문항 수를 정한다. 실제 출력 수는 글자·배치·필터 조건에 따라 달라진다. 학습 샘플링 비율은 `prepare.task_mix`도 함께 확인한다.

**수량 계획:** 서식 3종에 `per_doc: 10`이면 단일 서류 30건이다. 업무 2종에 `bundles: 10`이면 고객 묶음 20건이다. 한 문서가 여러 쪽이고 한 문서/묶음에서 여러 문항이 나오므로 “문항 1,000개”가 필요하면 먼저 소량 생성으로 실제 수를 확인한 후 규모를 정한다. 촬영 조건과 변조 비율도 소량에서 정확한 개수가 보장되는 설정은 아니다.

## 4. 목적을 레시피로 바꾸는 예

### A. 소득 서류의 값·위치 추출 학습

아래 JSON을 UTF-8로 `income-pilot.json`에 저장한다. 서식당 2건을 먼저 만들고 `tasks/kie.jsonl`을 확인한다.

```json
{
  "about": "소득 서류 값·위치 추출 소량 확인",
  "track": "bank",
  "split": "train",
  "types": ["income"],
  "per_doc": 2,
  "scenarios": [],
  "bundles": 0,
  "max_keys": 40,
  "conditions": {"clean": 0.5, "scan": 0.5},
  "start": 0
}
```

```powershell
python docker/remote_build.py build --name income-pilot-001 --file income-pilot.json
```

### B. 전세대출 서류 대조 평가

`lease_owner` 사례를 변조 확률 0.5로 설정한다. 그 밖의 대조 사례는 기본 설정으로 함께 생성된다. 임대인 불일치만 필요하면 결과의 문항 메타데이터를 확인해 선별하거나, 다른 사례의 `enabled`를 명시적으로 끈다.

```json
{
  "about": "전세대출 서류 대조 평가 소량 확인",
  "track": "bank",
  "split": "test",
  "types": [],
  "per_doc": 0,
  "scenarios": ["jeonse_loan"],
  "bundles": 2,
  "cases": {"lease_owner": {"enabled": true, "tamper": 0.5}},
  "conditions": {"clean": 1.0}
}
```

같은 방식으로 파일을 저장하고 `build --name lease-pilot-001 --file <파일>`을 실행한다. 이 묶음에서 `doc_check`, `cross_check`, `review`가 함께 나올 수 있으며, 필요한 것은 `tasks/cross_check.jsonl`에서 읽는다.

### C. 촬영된 신원 서류의 전체 OCR·위치 평가

```json
{
  "about": "사진·팩스 조건 OCR 평가 소량 확인",
  "track": "ocr",
  "split": "benchmark",
  "types": ["identity"],
  "per_doc": 2,
  "unit": "line",
  "conditions": {"photo": 0.5, "fax": 0.5}
}
```

출력의 `prepared/tasks/spotting.jsonl` 등이 문항 파일이다. OCR 학습용이면 `split`을 `train`으로 바꾸고, `prepared` 안 문항의 `meta.split`으로 train/val/benchmark를 구분한다.

## 5. 생성 결과를 연구에 가져가기

생성 구성은 **데이터셋 → 구성·추적**에서 업무·시나리오·정답 구조별로 확인한다. 같은 분류가 train의 구분별 평가 보고서로 이어진다. [벤치마크 구성·추적](benchmark-tracking.md)에 메타데이터와 보고서 파일 규격을 정리했다.

생성하려면 Studio가 실행 중이고 에이전트에서 서버로 HTTP 요청이 가능해야 한다. 결과를 읽으려면 공유 볼륨 접근 또는 별도 파일 복사 경로도 필요하다. 원격 생성 도구는 생성·진행 확인·경로 안내를 제공하며 결과 ZIP을 자동으로 내려받는 도구는 아니다.

```powershell
python docker/remote_build.py paths
python docker/remote_build.py jobs
python docker/remote_build.py status <작업ID>
```

| 결과 | bank | OCR |
|---|---|---|
| 이미지·질문·정답 문항 | `<결과>/tasks/<과제>.jsonl` | `<결과>/prepared/tasks/<과제>.jsonl` |
| 공통 문항 형식 | `id`, `task`, `images`, `prompt`, `answer`, `eval`, `meta` | 동일 |
| 이미지 경로 기준 | `<결과>/` | `<결과>/prepared/` 기준으로 해석. 절대 경로가 있으면 접근 가능 여부 확인 |
| 학습용 대화 | `swift/` (`split: train`) | `prepared/train_sft.jsonl`, `val_sft.jsonl` |
| 설정·수량·재현 근거 | `meta.json`, `dataset.json` | `ocr_set.json`, `config.json`, `prepared/meta.json` |

질문·정답·좌표의 실제 규격은 [과제 예시](tasks.md)와 [질문 문장](questions.md)을 기준으로 한다. 위치 답의 `bbox_2d`는 0~1000 상대 좌표이고, bank KIE·marks의 `page`는 1부터다. 원본 라벨의 픽셀 좌표·0부터 시작하는 page와 혼동하지 않는다.

생성 후에는 다음을 확인한다.

1. 작업이 `done`인지 확인하고, 필요한 과제 파일이 비어 있지 않은지와 실제 문항 수를 센다.
2. 일부 문항의 이미지와 정답을 함께 확인한다. 선택한 서식에 필요한 필드·표시가 있는지 확인한다.
3. 학습/평가의 고객·서식 분리와 중복을 확인한다. 서로 다른 split의 seed 정책만으로 미지 서식 평가까지 보장되지는 않는다. OCR과 bank를 섞을 때도 중복 여부를 별도로 확인한다.
4. 다른 포맷이 필요하면 별도 출력으로 변환하고 이미지 경로를 함께 옮긴다. 질문·정답 의미와 좌표 변환을 보존한다.
5. 사용한 레시피, 생성기 커밋·서식 해시, 원본 데이터셋 위치, 실제 과제별 수량, 필터·변환 내용을 기록한다. 소량 결과를 확인한 후 본 생성 규모를 늘린다.

## 6. 설정으로 만들 수 없는 요구

- **새로운 서류 양식:** 기존 목록에 없으면 서식을 추가해야 한다. [템플릿 추가 가이드](../docgen/manual/TEMPLATE_GUIDE.md)를 참고한다.
- **새로운 심사 질문·대조 규칙:** 자유로운 자연어 요청을 자동으로 실행 규칙으로 바꾸지는 않는다. 해당 생성·정답·채점 로직을 추가해야 한다.
- **특정 필드값·사건의 정확한 개수 강제:** 위 레시피 옵션이 모든 값과 분포를 제어하지는 않는다. 현재 설정으로 표현 가능한지 코드를 확인하고, 부족하면 선별 또는 생성 로직 확장이 필요하다.
- **임의의 학습 포맷:** 기본 출력 이후 변환이 필요하다. 변환한 파일만 복사해서 이미지 경로가 끊기지 않게 한다.
- **실제 고객 데이터·현실 성능 보장:** 이 경로에서 생성하는 것은 합성 데이터다. 실서류를 가진 경우의 가져오기는 [DATA_IMPORT.md](../studio/DATA_IMPORT.md)를 따른다.

## 7. Research agent에 넘길 지시 예시

> `guide/research-agent.md`를 먼저 읽고 연구 목적에 맞는 데이터 계획을 세워라. 현재 Studio의 서식·시나리오를 조회하고, 필요한 과제·서식·난이도·학습/평가 분리·수량·최종 포맷을 정하라. 선택 근거와 지원되지 않는 요구를 명시하라. JSON 레시피로 소량 생성해 이미지·정답·문항 수를 확인한 뒤 본 데이터를 생성하라. 결과 경로와 이미지 접근을 검증하고, 사용 레시피·재현 정보·필터·포맷 변환 내용을 함께 남겨라.
