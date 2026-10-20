"""④ 결과 폴더 · ⑤ 라벨 검수 API (studio/results.py, studio/label_review.py).

  POST /api/results/check                    결과 폴더 검사 {path}
  GET  /api/labels/{묶음}                      라벨 검수 첫 화면 (포맷마다 서식·진행·키 대응)
  GET/PUT /api/labels/{묶음}/keymap/{포맷}      키 대응 (모델 키 → 표준 키)
  GET  /api/labels/{묶음}/formats/{포맷}        먼저 볼 문서 순서 (빠진 키·위치 없는 값·OCR 에 없는 값)
  GET  /api/labels/{묶음}/keyview/{포맷}?key=   같은 자리 모아 보기
  GET/PUT /api/labels/{묶음}/doc?d=             문서 하나 검수 {fields, done}
  GET  /api/labels/{묶음}/crop?p=&box=          쪽 그림 한 부분 (같은 자리 모아 보기)
  GET  /api/labels/{묶음}/score                 검수 전 점수 (원래 추론 → 검수 결과)
  GET/PUT /api/labels/{묶음}/bundles            업무 묶음
  POST /api/labels/{묶음}/autolabel/{포맷}       내부 모델로 먼저 채우기 {provider, overwrite} → 분석기 작업 (⑧)
"""
import io
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from . import importer as IM
from . import label_review as LR
from . import results as RS


def make_router(reg, jobs, guard, cfg: dict, real_root: Path) -> APIRouter:
    r = APIRouter()
    imports = reg.ws / "imports"

    def bdir(name: str) -> Path:
        d = imports / IM._slug(name)
        if not (d / "batch.json").exists():
            raise HTTPException(404, f"묶음이 없습니다: {name}")
        return d

    class PathReq(BaseModel):
        path: str

    @r.post("/api/results/check")
    def check(req: PathReq):
        res = guard(RS.check, req.path)
        return {k: res.get(k) for k in ("ok", "errors", "warnings", "summary", "root")} | {"meta": res.get("meta")}

    @r.get("/api/labels/{name}")
    def overview(name: str):
        return {**guard(LR.overview, bdir(name), real_root), "real_root_set": bool(cfg.get("real_data_dir"))}

    @r.get("/api/labels/{name}/keymap/{fid}")
    def get_keymap(name: str, fid: str):
        return guard(LR.keymap_view, bdir(name), real_root, fid)

    class KeymapReq(BaseModel):
        mapping: dict

    @r.put("/api/labels/{name}/keymap/{fid}")
    def put_keymap(name: str, fid: str, req: KeymapReq):
        return guard(LR.save_keymap, bdir(name), real_root, fid, req.mapping)

    @r.get("/api/labels/{name}/formats/{fid}")
    def docs(name: str, fid: str):
        return {"docs": guard(LR.suspicious, bdir(name), real_root, fid)}

    @r.get("/api/labels/{name}/keyview/{fid}")
    def keyview(name: str, fid: str, key: str):
        return {"rows": guard(LR.key_view, bdir(name), real_root, fid, key)}

    @r.get("/api/labels/{name}/doc")
    def get_doc(name: str, d: str):
        return guard(LR.load_doc, bdir(name), real_root, d)

    class DocReq(BaseModel):
        fields: list[dict]
        done: bool = False

    @r.put("/api/labels/{name}/doc")
    def put_doc(name: str, d: str, req: DocReq):
        return guard(LR.save_doc, bdir(name), real_root, d, req.fields, req.done, cfg.get("user") or "studio")

    @r.get("/api/labels/{name}/crop")
    def crop(name: str, p: str, box: str):
        from PIL import Image

        row = next((x for x in IM._jsonl(bdir(name) / "pages.jsonl") if x["id"] == p), None)
        if row is None:
            raise HTTPException(404, "쪽이 없습니다")
        try:
            x0, y0, x1, y1 = (float(v) for v in box.split(","))
        except ValueError:
            raise HTTPException(400, "box=x0,y0,x1,y1")
        with Image.open(row.get("image") or row["source"]) as im:
            pad = (y1 - y0) * 0.6 + 6
            c = im.crop((max(0, int(x0 - pad * 2)), max(0, int(y0 - pad)), min(im.width, int(x1 + pad * 2)), min(im.height, int(y1 + pad))))
            c = c.convert("RGB")
            c.thumbnail((520, 160))
            buf = io.BytesIO()
            c.save(buf, "JPEG", quality=85)
        return Response(buf.getvalue(), media_type="image/jpeg")

    @r.get("/api/labels/{name}/score")
    def score(name: str):
        return guard(LR.score, bdir(name), real_root)

    @r.get("/api/labels/{name}/bundles")
    def get_bundles(name: str):
        return guard(LR.bundles, bdir(name), real_root)

    class BundlesReq(BaseModel):
        bundles: list[dict]

    @r.put("/api/labels/{name}/bundles")
    def put_bundles(name: str, req: BundlesReq):
        return {"saved": guard(LR.save_bundles, bdir(name), real_root, req.bundles)}

    class AutoReq(BaseModel):
        provider: str
        overwrite: bool = False

    @r.post("/api/labels/{name}/autolabel/{fid}")
    def autolabel(name: str, fid: str, req: AutoReq):
        import json as _json

        from . import analyzers as AZ
        from .jobs import python

        d = bdir(name)
        fx = _json.loads((d / "formats.json").read_text(encoding="utf-8"))
        f = next((x for x in fx["formats"] if x["id"] == fid), None)
        if f is None:
            raise HTTPException(404, fid)
        rows = IM._jsonl(d / "pages.jsonl")
        docs = [{"doc": doc, "pages": [x.get("image") or x["source"] for x in sorted((x for x in rows if x["doc"] == doc), key=lambda x: x.get("page", 1))]}
                for doc in (f.get("docs") or {})]
        keys = LR.form_keys(LR.doc_type_of(f))
        jd = guard(AZ.create_autolabel, reg.ws, cfg, req.provider, d, fid, docs, keys, req.overwrite)
        aid = jd.name
        j = jobs.start("analyzer", f"autolabel: {name} › {f['name']} ({req.provider}, 문서 {len(docs)})",
                       [python(), "-m", "studio.analyzers", "autolabel", str(jd)], lambda _j: AZ.validate_autolabel(jd), {"analyzer": aid})
        return {"analyzer": aid, "job": j["id"]}

    return r
