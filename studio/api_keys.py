"""값 종류 API: 영역 편집기의 "다른 서식에서도 쓰게 저장"이 만든 값 종류를 docgen/forms/_common/key_rules.json 의 "kinds" 에 둔다
(docgen/keyrules.py). 키는 서식마다 fields.json 에서 정한다 — 모든 서식에 걸치는 키 사전은 없다.

  PUT    /api/keyrules/kinds/{종류}      {meaning, how, source | choices | pattern}
  DELETE /api/keyrules/kinds/{종류}      (쓰는 키가 없을 때만)
"""
import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


def make_router(guard) -> APIRouter:
    from docgen import keyrules as KR

    r = APIRouter()

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

    return r
