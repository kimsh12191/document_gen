"""실문서 벤치마크 탭의 작업 API. 기존 imports·jobs·dataset 등록부를 공유한다."""
import shutil
import re
import threading
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from . import importer as IM, real_benchmark as RB, key_suggestions as KS
from .jobs import python


def make_router(reg, jobs, guard, cfg, real_root):
    r = APIRouter(prefix="/api/real-bench")
    lock = threading.RLock()

    def bdir(name):
        if name in (".", "..") or IM._slug(name) != name:
            raise HTTPException(404, "작업이 없습니다")
        d = reg.ws / "imports" / name
        guard(RB.work, d)
        return d

    def active(name):
        return [j for j in jobs.list() if j.get("info", {}).get("real_benchmark") == name and j["status"] == "running"]

    def idle(name):
        if active(name):
            raise HTTPException(409, "실행 중인 작업이 끝난 뒤 수정하세요")

    def start_ocr(d):
        return jobs.start("real_benchmark_ocr", f"실문서 OCR·포맷 묶기: {d.name}",
                          [python(), "-m", "studio.importer", "ocr", str(d)], info={"real_benchmark": d.name})

    @r.get("/connections")
    def connections():
        return RB.public_connections(reg.ws, cfg)

    class Connections(BaseModel):
        ocr: dict = Field(default_factory=dict)
        providers: dict = Field(default_factory=dict)

    @r.put("/connections")
    def save_connections(req: Connections):
        with lock:
            return guard(RB.save_connections, reg.ws, cfg, req.ocr, req.providers)

    class Check(BaseModel):
        kind: str
        provider: str = ""

    @r.post("/connections/check")
    def check_connection(req: Check):
        from urllib.request import urlopen

        c = RB.connection_config(reg.ws, cfg)
        if req.kind == "vlm":
            return guard(RB.AZ.check, c, req.provider)
        if req.kind != "ocr" or not c["ocr"].get("base_url"):
            raise HTTPException(400, "OCR 서버 주소를 먼저 저장하세요")
        try:
            with urlopen(c["ocr"]["base_url"].rstrip("/") + "/health", timeout=10) as res:
                return {"ok": res.status == 200, "detail": res.read(500).decode("utf-8", "replace")}
        except Exception as e:
            return {"ok": False, "detail": str(e)}

    @r.get("")
    def listing():
        data = []
        for p in sorted((reg.ws / "imports").glob("*/real_benchmark.json"), key=lambda p: p.stat().st_mtime, reverse=True):
            s = RB.summary(p.parent, real_root)
            data.append({k: s[k] for k in ("name", "created", "stage", "n_documents", "done", "with_pred", "snapshots")})
        return {"works": data, "connections": RB.public_connections(reg.ws, cfg)}

    def create(name, source, kind="folder"):
        if not name.strip() or IM._slug(name) in (".", ".."):
            raise ValueError("작업 이름을 입력하세요")
        c = RB.connection_config(reg.ws, cfg)
        if not c["ocr"].get("revision"):
            raise ValueError("연결 설정에서 OCR 서버와 버전을 먼저 설정하세요")
        src = Path(source)
        if not src.is_dir() or not any(p.is_file() and p.suffix.lower() in (*IM.IMAGE_EXT, ".pdf") for p in src.rglob("*")):
            raise ValueError("폴더에 가져올 이미지·PDF가 없습니다")
        c["ocr"].setdefault("cache_dir", str(reg.ws / "ocr_cache"))
        b = IM.create_batch(reg.ws, name, source, True, False, c["ocr"], cfg.get("import_dir") if kind == "folder" else None, kind)
        d = reg.ws / "imports" / b["name"]
        if not IM._jsonl(d / "pages.jsonl"):
            raise ValueError("가져올 이미지·PDF가 없습니다")
        RB.initialize(d)
        return {"name": b["name"], "job": start_ocr(d)["id"]}

    class Create(BaseModel):
        name: str
        path: str

    @r.post("")
    def create_folder(req: Create):
        with lock:
            return guard(create, req.name, req.path)

    @r.post("/upload")
    def upload(name: str = Form(...), files: list[UploadFile] = File(...)):
        with lock:
            if not name.strip() or IM._slug(name) in (".", ".."):
                raise HTTPException(400, "작업 이름을 입력하세요")
            if (reg.ws / "imports" / IM._slug(name)).exists():
                raise HTTPException(400, "같은 이름의 작업이 있습니다")
            filenames = [Path((f.filename or "").replace("\\", "/")).name for f in files]
            if not files or len(set(filenames)) != len(filenames) or any(Path(n).suffix.lower() not in (*IM.IMAGE_EXT, ".pdf") for n in filenames):
                raise HTTPException(400, "서로 다른 파일 이름의 이미지·PDF를 선택하세요")
            raw = reg.ws / "uploads" / ("real-" + uuid.uuid4().hex)
            raw.mkdir(parents=True)
            for f, filename in zip(files, filenames):
                with (raw / filename).open("wb") as out:
                    shutil.copyfileobj(f.file, out)
            return guard(create, name, str(raw), "upload")

    @r.get("/{name}")
    def detail(name: str):
        d = bdir(name)
        with lock:
            s = guard(RB.summary, d, real_root)
            s["jobs"] = [jobs.get(j["id"]) for j in jobs.list() if j.get("info", {}).get("real_benchmark") == name]
            return s

    @r.post("/{name}/ocr")
    def retry_ocr(name: str):
        with lock:
            d = bdir(name)
            idle(name)
            c = RB.connection_config(reg.ws, cfg)
            b = RB.read(d / "batch.json")
            # 이미 읽은 쪽은 보존하고 실패·미실행 쪽만 기존 OCR 작업이 처리한다.
            b["ocr"] = c["ocr"]
            RB.write(d / "batch.json", b)
            return {"job": start_ocr(d)["id"]}

    class Grouping(BaseModel):
        action: str
        src: str = ""
        dst: str = ""
        documents: list[str] = Field(default_factory=list)
        title: str = "새 포맷"

    @r.post("/{name}/grouping")
    def grouping(name: str, req: Grouping):
        with lock:
            d = bdir(name)
            idle(name)
            if RB.work(d)["schemas"]:
                raise HTTPException(400, "추출 항목을 저장하기 전에 포맷과 문서 묶음을 확정하세요")
            if req.action == "merge":
                if req.src == req.dst:
                    raise HTTPException(400, "서로 다른 포맷을 선택하세요")
                return guard(IM.merge_formats, d, req.src, req.dst)
            rows = IM._jsonl(d / "pages.jsonl")
            docs = set(req.documents)
            if not docs or not docs <= {row["doc"] for row in rows}:
                raise HTTPException(400, "문서를 선택하세요")
            pages = [row["id"] for row in rows if row["doc"] in docs]
            if req.action == "split":
                return guard(IM.split_pages, d, pages, req.title)
            if req.action == "document":
                if len(docs) < 2:
                    raise HTTPException(400, "이어 붙일 이미지 문서를 둘 이상 선택하세요")
                ordered = [row for row in rows if row["doc"] in docs]
                newdoc = "joined-" + uuid.uuid4().hex[:12]
                for i, row in enumerate(ordered, 1):
                    row.update(doc=newdoc, page=i)
                IM._write_jsonl(d / "pages.jsonl", rows)
                return guard(IM.run_group, d)
            raise HTTPException(400, "지원하지 않는 묶기 작업입니다")

    class Schema(BaseModel):
        name: str
        fields: list[dict]

    @r.put("/{name}/schemas/{fid}")
    def schema(name: str, fid: str, req: Schema):
        with lock:
            d = bdir(name)
            idle(name)
            return guard(RB.save_schema, d, fid, req.name, req.fields)

    class SuggestKeys(BaseModel):
        provider: str
        fields: list[dict] = Field(default_factory=list)
        document: str = ""

    @r.post("/{name}/schemas/{fid}/suggest-keys")
    def suggest_keys(name: str, fid: str, req: SuggestKeys):
        with lock:
            d = bdir(name)
            idle(name)
            p = guard(RB.AZ._provider, RB.connection_config(reg.ws, cfg), req.provider)
            if p["kind"] != "openai" or p.get("external", True):
                raise HTTPException(400, "내부 VLM 연결을 선택하세요")
            request = guard(KS.prepare, reg.ws, d, fid, req.provider, p, req.fields, req.document)
            token = uuid.uuid4().hex
            path = reg.ws / "real_benchmark_requests" / (token + ".json")
            request["result_path"] = str(path.with_suffix(".result.json"))
            RB.write(path, request)
            def done(_job):
                result = RB.read(Path(request["result_path"]))
                return {"key_suggestions": len(result["suggestions"]), "format": fid}
            j = jobs.start("real_benchmark_keys", f"실문서 항목·키 제안: {name} / {fid}",
                           [python(), "-m", "studio.real_benchmark", str(path)], done,
                           {"real_benchmark": name, "key_suggestions": token, "format": fid})
            w = RB.work(d)
            w.setdefault("key_suggestions", {})[fid] = j["id"]
            RB.write(d / "real_benchmark.json", w)
            return {"job": j["id"], "candidate_count": len(request["catalog"]), "catalog_total": request["catalog_total"]}

    @r.get("/{name}/key-suggestions/{job_id}")
    def key_suggestions(name: str, job_id: str):
        bdir(name)
        if not re.fullmatch(r"[\w-]+", job_id):
            raise HTTPException(404, "키 제안 작업이 없습니다")
        j = guard(jobs.get, job_id)
        token = j.get("info", {}).get("key_suggestions", "")
        if j.get("info", {}).get("real_benchmark") != name or not re.fullmatch(r"[0-9a-f]{32}", token):
            raise HTTPException(404, "이 작업의 키 제안이 아닙니다")
        result = RB.read(reg.ws / "real_benchmark_requests" / (token + ".result.json"), {})
        return {"job": job_id, "status": j["status"], "error": j.get("error") or (j.get("log_tail", "") if j["status"] != "done" else ""),
                **{k: v for k, v in result.items() if k not in ("raw", "prompt")}}

    @r.get("/{name}/doc")
    def document(name: str, doc: str):
        return guard(RB.load_document, bdir(name), real_root, doc)

    class Review(BaseModel):
        fields: list[dict]
        done: bool = False

    @r.put("/{name}/doc")
    def save_document(name: str, doc: str, req: Review):
        with lock:
            d = bdir(name)
            idle(name)
            return guard(RB.save_document, d, real_root, doc, req.fields, req.done, cfg.get("user") or "studio")

    class Infer(BaseModel):
        provider: str
        formats: list[str] = Field(default_factory=list)

    @r.post("/{name}/infer")
    def infer(name: str, req: Infer):
        with lock:
            d = bdir(name)
            idle(name)
            c = RB.connection_config(reg.ws, cfg)
            p = guard(RB.AZ._provider, c, req.provider)
            if p["kind"] != "openai" or p.get("external", True):
                raise HTTPException(400, "내부 VLM 연결을 선택하세요")
            w, rows = RB.work(d), IM._jsonl(d / "pages.jsonl")
            fs = [f for f in RB.formats(d) if not req.formats or f["id"] in req.formats]
            if not fs or any(f["id"] not in w["schemas"] for f in fs):
                raise HTTPException(400, "선택한 모든 포맷의 추출 항목을 먼저 저장하세요")
            docs = []
            for f in fs:
                for doc in f["docs"]:
                    if RB.prediction(d, doc) is None:
                        docs.append({"doc": doc, "schema": w["schemas"][f["id"]],
                                     "images": [r.get("image") or r["source"] for r in RB.LR._doc_rows(rows, doc)]})
            if not docs:
                raise HTTPException(400, "추론할 문서가 없습니다. 성공한 문서는 보존하며 실패·미실행 문서만 실행합니다")
            request_path = reg.ws / "real_benchmark_requests" / (uuid.uuid4().hex + ".json")
            result = str(request_path.with_suffix(".result.json"))
            RB.write(request_path, {"batch_dir": str(d), "provider": req.provider, "provider_config": p,
                                    "documents": docs, "result_path": result})
            j = jobs.start("real_benchmark_infer", f"실문서 추출: {name} ({len(docs)}건)",
                           [python(), "-m", "studio.real_benchmark", str(request_path)],
                           lambda _j: RB.read(Path(result)), {"real_benchmark": name})
            return {"job": j["id"]}

    class Finalize(BaseModel):
        name: str
        version: str = "v1"
        classify: bool = False

    @r.post("/{name}/finalize")
    def finalize(name: str, req: Finalize):
        with lock:
            d = bdir(name)
            idle(name)
            return guard(RB.finalize, d, real_root, reg, req.name, req.version, req.classify)

    return r
