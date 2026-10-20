"""overlay 영역 편집기의 서버 쪽: 레이아웃 보기, 사람 수정 저장, 검수 전 자동 검사.

화면은 사람 수정(docgen/forms/overrides/<ID>.json)을 그대로 들고 고친 뒤 통째로 저장한다. 여기서는
  - 자동 추출 영역마다 id·match·상태(자동/수정/뺌)를 붙여 보여 주고 (docgen/overrides.py 와 같은 규칙)
  - 저장할 때 형식을 검사하고
  - 검수 버튼을 누를 때 보여 줄 경고(한글 키, 겹침, 깨진 수정, 값이 안 채워지는 칸)를 만든다.
좌표는 모두 레이아웃과 같은 PDF pt. 배경 그림은 pt × 2.667(BG_ZOOM) 픽셀이다.
"""
from __future__ import annotations

import copy
import re

from docgen import overrides as OV
from docgen import realform as RF
from docgen import sources as SRC
from docgen.registry import load_all

ITEM_TYPES = ("text", "check", "date", "sign", "copy", "staff")
ADDABLE = ("text", "check", "sign", "copy", "staff")
VALUE_KINDS = ["text"] + [k for k, _ in RF.KIND_RULES if k not in ("skip",)]
_ASCII = re.compile(r"^[A-Za-z0-9_.{}]+$")


def _overlay(doc_id: str):
    spec = load_all().get(doc_id)
    if spec is None:
        raise KeyError(doc_id)
    if spec.group not in ("hana", "imported"):
        raise ValueError("영역 편집기는 overlay 서식만 씁니다 (html 서식은 html 편집기)")
    return spec


def _rect_of(it: dict) -> list[float] | None:
    """영역의 대표 사각형 (목록·겹침 검사용)."""
    if it.get("rect"):
        return it["rect"]
    if it["t"] == "check" and it.get("options"):
        os_ = it["options"]
        return [min(o["rect"][0] for o in os_), min(o["rect"][1] for o in os_),
                max(o["rect"][2] for o in os_), max(o["rect"][3] for o in os_)]
    if it["t"] == "date" and it.get("parts"):
        ps = it["parts"].values()
        return [min(p[0] for p in ps), min(p[1] for p in ps), max(p[2] for p in ps), max(p[3] for p in ps)]
    if it["t"] == "sign" and it.get("mark"):
        m = it["mark"]
        if it.get("name"):
            n = it["name"]
            return [min(m[0], n[0]), min(m[1], n[1]), max(m[2], n[2]), max(m[3], n[3])]
        return m
    return None


def _auto(it: dict) -> dict:
    """자동 규칙이 이 영역에 붙이는 키·값 종류 (사람이 바꾸기 전)."""
    label = it.get("label") or ""
    if it["t"] == "text":
        if it.get("row"):
            return {"key": None, "kind": RF.kind_of(label, it.get("unit"), it.get("hint")), "row": True}
        return {"key": RF.key_of(label), "kind": RF.kind_of(label, it.get("unit"), it.get("hint"))}
    return {"key": None, "kind": None}


def _public(it: dict) -> dict:
    keep = ("t", "page", "label", "rect", "options", "parts", "mark", "name", "text", "unit", "row", "group", "section",
            "pick", "key", "kind", "source", "choices", "note")
    return {k: copy.deepcopy(it[k]) for k in keep if k in it}


def layout_view(doc_id: str) -> dict:
    _overlay(doc_id)
    raw = RF.raw_layout(doc_id)
    ov = OV.load(doc_id)
    by_id = {OV.item_id({"n": 0, **o["match"]}): o for o in ov.get("items", [])}
    items = []
    for it, m in OV.matches(raw):
        iid = OV.item_id(m)
        o = by_id.get(iid)
        merged = {**_public(it), **copy.deepcopy((o or {}).get("set", {}))}
        for k in ("key", "kind", "source", "choices", "text", "note"):
            if o and o.get(k) not in (None, ""):
                merged[k] = o[k]
        status = "auto" if not o else "dropped" if o.get("drop") else "edited"
        items.append({"id": iid, "match": m, "status": status, "auto": _auto(it), "base_raw": _public(it), **merged})
    for k, a in enumerate(ov.get("add", [])):
        items.append({"id": f"add:{k}", "status": "added", "auto": {"key": None, "kind": None}, **_public(a)})
    found = {OV.item_id(m) for _, m in OV.matches(raw)}
    broken = [o for o in ov.get("items", []) if OV.item_id({"n": 0, **o["match"]}) not in found]
    pages = [{"w": pg["width"], "h": pg["height"]} for pg in raw["pages"]]
    return {"doc_id": doc_id, "name": raw.get("name"), "pages": pages, "scale": RF.BG_ZOOM, "items": items,
            "overrides": ov, "broken": broken, "kinds": VALUE_KINDS, "item_types": ITEM_TYPES, "addable": ADDABLE}


def _box(v, name: str) -> list[float]:
    if not (isinstance(v, list) and len(v) == 4 and all(isinstance(x, (int, float)) for x in v)):
        raise ValueError(f"{name}: [x0, y0, x1, y1] 숫자 넷이어야 합니다")
    x0, y0, x1, y1 = (round(float(x), 1) for x in v)
    if x1 <= x0 or y1 <= y0:
        raise ValueError(f"{name}: 크기가 0 입니다")
    return [x0, y0, x1, y1]


def _check_key(key: str | None, where: str):
    if key and not _ASCII.match(key):
        raise ValueError(f"{where}: 키는 영어·숫자·밑줄·점으로 씁니다 ({key!r})")


def _check_source(src: str | None, where: str):
    if not src:
        return
    if src.startswith("profile."):
        return
    if src.startswith("rule:") and src[5:] in SRC.RULE_KINDS + SRC.SPECIAL_RULES:
        return
    raise ValueError(f"{where}: 알 수 없는 값 출처 {src!r}")


def validate(doc_id: str, ov: dict) -> dict:
    """저장 전 형식 검사. 고친 사본을 돌려준다 (숫자 반올림, 빈 칸 정리)."""
    _overlay(doc_id)
    raw = RF.raw_layout(doc_id)
    n_pages = len(raw["pages"])
    out: dict = {}
    items = []
    for i, o in enumerate(ov.get("items", [])):
        m = o.get("match") or {}
        if m.get("t") not in ITEM_TYPES or not isinstance(m.get("page"), int):
            raise ValueError(f"수정 {i + 1}: match 에 page·t 가 필요합니다")
        o = {k: v for k, v in o.items() if v not in (None, "", [], {})}
        o["match"] = {"page": m["page"], "t": m["t"], "label": m.get("label") or "", "n": int(m.get("n", 0))}
        if "set" in o and "rect" in o["set"]:
            o["set"]["rect"] = _box(o["set"]["rect"], f"수정 {i + 1} rect")
        _check_key(o.get("key"), f"수정 {i + 1}")
        _check_source(o.get("source"), f"수정 {i + 1}")
        if len(o) > 1:
            items.append(o)
    adds = []
    for i, a in enumerate(ov.get("add", [])):
        a = {k: v for k, v in a.items() if v not in (None, "", [], {})}
        if a.get("t") not in ADDABLE:
            raise ValueError(f"추가 {i + 1}: 종류는 {ADDABLE} 중 하나")
        if not isinstance(a.get("page"), int) or not 0 <= a["page"] < n_pages:
            raise ValueError(f"추가 {i + 1}: 쪽 번호가 틀렸습니다")
        if a["t"] == "check":
            if not a.get("options"):
                raise ValueError(f"추가 {i + 1}: 체크박스는 보기(options)가 하나 이상 필요합니다")
            for j, op in enumerate(a["options"]):
                op["box"] = _box(op.get("box"), f"추가 {i + 1} 보기 {j + 1} □")
                op["rect"] = _box(op.get("rect") or op["box"], f"추가 {i + 1} 보기 {j + 1}")
                op["text"] = op.get("text") or f"보기{j + 1}"
        elif a["t"] == "sign":
            a["mark"] = _box(a.get("mark") or a.get("rect"), f"추가 {i + 1} 서명 자리")
            a.pop("rect", None)
            if a.get("name"):
                a["name"] = _box(a["name"], f"추가 {i + 1} 이름 자리")
        else:
            a["rect"] = _box(a.get("rect"), f"추가 {i + 1}")
        if a["t"] == "copy" and not a.get("text"):
            raise ValueError(f"추가 {i + 1}: 자필 기재란은 따라 쓸 문구(text)가 필요합니다")
        _check_key(a.get("key"), f"추가 {i + 1}")
        _check_source(a.get("source"), f"추가 {i + 1}")
        adds.append(a)
    erases = []
    for i, e in enumerate(ov.get("erase", [])):
        if not isinstance(e.get("page"), int) or not 0 <= e["page"] < n_pages:
            raise ValueError(f"지우기 {i + 1}: 쪽 번호가 틀렸습니다")
        erases.append({"page": e["page"], "rect": _box(e.get("rect"), f"지우기 {i + 1}"),
                       "fill": "auto" if e.get("fill") == "auto" else "white"})
    for k, v in (("items", items), ("add", adds), ("erase", erases)):
        if v:
            out[k] = v
    if ov.get("marks"):
        out["marks"] = ov["marks"]
    for k in ("confirmed_erase", "updated"):
        if ov.get(k):
            out[k] = ov[k]
    return out


def save(doc_id: str, ov: dict, by: str = "") -> dict:
    import time

    clean = validate(doc_id, ov)
    if clean:
        clean["updated"] = {"by": by or "studio", "at": time.strftime("%Y-%m-%d %H:%M")}
    OV.save(doc_id, clean)
    return layout_view(doc_id)


# ---------------------------------------------------------------------------
# 검수 전 자동 검사 (경고만, 막지 않는다)
# ---------------------------------------------------------------------------

def _overlap(a, b) -> float:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    small = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1])) or 1
    return inter / small


def _pdf_words(doc_id: str) -> dict[int, list]:
    """원본 PDF 의 인쇄된 글자 (쪽마다 [x0, y0, x1, y1, 글자]). image 서식이면 빈 것."""
    no = RF.form_no(doc_id)
    if no is None:
        return {}
    import pymupdf

    lay = RF.load_layout(no)
    out = {}
    with pymupdf.open(RF.ROOT / lay["file"]) as doc:
        for i, page in enumerate(doc):
            out[i] = [w[:5] for w in page.get_text("words")]
    return out


def checks(doc_id: str, label: dict | None = None, fields_keys: list[dict] | None = None) -> list[dict]:
    """경고 목록 [{level, code, text, id?}]. label: 미리보기 라벨 하나 (한글 키 검사), fields_keys: fields.json 의 키."""
    out = []
    spec = load_all()[doc_id]
    if label is not None:
        kr = sorted({f["key"] for f in label["fields"] if not _ASCII.match(f["key"])})
        if kr:
            out.append({"level": "warn", "code": "korean_key",
                        "text": f"한글 키 {len(kr)}개: {', '.join(kr[:8])}{' …' if len(kr) > 8 else ''}"})
        if label.get("overflow"):
            out.append({"level": "warn", "code": "overflow", "text": "내용이 쪽 밖으로 넘칩니다"})
    if fields_keys:
        empty = [k["key"] for k in fields_keys if k.get("type") not in ("checkbox", "checkbox_multi", "seal", "signature")
                 and not k.get("example")]
        if empty:
            out.append({"level": "info", "code": "never_filled",
                        "text": f"30번 렌더링에서 한 번도 안 채워진 칸 {len(empty)}개: {', '.join(empty[:8])}"
                                f"{' …' if len(empty) > 8 else ''}"})
    if spec.group not in ("hana", "imported"):
        return out
    view = layout_view(doc_id)
    if view["broken"]:
        out.append({"level": "warn", "code": "broken",
                    "text": f"깨진 수정 {len(view['broken'])}개: 레이아웃을 다시 추출해 대상 영역을 못 찾음 "
                            f"({', '.join(o['match'].get('label') or '?' for o in view['broken'][:5])})"})
    live = [it for it in view["items"] if it["status"] != "dropped" and it["t"] in ("text", "copy")]
    for i, a in enumerate(live):
        for b in live[i + 1:]:
            ra, rb = _rect_of(a), _rect_of(b)
            if ra and rb and a["page"] == b["page"] and _overlap(ra, rb) > 0.3:
                out.append({"level": "warn", "code": "overlap", "id": a["id"],
                            "text": f"{a['page'] + 1}쪽: 값 영역 '{a.get('label') or a['id']}'·'{b.get('label') or b['id']}' 이 겹칩니다"})
    try:
        words = _pdf_words(doc_id)
    except Exception:  # noqa: BLE001  PDF 를 못 읽으면 이 검사만 건너뛴다
        words = {}
    printed: dict[tuple, dict] = {}   # 같은 항목명(표의 여러 행)은 한 줄로 모은다
    for it in live:
        r = _rect_of(it)
        if not r or it["t"] != "text":
            continue
        inside = [w[4] for w in words.get(it["page"], [])
                  if r[0] <= (w[0] + w[2]) / 2 <= r[2] and r[1] <= (w[1] + w[3]) / 2 <= r[3]]
        if inside:
            g = printed.setdefault((it["page"], it.get("label") or it["id"]), {"id": it["id"], "n": 0, "words": inside})
            g["n"] += 1
    for (page, label), g in printed.items():
        many = f" ({g['n']}칸)" if g["n"] > 1 else ""
        out.append({"level": "warn", "code": "printed_text", "id": g["id"],
                    "text": f"{page + 1}쪽 '{label}'{many}: 값 영역 안에 인쇄된 글자가 있습니다 "
                            f"({' '.join(g['words'][:6])}) — 안내 문구와 겹치면 영역을 줄이거나 배경을 지우세요"})
    junk = [it for it in live if it["t"] == "text" and it["status"] == "auto" and it.get("label")
            and not _ASCII.match(RF.norm(it["label"])) and len(RF.norm(it["label"])) <= 3 and not it["auto"].get("key")
            and RF.kind_of(it["label"], it.get("unit"), it.get("hint")) == "text"]
    if junk:
        out.append({"level": "info", "code": "fragment",
                    "text": f"뜻을 모르는 짧은 항목명 {len(junk)}개 (문장 조각일 수 있음): "
                            f"{', '.join(it['label'] for it in junk[:8])}"})
    return out
