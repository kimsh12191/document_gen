# 모든 서식이 같이 쓰는 것 (`docgen/forms/_common/`)

서식 폴더 `docgen/forms/<ID>/` 에는 **그 서식만의 것**이, 이 폴더에는 **모든 서식에 영향을 주는 것**이 있습니다.
서식을 손볼 때는 이 두 곳만 봅니다. 서식 하나를 이해하려면 그 폴더의 카드 `FORM.md` 부터 읽습니다.

```
docgen/forms/
  _common/                 ← 여기 (모든 서식)
  <ID>/                    ← 서식 하나
    FORM.md                  카드 (자동): 항목·위치·정한 곳·질문→답 예시·고치는 곳
    look/template.html.j2    모양·칸 자리            (원본 서식은 look/original.pdf + layout.json)
    fields.json              칸 목록 — 칸 하나 = 한 줄: 키·항목명·값 출처·박스·질문 설정 q
    generate.py              값 만들기 (코드 서식: @doc 함수 / html 서식: adjust 로 칸끼리 관계)
    questions.json           질문 껍데기 (문장·항목 줄 틀·답 틀·전용 질문) — 기본과 다르게 할 것만 (없으면 모두 기본)
    form.json, variants/ …
```

## 이 폴더의 파일

| 파일 | 정하는 것 | 고치면 바뀌는 것 | 고치는 법 |
|---|---|---|---|
| `questions.json` | **기본 질문 문장·질문 항목 줄 틀(`item`)·답 항목 틀(`answer`, `answer_empty`)** (과제마다). 서식의 `questions.json` 에 없으면 이것 | 모든 서식의 문항 → 평가 세트가 달라짐 (`docgen/bench/build.py` 의 `VERSION` 을 올림), 모든 카드 오래됨 | 파일로. `guide/questions.md` 도 같이 고침 (테스트가 둘을 맞춰 봄) |
| `dictionary/` | **키 사전**: 공통 키(`common.json`), 서식 칸 → 누구의·무엇(`form_keys.json`), 문서명 = 분류 정답(`doc_types.json`), 당사자·속성(`parties.json`·`attributes.json`) … | 질문·정답의 키(공통 키로 묻기), 괄호 설명, 분류 정답 | studio 키 사전 화면. 자동 초안 `python docgen/scripts/build_dictionary.py` (사람이 정한 것은 남음) |
| `key_rules.json` | 항목명 → 표준 키 규칙, 값 종류(`rule:<종류>`)의 정의 | 원본 서식(overlay)의 칸 키·값 | studio 키 사전 화면 |
| `keys.json` | 서식들이 쓰는 키 목록 (영역 편집기가 키를 고를 때) | 키 고르기 목록 | 자동: `python docgen/scripts/build_keys.py` |
| `marks.json` | 체크·도장·서명 표시 확률 | 모든 서식의 체크·도장 그림 | studio ② 표시 요소 |
| `freetext_templates.json` | 기타·비고 칸의 자유 기재 문장 틀 (freetext 과제) | 그 칸의 글과 정답 | 파일로 |
| `templates/` | **바탕 틀**: `_base.html.j2`(쪽·글꼴), `_macros.html.j2`(`f()`·`m.check`·`m.seal` …), `_official_*`, `_real_form.html.j2`(원본 서식), 그룹 부품(`bank_form/`, `corporate/_seal` …) | 모든 html·코드 서식의 그림 → 재검수 | 파일로 (조심) |
| `values.md` | 값 출처 목록 (`fields.json` 의 `source` 에 쓰는 것) | — | 자동: `python -m docgen.formdir values` |
| `hash_moves.json` | 파일을 옮기기만 한 서식의 예전 서식 해시 (검수 기록이 그대로 맞게) | — | 고치지 않음 |

## 폴더 밖이지만 서식이 쓰는 코드

| 위치 | 정하는 것 |
|---|---|
| `docgen/docs/<그룹>.py` | 같은 그룹 **코드 서식**들이 같이 쓰는 도우미 (예: 소득 서식의 부서별 업무). 서식마다 값 만드는 함수는 그 서식 폴더의 `generate.py` |
| `docgen/docs/_common.py` | 모든 코드 서식의 도우미: `D`(날짜 표기), `won`(금액), `special`(특수 상황 확률), `K`(한글 표기) … |

## 서식 작업에서 안 보는 것 (엔진·데이터셋 설정)

| 분류 | 위치 | 누가 고치나 |
|---|---|---|
| 그리기·값 채우기·증강 | `docgen/render.py`, `realform.py`, `htmlform.py`, `sources.py`, `augment.py`, `entities.py`(고객) | 개발자 |
| 문항 만들기·채점 | `docgen/bench/tasks/<과제>.py`(정답을 그린 문서에서 꺼냄), `docgen/bench/evaluate.py` | 개발자 (바꾸면 세트 `VERSION`) |
| 업무 묶음 과제 | `docgen/bench/build.py`·`cases.py`·`rules.py`, `docgen/scenarios.json` | 개발자 / studio ③ 시나리오 |
| 데이터셋 설정 | `docgen/recipes/*.json`, `docgen/catalog.json`(검수·배정) | studio |

## 고친 뒤

```bash
python -m docgen.formdir card --all --stale --workers 4     # 오래된 카드 다시 만들기 (공통을 고쳤으면 전부)
python -m docgen.formdir check --all                       # 모든 서식 검사 (칸 목록·박스·값 출처·질문 설정·questions.json·카드)
python -m pytest docgen/tests                              # 카드가 최신인지도 검사함
```

자세한 설명: [guide/forms.md](../../../guide/forms.md) (서식 관리), [guide/qa.md](../../../guide/qa.md) (질문·답).
