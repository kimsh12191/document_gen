"""서류별 대표 샘플 이미지와 정답 JSON 을 samples/ 에 저장한다.

  python scripts/make_samples.py            # 서류당 1장 (seed 7)
  python scripts/make_samples.py --per 3    # 서류당 3장

은행 서식은 --banks 의 은행별로 samples/bank_variants/<은행>/ 에도 1장씩 만든다.
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PIL import Image  # noqa: E402

from docgen.banks import LEGACY, supports  # noqa: E402
from docgen.entities import make_profile  # noqa: E402
from docgen.image import ImageRenderer  # noqa: E402
from docgen.registry import GROUPS, load_all  # noqa: E402
from docgen.render import render, to_nested  # noqa: E402
from docgen.schema import build_fields  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "samples"))
    ap.add_argument("--per", type=int, default=1)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--scale", type=float, default=1.5)
    ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--banks", default="하나은행,KEB하나은행,외환은행", help="은행 서식 은행별 샘플 (빈 값이면 생략)")
    args = ap.parse_args()

    reg = load_all()
    out = Path(args.out)
    index = []
    tmp = out / "_tmp.png"
    out.mkdir(parents=True, exist_ok=True)
    with ImageRenderer(scale=args.scale) as r:
        for spec in sorted(reg.values(), key=lambda s: (list(GROUPS).index(s.group), s.id)):
            (out / spec.group).mkdir(exist_ok=True)
            for k in range(args.per):
                seed = args.seed + k
                prof = make_profile(seed)
                prof.extra["form_bank"] = prof.bank  # 대표 샘플은 프로필 은행 그대로 (은행별은 bank_variants/)
                html, fields, _ = render(spec, prof, seed)
                info = r.render(html, tmp)
                name = spec.id if args.per == 1 else f"{spec.id}_{k}"
                img = Image.open(tmp).convert("RGB")
                buf = io.BytesIO()
                img.save(buf, "JPEG", quality=args.quality, optimize=True)
                (out / spec.group / f"{name}.jpg").write_bytes(buf.getvalue())
                gt = {"document_type": spec.name, **to_nested(build_fields(fields, info))}
                (out / spec.group / f"{name}.json").write_text(json.dumps(gt, ensure_ascii=False, indent=1), encoding="utf-8")
                index.append({"id": spec.id, "name": spec.name, "group": spec.group, "group_name": GROUPS[spec.group],
                              "category": spec.category, "image": f"{spec.group}/{name}.jpg",
                              "gt": f"{spec.group}/{name}.json", "n_fields": len(fields),
                              "overflow": info["overflow"], "size": [img.width, img.height]})
                print(f"{spec.id:40s} {len(fields):4d} fields{'  OVERFLOW' if info['overflow'] else ''}")
        for bank in [b for b in args.banks.split(",") if b]:
            d = out / "bank_variants" / bank
            d.mkdir(parents=True, exist_ok=True)
            for spec in sorted(reg.values(), key=lambda s: s.id):
                if spec.group != "bank_form" or not supports(bank, spec.id):
                    continue
                prof = make_profile(args.seed, None if bank in LEGACY else bank)
                prof.extra["form_bank"] = bank
                html, fields, _ = render(spec, prof, args.seed)
                info = r.render(html, tmp)
                img = Image.open(tmp).convert("RGB")
                buf = io.BytesIO()
                img.save(buf, "JPEG", quality=args.quality, optimize=True)
                (d / f"{spec.id}.jpg").write_bytes(buf.getvalue())
                gt = {"document_type": spec.name, **to_nested(build_fields(fields, info))}
                (d / f"{spec.id}.json").write_text(json.dumps(gt, ensure_ascii=False, indent=1), encoding="utf-8")
                index.append({"id": spec.id, "name": spec.name, "group": spec.group, "group_name": GROUPS[spec.group],
                              "category": spec.category, "bank": bank,
                              "image": f"bank_variants/{bank}/{spec.id}.jpg", "gt": f"bank_variants/{bank}/{spec.id}.json",
                              "n_fields": len(fields), "overflow": info["overflow"], "size": [img.width, img.height]})
                print(f"{bank:8s} {spec.id:32s} {len(fields):4d} fields{'  OVERFLOW' if info['overflow'] else ''}")
    tmp.unlink(missing_ok=True)
    (out / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(index)}장 → {out}")


if __name__ == "__main__":
    main()
