"""layout.json + grid_<n>.json → template.html.j2 · form.json · fields.md (form-from-image 스킬 4단계).

    python .claude/skills/form-from-image/build.py <초안 폴더>

모양(표 자리·열 너비·행 높이·합친 칸·표 밖 글자 자리)은 grid.py 가 잰 숫자를 그대로 쓰고,
글자와 값 자리는 layout.json 에서 가져온다. 다시 돌리면 template.html.j2·form.json·fields.md 를 새로 쓴다 (손으로 고친 것은 사라짐 —
고칠 것은 layout.json 에 적는다).

layout.json (모델이 쓴다):
{
  "form":  {"name": "서식 이름", "group": "bank_form", "category": "internal"},
  "pages": [                                            # 쪽마다 하나, 순서대로
    {"cells": {"T2.2": "신청구분",                        # 칸 글자 (grid 의 칸 이름)
               "T2.3": "{apply.kind:등록|변경|해제}",      # 값 자리 표시는 아래
               "T2.1": {"t": "신청\\n사항", "size": 14, "bold": true, "align": "center"}},
     "blocks": {"B1": {"t": "예금(신탁) 잔액증명 의뢰서", "size": 26, "bold": true},
                "B9": null},                             # null = 그리지 않음 (바코드·티끌)
     "extra":  [{"box": [x0, y0, x1, y1], "t": "…"}],     # grid 가 못 찾은 글자·선 (선: {"line": [x0, y0, x1, y1]})
     "skip":   ["T5"]}                                   # 표를 통째로 빼기 (잘못 찾은 표)
  ],
  "fields": {"apply.kind": {"label": "신청구분", "type": "checkbox", "source": "rule:choice",
                            "choices": ["등록", "변경", "해제"], "description": "신청 종류"}},
  "lists":  {}                                           # 반복 표 (NEW_FORM_SPEC 3절 꼴 그대로)
}

글자 안 표시:
  {키}                      값 자리 → f("키")
  {키:보기1|보기2}           체크 보기 하나 고르기 → m.choice("키", [...])  (원본 "□ 보기1 □ 보기2")
  {seal:키|도장 글자}         기관 도장 → m.seal(...)
  {sign:키|이름 키|표시}      서명·날인 자리 → m.sigspot(...)  (표시: 원본 글자 "(서명/인)" 등. 없으면 "(서명 또는 인)")
  \\n 줄 바꿈. 띄어쓰기는 그대로 (여러 칸 띄움도).
칸·글자 덩어리 옵션: t(글자) size(px) bold align(left|center|right) valign(top|middle|bottom) shade(true/false) wrap(true: 칸 너비에서 줄 바꿈)
  squeeze(가로 줄임 0.7~1, 기본은 원본 글자 너비에 맞춰 자동 · null 이면 줄이지 않음)
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

TOKEN = re.compile(r"\{([^{}]+)\}")
KEY = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+)*$")
SHEET_H = 1095              # 쪽 하나 높이 (쪽 번호 자리를 남김)
PAD = 4


class BuildError(Exception):
    pass


def esc(s: str) -> str:
    """고정 글자: html 이스케이프, 여러 칸 띄움 유지, jinja 문법 글자 막기."""
    s = html.escape(s, quote=False)
    s = s.replace("{{", "{ {").replace("}}", "} }").replace("{%", "{ %").replace("%}", "% }").replace("{#", "{ #")
    return re.sub(r" {2,}", lambda m: "&nbsp;" * len(m.group()), s)


def jstr(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


class Builder:
    def __init__(self, layout: dict):
        self.fields = dict(layout.get("fields") or {})
        self.lists = dict(layout.get("lists") or {})
        self.used: dict[str, list[str]] = {}
        self.warnings: list[str] = []

    def label(self, key: str) -> str:
        if key in self.fields:
            return self.fields[key].get("label") or key
        m = re.match(r"^([a-z0-9_]+)\.(\d+)\.([a-z0-9_.]+)$", key)
        if m and m.group(1) in self.lists:
            col = (self.lists[m.group(1)].get("fields") or {}).get(m.group(3)) or {}
            return col.get("label") or m.group(3)
        return key

    def use(self, key: str, where: str):
        if not KEY.match(key):
            raise BuildError(f"{where}: 키 '{key}' 는 영어 소문자·숫자·밑줄·점만 (예: holder.name)")
        self.used.setdefault(key, []).append(where)

    def value(self, key: str, where: str) -> str:
        self.use(key, where)
        call = f'{{{{ f({jstr(key)}, label={jstr(self.label(key))}) }}}}'
        m = re.match(r"^([a-z0-9_]+)\.(\d+)\.", key)
        if m and m.group(1) in self.lists:          # 인쇄된 빈 행: 값이 있는 행만 채운다
            return f'{{% if (d.{m.group(1)} or [])|length > {m.group(2)} %}}{call}{{% endif %}}'
        return call

    def inline(self, text: str, where: str) -> str:
        out, pos = [], 0
        for m in TOKEN.finditer(text):
            out.append(esc(text[pos:m.start()]))
            out.append(self.token(m.group(1).strip(), where))
            pos = m.end()
        out.append(esc(text[pos:]))
        return "".join(out).replace("\n", "<br>")

    def token(self, body: str, where: str) -> str:
        if body.startswith("seal:"):
            key, _, text = body[5:].partition("|")
            key = key.strip()
            self.use(key, where)
            return f'{{{{ m.seal({jstr(text.strip() or "인")}, square=True, key={jstr(key.removeprefix("seal."))}, kind="직인") }}}}'
        if body.startswith("sign:"):
            key, name, mark = (body[5:].split("|") + ["", ""])[:3]
            key = key.strip()
            self.use(key, where)
            name_expr = f"val({jstr(name.strip())})" if name.strip() else '""'
            mark_arg = f", mark={jstr(mark.strip())}" if mark.strip() else ""
            return f'{{{{ m.sigspot({jstr(key.removeprefix("sign."))}, {name_expr}{mark_arg}, label={jstr(self.label(key))}) }}}}'
        if ":" in body:
            key, _, opts = body.partition(":")
            key = key.strip()
            options = [o.strip() for o in opts.split("|") if o.strip()]
            if not options:
                raise BuildError(f"{where}: 보기가 없습니다: {{{body}}}")
            self.use(key, where)
            f = self.fields.setdefault(key, {"label": key, "type": "checkbox", "source": "rule:choice"})
            if f.get("source") == "rule:choice" and f.get("choices") != options:
                if f.get("choices"):
                    self.warnings.append(f"{key}: fields 의 choices {f['choices']} 를 템플릿 보기 {options} 로 맞춤")
                f["choices"] = options
            return f'{{{{ m.choice({jstr(key)}, {json.dumps(options, ensure_ascii=False)}, label={jstr(self.label(key))}) }}}}'
        return self.value(body, where)


def em_width(text: str) -> float:
    """글자 줄 하나의 대략 너비 (글자 크기 = 1). 한글·한자·□ 는 1, 영문·숫자는 0.55 안팎, 띄어쓰기 0.3."""
    w = 0.0
    for ch in text:
        o = ord(ch)
        if 0xAC00 <= o <= 0xD7A3 or 0x3130 <= o <= 0x318F or 0x4E00 <= o <= 0x9FFF or ch in "※□■○●◎▶▷【】「」『』·":
            w += 1.0
        elif ch == " ":
            w += 0.3
        elif ch in "()[].,:;'\"`|!-/~":
            w += 0.35
        elif ch.isupper() or ch.isdigit():
            w += 0.62
        elif ch.isalpha():
            w += 0.52
        else:
            w += 0.6
    return w


def squeeze(text: str, ink_w: float | None, size: float | None) -> float | None:
    """고정 글자가 원본보다 넓게 그려질 것 같으면 줄일 비율 (원본이 좁은 글꼴일 때). 줄이기만, 0.7 아래로는 안 함.
    값 자리가 섞인 칸은 값이 없는 줄이 가장 넓은 줄일 때만 그 줄로 잰다."""
    if not text or not ink_w or not size:
        return None
    lines = text.split("\n")
    fixed = [em_width(l) for l in lines if not TOKEN.search(l)]
    if not fixed:
        return None
    em = max(fixed)
    if em < 1.5 or em < max(em_width(TOKEN.sub("", l)) for l in lines):
        return None
    k = ink_w / (size * em * 0.95) * 0.97
    return round(max(0.7, k), 2) if k < 0.99 else None


def norm_item(v) -> dict | None:
    if v is None:
        return None
    if isinstance(v, str):
        return {"t": v}
    if isinstance(v, dict):
        return v
    raise BuildError(f"칸 글자는 글자 또는 {{\"t\": …}} 이어야 합니다: {v!r}")


def style(**kw) -> str:
    return ";".join(f"{k.replace('_', '-')}:{v}" for k, v in kw.items() if v not in (None, ""))


def cell_html(b: Builder, cell: dict, item: dict | None) -> str:
    x0, y0, x1, y1 = cell["box"]
    ink = cell.get("ink") or {}
    it = item or {}
    text = it.get("t", "")
    attrs = []
    if cell["rs"] > 1:
        attrs.append(f'rowspan="{cell["rs"]}"')
    if cell["cs"] > 1:
        attrs.append(f'colspan="{cell["cs"]}"')
    shaded = it.get("shade", bool(cell.get("shade")))
    align = it.get("align") or ink.get("align") or "left"
    size = it.get("size") or (ink.get("size") if ink else None)
    sx = it.get("squeeze", squeeze(text, ink["box"][2] - ink["box"][0], size) if ink and size else None)
    pad_l = pad_r = PAD
    if text and ink and align == "left" and not it.get("align"):
        pad_l = max(PAD, ink["box"][0] - x0 - 1)
    if text and ink and align == "right" and not it.get("align"):
        pad_r = max(PAD, x1 - ink["box"][2] - 1)
    if size and sx:                              # 좁은 글꼴 흉내: 글자를 sx 만큼 작게 쓰고 세로만 1/sx 로 늘린다 (칸 너비 안에 맞음)
        size = float(size) * sx
    css = style(text_align=align if align != "left" else None,
                vertical_align=it.get("valign") if it.get("valign") not in (None, "middle") else None,
                font_size=f"{round(float(size), 1)}px" if size else None,
                font_weight="700" if it.get("bold") else None,
                padding=f"0 {pad_r}px 0 {pad_l}px" if (pad_l, pad_r) != (PAD, PAD) else None,
                white_space="pre-wrap" if it.get("wrap") else None)
    cls = " ".join(c for c in ("shade" if shaded else "", "wrap" if it.get("wrap") else "") if c)
    inner = b.inline(text, cell["id"]) if text else ""
    if inner and sx:
        inner = f'<span class="sx" style="transform:scaleY({round(1 / sx, 3)})">{inner}</span>'
    return (f'<td data-cell="{cell["id"]}"' + (" " + " ".join(attrs) if attrs else "") + (f' class="{cls}"' if cls else "")
            + (f' style="{css}"' if css else "") + f">{inner}</td>")


def table_html(b: Builder, t: dict, cells: dict, page: int) -> str:
    xs, ys = t["xs"], t["ys"]
    width = xs[-1] - xs[0]
    open_ = set(t.get("open") or [])
    cls = "g" + "".join(f" open-{s}" for s in sorted(open_))
    rows: dict[int, list[dict]] = {}
    for c in t["cells"]:
        rows.setdefault(c["r"], []).append(c)
    lines = [f'<table class="{cls}" data-grid="{page}:{t["id"]}" style="left:{xs[0]}px;top:{ys[0]}px;width:{width}px">',
             "<colgroup>" + "".join(f'<col style="width:{xs[i + 1] - xs[i]}px">' for i in range(len(xs) - 1)) + "</colgroup>"]
    for r in range(1, len(ys)):
        tds = "".join(cell_html(b, c, norm_item(cells.get(c["id"]))) for c in sorted(rows.get(r, []), key=lambda c: c["c"]))
        lines.append(f'<tr style="height:{ys[r] - ys[r - 1]}px">{tds}</tr>')
    lines.append("</table>")
    return "\n".join(lines)


def block_html(b: Builder, bid: str, box: list, item: dict, guess_size: float | None, page_w: int = 794) -> str:
    x0, y0, x1, y1 = box
    text = item.get("t", "")
    if not text and not item.get("line"):
        return ""
    size = float(item.get("size") or guess_size or 13)
    sx = item.get("squeeze", squeeze(text, x1 - x0, size))
    if sx:
        size *= sx
    cx = (x0 + x1) / 2
    align = item.get("align") or ("center" if abs(cx - page_w / 2) < 25 and x0 > 80 else "left")
    lines = text.count("\n") + 1
    top = round((y0 + y1) / 2 - lines * size * 1.25 / 2)    # 줄 상자 가운데 = 원본 글자 가운데 (line-height 1.25)
    css = {"top": f"{top}px", "font-size": f"{round(size, 1)}px"}
    scale = f" scaleY({round(1 / sx, 3)})" if sx else ""
    if align == "center":
        css.update({"left": f"{round(cx)}px", "transform": f"translateX(-50%){scale}", "text-align": "center"})
    elif align == "right":
        css.update({"right": f"{794 - x1}px", "text-align": "right"})
        if sx:
            css["transform"] = scale.strip()
    else:
        css["left"] = f"{x0}px"
        if sx:
            css["transform"] = scale.strip()
    if item.get("bold"):
        css["font-weight"] = "700"
    if item.get("wrap"):
        css.update({"width": f"{x1 - x0 + 4}px", "white-space": "pre-wrap"})
    s = ";".join(f"{k}:{v}" for k, v in css.items())
    return f'<div class="tx" data-block="{bid}" style="{s}">{b.inline(text, bid)}</div>'


def build(draft: Path) -> dict:
    lp = draft / "layout.json"
    if not lp.exists():
        raise BuildError("layout.json 이 없습니다")
    try:
        layout = json.loads(lp.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise BuildError(f"layout.json JSON 오류: {e}") from e
    b = Builder(layout)
    pages = layout.get("pages") or []
    grids = sorted(draft.glob("grid_*.json"), key=lambda p: int(re.sub(r"\D", "", p.stem)))
    if not grids:
        raise BuildError("grid_<n>.json 이 없습니다. 먼저 grid.py")
    if len(pages) != len(grids):
        raise BuildError(f"layout.json pages 가 {len(pages)}개인데 원본은 {len(grids)}쪽입니다")
    sheets = []
    for n, (gp, pg) in enumerate(zip(grids, pages), 1):
        g = json.loads(gp.read_text(encoding="utf-8"))
        cells, blocks = pg.get("cells") or {}, pg.get("blocks") or {}
        skip = set(pg.get("skip") or [])
        known = {c["id"] for t in g["tables"] for c in t["cells"]} | {bl["id"] for bl in g["blocks"]}
        for k in list(cells) + list(blocks):
            if k.split(":")[-1] not in known:
                raise BuildError(f"{n}쪽: '{k}' 는 grid_{n}.json 에 없는 이름입니다 (칸 T<n>.<n>, 글자 덩어리 B<n>)")
        parts = []
        for t in g["tables"]:
            if t["id"] in skip:
                continue
            parts.append(table_html(b, t, {k.split(":")[-1]: v for k, v in cells.items()}, n))
        for bl in g["blocks"]:
            if bl["id"] in skip:
                continue
            item = norm_item(blocks.get(bl["id"], {"t": ""}))
            if item is None:
                continue
            if not item.get("t"):
                continue
            parts.append(block_html(b, bl["id"], bl["box"], item, bl.get("size")))
        for i, ex in enumerate(pg.get("extra") or [], 1):
            if ex.get("line"):
                x0, y0, x1, y1 = ex["line"]
                parts.append(f'<div class="ln" style="left:{min(x0, x1)}px;top:{min(y0, y1)}px;'
                             f'width:{max(abs(x1 - x0), 1)}px;height:{max(abs(y1 - y0), 1)}px"></div>')
            elif ex.get("box"):
                parts.append(block_html(b, f"X{i}", ex["box"], ex, ex.get("size")))
        hidden = [bl["box"] for bl in g["blocks"] if bl["id"] in skip or (bl["id"] in blocks and blocks[bl["id"]] is None)]
        for ln in g.get("lines") or []:
            if f"L{ln['pos']}" in skip:
                continue
            a = (ln["from"], ln["pos"], ln["to"], ln["pos"]) if ln["dir"] == "h" else (ln["pos"], ln["from"], ln["pos"], ln["to"])
            length = max(a[2] - a[0], a[3] - a[1], 1)
            if any(b[1] - 4 <= a[1] and a[3] <= b[3] + 4 and b[0] - 4 <= a[0] + (a[2] - a[0]) and          # 그리지 않기로 한 덩어리(로고 등)에
                   (min(a[2], b[2]) - max(a[0], b[0]) if a[2] > a[0] else (min(a[3], b[3]) - max(a[1], b[1]))) >= 0.5 * length
                   for b in hidden):                       # 반 넘게 걸친 획은 그 덩어리의 일부
                continue
            if ln["dir"] == "h":
                parts.append(f'<div class="ln" style="left:{ln["from"]}px;top:{ln["pos"]}px;width:{ln["to"] - ln["from"]}px;height:1px"></div>')
            else:
                parts.append(f'<div class="ln" style="left:{ln["pos"]}px;top:{ln["from"]}px;width:1px;height:{ln["to"] - ln["from"]}px"></div>')
        h = min(SHEET_H, g["size"][1])
        sheets.append(f'<div class="sheet pg-keep" data-page="{n}" style="height:{h}px">\n' + "\n".join(parts) + "\n</div>")

    # 쓴 키 ↔ 칸 목록
    fields = {k: v for k, v in b.fields.items()}
    list_names = set(b.lists)
    for key, where in b.used.items():
        m = re.match(r"^([a-z0-9_]+)\.\d+\.", key)
        if m and m.group(1) in list_names:
            continue
        if key.startswith(("seal.", "sign.")):
            continue
        if key not in fields:
            fields[key] = {"label": key, "type": "text", "source": "rule:note"}
            b.warnings.append(f"{key} ({', '.join(where)}): fields 에 없어 임시로 rule:note — layout.json fields 에 label·type·source·description 을 적는다")
    unused = [k for k in fields if k not in b.used and not k.startswith(("seal.", "sign."))]
    for k in unused:
        b.warnings.append(f"{k}: fields 에 있는데 어느 칸에도 안 씀 — 지우거나 칸에 {{{k}}} 를 넣는다")
        del fields[k]
    names = sorted(fields)
    for a in names:
        for c in names:
            if c != a and c.startswith(a + "."):
                raise BuildError(f"키 '{a}' 가 '{c}' 의 앞부분입니다 (NEW_FORM_SPEC 4절). 하나를 바꾸세요")

    form = dict(layout.get("form") or {})
    form_json = {"name": form.get("name") or draft.name, "group": form.get("group") or "bank_form",
                 "category": form.get("category") or "internal", "page": "a4", "origin": "analyzer", "parent": None,
                 "source_image": "source.png", "fields": {k: clean_field(v) for k, v in fields.items()}}
    if b.lists:
        form_json["lists"] = b.lists
    tpl = TEMPLATE_HEAD + "\n".join(sheets) + "\n{% endblock %}\n"
    (draft / "template.html.j2").write_text(tpl, encoding="utf-8")
    (draft / "form.json").write_text(json.dumps(form_json, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (draft / "fields.md").write_text(fields_md(form_json, b.used), encoding="utf-8")
    return {"pages": len(sheets), "fields": len(fields), "lists": len(b.lists), "warnings": b.warnings}


FIELD_KEYS = ("label", "type", "source", "choices", "text", "description", "q", "part", "format", "fmt", "pattern", "options")


def clean_field(v: dict) -> dict:
    return {k: v[k] for k in FIELD_KEYS if k in v}


def fields_md(form: dict, used: dict) -> str:
    lines = [f"# {form['name']} — 뽑을 키와 항목 설명 (build.py 가 layout.json 에서 만듦)", "",
             "| 키 | 원본 항목명 | type | source | 이 칸이 무엇인지 | 자리 |", "|---|---|---|---|---|---|"]
    for k, v in form["fields"].items():
        src = v.get("source", "")
        if v.get("choices"):
            src += " " + json.dumps(v["choices"], ensure_ascii=False)
        lines.append(f"| `{k}` | {v.get('label', '')} | {v.get('type', '')} | {src} | {v.get('description', '')} | {', '.join(used.get(k, []))} |")
    for name, lst in (form.get("lists") or {}).items():
        lines += ["", f"## 반복 표 `{name}` — 행 {lst.get('min')}~{lst.get('max')}", "",
                  "| 열 키 | 원본 머리글 | type | source | 이 열이 무엇인지 |", "|---|---|---|---|---|"]
        for k, v in (lst.get("fields") or {}).items():
            lines.append(f"| `{k}` | {v.get('label', '')} | {v.get('type', '')} | {v.get('source', '')} | {v.get('description', '')} |")
    marks = sorted(k for k in used if k.startswith(("seal.", "sign.")))
    if marks:
        lines += ["", "## 도장·서명", ""] + [f"- `{k}` — {', '.join(used[k])}" for k in marks]
    return "\n".join(lines) + "\n"


TEMPLATE_HEAD = """{% extends "_base.html.j2" %}
{% import "_macros.html.j2" as m with context %}
{# form-from-image build.py 가 layout.json · grid_<n>.json 에서 만든 서식. 자리 단위는 쪽 px (가로 794).
   고칠 때는 layout.json 을 고치고 build.py 를 다시 돌린다 (여기를 직접 고치면 다음 build 에서 사라짐). #}
{% block style %}
.page { padding: 0; }
.sheet { position: relative; width: 794px; }
.sheet .tx { position: absolute; white-space: pre; line-height: 1.25; }
.sheet .ln { position: absolute; background: var(--border); }
.sheet table.g { position: absolute; table-layout: fixed; border-collapse: collapse; margin: 0; }
.sheet table.g td { border: var(--bw) solid var(--border); padding: 0 3px; line-height: 1.2; white-space: pre; overflow: hidden;
  vertical-align: middle; word-break: keep-all; }
.sheet table.g td.wrap { white-space: pre-wrap; }
.sheet table.g td.shade { background: var(--label-bg); }
.sheet .sx { display: inline-block; }
.sheet table.g.open-left tr > td:first-child { border-left: none; }
.sheet table.g.open-right tr > td:last-child { border-right: none; }
.sheet table.g.open-top tr:first-child > td { border-top: none; }
.sheet table.g.open-bottom tr:last-child > td { border-bottom: none; }
{% endblock %}
{% block content %}
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft", type=Path)
    a = ap.parse_args()
    try:
        res = build(a.draft)
    except BuildError as e:
        print(f"오류: {e}")
        print(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))
        return 1
    for w in res["warnings"]:
        print("경고:", w)
    print(json.dumps({"ok": True, **res}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
