"""④ 서류 넣기 ❶ 넣기 (studio/DESIGN.md 15.2·15.3): 여러 장을 한 번에 넣는 폴더를 읽고 검사해 묶음을 만든다.
OCR(저장된 것 우선)·묶기는 가져오기와 같은 코드(studio/importer.py run_ocr·run_group)를 쓴다. 묶음에는 결과 폴더 묶음과 같은
batch["results"](추출 결과 위치)를 남겨 ⑤ 라벨 검수도 그대로 쓸 수 있다.

넣는 폴더 (단계는 빠져도 된다)
  images/<업무>/<건>/<서류>/p1.png …   또는 <서류>.pdf, <서류>.png — images/ 가 없으면 폴더 자체를 이미지 폴더로 본다
  ocr/<서류 경로>/<쪽>.json            (선택) 사내 OCR 응답. 1부 find_saved_ocr 규칙. PDF 는 ocr/<서류>/p<쪽>.json
  pred/<서류 경로>.json                 (선택) 추출 결과 (RESULTS_FORMAT.md 4절)
  cases.csv                             (선택) path,case,scenario — 서류 경로 → 건·업무. 있으면 폴더 단계보다 우선
  meta.json                             (선택) real_data(기본 true)·mapping·model·name

서류 = 이미지가 직접 든 폴더 중 파일 이름이 모두 쪽 번호꼴(p1·page_2·003)인 폴더, 또는 PDF 하나, 또는 이미지 한 장.
서류 위 단계는 가까운 쪽부터 건, 업무로 본다(한 단계뿐이면 건). 더 깊은 단계는 업무 이름 앞에 붙인다.

  python -m studio.intake check <폴더>
  python -m studio.intake score <묶음 폴더> <truth.json>    묶기 정확도 (studio/intake_testset.py 의 정답)
"""
from __future__ import annotations

import csv
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

from . import importer as IM
from .results import pred_items

PAGE_RE = re.compile(r"^(?:p|pg|page|쪽)?[_-]?0*(\d{1,4})$", re.I)


def _rel_parts(rel: str) -> tuple[str | None, str | None]:
    """서류 경로의 위 단계 → (업무, 건)."""
    up = rel.split("/")[:-1]
    if not up:
        return None, None
    if len(up) == 1:
        return None, up[0]
    return "/".join(up[:-1]), up[-1]


def find_docs(images: Path) -> list[dict]:
    """[{id, kind: pages|pdf|image, files: [쪽 파일…]}] — id 는 images 기준 경로 (pdf·image 는 확장자 뺀 것)."""
    docs, by_dir = [], {}
    for p in sorted(images.rglob("*")):
        if p.is_file() and p.suffix.lower() in IM.IMAGE_EXT:
            by_dir.setdefault(p.parent, []).append(p)
        elif p.is_file() and p.suffix.lower() == ".pdf":
            docs.append({"id": p.relative_to(images).with_suffix("").as_posix(), "kind": "pdf", "files": [p]})
    for d, files in by_dir.items():
        nums = [PAGE_RE.match(f.stem) for f in files]
        if d != images and all(nums):
            files = [f for _, f in sorted(zip((int(m.group(1)) for m in nums), files))]
            docs.append({"id": d.relative_to(images).as_posix(), "kind": "pages", "files": files})
        else:
            docs += [{"id": f.relative_to(images).with_suffix("").as_posix(), "kind": "image", "files": [f]} for f in files]
    return sorted(docs, key=lambda x: x["id"])


def _cases_csv(root: Path) -> dict[str, dict]:
    f = root / "cases.csv"
    if not f.is_file():
        return {}
    out = {}
    with f.open(encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            path = (row.get("path") or "").strip().strip("/")
            if path:
                out[re.sub(r"\.[^./]+$", "", path) if not path.endswith("/") else path] = {
                    "case": (row.get("case") or "").strip() or None, "scenario": (row.get("scenario") or "").strip() or None}
    return out


def check(path: str) -> dict:
    """넣을 폴더 검사. 문제를 한 번에 모두. {ok, errors, warnings, meta, root, mapping, docs, summary}."""
    from docgen.bench.ocr_data import find_saved_ocr, parse_ocr

    root = Path(path).expanduser().resolve()
    if not root.is_dir():
        return {"ok": False, "errors": [f"폴더가 없습니다: {root}"], "warnings": [], "docs": []}
    errors, warnings = [], []
    meta = {}
    if (root / "meta.json").is_file():
        try:
            meta = json.loads((root / "meta.json").read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"meta.json: {e}")
    images = root / (meta.get("images_dir") or "images")
    if not images.is_dir():
        images = root
    ocr_dir = root / (meta.get("ocr_dir") or "ocr")
    pred_dir = root / (meta.get("pred_dir") or "pred")
    mapping = meta.get("mapping") or json.loads(IM.OCR_CONFIG.read_text(encoding="utf-8"))["mapping"]
    skip = {ocr_dir, pred_dir} if images == root else set()
    found = [d for d in find_docs(images) if not any(s in d["files"][0].parents for s in skip)]
    if not found:
        errors.append(f"{images}: 이미지(png·jpg·tif…)나 PDF 가 없습니다")
    cases = _cases_csv(root)
    from PIL import Image

    docs = []
    for d in found:
        sc, case = _rel_parts(d["id"])
        if d["id"] in cases:
            case, sc = cases[d["id"]]["case"] or case, cases[d["id"]]["scenario"] or sc
        pages = []
        if d["kind"] == "pdf":
            import pymupdf

            try:
                with pymupdf.open(d["files"][0]) as pdf:
                    n = pdf.page_count
            except Exception as e:  # noqa: BLE001
                errors.append(f"{d['id']}.pdf: {e}")
                continue
            for k in range(1, n + 1):
                oj = ocr_dir / d["id"] / f"p{k}.json"
                pages.append({"id": f"{d['id']}.pdf#p{k}", "pdf": str(d["files"][0]), "page": k, "ocr": str(oj) if oj.is_file() else None})
        else:
            for k, f in enumerate(d["files"], 1):
                rel = f.relative_to(images).as_posix()
                oj = find_saved_ocr(ocr_dir, rel) if ocr_dir.is_dir() else None
                pages.append({"id": rel, "image": str(f), "page": k, "ocr": str(oj) if oj else None})
        for p in pages:
            if p["ocr"] and p.get("image"):
                try:
                    with Image.open(p["image"]) as im:
                        w, h = im.size
                    parse_ocr(json.loads(Path(p["ocr"]).read_text(encoding="utf-8")), w, h, mapping)
                except Exception as e:  # noqa: BLE001
                    errors.append(f"OCR {p['ocr']}: {e}")
        doc = {"id": d["id"], "kind": d["kind"], "scenario": sc, "case": case, "pages": pages}
        pf = pred_dir / f"{d['id']}.json"
        if pf.is_file():
            try:
                items = pred_items(json.loads(pf.read_text(encoding="utf-8")))
                doc["pred"] = str(pf)
                for i, it in enumerate(items):
                    b = it.get("bbox_2d")
                    if "key" not in it:
                        errors.append(f"pred/{d['id']}.json items[{i}]: key 가 없습니다")
                    if b is not None and (not isinstance(b, list) or len(b) != 4 or not all(0 <= v <= 1000 for v in b)):
                        errors.append(f"pred/{d['id']}.json items[{i}]: bbox_2d 는 0~1000 정수 4개")
                    if b is not None and not 1 <= int(it.get("page", 1)) <= len(pages):
                        errors.append(f"pred/{d['id']}.json items[{i}]: page 는 1~{len(pages)}")
            except json.JSONDecodeError as e:
                errors.append(f"pred/{d['id']}.json: {e}")
        docs.append(doc)
    ids = {d["id"] for d in docs}
    extra = {p.relative_to(pred_dir).with_suffix("").as_posix() for p in pred_dir.rglob("*.json")} - ids if pred_dir.is_dir() else set()
    if extra:
        warnings.append(f"이미지가 없는 pred 파일 {len(extra)}개 (예: {sorted(extra)[:3]})")
    n_pages = sum(len(d["pages"]) for d in docs)
    n_ocr = sum(1 for d in docs for p in d["pages"] if p["ocr"])
    if n_pages and n_ocr < n_pages:
        warnings.append(f"OCR 파일이 없는 쪽 {n_pages - n_ocr}개: 설정된 사내 OCR 로 읽습니다")
    n_pred = sum(1 for d in docs if "pred" in d)
    if docs and n_pred < len(docs):
        warnings.append(f"추출 결과가 없는 서류 {len(docs) - n_pred}개 (괜찮음 — 값 칸 초안이 덜 채워집니다)")
    has_case = sum(1 for d in docs if d["case"])
    has_sc = sum(1 for d in docs if d["scenario"])
    structure = "업무/건/서류" if docs and has_sc == len(docs) else "건/서류" if docs and has_case == len(docs) else \
        "구분 없음" if not has_case else "일부만 구분"
    if structure != "업무/건/서류":
        warnings.append(f"업무·건 구분: {structure} → 반영 단계에서 추정합니다 (DESIGN.md 15.5)")
    summary = {"documents": len(docs), "pages": n_pages, "with_ocr": n_ocr, "with_pred": n_pred, "structure": structure,
               "scenarios": len({d["scenario"] for d in docs if d["scenario"]}),
               "cases": len({(d["scenario"], d["case"]) for d in docs if d["case"]}),
               "pdf": sum(1 for d in docs if d["kind"] == "pdf"), "cases_csv": bool(cases)}
    return {"ok": not errors, "errors": errors[:200], "warnings": warnings, "meta": meta, "root": str(root), "images": str(images),
            "mapping": mapping, "docs": docs, "summary": summary}


def create_batch(ws: Path, name: str, path: str, ocr: dict | None, import_dir: str | None = None) -> dict:
    """검사를 통과한 폴더로 묶음을 만든다. PDF 는 쪽마다 그림으로 그린다. OCR·묶기는 작업(importer ocr)으로."""
    res = check(path)
    if not res["ok"]:
        raise ValueError("폴더 검사 실패: " + "; ".join(res["errors"][:5]))
    root = Path(res["root"])
    if import_dir and Path(import_dir).resolve() not in [root, *root.parents]:
        raise ValueError(f"넣을 폴더는 설정의 import_dir ({import_dir}) 아래여야 합니다")
    bdir = ws / "imports" / IM._slug(name)
    if bdir.exists():
        raise ValueError(f"이미 있는 묶음 이름입니다: {IM._slug(name)}")
    (bdir / "pages").mkdir(parents=True)
    rows = []
    for d in res["docs"]:
        for p in d["pages"]:
            src = p.get("image")
            if p.get("pdf"):
                import pymupdf

                out = bdir / "pages" / f"{p['id'].replace('/', '__').replace('#', '_')}.png"
                with pymupdf.open(p["pdf"]) as pdf:
                    pdf[p["page"] - 1].get_pixmap(matrix=pymupdf.Matrix(200 / 72, 200 / 72), alpha=False).save(str(out))
                src = str(out)
            rows.append({"id": p["id"], "doc": d["id"], "source": src, "page": p["page"], **({"ocr_json": p["ocr"]} if p["ocr"] else {})})
    meta = res["meta"]
    o = dict(ocr or {})
    o["mapping"] = res["mapping"]
    if all(p["ocr"] for d in res["docs"] for p in d["pages"]):   # 모든 쪽에 저장된 OCR: 사내 OCR 을 부를 일이 없다
        o.setdefault("revision", "saved-ocr:" + str(meta.get("ocr") or "intake"))
    batch = {"name": bdir.name, "created": time.strftime("%Y-%m-%d %H:%M"), "source": {"kind": "intake", "path": str(root)},
             "real_data": bool(meta.get("real_data", True)), "public": bool(meta.get("public", False)), "ocr": o, "stage": "listed",
             "results": {"model": meta.get("model"), "task": meta.get("task"), "ocr": meta.get("ocr"),
                         "pred": {d["id"]: d["pred"] for d in res["docs"] if d.get("pred")}, "bundles": None},
             "intake": {"summary": res["summary"], "warnings": res["warnings"],
                        "docs": {d["id"]: {"scenario": d["scenario"], "case": d["case"], "kind": d["kind"], "pages": len(d["pages"])}
                                 for d in res["docs"]}}}
    IM._write_json(bdir / "batch.json", batch)
    IM._write_jsonl(bdir / "pages.jsonl", rows)
    return {**batch, "n_pages": len(rows)}


def overview(bdir: Path) -> dict:
    """❷에 넘길 양식 요약: 양식마다 서류 수·쪽 수·업무 분포·추출 결과 있는 서류 수·가까운 기존 서식."""
    batch = json.loads((bdir / "batch.json").read_text(encoding="utf-8"))
    fx = json.loads((bdir / "formats.json").read_text(encoding="utf-8")) if (bdir / "formats.json").exists() else {"formats": []}
    docs = batch.get("intake", {}).get("docs", {})
    pred = batch.get("results", {}).get("pred", {})
    out = []
    for f in fx["formats"]:
        ds = list(f["docs"])
        out.append({"id": f["id"], "name": f["name"], "n_docs": len(ds), "n_pages": len(f["pages"]),
                    "scenarios": dict(Counter(docs.get(d, {}).get("scenario") or "-" for d in ds).most_common()),
                    "with_pred": sum(1 for d in ds if d in pred), "similar": f.get("similar", [])[:1],
                    "sample": f["pages"][0], "decision": f.get("decision")})
    out.sort(key=lambda x: -x["n_docs"])
    return {"batch": batch, "formats": out}


def score(bdir: Path, truth_path: Path) -> dict:
    """묶기 정확도 (정답 = intake_testset 의 truth.json). 서류는 structured 경로나 flat ID 로 찾는다.
    순도 = 양식마다 가장 많은 진짜 서식의 서류 수 합 / 전체, 쪼개짐 = 진짜 서식 하나가 몇 양식으로 나뉘었나(평균)."""
    truth = json.loads(truth_path.read_text(encoding="utf-8"))["documents"]
    by = {**truth, **{d["flat"]: d for d in truth.values()}}
    fx = json.loads((bdir / "formats.json").read_text(encoding="utf-8"))
    total = pure = 0
    split: dict[str, set] = {}
    rows = []
    for f in fx["formats"]:
        forms = Counter(by[d]["form"] for d in f["docs"] if d in by)
        if not forms:
            continue
        top, n = forms.most_common(1)[0]
        total += sum(forms.values())
        pure += n
        for form in forms:
            split.setdefault(form, set()).add(f["id"])
        rows.append({"format": f["id"], "name": f["name"], "docs": sum(forms.values()), "top": top, "purity": round(n / sum(forms.values()), 3),
                     "forms": dict(forms.most_common())})
    return {"documents": total, "formats": len(rows), "true_forms": len(split), "purity": round(pure / total, 4) if total else None,
            "split": round(sum(len(v) for v in split.values()) / len(split), 3) if split else None,
            "rows": sorted(rows, key=lambda r: r["purity"])}


def main(argv=None) -> None:
    import argparse

    ap = argparse.ArgumentParser(prog="python -m studio.intake", description="서류 넣기 (studio/DESIGN.md 15절)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("folder")
    s = sub.add_parser("score")
    s.add_argument("batch")
    s.add_argument("truth")
    a = ap.parse_args(argv)
    if a.cmd == "check":
        res = check(a.folder)
        for e in res["errors"]:
            print("오류:", e)
        for w in res["warnings"]:
            print("주의:", w)
        print(json.dumps(res.get("summary", {}), ensure_ascii=False))
        sys.exit(0 if res["ok"] else 1)
    r = score(Path(a.batch), Path(a.truth))
    print(json.dumps({k: v for k, v in r.items() if k != "rows"}, ensure_ascii=False))
    for row in r["rows"][:15]:
        if row["purity"] < 1:
            print(f"  {row['format']} {row['name']}: 순도 {row['purity']} {row['forms']}")


if __name__ == "__main__":
    main()
