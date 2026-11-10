"""① 서식의 서버 쪽: 서식 목록과 서식 정보 (목록 화면·상세 화면), 검수·배정·문제 표시. API 는 studio/app.py, 화면은 static/js/forms.js.

- 서식: docgen 레지스트리 (`docgen.registry.load_all`)
- 서식별 키 목록: guide/fields/fields.json (`docgen/scripts/build_schema.py`가 서식마다 30번 렌더링해 모은 것)
- 검수·배정·메모·문제 표시: docgen/catalog.json (없으면 모두 미검수·미배정)

docgen/catalog.json
  {"hf169": {"reviewed": {"by": "suhyun", "at": "2026-10-21", "hash": "<서식 전용 파일 해시>"},
             "split": "train" | "test_only" | "unassigned", "note": "…",
             "issues": [{"id": "i3", "seed": 0, "page": 0, "bbox": [x0, y0, x1, y1], "key": "…", "note": "…",
                         "status": "open" | "done", "at": "…"}]}}
- 검수 완료는 사람이 누른다. 누른 뒤 그 서식 전용 파일(템플릿·생성 함수·레이아웃·수정 파일)이 바뀌면 "재검수 필요".
- split 은 docgen.bench build 가 읽는다: 학습 데이터(--split train)에서 test_only 서식을 뺀다.
"""
from __future__ import annotations

import inspect
import json
import re
import threading
import time
from functools import lru_cache
from pathlib import Path

from docgen.registry import GROUPS, load_all

from .config import ROOT

FIELDS_JSON = ROOT / "guide" / "fields" / "fields.json"
CATALOG_JSON = ROOT / "docgen" / "catalog.json"
MARK_TYPES = {"checkbox", "checkbox_multi", "seal", "signature"}
AUDIT_JSON = ROOT / "docgen" / "manual" / "form_value_audit.json"
_ASCII_KEY = re.compile(r"^[A-Za-z0-9_.]+$")


def kind_of(group: str, doc_id: str = "") -> tuple[str, str]:
    """(종류, origin). hf### 는 하나은행 원본 PDF 배경, 그 밖의 overlay 는 이미지 배경 (docgen/forms/img_*).
    화면에서 만든 html 서식(템플릿 "@form/<ID>")은 그룹과 상관없이 html (origin copy·analyzer)."""
    spec = load_all().get(doc_id)
    if spec is not None and spec.template.startswith("@form/"):
        return ("html", getattr(spec, "origin", None) or "copy")
    if group in ("hana", "imported"):
        return ("overlay", "pdf") if re.fullmatch(r"hf\d{3}", doc_id or "hf000") else ("overlay", "image")
    origin = getattr(spec, "origin", None) or "builtin"
    return ("html", origin)


@lru_cache(maxsize=1)
def _fields() -> dict:
    return json.loads(FIELDS_JSON.read_text(encoding="utf-8")) if FIELDS_JSON.exists() else {}


@lru_cache(maxsize=2)
def _audit_at(mtime: int) -> dict:
    if not AUDIT_JSON.exists():
        return {}
    return {r["id"]: r for r in json.loads(AUDIT_JSON.read_text(encoding="utf-8"))["forms"]}


def value_audit(doc_id: str) -> dict | None:
    row = _audit_at(AUDIT_JSON.stat().st_mtime_ns if AUDIT_JSON.exists() else 0).get(doc_id)
    if row is None:
        return None
    from docgen.preview import source_hash

    return {**row, "stale": row.get("source_hash") != source_hash(doc_id)}


def _keys(doc_id: str) -> list[dict]:
    keys = list(_fields().get(doc_id, {}).get("keys", []))
    from docgen import regions

    if load_all()[doc_id].template != "_real_form.html.j2" and regions.exists(doc_id):
        from docgen.entities import make_profile
        from docgen.render import render
        from docgen.schema import build_fields

        _, raw, _ = render(load_all()[doc_id], make_profile(0), 0)
        live = {f["key"]: {**f, "example": f.get("value")} for f in build_fields(raw)}
        live = {**{f["key"]: f for f in keys}, **live}
        keys = list(live.values())
    return keys


_LOCK = threading.Lock()
SPLITS = ("unassigned", "train", "test_only")


def _catalog() -> dict:
    return json.loads(CATALOG_JSON.read_text(encoding="utf-8")) if CATALOG_JSON.exists() else {}


def _write(cat: dict) -> None:
    cat = {k: v for k, v in sorted(cat.items()) if v}
    CATALOG_JSON.write_text(json.dumps(cat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def update(doc_id: str, fn) -> dict:
    """catalog.json 의 서식 하나를 fn(entry) 로 고쳐 저장하고 고친 entry 를 돌려준다."""
    if doc_id not in load_all():
        raise KeyError(doc_id)
    with _LOCK:
        cat = _catalog()
        entry = cat.get(doc_id, {})
        fn(entry)
        cat[doc_id] = {k: v for k, v in entry.items() if v not in (None, "", [])}
        _write(cat)
        return cat[doc_id]


def form_hash(doc_id: str) -> str:
    from docgen.preview import source_hash

    return source_hash(doc_id, common=False)


def set_review(doc_id: str, done: bool, by: str = "") -> dict:
    def fn(e):
        e["reviewed"] = {"by": by or "studio", "at": time.strftime("%Y-%m-%d %H:%M"), "hash": form_hash(doc_id)} if done else None
    return update(doc_id, fn)


def set_meta(doc_id: str, split: str | None = None, note: str | None = None) -> dict:
    if split is not None and split not in SPLITS:
        raise ValueError(f"split 은 {SPLITS} 중 하나")

    def fn(e):
        if split is not None:
            e["split"] = None if split == "unassigned" else split
        if note is not None:
            e["note"] = note
    return update(doc_id, fn)


def add_issue(doc_id: str, issue: dict) -> dict:
    def fn(e):
        lst = e.setdefault("issues", [])
        n = max([int(x["id"][1:]) for x in lst if x.get("id", "").startswith("i")] + [0]) + 1
        lst.append({"id": f"i{n}", "status": "open", "at": time.strftime("%Y-%m-%d %H:%M"),
                    **{k: issue[k] for k in ("seed", "page", "bbox", "key", "note", "heavy", "special", "condition")
                       if k in issue}})
    return update(doc_id, fn)


def set_issue(doc_id: str, issue_id: str, status: str | None = None, note: str | None = None,
              delete: bool = False) -> dict:
    def fn(e):
        lst = e.get("issues", [])
        if delete:
            e["issues"] = [x for x in lst if x["id"] != issue_id]
            return
        for x in lst:
            if x["id"] == issue_id:
                if status:
                    x["status"] = status
                if note is not None:
                    x["note"] = note
    return update(doc_id, fn)


def review_state(doc_id: str, entry: dict) -> str:
    """none / done / stale (검수 뒤 서식 파일이 바뀜)."""
    rv = entry.get("reviewed")
    if not rv:
        return "none"
    return "stale" if rv.get("hash") and rv["hash"] != form_hash(doc_id) else "done"


def _tables(doc_id: str, text: list[dict]) -> list[str]:
    """표(반복 묶음) 이름. 표 과제와 같은 규칙 (docgen.bench.tasks.Doc._scan_tables): 겹친 목록·도장·서명 칸, questions.json 에서 ask false 인 묶음은 뺌."""
    from docgen import formquestions as FQ
    from docgen.bench.tasks import table_cell

    cfg = (FQ.read(doc_id) or {}).get("table") or {}
    out = []
    for k in text:
        if k["key"].startswith(("seal.", "sign.")):
            continue
        tc = table_cell(k["key"].replace("[]", ".0"))
        if tc and tc[1] >= 0 and tc[0] not in out and (cfg.get(tc[0]) or {}).get("ask") is not False:
            out.append(tc[0])
    return out


def _key_stats(doc_id: str, keys: list[dict]) -> dict:
    text = [k for k in keys if k.get("type") not in MARK_TYPES]
    return {
        "n_keys": len(keys),
        "n_marks": len(keys) - len(text),
        "n_korean_keys": sum(1 for k in keys if not _ASCII_KEY.match(k["key"].replace("[]", ""))),
        "n_empty": sum(1 for k in text if not k.get("example")),
        "tables": _tables(doc_id, text),
    }


def _edited(doc_id: str) -> bool:
    from docgen import formfields, regions

    if regions.engine(doc_id) == "overlay" and formfields.exists(doc_id):
        f = formfields.read(doc_id)
        return bool(f.get("erase") or f.get("marks") or f.get("dropped") or any(it.get("edited") or it.get("added") for it in f["items"]))
    if not load_all()[doc_id].template.startswith("@") and formfields.exists(doc_id):   # 코드 서식에 적은 값 선언
        from docgen.htmlform import own

        if own(formfields.read(doc_id) or {}):   # "code"(생성 함수 값 그대로)가 아닌 값 선언
            return True
    return regions.exists(doc_id)


def _summary(spec, entry: dict, audit: bool = False) -> dict:
    """서식 한 줄. audit: 이미지 값 점검(상세 화면만 씀, 서식마다 원본 해시를 계산해 느리다)."""
    kind, origin = kind_of(spec.group, spec.id)
    official_source, script = None, False
    if spec.template.startswith("@form/"):
        from docgen.htmlform import load_form, script_path

        script = script_path(spec.id) is not None
        source = load_form(spec.id).get("source") or {}
        if isinstance(source, dict) and str(source.get("url", "")).startswith("https://") and source.get("online_verification", {}).get("matches_local"):
            official_source = source
    keys = _keys(spec.id)
    issues = entry.get("issues", [])
    return {
        "id": spec.id, "name": spec.name, "group": spec.group, "group_name": GROUPS.get(spec.group, spec.group),
        "kind": kind, "origin": origin, "category": spec.category, "page": spec.page,
        "official_source": official_source, "script": script,
        **({"value_audit": value_audit(spec.id)} if audit else {}),
        "reviewed": entry.get("reviewed"), "split": entry.get("split", "unassigned"),
        "open_issues": sum(1 for x in issues if x.get("status") == "open"),
        "edited": _edited(spec.id),
        **_key_stats(spec.id, keys),
    }


def clear_caches() -> None:
    """이 모듈의 캐시를 비운다 (키 목록 guide/fields/fields.json, 값 점검)."""
    _fields.cache_clear()
    _audit_at.cache_clear()


def refresh() -> dict:
    """서식 폴더를 다시 훑고 (docgen.registry.refresh) 서식 목록에 딸린 저장값을 비운다."""
    from docgen.registry import refresh as rescan

    clear_caches()
    res = rescan()
    from docgen import formcard

    res["stale_cards"] = sorted(i for i in load_all() if formcard.stale(i))   # 서식 카드 FORM.md 가 없거나 오래됨
    return res


def card(doc_id: str) -> dict:
    """서식 카드 FORM.md (docgen/formcard.py): 내용, 오래됐는지."""
    from docgen import formcard

    if doc_id not in load_all():
        raise KeyError(doc_id)
    p = formcard.path(doc_id)
    return {"path": _rel(p), "markdown": p.read_text(encoding="utf-8") if p.exists() else None, "stale": formcard.stale(doc_id)}


def overview(doc_id: str) -> dict:
    """개요 탭: 이 서식이 만드는 과제마다 무엇을 묻는지 + 질문 검사. 카드(docgen/formcard.py)와 같은 함수로 센다
    (고객 16명으로 그려 본 칸, formquestions.resolved). 표 칸은 kie 가 아니라 표 과제가 묻는다 (table_cell)."""
    from docgen import formcard, fieldinfo, formqa
    from docgen import formquestions as FQ
    from docgen.bench.tasks import table_cell

    if doc_id not in load_all():
        raise KeyError(doc_id)
    docs = FQ.seen_fields(doc_id)
    view = FQ.resolved(doc_id, docs)
    tcfg = (FQ.read(doc_id) or {}).get("table") or {}
    kie, nested, tables = [], [], {}
    for it in view["kie"]["items"]:
        tc = table_cell(it["key"].replace("*", "0"))
        if tc and tc[1] < 0:
            nested.append(it)
        elif tc and (tcfg.get(tc[0]) or {}).get("ask") is not False:
            t = tables.setdefault(tc[0], {"group": tc[0], "title": (tcfg.get(tc[0]) or {}).get("title"), "columns": [], "seen": 0})
            t["columns"].append({**it, "column": tc[2]})
            t["seen"] = max(t["seen"], it["seen"])
        else:
            kie.append(it)
    check = FQ.check(doc_id, docs=docs)
    return {
        "docs": len(docs),
        "classify": view["classify"],
        "kie": kie, "nested": nested, "tables": list(tables.values()),
        "marks": view["marks"]["items"],
        "ocr_exclude": view["ocr_page"]["exclude"],
        "ocr_off": sorted(k for k, it in fieldinfo.questions(doc_id).items() if it.get("ocr") is False),
        "form_qa": formqa.check(doc_id, docs)["rows"],
        "changed": {t: view[t]["changed"] for t in ("kie", "marks", "classify", "ocr_page", "ocr_field")},
        "problems": check["problems"], "notes": check["notes"],
        "card_stale": formcard.stale(doc_id), "card_exists": formcard.path(doc_id).exists(),
    }


def make_card(doc_id: str) -> dict:
    """카드를 다시 만든다 (그림을 그려 위치를 잰다 — 명령줄과 같은 python -m docgen.formdir card <ID>)."""
    import subprocess
    import sys

    if doc_id not in load_all():
        raise KeyError(doc_id)
    r = subprocess.run([sys.executable, "-m", "docgen.formdir", "card", doc_id], cwd=Path(__file__).resolve().parents[1],
                       capture_output=True, text=True, timeout=600)
    if r.returncode:
        raise ValueError(f"카드를 만들지 못했습니다: {(r.stderr or r.stdout).strip().splitlines()[-1:]}")
    return card(doc_id)


def list_forms() -> list[dict]:
    cat = _catalog()
    return [_summary(spec, cat.get(spec.id, {})) for spec in load_all().values()]


def _rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


def form_detail(doc_id: str) -> dict:
    reg = load_all()
    if doc_id not in reg:
        raise KeyError(doc_id)
    spec = reg[doc_id]
    entry = _catalog().get(doc_id, {})
    from docgen import formdir

    files = []
    for role, f in formdir.describe(doc_id):
        if role == "사람 수정":
            continue
        files.append({"role": role, "path": (_rel(f) + ("" if f.exists() else " (아직 없음)")) if f else "-"})
    if spec.template.startswith("@form/"):
        from docgen import htmlform

        form = htmlform.load_form(doc_id) if htmlform.form_dir(doc_id) else {}
        if form.get("parent") in load_all():
            parent = load_all()[form["parent"]]
            files.append({"role": f"생성 함수 (부모 서식 {parent.id})", "path": _rel(Path(inspect.getsourcefile(parent.generate)))})
    elif spec.group in ("hana", "imported"):
        files.append({"role": "값 채우기·렌더링", "path": "docgen/realform.py"})
    from docgen import formfields, regions

    op = formfields.path(doc_id)
    if not any(f["path"].startswith(_rel(op)) for f in files):   # formdir.describe 에 이미 있으면 한 번만
        files.append({"role": "칸 목록 (사람이 고치는 곳)", "path": _rel(op) + ("" if op.exists() else " (아직 없음)")})
    for f in [regions.path(doc_id), *regions.legacy(doc_id).values()]:
        if f.exists():
            files.append({"role": "예전 수정 파일",
                          "path": _rel(f) + (" (칸 목록이 있어 안 읽음 — python -m docgen.regions check)" if op.exists()
                                             else " (python -m docgen.formdir migrate 로 옮기세요)")})
    return {
        **_summary(spec, entry, audit=True),
        "description": spec.description,
        "sample_mark": spec.sample_mark,
        "note": entry.get("note", ""),
        "issues": entry.get("issues", []),
        "review_state": review_state(doc_id, entry),
        "keys": _keys(doc_id),
        "files": files,
        "script": _script_source(doc_id) if spec.template.startswith("@form/") else None,
        "questions": _questions_source(doc_id),
        "qa": _qa_source(doc_id),
    }


def _script_source(doc_id: str) -> dict | None:
    """생성 스크립트(generate.py) 내용 (파일 탭에서 읽고 확인)."""
    from docgen.htmlform import script_path

    p = script_path(doc_id)
    return {"path": _rel(p), "source": p.read_text(encoding="utf-8")[:200_000]} if p else None


def _questions_source(doc_id: str) -> dict | None:
    """이 서식의 질문·답 파일(questions.json) 내용 (질문·답 › 실제 문항에서 보고, 고치는 것은 파일로)."""
    from docgen import formquestions

    p = formquestions.path(doc_id)
    return {"path": _rel(p), "source": p.read_text(encoding="utf-8")[:200_000]} if p.exists() else None


def _qa_source(doc_id: str) -> dict | None:
    """이 서식만의 질문 qa.py 내용 (질문·답 › 실제 문항에서 보고, 고치는 것은 파일로)."""
    from docgen import formqa

    p = formqa.path(doc_id)
    return {"path": _rel(p), "source": p.read_text(encoding="utf-8")[:200_000]} if p.exists() else None
