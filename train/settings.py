"""설정 읽기 (JSON, YAML 은 학습 설정만)와 이미지 토큰 계산 (옛 bank_ocr/settings.py·cli.py)."""
import json
import math
from pathlib import Path


def load_settings(path):
    path = Path(path)
    if path.suffix.lower() == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
    else:
        try:
            import yaml
        except ImportError as exc:
            raise ValueError("YAML training configs require PyYAML (pip install pyyaml)") from exc
        try:
            value = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid YAML config: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("Config must be an object/mapping")
    if any(not isinstance(key, str) for key in value):
        raise ValueError("Config keys must be strings")
    return value


def image_tokens(model_dir, max_size):
    """Visual tokens needed for an image of max_size, from the model's vision config."""
    config = json.loads((Path(model_dir) / "config.json").read_text(encoding="utf-8"))
    vision = config.get("vision_config", {})
    patch, merge = vision.get("patch_size"), vision.get("spatial_merge_size")
    if not patch or not merge:
        raise ValueError("config.json has no vision_config.patch_size/spatial_merge_size")
    factor = patch * merge
    return image_tokens_for(max_size, factor), factor


def image_tokens_for(max_size, factor):
    return math.ceil(max(max_size) / factor) * math.ceil(min(max_size) / factor)
