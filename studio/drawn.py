"""그려서 만드는 overlay 서식: 서식 그림(PNG·JPG·PDF)을 올리면 OCR 없이 그 그림을 배경으로 하는 image 서식 img_* 를 만든다.
칸은 비어 있고, 사람이 영역 편집기에서 칸을 그리고 항목명·키·값 출처를 붙인다 (guide/new-forms.md "그림 위에 그려서 만들기").

서식 폴더 꼴은 image 서식 img_* 그대로다. 다른 점:
  - 만들 때 OCR 을 부르지 않는다. 배경 글자(layout.json texts)는 영역 편집기에서 사내 OCR 로 읽어 채운다 (아래 read_texts).
    채우지 않으면 합성 OCR 세트(docgen.ocr_set)에서는 빠진다 (쪽 전체 글자 정답을 만들 수 없음).
    문서 이해 과제(분류·kie·표·체크 …)는 칸만으로 만들어진다.
  - 쪽 크기를 A4 에 맞춘다: 긴 변이 A4 긴 변(842pt)이 되게 그림을 줄이거나 키운다. 그림 해상도가 달라도 값 글자 크기가 서류다워진다.

실서류 견본(값이 적힌 서류)에서 만든 서식은 사내 서식 폴더(private_forms_dir)에만 둔다. 빈 서식·공개 서식만 저장소 docgen/forms/<ID>/.
"""
from __future__ import annotations

import io
import json
import re
import shutil
import time
from pathlib import Path

ID_RX = re.compile(r"img_[a-z0-9_]{2,40}")
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}
A4_LONG_PT = 842.0
MAX_PAGES = 20
MAX_BYTES = 40 * 1024 * 1024   # 올린 파일 하나


def _pages(files: list[tuple[str, bytes]]) -> list[tuple[str, "object"]]:
    """올린 파일들 → 쪽 그림 [(출처 이름, PIL 그림)]. 파일 순서대로, PDF 는 쪽마다 200dpi."""
    from PIL import Image, ImageOps

    out = []
    for name, data in files:
        ext = Path(name).suffix.lower()
        if len(data) > MAX_BYTES:
            raise ValueError(f"{name}: 파일이 너무 큽니다 ({len(data) // 1024 // 1024}MB, 최대 {MAX_BYTES // 1024 // 1024}MB)")
        if ext == ".pdf":
            import pymupdf

            with pymupdf.open(stream=data, filetype="pdf") as doc:
                for k, page in enumerate(doc):
                    pix = page.get_pixmap(matrix=pymupdf.Matrix(200 / 72, 200 / 72), alpha=False)
                    out.append((f"{name}#p{k + 1}", Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")))
        elif ext in IMAGE_EXT:
            try:
                im = Image.open(io.BytesIO(data))
                im = ImageOps.exif_transpose(im).convert("RGB")   # 사진의 회전 정보를 적용
            except Exception as e:  # noqa: BLE001
                raise ValueError(f"{name}: 그림을 읽지 못했습니다 ({e})") from e
            out.append((name, im))
        else:
            raise ValueError(f"{name}: PNG·JPG·TIF·BMP·WEBP 그림이나 PDF 만 올릴 수 있습니다")
    if not out:
        raise ValueError("올린 그림이 없습니다")
    if len(out) > MAX_PAGES:
        raise ValueError(f"쪽이 너무 많습니다 ({len(out)}쪽, 최대 {MAX_PAGES}쪽)")
    return out


def create(files: list[tuple[str, bytes]], form_id: str, name: str, real_data: bool, private_dir: str | None) -> dict:
    """서식 그림 → 빈 overlay(image) 서식 폴더 + 등록. {form_id, dir, private, pages}."""
    from docgen import formdir
    from docgen import overrides as OV
    from docgen import realform as RF
    from docgen.registry import load_all

    form_id, name = (form_id or "").strip(), (name or "").strip()
    if not ID_RX.fullmatch(form_id):
        raise ValueError("서식 ID 는 img_ 로 시작하는 영어 소문자·숫자·밑줄 (예: img_payslip_a)")
    if not name:
        raise ValueError("서식 이름을 적으세요 (문서 분류의 정답이 됩니다)")
    if form_id in load_all() or RF.image_form_dir(form_id) or formdir.folder(form_id):
        raise ValueError(f"이미 있는 서식 ID: {form_id}")
    if real_data:
        if not private_dir:
            raise ValueError("실서류 견본에서 만든 서식은 사내 서식 폴더(private_forms_dir)에만 둡니다. studio 설정에 private_forms_dir 을 정하세요. "
                             "빈 서식·공개 서식 그림이면 '실서류 견본' 표시를 끄세요")
        root = Path(private_dir)
    else:
        root = None   # 저장소 docgen/forms/<ID>/
    pages_in = _pages(files)   # 폴더를 만들기 전에 읽어 본다 (깨진 파일이면 아무것도 남기지 않음)
    dest = formdir.new_dir(form_id, root)
    try:
        pages = []
        for k, (src, im) in enumerate(pages_in):
            scale = A4_LONG_PT * RF.BG_ZOOM / max(im.size)   # 긴 변 = A4 긴 변 (배경 해상도 BG_ZOOM 기준 픽셀)
            im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))))
            im.save(dest / "look" / f"page_{k}.png")
            pages.append({"width": round(im.width / RF.BG_ZOOM, 2), "height": round(im.height / RF.BG_ZOOM, 2), "from": src})
        lay = {"name": name, "class": "그린 서식", "origin": "drawn", "pages": pages, "items": [], "texts": [],
               "created": time.strftime("%Y-%m-%d %H:%M"), "private": root is not None}
        (dest / "layout.json").write_text(json.dumps(lay, ensure_ascii=False, indent=1), encoding="utf-8")
        OV.write_new(dest, {})   # 빈 칸 목록 fields.json
    except Exception:
        shutil.rmtree(dest, ignore_errors=True)   # 반쯤 만든 폴더를 남기지 않는다 (방금 만든 폴더만)
        raise
    RF.register_images()   # 바로 서식 목록·영역 편집기에 나오게
    return {"form_id": form_id, "dir": str(dest), "private": root is not None, "pages": len(pages)}



OCR_CONFIG = Path(__file__).resolve().parents[1] / "docgen" / "bench" / "ocr_config.example.json"   # mapping 기본값


def ocr_settings(ocr: dict | None) -> dict:
    """studio 설정의 ocr → 부를 함수·버전·캐시 폴더·결과 읽는 법(mapping). 옛 이름 internal_ocr_adapter:… 는 studio 로 옮긴 것."""
    o = dict(ocr or {})
    name = o.get("callable") or "studio.internal_ocr_adapter:ocr_from_file"
    o["callable"] = f"studio.{name}" if name.startswith("internal_ocr_adapter:") else name
    o.setdefault("revision", "")
    o.setdefault("cache_dir", str(Path(__file__).resolve().parents[1] / "studio_cache" / "ocr"))
    if not o.get("mapping"):
        o["mapping"] = json.loads(OCR_CONFIG.read_text(encoding="utf-8"))["mapping"]
    return o


def read_texts(doc_id: str, ocr: dict | None, replace: bool = False) -> dict:
    """그린 서식의 배경 그림을 사내 OCR 로 읽어 layout.json 의 texts (배경 글자) 를 채운다 → 합성 OCR 세트에 들어갈 수 있다.
    OCR 설정·캐시는 OCR 준비(docgen.bench.ocr_prepare)와 같은 키. 지운 곳의 글자는 정답에서 빠진다 (docgen/ocr_export.background_words).
    실서류 견본 그림이면 사내 OCR 로만 (외부로 보내지 않음, AGENTS.md 규칙 10)."""
    import os

    from docgen import realform as RF
    from docgen.bench.ocr_data import canonical_image, digest, dumps, load_callable, parse_ocr, write_json

    d = RF.image_form_dir(doc_id)
    if d is None:
        raise KeyError(doc_id)
    lay = json.loads((d / "layout.json").read_text(encoding="utf-8"))
    if lay.get("texts") and not replace:
        raise ValueError(f"이미 배경 글자가 있습니다 ({len(lay['texts'])}개). 다시 읽으려면 바꾸기를 고르세요")
    o = ocr_settings(ocr)
    if not o.get("revision"):
        raise ValueError("사내 OCR 설정이 없습니다 (studio 설정의 ocr.callable·revision). 사내 OCR 은 내부망에서만 쓸 수 있습니다")
    if o.get("base_url"):
        os.environ.setdefault("INTERNAL_OCR_BASE_URL", o["base_url"])
    adapter = load_callable(o["callable"])
    cache = Path(o["cache_dir"])
    texts = []
    for k, _ in enumerate(lay["pages"]):
        img = d / "look" / f"page_{k}.png"
        im = canonical_image(str(img))
        sha = digest(str(im.size).encode() + im.tobytes())
        cached = cache / "ocr" / f"{digest(dumps([sha, o['callable'], o['revision']]).encode())}.json"
        if cached.exists():
            raw = json.loads(cached.read_text(encoding="utf-8"))
        else:
            raw = adapter(str(img))
            if raw is None:
                raise ValueError(f"OCR 실패: {k + 1}쪽")
            write_json(cached, raw)
        for w in parse_ocr(raw, im.width, im.height, o["mapping"]):
            texts.append({"page": k, "text": w["text"], "rect": [round(v / RF.BG_ZOOM, 2) for v in w["bbox"]],
                          "line": w.get("line_num") or 0})
        im.close()
    lay["texts"] = texts
    lay["texts_from"] = {"ocr": o["callable"], "revision": o["revision"], "at": time.strftime("%Y-%m-%d %H:%M")}
    (d / "layout.json").write_text(json.dumps(lay, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"form_id": doc_id, "texts": len(texts), "pages": len(lay["pages"])}
