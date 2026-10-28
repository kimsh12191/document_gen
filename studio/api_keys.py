"""키 사전 API (studio/DESIGN.md 15.7). 사람이 정하는 부분은 docgen/key_rules.json (docgen/keyrules.py),
자동으로 모은 키 목록·이름 두 벌은 docgen/keys.json (docgen/scripts/build_keys.py).

  GET  /api/keyrules                    키 목록(자동 목록 + 사전) · 값 종류(코드·데이터) · 이름 두 벌 · 동의어
  GET  /api/keyrules/sources            값 출처로 고를 수 있는 프로필 경로와 예시 값
  POST /api/keyrules/examples           {kind | def} → 예시 값 10개 (저장 전 미리보기도)
  PUT  /api/keyrules/keys/{키}           {meaning, kind, source, aliases, labels} — labels 를 바꾸면 영향 받는 overlay 서식 수도 돌려준다
  DELETE /api/keyrules/keys/{키}
  PUT  /api/keyrules/kinds/{종류}        {meaning, how, source | choices | pattern}
  DELETE /api/keyrules/kinds/{종류}      (쓰는 키가 없을 때만)
  PUT  /api/keyrules/duplicates         {keys: [..], decision} — 이름 두 벌의 결정 (keys.json)
"""
import json
import random
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
KEYS_JSON = ROOT / "docgen" / "keys.json"


def _auto() -> dict:
    return json.loads(KEYS_JSON.read_text(encoding="utf-8")) if KEYS_JSON.exists() else {"keys": [], "duplicates": []}


def affected_forms(labels: list[str]) -> list[str]:
    """이 항목명들이 있는 overlay 서식 (켜면 생성 값이 바뀐다)."""
    from docgen import realform as RF

    want = {RF.norm(x).lower() for x in labels if x.strip()}
    if not want:
        return []
    out = []
    for lay in RF.all_layouts():
        if any(RF.norm(i.get("label", "")).lower() in want for i in lay.get("items", [])):
            out.append(f"hf{int(lay['no']):03d}" if str(lay.get("no", "")).isdigit() else str(lay.get("no")))
    return out


def make_router(guard) -> APIRouter:
    from docgen import keyrules as KR

    r = APIRouter()

    @r.get("/api/keyrules")
    def get_all():
        d, auto = KR.load(), _auto()
        rules: dict[str, list[str]] = {}
        for rx, k in d["label_rules"]:
            rules.setdefault(k, []).append(rx)
        rows = {}
        for k in auto.get("keys", []):
            rows[k["key"]] = {"key": k["key"], "labels": k.get("labels", [])[:5], "type": k.get("type"), "forms": k.get("forms", 0),
                              "groups": k.get("groups", [])}
        for k, v in d["keys"].items():
            rows.setdefault(k, {"key": k, "labels": [], "type": None, "forms": 0, "groups": []})["rule"] = v
        for k, rx in rules.items():
            rows.setdefault(k, {"key": k, "labels": [], "type": None, "forms": 0, "groups": []})["label_rules"] = rx
        used = {}
        for k, v in d["keys"].items():
            if v.get("kind"):
                used.setdefault(v["kind"], []).append(k)
        kinds = [{"name": n, "meaning": m, "how": "code", "keys": used.get(n, [])} for n, m in KR.CODE_KINDS.items()] + \
                [{"name": n, **v, "keys": used.get(n, [])} for n, v in d["kinds"].items()]
        return {"keys": sorted(rows.values(), key=lambda x: (-x["forms"], x["key"])), "kinds": kinds,
                "duplicates": auto.get("duplicates", []), "synonyms": d["synonyms"],
                "counts": {"keys": len(rows), "rules": len(d["keys"]) + len(rules),
                           "dup_open": sum(1 for x in auto.get("duplicates", []) if not x.get("decision"))}}

    @r.get("/api/keyrules/sources")
    def sources(seed: int = 0):
        from docgen.entities import make_profile

        return {"sources": KR.profile_sources(make_profile(seed))}

    class ExReq(BaseModel):
        kind: str | None = None
        definition: dict | None = None
        n: int = 10

    @r.post("/api/keyrules/examples")
    def examples(req: ExReq):
        from docgen.entities import make_profile

        def one(seed):
            p, rng = make_profile(seed), random.Random(f"keyrules:ex:{seed}")
            if req.definition:
                k = req.definition
                if k.get("how") == "source":
                    return KR.resolve_source(p, k.get("source") or "")
                if k.get("how") == "choices":
                    vals = list(k.get("choices") or {})
                    return rng.choices(vals, weights=[k["choices"][v] for v in vals])[0] if vals else None
                return KR.from_pattern(k.get("pattern") or "", rng)
            if req.kind in KR.load()["kinds"]:
                return KR.make_value(req.kind, p, rng)
            from docgen import realform as RF

            return RF.Values(p, rng, "기본").by_kind(req.kind or "text", "")
        return {"examples": [guard(one, s) for s in range(max(1, min(req.n, 30)))]}

    class KeyReq(BaseModel):
        meaning: str = ""
        kind: str | None = None
        source: str | None = None
        aliases: list[str] = []
        labels: list[str] = []
        label_suggestions: list[str] | None = None

    @r.put("/api/keyrules/keys/{key:path}")
    def put_key(key: str, req: KeyReq):
        d = json.loads(json.dumps(KR.load()))
        old = d["keys"].get(key, {})
        new = {"meaning": req.meaning.strip(), **({"kind": req.kind} if req.kind else {}), **({"source": req.source} if req.source else {}),
               "aliases": sorted({a.strip() for a in req.aliases if a.strip()}), "labels": [x.strip() for x in req.labels if x.strip()],
               "label_suggestions": req.label_suggestions if req.label_suggestions is not None else old.get("label_suggestions", [])}
        d["keys"][key] = new
        guard(KR.save, d)
        changed = sorted(set(new["labels"]) ^ set(old.get("labels", [])))
        return {"key": key, "rule": new, "affected": affected_forms(changed)}

    @r.delete("/api/keyrules/keys/{key:path}")
    def delete_key(key: str):
        d = json.loads(json.dumps(KR.load()))
        if key not in d["keys"]:
            raise HTTPException(404, key)
        old = d["keys"].pop(key)
        guard(KR.save, d)
        return {"deleted": key, "affected": affected_forms(old.get("labels", []))}

    class KindReq(BaseModel):
        meaning: str = ""
        how: str
        source: str | None = None
        choices: dict | None = None
        pattern: str | None = None

    @r.put("/api/keyrules/kinds/{name}")
    def put_kind(name: str, req: KindReq):
        d = json.loads(json.dumps(KR.load()))
        d["kinds"][name] = {"meaning": req.meaning.strip(), "how": req.how}
        if req.how in KR.HOW:   # 고른 방식의 칸만 남긴다
            d["kinds"][name][req.how] = getattr(req, req.how)
        guard(KR.save, d)
        return {"name": name, "kind": d["kinds"][name]}

    @r.delete("/api/keyrules/kinds/{name}")
    def delete_kind(name: str):
        d = json.loads(json.dumps(KR.load()))
        users = [k for k, v in d["keys"].items() if v.get("kind") == name]
        if users:
            raise HTTPException(400, f"이 값 종류를 쓰는 키가 있습니다: {users[:5]}")
        if d["kinds"].pop(name, None) is None:
            raise HTTPException(404, name)
        guard(KR.save, d)
        return {"deleted": name}

    class DupReq(BaseModel):
        keys: list[str]
        decision: str | None

    @r.put("/api/keyrules/duplicates")
    def put_dup(req: DupReq):
        auto = _auto()
        for x in auto.get("duplicates", []):
            if x["keys"] == req.keys:
                x["decision"] = (req.decision or "").strip() or None
                break
        else:
            raise HTTPException(404, "그 이름 두 벌이 없습니다")
        tmp = KEYS_JSON.with_suffix(".tmp")
        tmp.write_text(json.dumps(auto, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        tmp.replace(KEYS_JSON)
        return {"ok": True}

    return r
