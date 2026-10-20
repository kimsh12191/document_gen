"""Banking-task stage on top of the OCR model: docgen data -> SFT -> GRPO -> docgen benchmark.

Builds on the OCR project next door (../../ocr: bank_ocr data/inference/metrics helpers), so that folder is put on
sys.path here; then `import bank_task` works from the pipeline, the GRPO reward plugin, the viewer and studio."""
import sys
from pathlib import Path

_OCR = Path(__file__).resolve().parents[2] / "ocr"
if _OCR.is_dir() and str(_OCR) not in sys.path:
    sys.path.append(str(_OCR))
