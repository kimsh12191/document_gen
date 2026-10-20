"""Look at the model's OCR by eye: a small local web page (viewer/index.html) in front of a
running model server. See viewer/README.md; viewer/start.sh starts the model and this page.

    python viewer/ocr_viewer.py --endpoint http://127.0.0.1:8010/v1
    python viewer/ocr_viewer.py --endpoint http://127.0.0.1:8010/v1 --tasks data/prepared-v2/benchmark_tasks.jsonl
    python viewer/ocr_viewer.py --tasks data/prepared-v2/benchmark_tasks.jsonl --predictions runs/exp1/predictions/base.jsonl
"""
import argparse
import base64
import io
import json
import os
import random
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))  # bank_ocr lives next to this folder

from bank_ocr.augment import fit_scale  # noqa: E402
from bank_ocr.data import dumps, normalize_box, read_jsonl  # noqa: E402
from bank_ocr.inference import index_predictions  # noqa: E402
from bank_ocr.metrics import BOX_TASKS, answer, parse_boxes, parse_target, reward  # noqa: E402
from bank_ocr.tasks import DIRECTIONS, PROMPTS  # noqa: E402

PROMPT_BOX = re.compile(r"bbox_2d=(\[\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\])")
NUM = r"-?\d+(?:\.\d+)?"
QUAD = re.compile(rf"\[\s*({NUM})\s*,\s*({NUM})\s*,\s*({NUM})\s*,\s*({NUM})\s*\]")
LABEL = re.compile(r'"(?:label|text)"\s*:\s*"((?:[^"\\]|\\.)*)"')


def png_bytes(im):
    buffer = io.BytesIO()
    im.save(buffer, "PNG")
    return buffer.getvalue()


def data_url(im, quality=90):
    buffer = io.BytesIO()
    im.convert("RGB").save(buffer, "JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def to_pixels(box, width, height, x0=0, y0=0, scale=1000):
    """bbox_2d on a (tile) image of width x height -> pixels on the full image. scale=1000 for
    Qwen's 0..1000 coordinates; scale=None when the model answered in pixels of that image."""
    sx, sy = (width / scale, height / scale) if scale else (1, 1)
    return [x0 + box[0] * sx, y0 + box[1] * sy, x0 + box[2] * sx, y0 + box[3] * sy]


def find_positions(text):
    """Boxes anywhere in a free-form answer: the strict JSON list first, else every
    {"bbox_2d": [...], "label": ...} object, else any bare [x1, y1, x2, y2]."""
    strict = parse_boxes(text)
    if strict is not None:
        return strict
    text = answer(text)
    found = []
    for obj in re.finditer(r"\{[^{}]*\}", text):
        quad = QUAD.search(obj.group(0))
        if quad and "bbox" in obj.group(0):
            label = LABEL.search(obj.group(0))
            found.append({"bbox_2d": [float(v) for v in quad.groups()],
                          "label": json.loads(f'"{label.group(1)}"') if label else ""})
    if not found:
        found = [{"bbox_2d": [float(v) for v in m.groups()], "label": ""} for m in QUAD.finditer(text)]
    return [b for b in found if b["bbox_2d"][2] > b["bbox_2d"][0] and b["bbox_2d"][3] > b["bbox_2d"][1]]


def render_pdf(data, page, dpi):
    try:
        import pypdfium2 as pdfium
    except ImportError:
        pdfium = None
    if pdfium is not None:
        pdf = pdfium.PdfDocument(data)
        count = len(pdf)
        if not 1 <= page <= count:
            raise ValueError(f"PDF has {count} pages; page {page} does not exist")
        return pdf[page - 1].render(scale=dpi / 72).to_pil().convert("RGB"), count
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise ValueError("PDF needs pypdfium2 or PyMuPDF: pip install pypdfium2 (or convert the page to PNG)") from None
    doc = fitz.open(stream=data, filetype="pdf")
    if not 1 <= page <= doc.page_count:
        raise ValueError(f"PDF has {doc.page_count} pages; page {page} does not exist")
    pix = doc[page - 1].get_pixmap(dpi=dpi)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples), doc.page_count


class Viewer:
    def __init__(self, a):
        self.endpoint = a.endpoint.rstrip("/") if a.endpoint else None
        self.model, self.max_tokens, self.timeout = a.model, a.max_tokens, a.timeout
        self.max_size, self.dpi = a.max_size, a.pdf_dpi
        self.rows = read_jsonl(a.tasks) if a.tasks else []
        self.predictions = index_predictions(a.predictions) if a.predictions else {}
        if self.predictions:
            self.rows = [r for r in self.rows if r["id"] in self.predictions]
            if not self.rows:
                raise SystemExit("No task IDs of --tasks appear in --predictions")
        self._scores = {}

    # -- model -------------------------------------------------------------------------
    def chat(self, image_png, prompt):
        if not self.endpoint:
            raise ValueError("Start the viewer with --endpoint to ask the model")
        content = [{"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(image_png).decode("ascii")}},
                   {"type": "text", "text": prompt}]
        payload = {"model": self.model, "messages": [{"role": "user", "content": content}], "temperature": 0,
                   "max_tokens": self.max_tokens, "stream": False, "chat_template_kwargs": {"enable_thinking": False}}
        headers = {"Content-Type": "application/json"}
        if os.getenv("INTERNAL_MODEL_API_KEY"):
            headers["Authorization"] = "Bearer " + os.environ["INTERNAL_MODEL_API_KEY"]
        req = Request(self.endpoint + "/chat/completions", data=dumps(payload).encode(), headers=headers)
        with urlopen(req, timeout=self.timeout) as response:
            choice = json.load(response)["choices"][0]
        return choice["message"].get("content") or "", choice.get("finish_reason")

    # -- free test ---------------------------------------------------------------------
    def load(self, req):
        """Server path or upload; PDF pages are rendered. Resized exactly like prepare does."""
        if req.get("path"):
            path = Path(req["path"]).expanduser()
            data, name = path.read_bytes(), path.name
        elif req.get("upload"):
            data, name = base64.b64decode(req["upload"].split(",", 1)[1]), req.get("name", "")
        else:
            raise ValueError("Give an image/PDF path on the server or upload a file")
        page, pages = int(req.get("page") or 1), 1
        if data[:5] == b"%PDF-" or name.lower().endswith(".pdf"):
            im, pages = render_pdf(data, page, self.dpi)
        else:
            im = Image.open(io.BytesIO(data))
            pages = getattr(im, "n_frames", 1)
            if not 1 <= page <= pages:
                raise ValueError(f"The image has {pages} pages; page {page} does not exist")
            im.seek(page - 1)
            im = ImageOps.exif_transpose(im).convert("RGB")
        scale = fit_scale(*im.size, self.max_size)
        if scale != 1:
            im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
        return im, pages

    def run(self, req):
        im, pages = self.load(req)
        lang = 1 if req.get("lang") == "ko" else 0
        mode = req.get("mode", "spotting")
        picked = normalize_box(req["box"], im.width, im.height) if req.get("box") else None
        jobs = []  # (tile box in pixels, prompt)
        full = [0, 0, im.width, im.height]
        if mode == "spotting":
            rows, cols = (int(v) for v in req.get("grid", "1x1").split("x"))
            for r in range(rows):
                for c in range(cols):
                    jobs.append(([round(c * im.width / cols), round(r * im.height / rows),
                                  round((c + 1) * im.width / cols), round((r + 1) * im.height / rows)],
                                 PROMPTS["spotting"][lang].format()))
        elif mode == "find":
            jobs.append((full, PROMPTS["grounding"][lang].format(text=dumps(req["text"]))))
        elif mode == "read_box":
            if not picked:
                raise ValueError("Drag a region on the image first")
            jobs.append((full, PROMPTS["region_ocr"][lang].format(box=dumps(picked))))
        elif mode == "relation":
            direction = DIRECTIONS[req["direction"]]
            jobs.append((full, PROMPTS["relation"][lang].format(direction=direction[0], direction_ko=direction[1],
                                                                 anchor=dumps(req["text"]))))
        elif mode == "custom":
            prompt = req.get("prompt", "").strip()
            if not prompt:
                raise ValueError("Write a question")
            if "{box}" in prompt:
                if not picked:
                    raise ValueError("The question uses {box}: drag a region on the image first")
                prompt = prompt.replace("{box}", dumps(picked))
            jobs.append((full, prompt))
        else:
            raise ValueError(f"Unknown mode {mode}")
        scale = None if req.get("coords") == "pixel" else 1000

        def ask(job):
            tile, prompt = job
            crop = im.crop(tuple(tile)) if tile != full else im
            text, finish = self.chat(png_bytes(crop), prompt)
            boxes = find_positions(text) if mode == "custom" else parse_boxes(text)
            w, h = tile[2] - tile[0], tile[3] - tile[1]
            drawn = [{"px": to_pixels(b["bbox_2d"], w, h, tile[0], tile[1], scale), "label": b["label"]} for b in boxes or []]
            return {"tile": tile, "prompt": prompt, "raw": text, "finish_reason": finish,
                    "parsed": boxes is not None, "boxes": drawn}

        with ThreadPoolExecutor(max_workers=8) as pool:
            parts = list(pool.map(ask, jobs))
        result = {"image": data_url(im), "width": im.width, "height": im.height, "pages": pages, "parts": parts,
                  "pred": [b for p in parts for b in p["boxes"]], "gold": [], "query": [], "free": True}
        if len(parts) == 1:
            result["pred_text"] = answer(parts[0]["raw"])
        if mode == "read_box" or (mode == "custom" and "{box}" in req.get("prompt", "")):
            result["query"] = [req["box"]]
        return result

    # -- benchmark sample --------------------------------------------------------------
    def score(self, row):
        if row["id"] not in self._scores:
            self._scores[row["id"]] = reward(self.predictions[row["id"]], row["task"], row["target"])
        return self._scores[row["id"]]

    def info(self):
        return {"endpoint": self.endpoint, "stored_predictions": bool(self.predictions),
                "tasks": sorted({r["task"] for r in self.rows}), "views": sorted({r.get("view", "") for r in self.rows}),
                "rows": len(self.rows)}

    def sample(self, req):
        if not self.rows:
            raise ValueError("Start the viewer with --tasks (prepared *_tasks.jsonl) for benchmark samples")
        rows = [r for r in self.rows if (not req.get("task") or r["task"] == req["task"])
                and (not req.get("view") or r.get("view") == req["view"])]
        if req.get("id"):
            rows = [r for r in self.rows if r["id"] == req["id"].strip()]
        if self.predictions and req.get("max_reward") not in (None, ""):
            rows = [r for r in rows if self.score(r) <= float(req["max_reward"])]
        if not rows:
            raise ValueError("No question matches these filters")
        row = random.choice(rows)
        with Image.open(row["images"][0]) as im:
            im = im.convert("RGB")
        prompt = row["messages"][0]["content"].replace("<image>", "").strip()
        if self.predictions:
            raw, finish = self.predictions[row["id"]], "stored"
        else:
            raw, finish = self.chat(Path(row["images"][0]).read_bytes(), prompt)
        target = parse_target(row["target"])
        result = {"image": data_url(im), "width": im.width, "height": im.height, "id": row["id"], "task": row["task"],
                  "view": row.get("view"), "view_ops": row.get("view_ops"), "prompt": prompt, "raw": raw,
                  "finish_reason": finish, "reward": round(reward(raw, row["task"], row["target"]), 3),
                  "gold": [], "pred": [], "query": [], "gold_text": None, "pred_text": None}
        if row["task"] in BOX_TASKS:
            result["gold"] = [{"px": to_pixels(b["bbox_2d"], im.width, im.height), "label": b["label"]} for b in target["boxes"]]
            boxes = parse_boxes(raw)
            result["parsed"] = boxes is not None
            result["pred"] = [{"px": to_pixels(b["bbox_2d"], im.width, im.height), "label": b["label"]} for b in boxes or []]
        else:
            result["gold_text"], result["pred_text"] = target["text"], answer(raw)
        # Boxes named in the question (bbox_ocr / region_ocr / relation anchor / marked_ocr coordinates).
        result["query"] = [to_pixels(json.loads(m), im.width, im.height) for m in PROMPT_BOX.findall(prompt)]
        return result


def handler(viewer):
    class Handler(BaseHTTPRequestHandler):
        def reply(self, code, body, kind="application/json; charset=utf-8"):
            data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                # Read on every request so edits to index.html show up on reload.
                self.reply(200, (HERE / "index.html").read_bytes(), "text/html; charset=utf-8")
            elif self.path == "/api/info":
                self.reply(200, viewer.info())
            else:
                self.reply(404, {"error": "not found"})

        def do_POST(self):
            try:
                req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
                if self.path == "/api/run":
                    self.reply(200, viewer.run(req))
                elif self.path == "/api/sample":
                    self.reply(200, viewer.sample(req))
                else:
                    self.reply(404, {"error": "not found"})
            except Exception as exc:  # Shown in the page; the server keeps running.
                self.reply(400, {"error": f"{type(exc).__name__}: {exc}"})

        def log_message(self, fmt, *args):
            pass

    return Handler


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--endpoint", help="OpenAI-compatible server, e.g. http://127.0.0.1:8010/v1")
    p.add_argument("--model", default="bank-ocr", help="served_model_name of the server")
    p.add_argument("--tasks", help="Prepared *_tasks.jsonl for benchmark samples")
    p.add_argument("--predictions", help="Stored predictions for --tasks (no server needed)")
    p.add_argument("--max-size", type=int, nargs=2, default=[2300, 1600], metavar=("LONG", "SHORT"),
                   help="Same image_max_size as prepare (default 2300 1600)")
    p.add_argument("--pdf-dpi", type=int, default=200, help="Resolution for rendering PDF pages")
    p.add_argument("--max-tokens", type=int, default=2048)
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=7860)
    a = p.parse_args()
    if not a.endpoint and not a.predictions:
        p.error("Give --endpoint (ask the model) and/or --tasks with --predictions (stored answers)")
    if a.predictions and not a.tasks:
        p.error("--predictions needs --tasks")
    viewer = Viewer(a)
    server = ThreadingHTTPServer((a.host, a.port), handler(viewer))
    print(f"OCR viewer on http://{a.host}:{a.port}  (Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
