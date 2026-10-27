"""화면에서 만든 html 서식: 복제(copy)와 분석기가 이미지에서 만든 것(analyzer). studio 의 html 편집기가 고친다.

서식 폴더 (docgen/formdir.py):
  docgen/forms/<ID>/                공개 서식에서 만든 것 (저장소)
  <private_forms_dir>/<ID>/         실서류 견본에서 만든 것 (저장소 밖, 환경변수 DOCGEN_PRIVATE_FORMS)
    look/template.html.j2           Jinja 템플릿. 기존 서식과 같은 _base·_macros, f("키")·d·val 을 쓴다
    form.json                       {"name", "group", "category", "page", "origin": "copy" | "analyzer", "parent": 부모 ID | null,
                                     "source_image": "source.png" (있으면 편집기에서 원본 겹쳐 보기)}
    fields.json                     칸 목록 (docgen/formfields.py) — 값 선언:
                                     "fields": {키: {"label", "type", "source", "choices"?, "text"?}},
                                     "lists": {이름: {"min", "max", "fields": {하위 키: {...}}}}
                                    (load_form 은 둘을 합쳐 예전 form.json 꼴로 돌려준다. 칸 목록이 없으면 form.json 안의 것)
    source.png                      (있으면) 원본 이미지

값 채우기
- parent 가 있으면 부모 생성 함수로 값을 만든다 (키·정답 구조가 부모와 같다). 그다음 fields 값을 더하거나 덮는다.
- fields 의 키는 점으로 나눈 경로 ("customer.name" → d.customer.name). 값 출처 규칙은 docgen/sources.py (overlay 와 같다).
- lists 는 행 수를 min~max 에서 골라 d.<이름> = [{하위 키: 값}, ...]. 템플릿은 {% for r in d.rows %} … f("rows." ~ loop.index0 ~ ".date").
  행이 많으면 A4 서식은 paginate.js 가 쪽을 나눈다 (표 머리글 반복).
- 미리보기는 rows("min" | "max") 로 행 수를 끝으로 몰고, draft 로 저장하지 않은 템플릿·form.json 을 쓴다 (스레드 안에서만).

템플릿 이름은 "@form/<ID>" 이다. render.env() 의 로더가 이 이름을 서식 폴더(또는 초안)에서 찾는다.
"""
from __future__ import annotations

import json
import os
import random
import re
import shutil
import threading
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent   # docgen/
PREFIX = "@form/"
ID_RX = re.compile(r"[a-z][a-z0-9_]{2,50}")
_local = threading.local()


def form_dir(doc_id: str) -> Path | None:
    """form.json 과 템플릿이 있는 서식 폴더 (예전 자리 docgen/templates/copies/<ID> 도)."""
    from . import formdir

    return formdir.copy_dir(doc_id)


def _template_path(d: Path) -> Path:
    from . import formdir

    return formdir.template_in(d) or d / "look" / formdir.TEMPLATE


def _draft(doc_id: str) -> dict | None:
    return (getattr(_local, "drafts", None) or {}).get(doc_id)


def load_form(doc_id: str) -> dict:
    dr = _draft(doc_id)
    if dr and dr.get("form") is not None:
        return dr["form"]
    d = form_dir(doc_id)
    if d is None:
        raise KeyError(doc_id)
    form = json.loads((d / "form.json").read_text(encoding="utf-8"))
    from . import formfields

    f = formfields.read(doc_id) if formfields.exists(doc_id) else None
    if f is not None:   # 값 선언은 칸 목록 fields.json 에 있다
        form = {k: v for k, v in form.items() if k not in formfields.VALUE_KEYS}
        form.update({k: f[k] for k in formfields.VALUE_KEYS if k in f})
    return form


def write_form(d: Path, form: dict) -> None:
    """새 서식 폴더에 form.json(이름·그룹·부모·출처)과 칸 목록 fields.json(값 선언)을 쓴다."""
    from . import formfields

    meta = {k: v for k, v in form.items() if k not in formfields.VALUE_KEYS}
    vals = {k: form[k] for k in formfields.VALUE_KEYS if form.get(k) not in (None, [], {})}
    (d / "form.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (d / formfields.NAME).write_text(json.dumps({"engine": "html", "unit": "px", **vals}, ensure_ascii=False, indent=1) + "\n",
                                     encoding="utf-8")


def builtin_values(doc_id: str, p, rng: random.Random, data: dict) -> dict:
    """코드 서식: 생성 함수가 만든 값 위에 칸 목록 fields.json 의 값 선언(fields·lists)을 덮어쓴다 (적은 것이 있을 때만)."""
    from . import formfields

    try:
        f = formfields.read(doc_id) if formfields.exists(doc_id) else None
    except KeyError:
        return data
    if f and (f.get("fields") or f.get("lists")):
        return fill(f, p, rng, data)
    return data


def template_source(doc_id: str) -> str:
    dr = _draft(doc_id)
    if dr and dr.get("template") is not None:
        return dr["template"]
    d = form_dir(doc_id)
    if d is None:
        raise KeyError(doc_id)
    return _template_path(d).read_text(encoding="utf-8")


def jinja_source(name: str):
    """render.env() 의 FunctionLoader: "@form/<ID>" → (소스, 파일 이름, 다시 읽을지). 초안이 있으면 초안."""
    if not name.startswith(PREFIX):
        return None
    doc_id = name[len(PREFIX):]
    try:
        src = template_source(doc_id)
    except KeyError:
        return None
    d = form_dir(doc_id)
    path = str(_template_path(d)) if d else name
    mtime = os.path.getmtime(path) if d else 0
    drafted = _draft(doc_id) is not None
    return src, path, (lambda: not drafted and _draft(doc_id) is None and d is not None and os.path.getmtime(path) == mtime)


@contextmanager
def draft(doc_id: str, value: dict | None = None, rows: str | None = None):
    """이 스레드에서 렌더링하는 동안 doc_id 의 템플릿·form.json 을 value({"template"?, "form"?}) 로, 행 수를 rows 로."""
    drafts = getattr(_local, "drafts", None)
    if drafts is None:
        drafts = _local.drafts = {}
    old, old_rows = drafts.get(doc_id), getattr(_local, "rows", None)
    if value is not None:
        drafts[doc_id] = value
    _local.rows = rows
    try:
        yield
    finally:
        if value is not None:
            if old is None:
                drafts.pop(doc_id, None)
            else:
                drafts[doc_id] = old
        _local.rows = old_rows


def _set(data: dict, path: str, v) -> None:
    cur = data
    parts = path.split(".")
    for k in parts[:-1]:
        nxt = cur.get(k)
        if not isinstance(nxt, dict):
            nxt = cur[k] = {}
        cur = nxt
    cur[parts[-1]] = v


def fill(form: dict, p, rng: random.Random, data: dict | None = None) -> dict:
    """form.json 의 fields·lists 로 data 를 채운다 (부모 값 위에)."""
    from . import sources as S

    data = data if data is not None else {}
    values = None
    for key, it in (form.get("fields") or {}).items():
        src = it.get("source") or f"rule:{it.get('type') or 'note'}"
        if values is None and src.startswith("rule:"):
            from .realform import Values

            values = Values(p, rng, it.get("class", "기본"))
        if src.startswith("parent."):
            from .render import lookup

            value = lookup(data, src[len("parent."):])
        elif form.get("shared_copies") and key.endswith("_copy") and key[:-5] in (form.get("fields") or {}):
            from .render import lookup

            value = lookup(data, key[:-5])
        else:
            value = S.value(src, p, rng, {"label": key.split(".")[-1], **it}, values)
        if value is not None and "part" in it:   # 숫자 묶음 중 몇 번째 (모자라면 마지막: '2024년' 한 해만인 기간 등)
            nums = re.findall(r"\d+", str(value))
            value = nums[min(it["part"], len(nums) - 1)] if nums else None
        if value is not None and it.get("format") == "number":
            value = re.sub(r"[^0-9.,+-]", "", str(value))
        if value is not None and it.get("format") == "yy":
            value = str(value)[-2:]
        if value is not None and it.get("format") == "office_prefix":
            value = str(value).removesuffix("세무서장")
        _set(data, key, value)
    mode = getattr(_local, "rows", None)
    for name, L in (form.get("lists") or {}).items():
        lo, hi = int(L.get("min", 1)), int(L.get("max", L.get("min", 1)))
        hi = max(lo, hi)
        n = lo if mode == "min" else hi if mode == "max" else rng.randint(lo, hi)
        rows = []
        for i in range(n):
            row = {}
            for sub, it in (L.get("fields") or {}).items():
                src = it.get("source") or f"rule:{it.get('type') or 'note'}"
                if values is None and src.startswith("rule:"):
                    from .realform import Values

                    values = Values(p, rng, it.get("class", "기본"))
                if src.startswith("rule:") and src[5:] not in S.SPECIAL_RULES:
                    values.cache.pop(src[5:], None)   # 행마다 새 값 (같은 표준 키 캐시를 쓰지 않게)
                row[sub] = S.value(src, p, rng, {"label": sub, **it}, values, row=i)
            rows.append(row)
        _set(data, name, rows)
    return data


def make_generate(doc_id: str):
    def generate(p, rng: random.Random) -> dict:
        from .registry import load_all

        form = load_form(doc_id)
        data = {}
        if form.get("parent"):
            data = load_all()[form["parent"]].generate(p, rng)
            if re.fullmatch(r"hf\d{3}", form["parent"]):
                # 공식 PDF를 HTML로 옮긴 사본: 부모의 빈 칸도 값 선언에 남긴다.
                # items의 value를 직접 쓰는 템플릿에서 null을 누락된 키로 오인하지 않게 한다.
                for item in data.get("items", []):
                    key = item.get("key")
                    if item.get("t") != "mark" and key and key.split(".")[0] not in {"items", "pages", "style", "class", "name", "doc_id", "no", "fonts"}:
                        _set(data, key, item.get("value"))
        return fill(form, p, rng, data)
    generate.__doc__ = f"화면에서 만든 html 서식 {doc_id} (docgen/htmlform.py)"
    return generate


def register_forms() -> int:
    """docgen/forms/<ID>/ 와 DOCGEN_PRIVATE_FORMS 의 html 서식(form.json 이 있는 폴더)을 등록한다 (registry.load_all 이 처음 한 번 부른다).
    이미 등록된 ID 는 건너뛴다."""
    from .registry import GROUPS, REGISTRY, DocSpec

    from . import formdir

    n = 0
    for d in formdir.copy_dirs():
        if d.name not in REGISTRY:
            form = json.loads((d / "form.json").read_text(encoding="utf-8"))
            group = form.get("group") if form.get("group") in GROUPS else "finance"   # 그룹을 안 정했으면 금융거래
            REGISTRY[d.name] = DocSpec(d.name, form.get("name") or d.name, group, form.get("category", "external"),
                                       PREFIX + d.name, make_generate(d.name), form.get("page", "a4"), False,
                                       form.get("description") or f"화면에서 만든 html 서식 ({form.get('origin', 'copy')})",
                                       form.get("origin", "copy"))
            n += 1
    return n


def clone(parent_id: str, new_id: str, name: str, private: bool = False) -> Path:
    """기존 html 서식을 복제한다: 템플릿만 사본, 생성 함수는 부모 것 (키·정답 구조가 같다)."""
    from .registry import load_all

    reg = load_all()
    if parent_id not in reg:
        raise KeyError(parent_id)
    from . import formdir

    if not ID_RX.fullmatch(new_id) or new_id in reg or form_dir(new_id) or formdir.folder(new_id):
        raise ValueError(f"서식 ID 는 영어 소문자·숫자·밑줄 3~51자, 겹치지 않게: {new_id}")
    spec = reg[parent_id]
    if spec.template == "_real_form.html.j2":
        raise ValueError("overlay 서식은 복제하지 않습니다 (html 서식만)")
    made = spec.template.startswith(PREFIX)   # 부모도 화면에서 만든 서식이면 그 form.json 을 이어 받는다
    if private and not formdir.private_roots():
        raise ValueError("private_forms_dir 이 설정되지 않았습니다")
    src = template_source(parent_id) if made else formdir.template(parent_id).read_text(encoding="utf-8")
    d = formdir.new_dir(new_id, formdir.private_roots()[0] if private else None)
    (d / "look" / formdir.TEMPLATE).write_text(src, encoding="utf-8")
    parent_form = load_form(parent_id) if made else {}
    form = {"name": name or f"{spec.name} (복제)", "group": spec.group, "category": spec.category, "page": spec.page,
            "origin": "copy", "parent": parent_form.get("parent") if made else parent_id,
            "fields": parent_form.get("fields", {}), "lists": parent_form.get("lists", {})}
    if made and form["parent"] is None:   # 분석기가 만든 서식의 복제: 값은 form.json 만으로, 원본 이미지도 함께
        form["origin"] = parent_form.get("origin", "copy")
        img = form_dir(parent_id) / "source.png"
        if img.exists():
            shutil.copyfile(img, d / "source.png")
            form["source_image"] = "source.png"
    write_form(d, form)
    register_forms()   # 바로 목록·미리보기에 나오게
    return d


def save(doc_id: str, template: str | None = None, form: dict | None = None) -> Path:
    d = form_dir(doc_id)
    if d is None:
        raise KeyError(doc_id)
    if template is not None:
        _template_path(d).write_text(template, encoding="utf-8")
    if form is not None:
        from . import formfields

        meta = {k: v for k, v in form.items() if k not in formfields.VALUE_KEYS}
        formfields.update(doc_id, form, formfields.VALUE_KEYS)   # 값 선언은 칸 목록에 (처음이면 예전 form.json 것을 먼저 옮긴다)
        (d / "form.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    from .registry import REGISTRY

    spec = REGISTRY.get(doc_id)
    if spec is not None and form is not None:   # 이름·그룹·쪽 크기 바뀐 것을 바로 반영
        from .registry import GROUPS

        spec.name = form.get("name") or spec.name
        spec.group = form.get("group") if form.get("group") in GROUPS else spec.group
        spec.page = form.get("page", spec.page)
        spec.category = form.get("category", spec.category)
    return d


def declared(form: dict) -> dict[str, str]:
    """form.json 이 선언한 키 → 종류 ("field" / "list:<이름>"). 반복 행 하위 키는 "<이름>.0.<하위>" 로 (첫 행 기준)."""
    out = {k: "field" for k in form.get("fields") or {}}
    for name, L in (form.get("lists") or {}).items():
        for sub in L.get("fields") or {}:
            out[f"{name}.0.{sub}"] = f"list:{name}"
    return out


def check(form: dict, raw: list[dict], data: dict, overflow: bool = False) -> list[dict]:
    """저장 전 검사 (경고만): 선언했는데 안 나온 키, 템플릿에 있는데 값이 없는 키(선언·부모에 없음), 쪽 넘침."""
    from .render import lookup

    out = []
    shown = {r["key"] for r in raw}
    for k, kind in declared(form).items():
        if k not in shown:
            out.append({"level": "warn", "text": f"form.json 에 선언했는데 템플릿에 안 나오는 키: {k}" +
                        (" (반복 행 첫 줄 기준)" if kind != "field" else "")})
    for r in raw:
        if r.get("type") in ("seal", "signature") or r.get("value") is not None:
            continue
        try:
            lookup(data, r["key"])
        except (KeyError, IndexError, AttributeError, ValueError, TypeError):
            out.append({"level": "warn", "text": f"템플릿에 있는데 값이 없는 키 (form.json·부모에 없음): {r['key']}"})
    if overflow:
        out.append({"level": "warn", "text": "쪽 넘침: 한 쪽 서식(카드·여권 등) 밖으로 내용이 나갑니다"})
    return out
