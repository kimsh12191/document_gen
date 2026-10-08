"""OpenAI-compatible inference on a user-specified INTERNAL model endpoint."""
import base64
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from functools import lru_cache
from threading import Lock
from pathlib import Path
from urllib.request import Request, urlopen

from .data import digest, dumps, read_json, read_jsonl, write_json


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


def predict(tasks_path, output, endpoint, model, run_id, with_ocr=False, timeout=180, max_tokens=256,
            temperature=0, enable_thinking=False, request_options=None, concurrency=1):
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
    if not endpoint.startswith(("http://", "https://")):
        raise ValueError("Provide the internal HTTP(S) model endpoint")
    meta_path = output.with_suffix(output.suffix + ".meta.json")
    settings = {"tasks_sha256": digest(path.read_bytes()), "endpoint": endpoint, "model": model,
                "run_id": run_id, "with_ocr": with_ocr, "temperature": temperature, "max_tokens": max_tokens,
                "enable_thinking": enable_thinking, "reference_type": "ocr_pseudo_unreviewed"}
    if request_options:
        settings["request_options"] = request_options
    # A cache must never combine base/SFT/RL generations; use a unique checkpoint run_id.
    image_hashes = {}
    for row in rows:
        for image in row["images"]:
            if image not in image_hashes:
                image_hashes[image] = digest(Path(image).read_bytes())
    settings["images_sha256"] = digest(dumps(image_hashes).encode())
    if meta_path.exists():
        if read_json(meta_path) != settings:
            raise ValueError("Prediction run settings or input changed. Use a new output path.")
    elif output.exists():
        raise ValueError("Prediction output exists without metadata; use a new path")
    else:
        write_json(meta_path, settings)
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
        if with_ocr:
            # Explicit teacher-assisted baseline, never passed in vision-only runs.
            prompt += "\nInternal OCR context (may contain errors):\n" + dumps(row["ocr_items"])
        content = [{"type": "text", "text": prompt}]
        for image in row["images"]:
            image_path = Path(image)
            if image_path.suffix.lower() != ".png":
                raise ValueError("Prepared inference images must be PNG")
            with image_lock:
                encoded = encode_image(str(image_path))
            content.append({"type": "image_url", "image_url": {"url": "data:image/png;base64," + encoded}})
        payload = {"model": model, "messages": [{"role": "user", "content": content}],
                   "temperature": temperature, "max_tokens": max_tokens, "stream": False,
                   "chat_template_kwargs": {"enable_thinking": enable_thinking}, **request_options}
        req = Request(endpoint.rstrip("/") + "/chat/completions", data=dumps(payload).encode(), headers=headers)
        with urlopen(req, timeout=timeout) as response:
            response = json.load(response)
        choice = response["choices"][0]
        text = choice["message"].get("content")
        if not isinstance(text, str):
            raise ValueError(f"Non-text response for {row['id']}")
        return {"id": row["id"], "prediction": text, "finish_reason": choice.get("finish_reason")}

    remaining = iter(row for row in rows if row["id"] not in done)
    completed = len(done)
    started = time.monotonic()
    print(f"Inference {completed}/{len(rows)}; concurrency={concurrency}", flush=True)
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
    return {"predictions": len(rows), "output": str(output), "run_id": run_id, "teacher_context": with_ocr}
