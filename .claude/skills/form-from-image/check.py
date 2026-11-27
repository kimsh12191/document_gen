"""초안 서식 검사 한 번에 (form-from-image 스킬 5단계).

    python .claude/skills/form-from-image/check.py <초안 폴더> [--out <폴더>] [--seeds 1 2 3]
    python -m pytest .claude/skills/form-from-image/test_draft.py --draft <초안 폴더> -q     (같은 검사, pytest 로)

하는 일:
  1. 미리보기 5번: --rows min · --rows max · seed 1~3  (python -m docgen.preview --dir …). seed 1 쪽 그림을 render_<n>.png 로 둔다 (view.py compare)
  2. 통과 판정 (problems — 하나라도 있으면 통과 못 함):
     필요한 파일(layout.json · template.html.j2 · form.json · fields.md · grid_<n>.json), 명령 오류, checks, overflow,
     쪽 수(min 렌더 = 원본 그림 수), 템플릿에서 값을 {{ d.… }} 로 직접 찍은 곳
  3. 경고 (warnings — 통과는 막지 않음, 고치거나 왜 아닌지 적는다):
     layout.json 에 글자를 안 적은 칸·글자 덩어리, 모양 대조(원본 grid ↔ 렌더를 같은 방법으로 잰 것: 표 선 자리, 칸 글자 있음/없음,
     칸 가장자리에 닿은 글자 = 넘침, 글자 덩어리 너비), 값이 칸 밖으로 나감, 값 경고(같은 사람 값·날짜/금액 표기 섞임·빈 값)
  4. 그림: side_<쪽>.jpg (왼쪽 원본 · 오른쪽 min 렌더), renders.jpg (min·max·seed 1·2 첫 쪽 모음). 한 장 2MB 이하
  5. <out>/check.json, 마지막 줄에 요약 JSON. 통과면 종료 코드 0, 아니면 1

원본 그림은 초안 폴더의 source.png, source_2.png … (쪽 순서). grid.py 가 만든 page_<n>.png · grid_<n>.json 과 맞댄다.
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
import grid  # noqa: E402

REQUIRED = ("layout.json", "template.html.j2", "form.json", "fields.md")
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
        sc = label.get("scale") or 1
        info["label_fields"] = [{"key": f["key"], "page": f.get("page", 0), "bbox": [v / sc for v in f["bbox"]]}
                                for f in label.get("fields", []) if f.get("bbox")]
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


# ---------------------------------------------------------------- 모양 대조 (원본 grid ↔ 렌더를 같은 방법으로 잰 것)

TOKEN = re.compile(r"\{[^{}]+\}")
SHOW = 12                                    # 경고 한 줄에 보여 줄 칸 수
NEAR = 3                                     # 같은 선으로 볼 거리 (쪽 px)


def load_layout(draft: Path) -> dict:
    try:
        return json.loads((draft / "layout.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def item_text(v) -> str:
    if isinstance(v, dict):
        return v.get("t") or ""
    return v or ""


def grids(draft: Path) -> list[dict]:
    out = []
    for p in sorted(draft.glob("grid_*.json"), key=lambda p: int(re.sub(r"\D", "", p.stem))):
        out.append(json.loads(p.read_text(encoding="utf-8")))
    return out


def few(items: list[str]) -> str:
    return ", ".join(items[:SHOW]) + (f" 외 {len(items) - SHOW}" if len(items) > SHOW else "")


def coverage_warnings(draft: Path, layout: dict, gs: list[dict]) -> list[str]:
    """원본에 글자가 있는데 layout.json 에 안 적은 칸·글자 덩어리."""
    out = []
    pages = layout.get("pages") or []
    for n, g in enumerate(gs, 1):
        pg = pages[n - 1] if n - 1 < len(pages) else {}
        cells, blocks, skip = pg.get("cells") or {}, pg.get("blocks") or {}, set(pg.get("skip") or [])
        cells = {k.split(":")[-1]: v for k, v in cells.items()}
        empty = [c["id"] for t in g["tables"] if t["id"] not in skip for c in t["cells"] if c.get("ink") and c["id"] not in cells]
        if empty:
            out.append(f"{n}쪽: 원본에 글자가 있는데 layout.json cells 에 없는 칸 {len(empty)}개: {few(empty)} "
                       f"— view.py table 로 보고 글자(값이면 {{키}})를 적는다")
        loose = [b["id"] for b in g["blocks"] if b["id"] not in blocks and b["id"] not in skip]
        if loose:
            out.append(f"{n}쪽: layout.json blocks 에 없는 글자 덩어리 {len(loose)}개: {few(loose)} "
                       f"— view.py crop --cells 로 보고 글자를 적거나, 그리지 않을 것(티끌·바코드)은 null")
    return out


def match_box(box, cands, key="box"):
    best, score = None, 0.0
    for c in cands:
        b = c[key]
        ix = max(0, min(box[2], b[2]) - max(box[0], b[0]))
        iy = max(0, min(box[3], b[3]) - max(box[1], b[1]))
        inter = ix * iy
        union = (box[2] - box[0]) * (box[3] - box[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
        if union > 0 and inter / union > score:
            best, score = c, inter / union
    return best, score


def edge_ink(im: Image.Image, box) -> bool:
    """렌더 칸 안쪽 가장자리(왼·오른 1.5쪽px)에 글자가 닿았나 — overflow:hidden 으로 잘린 글자."""
    S = grid.S
    x0, y0, x1, y1 = (int(round(v * S)) for v in box)
    inset = 3                      # 선 가운데에서 1.5쪽px: 선은 grid.erase_lines 로 지워졌고, 잘린 글자만 여기까지 닿는다
    crop = im.crop((x0 + inset, y0 + inset, x1 - inset, y1 - inset))
    if crop.size[0] < 8 or crop.size[1] < 4:
        return False
    w = crop.size[0]
    edge = 4                       # 바른 글자는 칸 안쪽 여백(4px = 8) 밖에서 시작
    left = crop.crop((0, 0, edge, crop.size[1])).getbbox()
    right = crop.crop((w - edge, 0, w, crop.size[1])).getbbox()
    return bool(left or right)


def overlaps(a, b) -> bool:
    return min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1])


def shape_warnings(draft: Path, layout: dict, gs: list[dict], pages: list[str], values: dict | None) -> list[str]:
    """seed 1 렌더를 grid 로 재서 원본과 맞댄다. 도장·서명이 걸친 칸은 글자 대조에서 뺀다 (도장은 칸 밖으로 번지는 게 정상)."""
    out = []
    marks = [(f.get("page", 0), f["bbox"]) for f in values or [] if f.get("bbox") and f["key"].startswith(("seal.", "sign.", "signature."))]
    lp = layout.get("pages") or []
    for n, (g, ren_path) in enumerate(zip(gs, pages), 1):
        pg = lp[n - 1] if n - 1 < len(lp) else {}
        cells = {k.split(":")[-1]: v for k, v in (pg.get("cells") or {}).items()}
        skip = set(pg.get("skip") or [])
        ren = Image.open(ren_path).convert("L")
        if ren.size[0] != grid.WORK_W:
            ren = ren.resize((grid.WORK_W, round(ren.size[1] * grid.WORK_W / ren.size[0])))
        rg = grid.measure(ren)
        rbin = grid.erase_lines(grid.binary(ren), *[[{"pos": l[0] * grid.S, "a": l[1] * grid.S, "b": l[2] * grid.S, "thick": 3}
                                                     for l in rg["raw"][k]] for k in ("h", "v")])
        lines_off, missing_tables, cells_bad, gone, extra, clipped = [], [], [], [], [], []
        for t in g["tables"]:
            if t["id"] in skip:
                continue
            rt, iou = match_box(t["box"], rg["tables"])
            if not rt or iou < 0.5:
                missing_tables.append(f"{t['id']} (x {t['box'][0]}~{t['box'][2]} y {t['box'][1]}~{t['box'][3]})")
                continue
            dx = [x for x in t["xs"] if min(abs(x - r) for r in rt["xs"]) > NEAR]
            dy = [y for y in t["ys"] if min(abs(y - r) for r in rt["ys"]) > NEAR]
            ex = [x for x in rt["xs"] if min(abs(x - s) for s in t["xs"]) > NEAR]
            ey = [y for y in rt["ys"] if min(abs(y - s) for s in t["ys"]) > NEAR]
            if dx or dy or ex or ey:
                lines_off.append(f"{t['id']}: " + "; ".join(x for x in (
                    f"원본 세로선 x {dx} 이 렌더에 없음" if dx else "", f"원본 가로선 y {dy} 이 렌더에 없음" if dy else "",
                    f"렌더에만 세로선 x {ex}" if ex else "", f"렌더에만 가로선 y {ey}" if ey else "") if x))
            elif len(rt["cells"]) != len(t["cells"]):
                cells_bad.append(f"{t['id']} 칸 수 원본 {len(t['cells'])} · 렌더 {len(rt['cells'])}")
            for c in t["cells"]:
                if any(p == n - 1 and overlaps(b, c["box"]) for p, b in marks):
                    continue
                text = item_text(cells.get(c["id"]))
                fixed = text and not TOKEN.search(text)
                rk = grid.ink(rbin, [v * grid.S for v in c["box"]])
                if c.get("ink") and fixed and not rk:
                    gone.append(c["id"])
                if not c.get("ink") and rk and not text:
                    extra.append(c["id"])
                if rk and edge_ink(rbin, c["box"]):
                    clipped.append(c["id"])
        if missing_tables:
            out.append(f"{n}쪽: 렌더에서 원본 표를 못 찾음: {few(missing_tables)} — view.py compare 로 그 자리를 본다")
        if lines_off:
            out.append(f"{n}쪽 표 선이 원본과 다름: " + " | ".join(lines_off[:6]))
        if cells_bad:
            out.append(f"{n}쪽: " + ", ".join(cells_bad))
        if gone:
            out.append(f"{n}쪽: 원본엔 글자가 있는데 렌더 칸이 비었음: {few(gone)}")
        if extra:
            out.append(f"{n}쪽: 원본엔 빈 칸인데 렌더에 글자가 있음: {few(extra)}")
        if clipped:
            out.append(f"{n}쪽: 글자가 칸 가장자리에 닿음(넘쳐 잘림): {few(clipped)} — 그 칸 size 를 줄이거나 \\n 으로 줄을 나눈다")
        # 글자 덩어리: 원본 자리 근처의 렌더 덩어리 너비
        blocks = pg.get("blocks") or {}
        wide, lost = [], []
        for bl in g["blocks"]:
            text = item_text(blocks.get(bl["id"]))
            if bl["id"] in skip or not text:
                continue
            x0, y0, x1, y1 = (int(v * grid.S) for v in bl["box"])
            if rbin.crop((x0, y0, x1 + 1, y1 + 1)).getbbox() is None:
                lost.append(bl["id"])
                continue
            if TOKEN.search(text) or any(p == n - 1 and overlaps(b, bl["box"]) for p, b in marks):
                continue                                   # 값·도장이 섞인 덩어리는 너비가 서류마다 다르다
            b = bl["box"]
            if b[2] - b[0] < 40:                           # 한두 글자: 너비 차이가 늘 크게 보인다
                continue
            grow = [b[0] - 0.3 * (b[2] - b[0]), b[1] - 2, b[2] + 0.3 * (b[2] - b[0]), b[3] + 2]
            parts = [r["box"] for r in rg["blocks"] if grow[0] <= (r["box"][0] + r["box"][2]) / 2 <= grow[2]
                     and overlaps(r["box"], [0, b[1], 9999, b[3]])]
            if not parts:
                continue
            sw, rw = b[2] - b[0], max(p[2] for p in parts) - min(p[0] for p in parts)     # 렌더에서 낱말 사이가 벌어져 둘로 잡혀도 합쳐 잰다
            if rw > sw * 1.15 + 6 or rw < sw * 0.85 - 6:
                wide.append(f"{bl['id']} 원본 {sw}px · 렌더 {rw}px")
        if lost:
            out.append(f"{n}쪽: 원본 글자 덩어리 자리에 렌더 글자가 없음: {few(lost)}")
        if wide:
            out.append(f"{n}쪽: 글자 덩어리 너비가 다름 (size·띄어쓰기·bold 확인): {few(wide)}")
    # 값이 칸 밖으로
    if values:
        boxes = [(n, c) for n, g in enumerate(gs) for t in g["tables"] for c in t["cells"]]
        over = []
        for f in values:
            b, page = f.get("bbox"), f.get("page", 0)
            if not b or f["key"].startswith(("seal.", "sign.", "signature.")):
                continue
            cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
            for n, c in boxes:
                cb = c["box"]
                if n == page and cb[0] <= cx <= cb[2] and cb[1] <= cy <= cb[3]:
                    if b[0] < cb[0] - 2 or b[2] > cb[2] + 2 or b[1] < cb[1] - 2 or b[3] > cb[3] + 2:
                        over.append(f"{f['key']}({c['id']})")
                    break
        if over:
            out.append(f"값이 칸 밖으로 나감 (seed 1): {few(over)} — 그 칸 size 를 줄이거나 값 source 를 짧은 것으로")
    return out


def save_renders(draft: Path, info: dict | None = None) -> list[Path]:
    """seed 1 렌더 쪽 그림을 초안 폴더 render_<n>.png 로 (view.py compare·overlay 가 쓴다)."""
    if info is None:
        info = preview(draft, draft / "check" / "render_s1", ["--seed", "1"])
    out = []
    for i, p in enumerate(info.get("image_paths") or [], 1):
        dest = draft / f"render_{i}.png"
        Image.open(p).save(dest)
        out.append(dest)
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
            problems.append(f"{name} 이 없습니다" + (" (build.py 로 만든다)" if name != "layout.json" else ""))
    srcs = sources(draft)
    if not srcs:
        problems.append("원본 그림 source.png 가 없습니다")
    gs = grids(draft)
    if srcs and len(gs) != len(srcs):
        problems.append(f"grid_<n>.json 이 {len(gs)}개, 원본은 {len(srcs)}쪽 — grid.py 를 먼저 돌린다")
    layout = load_layout(draft)
    if layout and gs:
        warnings += coverage_warnings(draft, layout, gs)
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
    s1 = renders.get("s1") or {}
    if s1.get("image_paths"):
        save_renders(draft, s1)
        if layout and gs and len(gs) == len(s1["image_paths"]):
            warnings += shape_warnings(draft, layout, gs, s1["image_paths"], s1.get("label_fields"))
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
