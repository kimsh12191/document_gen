"""⑥ 데이터셋 · ⑦ 평가 API (studio/datasets.py 를 부른다).

  GET    /api/datasets                       등록부 목록
  POST   /api/datasets                       폴더 등록 {path, name, source?, gt?, real_data?}
  GET    /api/datasets/{id}                  데이터셋 하나: 정보, 모델 답 목록, 저장한 점수, 설명서
  DELETE /api/datasets/{id}                  등록만 지운다 (폴더는 그대로)
  PATCH  /api/datasets/{id}                  이름·출처·정답 종류·실서류 여부
  POST   /api/datasets/{id}/freeze           고정 {frozen}
  PUT    /api/datasets/{id}/card             설명서의 사람 칸 {purpose, limits, not_for}
  GET    /api/datasets/{id}/items            문항 {task, offset, limit, pids, order=id|worst, q}
  GET    /api/datasets/{id}/file?p=          문항 이미지
  POST   /api/datasets/{id}/runs             모델 답 붙이기 {path, label}
  POST   /api/datasets/{id}/score            채점 {pid}
  GET    /api/datasets/{id}/reports          파이프라인이 낸 점수 파일
  GET    /api/compare?ids=a,b                데이터셋들의 저장한 점수 비교표
"""

import json
import time
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel

from . import datasets as DS


def make_router(reg: DS.Registry, guard, jobs=None) -> APIRouter:
    r = APIRouter()
    scores_dir = reg.ws / "scores"

    def ds_or_404(ds_id: str) -> dict:
        try:
            return reg.get(ds_id)
        except KeyError:
            raise HTTPException(404, f"등록되지 않은 데이터셋: {ds_id}")

    def saved_scores(ds_id: str) -> list[dict]:
        d = scores_dir / ds_id
        out = []
        for f in sorted(d.glob("*.json")) if d.exists() else []:
            s = json.loads(f.read_text(encoding="utf-8"))
            out.append({k: s[k] for k in ("pid", "label", "run", "path", "scored_at", "n", "answered", "main", "reference_type")
                        if k in s})
        return out

    def card_path(ds: dict) -> Path:
        return (Path(ds["path"]) / "DATASET.md") if not ds.get("registered") else (reg.ws / "cards" / f"{ds['id']}.md")

    def write_card(ds: dict) -> str:
        trainings = [t for t in reg.load().get("trainings", []) if ds["id"] in t.get("datasets", [])]
        md = DS.card_markdown(ds, saved_scores(ds["id"]), trainings)
        if ds.get("frozen") and card_path(ds).exists() and not ds.get("registered"):
            return card_path(ds).read_text(encoding="utf-8")   # 고정한 데이터셋은 자동 칸을 다시 쓰지 않는다
        p = card_path(ds)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(md, encoding="utf-8")
        return md

    @r.get("/api/datasets")
    def list_datasets():
        if jobs is not None:
            from .build_registration import recover_completed

            guard(recover_completed, jobs, reg)
        d = reg.load()
        out = []
        for k, v in d["datasets"].items():
            out.append({"id": k, **{x: v.get(x) for x in ("name", "track", "format", "source", "gt", "real_data", "frozen",
                                                         "version", "counts", "created", "registered", "path")},
                        "exists": Path(v["path"]).exists(), "n_runs": len(v.get("runs", [])),
                        "n_scores": len(saved_scores(k))})
        return {"datasets": out, "workspace": str(reg.ws), "sources": DS.SOURCE_NAME, "gts": DS.GT_NAME}

    class RegisterReq(BaseModel):
        path: str
        name: str = ""
        source: str | None = None
        gt: str | None = None
        real_data: bool | None = None

    @r.post("/api/datasets")
    def register(req: RegisterReq):
        meta = {k: v for k, v in req.model_dump().items() if k not in ("path", "name") and v is not None}
        ds = guard(reg.register, req.path, req.name, **meta)
        write_card(ds)
        return ds

    @r.get("/api/datasets/{ds_id}")
    def get_dataset(ds_id: str):
        ds = ds_or_404(ds_id)
        preds = guard(DS.predictions_of, ds)
        return {**ds, "exists": Path(ds["path"]).exists(), "predictions": preds, "scores": saved_scores(ds_id),
                "tasks": {t: len(v) for t, v in guard(DS.items, ds).items()} if Path(ds["path"]).exists() else {},
                "card_md": write_card(ds), "card_file": str(card_path(ds))}

    @r.delete("/api/datasets/{ds_id}")
    def unregister(ds_id: str):
        guard(reg.unregister, ds_id)
        return {"ok": True}

    @r.patch("/api/datasets/{ds_id}")
    def patch(ds_id: str, req: dict):
        return guard(reg.set_meta, ds_id, req)

    class FreezeReq(BaseModel):
        frozen: bool = True

    @r.post("/api/datasets/{ds_id}/freeze")
    def freeze(ds_id: str, req: FreezeReq):
        ds = guard(reg.set_frozen, ds_id, req.frozen)
        write_card(ds)
        return ds

    @r.put("/api/datasets/{ds_id}/card")
    def card(ds_id: str, req: dict):
        ds = guard(reg.set_card, ds_id, req)
        return {"card_md": write_card(ds)}

    @r.get("/api/datasets/{ds_id}/card.md", response_class=PlainTextResponse)
    def card_md(ds_id: str):
        return write_card(ds_or_404(ds_id))

    def _per_item(ds_id: str, pid: str) -> dict:
        f = scores_dir / ds_id / f"{pid}.json"
        return json.loads(f.read_text(encoding="utf-8")).get("per_item", {}) if f.exists() else {}

    @r.get("/api/datasets/{ds_id}/items")
    def list_items(ds_id: str, task: str = "", offset: int = 0, limit: int = 20, pids: str = "", order: str = "id", q: str = ""):
        ds = ds_or_404(ds_id)
        by_task = guard(DS.items, ds)
        if task and task not in by_task:
            raise HTTPException(404, f"과제가 없습니다: {task}")
        rows = by_task[task] if task else [x for v in by_task.values() for x in v]
        if q:
            rows = [x for x in rows if q.lower() in json.dumps(x, ensure_ascii=False).lower()]
        pid_list = [p for p in pids.split(",") if p]
        known = {p["pid"]: p for p in DS.predictions_of(ds)}
        per = {p: _per_item(ds_id, p) for p in pid_list}
        if order == "worst" and pid_list:   # 첫 번째 답의 문항 점수가 낮은 것부터 (점수 없는 문항은 뒤)
            sc = per[pid_list[0]]
            rows = sorted(rows, key=lambda x: (sc.get(x["id"]) is None, sc.get(x["id"]) if sc.get(x["id"]) is not None else 0))
        page = rows[offset: offset + limit]
        answers = {p: DS.load_pred(known[p]["path"]) for p in pid_list if p in known}
        out = []
        for it in page:
            v = DS.view_item(ds, it)
            v["preds"] = [{"pid": p, "label": known[p]["label"], "output": answers[p].get(it["id"]),
                           "score": per[p].get(it["id"])} for p in pid_list if p in known]
            out.append(v)
        return {"total": len(rows), "offset": offset, "items": out}

    @r.get("/api/datasets/{ds_id}/file")
    def file(ds_id: str, p: str):
        ds = ds_or_404(ds_id)
        f = reg.resolve_file(ds, p)
        if f is None or not reg.allowed(ds, f):
            raise HTTPException(404, "파일을 찾을 수 없습니다")
        return FileResponse(f)

    class RunReq(BaseModel):
        path: str
        label: str = ""

    @r.post("/api/datasets/{ds_id}/runs")
    def attach(ds_id: str, req: RunReq):
        return guard(reg.attach_run, ds_id, req.path, req.label)

    class ScoreReq(BaseModel):
        pid: str

    @r.post("/api/datasets/{ds_id}/score")
    def score(ds_id: str, req: ScoreReq):
        ds = ds_or_404(ds_id)
        pred = next((p for p in DS.predictions_of(ds) if p["pid"] == req.pid), None)
        if pred is None:
            raise HTTPException(404, "모델 답을 찾을 수 없습니다")
        t0 = time.time()
        s = guard(DS.score, ds, DS.load_pred(pred["path"]))
        s.update(pid=pred["pid"], label=pred["label"], run=pred["run"], path=pred["path"],
                 scored_at=time.strftime("%Y-%m-%d %H:%M"), seconds=round(time.time() - t0, 2))
        (scores_dir / ds_id).mkdir(parents=True, exist_ok=True)
        (scores_dir / ds_id / f"{pred['pid']}.json").write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")
        write_card(ds)
        return {k: v for k, v in s.items() if k != "per_item"}

    @r.get("/api/datasets/{ds_id}/reports")
    def reports(ds_id: str):
        ds = ds_or_404(ds_id)
        out = []
        for p in DS.predictions_of(ds):
            for f in DS.report_files(p):
                try:
                    data = json.loads(Path(f["path"]).read_text(encoding="utf-8"))
                except ValueError:
                    continue
                tasks = data.get("tasks", data)
                out.append({"pid": p["pid"], "label": p["label"], "file": f["path"], "name": f["name"],
                            "model_label": data.get("model_label") or data.get("label"),
                            "tasks": {t: m for t, m in tasks.items() if isinstance(m, dict)}})
        uniq = {o["file"]: o for o in out}
        return {"reports": list(uniq.values())}

    @r.get("/api/compare")
    def compare(ids: str):
        out = []
        for ds_id in [x for x in ids.split(",") if x]:
            ds = ds_or_404(ds_id)
            for s in saved_scores(ds_id):
                out.append({"dataset": ds_id, "dataset_name": ds["name"], "track": ds["track"], "source": ds["source"],
                            "gt": ds["gt"], "real_data": ds.get("real_data"), **s})
        return {"rows": out}

    return r
