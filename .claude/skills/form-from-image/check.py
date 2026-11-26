"""초안 서식 검사 한 번에 (form-from-image 스킬 4·5단계).

    python .claude/skills/form-from-image/check.py <초안 폴더> [--out <폴더>] [--seeds 1 2 3]
    python -m pytest .claude/skills/form-from-image/test_draft.py --draft <초안 폴더> -q     (같은 검사, pytest 로)

하는 일:
  1. 미리보기 5번: --rows min · --rows max · seed 1~3  (python -m docgen.preview --dir …)
  2. 통과 판정 (problems — 하나라도 있으면 통과 못 함):
     필요한 파일(fields.md · template.html.j2 · form.json), 명령 오류, checks, overflow,
     쪽 수(min 렌더 = 원본 그림 수), 템플릿에서 값을 {{ d.… }} 로 직접 찍은 곳
  3. 정답 값 경고 (warnings — 통과는 막지 않음, 사람·모델이 판단):
     다른 칸에 같은 사람 값(대리인 전화 = 고객 전화 …), 한 서류 안 날짜·금액 표기 섞임, 빈 값이 절반 넘음
  4. 그림: side_<쪽>.jpg (왼쪽 원본 · 오른쪽 min 렌더), renders.jpg (min·max·seed 1·2 첫 쪽 모음). 한 장 2MB 이하
  5. <out>/check.json, 마지막 줄에 요약 JSON. 통과면 종료 코드 0, 아니면 1

원본 그림은 초안 폴더의 source.png, source_2.png … (쪽 순서).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]                      # 저장소 맨 위 (document_gen/)
sys.path.insert(0, str(HERE))
import compare  # noqa: E402  (같은 폴더의 비교 그림 도구)

REQUIRED = ("fields.md", "template.html.j2", "form.json")
DIRECT = re.compile(r"\{\{-?\s*d\.[\w.\[\]'\"]+")          # {{ d.x }} — 그림엔 나오지만 정답에서 빠짐
PERSON_PARTS = {"name", "phone", "mobile", "address", "email", "birth", "rrn"}
DATE_STYLES = (("dot", re.compile(r"^\d{4}\.\d{1,2}\.\d{1,2}$")), ("dash", re.compile(r"^\d{4}-\d{1,2}-\d{1,2}$")),
               ("slash", re.compile(r"^\d{4}/\d{1,2}/\d{1,2}$")), ("kor", re.compile(r"^\d{4}년\s*\d{1,2}월\s*\d{1,2}일$")))
THUMB = 700                                  # 렌더 모음의 한 칸 가로
TIMEOUT = 300


def sources(draft: Path) -> list[Path]:
    """원본 그림: source.png, source_2.png … (쪽 순서)."""
    first = draft / "source.png"
    rest = sorted(draft.glob("source_*.png"), key=lambda p: int(re.sub(r"\D", "", p.stem) or 0))
    return ([first] if first.exists() else []) + rest


ENV_FILE = ROOT / "out" / "form_drafts" / ".formagent_env.json"     # formagent 진행기가 ReLab 을 돌리기 전에 남긴 환경
BROWSER_ROOTS = ("/opt/ms-playwright", "/opt/pw-browsers", "~/.cache/ms-playwright")
BROWSER_HINT = (" — 렌더링 브라우저를 못 찾음. 설치(playwright install·pip)하지 말고 멈추고 보고한다 "
                "(에이전트 도구가 환경 변수 PLAYWRIGHT_BROWSERS_PATH 를 넘기지 않았을 수 있음: out/form_drafts/.formagent_env.json)")


def child_env() -> dict:
    """미리보기에 넘길 환경. ReLab 같은 에이전트는 검사 명령에 환경 변수를 몇 개만 넘겨 브라우저 위치(PLAYWRIGHT_BROWSERS_PATH)가
    빠진다. 진행기가 남긴 .formagent_env.json 으로 채우고, 그래도 없으면 흔한 설치 자리를 찾는다."""
    env = dict(os.environ)
    try:
        for k, v in json.loads(ENV_FILE.read_text(encoding="utf-8")).items():
            if v and not env.get(k):
                env[k] = v
    except (OSError, ValueError):
        pass
    if not env.get("PLAYWRIGHT_BROWSERS_PATH"):
        for root in BROWSER_ROOTS:
            r = Path(root).expanduser()
            if r.is_dir() and any(r.glob("chromium*")):
                env["PLAYWRIGHT_BROWSERS_PATH"] = str(r)
                break
    return env


def preview(draft: Path, out: Path, args: list[str]) -> dict:
    """미리보기 한 번. 마지막 줄 JSON + label.json."""
    cmd = [sys.executable, "-m", "docgen.preview", "--dir", str(draft), *args, "--out", str(out)]
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=TIMEOUT, env=child_env())
    except subprocess.TimeoutExpired:
        return {"error": f"{TIMEOUT}초 안에 끝나지 않음", "args": args}
    lines = [line for line in p.stdout.strip().splitlines() if line.startswith("{")]
    if p.returncode != 0 or not lines:
        tail = "\n".join((p.stderr or p.stdout).strip().splitlines()[-8:])
        hint = BROWSER_HINT if re.search(r"Executable doesn't exist|playwright install|BrowserType\.launch", p.stderr + p.stdout) else ""
        return {"error": f"종료 코드 {p.returncode}: {tail}{hint}", "args": args}
    info = json.loads(lines[-1])
    labels = sorted(out.rglob("label.json"), key=lambda f: f.stat().st_mtime)
    if labels:
        label = json.loads(labels[-1].read_text(encoding="utf-8"))
        info["values"] = {f["key"]: f.get("value") for f in label.get("fields", [])}
        info["types"] = {f["key"]: f.get("type") for f in label.get("fields", [])}
        info["image_paths"] = [str(p) for p in compare.page_images(labels[-1], label, out)]
    return info


def value_warnings(info: dict) -> dict[str, str]:
    """정답 값에서 기계로 잡을 수 있는 것 (경고). {묶는 이름: 글}."""
    values, types, out = info.get("values") or {}, info.get("types") or {}, {}
    by_value = defaultdict(set)
    for key, value in values.items():
        parts = key.split(".")
        if value and len(parts) >= 2 and parts[-1] in PERSON_PARTS and not parts[-2].isdigit():
            by_value[(parts[-1], str(value))].add(key)
    for (part, value), keys in sorted(by_value.items()):
        if len({k.split(".")[0] for k in keys}) > 1:
            same = " = ".join(sorted(keys))
            out[f"same:{same}"] = f"다른 칸에 같은 값: {same} (예: {value!r}) — 다른 사람 칸이면 source 를 바꾼다, 같은 사람이면 무시"
    styles = defaultdict(list)
    for key, value in values.items():
        if not value:
            continue
        if types.get(key) == "date" or key.split(".")[-1] in ("birth", "date") or key.endswith("_date"):
            for style, rx in DATE_STYLES:
                if rx.match(str(value)):
                    styles[style].append(key)
    if len(styles) > 1:
        out["date"] = "한 서류 안 날짜 표기가 섞임 (예: " + ", ".join(f"{s} {v[:3]}" for s, v in styles.items()) + ") — generate.py 의 date_like 로 맞춘다"
    amounts = [(k, str(v)) for k, v in values.items() if v and types.get(k) == "amount"]
    won = [k for k, v in amounts if v.endswith("원")]
    if won and len(won) < len(amounts):
        out["amount"] = f"한 서류 안 금액 표기가 섞임 (예: '원' 붙음 {won[:3]}) — generate.py 의 amount_like 로 맞춘다"
    if info.get("fields") and info.get("empty", 0) > info["fields"] / 2:
        out["empty"] = f"값 {info['fields']}개 중 {info['empty']}개가 빈 칸"
    return out


def pictures(srcs: list[Path], renders: dict, out: Path) -> dict:
    """side_<쪽>.jpg (원본|min 렌더), renders.jpg (렌더 첫 쪽 모음)."""
    made = {"side": [], "renders": None}
    pages = renders.get("min", {}).get("image_paths") or []
    for i, (src_path, ren_path) in enumerate(zip(srcs, pages)):
        ren = Image.open(ren_path).convert("RGB")
        src = ImageOps.exif_transpose(Image.open(src_path)).convert("RGB").resize(ren.size)
        side = out / f"side_{i}.jpg"
        compare.side_by_side(src, ren).save(side, quality=85)
        made["side"].append(str(side))
    firsts = [(name, (renders.get(name, {}).get("image_paths") or [None])[0]) for name in ("min", "max", "s1", "s2")]
    firsts = [(n, p) for n, p in firsts if p]
    if firsts:
        thumbs = []
        for name, path in firsts:
            im = Image.open(path).convert("RGB")
            im = im.resize((THUMB, round(im.height * THUMB / im.width)))
            compare.ImageDraw.Draw(im).text((8, 8), name, fill=(200, 0, 0))
            thumbs.append(im)
        cols = 2 if len(thumbs) > 1 else 1
        rows = (len(thumbs) + cols - 1) // cols
        h = max(t.height for t in thumbs)
        sheet = Image.new("RGB", (cols * THUMB + (cols - 1) * 12, rows * h + (rows - 1) * 12), "white")
        for k, t in enumerate(thumbs):
            sheet.paste(t, ((k % cols) * (THUMB + 12), (k // cols) * (h + 12)))
        made["renders"] = str(out / "renders.jpg")
        sheet.save(made["renders"], quality=80)
    return made


def run(draft: Path | str, out: Path | str | None = None, seeds: tuple[int, ...] = (1, 2, 3)) -> dict:
    """검사 전부. check.json 을 쓰고 결과 dict 를 돌려준다."""
    draft = Path(draft).resolve()
    out = Path(out).resolve() if out else draft / "check"
    out.mkdir(parents=True, exist_ok=True)
    problems, warnings = [], []
    for name in REQUIRED:
        if not (draft / name).exists():
            problems.append(f"{name} 이 없습니다")
    srcs = sources(draft)
    if not srcs:
        problems.append("원본 그림 source.png 가 없습니다")
    tpl = draft / "template.html.j2"
    if tpl.exists():
        for no, line in enumerate(tpl.read_text(encoding="utf-8").splitlines(), 1):
            if DIRECT.search(line):
                problems.append(f"template.html.j2 {no}번째 줄: 값을 {{{{ d.… }}}} 로 직접 찍음 → f(\"키\", label=…) 로 (정답에서 빠짐)")
    renders, seen, checks = {}, {}, {}
    if (draft / "template.html.j2").exists() and (draft / "form.json").exists():
        jobs = {"min": ["--rows", "min"], "max": ["--rows", "max"], **{f"s{s}": ["--seed", str(s)] for s in seeds}}
        with ThreadPoolExecutor(max_workers=3) as pool:
            done = {name: pool.submit(preview, draft, out / f"render_{name}", args) for name, args in jobs.items()}
        renders = {name: f.result() for name, f in done.items()}
        for name, info in renders.items():
            if "error" in info:
                problems.append(f"미리보기 {name} 실패: {info['error']}")
                continue
            for c in info.get("checks") or []:
                checks.setdefault(c.get("text") if isinstance(c, dict) else str(c), []).append(name)
            if info.get("overflow"):
                problems.append(f"미리보기 {name}: overflow (한 쪽보다 큰 덩어리)")
            for tag, text in value_warnings(info).items():
                seen.setdefault(tag, [text, []])[1].append(name)
        problems += [f"미리보기 checks: {text} [렌더 {', '.join(names)}]" for text, names in checks.items()]
        warnings += [f"{text} [렌더 {len(names)}/{len(renders)}: {', '.join(names)}]" for text, names in seen.values()]
        mn = renders.get("min", {})
        if "pages" in mn and srcs and mn["pages"] != len(srcs):
            problems.append(f"쪽 수: 원본 {len(srcs)}쪽인데 --rows min 렌더 {mn['pages']}쪽")
    images = pictures(srcs, renders, out) if renders.get("min", {}).get("image_paths") and srcs else {"side": [], "renders": None}
    problems = list(dict.fromkeys(problems))
    result = {
        "passed": not problems, "draft": str(draft), "problems": problems, "warnings": list(dict.fromkeys(warnings)),
        "renders": {n: {k: i.get(k) for k in ("pages", "fields", "empty", "overflow", "checks", "error")} for n, i in renders.items()},
        "values": {n: i.get("values") for n, i in renders.items() if i.get("values")},
        "images": images,
    }
    (out / "check.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    return result


def summary(result: dict) -> dict:
    return {"passed": result["passed"], "problems": result["problems"][:10], "warnings": result["warnings"][:10],
            "renders": {n: {k: v for k, v in r.items() if v not in (None, [])} for n, r in result["renders"].items()},
            "images": result["images"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("draft")
    ap.add_argument("--out", help="결과 폴더 (기본: <초안>/check)")
    ap.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3])
    a = ap.parse_args()
    result = run(a.draft, a.out, tuple(a.seeds))
    for p in result["problems"]:
        print("문제:", p)
    for w in result["warnings"]:
        print("경고:", w)
    print(json.dumps(summary(result), ensure_ascii=False))
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
