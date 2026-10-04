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


class FieldRecorder:
    """템플릿의 f() 구현. 출력된 값을 순서대로 기록한다."""

    def __init__(self, data: dict):
        self.data = data
        self.fields: dict[str, dict] = {}

    def __call__(self, path: str, value: Any = _MISSING, label: str | None = None) -> Markup:
        v = lookup(self.data, path) if value is _MISSING else value
        text = "" if v is None else str(v)
        if label:
            label = re.sub(r"[\s\u3000]+", "", str(label))
        rec = self.fields.get(path)
        if rec is None:
            self.fields[path] = {"key": path, "label": label, "value": text}
        elif label and not rec["label"]:
            rec["label"] = label
        body = escape(text).replace("\n", Markup("<br>"))
        return Markup(f'<span class="fv" data-field="{escape(path)}">{body}</span>')


def to_nested(fields: list[dict]) -> dict:
    """['a.b', 'items.0.x'] 형태의 키를 중첩 dict/list 로 변환."""
    root: dict = {}
    for fld in fields:
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
                    cur[idx] = fld["value"]
                else:
                    if cur[idx] is None:
                        cur[idx] = [] if nxt_is_idx else {}
                    cur = cur[idx]
            else:
                if last:
                    cur[part] = fld["value"]
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


_env: Environment | None = None


def env() -> Environment:
    global _env
    if _env is None:
        _env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), undefined=StrictUndefined,
                           autoescape=True, trim_blocks=True, lstrip_blocks=True)
        _env.globals.update(kv_layout=kv_layout, seal_lines=seal_lines, seal_font=seal_font, BR=Markup("<br>"))
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
    rec = FieldRecorder(data)
    html = env().get_template(spec.template).render(
        d=data, f=rec, val=lambda p: lookup(data, p), style=style, spec=spec, bk=bk,
        sample_mark=spec.sample_mark if sample_mark is None else (sample_mark or spec.sample_mark),
    )
    return html, list(rec.fields.values()), data
