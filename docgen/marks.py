"""표시 요소: 손글씨·체크 표시·도장·서명이 "어느 칸에 얼마나 나올지"(확률)와 "어떻게 생겼는지"(풀).

  docgen/marks.json        확률 설정. 없는 항목은 아래 DEFAULTS (= 이 파일을 만들기 전 코드의 상수)
  assets/marks/pools.json  풀: 체크 표시·서명 이미지, 도장 틀, 손글씨·인쇄체 글꼴
  assets/marks/<풀>/…      풀에 올린 이미지 (투명 배경 PNG)

- 기본값은 예전 코드와 같은 값·같은 순서다. 설정과 풀을 바꾸지 않으면 생성 결과가 그대로다.
- 풀에서 고를 항목이 하나뿐이면 난수를 쓰지 않는다. 항목을 더하면 그때부터 그 서류의 나머지 값도 달라질 수 있다.
- 서식마다 덮어쓰기: overlay 는 add_template/overrides/<ID>.json 의 "marks".
- 실서류에서 잘라 온 서명·도장은 저장소 풀에 넣지 않는다 (studio 가 private_forms_dir 아래 풀에만 저장).
"""
from __future__ import annotations

import copy
import json
import random
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SETTINGS = ROOT / "docgen" / "marks.json"
POOLS_DIR = ROOT / "assets" / "marks"
POOLS = POOLS_DIR / "pools.json"

DEFAULTS = {
    "hand": 0.72,                     # overlay: 서류 전체를 손글씨로 쓸 확률 (나머지는 인쇄체)
    "staff": {"processed": 0.85,      # 결재란: 접수·처리를 마친 서류 비율
              "filled": 0.85},        #         처리된 서류에서 칸마다 찍혀 있을 확률
    "sign_spot": {"seal_below": 0.4, "sign_below": 0.88},   # overlay "(서명 또는 인)": 난수 < 0.4 도장, < 0.88 서명, 나머지 빈칸
    "seal_spot": {"seal_below": 0.5, "sign_below": 0.8},    # overlay "인감·서명/날인" 칸
    "staff_spot": {"square_below": 0.2, "seal_below": 0.7},  # 결재란: 사각 도장 비율, 도장(나머지는 서명)
}

DEFAULT_POOLS = {
    # overlay 체크 표시 모양 (가중치 = 예전 목록에서 나온 횟수). html 서식은 render.checkmark 의 손 V
    "check": [{"id": "V", "name": "손으로 그은 V", "builtin": True, "weight": 2},
              {"id": "✓", "name": "✓ 글자", "builtin": True, "weight": 1},
              {"id": "✔", "name": "✔ 글자", "builtin": True, "weight": 1},
              {"id": "■", "name": "■ 칠하기", "builtin": True, "weight": 1},
              {"id": "O", "name": "○ 동그라미", "builtin": True, "weight": 1}],
    "sign": [{"id": "scribble", "name": "선으로 그린 낙서 서명 (코드)", "builtin": True, "weight": 1}],
    "seal": [{"id": "builtin", "name": "원형·사각 도장 (코드)", "builtin": True, "weight": 1}],
    # 손글씨 글꼴은 fonts/<id>.woff2 가 있어야 한다. scale: 같은 칸 높이에서 키우는 비율 (글꼴마다 글자 몸집이 다름)
    "hand_fonts": [{"id": "NanumPen", "scale": 1.3, "weight": 1, "builtin": True},
                   {"id": "NanumBrush", "scale": 1.3, "weight": 1, "builtin": True},
                   {"id": "HiMelody", "scale": 1.05, "weight": 1, "builtin": True},
                   {"id": "GamjaFlower", "scale": 1.0, "weight": 1, "builtin": True}],
    "print_fonts": [{"id": "'Nanum Gothic'", "weight": 1, "builtin": True}, {"id": "'NanumBarunGothic'", "weight": 1, "builtin": True},
                    {"id": "'Noto Sans CJK KR'", "weight": 1, "builtin": True}, {"id": "'Nanum Myeongjo'", "weight": 1, "builtin": True},
                    {"id": "'NanumGothicCoding'", "weight": 1, "builtin": True}],
}
POOL_NAMES = {"check": "체크 표시", "sign": "서명", "seal": "도장 틀", "hand_fonts": "손글씨 글꼴", "print_fonts": "인쇄체 글꼴"}


def _merge(base: dict, over: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        out[k] = _merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def _read(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def settings(form_marks: dict | None = None) -> dict:
    """확률 설정: 기본값 ← docgen/marks.json ← 서식 덮어쓰기."""
    return _merge(_merge(DEFAULTS, _read(SETTINGS)), form_marks or {})


def pools() -> dict:
    """풀 전체. pools.json 에 없는 풀은 기본 풀."""
    saved = _read(POOLS)
    return {name: saved.get(name, copy.deepcopy(items)) for name, items in DEFAULT_POOLS.items()}


def expand(items: list[dict]) -> list[dict]:
    """켜진 항목을 가중치만큼 늘어놓은 목록 (rng.choice 로 고른다). 순서는 풀 순서 그대로."""
    out = []
    for it in items:
        if it.get("enabled", True):
            out += [it] * max(0, int(it.get("weight", 1)))
    return out


def pick(rng: random.Random, items: list[dict]) -> dict | None:
    """풀에서 하나. 고를 것이 하나뿐이면 난수를 쓰지 않는다."""
    lst = expand(items)
    if not lst:
        return None
    if len({id(x) for x in lst}) == 1:
        return lst[0]
    return rng.choice(lst)


@lru_cache(maxsize=256)
def _image_bytes(rel: str, mtime: float) -> bytes:
    return (POOLS_DIR / rel).read_bytes()


def image(rel: str) -> bytes | None:
    """풀 이미지 (assets/marks/ 기준 경로). 렌더러가 https://docgen.local/marks/<경로> 로 받는다."""
    p = (POOLS_DIR / rel).resolve()
    if POOLS_DIR.resolve() not in p.parents or not p.is_file():
        return None
    return _image_bytes(rel, p.stat().st_mtime)


def image_url(item: dict) -> str | None:
    return f"https://docgen.local/marks/{item['file']}" if item.get("file") else None
