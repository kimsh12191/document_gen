"""python -m playground [--port 7860] [--open] [--home ~/.docgen_playground] — 설명은 playground/README.md."""
import argparse
import socket
from pathlib import Path

from .server import serve


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m playground", description=__doc__)
    p.add_argument("--port", type=int, default=7860)
    p.add_argument("--open", action="store_true", help="다른 PC 에서도 열리게 (0.0.0.0). 없으면 이 서버 안에서만")
    p.add_argument("--home", default="~/.docgen_playground", help="띄운 모델 목록·로그·보낸 그림·묻고 받은 기록을 두는 곳")
    a = p.parse_args(argv)
    host = "0.0.0.0" if a.open else "127.0.0.1"
    httpd = serve(Path(a.home).expanduser(), host, a.port)
    where = f"http://{socket.gethostname()}:{a.port}" if a.open else f"http://127.0.0.1:{a.port}"
    print(f"모델 써 보기: {where}   (기록 {Path(a.home).expanduser()})", flush=True)
    if not a.open:
        print(f"  다른 PC 에서 열려면 --open (또는 ssh -L {a.port}:127.0.0.1:{a.port} <이 서버>)", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print("화면을 끕니다. 띄운 모델은 계속 떠 있습니다 (다시 켜면 목록에 나옴, 끄려면 화면에서 [내리기]).", flush=True)


if __name__ == "__main__":
    main()
