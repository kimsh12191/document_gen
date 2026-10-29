"""시험용 openai 방식 모델 서버 (vLLM 대신). python playground/tests/fake_vlm.py --port 8100 [--wait 1]
답: 마지막 질문에 "REPLY:" 가 있으면 그 뒤 글 그대로, 아니면 받은 요청 요약 JSON (메시지 수·그림 수·그림 크기·질문)."""
import argparse
import base64
import io
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def summary(body: dict) -> dict:
    from PIL import Image

    sizes, texts = [], []
    for m in body["messages"]:
        content = m["content"] if isinstance(m["content"], list) else [{"type": "text", "text": m["content"]}]
        for c in content:
            if c["type"] == "image_url":
                data = base64.b64decode(c["image_url"]["url"].split(",", 1)[1])
                sizes.append(list(Image.open(io.BytesIO(data)).size))
            else:
                texts.append(c["text"])
    return {"n_messages": len(body["messages"]), "roles": [m["role"] for m in body["messages"]], "sizes": sizes,
            "prompt": texts[-1], "model": body.get("model"), "thinking": body.get("chat_template_kwargs")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--wait", type=float, default=0, help="뜨기 전 기다리는 초 (모델 읽는 시간 흉내)")
    a = ap.parse_args()
    print("loading model ...", flush=True)
    time.sleep(a.wait)

    class H(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _json(self, obj):
            data = json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path.rstrip("/").endswith("/models"):
                return self._json({"data": [{"id": "docgen"}]})
            self.send_error(404)

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            s = summary(body)
            text = s["prompt"].split("REPLY:", 1)[1].strip() if "REPLY:" in s["prompt"] else json.dumps(s, ensure_ascii=False)
            self._json({"choices": [{"message": {"role": "assistant", "content": text}, "finish_reason": "stop"}],
                        "usage": {"prompt_tokens": 1, "completion_tokens": 1}})

    httpd = ThreadingHTTPServer(("127.0.0.1", a.port), H)
    print(f"INFO:     Uvicorn running on http://127.0.0.1:{a.port} (Press CTRL+C to quit)", flush=True)
    sys.stdout.flush()
    httpd.serve_forever()


if __name__ == "__main__":
    main()
