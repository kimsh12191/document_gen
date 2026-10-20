"""Banking-task viewer: browse benchmark answers of the pipeline's models side by side, and try
your own documents. A small local web page (viewer/bank.html); see viewer/README.md. Run from bank/:

    python viewer/bank_viewer.py --config configs/bank_pipeline.json                    # stored answers only
    python viewer/bank_viewer.py --config configs/bank_pipeline.json --endpoint http://127.0.0.1:8011/v1
    bash viewer/bank_start.sh runs/bank1/merged/sft-<버전>-checkpoint-<번호> 1          # model + page together
"""
import argparse
import base64
import io
import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # bank/
OCR = ROOT.parent / "ocr"               # 1부 OCR 코드와 OCR viewer (PDF 그리기를 같이 쓴다)
sys.path[:0] = [str(ROOT), str(OCR), str(OCR / "viewer")]

from bank_ocr.data import dumps, read_json, read_jsonl  # noqa: E402
from bank_ocr.inference import index_predictions  # noqa: E402
from bank_ocr.settings import load_settings  # noqa: E402
from bank_task.cli import resolve_data  # noqa: E402
from bank_task.prepare import fit_size, sample_caps  # noqa: E402
from bank_task.score import docgen, reward  # noqa: E402
from ocr_viewer import render_pdf  # noqa: E402

TASK_NAMES = {"ocr_field": "값 칸 OCR", "ocr_page": "전체 받아쓰기", "classify": "서류 분류", "kie": "정보 추출",
              "marks": "체크·도장·서명", "doc_check": "서류 구비 확인", "cross_check": "서류 대조", "review": "심사 질의"}
FREE_TASKS = {"doc_check": "서류 구비 확인", "cross_check": "서류 대조", "review": "심사 질의", "kie": "정보 추출",
              "classify": "서류 분류", "ocr_page": "전체 받아쓰기", "custom": "직접 질문"}
TAGS = (("_other_person", "다른 고객 서류"), ("_other", "다른 고객 서류"), ("_aged", "발급일 바뀜"), ("_extra", "업무와 무관한 서류"))
MAX_FREE_IMAGES = 16  # the model server allows 16 images per question


def jpeg_url(im, long_side=1600, quality=85):
    """Image for the page (display only; the model gets the PNG at its own size)."""
    im = im.convert("RGB")
    if max(im.size) > long_side:
        k = long_side / max(im.size)
        im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def png_bytes(im):
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return buf.getvalue()


class Viewer:
    def __init__(self, a):
        self.endpoint = a.endpoint.rstrip("/") if a.endpoint else None
        self.model, self.max_tokens, self.timeout, self.dpi = a.model, a.max_tokens, a.timeout, a.pdf_dpi
        data, workdir = self.locate(a)
        done = read_json(data / "DONE.json")
        self.factor = done.get("pixels_per_token_side", 32)
        self.per_image = done.get("max_image_tokens_per_image", 3600)
        self.per_sample = done.get("max_image_tokens_per_sample", 12000)
        self.E = docgen("evaluate")
        self.P = docgen("prompts")
        self.rows = {r["id"]: r for r in read_jsonl(data / "benchmark_tasks.jsonl")}
        self.items = {it["id"]: it for it in read_jsonl(data / "benchmark_items.jsonl") if it["id"] in self.rows}
        bench = Path(done.get("sources", {}).get("benchmark", {}).get("path") or "")
        self.doc_names = read_json(bench / "meta.json").get("doc_names", {}) if (bench / "meta.json").is_file() else {}
        self.models = self.load_models(workdir, a.predictions)
        print(f"benchmark {len(self.items)} items, models: " + ", ".join(m["label"] for m in self.models), flush=True)
        self.scores = {}  # (model index, id) -> (reward, main metric, parse_fail)
        for i, m in enumerate(self.models):
            for qid, out in m["preds"].items():
                if qid in self.items:
                    self.scores[i, qid] = self.score(self.items[qid], out)
        # Business types for the free test, from the benchmark's document-check questions.
        self.workflows = {}
        for it in self.items.values():
            if it["task"] == "doc_check" and it["meta"].get("task_name"):
                self.workflows.setdefault(it["meta"]["task_name"], it["eval"]["required"])

    @staticmethod
    def locate(a):
        if a.config:
            path = Path(a.config).resolve()
            cfg = load_settings(path)
            d = resolve_data(cfg, path.parent)
            if d.get("docgen_root"):
                os.environ["DOCGEN_ROOT"] = d["docgen_root"]
            data = Path(a.data or d["output_dir"])
            workdir = Path(a.workdir) if a.workdir else (path.parent / cfg["workdir"]).resolve() / ("smoke" if a.smoke else "")
        else:
            if not a.data:
                raise SystemExit("Give --config configs/bank_pipeline.json (or --data with the prepared folder)")
            data, workdir = Path(a.data), Path(a.workdir) if a.workdir else None
        if a.docgen_root:
            os.environ["DOCGEN_ROOT"] = a.docgen_root
        if not (data / "DONE.json").is_file():
            raise SystemExit(f"{data} is not a prepared folder (run the pipeline's prepare stage first)")
        return data, workdir

    @staticmethod
    def load_models(workdir, extra):
        """Every benchmark prediction file the pipeline scored (reports/*.json), oldest model first."""
        models, seen = [], set()
        order = {"other": 0, "start": 1, "sft": 2, "grpo": 3}
        reports = []
        if workdir and (workdir / "reports").is_dir():
            for p in (workdir / "reports").glob("*.json"):
                if p.name.startswith("ocr-") or p.name.startswith("benchmark"):
                    continue
                r = read_json(p)
                if r.get("predictions") and Path(r["predictions"]).is_file():
                    reports.append((order.get(r.get("role"), 0), p.stat().st_mtime, r))
        for _, _, r in sorted(reports, key=lambda x: (x[0], x[1])):
            if r["predictions"] in seen:
                continue  # reports/grpo.json repeats the latest grpo-<run>.json
            seen.add(r["predictions"])
            models.append({"label": r["label"], "preds": index_predictions(r["predictions"])})
        for spec in extra or []:
            label, _, path = spec.partition("=")
            if not path:
                label, path = Path(spec).stem, spec
            models.append({"label": label, "preds": index_predictions(path)})
        return models

    def score(self, item, out):
        res = self.E.SCORERS[item["task"]](item, out)
        main = res["metrics"].get(self.E.MAIN[item["task"]])
        return round(reward(out, item), 4), (None if main is None else round(main, 4)), bool(res.get("parse_fail"))

    # -- model ---------------------------------------------------------------------------
    def chat(self, pngs, prompt):
        if not self.endpoint:
            raise ValueError("모델 서버 없이 띄웠습니다. viewer/bank_start.sh 로 모델과 함께 띄우세요")
        content = [{"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(b).decode("ascii")}}
                   for b in pngs] + [{"type": "text", "text": prompt}]
        payload = {"model": self.model, "messages": [{"role": "user", "content": content}], "temperature": 0,
                   "max_tokens": self.max_tokens, "stream": False, "chat_template_kwargs": {"enable_thinking": False}}
        headers = {"Content-Type": "application/json"}
        if os.getenv("INTERNAL_MODEL_API_KEY"):
            headers["Authorization"] = "Bearer " + os.environ["INTERNAL_MODEL_API_KEY"]
        req = Request(self.endpoint + "/chat/completions", data=dumps(payload).encode(), headers=headers)
        with urlopen(req, timeout=self.timeout) as response:
            choice = json.load(response)["choices"][0]
        return choice["message"].get("content") or "", choice.get("finish_reason")

    # -- benchmark -----------------------------------------------------------------------
    def info(self):
        def values(key, task=None):
            return sorted({str(it["meta"].get(key)) for it in self.items.values()
                           if (task is None or it["task"] == task) and it["meta"].get(key) is not None})
        tasks = {}
        for it in self.items.values():
            tasks[it["task"]] = tasks.get(it["task"], 0) + 1
        return {"endpoint": self.endpoint, "models": [m["label"] for m in self.models],
                "tasks": [[t, TASK_NAMES.get(t, t), tasks[t]] for t in self.E.TASK_ORDER if t in tasks],
                "workflows": [[k, v] for k, v in sorted(self.workflows.items())],
                "task_names": values("task_name"), "categories": values("category", "cross_check"),
                "cases": values("case", "cross_check"), "skills": values("skill", "review"),
                "free_tasks": list(FREE_TASKS.items()),
                "budget": {"per_image": self.per_image, "per_sample": self.per_sample, "max_images": MAX_FREE_IMAGES}}

    def matches(self, it, f):
        m = it["meta"]
        if f.get("task") and it["task"] != f["task"]:
            return False
        for key in ("task_name", "category", "case", "skill"):
            if f.get(key) and str(m.get(key)) != f[key]:
                return False
        if f.get("perturbed") in ("yes", "no") and bool(m.get("perturbed")) != (f["perturbed"] == "yes"):
            return False
        if f.get("q") and f["q"].strip() not in it["id"]:
            return False
        ok = lambda i: self.scores.get((i, it["id"]), (0,))[0] >= 0.999  # noqa: E731
        if f.get("model") not in (None, ""):
            i = int(f["model"])
            if (i, it["id"]) not in self.scores:
                return False
            verdict = f.get("verdict")
            if verdict == "wrong" and ok(i) or verdict == "right" and not ok(i):
                return False
        if f.get("better") not in (None, "") and f.get("worse") not in (None, ""):
            b, w = int(f["better"]), int(f["worse"])
            if not (ok(b) and not ok(w)):
                return False
        return True

    def list(self, f):
        ids = [qid for qid, it in self.items.items() if self.matches(it, f)]
        means = []
        for i, m in enumerate(self.models):
            got = [self.scores[i, q] for q in ids if (i, q) in self.scores]
            means.append({"label": m["label"], "n": len(got),
                          "reward": sum(s[0] for s in got) / len(got) if got else None,
                          "right": sum(s[0] >= 0.999 for s in got) / len(got) if got else None})
        rows = [{"id": q, "scores": [self.scores.get((i, q), (None,))[0] for i in range(len(self.models))]}
                for q in ids[:3000]]
        return {"n": len(ids), "rows": rows, "means": means}

    def page_label(self, src, k, n):
        stem = Path(src).stem
        page = re.search(r"_p(\d+)$", stem)
        if page:
            stem = stem[:page.start()]
        doc = max((d for d in self.doc_names if stem == d or stem.startswith(d + "_")), key=len, default=None)
        name = self.doc_names.get(doc, Path(src).stem) if doc else f"이미지 {k + 1}"
        rest = stem[len(doc):] if doc else ""
        tag = next((t for suffix, t in TAGS if rest.startswith(suffix)), None)
        if rest and not tag and not re.fullmatch(r"_\d+", rest):
            tag = "값을 바꾼 사본 (" + rest.lstrip("_") + ")"
        return {"name": name + (f" {page.group(1)}쪽" if page else ""), "tag": tag, "file": src, "index": f"{k + 1}/{n}"}

    def detail(self, it, outputs):
        """Per-task side-by-side view of the answer and each model's output."""
        task, gold = it["task"], it["answer"]
        parse = self.E.parse_json
        if task in ("kie", "marks"):
            labels = dict(re.findall(r"^- ([^:\n]+): ([^\n(]*)", self.rows[it["id"]]["messages"][0]["content"], re.M))
            flats = [self.E._flatten(parse(o)) if isinstance(parse(o), dict) else {} for o in outputs]
            sub = [self.E.SCORERS[task](it, o).get("sub", []) if o is not None else [] for o in outputs]
            rows = []
            for j, (key, g) in enumerate(gold.items()):
                rows.append({"key": key, "label": labels.get(key, "").strip(), "gold": g,
                             "pred": [f.get(key) for f in flats],
                             "ok": [s[j][2] if j < len(s) else False for s in sub]})
            return {"kind": "fields", "rows": rows}
        if task in ("doc_check", "cross_check"):
            return {"kind": "json", "gold": gold, "pred": [parse(o) for o in outputs]}
        return {"kind": "text", "gold": gold, "pred": [self.E.strip_answer(o) if o is not None else None for o in outputs]}

    def item(self, req):
        qid = req["id"]
        it, row = self.items[qid], self.rows[qid]
        imgs = []
        sources = row.get("source_images") or [None] * len(row["images"])
        for k, (p, src) in enumerate(zip(row["images"], sources)):
            with Image.open(p) as im:
                imgs.append({"url": jpeg_url(im), "w": im.width, "h": im.height,
                             **(self.page_label(src, k, len(row["images"])) if src else
                                {"name": f"이미지 {k + 1}", "tag": None, "file": p, "index": f"{k + 1}/{len(row['images'])}"})})
        outputs = [m["preds"].get(qid) for m in self.models]
        answers = []
        for i, m in enumerate(self.models):
            s = self.scores.get((i, qid))
            answers.append({"label": m["label"], "output": outputs[i], "reward": s[0] if s else None,
                            "main": s[1] if s else None, "parse_fail": s[2] if s else None})
        return {"id": qid, "task": it["task"], "task_title": TASK_NAMES.get(it["task"], it["task"]), "meta": it["meta"],
                "main_metric": self.E.METRIC_TITLE.get(self.E.MAIN[it["task"]], ""),
                "prompt": row["messages"][0]["content"].replace("<image>", ""), "images": imgs, "gold": it["answer"],
                "answers": answers, "detail": self.detail(it, outputs)}

    def ask(self, req):
        it, row = self.items[req["id"]], self.rows[req["id"]]
        prompt = row["messages"][0]["content"].replace("<image>", "")
        text, finish = self.chat([Path(p).read_bytes() for p in row["images"]], prompt)
        r, main, fail = self.score(it, text)
        return {"output": text, "finish_reason": finish, "reward": r, "main": main, "parse_fail": fail,
                "detail": self.detail(it, [text])}

    # -- free test -----------------------------------------------------------------------
    def pages(self, f, first_only):
        data = base64.b64decode(f["data"].split(",", 1)[1])
        out = []
        if data[:5] == b"%PDF-" or f["name"].lower().endswith(".pdf"):
            first, count = render_pdf(data, 1, self.dpi)
            out.append(first)
            for page in range(2, (1 if first_only else min(count, MAX_FREE_IMAGES)) + 1):
                out.append(render_pdf(data, page, self.dpi)[0])
        else:
            im = Image.open(io.BytesIO(data))
            for k in range(1 if first_only else min(getattr(im, "n_frames", 1), MAX_FREE_IMAGES)):
                im.seek(k)
                out.append(ImageOps.exif_transpose(im).convert("RGB"))
        return [(f["name"], k + 1, len(out), p) for k, p in enumerate(out)]

    def free(self, req):
        task, files = req.get("task"), req.get("files") or []
        if task not in FREE_TASKS:
            raise ValueError("과제를 고르세요")
        if not files:
            raise ValueError("서류 파일을 올리세요")
        if task in ("classify", "ocr_page", "kie") and len(files) > 1:
            raise ValueError(f"{FREE_TASKS[task]}: 서류 한 건(파일 하나)만 올리세요")
        pages = [p for f in files for p in self.pages(f, first_only=(task == "doc_check"))]
        if len(pages) > MAX_FREE_IMAGES:
            raise ValueError(f"이미지가 {len(pages)}장입니다. 한 번에 {MAX_FREE_IMAGES}장까지 보낼 수 있습니다")
        cap = sample_caps(len(pages), self.per_image, self.per_sample)
        sent = []
        for _, _, _, im in pages:  # same budget rule as prepare: every page gets the same share
            size = fit_size(*im.size, cap, self.factor)
            sent.append(im.resize(size, Image.LANCZOS) if size != im.size else im)
        customer, workflow = (req.get("customer") or "").strip(), (req.get("workflow") or "").strip()
        P = self.P
        if task == "classify":
            prompt = P.P_CLASSIFY
        elif task == "ocr_page":
            prompt = P.P_OCR_PAGE
        elif task == "kie":
            lines = [ln.strip() for ln in (req.get("items") or "").splitlines() if ln.strip()]
            if not lines:
                raise ValueError("뽑을 항목을 한 줄에 하나씩 적으세요 (예: 성명 / 주민등록번호)")
            items = [ln.split(":", 1) if ":" in ln else [ln, ln] for ln in lines]
            prompt = P.P_KIE.format(items="\n".join(f"- {k.strip()}: {v.strip()}" for k, v in items))
        elif task == "doc_check":
            required = [ln.strip() for ln in (req.get("required") or "").splitlines() if ln.strip()]
            if not (customer and workflow and required):
                raise ValueError("고객 성명, 업무, 필수 서류 목록을 채우세요")
            prompt = P.P_DOC_CHECK.format(customer=customer, task=workflow,
                                          required="\n".join(f"{i + 1}. {n}" for i, n in enumerate(required)))
        elif task == "cross_check":
            if not (customer and workflow):
                raise ValueError("고객 성명과 업무를 채우세요")
            prompt = P.P_CROSS.format(customer=customer, task=workflow, n=len(files), pages=len(pages))
        elif task == "review":
            if not (workflow and (req.get("question") or "").strip()):
                raise ValueError("업무와 질문을 채우세요")
            prompt = P.P_REVIEW.format(task=workflow, pages=len(pages), question=req["question"].strip())
        else:
            prompt = (req.get("prompt") or "").strip()
            if not prompt:
                raise ValueError("질문을 적으세요")
        text, finish = self.chat([png_bytes(im) for im in sent], prompt)
        return {"task": task, "prompt": prompt, "output": text, "finish_reason": finish,
                "parsed": self.E.parse_json(text) if task in ("doc_check", "cross_check", "kie") else None,
                "images": [{"url": jpeg_url(im), "w": s.width, "h": s.height, "name": f"{name} {page}쪽" if total > 1 else name,
                            "tag": None, "file": name, "index": f"{k + 1}/{len(pages)}"}
                           for k, ((name, page, total, im), s) in enumerate(zip(pages, sent))]}


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
                self.reply(200, (HERE / "bank.html").read_bytes(), "text/html; charset=utf-8")
            elif self.path == "/api/info":
                self.reply(200, viewer.info())
            else:
                self.reply(404, {"error": "not found"})

        def do_POST(self):
            try:
                req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
                routes = {"/api/list": viewer.list, "/api/item": viewer.item, "/api/ask": viewer.ask, "/api/free": viewer.free}
                if self.path not in routes:
                    return self.reply(404, {"error": "not found"})
                self.reply(200, routes[self.path](req))
            except Exception as exc:  # shown in the page; the server keeps running
                self.reply(400, {"error": f"{type(exc).__name__}: {exc}"})

        def log_message(self, fmt, *args):
            pass

    return Handler


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", help="Banking pipeline config (finds the prepared data, workdir and docgen code)")
    p.add_argument("--smoke", action="store_true", help="Show the rehearsal run (<workdir>/smoke)")
    p.add_argument("--data", help="Prepared folder (default: data.output_dir of --config)")
    p.add_argument("--workdir", help="Pipeline workdir with reports/ (default: workdir of --config)")
    p.add_argument("--docgen-root", help="Folder with docgen/ (default: data.docgen_root of --config)")
    p.add_argument("--predictions", action="append", help="Extra benchmark predictions: LABEL=path.jsonl (repeatable)")
    p.add_argument("--endpoint", help="Model server for asking again and for your own files, e.g. http://127.0.0.1:8011/v1")
    p.add_argument("--model", default="bank-ocr", help="served_model_name of the server")
    p.add_argument("--max-tokens", type=int, default=4096)
    p.add_argument("--timeout", type=int, default=600)
    p.add_argument("--pdf-dpi", type=int, default=200)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=7861)
    a = p.parse_args()
    viewer = Viewer(a)
    server = ThreadingHTTPServer((a.host, a.port), handler(viewer))
    print(f"Bank viewer on http://{a.host}:{a.port}  (Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
