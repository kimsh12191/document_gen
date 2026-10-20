"""서식 목록과 서식 정보 (목록 화면·상세 화면).

- 서식: docgen 레지스트리 (`docgen.registry.load_all`)
- 서식별 키 목록: guide/fields/fields.json (`scripts/build_schema.py`가 서식마다 30번 렌더링해 모은 것)
- 검수·배정: docgen/catalog.json (없으면 모두 미검수·미배정)
"""
from __future__ import annotations

import inspect
import json
import re
from functools import lru_cache
from pathlib import Path

from docgen.registry import GROUPS, SCENARIOS, load_all

from .config import ROOT

FIELDS_JSON = ROOT / "guide" / "fields" / "fields.json"
CATALOG_JSON = ROOT / "docgen" / "catalog.json"
MARK_TYPES = {"checkbox", "checkbox_multi", "seal", "signature"}
_ASCII_KEY = re.compile(r"^[A-Za-z0-9_.]+$")


def kind_of(group: str) -> tuple[str, str]:
    """(종류, origin). 지금은 하나은행 원본 서식만 overlay 다."""
    return ("overlay", "pdf") if group == "hana" else ("html", "builtin")


@lru_cache(maxsize=1)
def _fields() -> dict:
    return json.loads(FIELDS_JSON.read_text(encoding="utf-8")) if FIELDS_JSON.exists() else {}


def _catalog() -> dict:
    return json.loads(CATALOG_JSON.read_text(encoding="utf-8")) if CATALOG_JSON.exists() else {}


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


def _summary(spec, entry: dict) -> dict:
    kind, origin = kind_of(spec.group)
    keys = _fields().get(spec.id, {}).get("keys", [])
    return {
        "id": spec.id, "name": spec.name, "group": spec.group, "group_name": GROUPS.get(spec.group, spec.group),
        "kind": kind, "origin": origin, "category": spec.category, "page": spec.page,
        "scenarios": [s["id"] for s in _scenarios_of().get(spec.id, [])],
        "reviewed": entry.get("reviewed"), "split": entry.get("split", "unassigned"),
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
    reg = load_all()
    if doc_id not in reg:
        raise KeyError(doc_id)
    spec = reg[doc_id]
    entry = _catalog().get(doc_id, {})
    files = []
    if spec.group == "hana":
        from docgen.realform import layout_path, load_layout

        lp = layout_path(int(doc_id[2:]))
        if lp:
            lay = load_layout(int(doc_id[2:]))
            files.append({"role": "레이아웃 (자동 추출)", "path": _rel(lp)})
            files.append({"role": "원본 PDF", "path": lay.get("file", "")})
        files.append({"role": "값 채우기·렌더링", "path": "docgen/realform.py"})
    else:
        files.append({"role": "템플릿", "path": f"templates/{spec.template}"})
        files.append({"role": "생성 함수", "path": _rel(Path(inspect.getsourcefile(spec.generate)))})
    return {
        **_summary(spec, entry),
        "description": spec.description,
        "sample_mark": spec.sample_mark,
        "scenario_names": _scenarios_of().get(doc_id, []),
        "note": entry.get("note", ""),
        "keys": _fields().get(doc_id, {}).get("keys", []),
        "files": files,
    }


def groups() -> list[dict]:
    return [{"id": g, "name": n} for g, n in GROUPS.items()]
