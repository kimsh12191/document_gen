# studio — 개발자용

**화면 쓰는 법은 [guide/studio/studio.md](../guide/studio/studio.md)** (서식 · 새 서식 추가 · 데이터셋). 이 문서는 띄우는 법, 화면 ↔ 코드, 고친 것이 저장되는 파일입니다.
지금 남은 화면은 서식(overlay 영역 편집·미리보기·검수), 새 서식 추가(overlay), 표시 요소, 데이터셋(레시피·생성·작업·등록부·OCR 데이터셋)입니다.
설계·구현 기록은 [archive/studio/DESIGN.md](../archive/studio/DESIGN.md), 예전 이 문서 전체(숨긴 화면 설명 포함)는 [archive/studio/README_2026-11.md](../archive/studio/README_2026-11.md).

## 띄우기

```bash
pip install -r docgen/requirements.txt -r studio/requirements.txt
python -m studio                      # → http://localhost:8765
python -m studio --host 0.0.0.0       # 서버에서 띄우고 다른 PC 브라우저로 접속할 때
sh docker/studio.sh --data /database/docgen_studio   # 내부망 도커 (처음 한 번 저장 폴더 지정) — docker/README.md 3절
```

- **설정:** `studio/config.json` (git 제외, 없어도 됨, 다른 파일은 `STUDIO_CONFIG=<파일>`). 사내 OCR 연결, 브라우저 경로, `private_forms_dir`, 학습 컨테이너 `path_map` 처럼 환경마다 다른 것만. 예시 [config.example.json](config.example.json).
- **사내 OCR:** 설정 `ocr` 에 `revision` 이 있어야 켜집니다 (`/api/info` 의 `ocr_configured`, 없으면 화면이 [사내 OCR 로 읽기]를 숨김). 응답 캐시는 `<ocr.cache_dir>/ocr/<키>.json` — OCR 준비(`docgen.bench.ocr_prepare`)의 `cache_dir` 와 같은 뜻이라 같은 폴더를 쓰면 이미 읽은 그림을 다시 부르지 않습니다. 기본 `studio_cache` (예전 기본값이 만든 `studio_cache/ocr/ocr/` 도 읽음).
- **렌더링 브라우저:** Playwright Chromium → 설정 `browser` → `CHROMIUM_PATH` → 이 PC 의 Chrome·Edge 순. 없으면 렌더링(미리보기·생성)만 꺼짐.
- **도커:** 데이터셋은 `<저장 폴더>/workspace/datasets/<이름>/`. 코드는 마운트라 고치면 studio 가 저절로 다시 뜸. 다른 컨테이너에서 생성 맡기기 `docker/remote_build.py` ([guide/studio/data.md](../guide/studio/data.md)).
- 이 PC 에서 만든 그림은 글꼴이 서버와 다를 수 있습니다. 학습·평가 데이터는 서버나 도커에서 만듭니다.
- 미리보기 캐시 `studio_cache/preview/` (git 제외). 서식 파일·공통 렌더링 코드가 바뀌면 다시 그림.
- **띄울 때 한 번:** 옛 등록부 줄을 과제 형식으로 고치고(tasks/ 없는 옛 OCR 준비 폴더는 tasks/ 를 만듦), 재시작으로 놓친 생성 완료 등록을 복구합니다 (`app.py` `startup_once`). GET 요청은 파일을 쓰지 않습니다 (미리보기 그림 캐시만 예외).

## 화면 ↔ 코드

| 메뉴 | 화면 (`static/js/`) | 서버 |
|---|---|---|
| 서식 | `forms.js` (목록·상세 탭), `questions.js`, `editor.js` (영역 편집, overlay 만) | `catalog.py`, `editor.py`, `questions.py` |
| 새 서식 추가 | `new-forms.js` (그림 위에 그리기, overlay 만) | `drawn.py` (`POST /api/forms/new-image`), `generators.py` (생성 방법 고르기 창) |
| 이미지로 서식 만들기 | `form-agent.js` (목록·새로 만들기·진행·결과·파일·이어서 지시) | `api_form_agent.py` → 작업 `python -m formagent go\|continue` ([formagent/README.md](../formagent/README.md)) |
| 데이터셋 | `datasets.js`, `recipes.js`, `dataset-builds.js` (생성 현황), `dataset-tracking.js`, `jobs.js` (작업) | `datasets.py`·`api_datasets.py`, `bank_data.py`·`api_bank.py`, `ocr_data.py`, `build_registration.py`, `jobs.py` |
| 표시 요소 | `marks.js` | `marks_admin.py` |
| 사용 가이드 · OCR 예시 | `guide.js` · `ocr-examples.js` | `guidebook.py` (문서 목록 `DOCUMENTS`) · `ocr_examples.py` |
| 설정 (메뉴에 없음, `#/settings`) | `misc.js` | `app.py` `/api/info` |

**html 서식은 화면에서 고치지 않습니다.** 서식 상세의 고치기 탭에는 파일 목록과 안내만 있고, 고치거나 새로 더하는 것은 코드로 합니다:
고칠 곳 [docgen/forms/README.md](../docgen/forms/README.md) 0절, 파일 꼴 [NEW_FORM_SPEC.md](../docgen/manual/NEW_FORM_SPEC.md), 모양만 [FORM_SHELL_GUIDE.md](../docgen/manual/FORM_SHELL_GUIDE.md).

## 고친 것이 저장되는 곳

모두 저장소 안 파일이라 `git diff` 로 검토합니다 (실서류 견본에서 만든 서식만 `private_forms_dir`).

| 고친 것 | 파일 | 생성기가 읽는 곳 |
|---|---|---|
| 영역·키·키 설명·생성 방법·배경 지우기 (영역 편집, overlay) | 서식 폴더의 칸 목록 `docgen/forms/<ID>/fields.json` (실서류에서 만든 서식은 `private_forms_dir/<ID>/fields.json`). 서식 파일 전부 `python -m docgen.formdir path <ID>` | `docgen/formfields.py` → overlay `docgen/overrides.py`·`realform.py`, html `docgen/html_regions.py`·`htmlform.py` |
| 가져온 서식 (공개 서식 묶음) | `docgen/forms/img_*/` (`layout.json`, `look/page_<n>.png`) — 실서류 묶음에서 만든 것은 `private_forms_dir/img_*/` (저장소 밖) | `docgen/realform.py` `register_images` |
| 검수·배정·메모·문제 표시 | `docgen/catalog.json` | `docgen/bench/build.py` (학습 데이터에서 평가 전용 서식 빼기) |
| 표시 요소 확률 | `docgen/forms/_common/marks.json` | `docgen/marks.py` |
| 표시 요소 풀 | `docgen/assets/marks/pools.json`, `docgen/assets/marks/<풀>/` | `docgen/marks.py` → `realform.py`·`render.py` |
| 질문·답 (studio 는 보기만, 파일로 고침) | 칸마다 `fields.json` 의 `q`, 이 서식만 다르게 `docgen/forms/<ID>/questions.json`, 이 서식만의 질문 `qa.py`, 기본 `docgen/forms/_common/questions.json` ([서식 폴더 설명서 5절](../docgen/forms/README.md#5-질문과-답-고치기)) | `docgen/bench/prompts.py`, `docgen/bench/tasks/<과제>.py` |

검수 완료 전의 그린·가져온 서식(`img_*`)은 레시피의 `"all"`·그룹 선택에 들어가지 않습니다 (ID 를 직접 적으면 시험용으로 들어감).

## 작업 공간 (`workspace_dir`)

studio 가 만든 데이터셋과 기록입니다. 손으로 고치지 말고 화면·API 로 다룹니다.

| 파일 | 내용 |
|---|---|
| `registry.json` | 데이터셋 등록부 (`datasets.py`) |
| `datasets/<이름>/` | 레시피로 만든 데이터셋. 설명서 `DATASET.md` 는 등록·고정·사람 칸 저장 때 씀 (폴더가 없으면 쓰지 않음) |
| `cards/<ID>.md` | 등록만 한 폴더의 설명서 (그 폴더에는 쓰지 않음) |
| `jobs/<작업ID>/job.json`·`log.txt` | 백그라운드 작업 (`jobs.py`). 깨진 `job.json` 은 경고만 찍고 건너뜀 |

- 같은 이름으로 생성을 두 번 누르거나 이미 있는 폴더 이름이면 `POST /api/builds` 가 409 로 거절합니다 (덮어쓰지 않음).
- 명령을 띄우지 못한 작업은 `failed` 로 남고 `error` 에 까닭이 적힙니다.

## 구조

```
studio/
  __main__.py     python -m studio (uvicorn 실행)
  app.py          FastAPI: /api/* 와 정적 파일
  catalog.py      서식 목록·상세, 검수·배정·문제 표시 (docgen/catalog.json), 서식 다시 읽기(캐시도 비움), 카드 FORM.md
  config.py       설정 읽기, 렌더링 브라우저 찾기
  questions.py    서식 › 질문·답 › 실제 문항: 실제 생성기로 만든 문항
  guidebook.py    사용 가이드 화면의 문서 목록 (python -m studio.guidebook)
  editor.py       overlay 영역 편집기: 레이아웃 보기, 사람 수정 검사·저장, 검수 전 자동 검사
  drawn.py        새 서식 추가: 그림을 올려 빈 overlay 서식 img_* 만들기, 배경 글자 사내 OCR 로 읽기
  api_form_agent.py 이미지로 서식 만들기: 초안 시작·목록·상세·로그·파일·이어서·멈추기 (formagent 진행기를 작업으로, 한 번에 한 건)
  generators.py   영역 편집기의 생성 방법 고르기 목록·예시 값
  marks_admin.py  표시 요소 확률·풀 읽고 쓰기 (풀 이미지·글꼴 파일 경로는 서버가 정함, 지울 때 폴더 밖은 안 지움)
  datasets.py     데이터셋 등록부·옛 줄 고치기(migrate), 문항 보기, 설명서 (api_datasets.py 가 API)
  bank_data.py    레시피, 은행 서류 데이터 빌드 (api_bank.py 가 API)
  ocr_data.py     합성 OCR 레시피·빌드
  ocr_examples.py OCR 예시 화면
  internal_ocr_adapter.py 사내 OCR 부르기 (studio·학습 준비 공용)
  jobs.py         백그라운드 작업 (명령줄과 같은 명령, <workspace>/jobs/). 같은 출력 폴더는 하나만
  build_registration.py  데이터셋 › 생성 현황: 끝난 데이터셋 자동 등록, 띄울 때 놓친 등록 복구
  deps.py         내부망 컨테이너용 패키지 설치 (python -m studio.deps download | install)
  wheels/         그 설치 파일 (Linux, 파이썬 3.12)
  static/         화면 (index.html, style.css, js/<메뉴>.js — 빌드 없음, 외부 CDN 없음)
docgen/preview.py 서식 하나 렌더링 (브라우저 전용 스레드, 결과 캐시)
```

## 테스트

```bash
python -m pytest studio/tests
```
