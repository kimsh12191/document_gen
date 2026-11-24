# 완성 예시: 예금(신탁) 잔액증명 의뢰서

이 스킬 순서대로 만든 초안 폴더입니다 (원본: 하나은행 공개 서식 `docgen/forms/hf011/look/original.pdf` 1쪽).
그림은 `python -c "import pymupdf; pymupdf.open('docgen/forms/hf011/look/original.pdf')[0].get_pixmap(dpi=144).save('source.png')"` 로 만들 수 있습니다.

| 파일 | 볼 것 |
|---|---|
| `fields.md` | 칸 표: 키·항목 설명·source·확신, 반복 표, 도장·서명, 칸끼리 관계, 판단이 안 선 것 |
| `template.html.j2` | 선 있는 영역 = table (colgroup %, tr height px, rowspan/colspan), 빈 칸 6개 계좌번호, 체크 보기, (서명/인) 자리 |
| `form.json` | 초안 꼴 (`fields`·`lists` 포함), `q.label`, `part`·`format`, `rule:pattern` |
| `generate.py` | 년·월·일 칸을 한 날짜에서, 다른 사람 생년월일, 조건에 따라 표 값 비우기, 보기 하나짜리 체크 |

검사: `--rows min`·`max`·seed 1~3 모두 1쪽, `checks: []`, `overflow: false`.
