"""overlay 서식의 사람 수정층: 자동 추출 레이아웃 위에 사람이 고친 것을 덧씌운다 (studio 영역 편집기가 쓴다).

  add_template/overrides/<서식ID>.json        (가져온 이미지 서식 img_* 는 그 서식 폴더의 overrides.json:
                                              실서류에서 만든 서식은 수정도 private_forms_dir 밖으로 나가지 않는다)
  {
    "items": [ {"match": {"page": 0, "t": "text", "label": "직장주소", "n": 0},   자동 추출 영역 고르기
                "set": {"rect": [...]},                                         영역 정보 바꾸기 (rect, options, parts …)
                "key": "employer.address", "kind": "address",                   키·값 종류
                "source": "profile.employment.company.address.road_short",      값 출처 (docgen/sources.py)
                "drop": true, "note": "…"} ],                                   영역 빼기, 메모
    "add":   [ {"t": "text", "page": 1, "label": "비고", "rect": [...], "key": "remark", "source": "rule:free_text"} ],
    "erase": [ {"page": 0, "rect": [...], "fill": "white" | "auto"} ],          배경 지우기 (흰색 / 주변색)
    "marks": {"hand": 1.0}                                                      표시 설정 덮어쓰기 (docgen/marks.py)
  }

- 좌표는 레이아웃과 같은 PDF pt 단위.
- match 는 쪽·종류·항목명과 "같은 항목명 중 몇 번째(n)" 로 고른다. 레이아웃을 다시 추출해 영역 순서가 바뀌어도 같은
  영역을 찾는다. 못 찾은 수정은 broken 으로 돌려준다 (studio 가 "깨진 수정"으로 보여 준다).
- 결재란 칸(쪽 정보의 staff)도 t="staff", label=칸 이름으로 고른다.
- studio 가 저장 전 미리보기를 할 때는 draft() 로 그 렌더링 동안만 파일 대신 쓸 수정을 넘긴다.
"""
from __future__ import annotations

import copy
import hashlib
import json
import threading
import unicodedata
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OVERRIDES = ROOT / "add_template" / "overrides"
_local = threading.local()


def path(doc_id: str) -> Path:
    if doc_id.startswith("img_"):
        from .realform import image_form_dir

        d = image_form_dir(doc_id)
        if d is not None:
            return d / "overrides.json"
    return OVERRIDES / f"{doc_id}.json"


def load(doc_id: str) -> dict:
    """저장된 수정 (미리보기 중이면 그 초안). 없으면 빈 수정."""
    drafts = getattr(_local, "drafts", None)
    if drafts and doc_id in drafts:
        return drafts[doc_id]
    p = path(doc_id)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def save(doc_id: str, ov: dict) -> Path:
    p = path(doc_id)
    ov = {k: v for k, v in ov.items() if v not in (None, [], {})}
    if not ov or not any(ov.get(k) for k in ("items", "add", "erase", "marks")):
        if p.exists():
            p.unlink()
        return p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(ov, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return p


@contextmanager
def draft(doc_id: str, ov: dict):
    """이 스레드에서 렌더링하는 동안 doc_id 의 수정을 ov 로 바꿔 쓴다 (저장하지 않은 미리보기)."""
    drafts = getattr(_local, "drafts", None)
    if drafts is None:
        drafts = _local.drafts = {}
    old = drafts.get(doc_id)
    drafts[doc_id] = ov
    try:
        yield
    finally:
        if old is None:
            drafts.pop(doc_id, None)
        else:
            drafts[doc_id] = old


def digest(ov: dict) -> str:
    return hashlib.sha1(json.dumps(ov, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12] if ov else "-"


def _norm(s: str | None) -> str:
    return "".join(unicodedata.normalize("NFKC", s or "").split())


def matches(lay: dict) -> list[tuple[dict, dict]]:
    """레이아웃의 모든 영역과 그 match 조건. 결재란 칸은 {"t": "staff", "_staff": (쪽, 칸 번호)} 로 넣는다."""
    seen: dict[tuple, int] = {}
    out = []

    def add(item, page, t, label):
        k = (page, t, _norm(label))
        n = seen[k] = seen.get(k, -1) + 1
        out.append((item, {"page": page, "t": t, "label": label or "", "n": n}))

    for it in lay["items"]:
        add(it, it["page"], it["t"], it.get("label"))
    for page, pg in enumerate(lay["pages"]):
        for j, c in enumerate(pg.get("staff", [])):
            add({"t": "staff", "page": page, "label": c["role"], "rect": c["rect"], "_staff": (page, j)}, page, "staff",
                c["role"])
    return out


def item_id(m: dict) -> str:
    return f"{m['page']}:{m['t']}:{_norm(m['label'])}:{m['n']}"


def apply(lay: dict, ov: dict) -> tuple[dict, list[dict]]:
    """레이아웃 사본에 수정을 덧씌운다. (새 레이아웃, 못 찾은 수정 목록)."""
    if not ov:
        return lay, []
    lay = copy.deepcopy(lay)
    found = {item_id(m): (it, m) for it, m in matches(lay)}
    broken, drop_items, drop_staff = [], set(), set()
    for o in ov.get("items", []):
        hit = found.get(item_id({"n": 0, **o["match"]}))
        if hit is None:
            broken.append(o)
            continue
        it, _ = hit
        if it["t"] == "staff":
            page, j = it["_staff"]
            cell = lay["pages"][page]["staff"][j]
            if o.get("drop"):
                drop_staff.add((page, j))
            if o.get("set", {}).get("rect"):
                cell["rect"] = o["set"]["rect"]
            continue
        if o.get("drop"):
            drop_items.add(id(it))
            continue
        it.update(copy.deepcopy(o.get("set", {})))
        for k in ("key", "kind", "source", "choices", "text"):
            if o.get(k) not in (None, ""):
                it[k] = o[k]
        it["edited"] = True
    lay["items"] = [it for it in lay["items"] if id(it) not in drop_items]
    for page, pg in enumerate(lay["pages"]):
        if pg.get("staff"):
            pg["staff"] = [c for j, c in enumerate(pg["staff"]) if (page, j) not in drop_staff]
    for a in ov.get("add", []):
        a = copy.deepcopy(a)
        if a.get("t") == "staff":
            lay["pages"][a["page"]].setdefault("staff", []).append({"role": a.get("label") or "결재", "rect": a["rect"]})
            continue
        a.setdefault("label", "")
        a["added"] = True
        lay["items"].append(a)
    return lay, broken


# ---------------------------------------------------------------------------
# 배경 지우기
# ---------------------------------------------------------------------------

def erase_for(ov: dict, page: int) -> list[dict]:
    return [e for e in ov.get("erase", []) if e.get("page", 0) == page]


def apply_erase(img, erases: list[dict], scale: float):
    """PIL 이미지에 지우기를 적용한 사본. rect 는 pt, scale 은 pt → 이미지 픽셀 배율.
    fill: white(흰색) / auto(사각형 바깥 테두리 픽셀 중 밝은 쪽 = 주변 종이색. 테두리가 표 선에 걸쳐도 선 색을 고르지 않게
    밝기 순으로 95% 자리의 픽셀)."""
    from PIL import ImageDraw

    img = img.convert("RGB").copy()
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for e in erases:
        x0, y0, x1, y1 = (int(round(v * scale)) for v in e["rect"])
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(w, x1), min(h, y1)
        if x1 <= x0 or y1 <= y0:
            continue
        color = (255, 255, 255)
        if e.get("fill") == "auto":
            px = []
            for x in range(max(0, x0 - 2), min(w, x1 + 2)):
                for y in (max(0, y0 - 2), min(h - 1, y1 + 1)):
                    px.append(img.getpixel((x, y)))
            for y in range(max(0, y0 - 2), min(h, y1 + 2)):
                for x in (max(0, x0 - 2), min(w - 1, x1 + 1)):
                    px.append(img.getpixel((x, y)))
            if px:
                px.sort(key=lambda c: c[0] * 299 + c[1] * 587 + c[2] * 114)
                color = px[min(len(px) - 1, int(len(px) * 0.95))]
        draw.rectangle([x0, y0, x1 - 1, y1 - 1], fill=color)
    return img
