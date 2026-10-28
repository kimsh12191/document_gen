"""OCR 준비 시험용 가짜 사내 OCR 과 작은 manifest (옛 ocr/demo.py). 모델·네트워크를 쓰지 않는다."""
from pathlib import Path

from PIL import Image, ImageDraw

from docgen.bench.ocr_data import write_json, write_jsonl


def ocr_from_file(image_path):
    entries = []
    for text, box in [("USD 123.45", [20, 40, 180, 65]), ("DATE", [20, 100, 80, 120]), ("DATE", [200, 100, 260, 120])]:
        x1, y1, x2, y2 = box
        entries.append({"text": text, "confidence": 0.99, "line_num": 0,
                        "bounding": {"shape": "rectangle", "vertices": [
                            {"x": x1, "y": y1}, {"x": x2, "y": y1}, {"x": x2, "y": y2}, {"x": x1, "y": y2}]}})
    return {"filename": Path(image_path).name, "success": "Y", "data": {"basicData": [entries]}}


def create_demo(root):
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    manifest = []
    for idx in range(4):
        path = root / f"document_{idx}.png"
        im = Image.new("RGB", (400, 200), "white")
        draw = ImageDraw.Draw(im)
        draw.text((20, 5), f"SYNTHETIC DOCUMENT {idx}", fill="black")
        draw.text((20, 40), "USD 123.45", fill="black")
        draw.text((20, 100), "DATE", fill="black")
        draw.text((200, 100), "DATE", fill="black")
        im.save(path)
        manifest.append({"document_id": f"doc_{idx}", "page_id": "page_1", "image": str(path), "split": "benchmark" if idx == 3 else "train"})
    write_jsonl(root / "manifest.jsonl", manifest)
    config = {"manifest": "manifest.jsonl", "output_dir": "prepared", "cache_dir": "cache", "ocr_callable": "docgen.tests.ocr_fixture:ocr_from_file",
              "ocr_revision": "synthetic-fixture-v1", "mapping": {"items_path": "data.basicData", "success_key": "success", "success_value": "Y"},
              "val_fraction": 0.34, "sft_max_examples": 30, "seed": 42}
    write_json(root / "config.json", config)
    return root / "config.json"
