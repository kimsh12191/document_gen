# 완성 예시: 예금(신탁) 잔액증명 의뢰서

이 스킬 순서대로 만든 초안의 **내가 쓰는 파일**입니다 (원본: 하나은행 공개 서식 `docgen/forms/hf011/look/original.pdf` 1쪽).
`template.html.j2`·`form.json`·`fields.md` 는 `build.py` 가 이 두 파일과 `grid_1.json` 에서 만듭니다.

| 파일 | 볼 것 |
|---|---|
| `layout.json` | 칸 이름(`T2.7`)마다 원본 글자, 값 자리 `{키}`, 체크 `{키:보기|보기}`, 서명 `{sign:…|…|(서명/인)}`, 표 밖 글자 덩어리(`B1`…, 그리지 않을 것 `null`), `extra`, 키마다 `label`·`type`·`source`·`description`, 인쇄된 빈 행 `lists` |
| `generate.py` | 칸끼리 관계: 지점 글자 겹침 떼기, 시작일 ≤ 끝일, 다른 사람 생년월일, 조건에 따라 표 값 비우기, 보기 하나짜리 체크 |

다시 만들어 보기 (초안 폴더 하나에서):

```bash
mkdir -p out/form_drafts/zz_example && cd out/form_drafts/zz_example
python -c "import pymupdf; pymupdf.open('../../../docgen/forms/hf011/look/original.pdf')[0].get_pixmap(dpi=200).save('source.png')"
cd ../../.. && cp .claude/skills/form-from-image/example/{layout.json,generate.py} out/form_drafts/zz_example/
python .claude/skills/form-from-image/grid.py out/form_drafts/zz_example
python .claude/skills/form-from-image/build.py out/form_drafts/zz_example
python -m pytest .claude/skills/form-from-image/test_draft.py --draft out/form_drafts/zz_example -q
```

칸 이름은 grid.py 가 원본에서 잰 순서이므로 **다른 원본에 그대로 쓸 수 없습니다** — 꼴만 참고합니다.
