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
# 모든 서식이 함께 쓰는 렌더링 코드. 바뀌면 모든 미리보기를 새로 그린다.
COMMON = ["docgen/render.py", "docgen/schema.py", "docgen/image.py", "docgen/paginate.js", "docgen/augment.py",
          "docgen/realform.py", "docgen/keyrules.py", "docgen/key_rules.json", "docgen/entities.py", "docgen/korean.py", "docgen/banks.py", "docgen/docs/_common.py",
          "docgen/marks.py", "docgen/overrides.py", "docgen/sources.py", "docgen/preview.py", "docgen/marks.json", "docgen/assets/marks/pools.json",
          "docgen/templates/_base.html.j2", "docgen/templates/_macros.html.j2", "docgen/templates/_real_form.html.j2",
          "docgen/templates/_official_base.html.j2", "docgen/templates/_official_values.html.j2",
          "docgen/html_regions.py", "docgen/html_regions.js", "docgen/template_variants.py"]


@cache
def _source_file(fn) -> str:
    return inspect.getsourcefile(fn)


def source_files(doc_id: str, common: bool = True) -> list[Path]:
    """이 서식의 결과를 바꾸는 파일들 (서식 전용 + 공통). common=False 면 서식 전용만 (검수 후 바뀌었는지 볼 때)."""
    from . import overrides

    spec = load_all()[doc_id]
    files = [Path(_source_file(spec.generate)), overrides.path(doc_id)]
    if spec.template != "_real_form.html.j2":
        from . import html_regions

        files.append(html_regions.path(doc_id))
        from .template_variants import folder
        vd=folder(doc_id)
        files += [vd/"variants.json"] + (sorted(vd.glob("*.html.j2")) + sorted(vd.glob("*.regions.json")) if vd.exists() else [])
    if spec.template.startswith("@form/"):   # 화면에서 만든 html 서식: 서식 폴더 (+ 복제면 부모의 생성 함수)
        from . import htmlform

        d = htmlform.form_dir(doc_id)
        files += [d / "template.html.j2", d / "form.json"] if d else []
        parent = (htmlform.load_form(doc_id) if d else {}).get("parent")
        if parent in load_all():
            files.append(Path(_source_file(load_all()[parent].generate)))
            if re.fullmatch(r"hf\d{3}", parent):
                from .realform import layout_path

                lp = layout_path(int(parent[2:]))
                files += ([lp] if lp else []) + [overrides.path(parent)]
    else:
        files.insert(0, ROOT / "docgen" / "templates" / spec.template)
    if spec.group in ("hana", "imported"):
        from .realform import form_no, image_form_dir, layout_path

        no = form_no(doc_id)
        lp = layout_path(no) if no is not None else None
        if lp:
            files.append(lp)
        d = image_form_dir(doc_id) if no is None else None
        if d:
            files += [f for f in sorted(d.iterdir()) if f.is_file() and f.name != "overrides.json"]
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
        d = _DIGESTS[key] = hashlib.sha1(p.read_bytes()).digest()
    return d


def source_hash(doc_id: str, common: bool = True) -> str:
    h = hashlib.sha1()
    for p in source_files(doc_id, common):
        h.update(str(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p).encode())
        h.update(_file_digest(p))
    return h.hexdigest()[:12]


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
        "min" | "max" (없으면 서식대로 무작위).
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
            if spec.template.startswith("@form/"):
                from . import htmlform

                ctx = htmlform.draft(doc_id, draft, rows)
            else:
                ctx = overrides.draft(doc_id, draft) if draft is not None else nullcontext()
            from . import html_regions
            region_draft = (draft or {}).get("html_regions")
            with ctx, html_regions.draft(doc_id, region_draft):
                profile = make_profile(seed)
                profile.extra.update(extra or {})
                html, raw, data = render(spec, profile, seed)
                info = self._renderer.render(html, folder / "page.png", **({"first_only": True} if early else {}))
                checks = None
                if spec.template.startswith("@form/"):   # html 서식: 저장 전 검사 (선언·템플릿 키, 쪽 넘침)
                    checks = htmlform.check(htmlform.load_form(doc_id), raw, data, bool(info.get("overflow")))
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
        draft = {"template": (d / "template.html.j2").read_text(encoding="utf-8"), "form": form}
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
