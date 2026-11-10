"""서류에 없는 키·열 (정답 null): kie·table 질문의 일부에 섞어 "물어도 없으면 null" 을 배우게 한다.

후보는 같은 그룹(registry group) 다른 서식의 칸 — 서식 카탈로그 guide/fields/fields.json (python docgen/scripts/build_schema.py
가 만드는 자동 생성 파일, 그리지 않고 읽음). 카탈로그가 없으면 후보가 없어 섞지 않는다.
이 서류에 같은 키, 같은 항목명(공백·문장부호 무시), 한쪽이 다른 쪽을 품는 항목명(대출금액 ↔ 대출신청금액)이 있으면
후보에서 뺀다 — 비슷한 칸이 서류에 있으면 null 이 정답인지 흔들리므로. 주민번호로 알 수 있는 생년월일·나이·성별처럼
문서의 다른 값으로 짐작할 수 있는 항목명도 뺀다 (없는 칸이지만 답이 흔들리지 않게).
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[2] / "guide" / "fields" / "fields.json"
MARK = ("checkbox", "checkbox_multi", "seal", "signature")
GUESSABLE = re.compile(r"생년월일|나이|연령|성별|만\d+세")


def _norm(s) -> str:
    return re.sub(r"[^0-9a-z가-힣]", "", str(s or "").lower())


@lru_cache(maxsize=1)
def _catalog(mtime: float) -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def catalog() -> dict:
    try:
        return _catalog(CATALOG.stat().st_mtime)
    except (OSError, ValueError):
        return {}


@lru_cache(maxsize=64)
def _pools(group: str, mtime: float) -> tuple[list, list]:
    """(kie 후보 [(서식, 키, 항목명, 타입)], 열 후보 [(서식, 열, 항목명, 타입)]) — 같은 그룹 서식들, 서식·키 순."""
    keys, cols = [], []
    for form, v in sorted(catalog().items()):
        if v.get("group") != group:
            continue
        for k in v.get("keys") or []:
            key, label, t = k.get("key") or "", k.get("label"), k.get("type") or "text"
            if t in MARK or key.startswith(("seal.", "sign.")) or not label or GUESSABLE.search(label):
                continue
            if "[]" in key:
                if key.count("[]") == 1:
                    col = key.split("[].", 1)[1] if "[]." in key else "value"
                    cols.append((form, col, label, t))
            else:
                keys.append((form, key, label, t))
    return keys, cols


def pools(group: str) -> tuple[list, list]:
    try:
        return _pools(group, CATALOG.stat().st_mtime)
    except OSError:
        return [], []


def _near(label: str, labels: set) -> bool:
    """항목명이 서류의 항목명과 같거나 한쪽이 다른 쪽을 품는지 (두 글자 이상)."""
    n = _norm(label)
    return n in labels or any(len(x) >= 2 and len(n) >= 2 and (x in n or n in x) for x in labels)


def _taken(doc) -> tuple[set, set]:
    keys = {f["key"] for f in doc.fields}
    labels = {_norm(f.get("label")) for f in doc.fields if f.get("label")}
    return keys, labels


def absent_keys(doc, n: int) -> list[dict]:
    """kie 에 섞을 없는 칸 n 개 (doc.rng 로 고름): [{"key", "label", "type", "value": None, "_absent": 서식}]."""
    pool, _ = pools(doc.r["group"])
    keys, labels = _taken(doc)
    cand, seen = [], set()
    for form, key, label, t in pool:
        if form == doc.r["doc_id"] or key in keys or _near(label, labels):
            continue
        if key in seen or _norm(label) in seen:
            continue
        seen.update((key, _norm(label)))
        cand.append({"key": key, "label": label, "type": t, "value": None, "_absent": form})
    if not cand:
        return []
    return doc.rng.sample(cand, min(n, len(cand)))


def absent_column(doc, group: str, cols: list[tuple[str, dict]]) -> dict | None:
    """table 에 섞을 없는 열 하나: {"key", "label", "type"} 또는 None. 이 표의 열 키·항목명, 서류의 항목명과 겹치지 않게."""
    _, pool = pools(doc.r["group"])
    have = {c for c, _ in cols}
    _, labels = _taken(doc)
    labels |= {_norm(f.get("label")) for _, f in cols}
    cand, seen = [], set()
    for form, col, label, t in pool:
        if form == doc.r["doc_id"] or col in have or (col, _norm(label)) in seen or _near(label, labels):
            continue
        seen.add((col, _norm(label)))
        cand.append({"key": col, "label": label, "type": t})
    return doc.rng.choice(cand) if cand else None
