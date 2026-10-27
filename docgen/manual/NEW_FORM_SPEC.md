# 새 html 서식 만들기: 결과물 형식

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
                                                fields.json               칸 목록 (A 의 form.json 에서 fields·lists)
                                                source.png                (선택) 원본 그림
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

- 첫 두 줄은 바꾸지 않습니다. 공통 틀(`docgen/templates/_base.html.j2`)이 글꼴·쪽 크기·쪽 나눔을 맡습니다.
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
  전체 목록은 `docgen/templates/_macros.html.j2`, 설명은 [TEMPLATE_GUIDE.md 2절](TEMPLATE_GUIDE.md#2-템플릿).

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

`rule:` 값은 칸마다 따로 뽑습니다 (예: 조회 시작일이 종료일보다 늦을 수 있음). 값끼리 맞아야 하는 칸은 `profile.` 을 쓰거나, 등록 뒤 studio 에서 값 출처를 고칩니다.
값 출처를 다 정하지 못했으면 `rule:note`(아무 글자) 로 두고 studio ① 서식에서 고쳐도 됩니다. **키와 위치만 맞으면 값 출처는 나중에 고칠 수 있습니다.**

---

## 4. 키 이름

키는 학습 데이터의 정답 키가 됩니다. 사람마다 다르게 지으면 학습 데이터가 흩어지므로 가장 신경 쓸 곳입니다.

- 영어 소문자·숫자·밑줄, 점으로 나눈 경로: `applicant.name`, `account.number`, `rows.0.date`.
- **이미 있는 키를 먼저 씁니다.** 키 사전: `docgen/dictionary/common.json`(공통 키), `docgen/keys.json`(서식들이 쓰는 키),
  `docgen/dictionary/parties.json`(누구: 신청인·대리인·임대인 …). "누구의 무엇"으로 짓습니다: `agent.name`, `lessor.address`.
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
python -m docgen.preview --dir <초안 폴더> --rows min --out work/min
python -m docgen.preview --dir <초안 폴더> --rows max --out work/max
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
```

- **서식 ID**: 영어 소문자로 시작, 소문자·숫자·밑줄 3~51자 (`[a-z][a-z0-9_]{2,50}`). 이미 있는 ID 는 쓰지 않습니다 (`python -m docgen.formdir path <ID>` 로 확인). 기존 폴더를 덮어쓰지 않습니다.
- **어디에**: 공개·빈 서식에서 만든 것은 `docgen/forms/<ID>/`, **실서류에서 만든 것은 `$DOCGEN_PRIVATE_FORMS/<ID>/`** (studio `private_forms_dir`).
- studio ① 서식 목록 위의 **서식 다시 읽기** 를 누르면 목록에 나옵니다 (다시 띄우지 않아도 됨). 폴더가 깨져 있으면 등록하지 않고 이유를 보여 줍니다 (JSON·템플릿 문법·ID 형식·코드 서식과 ID 겹침).
- 이미 등록된 서식의 템플릿·칸 목록을 고친 것은 누르지 않아도 다음 미리보기부터 반영됩니다. 버튼은 새 폴더, 지운 폴더, `form.json` 의 이름·그룹을 바꿨을 때 누릅니다.

**3) 등록 뒤 확인**

```bash
python -m docgen.formdir path <ID>                         # 파일 자리
python -m docgen.regions check <ID>                        # 칸 목록 형식
python -m docgen.preview <ID> --rows max --out work/<ID>   # 등록된 서식으로 그리기
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

## 8. 전체 예시 (검사 통과)

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
