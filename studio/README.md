# studio — 개발자용

**화면 쓰는 법은 [guide/studio.md](../guide/studio.md)** (서식 · 새 서식 추가 · 데이터셋). 이 문서는 띄우는 법, 화면 ↔ 코드, 고친 것이 저장되는 파일입니다.
설계 기록은 [DESIGN.md](DESIGN.md), 예전 이 문서 전체(숨긴 화면 설명 포함)는 [archive/studio/README_2026-11.md](../archive/studio/README_2026-11.md).

## 띄우기

```bash
pip install -r requirements.txt -r studio/requirements.txt
python -m studio                      # → http://localhost:8765
python -m studio --host 0.0.0.0       # 서버에서 띄우고 다른 PC 브라우저로 접속할 때
sh docker/studio.sh --data /database/docgen_studio   # 내부망 도커 (처음 한 번 저장 폴더 지정) — docker/README.md 3절
```

- **설정:** `studio/config.json` (git 제외, 없어도 됨). 사내 OCR 연결, 브라우저 경로, `private_forms_dir`, 학습 컨테이너 `path_map` 처럼 환경마다 다른 것만. 예시 [config.example.json](config.example.json).
- **렌더링 브라우저:** Playwright Chromium → 설정 `browser` → `CHROMIUM_PATH` → 이 PC 의 Chrome·Edge 순. 없으면 렌더링(미리보기·생성)만 꺼짐.
- **도커:** 데이터셋은 `<저장 폴더>/workspace/datasets/<이름>/`. 코드는 마운트라 고치면 studio 가 저절로 다시 뜸. 다른 컨테이너에서 생성 맡기기 `docker/remote_build.py` ([guide/data.md](../guide/data.md)).
- 이 PC 에서 만든 그림은 글꼴이 서버와 다를 수 있습니다. 학습·평가 데이터는 서버나 도커에서 만듭니다.
- 미리보기 캐시 `studio_cache/preview/` (git 제외). 서식 파일·공통 렌더링 코드가 바뀌면 다시 그림.

## 화면 ↔ 코드

| 메뉴 | 화면 (`static/js/`) | 서버 |
|---|---|---|
| 서식 | `forms.js` (목록·상세 탭), `review.js`, `questions.js`, `editor.js` (영역 편집), `html-spots.js` (자리·템플릿), `htmled.js` | `catalog.py`, `editor.py`, `spots.py`, `questions.py`, `api_html.py` |
| 새 서식 추가 | `new-forms.js` (A 그림 위에 그리기, B html 안내) | `drawn.py` (`POST /api/forms/new-image`), `generators.py` (생성 방법 고르기 창) |
| 데이터셋 | `datasets.js`, `recipes.js`, `dataset-builds.js` (생성 현황), `dataset-tracking.js` | `datasets.py`·`api_datasets.py`, `bank_data.py`·`api_bank.py`, `ocr_data.py`, `build_registration.py`, `training_link.py`, `jobs.py` |
| 시나리오·묶음 | `scenarios.js`, `scenario-preview.js`, `scenario-processing.js` | `bank_data.py`, `scenario_processing.py` |
| 키 사전 · 표시 요소 | `keys.js`, `keypick.js` · `marks.js` | `api_dictionary.py`·`api_keys.py` · `marks_admin.py` |
| 사용 가이드 · OCR 예시 | `guide.js` · `ocr-examples.js` | `guidebook.py` (문서 목록 `DOCUMENTS`) |

**숨긴 화면** (메뉴에 없음, 주소로 열림, 지금 쓰지 않음): 가져오기 `#/import`, 검수 `#/review`, 평가 `#/eval`, 작업 `#/jobs`, 설정 `#/settings`,
서식 초안 `#/form-draft`, 실문서 벤치마크 `#/real-bench`. 설명은 [예전 문서](../archive/studio/README_2026-11.md).

## 고친 것이 저장되는 곳

모두 저장소 안 파일이라 `git diff` 로 검토합니다 (실서류 견본에서 만든 서식만 `private_forms_dir`).

| 고친 것 | 파일 | 생성기가 읽는 곳 |
|---|---|---|
| 영역·키·항목명·값 출처·배경 지우기 (overlay·html 공통) | 서식 폴더의 칸 목록 `docgen/forms/<ID>/fields.json` (실서류에서 만든 서식은 `private_forms_dir/<ID>/fields.json`). 서식 파일 전부 `python -m docgen.formdir path <ID>` | `docgen/formfields.py` → overlay `docgen/overrides.py`·`realform.py`, html `docgen/html_regions.py`·`htmlform.py` |
| 가져온 서식 (공개 서식 묶음) | `docgen/forms/img_*/` (`layout.json`, `look/page_<n>.png`) — 실서류 묶음에서 만든 것은 `private_forms_dir/img_*/` (저장소 밖) | `docgen/realform.py` `register_images` |
| 검수·배정·메모·문제 표시 | `docgen/catalog.json` | `docgen/bench/build.py` (학습 데이터에서 평가 전용 서식 빼기) |
| 표시 요소 확률 | `docgen/forms/_common/marks.json` | `docgen/marks.py` |
| 표시 요소 풀 | `docgen/assets/marks/pools.json`, `docgen/assets/marks/<풀>/` | `docgen/marks.py` → `realform.py`·`render.py` |
| 표준 키 사전 (자동 생성) | `docgen/forms/_common/keys.json` (`python docgen/scripts/build_keys.py`) | studio 의 키 고르기 |
| 키 사전 (칸의 누구의·무엇, 문서명, 키 규칙·값 종류) | `docgen/forms/_common/dictionary/*.json`, `docgen/forms/_common/key_rules.json` | `docgen/dictionary.py`, `docgen/keyrules.py` |
| 질문·답 (studio 는 보기만, 파일로 고침) | 칸마다 `fields.json` 의 `q`, 이 서식만 다르게 `docgen/forms/<ID>/questions.json`, 이 서식만의 질문 `qa.py`, 기본 `docgen/forms/_common/questions.json` ([서식 폴더 설명서 5절](../docgen/forms/README.md#5-질문과-답-고치기)) | `docgen/bench/prompts.py`, `docgen/bench/tasks/<과제>.py` |

검수 완료 전의 그린·가져온 서식(`img_*`)은 레시피의 `"all"`·그룹 선택에 들어가지 않습니다 (ID 를 직접 적으면 시험용으로 들어감).

## 구조

```
studio/
  __main__.py     python -m studio (uvicorn 실행)
  app.py          FastAPI: /api/* 와 정적 파일
  catalog.py      서식 목록·상세, 검수·배정·문제 표시 (docgen/catalog.json), 서식 다시 읽기, 카드 FORM.md
  config.py       설정 읽기, 렌더링 브라우저 찾기
  questions.py    ① 질문·답 › 실제 문항: 실제 생성기로 만든 문항과 모델 답 예시
  guidebook.py    사용 가이드 화면의 문서 목록(DOCUMENTS·MANUALS)과 카탈로그 (python -m studio.guidebook)
  api_dictionary.py·api_keys.py  키 사전 API (docgen/forms/_common/dictionary/, key_rules.json)
  editor.py       overlay 영역 편집기: 레이아웃 보기, 사람 수정 검사·저장, 검수 전 자동 검사
  spots.py        html·코드 서식의 자리·템플릿 화면: 모든 자리와 정한 곳(템플릿 줄·fields.json 줄), 템플릿 초안의 키 전후 비교·저장, 값 출처 저장
  marks_admin.py  표시 요소 확률·풀 읽고 쓰기
  datasets.py     데이터셋 등록부, 문항 보기, 모델 답, 채점, 설명서 (api_datasets.py 가 API)
  bank_data.py    레시피, 은행 업무 빌드, 업무 묶음 보기·고객 일관성 검사, 시나리오 편집 (api_bank.py 가 API)
  training_link.py 학습 설정 쓰기, 학습 기록, 진행 읽기, 결과 자동 붙이기
  ocr_data.py     합성 OCR 레시피·빌드
  importer.py     ④ 가져오기: 묶음, 쪽 목록, 사내 OCR(OCR 준비 규칙), 묶기·합치기·떼기·결정, 템플릿·값 자리 초안, OCR 세트 (api_import.py 가 API)
  formats.py      포맷·양식 지문과 묶기 (masking_ui 6f5bca6 에서 옮김)
  ocr_review.py   ⑤ OCR 검수: 검수본 읽고 쓰기, 사내 OCR 오류 통계
  results.py      ④ 결과 폴더 검사·가져오기 (python -m studio.results check)
  label_review.py ⑤ 라벨 검수: 키 대응, 문서 검수, v1 라벨로 내보내기, 같은 자리 모아 보기, 의심 먼저, 검수 전 점수, 업무 묶음 (api_review.py 가 API)
  analyzers.py    ⑧ 분석기: 설정·연결 확인, 작업 폴더·지시문, 명령 틀, openai 실행, 결과 검사, 승인 (api_html.py 가 API, 지시문 틀은 analyzer_tasks/)
  api_html.py     ① html 편집·복제, ⑧ 분석기 API
  labeled_data.py 표준 라벨 검사·원본 해시/복사·은행 업무/OCR 변환 (api_labels.py가 API)
  labeled_bundles.py 실제 라벨 묶음의 구비·직접 추출/비교·계산 문항 (합성 변조 없음)
  jobs.py         백그라운드 작업 (명령줄과 같은 명령, <workspace>/jobs/)
  build_registration.py  ⑥ 생성 현황: 끝난 데이터셋 자동 등록
  scenario_processing.py ③ 처리 설정 예시 실행
  intake*.py      ④ 서류 넣기 (만드는 중, 아래)   form_draft.py·real_benchmark.py  숨긴 메뉴 (서식 초안·실문서 벤치마크)
  deps.py         내부망 컨테이너용 패키지 설치 (python -m studio.deps download | install)
  wheels/         그 설치 파일 (Linux, 파이썬 3.12)
  static/         화면 (index.html, style.css, js/<메뉴>.js — 빌드 없음, 외부 CDN 없음)
docgen/preview.py 서식 하나 렌더링 (브라우저 전용 스레드, 결과 캐시)
```

## 테스트

```bash
python -m pytest studio/tests
```
