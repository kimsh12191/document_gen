---
name: form-from-image
description: 서식 이미지(빈 서식·견본·실서류 사진)를 직접 보고 docgen 서식 하나를 추가한다 — 뽑을 키와 항목 설명(fields.md)을 정하고, template.html.j2 · fields.json · form.json (칸끼리 관계가 있으면 generate.py)을 써서 원본과 비교하며 고친다. "이 이미지로 서식 만들어줘", "forms 에 서식 추가", "이 서류에서 뽑을 키 정해줘" 같은 요청에 쓴다. 이미 있는 서식 고치기는 docgen/forms/README.md.
---

# 서식 이미지 → docgen 서식 추가

## 목표

서식 이미지(쪽마다 한 장)를 **직접 보고**, `docgen/forms/` 에 넣을 서식 폴더를 만든다. 이 서식은 서류 한 건마다 다른 가짜 고객 값을 채워
그림과 정답(키·값·위치)을 계속 찍어 내는 **합성 데이터 생성기**다. 원본을 똑같이 베끼는 것이 아니라, 같은 서류로 보이는 틀을 만드는 것이다.

| 결과물 | 필수 | 정의하는 것 |
|---|---|---|
| `template.html.j2` | ✓ | 모양(제목·항목명·표 선·안내문)과 **값이 들어갈 자리** `{{ f("키", label="항목명") }}`. 이 자리가 정답 위치(bbox)가 된다 |
| `fields.json` (초안에서는 `form.json` 의 `fields`·`lists`) | ✓ | **키마다**: 항목명 `label`, 종류 `type`, 값 만드는 법 `source`, 보기 `choices`, 질문 설명 `q` |
| `form.json` | ✓ | 서식 정보: 이름·그룹·종류·쪽 크기 |
| `generate.py` | 관계가 있을 때만 | 칸끼리 관계(합계=행 합, 발급일≥조회일 …) `adjust(d, p, rng)` |
| `fields.md` (작업 파일) | ✓ | 사람이 검토하는 **칸 표**: 뽑을 키와 항목 설명. 서식 폴더에는 넣지 않는다 |

**다 됐다:** 검사(`checks: []`, `overflow: false`, 쪽 수) 통과 · 여러 seed 로 그려도 값이 칸 안 · 원본과 나란히 봐서 같은 서류 · 칸 표에 판단이 안 선 것까지 적힘.
검수 완료는 사람이 studio 에서 누른다. 검사 통과를 "검수 완료"라고 하지 않는다.

**지킬 것**
- 실서류 그림은 사내 모델(지금 이 작업)에서만 다룬다. 외부 서비스로 보내지 않는다. 원본에 적힌 실제 값(이름·번호·주소)은 어느 파일에도 옮기지 않는다.
- 고치는 곳은 초안 폴더뿐. 기존 서식 폴더·`docgen/forms/_common/`·엔진 코드(`docgen/*.py`)는 고치지 않는다. 등록은 사용자가 하라고 할 때만 (7단계).
- 같은 단계에서 같은 오류가 두 번 나면 멈추고 오류 끝부분과 함께 보고한다.
- 패키지·브라우저를 설치하지 않는다 (`pip install`, `playwright install` …). 미리보기가 브라우저를 못 찾는 등 **환경 오류는 고치려 하지 말고** 멈추고 보고한다.

명령은 저장소 맨 위 폴더(`document_gen/`)에서 실행한다. 파일 꼴의 원문은 `docgen/manual/NEW_FORM_SPEC.md` 이고, 이 문서와 다르면 그쪽을 따른다.

**에이전트 진행기(`python -m formagent`, ReLab)로 돌 때:** 요청에 서식 ID·초안 폴더·원본 종류가 적혀 오고, 원본은 이미 초안 폴더에 있다 (0단계 3~5는 하지 않는다).
일은 회차로 나뉜다 — 1회차는 0~4단계, 2회차부터 5단계. 회차 안에서는 그림 파일을 열어 볼 수 없고, **원본과 렌더를 나란히 놓은 그림은 다음 회차 요청에 붙어 온다.**
회차마다 새 대화라 앞 회차의 대화는 없다: 초안 폴더의 `fields.md`·`review.md` 를 먼저 읽는다. 초안 폴더의 `__init__.py`·`run.json`·`relab_*.log`·`check_*` 는 진행기 것이니 건드리지 않는다.
셸 문법(`for`, `|`, heredoc)은 쓸 수 없다 — 아래의 검사 명령 하나로 확인한다.

## 0. 준비

1. 읽는다: `docgen/manual/NEW_FORM_SPEC.md` 2·3·4·9·11절, `guide/studio/keys.md` 3~6절.
2. **완성 예시**를 연다: `.claude/skills/form-from-image/example/` (은행 신청서 한 장을 이 순서대로 만든 것 — `fields.md`·`template.html.j2`·`form.json`·`generate.py`).
   발급 서류(표·반복 행·발급기관 직인) 견본은 `docgen/forms/bank_statement/look/template.html.j2`.
3. **서식 ID**: 원본 제목의 영어 이름, 소문자·숫자·밑줄 3~51자. `python -m docgen.formdir path <ID>` 가 "없습니다 (새 서식이면 쓸 수 있는 ID)" 여야 한다.
4. 초안 폴더 `out/form_drafts/<ID>/` 를 만들고 원본을 복사한다: 1쪽 `source.png`, 2쪽부터 `source_2.png` ….
5. 원본이 실서류(값이 적힌 진짜 서류)인지 사용자에게 듣고 적어 둔다. 모르면 묻는다.

## 1. 그림 읽기 → 칸 표 `fields.md`

**`fields.md` 를 끝까지 쓰기 전에는 html·form.json 을 쓰지 않는다.** 이 표가 "이 서류에서 뽑을 키와 항목 설명"이고 사람이 가장 먼저 검토하며, 2·3단계는 이 표를 옮기는 일이다.
html 을 쓰다가 칸이 바뀌면 `fields.md` 를 먼저 고치고 html 을 맞춘다.

**읽는 순서:** 쪽 전체를 보고 덩어리로 나눈다(제목 · 발급번호/결재란 · 위 정보 표 · 목록 표 · 체크 항목 · 안내문/약관 · 날짜·서명란·발급기관).
위에서 아래로 덩어리마다, 안에서 왼쪽→오른쪽·위→아래로 칸을 본다. 그림이 작아 안 보이면 그 부분을 잘라 크게 보고 읽는다.

**값 자리 / 고정 글자 구분:** 서류마다 달라질 것(사람·회사·번호·날짜·금액·주소·체크 결과·지점명·도장)은 **값 자리**,
모든 서류에 똑같이 인쇄된 것(제목·항목명·안내문·약관·"년 월 일" 같은 틀 글자)은 **고정 글자**.
빈 서식이면 빈 칸·밑줄·괄호·"년 월 일" 앞 공백이 값 자리다. 실서류면 손글씨·다른 글꼴·다른 색 글자가 값이다.

```markdown
# <서식 이름> (<ID>) — <쪽 수>쪽, group=<…>, category=<external|internal>, 원본=<빈 서식|견본|실서류>

## 칸
| 쪽 | 원본 항목명 | 키 | type | source | 이 칸이 무엇인지 | 값 예시·형식 | 확신 |
|---|---|---|---|---|---|---|---|
| 1 | 성명 | customer.name | text | profile.person.name | 신청인 본인 이름 | 홍길동 | 높음 |
| 1 | 신청금액 | loan.amount | amount | rule:amount | 대출 신청 금액 (원) | 30,000,000 | 높음 |
| 1 | 용도 □대출 □기타 | purpose | checkbox | rule:choice [대출, 기타] | 제출 용도, 하나만 체크 | 대출 | 높음 |

## 반복 표 <표 키> — 원본 행 n개 → min n, max m   (빈 행 N개가 인쇄된 서식이면: 칸은 늘 N행, 값은 min 1 · max N)
| 열 | 원본 머리글 | 열 키 | type | source | 이 열이 무엇인지 |

## 도장·서명
| 원본 표시 | 키 | 매크로 |
| 성명 옆 (인) | seal.customer · sign.customer | m.sigspot("customer", val("customer.name"), label="신청인") |
| 발급기관 직인 | seal.issuer | m.seal("…직인", square=True, over=True) |

## 칸끼리 관계 (→ generate.py)
- 조회 시작일 ≤ 종료일 ≤ 발급일 …

## 고정 글자 (값 아님)
- 약관 1~5조, "위와 같이 신청합니다" …

## 판단이 안 선 것
- <칸> — <왜 애매한지>
```

**키** (keys.md): 영어 소문자 `누구의.무엇` — `customer.name`, `agent.phone`, `employer.name`, `loan.amount`, `period.start`, `issue_date`, `account`.
같은 뜻은 서식 안에서 같은 이름. 한글·대문자·번호 붙은 키(`name2`) 금지. 한 키가 다른 키의 앞부분이면 안 됨(`account` 와 `account.number` 동시 금지).
같은 사람 이름이 두 자리에 있으면 뒤 자리는 역할로(`applicant.name`) 짓고 source 를 같게 한다.

**type**: `text` `amount` `number` `date` `checkbox`. 도장·서명은 칸 목록에 넣지 않고 매크로가 기록한다.

**source** (값 만드는 법). 전체 목록과 예시 값은 `docgen/forms/_common/values.md` 에서 찾는다 (추측하지 않는다).
- 고객 본인·본인 회사 값 → `profile.…` (`profile.person.name`·`.birth`·`.rrn`·`.mobile`·`.email`·`.name_en`·`.address.road_short`, `profile.business.biz_no`, `profile.issue_date` …).
- 그 밖 → `rule:<종류>` (`date` `amount` `account` `currency` `bank` `branch` `company` `number` `count` `percent` `rate` `note` …).
- 보기 `rule:choice` + `choices`(원본 글자 그대로), 늘 같은 글자 `rule:fixed` + `text`, 틀 `rule:pattern` + `pattern`(`#` 숫자), 반복 행 날짜 `rule:date_seq`, 짧은 자유 글 `rule:free_text`, 늘 빈 칸 `rule:empty`.
- 모르겠으면 `rule:note` 로 두고 "판단이 안 선 것"에 적는다. 키·위치가 맞으면 source 는 나중에 고칠 수 있다.

**값이 이상하게 나오는 함정** (실제로 겪은 것):
- `rule:phone`·`rule:address`·`rule:email` 은 **고객 본인 값**을 낸다. `rule:person` 도 자주 고객 이름이다.
  대리인·보증인·수령인 같은 **다른 사람** 칸은 이름 `rule:other_person`, 전화 `rule:pattern` `"010-####-####"`, 생년월일은 3단계 `generate.py` 로.
- `rule:date` 는 요즘 날짜를 낸다 → 생년월일에 쓰면 2025년생이 나온다. 고객이면 `profile.person.birth`, 다른 사람이면 `generate.py`.
- "____년 __월 __일"처럼 한 날짜가 칸 여러 개로 나뉘면 키를 나눈다(`apply_y`·`apply_m`·`apply_d`; `apply_date` 와 같이 쓰지 않음).
  `profile.issue_date` 처럼 **하나로 정해진 값**이면 같은 source 에 `"part": 0|1|2, "format": "number"` 로 충분하다.
  `rule:date` 는 칸마다 따로 뽑혀 년·월·일이 서로 다른 날짜가 되므로 `generate.py` 로 한 날짜에서 나눠 넣는다.
- `rule:branch` 는 "○○지점" 을 낸다. 원본에 "지점(부) 앞" 이 인쇄돼 있으면 "지점"이 겹친다 → `generate.py` 에서 떼기.
- 보기가 하나뿐인 체크(□계좌마스킹)는 `rule:choice` 면 늘 체크된다 → `generate.py` 에서 가끔 `None`.
- `rule:amount` 는 가끔 "원"을 붙인다 (`480,000` 과 `62,630,000원` 이 섞임). 머리글·칸에 "(원)"·"원" 이 인쇄돼 있으면 숫자 꼴로 맞춘다:
  `generate.py` 에서 `put(d, 키, amount_like(to_amount(값), "1,000"))` (반복 표는 `for r in rows(d, "<표 키>")` 로 행마다). 합계도 같은 꼴로.
- 표기(`"fmt"`)는 html 서식에 적용되지 않는다. 날짜·금액 표기를 바꾸려면 `generate.py` 의 `date_like`·`amount_like`.

**체크 칸 나누기**
- 보기 중 **하나만** 고르는 묶음(□등록 □변경 □해제) → 키 하나, `type: checkbox`, `rule:choice` + `choices`, 템플릿 `m.choice`.
- **여러 개를 같이** 고를 수 있는 묶음(□입금내역 □출금내역 □대출이자 …) → 보기마다 키 하나(`detail.deposit`, `detail.withdraw` …),
  각각 `choices: ["<보기 글자>"]` 하나짜리 + `generate.py` 에서 가끔 `None` (보기 하나짜리는 늘 체크되므로). 템플릿은 보기마다 `m.choice("<키>", ["<보기 글자>"])`.
- 원본이 어느 쪽인지 모르겠으면 "판단이 안 선 것"에 적고 하나만 고르는 쪽으로.

**나뉜 날짜 칸의 꼴 (`part`·`format`)**: 한 값을 숫자 묶음으로 나눠 칸마다 넣는다. `"part": 0` 첫 숫자 묶음(년), `1` 둘째(월), `2` 셋째(일),
`"format": "number"` 숫자만 남김. 예: `"apply_y": {"label": "신청일 년", "type": "number", "source": "profile.issue_date", "part": 0, "format": "number"}`.

**질문 설명 `q`**: kie 질문의 항목 줄은 `- 키: 항목명 (괄호 설명)` 이다. 항목명만으로 헷갈리는 칸에만 넣는다:
같은 항목명이 두 군데(신청인 성명·대리인 성명 → `"q": {"label": "대리인 성명"}`), 항목명이 없거나 "금액"처럼 막연함(`"q": {"note": "이체 금액"}`).
반복 표 열에는 `q.note` 를 넣지 않는다 (자동 "몇 번째 행" 설명이 사라짐).

**확신 낮음은 숨기지 않는다.** 글자가 흐려 못 읽음, 값인지 고정 글자인지 모름, 키가 애매함 → 표에 표시하고 "판단이 안 선 것"에 적는다.

## 2. 템플릿 `template.html.j2` 쓰기

그림을 보고 html 로 옮긴다. **같은 서류로 보이게**가 목표이고 px 까지 맞출 필요는 없다 (글꼴·크기·선 굵기는 생성할 때 무작위로 바뀐다).

**틀**: 첫 두 줄 `{% extends "_base.html.j2" %}` · `{% import "_macros.html.j2" as m with context %}` 는 그대로. 쪽은 A4 794×1123px, 넘치면 자동으로 다음 쪽.

**그림 → 크기 옮기기**: 원본 가로 = 794px 로 놓고 비율로 잰다. 표 너비·열 너비는 원본 가로에 대한 %, 행 높이는 `원본 행 높이 / 원본 세로 × 1123` px.
덩어리 사이 간격도 같은 비율로 margin px.

**덩어리별로 쓰는 법**
- 제목: `{{ m.title("…") }}` (글자 사이 띄움도 원본대로).
- 선이 있는 영역은 모두 `<table>`: `table-layout: fixed`, `<colgroup>` 열 너비 %, `tr { height: Npx }` (padding 으로 높이 맞추지 않음), 합친 칸은 `colspan`/`rowspan`. 항목명 칸은 `<th>`(배경 `var(--label-bg)`), 값 칸은 `<td>` 안에 `f()`.
- 값 자리: `{{ f("키", label="원본 항목명") }}`. 한 칸 안에 고정 글자와 값이 섞이면 그대로: `{{ f("issue_y", label="발급일 년") }}년 {{ f("issue_m", …) }}월`.
- 체크 보기: `{{ m.choice("purpose", ["대출", "기타"], label="용도") }}` (보기 글자 = 칸 목록 `choices`). 예/아니오 동의: `m.agree`.
- 반복 표(행 수가 서류마다 다른 목록): `{% for r in d.<표 키> %}` 행마다 `f("<표 키>." ~ loop.index0 ~ ".<열 키>", label="머리글")` (NEW_FORM_SPEC 2절). 원본의 빈 줄까지 반복 표로 만든다.
- **빈 칸·빈 행이 정해진 개수만큼 인쇄된 곳**(계좌번호 칸 6개, 순번 1~10 행 등)은 칸·행은 늘 N개 그리고 값만 일부 채운다:
  `lists` 에 `"min": 1, "max": N` (빈 서식은 몇 행이 채워질지 모르므로 min 은 1),
  `{% set acc = d.accounts or [] %}{% for i in range(6) %}<td>{% if i < acc|length %}{{ f("accounts." ~ i ~ ".number", label="계좌번호") }}{% endif %}</td>{% endfor %}`.
  값이 없는 행에도 인쇄된 글자(순번, "□현금 □대체" 같은 보기)는 그대로 그린다.
- 체크 보기가 좁은 칸에 있으면, **체크된 보기는 값 글자로 크게 찍혀** 안 찍힌 보기보다 길어진다. 칸을 넘지 않게 그 칸의 글자를 줄이거나(`font-size`) 보기마다 줄을 나눈다.
  원본에서 작게 인쇄된 괄호 글자("(수수료차감 후 입금)")가 있는 보기도 보기 글자 전체가 `choices` 값이므로 같은 크기로 찍힌다는 것을 감안한다.
- 보기 사이에 설명이 낀 줄("□ 대체(계좌출금) : 지급건별로 처리됩니다. □ 대체 □ 현금")은 `m.choice` 로 보기를 한데 묶고 설명은 묶음 뒤에 둔다. 순서가 달라진 것은 "판단이 안 선 것"에 적는다.
- 체크와 날짜 칸이 섞인 줄("□ ____년 __월 __일 ~ ____년 __월 __일 / □ 최근 3개월 □ 최근 6개월")은 고르는 쪽을 키 하나(`period.kind`, 보기: `기간 지정`·`최근 3개월`…)로 두고,
  날짜 칸은 `f()` 로 그린 뒤 `generate.py` 에서 `period.kind` 가 `기간 지정` 이 아닐 때 날짜를 `None` 으로. "기간 지정"의 □ 는 `{% if val("period.kind") == "기간 지정" %}■{% else %}□{% endif %}` 처럼 그린다.
- `rowspan`·`colspan` 은 세기 쉽게 틀린다. 왼쪽 세로 머리(예: "신청 사항")의 `rowspan` = 그 덩어리의 `<tr>` 수. 틀리면 아래 덩어리가 통째로 밀린다 (5단계에서 보임).
- 긴 항목명이 좁은 칸에서 두 줄로 넘치면 그 `<th>` 에 `white-space: nowrap` 과 작은 글자.
- 서명·날인 자리 "(서명 또는 인)": `{{ m.sigspot("customer", val("customer.name"), label="신청인") }}` → 정답 키 `seal.customer`·`sign.customer`.
- 발급기관 직인: `{{ m.seal("…", square=True, over=True) }}`, 은행 결재란은 칸만 그린 표 (값 자리 없음).
- 안내문·약관: 원본 글자 그대로 옮긴다 (`<p class="note">`, `<ol class="clauses">`, 작은 글자는 `small`·`tiny`). 길어도 줄이지 않는다.
- 색·글꼴은 CSS 변수(`var(--border)`, `var(--label-bg)`, `var(--accent)`). 외부 URL·`<script>`·로고·바코드·QR·관인 그림은 넣지 않는다 (로고 자리는 비우거나 기관명 글자).
- 값을 `{{ d.x }}` 로 직접 찍지 않는다 (그림엔 나오지만 정답에서 빠짐). 조건에만 `{% if val("x") == … %}`.

## 3. `form.json` (초안 꼴) · `generate.py`

```json
{"name": "<원본 제목>", "group": "<identity|family|income|tax|finance|real_estate|business|corporate|fx|bank_form>",
 "category": "<external(고객이 가져오는 서류)|internal(은행 서식)>", "page": "a4", "origin": "analyzer", "parent": null,
 "source_image": "source.png",
 "fields": {"customer.name": {"label": "성명", "type": "text", "source": "profile.person.name"}, "…": {}},
 "lists":  {"rows": {"min": 5, "max": 20, "fields": {"date": {"label": "거래일", "type": "date", "source": "rule:date_seq"}}}}}
```

- `fields`·`lists` 는 `fields.md` 와 같아야 한다 (템플릿의 모든 `f()` 키, `m.choice` 키). 도장·서명 키는 넣지 않는다.
- 칸끼리 관계나 1단계 "함정"이 있으면 `generate.py` 의 `adjust(d, p, rng)` 로 맞춘다 (NEW_FORM_SPEC 8절: `docgen.formkit` 도우미와 표준 라이브러리 `datetime`·`re`·`math` 만,
  칸 목록에 있는 키만 고침, 난수는 `rng` 만). 관계가 없으면 만들지 않는다.
- 반복 표를 조건에 따라 비울 때는 목록을 지우지 말고 행의 값만 `None` 으로 (`for r in rows(d, "accounts"): r["number"] = None`). 목록을 지우면 `checks` 경고.

```python
from datetime import date, timedelta
from docgen.formkit import to_date, date_like, get, put, rows


def adjust(d, p, rng):
    start = (to_date(get(d, "base_date")) or date(2025, 1, 1)) + timedelta(days=rng.randint(0, 30))
    end = start + timedelta(days=rng.choice([182, 365, 1095]) - 1)          # 시작 ≤ 끝 ≤ 3년
    for name, day in (("start", start), ("end", end)):                       # 년·월·일 칸을 한 날짜에서
        put(d, f"period.{name}_y", str(day.year)); put(d, f"period.{name}_m", f"{day.month:02d}"); put(d, f"period.{name}_d", f"{day.day:02d}")
    if get(d, "agent.birth"):                                                # 다른 사람 생년월일: 20~70세
        put(d, "agent.birth", date_like(date(rng.randint(1955, 2004), rng.randint(1, 12), rng.randint(1, 28)), get(d, "agent.birth")))
    if get(d, "target_scope") == "전체계좌":                                  # 조건에 따라 표 값 비우기
        for r in rows(d, "accounts"):
            r["number"] = None
    return d
```

## 4. 그려 보기·검사 (명령 하나)

```bash
python -m pytest .claude/skills/form-from-image/test_draft.py --draft out/form_drafts/<ID> -q     # 에이전트·사람 모두 (통과해야 끝)
python .claude/skills/form-from-image/check.py out/form_drafts/<ID>                              # 같은 검사, 결과를 글로 보기
```

미리보기 5번(`--rows min` · `--rows max` · seed 1~3)을 그리고 `<초안>/check/` 에 결과를 쓴다:
`check.json`(문제·경고·렌더별 pages/fields/empty·seed 별 키→값), `side_<쪽>.jpg`(왼쪽 원본 · 오른쪽 min 렌더), `renders.jpg`(min·max·seed1·seed2 모음).

| 검사가 보는 것 | 통과 못 함 (problems) | 경고 (warnings — 읽고 판단해 고친다) |
|---|---|---|
| 파일 | `fields.md`·`template.html.j2`·`form.json` 이 없음 | |
| 미리보기 | 명령 오류 (템플릿 문법·키 오류), `checks` 가 비지 않음, `overflow` | |
| 쪽 수 | `--rows min` 렌더 쪽 수 ≠ 원본 그림 수 | |
| 템플릿 | 값을 `{{ d.… }}` 로 직접 찍음 (정답에서 빠짐) | |
| 정답 값 | | 다른 칸에 같은 사람 값(대리인 전화 = 고객 전화 …), 한 서류 안 날짜·금액 표기 섞임, 빈 값이 절반 넘음 |

경고의 "다른 칸에 같은 값"은 정말 같은 사람(위임인 = 예금주)이면 그대로 둔다. 그림은 사람(또는 다음 회차의 나)이 보고, 넘치는 값·겹치는 글자·이상한 줄바꿈을 찾는다
(**체크된 보기 글자**, 긴 금액·주소, 도장·서명이 옆 칸·글자를 덮지 않는지). `fields` 수가 칸 표의 값 자리 수와 맞는지도 본다.

## 5. 원본과 비교하며 고치기 (최대 3회)

4단계 검사가 만든 `check/side_<쪽>.jpg`(왼쪽 원본 · 오른쪽 렌더)와 `check/renders.jpg` 를 본다 (에이전트 진행기면 요청에 붙어 온다).
값 박스 자리까지 보려면 `python .claude/skills/form-from-image/compare.py --source <초안>/source.png --render <초안>/check/render_min --out <초안>/compare`
의 `overlay_<쪽>.png`(회색 원본 위에 빨강 렌더, 파랑 값 박스와 키).
아래를 쪽마다 예/아니오로 `review.md` 에 회차별로 적고, "아니오"마다 어디가 어떻게 다른지 한 줄. 꼴:

```markdown
## 2회차
| # | 1쪽 | 다른 곳 |
|---|---|---|
| 1 | 예 | |
| 3 | 아니오 | 계좌번호 칸이 원본은 3칸(□전체 · 계좌1 · 계좌2), 렌더는 1칸 |
…
고친 것: 계좌번호 칸을 3칸으로 · 고칠 것 없음이면 그렇게
```

1. 원본의 제목·항목명·안내문이 렌더에 모두 있다 (빠진 것 없음)
2. 원본에 없는 항목명·문구를 지어내지 않았다
3. 표마다 열 수·칸 나눔(합친 칸, 항목명/값 칸 배치)이 같다. 행 수는 고정 표면 같고, 반복 표면 min 이 원본과 같다
4. 덩어리의 순서와 대략의 자리·크기가 같다 (위·가운데·아래, 왼쪽·오른쪽)
5. 원본의 값 자리마다 렌더에 값(파랑 박스)이 있고, 값이 아닌 곳에 값이 없다
6. 체크 보기·도장·서명 자리가 원본과 같다
7. 원본에 적혀 있던 실제 값(실서류)이 렌더에 고정 글자로 남지 않았다
8. 쪽 수가 같다

"아니오"를 고치고 4단계부터 다시. 3회 뒤에도 남은 것은 보고에 적는다. 글꼴·글자 크기·선 굵기의 작은 차이는 고치지 않는다.

## 6. 보고

| 항목 | 내용 |
|---|---|
| 서식 | ID · 이름 · 쪽 수 · 원본 종류(빈 서식/견본/실서류) · group · category |
| 순서 | `fields.md` 를 html 보다 먼저 다 썼는지 (아니면 왜) |
| 칸 | 값 자리 수, 반복 표(행 min~max), 도장·서명, `generate.py` 유무와 맞춘 관계 |
| 검사 | `--rows min`·`max` 마지막 줄 JSON |
| 비교 | 마지막 회차 8문항, `compare_<회차>/side_*.png` 경로 |
| 판단이 안 선 것 | `fields.md` 의 확신 낮음·애매한 칸, 남은 "아니오" |
| 사람이 볼 것 | `fields.md` 의 키·설명 (데이터셋을 만든 뒤에는 키를 못 바꿈), 비교 그림 |

에이전트 진행기로 돌면 이 보고를 초안 폴더의 `report.md` 로 쓴다.

## 7. 등록 (사용자가 하라고 할 때만 — 에이전트 회차에서는 하지 않는다)

- 어디에: 빈 서식·공개 견본 → `docgen/forms/<ID>/`, **실서류에서 만든 것 → `$DOCGEN_PRIVATE_FORMS/<ID>/`**. 폴더가 이미 있으면 멈추고 보고 (덮어쓰지 않음).
- 옮기기 (NEW_FORM_SPEC 6절) — 명령 하나. 검사 통과·ID·폴더가 비었는지 확인하고, 하나라도 안 되면 아무것도 옮기지 않는다:

```bash
python .claude/skills/form-from-image/register.py out/form_drafts/<ID> --to public          # docgen/forms/<ID>/
python .claude/skills/form-from-image/register.py out/form_drafts/<ID> --to private --real  # $DOCGEN_PRIVATE_FORMS/<ID>/ (실서류)
```
  `template.html.j2` → `look/template.html.j2`, `form.json` 의 `fields`·`lists` → `fields.json`, 나머지 → `form.json`, `source*.png`, `generate.py` 를 옮기고
  카드(`formdir card`)와 `formdir check` 를 돌린다. 작업 파일(`fields.md`·`review.md`·`report.md`·`check*`·`run.json`·`relab_*.log` …)은 옮기지 않는다.
  studio 는 **이미지로 서식 만들기 › 결과 › [등록]**, 명령줄은 `python -m formagent register --id <ID> --to public|private` 가 같은 것을 부른다.
- 더 확인: `python -m docgen.formdir card <ID>` 의 질문→답 예시가 말이 되는지 · `python -m docgen.preview <ID> --rows max --out out/<ID>`.
- 사용자에게: studio 서식 › **서식 다시 읽기** → 목록에 나옴 → **생성 사례 › 미리보기/검수** 에서 원본과 비교해 검수 완료.
  시험 생성: `python -m docgen.bench build --types <ID> --per-doc 2 --out out/try_<ID>`.
