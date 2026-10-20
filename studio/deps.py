"""studio 가 쓰는 파이썬 패키지(fastapi, uvicorn …)를 인터넷 없는 docgen 컨테이너에 넣는다.

docgen 도커 이미지에는 studio 패키지가 없고, 이미지를 새로 반입하기는 어렵다. 그래서 Linux 용 설치 파일(wheel)을
코드와 함께 반입해 코드 폴더 아래 studio_deps/ 에 설치한다. studio 는 이 폴더가 있으면 자동으로 읽는다.

  python -m studio.deps download   인터넷 되는 PC: studio/wheels/ 에 Linux(파이썬 3.12) 설치 파일을 받는다
  python -m studio.deps install    docgen 컨테이너 안: studio/wheels/ 에서 studio_deps/ 로 설치 (인터넷 불필요)
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQS = ROOT / "studio" / "requirements.txt"
WHEELS = ROOT / "studio" / "wheels"
TARGET = ROOT / "studio_deps"
# docgen 도커 이미지 (ubuntu 24.04, 파이썬 3.12, x86_64)
PLATFORM = ["--platform", "manylinux2014_x86_64", "--platform", "manylinux_2_17_x86_64",
            "--python-version", "3.12", "--implementation", "cp", "--only-binary=:all:"]


def download() -> None:
    if WHEELS.exists():
        shutil.rmtree(WHEELS)
    subprocess.run([sys.executable, "-m", "pip", "download", "-r", str(REQS), "-d", str(WHEELS), *PLATFORM], check=True)
    print(f"{len(list(WHEELS.glob('*.whl')))}개 → {WHEELS}. 코드와 함께 반입한 뒤 컨테이너에서 python -m studio.deps install")


def install() -> None:
    if not any(WHEELS.glob("*.whl")):
        sys.exit(f"{WHEELS} 에 설치 파일이 없습니다. 인터넷 되는 PC에서 python -m studio.deps download 를 먼저 하세요.")
    if TARGET.exists():
        shutil.rmtree(TARGET)
    subprocess.run([sys.executable, "-m", "pip", "install", "--no-index", "--find-links", str(WHEELS),
                    "--target", str(TARGET), "-r", str(REQS)], check=True)
    print(f"설치 → {TARGET}. 이제 python -m studio 로 띄운다")


def main() -> None:
    ap = argparse.ArgumentParser(prog="python -m studio.deps", description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["download", "install"])
    {"download": download, "install": install}[ap.parse_args().command]()


if __name__ == "__main__":
    main()
