---
name: form-from-image
description: 서식 이미지(빈 서식·견본·실서류 사진)를 보고 docgen html 서식 초안을 만든다 — 칸마다 항목명·키·설명·생성 방법을 정한 칸 표(fields.md)와 template.html.j2·form.json 을 쓰고, 렌더를 원본과 나란히·겹쳐 보며 고친다. "이 이미지로 서식 만들어줘", "forms 에 넣을 html 서식", "칸·키 정해줘" 같은 요청에 쓴다. 이미 있는 서식 고치기는 이 스킬이 아니라 docgen/forms/README.md.
---

# 이미지 → html 서식 초안

서식 이미지 한 장(쪽마다 한 장)을 받아 docgen 이 그대로 읽는 **초안 폴더**를 만든다.
결과물 꼴의 원문은 `docgen/manual/NEW_FORM_SPEC.md` 이고, 이 문서는 그것을 따르는 작업 순서다. 둘이 다르면 NEW_FORM_SPEC 을 따른다.

- **내놓는 것:** `out/form_drafts/<ID>/` 에 `fields.md`(칸 표) · `template.html.j2` · `form.json` · `source.png` · `review.md`(비교 기록) + 보고.
- **하지 않는 것:** 등록(`docgen/forms/` 로 옮기기)은 사용자가 하라고 할 때만 (7단계). 기존 서식 폴더·다른 서식·`docgen/forms/_common/`·엔진 코드(`docgen/*.py`)는 고치지 않는다.
- **실서류 그림**은 사내 모델(지금 이 작업)에서만 다룬다. 외부 서비스·모델에 보내지 않는다. 실서류에서 만든 서식은 공개 폴더가 아니라 `$DOCGEN_PRIVATE_FORMS/` 에 등록한다.
- 같은 단계에서 같은 오류가 두 번 나면 멈추고 오류 끝부분과 함께 보고한다.

명령은 저장소 맨 위 폴더(`document_gen/`)에서 실행한다.

## 1. 준비

1. 먼저 읽는다: `docgen/manual/NEW_FORM_SPEC.md` 1~7절·9절 (템플릿 문법·칸 목록·키·검사·예시), `guide/studio/keys.md` 3~6절 (키 짓기).
2. **서식 ID** 를 정한다: 원본 제목의 영어 이름, 소문자·숫자·밑줄 3~51자 (`loan_application`). 쓸 수 있는지 확인:
   `python -m docgen.formdir path <ID>` → "없습니다 (새 서식이면 쓸 수 있는 ID)" 가 나와야 한다. 이미 있으면 다른 ID.
3. 초안 폴더 `out/form_drafts/<ID>/` 를 만들고 원본 그림을 복사한다: 1쪽 `source.png`, 2쪽부터 `source_2.png`, `source_3.png` ….
4. 원본이 실서류인지(사람 이름·번호가 실제 값으로 찍혀 있는지) 사용자에게 들은 대로 적어 둔다. 모르면 묻는다.

## 2. 칸 표 `fields.md` (항목 설명·키 지정)

그림을 위에서 아래로 읽으며 **값이 들어가는 자리**를 모두 표로 적는다. html 보다 먼저 쓴다. 이 표가 이 작업의 핵심 결과물이고 사람이 검토한다.

```markdown
# <서식 이름> (<ID>) — <쪽 수>쪽, group=<group>, category=<external|internal>

| 쪽 | 원본 항목명 | 키 | type | source | 설명 | 확신 |
|---|---|---|---|---|---|---|
| 1 | 성명 | customer.name | text | profile.person.name | 신청인 본인 이름 | 높음 |
| 1 | 대출신청금액 | loan.amount | amount | rule:amount | 원 단위 금액 | 높음 |
| 1 | 용도 (□대출 □기타) | purpose | checkbox | rule:choice [대출, 기타] | 보기 중 하나 | 높음 |

## 반복 표 <표 키> (원본 행 수 n → min n, max m)
| 열 | 원본 항목명 | 열 키 | type | source | 설명 |

## 도장·서명
| 원본 표시 | 키 | 매크로 |  (예: (인) → sign.customer → m.sigspot)

## 고정 문구 (값 아님 — 템플릿에 글자 그대로)
- 약관 1~5조, "위와 같이 신청합니다" …

## 판단이 안 선 것
- <무엇이 왜 애매한지>
```

정하는 규칙:
- **값 자리 / 고정 문구 구분:** 문서마다 달라지는 것(사람·번호·날짜·금액·주소·체크 결과·지점명)은 값 자리, 모든 문서에 똑같이 인쇄되는 것(제목·항목명·안내문·약관)은 고정 문구.
  원본에 찍힌 실제 값(이름·번호·주소)은 절대 템플릿에 옮기지 않는다 — 값 자리로 바꾼다.
- **원본 항목명**은 인쇄된 글자 그대로 (띄어쓰기 포함). 항목명이 없는 자리는 뜻을 괄호로: `(발급일)`.
- **키**: keys.md 3절 `누구의.무엇` — `customer.name`, `agent.phone`, `loan.amount`, `period.start`, `issue_date`. 같은 뜻은 서식 안에서 같은 이름. 한글·대문자·번호 붙은 키(`name2`) 금지. 한 키가 다른 키의 앞부분이면 안 됨(`account` 와 `account.number` 같이 쓰지 않음). 도장·서명은 `seal.`·`sign.` 으로 시작.
- **type**: `text` `amount` `number` `date` `checkbox` `seal` `signature`.
- **source**: 같은 사람·회사 값은 `profile.…`(NEW_FORM_SPEC 3절), 그 밖은 `rule:<종류>`. 체크 보기는 `rule:choice` + 보기 목록(원본 글자 그대로), 늘 같은 글자는 `rule:fixed`, 정하기 어려우면 `rule:note`(나중에 고침).
- **설명**: 그 칸에 무엇이 들어가는지 한 줄 (form.json 의 `description` 이 된다). 칸끼리 관계(합계=행 합, 발급일≥조회종료일)가 보이면 설명에 적고 "판단이 안 선 것"에도 남긴다 — `generate.py` 는 사용자가 원할 때만 쓴다 (NEW_FORM_SPEC 8절).
- **확신 낮음**은 숨기지 말고 표시한다: 키가 애매함, 값인지 고정 문구인지 모름, 글자가 흐려 읽지 못함.

## 3. 템플릿·칸 목록 쓰기

`fields.md` 대로 `template.html.j2` 와 `form.json`(초안 꼴: `fields`·`lists` 포함)을 쓴다. NEW_FORM_SPEC 9절 예시를 뼈대로 삼는다.

- 첫 두 줄(`{% extends "_base.html.j2" %}`, `{% import "_macros.html.j2" as m with context %}`)은 그대로.
- 값 자리는 **모두** `f("키", label="원본 항목명")`, `m.choice`, `m.agree`, `m.seal`, `m.sigspot`, 반복 표 `{% for r in d.<표 키> %}` 로. `{{ d.x }}` 로 직접 찍지 않는다 (정답에서 빠짐).
- 쪽은 A4 794×1123px. 표는 `table-layout: fixed` + `<colgroup>` 열 너비 %, **행 높이는 `tr { height: Npx }`** (padding 으로 맞추지 않음). 합친 칸은 `colspan`/`rowspan`.
- 원본의 비율을 잰다: 표 너비·열 너비는 원본 가로에 대한 %, 행 높이·간격은 원본 세로 비율 × 1123px.
- 색·글꼴은 CSS 변수(`var(--border)`, `var(--label-bg)`, `var(--accent)`)로. 외부 URL·`<script>`·실제 로고·바코드·관인 그림은 넣지 않는다.
- `form.json` 의 `name`(원본 제목), `group`, `category`, `page: "a4"`, `origin: "analyzer"`, `parent: null`, `source_image: "source.png"`. 칸마다 `label`·`type`·`source`·`description`.

## 4. 그려 보기·형식 검사

```bash
python -m docgen.preview --dir out/form_drafts/<ID> --rows min --out out/form_drafts/<ID>/render_min
python -m docgen.preview --dir out/form_drafts/<ID> --rows max --out out/form_drafts/<ID>/render_max
```

마지막 줄 JSON 이 통과 조건을 모두 만족할 때까지 고친다:

| 볼 것 | 통과 |
|---|---|
| 명령 | 오류 없이 끝남 |
| `checks` | `[]` (키가 칸 목록·템플릿 한쪽에만 있으면 여기 나옴) |
| `overflow` | `false` |
| `pages` (`--rows min`) | 원본 쪽 수와 같음 (`--rows max` 는 늘어나도 됨) |
| `fields` | `fields.md` 의 칸 수와 맞음 (반복 표는 행 수만큼) |

추가로 `grep -n "{{ *d\." out/form_drafts/<ID>/template.html.j2` 가 값 출력에 걸리지 않는지 본다 (조건문 `{% if d.… %}` 는 괜찮음).

## 5. 원본과 비교하며 고치기 (최대 3회)

```bash
python .claude/skills/form-from-image/compare.py \
  --source out/form_drafts/<ID>/source.png [source_2.png …] \
  --render out/form_drafts/<ID>/render_min --out out/form_drafts/<ID>/compare_<회차>
```

`side_<쪽>.png`(왼쪽 원본·오른쪽 렌더)와 `overlay_<쪽>.png`(회색 원본 위에 빨강 렌더, 파랑 값 박스와 키)를 **둘 다 열어 본다**.
원본을 A4 크기로 늘려 맞췄을 뿐이라 스캔 여백만큼 전체가 밀린 것은 무시하고 부분끼리 어긋난 것을 본다.

아래를 쪽마다 예/아니오로 답해 `review.md` 에 회차별로 적는다. "아니오"마다 어디가(위치·항목명) 어떻게 다른지 한 줄.

1. 원본의 제목·항목명·고정 문구가 렌더에 모두 있다 (빠진 것 없음)
2. 원본에 없는 항목명·문구를 렌더에 지어내지 않았다
3. 표마다 행 수·열 수가 같다 (반복 표는 `--rows min` 행 수 기준)
4. 칸 나눔(합친 칸, 라벨 칸과 값 칸의 배치)이 같다
5. 덩어리(표·문단·서명란)의 위아래 순서와 대략의 위치·크기가 같다 (겹친 그림에서 빨강과 회색이 크게 어긋나지 않음)
6. 파랑 값 박스가 원본에서 값이 적힌(적힐) 자리에 있다, 값 자리가 빠진 곳이 없다
7. 체크 보기 목록·도장·서명 자리가 원본과 같다
8. 쪽 수가 같다

"아니오"를 고치고 4단계부터 다시. 3회 뒤에도 남은 "아니오"는 고치지 말고 보고에 적는다. 글자 크기·굵기·선 굵기의 작은 차이는 고치지 않아도 된다 (생성할 때 무작위로 바뀜).

## 6. 보고

| 항목 | 내용 |
|---|---|
| 서식 | ID, 이름, 쪽 수, 원본이 실서류인지 |
| 칸 | 값 자리 수, 반복 표(행 min~max), `fields.md` 경로 |
| 검사 | `--rows min`/`max` 마지막 줄 JSON |
| 비교 | 마지막 회차의 8문항 결과, `compare_<회차>/` 그림 경로 |
| 판단이 안 선 것 | `fields.md` 의 확신 낮음·애매한 칸, 남은 "아니오" |
| 사람이 볼 것 | 칸 표의 키(데이터셋을 만든 뒤에는 못 바꿈), 비교 그림 |

형식 검사·비교 통과를 "검수 완료"라고 하지 않는다. 검수는 등록 뒤 사람이 studio 에서 한다.

## 7. 등록 (사용자가 하라고 할 때만)

NEW_FORM_SPEC 6절 2)·3) 대로 초안을 등록 폴더 꼴로 옮긴다.

- 어디에: 공개·빈 서식 → `docgen/forms/<ID>/`, **실서류에서 만든 것 → `$DOCGEN_PRIVATE_FORMS/<ID>/`**. 그 자리에 폴더가 이미 있으면 멈추고 보고한다 (덮어쓰지 않음).
- `template.html.j2` → `<ID>/look/template.html.j2`, `form.json` 의 `fields`·`lists` → `<ID>/fields.json` (`{"engine": "html", "unit": "px", "fields": …, "lists": …}`), 나머지 → `<ID>/form.json`, `source.png` → `<ID>/source.png`. `fields.md`·`review.md`·렌더 폴더는 옮기지 않는다.
- 확인: `python -m docgen.formdir check <ID>`, `python -m docgen.formdir card <ID>`, `python -m docgen.preview <ID> --rows max --out out/<ID>`.
- 사용자에게 알린다: studio 서식 › **서식 다시 읽기** 를 누르면 목록에 나오고, **생성 사례 › 미리보기/검수** 에서 원본과 비교해 검수 완료를 누른다.
