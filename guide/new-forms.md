# 새 서식 추가하기

서식 그림 한 장에서 시작해 합성 데이터에 쓰이는 서식으로 올리기까지의 절차입니다.
**html 서식과 기본 키는 대형 모델(클로드 등)이 만들고**, 사람은 검사하고 studio에서 손보고 검수합니다.

```text
서식 그림 ──▶ ① 대형 모델: 초안 폴더 (template.html.j2 + form.json)
                 │   그려 보며 원본과 맞춤 (python -m docgen.preview --dir)
                 ▼
             ② 사람: 검사 통과 확인 (생성 스크립트가 있으면 읽기) → studio 서식 폴더로 옮기기 → studio [서식 다시 읽기]
                 ▼
             ③ 사람: studio ① 서식에서 손보기 (값 출처, 빠진 칸, 위치) → 검수 완료
                 ▼
             ④ 시나리오·레시피에 넣어 데이터셋 생성
```

---

## 1. 모델이 만들 결과물

모델에게는 **폴더 하나에 파일 둘**을 만들게 합니다. 이 꼴이면 docgen·studio 가 그대로 받습니다.

```text
<이름>/
  template.html.j2   모양 + 값 자리 (Jinja2 html)
  form.json          서식 이름·그룹 + 칸 목록 (키마다 항목명·타입·값 출처)
  source.png         (선택) 원본 그림 — studio 에서 겹쳐 보기용
  generate.py        (선택) 생성 스크립트 — 칸끼리 관계(순서·합계·잔액·조건·표기)를 맞출 때
```

서식은 **템플릿 하나 + 칸 목록**으로, 고객 정보·행 수·글꼴을 바꿔 가며 문서를 계속 찍어 냅니다.
그래서 템플릿에는 원본의 모양(표·문구·선)과 "어디에 어떤 키의 값이 들어가는지"만 있고, 원본에 적힌 개인 값은 없습니다.

### template.html.j2 — 지킬 것

```jinja
{% extends "_base.html.j2" %}
{% import "_macros.html.j2" as m with context %}
{% block style %} .page { padding: 60px 56px; --fs: 12px; } table.t tr { height: 26px; } {% endblock %}
{% block content %}
  {{ m.title("거 래 내 역 확 인 서") }}
  <table class="t"> … <td>{{ f("holder.name", label="예금주") }}</td> … </table>
  {% for r in d.rows %}<tr><td>{{ f("rows." ~ loop.index0 ~ ".date", label="거래일") }}</td>…</tr>{% endfor %}
  {{ m.choice("purpose", ["대출신청", "기타"], label="용도") }}
  {{ m.seal("은행인", key="seal.bank", kind="직인") }}
{% endblock %}
```

| 규칙 | 이유 |
|---|---|
| 첫 두 줄 그대로, 쪽은 794×1123px (A4) | 공통 틀이 글꼴·쪽 나눔을 맡음. 넘치면 자동으로 다음 쪽 |
| **값 자리는 모두 `f("키", label="원본 항목명")`** (체크 `m.choice`, 도장 `m.seal`, 서명 `m.sigspot`) | `{{ d.x }}` 로 찍으면 그림엔 나와도 **정답 라벨에서 빠짐** |
| 행 수가 바뀌는 표는 `{% for r in d.rows %}` + `f("rows." ~ loop.index0 ~ ".키")` | 행 수를 바꿔 가며 찍기 위해 |
| 행 높이는 `tr { height: …px }` 로 직접, 열 너비는 `<colgroup>` % | padding 으로 맞추면 차이가 행마다 쌓임 |
| 외부 URL·스크립트·실제 로고·관인 그림 없음 | 도장은 `m.seal` 글자 도장만 |

### form.json — 칸 목록

```json
{"name": "거래내역확인서", "group": "finance", "category": "external", "page": "a4", "origin": "analyzer", "parent": null,
 "source_image": "source.png",
 "fields": {
  "holder.name": {"label": "예금주", "type": "text",     "source": "profile.person.name"},
  "purpose":     {"label": "용도",   "type": "checkbox", "source": "rule:choice", "choices": ["대출신청", "기타"]}},
 "lists": {
  "rows": {"min": 5, "max": 30, "fields": {
    "date": {"label": "거래일", "type": "date", "source": "rule:date_seq"}}}}}
```

- 템플릿의 키마다 한 줄. `type`: `text` `amount` `number` `date` `checkbox` `seal` `signature`.
- `source`(값 출처): `profile.<경로>`(합성 고객 정보) · `rule:<종류>`(그럴듯한 값: `date` `amount` `account` `phone` `address` `company` `person` `branch` `note` …) · `rule:choice` · `rule:fixed` · `rule:date_seq`(행마다 늘어나는 날짜).
- **값 출처는 나중에 studio 에서 고칠 수 있습니다.** 모델이 모르겠으면 `rule:note` 로 두게 합니다. 처음에 중요한 것은 **키와 위치**입니다.

### 키 이름 — 가장 중요

키는 학습 데이터의 정답 키가 됩니다. 서식마다 제각각이면 학습 데이터가 흩어집니다.

- 영어 소문자·숫자·밑줄, 점으로 나눈 "누구의 무엇": `applicant.name`, `account.number`, `lessor.address`.
- **있는 키를 먼저**: `docgen/dictionary/common.json`(공통 키), `docgen/keys.json`(서식들이 쓰는 키), `docgen/dictionary/parties.json`(누구).
- `account` 와 `account.number` 처럼 한 키가 다른 키의 앞부분이면 안 됨. 도장·서명 키는 `seal.`·`sign.` 으로 시작.

### generate.py — 칸끼리 관계 (선택)

칸 목록은 칸마다 값을 따로 뽑습니다. "시작일 ≤ 종료일", "합계 = 행 금액의 합", "기타를 골랐을 때만 사유" 처럼 칸끼리 맞아야 하면
`generate.py` 의 `adjust(d, p, rng)` 가 채운 값을 다듬습니다. 날짜·금액 계산 도우미는 `docgen.formkit`.

```python
from docgen.formkit import to_amount, amount_like, rows

def adjust(d, p, rng):
    d["total"]["out"] = amount_like(sum(to_amount(r["out"]) or 0 for r in rows(d, "rows")), d["total"]["out"])
    return d
```

약속: 난수는 `rng` 만, 시간·파일·네트워크 금지, 키는 칸 목록에 있는 것만 (어기면 검사 경고). 그림마다 실행되는 코드라 **사람이 읽고 넣습니다** (5절).

전체 규칙(매크로·CSS 클래스·값 출처 목록·생성 스크립트·흔한 실수·검사 통과한 전체 예시)은 [docgen/manual/NEW_FORM_SPEC.md](../docgen/manual/NEW_FORM_SPEC.md) 입니다. **모델에게는 이 파일을 통째로 줍니다.**

---

## 2. 시작 전에

| 확인 | 내용 |
|---|---|
| **어떤 그림을 모델에 보내나** | 외부 대형 모델(클로드 등)에는 **빈 서식·공개 서식 그림만**. 값이 적힌 실서류 견본은 외부로 보내지 않습니다 (AGENTS.md 규칙 10). 실서류 견본뿐이면 사내 모델에 맡기거나, 빈 서식 그림을 구합니다 |
| 서식 ID | 영어 소문자로 시작, 소문자·숫자·밑줄 3~51자. 겹치는지 `python -m docgen.formdir path <ID>` (없다고 나와야 함) |
| 같은 서식이 이미 있나 | studio ① 서식에서 이름 검색. 비슷한 html 서식이 있으면 새로 만들기보다 **복제** 후 고치는 편이 빠름 |
| 넣을 곳 | 공개·빈 서식에서 만든 것: `docgen/forms/<ID>/` · 실서류에서 만든 것: 사내 서식 폴더 `$DOCGEN_PRIVATE_FORMS/<ID>/` |

---

## 3. 모델에게 맡기기

### 넘길 것

- 서식 그림 (여러 쪽이면 쪽마다)
- [docgen/manual/NEW_FORM_SPEC.md](../docgen/manual/NEW_FORM_SPEC.md)
- 키 사전: `docgen/dictionary/common.json`, `docgen/keys.json` (저장소를 열 수 있는 모델이면 경로만)

### 지시문 (그대로 붙여 넣기, `<…>` 만 바꿈)

```text
첨부한 서식 그림과 똑같이 생긴 docgen html 서식을 만들어라. 형식은 NEW_FORM_SPEC.md 를 따른다.

결과: work/<이름>/template.html.j2 와 work/<이름>/form.json (form.json 에 fields·lists 포함, 9절 예시 꼴).
- 그림에 인쇄된 글자(제목·항목명·안내문·보기·주석)는 빠짐없이 옮긴다. 그림에 적힌 개인 값(이름·번호·주소·금액)은 옮기지 말고 값 자리로 바꾼다.
- 사람이 쓰거나 출력되어 채워지는 자리는 모두 값 자리로 만든다: 글자 f(), 체크 m.choice, 도장 m.seal, 서명 m.sigspot.
  label 은 그림에 인쇄된 항목명 그대로.
- 행 수가 바뀌는 표는 {% for r in d.<목록> %} 반복 행과 form.json lists(min = 그림에 보이는 행 수)로.
- 키는 docgen/dictionary/common.json, docgen/keys.json 에 있는 것을 먼저 쓰고, 없으면 "누구의 무엇" 영어 키를 새로 짓는다.
- 값 출처(source)는 맞는 profile.* 이나 rule:* 를 고르고, 모르겠으면 rule:note.
- 칸끼리 관계(시작일 ≤ 종료일, 합계 = 행의 합, 잔액, 조건부 칸, 금액 한글 표기)가 있으면 work/<이름>/generate.py 의
  adjust(d, p, rng) 로 맞춘다 (NEW_FORM_SPEC.md 8절: docgen.formkit 과 표준 라이브러리만, 난수는 rng 만, 새 키 금지).
- 서식 이름: <서식 이름>, 그룹: <finance 등>, 종류: <external|internal>

끝내기 전에 아래 두 명령으로 그려서 원본 그림과 비교하고, 비슷해질 때까지 고친다.
  python -m docgen.preview --dir work/<이름> --rows min --out work/<이름>_min
  python -m docgen.preview --dir work/<이름> --rows max --out work/<이름>_max
마지막 줄 JSON 에서 overflow 가 false, checks 가 [] 이고, --rows min 의 pages 가 원본 쪽 수와 같아야 한다.
판단이 안 선 칸(값 자리인지, 누구의 값인지)은 목록으로 따로 적어 보고한다.
```

- **명령을 직접 돌릴 수 있는 모델**(클로드 코드처럼 저장소에서 일하는 에이전트)이면 그려 보고 고치기를 스스로 반복합니다.
- **채팅만 되는 모델**이면 사람이 위 명령을 대신 돌리고, 그려진 그림(`images` 경로)과 마지막 줄 JSON 을 붙여 "원본과 다른 곳을 고쳐"로 몇 번 주고받습니다.

---

## 4. 검사

모델이 끝났다고 해도 사람이 한 번 더 돌립니다.

```bash
python -m docgen.preview --dir work/<이름> --rows min --out work/check_min
python -m docgen.preview --dir work/<이름> --rows max --out work/check_max
```

| 볼 것 | 통과 |
|---|---|
| 명령이 오류 없이 끝남 | 템플릿 문법이 맞음 |
| `overflow` | `false` |
| `checks` | `[]` — 키가 칸 목록과 템플릿에서 안 맞으면 여기 나옴 |
| `pages` (`--rows min`) | 원본 쪽 수와 같음 (`--rows max` 는 늘어도 됨, 자동 쪽 나눔) |
| 그림 (`images` 경로) | 원본과 나란히 놓고: 표 구조·문구가 같은지, 값이 칸 안에 들어가는지 |
| 템플릿에 `{{ d.` | 없어야 함 (값을 직접 찍으면 정답 라벨에서 빠지는데 검사가 못 잡음) |
| `generate.py` (있으면) | **사람이 읽음**: `docgen.formkit`·표준 라이브러리만 쓰는지, 파일·네트워크·`os`·`subprocess` 가 없는지, 하는 일이 원본의 칸 관계와 맞는지. seed 몇 개로 그려 관계가 지켜지는지 |

---

## 5. studio 에 넣기

초안 폴더를 서식 폴더 꼴(`look/template.html.j2` + `form.json` + `fields.json`)로 옮깁니다. 저장소 루트에서:

```bash
# 공개·빈 서식에서 만든 것 → docgen/forms/<ID>/
python - work/<이름> <서식ID> <<'EOF'
import json, shutil, sys
from pathlib import Path
from docgen import formdir, htmlform as H
src, form_id, root = Path(sys.argv[1]), sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else None)
assert H.ID_RX.fullmatch(form_id), "서식 ID 형식 (영어 소문자로 시작, 소문자·숫자·밑줄 3~51자)"
dest = formdir.new_dir(form_id, Path(root) if root else None)   # 이미 있으면 멈춤 (덮어쓰지 않음)
shutil.copyfile(src / "template.html.j2", dest / "look" / formdir.TEMPLATE)
H.write_form(dest, json.loads((src / "form.json").read_text(encoding="utf-8")))   # form.json + fields.json 으로 나눔
for extra in ("source.png", "generate.py", "questions.json"):   # 원본 그림, 생성 스크립트(읽고 확인한 것만), 질문·답 (있으면)
    if (src / extra).exists():
        shutil.copyfile(src / extra, dest / extra)
print(dest)
EOF
```

실서류에서 만든 서식은 명령 끝에 사내 서식 폴더를 더 적습니다: `python - work/<이름> <서식ID> "$DOCGEN_PRIVATE_FORMS" <<'EOF'` (나머지 같음).

그다음 **studio ① 서식 › [서식 다시 읽기]** 를 누릅니다. "새로 1" 과 함께 목록에 나오면 끝입니다 (studio 를 다시 띄우지 않아도 됨).
폴더가 깨져 있으면 등록하지 않고 이유(JSON·템플릿 문법 몇 번째 줄·ID 형식·ID 겹침)를 보여 줍니다.

확인:

```bash
python -m docgen.formdir path <서식ID>                    # 파일 자리
python -m docgen.regions check <서식ID>                   # 칸 목록 형식
python -m docgen.preview <서식ID> --rows max --out work/<서식ID>
python -m docgen.formdir questions <서식ID> --write        # 질문·답 파일 questions.json (지금 규칙 그대로) — 고치는 법 qa.md
```

---

## 6. studio 에서 손보기

① 서식 › 그 서식을 엽니다. 고칠 것에 따라 화면이 다릅니다.

| 고칠 것 | 어디서 |
|---|---|
| 값 출처 (값이 그럴듯하지 않음, 서로 안 맞음) | **영역 편집**: 칸을 눌러 오른쪽에서 값 출처·고정 값 |
| 빠진 **단독** 칸 추가, 칸 위치·크기 | **영역 편집**: 그림 위에서 그리기·끌기 |
| 체크 보기, 도장, 서명 | **html 편집** (템플릿) |
| **반복 표 안의 칸**, 표 구조, 인쇄 문구, 선 | **html 편집** (템플릿), 또는 모델에게 다시 맡기기 |
| 키 이름 | `fields.json` 과 템플릿을 같이 (html 편집) |
| 칸끼리 관계 (순서·합계·조건·표기) | 서식 폴더의 `generate.py` (파일로. 내용은 **파일** 탭에서 보임) |
| 질문 문장·답 꼴, 묻는 칸·질문의 항목명, 이 서식만의 질문 | 서식 폴더의 `questions.json` (파일로. **문항 Q/A** 탭에서 내용과 실제 문항을 봄, [qa.md](qa.md)) |

- 영역 편집으로 그린 칸은 **쪽 위의 고정 위치**라 행 수가 바뀌어도 따라 움직이지 않습니다. 반복 표 안의 칸은 템플릿에서 고칩니다.
- 이미 등록된 서식의 템플릿·`fields.json` 을 파일로 고친 것은 [서식 다시 읽기] 없이 다음 미리보기에 바로 나옵니다.
- 모양을 다시 크게 고쳐야 하면 [docgen/manual/FORM_SHELL_GUIDE.md](../docgen/manual/FORM_SHELL_GUIDE.md) 와 함께 모델에게 맡깁니다 (키는 그대로 두고 모양만).

---

## 7. 검수하고 데이터셋에 넣기

1. **검수**: ① 서식 › 검수 탭. 미리보기를 원본과 나란히 보고(행 최소·최대, seed 몇 개) **검수 완료**. 학습/평가 배정도 여기서.
   형식 검사 통과는 검수 완료가 아닙니다 (AGENTS.md 규칙 7). 검수 뒤 서식 파일이 바뀌면 "재검수 필요"로 돌아갑니다.
2. **업무에 넣기**: ③ 시나리오·묶음에서 그 서식이 제출되는 업무에 더합니다 ([studio.md](studio.md)).
3. **데이터셋**: ⑥ 데이터셋 › 새로 만들기(레시피)에서 서식·시나리오를 고릅니다.
   **html 서식은 검수 전이어도 레시피의 `"all"`·그룹 선택에 들어갑니다.** 검수한 서식만 쓰려면 레시피의 **검수 완료 서식만**(`reviewed_only`)을 켜거나, 검수가 끝날 때까지 `exclude` 에 그 ID 를 적어 둡니다.

---

## 8. 문제 해결

| 증상 | 할 일 |
|---|---|
| checks: `form.json 에 선언했는데 템플릿에 안 나오는 키` | 칸 목록에만 있는 키 → 템플릿에 넣거나 칸 목록에서 빼기 |
| checks: `템플릿에 있는데 값이 없는 키` | 템플릿 키가 칸 목록에 없음 (오타 포함) |
| 한 쪽 서식이 2쪽으로 | 높이·간격·글자 크기를 줄이게 모델에 다시 |
| 아래쪽이 점점 밀림 | 행 높이를 px 로 직접 (padding 아님) |
| `키 'a' 와 'a.b' 를 함께 쓸 수 없습니다` | 1절 키 이름 규칙 (한 키가 다른 키의 앞부분) |
| [서식 다시 읽기] 의 문제: `코드 서식과 ID 가 겹칩니다` | 다른 ID 로 폴더 이름을 바꾸고 다시 누르기 |
| 5절 명령이 `FileExistsError` | 같은 ID 폴더가 이미 있음. 다른 ID 를 쓰거나, 기존 서식을 고칠 거면 6절로 |
| `생성 스크립트 generate.py N번째 줄: …` | 그 줄의 오류. 이 서식만 그려지지 않음 |
| checks: `같은 seed 로 두 번 돌렸는데 결과가 다릅니다` | 스크립트가 `rng` 말고 `random`·시간 등을 씀 → `rng` 로 |
| checks: `칸 목록에 없는 키를 만들었습니다` | 스크립트가 새 키를 만듦 → 칸 목록 `fields` 에 선언하고 템플릿에 `f()` 로, 아니면 지우기 |
| 목록의 "키" 수가 0 | 목록의 그 칸은 미리 만든 카탈로그에서 읽어 새 서식은 0. 상세·미리보기에는 정상으로 나옴 |
