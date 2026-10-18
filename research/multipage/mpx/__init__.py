"""서류 묶음 속 여러 쪽 문서 추출 연구 (mpx).

저장소 루트의 docgen 을 가져다 쓰므로, research/multipage 에서 `python -m mpx ...` 로 실행하면 루트를 경로에 넣는다.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
