"""서식 하나 미리보기: seed·변형·촬영 조건을 받아 이미지와 라벨을 만든다 (studio 가 쓴다).

  pv = Previewer("studio_cache/preview")
  label = pv.render("hf169", seed=0, heavy="default", special="default", condition="clean")
  pv.close()

- Playwright 동기 API 는 만든 스레드에서만 쓸 수 있고 asyncio 이벤트 루프 안에서는 쓸 수 없다. 그래서 브라우저를
  전용 스레드 하나에 띄워 두고 요청을 차례로 처리한다 (서버의 어느 스레드에서 불러도 된다).
- 같은 입력이면 다시 그리지 않고 저장해 둔 결과를 돌려준다. 입력에는 서식 파일(템플릿·생성 함수·레이아웃)과 공통
  렌더링 코드의 내용 해시가 들어가므로, 서식을 고치면 새로 그린다.
- 변형(heavy, special)은 docgen/docs/_common.py 의 환경변수 스위치를 그 요청 동안만 바꿔 쓴다.
"""
from __future__ import annotations

import hashlib
import inspect
import json
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor
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
          "docgen/realform.py", "docgen/entities.py", "docgen/korean.py", "docgen/banks.py", "docgen/docs/_common.py",
          "templates/_base.html.j2", "templates/_macros.html.j2", "templates/_real_form.html.j2"]


def source_files(doc_id: str) -> list[Path]:
    """이 서식의 결과를 바꾸는 파일들 (서식 전용 + 공통)."""
    spec = load_all()[doc_id]
    files = [ROOT / "templates" / spec.template, Path(inspect.getsourcefile(spec.generate))]
    if spec.group == "hana":
        from .realform import layout_path

        lp = layout_path(int(doc_id[2:]))
        if lp:
            files.append(lp)
    return files + [ROOT / c for c in COMMON]


def source_hash(doc_id: str) -> str:
    h = hashlib.sha1()
    for p in source_files(doc_id):
        h.update(str(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p).encode())
        h.update(p.read_bytes() if p.exists() else b"-")
    return h.hexdigest()[:12]


class Previewer:
    def __init__(self, out_dir: str | Path, scale: float = 2.0):
        self.out = Path(out_dir)
        self.scale = scale
        self._renderer = None
        self._pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="docgen-preview")

    def render(self, doc_id: str, seed: int = 0, heavy: str = "default", special: str = "default",
               condition: str = "clean", force: bool = False) -> dict:
        """라벨 dict 를 돌려준다. 이미지 경로(`images`)는 out_dir 기준 상대 경로."""
        reg = load_all()
        if doc_id not in reg:
            raise KeyError(f"알 수 없는 서식: {doc_id}")
        if heavy not in MODES or special not in MODES:
            raise ValueError(f"heavy·special 은 {MODES} 중 하나")
        if condition not in CONDITIONS:
            raise ValueError(f"condition 은 {CONDITIONS} 중 하나")
        src = source_hash(doc_id)
        key = hashlib.sha1(json.dumps([doc_id, seed, heavy, special, condition, self.scale, src]).encode()).hexdigest()[:16]
        folder = self.out / doc_id / key
        label_path = folder / "label.json"
        if label_path.exists() and not force:
            return json.loads(label_path.read_text(encoding="utf-8"))
        return self._pool.submit(self._render, doc_id, seed, heavy, special, condition, src, folder).result()

    def close(self) -> None:
        def stop():
            if self._renderer:
                self._renderer.__exit__(None, None, None)
                self._renderer = None
        self._pool.submit(stop).result()
        self._pool.shutdown()

    # 아래는 전용 스레드에서만 돈다
    def _render(self, doc_id, seed, heavy, special, condition, src, folder: Path) -> dict:
        from .cli import _aug_fields
        from .schema import build_fields

        if self._renderer is None:
            from .image import ImageRenderer

            self._renderer = ImageRenderer(scale=self.scale).__enter__()
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
            html, raw, _ = render(spec, make_profile(seed), seed)
        finally:
            for name, (var, _) in _ENV.items():
                if saved[name] is None:
                    os.environ.pop(var, None)
                else:
                    os.environ[var] = saved[name]
        info = self._renderer.render(html, folder / "page.png")
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
            "elapsed": round(time.time() - t0, 2),
        }
        (folder / "label.json").write_text(json.dumps(label, ensure_ascii=False), encoding="utf-8")
        return label
