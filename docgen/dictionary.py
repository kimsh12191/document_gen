"""키 사전 풀이 (studio/DESIGN.md 16절). 파일은 docgen/dictionary/*.json (자동 초안: docgen/scripts/build_dictionary.py).

화면·문서에서 쓰는 말은 업무명·문서명·키 셋이다. 키는 범위가 둘:
  공통 키   여러 문서에 나오고 서류끼리 대조·심사하는 값 (common.json, 예: customer.name 고객 성명)
  문서별 키 서식의 키 그대로, 그 문서에서만 의미 (fields.json). 공통 키에 이으면(links.json) 공통 키로 묻고 답한다
  common_key("loan_application", "applicant.name") → "customer.name" (이음만, 제안·끊음은 None)
당사자·역할(parties·roles)은 잇기 제안을 만드는 속 장치다.

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
FILES = ("parties", "roles", "attributes", "doc_types", "tasks", "options", "merges", "relations", "common", "links")
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
    key = re.sub(r"\[\]", ".*", key)   # owners[].name → owners.*.name (반복 행)
    parts = key.split(".")
    if parts[0] in ("seal", "sign") and len(parts) >= 2:
        return ("staff" if parts[1] == "staff" else ".".join(parts[1:])), [], parts[0]
    if len(parts) == 1:
        return None, [], parts[0]
    return parts[0], parts[1:-1], parts[-1]


def role_party(role: str | None, doc_type: str | None = None, task: str | None = None, attr: str | None = None) -> str:
    """서류 속 역할 → 당사자. 업무 > 문서 종류 > 역할 기본값 순."""
    if role is None:   # 역할 없이 속성만 있는 키 (bank, date …): roles.json 의 single
        return load("roles").get("single", {}).get(attr or "", "unassigned")
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
    party = role_party(role, doc_type, task, attr)
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


def common_key(doc_type: str | None, key: str, include_suggested: bool = False) -> str | None:
    """문서별 키 → 이은 공통 키. 그 자체가 공통 키면 그대로."""
    if key in load("common").get("keys", {}):
        return key
    x = load("links").get("links", {}).get(doc_type or "", {}).get(key)
    if x and (x["state"] == "이음" or (include_suggested and x["state"] == "제안")):
        return x["to"]
    return None


def scope(doc_type: str | None, key: str) -> str:
    return "공통" if common_key(doc_type, key) else "문서별"


def match_extracted(key: str, doc_type: str | None = None) -> str | None:
    """외부 추출 결과의 키 → 공통 키 (서류 넣기). 공통 키 그대로 · 그 문서에서 이은 칸 · 키 규칙의 다른 이름(aliases, 대소문자·기호 무시)."""
    if ck := common_key(doc_type, key):
        return ck
    from . import keyrules as KR

    common = load("common").get("keys", {})
    alias = {re.sub(r"[^a-z0-9]", "", a.lower()): k for a, k in KR.alias_index().items()}
    k = alias.get(re.sub(r"[^a-z0-9]", "", key.lower()))
    if k in common:
        return k
    pk = resolve(key, doc_type)["party_key"] if re.fullmatch(r"[a-z][a-z0-9_]*(\.[a-z0-9_]+)+", key) else None   # 역할.값 꼴이면 역할의 뜻으로
    return pk if pk in common else None


def apply_common(doc_id: str, fields: list[dict]) -> list[dict]:
    """문항·라벨에 쓸 키 (평가 세트 3.0, DESIGN 16.5 K4): 공통 키에 이은(이음) 칸은 공통 키로 묻고 답한다. 원래 키는 doc_key.
    같은 공통 키가 이미 있거나 둘 이상의 칸이 같은 공통 키에 이어져 있으면 처음 것만 바꿔 한 문서 안에서 키가 겹치지 않게 한다."""
    dt = doc_type_of(doc_id)
    if not dt:
        return fields
    present = {f["key"] for f in fields}
    taken, out = set(), []
    for f in fields:
        ck = None if f.get("group") else common_key(dt, f["key"])
        if ck and ck != f["key"] and ck not in present and ck not in taken:
            taken.add(ck)
            out.append({**f, "key": ck, "doc_key": f["key"]})
        else:
            out.append(f)
    return out


def doc_name(doc_id: str, default: str) -> tuple[str, list[str]]:
    """분류 문항의 정답 문서명과 다른 이름 (같은 문서의 서식이 여러 개여도 정답은 하나)."""
    dt = doc_type_of(doc_id)
    t = load("doc_types").get("types", {}).get(dt or "")
    if not t:
        return default, []
    return t["name"], [x for x in dict.fromkeys([default, *t.get("aliases", [])]) if x and x != t["name"]]
