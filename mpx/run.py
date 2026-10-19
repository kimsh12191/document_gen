"""실행: 묶음마다 방법대로 모델(OpenAI 호환 서버, 예: vLLM)에 묻고, 문서 목록으로 정리해 저장한다.

방법
  allatonce  묶음의 모든 쪽을 한 질문에 넣는다. 쪽마다 같은 비율로 줄여 이미지 토큰 합을 --budget 이하로
             (2부 은행 업무 모델이 여러 장 문항을 받는 방식과 같음: 합 12,000토큰, 13장이면 장당 약 920토큰).
  pagewise   한 쪽씩 원래 해상도로 따로 묻고, 모델이 답한 'continues'(앞 쪽에서 이어짐)로 문서를 이어 붙인다.
             해상도는 높고 답은 짧은 비교 조건이다.

--oracle 이면 모델 대신 정답을 답으로 써서 파이프라인 전체(병합·분류·채점)가 맞는지 확인한다 (점수 100% 가 나와야 함).
--simulate p 는 정답에 일부러 오류를 넣는다: 행마다 확률 p 로 건너뜀·잘못 읽음·다른 목록에 넣음·칸 하나 틀림, 답마다
확률 p 로 길이 상한에서 잘림, p/2 로 마지막 목록 끝 행을 빼고 스스로 끝냄. 넣은 수는 기록의 'injected'. 행 결과 분류
(rows.py)와 viewer 가 오류를 제대로 가르는지 보는 시험용이며 모델 결과가 아니다.

기록 한 줄: {bundle, method, budget, outputs(원문), truncated(답마다 잘림 여부), docs(문서 목록), usage,
image_tokens, latency, injected}. 잘린 답은 parse.py 로 잘리기 전까지 살린다.
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

from .common import data_url, dumps, load_resized, page_budget, tokens_of
from .gen import load
from .pages import all_prompt, doc_content, flatten, page_answer, page_views, run_pagewise, schema_hint
from .parse import parse_output


class Client:
    """OpenAI 호환 서버. sampling 으로 repetition_penalty 등을 직접 줄 수 있다. 주지 않으면 서버 기본값
    (vLLM 은 모델 폴더의 generation_config.json 값을 기본으로 쓴다)."""

    def __init__(self, base_url: str, model: str, max_tokens: int, timeout: float = 900,
                 api_key_env: str = "INTERNAL_MODEL_API_KEY", sampling: dict | None = None):
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.model, self.max_tokens, self.timeout = model, max_tokens, timeout
        self.sampling = dict(sampling or {})
        self.headers = {"Content-Type": "application/json"}
        if os.environ.get(api_key_env):
            self.headers["Authorization"] = "Bearer " + os.environ[api_key_env]

    def ask(self, images, prompt: str, sampling: dict | None = None) -> tuple[str | None, dict]:
        content = [{"type": "image_url", "image_url": {"url": data_url(img)}} for img in images]
        content.append({"type": "text", "text": prompt})
        body = {"model": self.model, "messages": [{"role": "user", "content": content}], "temperature": 0,
                "max_tokens": self.max_tokens, "chat_template_kwargs": {"enable_thinking": False},
                **self.sampling, **(sampling or {})}
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


def served_model(base_url: str, prefer: str | None = None, timeout: float = 30) -> str:
    """서버가 내놓은 모델 이름 (GET /models). prefer 가 그중에 있으면 그것, 아니면 첫 번째."""
    req = urllib.request.Request(base_url.rstrip("/") + "/models")
    key = os.environ.get("INTERNAL_MODEL_API_KEY")
    if key:
        req.add_header("Authorization", "Bearer " + key)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        ids = [m["id"] for m in json.load(resp).get("data", [])]
    if not ids:
        raise RuntimeError(f"{base_url} 가 모델을 내놓지 않습니다")
    return prefer if prefer in ids else ids[0]


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


GARBAGE = "#"


def simulate_rows(obj: dict, rng: random.Random, p: float, counts: dict) -> dict:
    """시험용: 목록 행마다 확률 p 로 오류 하나 (건너뜀, 잘못 읽음, 다른 목록에 넣음, 칸 하나 틀림). counts 에 센다."""
    obj = copy.deepcopy(obj)
    lists = obj.get("lists") or {}
    moved = []
    for path, rows in list(lists.items()):
        kept = []
        for r in rows:
            x = rng.random() / p if p else 1.0
            if x < 0.3:
                counts["skip"] = counts.get("skip", 0) + 1
                continue
            if x < 0.55 and isinstance(r, dict):
                r = {k: GARBAGE for k in flatten(r)}
                counts["misread"] = counts.get("misread", 0) + 1
            elif x < 0.7 and isinstance(r, dict):
                moved.append(r)
                counts["misplace"] = counts.get("misplace", 0) + 1
                continue
            elif x < 1.0 and isinstance(r, dict) and r:
                r = flatten(r)
                k = rng.choice(sorted(r))
                r[k] = f"{r[k]}X9"
                counts["partial"] = counts.get("partial", 0) + 1
            kept.append(r)
        lists[path] = kept
    if moved:
        lists["_misplaced"] = moved
    return obj


def simulate_cut(raw: str, obj, rng: random.Random, p: float, counts: dict, end_key: str) -> tuple[str, object, bool, str]:
    """시험용: 확률 p 로 답을 길이 상한에서 자르거나(원문 자름), p/2 로 마지막 목록 끝 행들을 빼고 스스로 끝낸다."""
    x = rng.random()
    if x < p and len(raw) > 40:
        cut = raw[:int(len(raw) * rng.uniform(0.5, 0.95))]
        counts["cut_length"] = counts.get("cut_length", 0) + 1
        o, _ = parse_output(cut)
        return cut, o, True, "length"
    if x < 1.5 * p and isinstance(obj, dict):
        o = copy.deepcopy(obj)
        holder = (o.get(end_key) or [{}])[-1] if end_key else o
        lists = (holder or {}).get("lists") or {}
        if lists:
            path = list(lists)[-1]
            k = rng.randint(1, max(1, len(lists[path]) // 3))
            lists[path] = lists[path][:-k] if len(lists[path]) > k else lists[path]
            counts["cut_stop"] = counts.get("cut_stop", 0) + 1
        return dumps(o), o, False, "stop"
    return raw, obj, False, "stop"


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


def run_bundle(bundle: dict, labels: dict, data_dir: Path, method: str, client: Client | None,
               budget: int, simulate: float = 0.0, hint: str = "") -> dict:
    t0 = time.monotonic()
    usage, image_tokens, truncated = [], [], []
    injected: dict = {}
    sim_rng = random.Random(f"simulate:{bundle['id']}:{method}")
    n = len(bundle["pages"])
    if method == "pagewise":
        cache: dict = {}

        def answer(i, prompt):
            if client is None:
                obj = oracle_page(bundle, labels, i, cache)
                raw, finish, cut = dumps(obj), "stop", False
                if simulate:
                    obj = simulate_rows(obj, sim_rng, simulate, injected)
                    raw, obj, cut, finish = simulate_cut(dumps(obj), obj, sim_rng, simulate, injected, "")
                usage.append({"finish_reason": finish})
                truncated.append(cut)
                return raw, obj
            img = load_resized(data_dir / bundle["pages"][i]["image"])
            image_tokens.append(tokens_of(*img.size))
            raw, u = client.ask([img], prompt)
            usage.append(u)
            obj, repaired = parse_output(raw)
            truncated.append(repaired or u.get("finish_reason") == "length")
            return raw, obj

        raws, docs = run_pagewise(answer, n, hint)
    elif method == "allatonce":
        if client is None:
            docs = oracle_documents(bundle, labels)
            raw, finish, cut = dumps({"documents": docs}), "stop", False
            if simulate:
                docs = [simulate_rows(d, sim_rng, simulate, injected) for d in docs]
                raw, obj, cut, finish = simulate_cut(dumps({"documents": docs}), {"documents": docs}, sim_rng,
                                                     simulate, injected, "documents")
                docs = normalize_documents(obj)
            raws = [raw]
            usage.append({"finish_reason": finish})
        else:
            per = page_budget(n, budget)
            imgs = [load_resized(data_dir / p["image"], per) for p in bundle["pages"]]
            image_tokens += [tokens_of(*im.size) for im in imgs]
            raw, u = client.ask(imgs, all_prompt(n, hint))
            usage.append(u)
            obj, cut = parse_output(raw)
            cut = cut or u.get("finish_reason") == "length"
            raws, docs = [raw], normalize_documents(obj)
        truncated.append(cut)
    else:
        raise ValueError(f"알 수 없는 방법: {method}")
    return {"bundle": bundle["id"], "method": method,
            "budget": budget, "oracle": client is None, "simulated_errors": simulate if client is None else 0,
            "injected": injected, "outputs": raws, "truncated": truncated, "docs": docs,
            "usage": usage, "image_tokens": image_tokens, "latency": time.monotonic() - t0}


def run(data_dir, out, method: str, client: Client | None = None, workers: int = 8,
        budget: int = 12000, limit: int = 0, simulate: float = 0.0, hint: bool = True) -> Path:
    """묶음마다 실행해 <out> 에 한 줄씩. hint 면 질문에 대상 서류의 목록·칸 이름을 알려 준다(정답 label 에서 모음)."""
    data_dir, out = Path(data_dir), Path(out)
    bundles, labels = load(data_dir)
    hint_text = schema_hint(labels.values()) if hint else ""
    if limit:
        bundles = bundles[:limit]
    done = set()
    if out.exists():
        done = {json.loads(ln)["bundle"] for ln in out.open(encoding="utf-8") if ln.strip()}
    todo = [b for b in bundles if b["id"] not in done]
    out.parent.mkdir(parents=True, exist_ok=True)
    meta = out.with_suffix(".meta.json")
    meta.write_text(json.dumps({"data": str(data_dir), "method": method, "budget": budget,
                                "model": client.model if client else "oracle", "simulate": simulate,
                                "sampling": client.sampling if client else None,
                                "hint": hint_text},
                               ensure_ascii=False, indent=1),
                    encoding="utf-8")
    with out.open("a", encoding="utf-8") as f, ThreadPoolExecutor(max(1, workers)) as ex:
        futs = {ex.submit(run_bundle, b, labels, data_dir, method, client, budget, simulate, hint_text): b
                for b in todo}
        for k, fu in enumerate(as_completed(futs), 1):
            f.write(json.dumps(fu.result(), ensure_ascii=False) + "\n")
            f.flush()
            print(f"\r{client.model if client else 'oracle'} {method}: {k}/{len(todo)}", end="", file=sys.stderr)
    print(file=sys.stderr)
    return out
