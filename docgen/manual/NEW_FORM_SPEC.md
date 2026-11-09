# 새 서식 만들기: 결과물 형식

이미지를 보고 html 서식을 만드는 도구(사람·VLM·직접 만든 스크립트 무엇이든)가 **무엇을 내놓으면 docgen·studio 가 그대로 받는지** 정리한 문서입니다.
만드는 방법은 자유이고, 결과물만 이 꼴이면 됩니다. 아래 예시는 실제로 그려 보고 검사를 통과한 것입니다.

> 실서류에서 만든 서식의 그림은 외부 모델·서비스에 보내지 않습니다 (AGENTS.md 규칙 10). 사내 모델만 씁니다.

---

## 1. 한눈에

서식 하나 = 폴더 하나입니다. 결과물 꼴은 두 가지이고, 내용은 같습니다.

```
A. 초안 폴더 (만들면서 검사할 때)            B. 등록 폴더 (studio 에 넣을 때)
<아무 곳>/<이름>/                            docgen/forms/<서식ID>/          (공개 서식)
  template.html.j2   모양 + 값 자리           $DOCGEN_PRIVATE_FORMS/<서식ID>/  (실서류에서 만든 것)
  form.json          이름·그룹 + 칸 목록        look/template.html.j2     A 의 template.html.j2 그대로
  source.png         (선택) 원본 그림           form.json                 이름·그룹·출처만
  generate.py        (선택) 생성 스크립트       fields.json               칸 목록 (A 의 form.json 에서 fields·lists)
  qa.py              (선택) 서식 전용 질문      source.png                (선택) 원본 그림
                                                generate.py               (선택) 생성 스크립트 (8절)
                                                qa.py                     (선택) 서식 전용 질문 (10절)
```

- **A** 는 `python -m docgen.preview --dir <폴더>` 로 바로 그려 볼 수 있습니다. 만드는 도구가 고치고 그려 보기를 반복할 때 씁니다.
- **B** 는 폴더를 그 자리에 두기만 하면 등록됩니다 (studio ① 서식 › **서식 다시 읽기** 를 누르면 목록에 나옴). 따로 등록 명령이나 목록 파일 수정은 없습니다.
- A → B 는 파일을 옮기고 `form.json` 의 `fields`·`lists` 를 `fields.json` 으로 떼어 내면 끝입니다 (6절).
  B 에 `fields.json` 없이 A 의 `form.json` 을 그대로 둬도 읽습니다 (예전 꼴). 그래도 B 꼴로 두는 것을 권합니다.

서식이 문서를 만드는 원리: **템플릿 하나 + 칸 목록**으로, 고객 정보·행 수·글꼴·선 굵기를 바꿔 가며 문서를 계속 찍어 냅니다.
템플릿은 모양과 "어디에 어떤 키의 값이 들어가는지"만 갖고, 실제 값은 칸 목록의 값 출처(`source`)가 매번 만듭니다.

---

## 2. 템플릿 `template.html.j2`

Jinja2 + HTML 입니다. 쪽은 **A4 세로 794 × 1123 px** 입니다.

### 뼈대 (그대로)

```jinja
{% extends "_base.html.j2" %}
{% import "_macros.html.j2" as m with context %}
{% block style %}
  /* 이 서식 전용 CSS */
{% endblock %}
{% block content %}
  … 내용 …
{% endblock %}
```

- 첫 두 줄은 바꾸지 않습니다. 공통 틀(`docgen/forms/_common/templates/_base.html.j2`)이 글꼴·쪽 크기·쪽 나눔을 맡습니다.
- 내용이 한 쪽을 넘으면 **자동으로 다음 쪽으로 나뉩니다** (반복 표는 머리글이 다음 쪽에 다시 나옴). 쪽을 직접 나누지 않습니다.

### 값 자리: 반드시 이 문법으로

값이 들어가는 자리는 **모두** 아래 중 하나로 씁니다. `{{ d.x }}` 처럼 직접 찍으면 그림에는 나오지만 **정답 라벨에서 빠집니다**.

| 자리 | 쓰는 법 | 정답 라벨 |
|---|---|---|
| 글자 값 | `{{ f("holder.name", label="예금주") }}` | key·label·value·bbox |
| 체크 보기 (■/□) | `{{ m.choice("purpose", ["대출신청", "기타"], label="용도") }}` | 고른 보기 |
| 동의 체크 | `{{ m.agree("consent.marketing", "동의함", "동의하지 않음", label="마케팅 동의") }}` | 고른 쪽 |
| 도장 | `{{ m.seal("은행인", key="seal.bank", kind="직인") }}` | 도장 표시 |
| 서명·날인 자리 | `{{ m.sigspot("sign.applicant", val("applicant.name")) }}` (두 번째 = 그 사람 이름) | 서명/도장 표시 |
| 반복 표 (행 수가 바뀜) | 아래 |  행마다 |

- `label` 은 **원본에 인쇄된 항목명** 그대로 씁니다 (정답의 `label` 이 됩니다).
- 같은 값이 서식에 두 번 나오면 같은 키를 두 번 써도 됩니다.
- 값으로 모양을 바꿀 때(조건 칸)는 `val("키")` 나 `d.키` 로 읽습니다: `{% if val("purpose") == "기타" %}…{% endif %}`.

**반복 표** — 칸 목록의 `lists` 이름(예: `rows`)과 맞춥니다:

```jinja
{% for r in d.rows %}
<tr><td>{{ f("rows." ~ loop.index0 ~ ".date", label="거래일") }}</td>
    <td class="num">{{ f("rows." ~ loop.index0 ~ ".out", label="출금") }}</td></tr>
{% endfor %}
```

또는 매크로 한 줄: `{{ m.grid(["거래일", "출금"], "rows", ["date", "out"], num_cols=[1]) }}`.

### 모양 규칙 (원본과 비슷하게)

- 쪽 여백·기본 글자: `.page { padding: 60px 56px; --fs: 12px; --lh: 1.3; }`
- 표: `table-layout: fixed`, 열 너비는 `<colgroup>` 의 %.
- **행 높이는 `tr { height: 26px; }` 처럼 px 로 직접.** padding 으로 맞추면 차이가 행마다 쌓입니다.
- 합친 칸은 `colspan`·`rowspan`. 덩어리 사이 간격은 margin px.
- 쓸 수 있는 공통 클래스: `right` `center` `bold` `small` `tiny` `muted` `num`(숫자 오른쪽 정렬) `c`(가운데) `mt` `mb` `box` `note`, 표 `table.compact` `table.plain`.
- 그 밖의 매크로: `m.title(제목)`, `m.kv([[라벨, 키], …], cols=2)`, `m.issuer(날짜키, org_text="…", seal_text="…")`, `m.doc_no(키)`.
  전체 목록은 `docgen/forms/_common/templates/_macros.html.j2`, 설명은 [11절](#11-매크로css-전체).

### 넣지 않는 것

- 외부 URL (그림·글꼴·스크립트), `<script>`
- 실제 기관 로고·관인 그림·바코드·QR (도장은 `m.seal` 글자 도장만)
- 원본에 적힌 개인 값 (이름·번호·주소) — 모두 값 자리로 바꿉니다

---

## 3. 칸 목록 (A: `form.json` 안 / B: `fields.json`)

템플릿에 쓴 키마다 **값을 어디서 만들지** 적습니다.

```json
"fields": {
  "holder.name":    {"label": "예금주",   "type": "text",     "source": "profile.person.name"},
  "account.number": {"label": "계좌번호", "type": "text",     "source": "rule:account"},
  "purpose":        {"label": "용도",     "type": "checkbox", "source": "rule:choice", "choices": ["대출신청", "기타"]}
},
"lists": {
  "rows": {"min": 5, "max": 30, "fields": {
    "date": {"label": "거래일", "type": "date",   "source": "rule:date_seq"},
    "out":  {"label": "출금",   "type": "amount", "source": "rule:amount"}}}
}
```

| 칸 | 값 |
|---|---|
| `label` | 원본 항목명 |
| `type` | `text` `amount` `number` `date` `checkbox` `seal` `signature` |
| `source` | 값 출처 (아래) |
| `choices` | `rule:choice` 일 때 보기 목록 (템플릿 `m.choice` 의 보기와 같게) |
| `text` | `rule:fixed` 일 때 늘 쓸 글자 |
| `description` | (선택) 항목 설명 |
| `lists.<이름>.min`·`max` | 반복 표 행 수 범위. min = 원본에 보이는 행 수가 무난 |

**값 출처 `source`** (`docgen/sources.py`)

| 쓰는 법 | 값 |
|---|---|
| `profile.<경로>` | 합성 고객 프로필. 예: `profile.person.name`, `profile.person.rrn`, `profile.person.address.road_short`, `profile.person.phone`, `profile.employment.company.name`. 한 문서 안에서 서로 맞는 값(같은 사람)이 필요하면 이쪽 |
| `rule:<종류>` | 종류에 맞는 그럴듯한 값: `date` `amount` `fx_amount` `percent` `rate` `currency` `account` `phone` `number` `count` `biz_no` `passport` `check_no` `product` `goods` `reason` `bank` `branch` `country` `email` `address` `company` `person` `note` … |
| `rule:choice` | `choices` 중 하나 |
| `rule:fixed` | `text` 그대로 |
| `rule:free_text` | 짧은 자유 문장 (가끔 빈 칸) |
| `rule:empty` | 늘 빈 칸 |
| `rule:date_seq` | 반복 행에서 행마다 늘어나는 날짜 |

`rule:` 값은 칸마다 따로 뽑습니다 (예: 합계가 행 금액의 합과 다름, 발급일이 조회기간보다 앞섬). 같은 사람의 값은 `profile.` 로 맞추고,
**칸끼리 관계(순서·합계·잔액·조건·표기)는 생성 스크립트 `generate.py` 로 맞춥니다 (8절).**
값 출처를 다 정하지 못했으면 `rule:note`(아무 글자) 로 두고 studio ① 서식에서 고쳐도 됩니다. **키와 위치만 맞으면 값 출처는 나중에 고칠 수 있습니다.**

---

## 4. 키 이름

키는 학습 데이터의 정답 키가 됩니다. 사람마다 다르게 지으면 학습 데이터가 흩어지므로 가장 신경 쓸 곳입니다.

- 영어 소문자·숫자·밑줄, 점으로 나눈 경로: `applicant.name`, `account.number`, `rows.0.date`.
- **이미 있는 키를 먼저 씁니다.** 키 사전: `docgen/forms/_common/dictionary/common.json`(공통 키), `docgen/forms/_common/keys.json`(서식들이 쓰는 키),
  `docgen/forms/_common/dictionary/parties.json`(누구: 신청인·대리인·임대인 …). "누구의 무엇"으로 짓습니다: `agent.name`, `lessor.address`.
- 한 키가 다른 키의 앞부분이면 안 됩니다: `account` 와 `account.number` 를 함께 쓸 수 없음.
- 반복 표 하위 키는 행 안의 이름만 (`date`, `out`). 템플릿에서는 `rows.<번호>.date` 로 씁니다.
- 도장·서명 키는 `seal.`·`sign.` 으로 시작: `seal.bank`, `sign.applicant`.

---

## 5. `form.json` (서식 정보)

```json
{"name": "거래내역확인서", "group": "finance", "category": "external", "page": "a4",
 "origin": "analyzer", "parent": null, "source_image": "source.png"}
```

| 칸 | 값 |
|---|---|
| `name` | 서식 이름 (원본 제목) |
| `group` | `identity` `family` `income` `tax` `finance` `real_estate` `business` `corporate` `fx` `bank_form` 중 하나 (없으면 finance) |
| `category` | `external`(고객이 가져오는 서류) / `internal`(은행 서식) |
| `page` | `a4` |
| `origin` | `analyzer` (이미지에서 만든 서식) |
| `parent` | `null` (기존 코드 서식의 값 생성을 빌릴 때만 그 서식 ID) |
| `source_image` | 원본 그림 파일 이름 (있으면 studio 편집기에서 겹쳐 보기) |

A(초안 폴더)에서는 여기에 `"fields"`·`"lists"` 를 같이 넣습니다.

---

## 6. 검사와 등록

**1) 초안 폴더 검사** — 행 최소·최대 둘 다:

```bash
python -m docgen.preview --dir <초안 폴더> --rows min --out out/min
python -m docgen.preview --dir <초안 폴더> --rows max --out out/max
# 마지막 줄 JSON: {"images": [...], "pages": 1, "fields": 28, "empty": 4, "overflow": false, "checks": []}
```

| 볼 것 | 통과 |
|---|---|
| 명령이 오류 없이 끝남 | 템플릿 문법·키 오류가 없음 |
| `overflow` | `false` |
| `checks` | `[]`. 칸 목록과 템플릿 키가 안 맞으면 여기 나옴 (아래 7절) |
| `pages` (`--rows min`) | 원본 쪽 수와 같음. `--rows max` 는 늘어나도 됨 (자동 쪽 나눔) |
| `fields` | 템플릿 값 자리 수와 맞음 |
| `images` 의 그림 | 원본과 나란히 놓고 눈으로 |

**2) 등록 (B 꼴로 옮기기)**

```
<초안>/template.html.j2      →  <서식ID>/look/template.html.j2
<초안>/form.json 의 fields·lists →  <서식ID>/fields.json   {"engine": "html", "unit": "px", "fields": …, "lists": …}
<초안>/form.json 의 나머지     →  <서식ID>/form.json
<초안>/source.png            →  <서식ID>/source.png
<초안>/generate.py           →  <서식ID>/generate.py       (있으면. 사람이 읽고 옮긴다 — 8절)
<초안>/qa.py                 →  <서식ID>/qa.py             (있으면. 사람이 읽고 옮긴다 — 10절)
```

- **서식 ID**: 영어 소문자로 시작, 소문자·숫자·밑줄 3~51자 (`[a-z][a-z0-9_]{2,50}`). 이미 있는 ID 는 쓰지 않습니다 (`python -m docgen.formdir path <ID>` 로 확인). 기존 폴더를 덮어쓰지 않습니다.
- **어디에**: 공개·빈 서식에서 만든 것은 `docgen/forms/<ID>/`, **실서류에서 만든 것은 `$DOCGEN_PRIVATE_FORMS/<ID>/`** (studio `private_forms_dir`).
- studio ① 서식 목록 위의 **서식 다시 읽기** 를 누르면 목록에 나옵니다 (다시 띄우지 않아도 됨). 폴더가 깨져 있으면 등록하지 않고 이유를 보여 줍니다 (JSON·템플릿 문법·ID 형식·코드 서식과 ID 겹침).
- 이미 등록된 서식의 템플릿·칸 목록을 고친 것은 누르지 않아도 다음 미리보기부터 반영됩니다. 버튼은 새 폴더, 지운 폴더, `form.json` 의 이름·그룹을 바꿨을 때 누릅니다.

**3) 등록 뒤 확인**

```bash
python -m docgen.formdir path <ID>                         # 파일 자리
python -m docgen.formdir check <ID>                        # 서식 검사 (칸 목록·박스·값 출처·질문·qa.py·카드)
python -m docgen.preview <ID> --rows max --out out/<ID>    # 등록된 서식으로 그리기
```

등록된 서식은 **검수 전** 상태입니다. studio ① 서식에서 사람이 원본과 비교해 검수 완료를 누릅니다.
**html 서식은 검수 전이어도 레시피의 `"all"`·그룹 선택에 들어갑니다.** 검수한 서식만 쓰려면 레시피에서 **검수 완료 서식만**(`reviewed_only`)을 켭니다 (검수 전에는 자동으로 빠지는 것은 가져온 이미지 서식 `img_*` 뿐).
형식 검사 통과는 검수 완료가 아닙니다 (AGENTS.md 규칙 7).

---

## 7. 흔한 실수

| 증상 | 원인 |
|---|---|
| 그림에는 값이 있는데 정답 라벨에 없음 | `{{ d.x }}` 로 직접 찍음 → `f("x", label=…)` 로. **검사가 잡지 못하니** 템플릿에서 `{{ d.` 를 찾아 보기 |
| checks: `form.json 에 선언했는데 템플릿에 안 나오는 키: …` | 칸 목록에만 있는 키 → 템플릿에 넣거나 칸 목록에서 빼기 |
| checks: `템플릿에 있는데 값이 없는 키 …` | 템플릿 `f("…")` 키가 칸 목록에 없음 (오타 포함) → 칸 목록에 더하기 |
| 아래쪽이 점점 밀림 | 행 높이를 padding 으로 맞춤 → `tr { height: …px }` |
| 한 쪽 서식이 2쪽으로 | 높이·간격·글자 크기 합이 1123px 초과 (`--rows min` 에서 `pages` 1 이어야) |
| `키 'a' 와 'a.b' 를 함께 쓸 수 없습니다` | 4절 앞부분 규칙 |
| 체크 보기 값이 엉뚱함 | `m.choice` 보기와 칸 목록 `choices` 가 다름 |

---

## 8. 생성 스크립트 `generate.py` (선택)

그림 위에 그린 서식(overlay)의 `generate.py` 는 같은 약속에 고칠 수 있는 칸이 다릅니다: [guide/generators.md 2절](../../guide/generators.md#2-칸끼리-관계-서식-폴더-generatepy-의-adjust).

칸 목록의 값 출처는 칸마다 값을 따로 뽑습니다. 칸끼리 관계가 있으면 서식 폴더에 `generate.py` 를 두고 **값을 다 채운 뒤 다듬습니다.**

```
칸 목록(fields)으로 값을 채운다 → generate.py 의 adjust(d, p, rng) → 템플릿에 넣어 그린다 → 정답 라벨
```

```python
from docgen.formkit import to_date, date_like, to_amount, amount_like, rows


def adjust(d, p, rng):
    """d: 칸 목록으로 채운 값 (dict, 고쳐서 돌려준다) · p: 고객 프로필 · rng: 이 문서의 난수."""
    s, e = to_date(d["period"]["start"]), to_date(d["period"]["end"])
    if s > e:                                                    # 조회 시작 ≤ 종료
        s, e = e, s
    d["period"]["start"], d["period"]["end"] = date_like(s, d["period"]["start"]), date_like(e, d["period"]["end"])
    d["issue_date"] = date_like(e, d["issue_date"])              # 발급일 = 조회 종료일
    for r in rows(d, "rows"):                                    # 행마다 출금·입금 중 하나만
        if rng.random() < 0.5:
            r["out"] = ""
        else:
            r["in"] = ""
    d["total"]["out"] = amount_like(sum(to_amount(r["out"]) or 0 for r in rows(d, "rows")), d["total"]["out"])  # 합계 칸 (칸 목록에 total.out 선언)
    return d
```

**`d` 의 꼴**: 키의 점 경로가 그대로 dict 입니다 (`period.start` → `d["period"]["start"]`, 반복 표 `rows` → `d["rows"]` = 행 dict 목록).
값은 서식에 찍힐 **글자**입니다 (`"2025.01.03"`, `"1,234,000원"`). 계산할 때는 도우미로 바꾸고 같은 표기로 되돌립니다.
빈 칸은 `""` 나 `None`.

**도우미** `docgen.formkit`

| 함수 | 하는 일 |
|---|---|
| `to_date(s)` / `date_like(date, 보기)` | `'2025.01.03'`·`'2025-01-03'`·`'2025년 1월 3일'` → date / date → 보기와 같은 표기 |
| `add_days(s, n)` | 날짜 글자에 n 일 더해 같은 표기로 |
| `to_amount(s)` / `amount_like(n, 보기)` | `'1,234,000원'` → 1234000 / 정수 → 보기와 같은 꼴 (쉼표·'원'·통화 유지) |
| `won_korean(n)` | 120000000 → `'일억이천만'` (금액 한글 표기) |
| `rows(d, "rows")` | 반복 표 행 목록 |
| `get(d, "a.b")` / `put(d, "a.b", 값)` | 점 경로로 읽기·쓰기 |

**약속** (검사가 잡는 것은 ✓)

| 약속 | |
|---|---|
| 함수 이름은 `adjust(d, p, rng)`, 값 dict 를 돌려준다 (`None` 이면 d 그대로) | ✓ 없으면 오류 |
| 난수는 넘겨받은 `rng` 만 쓴다. 시간·파일·네트워크·전역 상태를 읽지 않는다 | ✓ 같은 seed 로 두 번 돌려 다르면 경고 |
| **키는 칸 목록에 있는 것만 고친다.** 새 값 칸이 필요하면 칸 목록(`fields`)에 선언하고 템플릿에 `f()` 로 | ✓ 칸 목록에 없는 키를 만들면 경고 |
| `docgen.formkit` 과 파이썬 표준 라이브러리(`re`, `datetime`, `math`)만 쓴다 | 사람이 읽고 확인 |
| 오류가 나면 그 서식만 실패합니다 | `생성 스크립트 generate.py 3번째 줄: KeyError: …` |

- 초안 폴더에 두면 `python -m docgen.preview --dir` 도 스크립트를 실행합니다. 검사 경고는 `checks` 에 나옵니다.
- 스크립트도 서식 해시에 들어갑니다: 고치면 미리보기를 다시 그리고 검수 완료는 "재검수 필요" 로 바뀝니다.
- **그림을 그릴 때마다 실행되는 코드입니다.** 외부 모델이 쓴 스크립트는 사람이 읽고 서식 폴더에 넣습니다.
  studio 는 스크립트가 있는 서식에 `스크립트` 표시를 붙이고, [서식 다시 읽기] 결과와 서식의 파일 탭에 내용을 보여 줍니다.
- 기존 서식을 복제한 서식(`parent`)도 부모가 값을 만들고 칸 목록이 덮어쓴 뒤에 실행됩니다.

---

## 9. 전체 예시 (검사 통과)

`template.html.j2`

```jinja
{% extends "_base.html.j2" %}
{% import "_macros.html.j2" as m with context %}
{% block style %}
.page { padding: 60px 56px; --fs: 12px; --lh: 1.3; }
table.t { width: 100%; table-layout: fixed; border-collapse: collapse; }
table.t td, table.t th { border: 1px solid #000; padding: 0 6px; }
table.t tr { height: 26px; }
table.t th { background: #f2f2f2; font-weight: normal; }
{% endblock %}
{% block content %}
  {{ m.title("거 래 내 역 확 인 서") }}
  <table class="t">
    <colgroup><col style="width:18%"><col style="width:32%"><col style="width:18%"><col style="width:32%"></colgroup>
    <tr><th>예금주</th><td>{{ f("holder.name", label="예금주") }}</td>
        <th>계좌번호</th><td>{{ f("account.number", label="계좌번호") }}</td></tr>
    <tr><th>조회기간</th><td colspan="3">{{ f("period.start", label="조회시작일") }} ~ {{ f("period.end", label="조회종료일") }}</td></tr>
    <tr><th>용도</th><td colspan="3">{{ m.choice("purpose", ["대출신청", "기타"], label="용도") }}</td></tr>
  </table>
  <table class="t" style="margin-top:16px">
    <colgroup><col style="width:20%"><col style="width:40%"><col style="width:20%"><col style="width:20%"></colgroup>
    <tr><th>거래일</th><th>적요</th><th>출금</th><th>입금</th></tr>
    {% for r in d.rows %}
    <tr><td class="c">{{ f("rows." ~ loop.index0 ~ ".date", label="거래일") }}</td>
        <td>{{ f("rows." ~ loop.index0 ~ ".memo", label="적요") }}</td>
        <td class="num">{{ f("rows." ~ loop.index0 ~ ".out", label="출금") }}</td>
        <td class="num">{{ f("rows." ~ loop.index0 ~ ".in", label="입금") }}</td></tr>
    {% endfor %}
  </table>
  <p class="mt right">{{ f("issue_date", label="발급일") }}</p>
  <p class="right">{{ f("bank.branch", label="발급점") }} {{ m.seal("은행인", key="seal.bank", kind="직인") }}</p>
{% endblock %}
```

`form.json` (초안 폴더 꼴: 칸 목록 포함)

```json
{"name": "거래내역확인서", "group": "finance", "category": "external", "page": "a4", "origin": "analyzer", "parent": null,
 "fields": {
  "holder.name":    {"label": "예금주",     "type": "text",     "source": "profile.person.name"},
  "account.number": {"label": "계좌번호",   "type": "text",     "source": "rule:account"},
  "period.start":   {"label": "조회시작일", "type": "date",     "source": "rule:date"},
  "period.end":     {"label": "조회종료일", "type": "date",     "source": "rule:date"},
  "purpose":        {"label": "용도",       "type": "checkbox", "source": "rule:choice", "choices": ["대출신청", "기타"]},
  "issue_date":     {"label": "발급일",     "type": "date",     "source": "rule:date"},
  "bank.branch":    {"label": "발급점",     "type": "text",     "source": "rule:branch"}},
 "lists": {
  "rows": {"min": 5, "max": 30, "fields": {
    "date": {"label": "거래일", "type": "date",   "source": "rule:date_seq"},
    "memo": {"label": "적요",   "type": "text",   "source": "rule:free_text"},
    "out":  {"label": "출금",   "type": "amount", "source": "rule:amount"},
    "in":   {"label": "입금",   "type": "amount", "source": "rule:amount"}}}}}
```

검사 결과: `--rows min` 1쪽·값 28개, `--rows max` 2쪽(자동 나눔)·값 128개, 둘 다 `overflow: false`, `checks: []`.
B 꼴로 옮긴 뒤 `docgen.preview <ID>`, `docgen.regions check <ID>` 도 통과.

---

## 10. 이 서식만의 질문 `qa.py` (선택) · 서식 카드 `FORM.md`

질문·답은 따로 적지 않아도 됩니다. 기본 과제(분류·받아쓰기·정보 추출·체크)는 칸 목록에서 자동으로 만들어집니다.
이 서식에서만 묻고 싶은 질문이 있을 때만 초안 폴더에 `qa.py` 를 넣습니다. 함수 하나 = 질문 하나:

```python
def 신청금액(v):                    # v = 그린 문서의 칸 값 {키: 값} (칸 목록의 키)
    return "대출 신청금액은 얼마입니까? 원 단위 숫자로만 답하세요.", number(v["loan.amount"])


def 보증인(v):                      # True/False → 예/아니오
    return "보증인 성명이 적혀 있습니까? 예/아니오로 답하세요.", v.get("guarantor.name") is not None
```

- 파일 맨 위에 `from docgen.formqa import number, date, months` (도우미가 필요하면).
- `(질문, 정답)` 을 돌려줍니다. 정답 **값**은 적지 않고 `v` 에서 꺼냅니다 — 문서를 그릴 때마다 그 칸 값으로 정해집니다.
- 답 꼴(숫자만, 예/아니오, JSON 칸 이름)을 질문 문장에 적습니다. 채점은 정답 꼴로 정해집니다.
- 자세한 규칙: [서식 폴더 설명서 5.3절](../forms/README.md#53-이-서식만의-질문-qapy).
- 기본 과제의 질문 문장·답 모양을 바꾸는 `questions.json`, 칸마다 묻기·항목명을 정하는 칸의 `"q"` 는 보통 쓰지 않습니다
  ([서식 폴더 설명서 5.1·5.2절](../forms/README.md#5-질문과-답-고치기)).

**등록한 뒤** 서식 카드를 만듭니다. 카드는 항목·위치·정한 곳·실제 질문→답을 적은 읽는 문서입니다 (자동 생성, 직접 고치지 않음):

```bash
python -m docgen.formdir card <ID>                  # docgen/forms/<ID>/FORM.md
python -m docgen.formdir check <ID>                 # 서식 검사: 칸 목록·값 출처·질문 설정·questions.json·qa.py
```

---

## 11. 매크로·CSS 전체

주요 매크로 (`docgen/forms/_common/templates/_macros.html.j2`):

| 매크로 | 용도 |
|---|---|
| `m.title(text, sub=None, boxed=False)` | 문서 제목 |
| `m.kv(rows, cols=1, label_w=None)` | 라벨/값 표. `[라벨, 경로, True]`는 한 줄 전체를 차지한다 |
| `m.grid(headers, list_path, keys, num_cols=[], widths=None, min_rows=0)` | 목록 표 |
| `m.choice(path, options, label=None)` | ■/□ 선택 항목 (선택된 값만 GT로 기록) |
| `m.agree(path, yes, no)` | 동의/미동의 체크 |
| `m.seal(text, square=False, size="sm"\|"lg", over=False)` | 도장 |
| `m.issuer(date_path, org_path=None, org_text=None, seal_text=None)` | 발급일 + 기관명 + 직인 |
| `m.sign(label, path, mark="(서명 또는 인)")` | 서명란 |
| `m.doc_no(path, label="발급번호")` | 상단 발급번호 |

`_base.html.j2`의 CSS 클래스:
- 배치: `row`, `between`
- 정렬·글자: `right`, `center`, `bold`, `small`, `tiny`, `muted`, `accent`
- 상자·안내문: `box`, `note`
- 간격: `mt`, `mb`, `mt-l`
- 표: `num`, `c`, `table.compact`, `table.outer`, `table.plain`
- 조항 목록: `ol.clauses`
- 사진 자리: `.photo`
- 공문서 상단 줄: `.gov-head`
- 글자가 많은 서류: `{% block page_class %} dense{% endblock %}`로 글자를 줄인다.

`style.*` 변수(폰트, 테두리, 배경색)는 샘플마다 랜덤으로 바뀐다. 색과 폰트는 하드코딩하지 말고 CSS 변수(`var(--accent)`, `var(--border)`, `var(--label-bg)`, `var(--seal)`)를 쓴다. 신분증류처럼 고유 디자인이 필요할 때만 예외로 한다.

---

## 12. 코드 서식 (값을 파이썬 함수가 만드는 서식)

html 서식은 칸 목록의 값 출처가 값을 만들고, **코드 서식**은 서식 폴더 `generate.py` 의 `@doc` 함수가 값 전부를 만듭니다 (지금 70종). 새로 만들 때는 보통 html 서식(1~10절)이 쉽고, 칸끼리 얽힌 계산이 많을 때만 코드 서식으로 만듭니다. 템플릿 규칙(2절)은 같습니다.

코드 서식(값을 파이썬이 만드는 서식) 한 종을 추가하려면 서식 폴더에 **생성 함수 1개 + 템플릿 1개**를 만들고 그룹 모듈에 등록한다.

```
docgen/forms/<서류ID>/generate.py             @doc(...) 로 등록하는 생성 함수
docgen/forms/<서류ID>/look/template.html.j2   Jinja2 HTML 템플릿 (registry 이름은 "<그룹>/<서류ID>.html.j2")
docgen/docs/<그룹>.py                         끝의 FORMS 목록에 <서류ID> 를 더한다 (등록 차례 = 서식 목록·데이터셋 순서).
                                              같은 그룹 서식들이 같이 쓰는 도우미도 여기
```

예시: `docgen/forms/employment_certificate/generate.py`(값)와 `docgen/forms/employment_certificate/look/template.html.j2`

다 만들면 `python -m docgen.formdir declare <서류ID> --apply` 로 칸 목록 `docgen/forms/<서류ID>/fields.json` 에 칸을 적습니다
(값은 생성 함수 그대로 `"source": "code"`, 키 하나만 값 출처를 바꿔 덮어쓸 수 있음 — docgen/README.md "서식 수정 파일").

### 생성 함수

```python
# docgen/forms/<서류ID>/generate.py
from docgen.docs._common import *  # D, won, K, special, issue_no, district_office, tax_office, courthouse, rand_date, date, timedelta ...
from docgen.registry import doc

@doc("employment_certificate", "재직증명서", "income")       # (id, 한글명, 그룹, category="external"|"internal", page="a4"|"a4_landscape"|"card"|"passport", sample_mark=False)
def employment_certificate(p: Profile, rng: random.Random) -> dict:
    """한 줄 설명."""
    return {"employee": {"name": p.person.name, ...}, "items": [{"name": ..., "amount": won(1000)}], ...}
```

- `p: Profile`에는 고객 1명의 일관된 정보가 들어 있다. 자세한 내용은 `docgen/entities.py`를 본다.
  - 본인·가족: `p.person`, `p.spouse`, `p.children`, `p.father`, `p.mother`, `p.address_history`
  - 근무처: `p.employment` (`.company`, `.annual_salary` 등)
  - 사업체: 개인사업체 `p.business`, 법인 `p.corporation`, 임원 `p.directors`, 주주 `p.shareholders`
  - 부동산: `p.property`
  - 금융: `p.accounts`, `p.bank`, `p.bank_branch`
  - 해외 거래처: `p.foreign`
  - 기준일: `p.issue_date`
- **은행 서식(`bank_form` 그룹)은 서식을 낸 은행 기준 프로필을 받는다.** `p.bank`가 외환은행·KEB하나은행 같은 옛 은행이면 `p.issue_date`를 포함한 모든 날짜가 그 시기로 옮겨져 있다(`docgen/banks.py`).
  - 시기에 따라 달라지는 제도(예금자보호한도, 금소법 문구 등)는 `banks.since(p.issue_date, "fsca")`처럼 날짜로 판단한다.
  - 템플릿에는 `bk`(은행명·법인명칭·영문명·`bk.rev()` 개정년월·시기 플래그)가 넘어온다. 표시 전용이며 GT가 아니다. 다른 그룹 템플릿에서는 `bk`가 `None`이다.
- **같은 고객의 다른 서류와 값이 맞아야 한다.** 예를 들어 소득금액증명원의 소득은 `p.employment.annual_salary`를 기준으로 계산한다. 이름, 주소, 주민번호, 회사 정보는 프로필 값을 그대로 쓴다.
- 서류에만 필요한 값(발급번호, 월별 내역, 세부 금액 등)은 `rng`로 만든다. 프로필의 `World.rng`는 쓰지 않는다.
- **반환 dict의 모든 값은 화면에 표시될 문자열**이다. 날짜와 금액은 함수 안에서 포맷한다.
  - 날짜: `D(date, "dot"|"dash"|"kor"|"kor_short"|"slash"|"en"|"en_long")`
  - 금액: `won(n)`는 `1,000원`, `won(n, "")`는 `1,000`, 한글 금액은 `K.won_korean(n)`
  - 서류마다 실제로 쓰는 표기를 따르고, 여러 표기가 쓰이면 `rng.choice`로 다양화한다.
- dict 키는 영어 snake_case를 쓴다. 이 키가 그대로 VLM 학습 정답(JSON)의 키가 된다.
  - 의미가 드러나게 짓는다(`applicant.name`, `loan.amount`).
  - 반복 항목은 리스트로 만든다(`items: [...]`).
- 생성한 값은 모두 템플릿에 표시한다. 표시하지 않은 값이 있으면 `check`가 경고한다.
- 개수가 변하는 리스트(거래내역, 가족 등)는 길이를 랜덤으로 하되 한 페이지 안에 들어가게 제한한다.

### 사실성
- 실제 서류의 **항목 구성, 순서, 표기 관행**을 최대한 따른다.
  - 예: 정부24·홈택스 발급본의 발급번호와 "이 증명서는 인터넷으로 발급되었으며..." 문구
  - 예: 등기부의 표제부·갑구·을구 구조
- 실제 기관 로고, 바코드, 위변조 방지 패턴, 공식 관인 이미지는 넣지 않는다. 도장은 `m.seal`의 텍스트 도장만 쓴다.
- 신분증, 인감증명서처럼 위조 위험이 큰 서류는 `sample_mark=True`로 등록한다. 그러면 "견본 SAMPLE" 워터마크가 항상 들어간다.
- 한 장일 필요는 없다. A4 서류(`.page.a4`, 794×1123px)는 내용이 넘치면 `docgen/paginate.js` 가 다음 쪽으로 나눈다
  (문단·표·섹션 단위, 표는 줄 단위, 표 머리글 반복, 쪽 번호, 최대 12쪽). 보통은 쪽을 직접 나누지 않는다. 원본이 한 쪽이면 한 쪽 안에 들어가게.
- 나눌 수 없는 것이 넘치면 `docgen check` 가 "페이지 넘침"(`overflow`)으로 잡는다: 한 쪽보다 큰 블록 하나, rowspan 으로 묶인 줄들,
  자동 나눔이 없는 고정 크기 서식(카드 540×340px 등). 블록을 나누거나 `dense` 로 글자를 줄인다.

### 검증

```bash
python -m docgen check --types <서류ID,...> --png --tmp /tmp/check   # 예외, 미표시 값, 페이지 넘침 검사
python -m docgen generate --types <서류ID> --n 3 --out /tmp/out --png  # 실제 이미지 확인
```
