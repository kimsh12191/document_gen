# 작업: 서식 이미지 → html 서식 (docgen)

`input/source.png` 는 은행·공공 서류의 서식 이미지다. 이 서식을 **docgen html 서식**으로 만든다. 결과는 `output/` 에 두 파일로 쓴다.
작업 폴더 밖의 파일은 바꾸지 않는다.

{target}

## 만들 것

1. `output/template.html.j2` — Jinja2 템플릿
   - 맨 위 두 줄은 그대로: `{% extends "_base.html.j2" %}`, `{% import "_macros.html.j2" as m with context %}`
   - 내용은 `{% block content %} … {% endblock %}`, 서식 전용 CSS 는 `{% block style %} … {% endblock %}`
   - **값은 반드시 `{{ f("키", label="항목명") }}` 로 넣는다.** f() 가 값과 위치를 정답으로 기록한다. 그냥 `{{ d.키 }}` 로 쓰면 정답에 안 들어간다.
   - 고정 문구(제목, 항목명, 안내문)는 서식에 적힌 그대로 쓴다. 원본 이미지와 칸 배치·선·글자 크기가 비슷하게.
   - 개수가 바뀌는 표(거래내역 등)는 반복 행으로: `{% for r in d.rows %}<tr><td>{{ f("rows." ~ loop.index0 ~ ".date", label="거래일") }}</td>…</tr>{% endfor %}`.
     A4 서식은 내용이 넘치면 자동으로 다음 쪽으로 나뉜다 (표 머리글 반복, 쪽 번호). 쪽을 직접 나누지 않는다.
   - 도장 자리: `{{ m.seal("회사인", key="company", kind="직인") }}`, 체크 보기·결재란 등 매크로는 `input/_macros.html.j2` 를 본다.
2. `output/form.json` — 값 선언
   ```json
   {"name": "서식 이름", "group": "{group}", "category": "external 또는 internal", "page": "a4", "origin": "analyzer", "parent": null,
    "fields": {"키": {"label": "항목명", "type": "text|date|amount|…", "source": "값 출처"}},
    "lists": {"rows": {"min": 3, "max": 60, "fields": {"date": {"source": "rule:date_seq"}, "amount": {"source": "rule:amount"}}}}}
   ```
   - 키는 영어 snake_case 경로 (`customer.name`, `account.number`, `issue_date`). 표준 키는 `input/keys.json` 에서 고른다.
   - 값 출처: `profile.<경로>`(고객 프로필, 예: `profile.person.name`, `profile.person.address.road_full`, `profile.employment.company.name`) 또는
     `rule:<종류>`(`date amount account phone number company person address note …`), `rule:choice`(+ `"choices": [...]`), `rule:fixed`(+ `"text"`),
     `rule:free_text`, `rule:empty`, `rule:date_seq`(반복 행에서 행마다 늘어나는 날짜).
   - 템플릿에 쓴 키는 모두 선언하고, 선언한 키는 모두 템플릿에 쓴다.

## 확인하는 법 (작업 폴더에서)

```bash
python -m docgen.preview --dir output --rows max --out check      # 행을 최대로: 여러 쪽으로 잘 나뉘는지
python -m docgen.preview --dir output --rows min --out check      # 행을 최소로
```

출력 JSON 의 `checks` 가 비어 있어야 한다 (선언했는데 안 나온 키, 템플릿에 있는데 값이 없는 키). 만든 그림(`check/…/page_p1.png`)을
`input/source.png` 와 나란히 보고 다르면 고친다. 서너 번 되풀이해 비슷해지면 끝낸다.

## 참고 파일 (`input/`)

- `TEMPLATE_GUIDE.md`: 서식 작성 가이드 (생성 함수 부분은 이 작업에서는 form.json 이 대신한다)
- `example_simple.html.j2`: 칸 위주 서식 예 (재직증명서), `example_rows.html.j2`: 반복 표 예 (거래내역)
- `_macros.html.j2`: 제목·표·체크 보기·도장 매크로
- `keys.json`: 표준 키 사전

{feedback}
