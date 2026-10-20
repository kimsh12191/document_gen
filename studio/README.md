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
- **내부망:** 인터넷이 되는 PC에서 wheel 을 받아 옮긴다.
  ```bash
  pip download -r requirements.txt -r studio/requirements.txt -d wheels --only-binary=:all: --platform manylinux2014_x86_64 --python-version 3.10
  pip install --no-index --find-links wheels -r requirements.txt -r studio/requirements.txt
  ```
- 이 PC에서 만든 이미지는 글꼴이 서버와 다를 수 있다(나눔·Noto 글꼴이 없으면 대체 글꼴). 편집·미리보기용으로 쓰고, 학습·평가 데이터는 서버나 도커에서 만든다.

## 지금 되는 것 (1단계)

| 메뉴 | 기능 |
|---|---|
| ① 서식 | 476종 목록 (검색, 그룹·종류·검수 필터, 한글 키·값 없는 칸 수, 쓰이는 시나리오) |
| | 미리보기: seed·내용 많음·특수 상황·촬영 조건을 바꿔 즉석 렌더링, 쪽 넘기기, 값·항목명·체크박스·도장·서명 박스를 층별로 겹쳐 보기, 박스나 표를 누르면 항목 정보 |
| | 예시: seed 여러 개(기본 8장)를 격자로, 같은 층 표시. 카드를 누르면 그 seed 로 미리보기 |
| | 키 목록(30번 렌더링 기준 채움률·예시, 한글 키 표시), 파일(이 서식을 정하는 파일) |
| ⑨ 설정 | 적용된 설정 보기 |
| ②~⑧ | 들어올 기능 안내 (DESIGN.md 11절의 단계) |

메뉴는 일의 흐름 순서다: ① 서식 → ② 표시 요소 → ③ 시나리오·묶음 (합성 재료) → ④ 가져오기 → ⑤ 검수 (실서류·기존 결과) → ⑥ 데이터셋 → ⑦ 평가 (두 벤치마크를 출처와 상관없이 같은 화면에서) → ⑧ 작업 → ⑨ 설정.

미리보기는 `studio_cache/preview/` 에 저장된다(git 제외). 서식 파일(템플릿·생성 함수·레이아웃)이나 공통 렌더링 코드가 바뀌면 자동으로 다시 그린다. 렌더링 코드는 [docgen/preview.py](../docgen/preview.py).

## 구조

```
studio/
  __main__.py     python -m studio (uvicorn 실행)
  app.py          FastAPI: /api/* 와 정적 파일
  catalog.py      서식 목록·상세 (레지스트리 + guide/fields/fields.json + docgen/catalog.json)
  config.py       설정 읽기, 렌더링 브라우저 찾기
  static/         화면 (index.html, app.js, style.css — 빌드 없음, 외부 CDN 없음)
docgen/preview.py 서식 하나 렌더링 (브라우저 전용 스레드, 결과 캐시)
```
