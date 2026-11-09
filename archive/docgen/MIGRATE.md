# 예전 서식 파일 자리에서 옮기기 (끝난 작업)

2026-11 docgen/README.md 에서 옮겼습니다. 지금 저장소에는 예전 자리가 없고 `*.migrated` 파일도 없습니다.

예전 자리는 새 자리에 없을 때만 읽습니다: 서식 파일은 `forms/layouts/<분류>/<No>.json`, `하나은행_서식자료/` 의 PDF, `forms/images/<ID>/`, `templates/<그룹>/<ID>.html.j2`, `templates/copies/<ID>/`, `templates/variants/<ID>/`, 서식 폴더 바로 아래 `template.html.j2`·`page_<n>.png`. 사람 수정은 `forms/regions/<ID>.json`, `forms/overrides/<ID>.json`, `forms/html_regions/<ID>.json`, 이미지 서식 폴더의 `overrides.json`, `<변형>.regions.json`.

한꺼번에 옮기기:

```bash
python -m docgen.formdir migrate            # 무엇을 어디로 옮길지 목록 (예전과 새 파일이 다르면 "건너뜀: 다름")
python -m docgen.formdir migrate --apply    # 옮김: 글 파일은 복사하고 예전 것을 <이름>.migrated 로, 그림·PDF 는 옮김.
                                            # overlay 는 칸 목록 fields.json 을 만든다 (못 찾은 예전 수정이 있으면 알려 줌)
python -m docgen.regions check --all
```

영역 편집기에서 저장하면 그 서식의 사람 수정은 바로 새 자리로 옮겨집니다(overlay 는 칸 목록이 만들어짐). 서식 해시(studio "검수 후 바뀜")에는 파일을 옮기기 전 자리 이름을 넣으므로 위치를 옮겨도 그대로입니다. 생성 코드(`realform.py`·`htmlform.py` 등)가 바뀌면 그 코드를 쓰는 서식의 해시는 바뀝니다.
