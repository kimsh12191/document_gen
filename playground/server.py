"""웹 서버 (표준 라이브러리). 화면 static/, API /api/…. 명령을 실행하는 화면이라 기본은 이 서버 안(127.0.0.1)에서만 열린다."""
from __future__ import annotations

import json
import mimetypes
import os
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import gpus as G, images as IM, questions as Q
from .ask import Asker
from .models import ENGINES, Models, command

STATIC = Path(__file__).resolve().parent / "static"


class App:
    def __init__(self, home: Path):
        self.home = Path(home).expanduser()
        self.home.mkdir(parents=True, exist_ok=True)
        self.models = Models(self.home)
        self.asker = Asker(self.home, self.models)
        self.recent_file = self.home / "recent.json"

    def recent(self, kind: str, value: str | None = None) -> list[str]:
        """최근 쓴 모델 경로·이미지 폴더 (앞이 최근)."""
        try:
            body = json.loads(self.recent_file.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            body = {}
        items = body.get(kind, [])
        if value:
            items = [value] + [x for x in items if x != value]
            body[kind] = items[:20]
            self.recent_file.write_text(json.dumps(body, ensure_ascii=False, indent=1), encoding="utf-8")
        return items

    # -- API: (method, path) → 함수 --------------------------------------------------------
    def get(self, path: str, qs: dict):
        if path == "/api/gpus":
            return G.status()
        if path == "/api/models":
            return {"models": self.models.list(), "recent": self.recent("model"), "engines": list(ENGINES),
                    "next_port": self.models.next_port()}
        if path.startswith("/api/models/") and path.endswith("/log"):
            return {"log": self.models.log(path.split("/")[3])}
        if path == "/api/forms":
            return {"forms": Q.forms(), "tasks": Q.TASKS}
        if path == "/api/folder":
            folder = qs.get("dir", [""])[0]
            out = IM.listing(folder)
            self.recent("folder", out["folder"])
            return out
        if path == "/api/recent":
            return {"folder": self.recent("folder"), "model": self.recent("model")}
        raise KeyError(path)

    def post(self, path: str, body: dict):
        if path == "/api/models/command":
            gpus = [int(g) for g in body.get("gpus") or []]
            return command(body.get("path") or "", gpus, int(body.get("port") or self.models.next_port()),
                           body.get("model_type") or None, body.get("engine") or "swift")
        if path == "/api/models/start":
            if body.get("path"):
                self.recent("model", body["path"])
            return self.models.start(body.get("name") or "", body.get("path") or "", body.get("command") or "",
                                     [int(g) for g in body.get("gpus") or []], int(body.get("factor") or 32))
        if path == "/api/models/attach":
            return self.models.attach(body.get("name") or "", body.get("endpoint") or "", int(body.get("factor") or 32))
        if path.startswith("/api/models/") and path.endswith("/stop"):
            return self.models.stop(path.split("/")[3])
        if path.startswith("/api/models/") and path.endswith("/remove"):
            self.models.remove(path.split("/")[3])
            return {"removed": True}
        if path == "/api/question":
            return Q.build(body)
        if path == "/api/ask":
            return self.asker.ask(body)
        raise KeyError(path)


def handler(app: App):
    class H(BaseHTTPRequestHandler):
        server_version = "docgen-playground"

        def log_message(self, fmt, *args):   # 요청마다 찍지 않는다
            pass

        def _send(self, code: int, data: bytes, ctype: str, cache: bool = False):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "max-age=3600" if cache else "no-store")
            self.end_headers()
            self.wfile.write(data)

        def _json(self, code: int, obj):
            self._send(code, json.dumps(obj, ensure_ascii=False).encode(), "application/json; charset=utf-8")

        def _run(self, fn):
            try:
                self._json(200, fn())
            except KeyError as exc:
                self._json(404, {"error": f"없음: {exc}"})
            except (ValueError, OSError) as exc:
                self._json(400, {"error": str(exc)})
            except Exception as exc:   # 화면에 보여 주고 서버는 계속
                traceback.print_exc()
                self._json(500, {"error": f"{type(exc).__name__}: {exc}"})

        def do_GET(self):
            u = urlparse(self.path)
            qs = parse_qs(u.query)
            if u.path.startswith("/api/"):
                return self._run(lambda: app.get(u.path, qs))
            if u.path == "/img":   # 고른 그림 원본 (thumb=크기 면 작은 그림)
                try:
                    path, page = qs["path"][0], int(qs.get("page", ["0"])[0])
                    if "thumb" in qs:
                        data = IM.thumb(path, page, int(qs["thumb"][0]), os.path.getmtime(path))
                        return self._send(200, data, "image/jpeg", cache=True)
                    data, _ = IM.view(path, page)
                    return self._send(200, data, "image/png")
                except (KeyError, ValueError, OSError, EOFError) as exc:
                    return self._json(400, {"error": str(exc)})
            if u.path.startswith("/sent/"):
                p = app.asker.sent / Path(u.path).name
                if p.is_file():
                    return self._send(200, p.read_bytes(), "image/png", cache=True)
                return self._json(404, {"error": "없음"})
            name = "index.html" if u.path in ("/", "") else u.path.lstrip("/")
            p = (STATIC / name).resolve()
            if STATIC.resolve() not in p.parents or not p.is_file():
                return self._json(404, {"error": "없음"})
            self._send(200, p.read_bytes(), (mimetypes.guess_type(p.name)[0] or "application/octet-stream") + "; charset=utf-8")

        def do_POST(self):
            u = urlparse(self.path)
            n = int(self.headers.get("Content-Length") or 0)
            try:
                body = json.loads(self.rfile.read(n) or b"{}")
            except ValueError:
                return self._json(400, {"error": "JSON 이 아닙니다"})
            self._run(lambda: app.post(u.path, body))

    return H


def serve(home: Path, host: str, port: int) -> ThreadingHTTPServer:
    httpd = ThreadingHTTPServer((host, port), handler(App(home)))
    httpd.daemon_threads = True
    return httpd
