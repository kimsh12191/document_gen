"""서류 넣기 시험용 외부 공개 문서 묶음 (studio/DESIGN.md 15.6): studio/testdata/external 의 원본(PDF·이미지)을
쪽 이미지 + 사내 OCR 형식 OCR + 추출 결과(라벨)로 만든다. studio/intake_testset.py 의 --external 이 합친다.

- 원본 목록·출처·라이선스: studio/testdata/external/sources.json (원본은 sources/, 라이선스 전문은 licenses/).
- OCR: PDF 는 글자층 단어 박스(pymupdf, 정답과 같음), 이미지는 미리 만들어 둔 OCR JSON(sources 의 *.ocr.json).
- 라벨: invoice2data 는 원래 정답 JSON 의 값, acroform 은 입력란 값, 나머지는 sources.json 에 적은 값. 키 이름은 출처 그대로
  (표준 키가 아니다 — 키 사전 대기 탭의 시험). 위치는 값 글자를 OCR 단어에서 찾아 붙이고, 못 찾으면 위치 없이 둔다.

  python -m studio.intake_external <out>      # <out>/images·ocr·pred/external/<종류>/<ID>/… + truth.json
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

from docgen.bench.metrics import normalize_box
from docgen.ocr_export import item, page_document

SRC = Path(__file__).resolve().parent / "testdata" / "external"
DPI = 150
MONTHS = {
    "en": ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"],
    "nl": ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"],
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
}


def _sq(s: str) -> str:
    return re.sub(r"\s+", "", s).lower()


def _alnum(s: str) -> str:
    return re.sub(r"[^0-9a-z가-힣]", "", s.lower())


def variants(v) -> list[str]:
    """값 하나가 문서에 찍혔을 법한 모양들 (숫자 소수점·자리 표시, 날짜 형식·달 이름)."""
    if isinstance(v, bool):
        return []
    if isinstance(v, (int, float)):
        x = float(v)
        out = [f"{x:.2f}", f"{x:,.2f}", f"{x:.2f}".replace(".", ","), f"{x:,.2f}".replace(",", " ").replace(".", ","),
               f"{x:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")]
        if x == int(x):
            out += [str(int(x)), f"{int(x):,}"]
        return list(dict.fromkeys(out))
    s = str(v).strip()
    out = [s]
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        d = date.fromisoformat(s)
        out += [d.strftime(f) for f in ("%d/%m/%Y", "%m/%d/%Y", "%d.%m.%Y", "%d-%m-%Y", "%d/%m/%y", "%d.%m.%y", "%Y/%m/%d", "%Y.%m.%d")]
        out += [f"{d.day}{c}{d.month}{c}{d.year}" for c in "-/."]
        for names in MONTHS.values():
            m = names[d.month - 1]
            for mm in (m, m[:3]):
                out += [f"{mm} {d.day}, {d.year}", f"{mm} {d.day:02d}, {d.year}", f"{d.day} {mm} {d.year}", f"{d.day:02d} {mm} {d.year}",
                        f"{d.day}. {mm} {d.year}", f"{mm}{d.day},{d.year}"]
    return list(dict.fromkeys(out))


def locate(value, words: list[dict]) -> list[float] | None:
    """값의 글자를 쪽 단어(읽는 순서)에서 찾아 박스를 돌려준다. 이어진 단어 최대 8개, 한 단어(줄) 안의 일부도."""
    for level in (_sq, _alnum):
        for c in (level(x) for x in variants(value)):
            if len(c) < 2:
                continue
            for i in range(len(words)):
                acc = ""
                for j in range(i, min(i + 8, len(words))):
                    acc += level(words[j]["text"])
                    if acc == c:
                        ws = words[i:j + 1]
                        return [min(w["bbox"][0] for w in ws), min(w["bbox"][1] for w in ws),
                                max(w["bbox"][2] for w in ws), max(w["bbox"][3] for w in ws)]
                    if len(acc) >= len(c):
                        break
            for w in words:   # 줄 단위 OCR: 줄 안의 일부면 글자 비율로 자른다
                t = level(w["text"])
                k = t.find(c)
                if k >= 0 and len(t) > len(c) and len(c) >= 4:
                    x0, y0, x1, y1 = w["bbox"]
                    return [x0 + (x1 - x0) * k / len(t), y0, x0 + (x1 - x0) * (k + len(c)) / len(t), y1]
    return None


def pdf_pages(path: Path, out_dir: Path) -> tuple[list[Path], list[list[dict]], list]:
    import pymupdf

    doc = pymupdf.open(path)
    z = DPI / 72
    paths, words, widgets = [], [], []
    for k, page in enumerate(doc):
        p = out_dir / f"p{k + 1}.png"
        p.parent.mkdir(parents=True, exist_ok=True)
        page.get_pixmap(matrix=pymupdf.Matrix(z, z), alpha=False).save(str(p))
        lines: dict = {}
        ws = []
        for x0, y0, x1, y1, t, b, ln, _ in page.get_text("words", sort=True):
            ws.append({"text": t, "bbox": [x0 * z, y0 * z, x1 * z, y1 * z], "line": lines.setdefault((b, ln), len(lines))})
        ws += image_words(page, z, len(lines) + len(ws))
        wg = [(w.field_name, w.field_type_string, w.field_value, [v * z for v in w.rect]) for w in page.widgets() or []]
        for name, typ, val, r in wg:   # 입력란에 넣은 값은 글자층에 없으므로 OCR 에 더한다
            if typ == "Text" and val:
                ws.append({"text": str(val), "bbox": r, "line": len(lines) + len(ws)})
        paths.append(p)
        words.append(ws)
        widgets.append(wg)
    return paths, words, widgets


def image_words(page, z: float, line0: int) -> list[dict]:
    """PDF 안 그림에 든 글자 (글자층에 없음). 로컬 OCR(rapidocr_onnxruntime)이 있을 때만 — 묶음을 다시 만들 때 필요하다."""
    try:
        from rapidocr_onnxruntime import RapidOCR
    except ImportError:
        return []
    import numpy as np
    import pymupdf
    from PIL import Image

    global _OCR
    _OCR = globals().get("_OCR") or RapidOCR()
    out = []
    for info in page.get_image_info():
        r = pymupdf.Rect(info["bbox"]) & page.rect
        if r.width < 40 or r.height < 20:
            continue
        pix = page.get_pixmap(matrix=pymupdf.Matrix(z * 2, z * 2), clip=r, alpha=False)
        img = np.array(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
        for box, text, score in _OCR(img)[0] or []:
            xs, ys = [q[0] for q in box], [q[1] for q in box]
            out.append({"text": text, "conf": round(float(score), 3), "line": line0 + len(out),
                        "bbox": [r.x0 * z + min(xs) / 2, r.y0 * z + min(ys) / 2, r.x0 * z + max(xs) / 2, r.y0 * z + max(ys) / 2]})
    return out


def image_page(path: Path, ocr_json: Path, out_dir: Path) -> tuple[list[Path], list[list[dict]]]:
    import shutil

    p = out_dir / f"p1{path.suffix.lower()}"
    p.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, p)
    oj = json.loads(ocr_json.read_text(encoding="utf-8"))
    ws = [{"text": it["text"], "line": it.get("line_num", 0),
           "bbox": [it["bounding"]["vertices"][0]["x"], it["bounding"]["vertices"][0]["y"],
                    it["bounding"]["vertices"][2]["x"], it["bounding"]["vertices"][2]["y"]], "conf": it["confidence"]}
          for it in oj["data"]["basicData"][0]]
    return [p], [ws]


def labels_of(doc: dict, src: Path, widgets: list) -> list[tuple[str, object, str | None]]:
    """(키, 값, 종류) 목록. 종류는 checkbox 만 붙인다."""
    how = doc["labels"]
    if how == "invoice2data":
        gt = json.loads((src / "sources" / Path(doc["file"]).with_suffix(".json")).read_text(encoding="utf-8"))
        gt = gt[0] if isinstance(gt, list) else gt
        return [(k, v, None) for k, v in gt.items() if k != "desc" and not isinstance(v, (list, dict)) and str(v).strip()]
    if how == "acroform":
        out = []
        for pg in widgets:
            for name, typ, val, _ in pg:
                if typ == "Text" and val:
                    out.append((name, val, None))
                elif typ == "CheckBox" and val not in ("", "Off", None):
                    out.append((name, val, "checkbox"))
        return out
    if isinstance(how, dict):
        return [(k, v, None) for k, v in how.items()]
    return []


def build(out: Path, src: Path = SRC, log=print) -> dict:
    meta = json.loads((src / "sources.json").read_text(encoding="utf-8"))
    truth = {"documents": {}, "placement": meta["placement"]}
    for d in meta["documents"]:
        repo = meta["repos"][d["repo"]]
        f = src / "sources" / d["file"]
        rel = f"external/{d['kind']}/{d['id']}"
        if f.suffix.lower() == ".pdf":
            paths, words, widgets = pdf_pages(f, out / "images" / rel)
        else:
            paths, words = image_page(f, src / "sources" / d["ocr"], out / "images" / rel)
            widgets = []
        from PIL import Image

        sizes = [Image.open(p).size for p in paths]
        for k, (p, ws) in enumerate(zip(paths, words), 1):
            oj = page_document([item(w["text"], w["bbox"], w.get("conf", 0.99), w["line"]) for w in ws], p.name)
            q = out / "ocr" / rel / f"p{k}.json"
            q.parent.mkdir(parents=True, exist_ok=True)
            q.write_text(json.dumps(oj, ensure_ascii=False), encoding="utf-8")
        items, found = [], 0
        for key, val, typ in labels_of(d, src, widgets):
            it = {"key": key, "value": str(val), **({"type": typ} if typ else {})}
            if typ == "checkbox":
                r = next((w[3] for pg in widgets for w in pg if w[0] == key), None)
                pg = next((i for i, pgw in enumerate(widgets) if any(w[0] == key for w in pgw)), 0)
            else:
                r, pg = None, 0
                for pg, ws in enumerate(words):
                    if (r := locate(val, ws)) is not None:
                        break
            if r is not None:
                it.update(bbox_2d=normalize_box(r, *sizes[pg]), page=pg + 1)
                found += 1
            items.append(it)
        if items:
            q = out / "pred" / f"{rel}.json"
            q.parent.mkdir(parents=True, exist_ok=True)
            q.write_text(json.dumps({"items": items}, ensure_ascii=False, indent=1), encoding="utf-8")
        name = Path(d["file"]).name
        truth["documents"][rel] = {   # form: 같은 발행처의 같은 양식은 sources.json 의 format 으로 묶는다
            "form": f"ext:{d.get('format') or d['id']}", "name": d["id"], "role": f"external_{d['kind']}", "kind": d["kind"], "pages": len(paths),
            "condition": "external", "pred": bool(items), "pred_errors": [], "boxes": f"{found}/{len(items)}",
            "source": f"{repo['url']}/blob/{repo['commit']}/{repo['path']}/{name}" if d["repo"] != "docling"
            else f"{repo['url']}/blob/{repo['commit']}/{repo['path']}/{'ocr' if f.suffix != '.pdf' else 'pdf'}/sources/{name}",
            "license": repo["license"], "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
        log(f"{rel}: 쪽 {len(paths)} · 라벨 {len(items)} (위치 {found})")
    (out / "truth.json").write_text(json.dumps(truth, ensure_ascii=False, indent=1), encoding="utf-8")
    return truth


def main(argv=None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        sys.exit(__doc__)
    build(Path(argv[0]))


if __name__ == "__main__":
    main()
