"""그린 html 의 값 칸 도우미 (예전 서류 대조 과제의 값 바꾸기는 업무 묶음과 함께 없앰).

  visible_keys(html)  화면에 글자로 보이는 값 칸의 키 (build.render_doc)
  NAME_LABEL          이름 칸의 키 설명 (tasks.field_kind)
"""
from __future__ import annotations

import re

NAME_LABEL = re.compile(r"성명|이름|예금주|대표자")


def visible_keys(html: str) -> set[str]:
    """화면에 글자로 보이는 값 칸의 키 (원본 서식의 투명 칸·체크 보기 칸 제외)."""
    hidden = set(re.findall(r'<div class="(?:ov hid|opt)"[^>]*>\s*<span class="fv" data-field="([^"]+)"', html))
    return set(re.findall(r'data-field="([^"]+)"', html)) - hidden
