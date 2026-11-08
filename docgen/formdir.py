"""서식 폴더: 서식 하나 = 폴더 하나. 서식 파일이 어디 있는지는 여기서만 정한다.

  docgen/forms/<ID>/                     공개 서식 (저장소)
  $DOCGEN_PRIVATE_FORMS/<ID>/            실서류에서 만든 서식 (저장소 밖, 같은 꼴)
    look/                                모양
      original.pdf                         hf###: 하나은행 원본 PDF
      page_0.png …                         img_*: 견본 쪽 그림
      template.html.j2                     html 서식 (코드 서식·복제 서식 모두)
    layout.json                          overlay: 기재 자리 (hf### 은 PDF 에서 자동 추출, img_* 는 가져올 때 만든 것)
    form.json                            복제·분석기 html 서식: 부모 서식·값 선언 (docgen/htmlform.py)
    regions.json                         사람 수정 (docgen/regions.py)
    fields.json                          칸 목록 (docgen/formfields.py)
    generate.py                          값 만들기: 코드 서식은 @doc 함수(값 전부), html 서식은 adjust(d, p, rng)(칸끼리 관계)
    questions.json                       이 서식의 질문·답 — 기본과 다르게 할 것만 (docgen/formquestions.py)
    FORM.md                              서식 카드 (자동 생성, 읽는 곳): 항목·위치·정의한 곳·질문→답 예시·고치는 곳 (docgen/formcard.py)
    variants/                            html 레이아웃 변형: variants.json, <변형>.html.j2 (docgen/template_variants.py)

  docgen/forms/_common/                  모든 서식이 같이 쓰는 것 (README.md): 바탕 틀 templates/(_base·_macros·_official_*·_real_form,
                                         그룹 부품 _seal 등)·키 사전 dictionary/·기본 질문 questions.json
  docgen/forms/하나은행_서식자료/        원본 다운로드 보관 (목록 csv·안내문, 레이아웃이 없는 파일)
  docgen/forms/official_sources/         공식 원본 대조용 PDF (여러 서식이 같이 쓰므로 보관소에 둔다)

코드 서식(서식 폴더 generate.py 의 @doc)은 값을 파이썬이 만든다. spec.template("<그룹>/<ID>.html.j2")은 이름으로 남고,
render 의 로더가 그 이름을 이 폴더의 look/template.html.j2 로 찾는다.
hf### 레이아웃의 "file"(원본을 내려받은 자리)과 form.json 의 source.source_file 은 기록으로 두고, 파일은 source_path() 로 찾는다.

예전 위치(docgen/forms/layouts, docgen/forms/images, docgen/templates/<그룹>·copies·variants, 하나은행_서식자료의 PDF,
서식 폴더 바로 아래의 template.html.j2·page_<n>.png)는 새 위치에 없을 때만 읽는다. 옮기기:
  python -m docgen.formdir migrate [--apply]     (기본은 목록만. 글 파일은 복사하고 예전 것을 <이름>.migrated 로, 그림·PDF 는 옮긴다)
  python -m docgen.formdir path <ID>             이 서식의 파일들
  python -m docgen.formdir questions <ID>…|--all [--show|--check|--slim [--write]]   질문·답 questions.json (docgen/formquestions.py)
  python -m docgen.formdir card <ID>…|--all [--stale|--check] [--workers N]          서식 카드 FORM.md (docgen/formcard.py)
  python -m docgen.formdir values                                                    공통 값 출처 목록 forms/_common/values.md
  python -m docgen.formdir check <ID>…|--all                                         서식 검사 (고친 뒤 이것 하나)
"""
from __future__ import annotations

import argparse
import filecmp
import json
import os
import re
import shutil
import sys
import threading
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path

DOCGEN = Path(__file__).resolve().parent
PUBLIC = DOCGEN / "forms"
NEW_FORMS = PUBLIC          # 새 공개 서식을 만드는 곳 (테스트는 임시 폴더로 바꾼다. 찾을 때는 이것부터 본다)
SHARED = PUBLIC / "_common"  # 모든 서식이 같이 쓰는 것: 바탕 틀(templates/)·키 사전(dictionary/)·기본 질문(questions.json)
TEMPLATES = SHARED / "templates"
LEGACY_TEMPLATES = DOCGEN / "templates"   # 예전 자리 (코드 서식 템플릿·copies·variants·바탕 틀이 있던 곳)
SHARED_FILES = ("key_rules.json", "keys.json", "marks.json", "freetext_templates.json")   # docgen/ 에서 공통 폴더로 옮긴 설정
ARCHIVE = PUBLIC / "하나은행_서식자료"
LEGACY_LAYOUTS = PUBLIC / "layouts"
LEGACY_IMAGES = PUBLIC / "images"
LEGACY_COPIES = LEGACY_TEMPLATES / "copies"
LEGACY_VARIANTS = LEGACY_TEMPLATES / "variants"
LEGACY_REGIONS = PUBLIC / "regions"
MARKERS = ("look", "layout.json", "form.json", "regions.json", "variants")
TEMPLATE = "template.html.j2"


# ---------------------------------------------------------------------------
# 폴더
# ---------------------------------------------------------------------------

def private_roots() -> list[Path]:
    p = os.environ.get("DOCGEN_PRIVATE_FORMS")
    return [Path(p)] if p else []


def roots() -> list[Path]:
    out = []
    for r in [NEW_FORMS, PUBLIC, *private_roots()]:
        if r not in out:
            out.append(r)
    return out


def is_private(path: Path) -> bool:
    path = Path(path).resolve()
    return any(path.is_relative_to(r.resolve()) for r in private_roots())


def folder(doc_id: str) -> Path | None:
    """서식 폴더 (새 꼴). 없으면 None."""
    for r in roots():
        d = r / doc_id
        if d.is_dir() and any((d / m).exists() for m in MARKERS):
            return d
    return None


def home(doc_id: str, private: bool = False) -> Path:
    """서식 폴더. 아직 없으면 만들 자리 (private 면 사내 폴더 — 설정이 없으면 ValueError)."""
    d = folder(doc_id)
    if d is not None:
        return d
    if private:
        if not private_roots():
            raise ValueError("private_forms_dir 이 설정되지 않았습니다")
        return private_roots()[0] / doc_id
    return NEW_FORMS / doc_id


def new_dir(doc_id: str, root: Path | None = None) -> Path:
    """새 서식 폴더를 만든다. root = 사내 폴더(실서류에서 만든 것) 또는 None(저장소)."""
    d = (Path(root) if root else NEW_FORMS) / doc_id
    (d / "look").mkdir(parents=True)
    return d


# ---------------------------------------------------------------------------
# hf### (하나은행 원본 PDF)
# ---------------------------------------------------------------------------

def _hf(no: int) -> str:
    return f"hf{no:03d}"


def _legacy_layout(no: int) -> Path | None:
    hits = sorted(LEGACY_LAYOUTS.glob(f"*/{no:03d}.json"))
    return hits[0] if hits else None


def hf_layout(no: int) -> Path | None:
    d = folder(_hf(no))
    if d is not None and (d / "layout.json").exists():
        return d / "layout.json"
    return _legacy_layout(no)


@lru_cache(maxsize=None)
def _layout_head(path: str, mtime: int) -> tuple[int, str, str]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return d["no"], d.get("class", ""), d.get("file", "")


def layout_head(path: Path) -> tuple[int, str, str]:
    """레이아웃 파일의 (번호, 분류, 원본 기록 경로)."""
    return _layout_head(str(path), path.stat().st_mtime_ns)


def hf_layouts() -> list[Path]:
    """hf### 레이아웃 파일 전부. 예전 순서(분류 폴더 → 번호)대로."""
    found = {}
    for r in roots():
        if r in private_roots():
            continue
        for p in r.glob("hf[0-9][0-9][0-9]/layout.json"):
            found.setdefault(int(p.parent.name[2:]), p)
    for p in LEGACY_LAYOUTS.glob("*/*.json"):
        if p.stem.isdigit():
            found.setdefault(int(p.stem), p)
    return sorted(found.values(), key=hash_label)


def original_pdf(no: int) -> Path:
    d = folder(_hf(no))
    if d is not None and (d / "look" / "original.pdf").exists():
        return d / "look" / "original.pdf"
    return DOCGEN / layout_head(hf_layout(no))[2]


def source_path(rel: str) -> Path:
    """기록된 원본 경로(docgen 기준, 예: forms/하나은행_서식자료/…pdf) → 지금 파일 자리."""
    p = DOCGEN / rel
    if p.exists():
        return p
    m = re.match(r"(\d{3})_", Path(rel).name)
    if m and rel.startswith("forms/하나은행_서식자료/"):
        d = folder(_hf(int(m.group(1))))
        if d is not None and (d / "look" / "original.pdf").exists():
            return d / "look" / "original.pdf"
    return p


# ---------------------------------------------------------------------------
# img_* (견본 그림)
# ---------------------------------------------------------------------------

def image_dir(doc_id: str) -> Path | None:
    """가져온 이미지 서식 폴더 (layout.json 이 있는 곳)."""
    d = folder(doc_id)
    if d is not None and (d / "layout.json").exists():
        return d
    for r in [LEGACY_IMAGES, *private_roots()]:
        if (r / doc_id / "layout.json").exists():
            return r / doc_id
    return None


def image_dirs() -> list[Path]:
    """등록할 이미지 서식 폴더들 (저장소 → 예전 저장소 자리 → 사내 폴더, 각각 이름 순)."""
    out, seen = [], set()
    for r in [*[r for r in roots() if r not in private_roots()], LEGACY_IMAGES, *private_roots()]:
        for d in sorted(r.glob("img_*")) if r.is_dir() else []:
            if d.name not in seen and (d / "layout.json").exists():
                seen.add(d.name)
                out.append(d)
    return out


def page_png(doc_id: str, page: int) -> Path:
    d = image_dir(doc_id)
    if d is None:
        raise KeyError(doc_id)
    p = d / "look" / f"page_{page}.png"
    return p if p.exists() else d / f"page_{page}.png"


def image_files(doc_id: str) -> list[Path]:
    """이미지 서식 폴더의 파일 (사람 수정 제외), 예전 이름 순 — 서식 해시용."""
    d = image_dir(doc_id)
    if d is None:
        return []
    files = [f for f in [*d.iterdir(), *((d / "look").iterdir() if (d / "look").is_dir() else [])]
             if f.is_file() and f.name not in ("overrides.json", "regions.json") and not f.name.endswith(".migrated")]
    return sorted(files, key=hash_label)


# ---------------------------------------------------------------------------
# html 서식
# ---------------------------------------------------------------------------

def template_in(d: Path) -> Path | None:
    for p in (d / "look" / TEMPLATE, d / TEMPLATE):
        if p.exists():
            return p
    return None


def copy_dir(doc_id: str) -> Path | None:
    """화면에서 만든 html 서식(복제·분석기)의 폴더: form.json 과 템플릿이 있는 곳."""
    for r in [*roots(), LEGACY_COPIES]:
        d = r / doc_id
        if (d / "form.json").exists() and template_in(d):
            return d
    return None


def copy_dirs() -> list[Path]:
    """등록할 복제·분석기 html 서식 폴더 (예전 copies → 저장소 → 사내 순, 각각 이름 순)."""
    out, seen = [], set()
    for r in [LEGACY_COPIES, *roots()]:
        for d in sorted(r.iterdir()) if r.is_dir() else []:
            if d.name not in seen and (d / "form.json").exists() and template_in(d):
                seen.add(d.name)
                out.append(d)
    return out


def template(doc_id: str) -> Path | None:
    """html 서식의 템플릿 파일 (코드 서식·복제 서식). overlay 는 None."""
    d = copy_dir(doc_id)
    if d is not None:
        return template_in(d)
    d = folder(doc_id)
    if d is not None and (d / "look" / TEMPLATE).exists():
        return d / "look" / TEMPLATE
    from .registry import load_all

    spec = load_all().get(doc_id)
    if spec is None or spec.template.startswith("@") or spec.template == "_real_form.html.j2":
        return None
    p = LEGACY_TEMPLATES / spec.template
    return p if p.exists() else None


_drafts = threading.local()


def draft_key(doc_id: str, variant: str = "default") -> str:
    return doc_id if variant == "default" else f"{doc_id}@{variant}"


def template_draft_of(doc_id: str, variant: str = "default") -> str | None:
    """이 스레드의 저장하지 않은 템플릿 (없으면 None). variant: 레이아웃 변형 (template_variants 가 읽음)."""
    return (getattr(_drafts, "map", None) or {}).get(draft_key(doc_id, variant))


@contextmanager
def template_draft(doc_id: str, text: str, variant: str = "default"):
    """이 스레드에서 렌더링하는 동안 doc_id 의 템플릿을 text 로 (저장하지 않은 템플릿 미리보기, studio 자리·템플릿 화면).
    variant 가 "default" 면 코드 서식의 look/template.html.j2, 아니면 레이아웃 변형 variants/<변형>.html.j2."""
    d = getattr(_drafts, "map", None)
    if d is None:
        d = _drafts.map = {}
    key = draft_key(doc_id, variant)
    old = d.get(key)
    d[key] = text
    try:
        yield
    finally:
        if old is None:
            d.pop(key, None)
        else:
            d[key] = old


def jinja_source(name: str):
    """render 의 로더: 코드 서식 템플릿 이름 "<그룹>/<ID>.html.j2" → 서식 폴더의 look/template.html.j2 (초안이 있으면 초안)."""
    if name.startswith("@") or "/" not in name or not name.endswith(".html.j2"):
        return None
    doc_id = name.rsplit("/", 1)[1][:-len(".html.j2")]
    if doc_id.startswith("_"):
        return None   # 그룹 부품 (forms/_common/templates/ 에 있다)
    text = (getattr(_drafts, "map", None) or {}).get(doc_id)
    if text is not None:
        return text, f"{doc_id} (저장 전 초안)", lambda: False
    d = folder(doc_id)
    p = d / "look" / TEMPLATE if d else None
    if p is None or not p.exists():
        return None
    mtime = p.stat().st_mtime_ns
    # 이 스레드에 초안이 생기면 캐시에 있던 저장본은 낡은 것으로 (초안이 바로 쓰이게)
    return p.read_text(encoding="utf-8"), str(p), lambda: (p.exists() and p.stat().st_mtime_ns == mtime
                                                            and doc_id not in (getattr(_drafts, "map", None) or {}))


def variants_dir(doc_id: str) -> Path:
    """레이아웃 변형 폴더. 새 자리에 없고 예전 자리(templates/variants/<ID>)에 있으면 그곳."""
    d = folder(doc_id)
    new = (d or home(doc_id)) / "variants"
    if not new.exists() and (LEGACY_VARIANTS / doc_id).exists():
        return LEGACY_VARIANTS / doc_id
    return new


# ---------------------------------------------------------------------------
# 서식 해시 이름 (docgen.preview.source_hash)
# ---------------------------------------------------------------------------

def _root_of(path: Path) -> Path | None:
    for r in roots():
        if path.is_relative_to(r.resolve()):
            return r.resolve()
    return None


def hash_label(path: Path) -> Path:
    """서식 해시에 넣는 이름: 파일을 옮기기 전 자리. 그래서 서식 폴더로 옮겨도 서식 해시(검수 후 바뀌었는지)가 그대로다."""
    path = Path(path).resolve()
    r = _root_of(path)
    if r is None or path == r:
        return path
    doc_id, *rest = path.relative_to(r).parts
    if doc_id == SHARED.name and rest:   # 공통 폴더로 옮긴 바탕 틀·키 사전·설정 파일: 예전 자리 이름
        if rest[0] in ("templates", "dictionary"):
            return (LEGACY_TEMPLATES if rest[0] == "templates" else DOCGEN / "dictionary") / Path(*rest[1:])
        if rest[0] in SHARED_FILES:
            return DOCGEN / rest[0]
    if not rest or doc_id in ("layouts", "images", "regions", "하나은행_서식자료", "official_sources"):
        return path
    private = r in [p.resolve() for p in private_roots()]
    if rest == ["regions.json"]:
        return (r / "regions" / f"{doc_id}.json") if private else LEGACY_REGIONS / f"{doc_id}.json"
    if rest[0] == "variants":
        return path if private else LEGACY_VARIANTS / doc_id / Path(*rest[1:])
    if rest[0] == "look":
        rest = rest[1:]
    if re.fullmatch(r"hf\d{3}", doc_id) and not private:
        if rest == ["layout.json"] and path.exists():
            no, cls, _ = layout_head(path)
            return LEGACY_LAYOUTS / cls.replace("/", "_") / f"{no:03d}.json"   # 분류 폴더 이름 (extract_form_layout 과 같게)
        return path
    if private:
        return r / doc_id / Path(*rest)
    if doc_id.startswith("img_"):
        return LEGACY_IMAGES / doc_id / Path(*rest)
    if (r / doc_id / "form.json").exists():
        return LEGACY_COPIES / doc_id / Path(*rest)
    if rest == [TEMPLATE]:
        from .registry import load_all

        spec = load_all().get(doc_id)
        if spec is not None and not spec.template.startswith("@"):
            return LEGACY_TEMPLATES / spec.template
    return path


# ---------------------------------------------------------------------------
# 옮기기
# ---------------------------------------------------------------------------

def _moves(doc_id: str) -> list[tuple[Path, Path]]:
    """(예전 파일, 새 자리) 목록."""
    from .registry import load_all

    spec = load_all().get(doc_id)
    out = []
    if re.fullmatch(r"hf\d{3}", doc_id):
        old = _legacy_layout(int(doc_id[2:]))
        if old is not None:
            d = NEW_FORMS / doc_id
            out.append((old, d / "layout.json"))
            pdf = DOCGEN / layout_head(old)[2]
            if pdf.exists():
                out.append((pdf, d / "look" / "original.pdf"))
        return out
    if doc_id.startswith("img_"):
        for r in [LEGACY_IMAGES, *private_roots()]:
            src = r / doc_id
            if (src / "layout.json").exists():
                dst = (NEW_FORMS / doc_id) if r == LEGACY_IMAGES else src
                for f in sorted(src.iterdir()):
                    if f.is_file() and f.name not in ("overrides.json",) and not f.name.endswith(".migrated"):
                        to = dst / "look" / f.name if f.name.startswith("page_") else dst / f.name
                        if f != to:
                            out.append((f, to))
                break
        return out
    if spec is None or spec.template == "_real_form.html.j2":
        return out
    for r in [LEGACY_COPIES, *private_roots()]:
        src = r / doc_id
        if (src / "form.json").exists():
            dst = (NEW_FORMS / doc_id) if r == LEGACY_COPIES else src
            for f in sorted(src.rglob("*")):
                if not f.is_file() or f.name.endswith(".migrated") or f.name == "regions.json":
                    continue
                rel = f.relative_to(src)
                to = dst / "look" / TEMPLATE if rel == Path(TEMPLATE) else dst / rel
                if f != to:
                    out.append((f, to))
            break
    else:
        if not spec.template.startswith("@") and (LEGACY_TEMPLATES / spec.template).exists():
            out.append((LEGACY_TEMPLATES / spec.template, NEW_FORMS / doc_id / "look" / TEMPLATE))
    vd = LEGACY_VARIANTS / doc_id
    for f in sorted(vd.iterdir()) if vd.is_dir() else []:
        if f.is_file() and not f.name.endswith(".migrated") and not f.name.endswith(".regions.json"):
            out.append((f, (NEW_FORMS / doc_id) / "variants" / f.name))
    return out


def migrate(apply: bool = False, ids: list[str] | None = None) -> list[dict]:
    """예전 자리 → 서식 폴더. [{id, from, to, status}]. 사람 수정(regions)은 regions.migrate 가 옮긴다."""
    from .registry import load_all

    rows = []
    hf = {_hf(int(p.stem)) for p in LEGACY_LAYOUTS.glob("*/*.json") if p.stem.isdigit()}   # 등록 안 되는 레이아웃도 함께
    for doc_id in ids or sorted(set(load_all()) | hf):
        moves = _moves(doc_id)
        if not moves:
            continue
        clash = [(a, b) for a, b in moves if b.exists() and not filecmp.cmp(a, b, shallow=False)]
        row = {"id": doc_id, "files": len(moves), "from": _rel(moves[0][0].parent), "to": _rel(moves[0][1].parent)}
        if clash:
            row["status"] = "건너뜀: 예전과 새 파일이 다름 — " + ", ".join(f"{_rel(a)} ≠ {_rel(b)}" for a, b in clash[:3])
        elif apply:
            for a, b in moves:
                b.parent.mkdir(parents=True, exist_ok=True)
                if a.suffix in (".pdf", ".png"):
                    if b.exists():
                        a.unlink()
                    else:
                        shutil.move(a, b)
                else:
                    if not b.exists():
                        shutil.copy2(a, b)
                    a.replace(a.with_name(a.name + ".migrated"))
            row["status"] = "옮김"
        else:
            row["status"] = "옮길 것"
        rows.append(row)
    if apply:
        _register_again()
    return rows


def freeze(apply: bool = False, ids: list[str] | None = None) -> list[dict]:
    """서식마다 칸 목록(fields.json)이 없으면 만든다. overlay 는 자동 추출 레이아웃 + 예전 사람 수정 (overrides.freeze),
    html 은 예전 regions.json + 복제 서식 form.json 의 값 선언 (formfields.adopt).
    [{id, status, broken}]. 목록만 볼 때도 못 찾을 예전 수정을 알려 준다."""
    from . import formfields
    from . import overrides as OV
    from . import regions
    from .realform import raw_layout
    from .registry import load_all

    rows = []
    for doc_id in ids or sorted(load_all()):
        if formfields.exists(doc_id):
            continue
        if load_all()[doc_id].template != "_real_form.html.j2":   # html: 예전 regions.json·form.json 값 선언을 칸 목록으로
            if apply:
                formfields.adopt(doc_id)
            rows.append({"id": doc_id, "status": "만듦" if apply else "만들 것", "broken": []})
            continue
        if apply:
            _, broken = OV.freeze(doc_id)
        else:
            _, broken = OV.apply(raw_layout(doc_id), regions.read(doc_id))
        rows.append({"id": doc_id, "status": "만듦" if apply else "만들 것", "broken": broken})
    return rows


def declare(apply: bool = False, ids: list[str] | None = None, seeds: int = 24) -> list[dict]:
    """코드 서식(html 70종)의 칸을 칸 목록에 적는다: 여러 seed 로 그려 나온 키마다 항목명·종류와 source "code"
    (값은 생성 함수 그대로). 사람이 값 출처를 바꾼 칸은 건드리지 않는다. [{id, keys, new}]."""
    from . import formfields
    from .htmlform import declare as found
    from .registry import load_all

    rows = []
    for doc_id in ids or sorted(load_all()):
        spec = load_all()[doc_id]
        if spec.template.startswith("@") or spec.template == "_real_form.html.j2":
            continue
        d = found(doc_id, seeds)
        n = sum(len(L["fields"]) for L in d["lists"].values()) + len(d["fields"])
        new = formfields.merge_declared(doc_id, d)[1] if apply else n
        rows.append({"id": doc_id, "keys": n, "new": new})
    return rows


def _register_again() -> None:
    """옮긴 뒤 같은 프로세스에서 레이아웃 캐시를 비운다."""
    from . import realform

    realform.load_layout.cache_clear()


def _rel(p: Path) -> str:
    try:
        return str(Path(p).resolve().relative_to(DOCGEN.parent))
    except ValueError:
        return str(p)


def unknown_id(doc_id: str) -> str:
    """없는 서식 ID 안내 (비슷한 ID 와 목록 보는 법)."""
    import difflib

    from .registry import load_all

    near = difflib.get_close_matches(doc_id, list(load_all()), n=5, cutoff=0.6)
    return (f"서식 ID '{doc_id}' 가 없습니다 (새 서식이면 쓸 수 있는 ID)." + (f" 비슷한 ID: {', '.join(near)}." if near else "")
            + " 목록: python -m docgen list")


def describe(doc_id: str) -> list[tuple[str, Path | None]]:
    from . import regions
    from .registry import load_all

    spec = load_all()[doc_id]
    rows = [("서식 폴더", folder(doc_id)), ("서식 카드 FORM.md (자동, 읽는 곳)", (folder(doc_id) or home(doc_id)) / "FORM.md")]
    if spec.template == "_real_form.html.j2":
        if re.fullmatch(r"hf\d{3}", doc_id):
            rows += [("기재 자리 (자동 추출)", hf_layout(int(doc_id[2:]))), ("모양 (원본 PDF)", original_pdf(int(doc_id[2:])))]
        else:
            d = image_dir(doc_id)
            rows += [("기재 자리", d / "layout.json" if d else None), ("모양 (견본 그림)", page_png(doc_id, 0) if d else None)]
        d = folder(doc_id)   # 칸끼리 관계 (overlay 도 서식 폴더 generate.py 의 adjust)
        if d is not None:
            rows += [("칸끼리 관계 (generate.py)", d / "generate.py")]
    else:
        rows += [("모양 (템플릿)", template(doc_id))]
        if copy_dir(doc_id):
            rows += [("값 선언 (form.json)", copy_dir(doc_id) / "form.json")]
            if (copy_dir(doc_id) / "generate.py").exists():
                rows += [("생성 스크립트 (generate.py)", copy_dir(doc_id) / "generate.py")]
        else:
            from .preview import generator_files

            gen = generator_files(spec.generate)
            rows += [("값 만들기 (generate.py)", gen[0])] + [("같은 그룹 도우미", g) for g in gen[1:]]
        vd = variants_dir(doc_id)
        if vd.exists():
            rows += [("레이아웃 변형", vd)]
    from . import formfields

    from . import formquestions

    from . import formqa

    rows += [("칸 목록 (사람이 고치는 곳)", formfields.path(doc_id)), ("질문·답 (questions.json)", formquestions.path(doc_id)),
             ("서식 전용 질문 (qa.py)", formqa.path(doc_id))]
    return rows


def questions_slim(ids: list[str], write: bool = False) -> list[dict]:
    """questions.json 에서 기본과 같은 것을 지운다 (예전 꼴의 전체 사본 → 바꾼 것만, 다 같으면 파일을 지움). [{id, status}]."""
    from . import formquestions as FQ

    rows = []
    for doc_id in ids:
        body = FQ.read(doc_id) if FQ.path(doc_id).exists() else None
        if body is None:
            continue
        new = FQ.slim(doc_id, body)
        status = "그대로" if new == body else ("지움 (모두 기본)" if not new else "줄임")
        if write and status != "그대로":
            FQ.write(doc_id, new)
        rows.append({"id": doc_id, "status": status, "body": new})
    return rows


def check_form(doc_id: str, seeds: int = 4) -> dict:
    """서식 하나 검사 — 고친 뒤 이것 하나: 칸 목록 형식·박스가 쪽 안·값 출처·그려지지 않는 선언·질문(questions.json·q)·카드.
    {"problems": 고쳐야 하는 것, "notes": 알아 둘 것}."""
    from . import formcard, formfields, regions
    from . import formquestions as FQ
    from . import sources as S
    from .entities import make_profile
    from .keyrules import load as rules

    problems, notes = list(regions.check(doc_id)), []
    body = formfields.read(doc_id) or {}
    profiles = [make_profile(s) for s in range(8)]
    kinds = set(S.RULE_KINDS) | set(S.SPECIAL_RULES) | set(rules().get("kinds", {})) | {"text"}
    from .keyrules import CODE_KINDS

    kinds |= set(CODE_KINDS)
    from . import usergen

    try:
        kinds |= set(usergen.all_generators())   # 직접 만든 생성기 (docgen/forms/_common/generators.py)
    except ValueError as e:
        problems.append(f"직접 만든 생성기 파일 오류: {e}")

    def bad_source(src) -> str | None:
        if src in (None, "code"):
            return None
        if not isinstance(src, str):
            return "글자가 아님"
        if src.startswith("profile."):   # 고객 8명 중 누구에게든 값이 있으면 맞는 경로 (조건부 정보: 사업자·외국인 …)
            return None if any(S.lookup_profile(p, src) is not None for p in profiles) else "고객 정보에 없는 경로 (forms/_common/values.md)"
        if src.startswith("parent."):   # 복제 서식: 부모 서식 생성 함수가 만든 값
            return None
        if src.startswith("rule:"):
            return None if src[5:] in kinds else "모르는 값 종류 (forms/_common/values.md)"
        return "profile.<경로>·rule:<종류>·parent.<경로>(복제 서식) 여야 합니다"
    pages = body.get("pages") or []
    for i, it in enumerate(body.get("items") or []):
        why = bad_source(it.get("source"))
        if why:
            problems.append(f"items[{i}] '{it.get('label', '')}': source {it.get('source')!r} — {why}")
        r, pg = it.get("rect"), it.get("page", 0)
        if r and pg < len(pages) and (r[0] < 0 or r[1] < 0 or r[2] > pages[pg].get("width", 1e9) + 1 or r[3] > pages[pg].get("height", 1e9) + 1):
            problems.append(f"items[{i}] '{it.get('label', '')}': 박스 {r} 가 {pg + 1}쪽 밖으로 나갑니다")
    declared = dict(body.get("fields") or {})
    for name, lst in (body.get("lists") or {}).items():
        for sub, d in (lst.get("fields") or {}).items():
            declared[f"{name}.*.{sub}"] = d
    for k, d in declared.items():
        why = bad_source(d.get("source"))
        if why:
            problems.append(f"fields.json '{k}': source {d.get('source')!r} — {why}")
    docs = FQ.seen_fields(doc_id, seeds)
    from .fieldinfo import pattern

    drawn = {pattern(f.get("doc_key") or f["key"]) for fs in docs for f in fs}
    stray = [k for k in (body.get("q") or {}) if pattern(k.replace("*", "0")) not in drawn]
    if stray:
        problems.append(f"fields.json 맨 위 \"q\" 의 키가 그린 칸에 없습니다 (오타·반복 행은 *): {', '.join(stray[:8])}")
    if declared:
        never = [k for k in declared if pattern(k.replace("*", "0")) not in drawn]
        if never:
            notes.append(f"fields.json 에 적었는데 {len(docs)}번 그려도 안 나온 칸 {len(never)}개 (템플릿에 f(\"키\") 가 없거나 드문 조건부 칸): "
                         + ", ".join(never[:8]))
    q = FQ.check(doc_id, seeds, docs)
    problems += q["problems"]
    notes += q["notes"]
    if formcard.stale(doc_id):
        notes.append(f"카드 FORM.md 가 없거나 오래됨 — python -m docgen.formdir card {doc_id}")
    return {"problems": problems, "notes": notes}


def show_questions(doc_id: str, seeds: int = 8) -> str:
    """합친 전체 (기본 + 이 서식에서 바꾼 것) 를 글로."""
    from . import formquestions as FQ

    v = FQ.resolved(doc_id, seeds=seeds)
    mark = lambda task, k: " ← 이 서식에서 바꿈" if k in v[task]["changed"] else ""  # noqa: E731
    out = [f"# {doc_id} 질문·답 (기본 + {FQ.path(doc_id).name if FQ.path(doc_id).exists() else '바꾼 것 없음'})"]
    for task in ("kie", "marks"):
        t = v[task]
        out += [f"\n## {task}", f"질문 항목 줄 틀: {t['item']}{mark(task, 'item')}",
                f"답 항목 틀: {json.dumps(t['answer'], ensure_ascii=False)}{mark(task, 'answer')}",
                f"빈 칸 답 틀: {json.dumps(t['answer_empty'], ensure_ascii=False)}{mark(task, 'answer_empty')}",
                f"질문{mark(task, 'prompt')}:", *("  " + x for x in t["prompt"].split("\n")), "칸:"]
        for it in t["items"]:
            ch = f"  ← 바꿈: {', '.join(it['changed'])}" if it["changed"] else ""
            seen = "" if it["seen"] == it["of"] else f"  (그린 {it['of']}번 중 {it['seen']}번 나옴)"
            out.append(f"  {'묻기' if it['ask'] else '안 묻기'}  {it['key']}: {it['q_label'] or '/'.join(map(str, it['labels']))}"
                       + (f" ({it['note']})" if it["note"] else "") + seen + ch)
        if t.get("unknown"):
            out.append(f"  (지금 칸에 없는 키: {', '.join(t['unknown'])})")
    for task in ("classify", "ocr_field", "ocr_page"):
        t = v[task]
        out += [f"\n## {task}{mark(task, 'prompt')}", "  " + t["prompt"].replace("\n", "\n  ")]
        if task == "classify":
            out.append(f"  정답: {t['answer']}{mark(task, 'answer')}" + (f" (다른 이름: {', '.join(t['aliases'])})" if t["aliases"] else ""))
        elif t["exclude"]:
            out.append(f"  뺄 칸: {', '.join(t['exclude'])}")
    from . import formqa

    qa = formqa.check(doc_id, FQ.seen_fields(doc_id, seeds))
    out.append("\n## form_qa (이 서식만의 질문, qa.py)" + ("" if qa["rows"] else ": 없음"))
    for r in qa["rows"]:
        ex = r["example"] or {}
        out += [f"  {r['name']}()  — 그린 {r['of']}개 중 {r['asked']}개에서 물음, 정답 꼴 {r['kind'] or '-'}",
                f"    질문: {ex.get('prompt', '-')}", f"    정답: {json.dumps(ex['answer'], ensure_ascii=False) if 'answer' in ex else '-'}"]
    out += [f"  문제: {p}" for p in qa["problems"]]
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m docgen.formdir", description="서식 폴더 (서식 하나 = 폴더 하나)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("path", help="이 서식의 파일들").add_argument("id")
    dc = sub.add_parser("declare", help="코드 서식의 칸을 칸 목록에 적기 (source \"code\", 값은 생성 함수 그대로)")
    dc.add_argument("ids", nargs="*")
    dc.add_argument("--apply", action="store_true")
    dc.add_argument("--seeds", type=int, default=24, help="그려 볼 seed 수 (조건부 칸을 찾으려면 늘린다)")
    qs = sub.add_parser("questions", help="서식의 질문·답 (questions.json = 기본과 다르게 할 것만): 보기·검사·정리")
    qs.add_argument("ids", nargs="*")
    qs.add_argument("--all", action="store_true", help="모든 서식")
    qs.add_argument("--show", action="store_true", help="합친 전체 (기본 + 이 서식에서 바꾼 것)")
    qs.add_argument("--check", action="store_true", help="지금 칸과 맞는지 검사 (질문 설정 q·답 틀과 질문·기본과 같은 줄)")
    qs.add_argument("--slim", action="store_true", help="기본과 같은 것을 파일에서 지움 (예전 꼴의 전체 사본 정리)")
    qs.add_argument("--write", action="store_true", help="--slim 을 파일에 쓴다 (없으면 목록만)")
    qs.add_argument("--seeds", type=int, default=8, help="그려 볼 seed 수 (평가·학습 범위에서 각각)")
    qa = sub.add_parser("qa", help="이 서식만의 질문 qa.py: 견본 만들기(--new)·보기")
    qa.add_argument("id")
    qa.add_argument("--new", action="store_true", help="견본 qa.py 를 만든다 (이 서식의 칸 키로 쓴 예시, 주석). 있으면 멈춤")
    qa.add_argument("--seeds", type=int, default=8)
    ad = sub.add_parser("adjust", help="칸끼리 관계 generate.py (overlay 서식): 견본 만들기(--new)")
    ad.add_argument("id")
    ad.add_argument("--new", action="store_true", help="견본 generate.py 를 만든다 (이 서식의 칸 키를 주석으로). 있으면 멈춤")
    ck = sub.add_parser("check", help="서식 검사 (고친 뒤 이것 하나): 칸 목록·박스·값 출처·질문 설정·questions.json·카드")
    ck.add_argument("ids", nargs="*")
    ck.add_argument("--all", action="store_true", help="모든 서식")
    sub.add_parser("values", help="공통 값 출처 목록 docgen/forms/_common/values.md 다시 만들기")
    cd = sub.add_parser("card", help="서식 카드 FORM.md 만들기 (항목·위치·정의한 곳·질문→답 예시·고치는 곳)")
    cd.add_argument("ids", nargs="*")
    cd.add_argument("--all", action="store_true", help="모든 서식")
    cd.add_argument("--stale", action="store_true", help="오래된(원본이 바뀐) 카드만")
    cd.add_argument("--check", action="store_true", help="만들지 않고 오래된 카드만 보임 (있으면 종료 코드 1)")
    cd.add_argument("--workers", type=int, default=1, help="동시에 그릴 프로세스 수")
    m = sub.add_parser("migrate", help="예전 자리의 서식 파일을 서식 폴더로 (사람 수정도 함께)")
    m.add_argument("--apply", action="store_true", help="실제로 옮긴다 (없으면 목록만)")
    a = ap.parse_args(argv)
    from .registry import load_all

    known = load_all()
    for i in [getattr(a, "id", None), *(getattr(a, "ids", None) or [])]:
        if i is not None and i not in known:
            print(unknown_id(i), file=sys.stderr)
            return 2

    if a.cmd == "path":
        for role, p in describe(a.id):
            print(f"{role:<16} {_rel(p) if p else '-'}" + ("" if p is None or p.exists() else "  (아직 없음)"))
        return 0
    if a.cmd == "declare":
        rows = declare(a.apply, a.ids or None, a.seeds)
        for r in rows:
            print(f"{r['id']}: 칸 {r['keys']}개" + (f" (새로 {r['new']}개)" if a.apply else ""))
        print(f"코드 서식 {len(rows)}개" + ("" if a.apply else ". 목록만 보였습니다. 적으려면 --apply"))
        return 0
    if a.cmd == "questions":
        ids = sorted(load_all()) if a.all else a.ids
        if not ids:
            ap.error("서식 ID 나 --all")
        from . import formquestions as FQ

        if a.show:
            for i in ids:
                print(show_questions(i, a.seeds))
            return 0
        if a.slim:
            rows = questions_slim(ids, a.write)
            for r in rows:
                if r["status"] != "그대로":
                    print(f"{r['status']}  {r['id']}")
            n = sum(r["status"] != "그대로" for r in rows)
            print(f"questions.json {len(rows)}개 중 {n}개 " + ("정리함" if a.write else "정리할 것 (목록만. 쓰려면 --write)"))
            return 0
        bad = 0
        for i in ids:
            r = FQ.check(i, a.seeds)
            bad += bool(r["problems"])
            for p in r["problems"]:
                print(f"문제  {i}: {p}")
            for n in r["notes"]:
                if FQ.path(i).exists() or len(ids) == 1:
                    print(f"참고  {i}: {n}")
        print(f"서식 {len(ids)}개 검사, 문제 있는 서식 {bad}개")
        return 1 if bad else 0
    if a.cmd == "adjust":
        from . import realform as RF

        d = folder(a.id)
        if d is None or not (d / "layout.json").exists() and RF.form_no(a.id) is None:
            print("overlay(원본·그린) 서식만 됩니다. html 서식의 generate.py 는 docgen/manual/NEW_FORM_SPEC.md 8절", file=sys.stderr)
            return 2
        p = d / "generate.py"
        if not a.new:
            print(_rel(p) if p.exists() else f"없음: {_rel(p)} — 견본: python -m docgen.formdir adjust {a.id} --new")
            return 0
        if p.exists():
            print(f"이미 있습니다 (덮어쓰지 않음): {_rel(p)}")
            return 1
        p.write_text(RF.adjust_skeleton(a.id), encoding="utf-8")
        print(f"만듦: {_rel(p)} — adjust 를 고친 뒤 영역 편집의 수정 전후 비교, check {a.id} 로 확인")
        return 0
    if a.cmd == "qa":
        from . import formqa
        from . import formquestions as FQ

        p = formqa.path(a.id)
        if a.new:
            if p.exists():
                print(f"이미 있습니다 (덮어쓰지 않음): {_rel(p)}")
                return 1
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(formqa.skeleton(a.id, FQ.seen_fields(a.id, a.seeds)), encoding="utf-8")
            print(f"만듦: {_rel(p)} — 주석을 풀고 고친 뒤 python -m docgen.formdir qa {a.id} 로 확인, 카드는 card {a.id}")
            return 0
        print("## form_qa" + show_questions(a.id, a.seeds).split("\n## form_qa", 1)[-1] if p.exists()
              else f"{_rel(p)} 없음 — 견본: python -m docgen.formdir qa {a.id} --new")
        return 0
    if a.cmd == "check":
        ids = sorted(load_all()) if a.all else a.ids
        if not ids:
            ap.error("서식 ID 나 --all")
        bad = 0
        for i in ids:
            r = check_form(i)
            bad += bool(r["problems"])
            for p in r["problems"]:
                print(f"문제  {i}: {p}")
            if len(ids) == 1 or r["problems"]:
                for n in r["notes"]:
                    print(f"참고  {i}: {n}")
        print(f"서식 {len(ids)}개 검사, 문제 있는 서식 {bad}개" + ("" if bad else " — 괜찮습니다"))
        return 1 if bad else 0
    if a.cmd == "values":
        from . import formcard

        p = SHARED / "values.md"
        p.write_text(formcard.values_md(), encoding="utf-8")
        print(p)
        return 0
    if a.cmd == "card":
        from . import formcard

        ids = sorted(load_all()) if a.all else a.ids
        if not ids:
            ap.error("서식 ID 나 --all")
        stale = [i for i in ids if formcard.stale(i)]
        if a.check:
            for i in stale:
                print(f"오래됨  {i}: {formcard.path(i)}")
            print(f"서식 {len(ids)}개 중 카드가 없거나 오래된 것 {len(stale)}개")
            return 1 if stale else 0
        todo = stale if a.stale else ids
        done = formcard.write_many(todo, a.workers)
        print(f"카드 {len(done)}개 만듦" + (f" (예: {formcard.path(done[0])})" if done else ""))
        return 0
    from . import regions

    rows = migrate(a.apply)
    for r in rows:
        print(f"{r['status']}  {r['id']}: {r['from']} → {r['to']} ({r['files']}개)")
    reg = regions.migrate(a.apply)
    for r in reg:
        print(f"{r['status']}  {r['id']} 사람 수정: {', '.join(r['from'])} → {r['to']}")
    frozen = freeze(a.apply)
    if a.apply:   # 코드 서식의 칸을 칸 목록에 (아직 안 적은 서식만)
        from . import formfields

        todo = [i for i in sorted(load_all()) if not load_all()[i].template.startswith("@")
                and load_all()[i].template != "_real_form.html.j2" and not (formfields.read(i) or {}).get("fields")]
        if todo:
            print(f"코드 서식 칸 적기 {len(declare(True, todo))}개")
    for r in frozen:
        if r["broken"]:
            print(f"{r['status']}  {r['id']} 칸 목록: 못 찾은 예전 수정 {len(r['broken'])}개 (빠짐): "
                  + ", ".join(f"{b['match'].get('page', 0) + 1}쪽 '{b['match'].get('label', '')}'" for b in r["broken"][:5]))
    if not rows and not reg and not frozen:
        print("옮길 예전 파일이 없습니다")
    elif not a.apply:
        print(f"서식 {len(rows)}개 · 사람 수정 {len(reg)}개 · 칸 목록 만들 서식 {len(frozen)}개. 목록만 보였습니다. 옮기려면 --apply")
    else:
        print(f"서식 {sum(r['status'] == '옮김' for r in rows)}개 · 사람 수정 {sum(r['status'] == '옮김' for r in reg)}개 옮김 · "
              f"칸 목록 {len(frozen)}개 만듦 (못 찾은 예전 수정 {sum(len(r['broken']) for r in frozen)}개)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
