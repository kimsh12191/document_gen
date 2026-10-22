"""키 사전 풀이 (studio/DESIGN.md 16절). 파일은 docgen/dictionary/*.json (자동 초안: docgen/scripts/build_dictionary.py).

칸마다 키는 하나, 범위는 둘이다.
  공통 키   여러 문서에 나오고 서류끼리 대조·심사하는 값 (common.json, 예: customer.name 고객 성명)
  문서별 키 그 서식에만 있는 칸. 서식의 키(fields.json) 그대로
칸이 '누구의 · 무엇'(당사자 parties.json · 속성 attributes.json)인지 정하면(form_keys.json, 서식마다), 그 둘이 공통 키이면
공통 키로 묻고 답한다. 정하지 않은 칸은 서식의 키 그대로 (그 자체가 공통 키면 공통).
  field_key("hf011", "signer2.name") → {key: "agent.name", common: True, who: "agent", what: "name", by: "사람", …}
  apply("hf011", fields) → 문항·라벨에 쓸 키로 바꾼 칸 (원래 키는 doc_key)

  resolve("remitter.name", task="fx_remittance") → {party: "customer", role: "remitter", attribute: "name", sub: [],
                                                    canonical: "remitter.name", party_key: "customer.name"}
  resolve 는 정하지 않은 칸의 '누구의 · 무엇' 추정 (키 사전 '정리할 것'의 후보). 합치기는 결정(accepted)된 것만 따라간다.
  doc_type_of("hana_official_049") → 문서 종류 ID, task_of("주담대") → 업무 ID, find_doc_type("Commercial Invoice") → 문서 종류 ID
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

DIR = Path(__file__).with_name("dictionary")
FILES = ("parties", "roles", "attributes", "doc_types", "tasks", "options", "merges", "relations", "common", "form_keys")
MARKS = ("seal", "sign")   # 무엇이 도장·서명이면 키는 seal.<누구> (resolve 의 party_key 와 같은 꼴)
_cache: dict = {}


def load(name: str) -> dict:
    """파일이 바뀌면 다시 읽는다. 바뀌었는지는 1초에 한 번만 본다 (화면 하나가 수만 칸을 풀 때 stat 이 대부분이라)."""
    now = time.monotonic()
    hit = _cache.get(name)
    if hit and hit[2] == DIR and now - hit[3] < 1.0:
        return hit[1]
    p = DIR / f"{name}.json"
    m = p.stat().st_mtime if p.exists() else 0.0
    if not hit or hit[0] != m or hit[2] != DIR:
        hit = (m, json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}, DIR, now)
    _cache[name] = (hit[0], hit[1], DIR, now)
    return hit[1]


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
    ms = load("merges")
    if _cache.get("_into", (None,))[0] is not ms:
        _cache["_into"] = (ms, {(m["dict"], m["from"]): m["into"] for m in ms.get("items", []) if m["status"] == "accepted"})
    acc = _cache["_into"][1]
    while (dict_, name) in acc and name not in seen:
        seen.add(name)
        name = acc[(dict_, name)]
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


def key_for(who: str, what: str) -> str:
    """누구의 · 무엇 → 키 이름 (customer·name → customer.name, customer·seal → seal.customer)."""
    return f"{what}.{who}" if what in MARKS else f"{who}.{what}"


def who_what(key: str) -> tuple[str | None, str | None]:
    """키 이름 → 누구의 · 무엇 (key_for 의 반대). 공통 키에 쓴다."""
    p = key.split(".")
    if len(p) != 2:
        return None, None
    return (p[1], p[0]) if p[0] in MARKS else (p[0], p[1])


def common_of(who: str | None, what: str | None) -> str | None:
    if not who or not what:
        return None
    k = key_for(who, what)
    return k if k in load("common").get("keys", {}) else None


def form_entries(form_id: str) -> dict[str, dict]:
    """그 서식에서 사람(또는 자동 초안)이 정한 칸: 서식의 키 → {who, what, by}."""
    return load("form_keys").get("forms", {}).get(form_id, {})


def guess(key: str, doc_type: str | None = None) -> tuple[str | None, str | None]:
    """정하지 않은 칸의 누구의 · 무엇 추정 (당사자 미정이면 who 없음)."""
    r = resolve(key, doc_type)
    who = None if r["party"] in ("unassigned", "staff", None) else r["party"]
    return who, (None if r["sub"] else r["attribute"])


def field_key(form_id: str, key: str) -> dict:
    """칸 하나의 최종 키. by: 사람 | 자동 (정한 것) | 없음 (서식의 키 그대로)."""
    e = form_entries(form_id).get(key)
    if e:
        ck = common_of(e.get("who"), e.get("what"))
        return {"raw": key, "key": ck or key, "common": bool(ck), "who": e.get("who"), "what": e.get("what"), "by": e.get("by", "사람")}
    if key in load("common").get("keys", {}):
        who, what = who_what(key)
        return {"raw": key, "key": key, "common": True, "who": who, "what": what, "by": "없음"}
    return {"raw": key, "key": key, "common": False, "who": None, "what": None, "by": "없음"}


def describe(form_id: str | None, key: str, label: str | None = None, doc_key: str | None = None) -> str:
    """질문에 붙일 칸 설명: 누구의 · 무엇(키 사전)과 표의 몇 번째 행인지. 이름표와 같으면 뺀다.
    describe("hf011", "customer.name", "성명") → "고객 성명", describe(None, "debts.1.balance", "잔액") → "2행"."""
    parts = []
    common = load("common").get("keys", {})
    if key in common:
        parts.append(common[key].get("name") or "")
    elif form_id:
        e = field_key(form_id, doc_key or key)
        who = load("parties").get("parties", {}).get(e["who"] or "", {}).get("name")
        what = load("attributes").get("attributes", {}).get(e["what"] or "", {}).get("name")
        if who:
            parts.append(f"{who}의 {what}" if what else who)
    segs = key.split(".")
    nums = [i for i, s in enumerate(segs) if s.isdigit()]
    if nums:   # 생성기 서식은 행을 0부터 센다 (템플릿 loop.index0)
        i = nums[0]
        table = ".".join(segs[:i]).replace("_", " ")   # 한글 키면 표 이름으로 쓴다 (기업부담금_목록.0.상품명 → 기업부담금 목록 1행)
        table = table + " " if re.search(r"[가-힣]", table) else ""
        parts.append(f"{table}{int(segs[i]) + 1}{'번째' if i == len(segs) - 1 else '행'}")
    return ", ".join(p for p in parts if p and _norm(p) != _norm(label or ""))


def mark_what(key: str, what: str | None) -> str | None:
    """도장·서명 자리 키(seal.* · sign.*)의 무엇은 늘 도장·서명이다."""
    p = key.split(".")[0]
    return p if p in MARKS else what


def set_fields(form_id: str, keys: list[str], who: str | None, what: str | None, by: str = "사람", clear: bool = False) -> list[dict]:
    """칸(서식의 키 하나 이상 — 서명 칸이면 이름·서명·도장)의 누구의 · 무엇을 정한다.
    둘 다 비워도 '문서별로 정함'으로 남는다 (자동 초안이 다시 잇지 않게).
    clear: 정한 것을 지워 처음 상태로 (서식의 키 그대로, 사전을 다시 만들면 자동 초안이 다시 정할 수 있음)."""
    d = load("form_keys")
    fk = d.setdefault("forms", {}).setdefault(form_id, {})
    for key in keys:
        if clear:
            fk.pop(key, None)
        else:
            fk[key] = {"who": who or None, "what": mark_what(key, what) or None, "by": by}
    if not fk:
        d["forms"].pop(form_id)
    save("form_keys", d)
    return [field_key(form_id, k) for k in keys]


def set_field(form_id: str, key: str, who: str | None, what: str | None, by: str = "사람", clear: bool = False) -> dict:
    return set_fields(form_id, [key], who, what, by, clear)[0]


FIELDS_JSON = DIR.parents[1] / "guide" / "fields" / "fields.json"   # html 서식의 칸 (서식마다 렌더링해 모은 키, build_schema.py)
_cells: dict = {}


def _raw_cells(form_id: str) -> list[dict]:
    """서식의 칸: [{id, t, label, keys}]. overlay 서식은 레이아웃에서 바로 (영역 편집기와 같은 키), html 서식은 fields.json."""
    from .registry import load_all

    spec = load_all().get(form_id)
    if spec is not None and spec.template == "_real_form.html.j2":
        from . import overrides as OV
        from . import realform as RF

        if ("_src", form_id) not in _cells:   # 레이아웃 파일 찾기(glob)는 한 번만
            no = RF.form_no(form_id)
            _cells[("_src", form_id)] = (RF.layout_path(no) if no is not None else (RF.image_form_dir(form_id) or Path()) / "layout.json",
                                         OV.path(form_id))
        stamp = tuple(f.stat().st_mtime if f and f.exists() else 0 for f in _cells[("_src", form_id)])
        if _cells.get(form_id, (None,))[0] != stamp:
            _cells[form_id] = (stamp, [{"id": i, **v} for i, v in RF.layout_keys(form_id).items() if v["keys"]])
        return _cells[form_id][1]
    m = FIELDS_JSON.stat().st_mtime if FIELDS_JSON.exists() else 0
    if _cells.get("__fields__", (None,))[0] != m:
        _cells["__fields__"] = (m, json.loads(FIELDS_JSON.read_text(encoding="utf-8")) if FIELDS_JSON.exists() else {})
    t_of = {"seal": "sign", "signature": "sign", "checkbox": "check"}
    return [{"id": k["key"], "t": t_of.get(k.get("type"), "text"), "label": k.get("label") or "", "keys": [k["key"]],
             "example": k.get("example")} for k in _cells["__fields__"][1].get(form_id, {}).get("keys", [])]


def form_cells(form_id: str) -> list[dict]:
    """서식의 칸마다 최종 키: 칸의 첫 키(서명 칸이면 이름, 없으면 도장)로 누구의 · 무엇과 공통/문서별을 보인다."""
    out = []
    for c in _raw_cells(form_id):
        ks = [field_key(form_id, k) for k in c["keys"]]
        main = ks[0]
        out.append({**c, "keys": ks, "key": main["key"], "common": main["common"], "who": main["who"],
                    "what": main["what"], "by": main["by"]})
    return out


def common_key(doc_type: str | None, key: str) -> str | None:
    """문서 종류의 칸 키 → 공통 키 (그 문서 종류의 서식 가운데 정한 것이 있으면 그것). 그 자체가 공통 키면 그대로.
    서류 넣기·라벨 검수처럼 서식이 아니라 문서 종류만 아는 곳이 쓴다."""
    if key in load("common").get("keys", {}):
        return key
    forms = load("doc_types").get("types", {}).get(doc_type or "", {}).get("forms", [])
    for fid in forms:
        f = field_key(fid, key)
        if f["by"] != "없음":
            return f["key"] if f["common"] else None
    return None


def scope(doc_type: str | None, key: str) -> str:
    return "공통" if common_key(doc_type, key) else "문서별"


def match_extracted(key: str, doc_type: str | None = None) -> str | None:
    """외부 추출 결과의 키 → 공통 키 (서류 넣기). 공통 키 그대로 · 그 문서에서 정한 칸 · 키 규칙·공통 키의 다른 이름(aliases, 대소문자·기호 무시)."""
    if ck := common_key(doc_type, key):
        return ck
    from . import keyrules as KR

    common = load("common").get("keys", {})
    alias = {re.sub(r"[^a-z0-9]", "", a.lower()): k for a, k in KR.alias_index().items()}
    alias.update({re.sub(r"[^0-9a-z가-힣]", "", a.lower()): ck for ck, v in common.items() for a in v.get("aliases", [])})   # 공통 키에 남긴 다른 이름 (건 번호 등)
    k = alias.get(re.sub(r"[^a-z0-9]", "", key.lower())) or alias.get(re.sub(r"[^0-9a-z가-힣]", "", key.lower()))
    if k in common:
        return k
    pk = resolve(key, doc_type)["party_key"] if re.fullmatch(r"[a-z][a-z0-9_]*(\.[a-z0-9_]+)+", key) else None   # 역할.값 꼴이면 역할의 뜻으로
    return pk if pk in common else None


def apply(form_id: str, fields: list[dict]) -> list[dict]:
    """문항·라벨에 쓸 키 (평가 세트 3.0, DESIGN 16.5 K4): 공통 키로 정한 칸은 공통 키로 묻고 답한다. 원래 키는 doc_key.
    같은 공통 키가 이미 있거나 둘 이상의 칸이 같은 공통 키면 처음 것만 바꿔 한 문서 안에서 키가 겹치지 않게 한다."""
    present = {f["key"] for f in fields}
    taken, out = set(), []
    for f in fields:
        ck = None if f.get("group") else field_key(form_id, f["key"])
        ck = ck["key"] if ck and ck["common"] else None
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
