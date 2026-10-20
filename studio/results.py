"""④ 가져오기 › 결과 폴더 (studio/RESULTS_FORMAT.md): 이미 OCR·추론을 돌려 저장해 둔 폴더를 읽어 묶음으로 만든다.
API 는 studio/api_review.py (검사)·api_import.py (묶음 만들기 kind: results), 화면은 static/js/import.js.

- 이미지·OCR 은 1부 OCR 준비 단계와 같은 규칙 (ocr/bank_ocr/data.py 의 scan·find_saved_ocr·parse_ocr).
- 묶음은 이미지 묶음과 같은 꼴(studio/importer.py)이고 출처만 "results". OCR 이 있는 쪽은 그 OCR 을 쓰고, 없는 쪽만 사내 OCR 을 부른다.
- 추론 결과 pred/<문서ID>.json 은 ⑤ 라벨 검수의 출발점이다 (studio/label_review.py). 결과 폴더에는 쓰지 않는다.

  python -m studio.results check <결과 폴더>      형식 검사 (문제를 한 번에 모두)
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

from . import importer as IM

FORMAT = "studio-results/1"
REQUIRED = ("format", "name", "real_data")


def _dir(root: Path, meta: dict, key: str, default: str) -> Path:
    p = Path(meta.get(key) or default)
    return p if p.is_absolute() else root / p


def flatten(obj, prefix="") -> list[dict]:
    """중첩 JSON 답 → 점 경로 항목 (위치 없음)."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            out += flatten(v, f"{prefix}{k}.")
    elif isinstance(obj, list) and obj and all(isinstance(x, dict) for x in obj):
        for i, v in enumerate(obj):
            out += flatten(v, f"{prefix}{i}.")
    else:
        out.append({"key": prefix[:-1], "value": obj})
    return out


def pred_items(pred: dict) -> list[dict]:
    if isinstance(pred.get("items"), list):
        return pred["items"]
    if "answer" in pred:
        return flatten(pred["answer"])
    return []


def check(path: str) -> dict:
    """결과 폴더 검사. {ok, errors, warnings, meta, docs: [{id, pages: [{id, image, ocr}], pred}], summary}."""
    from bank_ocr.data import find_saved_ocr, parse_ocr, scan

    root = Path(path).expanduser().resolve()
    errors, warnings = [], []
    if not (root / "meta.json").is_file():
        return {"ok": False, "errors": [f"{root}/meta.json 이 없습니다 (studio/RESULTS_FORMAT.md 2절)"], "warnings": [], "docs": []}
    try:
        meta = json.loads((root / "meta.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {"ok": False, "errors": [f"meta.json: {e}"], "warnings": [], "docs": []}
    for k in REQUIRED:
        if k not in meta:
            errors.append(f"meta.json: {k} 가 없습니다")
    if meta.get("format") not in (None, FORMAT):
        errors.append(f"meta.json: format 은 {FORMAT}")
    if not meta.get("document_regex") and not meta.get("single_page"):
        errors.append("meta.json: document_regex 또는 single_page:true 중 하나가 필요합니다")
    images, ocr_dir, pred_dir = _dir(root, meta, "images_dir", "images"), _dir(root, meta, "ocr_dir", "ocr"), _dir(root, meta, "pred_dir", "pred")
    mapping = meta.get("mapping") or json.loads((IM.OCR_DIR / "config.example.json").read_text(encoding="utf-8"))["mapping"]
    docs: dict[str, dict] = {}
    if not errors:
        try:
            rows = scan(images, "benchmark", meta.get("document_regex"), bool(meta.get("single_page")))
        except ValueError as e:
            errors.append(f"이미지: {e}")
            rows = []
        from PIL import Image

        for r in rows:
            rel = r["page_id"]
            doc_id = r["document_id"] if meta.get("document_regex") else re.sub(r"\.[^./]+$", "", rel)
            ocr = find_saved_ocr(ocr_dir, rel) if ocr_dir.is_dir() else None
            if ocr is not None:
                try:
                    with Image.open(r["image"]) as im:
                        w, h = im.size
                    parse_ocr(json.loads(ocr.read_text(encoding="utf-8")), w, h, mapping)
                except Exception as e:  # noqa: BLE001
                    errors.append(f"OCR {ocr.name}: {e}")
            docs.setdefault(doc_id, {"id": doc_id, "pages": []})["pages"].append(
                {"id": rel, "image": r["image"], "ocr": str(ocr) if ocr else None})
        n_no_ocr = sum(1 for d in docs.values() for p in d["pages"] if not p["ocr"])
        if n_no_ocr:
            warnings.append(f"OCR 파일이 없는 쪽 {n_no_ocr}개: studio 가 설정된 사내 OCR 로 읽습니다")
        for d in docs.values():
            pf = pred_dir / f"{d['id']}.json"
            if not pf.is_file():
                continue
            try:
                pred = json.loads(pf.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                errors.append(f"pred/{d['id']}.json: {e}")
                continue
            d["pred"] = str(pf)
            for i, it in enumerate(pred_items(pred)):
                if "key" not in it:
                    errors.append(f"pred/{d['id']}.json items[{i}]: key 가 없습니다")
                b = it.get("bbox_2d")
                if b is not None and (not isinstance(b, list) or len(b) != 4 or not all(0 <= v <= 1000 for v in b)):
                    errors.append(f"pred/{d['id']}.json items[{i}]: bbox_2d 는 0~1000 정수 4개")
                if b is not None and not 1 <= int(it.get("page", 1)) <= len(d["pages"]):
                    errors.append(f"pred/{d['id']}.json items[{i}]: page 는 1~{len(d['pages'])}")
        extra = {p.relative_to(pred_dir).with_suffix("").as_posix() for p in pred_dir.rglob("*.json")} - set(docs) if pred_dir.is_dir() else set()
        if extra:
            warnings.append(f"이미지가 없는 pred 파일 {len(extra)}개 (예: {sorted(extra)[:3]})")
        if not any("pred" in d for d in docs.values()):
            warnings.append("추론 결과(pred/)가 없습니다. 라벨 검수는 빈 라벨에서 시작합니다")
    bundles = root / "bundles.jsonl"
    nb = 0
    if bundles.is_file():
        for i, s in enumerate(bundles.read_text(encoding="utf-8").splitlines()):
            if not s.strip():
                continue
            b = json.loads(s)
            nb += 1
            miss = [x for x in b.get("documents", []) if x not in docs]
            if not b.get("bundle_id") or miss:
                errors.append(f"bundles.jsonl {i + 1}행: bundle_id 와 문서 ID 확인 (없는 문서 {miss[:3]})")
    errors = errors[:200]
    return {"ok": not errors, "errors": errors, "warnings": warnings, "meta": meta, "root": str(root), "mapping": mapping,
            "docs": list(docs.values()),
            "summary": {"documents": len(docs), "pages": sum(len(d["pages"]) for d in docs.values()),
                        "with_pred": sum(1 for d in docs.values() if "pred" in d), "bundles": nb}}


def create_batch(ws: Path, name: str, path: str, ocr: dict | None, import_dir: str | None = None) -> dict:
    """검사를 통과한 결과 폴더로 묶음을 만든다 (쪽 목록·저장된 OCR·추론 결과 위치). OCR·묶기는 작업으로."""
    res = check(path)
    if not res["ok"]:
        raise ValueError("결과 폴더 검사 실패: " + "; ".join(res["errors"][:5]))
    root = Path(res["root"])
    if import_dir and Path(import_dir).resolve() not in [root, *root.parents]:
        raise ValueError(f"결과 폴더는 설정의 import_dir ({import_dir}) 아래여야 합니다")
    bdir = ws / "imports" / IM._slug(name)
    if bdir.exists():
        raise ValueError(f"이미 있는 묶음 이름입니다: {IM._slug(name)}")
    (bdir / "pages").mkdir(parents=True)
    meta = res["meta"]
    rows = []
    for d in res["docs"]:
        for k, p in enumerate(d["pages"], 1):
            rows.append({"id": p["id"], "doc": d["id"], "source": p["image"], "page": k, **({"ocr_json": p["ocr"]} if p["ocr"] else {})})
    o = dict(ocr or {})
    o["mapping"] = res["mapping"]
    if all(p["ocr"] for d in res["docs"] for p in d["pages"]):   # 모든 쪽에 저장된 OCR: 사내 OCR 을 부를 일이 없다
        o.setdefault("revision", "saved-ocr:" + str(meta.get("ocr") or "results"))
    batch = {"name": bdir.name, "created": time.strftime("%Y-%m-%d %H:%M"), "source": {"kind": "results", "path": str(root)},
             "real_data": bool(meta.get("real_data")), "public": bool(meta.get("public", False)), "ocr": o, "stage": "listed",
             "results": {"model": meta.get("model"), "task": meta.get("task"), "ocr": meta.get("ocr"),
                         "pred": {d["id"]: d["pred"] for d in res["docs"] if d.get("pred")},
                         "bundles": str(root / "bundles.jsonl") if (root / "bundles.jsonl").is_file() else None}}
    IM._write_json(bdir / "batch.json", batch)
    IM._write_jsonl(bdir / "pages.jsonl", rows)
    return {**batch, "n_pages": len(rows), "summary": res["summary"], "warnings": res["warnings"]}


def main(argv=None) -> None:
    import argparse

    ap = argparse.ArgumentParser(prog="studio.results", description="결과 폴더 검사 (studio/RESULTS_FORMAT.md)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("folder")
    a = ap.parse_args(argv)
    res = check(a.folder)
    for e in res["errors"]:
        print("오류:", e)
    for w in res["warnings"]:
        print("주의:", w)
    print(json.dumps(res.get("summary", {}), ensure_ascii=False))
    sys.exit(0 if res["ok"] else 1)


if __name__ == "__main__":
    main()
