"""HTML 값 영역의 별도 수정층. 템플릿 원본을 보존하고 모든 렌더 경로에 같은 수정을 적용한다.

좌표는 페이지 왼쪽 위 기준 CSS px. 반복 출력은 key + occurrence(0부터)로 구분한다.
"""
from __future__ import annotations

import json
import math
import random
import re
import threading
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).parent / "forms" / "html_regions"
_local = threading.local()
_lock = threading.Lock()


def path(doc_id: str, variant: str = "default") -> Path:
    from .registry import load_all
    from .htmlform import form_dir, COPIES

    spec = load_all()[doc_id]
    if spec.template == "_real_form.html.j2":
        raise ValueError("overlay는 기존 영역 편집기를 사용하세요")
    if variant != "default":
        from .template_variants import folder, load as variants
        if variant not in {r["id"] for r in variants(doc_id)["variants"]}:
            raise ValueError("등록되지 않은 레이아웃입니다")
        return folder(doc_id)/(variant+".regions.json")
    folder = form_dir(doc_id)
    if folder and not folder.is_relative_to(COPIES):
        return folder / "regions.json"
    return ROOT / f"{doc_id}.json"


def load(doc_id: str, variant: str = "default") -> dict:
    from .registry import load_all

    if doc_id not in load_all():
        return {"regions": []}
    drafts = getattr(_local, "drafts", {})
    if doc_id in drafts:
        return drafts[doc_id]
    p = path(doc_id,variant)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"regions": []}


def validate(value: dict) -> dict:
    from .sources import RULE_KINDS, SPECIAL_RULES
    from .render import lookup
    from .entities import make_profile

    if not isinstance(value, dict) or set(value) != {"regions"} or not isinstance(value["regions"], list):
        raise ValueError("regions 목록을 지정하세요")
    seen, sources = set(), {}
    for r in value["regions"]:
        if not isinstance(r, dict) or set(r) - {"key", "occurrence", "page", "rect", "source", "label", "text", "choices", "font_size", "drop", "target", "option", "present", "mark_type", "shape"}:
            raise ValueError("모르는 영역 설정입니다")
        key = r.get("key")
        if not isinstance(key, str) or not re.fullmatch(r"[\w]+(?:\.[\w]+)*", key):
            raise ValueError("값 키는 점으로 나눈 문자·숫자·밑줄이어야 합니다")
        n = r.get("occurrence", 0)
        target = r.get("target", "field")
        option = r.get("option", 0)
        if target not in ("field", "mark", "box") or type(option) is not int or option < 0:
            raise ValueError("영역 종류 또는 보기 번호가 잘못되었습니다")
        ident = (target, key, option, n)
        if type(n) is not int or n < 0 or ident in seen:
            raise ValueError("같은 키의 출력 순서가 중복되거나 잘못되었습니다")
        seen.add(ident)
        if "present" in r and type(r["present"]) is not bool:
            raise ValueError("날인·서명 여부는 켜기/끄기입니다")
        if r.get("mark_type", "seal") not in ("seal", "signature") or r.get("shape", "circle") not in ("circle", "square"):
            raise ValueError("도장·서명 종류가 잘못되었습니다")
        if "drop" in r and type(r["drop"]) is not bool:
            raise ValueError("빼기는 켜기/끄기입니다")
        if "rect" in r:
            box = r["rect"]
            if not isinstance(box, list) or len(box) != 4 or any(type(v) not in (int, float) or not math.isfinite(v) or v < 0 for v in box) or box[2] <= box[0] or box[3] <= box[1]:
                raise ValueError("영역은 양수 너비·높이를 가진 좌표 네 개입니다")
            if type(r.get("page")) is not int or r["page"] < 0:
                raise ValueError("영역의 쪽을 지정하세요")
        if "font_size" in r and (type(r["font_size"]) not in (int, float) or not math.isfinite(r["font_size"]) or not 4 <= r["font_size"] <= 96):
            raise ValueError("글자 크기는 4~96입니다")
        if any(k in r and not isinstance(r[k], str) for k in ("source", "label", "text")):
            raise ValueError("값 출처·항목명·고정 값은 문자열입니다")
        if "choices" in r and (not isinstance(r["choices"], list) or any(not isinstance(c, str) for c in r["choices"])):
            raise ValueError("보기는 문자열 목록입니다")
        src = r.get("source")
        if src:
            if key in sources and sources[key] != (src, r.get("text"), r.get("choices")):
                raise ValueError("같은 키의 값 출처는 같아야 합니다")
            sources[key] = (src, r.get("text"), r.get("choices"))
            if src.startswith("profile."):
                try:
                    lookup(make_profile(0), src[len("profile."):])
                except (KeyError, AttributeError, ValueError, IndexError, TypeError):
                    raise ValueError(f"프로필에 없는 출처: {src}") from None
            elif src not in {f"rule:{k}" for k in RULE_KINDS + SPECIAL_RULES}:
                raise ValueError(f"알 수 없는 값 출처: {src}")
    return json.loads(json.dumps(value, ensure_ascii=False))


def save(doc_id: str, value: dict, variant: str = "default") -> dict:
    value = validate(value)
    p = path(doc_id,variant)
    with _lock:
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(p)
    return value


@contextmanager
def draft(doc_id: str, value: dict | None):
    old = getattr(_local, "drafts", {})
    _local.drafts = {**old, **({doc_id: validate(value)} if value is not None else {})}
    try:
        yield
    finally:
        _local.drafts = old


def bindings(config: dict, profile, seed) -> dict:
    from .sources import value

    out = {}
    for r in config["regions"]:
        if r.get("label"):
            out.setdefault(r["key"], {})["label"] = r["label"]
        if r.get("source") and r["key"] not in out:
            out[r["key"]] = {"value": value(r["source"], profile, random.Random(f"html-region:{seed}:{r['key']}"), r), "label": r.get("label")}
        elif r.get("source") and "value" not in out[r["key"]]:
            out[r["key"]]["value"] = value(r["source"], profile, random.Random(f"html-region:{seed}:{r['key']}"), r)
    return out


def attach(html: str, config: dict, rec, profile=None, seed=0) -> str:
    from markupsafe import escape
    from .render import scribble

    additions = {}
    mark_art = {}
    for r in config["regions"]:
        key = r["key"]
        if r.get("target") == "box":
            continue
        if r.get("target") == "mark":
            field = rec.fields.get(key)
            if field is None:
                typ = r.get("mark_type", "signature" if key.startswith("sign.") else "seal")
                field = rec.fields[key] = {"key": key, "type": typ, "label": r.get("label") or "추가 날인·서명", "present": True, "value": None}
            if field.get("type") not in ("seal", "signature"):
                raise ValueError(f"도장·서명 키가 아닙니다: {key}")
            present = r.get("present", field.get("present", False)) and not r.get("drop")
            text = (getattr(rec, "bindings", {}).get(key) or {}).get("value", field.get("value"))
            text = str(text or (profile.person.name if profile else "서명"))
            field.update(present=present, value=text if present else None, label=r.get("label") or field.get("label"))
            if not present:
                mark_art[key] = ""
            elif field["type"] == "signature":
                mark_art[key] = str(scribble(text, random.Random(f"region-sign:{seed}:{key}")))
            else:
                radius = "2px" if r.get("shape") == "square" else "50%"
                mark_art[key] = f'<span style="display:flex;box-sizing:border-box;width:100%;height:100%;border:2px solid #b22222;border-radius:{radius};align-items:center;justify-content:center;color:#b22222;font-size:11px;line-height:1.1;text-align:center">{escape(text)}</span>'
            continue
        if key not in rec.fields and not r.get("drop") and r.get("source") and "rect" in r:
            additions[key] = str(rec(key))
    payload = json.dumps({**config, "mark_art": mark_art}, ensure_ascii=False).replace("<", "\\u003c")
    staging = '<div id="docgen-html-added" hidden>' + ''.join(additions.values()) + '</div>'
    return html + staging + '<script type="application/json" id="docgen-html-regions">' + payload + '</script>'
