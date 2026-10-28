"""docgen studio — 벤치마크 데이터 생성·관리 도구. 설계는 studio/DESIGN.md."""
import sys
from pathlib import Path

# 이미지를 다시 만들 수 없는 docgen 컨테이너용: python -m studio.deps install 이 설치한 패키지 (README "내부망")
_ROOT = Path(__file__).resolve().parents[1]
_DEPS = _ROOT / "studio_deps"
if _DEPS.is_dir() and str(_DEPS) not in sys.path:
    sys.path.append(str(_DEPS))
