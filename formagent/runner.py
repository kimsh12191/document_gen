"""회차 진행기: ReLab 을 스킬 form-from-image 로 회차마다 돌리고, 회차 사이에 검사하고 보기 창 그림을 갈아 다음 요청을 넣는다.

  out/form_drafts/<ID>/
    source.png, source_2.png …     원본 (시작할 때)
    page_<n>.png · grid_<n>.json   진행기가 첫 회차 전에 grid.py 로 잰 것 (표·칸·글자 덩어리 자리), grid.txt = 그 목록
    view_1.png … view_4.png        보기 창: 요청에 늘 붙는 그림 네 장. 모델이 view.py 로 다시 쓰면 다음 단계에서 새 그림이 보인다
    run.json                       상태: status(running/waiting/done/stopped/failed) · 회차마다 요청·종료 코드·검사 요약
    relab_<n>.log                  n회차 ReLab 출력 그대로
    check_<n>/                     n회차 뒤 진행기의 검사 (check.py: check.json · side_*.jpg · renders.jpg · render_*/)
    layout.json · generate.py · report.md     ← 모델이 쓴 것 (template.html.j2 · form.json · fields.md 는 build.py 가 layout.json 에서)
    report.json                    끝날 때 진행기의 마지막 검사·초안 밖 변경·회차 요약

회차: 1 만들기(layout.json 이 없을 때: 보기 창으로 칸을 읽어 layout.json → build → 검사) → 2~ 원본과 맞대 보며 고치기.
재기(grid)·html 쓰기(build)는 도구가 하고, 모델은 잘라 크게 본 그림에서 칸 글자를 읽고 값 자리·키를 정한다 (PLAN.md 16절).

ReLab 의 `-p` 는 `-c` 를 보지 않아 회차마다 새 대화다. 앞 회차는 초안 폴더의 파일과 요청 문장으로 넘긴다 (PLAN.md 2·13절).
요청에 경로("폴더/파일")로 적은 파일은 그 회차에 읽어야 ReLab 이 끝내기를 받는다. 그래서 읽을 필요 없는 파일은 경로 없이 이름만 적는다.
ReLab 은 `@` 로 붙인 그림을 단계마다 디스크에서 다시 읽는다 — 그래서 보기 창을 명령으로 다시 쓰면 실행 중에도 새 그림을 볼 수 있다 (PLAN.md 16절).
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
SKILL_DIR = Path(__file__).resolve().parents[1] / SKILL        # 도구는 늘 이 저장소의 스킬 폴더에서 (ROOT 를 바꿔 시험할 때도)
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
    spec = importlib.util.spec_from_file_location(f"form_{name}", SKILL_DIR / f"{name}.py")
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
            f"- 이번에 만드는 서식은 {state['id']} 하나다. out/form_drafts/ 의 다른 초안 폴더는 읽지도 고치지도 않는다 (다른 서식이다).",
            f"- 검사 명령: python -m pytest {SKILL}/test_draft.py --draft {d} -q  (통과해야 끝난다. 문제·경고는 명령 출력에 나온다)",
            "- 초안 폴더 밖의 파일은 만들거나 고치지 않는다. 등록(스킬 8단계)은 하지 않는다."]


VIEWS = 4
def execution_python(settings: dict) -> str:
    """모델이 돌리는 python 명령이 쓸 인터프리터 (ReLab RELAB_EXECUTION_PYTHON — 그 가상환경을 켠 것처럼 PATH·VIRTUAL_ENV 도).
    설정 form_agent.python 이 있으면 그것, 없으면 진행기(studio)를 돌리는 python — 검사 도구가 쓰는 패키지(playwright·jinja2·Pillow)가 있는 곳."""
    given = (settings or {}).get("python")
    path = Path(given).expanduser() if given else Path(sys.executable)
    if not path.is_absolute():
        path = ROOT / path
    return str(path.absolute())


RECORDS = ".relab_home"      # 서식마다 ReLab 기록(대화·loop·메모·교훈) 폴더 — RELAB_PRIVATE_HOME. 모델 설정은 늘 ~/.relab/config.json
FORM_IN_REQUEST = re.compile(r"out/form_drafts/([a-z][a-z0-9_]{2,50})/")


def relab_procs() -> list[dict]:
    """이 저장소를 작업 공간으로 도는 `relab chat` 실행들 (/proc 에서). 요청 글에서 어느 서식인지 찾는다.
    [{pid, form_id, started(시각), runner_alive(그 서식의 진행기가 살아 있나)}]"""
    out = []
    proc = Path("/proc")
    if not proc.is_dir():
        return out
    root = str(ROOT.resolve())
    for p in proc.iterdir():
        if not p.name.isdigit():
            continue
        try:
            args = [a.decode("utf-8", "replace") for a in (p / "cmdline").read_bytes().split(b"\0") if a]
            started = p.stat().st_mtime
        except OSError:
            continue
        if "chat" not in args or "-p" not in args or not any(Path(a).name in ("relab", "relab.exe") for a in args[:3]):
            continue
        ws = args[args.index("--workspace") + 1] if "--workspace" in args[:-1] else None
        if not ws or str(Path(ws).resolve()) != root:
            continue
        request = args[args.index("-p") + 1] if args.index("-p") + 1 < len(args) else ""
        m = FORM_IN_REQUEST.search(request)
        form_id = m.group(1) if m else None
        alive = False
        if form_id and (DRAFTS / form_id / "run.json").exists():
            try:
                st = json.loads((DRAFTS / form_id / "run.json").read_text(encoding="utf-8"))
                alive = st.get("status") in ("running", "installing") and _alive(st.get("runner_pid"))
            except (OSError, ValueError):
                pass
        out.append({"pid": int(p.name), "form_id": form_id, "started": datetime.fromtimestamp(started).strftime("%Y-%m-%d %H:%M:%S"),
                    "runner_alive": alive, "draft_exists": bool(form_id and (DRAFTS / form_id).is_dir())})
    return sorted(out, key=lambda x: x["pid"])


def _gone(pid: int) -> bool:
    """끝났나 (거두지 않은 좀비도 끝난 것으로)."""
    if not _alive(pid):
        return True
    try:
        return (Path("/proc") / str(pid) / "stat").read_text().rsplit(")", 1)[1].split()[0] == "Z"
    except (OSError, IndexError):
        return False


def kill_relab(pid: int) -> bool:
    """이 저장소의 relab chat 실행 하나를 끝낸다 (다른 프로그램이면 거절). 끝냈으면 True."""
    if not any(p["pid"] == pid for p in relab_procs()):
        raise AgentError(f"이 저장소의 relab 실행이 아닙니다: {pid}")
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(pid, sig)                 # 진행기는 relab 을 새 세션으로 띄운다 (명령 자식까지)
        except (ProcessLookupError, PermissionError):
            try:
                os.kill(pid, sig)
            except ProcessLookupError:
                return True
        for _ in range(20):
            if _gone(pid):
                return True
            time.sleep(0.25)
    return _gone(pid)


def kill_relab_quiet(pid: int) -> bool:
    try:
        return kill_relab(pid)
    except AgentError:
        return False


def leftovers() -> list[dict]:
    """끝나지 않고 남은 relab 실행: 그 서식의 진행기가 죽었거나(끊김) 서식 폴더가 없어진 것."""
    return [p for p in relab_procs() if not p["runner_alive"]]


def round_kind(state: dict) -> str:
    """이번 회차에 할 일: build(만들기) · fix(맞대 보며 고치기)."""
    d = draft_dir(state["id"])
    if not (d / "layout.json").exists() or not (d / "template.html.j2").exists():
        return "build"
    return "fix"


def _blank(path: Path, text: str) -> None:
    from PIL import ImageDraw
    im = Image.new("RGB", (640, 80), "white")
    ImageDraw.Draw(im).text((10, 30), text, fill=(120, 120, 120))
    im.save(path)


def measure(state: dict) -> str:
    """grid.py 로 쪽마다 잰다 (없을 때만). grid.txt 에 모델이 읽을 목록을 쓴다."""
    d = draft_dir(state["id"])
    g = _skill("grid")
    if not (d / "grid_1.json").exists():
        g.run(d, quiet=True)
    pages = sorted(d.glob("grid_*.json"), key=lambda p: int(re.sub(r"\D", "", p.stem)))
    text = "\n\n".join(g.describe(json.loads(p.read_text(encoding="utf-8")), i, len(pages) > 1) for i, p in enumerate(pages, 1))
    (d / "grid.txt").write_text(text + "\n", encoding="utf-8")
    return text


def prepare_views(state: dict, kind: str, check: dict | None) -> list[str]:
    """보기 창 네 장을 이번 회차에 맞게 새로 쓴다. 무엇을 띄웠는지 글 목록."""
    d = draft_dir(state["id"])
    v = _skill("view")
    shown = []

    def put(n, args, what):
        try:
            v.main([args[0], str(d), *args[1:], "--to", str(n)])
            shown.append(f"view_{n}.png: {what}")
        except SystemExit as e:
            _blank(d / f"view_{n}.png", f"view_{n}: (empty) {e}")
            shown.append(f"view_{n}.png: 빈 창")

    pages = len(state["sources"])
    if kind == "build":
        put(1, ["page"], "원본 1쪽 전체 + 칸 이름")
        for n in range(2, VIEWS + 1):
            if n <= pages:
                put(n, ["page", "--page", str(n)], f"원본 {n}쪽 전체 + 칸 이름")
            else:
                _blank(d / f"view_{n}.png", f"view_{n}: empty - write with view.py ... --to {n}")
                shown.append(f"view_{n}.png: 빈 창")
        return shown
    imgs = (check or {}).get("images") or {}
    for n, path, what in ((1, (imgs.get("side") or [None])[0], "1쪽 왼쪽 원본 · 오른쪽 렌더(--rows min) 전체"),
                          (2, imgs.get("renders"), "렌더 모음 (min·max·seed1·seed2 첫 쪽) — 값이 바뀌어도 넘치지 않는지")):
        try:
            v.save(Image.open(path).convert("RGB"), d / f"view_{n}.png")
            shown.append(f"view_{n}.png: {what}")
        except (OSError, TypeError, AttributeError, ValueError):
            _blank(d / f"view_{n}.png", f"view_{n}: empty")
            shown.append(f"view_{n}.png: 빈 창")
    h = json.loads((d / "grid_1.json").read_text(encoding="utf-8"))["size"][1] if (d / "grid_1.json").exists() else 1123
    put(3, ["compare", "0", "0", "794", str(h // 2)], "1쪽 위 절반: 원본(위) · 렌더(아래)")
    put(4, ["compare", "0", str(h // 2), "794", str(h)], "1쪽 아래 절반: 원본(위) · 렌더(아래)")
    return shown


def _views(state: dict) -> str:
    d = state["draft"]
    return " ".join(f"@{d}/view_{n}.png" for n in range(1, VIEWS + 1))


TOOLS = [
    "- 도구 (T = {skill}, 자리 단위는 쪽 px: 가로 794):",
    "  · python T/view.py table {d} T2 --rows 1-8 --to 2   표를 크게 + 칸 이름 (글자는 이것으로 읽는다)",
    "  · python T/view.py crop {d} x0 y0 x1 y1 --cells --to 3   아무 곳이나 크게",
    "  · python T/view.py compare {d} x0 y0 x1 y1 --to 4   같은 자리의 원본(위)·렌더(아래)",
    "  · python T/build.py {d}   layout.json → template.html.j2 · form.json · fields.md",
]


def _tools(state: dict) -> list[str]:
    return [t.format(skill=SKILL, d=state["draft"]).replace("T/", f"{SKILL}/") for t in TOOLS]


def build_request(state: dict, n: int, message: str | None = None, shown: list[str] | None = None) -> str:
    """만들기 회차: 보기 창으로 칸을 읽어 layout.json 을 쓰고 build·검사."""
    d = state["draft"]
    lines = [_views(state),
             f"{SKILL}/SKILL.md 를 끝까지 읽고 그 순서(2~5단계)를 따라 docgen 서식을 만들어라. {n}회차 — 만들기다.",
             *_head(state, n),
             f"- 원본은 진행기가 이미 쟀다 (SKILL.md 1단계): {d}/grid.txt 에 쪽마다 표·칸 이름(T2.7)·자리·글자 덩어리(B3) 목록이 있다 — 먼저 읽는다.",
             "- 붙인 그림 네 장은 **보기 창**이다 (지금 보인다): " + "; ".join(shown or []),
             "  보기 창은 view.py 로 다시 쓰면 다음 단계에서 새 그림으로 보인다 (--to 1~4). 붙지 않은 그림 파일은 열어 볼 수 없다.",
             *_tools(state),
             "- 할 일: 표마다 view.py table 로 칸 이름이 찍힌 그림을 크게 보고(6~10행씩), 칸마다 원본 글자를 그대로 · 값 자리는 {키} 로 "
             "초안 폴더의 layout.json 에 적는다 (cells · blocks · fields · lists — 꼴은 SKILL.md 3·4단계). "
             "그다음 build.py, 검사 명령. 검사가 통과하면 끝낸다 (원본과 맞대 보며 고치기는 다음 회차).",
             "- 못 읽은 칸은 짐작하지 않고 crop 으로 더 좁게 본다. 그래도 안 보이면 비워 두고 끝낼 때 적는다."]
    if state["kind"] == "real":
        lines.append("- 실서류다: 손글씨·타자로 채운 값(이름·번호·주소·지점명·날짜)은 절대 옮기지 않고 {키} 로만 적는다.")
    if state.get("note"):
        lines.append(f"- 사람의 추가 요청: {state['note']}")
    if message:
        lines.append(f"- 사람의 지시 (가장 먼저 반영): {message}")
    return "\n".join(lines)


def next_request(state: dict, n: int, check: dict, message: str | None = None, shown: list[str] | None = None) -> str:
    """고치기 회차: 보기 창에 원본|렌더를 띄우고 덩어리마다 맞대 보며 layout.json 을 고친다."""
    d = state["draft"]
    probs = check.get("problems") or []
    warns = check.get("warnings") or []
    lines = [_views(state),
             f"{SKILL}/SKILL.md 를 따르는 서식 만들기의 {n}회차 — 원본과 맞대 보며 고치기다 (SKILL.md 6단계). 새 대화라 앞 회차의 대화는 없다 — "
             f"SKILL.md 와 {d}/layout.json, {d}/grid.txt 를 먼저 읽어라.",
             *_head(state, n),
             "- 붙인 그림 네 장은 **보기 창**이다 (지금 보인다): " + "; ".join(shown or []),
             "  보기 창은 view.py 로 다시 쓰면 다음 단계에서 새 그림으로 보인다 (--to 1~4). 붙지 않은 그림 파일은 열어 볼 수 없다.",
             *_tools(state),
             f"- 직전 검사: {'통과' if check.get('passed') else '통과 못 함'}"]
    lines += [f"  · 문제: {p}" for p in probs[:12]]
    lines += [f"  · 경고: {w}" for w in warns[:14]]
    sample = sample_values(check)
    if sample:
        lines.append("- 렌더 값 예시 (키: seed 1 값 / seed 2 값) — 값이 칸의 뜻에 맞는지 본다:")
        lines += [f"  · {line}" for line in sample]
    if message:
        lines.append(f"- 사람의 지시 (가장 먼저 반영): {message}")
    lines.append("- 할 일: 문제·경고에 나온 칸부터, 그다음 표·덩어리마다 view.py compare 로 원본과 렌더를 같은 자리끼리 크게 보고 "
                 "다른 곳을 layout.json 에서 고친다 (글자·size·align·\\n·{키}·fields 의 source). template.html.j2 는 직접 고치지 않는다. "
                 "고친 뒤 build.py → 검사 명령. 끝나면 SKILL.md 7단계 보고를 초안 폴더의 report.md 로 쓴다 (있으면 고쳐 쓴다).")
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
    """이번 회차의 요청: 초안 폴더에 무엇이 있는지로 고르고, 보기 창을 그에 맞게 새로 쓴다."""
    kind = round_kind(state)
    measure(state)
    shown = prepare_views(state, kind, check)
    if kind == "build":
        return build_request(state, n, message, shown)
    return next_request(state, n, check or {}, message, shown)


def first_request(state: dict) -> str:
    """처음 회차의 요청 (만들기)."""
    return round_request(state, 1, None)


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
    for p in relab_procs():                    # 진행기가 끊겨 relab_pid 가 옛것이어도, 이 서식의 relab 은 모두
        if p["form_id"] == form_id:
            kill_relab_quiet(p["pid"])
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
    if state.get("status") in ("running", "installing") and _alive(state.get("runner_pid")):
        raise AgentError("도는 중입니다. 멈춘 뒤에 지우세요")
    if d.resolve().parent != DRAFTS.resolve():
        raise AgentError(f"초안 폴더가 아닙니다: {d}")
    for p in relab_procs():                    # 진행기는 끊겼는데 relab 만 남았으면 같이 끈다 (지운 뒤 다른 서식을 건드리지 않게)
        if p["form_id"] == form_id:
            kill_relab_quiet(p["pid"])
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
    cleaned = []
    for p in relab_procs():                    # 한 번에 한 건: 진행기가 죽고 남은 relab 은 다른 서식을 건드릴 수 있어 끈다
        if p["runner_alive"] and p["form_id"] != form_id:
            continue                           # 다른 서식이 정말 도는 중 (명령줄로 따로 띄운 것) — 건드리지 않는다
        if kill_relab_quiet(p["pid"]):
            cleaned.append(p)
            log(f"[{form_id}] 남아 있던 relab 실행을 끔: pid {p['pid']} ({p['form_id'] or '서식 모름'}, {p['started']} 시작)")
    py = execution_python(st)
    if not Path(py).is_file():
        state.update(status="failed", error=f"명령 실행 python 이 없습니다: {py} (studio 설정 form_agent.python)")
        save(state)
        raise AgentError(state["error"])
    state.update(status="running", runner_pid=os.getpid(), relab=relab, relab_version=R.VERSION, python=py)
    if cleaned:
        state.setdefault("cleaned", []).extend({**p, "at": now()} for p in cleaned)
    save(state)
    stopped = lambda: (d / "STOP").exists()  # noqa: E731
    first = not state["rounds"]
    planned = (1 + fix_rounds) if first else max(1, fix_rounds)     # 처음: 만들기 + 고치기 회차
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
        code = R.run(cmd, d / rnd["log"], ROOT, float(st.get("round_minutes", 60)), on_start=remember, stopped=stopped,
                     env_extra={"RELAB_PRIVATE_HOME": str(d / RECORDS), "RELAB_EXECUTION_PYTHON": py})
        rnd.update(exit=code, ended=now(), seconds=round(time.time() - t0))
        state["relab_pid"] = None
        if code is None:
            state["status"] = "stopped" if stopped() else "failed"
            state["error"] = "멈춤" if stopped() else "회차 시간 한도를 넘음"
            break
        if code == 2:
            state.update(status="failed", error="ReLab 이 시작하지 못함 (종료 코드 2) — " + tail(d / rnd["log"]))
            break
        if not (d / "template.html.j2").exists() and (d / "layout.json").exists():   # 모델이 build 를 안 돌렸으면 진행기가
            try:
                _skill("build").build(d)
            except Exception as e:                                                  # noqa: BLE001 — 오류는 다음 요청의 검사 문제로 간다
                log(f"[{form_id}] build.py 오류: {e}")
        if not (d / "layout.json").exists():
            last_check = None
            rnd["read"] = {"layout": False}
            log(f"[{form_id}] {n}회차 끝: 종료 코드 {code}, layout.json 없음 — 다음 회차에 다시 만든다")
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
