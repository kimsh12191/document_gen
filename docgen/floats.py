"""자유 위치 요소: 접수인·일부인·원본대조필 같은 도장, Ref No·접수번호 같은 번호처럼 서류마다 아무 데나 찍히는 것.

두 곳에서 정한다.
  서식마다   overlay 서식(원본 hf###·그린 img_*)의 칸 목록 fields.json 칸 {"t": "float", "page", "rect"(나올 수 있는 영역, pt), "preset", ...}
             — studio 영역 편집기의 자유 위치 도구
  모든 서식  표시 설정 docgen/forms/_common/marks.json 의 "floats": [{"preset", "p", "area", ...}] — studio 표시 요소 화면.
             overlay 는 realform.py 가 자리까지 정하고, html 서식은 html_block 이 정답을 기록하고 floats.js 가 쪽 나눔 뒤 자리를 고른다

요소 하나의 설정 (둘 다 같은 칸)
  preset   종류 (아래 PRESETS)               p       나올 확률 (0~1, 기본 0.5)
  answer   도장 글자를 정답(kie)에 넣을지      key     정답 키 (없으면 종류의 기본 키)
  text     도장 글자 틀 ({date} {bank} {branch} {name} 자리, 줄바꿈 \\n) — 직접 만든 도장
  source · pattern · choices   번호·글자의 생성 방법 (칸의 생성 방법과 같은 규칙, docgen/sources.py)
  shape    round · square        color   red · blue       size   도장 지름 pt
  area     (모든 서식만) any · top · bottom · right · top_right · bottom_right — 쪽에서 나올 영역

정답: 도장은 체크·도장 과제(marks)에 seal.<키> (찍혔는지 + 위치). answer 가 켜졌으면 도장 글자도 kie 칸 <키> (값 + 위치).
번호·글자는 kie 칸 <키>. 안 나온 서류: 도장은 seal.<키> 가 '없음', 번호는 칸이 없다.
위치·나올지는 따로 난수 (서식의 다른 칸 값을 흔들지 않는다). 영역 안에서 값 칸과 많이 겹치면 다시 뽑는다.
"""
from __future__ import annotations

import random
import re

PRESETS = {
    "received": {"name": "접수인 (날짜·지점)", "type": "stamp", "shape": "round", "text": "접 수\n{date}\n{branch}", "answer": True,
                 "key": "stamp_received", "size": 62},
    "dated": {"name": "일부인 (은행·날짜·지점)", "type": "stamp", "shape": "round", "text": "{bank}\n{date}\n{branch}", "answer": True,
              "key": "stamp_dated", "size": 64},
    "certified": {"name": "원본대조필", "type": "stamp", "shape": "square", "text": "원본\n대조필", "answer": False,
                  "key": "stamp_certified", "size": 46},
    "confirm": {"name": "확인", "type": "stamp", "shape": "round", "text": "확 인", "answer": False, "key": "stamp_confirm", "size": 36},
    "bank_seal": {"name": "은행 직인 (지점장)", "type": "stamp", "shape": "square", "text": "{bank}\n{branch}장", "answer": False,
                  "key": "stamp_bank", "size": 50},
    "stamp": {"name": "직접 만든 도장", "type": "stamp", "shape": "round", "text": "", "answer": True, "key": "stamp", "size": 50},
    "ref_no": {"name": "문서번호 (Ref No)", "type": "text", "pattern": "Ref. No. ####-######", "key": "ref_no", "style": "print"},
    "receipt_no": {"name": "접수번호", "type": "text", "pattern": "접수 제####-#####호", "key": "receipt_no", "style": "stamp"},
    "text": {"name": "직접 만든 글자·번호", "type": "text", "key": "note", "style": "print"},
}
AREAS = {   # 모든 서식 설정의 영역 (쪽 크기 대비 비율 x0, y0, x1, y1)
    "any": (0.04, 0.03, 0.96, 0.97), "top": (0.04, 0.01, 0.96, 0.2), "bottom": (0.04, 0.8, 0.96, 0.99),
    "right": (0.62, 0.03, 0.98, 0.97), "top_right": (0.55, 0.01, 0.98, 0.25), "bottom_right": (0.55, 0.75, 0.98, 0.99),
}
AREA_NAMES = {"any": "쪽 어디나", "top": "위쪽 여백", "bottom": "아래쪽 여백", "right": "오른쪽", "top_right": "오른쪽 위",
              "bottom_right": "오른쪽 아래"}
COLORS = {"red": "#d11", "blue": "#2747b8"}
STYLES = ("print", "stamp", "hand")


def preset(el: dict) -> dict:
    """요소 설정 + 종류 기본값."""
    base = PRESETS.get(el.get("preset") or "", PRESETS["stamp"])
    return {**base, **{k: v for k, v in el.items() if v not in (None, "")}}


def check(el: dict, where: str) -> None:
    """설정 검사 (영역 편집기·표시 요소 저장 전)."""
    if el.get("preset") not in PRESETS:
        raise ValueError(f"{where}: 자유 위치 종류는 {list(PRESETS)} 중 하나")
    pv = el.get("p", 0.5)
    if not isinstance(pv, (int, float)) or not 0 <= pv <= 1:
        raise ValueError(f"{where}: 나올 확률은 0~1")
    c = preset(el)
    if c["type"] == "stamp" and not (c.get("text") or "").strip():
        raise ValueError(f"{where}: 직접 만든 도장은 도장 글자(text)가 필요합니다 (예: 접 수\\n{{date}})")
    if c["type"] == "text" and not (c.get("source") or c.get("pattern")):
        raise ValueError(f"{where}: 글자·번호는 생성 방법이나 틀(pattern)이 필요합니다")
    if el.get("area") and el["area"] not in AREAS:
        raise ValueError(f"{where}: 영역은 {list(AREAS)} 중 하나")
    if el.get("color") and el["color"] not in COLORS:
        raise ValueError(f"{where}: 색은 red · blue")
    if el.get("style") and el["style"] not in STYLES:
        raise ValueError(f"{where}: 글자 모양은 {STYLES} 중 하나")
    if el.get("key") and not re.fullmatch(r"[a-z][a-z0-9_.]*", el["key"]):
        raise ValueError(f"{where}: 키는 영어 소문자·숫자·밑줄·점")


def stamp_text(c: dict, p, rng: random.Random) -> str:
    """도장 글자: 틀의 {date} {bank} {branch} {name} 를 이 서류 값으로. 날짜는 서류 날짜 (점 또는 띄어 쓴 꼴)."""
    d = p.issue_date
    date = rng.choice([f"{d:%Y.%m.%d}", f"{d.year}. {d.month}. {d.day}.", f"{d:%y.%m.%d}"])
    branch = p.bank_branch if str(p.bank_branch).endswith(("점", "지점")) else f"{p.bank_branch}점"
    vals = {"date": date, "bank": p.bank, "branch": branch, "name": p.person.name}
    return re.sub(r"\{(\w+)\}", lambda m: str(vals.get(m.group(1), m.group(0))), c.get("text") or "").replace("\\n", "\n")


def text_value(c: dict, p, rng: random.Random, item: dict, cls: str, vals) -> str | None:
    """번호·글자: 칸의 생성 방법과 같은 규칙 (source 가 없으면 틀 pattern)."""
    from . import sources as SRC

    src = c.get("source") or "rule:pattern"
    return SRC.value(src, p, rng, {**item, **c, "class": cls}, vals)


def place(size: tuple[float, float], area: list[float], busy: list[list[float]], rng: random.Random) -> list[float]:
    """영역 안에서 (w, h) 상자 자리를 뽑는다. 값 칸(busy)과 겹치면 다시 (둘 중 작은 상자의 25% 넘게, 20번까지,
    못 찾으면 덜 겹친 자리). 인쇄 글자와는 겹쳐도 된다 (실제 서류처럼)."""
    w, h = size
    x0, y0, x1, y1 = area
    best, best_ov = None, None
    for _ in range(20):
        x = rng.uniform(x0, max(x0, x1 - w))
        y = rng.uniform(y0, max(y0, y1 - h))
        r = [x, y, x + w, y + h]
        ov = max([_overlap(r, b) for b in busy] or [0.0])
        if best is None or ov < best_ov:
            best, best_ov = r, ov
        if ov <= 0.25:
            break
    return [round(v, 1) for v in best]


def _overlap(a, b) -> float:
    """겹친 넓이 / 둘 중 작은 상자 넓이 — 긴 번호가 짧은 값을 덮어도 크게 잡힌다."""
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    area = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1])) or 1
    return ix * iy / area


def text_size(text: str, fs: float) -> tuple[float, float]:
    em = sum(1.0 if ord(ch) > 0x2E80 else 0.6 for ch in text) or 1
    return round(em * fs + 6, 1), round(fs * 1.6, 1)


# ---------------------------------------------------------------------------
# html 서식: 모든 서식 설정(marks.json floats)만. 쪽 나눔이 렌더링 중에 정해지므로 자리는 브라우저가 고른다
# (docgen/floats.js — image.py 가 쪽 나눔 뒤에 부른다). 여기서는 나올지·글자·정답 기록만 하고, 숨긴 상자로 html 끝에 붙인다.
# ---------------------------------------------------------------------------

def html_block(spec_id: str, p, seed, rec, settings: dict) -> str:
    """html 서식 끝에 붙일 숨긴 자유 위치 요소들 (<div id="dg-floats">). 없으면 "" (html 이 예전과 같다).
    rec: render.FieldRecorder — 도장은 rec.mark (seal.<키>), 정답 글자·번호는 rec(<키>) 로 기록한다."""
    from markupsafe import escape

    els = settings.get("floats") or []
    if not els:
        return ""
    parts = []
    for j, el in enumerate(els):
        r = random.Random(f"float:{seed}:{spec_id}:{j}")
        c = preset(el)
        show = r.random() < float(c.get("p", 0.5))
        area = c.get("area") or "any"
        jseed = r.randrange(1, 2 ** 31)
        key, label = c["key"], c["name"]
        if c["type"] == "stamp":
            text = stamp_text(c, p, r) if show else ""
            size = round(float(c.get("size") or 50) * 96 / 72, 1)
            ks = rec.mark(key, "seal", show, text if show else None, label=label, kind=c["name"].split(" ")[0])
            color = COLORS.get(c.get("color") or "red")
            lines = [ln for ln in text.split("\n") if ln.strip()] or [""]
            ems = max(sum(1.0 if ord(ch) > 0x2E80 else 0.56 for ch in ln) for ln in lines) or 1
            fs = round(min(size * 0.24, size * 0.78 / ems, size * 0.7 / (len(lines) * 1.12)), 1)
            radius = "4px" if c.get("shape") == "square" else "50%"
            inner = "<br>".join(str(escape(ln)) for ln in lines)
            body = (f'<span data-mark="{escape(ks)}" style="display:flex;align-items:center;justify-content:center;text-align:center;'
                    f'width:{size}px;height:{size}px;border:2px solid {color};border-radius:{radius};color:{color};opacity:.82;'
                    f"font:700 {fs}px/1.12 'Nanum Myeongjo','Noto Serif CJK KR',serif;transform:rotate({r.uniform(-25, 25):.1f}deg)\">{inner}</span>"
                    if show else "")
            ans = ""
            if show and c.get("answer"):   # 도장 글자도 정답 (kie): 도장 자리를 덮는 투명 글자
                ans = (f'<span class="dg-ans" style="position:absolute;inset:0;color:transparent;font-size:1px;overflow:hidden">'
                       f'{rec(key, value=" ".join(text.split()), label=label)}</span>')
            mark_attr = "" if show else f' data-mark="{escape(ks)}"'
            parts.append(f'<div class="dg-float" data-seed="{jseed}" data-area="{area}"{mark_attr} '
                         f'style="position:absolute;width:{size}px;height:{size}px">{body}{ans}</div>')
        elif show:
            v = text_value(c, p, r, el, "기본", None)
            if v in (None, ""):
                continue
            st = c.get("style") or "print"
            color = COLORS[c.get("color") or "blue"] if st == "stamp" else "#1a1a1a"
            rot = f"transform:rotate({r.uniform(-8, 8):.1f}deg);" if st == "stamp" else ""
            fs = round(r.uniform(11, 14.5), 1)
            parts.append(f'<div class="dg-float" data-seed="{jseed}" data-area="{area}" style="position:absolute;white-space:nowrap;'
                         f'font-size:{fs}px;color:{color};{rot}">{rec(key, value=str(v), label=label)}</div>')
    if not parts:
        return ""
    areas = {k: list(v) for k, v in AREAS.items()}
    import json

    # 도장 글자 정답 칸(.dg-ans .fv)이 도장 자리를 다 덮게. style 은 숨긴 상자 밖에 둔다 (상자는 자리를 정한 뒤 지워짐)
    return (f'<style>.dg-ans .fv{{display:block;width:100%;height:100%}}</style>'
            f'<div id="dg-floats" data-areas=\'{json.dumps(areas)}\' style="display:none">{"".join(parts)}</div>')
