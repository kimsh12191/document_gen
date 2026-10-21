"""키 사전 API (studio/DESIGN.md 16.0). 화면의 말은 업무명·문서명·키. 키의 범위는 공통 키(common.json) | 문서별 키(서식의 키 그대로,
fields.json), 문서별 키를 공통 키에 잇는 것은 links.json. 파일 읽기·풀이는 docgen/dictionary.py. 사람이 고친 것은 by: 사람.

  GET  /api/dictionary                          개수 (공통 키·문서별 키·이음·제안·문서·업무)
  GET  /api/dictionary/keys?scope=common|doc&doc=&q=&state=&to=   키 목록 (문서별은 문서·키마다 한 줄, 잇기 상태)
  GET  /api/dictionary/key/{공통 키}             공통 키: 이름·값 종류·이은 문서별 키(문서마다)·쓰는 업무
  PUT  /api/dictionary/key/{공통 키}             {name, kind} — 없으면 새로 만든다 (공통으로 올리기)
  POST /api/dictionary/link                     {items: [{doc, key}], to: 공통 키 | null, state: 이음 | 제안 | 끊음}
  GET  /api/dictionary/doc_types · PUT /api/dictionary/doc_type/{ID} {name, group, aliases}
  GET  /api/dictionary/tasks · PUT /api/dictionary/task/{ID} {name, group, aliases, roles}
  GET  /api/dictionary/common_for/{서식 ID}      그 서식에 있는 공통 키 (그 자체가 공통 키이거나 이은 칸) — 시나리오 작업의 항목 고르기
  GET  /api/dictionary/links/task/{업무} · /links/doc_type/{문서}   업무 ↔ 문서 ↔ 공통 키 (업무 안 둘 이상의 문서에 나오는 공통 키 = 대조 후보)
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
HUMAN = "사람"
STATES = ("이음", "제안", "끊음")


def make_router(guard) -> APIRouter:
    from docgen import dictionary as DIC

    r = APIRouter()
    cache: dict = {}

    def doc_keys() -> dict[str, dict[str, dict]]:
        """문서 → 문서별 키 → {label, type, forms}. fields.json 이 바뀌면 다시."""
        f = ROOT / "guide" / "fields" / "fields.json"
        m = f.stat().st_mtime if f.exists() else 0
        if cache.get("m") != m:
            out: dict = defaultdict(dict)
            ft = {fid: tid for tid, t in DIC.load("doc_types")["types"].items() for fid in t["forms"]}
            for fid, v in (json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}).items():
                tid = ft.get(fid)
                if not tid:
                    continue
                for k in v["keys"]:
                    x = out[tid].setdefault(k["key"], {"label": k.get("label") or "", "type": k.get("type"), "forms": 0})
                    x["forms"] += 1
            cache.update(m=m, v=dict(out))
        return cache["v"]

    def names():
        return ({k: v["name"] for k, v in DIC.load("doc_types")["types"].items()},
                {k: v["name"] for k, v in DIC.load("tasks")["tasks"].items()})

    @r.get("/api/dictionary")
    def summary():
        links = DIC.load("links").get("links", {})
        st = Counter(x["state"] for v in links.values() for x in v.values())
        return {"common": len(DIC.load("common").get("keys", {})), "doc_keys": sum(len(v) for v in doc_keys().values()),
                "linked": st.get("이음", 0), "suggested": st.get("제안", 0), "docs": len(DIC.load("doc_types")["types"]),
                "tasks": len(DIC.load("tasks")["tasks"])}

    @r.get("/api/dictionary/keys")
    def keys(scope: str = "common", doc: str = "", q: str = "", state: str = "", to: str = "", limit: int = 300):
        common = DIC.load("common").get("keys", {})
        ql = q.strip().lower()
        links = DIC.load("links").get("links", {})
        if scope == "common":
            n_links = Counter(x["to"] for v in links.values() for x in v.values() if x["state"] == "이음")
            n_sugg = Counter(x["to"] for v in links.values() for x in v.values() if x["state"] == "제안")
            rows = [{"key": k, **v, "linked": n_links.get(k, 0), "suggested": n_sugg.get(k, 0)} for k, v in common.items()
                    if not ql or ql in k.lower() or ql in v["name"].lower()]
            rows.sort(key=lambda x: -x.get("docs", 0))
            return {"rows": rows, "total": len(rows)}
        dn, _ = names()
        rows = []
        for tid, ks in doc_keys().items():
            if doc and tid != doc:
                continue
            for k, v in ks.items():
                ln = links.get(tid, {}).get(k)
                st = ln["state"] if ln else ("공통" if k in common else "")
                if (state and st != state) or (to and (not ln or ln["to"] != to)):
                    continue
                if ql and ql not in k.lower() and ql not in v["label"].lower() and ql not in dn.get(tid, "").lower():
                    continue
                rows.append({"doc": tid, "doc_name": dn.get(tid, tid), "key": k, **v, "state": st,
                             "to": (ln or {}).get("to") or (k if k in common else None), "by": (ln or {}).get("by")})
        rows.sort(key=lambda x: (x["doc_name"], x["key"]))
        return {"rows": rows[:max(1, min(limit, 2000))], "total": len(rows)}

    @r.get("/api/dictionary/key/{ck:path}")
    def key(ck: str):
        common = DIC.load("common").get("keys", {})
        if ck not in common:
            raise HTTPException(404, ck)
        dn, tn = names()
        linked = defaultdict(list)
        for tid, ks in DIC.load("links").get("links", {}).items():
            for k, x in ks.items():
                if x["to"] == ck and x["state"] != "끊음":
                    linked[tid].append({"key": k, "state": x["state"], "label": doc_keys().get(tid, {}).get(k, {}).get("label", "")})
        rel = DIC.load("relations").get("doc_types", {})
        tasks = sorted({t for d in linked for t in rel.get(d, {}).get("tasks", [])})
        return {"key": ck, **common[ck],
                "docs": [{"doc": d, "name": dn.get(d, d), "keys": linked[d]} for d in sorted(linked, key=lambda d: dn.get(d, d))],
                "tasks": [{"id": t, "name": tn.get(t, t)} for t in tasks]}

    class KeyReq(BaseModel):
        name: str
        kind: str = "text"

    @r.put("/api/dictionary/key/{ck:path}")
    def put_key(ck: str, req: KeyReq):
        if not re.fullmatch(r"[a-z][a-z0-9_]*(\.[a-z0-9_]+)+", ck):
            raise HTTPException(400, "공통 키는 영어 소문자 snake_case, 앞부분.값 (예: foreign.bank_address)")
        if not req.name.strip():
            raise HTTPException(400, "이름을 적으세요")
        d = DIC.load("common")
        x = d.setdefault("keys", {}).setdefault(ck, {"docs": 0})
        x.update(name=req.name.strip(), kind=req.kind or "text", by=HUMAN)
        DIC.save("common", d)
        return {"key": ck, **x}

    class LinkReq(BaseModel):
        items: list[dict]
        to: str | None = None
        state: str = "이음"

    @r.post("/api/dictionary/link")
    def link(req: LinkReq):
        if req.state not in STATES:
            raise HTTPException(400, f"state 는 {STATES}")
        if req.to is not None and req.to not in DIC.load("common").get("keys", {}):
            raise HTTPException(400, f"없는 공통 키: {req.to}")
        d = DIC.load("links")
        n = 0
        for it in req.items:
            cur = d.setdefault("links", {}).setdefault(it["doc"], {}).get(it["key"], {})
            to = req.to or cur.get("to")
            if to:
                d["links"][it["doc"]][it["key"]] = {"to": to, "state": req.state, "by": HUMAN}
                n += 1
        DIC.save("links", d)
        return {"changed": n}

    @r.get("/api/dictionary/common_for/{form_id}")
    def common_for(form_id: str):
        dt = DIC.doc_type_of(form_id)
        common = DIC.load("common").get("keys", {})
        f = ROOT / "guide" / "fields" / "fields.json"
        fields = json.loads(f.read_text(encoding="utf-8")).get(form_id, {}).get("keys", []) if f.exists() else []
        out = {}
        for k in fields:
            ck = DIC.common_key(dt, k["key"])
            if ck and ck not in out:
                out[ck] = {"key": ck, "name": common.get(ck, {}).get("name", ck), "doc_key": k["key"], "label": k.get("label") or ""}
        return {"doc_type": dt, "keys": sorted(out.values(), key=lambda x: x["key"])}

    @r.get("/api/dictionary/doc_types")
    def doc_types():
        return DIC.load("doc_types")

    class DocReq(BaseModel):
        name: str
        group: str
        aliases: list[str] = []

    @r.put("/api/dictionary/doc_type/{tid}")
    def put_doc(tid: str, req: DocReq):
        d = DIC.load("doc_types")
        if tid not in d["types"]:
            raise HTTPException(404, tid)
        if req.group not in d["groups"]:
            raise HTTPException(400, f"모르는 대분류: {req.group}")
        d["types"][tid].update(name=req.name.strip(), group=req.group, aliases=sorted({a.strip() for a in req.aliases if a.strip()}), by=HUMAN)
        DIC.save("doc_types", d)
        return {"id": tid, **d["types"][tid]}

    @r.get("/api/dictionary/tasks")
    def tasks():
        return DIC.load("tasks") | {"parties": {k: v["name"] for k, v in DIC.load("parties")["parties"].items()}}

    class TaskReq(BaseModel):
        name: str
        group: str
        aliases: list[str] = []
        roles: dict = {}

    @r.put("/api/dictionary/task/{tid}")
    def put_task(tid: str, req: TaskReq):
        d = DIC.load("tasks")
        if tid not in d["tasks"]:
            raise HTTPException(404, tid)
        parties = DIC.load("parties")["parties"]
        bad = [p for p in req.roles.values() if p not in parties]
        if bad or req.group not in d["groups"]:
            raise HTTPException(400, f"모르는 당사자·대분류: {bad or req.group}")
        d["tasks"][tid].update(name=req.name.strip(), group=req.group, aliases=sorted({a.strip() for a in req.aliases if a.strip()}),
                               roles={k.strip(): v for k, v in req.roles.items() if k.strip()}, by=HUMAN)
        DIC.save("tasks", d)
        return {"id": tid, **d["tasks"][tid]}

    @r.get("/api/dictionary/links/task/{tid}")
    def links_task(tid: str):
        rel = DIC.load("relations").get("tasks", {}).get(tid)
        if rel is None:
            raise HTTPException(404, tid)
        dn, _ = names()
        common = DIC.load("common").get("keys", {})
        return {"doc_types": [{"id": d, "name": dn.get(d, d)} for d in rel["doc_types"]],
                "shared": [{"key": x["party_key"], "name": common.get(x["party_key"], {}).get("name", ""), "doc_types": x["doc_types"],
                            "names": [dn.get(d, d) for d in x["doc_types"]]} for x in rel["shared"]]}

    @r.get("/api/dictionary/links/doc_type/{tid}")
    def links_doc(tid: str):
        rel = DIC.load("relations").get("doc_types", {}).get(tid)
        if rel is None:
            raise HTTPException(404, tid)
        _, tn = names()
        common = DIC.load("common").get("keys", {})
        ks = doc_keys().get(tid, {})
        ln = DIC.load("links").get("links", {}).get(tid, {})
        return {"tasks": [{"id": t, "name": tn.get(t, t)} for t in rel["tasks"]], "keys": len(ks),
                "common": sum(1 for k in ks if k in common or (ln.get(k) or {}).get("state") == "이음"),
                "suggested": sum(1 for k in ks if (ln.get(k) or {}).get("state") == "제안")}

    return r
