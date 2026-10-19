"""모델 답에서 JSON 꺼내기. 길이 상한에 잘린 답도 잘리기 전까지의 내용을 살린다.

잘린 답을 그냥 버리면(파싱 실패 → 빈 답) 그 묶음의 모든 행이 '못 읽음'으로 세어져 원인 분석이 틀어진다.
살리는 방법: 처음 '{' 또는 '[' 부터 훑으며 객체·배열이 닫힌 자리를 기억해 두고, 마지막으로 닫힌 자리에서 자른 뒤
아직 열려 있는 괄호를 닫는다. 쓰다 만 행은 버려진다.
"""
from __future__ import annotations

import json
import re

from docgen.bench.metrics import parse_json

CLOSE = {"{": "}", "[": "]"}


def repair(text: str):
    """잘린 JSON 원문 → 살린 객체, 못 살리면 None."""
    m = re.search(r"```(?:json)?\s*", text)
    t = text[m.end():] if m else text
    t = t.split("```")[0]
    starts = [i for i in (t.find("{"), t.find("[")) if i >= 0]
    if not starts:
        return None
    t = t[min(starts):]
    stack: list[str] = []
    cuts: list[tuple[int, str]] = []  # (닫힌 자리, 그때 열려 있던 괄호를 닫는 글자)
    in_str = esc = False
    for i, ch in enumerate(t):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch in CLOSE:
            stack.append(ch)
        elif ch in "}]":
            if not stack:
                break
            stack.pop()
            if not stack:
                cuts.append((i, ""))
                break
            cuts.append((i, "".join(CLOSE[c] for c in reversed(stack))))
    for pos, closers in reversed(cuts[-300:]):
        try:
            return json.loads(t[:pos + 1] + closers)
        except ValueError:
            continue
    return None


def parse_output(text: str | None) -> tuple[object, bool]:
    """(객체 또는 None, 살려 낸 답인지). 온전한 답이면 (객체, False)."""
    obj = parse_json(text)
    if obj is not None or not isinstance(text, str):
        return obj, False
    obj = repair(text)
    return obj, obj is not None
