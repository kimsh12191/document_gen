"""실행: 묶음마다 방법대로 모델(OpenAI 호환 서버, 예: vLLM)에 묻고, 문서 목록으로 정리해 저장한다.

방법
  pagewise   한 쪽씩 원래 해상도로 읽는다. 앞 쪽 답으로 상태(--state none|doc|tail|context)를 만들어 다음 쪽 질문에 넣는다.
             state=none 은 상태 없이 쪽마다 따로 읽고 'continues' 로만 이어 붙이는 비교 방법이다.
  allatonce  묶음의 모든 쪽을 한 질문에 넣는다. 쪽마다 같은 비율로 줄여 이미지 토큰 합을 --budget 이하로 (지금 2부 방식).

--oracle 이면 모델 대신 정답을 답으로 써서 파이프라인 전체(상태·병합·채점)가 맞는지 확인한다 (점수 100% 가 나와야 함).
--simulate p 는 정답에 일부러 오류(행 빠뜨림·칸 바꿈, 확률 p)를 넣는다. 채점과 viewer 가 오류를 잡는지 보는 시험용이며
모델 결과가 아니다.
"""
from __future__ import annotations

import copy
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from docgen.bench.metrics import parse_json

from .common import data_url, dumps, load_resized, page_budget, tokens_of
from .gen import load
from .pages import all_prompt, doc_content, page_answer, page_views, run_pagewise


class Client:
    def __init__(self, base_url: str, model: str, max_tokens: int, timeout: float = 900, api_key_env: str = "INTERNAL_MODEL_API_KEY"):
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.model, self.max_tokens, self.timeout = model, max_tokens, timeout
        self.headers = {"Content-Type": "application/json"}
        if os.environ.get(api_key_env):
            self.headers["Authorization"] = "Bearer " + os.environ[api_key_env]

    def ask(self, images, prompt: str) -> tuple[str | None, dict]:
        content = [{"type": "image_url", "image_url": {"url": data_url(img)}} for img in images]
        content.append({"type": "text", "text": prompt})
        body = {"model": self.model, "messages": [{"role": "user", "content": content}], "temperature": 0,
                "max_tokens": self.max_tokens, "chat_template_kwargs": {"enable_thinking": False}}
        req = urllib.request.Request(self.url, data=json.dumps(body).encode(), headers=self.headers)
        delay = 2.0
        for attempt in range(4):
            t0 = time.monotonic()
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    r = json.load(resp)
                u = r.get("usage") or {}
                return r["choices"][0]["message"].get("content"), {
                    "prompt_tokens": u.get("prompt_tokens"), "completion_tokens": u.get("completion_tokens"),
                    "finish_reason": r["choices"][0].get("finish_reason"), "latency": time.monotonic() - t0}
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors="replace")[:300]
                if e.code not in (408, 429, 500, 502, 503, 504) or attempt == 3:
                    return None, {"error": f"HTTP {e.code}: {msg}"}
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                if attempt == 3:
                    return None, {"error": str(e)}
            time.sleep(delay)
            delay *= 2
        return None, {"error": "retries exhausted"}


def oracle_documents(bundle: dict, labels: dict) -> list[dict]:
    pages: dict[str, list[int]] = {}
    for i, p in enumerate(bundle["pages"], 1):
        pages.setdefault(p["doc"], []).append(i)
    out = []
    for sid in bundle["docs"]:
        lb = labels[sid]
        out.append({"type": lb["doc_type"], "name": lb["doc_name"], "pages": pages[sid], **doc_content(page_views(lb))})
    return out


def oracle_page(bundle: dict, labels: dict, i: int, cache: dict) -> dict:
    p = bundle["pages"][i]
    lb = labels[p["doc"]]
    if p["doc"] not in cache:
        cache[p["doc"]] = page_views(lb)
    return page_answer(lb, cache[p["doc"]], p["page"])


def simulate_errors(obj: dict, rng: random.Random, p: float) -> dict:
    """시험용: 목록 행을 확률 p 로 빠뜨리거나 칸 하나를 바꾼다 (쪽 단위 답, 또는 한 번에 넣기의 문서)."""
    obj = copy.deepcopy(obj)
    for path, rows in (obj.get("lists") or {}).items():
        kept = []
        for r in rows:
            x = rng.random()
            if x < p / 2:
                continue  # 행 빠뜨림
            if x < p and isinstance(r, dict) and r:
                k = rng.choice(sorted(r))
                r[k] = f"{r[k]}?" if isinstance(r[k], str) else r[k]  # 칸 하나 틀림
            kept.append(r)
        obj["lists"][path] = kept
    return obj


def normalize_documents(obj) -> list[dict]:
    """한 번에 넣기 답 → 문서 목록. 모양이 틀리면 빈 목록."""
    docs = obj.get("documents") if isinstance(obj, dict) else obj
    if not isinstance(docs, list):
        return []
    out = []
    for d in docs:
        if not isinstance(d, dict):
            continue
        pages = [int(x) for x in d.get("pages") or [] if isinstance(x, (int, float)) or str(x).isdigit()]
        lists = d.get("lists") if isinstance(d.get("lists"), dict) else {}
        out.append({"type": d.get("type"), "name": d.get("name"), "pages": pages,
                    "fields": d.get("fields") if isinstance(d.get("fields"), dict) else {},
                    "lists": {k: v for k, v in lists.items() if isinstance(v, list)}})
    return out


def run_bundle(bundle: dict, labels: dict, data_dir: Path, method: str, state: str, client: Client | None,
               budget: int, simulate: float = 0.0) -> dict:
    t0 = time.monotonic()
    usage, image_tokens, states = [], [], []
    sim_rng = random.Random(f"simulate:{bundle['id']}:{method}:{state}")
    n = len(bundle["pages"])
    if method == "pagewise":
        cache: dict = {}

        def answer(i, prompt):
            if client is None:
                obj = oracle_page(bundle, labels, i, cache)
                if simulate:
                    obj = simulate_errors(obj, sim_rng, simulate)
                return dumps(obj), obj
            img = load_resized(data_dir / bundle["pages"][i]["image"])
            image_tokens.append(tokens_of(*img.size))
            raw, u = client.ask([img], prompt)
            usage.append(u)
            return raw, parse_json(raw)

        raws, docs, states = run_pagewise(answer, n, state)
    elif method == "allatonce":
        if client is None:
            docs = oracle_documents(bundle, labels)
            if simulate:
                docs = [simulate_errors(d, sim_rng, simulate) for d in docs]
            raws = [dumps({"documents": docs})]
        else:
            per = page_budget(n, budget)
            imgs = [load_resized(data_dir / p["image"], per) for p in bundle["pages"]]
            image_tokens += [tokens_of(*im.size) for im in imgs]
            raw, u = client.ask(imgs, all_prompt(n))
            usage.append(u)
            raws, docs = [raw], normalize_documents(parse_json(raw))
    else:
        raise ValueError(f"알 수 없는 방법: {method}")
    return {"bundle": bundle["id"], "method": method, "state": state if method == "pagewise" else None,
            "oracle": client is None, "simulated_errors": simulate if client is None else 0, "outputs": raws, "docs": docs, "states": states, "usage": usage,
            "image_tokens": image_tokens,
            "latency": time.monotonic() - t0}


def run(data_dir, out, method: str, state: str = "context", client: Client | None = None, workers: int = 8,
        budget: int = 12000, limit: int = 0, simulate: float = 0.0) -> Path:
    data_dir, out = Path(data_dir), Path(out)
    bundles, labels = load(data_dir)
    if limit:
        bundles = bundles[:limit]
    done = set()
    if out.exists():
        done = {json.loads(ln)["bundle"] for ln in out.open(encoding="utf-8") if ln.strip()}
    todo = [b for b in bundles if b["id"] not in done]
    out.parent.mkdir(parents=True, exist_ok=True)
    meta = out.with_suffix(".meta.json")
    meta.write_text(json.dumps({"data": str(data_dir), "method": method, "state": state, "budget": budget,
                                "model": client.model if client else "oracle", "simulate": simulate},
                               ensure_ascii=False, indent=1),
                    encoding="utf-8")
    with out.open("a", encoding="utf-8") as f, ThreadPoolExecutor(max(1, workers)) as ex:
        futs = {ex.submit(run_bundle, b, labels, data_dir, method, state, client, budget, simulate): b for b in todo}
        for k, fu in enumerate(as_completed(futs), 1):
            f.write(json.dumps(fu.result(), ensure_ascii=False) + "\n")
            f.flush()
            print(f"\r{method}/{state}: {k}/{len(todo)}", end="", file=sys.stderr)
    print(file=sys.stderr)
    return out
