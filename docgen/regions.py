"""서식 수정 파일: 서식 하나 = 파일 하나 = 서식 폴더의 regions.json (docgen/formdir.py).

  공개 서식 (저장소)             docgen/forms/<ID>/regions.json
  사내 서식 (실서류에서 만든 것) $DOCGEN_PRIVATE_FORMS/<ID>/regions.json   (수정도 저장소 밖에 둔다)

  overlay 서식 (hf###, img_*)  예전 사람 수정 {"engine": "overlay", "unit": "pt", "items": [...], "add": [...], "erase": [...]}
                                지금은 칸 목록 fields.json 이 기준이다 (docgen/formfields.py). 이 파일은 칸 목록을 만들 때
                                합쳐지고 <이름>.migrated 가 된다 (docgen/overrides.py freeze)
  html 서식                     {"engine": "html", "unit": "px", "regions": [...],
                                 "variants": {"<레이아웃 변형 ID>": {"regions": [...]}}}
                                내용은 docgen/html_regions.py. html 서식은 템플릿이 칸을 만들고, 이 파일은 그 위의 수정층
                                (템플릿 칸을 key 로 집어 위치·값·항목명을 바꾸거나 drop, 새 칸 추가).

예전 위치(forms/regions/<ID>.json, <사내 폴더>/regions/<ID>.json, forms/overrides/<ID>.json,
forms/html_regions/<ID>.json, 이미지 서식 폴더의 overrides.json, 레이아웃 변형 폴더의 <변형>.regions.json)는
새 파일이 없을 때만 읽는다. 저장하면 새 파일로 쓰고 예전 파일은 <이름>.migrated 로 바꿔 둔다.
한꺼번에 옮기기: python -m docgen.formdir migrate [--apply] (서식 파일과 함께) 또는 python -m docgen.regions migrate.

  python -m docgen.regions path <ID>          이 서식의 수정 파일 위치 (예전 파일이 남았으면 함께)
  python -m docgen.regions show <ID>          최종 칸 목록 (자동 추출·템플릿 칸 + 수정)
  python -m docgen.regions check [<ID>…|--all] 형식·종류·깨진 수정·예전 파일 검사
  python -m docgen.regions migrate [--apply]  예전 파일을 새 파일로 (기본은 목록만)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import threading
from pathlib import Path

DOCGEN = Path(__file__).resolve().parent
LEGACY_OVERLAY = DOCGEN / "forms" / "overrides"
LEGACY_HTML = DOCGEN / "forms" / "html_regions"
UNIT = {"overlay": "pt", "html": "px"}
BODY = {"overlay": ("items", "add", "erase", "marks"), "html": ("regions", "variants")}   # 수정 내용 (이게 다 비면 파일을 지운다)
EXTRA = {"overlay": ("confirmed_erase", "updated"), "html": ("updated",)}                 # 내용과 함께 두는 기록
_lock = threading.Lock()


# ---------------------------------------------------------------------------
# 위치
# ---------------------------------------------------------------------------

def engine(doc_id: str) -> str:
    """overlay | html. 등록 전 서식(가져오는 중인 img_*)도 ID 모양으로 안다."""
    if re.fullmatch(r"hf\d{3}", doc_id) or doc_id.startswith("img_"):
        return "overlay"
    from .registry import load_all

    spec = load_all().get(doc_id)
    if spec is None:
        raise KeyError(f"모르는 서식: {doc_id}")
    return "overlay" if spec.template == "_real_form.html.j2" else "html"


def path(doc_id: str) -> Path:
    from . import formdir

    return formdir.home(doc_id) / "regions.json"


def _private_home(doc_id: str) -> Path | None:
    """사내 폴더의 서식이면 그 사내 폴더."""
    from . import formdir

    for r in formdir.private_roots():
        if (r / doc_id).is_dir():
            return r
    return None


def _gen2(doc_id: str) -> Path:
    """바로 전 자리: docgen/forms/regions/<ID>.json (사내 서식은 <사내 폴더>/regions/<ID>.json)."""
    from . import formdir

    r = _private_home(doc_id)
    return (r / "regions" / f"{doc_id}.json") if r else formdir.LEGACY_REGIONS / f"{doc_id}.json"


def _gen1(doc_id: str) -> list[Path]:
    """그 전 자리 (기본 레이아웃)."""
    from . import formdir

    r = _private_home(doc_id)
    if engine(doc_id) == "overlay":
        if doc_id.startswith("img_"):
            return [(r or formdir.LEGACY_IMAGES) / doc_id / "overrides.json"]
        return [LEGACY_OVERLAY / f"{doc_id}.json"]
    return [] if r else [LEGACY_HTML / f"{doc_id}.json"]   # 사내 html 은 그때도 <사내 폴더>/<ID>/regions.json (지금 자리)


def _variant_files(doc_id: str) -> list[Path]:
    from . import formdir

    out = []
    for vd in dict.fromkeys([formdir.variants_dir(doc_id), formdir.LEGACY_VARIANTS / doc_id]):
        out += sorted(vd.glob("*.regions.json")) if vd.exists() else []
    return out


def legacy(doc_id: str) -> dict[str, Path]:
    """예전 위치의 파일 (있는 것만). {"": 기본, "<변형 ID>": 그 변형} — overlay 는 "" 하나. 모르는 서식이면 {}."""
    try:
        eng = engine(doc_id)
    except KeyError:
        return {}
    out = {}
    g2 = _gen2(doc_id)
    if g2.exists():
        out[""] = g2   # 바로 전 자리에는 변형도 함께 들어 있다
    for p in _gen1(doc_id):
        if p.exists() and "" not in out:
            out[""] = p
    if eng == "html" and not g2.exists():
        for p in _variant_files(doc_id):
            out.setdefault(p.name[:-len(".regions.json")], p)
    return out


def files(doc_id: str) -> list[Path]:
    """이 서식의 결과를 바꿀 수 있는 수정 파일 (새 위치 + 남은 예전 파일). 미리보기 캐시 키에 쓴다."""
    return [path(doc_id), *legacy(doc_id).values()]


def hash_files(doc_id: str) -> list[Path]:
    """서식 해시(docgen.preview.source_hash: 검수 후 바뀌었는지·데이터셋 기록)에 넣을 수정 파일.
    해시에는 경로도 들어가므로(새 자리는 formdir.hash_label 이 바로 전 자리 이름으로 바꾼다), 수정 파일을 옮기지 않은
    서식은 예전 경로 그대로 둬서 해시가 그대로다. 예전 레이아웃 변형 파일은 preview 가 변형 폴더에서 넣는다."""
    p, g2 = path(doc_id), _gen2(doc_id)
    if p.exists() or g2.exists():
        return [f for f in [p, g2] if f.exists()] + [f for f in _gen1(doc_id) if f.exists()]
    if engine(doc_id) == "overlay":
        return _gen1(doc_id)
    r = _private_home(doc_id)
    return [LEGACY_OVERLAY / f"{doc_id}.json", (r / doc_id / "regions.json") if r else LEGACY_HTML / f"{doc_id}.json"]


def exists(doc_id: str) -> bool:
    return any(p.exists() for p in files(doc_id))


# ---------------------------------------------------------------------------
# 읽기·쓰기
# ---------------------------------------------------------------------------

def _read_json(p: Path) -> dict:
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{p}: 수정 파일은 JSON 객체여야 합니다")
    return data


def _guess(data: dict) -> str | None:
    if data.get("engine"):
        return data["engine"]
    if "regions" in data or "variants" in data:
        return "html"
    if any(k in data for k in BODY["overlay"]):
        return "overlay"
    return None


def _check_engine(doc_id: str, data: dict, where: Path) -> None:
    """서식 종류와 다른 수정이면 멈춘다 (조용히 무시되지 않게). 모르는 칸은 check 가 알려 준다."""
    want, got = engine(doc_id), _guess(data)
    if got not in (None, want):
        raise ValueError(f"{doc_id} 는 {want} 서식인데 {where} 는 {got} 수정입니다 "
                         f"({'html 서식은 regions 목록' if want == 'html' else 'overlay 서식은 items·add·erase·marks'})")
    if data.get("unit") not in (None, UNIT[want]):
        raise ValueError(f"{where}: {want} 서식의 좌표 단위는 {UNIT[want]} 입니다")


def unknown(doc_id: str, data: dict) -> list[str]:
    eng = engine(doc_id)
    return sorted(set(data) - {"engine", "unit", *BODY[eng], *EXTRA[eng]})


def read(doc_id: str) -> dict:
    """수정 내용 (engine·unit 칸 뺀 것). 새 파일이 없으면 예전 파일들을 모아서. 없으면 (모르는 서식도) {}."""
    p = path(doc_id)
    if p.exists():
        data = _read_json(p)
        _check_engine(doc_id, data, p)
        return {k: v for k, v in data.items() if k not in ("engine", "unit")}
    old = legacy(doc_id)
    if not old:
        return {}
    if engine(doc_id) == "overlay":
        data = _read_json(old[""])
        _check_engine(doc_id, data, old[""])
        return data
    out = {}
    for vid, f in old.items():
        data = _read_json(f)
        _check_engine(doc_id, data, f)
        if vid:
            out.setdefault("variants", {})[vid] = {"regions": data.get("regions", [])}
        else:
            out["regions"] = data.get("regions", [])
    return out


def write(doc_id: str, body: dict) -> Path:
    """수정 내용 전체를 새 파일에 쓴다 (빈 것은 파일을 지운다). 예전 파일은 <이름>.migrated 로."""
    eng = engine(doc_id)
    body = {k: v for k, v in body.items() if k not in ("engine", "unit") and v not in (None, [], {})}
    if eng == "html" and "variants" in body:
        body["variants"] = {k: v for k, v in body["variants"].items() if v.get("regions")}
        if not body["variants"]:
            body.pop("variants")
    p = path(doc_id)
    with _lock:
        if any(body.get(k) for k in BODY[eng]):
            p.parent.mkdir(parents=True, exist_ok=True)
            tmp = p.with_suffix(".tmp")
            tmp.write_text(json.dumps({"engine": eng, "unit": UNIT[eng], **body}, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8")
            tmp.replace(p)
        elif p.exists():
            p.unlink()
        for f in legacy(doc_id).values():
            f.replace(f.with_name(f.name + ".migrated"))
    return p


# ---------------------------------------------------------------------------
# 명령
# ---------------------------------------------------------------------------

def _rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(DOCGEN.parent))
    except ValueError:
        return str(p)


def show(doc_id: str) -> list[dict]:
    """최종 값 칸 목록 (키가 있는 칸): [{page, key, label, kind, source, how}].
    how = 자동|수정|추가 (overlay: 자동 추출 + 수정), 템플릿|수정|추가|뺌 (html: 템플릿 칸 + 수정)."""
    if engine(doc_id) == "overlay":
        from .realform import form_layout, layout_keys

        lay, _ = form_layout(doc_id)
        keys = layout_keys(doc_id)
        return [{"page": it.get("page", 0), "key": ", ".join(keys[it["_id"]]["keys"]), "label": it.get("label") or "",
                 "kind": it.get("kind") or it["t"], "source": it.get("source") or "",
                 "how": "추가" if it.get("added") else "수정" if it.get("edited") else "자동"}
                for it in lay["items"] if keys.get(it.get("_id"), {}).get("keys")]
    from . import html_regions as HR
    from .entities import make_profile
    from .registry import load_all
    from .render import render
    from .schema import build_fields

    _, raw, _ = render(load_all()[doc_id], make_profile(0), 0)
    edits = {}
    for r in HR.load(doc_id)["regions"]:
        edits.setdefault(r["key"], r)
    out = []
    for f in build_fields(raw):
        r = edits.pop(f["key"], None)
        how = "템플릿" if r is None else "뺌" if r.get("drop") else "수정"
        out.append({"page": f.get("page", 0), "key": f["key"], "label": f.get("label") or "", "kind": f.get("type") or "text",
                    "source": (r or {}).get("source") or "", "how": how})
    for k, r in edits.items():
        out.append({"page": r.get("page", 0), "key": k, "label": r.get("label") or "", "kind": r.get("target") or "field",
                    "source": r.get("source") or "", "how": "뺌" if r.get("drop") else "추가" if "rect" in r else "수정 (못 찾음)"})
    return out


def check(doc_id: str) -> list[str]:
    """문제 목록 (빈 목록 = 괜찮음)."""
    if engine(doc_id) == "overlay":
        from . import formfields

        if formfields.exists(doc_id):
            return check_fields(doc_id)
    problems = []
    p, old = path(doc_id), legacy(doc_id)
    if p.exists() and old:
        problems.append("예전 수정 파일이 남아 있음 (새 파일만 씀): " + ", ".join(_rel(f) for f in old.values()))
    try:
        body = read(doc_id)
    except (ValueError, json.JSONDecodeError) as e:
        return problems + [str(e)]
    if unknown(doc_id, body):
        problems.append(f"모르는 칸 (생성에 안 쓰임): {unknown(doc_id, body)}")
    if engine(doc_id) == "overlay":
        from . import overrides as OV
        from .realform import raw_layout

        for o in body.get("items", []):
            if not isinstance(o.get("match"), dict):
                problems.append(f"items 에 match 가 없는 수정: {o}")
        _, broken = OV.apply(raw_layout(doc_id), body)
        problems += [f"깨진 수정 (자동 영역을 못 찾음): {o['match']}" for o in broken]
        return problems
    from . import html_regions as HR
    from .template_variants import load as variants

    known = {v["id"] for v in variants(doc_id)["variants"]}
    for vid, part in [("default", body), *body.get("variants", {}).items()]:
        if vid not in known:
            problems.append(f"등록되지 않은 레이아웃 변형: {vid}")
        try:
            HR.validate({"regions": part.get("regions", [])})
        except ValueError as e:
            problems.append(f"{vid}: {e}")
    return problems


def check_fields(doc_id: str) -> list[str]:
    """overlay 칸 목록(fields.json) 검사: 형식, 쪽 번호, 남은 예전 수정 파일."""
    from . import formfields

    problems = []
    left = [f for f in [path(doc_id), *legacy(doc_id).values()] if f.exists()]
    if left:
        problems.append("예전 수정 파일이 남아 있음 (칸 목록이 있어 안 읽음): " + ", ".join(_rel(f) for f in left))
    try:
        f = formfields.read(doc_id)
    except (ValueError, json.JSONDecodeError) as e:
        return problems + [str(e)]
    n = len(f.get("pages") or [])
    if not n:
        problems.append("pages 가 없습니다")
    for i, it in enumerate(f.get("items") or []):
        if not isinstance(it, dict) or not it.get("t") or not isinstance(it.get("page"), int) or not 0 <= it["page"] < n:
            problems.append(f"items[{i}]: 종류(t)·쪽(page)이 틀렸습니다")
    for i, e in enumerate(f.get("erase") or []):
        if not isinstance(e.get("page"), int) or not 0 <= e["page"] < n or len(e.get("rect") or []) != 4:
            problems.append(f"erase[{i}]: 쪽·사각형이 틀렸습니다")
    return problems


def _all_ids() -> list[str]:
    from .registry import load_all

    return sorted(load_all())


def migrate(apply: bool = False, ids: list[str] | None = None) -> list[dict]:
    """예전 파일 → 새 파일. [{id, from, to, status}] (status: 옮김|옮길 것|건너뜀: …)."""
    rows = []
    for doc_id in ids or _all_ids():
        old = legacy(doc_id)
        if not old:
            continue
        row = {"id": doc_id, "from": [_rel(f) for f in old.values()], "to": _rel(path(doc_id))}
        if path(doc_id).exists():
            row["status"] = "건너뜀: 새 파일이 이미 있음 (예전 파일을 확인하고 지우세요)"
        else:
            try:
                body = read(doc_id)
            except (ValueError, json.JSONDecodeError) as e:
                row["status"] = f"건너뜀: {e}"
            else:
                if apply:
                    write(doc_id, body)
                row["status"] = "옮김" if apply else "옮길 것"
        rows.append(row)
    known = set(_all_ids())
    for d in (LEGACY_OVERLAY, LEGACY_HTML):
        for f in sorted(d.glob("*.json")) if d.exists() else []:
            if f.stem not in known:
                rows.append({"id": f.stem, "from": [_rel(f)], "to": "", "status": "건너뜀: 등록되지 않은 서식"})
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m docgen.regions", description="서식 수정 파일 (regions/<ID>.json)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("path", help="수정 파일 위치").add_argument("id")
    sub.add_parser("show", help="최종 칸 목록").add_argument("id")
    c = sub.add_parser("check", help="형식·종류·깨진 수정·예전 파일 검사")
    c.add_argument("ids", nargs="*")
    c.add_argument("--all", action="store_true", help="수정 파일이 있는 서식 전부")
    m = sub.add_parser("migrate", help="예전 위치의 수정 파일을 새 파일로")
    m.add_argument("--apply", action="store_true", help="실제로 옮긴다 (없으면 목록만)")
    a = ap.parse_args(argv)
    if a.cmd == "path":
        p = path(a.id)
        print(f"{_rel(p)}  ({engine(a.id)}, {'있음' if p.exists() else '아직 없음'})")
        for vid, f in legacy(a.id).items():
            print(f"  예전 파일{' (' + vid + ')' if vid else ''}: {_rel(f)}" + ("  ← 새 파일이 없어 이것을 읽음" if not p.exists() else "  ← 안 읽음"))
        return 0
    if a.cmd == "show":
        rows = show(a.id)
        print(f"{a.id} ({engine(a.id)}) 칸 {len(rows)}개 · 수정 파일 {_rel(path(a.id))}")
        for r in rows:
            print(f"  [{r['how']}] p{r['page']} {r['key'] or '(키 없음)'}  {r['label']}  {r['kind']}" + (f"  ← {r['source']}" if r["source"] else ""))
        return 0
    if a.cmd == "check":
        from . import formfields

        ids = a.ids if a.ids and not a.all else [i for i in _all_ids() if exists(i) or formfields.exists(i)]
        bad = 0
        for doc_id in ids:
            probs = check(doc_id)
            bad += bool(probs)
            print(f"{'문제' if probs else '괜찮음'}  {doc_id}  {_rel(path(doc_id))}")
            for s in probs:
                print(f"    - {s}")
        print(f"{len(ids)}개 서식 중 문제 {bad}개")
        return 1 if bad else 0
    rows = migrate(a.apply)
    for r in rows:
        print(f"{r['status']}  {r['id']}: {', '.join(r['from'])} → {r['to']}")
    if not rows:
        print("옮길 예전 파일이 없습니다")
    elif not a.apply:
        print("목록만 보였습니다. 옮기려면 --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
