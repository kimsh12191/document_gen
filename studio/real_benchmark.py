"""실문서 벤치마크 작업. 가져오기·포맷 묶기·라벨 변환·문항 생성은 기존 기능을 쓴다.

작업 정의는 imports/<batch>/real_benchmark.json, 검수는 real_data/real_bench/<batch>에 둔다.
확정할 때 원본·추론·검수·질문을 복사하므로 이후 작업 수정은 확정 세트를 바꾸지 않는다.
"""
from __future__ import annotations

import hashlib
import json
import math
import mimetypes
import re
import shutil
import time
import uuid
from pathlib import Path
from urllib.parse import urlparse

from . import analyzers as AZ, importer as IM, label_review as LR, labeled_data as LD

TYPES = ("text", "amount", "number", "date", "checkbox", "seal", "signature")


def read(path, default=None):
    return json.loads(Path(path).read_text(encoding="utf-8")) if Path(path).exists() else default


def write(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(uuid.uuid4().hex + ".tmp")
    temp.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    temp.replace(path)


def doc_id(doc):
    return hashlib.sha256(doc.encode()).hexdigest()[:24]


def prediction_path(bdir, doc):
    return bdir / "pred" / (doc_id(doc) + ".json")


def prediction(bdir, doc):
    return read(prediction_path(bdir, doc))


def connection_config(ws, cfg):
    saved = read(Path(ws) / "real_benchmark_connections.json", {})
    return {**cfg, "ocr": saved.get("ocr", cfg.get("ocr")) or {},
            "providers": {**cfg.get("providers", {}), **saved.get("providers", {})}}


def public_connections(ws, cfg):
    c = connection_config(ws, cfg)
    return {"ocr": c["ocr"], "providers": {k: v for k, v in c["providers"].items()
                                           if v.get("kind") == "openai" and not v.get("external", True)}}


def _url(value):
    u = urlparse(value)
    if u.scheme not in ("http", "https") or not u.hostname or u.username or u.password:
        raise ValueError("접속 주소는 인증 정보를 포함하지 않는 http(s) 주소여야 합니다")
    return value.rstrip("/")


def save_connections(ws, cfg, ocr, providers):
    o = {**(connection_config(ws, cfg).get("ocr") or {}), **ocr}
    if o.get("base_url"):
        o["base_url"] = _url(o["base_url"])
    o.setdefault("callable", IM.OCR_CALLABLE)
    if o.get("base_url") and not str(o.get("revision", "")).strip():
        raise ValueError("OCR 버전을 입력하세요. 버전은 OCR 캐시를 구분합니다")
    clean = {}
    for name, p in providers.items():
        if not name.strip() or not str(p.get("model", "")).strip():
            raise ValueError("연결 이름과 모델 이름을 입력하세요")
        clean[name] = {"kind": "openai", "external": False, "base_url": _url(p.get("base_url", "")),
                       "model": p["model"], "api_key_env": p.get("api_key_env", ""),
                       "max_tokens": max(256, min(65536, int(p.get("max_tokens", 8192)))),
                       "timeout": max(5, min(1800, int(p.get("timeout", 300))))}
    write(Path(ws) / "real_benchmark_connections.json", {"ocr": o, "providers": clean})
    return public_connections(ws, cfg)


def initialize(bdir):
    write(bdir / "real_benchmark.json", {"schemas": {}, "snapshots": [], "jobs": [], "created": time.time()})


def work(bdir):
    w = read(bdir / "real_benchmark.json")
    if w is None:
        raise KeyError("실문서 벤치마크 작업이 없습니다")
    return w


def review_root(real_root, bdir):
    return Path(real_root) / "real_bench" / bdir.name


def review_path(real_root, bdir, doc):
    return review_root(real_root, bdir) / "reviews" / (doc_id(doc) + ".json")


def formats(bdir):
    return read(bdir / "formats.json", {"formats": []})["formats"]


def group(bdir, fid):
    return next((f for f in formats(bdir) if f["id"] == fid), None) or (_ for _ in ()).throw(KeyError(fid))


def schema_hash(schema):
    return hashlib.sha256(json.dumps(schema, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def save_schema(bdir, fid, name, fields):
    group(bdir, fid)
    if not name.strip() or not fields:
        raise ValueError("포맷 이름과 추출 항목을 입력하세요")
    keys, clean = set(), []
    for f in fields:
        key = str(f.get("key", "")).strip()
        if not re.fullmatch(r"[\w.-]+", key) or key in keys:
            raise ValueError("키는 중복 없이 글자·숫자·밑줄·점·하이픈으로 입력하세요")
        typ = f.get("type", "text")
        if typ not in TYPES:
            raise ValueError(f"지원하지 않는 타입: {typ}")
        label = str(f.get("label", "")).strip()
        if not label:
            raise ValueError(f"{key}: 찾을 내용 설명을 입력하세요")
        keys.add(key)
        clean.append({"key": key, "label": label, "type": typ})
    w = work(bdir)
    new = {"name": name.strip(), "fields": clean}
    old = w["schemas"].get(fid)
    # 질문이 바뀐 상태에서 예전 추론과 검수를 조용히 재사용하지 않는다.
    if old and old != new:
        if any(prediction_path(bdir, d).exists() for d in group(bdir, fid)["docs"]):
            raise ValueError("이미 추론한 포맷의 항목은 변경할 수 없습니다. 새 작업에서 다른 항목으로 만드세요")
    w["schemas"][fid] = new
    IM.set_decision(bdir, fid, None, name.strip())
    write(bdir / "real_benchmark.json", w)
    return new


def load_document(bdir, real_root, doc):
    rows = IM._jsonl(bdir / "pages.jsonl")
    pages = sorted((r for r in rows if r["doc"] == doc), key=lambda r: r["page"])
    if not pages:
        raise KeyError(doc)
    fmt = next((f for f in formats(bdir) if doc in f["docs"]), None)
    schema = work(bdir)["schemas"].get(fmt["id"]) if fmt else None
    if not schema:
        raise ValueError("먼저 포맷별 추출 항목을 저장하세요")
    rv = read(review_path(real_root, bdir, doc), {})
    pred = prediction(bdir, doc)
    fields = rv.get("fields") if rv else LR.pred_fields(pred, pages, {})
    spec = {f["key"]: f for f in schema["fields"]}
    for f in fields:
        if f["key"] in spec:
            f.update(type=spec[f["key"]]["type"], label=spec[f["key"]]["label"])
    status = rv.get("status") if rv.get("schema_hash") == schema_hash(schema) else ("in_progress" if rv else None)
    return {"doc": doc, "format": fmt["id"], "format_name": schema["name"], "doc_type": schema["name"],
            "pages": [{k: r[k] for k in ("id", "width", "height")} for r in pages], "fields": fields,
            "standard": schema["fields"], "status": status, "has_pred": pred is not None,
            "model": (pred or {}).get("model"), "raw": (pred or {}).get("raw", "")}


def save_document(bdir, real_root, doc, fields, done, by):
    cur = load_document(bdir, real_root, doc)
    standard = {f["key"]: f for f in cur["standard"]}
    clean, keys = [], set()
    original = {f["key"]: f.get("original") for f in LR.pred_fields(prediction(bdir, doc), cur["pages"], {})}
    for f in fields:
        key = str(f.get("key") or "").strip()
        if f.get("state") == "deleted":
            continue
        if key not in standard or key in keys:
            raise ValueError(f"정의하지 않았거나 중복된 키입니다: {key}")
        keys.add(key)
        typ, value = standard[key]["type"], f.get("value")
        if typ not in ("seal", "signature") and value is not None and (isinstance(value, (dict, list, bool))
                or not isinstance(value, (str, int, float)) or isinstance(value, float) and not math.isfinite(value)):
            raise ValueError(f"{key}: 값은 글자·숫자 또는 빈칸이어야 합니다")
        if typ in ("seal", "signature") and not isinstance(value, bool):
            raise ValueError(f"{key}: 있음/없음을 선택하세요")
        if typ == "checkbox_multi" and value is not None and not isinstance(value, list):
            raise ValueError(f"{key}: 복수 선택 값은 목록이어야 합니다")
        pg = int(f.get("page") or 0)
        if not 0 <= pg < len(cur["pages"]):
            raise ValueError(f"{key}: 쪽 번호가 범위를 벗어났습니다")
        box = f.get("bbox")
        active = value is not None and value != "" and value != [] and value is not False
        if box is not None:
            if not isinstance(box, list) or len(box) != 4 or not all(isinstance(v, (int, float)) and math.isfinite(v) for v in box):
                raise ValueError(f"{key}: 위치는 유한한 숫자 4개여야 합니다")
            p = cur["pages"][pg]
            if not (0 <= box[0] < box[2] <= p["width"] and 0 <= box[1] < box[3] <= p["height"]):
                raise ValueError(f"{key}: 박스가 이미지 범위를 벗어났습니다")
        if done and active and not box:
            raise ValueError(f"{key}: 값이 있는 항목의 위치를 그려주세요")
        g = {**standard[key], "value": None if value == "" else value, "page": pg, "bbox": box if active else None,
             "state": "confirmed" if done else f.get("state", "edited"), "original": original.get(key)}
        if typ in ("seal", "signature"):
            g["present"] = value
        clean.append(g)
    if done and keys != set(standard):
        raise ValueError("정의한 모든 항목을 확인하세요. 빈칸도 항목을 추가하고 값을 비워 두세요")
    write(review_path(real_root, bdir, doc), {"doc": doc, "fields": clean, "status": "done" if done else "in_progress",
          "schema_hash": schema_hash(work(bdir)["schemas"][cur["format"]]), "by": by, "at": time.strftime("%Y-%m-%d %H:%M:%S")})
    return {"status": "done" if done else "in_progress", "fields": len(clean)}


def summary(bdir, real_root):
    w = work(bdir)
    batch = read(bdir / "batch.json")
    rows = IM._jsonl(bdir / "pages.jsonl")
    fs = []
    for f in formats(bdir):
        docs = []
        for doc in f["docs"]:
            rv = read(review_path(real_root, bdir, doc), {})
            pred = prediction(bdir, doc)
            schema = w["schemas"].get(f["id"])
            status = rv.get("status") if schema and rv.get("schema_hash") == schema_hash(schema) else ("in_progress" if rv else None)
            docs.append({"doc": doc, "pages": f["docs"][doc], "status": status,
                         "has_pred": pred is not None, "model": (pred or {}).get("model")})
        schema = w["schemas"].get(f["id"])
        fs.append({**f, "documents": docs, "schema": schema, "prompt": prompt_for(schema) if schema else None,
                   "key_suggestion_job": w.get("key_suggestions", {}).get(f["id"]),
                   "done": sum(d["status"] == "done" for d in docs), "with_pred": sum(d["has_pred"] for d in docs)})
    return {"name": bdir.name, "created": batch["created"], "stage": batch["stage"], "pages": rows,
            "n_documents": len({r["doc"] for r in rows}), "formats": fs, "snapshots": w["snapshots"], "jobs": w["jobs"],
            "done": sum(f["done"] for f in fs), "with_pred": sum(f["with_pred"] for f in fs)}


def prompt_for(schema):
    from docgen.bench.prompts import P_KIE, kie_line

    items = "\n".join(kie_line(None, f["key"], f["label"], extra=f"타입: {f['type']}") for f in schema["fields"])
    return P_KIE.format(items=items) + "\n도장·서명은 true/false, 체크는 선택한 보기 글자로 답하세요. " \
        "각 키를 반드시 한 번씩 답하고, 빈칸·찾지 못한 값은 null로 답하세요. 추측하지 마세요."


def parse_items(text, schema, n_pages):
    from docgen.bench.metrics import parse_json

    raw = parse_json(text)
    if isinstance(raw, dict):
        raw = raw.get("items")
    if not isinstance(raw, list):
        raise ValueError("응답이 항목 JSON 목록이 아닙니다")
    std = {f["key"]: f for f in schema["fields"]}
    seen, result = set(), []
    for it in raw:
        if not isinstance(it, dict) or it.get("key") not in std or it["key"] in seen or "value" not in it:
            raise ValueError("응답에 중복·미정의 키 또는 값 없는 항목이 있습니다")
        key, value = it["key"], it["value"]
        typ = std[key]["type"]
        if typ not in ("seal", "signature") and value is not None and (isinstance(value, (dict, list, bool))
                or not isinstance(value, (str, int, float)) or isinstance(value, float) and not math.isfinite(value)):
            raise ValueError(f"{key}: 응답 값의 타입이 잘못되었습니다")
        if typ in ("seal", "signature") and not isinstance(value, bool):
            raise ValueError(f"{key}: 도장·서명 응답은 true/false여야 합니다")
        if typ == "checkbox_multi" and value is not None and not isinstance(value, list):
            raise ValueError(f"{key}: 복수 체크 응답은 목록이어야 합니다")
        if it.get("bbox_2d") is not None:
            box = it["bbox_2d"]
            page = it.get("page")
            if not isinstance(page, int) or not 1 <= page <= n_pages:
                raise ValueError(f"{key}: 응답의 쪽 번호가 잘못되었습니다")
            if not isinstance(box, list) or len(box) != 4 or not all(isinstance(x, (int, float)) and math.isfinite(x) for x in box) \
                    or not (0 <= box[0] < box[2] <= 1000 and 0 <= box[1] < box[3] <= 1000):
                raise ValueError(f"{key}: 응답의 좌표가 잘못되었습니다")
        result.append({**it, "type": typ, "label": std[key]["label"]})
        seen.add(key)
    if seen != set(std):
        raise ValueError("응답에서 일부 키가 빠졌습니다")
    return result


def vlm_completion(provider, images, prompt):
    """키 제안과 값 추출이 같은 이미지 전송·인증·길이 제한 처리를 사용한다."""
    import base64
    from urllib.request import Request, urlopen

    content = [{"type": "image_url", "image_url": {"url": "data:" + (mimetypes.guess_type(im)[0] or "image/png")
               + ";base64," + base64.b64encode(Path(im).read_bytes()).decode()}} for im in images]
    content.append({"type": "text", "text": prompt})
    body = {"model": provider["model"], "messages": [{"role": "user", "content": content}], "temperature": 0,
            "max_tokens": int(provider.get("max_tokens", 8192))}
    req = Request(provider["base_url"].rstrip("/") + "/chat/completions", data=json.dumps(body).encode(),
                  headers={"Content-Type": "application/json", **AZ._auth(provider)})
    with urlopen(req, timeout=int(provider.get("timeout", 300))) as res:
        response = json.loads(res.read())
    if response["choices"][0].get("finish_reason") == "length":
        raise ValueError("응답이 최대 길이에서 잘렸습니다. 최대 응답 길이를 늘리세요")
    return response["choices"][0]["message"]["content"]


def run_inference(request):
    """기존 분석기 연결·인증과 라벨 형식을 쓰고, 문서별 실패는 별도 보관한다."""
    bdir = Path(request["batch_dir"])
    p = request["provider_config"]
    failures, completed, skipped = {}, 0, 0
    for i, doc in enumerate(request["documents"], 1):
        out = prediction_path(bdir, doc["doc"])
        if out.exists():
            skipped += 1
            continue
        raw = ""
        try:
            prompt = prompt_for(doc["schema"])
            raw = vlm_completion(p, doc["images"], prompt)
            items = parse_items(raw, doc["schema"], len(doc["images"]))
            write(out, {"items": items, "raw": raw, "model": p["model"], "provider": request["provider"],
                        "prompt": prompt, "schema_hash": schema_hash(doc["schema"]), "settings": p,
                        "temperature": 0, "at": time.strftime("%Y-%m-%d %H:%M:%S")})
            completed += 1
        except Exception as e:
            failures[doc["doc"]] = {"error": f"{type(e).__name__}: {e}", "raw": raw}
            print(f"{doc['doc']}: {e}", flush=True)
        print(f"추론 {i}/{len(request['documents'])}", flush=True)
    result = {"completed": completed, "skipped": skipped, "failed": len(failures), "failures": failures}
    write(Path(request["result_path"]), result)
    return result


def finalize(bdir, real_root, reg, name, version, classify=False):
    if not name.strip() or not re.fullmatch(r"[\w.-]+", version):
        raise ValueError("벤치마크 이름과 버전(글자·숫자·점·밑줄·하이픈)을 입력하세요")
    slug = IM._slug(f"{name}-{version}")
    out = reg.ws / "datasets" / slug
    if out.exists():
        raise ValueError("같은 이름·버전의 출력이 있습니다. 새 버전을 지정하세요")
    info = summary(bdir, real_root)
    if not info["done"]:
        raise ValueError("검수 완료 문서가 없습니다")
    staging = reg.ws / "real_benchmark_exports" / uuid.uuid4().hex
    staging.mkdir(parents=True)
    documents = []
    for f in info["formats"]:
        for d in f["documents"]:
            if d["status"] != "done":
                continue
            cur = load_document(bdir, real_root, d["doc"])
            rv = read(review_path(real_root, bdir, d["doc"]))
            if rv["schema_hash"] != schema_hash(f["schema"]):
                raise ValueError("추출 항목이 바뀐 문서는 다시 검수해야 합니다")
            sid = doc_id(d["doc"])
            rows = LR._doc_rows(info["pages"], d["doc"])
            images = []
            for k, r in enumerate(rows):
                src = Path(r.get("image") or r["source"])
                rel = f"images/{sid}_p{k}{src.suffix}"
                dest = staging / rel
                dest.parent.mkdir(exist_ok=True)
                shutil.copyfile(src, dest)
                images.append(rel)
            converted = [LR._v1_field(g) for g in cur["fields"]]
            for raw, field in zip(cur["fields"], converted):
                if raw["type"] == "checkbox_multi" and raw.get("bbox"):
                    field["page"] = raw["page"]
            label = {"id": sid, "doc_type": f"real_{bdir.name}_{f['id']}", "doc_name": f["schema"]["name"], "images": images,
                     "pages": [{"width": r["width"], "height": r["height"]} for r in rows],
                     "fields": converted, "source": {"document": d["doc"], "batch": bdir.name}}
            write(staging / "labels" / (sid + ".json"), label)
            write(staging / "provenance" / (sid + ".json"), {"review": rv, "prediction": prediction(bdir, d["doc"]),
                                                            "schema": f["schema"]})
            documents.append({"label": label})
    write(staging / "meta.json", {"format": "docgen-labels/1", "gt": "reviewed", "real_data": True, "name": name, "version": version})
    files = {p.relative_to(staging).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in staging.rglob("*") if p.is_file()}
    report = {"source": str(staging), "documents": documents, "files": files, "meta": read(staging / "meta.json"),
              "bundles": [], "scenarios": {}, "fingerprint": hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()}
    out.mkdir(parents=True)
    LD.build_bank(report, out, ["kie", "marks"] + (["classify"] if classify else []), "test")
    ds = reg.register(str(out), f"{name} {version}", frozen=True, made_by_studio=True,
                      source="results", gt="reviewed", real_data=True, purpose=f"실문서 벤치마크 {bdir.name} / {version}")
    w = work(bdir)
    w["snapshots"].append({"dataset": ds["id"], "name": name, "version": version, "documents": len(documents),
                            "at": time.strftime("%Y-%m-%d %H:%M:%S")})
    write(bdir / "real_benchmark.json", w)
    return ds


if __name__ == "__main__":
    import sys

    request = read(Path(sys.argv[1]))
    if request.get("action") == "suggest_keys":
        from .key_suggestions import run as suggest_keys

        suggest_keys(request)
    else:
        run_inference(request)
