"""서류별 대표 샘플 이미지와 정답 JSON 을 samples/ 에 저장한다.

  python scripts/make_samples.py            # 서류당 1장 (seed 7)
  python scripts/make_samples.py --per 3    # 서류당 3장

추가로 만드는 것:
  samples/variants/<서류ID>*.jpg       내용이 많은 경우 + 특수 상황을 모두 켠 샘플 (여러 쪽이면 _p1, _p2 ...)
  samples/bank_variants/<은행>/         은행 서식의 은행별 샘플 (--banks)
샘플마다 <이름>.json(정답)과 <이름>.label.json(필드별 타입·위치) 을 함께 저장한다.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PIL import Image  # noqa: E402

from docgen.banks import LEGACY, supports  # noqa: E402
from docgen.entities import make_profile  # noqa: E402
from docgen.image import ImageRenderer  # noqa: E402
from docgen.registry import BANK_FORM_GROUPS, GROUPS, load_all  # noqa: E402
from docgen.render import render, to_nested  # noqa: E402
from docgen.schema import build_fields  # noqa: E402


@contextlib.contextmanager
def forced(heavy: bool):
    """DOCGEN_HEAVY / DOCGEN_SPECIAL 을 잠시 켠다."""
    old = {k: os.environ.get(k) for k in ("DOCGEN_HEAVY", "DOCGEN_SPECIAL")}
    if heavy:
        os.environ.update(DOCGEN_HEAVY="1", DOCGEN_SPECIAL="all")
    else:
        os.environ.update(DOCGEN_HEAVY="0", DOCGEN_SPECIAL="none")
    try:
        yield
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def save(r, args, spec, prof, seed, folder: Path, name: str, out: Path, extra: dict) -> dict:
    html, raw, _ = render(spec, prof, seed)
    tmp = out / "_tmp.png"
    info = r.render(html, tmp)
    imgs = []
    for i, p in enumerate(info["images"]):
        img = Image.open(p).convert("RGB")
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=args.quality, optimize=True)
        fn = f"{name}.jpg" if len(info["images"]) == 1 else f"{name}_p{i + 1}.jpg"
        (folder / fn).write_bytes(buf.getvalue())
        imgs.append(str((folder / fn).relative_to(out)))
        Path(p).unlink(missing_ok=True)
    fields = build_fields(raw, info)
    gt = {"document_type": spec.name, **to_nested(fields)}
    (folder / f"{name}.json").write_text(json.dumps(gt, ensure_ascii=False, indent=1), encoding="utf-8")
    (folder / f"{name}.label.json").write_text(json.dumps({"images": imgs, "pages": info["pages"], "fields": fields},
                                                          ensure_ascii=False, indent=1), encoding="utf-8")
    rel = folder.relative_to(out)
    entry = {"id": spec.id, "name": spec.name, "group": spec.group, "group_name": GROUPS[spec.group],
             "category": spec.category, **extra, "image": imgs[0], "images": imgs, "n_pages": len(imgs),
             "gt": f"{rel}/{name}.json", "label": f"{rel}/{name}.label.json",
             "n_fields": sum(1 for f in fields if not f.get("group")), "overflow": info["overflow"],
             "size": [info["width"], info["height"]]}
    pg = f" {len(imgs)}쪽" if len(imgs) > 1 else ""
    print(f"{extra.get('bank', extra.get('kind', '')):8s} {spec.id:40s} {entry['n_fields']:4d} fields{pg}"
          f"{'  OVERFLOW' if info['overflow'] else ''}")
    return entry


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "samples"))
    ap.add_argument("--per", type=int, default=1)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--scale", type=float, default=1.5)
    ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--banks", default="하나은행,KEB하나은행,외환은행", help="은행 서식 은행별 샘플 (빈 값이면 생략)")
    ap.add_argument("--no-variants", action="store_true", help="여러 쪽·특수 상황 샘플 생략")
    args = ap.parse_args()

    reg = load_all()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    index = []
    specs = sorted(reg.values(), key=lambda s: (list(GROUPS).index(s.group), s.id))
    with ImageRenderer(scale=args.scale) as r:
        with forced(False):  # 대표 샘플: 보통 경우
            for spec in specs:
                (out / spec.group).mkdir(exist_ok=True)
                for k in range(args.per):
                    seed = args.seed + k
                    prof = make_profile(seed)
                    prof.extra["form_bank"] = prof.bank  # 대표 샘플은 프로필 은행 그대로 (은행별은 bank_variants/)
                    name = spec.id if args.per == 1 else f"{spec.id}_{k}"
                    index.append(save(r, args, spec, prof, seed, out / spec.group, name, out, {"kind": "basic"}))
        if not args.no_variants:
            (out / "variants").mkdir(exist_ok=True)
            with forced(True):
                for spec in specs:
                    prof = make_profile(args.seed)
                    prof.extra["form_bank"] = prof.bank
                    index.append(save(r, args, spec, prof, args.seed, out / "variants", spec.id, out, {"kind": "variant"}))
        with forced(False):
            for bank in [b for b in args.banks.split(",") if b]:
                d = out / "bank_variants" / bank
                d.mkdir(parents=True, exist_ok=True)
                for spec in specs:
                    if spec.group not in BANK_FORM_GROUPS or not supports(bank, spec.id):
                        continue
                    prof = make_profile(args.seed, None if bank in LEGACY else bank)
                    prof.extra["form_bank"] = bank
                    index.append(save(r, args, spec, prof, args.seed, d, spec.id, out, {"kind": "bank", "bank": bank}))
    (out / "_tmp.png").unlink(missing_ok=True)
    (out / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(index)}건 → {out}")


if __name__ == "__main__":
    main()
