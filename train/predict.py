"""모델 답 내기: OpenAI 호환 모델 서버(여러 개면 그림별로 나눠 보냄)에 평가 질문을 보내고, 끊기면 이어서.
입력은 준비한 평가 세트의 tasks.jsonl ({id, messages, images(PNG)}), 출력은 {id, prediction, finish_reason} 줄 + <출력>.meta.json.
meta.json 은 질문 파일·그림·답 내기 설정의 지문: 다르면 이어 쓰지 않는다 (서버 주소는 상관없음)."""
import base64
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from functools import lru_cache
from threading import Lock
from pathlib import Path
from urllib.request import Request, urlopen

from docgen.bench.ocr_data import digest, dumps, read_json, read_jsonl, write_json


def index_predictions(path):
    result = {}
    for row in read_jsonl(path):
        if row["id"] in result:
            raise ValueError(f"Duplicate prediction ID: {row['id']}")
        if not isinstance(row.get("prediction"), str):
            raise ValueError("Each prediction must be a string")
        result[row["id"]] = row["prediction"]
    return result


def validate_tasks(rows):
    ids = [r["id"] for r in rows]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Tasks must be nonempty and have unique IDs")


def predict(tasks_path, output, endpoint, model="docgen", timeout=600, max_tokens=4096,
            temperature=0, enable_thinking=False, request_options=None, concurrency=1, about=None):
    """about: 답 파일에 남길 설명 (모델 경로 등, 지문에는 안 들어감)."""
    if type(concurrency) is not int or concurrency < 1:
        raise ValueError("concurrency must be a positive integer")
    request_options = dict(request_options or {})
    reserved = {"model", "messages", "stream", "temperature", "max_tokens", "chat_template_kwargs"}
    if reserved & request_options.keys():
        raise ValueError("Use named settings for reserved request fields: " + ", ".join(sorted(reserved & request_options.keys())))
    if isinstance(max_tokens, bool) or not isinstance(max_tokens, int) or max_tokens < 1:
        raise ValueError("max_tokens must be a positive integer")
    if not isinstance(temperature, (float, int)) or isinstance(temperature, bool) or not 0 <= temperature <= 2:
        raise ValueError("temperature must be between 0 and 2")
    if not isinstance(enable_thinking, bool):
        raise ValueError("enable_thinking must be boolean")
    path, output = Path(tasks_path), Path(output)
    rows = read_jsonl(path)
    validate_tasks(rows)
    endpoints = [e.strip().rstrip("/") for e in (endpoint.split(",") if isinstance(endpoint, str) else endpoint) if e.strip()]
    if not endpoints or not all(e.startswith(("http://", "https://")) for e in endpoints):
        raise ValueError("Provide the internal HTTP(S) model endpoint(s)")
    endpoint = endpoints[0] if len(endpoints) == 1 else endpoints
    meta_path = output.with_suffix(output.suffix + ".meta.json")
    settings = {"tasks_sha256": digest(path.read_bytes()), "temperature": temperature, "max_tokens": max_tokens,
                "enable_thinking": enable_thinking}
    if request_options:
        settings["request_options"] = request_options
    image_hashes = {}
    for row in rows:
        for image in row["images"]:
            if image not in image_hashes:
                image_hashes[image] = digest(Path(image).read_bytes())
    settings["images_sha256"] = digest(dumps(image_hashes).encode())
    if meta_path.exists():
        old = read_json(meta_path)
        if {k: old.get(k) for k in settings} != settings:
            raise ValueError(f"{output}: 질문·그림·답 내기 설정이 그 답 파일을 낼 때와 다릅니다. 새 파일에 내세요")
    elif output.exists():
        raise ValueError(f"{output}: meta.json 없는 답 파일이 있습니다; 새 파일에 내세요")
    else:
        write_json(meta_path, {**settings, **({"about": about} if about else {})})
    done = index_predictions(output) if output.exists() else {}
    if set(done) - {r["id"] for r in rows}:
        raise ValueError("Unknown IDs in prediction cache")
    headers = {"Content-Type": "application/json"}
    if os.getenv("INTERNAL_MODEL_API_KEY"):
        headers["Authorization"] = "Bearer " + os.environ["INTERNAL_MODEL_API_KEY"]
    output.parent.mkdir(parents=True, exist_ok=True)
    image_lock = Lock()

    @lru_cache(maxsize=16)
    def encode_image(path):
        return base64.b64encode(Path(path).read_bytes()).decode("ascii")

    def infer(row):
        prompt = row["messages"][0]["content"].replace("<image>", "").strip()
        # Image(s) first, then the question: the same order as training ("<image>\n...") and a
        # shared prefix across questions on one image, which the server's prefix cache reuses.
        content = []
        for image in row["images"]:
            image_path = Path(image)
            if image_path.suffix.lower() != ".png":
                raise ValueError("Prepared inference images must be PNG")
            with image_lock:
                encoded = encode_image(str(image_path))
            content.append({"type": "image_url", "image_url": {"url": "data:image/png;base64," + encoded}})
        content.append({"type": "text", "text": prompt})
        payload = {"model": model, "messages": [{"role": "user", "content": content}],
                   "temperature": temperature, "max_tokens": max_tokens, "stream": False,
                   "chat_template_kwargs": {"enable_thinking": enable_thinking}, **request_options}
        # Same image -> same server, so its prefix (image) cache is reused across questions.
        # Routed by content, so identical pixels in different files also share one server.
        server = endpoints[int(image_hashes[row["images"][0]][:8], 16) % len(endpoints)]
        req = Request(server + "/chat/completions", data=dumps(payload).encode(), headers=headers)
        with urlopen(req, timeout=timeout) as response:
            response = json.load(response)
        choice = response["choices"][0]
        text = choice["message"].get("content")
        if not isinstance(text, str):
            raise ValueError(f"Non-text response for {row['id']}")
        return {"id": row["id"], "prediction": text, "finish_reason": choice.get("finish_reason")}

    # Questions about one image run back to back while its cache entries are warm.
    remaining = iter(sorted((row for row in rows if row["id"] not in done), key=lambda r: (image_hashes[r["images"][0]], r["id"])))
    completed = len(done)
    started = time.monotonic()
    print(f"Inference {completed}/{len(rows)}; concurrency={concurrency}; servers={len(endpoints)}", flush=True)
    with output.open("a", encoding="utf-8", newline="\n") as f:
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            pending = set()
            for _ in range(concurrency):
                row = next(remaining, None)
                if row is not None:
                    pending.add(executor.submit(infer, row))
            try:
                while pending:
                    finished, pending = wait(pending, return_when=FIRST_COMPLETED)
                    errors = []
                    for future in finished:
                        try:
                            result = future.result()
                        except Exception as exc:
                            errors.append(exc)
                            continue
                        f.write(dumps(result) + "\n")
                        f.flush()
                        completed += 1
                        if completed % 100 == 0 or completed == len(rows):
                            elapsed = time.monotonic() - started
                            print(f"Inference {completed}/{len(rows)}; elapsed={elapsed:.1f}s", flush=True)
                    if errors:
                        raise errors[0]
                    for _ in finished:
                        row = next(remaining, None)
                        if row is not None:
                            pending.add(executor.submit(infer, row))
            except BaseException:
                for future in pending:
                    future.cancel()
                raise
    return {"predictions": len(rows), "output": str(output)}
