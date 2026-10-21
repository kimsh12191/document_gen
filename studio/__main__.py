"""python -m studio [--host 0.0.0.0] [--port 8765]

저장소 루트에서 실행한다. 설정은 studio/config.json (없으면 기본값, 예시는 config.example.json).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import uvicorn

from .config import load


def main() -> None:
    cfg = load()
    ap = argparse.ArgumentParser(prog="studio", description="docgen studio")
    ap.add_argument("--host", default=cfg["host"], help="다른 PC에서 접속하려면 0.0.0.0")
    ap.add_argument("--port", type=int, default=cfg["port"])
    ap.add_argument("--reload", action="store_true", help="코드를 고치면 서버를 다시 띄움 (개발용)")
    args = ap.parse_args()
    print(f"docgen studio → http://{'localhost' if args.host in ('127.0.0.1', '0.0.0.0') else args.host}:{args.port}")
    # 다시 띄우는 기준은 studio/·docgen/ 의 .py 만 (작업 폴더·데이터는 보지 않음)
    root = Path(__file__).resolve().parents[1]
    dirs = [str(root / "studio"), str(root / "docgen")] if args.reload else None
    uvicorn.run("studio.app:app", host=args.host, port=args.port, reload=args.reload, reload_dirs=dirs)


main()
