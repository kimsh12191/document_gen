"""docgen labels -> OCR JSON in the in-house OCR response format, one file per page image (example data only).

Real training uses the in-house OCR on real scans. For the guide examples there is no real image to show, so this
turns the generator's ground truth (value boxes, label boxes) into the same response format, one line per item:

  python guide/examples/labels_to_ocr.py <docgen generate --out 폴더> <OCR JSON 폴더>

The conversion lives in docgen/ocr_export.py (export_fields). The synthetic OCR benchmark uses the full-page
version there (every printed word, python -m docgen.ocr_set).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from docgen.ocr_export import export_fields  # noqa: E402

export_fields(Path(sys.argv[1]), Path(sys.argv[2]))
print("done")
