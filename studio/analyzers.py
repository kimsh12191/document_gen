"""⑧ 작업 › 분석기 (DESIGN.md 7절): 서식 이미지를 분석기에 맡겨 html 서식(`html`)이나 overlay 값 영역 초안(`layout`)을 받는다.

분석기는 두 방식만 붙인다 (특정 도구 이름은 코드에 없다). studio/config.json 의 "providers":
  {"<이름>": {"kind": "openai", "base_url": "http://<서버>:8000/v1", "model": "…", "api_key_env": "환경변수 이름", "external": false},
   "<이름>": {"kind": "cli", "cmd": "<실행 파일>" 또는 "discover": "<glob>", "args": ["-p", "{task_text}", …],
              "version_args": ["--version"], "external": true}}
  - args 의 {job_dir} {image} {task_file} {task_text} 는 실행할 때 채운다. discover 에 맞는 것이 여럿이면 가장 최근 것.
  - external 은 도구가 아니라 연결 대상으로 정한다 (사내 게이트웨이에 붙은 CLI 면 false). external 분석기에는 실서류 묶음의 이미지를 보내지 않는다.

작업 폴더 <workspace_dir>/analyzer/<작업 ID>/
  job.json      {id, kind, provider, provider_kind, external, target, source, created, sent: [보낸 파일], from_job?}
  input/        source.png(html) 또는 page_<쪽>.png(layout), 참고 파일 (가이드, 예시 템플릿, 키 사전, 지난 결과)
  TASK.md       지시문 (studio/analyzer_tasks/<kind>.md 틀)
  output/       분석기가 쓰는 결과. html: template.html.j2 + form.json, layout: layout.json
  check/        studio 가 결과를 렌더링해 본 것 (python -m docgen.preview)
  review.json   {"comments": [{at, by, text}], "approved": {as, at, by}}
실행은 studio 작업(⑧)으로 돌리고, 끝나면 결과를 검사해 결과 요약을 남긴다. 사람이 승인해야 서식으로 등록된다 (등록 뒤에도 검수 전).

  python -m studio.analyzers openai <작업 폴더>     openai 방식 실행 (작업이 이 명령을 돌린다)
"""
from __future__ import annotations

import base64
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = Path(__file__).resolve().parent / "analyzer_tasks"
KINDS = ("html", "layout")


# ---------------------------------------------------------------------------
# 분석기 설정
# ---------------------------------------------------------------------------

def resolve_cmd(p: dict) -> str | None:
    if p.get("cmd"):
        return p["cmd"]
    if p.get("discover"):
        hits = [h for h in glob.glob(os.path.expanduser(p["discover"])) if os.path.isfile(h)]
        return max(hits, key=os.path.getmtime) if hits else None
    return None


def providers(cfg: dict) -> list[dict]:
    out = []
    for name, p in (cfg.get("providers") or {}).items():
        kind = p.get("kind")
        out.append({"name": name, "kind": kind, "external": bool(p.get("external", True)),
                    "model": p.get("model"), "base_url": p.get("base_url"),
                    "cmd": resolve_cmd(p) if kind == "cli" else None, "ok_kind": kind in ("openai", "cli")})
    return out


def _provider(cfg: dict, name: str) -> dict:
    p = (cfg.get("providers") or {}).get(name)
    if not p:
        raise KeyError(f"분석기 {name}")
    if p.get("kind") not in ("openai", "cli"):
        raise ValueError(f"{name}: kind 는 openai 또는 cli")
    return p


def check(cfg: dict, name: str) -> dict:
    """연결 확인: openai 는 모델 목록, cli 는 --version (요청은 보내지 않는다)."""
    p = _provider(cfg, name)
    if p["kind"] == "cli":
        cmd = resolve_cmd(p)
        if not cmd:
            return {"ok": False, "detail": "실행 파일을 찾지 못했습니다 (cmd 또는 discover)"}
        try:
            r = subprocess.run([cmd, *p.get("version_args", ["--version"])], capture_output=True, text=True, timeout=30,
                               encoding="utf-8", errors="replace")
        except (OSError, subprocess.TimeoutExpired) as e:
            return {"ok": False, "detail": f"{type(e).__name__}: {e}"}
        return {"ok": r.returncode == 0, "detail": (r.stdout or r.stderr).strip()[:300], "cmd": cmd}
    from urllib.request import Request, urlopen

    req = Request(p["base_url"].rstrip("/") + "/models", headers=_auth(p))
    try:
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        models = [m.get("id") for m in data.get("data", [])]
        return {"ok": True, "detail": ", ".join(models[:8]) or "(모델 목록 비어 있음)",
                "model_listed": not p.get("model") or p["model"] in models}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "detail": f"{type(e).__name__}: {e}"}


def _auth(p: dict) -> dict:
    key = os.environ.get(p.get("api_key_env") or "", "")
    return {"Authorization": f"Bearer {key}"} if key else {}


# ---------------------------------------------------------------------------
# 작업 만들기
# ---------------------------------------------------------------------------

def _root(ws: Path) -> Path:
    return Path(ws) / "analyzer"


def _write(p: Path, obj) -> None:
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


def _read(p: Path, default=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def create_job(ws: Path, cfg: dict, kind: str, provider: str, images: list[str], target: dict, source: dict,
               from_job: str | None = None, comment: str = "", previous_files: dict | None = None) -> Path:
    """작업 폴더를 만들고 입력·지시문을 둔다 (아직 실행하지 않는다).
    images: 서식 그림 경로 (html 은 첫 장, layout 은 쪽 순서대로). source: {real_data, public, label} (어디서 온 그림인지).
    from_job: 다시 고쳐 — 그 작업의 결과와 의견을 함께 보낸다. previous_files: 편집기에서 고치던 파일 {이름: 내용} (같은 뜻)."""
    if kind not in KINDS:
        raise ValueError(f"작업 종류는 {KINDS}")
    p = _provider(cfg, provider)
    external = bool(p.get("external", True))
    if external and source.get("real_data") and not source.get("public"):
        raise ValueError("실서류에서 온 그림은 외부 분석기(external: true)로 보낼 수 없습니다. 내부 분석기를 고르거나, 빈 서식·공개 서식만 보내세요")
    if not images:
        raise ValueError("서식 그림이 없습니다")
    job_id = time.strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:4]
    d = _root(ws) / job_id
    (d / "input").mkdir(parents=True)
    (d / "output").mkdir()
    sent = []
    if kind == "html":
        shutil.copyfile(images[0], d / "input" / "source.png")
        sent.append("input/source.png")
        refs = {"TEMPLATE_GUIDE.md": ROOT / "docgen" / "manual" / "TEMPLATE_GUIDE.md",
                "example_simple.html.j2": ROOT / "docgen" / "templates" / "income" / "employment_certificate.html.j2",
                "example_rows.html.j2": ROOT / "docgen" / "templates" / "finance" / "bank_statement.html.j2",
                "_macros.html.j2": ROOT / "docgen" / "templates" / "_macros.html.j2",
                "keys.json": ROOT / "docgen" / "keys.json"}
    else:
        for k, im in enumerate(images):
            shutil.copyfile(im, d / "input" / f"page_{k}.png")
            sent.append(f"input/page_{k}.png")
        refs = {"keys.json": ROOT / "docgen" / "keys.json"}
        if target.get("texts"):   # 견본 그림 속 인쇄 글자 (가져온 이미지 서식의 OCR) — 항목명 찾기를 돕는다
            _write(d / "input" / "ocr_words.json", target["texts"])
            sent.append("input/ocr_words.json")
    for name, src in refs.items():
        if src.exists():
            shutil.copyfile(src, d / "input" / name)
            sent.append(f"input/{name}")
    feedback = ""
    if previous_files:
        (d / "input" / "previous").mkdir()
        for name, text in previous_files.items():
            (d / "input" / "previous" / name).write_text(text if isinstance(text, str) else json.dumps(text, ensure_ascii=False, indent=1),
                                                       encoding="utf-8")
            sent.append(f"input/previous/{name}")
        feedback = ("## 다시 고칠 것\n\n지금 서식이 `input/previous/` 에 있다. 그것에서 출발해 아래 의견대로 고친다.\n\n"
                    + (f"- {comment}" if comment.strip() else "- 원본 그림과 더 비슷하게"))
    if from_job:   # 다시 고쳐: 지난 결과와 사람 의견을 함께 보낸다
        prev = _root(ws) / from_job
        if (prev / "output").is_dir():
            shutil.copytree(prev / "output", d / "input" / "previous")
            sent += [f"input/previous/{f.name}" for f in (d / "input" / "previous").iterdir()]
        notes = [c["text"] for c in (_read(prev / "review.json", {}) or {}).get("comments", [])] + ([comment] if comment else [])
        feedback = ("## 다시 고칠 것\n\n지난 결과가 `input/previous/` 에 있다. 그것에서 출발해 아래 의견대로 고친다.\n\n"
                    + "\n".join(f"- {n}" for n in notes if n.strip()))
    tgt = "\n".join(f"- {k}: {v}" for k, v in target.items() if k != "texts" and v not in (None, ""))
    task = (TASKS / f"{kind}.md").read_text(encoding="utf-8")
    task = (task.replace("{target}", f"## 대상\n\n{tgt}" if tgt else "").replace("{group}", target.get("group") or "finance")
            .replace("{feedback}", feedback)
            .replace("{ocr_hint}", "- `input/ocr_words.json` 은 그림 속 인쇄 글자와 위치(pt, 그림 픽셀 ÷ 2.667)다. 항목명을 찾을 때 쓴다."
                     if target.get("texts") else ""))
    (d / "TASK.md").write_text(task, encoding="utf-8")
    _write(d / "job.json", {"id": job_id, "kind": kind, "provider": provider, "provider_kind": p["kind"], "external": external,
                            "target": {k: v for k, v in target.items() if k != "texts"}, "source": source,
                            "created": time.strftime("%Y-%m-%d %H:%M:%S"), "sent": sent, "from_job": from_job})
    if comment and not from_job:
        add_comment(ws, job_id, comment, "studio")
    return d


def command(cfg: dict, d: Path) -> list[str]:
    """작업을 돌릴 명령. cli 는 등록한 명령 틀, openai 는 이 모듈."""
    job = _read(d / "job.json")
    p = _provider(cfg, job["provider"])
    if p["kind"] == "openai":
        return [sys.executable, "-m", "studio.analyzers", "openai", str(d)]
    cmd = resolve_cmd(p)
    if not cmd:
        raise ValueError(f"{job['provider']}: 실행 파일을 찾지 못했습니다")
    task_text = (d / "TASK.md").read_text(encoding="utf-8")
    image = d / "input" / ("source.png" if job["kind"] == "html" else "page_0.png")
    fill = {"job_dir": str(d), "image": str(image), "task_file": str(d / "TASK.md"), "task_text": task_text}
    return [cmd] + [a.format(**fill) if isinstance(a, str) else str(a) for a in p.get("args", ["{task_text}"])]


def env(cfg: dict) -> dict:
    """CLI 가 작업 폴더 안에서 python -m docgen.preview 를 돌릴 수 있게."""
    return {"PYTHONPATH": os.pathsep.join([str(ROOT)] + ([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else []))}


# ---------------------------------------------------------------------------
# openai 방식 (작업 프로세스 안에서 돈다)
# ---------------------------------------------------------------------------

def run_openai(d: Path, cfg: dict) -> None:
    from urllib.request import Request, urlopen

    job = _read(d / "job.json")
    p = _provider(cfg, job["provider"])
    task = (d / "TASK.md").read_text(encoding="utf-8")
    if job["kind"] == "html":
        task += ("\n\n## 답 형식 (이 연결은 파일을 쓸 수 없으므로)\n\n"
                 'JSON 하나로만 답한다: {"template.html.j2": "<템플릿 전체>", "form.json": {…}}\n')
        images = [d / "input" / "source.png"]
    else:
        task += "\n\n## 답 형식\n\nlayout.json 내용(JSON 하나)만 답한다.\n"
        images = sorted((d / "input").glob("page_*.png"))
    content = [{"type": "text", "text": task}] + [
        {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(im.read_bytes()).decode()}}
        for im in images]
    body = {"model": p.get("model"), "messages": [{"role": "user", "content": content}], "temperature": 0,
            "max_tokens": int(p.get("max_tokens", 16000))}
    print(f"요청: {p['base_url']} · {p.get('model')} · 그림 {len(images)}장", flush=True)
    req = Request(p["base_url"].rstrip("/") + "/chat/completions", data=json.dumps(body).encode("utf-8"),
                  headers={"Content-Type": "application/json", **_auth(p)})
    with urlopen(req, timeout=int(p.get("timeout", 900))) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    text = data["choices"][0]["message"]["content"]
    (d / "output" / "raw_answer.txt").write_text(text, encoding="utf-8")
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise SystemExit("답에서 JSON 을 찾지 못했습니다 (output/raw_answer.txt)")
    ans = json.loads(m.group(0))
    if job["kind"] == "html":
        (d / "output" / "template.html.j2").write_text(ans["template.html.j2"], encoding="utf-8")
        _write(d / "output" / "form.json", ans["form.json"])
    else:
        _write(d / "output" / "layout.json", ans)
    print("결과를 output/ 에 썼습니다", flush=True)


# ---------------------------------------------------------------------------
# 결과 검사·보기·승인
# ---------------------------------------------------------------------------

def validate(d: Path) -> dict:
    """결과 형식 검사 + (html) 행 최소·최대로 렌더링해 본다. 작업이 끝나면 부른다."""
    job = _read(d / "job.json")
    out = d / "output"
    res = {"ok": False, "errors": [], "renders": {}}
    if job["kind"] == "html":
        for f in ("template.html.j2", "form.json"):
            if not (out / f).exists():
                res["errors"].append(f"output/{f} 가 없습니다")
        if res["errors"]:
            return _save_result(d, res)
        try:
            form = json.loads((out / "form.json").read_text(encoding="utf-8"))
            if not isinstance(form.get("fields", {}), dict) or not isinstance(form.get("lists", {}), dict):
                res["errors"].append("form.json 의 fields·lists 는 객체")
        except json.JSONDecodeError as e:
            res["errors"].append(f"form.json: {e}")
            return _save_result(d, res)
        for rows in ("min", "max"):
            r = subprocess.run([sys.executable, "-m", "docgen.preview", "--dir", str(out), "--rows", rows, "--out", str(d / "check")],
                               capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(ROOT),
                               env={**os.environ, **env({}), "PYTHONIOENCODING": "utf-8"}, timeout=300)
            if r.returncode != 0:
                res["errors"].append(f"렌더링 실패 (행 {rows}): {(r.stderr or r.stdout).strip().splitlines()[-1:] or ['?']}")
                continue
            info = json.loads(r.stdout.strip().splitlines()[-1])
            info["images"] = [str(Path(p).resolve().relative_to(d.resolve())).replace("\\", "/") for p in info["images"]]
            res["renders"][rows] = info
        res["ok"] = not res["errors"]
    else:
        try:
            lay = json.loads((out / "layout.json").read_text(encoding="utf-8"))
            items = lay.get("items") if isinstance(lay, dict) else None
            if not isinstance(items, list):
                raise ValueError('{"items": [...]} 형식이 아닙니다')
            n_pages = len(list((d / "input").glob("page_*.png")))
            bad = [i for i, it in enumerate(items) if it.get("t") not in ("text", "check", "sign", "date")
                   or not (isinstance(it.get("rect"), list) and len(it["rect"]) == 4) or not 0 <= int(it.get("page", 0)) < n_pages]
            if bad:
                res["errors"].append(f"형식이 틀린 항목 {len(bad)}개 (번호 {bad[:10]})")
            res["items"] = len(items)
            res["ok"] = not bad and bool(items)
        except FileNotFoundError:
            res["errors"].append("output/layout.json 가 없습니다")
        except (ValueError, json.JSONDecodeError) as e:
            res["errors"].append(f"layout.json: {e}")
    return _save_result(d, res)


def _save_result(d: Path, res: dict) -> dict:
    res["checked"] = time.strftime("%Y-%m-%d %H:%M:%S")
    _write(d / "result.json", res)
    return res


def list_jobs(ws: Path) -> list[dict]:
    out = []
    for f in sorted(_root(ws).glob("*/job.json"), reverse=True):
        j = _read(f)
        rv = _read(f.parent / "review.json", {}) or {}
        out.append({**j, "result": _read(f.parent / "result.json"), "approved": rv.get("approved")})
    return out


def get_job(ws: Path, job_id: str) -> dict:
    d = _root(ws) / job_id
    if not (d / "job.json").exists():
        raise KeyError(job_id)
    j = _read(d / "job.json")
    files = {}
    for name in ("template.html.j2", "form.json", "layout.json", "raw_answer.txt"):
        f = d / "output" / name
        if f.exists():
            files[name] = f.read_text(encoding="utf-8")[:200_000]
    return {**j, "task": (d / "TASK.md").read_text(encoding="utf-8"), "output": files, "result": _read(d / "result.json"),
            "review": _read(d / "review.json", {}) or {}, "inputs": sorted(p.name for p in (d / "input").iterdir() if p.is_file())}


def job_file(ws: Path, job_id: str, rel: str) -> Path:
    d = (_root(ws) / job_id).resolve()
    f = (d / rel).resolve()
    if d not in f.parents or not f.is_file():
        raise KeyError(rel)
    return f


def add_comment(ws: Path, job_id: str, text: str, by: str) -> dict:
    d = _root(ws) / job_id
    rv = _read(d / "review.json", {}) or {}
    rv.setdefault("comments", []).append({"at": time.strftime("%Y-%m-%d %H:%M"), "by": by, "text": text})
    _write(d / "review.json", rv)
    return rv


def approve(ws: Path, job_id: str, by: str, form_id: str | None = None, name: str | None = None,
            private_dir: str | None = None) -> dict:
    """승인: html 은 서식 폴더로 복사해 등록 (실서류 그림이면 private_forms_dir), layout 은 대상 overlay(image) 서식의
    사람 수정에 값 영역 초안(add)으로 더한다. 등록한 서식은 검수 전 상태로 시작한다."""
    d = _root(ws) / job_id
    job = _read(d / "job.json")
    res = _read(d / "result.json") or {}
    if not res.get("ok"):
        raise ValueError("결과 검사를 통과하지 못한 작업은 승인할 수 없습니다")
    if job["kind"] == "html":
        from docgen import htmlform as H
        from docgen.registry import load_all

        form_id = form_id or job["target"].get("form_id")
        if job["target"].get("update") and form_id == job["target"].get("form_id") and H.form_dir(form_id):
            # 편집기에서 "다시 고쳐"로 맡긴 것: 그 서식을 고친 결과로 바꾼다 (이름·출처는 그대로)
            old = H.load_form(form_id)
            form = json.loads((d / "output" / "form.json").read_text(encoding="utf-8"))
            form.update({k: old[k] for k in ("origin", "source_image", "parent") if k in old}, from_job=job_id)
            H.save(form_id, (d / "output" / "template.html.j2").read_text(encoding="utf-8"), form)
            rv = _read(d / "review.json", {}) or {}
            rv["approved"] = {"as": form_id, "updated": True, "at": time.strftime("%Y-%m-%d %H:%M"), "by": by}
            _write(d / "review.json", rv)
            return rv["approved"]
        if not form_id or not H.ID_RX.fullmatch(form_id) or form_id in load_all() or H.form_dir(form_id):
            raise ValueError(f"서식 ID 를 확인하세요 (영어 소문자·숫자·밑줄, 겹치지 않게): {form_id}")
        private = bool(job["source"].get("real_data")) and not job["source"].get("public")
        if private and not private_dir:
            raise ValueError("실서류 그림에서 만든 서식은 private_forms_dir 에만 둡니다. 설정에 private_forms_dir 을 정하세요")
        dest = (Path(private_dir) if private else H.COPIES) / form_id
        dest.mkdir(parents=True)
        shutil.copyfile(d / "output" / "template.html.j2", dest / "template.html.j2")
        form = json.loads((d / "output" / "form.json").read_text(encoding="utf-8"))
        form.update({"origin": "analyzer", "source_image": "source.png", "from_job": job_id})
        if name:
            form["name"] = name
        (dest / "form.json").write_text(json.dumps(form, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        shutil.copyfile(d / "input" / "source.png", dest / "source.png")
        H.register_forms()
        approved = {"as": form_id, "dir": str(dest), "private": private}
    else:
        from docgen import overrides as OV
        from docgen import realform as RF

        form_id = job["target"].get("form_id")
        if not form_id or RF.image_form_dir(form_id) is None:
            raise ValueError("layout 결과는 가져온 이미지 서식(img_*)에만 붙입니다")
        lay = json.loads((d / "output" / "layout.json").read_text(encoding="utf-8"))
        ov = OV.load(form_id)
        k = RF.BG_ZOOM
        pt = lambda r: [round(v / k, 2) for v in r]  # noqa: E731  그림 픽셀 → pt
        for it in lay["items"]:
            a = {"t": it["t"], "page": int(it.get("page", 0)), "label": it.get("label", ""), "rect": pt(it["rect"]),
                 "note": f"분석기 초안 ({job_id})"}
            if it.get("key"):
                a["key"] = it["key"]
            if it["t"] == "check" and it.get("options"):
                a["options"] = [{"text": o.get("text", ""), "box": pt(o["box"]), "rect": pt(o.get("rect") or o["box"])}
                                for o in it["options"] if o.get("box")]   # box: □ 자리, rect: 보기 글자까지 (영역 편집기와 같은 꼴)
            ov.setdefault("add", []).append(a)
        OV.save(form_id, ov)
        approved = {"as": form_id, "added": len(lay["items"])}
    rv = _read(d / "review.json", {}) or {}
    rv["approved"] = {**approved, "at": time.strftime("%Y-%m-%d %H:%M"), "by": by}
    _write(d / "review.json", rv)
    return rv["approved"]


def main(argv=None) -> None:
    import argparse

    ap = argparse.ArgumentParser(prog="studio.analyzers")
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("openai")
    o.add_argument("job_dir")
    a = ap.parse_args(argv)
    from .config import load

    run_openai(Path(a.job_dir), load())


if __name__ == "__main__":
    main()
