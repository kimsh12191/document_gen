"""서식 하나 미리보기: seed·변형·촬영 조건을 받아 이미지와 라벨을 만든다 (studio 가 쓴다).

  pv = Previewer("studio_cache/preview")
  label = pv.render("hf169", seed=0, heavy="default", special="default", condition="clean")
  pv.close()

- Playwright 동기 API 는 만든 스레드에서만 쓸 수 있고 asyncio 이벤트 루프 안에서는 쓸 수 없다. 그래서 브라우저를
  전용 스레드 하나에 띄워 두고 요청을 차례로 처리한다 (서버의 어느 스레드에서 불러도 된다).
- 같은 입력이면 다시 그리지 않고 저장해 둔 결과를 돌려준다. 입력에는 서식 파일(템플릿·생성 함수·레이아웃)과 공통
  렌더링 코드의 내용 해시가 들어가므로, 서식을 고치면 새로 그린다.
- 변형(heavy, special)은 docgen/docs/_common.py 의 환경변수 스위치를 그 요청 동안만 바꿔 쓴다.
- source_hash() 는 docgen.bench build·docgen.ocr_set 도 데이터셋 기록(서식 파일 해시)에 쓴다.

명령줄 (분석기가 작업 폴더에서 html 서식을 고치며 쓴다. main() 참고):
  python -m docgen.preview <서식ID> --out <폴더>
  python -m docgen.preview --dir <template.html.j2·form.json 폴더> [--rows max] --out <폴더>
"""
from __future__ import annotations

import hashlib
import inspect
import json
import os
import random
import re
import threading
import time
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from functools import cache
from pathlib import Path

from .entities import make_profile
from .registry import load_all
from .render import render

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ("clean", "scan", "photo", "fax", "clean_jpeg")   # clean 외에는 docgen/augment.py 의 preset
MODES = ("default", "on", "off")
_ENV = {"heavy": ("DOCGEN_HEAVY", {"on": "1", "off": "0"}),
        "special": ("DOCGEN_SPECIAL", {"on": "all", "off": "none"})}
# 공란으로 그리기: 값 글자는 투명(자리·크기는 그대로), 도장·서명은 숨김.
BLANK_CSS = "<style>.fv{color:transparent!important}.seal,.scribble,.sigimg{visibility:hidden!important}</style>"
# 모든 서식이 함께 쓰는 렌더링 코드. 바뀌면 모든 미리보기를 새로 그린다.
COMMON = ["docgen/render.py", "docgen/schema.py", "docgen/image.py", "docgen/paginate.js", "docgen/augment.py",
          "docgen/realform.py", "docgen/keyrules.py", "docgen/forms/_common/key_rules.json", "docgen/entities.py", "docgen/korean.py", "docgen/banks.py", "docgen/docs/_common.py",
          "docgen/marks.py", "docgen/overrides.py", "docgen/regions.py", "docgen/sources.py", "docgen/preview.py", "docgen/forms/_common/marks.json", "docgen/assets/marks/pools.json",
          "docgen/forms/_common/templates/_base.html.j2", "docgen/forms/_common/templates/_macros.html.j2",
          "docgen/forms/_common/templates/_real_form.html.j2", "docgen/forms/_common/templates/_official_base.html.j2",
          "docgen/forms/_common/templates/_official_values.html.j2",
          "docgen/html_regions.py", "docgen/html_regions.js", "docgen/template_variants.py"]


@cache
def _source_file(fn) -> str:
    return inspect.getsourcefile(fn)


def generator_files(fn) -> list[Path]:
    """값 만드는 함수의 파일. 서식 폴더의 generate.py(코드 서식)면 그것이 가져다 쓰는 그룹 도우미 모듈(docgen/docs/<그룹>.py)도."""
    p = Path(_source_file(fn))
    if p.name != "generate.py":
        return [p]
    groups = re.findall(r"^\s*from docgen\.docs\.(\w+) import", p.read_text(encoding="utf-8"), re.M)
    return [p, *(ROOT / "docgen" / "docs" / f"{g}.py" for g in dict.fromkeys(groups) if g != "_common")]


def source_files(doc_id: str, common: bool = True) -> list[Path]:
    """이 서식의 결과를 바꾸는 파일들 (서식 전용 + 공통). common=False 면 서식 전용만 (검수 후 바뀌었는지 볼 때)."""
    from . import formdir, formfields, regions

    spec = load_all()[doc_id]
    files = [*generator_files(spec.generate), *regions.hash_files(doc_id)]
    if spec.template != "_real_form.html.j2":
        vd = formdir.variants_dir(doc_id)
        files += [vd/"variants.json"] + (sorted(vd.glob("*.html.j2")) + sorted(vd.glob("*.regions.json")) if vd.exists() else [])
    if spec.template.startswith("@form/"):   # 화면에서 만든 html 서식: 서식 폴더 (+ 복제면 부모의 생성 함수)
        from . import htmlform

        d = htmlform.form_dir(doc_id)
        files += [formdir.template_in(d), d / "form.json"] if d else []
        if d and (d / htmlform.SCRIPT).exists():   # 생성 스크립트 (없는 서식은 해시가 예전 그대로)
            files.append(d / htmlform.SCRIPT)
        parent = (htmlform.load_form(doc_id) if d else {}).get("parent")
        if parent in load_all():
            files += generator_files(load_all()[parent].generate)
            if re.fullmatch(r"hf\d{3}", parent):
                from .realform import layout_path

                lp = layout_path(int(parent[2:]))
                files += ([lp] if lp else []) + regions.hash_files(parent) + formfields.hash_files(parent)
    else:
        files.insert(0, formdir.template(doc_id) or formdir.TEMPLATES / spec.template)
    if spec.group in ("hana", "imported"):
        from .realform import form_no, layout_path

        no = form_no(doc_id)
        lp = layout_path(no) if no is not None else None
        if lp:
            files.append(lp)
        if no is not None:
            files += formfields.hash_files(doc_id)
        if no is None:
            files += formdir.image_files(doc_id)
    return files + ([ROOT / c for c in COMMON] if common else [])


_DIGESTS: dict = {}


def _file_digest(p: Path) -> bytes:
    """파일 내용 해시 (경로·mtime·크기가 같으면 다시 읽지 않는다)."""
    try:
        st = p.stat()
    except OSError:
        return b"-"
    key = (str(p), st.st_mtime_ns, st.st_size)
    d = _DIGESTS.get(key)
    if d is None:
        d = _DIGESTS[key] = hashlib.sha1(_without_questions(p) if p.name == "fields.json" else p.read_bytes()).digest()
    return d


def _without_questions(p: Path) -> bytes:
    """칸 목록의 질문 설정 "q" 는 그림을 바꾸지 않으므로 서식 해시에서 뺀다 (q 만 고치면 재검수 필요로 바뀌지 않게).
    q 가 없으면 파일 그대로, 있으면 q 를 뺀 내용을 칸 목록을 쓰는 꼴(json indent 1)로 다시 써서 잰다."""
    raw = p.read_bytes()
    if b'"q"' not in raw:
        return raw
    data = json.loads(raw)

    def strip(v):
        if isinstance(v, dict):
            return {k: strip(x) for k, x in v.items() if not (k == "q" and isinstance(x, dict))}
        if isinstance(v, list):
            return [strip(x) for x in v]
        return v
    return (json.dumps(strip(data), ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def source_hash(doc_id: str, common: bool = True) -> str:
    from .formdir import hash_label

    h = hashlib.sha1()
    for p in source_files(doc_id, common):
        name = hash_label(p)   # 서식 폴더로 옮긴 파일은 예전 자리 이름으로 (옮겨도 해시가 그대로)
        h.update(str(name.relative_to(ROOT) if name.is_relative_to(ROOT) else name).encode())
        h.update(_file_digest(p))
    out = h.hexdigest()[:12]
    if not common:   # 파일을 옮기기만 한 서식은 옮기기 전 해시 (검수 기록·데이터셋 기록이 그대로 맞게). 고치면 새 해시
        out = _moved().get(doc_id, {}).get(out, out)
    return out


@cache
def _moved() -> dict:
    """docgen/forms/_common/hash_moves.json: {서식ID: {옮긴 뒤 해시: 옮기기 전 해시}} — 내용을 바꾸지 않고 파일만 옮긴 서식."""
    p = ROOT / "docgen" / "forms" / "_common" / "hash_moves.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


class Previewer:
    def __init__(self, out_dir: str | Path, scale: float = 2.0):
        self.out = Path(out_dir)
        self.scale = scale
        self._renderer = None
        self._pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="docgen-preview")
        self._waiting = 0             # 렌더러 스레드에 줄 선 일 (남은 쪽을 찍다가 줄이 있으면 양보한다)
        self._lock = threading.Lock()
        self._finishing: Path | None = None   # 지금 남은 쪽을 찍는 폴더

    def _submit(self, fn, *args):
        with self._lock:
            self._waiting += 1

        def run():
            with self._lock:
                self._waiting -= 1
            return fn(*args)
        return self._pool.submit(run)

    def render(self, doc_id: str, seed: int = 0, heavy: str = "default", special: str = "default",
               condition: str = "clean", force: bool = False, draft: dict | None = None,
               extra: dict | None = None, rows: str | None = None, first: bool = False) -> dict:
        """라벨 dict 를 돌려준다. 이미지 경로(`images`)는 out_dir 기준 상대 경로.
        draft: 저장하지 않은 overlay 수정 (docgen/overrides.py). 주면 파일 대신 그것으로 그린다 (수정 전후 비교).
        extra: 시나리오 미리보기의 Profile.extra. 캐시에도 반영한다.
        html 서식(복제·분석기)이면 draft 는 {"template"?, "form"?} (저장하지 않은 템플릿·form.json), rows 는 반복 행 수
        "min" | "max" (없으면 서식대로 무작위). 코드 서식은 draft {"template"} (저장하지 않은 look/template.html.j2).
        draft 에 "blank": true 를 더하면 값 글자·도장·서명을 안 보이게 그린다 (자리·위치는 같음, studio 자리·템플릿 화면).
        "texts": true 면 라벨에 쪽 전체 글자 박스 texts, "fields": 저장하지 않은 칸 목록, "variant": 그 레이아웃 변형의 템플릿 초안.
        first=True (화면 미리보기): 1쪽을 찍으면 바로 돌려주고 남은 쪽은 렌더러가 이어서 찍는다 (다른 요청이 오면 양보).
        그동안 폴더에 pending.json 이 있고, 남은 쪽 그림은 complete(폴더) 가 마저 만든다. first=False 면 늘 모든 쪽이 있다."""
        reg = load_all()
        if doc_id not in reg:
            raise KeyError(f"알 수 없는 서식: {doc_id}")
        if heavy not in MODES or special not in MODES:
            raise ValueError(f"heavy·special 은 {MODES} 중 하나")
        if condition not in CONDITIONS:
            raise ValueError(f"condition 은 {CONDITIONS} 중 하나")
        if rows not in (None, "auto", "min", "max"):
            raise ValueError("rows 는 auto / min / max")
        rows = None if rows == "auto" else rows
        if extra is not None and not isinstance(extra, dict):
            raise ValueError("프로필 값은 JSON 객체여야 합니다")
        extra = json.loads(json.dumps(extra or {}, sort_keys=True))
        from .overrides import digest

        src = source_hash(doc_id) + ("" if draft is None else ":draft:" + digest(draft))
        key = hashlib.sha1(json.dumps([doc_id, seed, heavy, special, condition, self.scale, src, extra]
                                      + ([rows] if rows else [])).encode()).hexdigest()[:16]
        folder = self.out / doc_id / key
        label_path = folder / "label.json"
        if label_path.exists() and not force:
            if first or not (folder / "pending.json").exists():
                return json.loads(label_path.read_text(encoding="utf-8"))
            return self.complete(folder)
        args = (doc_id, seed, heavy, special, condition, src, folder, draft, extra, rows)
        if not (first and condition == "clean" and draft is None):
            return self._submit(self._render, *args).result()
        early: Future = Future()
        task = self._submit(self._render, *args, early)
        wait([early, task], return_when=FIRST_COMPLETED)
        return early.result() if early.done() else task.result()

    def finishing(self, folder: Path) -> bool:
        """그 폴더의 남은 쪽을 지금 찍고 있나 (또는 찍으려고 줄 서 있나)."""
        return self._finishing is not None and Path(folder) == self._finishing

    def complete(self, folder: Path) -> dict:
        """first=True 로 그린 폴더의 남은 쪽까지 (남은 쪽을 찍다 양보했으면 다시 그린다)."""
        folder = Path(folder)
        pending = folder / "pending.json"
        if not pending.exists():
            return json.loads((folder / "label.json").read_text(encoding="utf-8"))
        a = json.loads(pending.read_text(encoding="utf-8"))
        return self.render(a["doc_id"], a["seed"], a["heavy"], a["special"], "clean", True, None, a["extra"], a["rows"])

    def warm(self) -> None:
        """브라우저를 미리 띄운다 (첫 미리보기가 약 1초 빨라진다). 기다리지 않는다."""
        self._submit(self._ensure_renderer)

    def call(self, fn, *args):
        """렌더러 스레드에서 fn(*args) 를 돌린다 (배경 그림처럼 렌더링과 같은 스레드 상태가 필요한 일)."""
        return self._submit(fn, *args).result()

    def close(self) -> None:
        def stop():
            if self._renderer:
                self._renderer.__exit__(None, None, None)
                self._renderer = None
        self._pool.submit(stop).result()
        self._pool.shutdown()

    # 아래는 전용 스레드에서만 돈다
    def _ensure_renderer(self):
        if self._renderer is None:
            from .image import ImageRenderer

            self._renderer = ImageRenderer(scale=self.scale).__enter__()
        return self._renderer

    def _render(self, doc_id, seed, heavy, special, condition, src, folder: Path, draft: dict | None = None,
                extra: dict | None = None, rows: str | None = None, early: Future | None = None) -> dict:
        from contextlib import nullcontext

        from . import overrides
        from .cli import _aug_fields
        from .schema import build_fields
        from .bench.perturb import visible_keys

        self._ensure_renderer()
        spec = load_all()[doc_id]
        blank, texts = bool((draft or {}).get("blank")), bool((draft or {}).get("texts"))
        fields_draft, variant = (draft or {}).get("fields"), (draft or {}).get("variant") or "default"
        if draft is not None:
            draft = {k: v for k, v in draft.items() if k not in ("blank", "texts", "fields", "variant")} or None
        folder.mkdir(parents=True, exist_ok=True)
        t0 = time.time()
        saved = {name: os.environ.get(var) for name, (var, _) in _ENV.items()}
        try:
            for name, mode in (("heavy", heavy), ("special", special)):
                var, values = _ENV[name]
                if mode == "default":
                    os.environ.pop(var, None)
                else:
                    os.environ[var] = values[mode]
            if variant != "default" and draft is not None and "template" in draft:   # 레이아웃 변형 템플릿 초안
                from . import formdir

                ctx = formdir.template_draft(doc_id, draft["template"], variant)
            elif spec.template.startswith("@form/"):
                from . import htmlform

                ctx = htmlform.draft(doc_id, draft, rows)
            elif draft is not None and "template" in draft:
                from . import formdir

                ctx = formdir.template_draft(doc_id, draft["template"])
            else:
                ctx = overrides.draft(doc_id, draft) if draft is not None else nullcontext()
            from . import html_regions
            region_draft = (draft or {}).get("html_regions")
            from . import formfields
            fctx = formfields.draft(doc_id, fields_draft) if fields_draft is not None else nullcontext()
            with ctx, fctx, html_regions.draft(doc_id, region_draft):
                profile = make_profile(seed)
                profile.extra.update(extra or {})
                html, raw, data = render(spec, profile, seed)
                if blank:
                    html = html.replace("</head>", BLANK_CSS + "</head>", 1)
                info = self._renderer.render(html, folder / "page.png", **({"texts": True} if texts else {}),
                                             **({"first_only": True} if early else {}))
                checks = None
                if spec.template.startswith("@form/"):   # html 서식: 저장 전 검사 (선언·템플릿 키, 쪽 넘침)
                    checks = htmlform.check(htmlform.load_form(doc_id), raw, data, bool(info.get("overflow")), doc_id)
        finally:
            for name, (var, _) in _ENV.items():
                if saved[name] is None:
                    os.environ.pop(var, None)
                else:
                    os.environ[var] = saved[name]
        fields = build_fields(raw, info)
        images = [Path(p) for p in info["images"]]
        pages = info["pages"]
        if condition != "clean":
            from PIL import Image

            from .augment import augment

            rng = random.Random(f"aug:{doc_id}:{seed}:{condition}")
            aug_images, pages, tfs = [], [], []
            for p in images:
                img, _, tf = augment(Image.open(p), rng, condition, with_transform=True)
                ap = p.with_name(f"{p.stem}_{condition}.jpg")
                img.save(ap, quality=92)
                aug_images.append(ap)
                pages.append({"width": img.size[0], "height": img.size[1]})
                tfs.append(tf)
            images = aug_images
            fields = _aug_fields(fields, tfs)
        label = {
            "doc_type": doc_id, "doc_name": spec.name, "group": spec.group, "seed": seed, "heavy": heavy,
            "special": special, "condition": condition, "source_hash": src,
            "images": [str(p.relative_to(self.out)).replace("\\", "/") for p in images],
            "pages": pages, "overflow": info["overflow"], "fields": fields,
            "anchors": [{**a, **{k: next((f for f in raw if f["key"] == a["key"]), {}).get(k) for k in ("type", "label")}}
                        for a in info.get("anchors", [])] if condition == "clean" else [],
            "editable_fields": [{k: f.get(k) for k in ("key", "type", "label", "value", "present")} for f in raw]
                               if spec.template != "_real_form.html.j2" else [],
            "scale": self.scale,
            "template_variant": data.get("_template_variant", {"id":"default","name":"기본 레이아웃"}),
            "raw_keys": [f["key"] for f in raw],
            "visible": sorted(visible_keys(html)),
            "writing": "hand" if spec.group in ("hana", "imported") and (data or {}).get("style", {}).get("hand") else "print",
            "elapsed": round(time.time() - t0, 2),
            **({"texts": info.get("texts", [])} if texts else {}),
            **({"checks": checks, "rows": rows or "auto"} if checks is not None else {}),
        }
        pending = folder / "pending.json"
        rest = info.get("rest")
        if rest:   # 1쪽만 찍었다: 라벨을 먼저 돌려주고 남은 쪽을 찍는다
            pending.write_text(json.dumps({"doc_id": doc_id, "seed": seed, "heavy": heavy, "special": special,
                                           "extra": extra, "rows": rows}, ensure_ascii=False), encoding="utf-8")
            (folder / "label.json").write_text(json.dumps(label, ensure_ascii=False), encoding="utf-8")
            self._finishing = folder   # 돌려주기 전에: 바로 온 남은 쪽 요청이 기다리게
            early.set_result(label)
            try:
                if self._renderer.finish(rest, stop=lambda: self._waiting > 0):
                    pending.unlink()
            except Exception as e:  # noqa: BLE001 — 남은 쪽은 complete() 가 다시 그린다
                print(f"preview: {doc_id} 남은 쪽을 찍지 못함 ({type(e).__name__}: {e})", flush=True)
            finally:
                self._finishing = None
            return label
        pending.unlink(missing_ok=True)
        (folder / "label.json").write_text(json.dumps(label, ensure_ascii=False), encoding="utf-8")
        if early is not None:
            early.set_result(label)
        return label


def main(argv=None) -> None:
    """명령줄 미리보기 (분석기 CLI 가 작업 폴더 안에서 html 서식을 고치며 쓴다).

      python -m docgen.preview <서식ID> [--seed 0] [--rows auto|min|max] [--condition clean] --out <폴더>
      python -m docgen.preview --dir <template.html.j2·form.json 이 있는 폴더> [--seed 0] [--rows max] --out <폴더>

    <폴더>/<서식>/<키>/page*.png 와 label.json 을 쓰고, 쪽 수·항목 수·검사 결과를 JSON 한 줄로 출력한다."""
    import argparse

    ap = argparse.ArgumentParser(prog="docgen.preview", description="서식 하나를 렌더링해 쪽 그림·라벨·검사 결과를 낸다")
    ap.add_argument("doc_id", nargs="?")
    ap.add_argument("--dir", help="저장하지 않은 html 서식 폴더 (template.html.j2 + form.json)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--rows", default="auto", choices=["auto", "min", "max"])
    ap.add_argument("--condition", default="clean", choices=CONDITIONS)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    draft = None
    doc_id = a.doc_id
    if a.dir:
        from . import htmlform
        from .registry import GROUPS, REGISTRY, DocSpec

        d = Path(a.dir)
        form = json.loads((d / "form.json").read_text(encoding="utf-8"))
        draft = {"template": (d / "template.html.j2").read_text(encoding="utf-8"), "form": form,
                 "script": str(d / htmlform.SCRIPT) if (d / htmlform.SCRIPT).exists() else None}
        load_all()
        doc_id = "draft_" + "".join(c if c.isalnum() else "_" for c in d.resolve().name.lower())
        REGISTRY[doc_id] = DocSpec(doc_id, form.get("name") or doc_id, form.get("group") if form.get("group") in GROUPS else "imported",
                                   form.get("category", "external"), htmlform.PREFIX + doc_id, htmlform.make_generate(doc_id),
                                   form.get("page", "a4"), False, "명령줄 미리보기", form.get("origin", "analyzer"))
    if not doc_id:
        ap.error("서식 ID 또는 --dir")
    pv = Previewer(a.out)
    try:
        label = pv.render(doc_id, a.seed, condition=a.condition, force=True, draft=draft, rows=a.rows)
    finally:
        pv.close()
    out = Path(a.out)
    print(json.dumps({"images": [str(out / p) for p in label["images"]], "pages": len(label["images"]),
                      "fields": len(label["fields"]), "empty": sum(1 for f in label["fields"] if f.get("value") in (None, "")),
                      "overflow": label["overflow"], "checks": label.get("checks", [])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
