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

from docgen.registry import GROUPS, SCENARIOS, load_all

from .config import ROOT

FIELDS_JSON = ROOT / "guide" / "fields" / "fields.json"
CATALOG_JSON = ROOT / "docgen" / "catalog.json"
MARK_TYPES = {"checkbox", "checkbox_multi", "seal", "signature"}
AUDIT_JSON = ROOT / "docgen" / "manual" / "form_value_audit.json"
_ASCII_KEY = re.compile(r"^[A-Za-z0-9_.]+$")


def kind_of(group: str, doc_id: str = "") -> tuple[str, str]:
    """(종류, origin). hf### 는 하나은행 원본 PDF 배경, 그 밖의 overlay 는 이미지 배경 (docgen/forms/images).
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
    from docgen import html_regions

    if load_all()[doc_id].template != "_real_form.html.j2" and html_regions.path(doc_id).exists():
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


@lru_cache(maxsize=1)
def _scenarios_of() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for sid, (name, docs) in SCENARIOS.items():
        for d in docs:
            out.setdefault(d, []).append({"id": sid, "name": name})
    return out


def _key_stats(keys: list[dict]) -> dict:
    text = [k for k in keys if k.get("type") not in MARK_TYPES]
    return {
        "n_keys": len(keys),
        "n_marks": len(keys) - len(text),
        "n_korean_keys": sum(1 for k in keys if not _ASCII_KEY.match(k["key"].replace("[]", ""))),
        "n_empty": sum(1 for k in text if not k.get("example")),
    }


def _edited(doc_id: str) -> bool:
    from docgen import overrides

    from docgen import html_regions
    from docgen import template_variants

    return overrides.path(doc_id).exists() or (load_all()[doc_id].template != "_real_form.html.j2" and (html_regions.path(doc_id).exists() or any(template_variants.folder(doc_id).glob("*.regions.json"))))


def _summary(spec, entry: dict) -> dict:
    kind, origin = kind_of(spec.group, spec.id)
    official_source = None
    if spec.template.startswith("@form/"):
        from docgen.htmlform import load_form

        source = load_form(spec.id).get("source") or {}
        if isinstance(source, dict) and str(source.get("url", "")).startswith("https://") and source.get("online_verification", {}).get("matches_local"):
            official_source = source
    keys = _keys(spec.id)
    issues = entry.get("issues", [])
    return {
        "id": spec.id, "name": spec.name, "group": spec.group, "group_name": GROUPS.get(spec.group, spec.group),
        "kind": kind, "origin": origin, "category": spec.category, "page": spec.page,
        "official_source": official_source,
        "value_audit": value_audit(spec.id),
        "scenarios": [s["id"] for s in _scenarios_of().get(spec.id, [])],
        "reviewed": entry.get("reviewed"), "split": entry.get("split", "unassigned"),
        "open_issues": sum(1 for x in issues if x.get("status") == "open"),
        "edited": _edited(spec.id),
        **_key_stats(keys),
    }


def list_forms() -> list[dict]:
    cat = _catalog()
    return [_summary(spec, cat.get(spec.id, {})) for spec in load_all().values()]


def _rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(p)


def form_detail(doc_id: str) -> dict:
    from docgen.roles import index as role_index

    reg = load_all()
    if doc_id not in reg:
        raise KeyError(doc_id)
    spec = reg[doc_id]
    entry = _catalog().get(doc_id, {})
    files = []
    if spec.template.startswith("@form/"):
        from docgen import htmlform

        d = htmlform.form_dir(doc_id)
        form = htmlform.load_form(doc_id) if d else {}
        files.append({"role": "템플릿", "path": _rel(d / "template.html.j2") if d else spec.template})
        files.append({"role": "값 선언 (form.json)", "path": _rel(d / "form.json") if d else "-"})
        if form.get("parent") in load_all():
            parent = load_all()[form["parent"]]
            files.append({"role": f"생성 함수 (부모 서식 {parent.id})", "path": _rel(Path(inspect.getsourcefile(parent.generate)))})
    elif spec.group in ("hana", "imported"):
        from docgen import overrides
        from docgen.realform import form_no, image_form_dir, layout_path, load_layout

        no = form_no(doc_id)
        lp = layout_path(no) if no is not None else None
        if lp:
            lay = load_layout(no)
            files.append({"role": "레이아웃 (자동 추출)", "path": _rel(lp)})
            files.append({"role": "원본 PDF", "path": lay.get("file", "")})
        elif (d := image_form_dir(doc_id)):
            files.append({"role": "레이아웃·배경 이미지", "path": _rel(d)})
        op = overrides.path(doc_id)
        files.append({"role": "사람 수정 (영역 편집기)", "path": _rel(op) + ("" if op.exists() else " (아직 없음)")})
        files.append({"role": "값 채우기·렌더링", "path": "docgen/realform.py"})
    else:
        files.append({"role": "템플릿", "path": f"docgen/templates/{spec.template}"})
        files.append({"role": "생성 함수", "path": _rel(Path(inspect.getsourcefile(spec.generate)))})
    return {
        **_summary(spec, entry),
        "description": spec.description,
        "document_role": role_index().get(doc_id),
        "sample_mark": spec.sample_mark,
        "scenario_names": _scenarios_of().get(doc_id, []),
        "note": entry.get("note", ""),
        "issues": entry.get("issues", []),
        "review_state": review_state(doc_id, entry),
        "keys": _keys(doc_id),
        "files": files,
    }


def groups() -> list[dict]:
    return [{"id": g, "name": n} for g, n in GROUPS.items()]
