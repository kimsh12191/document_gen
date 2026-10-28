# 서식 껍데기 고치기 (사람·VLM 공용 안내)

서식의 **모양(껍데기)** 만 원본에 맞게 고칠 때 읽는 문서입니다. 값·키·정답은 건드리지 않습니다.
VLM 에게 맡길 때는 이 파일과 아래 "VLM 에게 줄 것"을 함께 넘깁니다.

> 실서류에서 만든 서식(`$DOCGEN_PRIVATE_FORMS/<ID>/`)의 그림은 외부 VLM 에 보내지 않습니다 (AGENTS.md 규칙 10). 사내 모델에만 맡깁니다.

---

## 1. 서식은 이렇게 생겼다 (사람용 요약)

서식 하나 = 폴더 하나입니다. 폴더 안은 세 칸으로 나뉩니다.

```
docgen/forms/<ID>/
  look/          ① 모양 (껍데기)   — 서류가 어떻게 생겼나
  fields.json    ② 칸 목록         — 어디에 무슨 값이 들어가나 (키·항목명·값 출처·위치)
  (값 만들기)    ③ 값              — 고객 정보로 실제 값을 만든다 (코드 서식은 docgen/docs/<그룹>.py)
```

| | overlay 서식 (`hf###`, `img_*`) | html 서식 (그 밖의 ID) |
|---|---|---|
| ① 모양 | `look/original.pdf`(하나은행 원본) 또는 `look/page_0.png`(견본 사진). **그림이라 고치지 않는다** | `look/template.html.j2` (HTML 템플릿). **여기를 고친다** |
| ② 칸 목록 | `fields.json` 의 `items` = 값이 놓일 사각형 좌표 전부. **칸 위치는 여기서 고친다** | `fields.json` 의 `fields`·`regions` = 템플릿 칸 위에 덮어쓰기. 칸 자리는 템플릿 안 `f("키")` 가 정한다 |
| ③ 값 | 항목명 규칙 + 고객 정보 (`docgen/realform.py`) | 생성 함수(서식 폴더 `generate.py`) 또는 `fields.json` 값 출처 |
| "껍데기만 고친다" 는 | 칸 사각형(`rect`)을 원본 빈칸에 맞추기 | 템플릿의 표·문구·선·배치를 원본처럼 고치기 |

한 줄로: **overlay 는 그림 위에 칸을 맞추고, html 은 칸을 품은 그림(템플릿)을 다시 그린다.**

서식 하나의 파일을 모두 보려면:

```bash
python -m docgen.formdir path <ID>
```

---

## 2. 공통 준비

1. **원본 그림** (목표 모양)
   - overlay `hf###`: `look/original.pdf` (쪽마다 그림으로 바꿔서 준다)
   - overlay `img_*`: `look/page_<n>.png`
   - html 분석기 서식: `source.png` (서식 폴더)
   - html 공식 대조 서식: `form.json` 의 `source.source_file` (예: `forms/official_sources/gov_income.pdf`)
   - html 코드 서식: 원본 그림이 없다. 참고할 실물 서식 그림을 따로 준비한다.
2. **지금 렌더링 그림**
   ```bash
   python -m docgen.preview <ID> --out work/before          # work/before/<ID>/<해시>/page_p1.png …
   ```
   마지막 줄 JSON 의 `pages`(쪽 수)·`fields`(칸 수)·`overflow`·`checks` 를 적어 둔다.
3. **지금 칸 키 목록** (끝나고 비교용)
   ```bash
   python -m docgen.regions show <ID> > work/keys_before.txt
   ```
4. **고칠 파일 백업**: `cp <고칠 파일> <고칠 파일>.bak`

---

## 3. html 서식: 템플릿 고치기

### VLM 에게 줄 것

- 원본 그림, 지금 렌더링 그림, `look/template.html.j2` 전체
- 이 문서의 3장, `docgen/manual/TEMPLATE_GUIDE.md` 의 "2. 템플릿"

### 지시문 (그대로 붙여 넣기)

```
이 서식은 HTML 템플릿(look/template.html.j2, Jinja2)이 모양을 그린다. 껍데기 = 이 템플릿이다.
고칠 수 있는 것은 이 파일(과 레이아웃 변형 variants/<변형>.html.j2)뿐이다.

고쳐도 되는 것
- 표 구조(행·열·칸 합치기), 인쇄 문구, 선, 칸 배치, 글자 크기, 여백, 정렬.

바꾸면 안 되는 것
- {{ f("키", ...) }}, {{ m.xxx(...) }}, {{ d.… }} 는 값이 들어가는 자리다.
  키 이름·개수를 바꾸지 말고, 원본에서 그 값이 들어가는 칸 안으로 옮기기만 한다.
- {% for … %} … {% endfor %} 는 반복 행, {% if … %} 는 조건 칸이다. 감싼 구조를 지우지 말고 표 안의 위치만 맞춘다.
- 첫 줄의 {% extends "…" %}, {% import "…" as m … %} 는 그대로 둔다.
- 공통 틀(docgen/forms/_common/templates/_base.html.j2, _macros.html.j2 등)은 고치지 않는다.
- 외부 그림·글꼴·스크립트(URL)를 넣지 않는다.

할 일
원본 그림과 지금 렌더링 그림을 비교해, 표 구조와 인쇄 문구를 원본처럼 고친 템플릿 전체를 낸다.
값 자리가 원본의 어느 칸에 들어가야 하는지 판단이 안 서면 바꾸지 말고 그 키를 적어 보고한다.
```

### 끝나고 확인

```bash
python -m docgen.preview <ID> --out work/after
python -m docgen.regions show <ID> > work/keys_after.txt
diff work/keys_before.txt work/keys_after.txt      # 키가 빠지거나 생겼으면 껍데기만 고친 게 아니다
```

- `overflow` 가 `false`, `checks` 가 비어 있어야 한다. 쪽 수가 바뀌었으면 원본과 같은지 본다.
- 반복 행이 많은 서식은 `--rows max` 로도 그려 쪽 나눔을 본다.
- 레이아웃 변형이 있으면 변형마다 확인한다 (studio ① 서식 › 레이아웃·샘플링).

---

## 4. overlay 서식: 칸 위치 맞추기

배경 그림은 원본 그대로라 모양을 고칠 일이 없다. 껍데기 작업은 **값이 놓일 사각형을 원본 빈칸에 맞추는 것**이다.

### VLM 에게 줄 것

- 원본 그림(쪽마다), 지금 렌더링 그림, `fields.json`
- 쪽 크기: `fields.json` 의 `pages[i].width`, `pages[i].height` (단위 pt)

### 지시문 (그대로 붙여 넣기)

```
이 서식은 원본 그림을 배경으로 깔고 그 위에 값을 얹는다. 배경 그림은 바꾸지 않는다.
고칠 수 있는 것은 fields.json 뿐이다.

fields.json
- items[]: 값이 놓일 칸 하나.
  t: text(글자) · check(□ 보기, options[].box) · date(년월일, parts) · sign(서명·도장, mark) · copy(따라 쓰기)
  page: 쪽 번호(0부터), rect: [x0, y0, x1, y1] 사각형, label: 그 칸의 항목명, key: 정답 키
- pages[i].staff[]: 결재란 도장 칸 {role, rect}
- erase[]: 원본 배경에 원래 적혀 있던 값을 지울 사각형 {page, rect, fill: "white"|"auto"}
좌표 단위는 PDF pt, 쪽 왼쪽 위가 (0, 0). 그림 픽셀 → pt 는 (그림 가로 픽셀 ÷ pages[i].width) 로 나눈다.

할 일
원본 그림에서 손님이 쓰는 빈칸마다 맞는 items 가 있는지, rect 가 그 빈칸 안에 들어가는지 본다.
- 어긋난 칸: rect 를 고치고 "edited": true 를 붙인다.
- 빠진 빈칸: items 에 추가하고 "added": true 를 붙인다 (t, page, rect, label).
- 빈칸이 아닌 곳(인쇄 글자·은행 사용란)에 잡힌 칸: 그 item 을 지운다.
- key, label 은 바꾸지 않는다 (추가한 칸의 label 은 원본 항목명).
- 결재란 칸(staff)도 같은 방법으로 맞춘다.
고친 fields.json 전체를 낸다. 순서는 바꾸지 말고, 추가한 칸은 같은 쪽 끝에 붙인다.
```

### 끝나고 확인

```bash
python -m docgen.regions check <ID>                 # 형식·쪽 번호
python -m docgen.preview <ID> --out work/after      # 값이 빈칸 안에 들어갔는지 눈으로
python -m docgen.regions show <ID> > work/keys_after.txt && diff work/keys_before.txt work/keys_after.txt
```

- 지운 칸·추가한 칸만큼만 키가 달라져야 한다.
- 사람이 하면 studio ① 서식 › 영역 편집이 더 빠르다 (끌어서 옮기기·그리기, 저장하면 `fields.json` 에 바로 들어간다).

---

## 5. 보고 (VLM·사람 공통)

- 서식 ID, 고친 파일, 원본 그림 출처
- 전·후 렌더링 그림 경로, 쪽 수·칸 수 전후
- 키 비교 결과 (같음 / 달라진 키와 이유)
- 판단이 안 서서 남긴 곳

형식 검사 통과는 "검수 완료"가 아닙니다 (AGENTS.md 규칙 7). 원본과 나란히 놓고 보는 확인은 사람이 합니다.
