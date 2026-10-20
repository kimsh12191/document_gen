# docgen studio

은행 벤치마크 데이터 생성·관리 웹 도구. 생성기(`docgen`)의 서식·라벨을 보고 고치고, OCR·은행 업무 벤치마크를 합성·이미지 묶음·이미 있는 결과에서 만들고, 데이터셋·모델 답·점수를 한 화면에서 관리한다. 설계는 [DESIGN.md](DESIGN.md), 이미 만든 OCR·추론 결과를 가져올 때의 폴더 형식은 [RESULTS_FORMAT.md](RESULTS_FORMAT.md), 만든 데이터셋을 1부·2부 학습에 넣는 방법은 [TRAINING.md](TRAINING.md).

## 띄우기

저장소 루트에서:

```bash
pip install -r requirements.txt -r studio/requirements.txt
python -m studio                      # → http://localhost:8765
python -m studio --host 0.0.0.0       # 서버에서 띄우고 다른 PC 브라우저로 접속할 때
```

- **렌더링 브라우저:** Playwright 의 Chromium 이 없으면 설정의 `browser` → 환경변수 `CHROMIUM_PATH` → 이 PC의 Chrome·Edge 순으로 찾는다. 회사망에서 `playwright install chromium` 이 인증서 오류로 막혀도 설치된 Chrome 으로 돈다.
- **설정:** `studio/config.json` (git 제외). 바꿀 항목만 적는다. 예시는 [config.example.json](config.example.json).
- **내부망:** docgen 도커 컨테이너(Chromium·글꼴 포함)에서 띄우고, 윈도우 PC에서 SSH 터널로 접속한다. 이미지는 새로 반입하지 않는다. studio 패키지는 코드에 든 Linux 설치 파일(`studio/wheels/`)로 컨테이너 안에서 `python -m studio.deps install` 한 번이면 된다. 순서는 [docs/DOCKER.md 4절](../docs/DOCKER.md#4-studio-띄우기-같은-컨테이너).
  - 설치 파일 새로 받기(인터넷 되는 PC, 패키지 판을 바꿀 때만): `python -m studio.deps download`
  - 학습은 별도 학습 컨테이너에서 한다. 두 컨테이너는 폴더를 공유하고, 경로가 다르면 설정의 `path_map`으로 맞춘다([TRAINING.md](TRAINING.md)).
- **브라우저가 없을 때:** studio는 그대로 뜨고 렌더링(미리보기·합성 데이터 만들기)만 꺼진다. 등록부·평가·검수처럼 렌더링이 필요 없는 화면은 쓸 수 있다.
- 이 PC에서 만든 이미지는 글꼴이 서버와 다를 수 있다(나눔·Noto 글꼴이 없으면 대체 글꼴). 편집·미리보기용으로 쓰고, 학습·평가 데이터는 서버나 도커에서 만든다.

## 지금 되는 것 (1~7단계)

| 메뉴 | 기능 |
|---|---|
| ① 서식 | 476종 목록 (검색, 그룹·종류·검수·문제 표시·사람 수정 필터, 한글 키·값 없는 칸 수, 쓰이는 시나리오, 배정) |
| | **미리보기**: seed·내용 많음·특수 상황·촬영 조건을 바꿔 즉석 렌더링, 쪽 넘기기, 값·항목명·체크박스·도장·서명 박스를 층별로 겹쳐 보기, 박스나 표를 누르면 항목 정보. **문제 표시**를 켜고 그림을 누르면 메모가 남는다 |
| | **예시**: seed 여러 개(기본 8장)를 격자로, 같은 층 표시. 카드를 누르면 그 seed 로 미리보기 |
| | **영역 편집** (overlay): 값 영역 고르기·옮기기·크기 바꾸기·빼기·되살리기, 새 칸 그리기(글자·체크 보기·서명·결재란), 키(사전 후보)·값 종류·값 출처, 배경 지우기(흰색·주변색), "지운 자리를 값 영역으로", 깨진 수정 표시, **수정 전후 비교**(같은 seed 로 저장본과 고친 것을 나란히, 바뀐 키·값 목록) |
| | **검수**: 자동 검사(한글 키, 값 영역 겹침, 영역 안 인쇄 글자, 깨진 수정, 안 채워지는 칸 — 경고만), 검수 완료 버튼(누른 사람·날짜, 서식 파일이 바뀌면 "재검수 필요"), 학습/평가 배정, 메모, 문제 표시 목록 |
| | 키 목록(30번 렌더링 기준 채움률·예시, 한글 키 표시), 파일(이 서식을 정하는 파일) |
| ② 표시 요소 | 확률(손글씨 비율, 결재란, 서명·도장 자리), 풀(체크 표시·서명 이미지 올리기, 도장 틀, 손글씨·인쇄체 글꼴)의 가중치·켜기, 샘플 서식에 적용해 보기 |
| ⑥ 데이터셋 | 등록부: 1부 prepare 결과·docgen.bench 결과·2부 prepare 결과 폴더를 경로로 등록(형식 자동 인식, 읽기만), 출처·정답 종류·실서류 표시, 고정 |
| | **설명서**: 구성·점수·쓴 학습은 자동, 목적·쓰면 안 되는 곳·한계는 사람이 (studio 가 만든 데이터셋은 폴더의 `DATASET.md`, 등록만 한 폴더는 `<workspace>/cards/<ID>.md`) |
| | **문항**: 과제별로 이미지·질문·정답 박스(0~1000)·모델 답 박스를 겹쳐 보기, 검색, 첫 답 점수 낮은 것부터 |
| | **모델 답**: `runs/<실험>/`(1부·2부 파이프라인), docgen.bench 예측 폴더, 답 파일을 붙이고 채점. 1부 `bank_ocr.metrics`·`docgen.bench.evaluate`를 그대로 불러 명령줄과 같은 숫자 (2026-10-20 시험 세트로 차이 0 확인). 파이프라인 점수 파일도 보기 |
| ⑦ 평가 | 고른 데이터셋들의 채점 결과를 벤치마크별 한 표로 (모델·버전·합성/실서류·의사정답/검수 정답 비교) |
| | **새로 만들기 (은행 업무)**: 레시피(`datasets/recipes/<이름>.json`) 편집 — 용도(평가/학습), 서식·시나리오·묶음 수, 촬영 조건 비율, 묶음 규칙(빠진·타인·불필요 서류, 변조 비율), 대조 사례 켜기·변조 비율, 검수 완료 서식만, 직접 만든 묶음. 만들기를 누르면 `python -m docgen.bench build --recipe …` 를 작업으로 돌리고 끝나면 등록부에 올린다 (`dataset.json`: 레시피·커밋·버전·서식 해시) |
| | **업무 묶음**: 묶음 목록(빠짐·타인·불필요·변조로 거르기), 묶음 상세(서류 전부, 고객 프로필 값과 그 값이 있는 자리, 고객 일관성 검사, 대조 변조판과 바뀐 칸, 같은 seed 로 다시 만들기) |
| | **학습**: 2부 `run_bank_pipeline.py` 설정 조각(학습 데이터·평가 세트·OCR 유지용, `path_map` 으로 학습 컨테이너 경로) → `training/configs/studio-<이름>.json`, 실행할 명령, 진행(state.json), 끝나면 평가 세트에 모델 답으로 자동으로 붙음 |
| | **새로 만들기 (합성 OCR)**: OCR 레시피(용도 평가 전용/학습, 서식, 고객 수, 촬영 조건, 정답 단위 단어/줄, 합칠 1부 manifest, 1부 설정 덮어쓰기) → `python -m docgen.ocr_set build` → 1부 `bank_ocr prepare` 결과를 등록. 정답은 쪽 전체 글자(html 은 화면 단어 박스, overlay 는 배경 PDF 글자 + 값), 견본 표시·도장 글자·정정 글자는 신뢰도 0.3 |
| | **학습 (1부)**: `run_pipeline.py` 설정과 데이터 설정(`output_dir` = 이 데이터셋, 준비 단계 건너뜀) |
| | **평가 세트 2.0**: 은행 업무 `kie`·`marks` 답에 위치(bbox_2d 0~1000, page). 값·위치·값+위치 점수, 문항 보기에 정답 박스 (1.x 세트도 같은 화면·채점기) |
| ③ 시나리오·묶음 | 업무 시나리오의 필수 서류 넣기·빼기, 새 시나리오 (`docgen/scenarios.json`, 이미 있던 순서는 고정), 대조 사례·심사 규칙 목록 |
| ⑧ 작업 | 데이터셋 빌드 같은 백그라운드 작업: 진행, 명령, 로그, 취소 |
| ⑨ 설정 | 적용된 설정 보기 |
| ④ 가져오기 | **이미지 묶음**: 서버 폴더(`import_dir` 아래) 또는 파일 올리기 → 쪽 목록(PDF 는 쪽마다 200dpi 그림) → 사내 OCR(1부와 같은 캐시 규칙) → 포맷·양식 묶기(masking_ui 지문, `studio/formats.py`). 여러 쪽 문서의 뒷쪽은 첫 쪽 포맷을 따른다 |
| | 포맷 카드(견본 썸네일, 문서·쪽·변형 수, 가까운 기존 서식), 포맷 열기: 이름 바꾸기, 결정(**템플릿으로** / 기존 서식과 같음 / 건너뛰기), 합치기, 고른 쪽·변형 따로 떼기 (사람이 정한 것은 다시 묶어도 남는다) |
| | **템플릿으로**: 견본 문서의 쪽 그림을 배경으로 overlay(image) 서식 `img_*` → 바로 영역 편집기. 같은 포맷의 다른 문서와 견줘 **값 자리·지우기 초안**(문서마다 바뀌는 글자 = 값, 항목명 = 왼쪽·위 고정 글자). 실서류 묶음은 `private_forms_dir` 에만 만든다 |
| | **OCR 벤치마크로**: 묶음 전체나 고른 포맷 → 1부 manifest·설정 → `bank_ocr prepare` → 등록부. 정답은 사내 OCR 그대로 / OCR 검수본(확인한 쪽만) |
| | **생성 데이터로 시험**: 사내 OCR 없이 흐름 전체를 본다 (합성 정답을 OCR 결과로, 진짜 서식 대비 묶기 순도 표시) |
| ⑤ 검수 | **OCR 검수**: 쪽 그림 위 단어 박스(신뢰도 낮음·고침·새로 그림 색 구분), 글자 고치기, 옮기기·크기, 새 박스, 지우기, 합치기, 커서 자리에서 나누기, 원래 OCR 겹쳐 보기, 의심 먼저(신뢰도 낮음 → 숫자). 저장·확인(다음 쪽으로). 사내 OCR 응답 형식 그대로 `real_data_dir/ocr_reviewed/<묶음>/` 에 저장하고, 원래 OCR 과의 차이(글자 오류율·박스 F1·고친·더한·뺀 단어)를 쌓는다 |

**고친 것이 저장되는 곳** (모두 저장소 안 파일, git diff 로 검토)

| 고친 것 | 파일 | 생성기가 읽는 곳 |
|---|---|---|
| overlay 영역·키·값 출처·배경 지우기 | `add_template/overrides/<ID>.json` (가져온 서식 `img_*` 는 그 서식 폴더의 `overrides.json`) | `docgen/overrides.py` → `docgen/realform.py` |
| 가져온 서식 (공개 서식 묶음) | `add_template/images/img_*/` (`layout.json`, `page_<n>.png`) — 실서류 묶음에서 만든 것은 `private_forms_dir/img_*/` (저장소 밖) | `docgen/realform.py` `register_images` |
| 검수·배정·메모·문제 표시 | `docgen/catalog.json` | `docgen/bench/build.py` (학습 데이터에서 평가 전용 서식 빼기) |
| 표시 요소 확률 | `docgen/marks.json` | `docgen/marks.py` |
| 표시 요소 풀 | `assets/marks/pools.json`, `assets/marks/<풀>/` | `docgen/marks.py` → `realform.py`·`render.py` |
| 표준 키 사전 (자동 생성) | `docgen/keys.json` (`python scripts/build_keys.py`) | studio 의 키 고르기 |

저장소 밖에 두는 것: 가져온 묶음(`<workspace>/imports/<묶음>/`: `batch.json`, `pages.jsonl`, `formats.json`, 썸네일), OCR 캐시(설정 `ocr.cache_dir`, 기본 `studio_cache/ocr`), OCR 검수본(`real_data_dir/ocr_reviewed/`, 설정이 없으면 `<workspace>/real_data/` 에 두고 화면에 경고).

가져온 서식은 등록되자마자 목록·편집기에 나오지만, **검수 완료 전에는 레시피의 `"all"`·그룹 선택으로 데이터셋에 들어가지 않는다** (값을 덜 지운 견본 배경이 생성 이미지마다 복제되지 않게). 서식 ID 를 직접 적으면 시험용으로 들어간다.

기본값은 예전 생성기와 같아서 아무것도 고치지 않으면 생성 결과(라벨·이미지)가 그대로다 (2026-10-20, overlay·html 서식 10종 × seed 3개로 확인).

메뉴는 일의 흐름 순서다: ① 서식 → ② 표시 요소 → ③ 시나리오·묶음 (합성 재료) → ④ 가져오기 → ⑤ 검수 (실서류·기존 결과) → ⑥ 데이터셋 → ⑦ 평가 (두 벤치마크를 출처와 상관없이 같은 화면에서) → ⑧ 작업 → ⑨ 설정.

미리보기는 `studio_cache/preview/` 에 저장된다(git 제외). 서식 파일(템플릿·생성 함수·레이아웃)이나 공통 렌더링 코드가 바뀌면 자동으로 다시 그린다. 렌더링 코드는 [docgen/preview.py](../docgen/preview.py).

## 구조

```
studio/
  __main__.py     python -m studio (uvicorn 실행)
  app.py          FastAPI: /api/* 와 정적 파일
  catalog.py      서식 목록·상세, 검수·배정·문제 표시 (docgen/catalog.json)
  config.py       설정 읽기, 렌더링 브라우저 찾기
  editor.py       overlay 영역 편집기: 레이아웃 보기, 사람 수정 검사·저장, 검수 전 자동 검사
  marks_admin.py  표시 요소 확률·풀 읽고 쓰기
  datasets.py     데이터셋 등록부, 문항 보기, 모델 답, 채점, 설명서 (api_datasets.py 가 API)
  bank_data.py    레시피, 은행 업무 빌드, 업무 묶음 보기·고객 일관성 검사, 시나리오 편집, 2부 학습 설정 (api_bank.py 가 API)
  training_link.py 학습 설정 쓰기, 학습 기록, 진행 읽기, 결과 자동 붙이기
  ocr_data.py     합성 OCR 레시피·빌드, 1부 학습 설정
  importer.py     ④ 가져오기: 묶음, 쪽 목록, 사내 OCR(1부 규칙), 묶기·합치기·떼기·결정, 템플릿·값 자리 초안, OCR 세트 (api_import.py 가 API)
  formats.py      포맷·양식 지문과 묶기 (masking_ui 6f5bca6 에서 옮김)
  ocr_review.py   ⑤ OCR 검수: 검수본 읽고 쓰기, 사내 OCR 오류 통계
  jobs.py         백그라운드 작업 (명령줄과 같은 명령, <workspace>/jobs/)
  deps.py         내부망 컨테이너용 패키지 설치 (python -m studio.deps download | install)
  wheels/         그 설치 파일 (Linux, 파이썬 3.12)
  static/         화면 (index.html, style.css, js/<메뉴>.js — 빌드 없음, 외부 CDN 없음)
docgen/preview.py 서식 하나 렌더링 (브라우저 전용 스레드, 결과 캐시)
```
