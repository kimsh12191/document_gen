"""키 사전 계층 API (studio/DESIGN.md 16절). 파일: docgen/dictionary/*.json (docgen/dictionary.py). 사람이 고친 항목은 by: 사람.

  GET  /api/dictionary                     당사자별 역할·키 수, 통계, 미확정 수 (탭 배지)
  GET  /api/dictionary/role/{역할}          역할 정보 + 그 역할의 키 (속성·항목명·당사자 키)
  PUT  /api/dictionary/role/{역할}          {party, name, by_task}
  PUT  /api/dictionary/attribute/{속성}     {name, kind, aliases}
  GET  /api/dictionary/marks               표시 요소: 도장·서명 키(당사자별) + 체크 보기 목록
  GET  /api/dictionary/doc_types · PUT /api/dictionary/doc_type/{ID} {name, group, aliases}
  GET  /api/dictionary/tasks · PUT /api/dictionary/task/{ID} {name, group, aliases, roles}
  GET  /api/dictionary/merges?dict=&status=&q=   ·   POST /api/dictionary/merges {items: [{dict, from, into}], status}
  GET  /api/dictionary/single?show=unassigned|unsure|all&q=   역할 없이 속성만 있는 키(bank, 취급점 …)와 당사자
  PUT  /api/dictionary/single {parties: {속성: 당사자}}       사람이 정한 것으로 남긴다
  GET  /api/dictionary/links/task/{업무} · /links/doc_type/{문서 종류} · /links/party_key/{당사자 키}
       업무 ↔ 문서 종류 ↔ 당사자 키 연결 (relations.json, 초안 만들 때 새로 계산). 업무에서는 둘 이상의 문서에 나오는 당사자 키 = 대조 후보
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
HUMAN = "사람"


def _keys() -> list[dict]:
    p = ROOT / "docgen" / "keys.json"
    return json.loads(p.read_text(encoding="utf-8"))["keys"] if p.exists() else []


def make_router(guard) -> APIRouter:
    from docgen import dictionary as DIC

    r = APIRouter()

    @r.get("/api/dictionary")
    def summary():
        parties = DIC.load("parties")["parties"]
        roles = DIC.load("roles")["roles"]
        by = defaultdict(list)
        for name, x in roles.items():
            by[x["party"]].append({"role": name, **x})
        merges = DIC.load("merges")["items"]
        return {"parties": [{"id": p, **v, "roles": sorted(by.get(p, []), key=lambda x: -x["forms"]),
                             "forms": sum(x["forms"] for x in by.get(p, [])), "keys": sum(x["keys"] for x in by.get(p, []))}
                            for p, v in parties.items()],
                "stats": json.loads((DIC.DIR / "stats.json").read_text(encoding="utf-8")) if (DIC.DIR / "stats.json").exists() else {},
                "unsure": sum(1 for x in roles.values() if not x.get("sure", True) and x.get("by") != HUMAN),
                "proposed": sum(1 for m in merges if m["status"] == "proposed"),
                "tasks": {k: v["name"] for k, v in DIC.load("tasks")["tasks"].items()}}

    @r.get("/api/dictionary/role/{role}")
    def role(role: str):
        roles = DIC.load("roles")["roles"]
        if role not in roles:
            raise HTTPException(404, role)
        rows = []
        pks = DIC.load("relations").get("party_keys", {})
        for k in _keys():
            rr, sub, attr = DIC.split(k["key"])
            if rr == role:
                res = DIC.resolve(k["key"])
                rows.append({"key": k["key"], "attribute": attr, "sub": sub, "labels": k.get("labels", [])[:4], "type": k.get("type"),
                             "forms": k.get("forms", 0), "party_key": res["party_key"], "canonical": res["canonical"],
                             "doc_types": pks.get(res["party_key"], {}).get("doc_types", 0)})
        return {"role": role, **roles[role], "keys": sorted(rows, key=lambda x: -x["forms"])}

    class RoleReq(BaseModel):
        party: str
        name: str = ""
        by_task: dict = {}

    @r.put("/api/dictionary/role/{role}")
    def put_role(role: str, req: RoleReq):
        d = DIC.load("roles")
        if req.party not in DIC.load("parties")["parties"]:
            raise HTTPException(400, f"모르는 당사자: {req.party}")
        x = d["roles"].setdefault(role, {"forms": 0, "keys": 0})
        x.update(party=req.party, sure=True, by=HUMAN, **({"name": req.name} if req.name else {}))
        x["by_task"] = {t: p for t, p in req.by_task.items() if p}
        if not x["by_task"]:
            x.pop("by_task")
        DIC.save("roles", d)
        return {"role": role, **x}

    class AttrReq(BaseModel):
        name: str = ""
        kind: str | None = None
        aliases: list[str] = []

    @r.put("/api/dictionary/attribute/{attr}")
    def put_attr(attr: str, req: AttrReq):
        d = DIC.load("attributes")
        x = d["attributes"].setdefault(attr, {"keys": 0})
        x.update(name=req.name, kind=req.kind, aliases=sorted({a.strip() for a in req.aliases if a.strip()}), by=HUMAN)
        DIC.save("attributes", d)
        return {"attribute": attr, **x}

    @r.get("/api/dictionary/attributes")
    def attributes(q: str = ""):
        a = DIC.load("attributes")["attributes"]
        ql = q.lower()
        rows = [{"id": k, **v} for k, v in a.items() if not ql or ql in k or ql in (v.get("name") or "").lower()]
        return {"attributes": sorted(rows, key=lambda x: -x.get("keys", 0))[:300], "total": len(a)}

    @r.get("/api/dictionary/marks")
    def marks():
        rows = []
        for k in _keys():
            if k.get("type") in ("seal", "signature"):
                res = DIC.resolve(k["key"])
                rows.append({"key": k["key"], "type": k["type"], "role": res["role"], "party": res["party"], "party_key": res["party_key"],
                             "labels": k.get("labels", [])[:3], "forms": k.get("forms", 0)})
        opts = DIC.load("options")["options"]
        return {"marks": sorted(rows, key=lambda x: (x["party"], -x["forms"])),
                "by_party": dict(Counter(x["party"] for x in rows)),
                "options": [{"attribute": a, **v} for a, v in list(opts.items())[:400]], "n_options": len(opts)}

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

    @r.get("/api/dictionary/merges")
    def merges(dict: str = "", status: str = "", q: str = ""):
        items = DIC.load("merges")["items"]
        ql = q.lower()
        rows = [m for m in items if (not dict or m["dict"] == dict) and (not status or m["status"] == status)
                and (not ql or ql in m["from"].lower() or ql in m["into"].lower() or ql in m["reason"].lower())]
        return {"items": rows[:500], "total": len(rows), "counts": dict_counts(items)}

    def dict_counts(items):
        return {"by_dict": dict(Counter(m["dict"] for m in items)), "by_status": dict(Counter(m["status"] for m in items)),
                "by_reason": dict(Counter(m["reason"].split("(")[0].split(":")[0] for m in items if m["status"] == "proposed"))}

    class MergeReq(BaseModel):
        items: list[dict]
        status: str

    @r.post("/api/dictionary/merges")
    def set_merges(req: MergeReq):
        if req.status not in ("proposed", "accepted", "rejected"):
            raise HTTPException(400, "status 는 proposed·accepted·rejected")
        d = DIC.load("merges")
        want = {(x["dict"], x["from"], x["into"]) for x in req.items}
        n = 0
        for m in d["items"]:
            if (m["dict"], m["from"], m["into"]) in want:
                m["status"], n = req.status, n + 1
        DIC.save("merges", d)
        dups = [m for m in d["items"] if (m["dict"], m["from"], m["into"]) in want and m["reason"].startswith("이름 두 벌")]
        if dups:   # 이름 두 벌의 결정은 keys.json 에도 (build_keys.py 가 남긴다)
            p = ROOT / "docgen" / "keys.json"
            k = json.loads(p.read_text(encoding="utf-8"))
            for x in k.get("duplicates", []):
                for m in dups:
                    if set(x["keys"]) == {m["from"], m["into"]}:
                        x["decision"] = m["into"] if req.status == "accepted" else None
            p.write_text(json.dumps(k, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        return {"changed": n, "counts": dict_counts(d["items"])}

    def _single_rows():
        f = ROOT / "guide" / "fields" / "fields.json"
        cnt, lab = Counter(), {}
        for v in (json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}).values():
            for k in v["keys"]:
                role, _, attr = DIC.split(k["key"])
                if role is None:
                    cnt[attr] += 1
                    lab.setdefault(attr, k.get("label") or "")
        return cnt, lab

    @r.get("/api/dictionary/single")
    def single(show: str = "unassigned", q: str = ""):
        d = DIC.load("roles")
        sm, unsure, human = d.get("single", {}), set(d.get("single_unsure", [])), set(d.get("single_human", []))
        cnt, lab = _single_rows()
        rows = [{"attribute": a, "party": sm.get(a, "unassigned"), "forms": n, "label": lab.get(a, ""),
                 "state": "사람" if a in human else "추정" if a in unsure else "기본"} for a, n in cnt.items()]
        rows = [x for x in rows if (show == "all" or (show == "unassigned" and x["party"] == "unassigned")
                                    or (show == "unsure" and x["state"] == "추정")) and (not q or q in x["attribute"] or q in x["label"])]
        return {"rows": sorted(rows, key=lambda x: -x["forms"])[:400], "total": len(rows),
                "counts": {"unassigned": sum(1 for a in cnt if sm.get(a, "unassigned") == "unassigned"),
                           "unsure": len(unsure & set(cnt)), "all": len(cnt)}}

    class SingleReq(BaseModel):
        parties: dict

    @r.put("/api/dictionary/single")
    def put_single(req: SingleReq):
        known = DIC.load("parties")["parties"]
        bad = [p for p in req.parties.values() if p not in known]
        if bad:
            raise HTTPException(400, f"모르는 당사자: {bad[:3]}")
        d = DIC.load("roles")
        d.setdefault("single", {}).update(req.parties)
        d["single_human"] = sorted(set(d.get("single_human", [])) | set(req.parties))
        d["single_unsure"] = sorted(set(d.get("single_unsure", [])) - set(req.parties))
        DIC.save("roles", d)
        return {"changed": len(req.parties)}

    def _names():
        return {k: v["name"] for k, v in DIC.load("doc_types")["types"].items()}, {k: v["name"] for k, v in DIC.load("tasks")["tasks"].items()}

    @r.get("/api/dictionary/links/task/{tid}")
    def links_task(tid: str):
        rel = DIC.load("relations").get("tasks", {}).get(tid)
        if rel is None:
            raise HTTPException(404, tid)
        dn, _ = _names()
        return {"doc_types": [{"id": d, "name": dn.get(d, d)} for d in rel["doc_types"]],
                "shared": [{**x, "names": [dn.get(d, d) for d in x["doc_types"]]} for x in rel["shared"]]}

    @r.get("/api/dictionary/links/doc_type/{tid}")
    def links_doc(tid: str):
        rel = DIC.load("relations").get("doc_types", {}).get(tid)
        if rel is None:
            raise HTTPException(404, tid)
        _, tn = _names()
        pks = DIC.load("relations").get("party_keys", {})
        return {"tasks": [{"id": t, "name": tn.get(t, t)} for t in rel["tasks"]], "keys": rel["keys"],
                "party_keys": sorted(({"party_key": pk, "doc_types": pks.get(pk, {}).get("doc_types", 0)} for pk in rel["party_keys"]),
                                     key=lambda x: (-x["doc_types"], x["party_key"]))}

    @r.get("/api/dictionary/links/party_key/{pk:path}")
    def links_pk(pk: str):
        rel = DIC.load("relations")
        dn, tn = _names()
        docs = [d for d, v in rel.get("doc_types", {}).items() if pk in v["party_keys"]]
        return {"party_key": pk, "doc_types": [{"id": d, "name": dn.get(d, d)} for d in docs],
                "tasks": [{"id": t, "name": tn.get(t, t)} for t in rel.get("party_keys", {}).get(pk, {}).get("tasks", [])]}

    return r
