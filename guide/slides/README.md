# 발표 자료: 은행 서류 VLM 프로젝트 소개

팀 내부 개발자용 소개 슬라이드입니다. 본편 26장에서 1부 OCR 학습, 2부 은행 업무 학습, 실제 데이터로 확장하는 구조, 현재 상태를 다룹니다. 부록 155장에는 모든 과제의 데이터 예시가 실제 형식 그대로 들어 있습니다.

| 부록 | 내용 |
|---|---|
| A. OCR 과제 데이터 예시 | 입력 데이터(페이지 이미지 + 사내 OCR JSON → manifest → pages.jsonl), 문항 필드표, 과제 8종 각 한 건(이미지, 문항 한 줄 전체, 정답, SFT 답), SFT·GRPO 학습 샘플 |
| B. 은행 업무 과제 데이터 예시 | 공통 필드·meta·eval 키 표, 과제 8종 각 한 건(이미지, 질문 전문, 정답, eval, meta, 학습 레코드) |
| C. 서류 대조 사례 14종 | 사례마다 문항 한 건 |
| D. 심사 질의 규칙 | 규칙마다 문항 한 건 |

부록과 같은 내용이 문서로는 [../tasks.md](../tasks.md)에 있습니다(슬라이드는 1-0의 OCR JSON 같은 긴 목록을 앞 몇 개만 보이고, tasks.md는 전부 보입니다).

- **보기:** `index.html`을 브라우저로 엽니다. 슬라이드 아래에 발표자 노트가 함께 나옵니다. 부록 이미지는 `../examples/img/`에서 읽습니다. 글꼴은 인터넷이 될 때 Google Fonts에서 받고, 안 되면 기본 글꼴로 보입니다.
- **원본:** `project/deck.json`(순서·제목)과 `project/slides/<id>.html`(슬라이드 한 장씩). 웹 슬라이드 도구의 파일 그대로입니다. 부록 이미지는 웹 슬라이드에서 `/_blob/<id>`로 들어가 있고, `asset_map.json`이 `examples/img/<파일>`과의 대응표입니다.
- **다시 만들기:** 슬라이드 원본을 고친 뒤 `python guide/slides/build_html.py`를 실행하면 `index.html`이 갱신됩니다.
- **부록 다시 만들기:** 예시 데이터가 바뀌면

  ```bash
  # 1) 예시 고르기 + tasks.md, examples/img/ 다시 만들기 (입력 만드는 법은 tasks.md 맨 위)
  python guide/examples/make_catalog.py --bench <벤치 폴더> --ocr <prepared 폴더> --ocr-json <OCR JSON 폴더> --dump examples.json
  # 2) 부록 슬라이드(ax-*.html) 다시 쓰기 + deck.json 순서 갱신 (본편 슬라이드는 그대로)
  python guide/slides/make_appendix.py --examples examples.json --assets guide/slides/asset_map.json --deck guide/slides/project
  python guide/slides/build_html.py
  ```

  새 이미지가 생기면 웹 슬라이드에 올리고 `asset_map.json`에 `/_blob/<id>`를 추가해야 합니다.
- 같은 내용의 문서판은 [../overview.md](../overview.md)입니다.
