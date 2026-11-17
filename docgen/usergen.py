"""사람이 코드로 더하는 생성기: docgen/forms/_common/generators.py 의 @generator 함수.

칸의 생성 방법(fields.json 의 source)을 rule:<함수 이름> 으로 고르면 문서를 만들 때마다 그 함수가 값을 만든다.
studio 영역 편집기의 생성 방법 고르기 창에 "직접 만든 생성기 (코드)" 로 나온다 (이름 = @generator 의 첫 인자).

    from docgen.usergen import generator

    @generator("카드번호 (가운데 가림)", note="1234-56**-****-7890 꼴")
    def card_masked(p, rng, item, row):
        return f"{rng.randint(1000, 9999)}-{rng.randint(10, 99)}**-****-{rng.randint(1000, 9999)}"

함수가 받는 것: p 고객 프로필 (docgen/entities.py — p.person.name, p.issue_date …), rng 난수 (이것만 쓴다),
item 칸 정보 (label 항목명, choices 보기, text 글자 …), row 표 행 번호 (표가 아니면 0). 돌려줄 것: 글자 (None·"" = 빈 칸).
약속은 서식 generate.py 와 같다: 난수는 rng 만, 파일·네트워크·시간을 읽지 않는다 (같은 seed → 같은 값).
이름은 영어 소문자·숫자·밑줄, 이미 있는 값 종류(docgen/sources.py RULE_KINDS·SPECIAL_RULES, 키 사전 kinds)와 겹치면 안 된다.
"""
from __future__ import annotations

import importlib.util
import re
import threading
from pathlib import Path

_ID = re.compile(r"[a-z][a-z0-9_]{1,40}")
_lock = threading.Lock()
_cache: dict = {"key": None, "gens": {}, "error": None}


def path() -> Path:
    from . import formdir

    return formdir.SHARED / "generators.py"


def generator(name: str, note: str = ""):
    """생성기 표시: 화면에 보일 이름(name)과 설명(note)."""
    def wrap(fn):
        fn._docgen_generator = {"name": name, "note": note}
        return fn
    return wrap


def _load() -> dict:
    p = path()
    key = p.stat().st_mtime_ns if p.exists() else None
    with _lock:
        if _cache["key"] == key and key is not None:
            if _cache["error"]:
                raise ValueError(_cache["error"])
            return _cache["gens"]
        gens, error = {}, None
        if p.exists():
            spec = importlib.util.spec_from_file_location(f"docgen_user_generators_{key}", p)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
            except Exception as e:  # noqa: BLE001 — 어느 줄인지와 함께 (이 파일을 쓰는 칸만 실패)
                import traceback

                tb = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == str(p)]
                error = f"{p.name}{f' {tb[-1].lineno}번째 줄' if tb else ''}: {type(e).__name__}: {e}"
            if error is None:
                taken = _taken()
                for fn_name, fn in vars(mod).items():
                    meta = getattr(fn, "_docgen_generator", None)
                    if not (callable(fn) and meta):
                        continue
                    if not _ID.fullmatch(fn_name):
                        error = f"{p.name}: 생성기 함수 이름 {fn_name!r} 는 영어 소문자·숫자·밑줄"
                    elif fn_name in taken:
                        error = f"{p.name}: 생성기 {fn_name!r} 가 이미 있는 값 종류와 이름이 겹칩니다"
                    else:
                        gens[fn_name] = {"name": meta["name"], "note": meta["note"], "fn": fn,
                                         "line": getattr(getattr(fn, "__code__", None), "co_firstlineno", None)}
        _cache.update(key=key, gens=gens if error is None else {}, error=error)
        if error:
            raise ValueError(error)
        return gens


def _taken() -> set[str]:
    from . import keyrules as KR
    from .sources import RULE_KINDS, SPECIAL_RULES

    return set(RULE_KINDS) | set(SPECIAL_RULES) | set(KR.load()["kinds"]) | {"text"}


def all_generators() -> dict:
    """{함수 이름: {name, note, fn, line}}. 파일에 오류가 있으면 ValueError (어느 줄인지)."""
    return _load()


def get(rule: str) -> dict | None:
    """rule 이름의 생성기 (없으면 None). 파일에 오류가 있으면 ValueError."""
    if not _ID.fullmatch(rule or ""):
        return None
    return _load().get(rule)


def error() -> str | None:
    """파일 오류 (없으면 None). 화면·검사가 보여 준다."""
    try:
        _load()
    except ValueError as e:
        return str(e)
    return None
