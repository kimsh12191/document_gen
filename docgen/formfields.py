"""서식의 칸 목록 fields.json (서식 폴더, docgen/formdir.py). 사람이 고치는 곳은 이 파일 하나다.

overlay 서식 (hf###, img_*)
  {"engine": "overlay", "unit": "pt",
   "pages": [{"width", "height", "bank"?, "staff": [{"role", "rect"}]}],    쪽 크기·결재란 칸
   "items": [{"t", "page", "label", "rect"|"options"|"parts"|"mark", "key"?, "kind"?, "source"?, …,
              "edited"?: true, "added"?: true}],                             기재 자리 (순서대로 키 번호가 붙는다)
   "erase": [{"page", "rect", "fill"}], "marks": {...},                      배경 지우기·표시 설정
   "confirmed_erase"?, "updated"?,                                           기록
   그 밖의 칸(name, class, no, file, texts …)은 자동 추출 레이아웃에서 그대로}

- 처음 한 번 자동 추출 레이아웃(layout.json)과 예전 사람 수정(regions.json)을 합쳐 만든다 (overrides.freeze,
  python -m docgen.formdir migrate). 그 뒤로는 이것이 기준이고 layout.json 은 자동 초안으로만 남는다.
- studio 영역 편집기는 고친 것을 overrides 꼴(match·set·add·erase)로 보내고, 서버가 이 파일에 바로 합쳐 쓴다.

html 서식 (템플릿이 칸을 만든다 — 반복 행·조건 칸·레이아웃 변형은 템플릿에 그대로)
  {"engine": "html", "unit": "px",
   "fields": {"<키>": {"label", "type", "source", …}},                      값 선언: 값 출처로 값을 만든다 (docgen/htmlform.fill)
   "lists": {"<이름>": {"min", "max", "fields": {...}}}, "shared_copies"?,  반복 행 값 선언
   "regions": [{"key", "occurrence"?, "label"?, "source"?, "rect"?, "drop"?, …}],   칸 하나씩 덮어쓰기: 항목명·값·위치·빼기·새 칸
   "variants": {"<변형 ID>": {"regions": [...]}}}                          레이아웃 변형별 덮어쓰기 (docgen/html_regions.py)
- 복제·분석기 서식은 예전 form.json 의 fields·lists 가 여기로 왔다 (form.json 에는 이름·그룹·부모·출처만 남는다).
- 코드 서식은 값을 생성 함수(docgen/docs/*.py)가 만들고, fields·lists 를 적으면 그 위에 덮어쓴다.
- 처음 한 번 예전 자리(regions.json, form.json 의 값 선언)를 모아 만든다 (adopt, python -m docgen.formdir migrate).
"""
from __future__ import annotations

import json
import threading
from pathlib import Path

NAME = "fields.json"
VALUE_KEYS = ("fields", "lists", "shared_copies")   # html 값 선언 (예전 form.json)
REGION_KEYS = ("regions", "variants")              # html 칸 덮어쓰기 (예전 regions.json)
UNIT = {"overlay": "pt", "html": "px"}
_lock = threading.Lock()


def path(doc_id: str) -> Path:
    from . import formdir

    return (formdir.folder(doc_id) or formdir.copy_dir(doc_id) or formdir.home(doc_id)) / NAME


def read(doc_id: str) -> dict | None:
    """칸 목록 (engine·unit 칸 뺀 것). 아직 없으면 None."""
    p = path(doc_id)
    if not p.exists():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    from .regions import engine

    want = engine(doc_id)
    if data.get("engine") not in (None, want):
        raise ValueError(f"{doc_id} 는 {want} 서식인데 {p} 는 {data.get('engine')} 칸 목록입니다")
    return {k: v for k, v in data.items() if k not in ("engine", "unit")}


def hash_files(doc_id: str) -> list[Path]:
    """서식 해시에 넣을 칸 목록 (내용이 있을 때만 — 없거나 빈 서식은 해시가 예전 그대로)."""
    p = path(doc_id)
    if not p.exists():
        return []
    body = read(doc_id) or {}
    return [p] if any(body.get(k) for k in body) else []


def exists(doc_id: str) -> bool:
    return path(doc_id).exists()


def write(doc_id: str, body: dict) -> Path:
    from .regions import engine

    eng = engine(doc_id)
    p = path(doc_id)
    with _lock:
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps({"engine": eng, "unit": UNIT[eng], **{k: v for k, v in body.items() if k not in ("engine", "unit")}},
                                  ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        tmp.replace(p)
    return p


def update(doc_id: str, values: dict, keys: tuple) -> Path:
    """칸 목록의 keys 칸을 values 의 것으로 바꾼다 (비었으면 뺀다). html 서식에 칸 목록이 아직 없으면 예전 자리를 먼저 모은다."""
    from .regions import engine

    if engine(doc_id) == "html":
        adopt(doc_id)
    cur = read(doc_id) or {}
    for k in keys:
        v = values.get(k)
        if v in (None, [], {}):
            cur.pop(k, None)
        else:
            cur[k] = v
    return write(doc_id, cur)


def adopt(doc_id: str) -> Path | None:
    """html 서식의 칸 목록이 없으면 예전 자리를 모아 만든다: 사람 수정 regions.json(과 그 전 자리들), 복제·분석기 서식
    form.json 의 값 선언(fields·lists·shared_copies — form.json 에서는 빠진다). 예전 수정 파일은 <이름>.migrated 로.
    이미 있으면 None."""
    from . import htmlform, regions

    if exists(doc_id):
        return None
    body = regions.read(doc_id)
    d = htmlform.form_dir(doc_id)
    if d is not None:
        form = json.loads((d / "form.json").read_text(encoding="utf-8"))
        vals = {k: form.pop(k) for k in VALUE_KEYS if k in form}
        if vals:
            body.update(vals)
    p = write(doc_id, body)
    if d is not None and vals:
        (d / "form.json").write_text(json.dumps(form, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for f in [regions.path(doc_id), *regions.legacy(doc_id).values()]:
        if f.exists():
            f.replace(f.with_name(f.name + ".migrated"))
    return p
