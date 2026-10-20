"""studio 설정: studio/config.json (없으면 기본값). 환경마다 다른 것은 모두 여기에 둔다.

config.json 에는 바꿀 항목만 적는다. 예시는 studio/config.example.json.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = Path(os.environ.get("STUDIO_CONFIG", ROOT / "studio" / "config.json"))

DEFAULTS = {
    "host": "127.0.0.1",
    "port": 8765,
    "browser": None,            # 렌더링에 쓸 Chrome/Edge 실행 파일. 없으면 CHROMIUM_PATH → 이 PC의 Chrome/Edge 순으로 찾음
    "cache_dir": "studio_cache",
    "ocr": None,                # {"callable", "revision", "cache_dir", "mapping", "base_url"} — 1부 OCR 준비 단계와 같은 키 (DESIGN.md 8.2)
    "workspace_dir": "studio_workspace",  # 데이터셋 등록부·studio가 만든 데이터셋·채점 결과 (DESIGN.md 9.1)
    "import_dir": None,         # 가져올 문서 이미지 뭉치 폴더 (DESIGN.md 8절)
    "real_data_dir": None,      # 실서류 검수 결과: 라벨·OCR·업무 묶음 (저장소 밖)
    "private_forms_dir": None,  # 실서류에서 만든 서식 (저장소 밖)
    "providers": {},            # 분석기 (9단계)
}

# Windows 에서 흔한 브라우저 위치. 회사망에서 Playwright 가 Chromium 을 내려받지 못할 때 쓴다.
_BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def load() -> dict:
    cfg = dict(DEFAULTS)
    if CONFIG_PATH.exists():
        cfg.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
    cfg["config_file"] = str(CONFIG_PATH) if CONFIG_PATH.exists() else None
    return cfg


def resolve_path(p: str | None) -> Path | None:
    if not p:
        return None
    p = Path(os.path.expanduser(p))
    return p if p.is_absolute() else ROOT / p


def setup_browser(cfg: dict) -> str | None:
    """렌더러가 쓸 브라우저를 CHROMIUM_PATH 로 넘긴다 (docgen/image.py 가 읽음). 찾은 경로를 돌려준다."""
    path = cfg.get("browser") or os.environ.get("CHROMIUM_PATH")
    if not path:
        path = next((b for b in _BROWSERS if Path(b).exists()), None)
    if path:
        os.environ["CHROMIUM_PATH"] = path
    return path
