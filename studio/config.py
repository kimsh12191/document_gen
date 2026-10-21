"""studio 설정: studio/config.json (없으면 기본값). 환경마다 다른 것은 모두 여기에 둔다.

config.json 에는 바꿀 항목만 적는다. 예시는 studio/config.example.json.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]   # 저장소 최상위
CONFIG_PATH = Path(os.environ.get("STUDIO_CONFIG", ROOT / "studio" / "config.json"))

DEFAULTS = {
    "host": "127.0.0.1",
    "port": 8765,
    "browser": None,            # 렌더링에 쓸 Chrome/Edge 실행 파일. 없으면 CHROMIUM_PATH → Playwright Chromium → 이 PC의 Chrome/Edge 순으로 찾음
    "cache_dir": "studio_cache",
    "ocr": None,                # {"callable", "revision", "cache_dir", "mapping", "base_url"} — OCR 준비(docgen.bench.ocr_prepare)와 같은 키 (DESIGN.md 8.2)
    "workspace_dir": "studio_workspace",  # 데이터셋 등록부·studio가 만든 데이터셋·채점 결과 (DESIGN.md 9.1)
    "import_dir": None,         # 가져올 문서 이미지 뭉치 폴더 (DESIGN.md 8절). 있으면 ④에서 서버 경로는 이 아래만 받는다
    "real_data_dir": None,      # 실서류 검수 결과: 라벨·OCR·업무 묶음 (저장소 밖). 없으면 <workspace_dir>/real_data (화면에 경고)
    "private_forms_dir": None,  # 실서류에서 만든 서식 (저장소 밖)
    "providers": {},            # 분석기 (⑧ 작업 › 분석기, ⑤ autolabel. 형식은 studio/analyzers.py 머리말, DESIGN.md 7.2)
    "path_map": {},             # studio 경로 → 학습 컨테이너 경로 (예: {"/out": "/share/me/docgen_data"}). 학습 설정을 내보낼 때 바꾼다 (DESIGN.md 9.9)
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


def _playwright_browser() -> str | None:
    """Playwright 가 내려받아 둔 Chromium (docgen 도커 이미지는 PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright).
    설치를 끝까지 마친 폴더(INSTALLATION_COMPLETE 표시)만 센다."""
    roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH"), "~/.cache/ms-playwright",
             os.path.join(os.environ.get("LOCALAPPDATA", ""), "ms-playwright")]
    for root in filter(None, roots):
        root = Path(os.path.expanduser(root))
        if not root.is_dir():
            continue
        for pattern in ("chromium_headless_shell-*", "chromium-*"):
            done = [d for d in sorted(root.glob(pattern)) if (d / "INSTALLATION_COMPLETE").exists()]
            if done:
                return str(done[-1])
    return None


def setup_browser(cfg: dict) -> str | None:
    """렌더링에 쓸 브라우저를 찾아 그 위치를 돌려준다. 못 찾으면 None (렌더링 기능만 꺼진다).

    렌더러(docgen/image.py)는 Playwright Chromium 을 먼저 쓰고, 안 되면 CHROMIUM_PATH 의 실행 파일을 쓴다.
    그래서 설정·환경변수에 실행 파일이 없으면 이 PC의 Chrome/Edge 를 예비로 CHROMIUM_PATH 에 넘긴다."""
    path = cfg.get("browser") or os.environ.get("CHROMIUM_PATH")
    if path:
        os.environ["CHROMIUM_PATH"] = path
        return path
    spare = next((b for b in _BROWSERS if Path(b).exists()), None)
    if spare:
        os.environ["CHROMIUM_PATH"] = spare
    return _playwright_browser() or spare
