"""0단계 측정: 서류 한 장 + 질문 N개를 지금처럼 동시에(async) 보낼 때, 이미지 읽기(prefill)와 답 생성(decode)에 각각 몇 초가 드는가.

docgen 벤치마크 세트에서 이미지 한 장짜리 문항(classify, kie, marks)을 페이지별로 묶고, 페이지마다 아래 방식으로 보낸다.

  async  질문 N개를 한꺼번에 (지금 운영 방식)
  warm   이미지 + 짧은 글로 max_tokens=1 요청을 먼저 보내 기다린 뒤(= 이미지 읽기 시간), 질문 N개를 한꺼번에
  serial 질문을 하나씩 차례로 (비교용)

--split-fields 를 주면 kie·marks 를 항목 하나에 질문 하나로 나눈다 (운영에서 항목마다 묻는 방식).
방식마다 이미지 왼쪽 위 한 픽셀을 바꿔 보내, 앞 방식의 프리픽스·인코더 캐시가 다음 방식에 섞이지 않게 한다.

  python research/inference-speed/measure_page.py --bench out/bench_test --base-url http://127.0.0.1:8000/v1 \
      --model bank-ocr --pages 20 --split-fields --out runs/measure1

결과: <out>/requests.jsonl (질문마다), <out>/pages.jsonl (페이지·방식마다), <out>/summary.json
"""
import argparse
import base64
import io
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from docgen.bench.prompts import P_KIE, P_MARKS  # noqa: E402

PAGE_TASKS = ("classify", "kie", "marks")
MAX_TOKENS = {"classify": 128, "kie": 2048, "marks": 1024}
METRICS = ("vllm:prefix_cache_queries", "vllm:prefix_cache_hits", "vllm:prompt_tokens", "vllm:generation_tokens")


def load_pages(bench, split_fields, limit):
    pages = defaultdict(list)
    for task in PAGE_TASKS:
        path = bench / "tasks" / f"{task}.jsonl"
        if not path.exists():
            continue
        for line in path.open(encoding="utf-8"):
            if not line.strip():
                continue
            it = json.loads(line)
            if len(it["images"]) != 1:
                continue
            for q in split(it) if split_fields else [it]:
                pages[it["images"][0]].append({"id": q["id"], "task": it["task"], "prompt": q["prompt"]})
    keys = sorted(pages)[:limit] if limit else sorted(pages)
    return [(k, pages[k]) for k in keys]


def split(it):
    """kie·marks 문항을 항목 하나짜리 문항들로 나눈다. 항목 줄은 build.py 가 만든 '- 키: …' 형식."""
    if it["task"] not in ("kie", "marks"):
        return [it]
    lines = [ln for ln in it["prompt"].splitlines() if ln.startswith("- ")]
    template = P_KIE if it["task"] == "kie" else P_MARKS
    return [{"id": f"{it['id']}/{re.match(r'- ([^:]+):', ln).group(1)}", "prompt": template.format(items=ln)}
            for ln in lines]


def image_url(path, max_side, nonce):
    from PIL import Image

    img = Image.open(path).convert("RGB")
    if max_side and max(img.size) > max_side:
        k = max_side / max(img.size)
        img = img.resize((round(img.width * k), round(img.height * k)), Image.LANCZOS)
    r, g, b = img.getpixel((0, 0))
    img.putpixel((0, 0), (r, g, (b + nonce) % 256))  # 캐시 분리용. 내용에는 영향 없음
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


class Client:
    def __init__(self, args):
        self.url = args.base_url.rstrip("/") + "/chat/completions"
        self.metrics_url = args.metrics_url or re.sub(r"/v1/?$", "", args.base_url.rstrip("/")) + "/metrics"
        self.model, self.timeout, self.stream = args.model, args.timeout, not args.no_stream
        self.headers = {"Content-Type": "application/json"}
        if os.environ.get(args.api_key_env):
            self.headers["Authorization"] = "Bearer " + os.environ[args.api_key_env]

    def ask(self, image, prompt, max_tokens):
        body = {"model": self.model, "temperature": 0, "max_tokens": max_tokens, "stream": self.stream,
                "messages": [{"role": "user", "content": [{"type": "image_url", "image_url": {"url": image}},
                                                          {"type": "text", "text": prompt}]}],
                "chat_template_kwargs": {"enable_thinking": False}}
        if self.stream:
            body["stream_options"] = {"include_usage": True}
        req = urllib.request.Request(self.url, data=json.dumps(body).encode(), headers=self.headers)
        t0 = time.monotonic()
        first, text, usage = None, [], None
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            if not self.stream:
                r = json.load(resp)
                text, usage = [r["choices"][0]["message"].get("content") or ""], r.get("usage")
            else:
                for raw in resp:
                    line = raw.decode("utf-8", "replace").strip()
                    if not line.startswith("data:") or line == "data: [DONE]":
                        continue
                    chunk = json.loads(line[5:])
                    usage = chunk.get("usage") or usage
                    for c in chunk.get("choices") or []:
                        piece = (c.get("delta") or {}).get("content")
                        if piece:
                            first = first if first is not None else time.monotonic() - t0
                            text.append(piece)
        usage = usage or {}
        return {"ttft": first, "latency": time.monotonic() - t0, "output": "".join(text),
                "prompt_tokens": usage.get("prompt_tokens"), "completion_tokens": usage.get("completion_tokens"),
                "cached_tokens": (usage.get("prompt_tokens_details") or {}).get("cached_tokens")}

    def metrics(self):
        try:
            with urllib.request.urlopen(self.metrics_url, timeout=10) as resp:
                text = resp.read().decode()
        except (urllib.error.URLError, TimeoutError):
            return None
        out = {}
        for line in text.splitlines():
            for name in METRICS:
                if line.startswith(name + "_total") or line.startswith(name + "{") or line.startswith(name + " "):
                    out[name] = out.get(name, 0.0) + float(line.rsplit(" ", 1)[1])
        return out


def run_together(client, image, questions, start):
    results = [None] * len(questions)

    def one(i, q):
        try:
            r = client.ask(image, q["prompt"], MAX_TOKENS[q["task"]])
        except Exception as exc:  # 한 문항 오류가 측정 전체를 멈추지 않게
            r = {"error": f"{type(exc).__name__}: {exc}"}
        results[i] = {**q, **r, "end": time.monotonic() - start}

    threads = [threading.Thread(target=one, args=(i, q)) for i, q in enumerate(questions)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return results


def measure(client, image, questions, mode):
    start = time.monotonic()
    warm = None
    if mode == "serial":
        results = []
        for q in questions:
            r = client.ask(image, q["prompt"], MAX_TOKENS[q["task"]])
            results.append({**q, **r, "end": time.monotonic() - start})
    else:
        if mode == "warm":
            warm = client.ask(image, ".", 1)["latency"]
        results = run_together(client, image, questions, start)
    return {"page_time": time.monotonic() - start, "warmup": warm}, results


def summarize(pages):
    out = {}
    for mode in sorted({p["mode"] for p in pages}):
        ps = [p for p in pages if p["mode"] == mode]
        row = {"pages": len(ps), "questions_per_page": median(p["questions"] for p in ps),
               "page_time_p50": median(p["page_time"] for p in ps), "errors": sum(p["errors"] for p in ps)}
        warm = [p["warmup"] for p in ps if p["warmup"] is not None]
        if warm:
            row["warmup_p50"] = median(warm)
            row["warmup_share_p50"] = median(p["warmup"] / p["page_time"] for p in ps if p["warmup"] is not None)
        for key in ("prompt_tokens_p50", "completion_tokens_max_p50", "prefix_hit_rate"):
            vals = [p[key] for p in ps if p.get(key) is not None]
            if vals:
                row[key] = median(vals)
        out[mode] = row
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--bench", required=True, type=Path, help="docgen.bench build 결과 세트 폴더")
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--modes", default="async,warm", help="async, warm, serial 중 쉼표로")
    ap.add_argument("--pages", type=int, default=20, help="잴 페이지 수 (0 = 전부)")
    ap.add_argument("--split-fields", action="store_true", help="kie·marks 를 항목 하나에 질문 하나로")
    ap.add_argument("--max-side", type=int, default=2300, help="긴 변 상한 (학습 입력과 같게)")
    ap.add_argument("--timeout", type=float, default=600)
    ap.add_argument("--no-stream", action="store_true", help="서버가 스트리밍을 못 하면. 첫 토큰 시간은 못 잼")
    ap.add_argument("--metrics-url", help="vLLM /metrics 주소 (기본: base-url 에서 /v1 을 뗀 곳)")
    ap.add_argument("--api-key-env", default="INTERNAL_MODEL_API_KEY")
    args = ap.parse_args()

    pages = load_pages(args.bench, args.split_fields, args.pages)
    if not pages:
        sys.exit(f"{args.bench}/tasks 에 이미지 한 장짜리 classify·kie·marks 문항이 없습니다")
    modes = [m.strip() for m in args.modes.split(",") if m.strip()]
    if set(modes) - {"async", "warm", "serial"}:
        sys.exit("--modes 는 async, warm, serial 중에서 고르세요")
    client = Client(args)
    args.out.mkdir(parents=True, exist_ok=True)
    print(f"페이지 {len(pages)}장, 페이지당 질문 {median(len(q) for _, q in pages)}개 (중앙값), 방식 {modes}", file=sys.stderr)

    page_rows = []
    with (args.out / "requests.jsonl").open("w", encoding="utf-8") as req_f:
        for n, (image_path, questions) in enumerate(pages, 1):
            for m_i, mode in enumerate(modes):
                image = image_url(args.bench / image_path, args.max_side, nonce=m_i + 1)
                before = client.metrics()
                page, results = measure(client, image, questions, mode)
                after = client.metrics()
                ok = [r for r in results if "error" not in r]
                row = {"page": image_path, "mode": mode, "questions": len(questions),
                       "errors": len(results) - len(ok), **page}
                if ok and ok[0].get("prompt_tokens") is not None:
                    row["prompt_tokens_p50"] = median(r["prompt_tokens"] for r in ok)
                if ok and ok[0].get("completion_tokens") is not None:
                    row["completion_tokens_max_p50"] = max(r["completion_tokens"] for r in ok)
                if before and after and after.get("vllm:prefix_cache_queries", 0) > before.get("vllm:prefix_cache_queries", 0):
                    q = after["vllm:prefix_cache_queries"] - before.get("vllm:prefix_cache_queries", 0)
                    row["prefix_hit_rate"] = (after.get("vllm:prefix_cache_hits", 0) - before.get("vllm:prefix_cache_hits", 0)) / q
                page_rows.append(row)
                for r in results:
                    req_f.write(json.dumps({"page": image_path, "mode": mode, **r}, ensure_ascii=False) + "\n")
            print(f"\r{n}/{len(pages)}", end="", file=sys.stderr)
    print(file=sys.stderr)
    with (args.out / "pages.jsonl").open("w", encoding="utf-8") as f:
        for row in page_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    summary = summarize(page_rows)
    (args.out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
