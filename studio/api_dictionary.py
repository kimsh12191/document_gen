"""키 사전 API (studio/DESIGN.md 16.0). 칸마다 키는 하나: 공통 키(common.json) 또는 문서별 키(서식의 키 그대로).
칸이 누구의(parties.json) · 무엇(attributes.json)인지 정하면(form_keys.json) 그 둘이 공통 키일 때 공통 키가 된다.
파일 읽기·풀이는 docgen/dictionary.py. 사람이 정한 것은 by: 사람.

  GET  /api/dictionary                          개수 (공통 키 · 칸 · 공통 칸 · 문서별 칸 · 정리할 것 · 서식 · 문서 · 업무)
  GET  /api/dictionary/vocab                    누구의(당사자) · 무엇(속성) · 공통 키 목록 — 고르기 상자
  GET  /api/dictionary/common                   공통 키마다 누구의 · 무엇 · 쓰는 서식·칸 수 (누구의 × 무엇 표)
  GET  /api/dictionary/keys?scope=common&q=     공통 키 목록 (영역 편집·서류 넣기가 쓰는 예전 모양)
  GET  /api/dictionary/key/{공통 키}             공통 키: 이름·값 종류·그 키인 칸(서식마다)·쓰는 업무
  POST /api/dictionary/common {who, what, name, kind}   새 공통 키 (누구의 · 무엇) · PUT /api/dictionary/key/{공통 키} {name, kind}
  GET  /api/dictionary/cells?form=&doc=&q=&scope=common|doc&who=   칸 목록 (서식마다, 서명 칸은 이름·서명·도장을 한 칸으로)
  PUT  /api/dictionary/cells {items: [{form, keys}], who, what, clear}   칸의 누구의 · 무엇 정하기 (clear: 처음 상태로)
  GET  /api/dictionary/todo                     정리할 것: 공통 키 후보 · 누구 것인지 모르는 서명 칸 · 누구의만 정하면 되는 칸 · 깨진 이름표
  GET  /api/dictionary/common_for/{서식 ID}      그 서식의 공통 키 칸 — 시나리오 작업의 항목 고르기
  GET  /api/dictionary/doc_types · PUT /api/dictionary/doc_type/{ID} {name, group, aliases}
  GET  /api/dictionary/tasks · PUT /api/dictionary/task/{ID} {name, group, aliases, roles}
  GET  /api/dictionary/links/task/{업무} · /links/doc_type/{문서}   업무 ↔ 문서 ↔ 공통 키 (업무 안 둘 이상의 문서에 나오는 공통 키 = 대조 후보)
"""
import re
from collections import Counter, defaultdict
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
HUMAN = "사람"
WHAT_NAME = {"seal": "도장", "sign": "서명"}
BROKEN = re.compile(r"^.?$|_{3,}")   # 한 글자 이하, 밑줄 칸


def make_router(guard) -> APIRouter:
    from docgen import dictionary as DIC
    from docgen.registry import load_all

    r = APIRouter()

    def forms() -> dict[str, dict]:
        """서식 ID → {name, doc (문서 종류), doc_name}."""
        types = DIC.load("doc_types").get("types", {})
        of = {f: tid for tid, t in types.items() for f in t.get("forms", [])}
        return {fid: {"name": s.name, "doc": of.get(fid), "doc_name": types.get(of.get(fid) or "", {}).get("name", s.name),
                      "overlay": s.template == "_real_form.html.j2"} for fid, s in sorted(load_all().items())}

    def all_cells():
        for fid, f in forms().items():
            for c in DIC.form_cells(fid):
                yield fid, f, c

    def who_names() -> dict[str, str]:
        return {k: v["name"] for k, v in DIC.load("parties")["parties"].items()}

    def what_name(what: str | None) -> str:
        if not what:
            return ""
        return WHAT_NAME.get(what) or DIC.load("attributes")["attributes"].get(what, {}).get("name") or what

    def row(fid: str, f: dict, c: dict) -> dict:
        return {"form": fid, "form_name": f["name"], "doc": f["doc"], "doc_name": f["doc_name"], "id": c["id"], "t": c["t"],
                "label": c["label"], "key": c["key"], "common": c["common"], "who": c["who"], "what": c["what"], "by": c["by"],
                "raw": [k["raw"] for k in c["keys"]], "keys": [{"raw": k["raw"], "key": k["key"], "common": k["common"]} for k in c["keys"]],
                "example": c.get("example")}

    def todo_groups(cells: list | None = None) -> list[dict]:
        common = DIC.load("common").get("keys", {})
        norm = lambda t: re.sub(r"[\s()\[\]:*·.]", "", t or "")  # noqa: E731
        whats = {norm(what_name(w)): w for w in {DIC.who_what(k)[1] for k in common} - {"kind", "id", "office"}}   # 공통 키에 쓰이는 무엇의 이름 (주소·성명 …, '구분' 같은 말은 빼고)
        cand, marks, broken, labels = [], [], [], defaultdict(list)
        for fid, f, c in (all_cells() if cells is None else cells):
            if c["t"] == "staff":   # 결재란은 늘 은행
                continue
            x = row(fid, f, c)
            who, what = DIC.guess(c["keys"][0]["raw"], f["doc"]) if c["by"] == "없음" else (c["who"], c["what"])
            if c["by"] == "없음" and not c["common"] and DIC.common_of(who, what):
                cand.append({**x, "suggest": {"who": who, "what": what, "key": DIC.key_for(who, what)}})
            elif c["t"] == "sign" and f["overlay"] and not c["who"]:   # html 서식의 서명 칸은 템플릿이 이름을 정한다
                marks.append(x)
            elif c["t"] == "text" and c["by"] == "없음" and BROKEN.search(re.sub(r"\s", "", c["label"] or "")):
                broken.append(x)
            elif not c["common"] and not c["who"] and c["t"] in ("text", "date") and norm(c["label"]) in whats:
                labels[norm(c["label"])].append({**x, "suggest": {"what": whats[norm(c["label"])]}})
        who_missing = [{"label": rows[0]["label"], "what": rows[0]["suggest"]["what"], "what_name": what_name(rows[0]["suggest"]["what"]),
                        "forms": len({x["form"] for x in rows}), "rows": rows} for rows in labels.values()]
        who_missing.sort(key=lambda g: -len(g["rows"]))
        return [
            {"id": "candidate", "title": "공통 키 후보", "n": len(cand), "rows": cand,
             "desc": "칸의 키를 풀어 보면 공통 키인데 아직 정하지 않은 칸. 맞으면 제안대로 정하고, 아니면 문서별로 남깁니다."},
            {"id": "mark", "title": "누구 것인지 모르는 서명 칸", "n": len(marks), "rows": marks,
             "desc": "서명·도장 칸에 누구의 이름을 쓸지 정합니다. 은행·직원 칸으로 정하면 고객 이름을 쓰지 않습니다."},
            {"id": "who", "title": "누구의만 정하면 되는 칸", "n": sum(len(g["rows"]) for g in who_missing), "groups": who_missing,
             "desc": "이름표가 공통 키의 '무엇'(주소·성명 …)인데 누구의 것인지 모르는 문서별 키. 누구의를 고르면 공통 키가 됩니다."},
            {"id": "broken", "title": "깨진 이름표", "n": len(broken), "rows": broken,
             "desc": "이름표가 한 글자이거나 밑줄·안내 문구인 칸. 서식의 영역 편집에서 이름표를 고칩니다."},
        ]

    @r.get("/api/dictionary")
    def summary():
        n = Counter()
        fs = forms()
        cells = list(all_cells())   # 칸을 한 번만 푼다 (해야 할 일도 같은 칸으로)
        for _, _, c in cells:
            n["cells"] += 1
            n["common_cells" if c["common"] else "doc_cells"] += 1
        return {"common": len(DIC.load("common").get("keys", {})), **n, "forms": len(fs),
                "todo": sum(g["n"] for g in todo_groups(cells)),
                "docs": len(DIC.load("doc_types")["types"]), "tasks": len(DIC.load("tasks")["tasks"])}

    @r.get("/api/dictionary/vocab")
    def vocab():
        parties = DIC.load("parties")["parties"]
        attrs = DIC.load("attributes")["attributes"]
        common = DIC.load("common").get("keys", {})
        used = Counter(DIC.who_what(k)[1] for k in common)
        what = [{"id": k, "name": WHAT_NAME[k], "common": used.get(k, 0)} for k in DIC.MARKS]
        what += sorted(({"id": k, "name": v.get("name") or k, "kind": v.get("kind"), "common": used.get(k, 0)}
                        for k, v in attrs.items() if k not in DIC.MARKS), key=lambda x: (-x["common"], x["name"]))
        return {"who": [{"id": k, "name": v["name"], "desc": v.get("desc", "")} for k, v in parties.items() if k != "unassigned"],
                "what": what,
                "common": [{"key": k, "who": DIC.who_what(k)[0], "what": DIC.who_what(k)[1], **v} for k, v in common.items()]}

    @r.get("/api/dictionary/common")
    def common_table():
        common = DIC.load("common").get("keys", {})
        n_cells, n_forms = Counter(), defaultdict(set)
        for fid, _, c in all_cells():
            for k in c["keys"]:
                if k["common"]:
                    n_cells[k["key"]] += 1
                    n_forms[k["key"]].add(fid)
        wn = who_names()
        rows = [{"key": k, "who": DIC.who_what(k)[0], "what": DIC.who_what(k)[1], "who_name": wn.get(DIC.who_what(k)[0], ""),
                 "what_name": what_name(DIC.who_what(k)[1]), **v, "cells": n_cells[k], "forms": len(n_forms[k])}
                for k, v in common.items()]
        return {"rows": sorted(rows, key=lambda x: -x["forms"]), "who": wn}

    @r.get("/api/dictionary/keys")
    def keys(scope: str = "common", q: str = ""):
        ql = q.strip().lower()
        rows = [{"key": k, **v} for k, v in DIC.load("common").get("keys", {}).items()
                if not ql or ql in k.lower() or ql in v["name"].lower()]
        return {"rows": sorted(rows, key=lambda x: -x.get("docs", 0)), "total": len(rows)}

    @r.get("/api/dictionary/key/{ck:path}")
    def key(ck: str):
        common = DIC.load("common").get("keys", {})
        if ck not in common:
            raise HTTPException(404, ck)
        cells = [row(fid, f, c) for fid, f, c in all_cells() if any(k["key"] == ck for k in c["keys"])]
        rel = DIC.load("relations").get("doc_types", {})
        tn = {k: v["name"] for k, v in DIC.load("tasks")["tasks"].items()}
        tasks = sorted({t for x in cells for t in rel.get(x["doc"] or "", {}).get("tasks", [])})
        who, what = DIC.who_what(ck)
        return {"key": ck, **common[ck], "who": who, "what": what, "who_name": who_names().get(who, ""), "what_name": what_name(what),
                "cells": cells, "forms": len({x["form"] for x in cells}), "tasks": [{"id": t, "name": tn.get(t, t)} for t in tasks]}

    class KeyReq(BaseModel):
        name: str
        kind: str = "text"

    @r.put("/api/dictionary/key/{ck:path}")
    def put_key(ck: str, req: KeyReq):
        d = DIC.load("common")
        if ck not in d.get("keys", {}):
            raise HTTPException(404, f"없는 공통 키: {ck} (새로 만들 때는 누구의 · 무엇으로)")
        if not req.name.strip():
            raise HTTPException(400, "이름을 적으세요")
        d["keys"][ck].update(name=req.name.strip(), kind=req.kind or "text", by=HUMAN)
        DIC.save("common", d)
        return {"key": ck, **d["keys"][ck]}

    class CommonReq(BaseModel):
        who: str
        what: str
        name: str = ""
        kind: str = "text"

    @r.post("/api/dictionary/common")
    def new_common(req: CommonReq):
        if req.who not in DIC.load("parties")["parties"] or req.who == "unassigned":
            raise HTTPException(400, f"모르는 누구의: {req.who}")
        if not re.fullmatch(r"[a-z][a-z0-9_]*", req.what):
            raise HTTPException(400, "무엇은 영어 소문자 snake_case (예: bank_address)")
        ck = DIC.key_for(req.who, req.what)
        d = DIC.load("common")
        if ck in d.get("keys", {}):
            raise HTTPException(400, f"이미 있는 공통 키: {ck}")
        name = req.name.strip() or f"{who_names()[req.who]} {what_name(req.what)}"
        d.setdefault("keys", {})[ck] = {"name": name, "kind": req.kind or "text", "docs": 0, "by": HUMAN}
        DIC.save("common", d)
        return {"key": ck, **d["keys"][ck]}

    @r.get("/api/dictionary/cells")
    def cells(form: str = "", doc: str = "", q: str = "", scope: str = "", who: str = "", limit: int = 500):
        ql = q.strip().lower()
        out = []
        fs = forms()
        for fid in ([form] if form else fs):
            if fid not in fs or (doc and fs[fid]["doc"] != doc):
                continue
            for c in DIC.form_cells(fid):
                x = row(fid, fs[fid], c)
                if scope and (scope == "common") != x["common"]:
                    continue
                if who and (x["who"] or "") != (who if who != "-" else ""):
                    continue
                if ql and not any(ql in (s or "").lower() for s in (x["label"], x["key"], x["form_name"], x["doc_name"], *x["raw"])):
                    continue
                out.append(x)
        return {"rows": out[:max(1, min(limit, 3000))], "total": len(out)}

    class CellsReq(BaseModel):
        items: list[dict]
        who: str | None = None
        what: str | None = None
        clear: bool = False

    @r.put("/api/dictionary/cells")
    def put_cells(req: CellsReq):
        parties = DIC.load("parties")["parties"]
        if req.who and req.who not in parties:
            raise HTTPException(400, f"모르는 누구의: {req.who}")
        fs = forms()
        out = []
        for it in req.items:
            if it.get("form") not in fs or not it.get("keys"):
                raise HTTPException(400, f"서식·키가 없습니다: {it}")
            out += DIC.set_fields(it["form"], list(it["keys"]), req.who, req.what, HUMAN, req.clear)
        return {"changed": len(req.items), "keys": out}

    @r.get("/api/dictionary/todo")
    def todo():
        return {"groups": todo_groups()}

    @r.get("/api/dictionary/common_for/{form_id}")
    def common_for(form_id: str):
        common = DIC.load("common").get("keys", {})
        out = {}
        for c in DIC.form_cells(form_id):
            for k in c["keys"]:
                if k["common"] and k["key"] not in out:
                    out[k["key"]] = {"key": k["key"], "name": common.get(k["key"], {}).get("name", k["key"]),
                                     "doc_key": k["raw"], "label": c["label"]}
        return {"doc_type": DIC.doc_type_of(form_id), "keys": sorted(out.values(), key=lambda x: x["key"])}

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
        return DIC.load("tasks") | {"parties": who_names()}

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
        dn = {k: v["name"] for k, v in DIC.load("doc_types")["types"].items()}
        common = DIC.load("common").get("keys", {})
        return {"doc_types": [{"id": d, "name": dn.get(d, d)} for d in rel["doc_types"]],
                "shared": [{"key": x["party_key"], "name": common.get(x["party_key"], {}).get("name", ""), "doc_types": x["doc_types"],
                            "names": [dn.get(d, d) for d in x["doc_types"]]} for x in rel["shared"]]}

    @r.get("/api/dictionary/links/doc_type/{tid}")
    def links_doc(tid: str):
        rel = DIC.load("relations").get("doc_types", {}).get(tid)
        if rel is None:
            raise HTTPException(404, tid)
        tn = {k: v["name"] for k, v in DIC.load("tasks")["tasks"].items()}
        cs = [c for fid in DIC.load("doc_types")["types"].get(tid, {}).get("forms", []) for c in DIC.form_cells(fid)]
        return {"tasks": [{"id": t, "name": tn.get(t, t)} for t in rel["tasks"]], "keys": len(cs),
                "common": sum(1 for c in cs if c["common"])}

    return r
