"""모델 실행: 문항을 OpenAI 호환 Chat Completions API 로 보내 예측을 저장한다.

  python -m docgen.bench run --bench bench_out --pred preds/qwen7b \\
      --base-url http://localhost:8000/v1 --model Qwen/Qwen2.5-VL-7B-Instruct

vLLM·SGLang·LMDeploy 의 OpenAI 호환 서버, 또는 같은 형식을 받는 상용 API 에 쓸 수 있다.
API 키는 --api-key-env 로 지정한 환경변수(기본 OPENAI_API_KEY)에서 읽는다.
이미 예측한 문항은 건너뛰므로 중단 후 같은 명령으로 이어서 돌릴 수 있다.

  --oracle   정답을 그대로 출력으로 쓴다 (채점기 점검용: 모든 과제가 100% 가 나와야 한다)
"""
from __future__ import annotations

import base64
import io
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .evaluate import load_items

MAX_TOKENS = {"ocr_page": 4096, "kie": 2048, "marks": 1024, "cross_check": 1024, "doc_check": 512,
              "ocr_field": 256, "classify": 128, "review": 256}


def oracle_output(item: dict) -> str:
    a = item["answer"]
    if item["task"] == "ocr_page":
        return "\n".join(a)
    return a if isinstance(a, str) else json.dumps(a, ensure_ascii=False)


def _image_url(path: Path, max_side: int | None) -> str:
    from PIL import Image

    img = Image.open(path)
    if max_side and max(img.size) > max_side:
        k = max_side / max(img.size)
        img = img.resize((round(img.width * k), round(img.height * k)), Image.LANCZOS)
    buf = io.BytesIO()
    if path.suffix.lower() in (".jpg", ".jpeg"):
        img.convert("RGB").save(buf, "JPEG", quality=92)
        mime = "image/jpeg"
    else:
        img.save(buf, "PNG")
        mime = "image/png"
    return f"data:{mime};base64,{base64.b64encode(buf.getvalue()).decode()}"


class Client:
    def __init__(self, base_url: str, model: str, api_key: str | None, max_side: int | None, temperature: float,
                 timeout: float, system: str | None):
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.model, self.api_key, self.max_side = model, api_key, max_side
        self.temperature, self.timeout, self.system = temperature, timeout, system

    def __call__(self, bench: Path, item: dict) -> dict:
        content = [{"type": "image_url", "image_url": {"url": _image_url(bench / p, self.max_side)}} for p in item["images"]]
        content.append({"type": "text", "text": item["prompt"]})
        messages = ([{"role": "system", "content": self.system}] if self.system else []) + [{"role": "user", "content": content}]
        body = {"model": self.model, "messages": messages, "temperature": self.temperature,
                "max_tokens": MAX_TOKENS.get(item["task"], 1024)}
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        req = urllib.request.Request(self.url, data=json.dumps(body).encode(), headers=headers, method="POST")
        delay = 2.0
        for attempt in range(5):
            t0 = time.time()
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    r = json.loads(resp.read())
                return {"output": r["choices"][0]["message"].get("content") or "", "latency": round(time.time() - t0, 2),
                        "usage": r.get("usage")}
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors="replace")[:300]
                if e.code not in (408, 429, 500, 502, 503, 504) or attempt == 4:
                    return {"output": None, "error": f"HTTP {e.code}: {msg}"}
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                if attempt == 4:
                    return {"output": None, "error": str(e)}
            time.sleep(delay)
            delay *= 2
        return {"output": None, "error": "retries exhausted"}


def run(args) -> None:
    bench, pred = Path(args.bench), Path(args.pred)
    pred.mkdir(parents=True, exist_ok=True)
    tasks = [t.strip() for t in args.tasks.split(",")] if args.tasks != "all" else None
    items = load_items(bench, tasks)
    if not items:
        sys.exit(f"{bench}/tasks 에 문항이 없습니다")
    if args.oracle:
        call = None
    else:
        if not args.base_url or not args.model:
            sys.exit("--base-url 과 --model 이 필요합니다 (또는 --oracle)")
        call = Client(args.base_url, args.model, os.environ.get(args.api_key_env), args.max_side, args.temperature,
                      args.timeout, args.system)
    (pred / "run.json").write_text(json.dumps({"model": "oracle" if args.oracle else args.model, "base_url": args.base_url,
                                               "max_side": args.max_side, "temperature": args.temperature,
                                               "bench": str(bench)}, ensure_ascii=False, indent=1), encoding="utf-8")
    for task, its in items.items():
        path = pred / f"{task}.jsonl"
        done = set()
        if path.exists():
            for ln in path.open(encoding="utf-8"):
                if ln.strip():
                    r = json.loads(ln)
                    if r.get("output") is not None:
                        done.add(r["id"])
        todo = [it for it in its if it["id"] not in done]
        if args.limit:
            todo = todo[: max(0, args.limit - len(done))]
        if not todo:
            print(f"{task}: 이미 완료 ({len(done)})", file=sys.stderr)
            continue
        lock = threading.Lock()
        n_err = 0
        with open(path, "a", encoding="utf-8") as fh:
            def save(it, r):
                with lock:
                    fh.write(json.dumps({"id": it["id"], **r}, ensure_ascii=False) + "\n")
                    fh.flush()

            if call is None:
                for it in todo:
                    save(it, {"output": oracle_output(it)})
            else:
                with ThreadPoolExecutor(args.workers) as ex:
                    futs = {ex.submit(call, bench, it): it for it in todo}
                    for k, fu in enumerate(as_completed(futs), 1):
                        r = fu.result()
                        n_err += r.get("output") is None
                        save(futs[fu], r)
                        print(f"\r{task}: {k}/{len(todo)} (오류 {n_err})", end="", file=sys.stderr)
                print(file=sys.stderr)
        if n_err:
            print(f"  {task}: 오류 {n_err}건 — 다시 실행하면 오류 난 문항만 다시 보냅니다", file=sys.stderr)
    print(f"예측 → {pred}")
