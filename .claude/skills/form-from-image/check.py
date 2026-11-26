"""초안 서식 검사 한 번에 (form-from-image 스킬 4·5단계).

    python .claude/skills/form-from-image/check.py <초안 폴더> [--out <폴더>] [--seeds 1 2 3]
    python -m pytest .claude/skills/form-from-image/test_draft.py --draft <초안 폴더> -q     (같은 검사, pytest 로)

하는 일:
  1. 미리보기 5번: --rows min · --rows max · seed 1~3  (python -m docgen.preview --dir …)
  2. 통과 판정 (problems — 하나라도 있으면 통과 못 함):
     필요한 파일(source_text.md · fields.md · template.html.j2 · form.json), 명령 오류, checks, overflow,
     쪽 수(min 렌더 = 원본 그림 수), 템플릿에서 값을 {{ d.… }} 로 직접 찍은 곳
  3. 정답 값 경고 (warnings — 통과는 막지 않음, 사람·모델이 판단):
     다른 칸에 같은 사람 값(대리인 전화 = 고객 전화 …), 한 서류 안 날짜·금액 표기 섞임, 빈 값이 절반 넘음,
     원본 글자 대조: 템플릿 글자 중 source_text.md 에 없는 것(지어냈을 수 있음) · source_text.md 글자 중 템플릿에 없는 것(빠짐)
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
import unicodedata
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from PIL import Image, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]                      # 저장소 맨 위 (document_gen/)
sys.path.insert(0, str(HERE))
import compare  # noqa: E402  (같은 폴더의 비교 그림 도구)

REQUIRED = ("source_text.md", "fields.md", "template.html.j2", "form.json")
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


# ---------------------------------------------------------------- 원본 글자 대조 (source_text.md ↔ 템플릿)

JINJA = re.compile(r"\{\{.*?\}\}|\{%.*?%\}|\{#.*?#\}", re.S)
STRINGS = re.compile(r"\"([^\"]*)\"|'([^']*)'")
MARK = re.compile(r"^\((값|안 ?보임|로고|바코드|도장|서명|그림|빈 ?칸)[^)]*\)$")
SPLIT = re.compile(r"\s*\|\s*|\s{3,}|\s+/\s+")


def norm(s: str) -> str:
    """대조용: 글자·숫자만, 대문자로 (띄어쓰기·기호·괄호 차이는 무시)."""
    s = unicodedata.normalize("NFKC", s).upper()
    return "".join(ch for ch in s if ch.isalnum())


def printed_text(template: str) -> list[str]:
    """템플릿에서 그림에 인쇄되는 글자 덩어리: 태그·jinja 밖 글자 + m.title 글자 + 체크 보기 글자."""
    chunks = []
    body = re.sub(r"<style.*?</style>|<script.*?</script>|<!--.*?-->|\{%-?\s*block\s+(style|head)\s*-?%\}.*?\{%-?\s*endblock",
                  " ", template, flags=re.S | re.I)
    for block in re.findall(r"\{\{(.*?)\}\}", body, re.S):
        if re.match(r"\s*m\.title\(", block):
            chunks += [a or b for a, b in STRINGS.findall(block)]
        elif re.match(r"\s*m\.(choice|agree)\(", block):
            for lst in re.findall(r"\[(.*?)\]", block, re.S):
                chunks += [a or b for a, b in STRINGS.findall(lst)]
    text = JINJA.sub("\n", body)
    text = re.sub(r"<[^>]+>", "\n", text)
    text = re.sub(r"&nbsp;|&#160;", " ", text)
    text = re.sub(r"&[a-z]+;|&#\d+;", "", text)
    chunks += [c.strip() for c in text.splitlines()]
    return [c for c in chunks if len(norm(c)) >= 2]


def source_items(md: str) -> list[str]:
    """source_text.md 의 칸 글자: 제목줄(#) 빼고, 줄을 | 로 나눈 것. (값)·(안 보임 …)·(로고 …) 표시는 뺀다."""
    items = []
    for line in md.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        line = re.sub(r"^[-*>]\s+", "", line)
        for part in SPLIT.split(line):
            part = re.sub(r"\((값|안 ?보임|로고|바코드|도장|서명|그림)[^)]*\)", " ", part).strip()
            if len(norm(part)) >= 2 and not MARK.match(part):
                items.append(part)
    return items


def covered(piece: str, whole: str, whole_bigrams: set) -> bool:
    """piece 가 whole 에 있나. 짧으면 그대로 들어 있어야, 길면(문장) 두 글자 묶음 80% 이상."""
    p = norm(piece)
    if p in whole:
        return True
    if len(p) < 8:                     # 짧은 것: 띄어 쓴 낱말(두 글자 이상)이 모두 있으면 (사이에 값이 끼는 "년 월 일" 같은 줄)
        words = [w for w in (norm(x) for x in piece.split()) if len(w) >= 2]
        return all(w in whole for w in words) and (len(words) > 1 or not words)
    grams = [p[i:i + 2] for i in range(len(p) - 1)]
    return sum(g in whole_bigrams for g in grams) / len(grams) >= 0.8


def text_warnings(draft: Path) -> list[str]:
    """원본 글자(source_text.md)와 템플릿 글자를 맞대 본다. 경고 글 목록."""
    src_file, tpl_file = draft / "source_text.md", draft / "template.html.j2"
    if not (src_file.exists() and tpl_file.exists()):
        return []
    md = src_file.read_text(encoding="utf-8")
    src_items = source_items(md)
    tpl_items = printed_text(tpl_file.read_text(encoding="utf-8"))
    heads = [line.lstrip("#").strip() for line in md.splitlines() if line.startswith("###")]   # 덩어리 이름도 원본 글자일 수 있다
    src_all, tpl_all = norm(" ".join(src_items + heads)), norm(" ".join(tpl_items))
    bigrams = lambda s: {s[i:i + 2] for i in range(len(s) - 1)}  # noqa: E731
    src_bi, tpl_bi = bigrams(src_all), bigrams(tpl_all)
    extra = list(dict.fromkeys(c for c in tpl_items if not covered(c, src_all, src_bi)))
    missing = list(dict.fromkeys(c for c in src_items if not covered(c, tpl_all, tpl_bi)))
    out = []
    if extra:
        out.append(f"원본 글자(source_text.md)에 없는 글자가 템플릿에 {len(extra)}곳: "
                   + ", ".join(repr(c[:30]) for c in extra[:10])
                   + " — 그림에 정말 있으면 source_text.md 에 더하고, 없으면 템플릿에서 뺀다 (지어낸 항목명)")
    if missing:
        out.append(f"원본 글자 중 템플릿에 없는 것 {len(missing)}곳: "
                   + ", ".join(repr(c[:30]) for c in missing[:10])
                   + " — 템플릿에 옮긴다 (항목명·안내문 빠짐)")
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
    warnings += text_warnings(draft)
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
