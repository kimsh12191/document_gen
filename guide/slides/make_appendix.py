"""Appendix slides: every example in guide/tasks.md as slides, the data shown in full (long blocks continue
on the next slide, nothing is cut).

  python guide/examples/make_catalog.py ... --dump examples.json
  (upload the images in guide/examples/img/ to the deck; write asset_map.json {"examples/img/x.jpg": "/_blob/<id>"})
  python guide/slides/make_appendix.py --examples examples.json --assets guide/slides/asset_map.json --deck <deck root>/project

Writes <deck>/slides/ax-*.html and appends them (with sections) to <deck>/deck.json.
"""
from __future__ import annotations

import argparse
import html
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "guide" / "examples"))
import make_catalog as C  # noqa: E402  (field dictionaries)

BG, BG2, DARK, BODY, MUTED = "#F6F5F1", "#ECEEF0", "#16202A", "#44505C", "#6B7682"
OCR_C, BANK_C = "#1E5AA8", "#B54A12"
FONT = "font-family:'IBM Plex Sans KR', Arial, sans-serif"
MONO = "font-family:'JetBrains Mono', 'Courier New', monospace"
H_AVAIL = 792 - 140          # inside the margins, under the eyebrow and title
CODE_LH = 31                 # 24px mono, line-height 1.3
COL_W = 816                  # two columns


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def units(ch: str) -> float:
    """Width of one character in 24px mono, in units of a Latin character (~14.4px)."""
    return 1.75 if ord(ch) > 0x2E80 else 1.0


def wrap(text: str, width_px: int, size: int = 24, mono: bool = True) -> list[str]:
    """Break every line so it fits; nothing is dropped."""
    unit = size * (0.6 if mono else 0.55)
    limit = width_px / unit
    out = []
    for line in text.split("\n"):
        cur, w = "", 0.0
        for ch in line:
            u = units(ch) if mono else (1.8 if ord(ch) > 0x2E80 else 1.0)
            if w + u > limit and cur:
                out.append(cur)
                cur, w = "", 0.0
            cur += ch
            w += u
        out.append(cur)
    return out


def section(sid: str, inner: str, color: str, eyebrow: str, title: str, notes: str = "", bg: str = BG) -> str:
    aside = f"<aside>{esc(notes)}</aside>" if notes else ""
    return (f'<section id="{sid}" style="background:{bg};color:{DARK};{FONT};padding:128px 128px 160px;'
            f'display:flex;flex-direction:column;gap:20px">\n'
            f'<p style="font-size:24px;font-weight:600;color:{color}">{esc(eyebrow)}</p>\n'
            f'<h2 style="font-size:44px;font-weight:700;line-height:1.2">{esc(title)}</h2>\n{inner}\n'
            f'<p style="position:absolute;left:128px;bottom:64px;width:1664px;font-size:24px;color:{MUTED}">'
            f'{esc(eyebrow)} · 전체 데이터: guide/tasks.md</p>\n{aside}\n</section>\n')


def code_box(label: str, lines: list[str]) -> str:
    def keep_indent(x: str) -> str:
        n = len(x) - len(x.lstrip(" "))
        return "&#160;" * n + esc(x[n:]).replace("  ", " &#160;") if x else "&#160;"

    body = "<br>".join(keep_indent(x) for x in lines)
    return (f'<div style="display:flex;flex-direction:column;gap:6px">'
            f'<p style="font-size:24px;font-weight:600;color:{DARK}">{esc(label)}</p>'
            f'<p style="{MONO};font-size:24px;line-height:1.3;color:#E6E9EC;background:{DARK};padding:14px 18px;'
            f'border-radius:10px">{body}</p></div>')


def pack_blocks(blocks: list[tuple[str, str]]) -> list[list[list[tuple[str, list[str]]]]]:
    """Blocks -> slides of two columns, filled top to bottom; a block that does not fit in what is left of a
    column fills it and continues ("(계속)") in the next column / slide."""
    box = 34 + 28 + 16  # label + box padding + gap
    slides, cols, col, used = [], [], [], 0

    def next_col():
        nonlocal col, used, cols
        cols.append(col)
        col, used = [], 0
        if len(cols) == 2:
            slides.append(cols)
            cols = []

    for label, text in blocks:
        lines, n = wrap(text, COL_W - 40) or [""], 0
        while lines:
            room = int((H_AVAIL - used - box) // CODE_LH)
            if col and room < min(len(lines), 4):  # too little room left: start the next column
                next_col()
                continue
            take = lines[:max(room, 1)]
            col.append((label + (" (계속)" if n else ""), take))
            used += box + len(take) * CODE_LH
            lines, n = lines[len(take):], n + 1
    if col:
        cols.append(col)
    if cols:
        slides.append(cols)
    return slides


def image_grid(paths: list[str], amap: dict, width: int, height: int) -> str:
    n = len(paths)
    cols = 1 if n == 1 else 2 if n <= 4 else 3 if n <= 9 else 4
    rows = math.ceil(n / cols)
    cw = (width - (cols - 1) * 12) // cols
    ch = min(int(cw * 1.414), (height - (rows - 1) * 12) // rows)
    cells = "".join(f'<img src="{amap[p]}" alt="{esc(Path(p).stem)}" style="width:{cw}px;height:{ch}px;object-fit:contain;'
                    f'background:#FFFFFF;border:1px solid #D5DBE1;border-radius:8px">' for p in paths)
    return (f'<div style="width:{width}px;display:grid;grid-template-columns:repeat({cols}, {cw}px);gap:12px">{cells}</div>')


def example_slides(e: dict, amap: dict, color: str, eyebrow: str, start: int) -> list[tuple[str, str]]:
    out = []
    e["notes"] = [(k, v.replace("`", "")) for k, v in e["notes"]]
    notes = " / ".join(f"{k}: {v}" for k, v in e["notes"])
    blocks = list(e["blocks"])
    # first slide: images on the left; on the right the notes and, when it fits, the first block (the question)
    right_w = 1664 - 760 - 32
    right = "".join(f'<p style="font-size:24px;line-height:1.4;color:{BODY}"><b style="color:{DARK}">{esc(k)}</b> {esc(v)}</p>'
                    for k, v in e["notes"])
    used = sum(len(wrap(f"{k} {v}", right_w, mono=False)) * 34 + 10 for k, v in e["notes"])
    if blocks:
        label, text = blocks[0]
        lines = wrap(text, right_w - 40)
        if used + 34 + 28 + len(lines) * CODE_LH <= H_AVAIL:
            right += code_box(label, lines)
            blocks = blocks[1:]
    inner = (f'<div style="display:flex;flex-direction:row;gap:32px;align-items:start">'
             f'{image_grid(e["images"], amap, 760, H_AVAIL)}'
             f'<div style="width:{right_w}px;display:flex;flex-direction:column;gap:14px">{right}</div></div>')
    title = f'{e["no"]} {e["title"]}'
    out.append((f"ax-{start}", section(f"ax-{start}", inner, color, eyebrow, title, notes)))
    for k, cols in enumerate(pack_blocks(blocks), 1):
        inner = '<div style="display:flex;flex-direction:row;gap:32px;align-items:start">' + "".join(
            f'<div style="width:{COL_W}px;display:flex;flex-direction:column;gap:16px">'
            + "".join(code_box(lb, ln) for lb, ln in col) + "</div>" for col in cols) + "</div>"
        sid = f"ax-{start + k}"
        out.append((sid, section(sid, inner, color, eyebrow, f"{title} — 데이터 {k}", notes)))
    return out


def table_slides(rows: list[tuple[str, str]], color: str, eyebrow: str, title: str, start: int) -> list[tuple[str, str]]:
    """A key/meaning dictionary, as many slides as it needs."""
    out, cur, used = [], [], 54
    for k, v in rows:
        h = max(len(wrap(v, 1664 * 0.7 - 30, mono=False)), len(wrap(k, 1664 * 0.3 - 30))) * 34 + 18
        if cur and used + h > H_AVAIL:
            out.append(cur)
            cur, used = [], 54
        cur.append((k, v))
        used += h
    if cur:
        out.append(cur)
    res = []
    for i, part in enumerate(out):
        body = "".join(f'<tr><td style="{MONO}">{esc(k)}</td><td>{esc(v)}</td></tr>' for k, v in part)
        inner = (f'<table style="font-size:24px;color:{DARK};background:#FFFFFF"><tr><th style="width:30%">키</th>'
                 f'<th style="width:70%">뜻</th></tr>{body}</table>')
        sid = f"ax-{start + i}"
        res.append((sid, section(sid, inner, color, eyebrow, title + (f" ({i + 1}/{len(out)})" if len(out) > 1 else ""))))
    return res


def divider(sid: str, color: str, part: str, title: str, text: str) -> tuple[str, str]:
    return (sid, f'<section id="{sid}" style="background:{color};color:#F6F5F1;{FONT};padding:128px;display:flex;'
                 f'flex-direction:column;justify-content:center;gap:28px">\n'
                 f'<p style="font-size:32px;font-weight:600;color:#F6F5F1">{esc(part)}</p>\n'
                 f'<h1 style="font-size:88px;font-weight:700;line-height:1.15;color:#F6F5F1">{esc(title)}</h1>\n'
                 f'<p style="font-size:36px;line-height:1.4;color:#F6F5F1">{esc(text)}</p>\n</section>\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--examples", required=True, type=Path)
    ap.add_argument("--assets", required=True, type=Path)
    ap.add_argument("--deck", required=True, type=Path, help="the deck's project/ folder")
    a = ap.parse_args()
    ex = json.loads(a.examples.read_text(encoding="utf-8"))
    amap = json.loads(a.assets.read_text(encoding="utf-8"))
    slides: list[tuple[str, str]] = []
    sections = {}

    def add(items, section_key=None, desc=None):
        if section_key and items:
            sections[section_key] = {"description": desc, "start": items[0][0]}
        slides.extend(items)

    nxt = lambda: 1 + len(slides)
    add([divider(f"ax-{nxt()}", OCR_C, "부록 A", "OCR 과제 데이터 예시",
                 "입력 데이터부터 과제 8종의 문항 한 줄, 학습 샘플까지 실제 형식 그대로")],
        "ax-ocr", "부록 A: OCR 과제의 실제 데이터 예시")
    ocr = [e for e in ex if e["part"] == "OCR"]
    for e in ocr[:1]:
        add(example_slides(e, amap, OCR_C, "부록 A · OCR 입력 데이터", nxt()))
    add(table_slides(list(C.OCR_ROW.items()), OCR_C, "부록 A · OCR 문항 필드", "문항 한 줄의 필드 (*_tasks.jsonl)", nxt()))
    for e in ocr[1:]:
        add(example_slides(e, amap, OCR_C, f"부록 A · OCR {e['no']}", nxt()))

    add([divider(f"ax-{nxt()}", BANK_C, "부록 B", "은행 업무 과제 데이터 예시",
                 "과제 8종의 문항 한 줄: 이미지, 질문, 정답, 채점 정보, meta, 학습 레코드")],
        "ax-bank", "부록 B: 은행 업무 과제 8종의 실제 데이터 예시")
    add(table_slides(list(C.BANK_COMMON.items()), BANK_C, "부록 B · 필드", "문항 한 줄의 공통 필드 (tasks/<과제>.jsonl)", nxt()))
    add(table_slides(list(C.META.items()), BANK_C, "부록 B · 필드", "meta 키", nxt()))
    add(table_slides(list(C.EVAL.items()), BANK_C, "부록 B · 필드", "eval 키", nxt()))
    bank = [e for e in ex if e["part"] == "BANK"]
    for e in [e for e in bank if e["no"].startswith("2-")]:
        add(example_slides(e, amap, BANK_C, f"부록 B · 은행 업무 {e['no']}", nxt()))
    add([divider(f"ax-{nxt()}", BANK_C, "부록 C", "서류 대조 사례 14종",
                 "사례마다 변조 문항 한 건 (format_only 는 정상 문항)")],
        "ax-cases", "부록 C: 서류 대조 불일치 사례 14종의 실제 문항")
    for e in [e for e in bank if e["no"].startswith("3-")]:
        add(example_slides(e, amap, BANK_C, f"부록 C · 서류 대조 {e['no']}", nxt()))
    add([divider(f"ax-{nxt()}", BANK_C, "부록 D", "심사 질의 규칙",
                 "규칙마다 문항 한 건: 질문 전문, 정답, 허용 오차")],
        "ax-rules", "부록 D: 심사 질의 규칙별 실제 문항")
    for e in [e for e in bank if e["no"].startswith("4-")]:
        add(example_slides(e, amap, BANK_C, f"부록 D · 심사 질의 {e['no']}", nxt()))

    sdir = a.deck / "slides"
    for old in sdir.glob("ax-*.html"):
        old.unlink()
    for sid, body in slides:
        (sdir / f"{sid}.html").write_text(body, encoding="utf-8")
    deck = json.loads((a.deck / "deck.json").read_text(encoding="utf-8"))
    deck["order"] = [s for s in deck["order"] if not s.startswith("ax-")] + [sid for sid, _ in slides]
    deck["sections"] = {k: v for k, v in deck["sections"].items() if not k.startswith("ax-")} | sections
    (a.deck / "deck.json").write_text(json.dumps(deck, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(slides)} appendix slides")


if __name__ == "__main__":
    main()
