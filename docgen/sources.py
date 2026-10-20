"""값 출처: 서식 칸에 넣을 값을 "어디서 가져올지" 적은 짧은 문자열을 실제 값으로 바꾼다.

overlay 서식의 사람 수정(add_template/overrides/<ID>.json)과 화면에서 만든 html 서식(templates/copies/<ID>/form.json)이
같은 규칙을 쓴다.

  profile.<경로>        고객 프로필 값. 예: profile.person.name, profile.employment.company.address.road_short
                        날짜는 2025.03.02 꼴, 숫자는 천 단위 쉼표
  rule:<종류>           값 종류에 맞는 그럴듯한 값 (realform.Values.by_kind 와 같은 규칙).
                        종류: date amount fx_amount percent rate currency account phone number count biz_no passport
                              product goods reason bank branch country email address company person note ...
  rule:choice           칸 정보의 choices 목록에서 하나
  rule:fixed            칸 정보의 text 그대로
  rule:free_text        짧은 자유 기재 문장 (가끔 비어 있음)
  rule:empty            늘 빈 칸
  rule:date_seq         반복 행에서 행마다 늘어나는 날짜 (html 서식의 거래내역 등)
"""
from __future__ import annotations

import dataclasses
import random
from datetime import date, timedelta

from . import korean as K

RULE_KINDS = ["date", "amount", "fx_amount", "percent", "rate", "currency", "account", "phone", "number", "count",
              "biz_no", "passport", "check_no", "product", "goods", "reason", "bank", "branch", "country", "email",
              "address", "company", "person", "note", "loan_subject", "repay", "check_kind"]
SPECIAL_RULES = ["choice", "fixed", "free_text", "empty", "date_seq"]
FREE_TEXT = ["해당 없음", "본인 요청", "만기 해지", "계좌 정리", "생활자금", "추가 서류 제출 예정", "담당자 확인 완료",
             "전화 확인", "기존 계좌 유지", "주소 변경"]


def lookup_profile(p, path: str):
    """profile.person.name → p.person.name. 리스트는 숫자로 (profile.accounts.0.number)."""
    cur = p
    for part in path.split(".")[1:]:
        if cur is None:
            return None
        if isinstance(cur, (list, tuple)):
            i = int(part)
            cur = cur[i] if i < len(cur) else None
        elif isinstance(cur, dict):
            cur = cur.get(part)
        else:
            cur = getattr(cur, part, None)
    return cur


def show(v) -> str | None:
    """프로필 값 → 서식에 쓰는 글자."""
    if v is None:
        return None
    if isinstance(v, date):
        return K.fmt_date(v, "dot")
    if isinstance(v, bool):
        return "예" if v else "아니오"
    if isinstance(v, int):
        return f"{v:,}"
    if isinstance(v, float):
        return f"{v:,.2f}".rstrip("0").rstrip(".")
    if dataclasses.is_dataclass(v):
        return getattr(v, "road_short", None) or getattr(v, "name", None) or str(v)
    return str(v)


def value(source: str, p, rng: random.Random, item: dict | None = None, values=None, row: int = 0) -> str | None:
    """값 출처 하나를 값으로. values: realform.Values (rule:<종류> 에 씀, 없으면 새로 만든다)."""
    item = item or {}
    if source.startswith("profile."):
        return show(lookup_profile(p, source))
    if not source.startswith("rule:"):
        raise ValueError(f"알 수 없는 값 출처: {source}")
    rule = source[5:]
    if rule == "empty":
        return None
    if rule == "fixed":
        return item.get("text")
    if rule == "choice":
        choices = item.get("choices") or []
        return rng.choice(choices) if choices else None
    if rule == "free_text":
        return rng.choice(FREE_TEXT) if rng.random() < 0.6 else None
    if rule == "date_seq":
        start = p.issue_date - timedelta(days=item.get("span_days", 90))
        return K.fmt_date(start + timedelta(days=row * item.get("step_days", 1) + rng.randint(0, 1)), "dot")
    if values is None:
        from .realform import Values

        values = Values(p, rng, item.get("class", "기본"))
    return values.by_kind(rule, item.get("label") or "")


def profile_paths(p, prefix: str = "profile", depth: int = 4) -> list[dict]:
    """프로필에서 고를 수 있는 경로와 예시 값 (화면의 값 출처 고르기). 리스트는 첫 원소만."""
    out: list[dict] = []

    def walk(v, path, d):
        if v is None or d < 0:
            return
        if dataclasses.is_dataclass(v) and not isinstance(v, type):
            for f in dataclasses.fields(v):
                walk(getattr(v, f.name), f"{path}.{f.name}", d - 1)
            for prop in ("road_short", "road_full", "jibun_full", "region", "name_en", "age", "gender_ko"):
                if isinstance(getattr(type(v), prop, None), property):
                    walk(getattr(v, prop), f"{path}.{prop}", d - 1)
        elif isinstance(v, (list, tuple)):
            if v and not isinstance(v[0], tuple):
                walk(v[0], f"{path}.0", d - 1)
        elif isinstance(v, dict):
            return
        else:
            out.append({"source": path, "example": show(v)})

    walk(p, prefix, depth)
    return out
