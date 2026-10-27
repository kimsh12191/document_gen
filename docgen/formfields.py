"""서식의 칸 목록 fields.json (서식 폴더, docgen/formdir.py). 사람이 고치는 곳은 이 파일 하나다.

overlay 서식 (hf###, img_*)
  {"engine": "overlay", "unit": "pt",
   "pages": [{"width", "height", "bank"?, "staff": [{"role", "rect"}]}],    쪽 크기·결재란 칸
   "items": [{"t", "page", "label", "rect"|"options"|"parts"|"mark", "key"?, "kind"?, "source"?, …,
              "edited"?: true, "added"?: true}],                             기재 자리 (순서대로 키 번호가 붙는다)
   "erase": [{"page", "rect", "fill"}], "marks": {...},                      배경 지우기·표시 설정
   "confirmed_erase"?, "updated"?,                                           기록
   그 밖의 칸(name, class, no, file, texts …)은 자동 추출 레이아웃에서 그대로}

- 처음 한 번 자동 추출 레이아웃(layout.json)과 예전 사람 수정(regions.json)을 합쳐 만든다 (overrides.freeze,
  python -m docgen.formdir migrate). 그 뒤로는 이것이 기준이고 layout.json 은 자동 초안으로만 남는다.
- studio 영역 편집기는 고친 것을 overrides 꼴(match·set·add·erase)로 보내고, 서버가 이 파일에 바로 합쳐 쓴다.
"""
from __future__ import annotations

import json
import threading
from pathlib import Path

NAME = "fields.json"
UNIT = {"overlay": "pt", "html": "px"}
_lock = threading.Lock()


def path(doc_id: str) -> Path:
    from . import formdir

    return formdir.home(doc_id) / NAME


def read(doc_id: str) -> dict | None:
    """칸 목록 (engine·unit 칸 뺀 것). 아직 없으면 None."""
    p = path(doc_id)
    if not p.exists():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    from .regions import engine

    want = engine(doc_id)
    if data.get("engine") not in (None, want):
        raise ValueError(f"{doc_id} 는 {want} 서식인데 {p} 는 {data.get('engine')} 칸 목록입니다")
    return {k: v for k, v in data.items() if k not in ("engine", "unit")}


def hash_files(doc_id: str) -> list[Path]:
    """서식 해시에 넣을 칸 목록 (있을 때만 — 없는 서식은 해시가 예전 그대로)."""
    p = path(doc_id)
    return [p] if p.exists() else []


def exists(doc_id: str) -> bool:
    return path(doc_id).exists()


def write(doc_id: str, body: dict) -> Path:
    from .regions import engine

    eng = engine(doc_id)
    p = path(doc_id)
    with _lock:
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps({"engine": eng, "unit": UNIT[eng], **{k: v for k, v in body.items() if k not in ("engine", "unit")}},
                                  ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        tmp.replace(p)
    return p
