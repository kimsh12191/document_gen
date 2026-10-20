"""공식 PDF의 인쇄층을 편집 가능한 HTML 글자와 SVG 표 선으로 옮긴다.

python -m docgen.scripts.build_official_html [--id hana_official_003] [--overwrite]

입력은 manual/official_html_sources.json. 다운로드·원본 교체는 하지 않는다.
PDF의 글자 좌표를 보존하되 글꼴은 시스템 글꼴로 대체하고 폭을 맞춘다.
이미지(로고·QR·직인 등)는 복제하지 않는다. 기재란은 manifest의 fields 또는
기존 hf### 생성 함수를 사용한다. 자동 추출된 기재란의 의미 검수는 별도다.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manual" / "official_html_sources.json"
PX = 96 / 72


def number(n):
    return f"{n:.3f}".rstrip("0").rstrip(".") or "0"


def color(c):
    return "none" if c is None else "rgb(" + ",".join(str(round(v * 255)) for v in c[:3]) + ")"


def graphics(page, exclusions):
    """표 선·음영·원본이 윤곽선으로 저장한 글자를 SVG로 보존. 보안 표식은 제외."""
    out = []
    omitted = 0
    for d in page.get_drawings():
        r = d["rect"]
        if any(pymupdf.Rect(b).contains(r) for b in exclusions):
            omitted += 1
            continue
        commands = []
        last = None
        for it in d["items"]:
            if it[0] == "re":
                a = it[1]
                commands.append(f"M{number(a.x0)} {number(a.y0)}H{number(a.x1)}V{number(a.y1)}H{number(a.x0)}Z")
                last = None
            elif it[0] == "qu":
                q = it[1]
                points = [q.ul, q.ur, q.lr, q.ll]
                commands.append("M" + "L".join(f"{number(p.x)} {number(p.y)}" for p in points) + "Z")
                last = None
            elif it[0] in ("l", "c"):
                pts = it[1:]
                if last != pts[0]:
                    commands.append(f"M{number(pts[0].x)} {number(pts[0].y)}")
                commands.append(("L" if it[0] == "l" else "C") + " ".join(f"{number(p.x)} {number(p.y)}" for p in pts[1:]))
                last = pts[-1]
        if not commands:
            continue
        if d.get("closePath"):
            commands.append("Z")
        fill = color(d.get("fill")) if "f" in d["type"] else "none"
        stroke = color(d.get("color")) if "s" in d["type"] else "none"
        dash = d.get("dashes") or ""
        # PDF dash arrays are optional; the geometry and line width remain explicit.
        import re
        dm = re.search(r"\[([^\]]+)\]", dash)
        dash_attr = f' stroke-dasharray="{html.escape(dm[1])}"' if dm else ""
        out.append(f'<path d="{"".join(commands)}" fill="{fill}" stroke="{stroke}" '
                   f'stroke-width="{number(d.get("width") or 0.4)}" fill-opacity="{d.get("fill_opacity", 1)}" '
                   f'stroke-opacity="{d.get("stroke_opacity", 1)}" fill-rule="{"evenodd" if d.get("even_odd") else "nonzero"}"{dash_attr}/>')
    w, h = page.rect.width, page.rect.height
    return f'<svg class="printed-lines" viewBox="0 0 {number(w)} {number(h)}" aria-hidden="true">' + "".join(out) + "</svg>", omitted


def printed_text(page, exclusions):
    out = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for s in line["spans"]:
                text = s["text"]
                r = pymupdf.Rect(s["bbox"])
                # Some official PDFs pair outlined headings with an invisible text layer.
                # Painting that search layer again doubles the visible heading.
                if s.get("alpha", 255) == 0 or not text.strip() or any(pymupdf.Rect(b).contains(r) for b in exclusions):
                    continue
                x, baseline = s["origin"]
                # Keep separate spans: the editor can change the actual printed wording.
                size = s["size"] * PX
                c = f'#{s["color"]:06x}'
                bold = 700 if s["flags"] & 16 or s["font"].endswith(("B", "Bold")) else 400
                top = (baseline - s["size"] * .88) * PX
                literal = html.escape(text).replace("{", "&#123;").replace("}", "&#125;")
                out.append(f'<span class="printed" data-width="{number(r.width * PX)}" '
                           f'style="left:{number(x * PX)}px;top:{number(top)}px;font-size:{number(size)}px;'
                           f'font-weight:{bold};color:{c}">{literal}</span>')
    return "\n".join(out)


def compile_form(entry, overwrite=False):
    source = ROOT / entry["source_file"]
    expected = entry["sha256"]
    actual = hashlib.sha256(source.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f"원본 해시 불일치: {source}")
    dest = ROOT / "templates" / "copies" / entry["id"]
    if dest.exists() and not overwrite:
        raise FileExistsError(f"편집한 서식 보호: {dest} (--overwrite로 명시)")
    doc = pymupdf.open(source)
    pages = entry.get("source_pages", list(range(len(doc))))
    parts = ['{% extends "_official_base.html.j2" %}', '{% block pages %}']
    stats = []
    for pno, source_pno in enumerate(pages):
        page = doc[source_pno]
        w, h = page.rect.width, page.rect.height
        excluded = entry.get("exclude_regions", {}).get(str(source_pno), [])
        vectors, omitted = graphics(page, excluded)
        parts.append(f'<section class="page" data-source-page="{source_pno + 1}" style="width:{number(w * PX)}px;height:{number(h * PX)}px">')
        parts.append(vectors)
        parts.append(printed_text(page, excluded))
        if entry.get("parent", "").startswith("hf"):
            types = json.dumps(entry.get("parent_item_types", ["text", "hidden", "check", "mark"]))
            parts.append('{% set parent_types = ' + types + ' %}{% set pno = ' + str(pno) + ' %}{% include "_official_values.html.j2" %}')
        for field in entry.get("placements", []):
            if field.get("page", 0) != pno:
                continue
            x0, y0, x1, y1 = [v * PX for v in field["rect"]]
            key = field["key"]
            label = entry["fields"][key].get("label", key)
            size = field.get("size", 9) * PX
            opening = f'<div class="entry" style="left:{number(x0)}px;top:{number(y0)}px;width:{number(x1-x0)}px;height:{number(y1-y0)}px;font-size:{number(size)}px"'
            k, lab = json.dumps(key, ensure_ascii=False), json.dumps(label, ensure_ascii=False)
            if field.get("check"):
                parts.append(opening + f' data-box="{key}#0">'
                             '{% set value_span = f(' + k + ', label=' + lab + ', type="checkbox") %}'
                             '{{ f.opts(' + k + ', [' + lab + '], val(' + k + '), ' + lab + ') }}'
                             '<span style="position:absolute;color:transparent;font-size:1px">{{ value_span }}</span>'
                             '{% if val(' + k + ') %}✓{% endif %}</div>')
            else:
                parts.append(opening + '>{{ f(' + k + ', label=' + lab + ') }}</div>')
        parts.append('<div class="sample-mark">합성 데이터 · 견본</div></section>')
        stats.append({"source_page": source_pno + 1, "text_spans": len(page.get_text("words")), "omitted_paths": omitted,
                      "omitted_images": len(page.get_images())})
    parts.append('{% endblock %}')
    form = {k: entry[k] for k in ("name", "group", "category", "parent", "fields", "shared_copies") if k in entry}
    form.update({"page": "a4_landscape" if doc[pages[0]].rect.width > doc[pages[0]].rect.height else "a4",
                 "origin": "copy", "description": entry["description"],
                 "source": {k: entry[k] for k in ("publisher", "url", "source_file", "sha256", "checked_at", "revision", "matches", "source_pages", "online_verification") if k in entry},
                 "reconstruction": {"method": "native_html_text_svg_lines", "pages": stats,
                                    "notice": "시스템 글꼴 대체. 원본 이미지·직인·QR 제외. 합성값을 채운 연구용 HTML 견본."}})
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "form.json").write_text(json.dumps(form, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (dest / "template.html.j2").write_text("\n".join(parts) + "\n", encoding="utf-8")
    doc.close()
    return len(pages)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--id", action="append")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for entry in manifest["forms"]:
        if args.id and entry["id"] not in args.id:
            continue
        n = compile_form(entry, args.overwrite)
        print(f'{entry["id"]}: {n}쪽')


if __name__ == "__main__":
    main()
