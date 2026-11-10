"""칸마다 "이 칸은 fields.json 의 어디이고, 키·값이 어디서 정해지나" (서식 카드·질문 설정이 같이 쓴다).

  entries(doc_id) → {서식의 키(반복 행은 *, 이름 통일): {"where": "fields.json:61" | None, "key_from": 설명, "value_from": 설명,
                                               "q": 칸의 질문 설정 | None, "ref": ("items", i) | ("fields", 키) | ("lists", 이름, 칸)}}

질문 설정 q 는 칸 줄 안에 ("q": {...}). html·코드 서식에서 칸 목록에 줄이 없는 칸(부모 서식이 값을 만드는 복제 서식, 체크·도장 …)은
fields.json 맨 위 "q" 묶음에 키로 적는다: "q": {"special_terms.*": {"ask": false}}. 둘 다 생성(값)에는 쓰이지 않는다.

원본 서식(overlay)의 키·값 종류는 규칙(키 사전 key_rules.json)이 항목명으로 정한다. 칸에 "key"·"kind"·"source" 를 적으면
그 칸만 규칙 대신 그것을 쓴다 — 여기서는 어느 쪽인지 알려 준다 (규칙은 studio 키 사전 화면에서 고치면 모든 서식에 반영).
"""
from __future__ import annotations

import json
import re

_cache: dict = {}


def pattern(key: str) -> str:
    """반복 행 번호는 *, 마지막 이름은 그린 칸과 같게 통일 (schema.canonical_key: dob → birth …)."""
    from .schema import canonical_key

    return re.sub(r"(?<=\.)\d+(?=\.|$)", "*", canonical_key(key))


def _item_lines(text: str) -> list[int]:
    """fields.json(indent 1) 의 items 목록에서 칸마다 시작 줄 번호 (1부터)."""
    lines = text.splitlines()
    try:
        start = next(i for i, ln in enumerate(lines) if ln.startswith(' "items": ['))
    except StopIteration:
        return []
    out = []
    for i in range(start + 1, len(lines)):
        if lines[i].startswith(" ]"):
            break
        if lines[i] == "  {":
            out.append(i + 1)
    return out


def _key_line(text: str, needle: str, after: int = 0) -> int | None:
    for n, line in enumerate(text.splitlines(), 1):
        if n > after and needle in line:
            return n
    return None


def entries(doc_id: str) -> dict[str, dict]:
    from . import formfields
    from .registry import load_all

    p = formfields.path(doc_id)
    if not p.exists():
        return {}
    spec = load_all()[doc_id]
    stamp = (doc_id, p.stat().st_mtime_ns, _rules_stamp())
    hit = _cache.get(doc_id)
    if hit and hit[0] == stamp:
        return hit[1]
    text = p.read_text(encoding="utf-8")
    out = _overlay(doc_id, text) if spec.template == "_real_form.html.j2" else _declared(doc_id, text, spec)
    _cache[doc_id] = (stamp, out)
    return out


def _rules_stamp():
    from .keyrules import PATH

    try:
        return PATH.stat().st_mtime_ns
    except OSError:
        return 0


def _declared(doc_id: str, text: str, spec) -> dict:
    """html·코드 서식: fields.json 의 fields·lists (적은 칸만). 키는 템플릿 f("키") 가 정한다."""
    body = json.loads(text)
    code = not spec.template.startswith("@")
    out = {}
    fields_at = _key_line(text, '"fields": {') or 0
    for key, d in (body.get("fields") or {}).items():
        src = d.get("source")
        out[pattern(key)] = {"where": f"fields.json:{_key_line(text, json.dumps(key, ensure_ascii=False) + ':', fields_at) or '?'}",
                    "key_from": "템플릿 f(\"키\")", "value_from": _value(src, code), "q": d.get("q"), "ref": ("fields", key)}
    lists_at = _key_line(text, '"lists": {') or 0
    for name, lst in (body.get("lists") or {}).items():
        at = _key_line(text, json.dumps(name, ensure_ascii=False) + ":", lists_at) or lists_at
        for sub, d in (lst.get("fields") or {}).items():
            out[pattern(f"{name}.0.{sub}")] = {"where": f"fields.json:{_key_line(text, json.dumps(sub, ensure_ascii=False) + ':', at) or '?'}",
                                      "key_from": "템플릿 f(\"키\")", "value_from": _value(d.get("source"), code),
                                      "q": d.get("q"), "ref": ("lists", name, sub)}
    q_at = _key_line(text, '"q": {') or 0   # 맨 위 "q" 묶음: 칸 목록에 줄이 없는 칸(부모 서식 값·체크·도장 …)의 질문 설정
    for key, q in (body.get("q") or {}).items():
        k = pattern(key)
        e = out.setdefault(k, {"where": None, "key_from": "템플릿 f(\"키\")", "value_from": _value(None, code), "q": None,
                               "ref": ("q", key)})
        e["q"] = {**q, **(e.get("q") or {})} if isinstance(q, dict) else q
        e["q_where"] = f"fields.json:{_key_line(text, json.dumps(key, ensure_ascii=False) + ':', q_at) or '?'}"
    return out


def _value(src: str | None, code: bool) -> str:
    if code and src in (None, "code"):
        return "generate.py"
    return f"`{src}`" if src else "-"


def _overlay(doc_id: str, text: str) -> dict:
    """원본 서식: fields.json 의 items. 칸마다 키·값이 규칙인지 파일인지."""
    from . import realform as RF

    lay, _ = RF.form_layout(doc_id)
    keys = RF.layout_keys(doc_id)
    lines = _item_lines(text)
    by_id = {it.get("_id"): (i, it) for i, it in enumerate(lay["items"])}
    out = {}
    for iid, info in keys.items():
        if iid not in by_id:
            continue   # 결재란 칸
        i, it = by_id[iid]
        where = f"fields.json:{lines[i]}" if i < len(lines) else "fields.json"
        label = it.get("label") or ""
        t = it["t"]
        if t == "text" and it.get("row"):
            key_from = "파일 key" if it.get("key") else f"표 행 (묶음·키 설명 '{label}')"
            kind = it.get("kind") or "text"
            value_from = f"`{it['source']}` (파일)" if it.get("source") else f"값 종류 `{kind}`"
        elif t == "text":
            skey, kind = RF._text_key(it)
            key_from = "파일 key" if it.get("key") else "키 설명 그대로"
            if it.get("source"):
                value_from = f"`{it['source']}` (파일)"
            elif skey and kind != "seal" and it.get("std", True):
                value_from = f"고객 정보 (키 `{skey}`, 없으면 값 종류 `{kind}`)"
            else:
                value_from = f"값 종류 `{kind}`"
        elif t == "check":
            key_from = "파일 key" if it.get("key") else "체크 (키 설명)"
            value_from = "보기 중 고름: " + " / ".join(o.get("text") or "?" for o in it.get("options", []))
        elif t == "date":
            key_from, value_from = ("파일 key" if it.get("key") else "date"), "작성일"
        elif t == "sign":
            key_from, value_from = ("파일 key" if it.get("key") else "서명 자리"), "도장·서명 (표시 확률 marks.json)"
        else:
            key_from, value_from = ("파일 key" if it.get("key") else t), t
        for k in info["keys"]:
            out.setdefault(pattern(k), {"where": where, "key_from": key_from, "value_from": value_from,
                                        "q": it.get("q"), "ref": ("items", i)})
    return out


def questions(doc_id: str) -> dict[str, dict]:
    """칸마다 질문 설정 q ({ask?, label?, note?, ocr?}) — 적은 칸만. 키는 서식의 키(반복 행은 *)."""
    return {k: e["q"] for k, e in entries(doc_id).items() if e.get("q")}


Q_KEYS = {"ask": bool, "label": str, "note": str, "ocr": bool}


def check_q(doc_id: str) -> list[str]:
    """칸 목록에 적은 q 의 형식 문제."""
    bad = []
    for k, e in entries(doc_id).items():
        q = e.get("q")
        if q is None:
            continue
        if not isinstance(q, dict):
            bad.append(f"{e.get('q_where') or e['where']} ({k}): q 는 {{\"ask\", \"label\", \"note\", \"ocr\"}} 객체여야 합니다")
            continue
        for x, v in q.items():
            if x not in Q_KEYS:
                bad.append(f"{e.get('q_where') or e['where']} ({k}): q 에 모르는 칸 '{x}' (쓸 수 있는 것: {', '.join(Q_KEYS)})")
            elif not isinstance(v, Q_KEYS[x]):
                bad.append(f"{e.get('q_where') or e['where']} ({k}): q.{x} 는 {'true/false' if Q_KEYS[x] is bool else '글자'}")
    return bad


def doc_key_of(f: dict) -> str:
    """그린 칸의 서식 키 (반복 행은 *)."""
    return pattern(f["key"])
