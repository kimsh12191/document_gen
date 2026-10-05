"""템플릿 렌더링 + 정답(GT) 수집.

템플릿에서 값은 반드시 f('경로') 로 출력한다. f()는
  1) 값을 <span data-field="경로"> 로 감싸 HTML에 넣고 (이미지 렌더 시 bbox 추출용)
  2) 화면에 표시된 문자열을 GT로 기록한다.
따라서 GT는 '문서에 실제로 보이는 값'과 항상 일치한다.
"""
from __future__ import annotations

import random
import re
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup, escape

from .banks import bank_view, brand_accent, form_bank, form_context
from .entities import Profile
from .registry import DocSpec

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"

_MISSING = object()

FONTS_SANS = ["'Malgun Gothic'", "'Nanum Gothic'", "'NanumBarunGothic'", "'Noto Sans CJK KR'", "'Gulim'", "'Dotum'"]
FONTS_SERIF = ["'Batang'", "'Nanum Myeongjo'", "'Noto Serif CJK KR'", "'Gungsuh'"]


def lookup(data: Any, path: str) -> Any:
    cur = data
    for part in path.split("."):
        if isinstance(cur, (list, tuple)):
            cur = cur[int(part)]
        elif isinstance(cur, dict):
            cur = cur[part]
        else:
            cur = getattr(cur, part)
    return cur


# 도장·서명 자리의 기본 항목명 (템플릿에서 label 을 주지 않았을 때)
MARK_LABELS = {
    "issuer": "발급기관 직인", "corp": "법인인감", "registered": "등록 인감", "company": "회사 직인",
    "payer": "징수의무자", "employer": "사용자", "employee": "근로자", "grantor": "위임인",
    "mortgagor": "근저당권설정자", "guarantor": "보증인", "debtor": "채무자", "applicant": "신청인",
    "customer": "고객", "holder": "예금주", "taxpayer": "신고인", "customs": "세관장",
    "staff.clerk": "담당자", "staff.manager": "책임자",
}


class FieldRecorder:
    """템플릿의 f() 구현. 출력된 값을 순서대로 기록한다.

    기록 형식 (fields 의 원소):
      일반 값   {"key", "label", "value", "type"?}            value 가 None 이면 '빈 칸'(항목명은 있는데 값이 없음)
      선택형    위 + "options": [{"text", "checked"}]          m.choice / m.agree / bf.multi
      도장·서명 {"key": "seal.xxx"|"sign.xxx", "type": "seal"|"signature",
                 "label", "value": 도장 글자 또는 None, "present": bool, "kind"?, "anchor"?}
    """

    def __init__(self, data: dict, rng: random.Random | None = None):
        self.data = data
        self.fields: dict[str, dict] = {}
        self.groups: dict[str, dict] = {}  # 복수 선택 체크박스 묶음 (정답이 아니라 라벨 정보)
        self.rng = rng or random.Random(0)
        self._auto = 0

    def __call__(self, path: str, value: Any = _MISSING, label: str | None = None, type: str | None = None) -> Markup:
        try:
            v = lookup(self.data, path) if value is _MISSING else value
        except (KeyError, IndexError, AttributeError):
            v = None
        text = None if v is None or (isinstance(v, str) and not v.strip()) else str(v)
        if label:
            label = re.sub(r"[\s\u3000]+", "", str(label))
        rec = self.fields.get(path)
        if rec is None:
            rec = self.fields[path] = {"key": path, "label": label, "value": text}
            if type:
                rec["type"] = type
        elif label and not rec["label"]:
            rec["label"] = label
        body = escape(text or "").replace("\n", Markup("<br>"))
        return Markup(f'<span class="fv" data-field="{escape(path)}">{body}</span>')

    def has(self, path: str) -> bool:
        try:
            return lookup(self.data, path) is not None
        except (KeyError, IndexError, AttributeError):
            return False

    def opts(self, path: str, options: list, selected, label: str | None = None) -> str:
        """선택형 항목의 보기 목록을 기록한다. selected 는 값 하나 또는 리스트."""
        sel = set(selected) if isinstance(selected, (list, tuple, set)) else {selected}
        if isinstance(selected, (list, tuple, set)):  # 복수 선택: 선택값은 path.0, path.1 ... 리스트 필드로 기록됨
            self.groups[path] = {"key": path, "label": re.sub(r"[\s\u3000]+", "", label) if label else None,
                                 "type": "checkbox_multi", "options": [{"text": str(o), "checked": o in sel} for o in options]}
            return ""
        rec = self.fields.get(path)
        if rec is None:  # 선택된 보기가 없을 때 (모두 □)
            rec = self.fields[path] = {"key": path, "label": re.sub(r"[\s\u3000]+", "", label) if label else None,
                                       "value": None}
        rec["type"] = "checkbox"
        rec["options"] = [{"text": str(o), "checked": o in sel} for o in options]
        return ""

    def mark(self, key: str | None, type: str = "seal", present: bool = True, text: str | None = None,
             label: str | None = None, kind: str | None = None, anchor: str | None = None) -> str:
        """도장·서명 자리를 기록하고 key 를 돌려준다 (템플릿에서 data-mark 속성으로 쓴다)."""
        root = "seal" if type == "seal" else "sign"  # 'signature' 는 서명란 이름 값으로 이미 쓰인다
        if not key:
            self._auto += 1
            key = f"{root}.mark{self._auto}"
        elif "." not in key:
            key = f"{root}.{key}"
        else:
            key = f"{root}.{key}"
        n, base = 2, key
        while key in self.fields:  # 같은 자리 이름이 여러 번 나오면 번호를 붙인다
            key = f"{base}{n}"
            n += 1
        if not label:
            short = key.split(".", 1)[1]
            label = MARK_LABELS.get(short) or MARK_LABELS.get(short.rstrip("0123456789"))
            if not label and short.startswith("signer"):
                label = f"서명인 {short[6:] or 1}"
            label = label or kind
        label = re.sub(r"[\s\u3000]+", "", label) if label else None
        rec = {"key": key, "type": type, "label": label, "value": text if present else None, "present": bool(present)}
        if kind:
            rec["kind"] = kind
        if anchor:
            rec["anchor"] = anchor
        self.fields[key] = rec
        return key

    def chance(self, p: float) -> bool:
        """템플릿용 난수 (도장 누락 등). 렌더링마다 결정론적."""
        return self.rng.random() < p


def _gt_value(fld: dict):
    """정답 JSON 값: 도장·서명은 날인/서명 여부(bool), 나머지는 표시 문자열(빈 칸은 null)."""
    return fld["present"] if fld.get("type") in ("seal", "signature") else fld["value"]


def to_nested(fields: list[dict]) -> dict:
    """['a.b', 'items.0.x'] 형태의 키를 중첩 dict/list 로 변환."""
    root: dict = {}
    for fld in fields:
        if fld.get("group_only") or fld.get("group"):
            continue
        parts = fld["key"].split(".")
        cur: Any = root
        for i, part in enumerate(parts):
            last = i == len(parts) - 1
            nxt_is_idx = not last and parts[i + 1].isdigit()
            if isinstance(cur, list):
                idx = int(part)
                while len(cur) <= idx:
                    cur.append(None)
                if last:
                    cur[idx] = _gt_value(fld)
                else:
                    if cur[idx] is None:
                        cur[idx] = [] if nxt_is_idx else {}
                    cur = cur[idx]
            else:
                if last:
                    cur[part] = _gt_value(fld)
                else:
                    cur = cur.setdefault(part, [] if nxt_is_idx else {})
    return root


def random_style(rng: random.Random, spec: DocSpec) -> dict:
    """같은 서류라도 렌더링마다 폰트/크기/선 색 등을 조금씩 바꿔 시각적 다양성을 준다."""
    serif = rng.random() < 0.25
    fonts = FONTS_SERIF if serif else FONTS_SANS
    primary = rng.choice(fonts)
    return {
        "font": f"{primary}, {', '.join(f for f in fonts if f != primary)}, sans-serif",
        "font_size": round(rng.uniform(12.0, 14.0), 1),
        "title_size": rng.randint(24, 32),
        "line_height": round(rng.uniform(1.35, 1.6), 2),
        "border": rng.choice(["#000", "#222", "#333", "#444", "#555"]),
        "border_w": rng.choice([1, 1, 1, 1.5]),
        "label_bg": rng.choice(["#f2f2f2", "#eeeeee", "#f5f5f0", "#eef2f7", "#ffffff", "#f7f3ea"]),
        "accent": rng.choice(["#1f3a68", "#00573f", "#0b5394", "#7a1f2b", "#3d3d3d", "#005a8c"]),
        "cell_pad": rng.choice([4, 5, 6, 7]),
        "page_pad": rng.randint(48, 72),
        "paper": rng.choice(["#ffffff", "#ffffff", "#fffffb", "#fcfcfa"]),
        "seal_color": rng.choice(["#d11", "#c00", "#e0312b", "#b22222"]),
    }


def kv_layout(rows: list, cols: int) -> list[list]:
    """kv 매크로용 배치. [라벨, 경로, True] 처럼 3번째 값이 있으면 그 항목은 한 줄 전체를 차지한다.
    반환: 줄 리스트, 각 줄은 (라벨, 경로, 값칸 colspan) 리스트."""
    lines, cur = [], []
    for item in rows:
        if item is not None and len(item) > 2 and item[2]:
            if cur:
                lines.append(cur + [None] * (cols - len(cur)))
                cur = []
            lines.append([(item[0], item[1], cols * 2 - 1)])
            continue
        cur.append(None if item is None else (item[0], item[1], 1))
        if len(cur) == cols:
            lines.append(cur)
            cur = []
    if cur:
        lines.append(cur + [None] * (cols - len(cur)))
    return lines


def seal_lines(text: str) -> list[str]:
    """도장 안 글자 배치: 3자 이하 1줄, 4자 2x2, 9자 이하 3자씩, 그보다 길면 4자씩."""
    n = len(text)
    if n <= 3:
        return [text]
    per = 2 if n == 4 else 3 if n <= 9 else 4
    return [text[i:i + per] for i in range(0, n, per)]


def seal_font(text: str) -> str:
    """긴 도장 글자는 글자 크기를 줄여 도장 밖으로 넘치지 않게 한다."""
    n = len(text)
    return "" if n <= 6 else "font-size:11px" if n <= 9 else "font-size:9.5px;line-height:1.05"


def scribble(name: str, rng: random.Random) -> Markup:
    """손 서명 흉내: 이름 길이에 맞춘 이어진 곡선 (SVG). 글자로 읽히지 않는 서명 모양."""
    n = max(2, len(name))
    w, h = 26 * n + rng.randint(10, 30), rng.randint(30, 42)
    x, y = 2.0, h * rng.uniform(0.45, 0.7)
    d = [f"M{x:.1f},{y:.1f}"]
    for _ in range(n * rng.randint(2, 3)):
        nx = min(w - 2, x + rng.uniform(6, 16))
        c1 = (x + rng.uniform(-4, 8), rng.uniform(0, h))
        c2 = (nx + rng.uniform(-8, 4), rng.uniform(0, h))
        ny = rng.uniform(h * 0.25, h * 0.85)
        d.append(f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {nx:.1f},{ny:.1f}")
        x, y = nx, ny
    if rng.random() < 0.6:  # 끝의 긴 꼬리 획
        d.append(f"Q{x + 10:.1f},{h * 0.2:.1f} {w:.1f},{y + rng.uniform(-6, 6):.1f}")
    color = rng.choice(["#1b2a80", "#111", "#222c55", "#0d3a8a"])
    sw = rng.uniform(1.2, 2.0)
    return Markup(f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><path d="{" ".join(d)}" fill="none" '
                  f'stroke="{color}" stroke-width="{sw:.2f}" stroke-linecap="round" stroke-linejoin="round"/></svg>')


_env: Environment | None = None


def env() -> Environment:
    global _env
    if _env is None:
        _env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), undefined=StrictUndefined,
                           autoescape=True, trim_blocks=True, lstrip_blocks=True)
        _env.globals.update(kv_layout=kv_layout, seal_lines=seal_lines, seal_font=seal_font, scribble=scribble,
                           BR=Markup("<br>"))
    return _env


def render(spec: DocSpec, profile: Profile, seed: int | str, sample_mark: bool | None = None,
           style: dict | None = None) -> tuple[str, list[dict], dict]:
    """서류 하나를 렌더링한다. (html, fields, data) 반환."""
    bk = None
    if spec.group == "bank_form":  # 은행 서식: 서식을 낸 은행(옛 은행 포함)에 맞춰 프로필·표기를 바꾼다
        profile = bank_view(profile, form_bank(profile, spec.id))
        bk = form_context(profile, spec.id)
    data_rng = random.Random(f"data:{seed}:{spec.id}")
    data = spec.generate(profile, data_rng)
    if style is None:
        style = random_style(random.Random(f"style:{seed}:{spec.id}"), spec)
        if bk:
            accent = brand_accent(profile.bank, random.Random(f"accent:{seed}:{spec.id}"))
            style["accent"] = accent or style["accent"]
    rec = FieldRecorder(data, random.Random(f"marks:{seed}:{spec.id}"))
    html = env().get_template(spec.template).render(
        d=data, f=rec, val=lambda p: lookup(data, p), style=style, spec=spec, bk=bk,
        sample_mark=spec.sample_mark if sample_mark is None else (sample_mark or spec.sample_mark),
    )
    groups = [{**g, "value": None, "group_only": True} for g in rec.groups.values()]
    return html, list(rec.fields.values()) + groups, data
