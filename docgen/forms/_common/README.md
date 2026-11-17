# 모든 서식이 같이 쓰는 것 (`docgen/forms/_common/`)

서식 폴더 `docgen/forms/<ID>/` 에는 **그 서식만의 것**이, 이 폴더에는 **모든 서식에 영향을 주는 것**이 있습니다.
서식을 손볼 때는 이 두 곳만 봅니다. 서식 하나를 이해하려면 그 폴더의 카드 `FORM.md` 부터, 고치는 법은 [서식 폴더 설명서](../README.md).

```
docgen/forms/
  _common/                 ← 여기 (모든 서식)
  <ID>/                    ← 서식 하나
    FORM.md                  카드 (자동): 항목·위치·정한 곳·질문→답 예시·고치는 곳
    look/template.html.j2    모양·칸 자리            (원본 서식은 look/original.pdf + layout.json)
    fields.json              칸 목록 — 칸 하나 = 한 줄: 키·키 설명·생성 방법·박스·질문 설정 q
    generate.py              값 만들기 (코드 서식: @doc 함수 / html 서식: adjust 로 칸끼리 관계)
    questions.json           기본 과제의 질문 문장·항목 줄 틀·답 틀 — 기본과 다르게 할 것만 (없으면 모두 기본)
    qa.py                    이 서식만의 질문·정답 (함수 하나 = 질문 하나)
    form.json, variants/ …
```

## 이 폴더의 파일

| 파일 | 정하는 것 | 고치면 바뀌는 것 | 고치는 법 |
|---|---|---|---|
| `questions.json` | **기본 질문 문장·질문 항목 줄 틀(`item`)·답 항목 틀(`answer`, `answer_empty` — JSON 틀이나 줄글)** (과제마다). 서식의 `questions.json` 에 없으면 이것. freetext 과제의 문장도 여기 (서식별로 못 바꿈). 읽는 곳 `docgen/bench/prompts.py` | 모든 서식의 문항 → 평가 세트가 달라짐 (`docgen/bench/build.py` 의 `VERSION` 을 올림), 모든 카드 오래됨 | 파일로. `guide/reference/questions.md` 도 같이 고침 (테스트가 둘을 맞춰 봄) |
| `key_rules.json` | 값 규칙: `keys` = 값 출처(고객 정보 경로)나 값 종류를 정해 둔 키 (`foreign.swift` …), `kinds` = 공통 값 종류 `rule:<종류>` (영역 편집 고르기 창의 "공통 값 종류"). `synonyms` 는 비워 둠 (키 바꿔 쓰기 없음, 평가 세트 5.1부터). `label_rules`·`kind_rules` 는 예전 규칙이라 고쳐도 생성 값이 안 바뀜 | 그 키·값 종류를 쓰는 원본 서식(overlay) 칸의 값 | 파일로 (조심) |
| `keys.json` | 예전 키 목록 초안 (`python docgen/scripts/build_keys.py`). 지금 화면·생성 코드는 읽지 않음 | — | 고치지 않음 |
| `marks.json` | 체크·도장·서명 표시 확률 | 모든 서식의 체크·도장 그림 | studio 표시 요소 |
| `freetext_templates.json` | 기타·비고 칸의 자유 기재 문장 틀 (freetext 과제) | 그 칸의 글과 정답 | 파일로 |
| `templates/` | **바탕 틀**: `_base.html.j2`(쪽·글꼴), `_macros.html.j2`(`f()`·`m.check`·`m.seal` …), `_official_*`, `_real_form.html.j2`(원본 서식), 그룹 부품(`bank_form/`, `corporate/_seal` …) | 모든 html·코드 서식의 그림 → 재검수 | 파일로 (조심) |
| `generators.py` | **사람이 더하는 생성 방법**: `@generator` 함수 하나 = 생성 방법 `rule:<함수 이름>` 하나 (고르기 창 "직접 만든 생성기") | 그 생성 방법을 고른 모든 칸 | 파일로 — 함수를 더하기만, 기존 함수는 고치지 않음 ([guide/studio/generators.md](../../../guide/studio/generators.md) 2절) |
| `fields_catalog.json` | 모든 서식의 칸 목록 (서식마다 여러 번 그려 모은 키·키 설명·타입·채워지는 비율·예시). 읽는 곳: 데이터셋의 없는 키·열 후보(`docgen/bench/absent.py`, 같은 그룹 다른 서식의 칸), studio 서식 목록의 키 수, playground 질문 | 없는 키 문항 → 같은 레시피라도 데이터셋이 달라짐 (`dataset.json` 의 `absent_catalog_hash`) | 자동: `python docgen/scripts/build_schema.py` (서식을 더하거나 키를 바꾼 뒤, 몇 분) |
| `values.md` | 생성 방법 목록 (`fields.json` 의 `source` 에 쓰는 것) | — | 자동: `python -m docgen.formdir values` |
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
| 데이터셋 설정 | `docgen/recipes/*.json`, `docgen/catalog.json`(검수·배정) | studio |

## 키 이름 규칙

> 새 서식에 키를 붙일 때의 기준 문서는 [guide/studio/keys.md](../../../guide/studio/keys.md) 입니다 (예시·순서·표·체크·서명).

모든 서식이 같이 쓰는 키 사전·공통 키는 없습니다. 칸의 키(정답 JSON 의 키)는 **그 서식 파일에 적힌 그대로** 질문·정답에 나갑니다.
서식마다 쓰는 키는 그 서식 카드 `FORM.md`, 모든 서식의 칸 목록은 `docgen/forms/_common/fields_catalog.json` (자동, `python docgen/scripts/build_schema.py`. 없는 키·열 후보로도 씀).

- **형식:** 영어 snake_case, 점(.)으로 중첩, `역할.속성` 순서 (`applicant.name`, `company.biz_no`, `loan.amount`).
- **반복 항목:** 순번이 들어감 (`rows.0.amount`, `rows.1.amount`).
- **같은 뜻은 같은 속성 이름:** 성명 `name`, 주민번호 `rrn`, 생년월일 `birth`, 성별 `gender`, 주소 `address`, 전화 `phone`/`mobile`,
  사업자번호 `biz_no`, 대표자 `ceo`, 발급일 `issue_date`, 발급기관 `issuer`, 발급번호 `issue_no`.
- **도장·서명:** `seal.<자리>`, `sign.<자리>`. 정답은 있으면 `true`, 없으면 `false` (자리 예: `issuer` 발급기관 직인, `corp` 법인인감, `applicant` 신청인).
- **빈 칸:** 키 설명은 있는데 값이 비어 있으면 `null`.
- **체크박스:** 정답은 체크된 보기의 글자 (없으면 `null`, 복수 선택은 리스트).

값 타입: `text` 그대로 · `date`/`month` `YYYY-MM-DD`/`YYYY-MM` · `amount`/`number`/`percent` 숫자 · `amount_korean` 한글 금액을 숫자로 ·
`rrn`/`biz_no`/`account_no` 표시값 그대로 (마스킹 `*` 포함) · `phone` 숫자만 · `checkbox` 체크된 보기 · `seal`/`signature` 있음 여부.

## 고친 뒤

```bash
python -m docgen.formdir card --all --stale --workers 4     # 오래된 카드 다시 만들기 (공통을 고쳤으면 전부)
python -m docgen.formdir check --all                       # 모든 서식 검사 (칸 목록·박스·생성 방법·질문 설정·questions.json·카드)
python -m pytest docgen/tests                              # 카드가 최신인지도 검사함
```

자세한 설명: [서식 폴더 설명서](../README.md) (파일마다 할 일·질문·답·qa.py·채점·검사).
