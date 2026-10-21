"""키 사전 풀이 (studio/DESIGN.md 16절). 파일은 docgen/dictionary/*.json (자동 초안: docgen/scripts/build_dictionary.py).

  resolve("remitter.name", task="fx_remittance") → {party: "customer", role: "remitter", attribute: "name", sub: [],
                                                    canonical: "remitter.name", party_key: "customer.name"}
  party_key 는 서식이 달라도 같은 값을 가리키는 키 (시나리오 대조·추출이 쓸 키). 합치기는 결정(accepted)된 것만 따라간다.
  doc_type_of("hana_official_049") → 문서 종류 ID, task_of("주담대") → 업무 ID, find_doc_type("Commercial Invoice") → 문서 종류 ID

생성 코드는 아직 이 모듈을 쓰지 않는다 (DESIGN 16.5 K3).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

DIR = Path(__file__).with_name("dictionary")
FILES = ("parties", "roles", "attributes", "doc_types", "tasks", "options", "merges")
_cache: dict = {}


def load(name: str) -> dict:
    p = DIR / f"{name}.json"
    m = p.stat().st_mtime if p.exists() else 0.0
    if _cache.get(name, (None,))[0] != m:
        _cache[name] = (m, json.loads(p.read_text(encoding="utf-8")) if p.exists() else {})
    return _cache[name][1]


def save(name: str, obj: dict) -> None:
    p = DIR / f"{name}.json"
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tmp.replace(p)
    _cache.pop(name, None)


def _norm(s: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]", "", (s or "").lower())


def merged(dict_: str, name: str) -> str:
    """결정된 합치기를 따라간 이름 (A→B→C)."""
    seen = set()
    into = {m["from"]: m["into"] for m in load("merges").get("items", []) if m["dict"] == dict_ and m["status"] == "accepted"}
    while name in into and name not in seen:
        seen.add(name)
        name = into[name]
    return name


def split(key: str) -> tuple[str | None, list[str], str]:
    parts = key.split(".")
    if parts[0] in ("seal", "sign") and len(parts) >= 2:
        return ("staff" if parts[1] == "staff" else ".".join(parts[1:])), [], parts[0]
    if len(parts) == 1:
        return None, [], parts[0]
    return parts[0], parts[1:-1], parts[-1]


def role_party(role: str | None, doc_type: str | None = None, task: str | None = None) -> str:
    """서류 속 역할 → 당사자. 업무 > 문서 종류 > 역할 기본값 순."""
    if role is None:
        return "document"
    role = merged("role", role)
    t = load("tasks").get("tasks", {}).get(task or "", {})
    if role in t.get("roles", {}):
        return t["roles"][role]
    r = load("roles").get("roles", {}).get(role, {})
    if doc_type and doc_type in r.get("by_doc_type", {}):
        return r["by_doc_type"][doc_type]
    if task and task in r.get("by_task", {}):
        return r["by_task"][task]
    return r.get("party", "unassigned")


def resolve(key: str, doc_type: str | None = None, task: str | None = None) -> dict:
    canonical = merged("field", key)
    role, sub, attr = split(canonical)
    attr = merged("attribute", attr)
    party = role_party(role, doc_type, task)
    a = load("attributes").get("attributes", {}).get(attr, {})
    mark = attr in ("seal", "sign")
    return {"key": key, "canonical": canonical, "party": party, "role": role, "sub": sub, "attribute": attr,
            "kind": a.get("kind"), "mark": mark,
            "party_key": ".".join(([f"{attr}"] if mark else []) + [party] + sub + ([] if mark else [attr]))}


def doc_type_of(form_id: str) -> str | None:
    for tid, t in load("doc_types").get("types", {}).items():
        if form_id in t.get("forms", []):
            return merged("doc_type", tid)
    return None


def find_doc_type(name: str) -> str | None:
    """이름·다른 이름으로 문서 종류 찾기 (분류 문항 채점·서류 넣기)."""
    n = _norm(name)
    for tid, t in load("doc_types").get("types", {}).items():
        if n and n in {_norm(x) for x in [tid, t["name"], *t.get("aliases", [])]}:
            return merged("doc_type", tid)
    return None


def task_of(name: str) -> str | None:
    n = _norm(name)
    for tid, t in load("tasks").get("tasks", {}).items():
        if n and n in {_norm(x) for x in [tid, t["name"], *t.get("aliases", [])]}:
            return merged("task", tid)
    return None
