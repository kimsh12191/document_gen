"""모델 서버 관리: 실행할 명령 만들기 (평가와 같은 swift deploy, train/pipeline.py), 띄우기·상태·내리기, 이미 떠 있는 서버에 붙기.
띄운 것은 <home>/models.json 에 적어 두어 화면을 다시 켜도 찾는다. 명령은 화면에 보인 글자 그대로 bash 로 실행한다."""
from __future__ import annotations

import copy
import json
import os
import re
import shlex
import signal
import socket
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

from train import fill_weights as FW
from train.pipeline import DEFAULTS
from train.serve import EVAL_DEFAULTS
from train.settings import image_tokens, image_tokens_for

from .images import IMAGE_MAX_SIZE

ROOT = Path(__file__).resolve().parents[1]
PIPE = copy.deepcopy({**DEFAULTS, "eval": EVAL_DEFAULTS})   # 평가 설정의 기본값 (model_type, eval.deploy_command·merge_command). 읽을 때의 사본
INFERENCE = json.loads((ROOT / "train" / "configs" / "inference.json").read_text(encoding="utf-8"))
PORT_BASE = 8100   # 학습 평가 서버(8000~)와 겹치지 않게
RUNNING = re.compile(r"Uvicorn running on https?://\S+?:(\d+)")
PORT_FLAG = re.compile(r"--port[ =](\d+)")
STOP_GRACE = 20    # 초: SIGTERM 뒤 이만큼 지나도 남아 있으면 SIGKILL
ENGINES = ("swift", "vllm")


def _read(p: Path, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def inspect(path: str) -> dict:
    """경로가 무엇인가: model (config.json) / adapter (LoRA 체크포인트, adapter_config.json) / None.
    adapter 면 출발 모델(base)과 합친 모델을 둘 곳(merged, 체크포인트 옆 새 폴더)."""
    p = Path(path).expanduser()
    if not p.is_dir():
        return {"path": str(p), "kind": None, "problem": "폴더가 없습니다"}
    if (p / "adapter_config.json").exists():
        base = None
        for args in (p / "args.json", p.parent / "args.json"):   # ms-swift 가 학습 설정을 남기는 곳
            base = (_read(args) or {}).get("model")
            if base:
                break
        base = base or (_read(p / "adapter_config.json") or {}).get("base_model_name_or_path")
        merged = p.parent / f"{p.name}-merged"
        ready = (merged / "config.json").exists()
        return {"path": str(p), "kind": "adapter", "base": base, "merged": str(merged), "merged_ready": ready,
                **({k: v for k, v in _dropped(merged, base).items() if k != "base"} if ready else {}),
                **({} if base else {"problem": "출발 모델 경로를 못 찾았습니다 (args.json). 명령의 --model 을 직접 고치세요"})}
    if (p / "config.json").exists():
        return {"path": str(p), "kind": "model", **_dropped(p)}
    return {"path": str(p), "kind": None, "problem": "config.json 도 adapter_config.json 도 없습니다"}


def _dropped(p: Path, base: str | None = None) -> dict:
    """합친 모델이면 출발 모델(swift export 가 남긴 args.json 의 model)과 비교해 빠진 가중치 (예: MTP mtp.*).
    {"base", "missing": {묶음: 개수}, "fillable", "blocked"?} 또는 {} (출발 모델을 모르거나 빠진 것 없음, 이미 채움)."""
    if (p / FW.RECORD).exists():
        return {"filled": True}
    base = (_read(p / "args.json") or {}).get("model") or base
    if not base or not Path(base).is_dir() or Path(base).resolve() == p.resolve():
        return {}
    try:
        plan = FW.plan(Path(base), p)
    except (ValueError, OSError):
        return {}
    if not plan["missing"]:
        return {}
    return {"base": base, "missing": plan["missing"], "fillable": bool(plan["fill"]), **({"blocked": plan["blocked"]} if plan.get("blocked") else {})}


def fill_copy(path: str) -> dict:
    """빠진 가중치를 채운 새 폴더 <경로>-filled (원본은 그대로, 파일은 링크)."""
    info = inspect(path)
    if info["kind"] != "model" or not info.get("fillable"):
        raise ValueError("채울 것이 없거나 출발 모델을 모릅니다 (python -m train.fill_weights 로 직접)")
    out = Path(info["path"] + "-filled")
    if out.exists():
        raise ValueError(f"{out} 가 이미 있습니다. 그 폴더를 쓰세요")
    return FW.fill(info["base"], info["path"], out=out)


def bindable(port: int) -> bool:
    with socket.socket() as s:
        try:
            s.bind(("", port))
            return True
        except OSError:
            return False


def _tokens(model_dir: str | None) -> tuple[int, int]:
    """(IMAGE_MAX_TOKEN_NUM, 화소/토큰 한 변). 모델의 vision 설정, 못 읽으면 32 (train/pipeline.py 와 같음)."""
    try:
        return image_tokens(model_dir, IMAGE_MAX_SIZE)
    except (OSError, ValueError, TypeError):
        return image_tokens_for(IMAGE_MAX_SIZE, 32), 32


def _lines(parts: list[str]) -> str:
    """명령을 사람이 읽기 좋게: 옵션마다 줄을 바꾼다 (bash 는 \\ 줄바꿈을 이어 읽음)."""
    out, cur = [], []
    for part in parts:
        if part.startswith("--") and cur:
            out.append(" ".join(cur))
            cur = []
        cur.append(shlex.quote(part))
    out.append(" ".join(cur))
    return " \\\n    ".join(out)


def command(path: str, gpus: list[int], port: int, model_type: str | None = None, engine: str = "swift") -> dict:
    """화면에 보일 실행 명령. {"command", "port", "factor", "info", "warnings"}"""
    if engine not in ENGINES:
        raise ValueError(f"방식은 {', '.join(ENGINES)}")
    if not gpus:
        raise ValueError("GPU 를 하나 이상 고르세요")
    info = inspect(path)
    warnings = [info["problem"]] if info.get("problem") else []
    model_type = model_type or PIPE["model_type"]
    model, pre = info["path"], ""
    if info["kind"] == "adapter":   # LoRA 체크포인트: 평가와 같이 먼저 합친다 (새 폴더, 있으면 그대로 씀)
        model = info["merged"]
        if not info["merged_ready"]:
            merge = [p.format(model=info.get("base") or "<출발 모델 경로>", model_type=model_type, adapter=info["path"], output=model)
                     for p in PIPE["eval"]["merge_command"]]
            fill = [sys.executable, "-m", "train.fill_weights", info.get("base") or "<출발 모델 경로>", model, "--in-place"]
            # 평가처럼 GPU 하나로 합치고, 빠진 가중치를 채운다 (채우기가 실패해도 띄움)
            pre = (f"CUDA_VISIBLE_DEVICES={gpus[0]} {_lines(merge)} &&\n"
                   f"{{ {_lines(fill)} || echo '빠진 가중치 채우기 실패: 그대로 띄웁니다'; }} &&\n")
            warnings.append(f"LoRA 체크포인트라 먼저 합칩니다 → {model} (몇 분 걸림, 다음부터는 합친 것을 바로 씀)")
    if info.get("missing"):
        groups = ", ".join(f"{g} {n}개" for g, n in info["missing"].items())
        warnings.append(f"합친 모델에 출발 모델의 가중치가 빠져 있습니다 ({groups}). MTP(speculative) 같은 옵션을 켜면 에러가 납니다"
                        + (". [채운 사본 만들기] 로 새 폴더를 만들어 쓰세요" if info.get("fillable") else f". {info.get('blocked', '')}"))
    tokens, factor = _tokens(info.get("base") if info["kind"] == "adapter" else model)
    env = {"CUDA_VISIBLE_DEVICES": ",".join(str(g) for g in gpus), "IMAGE_MAX_TOKEN_NUM": str(tokens),
           "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"}
    if engine == "swift":
        cmd = [p.format(model=model, model_type=model_type, port=port) for p in PIPE["eval"]["deploy_command"]]
        if len(gpus) > 1:
            cmd += ["--vllm_tensor_parallel_size", str(len(gpus))]
    else:
        cmd = ["vllm", "serve", model, "--host", "127.0.0.1", "--port", str(port), "--served-model-name", "docgen",
               "--max-model-len", "20480", "--limit-mm-per-prompt", '{"image": 16}', "--gpu-memory-utilization", "0.9"]
        if len(gpus) > 1:
            cmd += ["--tensor-parallel-size", str(len(gpus))]
        env.pop("IMAGE_MAX_TOKEN_NUM")   # swift 만 읽는다. 그림은 이 화면이 평가와 같은 크기로 줄여 보낸다
    head = " ".join(f"{k}={shlex.quote(v)}" for k, v in env.items())
    text = pre + head + " \\\n" + _lines(cmd)
    if not bindable(port):
        warnings.append(f"포트 {port} 를 이미 쓰고 있습니다")
    return {"command": text, "port": port, "factor": factor, "info": info, "warnings": warnings}


def _alive(pid: int) -> bool:
    """그룹(띄울 때 새 세션이라 pid = 프로세스 그룹)에 아직 도는 프로세스가 있나. 거두지 않은 좀비만 남았으면 없는 것."""
    try:
        os.killpg(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    proc = Path("/proc")
    if not proc.is_dir():
        return True
    for d in proc.iterdir():
        if d.name.isdigit():
            try:
                state, _, pgrp = (d / "stat").read_text().rsplit(")", 1)[1].split()[:3]
            except (OSError, ValueError):
                continue
            if pgrp == str(pid) and state != "Z":
                return True
    return False


def _start_time(pid: int) -> str | None:
    """pid 가 다른 프로세스로 재사용됐는지 보려고 (/proc 이 없으면 None)."""
    try:
        return Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[19]
    except (OSError, IndexError):
        return None


def tail(path: str | Path, n: int = 60) -> str:
    try:
        with open(path, "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 64 * 1024))
            return "\n".join(f.read().decode("utf-8", "replace").splitlines()[-n:])
    except OSError:
        return ""


def _get(url: str, timeout: float = 3) -> dict | None:
    try:
        with urlopen(url, timeout=timeout) as r:
            return json.load(r) if r.status == 200 else None
    except (URLError, OSError, ValueError):
        return None


class Models:
    def __init__(self, home: Path):
        self.home = Path(home)
        (self.home / "logs").mkdir(parents=True, exist_ok=True)
        self.file = self.home / "models.json"
        self.lock = threading.Lock()
        self.procs: dict[str, subprocess.Popen] = {}   # 이 화면이 띄운 것 (끝난 자식을 거두려고)
        self.entries: list[dict] = [e for e in _read(self.file, []) if self._still_ours(e)]
        self._save()

    def _still_ours(self, e: dict) -> bool:
        if e.get("kind") == "attached" or e.get("state") == "stopped":
            return True
        return bool(e.get("pid")) and _alive(e["pid"]) and (e.get("start_time") is None or _start_time(e["pid"]) == e["start_time"])

    def _save(self):
        tmp = self.file.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.entries, ensure_ascii=False, indent=1), encoding="utf-8")
        tmp.replace(self.file)

    def _entry(self, mid: str) -> dict:
        for e in self.entries:
            if e["id"] == mid:
                return e
        raise KeyError(mid)

    def next_port(self) -> int:
        used = {e.get("port") for e in self.entries if e.get("state") != "stopped"}
        port = PORT_BASE
        while port in used or not bindable(port):
            port += 1
        return port

    def start(self, name: str, path: str, text: str, gpus: list[int], factor: int = 32) -> dict:
        if not text.strip():
            raise ValueError("실행할 명령이 비었습니다")
        ports = PORT_FLAG.findall(text)
        if not ports:
            raise ValueError("명령에 --port 가 없습니다")
        port = int(ports[-1])
        with self.lock:
            if any(e.get("port") == port and e.get("state") != "stopped" for e in self.entries):
                raise ValueError(f"포트 {port} 는 이 화면의 다른 모델이 씁니다")
            mid = uuid.uuid4().hex[:8]
            log = self.home / "logs" / f"{time.strftime('%Y%m%d-%H%M%S')}-{mid}.log"
            with log.open("w", encoding="utf-8") as out:
                out.write(f"$ {text}\n\n")
                out.flush()
                proc = subprocess.Popen(["bash", "-c", text], stdout=out, stderr=subprocess.STDOUT, cwd=ROOT,
                                        env={**os.environ, "PYTHONIOENCODING": "utf-8"}, start_new_session=True)
            self.procs[mid] = proc
            e = {"id": mid, "kind": "started", "name": name or Path(path).name, "path": path, "command": text, "gpus": gpus,
                 "port": port, "pid": proc.pid, "start_time": _start_time(proc.pid), "log": str(log), "factor": factor,
                 "started": time.time(), "state": "starting"}
            self.entries.append(e)
            self._save()
        return self.view(e)

    def attach(self, name: str, endpoint: str, factor: int = 32) -> dict:
        endpoint = endpoint.strip().rstrip("/")
        if not endpoint.startswith(("http://", "https://")):
            raise ValueError("주소는 http://<서버>:<포트>/v1 꼴")
        if not endpoint.endswith("/v1"):
            endpoint += "/v1"
        with self.lock:
            e = {"id": uuid.uuid4().hex[:8], "kind": "attached", "name": name or endpoint, "endpoint": endpoint,
                 "factor": factor, "started": time.time(), "state": "starting"}
            self.entries.append(e)
            self._save()
        return self.view(e)

    def endpoint(self, e: dict) -> str:
        return e.get("endpoint") or f"http://127.0.0.1:{e['port']}/v1"

    def refresh(self, e: dict) -> dict:
        """상태를 다시 본다: starting → ready / exited. swift 가 포트를 옮겨 떴으면 로그에서 실제 포트를 읽는다."""
        if e.get("state") == "stopped":
            return e
        if e["kind"] == "started":
            proc = self.procs.get(e["id"])
            if not (proc.poll() is None if proc else _alive(e["pid"])):
                if e["state"] != "exited":
                    e["state"], e["ended"] = "exited", time.time()
                    self._save()
                return e
            found = RUNNING.findall(tail(e["log"], 400))
            if found and int(found[-1]) != e["port"]:
                e["port"] = int(found[-1])
                self._save()
        body = _get(self.endpoint(e) + "/models")
        state = "ready" if body else ("starting" if e["kind"] == "started" else "unreachable")
        if body and body.get("data"):
            e["served"] = body["data"][0].get("id")
        if state != e["state"]:
            e["state"] = state
            if state == "ready":
                e.setdefault("ready_at", time.time())
            self._save()
        return e

    def view(self, e: dict) -> dict:
        return {k: v for k, v in e.items() if k not in ("start_time",)} | {"endpoint": self.endpoint(e)}

    def list(self) -> list[dict]:
        with self.lock:
            return [self.view(self.refresh(e)) for e in self.entries]

    def log(self, mid: str, n: int = 200) -> str:
        e = self._entry(mid)
        return tail(e["log"], n) if e.get("log") else ""

    def stop(self, mid: str) -> dict:
        """그룹 전체를 끈다 (swift deploy 가 띄운 vLLM 작업 프로세스까지, 안 그러면 GPU 메모리가 남음). 붙은 서버는 목록에서만 뺀다."""
        with self.lock:
            e = self._entry(mid)
            if e["kind"] == "attached":
                self.entries.remove(e)
                self._save()
                return {"id": mid, "state": "removed"}
            pid = e["pid"]
            if _alive(pid) and (e.get("start_time") is None or _start_time(pid) in (None, e["start_time"])):
                try:
                    os.killpg(pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                threading.Thread(target=self._finish, args=(pid, self.procs.get(mid)), daemon=True).start()
            e["state"], e["ended"] = "stopped", time.time()
            self._save()
            return self.view(e)

    @staticmethod
    def _finish(pid: int, proc: subprocess.Popen | None):
        deadline = time.time() + STOP_GRACE
        while time.time() < deadline and _alive(pid):
            if proc:
                proc.poll()
            time.sleep(0.5)
        if _alive(pid):
            try:
                os.killpg(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        if proc:
            proc.wait(timeout=10)

    def remove(self, mid: str) -> None:
        """꺼진 것을 목록에서 지운다 (로그 파일은 남김)."""
        with self.lock:
            e = self._entry(mid)
            if e["kind"] == "started" and e["state"] not in ("stopped", "exited"):
                raise ValueError("먼저 내리세요")
            self.entries.remove(e)
            self.procs.pop(mid, None)
            self._save()

    def chat(self, mid: str, messages: list[dict], max_tokens: int | None = None) -> dict:
        """평가와 같은 요청 (train/predict.py: temperature·max_tokens·enable_thinking 은 train/configs/inference.json)."""
        e = self._entry(mid)
        payload = {"model": e.get("served") or INFERENCE["model"], "messages": messages, "temperature": INFERENCE["temperature"],
                   "max_tokens": max_tokens or INFERENCE["max_tokens"], "stream": False,
                   "chat_template_kwargs": {"enable_thinking": INFERENCE["enable_thinking"]}, **INFERENCE.get("request_options", {})}
        headers = {"Content-Type": "application/json"}
        if os.getenv("INTERNAL_MODEL_API_KEY"):
            headers["Authorization"] = "Bearer " + os.environ["INTERNAL_MODEL_API_KEY"]
        req = Request(self.endpoint(e) + "/chat/completions", data=json.dumps(payload, ensure_ascii=False).encode(), headers=headers)
        t0 = time.time()
        with urlopen(req, timeout=INFERENCE["timeout"]) as r:
            body = json.load(r)
        choice = body["choices"][0]
        return {"text": choice["message"].get("content") or "", "finish_reason": choice.get("finish_reason"),
                "seconds": round(time.time() - t0, 2), "usage": body.get("usage")}
