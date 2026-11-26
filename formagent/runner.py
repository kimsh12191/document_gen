"""회차 진행기: ReLab 을 스킬 form-from-image 로 회차마다 돌리고, 회차 사이에 검사하고 그림을 붙여 다음 요청을 넣는다.

  out/form_drafts/<ID>/
    source.png, source_2.png …     원본 (시작할 때)
    run.json                       상태: status(running/waiting/done/stopped/failed) · 회차마다 요청·종료 코드·검사 요약
    relab_<n>.log                  n회차 ReLab 출력 그대로
    check_<n>/                     n회차 뒤 진행기의 검사 (check.py: check.json · side_*.jpg · renders.jpg · render_*/)
    source_text.md                 1회차(글자 옮기기)에 모델이 그림에서 옮겨 적은 인쇄 글자
    fields.md · template.html.j2 · form.json · generate.py · review.md · report.md   ← 2회차(만들기)·3회차부터(고치기)에 모델이 쓴 것

회차: 1 글자 옮기기(source_text.md 가 없을 때) → 2 만들기(template 이 없을 때) → 3~ 원본과 비교하며 고치기.
글자 옮기기를 따로 하는 까닭: 문서를 잔뜩 읽은 뒤 그림을 보면 약한 모델은 그림 대신 짐작으로 항목명을 쓴다 (PLAN.md 14절).
    report.json                    끝날 때 진행기의 마지막 검사·초안 밖 변경·회차 요약

ReLab 의 `-p` 는 `-c` 를 보지 않아 회차마다 새 대화다. 앞 회차는 초안 폴더의 파일과 요청 문장으로 넘긴다 (PLAN.md 2·13절).
요청에 경로("폴더/파일")로 적은 파일은 그 회차에 읽어야 ReLab 이 끝내기를 받는다. 그래서 읽을 필요 없는 파일은 경로 없이 이름만 적는다.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageOps

from . import relab as R

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "out" / "form_drafts"
SKILL = ".claude/skills/form-from-image"
ID_RX = re.compile(r"[a-z][a-z0-9_]{2,50}")
BAD_WORDS = ("private", "secrets")          # ReLab 이 경로 조각으로 막는 이름
KINDS = {"blank": "빈 서식", "sample": "견본", "real": "실서류 (값이 적힌 진짜 서류 — 실제 값을 어느 파일에도 옮기지 않는다)"}
MAX_IMAGE_BYTES = 1_900_000                  # ReLab: 그림 한 장 2MB, 요청당 4장
MAX_PAGES = 3
SKIP_DIRS = {".git", "out", "__pycache__", ".pytest_cache", "node_modules", ".relab", "studio_workspace", "studio_cache",
             "studio_jobs", "studio_private_forms", "studio_deps", "bench_out", "preds", "temp"}
SKIP_PREFIXES = ("train/runs", "train/data")


class AgentError(RuntimeError):
    pass


# ---------------------------------------------------------------- 상태 파일

def draft_dir(form_id: str) -> Path:
    return DRAFTS / form_id


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def load(form_id: str) -> dict:
    f = draft_dir(form_id) / "run.json"
    if not f.exists():
        raise AgentError(f"{form_id} 작업이 없습니다 ({rel(f)})")
    return json.loads(f.read_text(encoding="utf-8"))


def save(state: dict) -> None:
    f = draft_dir(state["id"]) / "run.json"
    tmp = f.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(f)


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


# ---------------------------------------------------------------- 준비

def check_id(form_id: str) -> None:
    if not ID_RX.fullmatch(form_id):
        raise AgentError("서식 ID 는 영어 소문자로 시작, 소문자·숫자·밑줄 3~51자")
    if any(w in form_id for w in BAD_WORDS):
        raise AgentError(f"서식 ID 에 {', '.join(BAD_WORDS)} 를 넣을 수 없습니다 (ReLab 이 그 경로를 막음)")
    p = subprocess.run([sys.executable, "-m", "docgen.formdir", "path", form_id], cwd=ROOT, capture_output=True, text=True)
    if "없습니다" not in p.stdout + p.stderr:
        raise AgentError(f"이미 있는 서식 ID 입니다: {form_id}")
    if draft_dir(form_id).exists():
        raise AgentError(f"초안 폴더가 이미 있습니다: {rel(draft_dir(form_id))} (이어서 하려면 continue)")


def package_marks(d: Path) -> None:
    """out/ · out/form_drafts/ · 초안 폴더에 빈 __init__.py.

    ReLab 은 요청에 적힌 폴더(또는 쓴 파일들의 맨 위 폴더)를 "프로젝트 폴더"로 잡고, 그 밖의 코드 import 를 막고 명령을
    그 안에서 돌린다. 그 폴더가 맨 위까지 파이썬 패키지면 작업 공간 전체를 프로젝트로 본다 (relab_app/project_scope.project_of).
    그래서 초안의 generate.py 가 docgen.formkit 을 import 하고, 검사 명령이 저장소 맨 위에서 돈다."""
    for folder in (DRAFTS.parent, DRAFTS, d):
        mark = folder / "__init__.py"
        if not mark.exists():
            mark.write_text('"""formagent: ReLab 이 저장소 전체를 프로젝트로 보게 하는 표시 (formagent/runner.py package_marks)."""\n',
                            encoding="utf-8")


ENV_KEYS = ("PLAYWRIGHT_BROWSERS_PATH", "CHROMIUM_PATH", "DOCGEN_PRIVATE_FORMS")


def save_env() -> None:
    """ReLab 은 검사 명령에 환경 변수를 몇 개(PATH·HOME …)만 넘긴다. 미리보기가 브라우저를 찾도록 지금 환경의 위치를
    out/form_drafts/.formagent_env.json 에 남기고, 스킬 check.py 가 읽어 채운다."""
    DRAFTS.mkdir(parents=True, exist_ok=True)
    env = {k: os.environ[k] for k in ENV_KEYS if os.environ.get(k)}
    (DRAFTS / ".formagent_env.json").write_text(json.dumps(env, ensure_ascii=False, indent=1), encoding="utf-8")


def save_image(src: Path, dest: Path) -> None:
    """원본을 png 로, 2MB 아래로 줄여 저장."""
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    longest = 2400
    while True:
        if max(im.size) > longest:
            im.thumbnail((longest, longest))
        im.save(dest, optimize=True)
        if dest.stat().st_size <= MAX_IMAGE_BYTES or longest < 900:
            return
        longest = int(longest * 0.8)


def snapshot() -> dict[str, list[int]]:
    """저장소 파일 크기·시각 (초안 폴더·작업 폴더류 제외). 초안 밖 변경을 찾는 데 쓴다 (git 이 없어도 됨)."""
    files = {}
    for top, dirs, names in os.walk(ROOT):
        r = Path(top).relative_to(ROOT).as_posix()
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not f"{r}/{d}".lstrip("./").startswith(SKIP_PREFIXES)]
        for n in names:
            p = Path(top) / n
            try:
                st = p.stat()
            except OSError:
                continue
            files[p.relative_to(ROOT).as_posix()] = [st.st_size, st.st_mtime_ns]
    return files


def outside_changes(before: dict, after: dict) -> list[str]:
    out = [f"새로 생김: {k}" for k in after if k not in before]
    out += [f"없어짐: {k}" for k in before if k not in after]
    out += [f"바뀜: {k}" for k in after if k in before and after[k] != before[k]]
    return sorted(out)


def _skill(name: str):
    """스킬 폴더의 스크립트를 모듈로 (check.py · register.py)."""
    spec = importlib.util.spec_from_file_location(f"form_{name}", ROOT / SKILL / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def register(form_id: str, to: str, log=print) -> dict:
    """초안을 등록 폴더로 (스킬 register.py). 실서류는 비공개 폴더만. run.json 에 registered 를 남긴다."""
    state = load(form_id)
    if state.get("registered"):
        raise AgentError(f"이미 등록했습니다: {state['registered']['path']}")
    if state.get("status") in ("running", "installing"):
        raise AgentError("아직 돌고 있습니다")
    mod = _skill("register")
    try:
        out = mod.register(draft_dir(form_id), to, form_id, real=state.get("kind") == "real", log=log)
    except mod.RegisterError as e:
        raise AgentError(str(e))
    state["registered"] = {"to": to, "path": out["path"], "at": now(), "files": out["files"],
                           "card_ok": out["card"]["ok"], "check_ok": out["formdir_check"]["ok"]}
    save(state)
    return out


def run_check(draft: Path, out: Path) -> dict:
    """스킬의 check.py 로 검사."""
    return _skill("check").run(draft, out)


# ---------------------------------------------------------------- 요청 문장

def _head(state: dict, n: int) -> list[str]:
    d = state["draft"]
    return [f"- 서식 ID: {state['id']} · 초안 폴더: {d}/ · 원본 종류: {KINDS[state['kind']]}",
            f"- 검사 명령: python -m pytest {SKILL}/test_draft.py --draft {d} -q  (통과해야 끝난다. 문제·경고는 명령 출력에 나온다)",
            "- 초안 폴더 밖의 파일은 만들거나 고치지 않는다. 등록(스킬 7단계)은 하지 않는다."]


def round_kind(state: dict) -> str:
    """이번 회차에 할 일: read(글자 옮기기) · build(만들기) · fix(비교하며 고치기)."""
    d = draft_dir(state["id"])
    if not (d / "source_text.md").exists():
        return "read"
    if not (d / "template.html.j2").exists() or not (d / "form.json").exists():
        return "build"
    return "fix"


def read_request(state: dict, n: int) -> str:
    """1회차: 그림만 보고 인쇄 글자를 옮겨 적는다. 문서는 읽지 않는다 (그림에 집중).
    쓸 파일은 경로로 적지 않는다 — ReLab 은 요청에 경로로 적힌 파일을 그 회차에 읽어야 끝내기를 받는다."""
    d = state["draft"]
    pics = " ".join(f"@{d}/{s}" for s in state["sources"])
    pages = len(state["sources"])
    lines = [pics,
             f"붙인 그림 {pages}장은 서식 원본이다 ({'쪽 순서대로 ' if pages > 1 else ''}쪽마다 한 장). 그림은 이 요청에 붙어 있어 지금 보인다. "
             f"서식 만들기의 {n}회차 — 글자 옮기기다. 다른 파일은 읽지 말고 그림만 보고 한다.",
             f"- 서식 ID: {state['id']} · 원본 종류: {KINDS[state['kind']]}",
             "- 할 일: 그림에 인쇄된 글자를 위에서 아래로 빠짐없이 그대로, 붙인 그림과 같은 폴더(초안 폴더)에 source_text.md 라는 이름으로 적는다 "
             "(스킬 1-1단계). 꼴:",
             "  · 쪽마다 `## 1쪽`, 그 안에서 덩어리마다 `### <덩어리 이름>` (결재란 · 제목 · 위 정보 표 · 목록 표 · 체크 항목 · 안내문/약관 · 날짜·서명란 · 맨 아래).",
             "  · 한 줄에 그림의 한 줄. 같은 줄에 칸이 여럿이면 ` | ` 로 나눈다. 값이 들어갈 빈 칸은 `( )`.",
             "  · 영어·숫자·기호·괄호는 그림 그대로 (`대상계좌 (발급세부)`, `(통화코드 : )`, `□ E-mail :`, `□ 등록`). 한글 띄어쓰기도 그대로.",
             "  · 안내문·약관은 문장 끝까지 전부. 줄이거나 \"…\"로 자르지 않는다.",
             "  · 손글씨·타자로 채운 값(이름·번호·금액·날짜·체크 표시)은 옮기지 않고 `(값)` 으로. 로고·바코드·도장은 `(로고: 글자)` `(바코드)` `(도장)`.",
             "  · 작거나 흐려 못 읽는 곳은 `(안 보임: 어디)`. 짐작으로 채우지 않고, 그림에 없는 글자를 더하지 않는다.",
             "- 이번 회차는 source_text.md 하나만 쓴다. fields.md·template·form.json 은 다음 회차에 쓴다. 검사 명령은 돌리지 않는다. 다 쓰면 끝낸다."]
    if state.get("note"):
        lines.append(f"- 사람의 추가 요청 (다음 회차에 반영할 것 — 이번에는 참고만): {state['note']}")
    return "\n".join(lines)


def build_request(state: dict, n: int, message: str | None = None) -> str:
    """2회차: 원본 그림을 다시 붙이고, source_text.md 를 글자의 기준으로 서식을 만든다."""
    d = state["draft"]
    pics = " ".join(f"@{d}/{s}" for s in state["sources"])
    lines = [pics,
             f"{SKILL}/SKILL.md 를 끝까지 읽고 그 순서를 따라, 붙인 그림으로 docgen 서식을 만들어라. {n}회차 — 만들기다.",
             *_head(state, n),
             f"- 붙인 그림은 원본이다 (쪽마다 한 장, 지금 보인다). 앞 회차에 그림의 인쇄 글자를 {d}/source_text.md 에 옮겨 두었다 — 먼저 읽는다.",
             "- 항목명·제목·안내문 글자는 source_text.md 에서 그대로 옮긴다. source_text.md 에 없는 항목명은 만들지 않는다 "
             "(그림에 있는데 빠졌으면 source_text.md 에 먼저 더한다). 표 모양·칸 나눔·자리는 붙인 그림을 보고 정한다.",
             "- 이번 회차: 스킬 0단계 1~2(읽기), 1-2단계(fields.md), 2~4단계. fields.md 를 먼저 끝까지 쓰고, template.html.j2 · form.json "
             "(칸끼리 관계가 있으면 generate.py) 을 쓴 뒤 검사 명령을 통과시킨다.",
             "- 원본과 렌더를 나란히 놓은 그림은 다음 회차 요청에 붙여 준다 (붙인 그림 말고 다른 그림 파일은 열어 볼 수 없다).",
             "- 원본 비교(5단계)는 진행기가 다음 회차로 넘긴다. 검사 명령이 통과하면 끝내고, 그것을 \"Not done\"에 적지 않는다."]
    if state.get("note"):
        lines.append(f"- 사람의 추가 요청: {state['note']}")
    if message:
        lines.append(f"- 사람의 지시 (가장 먼저 반영): {message}")
    return "\n".join(lines)


def first_request(state: dict) -> str:
    """처음 회차의 요청 (지금은 글자 옮기기)."""
    return round_request(state, 1, None)


def next_request(state: dict, n: int, check: dict, message: str | None = None) -> str:
    """고치기 회차: 원본|렌더 그림을 붙이고 비교·고치기·보고."""
    d = state["draft"]
    imgs = check.get("images") or {}
    pics = [p for p in (imgs.get("side") or [])[:3]] + ([imgs["renders"]] if imgs.get("renders") else [])
    pics = [f"@{rel(Path(p))}" for p in pics[:4]]
    have = [f for f in ("source_text.md", "fields.md", "template.html.j2", "form.json", "generate.py", "review.md", "report.md")
            if (draft_dir(state["id"]) / f).exists()]
    probs = check.get("problems") or []
    warns = check.get("warnings") or []
    lines = [" ".join(pics),
             f"{SKILL}/SKILL.md 를 따르는 서식 만들기의 {n}회차 — 원본과 비교하며 고치기다. 새 대화라 앞 회차의 대화는 없다 — SKILL.md 와 초안 폴더의 파일을 먼저 읽어라.",
             *_head(state, n),
             f"- 앞 회차까지 초안 폴더에 쓴 것: {', '.join(have) or '없음'}. source_text.md(원본 글자)·fields.md 와 (있으면) review.md 를 먼저 읽는다.",
             "- 붙인 그림(지금 보인다): side_*.jpg = 왼쪽 원본 · 오른쪽 렌더(--rows min, 쪽마다), renders.jpg = 렌더 모음(min·max·seed1·seed2 첫 쪽).",
             f"- 직전 검사: {'통과' if check.get('passed') else '통과 못 함'}"]
    lines += [f"  · 문제: {p}" for p in probs[:12]]
    lines += [f"  · 경고: {w}" for w in warns[:12]]
    sample = sample_values(check)
    if sample:
        lines.append("- 렌더 값 예시 (키: seed 1 값 / seed 2 값) — 값이 칸의 뜻에 맞는지 본다 (스킬 5단계 9번):")
        lines += [f"  · {line}" for line in sample]
    if message:
        lines.append(f"- 사람의 지시 (가장 먼저 반영): {message}")
    lines.append(f"- 할 일: 스킬 5단계대로 원본과 렌더를 비교해 review.md 에 '{n}회차' 9문항을 더하고, 문제·경고·\"아니오\"를 고친 뒤 검사 명령을 통과시킨다. "
                 "원본 글자 대조 경고(지어낸 글자·빠진 글자)는 그림을 보고 판단해 고친다. "
                 "고칠 것이 없으면 review.md 에 그렇게 적는다. 끝나면 스킬 6단계 보고를 초안 폴더의 report.md 로 쓴다 (있으면 고쳐 쓴다).")
    return "\n".join(lines)


def sample_values(check: dict, limit: int = 70) -> list[str]:
    """검사 렌더의 키→값 두 벌 (seed 1·2). 반복 표는 첫 행만. 요청에 직접 넣어 모델이 파일을 안 읽어도 보게."""
    vals = check.get("values") or {}
    a, b = vals.get("s1") or vals.get("min") or {}, vals.get("s2") or {}
    out = []
    for key, v in a.items():
        parts = key.split(".")
        if any(p.isdigit() and p != "0" for p in parts):
            continue
        w = b.get(key)
        cut = lambda x: (str(x)[:40] + "…") if x is not None and len(str(x)) > 40 else ("(빈 칸)" if x in (None, "") else str(x))  # noqa: E731
        out.append(f"{key}: {cut(v)}" + (f" / {cut(w)}" if key in b else ""))
        if len(out) >= limit:
            break
    return out


def round_request(state: dict, n: int, check: dict | None, message: str | None = None) -> str:
    """이번 회차의 요청: 초안 폴더에 무엇이 있는지로 고른다."""
    kind = round_kind(state)
    if kind == "read":
        req = read_request(state, n)
        return req + (f"\n- 사람의 지시: {message}" if message else "")
    if kind == "build":
        return build_request(state, n, message)
    return next_request(state, n, check or {}, message)


# ---------------------------------------------------------------- 진행

def start(images: list[str], form_id: str, kind: str, note: str | None = None, settings: dict | None = None) -> dict:
    """초안 폴더와 run.json 을 만든다 (ReLab 은 아직 안 돌림)."""
    if kind not in KINDS:
        raise AgentError(f"원본 종류는 {', '.join(KINDS)} 중 하나")
    if not images or len(images) > MAX_PAGES:
        raise AgentError(f"이미지는 쪽마다 한 장, 1~{MAX_PAGES}장")
    check_id(form_id)
    d = draft_dir(form_id)
    d.mkdir(parents=True)
    package_marks(d)
    names = []
    for i, src in enumerate(images):
        name = "source.png" if i == 0 else f"source_{i + 1}.png"
        save_image(Path(src), d / name)
        names.append(name)
    state = {"id": form_id, "kind": kind, "note": note, "draft": rel(d), "sources": names, "status": "ready",
             "created": now(), "settings": settings or {}, "rounds": [], "relab_pid": None, "runner_pid": None}
    save(state)
    return state


def stop(form_id: str) -> dict:
    """멈춤: 표시를 남기고 돌고 있는 relab 을 끝낸다."""
    state = load(form_id)
    (draft_dir(form_id) / "STOP").write_text(now(), encoding="utf-8")
    for key in ("relab_pid",):
        pid = state.get(key)
        if pid:
            try:
                os.killpg(pid, signal.SIGTERM)
            except (ProcessLookupError, PermissionError):
                pass
    return state


def _alive(pid) -> bool:
    if not pid:
        return False
    try:
        os.kill(int(pid), 0)
        return True
    except (OSError, ValueError):
        return False


def delete(form_id: str) -> dict:
    """초안 폴더를 통째로 지운다 (원본 그림·회차 기록·검사 그림). 등록한 서식 폴더는 건드리지 않는다. 도는 중이면 거절."""
    if not ID_RX.fullmatch(form_id or ""):
        raise AgentError(f"서식 ID 꼴이 아닙니다: {form_id!r}")
    d = draft_dir(form_id)
    state = load(form_id)
    if state.get("status") in ("running", "installing") and (_alive(state.get("runner_pid")) or _alive(state.get("relab_pid"))):
        raise AgentError("도는 중입니다. 멈춘 뒤에 지우세요")
    if d.resolve().parent != DRAFTS.resolve():
        raise AgentError(f"초안 폴더가 아닙니다: {d}")
    shutil.rmtree(d)
    return {"id": form_id, "deleted": rel(d), "registered": state.get("registered")}


def go(form_id: str, message: str | None = None, max_rounds: int | None = None, log=print) -> dict:
    """회차를 돈다. 처음이면 1회차부터, 이어서면 사람의 지시로 한 회차 + 고치기."""
    state = load(form_id)
    d = draft_dir(form_id)
    st = state["settings"]
    fix_rounds = max_rounds if max_rounds is not None else int(st.get("max_fix_rounds", 3))
    (d / "STOP").unlink(missing_ok=True)
    package_marks(d)
    save_env()
    if not R.find(st.get("relab")) and not st.get("relab"):     # 없으면 묶음으로 설치 (화면에 "ReLab 설치 중")
        state.update(status="installing", runner_pid=os.getpid())
        save(state)
    try:
        relab = R.ensure(st.get("relab"), log=log)
    except R.RelabError as e:
        state.update(status="failed", error=str(e))
        save(state)
        raise
    state.update(status="running", runner_pid=os.getpid(), relab=relab, relab_version=R.VERSION)
    save(state)
    stopped = lambda: (d / "STOP").exists()  # noqa: E731
    first = not state["rounds"]
    planned = (2 + fix_rounds) if first else (1 + max(0, fix_rounds - 1))     # 처음: 글자 옮기기 + 만들기 + 고치기 회차
    before = snapshot()
    last_check = state["rounds"][-1].get("check_full") if state["rounds"] else None
    for k in range(planned):
        if stopped():
            state.update(status="stopped", error="멈춤")
            break
        n = len(state["rounds"]) + 1
        kind = round_kind(state)
        if kind == "fix" and last_check is None:
            last_check = run_check(d, d / f"check_{n - 1}")
        request = round_request(state, n, last_check, message if k == 0 else None)
        rnd = {"n": n, "kind": kind, "request": request, "started": now(), "log": f"relab_{n}.log"}
        state["rounds"].append(rnd)
        save(state)
        log(f"[{form_id}] {n}회차 시작")
        t0 = time.time()

        def remember(pid):
            state["relab_pid"] = pid
            save(state)

        cmd = R.command(relab, request, ROOT, st.get("provider"), st.get("endpoint"), st.get("model"))
        code = R.run(cmd, d / rnd["log"], ROOT, float(st.get("round_minutes", 60)), on_start=remember, stopped=stopped)
        rnd.update(exit=code, ended=now(), seconds=round(time.time() - t0))
        state["relab_pid"] = None
        if code is None:
            state["status"] = "stopped" if stopped() else "failed"
            state["error"] = "멈춤" if stopped() else "회차 시간 한도를 넘음"
            break
        if code == 2:
            state.update(status="failed", error="ReLab 이 시작하지 못함 (종료 코드 2) — " + tail(d / rnd["log"]))
            break
        if kind == "read":                  # 글자 옮기기 뒤에는 서식 검사가 할 게 없다 (템플릿이 아직 없는 게 정상)
            last_check = None
            got = (d / "source_text.md").exists()
            rnd["read"] = {"source_text": got}
            log(f"[{form_id}] {n}회차 끝: 종료 코드 {code}, source_text.md {'있음' if got else '없음 — 다음 회차에 다시 옮긴다'}")
        else:
            last_check = run_check(d, d / f"check_{n}")
            rnd["check"] = {k2: last_check[k2] for k2 in ("passed", "problems", "warnings")}
            rnd["check_full"] = {k2: last_check[k2] for k2 in ("passed", "problems", "warnings", "images")}
            rnd["check_full"]["values"] = {s: v for s, v in (last_check.get("values") or {}).items() if s in ("s1", "s2")}
            log(f"[{form_id}] {n}회차 끝: 종료 코드 {code}, 검사 {'통과' if last_check['passed'] else '통과 못 함'}")
        if code == 3:
            state.update(status="waiting", question=tail(d / rnd["log"], 25))
            break
        report = d / "report.md"
        if kind == "fix" and last_check and last_check["passed"] and report.exists() and report.stat().st_mtime >= t0:
            state["status"] = "done"
            break
        save(state)
    else:
        state["status"] = "done"
        state["note_end"] = "고치기 회차 한도까지 돌았다"
    changes = outside_changes(before, snapshot())
    final = run_check(d, d / "check_final") if (d / "template.html.j2").exists() else {"passed": False, "problems": ["초안이 없습니다"], "warnings": [], "images": {}}
    (d / "report.json").write_text(json.dumps({
        "id": form_id, "status": state["status"], "rounds": [{k2: r.get(k2) for k2 in ("n", "exit", "seconds", "check")} for r in state["rounds"]],
        "final_check": {k2: final.get(k2) for k2 in ("passed", "problems", "warnings", "renders", "images")},
        "outside_changes": changes, "report_md": (d / "report.md").exists()}, ensure_ascii=False, indent=1), encoding="utf-8")
    state["outside_changes"] = changes       # 마지막 검사·report.json 을 쓴 뒤에 상태를 끝으로 (화면이 끝남을 보면 결과가 다 있게)
    state["ended"] = now()
    save(state)
    if changes:
        log(f"[{form_id}] 경고: 초안 폴더 밖에서 바뀐 파일 {len(changes)}개 — report.json 의 outside_changes")
    log(f"[{form_id}] {state['status']} · 마지막 검사 {'통과' if final.get('passed') else '통과 못 함'} · {rel(d / 'report.json')}")
    return state


def tail(path: Path, lines: int = 8) -> str:
    try:
        return "\n".join(path.read_text(encoding="utf-8", errors="replace").strip().splitlines()[-lines:])
    except OSError:
        return ""
