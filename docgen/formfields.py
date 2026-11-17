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
- 코드 서식은 값을 서식 폴더의 생성 함수(generate.py 의 @doc)가 만들고, fields·lists 를 적으면 그 위에 덮어쓴다.
- 처음 한 번 예전 자리(regions.json, form.json 의 값 선언)를 모아 만든다 (adopt, python -m docgen.formdir migrate).
"""
from __future__ import annotations

import json
import threading
from contextlib import contextmanager
from pathlib import Path

NAME = "fields.json"
VALUE_KEYS = ("fields", "lists", "shared_copies")   # html 값 선언 (예전 form.json)
REGION_KEYS = ("regions", "variants")              # html 칸 덮어쓰기 (예전 regions.json)
UNIT = {"overlay": "pt", "html": "px"}
_lock = threading.Lock()
_drafts = threading.local()


@contextmanager
def draft(doc_id: str, body: dict):
    """이 스레드에서 렌더링하는 동안 doc_id 의 칸 목록을 body 로 (저장하지 않은 값 출처 미리보기, studio 자리·템플릿)."""
    d = getattr(_drafts, "map", None)
    if d is None:
        d = _drafts.map = {}
    old = d.get(doc_id)
    d[doc_id] = body
    try:
        yield
    finally:
        if old is None:
            d.pop(doc_id, None)
        else:
            d[doc_id] = old


def _draft(doc_id: str) -> dict | None:
    return (getattr(_drafts, "map", None) or {}).get(doc_id)


def path(doc_id: str) -> Path:
    from . import formdir

    return (formdir.folder(doc_id) or formdir.copy_dir(doc_id) or formdir.home(doc_id)) / NAME


def read(doc_id: str) -> dict | None:
    """칸 목록 (engine·unit 칸 뺀 것). 아직 없으면 None. 이 스레드에 초안이 있으면 초안."""
    dr = _draft(doc_id)
    if dr is not None:
        return json.loads(json.dumps({k: v for k, v in dr.items() if k not in ("engine", "unit")}))
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
    from .regions import engine

    body = read(doc_id) or {}
    if engine(doc_id) == "html":   # "code"(생성 함수 값 그대로)만 적힌 칸 목록은 결과를 바꾸지 않는다
        from .htmlform import own

        live = own(body) or any(body.get(k) for k in ("regions", "variants", "shared_copies"))
        return [p] if live else []
    return [p] if any(body.get(k) for k in body) else []


def exists(doc_id: str) -> bool:
    return _draft(doc_id) is not None or path(doc_id).exists()


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
            cur[k] = keep_q(cur.get(k), v) if k in ("fields", "lists") else v
    return write(doc_id, cur)


def keep_q(old, new):
    """칸 선언을 통째로 바꿀 때 (html 편집기 저장) 있던 칸의 질문 설정 "q" 는 남긴다 (새 값에 q 가 없으면).
    fields {키: {…}} 와 lists {이름: {fields: {칸: {…}}}} 둘 다."""
    if not isinstance(old, dict) or not isinstance(new, dict):
        return new
    out = {}
    for k, v in new.items():
        o = old.get(k)
        if isinstance(v, dict) and isinstance(o, dict):
            if "fields" in v and isinstance(v["fields"], dict):   # 반복 표
                v = {**v, "fields": keep_q(o.get("fields"), v["fields"])}
            elif "q" in o and "q" not in v:
                v = {**v, "q": o["q"]}
        out[k] = v
    return out


def merge_declared(doc_id: str, declared: dict) -> tuple[Path, int]:
    """코드 서식 칸 목록에 생성 함수 칸(declare 결과, source "code")을 더한다. 사람이 값 출처를 바꾼 칸은 그대로 둔다.
    (파일, 새로 더한 칸 수)."""
    adopt(doc_id)
    cur = read(doc_id) or {}
    n = 0
    fields = cur.setdefault("fields", {})
    for k, e in declared.get("fields", {}).items():
        if k not in fields:
            n += 1
        if fields.get(k, {}).get("source", "code") == "code":
            fields[k] = {**fields.get(k, {}), **e}
    lists = cur.setdefault("lists", {})
    for name, L in declared.get("lists", {}).items():
        mine = lists.setdefault(name, {"source": "code", "fields": {}})
        for sub, e in L["fields"].items():
            if sub not in mine.setdefault("fields", {}):
                n += 1
            if mine["fields"].get(sub, {}).get("source", "code") == "code":
                mine["fields"][sub] = {**mine["fields"].get(sub, {}), **e}
    for k in ("fields", "lists"):
        if not cur[k]:
            cur.pop(k)
    return write(doc_id, cur), n


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
