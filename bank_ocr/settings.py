"""Small configuration readers; YAML is only needed by the training launcher."""
import json
from pathlib import Path


def load_settings(path):
    path = Path(path)
    if path.suffix.lower() == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
    else:
        try:
            import yaml
        except ImportError as exc:
            raise ValueError("YAML training configs require PyYAML; install requirements-train.in") from exc
        try:
            value = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid YAML config: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("Config must be an object/mapping")
    if any(not isinstance(key, str) for key in value):
        raise ValueError("Config keys must be strings")
    return value
