"""문서 하나를 쪽 단위로 나누고, 쪽마다의 정답·앞 쪽 상태·질문 문장을 만들고, 쪽 단위 답을 문서로 다시 합친다.

문서 내용 표현 (정답과 모델 답 모두 같은 모양):
    {"fields": {중첩 항목: 값}, "lists": {"rows": [행, ...], "summary.owners": [행, ...]}}
목록은 키에 숫자 칸이 처음 나오는 곳까지가 목록 이름이다. 'gapgu.3.holders.1.name' → 목록 'gapgu', 3번 행의 'holders.1.name'.
"""
from __future__ import annotations

import json

STATES = ("none", "doc", "tail", "context")

# 앞 쪽 상태(context)에 넣는 문서 단위 정보. 뒤쪽 행을 해석하는 데 필요한 것만.
CONTEXT_KEYS = {
    "bank_statement": ["holder", "account_no", "period", "opening_balance"],
    "real_estate_registry": ["property", "unique_no"],
    "resident_registration_copy": ["household_head.name", "current_address.address"],
    "commercial_invoice": ["invoice_no", "shipper.name", "consignee.name"],
    "packing_list": ["invoice_no", "shipper.name", "consignee.name"],
    "financial_statements": ["company_name", "unit", "current_term", "prior_term"],
}

P_PAGE = (
    "여러 서류가 섞인 서류 묶음을 한 쪽씩 읽고 있습니다.\n"
    "앞 쪽까지 정리한 내용: {state}\n\n"
    "이 쪽이 어떤 서류의 몇 쪽인지, 앞 쪽 서류에서 이어지는 쪽인지 판단하고, 이 쪽에 적힌 내용만 JSON 으로 답하세요.\n"
    '형식: {{"document": {{"type": "서류ID", "name": "서류명", "page": 서류 안 쪽 번호, "continues": 앞 쪽에서 이어지면 true}}, '
    '"fields": {{"항목": "값"}}, "lists": {{"목록 이름": [이 쪽의 행을 위에서부터]}}}}\n'
    "값은 적힌 그대로 옮기고, 이 쪽에 없는 항목과 행은 쓰지 마세요."
)
P_ALL = (
    "서류 묶음입니다 (이미지 {n}장, 순서대로 1~{n}쪽). 묶음에 든 서류를 모두 찾아, 서류마다 종류, 묶음 안 쪽 번호, 내용을 JSON 으로 답하세요.\n"
    '형식: {{"documents": [{{"type": "서류ID", "name": "서류명", "pages": [쪽 번호, ...], '
    '"fields": {{"항목": "값"}}, "lists": {{"목록 이름": [행, ...]}}}}]}}\n'
    "값은 적힌 그대로 옮기세요."
)
NO_STATE = "없음"


def split_key(key: str):
    """('목록 이름', 행 번호, 행 안의 키) 또는 목록이 아니면 (None, None, key)."""
    parts = key.split(".")
    for i, p in enumerate(parts):
        if p.isdigit():
            return ".".join(parts[:i]), int(p), ".".join(parts[i + 1:])
    return None, None, key


def leaf(f: dict):
    """정답 값: 도장·서명은 있는지(bool), 나머지는 적힌 글자 (docgen.render._gt_value 와 같음)."""
    return f.get("present") if f.get("type") in ("seal", "signature") else f.get("value")


def nest(flat: dict) -> dict:
    """{'a.b': 1, 'c.0.d': 2} → {'a': {'b': 1}, 'c': [{'d': 2}]}"""
    root: dict = {}
    for key, value in flat.items():
        parts = key.split(".")
        cur = root
        for i, part in enumerate(parts):
            last = i == len(parts) - 1
            nxt_list = not last and parts[i + 1].isdigit()
            if isinstance(cur, list):
                idx = int(part)
                while len(cur) <= idx:
                    cur.append(None)
                if last:
                    cur[idx] = value
                else:
                    if cur[idx] is None:
                        cur[idx] = [] if nxt_list else {}
                    cur = cur[idx]
            else:
                if last:
                    cur[part] = value
                else:
                    if not isinstance(cur.get(part), (dict, list)):
                        cur[part] = [] if nxt_list else {}
                    cur = cur[part]
    return root


def flatten(obj, prefix: str = "") -> dict:
    """nest 의 반대. 잎(문자열·숫자·bool·None)만."""
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, f"{prefix}{k}."))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(flatten(v, f"{prefix}{i}."))
    elif prefix:
        out[prefix[:-1]] = obj
    return out


def _fields(label: dict):
    return [f for f in label["fields"] if not (f.get("group") or f.get("group_only"))]


def page_views(label: dict) -> list[dict]:
    """쪽마다 {'fields': {평탄 키: 값}, 'lists': {목록: [(행 번호, {행 안 키: 값})]}}. 행은 칸이 처음 나온 쪽에 둔다."""
    n = max(1, len(label.get("pages") or [None]))
    views = [{"fields": {}, "lists": {}} for _ in range(n)]
    rows: dict[tuple, dict] = {}
    for f in _fields(label):
        path, idx, rest = split_key(f["key"])
        page = min(f.get("page", 0) or 0, n - 1)
        if path is None:
            views[page]["fields"][f["key"]] = leaf(f)
            continue
        r = rows.setdefault((path, idx), {"page": page, "cells": {}})
        r["page"] = min(r["page"], page)
        r["cells"][rest] = leaf(f)
    for (path, idx), r in sorted(rows.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        views[r["page"]]["lists"].setdefault(path, []).append((idx, r["cells"]))
    return views


def doc_content(views: list[dict]) -> dict:
    """쪽들을 합친 문서 전체 내용 (정답)."""
    fields, lists = {}, {}
    for v in views:
        fields.update(v["fields"])
        for path, rows in v["lists"].items():
            lists.setdefault(path, []).extend(nest(cells) for _, cells in rows)
    return {"fields": nest(fields), "lists": lists}


def page_answer(label: dict, views: list[dict], k: int) -> dict:
    """k 쪽(0부터)의 정답 답변."""
    v = views[k]
    return {"document": {"type": label["doc_type"], "name": label["doc_name"], "page": k + 1, "continues": k > 0},
            "fields": nest(v["fields"]),
            "lists": {path: [nest(cells) for _, cells in rows] for path, rows in v["lists"].items()}}


# ---------------------------------------------------------------------------
# 앞 쪽 상태와 병합
# ---------------------------------------------------------------------------

def merge_pages(outputs: list) -> list[dict]:
    """쪽 단위 답(파싱된 dict, 실패면 None)을 순서대로 합쳐 문서 목록으로. 쪽 번호는 1부터.

    'continues' 가 참이고 앞 문서와 종류가 같으면 이어 붙이고, 아니면 새 문서를 연다.
    """
    docs: list[dict] = []
    for i, o in enumerate(outputs, 1):
        o = o if isinstance(o, dict) else {}
        d = o.get("document") if isinstance(o.get("document"), dict) else {}
        typ = d.get("type")
        if not (d.get("continues") is True and docs and docs[-1]["type"] == typ):
            docs.append({"type": typ, "name": d.get("name"), "pages": [], "_flat": {}, "lists": {}})
        cur = docs[-1]
        cur["pages"].append(i)
        for k, v in flatten(o.get("fields") or {}).items():
            cur["_flat"].setdefault(k, v)
        lists = o.get("lists") if isinstance(o.get("lists"), dict) else {}
        for path, rows in lists.items():
            if isinstance(rows, list):
                cur["lists"].setdefault(path, []).extend(r for r in rows if isinstance(r, dict))
    for d in docs:
        d["fields"] = nest(d.pop("_flat"))
    return docs


def build_state(doc: dict | None, kind: str) -> dict | None:
    """앞 쪽까지 열려 있는 문서(merge_pages 의 마지막 문서 모양)로 다음 쪽에 넘길 상태."""
    if kind == "none" or not doc:
        return None
    state = {"document": {"type": doc.get("type"), "name": doc.get("name"), "pages_read": len(doc.get("pages", []))}}
    if kind in ("tail", "context"):
        tail = {path: {"count": len(rows), "last": rows[-1]} for path, rows in doc.get("lists", {}).items() if rows}
        if tail:
            state["lists"] = tail
    if kind == "context":
        flat = flatten(doc.get("fields") or {})
        ctx = {k: flat[k] for k in CONTEXT_KEYS.get(doc.get("type"), []) if flat.get(k) not in (None, "")}
        if ctx:
            state["context"] = ctx
    return state


def page_prompt(state: dict | None) -> str:
    return P_PAGE.format(state=NO_STATE if state is None else json.dumps(state, ensure_ascii=False))


def all_prompt(n_pages: int) -> str:
    return P_ALL.format(n=n_pages)


def run_pagewise(answer_fn, n_pages: int, state_kind: str):
    """answer_fn(page_index, prompt) → (원문, 파싱된 dict 또는 None). 앞 쪽 답으로 상태를 만들며 차례로 읽는다."""
    raws, parsed = [], []
    for i in range(n_pages):
        docs = merge_pages(parsed) if parsed else []
        state = build_state(docs[-1] if docs else None, state_kind)
        raw, obj = answer_fn(i, page_prompt(state))
        raws.append(raw)
        parsed.append(obj)
    return raws, merge_pages(parsed)
