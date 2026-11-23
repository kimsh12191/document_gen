"""평가 서버와 모델 답: GPU 마다 vLLM 서버(swift deploy)를 하나씩 띄우고 평가 세트마다 답을 낸다. LoRA 합치기도.

모델 답은 <cache_dir>/answers/<평가 세트 폴더 이름>/<모델 이름>-<지문>.jsonl 에 둔다.
지문 = 모델 폴더(경로·config.json 시각)·model_type·평가 서버 명령·답 내기 설정(inference.json)·질문 파일
(template 은 model_type 과 다를 때만 — 같으면 --template 을 붙이기 전의 답을 그대로 씀).
같으면 다른 실행·실험·평가만 하기도 그 답을 그대로 쓴다 (출발 모델은 한 번만 평가). 다 낸 답은 <답>.done 이 있다.
같은 답을 다른 실행이 내는 중이면 잠금(<답>.lock)이 풀리기를 기다렸다가 그 답을 쓴다.
"""
import hashlib
import json
import os
import random
import re
import signal
import socket
import subprocess
import time
from contextlib import ExitStack, contextmanager
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from docgen.bench.ocr_data import read_json, read_jsonl, write_json, write_jsonl

from .settings import image_tokens, image_tokens_for, load_settings, locked, log

ROOT = Path(__file__).resolve().parents[1]
EVAL_DEFAULTS = {
    "inference_config": "inference.json",
    "concurrency_per_server": 16,
    "port_base": 8000,
    "server_start_timeout_minutes": 40,
    "merge_command": ["swift", "export", "--model", "{model}", "--model_type", "{model_type}",
                      "--adapters", "{adapter}", "--merge_lora", "true", "--output_dir", "{output}"],
    # 질문 하나에 그림 13장까지 (여러 서류), 그림 토큰 ~12000 + 답 4096
    "deploy_command": ["swift", "deploy", "--model", "{model}", "--model_type", "{model_type}",
                       "--infer_backend", "vllm", "--vllm_max_model_len", "20480", "--vllm_max_num_seqs", "32",
                       "--vllm_limit_mm_per_prompt", "{{\"image\": 16}}",  # 중괄호 두 겹: str.format 을 거친다
                       "--vllm_gpu_memory_utilization", "0.9", "--host", "127.0.0.1", "--port", "{port}",
                       "--served_model_name", "docgen", "--enable_thinking", "false", "--max_new_tokens", "4096"],
    "health_path": "/v1/models",
    # 합친 뒤 출발 모델에만 있는 가중치(예: Qwen3.5 MTP 머리 mtp.*)를 채운다 (train/fill_weights.py). 평가 답은 그대로
    "fill_from_base": True,
}
INFERENCE_DEFAULTS = {"model": "docgen", "timeout": 600, "max_tokens": 4096, "temperature": 0, "enable_thinking": False,
                      "request_options": {}}


def swift_command(parts, template=None, **values):
    """명령 틀(deploy_command · merge_command)을 채운다. swift 명령인데 --template 이 없으면 붙인다 (template 이 없으면 model_type;
    다른 명령은 틀에 {template} 을 적어 쓴다).
    ms-swift 는 --template 이 없으면 모델 폴더 이름을 공식 이름(Qwen3.5-9B …)과 맞춰 template 을 고르는데, 폴더 이름이 다르고
    같은 model_type 에 template 이 여럿이면 못 고르고 멈춘다 (4.6: qwen3_5 에 qwen3_5 · qwen3_8)."""
    template = template or values.get("model_type")
    cmd = [part.format(template=template, **values) for part in parts]
    if template and cmd and Path(cmd[0]).name == "swift" and "--template" not in cmd:
        cmd += ["--template", template]
    return cmd


# swift deploy 는 --port 에 bind 가 안 되면 말없이 다음 포트로 뜬다 (ms-swift find_free_port).
# 앞 서버를 끈 직후에는 그 포트의 연결이 TIME_WAIT(리눅스 60초)로 남아 bind 가 안 되므로, 비기를 기다렸다 띄운다.
PORT_FREE_WAIT = 180   # 초
RUNNING = re.compile(r"Uvicorn running on https?://\S+?:(\d+)")
WAIT_NOTE = 5 * 60     # 서버를 기다리는 동안 이만큼마다 알림 (초)


def conf_path(p, base: Path):
    """설정 파일 기준 상대 경로, 거기 없으면 train/configs 의 기본 파일."""
    q = Path(p) if Path(p).is_absolute() else (base / p).resolve()
    return str(q) if q.exists() or Path(p).is_absolute() else str(Path(__file__).resolve().parent / "configs" / p)


def port_bindable(port: int) -> bool:
    """swift deploy 의 빈 포트 검사와 같게: SO_REUSEADDR 없이 bind 가 되는지."""
    with socket.socket() as sock:
        try:
            sock.bind(("", port))
            return True
        except OSError:
            return False


def wait_port_free(port: int, limit: float | None = None) -> None:
    """포트에 bind 가 될 때까지 기다린다 (앞 서버 연결의 TIME_WAIT). limit 초 안에 안 비면 RuntimeError."""
    limit = PORT_FREE_WAIT if limit is None else limit
    if port_bindable(port):
        return
    log(f"port {port} is not free yet (connections of the previous server in TIME_WAIT); waiting up to {limit:.0f}s")
    deadline = time.monotonic() + limit
    while not port_bindable(port):
        if time.monotonic() > deadline:
            raise RuntimeError(f"Port {port} is still not free after {limit:.0f}s; check `ss -tanp | grep :{port}` "
                               "or set eval.port_base to other ports")
        time.sleep(2)
    log(f"port {port} is free")


def _tail(path, n: int = 15) -> str:
    try:
        lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()[-n:]
    except OSError:
        return ""
    return "\n".join("    " + x for x in lines)


def _listening_port(log_path, offset):
    """서버 로그에서 새로 쓰인 부분의 'Uvicorn running on http://…:<포트>' → (읽은 끝 위치, 포트 또는 None)."""
    try:
        with open(log_path, "rb") as f:
            f.seek(offset)
            chunk = f.read()
    except OSError:
        return offset, None
    cut = chunk.rfind(b"\n") + 1   # 줄 끝까지만 읽은 것으로 (반쪽 줄은 다음에)
    m = RUNNING.search(chunk[:cut].decode("utf-8", "replace"))
    return offset + cut, (int(m.group(1)) if m else None)


def _slug(model):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", "-".join(Path(str(model)).parts[-2:]))[:60]


class Evaluator:
    """eval: 설정의 eval 칸 (EVAL_DEFAULTS 위에), gpus: GPU 번호, logs: 서버·답 내기 로그 폴더, cache_dir: 평가 세트·답 캐시."""

    def __init__(self, eval_cfg, gpus, logs, cache_dir, dry=False, smoke_per_task=None):
        self.ev = {**EVAL_DEFAULTS, **(eval_cfg or {})}
        self.gpus = [str(g) for g in gpus]
        self.logs, self.cache, self.dry, self.smoke = Path(logs), Path(cache_dir), dry, smoke_per_task
        self.inference = {**INFERENCE_DEFAULTS, **load_settings(self.ev["inference_config"])}
        unknown = set(self.inference) - set(INFERENCE_DEFAULTS) - {"endpoint", "concurrency"}
        if unknown:
            raise ValueError(f"{self.ev['inference_config']}: 모르는 칸 {sorted(unknown)}")
        self.inference.pop("endpoint", None)
        self.inference.pop("concurrency", None)

    # -- 질문 파일 ----------------------------------------------------------------------------
    def image_limit(self):
        """평가 서버가 질문 하나에 받는 그림 수 (deploy_command 의 limit_mm_per_prompt). 못 읽으면 None."""
        cmd = self.ev["deploy_command"]
        for flag, value in zip(cmd, cmd[1:]):
            if flag.lstrip("-").replace("-", "_") in ("vllm_limit_mm_per_prompt", "limit_mm_per_prompt"):
                try:
                    return int(json.loads(value.format())["image"])
                except (ValueError, KeyError, TypeError):
                    return None
        return None

    def tasks_file(self, set_dir):
        """이 서버로 물을 질문 파일: 리허설이면 과제마다 몇 개, 그림이 서버 한도보다 많은 문항은 뺀다 (모든 모델이 같은 문항)."""
        set_dir = Path(set_dir)
        src = set_dir / "tasks.jsonl"
        limit, n = self.image_limit(), self.smoke
        if not limit and not n:
            return src
        name = "tasks" + (f".smoke{n}" if n else "") + (f".max{limit}images" if limit else "") + ".jsonl"
        out = set_dir / name
        if out.exists():
            return out
        rows = read_jsonl(src)
        if n:
            by_task = {}
            for r in rows:
                by_task.setdefault(r["task"], []).append(r)
            rows = [r for t in sorted(by_task) for r in random.Random(0).sample(by_task[t], min(n, len(by_task[t])))]
        keep = [r for r in rows if not limit or len(r["images"]) <= limit]
        if len(keep) < len(rows):
            log(f"WARNING: {set_dir.name}: 그림이 {limit}장보다 많은 {len(rows) - len(keep)}문항은 빼고 평가합니다 (서버 limit_mm_per_prompt)")
        tmp = out.with_name(out.name + f".{os.getpid()}.tmp")
        write_jsonl(tmp, keep)
        tmp.replace(out)
        return out

    def answers_path(self, model, model_type, tasks: Path, template=None):
        cfg = Path(model) / "config.json"
        sig = {"model": str(Path(model).resolve()), "config": cfg.stat().st_mtime_ns if cfg.exists() else None,
               "model_type": model_type, "deploy": self.ev["deploy_command"], "inference": self.inference,
               "tasks": hashlib.sha256(tasks.read_bytes()).hexdigest() if tasks.exists() else str(tasks)}
        if template and template != model_type:
            sig["template"] = template
        key = hashlib.sha256(json.dumps(sig, sort_keys=True).encode()).hexdigest()[:12]
        return self.cache / "answers" / tasks.parent.name / f"{_slug(model)}-{key}{'' if tasks.name == 'tasks.jsonl' else '.' + tasks.stem}.jsonl"

    # -- 서버 --------------------------------------------------------------------------------
    def image_token_budget(self, model, sets):
        """서버가 평가 그림을 다시 줄이지 않을 토큰 수 (평가 세트 그림 예산 중 가장 큰 것)."""
        sizes = [read_json(Path(d) / "DONE.json")["image_max_size"] for d in sets.values() if (Path(d) / "DONE.json").exists()]
        sizes = sizes or [[2300, 1600]]
        try:
            return max(image_tokens(model, s)[0] for s in sizes)
        except (OSError, ValueError):
            return max(image_tokens_for(s, 32) for s in sizes)

    @contextmanager
    def serve(self, model, model_type, name, tokens, template=None):
        ev = self.ev
        procs, endpoints = [], []
        for i, gpu in enumerate(self.gpus):
            port = ev["port_base"] + i
            with socket.socket() as sock:
                if sock.connect_ex(("127.0.0.1", port)) == 0 and not self.dry:
                    raise RuntimeError(f"Port {port} is already in use; stop the old server so the wrong model is not evaluated")
            if not self.dry:
                wait_port_free(port)   # 안 그러면 swift 가 다른 포트로 띄우고, 여기서는 이 포트만 기다리게 된다
            cmd = swift_command(ev["deploy_command"], template, model=model, model_type=model_type, port=port)
            env = {**os.environ, "CUDA_VISIBLE_DEVICES": gpu, "IMAGE_MAX_TOKEN_NUM": str(tokens),
                   "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"}
            env.pop("NPROC_PER_NODE", None)
            log(f"start server {name} on GPU {gpu}: IMAGE_MAX_TOKEN_NUM={tokens} " + " ".join(cmd))
            endpoints.append(f"http://127.0.0.1:{port}/v1")
            if not self.dry:
                self.logs.mkdir(parents=True, exist_ok=True)
                out = (self.logs / f"server-{name}-{i}.log").open("w", encoding="utf-8")
                procs.append((subprocess.Popen(cmd, env=env, stdout=out, stderr=subprocess.STDOUT, cwd=ROOT,
                                               start_new_session=True), out, port))
        try:
            started = time.monotonic()
            deadline = started + ev["server_start_timeout_minutes"] * 60
            for proc, out, port in procs:
                seen, note = 0, started + WAIT_NOTE
                while True:
                    if proc.poll() is not None:
                        raise RuntimeError(f"Server on port {port} exited; see {out.name}\n{_tail(out.name)}")
                    try:
                        with urlopen(f"http://127.0.0.1:{port}{ev['health_path']}", timeout=5) as response:
                            if response.status == 200:
                                break
                    except (URLError, OSError):
                        pass
                    seen, actual = _listening_port(out.name, seen)
                    if actual is not None and actual != port:
                        raise RuntimeError(f"Server for port {port} started on port {actual} instead (swift deploy moves to the "
                                           f"next free port when {port} cannot be bound); see {out.name}")
                    now = time.monotonic()
                    if now > deadline:
                        raise RuntimeError(f"Server on port {port} not ready in time "
                                           f"({ev['server_start_timeout_minutes']} min, eval.server_start_timeout_minutes); "
                                           f"see {out.name}\n{_tail(out.name)}")
                    if now > note:
                        log(f"waiting for server on port {port}: {(now - started) / 60:.0f} min (log {out.name})")
                        note = now + WAIT_NOTE
                    time.sleep(3)
                log(f"server on port {port} ready")
            yield ",".join(endpoints)
        finally:
            for proc, out, _ in procs:
                if proc.poll() is None:
                    os.killpg(proc.pid, signal.SIGTERM)
            for proc, out, _ in procs:
                try:
                    proc.wait(timeout=120)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                out.close()

    # -- 답 ----------------------------------------------------------------------------------
    def answer(self, model, model_type, sets: dict, name: str, template=None) -> dict:
        """평가 세트마다 모델 답 → {세트 id: {"dir", "tasks", "answers"}}. 캐시에 다 낸 답이 있으면 서버를 띄우지 않는다."""
        plan = {}
        for sid, d in sets.items():
            tasks = self.tasks_file(d) if not self.dry or (Path(d) / "tasks.jsonl").exists() else Path(d) / "tasks.jsonl"
            plan[sid] = {"dir": str(d), "tasks": str(tasks), "answers": str(self.answers_path(model, model_type, Path(tasks), template))}

        def todo():
            return [s for s in plan if not Path(plan[s]["answers"] + ".done").exists()]
        if not todo():
            log(f"{name}: 평가 세트 {len(plan)}개 모두 답이 있습니다 (캐시)")
            return plan
        if self.dry:
            log(f"{name}: 답 낼 평가 세트 {', '.join(todo())} (dry run)")
            return plan
        with ExitStack() as stack:
            for s in sorted(todo()):   # 늘 같은 차례로 잡는다 (실행끼리 서로 기다리다 멈추지 않게)
                stack.enter_context(locked(plan[s]["answers"], f"{name} 답 ({s})"))
            left = todo()   # 기다리는 동안 다른 실행이 낸 것은 빠진다
            if not left:
                log(f"{name}: 다른 실행이 낸 답을 씁니다")
                return plan
            from .predict import predict

            tokens = self.image_token_budget(model, {s: plan[s]["dir"] for s in left})
            with self.serve(model, model_type, _slug(model), tokens, template) as endpoints:
                for s in left:
                    p = plan[s]
                    started = time.monotonic()
                    log(f"{name}: {s} 답 내기 → {p['answers']}")
                    predict(p["tasks"], p["answers"], endpoints, concurrency=self.ev["concurrency_per_server"] * len(self.gpus),
                            about={"model": str(model), "model_type": model_type, "set": s}, **self.inference)
                    n = sum(1 for _ in read_jsonl(p["answers"]))
                    write_json(Path(p["answers"] + ".done"), {"n": n, "model": str(model), "minutes": round((time.monotonic() - started) / 60, 1)})
                    log(f"{name}: {s} {n}문항 ({(time.monotonic() - started) / 60:.1f} min)")
        return plan

    # -- LoRA 합치기 --------------------------------------------------------------------------
    def merge(self, base_model, model_type, adapter, output, log_file, template=None):
        output = Path(output)
        if (output / "config.json").exists():
            return str(output)
        cmd = swift_command(self.ev["merge_command"], template, model=base_model, model_type=model_type, adapter=adapter, output=output)
        log("$ " + " ".join(cmd) + f"   (log: {log_file})")
        if self.dry:
            return str(output)
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "a", encoding="utf-8") as out:
            code = subprocess.run(cmd, env={**os.environ, "CUDA_VISIBLE_DEVICES": self.gpus[0], "PYTHONIOENCODING": "utf-8"},
                                  stdout=out, stderr=subprocess.STDOUT, cwd=ROOT).returncode
        if code:
            raise RuntimeError(f"합치기 실패 ({code}); see {log_file}\n{_tail(log_file)}")
        if self.ev.get("fill_from_base", True):
            fill_from_base(base_model, output)
        return str(output)


def fill_from_base(base_model, output):
    """합치기가 버린 가중치를 출발 모델에서 채운다. 못 채워도 평가는 계속한다 (MTP 같은 추측용 부분만 빠짐)."""
    from .fill_weights import fill

    try:
        r = fill(base_model, output, in_place=True)
    except (ValueError, OSError) as exc:
        log(f"WARNING: 빠진 가중치 채우기를 건너뜀 ({output}): {exc}")
        return
    if r["filled"]:
        log(f"출발 모델에만 있던 가중치 {r['filled']}개를 채움 ({', '.join(f'{g} {n}' for g, n in r['missing'].items())}) → {output}")
    elif r.get("blocked"):
        log(f"WARNING: {output}: {r['blocked']} 빠진 것 {r['missing']}, 합친 모델에만 있는 것 {r['extra']}")
