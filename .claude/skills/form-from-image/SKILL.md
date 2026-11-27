---
name: form-from-image
description: 서식 이미지(빈 서식·견본·실서류 사진·팩스)를 보고 docgen 서식 하나를 추가한다 — 도구로 표 선·칸·글자 자리를 재고(grid.py), 보기 창으로 잘라 크게 보며 칸마다 글자와 값 자리를 layout.json 에 적고, build.py 가 원본과 거의 같은 template.html.j2 · form.json · fields.md(뽑을 키와 항목 설명)를 만든다. 원본과 렌더를 같은 자리끼리 맞대 보며 고친다. "이 이미지로 서식 만들어줘", "forms 에 서식 추가", "이 서류에서 뽑을 키 정해줘" 같은 요청에 쓴다. 이미 있는 서식 고치기는 docgen/forms/README.md.
---

# 서식 이미지 → docgen 서식 추가

## 목표

서식 이미지(쪽마다 한 장)로 **원본과 거의 같은 모양의, 고칠 수 있는 html 서식**을 만든다. 서류 한 건마다 가짜 고객 값을 채워
그림과 정답(키·값·위치)을 찍어 내는 **합성 데이터 생성기**가 된다 (studio 서식 목록에 등록되는 꼴 그대로).

| 결과물 | 누가 | 정의하는 것 |
|---|---|---|
| `layout.json` | **내가 쓴다** | 칸마다 원본 글자, 값 자리 `{키}`, 키마다 항목명·종류·값 만드는 법·설명. 이 서식의 원본 |
| `template.html.j2` | build.py | 모양: 표 자리·열 너비·행 높이·합친 칸(grid 가 잰 숫자 그대로) + 글자 + 값 자리 `f("키")` |
| `form.json` | build.py | 서식 정보 + 칸 목록 `fields`·`lists` |
| `fields.md` | build.py | 사람이 검토하는 **뽑을 키와 항목 설명** 표 |
| `generate.py` | 내가 (필요할 때만) | 칸끼리 관계 (시작일 ≤ 끝일, 합계 = 행 합 …) |

**순서가 핵심이다: 재기는 도구가, 읽기는 내가, 쓰기는 도구가.** 표의 선 자리·칸 나눔·글자 크기를 그림을 보고 짐작하지 않는다 — `grid.py` 가 잰다.
나는 잘라 크게 본 그림에서 **칸 안의 글자를 읽고, 그것이 고정 글자인지 값 자리인지 정하는 일**만 한다. html 은 손으로 쓰지 않는다 — `build.py` 가 쓴다.

**다 됐다:** 검사 통과(문제 없음) · 경고를 다 고쳤거나 왜 두는지 적음 · 원본과 렌더를 덩어리마다 맞대 봐서 같은 서류 · `fields.md` 의 키·설명이 칸의 뜻에 맞음.
검수 완료는 사람이 studio 에서 누른다. 검사 통과를 "검수 완료"라고 하지 않는다.

**지킬 것**
- 실서류 그림은 사내 모델에서만 다룬다. 외부 서비스로 보내지 않는다. 원본에 적힌 **실제 값(이름·번호·주소·지점명·날짜)은 어느 파일에도 옮기지 않는다** — 값 칸은 `{키}` 로만.
- 고치는 곳은 초안 폴더뿐. 기존 서식 폴더·`docgen/forms/_common/`·엔진 코드는 고치지 않는다. 등록은 사용자가 하라고 할 때만 (8단계).
- 같은 단계에서 같은 오류가 두 번 나면 멈추고 오류 끝부분과 함께 보고한다.
- 패키지·브라우저를 설치하지 않는다. 미리보기가 브라우저를 못 찾는 등 **환경 오류는 고치려 하지 말고** 멈추고 보고한다.

명령은 저장소 맨 위 폴더(`document_gen/`)에서 실행한다. 아래 `<초안>` = `out/form_drafts/<ID>`, `T=.claude/skills/form-from-image`.

## 도구

| 명령 | 하는 일 |
|---|---|
| `python $T/grid.py <초안>` | 원본 기울기 바로잡기 → **표·칸·글자 덩어리의 자리를 잰다** (글자는 읽지 않음). 칸 이름 `T2.7`, 글자 덩어리 `B3`. 결과 `page_<n>.png`·`grid_<n>.json`, 화면에 칸 목록 |
| `python $T/view.py page <초안> --to 1` | 쪽 전체 + 칸 이름 → `view_1.png` |
| `python $T/view.py table <초안> T2 --rows 1-6 --to 2` | 표(행 범위)를 크게 + 칸 이름 → `view_2.png`. **글자는 이것으로 읽는다** |
| `python $T/view.py crop <초안> x0 y0 x1 y1 --cells --to 3` | 아무 곳이나 크게 (눈금은 쪽 px) |
| `python $T/view.py compare <초안> x0 y0 x1 y1 --to 4` | 같은 자리의 원본(위)·렌더(아래) — **고칠 때는 이것으로 본다** |
| `python $T/view.py overlay <초안> x0 y0 x1 y1 --to 4` | 회색 원본 위에 빨강 렌더 (어긋남을 볼 때) |
| `python $T/build.py <초안>` | `layout.json` + `grid_<n>.json` → `template.html.j2`·`form.json`·`fields.md` |
| `python -m pytest $T/test_draft.py --draft <초안> -q` | 검사 (미리보기 5번 · 모양 대조 · 값 경고). 경고는 출력 아래 `warnings summary` 의 `DraftWarning: 경고: …` |

**자리 단위는 쪽 px**: 쪽 가로 = 794 (A4 세로 1123). grid 목록·보기 창 눈금·`layout.json` 의 `box` 가 모두 이 단위다.
**보기 창**: `--to 1~4` 로 `view_1.png`~`view_4.png` 에 쓴다. 쓴 다음 그 파일을 열어 본다
(에이전트 진행기(ReLab)에서는 네 장이 요청에 붙어 있어서, **명령으로 다시 쓰면 다음 단계에서 새 그림이 보인다** — 파일을 따로 열 수는 없다).
한 번에 크게 볼 수 있는 넓이는 정해져 있다: 표 하나는 `--rows` 로 6~10행씩 나눠 본다. 작은 글자·손글씨·도장 겹친 곳은 `crop` 으로 더 좁게.

## 0. 준비

1. 서식 ID: 원본 제목의 영어 이름, 소문자·숫자·밑줄 3~51자. `python -m docgen.formdir path <ID>` 가 "없습니다" 여야 한다.
2. 초안 폴더 `out/form_drafts/<ID>/` 를 만들고 원본을 복사한다: 1쪽 `source.png`, 2쪽부터 `source_2.png` ….
3. 원본이 빈 서식인지 실서류(값이 적힌 진짜 서류)인지 사용자에게 듣고 적어 둔다.
(에이전트 진행기로 돌 때는 1~3 과 아래 1단계 grid.py 를 진행기가 해 두었다.)

## 1. 재기 — `grid.py`

```bash
python $T/grid.py <초안>
```

화면에 쪽마다 **표**(열 경계 x · 행 경계 y · 칸 목록), **표 밖 선**, **바코드 자리**, **표 밖 글자 덩어리**가 나온다. 칸 한 줄의 뜻:

```
- T2.6 행2~5 열2 · x 108~190 y 186~330 · 글자 2줄 약 14px center · 회색 바탕
```
= 표 T2 의 2~5행(합친 칸)·2열, 자리, 원본에 글자가 2줄(크기·정렬 짐작), 바탕이 회색. "빈 칸" 이면 원본에서 그 칸이 비어 있다.
이 숫자(자리·합친 칸·크기·정렬·바탕)는 build.py 가 그대로 쓰므로 **내가 다시 잴 필요가 없다.**

## 2. 전체 보기

`view.py page <초안> --to 1` 로 쪽 전체를 보고 정한다:
- 이 서류가 무엇인지 (제목), 빈 서식인지 값이 적힌 서류인지.
- grid 가 **잘못 찾은 것**: 글자를 표로 잘못 본 작은 표 → `skip`, 티끌·검은 네모(맞춤 표시)·바코드 글자 → 그 글자 덩어리 `null`.
- grid 가 **못 찾은 것**: 선이 흐려 빠진 표·칸이 있으면 `crop` 으로 그 자리를 보고 `extra` 로 더한다 (드물다).

## 3. 칸 읽기 → `layout.json` 의 `cells`·`blocks`

표마다 `view.py table <초안> T<n> --rows a-b --to 2` 로 칸 이름이 찍힌 그림을 보고, **칸마다** 적는다. 표 밖 글자 덩어리는 `view.py crop … --cells` 로 보고 `blocks` 에 적는다.

- **인쇄된 글자(항목명·제목·안내문·보기·괄호 글자)는 보이는 그대로** — 띄어쓰기·괄호·기호(□ ※ ▶ :)까지. 줄이 나뉘어 있으면 `\n`. 안내문·약관은 끝까지 다 적는다 (줄이지 않는다).
- **값(서류마다 달라질 것)은 `{키}`**. 빈 서식이면 빈 칸·밑줄·괄호 안이 값 자리, 실서류면 손글씨·타자·다른 글꼴로 채운 글자가 값이다.
  실서류의 값 글자는 **절대 옮기지 않는다** (`2020-11592` → `{warrant.no}`). 한 칸에 고정 글자와 값이 섞이면 그대로: `"(통화코드 : {currency}          )"`.
- **체크 보기** `□ 등록 □ 변경 □ 해제` 처럼 하나를 고르는 묶음 → `{apply.kind:등록|변경|해제}` (보기 글자는 원본 그대로). 실서류에서 ■ 로 체크돼 있어도 보기 전부를 적는다.
- **도장·서명 자리**: `(서명/인)` 같은 날인 자리 → `{sign:sign.customer|customer.name|(서명/인)}` (표시 글자 원본대로), 기관 직인 → `{seal:seal.court|대전지방법원장}`.
- **못 읽은 곳은 짐작하지 않는다.** `crop` 으로 더 좁게 보고, 그래도 안 보이면 그 칸은 비워 두고 보고에 "판단이 안 선 것"으로 적는다. 손글씨와 도장이 겹친 곳의 인쇄 글자도 같다.
- **은행 결재란**(담당·책임자·부점장 … 아래 빈 칸)·접수란의 빈 칸은 고객이 쓰는 곳이 아니라 **값 자리가 아니다** — 머리 글자만 적고 빈 칸은 비워 둔다.
  표 밖에 "년 월 일" 이 인쇄돼 있으면 그 글자 덩어리를 `"{apply_y} 년  {apply_m} 월  {apply_d} 일"` 처럼 **한 덩어리 안에** 적는다 (따로 `extra` 로 겹쳐 놓지 않는다).
- 그림에 없는 항목명을 더하지 않는다 ("이런 서식이면 보통 있는 항목" 금지).
- 칸 옵션은 필요할 때만: `{"t": "…", "align": "center", "size": 12, "bold": true}` (grid 짐작이 틀렸을 때). 옵션 전체는 `build.py` 맨 위 설명.

`layout.json` 꼴 (완성 예시: `$T/example/layout.json` — **꼴만 참고**, 내용은 지금 원본에서):

```json
{
 "form": {"name": "예금(신탁) 잔액증명 의뢰서", "group": "bank_form", "category": "internal"},
 "pages": [
  {"cells": {"T2.2": "신청구분", "T2.3": "{apply_type:등록|변경|해제}", "T2.4": "발급기준일", "T2.5": "{base_date}",
             "T2.16": "(통화코드 : {currency}                    )"},
   "blocks": {"B1": {"t": "예금(신탁) 잔액증명 의뢰서", "bold": true}, "B2": null},
   "skip": [],
   "extra": [{"box": [180, 123, 340, 140], "t": "{bank.branch}"}]}
 ],
 "fields": {"apply_type": {"label": "신청구분", "type": "checkbox", "source": "rule:choice", "choices": ["등록", "변경", "해제"],
                           "description": "잔액증명 신청 종류"}},
 "lists": {"accounts": {"min": 1, "max": 6, "fields": {"number": {"label": "계좌번호", "type": "text", "source": "rule:account"}}}}
}
```

`group`: identity · family · income · tax · finance · real_estate · business · corporate · fx · bank_form. `category`: external(고객이 가져오는 서류) · internal(은행 서식).

## 4. 키와 항목 설명 → `layout.json` 의 `fields`

`{키}` 마다 `fields` 에 적는다: `label`(원본 항목명 그대로), `type`, `source`, `description`(이 칸이 무엇인지 한 줄 — 사람이 가장 먼저 검토한다),
체크면 `choices`. 아래 "키·값 규칙"을 따른다. 읽을 것: `guide/studio/keys.md` 3~5절, `docgen/forms/_common/values.md` 1~106줄(값 종류 표).
인쇄된 빈 행이 정해진 수만큼 있는 표(계좌번호 칸 6개 등)는 `lists` 에 `"min": 1, "max": N` 으로 두고 칸에는 `{accounts.0.number}` … `{accounts.5.number}`.

## 5. 만들기·검사

```bash
python $T/build.py <초안>                                    # 오류면 메시지대로 layout.json 을 고친다
python -m pytest $T/test_draft.py --draft <초안> -q          # 검사
```

| 검사 | 통과 못 함 (problems) | 경고 (warnings — 고치거나 왜 두는지 적는다) |
|---|---|---|
| 파일 | `layout.json`·`template.html.j2`·`form.json`·`fields.md`·`grid_<n>.json` 없음 | |
| 미리보기 | 명령 오류, `checks`, `overflow`, 쪽 수 ≠ 원본 | |
| 빠진 글자 | | 원본에 글자가 있는데 `layout.json` 에 안 적은 칸·글자 덩어리 |
| 모양 대조 | | 원본과 렌더를 **같은 도구로 재서** 맞댄 것: 표 선 자리, 원본엔 글자 있는데 렌더 칸이 빔 / 그 반대, **칸 가장자리에 닿은 글자(넘쳐 잘림)**, 글자 덩어리 너비 |
| 값 | | 값이 칸 밖으로 나감, 다른 칸에 같은 사람 값, 날짜·금액 표기 섞임, 빈 값이 많음 |

검사는 seed 1 렌더를 `render_<n>.png` 로 두어 `view.py compare` 가 쓴다.

## 6. 원본과 맞대 보며 고치기

**덩어리마다** `view.py compare <초안> x0 y0 x1 y1 --to 4` 로 같은 자리의 원본·렌더를 보고 고친다. 쪽 전체 한 장으로 보지 않는다 (작아서 차이가 안 보인다).
경고에 나온 칸·덩어리부터, 그다음 표마다 한 번씩. 고칠 곳은 **늘 `layout.json`** 이고 `build.py` → 검사를 다시 돌린다 (template 을 직접 고치면 다음 build 에서 사라진다).

| 보이는 것 | 고치는 법 (`layout.json`) |
|---|---|
| 글자가 칸을 넘치거나 잘림 | 그 칸 `size` 를 줄이거나 `\n` 으로 원본처럼 줄을 나눈다 |
| 글자가 원본보다 크거나 작음, 굵기 다름 | `size` · `bold` |
| 정렬이 다름 | `align` (left·center·right), 세로는 `valign` |
| 칸 안 글자 사이 간격(보기 사이 띄움)이 다름 | 띄어쓰기 수 |
| 글자가 다름·빠짐 | 그 칸 글자를 원본대로 (crop 으로 다시 읽고) |
| 값이 들어갈 곳에 고정 글자가 있음 / 그 반대 | `{키}` 로 바꾸거나 글자로 |
| 표 선이 원본과 다름 (경고) | grid 가 잘못 잰 것: 그 자리를 crop 으로 보고 보고서에 적는다 (layout 으로 선을 옮기지는 않는다) |
| 값이 칸의 뜻에 안 맞음 (기간 칸에 메모 글 …) | `fields` 의 `source` (아래 "키·값 규칙") |
| 칸끼리 관계가 틀림 (끝일 < 시작일, 대리인 = 고객) | `generate.py` (아래) |

글꼴·선 굵기·바탕색은 생성할 때 무작위로 바뀌므로 맞추지 않는다. 원본이 좁은 글꼴이면 build.py 가 글자를 가로로 줄여 맞춘다 (`squeeze`).

## 7. 보고

| 항목 | 내용 |
|---|---|
| 서식 | ID · 이름 · 쪽 수 · 원본 종류 · group · category |
| 칸 | 값 자리 수, 반복 표(행 min~max), 도장·서명, `generate.py` 유무와 맞춘 관계 |
| 검사 | 마지막 검사의 문제·경고 수, 남긴 경고와 까닭 |
| 비교 | 덩어리마다 원본과 같은지, 남은 차이 |
| 판단이 안 선 것 | 못 읽은 칸, 값인지 고정 글자인지 애매한 칸, 키가 애매한 칸 |
| 사람이 볼 것 | `fields.md` 의 키·설명 (데이터셋을 만든 뒤에는 키를 못 바꿈), 비교 그림 |

에이전트 진행기로 돌면 이 보고를 초안 폴더의 `report.md` 로 쓴다.

## 키·값 규칙

**키** (keys.md): 영어 소문자 `누구의.무엇` — `customer.name`, `agent.phone`, `employer.name`, `loan.amount`, `period.start`, `issue_date`, `account`.
같은 뜻은 서식 안에서 같은 이름. 한글·대문자·번호 붙은 키(`name2`) 금지. 한 키가 다른 키의 앞부분이면 안 됨(`account` 와 `account.number` 동시 금지).
같은 사람 이름이 두 자리에 있으면 뒤 자리는 역할로(`applicant.name`) 짓고 source 를 같게 한다.

**type**: `text` `amount` `number` `date` `checkbox`. 도장·서명(`{sign:…}`·`{seal:…}`)은 `fields` 에 넣지 않는다.

**source** (값 만드는 법). 전체 목록과 예시 값은 `docgen/forms/_common/values.md` 에서 찾는다 (추측하지 않는다).
- 고객 본인·본인 회사 값 → `profile.…` (`profile.person.name`·`.birth`·`.rrn`·`.mobile`·`.email`·`.name_en`·`.address.road_short`, `profile.business.biz_no`, `profile.issue_date` …).
- 그 밖 → `rule:<종류>` (`date` `amount` `account` `currency` `bank` `branch` `company` `number` `count` `percent` `rate` `note` …).
- 보기 `rule:choice` + `choices`(원본 글자 그대로), 늘 같은 글자 `rule:fixed` + `text`, 틀 `rule:pattern` + `pattern`(`#` 숫자), 반복 행 날짜 `rule:date_seq`, 짧은 자유 글 `rule:free_text`, 늘 빈 칸 `rule:empty`.
- **칸마다 값 종류 표에서 가장 가까운 것을 고른다**: HS 코드 `rule:hs_code`, 가격 조건 `rule:incoterms`, 항구 `rule:port`, SWIFT `rule:swift`, 외화 금액 `rule:fx_amount`,
  통화 `rule:currency`, 국가 `rule:country`, 은행 `rule:bank`, 품목 `rule:goods`, 회사 `rule:company`, 개수 `rule:count` …
  표에 없으면 그 칸에 올 만한 값 몇 개를 `rule:choice` 로(예: 기간 조건 `["AT SIGHT", "30 DAYS AFTER SIGHT", "90 DAYS AFTER B/L DATE"]`), 꼴이 정해진 번호·코드는 `rule:pattern`.
- `rule:note`·`rule:free_text`·`rule:reason` 은 "해당 없음", "본인 요청", "계좌 정리" 같은 **메모 글**을 낸다 → 비고·사유·메모 칸에만. 기간·장소·조건·코드 칸에 쓰면 엉뚱한 값이 된다.
  `rule:account`·`rule:number` 는 계좌번호 꼴(`343-882701-43380`)이라 은행 코드·고객번호 같은 짧은 코드 칸에는 `rule:pattern`(`####`, `###-##-######`)이 낫다.
- 정말 모르겠으면 `rule:choice` 로 그럴듯한 보기 두세 개를 두고 "판단이 안 선 것"에 적는다. 키·위치가 맞으면 source 는 나중에 고칠 수 있다.

**값이 이상하게 나오는 함정** (실제로 겪은 것):
- `rule:phone`·`rule:address`·`rule:email` 은 **고객 본인 값**을 낸다. `rule:person` 도 자주 고객 이름이다.
  대리인·보증인·수령인 같은 **다른 사람** 칸은 이름 `rule:other_person`, 전화 `rule:pattern` `"010-####-####"`, 생년월일은 `generate.py` 로.
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
- 보기 중 **하나만** 고르는 묶음(□등록 □변경 □해제) → 키 하나, `type: checkbox`, `rule:choice` + `choices`, 칸 글자 `{키:보기1|보기2|보기3}`.
- **여러 개를 같이** 고를 수 있는 묶음(□입금내역 □출금내역 □대출이자 …) → 보기마다 키 하나(`detail.deposit`, `detail.withdraw` …),
  각각 `choices: ["<보기 글자>"]` 하나짜리 + `generate.py` 에서 가끔 `None` (보기 하나짜리는 늘 체크되므로). 칸 글자는 보기마다 `{detail.deposit:입금내역} {detail.withdraw:출금내역}`.
- 원본이 어느 쪽인지 모르겠으면 "판단이 안 선 것"에 적고 하나만 고르는 쪽으로.

**나뉜 날짜 칸의 꼴 (`part`·`format`)**: 한 값을 숫자 묶음으로 나눠 칸마다 넣는다. `"part": 0` 첫 숫자 묶음(년), `1` 둘째(월), `2` 셋째(일),
`"format": "number"` 숫자만 남김. 예: `"apply_y": {"label": "신청일 년", "type": "number", "source": "profile.issue_date", "part": 0, "format": "number"}`.

**질문 설명 `q`**: kie 질문의 항목 줄은 `- 키: 항목명 (괄호 설명)` 이다. 항목명만으로 헷갈리는 칸에만 넣는다:
같은 항목명이 두 군데(신청인 성명·대리인 성명 → `"q": {"label": "대리인 성명"}`), 항목명이 없거나 "금액"처럼 막연함(`"q": {"note": "이체 금액"}`).
반복 표 열에는 `q.note` 를 넣지 않는다 (자동 "몇 번째 행" 설명이 사라짐).

**칸끼리 관계 → `generate.py`** (관계가 있을 때만): `adjust(d, p, rng)` 로 값을 맞춘다 (NEW_FORM_SPEC 8절: `docgen.formkit` 도우미와 표준 라이브러리만,
칸 목록에 있는 키만 고침, 난수는 `rng` 만). 예시: `$T/example/generate.py` (년·월·일 칸을 한 날짜에서, 다른 사람 생년월일, 조건에 따라 표 값 비우기).
반복 표를 조건에 따라 비울 때는 목록을 지우지 말고 행의 값만 `None`.

## 8. 등록 (사용자가 하라고 할 때만 — 에이전트 회차에서는 하지 않는다)

- 어디에: 빈 서식·공개 견본 → `docgen/forms/<ID>/`, **실서류에서 만든 것 → `$DOCGEN_PRIVATE_FORMS/<ID>/`**. 폴더가 이미 있으면 멈추고 보고 (덮어쓰지 않음).
- 옮기기 (NEW_FORM_SPEC 6절) — 명령 하나. 검사 통과·ID·폴더가 비었는지 확인하고, 하나라도 안 되면 아무것도 옮기지 않는다:

```bash
python .claude/skills/form-from-image/register.py out/form_drafts/<ID> --to public          # docgen/forms/<ID>/
python .claude/skills/form-from-image/register.py out/form_drafts/<ID> --to private --real  # $DOCGEN_PRIVATE_FORMS/<ID>/ (실서류)
```
  `template.html.j2` → `look/template.html.j2`, `form.json` 의 `fields`·`lists` → `fields.json`, 나머지 → `form.json`, `source*.png`, `generate.py` 를 옮기고
  카드(`formdir card`)와 `formdir check` 를 돌린다. 작업 파일(`layout.json`·`grid_*`·`page_*`·`view_*`·`render_*`·`fields.md`·`review.md`·`report.md`·`check*`·`run.json`·`relab_*.log` …)은 옮기지 않는다.
  studio 는 **이미지로 서식 만들기 › 결과 › [등록]**, 명령줄은 `python -m formagent register --id <ID> --to public|private` 가 같은 것을 부른다.
- 더 확인: `python -m docgen.formdir card <ID>` 의 질문→답 예시가 말이 되는지 · `python -m docgen.preview <ID> --rows max --out out/<ID>`.
- 사용자에게: studio 서식 › **서식 다시 읽기** → 목록에 나옴 → **생성 사례 › 미리보기/검수** 에서 원본과 비교해 검수 완료.
  시험 생성: `python -m docgen.bench build --types <ID> --per-doc 2 --out out/try_<ID>`.
