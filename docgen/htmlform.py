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
    generate.py                     (있으면) 생성 스크립트: adjust(d, p, rng) 가 칸 목록으로 채운 값을 다듬는다
                                    (칸끼리 순서·합계·조건·표기). 도우미 docgen/formkit.py, 연결점 run_script

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
CODE = "code"   # 값 출처 "code": 코드 서식의 생성 함수(docgen/docs/*.py)가 만든 값 그대로
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
    if f and own(f):
        return fill(f, p, rng, data)
    return data


def own(f: dict) -> bool:
    """칸 목록에 생성 함수 값이 아닌 값 선언이 있나 ("code" 만 적힌 칸 목록은 결과를 바꾸지 않는다)."""
    return any(it.get("source") != CODE for it in (f.get("fields") or {}).values()) or \
        any(L.get("source") != CODE or any(it.get("source") != CODE for it in (L.get("fields") or {}).values())
            for L in (f.get("lists") or {}).values())


def declare(doc_id: str, seeds: int = 24) -> dict:
    """코드 서식의 칸을 칸 목록 꼴로: 여러 seed 로 그려 나온 키마다 {"label", "type", "source": "code"}.
    반복 행(키에 번호)은 lists 로 모은다. {"fields": {...}, "lists": {...}}."""
    from collections import Counter

    from .entities import make_profile
    from .registry import load_all
    from .render import render

    spec = load_all()[doc_id]
    seen: dict[str, Counter] = {}
    types: dict[str, str] = {}
    for seed in range(seeds):
        _, raw, _ = render(spec, make_profile(seed), seed)
        for r in raw:
            k = re.sub(r"\.\d+(?=\.|$)", ".#", r["key"])
            seen.setdefault(k, Counter())[r.get("label") or ""] += 1
            types.setdefault(k, r.get("type") or "text")
    fields, lists = {}, {}
    for k in sorted(seen):
        label = seen[k].most_common(1)[0][0]
        entry = {**({"label": label} if label else {}), "type": types[k], "source": CODE}
        if ".#." in k or k.endswith(".#"):
            name, _, sub = k.partition(".#.")
            L = lists.setdefault(name, {"source": CODE, "fields": {}})
            L["fields"][sub or "#"] = entry
        else:
            fields[k] = entry
    return {"fields": fields, "lists": lists}


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
        if it.get("source") == CODE:   # 코드 서식의 생성 함수 값 그대로
            continue
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
        if L.get("source") == CODE:   # 행은 생성 함수 것 그대로, 값 출처를 바꾼 하위 칸만 행마다 덮어쓴다
            from .render import lookup

            try:
                rows = lookup(data, name)
            except (KeyError, IndexError, AttributeError, TypeError, ValueError):
                rows = None
            for sub, it in (L.get("fields") or {}).items():
                if it.get("source") == CODE or not isinstance(rows, list) or "#" in sub:
                    continue
                src = it.get("source")
                if values is None and src.startswith("rule:"):
                    from .realform import Values

                    values = Values(p, rng, it.get("class", "기본"))
                for i, row in enumerate(rows):
                    if isinstance(row, dict):
                        if src.startswith("rule:") and src[5:] not in S.SPECIAL_RULES:
                            values.cache.pop(src[5:], None)
                        _set(row, sub, S.value(src, p, rng, {"label": sub.split(".")[-1], **it}, values, row=i))
            continue
        lo, hi = int(L.get("min", 1)), int(L.get("max", L.get("min", 1)))
        hi = max(lo, hi)
        n = lo if mode == "min" else hi if mode == "max" else rng.randint(lo, hi)
        rows = []
        for i in range(n):
            row = {}
            for sub, it in (L.get("fields") or {}).items():
                if it.get("source") == CODE:
                    continue
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
                cont = [c for t in data.get("extra_rows") or [] for r in t["rows"] for c in r["cells"]]   # 별지에 이어 적은 표 행
                for item in [*data.get("items", []), *cont]:
                    key = item.get("key")
                    if item.get("t") != "mark" and key and key.split(".")[0] not in {"items", "pages", "style", "class", "name", "doc_id", "no", "fonts", "extra_rows"}:
                        _set(data, key, item.get("value"))
        return run_script(doc_id, fill(form, p, rng, data), p, rng)
    generate.__doc__ = f"화면에서 만든 html 서식 {doc_id} (docgen/htmlform.py)"
    return generate


# ---------------------------------------------------------------------------
# 생성 스크립트 (서식 폴더의 generate.py): 칸 목록이 값을 채운 뒤 칸끼리 관계를 맞춘다
# ---------------------------------------------------------------------------
SCRIPT = "generate.py"
_SCRIPTS: dict = {}   # (경로, 수정 시각) → {"fn", "checked", "warn"}


def script_path(doc_id: str) -> Path | None:
    """이 서식의 생성 스크립트. 초안(preview --dir)이면 초안 폴더의 것, 아니면 서식 폴더의 generate.py. 없으면 None."""
    dr = _draft(doc_id)
    if dr and "script" in dr:
        return Path(dr["script"]) if dr["script"] else None
    d = form_dir(doc_id)
    p = d / SCRIPT if d else None
    return p if p is not None and p.exists() else None


def _where(path: Path, e: BaseException) -> str:
    import traceback

    line = e.lineno if isinstance(e, SyntaxError) else next(
        (f.lineno for f in reversed(traceback.extract_tb(e.__traceback__)) if Path(f.filename) == path), None)
    return f"생성 스크립트 {path.name}{f' {line}번째 줄' if line else ''}: {type(e).__name__}: {e}"


def _load_script(path: Path) -> dict:
    import importlib.util

    key = (str(path), path.stat().st_mtime_ns)
    if key not in _SCRIPTS:
        spec = importlib.util.spec_from_file_location(f"docgen_form_script_{abs(hash(key))}", path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:  # noqa: BLE001  스크립트 오류는 그 서식만 (어느 줄인지와 함께)
            raise ValueError(_where(path, e)) from e
        fn = getattr(mod, "adjust", None)
        if not callable(fn):
            raise ValueError(f"생성 스크립트 {path.name} 에 adjust(d, p, rng) 함수가 없습니다")
        _SCRIPTS[key] = {"fn": fn, "checked": False, "warn": []}
    return _SCRIPTS[key]


def _paths(v, prefix: str = "") -> set[str]:
    """값 dict 의 끝 칸 경로 (반복 행 번호는 #). 밑줄로 시작하는 칸(_template_variant 등)은 뺀다."""
    out = set()
    if isinstance(v, dict):
        for k, x in v.items():
            if not str(k).startswith("_"):
                out |= _paths(x, f"{prefix}{k}.")
    elif isinstance(v, list) and v and all(isinstance(x, dict) for x in v):
        for x in v:
            out |= _paths(x, f"{prefix}#.")
    else:
        out.add(prefix[:-1])
    return out


def run_script(doc_id: str, data: dict, p, rng: random.Random, path: Path | None = None) -> dict:
    """생성 스크립트가 있으면 adjust(d, p, rng) 를 불러 값을 다듬는다. 없으면 data 그대로.
    약속: 난수는 rng 만, 파일·네트워크·시간을 읽지 않는다, 키는 칸 목록이 정한 것만 고친다 (새 키는 검사 경고).
    스크립트마다 처음 한 번은 같은 입력·같은 난수로 한 번 더 돌려 결과가 같은지 본다 (다르면 검사 경고)."""
    path = path or script_path(doc_id)   # overlay 서식은 realform 이 서식 폴더의 generate.py 를 넘긴다
    if path is None:
        return data
    import copy

    s = _load_script(path)
    before = _paths(data)
    first = None
    if not s["checked"]:
        try:
            first, state = copy.deepcopy(data), rng.getstate()
        except Exception:  # noqa: BLE001  복사할 수 없는 값이면 재현성 검사를 건너뛴다
            first = None
    try:
        out = s["fn"](data, p, rng)
    except Exception as e:  # noqa: BLE001
        raise ValueError(_where(path, e)) from e
    out = data if out is None else out
    if not isinstance(out, dict):
        raise ValueError(f"생성 스크립트 {path.name}: adjust 는 값 dict 를 돌려줘야 합니다 ({type(out).__name__})")
    if not s["checked"]:
        s["checked"] = True
        if first is not None:
            r2 = random.Random()
            r2.setstate(state)
            try:
                again = s["fn"](first, p, r2)
                again = first if again is None else again
                same = json.dumps(again, sort_keys=True, default=str) == json.dumps(out, sort_keys=True, default=str)
            except Exception:  # noqa: BLE001
                same = False
            if not same:
                s["warn"].append(f"생성 스크립트 {path.name}: 같은 seed 로 두 번 돌렸는데 결과가 다릅니다 "
                                 "(난수는 넘겨받은 rng 만 쓰고, 시간·파일·전역 상태를 읽지 않습니다)")
    new = sorted(_paths(out) - before)
    infos = getattr(_local, "scripts", None)
    if infos is None:
        infos = _local.scripts = {}
    infos[doc_id] = {"file": str(path), "warn": list(s["warn"]) +
                     ([f"생성 스크립트 {path.name} 가 칸 목록에 없는 키를 만들었습니다: {', '.join(new[:10])} "
                       "(정답 키는 칸 목록·템플릿이 정합니다. 칸 목록에 선언하세요)"] if new else [])}
    return out


def script_warnings(doc_id: str) -> list[str]:
    """이 스레드에서 마지막으로 그린 doc_id 의 생성 스크립트 검사 경고."""
    return ((getattr(_local, "scripts", None) or {}).get(doc_id) or {}).get("warn", [])


def register_forms() -> int:
    """docgen/forms/<ID>/ 와 DOCGEN_PRIVATE_FORMS 의 html 서식(form.json 이 있는 폴더)을 등록한다 (registry.load_all 이 처음 한 번 부른다).
    이미 등록된 ID 는 건너뛴다."""
    from .registry import GROUPS, REGISTRY, DocSpec

    from . import formdir

    n = 0
    for d in formdir.copy_dirs():
        if d.name not in REGISTRY:
            REGISTRY[d.name] = spec_of(d)
            n += 1
    return n


def spec_of(d: Path):
    """서식 폴더 → 등록 정보 (form.json 의 이름·그룹·종류·쪽·설명·출처)."""
    from .registry import GROUPS, DocSpec

    form = json.loads((d / "form.json").read_text(encoding="utf-8"))
    group = form.get("group") if form.get("group") in GROUPS else "finance"   # 그룹을 안 정했으면 금융거래
    return DocSpec(d.name, form.get("name") or d.name, group, form.get("category", "external"),
                   PREFIX + d.name, make_generate(d.name), form.get("page", "a4"), False,
                   form.get("description") or f"화면에서 만든 html 서식 ({form.get('origin', 'copy')})",
                   form.get("origin", "copy"))


def check_dir(d: Path) -> str | None:
    """서식 폴더를 등록해도 되는지: form.json·칸 목록을 읽을 수 있고 템플릿 문법이 맞는지, 서식 ID 형식. 문제면 그 이유."""
    from jinja2 import TemplateSyntaxError

    from . import formdir, formfields
    from .render import env

    if not ID_RX.fullmatch(d.name):
        return f"서식 ID 형식이 아닙니다 (영어 소문자로 시작, 소문자·숫자·밑줄 3~51자): {d.name}"
    try:
        form = json.loads((d / "form.json").read_text(encoding="utf-8"))
        if not isinstance(form, dict):
            return "form.json 이 JSON 객체가 아닙니다"
        if (d / formfields.NAME).exists():
            json.loads((d / formfields.NAME).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return f"JSON 을 읽지 못했습니다: {e}"
    tpl = formdir.template_in(d)
    try:
        env().parse(tpl.read_text(encoding="utf-8"))
    except TemplateSyntaxError as e:
        return f"템플릿 문법 오류 ({tpl.name} {e.lineno}번째 줄): {e.message}"
    if (d / SCRIPT).exists():
        try:
            compile((d / SCRIPT).read_text(encoding="utf-8"), str(d / SCRIPT), "exec")
        except SyntaxError as e:
            return f"생성 스크립트 문법 오류 ({SCRIPT} {e.lineno}번째 줄): {e.msg}"
    return None


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


def check(form: dict, raw: list[dict], data: dict, overflow: bool = False, doc_id: str | None = None) -> list[dict]:
    """저장 전 검사 (경고만): 선언했는데 안 나온 키, 템플릿에 있는데 값이 없는 키(선언·부모에 없음), 쪽 넘침,
    (doc_id 를 주면) 생성 스크립트 경고 (재현성, 칸 목록에 없는 새 키)."""
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
    if doc_id:
        out += [{"level": "warn", "text": w} for w in script_warnings(doc_id)]
    return out
